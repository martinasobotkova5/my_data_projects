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
ZCELL = V.Z_S0 - p.BODY_BOTTOM                     # underside of the cell
ZB0 = ZCELL - p.C_INS_T                            # top of the base plate (rev. B: printed base + G10 pads)
COL_H = p.C_INS_T + p.BODY_BOTTOM + p.H_SAMPLE + p.C_BEAM_GAP
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
XPS = "#dbe8f3"
G10 = "#9bbf6a"
RO = p.BODY_D / 2 + p.C_SLEEVE_T                   # outer radius of the one-piece printed cell
Z_LV = ZC - 35                                     # LVDT body (25 long) under the carrier
TAN_L = math.tan(math.radians(p.C_LASER_ANG))      # laser line shift Δy = Δh / tan 68°


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
    bw, bd, bt = p.C_BASE
    v.rect(-bd / 2, ZB0 - bt, bd / 2, ZB0, fc=METAL, hatch="////")
    # rev. B: the cell is printed in one piece with its insulation (low-infill base + wall), G10 pads in pockets
    v.rect(-RO, ZB0, RO, ZCELL, fc=V.PETG, lw=THIN, hatch="..")
    for a in (90, 210):
        yy = p.C_PAD_R * math.sin(math.radians(a)) if a == 90 else -p.C_PAD_R / 2
        v.rect(yy - p.C_PAD_D / 2, ZB0, yy + p.C_PAD_D / 2, ZCELL, fc=G10, lw=THIN, z=2.2)
    for s_ in (-1, 1):
        v.rect(s_ * p.BODY_D / 2, ZCELL, s_ * RO, ZCELL + p.BODY_H, fc=V.PETG, lw=THIN, hatch="..")
        v.line([(s_ * p.BODY_D / 2, ZCELL), (s_ * p.BODY_D / 2, ZCELL + p.BODY_H)], lw=0.4, c="#9aa5ab", ls=":", z=2.3)
    v.poly([(-RO, ZB0), (RO, ZB0), (RO, ZCELL + p.BODY_H), (-RO, ZCELL + p.BODY_H)], fc="none", lw=THICK, z=2.4)
    for xf in (-bd / 2 + 20, bd / 2 - 20):
        v.rect(xf - 8, ZB0 - bt - 18, xf + 8, ZB0 - bt, fc=V.STEEL, lw=THIN)
    v.rect(-40, ZB0, 40, ZBEAM, fc="#eceff1", lw=THIN, ls="--", z=1.2)
    v.rect(-40, ZBEAM, 40, ZBEAM + p.AF_BEAM_H, fc="#d9dde1", lw=THICK)
    bo, bl = p.C_BUSH
    v.rect(-bo / 2, ZBEAM + (p.AF_BEAM_H - bl) / 2, bo / 2, ZBEAM + (p.AF_BEAM_H + bl) / 2, fc=V.STEEL, lw=THIN,
           hatch="xx")
    V.cup_cell(v)
    # one piece: the core outline is not an edge of the print (draw it as a hint only)
    for s_ in (-1, 1):
        v.line([(s_ * p.BODY_D / 2, ZCELL), (s_ * p.BODY_D / 2, ZCELL + p.BODY_H)], lw=THICK + 0.6, c=V.PETG, z=2.45)
        v.line([(s_ * p.BODY_D / 2, ZCELL), (s_ * p.BODY_D / 2, ZCELL + p.BODY_H)], lw=0.4, c="#9aa5ab", ls=":", z=2.46)
    v.line([(-p.BODY_D / 2, ZCELL), (p.BODY_D / 2, ZCELL)], lw=THICK + 0.6, c=V.PETG, z=2.45)
    v.line([(-p.BODY_D / 2, ZCELL), (p.BODY_D / 2, ZCELL)], lw=0.4, c="#9aa5ab", ls=":", z=2.46)
    v.rect(-p.D_SAMPLE / 2, V.Z_S0, p.D_SAMPLE / 2, V.Z_S1, fc="#e9dcb8", lw=THIN)
    V.m_section_a(v, labels=True, cable_up=True, pt_port=True)
    # moving load
    v.rect(-p.C_PISTON_D / 2, V.Z_S1, p.C_PISTON_D / 2, ZP, fc=METAL, lw=THICK, hatch="////", z=5)
    v.circle(0, ZP + p.C_BALL_D / 2 - 1, p.C_BALL_D / 2, fc=V.STEEL, lw=THIN, z_=5.2)
    v.rect(-p.C_ROD_D / 2, Z_ROD0, p.C_ROD_D / 2, ZC, fc=V.INVAR, lw=THIN, z=5)
    v.rect(-p.C_CARRIER_D / 2, ZC, p.C_CARRIER_D / 2, ZC + p.C_CARRIER_T, fc=METAL, lw=THIN, hatch="////")
    z = ZC + p.C_CARRIER_T
    for _ in range(4):
        v.rect(-p.C_DISC_D / 2, z, p.C_DISC_D / 2, z + T1, fc="#8a8f96", lw=THIN, hatch="////")
        z += T1
    # (2) LVDT on an arm of the Invar post (x = −95, beside the sleeve), plunger on the carrier underside
    yl_, yi, yr = p.C_LVDT_XY[1], p.C_INVAR_XY[1], p.C_REF_XY[1]
    v.rect(yi - p.C_INVAR_D / 2, ZB0, yi + p.C_INVAR_D / 2, Z_LV, fc=V.INVAR, lw=THIN, z=4.8)
    v.rect(yl_, Z_LV - 6, yi, Z_LV, fc=V.INVAR, lw=THIN, z=4.8)
    v.rect(yl_ - 9.5, Z_LV, yl_ + 9.5, Z_LV + 25, fc=V.SENS, lw=THIN, z=4.9)
    v.line([(yl_, Z_LV + 25), (yl_, ZC)], lw=THICK, z=4.9)
    z_rim = ZCELL + p.COLLAR_TOP
    v.rect(yr, z_rim, yi, z_rim + 3, fc=V.INVAR, lw=THIN, z=4.8)
    v.rect(yr - 5, z_rim + 3, yr + 5, z_rim + 4.5, fc="white", lw=THIN, z=4.85)
    # (1) camera + RPi 5 in one box (−y) and line laser (+y) hanging from the beam
    box_ = [cam_rot(-50, -35), cam_rot(50, -35), cam_rot(50, 35), cam_rot(-50, 35)]
    v.poly(box_, fc="#f3e7c9", lw=THICK)
    v.poly([cam_rot(-14, -35), cam_rot(14, -35), cam_rot(14, -47), cam_rot(-14, -47)], fc="#555", lw=THIN)
    v.rect(p.C_CAM_Y - 8, ZCAM + 30, -40, ZBEAM, fc=METAL, lw=THIN)
    c0 = cam_rot(0, -47)
    for xx in (-p.COLLAR_OD / 2 - 2, p.COLLAR_OD / 2 + 2):
        v.line([c0, (xx, ZCELL + p.COLLAR_TOP)], lw=0.5, c=FREE, ls="--")
    v.rect(40, ZL - 6, 43, ZBEAM, fc=METAL, lw=THIN)
    v.rect(YL - 5, ZL - 5, YL + 5, ZL + 5, fc="#c0392b", lw=THIN, z=5)
    v.line([(YL, ZL), (0, V.Z_S1)], lw=1.0, c=LASER, z=4.6)
    for s_ in (-1, 1):
        v.line([(s_ * p.D_SAMPLE / 2, V.Z_S1 + 0.3), (s_ * p.C_PISTON_D / 2, V.Z_S1 + 0.3)], lw=1.6, c=FREE, z=4.6)
    v.line([(-p.C_CARRIER_D / 2 - 12, ZC - 15), (-p.C_CARRIER_D / 2 - 12, ZC + 40)], lw=1.2, c=RED)
    v.text(-p.C_CARRIER_D / 2 - 15, ZC + 12, "±25", fontsize=fs(), color=RED, ha="right", va="center")
    return z, box_


