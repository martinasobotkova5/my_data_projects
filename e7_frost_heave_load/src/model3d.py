"""3D models of E7 rigs for Onshape (STEP assemblies, mm, z up).

Run: python model3d.py → ../3d/E7_variant_A.step, E7_variant_B.step, E7_freezer_layout.step
     + STL. Shaded PNG previews: python render3d.py. Import the STEP files in Onshape (Create → Import), the
     assembly keeps one part per component with its name and colour.
Geometry follows params.py and the drawings E7-V01…V06 (simplified: profile slots,
threads, cables and fasteners are not modelled).
"""
import math
import os

import cadquery as cq

import params as p

OUT = os.path.join(os.path.dirname(__file__), "..", "3d")

# stack heights (same as vykresy.py); z = 0 is the top of the base plate
H_BOT, G10_T = 40.0, 10.0
Z_PED = H_BOT + G10_T
Z_S0 = Z_PED + p.PEDESTAL_H          # 80
Z_S1 = Z_S0 + p.H_SAMPLE             # 180
Z_PT = Z_S1 + 40.0                   # piston top 220
TUBE_TOP = Z_S1 + 25.0               # 205
Z_TGT = Z_PT + 5.0                   # target plate top 225
BALL_C = Z_TGT + 6.0
Z_LC = Z_TGT + 12.0                  # 237
R_IN, R_OUT = p.D_CELL_IN / 2, p.D_CELL_OUT / 2
X_COL = p.COL_SPAN / 2
WALL_TH = [(10, 0), (30, 72), (50, 144), (70, 216), (90, 288)]

INS_T = 25.0             # Kaiflex around the cell
CELL_H = TUBE_TOP - Z_S0     # 125


C = {
    "al": cq.Color(0.78, 0.80, 0.82),
    "profile": cq.Color(0.70, 0.72, 0.75),
    "steel": cq.Color(0.50, 0.52, 0.55),
    "petg": cq.Color(0.20, 0.22, 0.24),
    "ptfe": cq.Color(0.95, 0.95, 0.95),
    "soil": cq.Color(0.55, 0.45, 0.33),
    "stone": cq.Color(0.75, 0.73, 0.62),
    "g10": cq.Color(0.60, 0.75, 0.40),
    "ins": cq.Color(0.15, 0.15, 0.15, 0.55),
    "sensor": cq.Color(0.91, 0.64, 0.24),
    "temp": cq.Color(0.75, 0.22, 0.17),
    "invar": cq.Color(0.56, 0.49, 0.76),
    "weight": cq.Color(0.35, 0.35, 0.38),
    "tray": cq.Color(0.85, 0.86, 0.88, 0.6),
    "pressure": cq.Color(0.12, 0.48, 0.55),
    "sand": cq.Color(0.86, 0.78, 0.58),
    "freezer": cq.Color(0.9, 0.95, 1.0, 0.15),
    "tdr": cq.Color(0.20, 0.55, 0.25),
    "pt100": cq.Color(0.85, 0.85, 0.20),
    "fbg": cq.Color(0.10, 0.75, 0.90),
}


def cyl(d, h, z0, x=0.0, y=0.0):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(d / 2).extrude(h)


def tube(d_out, d_in, h, z0):
    return cq.Workplane("XY").workplane(offset=z0).circle(d_out / 2).circle(d_in / 2).extrude(h)


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def radial(ang, r0, r1, z, d):
    """Cylinder along the radius at angle `ang` (deg) from r0 to r1, at height z."""
    c = cq.Workplane("YZ").circle(d / 2).extrude(r1 - r0).translate((r0, 0, z))
    return c.rotate((0, 0, 0), (0, 0, 1), ang)


def radial_off(ang, r0, r1, z, d, w=0.0):
    """Like radial(), but shifted sideways by w (perpendicular to the radius) before rotating."""
    c = cq.Workplane("YZ").circle(d / 2).extrude(r1 - r0).translate((r0, w, z))
    return c.rotate((0, 0, 0), (0, 0, 1), ang)


