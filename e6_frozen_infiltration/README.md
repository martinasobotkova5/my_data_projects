# E6: infiltrace z minidisku do zmrzlé zeminy – revize schématu a návrh

Revize dvou původních schémat: řez minidiskem na koloně ⌀100 × 100 a sestava E6 v mrazicí komoře. Obsahuje přehled podobných experimentů, navrženou úpravu a výkresy.

| soubor | obsah |
|---|---|
| `vykresy/E6_drawings.pdf` | 12 listů A3, anglicky (PNG po listech ve stejné složce) |
| `vypocty.md` | kontrolní a návrhové výpočty (generované) |
| `src/params.py` | všechny rozměry a předpoklady na jednom místě |
| `src/vykresy.py`, `src/drafting.py` | generátor výkresů (matplotlib) |
| `src/vypocty.py` | generátor `vypocty.md` |
| `src/termometrie.py` | kanály teploty, můstek NTC, rozpočet nejistoty, ohřev kolony mimo mrazák |

Regenerace po změně parametru: `cd src && python vykresy.py && python vypocty.py > ../vypocty.md`

---

## 1. Shrnutí

Čísla v původním schématu sedí (plochy, 4,94 : 1, 0,475 mm, 785 cm³). Koncept „minidisk nahoře, frakční sběrač dole“ je proveditelný. Do první stavby je ale potřeba vyřešit pět věcí:

1. **Zamrzání vody mimo zeminu.** Pokud je komora během infiltrace pod 0 °C, zamrzne zásobník, disk, hadička i výtok. Láhev značené vody „0,0 °C“ uvnitř komory při −3 °C neudržíte. Infiltrační fáze proto musí běžet se vzduchem komory kolem +0,5 °C a s temperovaným dnem.
2. **„Zmrzlá“ fáze je krátká.** Citelný chlad vzorku při −3 °C stačí na opětovné zmrznutí jen asi 13 ml vody. To je 6 % pórového objemu, při 3–8 ml/h zhruba 2–4 h. Pak je vzorek izotermní na 0 °C s ledem v pórech. Pro tání sněhu je to realistický režim. Je ale potřeba s ním počítat při interpretaci a v okrajových podmínkách modelu (`vypocty.md`, část 4).
3. **Spodní okraj.** Dutá nálevka s perforovanou deskou drží na dně tlak h = 0, tedy průsakovou plochu (seepage face). Voda se pak u dna hromadí, než začne odtékat, a průnikové křivky se zkreslí (Abdou & Flury 2004; Zhang et al. 2008). Navrhuji **kónický odtok s plným kuželem**: zvenku stejná nálevka 45°, nahoře nylonová membrána 20 µm, pod ní drážky. Sání dna h_b = 0 … −30 cm se nastavuje výškou přepadové misky. h_b = 0 dá původní režim, takže se dají porovnat oba. Mrtvý objem je ~1,7 ml místo ~120 cm³.
4. **Doba běhu.** Údaj „5–37 h“ je jen doba, za kterou čelo zvlhčení zaplní Δθ. Průnik značky na 1,5 pórového objemu (~350 ml) trvá **44–111 h**. 60 frakcí po 2–5 ml pokryje jen 0,5–1,3 PV. Počítejte s 2–5 dny infiltrace a 70–180 frakcemi.
5. **Zásobník ⌀31 nestačí.** Repozitář AMDI uvádí ~150 ml, potřeba je ~350 ml. Plný zásobník navíc zatěžuje disk ~2 kPa. Navrhuji externí Mariottovu láhev na váze (0,01 g) a nízkoprofilovou hlavu se snímačem tlaku přímo na disku.

## 2. Podrobné připomínky k původnímu schématu

