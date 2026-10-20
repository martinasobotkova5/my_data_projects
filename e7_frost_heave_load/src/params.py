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
FRAME_H = 330.0         # (původní tuhý rám B – už se nepoužívá, B je bez zatížení)
BEAM_PROFILE = "80x80"  # příčník
PEDESTAL_H = 30.0       # Al podstavec pod celou

# --- zatížení -------------------------------------------------------------------
SURCHARGES_KPA = (5, 10, 15, 20, 25)   # varianta A – přitížení závažím (max. 25 kPa)

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
SURCHARGE_A_KPA = 25.0       # výchozí = maximální přitížení závažím
# vložené tlakové buňky: (tag, měří, hloubka pod povrchem [mm], r [mm], úhel [°])
#   "v" = leží vodorovně → svislé napětí; "h" = stojí svisle, čelem k ose → radiální napětí
PCELLS = [("PV1", "v", 40.0, 0.0, 0.0),        # na ose, svislé napětí
          ("PH1", "h", 62.0, 25.0, 30.0)]       # radiální napětí (volitelné – další inkluze)
# TML PDA-PA (⌀6,5 × 1 mm) vlepený do nerezového nosného disku ⌀20 × 2 → D/t = 10, D/d50 ≈ 65
PCELL_D, PCELL_T = 20.0, 2.0
# snímač v patce: PDA-PA zapuštěný lícem s horní plochou porézního kamene (svislé napětí u dna)
PBASE = [("PB1", 25.0, 120.0)]               # (tag, r, úhel)
# tlakové snímače ve stěně (lícují s vnitřním povrchem kroužku): (tag, hloubka, úhel)
PWALL = [("PW1", 20.0, 30.0), ("PW2", 42.0, 150.0), ("PW3", 64.0, 270.0)]
PWALL_D = 8.0                                # PDA-PA v pouzdře ⌀8 (vejde se do kroužku 10 mm)

# --- varianta A: přitížení závažím (zatěžovací deska + ocelové kotouče) -------------
FRAME_H_A = 410.0            # lehký rám 40×40 – nese jen vedení závaží a nic nezatěžuje
BEAM_H_A = 40.0              # příčka 40×40 s lineárním ložiskem pro vodicí tyč
RHO_STEEL = 7850.0
DW_D, DW_HOLE = 150.0, 18.0  # ocelové kotouče ⌀150 se středovým otvorem
DW_FULL_T, DW_HALF_T = 36.0, 18.0   # ≈ 4,9 kg a ≈ 2,5 kg
DW_CARRIER_T = 10.0          # nosná deska ⌀150 × 10 s pevnou vodicí tyčí
DW_ROD_D, DW_ROD_L = 16.0, 230.0
DW_G10_D, DW_G10_T = 60.0, 10.0     # tepelný mezikus pod nosnou deskou
PISTON_ASSY_KG = 1.0         # píst + porézní kámen + terčík + kulička (≈, zvážit)
LVDT_R = 95.0                # LVDT na bocích (±y), terčík má výstupky do r 100

# --- varianta B: stejný vzorek bez zatížení, posuny a deformace po vrstvách ------------
TOP_PLATE_D, TOP_PLATE_T = 99.0, 6.0      # lehká horní deska PETG-CF (≈ 60 g ≈ 0,1 kPa), jen terč pro LVDT
TOP_PLATE_KG = 0.065
# povrchové LVDT na horní desce: (tag, r, úhel) → průměrný zdvih + náklon
SURF_LVDT = [("S1", 40.0, 30.0), ("S2", 40.0, 150.0), ("S3", 40.0, 270.0)]
# kotvy (settlement anchors) uvnitř písku: (tag, hloubka pod povrchem, r, úhel)
ANCHORS = [("E1", 25.0, 25.0, 90.0), ("E2", 50.0, 25.0, 210.0), ("E3", 75.0, 25.0, 330.0)]
ANCHOR_D, ANCHOR_T = 16.0, 1.5            # nerezový kotouček
ROD_D, SLEEVE_D = 2.0, 4.0                # Invarová tyčka ⌀2 v PTFE trubičce ⌀4/2,5 (sleeve)
PLATE_HOLE_D = 7.0                        # otvor v horní desce pro trubičku (deska se po ní volně posouvá)
# referenční stojan: 3 Invarové sloupky ze základové desky + Al můstek s LVDT
STAND_R, STAND_POST_D = 100.0, 12.0
STAND_ANG = (60.0, 180.0, 300.0)
BRIDGE_D, BRIDGE_T = 220.0, 10.0
Z_BRIDGE = 250.0                          # spodní líc můstku nad základovou deskou
LVDT_B_BODY = (19.0, 90.0)                # ⌀ × délka těla (≈, RDP DCTH200 s volným jádrem – ověřit)
LVDT_B_RANGE = 5.0                        # ±mm
ALPHA_G10 = 15e-6
