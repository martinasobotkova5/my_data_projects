"""E7 – variant C: freeze–thaw of the sample in the printed cell (axisymmetric, explicit finite volumes,
enthalpy method). Feeds the animated 3D model web/E7_thaw_3d.html (template web/thaw_3d_template.html).

Illustrative – thermal properties are ASSUMED (table PROPS below), heat transfer coefficients estimated for
still air in a chest freezer. Heave = in-situ expansion of pore water (9 %) only, no ice lenses → upper bound;
in the unsaturated sand (Sr 0.3–0.5) the expansion fits into the pore air, so the expected in-situ heave is ≈ 0.
Also computed: thermal drift of the rig as seen by the LVDT (Al beam vs Invar post) and by the camera
(rim vs Invar reference), from lumped part temperatures.

Run:  python src/sim_thaw.py          rev. B (insulated: XPS sleeve + XPS/G10 under the cell), writes the web files
      python src/sim_thaw.py --bare   original cell on the Al plate, summary only (for comparison)
"""
import json
import math
import os
import sys

import numpy as np

import params as p

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(HERE, "..", "web")

# ---- grid (mm) ----------------------------------------------------------------------------------------
DR, DZ = 2.5, 2.0
NR, NZ = 32, 80                       # r 0–80, z 0–160 (z = 0 underside of the cell)
R_SAND = p.CAV_D / 2                  # 50
R_WALL = 52.5                         # inner PETG tube 3 mm → one cell 50–52.5 (grid)
Z_BOT, Z_SAND, Z_JACKET, Z_TOP = p.BODY_BOTTOM, p.SAND_TOP, p.BODY_H, p.COLLAR_TOP   # 26, 126, 130, 160
R_PIST, H_PIST = p.C_PISTON_D / 2, p.C_PISTON_H

# ---- assumed properties -------------------------------------------------------------------------------
THETA = 0.15                          # volumetric water content (SAND theta 0.10–0.18)
PROPS = {                             # k [W/mK], C [J/m3K]
    "sand_u": (1.2, 1.91e6),          # unfrozen: ρd 1600 × 800 + θ × 4.18e6
    "sand_f": (1.9, 1.57e6),          # frozen: ice instead of water
    "petg": (0.20, 1.60e6),           # inner tube, bottom (100 % infill)
    "jacket": (0.05, 0.20e6),         # outer body, 10 % infill (insulation)
}
L_VOL = THETA * 334e6                 # latent heat 5.0e7 J/m3
T_S, T_L = -0.5, 0.0                  # freezing range (residual unfrozen water)
H_OUT, H_CAV, H_BOT = 7.0, 5.0, 10.0  # W/m2K: free surfaces, inside the collar, underside (Al base plate)
H_CONTACT = 100.0                     # sand – Al piston
INSULATED = "--bare" not in sys.argv
K_XPS = 0.035
# rev. B: XPS sleeve 40 mm on the jacket (side + top ring); XPS 40 + 3 G10 pads ⌀20 under the cell
H_SIDE = 1 / (1 / H_OUT + p.C_SLEEVE_T / 1e3 / K_XPS) if INSULATED else H_OUT
_a_pad = 3 * math.pi / 4 * (p.C_PAD_D / 1e3) ** 2
_a_bot = math.pi / 4 * (p.BODY_D / 1e3) ** 2
_g_ins = (0.3 * _a_pad + K_XPS * (_a_bot - _a_pad)) / (p.C_INS_T / 1e3) / _a_bot      # W/m2K through pads + XPS
H_UNDER = 1 / (1 / H_BOT + 1 / _g_ins) if INSULATED else H_BOT
POROSITY = 0.38                       # → Sr = θ / n ≈ 0.39; pore air n − θ ≫ 0.09 θ
C_PISTON = 2700 * 900 * math.pi / 4 * (p.C_PISTON_D / 1e3) ** 2 * (p.C_PISTON_H / 1e3)   # ≈ 95 J/K
A_PISTON_AIR = math.pi * (R_PIST / 1e3) ** 2 + 2 * math.pi * (R_PIST / 1e3) * (H_PIST / 1e3)
EXPANSION = 0.09                      # water → ice

