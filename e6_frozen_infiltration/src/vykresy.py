"""E6 drawings (A3, English). Run: python vykresy.py → ../vykresy/E6_drawings.pdf + one PNG per sheet."""
import math
import os

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

import params as p
import termometrie as tm
from drafting import (BLUE, FROZEN, FS, FS_SMALL, INK, INSUL, METAL, PLASTIC, RED,
                      THICK, THIN, WATER, Sheet, View, table)

OUT = os.path.join(os.path.dirname(__file__), "..", "vykresy")
TOTAL = 9
BROWN = "#7a5a2a"
FOAM = "#e7dcc6"

# derived geometry; z = 0 is the top face of the membrane = bottom of the soil
R, RO = p.D_COL / 2, p.D_OUT / 2
Z_TOP = p.H_SOIL
R_DISK, R_SAND, R_HEAD, H_HEAD = p.D_DISK / 2, 24.0, 28.0, 22.0
Z_HEAD = Z_TOP + p.T_SAND
R_RAFT_I, R_RAFT_O, H_RAFT = 30.0, 48.0, p.INS_TOP
FL_R, FL_T, BOLT_R = 70.0, 6.0, 62.5
R_INS = RO + p.INS
Z_SUP = -(p.T_SUPPORT + p.T_MEMBR)
Z_GROOVE = Z_SUP - p.GROOVE
R_MEMBR = 52.0
OR_R = 53.5
# cone
CR, CT = p.CONE_RIM_R, p.CONE_RIM_T
Z_CONE0 = -CT
Z_TIP = Z_CONE0 - p.CONE_H
Z_NOZ = Z_TIP - p.NOZZLE_L
R_NOZ = 3.0
STAND_I, STAND_O, STAND_T = 57.0, 112.0, 10.0
Z_STAND = Z_CONE0 - STAND_T
POST_X, Z_BRIDGE = 92.0, 160.0
TH_CONE_Z = -4.5


def dz(d):
    return Z_TOP - d


def soil_texture(v, x0, x1, z0, z1, seed=3, n=260):
    import random
    rnd = random.Random(seed)
    for _ in range(n):
        v.circle(rnd.uniform(x0 + 1.5, x1 - 1.5), rnd.uniform(z0 + 1.5, z1 - 1.5),
                 rnd.uniform(0.35, 1.1), fc="#b9a888", ec="none", lw=0, z_=2.1)


def cone_outline(s):
    """Half outline of the cone body (side s = ±1)."""
    return [(0, 0), (s * CR, 0), (s * CR, Z_CONE0), (s * p.CONE_R_TOP, Z_CONE0),
            (s * p.CONE_R_TIP, Z_TIP), (s * R_NOZ, Z_TIP), (s * R_NOZ, Z_NOZ), (0, Z_NOZ)]


def cone_normal_pt(s, t, off):
    """Point on the conical surface (t = 0 top … 1 tip), offset `off` along the outward normal."""
    x = p.CONE_R_TOP + t * (p.CONE_R_TIP - p.CONE_R_TOP)
    z = Z_CONE0 - t * p.CONE_H
    n = 1 / math.sqrt(2)
    return s * (x + off * n), z - off * n


def draw_cone(v, detail=True):
    for s in (-1, 1):
        v.poly(cone_outline(s), fc=METAL, hatch="////")
    v.rect(-R - 0.25, Z_SUP, R + 0.25, 0, fc="white", lw=THIN)
    v.rect(-R, Z_SUP, R, -p.T_MEMBR, fc="#9aa3ab", lw=THIN, hatch="xxxx")
    v.rect(-R_MEMBR, -p.T_MEMBR, R_MEMBR, 0, fc="#e9d9a8", lw=THIN)
    for xg in (0, -15, 15, -30, 30, -45, 45):
        v.rect(xg - 0.5, Z_GROOVE, xg + 0.5, Z_SUP, fc=WATER, lw=THIN)
    v.rect(-p.BORE_D / 2, Z_NOZ, p.BORE_D / 2, Z_GROOVE, fc=WATER, lw=THIN)
    # air purge (+x) and cone thermistor (−x)
    v.rect(44.25, -5.75, 45.75, Z_GROOVE, fc=WATER, lw=THIN)
    v.rect(44.25, -5.75, CR, -4.25, fc=WATER, lw=THIN)
    v.rect(CR, -7, CR + 7, -3, fc=METAL, lw=THIN)
    v.rect(-CR, TH_CONE_Z - 0.8, -20, TH_CONE_Z + 0.8, fc="#444", lw=0)
    v.circle(-20, TH_CONE_Z, 0.9, fc=INK, lw=0)
    for s in (-1, 1):
        v.circle(s * OR_R, -0.9, 1.0, fc="#333", lw=0)
    v.rect(BOLT_R - 2.5, -7, BOLT_R + 2.5, 0, fc="#888", lw=THIN)
    if detail:
        for s in (-1, 1):
            for t in (0.12, 0.34, 0.56, 0.78):
                v.circle(*cone_normal_pt(s, t, 3.2), 3.0, fc="#d08a4a", lw=THIN)


def draw_cone_insulation(v):
    n = 1 / math.sqrt(2)
    for s in (-1, 1):
        ox, oz = p.CONE_R_TOP + 20 * n, Z_CONE0 - 20 * n          # outer offset line point
        x18 = ox + (Z_STAND - oz)                                 # outer line at z = Z_STAND
        z_bot = Z_TIP - 6
        xb = ox - (oz - z_bot)
        pts = [(p.CONE_R_TOP, Z_CONE0), (STAND_I, Z_CONE0), (STAND_I, Z_STAND), (x18, Z_STAND),
               (xb, z_bot), (R_NOZ + 1, z_bot), (R_NOZ + 1, Z_TIP), (p.CONE_R_TIP, Z_TIP)]
        v.poly([(s * a, b) for a, b in pts], fc=FOAM, lw=THIN, hatch="oo", z=1.8)


