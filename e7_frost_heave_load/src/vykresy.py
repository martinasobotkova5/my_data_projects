"""E7 drawings (A3, English). Run: python vykresy.py → ../vykresy/E7_drawings.pdf + PNG per sheet."""
import math
import os

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

import params as p
from drafting import (BLUE, FROZEN, FS, FS_SMALL, INK, INSUL, METAL, PLASTIC, RED,
                      THICK, THIN, WATER, Sheet, View, table)

OUT = os.path.join(os.path.dirname(__file__), "..", "vykresy")
TOTAL = 8
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


def parts_list(sh, items, y0=276):
    y = y0
    for i, it in enumerate(items, 1):
        sh.ax.add_patch(Circle((259, y), 2.2, fc="white", ec=INK, lw=THIN))
        sh.text(259, y, str(i), fontsize=FS_SMALL - 0.5, ha="center", va="center")
        sh.text(264, y, it, fontsize=FS_SMALL, va="center")
        y -= 5.6
    return y


def sheet_cell(pdf):
    sh = Sheet("Sample cell – PETG-CF, solid 3D print (both variants)", "E7-V03", "1 : 1", 3, TOTAL,
               "print upright in one piece; hoop direction = layer direction; foot rests on the pedestal, not bolted")
    v = View(sh, 120, 112, 1.0)
    h = TUBE_TOP - Z_S0
    for s_ in (-1, 1):
        v.rect(s_ * R_IN, 0, s_ * R_OUT, h, fc=PETG, hatch="\\\\\\\\")
        v.rect(s_ * R_OUT, 0, s_ * R_FOOT, p.CELL_FOOT_T, fc=PETG, hatch="\\\\\\\\")
        v.poly([(s_ * R_OUT, p.CELL_FOOT_T), (s_ * (R_OUT + 4), p.CELL_FOOT_T), (s_ * R_OUT, p.CELL_FOOT_T + 4)],
               fc=PETG, lw=THIN)
        v.rect(s_ * (R_IN - p.LINER), 0, s_ * R_IN, h, fc="white", lw=0.4)
    # thermistor bosses (revolved into the section; true angles on view F)
    for d, ang in WALL_TH:
        s_ = 1 if math.cos(math.radians(ang)) >= 0 else -1
        z = p.H_SAMPLE - d
        v.rect(s_ * R_OUT, z - 5, s_ * (R_OUT + 8), z + 5, fc=PETG, lw=THIN)
        v.rect(s_ * R_IN, z - 0.85, s_ * (R_OUT + 8), z + 0.85, fc="white", lw=THIN)
        v.text(s_ * (R_OUT + 10), z, f"T  d{d} / {ang}°", fontsize=FS_SMALL - 0.5, va="center",
               ha="left" if s_ > 0 else "right", color=RED)
    # wall pressure-sensor holders PW1–3
    for tag_, d, ang in p.PWALL:
        s_ = 1 if math.cos(math.radians(ang)) >= 0 else -1
        z = p.H_SAMPLE - d
        v.rect(s_ * R_OUT, z - 6, s_ * (R_OUT + 8), z + 6, fc=PETG, lw=THIN)
        v.rect(s_ * (R_IN - p.LINER), z - p.PWALL_D / 2, s_ * (R_OUT + 8), z + p.PWALL_D / 2, fc=PCOL, lw=THIN)
        v.text(s_ * (R_OUT + 10), z, f"{tag_}  d{d:g} / {ang:g}°", fontsize=FS_SMALL - 0.5, va="center",
               ha="left" if s_ > 0 else "right", color=PCOL, weight="bold")
    v.axis_line([(0, -5), (0, h + 8)])
    v.dim_h(-R_IN, R_IN, h, h + 8, "⌀101 (printed, reamed) → ⌀100 with liner")
    v.dim_h(-R_OUT, R_OUT, h, h + 18, "⌀117")
    v.dim_h(-R_FOOT, R_FOOT, 0, -8, "⌀150 foot", side="below")
    v.dim_v(0, h, R_FOOT, R_FOOT + 10, f"{h:g}")
    v.dim_v(0, p.CELL_FOOT_T, R_FOOT, R_FOOT + 4, f"{p.CELL_FOOT_T:g}")
    v.dim_v(h - 25, h, -R_FOOT, -R_FOOT - 6, "25")
    v.note(-R_IN + 0.25, 72, "PTFE film 0.5 mm, butt seam at 180°,\nsilicone grease; cut-outs ⌀8 at PW1–3", -98, 140,
           ha="left")
    v.note(R_OUT + 8, 10, "boss 8×10, ⌀1.7 hole for 109SS\n(45° chamfer below)", 95, -10, ha="left")
    v.note(-R_OUT - 2, p.CELL_FOOT_T + 2, "fillet R4 (no notch)", -98, -7, ha="left")
    v.note(R_IN - 10, h - 12, "25 free height above the sample:\npiston (A) / top plate (B)", 95, 140, ha="left")
    f = View(sh, 205, 52, 0.42, "VIEW F – cell from above  1 : 2.4", (205, 94))
    f.circle(0, 0, R_FOOT, fc="#eef0f2", lw=THIN)
    f.circle(0, 0, R_OUT, fc=PETG, lw=THIN)
    f.circle(0, 0, R_IN, fc="white", lw=THIN)
    for d, ang in WALL_TH:
        c, s2 = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        f.line([(R_OUT * c, R_OUT * s2), ((R_OUT + 8) * c, (R_OUT + 8) * s2)], lw=2.6, c=PETG)
        f.line([(p.T_TIP_R * c, p.T_TIP_R * s2), ((R_OUT + 16) * c, (R_OUT + 16) * s2)], lw=0.7, c=RED)
    for tag_, d, ang in p.PWALL:
        c, s2 = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        f.circle((R_OUT + 3) * c, (R_OUT + 3) * s2, 5, fc=PCOL, lw=THIN)
    c, s2 = math.cos(math.radians(p.M_ANG)), math.sin(math.radians(p.M_ANG))
    f.line([(R_OUT * c, R_OUT * s2), ((R_OUT + p.M_BOSS[2]) * c, (R_OUT + p.M_BOSS[2]) * s2)], lw=8, c=TDRC)
    f.text((R_OUT + 20) * c, (R_OUT + 20) * s2, "M", fontsize=FS_SMALL, color="#d33682", ha="center",
           va="center", weight="bold")
    sh.text(85, 88, f"DETAIL M – sensor port, plan at depth {p.M_DEPTH:g} mm (angle {p.M_ANG:g}°)  1 : 1",
            fontsize=FS + 0.5, weight="bold", ha="center")
    m_plan(View(sh, 35, 58, 1.0))
    sh.text(205, 20, "red = thermistors T1–T5 at 0/72/144/216/288°, tip r 40;\nblue = PW1–3 at 30/150/270°; green = point M at 108°",
            fontsize=FS_SMALL - 0.5, ha="center", va="top")
    sh.heading(255, 276, "Material check – PETG-CF")
    rows = [["hoop: A 25 kPa surcharge, K0 = 1", "0.16 MPa", "> 250", "> 75"],
            ["hoop: B ice on the wall 200 kPa (upper est.)", "1.3 MPa", "32–44", "9–13"],
            ["hoop: extreme 1 MPa", "6.3 MPa", "6–9", "1.9–2.6"],
            ["axial (across layers): friction, A 25 kPa", "< 0.05 MPa", "> 300", "> 90"]]
    table(sh, 255, 272, ["load case", "stress", "SF short", "SF long"], rows, [66, 22, 20, 20], row_h=4.6)
    sh.text(255, 246,
            "Assumed strength (data-sheet range, verify): XY 40–55 MPa, Z 15–30 MPa,\n"
            "E 3–6 GPa; long-term limit ≈ 30 % (creep, layer bond). Details: vypocty.md §5.\n"
            "\n"
            "Verdict: suitable for both variants as a solid print (no sleeve needed).\n"
            "\n"
            "Wall friction (the price of a solid cell, vypocty.md §5)\n"
            "• A: friction carries part of the surcharge into the wall; with the PTFE liner\n"
            "  + grease (μ ≈ 0.05) the vertical stress at the base is ≈ 90 % of the top,\n"
            "  without the liner (μ ≈ 0.5) only ≈ 30–45 % → compare PV1 / PB1 with it.\n"
            "• B: friction and ice adhesion hold back heave of the frozen top layer;\n"
            "  PTFE has very low ice adhesion – liner and grease are mandatory.\n"
            "\n"
            "Conditions\n"
            "• wall 8 mm, concentric perimeters only, 100 % infill;\n"
            "• no printed threads or sharp notches (CF lowers toughness at −10 °C);\n"
            "• inside sealed with a thin epoxy coat before the liner goes in;\n"
            "• cell not clamped at the foot – friction then pushes, never pulls layers.\n"
            "\n"
            "Print settings (starting point)\n"
            "hardened nozzle 0.6 mm, layer 0.2 mm, 250–260 °C, bed 80 °C, slow outer\n"
            "walls, filament dried 4 h at 65 °C, enclosure, part cooling ≤ 30 %.\n"
            "Print upright, bosses with 45° chamfer underneath (no supports).\n"
            "\n"
            "Qualification before use\n"
            "1  10 freeze–thaw cycles −10/+10 °C of water-saturated coupons, then\n"
            "   tensile test XY and Z vs. dry control;\n"
            "2  bore check ⌀101 ± 0.1 at 3 heights, at +20 and −10 °C.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V03_cell_PETG-CF.png"))


