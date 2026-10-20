# E7: zatěžovací zkoušky zeminy při mrznutí a tání

Vzorek ⌀100 × 100 mm (vnitřní) v tištěné cele z PETG-CF, v rámu z Al profilů, v truhlicovém mrazáku z E6 s programovatelným regulátorem. Obě sestavy jsou **bez páky**: varianta A má přitížení **závažím** (ocelové kotouče, max. 25 kPa), varianta B pevné omezení šroubem.

| soubor | obsah |
|---|---|
| `vykresy/E7_drawings.pdf` | 6 listů A3, anglicky (PNG po listech ve stejné složce) |
| `3d/*.step` | 3D sestavy pro Onshape: varianta A, varianta B, vícekroužková cela, obě v mrazáku (+ STL a PNG náhledy) |
| `vypocty.md` | síly, závaží a jejich tepelná setrvačnost, tuhost rámu, teplotní artefakt, napětí v cele, siloměry |
| `src/params.py` | všechny rozměry a předpoklady |
| `src/sensors.py` | výběr čidel a plán kanálů CR1000 |
| `src/vykresy.py`, `src/vypocty.py`, `src/model3d.py`, `src/render3d.py` | generátory |

Regenerace: `cd src && python vykresy.py && python vypocty.py > ../vypocty.md && python model3d.py && python render3d.py`

---

## 1. Dvě varianty

| | **A – nenasycený písek, konstantní přitížení** (E7-V01) | **B – konstantní výška** (E7-V02) |
|---|---|---|
| vzorek | nenasycený písek (Sr ≈ 0,3–0,5) | zemina podle zadání |
| co se drží | svislé napětí 5 / 10 / 15 / 20 / 25 kPa (výchozí 25 kPa) | výška vzorku (píst opřený o rám) |
| zatížení | **závaží** – ocelové kotouče ⌀150 na nosné desce s vodicí tyčí ⌀16 | jemný šroub M24 × 1,5, dosedací předpětí 5 kPa |
| co se měří | tlaky uvnitř písku, u dna a na stěně; LVDT kontrolují, že se vzorek nehýbe | síla z mrazového zdvihu nahoře a dole (rozdíl = tření o stěnu) |
| siloměr | není potřeba (síla = hmotnost závaží) | 2× kompresní 20 kN |
| cela | vícekroužková + latexová membrána | monolitická + Al objímka 5 mm |
| rám | lehký 40×40, sloupy 410 mm, příčka s lineárním ložiskem | 40×80, sloupy 330 mm, příčník 80×80 |

Obě varianty sdílejí spodní a horní část sestavy:
- podstavec s porézním kamenem a izolační mezikus G10,
- píst s porézním kamenem a kuličku v kuželových sedlech,
- LVDT na Invarovém rámečku a termistory ve stěně.

**Proč závaží:**
- Gravitace dává přesně konstantní přitížení. Nezávisí na posunu vzorku ani na smrštění rámu v mrazu.
- Není potřeba siloměr ani dotahování. Rám jen vede tyč a nese LVDT, takže nic nezatěžuje.
- Do 25 kPa je to 20 kg, tedy 3 plné a 1 poloviční kotouč (výška 126 mm). To se do mrazáku vejde.

## 2. Přitížení závažím (varianta A, E7-V01, `vypocty.md` §7)

**Sestava shora dolů:**
- vodicí tyč ⌀16 v lineárním kuličkovém ložisku v příčce rámu (jen vedení, žádná síla);
- ocelové kotouče ⌀150 se středovým otvorem ⌀18: plný 36 mm ≈ 4,92 kg, poloviční 18 mm ≈ 2,46 kg;
- nosná deska ⌀150 × 10 (1,39 kg) s pevně spojenou tyčí ⌀16 × 230 (0,36 kg);
- tepelný mezikus G10 ⌀60 × 10;
- kulička v kuželových sedlech a píst s porézním kamenem (≈ 1 kg, zvážit).

Pevná část (píst, nosná deska, tyč) ≈ 2,75 kg ≈ **3,4 kPa**, to je nejmenší možné přitížení.

| přitížení [kPa] | celkem [kg] | plné kotouče | poloviční | doladit [kg] |
|---|---|---|---|---|
| 5 | 4,0 | 0 | 0 | 1,25 |
| 10 | 8,0 | 1 | 0 | 0,33 |
| 15 | 12,0 | 1 | 1 | 1,88 |
| 20 | 16,0 | 2 | 1 | 0,96 |
| 25 | 20,0 | 3 | 1 | 0,04 |

**Postup:** všechno, co leží na vzorku, zvážit na váze (±10 g ≈ ±0,01 kPa) a doladit tenkými kotouči nebo podložkami. Kotouče pokládat na nosnou desku pomalu, bez rázu.

**Tepelná setrvačnost:**
- Závaží 20 kg má tepelnou kapacitu ≈ 8,7 kJ/K, vzorek jen ≈ 1,6 kJ/K. Časová konstanta je ≈ 5,5 h.
- Program regulátoru mění teplotu jen o ≈ 0,1 K/h, takže závaží za vzduchem zaostává jen o ≈ 0,6 K.
- G10 mezikus omezí tok tepla ze závaží do pístu. Volitelně obalit kotouče izolací 10 mm. Teplotu závaží logovat (Tw).

