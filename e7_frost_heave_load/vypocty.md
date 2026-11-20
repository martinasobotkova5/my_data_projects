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
| tištěné dno cely 26 mm (PETG) | 26 | 45.0·10⁻⁶ | +23 |
| Invarové sloupky 196 mm | 196 | 1.2·10⁻⁶ | -5 |
| tělo LVDT (nerez) od upnutí k nule | 45 | 17.0·10⁻⁶ | +15 |
| horní deska PETG-CF | 6 | 45.0·10⁻⁶ | +5 |
| **zdánlivý posun povrchu** |  |  | **+39** |

Zdánlivý posun ≈ 39 µm za 20 K je malý proti očekávaným desetinám mm, ale ne zanedbatelný. Odstraní se **slepou zkouškou** s Al náhradou vzorku ve stejném programu (odečíst jako funkci teploty Tbot a Tstand). Kotvy mají Invarové tyčky (100–160 mm × 1,2·10⁻⁶ × 20 K ≈ 3–4 µm), takže chyba vrstev je hlavně společná všem snímačům a v rozdílech mezi kotvami se odečte.

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

Horní mez při θ 0.19: 9 % × θ × 100 mm ≈ **1.7 mm**; v nenasyceném písku podstatně méně (viz §2). LVDT ±10 mm stačí s rezervou.

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

## 12. Varianta B-open – nejjednodušší sestava, otevřený povrch

Tištěná cela ⌀160 na Al desce, bod M (CS645 + vlákno + Pt100 – už máte), na povrchu písku jen malý terčík ⌀30 × 2 s jedním LVDT s volným jádrem na Invarovém sloupku. Žádné víko, horní deska, kotvy ani můstek.

**Přítlak terčíku na písek:** ≈ 18 g na ⌀30 → ≈ 0.25 kPa jen pod terčíkem; zbytek povrchu je volný.

| prvek | délka [mm] | změna při 20 K [µm] |
|---|---|---|
| tištěné dno cely 26 mm | 26 | +23 |
| Invarový sloupek ≈ 235 mm | 235 | -6 |
| Invarová tyčka jádra ≈ 110 mm | 110 | -3 |
| tělo LVDT od upnutí k nule | 45 | +15 |
| **zdánlivý posun povrchu** |  | **+30** |

Odečte se slepou zkouškou (Al náhrada vzorku). S nerezovou tyčkou jádra místo Invarové by chyba vzrostla o ≈ 35 µm.

**Otevřený povrch a vysychání:** v mrazáku písek z povrchu pomalu sublimuje/vysychá (u mrazáků s odmrazováním rychleji). Celu vážit na začátku a po každém cyklu (váha 5 kg / 0,1 g); pokud ztráta přesáhne ≈ 1 % vody, dát nad celu volný stan z fólie (nedotýká se povrchu, povrch zůstane otevřený).

**Co koupit:** LVDT s volným jádrem + zdroj, Invarový sloupek s ramenem, Al deska, terčík; volitelně Tair. Celkem ≈ 830–1250 € bez DPH (≈ 21–31 tis. Kč).

## 13. Varianta B-open – bezkontaktně: kamera shora + čárový laser

Na povrchu písku nic neleží. Čárový laser svítí šikmo (45° od svislice) přes celý povrch a přes horní hranu límce; kamera shora snímá čáru. Když povrch stoupne o Δh, čára se v obraze posune do strany o Δh·tan 45° = Δh. Zorné pole ≈ 115 mm → **28 µm/px**; s vyhodnocením těžiště čáry (≈ 0,1–0,3 px) ≈ 3–9 µm, reálně ≈ 10 µm (zrnitost písku, námraza).

Čára dává celý **profil povrchu** napříč vzorkem (střed i okraj u stěny), ne jen jeden bod. Druhý laser otočený o 90° (+15–60 €) přidá druhý profil.

**Reference = čára na horní hraně límce** ve stejném snímku – ruší pohyb kamery i laseru. Límec se ale sám posune o ≈ 121 µm na 20 K → odečíst ze **slepé zkoušky** (Al náhrada vzorku).

**Kamera a laser v mrazáku:** oba v izolovaném boxu (XPS 30 mm) s topnou fólií 5 W a termostatem na +5 °C, okénka ze dvou skel. Teplo boxu nad vzorkem je malé (≈ 1 W přes izolaci a okénko), ale vliv ověřit termistorem Ttop / bodem M ve slepé zkoušce; lepší je kamera mimo mrazák s okénkem ve víku, pokud to víko dovolí. Laser zapínat jen na snímek (každých 10 min), jinak tma; čas synchronizovat s CR1000.

**Cena:** ≈ 457–770 € bez DPH (≈ 11–19 tis. Kč).

## 14. Varianta C – kombinace: Al rám vede mrtvou váhu, částečný píst, kamera nad volným povrchem

