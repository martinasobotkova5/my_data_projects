# E7 – rešerše ve Scopusu a Web of Science: dotazy a postup

Cíl: ověřit, že tyto dvě věci zatím nikdo neudělal:
**(A)** laboratorní měření sublimace ledu z písku s ledem, kde je část povrchu krytá / zatížená („kámen“, deska,
stavba) a část volná – rozdílný pokles povrchu a vznik podstavce, v kombinaci s cykly mrznutí a tání;
**(B)** zatížená a volná část povrchu v jednom vzorku při mrznutí a tání (nenasycený písek, malé zatížení, rozlišení µm).

Přístup: přes knihovnu ČVUT (přihlášení ČVUT) – scopus.com a webofscience.com.

---

## 1 · Scopus (Advanced search, pole TITLE-ABS-KEY)

**S1 – sublimace ledu ze zeminy + kryt / kámen (jádro novosti A)**
```
TITLE-ABS-KEY ( ( sublimation OR "vapor diffusion" OR "vapour diffusion" OR desiccation )
  AND ( "ground ice" OR "ice-cemented" OR "ice-rich" OR "frozen soil" OR "frozen sand" OR permafrost OR "pore ice" )
  AND ( boulder* OR stone* OR clast* OR cover* OR cap OR "surface load*" OR footing* OR pedestal* OR shield* OR "dry lag" ) )
```

**S2 – totéž jen laboratorní pokusy**
```
TITLE-ABS-KEY ( ( sublimation ) AND ( "ice-cemented" OR "ice-rich" OR "frozen soil" OR "frozen sand" OR "ground ice" OR regolith )
  AND ( laborator* OR experiment* OR chamber OR "column test*" OR "analog*" OR analogue* ) )
```

**S3 – zatížená a volná část v jednom vzorku (novost B)**
```
TITLE-ABS-KEY ( ( "frost heave" OR "thaw settlement" OR "freeze-thaw" OR "freeze thaw" )
  AND ( "partial load*" OR "partially loaded" OR "local load*" OR "differential heave" OR "loaded and unloaded"
        OR "free surface" OR footing OR "plate load*" OR "rigid plate" )
  AND ( laborator* OR "model test*" OR specimen* OR sample* ) )
```

**S4 – nenasycený písek, sedání při tání, malé zatížení**
```
TITLE-ABS-KEY ( ( "unsaturated sand" OR "unsaturated soil" OR "partially saturated" OR "degree of saturation" )
  AND ( "thaw settlement" OR "thaw consolidation" OR "frost heave" OR "freeze-thaw cycle*" )
  AND ( surcharge OR overburden OR "vertical load*" OR "vertical stress" ) )
```

**S5 – laboratorní analogie činné vrstvy podle polních dat (Antarktida / Arktida)**
```
TITLE-ABS-KEY ( ( "active layer" OR permafrost ) AND ( laborator* OR "physical model*" OR "analog*" OR analogue* )
  AND ( "field data" OR "ground temperature record*" OR "measured temperature*" OR "replay*" )
  AND ( Antarctic* OR Svalbard OR Arctic OR "James Ross" OR "Dry Valleys" ) )
```

**S6 – průnik A + mrznutí a tání (nejpřísnější; ideálně 0 shod)**
```
TITLE-ABS-KEY ( sublimation AND ( "freeze-thaw" OR "freeze thaw" OR thaw* ) AND ( sand OR soil OR regolith )
  AND ( boulder* OR stone* OR cover* OR load* OR footing* OR pedestal* ) AND ( laborator* OR experiment* ) )
```

Filtry: všechny roky; typ dokumentu Article, Conference paper, Review; jazyk bez omezení.

## 2 · Web of Science Core Collection (Advanced search, pole TS=)

