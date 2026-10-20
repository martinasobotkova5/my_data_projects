# E7: zatěžovací zkoušky zeminy při mrznutí a tání

Vzorek ⌀100 × 100 mm (vnitřní) v plné cele z PETG-CF vytištěné 3D tiskem v jednom kuse, v truhlicovém mrazáku z E6 s programovatelným regulátorem. V obou variantách je **stejný vzorek** (nenasycený písek) a stejná cela. Varianta A má přitížení **závažím** (ocelové kotouče, max. 25 kPa) a měří tlaky uvnitř písku. Varianta B je **bez zatížení** a měří zdvih, sednutí a deformace po vrstvách mezi mrznutím a táním.

| soubor | obsah |
|---|---|
| `vykresy/E7_drawings.pdf` | 6 listů A3, anglicky (PNG po listech ve stejné složce) |
| `3d/*.step` | 3D sestavy pro Onshape: varianta A, varianta B, samotná cela, obě v mrazáku (+ STL a PNG náhledy) |
| `vypocty.md` | zatížení, očekávané deformace, rozlišení LVDT, teplotní chyba stojanu, napětí v cele, závaží |
| `src/params.py` | všechny rozměry a předpoklady |
| `src/sensors.py` | výběr čidel a plán kanálů CR1000 |
| `src/vykresy.py`, `src/vypocty.py`, `src/model3d.py`, `src/render3d.py` | generátory |

Regenerace: `cd src && python vykresy.py && python vypocty.py > ../vypocty.md && python model3d.py && python render3d.py`

---

## 1. Dvě varianty

| | **A – konstantní přitížení** (E7-V01) | **B – bez zatížení** (E7-V02) |
|---|---|---|
| vzorek | nenasycený písek ⌀100 × 100 (Sr ≈ 0,3–0,5) | **stejný** |
| cela | plná, 3D tisk PETG-CF v jednom kuse, PTFE fólie 0,5 mm + silikonový tuk | **stejná** |
| zatížení | **závaží** 5–25 kPa (ocelové kotouče ⌀150 na nosné desce s vodicí tyčí) | **žádné** – jen lehká horní deska PETG-CF (≈ 0,08 kPa) |
| co se měří | tlaky uvnitř písku, u dna a na stěně; LVDT kontrolují, že se vzorek nehýbe | zdvih při mrznutí, sednutí při tání, nevratná deformace za cyklus, poměrné deformace 4 vrstev po 25 mm |
| snímače posunu | 2× LVDT ±10 mm s pružinou | 6× LVDT ±5 mm s **volným jádrem**: S1–S3 na horní desce, E1–E3 na kotvách v hloubce 25/50/75 mm |
| rám | lehký 40×40, sloupy 410 mm, příčka s lineárním ložiskem | **žádný** – jen 3 Invarové sloupky a Al můstek s LVDT |
| termistory | T1–T5 v písku, Ttop, Tbot, Tw, Tframe, Tair | T1–T5 v písku, Ttop, Tbot, Tstand, Tair |
| **bod M** | **TDR + Pt100 + optické čidlo (FBG)** v jednom místě | **stejně** |

Obě varianty sdílejí základovou desku, Al distanční kus, mezikus G10, podstavec s porézním kamenem, tištěnou celu, termistory T1–T5 a bod M (TDR + Pt100 + optické čidlo). Výsledky A a B jsou tak přímo srovnatelné: rozdíl je jen v přitížení.

**Proč závaží (A):**
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
- **Led na snímačích:** snímače utěsnit silikonem nebo epoxidem.
- **Sání v nenasyceném písku:** tenziometry v mrazu zamrznou. Před zmrazením změřit sání (tenziometr nebo filtrační papír) a pak ho odhadovat z teploty (Clapeyron) nebo z obsahu nezamrzlé vody (TDR).

## 4. Cela – plná, 3D tisk z PETG-CF (obě varianty, E7-V03)

