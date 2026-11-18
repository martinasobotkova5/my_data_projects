"""E7 – nářezové výkresy (cutting plans) for the parts that are bought cut to size.

Sheets (A4 landscape):
  N00  přehled nářezů podle dodavatele (fáze 1 / fáze 2)
  N01  T-profily 40×80 a 40×40 – nářezový plán (ENPRAG)
  N02  tyče Invar ⌀12 / ⌀16 a G10 ⌀20 – nářezový plán (Kovohutě Rokycany, Elektroizolanty Praha)
  N03  laserové řezání – rozložení kotoučů na plechu (grupol.cz)
Then the existing production drawings of the same parts (L03–L07, B01–B03, T01–T04) are appended, and one PDF
per supplier is written, so each firm gets only its own pages.

Output: vyroba/narezy/E7_narezove_vykresy.pdf + E7_narezy_<firma>.pdf
"""
import os
import sys
import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.backends.backend_pdf import PdfPages
from pypdf import PdfReader, PdfWriter

sys.path.insert(0, os.path.dirname(__file__))
import params as p          # noqa: E402
import buildparts as bp     # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "vyroba", "narezy")
PROD = os.path.join(ROOT, "vyroba", "vykresy", "E7_vyrobni_vykresy.pdf")
TODAY = datetime.date.today().isoformat()
KERF = 3.0           # saw kerf, mm
GAP = 6.0            # laser: gap between parts / to plate edge
INK, MUTE, CUT, OFF = "#111111", "#666666", "#1f6f99", "#d9d9d9"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.5})

PROF = {d["no"]: d for d in bp.PROFILES}
LAS = {d["name"]: d for d in bp.LASER}


def sheet(no, title, firm):
    fig = plt.figure(figsize=(297 / 25.4, 210 / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 297); ax.set_ylim(0, 210); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((8, 8), 281, 194, fill=False, lw=0.8, ec=INK))
    # title block (bottom right) – same rows as the production drawings
    x0, y0, w, h = 289 - 150, 8, 150, 26
    ax.add_patch(Rectangle((x0, y0), w, h, fill=False, lw=0.6, ec=INK))
    rows = [(f"{no}  {title}", "A4"), (f"pro: {firm}", "rozměry v mm"),
            ("E7 – mrznutí a tání / sublimace, varianta C rev. B3", f"{TODAY}  nářezový výkres")]
    for k, (a, b) in enumerate(rows):
        yy = y0 + h - (k + 1) * h / 3
        if k:
            ax.plot([x0, x0 + w], [yy + h / 3, yy + h / 3], lw=0.4, c=INK)
        ax.text(x0 + 2, yy + 3, a, fontsize=8.5 if k == 0 else 7, weight="bold" if k == 0 else None, va="bottom")
        ax.text(x0 + w - 2, yy + 3, b, fontsize=7, ha="right", va="bottom")
    return fig, ax


def dim(ax, x0, x1, y, txt, above=True):
    ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", lw=0.5, color=INK, shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, y + (1.0 if above else -1.0), txt, ha="center", va="bottom" if above else "top", fontsize=6.5)


