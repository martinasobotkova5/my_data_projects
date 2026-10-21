# E7 – návrhové výpočty

Generováno skriptem `src/vypocty.py` z `src/params.py`. Hodnoty ≈ jsou odhady k ověření.

## 1. Zatížení

Plocha vzorku ⌀100: 7854 mm² = 78.54 cm².

| varianta | napětí na povrchu [kPa] | síla [N] | hmotnost na vzorku [kg] |
|---|---|---|---|
| A – závaží | 5 | 39 | 4.0 |
| A – závaží | 10 | 79 | 8.0 |
| A – závaží | 15 | 118 | 12.0 |
| A – závaží | 20 | 157 | 16.0 |
| A – závaží | 25 | 196 | 20.0 |
| B – jen horní deska PETG-CF | 0.08 | 0.64 | 0.065 |

Ve variantě B nese písek jen lehkou desku (0.08 kPa) – to odpovídá vlastní tíze horních 5 mm písku (≈ 0.08 kPa). Kotvy s Invarovými tyčkami váží dohromady 17 g a visí každá na svém místě v písku. LVDT mají **volné jádro** (bez pružiny), takže na vzorek netlačí. Běžné LVDT s pružinou by přidaly ≈ 1–2 N na hrot, tj. 0,1–0,25 kPa na každý snímač.

## 2. Varianta B – očekávané deformace (uzavřený systém)

| θ [-] | Sr [-] | pórovitost n | vzduch n(1−Sr) | objem z mrznutí 0,09·θ | horní mez zdvihu [mm] |
|---|---|---|---|---|---|
| 0.11 | 0.3 | 0.38 | 0.27 | 0.010 | 1.0 |
| 0.15 | 0.4 | 0.38 | 0.23 | 0.014 | 1.4 |
| 0.19 | 0.5 | 0.38 | 0.19 | 0.017 | 1.7 |

Horní mez platí, jen kdyby se celé rozpínání vody při mrznutí projevilo svisle. V nenasyceném písku je ale vzduchových pórů mnohonásobně víc, než kolik objemu led přidá. Celkový zdvih bude proto malý (desetiny mm), ale **uvnitř vzorku se může voda přesouvat** k čelu promrzání (kryosukce): nahoře vrstva nabobtná, níž se vysuší a smrští. Proto se měří deformace **po vrstvách** (kotvy E1–E3), ne jen povrch. Při tání se ukáže nevratné sednutí (zhutnění) za každý cyklus.

## 3. Varianta B – rozlišení posunů a poměrných deformací

| vrstva | hloubka [mm] | tloušťka L0 [mm] | posun = rozdíl | rozlišení ε [–] |
|---|---|---|---|---|
| povrch – E1 | 0–25 | 25 | S̄ − E1 | 3.8e-05 |
| E1 – E2 | 25–50 | 25 | E1 − E2 | 3.8e-05 |
| E2 – E3 | 50–75 | 25 | E2 − E3 | 3.8e-05 |
| E3 – dno | 75–100 | 25 | E3 − 0 (dno pevné) | 2.7e-05 |

LVDT ±5 mm s výstupem ±5 V na rozsahu CR1000 ±5000 mV: rozlišení ≈ 0.67 µm. Poměrná deformace vrstvy 25 mm se tak rozliší na ≈ 4·10⁻⁵ (0,004 %). Absolutní linearita LVDT (±0,25 % FS ≈ ±25 µm) se odstraní kalibrací mikrometrem; pro deformace mezi cykly rozhoduje stabilita, ne linearita.

## 4. Varianta B – teplotní chyba referenčního stojanu

| prvek | délka [mm] | α [1/K] | změna při 20 K [µm] |
|---|---|---|---|
| Al distanční kus + podstavec | 70 | 23.1·10⁻⁶ | +32 |
| G10 mezikus | 10 | 15.0·10⁻⁶ | +3 |
| Invarové sloupky 250 mm | 250 | 1.2·10⁻⁶ | -6 |
| tělo LVDT (nerez) od upnutí k nule | 45 | 17.0·10⁻⁶ | +15 |
| horní deska PETG-CF | 6 | 45.0·10⁻⁶ | +5 |
| **zdánlivý posun povrchu** |  |  | **+50** |