Píst ⌀50 (plocha 1963 mm² = 25 % vzorku), volné mezikruží 25 mm kolem něj. Pohyblivá část bez závaží: píst Al 106 g + kulička + tyč ⌀12 × 159 141 g + Al nosná deska 249 g = **0.50 kg ≈ 2.5 kPa** (nejmenší přitížení pod pístem).

| napětí pod pístem [kPa] | celkem [kg] | kotouče 1 kg | 0,5 kg | doladit [kg] |
|---|---|---|---|---|
| 5 | 1.00 | 0 | 1 | 0.00 |
| 10 | 2.00 | 1 | 1 | 0.00 |
| 15 | 3.00 | 2 | 1 | 0.00 |
| 20 | 4.00 | 3 | 1 | 0.00 |
| 25 | 5.00 | 4 | 1 | 0.01 |

Kotouč ⌀165/6.6: 1 kg = 6.0 mm, 0,5 kg = 3.0 mm. Při 25 kPa jen ≈ 4 kotouče.

**Konstantní zatížení:** zátěž leží jen na pístu a s povrchem volně stoupá i klesá (zdvih ±5 mm). Kluzné pouzdro igus drylin RJ4JP-01-12 (bez maziva, do −40 °C) má tření ≈ 0,1–0,25 × boční síla; při náklonu tyče 0,5° je boční síla < 0,1 N → změna zatížení < 0,02 kPa. Kulička mezi tyčí a pístem dovolí pístu se naklonit, tyč zůstává svislá.

**Co se měří (jen 1 + 2):** (1) kamera + vícečárový laser 60° (11 čar po ≈ 13.1 mm, posun čáry = 0.58 × zdvih) → mapa výšek **celého povrchu** ⌀100 v každém snímku: volné mezikruží i horní plocha pístu, reference = invarový terčík u límce; (2) LVDT na rameni invarového sloupku pod nosnou deskou = pohyb zátěže (pístu), rozlišení ≈ 1 µm. Tlakové snímače nejsou potřeba – zatížení je známá mrtvá váha.

**Rozměry:** sloupy 40×80 × 276 mm, spodní líc příčníku 130 mm nad pískem (místo pro kameru a laser), závaží nad příčníkem mimo zorné pole. Pt100 jde ze strany TDR otvorem a nasedá uprostřed přímo nad horní tyčku CS645 (hloubka ≈ 33 mm) – povrch zůstává volný.

## 15. Varianta C rev. B – posudek měření (10/2026, přepočteno pro Sr = 0,5 v 11/2026)

**Očekávaný zdvih (rozhodnuto Sr = 0.5):** pórovitost ≈ 0.38, θ = 0.19; vzduch v pórech 19 % objemu, objem ledu přibude jen o 1.7 % → v uzavřeném vzorku se rozpínání vejde do pórů, zdvih in situ ≈ 0 (desítky µm nanejvýš od migrace vody). Horní mez (vše nahoru) 1.71 mm. E7 tedy měří hlavně sednutí při tání pod zatížením; pro měření zdvihu by bylo nutné Sr ≥ 0,85 nebo voda zespodu.

**Směr mrznutí (sim_thaw.py, Sr 0,5):** cela přímo na Al desce – 95 % zmrzne za ≈ 10,5 h i zespodu, poslední nezmrzlé místo 35 mm nade dnem; rev. B (cela tištěná vcelku ⌀220 × 200: stěna 30 mm a dno 40 mm z nízké výplně λ ≈ 0,06, podložky G10 v kapsách) – 95 % zmrzne za ≈ 14,5 h, celý vzorek za ≈ 15 h, poslední nezmrzlé 13 mm nade dnem → mrznutí shora. Tání ≈ 14,5 h → cyklus 24 h + 24 h stačí (rezerva ≈ 9 h). Stěna 40 / 30 / 25 mm (⌀240 / 220 / 210): 95 % zmrzne za 15,0 / 14,5 / 14,25 h, poslední nezmrzlé místo vždy 13 mm nade dnem na ose – stěna 30 mm stačí a cela ⌀220 se vejde na podložku tiskárny 24 cm.

**Tepelný drift sestavy (20 K, sim_thaw.py, zbytek = po korekci podle teplot cely ze slepé zkoušky):** rev. A (bez izolace, LVDT na Al příčníku, ocelová tyč) −24…+48 µm, zbytek ≤ 12 µm; kamera vůči PETG límci 0…100 µm, zbytek ≤ 8 µm. Jen izolace bez Invaru by zbytek LVDT zhoršila na 57 µm (cela reaguje pomaleji než sloupy a tyč). Rev. B (izolace + invarový sloupek + invarová tyč) −59…0 µm, zbytek ≤ 6 µm; kamera vůči invarovému terčíku −49…0 µm, zbytek ≤ 3 µm. Zbylý drift = PETG dno 26 mm + písek → změřit slepou zkouškou s Al atrapou.

**Další změny:** RPi 5 v boxu s kamerou (žádný plochý kabel přes těsnění, jeho teplo drží okénko bez námrazy); snímek spouští CR850 (C4); kluzné pouzdro drylin místo kuličkového; čidlo vzduchu 109 povinně; ventilátor 80 mm; vážení cely před/po cyklu a RH vzduchu (SHT45) kvůli vymrzání a námraze; kalibrace kamery podložkami 0,1/0,5/1,0 mm.