# ---------------------------------------------------------------------------
def sheet_v01(pdf):
    sh = Sheet("Column assembly – section A–A", "E6-V01", "1 : 1", 1, TOTAL,
               "axisymmetric section; off-plane items revolved into the section plane (angles: E6-V02)")
    v = View(sh, 135, 96, 1.0)

    # stand and legs
    for s in (-1, 1):
        v.rect(s * STAND_I, Z_STAND, s * STAND_O, Z_CONE0, fc=PLASTIC, hatch="....")
        v.rect(s * 100, -78, s * 112, Z_STAND, fc=PLASTIC, hatch="....")
        v.break_line(s * 98, s * 114, -78)
    draw_cone_insulation(v)
    draw_cone(v)
    v.line([(0, Z_NOZ), (0, -84), (40, -84)], c=BLUE, lw=THICK)
    v.text(42, -84, "to V3 → overflow cup (E6-V06)", fontsize=FS_SMALL, va="center", color=BLUE)
    v.text(CR + 9, -5, "V4", fontsize=FS_SMALL, va="center")

    # tube, flange, bolts, insulation
    for s in (-1, 1):
        v.rect(s * R, 0, s * RO, p.L_TUBE, fc="#dfeef5", hatch="\\\\\\\\")
        v.rect(s * RO, 0, s * FL_R, FL_T, fc="#dfeef5", hatch="\\\\\\\\")
        v.rect(s * RO, FL_T + 4, s * R_INS, p.L_TUBE + 5, fc=INSUL, lw=THIN, hatch="oo")
        v.rect(s * FL_R, Z_CONE0, s * R_INS, FL_T + 4, fc=INSUL, lw=THIN, hatch="oo")

    # soil, sand, head, disc
    v.rect(-R, 0, R, Z_TOP, fc=FROZEN, lw=THIN)
    soil_texture(v, -R, R, 0, Z_TOP)
    v.rect(-R_SAND, Z_TOP, R_SAND, Z_HEAD, fc="#e8d8a0", lw=THIN, hatch="....")
    v.rect(-R_HEAD, Z_HEAD, R_HEAD, Z_HEAD + H_HEAD, fc=PLASTIC, hatch="////")
    v.rect(-R_DISK, Z_HEAD, R_DISK, Z_HEAD + p.T_DISK, fc="#8d99a6", lw=THIN, hatch="xxxx")
    v.rect(-20, Z_HEAD + p.T_DISK, 20, Z_HEAD + 10, fc=WATER, lw=THIN)
    for xh in (-12, 12):
        v.rect(xh - 1, Z_HEAD + 10, xh + 1, Z_HEAD + H_HEAD, fc=WATER, lw=THIN)
        v.rect(xh - 3, Z_HEAD + H_HEAD, xh + 3, Z_HEAD + H_HEAD + 6, fc=METAL, lw=THIN)
    v.line([(-12, Z_HEAD + H_HEAD + 6), (-12, 142), (-70, 142), (-70, 150)], c=BLUE, lw=THICK)
    v.line([(12, Z_HEAD + H_HEAD + 6), (12, 138), (40, 138)], c=BLUE, lw=THICK)
    v.rect(40, 133, 52, 143, fc="white", lw=THIN)
    v.text(46, 138, "PT", fontsize=FS_SMALL, ha="center", va="center")
    v.text(-70, 152, "from Mariotte bottle (E6-V06)", fontsize=FS_SMALL, ha="center", va="bottom", color=BLUE)

    # floating ring, heat-flux plate (revolved to −x), needles (+x)
    for s in (-1, 1):
        v.rect(s * R_RAFT_I, Z_TOP, s * R_RAFT_O, Z_TOP + H_RAFT, fc=INSUL, lw=THIN, hatch="oo")
        v.rect(s * R_RAFT_I, Z_TOP + H_RAFT - 2, s * R_RAFT_O, Z_TOP + H_RAFT, fc=PLASTIC, lw=THIN)
    v.rect(-41, Z_TOP, -31, Z_TOP + 0.6, fc=RED, lw=0)
    for d, xx in ((2, 33), (6, 39)):
        v.line([(xx, Z_TOP + 10), (xx, dz(d))], lw=THICK, c="#444")
        v.circle(xx, dz(d), 0.9, fc=INK, lw=0)

    # wall thermistors (revolved: cos > 0 → +x side)
    for d, ang in p.THERMISTORS:
        s = 1 if math.cos(math.radians(ang)) > 0.01 else -1
        z = dz(d)
        v.line([(s * R_INS, z), (s * p.TH_R, z)], lw=THICK, c="#444")
        v.circle(s * p.TH_R, z, 1.2, fc=INK, lw=0)
        v.text(s * (R_INS + 2), z, f"T{d} ({ang}°)", fontsize=FS_SMALL, va="center",
               ha="left" if s > 0 else "right")

    # TDR
    for name, d, yoff, L, ins in p.TDR:
        z = dz(d)
        if yoff == 0:
            v.line([(-R, z), (-R + L, z)], lw=1.6, c=BROWN)
            v.line([(-R, z), (-R + ins, z)], lw=3.2, c="#555")
            v.rect(-R_INS - 6, z - 4, -RO, z + 4, fc=BROWN, lw=THIN)
            v.text(-R + L + 1.5, z + 1.5, name, fontsize=FS_SMALL, color=BROWN)
        else:
            x0 = -math.sqrt(R ** 2 - yoff ** 2)
            for dzr in (-p.TDR_PITCH, 0, p.TDR_PITCH):
                v.hidden([(x0, z + dzr), (x0 + L, z + dzr)], c=BROWN)
            v.text(x0 + L + 1.5, z - 7.5, f"{name} (behind)",
                   fontsize=FS_SMALL, color=BROWN)

    v.rect(BOLT_R - 2.5, 0, BOLT_R + 2.5, FL_T, fc="#888", lw=THIN)
    v.rect(BOLT_R - 4.5, FL_T, BOLT_R + 4.5, FL_T + 4, fc="#888", lw=THIN)
    # LVDT bridge
    for s in (-1, 1):
        v.rect(s * POST_X - 4, Z_CONE0, s * POST_X + 4, Z_BRIDGE, fc=METAL, lw=THIN)
    v.rect(-POST_X - 6, Z_BRIDGE, POST_X + 6, Z_BRIDGE + 8, fc=METAL, hatch="////")
    for xl, zt in ((0, Z_HEAD + H_HEAD + 6), (38, Z_TOP + H_RAFT)):
        v.rect(xl - 4, Z_BRIDGE - 20, xl + 4, Z_BRIDGE, fc="white", lw=THIN)
        v.line([(xl, Z_BRIDGE - 20), (xl, zt)], lw=THICK)
    v.axis_line([(0, -90), (0, Z_BRIDGE + 14)])

    B = v.balloon
    B(25, -20, 1, 125, -40)
    B(-35, -1.2, 2, -125, -2)
    B(-30, -0.07, 3, -125, 7)
    B(15, Z_GROOVE + 0.5, 4, 30, -60)
    B(0, -40, 5, -30, -70)
    B(CR + 4, -5, 6, 125, -14)
    B(-OR_R, -0.9, 7, -125, -11)
    B(-52.5, 60, 8, -125, 50)
    B(-64, 3, 9, -125, 18)
    B(-20, 20, 10, -125, 34)
    B(-23, Z_TOP + 1, 11, -62, 124)
    B(-17, Z_HEAD + 1.5, 12, -50, 131)
    B(-24, Z_HEAD + 16, 13, -36, 135)
    B(-40, 142, 14, -40, 150)
    B(46, 143, 15, 46, 152)
    B(44, Z_TOP + 12, 16, 70, 132)
    B(-36, Z_TOP + 0.3, 17, -62, 112)
    B(39, dz(6), 18, 72, 116)
    B(-p.TH_R, dz(50), 19, -30, 28)
    B(0, dz(27), 20, 22, 82)
    B(-R_INS + 10, 112, 22, -125, 118)
    B(*cone_normal_pt(1, 0.56, 3.2), 23, 125, -28)
    B(-40, -40, 24, -125, -50)
    B(-80, -14, 25, -125, -30)
    B(0, Z_BRIDGE + 4, 26, 30, 174)
    B(38, Z_BRIDGE - 10, 27, 62, 174)
    B(-20, TH_CONE_Z, 28, -125, -20)

    v.dim_v(0, Z_TOP, -R, -R_INS - 22, "100 (sample height)")
    v.dim_v(0, p.L_TUBE, -RO, -R_INS - 34)
    v.dim_v(Z_TIP, Z_CONE0, -p.CONE_R_TIP, -60, "46")
    v.dim_h(-R, R, 0, 5, "⌀100 H8 (sample)")
    v.dim_h(-RO, RO, p.L_TUBE, p.L_TUBE + 8, "⌀110")
    v.dim_h(-R_DISK, R_DISK, Z_HEAD, Z_HEAD - 5, "⌀45")

    sh.heading(255, 276, "Parts list")
    items = [
        "cone outlet body, Al 6082, solid, 45° (E6-V04)",
        "perforated support plate AISI 316, t 2, holes ⌀1.5 / pitch 4",
        "nylon membrane 20 µm, ⌀104, clamped by tube end face",
        "drainage grooves 1×1: 12 radial + 3 rings (r 15/30/45)",
        "axial bore ⌀1.5 → nozzle ⌀6 → PTFE 1/16\" → valve V3",
        "air-purge port from ring groove r 45, valve V4",
        "O-ring ⌀107×2 NBR, face seal",
        "PMMA tube ⌀110/100×125, inner wall sand-coated (epoxy)",
        "PMMA flange ⌀140×6, bonded; 4× M5 into cone rim",
        "soil sample ⌀100×100, packed in 10 mm lifts",
        "contact sand 0.1–0.3 mm, t 2, ⌀48, placed dry",
        "sintered disc ⌀45×3, stainless (as Mini Disk / AMDI)",
        "AMDI head body, PETG – low-profile variant, 2 ports",
        "supply line from Mariotte bottle on balance, FEP 4/2",
        "diff. pressure sensor at disc ±2.5 kPa (+ air purge)",
        "floating insulation ring XPS ⌀96/60×20, PETG frame",
        "heat-flux sensor 10×10 mm, 2× at r 36 (45°, 225°)",
        "thermistor needles in ring, 2 and 6 mm (135°, 315°)",
        "wall thermistor ⌀1.6, tip at r 9, 6× helix at 60°",
        "centre TDR C27, C60: 3 rods ⌀1.6×75, 25 mm insulated",
        "annulus TDR A27: chord y 36, 3 rods ⌀1.6×50, stacked",
        "side insulation Kaiflex t 30",
        "Cu coil ⌀6, 4 turns on cone → circulating bath",
        "cone insulation, PU foam shell t 20",
        "stand plate POM t 10, 3 legs",
        "LVDT bridge, Al 20×8 on posts from stand plate",
        "LVDT ±10 mm: 0 – head, 1/2 – ring (90°, 270°)",
        "thermistor in cone, 4.5 mm below membrane",
    ]
    y = 270
    for i, it in enumerate(items, 1):
        sh.ax.add_patch(Circle((259, y), 2.2, fc="white", ec=INK, lw=THIN))
        sh.text(259, y, str(i), fontsize=FS_SMALL - 0.5, ha="center", va="center")
        sh.text(264, y, it, fontsize=FS_SMALL, va="center")
        y -= 6.0
    sh.text(255, y - 1, "z = 0: top face of membrane = bottom of sample.\n"
                        "Sensor depths refer to the initial surface z = 100.\n"
                        "Item 21 lies behind the section plane (dashed).",
            fontsize=FS_SMALL, va="top")
    sh.save(pdf, os.path.join(OUT, "E6-V01_assembly.png"))


# ---------------------------------------------------------------------------
def polar(ang, r):
    a = math.radians(ang)
    return r * math.cos(a), r * math.sin(a)