| # | závažnost | zjištění | návrh |
|---|---|---|---|
| A | zásadní | Komora −8 … +5 °C chladí vše, včetně láhve, zásobníku, bublinkové věže, výtoku a sběrače. | Fáze infiltrace při vzduchu +0,5 °C; láhev v plášti +0,5 °C; vyhřívaná odtoková linka +1 °C; sběrač v izolovaném boxu +4 °C (E6-V06). |
| B | zásadní | Chlazení jen vzduchem s nuceným oběhem dává radiální mrznutí od stěn. | Izolace 30 mm, zmrazování shora (vzduch −5 °C) při kuželi +1 °C, pak kužel −3 °C. Kužel je zároveň spodní výměník: Cu spirála napojená na kryostat (E6-V01, V04, V07). |
| C | zásadní | Otevřený kužel znamená seepage face: dno se musí nasytit, než voda odteče. U nenasyceného toku při h₀ = −2 cm to zkresluje odtok i průnik značky. | Membrána + nastavitelné h_b (E6-V04, V06). |
| D | zásadní | Zmrzlá zemina při −3 °C má podle Clapeyronovy rovnice potenciál ≈ −370 m. Během mrznutí by nasála vodu z odtokové linky (kryosukce) a vytvořila u dna ledové čočky. | Ventil V3 na výtoku zavřený po celou dobu mrznutí. Přepadová miska místo volného odkapu, aby zpětné sání nevtáhlo vzduch pod membránu. |
| E | důležité | Kapacita zásobníku ⌀31: 1 PV odpovídá ~31 cm sloupce; zatížení disku. | Externí Mariottova láhev na váze. Pozor: při zdvihu povrchu se h₀ mění o velikost zdvihu, proto snímač tlaku na disku (PT) a LVDT-0. Integrovaný minidisk to kompenzuje sám, ale nestačí objemem. |
| F | důležité | Snímač 0–10 kPa s „0,1 mm v. sl.“ = 1 Pa = 0,01 % FS, což je nereálné. Běžně 0,1 % FS ≈ 1 mm. | Přítok měřit váhou (0,01 g ≙ 0,006 mm přes disk). Diferenční snímač ±2,5 kPa jen pro kontrolu h₀. |
| G | důležité | Stereo-DIC „přes okno komory“ nevidí povrch: mezikruží zakrývá límec a izolace, stěnu Kaiflex. Okno se navíc orosí nebo namrzne. | Zdvih měřit 3× LVDT (hlava + plovoucí prstenec), E6-V01/V05. |
| H | důležité | Izotopy: frakcionace led–voda α(D/H) ≈ 1,0212, tj. ~21 ‰ (Lehmann & Siegenthaler 1991). To je 4–7 % rozdílu značky vůči pozadí. | δ¹⁸O **neznačit** (jen D₂O). δ¹⁸O pak slouží jako nezávislý indikátor frakcionace a podílu „staré“ vody (d-excess). |
| I | důležité | OA-ICOS a značka +500 ‰: paměťový efekt 7–8 nástřiků při skoku ~200 ‰ (Penna et al. 2012). Br⁻ = sůl ve vaporizéru. | Řadit vzorky podle očekávaného obohacení. Obohacené laboratorní standardy, které pokrývají rozsah. Br⁻ držet v jednotkách až desítkách mg/l a často měnit septa a liner. EC a Br⁻ (IC) měřit z odděleného alikvotu. |
| J | důležité | Odpar frakcí mění δ²H (Williams et al. 2018; von Freyberg et al. 2020). | Vialky se septem, sběr při +4 °C, zavírat ihned. Žádný olejový film: ruší laserovou spektroskopii (Michelsen et al. 2019). |
| K | střední | Kontaktní písek a disk v kontaktu s půdou při −3 °C: první voda zmrzne v písku nebo v disku a zablokuje přítok. Publikované řešení pro tenzní infiltrometr na zmrzlé půdě existuje jen s glykolem (Jiang et al. 2021), což se značkou nejde. | Písek vkládat suchý, předchlazený na 0 °C, vzduch +0,5 °C. Termistor Tdisc na kontaktu. Selhání přítoku je měřitelný výsledek, ne chyba. |
| L | střední | Nesrovnalosti mezi obrázky: „porézní deska“ × „perforovaná deska + síťka 50 µm + kužel“. 6 termistorů 2–70 mm × 3 body v půdorysu. „3× TDR ve dvou poloměrech“ × 2 TDR v půdorysu. „Plovoucí raft“ chybí v řezu. | Sjednoceno ve výkresech E6-V01, E6-V02, E6-V03 (tabulka čidel a otvorů). |
| M | střední | Nejhlubší termistor je 70 mm, spodních 30 mm není pokryto. Termistory jen pod diskem (r = 9). | 6 termistorů ve stěně na hloubkách 10–90 mm, 2 jehly v plovoucím prstenci (2 a 6 mm, mezikruží), Tdisc, Tcone. |
| N | menší | Desky tepelného toku ±100 W/m² se do mezikruží 27,5 mm vejdou jen jako miniaturní (≤ 10 × 10 mm). | Uvedeno 10 × 10 mm. Typ ověřit. |
| O | menší | 3D divergence pod diskem: souhlasím, že ji WL3.3 osově symetricky popíše. | Volitelná varianta B: dělený odtok (vnitřní ⌀50 a mezikruží) dá dvě průnikové křivky a model víc omezí (E6-V04, červeně). |