def variant_b(asm, prefix=""):
    """Variant B: same printed cell ⌀160 and point M as A, no load; surface + anchor LVDTs on an Invar stand."""
    hb, hd = p.BASE_W / 2, p.BASE_D / 2
    zb = body_a(asm, prefix, temps=WALL_TH, pv=False, pb=False, opt=False)
    asm.add(box(-hb, hb, -hd, hd, zb - p.B_BASE_T, zb), name=prefix + "Al base plate 260x200x20", color=C["al"])
    for i, (x, y) in enumerate(((-hb + 20, -hd + 20), (hb - 20, -hd + 20), (0, hd - 20))):
        asm.add(cyl(16, 18, zb - p.B_BASE_T - 18, x, y), name=f"{prefix}levelling foot {i + 1}", color=C["steel"])
    z_tp = Z_S1 + p.TOP_PLATE_T
    plate = cyl(p.TOP_PLATE_D, p.TOP_PLATE_T, Z_S1)
    for t, d, r, ang in p.ANCHORS:
        x, y = r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang))
        plate = plate.cut(cyl(p.PLATE_HOLE_D, p.TOP_PLATE_T, Z_S1, x, y))
    a_pt = p.PORT_ANG + 90
    xp, yp = p.PT100_R * math.cos(math.radians(a_pt)), p.PT100_R * math.sin(math.radians(a_pt))
    plate = plate.cut(cyl(p.B_PT100_HOLE, p.TOP_PLATE_T, Z_S1, xp, yp))
    asm.add(plate, name=prefix + "top plate PETG-CF D99x6", color=C["petg"])
    bd_, bl = p.LVDT_B_BODY
    z_body = p.Z_BRIDGE - 35.0
    for t, r, ang in p.SURF_LVDT:
        x, y = r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang))
        asm.add(cyl(5, 3, z_tp, x, y), name=f"{prefix}{t} rod seat", color=C["steel"])
        asm.add(cyl(3, z_body + 20 - z_tp - 3, z_tp + 3, x, y), name=f"{prefix}{t} core rod D3", color=C["steel"])
        asm.add(tube(bd_, 4, bl, z_body).translate((x, y, 0)), name=f"{prefix}{t} LVDT DCTH200 free core",
                color=C["sensor"])
    for t, d, r, ang in p.ANCHORS:
        x, y = r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang))
        z = Z_S1 - d
        asm.add(cyl(p.ANCHOR_D, p.ANCHOR_T, z - p.ANCHOR_T / 2, x, y), name=f"{prefix}{t} anchor D16 stainless",
                color=C["steel"])
        asm.add(tube(p.SLEEVE_D, p.ROD_D + 0.5, z_tp + 4 - (z + 2), z + 2).translate((x, y, 0)),
                name=f"{prefix}{t} PTFE sleeve D4", color=C["ptfe"])
        asm.add(cyl(p.ROD_D, z_body + 20 - z, z, x, y), name=f"{prefix}{t} Invar rod D2", color=C["invar"])
        asm.add(tube(bd_, 4, bl, z_body).translate((x, y, 0)), name=f"{prefix}{t} LVDT DCTH200 free core",
                color=C["sensor"])
    for i, ang in enumerate(p.STAND_ANG, 1):
        x, y = p.STAND_R * math.cos(math.radians(ang)), p.STAND_R * math.sin(math.radians(ang))
        asm.add(cyl(p.STAND_POST_D, p.Z_BRIDGE - zb, zb, x, y), name=f"{prefix}Invar post {i}", color=C["invar"])
    bridge = cyl(p.BRIDGE_D, p.BRIDGE_T, p.Z_BRIDGE)
    for t, r, ang in p.SURF_LVDT + [(a[0], a[2], a[3]) for a in p.ANCHORS]:
        bridge = bridge.cut(cyl(bd_ + 0.5, p.BRIDGE_T, p.Z_BRIDGE, r * math.cos(math.radians(ang)),
                                r * math.sin(math.radians(ang))))
    asm.add(bridge, name=prefix + "Al bridge D220x10 (LVDT clamps)", color=C["al"])
    asm.add(radial(180, p.STAND_R - 6, p.STAND_R + 20, 230, 1.6), name=prefix + "Tstand 109SS", color=C["temp"])

