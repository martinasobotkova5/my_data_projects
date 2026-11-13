"""E7 rig C rev. B3 – parts that are MADE to order (T-slot profiles cut to length, laser-cut discs, 3D-printed
parts, cut bars) and the fixing scheme, so the rig can be ordered from Czech e-shops and assembled without
machining (the only drilled hole is ⌀14 through the top beam).

  T-slot profiles slot 8              → PROFILES (cut list, used by objednavka.py and vyrobni_vykresy.py)
  laser (Al 10 / steel 12 / steel 6)  → ../vyroba/laser/*.dxf   (1 : 1, outline + holes only, one part per file)
  3D print (PETG-CF)                  → ../vyroba/tisk/*.stl + *.step
  cut bars (Invar, G10)               → cut list in objednavka.py

Coordinates of the rig (as model3d.py): x along the frame, y towards the laser (+) / camera (−), z up.
Run: python buildparts.py
"""
import math
import os

import cadquery as cq

import params as p

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "vyroba")

# --- vertical levels (model3d coordinates; sand bottom Z_S0 = 80, sand top Z_S1 = 180) -----------------
Z_S0 = 80.0
Z_S1 = Z_S0 + p.H_SAMPLE
ZC0 = Z_S0 - p.BODY_BOTTOM                       # underside of the core = top of the G10 pads
ZB0 = ZC0 - p.C_INS_T                            # top of the base frame (T-profiles)
ZBEAM = Z_S1 + p.C_BEAM_GAP                      # underside of the top beam
Z_TOP = ZBEAM + p.C_TOP[2]                       # top of the top T-profile (bearing housing hangs below it)
ZC = ZBEAM + p.C_BEAM_H + p.C_TRAVEL + 10        # underside of the carrier plate
COLLAR = (22.0, 12.0)                            # stavěcí kroužek DIN 705-A 12 (⌀22 × 12, stavěcí šroub M6)
Z_COLLAR = ZC - COLLAR[1]                        # under the carrier (carries it)
LV_D, LV_L = p.C_LVDT_BODY
Z_LV_TOP = ZC - 12                               # LVDT body top (plunger to the carrier ≈ mid-range)
Z_LV_BOT = Z_LV_TOP - LV_L
ARM_T = 12.0
Z_ARM = Z_LV_BOT                                 # LVDT arm z Z_ARM … Z_ARM + ARM_T (clamps the body bottom)
Z_RIM = ZC0 + p.COLLAR_TOP                       # top of the collar (camera sees it)
COL_H = ZBEAM - ZB0                              # column length
POST_FLOOR = 3.0                                 # printed floor of the post foot (bridges the T-slot)
POST_L = Z_ARM + ARM_T - ZB0 - POST_FLOOR        # Invar post: stands in its foot on the cross bar, top flush with the arm
_bh = math.sqrt((p.C_BALL_D / 2) ** 2 - 3.0 ** 2)   # ball ⌀7.94 sitting in a ⌀6 hole of the top piston disc
Z_BALL = Z_S1 + p.C_PISTON_H + _bh               # ball centre
Z_ROD0 = Z_BALL + p.C_BALL_D / 2                 # rod bottom (flat end on the ball)
N_DISC = 4
Z_ROD1 = ZC + p.C_CARRIER_T + N_DISC * p.C_DISC_T + 6 + 10   # rod top: above the disc stack + 0.5 kg disc
ROD_L = math.ceil(Z_ROD1 - Z_ROD0)
XC = p.C_COL_SPAN / 2

# --- 2D laser parts: outline (w, h, corner r) or circle, holes (x, y, d), slots (x0, y0, x1, y1, w) -------
def _carrier():
    return dict(name="E7-L03_carrier", mat="Al EN AW-5754 (or 6082)", t=p.C_CARRIER_T, circle=p.C_CARRIER_D,
                holes=[(0, 0, p.C_ROD_D + 0.3)], slots=[], engrave=[], qty=1)


def _piston(top):
    holes = [(0, 0, 6.0)] if top else []
    return dict(name="E7-L04_piston_top" if top else "E7-L05_piston_bottom", mat="Al EN AW-5754 (or 6082)",
                t=p.C_PISTON_H / 2, circle=p.C_PISTON_D, holes=holes, slots=[], engrave=[], qty=1)