# ---- program ------------------------------------------------------------------------------------------
T0 = p.T_WARM                         # start: everything at +10 °C
PROGRAM = [(0.0, p.T_COLD), (p.C_CYCLE_H[0], p.T_WARM)]   # (from hour, set-point)
T_END_H = sum(p.C_CYCLE_H)
TAU_AIR_H = 0.5                       # freezer air follows the set-point with τ ≈ 30 min
DT = 0.8                              # s (explicit limit ≈ 1.0 s)
FRAME_MIN = 15


def air_temp(t_h):
    T = T0
    for k, (h0, ts) in enumerate(PROGRAM):
        if t_h < h0:
            break
        h1 = PROGRAM[k + 1][0] if k + 1 < len(PROGRAM) else 1e9
        Tstart = T
        T = ts + (Tstart - ts) * math.exp(-(min(t_h, h1) - h0) / TAU_AIR_H)
    return T


def build():
    rc = (np.arange(NR) + 0.5) * DR
    zc = (np.arange(NZ) + 0.5) * DZ
    R, Z = np.meshgrid(rc, zc, indexing="ij")
    mat = np.full((NR, NZ), "air", dtype=object)
    mat[(R < R_SAND) & (Z < Z_BOT)] = "petg"
    mat[(R < R_SAND) & (Z > Z_BOT) & (Z < Z_SAND)] = "sand"
    mat[(R > R_SAND) & (R < R_WALL) & (Z < Z_TOP)] = "petg"
    mat[(R > R_WALL) & (Z < Z_JACKET)] = "jacket"
    mat[(R < R_PIST) & (Z > Z_SAND) & (Z < Z_SAND + H_PIST)] = "piston"
    return rc, zc, mat


