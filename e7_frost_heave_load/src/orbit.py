"""E7 – oběh kamery kolem vzorku, JEDNA sestava pro fázi 1 (bez zatížení) i fázi 2 (se zátěží).

Pod středem horního příčníku T04 je pevné tištěné jádro P12 (4× M5 do spodních drážek) s otvorem ve středu:
v něm je kluzné pouzdro igus RJ4JP-01-12 pro vodicí tyč zátěže (nahrazuje dřívější pouzdro P01), takže ve fázi 2
tyč prochází středem oběhu a hlava kamery obíhá kolem ní. Na jádře jsou vnitřní kroužky dvou ložisek 6806-2RS
(30 × 42 × 7); na jejich vnějších kroužcích je otočný náboj P13 – dole příruba s ramenem a hlavou kamery P14,
nahoře ozubený věnec m1 z72. Pastorek z12 na krokovém motoru 28BYJ-48 (držák P16, pod příčníkem, strana −x)
→ převod 6 : 1. Výchozí polohu hlásí Hall senzor zalitý ve spodní ploše desky P12 nad magnetem ve věnci.

Vějíř laseru (+y) prochází pod příčníkem nejblíže 41 mm od osy ve výšce věnce → věnec má hlavu zubů na r 37.
Rameno vede pod motorem (z 271–279) a teprve za ním stoupá k hlavě; nad zorným polem kamery.
RPi 5 je v boxu P06 na vnější straně pravého sloupu (+x, držák P18), plochý kabel 500 mm ve smyčce → rozsah ±180°.

Díly se vracejí ve SVĚTOVÝCH souřadnicích sestavy (model3d.py) ve výchozí poloze (úhel 0 = hlava na −y).
Tisk (PETG-CF): P12 jádro, P12b distanční kroužek, P12c svěrný kroužek, P13 náboj s věncem, P14 rameno s hlavou,
P15 víčko hlavy, P16 držák motoru, P18 držák boxu RPi, P19 pastorek.
"""
import math

import cadquery as cq

import buildparts as bp
import params as p

ZB = bp.ZBEAM                       # underside of the top beam (320)
ZT = ZB + p.C_TOP[2]                # top of the beam (360)
d_b, D_b, B_b = p.C_ORB_BRG         # 6806-2RS
M_G, Z_RING, Z_PIN = p.C_ORB_GEAR
A_DIST = M_G * (Z_RING + Z_PIN) / 2         # 42 – centre distance ring ↔ pinion
IGUS = p.C_BUSH                     # (21, 30) – igus RJ4JP-01-12 outer ⌀ × length
# vertical stack under the beam (z)
Z_PLATE = ZB - 6                    # 314 – underside of the P12 plate
Z_SH = Z_PLATE - 1                  # 313 – shoulder ⌀34 (inner rings only) → outer ring 1 mm clear of the plate
Z_B1 = Z_SH - B_b                   # 306 – upper bearing 306 … 313
Z_B0 = Z_B1 - 6 - B_b               # 293 – lower bearing 293 … 300, spacer 300 … 306
Z_GEAR = (Z_B1 + 1, Z_SH)           # 307 … 313 – ring teeth
Z_CLAMP = Z_B0 - 3                  # 290 – clamp ring ⌀34 × 3 under the lower inner ring (3× M3 into the core)
Z_IGUS = ZB - IGUS[1]               # 290 – igus bushing 290 … 320
Z_MPL = (Z_B1 - 4, Z_B1)            # 302 … 306 – motor plate under the pinion
Z_ARM = (ZB - 49.0, ZB - 41.0)              # horizontal run of the arm (under the motor, above the camera's view)
HOME_MAG = (0.0, -31.0)             # magnet in the ring / Hall sensor in the plate at the home position
th = math.radians(p.C_ORB_TILT)
WIN = (0.0, -p.C_ORB_R, bp.Z_S1 + p.C_ORB_H)   # head window centre at the home position


