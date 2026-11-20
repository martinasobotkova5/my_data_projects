# E7 – revize návrhu 20. 11. 2026

**Zadání revize:**
- Mrazák má vnitřní rozměry 59 × 39 × 41 cm (délka × šířka × výška).
- Vše má sedět, nic nesmí chybět, vše se musí dát smontovat bez pájení a lepení.
- Kamera má fungovat v mrazáku při −20 až +20 °C, mít vysoké rozlišení, ostřit od 5 cm, dlouho vydržet na napájení a jít připevnit na otočné rameno.
- Váleček má vnitřní rozměr ⌀100 × 100.
- Navrhnout umístění TDR a teplotních čidel.
- Cílem je měřit deformaci a posun během cyklů mrznutí a tání a experiment má být inovativní.

**Výsledek:** po opravách níže sestava sedí, model je bez kolizí a vše se šroubuje nebo zasouvá. Kontrolu lze kdykoli zopakovat skriptem `src/kontrola_kolizi.py`.

| # | požadavek | stav | kde |
|---|---|---|---|
| 1 | mrazák 59 × 39 × 41 cm | ✓ fáze 1: 383 mm (27 mm k víku); fáze 2: 400 mm (9,8 mm k víku); po stranách 87 / 35 mm | kap. 1 |
| 2 | vše sedí, nic nekoliduje | ✓ po opravách (kap. 4) – sondy, bod M, oběh ±180° bez kolizí | `kontrola_kolizi.py` |
| 3 | nic nechybí | ✓ doplněno 14 položek; platný seznam je jen `dodavatele_E7.md` | kap. 5 |
| 4 | nic se nepájí ani nelepí | ✓ vše na šrouby, svorky, vývodky a zalisování | kap. 6 |
| 5 | kamera: mráz, rozlišení, ostření od 5 cm, výdrž, rameno | ✓ Camera Module 3 **Wide** ve vyhřívané hlavě, 2 polohy ostření, napájení ze sítě se zálohou | kap. 2 |
| 6 | váleček ⌀100 × 100 | ✓ dutina cely přesně ⌀100 × 100, stejná cela pro obě fáze | V03u, V09 |
| 7 | umístění TDR a teplotních čidel | ✓ bod M v hloubce 45 mm + profil T1–T5 po 20 mm | kap. 3, **V09** |
| 8 | deformace při cyklech mrznutí a tání, inovace | ✓ program F1–F4, pole posunů povrchu + profil teploty + TDR | kap. 7, `koncepce_E7.md` |

## 1 · Mrazák 590 × 390 × 410 mm

| | fáze 1 (bez zátěže) | fáze 2 (zátěž) |
|---|---|---|
| výška sestavy | 383 mm | 400 mm |
| k víku | 27 mm | **9,8 mm** |
| po stranách (délka / šířka) | 87 / 35 mm | 87 / 35 mm |

**Ověřit na místě:**
- **Schod nad kompresorem.** Truhlicové mrazáky ho často mají na jednom konci. Sestava s půdorysem 416 × 320 mm musí stát na rovné části dna.
- **Víko ve fázi 2.** Zbývá jen 9,8 mm, a to včetně těsnění a vnitřního výlisku víka. Před prvním zavřením zkontrolovat.
- **Kabely** vedou těsněním víka (plochý Ethernet, USB, kabely čidel). Pod víkem nesmí být nic nad sestavou.

## 2 · Kamera

**Požadavky a jejich splnění:**

| požadavek | řešení | poznámka |
|---|---|---|
| provoz −20 až +20 °C | Raspberry Pi Zero 2 W (výrobce uvádí od −20 °C) v krabičce P06. Kamera je ve **vyhřívané hlavě** P14/P15: topné tělísko PTC 5 V a termostat 5–8 °C podle DS18B20. | Provozní teplotu kamerového modulu výrobce neuvádí, proto se hlava vyhřívá. Ověří se ve slepé zkoušce S0 při −20 °C. |
| vysoké rozlišení | 12 Mpx (4608 × 2592), 36 pohledů na oběh | 1 px ≈ 66 µm na povrchu; výška laserem ≈ 11–23 µm; fotogrammetrie z 36 pohledů |
| ostření od 5 cm | **Camera Module 3 Wide** ostří od 5 cm. Standardní verze ostří až od 10 cm, a to nestačí. | Okénko je od písku 97–162 mm. |
| ostrý celý povrch | **2 polohy ostření** na každé pozici (108 a 140 mm) pokryjí 95–169 mm | Standardní modul by měl ostrý jen pás 118–124 mm (`vypocty.md` §23). |
| dlouhá výdrž | Powerbanka ≈ 100 Wh mimo mrazák trvale na nabíječce USB-C PD funguje jako záložní zdroj. | Ze sítě běží neomezeně, při výpadku ≈ 2 dny (spotřeba ≈ 1,5 W). |
| montáž na otočné rameno | Modul 25 × 24 mm a pár gramů, 4× M2 do hlavy P14; plochý kabel 500 mm ve smyčce | Rameno obíhá ±180°, krok 0,03°, výchozí poloha přes optickou koncovku. |
| video | Modul umí i video 1080p50. Pro cykly trvající desítky hodin je ale vhodnější časosběr. | Krátké video lze spustit z webové stránky ručně. |

