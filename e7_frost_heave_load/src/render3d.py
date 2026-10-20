"""Shaded PNG previews of the STEP assemblies (matplotlib, no GPU needed)."""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import model3d as m

LIGHT = np.array([0.4, -0.6, 0.7])
LIGHT = LIGHT / np.linalg.norm(LIGHT)


def faces(asm):
    for shape, name, loc, color in asm:
        rgba = color.toTuple() if color else (0.7, 0.7, 0.7, 1)
        vs, ts = shape.moved(loc).tessellate(1.0, 0.5)
        v = np.array([[q.x, q.y, q.z] for q in vs])
        for t in ts:
            yield v[list(t)], rgba


def render(asm, path, elev=22, azim=-60, title=""):
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection="3d")
    polys, cols = [], []
    for tri, rgba in faces(asm):
        n = np.cross(tri[1] - tri[0], tri[2] - tri[0])
        nn = np.linalg.norm(n)
        shade = 0.55 + 0.45 * abs(np.dot(n / nn, LIGHT)) if nn else 0.8
        polys.append(tri)
        cols.append((rgba[0] * shade, rgba[1] * shade, rgba[2] * shade, rgba[3]))
    pc = Poly3DCollection(polys, facecolors=cols, edgecolors="none")
    ax.add_collection3d(pc)
    allv = np.concatenate(polys)
    mn, mx = allv.min(0), allv.max(0)
    c, r = (mn + mx) / 2, (mx - mn).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r)
    ax.set_ylim(c[1] - r, c[1] + r)
    ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_title(title, fontsize=12)
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    import cadquery as cq
    a = cq.Assembly(); m.variant_a(a)
    b = cq.Assembly(); m.variant_b(b)
    render(a, os.path.join(m.OUT, "E7_variant_A.png"), title="E7 variant A – constant load")
    render(b, os.path.join(m.OUT, "E7_variant_B.png"), title="E7 variant B – constant height")
    amr = cq.Assembly(); m.variant_a(amr, multiring=True)
    render(amr, os.path.join(m.OUT, "E7_variant_A_multiring.png"), title="E7 variant A – multi-ring cell")
    mr = cq.Assembly(); m.multiring_cell(mr)
    render(mr, os.path.join(m.OUT, "E7_multiring_cell.png"), elev=18, azim=-50, title="E7 multi-ring cell")
    render(m.freezer_layout(), os.path.join(m.OUT, "E7_freezer_layout.png"), elev=35, azim=-70,
           title="E7 – both rigs in the chest freezer")
