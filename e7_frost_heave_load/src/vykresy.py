"""E7 drawings (A3, English). Run: python vykresy.py → ../vykresy/E7_drawings.pdf + PNG per sheet."""
import math
import os

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

import params as p
from drafting import (BLUE, FROZEN, FS, FS_SMALL, INK, INSUL, METAL, PLASTIC, RED,
                      THICK, THIN, WATER, Sheet, View, table)

OUT = os.path.join(os.path.dirname(__file__), "..", "vykresy")
TOTAL = 6
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


def frame(v, extend=None, z_beam=None, beam_h=None):
    extend = extend or X_COL + 20
    Z_BEAM = z_beam or p.FRAME_H
    BEAM_H = beam_h or 80.0
    hb = p.BASE_W / 2
    v.rect(-hb, -p.BASE_T, hb, 0, fc=METAL, hatch="////")
    for xf in (-hb + 20, hb - 20):
        v.rect(xf - 8, -p.BASE_T - 18, xf + 8, -p.BASE_T, fc=STEEL, lw=THIN)
    for s in (-1, 1):
        v.rect(s * (X_COL - COL_W / 2), 0, s * (X_COL + COL_W / 2), Z_BEAM, fc="#d9dde1", lw=THICK)
        v.line([(s * X_COL, 0), (s * X_COL, Z_BEAM)], lw=0.3, c="#888")
    v.rect(-extend, Z_BEAM, extend, Z_BEAM + BEAM_H, fc="#d9dde1", lw=THICK)
    for zz in (Z_BEAM + BEAM_H / 4, Z_BEAM + 3 * BEAM_H / 4):
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
    v.dim_h(-p.BASE_W / 2, p.BASE_W / 2, -p.BASE_T, -p.BASE_T - 60, f"{p.BASE_W:g}", side="below")
    v.dim_h(-X_COL, X_COL, Z_BEAM + BEAM_H, Z_BEAM + BEAM_H + 40, f"{p.COL_SPAN:g}")
    v.dim_v(0, Z_BEAM, -X_COL - 20, -X_COL - 60, f"{Z_BEAM:g}")
    v.dim_v(-p.BASE_T, Z_BEAM + BEAM_H, 150, 200, f"{Z_BEAM + BEAM_H + p.BASE_T:g}")
    s = View(sh, 175, 80, k, "SIDE VIEW  1 : 5", (175, 200))
    s.rect(-p.BASE_D / 2, -p.BASE_T, p.BASE_D / 2, 0, fc=METAL, hatch="////")
    s.rect(-40, 0, 40, Z_BEAM, fc="#d9dde1", lw=THICK)
    s.rect(-40, Z_BEAM, 40, Z_BEAM + BEAM_H, fc="#d9dde1", lw=THICK)
    s.rect(-R_INS, Z_S0, R_INS, TUBE_TOP, fc="none", lw=THIN, ls="--")
    s.dim_h(-p.BASE_D / 2, p.BASE_D / 2, -p.BASE_T, -p.BASE_T - 60, f"{p.BASE_D:g}", side="below")
    s.dim_h(-40, 40, Z_BEAM + BEAM_H, Z_BEAM + BEAM_H + 40, "80")
    rows = [["1", "base plate Al 6082 T6", f"{p.BASE_W:g} × {p.BASE_D:g} × 25", "1"],
            ["2", "profile 40×80 (B) / 40×40 (A) column", f"l = {p.FRAME_H:g} (B) / {p.FRAME_H_A:g} (A)", "2"],
            ["3", "profile 80×80 (cross-beam)", f"l = {p.COL_SPAN + 40:g}", "1"],
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
            "Stiffness at 15.7 kN (2 MPa): cross-beam 0.036 mm, columns 0.035 mm,\n"
            "load cell ≈ 0.05 mm, joints 0.02–0.15 mm. Joints dominate → core bolts\n"
            "into tapped profile ends, torque-controlled, no angle brackets; optionally\n"
            "2 steel tie rods M12 next to the cell.\n"
            "\n"
            f"Fit in the chest freezer: frame {p.BASE_W:g} × {p.BASE_D:g}, height "
            f"{p.FRAME_H + 80 + p.BASE_T:g} mm incl. base;\n"
            f"variant B; variant A uses a light 40×40 frame, columns {p.FRAME_H_A:g} mm\n"
            "(it only guides the weights);\n"
            "two rigs side by side on the tray – layout and heights on E7-V06.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V04_frame.png"))

# ---------------------------------------------------------------------------
# simplified schemes (variant A and B)
import sensors as sn