def run():
    rc, zc, mat = build()
    m = 1e-3
    ri = np.arange(NR) * DR * m                      # inner face radius
    ro = (np.arange(NR) + 1) * DR * m
    vol = np.pi * (ro ** 2 - ri ** 2) * DZ * m       # per cell (depends on i only)
    a_ax = np.pi * (ro ** 2 - ri ** 2)               # axial face area
    solid = np.isin(mat, ["sand", "petg", "jacket"])
    idx = -np.ones((NR, NZ), int)
    idx[solid] = np.arange(solid.sum())
    n = solid.sum()
    is_sand = (mat[solid] == "sand")
    V = np.repeat(vol[:, None], NZ, 1)[solid]
    kfix = np.array([PROPS.get(mm, (0, 0))[0] for mm in mat[solid]])
    cfix = np.array([PROPS.get(mm, (0, 1))[1] for mm in mat[solid]])

    # links: (a, b, area, da, db) between solid cells; boundary: (a, kind, area, da, h)
    la, lb, lA, lda, ldb = [], [], [], [], []
    ba, bkind, bA, bda, bh = [], [], [], [], []      # bkind 0 = air, 1 = piston

    def bnd(a, kind, A, d, h):
        ba.append(a); bkind.append(kind); bA.append(A); bda.append(d); bh.append(h)

    for i in range(NR):
        for j in range(NZ):
            if not solid[i, j]:
                continue
            a = idx[i, j]
            # radial neighbour (outer face)
            A_r = 2 * np.pi * ro[i] * DZ * m
            if i + 1 < NR:
                if solid[i + 1, j]:
                    la.append(a); lb.append(idx[i + 1, j]); lA.append(A_r); lda.append(DR / 2 * m); ldb.append(DR / 2 * m)
                else:
                    bnd(a, 0, A_r, DR / 2 * m, H_CAV if rc[i] < R_SAND else (H_SIDE if zc[j] < Z_JACKET else H_OUT))
            else:
                bnd(a, 0, A_r, DR / 2 * m, H_SIDE if zc[j] < Z_JACKET else H_OUT)
            if i > 0 and not solid[i - 1, j]:      # inner face towards air (cavity wall above the sand)
                bnd(a, 0, 2 * np.pi * ri[i] * DZ * m, DR / 2 * m, H_CAV)
            # axial
            for dj in (1, -1):
                jj = j + dj
                if jj < 0:
                    bnd(a, 0, a_ax[i], DZ / 2 * m, H_UNDER)
                elif jj >= NZ:
                    bnd(a, 0, a_ax[i], DZ / 2 * m, H_OUT)
                elif solid[i, jj]:
                    if dj == 1:
                        la.append(a); lb.append(idx[i, jj]); lA.append(a_ax[i]); lda.append(DZ / 2 * m); ldb.append(DZ / 2 * m)
                elif mat[i, jj] == "piston":
                    bnd(a, 1, a_ax[i], DZ / 2 * m, H_CONTACT)
                else:
                    h = H_OUT if (mat[i, j] == "sand" or rc[i] > R_WALL or zc[j] > Z_TOP - DZ) else H_CAV
                    if mat[i, j] == "jacket":
                        h = H_SIDE
                    bnd(a, 0, a_ax[i], DZ / 2 * m, h)
    la, lb = np.array(la), np.array(lb)
    lA, lda, ldb = map(np.array, (lA, lda, ldb))
    ba, bkind = np.array(ba), np.array(bkind)
    bA, bda, bh = map(np.array, (bA, bda, bh))
    b_air, b_pis = bkind == 0, bkind == 1

    ku, cu = PROPS["sand_u"]
    kf, cf = PROPS["sand_f"]
    Hm = cf * (T_L - T_S) + L_VOL                    # enthalpy at T_L (H = 0 at T_S)

    def h_of_T(T):
        H = cfix * T
        Ts = T[is_sand]
        Hs = np.where(Ts < T_S, cf * (Ts - T_S),
                      np.where(Ts < T_L, (cf + L_VOL / (T_L - T_S)) * (Ts - T_S), Hm + cu * (Ts - T_L)))
        H[is_sand] = Hs
        return H

    def T_of_h(H):
        T = H / cfix
        Hs = H[is_sand]
        T[is_sand] = np.where(Hs < 0, T_S + Hs / cf,
                              np.where(Hs < Hm, T_S + Hs / (cf + L_VOL / (T_L - T_S)), T_L + (Hs - Hm) / cu))
        return T

    def ice(H):
        Hs = H[is_sand]
        return np.clip(1 - Hs / Hm, 0, 1)            # 1 = all pore water frozen

    T = np.full(n, T0)
    H = h_of_T(T) * V
    Tp = T0
    k = kfix.copy()
    steps = int(T_END_H * 3600 / DT)
    every = int(FRAME_MIN * 60 / DT)
    sand_ij = np.argwhere(mat == "sand")
    frames = []
    # rig parts as lumped first-order elements in still air (τ = ρ c V / (h A))
    tau = dict(col=2.6 * 900 / (H_OUT * 0.24), rod=7850 * 490 * 0.012 / (4 * H_OUT),
               inv=8100 * 515 * p.C_INVAR_D / 1e3 / (4 * H_OUT))
    Tr = dict(col=T0, rod=T0, inv=T0)
    sel = lambda name: (mat[solid] == name)
    wall = np.zeros(n, bool); wall[idx[int(R_SAND / DR), :NZ][idx[int(R_SAND / DR), :NZ] >= 0]] = True
    bot = np.zeros(n, bool)
    for i in range(int(R_SAND / DR)):
        for j in range(int(Z_BOT / DZ)):
            bot[idx[i, j]] = True
    Vs = V[is_sand]
    ins = p.C_INS_T if INSULATED else 0.0
    z_beam = ins + Z_BOT + 100 + p.C_BEAM_GAP                     # above the base plate
    z_c = z_beam + p.AF_BEAM_H + p.C_TRAVEL + 10                    # carrier underside
    L_rod = z_c - (ins + Z_SAND + H_PIST + 6)
    L_inv = z_c - 35                                                # Invar post: base plate → LVDT clamp
    drift = []
    for s in range(steps + 1):
        t_h = s * DT / 3600
        Ta = air_temp(t_h)
        Hv = H / V
        T = T_of_h(Hv)
        f = ice(Hv)
        k[is_sand] = ku * (1 - f) + kf * f
        for kk in Tr:
            Tr[kk] += (Ta - Tr[kk]) * DT / tau[kk]
        if s % every == 0:
            dTb = T[bot].mean() - T0
            dTw = T[wall].mean() - T0
            dTs = (T[is_sand] * Vs).sum() / Vs.sum() - T0
            pads = p.ALPHA_G10_Z * ins * ((Ta + T[bot].mean()) / 2 - T0)
            surf = pads + p.ALPHA_PETG * Z_BOT * dTb + p.ALPHA_SAND * 100 * dTs        # sand surface (mm)
            piston = surf + p.ALPHA_AL * H_PIST * (Tp - T0)
            carrier_a = piston + p.ALPHA_STEEL * L_rod * (Tr["rod"] - T0)                   # rev. A: steel rod
            carrier_b = piston + (p.ALPHA_INVAR if p.C_ROD_INVAR else p.ALPHA_STEEL) * L_rod * (Tr["rod"] - T0)
            drift.append([round(1000 * (carrier_a - p.ALPHA_AL * z_beam * (Tr["col"] - T0)), 1),      # rev. A: LVDT on Al beam
                          round(1000 * (carrier_b - p.ALPHA_INVAR * L_inv * (Tr["inv"] - T0)), 1),    # rev. B: Invar post + rod
                          round(1000 * (surf - pads - p.ALPHA_PETG * Z_TOP * dTw), 1),                 # camera vs rim
                          round(1000 * (surf - p.ALPHA_INVAR * (ins + Z_TOP) * (Tr["inv"] - T0)), 1)])  # camera vs Invar
            grid = np.full((NR, NZ), -128, np.int8)
            grid[solid] = np.clip(np.round(T * 10), -127, 127).astype(np.int8)
            pg = np.where(mat == "piston", np.int8(np.clip(round(Tp * 10), -127, 127)), grid)
            fz = np.zeros((NR, NZ)); fz[sand_ij[:, 0], sand_ij[:, 1]] = f
            heave = (fz * THETA * EXPANSION * DZ).sum(1)[: int(R_SAND / DR)] * 1000      # µm per ring
            frames.append(dict(t=round(t_h, 2), air=round(Ta, 2), piston=round(Tp, 2),
                               grid=pg.T.tobytes(), heave=[int(round(x)) for x in heave],
                               frozen=round(float((fz * vol[:, None] / vol[:20].sum()).sum() / (100 / DZ)), 4)))
        G = lA / (lda / k[la] + ldb / k[lb])
        q = G * (T[lb] - T[la])
        dH = np.bincount(la, q, n) - np.bincount(lb, q, n)
        Gb = bA / (bda / k[ba] + 1 / bh)
        Tb = np.where(b_air, Ta, Tp)
        qb = Gb * (Tb - T[ba])
        dH += np.bincount(ba, qb, n)
        Qp = -qb[b_pis].sum() + H_OUT * A_PISTON_AIR * (Ta - Tp)
        H = H + dH * DT
        Tp += Qp * DT / C_PISTON
    return rc, zc, mat, frames, drift


