# E7 – porovnání se zdroji o tlaku od zvedání mrazem (20. 11. 2026)

Zdroje: HBK C9C (siloměr), Hoekstra et al. 1965 (siloměr na horní desce), TML KDE-PA/KDF-PA a Kyowa BEC-A (tlaková čidla do zeminy), Domaschuk 1982, CPC4 s. 487 (tlaky naměřené na ocelových prvcích).

**Omezení:** stránky výrobců ani PDF nešly v tomto prostředí otevřít (síťová politika). Údaje jsou z výsledků vyhledávání – z výňatků katalogových listů a z citací. Čísla označená ⚠ je třeba ověřit v originálu.

## 1 · Hlavní rozdíl: co se měří

| | zdroje (Hoekstra, Domaschuk) | E7 dnes (fáze 1 a 2) |
|---|---|---|
| typ zkoušky | **zvedání je zabráněno** (pevné omezení), měří se **síla / tlak** | zvedání je **volné pod stálou zátěží** (závaží), měří se **posun** |
| čidlo | siloměr nad vzorkem, tlaková čidla v zemině | laser + kamera (povrch), LVDT (píst) |
| zemina | prachy a jíly (namrzavé), často s přísunem vody | písek, uzavřená cela bez přísunu vody |
| hlavní téma | tlak na konstrukce | sublimace pod „kamenem“, zdvih a sednutí při mrznutí a tání |

Obě metody se doplňují. Tlak při zabráněném zvedání je ale jiná veličina: závisí na **tuhosti omezení** (Hoekstra 1965, Ji et al. 2019). Ve stávajícím uspořádání E7 se nedá změřit „mimochodem“.

Repozitář už jednou variantu s pevným omezením obsahoval (A-min a A-rám, `vypocty.md` §9–10, README). Byly v ní miniaturní tlaková čidla TML PDA-PA 500 kPa a vložka z POM-C proti teplotní roztažnosti. Od té varianty se ustoupilo ve prospěch sublimace.

## 2 · Co říkají zdroje

- **Hoekstra, Chamberlain & Frate (1965)** – *Frost-heaving pressures*, CRREL RR 176 = Highway Research Record 101, s. 28–38:
  - válcový vzorek v laboratoři, tlak od zvedání měřený nad vzorkem, současně tlak vody v pórech;
  - maximální tlak odliší namrzavé zeminy od nenamrzavých;
  - lepším ukazatelem namrzavosti je velikost pórů než zrnitost;
  - plný text nebyl dostupný. Přehledová literatura uvádí v jílu až 213 psi ≈ 1,5 MPa ⚠.
- **Domaschuk (1982)** – *Frost heave forces on embedded structural units*, 4th Canadian Permafrost Conference, s. 487–496:
  - velké modelové zkoušky v prachu, ocelové prvky svislé, vodorovné a šikmé (45°);
  - rychlost postupu mrazu 4–75 mm (za den ⚠);
  - **tlak pod prvkem 1 900–2 500 kPa, mezní hodnota nebyla dosažena**.
  - Pro srovnání (jiná zpráva CRREL): H-pilota v prachu ve Fairbanksu dostala 752–802 kN za zimu.
- **Písek:** čistý písek nevytváří ledové čočky, takže velký tlak od zvedání nevzniká. Tlak vzniká jen z 9% zvětšení objemu vody při zamrznutí, a to jen když voda nemůže uniknout (nasycený uzavřený vzorek). Při Sr 0,5 (série S5) se led rozšíří do vzduchových pórů a tlak bude zanedbatelný. Zdroje to přímo neměří, je to obecně známé chování, ale pro E7 je to podstatné.

## 3 · Čidla – parametry a vhodnost pro E7

