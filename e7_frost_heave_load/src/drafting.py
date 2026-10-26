"""Minimální kreslicí knihovna nad matplotlib: list A3, razítko, kóty, odkazy.

Souřadnice listu jsou v mm papíru (0–420 × 0–297). Pohled (View) převádí
souřadnice modelu v mm do papíru podle měřítka, takže kóty jsou vždy
skutečné rozměry modelu.
"""
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

PROJECT = "E7 – freeze–thaw loading tests"
PT_PER_MM = 72 / 25.4
THICK = 0.5 * PT_PER_MM
THIN = 0.25 * PT_PER_MM
FS = 7.0            # běžný text [pt]
FS_SMALL = 6.0
INK = "#1a1a1a"
WATER = "#a9c4e0"
SOIL = "#ddd3bf"
FROZEN = "#c9d3dc"
INSUL = "#f0e3c2"
METAL = "#c8cbcf"
PLASTIC = "#ebe9e4"
RED = "#b8322a"
BLUE = "#2b62a3"

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["hatch.linewidth"] = 0.4


class Sheet:
    W, H = 420.0, 297.0

    def __init__(self, title, number, scale, sheet_no, sheet_total, subtitle=""):
        self.fig = plt.figure(figsize=(self.W / 25.4, self.H / 25.4))
        ax = self.fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, self.W)
        ax.set_ylim(0, self.H)
        ax.set_aspect("equal")
        ax.axis("off")
        self.ax = ax
        # (no outer frame)
        self._title_block(title, number, scale, sheet_no, sheet_total, subtitle)

    def _title_block(self, title, number, scale, n, tot, subtitle):
        ax, x0, y0, w = self.ax, 250.0, 10.0, 160.0
        rows = [8, 8, 8, 14]
        y = y0
        for h in rows:
            ax.add_patch(Rectangle((x0, y), w, h, fill=False, lw=THIN, ec=INK))
            y += h
        ax.plot([x0 + 40, x0 + 40], [y0, y0 + 24], lw=THIN, c=INK)
        ax.plot([x0 + 110, x0 + 110], [y0, y0 + 24], lw=THIN, c=INK)
        t = lambda x, yy, s, **k: ax.text(x, yy, s, va="center", fontsize=min(k.pop("fs", FS_SMALL), 9.5), color=INK, **k)
        t(x0 + 2, y0 + 4, "scale")
        t(x0 + 22, y0 + 4, scale, fs=FS, weight="bold")
        t(x0 + 42, y0 + 4, "drawing no.")
        t(x0 + 70, y0 + 4, number, fs=FS + 1, weight="bold")
        t(x0 + 112, y0 + 4, f"sheet {n} / {tot}")
        t(x0 + 2, y0 + 12, "units")
        t(x0 + 22, y0 + 12, "mm")
        t(x0 + 42, y0 + 12, "project")
        t(x0 + 60, y0 + 12, PROJECT)
        t(x0 + 112, y0 + 12, "date " + __import__("datetime").date.today().isoformat())
        t(x0 + 2, y0 + 20, "status")
        t(x0 + 22, y0 + 20, "DRAFT")
        t(x0 + 42, y0 + 20, "drawn")
        t(x0 + 60, y0 + 20, "Claude Code (draft)")
        t(x0 + 112, y0 + 20, "checked: —")
        ax.text(x0 + 2, y0 + 28.5, title, va="center", fontsize=min(FS + 3, 12.5), color=INK, weight="bold")
        if subtitle:
            t(x0 + 2, y0 + 33.5, subtitle, fs=FS_SMALL)

    def text(self, x, y, s, **k):
        k.setdefault("fontsize", FS)
        k.setdefault("color", INK)
        return self.ax.text(x, y, s, **k)

    def heading(self, x, y, s):
        self.text(x, y, s, fontsize=FS + 2, weight="bold", va="bottom")

    def save(self, pdf, png_path):
        pdf.savefig(self.fig)
        self.fig.savefig(png_path, dpi=150)
        plt.close(self.fig)


