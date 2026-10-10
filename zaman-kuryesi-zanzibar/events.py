"""Görüntü ve sesin ortak kullandığı zaman çizelgesi (tek doğruluk kaynağı)."""
import math

from engine import clamp, ease_in, ease_io, ease_out, lerp, prog, rng_hash

# ───────── liman sahnesi geometrisi (dünya koordinatları) ─────────
PAL = dict(ox=560.0, oy=960.0, s=0.95)
SHIPS = [(690.0, 1335.0, 0.96), (300.0, 1240.0, 0.86), (520.0, 1150.0, 0.74), (310.0, 1075.0, 0.64), (560.0, 1002.0, 0.55)]
SULTAN = (880.0, 1175.0, 0.86)
TARGETS = [(-160, -150), (100, -132), (-20, -240), (180, -150), (-100, -60), (40, -80), (-210, -110), (140, -260)]

SHIP_IN0 = 11.15  # ilk geminin kayma başlangıcı
SHIP_STEP = 0.28
SHIP_SLIDE = 1.5

WHIPS = [6.0, 11.0, 32.0, 35.0]
WHIP_HALF = 0.18


def palace_pt(lx, ly):
    return PAL["ox"] + lx * PAL["s"], PAL["oy"] + ly * PAL["s"]


def ship_x_off(i, t):
    """Gemi i'nin yatay kayma ofseti (sahneye soldan girerken)"""
    a = SHIP_IN0 + SHIP_STEP * i
    return -(1 - ease_out(prog(t, a, a + SHIP_SLIDE), 3)) * 1000.0


def ship_pose(i, t):
    x, y, s = SHIPS[i]
    bob = math.sin(t * 1.7 + i * 1.3) * 5 * s
    rot = math.sin(t * 1.2 + i * 0.9) * 1.1
    return x + ship_x_off(i, t), y + bob, s, rot


def muzzle(i, gun, t, recoil=0.0):
    from art import ship_gun_tips  # geç içe aktarma (döngüsel bağımlılığı önler)
    x, y, s, rot = ship_pose(i, t)
    tips = ship_gun_tips(x, y, s, rot=rot, angs=(-24, -24), recoil=(recoil, recoil))
    return tips[gun]