| | **HBK C9C** (siloměr) | **TML KDE-PA / KDF-PA** | **Kyowa BEC-A** |
|---|---|---|---|
| co měří | tlakovou sílu | tlak v zemině / na stěně | tlak v zemině |
| rozsahy | 50 N – 50 kN | 200 kPa, 500 kPa, 1 MPa, 2 MPa | 200 kPa, 500 kPa, 1 MPa |
| rozměr | ⌀26 × 13 mm (0,5–20 kN) | ⌀50, citlivá plocha ⌀46 | ⌀30, citlivá plocha ⌀23 (některé zdroje ⌀27 ⚠) |
| přesnost | třída 0,2 | nelinearita 2 % rozsahu | nelinearita ±2 % rozsahu |
| teplota | jmenovitá −10…+70 °C, provozní −30…+85 °C; u 50–200 N jmenovitá −10…+50, provozní −20…+60 °C | −20…+60 °C | nenalezeno ⚠ |
| výstup | mV/V (plný můstek), volitelně 0–10 V, 4–20 mA, IO-Link; IP67 | ≈ 0,3–0,5 mV/V (zdroje se liší ⚠), nerez, IP68 | mV/V |
| dodavatel v ČR | ✓ **HBP měřicí technika s.r.o., Praha 4** (výhradní zástupce HBM) | ✗ nenalezen (Althen DE, Elkome FI) | ✗ nenalezen (ZSE DE, Slentech AU) |

**Převod na E7:** píst ⌀50 má plochu 1 963 mm².

| tlak | 100 kPa | 500 kPa | 1 MPa | 2,5 MPa (Domaschuk) |
|---|---|---|---|---|
| síla na píst | 196 N | 982 N | 1,96 kN | 4,9 kN |

- **C9C:** jediné čidlo ze seznamu, které se do E7 hodí.
  - Malé a přesné: verze 1 kN dává ±2 N, tj. ±1 kPa.
  - Má českého zástupce.
  - Jde přímo do CR850 jako plný můstek (ověřit volný diferenciální vstup).
  - Při −20 °C je mimo jmenovitý, ale v provozním rozsahu, takže nulu je nutné kalibrovat ve slepé zkoušce.
  - Verze 50–200 N mají provozní rozsah jen od −20 °C, proto zvolit 0,5 kN a výš.
- **TML KDE/KDF:** ⌀50 je polovina průměru vzorku. Ocelové tělo by vedlo teplo a měnilo mrznutí. Přesnost ±4 kPa (2 % z 200 kPa) je víc, než je celé zatížení v E7 (2,5–25 kPa). Navíc nemá českého dodavatele. **Nehodí se.**
- **Kyowa BEC-A:** ⌀30 by šlo zapustit do dna cely nebo do čela pístu. Má ale stejně hrubou přesnost (±2 % z ≥ 200 kPa) a nemá českého dodavatele. **Jen jako doplněk**, například pro tlak u dna, z něhož lze odhadnout tření na stěně.

## 4 · Kdyby se E7 rozšířil o tlak od zvedání (varianta „R“)

**Uspořádání:** místo kotoučů C9C mezi horní čelo vodicí tyče a můstek přišroubovaný na horní příčník T04.
- Vejde se: můstek 6 mm + C9C 13 mm je nižší než kotouče se závažím.
- Předpětí šroubem asi na 5 kPa.
- Stávající LVDT současně měří, o kolik se píst pohnul, takže ke každému tlaku je známá tuhost omezení. Takto to doporučuje Ji et al. (2019).

**Problémy, které by bylo nutné vyřešit:**

1. **Teplotní roztažnost rámu.**
   - Rám se při mrznutí a tání (S5) pohne asi o 255 µm na 40 K (§25).
   - Při pevném omezení se tento posun změní v sílu. Odhad z §10: zmrzlý vzorek ≈ 16 kN/mm, falešná síla tedy řádově kN. To je víc, než písek sám vyvine.
   - Řešení: kompenzační vložka jako ve variantě A-rám, nebo slepá zkouška s hliníkovou atrapou ve stejném teplotním programu.
   - Při sublimaci se teplota nemění (−10 °C), takže tam problém není.