SENS = "#e8a33d"      # sensor colour
SENS_TXT = "#a05a00"
TCOL = "#c0392b"      # temperature points


def tag(v, x, z, tx, tz, text, color=INK, ha=None):
    a, b = v.p(x, z), v.p(tx, tz)
    v.ax.plot([a[0], b[0]], [a[1], b[1]], lw=THIN, c=color, zorder=7)
    v.ax.add_patch(Circle(a, 0.6, fc=color, ec="none", zorder=7))
    ha = ha or ("left" if b[0] >= a[0] else "right")
    v.ax.text(b[0] + (0.8 if ha == "left" else -0.8), b[1], text, fontsize=FS_SMALL, ha=ha, va="center",
              color=color, zorder=8, bbox=dict(fc="white", ec=color, lw=0.4, pad=0.6, boxstyle="round,pad=0.25"))


def simple_rig(v, variant):
    """Simplified elevation of one rig (A: dead-weight surcharge, B: restrained)."""
    zb = p.FRAME_H_A if variant == "A" else Z_BEAM
    frame(v, z_beam=zb, beam_h=p.BEAM_H_A if variant == "A" else None)
    sand = variant == "A"
    light = dict(lw=THIN)
    # bottom: spacer (A) or load cell (B)
    if variant == "B":
        v.rect(-30, 0, 30, H_BOT, fc=SENS, **light)
    else:
        v.rect(-30, 0, 30, H_BOT, fc=METAL, **light)
    v.rect(-75, Z_G10, 75, Z_PED, fc=G10, **light)
    v.rect(-75, Z_PED, 75, Z_S0, fc=METAL, **light)
    # cell, insulation, sample
    for s_ in (-1, 1):
        v.rect(s_ * R_OUT, Z_S0, s_ * R_INS, TUBE_TOP, fc=INSUL, lw=0.3)
        if sand:                     # multi-ring cell: base ring + 10 rings with PTFE washers
            v.rect(s_ * R_IN, Z_S0, s_ * R_OUT, Z_S0 + 8, fc=PETG, **light)
            for k in range(10):
                z0 = Z_S0 + 9 + 11 * k
                v.rect(s_ * R_IN, z0, s_ * R_OUT, z0 + 10, fc=PETG, lw=0.4)
        else:
            v.rect(s_ * R_IN, Z_S0, s_ * R_OUT, TUBE_TOP, fc=PETG, **light)
    v.rect(-p.D_SAMPLE / 2, Z_S0, p.D_SAMPLE / 2, Z_S1, fc="#e9dcb8" if sand else FROZEN, **light)
    v.rect(-49.75, Z_S0 - 4, 49.75, Z_S0, fc="#bfc5b0", lw=0.3)
    v.rect(-49.75, Z_S1, 49.75, Z_S1 + 4, fc="#bfc5b0", lw=0.3)
    if sand:
        pressure_cells(v, labels=False)
    else:
        v.text(0, (Z_S0 + Z_S1) / 2 + 12, "soil sample\n⌀100 × 100", fontsize=FS_SMALL, ha="center", va="center")
    v.rect(-49.75, Z_S1 + 4, 49.75, Z_PT, fc=METAL, **light)
    v.rect(-70, Z_PT, 70, Z_PT + TARGET_T, fc=METAL, **light)
    v.circle(0, Z_BALL + 6, 6, fc=STEEL, lw=THIN)
    z_lc = Z_BALL + 12
    # LVDTs on an Invar reference (dashed)
    if sand:      # variant A: LVDTs at ±y on tabs of the target plate (revolved, behind the weights)
        v.rect(-p.LVDT_R - 6, Z_PT, p.LVDT_R + 6, Z_PT + TARGET_T, fc=METAL, lw=0.3)
        for s_ in (-1, 1):
            v.rect(s_ * p.LVDT_R - 6, z_lc + 5, s_ * p.LVDT_R + 6, z_lc + 45, fc=SENS, lw=THIN, ls="--")
            v.line([(s_ * p.LVDT_R, z_lc + 5), (s_ * p.LVDT_R, Z_PT + TARGET_T)], lw=THICK)
            v.line([(s_ * (p.LVDT_R + 8), 0), (s_ * (p.LVDT_R + 8), z_lc + 50), (s_ * p.LVDT_R, z_lc + 50)],
                   lw=THIN, ls=(0, (4, 2)), c=INVAR)
    else:
        for s_ in (-1, 1):
            v.rect(s_ * 62 - 6, z_lc + 5, s_ * 62 + 6, z_lc + 45, fc=SENS, **light)
            v.line([(s_ * 62, z_lc + 5), (s_ * 62, Z_PT + TARGET_T)], lw=THICK)
        v.line([(-75, 0), (-75, z_lc + 50), (75, z_lc + 50), (75, 0)], lw=THIN, ls=(0, (4, 2)), c=INVAR)
    if variant == "A":
        zg = Z_BALL + 12
        v.rect(-p.DW_G10_D / 2, zg, p.DW_G10_D / 2, zg + p.DW_G10_T, fc=G10, **light)
        zc = zg + p.DW_G10_T
        v.rect(-p.DW_D / 2, zc, p.DW_D / 2, zc + p.DW_CARRIER_T, fc=STEEL, **light)
        z = zc + p.DW_CARRIER_T
        for t in (p.DW_FULL_T,) * 3 + (p.DW_HALF_T,):
            v.rect(-p.DW_D / 2, z, p.DW_D / 2, z + t, fc="#8a8f96", lw=THIN, hatch="////")
            z += t
        v.rect(-p.DW_D / 2 - 10, zc, p.DW_D / 2 + 10, z + 10, fc="none", lw=THIN, ls=(0, (3, 2)))
        v.rect(-p.DW_ROD_D / 2, zc + p.DW_CARRIER_T, p.DW_ROD_D / 2, zc + p.DW_CARRIER_T + p.DW_ROD_L,
               fc=STEEL, lw=THIN)
        v.rect(-14, zb, 14, zb + p.BEAM_H_A, fc="white", lw=THIN, hatch="xx")
        return z_lc, (zg, zc, z), zb
    v.rect(-28, z_lc, 28, z_lc + 40, fc=SENS, **light)
    v.rect(-18, z_lc + 40, 18, Z_BEAM, fc=METAL, **light)
    v.rect(-10, Z_BEAM - 15, 10, Z_BEAM + BEAM_H + 35, fc=STEEL, lw=THIN)
    v.rect(-45, Z_BEAM + BEAM_H + 35, 45, Z_BEAM + BEAM_H + 42, fc=STEEL, lw=THIN)
    return z_lc, None, None


