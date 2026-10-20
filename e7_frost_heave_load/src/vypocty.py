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
print("## 1. Zatížení a síly\n")
print(f"Plocha vzorku ⌀{p.D_SAMPLE:g}: {A:.0f} mm² = {A / 100:.2f} cm².\n")
head("napětí [kPa]", "síla [N]", "závaží na páce 1:10 [kg]", "poznámka")
for s in p.SURCHARGES_KPA + (500, 1000, 2000):
    f = s * A / 1000
    note = "varianta A" if s in p.SURCHARGES_KPA else "varianta B (tlak ze zdvihu)"
    row(s, f"{f:.0f}", f"{f / p.LEVER_RATIO / 9.81:.1f}" if s in p.SURCHARGES_KPA else "–", note)

# 2 ---------------------------------------------------------------------------
print("\n## 2. Tuhost rámu (varianta B, konstantní výška)\n")
F = p.B_MAX_KPA * A / 1000
beam = p.PROFILES[p.BEAM_PROFILE]
col = p.PROFILES[p.COL_PROFILE]
d_beam = F * p.COL_SPAN ** 3 / (48 * p.E_AL * beam["I"])
d_col = F * p.FRAME_H / (p.E_AL * 2 * col["A"])
d_cell = 0.05                                   # kompresní siloměr 10 kN, ≈ deformace při FS
d_joint = (0.02, 0.15)                          # spoje profilů: šrouby do čela vs. úhelníky
k_soil = p.E_FROZEN * A / p.H_SAMPLE / 1000     # kN/mm
head("složka", f"poddajnost při {F / 1000:.1f} kN [mm]", "poznámka")
row(f"příčník {p.BEAM_PROFILE}, rozpětí {p.COL_SPAN:g}", f"{d_beam:.3f}", "ohyb, prostý nosník")
row(f"2 sloupy {p.COL_PROFILE}, délka {p.FRAME_H:g}", f"{d_col:.3f}", "tah")
row("kompresní siloměr 20 kN (≈)", f"{d_cell:.3f}", "podle katalogu, typicky 0,02–0,1")
row("spoje profilů (≈)", f"{d_joint[0]:.2f}–{d_joint[1]:.2f}", "šrouby do čela / úhelníky – rozhoduje")
tot = (d_beam + d_col + d_cell + d_joint[0], d_beam + d_col + d_cell + d_joint[1])
row("**celkem**", f"**{tot[0]:.2f}–{tot[1]:.2f}**", f"tuhost {F / 1000 / tot[1]:.0f}–{F / 1000 / tot[0]:.0f} kN/mm")
print(f"\nPro srovnání: tuhost zmrzlého vzorku E·A/H ≈ {k_soil:.0f} kN/mm (E = {p.E_FROZEN:g} MPa). "
      "Rám tedy není dokonale tuhý – posun pístu je nutné měřit (LVDT) a výsledek uvádět jako "
      "tlak při známé tuhosti omezení.\n")

# 3 ---------------------------------------------------------------------------
print("## 3. Teplotní roztažnost rámu – největší zdroj chyby ve variantě B\n")
dT = p.T_WARM - p.T_COLD
d_frame = p.ALPHA_AL * p.FRAME_H * dT
stack_steel = 110.0         # siloměr + šroub
stack_al = p.PEDESTAL_H + p.PISTON_H + p.BASE_T * 0
d_stack = p.ALPHA_AL * stack_al * dT + p.ALPHA_STEEL * stack_steel * dT
mismatch = d_frame - d_stack
k_frame = F / 1000 / tot[1]
k_series = 1 / (1 / k_frame + 1 / k_soil)
head("veličina", "hodnota", "jednotka", "poznámka")
row(f"zkrácení sloupů Al {p.FRAME_H:g} mm při ΔT {dT:g} K", f"{d_frame:.3f}", "mm")
row("zkrácení vnitřní sestavy (Al podstavec + píst, ocel. siloměr + šroub)", f"{d_stack:.3f}", "mm", "bez zeminy")
row("rozdíl, který stlačí vzorek při ochlazení", f"{mismatch:.3f}", "mm")
row("tuhost rám + zmrzlý vzorek v sérii", f"{k_series:.1f}", "kN/mm")
art = mismatch * k_series * 1000
row("**falešná síla jen z teploty**", f"**{art:.0f}**", "N", f"≈ {art / A * 1000:.0f} kPa – srovnatelné s měřeným tlakem")
row("s tepelně sladěnou sestavou (Al distanční trubka místo oceli)", f"{(p.ALPHA_AL - p.ALPHA_STEEL) * 40 * dT * k_series * 1000:.0f}", "N",
    "zbývá jen siloměr ≈ 40 mm oceli")
