"""E7 – oběh kamery kolem vzorku (fáze 1, varianta U bez zatížení).

Malá hlava s Raspberry Pi Camera Module 3 obíhá kolem svislé osy vzorku. Pohon a ložiska jsou NAD horním
příčníkem T04 (tam je ve fázi 1 volno): svislý hřídel ⌀12 h6 prochází stávajícím otvorem ⌀14 v příčníku,
nahoře se točí ve dvou ložiskách 6001-2RS v tištěném bloku P12, visí na stavěcím kroužku DIN 705 ⌀12 a nese
ozubené kolo m1 z72, které pohání krokový motor 28BYJ-48 přes pastorek z12 (převod 6 : 1). Pod příčníkem je
jen tištěné rameno s nábojem P14 (sevřené na hřídeli 2 červíky M4) a hlava kamery – nic dalšího, takže vějíř
laseru i pohled kamery zůstávají volné a hlava může obíhat bez kolize.

RPi 5 je v pevném boxu P06 na horní straně příčníku (vanička P18); plochý kabel kamery 500 mm jde ve smyčce
kolem náboje, proto se hlava otáčí ±180° od výchozí polohy (výchozí poloha = strana −y, odtud se snímá laser).

Díly se vracejí ve SVĚTOVÝCH souřadnicích sestavy (model3d.py) ve výchozí poloze (úhel 0).
Tisk (PETG-CF): P12 ložiskový blok, P14 rameno s nábojem a hlavou, P15 víčko hlavy, P16 držák motoru,
P17 ozubené kolo z72, P19 pastorek z12, P18 vanička boxu RPi.
"""
import math

import cadquery as cq

import buildparts as bp
import params as p

ZB = bp.ZBEAM                       # underside of the top beam (320)
ZT = ZB + p.C_TOP[2]                # top of the beam (360)
M_G, Z_RING, Z_PIN = p.C_ORB_GEAR
A_DIST = M_G * (Z_RING + Z_PIN) / 2         # 42 – centre distance gear ↔ pinion
BRG = (12.0, 28.0, 8.0)             # 6001-2RS
# stack on the top beam (z)
Z_BASE = ZT + 5                     # 365 – top of the P12 base plate
Z_BR0 = Z_BASE                      # 365 … 373 lower bearing
Z_BR1 = Z_BASE + 19                 # 384 … 392 upper bearing
Z_BLK = Z_BR1 + BRG[2]              # 392 – top of the block
Z_COL = (Z_BLK, Z_BLK + 12)         # 392 … 404 shaft collar DIN 705-A 12 (the shaft hangs on it)
Z_GEAR = (Z_COL[1] + 0.5, Z_COL[1] + 6.5)   # 404.5 … 410.5 gear teeth
Z_MPL = (Z_GEAR[0] - 5, Z_GEAR[0] - 1)      # motor plate under the pinion
# under the beam
Z_HUB = (ZB - 24, ZB - 4)           # 296 … 316 hub sleeve of the arm
SHAFT = (Z_HUB[0], Z_GEAR[1] + 6)   # shaft ⌀12 296 … 416.5 → 120 mm
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
        a0 = half - inv(r0)                                   # half tooth angle where the flank starts
        d = min(0.02, 0.4 * (math.pi / z - a0))               # root land, never past the middle of the gap
        if rf < r0 - 1e-6:
            pts.append((rf * math.cos(c - a0 - d), rf * math.sin(c - a0 - d)))
        pts += [(r * math.cos(c - a), r * math.sin(c - a)) for r, a in flank]
        pts += [(r * math.cos(c + a), r * math.sin(c + a)) for r, a in reversed(flank)]
        if rf < r0 - 1e-6:
            pts.append((rf * math.cos(c + a0 + d), rf * math.sin(c + a0 + d)))
    s = cq.Workplane("XY").workplane(offset=z0).polyline(pts).close().extrude(width)
    if bore:
        s = s.cut(cq.Workplane("XY").workplane(offset=z0).circle(bore / 2).extrude(width))
    return s.translate((x, y, 0))


