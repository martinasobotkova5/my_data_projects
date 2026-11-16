# E7 – co může při měření zlobit a postup zkoušky (rev. B3, 11/2026)

Sestava: rám z T-profilů, cela ⌀220 tištěná vcelku na 3 podložkách G10, písek ⌀100 × 100 mm, Sr = 0,5,
mrtvá váha na pístu ⌀50, (1) kamera + laser 11 čar, (2) LVDT na invarovém sloupku, bod M (TDR CS645, Pt100,
optické vlákno), datalogger **CR850**. Výpočty: `vypocty.md` §15–18.

## 1 · Rizika a opatření

| # | co může zlobit | dopad na měření | opatření (✓ = zapracováno do návrhu) |
|---|---|---|---|
| 1 | **Rám se překlopí** při nasazování kotoučů – stačí ≈ 40 N vodorovně na horní příčník | rozhozený vzorek, čidla | ✓ podélníky 320 mm, nohy ±140 (H_krit 37 → 48 N, §17); kotouče nasazovat oběma rukama, druhou rukou přidržet rám; v mrazáku rám stojí ve vaně |
| 2 | **Cela není souosá s vodicí tyčí** (cela na podložkách není nikde ustavena) | nesymetrické mezikruží, píst u stěny, jiné pokrytí čarami | ✓ středicí víčko **P09** na límci – tyč projde středem, celou posunout, víčko vysunout |
| 3 | **Povrch písku není v přesné výšce / rovinný** | chyba výšky pístu vůči límci, rozptýlené čáry laseru | ✓ stěrka **P10** – leží na límci, břit přesně 34 mm pod hranou → povrch 100 mm, rovinný |
| 4 | **Hutnění kolem tyček TDR a Pt100** – dutiny pod tyčkami, ohnuté tyčky, zlomené vlákno | špatný kontakt → chyba vlhkosti TDR, zpožděná teplota | hutnit **bez čidel**, otvory ve vnitřní stěně zaslepit kolíky ⌀3; po zhutnění předvrtat tyčinkou ⌀3 a čidla zasunout portem (jako v terénu); zkontrolovat průběh TDR |
| 5 | **Hutnění na celě stojící na 3 podložkách** | ohyb dna, posun podložek | hutnit **mimo rám** na rovné tuhé desce (celé dno podepřené), pak celu přenést |
| 6 | **Nestejné zhutnění po výšce** | rozdílné sedání, nepřesná Sr | 5 vrstev po 20 mm, každá na **stejnou hmotnost** (tabulka níže), povrch vrstvy zdrsnit; výšku kontrolovat |
| 7 | **Kabely tahají za celu** (RG58 TDR je tuhý) | posun cely, šum LVDT a kamery | kabely přichytit do drážky podélníku (příchytky drážka 8), smyčka bez napětí mezi celou a rámem |
| 8 | **Vážení cely každý cyklus** = vyndat ji z rámu | rozhodí čidla, nulu LVDT a kamery | celu během série **nevážit**; místo toho kontrolní miska („svědek“) se stejným pískem vedle cely, váží se každý cyklus; celu zvážit jen na začátku a na konci série + na konci vlhkost po vrstvách (sušení) |
| 9 | **Vymrzání / sublimace z volného mezikruží**, námraza a rosa při začátku tání | zdánlivý zdvih desítky µm, pokles Sr u povrchu | RH vzduchu (SHT45), svědek, ventilátor; začátek tání vyhodnocovat opatrně; počet cyklů na jeden vzorek omezit (např. 5) |
| 10 | **Výměna vzorku**: tyč sedí v límci, kamera visí 6 mm nad límcem (−y), rameno terčíku je v úrovni límce (+y) | náraz do kamery = nová kalibrace | ✓ parkovací vidlice **P11** (tyč nahoru o 30 mm); celu vyjímat **směrem +y** (k laseru) po natočení ramene P03 stranou – ověřeno v 3D modelu (−y projde jen s vůlí 6 mm pod kamerou) |
| 11 | **Změna zatížení** (přidání kotouče) | průhyb příčky T03 se změní o 0,7 µm/kg → jde do LVDT | zanedbatelné; zatížení měnit jen mezi sériemi, po změně vynulovat |
| 12 | **CR850 má jen porty C1–C4** (C1–C3 bere TDR), LVDT na SE dává jen 2,7 µm | – | ✓ jen 3 teploty → bez multiplexoru; C4 spouští snímek; LVDT a ventilátor trvale napájené; LVDT **diferenciálně** (1,3 µm, průměr ≈ 0,5 µm), plán kanálů §18 |
| 16 | **Teplota dna cely se neměří** – korekce driftu ze slepé zkoušky by stála jen na teplotě písku | zbytkový drift větší než 6 µm | ✓ termistor NTC v radiálním otvoru ve dně cely (CR850 SE6) |
| 13 | **LVDT při −10 °C** (pružina, mazivo jádra) | skoky, hystereze | ověřit u výrobce; ve slepé zkoušce sledovat hladkost průběhu |
| 14 | **Zamrzlé pouzdro / tyč** (námraza při přechodu na tání) | tření → píst „visí“ | drylin bez maziva; před táním vlhkost vzduchu nízko (ventilátor); kontrola: LVDT a kamera na pístu musí souhlasit |
| 15 | **Odrazivost povrchu se mění** (mokrý ↔ zmrzlý písek, námraza) | detekce čar laseru | pevná expozice, kalibrace kamery podložkami jak v nezmrzlém, tak ve zmrzlém stavu (slepá zkouška) |