def sheet_frame(pdf):
    sh = Sheet("Frame A (aluminium profiles) and Invar stand B", "E7-V04", "1 : 4", 4, TOTAL,
               "frame A only guides the weights; stand B is only a displacement reference – neither carries load")
    k = 0.25
    zb = p.FRAME_H_A
    v = View(sh, 80, 70, k, "A – FRONT VIEW  1 : 4", (80, 210))
    frame(v, z_beam=zb, beam_h=p.BEAM_H_A)
    v.rect(-R_INS, Z_S0, R_INS, TUBE_TOP, fc="none", lw=THIN, ls="--")
    v.rect(-p.DW_D / 2, Z_BALL + 22, p.DW_D / 2, Z_BALL + 158, fc="none", lw=THIN, ls="--")
    v.dim_h(-p.BASE_W / 2, p.BASE_W / 2, -p.BASE_T, -p.BASE_T - 60, f"{p.BASE_W:g}", side="below")
    v.dim_h(-X_COL, X_COL, zb + p.BEAM_H_A, zb + p.BEAM_H_A + 40, f"{p.COL_SPAN:g}")
    v.dim_v(0, zb, -X_COL - 20, -X_COL - 60, f"{zb:g}")
    v.dim_v(-p.BASE_T, zb + p.BEAM_H_A, 150, 200, f"{zb + p.BEAM_H_A + p.BASE_T:g}")
    b = View(sh, 190, 70, k, "B – FRONT VIEW  1 : 4", (190, 210))
    hb = p.BASE_W / 2
    b.rect(-hb, -p.BASE_T, hb, 0, fc=METAL, hatch="////")
    for xf in (-hb + 20, hb - 20):
        b.rect(xf - 8, -p.BASE_T - 18, xf + 8, -p.BASE_T, fc=STEEL, lw=THIN)
    for x in (-p.STAND_R, p.STAND_R * math.cos(math.radians(60))):
        b.rect(x - 6, 0, x + 6, p.Z_BRIDGE, fc=INVAR, lw=THIN, alpha=0.8)
    b.rect(-p.BRIDGE_D / 2, p.Z_BRIDGE, p.BRIDGE_D / 2, p.Z_BRIDGE + p.BRIDGE_T, fc=METAL, lw=THIN, hatch="////")
    b.rect(-R_INS, Z_S0, R_INS, TUBE_TOP, fc="none", lw=THIN, ls="--")
    for x in (-42, -22, 6, 22, 42):
        b.rect(x - 5, Z_BODY0, x + 5, Z_BODY0 + BODY_L, fc=SENS, lw=THIN)
    b.dim_h(-p.BASE_W / 2, p.BASE_W / 2, -p.BASE_T, -p.BASE_T - 60, f"{p.BASE_W:g}", side="below")
    b.dim_v(0, p.Z_BRIDGE, -hb, -hb - 40, f"{p.Z_BRIDGE:g}")
    b.dim_v(-p.BASE_T, Z_BODY0 + BODY_L, 150, 200, f"{Z_BODY0 + BODY_L + p.BASE_T:g}")
    b.dim_h(-p.BRIDGE_D / 2, p.BRIDGE_D / 2, p.Z_BRIDGE + p.BRIDGE_T, Z_BODY0 + BODY_L + 30, f"⌀{p.BRIDGE_D:g}")
    rows = [["1", "base plate Al 6082 T6 (A and B)", f"{p.BASE_W:g} × {p.BASE_D:g} × 25", "2"],
            ["2", "A: profile 40×40 column", f"l = {p.FRAME_H_A:g}", "2"],
            ["3", "A: profile 40×40 cross-bar", f"l = {p.COL_SPAN + 40:g}", "1"],
            ["4", "A: linear ball bushing ⌀16 in cross-bar", "", "1"],
            ["5", "A: Invar post ⌀10 + clamp arm (LVDT)", f"l ≈ 300", "2"],
            ["6", f"B: Invar post ⌀{p.STAND_POST_D:g}, M6 both ends", f"l = {p.Z_BRIDGE:g}", "3"],
            ["7", f"B: Al bridge ⌀{p.BRIDGE_D:g}×{p.BRIDGE_T:g}, 6 LVDT clamps", "", "1"],
            ["8", "core bolt M8 / socket screw M8", "", "8"],
            ["9", "levelling foot M12, steel", "", "6"]]
    sh.heading(255, 276, "Bill of materials")
    table(sh, 255, 272, ["#", "part", "size", "qty"], rows, [8, 80, 30, 12], row_h=4.6)
    sh.text(255, 222,
            "Frame A: carries nothing except the guide of the weight rod (bushing)\n"
            "and the LVDT posts; the surcharge goes straight down through the sample.\n"
            "\n"
            "Stand B: three Invar posts screwed into the base plate at r 100\n"
            "(60/180/300°, outside the insulation), bridge on top with split clamps\n"
            "for 5 LVDTs (+1 spare). The bridge is lifted off to fill the cell.\n"
            "Reference error of the stand ≈ 50 µm per 20 K (Al pedestal vs. Invar)\n"
            "→ blank run with an Al dummy sample (vypocty.md §4).\n"
            "\n"
            f"Heights incl. base plate: A {zb + p.BEAM_H_A + p.BASE_T:g} mm (+ guide rod), "
            f"B {Z_BODY0 + BODY_L + p.BASE_T:g} mm;\n"
            "two rigs side by side on the tray – layout on E7-V06.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V04_frame.png"))

# ---------------------------------------------------------------------------
# simplified schemes (variant A and B)
import sensors as sn

SENS = "#e8a33d"      # sensor colour
SENS_TXT = "#a05a00"
TCOL = "#c0392b"      # temperature points


def solid_cell(v, top=TUBE_TOP, foot=True):
    """Solid 3D-printed PETG-CF cell with foot and PTFE liner (both variants)."""
    for s_ in (-1, 1):
        v.rect(s_ * R_IN, Z_S0, s_ * R_OUT, top, fc=PETG, lw=THIN, hatch="\\\\\\\\")
        if foot:
            v.rect(s_ * R_OUT, Z_S0, s_ * R_FOOT, Z_S0 + p.CELL_FOOT_T, fc=PETG, lw=THIN, hatch="\\\\\\\\")
        v.rect(s_ * (R_IN - p.LINER), Z_S0, s_ * R_IN, top, fc="#f7f7f7", lw=0.3)


def tag(v, x, z, tx, tz, text, color=INK, ha=None):
    a, b = v.p(x, z), v.p(tx, tz)
    v.ax.plot([a[0], b[0]], [a[1], b[1]], lw=THIN, c=color, zorder=7)
    v.ax.add_patch(Circle(a, 0.6, fc=color, ec="none", zorder=7))
    ha = ha or ("left" if b[0] >= a[0] else "right")
    v.ax.text(b[0] + (0.8 if ha == "left" else -0.8), b[1], text, fontsize=FS_SMALL, ha=ha, va="center",
              color=color, zorder=8, bbox=dict(fc="white", ec=color, lw=0.4, pad=0.6, boxstyle="round,pad=0.25"))


def simple_rig(v, variant):
    """Simplified elevation of rig A (dead-weight surcharge); rig B is drawn by rig_b()."""
    zb = p.FRAME_H_A
    frame(v, z_beam=zb, beam_h=p.BEAM_H_A)
    sand = True
    light = dict(lw=THIN)
    v.rect(-30, 0, 30, H_BOT, fc=METAL, **light)
    v.rect(-75, Z_G10, 75, Z_PED, fc=G10, **light)
    v.rect(-75, Z_PED, 75, Z_S0, fc=METAL, **light)
    # cell, insulation, sample
    for s_ in (-1, 1):
        v.rect(s_ * R_OUT, Z_S0 + p.CELL_FOOT_T, s_ * R_INS, TUBE_TOP, fc=INSUL, lw=0.3)
    solid_cell(v)
    v.rect(-p.D_SAMPLE / 2, Z_S0, p.D_SAMPLE / 2, Z_S1, fc="#e9dcb8" if sand else FROZEN, **light)
    v.rect(-49.75, Z_S0 - 4, 49.75, Z_S0, fc="#bfc5b0", lw=0.3)
    v.rect(-49.75, Z_S1, 49.75, Z_S1 + 4, fc="#bfc5b0", lw=0.3)
    if sand:
        pressure_cells(v, labels=False)
        m_section(v)
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


