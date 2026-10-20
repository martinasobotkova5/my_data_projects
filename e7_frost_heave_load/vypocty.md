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

