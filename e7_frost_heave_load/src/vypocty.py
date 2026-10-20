"""Návrhové výpočty E7. Spuštění: python vypocty.py > ../vypocty.md"""
import math

import params as p

A = math.pi * (p.D_SAMPLE / 2) ** 2          # mm²


def row(*c):
    print("| " + " | ".join(str(x) for x in c) + " |")


def head(*c):
    row(*c)
    print("|" + "---|" * len(c))


print("# E7 – návrhové výpočty\n")
print("Generováno skriptem `src/vypocty.py` z `src/params.py`. Hodnoty ≈ jsou odhady k ověření.\n")

# 1 ---------------------------------------------------------------------------
print("## 1. Zatížení\n")
print(f"Plocha vzorku ⌀{p.D_SAMPLE:g}: {A:.0f} mm² = {A / 100:.2f} cm².\n")
head("varianta", "napětí na povrchu [kPa]", "síla [N]", "hmotnost na vzorku [kg]")
for s in p.SURCHARGES_KPA:
    f = s * A / 1000
    row("A – závaží", s, f"{f:.0f}", f"{f / 9.81:.1f}")
m_rods = sum(math.pi / 4 * (p.ROD_D / 1000) ** 2 * (p.H_SAMPLE + 80 - d) / 1000 * 8100
             + math.pi / 4 * (p.ANCHOR_D / 1000) ** 2 * p.ANCHOR_T / 1000 * 7900 for _, d, _, _ in p.ANCHORS)
sig_b = p.TOP_PLATE_KG * 9.81 / A * 1000
row("B – jen horní deska PETG-CF", f"{sig_b:.2f}", f"{p.TOP_PLATE_KG * 9.81:.2f}", f"{p.TOP_PLATE_KG:g}")
print(f"\nVe variantě B nese písek jen lehkou desku ({sig_b:.2f} kPa) – to odpovídá vlastní tíze "
      f"horních 5 mm písku (≈ {1700 * 9.81 * 0.005 / 1000:.2f} kPa). Kotvy s Invarovými tyčkami váží "
      f"dohromady {m_rods * 1000:.0f} g a visí každá na svém místě v písku. LVDT mají **volné jádro** "
      "(bez pružiny), takže na vzorek netlačí. Běžné LVDT s pružinou by přidaly ≈ 1–2 N na hrot, "
      "tj. 0,1–0,25 kPa na každý snímač.\n")

# 2 ---------------------------------------------------------------------------
print("## 2. Varianta B – očekávané deformace (uzavřený systém)\n")
head("θ [-]", "Sr [-]", "pórovitost n", "vzduch n(1−Sr)", "objem z mrznutí 0,09·θ", "horní mez zdvihu [mm]")
n = 0.38                     # pórovitost uloženého písku (≈)
for sr in (0.3, 0.4, 0.5):
    if True:
        th = n * sr
        row(f"{th:.2f}", f"{sr:.1f}", f"{n:.2f}", f"{n * (1 - sr):.2f}", f"{0.09 * th:.3f}",
            f"{0.09 * th * p.H_SAMPLE:.1f}")
print("\nHorní mez platí, jen kdyby se celé rozpínání vody při mrznutí projevilo svisle. V nenasyceném "
      "písku je ale vzduchových pórů mnohonásobně víc, než kolik objemu led přidá. Celkový zdvih bude proto "
      "malý (desetiny mm), ale **uvnitř vzorku se může voda přesouvat** k čelu promrzání (kryosukce): nahoře "
      "vrstva nabobtná, níž se vysuší a smrští. Proto se měří deformace **po vrstvách** (kotvy E1–E3), ne "
      "jen povrch. Při tání se ukáže nevratné sednutí (zhutnění) za každý cyklus.\n")

# 3 ---------------------------------------------------------------------------
print("## 3. Varianta B – rozlišení posunů a poměrných deformací\n")
res_mv = 0.667               # CR1000, rozsah ±5000 mV, diferenciálně s reverzací (≈)
res_um = p.LVDT_B_RANGE * 2 * 1000 / 10000 * res_mv
layers = [("povrch – E1", 0, 25), ("E1 – E2", 25, 50), ("E2 – E3", 50, 75), ("E3 – dno", 75, 100)]
head("vrstva", "hloubka [mm]", "tloušťka L0 [mm]", "posun = rozdíl", "rozlišení ε [–]")
for name, a, b in layers:
    n_sens = 1 if b == 100 else 2
    row(name, f"{a:g}–{b:g}", f"{b - a:g}", "S̄ − E1" if a == 0 else ("E3 − 0 (dno pevné)" if b == 100 else name.replace(" – ", " − ")),
        f"{n_sens ** 0.5 * res_um / 1000 / (b - a):.1e}")
