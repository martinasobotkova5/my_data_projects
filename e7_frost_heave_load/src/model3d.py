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

# multi-ring cell (variant A option): rings slide on 3 guide rods
MR_FOOT_T = 8.0          # base ring with flange ⌀150
MR_RING_H = 10.0
MR_WASHER = 1.0          # PTFE washer between rings
MR_N = 10
MR_LATEX = 0.3           # greased latex membrane
MR_ID = p.D_SAMPLE + 2 * MR_LATEX + 0.4     # 101.0 incl. clearance
MR_LUG_R = 63.0          # guide rods ⌀5 at r 63, 3× 120°
MR_INS_IN, MR_INS_T = 71.0, 18.0   # clears the lugs (r 70) and the columns (r 90)
MR_PROBE_ANG = (0, 60, 120, 180, 240)   # 30° away from the guide-rod lugs (90/210/330)


def mr_ring_z(k):
    """Bottom z of ring k (0 = lowest moving ring)."""
    return Z_S0 + MR_FOOT_T + MR_WASHER + k * (MR_RING_H + MR_WASHER)


def mr_probe_positions():
    """Thermistor heights: centre of the ring nearest to each target depth."""
    out = []
    for (d, _), ang in zip(WALL_TH, MR_PROBE_ANG):
        z_t = Z_S1 - d
        k = min(range(MR_N), key=lambda i: abs(mr_ring_z(i) + MR_RING_H / 2 - z_t))
        out.append((k, mr_ring_z(k) + MR_RING_H / 2, ang))
    return out

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


def multiring_cell(asm, prefix="", with_sample=False):
    """Multi-ring cell: base ring with flange, 10 rings h 10 with lugs, PTFE washers,
    3 guide rods, greased latex membrane, thermistor bosses on the rings."""
    foot = tube(p.CELL_FOOT_D, MR_ID, MR_FOOT_T, Z_S0)
    for ang in (90, 210, 330):
        foot = foot.cut(cyl(5.2, MR_FOOT_T, Z_S0, MR_LUG_R * math.cos(math.radians(ang)),
                            MR_LUG_R * math.sin(math.radians(ang))))
    asm.add(foot, name=prefix + "multi-ring base ring PETG-CF", color=C["petg"])
    probes = {k: (z, ang) for k, z, ang in mr_probe_positions()}
    walls = {}
    for tag, d, ang in p.PWALL:
        z_t = Z_S1 - d
        k = min(range(MR_N), key=lambda i: abs(mr_ring_z(i) + MR_RING_H / 2 - z_t))
        walls[k] = (tag, mr_ring_z(k) + MR_RING_H / 2, ang)
    for k in range(MR_N):
        z0 = mr_ring_z(k)
        ring = tube(p.D_CELL_OUT, MR_ID, MR_RING_H, z0)
        for ang in (90, 210, 330):
            lug = (cq.Workplane("XY").workplane(offset=z0).center(MR_LUG_R, 0).rect(14, 14).extrude(MR_RING_H)
                   .union(cq.Workplane("XY").workplane(offset=z0).center((R_OUT + MR_LUG_R) / 2 - 1, 0)
                          .rect(MR_LUG_R - R_OUT + 2, 14).extrude(MR_RING_H))
                   .rotate((0, 0, 0), (0, 0, 1), ang))
            ring = ring.union(lug)
            ring = ring.cut(cyl(5.6, MR_RING_H, z0, MR_LUG_R * math.cos(math.radians(ang)),
                                MR_LUG_R * math.sin(math.radians(ang))))
        if k in probes:
            z, ang = probes[k]
            ring = ring.union(box(R_OUT - 2, R_OUT + 6, -5, 5, z0, z0 + MR_RING_H)
                              .rotate((0, 0, 0), (0, 0, 1), ang))
            ring = ring.cut(radial(ang, MR_ID / 2 - 1, R_OUT + 7, z, 1.7))
        if k in walls:
            tag, z, ang = walls[k]
            ring = ring.union(box(R_OUT - 2, R_OUT + 6, -7, 7, z0, z0 + MR_RING_H)
                              .rotate((0, 0, 0), (0, 0, 1), ang))
            ring = ring.cut(radial(ang, MR_ID / 2 - 1, R_OUT + 7, z, p.PWALL_D + 0.2))
            asm.add(radial(ang, MR_ID / 2, R_OUT + 14, z, p.PWALL_D), name=f"{prefix}{tag} wall pressure sensor",
                    color=C["pressure"])
        asm.add(ring, name=f"{prefix}ring {k + 1:02d} PETG-CF", color=C["petg"])
        asm.add(tube(MR_LUG_R * 2 - 12, MR_ID + 2, MR_WASHER, z0 - MR_WASHER),
                name=f"{prefix}PTFE washer {k + 1:02d}", color=C["ptfe"])
    top = mr_ring_z(MR_N) - MR_WASHER
    for i, ang in enumerate((90, 210, 330), 1):
        asm.add(cyl(5, top - Z_S0 + 15, Z_S0, MR_LUG_R * math.cos(math.radians(ang)),
                    MR_LUG_R * math.sin(math.radians(ang))),
                name=f"{prefix}guide rod {i} (PTFE-coated)", color=C["steel"])
    asm.add(tube(p.D_SAMPLE + 2 * MR_LATEX, p.D_SAMPLE, top - Z_S0, Z_S0),
            name=prefix + "latex membrane 0.3 (greased)", color=cq.Color(0.85, 0.62, 0.35))
    asm.add(tube(2 * (MR_INS_IN + MR_INS_T), 2 * MR_INS_IN, top - Z_S0 - MR_FOOT_T, Z_S0 + MR_FOOT_T),
            name=prefix + "insulation Kaiflex 18", color=C["ins"])
    if with_sample:
        asm.add(cyl(p.D_SAMPLE, p.H_SAMPLE, Z_S0), name=prefix + "soil sample D100x100", color=C["soil"])
    for i, (k, z, ang) in enumerate(mr_probe_positions(), 1):
        asm.add(radial(ang, 9, MR_INS_IN + MR_INS_T + 15, z, 1.6), name=f"{prefix}T{i} 109SS", color=C["temp"])
    return top


