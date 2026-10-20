"""E7 drawings (A3, English). Run: python vykresy.py → ../vykresy/E7_drawings.pdf + PNG per sheet."""
import math
import os

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

import params as p
from drafting import (BLUE, FROZEN, FS, FS_SMALL, INK, INSUL, METAL, PLASTIC, RED,
                      THICK, THIN, WATER, Sheet, View, table)

OUT = os.path.join(os.path.dirname(__file__), "..", "vykresy")
TOTAL = 5
PETG = "#cfd8dc"
G10 = "#c9d9a6"
INVAR = "#8e7cc3"
STEEL = "#9aa0a6"

# vertical stack (z = 0 is the top of the base plate)
H_BOT = 40.0                      # bottom load cell (B) or Al spacer (A)
G10_T = 10.0                      # insulating, stiff disc under the pedestal
Z_G10 = H_BOT
Z_PED = Z_G10 + G10_T
Z_S0 = Z_PED + p.PEDESTAL_H       # bottom of the sample
Z_S1 = Z_S0 + p.H_SAMPLE          # top of the sample
PISTON_H = 40.0
Z_PT = Z_S1 + PISTON_H            # top of the piston
TUBE_TOP = Z_S1 + 25.0
TARGET_T = 5.0
Z_BALL = Z_PT + TARGET_T
R_IN, R_OUT = p.D_CELL_IN / 2, p.D_CELL_OUT / 2
R_FOOT = p.CELL_FOOT_D / 2
INS = 25.0
R_INS = R_OUT + INS
BEAM_H = 80.0
Z_BEAM = p.FRAME_H
COL_W = 40.0
X_COL = p.COL_SPAN / 2
WALL_TH = [(10, 0), (30, 72), (50, 144), (70, 216), (90, 288)]   # depth below sample top, angle


def frame(v, extend=160.0):
    v.rect(-150, -p.BASE_T, 150, 0, fc=METAL, hatch="////")
    for xf in (-130, 130):
        v.rect(xf - 8, -p.BASE_T - 18, xf + 8, -p.BASE_T, fc=STEEL, lw=THIN)
    for s in (-1, 1):
        v.rect(s * (X_COL - COL_W / 2), 0, s * (X_COL + COL_W / 2), Z_BEAM, fc="#d9dde1", lw=THICK)
        v.line([(s * X_COL, 0), (s * X_COL, Z_BEAM)], lw=0.3, c="#888")
    v.rect(-extend, Z_BEAM, extend, Z_BEAM + BEAM_H, fc="#d9dde1", lw=THICK)
    for zz in (Z_BEAM + 20, Z_BEAM + 60):
        v.line([(-extend, zz), (extend, zz)], lw=0.3, c="#888")


