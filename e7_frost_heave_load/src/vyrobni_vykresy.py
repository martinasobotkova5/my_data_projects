"""E7 rev. B3 – výrobní výkresy jednotlivých dílů (DXF s kótami + PDF), pro dílnu i pro import do Onshape.

Pohledy se počítají přesně z 3D modelu dílu (skryté hrany HLR, OpenCASCADE), kóty jsou skutečné DIMENSION
entity (v Onshape / AutoCAD / LibreCAD je lze upravovat). Otvory se čtou z modelu a vypisují se do tabulky
souřadnic od výchozího rohu (laserové desky) nebo od středu (kotouče).

Run: python vyrobni_vykresy.py → ../vyroba/vykresy/<díl>.dxf + E7_vyrobni_vykresy.pdf
"""
import datetime
import math
import os

import cadquery as cq
import ezdxf
from ezdxf.enums import TextEntityAlignment
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape

import buildparts as bp
import params as p

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "vyroba", "vykresy")
TODAY = datetime.date.today().isoformat()
SCALES = (1, 1.5, 2, 2.5, 3, 4, 5)
VIEWS = {  # view direction (from the eye towards the part), x direction on paper
    "top": ((0, 0, 1), (1, 0, 0)),
    "front": ((0, -1, 0), (1, 0, 0)),
    "right": ((1, 0, 0), (0, 1, 0)),
}


# ---------------------------------------------------------------------------------- projection
def project(solid, view):
    """Visible / hidden 2D edges of `solid` seen from `view` → (vis polylines, hid polylines, circles)."""
    d, xd = VIEWS[view]
    algo = HLRBRep_Algo()
    algo.Add(solid.val().wrapped if hasattr(solid, "val") else solid.wrapped)
    algo.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(*d), gp_Dir(*xd))))
    algo.Update()
    algo.Hide()
    h = HLRBRep_HLRToShape(algo)

    def edges(comp):
        if comp is None or comp.IsNull():
            return []
        return cq.Shape.cast(comp).Edges()
    vis = edges(h.VCompound()) + edges(h.OutLineVCompound()) + edges(h.Rg1LineVCompound())
    hid = edges(h.HCompound()) + edges(h.OutLineHCompound())

    def poly(e):
        if e.geomType() == "LINE":
            a, b = e.startPoint(), e.endPoint()
            return [(a.x, a.y), (b.x, b.y)]
        n = max(8, int(e.Length() / 1.0))
        return [(q.x, q.y) for q in e.positions([i / n for i in range(n + 1)])]
    circles = []
    for e in vis:
        if e.geomType() == "CIRCLE" and e.IsClosed():
            c = e.arcCenter()
            circles.append((round(c.x, 2), round(c.y, 2), round(2 * e.radius(), 2)))
    return [poly(e) for e in vis], [poly(e) for e in hid], sorted(set(circles))


def bbox(polys):
    xs = [x for pl in polys for x, _ in pl]
    ys = [y for pl in polys for _, y in pl]
    return min(xs), min(ys), max(xs), max(ys)


# ---------------------------------------------------------------------------------- DXF sheet
def new_doc(S):
    doc = ezdxf.new("R2010", setup=True, units=4)
    for name, color, lt in (("OUTLINE", 7, "CONTINUOUS"), ("HIDDEN", 8, "DASHED"), ("CENTER", 8, "CENTER"),
                            ("DIM", 7, "CONTINUOUS"), ("TEXT", 7, "CONTINUOUS"), ("FRAME", 7, "CONTINUOUS")):
        lay = doc.layers.add(name, color=color, linetype=lt)
        if name != "HIDDEN" and name != "CENTER":
            lay.rgb = (0, 0, 0)
    ds = doc.dimstyles.new("E7")
    ds.dxf.dimtxt, ds.dxf.dimasz = 3.0 * S, 2.5 * S
    ds.dxf.dimexe, ds.dxf.dimexo, ds.dxf.dimgap = 1.5 * S, 1.0 * S, 0.8 * S
    ds.dxf.dimdec, ds.dxf.dimdsep, ds.dxf.dimzin = 2, ord(","), 8
    ds.dxf.dimtad, ds.dxf.dimtih, ds.dxf.dimtoh = 1, 0, 0
    ds.dxf.dimclrd = ds.dxf.dimclre = ds.dxf.dimclrt = 256
    ds.dxf.dimtxsty = "OpenSans"
    doc.header["$LTSCALE"] = S
    return doc