def bar(ax, x, y, cuts, scale, hgt, label, stock_note, holes=()):
    """cuts: list of (tag, length). Draws pieces with kerf gaps; returns total used length (incl. kerf)."""
    ax.text(x, y + hgt + 9, label, fontsize=8.5, weight="bold")
    ax.text(x, y + hgt + 4.5, stock_note, fontsize=7, color=MUTE)
    pos = 0.0
    for k, (tag, L) in enumerate(cuts):
        ax.add_patch(Rectangle((x + pos * scale, y), L * scale, hgt, fc="#eaf3f8", ec=CUT, lw=0.8))
        tx = pos + (L / 4 if any(h[0] == tag for h in holes) else L / 2)
        ax.text(x + tx * scale, y + hgt / 2, tag, ha="center", va="center", fontsize=7.5, weight="bold", color=CUT)
        dim(ax, x + pos * scale, x + (pos + L) * scale, y - 4, f"{L:g}", above=False)
        for (htag, hx, hd) in holes:
            if htag == tag:
                cx = x + (pos + hx) * scale
                ax.add_patch(Circle((cx, y + hgt / 2), hd / 2 * scale * 1.0 + 0.6, fill=False, ec=INK, lw=0.6))
                ax.text(cx, y + hgt + 1, f"⌀{hd:g} skrz, {hx:g} od čela", ha="center", va="bottom", fontsize=6)
        pos += L
        ax.add_patch(Rectangle((x + pos * scale, y), KERF * scale, hgt, fc=INK, ec=INK, lw=0.2))
        pos += KERF
    ax.text(x + pos * scale + 2, y + hgt / 2, f"celkem {pos:g} mm\n(vč. prořezů {KERF:g} mm)", va="center", fontsize=6.5,
            color=MUTE)
    return pos


def table(ax, x, y, cols, widths, rows, fs=6.6, rh=5.2, head_fill="#e3eef5"):
    xs = [x]
    for wd in widths:
        xs.append(xs[-1] + wd)
    ax.add_patch(Rectangle((x, y - rh), sum(widths), rh, fc=head_fill, ec=INK, lw=0.4))
    for c, cx in zip(cols, xs):
        ax.text(cx + 1.2, y - rh / 2, c, va="center", fontsize=fs, weight="bold")
    yy = y - rh
    for r in rows:
        bold = r[0].startswith("§")
        n = max(len(str(v).split("\n")) for v in r)
        hh = rh * (0.75 * n + 0.25) if n > 1 else rh
        if not bold:
            for cx in xs[1:-1]:
                ax.plot([cx, cx], [yy, yy - hh], lw=0.3, c=INK)
        if bold:
            ax.add_patch(Rectangle((x, yy - hh), sum(widths), hh, fc="#f4f4f4", ec=INK, lw=0.3))
            ax.text(x + 1.2, yy - hh / 2, r[0][1:], va="center", fontsize=fs, weight="bold")
        else:
            ax.add_patch(Rectangle((x, yy - hh), sum(widths), hh, fill=False, ec=INK, lw=0.3))
            for v, cx in zip(r, xs):
                ax.text(cx + 1.2, yy - hh / 2, str(v), va="center", fontsize=fs, linespacing=1.15)
        yy -= hh
    for cx in xs[1:-1]:
        ax.plot([cx, cx], [y, y - rh], lw=0.3, c=INK)
    return yy