PCOL = "#1f7a8c"     # pressure sensors


TDRC, PTC, FBGC = "#2e7d32", "#c9a800", "#0097a7"     # point M colours


def m_section(v, side=-1, labels=False, big=False):
    """Point M revolved into the section on `side`: 3 TDR rods; Pt100 and FBG lie ±12 mm beside them
    (hidden behind / in front of the rods – true layout on the plan of point M)."""
    z = Z_S1 - p.M_DEPTH
    r_w = p.D_SAMPLE / 2
    hw, hh, hd = p.TDR_HEAD
    v.rect(side * R_OUT, z - p.M_BOSS[1] / 2, side * (R_OUT + p.M_BOSS[2]), z + p.M_BOSS[1] / 2, fc=PETG, lw=THIN, z=4)
    v.rect(side * (R_OUT - 2), z - hh / 2, side * (R_OUT - 2 + hd), z + hh / 2, fc=TDRC, lw=THIN, z=4.5)
    for dz in p.TDR_RODS_DZ:
        v.line([(side * R_OUT, z + dz), (side * (r_w - p.TDR_ROD_L), z + dz)], lw=1.1 if big else 0.9, c="#555", z=5)
    v.line([(side * (R_OUT + p.M_BOSS[2]), z + 2.5), (side * p.PT100_TIP_R, z + 2.5)], lw=0.8, c=PTC, ls=(0, (3, 1.5)), z=5.2)
    v.line([(side * (R_OUT + p.M_BOSS[2]), z - 2.5), (side * p.FBG_TIP_R, z - 2.5)], lw=0.8, c=FBGC, ls=(0, (1, 1)), z=5.2)
    v.circle(side * 25, z, 2.2 if big else 3.5, fc="none", ec="#d33682", lw=0.8, z_=6)
    if labels:
        v.text(side * 25, z - 6, "M", fontsize=FS_SMALL, color="#d33682", ha="center", va="top", weight="bold", zorder=6)


def m_plan(v):
    """Plan of point M at its depth: boss, TDR head + 3 rods (stacked), Pt100 (+12) and FBG (−12)."""
    r_w = p.D_SAMPLE / 2
    hw, hh, hd = p.TDR_HEAD
    bw, bh, bt = p.M_BOSS
    # local frame: x = radius (0 = axis, wall at 50…58.5), y = sideways
    v.rect(0, -bw / 2 - 12, r_w, bw / 2 + 12, fc="#e9dcb8", lw=THIN)
    v.rect(r_w - p.LINER, -bw / 2 - 12, r_w, bw / 2 + 12, fc="#f7f7f7", lw=0.3)
    v.rect(R_IN, -bw / 2 - 12, R_OUT, bw / 2 + 12, fc=PETG, lw=THIN, hatch="\\\\\\\\")
    v.rect(R_OUT, -bw / 2, R_OUT + bt, bw / 2, fc=PETG, lw=THIN, hatch="\\\\\\\\")
    v.rect(R_OUT - 2, -hw / 2, R_OUT - 2 + hd, hw / 2, fc=TDRC, lw=THIN, z=4)
    v.rect(r_w - p.TDR_ROD_L, -p.TDR_ROD_D / 2, R_OUT - 2, p.TDR_ROD_D / 2, fc="#888", lw=0.4, z=4)
    v.rect(p.PT100_TIP_R, p.M_SIDE - p.PT100_D / 2, R_OUT + bt + 25, p.M_SIDE + p.PT100_D / 2, fc=PTC, lw=0.4, z=4)
    v.rect(p.PT100_TIP_R, p.M_SIDE - p.PT100_D / 2, p.PT100_TIP_R + 10, p.M_SIDE + p.PT100_D / 2, fc="#8a7300",
           lw=0.4, z=4.1)
    v.rect(p.FBG_TIP_R, -p.M_SIDE - p.FBG_D / 2, R_OUT + bt + 25, -p.M_SIDE + p.FBG_D / 2, fc=FBGC, lw=0.4, z=4)
    v.rect(p.FBG_TIP_R, -p.M_SIDE - 1.2, p.FBG_TIP_R + 10, -p.M_SIDE + 1.2, fc="none", ec="#00606b", lw=0.5, z=4.1)
    v.circle(25, 0, 4.5, fc="none", ec="#d33682", lw=0.9, z_=6)
    v.text(0, bw / 2 + 13, "r 0 (cell axis)", fontsize=FS_SMALL - 1, ha="left", va="bottom", color="#555")
    v.text(R_OUT + bt + 27, p.M_SIDE, "Pt100 1/10 DIN ⌀3", fontsize=FS_SMALL - 0.5, va="center", color="#8a7300")
    v.text(R_OUT + bt + 27, -p.M_SIDE, "FBG in capillary ⌀1", fontsize=FS_SMALL - 0.5, va="center", color="#00606b")
    v.text(R_OUT + bt + 27, 0, "TDR head + coax", fontsize=FS_SMALL - 0.5, va="center", color=TDRC)
    v.dim_h(r_w - p.TDR_ROD_L, r_w, -bw / 2 - 12, -bw / 2 - 18, f"TDR rods {p.TDR_ROD_L:g} (3× ⌀1.6, 5 apart vertically)",
            side="below")
    v.dim_v(0, p.M_SIDE, 10, 4, f"{p.M_SIDE:g}")
    v.dim_v(-p.M_SIDE, 0, 10, 4, f"{p.M_SIDE:g}")


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
            v.text(-R_IN + 3, z, tag_, fontsize=FS_SMALL - 0.5, color=PCOL, ha="left", va="center", weight="bold",
                   bbox=dict(fc="white", ec="none", pad=0.2), zorder=7)


def cell_detail(sh, ox, oy, k):
    """Enlarged section of the cell with sand, pressure sensors and thermistors."""
    v = View(sh, ox, oy, k)
    v.rect(-R_IN - 1, Z_S0 - 12, R_IN + 1, Z_S0, fc=METAL, lw=THIN)
    solid_cell(v, top=Z_S1 + 18, foot=False)
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
        v.line([(s_ * R_OUT, z), (s_ * p.T_TIP_R, z)], lw=0.7, c=TCOL)
        v.circle(s_ * p.T_TIP_R, z, 1.2, fc=TCOL, lw=0)
        v.text(s_ * (R_OUT + 2), z, f"T{i}", fontsize=FS_SMALL - 0.5, color=TCOL, va="center",
               ha="left" if s_ > 0 else "right")
    pressure_cells(v, labels=True)
    m_section(v, labels=True)
    v.dim_v(Z_S0, Z_S1, R_OUT, R_OUT + 14, "100")
    v.dim_h(-p.D_SAMPLE / 2, p.D_SAMPLE / 2, Z_S0 - 12, Z_S0 - 18, "⌀100 unsaturated sand", side="below")


