# E7 – dodavatelé a objednávka (jen české firmy, nic se nepájí ani nelepí)

Stav 19. 11. 2026. Ceny jsou orientační, většinou bez DPH, a je potřeba je před objednáním potvrdit. Výpočty jsou ve `vypocty.md` (§24 mrazák, §25 kontrola zadání), postup v `postup_zkousky.md` (kap. 7 a 10). Výkresy: V05 (sestava v mrazáku), V07 (fáze 1), V08 (fáze 2), nářezové výkresy `vyroba/narezy/`.

## Kontrola zadání

| # | požadavek | jak je splněn | stav |
|---|---|---|---|
| 1 | nic nepájet, nelepit | <ul><li>elektronika: moduly s piny, kabely Dupont, šroubovací svorky, svorky WAGO</li><li>pouzdro igus a ložiska: zalisovat</li><li>píst: 3× M3 místo epoxidu</li><li>dutina cely: vodotěsný tisk bez nátěru</li><li>terčík: tisk z bílého PETG</li><li>LED a topení: přišroubované</li><li>výchozí poloha: optická koncovka místo lepeného magnetu</li><li>pryžový pás: volně položený</li></ul> | ✓ |
| 2 | vše šroubovat a jednoduše propojit | <ul><li>rám z T-profilů na T-matice</li><li>díly na M3–M6</li><li>kotouče na závitový čep M6 s maticí</li><li>cela se vystředí dorazy P20</li><li>elektronika v šroubovacích svorkách</li></ul> | ✓ |
| 3 | ovládat jen z počítače | <ul><li>Raspberry Pi Zero 2 W: webová stránka s tlačítky + SSH přes kabel Ethernet; ovládá motor, LED, laser, topení, teploměr a kameru</li><li>CR850 z LoggerNetu</li></ul> | ✓ (regulátor mrazáku viz níže) |
| 4 | závaží vedené, nechvěje se, nenaklání | <ul><li>tyč vedená nahoře pouzdrem igus, dole důlkem na kuličce (rozteč ≈ 90 mm, náklon ≤ 0,04°)</li><li>kotouče na čepu M6 stažené maticí</li></ul> | ✓ (§25) |
| 5 | konstrukce se nepřeklopí | <ul><li>převrhne se až při náklonu ≈ 32° nebo vodorovné síle ≈ 51 N na horní hranu</li><li>stojí celou délkou podélníků</li></ul> | ✓ (§25) |
| 6 | teplotně se neroztahuje | <ul><li>vodicí tyč a sloupek LVDT z Invaru (7 a 14 µm na 40 K)</li><li>posun rámu (255 µm) se odečte z invarového terčíku v každém snímku</li><li>cela a podložky (95 µm) ze slepé zkoušky</li></ul> | ✓ (§25) |
| 7 | váleček vnitřní ⌀100, výška 100 | dutina cely přesně ⌀100 × 100; povrch písku = čelo cely (srovná se pravítkem P10u); stejná cela pro obě fáze | ✓ |
| 8 | jen čeští dodavatelé | <ul><li>vše z českých firem a e-shopů</li><li>LVDT: česká pobočka Micro-Epsilon</li><li>laser 11 čar: český dodavatel nenalezen</li></ul> | **⚠ laser** |

**Otevřené body:**

- **Laser s 11 čarami nemá českého dodavatele.** Možnosti:
  - Picotronic (Německo) – nabídka A2627918 už je;
  - TME – polská firma, prodává do ČR;
  - laser-shop.cz (CZ) – jen jednočárové lasery, tři kusy by daly tři profily místo jedenácti.
- **Regulátor mrazáku:** pokud ho nelze ovládat z počítače, může teplotní program řídit CR850 přes relé SSR se šroubovacími svorkami.

## Fáze 1 – bez zatížení