def sheet_v02(pdf):
    sh = Sheet("Sensor layout – plan view", "E6-V02", "1 : 1", 2, TOTAL,
               "angle 0° = +x (right half of section A–A), counter-clockwise seen from above")
    v = View(sh, 125, 180, 1.0)
    v.circle(0, 0, R_INS, fc=INSUL, lw=THIN, z_=1)
    v.circle(0, 0, RO, fc="#dfeef5", lw=THICK, z_=1.2)
    v.circle(0, 0, R, fc=FROZEN, lw=THICK, z_=1.4)
    v.circle(0, 0, R_RAFT_O, fc="none", lw=THIN, ls="--", z_=1.6)
    v.circle(0, 0, R_RAFT_I, fc="none", lw=THIN, ls="--", z_=1.6)
    v.circle(0, 0, R_HEAD, fc=PLASTIC, lw=THIN, z_=1.7)
    v.circle(0, 0, R_DISK, fc="#8d99a6", lw=THICK, z_=1.8)
    for ang in (45, 135, 225, 315):
        v.circle(*polar(ang, BOLT_R), 2.75, fc="none", lw=THIN, ls="--", z_=1.5)
    v.axis_line([(-R_INS - 12, 0), (R_INS + 12, 0)])
    v.axis_line([(0, -R_INS - 12), (0, R_INS + 12)])
    for s, lab in ((-1, "A"), (1, "A")):
        v.line([(s * (R_INS + 6), 0), (s * (R_INS + 14), 0)], lw=THICK)
        v.text(s * (R_INS + 16), 3, lab, fontsize=FS + 2, weight="bold", ha="center")
    for ang in range(0, 360, 30):
        x, y = polar(ang, R_INS + 4)
        v.text(x, y, f"{ang}°", fontsize=FS_SMALL - 1, ha="center", va="center", color="#666")
    # wall thermistors
    for d, ang in p.THERMISTORS:
        x0, y0 = polar(ang, R_INS)
        x1, y1 = polar(ang, p.TH_R)
        v.line([(x0, y0), (x1, y1)], lw=THICK, c="#444")
        v.circle(x1, y1, 1.1, fc=INK, lw=0, z_=4)
        lx, ly = polar(ang + 6, 30)
        v.text(lx, ly, f"T{d}", fontsize=FS_SMALL, ha="center", va="center",
               bbox=dict(fc="white", ec="none", pad=0.2))
    # TDR
    for name, d, yoff, L, ins in p.TDR:
        if yoff == 0:
            if d == p.TDR[0][1]:
                for yy in (-p.TDR_PITCH, 0, p.TDR_PITCH):
                    v.line([(-R, yy), (-R + L, yy)], lw=1.4, c=BROWN)
                    v.line([(-R, yy), (-R + ins, yy)], lw=2.8, c="#555")
                v.text(-R + L + 2, -p.TDR_PITCH - 8, "TDR-C27 / C60\n(same plan position)",
                       fontsize=FS_SMALL, color=BROWN, va="top")
        else:
            x0 = -math.sqrt(R ** 2 - yoff ** 2)
            v.line([(x0, yoff), (x0 + L, yoff)], lw=1.4, c=BROWN)
            v.text(x0 + L + 2, yoff, name, fontsize=FS_SMALL, color=BROWN, va="center")
    for ang, r in p.HFP:
        x, y = polar(ang, r)
        h = p.HFP_SIZE / 2
        v.rect(x - h, y - h, x + h, y + h, fc=RED, lw=THIN, z=4)
    for d, ang, r in p.RAFT_TH:
        x, y = polar(ang, r)
        v.circle(x, y, 1.2, fc="#444", lw=0, z_=4)
    for name, ang, r in p.LVDT:
        x, y = polar(ang, r)
        v.circle(x, y, 2.5, fc="white", lw=THIN, z_=4)
        v.line([(x - 2.5, y), (x + 2.5, y)], lw=THIN)
        v.line([(x, y - 2.5), (x, y + 2.5)], lw=THIN)
    v.note(*polar(45, 36), "heat-flux plate", 70, 72)
    v.note(*polar(135, 36), "needle T2", -70, 72)
    v.note(*polar(315, 36), "needle T6", 70, -72)
    v.note(0, -38, "LVDT-2", 30, -88)
    v.note(0, 38, "LVDT-1", 30, 92)
    v.note(*polar(10, 26), "disc ⌀45 / head ⌀56", 70, -88)
    v.dim_h(-R_DISK, R_DISK, 0, -60, "⌀45")
    v.dim_h(R_DISK, R, 0, -60, "27.5")

    rows = []
    for d, ang in p.THERMISTORS:
        rows.append([f"T{d}", "thermistor, wall", f"{ang}", f"{p.TH_R:g}", f"{d}", f"{dz(d):g}"])
    for d, ang, r in p.RAFT_TH:
        rows.append([f"T{d}r", "thermistor needle, ring", f"{ang}", f"{r:g}", f"{d}", "floats"])
    rows += [["Tdisc", "thermistor, disc/sand", "180", "7", "0", "floats"],
             ["Tcone", "thermistor, cone", "180", "20", "–", f"{TH_CONE_Z:g}"]]
    for name, d, yoff, L, ins in p.TDR:
        rows.append([name, f"TDR 3×⌀1.6×{L}" + (f", {ins} ins." if ins else ""),
                     "180" if yoff == 0 else "chord", f"y={yoff:g}", f"{d}", f"{dz(d):g}"])
    for i, (ang, r) in enumerate(p.HFP, 1):
        rows.append([f"HF{i}", "heat-flux 10×10", f"{ang}", f"{r:g}", "0", "floats"])
    for name, ang, r in p.LVDT:
        rows.append([name, "LVDT ±10 mm", f"{ang}" if r else "–", f"{r:g}", "–", "top"])
    sh.heading(240, 278, "Sensor schedule")
    table(sh, 240, 274, ["ID", "type", "angle °", "r / y", "depth", "z"], rows,
          [16, 52, 16, 14, 13, 14], row_h=4.4)
    sh.text(240, 60, "depth = mm below the initial surface; z = height above the membrane.\n"
                     "Ring sensors float with the surface: they record heave / thaw settlement\n"
                     "via LVDT-1/2 and keep a fixed depth below the moving surface.",
            fontsize=FS_SMALL, va="top")
    sh.save(pdf, os.path.join(OUT, "E6-V02_sensor_layout.png"))


# ---------------------------------------------------------------------------
def wall_holes():
    """(id, angle on outer surface °, z, ⌀, direction, purpose)."""
    H = []
    for d, ang in p.THERMISTORS:
        H.append((f"T{d}", ang, dz(d), 2.0, "radial", "thermistor ⌀1.6 + gland"))
    for name, d, yoff, L, ins in p.TDR:
        z = dz(d)
        if yoff == 0:
            for k, yy in enumerate((-p.TDR_PITCH, 0, p.TDR_PITCH)):
                ang = math.degrees(math.atan2(yy, -math.sqrt(RO ** 2 - yy ** 2))) % 360
                H.append((f"{name}.{k + 1}", ang, z, 2.0, "parallel to x", "TDR rod ⌀1.6"))
        else:
            ang = math.degrees(math.atan2(yoff, -math.sqrt(RO ** 2 - yoff ** 2))) % 360
            for k, dzr in enumerate((-p.TDR_PITCH, 0, p.TDR_PITCH)):
                H.append((f"{name}.{k + 1}", ang, z + dzr, 2.0, "parallel to x (41° to wall)", "TDR rod ⌀1.6"))
    return H


def sheet_v03(pdf):
    sh = Sheet("Column tube – developed outer surface", "E6-V03", "1 : 1", 3, TOTAL,
               "PMMA tube ⌀110/100 × 125, seen from outside; angle increases to the right")
    circ = math.pi * p.D_OUT
    k = circ / 360.0
    v = View(sh, 40, 140, 1.0)
    v.rect(0, 0, circ, p.L_TUBE, fc="#eef6fa", lw=THICK)
    v.rect(0, 0, circ, FL_T, fc="#dfeef5", lw=THIN, hatch="\\\\\\\\")
    v.text(circ / 2, FL_T / 2, "bonded flange ⌀140 × 6 (behind)", fontsize=FS_SMALL, ha="center", va="center")
    v.line([(0, Z_TOP), (circ, Z_TOP)], lw=THIN, ls="--", c=BLUE)
    v.text(4, Z_TOP + 2, "initial soil surface z = 100", fontsize=FS_SMALL, va="bottom", color=BLUE)
    for ang in range(0, 361, 30):
        x = ang * k
        v.line([(x, -3), (x, 0)], lw=THIN)
        v.text(x, -5, f"{ang}°", fontsize=FS_SMALL - 0.5, ha="center", va="top")
        if 0 < ang < 360:
            v.line([(x, 0), (x, p.L_TUBE)], lw=0.3, c="#bbbbbb", z=1)
    for hid, ang, z, d, direc, purpose in wall_holes():
        x = ang * k
        v.circle(x, z, d / 2 + 0.3, fc="white", lw=THICK, z_=4)
        v.line([(x - 2.5, z), (x + 2.5, z)], lw=0.3)
        v.line([(x, z - 2.5), (x, z + 2.5)], lw=0.3)
        if hid.startswith("T") and not hid.startswith("TDR"):
            v.text(x + 2.4, z + 1.6, hid, fontsize=FS_SMALL - 1, zorder=6)
        elif hid.endswith(".2"):
            v.text(x + 4, z + (9 if "C" in hid else 0), hid[:-2] + " (3 holes)", fontsize=FS_SMALL - 1, zorder=6)
    v.dim_h(0, circ, p.L_TUBE, p.L_TUBE + 8, f"{circ:.1f} = π × 110")
    v.dim_v(0, p.L_TUBE, 0, -8)
    v.dim_v(0, Z_TOP, circ, circ + 10, "100")

    rows = [[h[0], f"{h[1]:.1f}", f"{h[1] * k:.1f}", f"{h[2]:.0f}", f"⌀{h[3]:.1f}", h[4], h[5]]
            for h in wall_holes()]
    sh.heading(30, 112, "Hole table")
    table(sh, 30, 108, ["ID", "angle °", "arc mm", "z", "hole", "direction", "purpose"], rows,
          [20, 14, 14, 10, 12, 40, 40], row_h=4.4)
    sh.text(250, 108, "Notes\n"
            "1  Arc length measured on ⌀110 from 0°; z from the tube end face (= membrane top).\n"
            "2  Drill TDR holes on CNC with a fixture: rods are parallel to the x axis, not radial.\n"
            "3  Seal glands with silicone (low-temperature grade); check at −10 °C before use.\n"
            "4  Inner wall: thin epoxy + 0.3–0.5 mm sand coat against wall flow; mask holes.\n"
            "5  Holes in the insulation jacket follow the same pattern.",
            fontsize=FS_SMALL, va="top", linespacing=1.6)
    sh.save(pdf, os.path.join(OUT, "E6-V03_tube_developed.png"))


