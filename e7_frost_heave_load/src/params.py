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
SURF_LVDT = [("S1", 40.0, 0.0), ("S2", 40.0, 120.0), ("S3", 40.0, 240.0)]     # mimo Pt100 (r 15, 0°) a kotvy
# kotvy (settlement anchors) uvnitř písku: (tag, hloubka pod povrchem, r, úhel)
ANCHORS = [("E1", 25.0, 25.0, 150.0), ("E2", 50.0, 25.0, 30.0), ("E3", 75.0, 25.0, 210.0)]   # ≥ 14 mm od TDR, vlákna a Pt100
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

# --- bod M: TDR + Pt100 + optické čidlo ve stejném místě (obě varianty) ----------------
# všechny tři vstupují vodorovně jedním nálitkem ve stěně, rovnoběžně s radiálou pod úhlem M_ANG
M_DEPTH, M_ANG = 54.0, 108.0            # hloubka pod povrchem, úhel (mezi termistory 72° a 144°)
TDR_RODS_DZ = (-5.0, 0.0, 5.0)          # 3 tyčky TDR nad sebou (svislá rovina), rozteč 5 mm
TDR_ROD_D, TDR_ROD_L = 1.6, 40.0        # nerez ⌀1,6, od stěny (r 50) po r 10
TDR_HEAD = (18.0, 16.0, 14.0)           # epoxidová hlava v nálitku: šířka × výška × hloubka
M_SIDE = 12.0                           # boční odsazení Pt100 (+) a optického čidla (−) od roviny TDR
PT100_D, PT100_TIP_R = 3.0, 20.0        # Pt100 1/10 DIN, plášť ⌀3, hrot na r 20 (element r 20–30)
FBG_D, FBG_TIP_R = 1.0, 20.0            # FBG v nerezové kapiláře ⌀1, mřížka 10 mm u hrotu (r 20–30)
M_BOSS = (34.0, 22.0, 10.0)             # nálitek na stěně: šířka × výška × přesah
T_TIP_R = 40.0                          # hroty termistorů T1–T5 (obě varianty), mimo bod M a kotvy

# --- varianta A-min: maximálně zjednodušená varianta A ----------------------------------
# bez rámu: závaží na závitové tyči přímo v pístu, cela vede píst; bez multiplexerů
AM_BASE = (230.0, 230.0, 10.0)          # Al deska (jen nese sloupek LVDT)
AM_G10_T = 0.0                          # G10 už není – tepelně izoluje tištěné dno 26 mm
AM_BOTTOM_T = 26.0                      # tištěné dno pod pískem (výkres: 160 − 134)
AM_PISTON_H = 40.0                      # plný Al píst ⌀99,5 se závitem M16
AM_ROD_L = 200.0                        # závitová tyč M16 – nosí kotouče
AM_TRIM_T = 9.0                         # čtvrtkotouč ⌀150 × 9 (≈ 1,2 kg) na doladění
AM_POST_D = 12.0                        # nerezový sloupek pro 1 LVDT
AM_TEMPS = [("T1", 20.0, 0.0), ("T2", 80.0, 180.0)]      # termistory v písku (tag, hloubka, úhel)
AM_PV = ("PV1", 75.0)                   # svislé napětí na ose (tag, hloubka) – pod TDR
AM_PB = ("PB1", 25.0, 288.0)            # na dně (tag, r, úhel)

# --- A-min: pevné (nehybné) omezení místo závaží --------------------------------------
# víko = ocelová deska přitažená 3 táhly k základové desce, píst dosednutý středovým šroubem
AM_TIE_R, AM_TIE_D = 92.0, 10.0          # táhla M10 nerez A4-70, r 92 (vně těla ⌀160)
AM_TIE_ANG = (45.0, 165.0, 285.0)        # mimo bod M (108°), termistory (0/180°) a PB1 (288° je pod dnem)
AM_LID_D, AM_LID_T = 240.0, 15.0         # ocelové víko ⌀230 × 15
AM_SCREW_D = 16.0                        # středový šroub M16 × 1,5 s pojistnou maticí
AM_LID_GAP = 15.0                        # mezera píst – víko (šroub)
AM_BASE_T2 = 20.0                        # základová deska Al tl. 20 (nese táhla)
AM_P_DESIGN_KPA = 1000.0                 # návrhový tlak z mrznutí při zamezeném zdvihu (horní mez)
AM_SEATING_KPA = 5.0                     # dosedací předpětí při dotažení

# --- A-rám: varianta A s nehybným omezením v rámu z Al profilů ---------------------------
AF_BASE = (260.0, 200.0, 25.0)          # Al deska 6082 (sloupy do ní šrouby do čela)
AF_COL_H = 245.0                         # 2 sloupy 40×80, osová vzdálenost COL_SPAN (220)
AF_BEAM_H = 80.0                         # příčník 80×80
AF_SPACER_D = 40.0                       # distanční sloupek mezi pístem a šroubem
AF_POM_T = 8.0                           # teplotně kompenzační vložka POM-C ⌀40 × 8
ALPHA_POM = 110e-6
ALPHA_SAND_FROZEN = 12e-6                # ≈, písek se zmrzlou vodou (ověřit slepou zkouškou)
AF_SCREW_PROTRUDE = 20.0                 # šroub M16 × 1,5 vyčnívá pod příčník

