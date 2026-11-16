"""E7-V07 – fáze 1, varianta U BEZ ZATÍŽENÍ: sestavný výkres z 3D modelu (skryté hrany HLR) + zorné pole kamery
a paprsky laseru, hlavní kóty a seznam dílů fáze 1.

Run: python vykres_u.py → ../vykresy/E7-V07_bez_zatizeni.pdf + .png
"""
import datetime
import math
import os

import cadquery as cq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import buildparts as bp
import model3d as m
import params as p
from vyrobni_vykresy import project

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "vykresy")
TODAY = datetime.date.today().isoformat()
S = 1 / 3.0                                   # 1 : 3 on A3
INK, HID, CAM, LAS, MUTE = "#111111", "#9a9a9a", "#1f5fa8", "#d23a2a", "#555555"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7})


def assembly():
    a = cq.Assembly()
    m.variant_u(a)
    return [(n.split("/")[-1], s.moved(l)) for s, n, l, c in a]


def draw_view(ax, comp, view, ox, oy, flip=False):
    vis, hid, _ = project(comp, view)
    for pl in hid:
        xs, ys = zip(*pl)
        ax.plot([ox + (-x if flip else x) * S for x in xs], [oy + y * S for y in ys], lw=0.25, c=HID, ls=(0, (2, 1.5)))
    for pl in vis:
        xs, ys = zip(*pl)
        ax.plot([ox + (-x if flip else x) * S for x in xs], [oy + y * S for y in ys], lw=0.45, c=INK)


def dim_v(ax, x, z0, z1, ox, oy, txt, side=1):
    X = ox + x * S
    ax.annotate("", (X, oy + z0 * S), (X, oy + z1 * S), arrowprops=dict(arrowstyle="<->", lw=0.5, shrinkA=0, shrinkB=0))
    ax.text(X + side * 1.2, oy + (z0 + z1) / 2 * S, txt, rotation=90, ha="left" if side > 0 else "right", va="center",
            fontsize=6.5)