Zdánlivý posun ≈ 50 µm za 20 K je malý proti očekávaným desetinám mm, ale ne zanedbatelný. Odstraní se **slepou zkouškou** s Al náhradou vzorku ve stejném programu (odečíst jako funkci teploty Tbot a Tbridge). Kotvy mají Invarové tyčky (100–160 mm × 1,2·10⁻⁶ × 20 K ≈ 3–4 µm), takže chyba vrstev je hlavně společná všem snímačům a v rozdílech mezi kotvami se odečte.

## 5. Cela z PETG-CF – napětí

| případ | boční tlak p [MPa] | obvodové napětí σθ [MPa] | pevnost XY [MPa] | bezpečnost krátkodobě | dlouhodobě (30 %) |
|---|---|---|---|---|---|
| A: 25 kPa, K0 = 1 | 0.025 | 0.16 | 40–55 | 253–349 | 76.0–104.6 |
| B: tlak ledu na stěnu 200 kPa (horní odhad) | 0.2 | 1.26 | 40–55 | 32–44 | 9.5–13.1 |
| extrém 1 MPa | 1.0 | 6.31 | 40–55 | 6–9 | 1.9–2.6 |

Cela je plná (jeden kus z 3D tisku), tištěná nastojato: obvodové napětí jde podél vláken.

**Tření o stěnu plné cely** – část přitížení odnese stěna (Janssen): σv(dno)/σv(povrch) = exp(−4·μ·K·H/D).

| rozhraní | μ | K | σv dno / povrch | A: σv u dna při 25 kPa [kPa] | osová síla do stěny [N] |
|---|---|---|---|---|---|
| PTFE fólie + silikonový tuk | 0.05 | 0.4 | 0.92 | 23.1 | 15 |
| PTFE fólie + silikonový tuk | 0.05 | 0.6 | 0.89 | 22.2 | 22 |
| PTFE fólie nasucho | 0.1 | 0.4 | 0.85 | 21.3 | 29 |
| PTFE fólie nasucho | 0.1 | 0.6 | 0.79 | 19.7 | 42 |
| bez fólie (písek–PETG) | 0.5 | 0.4 | 0.45 | 11.2 | 108 |
| bez fólie (písek–PETG) | 0.5 | 0.6 | 0.30 | 7.5 | 137 |

S PTFE fólií a tukem dojde ke dnu ≈ 90 % přitížení, bez fólie jen 30–40 %. Proto: fólie povinná a PV1 (40 mm) a PB1 (dno) vyhodnocovat jako profil σv(z), ne jako jednu hodnotu. Ve variantě B je přitížení nulové, tření je malé, ale **přimrznutí ledu ke stěně** může brzdit zdvih zmrzlé horní vrstvy; PTFE má ze všech běžných materiálů nejmenší adhezi ledu. Osové napětí ve stěně od tření (A, 25 kPa, bez fólie): 0.045 MPa – zanedbatelné.

Rozdílná roztažnost cela/vzorek: α PETG-CF ≈ 30–60·10⁻⁶ 1/K → změna průměru při 20 K ≈ 0.06–0.12 mm (cela se při ochlazení zúží víc než písek – boční tlak mírně vzroste; píst A má vůli ≥ 0,25 mm, horní deska B ≥ 0,5 mm).

## 6. Varianta A – zdvih pod přitížením

Horní mez při θ 0.18: 9 % × θ × 100 mm ≈ **1.6 mm**; v nenasyceném písku podstatně méně (viz §2). LVDT ±10 mm stačí s rezervou.

## 7. Varianta A – přitížení závažím (max. 25 kPa)

Kotouč ⌀150/18 × 36 mm = 4.92 kg, poloviční × 18 mm = 2.46 kg. Pevná část: píst se vším ≈ 1 kg + nosná deska 1.39 kg + vodicí tyč 0.36 kg = **2.75 kg ≈ 3.4 kPa** (nejmenší přitížení).

