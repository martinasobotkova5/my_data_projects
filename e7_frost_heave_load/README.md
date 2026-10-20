# E7: zatěžovací zkoušky zeminy při mrznutí a tání

Vzorek ⌀100 × 100 mm (vnitřní) v tištěné cele z PETG-CF, v rámu z Al profilů, v truhlicovém mrazáku s programovatelným regulátorem.

| soubor | obsah |
|---|---|
| `vykresy/E7_drawings.pdf` | 6 listů A3, anglicky (PNG po listech ve stejné složce) |
| `src/sensors.py` | výběr čidel a plán kanálů CR1000 |
| `3d/*.step` | 3D sestavy pro Onshape: varianta A, varianta B, obě v mrazáku (+ STL a PNG náhledy) |
| `vypocty.md` | síly, tuhost rámu, teplotní artefakt, napětí v cele, siloměry |
| `src/params.py` | všechny rozměry a předpoklady |
| `src/vykresy.py`, `src/vypocty.py` | generátory |

Regenerace: `cd src && python vykresy.py && python vypocty.py > ../vypocty.md`

---

## 1. Dvě varianty

| | **A – konstantní zatížení** (E7-V01) | **B – konstantní rozměry** (E7-V02) |
|---|---|---|
| co se drží | svislé napětí 25 / 50 / 100 / 200 kPa | výška vzorku (píst opřený o rám) |
| co se měří | zdvih při mrznutí, sednutí při tání (LVDT) | síla / tlak z mrazového zdvihu (siloměr) |
| zatížení | páka 1 : 10 se závažím 2–16 kg | jemný šroub M24×1,5, dosedací předpětí 5 kPa |
| siloměr | S-snímač 2 kN v sérii (kontrola skutečné síly) | kompresní 20 kN nahoře **i dole** → tření o stěnu = rozdíl |
| návrhové maximum | 200 kPa = 1,6 kN | 2 MPa = 15,7 kN (silty dosahují 0,2–2 MPa) |
| cela | vícekroužková (doporučeno) nebo monolitická | monolitická + Al objímka 5 mm |

Obě varianty používají stejný rám a stejnou spodní a horní část: podstavec s porézním kamenem, izolační mezikus G10, píst s porézním kamenem, kuličku, LVDT na Invarovém rámečku a termistory ve stěně. Přepnutí mezi variantami znamená vyměnit horní zatěžovací část a spodní distanční kus za siloměr.

**Proč páka se závažím (A):** zatížení zůstává konstantní, i když vzorek zvedá nebo sedá a mění se teplota. V mrazáku nepotřebuje vzduch ani elektřinu. Alternativou je pneumatický válec s valivou membránou a přesným regulátorem mimo mrazák (suchý vzduch, regulace podle siloměru). Ten je kompaktnější, ale závisí na tlakovém vzduchu a regulaci.

## 2. Vážní čidla, nebo siloměry?

**Siloměry**, tedy tahové a tlakové snímače síly zapojené do osy zatěžování. Ne plošinová ani jednobodová vážní čidla.

- **Vážní čidla** jsou stavěná pro plošinu s výstředným zatížením. V osové sestavě mezi pístem a rámem se ohýbají a jsou poddajná.
- **Kompresní siloměry** (kanystrový nebo sloupkový typ) jsou tuhé: při plném rozsahu se stlačí ≈ 0,02–0,1 mm. To je pro variantu B zásadní, protože každá poddajnost snižuje naměřený tlak. Literatura ukazuje, že tlak z mrazového zdvihu silně závisí na tuhosti omezení (Ji et al. 2019; viz část 5).
- **S-snímač 2 kN** ve variantě A dává jemné rozlišení při malých silách (1 kPa ≈ 7,9 N). Kloubové hlavice na obou koncích k němu nepustí ohybový moment.
- **Teplota:** běžné siloměry třídy C3 (OIML R60) jsou kompenzované v rozsahu −10 … +40 °C, takže −10 °C je na hraně. Vybrat typ s kompenzací do −20 °C nebo −30 °C (nerez, IP67), logovat teplotu siloměru a nulovat při +10 °C. Teplotní drift nuly ≈ 0,5 kPa na 20 K (`vypocty.md` §6).
- **Ruční digitální siloměr** se pro dlouhodobé logované zkoušky nehodí.
- **Odečet:** plný most 6vodičově, ratiometricky na CR3000 nebo 24bitovém můstkovém zesilovači.

## 3. Rám z Al profilů (E7-V04)

