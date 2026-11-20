#!/usr/bin/env python3
"""E7 – řízení obíhající kamery: Raspberry Pi Zero 2 W (krokový motor 28BYJ-48, optická koncovka, LED modul,
laser, topení hlavy s teploměrem) + Camera Module 3 Wide (ostří od 5 cm) + 5 teplotních sond DS18B20 ve vzorku. Vše se ovládá z počítače – přes webovou stránku nebo SSH.

Bez pájení a lepení: Raspberry Pi Zero 2 WH (s osazenou lištou) + svorkovnicový HAT (šroubovací svorky),
moduly s piny propojené kabely Dupont, prodloužení vodičů svorkami WAGO 221.

Zapojení (číslo GPIO → svorka HAT):
  ULN2003 IN1..IN4   GPIO5, GPIO6, GPIO13, GPIO19      deska ULN2003: +5 V, GND (motor se zasune do konektoru)
  optická koncovka   GPIO26 (signál), 3,3 V, GND          clona na náboji = výchozí poloha (rameno na −y)
  LED modul 3 W      GPIO27 (řídicí pin modulu), 5 V, GND
  relé 1 – laser     GPIO17                               laser 5 V přes kontakt relé (svorky)
  relé 2 – topení    GPIO23                               topné tělísko PTC 5 V v hlavě kamery přes kontakt relé
  teploměr DS18B20   GPIO4 (1-Wire), 3,3 V, GND           modul s rezistorem; v /boot/firmware/config.txt: dtoverlay=w1-gpio
  sondy T1–T5        na stejné sběrnici GPIO4             3 vodiče každé sondy do svorek WAGO 221 u modulu (VDD, GND, DQ)
  spouštění z CR850  GPIO22 přes modul optočlenu (aktivní v nule)

Použití (z počítače: ssh pi@e7-kamera … nebo prohlížeč http://e7-kamera:8080):
  python3 e7_kamera.py web            # webová stránka s tlačítky + stav (doporučeno, běží trvale – viz konec souboru)
  python3 e7_kamera.py test           # výchozí poloha, ±90°, zpět
  python3 e7_kamera.py laser          # jedna sada snímků ve výchozí poloze (LED / laser / tma)
  python3 e7_kamera.py orbit [krok]   # oběh −180 … +170° po `krok` stupních (výchozí 10), fotky s LED
  python3 e7_kamera.py run            # trvalý běh bez webu: pulsy z CR850 + oběh v časech ORBIT_AT + termostat
  python3 e7_kamera.py teploty        # vypíše adresy všech DS18B20 a teploty → doplnit HEAD_ID a PROFILE níže
                                      # (sondu po jedné ohřát v dlani a sledovat, které adrese stoupne teplota)

Data (≈ 5 GB/den): oběh 36 pozic × 2 ostření každé 3 h + sada laser/LED každých 10 min → karta 128 GB
a denně stáhnout do počítače, např. rsync -a pi@e7-kamera:e7/ D:/E7/ (spustit plánovačem na PC).

NEVYZKOUŠENO NA HARDWARU – první spuštění s rukou u napájení a s volně visícím kabelem.
"""
import csv
import datetime as dt
import glob
import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from gpiozero import DigitalInputDevice, OutputDevice

# --------------------------------------------------------------------------------------------- nastavení
PINS_COIL = (5, 6, 13, 19)
PIN_HOME, PIN_LED, PIN_LASER, PIN_HEAT, PIN_TRIG = 26, 27, 17, 23, 22
HOME_ACTIVE_HIGH = True                     # optická koncovka: clona ve štěrbině → 1 (u modulů s opačnou logikou False)
RELAY_ACTIVE_HIGH = False                   # běžné moduly relé spínají nulou
HALF_STEPS_MOTOR = 4076                     # 28BYJ-48: ≈ 4076 půlkroků na otáčku výstupní hřídele
GEAR = 72 / 12
STEPS_PER_DEG = HALF_STEPS_MOTOR * GEAR / 360.0   # ≈ 67,9 půlkroku na stupeň ramene
LIMIT_DEG = 180.0                           # kabel ve smyčce: nikdy dál než ±180° od výchozí polohy
STEP_DELAY = 0.002                          # s mezi půlkroky (pomaleji v mrazu)
BACKLASH_DEG = 3.0
SETTLE_S = 1.0
ORBIT_AT = tuple(f"{h:02d}:00" for h in range(0, 24, 3))   # oběh každé 3 h
HEAD_T = (5.0, 8.0)                         # termostat hlavy kamery: zapnout pod 5 °C, vypnout nad 8 °C
OUT = Path.home() / "e7"
STATE = OUT / "stav.json"
CAMERA = dict(exposure_us=20000, gain=1.0, lens_dioptre=8.0, colour_gains=(1.8, 1.6))   # 8 dpt ≈ 0,125 m
FOCUS_DPT = (1000 / 108, 1000 / 140)       # Camera Module 3 Wide: 2 polohy ostření (108 a 140 mm) → ostrý celý povrch
HEAD_ID = None                              # adresa DS18B20 v hlavě kamery, např. "28-3c01d607c1aa" (příkaz teploty)
PROFILE = {"T1": None, "T2": None, "T3": None, "T4": None, "T5": None}   # hloubky 10/30/50/70/90 mm
PROFILE_S = 60                              # zápis teplotního profilu každých 60 s do teploty.csv
HALF_SEQ = ((1, 0, 0, 0), (1, 1, 0, 0), (0, 1, 0, 0), (0, 1, 1, 0),
            (0, 0, 1, 0), (0, 0, 1, 1), (0, 0, 0, 1), (1, 0, 0, 1))
