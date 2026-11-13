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
    w = S[sid]["words"]
    return w[min(i, len(w) - 1)]["t0"]


def we(sid, i):
    w = S[sid]["words"]
    return w[min(i, len(w) - 1)]["t1"]


FINAL_T = T - 0.1            # bu andan sonraki kareler 0. kareyle birebir aynı
CAP_END = T - 0.1

# Sahne grupları: (ilk cümle, ...) — grup değişiminde geçiş yapılır
GROUPS = [["A1"], ["A2"], ["A3"], ["B1"], ["B2", "B3"], ["C1", "C2", "C3"], ["D0", "D1", "D2", "D3", "D4", "D5"],
          ["E1"], ["E2"], ["E3"], ["F1"], ["F2"], ["G1", "G2"], ["G3"], ["G4"], ["H1", "H2"]]
KINDS = ["whip", "zoom", "up", "whip", "zoom", "whip", "up", "whip", "zoom", "up", "whip", "zoom", "up", "whip", "zoom"]
TRANS = [(st(g[0]) - 0.04, k) for g, k in zip(GROUPS[1:], KINDS)]
TW = 0.17

# vurgu rengi (altyazı): grup başına
GOLD_C, SPICE_C, YEL_C = (255, 199, 90), (110, 215, 255), (255, 228, 92)
EMPH = [GOLD_C, GOLD_C, GOLD_C, SPICE_C, SPICE_C, YEL_C, GOLD_C, GOLD_C, GOLD_C, YEL_C, GOLD_C, SPICE_C, GOLD_C, GOLD_C, GOLD_C, GOLD_C]


def group_of(t):
    g = 0
    for tb, _ in TRANS:
        if t >= tb:
            g += 1
    return g


def emph_color(t):
    return EMPH[group_of(t)]


# KANIT sayacı (HUD): kartta "?", D0'dan itibaren 0/5 → 5/5, kapanışta tekrar "?"
def kanit(t):
    if t < st("D0"):
        return None
    n = 0
    for k, sid in enumerate(("D1", "D2", "D3", "D4", "D5")):
        if t >= wt(sid, 0) + 0.25:
            n = k + 1
    if t >= st("H2") - 0.04 + 0.17:
        return None
    return n


# Dönüm anları
FLASH = [(wt("A3", 13), 0.28, 0.12), (wt("G2", 5), 0.30, 0.12), (st("H2") - 0.04 + 0.17, 0.30, 0.12)]
SHAKES = [(wt("A3", 13) + 0.05, 10, 0.25), (wt("G2", 5), 12, 0.3), (st("H2") - 0.04 + 0.17, 10, 0.25)]
PULSES = [wt("D1", 6), wt("D2", 3), wt("D3", 0), wt("D4", 0), wt("D5", 0)]
# Kamera itişleri (zoom nabzı): (an, genlik) — yalnız vurgu anlarında; compose.drift() uygular
PUNCHES = [(wt("E2", 2) - 0.02, 0.022), (wt("E2", 5) - 0.02, 0.020), (wt("H1", 7) - 0.02, 0.022)]


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