def _rotz(s, deg):
    return s.rotate((0, 0, 0), (0, 0, 1), deg)


# ------------------------------------------------------------------------------------------------ fixed parts
def bearing_block():
    """P12 – ložiskový blok na horní straně příčníku: deska 56 × 80 × 5 (4× M5 do horních drážek y ±20, otvor ⌀16),
    trubka ⌀38 se dvěma lůžky ⌀28 × 8 pro 6001-2RS (mezi nimi osazení ⌀24)."""
    s = box(-28, 28, -40, 40, ZT, Z_BASE).union(cyl(38, Z_BLK - Z_BASE, Z_BASE))
    s = s.cut(cyl(16, Z_BLK - ZT + 1, ZT - 0.5))
    s = s.cut(cyl(BRG[1], BRG[2], Z_BR0)).cut(cyl(BRG[1], BRG[2] + 0.5, Z_BR1)).cut(cyl(24, Z_BR1 - Z_BR0, Z_BR0))
    s = s.cut(cyl(20.5, 2, Z_BR0 - 2))                       # lower bearing rests on its outer ring only
    for x in (-20, 20):
        for y in (-20, 20):
            s = s.cut(cyl(5.5, 6, ZT - 0.5, x, y))
    return s


def bearings():
    return [cyl(BRG[1], BRG[2], z0).cut(cyl(BRG[0], BRG[2], z0)) for z0 in (Z_BR0, Z_BR1)]


def motor_bracket():
    """P16 – stojánek motoru 28BYJ-48 na horní straně příčníku (strana −x): deska s otvory pro uši M4 (rozteč 35)
    a hřídel, dvě nohy, patka 2× M5 do horních drážek (y ±20), držák Hall senzoru A3144 u věnce."""
    xm = -A_DIST - 8                                        # motor body axis (shaft 8 mm closer to the axis)
    plate = box(-88, -26, -24, 24, Z_MPL[0], Z_MPL[1]).cut(cyl(28, 10, Z_MPL[0] - 1))
    plate = plate.cut(cyl(10, 10, Z_MPL[0] - 1, -A_DIST, 0))
    for y in (-17.5, 17.5):
        plate = plate.cut(cyl(4.4, 10, Z_MPL[0] - 1, xm, y))
    legs = box(-88, -80, -24, 24, ZT + 4, Z_MPL[0])
    foot = box(-92, -72, -30, 30, ZT, ZT + 4)
    for y in (-20, 20):
        foot = foot.cut(cyl(5.5, 6, ZT - 1, -82, y))
    hall = box(-46, -36, 24, 30, Z_MPL[0], Z_GEAR[1])        # Hall sensor face next to the gear rim
    return plate.union(legs).union(foot).union(hall).union(box(-46, -40, 20, 24, Z_MPL[0], Z_MPL[1]))


def motor():
    """28BYJ-48 (model): tělo ⌀28 × 19 pod deskou, hřídel 8 mm mimo osu těla směrem k ose vzorku, uši ±17,5."""
    xm = -A_DIST - 8
    s = cyl(28, 19, Z_MPL[0] - 19, xm, 0).union(box(xm - 3.5, xm + 3.5, -21, 21, Z_MPL[0] - 1, Z_MPL[0]))
    s = s.union(box(xm - 24, xm - 13, -8, 8, Z_MPL[0] - 18, Z_MPL[0] - 2))                     # wire cap
    shaft = cyl(5, Z_GEAR[1] - Z_MPL[0], Z_MPL[0], -A_DIST, 0).intersect(
        box(-A_DIST - 1.5, -A_DIST + 1.5, -3, 3, Z_MPL[0], Z_GEAR[1] + 1).union(cyl(5, 1.5, Z_MPL[0], -A_DIST, 0)))
    return s.union(shaft).union(cyl(9, Z_MPL[1] - Z_MPL[0] + 0.5, Z_MPL[0], -A_DIST, 0)).cut(cyl(10.2, 0.4, Z_MPL[1] + 0.1, -A_DIST, 0))


