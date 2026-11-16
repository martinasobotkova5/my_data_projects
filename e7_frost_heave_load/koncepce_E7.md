# E7 – koncepce: sublimace ledu z písku pod kamenem a vznik podstavce

Laboratorní experiment ČVUT FSv, 11/2026. Podrobnosti: sestava a výkresy `vykresy/E7_drawings.pdf`, výpočty
`vypocty.md` (§17–21), postup `postup_zkousky.md` (kap. 9), rešerše `reserse_novost.md`.

## 1 · Cíl

Změřit v laboratoři, jak **kámen nebo stavba na povrchu zmrzlé zeminy chrání led v ní před sublimací** (přeměnou ledu
přímo v páru) a jak rychle kolem nich **klesá volný povrch** – tedy jak vzniká „podstavec“. Měří se současně krytá
a volná část povrchu jednoho vzorku písku s ledem, s rozlišením na mikrometry, v suchém mrazivém vzduchu
a s krátkými táními podle antarktické lokality.

## 2 · Proč

- V Antarktidě a na Marsu ubývá ledu ze země hlavně sublimací; povrch se snižuje, mění se polygonální půdy a pod kameny
  se led drží déle. Dosud se to popisuje terénními pozorováními a modely (Victoria Valley ≈ 0,22 mm ledu za rok;
  permafrostový tunel u Fairbanks, 52 let).
- Laboratorní pokusy existují jen pro **čistý led s kotoučem** (podstavce „Zen stones“, PNAS 2021) a pro **led pod
  souvislou vrstvou regolitu** (komory pro Mars a Měsíc). **Zeminu s ledem s pevným krytem jen na části povrchu,
  se zatížením a s táním, měřenou na µm, jsem nenašla** (orientační rešerše, ověřit ve Scopusu / WoS).

## 3 · Hypotézy

| | hypotéza | jak se ověří |
|---|---|---|
| H1 | Pod krytem led nesublimuje; volný povrch písku s **přebytkem ledu** klesá a vzniká podstavec, jehož výška roste s odmocninou času (difuze páry suchou vrstvou). | laser (mezikruží) − LVDT (píst), řez na konci, √t |
| H2 | U **pórového ledu** (bez přebytku) povrch neklesá – vznikne jen suchá vrstva, kostra zrn stojí. | kontrolní vzorek A |
| H3 | Zatížení krytu (3,5 → 25 kPa) výšku podstavce mění jen málo (tečení ledu řádově µm); rozhoduje zakrytí. | dvě série se stejným vzorkem B |
| H4 | Krátká tání podstavec částečně „rozmažou“ (sesuv suchého písku, sednutí při tání). | série s táním každých 7 dní |

## 4 · Program zkoušek

| série | vzorek | podmínky | délka | co dá |
|---|---|---|---|---|
| S0 slepá zkouška | hliníková atrapa | celý teplotní cyklus | 2 dny | drift sestavy, kalibrace kamery |
| S1 předzkouška | miska ledu + miska písku s ledem na váze | −10 °C, silikagel, ventilátor | 2–3 dny | rychlost sublimace vs. RH → délka sérií |
| S2 kontrola | **A – pórový led** (Sr ≈ 1) | −10 °C, suchý vzduch, píst 3,5 kPa | 14–30 dní | H2 |
| S3 hlavní | **B – přebytek ledu** (≈ 60 % ledu) | −10 °C, suchý vzduch, píst **3,5** a **25 kPa** | 14–30 dní | H1, H3 |
| S4 s táním | B | jako S3 + každých 7 dní 6 h při +5 °C (podle Ostrova Jamese Rosse) | 28 dní | H4 |
| S5 mrznutí a tání | nenasycený písek Sr 0,5 | 24 h −10 °C / 24 h +10 °C | 10 cyklů | zdvih a sednutí, zatížená × volná část |

## 5 · Co se měří

| veličina | přístroj | rozlišení |
|---|---|---|
| pokles volného povrchu (mezikruží ⌀100/⌀50) | laser 11 čar + kamera | ≈ 10 µm |
| pohyb krytu (pístu) | LVDT na invarovém sloupku | ≈ 1 µm |
| úbytek ledu (rychlost sublimace) | váha s miskou v mrazáku (HX711), vážení cely na začátku a konci | 0,01 g |
| vlhkost a teplota vzduchu | SHT45, Campbell 109 | 2 % RH, 0,2 °C |
| teplota písku a dna | Pt100, NTC | 0,1 °C |
| obsah vody / ledu | TDR CS645 | – |
| tloušťka suché vrstvy | řez vzorku na konci, ruční 3D model povrchu | 0,1 mm |

## 6 · Očekávané hodnoty (odhad, `vypocty.md` §21)

- čistý led v mrazáku s ventilátorem: **0,1–1,5 mm/den** (podle vlhkosti);
- suchá vrstva v písku: ≈ 2 mm za 2 dny, 5–6 mm za 14 dní, 7–9 mm za 30 dní;
- pokles volného povrchu u písku s přebytkem ledu: **≈ 1,8 mm za 14 dní** → laserem měřitelný den po dni;
- tečení ledu pod pístem 25 kPa: ≈ 1 µm za 30 dní.

## 7 · Vazba na terén

- Teplotní program krátkých tání a vlhkost písku podle polních dat z **CALM-S u Mendelovy stanice (Ostrov Jamese
  Rosse, Masarykova univerzita)**; ideálně i vzorek písku odtud.
- Laboratoř je rychlejší než příroda (suchý proudící vzduch); srovnává se **mechanismus** a poměr krytý / volný povrch,
  ne absolutní rychlost.
- Spolupráce: polární tým MU (teploty, vlhkost, vzorky), případně Svalbard (Jihočeská univerzita).

## 8 · Rizika

| riziko | opatření |
|---|---|
| sublimace v mrazáku příliš pomalá / rychlá | předzkouška S1, silikagel / ventilátor, délka série |
| námraza na stěnách mrazáku mění vlhkost | SHT45 průběžně, silikagel měnit (indikátor) |
| příprava písku s přebytkem ledu nerovnoměrná | vážit vrstvy, příprava celá v mrazáku, dva vzorky |
| laser na suchém / zmrzlém povrchu | pevná expozice, kalibrace podložkami v obou stavech |
| novost nepotvrzena | rešerše Scopus / WoS (dotazy `reserse_scopus_wos.md`) před podáním |

## 9 · Výstupy

Článek o mechanismu (např. *Permafrost and Periglacial Processes*, *Geophysical Research Letters*, pro srovnání
s Marsem *Icarus*) a technická poznámka o zařízení (*Geotechnical Testing Journal*).
