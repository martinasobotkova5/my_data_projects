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

def body_a(asm, prefix="", temps=None, pv=True, pb=True, opt=True):
    """Variant A cell per drawing Column_one_body_version_1: body ⌀160 × 130 + collar ⌀106 to 160,
    cavity ⌀100 from z 26 (z = 0 at the underside), side port 13 wide at 67.5–94.5 (PORT_ANG).
    Point M: CS645 in the port, optical fibre, Pt100 vertical. Returns z of the underside."""
    zb = Z_S0 - p.BODY_BOTTOM
    rb, rc, ri = p.BODY_D / 2, p.COLLAR_OD / 2, p.CAV_D / 2
    body = cyl(p.BODY_D, p.BODY_H, zb).union(cyl(p.COLLAR_OD, p.COLLAR_TOP - p.BODY_H, zb + p.BODY_H))
    body = body.cut(cyl(p.CAV_D, p.COLLAR_TOP - p.BODY_BOTTOM, zb + p.BODY_BOTTOM))
    port = box(ri + p.CUP_WALL_IN, rb + 1, -p.PORT_W / 2, p.PORT_W / 2, zb + p.PORT_Z0, zb + p.PORT_Z1)
    body = body.cut(port.rotate((0, 0, 0), (0, 0, 1), p.PORT_ANG))
    t = p.TDR_CS645
    z_top = zb + p.COLLAR_TOP - t["top_from_collar"]
    a = p.PORT_ANG
    for k in range(3):
        body = body.cut(radial(a, ri - 1, ri + p.CUP_WALL_IN + 1, z_top - k * t["pitch"], t["rod_d"] + 0.3))
    body = body.cut(radial_off(a, ri - 1, ri + p.CUP_WALL_IN + 1, z_top + 2, 1.5, w=p.OF_SIDE))
    temps = [(d, ang) for _, d, ang in p.AM_TEMPS] if temps is None else temps
    for d, ang in temps:
        body = body.cut(radial(ang, ri - 1, rb + 1, Z_S1 - d, 2.0))
    if pv:
        body = body.cut(radial(90, ri - 1, rb + 1, Z_S1 - p.AM_PV[1], 3.5))
    body = body.cut(radial(0, ri - 1, rb + 1, Z_S1 - 1, 4.0))
    xb, yb = 25 * math.cos(math.radians(p.AM_PB[2])), 25 * math.sin(math.radians(p.AM_PB[2]))
    if pb:
        body = body.cut(cyl(8.2, 1.6, Z_S0 - 1.6, xb, yb))
    asm.add(body, name=prefix + "cell body PETG D160 (Column_one_body_version_1)", color=C["petg"])
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
    xp, yp = p.PT100_R * math.cos(math.radians(a + 90)), p.PT100_R * math.sin(math.radians(a + 90))
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


def freezer_layout():
    """Both rigs on the tray in the chest freezer (sheet V08): A-frame left, B-open turned 90° right."""
    asm = cq.Assembly(name="E7 freezer layout")
    z_tray = 20.0
    sub_a, sub_b = cq.Assembly(name="rig A-frame"), cq.Assembly(name="rig B-open")
    variant_a_frame(sub_a)
    zb_b = variant_b_open(sub_b)
    asm.add(box(0, p.FRZ_L, 0, p.FRZ_W, -5, 0), name="freezer floor (inside ≈ 900x550)", color=C["freezer"])
    walls = box(-10, p.FRZ_L + 10, -10, p.FRZ_W + 10, 0, p.FRZ_H).cut(box(0, p.FRZ_L, 0, p.FRZ_W, 0, p.FRZ_H))
    asm.add(walls, name="freezer walls (≈ 650 high)", color=C["freezer"])
    asm.add(box(620, 885, 15, 535, 0, 230), name="compressor step (if present)", color=C["freezer"])
    asm.add(box(25, 610, 70, 480, 0, z_tray), name="insulation mat", color=C["ins"])
    tray = box(50, 50 + p.TRAY_L, 105, 105 + p.TRAY_W, z_tray, z_tray + 40)
    tray = tray.cut(box(51.5, 48.5 + p.TRAY_L, 106.5, 103.5 + p.TRAY_W, z_tray + 1.5, z_tray + 41))
    asm.add(tray, name="stainless tray", color=C["tray"])
    z_top_tray = z_tray + 1.5
    zbA = Z_S0 - p.AM_BOTTOM_T - p.AM_G10_T - p.AF_BASE[2] - 18
    ax = 50 + 10 + p.AF_BASE[0] / 2
    asm.add(sub_a, loc=cq.Location((ax, 105 + p.TRAY_W / 2, z_top_tray - zbA)))
    zbB = zb_b - p.BC_BASE[2]
    bx_ = ax + p.AF_BASE[0] / 2 + 15 + p.BC_BASE[1] / 2
    asm.add(sub_b, loc=cq.Location((bx_, 105 + p.TRAY_W / 2 + 20, z_top_tray - zbB), (0, 0, 1), 90))
    return asm


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
    b = cq.Assembly(name="E7 V05 variant B - anchors, layer strain")
    variant_b(b)
    mr = cq.Assembly(name="E7 V04 cell A - Column_one_body_version_1")
    body_a(mr)
    am = cq.Assembly(name="E7 V02 variant A - fixed lid on tie rods")
    variant_a_min(am)
    af = cq.Assembly(name="E7 V03 variant A - fixed piston in Al frame")
    variant_a_frame(af)
    bo = cq.Assembly(name="E7 V06 variant B - open surface, camera + laser")
    variant_b_open(bo)
    lay = freezer_layout()
    for asm, fn in ((am, "E7_V02_variant_A_tie_rods"), (af, "E7_V03_variant_A_frame"), (mr, "E7_V04_cell"),
                    (b, "E7_V05_variant_B_anchors"), (bo, "E7_V06_variant_B_open"), (lay, "E7_V08_freezer_layout")):
        asm.save(os.path.join(OUT, fn + ".step"))
        cq.exporters.export(asm.toCompound(), os.path.join(OUT, fn + ".stl"), tolerance=0.2, angularTolerance=0.3)
        print(fn, "ok", len(asm.children))
    for asm, folder in ((af, "parts_V03_variant_A_frame"), (bo, "parts_V06_variant_B_open")):
        print(folder, export_parts(asm, os.path.join(OUT, folder)), "parts")