PCOL = "#1f7a8c"     # pressure sensors


def pressure_cells(v, labels=True):
    """Embedded cells (revolved into the section plane) and wall sensors, variant A."""
    side = {"PV1": 0, "PH1": 1}
    for tag_, kind, d, r, ang in p.PCELLS:
        x = side[tag_] * r
        z = Z_S1 - d
        if kind == "v":
            v.rect(x - p.PCELL_D / 2, z - p.PCELL_T / 2, x + p.PCELL_D / 2, z + p.PCELL_T / 2, fc=PCOL, lw=THIN, z=4)
        else:
            v.rect(x - p.PCELL_T / 2, z - p.PCELL_D / 2, x + p.PCELL_T / 2, z + p.PCELL_D / 2, fc=PCOL, lw=THIN, z=4)
        if labels:
            v.text(x, z + (p.PCELL_D / 2 + 1 if kind == "h" else p.PCELL_T / 2 + 1), tag_, fontsize=FS_SMALL,
                   color=PCOL, ha="center", va="bottom", weight="bold", zorder=6)
    for tag_, rr, ang in p.PBASE:
        v.rect(-rr - 4, Z_S0 - 1.5, -rr + 4, Z_S0, fc=PCOL, lw=THIN, z=4)
        if labels:
            v.text(-rr, Z_S0 + 1.5, tag_, fontsize=FS_SMALL, color=PCOL, ha="center", va="bottom", weight="bold")
    for tag_, d, ang in p.PWALL:
        z = Z_S1 - d
        v.rect(-R_IN - 3, z - p.PWALL_D / 2, -R_IN + 0.5, z + p.PWALL_D / 2, fc=PCOL, lw=THIN, z=4)
        if labels:
            v.text(-R_IN - 5, z, tag_, fontsize=FS_SMALL, color=PCOL, ha="right", va="center", weight="bold")


