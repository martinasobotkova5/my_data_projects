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
z_base = 80.0 - p.BODY_BOTTOM               # horní líc základové desky (výkresové souřadnice, dno vzorku = 80)
post = p.Z_BRIDGE - z_base
body = 45.0                               # upnutí LVDT → nulová poloha jádra (≈)
items = [(f"tištěné dno cely {p.BODY_BOTTOM:g} mm (PETG)", p.BODY_BOTTOM, p.ALPHA_PETG, +1),
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
      "Tbot a Tstand). Kotvy mají Invarové tyčky (100–160 mm × 1,2·10⁻⁶ × 20 K ≈ 3–4 µm), takže chyba "
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

# 8 ---------------------------------------------------------------------------
print("## 8. Bod M – TDR, Pt100 a optické čidlo ve stejném místě (obě varianty)\n")
c0 = 0.2998                       # m/ns
L = p.TDR_ROD_L / 1000
dt = 0.0122                       # ns, rozlišení TDR200 (≈, ověřit)
head("stav písku", "εa (≈)", "dvojí doba běhu t [ns]", "Δεa při Δt 12 ps", "Δθ (Topp, ≈)")
for name, ea in (("suchý", 3.0), ("θ 0,10", 6.0), ("θ 0,18", 10.0), ("zmrzlý, nezamrzlá voda ≈ 0,02", 4.0)):
    t = 2 * L * ea ** 0.5 / c0
    de = 2 * ea / t * dt
    dth = de * (0.0292 - 2 * 0.00055 * ea + 3 * 4.3e-6 * ea ** 2)
    row(name, f"{ea:g}", f"{t:.2f}", f"{de:.2f}", f"{dth:.3f}")
print(f"\nTyčky {p.TDR_ROD_L:g} mm jsou na hranici – krátká doba běhu. Proto: průměrovat více průběhů, "
      "kalibrovat sondu přímo v tomto písku (několik vlhkostí, +10 °C) a pro zmrzlý stav použít "
      "kalibraci nezamrzlé vody (Spaans & Baker 1995; Watanabe & Wake 2009). Citlivý objem 3-tyčkové sondy "
      f"sahá ≈ 1–1,5× rozteč (5 mm) od tyček; Pt100 a FBG jsou {p.M_SIDE:g} mm stranou, takže měření TDR "
      "téměř neovlivní.\n")
head("čidlo", "přesnost", "rozlišení na CR1000 / převodníku", "poznámka")
row("Pt100 1/10 DIN, 4vodič, 4WPB100", "±0,03 °C při 0 °C", "≈ 0,01 °C (BrHalf4W, 2500 mV)", "reference pro FBG a T3")
row("FBG v kapiláře ⌀1", "±0,2–0,5 °C po kalibraci", "≈ 0,05–0,1 °C (≈ 10 pm/K, 1 pm)", "kapilára = bez vlivu deformace")
row("termistor 109SS (T3, 4 mm výš, r 40)", "±0,38 °C při 0 °C", "≈ 0,01 °C", "porovnání s Pt100 → korekce")
print("\nVšechny tři prvky leží v hloubce 54 mm, kolem r ≈ 25 mm, v pásu ±12 mm do strany (TDR tyčky nad sebou ±5 mm), takže "
      "měří stejnou vrstvu ve stejný okamžik promrzání. Pt100 je teplotní reference: přes ni se kalibruje FBG "
      "i termistor T3 přímo v cele (ledový bod při tání), a TDR se vztahuje k teplotě Pt100 → křivka nezamrzlé "
      "vody θu(T) (charakteristika mrznutí písku).\n")

# 9 ---------------------------------------------------------------------------
import sensors as sn

print("## 9. Varianta A-min – zjednodušená A s nehybným (pevným) omezením\n")
print("Vzorek je nahoře sevřen ocelovým víkem na 3 táhlech; píst dosedne středovým šroubem s dosedacím "
      f"předpětím {p.AM_SEATING_KPA:g} kPa a pak se nic nehýbe. Tlak, který při mrznutí vznikne, měří PV1 a PB1.\n")
F = p.AM_P_DESIGN_KPA * A / 1000          # N
n = len(p.AM_TIE_ANG)
As = 58.0                                 # mm², M10
L_rod = p.AM_BASE_T2 + p.AM_G10_T + p.AM_BOTTOM_T + p.H_SAMPLE + p.AM_PISTON_H + p.AM_LID_GAP + p.AM_LID_T
E_st = 200_000.0
d_rod = F * L_rod / (E_st * n * As)
a, t, nu = p.AM_TIE_R, p.AM_LID_T, 0.3
D = E_st * t ** 3 / (12 * (1 - nu ** 2))
r0 = p.AM_SCREW_D / 2
sig_lid = 3 * F / (2 * math.pi * t ** 2) * ((1 + nu) * math.log(a / r0) + 1)
w_lid = F * a ** 2 / (16 * math.pi * D) * (3 + nu) / (1 + nu)
head(f"při {p.AM_P_DESIGN_KPA:g} kPa (F = {F / 1000:.2f} kN)", "hodnota", "poznámka")
row("tah v 1 táhle M10", f"{F / n / 1000:.2f} kN", f"napětí {F / n / As:.0f} MPa (A4-70: mez kluzu 450 MPa)")
row(f"protažení táhel (L ≈ {L_rod:.0f} mm)", f"{d_rod * 1000:.0f} µm", "")
row(f"průhyb víka ⌀{p.AM_LID_D:g} × {t:g} (podepřeno na r {a:g})", f"{w_lid * 1000:.0f} µm", f"napětí ≈ {sig_lid:.0f} MPa (S235: 235 MPa)")
row("**celkový posun pístu**", f"**{(d_rod + w_lid) * 1000:.0f} µm**", "při 200 kPa pětkrát méně")
print("\nOmezení je tedy prakticky nehybné: i při 1 MPa se píst posune o ≈ 0,1 mm, při realistických "
      "stovkách kPa o desítky µm. Skutečný posun ukazuje LVDT na víku.\n")
dT = p.T_WARM - p.T_COLD
rods = L_rod * 16e-6
stack = (p.AM_G10_T * p.ALPHA_G10 + p.AM_BOTTOM_T * p.ALPHA_PETG + p.AM_PISTON_H * p.ALPHA_AL + p.AM_LID_GAP * 16e-6
         + p.H_SAMPLE * 10e-6 + p.AM_BASE_T2 * 0)
print("**Teplotní roztažnost** (táhla nerez vs. vnitřní sestava: tištěné dno 26 + písek + Al píst + šroub):\n")
head("", f"změna při {dT:g} K [µm]")
row("táhla nerez", f"{rods * dT * 1000:.0f}")
row("vnitřní sestava", f"{stack * dT * 1000:.0f}")
row("**rozdíl**", f"**{(rods - stack) * dT * 1000:+.0f}**")
print("\nTáhla a vnitřní sestava se při ochlazení zkracují téměř stejně, takže teplota sama vzorek nestlačí "
      "ani neuvolní (na rozdíl od původní varianty B s Al rámem). Zbytek ukáže slepá zkouška s Al náhradou.\n")
lo = hi = 0
fm = lambda x: f"{x:,}".replace(",", " ")
print("**Co je potřeba koupit (EUR bez DPH, orientačně)**\n")
head("tag", "měří", "typ", "ks", "celkem", "zdroj ceny")
for tag, what, typ, n_, a_, b_, src, ch in sn.A_MIN_SENSORS:
    lo += n_ * a_; hi += n_ * b_
    row(tag or "", what, typ, n_, fm(n_ * a_) if a_ == b_ else f"{fm(n_ * a_)}–{fm(n_ * b_)}", src)
s_lo, s_hi = lo, hi
print()
head("mechanika", "cena")
for what, a_, b_ in sn.A_MIN_MECH:
    lo += a_; hi += b_
    row(what, f"{a_}–{b_}")
print(f"\n| | čidla | mechanika | **celkem** |\n|---|---|---|---|\n| EUR bez DPH | {fm(s_lo)}–{fm(s_hi)} | "
      f"{fm(lo - s_lo)}–{fm(hi - s_hi)} | **{fm(lo)}–{fm(hi)}** |\n| Kč bez DPH (≈ 25 Kč/€) | {s_lo * 25 / 1000:.0f}–"
      f"{s_hi * 25 / 1000:.0f} tis. | {(lo - s_lo) * 25 / 1000:.0f}–{(hi - s_hi) * 25 / 1000:.0f} tis. | "
      f"**{lo * 25 / 1000:.0f}–{hi * 25 / 1000:.0f} tis.** |\n")
print("Bez ceny (už máte): TDR, teplotní čidlo a optické vlákno v bodě M, datalogger CR1000. "
      "Termistory T1, T2, Tair jsou volitelné.\n")

# 10 --------------------------------------------------------------------------
print("## 10. Varianta A-rám – nehybné omezení v rámu z Al profilů\n")
print("Stejné jako A-min (tištěná cela ⌀160 podle výkresu Column_one_body), jen místo víka na táhlech drží píst rám: 2 sloupy 40×80 a příčník 80×80, "
      "v příčníku šroub M16 × 1,5, mezi šroubem a pístem Al sloupek ⌀40 a vložka POM-C.\n")
F = p.AM_P_DESIGN_KPA * A / 1000
beam = p.PROFILES["80x80"]
col = p.PROFILES["40x80"]
d_beam = F * p.COL_SPAN ** 3 / (48 * p.E_AL * beam["I"])
d_col = F * p.AF_COL_H / (p.E_AL * 2 * col["A"])
d_sp = F * (p.AF_SPACER_D and (p.AF_SPACER_L / (p.E_AL * math.pi / 4 * p.AF_SPACER_D ** 2)
                               + p.AF_POM_T / (3000 * math.pi / 4 * p.AF_SPACER_D ** 2)))
d_joint = (0.01, 0.08)
tot = (d_beam + d_col + d_sp + d_joint[0], d_beam + d_col + d_sp + d_joint[1])
head(f"při {p.AM_P_DESIGN_KPA:g} kPa (F = {F / 1000:.2f} kN)", "posun [µm]", "poznámka")
row("průhyb příčníku 80×80, rozpětí 220", f"{d_beam * 1000:.0f}", "prostý nosník")
row(f"protažení 2 sloupů 40×80 × {p.AF_COL_H:g}", f"{d_col * 1000:.0f}", "")
row(f"stlačení Al sloupku {p.AF_SPACER_L:g} + POM {p.AF_POM_T:g}", f"{d_sp * 1000:.0f}", "POM E ≈ 3 GPa")
row("spoje profilů (šrouby do čela)", f"{d_joint[0] * 1000:.0f}–{d_joint[1] * 1000:.0f}", "rozhoduje – dotáhnout momentem")
row("**celkem**", f"**{tot[0] * 1000:.0f}–{tot[1] * 1000:.0f}**", "při 200 kPa pětkrát méně")
dT = p.T_WARM - p.T_COLD
cols = p.AF_COL_H * p.ALPHA_AL
stack_noPOM = (p.AM_G10_T * p.ALPHA_G10 + p.AM_BOTTOM_T * p.ALPHA_PETG + (p.AM_PISTON_H + p.AF_SPACER_L + p.AF_POM_T) * p.ALPHA_AL
               + p.AF_SCREW_PROTRUDE * 16e-6 + p.H_SAMPLE * p.ALPHA_SAND_FROZEN)
stack_POM = (p.AM_G10_T * p.ALPHA_G10 + p.AM_BOTTOM_T * p.ALPHA_PETG + (p.AM_PISTON_H + p.AF_SPACER_L) * p.ALPHA_AL + p.AF_POM_T * p.ALPHA_POM
             + p.AF_SCREW_PROTRUDE * 16e-6 + p.H_SAMPLE * p.ALPHA_SAND_FROZEN)
k_soil = p.E_FROZEN * A / p.H_SAMPLE / 1000
k_frame = F / 1000 / ((tot[0] + tot[1]) / 2)
k_s = 1 / (1 / k_soil + 1 / k_frame)
print("\n**Teplotní roztažnost** – Al sloupy se při ochlazení zkrátí víc než vnitřní sestava (písek má menší α), "
      "takže by rám vzorek stlačil. Vložka POM-C (α ≈ 110·10⁻⁶) to vyrovná:\n")
head("", f"sloupy − sestava při {dT:g} K [µm]", "falešný tlak (zmrzlý písek) [kPa]")
for name, st in ((f"Al sloupek {p.AF_SPACER_L + p.AF_POM_T:g} mm (bez POM)", stack_noPOM),
                 (f"Al {p.AF_SPACER_L:g} + POM {p.AF_POM_T:g} mm", stack_POM)):
    mm = (cols - st) * dT
    row(name, f"{mm * 1000:+.0f}", f"{mm * k_s * 1e6 / A:.0f}")
print(f"\nTuhost rám ≈ {k_frame:.0f} kN/mm, zmrzlý vzorek ≈ {k_soil:.0f} kN/mm (E = {p.E_FROZEN:g} MPa). α zmrzlého písku "
      "je odhad – zbytek se odečte ze **slepé zkoušky** s Al náhradou vzorku ve stejném programu.\n")
lo = sum(n_ * a_ for _, _, _, n_, a_, b_, _, _ in sn.A_MIN_SENSORS)
hi = sum(n_ * b_ for _, _, _, n_, a_, b_, _, _ in sn.A_MIN_SENSORS)
mlo = sum(a_ for _, a_, b_ in sn.A_FRAME_MECH)
mhi = sum(b_ for _, a_, b_ in sn.A_FRAME_MECH)
print("**Mechanika A-rám (EUR bez DPH, odhad)**\n")
head("položka", "cena")
for what, a_, b_ in sn.A_FRAME_MECH:
    row(what, f"{a_}–{b_}")
print(f"\nČidla stejná jako A-min ({fm(lo)}–{fm(hi)} €). **Celkem ≈ {fm(lo + mlo)}–{fm(hi + mhi)} € "
      f"(≈ {(lo + mlo) * 25 / 1000:.0f}–{(hi + mhi) * 25 / 1000:.0f} tis. Kč) bez DPH**; TDR, teplotní čidlo, optické "
      "vlákno a CR1000 už máte.\n")

# 11 --------------------------------------------------------------------------
print("## 11. Tištěná cela A (Column_one_body_version_1) – kontrola\n")
print(f"Tělo ⌀{p.BODY_D:g} × {p.BODY_H:g}, límec ⌀{p.COLLAR_OD:g} do {p.COLLAR_TOP:g} mm, dutina ⌀{p.CAV_D:g}, dno {p.BODY_BOTTOM:g} mm, "
      f"písek {p.SAND_TOP - p.BODY_BOTTOM:g} mm, nad ním {p.COLLAR_TOP - p.SAND_TOP:g} mm pro píst. Plášť vytištěný s 10 % výplní "
      "slouží zároveň jako tepelná izolace.\n")
head("případ", "200 kPa", "1 MPa", "poznámka")
for name, f_ in (("obvodové napětí, jen vnitřní stěna 3 mm", lambda q: q * 50 / 3),
                 ("obvodové napětí, stěna kolem dutiny 5 mm (≈ 8 perimetrů)", lambda q: q * 50 / 5)):
    row(name, f"{f_(0.2):.1f} MPa", f"{f_(1.0):.1f} MPa", "PETG(-CF) 40–55 MPa krátkodobě, ≈ 12–16 MPa dlouhodobě")
row("tlak na dno (= tlak v písku)", "0,2 MPa", "1,0 MPa", "10 % gyroid ≈ 1–2 MPa pevnost v tlaku → pod dutinou 100 % výplň")
print("\nDoporučení pro tisk: kolem dutiny stěnu ≈ 5 mm (≈ 8 perimetrů), pod dutinou (z 0–26) 100 % výplň (modifikátor v PrusaSliceru), "
      "zbytek pláště 10 % (izolace). Pak cela snese i horní odhad 1 MPa.\n")

# 12 --------------------------------------------------------------------------
print("## 12. Varianta B-open – nejjednodušší sestava, otevřený povrch\n")
print("Tištěná cela ⌀160 na Al desce, bod M (CS645 + vlákno + Pt100 – už máte), na povrchu písku jen malý terčík "
      f"⌀{p.BO_TARGET_D:g} × {p.BO_TARGET_T:g} s jedním LVDT s volným jádrem na Invarovém sloupku. Žádné víko, horní deska, "
      "kotvy ani můstek.\n")
A_t = math.pi / 4 * p.BO_TARGET_D ** 2
m_t = 0.002 + math.pi / 4 * 0.003 ** 2 * 0.11 * 8100 + 0.010     # terčík + Invarová tyčka 110 mm + jádro LVDT (≈ 10 g)
print(f"**Přítlak terčíku na písek:** ≈ {m_t * 1000:.0f} g na ⌀{p.BO_TARGET_D:g} → ≈ {m_t * 9.81 / A_t * 1000:.2f} kPa "
      "jen pod terčíkem; zbytek povrchu je volný.\n")
z_base = 80.0 - p.BODY_BOTTOM
post = (80.0 + p.H_SAMPLE + (p.COLLAR_TOP - p.SAND_TOP) + p.BO_ARM_Z) - z_base
items = [(f"tištěné dno cely {p.BODY_BOTTOM:g} mm", p.BODY_BOTTOM, p.ALPHA_PETG, +1),
         (f"Invarový sloupek ≈ {post:.0f} mm", post, p.ALPHA_INVAR, -1),
         ("Invarová tyčka jádra ≈ 110 mm", 110.0, p.ALPHA_INVAR, -1),
         ("tělo LVDT od upnutí k nule", 45.0, 17e-6, +1)]
head("prvek", "délka [mm]", f"změna při {dT:g} K [µm]")
tot = 0.0
for name, L, a, sg in items:
    d = sg * a * L * dT * 1000
    tot += d
    row(name, f"{L:.0f}", f"{d:+.0f}")
row("**zdánlivý posun povrchu**", "", f"**{tot:+.0f}**")
print("\nOdečte se slepou zkouškou (Al náhrada vzorku). S nerezovou tyčkou jádra místo Invarové by chyba vzrostla "
      "o ≈ 35 µm.\n")
print("**Otevřený povrch a vysychání:** v mrazáku písek z povrchu pomalu sublimuje/vysychá (u mrazáků s odmrazováním "
      "rychleji). Celu vážit na začátku a po každém cyklu (váha 5 kg / 0,1 g); pokud ztráta přesáhne ≈ 1 % vody, "
      "dát nad celu volný stan z fólie (nedotýká se povrchu, povrch zůstane otevřený).\n")
lo = sum(n_ * a_ for _, _, _, n_, a_, b_, _, _ in sn.B_OPEN_BUY) + sum(a_ for _, a_, b_ in sn.B_OPEN_MECH)
hi = sum(n_ * b_ for _, _, _, n_, a_, b_, _, _ in sn.B_OPEN_BUY) + sum(b_ for _, a_, b_ in sn.B_OPEN_MECH)
print(f"**Co koupit:** LVDT s volným jádrem + zdroj, Invarový sloupek s ramenem, Al deska, terčík; volitelně Tair. "
      f"Celkem ≈ {lo:.0f}–{hi:.0f} € bez DPH (≈ {lo * 25 / 1000:.0f}–{hi * 25 / 1000:.0f} tis. Kč).\n")

# 13 --------------------------------------------------------------------------
print("## 13. Varianta B-open – bezkontaktně: kamera shora + čárový laser\n")
fov = p.BL_SENSOR_W * p.BL_CAM_H / p.BL_LENS_F
px = fov / p.BC_SENSOR_PX * 1000
k = math.tan(math.radians(p.BL_LASER_ANG))
print("Na povrchu písku nic neleží. Čárový laser svítí šikmo (45° od svislice) přes celý povrch a přes horní "
      "hranu límce; kamera shora snímá čáru. Když povrch stoupne o Δh, čára se v obraze posune do strany o "
      f"Δh·tan 45° = Δh. Zorné pole ≈ {fov:.0f} mm → **{px:.0f} µm/px**; s vyhodnocením těžiště čáry "
      f"(≈ 0,1–0,3 px) ≈ {0.1 * px / k:.0f}–{0.3 * px / k:.0f} µm, reálně ≈ 10 µm (zrnitost písku, námraza).\n")
print("Čára dává celý **profil povrchu** napříč vzorkem (střed i okraj u stěny), ne jen jeden bod. Druhý laser "
      "otočený o 90° (+15–60 €) přidá druhý profil.\n")
rim = (p.COLLAR_TOP - p.BODY_BOTTOM)
print(f"**Reference = čára na horní hraně límce** ve stejném snímku – ruší pohyb kamery i laseru. Límec se ale sám "
      f"posune o ≈ {rim * p.ALPHA_PETG * dT * 1000:.0f} µm na {dT:g} K → odečíst ze **slepé zkoušky** (Al náhrada vzorku).\n")
lo = sum(a_ for *_, a_, b_ in sn.B_CAM_BUY) + sum(a_ for _, a_, b_ in sn.B_CAM_MECH)
hi = sum(b_ for *_, a_, b_ in sn.B_CAM_BUY) + sum(b_ for _, a_, b_ in sn.B_CAM_MECH)
print("**Kamera a laser v mrazáku:** oba v izolovaném boxu (XPS 30 mm) s topnou fólií 5 W a termostatem na +5 °C, "
      "okénka ze dvou skel. Teplo boxu nad vzorkem je malé (≈ 1 W přes izolaci a okénko), ale vliv ověřit termistorem "
      "Ttop / bodem M ve slepé zkoušce; lepší je kamera mimo mrazák s okénkem ve víku, pokud to víko dovolí. "
      "Laser zapínat jen na snímek (každých 10 min), jinak tma; čas synchronizovat s CR1000.\n")
print(f"**Cena:** ≈ {lo:.0f}–{hi:.0f} € bez DPH (≈ {lo * 25 / 1000:.0f}–{hi * 25 / 1000:.0f} tis. Kč).\n")

# 14 --------------------------------------------------------------------------
print("## 14. Varianta C – kombinace: Al rám vede mrtvou váhu, částečný píst, kamera nad volným povrchem\n")
A_p = math.pi / 4 * p.C_PISTON_D ** 2
zb0 = 0.0
col_h = p.C_INS_T + p.BODY_BOTTOM + p.H_SAMPLE + p.C_BEAM_GAP   # sloup od horního líce desky po příčník (rev. B s izolací)
rod_l = p.C_BEAM_GAP - p.C_PISTON_H - p.C_BALL_D + p.C_BEAM_H + p.C_TRAVEL + 10
m_pist = math.pi / 4 * (p.C_PISTON_D / 1000) ** 2 * p.C_PISTON_H / 1000 * 2700
m_rod = math.pi / 4 * (p.C_ROD_D / 1000) ** 2 * rod_l / 1000 * p.RHO_STEEL
m_car = math.pi / 4 * (p.C_CARRIER_D / 1000) ** 2 * p.C_CARRIER_T / 1000 * 2700
m_fix = m_pist + m_rod + m_car + 0.002
print(f"Píst ⌀{p.C_PISTON_D:g} (plocha {A_p:.0f} mm² = 25 % vzorku), volné mezikruží 25 mm kolem něj. "
      f"Pohyblivá část bez závaží: píst Al {m_pist * 1000:.0f} g + kulička + tyč ⌀{p.C_ROD_D:g} × {rod_l:.0f} "
      f"{m_rod * 1000:.0f} g + Al nosná deska {m_car * 1000:.0f} g = **{m_fix:.2f} kg ≈ {m_fix * 9.81 / A_p * 1000:.1f} kPa** "
      "(nejmenší přitížení pod pístem).\n")
head("napětí pod pístem [kPa]", "celkem [kg]", "kotouče 1 kg", "0,5 kg", "doladit [kg]")
for s_ in p.C_SURCHARGES_KPA:
    m = s_ * A_p / 1000 / 9.81
    rest = m - m_fix
    n1 = int(max(rest, 0) // 1.0); rest -= n1
    n2 = int(max(rest, 0) // 0.5); rest -= 0.5 * n2
    row(f"{s_:g}", f"{m:.2f}", n1, n2, f"{rest:.2f}")
t_disc = 1.0 / (math.pi / 4 * ((p.C_DISC_D / 1000) ** 2 - (p.C_DISC_HOLE / 1000) ** 2) * p.RHO_STEEL) * 1000
print(f"\nKotouč ⌀{p.C_DISC_D:g}/{p.C_DISC_HOLE:g}: 1 kg = {t_disc:.1f} mm, 0,5 kg = {t_disc / 2:.1f} mm. Při 25 kPa jen ≈ 4 kotouče.\n")
print("**Konstantní zatížení:** zátěž leží jen na pístu a s povrchem volně stoupá i klesá (zdvih ±"
      f"{p.C_TRAVEL:g} mm). Kluzné pouzdro igus drylin RJ4JP-01-12 (bez maziva, do −40 °C) má tření ≈ 0,1–0,25 × boční "
      "síla; při náklonu tyče 0,5° je boční síla < 0,1 N → změna zatížení < 0,02 kPa. Kulička mezi tyčí a pístem dovolí "
      "pístu se naklonit, tyč zůstává svislá.\n")
print(f"**Co se měří (jen 1 + 2):** (1) kamera + vícečárový laser {p.C_LASER_ANG:g}° ({p.C_LINES} čar po ≈ {p.C_LINE_PITCH:g} mm, "
      f"posun čáry = {1 / math.tan(math.radians(p.C_LASER_ANG)):.2f} × zdvih) → mapa výšek **celého povrchu** ⌀100 v každém snímku: volné mezikruží i horní plocha pístu, "
      "reference = invarový terčík u límce; (2) LVDT na rameni invarového sloupku pod nosnou deskou = pohyb zátěže (pístu), "
      "rozlišení ≈ 1 µm. Tlakové snímače nejsou potřeba – zatížení je známá mrtvá váha.\n")
print(f"**Rozměry:** sloupy 40×80 × {col_h:.0f} mm, spodní líc příčníku {p.C_BEAM_GAP:g} mm nad pískem (místo pro kameru "
      "a laser), závaží nad příčníkem mimo zorné pole. Pt100 jde ze strany TDR otvorem a nasedá uprostřed přímo nad horní tyčku CS645 (hloubka ≈ 33 mm) – povrch zůstává volný.\n")

# 15 --------------------------------------------------------------------------
print("## 15. Varianta C rev. B – posudek měření (10/2026, přepočteno pro Sr = 0,5 v 11/2026)\n")
n_por, sr = p.POROSITY, p.SR_TARGET
th = sr * n_por
print(f"**Očekávaný zdvih (rozhodnuto Sr = {sr:g}):** pórovitost ≈ {n_por}, θ = {th:.2f}; vzduch v pórech {100 * (n_por - th):.0f} % "
      f"objemu, objem ledu přibude jen o {100 * 0.09 * th:.1f} % → v uzavřeném vzorku se rozpínání vejde do pórů, "
      f"zdvih in situ ≈ 0 (desítky µm nanejvýš od migrace vody). Horní mez (vše nahoru) {0.09 * th * p.H_SAMPLE:.2f} mm. "
      "E7 tedy měří hlavně sednutí při tání pod zatížením; pro měření zdvihu by bylo nutné Sr ≥ 0,85 nebo voda zespodu.\n")
print("**Směr mrznutí (sim_thaw.py, Sr 0,5):** cela přímo na Al desce – 95 % zmrzne za ≈ 10,5 h i zespodu, poslední "
      "nezmrzlé místo 35 mm nade dnem; rev. B (cela tištěná vcelku ⌀240 × 200: +40 mm stěna a +40 mm dno z nízké výplně "
      "λ ≈ 0,06, podložky G10 v kapsách) – 95 % zmrzne za ≈ 15 h, celý vzorek za ≈ 16 h, poslední nezmrzlé 13 mm nade dnem "
      "→ mrznutí shora. Tání ≈ 15 h → cyklus 24 h + 24 h stačí (rezerva ≈ 8 h).\n")
print("**Tepelný drift sestavy (20 K, sim_thaw.py, zbytek = po korekci podle teplot cely ze slepé zkoušky):** "
      "rev. A (bez izolace, LVDT na Al příčníku, ocelová tyč) −24…+48 µm, zbytek ≤ 12 µm; kamera vůči PETG límci 0…100 µm, "
      "zbytek ≤ 8 µm. Jen izolace bez Invaru by zbytek LVDT zhoršila na 57 µm (cela reaguje pomaleji než sloupy a tyč). "
      "Rev. B (izolace + invarový sloupek + invarová tyč) −59…0 µm, zbytek ≤ 6 µm; kamera vůči invarovému terčíku "
      "−49…0 µm, zbytek ≤ 3 µm. Zbylý drift = PETG dno 26 mm + písek → změřit slepou zkouškou s Al atrapou.\n")
print("**Další změny:** RPi 5 v boxu s kamerou (žádný plochý kabel přes těsnění, jeho teplo drží okénko bez námrazy); "
      "RPi fotí podle hodin NTP (CR850 nemá volný port); kluzné pouzdro drylin místo kuličkového; čidlo vzduchu 109 povinně; ventilátor 80 mm; "
      "vážení cely před/po cyklu a RH vzduchu (SHT45) kvůli vymrzání a námraze; kalibrace kamery podložkami 0,1/0,5/1,0 mm.\n")

# 16 --------------------------------------------------------------------------
print("## 16. Varianta C rev. B3 – rám z T-profilů (11/2026)\n")
print("**Rám:** jen hliníkové T-profily drážka 8 řezané na délku – 2 podélníky 40×40 × 260, příčka 40×80 × 260 naplocho "
      "(nese 3 podložky G10), 2 sloupy 40×80, horní příčník 40×80 × 340 s jediným otvorem ⌀14; pouzdro ložiska visí "
      f"pod příčníkem, mezera nad pískem {p.C_BEAM_GAP:g} mm. Hliníkové desky L01/L02 odpadly. Rám zátěž jen vede, "
      "měření se k rámu nevztahuje (LVDT i terčík kamery jsou na invarovém sloupku), takže drift po korekci zůstává "
      "≤ 6 µm (LVDT) a ≤ 3 µm (kamera).\n")
print(f"**Pt100 (potvrzeno):** vodorovně ze strany TDR, osa {p.C_PT100_DZ:g} mm nad osou horní tyčky CS645, "
      f"hrot {p.C_PT100_TIP:g} mm od vnitřní stěny.\n")
print(f"**Vzorek (rozhodnuto):** Sr = {p.SR_TARGET:g}, θ = {p.SR_TARGET * p.POROSITY:.2f} (n ≈ {p.POROSITY}).\n")

# 17 --------------------------------------------------------------------------
print("## 17. Rám z T-profilů – únosnost, tuhost a stabilita (rev. B3, 11/2026)\n")
E_AL, F_AL = 70000.0, 160.0                       # MPa; EN AW-6063 T66, f0,2 ≈ 200 MPa → návrhově 160 MPa
# průřezy – konzervativní odhady pro lehké profily drážka 8 (Enprag KA-4080 2,2 kg/m; ověřit v technickém listu)
PROF = {"40x80": dict(m=2.2, I_s=45e4, I_w=12e4, W_w=6.0e3), "40x40": dict(m=1.5, I_s=7e4, I_w=7e4, W_w=3.5e3)}
g = 9.81
L_beam = p.C_COL_SPAN                             # rozpětí příčníku osa–osa sloupů (konzervativně)
L_cross = 2 * p.C_RAIL_X                          # rozpětí příčky základny
col_h = p.C_INS_T + p.BODY_BOTTOM + p.H_SAMPLE + p.C_BEAM_GAP
m_frame = PROF["40x80"]["m"] * (2 * col_h + 2 * (p.C_RAIL_X - 20) + p.C_TOP[0]) / 1000 + PROF["40x40"]["m"] * 2 * p.C_BASE[1] / 1000 + 12 * 0.05 + 0.2
m_dead = 25.0 * math.pi / 4 * p.C_PISTON_D ** 2 / 1000 / g + 0.5   # mrtvá váha pro 25 kPa + půlkilový kotouč
th = p.SR_TARGET * p.POROSITY
m_sand = 1600 * (1 + th / 1.6) * math.pi / 4 * 0.1 ** 2 * 0.1
m_cell = 1.5
m_other = 0.54 + 0.5 + 0.3                        # Invarový sloupek, box kamery s RPi, tištěné díly
m_tot = m_frame + m_dead + m_sand + m_cell + m_other
rows = []


def beam(F, L, sec, axis="w"):
    I = PROF[sec]["I_" + axis]; W = PROF[sec]["W_w"] if axis == "w" else PROF[sec]["I_s"] / 40
    M = F * L / 4
    return M / W, F * L ** 3 / (48 * E_AL * I) * 1000          # MPa, µm


F2 = m_dead * g
sig, d = beam(1.5 * F2, L_beam, "40x80")
rows.append(("ZS2 mimořádný: celá mrtvá váha na příčníku T04 (kroužek dosedne)", f"{F2:.0f} N uprostřed", f"σ = {sig:.1f} MPa, průhyb {d / 1.5:.1f} µm"))
F3 = 500.0
sig, d = beam(1.5 * F3, L_beam, "40x80")
rows.append(("ZS3 nesprávné použití: 500 N svisle na T04 (opření, odložená závaží)", "500 N uprostřed", f"σ = {sig:.1f} MPa, průhyb {d / 1.5:.0f} µm"))
F1 = (m_cell + m_sand + m_dead + 0.1) * g
sig, d = beam(1.5 * F1, L_cross, "40x80")
rows.append(("ZS1 provoz: cela + písek + závaží na příčce T03 (3 podložky u středu)", f"{F1:.0f} N", f"σ = {sig:.1f} MPa, průhyb {d / 1.5:.1f} µm"))
d_disc = beam(g, L_cross, "40x80")[1]
rows.append(("změna zatížení o 1 kg kotouč → změna průhybu T03 (jde do LVDT)", f"{g:.1f} N", f"{d_disc:.2f} µm"))
Ncr = math.pi ** 2 * E_AL * PROF["40x80"]["I_w"] / (2 * col_h) ** 2      # sloup jako konzola (K = 2)
rows.append(("sloup 40×80 tlak (ZS3) vs. Eulerova kritická síla (konzola)", f"{1.5 * F3 / 2:.0f} N", f"N_cr = {Ncr / 1000:.0f} kN"))
rows.append(("úhelník 40 drážka 8, smyk na 1 úhelník (příčka T03, 4 ks)", f"{F1 / 4:.0f} N",
             "tření spoje M8 (předpětí ≈ 6 kN × 0,2) ≈ 1,2 kN → bez prokluzu"))
rows.append(("T-matice M5 pouzdra P01 (4 ks) – zatěžuje je jen tření v pouzdře", "< 1 N", "typ. únosnost T-matice M5 ≥ 500 N"))
z_floor = -(22 + p.C_BASE[2])                     # spodek noh vůči horní ploše rámu
h_push = col_h + p.C_TOP[2] - z_floor
for half, lab in ((110.0, "rev. B3 původně (podélníky 260, nohy ±110)"), (p.C_FOOT_Y, f"nyní (podélníky {p.C_BASE[1]:g}, nohy ±{p.C_FOOT_Y:g})")):
    H = m_tot * g * half / h_push
    rows.append((f"překlopení ve směru y – vodorovná síla na T04, {lab}", f"G = {m_tot * g:.0f} N", f"H_krit ≈ {H:.0f} N"))
Hx = m_tot * g * p.C_RAIL_X / h_push
rows.append(("překlopení ve směru x (nohy ±150)", "", f"H_krit ≈ {Hx:.0f} N"))
print(f"Hmotnosti: rám {m_frame:.1f} kg, mrtvá váha až {m_dead:.1f} kg, písek {m_sand:.2f} kg (Sr {p.SR_TARGET:g}), cela {m_cell} kg, "
      f"ostatní {m_other:.1f} kg → celkem ≈ {m_tot:.1f} kg. Výška tlaku na T04 nad podlahou {h_push:.0f} mm. "
      "Průřezy: konzervativní odhady pro lehké profily drážka 8 (40×80: I_slabá ≈ 12 cm⁴, 40×40: I ≈ 7 cm⁴) – ověřit "
      "v technickém listu dodavatele. Součinitel zatížení 1,5, návrhová pevnost 160 MPa.\n")
print("| stav | zatížení | výsledek |\n|---|---|---|")
for r in rows:
    print("| " + " | ".join(r) + " |")
print("\n**Závěr:** napětí v profilech jsou desetiny až jednotky MPa (rezerva > 20×), průhyby jednotky µm. Rám zátěž jen vede, "
      "takže jeho únosnost nerozhoduje; profil 40×80 je zvolen kvůli tuhosti spojů a ploše pro úhelníky, ne kvůli pevnosti. "
      "**Rozhoduje stabilita proti překlopení:** s nožkami ±110 by stačil vodorovný tlak ≈ 40 N na horní příčník (např. při "
      f"nasazování kotoučů). Proto podélníky {p.C_BASE[1]:g} mm a nohy ±{p.C_FOOT_Y:g}; v mrazáku rám stojí ve vaně (opře se o stěnu), "
      "mimo mrazák manipulovat se závažím jen při přidrženém rámu. Prokluz spojů pod konstantním zatížením nehrozí; "
      "při výměně kotoučů se změní průhyb příčky T03 o < 1 µm (jde do LVDT, zanedbatelné).\n")

# 18 --------------------------------------------------------------------------
print("## 18. Datalogger CR850 + multiplexor AM16/32B (11/2026)\n")
print("CR850 (= CR800 s klávesnicí a displejem): 6 SE / 3 DIFF analogových vstupů, buzení VX1–VX2, porty C1–C4 "
      "(při SDM jsou C1–C3 vyhrazené pro TDR) a výstup 12 V. Multiplexor potřebuje RES na řídicím portu a CLK na "
      "řídicím portu **nebo na budicím kanálu** (manuál AM16/32B) → RES = C4, CLK = VX1. Na spouštění snímku port "
      "nezbude: RPi fotí podle vlastních hodin synchronizovaných NTP, hodiny CR850 synchronizuje LoggerNet (odchylka "
      "< 1 s, při intervalu 1–10 min zanedbatelné). Zdroj LVDT a ventilátor trvale zapnuté. LVDT diferenciálně: rozsah "
      "±5000 mV, rozlišení ≈ 0,67 mV = 1,3 µm při 0,5 V/mm, průměrováním 20–50 vzorků ≈ 0,5 µm.\n")
print("| svorka CR850 | připojeno | měření |\n|---|---|---|")
for r in (("DIFF1 (1H/1L)", "(2) LVDT DCTH400AG", "VoltDiff ±5000 mV, průměr 20–50 vzorků"),
          ("DIFF2 (2H/2L) + VX2", "Pt100 přes 4WPB100", "BrHalf4W, 2500 mV"),
          ("SE5 + VX2", "AM16/32B COM (režim 2×32): signál / buzení termistorů", "Therm109 / BrHalf přes MUX"),
          ("SE6", "rezerva (kontrola napájení LVDT přes dělič)", "VoltSE"),
          ("C1–C3", "TDR100/TDR200 → CS645", "SDM"),
          ("C4", "AM16/32B RES", "PortSet"),
          ("VX1", "AM16/32B CLK", "ExciteV pulz"),
          ("12 V + G", "AM16/32B napájení, ventilátor 80 mm (trvale)", "–"),
          ("–", "LVDT z vlastního zdroje 24 V (trvale), RPi snímá podle NTP", "–")):
    print("| " + " | ".join(r) + " |")
print("\n**Kanály multiplexoru (2×32, termistory 2 vodiče + společná zem):** 1 Tair 109 (povinně), 2 vzduch ve výšce "
      "povrchu, 3 dno cely (otvor v tištěném dnu pod dutinou), 4 vnější stěna cely, 5 invarový sloupek, 6 horní příčník "
      "T04, 7 příčka T03 → teploty pro korekci driftu ze slepé zkoušky (dnes se teplota dna a rámu neměří); "
      "volitelně 8–11 teplotní profil písku 10 / 25 / 70 / 90 mm pod povrchem (4 radiální otvory ⌀3,4 ve stěně cely, "
      "hroty 25 mm od stěny) → poloha čáry 0 °C (hloubka promrznutí) v čase; zbytek rezerva. Čidla: NTC 10 kΩ v epoxidu "
      "nebo v nerezové jímce ⌀3 s doplňkovým odporem 10 kΩ 0,1 % na svorce MUX, kalibrace v ledové lázni (±0,1 K).\n")

# 19 --------------------------------------------------------------------------
print("## 19. Laser podle nabídky Picotronic A2627918 (13. 11. 2026)\n")
st, fan = p.C_LASER_DOE
d_old = math.hypot(50.0, 124.0)
d = math.hypot(p.C_LASER_Y, p.C_LASER_H)
a = p.C_LASER_ANG
def cover(dd, aa):
    return 2 * dd * math.tan(math.radians(fan / 2)), dd * math.tan(math.radians(st)) / math.sin(math.radians(aa))
L0, s0 = cover(d_old, 68.0)
L1, s1 = cover(d, a)
print(f"DOE-DER253: úhel mezi čarami {st:g}°, vějíř {fan:g}° (dříve odhadováno 3,8° / 41°). Z původní polohy (134 mm, 68°) "
      f"by čáry byly dlouhé jen {L0:.0f} mm po {s0:.1f} mm → nepokryly by povrch ⌀100. **Nová poloha:** laser vedle horního "
      f"příčníku, {p.C_LASER_Y:g} mm od osy, {p.C_LASER_H:g} mm nad pískem, vzdálenost {d:.0f} mm, sklon {a:g}° → čáry "
      f"≈ {L1:.0f} mm dlouhé po ≈ {s1:.1f} mm, na písku ⌀100 ≈ 9 čar, límec ⌀106 pokrytý; posun čáry = "
      f"{1 / math.tan(math.radians(a)):.2f} × zdvih. Držák P05 přepracován (blok mimo poloměr nosné desky 70 mm). Krajní "
      "čára u stěny na straně kamery je uprostřed zastíněná pouzdrem ložiska (krátká tětiva, zanedbatelné). "
      "Doporučen modul DOE253-635-5-6(10x24) s nastavitelným ohniskem (zaostřit na 200 mm) a 5 mW – rezerva pro tmavý "
      "mokrý / zmrzlý písek a krátkou expozici; třída 2M: nedívat se do svazku optickými přístroji.\n")