# --- cela A jako tištěný kelímek se dnem (PETG-CF, jeden kus) ---------------------------
CUP_ID, CUP_H = 100.0, 100.0            # vnitřní průměr a vnitřní výška = vzorek
CUP_WALL = 8.0                          # stěna
CUP_BOTTOM = 10.0                       # dno (zapuštěný PB1 ⌀8 × 1,5 + kanálek pro kabel)
CUP_OD = CUP_ID + 2 * CUP_WALL          # 116
CUP_R_IN = 1.0                          # vnitřní zaoblení dno–stěna (R1, aby písek dosedl)
ALPHA_PETG = 45e-6
AF_SPACER_L = AF_COL_H - (AM_G10_T + AM_BOTTOM_T + H_SAMPLE + AM_PISTON_H) - AF_SCREW_PROTRUDE - AF_POM_T   # Al sloupek

# --- tištěná cela A podle modelu "Column_one_body_version_1" (PrusaSlicer, MK4S) --------
# rozměry ≈ odhad ze screenshotu – POTVRDIT podle STL
CUP_WALL_IN = 3.0          # vnitřní stěna (perimetry) kolem vzorku ⌀100
JACKET_OD = 150.0          # vnější plášť ≈ ⌀150, mezi stěnami výplň 10 % = tepelná izolace
JACKET_WALL = 2.0          # vnější stěna pláště (perimetry)
JACKET_H = 90.0            # výška pláště od spodku dna (slicer ≈ 89,8 mm)
CUP_BOTTOM = 5.0           # dno (přepisuje dřívějších 10 mm)
COLLAR_OD = CUP_ID + 2 * CUP_WALL_IN   # horní límec (vnitřní trubka nad pláštěm) ⌀106
LEG_D, LEG_H, LEG_R = 10.0, 20.0, 65.0 # 4 nožičky
LEG_ANG = (0.0, 90.0, 180.0, 270.0)
PORT_W, PORT_H = 26.0, 14.0            # okénko + radiální kanál pláštěm (bod M)
AM_PORT_ANG = 270.0                    # kanál nad přední nožičkou
SUPPORT_D = 2 * (LEG_R - LEG_D / 2) - 2   # G10 podložka mezi nožičkami ⌀118 – nese dno

# --- cela A podle výkresu "Column_one_body_version_1_fillet" (M. Vrána, 23. 6. 2026) -----
BODY_D, BODY_H = 160.0, 130.0          # vnější tělo ⌀160 × 130 (výplň 10 % = izolace)
COLLAR_OD, COLLAR_TOP = 106.0, 160.0   # límec ⌀106 (stěna 3), horní hrana 160 nad spodkem
CAV_D = 100.0                          # vnitřní dutina ⌀100
BODY_BOTTOM = 26.0                     # dno pod pískem (160 − 134)
SAND_TOP = BODY_BOTTOM + 100.0         # 126 – písek 100 mm; nad ním 34–35 mm pro píst
CAV_FILLET = 5.0                       # zaoblení dna dutiny (na výkrese ⌀10)
PORT_W, PORT_Z0, PORT_Z1 = 13.0, 67.5, 94.5   # boční kanál: šířka 13, výška 67,5–94,5 nad spodkem
PORT_ANG = 270.0                       # kanál „dole“ na půdorysu
# bod M podle náčrtu
TDR_CS645 = dict(rod_d=3.2, rod_l=75.0, pitch=8.9, head_l=19.0)
# hlava CS645 vyplňuje kanál (z 67,5–94,5, horní hrana 65,5 pod límcem ≈ „66“ z náčrtu), tyčky symetricky ve středu kanálu
TDR_CS645["top_from_collar"] = COLLAR_TOP - ((PORT_Z0 + PORT_Z1) / 2 + TDR_CS645["pitch"])
OF_TIP_FROM_WALL = 37.5                # optické vlákno – vodorovně v úrovni horní tyčky, hrot 37,5 od stěny
OF_SIDE = 4.7                          # boční odsazení vlákna od roviny TDR (≈ z půdorysu)
PT100_L, PT100_METAL, PT100_R = 37.0, 25.0, 15.0   # Pt100 svisle shora, 37 mm (25 mm kov), 15 mm od osy
AM_PV_DEPTH = 75.0                     # PV1 přesunut pod TDR (tyčky TDR procházejí osou v hl. 32–50)

# --- varianta B v tištěné cele ⌀160 ----------------------------------------------------
B_BASE_T = 20.0                          # Al deska 260 × 200 × 20, cela stojí přímo na ní (izoluje tištěné dno)
B_PT100_HOLE = 6.0                       # otvor v horní desce pro svislé Pt100 (deska se po něm posouvá)