## 3. Podobné experimenty (literatura)

Ověřeno vyhledáním; DOI uvádím jen tam, kde se je podařilo potvrdit.

**Infiltrace do zmrzlé zeminy – kolony a boxy**
- Watanabe K. et al. (2013): Water infiltration into a frozen soil with simultaneous melting of the frozen layer. *Vadose Zone J.* 12. doi:10.2136/vzj2011.0188.
  - Kolony prachovité hlíny chlazené shora, ponor vody 3,5 °C.
  - Tři fáze: nulová infiltrace, pomalý tok zmrzlou vrstvou, rychlý tok po proniknutí do nezmrzlé zeminy.
  - Geometrie „zmrzlá vrstva nad nezmrzlou“ je standard. Z ní vychází navržený protokol E6-V07.
- Watanabe K., Kugisaki Y. (2017): Effect of macropores on soil freezing and thawing with infiltration. *Hydrol. Process.* 31, 270–278. doi:10.1002/hyp.10939.
  - Voda v makropóru zpětně zamrzá a makropór ucpe.
  - Totéž hrozí v kontaktní mezeře u stěny, odtud zdrsněná stěna.
- Stadler D. et al. (2000): Dye tracing and image analysis for quantifying water infiltration into frozen soils. *SSSAJ* 64, 505–516.
  - Kolony zmrazené v komoře na −5 °C.
  - O preferenčním toku rozhoduje vlhkost při zamrznutí.
- Nagare R. M. et al. (2012): Effects of freezing on soil temperature, freezing front propagation and moisture redistribution in peat. *HESS* 16, 501–515. doi:10.5194/hess-16-501-2012.
  - Při mrznutí se voda výrazně přesouvá k frontě.
  - Před infiltrací je proto potřeba znát profil vody i ledu. Pomáhá zavřený V3 a závěrečné řezání vzorku.
- Hansson K. et al. (2004): Water flow and heat transport in frozen soil. *VZJ* 3, 693–704.
  - Validace modulu HYDRUS na kolonách 8 × 20 cm chlazených deskou s cirkulující kapalinou.
  - Deska s kapalinou, ne vzduch, je obvyklé uspořádání.
- Demand D., Selker J. S., Weiler M. (2019): Influences of macropores on infiltration into seasonally frozen soil. *VZJ* 18. doi:10.2136/vzj2018.08.0147.
  - Zpětné zamrzání na povrchu rychlost infiltrace zhruba třikrát snížilo.
  - Varianta s NaCl je užitečná kontrola.