**Kdy závaží nestačí:** nad ≈ 25 kPa (max. ≈ 50 kPa = 40 kg) roste výška i tepelná hmota. Pro 50–200 kPa je náhradou předepnutá pružina se šroubem a siloměrem (ISO 10243, 20 nebo 80 N/mm), viz historie repozitáře.

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
- **Kalibrace v písku:** ve stejném písku a cele, pod známým přitížením 5–25 kPa (závaží), zatížení i odlehčení, při +10 a −10 °C.
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
- **Varianta A** siloměr nepotřebuje, síla je dána hmotností závaží.
- **Teplota:** běžné siloměry třídy C3 jsou kompenzované v rozsahu −10 … +40 °C, takže −10 °C je na hraně. Logovat teplotu siloměru a korigovat.

## 6. Rám z Al profilů (E7-V04)

- **Sestava:** základová deska Al 260 × 200 × 25, 2 sloupy 40×80, příčník 80×80 dlouhý 260 mm. To je rám B. Rám A je lehký: 2 sloupy 40×40 × 410 mm a příčka 40×40 s lineárním ložiskem ⌀16 pro vodicí tyč závaží.
- **Výška:** nejvyšší bod (vodicí tyč varianty A) je ≈ 530 mm nad podlahou mrazáku, proti odhadovaným ≈ 650 mm vnitřní výšky.
- **Tuhost varianty B při 15,7 kN:** příčník 0,036 mm, sloupy 0,035 mm, siloměr ≈ 0,05 mm, spoje 0,02–0,15 mm. **Rozhodují spoje.** Proto šrouby do čela profilů a žádné úhelníky v silové cestě.
- **Teplotní artefakt varianty B:** Al sloupy 330 mm se při změně o 20 K zkrátí o 0,15 mm. S ocelovou vnitřní sestavou by to do zmrzlého vzorku zatlačilo ≈ 160 kPa. Opatření:
  1. Al distanční trubka v silové cestě;
  2. **slepá zkouška** s Al náhradou vzorku;
  3. LVDT na Invarovém rámečku.
- **Varianta A:** tento problém nemá. Rám nenese zatížení, takže jeho smrštění přitížení nemění.

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
| síla B (2× 20 kN) | **HBM C9C/20kN** – ⌀26 × 13 mm, velmi tuhý, provoz −30 … +85 °C | Burster 8402, HBM C10, Futek LTH500 |
| posun (4×) | **RDP DCTH400** – DC-LVDT ±10 mm, výstup ±5 V, −40 … +80 °C | Micro-Epsilon DTA-10D, Solartron AX/10/S, HBM WA-L |
| tlak (6×, A) | **TML PDA-PA 200 kPa** | Kyowa BEC-A (jen 1 buňka), TE EPL (stěna) |
| teplota (≈ 24×) | **Campbell 109SS** – ⌀1,6 mm, ±0,38 °C při 0 °C | Campbell 107 (vzduch, rám) |

**Nevhodné kvůli mrazu:** TE DC-EC/HCD, Interface LBM, AML DBBSM a Burster 8438 (kompenzace nebo provoz jen od 0 °C či výš). HBM S2M existuje jen do 1 kN.

| svorky CR1000 | připojeno | poznámka |
|---|---|---|
| DIFF1–2 + VX1 | 2 siloměry (LC-T, LC-B, varianta B) | BrFull, ratiometricky s reverzací |
| SE7–10 | 4 LVDT | ±5000 mV, vlastní zdroj ±15 V |
| DIFF6 + VX3 (2000 mV) + C1/C2 | multiplexer AM16/32B č. 1 (4×16) | 6 tlakových můstků |
| SE13 + VX2 + C3/C4 | multiplexer AM16/32B č. 2 (2×32) | ≈ 24 termistorů |

- **Rozlišení:** síla ≈ 0,3 kPa (B), posun ≈ 1,3 µm. Absolutní přesnost LVDT ±50 µm → kalibrovat mikrometrem.
- **CR1000:** se už nevyrábí (nástupce CR1000X / CR1000Xe). Stávající stačí, ale musí zůstat mimo mrazák.

## 9. 3D modely pro Onshape (`3d/`)

| soubor | obsah |
|---|---|
| `E7_variant_A.step` | varianta A – lehký rám 40×40 (sloupy 410, příčka s ložiskem), vícekroužková cela, nenasycený písek, tlakové snímače PV1/PH1/PB1/PW1–3, G10, nosná deska s tyčí, 3 + 1 ocelové kotouče, 2× LVDT na bocích (±y) s Invarovými sloupky, termistory včetně Tw |
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
4. **Přitížení:** stačí 5–25 kPa (závaží)? Pro vyšší přitížení je připravená varianta s pružinou.
5. **Rozměry mrazáku a vany:** prosím změřit. Výška sestavy A je ≈ 530 mm.

> Výkresy jsou NÁVRH. Profilové hodnoty, hmotnosti závaží a údaje o čidlech jsou katalogové odhady. Ověřit u dodavatele a nechat zkontrolovat konstruktérem.
