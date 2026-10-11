"""Konuşma zamanlarından türetilen sahne/olay çizelgesi — görüntü ve ses aynı veriyi kullanır."""
import json, os
from engine import clamp, lerp, prog, ease_in, ease_out, ease_io

HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, "out", "timeline.json")))
T = TL["duration"]
S = {s["id"]: s for s in TL["sentences"]}


def st(sid):
    return S[sid]["t0"]


def en(sid):
    return S[sid]["t1"]


def wt(sid, i):
    return S[sid]["words"][i]["t0"]


def we(sid, i):
    return S[sid]["words"][i]["t1"]


FINAL_T = T - 0.1            # bu andan sonraki kareler 0. kareyle birebir aynı
CAP_END = T - 0.1

# Geçişler: (zaman, tür)   whip: yatay bulanık kaydırma, up: dikey, zoom: zoom-vuruş, slam: beyaz flaş vuruşu
TRANS = [(st("B") - 0.04, "whip"), (st("C") - 0.04, "up"), (st("D") - 0.04, "whip"), (st("E") - 0.04, "zoom"), (st("F") - 0.04, "whip"),
         (st("G") - 0.04, "whip"), (st("H") - 0.04, "zoom"), (st("I") - 0.04, "up"), (st("J") - 0.04, "whip"), (st("K") - 0.04, "slam")]
TW = 0.17  # geçiş yarı genişliği


def group_of(t):
    g = 0
    for tb, _ in TRANS:
        if t >= tb:
            g += 1
    return g


# Makineli tüfek / tüfek atışları: (başlangıç, atış sayısı, atış/sn)
BURSTS = [(wt("E", 5) + 0.10, 9, 14.0), (wt("E", 8) + 0.05, 12, 14.0),
          (st("F") + 0.55, 12, 14.0), (st("F") + 1.9, 14, 14.0), (st("F") + 3.3, 10, 14.0),
          (st("G") + 0.7, 12, 13.0), (st("G") + 1.9, 12, 13.0), (st("G") + 3.0, 8, 13.0)]
SHOTS = [b0 + k / r for (b0, n, r) in BURSTS for k in range(n)]


def firing(t, w=0.035):
    return any(0 <= t - s < w for s in SHOTS)


# Mermi sayacı (HUD): (zaman, değer) anahtar kareleri
AMMO_KEYS = [(wt("E", 6), 0), (st("F"), 700), (st("G"), 2900), (st("H"), 5400), (we("H", 4) - 0.05, 9100), (wt("I", 1) + 0.18, 9860)]
RESET0, RESET1 = 1.15, 1.70   # açılıştaki 9.860 → 0 geri sarma


def ammo(t):
    if t < RESET0:
        return 9860
    if t < RESET1:
        return int(9860 * (1 - ease_io(prog(t, RESET0, RESET1))))
    if t < AMMO_KEYS[0][0]:
        return 0
    for (t0, v0), (t1, v1) in zip(AMMO_KEYS[:-1], AMMO_KEYS[1:]):
        if t < t1:
            return int(lerp(v0, v1, ease_io(prog(t, t0, t1)) * 0.35 + prog(t, t0, t1) * 0.65))
    return 9860


# Flaş / sarsıntı olayları
FLASH = [(st("K") - 0.04 + 0.17, 0.85, 0.12), (wt("A", 8), 0.35, 0.10), (wt("I", 1) + 0.18, 0.5, 0.12), (wt("C", 1), 0.35, 0.10), (wt("K", 4), 0.5, 0.14)]
SHAKES = [(wt("A", 8), 16, 0.3), (wt("C", 1), 14, 0.25), (wt("I", 1) + 0.18, 14, 0.3), (wt("K", 4), 22, 0.4), (st("K") - 0.04 + 0.17, 20, 0.3)] + \
         [(s, 4.0, 0.08) for s in SHOTS]
STAMPS = [(wt("C", 1), 0.9), (wt("B", 4), 0.7), (wt("I", 1) + 0.18, 1.0), (wt("K", 4), 1.2), (wt("A", 8), 0.8)]
POPS = [wt("A", 2), wt("D", 2), wt("E", 6), wt("I", 4), wt("I", 10)]


def flash_alpha(t):
    a = 0.0
    for t0, s, d in FLASH:
        if t >= t0:
            a = max(a, s * (2.718281828 ** (-(t - t0) / d)))
    return a if a > 0.01 else 0.0


def shake(t):
    import math
    dx = dy = 0.0
    for t0, amp, dec in SHAKES:
        u = t - t0
        if 0 <= u < dec * 6:
            e = amp * math.exp(-u / dec)
            dx += e * math.sin(u * 109.0 + t0 * 3)
            dy += e * math.cos(u * 83.0 + t0 * 5)
    return max(-40, min(40, dx)), max(-40, min(40, dy))
