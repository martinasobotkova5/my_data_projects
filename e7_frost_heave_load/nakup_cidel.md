# E7 – varianta C rev. B: co koupit (čidla, výrobce, cena, kde)

Ceny podle e-shopů 10/2026; před objednáním ověřte. Přepočet 1 € ≈ 25 Kč.
Už máte: tištěnou celu, TDR CS645 + TDR100/200, Pt100, optické vlákno, CR1000.
Rev. B vychází z posudku měření (`E7_review.pdf`). Anglická verze: `purchase_list.md`.

## Čidla a elektronika

| # | Co | Výrobce / typ | Cena | Kde koupit |
|---|----|---------------|------|------------|
| 1 | Počítač ke kameře (je **uvnitř** boxu kamery) | Raspberry Pi 5, 4 GB | 2 769 Kč s DPH | [RPishop.cz](https://www.zbozi.cz/vyrobek/raspberry-pi-5-rpi5-4gb-single/) |
| 1a | Zdroj, SD karta, kabel ke kameře | oficiální zdroj 27 W, karta 32 GB, Camera Cable Standard–Mini 200 mm | ≈ 400–600 Kč | RPishop.cz |
| 2 | Kamera | Raspberry Pi HQ Camera, C/CS (OFI060), Sony IMX477 12 MP | 1 499 Kč s DPH | [RPishop.cz](https://rpishop.cz/mipi-kamerove-moduly/2458-raspberry-pi-hq-kamera.html), [Conrad.cz](https://www.conrad.cz/cs/p/raspberry-pi-sc1220-rasp-cam-hq-modul-barevne-kamery-cmos-vhodne-pro-vyvojove-sady-raspberry-pi-2264546.html) |
| 3 | Objektiv (rev. B: kamera blíž → 6 mm) | Raspberry Pi 6 mm CS širokoúhlý | odhad 20–30 € | RPishop.cz, The Pi Hut |
| 4 | Box kamery | XPS 30 mm, okénko ze 2 skel; ohřívá ho samo RPi 5 (bez topné fólie) | odhad 20–40 € | hobby market |
| 5 | Vlhkost vzduchu | SHT45 RH/T modul na RPi (I2C) | odhad 15–25 € | RPishop.cz, LaskaKit, TME |
| 6 | Vícečárový laser | Picotronic DOE253-635-1-6(10x22), obj. č. 70111842: 11 čar, 635 nm, 1 mW, 5 V | 91,51 € bez DPH | [Picotronic (DE)](https://www.picotronic.de/picopage/en/product/detail/id/86333) |
| 7 | LVDT (píst) | RDP Electronics DCTH400AG: ±10 mm, pružina, výstup ±5 V | 581 € | [Elkome (FI)](https://shop.elkome.com/en/dcth400ag-lvdt-displacement-sensor) nebo RDP (UK) |
| 8 | Napájení LVDT | Mean Well HDR-15-24, 24 V DIN (izolovaný) | ≈ 11 € bez DPH | [TME](https://www.tme.com/ca/en/details/hdr-15-24/din-rail-mounting-power-supplies/mean-well/) |
| 9 | Modul pro Pt100 do CR1000 | Campbell Scientific 4WPB100 | na dotaz (odhad 60–120 €) | [Ekotechnika, Černošice](https://campbellsci.com/ekotechnika), tel. 251 640 511 |
| 10 | Teplota vzduchu (**povinně** – okrajová podmínka) | Campbell Scientific 109, kabel 3 m | na dotaz (odhad 150–220 €) | Ekotechnika |
| 11 | Promíchání vzduchu v truhle | ventilátor 80 mm 12 V (ložisko do mrazu) | odhad 10–20 € | TME, GM electronic |
| 12 | Kalibrace kamery | podložky 0,1 / 0,5 / 1,0 mm (spároměrky) | odhad 10–25 € | nářadí |

## Mechanika (rev. B2 – objednatelná bez obrábění; podrobně po obchodech v `objednavka.md`)

| Co | Cena |
|----|------|
| Laser: Al 10 základní deska 340×260 a horní deska 340×80, nosná deska ⌀120, 2 kotouče pístu ⌀50; ocelové kotouče ⌀117,5 × 12 (4×) a × 6 (1×) | 100–190 € |
| Profily 40×80 drážka 8 × 326 (2×), 8 úhelníků, T-matice, 3 nohy M8 (Enprag) | 60–110 € |
| igus RJ4JP-01-12, stavěcí kroužek DIN 705-A 12, kulička 5/16", šrouby | 25–50 € |
| Invar 36: tyč ⌀12 × 289 a sloupek ⌀16 × 357, řez na délku (Evek) | 80–160 € |
| Cela tištěná VCELKU ⌀240 × 200 (PETG-CF ≈ 1,5 kg) + 3 podložky G10 ⌀20 × 40 (elektroizolanty.cz) | 45–90 € |
| Tištěné díly P01–P08: pouzdro ložiska, ramena LVDT a terčíku, patka sloupku, držák laseru, box kamery | 10–25 € |

Celkem ≈ 1 450–1 980 € bez DPH, tj. ≈ 36–50 tis. Kč (výkres V04). Rev. A byla ≈ 1 370–1 870 €.
Invar 36 (FeNi36): poptat u dodavatele speciálních kovů (např. Goodfellow nebo tuzemský distributor).

## Poznámky
- **Kamera:** verze HQ **C/CS**, ne M12. V rev. B je ≈ 135 mm od středu povrchu; doostřit kroužkem zadní ohniskové vzdálenosti.
  RPi 5 je v boxu, takže těsněním víka vede jen Ethernet a 5 V.
- **Laser:** v rev. B visí z příčníku pod 68° (y 46, 115 mm nad pískem, ≈ 124 mm od středu): vzor 41° dá 11 čar po ≈ 9,6 mm
  na ⌀100 a límec nestíní. Velikost vzoru ověřit u Picotronicu.
- **LVDT:** jeden izolovaný zdroj 24 V; výstup ±5 V přímo do CR1000. Provoz při −10 °C ověřit u RDP/Elkome.
- **4WPB100** jen pokud je Pt100 čtyřvodičová a měří se přímo CR1000.
- **Před nákupem:** rozhodnout nasycení vzorku (viz posudek). Při Sr ≈ 0,4 bude zdvih nanejvýš desítky µm.