- **Tvar:** trubka ⌀117/101, výška 125 mm, patka ⌀150 × 8 se zaoblením R4, tištěno nastojato v jednom kuse. Nad vzorkem zůstává 25 mm pro píst (A) nebo horní desku (B).
- **Vnitřek:** stěna utěsněná tenkou vrstvou epoxidu, pak PTFE fólie 0,5 mm (spoj natupo na 180°) a silikonový tuk → vnitřní ⌀100.
- **Termistory:** 5 nálitků 8 × 10 mm s otvorem ⌀1,7 v hloubkách 10/30/50/70/90 mm pod úhly 0/72/144/216/288°. Hroty v obou variantách na r 40 mm (mimo bod M a tyčky kotev).
- **Snímače na stěně PW1–3:** pouzdra ⌀8 v nálitcích, líc se snímačem zarovnaný s fólií (fólie má v těch místech výřezy ⌀8). Ve variantě B jsou volitelné.
- **Izolace:** Kaiflex 25 mm (vnější r 83,5) s výřezy pro nálitky. Vejde se mezi sloupy rámu A (r 90) i dovnitř Invarových sloupků B (r 100).
- **Bod M:** jeden širší nálitek 34 × 22 mm v hloubce 54 mm pod úhlem 108° pro TDR, Pt100 a optické čidlo (kap. 4a).
- **Cela není přišroubovaná**, jen leží patkou na podstavci. Tření pak stěnu tlačí, ale netrhá vrstvy tisku od sebe.

**Tření o stěnu (`vypocty.md` §5):** u plné cely odnese část přitížení stěna. To vícekroužková cela řešila, plná cela ne, proto je fólie s tukem povinná.

| rozhraní | μ | σv u dna / na povrchu |
|---|---|---|
| PTFE fólie + silikonový tuk | ≈ 0,05 | 0,89–0,92 |
| PTFE fólie nasucho | ≈ 0,10 | 0,79–0,85 |
| bez fólie (písek–PETG) | ≈ 0,5 | 0,30–0,45 |

- **A:** PV1 (40 mm) a PB1 (dno) vyhodnocovat jako profil σv(z), ne jako jednu hodnotu. Rozdíl mezi nimi přímo ukáže tření.
- **B:** přitížení je nulové, takže tření je malé. Zmrzlá horní vrstva ale může přimrznout ke stěně a brzdit zdvih. PTFE má ze všech běžných materiálů nejmenší adhezi ledu.

## 4a. Bod M – TDR, Pt100 a optické čidlo ve stejném místě (obě varianty, E7-V03 detail M, `vypocty.md` §8)

Všechna tři čidla vstupují vodorovně **jedním nálitkem** ve stěně cely, rovnoběžně, a měří stejnou vrstvu písku ve stejném okamžiku promrzání. Poloha je v obou variantách stejná: **hloubka 54 mm pod povrchem, r ≈ 25 mm, úhel 108°** (mezi termistory T2 a T3, mimo kotvy B a tlakové snímače A; kolize zkontrolované v 3D).

| čidlo | provedení | poloha v bodě M | měří | připojení |
|---|---|---|---|---|
| **TDR** | mini 3-tyčková sonda, nerez ⌀1,6 × 40 mm, tyčky nad sebou po 5 mm (hloubky 49/54/59), epoxidová hlava v nálitku | od stěny (r 50) po r 10 | objemová vlhkost, ve zmrzlém stavu **nezamrzlá voda** | koax → SDMX50SP → **TDR200** (SDM C1–C3) |
| **Pt100** | 1/10 DIN, 4vodičové, plášť ⌀3, element 10 mm u hrotu | 12 mm vedle roviny TDR, element r 20–30 | referenční teplota (±0,03 °C při 0 °C) | **4WPB100** → MUX-1 (BrHalf4W) |
| **optické čidlo** | FBG (Braggova mřížka) v nerezové kapiláře ⌀1, mřížka 10 mm u hrotu (bez vlivu deformace) | 12 mm na druhé straně, mřížka r 20–30 | teplota optickou cestou | vlákno ven z mrazáku → interrogátor (HBM FS22 / Luna si155 [ověřit]) na PC |

