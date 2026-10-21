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

## 9. Varianta A-min – zjednodušená A s nehybným (pevným) omezením

Vzorek je nahoře sevřen ocelovým víkem na 3 táhlech; píst dosedne středovým šroubem s dosedacím předpětím 5 kPa a pak se nic nehýbe. Tlak, který při mrznutí vznikne, měří PV1 a PB1.

| při 1000 kPa (F = 7.85 kN) | hodnota | poznámka |
|---|---|---|
| tah v 1 táhle M10 | 2.62 kN | napětí 45 MPa (A4-70: mez kluzu 450 MPa) |
| protažení táhel (L ≈ 216 mm) | 49 µm |  |
| průhyb víka ⌀240 × 15 (podepřeno na r 92) | 54 µm | napětí ≈ 70 MPa (S235: 235 MPa) |
| **celkový posun pístu** | **103 µm** | při 200 kPa pětkrát méně |

Omezení je tedy prakticky nehybné: i při 1 MPa se píst posune o ≈ 0,1 mm, při realistických stovkách kPa o desítky µm. Skutečný posun ukazuje LVDT na víku.

**Teplotní roztažnost** (táhla nerez vs. vnitřní sestava: tištěné dno 26 + písek + Al píst + šroub):

|  | změna při 20 K [µm] |
|---|---|
| táhla nerez | 69 |
| vnitřní sestava | 67 |
| **rozdíl** | **+2** |

Táhla a vnitřní sestava se při ochlazení zkracují téměř stejně, takže teplota sama vzorek nestlačí ani neuvolní (na rozdíl od původní varianty B s Al rámem). Zbytek ukáže slepá zkouška s Al náhradou.

**Co je potřeba koupit (EUR bez DPH, orientačně)**

| tag | měří | typ | ks | celkem | zdroj ceny |
|---|---|---|---|---|---|
| PV1, PB1 | svislé napětí v písku / u dna | TML PDA-PA 500 kPa (⌀6.5 × 1 mm) [U] | 2 | 1 200–2 000 | odhad |
| LVDT | kontrola, že se víko nehýbe | RDP DCTH400AG (±10 mm, spring) | 1 | 581 | web |
|  | zdroj pro LVDT | DIN-rail power supply for the LVDT | 1 | 40–80 | odhad |
| T1, T2, Tair | teplota 20/80 mm, vzduch (volitelně) | Campbell 109SS-L (⌀1.6 mm) | 3 | 540–780 | odhad |

| mechanika | cena |
|---|---|
| tištěná cela ⌀160 × 160 podle výkresu Column_one_body (slicer ≈ 600 g PETG, 21 h, ≈ 18 €) + epoxid | 25–50 |
| kluzný PTFE sprej + silikonový tuk na vnitřní stěnu | 15–30 |
| Al deska 230 × 230 × 20, Al píst ⌀99,5 × 40 (obrobení) | 150–300 |
| ocelové víko ⌀230 × 15 (pálení, 4 otvory, závit M16 × 1,5) | 60–120 |
| 3 táhla M10 nerez A4 + matice a podložky, šroub M16 × 1,5 + pojistná matice | 25–50 |
| nerezový sloupek ⌀12 + objímka LVDT | 15–40 |

| | čidla | mechanika | **celkem** |
|---|---|---|---|
| EUR bez DPH | 2 361–3 441 | 290–590 | **2 651–4 031** |
| Kč bez DPH (≈ 25 Kč/€) | 59–86 tis. | 7–15 tis. | **66–101 tis.** |

Bez ceny (už máte): TDR, teplotní čidlo a optické vlákno v bodě M, datalogger CR1000. Termistory T1, T2, Tair jsou volitelné.

## 10. Varianta A-rám – nehybné omezení v rámu z Al profilů

Stejné jako A-min (tištěná cela ⌀160 podle výkresu Column_one_body), jen místo víka na táhlech drží píst rám: 2 sloupy 40×80 a příčník 80×80, v příčníku šroub M16 × 1,5, mezi šroubem a pístem Al sloupek ⌀40 a vložka POM-C.