print(f"\nLVDT ±{p.LVDT_B_RANGE:g} mm s výstupem ±5 V na rozsahu CR1000 ±5000 mV: rozlišení ≈ {res_um:.2f} µm. "
      "Poměrná deformace vrstvy 25 mm se tak rozliší na ≈ 4·10⁻⁵ (0,004 %). Absolutní linearita LVDT "
      "(±0,25 % FS ≈ ±25 µm) se odstraní kalibrací mikrometrem; pro deformace mezi cykly rozhoduje "
      "stabilita, ne linearita.\n")

# 4 ---------------------------------------------------------------------------
print("## 4. Varianta B – teplotní chyba referenčního stojanu\n")
dT = p.T_WARM - p.T_COLD
al_stack = 40.0 + p.PEDESTAL_H           # Al distanční kus + podstavec
post = p.Z_BRIDGE
body = 45.0                               # upnutí LVDT → nulová poloha jádra (≈)
items = [("Al distanční kus + podstavec", al_stack, p.ALPHA_AL, +1),
         ("G10 mezikus", 10.0, p.ALPHA_G10, +1),
         (f"Invarové sloupky {post:g} mm", post, p.ALPHA_INVAR, -1),
         ("tělo LVDT (nerez) od upnutí k nule", body, 17e-6, +1),
         ("horní deska PETG-CF", p.TOP_PLATE_T, 45e-6, +1)]
head("prvek", "délka [mm]", "α [1/K]", f"změna při {dT:g} K [µm]")
tot = 0.0
for name, L, a, sg in items:
    d = sg * a * L * dT * 1000
    tot += d
    row(name, f"{L:g}", f"{a * 1e6:.1f}·10⁻⁶", f"{d:+.0f}")
row("**zdánlivý posun povrchu**", "", "", f"**{tot:+.0f}**")
print(f"\nZdánlivý posun ≈ {abs(tot):.0f} µm za 20 K je malý proti očekávaným desetinám mm, ale ne zanedbatelný. "
      "Odstraní se **slepou zkouškou** s Al náhradou vzorku ve stejném programu (odečíst jako funkci teploty "
      "Tbot a Tbridge). Kotvy mají Invarové tyčky (100–160 mm × 1,2·10⁻⁶ × 20 K ≈ 3–4 µm), takže chyba "
      "vrstev je hlavně společná všem snímačům a v rozdílech mezi kotvami se odečte.\n")

# 5 ---------------------------------------------------------------------------
print("## 5. Cela z PETG-CF – napětí\n")
r = p.D_CELL_IN / 2
head("případ", "boční tlak p [MPa]", "obvodové napětí σθ [MPa]", "pevnost XY [MPa]", "bezpečnost krátkodobě", "dlouhodobě (30 %)")
for name, pl in (("A: 25 kPa, K0 = 1", 0.025), ("B: tlak ledu na stěnu 200 kPa (horní odhad)", 0.2),
                 ("extrém 1 MPa", 1.0)):
    s = pl * r / p.WALL
    lo, hi = p.PETGCF["sigma_xy"]
    row(name, pl, f"{s:.2f}", f"{lo:g}–{hi:g}", f"{lo / s:.0f}–{hi / s:.0f}",
        f"{lo * p.LONG_TERM_FACTOR / s:.1f}–{hi * p.LONG_TERM_FACTOR / s:.1f}")
print("\nCela je plná (jeden kus z 3D tisku), tištěná nastojato: obvodové napětí jde podél vláken.\n")
print("**Tření o stěnu plné cely** – část přitížení odnese stěna (Janssen): "
      "σv(dno)/σv(povrch) = exp(−4·μ·K·H/D).\n")
head("rozhraní", "μ", "K", "σv dno / povrch", "A: σv u dna při 25 kPa [kPa]", "osová síla do stěny [N]")
for name, mu in (("PTFE fólie + silikonový tuk", 0.05), ("PTFE fólie nasucho", 0.10), ("bez fólie (písek–PETG)", 0.5)):
    for K in (0.4, 0.6):
        ratio = math.exp(-4 * mu * K * p.H_SAMPLE / p.D_SAMPLE)
        row(name, mu, K, f"{ratio:.2f}", f"{25 * ratio:.1f}", f"{25 * (1 - ratio) * A / 1000:.0f}")
print("\nS PTFE fólií a tukem dojde ke dnu ≈ 90 % přitížení, bez fólie jen 30–40 %. Proto: fólie povinná a "
      "PV1 (40 mm) a PB1 (dno) vyhodnocovat jako profil σv(z), ne jako jednu hodnotu. Ve variantě B je přitížení "
      "nulové, tření je malé, ale **přimrznutí ledu ke stěně** může brzdit zdvih zmrzlé horní vrstvy; PTFE má ze "
      "všech běžných materiálů nejmenší adhezi ledu. Osové napětí ve stěně od tření (A, 25 kPa, bez fólie): "
      f"{25 * (1 - math.exp(-4 * 0.5 * 0.5)) * A / 1000 / (math.pi * (p.D_CELL_OUT ** 2 - p.D_CELL_IN ** 2) / 4):.3f} MPa – zanedbatelné.\n")
