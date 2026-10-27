"""Sensor selection and CR1000 channel plan for E7 (both rigs in one freezer).

PICK = recommended model per tag (shown on the drawings).
OPTIONS = alternatives from other makers (sheet E7-V05).
Specs from manufacturer / distributor pages found by web search (README §7);
[U] = not confirmed, ask the supplier.
"""

# tag: (what it measures, recommended model, short spec, CR1000 connection)
PICK = {
    "LVDT": ("rig A: check that the sample does not move", "RDP DCTH400",
             "DC-LVDT ±10 mm, spring plunger, ±5 V out, −40…+80 °C", "SE1–2, VoltSE ±5 V"),
    "LVDT-B": ("rig B: surface S1–S3 and anchors E1–E3", "RDP DCTH200, free core [U]",
               "DC-LVDT ±5 mm, unguided core (no spring force), ±5 V out", "SE3–8, VoltSE ±5 V"),
    "T": ("soil, cell wall, piston, pedestal", "Campbell 109SS",
          "⌀1.6 mm sheath, ±0.38 °C at 0 °C", "MUX-2 → SE13, VX2"),
    "PC": ("stress inside the sand (A)", "TML PDA-PA 200 kPa on ⌀20×2 disc",
           "⌀6.5×1 mm, 0.8 mV/V, 350 Ω, comp. −10…+60 °C", "MUX-1 (4×16), BrFull, VX3 2 V"),
    "PW": ("stress on wall / base", "TML PDA-PA 200 kPa (flush)",
           "same, in ⌀8 holder flush with the surface", "MUX-1 (4×16), BrFull, VX3 2 V"),
    "TDR": ("point M: water content (frozen: unfrozen water)", "mini 3-rod TDR 40 mm [U] + TDR200",
            "3 rods ⌀1.6 × 40, 5 mm apart; TDR200 + SDMX50SP", "SDM C1–C3"),
    "PT100": ("point M: reference temperature", "Pt100 1/10 DIN, 4-wire, ⌀3",
              "±0.03 °C at 0 °C (1/10 B), sheath ⌀3 × 70", "MUX-1 + 4WPB100, BrHalf4W"),
    "FBG": ("point M: optical temperature", "FBG temp. sensor in capillary ⌀1 [U]",
            "≈ 10 pm/K, strain-free; interrogator outside", "PC (Ethernet), time-synced"),
    "TX": ("frame, Invar stand, air", "Campbell 109SS / 107",
           "107: ⌀7.6 mm, ±0.2 °C (0–50 °C)", "MUX-2 → SE13, VX2"),
}

