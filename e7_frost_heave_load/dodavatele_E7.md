# E7 – dodavatelé a objednávka podle fází

Stav 16. 11. 2026. Ceny jsou orientační, většinou bez DPH, 1 € ≈ 25 Kč. „Ověřeno“ znamená cenu z webu nebo z nabídky, ostatní je odhad – před objednáním potvrdit.

Kde co najdete:

- podrobné specifikace: `objednavka.md`
- nářezové výkresy: `vyroba/narezy/`
- sestava fáze 1: výkres `vykresy/E7-V07_bez_zatizeni.pdf`, 3D model `3d/E7_V07_bez_zatizeni.step`
- výpočty a kontrola zorného pole: `vypocty.md` §22

## Dvě fáze

**Fáze 1 – mrznutí a tání BEZ ZATÍŽENÍ (varianta U).**

- Vzorek: nenasycený písek Sr 0,5, cyklus 24 h −10 °C / 24 h +10 °C, 10 cyklů.
- Povrch písku je celý volný. Kamera s laserem měří jeho zdvih a sednutí po celé ploše ⌀100 (≈ 10 µm).
- **Kamera obíhá kolem vzorku** (±180°, snímek po 10°): z jednoho oběhu se udělá 3D model povrchu (fotogrammetrie). Laser se snímá ve výchozí poloze.
- **Oběh je pro obě fáze stejný:** ložiska, věnec a motor jsou pod příčníkem. Ve středu pevného jádra je pouzdro igus pro vodicí tyč zátěže, takže ve fázi 2 hlava obíhá kolem tyče. Motor řídí totéž RPi 5, které fotí (program `rpi/e7_kamera.py`).
- Bílá LED k tomu dává obyčejné fotky povrchu (námraza, trhliny).
- Cela má rovné čelo jen 5 mm nad pískem, aby kamera viděla až ke stěně.
- Teplotní posun rámu ukáže invarový terčík.
- **Bez pístu, závaží a LVDT.**

**Fáze 2 – sublimace se zátěží (varianta C).**

- Stejný rám, kamera i laser.
- Přibude píst se závažím jako „kámen“ a LVDT.
- Pro sublimaci navíc váha, vlhkoměr, silikagel a misky.
- Před fází 2 se rozhodne, zda vytisknout vyšší celu s límcem, nebo upravit středicí víčko P09 a stěrku pro nízkou celu.

**Už máte:** CR850, TDR + CS645, Pt100, optické vlákno, mrazák s regulátorem.

## 0 · Co objednat jako první – fáze 1

| pořadí | co | firma | proč hned | dodání (odhad) |
|---|---|---|---|---|
| 1 | laser 11 čar | Picotronic (DE) | jediné měření výšky ve fázi 1; platba předem podle nabídky A2627918 | 1–2 týdny |
| 2 | Campbell 4WPB100 + 109-L | Ekotechnika Černošice | zboží z USA, dlouhá lhůta | 3–6 týdnů |
| 3 | rám z T-profilů | ENPRAG Praha | nařežou podle výkresu, vyvrtají ⌀14 (pro fázi 2) | 1–2 týdny |
| 4 | Invar ⌀16 (+ ⌀12 pro fázi 2) | Kovohutě Rokycany | poptávka, řez na míru; obě tyče najednou | 1–3 týdny |
| 5 | RPi 5 + Camera Module 3 + kabel 500 mm | RPishop.cz | skladem | 1–3 dny |
| 6 | filament a tisk cely | Prusa | cela ⌀220 × 151 se tiskne ≈ 25–40 h | 2–3 dny + tisk |
| 7 | G10, elektronika, oběh (ložiska 6806, motor, pouzdro igus), šrouby, spotřební | Elektroizolanty, TME, GME, HENNLICH, Fabory, Hornbach | skladem | 1–3 dny |

LVDT (Elkome) a laserem řezané kotouče (grupol.cz) stačí objednat **až před fází 2**. Pouzdro igus se kupuje hned, sedí v jádře oběhu.

