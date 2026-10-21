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
PT_MM = 72 / 25.4        # points per mm of paper
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


# ---------------------------------------------------------------------------
# simplified schemes (variant A and B)
import sensors as sn

SENS = "#e8a33d"      # sensor colour
SENS_TXT = "#a05a00"
TCOL = "#c0392b"      # temperature points


def cup_cell(v, insulation=True):
    """Variant A cell per drawing Column_one_body_version_1: body ⌀160 × 130 (10 % infill = insulation),
    collar ⌀106 up to 160, cavity ⌀100 from 26 (bottom) up; side port 13 wide at 67.5–94.5 (revolved left)."""
    zb = Z_S0 - p.BODY_BOTTOM                       # underside of the body
    rb, rc, ri = p.BODY_D / 2, p.COLLAR_OD / 2, p.CAV_D / 2
    z_j, z_c = zb + p.BODY_H, zb + p.COLLAR_TOP
    for s_ in (-1, 1):
        v.rect(s_ * ri, Z_S0, s_ * rb, z_j, fc=PETG, lw=THIN, hatch="..")
        v.rect(s_ * ri, z_j, s_ * rc, z_c, fc=PETG, lw=THIN, hatch="..")
        v.rect(s_ * ri, Z_S0, s_ * (ri + p.CUP_WALL_IN), z_c, fc=PETG, lw=THIN)
        v.rect(s_ * (rb - 2), zb, s_ * rb, z_j, fc=PETG, lw=0.3)
    v.rect(-rb, zb, rb, Z_S0, fc=PETG, lw=THIN, hatch="..")
    v.rect(-rb, zb, rb, zb + 2, fc=PETG, lw=0.3)
    # side port (revolved to the left)
    v.rect(-rb - 0.5, zb + p.PORT_Z0, -ri - p.CUP_WALL_IN, zb + p.PORT_Z1, fc="white", lw=THIN)
    v.rect(-rb, zb, rb, z_j, fc="none", lw=THICK)


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


def m_section_a(v, labels=False, cable_up=False):
    """Point M of variant A (sketch): CS645 rods horizontal through the axis, optical fibre at the top-rod
    level (tip 37.5 from the wall), Pt100 vertical from the sand surface 15 mm beside the axis."""
    t = p.TDR_CS645
    zb = Z_S0 - p.BODY_BOTTOM
    z_top = zb + p.COLLAR_TOP - t["top_from_collar"]
    ri = p.CAV_D / 2
    for k in range(3):
        z = z_top - k * t["pitch"]
        v.line([(-ri, z), (-ri + t["rod_l"], z)], lw=1.3, c="#555", z=5)
    v.rect(-ri - p.CUP_WALL_IN - t["head_l"], zb + p.PORT_Z0 + 0.5, -ri, zb + p.PORT_Z1 - 0.5, fc=TDRC, lw=THIN, z=5)
    v.line([(-ri, z_top + 1.8), (-ri + p.OF_TIP_FROM_WALL, z_top + 1.8)], lw=1.1, c=FBGC, z=5.2)
    v.rect(p.PT100_R - 1.5, Z_S1 - p.PT100_L, p.PT100_R + 1.5, Z_S1 - (p.PT100_L - p.PT100_METAL), fc=PTC, lw=0.5, z=5.2)
    # Pt100 cable: up to the sand surface, in a groove under the piston, out through a ⌀4 hole in the collar
    if cable_up:
        v.line([(p.PT100_R, Z_S1 - (p.PT100_L - p.PT100_METAL)), (p.PT100_R, Z_S1 + 30)], lw=0.9, c="#8a7300", z=5.2)
    else:
        v.line([(p.PT100_R, Z_S1 - (p.PT100_L - p.PT100_METAL)), (p.PT100_R, Z_S1 - 1),
                (p.CAV_D / 2 + p.CUP_WALL_IN + 4, Z_S1 - 1)], lw=0.9, c="#8a7300", z=5.2)
    if labels:
        v.text(-ri + t["rod_l"] + 2, z_top - t["pitch"], "CS645", fontsize=FS_SMALL - 0.5, va="center", color="#333")


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


# --- variant B: same sample, no load, displacement + layer strain --------------------
Z_TP = Z_S1 + p.TOP_PLATE_T                    # top of the light top plate
Z_BR = p.Z_BRIDGE
BODY_D, BODY_L = p.LVDT_B_BODY
Z_BODY0 = Z_BR - 35.0                          # LVDT body bottom (clamped in the bridge)
# x positions in the revolved section (true positions on the plan view)
X_S = {"S1": -34.0, "S2": -47.0}
X_E = {"E1": -20.0, "E2": 28.0, "E3": 42.0}




def rig_b(v):
    """Simplified elevation of rig B: printed cell ⌀160 on a base plate, Invar stand + bridge with 6 free-core
    LVDTs, point M as in A (CS645 + fibre + Pt100)."""
    hb = p.BASE_W / 2
    zb = Z_S0 - p.BODY_BOTTOM
    v.rect(-hb, zb - p.B_BASE_T, hb, zb, fc=METAL, hatch="////")
    for xf in (-hb + 20, hb - 20):
        v.rect(xf - 8, zb - p.B_BASE_T - 18, xf + 8, zb - p.B_BASE_T, fc=STEEL, lw=THIN)
    light = dict(lw=THIN)
    cup_cell(v)
    v.rect(-p.D_SAMPLE / 2, Z_S0, p.D_SAMPLE / 2, Z_S1, fc="#e9dcb8", **light)
    v.rect(-p.TOP_PLATE_D / 2, Z_S1, p.TOP_PLATE_D / 2, Z_TP, fc=PETG, **light)
    v.rect(-p.STAND_R - 6, zb, -p.STAND_R + 6, Z_BR, fc=INVAR, lw=THIN, alpha=0.8)
    v.rect(p.STAND_R - 6, zb, p.STAND_R + 6, Z_BR, fc=INVAR, lw=THIN, ls="--", alpha=0.35)
    v.rect(-p.BRIDGE_D / 2, Z_BR, p.BRIDGE_D / 2, Z_BR + p.BRIDGE_T, fc=METAL, lw=THIN, hatch="////")
    for t, x in X_S.items():
        v.rect(x - 2, Z_TP, x + 2, Z_TP + 3, fc=STEEL, lw=0.3)
        v.line([(x, Z_TP + 3), (x, Z_BODY0 + 20)], lw=THICK, c=STEEL)
        v.rect(x - 6, Z_BODY0, x + 6, Z_BODY0 + BODY_L, fc=SENS, **light)
    for (t, d, r, ang) in p.ANCHORS:
        x = X_E[t]
        z = Z_S1 - d
        v.rect(x - p.ANCHOR_D / 2, z - p.ANCHOR_T / 2, x + p.ANCHOR_D / 2, z + p.ANCHOR_T / 2, fc="#555", lw=THIN, z=4)
        v.rect(x - p.SLEEVE_D / 2, z + 2, x + p.SLEEVE_D / 2, Z_TP + 4, fc="white", lw=0.3, z=4)
        v.line([(x, z), (x, Z_BODY0 + 20)], lw=1.0, c=INVAR, z=5)
        v.rect(x - 6, Z_BODY0, x + 6, Z_BODY0 + BODY_L, fc=SENS, **light)
        v.text(x + (p.ANCHOR_D / 2 + 1) * (1 if x > 0 else -1), z, t, fontsize=FS_SMALL - 0.5, va="center",
               ha="left" if x > 0 else "right", color="#333", weight="bold", zorder=6)
    m_section_a(v, cable_up=True)
    for name, x, z in (("Ttop", -40, Z_S1 + 3), ("Tbot", 30, zb - 8), ("Tstand", -p.STAND_R, 228)):
        v.circle(x, z, 2.0, fc=TCOL, lw=0, z_=6)
        v.text(x + (5 if name != "Ttop" else -5), z, name, fontsize=FS_SMALL, color=TCOL, va="center", weight="bold",
               zorder=6, ha="right" if name == "Ttop" else "left", bbox=dict(fc="white", ec="none", pad=0.2))
    rb = p.BODY_D / 2
    for i, (d, ang) in enumerate(WALL_TH, 1):
        s_ = 1 if i % 2 else -1
        z = Z_S1 - d - 2
        v.line([(s_ * (rb + 6), z), (s_ * 40, z)], lw=0.8, c=TCOL)
        v.circle(s_ * 40, z, 1.6, fc=TCOL, lw=0)
        v.text(s_ * (rb + 8), z, f"T{i}", fontsize=FS_SMALL, color=TCOL, va="center",
               ha="left" if s_ > 0 else "right", weight="bold")
    v.circle(-p.STAND_R - 45, 230, 2.0, fc=TCOL, lw=0)
    v.text(-p.STAND_R - 45, 236, "Tair", fontsize=FS_SMALL, color=TCOL, ha="center", weight="bold")