print("\nOpatření: (1) sestavu mezi základem a příčníkem udělat z Al tak, aby se smršťovala stejně jako sloupy; "
      "(2) slepá zkouška s ocelovou/Al náhradou vzorku ve stejném programu → odečíst teplotní artefakt; "
      "(3) LVDT vztažené k Invarové tyči ze základu.\n")

# 4 ---------------------------------------------------------------------------
print("## 4. Cela z PETG-CF – napětí\n")
r = p.D_CELL_IN / 2
head("případ", "boční tlak p [MPa]", "obvodové napětí σθ [MPa]", "pevnost XY [MPa]", "bezpečnost krátkodobě", "dlouhodobě (30 %)")
for name, pl in (("A: 200 kPa, K0 = 1", 0.2), ("B: 1 MPa, K0 = 1 (horní mez)", 1.0), ("B: 2 MPa (extrém)", 2.0)):
    s = pl * r / p.WALL
    lo, hi = p.PETGCF["sigma_xy"]
    row(name, pl, f"{s:.1f}", f"{lo:g}–{hi:g}", f"{lo / s:.0f}–{hi / s:.0f}",
        f"{lo * p.LONG_TERM_FACTOR / s:.1f}–{hi * p.LONG_TERM_FACTOR / s:.1f}")
print("\n**Osové napětí ve stěně od tření** (táhne vrstvy od sebe, pokud je cela dole uchycená):\n")
head("případ", "μ", "třecí síla [kN]", "osové napětí stěny [MPa]", "pevnost Z [MPa]", "bezpečnost")
a_wall = math.pi * p.D_CELL_IN * p.H_SAMPLE
a_sect = math.pi * (p.D_CELL_OUT ** 2 - p.D_CELL_IN ** 2) / 4
for name, mu in (("bez fólie (zmrzlá zemina–PETG)", 0.5), ("PTFE fólie + silikonový tuk", 0.05)):
    ff = mu * 1.0 * a_wall / 1000
    s = ff * 1000 / a_sect
    lo, hi = p.PETGCF["sigma_z"]
    row(name, mu, f"{ff:.1f}", f"{s:.1f}", f"{lo:g}–{hi:g}", f"{lo / s:.1f}–{hi / s:.1f}")
print("\n(boční tlak 1 MPa). Bez fólie je osové napětí přes vrstvy kritické → fólie + cela volně "
      "uložená (neupnutá), aby tření stěnu tlačilo, ne táhlo.\n")
lo_a, hi_a = p.PETGCF["alpha"]
print(f"Rozdílná roztažnost cela/vzorek: α PETG-CF ≈ {lo_a * 1e6:.0f}–{hi_a * 1e6:.0f}·10⁻⁶ 1/K → změna průměru "
      f"při 20 K ≈ {lo_a * p.D_CELL_IN * dT:.2f}–{hi_a * p.D_CELL_IN * dT:.2f} mm (cela se při ochlazení zúží "
      "víc než Al píst ⌀99,5 – vůle pístu ≥ 0,3 mm).\n")

# 5 ---------------------------------------------------------------------------
print("## 5. Očekávaný zdvih (uzavřený systém, bez přítoku vody)\n")
heave = 0.09 * p.THETA * p.H_SAMPLE
print(f"Zmrznutí vody v pórech na místě: 9 % × θ {p.THETA} × {p.H_SAMPLE:g} mm ≈ **{heave:.1f} mm**. "
      "Otevřený systém (přítok vody zespodu, růst ledových čoček) dá víc – podle zeminy několik mm až cm. "
      f"Rozsah LVDT ±10 mm a volný zdvih pístu {p.HEAVE_ALLOW:g} mm pokrývají oba případy.\n")

# 6 ---------------------------------------------------------------------------
print("## 6. Siloměry – rozsah a rozlišení\n")
head("použití", "typ", "rozsah", "1 kPa ≙", "tep. drift nuly (0,02 %FS/10 K) při 20 K")
for use, typ, fs in (("A: v sérii s pákou", "S-snímač tah/tlak, C3, kompenz. −10…+40 °C", 2000),
                     ("B: nahoře", "kompresní (kanystr/sloupek), vysoká tuhost", 20000),
                     ("B: dole pod podstavcem", "kompresní, stejný typ", 20000)):
    drift = 0.0002 * fs * 2
    row(use, typ, f"{fs / 1000:g} kN", f"{A / 1000:.1f} N = {A / 1000 / fs * 100:.3f} %FS",
        f"{drift:.1f} N ≈ {drift / A * 1000:.1f} kPa")
