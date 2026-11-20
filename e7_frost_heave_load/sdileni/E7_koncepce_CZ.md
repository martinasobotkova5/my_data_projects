# E7 – koncepce: deformace písku při cyklech mrznutí a tání (revize 20. 11. 2026)

Laboratorní experiment ČVUT FSv. Podrobnosti:
- sestava a výkresy: `vykresy/` (V07 fáze 1, V08 fáze 2, V09 čidla ve vzorku);
- výpočty: `vypocty.md` (§22–26);
- postup: `postup_zkousky.md`;
- revize: `revize_E7.md`;
- rešerše: `reserse_novost.md`.

## 1 · Cíl

Během **cyklů mrznutí a tání** měřit **deformaci a posun** vzorku písku ⌀100 × 100 mm v mrazáku (−20 až +20 °C). Kromě celkového zdvihu a sednutí měřit i **celé pole posunů povrchu** s rozlišením desítek µm. Současně měřit:
- **teplotní profil** (poloha čela mrznutí);
- **nezamrzlou vodu** (TDR).

Ve fázi 2 se na části povrchu přidá zatížený píst („kámen“), takže se v jednom vzorku porovná zatížená a volná část.

## 2 · Co je nové (ověřit rešerší ve Scopusu / WoS, `reserse_scopus_wos.md`)

1. **Celé 3D pole posunů povrchu během cyklů**, ne jen jeden bod.
   - Kamera obíhá kolem vzorku přímo v mrazáku: 36 pohledů, 2 polohy ostření.
   - K tomu laser s 11 čarami.
   - Výsledkem jsou výškové mapy a fotogrammetrie / 3D-DIC povrchu, tedy svislý i vodorovný posun zrn.
   - Běžné zkoušky (např. ASTM D5918) měří zdvih jedním snímačem.
2. **Synchronní teplotní profil a nezamrzlá voda v jednom vzorku.**
   - 5 teplotních sond, dno, vzduch a bod M (TDR + Pt100 + optické vlákno) uspořádaný stejně jako v terénu.
   - Okamžitý zdvih se dá přiřadit poloze čela mrznutí a obsahu nezamrzlé vody.
   - Lze tak přímo srovnat laboratoř s polními daty CALM-S (Ostrov Jamese Rosse).
3. **Zatížená a volná část povrchu ve stejném vzorku.** Píst ⌀50 na mezikruží ⌀100 dává rozdílný zdvih a sednutí bez rozptylu mezi vzorky (fáze 2).
4. **Kumulace deformace (ratcheting) přes ≥ 10 cyklů** s rozlišením µm až desítek µm a slepou zkouškou na teplotní drift sestavy.
5. **Levné a otevřené zařízení.**
   - Raspberry Pi, 3D tisk, T-profily.
   - Nic se nepájí ani nelepí, vše se ovládá z počítače.
   - Popis zařízení může vyjít jako technická poznámka.

## 3 · Hypotézy

| | hypotéza | jak se ověří |
|---|---|---|
| H1 | Zdvih při mrznutí roste se stupněm nasycení. Pod Sr ≈ 0,8 se led vejde do pórů a zdvih je malý. Při Sr → 1 v uzavřené cele roste až k ≈ 3 % zmrzlé tloušťky. | série F1, F2 – laser, kamera |
| H2 | Po každém tání zůstane trvalé sednutí. Přes cykly se kumuluje a nejvíc je ho u povrchu. | F1–F3, pole posunů, řez na konci |
| H3 | Zatížená část (píst) se zvedá méně a sedá víc než volná, rozdíl roste s přitížením. | F3 – LVDT × laser na mezikruží |
| H4 | Zdvih probíhá, dokud postupuje čelo mrznutí (0 °C v profilu), a jeho rychlost odpovídá poklesu nezamrzlé vody (TDR). | profil T1–T5, TDR, časová řada zdvihu |

## 4 · Program zkoušek