# (category, maker + model, key specs, verdict)
OPTIONS = [
    ("LVDT ±10", "RDP DCTH400", "±5 V / 0–10 V out, −40…+80 °C, ±0.25 % FS", "PICK (A)"),
    ("LVDT ±10", "Micro-Epsilon DTA-10D + MSC7401", "0–5 V / 4–20 mA, −20…+80 °C", "alternative"),
    ("LVDT ±10", "Solartron AX/10/S + OD5", "±5 V out, needs 230 V conditioner", "alternative"),
    ("LVDT ±10", "HBM WA-L 20 mm", "passive, needs carrier amplifier", "alternative"),
    ("LVDT free", "RDP DCTH200 unguided [U]", "±5 mm, no spring, core on ⌀3 rod; rig B", "PICK (B)"),
    ("LVDT free", "Micro-Epsilon DTA-5G8 + MSC7401 [U]", "±5 mm, free core, 0–5 V, −20…+80 °C", "alternative"),
    ("LVDT free", "Solartron AX/5/F (free core) + OD5 [U]", "±5 mm, ±5 V via conditioner", "alternative"),
    ("laser", "Micro-Epsilon optoNCDT 1420", "non-contact, but op. 0…+50 °C, frost on window", "not suitable"),
    ("LVDT ±10", "TE DC-EC 500", "operating only 0…+70 °C", "not suitable"),
    ("p cell", "TML PDA-PA 200 kPa", "⌀6.5×1 mm, 0.8 mV/V, comp. −10…+60, op. −20…+70 °C", "PICK"),
    ("p cell", "Kyowa BEC-A 200/500 kPa", "⌀30 mm, for model tests; t, temp. [U]", "one cell only"),
    ("p cell", "TML KDE/KDF-PA", "⌀50 mm – too large for ⌀100 sample", "not suitable"),
    ("p wall", "TE/MEAS EPL", "miniature, comp. −40…+90 °C, ⌀ [U]", "alternative"),
    ("p cell", "Tekscan FlexiForce A201", "thin film, drift < 5 %/log t", "comparison only"),
    ("T probe", "Campbell 109SS", "⌀1.6 mm, ±0.38 °C at 0 °C, direct on CR1000", "PICK"),
    ("T probe", "Campbell 107", "⌀7.6 mm, ±0.2 °C (0–50 °C)", "air / frame"),
    ("T probe", "TE/YSI 44031 bead", "±0.1 °C, own half bridge needed", "for 0.01 °C (E6 chain)"),
    ("Pt100", "Pt100 1/10 DIN 4-wire ⌀3 + 4WPB100", "±0.03 °C at 0 °C, via MUX-1", "PICK (point M)"),
    ("TDR", "mini 3-rod 40 mm (custom) + TDR200", "fits ⌀100 sample; calibrate in the sand", "PICK [U]"),
    ("TDR", "Campbell CS645 (3 rods 75 mm)", "too long for r 50 – would cross the axis", "not suitable"),
    ("TDR", "Easy Test LP/ms micro probe + own meter [U]", "rods ≈ 53 mm; separate logger", "alternative"),
    ("optical", "FBG in capillary ⌀1 + HBM FS22 / Luna si155 [U]", "≈ ±0.2–0.5 °C, many points on one fibre", "PICK [U]"),
    ("optical", "fluorescent probe Opsens OTG-F + TempSens [U]", "±0.3 °C, analog out → CR1000 SE", "alternative"),
]

# CR1000 terminal → use
CHANNELS = [
    ("SE1–SE2", "LVDT-A1, A2 (rig A)", "VoltSE ±5000 mV, averaging; own ±15 V supply"),
    ("SE3–SE5", "LVDT S1–S3 (rig B surface)", "VoltSE ±5000 mV"),
    ("SE6–SE8", "LVDT E1–E3 (rig B anchors)", "VoltSE ±5000 mV"),
    ("DIFF5, DIFF6", "MUX-1 AM16/32B, 4×16",
     "9 p-bridges + 2 Pt100 (4WPB100); COM H2/L2 → DIFF5"),
    ("VX3", "MUX-1 excitation", "2000 mV bridges / 2500 mV Pt100"),
    ("C1–C3", "TDR200 (SDM) → SDMX50SP", "2 TDR probes (point M, A and B)"),
    ("C4, C5", "MUX-1 reset, clock", ""),
    ("SE13", "MUX-2 AM16/32B, 2×32", "≈ 20 thermistors (Therm109), VX2"),
    ("C6, C7", "MUX-2 reset, clock", ""),
    ("12V, G", "both multiplexers, TDR200", ""),
    ("–", "FBG interrogator", "1 fibre for both rigs; own PC, clock synced"),
    ("SE14–16", "spare", ""),
]

