"""E7 – offline package for people without Claude: everything opens from a local folder in any browser.

Builds sdileni/ with
  E7_podklady.html   overview page, drawings embedded (no internet needed except web fonts)
  E7_model_3D.html   animated 3D model, three.js inlined (works offline)
  E7_vykresy.pdf     drawings V01–V05
  cad/, 3d/          DXF of the cell, STEP of the rig (Onshape)
and zips it to sdileni/E7_podklady.zip.

Run after sim_thaw.py and vykresy_c.py:  python src/build_offline.py
"""
import base64
import os
import shutil
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
WEB = os.path.join(ROOT, "web")
OUT = os.path.join(ROOT, "sdileni")
MODEL_URL = "https://claude.ai/artifact/MWEEN9zQqwWQfuePCFbiCd"
CDN = {
    "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js": "three-r128.min.js",
    "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js": "OrbitControls-r128.js",
}
EXTRA = [("vykresy/E7_drawings.pdf", "E7_vykresy.pdf"),
         ("cad/E7_V04_cell.dxf", "cad/E7_V04_cell.dxf"),
         ("3d/E7_V01_variant_C.step", "3d/E7_V01_variant_C.step"),
         ("3d/E7_V03_cell.step", "3d/E7_V03_cell.step"),
         ("3d/E7_V05_freezer_layout.step", "3d/E7_V05_freezer_layout.step")]


def read(p):
    return open(p, encoding="utf-8").read()


def page(body):
    """The published pages have no skeleton of their own; give the local copy one."""
    if body.lstrip().lower().startswith("<!doctype"):
        return body
    return ('<!doctype html>\n<html lang="cs">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n</head>\n<body>\n'
            + body + "\n</body>\n</html>\n")


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    # 3D model: inline three.js so it runs without internet
    html = read(os.path.join(WEB, "E7_thaw_3d.html"))
    for url, fn in CDN.items():
        tag = f'<script src="{url}"></script>'
        assert tag in html, tag
        js = read(os.path.join(WEB, "vendor", fn)).replace("</script", "<\\/script")
        html = html.replace(tag, f"<script>\n{js}\n</script>")
    open(os.path.join(OUT, "E7_model_3D.html"), "w", encoding="utf-8").write(html)
    # overview: embed drawings, point the model card at the local file
    html = read(os.path.join(WEB, "E7_podklady.html"))
    for fn in sorted(os.listdir(os.path.join(ROOT, "vykresy"))):
        if fn.startswith("E7-V0") and fn.endswith(".png"):
            b64 = base64.b64encode(open(os.path.join(ROOT, "vykresy", fn), "rb").read()).decode("ascii")
            html = html.replace(f'"vykresy/{fn}"', f'"data:image/png;base64,{b64}"')
    assert MODEL_URL in html
    html = html.replace(MODEL_URL, "E7_model_3D.html")
    html = html.replace(" target=\"_blank\" rel=\"noopener\"><img", "><img")      # images: no new tab for data URIs
    html = html.replace("Kliknutím otevřete list v plném rozlišení.", "Výkresy v plném rozlišení jsou v souboru E7_vykresy.pdf.")
    html = html.replace('<footer>', '<footer>Balíček obsahuje: E7_model_3D.html (3D model), E7_vykresy.pdf, cad/ (DXF cely), '
                        '3d/ (STEP pro Onshape). ')
    open(os.path.join(OUT, "E7_podklady.html"), "w", encoding="utf-8").write(page(html))
    for src, dst in EXTRA:
        os.makedirs(os.path.dirname(os.path.join(OUT, dst)) or OUT, exist_ok=True)
        shutil.copy(os.path.join(ROOT, src), os.path.join(OUT, dst))
    open(os.path.join(OUT, "PRECTI_ME.txt"), "w", encoding="utf-8").write(
        "Experiment E7 – varianta C\n\n"
        "Otevřete E7_podklady.html v libovolném prohlížeči (dvojklik).\n"
        "3D model mrznutí a tání: E7_model_3D.html (funguje i bez internetu).\n"
        "Výkresy: E7_vykresy.pdf. CAD: cad/E7_V04_cell.dxf, 3D: 3d/*.step (Onshape, SolidWorks, FreeCAD).\n")
    zp = os.path.join(OUT, "E7_podklady.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for d, _, fs in os.walk(OUT):
            for f in fs:
                p = os.path.join(d, f)
                if p != zp:
                    z.write(p, os.path.join("E7_podklady", os.path.relpath(p, OUT)))
    return zp


if __name__ == "__main__":
    zp = build()
    for f in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, f)
        print(f, os.path.getsize(p) if os.path.isfile(p) else "dir")