2. **Spoje rámu.** Úhelníky na T-maticích mohou při síle nad ≈ 1 kN prokluzovat ⚠. Pro tlakovou variantu by bylo potřeba sloupy připojit šrouby do čela profilu, jako ve variantě A-rám.
3. **Zemina.**
   - Nasycený písek v uzavřené cele: tlak může vzniknout a zatíží tištěnou celu.
   - Písek se Sr 0,5: téměř nulový tlak.
   - Tlaky ze zdrojů (MPa) se týkají namrzavých prachů s přísunem vody, což je jiný experiment (dno s přívodem vody, prach místo písku).

## 5 · Doporučení

1. **Pro E7, jak je navržen (sublimace + zdvih pod stálou zátěží), siloměr ani tlaková čidla nepotřebujete.** Zatížení dává závaží a jeho tíha je známá přesně. Zdroje se týkají jiné úlohy.
2. **Pokud chcete měřit i tlak od zvedání:** C9C 1 kN (do ≈ 500 kPa), nebo 2 kN (do ≈ 1 MPa), od HBP Praha, v samostatné sérii „R“. K tomu zpevnit spoje rámu a udělat slepou zkoušku s hliníkovou atrapou. Tlaková čidla TML a Kyowa nedoporučuji: jsou velká a hrubá na vzorek ⌀100 a nemají českého dodavatele.
3. Smysluplné hodnoty tlaku dá spíš namrzavý prach s přísunem vody než písek.

## Zdroje

- [HBK – C9C, stránka produktu](https://www.hbkworld.com/en/products/transducers/force/c9c/p-K-C9C) a [katalogový list B03868](https://assets.hbkworld.com/adobe/assets/deliver/urn:aaid:aem:3d9e3ed6-a31d-44c5-87a2-8506092c5641/C9C-Data-Sheet-B03868.pdf); [HBM C9C, návod k montáži](https://www.manualslib.com/manual/2953469/Hbm-C9c.html)
- [HBK – kontakt Česká republika (HBP měřicí technika)](https://hbkworld.com/en/contact-us/global-presence/hbm-worldwide-contacts/contact-europe/contact-czech-republic)
- [Hoekstra, Chamberlain & Frate 1965 – TRB HRR 101](https://onlinepubs.trb.org/Onlinepubs/hrr/1965/101/101-003.pdf); [záznam DTIC AD0626175](https://openpolar.no/Record/ftdtic:AD0626175/Description); [Phenomenon and Mechanism of Frost Heaving (HRR 304)](https://onlinepubs.trb.org/Onlinepubs/hrr/1970/304/304-001.pdf)
- [TML KDE-PA/KDF-PA](https://tml.jp/e/node/376); [Althen – KDE-PA/KDF-PA](https://www.althensensors.com/sensors/pressure-sensors/general-purpose-pressure-sensors/kde-pak-df-pa-soil-pressure-gauge/); [Althen – katalogový list](https://www.althensensors.com/uploads/products/datasheets/kde-pa_kdf-pa_kdg-pa_kdh-pa_19042021.pdf)
- [Kyowa BEC-A (CAS)](https://casscale.net/products/kyowa-bec-a-soil-pressure-transducer/?lang=en); [Kyowa – BEC-A](https://product.kyowa-ei.com/en/products/soil-pressure-transducer/type-bec-a); [ZSE – BEC-A](https://www.zse.de/en/applications/construction-measurement-technology/wall-surface-and-soil-pressure-transducer/bec-a-bed-a-small-sized-soil-pressure-transducer)
- [Domaschuk 1982, CPC4 s. 487](https://pubs.aina.ucalgary.ca/cpc/CPC4-487.pdf); [CRREL – Measurement of Frost Heave Forces on H-Piles and Pipe Piles](https://apps.dtic.mil/sti/tr/pdf/ADA205010.pdf)
