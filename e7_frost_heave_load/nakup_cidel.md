# E7 – varianta C: co koupit (čidla, výrobce, cena, kde)

Ceny podle e-shopů 10/2026. Před objednáním je ověřte, mohou se změnit. Přepočet 1 € ≈ 25 Kč.
Už máte: tištěnou celu, TDR CS645 + TDR100/200, Pt100, optické vlákno a CR1000.

| # | Co | Výrobce / typ | Cena | Kde koupit |
|---|----|---------------|------|------------|
| 1 | Počítač ke kameře | Raspberry Pi 5, 4 GB | 2 769 Kč s DPH | [RPishop.cz](https://www.zbozi.cz/vyrobek/raspberry-pi-5-rpi5-4gb-single/) |
| 1a | Zdroj, SD karta, kabel ke kameře | oficiální zdroj 27 W, karta 32 GB, Camera Cable Standard–Mini 200 mm | ≈ 400–600 Kč | RPishop.cz; kabel také [Berrybase](https://www.berrybase.de/fr/raspberry-pi-camera-cable-standard-mini-200mm) 1,20 € |
| 2 | Kamera | Raspberry Pi HQ Camera, C/CS-mount (OFI060), Sony IMX477 12 MP | 1 499 Kč s DPH | [RPishop.cz](https://rpishop.cz/mipi-kamerove-moduly/2458-raspberry-pi-hq-kamera.html), [Conrad.cz](https://www.conrad.cz/cs/p/raspberry-pi-sc1220-rasp-cam-hq-modul-barevne-kamery-cmos-vhodne-pro-vyvojove-sady-raspberry-pi-2264546.html) 1 426 Kč |
| 3 | Objektiv | Arducam 8 mm, CS-mount, F1.4, ruční ostření | £16,40 / 19,90 € s DPH | [The Pi Hut](https://thepihut.com/products/cs-mount-lens-for-raspberry-pi-hq-camera-8mm-focal-length), [Welectron](https://welectron.com/Arducam-LN038-CS-Mount-Lens-for-Raspberry-Pi-HQ-Camera) |
| 4 | Vícečárový laser | Picotronic DOE253-635-1-6(10x22), obj. č. 70111842: 11 čar, 635 nm, 1 mW, 5 V, ⌀10 × 22 mm | 91,51 € bez DPH | [Picotronic (DE)](https://www.picotronic.de/picopage/en/product/detail/id/86333) |
| 5 | LVDT (zdvih pístu) | RDP Electronics DCTH400AG: ±10 mm, pružina, vestavěná elektronika DC/DC | 581 € | [Elkome (FI)](https://shop.elkome.com/en/dcth400ag-lvdt-displacement-sensor) nebo přímo RDP (UK) |
| 6 | Napájení LVDT | Mean Well HDR-15-24: 24 V, 15 W, DIN lišta (izolovaný = „plovoucí“ zdroj) | ≈ 11 € bez DPH | [TME](https://www.tme.com/ca/en/details/hdr-15-24/din-rail-mounting-power-supplies/mean-well/) (sklad CZ/PL) |
| 7 | Modul pro Pt100 do CR1000 | Campbell Scientific 4WPB100 (4vodičový můstek) | na dotaz (odhad 60–120 €) | [Ekotechnika, Černošice](https://campbellsci.com/ekotechnika), tel. 251 640 511 |
| 8 | Teplota vzduchu (volitelně) | Campbell Scientific 109 (termistor, −50…+70 °C), kabel 3 m | na dotaz (odhad 150–220 €) | Ekotechnika |
| 9 | Vyhřívaný box kamery | XPS 30 mm, topná fólie 12 V/5 W + termostat, okénko z 2 skel | odhad 40–80 € | kutilské potřeby, GM electronic, TME |

Celkem i s mechanikou je to ≈ 1 370–1 870 € bez DPH, tedy ≈ 34–47 tis. Kč (výkres V04).

## Poznámky k výběru
- **Kamera a objektiv:** kupte verzi HQ **C/CS**, ne M12, protože na verzi M12 objektivy CS nepasují.
  Objektiv má nejmenší zaostřovací vzdálenost 0,3 m, kamera je ≈ 0,17 m od povrchu. Doostření je potřeba udělat
  kroužkem zadní ohniskové vzdálenosti na HQ kameře (stačí posun ≈ 0,2 mm). Raspberry Pi 5 potřebuje kabel Standard–Mini.
- **Laser:** typ s 11 čarami a vlnovou délkou 650 nm se nenašel, nejbližší je typ s 635 nm. Pro kameru to nevadí.
  Podle katalogu má vzor úhel 41°, takže ze současné polohy laseru (≈ 134 mm od středu, 45°) vyjde na písku
  rozteč ≈ 14 mm. Na ⌀100 tak dopadne asi 7–8 čar místo 11 po 9 mm. Pro 9 mm je potřeba buď užší DOE (≈ 28°), nebo laser blíž.
  Rozměry vzoru si ověřte u Picotronicu.
- **Stín límce:** při 45° stíní límec (34 mm nad pískem) pruh písku u stěny na straně laseru, asi y = 25–50 mm,
  takže tam 2–3 čáry chybí. Strmější laser (≈ 65–70°) stín téměř odstraní, ale sníží citlivost
  (posun čáry ≈ 0,4 × zdvih místo 1 ×).
- **LVDT:** DCTH je napájen ze stejnosměrného zdroje: buď symetricky ±12…±18 V, nebo jediným 24–40 V,
  pokud je zdroj izolovaný. Výstup ±5 V jde přímo na CR1000 (VoltSE ±5000 mV). Zdroje uvádějí rozdílné
  provozní teploty (−40 až −10 °C dole), takže u RDP/Elkome ověřte provoz při −10 °C v truhle.
- **4WPB100** potřebujete jen tehdy, když je vaše Pt100 čtyřvodičová a měří se přímo CR1000.
