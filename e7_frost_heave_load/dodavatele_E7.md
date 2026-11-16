# E7 – dodavatelé a objednávka podle fází

Stav 16. 11. 2026, sestava varianta C rev. B3. Ceny jsou orientační, většinou bez DPH, 1 € ≈ 25 Kč; „ověřeno“ = cena z webu nebo nabídky, ostatní je odhad – před objednáním potvrdit. Podrobné specifikace: `objednavka.md`. Nářezové výkresy: `vyroba/narezy/`. 3D model: `3d/E7_sestava_final.glb` (STEP: `3d/E7_V01_variant_C.step`).

**Fáze 1 – jednoduchá zkouška mrznutí a tání.** Nenasycený písek Sr 0,5, zatížený píst a volný povrch, 24 h −10 °C / 24 h +10 °C, 10 cyklů. Nakupuje se:

- **1A – jádro:** rám, cela, zátěž, LVDT a teploty. Bez toho zkouška nejde.
- **1B – povrch:** laser + kamera měří volný povrch. Doporučuji objednat hned, laser má dodací lhůtu. Ke stojanu se dá přišroubovat i později.

**Fáze 2 – sublimace.** Písek s ledem, suchý vzduch, píst slouží jako kryt. Stojan zůstává stejný. Doobjedná se jen váha, vlhkoměr, silikagel a misky, **žádné řezané ani obráběné díly**.

**Už máte:** CR850, TDR + CS645, Pt100, optické vlákno, mrazák s regulátorem.

## 0 · Co objednat jako první (nejdelší dodání)

| pořadí | co | firma | proč hned | dodání (odhad) |
|---|---|---|---|---|
| 1 | LVDT RDP DCTH400AG | Elkome (FI, e-shop) | bez LVDT se neměří zdvih; ověřit, zda je skladem | 1–4 týdny |
| 2 | Campbell 4WPB100 + 109-L | Ekotechnika Černošice | zboží z USA, dlouhá lhůta | 3–6 týdnů |
| 3 | Invar ⌀12 a ⌀16 | Kovohutě Rokycany | poptávka, řez na míru | 1–3 týdny |
| 4 | rám z T-profilů | ENPRAG Praha | nařežou podle výkresu, vyvrtají ⌀14 | 1–2 týdny |
| 5 | laser 11 čar | Picotronic (DE) | platba předem podle nabídky A2627918 | 1–2 týdny |
| 6 | kotouče a písty (laser) | grupol.cz | nahrát DXF, cena hned | ≈ 1 týden |
| 7 | filament a tisk cely | Prusa | tisk cely trvá 35–50 h | 2–3 dny + tisk |
| 8 | ostatní (TME, GME, RPishop, Fabory, Hornbach) | e-shopy | skladem | 1–3 dny |

## 1 · Fáze 1 – nákup podle firem

### 1.1 ENPRAG, s.r.o. – rám z T-profilů