## 2 · Příprava vzorku (Sr = 0,5)

Předpoklad: pórovitost n = 0,38, hustota zrn 2,65 g/cm³ → ρd ≈ 1,64 g/cm³, θ = 0,19, w = 11,6 %.
Po stanovení skutečné hustoty zrn a cílové ρd hodnoty přepočítat.

| vrstva (20 mm, ⌀100) | suchý písek | voda | vlhký písek |
|---|---|---|---|
| 1 vrstva | 258 g | 30 g | **288 g** |
| celkem 5 vrstev | 1 290 g | 150 g | **1 440 g** |

1. Písek navlhčit na w = 11,6 % (+ ≈ 0,3 % na odpar při míchání), promíchat, uzavřít 24 h v sáčku.
2. Celu postavit na rovnou tuhou desku (celé dno podepřené). Otvory pro tyčky TDR a Pt100 ve vnitřní stěně zaslepit
   kolíky ⌀3 zevnitř portu.
3. Hutnit 5 vrstev po 288 g pěchem ⌀95 na výšku 20 mm (značky na tyčce pěchu), povrch každé vrstvy zdrsnit.
4. Poslední vrstvu srovnat stěrkou **P10** (otáčet na límci) – povrch přesně 34 mm pod hranou límce.
5. Kolíky vytáhnout, tyčinkou ⌀3 předvrtat kanálky, zasunout CS645 (hlavu do portu), Pt100 (osa 3,5 mm nad horní
   tyčkou, hrot 30 mm od stěny) a vlákno. Zkontrolovat průběh TDR a odečet vlhkosti.
6. Zvážit celu (začátek série), vzorek písku do kontrolní misky (svědek) a zvážit.

## 3 · Vložení do rámu a start

1. Parkovací vidlice **P11** na příčníku, tyč zvednutá; rameno terčíku **P03** natočit stranou (značka na sloupku).
2. Celu vsunout ze strany **+y** a postavit na příčku T03 (podložky v kapsách). Kabely přichytit k podélníku.
3. Píst na střed povrchu, kulička do otvoru ⌀6. Na límec nasadit středicí víčko **P09**.
4. Vidlici odebrat, tyč spustit víčkem na kuličku, celou posunout do souososti, víčko vysunout do strany.
5. Rameno P03 vrátit na značku, terčík ve výšce horní hrany límce.
6. Nosná deska a kotouče (přidržet rám!), kroužek: nosná deska 37 mm nad T04 (zdvih ±25).
7. LVDT jádro do středu rozsahu (≈ 0 V). Mrazák zavřít, 24 h při +10 °C, pak vynulovat (1) a (2) a spustit cyklus
   24 h −10 °C / 24 h +10 °C.

## 4 · Během série

- Každý cyklus: zvážit svědka, zkontrolovat RH, LVDT ↔ kamera na pístu (musí souhlasit do ≈ 10 µm).
- Celu nevyjímat a nevážit. Zatížení neměnit.