class Drawing:
    def __init__(self, info, S, paper=(297.0, 210.0)):
        self.S, self.info = S, info
        self.W, self.H = paper[0] * S, paper[1] * S
        self.doc = new_doc(S)
        self.m = self.doc.modelspace()

    def pl(self, pts, layer="OUTLINE", ox=0, oy=0, close=False):
        self.m.add_lwpolyline([(ox + x, oy + y) for x, y in pts], close=close, dxfattribs={"layer": layer})

    def text(self, s, at, h=3.0, align=TextEntityAlignment.LEFT, layer="TEXT"):
        t = self.m.add_text(s, height=h * self.S, dxfattribs={"layer": layer, "style": "OpenSans"})
        t.set_placement(at, align=align)

    def dim_h(self, x0, x1, y, ybase, text="<>"):
        self.m.add_linear_dim(base=(x0, ybase), p1=(x0, y), p2=(x1, y), angle=0, dimstyle="E7", text=text,
                              dxfattribs={"layer": "DIM"}).render()

    def dim_v(self, y0, y1, x, xbase, text="<>"):
        self.m.add_linear_dim(base=(xbase, y0), p1=(x, y0), p2=(x, y1), angle=90, dimstyle="E7", text=text,
                              dxfattribs={"layer": "DIM"}).render()

    def dim_d(self, c, r, ang=45, text="<>"):
        self.m.add_diameter_dim(center=c, radius=r, angle=ang, dimstyle="E7", text=text,
                                dxfattribs={"layer": "DIM"}).render()

    def view(self, solid, which, ox, oy, label=None, dims=True, hidden=True):
        """Draw a projected view with its lower-left corner at (ox, oy); returns (bbox, circles) in sheet coords."""
        vis, hid, circ = project(solid, which)
        x0, y0, x1, y1 = bbox(vis)
        dx, dy = ox - x0, oy - y0
        for pts in vis:
            self.pl(pts, "OUTLINE", dx, dy)
        if hidden:
            for pts in hid:
                self.pl(pts, "HIDDEN", dx, dy)
        circ = [(cx + dx, cy + dy, d) for cx, cy, d in circ]
        b = (ox, oy, ox + x1 - x0, oy + y1 - y0)
        if dims:
            self.dim_h(b[0], b[2], b[1], b[1] - 8 * self.S)
            self.dim_v(b[1], b[3], b[0], b[0] - 8 * self.S)
        if label:
            self.text(label, (b[0], b[3] + 4 * self.S), h=3.5)
        return b, circ

    def title_block(self, scale_txt):
        S, W = self.S, self.W
        w, h = 180 * S, 32 * S
        x0, y0 = W - 10 * S - w, 8 * S
        self.pl([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], "FRAME", close=True)
        for k in (8, 16, 24):
            self.pl([(x0, y0 + k * S), (x0 + w, y0 + k * S)], "FRAME")
        i = self.info
        rows = [(f"{i['no']}  {i['name']}", f"ks: {i['qty']}"),
                (f"materiál: {i['mat']}", f"měřítko {scale_txt}"),
                ("nekótované tolerance ISO 2768-mK, hrany odjehlit 0,3", "rozměry v mm"),
                ("E7 – zatěžovací zkouška mrznutí a tání, varianta C rev. B3", f"{TODAY}  návrh")]
        for k, (a, b) in enumerate(rows):
            yy = y0 + h - (k + 1) * 8 * S + 2.4 * S
            self.text(a, (x0 + 2 * S, yy), h=3.6 if k == 0 else 3.0)
            self.text(b, (x0 + w - 2 * S, yy), h=3.0, align=TextEntityAlignment.RIGHT)

    def notes(self, lines, x, y):
        for k, s in enumerate(lines):
            self.text(s, (x, y - k * 5 * self.S), h=3.0)

    def hole_table(self, circles, ref, x, y, title="OTVORY (od výchozího bodu ◎)"):
        groups = {}
        for cx, cy, d in circles:
            groups.setdefault(d, []).append((cx - ref[0], cy - ref[1]))
        self.text(title, (x, y), h=3.2)
        k = 1
        for gi, (d, pts) in enumerate(sorted(groups.items(), reverse=True)):
            letter = "ABCDEFGH"[gi]
            for j, (px, py) in enumerate(sorted(pts), 1):
                self.text(f"{letter}{j}   X {px:7.1f}   Y {py:7.1f}   ⌀{d:g}".replace(".", ","), (x, y - k * 4.6 * self.S), h=2.8)
                k += 1
        return y - k * 4.6 * self.S

    def save(self, name, pdf=None):
        path = os.path.join(OUT, name + ".dxf")
        self.doc.saveas(path)
        if pdf is not None:
            import matplotlib.pyplot as plt
            from ezdxf.addons.drawing import Frontend, RenderContext
            from ezdxf.addons.drawing.config import BackgroundPolicy, Configuration, LineweightPolicy
            from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
            fig = plt.figure(figsize=(297 / 25.4, 210 / 25.4))
            ax = fig.add_axes([0, 0, 1, 1])
            Frontend(RenderContext(self.doc), MatplotlibBackend(ax),
                     config=Configuration(background_policy=BackgroundPolicy.WHITE,
                                          lineweight_policy=LineweightPolicy.ABSOLUTE)).draw_layout(self.m)
            ax.set_xlim(0, self.W)
            ax.set_ylim(0, self.H)
            ax.set_aspect("equal")
            ax.axis("off")
            fig.set_size_inches(297 / 25.4, 210 / 25.4)
            pdf.savefig(fig, facecolor="white")
            if name in ("E7-T04_top_beam", "E7-P01_bearing_housing", "E7-B01_invar_rod"):
                fig.savefig(os.path.join(OUT, name + ".png"), dpi=150, facecolor="white")
            plt.close(fig)
        return path