def pinion():
    """P19 – pastorek m1 z12 na hřídel 28BYJ-48 (⌀5 se dvěma ploškami 3 mm), natočený do záběru."""
    g = gear(M_G, Z_PIN, Z_GEAR[1] - Z_GEAR[0], Z_GEAR[0], -A_DIST, 0, phase=180.0 / Z_PIN)
    return g.cut(cyl(5.2, 10, Z_GEAR[0] - 1, -A_DIST, 0).intersect(box(-A_DIST - 1.7, -A_DIST + 1.7, -3, 3, Z_GEAR[0] - 1, Z_GEAR[1] + 1)))


def rpi_tray():
    """P18 – vanička pro box P06 (RPi 5) na horní straně příčníku, x 40 … 150; 2× M5 do horní drážky y −20."""
    s = box(40, 150, -50, 50, ZT, ZT + 12).cut(box(43, 147, -47, 47, ZT + 2, ZT + 13))
    for x in (70, 120):
        s = s.cut(cyl(5.5, 3, ZT - 0.5, x, -20))
    return s.cut(box(80, 110, 46, 51, ZT + 4, ZT + 13))                                       # cable notch (+y)


def rpi_box():
    """Box P06 (RPi 5, víko P07 nahoře) ležící ve vaničce (model)."""
    return bp.camera_box().rotate((0, 0, 0), (0, 0, 1), 90).translate((95, 0, ZT + 2 + 35))


# ------------------------------------------------------------------------------------------------ rotating parts
def shaft():
    """Hřídel ⌀12 h6 × 120 (kalená broušená tyč), prochází otvorem ⌀14 v příčníku."""
    return cyl(12, SHAFT[1] - SHAFT[0], SHAFT[0])


def collar():
    """Stavěcí kroužek DIN 705-A 12 (⌀22 × 12) – hřídel na něm visí, opírá se o vnitřní kroužek horního ložiska."""
    return cyl(22, 12, Z_COL[0]).cut(cyl(12, 12, Z_COL[0]))


def big_gear():
    """P17 – ozubené kolo m1 z72 s nábojem ⌀24 × 6 a červíkem M4 (matice v kapse); magnet ⌀6 × 2 pro výchozí polohu."""
    s = gear(M_G, Z_RING, Z_GEAR[1] - Z_GEAR[0], Z_GEAR[0]).union(cyl(24, 6, Z_GEAR[1]))
    s = s.cut(cyl(12.2, 13, Z_GEAR[0] - 0.5))
    s = s.cut(cq.Workplane("YZ").workplane(offset=0).center(0, Z_GEAR[1] + 3).circle(1.7).extrude(14))  # M4 set screw (+x)
    s = s.cut(box(6, 9.5, -3.6, 3.6, Z_GEAR[1] + 0.2, Z_GEAR[1] + 6.1))                    # M4 nut trap
    return s.cut(cyl(6.2, 2.2, Z_GEAR[1] - 2.2, -31.0, 0) .rotate((0, 0, 0), (0, 0, 1), 90))  # magnet at −y (home)


def _head_local():
    """Head box in its own frame: window centre at the origin, optical axis −z, box 34 × 34 × 24 behind it."""
    s = cq.Workplane("XY").box(34, 34, 24, centered=(True, True, False)).edges("|Z").fillet(3)
    s = s.cut(cq.Workplane("XY").workplane(offset=2).rect(28, 28).extrude(23))                 # cavity, open back
    s = s.cut(cyl(12, 3, -0.5))                                                              # window ⌀12 (lens)
    for x in (-10.5, 10.5):
        for y in (-6.25, 6.25):
            s = s.cut(cyl(2.2, 4, -0.5, x, y))                                               # CM3 M2 holes 21 × 12.5
    return s