## 16. Varianta C rev. B3 – rám z T-profilů (11/2026)

**Rám:** jen hliníkové T-profily drážka 8 řezané na délku – 2 podélníky 40×40 × 260, příčka 40×80 × 260 naplocho (nese 3 podložky G10), 2 sloupy 40×80, horní příčník 40×80 × 340 s jediným otvorem ⌀14; pouzdro ložiska visí pod příčníkem, mezera nad pískem 130 mm. Hliníkové desky L01/L02 odpadly. Rám zátěž jen vede, měření se k rámu nevztahuje (LVDT i terčík kamery jsou na invarovém sloupku), takže drift po korekci zůstává ≤ 6 µm (LVDT) a ≤ 3 µm (kamera).

**Pt100 (potvrzeno):** vodorovně ze strany TDR, osa 3.5 mm nad osou horní tyčky CS645, hrot 30 mm od vnitřní stěny.

**Vzorek (rozhodnuto):** Sr = 0.5, θ = 0.19 (n ≈ 0.38).

## 17. Rám z T-profilů – únosnost, tuhost a stabilita (rev. B3, 11/2026)

Hmotnosti: rám 4.3 kg, mrtvá váha až 5.5 kg, písek 1.41 kg (Sr 0.5), cela 1.5 kg, ostatní 1.3 kg → celkem ≈ 14.0 kg. Výška tlaku na T04 nad podlahou 378 mm. Průřezy: konzervativní odhady pro lehké profily drážka 8 (40×80: I_slabá ≈ 12 cm⁴, 40×40: I ≈ 7 cm⁴) – ověřit v technickém listu dodavatele. Součinitel zatížení 1,5, návrhová pevnost 160 MPa.

| stav | zatížení | výsledek |
|---|---|---|
| ZS2 mimořádný: celá mrtvá váha na příčníku T04 (kroužek dosedne) | 54 N uprostřed | σ = 1.0 MPa, průhyb 3.6 µm |
| ZS3 nesprávné použití: 500 N svisle na T04 (opření, odložená závaží) | 500 N uprostřed | σ = 9.4 MPa, průhyb 33 µm |
| ZS1 provoz: cela + písek + závaží na příčce T03 (3 podložky u středu) | 83 N | σ = 1.6 MPa, průhyb 5.6 µm |
| změna zatížení o 1 kg kotouč → změna průhybu T03 (jde do LVDT) | 9.8 N | 0.66 µm |
| sloup 40×80 tlak (ZS3) vs. Eulerova kritická síla (konzola) | 375 N | N_cr = 272 kN |
| úhelník 40 drážka 8, smyk na 1 úhelník (příčka T03, 4 ks) | 21 N | tření spoje M8 (předpětí ≈ 6 kN × 0,2) ≈ 1,2 kN → bez prokluzu |
| T-matice M5 pouzdra P01 (4 ks) – zatěžuje je jen tření v pouzdře | < 1 N | typ. únosnost T-matice M5 ≥ 500 N |
| překlopení ve směru y – vodorovná síla na T04, rev. B3 původně (podélníky 260, nohy ±110) | G = 138 N | H_krit ≈ 40 N |
| překlopení ve směru y – vodorovná síla na T04, nyní (podélníky 320, nohy ±140) | G = 138 N | H_krit ≈ 51 N |
| překlopení ve směru x (nohy ±150) |  | H_krit ≈ 55 N |

**Závěr:** napětí v profilech jsou desetiny až jednotky MPa (rezerva > 20×), průhyby jednotky µm. Rám zátěž jen vede, takže jeho únosnost nerozhoduje; profil 40×80 je zvolen kvůli tuhosti spojů a ploše pro úhelníky, ne kvůli pevnosti. **Rozhoduje stabilita proti překlopení:** s nožkami ±110 by stačil vodorovný tlak ≈ 40 N na horní příčník (např. při nasazování kotoučů). Proto podélníky 320 mm a nohy ±140; v mrazáku rám stojí ve vaně (opře se o stěnu), mimo mrazák manipulovat se závažím jen při přidrženém rámu. Prokluz spojů pod konstantním zatížením nehrozí; při výměně kotoučů se změní průhyb příčky T03 o < 1 µm (jde do LVDT, zanedbatelné).

## 18. Datalogger CR850 – zapojení bez multiplexoru (11/2026)

CR850 (= CR800 s klávesnicí a displejem): 6 SE / 3 DIFF analogových vstupů, buzení VX1–VX2, porty C1–C4 (při SDM jsou C1–C3 vyhrazené pro TDR) a výstup 12 V. Zjednodušená sestava potřebuje jen 3 teploty, takže se vše vejde přímo do CR850 bez multiplexoru a port C4 zůstane na spouštění snímku (jedna časová značka pro všechna data). Zdroj LVDT a ventilátor trvale zapnuté. LVDT diferenciálně: rozsah ±5000 mV, rozlišení ≈ 0,67 mV = 1,3 µm při 0,5 V/mm, průměrováním 20–50 vzorků ≈ 0,5 µm.