def body_a(asm, prefix="", temps=None, pv=True, pb=True, opt=True, pt_r=None, pt_ang=None, ins=False, pt_port=False,
           top=None):
    """Variant A cell per drawing Column_one_body_version_1: body ⌀160 × 130 + collar ⌀106 to 160,
    cavity ⌀100 from z 26 (z = 0 at the underside), side port 13 wide at 67.5–94.5 (PORT_ANG).
    Point M: CS645 in the port, optical fibre, Pt100 vertical. Returns z of the underside of the core.
    ins=True: rev. B, printed in ONE piece with +C_SLEEVE_T low-infill wall and a +C_INS_T base with 3 pockets
    for the G10 pads (⌀220 × 200 overall); the port runs through the whole wall."""
    zb = Z_S0 - p.BODY_BOTTOM
    rb, rc, ri = p.BODY_D / 2, p.COLLAR_OD / 2, p.CAV_D / 2
    ro = rb + (p.C_SLEEVE_T if ins else 0.0)
    ztop = p.COLLAR_TOP if top is None else top
    if top is None:
        body = cyl(p.BODY_D, p.BODY_H, zb).union(cyl(p.COLLAR_OD, p.COLLAR_TOP - p.BODY_H, zb + p.BODY_H))
    else:
        body = cyl(p.BODY_D, top, zb)
    if ins:
        body = body.union(cyl(2 * ro, (p.BODY_H if top is None else top) + p.C_INS_T, zb - p.C_INS_T))
        for k in range(3):
            a_ = math.radians(90 + 120 * k)
            body = body.cut(cyl(p.C_PAD_D + 0.4, p.C_INS_T, zb - p.C_INS_T, p.C_PAD_R * math.cos(a_),
                                p.C_PAD_R * math.sin(a_)))
        body = body.cut(radial(p.C_NTC_ANG, 0, ro + 1, zb - p.C_INS_T + p.C_NTC_Z, 4.0))   # NTC in the base
    body = body.cut(cyl(p.CAV_D, ztop - p.BODY_BOTTOM, zb + p.BODY_BOTTOM))
    rb = ro
    port = box(ri + p.CUP_WALL_IN, rb + 1, -p.PORT_W / 2, p.PORT_W / 2, zb + p.PORT_Z0, zb + p.PORT_Z1)
    body = body.cut(port.rotate((0, 0, 0), (0, 0, 1), p.PORT_ANG))
    t = p.TDR_CS645
    z_top = zb + p.COLLAR_TOP - t["top_from_collar"]
    a = p.PORT_ANG
    for k in range(3):
        body = body.cut(radial(a, ri - 1, ri + p.CUP_WALL_IN + 1, z_top - k * t["pitch"], t["rod_d"] + 0.3))
    body = body.cut(radial_off(a, ri - 1, ri + p.CUP_WALL_IN + 1, z_top + 2, 1.5, w=p.OF_SIDE))
    if pt_port:                                      # rev. B: Pt100 through the inner wall, on top of the top rod
        body = body.cut(radial(a, ri - 1, ri + p.CUP_WALL_IN + 1, z_top + p.C_PT100_DZ, 3.3))
    temps = [(d, ang) for _, d, ang in p.AM_TEMPS] if temps is None else temps
    for d, ang in temps:
        body = body.cut(radial(ang, ri - 1, rb + 1, Z_S1 - d, 2.0))
    if pv:
        body = body.cut(radial(90, ri - 1, rb + 1, Z_S1 - p.AM_PV[1], 3.5))
    body = body.cut(radial(0, ri - 1, rb + 1, Z_S1 - 1, 4.0))
    xb, yb = 25 * math.cos(math.radians(p.AM_PB[2])), 25 * math.sin(math.radians(p.AM_PB[2]))
    if pb:
        body = body.cut(cyl(8.2, 1.6, Z_S0 - 1.6, xb, yb))
    hh = ztop + p.C_INS_T
    asm.add(body, name=prefix + ((f"cell PETG D{p.BODY_D + 2 * p.C_SLEEVE_T:g}x{hh:g} one piece, rev. B (core Column_one_body_version_1)"
                                  if top is None else f"cell PETG D{p.BODY_D + 2 * p.C_SLEEVE_T:g}x{hh:g} flat top, variant U") if ins
                                 else "cell body PETG D160 (Column_one_body_version_1)"), color=C["petg"])
    if pb:
        asm.add(cyl(8, 1.5, Z_S0 - 1.5, xb, yb), name=prefix + "PB1 TML PDA-PA (flush)", color=C["pressure"])
    asm.add(cyl(p.D_SAMPLE, p.H_SAMPLE, Z_S0), name=prefix + "unsaturated sand D100x100", color=C["sand"])
    # point M
    asm.add(box(ri + p.CUP_WALL_IN, ri + p.CUP_WALL_IN + t["head_l"], -6, 6, zb + p.PORT_Z0 + 0.5, zb + p.PORT_Z1 - 0.5)
            .rotate((0, 0, 0), (0, 0, 1), a), name=prefix + "M TDR CS645 head", color=C["tdr"])
    for k in range(3):
        asm.add(radial_off(a, ri - t["rod_l"], ri, z_top - k * t["pitch"], t["rod_d"]),
                name=f"{prefix}M TDR CS645 rod {k + 1}", color=C["steel"])
    asm.add(radial_off(a, ri - p.OF_TIP_FROM_WALL, rb + 30, z_top + 2, 1.0, w=p.OF_SIDE),
            name=prefix + "M optical fibre", color=C["fbg"])
    if pt_port:
        zp = z_top + p.C_PT100_DZ
        r_tip, r_m = ri - p.C_PT100_TIP, ri - p.C_PT100_TIP + p.PT100_METAL
        asm.add(radial(a, r_tip, r_m, zp, 3.0), name=prefix + "M Pt100 metal part", color=C["pt100"])
        asm.add(radial(a, r_m, rb + 30, zp, 2.0), name=prefix + "M Pt100 cable", color=C["pt100"])
    else:
        pt_r = p.PT100_R if pt_r is None else pt_r
        pa = a + 90 if pt_ang is None else pt_ang
        xp, yp = pt_r * math.cos(math.radians(pa)), pt_r * math.sin(math.radians(pa))
        asm.add(cyl(3.0, p.PT100_METAL, Z_S1 - p.PT100_L, xp, yp), name=prefix + "M Pt100 metal part", color=C["pt100"])
        asm.add(cyl(2.0, p.PT100_L - p.PT100_METAL, Z_S1 - (p.PT100_L - p.PT100_METAL), xp, yp),
                name=prefix + "M Pt100 cable", color=C["pt100"])
    for i_, (d, ang) in enumerate(temps, 1):
        asm.add(radial(ang, p.T_TIP_R, rb + 8, Z_S1 - d, 1.6),
                name=f"{prefix}T{i_} 109SS" + (" (opt.)" if opt else ""), color=C["temp"])
    if not pv:
        return zb
    asm.add(cyl(p.PCELL_D, p.PCELL_T, Z_S1 - p.AM_PV[1] - p.PCELL_T / 2), name=prefix + "PV1 TML PDA-PA on D20 disc",
            color=C["pressure"])
    asm.add(radial(90, p.PCELL_D / 2, rb + 15, Z_S1 - p.AM_PV[1], 2.5), name=prefix + "PV1 cable",
            color=C["pressure"])
    return zb


def variant_a_min(asm, prefix=""):
    """Variant A-min: fixed steel lid on 3 tie rods (sample cannot move), 2 pressure cells, point M with the
    lab's own TDR / temperature sensor / optical fibre, 1 LVDT on the lid – the minimum version of A."""
    bw, bd, _ = p.AM_BASE
    bt = p.AM_BASE_T2
    zb0 = Z_S0 - p.AM_BOTTOM_T - p.AM_G10_T
    base = box(-bw / 2, bw / 2, -bd / 2, bd / 2, zb0 - bt, zb0)
    for ang in p.AM_TIE_ANG:
        base = base.cut(cyl(p.AM_TIE_D + 1, bt, zb0 - bt, p.AM_TIE_R * math.cos(math.radians(ang)),
                            p.AM_TIE_R * math.sin(math.radians(ang))))
    asm.add(base, name=prefix + "Al base plate 230x230x20", color=C["al"])
    body_a(asm, prefix)
    zp = Z_S1 + p.AM_PISTON_H
    asm.add(cyl(99.5, p.AM_PISTON_H, Z_S1), name=prefix + "Al piston D99.5x40", color=C["al"])
    zl0 = zp + p.AM_LID_GAP
    zl1 = zl0 + p.AM_LID_T
    lid = cyl(p.AM_LID_D, p.AM_LID_T, zl0).cut(cyl(p.AM_SCREW_D, p.AM_LID_T, zl0))
    for i, ang in enumerate(p.AM_TIE_ANG, 1):
        x, y = p.AM_TIE_R * math.cos(math.radians(ang)), p.AM_TIE_R * math.sin(math.radians(ang))
        lid = lid.cut(cyl(p.AM_TIE_D + 1, p.AM_LID_T, zl0, x, y))
        asm.add(cyl(p.AM_TIE_D, zl1 + 15 - (zb0 - bt - 10), zb0 - bt - 10, x, y), name=f"{prefix}tie rod M10 {i}",
                color=C["steel"])
        for zz, where in ((zl1, "top"), (zb0 - bt - 8, "bottom")):
            asm.add(cyl(17, 8, zz, x, y), name=f"{prefix}nut M10 {i} {where}", color=C["weight"])
    asm.add(lid, name=prefix + "steel lid D240x15", color=C["steel"])
    asm.add(cyl(p.AM_SCREW_D, zl1 + 30 - zp, zp), name=prefix + "centre screw M16x1.5", color=C["weight"])
    asm.add(cyl(26, 10, zl1), name=prefix + "lock nut M16", color=C["weight"])
    c = bw / 2 - 15
    r_l = p.AM_LID_D / 2 - 10
    xl, yl = r_l * math.cos(math.radians(225)), r_l * math.sin(math.radians(225))
    z_arm = zl1 + 75
    asm.add(cyl(p.AM_POST_D, z_arm + 10 - zb0, zb0, -c, -c), name=prefix + "stainless post D12", color=C["steel"])
    L = math.hypot(c + xl, c + yl)
    asm.add(box(0, L + 6, -6, 6, z_arm, z_arm + 10).rotate((0, 0, 0), (0, 0, 1), 45).translate((-c, -c, 0)),
            name=prefix + "LVDT clamp arm", color=C["steel"])
    asm.add(cyl(19, 60, z_arm - 60, xl, yl), name=prefix + "LVDT RDP DCTH400AG", color=C["sensor"])
    asm.add(cyl(4, z_arm - 60 - zl1, zl1, xl, yl), name=prefix + "LVDT plunger", color=C["steel"])