# --------------------------------------------------------------------------------------------
def _sheet_assembly(pdf):
    sh = Sheet("Rig C rev. B – dead weight on a partial piston, free surface", "E7-V01", "≈ 1 : 2.5", 1, TOTAL,
               "side view y–z through the axis; the Al frame only GUIDES the load; rev. B per measurement review")
    v = View(sh, 112, 34, 0.40)
    ztop, box_ = draw_c(v)
    bw, bd, bt = p.C_BASE
    v.dim_v(ZB0, ZBEAM, -bd / 2, -bd / 2 - 18, f"{COL_H:g}")
    v.dim_v(V.Z_S1, ZBEAM, 50, 72, f"{p.C_BEAM_GAP:g}")
    v.dim_v(ZB0 - bt, ztop, bd / 2 + 10, bd / 2 + 30, f"{ztop - ZB0 + bt:.0f}")
    v.dim_h(-p.C_PISTON_D / 2, p.C_PISTON_D / 2, ZP, ZP + 12, "⌀50 piston")
    v.dim_h(-p.C_DISC_D / 2, p.C_DISC_D / 2, ztop, ztop + 12, "⌀120 discs")
    t = V.tag
    t(v, 0, ZC + p.C_CARRIER_T + 20, 172, ztop + 25, "dead weight: carrier + discs 1 kg\n(moves up and down)")
    t(v, 0, ZBEAM + 40, 172, ZBEAM + 50, "plain bearing igus drylin\nRJ4JP-01-12 (no grease)")
    t(v, p.C_LVDT_XY[1], Z_LV + 12, 172, ZBEAM + 95, "(2) LVDT on the Invar arm", V.SENS_TXT)
    t(v, 0, V.Z_S1 + 90, 172, ZBEAM + 15, "guide rod Invar 36 ⌀12, ball ⌀8", "#5b4a99")
    t(v, p.C_INVAR_XY[1], V.Z_S1 + 60, 172, V.Z_S1 + 120, "Invar post ⌀16 (x = −95)\nfrom the base plate", "#5b4a99")
    t(v, p.C_REF_XY[1], ZCELL + p.COLLAR_TOP + 4, 172, V.Z_S1 + 85, "Invar target = camera reference", "#5b4a99")
    t(v, YL, ZL, 172, V.Z_S1 + 60, "(1) laser 68°, 11 lines", "#c0392b")
    t(v, 20, ZP - 5, 172, V.Z_S1 + 36, "partial piston ⌀50×20")
    t(v, 38, V.Z_S1 + 0.3, 172, V.Z_S1 + 14, "FREE surface (25 mm annulus)", FREE)
    t(v, -10, V.Z_S1 - 45, 172, V.Z_S1 - 30, "M: CS645 + fibre + Pt100", "#d33682")
    t(v, p.BODY_D / 2 - 5, V.Z_S0 + 10, 172, V.Z_S0 - 5, "printed cell ⌀240, one piece (V03)")
    t(v, RO - 8, ZCELL + 70, 172, V.Z_S0 - 30, "printed wall +40 (gyroid 10–15 %)", "#3a6f99")
    t(v, 60, ZB0 + 20, 172, ZB0 + 5, "printed base 40 + 3 G10 pads ⌀20×40", "#3a6f99")
    t(v, 100, ZB0 - 12, 172, ZB0 - 30, "Al plate 340×260×25")
    t(v, box_[0][0], box_[0][1], -150, ZCAM + 10, "(1) camera box:\nRPi HQ + 6 mm lens\n+ RPi 5 (its heat\nkeeps the window clear)",
      INK, ha="right")
    t(v, -40, ZBEAM + 40, -150, ZBEAM + 40, "columns 40×80\n(behind)", INK, ha="right")
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
    parts = [["1", f"Al base plate {bw:g}×{bd:g}×{bt:g}, 3 levelling feet"],
             ["2", f"2 columns Al 40×80 × {COL_H:g}, cross-beam 80×80 × {p.C_COL_SPAN + 40:g}"],
             ["3", "igus drylin RJ4JP-01-12 in the beam, Invar rod ⌀12"],
             ["4", "partial piston Al ⌀50×20, steel ball ⌀8"],
             ["5", "carrier Al ⌀120×8, steel discs ⌀120 (1 kg)"],
             ["6", "printed cell ⌀240 × 200, ONE piece incl. insulation (V03)"],
             ["7", "sand ⌀100×100; 3 G10 pads ⌀20×40 in the base pockets"],
             ["8", "Invar post ⌀16: LVDT arm + camera target arm"],
             ["9", "(1) camera + RPi 5 box, 11-line laser (V02)"],
             ["10", "(2) LVDT RDP DCTH400AG (V02)"],
             ["11", "point M: CS645, Pt100, optical fibre (existing)"]]
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
    # laser plane at 68° from +y: a surface at height h is hit at y = h / tan 68° = 0.40 h
    yl_, hl = p.C_LASER_Y, p.C_LASER_H
    yp = p.C_PISTON_H / TAN_L
    v.line([(yl_, hl), (yp, p.C_PISTON_H)], lw=1.2, c=LASER, z=5)
    v.line([(yp, p.C_PISTON_H), (0, 0)], lw=1.0, c=LASER, ls=":", z=5)
    v.rect(yl_ - 4, hl - 4, yl_ + 4, hl + 4, fc="#c0392b", lw=THIN, z=5)
    for h, lab, (tx, tz) in ((0, "● sand (|x| > 25): y = 0", (-50, 86)),
                             (p.C_PISTON_H, f"● piston top: y = {yp:.1f}", (-50, 96))):
        v.circle(h / TAN_L, h, 1.6, fc=LASER, lw=0, z_=6)
        v.text(tx, tz, lab, fontsize=fs(), color=LASER, va="center")
    v.circle(dh / TAN_L, dh, 1.6, fc="white", ec=LASER, lw=0.8, z_=6)
    v.dim_v(zs, zs + dh, -ri - 4, -ri - 16, "Δh")
    v.text(yl_ + 8, hl, f"laser {p.C_LASER_ANG:g}° (bracket on the beam)", fontsize=fs(), color=LASER, va="center")
    v.text(-ri + 2, -8, "sand", fontsize=fs())
    v.text(-p.C_PISTON_D / 2 + 2, p.C_PISTON_H / 2, "piston", fontsize=fs(), va="center")
    v.text(-rc - 18, zc_top + 4, "rim", fontsize=fs())
    v.text(-ri, -42, f"heave Δh moves the hit point by Δy = Δh / tan {p.C_LASER_ANG:g}° = {1 / TAN_L:.2f} Δh (open circle);\n"
           "no collar shadow: the laser sits above the cavity edge", fontsize=fs(), color=LASER, va="top")
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
        # piston top (h = 20): the same laser plane lands at y0 + 20 / tan 68°
        yp_ = y0 + p.C_PISTON_H / TAN_L
        if abs(yp_) < rp:
            xx = math.sqrt(rp ** 2 - yp_ ** 2)
            c.line([(-xx, yp_), (xx, yp_)], lw=1.2, c="#ffb3b3", z=5)
        # rim (h = 34): short segments on the collar top
        yr = y0 + zc_top / TAN_L
        if ri < abs(yr) < rc:
            pass
        for sgn in (-1, 1):
            if abs(yr) < rc:
                x0_ = math.sqrt(max(ri ** 2 - yr ** 2, 0))
                x1_ = math.sqrt(rc ** 2 - yr ** 2)
                c.line([(sgn * x0_, yr), (sgn * x1_, yr)], lw=2.2, c="#ff4d4d", z=5)
    xr_, yr_ = p.C_REF_XY
    c.rect(xr_ - 5, yr_ - 5, xr_ + 5, yr_ + 5, fc="white", lw=THIN, z=6)
    c.circle(xr_, yr_, 2, fc="#111", lw=0, z_=6.1)
    c.text(0, -62, f"+y (laser) ↑   pitch {p.C_LINE_PITCH:g} mm", fontsize=fs(), color="white", ha="center")
    V.tag(c, xr_ + 5, yr_ + 5, 75, 55, "Invar target = reference", "#5b4a99")
    V.tag(c, 46, 20, 75, 38, "rim: PETG, moves ≈ 100 µm / 20 K", INK)
    V.tag(c, 40, -9, 75, 18, "free sand: 11 profiles", INK)
    V.tag(c, 10, 6, 75, -2, "piston top (light red)", INK)
    V.tag(c, -20, -50, 75, -35, f"heave Δh: lines shift by {1 / TAN_L:.2f} Δh", INK)
    # (c) LVDT
    l_ = View(sh, 200, 190, 0.38, "(c) LVDT ON INVAR POST  1 : 2.6", (198, 252))
    yl_, yi = p.C_LVDT_XY[1], p.C_INVAR_XY[1]
    l_.rect(-40, 0, 40, 80, fc="#d9dde1", lw=THICK)
    l_.rect(-p.C_ROD_D / 2, -20, p.C_ROD_D / 2, 120, fc=V.INVAR, lw=THIN)
    l_.rect(-60, 115, 60, 115 + p.C_CARRIER_T, fc=METAL, lw=THIN, hatch="////")
    l_.rect(yi - 8, -20, yi + 8, 80, fc=V.INVAR, lw=THIN)
    l_.rect(yl_, 74, yi, 80, fc=V.INVAR, lw=THIN)
    l_.rect(yl_ - 9.5, 80, yl_ + 9.5, 105, fc=V.SENS, lw=THIN)
    l_.line([(yl_, 105), (yl_, 115)], lw=THICK)
    l_.dim_v(80, 115, 60, 72, "35 (±10 range)")
    V.tag(l_, yl_, 92, -60, -62, "LVDT DCTH400AG\non the Invar arm", V.SENS_TXT, ha="left")
    V.tag(l_, yi, 30, -60, -92, "Invar post from the base plate\n(beam and rod drift bypassed)", "#5b4a99", ha="left")
    V.tag(l_, -50, 118, -60, -38, "carrier = piston (Invar rod)", INK, ha="left")
    # right panel
    sh.heading(255, 276, "What is measured")
    rows = [["(1) camera + 11 lines", "map h(x, y) of the whole surface", "≈ 10 µm", "every 10 / 1 min"],
            ["(2) LVDT", "carrier = piston", "≈ 1 µm", "CR1000, 10 / 1 min"],
            ["Invar target", "camera / frame drift", "≈ 10 µm", "every photo"]]
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
            "1  blank run, Al dummy instead of sand, full cycle: drift of (1) and (2)\n"
            "   vs cell temperature (≈ 50 µm / 20 K, smooth) → fit and subtract\n"
            "2  calibrate (1): shims 0.1 / 0.5 / 1.0 mm under a flat plate,\n"
            "   camera px → mm for free sand and piston top\n"
            f"3  load, 24 h at +10 °C, then zero (1) and (2)\n"
            f"4  cycle {p.C_CYCLE_H[0]:g} h −10 °C / {p.C_CYCLE_H[1]:g} h +10 °C (fan on); CR1000 C5 pulse\n"
            "   triggers the photo; laser on only for the photo\n"
            "5  weigh the cell before / after each cycle; log air RH\n"
            "6  expected heave for Sr ≈ 0.4 is small (tens of µm) – decide Sr first",
            fontsize=fs(), va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V02_measurement.png"))