# --- varianta A-min: konkrétní typy a orientační ceny (EUR bez DPH) ---------------------
# zdroj: "web" = cena nalezená u prodejce (viz README), "odhad" = cena se nezveřejňuje → poptat
# (tag, co měří, typ, ks, cena/ks min, cena/ks max, zdroj, CR1000)
A_MIN_SENSORS = [
    ("PV1, PB1", "svislé napětí v písku / u dna", "TML PDA-PA 500 kPa (⌀6.5 × 1 mm) [U]", 2, 600, 1000, "odhad", "DIFF1, DIFF2 BrFull, VX1"),
    ("LVDT", "kontrola, že se víko nehýbe", "RDP DCTH400AG (±10 mm, spring)", 1, 581, 581, "web", "SE9 VoltSE ±5 V"),
    ("", "zdroj pro LVDT", "DIN-rail power supply for the LVDT", 1, 40, 80, "odhad", "–"),
    ("T1, T2, Tair", "teplota 20/80 mm, vzduch (volitelně)", "Campbell 109SS-L (⌀1.6 mm)", 3, 180, 260, "odhad", "SE11–13 Therm109, VX3"),
]
# čidla, která laboratoř už má (bod M) – bez ceny
A_MIN_OWN = [
    ("TDR", "vlhkost / nezamrzlá voda v bodě M", "Campbell CS645, 3 rods ⌀3.2 × 75, pitch 8.9", "TDR100/200, SDM"),
    ("Pt100", "teplota v bodě M", "Pt100, 37 mm (25 mm metal), vertical", "4-wire"),
    ("OF", "teplota optickým vláknem v bodě M", "optical fibre, tip 37.5 from the wall", "own interrogator"),
]
# mechanika (EUR bez DPH, odhad: materiál + zakázková výroba)
A_MIN_MECH = [
    ("tištěná cela ⌀160 × 160 podle výkresu Column_one_body (slicer ≈ 600 g PETG, 21 h, ≈ 18 €) + epoxid", 25, 50),
    ("kluzný PTFE sprej + silikonový tuk na vnitřní stěnu", 15, 30),
        
    ("Al deska 230 × 230 × 20, Al píst ⌀99,5 × 40 (obrobení)", 150, 300),
    ("ocelové víko ⌀230 × 15 (pálení, 4 otvory, závit M16 × 1,5)", 60, 120),
    ("3 táhla M10 nerez A4 + matice a podložky, šroub M16 × 1,5 + pojistná matice", 25, 50),
    ("nerezový sloupek ⌀12 + objímka LVDT", 15, 40),
]

# --- A-rám: mechanika (čidla stejná jako A-min) ---------------------------------------
A_FRAME_MECH = [
    ("tištěná cela ⌀160 × 160 podle výkresu Column_one_body (slicer ≈ 600 g PETG, 21 h, ≈ 18 €) + epoxid", 25, 50),
    ("kluzný PTFE sprej + silikonový tuk na vnitřní stěnu", 15, 30),
        
    ("Al profily: 2× 40×80 × 245 + 80×80 × 260 (řezané), krytky", 50, 100),
    ("4 šrouby do čela M12 + 4 šrouby M10 do desky, vrtání", 20, 50),
    ("Al deska 260 × 200 × 25, Al píst ⌀99,5 × 40, Al sloupek ⌀40 × 51 (obrobení)", 180, 350),
    ("vložka POM-C ⌀40 × 8", 5, 15),
    ("šroub M16 × 1,5 + pojistná matice, závitové pouzdro v příčníku", 20, 40),
    ("nerezový sloupek ⌀12 + objímka LVDT, terčík na sloupku", 20, 45),
]

# --- B-open: co koupit (EUR bez DPH, orientačně) ----------------------------------------
B_OPEN_BUY = [
    ("LVDT", "zdvih / sednutí povrchu", "RDP DCTH200, free core (±5 mm) [U]", 1, 550, 750, "odhad (DCTH400AG 581 € web)", "SE1"),
    ("", "zdroj pro LVDT", "DIN-rail power supply", 1, 40, 80, "odhad", "–"),
    ("Tair", "teplota vzduchu (volitelně)", "Campbell 109-L", 1, 150, 220, "odhad", "SE2, VX1"),
]
B_OPEN_MECH = [
    ("tištěná cela ⌀160 (už máte)", 0, 0),
    ("Al deska 220 × 220 × 10", 30, 60),
    ("Invarová tyč ⌀12 × 300 + objímka + Al rameno", 50, 110),
    ("terčík PETG ⌀30 × 2 + Invarová tyčka jádra ⌀3", 10, 30),
]

