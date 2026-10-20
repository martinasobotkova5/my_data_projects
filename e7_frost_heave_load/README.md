# E7: zatěžovací zkoušky zeminy při mrznutí a tání

Vzorek ⌀100 × 100 mm (vnitřní) v tištěné cele z PETG-CF, v rámu z Al profilů, v truhlicovém mrazáku z E6 s programovatelným regulátorem. Obě sestavy jsou **bez páky**: varianta A má přitížení předepnutou pružinou, varianta B pevné omezení šroubem.

| soubor | obsah |
|---|---|
| `vykresy/E7_drawings.pdf` | 6 listů A3, anglicky (PNG po listech ve stejné složce) |
| `3d/*.step` | 3D sestavy pro Onshape: varianta A, varianta B, vícekroužková cela, obě v mrazáku (+ STL a PNG náhledy) |
| `vypocty.md` | síly, pružiny, tuhost rámu, teplotní artefakt, napětí v cele, siloměry |
| `src/params.py` | všechny rozměry a předpoklady |
| `src/sensors.py` | výběr čidel a plán kanálů CR1000 |
| `src/vykresy.py`, `src/vypocty.py`, `src/model3d.py`, `src/render3d.py` | generátory |

Regenerace: `cd src && python vykresy.py && python vypocty.py > ../vypocty.md && python model3d.py && python render3d.py`

---

## 1. Dvě varianty

| | **A – nenasycený písek, konstantní přitížení** (E7-V01) | **B – konstantní výška** (E7-V02) |
|---|---|---|
| vzorek | nenasycený písek (Sr ≈ 0,3–0,5) | zemina podle zadání |
| co se drží | svislé napětí 25 / 50 / 100 / 200 kPa (výchozí 50 kPa) | výška vzorku (píst opřený o rám) |
| zatížení | **předepnutá pružina** ISO 10243 ⌀32 × 64 + šroub M20 × 1,5 | jemný šroub M24 × 1,5, dosedací předpětí 5 kPa |
| co se měří | tlaky uvnitř písku, u dna a na stěně; LVDT kontrolují, že se vzorek nehýbe | síla z mrazového zdvihu nahoře a dole (rozdíl = tření o stěnu) |
| siloměr | S-snímač 2 kN (kontrola síly pružiny) | 2× kompresní 20 kN |
| cela | vícekroužková + latexová membrána | monolitická + Al objímka 5 mm |
| sloupy rámu | 380 mm | 330 mm |

Obě varianty sdílejí spodní a horní část sestavy:
- podstavec s porézním kamenem a izolační mezikus G10,
- píst s porézním kamenem a kuličku v kuželových sedlech,
- LVDT na Invarovém rámečku a termistory ve stěně.

**Proč pružina:**
- Pružina je proti písku měkká, takže posun vzorku o 0,1 mm změní napětí jen o 0,25 kPa (pružina 20 N/mm). Smrštění Al rámu v mrazu (0,18 mm) ho změní o < 0,5 kPa.
- Sestava je kompaktní, bez závaží a nic nepřesahuje mimo rám.
- Siloměr LC-A loguje skutečnou sílu.

## 2. Přitížení pružinou (varianta A, `vypocty.md` §7)

**Postup:** šroubem dotáhnout, dokud LC-A neukáže cílovou sílu (50 kPa = 393 N), a zajistit pojistnou maticí. Dotahovat znovu jen tehdy, když síla ujede o více než 2 %.

| pružina | tuhost | přitížení | stlačení | změna napětí při posunu 0,1 mm | změna od smrštění rámu 0,18 mm |
|---|---|---|---|---|---|
| „light“ | 20 N/mm | 25–50 kPa | 9,8–19,6 mm | 0,25 kPa | 0,45 kPa |
| „heavy“ | 80 N/mm | 100–200 kPa | 9,8–19,6 mm | 1,0 kPa | 1,8 kPa |

Pro 200 kPa je stlačení těsně pod dovoleným (≈ 35 % volné délky). Konkrétní pružiny vybrat z katalogu podle tuhosti a dovoleného zdvihu, např. Lesjöfors, Danly, Meusburger nebo Fibro.

**Jiné způsoby přitížení bez páky:**

| způsob | výhody | nevýhody |
|---|---|---|
| **pružina + šroub (zvoleno)** | kompaktní, bez závaží, malý vliv teploty | sílu kontrolovat siloměrem |
| závaží přímo na pístu | síla přesně konstantní | 50 kPa = 40 kg na vzorku, velká tepelná hmota nad vzorkem |
| pneumatický válec (Bellofram) | přesné, nastavitelné | přívod suchého vzduchu do mrazáku, riziko námrazy |

## 3. Tlaky uvnitř vzorku (varianta A)