def _disc(t, qty, name):
    return dict(name=name, mat="steel S235JR", t=t, circle=p.C_DISC_D, holes=[(0, 0, p.C_DISC_HOLE)], slots=[],
                engrave=[], qty=qty)


LASER = [_carrier(), _piston(True), _piston(False),
         _disc(p.C_DISC_T, N_DISC, "E7-L06_disc_1kg"), _disc(p.C_DISC_T / 2, 1, "E7-L07_disc_0.5kg")]


# --- T-slot profiles (slot 8, item/Bosch compatible): only cut to length, one Ø14 hole in the top beam --------
PROFILES = [
    dict(no="E7-T01", name="sloup / column", section=(40.0, 80.0), L=COL_H, qty=2, note="řez kolmý, oba stejně"),
    dict(no="E7-T02", name="podélník základny / base rail", section=(40.0, 40.0), L=p.C_BASE[1], qty=2,
         note="pod sloupy, osa x = ±150"),
    dict(no="E7-T03", name="příčka základny / base cross bar", section=(80.0, 40.0), L=2 * (p.C_RAIL_X - 20), qty=1,
         note=f"naplocho mezi podélníky, osa y = {p.C_CROSS_Y[0]:g}; nese 3 podložky G10"),
    dict(no="E7-T04", name="horní příčník / top beam", section=(80.0, 40.0), L=p.C_TOP[0], qty=1,
         note="naplocho; uprostřed svislý otvor ⌀14 skrz (vodicí tyč)"),
]