def cell_stack(v, bottom_lc):
    if bottom_lc:
        v.rect(-30, 0, 30, H_BOT, fc="#f2d7a6", lw=THICK)
        v.text(0, H_BOT / 2, "LC-B", fontsize=FS_SMALL - 1, ha="center", va="center")
    else:
        v.rect(-30, 0, 30, H_BOT, fc=METAL, hatch="////")
    v.rect(-75, Z_G10, 75, Z_PED, fc=G10, lw=THIN, hatch="----")
    v.rect(-75, Z_PED, 75, Z_S0, fc=METAL, hatch="////")
    v.rect(-49.75, Z_S0 - p.POROUS_T, 49.75, Z_S0, fc="#bfc5b0", lw=THIN, hatch="....")
    # cell (PETG-CF) with foot, liner, bosses, insulation
    for s in (-1, 1):
        v.rect(s * R_IN, Z_S0, s * R_OUT, TUBE_TOP, fc=PETG, hatch="\\\\\\\\")
        v.rect(s * R_OUT, Z_S0, s * R_FOOT, Z_S0 + p.CELL_FOOT_T, fc=PETG, hatch="\\\\\\\\")
        v.rect(s * (R_IN - p.LINER), Z_S0, s * R_IN, TUBE_TOP, fc="white", lw=0.4)
        v.rect(s * R_OUT, Z_S0 + p.CELL_FOOT_T, s * R_INS, TUBE_TOP, fc=INSUL, lw=THIN, hatch="oo")
    v.rect(-p.D_SAMPLE / 2, Z_S0, p.D_SAMPLE / 2, Z_S1, fc=FROZEN, lw=THIN)
    import random
    rnd = random.Random(5)
    for _ in range(160):
        v.circle(rnd.uniform(-48, 48), rnd.uniform(Z_S0 + 2, Z_S1 - 2), rnd.uniform(0.4, 1.3),
                 fc="#b9a888", ec="none", lw=0, z_=2.1)
    # piston with porous stone, target plate, ball
    v.rect(-49.75, Z_S1, 49.75, Z_S1 + p.POROUS_T, fc="#bfc5b0", lw=THIN, hatch="....")
    v.rect(-49.75, Z_S1 + p.POROUS_T, 49.75, Z_PT, fc=METAL, hatch="////")
    v.rect(-70, Z_PT, 70, Z_PT + TARGET_T, fc=METAL, lw=THIN)
    v.circle(0, Z_BALL + 6, 6, fc=STEEL, lw=THIN)
    # thermistors through bosses (revolved)
    for d, ang in WALL_TH:
        s = 1 if math.cos(math.radians(ang)) >= 0 else -1
        z = Z_S1 - d
        v.rect(s * R_OUT, z - 5, s * (R_OUT + 6), z + 5, fc=PETG, lw=THIN)
        v.line([(s * R_INS, z), (s * 9, z)], lw=THICK, c=RED)
        v.circle(s * 9, z, 1.4, fc=RED, lw=0)
    v.line([(0, Z_PED + 5), (-60, Z_PED + 5)], lw=THICK, c=RED)
    v.line([(0, Z_PT - 5), (40, Z_PT - 5)], lw=THICK, c=RED)
    # LVDT on an Invar reference frame (behind the section plane)
    for s in (-1, 1):
        v.rect(s * 92 - 5, 0, s * 92 + 5, Z_BALL + 60, fc=INVAR, lw=THIN, ls="--", alpha=0.35)
        v.rect(s * 62 - 6, Z_BALL + 20, s * 62 + 6, Z_BALL + 60, fc="white", lw=THIN)
        v.line([(s * 62, Z_BALL + 20), (s * 62, Z_PT + TARGET_T)], lw=THICK)
    v.rect(-97, Z_BALL + 60, 97, Z_BALL + 68, fc=INVAR, lw=THIN, ls="--", alpha=0.35)


def parts_list(sh, items, y0=276):
    y = y0
    for i, it in enumerate(items, 1):
        sh.ax.add_patch(Circle((259, y), 2.2, fc="white", ec=INK, lw=THIN))
        sh.text(259, y, str(i), fontsize=FS_SMALL - 0.5, ha="center", va="center")
        sh.text(264, y, it, fontsize=FS_SMALL, va="center")
        y -= 5.6
    return y


COMMON_PARTS = [
    "base plate Al 6082, 300×250×25, 3 levelling feet",
    "columns 2× Al profile 40×80 (strong axis), h 420",
    "cross-beam Al profile 80×80, l 320, core-bolted",
    "G10/GFRP disc ⌀150×10 – thermal break, stiff",
    "pedestal Al ⌀150×30 with porous stone ⌀99.5×10",
    "cell PETG-CF ⌀117/101, foot ⌀150 (E7-V03), not bolted",
    "PTFE liner 0.5 mm + silicone grease (side friction)",
    "sample ⌀100 × 100",
    "piston Al ⌀99.5×40 (gap ≥ 0.3), porous stone below",
    "LVDT target plate Al ⌀140×5 on the piston",
    "steel ball ⌀12 in conical seats (no moment)",
    "insulation Kaiflex 25 around the cell",
    "thermistors ⌀1.6 in printed bosses, 5 depths",
    "2× LVDT ±10 mm on Invar reference frame (behind)",
]