LOCK = threading.Lock()                     # jedna akce najednou (web, CR850, plán)


# --------------------------------------------------------------------------------------------- hardware
class Orbit:
    def __init__(self):
        self.coils = [OutputDevice(p) for p in PINS_COIL]
        self.home_sw = DigitalInputDevice(PIN_HOME, pull_up=not HOME_ACTIVE_HIGH)
        self.phase = 0
        self.pos = self._load()

    def _load(self):
        try:
            return json.loads(STATE.read_text())["deg"]
        except Exception:
            return None

    def _save(self):
        OUT.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps({"deg": self.pos, "cas": dt.datetime.now().isoformat(timespec="seconds")}))

    def at_home(self):
        return self.home_sw.is_active

    def _step(self, d):
        self.phase = (self.phase + d) % 8
        for c, v in zip(self.coils, HALF_SEQ[self.phase]):
            c.value = v
        time.sleep(STEP_DELAY)

    def release(self):
        for c in self.coils:
            c.off()

    def _move(self, n, stop_home=False):
        d = 1 if n > 0 else -1
        for i in range(abs(n)):
            self._step(d)
            if stop_home and self.at_home():
                return i + 1
        return None

    def home(self):
        first = -1 if (self.pos or 0) > 0 else 1
        found = None
        for d, span in ((first, 200), (-first, 400)):
            found = self._move(int(d * span * STEPS_PER_DEG), stop_home=True)
            if found:
                break
        if not found:
            self.release()
            raise RuntimeError("koncovka výchozí polohy nenalezena – zkontrolujte clonu a kabel")
        self._move(-int(5 * STEPS_PER_DEG))                     # odjet a najet znovu pomalu v kladném směru
        self._move(int(10 * STEPS_PER_DEG), stop_home=True)
        self.pos = 0.0
        self.release()
        self._save()

    def goto(self, deg):
        if self.pos is None:
            self.home()
        deg = max(-LIMIT_DEG, min(LIMIT_DEG, deg))
        if deg < self.pos:
            under = max(-LIMIT_DEG, deg - BACKLASH_DEG)
            self._move(int(round((under - self.pos) * STEPS_PER_DEG)))
            self.pos = under
        self._move(int(round((deg - self.pos) * STEPS_PER_DEG)))
        self.pos = deg
        self.release()
        self._save()


class Relay(OutputDevice):
    def __init__(self, pin):
        super().__init__(pin, active_high=RELAY_ACTIVE_HIGH, initial_value=False)


def w1_all():
    """Všechna čidla DS18B20 na sběrnici: {adresa: teplota °C}."""
    out = {}
    for f in sorted(glob.glob("/sys/bus/w1/devices/28-*/temperature")):
        try:
            out[Path(f).parent.name] = int(Path(f).read_text()) / 1000.0
        except Exception:
            out[Path(f).parent.name] = None
    return out


def profile_loop():
    """Teplotní profil T1–T5 (+ hlava) do teploty.csv každých PROFILE_S sekund."""
    f = OUT / "teploty.csv"
    while True:
        allt = w1_all()
        row = [dt.datetime.now().isoformat(timespec="seconds")] + [allt.get(PROFILE[k]) if PROFILE[k] else None
                                                                   for k in PROFILE] + [allt.get(HEAD_ID) if HEAD_ID else None]
        OUT.mkdir(parents=True, exist_ok=True)
        new = not f.exists()
        with f.open("a", newline="") as fh:
            w = csv.writer(fh)
            if new:
                w.writerow(["cas"] + [f"{k}_C" for k in PROFILE] + ["hlava_C"])
            w.writerow(row)
        time.sleep(PROFILE_S)