# ---------------------------------------------------------------------------
def sheet_v04(pdf):
    sh = Sheet("Cone outlet with suction membrane", "E6-V04", "1 : 1 / 5 : 1", 4, TOTAL,
               "solid Al cone: external 45° funnel, internal drainage volume ≈ 1.2 mL")
    v = View(sh, 105, 215, 1.0, "SECTION B–B  1 : 1", (105, 276))
    draw_cone(v)
    v.axis_line([(0, Z_NOZ - 8), (0, 8)])
    v.dim_h(-CR, CR, 0, 12, "⌀140")
    v.dim_h(-p.CONE_R_TOP, p.CONE_R_TOP, Z_CONE0, -30, "⌀110")
    v.dim_h(-p.CONE_R_TIP, p.CONE_R_TIP, Z_TIP, Z_TIP - 4, "⌀18", side="below")
    v.dim_v(Z_CONE0, 0, -CR, -CR - 8, "8")
    v.dim_v(Z_TIP, Z_CONE0, -p.CONE_R_TOP, -CR - 8, "46")
    v.dim_v(Z_NOZ, Z_TIP, -R_NOZ, -CR - 8, "12")
    v.note(0, -30, "axial bore ⌀1.5", 30, -62)
    v.note(45, -5, "purge bore ⌀1.5 → V4 (M5 port)", 75, 14)
    v.note(-30, TH_CONE_Z, "thermistor bore ⌀1.7, depth 50 (at 180°)", -40, -72)
    v.note(*cone_normal_pt(1, 0.34, 3.2), "Cu coil ⌀6, 4 turns,\nthermal epoxy", 72, -40)
    v.note(BOLT_R, -3, "4× M5, depth 7 (at 45°, revolved)", 80, 4)
    v.note(0, Z_NOZ, "nozzle ⌀6, 1/4\"-28 flat-bottom port", 30, Z_NOZ - 4)
    # plan of the top face
    t = View(sh, 300, 225, 0.5, "VIEW C – top face (membrane removed)  1 : 2", (320, 276))
    t.circle(0, 0, CR, fc=METAL, lw=THICK, z_=1)
    t.circle(0, 0, R + 0.25, fc="#d7dbdf", lw=THIN, z_=1.2)
    for r in p.RING_R:
        t.circle(0, 0, r, fc="none", ec=BLUE, lw=1.4, z_=2)
    for i in range(p.N_GROOVE):
        a = 2 * math.pi * i / p.N_GROOVE
        t.line([(0, 0), ((R - 3) * math.cos(a), (R - 3) * math.sin(a))], c=BLUE, lw=1.4)
    t.circle(0, 0, OR_R, fc="none", lw=THIN, ls="--", z_=2)
    t.circle(0, 0, 25, fc="none", ec=RED, lw=THIN, ls=(0, (2, 2)), z_=2)
    for ang in (45, 135, 225, 315):
        t.circle(*polar(ang, BOLT_R), 2.5, fc="white", lw=THIN, z_=3)
    t.circle(0, 0, 0.75, fc=INK, lw=0, z_=3)
    t.circle(45, 0, 0.75, fc=INK, lw=0, z_=3)
    t.line([(-CR - 6, 0), (CR + 6, 0)], lw=THIN, ls=(0, (12, 3, 2, 3)), c="#555")
    t.note(0, 30, "ring grooves 1×1, r 15/30/45", 92, 70, ha="left")
    t.note(30, 17.3, "12 radial grooves 1×1,\nfloor falls 1° to centre", 92, 50, ha="left")
    t.note(-R, 0, "recess ⌀100.5 × 2.15", 92, 30, ha="left")
    t.note(45, 0, "purge bore r 45", 92, 10, ha="left")
    t.note(OR_R * 0.707, -OR_R * 0.707, "O-ring groove ⌀107×2", 92, -10, ha="left")
    t.note(25 * 0.707, -25 * 0.707, "variant B: lip seal r 25,\nsplit inner/outer outlet", 92, -34, ha="left")
    t.note(*polar(135, BOLT_R), "4× M5 at 45°/135°/225°/315°", 92, -58, ha="left")
    # detail of membrane clamp
    d = View(sh, 25 - 46 * 5 + 10, 72, 5.0, "DETAIL D – membrane clamp  5 : 1", (90, 102))
    x0, x1 = 46.0, 58.0
    d.rect(x0, -6, CR if CR < x1 else x1, 0, fc=METAL, hatch="////")
    d.rect(x0, Z_SUP, R + 0.25, 0, fc="white", lw=THIN)
    d.rect(x0, Z_SUP, R, -p.T_MEMBR, fc="#9aa3ab", lw=THIN, hatch="xxxx")
    d.rect(x0, -p.T_MEMBR, R_MEMBR, 0, fc="#e9d9a8", lw=THIN)
    d.rect(R, 0, RO, 5, fc="#dfeef5", hatch="\\\\\\\\")
    d.rect(RO, 0, x1, 5, fc="#dfeef5", hatch="\\\\\\\\")
    d.rect(x0, 0, R, 5, fc=FROZEN, lw=THIN)
    d.rect(OR_R - 1.2, -1.5, OR_R + 1.2, 0, fc="white", lw=THIN)
    d.circle(OR_R, -0.85, 1.0, fc="#333", lw=0)
    d.rect(45.5, Z_GROOVE, 46.0, Z_SUP, fc=WATER, lw=THIN)
    d.note(48, -1.2, "support plate t 2", 47, -10)
    d.note(51, -0.07, "membrane 20 µm, t 0.15", 56, -9)
    d.note(OR_R, -0.85, "O-ring 2 mm, groove 2.4 × 1.5", 59.5, -3)
    d.note(48, 3, "soil", 44.5, 3)
    d.note(53, 3, "tube end face clamps membrane edge", 59.5, 3.5)
    sh.text(255, 180, "Why a solid cone\n"
            "The external funnel keeps the drip point on the axis, but the inside is solid, so the\n"
            "drainage volume is grooves 1.1 mL + bore 0.1 mL (< 1 fraction) instead of the 120 cm³\n"
            "air space of a hollow funnel. The membrane lets the bottom be held at a set suction\n"
            "h_b = 0 … −30 cm (overflow cup height, E6-V06); h_b = 0 reproduces a seepage face.\n"
            "The Cu coil keeps the cone at −3 °C while freezing and at +0.3 °C during outflow.",
            fontsize=FS_SMALL, va="top", linespacing=1.5)
    sh.save(pdf, os.path.join(OUT, "E6-V04_cone_outlet.png"))