def plate_plan(v):
    """Plan of the top plate: true positions of S1–S3, E1–E3, Pt100, TDR axis, port and the Invar posts."""
    rb, rc, ri = p.BODY_D / 2, p.COLLAR_OD / 2, p.CAV_D / 2
    v.circle(0, 0, rb, fc=PETG, lw=THIN)
    v.circle(0, 0, rc, fc="none", lw=THIN)
    v.circle(0, 0, p.TOP_PLATE_D / 2, fc="#eef0f2", lw=THIN)
    a = math.radians(p.PORT_ANG)
    v.line([(rb * math.cos(a), rb * math.sin(a)), (-25 * math.cos(a), -25 * math.sin(a))], lw=1.6, c="#777")
    v.rect(-p.PORT_W / 2, -rb, p.PORT_W / 2, -ri - p.CUP_WALL_IN, fc=TDRC, lw=THIN)
    v.circle(p.PT100_R, 0, p.B_PT100_HOLE / 2, fc=PTC, lw=THIN)
    for t, r, ang in p.SURF_LVDT:
        x, y = r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang))
        v.circle(x, y, 4, fc=SENS, lw=THIN)
        v.text(x * 1.45, y * 1.45, t, fontsize=FS_SMALL - 0.5, ha="center", va="center", color=SENS_TXT, weight="bold")
    for t, d, r, ang in p.ANCHORS:
        x, y = r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang))
        v.circle(x, y, p.PLATE_HOLE_D / 2, fc="white", lw=THIN)
        v.circle(x, y, 1.0, fc=INVAR, lw=0)
        v.text(x * 1.45, y * 1.45, t, fontsize=FS_SMALL - 0.5, ha="center", va="center", color="#333", weight="bold")
    for ang in p.STAND_ANG:
        v.circle(p.STAND_R * math.cos(math.radians(ang)), p.STAND_R * math.sin(math.radians(ang)),
                 p.STAND_POST_D / 2, fc=INVAR, lw=THIN)
    v.circle(0, 0, p.BRIDGE_D / 2, fc="none", ec=INK, lw=THIN, ls="--")


def anchor_detail(sh, ox, oy, k):
    """Enlarged section: cell, sand, top plate, anchors with rods and sleeves."""
    v = View(sh, ox, oy, k)
    ri, w = p.CAV_D / 2, p.CUP_WALL_IN
    for s_ in (-1, 1):
        v.rect(s_ * ri, Z_S0 - 12, s_ * (ri + 14), Z_S1 + 22, fc=PETG, lw=THIN, hatch="..")
        v.rect(s_ * ri, Z_S0, s_ * (ri + w), Z_S1 + 22, fc=PETG, lw=THIN)
    v.rect(-ri, Z_S0 - 12, ri, Z_S0, fc=PETG, lw=THIN, hatch="..")
    zb = Z_S0 - p.BODY_BOTTOM
    v.rect(-ri - 14.5, zb + p.PORT_Z0, -ri - w, zb + p.PORT_Z1, fc="white", lw=THIN)
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
        v.line([(x + p.ANCHOR_D / 2, z), (p.CAV_D / 2 + 2, z)], lw=0.3, c="#777", ls=":")
    for i, (d, ang) in enumerate(WALL_TH, 1):
        s_ = 1 if i % 2 else -1
        z = Z_S1 - d - 2
        v.line([(s_ * (p.CAV_D / 2 + 14), z), (s_ * 40, z)], lw=0.7, c=TCOL)
        v.circle(s_ * 40, z, 1.2, fc=TCOL, lw=0)
        v.text(s_ * (p.CAV_D / 2 + 16), z, f"T{i}", fontsize=FS_SMALL - 0.5, color=TCOL, va="center",
               ha="left" if s_ > 0 else "right")
    m_section_a(v, labels=True, cable_up=True)
    zt = Z_S1
    for _, d, _, _ in p.ANCHORS:
        v.dim_v(Z_S1 - d, zt, p.CAV_D / 2 + 14, p.CAV_D / 2 + 34, f"{(zt and 25):g}")
        zt = Z_S1 - d
    v.dim_v(Z_S0, zt, p.CAV_D / 2 + 14, p.CAV_D / 2 + 34, "25")
    v.dim_v(Z_S0, Z_S1, p.CAV_D / 2 + 14, p.CAV_D / 2 + 46, "100")
    v.dim_h(-p.D_SAMPLE / 2, p.D_SAMPLE / 2, Z_S0 - 12, Z_S0 - 18, "⌀100 unsaturated sand", side="below")