def pick_scale(w, h, area=(255.0, 125.0)):
    for S in SCALES:
        if w / S <= area[0] and h / S <= area[1]:
            return S
    return SCALES[-1]


def scale_txt(S):
    return "1 : 1" if S == 1 else f"1 : {S:g}".replace(".", ",")


def centred(s):
    bb = s.val().BoundingBox() if hasattr(s, "val") else s.BoundingBox()
    return s.translate((-(bb.xmin + bb.xmax) / 2, -(bb.ymin + bb.ymax) / 2, -bb.zmin))


# ---------------------------------------------------------------------------------- part sheets
def sheet_plate(part, pdf):
    s = bp.laser_solid(part)
    rect = "rect" in part
    w = part["rect"][0] if rect else part["circle"]
    h = part["rect"][1] if rect else part["circle"]
    S = pick_scale(w + 60, h + part["t"] + 70)
    info = dict(no=part["name"][:6], name=part["name"][7:].replace("_", " ") + f", tl. {part['t']:g} mm",
                mat=part["mat"] + f", plech tl. {part['t']:g}", qty=part["qty"])
    D = Drawing(info, S)
    ox, oy = 25 * S, 70 * S
    btop, circ = D.view(s, "top", ox, oy + part["t"] + 25 * S, label="POHLED SHORA (řez laserem, DXF 1 : 1)")
    D.view(s, "front", ox, oy, label=None, hidden=False)
    D.dim_v(oy, oy + part["t"], ox + w, ox + w + 10 * S)
    if rect:
        ref = (btop[0], btop[1])
        D.text("◎", (ref[0] - 2 * S, ref[1] - 2 * S), h=4)
        r = part["rect"][2]
        D.notes([f"rohy R{r:g}", "drážky (šířka × délka): viz tabulka"], btop[0], btop[3] + 14 * S)
        y = D.hole_table(circ, ref, btop[2] + 14 * S, btop[3])
        if part["slots"]:
            D.text("DRÁŽKY (střed začátku → střed konce, šířka)", (btop[2] + 14 * S, y - 4 * S), h=3.2)
            for k, (x0, y0, x1, y1, ww) in enumerate(part["slots"], 1):
                cx0, cy0 = x0 + w / 2, y0 + h / 2
                cx1, cy1 = x1 + w / 2, y1 + h / 2
                D.text(f"S{k}   ({cx0:.1f}; {cy0:.1f}) → ({cx1:.1f}; {cy1:.1f})   š {ww:g}".replace(".", ","),
                       (btop[2] + 14 * S, y - (4 + 4.6 * k) * S), h=2.8)
            y -= (8 + 4.6 * len(part["slots"])) * S
        if part["engrave"]:
            D.text("gravírovat (nebo jen orýsovat): kružnice cely a 3× ⌀20 na r 35 – poloha cely a podložek G10",
                   (25 * S, 58 * S), h=2.8)
    else:
        cx, cy = (btop[0] + btop[2]) / 2, (btop[1] + btop[3]) / 2
        D.dim_d((cx, cy), w / 2, 40)
        for _, _, d in [c for c in circ if c[2] < w - 0.1][:1]:
            D.dim_d((cx, cy), d / 2, 220)
        extra = ""
        if part["mat"].startswith("steel"):
            extra = f"hmotnost {bp.disc_mass(part):.3f} kg – po výrobě převážit, doladit podložkami"
        D.notes([f"⌀{w:g}" + (f", otvor ⌀{part['holes'][0][2]:g} soustředně" if part["holes"] else ""), extra],
                btop[2] + 20 * S, btop[3])
    D.notes(["Výroba: laser / vodní paprsek podle DXF " + f"vyroba/laser/{part['name']}_{part['t']:g}mm.dxf",
             "Otvory řezat přímo (bez závitů), otřepy odstranit."], 25 * S, 50 * S)
    D.title_block(scale_txt(S))
    return D.save(part["name"], pdf)


