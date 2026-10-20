# E6 – kontrolní výpočty

Generováno skriptem `src/vypocty.py` z `src/params.py`.

## 1. Kontrola čísel z původního schématu

| veličina | hodnota | jednotka | poznámka |
|---|---|---|---|
| plocha kolony ⌀100 | 78.54 | cm² |  |
| plocha disku ⌀45 | 15.90 | cm² |  |
| podíl disku na průřezu | 20.2 | % | schéma: 20,2 % ✔ |
| poměr ploch kolona : disk | 4.94 | – | schéma: 4,94 ✔ |
| šířka mezikruží | 27.5 | mm | schéma: 27,5 ✔ |
| objem zeminy ⌀100 × 100 | 785 | cm³ | schéma: 785 ✔ |
| objem kolony ⌀85 × 140 (GACR-01) | 794 | cm³ | schéma: „prakticky shodný“ ✔ (+1 %) |
| 1 mm hladiny v zásobníku ⌀31 → přes disk | 0.475 | mm | schéma: 0,475 ✔ |
| 1 mm hladiny → přes průřez kolony | 0.0961 | mm | schéma: 0,0961 ✔ |

## 2. Doba průniku – co přesně číslo 5–37 h znamená

| veličina | hodnota | jednotka | poznámka |
|---|---|---|---|
| Δθ = 0.05, q_disk = 2.0 mm/h | 12.3 | h | q přes průřez = 0.405 mm/h; jen zaplnění Δθ (čelo zvlhčení) |
| Δθ = 0.05, q_disk = 5.0 mm/h | 4.9 | h | q přes průřez = 1.012 mm/h; jen zaplnění Δθ (čelo zvlhčení) |
| Δθ = 0.15, q_disk = 2.0 mm/h | 37.0 | h | q přes průřez = 0.405 mm/h; jen zaplnění Δθ (čelo zvlhčení) |
| Δθ = 0.15, q_disk = 5.0 mm/h | 14.8 | h | q přes průřez = 1.012 mm/h; jen zaplnění Δθ (čelo zvlhčení) |
| objemový přítok (= odtok v ustáleném stavu) | 3.2–8.0 | ml/h |  |
| objem vody ve vzorku (kapalná + led), θ = 0,30 | 236 | ml | „pórový objem“ pro stopovač |
| objem pórů, n = 0,45 | 353 | ml |  |
| 1.0 PV odtoku | 30–74 | h | 236 ml |
| 1.5 PV odtoku | 44–111 | h | 353 ml |
| 2.0 PV odtoku | 59–148 | h | 471 ml |
| počet frakcí po 2 ml na 1,5 PV | 177 | – | schéma počítá ~60 |
| počet frakcí po 5 ml na 1,5 PV | 71 | – | schéma počítá ~60 |
| 60 frakcí pokryje | 120–300 | ml | = 0.51–1.27 PV |

## 3. Zásobník a měření přítoku

| veličina | hodnota | jednotka | poznámka |
|---|---|---|---|
| objem zásobníku ⌀31, sloupec 200 mm | 151 | ml |  |
| objem zásobníku ⌀31, sloupec 300 mm | 226 | ml |  |
| potřebná výška sloupce ⌀31 pro 1,5 PV | 468 | mm | → nutné doplňování / větší Mariottova láhev |
| pokles hladiny ⌀31 za hodinu | 4.2–10.5 | mm/h |  |
| 1 Pa ≙ | 0,10 | mm v. sl. | 0,1 mm ≙ 1 Pa = 0,01 % FS snímače 0–10 kPa |
| typická přesnost 0–10 kPa (0,1 % FS) | 10 | Pa | ≙ 1 mm v. sl., ne 0,1 mm |
| váha 0,01 g na Mariottově láhvi | 0,01 | ml | ≙ 0.0063 mm přes disk |

## 4. Tepelná bilance: na kolik vody stačí „chlad“ zeminy při −3 °C

| veličina | hodnota | jednotka | poznámka |
|---|---|---|---|
| citelný chlad vzorku −3 → 0 °C | 4.5 | kJ | C = 1,9 MJ m⁻³ K⁻¹ |
| tolik vody může znovu zamrznout | 13 | ml | = 6 % PV, = 8 mm přes disk |
| doba přítoku tohoto objemu | 1.7–4.2 | h | pak je vzorek izotermní při 0 °C s ledem |
| led ve vzorku při −3 °C | 181 | ml |  |
| teplo na roztátí veškerého ledu | 55 | kJ | ≫ citelný chlad → fáze „0 °C s ledem“ trvá dny, řídí ji okrajové toky tepla |
| citelné teplo vody +0,5 °C na 1 ml | 2.1 | J | vs. 334 J/ml latentní – zanedbatelné |

## 5. Spodní okrajová podmínka

| veličina | hodnota | jednotka | poznámka |
|---|---|---|---|
| vstup vzduchu membrány 20 µm (Young–Laplace, θ = 0°) | ≈ 148 | cm | horní mez; skutečná bývá nižší → ověřit bublinkovým testem |
| vstup vzduchu membrány 50 µm (Young–Laplace, θ = 0°) | ≈ 59 | cm | horní mez; skutečná bývá nižší → ověřit bublinkovým testem |
| objem drážek pod membránou | 1.13 | ml |  |
| osový vývrt kuželem ⌀1,5 | 0.12 | ml |  |
| hadička PTFE ID 0,8 × 600 mm | 0.30 | ml |  |
| mrtvý objem celkem | 1.8 | ml | + ~0,3 ml podložka; < 1 frakce |
| pro srovnání: vnitřní objem duté nálevky ⌀100 × 46 (původní) | 120 | cm³ | otevřený výtok = seepage face, h = 0 |
| varianta B: vnitřní zóna ⌀50 / mezikruží | 19.6 / 58.9 | cm² | poměr ploch 1 : 3 |

## 6. Izotopy – rozlišitelnost značky

| veličina | hodnota | jednotka | poznámka |
|---|---|---|---|
| frakcionace led–voda δ²H | ≈ +20 | ‰ | α ≈ 1,0195–1,0212 |
| frakcionace led–voda δ¹⁸O | ≈ +3 | ‰ | α ≈ 1,0029–1,0031 |
| značka δ²H = +200 ‰ vs. pozadí −70 ‰ | 7 | % signálu | posun δ²H frakcionací vyjádřený v podílu značky |
| značka δ²H = +500 ‰ vs. pozadí −70 ‰ | 4 | % signálu | posun δ²H frakcionací vyjádřený v podílu značky |
| přesnost OA-ICOS δ²H | 0,5 | ‰ | ≙ 0.19–0.09 % podílu značky |
