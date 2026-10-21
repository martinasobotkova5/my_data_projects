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


def m_point(asm, prefix=""):
    """Measuring point M: 3-rod mini TDR probe, Pt100 and FBG side by side at one depth."""
    z = Z_S1 - p.M_DEPTH
    a = p.M_ANG
    r_wall = p.D_SAMPLE / 2
    hw, hh, hd = p.TDR_HEAD
    head = box(R_OUT - 2, R_OUT - 2 + hd, -hw / 2, hw / 2, z - hh / 2, z + hh / 2).rotate((0, 0, 0), (0, 0, 1), a)
    asm.add(head, name=prefix + "M TDR probe head (epoxy)", color=C["tdr"])
    for i, dz in enumerate(p.TDR_RODS_DZ, 1):
        asm.add(radial_off(a, r_wall - p.TDR_ROD_L, R_OUT, z + dz, p.TDR_ROD_D),
                name=f"{prefix}M TDR rod {i} D1.6", color=C["steel"])
    asm.add(radial_off(a, R_OUT + hd - 2, R_OUT + 60, z, 5.0), name=prefix + "M TDR coax cable", color=C["tdr"])
    asm.add(radial_off(a, p.PT100_TIP_R, R_OUT + INS_T + 25, z, p.PT100_D, w=p.M_SIDE),
            name=prefix + "M Pt100 1/10 DIN D3", color=C["pt100"])
    asm.add(radial_off(a, p.FBG_TIP_R, R_OUT + INS_T + 25, z, p.FBG_D, w=-p.M_SIDE),
            name=prefix + "M FBG temperature sensor (capillary D1)", color=C["fbg"])


def m_boss_cuts(cell, liner, ins):
    """Printed boss for point M on the cell wall + holes in wall, liner and insulation."""
    z = Z_S1 - p.M_DEPTH
    a = p.M_ANG
    bw, bh, bt = p.M_BOSS
    hw, hh, hd = p.TDR_HEAD
    cell = cell.union(box(R_OUT - 2, R_OUT + bt, -bw / 2, bw / 2, z - bh / 2, z + bh / 2)
                      .rotate((0, 0, 0), (0, 0, 1), a))
    cell = cell.cut(box(R_OUT - 2, R_OUT + bt + 1, -hw / 2 - 0.3, hw / 2 + 0.3, z - hh / 2 - 0.3, z + hh / 2 + 0.3)
                    .rotate((0, 0, 0), (0, 0, 1), a))
    for dz in p.TDR_RODS_DZ:
        cell = cell.cut(radial_off(a, R_IN - 1, R_OUT, z + dz, p.TDR_ROD_D + 0.2))
        liner = liner.cut(radial_off(a, p.D_SAMPLE / 2 - 1, R_IN + 1, z + dz, p.TDR_ROD_D + 0.6))
    for w, d in ((p.M_SIDE, p.PT100_D), (-p.M_SIDE, p.FBG_D)):
        cell = cell.cut(radial_off(a, R_IN - 1, R_OUT + bt + 1, z, d + 0.2, w))
        liner = liner.cut(radial_off(a, p.D_SAMPLE / 2 - 1, R_IN + 1, z, d + 0.6, w))
    ins = ins.cut(box(R_OUT - 1, R_OUT + bt + 1, -bw / 2 - 1, bw / 2 + 1, z - bh / 2 - 1, z + bh / 2 + 1)
                  .rotate((0, 0, 0), (0, 0, 1), a))
    return cell, liner, ins


