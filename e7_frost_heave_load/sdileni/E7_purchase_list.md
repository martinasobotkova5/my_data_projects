# E7 – variant C: what to buy (sensors, manufacturer, price, supplier)

Prices from online shops, October 2026; check them before ordering. 1 € ≈ 25 CZK.
Already available: printed cell, TDR CS645 + TDR100/200, Pt100, optical fibre, CR1000.
(Czech version: `nakup_cidel.md`.)

| # | Item | Manufacturer / type | Price | Where to buy |
|---|------|---------------------|-------|--------------|
| 1 | Camera computer | Raspberry Pi 5, 4 GB | 2,769 CZK incl. VAT | [RPishop.cz](https://www.zbozi.cz/vyrobek/raspberry-pi-5-rpi5-4gb-single/) |
| 1a | Power supply, SD card, camera cable | official 27 W supply, 32 GB card, Camera Cable Standard–Mini 200 mm | ≈ 400–600 CZK | RPishop.cz; cable also [Berrybase](https://www.berrybase.de/fr/raspberry-pi-camera-cable-standard-mini-200mm) 1.20 € |
| 2 | Camera | Raspberry Pi HQ Camera, C/CS mount (OFI060), Sony IMX477 12 MP | 1,499 CZK incl. VAT | [RPishop.cz](https://rpishop.cz/mipi-kamerove-moduly/2458-raspberry-pi-hq-kamera.html), [Conrad.cz](https://www.conrad.cz/cs/p/raspberry-pi-sc1220-rasp-cam-hq-modul-barevne-kamery-cmos-vhodne-pro-vyvojove-sady-raspberry-pi-2264546.html) 1,426 CZK |
| 3 | Lens | Arducam 8 mm, CS mount, F1.4, manual focus | £16.40 / 19.90 € incl. VAT | [The Pi Hut](https://thepihut.com/products/cs-mount-lens-for-raspberry-pi-hq-camera-8mm-focal-length), [Welectron](https://welectron.com/Arducam-LN038-CS-Mount-Lens-for-Raspberry-Pi-HQ-Camera) |
| 4 | Multi-line laser | Picotronic DOE253-635-1-6(10x22), order no. 70111842: 11 lines, 635 nm, 1 mW, 5 V, ⌀10 × 22 mm | 91.51 € excl. VAT | [Picotronic (DE)](https://www.picotronic.de/picopage/en/product/detail/id/86333) |
| 5 | LVDT (piston heave) | RDP Electronics DCTH400AG: ±10 mm, spring return, built-in DC/DC electronics | 581 € | [Elkome (FI)](https://shop.elkome.com/en/dcth400ag-lvdt-displacement-sensor) or directly from RDP (UK) |
| 6 | LVDT power supply | Mean Well HDR-15-24: 24 V, 15 W, DIN rail (isolated, i.e. floating supply) | ≈ 11 € excl. VAT | [TME](https://www.tme.com/ca/en/details/hdr-15-24/din-rail-mounting-power-supplies/mean-well/) |
| 7 | Pt100 module for the CR1000 | Campbell Scientific 4WPB100 (4-wire bridge) | on request (est. 60–120 €) | [Ekotechnika, Černošice](https://campbellsci.com/ekotechnika), tel. +420 251 640 511 |
| 8 | Air temperature (optional) | Campbell Scientific 109 (thermistor, −50…+70 °C), 3 m cable | on request (est. 150–220 €) | Ekotechnika |
| 9 | Heated camera box | XPS 30 mm, 12 V / 5 W heater foil + thermostat, double-glazed window | est. 40–80 € | DIY store, GM electronic, TME |

Total including mechanics ≈ 1,370–1,870 € excl. VAT, i.e. ≈ 34–47 thousand CZK (drawing V04).

## Notes on the selection
- **Camera and lens:** buy the HQ **C/CS** version, not M12; CS lenses do not fit the M12 version.
  The lens focuses from 0.3 m, the camera is ≈ 0.17 m from the surface: refocus with the back-focus ring
  of the HQ camera (≈ 0.2 mm is enough). The Raspberry Pi 5 needs the Standard–Mini cable.
- **Laser:** no 11-line module at 650 nm was found; the closest is 635 nm, which is fine for the camera.
  The catalogue gives a 41° pattern, so from the current laser position (≈ 134 mm from the centre, 45°) the line
  spacing on the sand is ≈ 14 mm, i.e. about 7–8 lines on ⌀100 instead of 11 at 9 mm. A 9 mm spacing needs a narrower
  DOE (≈ 28°) or a laser closer to the sample. Confirm the pattern dimensions with Picotronic.
- **Collar shadow:** at 45°, the collar (34 mm above the sand) shadows a strip of sand next to the wall on the laser
  side, about y = 25–50 mm, so 2–3 lines are missing there. A steeper laser (≈ 65–70°) almost removes the shadow
  but lowers the sensitivity (line shift ≈ 0.4 × heave instead of 1 ×).
- **LVDT:** the DCTH runs on DC: either ±12…±18 V, or a single 24–40 V supply if it is isolated.
  The ±5 V output goes straight into the CR1000 (VoltSE ±5000 mV). Sources disagree on the operating temperature
  (−40 °C or only −10 °C at the low end), so confirm operation at −10 °C in the freezer with RDP/Elkome.
- **4WPB100** is needed only if your Pt100 is 4-wire and read directly by the CR1000.