| svorka CR850 | připojeno | měření |
|---|---|---|
| DIFF1 (1H/1L) | (2) LVDT DCTH400AG | VoltDiff ±5000 mV, průměr 20–50 vzorků |
| DIFF2 (2H/2L) + VX2 | Pt100 v písku (bod M) přes 4WPB100 | BrHalf4W, 2500 mV |
| SE5 + VX1 | Tair Campbell 109 (vzduch = okrajová podmínka) | Therm109 |
| SE6 + VX1 | NTC 10 kΩ ve dně cely (+ odpor 10 kΩ 0,1 %) | BrHalf → teplota dna pro korekci driftu |
| C1–C3 | TDR100/TDR200 → CS645 | SDM |
| C4 | impuls → optočlen → GPIO RPi | spouští snímek + laser |
| 12 V + G | ventilátor 80 mm (trvale) | – |
| – | LVDT z vlastního zdroje 24 V (trvale) | – |

## 19. Laser podle nabídky Picotronic A2627918 (13. 11. 2026)

DOE-DER253: úhel mezi čarami 3.1°, vějíř 31° (dříve odhadováno 3,8° / 41°). Z původní polohy (134 mm, 68°) by čáry byly dlouhé jen 74 mm po 7.8 mm → nepokryly by povrch ⌀100. **Nová poloha:** laser vedle horního příčníku, 105 mm od osy, 182 mm nad pískem, vzdálenost 210 mm, sklon 60° → čáry ≈ 117 mm dlouhé po ≈ 13.1 mm, na písku ⌀100 ≈ 9 čar, límec ⌀106 pokrytý; posun čáry = 0.58 × zdvih. Držák P05 přepracován (blok mimo poloměr nosné desky 70 mm). Krajní čára u stěny na straně kamery je uprostřed zastíněná pouzdrem ložiska (krátká tětiva, zanedbatelné). Doporučen modul DOE253-635-5-6(10x24) s nastavitelným ohniskem (zaostřit na 200 mm) a 5 mW – rezerva pro tmavý mokrý / zmrzlý písek a krátkou expozici; třída 2M: nedívat se do svazku optickými přístroji.

## 20. Zjednodušení pro měření (15. 11. 2026)

Sestava posouzená očima toho, kdo ji staví a měří: **jediná pohyblivá část je zátěž**. Průběžně (každých 10 min, kolem 0 °C každou minutu) měří LVDT (sednutí / zdvih pod pístem, ≈ 1 µm), pevná kamera s laserem 11 čar (výšky volného povrchu, ≈ 10 µm), Pt100 a TDR v bodě M, teplota vzduchu a teplota dna cely. **3D model povrchu** se dělá ručně fotogrammetrií jen v klíčových stavech (před zmrazením, zmrzlý na konci fáze −10 °C, po roztátí, konec série): 30–50 snímků dokola kolem otevřené cely, měřítko a kódové značky na límci → model z celých 360°, bez stínu za pístem. Vypuštěno: motorový posuv kamery, LED osvětlení, multiplexor a 10 termistorů, volitelný teplotní profil v písku, fotky podle NTP. Úspora ≈ 100–130 €, 2 tištěné díly (P12, P13) a většina zapojení a programování.

## 21. Sublimace ledu pod částečným krytem – hlavní nová série (16. 11. 2026)

Nasycená pára nad ledem při −10 °C: 2.14 g/m³. Tok z volné plochy J = h_m · ρ_sat · (1 − RH), h_m = h / (ρ c_p Le^(2/3)) z přestupu tepla h (vzduch v truhle s ventilátorem 3–12 W/m²K).

| h [W/m²K] | RH | tok [kg/m²·den] | čistý led [mm/den] | mezikruží ⌀100/⌀50 [g/den] |
|---|---|---|---|---|
| 3 | 0.8 | 0.10 | 0.10 | 0.6 |
| 3 | 0.5 | 0.24 | 0.26 | 1.4 |
| 3 | 0.3 | 0.33 | 0.36 | 2.0 |
| 7 | 0.8 | 0.22 | 0.24 | 1.3 |
| 7 | 0.5 | 0.56 | 0.61 | 3.3 |
| 7 | 0.3 | 0.78 | 0.85 | 4.6 |
| 12 | 0.8 | 0.38 | 0.42 | 2.2 |
| 12 | 0.5 | 0.95 | 1.04 | 5.6 |
| 12 | 0.3 | 1.34 | 1.46 | 7.9 |

**Suchá vrstva (lag):** jakmile led z povrchu zmizí, pára prochází suchou vrstvou tloušťky L: J ≈ D_eff · Δρ / L, D_eff ≈ 5.3e-06 m²/s. Hranice ledu pak postupuje jako L = √(2 D_eff Δρ t / (ρ_led θ_led)).