def variant_a_frame(asm, prefix=""):
    """Variant A-frame: same sample and sensors as A-min, piston held by an Al profile frame
    (2 columns 40x80 + cross-beam 80x80), screw M16x1.5, Al spacer + POM-C thermal insert."""
    bw, bd, bt = p.AF_BASE
    zb0 = Z_S0 - p.AM_BOTTOM_T - p.AM_G10_T
    zbeam = zb0 + p.AF_COL_H
    xc = p.COL_SPAN / 2
    asm.add(box(-bw / 2, bw / 2, -bd / 2, bd / 2, zb0 - bt, zb0), name=prefix + "Al base plate 260x200x25", color=C["al"])
    for i, (x, y) in enumerate(((-bw / 2 + 20, -bd / 2 + 20), (bw / 2 - 20, -bd / 2 + 20), (0, bd / 2 - 20)), 1):
        asm.add(cyl(16, 18, zb0 - bt - 18, x, y), name=f"{prefix}levelling foot {i}", color=C["steel"])
    for s_ in (-1, 1):
        asm.add(box(s_ * xc - 20, s_ * xc + 20, -40, 40, zb0, zbeam),
                name=f"{prefix}column 40x80 {'L' if s_ < 0 else 'R'}", color=C["profile"])
    asm.add(box(-xc - 20, xc + 20, -40, 40, zbeam, zbeam + p.AF_BEAM_H).cut(cyl(16, p.AF_BEAM_H, zbeam)),
            name=prefix + "cross-beam 80x80", color=C["profile"])
    body_a(asm, prefix)
    zp = Z_S1 + p.AM_PISTON_H
    asm.add(cyl(99.5, p.AM_PISTON_H, Z_S1), name=prefix + "Al piston D99.5x40", color=C["al"])
    z_pom0 = zbeam - p.AF_SCREW_PROTRUDE - p.AF_POM_T
    asm.add(cyl(p.AF_SPACER_D, z_pom0 - zp, zp), name=prefix + f"Al spacer D40x{p.AF_SPACER_L:g}", color=C["al"])
    asm.add(cyl(p.AF_SPACER_D, p.AF_POM_T, z_pom0), name=prefix + f"POM-C thermal insert D40x{p.AF_POM_T:g}", color=C["ptfe"])
    asm.add(cyl(16, p.AF_SCREW_PROTRUDE + p.AF_BEAM_H + 35, zbeam - p.AF_SCREW_PROTRUDE),
            name=prefix + "screw M16x1.5", color=C["weight"])
    asm.add(cyl(26, 10, zbeam + p.AF_BEAM_H), name=prefix + "lock nut M16", color=C["weight"])
    asm.add(cyl(60, 6, zbeam + p.AF_BEAM_H + 35), name=prefix + "handwheel", color=C["steel"])
    # LVDT on the piston top edge at 300° (clear of the port at 270°), post outside the body
    al = math.radians(300)
    xl, yl = 40 * math.cos(al), 40 * math.sin(al)
    xp, yp = 92 * math.cos(al), 92 * math.sin(al)
    asm.add(cyl(p.AM_POST_D, zp + 70 - zb0, zb0, xp, yp), name=prefix + "stainless post D12", color=C["steel"])
    asm.add(box(0, 52 + 6, -6, 6, zp + 60, zp + 70).rotate((0, 0, 0), (0, 0, 1), 120).translate((xp, yp, 0)),
            name=prefix + "LVDT clamp arm", color=C["steel"])
    asm.add(cyl(19, 55, zp + 5, xl, yl), name=prefix + "LVDT RDP DCTH400AG", color=C["sensor"])
    asm.add(cyl(4, 5, zp, xl, yl), name=prefix + "LVDT plunger", color=C["steel"])