- **Proč takhle:** kovový plášť Pt100 a kapilára FBG jsou 12 mm od tyček TDR, tj. mimo jeho citlivý objem (≈ 1–1,5× rozteč 5 mm). Přitom všechna tři čidla leží ve stejné hloubce a ve stejném pásu ±12 mm.
- **Co z toho vznikne:**
  - Pt100 je **teplotní reference**: v cele přes ni zkalibrujete FBG i termistor T3 (ledový bod při tání);
  - TDR proti teplotě Pt100 dá **křivku nezamrzlé vody θu(T)**, tedy charakteristiku mrznutí písku;
  - totéž ve variantě A (přitížení 25 kPa) a B (bez zatížení) → vliv přitížení na mrznutí ve stejném bodě.
- **TDR v malém vzorku:** tyčky 40 mm jsou na hranici (dvojí doba běhu jen ≈ 0,5–0,8 ns). Rozlišení vlhkosti je i tak ≈ 0,005, ale je potřeba průměrovat průběhy a sondu kalibrovat přímo v tomto písku. Campbell CS645 (75 mm) je na ⌀100 příliš dlouhá.
- **Montáž:** tyčky TDR a Pt100/FBG se zasunou otvory ve stěně a ve fólii do už uloženého písku (nebo se písek ukládá kolem nich). Hlava TDR zalepená v nálitku, Pt100 a FBG utěsněné silikonem.
- **Optické čidlo:** předpokládám teplotní FBG. Pokud máte jiný typ (fluorescenční sonda, např. Opsens OTG-F s analogovým výstupem do CR1000, nebo distribuované měření DTS), poloha zůstane stejná, změní se jen průměr otvoru a připojení.

## 5. Varianta B – posuny a deformace mezi mrznutím a táním (E7-V02, `vypocty.md` §1–4)

**Sestava:**
- Stejný písek ve stejné tištěné cele s PTFE fólií jako A, bez pístu a bez závaží.
- Na povrchu leží **lehká horní deska** PETG-CF ⌀99 × 6 (≈ 65 g, tj. 0,08 kPa, to je jako tíha horních 5 mm písku). Deska je jen terč pro LVDT.
- **3 povrchové LVDT S1–S3** (r 40, po 120°) stojí na desce. Jejich průměr dává zdvih nebo sednutí povrchu, rozdíl mezi nimi náklon desky.
- **3 kotvy E1–E3** (settlement anchors) jsou při ukládání písku vloženy do hloubky 25, 50 a 75 mm (r 25, po 120°, mimo povrchová LVDT):
  - nerezový kotouček ⌀16 × 1,5;
  - Invarová tyčka ⌀2 vede nahoru v PTFE trubičce ⌀4 (trubička odděluje tyčku od písku nad kotvou);
  - tyčka prochází otvorem ⌀7 v horní desce (deska se po ní volně posouvá) a nese jádro LVDT.
- **LVDT s volným jádrem** (bez pružiny): na vzorek netlačí. Běžné LVDT s pružinou by přidaly 0,1–0,25 kPa na každý snímač, což je víc než celá horní deska.
- **Reference:** těla LVDT jsou upnutá v Al můstku ⌀220 × 10 na 3 Invarových sloupcích ⌀12 (r 100) přišroubovaných do základové desky. Můstek se při plnění cely sundá.

**Co se vyhodnocuje v každém cyklu:**