| firma (CZ) | položky | ks | cena (odhad) |
|---|---|---|---|
| **ENPRAG, s.r.o., Praha** – [enprag.cz](https://www.enprag.cz/hlinikove-profily/c-6027) | <ul><li>profily 40×80 drážka 8: T01 2× 276, T03 260, T04 340 s otvorem ⌀14</li><li>profily 40×40: T02 2× 320</li><li>14 úhelníků 40×40 drážka 8 s krytkou</li><li>28 T-matic M8 a 20 T-matic M5 (vkládací)</li><li>28 šroubů M8×16 s podložkou</li><li>krytky čel 4× 40×40, 2× 40×80</li></ul><br>Poslat `E7_narezy_profily_ENPRAG.pdf` – obsahuje nářezový plán N01 a rozpis spojů N04. | sada | ≈ 4 000–6 000 Kč |
| **Kovohutě Rokycany** – sales@koro.cz | <ul><li>Invar 36 ⌀16 × 283 (B02, sloupek)</li><li>Invar 36 ⌀12 h9 × 150 (B01, vodicí tyč, pro fázi 2): nahoře závit M6 hl. 15, dole středicí důlek 90° ⌀8</li></ul><br>Poslat `E7_narezy_invar_Rokycany.pdf`. | 1 + 1 | ≈ 2 000–4 000 Kč |
| **Elektroizolanty Praha** – [elektroizolanty.cz](https://www.elektroizolanty.cz/) | tyč G10 ⌀20, nařezat 3× 20 mm | 1 | ≈ 300 Kč |
| **HENNLICH s.r.o., Litoměřice** (igus) | kluzné pouzdro igus drylin RJ4JP-01-12 (zalisuje se do jádra oběhu) | 1 | ≈ 50–120 Kč |
| **Prusa Research, Praha** | <ul><li>Prusament PETG-CF 2 kg (cela ⌀220 × 146 a díly)</li><li>Prusament PETG bílý 0,25–1 kg (terčík P03)</li></ul> | 2 + 1 | ≈ 3 000 Kč |
| **RPishop.cz, České Budějovice** | <ul><li>Raspberry Pi **Zero 2 WH** (s osazenou lištou – nepájí se)</li><li>Camera Module 3 (standardní)</li><li>kabel kamery Mini–Standard 500 mm</li><li>microSD 32 GB</li><li>adaptér micro-USB → Ethernet</li><li>svorkovnicový HAT pro GPIO (šroubovací svorky)</li></ul> | sada | ≈ 2 000–2 500 Kč |
| **LaskaKit / GM electronic** (CZ) | <ul><li>krokový motor 28BYJ-48 + deska ULN2003</li><li>optická vidlicová koncovka (modul pro 3D tiskárny)</li><li>modul relé 2 kanály (3,3 V)</li><li>modul výkonové LED 3 W s řídicím pinem</li><li>teploměr DS18B20 (sonda s kabelem + modul)</li><li>modul optočlenu (spouštění z CR850)</li><li>topné tělísko PTC 5 V ≈ 2–3 W s otvory</li><li>kabely Dupont</li><li>svorky WAGO 221</li><li>ventilátor 80 mm 12 V + zdroj</li></ul> | sada | ≈ 900–1 400 Kč |
| obchody s ložisky (CZ, např. výrobce ZKL) | ložisko 6806-2RS (30 × 42 × 7) | 2 | ≈ 100–250 Kč |
| **Fabory CZ / Hornbach** | <ul><li>sada šroubů M2, M3, M4, M5, M6 s maticemi a podložkami</li><li>závitový čep DIN 913 M6 × 45</li><li>tenká matice M6 DIN 439</li><li>pryžový pás 3 mm</li><li>deska XPS 20 mm, pěna 5 mm</li><li>stahovací pásky</li><li>PTFE sprej, silikonová vazelína</li><li>závitník M3</li></ul> | sada | ≈ 800–1 200 Kč |
| **Alza.cz** | <ul><li>powerbanka ≈ 100 Wh (26 800 mAh, USB-C PD, průchozí nabíjení) – stojí **mimo mrazák**</li><li>plochý kabel Ethernet 3 m</li></ul> | 1 | ≈ 1 500–2 500 Kč |
| **Ekotechnika, Černošice** (Campbell) | 4WPB100 (modul pro Pt100), 109-L (teplota vzduchu) | 1 + 1 | ≈ 5 300–8 500 Kč |
| **laser 11 čar** | ⚠ bez českého dodavatele – viz otevřené body; dnes Picotronic DOE253-635-5-6(10x24) | 1 | ≈ 2 900 Kč |

## Fáze 2 – zátěž a sublimace

| firma (CZ) | položky | ks | cena (odhad) |
|---|---|---|---|
| **grupol.cz** (laserové řezání podle DXF) | <ul><li>L03 nosná deska Al 6 mm</li><li>L04 a L05 píst Al 10 mm (L05 se 3 otvory pro závit M3)</li><li>4× L06 ⌀165 × 6 (1 kg)</li><li>L07 ⌀165 × 3 (0,5 kg)</li></ul> | sada | ≈ 1 500–3 000 Kč |
| **Micro-Epsilon Czech Republic, Bechyně** | LVDT ±10 mm s vestavěnou elektronikou (induSENSOR DTD-10G8, výstup 0–5 V do CR850, napájení 24 V) – poptat; svěrka P02 se upraví na jeho tělo | 1 | poptat |
| **GM electronic** | zdroj Mean Well HDR-15-24 (napájení LVDT, šroubovací svorky) | 1 | ≈ 300 Kč |
| **Fabory CZ / cyklo prodejna** | ocelová kulička 5/16" | 1 | ≈ 30 Kč |
| **LaskaKit / GM electronic** | <ul><li>tenzometr 1 kg + HX711 (verze se svorkami)</li><li>čidlo vlhkosti SHT45 s konektorem (bez pájení)</li></ul> | 1 + 1 | ≈ 500–900 Kč |
| **P-LAB / Verkon** (CZ, laboratorní potřeby) | skleněné misky ⌀90 (3 ks), síto 2 mm | sada | ≈ 400–800 Kč |
| **Hornbach** | silikagel s indikátorem 2 kg + tác | 1 | ≈ 400–700 Kč |

## Soubory pro firmy

| firma | soubory |
|---|---|
| ENPRAG | `vyroba/narezy/E7_narezy_profily_ENPRAG.pdf`, `poptavka_ramu.md` |
| HENNLICH (igus) | `poptavka_igus_HENNLICH.md` |
| Kovohutě Rokycany | `vyroba/narezy/E7_narezy_invar_Rokycany.pdf` (B01: závit M6 nahoře, důlek 90° dole), `poptavka_invar_Rokycany.md` |
| Elektroizolanty Praha | `vyroba/narezy/E7_narezy_G10_Elektroizolanty.pdf`, `poptavka_G10_Elektroizolanty.md` |
| Micro-Epsilon CZ | `poptavka_LVDT_MicroEpsilon.md`, `vykresy/E7-V08_se_zatezi.pdf` |
| grupol.cz | `vyroba/laser/*.dxf` |
| vlastní tisk | `vyroba/tisk/*.stl` – cela `E7-V03u_cell_D220x146_bez_zatizeni`, P02–P07, P10u, P12–P16, P18–P21 (P01, P08–P10 jsou ve složce `_nepouzivat`) |

## Ověřit před objednáním

- **Mrazák:** ve fázi 2 zbývá k víku ≈ 10 mm (s maticí na čepu). Před zavřením víka zkontrolovat.
- **Laser:** rozhodnout o dodavateli (viz otevřené body).
- **Regulátor mrazáku:** lze ho ovládat z počítače? Jinak řízení přes CR850 a relé SSR.
- **Elektronické moduly** (topné tělísko PTC 5 V, LED modul s řídicím pinem, svorkovnicový HAT pro Zero): ověřit skladovou dostupnost u LaskaKit, GM electronic a RPishop.