def solid_cell(asm, prefix="", t_tip=None, temps=None, wall_cells=True):
    """Solid 3D-printed PETG-CF cell: wall 8, foot D150, thermistor bosses, PW holders, PTFE liner,
    Kaiflex 25 insulation; thermistors T1–T5 and wall pressure sensors PW1–3."""
    cell = tube(p.D_CELL_OUT, p.D_CELL_IN, CELL_H, Z_S0)
    cell = cell.union(tube(p.CELL_FOOT_D, p.D_CELL_IN, p.CELL_FOOT_T, Z_S0))
    liner = tube(p.D_CELL_IN, p.D_SAMPLE, CELL_H, Z_S0)
    ins = tube(2 * (R_OUT + INS_T), 2 * R_OUT, CELL_H - p.CELL_FOOT_T, Z_S0 + p.CELL_FOOT_T)
    temps = WALL_TH if temps is None else temps
    for d, ang in temps:
        z = Z_S1 - d
        cell = cell.union(box(R_OUT - 2, R_OUT + 8, -5, 5, z - 5, z + 5).rotate((0, 0, 0), (0, 0, 1), ang))
        cell = cell.cut(radial(ang, R_IN - 1, R_OUT + 9, z, 1.7))
        ins = ins.cut(box(R_OUT - 1, R_OUT + 9, -6, 6, z - 6, z + 6).rotate((0, 0, 0), (0, 0, 1), ang))
    for tag, d, ang in (p.PWALL if wall_cells else []):
        z = Z_S1 - d
        cell = cell.union(box(R_OUT - 2, R_OUT + 8, -6, 6, z - 6, z + 6).rotate((0, 0, 0), (0, 0, 1), ang))
        cell = cell.cut(radial(ang, R_IN - 1, R_OUT + 9, z, p.PWALL_D + 0.2))
        liner = liner.cut(radial(ang, p.D_SAMPLE / 2 - 1, R_IN + 1, z, p.PWALL_D + 0.2))
        ins = ins.cut(box(R_OUT - 1, R_OUT + 9, -7, 7, z - 7, z + 7).rotate((0, 0, 0), (0, 0, 1), ang))
        asm.add(radial(ang, p.D_SAMPLE / 2, R_OUT + 14, z, p.PWALL_D), name=f"{prefix}{tag} wall pressure sensor",
                color=C["pressure"])
    cell, liner, ins = m_boss_cuts(cell, liner, ins)
    m_point(asm, prefix)
    asm.add(cell, name=prefix + "cell PETG-CF (solid print)", color=C["petg"])
    asm.add(liner, name=prefix + "PTFE liner 0.5", color=C["ptfe"])
    asm.add(ins, name=prefix + "insulation Kaiflex 25", color=C["ins"])
    t_tip = t_tip or p.T_TIP_R
    for i, (d, ang) in enumerate(temps, 1):
        asm.add(radial(ang, t_tip, R_OUT + INS_T + 15, Z_S1 - d, 1.6), name=f"{prefix}T{i} 109SS", color=C["temp"])


def cell_stack(asm, prefix=""):
    asm.add(cyl(150, G10_T, H_BOT), name=prefix + "G10 thermal break", color=C["g10"])
    ped = cyl(150, p.PEDESTAL_H, Z_PED).cut(cyl(99.6, 10, Z_S0 - 10))
    asm.add(ped, name=prefix + "pedestal Al", color=C["al"])
    asm.add(cyl(99.5, 10, Z_S0 - 10), name=prefix + "porous stone bottom", color=C["stone"])
    solid_cell(asm, prefix)
    _piston_and_sensors(asm, prefix, sand=True)
    embedded_cells(asm, prefix)
    base_cells(asm, prefix)


def embedded_cells(asm, prefix=""):
    """Miniature earth pressure cells inside the sand (variant A)."""
    for tag, kind, d, rr, ang in p.PCELLS:
        z = Z_S1 - d
        x, y = rr * math.cos(math.radians(ang)), rr * math.sin(math.radians(ang))
        if kind == "v":
            c = cyl(p.PCELL_D, p.PCELL_T, z - p.PCELL_T / 2, x, y)
            label = "vertical stress"
        else:
            c = (cq.Workplane("YZ").circle(p.PCELL_D / 2).extrude(p.PCELL_T)
                 .translate((rr - p.PCELL_T / 2, 0, z)).rotate((0, 0, 0), (0, 0, 1), ang))
            label = "radial stress"
        asm.add(c, name=f"{prefix}{tag} earth pressure cell ({label})", color=C["pressure"])
        asm.add(radial(ang, rr + p.PCELL_D / 2 * (kind == "v"), R_OUT + INS_T + 15, z, 2.5),
                name=f"{prefix}{tag} cable", color=C["pressure"])