# ---------------------------------------------------------------------------
def sheet_v05(pdf):
    sh = Sheet("Disc–soil interface detail", "E6-V05", "2 : 1", 5, TOTAL,
               "AMDI disc (Kubát et al. 2025, github.com/kubatjanf/AMDI), low-profile head")
    v = View(sh, 150, 4, 2.0)
    zc = 88.0
    for s in (-1, 1):
        v.rect(s * R, zc, s * RO, p.L_TUBE, fc="#dfeef5", hatch="\\\\\\\\")
        v.rect(s * RO, zc, s * (RO + 8), p.L_TUBE + 2, fc=INSUL, lw=THIN, hatch="oo")
    v.rect(-R, zc, R, Z_TOP, fc=FROZEN, lw=THIN)
    soil_texture(v, -R, R, zc, Z_TOP, n=120)
    v.break_line(-R - 10, R + 10, zc)
    v.rect(-R_SAND, Z_TOP, R_SAND, Z_HEAD, fc="#e8d8a0", lw=THIN, hatch="....")
    v.rect(-R_HEAD, Z_HEAD, R_HEAD, Z_HEAD + H_HEAD, fc=PLASTIC, hatch="////")
    v.rect(-R_DISK, Z_HEAD, R_DISK, Z_HEAD + p.T_DISK, fc="#8d99a6", lw=THIN, hatch="xxxx")
    for s in (-1, 1):
        v.circle(s * (R_DISK + 1.8), Z_HEAD + p.T_DISK + 1.8, 1.8, fc="#333", lw=0)
    v.rect(-20, Z_HEAD + p.T_DISK, 20, Z_HEAD + 10, fc=WATER, lw=THIN)
    for xh in (-12, 12):
        v.rect(xh - 1, Z_HEAD + 10, xh + 1, Z_HEAD + H_HEAD, fc=WATER, lw=THIN)
        v.rect(xh - 3, Z_HEAD + H_HEAD, xh + 3, Z_HEAD + H_HEAD + 4, fc=METAL, lw=THIN)
    v.line([(-7, Z_HEAD + 0.3), (-7, Z_HEAD + 14)], lw=THICK, c="#444")
    v.circle(-7, Z_HEAD + 0.3, 0.6, fc=INK, lw=0)
    for s in (-1, 1):
        v.rect(s * R_RAFT_I, Z_TOP, s * R_RAFT_O, Z_TOP + H_RAFT, fc=INSUL, lw=THIN, hatch="oo")
        v.rect(s * R_RAFT_I, Z_TOP + H_RAFT - 2, s * R_RAFT_O, Z_TOP + H_RAFT, fc=PLASTIC, lw=THIN)
    v.rect(-41, Z_TOP, -31, Z_TOP + 0.6, fc=RED, lw=0)
    for d_, xx in ((2, 33), (6, 39)):
        v.line([(xx, Z_TOP + 10), (xx, dz(d_))], lw=THICK, c="#444")
        v.circle(xx, dz(d_), 0.5, fc=INK, lw=0)
    v.line([(38, Z_TOP + H_RAFT), (38, p.L_TUBE + 6)], lw=THICK)
    v.line([(0, Z_HEAD + H_HEAD + 4), (0, p.L_TUBE + 6)], lw=THICK)
    d = dz(10)
    v.line([(RO + 8, d), (p.TH_R, d)], lw=THICK, c="#444")
    v.circle(p.TH_R, d, 0.8, fc=INK, lw=0)
    v.axis_line([(0, zc - 2), (0, p.L_TUBE + 10)])

    v.dim_h(-R_DISK, R_DISK, Z_HEAD, Z_HEAD - 7, "⌀45 sintered disc, t 3")
    v.dim_h(-R_HEAD, R_HEAD, Z_HEAD + H_HEAD, Z_HEAD + H_HEAD + 8, "⌀56")
    v.dim_h(R_HEAD, R_RAFT_I, Z_TOP + H_RAFT, Z_TOP + H_RAFT + 4, "2")
    v.dim_h(R_RAFT_O, R, Z_TOP + 4, Z_TOP + H_RAFT + 4, "2")
    v.dim_h(-R_RAFT_O, -R_RAFT_I, Z_TOP + H_RAFT, Z_TOP + H_RAFT + 4, "18")
    v.dim_v(Z_TOP, Z_HEAD, R_SAND, R_SAND + 3, "2")
    v.dim_v(Z_TOP, p.L_TUBE, R, R + 3, "25")
    v.dim_v(dz(6), Z_TOP, 39, 44, "6")
    v.dim_v(dz(2), Z_TOP, 33, 30.5, "2")

    L, Rr = dict(ha="left"), dict(ha="left")
    v.note(-24, Z_TOP + 1, "contact sand 0.1–0.3 mm, t 2, ⌀48,\nplaced dry, pre-cooled to 0 °C", -60, 84, **L)
    v.note(-(R_DISK + 1.8), Z_HEAD + 4.8, "O-ring 45 × 3.6 (as AMDI)", -60, 78, **L)
    v.note(-7, Z_HEAD + 0.3, "thermistor at disc/sand contact (Tdisc)", -60, 74, **L)
    v.note(-36, Z_TOP + 0.3, "heat-flux sensor 10×10", -60, 70, **L)
    v.note(-40, Z_TOP + 14, "floating ring XPS + PETG frame", -60, 66, **L)
    v.note(-20, Z_HEAD + 6, "water chamber ⌀40", -60, 62, **L)
    v.note(-12, Z_HEAD + H_HEAD + 2, "supply port (from Mariotte bottle)", -60, 58, **L)
    v.note(12, Z_HEAD + H_HEAD + 2, "port to pressure sensor + air purge", 8, 84, **Rr)
    v.note(39, dz(6), "needle T6 (T2 at 135°)", 8, 80, **Rr)
    v.note(30, d, "wall thermistor T10, tip r 9", 8, 76, **Rr)
    v.note(0, p.L_TUBE + 3, "LVDT-0 on head", 8, 72, **Rr)
    v.note(38, p.L_TUBE + 3, "LVDT-1 on ring", 8, 68, **Rr)

    sh.text(255, 108, "Head changes against the AMDI repository\n"
            "• Keep the printed lower body, disc seat and O-ring; drop the on-board Mariotte tube.\n"
            "• Two top ports: supply from the external Mariotte bottle on a balance, and a port to\n"
            "  the differential pressure sensor that also serves as air purge.\n"
            "• Head mass full ≈ 60 g (≈ 0.4 kPa on the disc) instead of ≈ 300 g (≈ 2 kPa).\n"
            "• Gaps of 2 mm let head and ring float freely with frost heave / thaw settlement.\n"
            "• Supply water and head stay at +0.5 °C; log Tdisc to detect freezing in the sand.",
            fontsize=FS_SMALL, va="top", linespacing=1.5)
    sh.save(pdf, os.path.join(OUT, "E6-V05_disc_interface.png"))


# ---------------------------------------------------------------------------
def box(sh, x, y, w, h, label, fc="white", ec=INK, fs=FS_SMALL, lw=THIN, ls="-", va="center"):
    sh.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.5",
                                   fc=fc, ec=ec, lw=lw, ls=ls, zorder=2))
    if label:
        ty = y + h / 2 if va == "center" else y + h - 2
        sh.text(x + w / 2, ty, label, fontsize=fs, ha="center", va=va if va == "center" else "top",
                zorder=3)


def pipe(sh, pts, c=BLUE, lw=1.4, ls="-"):
    sh.ax.plot([q[0] for q in pts], [q[1] for q in pts], c=c, lw=lw, ls=ls, zorder=3,
               solid_capstyle="butt")


def valve(sh, x, y, name, vertical=False):
    s = 2.4
    if vertical:
        P = [(x - s, y - s), (x + s, y + s), (x + s, y - s), (x - s, y + s)]
    else:
        P = [(x - s, y - s), (x + s, y + s), (x - s, y + s), (x + s, y - s)]
    from matplotlib.patches import Polygon
    sh.ax.add_patch(Polygon(P, closed=True, fc="white", ec=INK, lw=THIN, zorder=4))
    sh.text(x + 3.5, y + 3, name, fontsize=FS_SMALL, zorder=5)


