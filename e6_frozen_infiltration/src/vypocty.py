"""Kontrolní a návrhové výpočty pro E6. Spuštění: python vypocty.py > ../vypocty.md"""
import math

import params as p


def area_cm2(d_mm):
    return math.pi * (d_mm / 20.0) ** 2


def row(name, value, unit, note=""):
    print(f"| {name} | {value} | {unit} | {note} |")


a_col, a_disk, a_res = area_cm2(p.D_COL), area_cm2(p.D_DISK), area_cm2(p.D_RES)
v_soil = a_col * p.H_SOIL / 10.0                       # cm3

print("# E6 – kontrolní výpočty\n")
print("Generováno skriptem `src/vypocty.py` z `src/params.py`.\n")

print("## 1. Kontrola čísel z původního schématu\n")
print("| veličina | hodnota | jednotka | poznámka |\n|---|---|---|---|")
row("plocha kolony ⌀100", f"{a_col:.2f}", "cm²")
row("plocha disku ⌀45", f"{a_disk:.2f}", "cm²")
row("podíl disku na průřezu", f"{100 * a_disk / a_col:.1f}", "%", "schéma: 20,2 % ✔")
row("poměr ploch kolona : disk", f"{a_col / a_disk:.2f}", "–", "schéma: 4,94 ✔")
row("šířka mezikruží", f"{(p.D_COL - p.D_DISK) / 2:.1f}", "mm", "schéma: 27,5 ✔")
row("objem zeminy ⌀100 × 100", f"{v_soil:.0f}", "cm³", "schéma: 785 ✔")
row("objem kolony ⌀85 × 140 (GACR-01)", f"{area_cm2(85) * 14:.0f}", "cm³", "schéma: „prakticky shodný“ ✔ (+1 %)")
row("1 mm hladiny v zásobníku ⌀31 → přes disk", f"{a_res / a_disk:.3f}", "mm", "schéma: 0,475 ✔")
row("1 mm hladiny → přes průřez kolony", f"{a_res / a_col:.4f}", "mm", "schéma: 0,0961 ✔")

print("\n## 2. Doba průniku – co přesně číslo 5–37 h znamená\n")
print("| veličina | hodnota | jednotka | poznámka |\n|---|---|---|---|")
for dth in (0.05, 0.15):
    for q in p.Q_DISK_MM_H:
        q_col = q * a_disk / a_col
        t = dth * p.H_SOIL / q_col
        row(f"Δθ = {dth}, q_disk = {q} mm/h", f"{t:.1f}", "h",
            f"q přes průřez = {q_col:.3f} mm/h; jen zaplnění Δθ (čelo zvlhčení)")
q_ml_h = [q / 10 * a_disk for q in p.Q_DISK_MM_H]      # mm/h × cm² → cm3/h
row("objemový přítok (= odtok v ustáleném stavu)",
    f"{q_ml_h[0]:.1f}–{q_ml_h[1]:.1f}", "ml/h")
pv_tot = p.THETA_TOT * v_soil
pv_por = p.POROSITY * v_soil
row("objem vody ve vzorku (kapalná + led), θ = 0,30", f"{pv_tot:.0f}", "ml", "„pórový objem“ pro stopovač")
row("objem pórů, n = 0,45", f"{pv_por:.0f}", "ml")
for n_pv in (1.0, 1.5, 2.0):
    v = n_pv * pv_tot
    t_lo, t_hi = v / q_ml_h[1], v / q_ml_h[0]
    row(f"{n_pv} PV odtoku", f"{t_lo:.0f}–{t_hi:.0f}", "h", f"{v:.0f} ml")
for fr in p.FRACTION_ML:
    row(f"počet frakcí po {fr:.0f} ml na 1,5 PV", f"{1.5 * pv_tot / fr:.0f}", "–", "schéma počítá ~60")
row("60 frakcí pokryje", f"{60 * p.FRACTION_ML[0]:.0f}–{60 * p.FRACTION_ML[1]:.0f}",
    "ml", f"= {60 * p.FRACTION_ML[0] / pv_tot:.2f}–{60 * p.FRACTION_ML[1] / pv_tot:.2f} PV")

print("\n## 3. Zásobník a měření přítoku\n")
print("| veličina | hodnota | jednotka | poznámka |\n|---|---|---|---|")
for h in (200, 300):
    row(f"objem zásobníku ⌀31, sloupec {h} mm", f"{a_res * h / 10:.0f}", "ml")