- **Sestava:** 2 sloupy 40×80, příčník 80×80, základová deska Al 300×250×25. Výška je 525 mm včetně desky. Páka varianty A přidá ≈ 120 mm nad příčník, takže je potřeba ověřit vnitřní výšku mrazáku (≈ 650 mm, změřit).
- **Tuhost při 15,7 kN:** příčník 0,046 mm, sloupy 0,045 mm, siloměr ≈ 0,05 mm, spoje 0,02–0,15 mm. **Rozhodují spoje.** Proto šrouby do čela profilů a žádné úhelníky v silové cestě, případně 2 ocelové táhla M12. Celková tuhost vychází 54–98 kN/mm.
- **Teplotní artefakt (hlavní riziko varianty B):** Al sloupy 420 mm se při změně o 20 K zkrátí o 0,19 mm. Kdyby byla vnitřní sestava z oceli, samotná teplota by do zmrzlého vzorku zatlačila ≈ 1,7 kN, tedy ≈ 220 kPa, což je řádově stejně jako měřený tlak. Opatření:
  1. distanční trubka z Al, aby se silová cesta smršťovala stejně jako sloupy (zbytek ≈ 0,1 kN);
  2. **slepá zkouška** s Al náhradou vzorku ve stejném programu, jejíž výsledek se odečte;
  3. LVDT vztažená k Invarovému rámečku ze základové desky.

## 4. Vydrží PETG-CF? (E7-V03, `vypocty.md` §4)

**Varianta A ano. Varianta B jen s Al objímkou.** Pevnost PETG-CF z katalogových listů a literatury: ≈ 40–55 MPa ve směru vlákna nebo vrstvy, jen 15–30 MPa kolmo na vrstvy. Pro neplněné PETG ukazuje Ultimaker TDS 19 ± 6 MPa v ose Z. Dlouhodobě počítám s ≈ 30 % pevnosti kvůli creepu a soudržnosti vrstev.

| zatěžovací stav | napětí | bezpečnost krátkodobě | dlouhodobě |
|---|---|---|---|
| obvod, A 200 kPa | 1,3 MPa | > 30 | > 9 |
| obvod, B 1 MPa | 6,3 MPa | 6–9 | 1,9–2,6 |
| obvod, B 2 MPa | 12,6 MPa | 3–4 | **1,0–1,3 – nestačí** |
| obvod, B 2 MPa + Al objímka 5 mm | ≈ 1 MPa v PETG | > 40 | > 12 |
| osově přes vrstvy, tření bez fólie, 1 MPa | 5,8 MPa | 2,6–5 | **< 1,6** |
| osově, PTFE fólie, 1 MPa | 0,6 MPa | > 25 | > 7 |

Podmínky:
- **Tisk:** tisknout nastojato (obvodové napětí jde podél vlákna). Stěna ≥ 8 mm, pouze soustředné perimetry, 100 % výplň.
- **Tření o stěnu:** PTFE fólie se silikonovým tukem. Cela je na podstavci jen položená, ne upnutá, aby ji tření tlačilo, a netrhalo vrstvy.
- **Voda v pórech tisku:** vnitřek utěsnit tenkým epoxidem. Porézní FDM PETG nasákne ≈ 5 % i při 100 % výplni a voda zmrzlá v mezerách mezi vrstvami je trhá. Samotné cykly mrznutí a tání suchých vzorků podle literatury vlastnosti téměř nemění (UMaine 2024; Stan et al. 2019: po cyklech do −40 °C bez významné změny).
- **Vruby:** žádné tištěné závity ani ostré rohy, protože uhlíková vlákna snižují houževnatost v mrazu. Místo nich zalisované závitové vložky a zaoblení.
- **Teplotní roztažnost:** α PETG-CF ≈ 30–60·10⁻⁶ 1/K, takže vůle Al pístu musí být ≥ 0,3 mm.
- **Kvalifikace před použitím:**
  1. tlaková zkouška tištěného kroužku do porušení (≥ 3× návrhový tlak);
  2. 10 cyklů −10/+10 °C nasycených vzorků a pak tahová zkouška XY a Z proti suchým kontrolním vzorkům;
  3. creep kroužku pod 1 MPa po 7 dní s tenzometrem po obvodu.

## 5. Literatura (ověřeno vyhledáním; DOI jen kde potvrzeno)