# ───────── bombardıman çizelgesi ─────────
def _barrage():
    shots = []  # dict(t, ship, gun, tx, ty, flight, kind, size)
    for i in range(5):  # 20.0'da dev salvo
        lx, ly = TARGETS[(i * 2 + 1) % len(TARGETS)]
        shots.append(dict(t=20.0 + 0.025 * i, ship=i, gun=0, target=palace_pt(lx, ly), flight=0.66 + 0.03 * i, kind="palace", size=1.25))
    t, k = 20.9, 0
    order = [2, 0, 4, 1, 3, 0, 2, 4, 1, 3]
    while t < 27.35:
        lx, ly = TARGETS[(k * 3 + 1) % len(TARGETS)]
        shots.append(dict(t=t, ship=order[k % len(order)], gun=(k // 2) % 2, target=palace_pt(lx, ly),
                          flight=0.52 + 0.08 * (k % 3), kind="palace", size=1.0 + 0.15 * (k % 3)))
        t += lerp(0.62, 0.27, prog(t, 20.9, 27.4))
        k += 1
    # sultanın gemisine üç isabet (24.05 / 24.40 / 24.75)
    sx, sy, ss = SULTAN
    for j, (tf, sh) in enumerate(((23.45, 0), (23.80, 1), (24.15, 2))):
        shots.append(dict(t=tf, ship=sh, gun=1, target=(sx + (j - 1) * 55, sy - 30), flight=0.60, kind="sultan", size=1.15))
    shots.sort(key=lambda d: d["t"])
    return shots


SHOTS = _barrage()
for _s in SHOTS:
    _s["t_hit"] = _s["t"] + _s["flight"]
IMPACTS = [dict(t=s["t_hit"], x=s["target"][0], y=s["target"][1], size=s["size"], kind=s["kind"]) for s in SHOTS]
IMPACTS.append(dict(t=27.95, x=palace_pt(150, -330)[0], y=palace_pt(150, -330)[1], size=1.7, kind="palace"))  # son büyük patlama
IMPACTS.sort(key=lambda d: d["t"])
PALACE_HITS = [i["t"] for i in IMPACTS if i["kind"] == "palace"]
SULTAN_HIT0 = 24.05


def palace_dmg(t):
    n = 0.0
    for th in PALACE_HITS:
        n += smooth_step(prog(t, th, th + 0.35))
    return clamp(n / 14.0)


def smooth_step(x):
    return x * x * (3 - 2 * x)


def sultan_sink(t):
    """0..1 batma ilerlemesi"""
    return ease_io(prog(t, SULTAN_HIT0 + 0.15, 27.5))


# ───────── savaş saati (saniye cinsinden) ─────────
T_FREEZE = 29.2
T_REWIND0, T_REWIND1 = 40.35, 41.25


def war_sec(t):
    if t < 16.35:
        return 0.0
    if t < 18.7:
        return 120.0 * ease_io(prog(t, 16.35, 18.7))
    if t < 20.0:
        return 120.0
    if t < 28.0:
        return 120.0 + (1800.0 - 120.0) * prog(t, 20.0, 28.0) ** 1.15
    if t < T_FREEZE:
        return 1800.0 + 480.0 * ease_out(prog(t, 28.0, T_FREEZE), 2)
    if t < T_REWIND0:
        return 2280.0
    if t < T_REWIND1:
        return 2280.0 * (1 - ease_io(prog(t, T_REWIND0, T_REWIND1)))
    return 0.0


def hud_mode(t):
    if t < 16.35 or t >= T_REWIND1:
        return "idle"
    if t < T_FREEZE:
        return "run"
    if t < T_REWIND0:
        return "frozen"
    return "rewind"


# ───────── dünya saati (08:59 → 09:02) ─────────
def world_time(t):
    """(saat, dakika, saniye) — sahne 4/5'teki büyük saat. 11.0'de 08:58:55 → 16.0'de 09:00:00 → 18.7'de 09:02:00"""
    if t < 16.0:
        total = 8 * 3600 + 58 * 60 + 55 + (t - 11.0)
    else:
        total = 9 * 3600 + 120.0 * ease_io(prog(t, 16.35, 18.7))
    return total


# ───────── tıkırtı çizelgesi ─────────
def tick_times():
    ts = [float(k) for k in range(0, 16)]  # 0..15
    # sahne 6: hızlanan tıkırtı (20.45 → 27.95)
    t, g = 20.45, 0.5
    while t < 27.96:
        ts.append(round(t, 4))
        g = lerp(0.5, 0.085, prog(t, 20.45, 27.9) ** 0.8)
        t += g
    ts += [float(k) for k in range(32, 42)]  # 32..41  (42 ≡ 0: döngüde bağlanır)
    return ts


# ───────── flaş ve sarsıntı ─────────
FLASH = [(3.78, 0.35, 0.10), (7.30, 0.85, 0.16), (20.00, 0.92, 0.10), (27.95, 0.60, 0.16), (30.12, 0.85, 0.20),
         (37.55, 0.45, 0.14), (39.32, 0.45, 0.14), (6.0 + 0.18, 0.30, 0.08), (11.0 + 0.18, 0.30, 0.08),
         (32.0 + 0.18, 0.30, 0.08), (35.0 + 0.18, 0.30, 0.08)]


def flash_alpha(t):
    a = 0.0
    for t0, s, d in FLASH:
        if t >= t0:
            a = max(a, s * math.exp(-(t - t0) / d))
    return a if a > 0.01 else 0.0


def _shake_list():
    L = [(3.78, 9, 0.18), (7.30, 24, 0.25), (20.0, 46, 0.55), (27.95, 36, 0.5), (30.12, 30, 0.38), (37.0, 9, 0.2), (39.32, 20, 0.3)]
    for s in SHOTS:
        L.append((s["t"], 6.0, 0.13))
    for im in IMPACTS:
        L.append((im["t"], 15.0 * im["size"], 0.22))
    return L


SHAKES = _shake_list()


def shake(t):
    dx = dy = 0.0
    for t0, amp, dec in SHAKES:
        u = t - t0
        if 0 <= u < dec * 6:
            e = amp * math.exp(-u / dec)
            dx += e * math.sin(u * 109.0 + t0 * 3)
            dy += e * math.cos(u * 83.0 + t0 * 5)
    lim = 60
    return max(-lim, min(lim, dx)), max(-lim, min(lim, dy))


# ───────── ses olayları (görselle aynı zamanlarda) ─────────
WHOOSH = [3.0, 6.0 - 0.15, 11.0 - 0.15, 32.0 - 0.15, 35.0 - 0.15]
STAMPS = [(7.30, 0.9), (30.12, 1.2), (39.32, 0.8)]  # (zaman, güç): ağır darbe
POPS = [3.78, 4.55]  # zarf/soru işareti "pop"ları
HORSE_T0, HORSE_T1 = 35.0, 37.6
DING_T = 41.42
SILENCE = (16.0, 20.0)
BIG_HIT = 20.0