# --------------------------------------------------------------------------------------------
def _sheet_cell(pdf):
    """Rev. B: the cell printed in ONE piece – core = Column_one_body_version_1 (M. Vrána) + 40 mm low-infill wall
    and 40 mm base with 3 pockets for the G10 pads. z = 0 at the new underside."""
    sh = Sheet("Printed cell rev. B – one piece ⌀240 × 200 with insulation, point M", "E7-V03", "1 : 1.67", 3, TOTAL,
               "core per M. Vrána 23.06.2026 + 40 mm printed insulation; z = 0 at the underside")
    O = p.C_INS_T
    rb, rc, ri, w = p.BODY_D / 2, p.COLLAR_OD / 2, p.CAV_D / 2, p.CUP_WALL_IN
    ro = rb + p.C_SLEEVE_T
    H, Hc, tb, zs = p.BODY_H + O, p.COLLAR_TOP + O, p.BODY_BOTTOM + O, p.SAND_TOP + O
    pz0, pz1 = p.PORT_Z0 + O, p.PORT_Z1 + O
    t = p.TDR_CS645
    z_top = Hc - t["top_from_collar"]
    v = View(sh, 118, 112, 0.6, "SECTION A–A  1 : 1.67 (along the TDR axis)", (118, 277))
    for s_ in (-1, 1):
        v.rect(s_ * ri, tb, s_ * ro, H, fc=V.PETG, lw=THIN, hatch="..")
        v.rect(s_ * ri, H, s_ * rc, Hc, fc=V.PETG, lw=THIN)
        v.rect(s_ * ri, tb, s_ * (ri + w), Hc, fc=V.PETG, lw=THIN)
    v.rect(-ro, 0, ro, O, fc=V.PETG, lw=THIN, hatch="..")                      # printed base (low infill)
    v.rect(-ri - w, O, ri + w, tb, fc=V.PETG, lw=THIN)                          # floor 100 % under the cavity
    v.rect(-ro, O, -ri - w, tb, fc=V.PETG, lw=THIN, hatch="..")
    v.rect(ri + w, O, ro, tb, fc=V.PETG, lw=THIN, hatch="..")
    yp = p.C_PAD_R                                                              # pad at 90° lies in the section
    v.rect(yp - p.C_PAD_D / 2 - 0.2, 0, yp + p.C_PAD_D / 2 + 0.2, O, fc="white", lw=THIN)
    v.rect(yp - p.C_PAD_D / 2, -0.5, yp + p.C_PAD_D / 2, O, fc=G10, lw=THIN, z=2.6)
    v.rect(-ro, 0, ro, H, fc="none", lw=THICK)
    v.rect(-rc, H, rc, Hc, fc="none", lw=THICK)
    for s_ in (-1, 1):
        v.line([(s_ * rb, O), (s_ * rb, H)], lw=0.4, c="#9aa5ab", ls=":", z=2.3)
    v.line([(-rb, O), (rb, O)], lw=0.4, c="#9aa5ab", ls=":", z=2.3)
    v.rect(-ro - 0.3, pz0, -ri, pz1, fc="white", lw=THIN)
    v.rect(-ri, tb, ri, zs, fc="#efe6cc", lw=0, z=1.5)
    v.line([(-ri, zs), (ri, zs)], lw=THIN, ls="--", c="#8a7a50")
    v.axis_line([(0, -6), (0, Hc + 8)])
    for k in range(3):
        z = z_top - k * t["pitch"]
        v.line([(-ri, z), (-ri + t["rod_l"], z)], lw=1.4, c="#555", z=5)
    v.rect(-ri - w - t["head_l"], pz0 + 0.5, -ri, pz1 - 0.5, fc=V.TDRC, lw=THIN, z=5)
    v.line([(-ri, z_top + 2), (-ri + p.OF_TIP_FROM_WALL, z_top + 2)], lw=1.2, c=V.FBGC, z=5.2)
    zpt = z_top + p.C_PT100_DZ                       # Pt100 from the port, centred on top of the top rod
    x_tip, x_m = -ri + p.C_PT100_TIP, -ri + p.C_PT100_TIP - p.PT100_METAL
    v.rect(x_m, zpt - 1.5, x_tip, zpt + 1.5, fc=V.PTC, lw=0.5, z=5.3)
    v.rect(-ri, zpt - 1.0, x_m, zpt + 1.0, fc="#8a7300", lw=0.3, z=5.3)
    v.line([(-ro - 8, zpt), (-ri, zpt)], lw=0.9, c="#8a7300", z=5.3)
    v.dim_h(-ro, ro, 0, -12, f"⌀{2 * ro:g}", side="below")
    v.dim_h(-rc, rc, Hc, Hc + 10, "⌀106")
    v.dim_h(-ri, ri, Hc, Hc + 20, "⌀100")
    v.dim_v(0, Hc, -ro, -ro - 44, f"{Hc:g}")
    v.dim_v(0, H, -ro, -ro - 32, f"{H:g}")
    v.dim_v(0, pz1, -ro, -ro - 20, f"{pz1:g}")
    v.dim_v(0, pz0, -ro, -ro - 8, f"{pz0:g}")
    v.dim_v(0, O, ro, ro + 10, f"{O:g}")
    v.dim_v(0, tb, ro, ro + 24, f"{tb:g}")
    v.dim_v(tb, zs, ro, ro + 10, "100 sand")
    v.dim_v(zs, Hc, ro, ro + 10, f"{Hc - zs:g}")
    v.dim_v(pz1, Hc, ro, ro + 38, f"{Hc - pz1:g}")
    v.dim_h(ri + w, ro, H, H + 10, f"{ro - ri - w:g}")
    v.dim_h(0, yp, O / 2, -26, f"{yp:g}", side="below")
    V.tag(v, -ri + 30, z_top - t["pitch"], 40, 90, f"CS645: 3 rods ⌀3.2 × {t['rod_l']:g}, pitch {t['pitch']:g}")
    V.tag(v, -ri + 20, z_top + 2, -70, Hc + 34, f"optical fibre, tip {p.OF_TIP_FROM_WALL:g} from the wall", V.FBGC)
    V.tag(v, x_tip - 6, zpt + 1.5, 75, Hc + 34, f"Pt100 {p.PT100_L:g} (metal {p.PT100_METAL:g}) from the port,\n"
          f"centred on the top rod (+{p.C_PT100_DZ:g}), tip {p.C_PT100_TIP:g} from the wall", "#8a7300")
    v.dim_h(-ri, x_tip, zpt, zpt + 14, f"{p.C_PT100_TIP:g}")
    V.tag(v, -ro + 20, pz0 + 6, -10, -40, f"port 13 × 27 through the whole wall\n(TDR head {t['head_l']:g} at the inner wall)",
          V.TDRC, ha="left")
    V.tag(v, yp, O / 2, 75, -20, f"G10 pad ⌀{p.C_PAD_D:g} × {O:g} in a pocket ⌀{p.C_PAD_D + 0.4:g},\n3× at r {p.C_PAD_R:g}, 0.5 mm proud",
          "#4d7a2a")
    V.tag(v, -ro + 15, H - 30, -ro - 40, Hc + 52, "low infill (gyroid 10–15 %) = insulation,\nprinted together with the core", INK,
          ha="left")
    f = View(sh, 58, 44, 0.3, "PLAN  1 : 3.3", (58, 88))
    f.circle(0, 0, ro, fc=V.PETG, lw=THICK)
    f.circle(0, 0, rb, fc="none", ec="#9aa5ab", lw=0.4, ls=":")
    f.circle(0, 0, rc, fc="none", lw=THIN)
    f.circle(0, 0, ri, fc="#efe6cc", lw=THIN)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        f.circle(p.C_PAD_R * math.cos(a), p.C_PAD_R * math.sin(a), p.C_PAD_D / 2, fc="none", ec="#4d7a2a", lw=THIN, ls="--")
    f.rect(-p.PORT_W / 2, -ro, p.PORT_W / 2, -ri - w, fc="white", lw=THICK)
    f.rect(-1.6, -ri, 1.6, -ri + t["rod_l"], fc="#777", lw=0.3)
    f.rect(-1.5, -ri + p.C_PT100_TIP - p.PT100_METAL, 1.5, -ri + p.C_PT100_TIP, fc=V.PTC, lw=0.3, z=5)
    f.circle(0, 0, p.C_PISTON_D / 2, fc="none", ec=INK, lw=THIN, ls="--")
    f.text(0, -ro - 8, "port 13 wide (TDR axis, camera side); pads dashed (underneath)", fontsize=fs(), ha="center",
           va="top", color=V.TDRC)
    sh.heading(255, 276, "Point M (existing sensors)")
    rows = [["TDR", "Campbell CS645", "3 rods 75, pitch 8.9, in the port, depth 36/45/54"],
            ["OF", "optical fibre", f"at the top rod, tip {p.OF_TIP_FROM_WALL:g} from the wall"],
            ["Pt100", "37 mm (25 metal)", f"from the port, on top of the top rod, tip {p.C_PT100_TIP:g}"]]
    y = table(sh, 255, 272, ["", "sensor", "position"], rows, [16, 36, 103], row_h=5.8)
    sh.heading(255, y - 8, "Print (one piece)")
    pr = [["size", f"⌀{2 * ro:g} × {Hc:g} mm – bed ≥ 250 × 250, Z ≥ 200"],
          ["material", "PETG or PETG-CF, 0.2 mm layers, ≈ 1.3–1.6 kg"],
          ["walls", "cavity wall ≈ 5 mm (≈ 8 perimeters), outer 3 perimeters"],
          ["floor", f"z {O:g}–{tb:g} under the cavity: 100 % (stiff, flat)"],
          ["insulation", f"base z 0–{O:g} and wall r {rb:g}–{ro:g}: gyroid 10–15 %"],
          ["pockets", f"3× ⌀{p.C_PAD_D + 0.4:g} × {O:g} from below, r {p.C_PAD_R:g}"],
          ["time", "≈ 40–60 h (one job)"]]
    y = table(sh, 255, y - 12, ["item", "value"], pr, [26, 129], row_h=5.6)
    sh.text(255, y - 4,
            f"• Sand 100 mm (z {tb:g}–{zs:g}), {Hc - zs:g} mm free above (piston 20 + travel).\n"
            "• The cell stands on the 3 G10 pads only (0.5 mm proud): the low-infill\n"
            "  base insulates but carries no load → no creep in the LVDT chain.\n"
            f"• Heat model: λ infill ≈ {p.C_INS_K:g} W/mK → freezes from the top, last unfrozen\n"
            "  ≈ 13 mm above the floor; 95 % frozen in ≈ 13 h, thawed in ≈ 13 h.\n"
            "• Inside: epoxy coat + PTFE spray + silicone grease.\n"
            "• Cables: TDR head, Pt100 and fibre all through the port;\n"
            "  the sand surface stays completely free (camera + laser).\n"
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
          ["SE3", "Tair 109 (required)", "Therm109, VX1"],
          ["C1–C3", "TDR100/200 → CS645", "SDM"],
          ["C4", "relay: LVDT supply", "on for the scan"],
          ["C5", "pulse → RPi GPIO (opto)", "triggers photo + laser"],
          ["–", "(1) camera + RH sensor", "RPi 5 in the camera box"],
          ["–", "optical fibre", "own reader"]]
    y = table(sh, 255, 274, ["terminal", "connected to", "measurement"], ch, [24, 56, 75], row_h=5.6)
    sh.text(255, y - 4,
            "Notes\n"
            "• CR1000 and TDR outside; RPi 5 inside the camera box\n"
            "  (no CSI ribbon through the seal, its ≈ 5 W heat the box).\n"
            "  Through the lid seal: Ethernet, 5 V, LVDT, sensor cables.\n"
            "• Scan 10 min, 1 min around 0 °C; the photo is triggered\n"
            "  by the CR1000 (C5) → same time stamps without NTP.\n"
            "• Fan in the freezer evens out the on/off air swings.\n"
            "• No pressure cells: the load is a known dead weight.",
            fontsize=fs(), va="top", linespacing=1.45)
    sh.save(pdf, os.path.join(OUT, "E7-V04_sensors_costs.png"))