# --- B-open s kamerou: co koupit (EUR bez DPH, orientačně) ---------------------------------
B_CAM_BUY = [
    ("CAM", "Raspberry Pi 5 (4 GB) + zdroj + karta", 1, 90, 120),
    ("", "Raspberry Pi HQ Camera (IMX477, 12 MP)", 1, 55, 70),
    ("", "objektiv 12 mm C-mount, nízké zkreslení", 1, 40, 80),
    ("LAS", "čárový laser 650 nm, třída 2 (≤ 1 mW), úhel 60°", 1, 15, 60),
    ("", "vyhřívaný box: XPS 30, topná fólie 5 W, termostat, okénko 2× sklo", 1, 40, 80),
    ("Tair", "Campbell 109-L (volitelně)", 1, 150, 220),
]
B_CAM_MECH = [
    ("Al deska 320 × 220 × 10", 40, 70),
    ("rameno nad celou: profil 20×20 (sloupek + výložník)", 25, 60),
    ("2 referenční plíšky na límec (matně bílé) – kontrola", 2, 10),
]

# --- varianta C: měření deformace 1 (kamera + laser) a 2 (LVDT) – co koupit (EUR bez DPH) --------
C_BUY = [   # rev. B – konkrétní typy (ceny 10/2026, EUR bez DPH; Kč s DPH přepočteno / 1,21 / 25) – viz purchase_list.md
    ("CAM", "Raspberry Pi 5 4 GB + PSU, SD, camera cable (RPishop)", 1, 105, 120, "web (RPishop 2769 Kč)", "– (Ethernet, NTP)"),
    ("", "Raspberry Pi HQ Camera C/CS, IMX477 (RPishop OFI060)", 1, 50, 62, "web (RPishop 1499 Kč)", "C5 trigger"),
    ("", "Raspberry Pi 6 mm CS wide-angle lens (RPishop / Pi Hut)", 1, 20, 30, "odhad", "–"),
    ("", "camera box XPS 30, double glass; houses the RPi 5 (no heater)", 1, 20, 40, "odhad", "–"),
    ("", "SHT45 RH/T sensor on the RPi (I2C), freezer air", 1, 15, 25, "odhad", "– (RPi)"),
    ("LAS", "Picotronic DOE253-635-1-6(10x22), 11 lines, 635 nm, 1 mW, 5 V", 1, 92, 92, "web (Picotronic 70111842)", "– (RPi GPIO)"),
    ("LVDT", "RDP DCTH400AG ±10 mm, spring (Elkome)", 1, 581, 581, "web (Elkome)", "SE1, ±5000 mV"),
    ("", "Mean Well HDR-15-24, 24 V DIN (floating supply) (TME)", 1, 11, 14, "web (TME)", "C4 relay"),
    ("", "Campbell 4WPB100 (for the existing Pt100) (Ekotechnika)", 1, 60, 120, "odhad – na dotaz", "DIFF1"),
    ("Tair", "Campbell 109-L, REQUIRED: air = boundary condition", 1, 150, 220, "odhad – na dotaz", "SE3, VX1"),
    ("", "fan 80 mm 12 V, air mixing in the freezer", 1, 10, 20, "odhad", "C4 relay"),
    ("CAL", "shims 0.1 / 0.5 / 1.0 mm (feeler gauge set) for camera px → mm", 1, 10, 25, "odhad", "–"),
]
C_MECH = [   # rev. B2 – only bought, laser-cut and printed parts (see objednavka.md)
    ("laser: Al 10 base + top plate, carrier, piston discs; steel discs", 100, 190),
    ("profiles 2× 40×80 slot 8 × 326, 8 angle brackets, T-nuts, 3 feet M8", 60, 110),
    ("igus RJ4JP-01-12, shaft collar 12, ball 5/16\", screws M3–M8", 25, 50),
    ("Invar 36: rod ⌀12 × 289 + post ⌀16 × 357 (Evek, cut to length)", 80, 160),
    ("cell printed in ONE piece ⌀240 × 200 (PETG(-CF) ≈ 1.5 kg) + 3 G10 pads ⌀20 × 40", 45, 90),
    ("printed parts: housing, arms, foot, laser holder, camera box (PETG-CF)", 10, 25),
]
