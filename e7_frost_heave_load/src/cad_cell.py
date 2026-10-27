"""CAD drawing (DXF, all dimensions) of the printed cell rev. B: printed in ONE piece ⌀240 × 200 –
core = Column_one_body_version_1 (M. Vrána) + 40 mm low-infill wall and 40 mm base with 3 pockets for G10 pads.

Run: python cad_cell.py → ../cad/E7_V04_cell.dxf + E7_V04_cell.pdf (preview).
Model space in mm 1 : 1; the A3 frame and texts are drawn for printing at 1 : 1.5.
Dimensions are real DXF DIMENSION entities (editable in AutoCAD / LibreCAD / Onshape import).
"""
import math
import os

import ezdxf
from ezdxf.enums import TextEntityAlignment

import params as p

OUT = os.path.join(os.path.dirname(__file__), "..", "cad")
S = 1.5                      # print scale 1 : 1.5 on A3
TH = 5.0 * S                 # headings 5 mm on paper
TS = 3.0 * S                 # small text 3 mm on paper

O = p.C_INS_T                                       # printed base under the core
RK = p.BODY_D / 2                                   # core jacket (internal, no edge in the print)
RB, RC, RI, W = RK + p.C_SLEEVE_T, p.COLLAR_OD / 2, p.CAV_D / 2, p.CUP_WALL_IN
H, HC, TB, ZS = p.BODY_H + O, p.COLLAR_TOP + O, p.BODY_BOTTOM + O, p.SAND_TOP + O
PZ0, PZ1 = p.PORT_Z0 + O, p.PORT_Z1 + O
T = p.TDR_CS645
Z_MID = (PZ0 + PZ1) / 2
RODS = [Z_MID + T["pitch"], Z_MID, Z_MID - T["pitch"]]


def setup():
    doc = ezdxf.new("R2010", setup=True, units=4)          # units = mm
    for name, color, lt, lw in (("OUTLINE", 7, "CONTINUOUS", 50), ("HIDDEN", 8, "DASHED", 25),
                                ("CENTER", 8, "CENTER", 18), ("HATCH", 8, "CONTINUOUS", 13),
                                ("DIM", 7, "CONTINUOUS", 25), ("TEXT", 7, "CONTINUOUS", 25),
                                ("SENSOR", 3, "CONTINUOUS", 25), ("SAND", 2, "DASHED", 25),
                                ("FRAME", 7, "CONTINUOUS", 50)):
        layer = doc.layers.add(name, color=color, linetype=lt)
        layer.dxf.lineweight = lw
        if name in ("OUTLINE", "DIM", "TEXT", "FRAME"):
            layer.rgb = (0, 0, 0)                           # true black (prints black on any background)
    ds = doc.dimstyles.new("E7")
    ds.dxf.dimtxt = 3.5 * S                                 # 3.5 mm on paper (ISO 129 for A3)
    ds.dxf.dimasz = 3.0 * S
    ds.dxf.dimexe = 2.0 * S
    ds.dxf.dimexo = 1.0 * S
    ds.dxf.dimgap = 1.0 * S
    ds.dxf.dimdec = 1
    ds.dxf.dimdsep = ord(",")                               # decimal comma (CZ)
    ds.dxf.dimzin = 8                                       # drop trailing zeros
    ds.dxf.dimtad = 1
    ds.dxf.dimtih = 0
    ds.dxf.dimtoh = 0
    ds.dxf.dimclrd = 256                                    # colours ByLayer → DIM layer = black
    ds.dxf.dimclre = 256
    ds.dxf.dimclrt = 256
    ds.dxf.dimlwd = 25
    ds.dxf.dimlwe = 25
    ds.dxf.dimtxsty = "OpenSans"
    doc.header["$LTSCALE"] = 1.5
    return doc