def variant_b_open(asm, prefix=""):
    """Variant B-open (sheet V06): printed cell ⌀160 on an Al plate, nothing on the sand; camera looking down
    in a heated box on a post + arm, line laser at 45°."""
    bw, bd, bt = p.BC_BASE
    zb = body_a(asm, prefix, temps=[], pv=False, pb=False, opt=False)
    rb = p.BODY_D / 2
    x0 = -rb - 20
    asm.add(box(x0, x0 + bw, -bd / 2, bd / 2, zb - bt, zb), name=prefix + "Al base plate 320x220x10", color=C["al"])
    zcam = Z_S1 + p.BL_CAM_H
    bx, bz = 70.0, 80.0
    xpost = rb + 50
    z_arm0, z_arm1 = zcam + bz / 2 + 20, zcam + bz / 2 + 40
    asm.add(box(xpost, xpost + 20, -10, 10, zb, z_arm1), name=prefix + "post Al profile 20x20", color=C["profile"])
    asm.add(box(-bx / 2 - 10, xpost, -10, 10, z_arm0, z_arm1), name=prefix + "arm Al profile 20x20", color=C["profile"])
    cam_box = box(-bx / 2, bx / 2, -bx / 2, bx / 2, zcam - bz / 2, z_arm0).cut(
        box(-bx / 2 + 20, bx / 2 - 20, -bx / 2 + 20, bx / 2 - 20, zcam - bz / 2 + 20, z_arm0 - 20)).cut(
        cyl(28, 20, zcam - bz / 2))
    asm.add(cam_box, name=prefix + "heated camera box XPS 30", color=C["ins"])
    asm.add(cyl(28, 2, zcam - bz / 2, 0, 0), name=prefix + "double-glass window", color=C["freezer"])
    asm.add(cyl(30, 25, zcam - bz / 2 + 2), name=prefix + "lens 12 mm C-mount", color=C["steel"])
    asm.add(box(-19, 19, -19, 19, zcam - bz / 2 + 27, zcam - bz / 2 + 47), name=prefix + "Raspberry Pi HQ camera",
            color=C["petg"])
    xl = p.BL_LASER_X
    zl = Z_S1 + p.BL_LASER_X / math.tan(math.radians(p.BL_LASER_ANG))
    laser = (cq.Workplane("YZ").circle(6).extrude(30).translate((-15, 0, 0))
             .rotate((0, 0, 0), (0, 1, 0), -p.BL_LASER_ANG).translate((xl, 0, zl)))
    asm.add(laser, name=prefix + "line laser 650 nm (45 deg)", color=C["temp"])
    asm.add(box(xpost + 20, xl + 12, -8, 8, zl + 8, zl + 14), name=prefix + "laser bracket", color=C["al"])
    return zb


def variant_c(asm, prefix="", orbit_angle=0.0):
    """Variant C rev. B3 (orderable): frame of T-slot profiles slot 8 (2 base rails 40×40, cross bar 40×80 flat,
    2 columns 40×80, top beam 40×80 flat with one ⌀14 hole), Invar rod and post, printed arms, cell printed in one
    piece on 3 G10 pads, laser-cut piston discs, carrier and steel weights.
    18. 11. 2026 – ONE setup for both phases: the igus bushing of the guide rod sits in the fixed core P12 of the
    camera orbit (orbit.py, replaces housing P01) and the camera head orbits round the rod (orbit_angle, 0 = home −y).
    orbit_angle=None → the old fixed camera box P06 on hanger P08 and housing P01 (rev. B3, for comparison)."""
    import buildparts as bp
    zb0 = _frame_c(asm, prefix)
    zbeam, zc = bp.ZBEAM, bp.ZC
    xc = p.C_COL_SPAN / 2
    lp = {d["name"]: d for d in bp.LASER}
    if orbit_angle is None:
        asm.add(bp.housing().translate((0, 0, zbeam - p.C_HOUSING[2])), name=prefix + "P01 bearing housing (print, hangs)",
                color=C["petg"])
        bush_od, bush_l = p.C_BUSH
        asm.add(tube(bush_od, p.C_ROD_D + 0.1, bush_l, zbeam - p.C_HOUSING[2] + 4.5),
                name=prefix + "igus drylin RJ4JP-01-12", color=C["ptfe"])
    # cell printed in one piece with its insulation; 3 G10 pads ⌀20 × 40 in pockets of the printed base carry it
    for k in range(3):
        a = math.radians(90 + 120 * k)
        x, y = p.C_PAD_R * math.cos(a), p.C_PAD_R * math.sin(a)
        asm.add(cyl(p.C_PAD_D, p.C_INS_T, zb0, x, y), name=f"{prefix}G10 pad D20x40 {k + 1}", color=C["g10"])
    body_a(asm, prefix, temps=[], pv=False, pb=False, opt=False, ins=True, pt_port=True, top=p.U_TOP)   # same cell as phase 1
    asm.add(bp.pad_locator().translate((0, 0, zb0)), name=prefix + "P20 cell stops on T03 (print)", color=C["petg"])
    # moving load: piston (2 laser discs), ball 5/16", Invar rod, shaft collar, carrier, discs
    asm.add(bp.laser_solid(lp["E7-L05_piston_bottom"]).translate((0, 0, Z_S1)), name=prefix + "L05 piston bottom",
            color=C["al"])
    asm.add(bp.laser_solid(lp["E7-L04_piston_top"]).translate((0, 0, Z_S1 + p.C_PISTON_H / 2)),
            name=prefix + "L04 piston top (ball seat)", color=C["al"])
    asm.add(cq.Workplane("XY").sphere(p.C_BALL_D / 2).translate((0, 0, bp.Z_BALL)), name=prefix + "steel ball 5-16in (7.94)",
            color=C["steel"])
    rod = cyl(p.C_ROD_D, bp.ROD_L, bp.Z_ROD0)
    rod = rod.cut(cq.Workplane("XY").add(cq.Solid.makeCone(p.C_ROD_CONE / 2, 0, p.C_ROD_CONE / 2,
                                                           cq.Vector(0, 0, bp.Z_ROD0 - 0.01))))
    rod = rod.cut(cyl(5.0, 15.5, bp.Z_ROD0 + bp.ROD_L - 15.0))                       # M6 thread for the stud (model: ⌀5 × 15)
    asm.add(rod, name=prefix + f"guide rod Invar 36 D12 x{bp.ROD_L}", color=C["invar"])
    zs = zc - 10.0                                   # M6 stud: 10 mm in the rod, through carrier and discs
    asm.add(cyl(5.0, 10.0, zs).union(cyl(p.C_STUD[0], p.C_STUD[1] - 10.0, zc)), name=prefix + f"M6 stud DIN 913 x{p.C_STUD[1]:g} (carrier + discs)",
            color=C["steel"])
    asm.add(bp.laser_solid(lp["E7-L03_carrier"]).translate((0, 0, zc)), name=prefix + f"L03 carrier Al D{p.C_CARRIER_D:g}x{p.C_CARRIER_T:g}",
            color=C["al"])
    z = zc + p.C_CARRIER_T
    for i in range(bp.N_DISC):
        asm.add(bp.laser_solid(lp["E7-L06_disc_1kg"]).translate((0, 0, z)), name=f"{prefix}L06 steel disc {i + 1} 1 kg",
                color=C["weight"])
        z += p.C_DISC_T
    asm.add(bp.laser_solid(lp["E7-L07_disc_0.5kg"]).translate((0, 0, z)), name=f"{prefix}L07 steel disc 0.5 kg",
            color=C["weight"])
    z += p.C_DISC_T / 2
    nut = cq.Workplane("XY").polygon(6, 11.5).extrude(3.2).translate((0, 0, z))
    asm.add(nut.cut(cyl(6, 4, z)), name=prefix + "thin nut M6 DIN 439 (clamps the discs)", color=C["steel"])
    # Invar post on the base rail (printed foot), printed arms with the LVDT and the camera target
    xi, yi = p.C_INVAR_XY
    asm.add(bp.post_foot().translate((0, 0, zb0)), name=prefix + "P04 post foot (print)", color=C["petg"])
    asm.add(cyl(p.C_INVAR_D, bp.POST_L, zb0 + bp.POST_FLOOR, xi, yi), name=prefix + f"Invar 36 post D16 x{bp.POST_L:.0f}",
            color=C["invar"])
    asm.add(bp.lvdt_arm().translate((0, 0, bp.Z_ARM)), name=prefix + "P02 LVDT arm (print)", color=C["petg"])
    xl, yl = p.C_LVDT_XY
    asm.add(cyl(bp.LV_D, bp.LV_L, bp.Z_LV_BOT, xl, yl), name=prefix + "LVDT RDP DCTH400AG", color=C["sensor"])
    asm.add(cyl(4, zc - bp.Z_LV_TOP, bp.Z_LV_TOP, xl, yl), name=prefix + "LVDT plunger", color=C["steel"])
    asm.add(bp.target_arm().translate((0, 0, bp.Z_REF_U)), name=prefix + "P03 target arm (print)", color=C["petg"])
    _optics_c(asm, prefix, orbit_angle=orbit_angle)
    return zb0


