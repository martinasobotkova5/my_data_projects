"""E7 drawings – current design: variant C (dead weight on a partial piston, free surface),
deformation measured by (1) camera + line laser and (2) LVDT on the load.

Run: python vykresy_c.py → ../vykresy/E7_drawings.pdf + E7-V01…V05 PNG.
Earlier variants A and B are drawn by vykresy.py into ../vykresy/archiv/.
"""
import math
import os

from matplotlib.backends.backend_pdf import PdfPages

import params as p
import sensors as sn
import vykresy as V
from drafting import INK, METAL, RED, THICK, THIN, Sheet, View, table

OUT = V.OUT
TOTAL = 5
ZB0 = V.Z_S0 - p.BODY_BOTTOM                       # top of the base plate = underside of the cell
COL_H = p.BODY_BOTTOM + p.H_SAMPLE + p.C_BEAM_GAP
ZBEAM = ZB0 + COL_H
ZP = V.Z_S1 + p.C_PISTON_H                        # piston top
Z_ROD0 = ZP + p.C_BALL_D - 2
ZC = ZBEAM + p.AF_BEAM_H + p.C_TRAVEL + 10        # carrier underside
T1 = 1.0 / (math.pi / 4 * ((p.C_DISC_D / 1000) ** 2 - (p.C_DISC_HOLE / 1000) ** 2) * p.RHO_STEEL) * 1000
ZCAM = V.Z_S1 + p.C_CAM_H
YL, ZL = p.C_LASER_Y, V.Z_S1 + p.C_LASER_H
A_P = math.pi / 4 * p.C_PISTON_D ** 2
LASER = "#e74c3c"
FREE = "#2b62a3"


def fs():
    return V.FS_SMALL


def m_fixed():
    return (math.pi / 4 * (p.C_PISTON_D / 1000) ** 2 * p.C_PISTON_H / 1000 * 2700
            + math.pi / 4 * (p.C_ROD_D / 1000) ** 2 * (ZC - Z_ROD0) / 1000 * p.RHO_STEEL
            + math.pi / 4 * (p.C_CARRIER_D / 1000) ** 2 * p.C_CARRIER_T / 1000 * 2700 + 0.002)


def cam_rot(x, z):
    a = math.radians(p.C_CAM_TILT)
    return (p.C_CAM_Y + x * math.cos(a) - z * math.sin(a), ZCAM + x * math.sin(a) + z * math.cos(a))


def draw_c(v):
    """Side view (y–z through the axis) of rig C, no labels. Returns the top of the discs."""
    bw, bd, bt = p.AF_BASE
    v.rect(-bd / 2, ZB0 - bt, bd / 2, ZB0, fc=METAL, hatch="////")
    for xf in (-bd / 2 + 20, bd / 2 - 20):
        v.rect(xf - 8, ZB0 - bt - 18, xf + 8, ZB0 - bt, fc=V.STEEL, lw=THIN)
    v.rect(-40, ZB0, 40, ZBEAM, fc="#eceff1", lw=THIN, ls="--")
    v.rect(-40, ZBEAM, 40, ZBEAM + p.AF_BEAM_H, fc="#d9dde1", lw=THICK)
    bo, bl = p.C_BUSH
    v.rect(-bo / 2, ZBEAM + (p.AF_BEAM_H - bl) / 2, bo / 2, ZBEAM + (p.AF_BEAM_H + bl) / 2, fc=V.STEEL, lw=THIN,
           hatch="xx")
    V.cup_cell(v)
    v.rect(-p.D_SAMPLE / 2, V.Z_S0, p.D_SAMPLE / 2, V.Z_S1, fc="#e9dcb8", lw=THIN)
    V.m_section_a(v, labels=True, cable_up=True, pt_r=-p.C_PT100_R)
    # moving load
    v.rect(-p.C_PISTON_D / 2, V.Z_S1, p.C_PISTON_D / 2, ZP, fc=METAL, lw=THICK, hatch="////", z=5)
    v.circle(0, ZP + p.C_BALL_D / 2 - 1, p.C_BALL_D / 2, fc=V.STEEL, lw=THIN, z_=5.2)
    v.rect(-p.C_ROD_D / 2, Z_ROD0, p.C_ROD_D / 2, ZC, fc=V.STEEL, lw=THIN, z=5)
    v.rect(-p.C_CARRIER_D / 2, ZC, p.C_CARRIER_D / 2, ZC + p.C_CARRIER_T, fc=METAL, lw=THIN, hatch="////")
    z = ZC + p.C_CARRIER_T
    for _ in range(4):
        v.rect(-p.C_DISC_D / 2, z, p.C_DISC_D / 2, z + T1, fc="#8a8f96", lw=THIN, hatch="////")
        z += T1
    # (2) LVDT on the beam, plunger on the carrier underside
    xl = p.C_LVDT_X
    v.rect(xl - 9.5, ZBEAM + p.AF_BEAM_H, xl + 9.5, ZBEAM + p.AF_BEAM_H + 25, fc=V.SENS, lw=THIN)
    v.line([(xl, ZBEAM + p.AF_BEAM_H + 25), (xl, ZC)], lw=THICK)
    # (1) camera (−y) and line laser (+y)
    box_ = [cam_rot(-35, -40), cam_rot(35, -40), cam_rot(35, 40), cam_rot(-35, 40)]
    v.poly(box_, fc="#f3e7c9", lw=THICK)
    v.poly([cam_rot(-14, -40), cam_rot(14, -40), cam_rot(14, -52), cam_rot(-14, -52)], fc="#555", lw=THIN)
    v.rect(p.C_CAM_Y - 10, ZCAM + 45, -40, ZBEAM, fc=METAL, lw=THIN)
    c0 = cam_rot(0, -52)
    for xx in (-p.COLLAR_OD / 2 - 2, p.COLLAR_OD / 2 + 2):
        v.line([c0, (xx, ZB0 + p.COLLAR_TOP)], lw=0.5, c=FREE, ls="--")
    v.rect(YL - 2, ZB0, YL + 18, ZL + 8, fc="#d9dde1", lw=THIN, ls="--")
    v.rect(YL - 8, ZL - 8, YL + 8, ZL + 8, fc="#c0392b", lw=THIN, z=5)
    v.line([(YL - 6, ZL - 6), (0, V.Z_S1)], lw=1.0, c=LASER, z=4.6)
    for s_ in (-1, 1):
        v.line([(s_ * p.D_SAMPLE / 2, V.Z_S1 + 0.3), (s_ * p.C_PISTON_D / 2, V.Z_S1 + 0.3)], lw=1.6, c=FREE, z=4.6)
    v.line([(-p.C_CARRIER_D / 2 - 12, ZC - 15), (-p.C_CARRIER_D / 2 - 12, ZC + 40)], lw=1.2, c=RED)
    v.text(-p.C_CARRIER_D / 2 - 15, ZC + 12, "±25", fontsize=fs(), color=RED, ha="right", va="center")
    return z, box_