## 5 · Konec série / výměna vzorku

1. Kotouče a nosnou desku sejmout, tyč zvednout a postavit pod kroužek vidlici P11.
2. Rameno P03 natočit stranou, celu vyjmout směrem +y (pozor na kabely).
3. Zvážit celu. Čidla vytáhnout portem. Písek odebírat po vrstvách 20 mm a sušit (105 °C) → profil vlhkosti
   (ukáže migraci vody k povrchu při mrznutí).
4. Celu vyčistit, zkontrolovat nátěr dutiny; nový vzorek podle bodu 2.

## 6 · Slepá zkouška (před prvním vzorkem)

Hliníková atrapa ⌀99 × 100 místo písku, celý cyklus: drift (1) a (2) proti teplotě cely → fit a odečet (zbytek
≤ 6 µm LVDT, ≤ 3 µm kamera). Kalibrace kamery podložkami 0,1 / 0,5 / 1,0 mm pod rovnou deskou v nezmrzlém i ve
zmrzlém stavu.


## 7 · Zapojení laseru (Picotronic DOE253-635-5-6(10x24))

Laser se napájí z Raspberry Pi 5 v boxu kamery (5 V), zapíná se tranzistorem z GPIO jen na dobu snímku.
GPIO samo laser napájet nesmí (3,3 V a max. ≈ 16 mA), proto spínač MOSFET na záporném vodiči.

```
RPi 5 (40pin)                                  laser DOE253 (5 V DC)
 pin 2  (5V) ───────────────────────────────── červený (+)
                                               černý (−) ──┐
                                                           │ D
 pin 11 (GPIO17) ──[100 Ω]──┬──────────────── G  MOSFET AO3400 / IRLZ44N
                            │                              │ S
                         [100 kΩ]                          │
 pin 9  (GND) ──────────────┴──────────────────────────────┘
```

- **Polarita:** červený = +, černý = − (ověřit podle štítku / listu Picotronic, přepólování může diodu zničit).
- **100 kΩ** mezi gate a GND drží laser vypnutý při startu RPi; **100 Ω** omezuje proud do gate.
- **Vedení kabelu:** laser sedí v držáku P05 na straně +y vedle horního příčníku T04. Kabel 2 × 0,25 mm²
  (prodloužit přívody laseru, spoj zapájet a přetáhnout bužírkou) vést drážkou příčníku T04 na stranu −y
  k závěsu P08, do boxu kamery druhou vývodkou PG7. Délka ≈ 0,5 m. Spínač připájet na malou destičku
  přišroubovanou na víko P07 vedle RPi.
- **Program (RPi):** `gpiozero.OutputDevice(17)` → zapnout laser, 0,2 s počkat, snímek s pevnou expozicí,
  laser vypnout; doporučeno ještě druhý snímek bez laseru (odečet pozadí). Interval 10 min, kolem 0 °C 1 min.
- **Zaostření:** při prvním zapnutí zaostřit kroužkem laseru na povrch (200 mm), čáry co nejtenčí; pak zajistit
  červíkem M3 v držáku P05 a natočit laser tak, aby čáry ležely napříč (ve směru x).
- **Rosa na optice laseru** na začátku tání: laser je mimo vyhřátý box – ve slepé zkoušce zkontrolovat ostrost
  čar po přepnutí na +10 °C; kdyby se rosil, nechat laser svítit trvale (5 mW = zanedbatelné teplo) nebo jej
  obalit pěnou.
- **Bezpečnost (třída 2M):** nedívat se do svazku, ani přes lupu / objektiv; svítí jen při snímku v zavřeném mrazáku.


## 8 · 3D model povrchu ruční fotogrammetrií (bez motoru)

Průběžné měření (každých 10 min) dělá LVDT a pevná kamera s laserem. **3D model** celého povrchu se pořídí ručně
v klíčových stavech – vždy na konci fáze, kdy je teplota ustálená:

| kdy | stav |
|---|---|
| 1 | po přípravě vzorku, před zmrazením (výchozí model) |
| 2 | na konci fáze −10 °C (zmrzlý povrch) – jen pokud to průběh dovolí, mrazák otevřít co nejkratší dobu |
| 3 | na konci fáze +10 °C po roztátí |
| 4 | konec série (před vyjmutím vzorku) |