class Sheet:
    def __init__(self, doc):
        self.msp = doc.modelspace()

    def line(self, a, b, layer="OUTLINE"):
        self.msp.add_line(a, b, dxfattribs={"layer": layer})

    def poly(self, pts, layer="OUTLINE", close=True):
        self.msp.add_lwpolyline(pts, close=close, dxfattribs={"layer": layer})

    def rect(self, x0, y0, x1, y1, layer="OUTLINE"):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], layer)

    def circle(self, c, r, layer="OUTLINE"):
        self.msp.add_circle(c, r, dxfattribs={"layer": layer})

    def text(self, s, at, h=TS, layer="TEXT", align=TextEntityAlignment.LEFT, rot=0):
        t = self.msp.add_text(s, height=h, rotation=rot, dxfattribs={"layer": layer, "style": "OpenSans"})
        t.set_placement(at, align=align)

    def hatch(self, pts, scale=3.0):
        h = self.msp.add_hatch(color=8, dxfattribs={"layer": "HATCH"})
        h.set_pattern_fill("ANSI31", scale=scale)
        h.paths.add_polyline_path(pts, is_closed=True)

    def dim_h(self, x0, x1, y, ybase, text="<>"):
        self.msp.add_linear_dim(base=(x0, ybase), p1=(x0, y), p2=(x1, y), angle=0, dimstyle="E7", text=text,
                                dxfattribs={"layer": "DIM"}).render()

    def dim_v(self, y0, y1, x, xbase, text="<>"):
        self.msp.add_linear_dim(base=(xbase, y0), p1=(x, y0), p2=(x, y1), angle=90, dimstyle="E7", text=text,
                                dxfattribs={"layer": "DIM"}).render()

    def dim_d(self, c, r, ang, text="<>"):
        self.msp.add_diameter_dim(center=c, radius=r, angle=ang, dimstyle="E7", text=text,
                                  dxfattribs={"layer": "DIM"}).render()

    def dim_r(self, c, r, ang, text="<>"):
        self.msp.add_radius_dim(center=c, radius=r, angle=ang, dimstyle="E7", text=text,
                                dxfattribs={"layer": "DIM"}).render()

    def leader(self, pts, s):
        self.msp.add_lwpolyline(pts, dxfattribs={"layer": "DIM"})
        self.text(s, (pts[-1][0] + 1.5, pts[-1][1] - TS / 2), layer="TEXT")