def _place_head(s):
    return s.rotate((0, 0, 0), (1, 0, 0), p.C_ORB_TILT).translate(WIN)


def _local_to_world(v):
    x, y, z = v
    return (x + WIN[0], y * math.cos(th) - z * math.sin(th) + WIN[1], y * math.sin(th) + z * math.cos(th) + WIN[2])


def arm_head():
    """P14 – rameno s nábojem a hlavou kamery (jeden díl): náboj ⌀28 × 20 na hřídel ⌀12 (2 červíky M4, matice v kapsách),
    vodorovné rameno 10 × 8 pod příčníkem, hlava 34 × 34 × 24 s okénkem ⌀12 pro Camera Module 3 (sklon 36,5°)."""
    hubs = cyl(28, Z_HUB[1] - Z_HUB[0], Z_HUB[0]).cut(cyl(12.2, Z_HUB[1] - Z_HUB[0] + 1, Z_HUB[0] - 0.5))
    for zz in (Z_HUB[0] + 5, Z_HUB[0] + 15):
        hubs = hubs.cut(cq.Workplane("YZ").center(0, zz).circle(1.7).extrude(16))            # M4 set screws (+x)
        hubs = hubs.cut(box(7.5, 10.5, -3.6, 3.6, zz - 4, zz + 4))                            # nut traps
    top = _local_to_world((0, 17, 16))                                                       # axis-side face of the head
    run = box(-5, 5, top[1] - 4, -10, Z_HUB[0] + 2, Z_HUB[0] + 10)
    web = box(-5, 5, top[1] - 4, top[1] + 10, top[2] - 6, Z_HUB[0] + 10)
    head = _place_head(_head_local())
    return hubs.union(run).union(web).union(head)


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


FIXED = [("P12 bearing block on the top beam (print)", bearing_block), ("P16 motor stand (print)", motor_bracket),
         ("stepper 28BYJ-48 5 V", motor), ("P19 pinion m1 z12 (print)", pinion),
         ("P18 RPi tray on the top beam (print)", rpi_tray), ("P06 box with RPi 5 (on the top beam)", rpi_box)]
ROTATING = [("shaft D12 h6 x120", shaft), ("shaft collar DIN 705-A 12 (orbit)", collar),
            ("P17 gear m1 z72 (print)", big_gear), ("P14 camera arm + hub + head (print)", arm_head),
            ("P15 head lid (print)", head_lid), ("Raspberry Pi Camera Module 3", cm3),
            ("LED white 1 W on star D20 (photo light)", led)]
PRINT_ORBIT = [("E7-P12_orbit_bearing_block", bearing_block, 1), ("E7-P14_camera_arm_head", arm_head, 1),
               ("E7-P15_head_lid", head_lid, 1), ("E7-P16_motor_stand", motor_bracket, 1),
               ("E7-P17_gear_z72", big_gear, 1), ("E7-P18_rpi_tray", rpi_tray, 1), ("E7-P19_pinion_z12", pinion, 1)]


def rotating(angle=0.0):
    """Rotating parts turned by `angle` degrees about the sample axis (0 = home on −y)."""
    return [(n, _rotz(f(), angle)) for n, f in ROTATING]


def add_to(asm, prefix="", colors=None, angle=0.0):
    C = colors or {}
    for n, f in FIXED:
        asm.add(f(), name=prefix + n, color=C.get("petg") if "print" in n else (C.get("ins") if "RPi" in n else C.get("steel")))
    for k, b in enumerate(bearings()):
        asm.add(b, name=f"{prefix}bearing 6001-2RS {k + 1}", color=C.get("steel"))
    for n, s in rotating(angle):
        c = C.get("petg") if "print" in n else (C.get("temp") if "LED" in n else (C.get("sensor") if "Camera" in n else C.get("steel")))
        asm.add(s, name=prefix + n, color=c)