def sheet_v06(pdf):
    sh = Sheet("Hydraulic and thermal scheme", "E6-V06", "–", 6, TOTAL,
               "not to scale except the marked elevations")
    ax = sh.ax
    # chamber
    box(sh, 28, 58, 210, 222, "", fc="#f5f9fc", ec="#557", lw=THICK)
    sh.text(32, 275, "programmable freezing chamber  −8 … +5 °C", fontsize=FS, weight="bold", va="top")
    # Mariotte bottle on balance
    box(sh, 40, 150, 30, 70, "", fc="white")
    ax.add_patch(Rectangle((40, 150), 30, 48, fc=WATER, ec="none", zorder=2.5))
    box(sh, 34, 140, 42, 9, "balance 0.01 g", fc="#eee")
    pipe(sh, [(52, 225), (52, 152)], c=INK, lw=1.0)
    sh.text(54, 226, "air inlet tube", fontsize=FS_SMALL)
    sh.text(55, 205, "Mariotte bottle\n600 mL, labelled\nwater δ²H +200…+500 ‰\n+ Br⁻, jacket +0.5 °C",
            fontsize=FS_SMALL - 0.5, ha="center", va="center", zorder=4)
    pipe(sh, [(70, 156), (100, 156), (100, 170), (128, 170)])
    valve(sh, 88, 156, "V1")
    # column
    cx = 150
    box(sh, cx - 22, 120, 44, 40, "", fc=FROZEN)
    sh.text(cx, 140, "frozen sample\n⌀100 × 100", fontsize=FS_SMALL, ha="center", va="center", zorder=4)
    box(sh, cx - 10, 160, 20, 7, "disc", fc=PLASTIC)
    pipe(sh, [(128, 170), (cx - 4, 170), (cx - 4, 167)])
    pipe(sh, [(cx + 4, 167), (cx + 4, 176), (cx + 26, 176)])
    box(sh, cx + 26, 172, 14, 8, "PT")
    from matplotlib.patches import Polygon
    ax.add_patch(Polygon([(cx - 24, 120), (cx + 24, 120), (cx + 3, 98), (cx - 3, 98)], closed=True,
                         fc=METAL, ec=INK, lw=THIN, zorder=2))
    sh.text(cx, 110, "cone", fontsize=FS_SMALL, ha="center", zorder=4)
    # elevations
    ax.plot([30, 236], [160, 160], c=RED, lw=THIN, ls="--", zorder=2.6)
    sh.text(236, 161, "disc surface", fontsize=FS_SMALL, ha="right", va="bottom", color=RED)
    ax.plot([30, 236], [120, 120], c=RED, lw=THIN, ls="--", zorder=2.6)
    sh.text(236, 121, "membrane", fontsize=FS_SMALL, ha="right", va="bottom", color=RED)
    ax.plot([46, 66], [152, 152], c=RED, lw=THIN)
    ax.plot([46, 66], [160, 160], c=RED, lw=THIN)
    ax.annotate("", xy=(62, 152), xytext=(62, 160),
                arrowprops=dict(arrowstyle="<|-|>", lw=THIN, color=RED, mutation_scale=6))
    sh.text(34, 134, "h₀ = −2 cm: air-inlet tip 20 mm below disc surface", fontsize=FS_SMALL - 0.5, va="center", color=RED)
    # outflow
    pipe(sh, [(cx, 98), (cx, 88), (cx + 30, 88), (cx + 30, 80)])
    valve(sh, cx, 92, "V3", vertical=True)
    pipe(sh, [(cx + 30, 88), (cx + 30, 88)])
    sh.text(cx + 32, 95, "heated line +1 °C", fontsize=FS_SMALL - 0.5, color=BLUE)
    pipe(sh, [(cx - 24, 117), (cx - 36, 117)])
    valve(sh, cx - 40, 117, "V4")
    pipe(sh, [(cx - 44, 117), (cx - 52, 117)])
    sh.text(cx - 74, 117, "purge", fontsize=FS_SMALL, va="center")
    # collector box
    box(sh, 150, 62, 84, 30, "", fc="#eef3e9", ec="#4a7")
    sh.text(152, 90, "insulated box +4 °C", fontsize=FS_SMALL, va="top", color="#2a6a3a")
    ax.add_patch(Rectangle((cx + 26, 76), 8, 4, fc=WATER, ec=INK, lw=THIN, zorder=3))
    sh.text(cx + 36, 79, "overflow cup 0.5 mL\n(lip sets h_b)", fontsize=FS_SMALL - 0.5, va="center")
    for i in range(6):
        ax.add_patch(Rectangle((cx + 4 + i * 11, 64), 8, 9, fc="white", ec=INK, lw=THIN, zorder=3))
        ax.add_patch(Rectangle((cx + 4 + i * 11, 64), 8, 4, fc=WATER, ec="none", zorder=3.1))
    sh.text(cx + 70, 70, "fraction\ncollector,\nseptum vials", fontsize=FS_SMALL - 0.5, va="center")
    ax.annotate("", xy=(cx + 28, 120), xytext=(cx + 28, 80),
                arrowprops=dict(arrowstyle="<|-|>", lw=THIN, color=RED, mutation_scale=6))
    sh.text(cx + 27, 104, "h_b = 0 … −30 cm\n(adjustable)", fontsize=FS_SMALL - 0.5, ha="right",
            color=RED, va="center")
    # thermal
    box(sh, 22, 30, 60, 20, "circulating bath\n−5 … +5 °C, ±0.02 K", fc="#fbeee3")
    pipe(sh, [(70, 50), (70, 104), (cx - 16, 104)], c="#d08a4a", lw=1.4)
    pipe(sh, [(76, 50), (76, 100), (cx - 10, 100)], c="#d08a4a", lw=1.4, ls="--")
    sh.text(78, 60, "Cu coil on cone", fontsize=FS_SMALL, color="#a05a20")
    box(sh, 92, 30, 50, 20, "datalogger CR3000\n+ ratiometric front-end", fc="#f1eff7")
    box(sh, 150, 30, 60, 20, "OA-ICOS δ²H, δ¹⁸O\n+ EC, Br⁻ (IC)", fc="#eef3f8")
    sh.ax.annotate("", xy=(180, 50), xytext=(190, 62), arrowprops=dict(arrowstyle="-|>", lw=THIN))
    box(sh, 196, 188, 36, 22, "reference cell\npure water\n(0 °C plateau)", fc="white", fs=FS_SMALL - 0.5)
    box(sh, 196, 216, 36, 14, "air T, RH", fc="white", fs=FS_SMALL - 0.5)

    sh.heading(250, 276, "Valves and boundary conditions")
    rows = [["V1", "supply on/off", "closed until infiltration start"],
            ["V3", "outflow", "closed while freezing (stops cryosuction\nfrom the outlet line), opened at start"],
            ["V4", "air purge", "flush grooves before freezing"],
            ["top", "h₀ = −2 cm", "set by Mariotte air inlet; PT logs real h₀"],
            ["bottom", "h_b = 0…−30 cm", "set by overflow-cup lip; h_b = 0 →\nseepage face (original design)"],
            ["sides", "≈ adiabatic", "Kaiflex 30 mm; check with T10…T90"],
            ["cone", "T_b", "−3 °C freezing, +0.3 °C during outflow"]]
    table(sh, 250, 272, ["item", "setting", "note"], rows, [18, 36, 100], row_h=7.5)
    sh.text(250, 205, "Balances\n"
            "water:   in (balance) − out (fractions) = ΔS; ΔS checked by TDR (liquid)\n"
            "         + gravimetric sectioning at the end (total = liquid + ice)\n"
            "tracer:  δ²H label, Br⁻; δ¹⁸O left unlabelled → indicator of ice–water\n"
            "         fractionation and of pre-event water\n"
            "heat:    T profile + 2 heat-flux sensors + cone bath power",
            fontsize=FS_SMALL, va="top", family="DejaVu Sans Mono", linespacing=1.5)
    sh.save(pdf, os.path.join(OUT, "E6-V06_hydraulic_scheme.png"))


# ---------------------------------------------------------------------------
def sheet_v07(pdf):
    sh = Sheet("Run protocol – set-points", "E6-V07", "–", 7, TOTAL,
               "one run ≈ 7–9 days; times are indicative")
    ax = sh.fig.add_axes([0.08, 0.50, 0.84, 0.38])
    phases = [("pack + equilibrate", 0, 24), ("freeze top-down", 24, 54), ("freeze base", 54, 66),
              ("hold −3 °C", 66, 90), ("warm head", 90, 92), ("infiltration + outflow", 92, 200)]
    air = [(0, 4), (24, 4), (24.1, -5), (66, -5), (66.1, -3), (90, -3), (92, 0.5), (200, 0.5)]
    cone = [(0, 4), (24, 4), (24.1, 1), (54, 1), (66, -3), (92, -3), (92.1, 0.3), (200, 0.3)]
    for (name, a, b), fc in zip(phases, ["#f2f2f2", "#e3edf7", "#d3e3f2", "#c6d8ec", "#f7ecdc", "#e6f2e3"]):
        ax.axvspan(a, b, color=fc, lw=0)
        ax.text((a + b) / 2, 6.3, name, ha="center", va="bottom", fontsize=FS_SMALL, rotation=0 if b - a > 15 else 90)
    ax.plot(*zip(*air), c=BLUE, lw=1.6, label="chamber air")
    ax.plot(*zip(*cone), c="#d08a4a", lw=1.6, label="cone (bath)")
    ax.plot([0, 200], [0, 0], c="#888", lw=0.6, ls=":")
    ax.set_xlim(0, 200)
    ax.set_ylim(-6.5, 8.5)
    ax.set_xlabel("time [h]", fontsize=FS)
    ax.set_ylabel("set-point [°C]", fontsize=FS)
    ax.tick_params(labelsize=FS_SMALL)
    ax.legend(fontsize=FS_SMALL, loc="lower right", frameon=False)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    rows = [["1", "0–24 h", "pack in 10 mm lifts, wet to θ ≈ 0.30 with background water;\nflush grooves (V4), V3 closed", "T profile uniform ±0.05 K"],
            ["2", "24–54 h", "air −5 °C, cone +1 °C: freezing front moves down;\nV3 closed", "front at T90 depth"],
            ["3", "54–66 h", "cone ramp to −3 °C at 0.3 °C/h", "all T < −2.8 °C"],
            ["4", "66–90 h", "isothermal hold −3 °C; record heave (LVDT)", "drift < 0.02 K/h"],
            ["5", "90–92 h", "air to +0.5 °C; place dry, pre-cooled sand + head; fill supply", "Tdisc logged"],
            ["6", "92 h →", "open V1; cone +0.3 °C, open V3; collect 2–5 mL fractions;\nrun until ≥ 1.5 PV (≈ 350 mL) out", "δ²H plateau or 200 h"],
            ["7", "end", "close V1, V3; section in 10 mm slices: gravimetric θ, δ²H, Br⁻", "mass balance ±2 %"]]
    table(sh, 30, 128, ["step", "time", "action", "go / no-go"], rows, [12, 20, 130, 50], row_h=8.5)
    sh.save(pdf, os.path.join(OUT, "E6-V07_protocol.png"))