lo_a, hi_a = p.PETGCF["alpha"]
print(f"Rozdílná roztažnost cela/vzorek: α PETG-CF ≈ {lo_a * 1e6:.0f}–{hi_a * 1e6:.0f}·10⁻⁶ 1/K → změna průměru "
      f"při 20 K ≈ {lo_a * p.D_CELL_IN * dT:.2f}–{hi_a * p.D_CELL_IN * dT:.2f} mm (cela se při ochlazení zúží "
      "víc než písek – boční tlak mírně vzroste; píst A má vůli ≥ 0,25 mm, horní deska B ≥ 0,5 mm).\n")

# 6 ---------------------------------------------------------------------------
print("## 6. Varianta A – zdvih pod přitížením\n")
heave = 0.09 * p.SAND["theta"][1] * p.H_SAMPLE
print(f"Horní mez při θ {p.SAND['theta'][1]}: 9 % × θ × {p.H_SAMPLE:g} mm ≈ **{heave:.1f} mm**; v nenasyceném písku podstatně "
      "méně (viz §2). LVDT ±10 mm stačí s rezervou.\n")

# 7 ---------------------------------------------------------------------------
print("## 7. Varianta A – přitížení závažím (max. 25 kPa)\n")


def disc_kg(t):
    return math.pi / 4 * ((p.DW_D / 1000) ** 2 - (p.DW_HOLE / 1000) ** 2) * t / 1000 * p.RHO_STEEL


m_full, m_half = disc_kg(p.DW_FULL_T), disc_kg(p.DW_HALF_T)
m_carrier = math.pi / 4 * (p.DW_D / 1000) ** 2 * p.DW_CARRIER_T / 1000 * p.RHO_STEEL
m_rod = math.pi / 4 * (p.DW_ROD_D / 1000) ** 2 * p.DW_ROD_L / 1000 * p.RHO_STEEL
m_fixed = p.PISTON_ASSY_KG + m_carrier + m_rod
print(f"Kotouč ⌀{p.DW_D:g}/{p.DW_HOLE:g} × {p.DW_FULL_T:g} mm = {m_full:.2f} kg, poloviční × {p.DW_HALF_T:g} mm = "
      f"{m_half:.2f} kg. Pevná část: píst se vším ≈ {p.PISTON_ASSY_KG:g} kg + nosná deska {m_carrier:.2f} kg "
      f"+ vodicí tyč {m_rod:.2f} kg = **{m_fixed:.2f} kg ≈ {m_fixed * 9.81 / A * 1000:.1f} kPa** (nejmenší přitížení).\n")
head("přitížení [kPa]", "celkem [kg]", "plné kotouče", "poloviční", "doladit [kg]", "výška kotoučů [mm]")
for s in p.SURCHARGES_KPA:
    m = s * A / 1000 / 9.81
    rest = m - m_fixed
    n_f = int(rest // m_full)
    rest -= n_f * m_full
    n_h = int(rest // m_half)
    rest -= n_h * m_half
    row(s, f"{m:.1f}", n_f, n_h, f"{rest:.2f}", f"{n_f * p.DW_FULL_T + n_h * p.DW_HALF_T:g}")
print("\nDoladění tenkými kotouči / podložkami; celkovou hmotnost všeho, co leží na vzorku, zvážit.\n")
m25 = 25 * A / 1000 / 9.81
c_w = (m25 - p.PISTON_ASSY_KG) * 460
c_s = 2.0e6 * math.pi / 4 * 0.1 ** 2 * 0.1
area = math.pi * p.DW_D / 1000 * 0.15 + math.pi / 4 * (p.DW_D / 1000) ** 2
ua = 5.0 * area
tau = c_w / ua / 3600
rate = (p.T_WARM - p.T_COLD) / p.STEP_H
head("tepelná setrvačnost závaží (25 kPa)", "hodnota", "poznámka")
row("tepelná kapacita závaží", f"{c_w / 1000:.1f} kJ/K", f"vzorek ≈ {c_s / 1000:.1f} kJ/K")
row("časová konstanta (volná konvekce h ≈ 5 W m⁻² K⁻¹)", f"{tau:.1f} h", "bez izolace kotoučů")
row("zpoždění teploty závaží při rampě programu", f"{rate * tau:.2f} K", f"rampa {rate:.2f} K/h (Set A)")
print("\nZávaží za vzduchem v mrazáku zaostává jen o desetiny kelvinu, protože program mění teplotu pomalu. "
      "Mezikus G10 ⌀60 × 10 pod nosnou deskou omezí tok tepla ze závaží do vzorku; teplotu závaží logovat (Tw).\n")