## 1 · Fáze 1 – nákup podle firem

### 1.1 ENPRAG, s.r.o. – rám z T-profilů

- Česká firma: K Holyni 833/42, Praha 5, IČO 62743741.
- Telefon +420 224 942 663, zdarma 800 888 868, [enprag.cz](https://www.enprag.cz/hlinikove-profily/c-6027).
- **Poslat:** `vyroba/narezy/E7_narezy_profily_ENPRAG.pdf` a text poptávky `poptavka_ramu.md`.
- Rám je pro obě fáze stejný, otvor ⌀14 v T04 nechat vyvrtat hned.

| položka | ks | cena |
|---|---|---|
| profil 40×80 drážka 8: T01 2× 306, T03 260, T04 340 s otvorem ⌀14 | 4 | 31,43 €/m + řezy (ověřeno) |
| profil 40×40 drážka 8: T02 2× 320 | 2 | ≈ 15–20 €/m + řezy |
| úhelník 40×40 drážka 8 + krytka | 12 | ≈ 3–6 €/ks |
| T-matice M8 / M5 vkládací | 32 / 12 | ≈ 1 €/ks |
| šroub ISO 4762 M8×16 + podložka | 24 | sada |
| ~~stavitelná noha M8~~ – **nekupovat**: mrazák je vysoký jen 41 cm, rám stojí na 4 pryžových podložkách ⌀30 × 3 (Hornbach / TME, ≈ 50 Kč) | 4 | – |
| **celkem** | | **≈ 4 000–6 000 Kč** |

Alternativy (české): [Alutec K&K](https://katalog.aluteckk.cz/kategorie-produktu/modul-40-drazka-8/), [Profimet](https://profimet.cz/sluzby/), [eProfily.cz](https://www.eprofily.cz/).

### 1.2 Kovohutě Rokycany – Invar 36

- FeNi36, 1.3912. E-mail sales@koro.cz, [koro.cz](http://www.koro.cz/produkty/nikl-a-slitiny-niklu/).
- **Poslat:** `E7_narezy_invar_Rokycany.pdf`.
- Obě tyče objednat najednou, i když ⌀12 je až pro fázi 2.

| položka | ks | cena | fáze |
|---|---|---|---|
| B02 tyč ⌀16 × 330 mm, čela kolmá – sloupek s terčíkem (později i LVDT) | 1 | | 1 |
| B01 tyč ⌀12 h9 × 265 mm, čela kolmá – vodicí tyč zátěže | 1 | | 2 |
| **celkem** (≈ 0,9 kg Invaru) | | **≈ 2 000–4 000 Kč** | |

### 1.3 Elektroizolanty Praha – sklotextit G10

[elektroizolanty.cz](https://www.elektroizolanty.cz/elektroizonlanty/eshop/57-1-Tyce-G10-130-C-akcni-ceny). **Poslat:** `E7_narezy_G10_Elektroizolanty.pdf`.

| položka | ks | cena |
|---|---|---|
| tyč G10 ⌀20 × 1000; nařezat 3× 20 mm, čela rovnoběžná | 1 | 298 Kč (ověřeno) |

### 1.4 Picotronic GmbH – čárový laser (Německo)

- Podle cenové nabídky A2627918 z 10. 11. 2026, podmínky EXW, platba předem.
- Český dodavatel 11čárového laseru nebyl nalezen.

| položka | ks | cena |
|---|---|---|
| **DOE253-635-5-6(10x24)**, obj. č. 70132403: 11 čar, 635 nm, 5 mW, 5 V, nastavitelné ohnisko | 1 | 104,96 € + doprava 11 € (ověřeno) |

### 1.5 RPishop.cz – kamera a Raspberry Pi (České Budějovice)

Oficiální prodejce Raspberry Pi, [rpishop.cz](https://rpishop.cz/). Alternativy: [LaskaKit](https://www.laskakit.cz/), Alza.

| položka | ks | cena |
|---|---|---|
| Raspberry Pi 5, 4 GB | 1 | 2 769 Kč (ověřeno) |
| **Raspberry Pi Camera Module 3** (standardní, ne Wide / NoIR) – malá hlava obíhá kolem vzorku; zorné pole 66° × 41° pokryje ⌀100 s rezervou ≈ 3° | 1 | ≈ 650–750 Kč |
| kabel kamery **Standard–Mini 500 mm** (pro RPi 5) – vede ve smyčce k obíhající hlavě | 1 | ≈ 100–200 Kč |
| zdroj 27 W, microSD 32 GB | 1 | ≈ 400–600 Kč |

### 1.6 Ekotechnika Černošice – Campbell Scientific pro ČR

Telefon +420 251 640 511, [campbellsci.com/ekotechnika](https://campbellsci.com/ekotechnika).

| položka | ks | cena |
|---|---|---|
| 4WPB100 – modul pro 4vodičové Pt100 | 1 | ≈ 60–120 € |
| 109-L teplota vzduchu, kabel 3 m | 1 | ≈ 150–220 € |
| **celkem** | | **≈ 5 300–8 500 Kč** |

### 1.7 Prusa Research – filament (Praha)

[prusa3d.com](https://www.prusa3d.com/product/prusament-petg-carbon-fiber-black-1kg/).

| položka | ks | cena |
|---|---|---|
| Prusament PETG Carbon Fiber 1 kg – cela U ≈ 1,1 kg + díly P03–P08, P10u ≈ 0,3 kg | 2 | ≈ 2 400–2 800 Kč |

Tiskárna pro celu: podložka ≥ 240 × 240 mm, **výška tisku ≥ 151 mm** (fáze 1; cela fáze 2 s límcem má 180 mm).

Fáze 1 tiskne:

- celu `E7-V03u_cell_D220x151_bez_zatizeni.stl`;
- P03 rameno s terčíkem (nová trasa);
- P04 patku sloupku;
- P05 držák laseru;
- P06 a P07 box pro RPi 5 (na polici P18 na boční straně příčníku);
- oběh kamery (obě fáze): P12 jádro s lůžkem igus, P12b distanční kroužek, P12c svěrný kroužek, P13 náboj s věncem z72, P14 rameno s hlavou, P15 víčko hlavy, P16 držák motoru, P18 držák boxu RPi, P19 pastorek z12;
- P10u stěrku s břitem 5 mm.

### 1.8 TME / GM electronic – elektronika

[TME](https://www.tme.eu/cz/) (prodává česky, sklad), [GM electronic](https://www.gme.cz/) (Praha, Brno).

| položka | ks | cena |
|---|---|---|
| **bílá LED 1 W na hliníkové hvězdě ⌀20 + odpor 6,8 Ω**, přilepit na hlavu kamery vedle okénka | 1 | ≈ 80–200 Kč |
| **oběh:** krokový motor 28BYJ-48 5 V + deska ULN2003 | 1 | ≈ 80–150 Kč |
| **oběh:** ložisko 6806-2RS (30 × 42 × 7, tenkostěnné) – TME, nebo český výrobce ZKL | 2 | ≈ 100–250 Kč |
| **oběh:** kluzné pouzdro igus drylin RJ4JP-01-12 do jádra P12 (ve fázi 2 jím jde vodicí tyč) – HENNLICH / TME | 1 | ≈ 50–120 Kč |
| **oběh:** Hall senzor A3144 + neodymový magnet ⌀6 × 2 (výchozí poloha) | 1 | ≈ 40–60 Kč |
| **hlava:** topný odpor 47 Ω / 1 W (2 ks ≈ 1 W, Camera Module 3 nad 0 °C a okénko bez rosy) | 2 | ≈ 10–20 Kč |
| MOSFET AO3400 / IRLZ44N 2× (laser + LED z GPIO), odpory, kabel, bužírka | 1 sada | ≈ 100–150 Kč |
| NTC 10 kΩ v nerezové jímce ⌀3 + odpor 10 kΩ 0,1 % (dno cely) | 2 | ≈ 150–400 Kč |
| ventilátor 80 mm 12 V + zdroj 12 V | 1 | ≈ 250–500 Kč |
| optočlen / relé modul 5 V (CR850 C4 → spouštění snímku) | 1 | ≈ 80–120 Kč |
| vývodka PG7 2×, Ethernet kabel 3 m | 1 | ≈ 150 Kč |

### 1.9 Fabory CZ / Hornbach – šrouby a spotřební materiál

| položka | ks | cena |
|---|---|---|
| šrouby M5 (20/12), M4×20, M3×20 + červík, M2,5×6 + distanční sloupky; M2×6 (Camera Module 3), M4 červíky 3× + matice (náboj ramene a kola) | sada | ≈ 300–500 Kč |
| **oběh:** šrouby M3 × 10 (3× svěrný kroužek, 2× rameno), M4 × 10 + matice (motor), M2 × 6 (kamera) | sada | ≈ 50 Kč |
| T-matice M5 navíc (oběh: P12 4×, P16 2×, P18 2×) | 8 | ≈ 1 €/ks |
| dvousložkový epoxid (dutina cely) | 1 | ≈ 250–400 Kč |
| PTFE sprej + silikonová vazelína (Molykote 111 – TME) | 1 | ≈ 400–600 Kč |
| spároměr 0,05–1,00 mm (kalibrace laseru) | 1 | ≈ 150–250 Kč |
| ocelové kolíky ⌀3 × 40 (4 ks) + tyčinka ⌀3 × 120 | 1 | ≈ 80 Kč |
| kontrolní miska ⌀100 × 20 (sklo / nerez) | 1 | ≈ 120 Kč |
| pěch ⌀95 (lze vytisknout) + kovové pravítko | 1 | ≈ 250 Kč |
| příchytky kabelů do drážky 8 + stahovací pásky | 4 | ≈ 100 Kč |
| sklo / plexi 50 × 50 × 2 mm do okénka boxu kamery | 1 | ≈ 50 Kč |
| bílá matná samolepka na terčík P03, značky ArUco 10 mm + ocelové měřítko 150 mm | 1 | ≈ 150 Kč |

## 2 · Fáze 2 – zátěž a sublimace (objednat po prvních cyklech fáze 1)

Stojan, kamera a laser zůstávají. Přibývá:

| položka | kde | ks | cena |
|---|---|---|---|
| LVDT RDP DCTH400AG, ±10 mm, DC vstup i výstup – předtím ověřit provoz při −10 °C | [Elkome](https://shop.elkome.com/en/dcth400ag-lvdt-displacement-sensor) (FI); česká alternativa [Micro-Epsilon CZ, Bechyně](https://www.micro-epsilon.cz/) | 1 | 581 € ≈ 14 500 Kč (ověřeno) |
| zdroj Mean Well HDR-15-24 (napájení LVDT) | TME | 1 | ≈ 11 € |
| L03 nosná deska Al 6, L04/L05 píst Al 10, 4× L06 ⌀165 × 6 (1 kg) + L07 ⌀165 × 3 (0,5 kg) – ocel (DXF) | [grupol.cz](https://grupol.cz/), alt. [Zamet](https://www.zamet.cz/laserove-rezani) | sada | ≈ 1 800–3 500 Kč |
| kulička 5/16", šroub DIN 912 M6 × 12 (nosná deska do čela tyče), šrouby M5 | Fabory CZ / cyklo prodejna | sada | ≈ 100–200 Kč |
| tisk P02, P09, P10, P11 (+ případně vyšší cela V03); pouzdro P01 už není potřeba – igus je v jádře oběhu P12 | vlastní tisk | – | filament z fáze 1 |
| **sublimace:** tenzometr 1 kg + HX711 | [LaskaKit](https://www.laskakit.cz/) / GM electronic | 1 | ≈ 150–300 Kč |
| **sublimace:** čidlo vlhkosti SHT45 (I²C) – povinné | RPishop.cz / LaskaKit (alt. SHT40) | 1 | ≈ 350–600 Kč |
| **sublimace:** skleněné misky ⌀90 (Petriho) | [P-LAB](https://www.p-lab.cz/) / [Verkon](https://www.verkon.cz/) | 3 | ≈ 200–400 Kč |
| **sublimace:** silikagel s indikátorem 2 kg + plastový tác | e-shopy se silikagelem / Hornbach | 1 | ≈ 400–700 Kč |
| **sublimace:** síto 2 mm (laboratorní nebo kuchyňské nerez) | Verkon / P-LAB / Hornbach | 1 | ≈ 150–400 Kč |

## 3 · Souhrn podle fáze (odhad)

| fáze | co | cena |
|---|---|---|
| 1 – bez zatížení | rám, cela, G10, Invar (obě tyče), laser, obíhající kamera (CM3, motor, ložiska 6806, igus) + RPi, LED, Campbell, elektronika, spotřební | ≈ 25 000–34 000 Kč |
| 2 – zátěž | LVDT + zdroj 24 V, kotouče a píst, šroub M6 | ≈ 17 000–19 000 Kč |
| 2 – sublimace | váha HX711, SHT45, misky, silikagel, síto | ≈ 1 300–2 400 Kč |
| **celkem** | | **≈ 43 000–55 000 Kč** |

Fáze 1 je bez LVDT zhruba o 17–19 tisíc Kč levnější. LVDT, největší položku (≈ 14 500 Kč), stačí koupit až před fází 2.

## 4 · Které soubory poslat které firmě

| firma | soubory | fáze |
|---|---|---|
| ENPRAG | `vyroba/narezy/E7_narezy_profily_ENPRAG.pdf`, text `poptavka_ramu.md` | 1 |
| Kovohutě Rokycany | `vyroba/narezy/E7_narezy_invar_Rokycany.pdf` (obě tyče) | 1 (+2) |
| Elektroizolanty Praha | `vyroba/narezy/E7_narezy_G10_Elektroizolanty.pdf` | 1 |
| vlastní tisk | `vyroba/tisk/E7-V03u_cell_D220x151_bez_zatizeni.stl`, P03–P07, P10u, oběh P12, P12b, P12c, P13–P16, P18, P19 | 1 |
| grupol.cz | `vyroba/laser/E7-L03…L07_*.dxf`, kontrola `vyroba/narezy/E7_narezy_laser_grupol.pdf` | 2 |
| všechny dohromady | `vyroba/narezy/E7_narezove_vykresy.pdf` (přehled N00 se sloupcem „fáze“, plány N01–N03 + výrobní výkresy) | – |

## 5 · Ověřit před objednáním

- **Tiskárna:** výška tisku ≥ 151 mm (cela fáze 1), pro fázi 2 ≥ 180 mm.
- **Mrazák (vnitřní 59 × 39 × 41 cm, š × h × v):** sestava fáze 1 je vysoká 383 mm (27 mm k víku), fáze 2 se zátěží 397 mm (13 mm k víku); půdorys s boxem RPi 415 × 320 mm. Proto: pryžové podložky místo noh, dno cely a podložky G10 20 mm, příčník 130 mm nad pískem, kotouče ⌀165 × 6, nosná deska Al 6 přišroubovaná M6 do tyče, laser 105 mm od osy, box RPi na sloupu (výkres V05).
- **grupol.cz:** zda řeže hliník 10 mm (až pro fázi 2).
- **LVDT RDP:** provoz při −10 °C (dotaz na Elkome, až pro fázi 2).
- **Fáze 2:** na straně kamery laser na invarový terčík nedosvítí, zakryje ho zátěžový sloupec. Kamera terčík vidí a posun rámu hlídá i LVDT na invarovém sloupku.
- **Oběh kamery ve fázi 2:** funguje stejně – hlava obíhá kolem tyče se závažím; ve fázi 2 se nic na oběhu nemění.