def sheet_a(pdf):
    sh = Sheet("Variant A – constant load (lever, dead weight)", "E7-V01", "1 : 3", 1, TOTAL,
               "stress-controlled freeze–thaw test; heave and thaw settlement measured by LVDT")
    v = View(sh, 80, 52, 1 / 3)
    frame(v)
    cell_stack(v, bottom_lc=False)
    # S-beam load cell, loading rod, linear bushing
    z_lc = Z_BALL + 12
    v.rect(-20, z_lc, 20, z_lc + 60, fc="#f2d7a6", lw=THICK)
    v.text(0, z_lc + 30, "LC-A\n2 kN", fontsize=FS_SMALL - 1, ha="center", va="center")
    v.rect(-8, z_lc + 60, 8, Z_BEAM + BEAM_H + 30, fc=STEEL, lw=THIN)
    v.rect(-20, Z_BEAM, 20, Z_BEAM + BEAM_H, fc="white", lw=THIN, hatch="xx")
    # lever
    z_lev = Z_BEAM + BEAM_H + 30
    v.rect(-70, Z_BEAM + BEAM_H, -30, z_lev, fc=METAL, lw=THIN)
    v.circle(-50, z_lev + 7, 4, fc="white", lw=THIN)
    v.rect(-130, z_lev, 470, z_lev + 15, fc=METAL, lw=THICK)
    v.rect(-130, z_lev + 15, -95, z_lev + 45, fc=STEEL, lw=THIN, hatch="////")
    v.line([(450, z_lev), (450, 300)], lw=THICK)
    for k in range(4):
        v.rect(400, 300 - (k + 1) * 22, 500, 300 - k * 22 - 2, fc=STEEL, lw=THIN)
    v.dim_h(-50, 0, z_lev + 15, z_lev + 70, "50")
    v.dim_h(-50, 450, z_lev + 15, z_lev + 110, "500  (ratio 1 : 10)")
    v.text(450, 300 - 4 * 22 - 10, "dead weights\n2 / 4 / 8 / 16 kg\n= 25 / 50 / 100 / 200 kPa",
           fontsize=FS_SMALL - 0.5, ha="center", va="top")
    v.dim_v(0, Z_BEAM + BEAM_H, -150, -175, f"{Z_BEAM + BEAM_H:g}")
    v.dim_v(Z_S0, Z_S1, -R_INS, -R_INS - 25, "100")
    v.dim_h(-X_COL, X_COL, 0, -60, f"{p.COL_SPAN:g}", side="below")
    B = v.balloon
    for n, (x, z, tx, tz) in enumerate([
            (-100, -12, -150, -60), (-X_COL, 200, -190, 200), (-120, Z_BEAM + 40, -190, Z_BEAM + 40),
            (-60, Z_G10 + 5, -190, 20), (-60, Z_PED + 15, -190, 60), (-R_OUT + 2, 150, -190, 120),
            (-R_IN + 0.2, 165, -190, 160), (-20, 130, -190, 240), (-30, Z_S1 + 25, -190, 280),
            (-60, Z_PT + 2, -190, 320), (0, Z_BALL + 6, 40, 330), (-R_INS + 8, 110, -190, 80),
            (9, Z_S1 - 10, 60, 270), (62, Z_BALL + 40, 120, 360)], 1):
        B(x, z, n, tx, tz)
    B(0, z_lc + 30, 15, 60, 300)
    B(0, Z_BEAM + 40, 16, 60, Z_BEAM + 40 + 0)
    B(-50, z_lev + 7, 17, -100, z_lev + 90)
    B(300, z_lev + 8, 18, 300, z_lev + 60)
    B(450, 250, 19, 360, 200)
    B(-112, z_lev + 30, 20, -150, z_lev + 90)
    y = parts_list(sh, COMMON_PARTS + [
        "S-beam load cell 2 kN, C3, comp. −10…+40 °C, rod-ends",
        "loading rod ⌀16 in linear ball bushing (cross-beam)",
        "lever pivot: needle bearings / knife edge",
        "lever Al 30×15, 600 long, level ± 3°",
        "weight hanger + steel discs",
        "counterweight (lever self-weight balanced)",
    ])
    sh.text(255, y - 2,
            "Why a lever with dead weight: the load stays constant when the sample\n"
            "heaves or settles and when the temperature changes; no air or power in the\n"
            "freezer. Re-level the lever when heave exceeds ≈ 25 mm at the hanger\n"
            "(2.5 mm at the sample) – turnbuckle on the rod. LC-A logs the real load\n"
            "(pivot friction, lever angle). Alternative: rolling-diaphragm air cylinder\n"
            "with a precision regulator outside the freezer (dry air, closed loop on LC-A).",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V01_variant_A_constant_load.png"))


def sheet_b(pdf):
    sh = Sheet("Variant B – constant height (restrained heave)", "E7-V02", "1 : 3", 2, TOTAL,
               "frost-heave force measured at the top and the bottom; frame stiffness and temperature artefact")
    v = View(sh, 105, 52, 1 / 3)
    frame(v)
    cell_stack(v, bottom_lc=True)
    z_lc = Z_BALL + 12
    v.rect(-30, z_lc, 30, z_lc + 40, fc="#f2d7a6", lw=THICK)
    v.text(0, z_lc + 20, "LC-T 20 kN", fontsize=FS_SMALL - 1, ha="center", va="center")
    z_sp = z_lc + 40
    v.rect(-20, z_sp, 20, Z_BEAM - 40, fc=METAL, hatch="////")
    v.rect(-12, Z_BEAM - 40, 12, Z_BEAM + BEAM_H + 40, fc=STEEL, lw=THIN, hatch="||")
    v.rect(-25, Z_BEAM + BEAM_H, 25, Z_BEAM + BEAM_H + 15, fc=STEEL, lw=THIN)
    v.rect(-50, Z_BEAM + BEAM_H + 40, 50, Z_BEAM + BEAM_H + 48, fc=STEEL, lw=THIN)
    v.dim_v(0, Z_BEAM + BEAM_H, -150, -175, f"{Z_BEAM + BEAM_H:g}")
    v.dim_v(Z_S0, Z_S1, -R_INS, -R_INS - 25, "100")
    v.dim_h(-X_COL, X_COL, 0, -60, f"{p.COL_SPAN:g}", side="below")
    B = v.balloon
    for n, (x, z, tx, tz) in enumerate([
            (-100, -12, -190, -40), (-X_COL, 200, -190, 200), (-120, Z_BEAM + 40, -190, Z_BEAM + 40),
            (-60, Z_G10 + 5, -190, 20), (-60, Z_PED + 15, -190, 60), (-R_OUT + 2, 150, -190, 120),
            (-R_IN + 0.2, 165, -190, 160), (-20, 130, -190, 240), (-30, Z_S1 + 25, -190, 280),
            (-60, Z_PT + 2, -190, 320), (0, Z_BALL + 6, 60, 330), (-R_INS + 8, 110, -190, 80),
            (9, Z_S1 - 10, 160, 270), (62, Z_BALL + 40, 160, 360)], 1):
        B(x, z, n, tx, tz)
    B(0, z_lc + 20, 15, 160, 300)
    B(0, H_BOT / 2, 16, 160, 20)
    B(0, Z_BEAM - 80, 17, 160, Z_BEAM - 25)
    B(0, Z_BEAM - 20, 18, 160, Z_BEAM + 30)
    B(40, Z_BEAM + BEAM_H + 44, 19, 160, Z_BEAM + BEAM_H + 70)
    y = parts_list(sh, COMMON_PARTS + [
        "LC-T compression load cell 20 kN, canister, stiff",
        "LC-B same type under the stack → wall friction",
        "Al spacer tube ⌀40 – thermally matched load path",
        "fine-thread screw M24×1.5 + lock nut (set height)",
        "handwheel; lock after seating at 5 kPa",
    ])
    sh.text(255, y - 2,
            "Design load 2 MPa = 15.7 kN (silts reach 0.2–2 MPa when restrained).\n"
            "Constant height is approximate: frame + load cell yield ≈ 0.16–0.29 mm\n"
            "at 15.7 kN (54–98 kN/mm, vypocty.md §2). LVDTs record the real piston movement; report\n"
            "pressure together with the measured restraint stiffness.\n"
            "Temperature artefact: Al columns shrink 0.19 mm for 20 K; with a steel\n"
            "stack this alone would press ≈ 1.7 kN (≈ 220 kPa) into frozen soil.\n"
            "→ Al spacer (item 17) matches the columns, and a blank run with a dummy\n"
            "  specimen through the same program gives the correction curve.\n"
            "Wall friction = LC-T − LC-B (PTFE liner keeps it small).",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V02_variant_B_constant_height.png"))


def sheet_cell(pdf):
    sh = Sheet("Sample cell – PETG-CF, 3D printed", "E7-V03", "1 : 1", 3, TOTAL,
               "print upright; hoop direction = layer direction; foot rests on the pedestal, not bolted")
    v = View(sh, 118, 118, 1.0)
    h = TUBE_TOP - Z_S0
    for s in (-1, 1):
        v.rect(s * R_IN, 0, s * R_OUT, h, fc=PETG, hatch="\\\\\\\\")
        v.rect(s * R_OUT, 0, s * R_FOOT, p.CELL_FOOT_T, fc=PETG, hatch="\\\\\\\\")
        v.poly([(s * R_OUT, p.CELL_FOOT_T), (s * (R_OUT + 4), p.CELL_FOOT_T), (s * R_OUT, p.CELL_FOOT_T + 4)],
               fc=PETG, lw=THIN)
        v.rect(s * (R_IN - p.LINER), 0, s * R_IN, h, fc="white", lw=0.4)
    for d, ang in WALL_TH:
        s = 1 if math.cos(math.radians(ang)) >= 0 else -1
        z = p.H_SAMPLE - d
        v.rect(s * R_OUT, z - 6, s * (R_OUT + 8), z + 6, fc=PETG, lw=THIN)
        v.rect(s * R_IN, z - 0.85, s * (R_OUT + 8), z + 0.85, fc="white", lw=THIN)
        v.text(s * (R_OUT + 10), z, f"T{d} ({ang}°)", fontsize=FS_SMALL, va="center",
               ha="left" if s > 0 else "right")
    for s in (-1, 1):
        v.rect(s * R_OUT, p.CELL_FOOT_T + 4, s * (R_OUT + 5), h - 4, fc="none", ec=INK, lw=THIN, ls="--")
    v.note(R_OUT + 5, 40, "variant B: Al sleeve ⌀117/127, slotted\nfor the bosses, carries the hoop load", 85, 110, ha="left")
    v.axis_line([(0, -5), (0, h + 8)])
    v.dim_h(-R_IN, R_IN, h, h + 8, "⌀101 H9 (printed, then reamed)")
    v.dim_h(-R_OUT, R_OUT, h, h + 18, "⌀117")
    v.dim_h(-R_FOOT, R_FOOT, 0, -8, "⌀150 foot", side="below")
    v.dim_v(0, h, R_OUT, R_FOOT + 22, f"{h:g}")
    v.dim_v(0, p.CELL_FOOT_T, R_FOOT, R_FOOT + 6, f"{p.CELL_FOOT_T:g}")
    v.note(-R_IN + 0.25, 60, "PTFE film 0.5 mm, overlap seam\nat 180°, silicone grease", -93, 140, ha="left")
    v.note(R_OUT + 6, p.H_SAMPLE - 30, "boss 12×12×8, ⌀1.7 hole,\nheat-set insert 1/4\"-28", 85, 30, ha="left")
    v.note(-R_OUT - 2, p.CELL_FOOT_T + 2, "fillet R4 (no notch)", -93, -18, ha="left")
    f = View(sh, 150, 18, 0.5, "VIEW F – multi-ring cell (variant A)  1 : 2", (150, 76))
    zz = 0.0
    for i in range(9):
        for s_ in (-1, 1):
            f.rect(s_ * R_IN, zz, s_ * R_OUT, zz + 10, fc=PETG, hatch="\\\\\\\\")
            f.rect(s_ * R_IN, zz + 10, s_ * R_OUT, zz + 11, fc="white", lw=THIN)
        zz += 11
    for s_ in (-1, 1):
        f.rect(s_ * (R_IN - 0.6), 0, s_ * R_IN, zz, fc="#e0b080", lw=0.3)
    f.axis_line([(0, -4), (0, zz + 6)])
    f.note(-R_IN, 40, "greased latex\nmembrane", -150, 70, ha="left")
    f.note(R_OUT, 10.5, "PTFE washer 1 mm", 75, 0, ha="left")
    f.note(R_OUT, 60, "ring 10 mm PETG-CF", 75, 50, ha="left")
    sh.heading(255, 276, "Material check – PETG-CF")
    rows = [["hoop stress, A 200 kPa", "1.3 MPa", "> 30", "> 9"],
            ["hoop stress, B 1 MPa", "6.3 MPa", "6–9", "1.9–2.6"],
            ["hoop stress, B 2 MPa", "12.6 MPa", "3–4", "1.0–1.3"],
            ["hoop, B 2 MPa + Al sleeve 5 mm", "≈ 1 MPa*", "> 40", "> 12"],
            ["axial (Z), friction μ 0.5, 1 MPa", "5.8 MPa", "2.6–5", "< 1.6"],
            ["axial (Z), PTFE μ 0.05, 1 MPa", "0.6 MPa", "> 25", "> 7"]]
    table(sh, 255, 272, ["load case", "stress", "SF short", "SF long"], rows, [62, 22, 22, 22], row_h=4.6)
    sh.text(255, 234,
            "Assumed strength (data-sheet range, verify): XY 40–55 MPa, Z 15–30 MPa,\n"
            "E 3–6 GPa; long-term limit ≈ 30 % (creep, layer bond). Details: vypocty.md §4.\n"
            "\n"
            "Verdict: suitable for variant A; for B (design 2 MPa) only with the\n"
            "Al sleeve shown dashed (*it carries ≈ 90 % of the hoop load: 70 GPa×5 mm\n"
            "vs. ≈ 4 GPa×8 mm), the PETG-CF then acts as a liner.\n"
            "Conditions for both:\n"
            "• the wall is ≥ 8 mm and printed with concentric perimeters only\n"
            "  (100 % infill, no zig-zag), so the hoop stress runs along the filament;\n"
            "• friction is kept low (PTFE liner) and the cell is not clamped at the foot,\n"
            "  so friction pushes the wall instead of pulling the layers apart;\n"
            "• the inside is sealed (thin epoxy coat) so water cannot enter print voids\n"
            "  and split layers when it freezes;\n"
            "• there are no printed threads or sharp notches (CF lowers toughness at\n"
            "  −10 °C) – heat-set inserts and fillets instead.\n"
            "Variant A: a multi-ring cell (view F) is the literature standard against\n"
            "wall friction – printed rings 10 mm + PTFE washers + greased latex.\n"
            "\n"
            "Print settings (starting point)\n"
            "hardened nozzle 0.6 mm, layer 0.2 mm, 250–260 °C, bed 80 °C, slow outer\n"
            "walls, filament dried 4 h at 65 °C, enclosure, part cooling ≤ 30 %.\n"
            "\n"
            "Qualification before use\n"
            "1  ring burst test: printed ring 20 mm high, internal water pressure to\n"
            "   failure (target ≥ 3× design pressure);\n"
            "2  10 freeze–thaw cycles −10/+10 °C of water-saturated coupons, then\n"
            "   tensile test XY and Z vs. dry control;\n"
            "3  creep: ring under 1 MPa for 7 days at +10 °C, hoop strain gauge.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V03_cell_PETG-CF.png"))


def sheet_frame(pdf):
    sh = Sheet("Frame – aluminium profiles", "E7-V04", "1 : 5", 4, TOTAL,
               "one frame for both variants; core-bolted joints, no angle brackets in the load path")
    k = 0.2
    v = View(sh, 70, 80, k, "FRONT VIEW  1 : 5", (70, 200))
    frame(v)
    v.rect(-R_INS, Z_S0, R_INS, TUBE_TOP, fc="none", lw=THIN, ls="--")
    v.dim_h(-150, 150, -p.BASE_T, -p.BASE_T - 60, "300", side="below")
    v.dim_h(-X_COL, X_COL, Z_BEAM + BEAM_H, Z_BEAM + BEAM_H + 40, f"{p.COL_SPAN:g}")
    v.dim_v(0, Z_BEAM, -X_COL - 20, -X_COL - 60, f"{Z_BEAM:g}")
    v.dim_v(-p.BASE_T, Z_BEAM + BEAM_H, 150, 200, f"{Z_BEAM + BEAM_H + p.BASE_T:g}")
    s = View(sh, 175, 80, k, "SIDE VIEW  1 : 5", (175, 200))
    s.rect(-125, -p.BASE_T, 125, 0, fc=METAL, hatch="////")
    s.rect(-40, 0, 40, Z_BEAM, fc="#d9dde1", lw=THICK)
    s.rect(-40, Z_BEAM, 40, Z_BEAM + BEAM_H, fc="#d9dde1", lw=THICK)
    s.rect(-R_INS, Z_S0, R_INS, TUBE_TOP, fc="none", lw=THIN, ls="--")
    s.dim_h(-125, 125, -p.BASE_T, -p.BASE_T - 60, "250", side="below")
    s.dim_h(-40, 40, Z_BEAM + BEAM_H, Z_BEAM + BEAM_H + 40, "80")
    rows = [["1", "base plate Al 6082 T6", "300 × 250 × 25", "1"],
            ["2", "profile 40×80 (column)", "l = 420", "2"],
            ["3", "profile 80×80 (cross-beam)", "l = 320", "1"],
            ["4", "core bolt M12 into tapped profile end", "", "8"],
            ["5", "socket screw M10 base → column end", "", "4"],
            ["6", "levelling foot M12, steel", "", "3"],
            ["7", "Invar rod ⌀10 + Invar/Al bridge (LVDT)", "l = 300", "2 + 1"],
            ["8", "linear ball bushing ⌀16 (A) / nut M24×1.5 (B)", "in cross-beam", "1"],
            ["9", "end caps, T-slot covers", "", "–"]]
    sh.heading(255, 276, "Bill of materials")
    table(sh, 255, 272, ["#", "part", "size", "qty"], rows, [8, 80, 30, 12], row_h=4.6)
    sh.text(255, 222,
            "Profile values used in vypocty.md §2 are typical catalogue values\n"
            "(series 8): 40×80 A ≈ 1050 mm², 80×80 I ≈ 1.4·10⁶ mm⁴ – check against the\n"
            "chosen supplier.\n"
            "\n"
            "Stiffness at 15.7 kN (2 MPa): cross-beam 0.046 mm, columns 0.045 mm,\n"
            "load cell ≈ 0.05 mm, joints 0.02–0.15 mm. Joints dominate → core bolts\n"
            "into tapped profile ends, torque-controlled, no angle brackets; optionally\n"
            "2 steel tie rods M12 next to the cell.\n"
            "\n"
            "Fit in the chest freezer: frame 300 × 250, height 525 mm incl. base;\n"
            "variant A needs the lever (≈ 600 mm long, 120 mm above the beam) –\n"
            "check against the inside height (≈ 650 mm, to be measured).",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V04_frame.png"))


def sheet_meas(pdf):
    sh = Sheet("Instrumentation and freeze–thaw program", "E7-V05", "–", 5, TOTAL,
               "channels for both variants; program = existing controller 'Set A'")
    ax = sh.fig.add_axes([0.08, 0.62, 0.40, 0.26])
    t, T = [0, 24], [10, 10]
    for i in range(1, 9):
        t += [24 + 192 * i]
        T += [-10 if i % 2 else 10]
    ax.plot(t, T, c=BLUE, lw=1.2)
    ax.set_xlabel("time [h]", fontsize=FS)
    ax.set_ylabel("freezer set-point [°C]", fontsize=FS)
    ax.tick_params(labelsize=FS_SMALL)
    ax.axhline(0, c="#888", lw=0.5, ls=":")
    ax.set_title("controller program Set A (photo): 24 h +10 °C, then 192 h ramps −10 / +10 °C",
                 fontsize=FS_SMALL)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    rows = [["LC-A", "S-beam 2 kN, full bridge 6-wire", "A", "applied load"],
            ["LC-T", "compression 20 kN", "B", "heave force at the top"],
            ["LC-B", "compression 20 kN", "B", "force at the base → friction = T − B"],
            ["LVDT-1, -2", "±10 mm, cold-rated", "A, B", "heave / settlement, tilt"],
            ["T10…T90", "NTC ⌀1.6 in bosses, r 9", "A, B", "freezing front, profile"],
            ["Ttop, Tbot", "NTC in piston / pedestal", "A, B", "boundary temperatures"],
            ["TLC-T, TLC-B", "NTC taped on load cells", "A, B", "zero-drift correction"],
            ["Tframe", "NTC on column", "A, B", "frame contraction"],
            ["Tair", "NTC in shield", "A, B", "freezer air"],
            ["SG-1, -2 (opt.)", "hoop strain gauges on cell", "B", "lateral pressure (calibrated)"]]
    sh.heading(30, 130, "Channels")
    table(sh, 30, 126, ["ID", "sensor", "variant", "quantity"], rows, [26, 58, 16, 70], row_h=4.8)
    sh.text(255, 278,
            "Weighing load cells or force transducers?\n"
            "Use force transducers (axial tension/compression load cells), not\n"
            "platform/single-point weighing cells:\n"
            "• they take a centred axial force in series in the load path; weighing\n"
            "  cells are made for a platform with off-centre loads and bend;\n"
            "• compression canister / column cells are much stiffer (≈ 0.02–0.1 mm\n"
            "  at full scale) – essential for constant height (variant B);\n"
            "• S-beams give fine resolution at low loads (variant A, 2 kN) and take\n"
            "  rod-ends that keep moments out;\n"
            "• choose a temperature-compensated range covering −10 °C\n"
            "  (typ. −10…+40 °C), stainless, IP67; log the cell temperature;\n"
            "• load introduction through a steel ball in conical seats.\n"
            "A hand-held force gauge is not suitable for long logged tests.\n"
            "\n"
            "Readout: full bridge, 6-wire, ratiometric on the CR3000 (or a 24-bit\n"
            "bridge amplifier); 2.5 V excitation; zero before each run at +10 °C.\n"
            "\n"
            "Blank run (both variants)\n"
            "Run the full program with an Al dummy specimen ⌀100×100 instead of soil.\n"
            "The recorded force and displacement are the apparatus response to\n"
            "temperature alone (frame contraction, load-cell drift, LVDT drift) and are\n"
            "subtracted from the soil runs.\n"
            "\n"
            "Derived quantities\n"
            "heave s = mean(LVDT-1, -2) − blank;  heave ratio s / H;\n"
            "A: s(t) at constant σ; thaw settlement; B: σ_h = LC-T / A;\n"
            "friction = LC-T − LC-B; frost-front depth from T10…T90 (0 °C crossing).",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V05_instrumentation.png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith((".png", ".pdf")):
            os.remove(os.path.join(OUT, f))
    with PdfPages(os.path.join(OUT, "E7_drawings.pdf")) as pdf:
        for fn in (sheet_a, sheet_b, sheet_cell, sheet_frame, sheet_meas):
            fn(pdf)