- **Konrad & Morgenstern (1980)**, *Can. Geotech. J.* 17: 473–486. Konrad (1987), *Geotech. Testing J.* 10(2): 51–58. Segregační potenciál klesá s přitížením, proto ve variantě A zkoušet více úrovní zatížení.
- **ASTM D5918**: mrazová a rozmrazovací náchylnost zemin. Vícekroužková cela, malé přitížení, dva cykly mrznutí a tání, LVDT.
- **Nixon & Nixon (2015)**, GeoQuébec: tření o stěnu působí jako přitížení až ≈ 35 kPa. Pomáhá namazaná latexová membrána a mrznutí odspodu.
- **Srovnání cel (TRB/CRREL)**: vícekroužkové cely jsou výrazně lepší než kuželové nebo dělené. Proto pohled F na E7-V03.
- **Jin, Lee, Ryu & Akagawa (2019)**, *Cold Reg. Sci. Technol.* 157: 119–132, doi:10.1016/j.coldregions.2018.09.011. Cela s vlastní regulací teploty místo klimakomory.
- **Hoekstra, Chamberlain & Frate (1965)**, CRREL RR 176: siloměr nad vzorkem měří tlak a zároveň brání zdvihu.
- **Ji et al. (2019)**, *Bull. Eng. Geol. Environ.*, doi:10.1007/s10064-018-1345-z, a CRST 2017: tlak z mrazového zdvihu silně závisí na tuhosti omezení (65 → 92 kPa při rostoucí tuhosti). Tuhost je proto nutné měřit a uvádět.
- **Přehled Penner a další**: maximální tlaky 0,2–3 MPa. Za studené desky až desítky MPa (teoreticky ≈ 1,1 MPa na 1 °C podchlazení).
- **PETG v mrazu a vlhku**:
  - Ultimaker PETG TDS (anizotropie XY/Z);
  - Stan et al. (2019), *Rom. J. Tech. Sci.* 64: 21–41;
  - Economides et al. (2024), *Polymers* 16: 3336, doi:10.3390/polym16233336;
  - UMaine MS thesis (2024): cykly mrznutí a tání minimální vliv, voda škodí.

## 6. Výkresy (aktualizováno)

| list | obsah |
|---|---|
| E7-V01 | varianta A – zjednodušené schéma se značkami čidel a doporučenými modely |
| E7-V02 | varianta B – zjednodušené schéma se značkami čidel a doporučenými modely |
| E7-V03 | cela PETG-CF (monolitická + vícekroužková) |
| E7-V04 | rám z Al profilů – zmenšený: deska 260 × 200, sloupy 330 mm, příčník 260 mm |
| E7-V05 | výběr čidel (varianty od více výrobců) a plán kanálů CR1000 |
| E7-V06 | obě sestavy vedle sebe na vaně ve stejném mrazáku jako E6, CR1000 venku |

Rám jsem zmenšil, aby se obě sestavy vešly vedle sebe na vanu (≈ 530 × 340 mm). Páka varianty A je kratší (300 mm, převod stále 1 : 10) a míří k volnému konci mrazáku. Nejvyšší bod je ≈ 555 mm proti odhadovaným ≈ 650 mm vnitřní výšky. Kratší sloupy zároveň snižují teplotní artefakt ve variantě B na ≈ 160 kPa; slepá zkouška zůstává nutná.

## 7. Konkrétní čidla pro CR1000 (E7-V05, `src/sensors.py`)

Údaje jsou z katalogových stránek výrobců a distributorů nalezených vyhledáváním. Stránky jsem nemohl otevřít přímo, takže teplotní rozsahy a deformace před objednáním ověřit u dodavatele. [U] = nepotvrzeno.

| měření | doporučeno | proč | alternativy |
|---|---|---|---|
| síla, varianta A (2 kN) | **Interface SSM 2 kN** | S-typ, kompenzace −15 … +65 °C (nejnižší nalezená), provoz −55 … +90 °C, IP67 | HBM S9M/2kN (třída 0,02, IP68, −10 … +70 °C); HBM U2B; ME KD80s; Lorenz K-25 (rozšířený rozsah na dotaz) |
| síla, varianta B (2× 20 kN) | **HBM C9C/20kN** | ⌀26 × 13 mm → velmi tuhý, 1 mV/V, jmenovitě −10 … +70 °C, provoz −30 … +85 °C, IP67 | Burster 8402 (≤ 50 µm, IP54); HBM C10 25 kN; Futek LTH500 |
| posun (4×) | **RDP DCTH400** | DC-LVDT ±10 mm s vestavěnou elektronikou, výstup ±5 V přímo do CR1000, −40 … +80 °C | Micro-Epsilon DTA-10D + MSC7401; Solartron AX/10/S + OD5; HBM WA-L |
| teplota (21×) | **Campbell 109SS** | trubička ⌀1,6 mm (pasuje do průchodek 1/16″), přímo na CR1000, ±0,38 °C při 0 °C | Campbell 107 (vzduch, rám); TE/YSI 44031 pro 0,01 °C (řetězec jako v E6) |

**Nevhodné kvůli mrazu:**
- TE DC-EC / HCD: jen 0 … +70 °C.
- Interface LBM: kompenzace jen +21 … +77 °C.
- AML DBBSM: kompenzace 0 … +70 °C, IP51.
- Burster 8438: 0 … +85 °C.
- HBM S2M: jen do 1 kN.