def base_cells(asm, prefix=""):
    for tag, rr, ang in p.PBASE:
        x, y = rr * math.cos(math.radians(ang)), rr * math.sin(math.radians(ang))
        asm.add(cyl(8, 1.5, Z_S0 - 1.5, x, y), name=f"{prefix}{tag} base pressure sensor (flush)",
                color=C["pressure"])


def _piston_and_sensors(asm, prefix, sand=False):
    asm.add(cyl(p.D_SAMPLE, p.H_SAMPLE, Z_S0),
            name=prefix + ("unsaturated sand D100x100" if sand else "soil sample D100x100"),
            color=C["sand"] if sand else C["soil"])
    asm.add(cyl(99.5, 10, Z_S1), name=prefix + "porous stone top", color=C["stone"])
    asm.add(cyl(99.5, Z_PT - Z_S1 - 10, Z_S1 + 10), name=prefix + "piston Al", color=C["al"])
    asm.add(cyl(140, 5, Z_PT), name=prefix + "LVDT target plate", color=C["al"])
    asm.add(cq.Workplane("XY").sphere(6).translate((0, 0, BALL_C)), name=prefix + "steel ball D12",
            color=C["steel"])
    # thermistor probes (Campbell 109SS, D1.6)
    asm.add(radial(180, 10, 74, Z_PED + 15, 1.6), name=prefix + "Tbot 109SS", color=C["temp"])
    asm.add(radial(0, 10, 49, Z_PT - 8, 1.6), name=prefix + "Ttop 109SS", color=C["temp"])
    # Invar reference with 2 LVDTs (RDP DCTH400)
    if sand:      # variant A: weights above → LVDTs at ±y on tabs of the target plate
        for s in (-1, 1):
            asm.add(box(-10, 10, s * 60, s * (p.LVDT_R + 6), Z_PT, Z_PT + 5) if s > 0 else
                    box(-10, 10, s * (p.LVDT_R + 6), s * 60, Z_PT, Z_PT + 5),
                    name=f"{prefix}target tab {'+y' if s > 0 else '-y'}", color=C["al"])
            n = 1 if s < 0 else 2
            asm.add(cyl(19, 60, Z_LC, 0, s * p.LVDT_R), name=f"{prefix}LVDT-{n} DCTH400", color=C["sensor"])
            asm.add(cyl(4, Z_LC - Z_TGT, Z_TGT, 0, s * p.LVDT_R), name=f"{prefix}LVDT-{n} plunger", color=C["steel"])
            asm.add(cyl(10, Z_LC + 60, 0, 25, s * p.LVDT_R), name=f"{prefix}Invar post {n}", color=C["invar"])
            arm = box(0, 25, s * p.LVDT_R - 6, s * p.LVDT_R + 6, Z_LC + 50, Z_LC + 60) if s > 0 else \
                box(0, 25, s * p.LVDT_R - 6, s * p.LVDT_R + 6, Z_LC + 50, Z_LC + 60)
            asm.add(arm, name=f"{prefix}LVDT clamp arm {n}", color=C["invar"])
        return
    for s in (-1, 1):
        asm.add(cyl(10, 300, 0, s * 62, -75), name=f"{prefix}Invar rod {'L' if s < 0 else 'R'}", color=C["invar"])
        asm.add(cyl(19, 60, Z_LC, s * 62, 0), name=f"{prefix}LVDT-{1 if s < 0 else 2} DCTH400", color=C["sensor"])
        asm.add(cyl(4, Z_LC - Z_TGT, Z_TGT, s * 62, 0), name=f"{prefix}LVDT-{1 if s < 0 else 2} plunger",
                color=C["steel"])
    bridge = box(-75, 75, -85, 12, 300, 308).cut(cyl(60, 8, 300))
    for s in (-1, 1):
        bridge = bridge.union(box(s * 62 - 12, s * 62 + 12, -10, 12, Z_LC + 60, 300))
    asm.add(bridge, name=prefix + "Invar/Al LVDT bridge", color=C["invar"])


