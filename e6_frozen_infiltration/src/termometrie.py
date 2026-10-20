"""Thermometry for E6: channel list, NTC half-bridge sizing, uncertainty budget,
and how fast the frozen column warms once it is out of the freezer.

Imported by vypocty.py (tables in Czech) and vykresy.py (sheets E6-V08, V09).
"""
import math

import params as p

# --- NTC thermistor (10 kΩ at 25 °C, glass bead) ---------------------------
R25 = 10_000.0
BETA = 3977.0                # typical 10k NTC; real coefficients come from calibration
R_REF = 30_000.0             # half-bridge reference ≈ R_T at −3 … 0 °C, 0.01 %, ≤ 2 ppm/K
V_EX = 0.5                   # excitation, switched on only for the measurement (≈ 50 ms)
DISSIPATION = 1.5e-3         # W/K, sheathed probe in moist soil (conservative)
T_RANGE = (-8.0, 25.0)


def r_ntc(t_c):
    t = t_c + 273.15
    return R25 * math.exp(BETA * (1 / t - 1 / 298.15))


def half_bridge(t_c):
    """Ratio X = V/Vx measured across the thermistor, sensitivity dX/dT, self-heating."""
    rt = r_ntc(t_c)
    x = rt / (rt + R_REF)
    drt = -BETA / (t_c + 273.15) ** 2 * rt          # dR/dT
    dx = R_REF / (rt + R_REF) ** 2 * drt
    i = V_EX / (rt + R_REF)
    p_w = i ** 2 * rt
    return rt, x, dx, p_w, p_w / DISSIPATION


# --- channel list -------------------------------------------------------------
# (ID, location, inside/outside, purpose)
CHANNELS = (
    [(f"T{d}", f"soil, wall probe, depth {d} mm, r 9", "in", "soil profile") for d, _ in p.THERMISTORS]
    + [(f"T{d}r", f"soil, ring needle, {d} mm below surface", "in", "near-surface, annulus") for d, _, _ in p.RAFT_TH]
    + [("Tdisc", "disc / contact sand", "in", "freezing at the disc"),
       ("Tcone", "cone body under membrane", "in", "bottom boundary"),
       ("Tsup", "Mariotte bottle water", "in", "inflow temperature"),
       ("Tout", "outflow at nozzle", "in", "outflow temperature"),
       ("A1", "freezer air, floor level, shielded", "in", "air stratification"),
       ("A2", "freezer air, column mid-height", "in", "air BC of column"),
       ("A3", "freezer air, under lid", "in", "air stratification"),
       ("Tcell", "reference cell, 50 mL pure water", "in", "0 °C plateau check in situ"),
       ("L1", "lab air at freezer, shielded", "out", "external load"),
       ("Llog", "logger enclosure, at R_ref", "out", "R_ref temperature"),
       ("ICE", "ice-point Dewar (spare probe)", "out", "daily 0.000 °C check"),
       ("Rchk", "fixed 30 kΩ resistor (no NTC)", "out", "logger drift check")]
)

# --- uncertainty budget (standard uncertainties, mK) --------------------------
BUDGET = [
    ("reference thermometer (SPRT / Pt100, cert. U = 5 mK, k = 2)", 2.5),
    ("bath inhomogeneity and stability", 2.0),
    ("Steinhart–Hart fit residual", 1.0),
    ("R_ref drift / tempco (2 ppm/K × 15 K, same logger as in calibration)", 0.6),
    ("logger resolution and noise (24 bit, averaged)", 0.3),
    ("self-heating difference bath vs. soil", 1.0),
    ("sensor drift between calibrations (checked at ice point)", 2.0),
]


def combined():
    u = math.sqrt(sum(v ** 2 for _, v in BUDGET))
    return u, 2 * u


# --- warming of the column outside the freezer ---------------------------------
K_INS = 0.035                 # W m-1 K-1, Kaiflex / XPS / PU
H_INS_SIDE = p.L_TUBE / 1000


def ua_column():
    r1, r2 = (p.D_OUT / 2) / 1000, (p.D_OUT / 2 + p.INS) / 1000
    side = 2 * math.pi * K_INS * H_INS_SIDE / math.log(r2 / r1)
    top = K_INS / (p.INS_TOP / 1000) * math.pi * (p.D_COL / 2000) ** 2
    cone_area = math.pi * (p.CONE_R_TOP / 1000) * math.hypot(p.CONE_H, p.CONE_R_TOP - p.CONE_R_TIP) / 1000
    bottom = K_INS / 0.020 * cone_area
    return side + top + bottom


def warming(t_room=20.0):
    v = math.pi * (p.D_COL / 2000) ** 2 * p.H_SOIL / 1000
    ua = ua_column()
    cold = p.C_FROZEN * abs(p.T_INIT) * v                         # J
    q_cold = ua * (t_room - p.T_INIT / 2)                           # W, mean while warming
    ice = (p.THETA_TOT - p.THETA_UNFROZEN) * v * 917 * p.L_F         # J
    q_melt = ua * t_room
    return ua, cold / q_cold / 3600, ice / q_melt / 3600