- Bauer J. et al. (2026): Thermohydraulic experiments on water infiltration into frozen slopes. *The Cryosphere* 20, 3483–3509. doi:10.5194/tc-20-3483-2026.
  - Nejnovější laboratorní box v klimakomoře, s diskusí omezení malých kolon.
- Mohammed A. A. et al. (2018): Snowmelt infiltration and macropore flow in frozen soils. *VZJ* 17. doi:10.2136/vzj2018.04.0084. Přehled a otevřené otázky.

**Tenzní infiltrometr a zmrzlá zemina**
- Jiang R. et al. (2021). *The Cryosphere* 15, 2133–2146. doi:10.5194/tc-15-2133-2021. Tenzní infiltrometr na zmrzlé zemině, ale s etylenglykolem.
- Kubát J.-F., Zanna F., Mildner M., Sněhota M. (2025): Low-cost autonomous 3D-printed mini disk infiltrometer. *J. Hydrol.* 663A, 134212. doi:10.1016/j.jhydrol.2025.134212.
  - Repozitář: https://github.com/kubatjanf/AMDI (CC0).
  - Disk ⌀45 × 3 ze spékané nerezi, ~150 ml vody, PETG.
- Bagarello V. et al. (2025). *Hydrology* 12(4), 85. doi:10.3390/hydrology12040085. Minidisk na kolonách: způsob hutnění mění parametry až 2,7×, je potřeba ~6 opakování.

**Izotopy a stopovače ve zmrzlé zemině**
- Lehmann M., Siegenthaler U. (1991). *J. Glaciol.* 37, 23–26. doi:10.3189/S0022143000042751. α led–voda.
- Muhic F. et al. (2024): Snowmelt-mediated isotopic homogenization of shallow till soil. *HESS* 28, 4861–4881. doi:10.5194/hess-28-4861-2024. Terénní značení δ²H přes zimu.
- **Mezera v literatuře:** laboratorní kolonový experiment s průnikem δ²H nebo Br⁻ zmrzlou zeminou jsme nenašli. E6 by byl v tomto ohledu nový.

**Spodní okraj a analytika**
- Abdou H. M., Flury M. (2004). *Eur. J. Soil Sci.* 55, 229–241. Seepage face u volně odtékajících lyzimetrů.
- Peters A., Durner W. (2009). *HESS* 13, 1671–1683. doi:10.5194/hess-13-1671-2009.
- Pütz T., Fank J., Flury M. (2018). *VZJ* 17. doi:10.2136/vzj2018.02.0035.
- Penna D. et al. (2012). *HESS* 16, 3925–3937. doi:10.5194/hess-16-3925-2012. Paměťový efekt laserových analyzátorů.
- Williams D. G. et al. (2018). *Agric. Environ. Lett.* 3. doi:10.2134/ael2018.02.0009. Odpar vzorků.
- von Freyberg J. et al. (2020). *HESS* 24, 5821–5834. Bariéra proti odparu pro ISCO.
- Michelsen N. et al. (2019). *HESS* 23, 2637–2645. Olejový film a laserové analyzátory.

## 4. Navržené řešení (výkresy)