def cyl(d, h, z0, x=0.0, y=0.0):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(d / 2).extrude(h)


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def gear(m, z, width, z0, x=0.0, y=0.0, bore=0.0, phase=0.0):
    """Spur gear with involute teeth (pressure angle 20°), axis z, from z0 up by width; phase rotates the teeth (deg)."""
    alpha = math.radians(20)
    rp = m * z / 2
    rb = rp * math.cos(alpha)
    ra = rp + m
    rf = max(rp - 1.25 * m, 0.5)

    def inv(r):
        a = math.acos(min(1.0, rb / r))
        return math.tan(a) - a
    half = math.pi / (2 * z) + inv(rp)
    r0 = max(rb, rf)
    pts = []
    for k in range(z):
        c = 2 * math.pi * k / z + math.radians(phase)
        flank = [(r0 + (ra - r0) * i / 6, 0.0) for i in range(7)]
        flank = [(r, half - inv(r)) for r, _ in flank]
        a0 = half - inv(r0)
        dd = min(0.02, 0.4 * (math.pi / z - a0))
        if rf < r0 - 1e-6:
            pts.append((rf * math.cos(c - a0 - dd), rf * math.sin(c - a0 - dd)))
        pts += [(r * math.cos(c - a), r * math.sin(c - a)) for r, a in flank]
        pts += [(r * math.cos(c + a), r * math.sin(c + a)) for r, a in reversed(flank)]
        if rf < r0 - 1e-6:
            pts.append((rf * math.cos(c + a0 + dd), rf * math.sin(c + a0 + dd)))
    s = cq.Workplane("XY").workplane(offset=z0).polyline(pts).close().extrude(width)
    if bore:
        s = s.cut(cq.Workplane("XY").workplane(offset=z0).circle(bore / 2).extrude(width))
    return s.translate((x, y, 0))


# ------------------------------------------------------------------------------------------------ fixed parts
def core():
    """P12 – pevné jádro pod příčníkem: deska 64 × 72 × 6 (4× M5 do spodních drážek y ±20), osazení ⌀34 × 1,
    čep ⌀30 pro 2× 6806-2RS, středem lůžko ⌀21 pro igus RJ4JP-01-12 (vodicí tyč zátěže ve fázi 2);
    3× M3 dole pro svěrný kroužek; kapsa pro Hall A3144 ve spodní ploše desky nad magnetem věnce (výchozí poloha)."""
    s = box(-32, 32, -36, 36, Z_PLATE, ZB)
    s = s.union(cyl(34, 1, Z_SH)).union(cyl(d_b, Z_SH - Z_B0, Z_B0))
    s = s.cut(cyl(IGUS[0] + 0.2, ZB - Z_B0 + 1, Z_B0 - 0.5))
    for x in (-24, 24):
        for y in (-20, 20):
            s = s.cut(cyl(5.5, 7, Z_PLATE - 0.5, x, y))
    for k in range(3):
        a = math.radians(90 + 120 * k)
        s = s.cut(cyl(2.5, 8, Z_B0 - 0.5, 12.75 * math.cos(a), 12.75 * math.sin(a)))
    s = s.cut(box(HOME_MAG[0] - 2.6, HOME_MAG[0] + 2.6, HOME_MAG[1] - 2.0, HOME_MAG[1] + 2.0, Z_PLATE - 0.1, Z_PLATE + 3.5))
    return s.cut(box(-1.5, 1.5, -36.5, HOME_MAG[1], Z_PLATE + 1.5, Z_PLATE + 3.5))     # wire channel to the edge


def spacer():
    """P12b – distanční kroužek mezi vnitřními kroužky ložisek: ⌀30,2 / ⌀34 × 6."""
    return cyl(34, 6, Z_B0 + B_b).cut(cyl(d_b + 0.2, 6, Z_B0 + B_b))


def clamp_ring():
    """P12c – svěrný kroužek ⌀34 / ⌀21,6 × 3 pod spodním vnitřním kroužkem, 3× M3 × 10 do jádra."""
    s = cyl(34, 3, Z_CLAMP).cut(cyl(IGUS[0] + 0.6, 3, Z_CLAMP))
    for k in range(3):
        a = math.radians(90 + 120 * k)
        s = s.cut(cyl(3.4, 3, Z_CLAMP, 12.75 * math.cos(a), 12.75 * math.sin(a)))
    return s


