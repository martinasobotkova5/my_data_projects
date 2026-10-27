"""E7 rig C rev. B2 – objednávka po obchodech (CZ) + postup sestavení.

Délky a počty se berou z params.py / buildparts.py, takže po změně rozměrů stačí spustit znovu:
    python objednavka.py      → ../objednavka.md
Ceny: „ověřeno“ = cena nalezená na webu prodejce (10/2026), „odhad“ = bez ověřené ceny, poptat.
"""
import os

import buildparts as bp
import params as p

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "objednavka.md")
EUR = 25.0          # Kč / €

# (obchod, odkaz, [(položka, specifikace / co napsat do objednávky, ks, cena, stav)])
SHOPS = [
    ("1 · Laserové řezání podle DXF (jedna objednávka)",
     "[grupol.cz](https://grupol.cz/) – nahrát DXF, cena hned; alternativy [Zamet](https://www.zamet.cz/laserove-rezani) "
     "(ocel do 20 mm), [Light Cut](https://lightcut.cz/co-umime/rezani-laserem/)",
     [(f"{d['name']}", f"{d['mat'].split(' (')[0]}, tl. {d['t']:g} mm – soubor `vyroba/laser/{d['name']}_{d['t']:g}mm.dxf`",
       d["qty"], "", "") for d in bp.LASER]
     + [("—", "Hliník 10 mm: ověřit, že ho laser zvládne; jinak stejné DXF na vodní paprsek. Ocel 12 mm: "
              "kotouče převážit, ±0,5 mm tloušťky = ±4 % hmotnosti", "", "≈ 100–190 € celkem", "odhad")]),
    ("2 · Hliníkové profily a spojovací díly rámu",
     "[Enprag](https://www.enprag.cz/hlinikove-profily/c-6027) (drážka 8, kompatibilní s item/Bosch, řez na míru); "
     "alternativa [eProfily.cz](https://www.eprofily.cz/hlinikovy-profil-80x40-s-drazkou-8-mm/kat3007.html)",
     [("Profil 40×80 drážka 8 (Enprag KA-4080H)", f"řez na délku {bp.COL_H:g} mm, kolmý řez ±0,2", 2,
       "31,43 €/m bez DPH (+ řez)", "ověřeno (Enprag EN)"),
      ("Úhelník 40×40 drážka 8 (Zn) s krytkou", "sloupy ↔ deska základny a horní deska", 8, "≈ 3–6 €/ks", "odhad"),
      ("T-matice drážka 8, M8 (pérová / otočná)", "+ 4 rezervní", 12, "≈ 1 €/ks", "odhad"),
      ("Stavitelná noha M8 (talíř ⌀30–40)", "do otvorů ⌀8,5 v základní desce + 2 matice M8", 3, "≈ 3–5 €/ks", "odhad")]),
    ("3 · Invar 36 (tyče řezané na délku)",
     "[Evek – Invar 36 kulatina](https://evek.vip/slitina-niklu/451-ty%C4%8D-invar36-%C3%B8-2mm-70mm-13912-ty%C4%8D-kulat%C3%A1-nilo-36-alloy-36-uns-k93600.html) "
     "(1.3912, česky, řez na míru)",
     [("Invar 36 ⌀12", f"délka {bp.ROD_L} mm, tolerance h9 nebo lepší (vodicí tyč pro kluzné pouzdro), čela kolmá, sražení 0,5×45°",
       1, "", "poptat"),
      ("Invar 36 ⌀16", f"délka {bp.POST_L:.0f} mm, čela kolmá", 1, "", "poptat"),
      ("—", "obojí ≈ 0,9 kg Invaru", "", "≈ 80–160 €", "odhad")]),
    ("4 · Podložky G10 (sklotextit)",
     "[Elektroizolanty Praha – tyče G10](https://www.elektroizolanty.cz/elektroizonlanty/eshop/57-1-Tyce-G10-130-C-akcni-ceny)",
     [("Sklotextit G10 tyč ⌀20 × 1000 mm", "požádat o nařezání 3× 40 mm (čela rovnoběžná) – nebo nařezat v dílně", 1,
       "298 Kč", "ověřeno")]),
    ("5 · Ložisko, kroužek, kulička, šrouby",
     "[igus.cz](https://www.igus.cz) nebo [TME](https://www.tme.eu/cz/) (igus drylin); "
     "[Fabory CZ – stavěcí kroužky](https://www.fabory.com/cs/Fasteners/Washers-and-Rings/Adjusting-rings/c/011001); "
     "šrouby Hornbach / Fabory; kulička v cyklo obchodě",
     [("igus drylin RJ4JP-01-12", "kluzné pouzdro ⌀12 (⌀21 × 30), bez maziva, do −40 °C", 1, "≈ 2–5 €", "odhad"),
      ("Stavěcí kroužek DIN 705-A 12 (⌀22 × 12, šroub M6)", "pod nosnou desku závaží (+1 rezerva)", 2, "≈ 2–4 €/ks", "odhad"),
      ("Ocelová ložisková kulička 5/16\" (7,94 mm)", "cyklo kuličky, balení", 1, "≈ 1–3 €", "odhad"),
      ("Imbus ISO 4762 M8×16 + podložka", "úhelníky do T-matic", 8, "", "sada"),
      ("Šroub M8×25 + matice + 2 podložky", "úhelníky ↔ desky (drážky v deskách)", 8, "", "sada"),
      ("Šroub M5×45 + matice + podložky", "pouzdro ložiska ↔ horní deska", 4, "", "sada"),
      ("Šroub M5×20 + matice + podložky", "patka sloupku (2), držák laseru (2), závěs kamery (2)", 6, "", "sada"),
      ("Šroub M4×20 + matice", "box kamery ↔ závěs, svěrky", 4, "", "sada"),
      ("Šroub M3×20 + matice, červík M3×6", "svěrky ramen (3), aretace laseru (1)", 4, "", "sada"),
      ("Šroubky M2,5×6 + distanční sloupky 10 mm", "HQ kamera (4) a RPi 5 (4) v boxu", 8, "", "sada"),
      ("—", "spojovací materiál celkem", "", "≈ 15–25 €", "odhad")]),
    ("6 · 3D tisk (vlastní tiskárna)",
     "[Prusament PETG Carbon Fiber](https://www.prusa3d.com/product/prusament-petg-carbon-fiber-black-1kg/) (Prusa, CZ)",
     [("Prusament PETG Carbon Fiber 1 kg", "cela ≈ 1,3–1,6 kg + díly P01–P08 ≈ 0,3 kg", 2, "≈ 55 €/ks", "ověřeno (USD cena)"),
      ("Tiskárna pro celu", "podložka ≥ 250 × 250, výška ≥ 200 (Prusa XL, Bambu X1/P1S); Prusa MK4/Core One nestačí",
       "", "", "info"),
      ("Sklo do okénka boxu kamery", "50 × 50 × 2 mm (sklo z fotorámečku / sklenářství) nebo plexi 2 mm", 1, "≈ 1–3 €", "odhad")]),
    ("7 · Kamera, Raspberry Pi, elektronika",
     "[RPishop.cz](https://rpishop.cz/), [LaskaKit](https://www.laskakit.cz/), [GM electronic](https://www.gme.cz/), "
     "[TME](https://www.tme.eu/cz/)",
     [("Raspberry Pi 5, 4 GB", "", 1, "2 769 Kč", "ověřeno"),
      ("Raspberry Pi HQ Camera C/CS (OFI060)", "ne verze M12", 1, "1 499 Kč", "ověřeno"),
      ("Raspberry Pi 6 mm CS objektiv (širokoúhlý)", "", 1, "≈ 20–30 €", "odhad"),
      ("Kabel kamery Standard–Mini 200 mm, zdroj 27 W, microSD 32 GB", "", 1, "≈ 400–600 Kč", "odhad"),
      ("Čidlo SHT45 (RH/T) na I2C", "vlhkost vzduchu v truhle", 1, "≈ 15–25 €", "odhad"),
      ("Ventilátor 80 mm 12 V + zdroj 12 V", "promíchání vzduchu (běží trvale)", 1, "≈ 10–20 €", "odhad"),
      ("Mean Well HDR-15-24 (24 V DIN)", "napájení LVDT (trvale zapnuté)", 1, "≈ 11 € bez DPH", "ověřeno (TME)"),
      ("Kabelová vývodka PG7 + Ethernet kabel 3 m", "box kamery", 1, "≈ 5 €", "odhad"),
      ("Optočlen / relé modul 5 V pro spouštění snímku", "CR1000 C5 → GPIO RPi", 1, "≈ 3–5 €", "odhad")]),
    ("8 · Čidla ze zahraničí a Campbell",
     "Picotronic (DE), Elkome (FI), [Ekotechnika Černošice](https://campbellsci.com/ekotechnika) (Campbell pro ČR)",
     [("Laser Picotronic DOE253-635-1-6(10x22), obj. č. 70111842",
       "11 čar, 635 nm, 1 mW, 5 V, ⌀10 × 22", 1, "91,51 € bez DPH",
       "ověřeno – [shop](https://www.picotronic.de/picopage/en/product/detail/id/86333)"),
      ("LVDT RDP DCTH400AG", "±10 mm, pružina, tělo ⌀20,6; ověřit provoz při −10 °C", 1, "581 €",
       "ověřeno – [Elkome](https://shop.elkome.com/en/dcth400ag-lvdt-displacement-sensor)"),
      ("Campbell 4WPB100", "modul pro 4vodičové Pt100", 1, "≈ 60–120 €", "poptat – tel. +420 251 640 511"),
      ("Campbell 109-L, kabel 3 m", "teplota vzduchu (povinně)", 1, "≈ 150–220 €", "poptat")]),
    ("9 · Spotřební materiál",
     "Hornbach / OBI, [TME](https://www.tme.eu/cz/) (Molykote)",
     [("Dvousložkový epoxid", "nátěr dutiny cely + slepení pístu (L04 + L05)", 1, "≈ 10–15 €", "odhad"),
      ("PTFE sprej + silikonová vazelína (Molykote 111)", "stěna dutiny", 1, "≈ 15–25 €", "odhad"),
      ("Spároměr 0,05–1,00 mm", "kalibrace kamery (0,1 / 0,5 / 1,0 mm)", 1, "≈ 5–10 €", "odhad"),
      ("Bílá matná samolepka / papír 12 × 12", "terčík na rameno P03", 1, "", "")]),
]