def sheet_bar(no, name, mat, d, L, qty, notes, pdf, chamfer=0.5, profile=None):
    if profile:
        s = cq.Workplane("YZ").rect(*profile).extrude(L)
    else:
        s = cq.Workplane("YZ").circle(d / 2).extrude(L)
        if chamfer:
            s = s.faces("<X or >X").edges().chamfer(chamfer)
    S = pick_scale(L + 60, (profile[1] if profile else d) + 60)
    D = Drawing(dict(no=no, name=name, mat=mat, qty=qty), S)
    ox, oy = 25 * S, 95 * S
    b, _ = D.view(s, "front", ox, oy, label="POHLED ZE STRANY")
    vis, _, circ = project(s, "right")
    D.view(s, "right", b[2] + 25 * S, oy, label="ČELO", dims=False)
    if not profile:
        bx = b[2] + 25 * S
        D.dim_d((bx + d / 2, oy + d / 2), d / 2, 45, text=f"⌀{d:g}" + (" h9" if "h9" in notes[0] else ""))
    D.notes(notes, 25 * S, 60 * S)
    D.title_block(scale_txt(S))
    return D.save(no + "_" + name.split(",")[0].replace(" ", "_"), pdf)


def sheet_profile(prof, pdf):
    """T-slot profile slot 8: cut to length; the top beam T04 also gets the ⌀14 hole."""
    w, h = prof["section"]
    L = prof["L"]
    hole = prof["no"] == "E7-T04"
    s = bp.profile_solid((w, h), L, hole=hole)
    S = pick_scale(L + 80, w + h + 110)
    sec = f"{min(w, h):g}×{max(w, h):g}"
    D = Drawing(dict(no=prof["no"], name=prof["name"].split(" / ")[0] + f", profil {sec} drážka 8",
                     mat=f"Al profil {sec} drážka 8 (item / Bosch kompatibilní), elox", qty=prof["qty"]), S)
    ox, oy = 25 * S, 92 * S
    bf, _ = D.view(s, "front", ox, oy, label="ZEPŘEDU")
    bt, circ = D.view(s, "top", ox, bf[3] + 22 * S, label=None, hidden=False)
    D.text("SHORA" + (" (otvor ⌀14 skrz)" if hole else ""), (bt[0], bt[3] + (17 if hole else 4) * S), h=3.5)
    D.view(s, "right", bf[2] + 25 * S, oy, label="ŘEZ / ČELO", dims=False)
    D.dim_h(bf[2] + 25 * S, bf[2] + 25 * S + w, oy, oy - 8 * S)
    D.dim_v(oy, oy + h, bf[2] + 25 * S + w, bf[2] + 25 * S + w + 8 * S)
    notes = [f"řez na délku {L:g} ±0,2, řez kolmý ≤ 0,1; {prof['qty']} ks" + (" – všechny stejně" if prof["qty"] > 1 else ""),
             prof["note"], "bez dalšího obrábění; spoje úhelníky 40 drážka 8 + T-matice M8 (vkládací)"]
    if hole:
        cx, cy = (bt[0] + bt[2]) / 2, (bt[1] + bt[3]) / 2
        D.dim_h(bt[0], cx, bt[3], bt[3] + 10 * S, f"{L / 2:g}")
        D.dim_d((cx, cy), 7.0, 45, text="⌀14")
        notes += ["otvor ⌀14 svisle skrz celý profil (40 mm), uprostřed délky i šířky, stojanová vrtačka",
                  "spodní drážky: 4 T-matice M5 pro jádro oběhu P12 (rozteč 48 × 40, souměrně k otvoru) + 2 pro držák motoru P16 (x −68)",
                  "boční drážky: T-matice M5 – držák laseru P05 (+y), držák boxu RPi P18 (−y)"]
    D.notes(notes, 25 * S, oy - 20 * S)
    D.title_block(scale_txt(S))
    return D.save(prof["no"] + "_" + prof["name"].split(" / ")[-1].replace(" ", "_"), pdf)


