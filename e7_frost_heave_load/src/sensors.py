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
    ("PV1, PB1", "svislé napětí v písku / u dna", "TML PDA-PA 200 kPa (⌀6.5 × 1 mm)", 2, 600, 1000, "odhad", "DIFF1, DIFF2 BrFull, VX1"),
    ("Pt100", "referenční teplota v bodě M", "Omega PM, Pt100 1/10 DIN, 4-wire, ⌀3.2 × 150 mm", 1, 230, 260, "web", "DIFF3+4 BrHalf4W, VX2"),
    ("", "doplňkový modul k Pt100", "Campbell 4WPB100", 1, 60, 120, "odhad", "–"),
    ("TDR", "vlhkost / nezamrzlá voda v bodě M", "Campbell TDR200 (reflectometer)", 1, 4500, 5200, "web", "C1–C3 (SDM), 12V"),
    ("", "sonda TDR", "TDR probe, custom 3 rods ⌀1.6 × 40 + RG58 1 m", 1, 50, 150, "odhad", "–"),
    ("OPT", "optická teplota v bodě M", "Opsens OTG-F (fluorescent, ⌀0.15 mm)", 1, 300, 600, "odhad", "–"),
    ("", "převodník k OPT", "Opsens TempSens 4-ch., ±5 V output", 1, 3500, 6000, "odhad", "SE10 VoltSE"),
    ("LVDT", "kontrola, že se vzorek nehýbe", "RDP DCTH400AG (±10 mm, spring)", 1, 581, 581, "web", "SE9 VoltSE ±5 V"),
    ("", "zdroj pro LVDT", "DIN-rail power supply for the LVDT", 1, 40, 80, "odhad", "–"),
    ("T1, T2, Tair", "teplota písku 20/80 mm, vzduch", "Campbell 109SS-L (⌀1.6 mm)", 3, 180, 260, "odhad", "SE11–13 Therm109, VX3"),
]
# mechanika (EUR bez DPH, odhad: materiál + zakázková výroba)
A_MIN_MECH = [
    ("cela PETG-CF (≈ 0,4 kg filamentu) + epoxid", 30, 60),
    ("PTFE fólie 0,5 mm + silikonový tuk", 25, 50),
    ("Kaiflex 25 mm samolepicí, ≈ 0,3 m²", 10, 20),
    ("G10 kotouč ⌀150 × 10", 25, 50),
    ("Al deska 200 × 200 × 10, Al dno ⌀150 × 15, Al píst ⌀99,5 × 40 (obrobení)", 120, 250),
    ("ocelové kotouče ⌀150: 3 × 36 + 1 × 18 + 1 čtvrtkotouč 9 mm (≈ 20 kg, pálení + vrtání)", 150, 300),
    ("závitová tyč M16, nerezový sloupek ⌀12, objímka LVDT", 20, 50),
]