**Zapojení na jeden CR1000 (obě sestavy):** CR1000 má 16 SE / 8 DIFF vstupů a 3 budicí výstupy ±2,5 V.

| svorky CR1000 | připojeno | poznámka |
|---|---|---|
| DIFF1–3 + VX1 | 3 siloměry | BrFull, ratiometricky s reverzací |
| DIFF4–7 | 4 LVDT | ±5000 mV; vlastní zdroj ±15 V |
| SE15 + VX2 + C1/C2 | multiplexer AM16/32B | režim 2×32 pro 21 termistorů |

- Moduly 4WFBS nejsou potřeba, slouží jen pro čtvrtmůstky.
- Rozlišení síly s CR1000: ≈ 0,04 kPa (A) a ≈ 0,3 kPa (B).
- Rozlišení posunu: ≈ 1,3 µm (0,7 µm s reverzací). Absolutní linearita LVDT ±0,25 % FS ≈ ±50 µm → kalibrovat mikrometrem.
- CR1000 se už nevyrábí (nástupce CR1000X / CR1000Xe s 24bitovým převodníkem). Stávající stačí. Musí ale zůstat mimo mrazák, protože pracuje v rozsahu −25 … +50 °C.
- Žádný siloměr jsem nenašel se standardní kompenzací do −20/−30 °C. Logovat teplotu siloměrů (TLC) a korigovat, případně poptat rozšířený rozsah (Interface, Lorenz).

## 8. 3D modely pro Onshape (`3d/`)

| soubor | obsah |
|---|---|
| `E7_variant_A.step` | varianta A – rám, cela, vzorek, páka se závažím, siloměr Interface SSM, 2× LVDT DCTH400, Invarová reference, termistory 109SS |
| `E7_variant_B.step` | varianta B – rám, cela s Al objímkou, 2× HBM C9C, Al distanční trubka, šroub M24 s ručním kolem, LVDT, termistory |
| `E7_freezer_layout.step` | obě sestavy na vaně v mrazáku (stěny mrazáku průhledné, ≈ rozměry) |

**Import do Onshape:**
1. Na stránce dokumentů *Create → Import*, nebo v otevřeném dokumentu tlačítko *Import*.
2. Vybrat soubor `.step`.
3. Sestava se načte po jednotlivých dílech s názvy (např. „LC-T HBM C9C 20 kN“, „cell PETG-CF“) a barvami.
4. Jednotky jsou mm, osa z míří nahoru, z = 0 je horní líc základové desky.

**Zjednodušení modelu:**
- Drážky profilů, závity, kabely a spojovací materiál nejsou modelované.
- Čidla mají obalové rozměry podle katalogů. Interface SSM je kvádr ≈ 51 × 19 × 64 mm [U], přesný tvar doplnit z modelu výrobce. Interface, HBM i RDP nabízejí ke stažení CAD modely svých čidel, ty lze v Onshape vložit místo zjednodušených těles.

Generuje `src/model3d.py` z `src/params.py`, náhledy `src/render3d.py`.

## 9. Doporučení a otevřené otázky

1. **Program regulátoru:** „Set A“ (24 h +10 °C, pak lineární rampy 192 h mezi −10 a +10 °C) lze použít přímo. Teplota se ale mění pomalu a stále, takže čelo promrzání postupuje pomalu. Pro jasné kroky zvážit výdrže na −10 °C a +10 °C.
2. **Směr promrzání:** v mrazáku promrzá vzorek ze všech stran. Izolace stěn a mezikus G10 pod podstavcem vedou k promrzání hlavně shora přes Al píst. Literatura doporučuje termostatované koncové desky a mrazák jen jako ochranné prostředí (Jin et al. 2019). Je to možné rozšíření.
3. **Otevřený, nebo uzavřený systém?** Bez přítoku vody je zdvih ≈ 2,7 mm (9 % × θ 0,30 × 100 mm). S přítokem vody zespodu (Mariottova láhev nad 0 °C, vyhřívaný podstavec) rostou ledové čočky a zdvih je výrazně větší. Který případ chcete?
4. **Zemina:** typ a vlhkost určí očekávaný tlak a volbu siloměru (20 kN je dimenzováno na 2 MPa).
5. **Výška mrazáku** s pákou varianty A (≈ 645 mm celkem): prosím změřit.
6. **Vícekroužková cela pro A:** souhlasíte? Tisk 9 kroužků po 10 mm je jednoduchý a výrazně omezí tření.

> Výkresy jsou NÁVRH. Profilové hodnoty a údaje o siloměrech jsou katalogové odhady. Ověřit u konkrétního dodavatele a nechat zkontrolovat konstruktérem.