# --------------------------------------------------------------------------------------------
def _sheet_assembly(pdf):
    sh = Sheet("Rig C – dead weight on a partial piston, free surface", "E7-V01", "≈ 1 : 2.5", 1, TOTAL,
               "side view y–z through the axis; the Al frame only GUIDES the load")
    v = View(sh, 112, 34, 0.40)
    ztop, box_ = draw_c(v)
    bw, bd, bt = p.AF_BASE
    v.dim_v(ZB0, ZBEAM, -bd / 2, -bd / 2 - 18, f"{COL_H:g}")
    v.dim_v(V.Z_S1, ZBEAM, 50, 72, f"{p.C_BEAM_GAP:g}")
    v.dim_v(ZB0 - bt, ztop, bd / 2 + 10, bd / 2 + 30, f"{ztop - ZB0 + bt:.0f}")
    v.dim_h(-p.C_PISTON_D / 2, p.C_PISTON_D / 2, ZP, ZP + 12, "⌀50 piston")
    v.dim_h(-p.C_DISC_D / 2, p.C_DISC_D / 2, ztop, ztop + 12, "⌀120 discs")
    t = V.tag
    t(v, 0, ZC + p.C_CARRIER_T + 20, 140, ztop + 25, "dead weight: carrier + discs 1 kg\n(moves up and down)")
    t(v, 0, ZBEAM + 40, 140, ZBEAM + 55, "ball bushing LM12UU\n(guides only)")
    t(v, p.C_LVDT_X, ZBEAM + p.AF_BEAM_H + 12, 140, ZBEAM + 105, "(2) LVDT on the load", V.SENS_TXT)
    t(v, 0, V.Z_S1 + 60, 140, V.Z_S1 + 120, "guide rod ⌀12, ball ⌀8")
    t(v, 20, ZP - 5, 140, V.Z_S1 + 45, "partial piston ⌀50×20")
    t(v, 38, V.Z_S1 + 0.3, 140, V.Z_S1 + 5, "FREE surface (25 mm annulus)", FREE)
    t(v, YL, ZL, 140, ZL - 20, "(1) laser 45°, 11 lines\n(whole surface)", "#c0392b")
    t(v, -10, V.Z_S1 - 45, 140, V.Z_S1 - 45, "M: CS645 + fibre + Pt100", "#d33682")
    t(v, p.BODY_D / 2 - 5, V.Z_S0 + 10, 140, V.Z_S0 - 20, "printed cell ⌀160 (V03)")
    t(v, 60, ZB0 - 12, 140, ZB0 - 45, "Al plate 260×200×25")
    t(v, box_[0][0], box_[0][1], -150, ZCAM + 10, "(1) camera\nRPi HQ, 8 mm\nheated box", INK, ha="right")
    t(v, -40, V.Z_S1 + 75, -150, V.Z_S1 + 75, "columns 40×80\n(behind)", INK, ha="right")
    # right panel: load table + parts
    sh.heading(255, 276, "Load under the piston (⌀50 = 1963 mm²)")
    mf = m_fixed()
    rows = []
    for s_ in p.C_SURCHARGES_KPA:
        m = s_ * A_P / 1000 / 9.81
        n1 = int(max(m - mf, 0) // 1.0)
        rows.append([f"{s_:g}", f"{m:.2f}", str(n1), f"{m - mf - n1:.2f}"])
    y = table(sh, 255, 272, ["kPa", "total kg", "1 kg discs", "trim kg"], rows, [24, 30, 34, 30], row_h=5.6)
    sh.text(255, y - 3, f"moving part without discs ≈ {mf:.2f} kg ≈ {mf * 9.81 / A_P * 1000:.1f} kPa (minimum)",
            fontsize=fs())
    sh.heading(255, y - 14, "Parts")
    parts = [["1", "Al base plate 260×200×25, 3 levelling feet"],
             ["2", f"2 columns Al 40×80 × {COL_H:g}, cross-beam 80×80 × 260"],
             ["3", "ball bushing LM12UU in the beam, rod ⌀12 h6"],
             ["4", "partial piston Al ⌀50×20, steel ball ⌀8"],
             ["5", "carrier Al ⌀120×8, steel discs ⌀120 (1 kg)"],
             ["6", "printed cell ⌀160 + sand ⌀100×100 (V03)"],
             ["7", "(1) camera + 11-line laser on brackets (V02)"],
             ["8", "(2) LVDT RDP DCTH400AG on the beam (V02)"],
             ["9", "point M: CS645, Pt100, optical fibre (existing)"]]
    table(sh, 255, y - 18, ["#", "part"], parts, [8, 120], row_h=5.4)
    sh.save(pdf, os.path.join(OUT, "E7-V01_rig_C.png"))


# --------------------------------------------------------------------------------------------
def _sheet_measurement(pdf):
    sh = Sheet("Deformation measurement – (1) camera + laser, (2) LVDT", "E7-V02", "various", 2, TOTAL,
               "heave while freezing, settlement while thawing, residual per cycle")
    # (a) triangulation detail, y–z section near the surface, 1 : 1.25
    v = View(sh, 95, 168, 0.8, "(a) LASER TRIANGULATION – section y–z  1 : 1.25", (95, 278))
    ri, rc = p.CAV_D / 2, p.COLLAR_OD / 2
    zs = 0.0
    zc_top = p.COLLAR_TOP - p.SAND_TOP
    for s_ in (-1, 1):
        v.rect(s_ * ri, -30, s_ * rc, zc_top, fc=V.PETG, lw=THIN)
        v.rect(s_ * rc, -30, s_ * (rc + 20), 4, fc=V.PETG, lw=THIN, hatch="..")
    v.rect(-ri, -30, ri, zs, fc="#e9dcb8", lw=THIN)
    v.rect(-p.C_PISTON_D / 2, zs, p.C_PISTON_D / 2, p.C_PISTON_H, fc=METAL, lw=THICK, hatch="////")
    v.rect(-p.C_ROD_D / 2, p.C_PISTON_H + 6, p.C_ROD_D / 2, 70, fc=V.STEEL, lw=THIN)
    v.circle(0, p.C_PISTON_H + 3, 4, fc=V.STEEL, lw=THIN)
    dh = 8.0
    v.line([(-ri, zs + dh), (-p.C_PISTON_D / 2, zs + dh)], lw=0.8, c=FREE, ls="--")
    v.line([(p.C_PISTON_D / 2, zs + dh), (ri, zs + dh)], lw=0.8, c=FREE, ls="--")
    v.rect(-p.C_PISTON_D / 2, zs + dh, p.C_PISTON_D / 2, p.C_PISTON_H + dh, fc="none", lw=0.8, ls="--")
    # laser plane z = y (45°): a surface at height h is hit at y = h → seen by the camera shifted by h
    v.line([(95, 95), (p.C_PISTON_H, p.C_PISTON_H)], lw=1.2, c=LASER, z=5)
    v.line([(p.C_PISTON_H, p.C_PISTON_H), (0, 0)], lw=1.0, c=LASER, ls=":", z=5)
    for h, lab in ((0, "sand (|x| > 25): y = 0"), (p.C_PISTON_H, f"piston top: y = {p.C_PISTON_H:g}"),
                   (zc_top, f"rim (|x| ≈ 38): y = {zc_top:g}")):
        v.circle(h, h, 1.6, fc=LASER, lw=0, z_=6)
        v.text(h + 4, h - 2, lab, fontsize=fs(), color=LASER, va="top")
    v.circle(dh, dh, 1.6, fc="white", ec=LASER, lw=0.8, z_=6)
    v.dim_v(zs, zs + dh, -ri - 4, -ri - 16, "Δh")
    v.text(60, 98, "laser 45° from +y", fontsize=fs(), color=LASER)
    v.text(-ri + 2, -8, "sand", fontsize=fs())
    v.text(-p.C_PISTON_D / 2 + 2, p.C_PISTON_H / 2, "piston", fontsize=fs(), va="center")
    v.text(-rc - 18, zc_top + 4, "rim", fontsize=fs())
    v.text(-ri, -42, "heave Δh moves the hit point by Δy = Δh (open circle)", fontsize=fs(), color=LASER)
    # (b) camera view – 11 laser lines over the whole surface
    c = View(sh, 95, 62, 0.62, f"(b) CAMERA VIEW – {p.C_LINES} laser lines, whole surface", (95, 120))
    c.rect(-66, -66, 66, 66, fc="#2a2a2a", lw=THIN)
    c.circle(0, 0, rc, fc="#cfd8dc", lw=THIN)
    c.circle(0, 0, ri, fc="#b9a888", lw=THIN)
    c.circle(0, 0, p.C_PISTON_D / 2, fc="#9aa0a6", lw=THIN)
    c.circle(0, 0, p.C_ROD_D / 2, fc="#555", lw=THIN)
    rp = p.C_PISTON_D / 2
    n = p.C_LINES
    for k in range(n):
        y0 = (k - (n - 1) / 2) * p.C_LINE_PITCH          # where the line hits the sand (h = 0)
        # free sand: chord of the cavity minus the piston (the line hits sand at y = y0)
        if abs(y0) < ri:
            xs = math.sqrt(ri ** 2 - y0 ** 2)
            if abs(y0) < rp:
                xp_ = math.sqrt(rp ** 2 - y0 ** 2)
                segs = [(-xs, -xp_), (xp_, xs)]
            else:
                segs = [(-xs, xs)]
            for a_, b_ in segs:
                c.line([(a_, y0), (b_, y0)], lw=1.2, c="#ff4d4d", z=5)
        # piston top (h = 20): the same laser plane lands at y0 + 20
        yp_ = y0 + p.C_PISTON_H
        if abs(yp_) < rp:
            xx = math.sqrt(rp ** 2 - yp_ ** 2)
            c.line([(-xx, yp_), (xx, yp_)], lw=1.2, c="#ffb3b3", z=5)
        # rim (h = 34): short segments on the collar top
        yr = y0 + zc_top
        if ri < abs(yr) < rc:
            pass
        for sgn in (-1, 1):
            if abs(yr) < rc:
                x0_ = math.sqrt(max(ri ** 2 - yr ** 2, 0))
                x1_ = math.sqrt(rc ** 2 - yr ** 2)
                c.line([(sgn * x0_, yr), (sgn * x1_, yr)], lw=2.2, c="#ff4d4d", z=5)
    pa = math.radians(p.C_PT100_ANG)
    c.circle(p.C_PT100_R * math.cos(pa), p.C_PT100_R * math.sin(pa), 1.8, fc=V.PTC, lw=0.3)
    c.text(0, -62, "+y (laser) ↑   pitch 9 mm", fontsize=fs(), color="white", ha="center")
    V.tag(c, 46, 20, 75, 55, "rim = reference (fixed)", INK)
    V.tag(c, 40, -9, 75, 25, "free sand: 11 profiles", INK)
    V.tag(c, 10, 2, 75, -5, "piston top (light red)", INK)
    V.tag(c, -20, -50, 75, -35, "heave Δh: all lines shift by Δh", INK)
    # (c) LVDT
    l_ = View(sh, 213, 190, 0.38, "(c) LVDT ON THE LOAD  1 : 2.6", (213, 252))
    l_.rect(-60, 0, 60, 80, fc="#d9dde1", lw=THICK)
    l_.rect(-p.C_ROD_D / 2, -20, p.C_ROD_D / 2, 120, fc=V.STEEL, lw=THIN)
    l_.rect(-60, 115, 60, 115 + p.C_CARRIER_T, fc=METAL, lw=THIN, hatch="////")
    l_.rect(p.C_LVDT_X - 9.5, 80, p.C_LVDT_X + 9.5, 105, fc=V.SENS, lw=THIN)
    l_.line([(p.C_LVDT_X, 105), (p.C_LVDT_X, 115)], lw=THICK)
    l_.dim_v(80, 115, 60, 72, "35 (±10 range)")
    V.tag(l_, p.C_LVDT_X, 92, -40, -30, "LVDT DCTH400AG\nin the beam", V.SENS_TXT, ha="left")
    V.tag(l_, -40, 118, -40, -70, "carrier = piston\n(moves with the load)", INK, ha="left")
    # right panel
    sh.heading(255, 276, "What is measured")
    rows = [["(1) camera + 11 lines", "map h(x, y) of the whole surface", "≈ 10 µm", "every 10 / 1 min"],
            ["(2) LVDT", "carrier = piston", "≈ 1 µm", "CR1000, 10 / 1 min"]]
    y = table(sh, 255, 272, ["method", "signal", "resolution", "interval"], rows, [38, 56, 22, 36], row_h=5.6)
    sh.heading(255, y - 10, "Evaluation per freeze–thaw cycle")
    ev = [["surface map", "Δh(x, y) on 11 profiles → contour map, whole ⌀100"],
          ["heave, free surface", "mean Δh over the annulus (minus rim)"],
          ["heave under load", "Δh_load = LVDT (check: (1) on the piston)"],
          ["settlement on thawing", "drop from the maximum to the end of thaw"],
          ["residual per cycle", "height at end of thaw − start of cycle"],
          ["effect of the load", "Δh_free − Δh_load"],
          ["strain", "Δh / 100 mm"],
          ["frost depth", "0 °C isotherm from Pt100 / fibre / CS645 (M)"]]
    y = table(sh, 255, y - 14, ["quantity", "how"], ev, [44, 108], row_h=5.6)
    sh.text(255, y - 4,
            "Procedure\n"
            "1  blank run with an Al dummy sample: thermal drift of rim,\n"
            "   frame and LVDT (rim ≈ 120 µm / 20 K) → subtract\n"
            "2  calibrate (1): lift a dummy with a micrometer in 0.5 mm steps,\n"
            "   camera px → mm for free sand and piston top\n"
            "3  load, 24 h at +10 °C, then zero (1) and (2)\n"
            "4  freeze–thaw program; photo + LVDT every 10 min, 1 min\n"
            "   around 0 °C; laser on only for the photo\n"
            "5  weigh the cell before and after each cycle\n"
            "6  LVDT ±10 mm: re-clamp if the heave exceeds ≈ 8 mm",
            fontsize=fs(), va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V02_measurement.png"))


# --------------------------------------------------------------------------------------------
def _sheet_cell(pdf):
    sh = Sheet("Printed cell ⌀160 (Column_one_body_version_1) with point M", "E7-V03", "1 : 1.25", 3, TOTAL,
               "per drawing M. Vrána 23.06.2026; z = 0 at the underside; CAD: cad/E7_V04_cell.dxf")
    rb, rc, ri, w = p.BODY_D / 2, p.COLLAR_OD / 2, p.CAV_D / 2, p.CUP_WALL_IN
    H, Hc, tb, zs = p.BODY_H, p.COLLAR_TOP, p.BODY_BOTTOM, p.SAND_TOP
    t = p.TDR_CS645
    z_top = Hc - t["top_from_collar"]
    v = View(sh, 118, 120, 0.8, "SECTION A–A  1 : 1.25 (along the TDR axis)", (118, 277))
    for s_ in (-1, 1):
        v.rect(s_ * ri, tb, s_ * rb, H, fc=V.PETG, lw=THIN, hatch="..")
        v.rect(s_ * ri, H, s_ * rc, Hc, fc=V.PETG, lw=THIN)
        v.rect(s_ * ri, tb, s_ * (ri + w), Hc, fc=V.PETG, lw=THIN)
    v.rect(-rb, 0, rb, tb, fc=V.PETG, lw=THIN, hatch="..")
    v.rect(-rb, 0, rb, H, fc="none", lw=THICK)
    v.rect(-rc, H, rc, Hc, fc="none", lw=THICK)
    v.rect(-rb - 0.3, p.PORT_Z0, -ri, p.PORT_Z1, fc="white", lw=THIN)
    v.rect(-ri, tb, ri, zs, fc="#efe6cc", lw=0, z=1.5)
    v.line([(-ri, zs), (ri, zs)], lw=THIN, ls="--", c="#8a7a50")
    v.axis_line([(0, -6), (0, Hc + 8)])
    for k in range(3):
        z = z_top - k * t["pitch"]
        v.line([(-ri, z), (-ri + t["rod_l"], z)], lw=1.4, c="#555", z=5)
    v.rect(-ri - w - t["head_l"], p.PORT_Z0 + 0.5, -ri, p.PORT_Z1 - 0.5, fc=V.TDRC, lw=THIN, z=5)
    v.line([(-ri, z_top + 2), (-ri + p.OF_TIP_FROM_WALL, z_top + 2)], lw=1.2, c=V.FBGC, z=5.2)
    xpt = p.C_PT100_R
    v.rect(xpt - 1.5, zs - p.PT100_L, xpt + 1.5, zs - (p.PT100_L - p.PT100_METAL), fc=V.PTC, lw=0.5, z=5.2)
    v.line([(xpt, zs - (p.PT100_L - p.PT100_METAL)), (xpt, Hc + 10)], lw=0.9, c="#8a7300", z=5.2)
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
    v.dim_h(-ri, -ri + t["rod_l"], tb + 6, tb + 6, f"CS645 rods {t['rod_l']:g}")
    v.dim_h(0, xpt, zs - p.PT100_L - 4, zs - p.PT100_L - 10, f"{xpt:g}", side="below")
    V.tag(v, -ri + 30, z_top - t["pitch"], 60, -26, f"3 rods ⌀3.2, pitch {t['pitch']:g}")
    V.tag(v, -ri + 20, z_top + 2, -60, 152, f"optical fibre, tip {p.OF_TIP_FROM_WALL:g} from the wall", V.FBGC)
    V.tag(v, xpt + 1.5, zs - 20, 100, 150, f"Pt100 {p.PT100_L:g} (metal {p.PT100_METAL:g})\nr {xpt:g}, 315°, cable up",
          "#8a7300")
    V.tag(v, -ri - 10, z_top - 4, -100, 175, f"TDR head {t['head_l']:g} in the port", V.TDRC, ha="left")
    f = View(sh, 70, 52, 0.42, "PLAN  1 : 2.4", (70, 98))
    f.circle(0, 0, rb, fc=V.PETG, lw=THICK)
    f.circle(0, 0, rc, fc="none", lw=THIN)
    f.circle(0, 0, ri, fc="#efe6cc", lw=THIN)
    f.rect(-p.PORT_W / 2, -rb, p.PORT_W / 2, -ri - w, fc="white", lw=THICK)
    f.line([(0, -rb - 6), (0, ri + 10)], lw=THIN, ls=(0, (8, 2, 2, 2)), c=V.TDRC)
    f.rect(-1.6, -ri, 1.6, -ri + t["rod_l"], fc="#777", lw=0.3)
    f.line([(-p.OF_SIDE, -ri), (-p.OF_SIDE, -ri + p.OF_TIP_FROM_WALL)], lw=1.2, c=V.FBGC)
    pa = math.radians(p.C_PT100_ANG)
    f.circle(p.C_PT100_R * math.cos(pa), p.C_PT100_R * math.sin(pa), 2.2, fc=V.PTC, lw=THIN)
    f.circle(0, 0, p.C_PISTON_D / 2, fc="none", ec=INK, lw=THIN, ls="--")
    f.line([(-ri, 0), (ri, 0)], lw=1.0, c=LASER, ls="--")
    f.text(0, -rb - 10, "port 13 wide (TDR axis, camera side)", fontsize=fs(), ha="center", va="top", color=V.TDRC)
    f.text(rb + 6, 0, "laser line", fontsize=fs(), va="center", color=LASER)
    sh.heading(255, 276, "Point M (existing sensors)")
    rows = [["TDR", "Campbell CS645", "3 rods 75, pitch 8.9, in the port, depth 36/45/54"],
            ["OF", "optical fibre", f"at the top rod, tip {p.OF_TIP_FROM_WALL:g} from the wall"],
            ["Pt100", "37 mm (25 metal)", "vertical, r 37.5 at 315° (free annulus, off the laser)"]]
    y = table(sh, 255, 272, ["", "sensor", "position"], rows, [16, 36, 103], row_h=5.8)
    sh.text(255, y - 4,
            "• The piston ⌀50 (dashed) covers the centre; the Pt100 sits in the free\n"
            "  annulus on the camera side so it never crosses the laser line.\n"
            "• Sand 100 mm (z 26–126), 34 mm free above (piston 20 + travel).\n"
            "• Print: PETG(-CF) 0.2 mm, jacket 10 % infill = insulation; 100 % infill\n"
            "  under the cavity, cavity wall ≈ 5 mm (≈ 8 perimeters).\n"
            "• Inside: epoxy coat + PTFE spray + silicone grease.\n"
            "• Cables: TDR head + fibre through the port, Pt100 straight up.\n"
            "• Full dimensions: cad/E7_V04_cell.dxf.",
            fontsize=fs(), va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V03_cell.png"))


# --------------------------------------------------------------------------------------------
def _sheet_sensors(pdf):
    sh = Sheet("Sensors, CR1000 wiring and costs", "E7-V04", "–", 4, TOTAL,
               "existing = already in the lab; prices ≈ EUR excl. VAT, * = dealer price found, rest estimated")
    sh.heading(28, 278, "To buy")
    rows = []
    for tg_, what, n, a, b, src, ch in sn.C_BUY:
        price = f"{n * a}" if a == b else f"{n * a}–{n * b}"
        rows.append([tg_ or "  +", what, price + (" *" if src.startswith("web") else ""), ch])
    y = table(sh, 28, 274, ["tag", "item", "EUR", "CR1000"], rows, [18, 112, 26, 52], row_h=5.6)
    sh.heading(28, y - 8, "Mechanics (estimate)")
    rows = [[what, f"{a}–{b}"] for what, a, b in sn.C_MECH]
    y2 = table(sh, 28, y - 12, ["item", "EUR"], rows, [130, 26], row_h=5.6)
    lo = sum(n * a for _, _, n, a, b, _, _ in sn.C_BUY) + sum(a for _, a, b in sn.C_MECH)
    hi = sum(n * b for _, _, n, a, b, _, _ in sn.C_BUY) + sum(b for _, a, b in sn.C_MECH)
    sh.text(28, y2 - 5, f"Total ≈ {lo}–{hi} EUR excl. VAT (≈ {lo * 25 / 1000:.0f}–{hi * 25 / 1000:.0f} tis. Kč). "
            "Already available: printed cell, CS645 + TDR100/200, Pt100, optical fibre, CR1000.",
            fontsize=fs(), weight="bold")
    sh.heading(255, 278, "CR1000 channel plan")
    ch = [["SE1", "(2) LVDT", "VoltSE ±5000 mV"],
          ["DIFF1", "Pt100 via 4WPB100", "BrHalf4W, VX2 2500 mV"],
          ["SE3", "Tair (optional)", "Therm109, VX1"],
          ["C1–C3", "TDR100/200 → CS645", "SDM"],
          ["C4", "relay: LVDT supply", "on for the scan"],
          ["–", "(1) camera + laser", "Raspberry Pi, NTP"],
          ["–", "optical fibre", "own reader"]]
    y = table(sh, 255, 274, ["terminal", "connected to", "measurement"], ch, [24, 56, 75], row_h=5.6)
    sh.text(255, y - 4,
            "Notes\n"
            "• CR1000, TDR and RPi outside the freezer;\n"
            "  cables and the camera USB/CSI cable through the lid seal.\n"
            "• Scan 10 min, 1 min around 0 °C; RPi photo at the\n"
            "  same time stamps (CR1000 sets a flag / NTP).\n"
            "• No pressure cells: the load is a known dead weight.",
            fontsize=fs(), va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V04_sensors_costs.png"))


# --------------------------------------------------------------------------------------------
def _sheet_layout(pdf):
    sh = Sheet("Rig C in the chest freezer", "E7-V05", "1 : 5", 5, TOTAL,
               "same freezer as E6 (inside ≈ 900 × 550 × 650, to be measured); CR1000 + RPi outside")
    k = 0.2
    v = View(sh, 35, 160, k)
    v.text(10, 535, "PLAN  1 : 5", fontsize=V.FS + 1, weight="bold", va="top")
    v.rect(0, 0, p.FRZ_L, p.FRZ_W, fc="#f5f9fc", lw=THICK, z=1)
    tx0, ty0 = 50, 105
    v.rect(tx0, ty0, tx0 + p.TRAY_L, ty0 + p.TRAY_W, fc="#d6d9dc", lw=THIN, z=1.2)
    v.rect(620, 15, 885, 535, fc="none", lw=THIN, ls="--", z=1.3)
    v.text(752, 60, "floor step (if present)", fontsize=fs() - 1, ha="center")
    bw, bd, bt = p.AF_BASE
    ax, ay = tx0 + p.TRAY_L / 2, ty0 + p.TRAY_W / 2
    v.rect(ax - bw / 2, ay - bd / 2, ax + bw / 2, ay + bd / 2, fc=METAL, lw=THIN, z=2)
    for s_ in (-1, 1):
        v.rect(ax + s_ * p.COL_SPAN / 2 - 20, ay - 40, ax + s_ * p.COL_SPAN / 2 + 20, ay + 40, fc="#d9dde1",
               lw=THIN, z=2.2)
    v.rect(ax - p.COL_SPAN / 2 - 20, ay - 40, ax + p.COL_SPAN / 2 + 20, ay + 40, fc="none", lw=THIN, ls="--", z=2.3)
    v.circle(ax, ay, p.BODY_D / 2, fc=V.PETG, lw=THIN, z_=2.1)
    v.circle(ax, ay, p.CAV_D / 2, fc="#e9dcb8", lw=THIN, z_=2.15)
    v.circle(ax, ay, p.C_DISC_D / 2, fc="none", ec=INK, lw=THIN, ls="--", z_=2.4)
    v.rect(ax - 35, ay + p.C_CAM_Y - 35, ax + 35, ay + p.C_CAM_Y + 35, fc="#f3e7c9", lw=THIN, z=2.5)
    v.rect(ax - 8, ay + YL - 8, ax + 8, ay + YL + 8, fc="#c0392b", lw=THIN, z=2.5)
    v.text(ax, ay, "C", fontsize=V.FS + 3, weight="bold", ha="center", va="center", zorder=5)
    v.dim_h(tx0, tx0 + p.TRAY_L, ty0, ty0 - 35, f"tray ≈ {p.TRAY_L:g} × {p.TRAY_W:g}", side="below")
    v.dim_h(ax - bw / 2, ax + bw / 2, ty0 + p.TRAY_W, ty0 + p.TRAY_W + 40, f"{bw:g}")
    e = View(sh, 35, 22, k)
    e.text(10, 650, "ELEVATION  1 : 5", fontsize=V.FS + 1, weight="bold", va="top")
    e.rect(0, 0, p.FRZ_L, p.FRZ_H, fc="#f5f9fc", lw=THICK, z=1)
    e.line([(0, p.FRZ_H), (p.FRZ_L, p.FRZ_H)], lw=THICK, c=RED, ls="--")
    e.text(p.FRZ_L - 5, p.FRZ_H - 8, "lid", fontsize=fs() - 1, ha="right", va="top", color=RED)
    e.rect(25, 0, 610, 20, fc="#3a3a3a", lw=0, z=1.2)
    e.rect(tx0, 20, tx0 + p.TRAY_L, 60, fc="none", lw=THIN, z=1.3)
    e.rect(620, 0, 885, 230, fc="none", lw=THIN, ls="--", z=1.2)
    z0 = 60 + 18 + bt                                  # top of the base plate
    e.rect(ax - bw / 2, z0 - bt, ax + bw / 2, z0, fc=METAL, lw=THIN, z=2)
    for s_ in (-1, 1):
        e.rect(ax + s_ * p.COL_SPAN / 2 - 20, z0, ax + s_ * p.COL_SPAN / 2 + 20, z0 + COL_H, fc="#d9dde1", lw=THIN, z=2)
    e.rect(ax - p.COL_SPAN / 2 - 20, z0 + COL_H, ax + p.COL_SPAN / 2 + 20, z0 + COL_H + p.AF_BEAM_H, fc="#d9dde1",
           lw=THIN, z=2)
    e.rect(ax - p.BODY_D / 2, z0, ax + p.BODY_D / 2, z0 + p.BODY_H, fc=V.PETG, lw=THIN, z=2.1)
    e.rect(ax - p.COLLAR_OD / 2, z0 + p.BODY_H, ax + p.COLLAR_OD / 2, z0 + p.COLLAR_TOP, fc=V.PETG, lw=THIN, z=2.1)
    zc = z0 + (ZC - ZB0)
    top = zc + p.C_CARRIER_T + 4 * T1
    e.rect(ax - p.C_DISC_D / 2, zc, ax + p.C_DISC_D / 2, top, fc="#8a8f96", lw=THIN, z=2.2)
    e.rect(ax - 6, z0 + p.BODY_BOTTOM + p.H_SAMPLE, ax + 6, zc, fc=V.STEEL, lw=THIN, z=2.15)
    e.text(ax, z0 + 60, "C", fontsize=V.FS + 2, weight="bold", ha="center", va="center", zorder=5)
    e.dim_v(0, top, ax + bw / 2 + 10, ax + bw / 2 + 50, f"{top:.0f}")
    e.dim_v(0, p.FRZ_H, p.FRZ_L, p.FRZ_L + 25, f"≈ {p.FRZ_H:g}")
    sh.heading(255, 278, "Fit check")
    rows = [["base plate", f"{bw:g} × {bd:g}", "tray ≈ 530 × 340", "OK"],
            ["rig height", "plate + frame + discs", f"{top - 60:.0f} above tray", "check"],
            ["highest point", "above freezer floor", f"{top:.0f}", f"≈ {p.FRZ_H - top:.0f} spare"],
            ["load travel", "± 25 mm above the beam", f"max {top + 25:.0f}", "lid closes?"]]
    table(sh, 255, 274, ["item", "size", "value", "status"], rows, [30, 50, 40, 35], row_h=5.6)
    sh.text(255, 242,
            "Notes\n"
            "• The free end of the freezer stays empty (cable bundle, a second rig).\n"
            "• Highest point is the disc stack; with 4 discs ≈ 50 mm under the lid –\n"
            "  measure the freezer and the tray before ordering the profiles.\n"
            "• Camera box and laser hang inside the frame – nothing outside the plate.\n"
            "• Run the blank test with the Al dummy first.",
            fontsize=fs(), va="top", linespacing=1.5)
    sh.save(pdf, os.path.join(OUT, "E7-V05_freezer_layout.png"))


def run(fn):
    old = V.TAG_BOX
    V.TAG_BOX = False
    try:
        with V.bigger_fonts(10.5, 9.5):
            fn(pdf)
    finally:
        V.TAG_BOX = old


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith((".png", ".pdf")):
            os.remove(os.path.join(OUT, f))
    with PdfPages(os.path.join(OUT, "E7_drawings.pdf")) as pdf:
        for fn in (_sheet_assembly, _sheet_measurement, _sheet_cell, _sheet_sensors, _sheet_layout):
            run(fn)