def section(sh, ox, oy):
    """SECTION A–A along the TDR axis (port on the left). z = 0 at the underside."""
    P = lambda x, z: (ox + x, oy + z)
    f = RI + 0.0
    r = p.CAV_FILLET
    # outer contour (body + collar)
    sh.poly([P(-RB, 0), P(RB, 0), P(RB, H), P(RC, H), P(RC, HC), P(RI, HC), P(RI, TB + r)], close=False)
    sh.msp.add_arc(P(RI - r, TB + r), r, 270, 360, dxfattribs={"layer": "OUTLINE"})
    sh.line(P(RI - r, TB), P(-RI + r, TB))
    sh.msp.add_arc(P(-RI + r, TB + r), r, 180, 270, dxfattribs={"layer": "OUTLINE"})
    sh.poly([P(-RI, TB + r), P(-RI, PZ0)], close=False)
    sh.poly([P(-RI, PZ1), P(-RI, HC), P(-RC, HC), P(-RC, H), P(-RB, H), P(-RB, PZ1)], close=False)
    sh.line(P(-RB, PZ0), P(-RB, 0))
    # port (left), through the jacket up to the 3 mm inner wall
    sh.poly([P(-RB, PZ0), P(-RI - W, PZ0), P(-RI - W, PZ1), P(-RB, PZ1)], close=False)
    sh.line(P(-RI - W, PZ0), P(-RI, PZ0))
    sh.line(P(-RI - W, PZ1), P(-RI, PZ1))
    # inner wall lines (3 mm wall inside the 10 % jacket)
    for s_ in (-1, 1):
        sh.line(P(s_ * (RI + W), TB), P(s_ * (RI + W), H), "HIDDEN")
    sh.line(P(-RB, TB), P(RB, TB), "HIDDEN")
    # rod holes ⌀3.5 and fibre hole ⌀1.5 in the inner wall
    for z in RODS:
        sh.rect(-RI - W + ox, z - 1.75 + oy, -RI + ox, z + 1.75 + oy)
    zf = RODS[0] + 2.0
    # hatch: right wall + bottom + left wall parts (section)
    sh.hatch([P(RI, TB + r), P(RI, HC), P(RC, HC), P(RC, H), P(RB, H), P(RB, 0), P(-RB, 0), P(-RB, PZ0),
              P(-RI - W, PZ0), P(-RI - W, PZ0), P(-RI, PZ0), P(-RI, TB + r), P(-RI + r, TB),
              P(RI - r, TB)])
    sh.hatch([P(-RB, PZ1), P(-RI - W, PZ1), P(-RI, PZ1), P(-RI, HC), P(-RC, HC), P(-RC, H),
              P(-RB, H)])
    # rev. B: pocket for the G10 pad at 90° (in the section plane, right), core boundary (internal)
    pr = (p.C_PAD_D + 0.4) / 2
    sh.rect(ox + p.C_PAD_R - pr, oy, ox + p.C_PAD_R + pr, oy + O)
    sh.rect(ox + p.C_PAD_R - p.C_PAD_D / 2, oy - 0.5, ox + p.C_PAD_R + p.C_PAD_D / 2, oy + O, "SENSOR")
    for s_ in (-1, 1):
        sh.line(P(s_ * RK, O), P(s_ * RK, H), "HIDDEN")
    sh.line(P(-RK, O), P(RK, O), "HIDDEN")
    sh.dim_v(oy, oy + O, ox + RB, ox + RB + 26)
    sh.dim_h(ox, ox + p.C_PAD_R, oy + O / 2, oy - 26)
    sh.dim_h(ox + p.C_PAD_R - pr, ox + p.C_PAD_R + pr, oy + O, oy + O + 6, "<> pocket")
    sh.text(f"low infill (gyroid 10–15 %): base z 0–{O:g}, wall r {RK:g}–{RB:g}", P(-RB, -34))
    # centre line, sand surface
    sh.line(P(0, -8), P(0, HC + 8), "CENTER")
    sh.line(P(-RI, ZS), P(RI, ZS), "SAND")
    sh.text("sand surface", P(-RI + 2, ZS + 1.5), align=TextEntityAlignment.BOTTOM_LEFT)
    # sensors (layer SENSOR, for position only)
    for z in RODS:
        sh.rect(-RI + ox, z - T["rod_d"] / 2 + oy, -RI + T["rod_l"] + ox, z + T["rod_d"] / 2 + oy, "SENSOR")
    sh.rect(-RI - W - T["head_l"] + ox, PZ0 + 0.5 + oy, -RI - W + ox, PZ1 - 0.5 + oy, "SENSOR")
    sh.line(P(-RB - 15, zf), P(-RI + p.OF_TIP_FROM_WALL, zf), "SENSOR")
    sh.rect(p.PT100_R - 1.5 + ox, ZS - p.PT100_L + oy, p.PT100_R + 1.5 + ox, ZS - (p.PT100_L - p.PT100_METAL) + oy,
            "SENSOR")
    sh.line(P(p.PT100_R, ZS - (p.PT100_L - p.PT100_METAL)), P(p.PT100_R, ZS + 8), "SENSOR")
    # ---- dimensions: heights (left)
    sh.dim_v(oy, oy + HC, ox - RB, ox - RB - 46)
    sh.dim_v(oy, oy + H, ox - RB, ox - RB - 36)
    sh.dim_v(oy, oy + PZ1, ox - RB, ox - RB - 26)
    sh.dim_v(oy, oy + PZ0, ox - RB, ox - RB - 16)
    # heights (right)
    sh.dim_v(oy, oy + TB, ox + RB, ox + RB + 12)
    sh.dim_v(oy + TB, oy + ZS, ox + RB, ox + RB + 12, "100 (sand)")
    sh.dim_v(oy + ZS, oy + HC, ox + RB, ox + RB + 12)
    sh.dim_v(oy + TB, oy + HC, ox + RB, ox + RB + 26)
    sh.dim_v(oy + H, oy + HC, ox + RC, ox + RB + 40)
    sh.dim_v(oy + PZ0, oy + PZ1, ox - RB, ox - RB - 6)
    # rods: positions from the collar top + pitch
    sh.dim_v(oy + RODS[0], oy + HC, ox - RI + T["rod_l"], ox + 40, "<> (top rod)")
    # widths (top)
    sh.dim_h(ox - RI, ox + RI, oy + HC, oy + HC + 10)
    sh.dim_h(ox - RC, ox + RC, oy + HC, oy + HC + 20)
    sh.dim_h(ox + RI, ox + RC, oy + HC, oy + HC + 10)
    # widths (bottom)
    sh.dim_h(ox - RB, ox + RB, oy, oy - 14)
    sh.dim_h(ox - RI, ox - RI + T["rod_l"], oy + RODS[2] - 2, oy + TB + 14, "75 CS645 (meas. 77)")
    sh.dim_h(ox - RI, ox - RI + p.OF_TIP_FROM_WALL, oy + zf, oy + zf + 22, "<> fibre")
    sh.dim_h(ox, ox + p.PT100_R, oy + ZS, oy + ZS + 7)
    sh.dim_v(oy + ZS - p.PT100_L, oy + ZS, ox + p.PT100_R - 1.5, ox + p.PT100_R - 9, "37 Pt100")
    sh.dim_h(ox - RI - W - T["head_l"], ox - RI - W, oy + PZ0, oy + PZ0 - 12, "19 head")
    sh.dim_h(ox - RI - W, ox - RI, oy + PZ1, oy + PZ1 + 7)
    sh.dim_r(P(RI - r, TB + r), r, 315)
    sh.text("SECTION A–A  (along the TDR axis)", (ox - RB, oy + HC + 40), h=TH)


