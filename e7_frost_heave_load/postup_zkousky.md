# E7 – co může při měření zlobit a postup zkoušky (rev. B3, 11/2026)

Sestava: rám z T-profilů, cela ⌀240 tištěná vcelku na 3 podložkách G10, písek ⌀100 × 100 mm, Sr = 0,5,
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
| 12 | **CR850 má jen porty C1–C4** (C1–C3 bere TDR), LVDT na SE dává jen 2,7 µm | – | ✓ multiplexor AM16/32B: RES = C4, CLK = VX1; RPi fotí podle NTP; LVDT a ventilátor trvale napájené; LVDT **diferenciálně** (1,3 µm, průměr ≈ 0,5 µm), plán kanálů §18 |
| 16 | **Teplota dna cely a rámu se neměří** – korekce driftu ze slepé zkoušky by stála jen na teplotě písku | zbytkový drift větší než 6 µm | ✓ termistory na multiplexoru: dno a stěna cely, invarový sloupek, příčníky, vzduch u povrchu |
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
