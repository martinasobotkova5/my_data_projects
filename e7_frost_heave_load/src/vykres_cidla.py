"""E7-V09 – umístění čidel ve vzorku ⌀100 × 100 (revize 20. 11. 2026): řez, půdorys, tabulka.

Spuštění: cd src && python3 vykres_cidla.py  → ../vykresy/E7-V09_cidla_ve_vzorku.pdf (+ .png)
"""
import datetime
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                       # noqa: E402
from matplotlib.patches import Circle, Rectangle, Wedge   # noqa: E402

import model3d as m                                   # noqa: E402
import params as p                                    # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "vykresy")
INK, MUTE, SAND, WALL = "#1f2328", "#6e7781", "#f3e3b5", "#d0d7de"
CT, CP, CF, CTD = "#cf222e", "#8250df", "#1a7f37", "#0969da"     # teploty, Pt100, vlákno, TDR

zb = m.Z_S0 - p.BODY_BOTTOM
z_top = zb + p.COLLAR_TOP - p.TDR_CS645["top_from_collar"]
D_ROD = [m.Z_S1 - (z_top - k * p.TDR_CS645["pitch"]) for k in range(3)]
D_PT = D_ROD[0] - p.C_PT100_DZ
D_OF = D_ROD[0] - 2.0
RI, RO = p.CAV_D / 2, p.BODY_D / 2 + p.C_SLEEVE_T


def section(ax):
    """Svislý řez rovinou portu bodu M (strana −y vlevo); sondy T1–T5 sklopené do roviny řezu (úhel v popisku)."""
    ax.add_patch(Rectangle((-RO, -p.C_INS_T - p.BODY_BOTTOM), RO - RI, 100 + p.C_INS_T + p.BODY_BOTTOM, fc=WALL, ec=INK, lw=0.8))
    ax.add_patch(Rectangle((RI, -p.C_INS_T - p.BODY_BOTTOM), RO - RI, 100 + p.C_INS_T + p.BODY_BOTTOM, fc=WALL, ec=INK, lw=0.8))
    ax.add_patch(Rectangle((-RI, -p.C_INS_T - p.BODY_BOTTOM), 2 * RI, p.C_INS_T + p.BODY_BOTTOM, fc=WALL, ec=INK, lw=0.8))
    ax.add_patch(Rectangle((-RI, 0), 2 * RI, 100, fc=SAND, ec=INK, lw=1.0))
    # bod M
    for d in D_ROD:
        ax.plot([-RI, -RI + p.TDR_CS645["rod_l"]], [100 - d] * 2, color=CTD, lw=2.2, solid_capstyle="butt")
    ax.add_patch(Rectangle((-RI - p.CUP_WALL_IN - p.C_HEAD_GAP - p.TDR_CS645["head_l"], 100 - D_ROD[2] - 4),
                           p.TDR_CS645["head_l"], D_ROD[2] - D_ROD[0] + 8, fc=CTD, alpha=0.35, ec=CTD))
    ax.plot([-RI, -RI + p.C_PT100_TIP], [100 - D_PT] * 2, color=CP, lw=2.6)
    ax.plot([-RI, -RI + p.OF_TIP_FROM_WALL], [100 - D_OF] * 2, color=CF, lw=1.0, ls="--")
    ax.plot([-RI - p.CUP_WALL_IN, -RI - p.CUP_WALL_IN - p.C_HEAD_GAP / 2, -RI - p.CUP_WALL_IN - p.C_HEAD_GAP / 2, -RO - 8],
            [100 - D_PT, 100 - D_PT, 100 - D_ROD[0] + 6.5, 100 - D_ROD[0] + 6.5], color=CP, lw=0.8)
    ax.text(-RO - 34, 100 - D_ROD[1], f"TDR CS645\n{D_ROD[0]:.0f} / {D_ROD[1]:.0f} / {D_ROD[2]:.0f} mm", color=CTD,
            fontsize=7, va="center", ha="left")
    ax.text(-RO - 34, 100 - D_PT + 7, f"Pt100 {D_PT:.0f} mm\nvlákno {D_OF:.0f} mm", color=CP, fontsize=7, va="center")
    # T1–T5 (sklopené)
    for tag, d, a in p.C_TEMPS:                       # sklopené do pravé poloviny řezu (skutečné úhly v půdorysu)
        x0 = RI - p.C_TEMP_TIP
        ax.plot([x0, RO], [100 - d] * 2, color=CT, lw=0.8)
        ax.add_patch(Rectangle((x0, 100 - d - p.C_TEMP_D / 2), p.C_TEMP_L, p.C_TEMP_D, fc=CT, alpha=0.55, ec=CT))
        ax.add_patch(Rectangle((RO, 100 - d - p.C_GLAND[2] / 2), p.C_GLAND[3], p.C_GLAND[2], fc="#8c959f", ec=INK, lw=0.5))
        ax.text(RO + p.C_GLAND[3] + 3, 100 - d, f"{tag}  {d:g} mm  ({a:g}°)", color=CT, fontsize=7, va="center")
    ax.plot([-RO - 30, RO + 10], [100, 100], color=INK, lw=0.6, ls=":")
    ax.text(RO + 12, 100, "povrch písku = čelo cely", fontsize=7, va="center")
    for d in range(0, 101, 10):
        ax.plot([-3, 3], [100 - d] * 2, color=INK, lw=0.5)
        ax.text(4, 100 - d + 1.2, f"{d}", fontsize=6, ha="left", va="bottom", color=MUTE)
    ax.text(0, 104, "hloubka [mm]", fontsize=6, ha="center", color=MUTE)
    ax.text(-RO, -p.C_INS_T - p.BODY_BOTTOM - 8, "−y: port bodu M; všechny kabely vedou ven na straně −y", fontsize=7, color=MUTE)
    ax.set_title("Řez: vlevo bod M (strana −y), vpravo T1–T5 sklopené do řezu (skutečný úhel v závorce, viz půdorys)", fontsize=9, loc="left")
    ax.set_xlim(-RO - 36, RO + 75); ax.set_ylim(-p.C_INS_T - p.BODY_BOTTOM - 14, 118)
    ax.set_aspect("equal"); ax.axis("off")