# ----------------------------------------------------------------------------------------------------------------
def n00(pdf):
    fig, ax = sheet("E7-N00", "přehled nářezů a dodavatelů", "všechny firmy (fáze 1 a 2)")
    ax.text(14, 194, "Nářezové výkresy – přehled", fontsize=13, weight="bold")
    ax.text(14, 188, "Fáze 1 = mrznutí–tání BEZ ZATÍŽENÍ (varianta U): rám T01–T04, podložky G10 a invarový sloupek B02. "
                     "Fáze 2 = sublimace se zátěží (varianta C): navíc vodicí tyč B01 a laserem řezané díly L03–L07.",
            fontsize=7.5, color=MUTE)
    t1 = PROF["E7-T01"]; t2 = PROF["E7-T02"]; t3 = PROF["E7-T03"]; t4 = PROF["E7-T04"]
    L80 = 2 * t1["L"] + t3["L"] + t4["L"] + 4 * KERF
    L40 = 2 * t2["L"] + 2 * KERF
    rows = [
        ("§ENPRAG, s.r.o., Praha 5 – T-profily drážka 8 (výkres N01 + T01–T04)",) + ("",) * 6,
        ("T01", "sloup", "profil 40×80 drážka 8", f"{t1['L']:g} ±0,2", "2", "řez kolmý ≤ 0,1", "N01, T01"),
        ("T03", "příčka základny", "profil 40×80 drážka 8", f"{t3['L']:g} ±0,2", "1", "řez kolmý ≤ 0,1", "N01, T03"),
        ("T04", "horní příčník", "profil 40×80 drážka 8", f"{t4['L']:g} ±0,2", "1", f"otvor ⌀14 skrz v {t4['L']/2:g}", "N01, T04"),
        ("T02", "podélník základny", "profil 40×40 drážka 8", f"{t2['L']:g} ±0,2", "2", "řez kolmý ≤ 0,1", "N01, T02"),
        ("", "", f"celkem 40×80: {L80:g} mm, 40×40: {L40:g} mm", "", "", "+ úhelníky, T-matice, nohy", ""),
        ("§Kovohutě Rokycany (sales@koro.cz) – Invar 36, 1.3912 (výkres N02 + B01, B02)",) + ("",) * 6,
        ("B01", "vodicí tyč", "Invar 36 ⌀12 h9", f"{bp.ROD_L:g} ±0,5", "1", "čela kolmá, sražení 0,5", "N02, B01"),
        ("B02", "sloupek (terčík, LVDT)", "Invar 36 ⌀16", f"{round(bp.POST_L):g} ±0,5", "1", "čela kolmá, sražení 0,5", "N02, B02"),
        ("§Elektroizolanty Praha – sklotextit G10 (výkres N02 + B03)",) + ("",) * 6,
        ("B03", "podložka pod celu", "G10 tyč ⌀20 × 1000", f"{p.C_INS_T:g} ±0,05", "3", "čela rovnoběžná ≤ 0,05", "N02, B03"),
        ("§grupol.cz (laser, nahrát DXF) – plechy (výkres N03 + L03–L07)",) + ("",) * 6,
        ("L03", "nosná deska závaží", "Al EN AW-5754, tl. 10", "⌀140, otvor ⌀12,3", "1", "E7-L03_carrier_10mm.dxf", "N03, L03"),
        ("L04", "píst horní", "Al EN AW-5754, tl. 10", "⌀50, otvor ⌀6", "1", "E7-L04_piston_top_10mm.dxf", "N03, L04"),
        ("L05", "píst spodní", "Al EN AW-5754, tl. 10", "⌀50", "1", "E7-L05_piston_bottom_10mm.dxf", "N03, L05"),
        ("L06", "závaží 1 kg", "ocel S235JR, tl. 12", "⌀117,5, otvor ⌀17", "4", "E7-L06_disc_1kg_12mm.dxf", "N03, L06"),
        ("L07", "závaží 0,5 kg", "ocel S235JR, tl. 6", "⌀117,5, otvor ⌀17", "1", "E7-L07_disc_0.5kg_6mm.dxf", "N03, L07"),
    ]
    PH = {"T": "1", "B02": "1", "B03": "1", "B01": "2 *", "L": "2"}
    rows = [r + ("",) if r[0].startswith("§") or not r[0] else r + (PH.get(r[0], PH.get(r[0][:1], "")),) for r in rows]
    yy = table(ax, 14, 182, ["poz.", "díl", "materiál / polotovar", "rozměr", "ks", "pozn.", "výkres", "fáze"],
               [12, 30, 62, 34, 9, 52, 22, 12], rows)
    notes = ["Prořez pily počítán 3 mm. Nekótované tolerance ISO 2768-mK, hrany odjehlit.",
             "Hliník 10 mm: ověřit u grupol.cz, že ho laser řeže; jinak stejné DXF na vodní paprsek (Zamet, Light Cut).",
             "Kotouče L06/L07 po výrobě zvážit, rozdíl hmotnosti doladit podložkami (±0,5 mm tloušťky ≈ ±4 %).",
             "Invar: pokud Rokycany čela nezarovnají, objednat B01 270 mm a B02 335 mm a čela srovnat v dílně.",
             "* B01 patří do fáze 2, ale objednat ji spolu s B02 (jedna poptávka, malé množství).",
             "Díly L03–L07 (grupol.cz) stačí objednat až před fází 2. Otvor ⌀14 v T04 vyvrtat hned (rám je společný).",
             "Tištěné díly (cela E7-V03u, P03–P07, P10u, oběh P12–P16, P18, P19) se neřežou – STL/STEP ve vyroba/tisk."]
    for k, s in enumerate(notes):
        ax.text(14, yy - 7 - k * 4.6, "• " + s, fontsize=7)
    pdf.savefig(fig); plt.close(fig)


