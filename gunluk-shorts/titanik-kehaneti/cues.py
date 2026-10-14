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

# Geçişler
TRANS = [(st("B") - 0.04, "whip"), (st("C") - 0.04, "zoom"), (st("D") - 0.04, "whip"), (st("E") - 0.04, "up"), (st("G") - 0.04, "whip"),
         (st("H") - 0.04, "up"), (st("I") - 0.04, "zoom"), (st("J") - 0.04, "zoom"), (st("K") - 0.04, "whip"),
         (st("L") - 0.04, "zoom")]
TW = 0.17


def group_of(t):
    g = 0
    for tb, _ in TRANS:
        if t >= tb:
            g += 1
    return g


# Benzerlik sayacı (HUD): açılışta 5/5 (spoiler), 1.2-1.7 sn'de 0'a sarar, anlatımda 1..5 olur
RESET0, RESET1 = 1.15, 1.65
SIM_T = [wt("D", 4), wt("E", 4), wt("G", 3), wt("H", 3), wt("I", 5)]


def sims(t):
    if t < RESET0:
        return 5.0
    if t < RESET1:
        return 5.0 * (1 - ease_io(prog(t, RESET0, RESET1)))
    n = 0
    for k, ts in enumerate(SIM_T):
        if t >= ts:
            n = k + 1
    return float(n)


FLASH = [(wt("E", 4), 0.55, 0.14), (wt("I", 5), 0.45, 0.12), (wt("J", 4), 0.45, 0.14), (st("L") - 0.04 + 0.17, 0.3, 0.12), (wt("A", 9), 0.25, 0.1)]
SHAKES = [(wt("E", 4), 20, 0.4), (wt("I", 5), 14, 0.3), (wt("J", 4), 16, 0.35), (st("L") - 0.04 + 0.17, 10, 0.25), (wt("D", 4), 8, 0.2)]
STAMPS = [(wt("D", 4), 0.9), (wt("J", 4), 1.0), (wt("I", 5), 1.0), (wt("G", 5), 0.8)]
CHECKS = SIM_T


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