| list | obsah |
|---|---|
| E6-V01 | Sestava, řez A–A 1 : 1, 28 pozic |
| E6-V02 | Půdorys čidel 1 : 1 + tabulka čidel (úhel, poloměr, hloubka, z) |
| E6-V03 | Rozvinutý plášť trubky PMMA ⌀110/100 × 125 + tabulka otvorů pro výrobu |
| E6-V04 | Kónický odtok: řez, horní líc s drážkami, detail sevření membrány 5 : 1, varianta B |
| E6-V05 | Detail disk–zemina 2 : 1, úpravy hlavy AMDI |
| E6-V06 | Hydraulické a tepelné schéma, ventily, okrajové podmínky, bilance |
| E6-V07 | Protokol: zmrazení v mrazáku → přenos → infiltrace na stole, odhad teploty vzorku, kroky go/no-go |
| E6-V08 | Měření teploty v truhlicovém mrazáku: rozmístění 20 kanálů uvnitř a vně, límec s průchodkami |
| E6-V09 | Termistorová sonda ⌀1,6, uložení ve stěně, polomůstek, kalibrace, rozpočet nejistoty |
| E6-V10 | Skutečná sestava podle fotek: půdorys a řez mrazákem 1 : 5, zjištění a změny |
| E6-V11 | Tištěný držák vzorku 1 : 1: kam umístit teploměry, TDR a desky tepelného toku |
| E6-V12 | Pracoviště na stole po vyndání z mrazáku, jak dlouho vydrží vzorek zmrzlý |

Klíčová rozhodnutí:
- Vzorek zůstává **⌀100 × 100 mm (vnitřní)**.
- **Pod vzorkem je kónický odtok:** plný Al kužel 45° s membránou, drážkami, osovým vývrtem a tryskou na hrotu. Kužel je obalený Cu spirálou z kryostatu.
- Plovoucí izolační prstenec na mezikruží nese desky tepelného toku a termistorové jehly. Hlava i prstenec mají vůli 2 mm a volně se pohybují se zdvihem.
- Zemina se zmrazuje shora dolů a pak se celá ustálí na −3 °C. Infiltrace běží při vzduchu +0,5 °C a kuželu +0,3 °C. Jde o scénář „tání sněhu na zmrzlou půdu“, kdy se dno rozmrazí jen v tenké vrstvě.

## 5. Varianta: zmrazení v mrazáku a měření teploty (doplněno)

Postup podle upřesnění: vzorek se zmrazí v mrazáku. Pak začne infiltrace minidiskem AMDI:
- Kubát J.-F., Zanna F., Mildner M., Sněhota M. (2025): *Low-cost autonomous 3D-printed mini disk infiltrometer.* J. Hydrol. 663A, 134212. doi:10.1016/j.jhydrol.2025.134212.
- Preprint SSRN: doi:10.2139/ssrn.5280249.
- Repozitář: https://github.com/kubatjanf/AMDI. Disk ⌀45 × 3 mm ze spékané nerezi, ~150 ml vody, čidlo TMS-4 v Mariottově komoře.

**Infiltrace mimo mrazák.** Pokud se vzorek po zmrazení vyndá do laboratoře (20 °C), získá i přes izolaci 30 mm zhruba 1,9 W tepla. To znamená:
- Na 0 °C se ohřeje asi za 0,6 h.
- Veškerý led roztaje asi za 8 h, a to bez započtení tepla z infiltrující vody.
- Průnik značky přitom trvá 44–111 h, takže by většina běhu proběhla v rozmrzlé zemině.

Doporučuji proto infiltraci nechat **v mrazáku**, s regulátorem nastaveným na +0,5 °C (výpočty v `vypocty.md`, část 8). Mrazák tak slouží zároveň jako klimakomora. Truhlicový typ se otevírá shora, což vyhovuje disku nahoře.