def _frame_c(asm, prefix=""):
    """T-slot frame of variant C / U: base rails, cross bar, columns, top beam (with the ⌀14 hole), brackets, feet."""
    import buildparts as bp
    zb0, zbeam, zc = bp.ZB0, bp.ZBEAM, bp.ZC
    xc = p.C_COL_SPAN / 2
    # base frame: 2 rails 40×40 (along y) under the columns, one cross bar 40×80 flat between them
    for s_ in (-1, 1):
        rail = bp.profile_solid((40, 40), p.C_BASE[1]).rotate((0, 0, 0), (0, 0, 1), 90).translate((s_ * p.C_RAIL_X, 0, zb0 - 40))
        asm.add(rail, name=f"{prefix}T02 base rail 40x40 x{p.C_BASE[1]:g} {'L' if s_ < 0 else 'R'}", color=C["profile"])
        for sy in (-1, 1):
            asm.add(cyl(p.C_RUBBER[0], p.C_RUBBER[1], zb0 - 40 - p.C_RUBBER[1], s_ * p.C_RAIL_X, sy * p.C_FOOT_Y),
                    name=f"{prefix}rubber pad D30x3 {'L' if s_ < 0 else 'R'}{sy:+d}", color=C["ins"])
    lcb = 2 * (p.C_RAIL_X - 20)
    yc = p.C_CROSS_Y[0]
    asm.add(bp.profile_solid((80, 40), lcb).translate((0, yc, zb0 - 40)), name=f"{prefix}T03 base cross bar 40x80 x{lcb:g}",
            color=C["profile"])
    for s_ in (-1, 1):                               # angle brackets rail inner face ↔ cross bar side faces (±y)
        x0, x1 = sorted((s_ * (p.C_RAIL_X - 20), s_ * (p.C_RAIL_X - 60)))
        xi0, xi1 = (x0, x1 - 4) if s_ > 0 else (x0 + 4, x1)
        for sy in (-1, 1):
            y0, y1 = sorted((yc + sy * 40, yc + sy * 80))
            yi0, yi1 = (y0 + 4, y1 + 1) if sy > 0 else (y0 - 1, y1 - 4)
            br = box(x0, x1, y0, y1, zb0 - 30, zb0 - 10).cut(box(xi0, xi1, yi0, yi1, zb0 - 31, zb0 - 9))
            asm.add(br, name=f"{prefix}angle bracket 40 base {'L' if s_ < 0 else 'R'}{sy:+d}", color=C["steel"])
    for s_ in (-1, 1):
        asm.add(box(s_ * xc - 20, s_ * xc + 20, -40, 40, zb0, zbeam),
                name=f"{prefix}T01 column 40x80 slot 8 x{bp.COL_H:g} {'L' if s_ < 0 else 'R'}", color=C["profile"])
        for sy in (-1, 1):                           # column ↔ rail: brackets on the ±y faces of the column
            br = box(s_ * xc - 10, s_ * xc + 10, 40 if sy > 0 else -80, 80 if sy > 0 else -40, zb0, zb0 + 40)
            br = br.cut(box(s_ * xc - 11, s_ * xc + 11, 44 if sy > 0 else -80, 80 if sy > 0 else -44, zb0 + 4, zb0 + 40))
            asm.add(br, name=f"{prefix}angle bracket 40 slot 8 {'L' if s_ < 0 else 'R'}b{sy:+d}", color=C["steel"])
        for y in (-20, 20):                          # column ↔ top beam: brackets on the inner faces, under the beam
            x0, x1 = (s_ * xc - 20 - 40, s_ * xc - 20) if s_ > 0 else (s_ * xc + 20, s_ * xc + 20 + 40)
            br = box(x0, x1, y - 10, y + 10, zbeam - 40, zbeam)
            xi0, xi1 = (x0, x1 - 4) if s_ > 0 else (x0 + 4, x1)
            br = br.cut(box(xi0, xi1, y - 11, y + 11, zbeam - 40, zbeam - 4))
            asm.add(br, name=f"{prefix}angle bracket 40 slot 8 {'L' if s_ < 0 else 'R'}t{y:+d}", color=C["steel"])
    asm.add(bp.profile_solid((80, 40), p.C_TOP[0], hole=True).translate((0, 0, zbeam)),
            name=prefix + "T04 top beam 40x80 x340, hole D14", color=C["profile"])
    return zb0