| přitížení [kPa] | celkem [kg] | plné kotouče | poloviční | doladit [kg] | výška kotoučů [mm] |
|---|---|---|---|---|---|
| 5 | 4.0 | 0 | 0 | 1.25 | 0 |
| 10 | 8.0 | 1 | 0 | 0.33 | 36 |
| 15 | 12.0 | 1 | 1 | 1.88 | 54 |
| 20 | 16.0 | 2 | 1 | 0.96 | 90 |
| 25 | 20.0 | 3 | 1 | 0.04 | 126 |

Doladění tenkými kotouči / podložkami; celkovou hmotnost všeho, co leží na vzorku, zvážit.

| tepelná setrvačnost závaží (25 kPa) | hodnota | poznámka |
|---|---|---|
| tepelná kapacita závaží | 8.7 kJ/K | vzorek ≈ 1.6 kJ/K |
| časová konstanta (volná konvekce h ≈ 5 W m⁻² K⁻¹) | 5.5 h | bez izolace kotoučů |
| zpoždění teploty závaží při rampě programu | 0.57 K | rampa 0.10 K/h (Set A) |

Závaží za vzduchem v mrazáku zaostává jen o desetiny kelvinu, protože program mění teplotu pomalu. Mezikus G10 ⌀60 × 10 pod nosnou deskou omezí tok tepla ze závaží do vzorku; teplotu závaží logovat (Tw).

## 8. Bod M – TDR, Pt100 a optické čidlo ve stejném místě (obě varianty)

| stav písku | εa (≈) | dvojí doba běhu t [ns] | Δεa při Δt 12 ps | Δθ (Topp, ≈) |
|---|---|---|---|---|
| suchý | 3 | 0.46 | 0.16 | 0.004 |
| θ 0,10 | 6 | 0.65 | 0.22 | 0.005 |
| θ 0,18 | 10 | 0.84 | 0.29 | 0.006 |
| zmrzlý, nezamrzlá voda ≈ 0,02 | 4 | 0.53 | 0.18 | 0.005 |

Tyčky 40 mm jsou na hranici – krátká doba běhu. Proto: průměrovat více průběhů, kalibrovat sondu přímo v tomto písku (několik vlhkostí, +10 °C) a pro zmrzlý stav použít kalibraci nezamrzlé vody (Spaans & Baker 1995; Watanabe & Wake 2009). Citlivý objem 3-tyčkové sondy sahá ≈ 1–1,5× rozteč (5 mm) od tyček; Pt100 a FBG jsou 12 mm stranou, takže měření TDR téměř neovlivní.

| čidlo | přesnost | rozlišení na CR1000 / převodníku | poznámka |
|---|---|---|---|
| Pt100 1/10 DIN, 4vodič, 4WPB100 | ±0,03 °C při 0 °C | ≈ 0,01 °C (BrHalf4W, 2500 mV) | reference pro FBG a T3 |
| FBG v kapiláře ⌀1 | ±0,2–0,5 °C po kalibraci | ≈ 0,05–0,1 °C (≈ 10 pm/K, 1 pm) | kapilára = bez vlivu deformace |
| termistor 109SS (T3, 4 mm výš, r 40) | ±0,38 °C při 0 °C | ≈ 0,01 °C | porovnání s Pt100 → korekce |

Všechny tři prvky leží v hloubce 54 mm, kolem r ≈ 25 mm, v pásu ±12 mm do strany (TDR tyčky nad sebou ±5 mm), takže měří stejnou vrstvu ve stejný okamžik promrzání. Pt100 je teplotní reference: přes ni se kalibruje FBG i termistor T3 přímo v cele (ledový bod při tání), a TDR se vztahuje k teplotě Pt100 → křivka nezamrzlé vody θu(T) (charakteristika mrznutí písku).

## 9. Varianta A-min – maximálně zjednodušená varianta A

Pevná část: Al píst 0.84 kg + tyč M16 0.27 kg = **1.11 kg ≈ 1.4 kPa**. Kotouče: plný 4.92 kg, poloviční 2.46 kg, čtvrtkotouč 9 mm 1.23 kg.

| přitížení [kPa] | celkem [kg] | plné 36 | poloviční 18 | čtvrtkotouče 9 | doladit podložkami [kg] | výška kotoučů [mm] |
|---|---|---|---|---|---|---|
| 5 | 4.0 | 0 | 1 | 0 | 0.43 | 18 |
| 10 | 8.0 | 1 | 0 | 1 | 0.75 | 45 |
| 15 | 12.0 | 2 | 0 | 0 | 1.06 | 72 |
| 20 | 16.0 | 3 | 0 | 0 | 0.14 | 108 |
| 25 | 20.0 | 3 | 1 | 1 | 0.45 | 135 |