def variant_a(asm, prefix=""):
    """Variant A: unsaturated sand in the solid printed cell, pressure sensors, dead-weight surcharge ≤ 25 kPa."""
    zb = p.FRAME_H_A
    hb, hd = p.BASE_W / 2, p.BASE_D / 2
    asm.add(box(-hb, hb, -hd, hd, -p.BASE_T, 0), name=prefix + "base plate Al 6082", color=C["al"])
    for i, (x, y) in enumerate(((-hb + 20, -hd + 20), (hb - 20, -hd + 20), (0, hd - 20))):
        asm.add(cyl(16, 18, -p.BASE_T - 18, x, y), name=f"{prefix}levelling foot {i + 1}", color=C["steel"])
    for s in (-1, 1):
        asm.add(box(s * X_COL - 20, s * X_COL + 20, -20, 20, 0, zb),
                name=f"{prefix}column 40x40 {'L' if s < 0 else 'R'}", color=C["profile"])
    bar = box(-X_COL - 20, X_COL + 20, -20, 20, zb, zb + p.BEAM_H_A).cut(cyl(28, p.BEAM_H_A, zb))
    asm.add(bar, name=prefix + "cross-bar 40x40 (guide only)", color=C["profile"])
    asm.add(tube(28, p.DW_ROD_D + 0.1, p.BEAM_H_A, zb), name=prefix + "linear ball bushing D16", color=C["steel"])
    asm.add(cyl(60, H_BOT, 0), name=prefix + "Al spacer (bottom)", color=C["al"])
    cell_stack(asm, prefix)
    zg = Z_LC
    asm.add(cyl(p.DW_G10_D, p.DW_G10_T, zg), name=prefix + "G10 thermal break D60x10", color=C["g10"])
    zc = zg + p.DW_G10_T
    asm.add(cyl(p.DW_D, p.DW_CARRIER_T, zc), name=prefix + "carrier plate steel D150x10", color=C["steel"])
    asm.add(cyl(p.DW_ROD_D, p.DW_ROD_L, zc + p.DW_CARRIER_T), name=prefix + "guide rod D16", color=C["steel"])
    z = zc + p.DW_CARRIER_T
    for i, t in enumerate((p.DW_FULL_T,) * 3 + (p.DW_HALF_T,), 1):
        asm.add(tube(p.DW_D, p.DW_HOLE, t - 0.5, z), name=f"{prefix}steel disc {i} D150x{t:g}", color=C["weight"])
        z += t
    asm.add(radial(0, 30, 75, (zc + z) / 2, 1.6), name=prefix + "Tw 109SS (weights)", color=C["temp"])


