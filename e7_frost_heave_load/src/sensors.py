"""Sensor selection and CR1000 channel plan for E7 (both rigs in one freezer).

PICK = the recommended model per tag (shown on the drawings).
OPTIONS = alternatives from other makers (sheet E7-V05).
Filled from manufacturer data sheets – see README for sources.
"""

# tag: (what it measures, recommended model, short spec, CR1000 connection)
PICK = {
    "LC-A": ("load, rig A (lever)", "TBD", "", ""),
    "LC-T": ("heave force, rig B top", "TBD", "", ""),
    "LC-B": ("force at base, rig B", "TBD", "", ""),
    "LVDT": ("heave / settlement (2 per rig)", "TBD", "", ""),
    "T": ("soil, cell wall, piston, pedestal", "TBD", "", ""),
    "TX": ("load cell, frame, air", "TBD", "", ""),
}

OPTIONS = []
CHANNELS = []