def plan(ax):
    """Půdorys: 0° = +x (pravý sloup s krabičkou RPi), 270° = −y (port bodu M)."""
    ax.add_patch(Circle((0, 0), RO, fc=WALL, ec=INK, lw=0.8))
    ax.add_patch(Circle((0, 0), RI, fc=SAND, ec=INK, lw=1.0))
    pw = p.PORT_W / 2
    ax.add_patch(Rectangle((-pw, -RO - 1), 2 * pw, RO - RI - p.CUP_WALL_IN + 1, fc="white", ec=INK, lw=0.5))
    ax.plot([0, 0], [-RI, -RI + p.TDR_CS645["rod_l"]], color=CTD, lw=2.2)
    ax.plot([0.9, 0.9], [-RI, -RI + p.C_PT100_TIP], color=CP, lw=1.6)
    ax.plot([-p.OF_SIDE] * 2, [-RI, -RI + p.OF_TIP_FROM_WALL], color=CF, lw=1.0, ls="--")
    by_ang = {}
    for tag, d, a in p.C_TEMPS:
        by_ang.setdefault(a, []).append(f"{tag} {d:g} mm")
    for a, labels in by_ang.items():
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        r0 = RI - p.C_TEMP_TIP
        ax.plot([r0 * c, (RO + p.C_GLAND[3]) * c], [r0 * s, (RO + p.C_GLAND[3]) * s], color=CT, lw=2.0)
        ax.text((RO + p.C_GLAND[3] + 9) * c, (RO + p.C_GLAND[3] + 9) * s, f"{a:g}°\n" + "\n".join(labels), color=CT,
                fontsize=7, ha="center", va="center")
    c, s = math.cos(math.radians(p.C_NTC_ANG)), math.sin(math.radians(p.C_NTC_ANG))
    ax.plot([0, RO * c], [0, RO * s], color=MUTE, lw=1.0, ls="-.")
    ax.text(RO * c - 6, RO * s + 8, "NTC ve dně (pod pískem)", fontsize=7, color=MUTE, ha="right")
    for k in range(3):
        a = math.radians(90 + 120 * k)
        ax.add_patch(Circle((p.C_PAD_R * math.cos(a), p.C_PAD_R * math.sin(a)), p.C_PAD_D / 2, fc="none", ec=MUTE, lw=0.6, ls=":"))
    for sx in (-1, 1):
        ax.add_patch(Rectangle((sx * p.C_COL_SPAN / 2 - 20, -40), 40, 80, fc="#eaeef2", ec=MUTE, lw=0.6))
    ax.text(p.C_COL_SPAN / 2, 46, "sloup T01 (+x)\nkrabička RPi", fontsize=6.5, ha="center", color=MUTE)
    ax.text(-p.C_COL_SPAN / 2, 46, "sloup T01 (−x)", fontsize=6.5, ha="center", color=MUTE)
    ax.text(0, -RO - 22, "TDR + Pt100 + vlákno (bod M), 270°", fontsize=7, ha="center", color=CTD)
    ax.annotate("", xy=(RO + 30, -RO + 5), xytext=(RO + 5, -RO + 5), arrowprops=dict(arrowstyle="->", lw=0.7))
    ax.text(RO + 32, -RO + 5, "+x (0°)", fontsize=7, va="center")
    ax.set_title("Půdorys (podložky G10 tečkovaně)", fontsize=9, loc="left")
    ax.set_xlim(-p.C_COL_SPAN / 2 - 25, p.C_COL_SPAN / 2 + 25); ax.set_ylim(-RO - 50, RO + 30)
    ax.set_aspect("equal"); ax.axis("off")