- **Příprava (jednou):** na horní hranu límce cely nalepit 8 kódových značek ArUco 10 mm (po obvodu), vedle cely
  položit ocelové měřítko 150 mm; horní plochu pístu nastříkat jemným matným náhodným vzorem.
- **Snímání:** sejmout kotouče a nosnou desku, tyč zvednout a podložit vidlicí **P11** (píst zůstává na písku);
  mobilem nebo fotoaparátem 30–50 snímků dokola ve dvou výškách (asi 30° a 60° nad povrchem), překryv ≥ 70 %,
  bez blesku, rovnoměrné světlo. Trvá ≈ 5 min, pak zátěž vrátit (kroužek na značku) – LVDT se vrátí na původní
  hodnotu, kontrola správného usazení.
- **Vyhodnocení:** COLMAP nebo Meshroom (zdarma), případně Agisoft Metashape → mračno bodů → síť; měřítko
  z ArUco značek a měřítka; modely srovnat podle značek na límci → mapa rozdílu výšek mezi stavy (≈ 20–50 µm).
- Model je z celých 360° (bez stínu za pístem a bez vlivu mrazu na techniku); průběh mezi stavy dává LVDT
  a laser.


## 9 · Sublimační série – podstavec pod „kamenem“ (hlavní nová série)

**Co se měří:** led z písku v suchém mrazivém vzduchu sublimuje (mění se přímo v páru). Volné mezikruží kolem pístu
proto klesá, pod pístem („kámen“) je led zakrytý a zůstává → vzniká podstavec. Laser měří pokles volného povrchu
(≈ 10 µm), LVDT pohyb pístu (≈ 1 µm), váha v mrazáku úbytek ledu z kontrolní misky, SHT45 vlhkost vzduchu.
Odhady rychlostí: `vypocty.md` §21.

**Navíc oproti ostatním sériím:** tác se silikagelem (1–2 kg) do mrazáku, malá váha (tenzometr 1 kg + HX711 na RPi)
s miskou, sítko 2 mm na drcený led, čidlo SHT45 na kabelu u vzorku (povinné).

### 9.1 Předzkouška (2–3 dny, bez cely)
1. Na váhu v mrazáku dát skleněnou misku ⌀90 s čistým ledem (vrstva 10 mm) a vedle misku s pískem nasyceným ledem.
2. Mrazák −10 °C, ventilátor zapnutý, silikagel v tácu; RPi zapisuje hmotnost a RH každých 10 min.
3. Výsledek: rychlost sublimace čistého ledu [mm/den] a písku s ledem při dané RH → podle ní zvolit délku série
   (cíl: pokles volného povrchu ≥ 0,5 mm).

### 9.2 Příprava vzorku
- **A – pórový led (kontrola):** písek nasytit vodou (Sr ≈ 1), hutnit po vrstvách jako v kap. 2, zmrazit shora
  v mrazáku. Při sublimaci vznikne suchá vrstva, povrch by klesat neměl.
- **B – přebytek ledu (hlavní):** v mrazáku při −10 °C smíchat suchý zmrzlý písek s drceným ledem (sítko 2 mm)
  v poměru objemů ≈ 40 : 60, plnit po vrstvách 20 mm a lehce upěchovat, každou vrstvu pokropit ledovou vodou
  (stmelí ji); celou přípravu dělat v mrazáku, aby led neroztál. Hmotnost vrstev zapsat (obsah ledu).
- Povrch srovnat stěrkou **P10**, ve zmrzlém stavu; čidla TDR a Pt100 zasunout jako v kap. 2 (předvrtat tyčinkou).

### 9.3 Průběh
1. Celu vložit do rámu (kap. 3), píst na střed: **bez kotoučů** (3,5 kPa – „samotný kámen“) nebo **s kotouči**
   (25 kPa) – dva vzorky / dvě série.
2. Mrazák stále −10 °C, ventilátor, silikagel; laser + kamera a LVDT každých 10 min, váha a RH na RPi.
3. Délka 14–30 dní podle předzkoušky. Volitelně **série B2:** stejné, ale každých 7 dní krátké tání (6 h při +5 °C)
   jako letní oteplení na Ostrově Jamese Rosse – ukáže, jestli tání podstavec „rozmaže“.