def igus():
    """igus drylin RJ4JP-01-12 (⌀21 × 30) v jádře – ve fázi 2 jím prochází vodicí tyč ⌀12 zátěže."""
    return cyl(IGUS[0], IGUS[1], Z_IGUS).cut(cyl(p.C_ROD_D + 0.1, IGUS[1], Z_IGUS))


def bearings():
    return [cyl(D_b, B_b, z0).cut(cyl(d_b, B_b, z0)) for z0 in (Z_B0, Z_B1)]


def motor_bracket():
    """P16 – držák motoru 28BYJ-48 pod příčníkem (strana −x): příruba 2× M5 do spodních drážek (y ±20), stěna,
    deska pod věncem s otvory pro uši M4 (rozteč 35) a pro hřídel; motor visí pod deskou, hřídel nahoru."""
    xm = -A_DIST - 8
    plate = box(-72, -30, -24, 24, Z_MPL[0], Z_MPL[1]).cut(cyl(54, 20, Z_MPL[0] - 10))     # clear of the hub ⌀50
    plate = plate.cut(cyl(10, 10, Z_MPL[0] - 1, -A_DIST, 0))
    for y in (-17.5, 17.5):
        plate = plate.cut(cyl(4.4, 10, Z_MPL[0] - 1, xm, y))
    wall = box(-72, -64, -24, 24, Z_MPL[1], Z_PLATE)
    flange = box(-80, -56, -30, 30, Z_PLATE, ZB)
    for y in (-20, 20):
        flange = flange.cut(cyl(5.5, 8, Z_PLATE - 1, -68, y))
    return plate.union(wall).union(flange)


def motor():
    """28BYJ-48 (model): tělo ⌀28 × 19 pod deskou, hřídel 8 mm mimo osu těla směrem k ose vzorku,
    uši ±17,5, kryt vodičů na vnější straně (přesah ≈ 3 mm)."""
    xm = -A_DIST - 8
    s = cyl(28, 19, Z_MPL[0] - 19, xm, 0).union(box(xm - 3.5, xm + 3.5, -21, 21, Z_MPL[0] - 1, Z_MPL[0]))
    s = s.union(box(xm - 17, xm - 10, -8.5, 8.5, Z_MPL[0] - 17, Z_MPL[0] - 2))
    shaft = cyl(5, Z_GEAR[1] - Z_MPL[0], Z_MPL[0], -A_DIST, 0).intersect(
        box(-A_DIST - 1.5, -A_DIST + 1.5, -3, 3, Z_MPL[0], Z_GEAR[1] + 1).union(cyl(5, 1.5, Z_MPL[0], -A_DIST, 0)))
    return s.union(shaft).union(cyl(9, Z_MPL[1] - Z_MPL[0] - 0.5, Z_MPL[0], -A_DIST, 0))


def pinion():
    """P19 – pastorek m1 z12 na hřídel 28BYJ-48 (⌀5 se dvěma ploškami 3 mm), natočený do záběru."""
    g = gear(M_G, Z_PIN, Z_GEAR[1] - Z_GEAR[0], Z_GEAR[0], -A_DIST, 0, phase=180.0 / Z_PIN)
    return g.cut(cyl(5.2, 10, Z_GEAR[0] - 1, -A_DIST, 0).intersect(
        box(-A_DIST - 1.7, -A_DIST + 1.7, -3, 3, Z_GEAR[0] - 1, Z_GEAR[1] + 1)))


RPI_Z = ZB - 105.0                  # shelf under the RPi box on the outer face of the +x column


def rpi_bracket():
    """P18 – držák boxu P06 s RPi 5 na vnější straně pravého sloupu T01 (+x): svislá deska 2× M5 do drážek sloupu
    (y ±20), police pod boxem, dvě bočnice. 19. 11. 2026: box mimo rám, aby sestava byla nižší (mrazák 41 cm)."""
    x0 = p.C_COL_SPAN / 2 + 20                                                              # outer face of the column (170)
    s = box(x0, x0 + 4, -36, 36, RPI_Z, RPI_Z + 70).union(box(x0, x0 + 76, -48, 48, RPI_Z - 4, RPI_Z))
    s = s.union(box(x0, x0 + 76, -48, -45, RPI_Z, RPI_Z + 25)).union(box(x0, x0 + 76, 45, 48, RPI_Z, RPI_Z + 25))
    for y in (-20, 20):
        s = s.cut(cq.Workplane("YZ").workplane(offset=x0 - 1).center(y, RPI_Z + 50).circle(2.75).extrude(6))
    return s