def pack(rc, zc, mat, frames, drift):
    import base64
    raw = b"".join(fr["grid"] for fr in frames)
    return dict(
        nr=NR, nz=NZ, dr=DR, dz=DZ,
        geom=dict(r_sand=R_SAND, r_wall=R_WALL, r_body=p.BODY_D / 2, r_collar=p.COLLAR_OD / 2,
                  z_bot=Z_BOT, z_sand=Z_SAND, z_jacket=Z_JACKET, z_top=Z_TOP, r_piston=R_PIST, h_piston=H_PIST,
                  base=list(p.C_BASE), col_span=p.C_COL_SPAN, beam_gap=p.C_BEAM_GAP, beam_h=p.AF_BEAM_H,
                  ins=p.C_INS_T if INSULATED else 0, sleeve=p.C_SLEEVE_T if INSULATED else 0,
                  pad=[p.C_PAD_D, p.C_PAD_R], invar=[p.C_INVAR_D, *p.C_INVAR_XY], lvdt=list(p.C_LVDT_XY),
                  ref=list(p.C_REF_XY), laser_ang=p.C_LASER_ANG,
                  rod_d=p.C_ROD_D, carrier=[p.C_CARRIER_D, p.C_CARRIER_T], disc_d=p.C_DISC_D,
                  cam=[p.C_CAM_Y, p.C_CAM_H, p.C_CAM_TILT], laser=[p.C_LASER_Y, p.C_LASER_H],
                  lines=[p.C_LINES, p.C_LINE_PITCH], pt100=[p.C_PT100_R, p.C_PT100_ANG], lvdt_x=p.C_LVDT_X,
                  port=[p.PORT_Z0, p.PORT_Z1, p.PORT_W, p.PORT_ANG], tdr_depths=[36, 45, 54]),
        props=dict(theta=THETA, k_u=PROPS["sand_u"][0], k_f=PROPS["sand_f"][0], h_out=H_OUT, h_cav=H_CAV,
                   h_bot=round(H_UNDER, 2), h_side=round(H_SIDE, 2), h_contact=H_CONTACT, latent=L_VOL,
                   porosity=POROSITY, insulated=INSULATED),
        program=dict(freeze_h=PROGRAM[0][0], thaw_h=PROGRAM[1][0], end_h=T_END_H, cold=p.T_COLD, warm=p.T_WARM),
        t=[fr["t"] for fr in frames], air=[fr["air"] for fr in frames], piston=[fr["piston"] for fr in frames],
        heave=[fr["heave"] for fr in frames], frozen=[fr["frozen"] for fr in frames], drift=drift,
        T=base64.b64encode(raw).decode("ascii"),
    )


