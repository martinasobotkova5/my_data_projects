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


def faces(asm, cut=None):
    for shape, name, loc, color in asm:
        rgba = color.toTuple() if color else (0.7, 0.7, 0.7, 1)
        if cut is not None and ("sand" in name or "insulation" in name):
            rgba = (rgba[0], rgba[1], rgba[2], 0.25)
        sh = shape.moved(loc)
        if cut is not None:
            sh = sh.cut(cut)
            if sh.isNull() or not sh.Solids():
                continue
        vs, ts = sh.tessellate(1.0, 0.5)
        v = np.array([[q.x, q.y, q.z] for q in vs])
        for t in ts:
            yield v[list(t)], rgba


def render(asm, path, elev=22, azim=-60, title="", cut=None):
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection="3d")
    polys, cols = [], []
    for tri, rgba in faces(asm, cut):
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
    xcut = cq.Workplane("XY").box(1000, 2000, 2000, centered=(False, True, True)).val()
    a = cq.Assembly(); m.variant_c(a)
    render(a, os.path.join(m.OUT, "E7_V01_variant_C.png"), elev=18, azim=-35,
           title="E7 C rev. B – dead weight on a partial piston, camera + laser, LVDT")
    render(a, os.path.join(m.OUT, "E7_V01_variant_C_section.png"), elev=10, azim=0, cut=xcut,
           title="E7 C – section x = 0")
    c = cq.Assembly(); m.body_a(c, temps=[], pv=False, pb=False, opt=False, pt_r=m.p.C_PT100_R, pt_ang=m.p.C_PT100_ANG)
    render(c, os.path.join(m.OUT, "E7_V03_cell.png"), elev=20, azim=-100, title="E7 cell rev. B – printed in one piece ⌀240, point M")
    render(m.freezer_layout(), os.path.join(m.OUT, "E7_V05_freezer_layout.png"), elev=35, azim=-70,
           title="E7 – rig C in the chest freezer")