| při 1000 kPa (F = 7.85 kN) | posun [µm] | poznámka |
|---|---|---|
| průhyb příčníku 80×80, rozpětí 220 | 18 | prostý nosník |
| protažení 2 sloupů 40×80 × 245 | 13 |  |
| stlačení Al sloupku 51 + POM 8 | 21 | POM E ≈ 3 GPa |
| spoje profilů (šrouby do čela) | 10–80 | rozhoduje – dotáhnout momentem |
| **celkem** | **62–132** | při 200 kPa pětkrát méně |

**Teplotní roztažnost** – Al sloupy se při ochlazení zkrátí víc než vnitřní sestava (písek má menší α), takže by rám vzorek stlačil. Vložka POM-C (α ≈ 110·10⁻⁶) to vyrovná:

|  | sloupy − sestava při 20 K [µm] | falešný tlak (zmrzlý písek) [kPa] |
|---|---|---|
| Al sloupek 59 mm (bez POM) | +14 | 23 |
| Al 51 + POM 8 mm | -0 | -0 |

Tuhost rám ≈ 81 kN/mm, zmrzlý vzorek ≈ 16 kN/mm (E = 200 MPa). α zmrzlého písku je odhad – zbytek se odečte ze **slepé zkoušky** s Al náhradou vzorku ve stejném programu.

**Mechanika A-rám (EUR bez DPH, odhad)**

| položka | cena |
|---|---|
| tištěná cela ⌀160 × 160 podle výkresu Column_one_body (slicer ≈ 600 g PETG, 21 h, ≈ 18 €) + epoxid | 25–50 |
| kluzný PTFE sprej + silikonový tuk na vnitřní stěnu | 15–30 |
| Al profily: 2× 40×80 × 245 + 80×80 × 260 (řezané), krytky | 50–100 |
| 4 šrouby do čela M12 + 4 šrouby M10 do desky, vrtání | 20–50 |
| Al deska 260 × 200 × 25, Al píst ⌀99,5 × 40, Al sloupek ⌀40 × 51 (obrobení) | 180–350 |
| vložka POM-C ⌀40 × 8 | 5–15 |
| šroub M16 × 1,5 + pojistná matice, závitové pouzdro v příčníku | 20–40 |
| nerezový sloupek ⌀12 + objímka LVDT, terčík na sloupku | 20–45 |

Čidla stejná jako A-min (2 361–3 441 €). **Celkem ≈ 2 696–4 121 € (≈ 67–103 tis. Kč) bez DPH**; TDR, teplotní čidlo, optické vlákno a CR1000 už máte.

## 11. Tištěná cela A (Column_one_body_version_1) – kontrola

Tělo ⌀160 × 130, límec ⌀106 do 160 mm, dutina ⌀100, dno 26 mm, písek 100 mm, nad ním 34 mm pro píst. Plášť vytištěný s 10 % výplní slouží zároveň jako tepelná izolace.

| případ | 200 kPa | 1 MPa | poznámka |
|---|---|---|---|
| obvodové napětí, jen vnitřní stěna 3 mm | 3.3 MPa | 16.7 MPa | PETG(-CF) 40–55 MPa krátkodobě, ≈ 12–16 MPa dlouhodobě |
| obvodové napětí, stěna kolem dutiny 5 mm (≈ 8 perimetrů) | 2.0 MPa | 10.0 MPa | PETG(-CF) 40–55 MPa krátkodobě, ≈ 12–16 MPa dlouhodobě |
| tlak na dno (= tlak v písku) | 0,2 MPa | 1,0 MPa | 10 % gyroid ≈ 1–2 MPa pevnost v tlaku → pod dutinou 100 % výplň |

Doporučení pro tisk: kolem dutiny stěnu ≈ 5 mm (≈ 8 perimetrů), pod dutinou (z 0–26) 100 % výplň (modifikátor v PrusaSliceru), zbytek pláště 10 % (izolace). Pak cela snese i horní odhad 1 MPa.