**Porovnání možností:**

| kamera | ostření | rozlišení | mráz | na rameno | výdrž, ovládání z PC | verdikt |
|---|---|---|---|---|---|---|
| **RPi Camera Module 3 Wide** + Zero 2 W | **od 5 cm** | 12 Mpx | vyhřívaná hlava | ✓ 25 × 24 mm | ✓ ze sítě / záloha, web + SSH | **zvoleno** |
| RPi Camera Module 3 (standardní) | od 10 cm | 12 Mpx | vyhřívaná hlava | ✓ | ✓ | ✗ nezaostří bližší okraj, malá hloubka ostrosti |
| Arducam 64 Mpx (Hawkeye) | od 8 cm | na Zero 2 W jen 16 Mpx | neuvedeno | ✓ | ✓ | ✗ plné rozlišení vyžaduje RPi 4/5 (ty nejsou na −20 °C) |
| RPi HQ + objektiv C/CS | ruční | 12 Mpx | box | ✗ velká a těžká | ✓ | ✗ rameno ji neunese, nejde přeostřit z programu |
| akční / časosběrné kamery (Brinno, GoPro, Insta360, DJI) | obvykle ≥ 10–30 cm | vysoké | baterie v mrazu hodiny | ✗ | ✗ ovládání z PC jen omezeně | ✗ (posouzeno dříve) |

**Data:** ≈ 5 GB za den, tj. ≈ 100 GB za sérii 10 cyklů. Proto karta 128 GB „high endurance“ a denní stažení do PC přes Ethernet (`rsync`).

## 3 · Čidla ve válečku ⌀100 × 100 (výkres **V09**)

| čidlo | hloubka | úhel | proč tady |
|---|---|---|---|
| **TDR CS645 (bod M)** | tyčky 36 / 45 / 54 mm | 270° (−y) | Uprostřed výšky, kudy čelo mrznutí projde v polovině cyklu. Vodorovně přes osu (75 mm), takže měří střed vzorku, ne okraj u stěny. Uspořádání je stejné jako v terénu (potvrzeno 9. 11.). |
| **Pt100 (bod M)** | 33 mm | 270° | 3,5 mm nad horní tyčkou TDR, hrot 30 mm od stěny. Teplota ve stejném místě jako nezamrzlá voda. |
| **optické vlákno (bod M)** | 31 mm | 270° | jako v terénu |
| **T1–T5 DS18B20 ⌀6** | **10, 30, 50, 70, 90 mm** | 240°, 330°, 210°, 330°, 240° | Profil po 20 mm určí polohu čela 0 °C s přesností ≈ 2–5 mm. Sondy jsou ve šroubovici, aby netvořily svislý „kanál“. Od tyček TDR jsou ≥ 14,6 mm, od stěny 30 mm (mimo vliv stěny). Kabely vedou na stejné straně jako bod M. |
| **NTC (dno)** | v tištěném dně | 30° | okrajová podmínka dole, korekce teplotního driftu cely |
| **vzduch (Campbell 109)** | nad vzorkem | – | okrajová podmínka nahoře |

**Zapojení:**
- Logger CR850 nemá volné vstupy: DIFF1 LVDT, DIFF2 Pt100, SE5 vzduch, SE6 dno, C1–C3 TDR, C4 spouštění.
- Proto profil T1–T5 čte **Raspberry Pi po sběrnici 1-Wire** (GPIO4). Každá sonda má 3 vodiče, které se zapojí do svorek WAGO.
- Adresy sond vypíše příkaz `python3 e7_kamera.py teploty` a zapíšou se do proměnné `PROFILE`.
- Data se zapisují každou minutu do souboru `teploty.csv` a zobrazují se na webové stránce.