| vzorek | led v objemu | L po 2 dnech | L po 14 dnech | L po 30 dnech | pokles volného povrchu po 14 dnech |
|---|---|---|---|---|---|
| pórový led (Sr ≈ 1, bez přebytku) | 0.38 | 2.4 mm | 6.3 mm | 9.2 mm | 0.00 mm |
| přebytek ledu (zrna 40 %, led 60 %) | 0.60 | 1.9 mm | 5.0 mm | 7.3 mm | 1.77 mm |

**Pod pístem** led nesublimuje (kryt), páru může odvést jen boční difuze od okraje pístu → vznikne **podstavec**: volné mezikruží klesá (laser), píst zůstává (LVDT). Tečení ledu pod pístem při 25 kPa za 30 dní je řádově 1.4 µm (Glenův zákon) – zatížení samo pokles neudělá, srovnání 3,5 a 25 kPa ukáže jen jeho vedlejší vliv. **Měřitelnost:** u písku s přebytkem ledu klesne volný povrch o desetiny mm za několik dní a o mm za týdny – laser (≈ 10 µm) ho zachytí den po dni; u pórového ledu pokles téměř nulový (kontrolní vzorek: suchá vrstva vznikne, kostra zrn stojí). Teplota se během sublimační série nemění (−10 °C), takže teplotní drift sestavy je prakticky nulový. Odhady ověří první 3 dny série (pokles volného povrchu laserem).

## 22. Fáze 1 bez zatížení – varianta U (16. 11. 2026)

*Pozn.: tento oddíl počítá s pevnou kamerou (HQ + 6 mm). Platí výsledky pro nízkou celu a laser; kamera nyní obíhá – její zorné pole a viditelnost jsou v §23.*

Bez pístu a zátěže je celý povrch ⌀100 volný. Aby ho kamera i laser opravdu viděly, cela má **rovné čelo jen 0 mm nad pískem** (bez límce; tisk ⌀220 × 146) a kamera je přesunuta (y -102, 110 mm nad pískem, sklon 38°; dříve −92 / 100 / 43°).

| | límec 34 mm (var. C) | čelo 5 mm (var. U) |
|---|---|---|
| kamera nevidí | 20.0 % povrchu | 0.0 % povrchu |
| laser neosvítí | 11.8 % | 0.0 % |

Zorné pole objektivu 6 mm na HQ kameře (6,29 × 4,71 mm): ±27,6° × ±21,4°; potřeba na celý ⌀100: ±24.4° × -17.7…19.7° → vejde se s rezervou 2–3°. Vzdálenost objektiv–střed 115 mm, 1 pixel ≈ 30 µm; posun čáry = 0.58 × změna výšky, střed čáry na 1/10 pixelu → výška ≈ 5–10 µm.

**Teplotní posun (−10 ↔ +10 °C):** sloupy rámu 276 mm Al zvednou kameru i laser o ≈ 128 µm – to ukáže invarový terčík P03 (stojí na základně, výška se nemění) a odečte se; dno cely a podložky G10 zvednou písek o ≈ 47 µm – opraví se podle slepé zkoušky S0 (atrapa) a teploty dna (NTC). Bez těchto oprav by posun byl srovnatelný se zdvihem písku.

**Fotky:** bílá LED 5 V vedle okénka kamery; při každém snímání dva snímky – s LED (obraz povrchu: námraza, trhliny, vysychání) a s laserem bez LED (výšková mapa). LVDT se ve fázi 1 nepoužívá – kupuje se až pro fázi 2 (píst = kryt při sublimaci).

## 23. Kamera obíhající kolem vzorku (16. 11. 2026)

Hlava s **Raspberry Pi Camera Module 3 Wide** (deska 25 × 24 mm, zorné pole 102° × 67°, 4608 × 2592 px, autofokus, ostří od 5 cm; revize 20. 11. 2026 – standardní modul ostří až od 10 cm) obíhá kolem osy vzorku – **jedna sestava pro obě fáze** (18. 11. 2026). Pod středem příčníku T04 je pevné jádro P12 s otvorem ve středu, v němž sedí kluzné pouzdro igus vodicí tyče zátěže (nahrazuje pouzdro P01); na jádře dvě ložiska 6806-2RS, na nich otočný náboj P13: dole rameno s hlavou kamery P14, nahoře věnec m1 z72. Krokový motor 28BYJ-48 s pastorkem z12 (převod 6 : 1) visí pod příčníkem na straně −x (držák P16). Ve fázi 2 tedy hlava obíhá kolem tyče se závažím. Rameno vede pod motorem (z 271–279) do 71 mm od osy, pak krátký sloupek k hlavě. Řídí Raspberry Pi Zero 2 W (program rpi/e7_kamera.py), které zároveň fotí; box s RPi je na vnější straně pravého sloupu (+x), plochý kabel 500 mm ve smyčce → rozsah ±180°.

