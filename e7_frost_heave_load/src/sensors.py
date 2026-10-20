"""Sensor selection and CR1000 channel plan for E7 (both rigs in one freezer).

PICK = recommended model per tag (shown on the drawings).
OPTIONS = alternatives from other makers (sheet E7-V05).
Specs from manufacturer / distributor pages found by web search (README §7);
[U] = not confirmed, ask the supplier.
"""

# tag: (what it measures, recommended model, short spec, CR1000 connection)
PICK = {
    "LC-A": ("load, rig A (lever)", "Interface SSM 2 kN",
             "S-type, comp. −15…+65 °C, IP67", "DIFF1, BrFull, VX1"),
    "LC-T": ("heave force, rig B top", "HBM C9C/20kN",
             "⌀26×13 mm, 1 mV/V, nom. −10…+70 °C, IP67", "DIFF2, BrFull, VX1"),
    "LC-B": ("force at base, rig B", "HBM C9C/20kN",
             "same as LC-T", "DIFF3, BrFull, VX1"),
    "LVDT": ("heave / settlement (2 per rig)", "RDP DCTH400",
             "DC-LVDT ±10 mm, ±5 V out, −40…+80 °C", "DIFF4–7, VoltDiff ±5 V"),
    "T": ("soil, cell wall, piston, pedestal", "Campbell 109SS",
          "⌀1.6 mm sheath, ±0.38 °C at 0 °C", "AM16/32B → SE15, VX2"),
    "TX": ("load cell, frame, air", "Campbell 109SS / 107",
           "107: ⌀7.6 mm, ±0.2 °C (0–50 °C)", "AM16/32B → SE15, VX2"),
}

# (category, maker + model, key specs, verdict)
OPTIONS = [
    ("LC 2 kN", "Interface SSM 2 kN", "comp. −15…+65 °C, op. −55…+90 °C, IP67", "PICK"),
    ("LC 2 kN", "HBM S9M/2kN", "class 0.02, 2 mV/V, 6-wire, IP68, nom. −10…+70 °C", "alternative"),
    ("LC 2 kN", "HBM U2B 2 kN", "class 0.1, 2 mV/V, IP67, temp. [U]", "alternative"),
    ("LC 2 kN", "ME KD80s 2 kN", "2 mV/V, 0.2 mm at FS, −10…+70 °C", "alternative"),
    ("LC 2 kN", "Lorenz K-25", "1–2 mV/V, IP67, ext. range on request", "ask quote"),
    ("LC 2 kN", "AML DBBSM", "comp. only 0…+70 °C, IP51", "not suitable"),
    ("LC 20 kN", "HBM C9C/20kN", "⌀26×13 mm, 1 mV/V, nom. −10…+70, op. −30…+85 °C", "PICK"),
    ("LC 20 kN", "Burster 8402 20 kN", "1.5 mV/V, ≤ 50 µm deflection, op. −30…+100 °C, IP54", "alternative"),
    ("LC 20 kN", "HBM C10 25 kN", "class 0.02–0.05, height 36 mm [U]", "alternative"),
    ("LC 20 kN", "Futek LTH500 (≈22 kN)", "donut, 0.05 mm, op. −50…+93 °C", "alternative"),
    ("LC 20 kN", "Interface LBM", "comp. only +21…+77 °C", "not suitable"),
    ("LVDT ±10", "RDP DCTH400", "±5 V / 0–10 V out, −40…+80 °C, ±0.25 % FS", "PICK"),
    ("LVDT ±10", "Micro-Epsilon DTA-10D + MSC7401", "0–5 V / 4–20 mA, −20…+80 °C", "alternative"),
    ("LVDT ±10", "Solartron AX/10/S + OD5", "±5 V out, needs 230 V conditioner", "alternative"),
    ("LVDT ±10", "HBM WA-L 20 mm", "passive, needs carrier amplifier", "alternative"),
    ("LVDT ±10", "TE DC-EC 500", "operating only 0…+70 °C", "not suitable"),
    ("T probe", "Campbell 109SS", "⌀1.6 mm, ±0.38 °C at 0 °C, direct on CR1000", "PICK"),
    ("T probe", "Campbell 107", "⌀7.6 mm, ±0.2 °C (0–50 °C)", "air / frame"),
    ("T probe", "TE/YSI 44031 bead", "±0.1 °C, own half bridge needed", "for 0.01 °C (E6 chain)"),
    ("T probe", "Pt100 1/10 DIN + 4WPB100", "2 DIFF + VX per sensor", "too many channels"),
]

# CR1000 terminal → use
CHANNELS = [
    ("DIFF1", "LC-A (rig A)", "BrFull, ±7.5 mV, reversal"),
    ("DIFF2", "LC-T (rig B)", "BrFull, ±2.5 mV (1 mV/V), reversal"),
    ("DIFF3", "LC-B (rig B)", "BrFull, ±2.5 mV, reversal"),
    ("VX1", "excitation, 3 load cells", "2500 mV, ≈ 21 mA"),
    ("DIFF4, 5", "LVDT-A1, A2", "VoltDiff ±5000 mV, reversal, averaging"),
    ("DIFF6, 7", "LVDT-B1, B2", "VoltDiff ±5000 mV, reversal, averaging"),
    ("SE15 (DIFF8)", "AM16/32B COM", "2×32 mode, 21 thermistors (BrHalf / Therm109)"),
    ("VX2", "thermistor excitation", "via AM16/32B"),
    ("C1, C2", "AM16/32B reset, clock", ""),
    ("12V, G", "AM16/32B power", "LVDTs: own ±15 V supply, common to AG"),
    ("SE16, VX3", "spare", "e.g. panel check / 4WPB100"),
]
