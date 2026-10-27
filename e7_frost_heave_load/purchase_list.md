# E7 – variant C rev. B: what to buy (sensors, manufacturer, price, supplier)

Prices from online shops, October 2026; check them before ordering. 1 € ≈ 25 CZK.
Already available: printed cell, TDR CS645 + TDR100/200, Pt100, optical fibre, CR1000.
Rev. B follows the measurement review (`E7_review.pdf`). Czech version: `nakup_cidel.md`.

## Sensors and electronics

| # | Item | Manufacturer / type | Price | Where to buy |
|---|------|---------------------|-------|--------------|
| 1 | Camera computer (sits **inside** the camera box) | Raspberry Pi 5, 4 GB | 2,769 CZK incl. VAT | [RPishop.cz](https://www.zbozi.cz/vyrobek/raspberry-pi-5-rpi5-4gb-single/) |
| 1a | Power supply, SD card, camera cable | official 27 W supply, 32 GB card, Camera Cable Standard–Mini 200 mm | ≈ 400–600 CZK | RPishop.cz |
| 2 | Camera | Raspberry Pi HQ Camera, C/CS mount (OFI060), Sony IMX477 12 MP | 1,499 CZK incl. VAT | [RPishop.cz](https://rpishop.cz/mipi-kamerove-moduly/2458-raspberry-pi-hq-kamera.html), [Conrad.cz](https://www.conrad.cz/cs/p/raspberry-pi-sc1220-rasp-cam-hq-modul-barevne-kamery-cmos-vhodne-pro-vyvojove-sady-raspberry-pi-2264546.html) |
| 3 | Lens (rev. B: camera closer → 6 mm) | Raspberry Pi 6 mm CS wide-angle lens | est. 20–30 € | RPishop.cz, The Pi Hut |
| 4 | Camera box | XPS 30 mm, double-glazed window; the RPi 5 heats it (no heater foil) | est. 20–40 € | DIY store |
| 5 | Air humidity | SHT45 RH/T breakout on the RPi (I2C) | est. 15–25 € | RPishop.cz, LaskaKit, TME |
| 6 | Multi-line laser | Picotronic DOE253-635-1-6(10x22), order no. 70111842: 11 lines, 635 nm, 1 mW, 5 V | 91.51 € excl. VAT | [Picotronic (DE)](https://www.picotronic.de/picopage/en/product/detail/id/86333) |
| 7 | LVDT (piston) | RDP Electronics DCTH400AG: ±10 mm, spring return, ±5 V output | 581 € | [Elkome (FI)](https://shop.elkome.com/en/dcth400ag-lvdt-displacement-sensor) or RDP (UK) |
| 8 | LVDT power supply | Mean Well HDR-15-24, 24 V DIN (isolated) | ≈ 11 € excl. VAT | [TME](https://www.tme.com/ca/en/details/hdr-15-24/din-rail-mounting-power-supplies/mean-well/) |
| 9 | Pt100 module for the CR1000 | Campbell Scientific 4WPB100 | on request (est. 60–120 €) | [Ekotechnika, Černošice](https://campbellsci.com/ekotechnika), tel. +420 251 640 511 |
| 10 | Air temperature (**required**: boundary condition) | Campbell Scientific 109, 3 m cable | on request (est. 150–220 €) | Ekotechnika |
| 11 | Air mixing in the freezer | 80 mm 12 V fan (low-temperature bearing) | est. 10–20 € | TME, GM electronic |
| 12 | Camera calibration | shims 0.1 / 0.5 / 1.0 mm (feeler gauge set) | est. 10–25 € | tool shop |

## Mechanics (rev. B, estimates)

| Item | Price |
|------|-------|
| Al base plate 340 × 260 × 25 (machined) | 80–150 € |
| Al profiles 2× 40×80 × 326 + 80×80 × 340, core bolts | 80–170 € |
| **igus drylin RJ4JP-01-12** (dry plain bearing, same size as LM12UU) + **Invar 36 rod ⌀12 ground × 250** + steel ball ⌀8 | 60–140 € |
| **Invar 36 post ⌀16 × 405** + arms for the LVDT and the camera target | 60–140 € |
| **XPS 40**: sleeve ⌀240 × 130 + slab ⌀240; **3 G10 pads ⌀20 × 40** | 20–50 € |
| Al partial piston ⌀50 × 20 + carrier ⌀120 × 8 | 40–80 € |
| steel discs ⌀120: 4 × 1 kg + 0.5 kg + trim washers | 40–90 € |
| camera and laser brackets (Al strip), cable glands | 15–40 € |

Total ≈ 1,520–2,210 € excl. VAT, i.e. ≈ 38–55 thousand CZK (drawing V04). Rev. A was ≈ 1,370–1,870 €.
Invar 36 bar: ask a specialty metals supplier (e.g. Goodfellow, or a local distributor of Invar/FeNi36).

## Notes
- **Camera:** buy the HQ **C/CS** version, not M12. Rev. B camera is ≈ 135 mm from the centre of the surface;
  focus with the back-focus ring. The RPi 5 sits in the box, so only Ethernet and 5 V pass the lid seal.
- **Laser:** in rev. B it hangs from the beam at 68° (y 46, 115 mm above the sand, ≈ 124 mm from the centre):
  the 41° pattern then gives 11 lines at ≈ 9.6 mm on ⌀100 and the collar casts no shadow. Confirm the pattern size with Picotronic.
- **LVDT:** single isolated 24 V supply; ±5 V output straight into the CR1000. Confirm operation at −10 °C with RDP/Elkome.
- **4WPB100** only if your Pt100 is 4-wire and read directly by the CR1000.
- **Before buying:** decide the saturation of the sample (see the review). At Sr ≈ 0.4 the expected heave is tens of µm at most.