def main():
    parts = assembly()
    solids = [s for n, s in parts]
    comp = cq.Compound.makeCompound(solids)
    fig = plt.figure(figsize=(420 / 25.4, 297 / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 420); ax.set_ylim(0, 297); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((10, 10), 400, 277, fill=False, lw=0.9, ec=INK))
    ax.text(18, 277, "Fáze 1 – sestava BEZ ZATÍŽENÍ (varianta U): kamera a laser vidí celý povrch ⌀100", fontsize=12,
            weight="bold")
    ax.text(18, 271, "Stejný rám z T-profilů, kamera, laser a podložky G10 jako varianta C (fáze 2). Bez pístu, závaží, "
                     "vodicí tyče, ložiska a LVDT. Cela s rovným čelem jen 5 mm nad pískem. Měřítko 1 : 3.",
            fontsize=7.5, color=MUTE)

    z_sand = bp.Z_S1
    # --- side view (paper x = world y), eye on +x looking −x → flip so that +y (laser) is on the right
    ox1, oy1 = 112, 45 + 48 * S
    draw_view(ax, comp, "right", ox1, oy1)
    ax.text(ox1 - 80, 252, "POHLED Z BOKU (rovina kamery a laseru, +y vpravo)", fontsize=8, weight="bold")
    # camera field of view and laser rays (world y, z) → paper
    th = math.radians(p.C_CAM_TILT)
    wy = p.C_CAM_Y + 36 * math.sin(th)
    wz = z_sand + p.C_CAM_H - 36 * math.cos(th)
    P = lambda y, z: (ox1 + y * S, oy1 + z * S)
    for y in (-50, 50):
        (x0, y0), (x1, y1) = P(wy, wz), P(y, z_sand)
        ax.plot([x0, x1], [y0, y1], c=CAM, lw=0.7, ls="--")
    yr, zr = p.C_REF_XY[1], bp.Z_REF_U + 8
    (x0, y0), (x1, y1) = P(wy, wz), P(yr, zr)
    ax.plot([x0, x1], [y0, y1], c=CAM, lw=0.5, ls=":")
    ly, lz = p.C_LASER_Y, z_sand + p.C_LASER_H
    for y in (-59.5, 0, 59.5):
        (x0, y0), (x1, y1) = P(ly, lz), P(y, z_sand)
        ax.plot([x0, x1], [y0, y1], c=LAS, lw=0.6)
    ax.text(16, oy1 + (wz + 75) * S, f"kamera RPi HQ + 6 mm\ny {p.C_CAM_Y:g}, {p.C_CAM_H:g} nad pískem,\nsklon {p.C_CAM_TILT:g}° "
            "od svislice\n+ bílá LED vedle okénka", color=CAM, fontsize=6.5, ha="left")
    ax.text(*P(ly + 25, lz + 22), f"laser 11 čar, 635 nm\ny {ly:g}, {p.C_LASER_H:g} nad pískem,\n{p.C_LASER_ANG:g}° od vodorovné",
            color=LAS, fontsize=6.5)
    ax.annotate("invarový terčík P03\n(reference posunu rámu)", P(yr, zr), (18, oy1 + (zr - 75) * S), color=CAM, fontsize=6,
                arrowprops=dict(arrowstyle="-", lw=0.4, color=CAM))
    # dimensions
    zf = -48.0
    dim_v(ax, 185, zf, 375.1, ox1, oy1, "423 celková výška", side=1)
    dim_v(ax, -180, zf, z_sand, ox1, oy1, f"{z_sand - zf:g} povrch písku", side=-1)
    zt = z_sand + p.C_U_RIM
    ax.annotate(f"čelo cely\n{p.C_U_RIM:g} mm nad pískem", P(60, zt), P(116, zt - 45), fontsize=6.5,
                arrowprops=dict(arrowstyle="-", lw=0.4))
    # --- front view (paper x = world x)
    ox2, oy2 = 255, oy1
    draw_view(ax, comp, "front", ox2, oy2)
    ax.text(ox2 - 60, 252, "POHLED ZEPŘEDU (rovina x–z)", fontsize=8, weight="bold")
    X = lambda x: ox2 + x * S
    ax.annotate("", (X(-170), oy2 + (zf - 8) / 1 * S), (X(170), oy2 + (zf - 8) * S),
                arrowprops=dict(arrowstyle="<->", lw=0.5, shrinkA=0, shrinkB=0))
    ax.text(X(0), oy2 + (zf - 8) * S - 1.2, "340 (horní příčník T04)", ha="center", va="top", fontsize=6.5)
    # --- parts table (phase 1)
    rows = [("rám T-profily T01–T04, úhelníky, T-matice, nohy", "1 sada", "ENPRAG"),
            ("cela ⌀220 × 171 s rovným čelem (E7-V03u)", "1", "tisk PETG-CF"),
            ("podložky G10 ⌀20 × 40", "3", "Elektroizolanty"),
            ("sloupek Invar ⌀16 × 330 + patka P04", "1", "Rokycany / tisk"),
            ("rameno s terčíkem P03 (nová trasa)", "1", "tisk"),
            ("box kamery P06 + víko P07, závěs P08", "1", "tisk"),
            ("RPi 5 + HQ kamera + objektiv 6 mm", "1", "RPishop.cz"),
            ("laser Picotronic DOE253, držák P05", "1", "Picotronic / tisk"),
            ("bílá LED 5 V na hvězdě ⌀20 + MOSFET", "1", "GME / TME"),
            ("stěrka P10u (břit 5 mm)", "1", "tisk"),
            ("bod M: TDR CS645, Pt100, vlákno; NTC ve dně", "–", "máte / TME")]
    tx, ty = 330, 240
    ax.text(tx, ty + 4, "DÍLY FÁZE 1", fontsize=8, weight="bold")
    wc = (52, 9, 22)
    for k, r in enumerate(rows):
        y = ty - k * 6.2
        ax.plot([tx, tx + sum(wc)], [y - 1.6, y - 1.6], lw=0.25, c=MUTE)
        ax.text(tx, y, r[0], fontsize=5.6)
        ax.text(tx + wc[0] + wc[1] / 2, y, r[1], fontsize=5.6, ha="center")
        ax.text(tx + wc[0] + wc[1] + 1, y, r[2], fontsize=5.6)
    ny = ty - len(rows) * 6.2 - 6
    notes = ["NEPOUŽÍVÁ SE (až fáze 2):", "píst L04/L05, kulička, Invar ⌀12,", "kroužek, nosná deska L03, závaží",
             "L06/L07, pouzdro igus + P01, LVDT", "+ rameno P02, zdroj 24 V, P09, P11.", "",
             "Ověřeno v modelu:", "• bez kolizí (42 dílů)", "• kamera vidí ≈ 99 % povrchu ⌀100,", "  laser osvítí ≈ 99,7 % (§22)",
             "• objektiv 6 mm: ±24° / −17…+19°", "  (rezerva 2–3° do ±27,6 / ±21,4)", "• terčík P03 vidí kamera i laser",
             "• 1 pixel ≈ 30 µm, výška ≈ 10 µm"]
    for k, s in enumerate(notes):
        ax.text(tx, ny - k * 4.4, s, fontsize=6.2, weight="bold" if s.endswith(":") else None)
    # title block
    x0, y0, w, h = 410 - 170, 10, 170, 24
    ax.add_patch(Rectangle((x0, y0), w, h, fill=False, lw=0.6, ec=INK))
    for k, (a_, b_) in enumerate((("E7-V07  Fáze 1 – sestava bez zatížení (varianta U)", "A3  1 : 3"),
                                  ("z 3D modelu model3d.variant_u, skryté hrany čárkovaně", "rozměry v mm"),
                                  ("E7 – mrznutí a tání / sublimace", f"{TODAY}  návrh"))):
        yy = y0 + h - (k + 1) * h / 3
        if k:
            ax.plot([x0, x0 + w], [yy + h / 3] * 2, lw=0.4, c=INK)
        ax.text(x0 + 2, yy + 2.5, a_, fontsize=8 if k == 0 else 6.5, weight="bold" if k == 0 else None)
        ax.text(x0 + w - 2, yy + 2.5, b_, fontsize=6.5, ha="right")
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "E7-V07_bez_zatizeni.pdf"))
    fig.savefig(os.path.join(OUT, "E7-V07_bez_zatizeni.png"), dpi=150)
    print("→ vykresy/E7-V07_bez_zatizeni.pdf")


if __name__ == "__main__":
    main()