**Stabilita bez rámu.** Píst je v cele veden na délce ≈ 25 mm s vůlí 0,5 mm (na průměr). Největší náklon ≈ atan(0,5/25) ≈ 1,1°. Těžiště 20 kg je ≈ 100 mm nad povrchem písku, takže se při plném náklonu posune o ≈ 2 mm – daleko uvnitř opěrné plochy ⌀100. Klopný moment ≈ 196 N × 2 mm = 0,4 N·m přenese stěna dvojicí sil ≈ 16 N; s třením Al–PTFE (μ ≈ 0,2) to je ≈ 3 N, tj. ≈ 0,4 kPa (1,6 % z 25 kPa). Rám tedy není potřeba; kotouče se jen musí nasazovat opatrně a souose (středicí osazení na kotoučích).

**Čidla – konkrétní typy a orientační ceny (EUR bez DPH)**

| tag | měří | typ | ks | cena/ks | celkem | zdroj ceny |
|---|---|---|---|---|---|---|
| PV1, PB1 | svislé napětí v písku / u dna | TML PDA-PA 200 kPa (⌀6.5 × 1 mm) | 2 | 600–1 000 | 1 200–2 000 | odhad |
| Pt100 | referenční teplota v bodě M | Omega PM, Pt100 1/10 DIN, 4-wire, ⌀3.2 × 150 mm | 1 | 230–260 | 230–260 | web |
|  | doplňkový modul k Pt100 | Campbell 4WPB100 | 1 | 60–120 | 60–120 | odhad |
| TDR | vlhkost / nezamrzlá voda v bodě M | Campbell TDR200 (reflectometer) | 1 | 4 500–5 200 | 4 500–5 200 | web |
|  | sonda TDR | TDR probe, custom 3 rods ⌀1.6 × 40 + RG58 1 m | 1 | 50–150 | 50–150 | odhad |
| OPT | optická teplota v bodě M | Opsens OTG-F (fluorescent, ⌀0.15 mm) | 1 | 300–600 | 300–600 | odhad |
|  | převodník k OPT | Opsens TempSens 4-ch., ±5 V output | 1 | 3 500–6 000 | 3 500–6 000 | odhad |
| LVDT | kontrola, že se vzorek nehýbe | RDP DCTH400AG (±10 mm, spring) | 1 | 581 | 581 | web |
|  | zdroj pro LVDT | DIN-rail power supply for the LVDT | 1 | 40–80 | 40–80 | odhad |
| T1, T2, Tair | teplota písku 20/80 mm, vzduch | Campbell 109SS-L (⌀1.6 mm) | 3 | 180–260 | 540–780 | odhad |

| mechanika | cena |
|---|---|
| cela PETG-CF (≈ 0,4 kg filamentu) + epoxid | 30–60 |
| PTFE fólie 0,5 mm + silikonový tuk | 25–50 |
| Kaiflex 25 mm samolepicí, ≈ 0,3 m² | 10–20 |
| G10 kotouč ⌀150 × 10 | 25–50 |
| Al deska 200 × 200 × 10, Al dno ⌀150 × 15, Al píst ⌀99,5 × 40 (obrobení) | 120–250 |
| ocelové kotouče ⌀150: 3 × 36 + 1 × 18 + 1 čtvrtkotouč 9 mm (≈ 20 kg, pálení + vrtání) | 150–300 |
| závitová tyč M16, nerezový sloupek ⌀12, objímka LVDT | 20–50 |

| | čidla | mechanika | **celkem** |
|---|---|---|---|
| EUR bez DPH | 11 001–15 771 | 380–780 | **11 381–16 551** |
| Kč bez DPH (≈ 25 Kč/€) | 275–394 tis. | 10–20 tis. | **285–414 tis.** |

CR1000 se nepočítá (už je k dispozici). Největší položky jsou TDR200 a převodník optického čidla – dohromady ≈ 75 % ceny čidel.

