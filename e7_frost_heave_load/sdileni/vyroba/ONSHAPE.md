# E7 rev. B3 – výrobní výkresy v Onshape

V této složce jsou dvě sady podkladů. Obě jde nahrát do Onshape:

| co | soubory | k čemu |
|---|---|---|
| 3D díly (STEP) | `laser/*.step`, `tisk/*.step`, celá sestava `../3d/E7_V01_variant_C.step`, cela `../3d/E7_V03_cell.step` | nativní díly v Onshape → z nich nativní výkresy |
| 2D výkresy (DXF s kótami) | `vykresy/*.dxf` (19 listů A4), náhled `vykresy/E7_vyrobni_vykresy.pdf` | hotové výrobní výkresy, v Onshape jako výkres |
| DXF pro řezání | `laser/*.dxf` (jen obrys a otvory 1 : 1) | posílá se přímo do laserového řezání |

## A) Nativní výkres z 3D dílu (doporučeno)
1. Onshape → **Create → Document** „E7 rig C rev. B3“.
2. **Import** (šipka nahoru vlevo dole) → vybrat STEP díly z `laser/` a `tisk/` (najednou). Onshape z nich vytvoří Part Studia.
3. U každého dílu: pravým tlačítkem na kartu Part Studia → **Create drawing** → šablona **ISO, A4 landscape, mm** → Onshape vloží pohledy.
4. Kóty: **Dimension** (lineární / průměr), u desek **Ordinate dimension** od rohu (stejný výchozí bod ◎ jako v tabulkách otvorů v PDF).
5. Do rohového razítka vepsat materiál, tloušťku a počet kusů podle PDF (`vykresy/E7_vyrobni_vykresy.pdf`).

## B) Hotové 2D výkresy (rychle)
1. **Import** souborů `vykresy/*.dxf`. Onshape z DXF vytvoří kartu výkresu (vrstvy OUTLINE, HIDDEN, DIM, TEXT, FRAME).
2. Jednotky při importu: **mm**. Kóty zůstanou editovatelné.

## Seznam listů
T01 sloup 40×80 · T02 podélník základny 40×40 · T03 příčka základny 40×80 · T04 horní příčník 40×80 s otvorem ⌀14 ·
L03 nosná deska · L04/L05 kotouče pístu · L06/L07 závaží (L01/L02 v rev. B3 odpadly – rám je celý z T-profilů) ·
B01 Invarová tyč · B02 Invarový sloupek · B03 podložka G10 ·
P01 pouzdro ložiska · P02 rameno LVDT · P03 rameno terčíku · P04 patka sloupku · P05 držák laseru ·
P06/P07 box kamery + víko · P08 závěs kamery · cela: `../cad/E7_V04_cell.dxf` + V03.

Generuje: `src/buildparts.py` (díly), `src/vyrobni_vykresy.py` (výkresy) – po změně rozměrů v `src/params.py` stačí obojí spustit znovu.
