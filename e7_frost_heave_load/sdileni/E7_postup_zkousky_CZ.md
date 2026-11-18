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


## 7 · Zapojení laseru – bez pájení

Laser (5 V) se zapíná **kontaktem relé** z dvoukanálového modulu relé se šroubovacími svorkami; relé ovládá Raspberry Pi
(GPIO17) jen na dobu snímku. Vodiče laseru se prodlouží **pákovými svorkami WAGO 221** (žádné pájení, žádná bužírka),
kabel vede drážkou příčníku T04 k boxu s Raspberry Pi na pravém sloupu.

- **Polarita:** červený = +, černý = − (ověřit podle štítku laseru); + laseru na kontakt relé (NO), druhý kontakt na 5 V
  svorkovnicového HATu, − laseru na GND.
- **Program:** `e7_kamera.py` zapne relé, 0,3 s počká, sejme snímek s pevnou expozicí a relé vypne; třetí snímek bez
  světla slouží jako pozadí. Ovládá se z počítače (webová stránka nebo SSH).
- **Zaostření:** při prvním zapnutí zaostřit kroužkem laseru na povrch, čáry co nejtenčí; zajistit červíkem M3 v držáku P05.
- **Bezpečnost (třída 2M):** nedívat se do svazku, ani přes lupu nebo objektiv; svítí jen při snímku v zavřeném mrazáku.


## 8 · 3D model povrchu ruční fotogrammetrií (bez motoru)

Průběžné měření (každých 10 min) dělá LVDT a pevná kamera s laserem. **3D model** celého povrchu se pořídí ručně
v klíčových stavech – vždy na konci fáze, kdy je teplota ustálená:

| kdy | stav |
|---|---|
| 1 | po přípravě vzorku, před zmrazením (výchozí model) |
| 2 | na konci fáze −10 °C (zmrzlý povrch) – jen pokud to průběh dovolí, mrazák otevřít co nejkratší dobu |
| 3 | na konci fáze +10 °C po roztátí |
| 4 | konec série (před vyjmutím vzorku) |

- **Příprava (jednou):** nic se nelepí – měřítko 3D modelu dává známý průměr dutiny ⌀100 a invarový terčík P03;
  vedle cely lze položit ocelové měřítko 150 mm.
- **Řízení – vše z počítače:** motor, LED, laser, topení i kameru řídí **Raspberry Pi Zero 2 W** (podle výrobce funguje od −20 °C) programem `rpi/e7_kamera.py`. Na počítači stačí otevřít v prohlížeči jeho webovou stránku (tlačítka *Výchozí poloha, Sada laser + LED, Oběh, Test*, teplota hlavy, poslední snímek) nebo se připojit přes SSH; CR850 se obsluhuje jako dosud z LoggerNetu. Arduino není potřeba: poloha se počítá v krocích, takže na přesném časování nezáleží, a jeden program pak sám otočí, počká, rozsvítí a vyfotí. Příkazy: `test`, `home`, `laser`, `orbit [krok]`, `run` (trvalý běh: puls z CR850 = sada snímků ve výchozí poloze, oběh v nastavených časech). Cíl se vždy najíždí ve stejném směru (vůle převodovky), po pohybu se cívky vypnou, poslední poloha se ukládá do `~/e7/stav.json`.

**Snímání:** sejmout kotouče a nosnou desku, tyč zvednout a podložit vidlicí **P11** (píst zůstává na písku);
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


## 10 · Kamera obíhá kolem vzorku – jedna sestava pro fázi 1 i 2 (výkresy V07, V08)

Začíná se fází 1 bez zatížení. Rám, laser, podložky G10, bod M a **oběh kamery** jsou pro obě fáze stejné. Ve fázi 2 se jen přidá zátěž: píst, kulička, vodicí tyč, nosná deska se závažím, LVDT s ramenem P02. Hlava pak obíhá kolem tyče se závažím.

- **Pouzdro igus** vodicí tyče je v pevném jádře oběhu P12. Dřívější pouzdro P01, pevný box kamery a závěs P08 se nepoužívají.
- **Na invarovém sloupku** je ve fázi 1 jen rameno s terčíkem P03, ve fázi 2 přibude rameno LVDT P02.

**Sestavení (oproti kap. 1–3):**