def variant_b(asm, prefix=""):
    """Variant B: same sand sample in the same printed cell, no load; surface + anchor LVDTs on an Invar stand."""
    hb, hd = p.BASE_W / 2, p.BASE_D / 2
    asm.add(box(-hb, hb, -hd, hd, -p.BASE_T, 0), name=prefix + "base plate Al 6082", color=C["al"])
    for i, (x, y) in enumerate(((-hb + 20, -hd + 20), (hb - 20, -hd + 20), (0, hd - 20))):
        asm.add(cyl(16, 18, -p.BASE_T - 18, x, y), name=f"{prefix}levelling foot {i + 1}", color=C["steel"])
    asm.add(cyl(60, H_BOT, 0), name=prefix + "Al spacer (bottom)", color=C["al"])
    asm.add(cyl(150, G10_T, H_BOT), name=prefix + "G10 thermal break", color=C["g10"])
    ped = cyl(150, p.PEDESTAL_H, Z_PED).cut(cyl(99.6, 10, Z_S0 - 10))
    asm.add(ped, name=prefix + "pedestal Al", color=C["al"])
    asm.add(cyl(99.5, 10, Z_S0 - 10), name=prefix + "porous stone bottom", color=C["stone"])
    solid_cell(asm, prefix)
    z_tp = Z_S1 + p.TOP_PLATE_T
    sand = cyl(p.D_SAMPLE, p.H_SAMPLE, Z_S0)
    plate = cyl(p.TOP_PLATE_D, p.TOP_PLATE_T, Z_S1)
    for t, d, r, ang in p.ANCHORS:
        x, y = r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang))
        plate = plate.cut(cyl(p.PLATE_HOLE_D, p.TOP_PLATE_T, Z_S1, x, y))
    asm.add(sand, name=prefix + "unsaturated sand D100x100", color=C["sand"])
    asm.add(plate, name=prefix + "top plate PETG-CF D99x6", color=C["petg"])
    asm.add(radial(0, 5, 45, Z_S1 + p.TOP_PLATE_T / 2, 1.6), name=prefix + "Ttop 109SS (in top plate)",
            color=C["temp"])
    asm.add(radial(180, 10, 74, Z_PED + 15, 1.6), name=prefix + "Tbot 109SS", color=C["temp"])
    bd, bl = p.LVDT_B_BODY
    z_body = p.Z_BRIDGE - 35.0
    for t, r, ang in p.SURF_LVDT:
        x, y = r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang))
        asm.add(cyl(5, 3, z_tp, x, y), name=f"{prefix}{t} rod seat", color=C["steel"])
        asm.add(cyl(3, z_body + 20 - z_tp - 3, z_tp + 3, x, y), name=f"{prefix}{t} core rod D3", color=C["steel"])
        asm.add(tube(bd, 4, bl, z_body).translate((x, y, 0)), name=f"{prefix}{t} LVDT DCTH200 free core",
                color=C["sensor"])
    for t, d, r, ang in p.ANCHORS:
        x, y = r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang))
        z = Z_S1 - d
        asm.add(cyl(p.ANCHOR_D, p.ANCHOR_T, z - p.ANCHOR_T / 2, x, y), name=f"{prefix}{t} anchor D16 stainless",
                color=C["steel"])
        asm.add(tube(p.SLEEVE_D, p.ROD_D + 0.5, z_tp + 4 - (z + 2), z + 2).translate((x, y, 0)),
                name=f"{prefix}{t} PTFE sleeve D4", color=C["ptfe"])
        asm.add(cyl(p.ROD_D, z_body + 20 - z, z, x, y), name=f"{prefix}{t} Invar rod D2", color=C["invar"])
        asm.add(tube(bd, 4, bl, z_body).translate((x, y, 0)), name=f"{prefix}{t} LVDT DCTH200 free core",
                color=C["sensor"])
    for i, ang in enumerate(p.STAND_ANG, 1):
        x, y = p.STAND_R * math.cos(math.radians(ang)), p.STAND_R * math.sin(math.radians(ang))
        asm.add(cyl(p.STAND_POST_D, p.Z_BRIDGE, 0, x, y), name=f"{prefix}Invar post {i}", color=C["invar"])
    bridge = cyl(p.BRIDGE_D, p.BRIDGE_T, p.Z_BRIDGE)
    for t, r, ang in p.SURF_LVDT + [(a[0], a[2], a[3]) for a in p.ANCHORS]:
        bridge = bridge.cut(cyl(bd + 0.5, p.BRIDGE_T, p.Z_BRIDGE, r * math.cos(math.radians(ang)),
                                r * math.sin(math.radians(ang))))
    asm.add(bridge, name=prefix + "Al bridge D220x10 (LVDT clamps)", color=C["al"])
    asm.add(radial(180, p.STAND_R - 6, p.STAND_R + 20, 230, 1.6), name=prefix + "Tstand 109SS", color=C["temp"])


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
    asm.add(cyl(150, p.AM_G10_T, zb0), name=prefix + "G10 thermal break D150x10", color=C["g10"])
    xb, yb = p.AM_PB[1] * math.cos(math.radians(p.AM_PB[2])), p.AM_PB[1] * math.sin(math.radians(p.AM_PB[2]))
    bottom = cyl(150, p.AM_BOTTOM_T, zb0 + p.AM_G10_T).cut(cyl(8.2, 1.5, Z_S0 - 1.5, xb, yb))
    asm.add(bottom, name=prefix + "Al bottom D150x15", color=C["al"])
    asm.add(cyl(8, 1.5, Z_S0 - 1.5, xb, yb), name=prefix + "PB1 TML PDA-PA (flush)", color=C["pressure"])
    solid_cell(asm, prefix, temps=[(d, a) for _, d, a in p.AM_TEMPS], wall_cells=False)
    asm.add(cyl(p.D_SAMPLE, p.H_SAMPLE, Z_S0), name=prefix + "unsaturated sand D100x100", color=C["sand"])
    asm.add(cyl(p.PCELL_D, p.PCELL_T, Z_S1 - p.AM_PV[1] - p.PCELL_T / 2), name=prefix + "PV1 TML PDA-PA on D20 disc",
            color=C["pressure"])
    asm.add(radial(0, p.PCELL_D / 2, R_OUT + INS_T + 15, Z_S1 - p.AM_PV[1], 2.5), name=prefix + "PV1 cable",
            color=C["pressure"])
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