| veličina | hodnota |
|---|---|
| okénko hlavy | 85 mm od osy, 90 mm nad pískem, sklon 39° od svislice |
| potřebné zorné pole pro celý ⌀100 | ±22.7° × -17.7…+17.3° (kamera má ±51° × ±33.5° → rezerva ≥ 15.8°) |
| vzdálenost okénko–střed, 1 pixel | 124 mm, ≈ 66 µm → výška laserem ≈ 11–23 µm (čára na 0,1–0,2 px) |
| kroky na otáčku ramene | 2048 × 72/12 = 12288 → 0.029° na krok |
| vůle převodovky 28BYJ-48 | ≈ 1–3° na hřídeli motoru → 0,2–0,5° na rameni; výchozí poloha vždy najetím ze stejné strany na optickou vidlicovou koncovku (clona na náboji, držák P21) → opakovatelnost ≈ 0,1° |
| moment | motor ≈ 0,03 N·m × 6 ≈ 0,16 N·m; tření 2 ložisek 2RS při −10 °C + smyčka kabelu ≈ 0,02–0,04 N·m → rezerva ≈ 4× |
| oběh pro 3D model | 36 pozic po 10° (−180 … +170°) × 2 polohy ostření = 72 snímků, ≈ 2,5 s na pozici → ≈ 3 min; při snímku svítí LED na hlavě |
| teplo | motor 1,2 W jen při pohybu (pak vypnout cívky – převod drží); hlava: topné tělísko PTC 5 V (≈ 2–3 W přes relé, termostat 5–8 °C podle DS18B20 na víčku) drží kameru nad 0 °C a okénko bez rosy – provozní teplotu modulu výrobce neuvádí, proto vyhřívaná hlava |

**Ostření a hloubka ostrosti (revize 20. 11. 2026).** Okénko je od písku 97–162 mm (šikmý pohled). Standardní Camera Module 3 ostří až od 100 mm a při zaostření na 121 mm je ostrý jen pás 118–124 mm (rozmazání ≤ 2 px) – nejbližší okraj nezaostří a většina povrchu je neostrá. Verze **Wide** (f = 2,75 mm, f/2,2) ostří od 50 mm; se **2 polohami ostření** na každé pozici oběhu (108 a 140 mm, rozmazání ≤ 3 px) pokryje 95–169 mm, tj. celý povrch. Za ostřejší obraz se platí hrubším pixelem (≈ 2× větší než u standardního modulu); přesnost výšky drží laser a vyhodnocení z 36 pohledů.

**Laser se snímá jen ve výchozí poloze (−y)**, kam se hlava vrací přes optickou koncovku. Protože se hlava mezi tím otáčí, výška se počítá vůči laserovým čarám na rovném čele cely (v úrovni povrchu písku) a na invarovém terčíku v témže snímku; malá nepřesnost návratu (≈ 0,1°) se tím vyruší.

**Fáze 2 (se zátěží):** vodicí tyč ⌀12 prochází středem jádra (pouzdro igus v P12), náboj s ramenem se točí kolem ní. Tyč a píst zakryjí z každé polohy jen malou část mezikruží, ostatní polohy oběhu ji vidí. Laser na invarový terčík na straně kamery ve fázi 2 nedosvítí (zakryje ho zátěžový sloupec) – posun rámu tam hlídá LVDT.

**Řízení motoru:** Raspberry Pi Zero 2 W (stejné, které fotí) přes desku ULN2003, půlkroky z Pythonu (gpiozero); poloha se jen počítá, takže na časování nezáleží – Arduino není potřeba. Po každém pohybu se cívky vypnou (převod 64 : 1 v motoru drží polohu, motor nehřeje). Výchozí poloha: optická vidlicová koncovka (držák P21) a vodorovná clona na náboji; cíl se vždy najíždí ve stejném směru (vymezení vůle). Poslední poloha se ukládá, aby se po výpadku proudu kabel nenavíjel dál.

## 24. Mrazák 59 × 39 × 41 cm – nižší sestava (19. 11. 2026)

Vnitřní prostor mrazáku 590 × 390 × 410 mm (šířka × hloubka × výška). Původní sestava měřila 486 mm (fáze 1) a 520 mm (fáze 2), proto byla snížena. Výšky jsou změřené na 3D modelu:

| | výška | k víku | volno po stranách (š / h) |
|---|---|---|---|
| fáze 1 – bez zatížení | 383 mm | 27 mm | 87 / 35 mm |
| fáze 2 – se zátěží | 400 mm | 10 mm | 87 / 35 mm |

**Co se změnilo:** pryžové podložky 3 mm místo stavitelných noh (−19 mm); dno cely a podložky G10 20 mm (dříve 40, −20 mm); příčník 130 mm nad pískem (dříve 140), oběh kamery se posunul s ním, okénko 90 mm nad pískem, sklon 39° (Camera Module 3 Wide, celý povrch v zorném poli, 1 px ≈ 66 µm, 2 polohy ostření); nosná deska Al 6 mm přišroubovaná M6 do čela vodicí tyče 5 mm nad příčníkem (bez stavěcího kroužku); kotouče ocel ⌀165 × 6 = 1,00 kg (dříve ⌀117,5 × 12); laser 105 mm od osy a 182 mm nad pískem (60°, posun čáry 0.58 × změna výšky) – mimo kotouče; LVDT vedle příčníku; box s RPi na vnější straně pravého sloupu.