def profile_solid(sec, L, hole=False):
    """Simplified T-slot profile (outer box with 8 mm slots on every 40 mm face), along x, z 0 … h."""
    w, h = sec
    s = cq.Workplane("XY").box(L, w, h, centered=(True, True, False))
    for yy in [(-w / 2 + 20 + 40 * k) for k in range(int(w // 40))]:
        for zz, dz in ((h, -4), (0, 0)):
            s = s.cut(cq.Workplane("XY").box(L, 8, 4, centered=(True, True, False)).translate((0, yy, zz + dz)))
    for zz in [(20 + 40 * k) for k in range(int(h // 40))]:
        for yy, dy in ((w / 2, -2), (-w / 2, 2)):
            s = s.cut(cq.Workplane("XY").box(L, 4, 8).translate((0, yy + dy, zz)))
    if hole:
        s = s.cut(cq.Workplane("XY").circle(7).extrude(h))
    return s


def disc_mass(part):
    a = math.pi / 4 * ((part["circle"] / 1000) ** 2 - (part["holes"][0][2] / 1000) ** 2)
    return a * part["t"] / 1000 * p.RHO_STEEL


def laser_solid(part):
    """Extruded solid of a laser part (centred, z 0 … t)."""
    t = part["t"]
    if "rect" in part:
        w, h, r = part["rect"]
        s = cq.Workplane("XY").rect(w, h).extrude(t).edges("|Z").fillet(r)
    else:
        s = cq.Workplane("XY").circle(part["circle"] / 2).extrude(t)
    for x, y, d in part["holes"]:
        s = s.cut(cq.Workplane("XY").center(x, y).circle(d / 2).extrude(t))
    for x0, y0, x1, y1, w in part["slots"]:
        L = math.hypot(x1 - x0, y1 - y0) + w
        a = math.degrees(math.atan2(y1 - y0, x1 - x0))
        s = s.cut(cq.Workplane("XY").center((x0 + x1) / 2, (y0 + y1) / 2).slot2D(L, w, a).extrude(t))
    return s


def write_dxf(part, folder):
    import ezdxf
    doc = ezdxf.new("R2010", units=4)
    doc.layers.add("CUT", color=7)
    doc.layers.add("ENGRAVE", color=1)
    m = doc.modelspace()
    if "rect" in part:
        w, h, r = part["rect"]
        x0, y0, x1, y1 = -w / 2, -h / 2, w / 2, h / 2
        m.add_line((x0 + r, y0), (x1 - r, y0), dxfattribs={"layer": "CUT"})
        m.add_line((x1, y0 + r), (x1, y1 - r), dxfattribs={"layer": "CUT"})
        m.add_line((x1 - r, y1), (x0 + r, y1), dxfattribs={"layer": "CUT"})
        m.add_line((x0, y1 - r), (x0, y0 + r), dxfattribs={"layer": "CUT"})
        for cx, cy, a0 in ((x1 - r, y0 + r, 270), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
            m.add_arc((cx, cy), r, a0, a0 + 90, dxfattribs={"layer": "CUT"})
    else:
        m.add_circle((0, 0), part["circle"] / 2, dxfattribs={"layer": "CUT"})
    for x, y, d in part["holes"]:
        m.add_circle((x, y), d / 2, dxfattribs={"layer": "CUT"})
    for x0, y0, x1, y1, w in part["slots"]:
        a = math.atan2(y1 - y0, x1 - x0)
        nx, ny = -math.sin(a) * w / 2, math.cos(a) * w / 2
        m.add_line((x0 + nx, y0 + ny), (x1 + nx, y1 + ny), dxfattribs={"layer": "CUT"})
        m.add_line((x0 - nx, y0 - ny), (x1 - nx, y1 - ny), dxfattribs={"layer": "CUT"})
        ad = math.degrees(a)
        m.add_arc((x1, y1), w / 2, ad - 90, ad + 90, dxfattribs={"layer": "CUT"})
        m.add_arc((x0, y0), w / 2, ad + 90, ad + 270, dxfattribs={"layer": "CUT"})
    for x, y, d in part["engrave"]:
        m.add_circle((x, y), d / 2, dxfattribs={"layer": "ENGRAVE"})
    path = os.path.join(folder, f"{part['name']}_{part['t']:g}mm.dxf")
    doc.saveas(path)
    return path


# --- 3D-printed parts (PETG-CF; local coordinates, then placed by model3d) --------------------------------
def housing():
    """Bearing housing hanging under the top T-profile (4× M5 into T-nuts, slots y = ±20): bore ⌀21.2 × 32 for
    igus RJ4JP-01-12 (inserted from above, held by the profile), ⌀14 below, clamp slit + M4."""
    w, d, h = p.C_HOUSING
    s = cq.Workplane("XY").rect(w, d).extrude(h).edges("|Z").fillet(4)
    s = s.cut(cq.Workplane("XY").circle(7).extrude(h))
    s = s.cut(cq.Workplane("XY").workplane(offset=4).circle(21.2 / 2).extrude(h))
    s = s.cut(cq.Workplane("XY").center(0, d / 4 + 2).rect(1.6, d / 2).extrude(h).translate((0, 0, 4)))
    s = s.cut(cq.Workplane("YZ").workplane(offset=-w / 2).center(d / 2 - 6, h / 2 + 2).circle(2.2).extrude(w))
    for sx in (-1, 1):
        for sy in (-1, 1):
            s = s.cut(cq.Workplane("XY").center(sx * 19, sy * 20).circle(2.75).extrude(h))
            s = s.cut(cq.Workplane("XY").center(sx * 19, sy * 20).circle(5).extrude(5))    # screw heads from below
    return s


def _clamp_ring(d_in, d_out, t, x, y):
    return (cq.Workplane("XY").center(x, y).circle(d_out / 2).extrude(t),
            cq.Workplane("XY").center(x, y).circle(d_in / 2).extrude(t))


def _arm(p0, p1, w, t):
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    a = math.degrees(math.atan2(y1 - y0, x1 - x0))
    return (cq.Workplane("XY").center(L / 2, 0).rect(L, w).extrude(t)
            .rotate((0, 0, 0), (0, 0, 1), a).translate((x0, y0, 0)))


def _slit(x, y, toward, length, t, d_screw=3.4):
    """Clamp slit from a ring centre (x, y) in direction `toward` (deg) + cross hole for an M3/M4 screw."""
    a = math.radians(toward)
    sl = (cq.Workplane("XY").center(length / 2, 0).rect(length, 1.6).extrude(t)
          .rotate((0, 0, 0), (0, 0, 1), toward).translate((x, y, 0)))
    hole = (cq.Workplane("XZ").circle(d_screw / 2).extrude(30, both=True)
            .rotate((0, 0, 0), (0, 0, 1), toward).translate((x + math.cos(a) * (length - 4), y + math.sin(a) * (length - 4), t / 2)))
    return sl.union(hole)


def lvdt_arm():
    """Arm from the Invar post ⌀16 to the LVDT body ⌀20.6 (both clamped), 12 mm thick; z 0 … 12."""
    (xi, yi), (xl, yl) = p.C_INVAR_XY, p.C_LVDT_XY
    o1, i1 = _clamp_ring(16.3, 30, ARM_T, xi, yi)
    o2, i2 = _clamp_ring(LV_D + 0.3, LV_D + 14, ARM_T, xl, yl)
    s = o1.union(o2).union(_arm((xi, yi), (xl, yl), 14, ARM_T)).cut(i1).cut(i2)
    s = s.cut(_slit(xi, yi, 135, 15, ARM_T)).cut(_slit(xl, yl, -45, 17, ARM_T))
    return s


def target_arm():
    """Arm from the Invar post to the camera reference target (white 12×12 face) at rim height; z 0 … 8."""
    (xi, yi), (xr, yr) = p.C_INVAR_XY, p.C_REF_XY
    o1, i1 = _clamp_ring(16.3, 30, 8, xi, yi)
    pad = cq.Workplane("XY").center(xr, yr).rect(14, 14).extrude(8)
    s = o1.union(pad).union(_arm((xi, yi), (xr, yr), 10, 8)).cut(i1).cut(_slit(xi, yi, 135, 15, 8))
    return s


def post_foot():
    """Foot of the Invar post on the base rail (x = C_RAIL_X): 2× M5 into T-nuts in the rail top slot (along y);
    the post stands on a 3 mm printed floor (bridges the slot) and is clamped by an M3 screw; z 0 … 20."""
    xi, yi = p.C_INVAR_XY
    s = cq.Workplane("XY").center(xi, yi).rect(32, 44).extrude(20).edges("|Z").fillet(3)
    s = s.cut(cq.Workplane("XY").workplane(offset=POST_FLOOR).center(xi, yi).circle(8.15).extrude(20))
    for dy in (-15, 15):
        s = s.cut(cq.Workplane("XY").center(xi, yi + dy).circle(2.75).extrude(20))
        s = s.cut(cq.Workplane("XY").workplane(offset=14).center(xi, yi + dy).circle(5).extrude(6))
    s = s.cut(cq.Workplane("XY").workplane(offset=POST_FLOOR).center(xi - 10, yi).rect(14, 1.6).extrude(20))
    s = s.cut(cq.Workplane("XZ").workplane(offset=-(yi + 30)).center(xi - 10, 12).circle(1.7).extrude(60))
    return s


def laser_holder():
    """Holder on the +y face of the top T-profile (2× M5 into T-nuts, face slot z = 20); holds the ⌀10 laser
    beside the beam at C_LASER_ANG, aimed at the sand centre (200 mm, so the 31° DOE fan covers ⌀100).
    Local z = 0 is the underside of the top beam; the block stays outside the carrier radius (r > 70)."""
    zl = Z_S1 + p.C_LASER_H - ZBEAM                  # laser centre relative to the beam underside (+43)
    yl, y0 = p.C_LASER_Y, p.C_TOP[1] / 2
    plate = cq.Workplane("XY").box(30, 6, 40, centered=(True, False, False)).translate((0, y0, 5))
    web = cq.Workplane("XY").box(16, yl - 8 - (y0 + 6) + 1, 9, centered=(True, False, False)).translate((0, y0 + 5, 36))
    blk = cq.Workplane("XY").box(16, 16, 18, centered=(True, True, True)).translate((0, yl, zl))
    s = plate.union(web).union(blk)
    bore = (cq.Workplane("XZ").circle(5.1).extrude(40, both=True)
            .rotate((0, 0, 0), (1, 0, 0), p.C_LASER_ANG).translate((0, yl, zl)))
    s = s.cut(bore)
    for dx in (-10, 10):
        s = s.cut(cq.Workplane("XZ").center(dx, 20).circle(2.75).extrude(-10).translate((0, y0 - 1, 0)))
    s = s.cut(cq.Workplane("YZ").workplane(offset=-10).center(yl, zl - 6).circle(1.4).extrude(20))   # M3 set screw
    return s


def camera_box():
    """Box for RPi HQ camera + 6 mm lens + RPi 5 (90 × 100 × 70, walls 3), lens window ⌀34 with a recess for
    a 50 × 50 × 2 glass; local frame: lens axis = −z, box centred at the origin (placed tilted by model3d)."""
    W, L, H = 90.0, 100.0, 70.0
    s = cq.Workplane("XY").box(W, L, H).edges("|Z").fillet(5)
    s = s.cut(cq.Workplane("XY").box(W - 6, L - 6, H - 6))
    s = s.cut(cq.Workplane("XY").workplane(offset=-H / 2 - 1).circle(17).extrude(5))
    s = s.cut(cq.Workplane("XY").workplane(offset=-H / 2 - 1).rect(51, 51).extrude(2.5))
    for sx in (-1, 1):
        for sy in (-1, 1):
            s = s.cut(cq.Workplane("XY").workplane(offset=-H / 2).center(sx * 15, sy * 15).circle(1.3).extrude(5))
    s = s.cut(cq.Workplane("XY").workplane(offset=H / 2 - 4).rect(W - 6, L - 6).extrude(5))   # open top (lid)
    s = s.cut(cq.Workplane("YZ").workplane(offset=W / 2 - 4).center(0, 10).circle(6.2).extrude(5))  # cable gland PG7
    tab = cq.Workplane("XY").workplane(offset=H / 2 - 4).center(0, L / 2 + 8).rect(40, 16).extrude(4)
    for dx in (-12, 12):
        tab = tab.cut(cq.Workplane("XY").workplane(offset=H / 2 - 4).center(dx, L / 2 + 8).circle(2.2).extrude(4))
    return s.union(tab)


def camera_box_lid():
    W, L = 90.0, 100.0
    s = cq.Workplane("XY").rect(W, L).extrude(3).edges("|Z").fillet(5)
    s = s.union(cq.Workplane("XY").workplane(offset=-4).rect(W - 6.4, L - 6.4).extrude(4)
                .cut(cq.Workplane("XY").workplane(offset=-4).rect(W - 10, L - 10).extrude(4)))
    for x, y in ((-29, -24.5), (29, -24.5), (-29, 24.5), (29, 24.5)):          # RPi 5 holes 58 × 49
        s = s.union(cq.Workplane("XY").workplane(offset=-8).center(x, y).circle(3).extrude(8)
                    .cut(cq.Workplane("XY").workplane(offset=-8).center(x, y).circle(1.2).extrude(8)))
    return s


def _cam_place(shape):
    """Place a shape given in the camera-box frame like model3d places the box (tilt about x, then move)."""
    return shape.rotate((0, 0, 0), (1, 0, 0), p.C_CAM_TILT).translate((0, p.C_CAM_Y, Z_S1 + p.C_CAM_H - ZBEAM))


def camera_hanger():
    """Camera mount: flange on the −y face of the top T-profile (2× M5 into T-nuts), arm, pad on the camera box
    tab (2× M4). Local z = 0 is the underside of the top beam."""
    y0 = -p.C_TOP[1] / 2
    flange = cq.Workplane("XY").box(30, 6, 30, centered=(True, False, False)).translate((0, y0 - 6, 5))
    for dx in (-10, 10):
        flange = flange.cut(cq.Workplane("XZ").center(dx, 20).circle(2.75).extrude(10).translate((0, y0 + 1, 0)))
    L, H = 100.0, 70.0
    pad = cq.Workplane("XY").box(40, 16, 14, centered=(True, True, False)).translate((0, L / 2 + 8, H / 2))
    for dx in (-12, 12):
        pad = pad.cut(cq.Workplane("XY").center(dx, L / 2 + 8).circle(2.2).extrude(14).translate((0, 0, H / 2)))
        pad = pad.cut(cq.Workplane("XY").center(dx, L / 2 + 8).circle(4.2).extrude(8).translate((0, 0, H / 2 + 6)))
    top = _cam_place(cq.Workplane("XY").box(4, 4, 1).translate((0, L / 2 + 8, H / 2 + 19)))
    pad = _cam_place(pad)
    c = top.val().Center()
    a = cq.Vector(0, y0 - 6, 18)
    v = cq.Vector(c.x, c.y, c.z) - a
    arm = cq.Workplane("XY").add(cq.Solid.makeBox(14, v.Length, 10, cq.Vector(-7, 0, -5)))
    ang = math.degrees(math.atan2(v.z, v.y))
    arm = arm.rotate((0, 0, 0), (1, 0, 0), ang).translate((a.x, a.y, a.z))
    keep_out = (cq.Workplane("XY").box(90.4, 100.4, 70.4).union(
        cq.Workplane("XY").box(40.4, 16.4, 4.2, centered=(True, True, False)).translate((0, L / 2 + 8, H / 2 - 4.2))))
    return flange.union(arm).union(pad).cut(_cam_place(keep_out))   # arm trimmed to clear box and lid


# --- pomůcky pro přípravu a výměnu vzorku (tisk) ---------------------------------------------------------
SCREED_DEPTH = p.COLLAR_TOP - p.SAND_TOP          # 34 – povrch písku pod horní hranou límce
PARK_LIFT = 30.0                                  # o kolik se tyč zvedne při výměně cely
PARK_H = (Z_COLLAR - Z_TOP) + PARK_LIFT           # výška vidlice na horní ploše T04


def centering_cap():
    """P09 – středicí víčko: nasadí se na límec plné cely (⌀106), tyč ⌀12 projde středem → cela je souosá
    s vedením; podkova (drážka 12,6) – po vystředění se vysune do strany. z 0 … 10."""
    s = cq.Workplane("XY").circle(66).extrude(10)
    s = s.cut(cq.Workplane("XY").circle(p.COLLAR_OD / 2 + 0.3).extrude(6))          # nasazení na límec
    s = s.cut(cq.Workplane("XY").circle(p.C_ROD_D / 2 + 0.2).extrude(10))           # tyč
    s = s.cut(cq.Workplane("XY").center(0, -35).rect(p.C_ROD_D + 0.6, 70).extrude(10))   # podkova
    return s


def screed():
    """P10 – stěrka povrchu: příčka 124 × 16 × 6 leží na límci, břit 99 × 3 sahá 34 mm pod jeho hranu;
    otáčením se srovná povrch písku přesně do výšky SAND_TOP. Lokální z = 0 je horní hrana límce."""
    bar = cq.Workplane("XY").box(124, 16, 6, centered=(True, True, False))
    blade = cq.Workplane("XY").box(p.CAV_D - 1.0, 3, SCREED_DEPTH, centered=(True, True, False)).translate((0, 0, -SCREED_DEPTH))
    grip = cq.Workplane("XY").box(16, 16, 30, centered=(True, True, False)).translate((0, 0, 6))
    return bar.union(blade).union(grip)


def parking_fork():
    """P11 – parkovací vidlice: postaví se na T04 kolem tyče pod stavěcí kroužek → tyč zůstane zvednutá
    o 30 mm nad límcem cely, cela se dá vyjmout. 40 × 60 × PARK_H, drážka 12,6."""
    s = cq.Workplane("XY").box(40, 60, PARK_H, centered=(True, True, False))
    s = s.cut(cq.Workplane("XY").center(0, -15).rect(p.C_ROD_D + 0.6, 30).extrude(PARK_H))
    s = s.cut(cq.Workplane("XY").circle(p.C_ROD_D / 2 + 0.3).extrude(PARK_H))
    return s


PRINT = [("E7-P01_bearing_housing", housing, 1), ("E7-P02_lvdt_arm", lvdt_arm, 1),
         ("E7-P03_target_arm", target_arm, 1), ("E7-P04_post_foot", post_foot, 1),
         ("E7-P05_laser_holder", laser_holder, 1), ("E7-P06_camera_box", camera_box, 1),
         ("E7-P07_camera_box_lid", camera_box_lid, 1), ("E7-P08_camera_hanger", camera_hanger, 1),
         ("E7-P09_centering_cap", centering_cap, 1), ("E7-P10_screed", screed, 1), ("E7-P11_parking_fork", parking_fork, 1)]


def export_all():
    for sub in ("laser", "tisk"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    out = []
    for part in LASER:
        out.append(write_dxf(part, os.path.join(OUT, "laser")))
        cq.exporters.export(laser_solid(part), os.path.join(OUT, "laser", f"{part['name']}_{part['t']:g}mm.step"))
    for name, fn, _ in PRINT:
        s = fn()
        cq.exporters.export(s, os.path.join(OUT, "tisk", name + ".stl"), tolerance=0.05, angularTolerance=0.1)
        cq.exporters.export(s, os.path.join(OUT, "tisk", name + ".step"))
        out.append(name)
    return out


if __name__ == "__main__":
    print(f"levels: base frame top {ZB0:.1f}, top beam underside {ZBEAM:.1f}, carrier {ZC:.1f}; column {COL_H:.0f}, "
          f"Invar post {POST_L:.0f}, Invar rod {ROD_L:.0f}")
    for d in LASER:
        if d["mat"].startswith("steel"):
            print(d["name"], f"{disc_mass(d):.3f} kg")
    for f in export_all():
        print("ok", os.path.basename(f))