| značka | co měří | umístění | čidlo |
|---|---|---|---|
| PV1 | svislé napětí v písku | na ose, hloubka 40 mm | TML PDA-PA 200 kPa vlepený do nerezového disku ⌀20 × 2 mm |
| PH1 | radiální napětí v písku (volitelné) | r 25, hloubka 62 mm, disk na výšku | totéž |
| PB1 | svislé napětí u dna | v patce, lícem s porézním kamenem, r 25 | TML PDA-PA v pouzdře ⌀8, zapuštěný |
| PW1–PW3 | boční tlak na stěnu | v kroužcích, hloubky ≈ 20 / 42 / 64 mm | TML PDA-PA v pouzdře ⌀8, lícem s vnitřní stěnou |

O kolik tlak při mrznutí vzroste nad přitížení, tolik vytváří led v pórech.

**Proč TML PDA-PA:**
- Jako jediný miniaturní snímač má podle katalogu kompenzaci do −10 °C (provoz −20 … +70 °C). Je to destička ⌀6,5 × 1 mm, 0,8 mV/V, 350 Ω.
- Kyowa BEC-A (⌀30 mm) je alternativa jen pro jednu buňku. Tloušťku a teplotní rozsah se nepodařilo potvrdit.
- TML KDE/KDF (⌀50 mm) jsou na vzorek ⌀100 mm příliš velké.
- Údaje jsou z katalogových stránek podle vyhledávání. Datasheety jsem nemohl otevřít, před objednáním ověřit.

**Zásady z literatury** (Weiler & Kulhawy 1982; Labuz & Theroux 2005, doi:10.1520/GTJ12089; Talesnick 2005):
- **Málo malých inkluzí:** poměr průměr/tloušťka ≥ 10 a průměr / d50 ≥ 20 (disk ⌀20 v písku d50 0,3 mm → ≈ 65). Proto jen 2 vložené disky a ostatní snímače v lícu stěny a dna.
- **Kalibrace v písku:** ve stejném písku a cele, pod známým přitížením 25–200 kPa (nastaveným pružinou a kontrolovaným siloměrem), zatížení i odlehčení, při +10 a −10 °C.
- **Teplota:** u každého snímače termistor a korekce nuly podle teploty. Zeng et al. (2022, doi:10.6052/1000-0879-21-231) ukázali při cyklech mrznutí a tání teplotní posun a degradaci miniaturních buněk.
- **Led na membráně:** snímače utěsnit silikonem nebo epoxidem.
- **Sání v nenasyceném písku:** tenziometry v mrazu zamrznou. Před zmrazením změřit sání (tenziometr nebo filtrační papír) a pak ho odhadovat z teploty (Clapeyron) nebo z obsahu nezamrzlé vody (TDR).

## 4. Vícekroužková cela (varianta A, E7-V03)

- **Kroužky:** spodní kroužek s patkou ⌀150 × 8, nad ním 10 kroužků PETG-CF ⌀117/101 × 10 mm.
- **Podložky:** mezi kroužky PTFE podložky 1 mm.
- **Vedení:** kroužky mají 3 oka, kterými volně kloužou po 3 vodicích tyčích ⌀5 s PTFE povlakem (r 63, po 120°).
- **Membrána:** uvnitř namazaná latexová membrána 0,3 mm.
- **Termistory:** 5 nálitků na kroužcích nejblíže hloubkám 10–90 mm, pod úhly 0/60/120/180/240°. Na dalších 3 kroužcích jsou snímače PW1–3.
- **Izolace:** Kaiflex 18 mm. Vnější poloměr 89 mm se ještě vejde mezi sloupy (r 90).
- **Princip:** písek se posouvá s kroužky, takže tření o stěnu se téměř nepřenáší. Vícekroužkové cely jsou podle srovnání TRB/CRREL nejlepší řešení proti tření o stěnu.

## 5. Vážní čidla, nebo siloměry?

**Siloměry**, tedy tahové a tlakové snímače síly zapojené do osy zatěžování. Ne plošinová ani jednobodová vážní čidla.

- **Vážní čidla** jsou stavěná pro plošinu s výstředným zatížením. V osové sestavě mezi pístem a rámem se ohýbají a jsou poddajná.
- **Kompresní siloměry** jsou tuhé (≈ 0,02–0,1 mm při plném rozsahu). To je pro variantu B zásadní, protože tlak z mrazového zdvihu silně závisí na tuhosti omezení (Ji et al. 2019).
- **S-snímač 2 kN** ve variantě A dává jemné rozlišení (1 kPa ≈ 7,9 N).
- **Teplota:** běžné siloměry třídy C3 jsou kompenzované v rozsahu −10 … +40 °C, takže −10 °C je na hraně. Logovat teplotu siloměru a korigovat.

## 6. Rám z Al profilů (E7-V04)