def temp_points(v, variant, z_lc):
    pts = []
    for i, (d, ang) in enumerate(WALL_TH, 1):
        s_ = 1 if i % 2 else -1
        z = Z_S1 - d
        v.line([(s_ * R_INS, z), (s_ * p.T_TIP_R, z)], lw=0.8, c=TCOL)
        v.circle(s_ * p.T_TIP_R, z, 2.0, fc=TCOL, lw=0)
        v.text(s_ * (R_INS + 3), z, f"T{i}", fontsize=FS_SMALL, color=TCOL, va="center",
               ha="left" if s_ > 0 else "right", weight="bold")
    for name, x, z in (("Ttop", 30, Z_PT - 8), ("Tbot", 30, Z_PED + 15)):
        v.circle(x, z, 2.0, fc=TCOL, lw=0)
        v.text(x + 5, z, name, fontsize=FS_SMALL, color=TCOL, va="center", weight="bold")
    v.circle(-X_COL, 70, 2.0, fc=TCOL, lw=0)
    v.text(-X_COL - 26, 70, "Tframe", fontsize=FS_SMALL, color=TCOL, va="center", ha="right", weight="bold")
    v.circle(-X_COL - 60, 260, 2.0, fc=TCOL, lw=0)
    v.text(-X_COL - 60, 268, "Tair", fontsize=FS_SMALL, color=TCOL, ha="center", weight="bold")


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
    tag(v, -R_IN - 4, Z_S0 + 50, -150, 160, "cell PETG-CF, solid print\n+ PTFE liner 0.5 + grease", INK)
    tag(v, -R_INS + 5, Z_S0 + 20, -150, 100, "insulation Kaiflex 25", INK)
    tag(v, -25, Z_S1 - p.M_DEPTH, -150, 130, f"M: TDR + Pt100 + FBG at one point\n(depth {p.M_DEPTH:g}, r ≈ 25, 108°)", "#d33682")
    tag(v, -60, Z_G10 + 5, -150, 40, "G10 thermal break", INK)
    tag(v, 0, -12, 60, -45, f"light frame: Al 40×40, columns {p.FRAME_H_A:g}", INK)
    rows = [["PV1 / PH1", "vert. / radial stress", sn.PICK["PC"][1], sn.PICK["PC"][3]],
            ["PB1", "vertical stress at base", sn.PICK["PW"][1], sn.PICK["PW"][3]],
            ["PW1…PW3", "lateral stress on wall", sn.PICK["PW"][1], sn.PICK["PW"][3]],
            ["LVDT-1,2", "check: no movement", sn.PICK["LVDT"][1], sn.PICK["LVDT"][3]],
            ["T1…T5", "soil, r 40 mm", sn.PICK["T"][1], sn.PICK["T"][3]],
            ["M: TDR", "water / unfrozen water", sn.PICK["TDR"][1], sn.PICK["TDR"][3]],
            ["M: Pt100", "reference temperature", sn.PICK["PT100"][1], sn.PICK["PT100"][3]],
            ["M: FBG", "optical temperature", sn.PICK["FBG"][1], sn.PICK["FBG"][3]],
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


# --- variant B: same sample, no load, displacement + layer strain --------------------
Z_TP = Z_S1 + p.TOP_PLATE_T                    # top of the light top plate
Z_BR = p.Z_BRIDGE
BODY_D, BODY_L = p.LVDT_B_BODY
Z_BODY0 = Z_BR - 35.0                          # LVDT body bottom (clamped in the bridge)
# x positions in the revolved section (true positions on the plan view)
X_S = {"S1": 42.0, "S2": -42.0}
X_E = {"E1": -22.0, "E2": 22.0, "E3": 6.0}




def rig_b(v):
    """Simplified elevation of rig B: no frame, Invar stand + bridge with 5 free-core LVDTs."""
    hb = p.BASE_W / 2
    v.rect(-hb, -p.BASE_T, hb, 0, fc=METAL, hatch="////")
    for xf in (-hb + 20, hb - 20):
        v.rect(xf - 8, -p.BASE_T - 18, xf + 8, -p.BASE_T, fc=STEEL, lw=THIN)
    light = dict(lw=THIN)
    v.rect(-30, 0, 30, H_BOT, fc=METAL, **light)
    v.rect(-75, Z_G10, 75, Z_PED, fc=G10, **light)
    v.rect(-75, Z_PED, 75, Z_S0, fc=METAL, **light)
    for s_ in (-1, 1):
        v.rect(s_ * R_OUT, Z_S0 + p.CELL_FOOT_T, s_ * R_INS, TUBE_TOP, fc=INSUL, lw=0.3)
    solid_cell(v)
    v.rect(-p.D_SAMPLE / 2, Z_S0, p.D_SAMPLE / 2, Z_S1, fc="#e9dcb8", **light)
    v.rect(-49.75, Z_S0 - 4, 49.75, Z_S0, fc="#bfc5b0", lw=0.3)
    v.rect(-p.TOP_PLATE_D / 2, Z_S1, p.TOP_PLATE_D / 2, Z_TP, fc=PETG, **light)
    # Invar posts (one in the section plane, two revolved) and the bridge
    v.rect(-p.STAND_R - 6, 0, -p.STAND_R + 6, Z_BR, fc=INVAR, lw=THIN, alpha=0.8)
    v.rect(p.STAND_R - 6, 0, p.STAND_R + 6, Z_BR, fc=INVAR, lw=THIN, ls="--", alpha=0.35)
    v.rect(-p.BRIDGE_D / 2, Z_BR, p.BRIDGE_D / 2, Z_BR + p.BRIDGE_T, fc=METAL, lw=THIN, hatch="////")
    # surface LVDTs on the top plate
    for t, x in X_S.items():
        v.rect(x - 2, Z_TP, x + 2, Z_TP + 3, fc=STEEL, lw=0.3)
        v.line([(x, Z_TP + 3), (x, Z_BODY0 + 20)], lw=THICK, c=STEEL)
        v.rect(x - 6, Z_BODY0, x + 6, Z_BODY0 + BODY_L, fc=SENS, **light)
    # anchors with Invar rods in PTFE sleeves
    for (t, d, r, ang) in p.ANCHORS:
        x = X_E[t]
        z = Z_S1 - d
        v.rect(x - p.ANCHOR_D / 2, z - p.ANCHOR_T / 2, x + p.ANCHOR_D / 2, z + p.ANCHOR_T / 2, fc="#555", lw=THIN, z=4)
        v.rect(x - p.SLEEVE_D / 2, z + 2, x + p.SLEEVE_D / 2, Z_TP + 4, fc="white", lw=0.3, z=4)
        v.line([(x, z), (x, Z_BODY0 + 20)], lw=1.0, c=INVAR, z=5)
        v.rect(x - 6, Z_BODY0, x + 6, Z_BODY0 + BODY_L, fc=SENS, **light)
        v.text(x + (p.ANCHOR_D / 2 + 1) * (1 if x > 0 else -1), z, t, fontsize=FS_SMALL - 0.5, va="center",
               ha="left" if x > 0 else "right", color="#333", weight="bold", zorder=6)
    m_section(v)
    for name, x, z in (("Ttop", -35, Z_S1 + 3), ("Tbot", 30, Z_PED + 15), ("Tstand", -p.STAND_R, 228)):
        v.circle(x, z, 2.0, fc=TCOL, lw=0, z_=6)
        v.text(x + (5 if name != "Ttop" else -5), z, name, fontsize=FS_SMALL, color=TCOL, va="center", weight="bold", zorder=6,
               ha="right" if name == "Ttop" else "left", bbox=dict(fc="white", ec="none", pad=0.2))
    for i, (d, ang) in enumerate(WALL_TH, 1):
        s_ = 1 if i % 2 else -1
        z = Z_S1 - d - 2
        v.line([(s_ * R_INS, z), (s_ * 40, z)], lw=0.8, c=TCOL)
        v.circle(s_ * 40, z, 1.6, fc=TCOL, lw=0)
        v.text(s_ * (R_INS + 3), z, f"T{i}", fontsize=FS_SMALL, color=TCOL, va="center",
               ha="left" if s_ > 0 else "right", weight="bold")
    v.circle(-p.STAND_R - 45, 230, 2.0, fc=TCOL, lw=0)
    v.text(-p.STAND_R - 45, 236, "Tair", fontsize=FS_SMALL, color=TCOL, ha="center", weight="bold")


def plate_plan(v):
    """Plan of the top plate: true positions of S1–S3, E1–E3 and the Invar posts."""
    v.circle(0, 0, R_INS, fc=INSUL, lw=THIN)
    v.circle(0, 0, R_OUT, fc=PETG, lw=THIN)
    v.circle(0, 0, p.TOP_PLATE_D / 2, fc="#eef0f2", lw=THIN)
    for t, r, ang in p.SURF_LVDT:
        x, y = r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang))
        v.circle(x, y, 4, fc=SENS, lw=THIN)
        v.text(x * 1.35, y * 1.35, t, fontsize=FS_SMALL - 0.5, ha="center", va="center", color=SENS_TXT, weight="bold")
    for t, d, r, ang in p.ANCHORS:
        x, y = r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang))
        v.circle(x, y, p.PLATE_HOLE_D / 2, fc="white", lw=THIN)
        v.circle(x, y, 1.0, fc=INVAR, lw=0)
        v.text(x * 0.45, y * 0.45, t, fontsize=FS_SMALL - 0.5, ha="center", va="center", color="#333", weight="bold")
    for ang in p.STAND_ANG:
        v.circle(p.STAND_R * math.cos(math.radians(ang)), p.STAND_R * math.sin(math.radians(ang)),
                 p.STAND_POST_D / 2, fc=INVAR, lw=THIN)
    v.circle(0, 0, p.BRIDGE_D / 2, fc="none", ec=INK, lw=THIN, ls="--")