```
S1: TS=((sublimation OR "vapor diffusion" OR desiccation) AND ("ground ice" OR "ice-cemented" OR "ice-rich" OR "frozen soil"
    OR "frozen sand" OR permafrost OR "pore ice") AND (boulder* OR stone* OR clast* OR cover* OR cap OR "surface load*"
    OR footing* OR pedestal* OR "dry lag"))
S2: TS=(sublimation AND ("ice-cemented" OR "ice-rich" OR "frozen soil" OR "frozen sand" OR "ground ice" OR regolith)
    AND (laborator* OR experiment* OR chamber OR "column test*" OR analog*))
S3: TS=(("frost heave" OR "thaw settlement" OR "freeze-thaw") AND ("partial load*" OR "partially loaded" OR "local load*"
    OR "differential heave" OR "loaded and unloaded" OR "free surface" OR footing OR "plate load*") AND (laborator*
    OR "model test*" OR specimen*))
S4: TS=(("unsaturated sand" OR "unsaturated soil" OR "degree of saturation") AND ("thaw settlement" OR "thaw consolidation"
    OR "frost heave" OR "freeze-thaw cycle*") AND (surcharge OR overburden OR "vertical load*" OR "vertical stress"))
S5: TS=(("active layer" OR permafrost) AND (laborator* OR "physical model*" OR analog*) AND ("field data"
    OR "measured temperature*" OR "ground temperature record*") AND (Antarctic* OR Svalbard OR Arctic OR "Dry Valleys"))
S6: TS=(sublimation AND (freeze-thaw OR thaw*) AND (sand OR soil OR regolith) AND (boulder* OR stone* OR cover* OR load*
    OR footing* OR pedestal*) AND (laborator* OR experiment*))
```

## 3 · Export pro vyhodnocení

- **Scopus:** označit vše → *Export* → **CSV**, zaškrtnout *Citation information* + *Bibliographical information* +
  *Abstract & keywords*. Jeden soubor na dotaz (S1.csv … S6.csv).
- **Web of Science:** *Export* → **Excel** nebo *Tab delimited*, *Record content: Full Record*. Jeden soubor na dotaz.
- Soubory nahrát sem do konverzace – vyhodnotím je (odstraním duplicity, roztřídím podle kritérií níže, vyberu
  nejbližší práce a sepíšu, čím se E7 liší).

## 4 · Kritéria pro posouzení každé nalezené práce

| kritérium | E7 (A) | E7 (B) |
|---|---|---|
| laboratoř (ne terén / model) | ano | ano |
| materiál | písek s ledem (ledem bohatý) | nenasycený písek, Sr 0,5 |
| kryt / zatížení jen části povrchu | ano (píst ⌀50 = kámen) | ano |
| volná část měřena současně | ano (laser, µm) | ano |
| sublimace (suchý vzduch, úbytek hmotnosti) | ano | – |
| cykly mrznutí a tání | ano (krátká tání) | ano (24 h + 24 h, polní program) |
| rozlišení deformace | ≈ 10 µm (laser), 1 µm (LVDT) | totéž |
| vazba na polní data (Antarktida / Arktida) | James Ross Island, CALM-S | totéž |

Práce, která splní **všechny** řádky jednoho sloupce, by novost vyvracela; práce, která splní většinu, je
„nejbližší“ a v článku se na ni odkáže jako na základ, od kterého se E7 odlišuje.

## 5 · Co už je známo z orientačního vyhledávání (11/2026)

- Kotouč na čistém ledu v lyofilizátoru → podstavec („Zen stones“), PNAS 2021 – čistý led, ne zemina.
- Sublimace ledu z permafrostu v tunelu u Fairbanks (52 let), Nature Communications 2019 – terén, bez krytu.
- Victoria Valley, Antarktida – model sublimace z polních dat (≈ 0,22 mm/rok).
- Beacon Valley – snižování povrchu sublimací mění polygonální půdy (Sletten et al. 2003).
- Kryté × volné místo, zatížení části povrchu: modelové zkoušky základů v boxech a centrifuze (sloupy, patky),
  ne nenasycený písek v µm a ne sublimace.