| veličina | výpočet |
|---|---|
| zdvih povrchu při mrznutí | S̄ = (S1 + S2 + S3)/3, od začátku mrznutí do konce |
| sednutí při tání | pokles S̄ během tání |
| nevratná deformace za cyklus | S̄ na konci tání − S̄ na začátku cyklu |
| deformace vrstev 0–25 / 25–50 / 50–75 / 75–100 mm | Δh₁ = S̄ − E1, Δh₂ = E1 − E2, Δh₃ = E2 − E3, Δh₄ = E3 (dno pevné); εᵢ = Δhᵢ / 25 mm |
| hloubka promrzání | izoterma 0 °C z T1–T5 → deformace zmrzlé vs. nezmrzlé vrstvy v čase |
| po posledním cyklu | výška vzorku (posuvka), hmotnost, vlhkost 5 plátků po 20 mm (přesun vody) |

**Co čekat (`vypocty.md` §2):**
- Horní mez zdvihu z rozpínání vody je 1,0–1,7 mm, ale v nenasyceném písku má led dost místa ve vzduchových pórech. Celkový zdvih bude spíš v desetinách mm.
- Voda se ale může přesouvat k čelu promrzání: horní vrstva nabobtná, spodní se vysuší a smrští. Povrchové LVDT by to nerozlišilo, proto kotvy po vrstvách.
- Při tání se ukáže nevratné zhutnění. To je hlavní výsledek pro porovnání cyklů.

**Přesnost (`vypocty.md` §3–4):**
- LVDT ±5 mm na CR1000: rozlišení ≈ 0,7 µm, poměrná deformace vrstvy 25 mm ≈ 4·10⁻⁵.
- Teplotní chyba stojanu: Al podstavec a distanční kus proti Invaru ≈ 50 µm na 20 K. Odstraní se **slepou zkouškou** s Al náhradou vzorku ve stejném programu (korekce podle Tbot a Tstand). Chyba je společná všem LVDT, takže v rozdílech mezi kotvami se z velké části odečte.
- Linearita LVDT ±0,25 % FS → každý LVDT zkalibrovat mikrometrem.

**Příprava vzorku B:**
1. Do cely s namazanou PTFE fólií uložit písek po vrstvách 12,5 mm na cílovou hustotu a vlhkost.
2. Po dosažení hloubky 75, 50 a 25 mm pod budoucím povrchem položit kotvu, na ní nasadit tyčku s trubičkou a pokračovat v hutnění (tyčky drží ve svislé poloze šablona nad celou).
3. Zarovnat povrch, položit horní desku přes trubičky, nasadit můstek s LVDT a vynulovat.
4. Mezeru mezi deskou a stěnou cely překrýt volnou PE fólií, aby písek během týdnů nevysychal sublimací.

**Siloměry** nejsou potřeba v žádné variantě. A je zatížená závažím (síla = hmotnost), B není zatížená vůbec.

## 6. Rám A a stojan B (E7-V04)

- **Základ:** v obou variantách základová deska Al 260 × 200 × 25 na 3 stavitelných nožkách.
- **Rám A:** 2 sloupy 40×40 × 410 mm a příčka 40×40 s lineárním kuličkovým ložiskem ⌀16 pro vodicí tyč závaží. Rám nenese zatížení, jen vede tyč a nese Invarové sloupky LVDT.
- **Stojan B:** 3 Invarové sloupky ⌀12 × 250 mm (r 100, 60/180/300°, mimo izolaci), nahoře Al můstek ⌀220 × 10 s děleným upnutím pro 5 LVDT (+1 rezerva). Žádný rám, nic se nezatěžuje.
- **Výška:** nejvyšší bod je vodicí tyč A (≈ 590 mm nad podlahou mrazáku, vč. vany). Sestava B je vysoká ≈ 330 mm vč. desky.
- **Teplota:** rám A přitížení nemění. Stojan B je reference posunu, jeho chyba ≈ 50 µm / 20 K se koriguje slepou zkouškou.

## 7. Vydrží PETG-CF? (E7-V03, `vypocty.md` §5)