1. **Cela** E7-V03u (⌀220 × 146, dutina přesně ⌀100 × 100) je **stejná pro obě fáze**. Stojí na 3 podložkách G10 ⌀20 × 20 na příčce T03; dva dorazy **P20** (2× M5 každý do drážek T03) ji vystředí pod vodicí tyč – bez rysek a bez měření. Ve fázi 2 vystředit na tyč víčkem P09.
2. **Invarový sloupek** ⌀16 do patky P04. Rameno P03 (tištěné z bílého PETG – terčík bez samolepky) utáhnout tak, aby **spodní plocha terčíku byla 3 mm nad čelem cely**. Terčík je na straně kamery (−y), nalepit na něj bílou matnou samolepku 12 × 12.
3. **Oběh – pevná část pod příčníkem:**
   1. Do jádra P12 zalisovat pouzdro igus RJ4JP-01-12 (rukou, bez lepidla).
   2. Na čep ⌀30 nasunout horní ložisko 6806-2RS, distanční kroužek P12b a spodní ložisko.
   3. Zespodu je stáhnout svěrným kroužkem P12c (3× M3 × 10).
   4. Jádro přišroubovat 4× M5 do T-matic ve spodních drážkách T04, otvor pouzdra přesně pod otvor ⌀14.
4. **Oběh – otočná část:**
   1. Náboj P13 (věnec z72, vodorovná clona výchozí polohy) nasunout zespodu na vnější kroužky ložisek.
   2. Pod něj přišroubovat rameno s hlavou P14 (2× M3). Patka ramene drží spodní ložisko.
   3. Motor 28BYJ-48 přišroubovat pod desku držáku P16 (uši M4, hřídel nahoru), na hřídel nalisovat pastorek P19.
   4. Držák přišroubovat 2× M5 do spodních drážek na straně −x, pastorek do záběru s věncem s malou vůlí.
   5. Držák koncovky **P21** přišroubovat 2× M5 do spodních drážek na straně +x, na něj 2× M3 optickou vidlicovou koncovku tak, aby clona náboje procházela štěrbinou.
5. **Hlava kamery:**
   1. Camera Module 3 přišroubovat 4× M2 do hlavy, čočkou do okénka ⌀12.
   2. Modul výkonové LED přišroubovat M3 na výstupek hlavy vedle okénka.
   3. Na víčko P15 přišroubovat (M3) topné tělísko PTC 5 V a sponu s teploměrem DS18B20; zavřít víčkem.
6. **Box P06 s Raspberry Pi Zero 2 WH** (svorkovnicový HAT, modul relé, deska ULN2003, modul optočlenu) na polici držáku P18 na vnější straně pravého sloupu (2× M5). Box obalit deskou XPS 20 mm (stažená páskami, nelepí se). Vše se propojuje kabely Dupont a svorkami – nic se nepájí.
   - Plochý kabel kamery 500 mm vést od boxu pod příčník k náboji.
   - Kolem náboje nechat volnou smyčku (jeden závit), pak kabel vést po rameni do hlavy, spolu s vodiči LED a topení.
   - **Před prvním měřením spustit `python3 e7_kamera.py test`** (výchozí poloha, ±90°, zpět) a zkontrolovat, že kabel nikde nedře, nenapíná se a nedotýká se tyče se závažím.

**Umístění v mrazáku (vnitřní 59 × 39 × 41 cm):**

- Sestava stojí přímo na dně na volně položeném pryžovém pásu 3 mm (nic se nelepí). Nemá stavitelné nohy, nerovnost se vyrovná podložkami.
- Box s RPi je na vnější straně pravého sloupu (+x), sestava je uprostřed šířky (výkres V05).
- Výška je 383 mm ve fázi 1 a 400 mm ve fázi 2. **Ve fázi 2 zbývá k víku jen ≈ 10 mm.** Před prvním zavřením zkontrolovat, že víko nic netlačí, hlavně těsnění a výstupek víka.
- Kabely vést po stranách, ne přes sestavu.

**Příprava vzorku:** hutnit po vrstvách 20 mm jako v kap. 2. Poslední vrstvu srovnat **stěrkou P10u** (rovná příčka leží na čele cely – povrch písku = čelo) otáčením kolem osy. Povrch je pak přesně 5 mm pod čelem. Hlava je při tom otočená na stranu +y, mimo práci.

**Zapojení – Raspberry Pi Zero 2 WH se svorkovnicovým HATem (vše šroubovací svorky nebo kabely Dupont, nic se nepájí):**