def cell_detail(sh, ox, oy, k):
    """Enlarged section of the multi-ring cell with sand, pressure sensors and thermistors."""
    v = View(sh, ox, oy, k)
    v.rect(-R_IN - 1, Z_S0 - 12, R_IN + 1, Z_S0, fc=METAL, lw=THIN)
    for s_ in (-1, 1):
        v.rect(s_ * R_IN, Z_S0, s_ * R_OUT, Z_S0 + 8, fc=PETG, lw=THIN)
        for kk in range(10):
            z0 = Z_S0 + 9 + 11 * kk
            v.rect(s_ * R_IN, z0, s_ * R_OUT, z0 + 10, fc=PETG, lw=0.4)
        v.rect(s_ * (R_IN - 0.6), Z_S0, s_ * R_IN, Z_S1 + 18, fc="#d9a066", lw=0)
    v.rect(-p.D_SAMPLE / 2, Z_S0, p.D_SAMPLE / 2, Z_S1, fc="#e9dcb8", lw=THIN)
    import random
    rnd = random.Random(2)
    for _ in range(260):
        v.circle(rnd.uniform(-48, 48), rnd.uniform(Z_S0 + 1, Z_S1 - 1), 0.35, fc="#b39a6b", ec="none", lw=0, z_=2.1)
    v.rect(-49.75, Z_S1, 49.75, Z_S1 + 4, fc="#bfc5b0", lw=0.3)
    v.rect(-49.75, Z_S1 + 4, 49.75, Z_S1 + 18, fc=METAL, lw=THIN)
    v.text(0, Z_S1 + 11, "piston + surcharge σ = const", fontsize=FS_SMALL - 0.5, ha="center", va="center")
    for i, (d, ang) in enumerate(WALL_TH, 1):
        s_ = 1 if i % 2 else -1
        z = Z_S1 - d
        v.line([(s_ * R_OUT, z), (s_ * 9, z)], lw=0.7, c=TCOL)
        v.circle(s_ * 9, z, 1.2, fc=TCOL, lw=0)
        v.text(s_ * (R_OUT + 2), z, f"T{i}", fontsize=FS_SMALL - 0.5, color=TCOL, va="center",
               ha="left" if s_ > 0 else "right")
    pressure_cells(v, labels=True)
    v.dim_v(Z_S0, Z_S1, R_OUT, R_OUT + 14, "100")
    v.dim_h(-p.D_SAMPLE / 2, p.D_SAMPLE / 2, Z_S0 - 12, Z_S0 - 18, "⌀100 unsaturated sand", side="below")


def temp_points(v, variant, z_lc):
    pts = []
    for i, (d, ang) in enumerate(WALL_TH, 1):
        s_ = 1 if i % 2 else -1
        z = Z_S1 - d
        v.line([(s_ * R_INS, z), (s_ * 9, z)], lw=0.8, c=TCOL)
        v.circle(s_ * 9, z, 2.0, fc=TCOL, lw=0)
        v.text(s_ * (R_INS + 3), z, f"T{i}", fontsize=FS_SMALL, color=TCOL, va="center",
               ha="left" if s_ > 0 else "right", weight="bold")
    for name, x, z in (("Ttop", 30, Z_PT - 8), ("Tbot", 30, Z_PED + 15)):
        v.circle(x, z, 2.0, fc=TCOL, lw=0)
        v.text(x + 5, z, name, fontsize=FS_SMALL, color=TCOL, va="center", weight="bold")
    v.circle(-X_COL, 120, 2.0, fc=TCOL, lw=0)
    v.text(-X_COL - 26, 120, "Tframe", fontsize=FS_SMALL, color=TCOL, va="center", ha="right", weight="bold")
    v.circle(-X_COL - 60, 260, 2.0, fc=TCOL, lw=0)
    v.text(-X_COL - 60, 268, "Tair", fontsize=FS_SMALL, color=TCOL, ha="center", weight="bold")
    lcs = [] if variant == "A" else [("TLC-T", 30, z_lc + 20), ("TLC-B", 30, 20)]
    for name, x, z in lcs:
        v.circle(x, z, 2.0, fc=TCOL, lw=0)
        v.text(x + 5, z, name, fontsize=FS_SMALL - 0.5, color=TCOL, va="center", weight="bold")


def legend(sh, rows, y0=276):
    sh.heading(255, y0, "Sensors (tag → model → CR1000)")
    return table(sh, 255, y0 - 4, ["tag", "measures", "recommended model", "CR1000"], rows,
                 [27, 36, 50, 37], row_h=5.2)