class Head:
    """Topení hlavy kamery (relé + PTC 5 V) a teploměr DS18B20 – termostat běží ve vlákně."""

    def __init__(self):
        self.heat = Relay(PIN_HEAT)
        self.t = None
        threading.Thread(target=self._loop, daemon=True).start()

    @staticmethod
    def read():
        allt = w1_all()
        if HEAD_ID:
            return allt.get(HEAD_ID)
        rest = [v for k, v in allt.items() if k not in PROFILE.values() and v is not None]
        return rest[0] if len(rest) == 1 else None               # dokud není HEAD_ID, jen při jediném volném čidle

    def _loop(self):
        while True:
            self.t = self.read()
            if self.t is None:
                self.heat.on()                                   # bez teploměru raději topit
            elif self.t < HEAD_T[0]:
                self.heat.on()
            elif self.t > HEAD_T[1]:
                self.heat.off()
            time.sleep(10)


class Cam:
    def __init__(self):
        from libcamera import controls
        from picamera2 import Picamera2
        self.cam = Picamera2()
        self.cam.configure(self.cam.create_still_configuration())
        self.cam.set_controls({"AeEnable": False, "AwbEnable": False,
                               "ExposureTime": CAMERA["exposure_us"], "AnalogueGain": CAMERA["gain"],
                               "ColourGains": CAMERA["colour_gains"],
                               "AfMode": controls.AfModeEnum.Manual, "LensPosition": CAMERA["lens_dioptre"]})
        self.cam.start()
        time.sleep(2)
        self.led, self.laser = OutputDevice(PIN_LED), Relay(PIN_LASER)

    def shot(self, path, led=False, laser=False, dpt=None):
        if dpt is not None:
            self.cam.set_controls({"LensPosition": dpt})
            time.sleep(0.5)
        self.led.value = led
        self.laser.value = laser
        time.sleep(0.3)
        self.cam.capture_file(str(path))
        self.led.off()
        self.laser.off()


def _folder():
    d = OUT / dt.date.today().isoformat()
    d.mkdir(parents=True, exist_ok=True)
    return d


def _log(row):
    f = OUT / "log.csv"
    new = not f.exists()
    with f.open("a", newline="") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["cas", "druh", "uhel_deg", "teplota_hlavy_C", "soubor"])
        w.writerow(row)


# --------------------------------------------------------------------------------------------- úlohy
def laser_set(orb, cam, head):
    with LOCK:
        orb.goto(0.0)
        time.sleep(SETTLE_S)
        t = dt.datetime.now().strftime("%H%M%S")
        for kind, led, las in (("led", True, False), ("laser", False, True), ("tma", False, False)):
            for k, d in enumerate(FOCUS_DPT if kind != "tma" else FOCUS_DPT[:1]):
                f = _folder() / f"{t}_{kind}_000_f{k}.jpg"
                cam.shot(f, led, las, dpt=d)
                _log([dt.datetime.now().isoformat(timespec="seconds"), kind, 0, head.t, f.name])


def orbit_set(orb, cam, head, step=10.0):
    with LOCK:
        orb.home()
        t = dt.datetime.now().strftime("%H%M%S")
        a = -LIMIT_DEG
        while a < LIMIT_DEG - 1e-6:
            orb.goto(a)
            time.sleep(SETTLE_S)
            for k, d in enumerate(FOCUS_DPT):
                f = _folder() / f"{t}_obeh_{a:+04.0f}_f{k}.jpg"
                cam.shot(f, led=True, dpt=d)
                _log([dt.datetime.now().isoformat(timespec="seconds"), "obeh", a, head.t, f.name])
            a += step
        orb.goto(0.0)


def scheduler(orb, cam, head):
    """Pulsy z CR850 → sada snímků ve výchozí poloze; oběh v časech ORBIT_AT."""
    trig = DigitalInputDevice(PIN_TRIG, pull_up=True)
    done = set()
    while True:
        if trig.wait_for_active(timeout=1.0):
            laser_set(orb, cam, head)
            trig.wait_for_inactive(timeout=10)
        now = dt.datetime.now()
        key = (now.date(), now.strftime("%H:%M"))
        if key[1] in ORBIT_AT and key not in done:
            done.add(key)
            orbit_set(orb, cam, head)