4. Konec: zvážit celu, vzorek rozříznout svisle (ve zmrzlém stavu) a změřit tloušťku suché vrstvy pod volným
   povrchem a pod pístem (posuvné měřítko, foto s měřítkem); ruční 3D model povrchu (kap. 8) před a po.

### 9.4 Vyhodnocení
- výška podstavce h(t) = pokles volného mezikruží (laser) − pohyb pístu (LVDT);
- rychlost sublimace z misky [mm/den] a z cely (úbytek hmotnosti) vs. RH;
- tloušťka suché vrstvy L(t) – srovnat s √t (difuze, `vypocty.md` §21);
- srovnání: pórový led × přebytek ledu, 3,5 × 25 kPa, bez tání × s krátkými táními;
- vztah k terénu: rychlost ústupu ledu v Antarktidě (Victoria Valley ≈ 0,22 mm/rok – model; laboratoř je řádově
  rychlejší, porovnává se mechanismus a poměr krytý / volný povrch, ne absolutní rychlost).


## 10 · Fáze 1 – mrznutí a tání BEZ ZATÍŽENÍ, kamera obíhá kolem vzorku (varianta U, výkres V07)

Začíná se touto jednodušší fází. Rám, laser, podložky G10 a bod M jsou stejné jako výše.

- **Nemontuje se:** píst, kulička, vodicí tyč zátěže, pouzdro P01, nosná deska se závažím, LVDT s ramenem P02 ani pevný box kamery na závěsu P08.
- **Na invarovém sloupku** je jen rameno s terčíkem P03.
- **Kamera:** malá hlava s Raspberry Pi Camera Module 3 obíhá kolem vzorku na hřídeli, který prochází otvorem ⌀14 v horním příčníku.

**Sestavení (oproti kap. 1–3):**

1. **Cela E7-V03u** (⌀220 × 171, rovné čelo 5 mm nad pískem) přijde na 3 podložky G10. Vystředit podle rysky na příčce T03 na ±1 mm. Hlava obíhá kolem osy příčníku, kamera vidí celý povrch s rezervou.
2. **Invarový sloupek** ⌀16 do patky P04. Rameno P03 nasunout shora a utáhnout tak, aby **spodní plocha terčíku byla 3 mm nad čelem cely**. Rameno obchází celu zvenku, terčík je na straně kamery (−y). Na terčík nalepit bílou matnou samolepku 12 × 12.
3. **Oběh – nad příčníkem:**
   1. Ložiskový blok P12 se 2 ložisky 6001-2RS přišroubovat 4× M5 do horních drážek, otvor bloku nad otvor ⌀14.
   2. Hřídel ⌀12 h6 × 120 prostrčit shora blokem a příčníkem.
   3. Na hřídel nasadit stavěcí kroužek DIN 705 tak, aby hřídel na něm visel a kroužek se opíral o vnitřní kroužek horního ložiska.
   4. Nad kroužek nasadit kolo P17 (z72) a utáhnout červíkem M4.
   5. Na stojánek P16 (strana −x, 2× M5) přišroubovat motor 28BYJ-48 hřídelí nahoru a nasadit pastorek P19 do záběru s kolem.
   6. Hall senzor A3144 přilepit do držáku na stojánku, magnet ⌀6 × 2 do kolíku v kole na straně −y. Ten určuje výchozí polohu.
4. **Oběh – pod příčníkem:**
   1. Rameno s hlavou P14 nasunout na spodní konec hřídele.
   2. Natočit hlavu na stranu −y, když je magnet u senzoru.
   3. Výšku nastavit tak, aby mezera náboje pod příčníkem byla 4 mm, a utáhnout 2 červíky M4.
   4. Camera Module 3 přišroubovat 4× M2 do hlavy čočkou do okénka ⌀12.
   5. Bílou LED na hvězdě ⌀20 přilepit tepelně vodivým lepidlem vedle okénka.
   6. Do hlavy vlepit 2 topné odpory 47 Ω / 1 W. Zavřít víčkem P15, plochý kabel a 4 vodiče vést výřezem.