# ---------------------------------------------------------------------------
def shield(sh, x, y, name):
    """Air sensor in a small radiation shield (stacked plates)."""
    for k in range(3):
        sh.ax.add_patch(Rectangle((x - 4, y + k * 1.6), 8, 0.9, fc="white", ec=INK, lw=THIN, zorder=4))
    sh.ax.add_patch(Circle((x, y + 1.6), 0.9, fc=INK, ec="none", zorder=5))
    sh.text(x + 5.5, y + 1.6, name, fontsize=FS_SMALL, va="center", weight="bold")


def sheet_v08(pdf):
    sh = Sheet("Thermometry – chest freezer layout", "E6-V08", "–", 8, TOTAL,
               "temperature channels inside and outside the freezer; not to scale")
    ax = sh.ax
    # freezer body (walls hatched), collar, lid
    ax.add_patch(Rectangle((30, 62), 160, 150, fc=INSUL, ec=INK, lw=THICK, hatch="oo", zorder=1))
    ax.add_patch(Rectangle((38, 70), 144, 142, fc="#f5f9fc", ec=INK, lw=THIN, zorder=1.2))
    ax.add_patch(Rectangle((150, 70), 32, 34, fc=INSUL, ec=INK, lw=THIN, hatch="oo", zorder=1.3))
    sh.text(166, 96, "compressor\nstep", fontsize=FS_SMALL - 0.5, ha="center", va="center", zorder=2)
    ax.add_patch(Rectangle((30, 212), 160, 14, fc="#e8dcc2", ec=INK, lw=THICK, hatch="////", zorder=1))
    ax.add_patch(Rectangle((28, 226), 164, 9, fc="white", ec=INK, lw=THICK, zorder=1))
    sh.text(110, 230.5, "original lid (hinged on the collar)", fontsize=FS_SMALL, ha="center", va="center")
    for i, (gx, lab) in enumerate([(70, "G1"), (95, "G2"), (120, "G3"), (145, "G4")]):
        ax.add_patch(Circle((gx, 219), 2.4, fc="white", ec=INK, lw=THIN, zorder=3))
        sh.text(gx + 3.2, 221.5, lab, fontsize=FS_SMALL - 0.5)
    sh.text(32, 240, "collar: XPS 50 mm + plywood skin, between body and lid; cable glands G1–G4 in the collar",
            fontsize=FS_SMALL)
    # drain port
    ax.add_patch(Rectangle((38, 74), 4, 4, fc="white", ec=INK, lw=THIN, zorder=3))
    sh.text(26, 76, "drain\nport", fontsize=FS_SMALL - 0.5, ha="right", va="center")

    # column on stand
    cx = 105
    ax.add_patch(Rectangle((cx - 16, 128), 32, 46, fc=INSUL, ec=INK, lw=THIN, hatch="oo", zorder=2))
    ax.add_patch(Rectangle((cx - 9, 130), 18, 40, fc=FROZEN, ec=INK, lw=THIN, zorder=2.2))
    ax.add_patch(Rectangle((cx - 5, 170), 10, 5, fc=PLASTIC, ec=INK, lw=THIN, zorder=2.3))
    from matplotlib.patches import Polygon
    ax.add_patch(Polygon([(cx - 12, 128), (cx + 12, 128), (cx + 2, 114), (cx - 2, 114)], closed=True,
                         fc=METAL, ec=INK, lw=THIN, zorder=2))
    for xl in (cx - 14, cx + 14):
        ax.plot([xl, xl], [128, 70], c=INK, lw=THICK, zorder=1.5)
    ax.plot([cx - 16, cx + 16], [128, 128], c=INK, lw=THICK, zorder=2.4)
    sh.text(cx, 150, "column\n(E6-V01)", fontsize=FS_SMALL - 0.5, ha="center", va="center", zorder=3)
    for k, yy in enumerate((166, 160, 152, 144, 138, 133)):
        ax.add_patch(Circle((cx - 7.5 + (k % 2) * 15, yy), 0.9, fc=INK, ec="none", zorder=3))
    # Mariotte bottle
    ax.add_patch(Rectangle((48, 136), 18, 40, fc="white", ec=INK, lw=THIN, zorder=2))
    ax.add_patch(Rectangle((48, 136), 18, 26, fc=WATER, ec="none", zorder=2.1))
    ax.add_patch(Rectangle((45, 130), 24, 6, fc="#eee", ec=INK, lw=THIN, zorder=2))
    sh.text(57, 133, "balance", fontsize=FS_SMALL - 1, ha="center", va="center", zorder=3)
    ax.add_patch(Rectangle((45, 70), 24, 60, fc="none", ec="#888", lw=THIN, ls="--", zorder=1.4))
    sh.text(57, 100, "shelf", fontsize=FS_SMALL - 1, ha="center", va="center", color="#666")
    pipe(sh, [(66, 142), (80, 142), (80, 178), (cx - 2, 178), (cx - 2, 175)])
    ax.add_patch(Circle((57, 145), 0.9, fc=INK, ec="none", zorder=3))
    # outflow → collector inside
    pipe(sh, [(cx, 114), (cx, 108), (130, 108), (130, 100)])
    ax.add_patch(Rectangle((112, 72), 34, 20, fc="#eef3e9", ec="#4a7", lw=THIN, zorder=2))
    for i in range(5):
        ax.add_patch(Rectangle((114.5 + i * 6.2, 74), 4.5, 8, fc="white", ec=INK, lw=THIN, zorder=3))
    ax.add_patch(Rectangle((127, 96), 6, 4, fc=WATER, ec=INK, lw=THIN, zorder=3))
    sh.text(129, 89, "fraction collector", fontsize=FS_SMALL - 1, ha="center", zorder=4)
    ax.add_patch(Circle((cx + 1.5, 111), 0.9, fc=INK, ec="none", zorder=3))
    # reference cell, thermal mass, fan
    ax.add_patch(Rectangle((80, 72), 8, 14, fc=WATER, ec=INK, lw=THIN, zorder=2))
    ax.add_patch(Circle((84, 79), 0.9, fc=INK, ec="none", zorder=3))
    sh.text(84, 88, "Tcell", fontsize=FS_SMALL, ha="center", weight="bold")
    for i in range(3):
        ax.add_patch(Rectangle((153 + i * 9, 104), 7, 22, fc="#d9e7f3", ec=INK, lw=THIN, zorder=2))
    sh.text(166, 128, "water bottles\n(thermal mass)", fontsize=FS_SMALL - 1, ha="center", va="bottom")
    ax.add_patch(Circle((168, 196), 6, fc="white", ec=INK, lw=THIN, zorder=2))
    ax.plot([162, 174], [196, 196], c=INK, lw=THIN, zorder=3)
    ax.plot([168, 168], [190, 202], c=INK, lw=THIN, zorder=3)
    sh.text(168, 186, "fan 12 V\n(mixing)", fontsize=FS_SMALL - 1, ha="center", va="top")
    shield(sh, 140, 74 + 30, "A1")
    shield(sh, 135, 150, "A2")
    shield(sh, 140, 200, "A3")
    ax.add_patch(Rectangle((120, 202), 8, 5, fc="white", ec=INK, lw=THIN, zorder=3))
    sh.text(124, 209, "C", fontsize=FS_SMALL, ha="center", weight="bold")
    # cable bundles to glands
    ax.plot([cx + 16, cx + 22, 70, 70], [160, 205, 205, 216.6], c="#6a3d9a", lw=1.0, zorder=2.5)
    ax.plot([140, 140, 95, 95], [203, 208, 208, 216.6], c="#6a3d9a", lw=1.0, zorder=2.5)
    pipe(sh, [(cx + 4, 175), (cx + 4, 190), (120, 190), (120, 216.6)], c=BLUE, lw=1.0)
    ax.plot([168, 168, 145, 145], [202, 210, 210, 216.6], c="#555", lw=1.0, zorder=2.5)

    # outside: logger, controller, ice point, lab air
    box(sh, 200, 178, 44, 40, "", fc="#f1eff7")
    sh.text(222, 214, "logger box", fontsize=FS_SMALL, ha="center", weight="bold")
    sh.text(222, 196, "CR3000 (28 SE ch.)\nR_ref 30 kΩ 0.01 %\n2 ppm/K, on Al block\nLlog, Rchk",
            fontsize=FS_SMALL - 1, ha="center", va="center")
    ax.plot([70, 70, 200], [235 + 6, 246, 246], c="#6a3d9a", lw=1.0)
    ax.plot([95, 95], [216.6, 241], c="#6a3d9a", lw=1.0)
    ax.plot([70, 70], [221.4, 241], c="#6a3d9a", lw=1.0)
    ax.plot([200, 200], [246, 218], c="#6a3d9a", lw=1.0)
    sh.text(150, 248, "shielded PTFE cables, no connectors on the cold side", fontsize=FS_SMALL - 0.5,
            ha="center", color="#6a3d9a")
    box(sh, 200, 130, 44, 26, "", fc="#fbeee3")
    sh.text(222, 143, "controller C\nrelay → compressor\nset-point −3 / +0.5 °C\n(own Pt100, not logged)",
            fontsize=FS_SMALL - 1, ha="center", va="center")
    ax.plot([124, 124, 196, 196, 200], [207, 212, 212, 143, 143], c="#a05a20", lw=0.8, ls="--")
    box(sh, 200, 84, 44, 34, "", fc="white")
    ax.add_patch(Rectangle((210, 88), 24, 22, fc="#e8f1f8", ec=INK, lw=THIN, hatch="..", zorder=3))
    sh.text(222, 113, "ICE: ice-point Dewar", fontsize=FS_SMALL - 0.5, ha="center")
    sh.text(222, 99, "crushed ice +\npure water", fontsize=FS_SMALL - 1, ha="center", va="center", zorder=4)
    shield(sh, 212, 66, "L1")
    sh.text(212, 62, "lab air", fontsize=FS_SMALL - 1, ha="center", va="top")

    rows = [[c[0], c[1], c[2]] for c in tm.CHANNELS]
    sh.heading(252, 278, "Temperature channels")
    table(sh, 252, 274, ["ID", "location", "in/out"], rows, [16, 120, 16], row_h=4.3)
    sh.text(252, 180, "Rules\n"
            "• Never drill the freezer walls (refrigerant lines inside); use the collar.\n"
            "• One logger, one R_ref, one set of cables for calibration and runs.\n"
            "• Logger stays outside at room temperature; log Llog next to R_ref.\n"
            "• Excitation 0.5 V for ~50 ms per reading → self-heating ≈ 1.4 mK.\n"
            "• Check ICE (0.000 °C) before and after each run; drift > 3 mK → recalibrate.\n"
            "• Tcell shows the 0 °C freezing plateau of pure water during freezing:\n"
            "  an in-situ check of the whole chain at the most important temperature.\n"
            "• Fan + water bottles damp the compressor cycling (typ. ±2 K → < ±0.3 K\n"
            "  at A2); the column insulation damps it further.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E6-V08_thermometry_layout.png"))