- **Sestava:** základová deska Al 260 × 200 × 25, 2 sloupy 40×80, příčník 80×80 dlouhý 260 mm. Sloupy jsou 380 mm (A) a 330 mm (B).
- **Výška:** nejvyšší bod (ruční kolo varianty A) je ≈ 605 mm nad podlahou mrazáku, proti odhadovaným ≈ 650 mm vnitřní výšky.
- **Tuhost varianty B při 15,7 kN:** příčník 0,036 mm, sloupy 0,035 mm, siloměr ≈ 0,05 mm, spoje 0,02–0,15 mm. **Rozhodují spoje.** Proto šrouby do čela profilů a žádné úhelníky v silové cestě.
- **Teplotní artefakt varianty B:** Al sloupy 330 mm se při změně o 20 K zkrátí o 0,15 mm. S ocelovou vnitřní sestavou by to do zmrzlého vzorku zatlačilo ≈ 160 kPa. Opatření:
  1. Al distanční trubka v silové cestě;
  2. **slepá zkouška** s Al náhradou vzorku;
  3. LVDT na Invarovém rámečku.
- **Varianta A:** tento problém téměř nemá, protože pružina smrštění rámu převede jen na < 2 kPa.

## 7. Vydrží PETG-CF? (E7-V03, `vypocty.md` §4)

**Varianta A ano. Varianta B jen s Al objímkou.** Pevnost PETG-CF z katalogových listů a literatury: ≈ 40–55 MPa ve směru vlákna nebo vrstvy, jen 15–30 MPa kolmo na vrstvy. Dlouhodobě počítám s ≈ 30 % pevnosti.

| zatěžovací stav | napětí | bezpečnost krátkodobě | dlouhodobě |
|---|---|---|---|
| obvod, A 200 kPa | 1,3 MPa | > 30 | > 9 |
| obvod, B 2 MPa | 12,6 MPa | 3–4 | **1,0–1,3 – nestačí** |
| obvod, B 2 MPa + Al objímka 5 mm | ≈ 1 MPa v PETG | > 40 | > 12 |
| osově přes vrstvy, tření bez fólie, 1 MPa | 5,8 MPa | 2,6–5 | **< 1,6** |
| osově, PTFE fólie / kroužky, 1 MPa | 0,6 MPa | > 25 | > 7 |

Podmínky:
- **Tisk:** nastojato, stěna ≥ 8 mm, pouze soustředné perimetry, 100 % výplň.
- **Vnitřek:** utěsnit epoxidem, aby voda nevnikla do mezer v tisku a tam nezmrzla.
- **Vruby:** žádné tištěné závity ani ostré rohy. Místo nich zalisované závitové vložky a zaoblení.
- **Vůle pístu:** ≥ 0,3 mm.
- **Před použitím:**
  1. tlaková zkouška kroužku;
  2. 10 cyklů mrznutí a tání nasycených vzorků a pak tahová zkouška;
  3. creep kroužku 7 dní.

## 8. Čidla a zapojení na CR1000 (E7-V05, `src/sensors.py`)

| měření | doporučeno | alternativy |
|---|---|---|
| síla A (2 kN) | **Interface SSM 2 kN** – kompenzace −15 … +65 °C, IP67 | HBM S9M/2kN, HBM U2B, ME KD80s, Lorenz K-25 |
| síla B (2× 20 kN) | **HBM C9C/20kN** – ⌀26 × 13 mm, velmi tuhý, provoz −30 … +85 °C | Burster 8402, HBM C10, Futek LTH500 |
| posun (4×) | **RDP DCTH400** – DC-LVDT ±10 mm, výstup ±5 V, −40 … +80 °C | Micro-Epsilon DTA-10D, Solartron AX/10/S, HBM WA-L |
| tlak (6×, A) | **TML PDA-PA 200 kPa** | Kyowa BEC-A (jen 1 buňka), TE EPL (stěna) |
| teplota (≈ 24×) | **Campbell 109SS** – ⌀1,6 mm, ±0,38 °C při 0 °C | Campbell 107 (vzduch, rám) |

**Nevhodné kvůli mrazu:** TE DC-EC/HCD, Interface LBM, AML DBBSM a Burster 8438 (kompenzace nebo provoz jen od 0 °C či výš). HBM S2M existuje jen do 1 kN.

| svorky CR1000 | připojeno | poznámka |
|---|---|---|
| DIFF1–3 + VX1 | 3 siloměry | BrFull, ratiometricky s reverzací |
| SE7–10 | 4 LVDT | ±5000 mV, vlastní zdroj ±15 V |
| DIFF6 + VX3 (2000 mV) + C1/C2 | multiplexer AM16/32B č. 1 (4×16) | 6 tlakových můstků |
| SE13 + VX2 + C3/C4 | multiplexer AM16/32B č. 2 (2×32) | ≈ 24 termistorů |