**Zatížení:** pohyblivá část bez kotoučů (píst, tyč, nosná deska) ≈ 0.49 kg → ≈ 2.5 kPa pod pístem ⌀50; každý kotouč 1 kg přidá ≈ 5.0 kPa (4 kotouče + 0,5 kg ≈ 25 kPa).

**Ověřeno v modelu:** v obou fázích bez kolizí v celém rozsahu oběhu kamery (po 10°); ve fázi 1 kamera i laser vidí celý povrch ⌀100 a invarový terčík. Ve fázi 2 laser pod sklonem 60° víc stíní vysoký límec cely (34 mm) – před fází 2 zvážit nižší límec nebo celu fáze 1.

## 25. Kontrola zadání 19. 11. 2026 – vedení zátěže, překlopení, teplotní roztažnost, baterie 24 h při −20 °C

**Překlopení (bod 5).** Sestava fáze 2 (nejtěžší, 4,5 kg závaží nahoře) stojí celou délkou podélníků T02 na pryžovém pásu. Hmotnosti jsou odhad (profily podle katalogové hmotnosti na metr):

| část | kg |
|---|---|
| rám z T-profilů (40×80 ≈ 2,6 kg/m, 40×40 ≈ 1,5 kg/m) + úhelníky | 4.56 |
| cela PETG + podložky G10 | 1.10 |
| písek ⌀100 × 100 (vlhký) | 1.60 |
| zátěž: 4 kotouče + 0,5 kg + nosná deska + tyč + píst | 5.01 |
| oběh kamery, motor, laser | 0.45 |
| box s RPi Zero 2 W na sloupu (+x) | 0.35 |
| sloupek Invar + ramena + LVDT | 0.50 |
| **celkem** | **13.6** |

Těžiště 253 mm nad dnem, posunuté o 10 mm k boxu RPi. Sestava se převrhne až po naklonění o 32° (do strany x 32°, y 32°) nebo vodorovnou silou ≈ 52 N na horní hranu (404 mm) – kabely ani zavírání víka ji nepřevrhnou.

**Vedení zátěže (bod 4).** Tyč je vedená ve dvou místech: nahoře kluzným pouzdrem igus ⌀12 × 30 v jádře oběhu, dole středicím důlkem 90° na kuličce v pístu (píst drží v písku tření pod zatížením). Vzdálenost obou míst 92 mm, vůle pouzdra ≈ 60 µm → náklon tyče nejvýš ≈ 0.04°, u kotoučů ≈ 49 µm do strany. Kotouče (otvor ⌀6,6) sedí na závitovém čepu M6 a maticí jsou staženy k nosné desce a k tyči – jsou vystředěné, nevrzají a nechvějí se; těžiště zátěže je v ose tyče. Chvění od kompresoru tlumí pryžový pás pod rámem.

**Teplotní roztažnost (bod 6)** pro změnu −20 → +20 °C (ΔT = 40 K):

| část | α [1/K] | délka [mm] | změna [µm] | jak se řeší |
|---|---|---|---|---|
| sloupy rámu Al (kamera, laser) | 2.3e-05 | 276 | 255 | invarový terčík P03 – odečte se v každém snímku |
| vodicí tyč Invar (píst → LVDT) | 1.2e-06 | 150 | 7 | zanedbatelné |
| sloupek LVDT Invar | 1.2e-06 | 283 | 14 | zanedbatelné |
| dno cely PETG pod pískem (+ jádro) | 4.5e-05 | 46 | 83 | slepá zkouška S0 + teplota dna (NTC) |
| podložky G10 | 1.5e-05 | 20 | 12 | slepá zkouška S0 |
| písek (bez fázové změny) | 1.0e-05 | 100 | 40 | patří k měřenému signálu |

Měřicí řetězec je tedy teplotně stabilní tam, kde to jde (Invar), a zbytek se odečte: rám přes invarový terčík v témže snímku, cela a podložky podle slepé zkoušky s hliníkovou atrapou. Zdvih písku při mrznutí je řádově stovky µm až 1,7 mm.

**Baterie 24 h při −20 °C (zadání).** Odhad spotřeby oběhu a kamery (RPi Zero 2 W místo RPi 5):

| spotřebič | W |
|---|---|
| Raspberry Pi Zero 2 W (průměr) | 0.80 |
| topení hlavy PTC 5 V (termostat, −20 °C, s pěnou 5 mm) | 0.55 |
| relé, LED, laser, motor (krátce) | 0.15 |
| **celkem** | **1.5 W → 36 Wh / den** |