Česká firma, K Holyni 833/42, Praha 5. IČO 62743741, tel. +420 224 942 663, zdarma 800 888 868, [enprag.cz](https://www.enprag.cz/hlinikove-profily/c-6027). **Poslat:** `vyroba/narezy/E7_narezy_profily_ENPRAG.pdf` a text poptávky `poptavka_ramu.md`. Požádat o celou sadu včetně spojovacího materiálu, případně o sestavení.

| položka | ks | cena | fáze |
|---|---|---|---|
| profil 40×80 drážka 8: T01 2× 306, T03 260, T04 340 s otvorem ⌀14 | 4 | 31,43 €/m + řezy (ověřeno) | 1A |
| profil 40×40 drážka 8: T02 2× 320 | 2 | ≈ 15–20 €/m + řezy | 1A |
| úhelník 40×40 drážka 8 + krytka | 12 | ≈ 3–6 €/ks | 1A |
| T-matice M8 / M5 vkládací | 32 / 12 | ≈ 1 €/ks | 1A |
| šroub ISO 4762 M8×16 + podložka | 24 | sada | 1A |
| stavitelná noha M8, talíř ⌀30–40 | 4 | ≈ 3–5 €/ks | 1A |
| **celkem** | | **≈ 4 000–6 000 Kč** | |

Alternativy (české): [Alutec K&K](https://katalog.aluteckk.cz/kategorie-produktu/modul-40-drazka-8/), [Profimet](https://profimet.cz/sluzby/), [eProfily.cz](https://www.eprofily.cz/).

### 1.2 grupol.cz – laserové řezání plechů

Online: nahrát DXF a cena se ukáže hned, [grupol.cz](https://grupol.cz/). **Poslat:** soubory `vyroba/laser/*.dxf` (5 souborů), pro kontrolu `E7_narezy_laser_grupol.pdf`.

| položka | ks | cena | fáze |
|---|---|---|---|
| L03 nosná deska ⌀140, Al 10 mm | 1 | | 1A |
| L04 a L05 píst ⌀50, Al 10 mm | 1 + 1 | | 1A |
| L06 závaží 1 kg ⌀117,5, ocel 12 mm | 4 | | 1A |
| L07 závaží 0,5 kg ⌀117,5, ocel 6 mm | 1 | | 1A |
| **celkem** | | **≈ 1 800–3 500 Kč** | |

Pokud grupol neřeže hliník 10 mm, stejné DXF pošlete na vodní paprsek nebo laser jinam: [Zamet](https://www.zamet.cz/laserove-rezani), [Light Cut](https://lightcut.cz/co-umime/rezani-laserem/).

### 1.3 Kovohutě Rokycany – Invar 36

FeNi36, 1.3912. E-mail sales@koro.cz, [koro.cz](http://www.koro.cz/produkty/nikl-a-slitiny-niklu/). **Poslat:** `E7_narezy_invar_Rokycany.pdf`.

| položka | ks | cena | fáze |
|---|---|---|---|
| B01 tyč ⌀12 h9 × 265 mm, čela kolmá (vodicí tyč) | 1 | | 1A |
| B02 tyč ⌀16 × 330 mm, čela kolmá (sloupek LVDT) | 1 | | 1A |
| **celkem** (≈ 0,9 kg Invaru) | | **≈ 2 000–4 000 Kč** | |

Alternativa: [Evek](https://evek.vip/) (Invar 36, řez na míru).

### 1.4 Elektroizolanty Praha – sklotextit G10

[elektroizolanty.cz](https://www.elektroizolanty.cz/elektroizonlanty/eshop/57-1-Tyce-G10-130-C-akcni-ceny). **Poslat:** `E7_narezy_G10_Elektroizolanty.pdf`.

| položka | ks | cena | fáze |
|---|---|---|---|
| tyč G10 ⌀20 × 1000; nařezat 3× 40 mm, čela rovnoběžná | 1 | 298 Kč (ověřeno) | 1A |

### 1.5 Elkome – LVDT (zastoupení RDP)

E-shop, Finsko: [shop.elkome.com](https://shop.elkome.com/en/dcth400ag-lvdt-displacement-sensor). Česká alternativa k poptání: [Micro-Epsilon Czech Republic, Bechyně](https://www.micro-epsilon.cz/), info@micro-epsilon.cz – induSENSOR DTA-10D. Jiný snímač ale znamená upravit svěrku P02.

| položka | ks | cena | fáze |
|---|---|---|---|
| LVDT RDP DCTH400AG, ±10 mm, DC vstup i výstup | 1 | 581 € ≈ 14 500 Kč (ověřeno) | 1A |

### 1.6 Ekotechnika Černošice – Campbell Scientific pro ČR

Tel. +420 251 640 511, [campbellsci.com/ekotechnika](https://campbellsci.com/ekotechnika).

| položka | ks | cena | fáze |
|---|---|---|---|
| 4WPB100 – modul pro 4vodičové Pt100 | 1 | ≈ 60–120 € | 1A |
| 109-L teplota vzduchu, kabel 3 m | 1 | ≈ 150–220 € | 1A |
| **celkem** | | **≈ 5 300–8 500 Kč** | |

### 1.7 HENNLICH (igus), Fabory CZ, Hornbach – vedení a šrouby

- **HENNLICH s.r.o.** – zastoupení igus. Litoměřice, tel. +420 416 711 333, [igus.eu](https://www.igus.eu/Contact/general/CZ). Alternativa: [TME](https://www.tme.eu/cz/).
- **Fabory CZ** – [fabory.com/cs](https://www.fabory.com/cs/).
- Hornbach / OBI.

| položka | kde | ks | cena | fáze |
|---|---|---|---|---|
| kluzné pouzdro igus drylin RJ4JP-01-12 | HENNLICH / TME | 1 | ≈ 50–120 Kč | 1A |
| stavěcí kroužek DIN 705-A 12 | Fabory | 2 | ≈ 50–100 Kč/ks | 1A |
| ocelová kulička 5/16" (7,94 mm) | cyklo prodejna / Fabory | 1 bal. | ≈ 30–80 Kč | 1A |
| šrouby M5 (35/20/12), M4×20, M3×20 + červík, M2,5×6 + sloupky | Fabory / Hornbach | sada | ≈ 300–600 Kč | 1A / 1B |

### 1.8 Prusa Research – filament (Praha)

[prusa3d.com](https://www.prusa3d.com/product/prusament-petg-carbon-fiber-black-1kg/).

| položka | ks | cena | fáze |
|---|---|---|---|
| Prusament PETG Carbon Fiber 1 kg (cela ≈ 1,3 kg + díly P01–P11 ≈ 0,5 kg) | 2 | ≈ 2 400–2 800 Kč | 1A |

Tiskárna pro celu: podložka ≥ 240 × 240 mm, výška tisku ≥ 200 mm.

### 1.9 TME / GM electronic – elektronika

[TME](https://www.tme.eu/cz/) (Łódź, prodává česky, sklad), [GM electronic](https://www.gme.cz/) (Praha, Brno).

| položka | ks | cena | fáze |
|---|---|---|---|
| zdroj Mean Well HDR-15-24 (24 V, napájení LVDT) | 1 | ≈ 11 € (ověřeno TME) | 1A |
| NTC 10 kΩ v nerezové jímce ⌀3 + odpor 10 kΩ 0,1 % (dno cely) | 2 | ≈ 150–400 Kč | 1A |
| ventilátor 80 mm 12 V + zdroj 12 V | 1 | ≈ 250–500 Kč | 1A |
| optočlen / relé modul 5 V (CR850 C4 → spouštění snímku) | 1 | ≈ 80–120 Kč | 1B |
| MOSFET AO3400 / IRLZ44N, odpory, kabel, bužírka (spínání laseru) | 1 sada | ≈ 80–120 Kč | 1B |
| vývodka PG7 2×, Ethernet kabel 3 m | 1 | ≈ 150 Kč | 1B |

### 1.10 Picotronic GmbH – čárový laser (Německo)

Podle cenové nabídky A2627918 z 10. 11. 2026. Podmínky EXW, platba předem. Český dodavatel 11čárového laseru nebyl nalezen. Alternativa: Laser Components FLEXPOINT přes TME nebo Distrelec CZ, ale vyžaduje úpravu držáku P05.

| položka | ks | cena | fáze |
|---|---|---|---|
| **DOE253-635-5-6(10x24)**, obj. č. 70132403: 11 čar, 635 nm, 5 mW, 5 V, nastavitelné ohnisko | 1 | 104,96 € + doprava 11 € (ověřeno) | 1B |

### 1.11 RPishop.cz – kamera a Raspberry Pi (České Budějovice)

Oficiální prodejce Raspberry Pi, [rpishop.cz](https://rpishop.cz/). Alternativy: [LaskaKit](https://www.laskakit.cz/), Alza.

| položka | ks | cena | fáze |
|---|---|---|---|
| Raspberry Pi 5, 4 GB | 1 | 2 769 Kč (ověřeno) | 1B |
| Raspberry Pi HQ Camera C/CS | 1 | 1 499 Kč (ověřeno) | 1B |
| objektiv 6 mm CS (širokoúhlý) | 1 | ≈ 500–750 Kč | 1B |
| kabel kamery Standard–Mini 200 mm, zdroj 27 W, microSD 32 GB | 1 | ≈ 400–600 Kč | 1B |

### 1.12 Hornbach / OBI / papírnictví – spotřební materiál

| položka | ks | cena | fáze |
|---|---|---|---|
| dvousložkový epoxid (dutina cely, slepení pístu) | 1 | ≈ 250–400 Kč | 1A |
| PTFE sprej + silikonová vazelína (Molykote 111 – TME) | 1 | ≈ 400–600 Kč | 1A |
| spároměr 0,05–1,00 mm (kalibrace laseru) | 1 | ≈ 150–250 Kč | 1B |
| ocelové kolíky ⌀3 × 40 (4 ks) + tyčinka ⌀3 × 120 | 1 | ≈ 80 Kč | 1A |
| kontrolní miska ⌀100 × 20 (sklo / nerez) | 1 | ≈ 120 Kč | 1A |
| pěch ⌀95 (lze vytisknout) + kovové pravítko | 1 | ≈ 250 Kč | 1A |
| příchytky kabelů do drážky 8 + stahovací pásky | 4 | ≈ 100 Kč | 1A |
| sklo / plexi 50 × 50 × 2 mm do okénka boxu kamery | 1 | ≈ 50 Kč | 1B |
| značky ArUco 10 mm (samolepky, tisk) + ocelové měřítko 150 mm | 1 | ≈ 125 Kč | 1B |

## 2 · Fáze 2 – sublimace (doobjednat po prvních cyklech fáze 1)

Stojan, cela, píst, LVDT, laser i kamera zůstávají. Přibývá jen:

| položka | kde (česky) | ks | cena | k čemu |
|---|---|---|---|---|
| tenzometr 1 kg + převodník HX711 | [LaskaKit](https://www.laskakit.cz/) / GM electronic | 1 | ≈ 150–300 Kč | váha s miskou v mrazáku → rychlost sublimace |
| čidlo vlhkosti SHT45 (I²C modul) | RPishop.cz / LaskaKit (alt. SHT40) | 1 | ≈ 350–600 Kč | vlhkost vzduchu v truhle – **povinné** |
| skleněné misky ⌀90 (Petriho) | [P-LAB](https://www.p-lab.cz/) / [Verkon](https://www.verkon.cz/) | 3 | ≈ 200–400 Kč | miska ledu + miska písku s ledem (předzkouška S1) |
| silikagel s indikátorem 2 kg + plastový tác | e-shopy se silikagelem / Hornbach | 1 | ≈ 400–700 Kč | suchý vzduch v mrazáku |
| síto 2 mm (laboratorní nebo kuchyňské nerez) | Verkon / P-LAB / Hornbach | 1 | ≈ 150–400 Kč | drcený led pro písek s přebytkem ledu |
| **celkem fáze 2** | | | **≈ 1 300–2 400 Kč** | |

## 3 · Souhrn podle fáze (odhad)

| fáze | co | cena |
|---|---|---|
| 1A – jádro | rám, laserové díly, Invar, G10, igus, šrouby, filament, LVDT, Campbell, elektronika, spotřební | ≈ 33 000–45 000 Kč |
| 1B – povrch | laser Picotronic, RPi 5 + HQ kamera + objektiv, drobná elektronika | ≈ 8 500–9 500 Kč |
| 2 – sublimace | váha HX711, SHT45, misky, silikagel, síto | ≈ 1 300–2 400 Kč |
| **celkem** | | **≈ 43 000–57 000 Kč** |

Největší položky jsou LVDT (≈ 14 500 Kč) a Campbell (≈ 5 300–8 500 Kč).

## 4 · Které soubory poslat které firmě

| firma | soubory |
|---|---|
| ENPRAG | `vyroba/narezy/E7_narezy_profily_ENPRAG.pdf`, text `poptavka_ramu.md` |
| grupol.cz | `vyroba/laser/E7-L03…L07_*.dxf`, kontrola `vyroba/narezy/E7_narezy_laser_grupol.pdf` |
| Kovohutě Rokycany | `vyroba/narezy/E7_narezy_invar_Rokycany.pdf` |
| Elektroizolanty Praha | `vyroba/narezy/E7_narezy_G10_Elektroizolanty.pdf` |
| vlastní tisk | `vyroba/tisk/*.stl` (cela E7-V03, díly P01–P11) |
| všechny dohromady | `vyroba/narezy/E7_narezove_vykresy.pdf` (přehled N00, plány N01–N03 + výrobní výkresy 12 dílů) |

## 5 · Ověřit před objednáním

- **Tiskárna:** výška tisku ≥ 200 mm (cela ⌀220 × 200).
- **Mrazák:** vnitřní výška ≥ 600 mm (sestava 559 mm + rezerva na kabely).
- **LVDT RDP:** provoz při −10 °C (dotaz na Elkome).
- **grupol.cz:** zda řeže hliník 10 mm.