**Ano, pro obě varianty.** Pevnost PETG-CF z katalogových listů a literatury: ≈ 40–55 MPa ve směru vlákna nebo vrstvy, jen 15–30 MPa kolmo na vrstvy. Dlouhodobě počítám s ≈ 30 % pevnosti.

| zatěžovací stav (obvodové napětí ve stěně) | napětí | bezpečnost krátkodobě | dlouhodobě |
|---|---|---|---|
| A: přitížení 25 kPa, K0 = 1 | 0,16 MPa | > 250 | > 75 |
| B: tlak ledu na stěnu 200 kPa (horní odhad) | 1,3 MPa | 32–44 | 9–13 |
| extrém 1 MPa | 6,3 MPa | 6–9 | 1,9–2,6 |

Osové napětí přes vrstvy od tření je i bez fólie < 0,05 MPa (A, 25 kPa), tedy zanedbatelné. Cela je volně položená, takže tření stěnu tlačí, netáhne.

Podmínky:
- **Tisk:** nastojato v jednom kuse, stěna 8 mm, pouze soustředné perimetry, 100 % výplň, nálitky se zkosením 45° zespodu (bez podpor). Vrtání ⌀101 ± 0,1 zkontrolovat ve 3 výškách.
- **Vnitřek:** utěsnit tenkou vrstvou epoxidu, aby voda nevnikla do mezer v tisku.
- **Vruby:** žádné tištěné závity ani ostré rohy.
- **Před použitím:**
  1. 10 cyklů mrznutí a tání nasycených vzorků materiálu a pak tahová zkouška;
  2. kontrola průměru ⌀101 při +20 a −10 °C (smrštění 0,06–0,12 mm, píst A má vůli 0,25 mm).

## 8. Čidla a zapojení na CR1000 (E7-V05, `src/sensors.py`)

| měření | doporučeno | alternativy |
|---|---|---|
| posun A (2×) | **RDP DCTH400** – DC-LVDT ±10 mm, výstup ±5 V, −40 … +80 °C | Micro-Epsilon DTA-10D, Solartron AX/10/S, HBM WA-L |
| posun B (6×, volné jádro) | **RDP DCTH200** s volným (unguided) jádrem, ±5 mm [ověřit u RDP] | Micro-Epsilon DTA-5G8, Solartron AX/5/F |
| tlak (A 6×, B 3× volitelně) | **TML PDA-PA 200 kPa** | Kyowa BEC-A (jen 1 buňka), TE EPL (stěna) |
| vlhkost, bod M (2×) | **mini 3-tyčková TDR 40 mm** + Campbell TDR200 + SDMX50SP [ověřit] | Easy Test LP/ms; CS645 je příliš dlouhá |
| referenční teplota, bod M (2×) | **Pt100 1/10 DIN, 4vodič, ⌀3** + Campbell 4WPB100 | – |
| optická teplota, bod M (2×) | **FBG v kapiláře ⌀1** + interrogátor HBM FS22 / Luna si155 [ověřit] | fluorescenční Opsens OTG-F (analogově do CR1000) |
| teplota (≈ 20×) | **Campbell 109SS** – ⌀1,6 mm, ±0,38 °C při 0 °C | Campbell 107 (vzduch, stojan) |

**Nevhodné kvůli mrazu:** TE DC-EC/HCD (provoz od 0 °C), laserové snímače optoNCDT (provoz od 0 °C, námraza na okénku).

| svorky CR1000 | připojeno | poznámka |
|---|---|---|
| SE1–2 | LVDT-A1, A2 | ±5000 mV, vlastní zdroj ±15 V |
| SE3–5 | LVDT S1–S3 (B, povrch) | ±5000 mV |
| SE6–8 | LVDT E1–E3 (B, kotvy) | ±5000 mV |
| DIFF6 + DIFF5 + VX3 + C4/C5 | multiplexer AM16/32B č. 1 (4×16) | 9 tlakových můstků (A 6, B 3) + 2× Pt100 přes 4WPB100 |
| C1–C3 (SDM) + 12V | TDR200 → SDMX50SP | 2 sondy TDR (bod M, A i B) |
| SE13 + VX2 + C6/C7 | multiplexer AM16/32B č. 2 (2×32) | ≈ 20 termistorů |
| – | FBG interrogátor (oba body M na jednom vlákně) | vlastní PC, hodiny synchronizované s CR1000 |
| SE14–16 | rezerva | |