def anchor_detail(sh, ox, oy, k):
    """Enlarged section: cell, sand, top plate, anchors with rods and sleeves."""
    v = View(sh, ox, oy, k)
    v.rect(-R_IN - 1, Z_S0 - 12, R_IN + 1, Z_S0, fc=METAL, lw=THIN)
    solid_cell(v, top=Z_S1 + 18, foot=False)
    v.rect(-p.D_SAMPLE / 2, Z_S0, p.D_SAMPLE / 2, Z_S1, fc="#e9dcb8", lw=THIN)
    import random
    rnd = random.Random(2)
    for _ in range(260):
        v.circle(rnd.uniform(-48, 48), rnd.uniform(Z_S0 + 1, Z_S1 - 1), 0.35, fc="#b39a6b", ec="none", lw=0, z_=2.1)
    v.rect(-p.TOP_PLATE_D / 2, Z_S1, p.TOP_PLATE_D / 2, Z_TP, fc=PETG, lw=THIN)
    for t, x in X_S.items():
        v.rect(x - 2, Z_TP, x + 2, Z_TP + 3, fc=STEEL, lw=0.3)
        v.line([(x, Z_TP + 3), (x, Z_TP + 16)], lw=THICK, c=STEEL)
        v.text(x, Z_TP + 17, t, fontsize=FS_SMALL - 0.5, ha="center", va="bottom", color=SENS_TXT, weight="bold")
    for t, d, r, ang in p.ANCHORS:
        x = X_E[t]
        z = Z_S1 - d
        v.rect(x - p.ANCHOR_D / 2, z - p.ANCHOR_T / 2, x + p.ANCHOR_D / 2, z + p.ANCHOR_T / 2, fc="#555", lw=THIN, z=4)
        v.rect(x - p.SLEEVE_D / 2, z + 2, x + p.SLEEVE_D / 2, Z_TP + 4, fc="white", lw=0.3, z=4)
        v.line([(x, z), (x, Z_TP + 16)], lw=0.9, c=INVAR, z=5)
        v.text(x, Z_TP + 17, t, fontsize=FS_SMALL - 0.5, ha="center", va="bottom", color="#333", weight="bold")
        v.line([(x + p.ANCHOR_D / 2, z), (R_IN + 2, z)], lw=0.3, c="#777", ls=":")
    for i, (d, ang) in enumerate(WALL_TH, 1):
        s_ = 1 if i % 2 else -1
        z = Z_S1 - d - 2
        v.line([(s_ * R_OUT, z), (s_ * 40, z)], lw=0.7, c=TCOL)
        v.circle(s_ * 40, z, 1.2, fc=TCOL, lw=0)
        v.text(s_ * (R_OUT + 2), z, f"T{i}", fontsize=FS_SMALL - 0.5, color=TCOL, va="center",
               ha="left" if s_ > 0 else "right")
    for tag_, d, ang in p.PWALL:
        z = Z_S1 - d
        v.rect(-R_IN - 3, z - p.PWALL_D / 2, -R_IN + 0.5, z + p.PWALL_D / 2, fc=PCOL, lw=THIN, z=4)
    m_section(v, labels=True)
    zt = Z_S1
    for _, d, _, _ in p.ANCHORS:
        v.dim_v(Z_S1 - d, zt, R_OUT, R_OUT + 12, f"{(zt and 25):g}")
        zt = Z_S1 - d
    v.dim_v(Z_S0, zt, R_OUT, R_OUT + 12, "25")
    v.dim_v(Z_S0, Z_S1, R_OUT, R_OUT + 24, "100")
    v.dim_h(-p.D_SAMPLE / 2, p.D_SAMPLE / 2, Z_S0 - 12, Z_S0 - 18, "⌀100 unsaturated sand", side="below")