def rpi_box():
    """Box P06 (RPi 5) stojící na polici P18 vedle sloupu, víko P07 ven (+x) (model)."""
    s = bp.camera_box().rotate((0, 0, 0), (1, 0, 0), 90).rotate((0, 0, 0), (0, 0, 1), 90)
    return s.translate((p.C_COL_SPAN / 2 + 20 + 4 + 35 + 1, 0, RPI_Z + 50))


# ------------------------------------------------------------------------------------------------ rotating parts
def hub():
    """P13 – otočný náboj: ⌀50 se dvěma lůžky ⌀42 × 7 pro 6806-2RS (mezi nimi osazení ⌀38), nahoře věnec m1 z72,
    dole příruba ⌀60 × 4 (spodní ložisko se zasouvá zespodu, drží ho patka ramene); kapsa ⌀6 × 2 pro magnet."""
    s = cyl(50, Z_GEAR[0] - Z_B0, Z_B0).union(gear(M_G, Z_RING, Z_GEAR[1] - Z_GEAR[0], Z_GEAR[0]))
    s = s.union(cyl(60, 4, Z_B0 - 4))
    s = s.cut(cyl(D_b, B_b + 4, Z_B0 - 4)).cut(cyl(D_b, B_b, Z_B1)).cut(cyl(38, 6, Z_B0 + B_b))
    for x in (-5.0, 5.0):
        s = s.cut(cyl(2.5, 8, Z_B0 - 4, x, -25.0))                                           # 2× M3 for the arm foot
    return s.cut(cyl(6.2, 2.2, Z_GEAR[1] - 2.2, *HOME_MAG))                               # magnet ⌀6 × 2


def _head_local():
    """Head box in its own frame: window centre at the origin, optical axis −z, box 34 × 34 × 24 behind it."""
    s = cq.Workplane("XY").box(34, 34, 24, centered=(True, True, False)).edges("|Z").fillet(3)
    s = s.cut(cq.Workplane("XY").workplane(offset=2).rect(28, 28).extrude(23))
    s = s.cut(cyl(12, 3, -0.5))
    for x in (-10.5, 10.5):
        for y in (-6.25, 6.25):
            s = s.cut(cyl(2.2, 4, -0.5, x, y))
    return s


def _place_head(s):
    return s.rotate((0, 0, 0), (1, 0, 0), p.C_ORB_TILT).translate(WIN)


def _local_to_world(v):
    x, y, z = v
    return (x + WIN[0], y * math.cos(th) - z * math.sin(th) + WIN[1], y * math.sin(th) + z * math.cos(th) + WIN[2])


def _bar(y0, z0, y1, z1, w, t):
    L = math.hypot(y1 - y0, z1 - z0)
    a = math.degrees(math.atan2(z1 - z0, y1 - y0))
    b = cq.Workplane("XY").box(w, L, t).translate((0, L / 2, 0))
    return b.rotate((0, 0, 0), (1, 0, 0), a).translate((0, y0, z0))


def arm_head():
    """P14 – rameno s hlavou kamery (jeden díl): patka ⌀60 / ⌀36 × 4 pod přírubou náboje (2× M3, drží spodní
    ložisko), svislý pás, vodorovné rameno pod motorem a nad zorným polem, krátký sloupek k hlavě (mimo motor);
    hlava 34 × 34 × 24 s okénkem ⌀12 pro Camera Module 3 (sklon 36,5°)."""
    foot = cyl(60, 4, Z_B0 - 8).cut(cyl(36, 4, Z_B0 - 8))
    for x in (-5.0, 5.0):
        foot = foot.cut(cyl(3.4, 5, Z_B0 - 8.5, x, -25.0))
    drop = box(-5, 5, -30, -20, Z_ARM[0], Z_B0 - 8)
    run = box(-5, 5, -71, -22, Z_ARM[0], Z_ARM[1])        # under the motor (r ≤ 67), above the view to the far edge
    pr = _local_to_world((0, 18.0, 3.0))                 # point just outside the axis-side face of the head, near its front
    riser = box(-5, 5, pr[1] - 4.0, pr[1] + 3.0, Z_ARM[0] + 4, pr[2] + 2.0)   # short post up to the head (beyond the motor)
    return foot.union(drop).union(run).union(riser).union(_place_head(_head_local()))