PRINT_NOTES = {
    "E7-P01_bearing_housing": ["NEPOUŽÍVÁ SE od 18. 11. 2026 – pouzdro igus je v jádře oběhu P12","otvor ⌀21,2 hl. 32 pro igus RJ4JP-01-12 (lisovat rukou, svěrka M4)",
                               "spodem ⌀14 průchozí pro tyč; 4× ⌀5,5 (M5×45) se zahloubením ⌀10 × 5",
                               "rozteč 38 × 40 = T-matice M5 ve spodních drážkách příčníku T04, pouzdro visí pod ním"],
    "E7-P02_lvdt_arm": ["svěrka ⌀16,3 na Invarový sloupek, svěrka ⌀20,9 na LVDT DCTH (⌀20,6)",
                        "drážky 1,6 + šroub M3 (svěrky)", "výška ramene 12"],
    "E7-P03_target_arm": ["svěrka ⌀16,3 na sloupek; plocha 14 × 14 pro bílý terčík (samolepka)",
                          "rameno obchází celu zvenku (ohyb), terčík na straně kamery – v zorném poli kamery i laseru",
                          "fáze 1 (cela U): spodní plocha 3 mm nad čelem cely; fáze 2: horní plocha ve výšce límce"],
    "E7-P12_orbit_core": ["pevné jádro oběhu pod T04: 4× M5 do T-matic ve spodních drážkách (y ±20), otvor ⌀21,2 pod otvor ⌀14",
                          "do otvoru zalisovat igus RJ4JP-01-12 (vodicí tyč ⌀12 ve fázi 2); čep ⌀30 pro 2× 6806-2RS",
                          "3× ⌀2,5 dole pro M3 (svěrný kroužek P12c); kapsa + kanálek pro Hall A3144 ve spodní ploše desky",
                          "tisk deskou dolů, 100 % výplň čepu"],
    "E7-P12b_bearing_spacer": ["distanční kroužek mezi vnitřními kroužky ložisek 6806-2RS (⌀30,2 / ⌀34 × 6)"],
    "E7-P12c_clamp_ring": ["svěrný kroužek pod spodním vnitřním kroužkem, 3× M3 × 10 do jádra P12"],
    "E7-P13_orbit_hub": ["otočný náboj: 2 lůžka ⌀42 × 7 pro 6806-2RS (zalisovat), mezi nimi osazení ⌀38",
                         "nahoře věnec m1 z72 (šířka 6), dole příruba ⌀60 se 2× M3 pro patku ramene P14",
                         "kapsa ⌀6,2 × 2,2 pro magnet výchozí polohy; tisk 0,15 mm, 100 % výplň"],
    "E7-P14_camera_arm_head": ["patka ⌀60 / ⌀36 pod přírubou náboje (2× M3) – drží spodní ložisko",
                               "rameno vede pod motorem (z 271–279) do r 71, krátký sloupek k hlavě 34 × 34 × 24, okénko ⌀12, sklon 36,5°",
                               "4× M2 pro Camera Module 3; LED na hvězdě a 2 odpory 47 Ω přilepit; tisk s podpěrami"],
    "E7-P15_head_lid": ["víčko hlavy, výřez 17 × 3 pro plochý kabel kamery a vodiče LED / topení"],
    "E7-P16_motor_bracket": ["držák 28BYJ-48 pod T04 (strana −x): 2× M5 do spodních drážek, uši motoru M4 (rozteč 35) zespodu",
                             "osa pastorku 42 mm od osy vzorku (záběr m1 z12 / z72)"],
    "E7-P18_rpi_bracket": ["držák boxu P06 s RPi 5 na boční straně T04 (−y): 2× M5 do boční drážky, police nad dráhou hlavy"],
    "E7-P19_pinion_z12": ["pastorek m1 z12 na hřídel 28BYJ-48 (⌀5 s ploškami 3 mm), nalisovat; tisk 0,1 mm, 100 % výplň"],
    "E7-P10u_screed_5mm": ["fáze 1 (cela U): příčka leží na rovném čele cely, břit sahá 5 mm pod čelo (= povrch písku)",
                           "otáčet kolem osy, přebytek písku odebrat; břit tisknout naležato, 100 % výplň"],
    "E7-V03u_cell_bez_zatizeni": ["fáze 1: cela ⌀220 × 171 v jednom kuse, rovné čelo 5 mm nad pískem (bez límce)",
                                  "dutina ⌀100, dno pod pískem 26; port bodu M (TDR, vlákno, Pt100), NTC ⌀4 ve dně",
                                  "3 kapsy ⌀20,4 hl. 40 pro podložky G10; tisk dnem na podložku, bez podpěr v dutině",
                                  "stěna kolem dutiny 3 perimetry + 10–15 % gyroid (izolace); dutinu natřít epoxidem"],
    "E7-P04_post_foot": ["otvor ⌀16,3 se dnem 3 mm (přemostí drážku) – sloupek stojí na dně patky",
                         "2× ⌀5,5 (M5×20) do T-matic v horní drážce podélníku T02, zahloubení ⌀10 × 6; svěrka M3"],
    "E7-P05_laser_holder": [f"otvor ⌀10,2 pod úhlem {p.C_LASER_ANG:g}° pro laser ⌀10; červík M3",
                            "2× ⌀5,5 (M5×12) do T-matic v boční drážce příčníku T04 (+y)"],
    "E7-P06_camera_box": ["okénko ⌀34 + drážka 51 × 51 × 2,5 pro sklo 50 × 50 × 2",
                          "4× ⌀2,6 (M2,5) pro HQ kameru (30 × 30); vývodka PG7 ⌀12,4", "úchyt 2× ⌀4,4 (M4)"],
    "E7-P07_camera_box_lid": ["sloupky pro RPi 5 (58 × 49, M2,5)", "víko zapadá 4 mm do boxu"],
    "E7-P09_centering_cap": ["nasadit na límec plné cely (⌀106,6 × 6), tyč ⌀12 projde otvorem ⌀12,4 → cela souosá s vedením",
                             "podkova: po vystředění vysunout do strany; tisk 100 % výplň, rovinnost dosedací plochy"],
    "E7-P10_screed": ["příčka leží na límci, břit sahá přesně 34 mm pod jeho hranu (= povrch písku 100 mm)",
                      "otáčet kolem osy, přebytek písku odebrat; břit tisknout naležato, 100 % výplň"],
    "E7-P11_parking_fork": [f"postavit na horní plochu T04 kolem tyče pod stavěcí kroužek: tyč zvednutá o {bp.PARK_LIFT:g} mm",
                            "pak lze celu vyjmout (směr +y, rameno terčíku P03 natočit stranou)"],
    "E7-P08_camera_hanger": ["NEPOUŽÍVÁ SE od 18. 11. 2026 – kamera obíhá (P14), box RPi na držáku P18","2× ⌀5,5 (M5×12) do T-matic v boční drážce příčníku T04 (−y)", "box kamery přišroubovat 2× M4"],
}