def sheet_b_simple(pdf):
    sh = Sheet("Variant B – same sample, no load: heave, settlement, layer strain", "E7-V02", "≈ 1 : 2", 2,
               TOTAL, "schematic; orange = displacement, red = temperature, violet = Invar reference; "
               "sensors revolved into section (true positions on the plan)")
    v = View(sh, 112, 66, 0.48)
    rig_b(v)
    tag(v, 42, Z_BODY0 + 60, 150, Z_BR + 60, "S1–S3  surface LVDT, free core\n(3× → mean heave + tilt)", SENS_TXT)
    tag(v, -22, Z_BODY0 + 60, -150, Z_BR + 60, "E1–E3  anchor LVDT, free core", SENS_TXT)
    tag(v, p.BRIDGE_D / 2 - 10, Z_BR + 5, 150, Z_BR + 20, "Al bridge ⌀220×10 (LVDT clamps)", INK)
    tag(v, -p.STAND_R, 60, -150, 120, "3 Invar posts ⌀12\nfrom the base plate", INVAR)
    tag(v, 30, Z_S1 + 3, 150, Z_S1 + 25, "top plate PETG-CF ⌀99×6\n≈ 65 g ≈ 0.08 kPa", INK)
    tag(v, 22, Z_S1 - 25, 150, Z_S1 - 10, "anchor ⌀16×1.5 + Invar rod ⌀2\nin PTFE sleeve ⌀4", INK)
    tag(v, R_OUT, Z_S0 + 40, 150, Z_S0 + 20, "same cell PETG-CF\n+ PTFE liner (as A)", INK)
    tag(v, -60, Z_G10 + 5, -150, 30, "G10 thermal break", INK)
    tag(v, -25, Z_S1 - p.M_DEPTH, -150, Z_S1 - 30, f"M: TDR + Pt100 + FBG at one point\n(depth {p.M_DEPTH:g}, r ≈ 25, 108°)", "#d33682")
    tag(v, 0, -12, 60, -40, "base plate Al 260×200×25 – no frame, no load", INK)
    rows = [["S1…S3", "surface heave / settlement", sn.PICK["LVDT-B"][1], "SE3–5"],
            ["E1…E3", "anchor displ. at 25/50/75", sn.PICK["LVDT-B"][1], "SE6–8"],
            ["PW1…PW3", "lateral stress (optional)", sn.PICK["PW"][1], sn.PICK["PW"][3]],
            ["T1…T5", "soil, r 40 mm", sn.PICK["T"][1], sn.PICK["T"][3]],
            ["M: TDR", "water / unfrozen water", sn.PICK["TDR"][1], sn.PICK["TDR"][3]],
            ["M: Pt100", "reference temperature", sn.PICK["PT100"][1], sn.PICK["PT100"][3]],
            ["M: FBG", "optical temperature", sn.PICK["FBG"][1], sn.PICK["FBG"][3]],
            ["Ttop, Tbot", "top plate, pedestal", sn.PICK["T"][1], "(same)"],
            ["Tstand, Tair", "Invar stand, air", sn.PICK["TX"][1], sn.PICK["TX"][3]]]
    y = legend(sh, rows)
    sh.text(255, y - 4,
            "What is measured in each freeze–thaw cycle\n"
            "• surface: heave during freezing, settlement during thawing, residual after the cycle\n"
            "  (mean of S1–S3; their difference = tilt of the top plate)\n"
            "• 4 layers of 25 mm: Δh₁ = S̄ − E1, Δh₂ = E1 − E2, Δh₃ = E2 − E3, Δh₄ = E3 (base fixed)\n"
            "  strain εᵢ = Δhᵢ / 25 mm, resolution ≈ 4·10⁻⁵ (vypocty.md §3)\n"
            "• frost depth from T1–T5 (0 °C isotherm) → strain vs. frozen / unfrozen layer\n"
            "• after the last cycle: height (caliper), mass, water content of 5 slices × 20 mm\n"
            "\n"
            "No load: free-core LVDTs push nothing; the plate adds 0.08 kPa only.\n"
            "Reference error ≈ 50 µm per 20 K → blank run with Al dummy (vypocty.md §4).",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.text(300, 153, "DETAIL – anchors and top plate  ≈ 1 : 1.6", fontsize=FS + 0.5, weight="bold", ha="center")
    anchor_detail(sh, 300, 18, 0.62)
    sh.text(378, 153, "PLAN – top plate  1 : 3.6", fontsize=FS + 0.5, weight="bold", ha="center")
    pv = View(sh, 378, 105, 0.28)
    plate_plan(pv)
    sh.text(378, 66, "orange S = surface LVDT (r 40)\nE = anchor rod hole (r 25)\nviolet = Invar posts (r 100)",
            fontsize=FS_SMALL - 0.5, ha="center", va="top", linespacing=1.4)
    sh.save(pdf, os.path.join(OUT, "E7-V02_variant_B_scheme.png"))


# --- variant A-min: maximally simplified A --------------------------------------------
def sheet_a_min(pdf):
    sh = Sheet("Variant A-min – simplified: fixed lid (no movement), no frame, no multiplexer", "E7-V07",
               "≈ 1 : 2.2", 7, TOTAL, "schematic; blue = pressure, red = temperature, magenta = point M "
               "(existing TDR + temp. sensor + fibre); revolved section")
    v = View(sh, 112, 40, 0.5)
    bw, bd, _ = p.AM_BASE
    bt = p.AM_BASE_T2
    zb0 = Z_S0 - p.AM_BOTTOM_T - p.AM_G10_T          # top of the base plate
    v.rect(-bw / 2, zb0 - bt, bw / 2, zb0, fc=METAL, hatch="////")
    v.rect(-75, zb0, 75, zb0 + p.AM_G10_T, fc=G10, lw=THIN)
    v.rect(-75, zb0 + p.AM_G10_T, 75, Z_S0, fc=METAL, lw=THIN, hatch="////")
    for s_ in (-1, 1):
        v.rect(s_ * R_OUT, Z_S0 + p.CELL_FOOT_T, s_ * R_INS, TUBE_TOP, fc=INSUL, lw=0.3)
    solid_cell(v)
    v.rect(-p.D_SAMPLE / 2, Z_S0, p.D_SAMPLE / 2, Z_S1, fc="#e9dcb8", lw=THIN)
    tg, d = p.AM_PV
    v.rect(-p.PCELL_D / 2, Z_S1 - d - 1, p.PCELL_D / 2, Z_S1 - d + 1, fc=PCOL, lw=THIN, z=4)
    tg_b, rb, _ = p.AM_PB
    v.rect(rb - 4, Z_S0 - 1.5, rb + 4, Z_S0, fc=PCOL, lw=THIN, z=4)
    for tg_t, d, ang in p.AM_TEMPS:
        s_ = 1 if math.cos(math.radians(ang)) >= 0 else -1
        v.line([(s_ * R_INS, Z_S1 - d), (s_ * p.T_TIP_R, Z_S1 - d)], lw=0.8, c=TCOL, ls=(0, (3, 2)))
        v.circle(s_ * p.T_TIP_R, Z_S1 - d, 2.0, fc=TCOL, lw=0)
        v.text(s_ * (p.AM_TIE_R + 9), Z_S1 - d, tg_t + " (opt.)", fontsize=FS_SMALL, color=TCOL, va="center",
               ha="left" if s_ > 0 else "right")
    m_section(v, labels=True)
    # piston, lid, tie rods, centre screw
    zp = Z_S1 + p.AM_PISTON_H
    v.rect(-49.75, Z_S1, 49.75, zp, fc=METAL, lw=THIN, hatch="////")
    zl0 = zp + p.AM_LID_GAP
    zl1 = zl0 + p.AM_LID_T
    v.rect(-p.AM_LID_D / 2, zl0, p.AM_LID_D / 2, zl1, fc=STEEL, lw=THICK, hatch="xx")
    for s_ in (-1, 1):
        v.rect(s_ * p.AM_TIE_R - p.AM_TIE_D / 2, zb0 - bt, s_ * p.AM_TIE_R + p.AM_TIE_D / 2, zl1 + 12,
               fc=STEEL, lw=THIN, ls="--" if s_ > 0 else "-")
        for zz in (zl1, zb0 - bt - 8):
            v.rect(s_ * p.AM_TIE_R - 9, zz, s_ * p.AM_TIE_R + 9, zz + 8, fc="#6f757b", lw=THIN)
    v.rect(-p.AM_SCREW_D / 2, zp, p.AM_SCREW_D / 2, zl1 + 30, fc="#6f757b", lw=THIN, z=3.5)
    v.rect(-14, zl1, 14, zl1 + 10, fc="#555", lw=THIN, z=3.6)
    # LVDT on the lid, post in the corner of the base plate
    xpost = -math.hypot(bw / 2 - 15, bw / 2 - 15)
    x_l = -p.AM_LID_D / 2 + 10                      # LVDT at 225° (towards the post), clear of the tie rods
    z_arm = zl1 + 75
    v.rect(xpost - p.AM_POST_D / 2, zb0, xpost + p.AM_POST_D / 2, z_arm + 10, fc=STEEL, lw=THIN)
    v.rect(xpost - 6, z_arm, x_l + 8, z_arm + 10, fc=STEEL, lw=THIN)
    v.rect(x_l - 6, zl1 + 15, x_l + 6, z_arm, fc=SENS, lw=THIN)
    v.line([(x_l, zl1), (x_l, zl1 + 15)], lw=THICK)
    v.circle(-p.AM_LID_D / 2 - 30, Z_S1 + 45, 2.0, fc=TCOL, lw=0)
    v.text(-p.AM_LID_D / 2 - 30, Z_S1 + 52, "Tair (opt.)", fontsize=FS_SMALL, color=TCOL, ha="center")
    v.text(0, (Z_S0 + Z_S1) / 2 - 22, "unsaturated\nsand ⌀100×100", fontsize=FS_SMALL - 0.5, ha="center", va="center")
    # labels (right)
    tag(v, x_l, z_arm - 20, 150, z_arm + 15, "LVDT  RDP DCTH400AG on the lid\n(proves the lid does not move)", SENS_TXT)
    tag(v, 0, zl1 + 25, 150, zl1 + 40, "centre screw M16×1.5 + lock nut\n(seat the piston at 5 kPa, then lock)", INK)
    tag(v, 60, zl0 + 7, 150, zl0 - 5, f"steel lid ⌀{p.AM_LID_D:g}×{p.AM_LID_T:g}", INK)
    tag(v, p.AM_TIE_R, Z_S1 + 20, 150, Z_S1 + 25, "3 tie rods M10 stainless (45/165/285°)", INK)
    tag(v, 40, Z_S1 + 25, 150, Z_S1 + 5, "Al piston ⌀99.5 × 40", INK)
    tag(v, 0, Z_S1 - 30, 150, Z_S1 - 25, "PV1  TML PDA-PA on ⌀20 disc (depth 30)", PCOL)
    tag(v, -25, Z_S1 - p.M_DEPTH, 150, Z_S1 - 55,
        "M: existing TDR (rods ≤ 40) + temp. sensor\n+ optical fibre – one point, depth 54", "#d33682")
    tag(v, rb, Z_S0 - 1, 150, Z_S0 + 5, "PB1  TML PDA-PA flush in the Al bottom", PCOL)
    tag(v, 30, zb0 + 17, 150, zb0 - 18, "Al bottom ⌀150×15 + G10 ⌀150×10", INK)
    tag(v, 60, zb0 - 10, 150, zb0 - 45, f"Al base plate {bw:g}×{bd:g}×{bt:g}", INK)
    # labels (left)
    tag(v, xpost, z_arm - 60, -128, z_arm - 40, "stainless post ⌀12", INK)
    tag(v, -R_IN - 4, Z_S0 + 50, -128, Z_S0 + 40, "cell PETG-CF solid print\n+ PTFE liner + grease", INK)
    tag(v, -R_INS + 5, Z_S0 + 75, -128, Z_S0 + 70, "Kaiflex 25", INK)
    v.dim_v(zb0 - bt, zl1, 125, 135, f"{zl1 - zb0 + bt:.0f}")
    # table
    sh.heading(255, 276, "To buy – type, quantity, price (EUR excl. VAT, ≈)")
    rows = []
    for tg_, what, typ, n, a, b, src, ch in sn.A_MIN_SENSORS:
        price = f"{n * a:,}" if a == b else f"{n * a:,}–{n * b:,}"
        rows.append([tg_ or "  +", typ, str(n), price.replace(",", " ") + (" *" if src == "web" else ""), ch])
    y = table(sh, 255, 272, ["tag", "type", "pcs", "EUR", "CR1000"], rows, [18, 66, 7, 22, 42], row_h=4.6)
    lo = sum(r[3] * r[4] for r in sn.A_MIN_SENSORS)
    hi = sum(r[3] * r[5] for r in sn.A_MIN_SENSORS)
    mlo = sum(a for _, a, b in sn.A_MIN_MECH)
    mhi = sum(b for _, a, b in sn.A_MIN_MECH)
    sh.text(255, y - 3,
            (f"sensors ≈ {lo:,}–{hi:,} EUR, mechanics ≈ {mlo}–{mhi} EUR → total ≈ {lo + mlo:,}–{hi + mhi:,} EUR\n").replace(",", " ")
            + "* price found at a dealer (Oct 2026, see README); others = estimates → ask for quotes.\n"
            "Already available (no cost): TDR, temperature sensor and optical fibre at point M, CR1000.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.heading(255, y - 20, "Existing sensors at point M")
    y2 = table(sh, 255, y - 24, ["tag", "type", "connection"], [[a, c, d] for a, b, c, d in sn.A_MIN_OWN],
               [18, 90, 47], row_h=4.6)
    sh.text(255, y2 - 3,
            "Fixed lid (vypocty.md §9)\n"
            "• piston seated by the centre screw at 5 kPa, locked → the sample cannot heave;\n"
            "  freezing pressure is read by PV1 (in the sand) and PB1 (at the bottom)\n"
            "• at 1 MPa: tie rods +49 µm, lid 60 µm → piston moves ≈ 0.1 mm (≈ 20 µm at 200 kPa)\n"
            "• stainless tie rods and the inner stack shrink almost equally (Δ ≈ 16 µm per 20 K)\n"
            "\n"
            "CR1000 wiring – no multiplexer\n"
            "DIFF1 PV1, DIFF2 PB1 (BrFull, VX1) · SE9 LVDT · SE11–13 T1, T2, Tair (optional)\n"
            "point M: per the existing devices (TDR on SDM C1–C3, temperature / fibre own reader)\n"
            "\n"
            "Removed vs. variant A: frame, weights, carrier, ball, Invar posts, 2nd LVDT,\n"
            "4 of 6 pressure cells, porous stones, pedestal, both multiplexers.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V07_variant_A_min.png"))


POMC = "#f4f1e8"


def sheet_a_frame(pdf):
    sh = Sheet("Variant A-frame – fixed piston in an Al profile frame, no multiplexer", "E7-V08", "≈ 1 : 2.2", 8,
               TOTAL, "schematic; blue = pressure, red = temperature, magenta = point M (existing sensors); "
               "dashed = behind the section plane")
    v = View(sh, 122, 44, 0.45)
    bw, bd, bt = p.AF_BASE
    zb0 = Z_S0 - p.AM_BOTTOM_T - p.AM_G10_T          # top of the base plate
    zbeam = zb0 + p.AF_COL_H
    xc = p.COL_SPAN / 2
    v.rect(-bw / 2, zb0 - bt, bw / 2, zb0, fc=METAL, hatch="////")
    for xf in (-bw / 2 + 20, bw / 2 - 20):
        v.rect(xf - 8, zb0 - bt - 18, xf + 8, zb0 - bt, fc=STEEL, lw=THIN)
    for s_ in (-1, 1):
        v.rect(s_ * (xc - 20), zb0, s_ * (xc + 20), zbeam, fc="#d9dde1", lw=THICK)
        v.line([(s_ * xc, zb0), (s_ * xc, zbeam)], lw=0.3, c="#888")
    v.rect(-xc - 20, zbeam, xc + 20, zbeam + p.AF_BEAM_H, fc="#d9dde1", lw=THICK)
    for zz in (zbeam + 20, zbeam + 60):
        v.line([(-xc - 20, zz), (xc + 20, zz)], lw=0.3, c="#888")
    v.rect(-75, zb0, 75, zb0 + p.AM_G10_T, fc=G10, lw=THIN)
    v.rect(-75, zb0 + p.AM_G10_T, 75, Z_S0, fc=METAL, lw=THIN, hatch="////")
    for s_ in (-1, 1):
        v.rect(s_ * R_OUT, Z_S0 + p.CELL_FOOT_T, s_ * R_INS, TUBE_TOP, fc=INSUL, lw=0.3)
    solid_cell(v)
    v.rect(-p.D_SAMPLE / 2, Z_S0, p.D_SAMPLE / 2, Z_S1, fc="#e9dcb8", lw=THIN)
    tg, d = p.AM_PV
    v.rect(-p.PCELL_D / 2, Z_S1 - d - 1, p.PCELL_D / 2, Z_S1 - d + 1, fc=PCOL, lw=THIN, z=4)
    tg_b, rb, _ = p.AM_PB
    v.rect(rb - 4, Z_S0 - 1.5, rb + 4, Z_S0, fc=PCOL, lw=THIN, z=4)
    for tg_t, d, ang in p.AM_TEMPS:
        s_ = 1 if math.cos(math.radians(ang)) >= 0 else -1
        v.line([(s_ * R_INS, Z_S1 - d), (s_ * p.T_TIP_R, Z_S1 - d)], lw=0.8, c=TCOL, ls=(0, (3, 2)))
        v.circle(s_ * p.T_TIP_R, Z_S1 - d, 2.0, fc=TCOL, lw=0)
        v.text(s_ * (R_INS + 2), Z_S1 - d + 4, tg_t, fontsize=FS_SMALL - 0.5, color=TCOL, va="bottom",
               ha="left" if s_ > 0 else "right")
    m_section(v, labels=True)
    zp = Z_S1 + p.AM_PISTON_H
    v.rect(-49.75, Z_S1, 49.75, zp, fc=METAL, lw=THIN, hatch="////")
    r_sp = p.AF_SPACER_D / 2
    z_pom0 = zbeam - p.AF_SCREW_PROTRUDE - p.AF_POM_T
    v.rect(-r_sp, zp, r_sp, z_pom0, fc=METAL, lw=THIN, hatch="////")
    v.rect(-r_sp, z_pom0, r_sp, z_pom0 + p.AF_POM_T, fc=POMC, lw=THIN, hatch="....")
    v.rect(-8, zbeam - p.AF_SCREW_PROTRUDE, 8, zbeam + p.AF_BEAM_H + 35, fc="#6f757b", lw=THIN, z=3.5)
    v.rect(-14, zbeam + p.AF_BEAM_H, 14, zbeam + p.AF_BEAM_H + 10, fc="#555", lw=THIN, z=3.6)
    v.rect(-30, zbeam + p.AF_BEAM_H + 35, 30, zbeam + p.AF_BEAM_H + 41, fc=STEEL, lw=THIN, z=3.6)
    # LVDT on the piston top edge, post at −y (behind the section)
    x_l = 40.0
    v.rect(x_l - 6, zp + 5, x_l + 6, zp + 60, fc=SENS, lw=THIN, ls="--")
    v.line([(x_l, zp), (x_l, zp + 5)], lw=THICK)
    v.line([(x_l + 6, zp + 55), (86, zp + 55), (86, zb0)], lw=THIN, ls=(0, (4, 2)), c=STEEL)
    v.circle(-xc - 60, Z_S1 + 70, 2.0, fc=TCOL, lw=0)
    v.text(-xc - 60, Z_S1 + 77, "Tair", fontsize=FS_SMALL, color=TCOL, ha="center")
    # labels right
    tag(v, 0, zbeam + p.AF_BEAM_H + 25, 150, zbeam + p.AF_BEAM_H + 45,
        "screw M16×1.5 + lock nut", INK)
    tag(v, 60, zbeam + 50, 150, zbeam + 20, "cross-beam Al 80×80", INK)
    tag(v, r_sp, z_pom0 + 7, 150, z_pom0 + 22, "POM-C ⌀40×15 (thermal comp.)", INK)
    tag(v, r_sp, zp + 25, 150, zp + 25, "Al spacer ⌀40×50", INK)
    tag(v, x_l, zp + 35, 150, zp + 45, "LVDT DCTH400AG on the piston\n(post at −y, behind)", SENS_TXT)
    tag(v, 40, Z_S1 + 25, 150, Z_S1 + 5, "Al piston ⌀99.5 × 40", INK)
    tag(v, 0, Z_S1 - 30, 150, Z_S1 - 25, "PV1  TML PDA-PA (depth 30)", PCOL)
    tag(v, -25, Z_S1 - p.M_DEPTH, 150, Z_S1 - 55, "M: existing TDR + temp. + fibre", "#d33682")
    tag(v, rb, Z_S0 - 1, 150, Z_S0 + 2, "PB1  TML PDA-PA, flush", PCOL)
    tag(v, 30, zb0 + 17, 150, zb0 - 20, "Al bottom ⌀150×15 + G10 ⌀150×10", INK)
    tag(v, 80, zb0 - 12, 150, zb0 - 50, f"Al base plate {bw:g}×{bd:g}×{bt:g}", INK)
    # labels left
    tag(v, -xc, zbeam - 40, -150, zbeam - 30, "2 columns Al 40×80 × 250", INK)
    tag(v, -R_IN - 4, Z_S0 + 50, -150, Z_S0 + 40, "cell PETG-CF + PTFE liner", INK)
    tag(v, -R_INS + 5, Z_S0 + 80, -150, Z_S0 + 75, "Kaiflex 25", INK)
    v.dim_v(zb0 - bt, zbeam + p.AF_BEAM_H, -xc - 30, -xc - 40, f"{p.AF_COL_H + p.AF_BEAM_H + bt:g}")
    v.dim_h(-xc, xc, zbeam + p.AF_BEAM_H, zbeam + p.AF_BEAM_H + 60, f"{p.COL_SPAN:g}")
    # right panel
    sh.heading(255, 276, "A-frame vs. A-min (tie rods)")
    rows = [["holds the piston", "frame 40×80 + 80×80, screw", "steel lid on 3 tie rods M10"],
            ["piston movement at 1 MPa", "≈ 0.08–0.15 mm", "≈ 0.11 mm"],
            ["thermal error (20 K)", "≈ 0 with POM-C insert", "≈ 16 µm"],
            ["access to the sample", "open sides, screw from top", "lid must be removed"],
            ["mechanics, EUR (≈)", "≈ 385–780", "≈ 340–690"],
            ["sensors to buy, EUR (≈)", "2 360–3 440 (same)", "2 360–3 440"]]
    y = table(sh, 255, 272, ["", "A-frame (this sheet)", "A-min (E7-V07)"], rows, [42, 58, 50], row_h=4.8)
    sh.heading(255, y - 6, "To buy (same sensors as A-min)")
    rows = []
    for tg_, what, typ, n, a, b, src, ch in sn.A_MIN_SENSORS:
        price = f"{n * a:,}" if a == b else f"{n * a:,}–{n * b:,}"
        rows.append([tg_ or "  +", typ, str(n), price.replace(",", " ") + (" *" if src == "web" else ""), ch])
    y = table(sh, 255, y - 10, ["tag", "type", "pcs", "EUR", "CR1000"], rows, [18, 66, 7, 22, 42], row_h=4.6)
    sh.text(255, y - 3,
            "* price found at a dealer (Oct 2026); others estimated – ask for quotes.\n"
            "Already available: TDR, temperature sensor, optical fibre (point M), CR1000.\n"
            "\n"
            "How it works\n"
            "• turn the screw until PV1 reads ≈ 5 kPa, lock the nut – the piston cannot move up;\n"
            "• freezing pressure is read by PV1 (in the sand) and PB1 (bottom); LVDT proves\n"
            "  the piston stays put (≈ 0.1 mm at 1 MPa, joints of the profiles dominate);\n"
            "• Al columns shrink more than the sand stack – the POM-C insert expands\n"
            "  the stack back (Δ ≈ 1 µm per 20 K), blank run with an Al dummy confirms it.\n"
            "Details: vypocty.md §10.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V08_variant_A_frame.png"))