def head_lid():
    """P15 – víčko hlavy 34 × 34 × 2 s výřezem 17 × 3 pro plochý kabel a 2 vodiče (LED, topný odpor)."""
    s = cq.Workplane("XY").box(34, 34, 2, centered=(True, True, False)).edges("|Z").fillet(3).translate((0, 0, 24))
    s = s.union(cq.Workplane("XY").workplane(offset=22).rect(27.6, 27.6).extrude(2).cut(
        cq.Workplane("XY").workplane(offset=22).rect(24, 24).extrude(2)))
    s = s.cut(cq.Workplane("XY").workplane(offset=21).center(0, 12).rect(17, 3).extrude(6))
    return _place_head(s)


def cm3():
    """Raspberry Pi Camera Module 3 (model): deska 25 × 24 × 1, čočka ⌀8 v okénku."""
    s = cq.Workplane("XY").box(25, 24, 1, centered=(True, True, False)).translate((0, 0, 7)).union(cyl(8, 6, 1))
    s = s.union(cq.Workplane("XY").box(8.5, 8.5, 4, centered=(True, True, False)).translate((0, 0, 3)))
    return _place_head(s)


def led():
    """Bílá LED 1 W na hvězdě ⌀20 vedle okénka na straně dál od osy, svítí podél osy kamery."""
    return _place_head(cyl(20, 3, 1.0, 0, -28.0).union(box(-6, 6, -20, -17, 1.0, 10.0)))


FIXED = [("P12 orbit core with igus seat (print)", core), ("P12b bearing spacer (print)", spacer),
         ("P12c clamp ring (print)", clamp_ring), ("igus drylin RJ4JP-01-12", igus),
         ("P16 motor bracket (print)", motor_bracket), ("stepper 28BYJ-48 5 V", motor),
         ("P19 pinion m1 z12 (print)", pinion), ("P18 RPi box bracket (print)", rpi_bracket),
         ("P06 box with RPi 5 (on the column)", rpi_box)]
ROTATING = [("P13 orbit hub m1 z72 (print)", hub), ("P14 camera arm + head (print)", arm_head),
            ("P15 head lid (print)", head_lid), ("Raspberry Pi Camera Module 3", cm3),
            ("LED white 1 W on star D20 (photo light)", led)]
PRINT_ORBIT = [("E7-P12_orbit_core", core, 1), ("E7-P12b_bearing_spacer", spacer, 1), ("E7-P12c_clamp_ring", clamp_ring, 1),
               ("E7-P13_orbit_hub", hub, 1), ("E7-P14_camera_arm_head", arm_head, 1), ("E7-P15_head_lid", head_lid, 1),
               ("E7-P16_motor_bracket", motor_bracket, 1), ("E7-P18_rpi_bracket", rpi_bracket, 1),
               ("E7-P19_pinion_z12", pinion, 1)]


def rotating(angle=0.0):
    """Rotating parts turned by `angle` degrees about the sample axis (0 = home on −y)."""
    return [(n, f().rotate((0, 0, 0), (0, 0, 1), angle)) for n, f in ROTATING]


def add_to(asm, prefix="", colors=None, angle=0.0):
    C = colors or {}
    for n, f in FIXED:
        c = C.get("petg") if "print" in n else (C.get("ins") if "RPi" in n else (C.get("ptfe") if "igus" in n else C.get("steel")))
        asm.add(f(), name=prefix + n, color=c)
    for k, b in enumerate(bearings()):
        asm.add(b, name=f"{prefix}bearing 6806-2RS {k + 1}", color=C.get("steel"))
    for n, s in rotating(angle):
        c = C.get("petg") if "print" in n else (C.get("temp") if "LED" in n else C.get("sensor"))
        asm.add(s, name=prefix + n, color=c)