def _sheet_b_simple(pdf):
    sh = Sheet("Variant B – same sample, no load: heave and layer strain", "E7-V05", "≈ 1 : 2", 5,
               TOTAL, "orange = displacement, red = temperature, violet = Invar; revolved section")
    v = View(sh, 118, 62, 0.48)
    rig_b(v)
    zb = Z_S0 - p.BODY_BOTTOM
    tag(v, X_S["S1"], Z_BODY0 + 60, -150, Z_BR + 75, "S1–S3 surface LVDT\n(free core, 3×)", SENS_TXT)
    tag(v, X_E["E3"], Z_BODY0 + 60, 150, Z_BR + 75, "E1–E3 anchor LVDT\n(free core)", SENS_TXT)
    tag(v, p.BRIDGE_D / 2 - 10, Z_BR + 5, 150, Z_BR + 30, "Al bridge ⌀220×10", INK)
    tag(v, -p.STAND_R, zb + 40, -150, zb + 60, "3 Invar posts ⌀12", INVAR)
    tag(v, 30, Z_S1 + 3, 150, Z_S1 + 45, "top plate PETG-CF ⌀99×6\n≈ 65 g ≈ 0.08 kPa", INK)
    tag(v, X_E["E2"], Z_S1 - 50, 150, Z_S1 + 5, "anchor ⌀16 + Invar rod ⌀2\nin PTFE sleeve", INK)
    tag(v, -10, Z_S1 - 45, 150, Z_S1 - 40, "M: CS645 + fibre + Pt100\n(as in A, depth 36–54)", "#d33682")
    tag(v, p.BODY_D / 2 - 5, Z_S0 + 15, 150, Z_S0 - 15, "printed cell ⌀160 (V04)", INK)
    tag(v, 0, zb - 12, 150, zb - 45, "Al base plate 260×200×20", INK)
    rows = [["S1…S3", "surface heave", sn.PICK["LVDT-B"][1], "SE3–5"],
            ["E1…E3", "anchors 25/50/75", sn.PICK["LVDT-B"][1], "SE6–8"],
            ["M: TDR", "unfrozen water", "Campbell CS645 (existing)", "C1–C3 SDM"],
            ["M: Pt100", "temperature", "Pt100 37 mm (existing)", "4-wire"],
            ["M: OF", "temperature", "optical fibre (existing)", "own reader"],
            ["T1…T5", "soil, r 40", sn.PICK["T"][1], "MUX-2 SE13"],
            ["Ttop, Tbot", "plate, base", sn.PICK["T"][1], "(same)"],
            ["Tstand, Tair", "stand, air", sn.PICK["TX"][1], "(same)"]]
    sh.heading(255, 276, "Sensors (tag → model → CR1000)")
    y = table(sh, 255, 272, ["tag", "measures", "model", "CR1000"], rows, [24, 34, 60, 37], row_h=5.6)
    sh.text(255, y - 4,
            "Per freeze–thaw cycle\n"
            "• heave, settlement, residual: mean of S1–S3 (difference = tilt)\n"
            "• 4 layers of 25 mm: S̄ − E1, E1 − E2, E2 − E3, E3 (bottom fixed)\n"
            "  → strain per layer, resolution ≈ 4·10⁻⁵\n"
            "• frost depth from T1–T5, unfrozen water at M\n"
            "No load: free-core LVDTs push nothing, the plate adds 0.08 kPa.\n"
            "Reference error ≈ 40 µm per 20 K → blank run (vypocty.md §4).",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.text(292, 150, "DETAIL – anchors  ≈ 1 : 1.9", fontsize=FS + 0.5, weight="bold", ha="center")
    anchor_detail(sh, 292, 30, 0.52)
    sh.text(386, 150, "PLAN  1 : 4", fontsize=FS + 0.5, weight="bold", ha="center")
    pv = View(sh, 386, 112, 0.24)
    plate_plan(pv)
    sh.text(386, 80, "S = surface LVDT (r 40)\nE = anchor (r 25)\nyellow = Pt100, green = port\n"
            "violet = Invar posts", fontsize=FS_SMALL - 0.5, ha="center", va="top", linespacing=1.4)
    sh.save(pdf, os.path.join(OUT, "E7-V05_variant_B_scheme.png"))


def sheet_b_simple(pdf):
    with bigger_fonts():
        _sheet_b_simple(pdf)


# --- variant A-min: maximally simplified A --------------------------------------------
def _sheet_a_min(pdf):
    sh = Sheet("Variant A-min – fixed lid on 3 tie rods", "E7-V02",
               "≈ 1 : 2.2", 2, TOTAL, "blue = pressure, red = temperature, magenta = point M")
    v = View(sh, 112, 40, 0.5)
    bw, bd, _ = p.AM_BASE
    bt = p.AM_BASE_T2
    zb0 = Z_S0 - p.AM_BOTTOM_T - p.AM_G10_T          # top of the base plate
    v.rect(-bw / 2, zb0 - bt, bw / 2, zb0, fc=METAL, hatch="////")
    cup_cell(v)
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
    m_section_a(v, labels=True)
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
    v.circle(-160, Z_S1 + 10, 2.0, fc=TCOL, lw=0)
    v.text(-160, Z_S1 + 18, "Tair (opt.)", fontsize=FS_SMALL, color=TCOL, ha="center")
    v.text(-20, Z_S1 - 14, "unsaturated sand ⌀100×100", fontsize=FS_SMALL - 0.5, ha="center", va="center")
    # labels (right)
    tag(v, x_l, z_arm - 20, 150, z_arm + 15, "LVDT  RDP DCTH400AG on the lid\n(proves the lid does not move)", SENS_TXT)
    tag(v, 0, zl1 + 25, 150, zl1 + 40, "centre screw M16×1.5 + lock nut\n(seat the piston at 5 kPa, then lock)", INK)
    tag(v, 60, zl0 + 7, 150, zl0 - 5, f"steel lid ⌀{p.AM_LID_D:g}×{p.AM_LID_T:g}", INK)
    tag(v, p.AM_TIE_R, Z_S1 + 20, 150, Z_S1 + 25, "3 tie rods M10 stainless (45/165/285°)", INK)
    tag(v, 40, Z_S1 + 25, 150, Z_S1 + 5, "Al piston ⌀99.5 × 40", INK)
    tag(v, 0, Z_S1 - p.AM_PV[1], 150, Z_S1 - 25, "PV1  TML PDA-PA on ⌀20 disc (depth 75)", PCOL)
    tag(v, -10, Z_S1 - 45, 150, Z_S1 - 55,
        "M: TDR CS645 + optical fibre + Pt100\n(existing, one point, depth 36–54)", "#d33682")
    tag(v, rb, Z_S0 - 1, 150, Z_S0 + 5, "PB1  TML PDA-PA flush in the cup bottom", PCOL)
    tag(v, 60, zb0 - 10, 150, zb0 - 45, f"Al base plate {bw:g}×{bd:g}×{bt:g}", INK)
    # labels (left)
    tag(v, xpost, z_arm - 60, -128, z_arm - 40, "stainless post ⌀12", INK)
    tag(v, -R_IN - 4, Z_S0 + 50, -118, Z_S0 + 40, "printed cell ⌀160\n(V04)", INK)
    v.dim_v(zb0 - bt, zl1, 125, 135, f"{zl1 - zb0 + bt:.0f}")
    # table
    sh.heading(255, 276, "To buy – type, quantity, price (EUR excl. VAT, ≈)")
    rows = []
    for tg_, what, typ, n, a, b, src, ch in sn.A_MIN_SENSORS:
        price = f"{n * a:,}" if a == b else f"{n * a:,}–{n * b:,}"
        rows.append([tg_ or "  +", typ, str(n), price.replace(",", " ") + (" *" if src == "web" else ""),
                     ch.replace(" VoltSE ±5 V", "").replace(" Therm109", "")])
    y = table(sh, 255, 272, ["tag", "type", "pcs", "EUR", "CR1000"], rows, [20, 60, 8, 23, 44], row_h=5.8)
    lo = sum(r[3] * r[4] for r in sn.A_MIN_SENSORS)
    hi = sum(r[3] * r[5] for r in sn.A_MIN_SENSORS)
    mlo = sum(a for _, a, b in sn.A_MIN_MECH)
    mhi = sum(b for _, a, b in sn.A_MIN_MECH)
    sh.text(255, y - 3,
            (f"sensors ≈ {lo:,}–{hi:,} EUR, mechanics ≈ {mlo}–{mhi} EUR → total ≈ {lo + mlo:,}–{hi + mhi:,} EUR\n").replace(",", " ")
            + "* price found at a dealer (Oct 2026, see README); others = estimates → ask for quotes.\n"
            "Already available (no cost): TDR CS645, Pt100, optical fibre (point M), CR1000.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.heading(255, y - 24, "Existing sensors at point M")
    y2 = table(sh, 255, y - 28, ["tag", "type", "connection"], [[a, c, d] for a, b, c, d in sn.A_MIN_OWN],
               [20, 88, 47], row_h=5.8)
    sh.text(255, y2 - 3,
            "Fixed lid (vypocty.md §9)\n"
            "• piston seated by the centre screw at 5 kPa, locked → the sample cannot heave;\n"
            "  freezing pressure is read by PV1 (in the sand) and PB1 (at the bottom)\n"
            "• at 1 MPa: tie rods +49 µm, lid 60 µm → piston moves ≈ 0.1 mm (≈ 20 µm at 200 kPa)\n"
            "• stainless tie rods and the inner stack shrink almost equally (Δ ≈ 12 µm per 20 K)\n"
            "\n"
            "CR1000 wiring – no multiplexer\n"
            "DIFF1 PV1, DIFF2 PB1 (BrFull, VX1) · SE9 LVDT · SE11–13 T1, T2, Tair (optional)\n"
            "point M: per the existing devices (TDR on SDM C1–C3, temperature / fibre own reader)\n"
            "\n"
            "Removed vs. variant A: frame, weights, carrier, ball, Invar posts, 2nd LVDT,\n"
            "4 of 6 pressure cells, porous stones, pedestal, both multiplexers.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V02_variant_A_min.png"))


def sheet_a_min(pdf):
    with bigger_fonts():
        _sheet_a_min(pdf)


POMC = "#f4f1e8"


class bigger_fonts:
    """Temporarily enlarge all text on one sheet (drafting + this module read the sizes at call time)."""
    def __init__(self, fs=9.5, fs_small=8.5):
        self.new = (fs, fs_small)

    def __enter__(self):
        import drafting
        g = globals()
        self.old = (drafting.FS, drafting.FS_SMALL, g["FS"], g["FS_SMALL"])
        drafting.FS, drafting.FS_SMALL = self.new
        g["FS"], g["FS_SMALL"] = self.new
        return self

    def __exit__(self, *exc):
        import drafting
        g = globals()
        drafting.FS, drafting.FS_SMALL, g["FS"], g["FS_SMALL"] = self.old


def draw_a_frame(v):
    """Elevation of variant A-frame (no labels); returns the key coordinates."""
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
    cup_cell(v)
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
    m_section_a(v, labels=True)
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
    return bw, bd, bt, zb0, zbeam, xc, zp, r_sp, z_pom0, x_l


def draw_b_open(v):
    """Elevation of variant B-open (no labels); returns the key coordinates."""
    bw, bd, bt = p.BC_BASE
    zb = Z_S0 - p.BODY_BOTTOM
    rb, rc = p.BODY_D / 2, p.COLLAR_OD / 2
    v.rect(-rb - 20, zb - bt, -rb - 20 + bw, zb, fc=METAL, hatch="////")
    cup_cell(v)
    v.rect(-p.D_SAMPLE / 2, Z_S0, p.D_SAMPLE / 2, Z_S1, fc="#e9dcb8", lw=THIN)
    m_section_a(v, labels=True, cable_up=True)
    v.line([(-p.D_SAMPLE / 2, Z_S1 + 0.3), (p.D_SAMPLE / 2, Z_S1 + 0.3)], lw=1.4, c="#4a90d9", z=4.5)
    z_c = zb + p.COLLAR_TOP
    zcam = Z_S1 + p.BL_CAM_H
    bx, by, bz = 70.0, 70.0, 80.0
    # bracket: post on the base plate + arm over the cell
    xpost = rb + 50
    v.rect(xpost, zb, xpost + 20, zcam + bz / 2 + 20, fc="#d9dde1", lw=THIN)
    v.rect(-bx / 2 - 10, zcam + bz / 2 + 20, xpost + 20, zcam + bz / 2 + 40, fc="#d9dde1", lw=THIN)
    # camera box above the axis
    v.rect(-bx / 2, zcam - bz / 2, bx / 2, zcam + bz / 2 + 20, fc="#f3e7c9", lw=THICK, hatch="..")
    v.rect(-15, zcam - 10, 15, zcam + 30, fc="#2f3b45", lw=THIN, z=4)
    v.rect(-12, zcam - bz / 2 + 2, 12, zcam - 10, fc="#555", lw=THIN, z=4)
    v.rect(-14, zcam - bz / 2 - 2, 14, zcam - bz / 2, fc="#bfe3f5", lw=THIN, z=4.2)
    # field of view
    for s_ in (-1, 1):
        v.line([(s_ * 12, zcam - bz / 2), (s_ * 58, z_c)], lw=0.5, c="#2b62a3", ls="--")
    # laser (on the arm, at 45° to the surface centre)
    xl = p.BL_LASER_X
    zl = Z_S1 + p.BL_LASER_X / math.tan(math.radians(p.BL_LASER_ANG))
    v.rect(xl - 8, zl - 8, xl + 8, zl + 8, fc="#c0392b", lw=THIN, z=4)
    v.line([(xl - 6, zl - 6), (0, Z_S1)], lw=1.2, c="#e74c3c", z=4.6)
    v.line([(0, Z_S1), (-8, Z_S1 + 8)], lw=0.4, c="#e74c3c", ls=":")
    # heave shift illustration
    dh = 10.0
    v.line([(-p.D_SAMPLE / 2, Z_S1 + dh), (p.D_SAMPLE / 2, Z_S1 + dh)], lw=0.6, c="#4a90d9", ls="--", z=4.5)
    v.line([(xl - 6, zl - 6), (dh, Z_S1 + dh)], lw=0.6, c="#e74c3c", ls="--", z=4.6)
    v.dim_h(0, dh, Z_S1 + dh, Z_S1 + dh + 8, "Δx = Δh")
    return bw, bd, bt, zb, rb, rc, z_c, zcam, xl, zl, xpost


def _sheet_a_frame(pdf):
    sh = Sheet("Variant A-frame – piston fixed by an Al frame", "E7-V03", "≈ 1 : 2.2", 3,
               TOTAL, "blue = pressure, red = temperature, magenta = point M; dashed = behind")
    v = View(sh, 122, 44, 0.45)
    bw, bd, bt, zb0, zbeam, xc, zp, r_sp, z_pom0, x_l = draw_a_frame(v)
    rb = p.AM_PB[1]
    # labels right
    tag(v, 0, zbeam + p.AF_BEAM_H + 25, 150, zbeam + p.AF_BEAM_H + 45,
        "screw M16×1.5 + lock nut", INK)
    tag(v, 60, zbeam + 50, 150, zbeam + 20, "cross-beam Al 80×80", INK)
    tag(v, r_sp, z_pom0 + 7, 150, z_pom0 + 22, f"POM-C ⌀40×{p.AF_POM_T:g} (thermal comp.)", INK)
    tag(v, r_sp, zp + 25, 150, zp + 25, f"Al spacer ⌀40×{p.AF_SPACER_L:g}", INK)
    tag(v, x_l, zp + 35, 150, zp + 45, "LVDT DCTH400AG on the piston\n(post at −y, behind)", SENS_TXT)
    tag(v, 40, Z_S1 + 25, 150, Z_S1 + 5, "Al piston ⌀99.5 × 40", INK)
    tag(v, 0, Z_S1 - p.AM_PV[1], 150, Z_S1 - 25, "PV1  TML PDA-PA (depth 75)", PCOL)
    tag(v, -10, Z_S1 - 45, 150, Z_S1 - 55, "M: CS645 + fibre + Pt100 (depth 36–54)", "#d33682")
    tag(v, rb, Z_S0 - 1, 150, Z_S0 + 2, "PB1  TML PDA-PA, flush", PCOL)
    tag(v, 80, zb0 - 12, 150, zb0 - 50, f"Al base plate {bw:g}×{bd:g}×{bt:g}", INK)
    # labels left
    tag(v, -xc, zbeam - 40, -150, zbeam - 30, f"columns 40×80 × {p.AF_COL_H:g}", INK)
    tag(v, -R_IN - 4, Z_S0 + 50, -150, Z_S0 + 40, "printed cell ⌀160\n(V04)", INK)
    v.dim_v(zb0 - bt, zbeam + p.AF_BEAM_H, -xc - 30, -xc - 40, f"{p.AF_COL_H + p.AF_BEAM_H + bt:g}")
    v.dim_h(-xc, xc, zbeam + p.AF_BEAM_H, zbeam + p.AF_BEAM_H + 60, f"{p.COL_SPAN:g}")
    # right panel
    sh.heading(255, 276, "A-frame vs. A-min (tie rods)")
    rows = [["holds the piston", "frame 40×80 + 80×80, screw", "steel lid on 3 tie rods M10"],
            ["piston movement at 1 MPa", "≈ 0.08–0.15 mm", "≈ 0.11 mm"],
            ["thermal error (20 K)", "≈ 0 with POM-C insert", "≈ 12 µm"],
            ["access to the sample", "open sides, screw from top", "lid must be removed"],
            ["mechanics, EUR (≈)", "≈ 375–760", "≈ 330–670"],
            ["sensors to buy, EUR (≈)", "2 360–3 440 (same)", "2 360–3 440"]]
    y = table(sh, 255, 272, ["", "A-frame (this sheet)", "A-min (E7-V02)"], rows, [46, 58, 51], row_h=5.8)
    sh.heading(255, y - 9, "To buy (same sensors as A-min)")
    rows = []
    for tg_, what, typ, n, a, b, src, ch in sn.A_MIN_SENSORS:
        price = f"{n * a:,}" if a == b else f"{n * a:,}–{n * b:,}"
        rows.append([tg_ or "  +", typ, str(n), price.replace(",", " ") + (" *" if src == "web" else ""),
                     ch.replace(" VoltSE ±5 V", "").replace(" Therm109", "")])
    y = table(sh, 255, y - 13, ["tag", "type", "pcs", "EUR", "CR1000"], rows, [20, 60, 8, 23, 44], row_h=5.8)
    sh.text(255, y - 3,
            "* price found at a dealer (Oct 2026); others estimated – ask for quotes.\n"
            "Already available: TDR CS645 + reflectometer, Pt100, optical fibre (point M), CR1000.\n"
            "\n"
            "How it works\n"
            "• turn the screw until PV1 reads ≈ 5 kPa, lock the nut – the piston cannot move up;\n"
            "• freezing pressure is read by PV1 (in the sand) and PB1 (bottom); LVDT proves\n"
            "  the piston stays put (≈ 0.1 mm at 1 MPa, joints of the profiles dominate);\n"
            "• Al columns shrink more than the sand stack – the POM-C insert expands\n"
            "  the stack back (Δ ≈ 1 µm per 20 K), blank run with an Al dummy confirms it.\n"
            "Details: vypocty.md §10.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V03_variant_A_frame.png"))