- **Rozlišení:** síla ≈ 0,04 kPa (A) a ≈ 0,3 kPa (B), posun ≈ 1,3 µm. Absolutní přesnost LVDT ±50 µm → kalibrovat mikrometrem.
- **CR1000:** se už nevyrábí (nástupce CR1000X / CR1000Xe). Stávající stačí, ale musí zůstat mimo mrazák.

## 9. 3D modely pro Onshape (`3d/`)

| soubor | obsah |
|---|---|
| `E7_variant_A.step` | varianta A – rám (sloupy 380), vícekroužková cela, nenasycený písek, tlakové snímače PV1/PH1/PB1/PW1–3, pružina se šroubem, siloměr Interface SSM, 2× LVDT, Invarová reference, termistory |
| `E7_variant_B.step` | varianta B – rám (sloupy 330), cela s Al objímkou, 2× HBM C9C, Al distanční trubka, šroub M24 s ručním kolem, LVDT, termistory |
| `E7_multiring_cell.step` | samotná vícekroužková cela |
| `E7_freezer_layout.step` | obě sestavy na vaně v mrazáku (stěny mrazáku průhledné, ≈ rozměry) |

Náhledy jsou `3d/*.png`. Řez variantou A ukazuje `E7_variant_A_section.png`.

**Import do Onshape:**
1. *Create → Import*, nebo v otevřeném dokumentu tlačítko *Import*.
2. Vybrat soubor `.step`.
3. Díly se načtou s názvy a barvami.
4. Jednotky jsou mm, osa z míří nahoru, z = 0 je horní líc základové desky.

**Zjednodušení modelu:**
- Drážky profilů, závity, kabely a spojovací materiál nejsou modelované.
- Čidla mají obalové rozměry podle katalogů. Přesné CAD modely lze stáhnout od výrobců.

## 10. Literatura (ověřeno vyhledáním; DOI jen kde potvrzeno)

- **Konrad & Morgenstern (1980)**, *Can. Geotech. J.* 17: 473–486. Segregační potenciál klesá s přitížením, proto zkoušet více úrovní přitížení.
- **ASTM D5918**: vícekroužková cela, malé přitížení, dva cykly mrznutí a tání, LVDT.
- **Nixon & Nixon (2015)**, GeoQuébec: tření o stěnu působí jako přitížení až ≈ 35 kPa.
- **Srovnání cel (TRB/CRREL)**: vícekroužkové cely jsou výrazně lepší než kuželové nebo dělené.
- **Jin et al. (2019)**, *Cold Reg. Sci. Technol.* 157: 119–132, doi:10.1016/j.coldregions.2018.09.011. Cela s vlastní regulací teploty.
- **Hoekstra, Chamberlain & Frate (1965)**, CRREL RR 176: siloměr nad vzorkem měří tlak a zároveň brání zdvihu.
- **Ji et al. (2019)**, *Bull. Eng. Geol. Environ.*, doi:10.1007/s10064-018-1345-z: tlak z mrazového zdvihu závisí na tuhosti omezení.
- **Tlakové buňky:**
  - Weiler & Kulhawy (1982), JGED 108(GT12);
  - Labuz & Theroux (2005), doi:10.1520/GTJ12089;
  - Talesnick (2005), doi:10.1520/GTJ12484;
  - Zeng et al. (2022), doi:10.6052/1000-0879-21-231.
- **PETG v mrazu a vlhku:**
  - Ultimaker PETG TDS;
  - Stan et al. (2019);
  - Economides et al. (2024), doi:10.3390/polym16233336;
  - UMaine MS thesis (2024).

## 11. Otevřené otázky

1. **Program regulátoru:** „Set A“ (rampy 192 h mezi −10 a +10 °C) lze použít přímo. Pro jasné kroky zvážit výdrže na −10 °C a +10 °C.
2. **Směr promrzání:** izolace stěn a G10 pod podstavcem vedou k promrzání hlavně shora. Termostatované koncové desky (Jin et al. 2019) jsou možné rozšíření.
3. **Písek:** zrnitost (d50) a cílová vlhkost / stupeň nasycení určí velikost tlakových disků a rozsah snímačů (200 kPa).
4. **Přitížení:** stačí 25–50 kPa (jedna pružina 20 N/mm), nebo i 100–200 kPa (druhá pružina 80 N/mm)?
5. **Rozměry mrazáku a vany:** prosím změřit. Výška sestavy A je ≈ 605 mm.

> Výkresy jsou NÁVRH. Profilové hodnoty, pružiny a údaje o čidlech jsou katalogové odhady. Ověřit u dodavatele a nechat zkontrolovat konstruktérem.