**Montáž bez lepení:**
- Otvory ⌀6,3 v cele, na vnější straně závit M12×1,5 vyřezaný závitníkem do předvrtu ⌀10,5 a v něm kabelová vývodka.
- Při hutnění se otvory zaslepí kolíky ⌀6, po hutnění se předvrtá tyčinkou ⌀6 a sonda se zasune po značku.
- Okraje otvorů se tisknou se 6 perimetry, aby voda nevnikla do výplně.

**Alternativa (nedoporučuji měnit):** tyčky TDR ve vodorovné rovině by měřily tenčí vrstvu (ostřejší čelo). Bod M je ale uspořádaný jako v terénu, a to je pro srovnání s CALM-S cennější.

## 4 · Co se při revizi našlo a opravilo

| # | problém | oprava |
|---|---|---|
| 1 | Kabel Pt100 a optické vlákno procházely **skrz hlavu CS645** v portu, takže by nešly smontovat. | Port je o 4 mm vyšší, hlava CS645 zůstane 2–3 mm od vnitřní stěny a kabely vedou nad ní (model, V03u, postup). |
| 2 | Standardní Camera Module 3 nezaostří na bližší okraj (97 mm) a ostrý je jen pás 6 mm. | Camera Module 3 Wide a 2 polohy ostření (`params.py`, `e7_kamera.py`, §23). |
| 3 | Krabička P06/P07 byla pořád box pro HQ kameru (okénko, sloupky pro RPi 5), takže Zero 2 W a moduly nešlo přišroubovat. | Nová krabička elektroniky: sloupky 58 × 23 pro Zero 2 W, dno s drážkami pro moduly (M3 + matice), otvor pro kabely. |
| 4 | Podložky G10 byly v kapsách zarovnané se dnem, takže cela stála celou plochou tištěného dna. | Kapsy hloubky 19,5 mm, podložky vyčnívají 0,5 mm a cela stojí na 3 bodech. |
| 5 | Zbytečný otvor ⌀4 v horní hraně cely (stará trasa Pt100) byl přímo v referenční ploše laseru. | odstraněn |
| 6 | Více DS18B20 na jedné sběrnici: program by bral pro termostat hlavy první nalezené čidlo. | `HEAD_ID` a `PROFILE` v `e7_kamera.py`, příkaz `teploty` |
| 7 | Zastaralé poznámky ve výrobních výkresech: V03u (čelo 5 mm, kapsy 40), P03, P10u, P12 (Hall), P13 (magnet), P14 (sklon), P18 (RPi 5). Totéž ve V04, V07, V08 a ve 3D stránce (T01 306 místo 276, G10 × 40 místo × 20, „samolepicí“ podložky). | opraveno a přegenerováno; poznámky se zalamují |
| 8 | `vypocty.md` §23 popisoval RPi 5, Hall senzor, topné odpory a čelo 5 mm nad pískem. | aktualizováno, přidán §26 (čidla, data, napájení) |
| 9 | `objednavka.md` obsahoval HQ kameru, RPi 5 a spínání laseru tranzistorem (pájení) a rozcházel se se seznamem dodavatelů. | označen jako archiv; platí jen `dodavatele_E7.md` |
| 10 | Pěch ⌀95 byl v postupu, ale nebyl nakreslený ani objednaný. | tištěný díl **P22** |

## 5 · Doplněno do seznamu dílů (`dodavatele_E7.md`)

- **Elektronika:**
  - Camera Module 3 **Wide** (místo standardní);
  - karta microSD 128 GB a 32 GB záložní;
  - 6× sonda DS18B20 ⌀6 × 50;
  - 5× kabelová vývodka M12×1,5;
  - další svorky WAGO;
  - NTC 10 kΩ v jímce ⌀3 s odporem 10 kΩ 0,1 %.
- **Nářadí a drobnosti:**
  - závitník M12×1,5;
  - kolíky ⌀3 a ⌀6 s tyčinkami;
  - spároměr, ocelové měřítko 150 mm;
  - příchytky kabelů do drážky 8;
  - volitelně pigment pro barevné značkovací vrstvy.
- **Napájení:** nabíječka USB-C PD ≥ 45 W pro powerbanku.
- **Tisk:** pěch P22.
- **Poptávka RPishop:** upravena (Camera Module 3 Wide, karta 128 GB). Pokud jste ji už odeslala, pošlete jim doplnění.

## 6 · Montáž bez pájení a lepení – kontrola spojů

