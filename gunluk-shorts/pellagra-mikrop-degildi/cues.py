"""Konuşma zamanlarından türetilen sahne/olay çizelgesi — görüntü ve ses aynı veriyi kullanır (Anayasa: tek zaman kaynağı)."""
import json, math, os
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


def nw(sid):
    return len(S[sid]["words"])


FINAL_T = T - 0.1            # bu andan sonraki kareler 0. kareyle birebir aynı
CAP_END = T - 0.1

# Sahne grupları: grup değişiminde geçiş yapılır
GROUPS = [["A1", "A2"], ["B1"], ["B2"], ["B3"], ["C1", "C2"], ["D0", "D1"], ["D2", "D3", "D4"], ["E0", "E0b"], ["E1", "E2", "E2b"],
          ["E3", "E4"], ["F1", "F2"], ["F3", "F4", "F4b"], ["F5"], ["G1"]]
NAMES = ["hook", "guney", "belirti", "mikrop", "yetimhane", "kuskucu", "kirli_parti", "tabak", "diyet", "hapishane", "niasin", "misir",
         "gemi", "kapanis"]
KINDS = ["whip", "up", "whip", "whip", "up", "zoom", "whip", "zoom", "up", "whip", "up", "whip", "zoom"]
TRANS = [(st(g[0]) - 0.04, k) for g, k in zip(GROUPS[1:], KINDS)]
TW = 0.17


def group_of(t):
    g = 0
    for tb, _ in TRANS:
        if t >= tb:
            g += 1
    return g


def gstart(g):
    return 0.0 if g == 0 else TRANS[g - 1][0]


# Vurgu rengi (altyazı): tek vurgu — lamba sarısı
EMPH_C = (255, 205, 96)

# KANIT sayacı (HUD): 4 kanıt, her biri bir sahnede "ödenir"
PROOFS = [we("C1", nw("C1") - 1) + 0.10, we("D3", nw("D3") - 1) + 0.05, we("E2b", nw("E2b") - 1) + 0.05, we("E4", nw("E4") - 1) + 0.05]


def kanit(t):
    n = 0
    for p in PROOFS:
        if t >= p:
            n += 1
    return n


def kanit_age(t, i):
    """i. kanıt kapsülünün dolum yaşı (sn); henüz dolmadıysa None"""
    return t - PROOFS[i] if t >= PROOFS[i] else None


# Dönüm anları (özel video: sınırlar süreyle ölçeklenir — 100 sn için ≤5 sarsıntı, ≤3 flaş)
STAMP_YEAR = wt("D2", 0) + 0.05           # "1916" damgası
STAMP_WARN = wt("D4", 0) - 0.02           # "SAKIN DENEMEYİN" damgası
GERM_X = wt("G1", 2) - 0.05               # mikrop çarpı
CARD_T = FINAL_T - 0.55                   # kapanışta karta dönüş başlar

FLASH = [(STAMP_WARN + 0.05, 0.26, 0.12), (GERM_X + 0.05, 0.30, 0.12)]
SHAKES = [(STAMP_YEAR, 9, 0.25), (STAMP_WARN + 0.05, 12, 0.3), (wt("F1", 1), 8, 0.25), (GERM_X + 0.05, 11, 0.28)]
PULSES = list(PROOFS)
# Kamera itişleri (zoom nabzı): yalnız vurgu anlarında
PUNCHES = [(wt("D3", 1) - 0.02, 0.022), (wt("E0b", 1) - 0.02, 0.020), (wt("F3", 4) - 0.02, 0.022), (wt("F2", 4) - 0.02, 0.018)]


def flash_alpha(t):
    a = 0.0
    for t0, s, d in FLASH:
        if t >= t0:
            a = max(a, s * (2.718281828 ** (-(t - t0) / d)))
    return a if a > 0.01 else 0.0


def shake(t):
    dx = dy = 0.0
    for t0, amp, dec in SHAKES:
        u = t - t0
        if 0 <= u < dec * 6:
            e = amp * math.exp(-u / dec)
            dx += e * math.sin(u * 109.0 + t0 * 3)
            dy += e * math.cos(u * 83.0 + t0 * 5)
    return max(-30, min(30, dx)), max(-30, min(30, dy))