def freezer_layout():
    asm = cq.Assembly(name="E7 freezer layout")
    z_tray = 20.0
    z0 = z_tray + 40 + 18 + p.BASE_T        # base plate top on feet on the tray
    sub_b, sub_a = cq.Assembly(name="rig B"), cq.Assembly(name="rig A")
    variant_b(sub_b)
    variant_a(sub_a)
    # chest freezer inside (origin at inner floor corner), tray and mat
    asm.add(box(0, p.FRZ_L, 0, p.FRZ_W, -5, 0), name="freezer floor (inside ≈ 900x550)", color=C["freezer"])
    walls = box(-10, p.FRZ_L + 10, -10, p.FRZ_W + 10, 0, p.FRZ_H).cut(box(0, p.FRZ_L, 0, p.FRZ_W, 0, p.FRZ_H))
    asm.add(walls, name="freezer walls (≈ 650 high)", color=C["freezer"])
    asm.add(box(620, 885, 15, 535, 0, 230), name="compressor step (if present)", color=C["freezer"])
    asm.add(box(25, 610, 70, 480, 0, z_tray), name="insulation mat", color=C["ins"])
    tray = box(50, 50 + p.TRAY_L, 105, 105 + p.TRAY_W, z_tray, z_tray + 40)
    tray = tray.cut(box(51.5, 48.5 + p.TRAY_L, 106.5, 103.5 + p.TRAY_W, z_tray + 1.5, z_tray + 41))
    asm.add(tray, name="stainless tray", color=C["tray"])
    asm.add(sub_b, loc=cq.Location((185, 275, z0)))
    asm.add(sub_a, loc=cq.Location((445, 275, z0)))
    return asm


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    a = cq.Assembly(name="E7 variant A - dead weight <= 25 kPa, unsaturated sand")
    variant_a(a)
    b = cq.Assembly(name="E7 variant B - no load, heave and layer strain")
    variant_b(b)
    mr = cq.Assembly(name="E7 cell PETG-CF")
    solid_cell(mr)
    am = cq.Assembly(name="E7 variant A-min - fixed lid")
    variant_a_min(am)
    lay = freezer_layout()
    for asm, fn in ((a, "E7_variant_A"), (b, "E7_variant_B"), (mr, "E7_cell"), (am, "E7_variant_A_min"),
                    (lay, "E7_freezer_layout")):
        asm.save(os.path.join(OUT, fn + ".step"))
        cq.exporters.export(asm.toCompound(), os.path.join(OUT, fn + ".stl"), tolerance=0.2, angularTolerance=0.3)
        print(fn, "ok", len(asm.children) if hasattr(asm, "children") else "")