row("potřebná výška sloupce ⌀31 pro 1,5 PV", f"{1.5 * pv_tot / a_res * 10:.0f}", "mm", "→ nutné doplňování / větší Mariottova láhev")
row("pokles hladiny ⌀31 za hodinu", f"{q_ml_h[0] / a_res * 10:.1f}–{q_ml_h[1] / a_res * 10:.1f}", "mm/h")
row("1 Pa ≙", "0,10", "mm v. sl.", "0,1 mm ≙ 1 Pa = 0,01 % FS snímače 0–10 kPa")
row("typická přesnost 0–10 kPa (0,1 % FS)", "10", "Pa", "≙ 1 mm v. sl., ne 0,1 mm")
row("váha 0,01 g na Mariottově láhvi", "0,01", "ml", f"≙ {0.01 / a_disk * 10:.4f} mm přes disk")

print("\n## 4. Tepelná bilance: na kolik vody stačí „chlad“ zeminy při −3 °C\n")
print("| veličina | hodnota | jednotka | poznámka |\n|---|---|---|---|")
v_m3 = v_soil * 1e-6
cold = p.C_FROZEN * abs(p.T_INIT) * v_m3
m_refreeze = cold / p.L_F * 1000                      # g
row("citelný chlad vzorku −3 → 0 °C", f"{cold / 1000:.1f}", "kJ", "C = 1,9 MJ m⁻³ K⁻¹")
row("tolik vody může znovu zamrznout", f"{m_refreeze:.0f}", "ml", f"= {m_refreeze / pv_tot * 100:.0f} % PV, = {m_refreeze / a_disk * 10:.0f} mm přes disk")
row("doba přítoku tohoto objemu", f"{m_refreeze / q_ml_h[1]:.1f}–{m_refreeze / q_ml_h[0]:.1f}", "h", "pak je vzorek izotermní při 0 °C s ledem")
ice = (p.THETA_TOT - p.THETA_UNFROZEN) * v_soil
row("led ve vzorku při −3 °C", f"{ice:.0f}", "ml")
row("teplo na roztátí veškerého ledu", f"{ice * 0.917 * p.L_F / 1e6:.0f}", "kJ",
    "≫ citelný chlad → fáze „0 °C s ledem“ trvá dny, řídí ji okrajové toky tepla")
row("citelné teplo vody +0,5 °C na 1 ml", f"{4.19 * 0.5:.1f}", "J", f"vs. {p.L_F / 1000:.0f} J/ml latentní – zanedbatelné")

print("\n## 5. Spodní okrajová podmínka\n")
print("| veličina | hodnota | jednotka | poznámka |\n|---|---|---|---|")
for pore in (20, 50):
    h_ae = 2 * 0.0728 / 1000 / 9.81 / (pore / 2 * 1e-6) * 100
    row(f"vstup vzduchu membrány {pore} µm (Young–Laplace, θ = 0°)", f"≈ {h_ae:.0f}", "cm",
        "horní mez; skutečná bývá nižší → ověřit bublinkovým testem")
groove_len = p.N_GROOVE * (p.D_COL / 2 - 3) + sum(2 * math.pi * r for r in p.RING_R)
v_groove = groove_len * p.GROOVE ** 2 / 1000
row("objem drážek pod membránou", f"{v_groove:.2f}", "ml")
v_bore = math.pi * (p.BORE_D / 2) ** 2 * (p.CONE_RIM_T + p.CONE_H + p.NOZZLE_L) / 1000
row("osový vývrt kuželem ⌀1,5", f"{v_bore:.2f}", "ml")
v_tube = math.pi * 0.4 ** 2 * 600 / 1000
row("hadička PTFE ID 0,8 × 600 mm", f"{v_tube:.2f}", "ml")
row("mrtvý objem celkem", f"{v_groove + v_bore + v_tube + 0.3:.1f}", "ml", "+ ~0,3 ml podložka; < 1 frakce")
cone = math.pi / 3 * (p.D_COL / 20) ** 2 * 4.6
row("pro srovnání: vnitřní objem duté nálevky ⌀100 × 46 (původní)", f"{cone:.0f}", "cm³", "otevřený výtok = seepage face, h = 0")
a_in = area_cm2(p.D_SPLIT)
row("varianta B: vnitřní zóna ⌀50 / mezikruží", f"{a_in:.1f} / {a_col - a_in:.1f}", "cm²", "poměr ploch 1 : 3")

print("\n## 6. Izotopy – rozlišitelnost značky\n")
print("| veličina | hodnota | jednotka | poznámka |\n|---|---|---|---|")
row("frakcionace led–voda δ²H", "≈ +20", "‰", "α ≈ 1,0195–1,0212")
row("frakcionace led–voda δ¹⁸O", "≈ +3", "‰", "α ≈ 1,0029–1,0031")
for lab in (200, 500):
    row(f"značka δ²H = +{lab} ‰ vs. pozadí −70 ‰", f"{20 / (lab + 70) * 100:.0f}", "% signálu",
        "posun δ²H frakcionací vyjádřený v podílu značky")
row("přesnost OA-ICOS δ²H", "0,5", "‰", f"≙ {0.5 / 270 * 100:.2f}–{0.5 / 570 * 100:.2f} % podílu značky")