def plan(sh, ox, oy):
    """PLAN (from above): port at the bottom (270°), TDR axis vertical."""
    P = lambda x, y: (ox + x, oy + y)
    for r in (RB, RC, RI):
        sh.circle(P(0, 0), r)
    sh.circle(P(0, 0), RI + W, "HIDDEN")
    sh.circle(P(0, 0), RK, "HIDDEN")
    for k in range(3):
        a_ = math.radians(90 + 120 * k)
        sh.circle(P(p.C_PAD_R * math.cos(a_), p.C_PAD_R * math.sin(a_)), (p.C_PAD_D + 0.4) / 2, "HIDDEN")
    sh.line(P(-RB - 8, 0), P(RB + 8, 0), "CENTER")
    sh.line(P(0, -RB - 8), P(0, RB + 8), "CENTER")
    hw = p.PORT_W / 2
    yb = -math.sqrt(RB ** 2 - hw ** 2)
    sh.poly([P(-hw, yb), P(-hw, -RI - W), P(hw, -RI - W), P(hw, yb)], "HIDDEN", close=False)
    # sensors
    sh.rect(ox - T["rod_d"] / 2, oy - RI, ox + T["rod_d"] / 2, oy - RI + T["rod_l"], "SENSOR")
    sh.line(P(-p.OF_SIDE, -RB - 15), P(-p.OF_SIDE, -RI + p.OF_TIP_FROM_WALL), "SENSOR")
    sh.circle(P(p.PT100_R, 0), 1.5, "SENSOR")
    sh.dim_d(P(0, 0), RB, 45)
    sh.dim_d(P(0, 0), RC, 135)
    sh.dim_d(P(0, 0), RI, 160)
    sh.dim_h(ox - hw, ox + hw, oy + yb, oy - RB - 14, "13 (port)")
    sh.dim_h(ox - p.OF_SIDE, ox, oy - RI + p.OF_TIP_FROM_WALL, oy - 30, "<> fibre")
    sh.dim_h(ox, ox + p.PT100_R, oy, oy + 30, "15 Pt100")
    sh.text("PLAN  (from above)", (ox - RB, oy + RB + 30), h=TH)
    sh.text("A", P(-RB - 14, -2), h=TH)
    sh.text("A", P(RB + 8, -2), h=TH)


def port_view(sh, ox, oy):
    """VIEW M: the port from outside."""
    hh = PZ1 - PZ0
    P = lambda x, z: (ox + x, oy + z)
    sh.rect(ox - p.PORT_W / 2, oy, ox + p.PORT_W / 2, oy + hh)
    for z in RODS:
        sh.circle(P(0, z - PZ0), 1.75)
    sh.circle(P(-p.OF_SIDE, RODS[0] + 2 - PZ0), 0.75)
    sh.dim_h(ox - p.PORT_W / 2, ox + p.PORT_W / 2, oy + hh, oy + hh + 8)
    sh.dim_v(oy, oy + hh, ox + p.PORT_W / 2, ox + p.PORT_W / 2 + 10)
    sh.dim_v(oy + RODS[2] - PZ0, oy + RODS[0] - PZ0, ox - p.PORT_W / 2, ox - p.PORT_W / 2 - 10,
             "2× 8.9")
    sh.text("VIEW M  (port from outside)", (ox - 40, oy + hh + 20), h=TH)
    sh.text("3× ⌀3.5 rods, ⌀1.5 fibre", (ox - 40, oy - 10))