# --- varianta B-open: nejjednodušší sestava, povrch otevřený (bez víka a horní desky) -----
BO_BASE = (220.0, 220.0, 10.0)          # Al deska – nese jen cela a 1 sloupek
BO_TARGET_D, BO_TARGET_T = 30.0, 2.0    # terčík PETG ⌀30 × 2 (≈ 2 g) volně na povrchu písku
BO_TARGET_R, BO_TARGET_ANG = 20.0, 135.0   # mimo Pt100 (r 15, 0°) a osu TDR (270°)
BO_POST_D = 12.0                        # 1 Invarový sloupek ⌀12 v rohu desky
BO_POST_ANG = 135.0                     # sloupek v rohu desky směrem k terčíku
BO_ARM_Z = 75.0                         # rameno LVDT nad horní hranou límce

# --- B-open s kamerou (bez LVDT a Invarového sloupku) -------------------------------------
BC_BASE = (320.0, 220.0, 10.0)          # Al deska – cela + držák kamery
BC_MARK_ROD_D = 3.0                     # tyčka značky (PETG/uhlík) z terčíku nad límec
BC_MARK_ABOVE = 20.0                    # hlava značky nad horní hranou límce
BC_MARK_HEAD = (12.0, 8.0)              # šachovnicová značka 12 × 8 mm
BC_REF_MARKS = 2                        # 2 referenční značky na límci (vlevo/vpravo od tyčky)
BC_CAM_DIST = 150.0                     # vzdálenost objektiv – značka
BC_CAM_BOX = (90.0, 70.0, 80.0)         # vyhřívaný izolovaný box kamery (d × š × v)
BC_FOV = 40.0                           # šířka zorného pole na značce [mm]
BC_SENSOR_PX = 4056                     # Raspberry Pi HQ camera (IMX477)

# --- B-open: bezkontaktně – kamera shora + čárový laser (laserová triangulace) ------------
BL_CAM_H = 220.0                        # objektiv nad povrchem písku
BL_LENS_F = 12.0                        # objektiv 12 mm → zorné pole ≈ 115 mm (celý ⌀100 + límec)
BL_SENSOR_W = 6.29                      # IMX477, šířka čipu [mm]
BL_LASER_ANG = 45.0                     # čárový laser odkloněný od svislice
BL_LASER_X = 150.0                      # laser stranou od osy (ve výšce kamery)

# --- varianta C: kombinace A (Al rám) + B (kamera) – částečný píst, mrtvá váha pohyblivá -------
# rám jen VEDE zátěž (kuličkové pouzdro), píst se s povrchem volně zvedá i klesá → konstantní zatížení
C_PISTON_D, C_PISTON_H = 50.0, 20.0     # částečný píst (patka) ⌀50 – zakrývá 25 % plochy, zbytek volný
C_BALL_D = 8.0                          # ocelová kulička v kuželových sedlech (píst se může naklonit)
C_ROD_D = 12.0                          # vodicí tyč (kalená, h6) v kuličkovém pouzdře LM12UU
C_BUSH = (21.0, 30.0)                   # LM12UU: vnější ⌀ × délka
C_BEAM_GAP = 200.0                      # spodní líc příčníku nad povrchem písku (místo pro kameru + laser)
C_CARRIER_D, C_CARRIER_T = 120.0, 8.0   # nosná deska závaží nad příčníkem (Al)
C_DISC_D, C_DISC_HOLE = 120.0, 17.0     # ocelové kotouče ⌀120
C_DISC_KG = (1.0, 0.5)                  # kotouč 1 kg a 0,5 kg
C_TRAVEL = 25.0                         # volný zdvih / pokles zátěže
C_SURCHARGES_KPA = (5.0, 10.0, 15.0, 20.0, 25.0)   # pod pístem
C_CAM_Y, C_CAM_H, C_CAM_TILT = -75.0, 150.0, 27.0  # kamera stranou (−y, nad kanálem TDR), výška nad pískem, sklon k ose
C_LASER_Y, C_LASER_H = 95.0, 95.0       # laser z protější strany (+y, 45°), čára napříč (osa x) přes límec–písek–píst–písek–límec
C_PT100_R, C_PT100_ANG = 37.5, 315.0    # Pt100 svisle ve volném mezikruží na straně kamery (y < 0) – mimo laserovou čáru (y ≥ 0)

# --- varianta C – měření deformace jen 1 (kamera + laser) a 2 (LVDT na zátěži) --------------
C_LENS_F = 8.0                           # objektiv 8 mm → zorné pole ≈ 130 mm (celý límec ⌀106 + okraj)
C_LVDT_X = 45.0                          # LVDT na příčníku, hrot na spodní straně nosné desky
C_SNAP_MIN = (10, 1)                     # snímek / měření: běžně 10 min, při průchodu 0 °C 1 min
C_LINES, C_LINE_PITCH = 11, 9.0          # vícečárový laser (DOE): 11 rovnoběžných čar po 9 mm → celý povrch ⌀100