**Měření teploty** (E6-V08, E6-V09, `vypocty.md` část 7):
- **Čidla:** NTC 10 kΩ ve skleněné perličce v nerezové trubičce ⌀1,6 mm (= 1/16″). Těsní se do standardního HPLC šroubení na nalepeném nálitku stěny.
- **Zapojení:** poloviční můstek s referenčním odporem 30 kΩ (0,01 %, 2 ppm/K) na stávajícím CR3000. Buzení 0,5 V jen po dobu měření, samoohřev ≈ 1,4 mK.
- **Rozlišení:** 0,01 K odpovídá ≈ 66 µV.
- **Nejistota:** rozšířená nejistota U ≈ 8 mK (k = 2) splní požadavek 0,01 °C. Podmínkou je kalibrace celého řetězce (sonda + kabel + stejný logger) v míchané lázni proti referenčnímu teploměru v 11 bodech od −8 do +20 °C a fit Steinhart–Hart. Nulový bod se kontroluje v Dewarově nádobě s ledem před a po každém běhu.
- **Uvnitř mrazáku (16 kanálů):** 6 sond ve stěně kolony, 2 jehly v plovoucím prstenci, rozhraní disk/písek, kužel, voda v Mariottově láhvi, odtok, 3 stíněná čidla vzduchu v různých výškách, referenční cela s čistou vodou (její plato 0 °C při mrznutí kontroluje celý řetězec přímo na místě).
- **Vně (4 kanály):** vzduch v laboratoři, teplota u referenčních odporů v boxu loggeru, sonda v ledové lázni, pevný odpor 30 kΩ pro kontrolu driftu loggeru.
- **Kabely:** vedou přes límec (XPS 50 mm) vložený mezi tělo a víko mrazáku. Stěny truhly **nevrtat**, vedou v nich chladivo. Na studené straně nesmí být konektory. Ventilátor a lahve s vodou tlumí cyklování kompresoru.

## 6. Skutečná sestava podle fotek (E6-V10, E6-V11)

**Co je na fotkách vidět:**
- Truhlicový mrazák s programovatelným regulátorem. Program „Set A“: 24 h při +10 °C, pak kroky po 192 h střídavě −10 / +10 °C, lineárně. Hodiny regulátoru ukazují 29.02.2000.
- Silná námraza na stěnách. Kabely vedou pod těsněním víka.
- Nerezová vana ≈ 530 × 340 mm na černé izolační podložce.
- Vzorek v průhledném tištěném držáku z PETG (⌀100 uvnitř, široká horní příruba) stojí přímo na vaně, takže nemá odtok.
- Na vzorku leží hliníková deska ≈ ⌀112 × 20 mm se středovým otvorem ≈ ⌀26 a vybráním ≈ ⌀60.
- Dva termistory jsou zapíchnuté svisle shora do písku.
- Dvě desky tepelného toku jsou přilepené páskou: jedna na Al desce, druhá na vaně.

**Navržené změny (červeně ve výkresech):**
- **Odtok:** vzorek postavit na kónický odtok se stojanem ≈ 150 mm. Frakční sběrač stojí vedle na vaně, přepadová miska nastavuje h_b.
- **Izolace:** kolem držáku izolační rukáv 30 mm.
- **Al deska:** otvor rozšířit na ⌀64, aby disk AMDI dosáhl na zeminu. Deska tak zůstane jako chladná prstencová horní hranice.
- **Kabely:** vést přes límec s průchodkami, ne pod víkem. Mrazák před během odmrazit a nastavit hodiny regulátoru.
- **Teploměry:** svislé sondy shora nahradit vodorovnými sondami ve stěně v hloubkách 10–90 mm. Do držáku natisknout nálitky pro šroubení 1/16″. Dále:
  - jehly 2 a 6 mm přes Al desku,
  - Tplate ve vývrtu Al desky,
  - Tdisc na kontaktu disku s pískem,
  - Tcone ve dně,
  - HF1 pod Al deskou,
  - HF2 na plášti držáku (kontrola bočních ztrát),
  - vzduch A1–A3 a referenční cela s čistou vodou.

## 7. Potvrzený postup: zmrazit v mrazáku, infiltrovat mimo něj (E6-V07, E6-V12)

Vzorek se zmrazí v truhlicovém mrazáku, pak se vyndá a infiltrace běží na laboratorním stole. Důsledky a úpravy:

- **Doba zmrzlého stavu je omezená.** Soustředěný odhad (`vypocty.md` §8) pro laboratoř 20 °C:

  | izolace | start −3 °C: na 0 °C | start −10 °C: na 0 °C | led roztaje |
  |---|---|---|---|
  | Kaiflex 30 mm | 0,6 h | 1,7 h | ≈ 8 h |
  | box PU/XPS 60 mm | 1,1 h | 3,1 h | ≈ 14 h |
  | box PU/XPS 100 mm | 1,5 h | 4,4 h | ≈ 20 h |

  Skutečné časy budou kratší: nezaizolovaná hlava AMDI, nožky, kabely a teplo vody. Průnik značky (44–111 h) proto vždy zahrne i tání a tok rozmrzlou zeminou. Teploty ukážou, kdy a kde led zmizí (konec plata 0 °C).
- **Izolace:** pro infiltraci použít dvoudílný izolační box ≥ 60 mm. Pokud má být delší zmrzlá fáze, zmrazit na −10 °C.
- **Teplota vody:** Mariottova láhev, kontaktní písek i disk na 0–0,5 °C (ledová lázeň). Voda 20 °C by nejdřív roztála stopu pod diskem.
- **Teploty bez přerušení:** logger stojí na vozíku mezi mrazákem a stolem a kabely (≥ 3 m) se nikdy neodpojují. Záznam teplot je tak spojitý od zmrazení po konec infiltrace. Kalibrace zůstává platná, protože se nemění řetězec.
- **Přenos:** kolona + kužel + stojan jako jeden celek, ≤ 10 min. Zapsat čas začátku a konce.
- **Dno:** zmrzlý kužel blokuje odtok. Volitelná lázeň +0,5 °C na spirále kužele rozmrazí spodní milimetry, aby voda odtekla při h_b.
- **Frakce:** vialky se septem na ledu nebo chladicím bloku, jinak se v laboratoři odpaří.
- **Co odpadá:** zamrzání přívodu a výtoku (body A a B v části 2) se týká jen infiltrace v mrazáku.

## 8. Otevřené otázky

1. **Typ zeminy a cílová vlhkost při zmrazení.** Na nich závisí nezamrzlá voda i to, zda vůbec něco proteče (Stadler 2000). Ve výpočtech předpokládám θ = 0,30 a θ_u(−3 °C) = 0,07.
2. **Nastavení h_b.** Navrhuji začít na −5 cm. h_b = 0 jako srovnávací běh s původním „volným“ výtokem?
3. **Má zůstat scénář „celý vzorek pod 0 °C po celou dobu“?** Pak by odtok byl možný jen po tání. Navržený protokol místo toho drží dno těsně nad 0 °C.
4. **Kryostat:** je k dispozici, nebo ho počítat do rozpočtu? Bez něj kužel neudržíte nad 0 °C při současném mrznutí shora.
5. **Frakční sběrač:** konkrétní typ (ISCO Foxy, Gilson…) a zda snese +4 °C. Podle toho upravím rozměry boxu.
6. **Mrazák „Kesa“:** značku ani typ se nepodařilo dohledat. Výkres E6-V08 předpokládá truhlicový mrazák s externím regulátorem. Prosím o přesný typ a vnitřní rozměry, upravím podle nich.
7. **Rozměry ze sestavy:** změřit vnitřek mrazáku, vanu, držák (stěna, výška, příruba), Al desku (⌀, tloušťka, otvor) a vnější ⌀ těla AMDI. Kde je čidlo regulátoru? Co je černý kabel a modrá hadička (TDR?)?
8. **Infiltrace v mrazáku, nebo mimo něj?** Podle výpočtu doporučuji v mrazáku (viz bod 5).
9. **Hlava AMDI:** navrhuji nízkoprofilovou variantu s externí Mariottovou láhví. Pokud chcete zachovat originální integrovaný zásobník, dá se to, ale s doplňováním během běhu a vyšším zatížením disku.

> Výkresy jsou NÁVRH generovaný ze `src/params.py`. Před výrobou je musí zkontrolovat konstruktér. Ověřit je potřeba hlavně uložení kužele, rozměry šroubení a skutečné rozměry čidel.