| spoj | jak |
|---|---|
| rám | T-profily, úhelníky, T-matice M8 / M5 |
| cela na rámu | 3 podložky G10 v kapsách (vyčnívají 0,5 mm), dorazy P20 na T03; cela se neupevňuje |
| čidla v cele | TDR, Pt100 a vlákno zasunuté portem; T1–T5 ve vývodkách M12 |
| oběh | ložiska a pouzdro igus zalisovaná; jádro P12 4× M5; motor M4; pastorek nalisovaný |
| kamera, LED, topení | M2 / M3 do hlavy a víčka |
| elektronika | Zero 2 WH s osazenou lištou a šroubovacím HATem; moduly na pinech, kabely Dupont, svorky WAGO; odpor NTC ve svorkách CR850 |
| zátěž (fáze 2) | píst 3× M3, kotouče na závitovém čepu M6 s maticí, nosná deska M6 do tyče |
| izolace | XPS a pěna stažené páskami, pryžový pás volně položený |

## 7 · Měření při cyklech mrznutí a tání a co je inovativní

Podrobně v `koncepce_E7.md`. Stručně:
- **Program:**
  - S0 slepá zkouška;
  - F1 Sr 0,5;
  - F2 Sr ≈ 1;
  - F3 se zátěží 2,5 / 25 kPa;
  - F4 cykly podle CALM-S.
- **Inovace:**
  1. 3D pole posunů celého povrchu (laser 11 čar a oběh kamery s 36 pohledy) přímo v mrazáku, místo jednoho snímače;
  2. synchronně profil teploty (čelo mrznutí) a nezamrzlá voda (TDR) v bodě M uspořádaném jako v terénu;
  3. zatížená a volná část povrchu v jednom vzorku;
  4. kumulace deformace přes ≥ 10 cyklů na µm až desítky µm;
  5. levné otevřené zařízení.
- **Novost** je potřeba potvrdit rešerší (Scopus / WoS).

## 8 · Otevřené body (rozhodnout nebo ověřit)

1. **Teplotní program mrazáku.** Ověřit, že regulátor z E6 dosáhne +20 °C. Mrazák sám neohřívá, takže bez topení je horní mez pokojová teplota a tání je pomalé. Zároveň ověřit, zda jde regulátor ovládat z počítače. Pokud ne, může program řídit CR850 přes relé SSR.
2. **Laser s 11 čarami nemá českého dodavatele:** Picotronic (DE), TME (PL), nebo jednočárový laser z laser-shop.cz.
3. **LVDT (fáze 2):** svěrka P02 je nakreslená pro tělo ⌀20,6. Upravit podle výkresu od Micro-Epsilon.
4. **Mrazák:** schod nad kompresorem a vůle víka 9,8 mm ve fázi 2.
5. **Sondy DS18B20:** ověřit průměr pláště ⌀6,0 (otvory ⌀6,3) a délku kabelu.
6. **Camera Module 3 Wide v mrazu:** vyzkoušet ve slepé zkoušce S0 při −20 °C (rozběh, rosa na okénku, ostření).
7. **Novost:** rešerše podle `reserse_scopus_wos.md`.

## Soubory

| | |
|---|---|
| výkresy | `vykresy/E7-V07_bez_zatizeni.pdf`, `E7-V08_se_zatezi.pdf`, **`E7-V09_cidla_ve_vzorku.pdf`**, výrobní `vyroba/vykresy/E7_vyrobni_vykresy.pdf` |
| 3D | `web/E7_sestava_3D_offline.html` (čidla T1–T5 jsou ve skupině Cela a vzorek), `3d/E7_V07_bez_zatizeni.step`, `3d/E7_sestava_final.glb` |
| tisk | `vyroba/tisk/` (cela V03u s otvory T1–T5, P06/P07 nová krabička, P22 pěch) |
| výpočty | `vypocty.md` §23 (kamera, ostření), §25 (roztažnost, překlopení), §26 (čidla, data, napájení) |
| postup, koncepce, dodavatelé | `postup_zkousky.md`, `koncepce_E7.md`, `dodavatele_E7.md` (+ `.docx`) |
| program RPi | `rpi/e7_kamera.py` (oběh, 2 ostření, teplotní profil, web) |
| kontrola | `src/kontrola_kolizi.py` |

Zdroje ke kameře:
- [Raspberry Pi – Camera Module 3, product brief](https://cdn.sparkfun.com/assets/c/b/3/a/1/Camera_Module_3_Product_Brief.pdf);
- [Raspberry Pi – dokumentace Camera Module 3](https://www.raspberrypi.com/documentation/accessories/camera-module-3.html);
- [Arducam 64MP Hawkeye](https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/64MP-Hawkeye/).