def cell_stack(asm, variant, prefix="", multiring=False):
    asm.add(cyl(150, G10_T, H_BOT), name=prefix + "G10 thermal break", color=C["g10"])
    ped = cyl(150, p.PEDESTAL_H, Z_PED).cut(cyl(99.6, 10, Z_S0 - 10))
    asm.add(ped, name=prefix + "pedestal Al", color=C["al"])
    asm.add(cyl(99.5, 10, Z_S0 - 10), name=prefix + "porous stone bottom", color=C["stone"])
    multiring_cell(asm, prefix)
    _piston_and_sensors(asm, prefix, with_wall_probes=False, sand=True)
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
        asm.add(radial(ang, rr + p.PCELL_D / 2 * (kind == "v"), MR_INS_IN + MR_INS_T + 15, z, 2.5),
                name=f"{prefix}{tag} cable", color=C["pressure"])


def base_cells(asm, prefix=""):
    for tag, rr, ang in p.PBASE:
        x, y = rr * math.cos(math.radians(ang)), rr * math.sin(math.radians(ang))
        asm.add(cyl(8, 1.5, Z_S0 - 1.5, x, y), name=f"{prefix}{tag} base pressure sensor (flush)",
                color=C["pressure"])


def _piston_and_sensors(asm, prefix, with_wall_probes, sand=False):
    asm.add(cyl(p.D_SAMPLE, p.H_SAMPLE, Z_S0),
            name=prefix + ("unsaturated sand D100x100" if sand else "soil sample D100x100"),
            color=C["sand"] if sand else C["soil"])
    asm.add(cyl(99.5, 10, Z_S1), name=prefix + "porous stone top", color=C["stone"])
    asm.add(cyl(99.5, Z_PT - Z_S1 - 10, Z_S1 + 10), name=prefix + "piston Al", color=C["al"])
    asm.add(cyl(140, 5, Z_PT), name=prefix + "LVDT target plate", color=C["al"])
    asm.add(cq.Workplane("XY").sphere(6).translate((0, 0, BALL_C)), name=prefix + "steel ball D12",
            color=C["steel"])
    # thermistor probes (Campbell 109SS, D1.6)
    if with_wall_probes:
        for i, (d, ang) in enumerate(WALL_TH, 1):
            asm.add(radial(ang, 9, R_OUT + 40, Z_S1 - d, 1.6), name=f"{prefix}T{i} 109SS", color=C["temp"])
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
    """Variant A: unsaturated sand in the multi-ring cell, pressure sensors, dead-weight surcharge ≤ 25 kPa."""
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
    cell_stack(asm, "A", prefix, multiring=True)
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
    """Variant B: same sand sample in the multi-ring cell, no load; surface + anchor LVDTs on an Invar stand."""
    hb, hd = p.BASE_W / 2, p.BASE_D / 2
    asm.add(box(-hb, hb, -hd, hd, -p.BASE_T, 0), name=prefix + "base plate Al 6082", color=C["al"])
    for i, (x, y) in enumerate(((-hb + 20, -hd + 20), (hb - 20, -hd + 20), (0, hd - 20))):
        asm.add(cyl(16, 18, -p.BASE_T - 18, x, y), name=f"{prefix}levelling foot {i + 1}", color=C["steel"])
    asm.add(cyl(60, H_BOT, 0), name=prefix + "Al spacer (bottom)", color=C["al"])
    asm.add(cyl(150, G10_T, H_BOT), name=prefix + "G10 thermal break", color=C["g10"])
    ped = cyl(150, p.PEDESTAL_H, Z_PED).cut(cyl(99.6, 10, Z_S0 - 10))
    asm.add(ped, name=prefix + "pedestal Al", color=C["al"])
    asm.add(cyl(99.5, 10, Z_S0 - 10), name=prefix + "porous stone bottom", color=C["stone"])
    multiring_cell(asm, prefix)
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
    mr = cq.Assembly(name="E7 multi-ring cell")
    multiring_cell(mr, with_sample=False)
    lay = freezer_layout()
    for asm, fn in ((a, "E7_variant_A"), (b, "E7_variant_B"), (mr, "E7_multiring_cell"),
                    (lay, "E7_freezer_layout")):
        asm.save(os.path.join(OUT, fn + ".step"))
        cq.exporters.export(asm.toCompound(), os.path.join(OUT, fn + ".stl"), tolerance=0.2, angularTolerance=0.3)
        print(fn, "ok", len(asm.children) if hasattr(asm, "children") else "")