def sheet_v09(pdf):
    sh = Sheet("Thermistor probe, circuit and calibration", "E6-V09", "2 : 1 / 1 : 1", 9, TOTAL,
               "probe ⌀1.6 = 1/16\" so it seals in a standard HPLC compression fitting")
    v = View(sh, 35, 240, 2.0, "PROBE P1 (wall probe, tip at r 9)  2 : 1", (115, 276))
    L = 60.0
    v.rect(0, -0.8, L, 0.8, fc="#d5d8dc", lw=THICK)
    v.rect(0.3, -0.5, 9, 0.5, fc="#b8a37a", lw=THIN)
    v.circle(1.6, 0, 0.45, fc=INK, lw=0)
    v.rect(9, -0.5, L, 0.5, fc="#efe6d2", lw=THIN, hatch="....")
    v.rect(L, -1.4, L + 8, 1.4, fc="#9aa3ab", lw=THIN)
    v.rect(L + 8, -0.9, L + 22, 0.9, fc="#6a3d9a", lw=THIN)
    v.dim_h(0, L, -0.8, -8, "60 (sheath AISI 316, ⌀1.6 × 0.2)", side="below")
    v.dim_h(0, 9, 0.8, 5, "9")
    v.note(1.6, 0, "NTC 10 kΩ glass bead ⌀0.8", 4, 14, ha="left")
    v.note(5, 0.3, "thermally conductive epoxy", 26, 14, ha="left")
    v.note(30, 0.3, "potting epoxy (low-T grade)", 48, 9, ha="left")
    v.note(L + 4, -1.4, "crimp sleeve + heat-shrink", L + 4, -12, ha="left")
    v.note(L + 18, 0.9, "PTFE 2 × 0.25 mm² + shield", L + 14, 7, ha="left")
    # installation sketch
    w = View(sh, 85, 168, 1.0, "INSTALLATION (section, 1 : 1)", (85, 200))
    w.rect(-5, -12, 0, 12, fc="#dfeef5", hatch="\\\\\\\\")
    w.rect(0, -6, 10, 6, fc="#dfeef5", lw=THIN)
    w.rect(10, -4, 20, 4, fc=METAL, lw=THIN)
    w.rect(-5 - 41, -12, -5, 12, fc=FROZEN, lw=THIN)
    w.line([(-5 - 41, 0), (20, 0)], lw=1.6, c="#444")
    w.line([(20, 0), (60, 0)], lw=1.0, c="#6a3d9a")
    w.rect(20, -12, 50, 12, fc=INSUL, lw=THIN, hatch="oo", z=1)
    w.circle(-46, 0, 1.2, fc=INK, lw=0)
    w.note(-2.5, 10, "PMMA wall 5, hole ⌀1.7", -30, 22, ha="left")
    w.note(5, 6, "PMMA boss 12×12×10 bonded, 1/4\"-28", 8, 18, ha="left")
    w.note(15, 4, "1/16\" fitting + PTFE ferrule", 30, 13, ha="left")
    w.note(-46, 0, "tip at r 9 (soil)", -46, -18, ha="left")
    w.note(35, -12, "Kaiflex 30", 52, -18)
    # circuit
    c = View(sh, 255, 214, 1.0, "HALF-BRIDGE (ratiometric)", (305, 276))
    c.line([(0, 40), (0, 30)], lw=1.0)
    c.text(0, 42, "Vx 0.5 V (switched)", fontsize=FS_SMALL, ha="center", va="bottom")
    c.rect(-4, 14, 4, 30, fc="white", lw=THIN)
    c.text(6, 22, f"R_ref {tm.R_REF / 1000:.0f} kΩ\n0.01 %, 2 ppm/K", fontsize=FS_SMALL, va="center")
    c.line([(0, 14), (0, 8), (40, 8)], lw=1.0)
    c.text(42, 8, "SE input → V", fontsize=FS_SMALL, va="center")
    c.rect(-4, -10, 4, 6, fc="#e6d3a3", lw=THIN)
    c.text(6, -2, "NTC (in freezer)\nX = V / Vx\nR_T = R_ref · X / (1 − X)", fontsize=FS_SMALL, va="center")
    c.line([(0, 8), (0, 6)], lw=1.0)
    c.line([(0, -10), (0, -16)], lw=1.0)
    c.line([(-5, -16), (5, -16)], lw=1.0)
    c.text(0, -19, "AG", fontsize=FS_SMALL, ha="center", va="top")
    c.text(-8, 0, "2 m cable:\nlead R ≈ 0.4 Ω\n≙ 0.3 mK", fontsize=FS_SMALL - 0.5, ha="right", va="center")
    # sensitivity + budget tables
    rows = []
    for T in (-8, -3, 0, 5, 20):
        rt, x, dx, pw, dt = tm.half_bridge(T)
        rows.append([f"{T}", f"{rt / 1000:.1f}", f"{x:.4f}", f"{abs(dx) * 0.01 * tm.V_EX * 1e6:.0f}", f"{dt * 1000:.1f}"])
    sh.heading(30, 128, "Bridge sensitivity")
    table(sh, 30, 124, ["T °C", "R_T kΩ", "X", "0.01 K ≙ µV", "self-heat mK"], rows, [16, 18, 18, 24, 24], row_h=4.4)
    u, U = tm.combined()
    brows = [[n, f"{x:.1f}"] for n, x in tm.BUDGET] + [["combined standard uncertainty u_c", f"{u:.1f}"],
                                                       ["expanded uncertainty U (k = 2)", f"{U:.1f}"]]
    sh.heading(140, 128, "Uncertainty budget (mK)")
    table(sh, 140, 124, ["component", "u"], brows, [92, 12], row_h=4.4)
    sh.heading(252, 166, "Calibration procedure")
    sh.text(252, 162,
            "1  Assemble probes with their final cables; connect to the run logger.\n"
            "2  Stirred bath (ethanol–water), reference SPRT/Pt100 with certificate.\n"
            "3  Points: −8, −5, −3, −2, −1, 0 (ice point), +1, +3, +5, +10, +20 °C;\n"
            "   ≥ 20 min per point, 10 readings averaged, probes within 20 mm of ref.\n"
            "4  Fit Steinhart–Hart per probe: 1/T = a + b ln R + c (ln R)³;\n"
            "   accept if all residuals < 2 mK.\n"
            "5  Ice-point check of every probe before and after each run.\n"
            "6  Recalibrate every 6 months or when ICE drift > 3 mK.\n"
            "7  Store coefficients with probe ID in the data repository.",
            fontsize=FS_SMALL, va="top", linespacing=1.5)
    sh.save(pdf, os.path.join(OUT, "E6-V09_thermistor_probe.png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith((".png", ".pdf")):
            os.remove(os.path.join(OUT, f))
    with PdfPages(os.path.join(OUT, "E6_drawings.pdf")) as pdf:
        for fn in (sheet_v01, sheet_v02, sheet_v03, sheet_v04, sheet_v05, sheet_v06, sheet_v07,
                   sheet_v08, sheet_v09):
            fn(pdf)