def frame_and_title(sh, x0, y0):
    w, h = 420 * S, 297 * S
    # no sheet border (title block only)
    tx, ty = x0 + w - 10 * S - 180 * S, y0 + 10 * S
    sh.rect(tx, ty, x0 + w - 10 * S, ty + 40 * S, "FRAME")
    for k in (10, 20, 30):
        sh.line((tx, ty + k * S), (x0 + w - 10 * S, ty + k * S), "FRAME")
    rows = [("Title", "E7 – cell rev. B, printed in ONE piece ⌀240 × 200"),
            ("Drawing", "E7-V04   sheet 1/1   scale 1 : 1.5 (A3)   mm"),
            ("Material", "PETG(-CF); base + wall gyroid 10–15 %, floor 100 %"),
            ("Ref.", "core: M. Vrána 23.06.2026; rev. B 2026-10-27, DRAFT")]
    for i, (a, b) in enumerate(rows):
        yy = ty + (35 - 10 * i) * S
        sh.text(a, (tx + 2 * S, yy - 1.8 * S), h=TS)
        sh.text(b, (tx + 25 * S, yy - 1.8 * S), h=TS * 1.1)
    notes = ["NOTES",
             "1  General tolerance ±0.2; cavity ⌀100 ±0.1 (ream/sand after printing).",
             "2  Sensor positions (green, layer SENSOR) are for information – CS645 rods",
             "   centred in the port (pitch 8.9 ≈ 9), fibre tip 37.5 from the wall,",
             "   Pt100 37 mm vertical, 15 from the axis. Check: Pt100 tip or length?",
             f"3  Sand 100 mm (z {TB:g}–{ZS:g}), 34 mm free above for the piston / camera.",
             f"   3 G10 pads ⌀{p.C_PAD_D:g} × {O:g} in pockets ⌀{p.C_PAD_D + 0.4:g} (r {p.C_PAD_R:g}), 0.5 mm proud.",
             "4  Inside: epoxy coat + PTFE spray + silicone grease.",
             "5  Port 13 × 27 runs through the whole wall (r 50–120); Pt100 cable ⌀4 at the top (0°).",
             "   Print bed ≥ 250 × 250, Z ≥ 200; ≈ 1.3–1.6 kg, ≈ 40–60 h."]
    for i, s in enumerate(notes):
        sh.text(s, (x0 + 20 * S, y0 + (78 - 7 * i) * S), h=TS)


def main():
    os.makedirs(OUT, exist_ok=True)
    doc = setup()
    sh = Sheet(doc)
    x0, y0 = 0.0, 0.0
    frame_and_title(sh, x0, y0)
    section(sh, x0 + 190, y0 + 180)
    plan(sh, x0 + 490, y0 + 300)
    port_view(sh, x0 + 455, y0 + 100)
    path = os.path.join(OUT, "E7_V04_cell.dxf")
    doc.saveas(path)
    # preview
    from ezdxf.addons.drawing import matplotlib as mpl_draw
    import matplotlib
    matplotlib.use("Agg")
    mpl_draw.qsave(doc.modelspace(), os.path.join(OUT, "E7_V04_cell.pdf"), bg="#FFFFFF", dpi=200)
    # PNG on a true A3 sheet (420 × 297 mm) at 300 dpi
    import matplotlib.pyplot as plt
    from ezdxf.addons.drawing import Frontend, RenderContext
    from ezdxf.addons.drawing.config import BackgroundPolicy, Configuration
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    fig = plt.figure(figsize=(420 / 25.4, 297 / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    Frontend(RenderContext(doc), MatplotlibBackend(ax),
             config=Configuration(background_policy=BackgroundPolicy.WHITE)).draw_layout(doc.modelspace())
    ax.set_xlim(0, 420 * S)
    ax.set_ylim(0, 297 * S)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.set_size_inches(420 / 25.4, 297 / 25.4)          # the backend shrinks the figure – restore A3
    fig.savefig(os.path.join(OUT, "E7_V04_cell.png"), dpi=300, facecolor="white")
    plt.close(fig)
    print("ok", path)


if __name__ == "__main__":
    main()
