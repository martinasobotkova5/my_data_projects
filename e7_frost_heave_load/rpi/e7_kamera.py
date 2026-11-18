#!/usr/bin/env python3
"""E7 – řízení obíhající kamery na Raspberry Pi 5 (krokový motor 28BYJ-48 přes ULN2003, Hall senzor, LED, laser).

Jedno RPi dělá všechno: točí ramenem, rozsvěcí LED / laser a fotí Camera Module 3. Arduino není potřeba – kroky
se jen počítají, přesnost polohy na časování nezávisí (Python stačí na ≈ 600 půlkroků / s).

Zapojení (fyzické piny RPi 5):
  ULN2003 IN1..IN4  GPIO5 (29), GPIO6 (31), GPIO13 (33), GPIO19 (35); deska ULN2003: +5 V (pin 2), GND (pin 6)
  Hall A3144        GPIO26 (37), napájení 3,3 V (pin 1), GND; výstup s otevřeným kolektorem → interní pull-up
  LED 1 W (MOSFET)  GPIO27 (13)        laser (MOSFET) GPIO17 (11)
  spouštění CR850   GPIO22 (15) přes optočlen (aktivní v nule)

Použití:
  python3 e7_kamera.py test           # najede na výchozí polohu, ±90°, zpět – kontrola kabelu a senzoru
  python3 e7_kamera.py home           # jen výchozí poloha
  python3 e7_kamera.py laser          # jedna sada snímků ve výchozí poloze (LED / laser / tma)
  python3 e7_kamera.py orbit [krok]   # oběh −180 … +170° po `krok` stupních (výchozí 10), fotky s LED
  python3 e7_kamera.py run            # trvalý běh: každý puls z CR850 = sada „laser“; oběh v časech ORBIT_AT

Stav (poslední poloha ramene) se ukládá do ~/e7/stav.json, aby se po restartu kabel nenavíjel dál.
NEVYZKOUŠENO NA HARDWARU – první spuštění dělat s rukou u napájení a s volně visícím kabelem.
"""
import csv
import datetime as dt
import json
import sys
import time
from pathlib import Path

from gpiozero import DigitalInputDevice, OutputDevice

# --------------------------------------------------------------------------------------------- nastavení
PINS_COIL = (5, 6, 13, 19)
PIN_HALL, PIN_LED, PIN_LASER, PIN_TRIG = 26, 27, 17, 22
HALF_STEPS_MOTOR = 4076                     # 28BYJ-48: ≈ 4076 půlkroků na otáčku výstupní hřídele (převod 63,68)
GEAR = 72 / 12                              # věnec / pastorek
STEPS_PER_DEG = HALF_STEPS_MOTOR * GEAR / 360.0   # ≈ 67,9 půlkroku na stupeň ramene
LIMIT_DEG = 180.0                           # kabel ve smyčce: rameno nikdy dál než ±180° od výchozí polohy
STEP_DELAY = 0.0016                         # s mezi půlkroky (≈ 1,5 °/s ramene); v mrazu raději pomaleji
BACKLASH_DEG = 3.0                          # cíl se najíždí vždy zespodu (+) – vymezí vůli převodovky
SETTLE_S = 1.0                              # uklidnění ramene před snímkem
ORBIT_AT = ("06:00", "18:00")               # kdy v režimu `run` udělat oběh (např. konec mrznutí / tání)
OUT = Path.home() / "e7"
STATE = OUT / "stav.json"
CAMERA = dict(exposure_us=20000, gain=1.0, lens_dioptre=7.6,   # 7,6 dpt ≈ ostření na 0,13 m (okénko – střed vzorku)
              colour_gains=(1.8, 1.6))
HALF_SEQ = ((1, 0, 0, 0), (1, 1, 0, 0), (0, 1, 0, 0), (0, 1, 1, 0),
            (0, 0, 1, 0), (0, 0, 1, 1), (0, 0, 0, 1), (1, 0, 0, 1))


