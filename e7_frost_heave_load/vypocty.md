# E7 – návrhové výpočty

Generováno skriptem `src/vypocty.py` z `src/params.py`. Hodnoty ≈ jsou odhady k ověření.

## 1. Zatížení a síly

Plocha vzorku ⌀100: 7854 mm² = 78.54 cm².

| napětí [kPa] | síla [N] | závaží na páce 1:10 [kg] | poznámka |
|---|---|---|---|
| 25 | 196 | 2.0 | varianta A |
| 50 | 393 | 4.0 | varianta A |
| 100 | 785 | 8.0 | varianta A |
| 200 | 1571 | 16.0 | varianta A |
| 500 | 3927 | – | varianta B (tlak ze zdvihu) |
| 1000 | 7854 | – | varianta B (tlak ze zdvihu) |
| 2000 | 15708 | – | varianta B (tlak ze zdvihu) |

## 2. Tuhost rámu (varianta B, konstantní výška)

| složka | poddajnost při 15.7 kN [mm] | poznámka |
|---|---|---|
| příčník 80x80, rozpětí 220 | 0.036 | ohyb, prostý nosník |
| 2 sloupy 40x80, délka 330 | 0.035 | tah |
| kompresní siloměr 20 kN (≈) | 0.050 | podle katalogu, typicky 0,02–0,1 |
| spoje profilů (≈) | 0.02–0.15 | šrouby do čela / úhelníky – rozhoduje |
| **celkem** | **0.14–0.27** | tuhost 58–112 kN/mm |

Pro srovnání: tuhost zmrzlého vzorku E·A/H ≈ 16 kN/mm (E = 200 MPa). Rám tedy není dokonale tuhý – posun pístu je nutné měřit (LVDT) a výsledek uvádět jako tlak při známé tuhosti omezení.

## 3. Teplotní roztažnost rámu – největší zdroj chyby ve variantě B

| veličina | hodnota | jednotka | poznámka |
|---|---|---|---|
| zkrácení sloupů Al 330 mm při ΔT 20 K | 0.152 | mm |
| zkrácení vnitřní sestavy (Al podstavec + píst, ocel. siloměr + šroub) | 0.051 | mm | bez zeminy |
| rozdíl, který stlačí vzorek při ochlazení | 0.102 | mm |
| tuhost rám + zmrzlý vzorek v sérii | 12.4 | kN/mm |
| **falešná síla jen z teploty** | **1258** | N | ≈ 160 kPa – srovnatelné s měřeným tlakem |
| s tepelně sladěnou sestavou (Al distanční trubka místo oceli) | 115 | N | zbývá jen siloměr ≈ 40 mm oceli |

Opatření: (1) sestavu mezi základem a příčníkem udělat z Al tak, aby se smršťovala stejně jako sloupy; (2) slepá zkouška s ocelovou/Al náhradou vzorku ve stejném programu → odečíst teplotní artefakt; (3) LVDT vztažené k Invarové tyči ze základu.

## 4. Cela z PETG-CF – napětí

| případ | boční tlak p [MPa] | obvodové napětí σθ [MPa] | pevnost XY [MPa] | bezpečnost krátkodobě | dlouhodobě (30 %) |
|---|---|---|---|---|---|
| A: 200 kPa, K0 = 1 | 0.2 | 1.3 | 40–55 | 32–44 | 9.5–13.1 |
| B: 1 MPa, K0 = 1 (horní mez) | 1.0 | 6.3 | 40–55 | 6–9 | 1.9–2.6 |
| B: 2 MPa (extrém) | 2.0 | 12.6 | 40–55 | 3–4 | 1.0–1.3 |

**Osové napětí ve stěně od tření** (táhne vrstvy od sebe, pokud je cela dole uchycená):

| případ | μ | třecí síla [kN] | osové napětí stěny [MPa] | pevnost Z [MPa] | bezpečnost |
|---|---|---|---|---|---|
| bez fólie (zmrzlá zemina–PETG) | 0.5 | 15.9 | 5.8 | 15–30 | 2.6–5.2 |
| PTFE fólie + silikonový tuk | 0.05 | 1.6 | 0.6 | 15–30 | 25.9–51.8 |

(boční tlak 1 MPa). Bez fólie je osové napětí přes vrstvy kritické → fólie + cela volně uložená (neupnutá), aby tření stěnu tlačilo, ne táhlo.

Rozdílná roztažnost cela/vzorek: α PETG-CF ≈ 30–60·10⁻⁶ 1/K → změna průměru při 20 K ≈ 0.06–0.12 mm (cela se při ochlazení zúží víc než Al píst ⌀99,5 – vůle pístu ≥ 0,3 mm).

## 5. Očekávaný zdvih (uzavřený systém, bez přítoku vody)

Zmrznutí vody v pórech na místě: 9 % × θ 0.3 × 100 mm ≈ **2.7 mm**. Otevřený systém (přítok vody zespodu, růst ledových čoček) dá víc – podle zeminy několik mm až cm. Rozsah LVDT ±10 mm a volný zdvih pístu 15 mm pokrývají oba případy.

## 6. Siloměry – rozsah a rozlišení

| použití | typ | rozsah | 1 kPa ≙ | tep. drift nuly (0,02 %FS/10 K) při 20 K |
|---|---|---|---|---|
| A: v sérii s pákou | S-snímač tah/tlak, C3, kompenz. −10…+40 °C | 2 kN | 7.9 N = 0.393 %FS | 0.8 N ≈ 0.1 kPa |
| B: nahoře | kompresní (kanystr/sloupek), vysoká tuhost | 20 kN | 7.9 N = 0.039 %FS | 8.0 N ≈ 1.0 kPa |
| B: dole pod podstavcem | kompresní, stejný typ | 20 kN | 7.9 N = 0.039 %FS | 8.0 N ≈ 1.0 kPa |
