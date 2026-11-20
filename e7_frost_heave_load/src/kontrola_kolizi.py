"""Kontrola sestavy (20. 11. 2026): rozměry v mrazáku a kolize.

1. Výška, půdorys a mezery k mrazáku 590 × 390 × 410 pro fázi 1 (U) a fázi 2 (C).
2. Kolize: každý díl s každým (bez písku a dílů, které se mají dotýkat), oběh kamery po 30° v rozsahu ±180°.

Spuštění: cd src && python3 kontrola_kolizi.py
"""
import itertools
import cadquery as cq
import params as p
import model3d as m

# dvojice, které se dotýkají nebo prostupují záměrně (vložené / zasunuté díly)
OK_PAIRS = ("sand", "cell PETG", "pad", "G10", "rubber", "bolt", "screw", "nut", "T-nut", "bracket", "TDR", "Pt100",
            "optical fibre", "DS18B20", "gland", "cable", "stud", "ball", "rod", "igus", "bearing", "core", "hub",
            "clamp", "spacer", "pinion", "ring", "motor", "piston", "carrier", "disc", "L0", "flag", "endstop")


def solids(asm):
    out = []
    for shape, name, loc, _ in asm:
        if shape is None:
            continue
        s = shape.moved(loc) if loc is not None else shape
        out.append((name.split("/")[-1], s))
    return out


def overlaps(parts, only=None, tol=0.5):
    """Objem průniku > tol mm³; only = podřetězec názvu, který musí mít aspoň jeden z dvojice."""
    hits = []
    for (na, a), (nb, b) in itertools.combinations(parts, 2):
        if only and not (only in na or only in nb):
            continue
        if not a.BoundingBox().intersect(b.BoundingBox()) if hasattr(a.BoundingBox(), "intersect") else False:
            continue
        ba, bb = a.BoundingBox(), b.BoundingBox()
        if ba.xmax < bb.xmin or bb.xmax < ba.xmin or ba.ymax < bb.ymin or bb.ymax < ba.ymin or ba.zmax < bb.zmin or bb.zmax < ba.zmin:
            continue
        try:
            v = a.intersect(b).Volume()
        except Exception:
            continue
        if v > tol:
            hits.append((na, nb, round(v, 1)))
    return hits


def main():
    print("Mrazák (vnitřní):", p.FRZ_L, "×", p.FRZ_W, "×", p.FRZ_H, "mm")
    for k, (h, gap, gx, gy) in m.freezer_clearance().items():
        print(f"  fáze {'1 (U)' if k == 'U' else '2 (C)'}: výška {h:.0f} mm, k víku {gap:.1f} mm, "
              f"po stranách {gx:.0f} mm (délka) a {gy:.0f} mm (šířka)")
    for label, fn in (("fáze 1 (U)", m.variant_u), ("fáze 2 (C)", m.variant_c)):
        # nová čidla proti všemu ostatnímu (bez cely, do které jsou zasunutá)
        a = cq.Assembly(); fn(a)
        parts = [(n, s) for n, s in solids(a) if "sand" not in n]
        sensors = [(n, s) for n, s in parts if any(k in n for k in ("DS18B20", "gland", " cable"))]
        others = [(n, s) for n, s in parts if not any(k in n for k in ("DS18B20", "gland", " cable", "cell PETG"))]
        hits = []
        for (ns, s), (no, o) in itertools.product(sensors, others):
            bs, bo = s.BoundingBox(), o.BoundingBox()
            if bs.xmax < bo.xmin or bo.xmax < bs.xmin or bs.ymax < bo.ymin or bo.ymax < bs.ymin or bs.zmax < bo.zmin or bo.zmax < bs.zmin:
                continue
            v = s.intersect(o).Volume()
            if v > 0.5:
                hits.append((ns, no, round(v, 1)))
        print(f"  {label}: teplotní sondy a vývodky – kolize: {hits or 'žádná'}")
        # oběh kamery: pohyblivé díly proti pevným
        worst = []
        for ang in range(-180, 181, 30):
            a = cq.Assembly(); fn(a, orbit_angle=ang)
            parts = solids(a)
            mov = [(n, s) for n, s in parts if any(k in n for k in ("P13", "P14", "P15", "camera", "CM3", "LED", "flag"))]
            fix = [(n, s) for n, s in parts if (n, s) not in mov and not any(k in n for k in ("P12", "bearing", "igus", "spacer", "clamp", "sand"))]
            for (nm, s), (nf, f) in itertools.product(mov, fix):
                bs, bf = s.BoundingBox(), f.BoundingBox()
                if bs.xmax < bf.xmin or bf.xmax < bs.xmin or bs.ymax < bf.ymin or bf.ymax < bs.ymin or bs.zmax < bf.zmin or bf.zmax < bs.zmin:
                    continue
                v = s.intersect(f).Volume()
                if v > 0.5:
                    worst.append((ang, nm, nf, round(v, 1)))
        print(f"  {label}: oběh ±180° po 30° – kolize: {worst or 'žádná'}")


if __name__ == "__main__":
    main()
