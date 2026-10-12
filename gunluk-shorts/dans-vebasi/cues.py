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

# Geçişler: (zaman, tür)   whip: yatay bulanık kaydırma, up: dikey, zoom: zoom-vuruş
TRANS = [(st("B") - 0.04, "whip"), (st("C") - 0.04, "zoom"), (st("D") - 0.04, "whip"), (st("E") - 0.04, "up"), (st("F") - 0.04, "whip"),
         (st("G") - 0.04, "zoom"), (st("H") - 0.04, "whip"), (st("I") - 0.04, "up"), (st("J") - 0.04, "whip"), (st("K") - 0.04, "zoom"),
         (st("L") - 0.04, "whip")]
TW = 0.17


def group_of(t):
    g = 0
    for tb, _ in TRANS:
        if t >= tb:
            g += 1
    return g


# Dansçı sayacı (HUD): (zaman, değer) anahtarları
def dancers(t):
    keys = [(0.0, 1), (wt("D", 2) - 0.02, 1), (wt("D", 2) + 0.30, 34), (wt("D", 7) - 0.02, 34), (wt("D", 7) + 0.55, 400),
            (wt("K", 3) - 0.05, 400), (wt("K", 4) + 0.35, 0), (wt("L", 2) + 0.05, 0), (wt("L", 2) + 0.35, 1), (T + 1, 1)]
    for (t0, v0), (t1, v1) in zip(keys[:-1], keys[1:]):
        if t < t1:
            if v1 >= v0:
                return int(round(lerp(v0, v1, ease_out(prog(t, t0, t1), 2))))
            return int(round(lerp(v0, v1, ease_io(prog(t, t0, t1)))))
    return 1


def crowd_n(t):
    """Meydandaki dansçı kuklası sayısı (görsel; sayaçtan bağımsız ölçekli)"""
    d = dancers(t)
    return d


FLASH = [(wt("A", 7), 0.25, 0.10), (wt("D", 7) + 0.1, 0.30, 0.12), (wt("F", 6), 0.30, 0.12), (st("K") - 0.04 + 0.17, 0.35, 0.12)]
SHAKES = [(wt("D", 7) + 0.1, 12, 0.3), (wt("F", 6), 10, 0.25), (wt("H", 3), 8, 0.3), (wt("I", 1), 14, 0.3)]
STAMPS = [(wt("C", 1) + 0.0, 0.8), (wt("I", 1) + 0.12, 1.0), (wt("B", 3), 0.7), (wt("F", 6), 0.7)]
POPS = [wt("D", 2), wt("D", 7), wt("F", 1), wt("K", 3)]
SILENCE_T = wt("K", 3) - 0.03     # müzik burada kesilir
SILENCE_END = wt("L", 0) - 0.05   # müziksiz sessizlik (yalnızca konuşma)


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
    return max(-30, min(30, dx)), max(-30, min(30, dy))