def rig_plan(v, cx, cy, variant):
    hb, hd = p.BASE_W / 2, p.BASE_D / 2
    v.rect(cx - hb, cy - hd, cx + hb, cy + hd, fc=METAL, lw=THIN, z=2)
    if variant == "A":
        for s_ in (-1, 1):
            v.rect(cx + s_ * X_COL - 20, cy - 20, cx + s_ * X_COL + 20, cy + 20, fc="#d9dde1", lw=THIN, z=2.1)
    else:
        v.circle(cx, cy, p.BRIDGE_D / 2, fc="none", ec=INK, lw=THIN, ls="--", z_=2.5)
        for ang in p.STAND_ANG:
            v.circle(cx + p.STAND_R * math.cos(math.radians(ang)), cy + p.STAND_R * math.sin(math.radians(ang)),
                     p.STAND_POST_D / 2, fc=INVAR, lw=THIN, z_=2.6)
    v.circle(cx, cy, R_INS, fc=INSUL, lw=THIN, z_=2.2)
    v.circle(cx, cy, R_OUT, fc=PETG, lw=THIN, z_=2.3)
    v.circle(cx, cy, p.D_SAMPLE / 2, fc="#e9dcb8", lw=THIN, z_=2.4)
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
    for cx, var in ((185, "B"), (445, "A")):
        e.rect(cx - p.BASE_W / 2, zb - p.BASE_T, cx + p.BASE_W / 2, zb, fc=METAL, lw=THIN, z=2)
        if var == "A":
            hcol = p.FRAME_H_A
            for s_ in (-1, 1):
                e.rect(cx + s_ * X_COL - 20, zb, cx + s_ * X_COL + 20, zb + hcol, fc="#d9dde1", lw=THIN, z=2)
            e.rect(cx - X_COL - 20, zb + hcol, cx + X_COL + 20, zb + hcol + p.BEAM_H_A, fc="#d9dde1", lw=THIN, z=2)
            e.rect(cx - p.DW_D / 2, zb + 257, cx + p.DW_D / 2, zb + 383, fc="#8a8f96", lw=THIN, z=3)
            e.rect(cx - 8, zb + 257, cx + 8, zb + 257 + p.DW_ROD_L, fc=STEEL, lw=THIN, z=3.1)
        else:
            for x in (-p.STAND_R, p.STAND_R / 2):
                e.rect(cx + x - 6, zb, cx + x + 6, zb + p.Z_BRIDGE, fc=INVAR, lw=THIN, z=2)
            e.rect(cx - p.BRIDGE_D / 2, zb + p.Z_BRIDGE, cx + p.BRIDGE_D / 2, zb + p.Z_BRIDGE + p.BRIDGE_T,
                   fc=METAL, lw=THIN, z=2)
            for x in (-42, -22, 6, 22, 42):
                e.rect(cx + x - 5, zb + Z_BODY0, cx + x + 5, zb + Z_BODY0 + BODY_L, fc=SENS, lw=THIN, z=3)
        e.rect(cx - R_INS, zb + Z_S0, cx + R_INS, zb + TUBE_TOP, fc=INSUL, lw=THIN, z=2.1)
        e.text(cx, zb + 120, var, fontsize=FS + 2, weight="bold", ha="center", va="center", zorder=5)
    top = max(zb + 257 + p.DW_ROD_L, zb + p.FRAME_H_A + p.BEAM_H_A)
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
            ["rig B (stand)", f"{zb + Z_BODY0 + BODY_L:.0f} mm high", "no load, no frame", "OK"],
            ["highest point", f"{top:.0f} mm", "inside ≈ 650", "OK, measure"],
            ["logger", "outside, 0…+40 °C", "CR1000 −25…+50 °C", "keep warm & dry"]]
    table(sh, 255, 274, ["item", "size", "limit", "status"], rows, [48, 32, 38, 32], row_h=5.0)
    sh.text(255, 236,
            "Notes\n"
            "• Both rigs share the freezer program (Set A) and the CR1000; each rig has\n"
            "  its own Tair sensor at sample mid-height.\n"
            "• Same sand, same printed cell, same thermistors in A and B – the only\n"
            "  difference is the load (A ≤ 25 kPa dead weight, B none).\n"
            "• Run the blank test with Al dummies in both rigs before the first sand run.\n"
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
            "Channel count (2 rigs): 8 LVDTs, 9 pressure bridges, ≈ 20 thermistors,\n"
            "point M ×2: 2 TDR (TDR200 + SDMX50SP), 2 Pt100 (MUX-1), 2 FBG (interrogator).\n"
            "No load cells: A is loaded by dead weight, B is not loaded at all.\n"
            "\n"
            "Resolution with the CR1000 (13-bit ADC, ±5000 mV range)\n"
            "• LVDT ±10 mm (A): ≈ 1.3 µm; LVDT ±5 mm (B): ≈ 0.7 µm\n"
            "  → layer strain over 25 mm ≈ 4·10⁻⁵ (B)\n"
            "• absolute linearity ±0.25 % FS → calibrate each LVDT with a micrometer\n"
            "• 109SS: ±0.38 °C at 0 °C; ice-point offset check improves it\n"
            "\n"
            "Notes\n"
            "• Rig B uses LVDTs with a FREE (unguided) core – no spring force on the\n"
            "  sample; the core rides on the anchor rod / plate rod. Check the free-core\n"
            "  version and the core length with RDP before ordering [U].\n"
            "• DC-LVDTs need their own ±15 V (or 24 V) supply, logger only reads ±5 V.\n"
            "• CR1000 is discontinued (successor CR1000X / CR1000Xe, 24-bit); the\n"
            "  existing one is fine for these resolutions.\n"
            "• Logger outside the freezer (CR1000 −25…+50 °C).\n"
            "• Point M: TDR, Pt100 and FBG sit 12 mm apart at one depth – Pt100 is the\n"
            "  reference for the FBG and for T3; TDR gives unfrozen water vs. temperature.\n"
            "• Pressure cells: calibrate in the same sand under dead weight (5–25 kPa)\n"
            "  at +10 and −10 °C; correct zero(T) with the neighbouring thermistor.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V05_sensors_CR1000.png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith((".png", ".pdf")):
            os.remove(os.path.join(OUT, f))
    with PdfPages(os.path.join(OUT, "E7_drawings.pdf")) as pdf:
        for fn in (sheet_a_simple, sheet_b_simple, sheet_cell, sheet_frame, sheet_sensors, sheet_layout,
                   sheet_a_min, sheet_a_frame):
            fn(pdf)