Powerbanka 26 800 mAh (≈ 99 Wh, výstup 5 V ≈ 80 Wh) **mimo mrazák** (v teple, trvale v zásuvce, s průchozím nabíjením) vydrží bez sítě ≈ 53 h. CR850 má vlastní napájení 12 V (záložní akumulátor podle vybavení E6); LVDT (fáze 2) a ventilátor jsou ze sítě – při výpadku proudu se zastaví i mrazák.

## 26. Revize 20. 11. 2026 – čidla ve vzorku, kamera, data, napájení

Cíl upřesněn: **deformace a posun při cyklech mrznutí a tání** (koncepce, `revize_E7.md`). Vzorek ⌀100 × 100, mrazák 590 × 390 × 410 mm (délka × šířka × výška).

**Čidla ve vzorku** (hloubka pod povrchem písku; úhel v půdorysu, 270° = strana −y, kde je port bodu M):

| čidlo | hloubka [mm] | úhel | poloha | připojení |
|---|---|---|---|---|
| TDR CS645 (bod M) | 36 / 45 / 54 (3 tyčky ⌀3.2 × 75, rozteč 8.9) | 270° | vodorovně ze strany, přes osu | TDR100/200 → CR850 C1–C3 |
| Pt100 (bod M) | ≈ 33 (3,5 mm nad horní tyčkou) | 270° | hrot 30 mm od stěny | 4WPB100 → CR850 DIFF2 |
| optické vlákno FBG (bod M) | ≈ 31 | 270°, bočně 4,7 mm | hrot 37,5 mm od stěny | vlastní vyhodnocovací jednotka |
| T1 DS18B20 ⌀6 × 50 | 10 | 240° | hrot 30 mm od stěny (r 20) | RPi GPIO4 (1-Wire), vývodka M12 |
| T2 DS18B20 ⌀6 × 50 | 30 | 330° | hrot 30 mm od stěny (r 20) | RPi GPIO4 (1-Wire), vývodka M12 |
| T3 DS18B20 ⌀6 × 50 | 50 | 210° | hrot 30 mm od stěny (r 20) | RPi GPIO4 (1-Wire), vývodka M12 |
| T4 DS18B20 ⌀6 × 50 | 70 | 330° | hrot 30 mm od stěny (r 20) | RPi GPIO4 (1-Wire), vývodka M12 |
| T5 DS18B20 ⌀6 × 50 | 90 | 240° | hrot 30 mm od stěny (r 20) | RPi GPIO4 (1-Wire), vývodka M12 |
| NTC 10 kΩ (dno) | pod pískem, v tištěném dně | 30° | radiální otvor ⌀4 | CR850 SE6 |

Bod M (TDR + Pt100 + vlákno) zůstává jako v terénu (potvrzeno 9. 11. 2026), uprostřed výšky vzorku – čelo mrznutí jím projde v polovině cyklu. Teplotní profil T1–T5 po 20 mm dává polohu izotermy 0 °C (čelo) s přesností ≈ 2–5 mm (lineární interpolace). Sondy jsou ve šroubovici kolem strany −y (kabely vedou spolu s bodem M), od tyček TDR ≥ 14,6 mm (≈ 1,6 × rozteč tyček – mimo citlivou oblast), od stěny 30 mm. Na CR850 už nejsou volné vstupy (DIFF1 LVDT, DIFF2 Pt100, SE5 vzduch, SE6 dno, C1–C3 TDR, C4 spouštění), proto profil čte RPi po sběrnici 1-Wire – bez pájení, 3 vodiče každé sondy do svorek WAGO. Port bodu M je o 4 mm vyšší: kabel Pt100 a vlákno vedou nad hlavou CS645, ne skrz ni (dříve by nešly smontovat).

**Data:** oběh 72 snímků (36 pozic × 2 ostření) každé 3 h + sada laser/LED/tma (5 snímků) každých 10 min ≈ 5.2 GB/den → série 10 cyklů (20 dní) ≈ 104 GB. Karta 128 GB „high endurance“ a denní stažení do PC přes Ethernet (rsync).

**Směr mrznutí v současné cele** (sim_thaw.py, 20. 11. 2026; tištěná izolace: stěna 30 mm a dno 20 mm z řídké výplně λ ≈ 0,06, podložky G10 na Al příčce): 95 % vzorku zmrzne za ≈ 13,75 h, celý za ≈ 14,25 h; poslední nezmrzlé místo je na ose 17 mm nade dnem → **≈ 83 % výšky promrzá shora**, spodních ≈ 17 mm zespodu (dno je po snížení sestavy jen 20 mm, dříve 40 mm → 13 mm). Stěna izoluje dostatečně, boční XPS není potřeba; dno ukáže T5 (90 mm) a NTC ve dně. Roztátí ≈ 13,75 h po přepnutí na +10 °C → cyklus 24 h + 24 h stačí.

**Napájení:** powerbanka mimo mrazák je trvale na nabíječce USB-C PD (≥ 45 W) – slouží jako záložní zdroj; ze sítě běží neomezeně, při výpadku ≈ 53 h. Spotřeba se dvěma polohami ostření se prakticky nemění (oběh trvá ≈ 3 min místo 1,5 min).