def sheet_a_frame(pdf):
    with bigger_fonts():
        _sheet_a_frame(pdf)


def _sheet_cup(pdf):
    sh = Sheet("Cell A – printed body ⌀160 (Column_one_body_version_1)", "E7-V04", "1 : 1.25", 4, TOTAL,
               "per drawing M. Vrána 23.06.2026 + sensor sketch; z = 0 at the underside")
    rb, rc, ri, w = p.BODY_D / 2, p.COLLAR_OD / 2, p.CAV_D / 2, p.CUP_WALL_IN
    H, Hc, tb, zs = p.BODY_H, p.COLLAR_TOP, p.BODY_BOTTOM, p.SAND_TOP
    t = p.TDR_CS645
    z_top = Hc - t["top_from_collar"]
    v = View(sh, 118, 120, 0.8, "SECTION A–A  1 : 1.25 (port and sensors revolved)", (118, 277))
    # body
    for s_ in (-1, 1):
        v.rect(s_ * ri, tb, s_ * rb, H, fc=PETG, lw=THIN, hatch="..")
        v.rect(s_ * ri, H, s_ * rc, Hc, fc=PETG, lw=THIN)
        v.rect(s_ * ri, tb, s_ * (ri + w), Hc, fc=PETG, lw=THIN)
    v.rect(-rb, 0, rb, tb, fc=PETG, lw=THIN, hatch="..")
    v.rect(-rb, 0, rb, H, fc="none", lw=THICK)
    v.rect(-rc, H, rc, Hc, fc="none", lw=THICK)
    v.rect(-rb - 0.3, p.PORT_Z0, -ri, p.PORT_Z1, fc="white", lw=THIN)
    v.rect(-ri, tb, ri, zs, fc="#efe6cc", lw=0, z=1.5)
    v.line([(-ri, zs), (ri, zs)], lw=THIN, ls="--", c="#8a7a50")
    v.axis_line([(0, -6), (0, Hc + 8)])
    # sensors (light)
    for k in range(3):
        z = z_top - k * t["pitch"]
        v.line([(-ri, z), (-ri + t["rod_l"], z)], lw=1.4, c="#555", z=5)
    v.rect(-ri - w - t["head_l"], p.PORT_Z0 + 0.5, -ri, p.PORT_Z1 - 0.5, fc=TDRC, lw=THIN, z=5)
    v.line([(-ri, z_top + 2), (-ri + p.OF_TIP_FROM_WALL, z_top + 2)], lw=1.2, c=FBGC, z=5.2)
    v.rect(p.PT100_R - 1.5, zs - p.PT100_L, p.PT100_R + 1.5, zs - (p.PT100_L - p.PT100_METAL), fc=PTC, lw=0.5, z=5.2)
    v.line([(p.PT100_R, zs - (p.PT100_L - p.PT100_METAL)), (p.PT100_R, zs - 1), (rb, zs - 1)], lw=0.9, c="#8a7300", z=5.2)
    # holes for the optional thermistors / cables (revolved)
    for z_, lab in ((zs - p.AM_TEMPS[0][1], "T1"), ):
        v.rect(ri, z_ - 1, rb, z_ + 1, fc="white", lw=0.4)
    v.rect(-rb, zs - p.AM_TEMPS[1][1] - 1, -ri, zs - p.AM_TEMPS[1][1] + 1, fc="white", lw=0.4)
    v.rect(25 - 4.1, tb - 1.6, 25 + 4.1, tb, fc=PCOL, lw=THIN)
    v.rect(-p.PCELL_D / 2, zs - p.AM_PV[1] - 1, p.PCELL_D / 2, zs - p.AM_PV[1] + 1, fc=PCOL, lw=THIN, z=5)
    # dimensions
    v.dim_h(-rb, rb, 0, -10, "⌀160", side="below")
    v.dim_h(-rc, rc, Hc, Hc + 9, "⌀106")
    v.dim_h(-ri, ri, Hc, Hc + 18, "⌀100")
    v.dim_v(0, Hc, -rb, -rb - 34, f"{Hc:g}")
    v.dim_v(0, H, -rb, -rb - 24, f"{H:g}")
    v.dim_v(0, p.PORT_Z1, -rb, -rb - 14, f"{p.PORT_Z1:g}")
    v.dim_v(0, p.PORT_Z0, -rb, -rb - 6, f"{p.PORT_Z0:g}")
    v.dim_v(0, tb, rb, rb + 8, f"{tb:g}")
    v.dim_v(zs, Hc, rb, rb + 8, f"{Hc - zs:g}")
    v.dim_v(tb, zs, rb, rb + 18, "100 sand")
    v.dim_v(p.PORT_Z1, Hc, rb, rb + 30, f"{Hc - p.PORT_Z1:g}")
    v.dim_h(-ri, -ri + t["rod_l"], tb + 6, tb + 6, f"CS645 rods {t['rod_l']:g} (measured 77)")
    v.note(-ri + 30, z_top - t["pitch"], f"3 rods ⌀3.2, pitch {t['pitch']:g}", -40, 40, ha="left")
    v.note(-ri + 20, z_top + 2, f"optical fibre, tip {p.OF_TIP_FROM_WALL:g} from the wall", -40, 150, ha="left")
    v.note(p.PT100_R + 1.5, zs - 30, f"Pt100 {p.PT100_L:g} (metal {p.PT100_METAL:g}), r {p.PT100_R:g}", 40, 150, ha="left")
    v.note(-ri - 10, z_top - 4, f"TDR head {t['head_l']:g} in the port", -100, 175, ha="left")
    v.note(0, zs - p.AM_PV[1], f"PV1 (depth {p.AM_PV[1]:g})", 40, 40, ha="left")
    v.note(25, tb - 1, "PB1 flush, r 25", 40, 12, ha="left")
    v.note(ri + 2, Hc - 5, "free 34–35 for the piston", 60, 172, ha="left")
    # PLAN
    f = View(sh, 70, 52, 0.42, "PLAN  1 : 2.4", (70, 98))
    f.circle(0, 0, rb, fc=PETG, lw=THICK)
    f.circle(0, 0, rc, fc="none", lw=THIN)
    f.circle(0, 0, ri, fc="#efe6cc", lw=THIN)
    f.rect(-p.PORT_W / 2, -rb, p.PORT_W / 2, -ri - w, fc="white", lw=THICK)
    f.line([(0, -rb - 6), (0, ri + 10)], lw=THIN, ls=(0, (8, 2, 2, 2)), c=TDRC)
    for k in (-1, 0, 1):
        pass
    f.rect(-1.6, -ri, 1.6, -ri + t["rod_l"], fc="#777", lw=0.3)
    f.line([(-p.OF_SIDE, -ri), (-p.OF_SIDE, -ri + p.OF_TIP_FROM_WALL)], lw=1.2, c=FBGC)
    f.circle(p.PT100_R, 0, 2.2, fc=PTC, lw=THIN)
    f.circle(0, 0, p.PCELL_D / 2, fc="none", ec=PCOL, lw=THIN, ls="--")
    f.circle(25 * math.cos(math.radians(288)), 25 * math.sin(math.radians(288)), 4, fc=PCOL, lw=THIN, ls="--")
    f.text(0, -rb - 10, "port 13 wide (TDR axis)", fontsize=FS_SMALL, ha="center", va="top", color=TDRC)
    f.text(rb + 6, 0, "T1 0°", fontsize=FS_SMALL, va="center")
    f.text(-rb - 6, 0, "T2 180°", fontsize=FS_SMALL, va="center", ha="right")
    f.dim_h(-ri, ri, ri, rb + 6, "⌀100")
    # notes
    sh.heading(255, 276, "Sensors at point M (existing)")
    rows = [["TDR", "Campbell CS645", "rods 75 (77 meas.), pitch 8.9; head fills the port, rods centred in it"],
            ["OF", "optical fibre", f"horizontal at the top rod, tip {p.OF_TIP_FROM_WALL:g} from the wall"],
            ["Pt100", "37 mm (25 metal)", f"vertical from the sand surface, {p.PT100_R:g} from the axis"]]
    y = table(sh, 255, 272, ["", "sensor", "position"], rows, [16, 36, 103], row_h=5.8)
    sh.text(255, y - 4,
            "Depths below the sand surface (z = 126): rods 36 / 45 / 54,\n"
            "fibre ≈ 34, Pt100 metal 12–37 → all three sense the 35–55 mm layer.\n"
            "Open (sketch 7.7.26): does the Pt100 measure at the tip or along its length?\n"
            "\n"
            "Cable routes (to print or drill)\n"
            "• TDR head + coax and the fibre: through the side port 13 × 27\n"
            "• Pt100 cable: groove under the piston, ⌀4 hole at z ≈ 125 (0°)\n"
            f"• PV1: ⌀3.5 hole at z = {zs - p.AM_PV[1]:g} (90°); PB1: groove in the cavity floor\n"
            "  + ⌀3.5 hole through the jacket at 288°\n"
            "• optional T1 (depth 20, 0°), T2 (depth 80, 180°): ⌀2 holes\n"
            "\n"
            "Print (PrusaSlicer, MK4S): PETG(-CF), 0.2 mm, ≈ 600 g, 21 h\n"
            "• jacket 10 % infill = insulation (replaces Kaiflex)\n"
            "• recommended: 100 % infill under the cavity (z 0–26) – the bottom\n"
            "  carries the full freezing pressure (10 % gyroid crushes at ≈ 1–2 MPa)\n"
            "• wall ≈ 5 mm (≈ 8 perimeters) around the cavity: 3 mm alone sees\n"
            "  ≈ 3 MPa hoop stress at 200 kPa, ≈ 17 MPa at 1 MPa\n"
            "• epoxy coat + PTFE spray + silicone grease inside the cavity",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V04_cup_A.png"))


def sheet_cup(pdf):
    with bigger_fonts():
        _sheet_cup(pdf)


def _sheet_b_open(pdf):
    sh = Sheet("Variant B-open – open surface, laser line + camera", "E7-V06", "≈ 1 : 2.5", 6, TOTAL,
               "nothing on the sand: camera above, laser at 45°, rim = reference")
    v = View(sh, 112, 42, 0.42)
    bw, bd, bt, zb, rb, rc, z_c, zcam, xl, zl, xpost = draw_b_open(v)
    tag(v, 0, zcam + 10, 150, zcam + 40, "Raspberry Pi HQ + 12 mm lens, looking down\n(heated box +5 °C, double window)", INK)
    tag(v, xl, zl, 150, zl - 10, "line laser 650 nm, 45° from vertical", "#c0392b")
    tag(v, 30, Z_S1 + 0.3, 150, Z_S1 - 25, "OPEN sand surface – nothing on it", "#2b62a3")
    tag(v, rc - 2, z_c, 150, z_c + 15, "collar rim = reference (laser line in the same image)", INK)
    tag(v, xpost + 10, zb + 40, 150, zb + 20, "post + arm on the base plate", INK)
    tag(v, -10, Z_S1 - 45, -110, Z_S1 - 75, "M: CS645 + fibre\n+ Pt100 (existing)", "#d33682")
    tag(v, -rb + 5, Z_S0 + 20, -110, Z_S0 - 15, "printed cell ⌀160 (V04)", INK)
    tag(v, -rb, zb - 5, -110, zb - 40, f"Al plate {bw:g}×{bd:g}×{bt:g}", INK)
    # camera view
    c = View(sh, 330, 108, 0.62, "CAMERA VIEW (from above, ≈ 115 mm field)", (330, 152))
    c.rect(-62, -58, 62, 58, fc="#2a2a2a", lw=THIN)
    c.circle(0, 0, rc, fc="#cfd8dc", lw=THIN)
    c.circle(0, 0, p.CAV_D / 2, fc="#b9a888", lw=THIN)
    c.line([(-rc, -4), (-p.CAV_D / 2, -4)], lw=1.4, c="#ff4d4d")
    c.line([(p.CAV_D / 2, -4), (rc, -4)], lw=1.4, c="#ff4d4d")
    c.line([(-p.CAV_D / 2, 0), (p.CAV_D / 2, 0)], lw=1.4, c="#ff4d4d")
    c.line([(-p.CAV_D / 2, 6), (p.CAV_D / 2, 6)], lw=0.8, c="#ff4d4d", ls="--")
    c.circle(p.PT100_R, 0, 1.8, fc=PTC, lw=0.3)
    sh.text(330, 68, "laser line on the rim (reference) and on the sand;\n"
            "dashed = after heave → shift Δx = Δh along the whole profile", fontsize=FS_SMALL, ha="center", va="top",
            linespacing=1.4)
    sh.heading(255, 276, "To buy (EUR excl. VAT, ≈)")
    tr = {"zdroj": "PSU", "karta": "SD card", "objektiv": "lens", "nízké zkreslení": "low distortion",
          "čárový laser": "line laser", "třída": "class", "úhel": "fan", "vyhřívaný box": "heated box",
          "topná fólie": "heater foil", "termostat": "thermostat", "okénko 2× sklo": "double-glass window",
          "volitelně": "optional", "deska": "plate", "rameno nad celou: profil 20×20 (sloupek + výložník)":
          "post + arm over the cell (profile 20×20)", "2 referenční plíšky na límec (matně bílé) – kontrola":
          "2 matt-white reference tabs on the rim (check)"}
    def en(t_):
        for a_, b_ in tr.items():
            t_ = t_.replace(a_, b_)
        return t_
    rows = [[tg_ or "  +", en(what), f"{a_}–{b_}"] for tg_, what, n, a_, b_ in sn.B_CAM_BUY]
    rows += [["mech.", en(what), f"{a_}–{b_}"] for what, a_, b_ in sn.B_CAM_MECH]
    y = table(sh, 255, 272, ["tag", "item", "EUR"], rows, [16, 116, 23], row_h=5.6)
    lo = sum(a_ for *_, a_, b_ in sn.B_CAM_BUY) + sum(a_ for _, a_, b_ in sn.B_CAM_MECH)
    hi = sum(b_ for *_, a_, b_ in sn.B_CAM_BUY) + sum(b_ for _, a_, b_ in sn.B_CAM_MECH)
    sh.text(255, y - 4,
            f"Total ≈ {lo:.0f}–{hi:.0f} EUR (estimates). Already available: cell, CS645,\n"
            "Pt100, optical fibre, CR1000.\n"
            "\n"
            "≈ 28 µm/px, line centre to 0.1–0.3 px → ≈ 3–9 µm, realistic ≈ 10 µm\n"
            "Gives the whole surface profile; rim moves ≈ 120 µm / 20 K → blank run.\n"
            "Laser on only for the photo (every 10 min); clock synced with the CR1000.",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V06_variant_B_open.png"))


def sheet_b_open(pdf):
    with bigger_fonts():
        _sheet_b_open(pdf)


# --- overview, sensors, freezer layout ---------------------------------------------------
def _sheet_overview(pdf):
    sh = Sheet("E7 – overview: variant A (fixed) and B (free, open surface)", "E7-V01", "≈ 1 : 3", 1, TOTAL,
               "same sand, same printed cell ⌀160, same point M in both variants")
    a = View(sh, 72, 52, 0.30)
    bw, bd, bt, zb0, zbeam, xc, zp, r_sp, z_pom0, x_l = draw_a_frame(a)
    a.text(0, zbeam + p.AF_BEAM_H + 70, "A – sample held fixed", fontsize=FS + 1, weight="bold", ha="center")
    a.text(0, zb0 - bt - 40, "Al frame + screw, piston locked\nmeasures freezing PRESSURE (PV1, PB1)",
           fontsize=FS_SMALL, ha="center", va="top", linespacing=1.4)
    b = View(sh, 178, 52, 0.30)
    bw2, bd2, bt2, zb, rb, rc, z_c, zcam, xl, zl, xpost = draw_b_open(b)
    b.text(20, zcam + 110, "B – free, open surface", fontsize=FS + 1, weight="bold", ha="center")
    b.text(20, zb - bt2 - 40, "nothing on the sand; camera + laser line\nmeasure HEAVE and SETTLEMENT",
           fontsize=FS_SMALL, ha="center", va="top", linespacing=1.4)
    sh.heading(255, 276, "Comparison")
    rows = [["", "A (V03, alt. V02)", "B (V06, alt. V05)"],
            ["sample", "unsaturated sand ⌀100 × 100", "same"],
            ["cell", "printed body ⌀160 (V04)", "same"],
            ["top of the sample", "piston locked (screw)", "open, nothing on it"],
            ["main result", "freezing pressure", "heave / settlement"],
            ["measured by", "PV1, PB1 (TML PDA-PA)", "camera + line laser"],
            ["check", "LVDT: piston does not move", "rim = in-image reference"],
            ["point M (existing)", "CS645 + Pt100 + fibre", "same"],
            ["to buy, EUR (≈)", "2 750–4 200", "460–770"]]
    y = table(sh, 255, 272, rows[0], rows[1:], [42, 60, 53], row_h=5.8)
    sh.text(255, y - 5,
            "Sheets\n"
            "V01 overview · V02 A with lid on tie rods · V03 A with Al frame\n"
            "V04 printed cell + point M · V05 B with anchors (layer strain)\n"
            "V06 B open, camera + laser · V07 sensors + CR1000 · V08 freezer\n"
            "\n"
            "Common to both\n"
            "• freezer program −10 / +10 °C, freezing from the top (insulating body)\n"
            "• point M at 36–54 mm depth: unfrozen water (CS645) vs. T (Pt100, fibre)\n"
            "• blank run with an Al dummy sample before the first sand run\n"
            "• weigh the cell before and after each cycle",
            fontsize=FS_SMALL, va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V01_overview.png"))


def sheet_overview(pdf):
    with bigger_fonts():
        _sheet_overview(pdf)


def _sheet_sensors(pdf):
    sh = Sheet("Sensors and CR1000 wiring (A + B-open in one freezer)", "E7-V07", "–", 7, TOTAL,
               "existing = already in the lab; prices ≈ EUR excl. VAT, ask for quotes")
    sh.heading(28, 278, "Sensors")
    rows = [["A", "PV1, PB1", "freezing pressure in sand / at bottom", "TML PDA-PA 500 kPa [U]", "buy", "1 200–2 000"],
            ["A", "LVDT", "check: piston does not move", "RDP DCTH400AG ±10 mm", "buy", "581 + PSU"],
            ["A", "T1, T2", "sand temp. 20 / 80 mm (optional)", "Campbell 109SS-L", "buy", "360–520"],
            ["A, B", "M: TDR", "unfrozen water (36–54 mm)", "Campbell CS645 + TDR100/200", "existing", "–"],
            ["A, B", "M: Pt100", "reference temperature", "Pt100 37 mm, 4-wire", "existing", "–"],
            ["A, B", "M: OF", "temperature (optical fibre)", "optical fibre + reader", "existing", "–"],
            ["B", "CAM + LAS", "surface profile, heave", "RPi HQ camera + line laser", "buy", "460–770"],
            ["A, B", "Tair", "air temperature", "Campbell 109-L / 107", "buy", "150–220"]]
    y = table(sh, 28, 274, ["rig", "tag", "measures", "model", "status", "EUR"], rows, [14, 24, 66, 58, 20, 26],
              row_h=5.8)
    sh.heading(28, y - 8, "CR1000 channel plan (no multiplexer)")
    ch = [["DIFF1", "PV1 (A)", "BrFull, VX1 2000 mV"],
          ["DIFF2", "PB1 (A)", "BrFull, VX1 2000 mV"],
          ["DIFF3", "Pt100 (A) via 4WPB100", "BrHalf4W, VX2 2500 mV"],
          ["DIFF4", "Pt100 (B) via 4WPB100", "BrHalf4W, VX2 2500 mV"],
          ["SE9", "LVDT (A)", "VoltSE ±5000 mV, own ±15 V supply"],
          ["SE10, SE11", "T1, T2 (A, optional)", "Therm109, VX3"],
          ["SE12", "Tair", "Therm109, VX3"],
          ["C1–C3", "TDR100/200 → SDMX50", "2× CS645 (A and B), SDM"],
          ["12V, G", "TDR, LVDT supply via relay", ""],
          ["–", "optical fibre", "own interrogator, clock synced"],
          ["–", "camera + laser (B)", "Raspberry Pi, NTP-synced, laser on per photo"],
          ["SE13–16", "spare", ""]]
    table(sh, 28, y - 12, ["terminal", "connected to", "measurement"], ch, [26, 60, 122], row_h=5.6)
    sh.text(255, 276,
            "Notes\n"
            "• CR1000 outside the freezer (−25…+50 °C); cables through the lid seal.\n"
            "• PV1 and PB1 share VX1, the Pt100s share VX2 – the program\n"
            "  measures them in sequence.\n"
            "• CS645: one TDR instrument + SDMX50 multiplexer serves both cells.\n"
            "  In frozen sand it gives unfrozen water; calibrate in this sand.\n"
            "• Pt100 is the reference: check fibre and thermistors against it in the\n"
            "  cell at the ice point during thawing.\n"
            "• LVDT supply switched by the CR1000 (relay) – less heat in the freezer.\n"
            "• Camera + laser: Raspberry Pi in a heated box, photo every 10 min,\n"
            "  time stamps synced with the CR1000 (NTP).\n"
            "• Scan interval 10 min; 1 min during the phase change.\n"
            "• CR1000 is discontinued (successor CR1000X); the existing one suffices.",
            fontsize=FS_SMALL, va="top", linespacing=1.5)
    sh.save(pdf, os.path.join(OUT, "E7-V07_sensors_CR1000.png"))


def sheet_sensors(pdf):
    with bigger_fonts():
        _sheet_sensors(pdf)


def _sheet_layout(pdf):
    sh = Sheet("Both rigs in the chest freezer", "E7-V08", "1 : 5", 8, TOTAL,
               "same freezer as E6 (inside ≈ 900 × 550 × 650, to be measured); CR1000 + RPi outside")
    k = 0.2
    v = View(sh, 35, 160, k)
    v.text(10, 535, "PLAN  1 : 5", fontsize=FS + 1, weight="bold", va="top")
    v.rect(0, 0, p.FRZ_L, p.FRZ_W, fc="#f5f9fc", lw=THICK, z=1)
    tx0, ty0 = 50, 105
    v.rect(tx0, ty0, tx0 + p.TRAY_L, ty0 + p.TRAY_W, fc="#d6d9dc", lw=THIN, z=1.2)
    v.rect(620, 15, 885, 535, fc="none", lw=THIN, ls="--", z=1.3)
    v.text(752, 60, "floor step (if present)", fontsize=FS_SMALL - 1, ha="center")
    bwA, bdA, btA = p.AF_BASE
    ax, ay = tx0 + 10 + bwA / 2, ty0 + p.TRAY_W / 2
    v.rect(ax - bwA / 2, ay - bdA / 2, ax + bwA / 2, ay + bdA / 2, fc=METAL, lw=THIN, z=2)
    for s_ in (-1, 1):
        v.rect(ax + s_ * p.COL_SPAN / 2 - 20, ay - 40, ax + s_ * p.COL_SPAN / 2 + 20, ay + 40, fc="#d9dde1",
               lw=THIN, z=2.2)
    v.rect(ax - p.COL_SPAN / 2 - 20, ay - 40, ax + p.COL_SPAN / 2 + 20, ay + 40, fc="none", lw=THIN, ls="--", z=2.3)
    v.circle(ax, ay, p.BODY_D / 2, fc=PETG, lw=THIN, z_=2.1)
    v.circle(ax, ay, p.CAV_D / 2, fc="#e9dcb8", lw=THIN, z_=2.15)
    v.text(ax, ay, "A", fontsize=FS + 3, weight="bold", ha="center", va="center", zorder=5)
    bwB, bdB, btB = p.BC_BASE
    bx_, by_ = ax + bwA / 2 + 15 + bdB / 2, ty0 + p.TRAY_W / 2
    v.rect(bx_ - bdB / 2, by_ - bwB / 2, bx_ + bdB / 2, by_ + bwB / 2, fc=METAL, lw=THIN, z=2)
    cyB = by_ - bwB / 2 + 20 + p.BODY_D / 2
    v.circle(bx_, cyB, p.BODY_D / 2, fc=PETG, lw=THIN, z_=2.1)
    v.circle(bx_, cyB, p.CAV_D / 2, fc="#e9dcb8", lw=THIN, z_=2.15)
    v.rect(bx_ - 10, by_ + bwB / 2 - 35, bx_ + 10, by_ + bwB / 2 - 15, fc="#d9dde1", lw=THIN, z=2.2)
    v.line([(bx_, by_ + bwB / 2 - 25), (bx_, cyB)], lw=2, c="#9aa0a6", z=2.3)
    v.text(bx_, cyB, "B", fontsize=FS + 3, weight="bold", ha="center", va="center", zorder=5)
    v.dim_h(tx0, tx0 + p.TRAY_L, ty0, ty0 - 35, f"tray ≈ {p.TRAY_L:g} × {p.TRAY_W:g}", side="below")
    v.dim_h(ax - bwA / 2, bx_ + bdB / 2, ty0 + p.TRAY_W, ty0 + p.TRAY_W + 40, f"{bwA + 15 + bdB:g}")
    v.circle(560, 470, 9, fc="white", ec=TCOL, lw=THIN, z_=3)
    v.text(575, 470, "Tair", fontsize=FS_SMALL, color=TCOL, va="center")
    e = View(sh, 35, 22, k)
    e.text(10, 650, "ELEVATION  1 : 5", fontsize=FS + 1, weight="bold", va="top")
    e.rect(0, 0, p.FRZ_L, p.FRZ_H, fc="#f5f9fc", lw=THICK, z=1)
    e.line([(0, p.FRZ_H), (p.FRZ_L, p.FRZ_H)], lw=THICK, c=RED, ls="--")
    e.text(p.FRZ_L - 5, p.FRZ_H - 8, "lid", fontsize=FS_SMALL - 1, ha="right", va="top", color=RED)
    e.rect(25, 0, 610, 20, fc="#3a3a3a", lw=0, z=1.2)
    e.rect(tx0, 20, tx0 + p.TRAY_L, 60, fc="none", lw=THIN, z=1.3)
    e.rect(620, 0, 885, 230, fc="none", lw=THIN, ls="--", z=1.2)
    z0 = 60
    zA = z0 + 18 + btA
    e.rect(ax - bwA / 2, zA - btA, ax + bwA / 2, zA, fc=METAL, lw=THIN, z=2)
    for s_ in (-1, 1):
        e.rect(ax + s_ * p.COL_SPAN / 2 - 20, zA, ax + s_ * p.COL_SPAN / 2 + 20, zA + p.AF_COL_H, fc="#d9dde1",
               lw=THIN, z=2)
    e.rect(ax - p.COL_SPAN / 2 - 20, zA + p.AF_COL_H, ax + p.COL_SPAN / 2 + 20, zA + p.AF_COL_H + p.AF_BEAM_H,
           fc="#d9dde1", lw=THIN, z=2)
    e.rect(ax - p.BODY_D / 2, zA, ax + p.BODY_D / 2, zA + p.BODY_H, fc=PETG, lw=THIN, z=2.1)
    e.rect(ax - p.COLLAR_OD / 2, zA + p.BODY_H, ax + p.COLLAR_OD / 2, zA + p.COLLAR_TOP, fc=PETG, lw=THIN, z=2.1)
    topA = zA + p.AF_COL_H + p.AF_BEAM_H + 41
    e.rect(ax - 8, zA + p.AF_COL_H + p.AF_BEAM_H, ax + 8, topA, fc=STEEL, lw=THIN, z=2.2)
    e.text(ax, zA + 60, "A", fontsize=FS + 2, weight="bold", ha="center", va="center", zorder=5)
    zB = z0 + btB
    e.rect(bx_ - bdB / 2, zB - btB, bx_ + bdB / 2, zB, fc=METAL, lw=THIN, z=2)
    e.rect(bx_ - p.BODY_D / 2, zB, bx_ + p.BODY_D / 2, zB + p.BODY_H, fc=PETG, lw=THIN, z=2.1)
    e.rect(bx_ - p.COLLAR_OD / 2, zB + p.BODY_H, bx_ + p.COLLAR_OD / 2, zB + p.COLLAR_TOP, fc=PETG, lw=THIN, z=2.1)
    zcam = zB + p.BODY_BOTTOM + p.H_SAMPLE + p.BL_CAM_H
    topB = zcam + 80
    e.rect(bx_ - 35, zcam - 40, bx_ + 35, zcam + 60, fc="#f3e7c9", lw=THIN, z=2.2)
    e.rect(bx_ + 60, zB, bx_ + 80, topB, fc="#d9dde1", lw=THIN, z=2)
    e.rect(bx_ - 45, topB - 20, bx_ + 80, topB, fc="#d9dde1", lw=THIN, z=2)
    e.text(bx_, zB + 60, "B", fontsize=FS + 2, weight="bold", ha="center", va="center", zorder=5)
    top = max(topA, topB)
    e.dim_v(0, top, bx_ + bdB / 2 + 10, bx_ + bdB / 2 + 50, f"{top:.0f}")
    e.dim_v(0, p.FRZ_H, p.FRZ_L, p.FRZ_L + 25, f"≈ {p.FRZ_H:g}")
    sh.heading(255, 278, "Fit check")
    rows = [["base plates", f"A {bwA:g}×{bdA:g}, B {bdB:g}×{bwB:g}", f"{bwA + 15 + bdB:g} × {max(bdA, bwB):g}",
             "tray 530×340 OK"],
            ["rig A height", "frame + screw", f"{topA - z0:.0f} above tray", "OK"],
            ["rig B height", "camera arm", f"{topB - z0:.0f} above tray", "OK"],
            ["highest point", "above freezer floor", f"{top:.0f}", "inside ≈ 650 OK"],
            ["outside", "CR1000, TDR, RPi", "0…+40 °C", "keep dry"]]
    table(sh, 255, 274, ["item", "size", "value", "status"], rows, [28, 56, 36, 35], row_h=5.6)
    sh.text(255, 236,
            "Notes\n"
            "• Both rigs share the freezer program and the CR1000.\n"
            "• B is turned 90° (320 mm along the tray depth) so both fit the tray.\n"
            "• LED/laser of B only on for the photo; camera box ≥ 100 mm from A.\n"
            "• Run the blank test with Al dummies in both cells first.\n"
            "• Dimensions marked ≈ are estimates from the photos (E6) – measure.",
            fontsize=FS_SMALL, va="top", linespacing=1.5)
    sh.save(pdf, os.path.join(OUT, "E7-V08_freezer_layout.png"))


def sheet_layout(pdf):
    with bigger_fonts():
        _sheet_layout(pdf)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith((".png", ".pdf")):
            os.remove(os.path.join(OUT, f))
    with PdfPages(os.path.join(OUT, "E7_drawings.pdf")) as pdf:
        for fn in (sheet_overview, sheet_a_min, sheet_a_frame, sheet_cup, sheet_b_simple, sheet_b_open,
                   sheet_sensors, sheet_layout):
            fn(pdf)