| série | vzorek | teplotní program | délka | co dá |
|---|---|---|---|---|
| S0 slepá zkouška | hliníková atrapa ⌀99 × 100 | 2 cykly −20/+20 °C a 2 cykly −10/+10 °C | 8 dní | teplotní drift sestavy, kalibrace kamery a laseru |
| F1 | písek Sr 0,5, bez zátěže (fáze 1) | 24 h −10 °C / 24 h +10 °C | 10 cyklů | základní zdvih a sednutí, H2 |
| F2 | písek Sr ≈ 0,9–1,0, bez zátěže | jako F1 | 10 cyklů | H1, H4 (největší deformace) |
| F3 | jako F2, píst 2,5 kPa a 25 kPa (fáze 2) | jako F1 | 2 × 10 cyklů | H3 |
| F4 | Sr podle terénu | denní cykly podle CALM-S (např. −5/+5 °C) | 14 dní | krátké mělké cykly jako v létě v Antarktidě |
| S (volitelně) | písek s přebytkem ledu, píst | −10 °C, suchý vzduch | 14–30 dní | sublimace pod „kamenem“ (původní série, `postup_zkousky.md` kap. 9) |

## 5 · Co se měří

| veličina | přístroj | interval | rozlišení |
|---|---|---|---|
| výška povrchu (mapa) | laser 11 čar + kamera ve výchozí poloze | 10 min | ≈ 11–23 µm |
| 3D pole posunů povrchu | oběh kamery 36 pohledů × 2 ostření (Camera Module 3 Wide) | 3 h + na konci každé fáze | desítky µm |
| posun pístu (fáze 2) | LVDT na invarovém sloupku | 1 min | ≈ 1 µm |
| posun rámu | invarový terčík P03 v každém snímku | 10 min | ≈ 10 µm |
| teplotní profil | 5× DS18B20 (10, 30, 50, 70, 90 mm) na RPi | 1 min | 0,06 °C (po kalibraci v ledové lázni ±0,1 °C) |
| teplota v bodě M, dno, vzduch | Pt100 (CR850), NTC ve dně, Campbell 109 | 1 min | 0,1 °C |
| nezamrzlá voda | TDR CS645 v bodě M (hloubka 45 mm) | 10–30 min | – |
| celkový úbytek vody | vážení cely na začátku a konci | – | 0,01 g |
| vnitřní deformace (na konci) | řez zmrzlým vzorkem, tenké barevné vrstvy písku po 20 mm | 1× | 0,1 mm |

## 6 · Očekávané hodnoty (odhad)

- **Sr 0,5:** led se vejde do pórů, zdvih jen desítky µm. Horní mez (veškeré rozšíření nahoru) je 9 % × θ × 100 mm ≈ 1,7 mm. Sednutí po tání bude desítky µm za cyklus a s cykly klesá.
- **Sr ≈ 1:** zdvih až ≈ 3 % zmrzlé tloušťky, tj. ≈ 1–3 mm. Laser i kamera to změří snadno.
- Vzorek zmrzne a roztaje za ≈ 9 h, takže 24 h na každou fázi stačí (README, model tání).

## 7 · Vazba na terén

- Teplotní program a vlhkost písku podle polních dat z **CALM-S u Mendelovy stanice** (Ostrov Jamese Rosse, Masarykova univerzita), ideálně i vzorek písku odtud.
- Bod M (TDR + Pt100 + optické vlákno) je uspořádaný stejně jako v terénu, takže lze přímo srovnat laboratorní a polní záznamy.

## 8 · Rizika

| riziko | opatření |
|---|---|
| teplotní drift rámu (Al) je srovnatelný se zdvihem při Sr 0,5 | invarový terčík v každém snímku, slepá zkouška S0, NTC ve dně |
| rosa nebo námraza na okénku kamery při tání | vyhřívaná hlava (5–8 °C), ventilátor, snímky s LED kontrolují ostrost |
| nasycený vzorek v uzavřené cele vytlačí vodu otvory čidel | vývodky M12, perimetry kolem otvorů; u F2 kontrolovat hmotnost |
| hloubka ostrosti kamery zblízka | Camera Module 3 Wide a 2 polohy ostření (`vypocty.md` §23) |
| novost nepotvrzena | rešerše Scopus / WoS před podáním |

## 9 · Výstupy

- Článek o deformaci písku při cyklech mrznutí a tání s plným polem posunů, například do časopisu *Permafrost and Periglacial Processes* nebo *Cold Regions Science and Technology*.
- Technická poznámka o zařízení do *Geotechnical Testing Journal*.
