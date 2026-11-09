# E7 – varianta C rev. B3: objednávka a sestavení

Vše, co je potřeba koupit, nechat vyrobit podle rozměrů a sestavit. Sestava je navržená tak, aby **nebylo potřeba soustružit ani frézovat**: celý rám je z T-profilů drážka 8, které se jen řežou na délku (jediný otvor ⌀14 v horním příčníku), kotouče se řežou laserem podle DXF, zbytek se tiskne. Výkresy: V01–V06 (`vykresy/E7_drawings.pdf`), výrobní soubory: `vyroba/laser` (DXF) a `vyroba/tisk` (STL/STEP).

**Už máte:** CR850, TDR100/200 + CS645, Pt100, optické vlákno + čtečku, truhlicový mrazák s regulátorem (E6).

Ceny: „ověřeno“ = nalezeno na webu prodejce v 10/2026 (ověřte před objednáním), „odhad/poptat“ = cenu je třeba zjistit. 1 € ≈ 25 Kč.

## 1 · Laserové řezání podle DXF (jedna objednávka)

Kde: [grupol.cz](https://grupol.cz/) – nahrát DXF, cena hned; alternativy [Zamet](https://www.zamet.cz/laserove-rezani) (ocel do 20 mm), [Light Cut](https://lightcut.cz/co-umime/rezani-laserem/)

| položka | specifikace | ks | cena | stav |
|---|---|---|---|---|
| E7-L03_carrier | Al EN AW-5754, tl. 10 mm – soubor `vyroba/laser/E7-L03_carrier_10mm.dxf` | 1 |  |  |
| E7-L04_piston_top | Al EN AW-5754, tl. 10 mm – soubor `vyroba/laser/E7-L04_piston_top_10mm.dxf` | 1 |  |  |
| E7-L05_piston_bottom | Al EN AW-5754, tl. 10 mm – soubor `vyroba/laser/E7-L05_piston_bottom_10mm.dxf` | 1 |  |  |
| E7-L06_disc_1kg | steel S235JR, tl. 12 mm – soubor `vyroba/laser/E7-L06_disc_1kg_12mm.dxf` | 4 |  |  |
| E7-L07_disc_0.5kg | steel S235JR, tl. 6 mm – soubor `vyroba/laser/E7-L07_disc_0.5kg_6mm.dxf` | 1 |  |  |
| — | Hliník 10 mm: ověřit, že ho laser zvládne; jinak stejné DXF na vodní paprsek. Ocel 12 mm: kotouče převážit, ±0,5 mm tloušťky = ±4 % hmotnosti |  | ≈ 70–140 € celkem | odhad |

## 2 · Hliníkové T-profily (drážka 8) a spojovací díly rámu – celý rám jako jedna sada

Kde: **doporučeno: [ENPRAG, s.r.o., Praha 5](https://www.enprag.cz/hlinikove-profily/c-6027)** (česká firma, IČO 62743741, K Holyni 833/42, tel. +420 224 942 663, zdarma 800 888 868) – profily drážka 8 (kompatibilní s item/Bosch) nařeže podle zadání, dodá je s návodem k montáži a výrobním výkresem, nebo jako **kompletně sestavenou konstrukci**, návrh s 3D vizualizací zdarma; poslat výkresy T01–T04 (`vyroba/vykresy`) a tabulku níže, požádat o vyvrtání ⌀14 v T04 a o celou sadu spojovacího materiálu (poptávka: `poptavka_ramu.md`). Alternativy: [Alutec K&K s.r.o.](https://katalog.aluteckk.cz/kategorie-produktu/modul-40-drazka-8/) (český výrobce, modul 40 drážka 8, délka na zakázku, úhelníky, matice), [Profimet](https://profimet.cz/sluzby/) (profily dle výkresu), [eProfily.cz](https://www.eprofily.cz/hlinikovy-profil-80x40-s-drazkou-8-mm/kat3007.html). Na Alze konstrukční profily nejsou.

| položka | specifikace | ks | cena | stav |
|---|---|---|---|---|
| T01 profil 40×80 drážka 8 – sloup | řez na délku 306 mm, kolmý řez ±0,2 | 2 | 31,43 €/m bez DPH (+ řez) | ověřeno (Enprag EN) |
| T02 profil 40×40 drážka 8 – podélník základny | řez na délku 320 mm, kolmý řez ±0,2 | 2 | ≈ 15–20 €/m (+ řez) | odhad |
| T03 profil 40×80 drážka 8 – příčka základny | řez na délku 260 mm, kolmý řez ±0,2 | 1 | 31,43 €/m bez DPH (+ řez) | ověřeno (Enprag EN) |
| T04 profil 40×80 drážka 8 – horní příčník | řez na délku 340 mm, kolmý řez ±0,2; uprostřed svislý otvor ⌀14 skrz | 1 | 31,43 €/m bez DPH (+ řez) | ověřeno (Enprag EN) |
| — | celkem 40×80: 1,21 m, 40×40: 0,64 m |  |  |  |
| Úhelník 40×40 drážka 8 (Zn) s krytkou | 4 příčka ↔ podélníky, 4 sloupy ↔ podélníky, 4 sloupy ↔ příčník | 12 | ≈ 3–6 €/ks | odhad |
| T-matice drážka 8, M8, vkládací (otočná) | úhelníky (24) + nohy (4) + 4 rezerva | 32 | ≈ 1 €/ks | odhad |
| T-matice drážka 8, M5, vkládací (otočná) | pouzdro P01 (4), patka P04 (2), držák laseru P05 (2), závěs kamery P08 (2) + 2 rezerva | 12 | ≈ 1 €/ks | odhad |
| Stavitelná noha M8 (talíř ⌀30–40) | do T-matic ve spodní drážce podélníků T02 (y ±140) | 4 | ≈ 3–5 €/ks | odhad |
| Krytka čela 40×80 / 40×40 (volitelně) | konce příčníku a podélníků | 6 | ≈ 0,5 €/ks | odhad |

## 3 · Invar 36 (tyče řezané na délku)

Kde: **česky:** [Kovohutě Rokycany](http://www.koro.cz/produkty/nikl-a-slitiny-niklu/) – FeNi36 (1.3912) tyče ⌀10–200 mm, délky 1–5 m, sales@koro.cz – poptat 2 krátké kusy nebo řez; jinak [Evek – Invar 36 kulatina](https://evek.vip/slitina-niklu/451-ty%C4%8D-invar36-%C3%B8-2mm-70mm-13912-ty%C4%8D-kulat%C3%A1-nilo-36-alloy-36-uns-k93600.html) (1.3912, česky, řez na míru)

| položka | specifikace | ks | cena | stav |
|---|---|---|---|---|
| Invar 36 ⌀12 | délka 265 mm, tolerance h9 nebo lepší (vodicí tyč pro kluzné pouzdro), čela kolmá, sražení 0,5×45° | 1 |  | poptat |
| Invar 36 ⌀16 | délka 330 mm, čela kolmá | 1 |  | poptat |
| — | obojí ≈ 0,9 kg Invaru |  | ≈ 80–160 € | odhad |

## 4 · Podložky G10 (sklotextit)

Kde: [Elektroizolanty Praha – tyče G10](https://www.elektroizolanty.cz/elektroizonlanty/eshop/57-1-Tyce-G10-130-C-akcni-ceny)

| položka | specifikace | ks | cena | stav |
|---|---|---|---|---|
| Sklotextit G10 tyč ⌀20 × 1000 mm | požádat o nařezání 3× 40 mm (čela rovnoběžná) – nebo nařezat v dílně | 1 | 298 Kč | ověřeno |

## 5 · Ložisko, kroužek, kulička, šrouby

Kde: igus v ČR: [HENNLICH s.r.o., Litoměřice](https://www.igus.eu/Contact/general/CZ) – skladový distributor, tel. +420 416 711 333; nebo [TME](https://www.tme.eu/cz/) (igus drylin); [Fabory CZ – stavěcí kroužky](https://www.fabory.com/cs/Fasteners/Washers-and-Rings/Adjusting-rings/c/011001); šrouby Hornbach / Fabory; kulička v cyklo obchodě

| položka | specifikace | ks | cena | stav |
|---|---|---|---|---|
| igus drylin RJ4JP-01-12 | kluzné pouzdro ⌀12 (⌀21 × 30), bez maziva, do −40 °C | 1 | ≈ 2–5 € | odhad |
| Stavěcí kroužek DIN 705-A 12 (⌀22 × 12, šroub M6) | pod nosnou desku závaží (+1 rezerva) | 2 | ≈ 2–4 €/ks | odhad |
| Ocelová ložisková kulička 5/16" (7,94 mm) | cyklo kuličky, balení | 1 | ≈ 1–3 € | odhad |
| Imbus ISO 4762 M8×16 + podložka | úhelníky do T-matic | 24 |  | sada |
| Imbus ISO 4762 M5×35 + podložka | pouzdro ložiska P01 ↔ T-matice ve spodní drážce T04 | 4 |  | sada |
| Imbus ISO 4762 M5×20 + podložka | patka sloupku P04 ↔ T-matice v podélníku | 2 |  | sada |
| Imbus ISO 4762 M5×12 + podložka | držák laseru P05 a závěs kamery P08 ↔ boční drážky T04 | 4 |  | sada |
| Šroub M4×20 + matice | box kamery ↔ závěs, svěrky | 4 |  | sada |
| Šroub M3×20 + matice, červík M3×6 | svěrky ramen (3), aretace laseru (1) | 4 |  | sada |
| Šroubky M2,5×6 + distanční sloupky 10 mm | HQ kamera (4) a RPi 5 (4) v boxu | 8 |  | sada |
| — | spojovací materiál celkem |  | ≈ 15–25 € | odhad |

## 6 · 3D tisk (vlastní tiskárna)

Kde: [Prusament PETG Carbon Fiber](https://www.prusa3d.com/product/prusament-petg-carbon-fiber-black-1kg/) (Prusa, CZ)

| položka | specifikace | ks | cena | stav |
|---|---|---|---|---|
| Prusament PETG Carbon Fiber 1 kg | cela ≈ 1,3–1,6 kg + díly P01–P11 ≈ 0,5 kg | 2 | ≈ 55 €/ks | ověřeno (USD cena) |
| Tiskárna pro celu | podložka ≥ 250 × 250, výška ≥ 200 (Prusa XL, Bambu X1/P1S); Prusa MK4/Core One nestačí |  |  | info |
| Sklo do okénka boxu kamery | 50 × 50 × 2 mm (sklo z fotorámečku / sklenářství) nebo plexi 2 mm | 1 | ≈ 1–3 € | odhad |

## 7 · Kamera, Raspberry Pi, elektronika

Kde: [RPishop.cz](https://rpishop.cz/), [LaskaKit](https://www.laskakit.cz/), [GM electronic](https://www.gme.cz/), [TME](https://www.tme.eu/cz/)

| položka | specifikace | ks | cena | stav |
|---|---|---|---|---|
| Raspberry Pi 5, 4 GB |  | 1 | 2 769 Kč | ověřeno |
| Raspberry Pi HQ Camera C/CS (OFI060) | ne verze M12 | 1 | 1 499 Kč | ověřeno |
| Raspberry Pi 6 mm CS objektiv (širokoúhlý) |  | 1 | ≈ 20–30 € | odhad |
| Kabel kamery Standard–Mini 200 mm, zdroj 27 W, microSD 32 GB |  | 1 | ≈ 400–600 Kč | odhad |
| Čidlo SHT45 (RH/T) na I2C | vlhkost vzduchu v truhle | 1 | ≈ 15–25 € | odhad |
| Ventilátor 80 mm 12 V + zdroj 12 V | promíchání vzduchu (běží trvale) | 1 | ≈ 10–20 € | odhad |
| Mean Well HDR-15-24 (24 V DIN) | napájení LVDT (trvale zapnuté) | 1 | ≈ 11 € bez DPH | ověřeno (TME) |
| Kabelová vývodka PG7 + Ethernet kabel 3 m | box kamery | 1 | ≈ 5 € | odhad |
| Optočlen / relé modul 5 V pro spouštění snímku | CR850 C4 → GPIO RPi | 1 | ≈ 3–5 € | odhad |

## 8 · Čidla ze zahraničí a Campbell

Kde: Picotronic (DE), Elkome (FI), [Ekotechnika Černošice](https://campbellsci.com/ekotechnika) (Campbell pro ČR)

| položka | specifikace | ks | cena | stav |
|---|---|---|---|---|
| Laser Picotronic DOE253-635-1-6(10x22), obj. č. 70111842 | 11 čar, 635 nm, 1 mW, 5 V, ⌀10 × 22 | 1 | 91,51 € bez DPH | ověřeno – [shop](https://www.picotronic.de/picopage/en/product/detail/id/86333) |
| LVDT RDP DCTH400AG | ±10 mm, pružina, tělo ⌀20,6; ověřit provoz při −10 °C | 1 | 581 € | ověřeno – [Elkome](https://shop.elkome.com/en/dcth400ag-lvdt-displacement-sensor) |
| Campbell 4WPB100 | modul pro 4vodičové Pt100 | 1 | ≈ 60–120 € | poptat – tel. +420 251 640 511 |
| Campbell 109-L, kabel 3 m | teplota vzduchu (povinně) | 1 | ≈ 150–220 € | poptat |

## 8a · České firmy / české zastoupení pro kameru, laser a LVDT (alternativy k bodu 8; doporučeno zůstat u bodu 8 – RPishop.cz, Picotronic, Elkome – rameno P02 a držák P05 jsou nakreslené přesně pro tato čidla; Micro-Epsilon CZ poptat jako srovnání)

Kde: vybrat jednu možnost v každém řádku; u jiného průměru těla LVDT / laseru upravit svěrku P02 / držák P05

| položka | specifikace | ks | cena | stav |
|---|---|---|---|---|
| Kamera: Raspberry Pi HQ + 6 mm objektiv + RPi 5 | [RPishop.cz](https://rpishop.cz/mipi-kamerove-moduly/2458-raspberry-pi-hq-kamera.html) – oficiální Raspberry Pi Approved Reseller, České Budějovice; Raspberry Pi prodává i [Alza](https://www.alza.cz/18852654-v3978.htm) | 1 | 1 499 + 2 769 Kč | ověřeno |
| Kamera (průmyslová varianta) | [ATEsystem Ostrava](https://eshop.atesystem.cz/c/2158/prumyslove-kamery) – výhradní distributor Basler pro ČR a SK, objektivy Computar/Tamron, osvětlení Smart View (CZ); potřebuje PC | 1 | poptat | info |
| Laser 11 rovnoběžných čar: Laser Components FLEXPOINT FP-DOE s DOE-233 (11 čar) | český e-shop [TME](https://www.tme.eu/cz/) (řada FLEXPOINT) nebo [Distrelec CZ](https://www.distrelec.cz/cs/pf/1633857); obě firmy jsou zahraniční, česky prodávající; český výrobce ani distributor 11čárového laseru nenalezen; DOE 5/7/11/25/65 čar ([katalog](https://media.distrelec.com/Web/Downloads/_t/ds/flexpoint_eng_tds.pdf)); modul ⌀11,5 → držák P05 na ⌀11,7 | 1 | poptat | info |
| Laser (jednoduchý, česky) | [laser-shop.cz](https://laser-shop.cz/115-laserove-moduly-prumyslove/) – čárové moduly 650 nm (1 čára) a mřížka 8 × 8; 11 rovnoběžných čar nemají |  |  | info |
| LVDT: Micro-Epsilon induSENSOR DTA-10D (±10 mm) + kontrolér MSC7401 (analog U/I) | [Micro-Epsilon Czech Republic, Bechyně](https://www.micro-epsilon.cz/displacement-position-sensors/inductive-sensor-lvdt/Spannhubsensor/) – česká pobočka výrobce, info@micro-epsilon.cz | 1 | poptat | doporučeno |
| LVDT: Omega LD620-10 (±10 mm, ±5 V DC, napájení 10–30 V) | [DwyerOmega CZ](https://www.jakar.cz/p/lvdt-linearni-snimac-polohy-s-ac-vystupem/6465) – stejné zapojení jako RDP DCTH (DC vstup i výstup), tělo ⌀19 | 1 | ≈ 1 000 USD (US ceník) | poptat |
| LVDT: HBM WA/10 mm (±10 mm, pružinový hrot) | [HBP měřicí technika s.r.o., Praha 4](https://www.hbm.cz/en/produkty/kategorie/wa/) – zastoupení HBK/HBM, tel. +420 224 921 861, hbmcz@hbm.cz; pasivní indukční snímač – potřebuje zesilovač s nosnou frekvencí, ne přímo CR850 | 1 | poptat | info |
| LVDT pro laboratoře (geotechnika) | [Labtech – stroje pro zkušebnictví](https://www.strojeprozkusebnictvi.cz/lvdt-snimac-polohy.html) – autorizovaný distributor, poptat ±10 mm s DC výstupem | 1 | poptat | info |
| LVDT Solartron | [RS Components CZ](https://cz.rs-online.com/web/b/solartron-metrology) – sondy ±10 mm; AC verze potřebují převodník | 1 | ≈ 390 € (PT ceník) | info |

## 9 · Spotřební materiál

Kde: Hornbach / OBI, [TME](https://www.tme.eu/cz/) (Molykote)

| položka | specifikace | ks | cena | stav |
|---|---|---|---|---|
| Dvousložkový epoxid | nátěr dutiny cely + slepení pístu (L04 + L05) | 1 | ≈ 10–15 € | odhad |
| PTFE sprej + silikonová vazelína (Molykote 111) | stěna dutiny | 1 | ≈ 15–25 € | odhad |
| Spároměr 0,05–1,00 mm | kalibrace kamery (0,1 / 0,5 / 1,0 mm) | 1 | ≈ 5–10 € | odhad |
| Bílá matná samolepka / papír 12 × 12 | terčík na rameno P03 | 1 |  |  |
| Ocelové kolíky / hřebíky ⌀3 × 40 (4 ks) + ocelová tyčinka ⌀3 × 120 | zátky otvorů pro tyčky TDR a Pt100 při hutnění; předvrtání kanálků před zasunutím čidel | 1 | ≈ 3 € | odhad |
| Kontrolní miska ⌀100 × 20 (sklo / nerez) | „svědek“ odpařování: stejný písek, váží se každý cyklus (cela se neváží) | 1 | ≈ 5 € | odhad |
| Pěch ⌀95 (ocel / PETG) + kovové pravítko | hutnění po vrstvách 20 mm mimo rám na rovné podložce | 1 | ≈ 10 € | odhad |
| Příchytky kabelů do drážky 8 + stahovací pásky | kabely TDR / Pt100 / vlákna k podélníku – netahají za celu | 4 | ≈ 1 €/ks | odhad |

## Rozměry pro kontrolu (z modelu)

- sloupy 306 mm, Invarová tyč 265 mm, Invarový sloupek 330 mm
- nosná deska závaží 383 mm nad horní plochou rámu; spodní líc příčníku 306 mm
- kotouč 117.5 × 12 mm = 1.00 kg, poloviční 0.50 kg
- kontrola kolizí v 3D sestavě (model3d.py): bez kolizí

## Postup sestavení

1. Vytiskněte celu (V03) a díly P01–P11 (`vyroba/tisk/*.stl`, PETG-CF, 0,2 mm, 3 perimetry, 40 % gyroid; cela podle V03). Dutinu cely natřete epoxidem, po vytvrzení PTFE sprej + tenká vrstva silikonové vazelíny.
2. Píst: kotouče L05 (spodní) a L04 (horní, otvor ⌀6) slepte epoxidem, soustředně.
3. Základ: 2 podélníky T02 (40×40 × 320, osy x = ±150) a mezi ně příčku T03 (40×80 naplocho × 260, osa y = 8,75) – 4 úhelníky, M8×16 do vkládacích T-matic. Do spodní drážky podélníků 4 stavitelné nohy M8 (y ±140). Rám vyrovnejte vodováhou. Na příčku položte 3 podložky G10 (poloha podle kapes ve dně cely, V06).
4. Sloupy T01 (40×80 × 306) postavte na podélníky (osa x = ±150, uprostřed délky) a připojte 2 úhelníky na stranách ±y (M8×16 + T-matice). Srovnejte do pravého úhlu, dotáhněte.
5. Pouzdro P01 přišroubujte zespodu na horní příčník T04 (4× M5×35 do T-matic ve spodních drážkách), souose s otvorem ⌀14; vložte igus RJ4JP-01-12 a stáhněte svěrný šroub M4.
6. Příčník T04 položte naplocho na sloupy, 2 úhelníky na vnitřní straně každého sloupu (pod příčníkem). Otvor ⌀14 musí být nad středem cely – srovnejte podle olovnice nebo trnu ⌀12 v pouzdře, pak dotáhněte.
7. Připravte vzorek mimo rám podle `postup_zkousky.md` (vlhčení, hutnění po vrstvách se zátkami v otvorech čidel, srovnání stěrkou P10, zasunutí čidel). Celu postavte na podložky G10 – kapsy ve dně na podložky; cela se nedotýká rámu.
8. Invarový sloupek ⌀16 postavte do patky P04 (2× M5×20 do T-matic v horní drážce pravého podélníku, y = 108); sloupek stojí na dně patky, svěrku dotáhněte. Nasaďte rameno P03 (terčík ve výšce horní hrany límce) a rameno P02 s LVDT.
9. Navrch písku položte píst, do otvoru ⌀6 kuličku 5/16". Na límec nasaďte středicí víčko P09 (rameno P03 natočené stranou).
10. Invarovou tyč zasuňte shora pouzdrem víčkem P09 až na kuličku – posunutím cely ji vystřeďte, víčko vysuňte do strany, rameno P03 vraťte na značku. Na tyč stavěcí kroužek, na něj nosná deska L03 a kotouče L06/L07. Kroužek nastavte tak, aby nosná deska byla 37 mm nad horní plochou příčníku T04 (spodní hrana kroužku 25 mm nad ním = zdvih ±25).
11. LVDT posuňte ve svěrce P02, až je jádro uprostřed rozsahu (výstup ≈ 0 V), dotáhněte.
12. Laser do držáku P05 (2× M5×12 do boční drážky T04, +y), kameru + RPi 5 do boxu P06/P07 (sklo do drážky, kabel přes PG7), box na závěs P08 (2× M5×12 do boční drážky T04, −y). Laser natočte, aby čáry ležely napříč přes celý povrch ⌀100; kameru zaostřete (zadní ohnisková vzdálenost).
13. Slepá zkouška s hliníkovou atrapou (V02) → kalibrace podložkami → první cyklus.

Celkem (V04): čidla a elektronika + mechanika ≈ 1 450–1 980 € bez DPH, tj. ≈ 36–50 tis. Kč.