ASSEMBLY = [
    "Vytiskněte celu (V03) a díly P01–P08 (`vyroba/tisk/*.stl`, PETG-CF, 0,2 mm, 3 perimetry, 40 % gyroid; cela podle V03). "
    "Dutinu cely natřete epoxidem, po vytvrzení PTFE sprej + tenká vrstva silikonové vazelíny.",
    "Píst: kotouče L05 (spodní) a L04 (horní, otvor ⌀6) slepte epoxidem, soustředně.",
    "Základní deska L01: zašroubujte 3 stavitelné nohy M8 (matice z obou stran). Na desku položte 3 podložky G10 do vyznačených kružnic.",
    "Sloupy 40×80: do boční drážky (±y) zasuňte T-matice, přišroubujte úhelníky (M8×16) a úhelníky přišroubujte "
    "k L01 přes drážky (M8×25 + matice). Sloupy srovnejte do pravého úhlu (úhelník), dotáhněte.",
    "Horní deska L02: úhelníky na vnitřní stranu sloupů, deska na ně (M8×25 + matice přes drážky). "
    "Otvor ⌀14 musí být nad středem cely – srovnejte podle olovnice nebo trnu ⌀12 z pouzdra.",
    "Pouzdro P01 přišroubujte na L02 (4× M5×45), vložte igus RJ4JP-01-12, stáhněte svěrný šroub M4.",
    "Celu (s čidly bodu M) postavte na podložky G10 – kapsy ve dně na podložky; kontrola: cela se nedotýká desky.",
    "Invarový sloupek ⌀16 postavte do patky P04 (2× M5×20 do L01), sloupek stojí přímo na desce, svěrku dotáhněte. "
    "Nasaďte rameno P03 (terčík ve výšce horní hrany límce) a rameno P02 s LVDT.",
    "Písek nasypte a zhutněte po vrstvách (V02, postup), navrch položte píst, do otvoru ⌀6 kuličku 5/16\".",
    "Invarovou tyč zasuňte shora pouzdrem až na kuličku. Na tyč stavěcí kroužek, na něj nosná deska L03 a kotouče L06/L07. "
    f"Kroužek nastavte tak, aby nosná deska byla {p.C_TRAVEL + 10:g} mm nad horní hranou pouzdra (zdvih ±{p.C_TRAVEL:g}).",
    "LVDT posuňte ve svěrce P02, až je jádro uprostřed rozsahu (výstup ≈ 0 V), dotáhněte.",
    "Laser do držáku P05 (M5 do L02), kameru + RPi 5 do boxu P06/P07 (sklo do drážky, kabel přes PG7), box na závěs P08 (M5 do L02). "
    "Laser natočte, aby čáry ležely napříč přes celý povrch ⌀100; kameru zaostřete (zadní ohnisková vzdálenost).",
    "Slepá zkouška s hliníkovou atrapou (V02) → kalibrace podložkami → první cyklus.",
]