def _optics_c(asm, prefix="", led=False, camera=True, orbit_angle=None):
    """Fixed camera (box P06 on hanger P08) and line laser (holder P05) on the top beam; led=True adds the white LED.
    orbit_angle given: no fixed camera – the orbiting Camera Module 3 head (orbit.py) at that angle instead."""
    import buildparts as bp
    zbeam = bp.ZBEAM
    zcam = Z_S1 + p.C_CAM_H
    if orbit_angle is not None:
        import orbit
        orbit.add_to(asm, prefix, C, orbit_angle)
        camera, led = False, False
    if camera:                                       # camera box (printed) hanging from the top beam, tilted to the axis
        cam = bp.camera_box().rotate((0, 0, 0), (1, 0, 0), p.C_CAM_TILT).translate((0, p.C_CAM_Y, zcam))
        asm.add(cam, name=prefix + "P06 camera box: RPi HQ + 6 mm lens + RPi 5", color=C["ins"])
        asm.add(bp.camera_hanger().translate((0, 0, zbeam)), name=prefix + "P08 camera mount (print)", color=C["petg"])
    asm.add(bp.laser_holder().translate((0, 0, zbeam)), name=prefix + "P05 laser holder (print)", color=C["petg"])
    yl_, zl = p.C_LASER_Y, Z_S1 + p.C_LASER_H
    las = (cq.Workplane("XZ").circle(5).extrude(11, both=True)
           .rotate((0, 0, 0), (1, 0, 0), p.C_LASER_ANG).translate((0, yl_, zl)))
    asm.add(las, name=prefix + f"line laser Picotronic DOE253 ({p.C_LASER_ANG:g} deg)", color=C["temp"])
    if led:
        lz = -35.0                                   # window face of the box (box height 70)
        led_s = (cyl(p.C_LED[0], p.C_LED[1], lz - p.C_LED[1], 0, -p.C_LED_OFF)
                 .rotate((0, 0, 0), (1, 0, 0), p.C_CAM_TILT).translate((0, p.C_CAM_Y, zcam)))
        asm.add(led_s, name=prefix + "LED white 5 V on star D20 (photo light)", color=C["temp"])


def variant_u(asm, prefix="", orbit_angle=0.0):
    """Variant U (phase 1, 16. 11. 2026): NO LOAD. Same frame, camera, laser and G10 pads as variant C; the cell has a
    flat top only 5 mm above the sand (no collar), so camera and laser see the whole surface ⌀100. No piston, weights,
    guide rod, bearing or LVDT; the Invar post carries only the reference target P03. The camera (Raspberry Pi Camera
    Module 3 in a small head with a white LED) ORBITS round the sample on a hub under the top beam (orbit.py);
    orbit_angle 0 = home on −y, where the laser images are taken. orbit_angle=None → old fixed camera box."""
    zb0 = _frame_c(asm, prefix)
    # cell printed in one piece with its insulation; 3 G10 pads ⌀20 × 40 in pockets of the printed base carry it
    for k in range(3):
        a = math.radians(90 + 120 * k)
        x, y = p.C_PAD_R * math.cos(a), p.C_PAD_R * math.sin(a)
        asm.add(cyl(p.C_PAD_D, p.C_INS_T, zb0, x, y), name=f"{prefix}G10 pad D20x40 {k + 1}", color=C["g10"])
    body_a(asm, prefix, temps=[], pv=False, pb=False, opt=False, ins=True, pt_port=True, top=p.U_TOP)
    import buildparts as bp
    asm.add(bp.pad_locator().translate((0, 0, zb0)), name=prefix + "P20 cell stops on T03 (print)", color=C["petg"])
    xi, yi = p.C_INVAR_XY                            # Invar post + reference target only (no LVDT in phase 1)
    asm.add(bp.post_foot().translate((0, 0, zb0)), name=prefix + "P04 post foot (print)", color=C["petg"])
    asm.add(cyl(p.C_INVAR_D, bp.POST_L, zb0 + bp.POST_FLOOR, xi, yi), name=prefix + f"Invar 36 post D16 x{bp.POST_L:.0f}",
            color=C["invar"])
    asm.add(bp.target_arm().translate((0, 0, bp.Z_REF_U)), name=prefix + "P03 target arm (print)", color=C["petg"])
    _optics_c(asm, prefix, led=True, orbit_angle=orbit_angle)
    return zb0


def freezer_layout():
    """Rig C (phase 2, the taller one) standing on rubber pads on the floor of the freezer, inner space
    FRZ_L × FRZ_W × FRZ_H = 590 × 390 × 410 mm (sheet V05). The rig is centred in x incl. the RPi box on the +x column."""
    asm = cq.Assembly(name="E7 freezer layout - rig C in a freezer 590 x 390 x 410")
    sub = cq.Assembly(name="rig C")
    variant_c(sub)
    bb = sub.toCompound().BoundingBox()
    dx = p.FRZ_L / 2 - (bb.xmin + bb.xmax) / 2
    dy = p.FRZ_W / 2 - (bb.ymin + bb.ymax) / 2
    asm.add(box(0, p.FRZ_L, 0, p.FRZ_W, -5, 0), name=f"freezer floor (inside {p.FRZ_L:g}x{p.FRZ_W:g})", color=C["freezer"])
    walls = box(-10, p.FRZ_L + 10, -10, p.FRZ_W + 10, 0, p.FRZ_H).cut(box(0, p.FRZ_L, 0, p.FRZ_W, 0, p.FRZ_H))
    asm.add(walls, name=f"freezer walls ({p.FRZ_H:g} high inside)", color=C["freezer"])
    asm.add(sub, loc=cq.Location((dx, dy, -bb.zmin)))
    return asm