5. **Box P06 s RPi 5** postavit do vaničky P18 na horní straně příčníku (strana +x, 2× M5).
   - Plochý kabel kamery 500 mm vést přes hranu příčníku pod něj a k náboji.
   - Kolem náboje udělat volnou smyčku (jeden závit), aby se hlava mohla otočit ±180°. Pak kabel vést po rameni do hlavy.
   - **Před prvním měřením projet celý rozsah ručně** a zkontrolovat, že kabel nikde nedře a nenapíná se.

**Příprava vzorku:** hutnit po vrstvách 20 mm jako v kap. 2. Poslední vrstvu srovnat **stěrkou P10u** (příčka leží na čele cely, břit 5 mm) otáčením kolem osy. Povrch je pak přesně 5 mm pod čelem. Hlava je při tom otočená na stranu +y, mimo práci.

**Zapojení na RPi 5:**

| co | piny RPi (fyzické) | poznámka |
|---|---|---|
| laser (kap. 7) | pin 11 = GPIO17 → MOSFET | 5 V, svítí jen při snímku |
| LED 1 W + 6,8 Ω | pin 13 = GPIO27 → druhý MOSFET AO3400 | 5 V (pin 4), GND pin 14 |
| motor 28BYJ-48 přes ULN2003 | IN1–IN4 = GPIO5, 6, 13, 19 (piny 29, 31, 33, 35) | napájení desky 5 V (pin 2) a GND; po pohybu všechny výstupy vypnout |
| Hall A3144 | GPIO26 (pin 37) + pull-up 10 kΩ na 3,3 V | napájení 3,3 V (pin 1); magnet = výchozí poloha |
| topení hlavy 2× 47 Ω paralelně | 5 V trvale (≈ 1 W) | drží Camera Module 3 nad 0 °C (provozní rozsah 0–50 °C), okénko bez rosy |
| spouštění snímku z CR850 | C4 → optočlen → GPIO22 (pin 15) | jako dosud |

**Snímání:**

- **Průběžně** (spuštění z CR850, interval 10 min, kolem 0 °C 1 min) – hlava stojí ve **výchozí poloze**. Pořizují se tři snímky s pevnou expozicí a pevným zaostřením (autofokus jednou nastavit a uzamknout, `LensPosition`):
  1. s LED – fotka povrchu;
  2. s laserem bez LED – čáry pro výšku;
  3. bez světla – pozadí.
- **Oběh pro 3D model** – v klíčových stavech: před zmrazením, na konci −10 °C, po roztátí, konec cyklu; podle potřeby i každý cyklus.
  1. Najet na výchozí polohu (Hall) vždy ze stejné strany.
  2. Otočit na −180°.
  3. Po 10° až do +170° pořídit 36 snímků s LED, každý s úhlem v názvu souboru.
  4. Vrátit se do výchozí polohy.
  - Trvá ≈ 1,5 min; laser je při oběhu vypnutý.
- **Výška z laseru** se počítá ve výchozí poloze **vůči čarám na rovném čele cely a na invarovém terčíku** v témže snímku. Malá nepřesnost návratu ramene (≈ 0,1°) se tím vyruší.

**Slepá zkouška S0 (povinná):** místo písku hliníková atrapa ⌀99 × 100 se stejným čelem, 2 celé cykly −10 / +10 °C.

- Z ní se zjistí, o kolik se „pohne“ povrch jen teplotou (dno cely a podložky ≈ 70 µm na 20 K). V měřené řadě se to pak odečítá podle teploty dna (NTC).
- Posun rámu (≈ 140 µm na 20 K) ukazuje terčík P03 a odečítá se průběžně.
- **Ve S0 se zkouší i oběh při −10 °C:** rozjezd motoru, kabel, rosa na okénku při přechodu na +10 °C.

**Vyhodnocení fáze 1:**

- zdvih při mrznutí a sednutí při tání po celé ploše (mapa 11 profilů);
- průměr, rozdíl střed × okraj u stěny a zbytková deformace po cyklu;
- z oběhů 3D model povrchu (fotogrammetrie, měřítko ze značek ArUco na čele cely) a jejich rozdíly mezi stavy;
- fotky povrchu z každého cyklu.

Ve fázi 2 se pak stejný postup opakuje s pístem (zatížená × volná část) a se sublimací (kap. 9). **Oběh ve fázi 2 nejde**, středem vede vodicí tyč zátěže. Hlava se připevní pevně ve výchozí poloze a 3D model se dělá ručně (kap. 8).