def main():
    L = ["# E7 – varianta C rev. B2: objednávka a sestavení", "",
         "Vše, co je potřeba koupit, nechat vyrobit podle rozměrů a sestavit. Sestava je navržená tak, aby **nebylo "
         "potřeba soustružit ani frézovat**: profily se jen řežou na délku, plechy se řežou laserem podle DXF, zbytek se "
         "tiskne. Výkresy: V01–V06 (`vykresy/E7_drawings.pdf`), výrobní soubory: `vyroba/laser` (DXF) a `vyroba/tisk` (STL/STEP).",
         "", "**Už máte:** CR1000, TDR100/200 + CS645, Pt100, optické vlákno + čtečku, truhlicový mrazák s regulátorem (E6).", "",
         f"Ceny: „ověřeno“ = nalezeno na webu prodejce v 10/2026 (ověřte před objednáním), „odhad/poptat“ = cenu je třeba zjistit. 1 € ≈ {EUR:g} Kč.", ""]
    for title, shop, rows in SHOPS:
        L += [f"## {title}", "", f"Kde: {shop}", "", "| položka | specifikace | ks | cena | stav |", "|---|---|---|---|---|"]
        for r in rows:
            L.append("| " + " | ".join(str(x) for x in r) + " |")
        L.append("")
    L += ["## Rozměry pro kontrolu (z modelu)", "",
          f"- sloupy {bp.COL_H:g} mm, Invarová tyč {bp.ROD_L} mm, Invarový sloupek {bp.POST_L:.0f} mm",
          f"- nosná deska závaží {bp.ZC - bp.ZB0:.0f} mm nad základní deskou; horní deska {bp.ZBEAM - bp.ZB0:.0f} mm",
          f"- kotouč {p.C_DISC_D:g} × {p.C_DISC_T:g} mm = {bp.disc_mass(bp.LASER[5]):.2f} kg, poloviční {bp.disc_mass(bp.LASER[6]):.2f} kg",
          "- kontrola kolizí v 3D sestavě (model3d.py): bez kolizí", "",
          "## Postup sestavení", ""]
    L += [f"{i}. {s}" for i, s in enumerate(ASSEMBLY, 1)]
    L += ["", "Celkem (V04): čidla a elektronika + mechanika ≈ 1 450–1 980 € bez DPH, tj. ≈ 36–50 tis. Kč.", ""]
    open(OUT, "w", encoding="utf-8").write("\n".join(L))
    print("ok", OUT)


if __name__ == "__main__":
    main()