def sheet_a_simple(pdf):
    sh = Sheet("Variant A – unsaturated sand, dead-weight surcharge ≤ 25 kPa", "E7-V01", "≈ 1 : 3", 1,
               TOTAL, "schematic; orange = displacement, blue = pressure, red = temperature; "
               "cells and LVDTs revolved into section")
    v = View(sh, 105, 68, 1 / 3)
    z_lc, (zg, zc, ztop), zb = simple_rig(v, "A")
    temp_points(v, "A", z_lc)
    v.circle(60, (zc + ztop) / 2, 2.0, fc=TCOL, lw=0)
    v.text(64, (zc + ztop) / 2, "Tw", fontsize=FS_SMALL, color=TCOL, va="center", weight="bold",
           bbox=dict(fc="white", ec="none", pad=0.3))
    tag(v, 0, (zc + ztop) / 2 + 15, 135, ztop + 25,
        f"steel discs ⌀{p.DW_D:g}: 3 × {p.DW_FULL_T:g} + 1 × {p.DW_HALF_T:g} mm\n"
        f"= 20 kg incl. piston → 25 kPa", INK)
    tag(v, -60, zc + 5, -150, zc + 40, "carrier plate ⌀150 + guide rod ⌀16", INK)
    tag(v, 0, zb + 20, 135, zb + 55, "linear ball bushing in light\ncross-bar 40×40 (guide only)", INK)
    tag(v, -20, zg + 5, -150, zg - 10, "G10 thermal break ⌀60×10", INK)
    tag(v, p.DW_D / 2 + 10, ztop - 20, 135, ztop - 45, "insulation wrap 10 (optional)", INK)
    tag(v, p.LVDT_R, z_lc + 25, 135, z_lc - 30, "LVDT-1, -2 at ±y (on target tabs)", SENS_TXT)
    tag(v, -(p.LVDT_R + 8), 60, -150, 200, "Invar reference", INVAR)
    tag(v, -R_IN - 4, Z_S0 + 50, -150, 160, "multi-ring cell PETG-CF\n+ greased latex membrane", INK)
    tag(v, -R_INS + 5, Z_S0 + 20, -150, 100, "insulation 18", INK)
    tag(v, -60, Z_G10 + 5, -150, 40, "G10 thermal break", INK)
    tag(v, 0, -12, 60, -45, f"light frame: Al 40×40, columns {p.FRAME_H_A:g}", INK)
    rows = [["PV1 / PH1", "vert. / radial stress", sn.PICK["PC"][1], sn.PICK["PC"][3]],
            ["PB1", "vertical stress at base", sn.PICK["PW"][1], sn.PICK["PW"][3]],
            ["PW1…PW3", "lateral stress on wall", sn.PICK["PW"][1], sn.PICK["PW"][3]],
            ["LVDT-1,2", "check: no movement", sn.PICK["LVDT"][1], sn.PICK["LVDT"][3]],
            ["T1…T5", "soil, r 9 mm", sn.PICK["T"][1], sn.PICK["T"][3]],
            ["Ttop, Tbot, Tw", "piston, pedestal, weights", sn.PICK["T"][1], "(same)"],
            ["Tframe, Tair", "frame, air", sn.PICK["TX"][1], sn.PICK["TX"][3]]]
    y = legend(sh, rows)
    A_ = math.pi * 2500
    disc = lambda t: math.pi / 4 * ((p.DW_D / 1000) ** 2 - (p.DW_HOLE / 1000) ** 2) * t / 1000 * p.RHO_STEEL
    m_fixed = (p.PISTON_ASSY_KG + math.pi / 4 * (p.DW_D / 1000) ** 2 * p.DW_CARRIER_T / 1000 * p.RHO_STEEL
               + math.pi / 4 * (p.DW_ROD_D / 1000) ** 2 * p.DW_ROD_L / 1000 * p.RHO_STEEL)
    mrows = []
    for s_ in p.SURCHARGES_KPA:
        m = s_ * A_ / 1000 / 9.81
        rest = m - m_fixed
        n_f = int(rest // disc(p.DW_FULL_T)); rest -= n_f * disc(p.DW_FULL_T)
        n_h = int(rest // disc(p.DW_HALF_T)); rest -= n_h * disc(p.DW_HALF_T)
        mrows.append([f"{s_}", f"{m:.1f}", f"{n_f}", f"{n_h}", f"{rest:.2f}"])
    y = table(sh, 255, y - 4, ["σ kPa", "total kg", "full discs", "half discs", "trim kg"], mrows,
              [22, 26, 26, 26, 26], row_h=4.6)
    sh.text(255, y - 3,
            "How it works\n"
            f"Gravity gives an exactly constant surcharge; fixed part ≈ {m_fixed:.1f} kg ≈ "
            f"{m_fixed * 9.81 / A_ * 1000:.1f} kPa (piston, carrier, rod).\n"
            "No load cell, no adjustment; the frame only guides the rod and carries the LVDTs.\n"
            "Weights lag the freezer air by ≈ 0.6 K at the 0.1 K/h ramp (vypocty.md §7).",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.text(330, 143, "DETAIL – sand, pressure sensors, thermistors  ≈ 1 : 1.6", fontsize=FS + 0.5,
            weight="bold", ha="center")
    cell_detail(sh, 330, 16, 0.62)
    sh.save(pdf, os.path.join(OUT, "E7-V01_variant_A_scheme.png"))


def sheet_b_simple(pdf):
    sh = Sheet("Variant B – constant height (simplified)", "E7-V02", "≈ 1 : 3", 2, TOTAL,
               "schematic, proportions to scale; sensors in orange (force, displacement) and red (temperature)")
    v = View(sh, 110, 68, 1 / 3)
    z_lc, _, _ = simple_rig(v, "B")
    temp_points(v, "B", z_lc)
    tag(v, 0, z_lc + 20, 140, z_lc + 50, "LC-T  load cell 20 kN (top)", SENS_TXT)
    tag(v, 0, 20, 140, -20, "LC-B  load cell 20 kN (base)", SENS_TXT)
    tag(v, 62, z_lc + 25, 140, z_lc + 10, "LVDT-1, -2  ±10 mm", SENS_TXT)
    tag(v, 0, Z_BEAM - 30, 140, Z_BEAM + 30, "Al spacer + screw M24×1.5\n(set height, then lock)", INK)
    tag(v, -75, 60, -150, 200, "Invar reference", INVAR)
    tag(v, -R_IN - 4, Z_S0 + 50, -150, 160, "cell PETG-CF + PTFE liner\n+ Al sleeve", INK)
    tag(v, -R_INS + 5, Z_S0 + 20, -150, 100, "insulation 25", INK)
    tag(v, -60, Z_G10 + 5, -150, 40, "G10 thermal break", INK)
    rows = [["LC-T", "heave force, top", sn.PICK["LC-T"][1], sn.PICK["LC-T"][3]],
            ["LC-B", "force at base", sn.PICK["LC-B"][1], sn.PICK["LC-B"][3]],
            ["LVDT-1,2", "residual movement", sn.PICK["LVDT"][1], sn.PICK["LVDT"][3]],
            ["T1…T5", "soil, r 9 mm", sn.PICK["T"][1], sn.PICK["T"][3]],
            ["Ttop, Tbot", "piston, pedestal", sn.PICK["T"][1], "(same)"],
            ["TLC-T/B, Tframe, Tair", "load cells, frame, air", sn.PICK["TX"][1], sn.PICK["TX"][3]]]
    y = legend(sh, rows)
    sh.text(255, y - 4,
            "How it works\n"
            "The screw holds the piston at constant height; the soil pushes against it\n"
            "while freezing. LC-T measures that force, LC-B the force arriving at the\n"
            "base – the difference is the friction on the cell wall. The LVDTs show how\n"
            "much the frame still gives (report the stiffness with the pressure).\n"
            "Run a blank test with an Al dummy to remove the effect of the frame\n"
            "shrinking in the cold (vypocty.md §3).",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V02_variant_B_scheme.png"))


def rig_plan(v, cx, cy, variant):
    hb, hd = p.BASE_W / 2, p.BASE_D / 2
    v.rect(cx - hb, cy - hd, cx + hb, cy + hd, fc=METAL, lw=THIN, z=2)
    for s_ in (-1, 1):
        v.rect(cx + s_ * X_COL - 20, cy - 40, cx + s_ * X_COL + 20, cy + 40, fc="#d9dde1", lw=THIN, z=2.1)
    v.circle(cx, cy, R_INS, fc=INSUL, lw=THIN, z_=2.2)
    v.circle(cx, cy, R_OUT, fc=PETG, lw=THIN, z_=2.3)
    v.circle(cx, cy, p.D_SAMPLE / 2, fc=FROZEN, lw=THIN, z_=2.4)
    v.text(cx, cy, variant, fontsize=FS + 2, weight="bold", ha="center", va="center", zorder=5)


def sheet_layout(pdf):
    sh = Sheet("Both rigs in the chest freezer + CR1000", "E7-V06", "1 : 5", 6, TOTAL,
               "same freezer as E6 (inside ≈ 900 × 550 × 650, to be measured); logger outside")
    k = 0.2
    v = View(sh, 35, 160, k)
    v.text(10, 530, "PLAN  1 : 5", fontsize=FS + 1, weight="bold", va="top")
    v.rect(0, 0, p.FRZ_L, p.FRZ_W, fc="#f5f9fc", lw=THICK, z=1)
    v.rect(50, 105, 50 + p.TRAY_L, 105 + p.TRAY_W, fc="#d6d9dc", lw=THIN, z=1.2)
    v.rect(620, 15, 885, 535, fc="none", lw=THIN, ls="--", z=1.3)
    v.text(752, 60, "floor step (if present)", fontsize=FS_SMALL - 1, ha="center")
    rig_plan(v, 185, 275, "B")
    rig_plan(v, 445, 275, "A")
    v.circle(560, 460, 9, fc="white", ec=TCOL, lw=THIN, z_=3)
    v.text(575, 460, "Tair", fontsize=FS_SMALL, color=TCOL, va="center")
    v.rect(0, p.FRZ_W, p.FRZ_L, p.FRZ_W + 30, fc="#f3e3e1", ec=RED, lw=THIN, z=1)
    for gx, lab in ((185, "G1"), (445, "G2"), (700, "G3")):
        v.circle(gx, p.FRZ_W + 15, 8, fc="white", ec=RED, lw=THIN, z_=3)
        v.text(gx + 12, p.FRZ_W + 15, lab, fontsize=FS_SMALL - 1, va="center", color=RED)
    v.dim_h(50, 50 + p.TRAY_L, 105, 70, f"tray ≈ {p.TRAY_L:g} × {p.TRAY_W:g}", side="below")
    v.dim_h(185 - p.BASE_W / 2, 185 + p.BASE_W / 2, 405, 470, f"{p.BASE_W:g}")
    # elevation
    e = View(sh, 35, 22, k)
    e.text(10, 640, "ELEVATION  1 : 5", fontsize=FS + 1, weight="bold", va="top")
    e.rect(0, 0, p.FRZ_L, p.FRZ_H, fc="#f5f9fc", lw=THICK, z=1)
    e.line([(0, p.FRZ_H), (p.FRZ_L, p.FRZ_H)], lw=THICK, c=RED, ls="--")
    e.text(p.FRZ_L - 5, p.FRZ_H - 8, "lid / collar", fontsize=FS_SMALL - 1, ha="right", va="top", color=RED)
    e.rect(25, 0, 610, 20, fc="#3a3a3a", lw=0, z=1.2)
    e.rect(50, 20, 580, 60, fc="none", lw=THIN, z=1.3)
    e.rect(620, 0, 885, 230, fc="none", lw=THIN, ls="--", z=1.2)
    zb = 60 + 18 + p.BASE_T
    for cx, var, hcol in ((185, "B", p.FRAME_H), (445, "A", p.FRAME_H_A)):
        e.rect(cx - p.BASE_W / 2, zb - p.BASE_T, cx + p.BASE_W / 2, zb, fc=METAL, lw=THIN, z=2)
        for s_ in (-1, 1):
            e.rect(cx + s_ * X_COL - 20, zb, cx + s_ * X_COL + 20, zb + hcol, fc="#d9dde1", lw=THIN, z=2)
        bh = p.BEAM_H_A if var == "A" else BEAM_H
        e.rect(cx - X_COL - 20, zb + hcol, cx + X_COL + 20, zb + hcol + bh, fc="#d9dde1", lw=THIN, z=2)
        if var == "B":
            e.rect(cx - 45, zb + hcol + bh + 35, cx + 45, zb + hcol + bh + 42, fc=STEEL, lw=THIN, z=3)
        else:
            e.rect(cx - p.DW_D / 2, zb + 257, cx + p.DW_D / 2, zb + 383, fc="#8a8f96", lw=THIN, z=3)
            e.rect(cx - 8, zb + 257, cx + 8, zb + 257 + p.DW_ROD_L, fc=STEEL, lw=THIN, z=3.1)
        e.rect(cx - R_INS, zb + Z_S0, cx + R_INS, zb + TUBE_TOP, fc=INSUL, lw=THIN, z=2.1)
        e.text(cx, zb + 120, var, fontsize=FS + 2, weight="bold", ha="center", va="center", zorder=5)
    top = max(zb + p.FRAME_H + BEAM_H + 42, zb + 257 + p.DW_ROD_L, zb + p.FRAME_H_A + p.BEAM_H_A)
    e.dim_v(0, top, 445 + 75, 640, f"{top:.0f}")
    e.dim_v(0, p.FRZ_H, p.FRZ_L, p.FRZ_L + 25, f"≈ {p.FRZ_H:g}")
    # logger box outside
    box_ = dict(boxstyle="round,pad=0,rounding_size=1.5")
    sh.ax.add_patch(FancyBboxPatch((222, 185), 26, 70, fc="#f1eff7", ec=INK, lw=THIN, zorder=2, **box_))
    sh.text(235, 250, "outside", fontsize=FS_SMALL - 1, ha="center", style="italic")
    sh.text(235, 238, "CR1000\n+ AM16/32B\n+ 12 V\nbattery /\nmains", fontsize=FS_SMALL - 1, ha="center", va="top")
    sh.ax.plot([35 + 185 * k, 35 + 185 * k, 222], [160 + (p.FRZ_W + 15) * k, 266, 266], c="#6a3d9a", lw=0.9)
    sh.ax.plot([35 + 445 * k, 35 + 445 * k], [160 + (p.FRZ_W + 15) * k, 266], c="#6a3d9a", lw=0.9)
    sh.ax.plot([235, 235], [266, 255], c="#6a3d9a", lw=0.9)
    sh.text(150, 278.5, "sensor cables through the collar glands (no connectors on the cold side)",
            fontsize=FS_SMALL - 1, color="#6a3d9a", ha="center", va="bottom")
    sh.heading(255, 278, "Fit check")
    rows = [["base plates 2 × 260 × 200", "520 × 200", "tray ≈ 530 × 340", "OK (tight)"],
            ["rig A (weights)", "20 kg steel discs ⌀150", "nothing outside frame", "OK"],
            ["highest point", f"{top:.0f} mm", "inside ≈ 650", "OK, measure"],
            ["logger", "outside, 0…+40 °C", "CR1000 −25…+50 °C", "keep warm & dry"]]
    table(sh, 255, 274, ["item", "size", "limit", "status"], rows, [48, 32, 38, 32], row_h=5.0)
    sh.text(255, 246,
            "Notes\n"
            "• Both rigs share the freezer program (Set A) and the CR1000; each rig has\n"
            "  its own Tair sensor at sample mid-height and its own load cell temperatures.\n"
            "• Both rigs are set from above with a screw and handwheel; the free end of\n"
            "  the freezer stays empty (room for the cable bundle or a third rig).\n"
            "• Run the blank test with Al dummies in both rigs before the first soil run.\n"
            "• Dimensions marked ≈ are estimates from the photos (E6) – please measure.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V06_freezer_layout.png"))


def sheet_sensors(pdf):
    sh = Sheet("Sensor selection and CR1000 wiring", "E7-V05", "–", 5, TOTAL,
               "both rigs on one CR1000 + AM16/32B; models from manufacturer data (see README §7)")
    sh.heading(28, 278, "Options per measurement (PICK = recommended)")
    rows = [list(o) for o in sn.OPTIONS]
    table(sh, 28, 274, ["sensor", "maker / model", "key specs", "verdict"], rows, [18, 58, 98, 34], row_h=4.4)
    sh.heading(240, 278, "CR1000 channel plan")
    y = table(sh, 240, 274, ["terminal", "connected to", "measurement"], [list(c) for c in sn.CHANNELS],
              [24, 40, 106], row_h=4.6)
    sh.text(240, y - 4,
            "Channel count (2 rigs): 3 load cells, 4 LVDTs, 6 pressure bridges, ≈ 24 thermistors.\n"
            "16 SE / 8 DIFF on the CR1000 → two AM16/32B: bridges (4×16), thermistors (2×32).\n"
            "\n"
            "Resolution with the CR1000 (13-bit ADC)\n"
            "• LC-T/B 1 mV/V: 2.5 mV FS → ≈ 2.6 N ≈ 0.3 kPa\n"
            "• LVDT ±5 V over ±10 mm: ≈ 1.3 µm (0.7 µm with reversal);\n"
            "  absolute linearity ±0.25 % FS ≈ ±50 µm → calibrate with a micrometer\n"
            "• 109SS: ±0.38 °C at 0 °C; ice-point offset check improves it\n"
            "\n"
            "Notes\n"
            "• CR1000 is discontinued (successor CR1000X / CR1000Xe, 24-bit); the\n"
            "  existing one is fine for these resolutions.\n"
            "• Logger outside the freezer (CR1000 −25…+50 °C).\n"
            "• No load cell found with compensation to −20/−30 °C as standard:\n"
            "  Interface SSM −15 °C, HBM −10 °C (op. −30 °C) – log TLC and\n"
            "  correct; Interface/Lorenz offer extended ranges on request.\n"
            "• 4WFBS modules are for quarter bridges – not needed here.\n"
            "• Pressure cells: calibrate in the same sand under dead weight (25–200 kPa)\n"
            "  at +10 and −10 °C; correct zero(T) with the neighbouring thermistor.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V05_sensors_CR1000.png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith((".png", ".pdf")):
            os.remove(os.path.join(OUT, f))
    with PdfPages(os.path.join(OUT, "E7_drawings.pdf")) as pdf:
        for fn in (sheet_a_simple, sheet_b_simple, sheet_cell, sheet_frame, sheet_sensors, sheet_layout):
            fn(pdf)