# --------------------------------------------------------------------------------------------
def _sheet_layout(pdf):
    sh = Sheet("Rig C rev. B in the chest freezer", "E7-V05", "1 : 5", 5, TOTAL,
               "same freezer as E6 (≈ 900 × 550 × 650, to be measured); CR1000 outside the freezer")
    k = 0.2
    v = View(sh, 35, 160, k)
    v.text(10, 535, "PLAN  1 : 5", fontsize=V.FS + 1, weight="bold", va="top")
    v.rect(0, 0, p.FRZ_L, p.FRZ_W, fc="#f5f9fc", lw=THICK, z=1)
    tx0, ty0 = 50, 105
    v.rect(tx0, ty0, tx0 + p.TRAY_L, ty0 + p.TRAY_W, fc="#d6d9dc", lw=THIN, z=1.2)
    v.rect(620, 15, 885, 535, fc="none", lw=THIN, ls="--", z=1.3)
    v.text(752, 60, "floor step (if present)", fontsize=fs() - 1, ha="center")
    bw, bd, bt = p.C_BASE
    ax, ay = tx0 + p.TRAY_L / 2, ty0 + p.TRAY_W / 2
    v.rect(ax - bw / 2, ay - bd / 2, ax + bw / 2, ay + bd / 2, fc=METAL, lw=THIN, z=2)
    for s_ in (-1, 1):
        v.rect(ax + s_ * p.C_COL_SPAN / 2 - 20, ay - 40, ax + s_ * p.C_COL_SPAN / 2 + 20, ay + 40, fc="#d9dde1",
               lw=THIN, z=2.2)
    v.rect(ax - p.C_COL_SPAN / 2 - 20, ay - 40, ax + p.C_COL_SPAN / 2 + 20, ay + 40, fc="none", lw=THIN, ls="--", z=2.3)
    v.circle(ax, ay, RO, fc=V.PETG, lw=THIN, z_=2.05)
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
    e.rect(ax - RO, z0, ax + RO, z0 + p.C_INS_T + p.BODY_H, fc=V.PETG, lw=THIN, z=2.05)
    e.rect(ax - bw / 2, z0 - bt, ax + bw / 2, z0, fc=METAL, lw=THIN, z=2)
    for s_ in (-1, 1):
        e.rect(ax + s_ * p.C_COL_SPAN / 2 - 20, z0, ax + s_ * p.C_COL_SPAN / 2 + 20, z0 + COL_H, fc="#d9dde1", lw=THIN, z=2)
    e.rect(ax - p.C_COL_SPAN / 2 - 20, z0 + COL_H, ax + p.C_COL_SPAN / 2 + 20, z0 + COL_H + p.AF_BEAM_H, fc="#d9dde1",
           lw=THIN, z=2)
    zi = z0 + p.C_INS_T                                # underside of the cell
    e.rect(ax - p.BODY_D / 2, zi, ax + p.BODY_D / 2, zi + p.BODY_H, fc=V.PETG, lw=THIN, z=2.1)
    e.rect(ax - p.COLLAR_OD / 2, zi + p.BODY_H, ax + p.COLLAR_OD / 2, zi + p.COLLAR_TOP, fc=V.PETG, lw=THIN, z=2.1)
    zc = z0 + (ZC - ZB0)
    top = zc + p.C_CARRIER_T + 4 * T1
    e.rect(ax - p.C_DISC_D / 2, zc, ax + p.C_DISC_D / 2, top, fc="#8a8f96", lw=THIN, z=2.2)
    e.rect(ax - 6, zi + p.BODY_BOTTOM + p.H_SAMPLE, ax + 6, zc, fc=V.INVAR, lw=THIN, z=2.15)
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
            "• Rev. B: cell printed in one piece ⌀240 × 200 (+40 base), beam gap 200 → 160:\n"
            "  the total height is unchanged.\n"
            "• 80 mm fan on the free end mixes the air; run the blank test first.",
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