class View:
    """Pohled: model (x, z) [mm] → papír. ox, oy = poloha počátku modelu na papíře."""

    def __init__(self, sheet, ox, oy, scale, label=None, label_xy=None):
        self.s, self.ax, self.ox, self.oy, self.k = sheet, sheet.ax, ox, oy, scale
        if label:
            lx, ly = label_xy
            sheet.text(lx, ly, label, fontsize=FS + 1.5, weight="bold", ha="center")

    def p(self, x, z):
        return self.ox + x * self.k, self.oy + z * self.k

    # --- tvary ---------------------------------------------------------
    def rect(self, x0, z0, x1, z1, fc="none", ec=INK, lw=THICK, hatch=None, z=2, **k):
        (a, b), (c, d) = self.p(x0, z0), self.p(x1, z1)
        r = Rectangle((min(a, c), min(b, d)), abs(c - a), abs(d - b), fc=fc, ec=ec, lw=lw,
                      hatch=hatch, zorder=z, **k)
        self.ax.add_patch(r)
        return r

    def poly(self, pts, fc="none", ec=INK, lw=THICK, hatch=None, z=2, closed=True, **k):
        P = Polygon([self.p(*q) for q in pts], closed=closed, fc=fc, ec=ec, lw=lw,
                    hatch=hatch, zorder=z, **k)
        self.ax.add_patch(P)
        return P

    def circle(self, x, z, r, fc="none", ec=INK, lw=THICK, z_=3, **k):
        c = Circle(self.p(x, z), r * self.k, fc=fc, ec=ec, lw=lw, zorder=z_, **k)
        self.ax.add_patch(c)
        return c

    def line(self, pts, c=INK, lw=THIN, ls="-", z=3, **k):
        P = [self.p(*q) for q in pts]
        self.ax.plot([q[0] for q in P], [q[1] for q in P], c=c, lw=lw, ls=ls, zorder=z,
                     solid_capstyle="butt", **k)

    def axis_line(self, pts):
        self.line(pts, lw=THIN, ls=(0, (12, 3, 2, 3)), c="#555555", z=1)

    def hidden(self, pts, c=INK):
        self.line(pts, lw=THIN, ls=(0, (4, 2)), c=c)

    def text(self, x, z, s, **k):
        k.setdefault("fontsize", FS)
        k.setdefault("color", INK)
        k.setdefault("zorder", 6)
        return self.ax.text(*self.p(x, z), s, **k)

    # --- kóty ----------------------------------------------------------
    def _arrow(self, a, b):
        self.ax.annotate("", xy=b, xytext=a, zorder=5,
                         arrowprops=dict(arrowstyle="<|-|>", lw=THIN, color=INK,
                                         shrinkA=0, shrinkB=0, mutation_scale=6))

    def dim_h(self, x0, x1, z, at, text=None, fmt="{:g}", side="above"):
        """Vodorovná kóta mezi x0 a x1 vynesená v z = at (model)."""
        a, b = self.p(x0, at), self.p(x1, at)
        for x in (x0, x1):
            p0, p1 = self.p(x, z), self.p(x, at)
            ext = 1.5 if at > z else -1.5
            self.ax.plot([p0[0], p1[0]], [p0[1] + (0.8 if at > z else -0.8), p1[1] + ext], lw=THIN * 0.8, c=INK, zorder=5)
        self._arrow(a, b)
        s = text if text is not None else fmt.format(abs(x1 - x0))
        dy = 0.8 if side == "above" else -0.8
        self.ax.text((a[0] + b[0]) / 2, a[1] + dy, s, ha="center",
                     va="bottom" if side == "above" else "top", fontsize=FS_SMALL, color=INK,
                     zorder=6, bbox=dict(fc="white", ec="none", pad=0.3))

    def dim_v(self, z0, z1, x, at, text=None, fmt="{:g}"):
        a, b = self.p(at, z0), self.p(at, z1)
        for zz in (z0, z1):
            p0, p1 = self.p(x, zz), self.p(at, zz)
            ext = 1.5 if at > x else -1.5
            self.ax.plot([p0[0] + (0.8 if at > x else -0.8), p1[0] + ext], [p0[1], p1[1]], lw=THIN * 0.8, c=INK, zorder=5)
        self._arrow(a, b)
        s = text if text is not None else fmt.format(abs(z1 - z0))
        self.ax.text(a[0] - 0.8, (a[1] + b[1]) / 2, s, ha="right", va="center", rotation=90,
                     fontsize=FS_SMALL, color=INK, zorder=6, bbox=dict(fc="white", ec="none", pad=0.3))

    def balloon(self, x, z, n, tx, tz):
        """Pozice: tečka v (x, z), odkazová čára, kroužek s číslem v (tx, tz) – vše model."""
        a, b = self.p(x, z), self.p(tx, tz)
        r = 2.6
        d = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
        end = (b[0] - (b[0] - a[0]) / d * r, b[1] - (b[1] - a[1]) / d * r)
        self.ax.plot([a[0], end[0]], [a[1], end[1]], lw=THIN, c=INK, zorder=7)
        self.ax.add_patch(Circle(a, 0.6, fc=INK, ec="none", zorder=7))
        self.ax.add_patch(Circle(b, r, fc="white", ec=INK, lw=THIN, zorder=7))
        self.ax.text(*b, str(n), ha="center", va="center", fontsize=FS_SMALL, zorder=8, color=INK)

    def note(self, x, z, s, tx, tz, **k):
        a, b = self.p(x, z), self.p(tx, tz)
        self.ax.plot([a[0], b[0]], [a[1], b[1]], lw=THIN, c=INK, zorder=7)
        self.ax.add_patch(Circle(a, 0.5, fc=INK, ec="none", zorder=7))
        k.setdefault("fontsize", FS_SMALL)
        k.setdefault("va", "center")
        k.setdefault("ha", "left" if b[0] >= a[0] else "right")
        pad = 0.8 if k["ha"] == "left" else -0.8
        k.setdefault("color", INK)
        self.ax.text(b[0] + pad, b[1], s, zorder=8, **k)

    def break_line(self, x0, x1, z):
        """Zlomová čára (přerušení) vodorovně v z."""
        n = 6
        pts = []
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            dz = 0 if i in (0, n) else (1.5 if i % 2 else -1.5) / self.k
            pts.append((x, z + dz))
        self.line(pts, lw=THIN)


def table(sheet, x, y, cols, rows, widths, row_h=4.6, header=True, fs=None):
    """Jednoduchá tabulka; (x, y) = levý horní roh v mm papíru."""
    fs = fs or FS_SMALL
    ax = sheet.ax
    allrows = ([cols] if header else []) + rows
    for i, r in enumerate(allrows):
        yy = y - (i + 0.5) * row_h
        xx = x
        for w, c in zip(widths, r):
            ax.text(xx + 1, yy, str(c), va="center", fontsize=fs, color=INK,
                    weight="bold" if (header and i == 0) else "normal")
            xx += w
        ax.plot([x, x + sum(widths)], [y - (i + 1) * row_h] * 2, lw=THIN * (1.6 if header and i == 0 else 0.6), c=INK)
    ax.plot([x, x + sum(widths)], [y, y], lw=THIN * 1.6, c=INK)
    return y - len(allrows) * row_h