def _prof_text():
    allt = w1_all()
    return " / ".join("–" if not PROFILE[k] or allt.get(PROFILE[k]) is None else f"{allt[PROFILE[k]]:.1f}" for k in PROFILE) + " °C"


PAGE = """<!doctype html><html lang="cs"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>E7 kamera</title><style>body{{font:16px system-ui;margin:24px;max-width:640px}}button{{font:inherit;padding:8px 14px;
margin:4px}}td{{padding:2px 10px}}</style><h1>E7 – kamera</h1>
<table><tr><td>poloha ramene</td><td>{pos}</td></tr><tr><td>výchozí poloha (koncovka)</td><td>{home}</td></tr>
<tr><td>teplota hlavy</td><td>{t}</td></tr><tr><td>vzorek T1–T5 (10/30/50/70/90 mm)</td><td>{prof}</td></tr><tr><td>topení hlavy</td><td>{heat}</td></tr>
<tr><td>poslední snímek</td><td>{last}</td></tr><tr><td>stav</td><td>{busy}</td></tr></table>
<form method="post"><button name="a" value="home">Výchozí poloha</button><button name="a" value="laser">Sada laser + LED</button>
<button name="a" value="orbit">Oběh (36 snímků)</button><button name="a" value="test">Test ±90°</button>
<button name="a" value="led">LED 2 s</button><button name="a" value="las">Laser 2 s</button></form>
<p><a href="/">obnovit</a> · snímky v ~/e7 na RPi (sdílená složka nebo scp)</p></html>"""


def web(orb, cam, head, port=8080):
    def last():
        files = sorted(OUT.glob("*/*.jpg"))
        return files[-1].name if files else "–"

    class H(BaseHTTPRequestHandler):
        def _page(self):
            body = PAGE.format(pos="neznámá" if orb.pos is None else f"{orb.pos:+.1f}°", home="ano" if orb.at_home() else "ne",
                               t="–" if head.t is None else f"{head.t:.1f} °C", heat="zapnuto" if head.heat.value else "vypnuto",
                               last=last(), busy="pracuje…" if LOCK.locked() else "připraveno",
                               prof=_prof_text())
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body.encode())

        def do_GET(self):
            self._page()

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0))
            a = self.rfile.read(n).decode().partition("=")[2]
            jobs = {"home": lambda: (LOCK.acquire(), orb.home(), LOCK.release()),
                    "laser": lambda: laser_set(orb, cam, head), "orbit": lambda: orbit_set(orb, cam, head),
                    "test": lambda: [orb.goto(x) for x in (90, -90, 0)],
                    "led": lambda: (cam.led.on(), time.sleep(2), cam.led.off()),
                    "las": lambda: (cam.laser.on(), time.sleep(2), cam.laser.off())}
            if a in jobs and not LOCK.locked():
                threading.Thread(target=jobs[a], daemon=True).start()
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()

        def log_message(self, *a):
            pass

    threading.Thread(target=scheduler, args=(orb, cam, head), daemon=True).start()
    HTTPServer(("", port), H).serve_forever()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "web"
    if cmd == "teploty":
        names = {v: k for k, v in PROFILE.items() if v}
        if HEAD_ID:
            names[HEAD_ID] = "hlava"
        for k, v in w1_all().items():
            print(f"{k}  {v if v is None else round(v, 2)} °C  {names.get(k, '(nepřiřazeno)')}")
        return
    orb, head = Orbit(), Head()
    threading.Thread(target=profile_loop, daemon=True).start()
    try:
        if cmd == "test":
            orb.home()
            for a in (90, -90, 0):
                orb.goto(a)
                print("poloha", a, "°  koncovka:", orb.at_home(), " hlava:", head.read(), "°C")
                time.sleep(1)
            return
        cam = Cam()
        if cmd == "laser":
            laser_set(orb, cam, head)
        elif cmd == "orbit":
            orbit_set(orb, cam, head, float(sys.argv[2]) if len(sys.argv) > 2 else 10.0)
        elif cmd == "run":
            scheduler(orb, cam, head)
        elif cmd == "web":
            web(orb, cam, head)
        else:
            print(__doc__)
    finally:
        orb.release()


if __name__ == "__main__":
    main()

# Trvalý běh po zapnutí (jednou na RPi):  sudo nano /etc/systemd/system/e7.service
#   [Unit] Description=E7 kamera  After=network.target
#   [Service] User=pi  ExecStart=/usr/bin/python3 /home/pi/e7_kamera.py web  Restart=always
#   [Install] WantedBy=multi-user.target
# pak:  sudo systemctl enable --now e7