def sheet_print(name, fn, qty, pdf, mat="PETG-CF, tisk 0,2 mm, 3 perimetry, 40 % gyroid"):
    s = centred(fn())
    bb = s.val().BoundingBox()
    w, d, h = bb.xlen, bb.ylen, bb.zlen
    S = pick_scale(w + d + 90, d + h + 70)
    no, nm = name.split("_", 1)
    D = Drawing(dict(no=no, name=nm.replace("_", " "), mat=mat, qty=qty), S)
    ox, oy = 25 * S, 62 * S
    bf, _ = D.view(s, "front", ox, oy, label="ZEPŘEDU")
    bt, circ = D.view(s, "top", ox, bf[3] + 22 * S, label="SHORA")
    D.view(s, "right", bf[2] + 25 * S, oy, label="ZPRAVA")
    ds = sorted({c[2] for c in circ}, reverse=True)
    D.notes(PRINT_NOTES.get(name, []) + ["průměry otvorů v pohledu shora: " + ", ".join(f"⌀{x:g}" for x in ds[:6]),
                                         "přesná geometrie: vyroba/tisk/" + name + ".step / .stl"],
            bf[2] + 25 * S, bt[3])
    D.title_block(scale_txt(S))
    return D.save(name, pdf)


def main():
    from matplotlib.backends.backend_pdf import PdfPages
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith((".dxf", ".pdf", ".png")):
            os.remove(os.path.join(OUT, f))
    made = []
    with PdfPages(os.path.join(OUT, "E7_vyrobni_vykresy.pdf")) as pdf:
        for part in bp.LASER:
            made.append(sheet_plate(part, pdf))
        made.append(sheet_bar("E7-B01", "invar rod, vodicí tyč ⌀12", "Invar 36 (1.3912), tyč ⌀12 h9", 12, bp.ROD_L, 1,
                              ["⌀12 h9 (−0,043) – kluzné pouzdro igus; Ra ≤ 0,8 na celé délce",
                               "čela kolmá k ose, sražení 0,5 × 45° oba konce",
                               "spodní čelo dosedá na kuličku 5/16\"; nahoře stavěcí kroužek DIN 705-A 12"], pdf))
        made.append(sheet_bar("E7-B02", "invar post, sloupek ⌀16", "Invar 36 (1.3912), tyč ⌀16", 16, round(bp.POST_L), 1,
                              ["čela kolmá k ose (sloupek stojí ve dně patky P04 na podélníku), sražení 0,5 × 45°",
                               "svěrky P02 a P03 se nasunou shora, P04 drží patu"], pdf))
        made.append(sheet_bar("E7-B03", "G10 pad, podložka ⌀20", "sklotextit G10 / FR4, tyč ⌀20", 20, p.C_INS_T, 3,
                              ["3 kusy, délka 40 ±0,05, čela rovnoběžná ≤ 0,05 (všechny 3 stejně)",
                               "v kapsách ⌀20,4 ve dně cely, vyčnívají 0,5 mm"], pdf, chamfer=0.3))
        for prof in bp.PROFILES:
            made.append(sheet_profile(prof, pdf))
        for name, fn, q in bp.PRINT:
            made.append(sheet_print(name, fn, q, pdf))
        # phase 1 – variant U (appended, page order of the sheets above stays the same)
        for name, fn, q in bp.PRINT_U_EXTRA:
            made.append(sheet_print(name, fn, q, pdf))
        import orbit
        for name, fn, q in orbit.PRINT_ORBIT:
            made.append(sheet_print(name, fn, q, pdf))
        cu = [f for f in os.listdir(os.path.join(HERE, "..", "vyroba", "tisk")) if f.startswith("E7-V03u") and f.endswith(".step")][0]
        made.append(sheet_print("E7-V03u_cell_bez_zatizeni",
                                lambda: cq.importers.importStep(os.path.join(HERE, "..", "vyroba", "tisk", cu)), 1, pdf,
                                mat="PETG-CF, 0,2 mm, 3 perimetry, gyroid 10–15 %"))
    print(len(made), "sheets →", OUT)


if __name__ == "__main__":
    main()