def n01(pdf):
    fig, ax = sheet("E7-N01", "T-profily – nářezový plán", "ENPRAG, s.r.o.")
    ax.text(14, 194, "T-profily drážka 8 (item / Bosch kompatibilní) – nářezový plán", fontsize=12, weight="bold")
    ax.text(14, 188.5, "Řezy kolmé k ose ≤ 0,1 mm, délky ±0,2 mm, otřepy odstranit. Profily stejné značky jako "
                       "úhelníky a T-matice.", fontsize=7.5, color=MUTE)
    S = 0.19
    t1, t2, t3, t4 = (PROF[k] for k in ("E7-T01", "E7-T02", "E7-T03", "E7-T04"))
    bar(ax, 14, 150, [("T01", t1["L"]), ("T01", t1["L"]), ("T03", t3["L"]), ("T04", t4["L"])], S, 15,
        "Profil 40×80 drážka 8 – 4 kusy z jedné tyče", "přířez z tyče 6 m (účtuje se odebraná délka + řezy)",
        holes=[("T04", t4["L"] / 2, 14)])
    bar(ax, 14, 108, [("T02", t2["L"]), ("T02", t2["L"])], S, 8,
        "Profil 40×40 drážka 8 – 2 kusy", "přířez z tyče 6 m")
    # T04 detail: hole position
    x, y, s2 = 14, 52, 0.42
    L = t4["L"]
    ax.text(x, y + 38, "Detail T04 – horní příčník, otvor ⌀14 (pohled shora, profil leží naplocho)", fontsize=8.5,
            weight="bold")
    ax.add_patch(Rectangle((x, y), L * s2, 80 * s2, fc="#eaf3f8", ec=CUT, lw=0.8))
    for k in (20, 60):
        ax.plot([x, x + L * s2], [y + k * s2, y + k * s2], lw=0.4, ls="--", c=MUTE)
    ax.add_patch(Circle((x + L / 2 * s2, y + 40 * s2), 7 * s2, fill=False, ec=INK, lw=0.8))
    ax.plot([x + L / 2 * s2] * 2, [y - 3, y + 80 * s2 + 3], lw=0.3, c=INK, ls="-.")
    dim(ax, x, x + L / 2 * s2, y - 6, f"{L/2:g}", above=False)
    dim(ax, x, x + L * s2, y - 13, f"{L:g}", above=False)
    ax.text(x + L * s2 + 4, y + 26, "⌀14 svisle skrz celou výšku profilu (40 mm),\nuprostřed délky i šířky "
                                   "(mezi drážkami)\nstojanová vrtačka, kolmost ≤ 0,2 / 40", fontsize=7)
    ax.text(x + L * s2 + 4, y + 8, "spodní drážky: T-matice M5 – jádro oběhu P12 (4×),\ndržák motoru P16 (2×); boční drážky: držák\n"
                                  "laseru P05 (+y), držák boxu RPi P18 (−y)", fontsize=7, color=MUTE)
    # kit to order with the profiles
    rows = [("úhelník 40×40 drážka 8 + krytka", "12"), ("T-matice M8 vkládací", "32"), ("T-matice M5 vkládací", "12"),
            ("šroub ISO 4762 M8×16 + podložka", "24"), ("stavitelná noha M8, talíř ⌀30–40", "4"),
            ("krytka čela 40×80 / 40×40", "6")]
    table(ax, 196, 134, ["spojovací materiál k profilům (ENPRAG)", "ks"], [72, 14], rows)
    pdf.savefig(fig); plt.close(fig)


