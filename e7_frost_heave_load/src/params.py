"""E7 – zatěžovací testy při mrznutí a tání. Rozměry v mm, síly v N, napětí v kPa / MPa.

Výkresy (vykresy.py) i výpočty (vypocty.py) čtou rozměry odsud.
"""

# --- vzorek a tištěná cela (PETG-CF) ------------------------------------------
D_SAMPLE = 100.0        # vnitřní průměr vzorku
H_SAMPLE = 100.0        # výška vzorku
LINER = 0.5             # PTFE fólie na vnitřní stěně (proti tření)
D_CELL_IN = D_SAMPLE + 2 * LINER    # 101 – tištěný vnitřní průměr
WALL = 8.0              # stěna cely
D_CELL_OUT = D_CELL_IN + 2 * WALL   # 117
CELL_FOOT_D, CELL_FOOT_T = 150.0, 8.0   # patka cely (opírá se, není přišroubovaná)
POROUS_T = 10.0         # porézní kámen / sintr ⌀99,5 nahoře i dole
PISTON_H = 25.0         # Al píst (s porézním kamenem) – vodí se v cele
HEAVE_ALLOW = 15.0      # volný zdvih pístu
# cela: od spodního líce porézního kamene (z = −POROUS_T) po horní okraj
Z_CELL_BOTTOM = -POROUS_T - 2.0
Z_CELL_TOP = H_SAMPLE + PISTON_H + 5.0
L_CELL = Z_CELL_TOP - Z_CELL_BOTTOM

# --- rám z Al profilů (typ 8, drážka 8) ----------------------------------------
# katalogové hodnoty ≈ (ověřit v katalogu konkrétního výrobce)
PROFILES = {
    "40x40":  dict(A=600.0,  I=7.0e4),     # mm², mm⁴ (ohyb)
    "40x80":  dict(A=1050.0, I=4.5e5),     # ohyb kolem silné osy
    "80x80":  dict(A=2000.0, I=1.4e6),
}
E_AL = 70_000.0         # MPa
ALPHA_AL = 23.1e-6      # 1/K
ALPHA_STEEL = 11.5e-6
ALPHA_INVAR = 1.2e-6
BASE_T = 25.0           # základová deska Al 6082, 260 × 200
BASE_W, BASE_D = 260.0, 200.0   # dvě sestavy vedle sebe na vaně ≈ 530 × 340
COL_PROFILE = "40x80"   # 2 sloupy
COL_SPAN = 220.0        # osová vzdálenost sloupů
FRAME_H = 330.0         # výška sloupů (snížená, aby se páka vešla pod víko mrazáku)
BEAM_PROFILE = "80x80"  # příčník
PEDESTAL_H = 30.0       # Al podstavec pod celou (varianta B: na spodním siloměru)

# --- zatížení -------------------------------------------------------------------
SURCHARGES_KPA = (25, 50, 100, 200)   # varianta A – konstantní zatížení
LEVER_RATIO = 10.0                    # páka 1 : 10 se závažím
LEVER_L = 300.0                       # délka páky od čepu po závěs (čep 30 mm od táhla)
B_MAX_KPA = 2000.0                    # varianta B – návrhový max. tlak (literatura: silty 0,2–2 MPa)
SEATING_KPA = 5.0                     # varianta B – dosedací předpětí

# --- teploty --------------------------------------------------------------------
T_COLD, T_WARM = -10.0, 10.0          # program regulátoru (Set A)
STEP_H = 192.0                        # délka kroku programu

# --- PETG-CF (odhad z katalogových listů, ověřit literaturou a zkouškou) ---------
PETGCF = dict(
    sigma_xy=(40.0, 55.0),   # MPa, tah v rovině vrstvy (obvodový směr cely)
    sigma_z=(15.0, 30.0),    # MPa, tah kolmo na vrstvy (osový směr)
    E=(3000.0, 6000.0),      # MPa
    alpha=(30e-6, 60e-6),    # 1/K
    water=(0.1, 0.3),        # % hm., nasákavost samotného materiálu
)
LONG_TERM_FACTOR = 0.3       # dovolené dlouhodobé napětí ≈ 30 % pevnosti (creep, vrstvy)

# --- zemina (pro odhad) -----------------------------------------------------------
E_FROZEN = 200.0             # MPa, modul zmrzlé zeminy (hrubý odhad)
THETA = 0.30

# --- mrazák (stejný jako E6, ≈ odhad z fotek – ZMĚŘIT) ---------------------------
FRZ_L, FRZ_W, FRZ_H = 900.0, 550.0, 650.0
TRAY_L, TRAY_W = 530.0, 340.0
INS = 25.0              # izolace kolem cely

# --- varianta A: nenasycený písek, tlaky uvnitř vzorku -----------------------------
SAND = dict(name="unsaturated sand", d50=0.3, Sr=(0.3, 0.5), theta=(0.10, 0.18))
SURCHARGE_A_KPA = 50.0       # výchozí přitížení (rozsah 25–200)
# vložené tlakové buňky: (tag, měří, hloubka pod povrchem [mm], r [mm], úhel [°])
#   "v" = leží vodorovně → svislé napětí; "h" = stojí svisle, čelem k ose → radiální napětí
PCELLS = [("PV1", "v", 40.0, 0.0, 0.0),
          ("PV2", "v", 80.0, 22.0, 210.0),
          ("PH1", "h", 62.0, 25.0, 30.0)]
PCELL_D, PCELL_T = 20.0, 5.0     # obalové rozměry miniaturní buňky (upřesní rešerše)
# tlakové snímače ve stěně (lícují s vnitřním povrchem): (tag, hloubka, úhel)
PWALL = [("PW1", 20.0, 30.0), ("PW2", 42.0, 150.0), ("PW3", 64.0, 270.0)]
PWALL_D = 8.0