# --------------------------------------------------------------------------------------------- hardware
class Orbit:
    def __init__(self):
        self.coils = [OutputDevice(p) for p in PINS_COIL]
        self.hall = DigitalInputDevice(PIN_HALL, pull_up=True)       # A3144: u magnetu = 0 → is_active
        self.phase = 0
        self.pos = self._load()                                      # stupně od výchozí polohy (None = neznámo)

    def _load(self):
        try:
            return json.loads(STATE.read_text())["deg"]
        except Exception:
            return None

    def _save(self):
        OUT.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps({"deg": self.pos, "cas": dt.datetime.now().isoformat(timespec="seconds")}))

    def _step(self, direction):
        self.phase = (self.phase + direction) % 8
        for c, v in zip(self.coils, HALF_SEQ[self.phase]):
            c.value = v
        time.sleep(STEP_DELAY)

    def release(self):
        for c in self.coils:                                         # cívky vypnout – převod drží, motor nehřeje
            c.off()

    def _move_steps(self, n, stop_on_hall=False):
        d = 1 if n > 0 else -1
        for i in range(abs(n)):
            self._step(d)
            if stop_on_hall and self.hall.is_active:
                return i + 1
        return None

    def home(self):
        """Najde magnet: hledá směrem k výchozí poloze podle uloženého stavu, nakonec vždy najíždí v kladném směru."""
        first = -1 if (self.pos or 0) > 0 else 1
        found = None
        for d, span in ((first, 200), (-first, 400)):
            found = self._move_steps(int(d * span * STEPS_PER_DEG), stop_on_hall=True)
            if found:
                break
        if not found:
            self.release()
            raise RuntimeError("Hall senzor nenalezen – zkontrolujte magnet, senzor a kabel")
        self._move_steps(-int(5 * STEPS_PER_DEG))                     # odjet a najet znovu zespodu (+) pomalu
        self._move_steps(int(10 * STEPS_PER_DEG), stop_on_hall=True)
        self.pos = 0.0
        self.release()
        self._save()

    def goto(self, deg):
        if self.pos is None:
            self.home()
        deg = max(-LIMIT_DEG, min(LIMIT_DEG, deg))
        if deg < self.pos:                                           # dolů s přejetím, pak nahoru – vůle vymezena
            under = max(-LIMIT_DEG, deg - BACKLASH_DEG)
            self._move_steps(int(round((under - self.pos) * STEPS_PER_DEG)))
            self.pos = under
        self._move_steps(int(round((deg - self.pos) * STEPS_PER_DEG)))
        self.pos = deg
        self.release()
        self._save()


class Cam:
    def __init__(self):
        from picamera2 import Picamera2
        from libcamera import controls
        self.cam = Picamera2()
        self.cam.configure(self.cam.create_still_configuration())
        self.cam.set_controls({"AeEnable": False, "AwbEnable": False,
                               "ExposureTime": CAMERA["exposure_us"], "AnalogueGain": CAMERA["gain"],
                               "ColourGains": CAMERA["colour_gains"],
                               "AfMode": controls.AfModeEnum.Manual, "LensPosition": CAMERA["lens_dioptre"]})
        self.cam.start()
        time.sleep(2)
        self.led, self.laser = OutputDevice(PIN_LED), OutputDevice(PIN_LASER)

    def shot(self, path, led=False, laser=False):
        self.led.value, self.laser.value = led, laser
        time.sleep(0.25)
        meta = self.cam.capture_file(str(path))
        self.led.off(); self.laser.off()
        return meta


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
            w.writerow(["cas", "druh", "uhel_deg", "soubor"])
        w.writerow(row)


# --------------------------------------------------------------------------------------------- úlohy
def laser_set(orb, cam):
    """Ve výchozí poloze: LED (fotka povrchu), laser (výška), tma (pozadí)."""
    orb.goto(0.0)
    time.sleep(SETTLE_S)
    t = dt.datetime.now().strftime("%H%M%S")
    for kind, led, las in (("led", True, False), ("laser", False, True), ("tma", False, False)):
        f = _folder() / f"{t}_{kind}_000.jpg"
        cam.shot(f, led, las)
        _log([dt.datetime.now().isoformat(timespec="seconds"), kind, 0, f.name])


def orbit_set(orb, cam, step=10.0):
    """Oběh pro 3D model: −180 … +180 − krok, s LED; na konci zpět do výchozí polohy."""
    orb.home()
    t = dt.datetime.now().strftime("%H%M%S")
    a = -LIMIT_DEG
    while a < LIMIT_DEG - 1e-6:
        orb.goto(a)
        time.sleep(SETTLE_S)
        f = _folder() / f"{t}_obeh_{a:+04.0f}.jpg"
        cam.shot(f, led=True)
        _log([dt.datetime.now().isoformat(timespec="seconds"), "obeh", a, f.name])
        a += step
    orb.goto(0.0)


def run(orb, cam):
    trig = DigitalInputDevice(PIN_TRIG, pull_up=True)                # optočlen sepne → 0 → is_active
    done = set()
    orb.home()
    while True:
        if trig.wait_for_active(timeout=1.0):
            laser_set(orb, cam)
            trig.wait_for_inactive(timeout=10)
        now = dt.datetime.now()
        key = (now.date(), now.strftime("%H:%M"))
        if key[1] in ORBIT_AT and key not in done:
            done.add(key)
            orbit_set(orb, cam)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "test"
    orb = Orbit()
    try:
        if cmd == "home":
            orb.home()
        elif cmd == "test":
            orb.home()
            for a in (90, -90, 0):
                orb.goto(a)
                print("poloha", a, "°  Hall:", orb.hall.is_active)
                time.sleep(1)
        else:
            cam = Cam()
            if cmd == "laser":
                laser_set(orb, cam)
            elif cmd == "orbit":
                orbit_set(orb, cam, float(sys.argv[2]) if len(sys.argv) > 2 else 10.0)
            elif cmd == "run":
                run(orb, cam)
            else:
                print(__doc__)
    finally:
        orb.release()


if __name__ == "__main__":
    main()