def table(ax):
    rows = [("čidlo", "hloubka", "úhel", "poloha / montáž", "čtení")]
    rows.append(("TDR CS645 (bod M)", f"{D_ROD[0]:.0f}/{D_ROD[1]:.0f}/{D_ROD[2]:.0f}", "270°",
                 "3 tyčky ⌀3,2 × 75 vodorovně přes osu; hlava v portu 2–3 mm od stěny", "TDR100/200 → CR850 C1–C3"))
    rows.append(("Pt100 1/10 DIN (bod M)", f"{D_PT:.0f}", "270°", "3,5 mm nad horní tyčkou, hrot 30 mm od stěny; kabel nad hlavou CS645",
                 "4WPB100 → CR850 DIFF2"))
    rows.append(("optické vlákno (bod M)", f"{D_OF:.0f}", "270°", "bočně 4,7 mm, hrot 37,5 mm od stěny; nad hlavou CS645", "vlastní jednotka"))
    for tag, d, a in p.C_TEMPS:
        rows.append((f"{tag} DS18B20 ⌀6 × 50", f"{d:g}", f"{a:g}°", "otvor ⌀6,3, hrot 30 mm od stěny; vývodka M12×1,5 (závitník)",
                     "RPi GPIO4 (1-Wire)"))
    rows.append(("NTC 10 kΩ (dno)", "pod pískem", f"{p.C_NTC_ANG:g}°", "radiální otvor ⌀4 v tištěném dně", "CR850 SE6"))
    rows.append(("vzduch (Campbell 109)", "nad vzorkem", "–", "volně nad čelem cely, mimo dráhu kamery", "CR850 SE5"))
    t = ax.table(cellText=rows[1:], colLabels=rows[0], loc="upper left", cellLoc="left", colLoc="left",
                 colWidths=[0.17, 0.09, 0.06, 0.48, 0.2])
    t.auto_set_font_size(False); t.set_fontsize(7); t.scale(1, 1.25)
    for (r, c), cell in t.get_celld().items():
        cell.set_edgecolor("#d0d7de")
        if r == 0:
            cell.set_text_props(weight="bold")
    ax.axis("off")
    ax.text(0, -0.02, "Bod M zůstává jako v terénu (uprostřed výšky). Profil T1–T5 po 20 mm ve šroubovici kolem strany −y: "
            "od tyček TDR ≥ 14,6 mm, od stěny 30 mm; kabely vedou spolu s bodem M. Otvory po hutnění předvrtat tyčinkou "
            "(⌀3 / ⌀6), nic se nelepí. Okraje otvorů 6 perimetrů – voda nevnikne do výplně.",
            fontsize=7, color=MUTE, transform=ax.transAxes, va="top", wrap=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    fig = plt.figure(figsize=(16.54, 11.69))                      # A3 na šířku
    ax1 = fig.add_axes([0.03, 0.36, 0.52, 0.58]); section(ax1)
    ax2 = fig.add_axes([0.57, 0.36, 0.41, 0.58]); plan(ax2)
    ax3 = fig.add_axes([0.03, 0.06, 0.94, 0.26]); table(ax3)
    fig.text(0.03, 0.965, "E7-V09  Čidla ve vzorku ⌀100 × 100 – TDR, Pt100, vlákno, teplotní profil T1–T5",
             fontsize=13, weight="bold")
    fig.text(0.97, 0.965, f"rev. 20. 11. 2026 · rozměry v mm · {datetime.date.today():%Y-%m-%d}", fontsize=8, ha="right",
             color=MUTE)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, f"E7-V09_cidla_ve_vzorku.{ext}"), dpi=130 if ext == "png" else None)
    print("E7-V09 ok, hloubky tyček TDR", [round(d, 1) for d in D_ROD], "Pt100", round(D_PT, 1))


if __name__ == "__main__":
    main()