def n02(pdf):
    fig, ax = sheet("E7-N02", "tyče Invar a G10 – nářezový plán", "Kovohutě Rokycany · Elektroizolanty Praha")
    ax.text(14, 194, "Tyče – nářezový plán", fontsize=12, weight="bold")
    S = 0.36
    ax.text(14, 186, "Kovohutě Rokycany – Invar 36 (FeNi36, 1.3912)", fontsize=9.5, weight="bold", color=CUT)
    bar(ax, 14, 160, [("B01", bp.ROD_L)], S, 6, f"B01 vodicí tyč ⌀12 h9 – 1 ks × {bp.ROD_L:g} mm",
        "h9 (−0,043), Ra ≤ 0,8 – jezdí v kluzném pouzdře igus; čela kolmá, sražení 0,5 × 45°")
    bar(ax, 14, 128, [("B02", round(bp.POST_L))], S, 8, f"B02 sloupek LVDT ⌀16 – 1 ks × {round(bp.POST_L):g} mm",
        "čela kolmá, sražení 0,5 × 45°")
    ax.text(14, 112, "Pokud nedodají řez s kolmými čely: objednat 270 mm a 335 mm, čela zarovnat v dílně.",
            fontsize=7, color=MUTE)
    ax.text(14, 98, "Elektroizolanty Praha – sklotextit G10, tyč ⌀20 × 1000 mm", fontsize=9.5, weight="bold", color=CUT)
    S2 = 0.22
    used = bar(ax, 14, 74, [("B03", p.C_INS_T)] * 3, S2 * 1.6, 8, "B03 podložky ⌀20 × 40 – 3 ks z jedné tyče",
               "délka 40 ±0,05, čela rovnoběžná ≤ 0,05 – všechny tři stejné (cela na nich stojí)")
    ax.text(14, 58, f"Zbytek tyče ≈ {1000 - used:g} mm (rezerva). Pokud firma neřeže na přesnou délku: nařezat "
                    "s přídavkem 1 mm a čela srovnat\nbroušením na rovné desce (smirkový papír), všechny tři najednou "
                    "v přípravku.", fontsize=7, color=MUTE)
    pdf.savefig(fig); plt.close(fig)