def freeze_pattern(data):
    """Where the last unfrozen sand sits when the sample is 95 % frozen: (r, height above the sand bottom) mm."""
    import base64
    nf = len(data["t"])
    T = np.frombuffer(base64.b64decode(data["T"]), np.int8).reshape(nf, NZ, NR)
    k = next(i for i, x in enumerate(data["frozen"]) if x > 0.95)
    j0, j1, ns = int(Z_BOT / DZ), int(Z_SAND / DZ), int(R_SAND / DR)
    g = T[k, j0:j1, :ns].astype(float)
    j, i = np.unravel_index(np.argmax(g), g.shape)
    return data["t"][k], (i + 0.5) * DR, (j + 0.5) * DZ


if __name__ == "__main__":
    rc, zc, mat, frames, drift = run()
    data = pack(rc, zc, mat, frames, drift)
    tk, r_last, z_last = freeze_pattern(data)
    dr_ = np.array(drift)
    print(f"{'rev. B insulated' if INSULATED else 'bare cell'}: h_side {H_SIDE:.2f}, h_under {H_UNDER:.2f} W/m2K; "
          f"95 % frozen at {tk} h, last unfrozen at r {r_last:.0f}, {z_last:.0f} mm above the sand bottom")
    print("drift range µm (LVDT Al, LVDT Invar, cam rim, cam Invar):",
          [f"{dr_[:, c].min():.0f}…{dr_[:, c].max():.0f}" for c in range(4)])
    if not INSULATED:
        fz, t = data["frozen"], data["t"]
        print("fully frozen", next((t[i] for i, x in enumerate(fz) if x > 0.99), None), "h; thawed",
              next((t[i] for i, x in enumerate(fz) if t[i] > PROGRAM[1][0] and x < 0.01), None), "h")
        sys.exit()
    os.makedirs(WEB, exist_ok=True)
    with open(os.path.join(WEB, "thaw_data.json"), "w") as f:
        json.dump(data, f, separators=(",", ":"))
    tpl = os.path.join(WEB, "thaw_3d_template.html")
    if os.path.exists(tpl):
        html = open(tpl, encoding="utf-8").read().replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
        open(os.path.join(WEB, "E7_thaw_3d.html"), "w", encoding="utf-8").write(html)
    # short summary
    fz = data["frozen"]
    t = data["t"]
    full = next((t[i] for i, x in enumerate(fz) if x > 0.99), None)
    thaw = next((t[i] for i, x in enumerate(fz) if t[i] > PROGRAM[1][0] and x < 0.01), None)
    print(f"frames {len(t)}, fully frozen at {full} h, fully thawed at {thaw} h, max heave "
          f"{max(max(h) for h in data['heave'])} µm")