| co | GPIO → svorka HAT | poznámka |
|---|---|---|
| motor 28BYJ-48 (konektor do desky ULN2003) | IN1–IN4 = GPIO5, 6, 13, 19 | deska ULN2003: 5 V a GND ze svorek HATu |
| optická koncovka (P21) | GPIO26 | 3,3 V, GND; clona náboje = výchozí poloha |
| LED modul 3 W (3 piny) | GPIO27 | 5 V, GND; modul má vlastní spínací tranzistor |
| relé 1 – laser | GPIO17 | kontakt relé spíná + laseru (5 V); vodiče laseru prodloužené svorkami WAGO |
| relé 2 – topení hlavy | GPIO23 | kontakt relé spíná topné tělísko PTC 5 V; termostat v programu (5 … 8 °C) |
| teploměr DS18B20 (modul / sonda s kabelem) | GPIO4 (1-Wire) | 3,3 V, GND; v config.txt `dtoverlay=w1-gpio` |
| spouštění snímku z CR850 | C4 → modul optočlenu → GPIO22 | jako dosud |
| spojení s počítačem | adaptér USB-Ethernet + plochý kabel přes těsnění víka | webová stránka `http://e7-kamera:8080` nebo SSH |
| napájení | powerbanka ≈ 100 Wh mimo mrazák → USB kabel přes těsnění | ≥ 24 h bez sítě (§25) |

**Řízení – vše z počítače:** motor, LED, laser, topení i kameru řídí **Raspberry Pi Zero 2 W** (podle výrobce funguje od −20 °C) programem `rpi/e7_kamera.py`. Na počítači stačí otevřít v prohlížeči jeho webovou stránku (tlačítka *Výchozí poloha, Sada laser + LED, Oběh, Test*, teplota hlavy, poslední snímek) nebo se připojit přes SSH; CR850 se obsluhuje jako dosud z LoggerNetu. Arduino není potřeba: poloha se počítá v krocích, takže na přesném časování nezáleží, a jeden program pak sám otočí, počká, rozsvítí a vyfotí. Příkazy: `test`, `home`, `laser`, `orbit [krok]`, `run` (trvalý běh: puls z CR850 = sada snímků ve výchozí poloze, oběh v nastavených časech). Cíl se vždy najíždí ve stejném směru (vůle převodovky), po pohybu se cívky vypnou, poslední poloha se ukládá do `~/e7/stav.json`.

**Snímání:**

- **Průběžně** (spuštění z CR850, interval 10 min, kolem 0 °C 1 min) – hlava stojí ve **výchozí poloze**. Pořizují se tři snímky s pevnou expozicí a pevným zaostřením (autofokus jednou nastavit a uzamknout, `LensPosition`):
  1. s LED – fotka povrchu;
  2. s laserem bez LED – čáry pro výšku;
  3. bez světla – pozadí.
- **Oběh pro 3D model** – v klíčových stavech: před zmrazením, na konci −10 °C, po roztátí, konec cyklu; podle potřeby i každý cyklus.
  1. Najet na výchozí polohu (optická koncovka) vždy ze stejné strany.
  2. Otočit na −180°.
  3. Po 10° až do +170° pořídit 36 snímků s LED, každý s úhlem v názvu souboru.
  4. Vrátit se do výchozí polohy.
  - Trvá ≈ 1,5 min; laser je při oběhu vypnutý.
- **Výška z laseru** se počítá ve výchozí poloze **vůči čarám na rovném čele cely a na invarovém terčíku** v témže snímku. Malá nepřesnost návratu ramene (≈ 0,1°) se tím vyruší.

**Slepá zkouška S0 (povinná):** místo písku hliníková atrapa ⌀99 × 100 se stejným čelem, 2 celé cykly −20 / +20 °C (nejhorší případ) a −10 / +10 °C.

- Z ní se zjistí, o kolik se „pohne“ povrch jen teplotou (dno cely a podložky ≈ 70 µm na 20 K). V měřené řadě se to pak odečítá podle teploty dna (NTC).
- Posun rámu (≈ 140 µm na 20 K) ukazuje terčík P03 a odečítá se průběžně.
- **Ve S0 se zkouší i oběh při −10 °C:** rozjezd motoru, kabel, rosa na okénku při přechodu na +10 °C.

**Vyhodnocení fáze 1:**

- zdvih při mrznutí a sednutí při tání po celé ploše (mapa 11 profilů);
- průměr, rozdíl střed × okraj u stěny a zbytková deformace po cyklu;
- z oběhů 3D model povrchu (fotogrammetrie, měřítko ze značek ArUco na čele cely) a jejich rozdíly mezi stavy;
- fotky povrchu z každého cyklu.

Ve fázi 2 se stejný postup opakuje s pístem (zatížená × volná část) a se sublimací (kap. 9). **Oběh funguje i ve fázi 2**: hlava obíhá kolem tyče se závažím. Tyč a píst zakryjí z každé polohy jen malou část mezikruží. Laser na invarový terčík ve fázi 2 nedosvítí, posun rámu hlídá LVDT.