def freezer_clearance():
    """(height of the rig, gap to the lid, side gaps x, y) for variant C and U in the freezer."""
    out = {}
    for name, fn in (("C", variant_c), ("U", variant_u)):
        a = cq.Assembly(); fn(a)
        bb = a.toCompound().BoundingBox()
        out[name] = (bb.zlen, p.FRZ_H - bb.zlen, (p.FRZ_L - bb.xlen) / 2, (p.FRZ_W - bb.ylen) / 2)
    return out


def export_parts(asm, folder):
    """One STEP per part (for drawings in Onshape); names from the assembly."""
    os.makedirs(folder, exist_ok=True)
    for f in os.listdir(folder):
        if f.endswith(".step"):
            os.remove(os.path.join(folder, f))
    n = 0
    for shape, name, loc, color in asm:
        nm = name.split("/")[-1]
        safe = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in nm).strip("_")
        cq.exporters.export(cq.Workplane().add(shape.moved(loc)), os.path.join(folder, safe + ".step"))
        n += 1
    return n


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    ARCH = os.path.join(OUT, "archiv")
    os.makedirs(ARCH, exist_ok=True)
    vc = cq.Assembly(name="E7 C - phase 2: dead weight on a partial piston, camera orbits round the rod, laser, LVDT")
    variant_c(vc)
    mr = cq.Assembly(name=f"E7 cell rev. B - printed in one piece D{p.BODY_D + 2 * p.C_SLEEVE_T:g} (core Column_one_body_version_1)")
    body_a(mr, temps=[], pv=False, pb=False, opt=False, ins=True, pt_port=True)
    # print-ready cell (bottom on the bed, z = 0) for vyroba/tisk
    cell = [sh.moved(loc) for sh, n, loc, c in mr if n.split("/")[-1].startswith("cell PETG")][0]
    bb = cell.BoundingBox()
    cell = cell.translate(cq.Vector(-(bb.xmin + bb.xmax) / 2, -(bb.ymin + bb.ymax) / 2, -bb.zmin))
    tisk = os.path.join(OUT, "..", "vyroba", "tisk")
    os.makedirs(tisk, exist_ok=True)
    cname = f"E7-V03_cell_D{bb.xlen:.0f}x{bb.zlen:.0f}"
    cq.exporters.export(cell, os.path.join(tisk, cname + ".stl"), tolerance=0.05, angularTolerance=0.1)
    cq.exporters.export(cell, os.path.join(tisk, cname + ".step"))
    print(cname, "for printing")
    # phase 1 – variant U without load: flat-top cell 5 mm above the sand
    vu = cq.Assembly(name="E7 U - phase 1 without load, camera + laser + LED see the whole surface")
    variant_u(vu)
    mu = cq.Assembly(name="E7 cell variant U - flat top 5 mm above the sand")
    body_a(mu, temps=[], pv=False, pb=False, opt=False, ins=True, pt_port=True, top=p.U_TOP)
    cu = [sh.moved(loc) for sh, n, loc, c in mu if n.split("/")[-1].startswith("cell PETG")][0]
    bu = cu.BoundingBox()
    cu = cu.translate(cq.Vector(-(bu.xmin + bu.xmax) / 2, -(bu.ymin + bu.ymax) / 2, -bu.zmin))
    uname = f"E7-V03u_cell_D{bu.xlen:.0f}x{bu.zlen:.0f}_bez_zatizeni"
    cq.exporters.export(cu, os.path.join(tisk, uname + ".stl"), tolerance=0.05, angularTolerance=0.1)
    cq.exporters.export(cu, os.path.join(tisk, uname + ".step"))
    print(uname, "for printing")
    vu.save(os.path.join(OUT, "E7_V07_bez_zatizeni.step"))
    cq.exporters.export(vu.toCompound(), os.path.join(OUT, "E7_V07_bez_zatizeni.stl"), tolerance=0.2, angularTolerance=0.3)
    vu.export(os.path.join(OUT, "E7_V07_bez_zatizeni.glb"), tolerance=0.15, angularTolerance=0.2)
    vc.export(os.path.join(OUT, "E7_sestava_final.glb"), tolerance=0.15, angularTolerance=0.2)
    print("E7_V07_bez_zatizeni ok", len(vu.children))
    lay = freezer_layout()
    for asm, fn in ((vc, "E7_V01_variant_C"), (mr, "E7_V03_cell"), (lay, "E7_V05_freezer_layout")):
        asm.save(os.path.join(OUT, fn + ".step"))
        cq.exporters.export(asm.toCompound(), os.path.join(OUT, fn + ".stl"), tolerance=0.2, angularTolerance=0.3)
        print(fn, "ok", len(asm.children))
    print("parts_V01_variant_C", export_parts(vc, os.path.join(OUT, "parts_V01_variant_C")), "parts")
    # archive: earlier variants A and B (not part of the current design)
    b = cq.Assembly(name="archive - variant B anchors"); variant_b(b)
    am = cq.Assembly(name="archive - variant A tie rods"); variant_a_min(am)
    af = cq.Assembly(name="archive - variant A frame"); variant_a_frame(af)
    bo = cq.Assembly(name="archive - variant B open"); variant_b_open(bo)
    for asm, fn in ((am, "A_tie_rods"), (af, "A_frame"), (b, "B_anchors"), (bo, "B_open")):
        asm.save(os.path.join(ARCH, fn + ".step"))
        print("archiv/" + fn, "ok")