def n03(pdf):
    fig, ax = sheet("E7-N03", "laserové řezání – rozložení na plechu (fáze 2)", "grupol.cz (alt. Zamet, Light Cut)")
    ax.text(14, 194, "Laserové řezání – rozložení dílů na plechu (orientační; firma si díly rozloží sama)",
            fontsize=12, weight="bold")
    ax.text(14, 188.5, f"Mezera mezi díly a k okraji {GAP:g} mm. Do e-shopu nahrát DXF z vyroba/laser – "
                       "1 soubor = 1 díl, v souboru je počet kusů v názvu výkresu.", fontsize=7.5, color=MUTE)
    s = 0.33

    def plate(x, y, title, parts, W, H):
        ax.text(x, y + H * s + 5, title, fontsize=8.5, weight="bold")
        ax.add_patch(Rectangle((x, y), W * s, H * s, fc="#f2f2f2", ec=INK, lw=0.6))
        for (tag, cx, cy, d, hole) in parts:
            ax.add_patch(Circle((x + cx * s, y + cy * s), d / 2 * s, fc="#eaf3f8", ec=CUT, lw=0.9))
            if hole:
                ax.add_patch(Circle((x + cx * s, y + cy * s), hole / 2 * s, fc="white", ec=CUT, lw=0.6))
            ax.text(x + cx * s, y + cy * s - (hole / 2 * s + 3 if hole else 0), tag, ha="center", va="center",
                    fontsize=6.5, weight="bold", color=CUT)
        dim(ax, x, x + W * s, y - 4, f"{W:g}", above=False)
        ax.annotate("", (x - 3, y), (x - 3, y + H * s), arrowprops=dict(arrowstyle="<->", lw=0.5, shrinkA=0, shrinkB=0))
        ax.text(x - 4, y + H * s / 2, f"{H:g}", rotation=90, ha="right", va="center", fontsize=6.5)

    D3, D4, D6 = p.C_CARRIER_D, p.C_PISTON_D, LAS["E7-L06_disc_1kg"]["circle"]
    hd = LAS["E7-L06_disc_1kg"]["holes"][0][2]
    W1 = GAP + D3 + GAP + D4 + GAP; H1 = GAP + D3 + GAP
    plate(20, 112, "Al EN AW-5754, tl. 10 mm: L03 + L04 + L05", [
        ("L03", GAP + D3 / 2, GAP + D3 / 2, D3, p.C_ROD_D + 0.3),
        ("L04", 2 * GAP + D3 + D4 / 2, H1 - GAP - D4 / 2, D4, 6.0),
        ("L05", 2 * GAP + D3 + D4 / 2, GAP + D4 / 2, D4, 0)], W1, H1)
    W2 = GAP + 2 * D6 + 2 * GAP
    plate(122, 86, "ocel S235JR, tl. 12 mm: 4× L06 (1 kg)", [
        ("L06", GAP + D6 / 2, GAP + D6 / 2, D6, hd), ("L06", 2 * GAP + 1.5 * D6, GAP + D6 / 2, D6, hd),
        ("L06", GAP + D6 / 2, 2 * GAP + 1.5 * D6, D6, hd), ("L06", 2 * GAP + 1.5 * D6, 2 * GAP + 1.5 * D6, D6, hd)],
        W2, W2)
    W3 = GAP + D6 + GAP
    plate(20, 44, "ocel S235JR, tl. 6 mm: 1× L07 (0,5 kg)", [("L07", W3 / 2, W3 / 2, D6, hd)], W3, W3)
    ax.text(222, 168, "Po výrobě:\n• kotouče zvážit (cíl 1,000 kg / 0,500 kg),\n  doladit podložkami\n"
                     "• otřepy odstranit, hrany sražení 0,3\n• písty L04 + L05 slepit epoxidem\n  (otvor ⌀6 v L04 nahoru)",
            fontsize=7, va="top")
    pdf.savefig(fig); plt.close(fig)


# production-drawing pages per supplier (order in E7_vyrobni_vykresy.pdf: L03–L07, B01–B03, T01–T04, P01–P11)
PAGES = {"laser_grupol": [0, 1, 2, 3, 4], "invar_Rokycany": [5, 6], "G10_Elektroizolanty": [7],
         "profily_ENPRAG": [8, 9, 10, 11]}
COVER = {"laser_grupol": [0, 3], "invar_Rokycany": [0, 2], "G10_Elektroizolanty": [0, 2], "profily_ENPRAG": [0, 1]}  # N00..N03


def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(OUT, "_narezy.pdf")
    with PdfPages(tmp) as pdf:
        n00(pdf); n01(pdf); n02(pdf); n03(pdf)
    cov, prod = PdfReader(tmp), PdfReader(PROD)
    w = PdfWriter()
    for pg in cov.pages:
        w.add_page(pg)
    for i in range(12):
        w.add_page(prod.pages[i])
    full = os.path.join(OUT, "E7_narezove_vykresy.pdf")
    with open(full, "wb") as f:
        w.write(f)
    for firm, idx in PAGES.items():
        w = PdfWriter()
        for c in COVER[firm]:
            w.add_page(cov.pages[c])
        for i in idx:
            w.add_page(prod.pages[i])
        with open(os.path.join(OUT, f"E7_narezy_{firm}.pdf"), "wb") as f:
            w.write(f)
    os.remove(tmp)
    print("→", full, len(cov.pages) + 12, "pages; + per supplier:", ", ".join(PAGES))


if __name__ == "__main__":
    main()
