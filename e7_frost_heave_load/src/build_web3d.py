"""E7 – 3D stránka sestavy (fáze 1 s obíhající kamerou / fáze 2 se zátěží).

  web/E7_sestava_3D.html          pro claude.ai (knihovna three.js z CDN)
  web/E7_sestava_3D_offline.html  jeden soubor ke sdílení: three.js i modely jsou uvnitř, funguje bez internetu
                                  (stačí poslat e-mailem / přes Teams / OneDrive a otevřít dvojklikem v prohlížeči)

Run: python build_web3d.py   (po python model3d.py, který vyrobí 3d/E7_V07_bez_zatizeni.glb a 3d/E7_sestava_final.glb)
"""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(HERE, "..", "web")
D3 = os.path.join(HERE, "..", "3d")
CDN = {
    "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js": "three-0.128.0.min.js",
    "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js": "OrbitControls-0.128.0.js",
    "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js": "GLTFLoader-0.128.0.js",
}


def b64(fn):
    return base64.b64encode(open(os.path.join(D3, fn), "rb").read()).decode()


def main():
    t = open(os.path.join(WEB, "rig_3d_template.html"), encoding="utf-8").read()
    t = t.replace("/*__GLB_U__*/", b64("E7_V07_bez_zatizeni.glb")).replace("/*__GLB_C__*/", b64("E7_sestava_final.glb"))
    open(os.path.join(WEB, "E7_sestava_3D.html"), "w", encoding="utf-8").write(t)
    off = t
    for url, fn in CDN.items():
        js = open(os.path.join(WEB, "lib", fn), encoding="utf-8").read().replace("</script", "<\\/script")
        tag = f'<script src="{url}"></script>'
        assert tag in off, url
        off = off.replace(tag, f"<script>/* {fn} (MIT, three.js authors) */\n{js}\n</script>")
    off = ('<!doctype html>\n<html lang="cs">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n</head>\n<body>\n'
           + off + "\n</body>\n</html>\n")
    open(os.path.join(WEB, "E7_sestava_3D_offline.html"), "w", encoding="utf-8").write(off)
    for fn in ("E7_sestava_3D.html", "E7_sestava_3D_offline.html"):
        print(fn, f"{os.path.getsize(os.path.join(WEB, fn)) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