- **Rozlišení:** posun ≈ 1,3 µm (A) a ≈ 0,7 µm (B). Absolutní linearita LVDT → kalibrovat mikrometrem.
- **CR1000:** se už nevyrábí (nástupce CR1000X / CR1000Xe). Stávající stačí, ale musí zůstat mimo mrazák.

## 9. 3D modely pro Onshape (`3d/`)

| soubor | obsah |
|---|---|
| `E7_variant_A.step` | varianta A – lehký rám 40×40 (sloupy 410, příčka s ložiskem), tištěná cela s PTFE fólií, nenasycený písek, tlakové snímače PV1/PH1/PB1/PW1–3, G10, nosná deska s tyčí, 3 + 1 ocelové kotouče, 2× LVDT na bocích (±y) s Invarovými sloupky, termistory včetně Tw |
| `E7_variant_B.step` | varianta B – základová deska, stejná tištěná cela, nenasycený písek, horní deska PETG-CF, kotvy E1–E3 s Invarovými tyčkami a PTFE trubičkami, 6× LVDT s volným jádrem, 3 Invarové sloupky, Al můstek, termistory |
| `E7_cell.step` | samotná cela PETG-CF s nálitky, PTFE fólií, izolací, termistory, snímači PW a bodem M (TDR, Pt100, FBG) |
| `E7_freezer_layout.step` | obě sestavy na vaně v mrazáku (stěny mrazáku průhledné, ≈ rozměry) |

Náhledy jsou `3d/*.png`. Řezy ukazují `E7_variant_A_section.png` a `E7_variant_B_section.png`.

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
- **ASTM D5918**: malé přitížení, dva cykly mrznutí a tání, LVDT; norma doporučuje vícekroužkovou celu – u plné cely proto PTFE fólie a vyhodnocení tření.
- **Nixon & Nixon (2015)**, GeoQuébec: tření o stěnu působí jako přitížení až ≈ 35 kPa.
- **Srovnání cel (TRB/CRREL)**: vícekroužkové cely mají menší tření o stěnu než plné; u plné cely je proto nutné tření snížit (fólie, tuk) a změřit (PV1 vs. PB1).
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
4. **Přitížení A:** stačí 5–25 kPa (závaží)? Pro vyšší přitížení je připravená varianta s pružinou.
5. **Varianta B – uzavřený, nebo otevřený systém?** Návrh je uzavřený (bez přítoku vody). Přívod vody zespodu přes porézní kámen (Mariottova láhev) lze doplnit, zdvih pak bude větší a LVDT ±5 mm může být málo.
6. **Optické čidlo:** jaký typ máte (FBG, fluorescenční sonda, DTS)? Návrh počítá s teplotním FBG v kapiláře ⌀1.
7. **TDR:** máte TDR100/TDR200, nebo jiný přístroj (např. Easy Test)? Podle toho se upraví sonda.
8. **Kotvy:** stačí 3 hloubky (25/50/75 mm), nebo chcete hustší profil (např. 5 kotev po 15 mm s menšími kotoučky)?
9. **Rozměry mrazáku a vany:** prosím změřit. Nejvyšší bod (vodicí tyč A) je ≈ 590 mm nad podlahou mrazáku.

> Výkresy jsou NÁVRH. Profilové hodnoty, hmotnosti závaží a údaje o čidlech jsou katalogové odhady. Ověřit u dodavatele a nechat zkontrolovat konstruktérem.
