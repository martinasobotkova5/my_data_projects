"""Společné parametry experimentu E6 (rozměry v mm, teploty v °C).

Výkresy (vykresy.py) i výpočty (vypocty.py) čtou rozměry odsud, takže
změna jednoho čísla se propíše do všech výkresů a bilancí.
"""

# --- kolona -------------------------------------------------------------
D_COL = 100.0          # vnitřní průměr kolony (= průměr vzorku)
WALL = 5.0             # tloušťka stěny trubky PMMA
H_SOIL = 100.0         # výška vzorku zeminy
H_FREE = 25.0          # volná výška nad zeminou (písek, límec, rezerva na zdvih)
L_TUBE = H_SOIL + H_FREE
D_OUT = D_COL + 2 * WALL

# --- minidisk (otevřená konstrukce, spékaný disk jako u Mini Disk) -------
D_DISK = 45.0          # průměr spékaného disku
T_DISK = 3.0           # tloušťka disku
D_RES = 31.0           # vnitřní průměr zásobníku hlavy
H0_CM = -2.0           # tlaková výška na disku [cm]
T_SAND = 2.0           # kontaktní písek 0,1–0,3 mm

# --- spodní okrajová podmínka: kónický odtok se sací membránou -----------
# plný hliníkový kužel (zvenku nálevka 45°), na horním líci membrána,
# drážky svedené do osového vývrtu → tryska na hrotu → odkap / přepad
CONE_RIM_R = 70.0      # poloměr horní příruby kužele
CONE_RIM_T = 8.0       # tloušťka příruby
CONE_R_TOP = 55.0      # poloměr kužele pod přírubou
CONE_R_TIP = 9.0       # poloměr hrotu
CONE_H = 46.0          # výška kuželové části (45°)
NOZZLE_L = 12.0        # tryska ⌀6 (vnější) na hrotu
BORE_D = 1.5           # osový vývrt
T_SUPPORT = 2.0        # perforovaná nerezová podložka
T_MEMBR = 0.15         # nylonová membrána 20 µm
N_GROOVE = 12          # radiální drážky 1 × 1 mm
GROOVE = 1.0
RING_R = (15.0, 30.0, 45.0)   # obvodové drážky 1 × 1 mm
HB_CM = (0.0, -30.0)   # rozsah nastavitelné sací výšky odkapu [cm]
D_SPLIT = 50.0         # varianta B: dělená sací deska, vnitřní zóna

# --- izolace a chlazení -------------------------------------------------
INS = 30.0             # boční izolace (Kaiflex / Armaflex)
INS_TOP = 20.0         # víko izolace přes mezikruží

# --- čidla (hloubka pod původním povrchem [mm], úhel [°]) -----------------
# termistory ve stěně: hrot na r = TH_R, šroubovice po 60°
THERMISTORS = [(10, 0), (20, 60), (35, 120), (50, 180), (70, 240), (90, 300)]
TH_R = 9.0             # radiální poloha hrotu termistoru
# další termistory: 2 jehly v plovoucím prstenci (2 a 6 mm pod povrchem),
# rozhraní disk/písek, sací deska, voda v Mariottově láhvi, vzduch, ref. cela
RAFT_TH = [(2, 135, 36.0), (6, 315, 36.0)]   # (hloubka, úhel, poloměr)
# TDR: (název, hloubka, vzdálenost tětivy od osy y, délka tyčí, izolovaný úsek)
TDR = [("TDR-C27", 27, 0.0, 75, 25),
       ("TDR-A27", 27, 36.0, 50, 0),
       ("TDR-C60", 60, 0.0, 75, 25)]
TDR_PITCH = 6.0        # rozteč tří tyčí (C: vodorovně vedle sebe, A: nad sebou)
HFP = [(45, 36.0), (225, 36.0)]   # desky tepelného toku: (úhel, poloměr), 10 × 10 mm
HFP_SIZE = 10.0
LVDT = [("LVDT-0", 0, 0.0), ("LVDT-1", 90, 38.0), ("LVDT-2", 270, 38.0)]

# --- materiálové a provozní předpoklady pro bilance ------------------------
POROSITY = 0.45
THETA_TOT = 0.30       # celkový obsah vody (kapalná + led) před zmrazením
THETA_UNFROZEN = 0.05  # nezamrzlá voda při −10 °C (prachovitá hlína, odhad)
T_INIT = -10.0         # teplota zmrazení v mrazáku (potvrzeno)
C_FROZEN = 1.9e6       # objemová tepelná kapacita zmrzlé zeminy [J m-3 K-1]
L_F = 334e3            # skupenské teplo tání [J kg-1]
RHO_W = 1000.0
Q_DISK_MM_H = (2.0, 5.0)  # rychlost infiltrace vztažená na plochu disku
FRACTION_ML = (2.0, 5.0)

# --- skutečná sestava podle fotek (≈ odhad z fotek, ZMĚŘIT) ----------------
FRZ_L, FRZ_W, FRZ_H = 900.0, 550.0, 650.0   # vnitřek truhlicového mrazáku
FROST = 15.0                                 # námraza na stěnách (fotka 1)
MAT_T = 20.0                                 # černá izolační podložka pod vanou
TRAY_L, TRAY_W, TRAY_H = 530.0, 340.0, 40.0  # nerezová vana
HOLDER_WALL = 4.0                            # tištěný držák PETG, ⌀100 vnitřní
HOLDER_FLANGE_D, HOLDER_FLANGE_T = 160.0, 10.0
AL_D, AL_T = 112.0, 20.0                     # Al deska na povrchu vzorku
AL_HOLE_NOW, AL_RECESS_NOW = 26.0, 60.0      # současný otvor / vybrání (fotka 5)
AL_HOLE_NEW = 64.0                           # návrh: otvor pro tělo AMDI (ověřit ⌀ těla)
AMDI_BODY_D = 60.0                           # ≈ vnější ⌀ těla AMDI (ověřit)
STAND_H = 150.0                              # stojan pod kuželem (výška nožek)
