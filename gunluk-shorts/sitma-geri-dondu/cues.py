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

# Geçişler: her cümle başında (A hariç)
TRANS = [(st("B") - 0.04, "whip"), (st("C") - 0.04, "zoom"), (st("D") - 0.04, "whip"), (st("E") - 0.04, "up"),
         (st("F") - 0.04, "whip"), (st("G") - 0.04, "zoom"), (st("H") - 0.04, "up"), (st("I") - 0.04, "whip"),
         (st("J") - 0.04, "zoom"), (st("K") - 0.04, "whip"), (st("L") - 0.04, "zoom")]
TW = 0.17


def group_of(t):
    g = 0
    for tb, _ in TRANS:
        if t >= tb:
            g += 1
    return g


# ─────────── HUD yıl sayacı: kare 0'da 1977 (spoiler), anlatıda yıllar akar, kapanışta 1977'ye sarar ───────────
YEAR_KF = [
    (0.0, 1977), (1.15, 1977), (1.75, 1970),                       # kart düşerken 1970'e sar: "neredeyse bitmişti"
    (wt("A", 5) - 0.05, 1970), (wt("A", 6) + 0.30, 1977),          # "geri döndü!" → 1977
    (st("B") - 0.04, 1977), (st("B") + 0.50, 1923),                # B: başa sar
    (en("B") - 0.10, 1970),                                        # kinin/bataklık: 1923 → 1970
    (st("D"), 1970), (wt("D", 3) + 0.40, 1977),                    # D: 1970 → 1977
    (en("H"), 1977), (en("I") - 0.10, 1979),                       # I: 1977 → 1979
    (st("J"), 1979), (wt("J", 4) + 0.15, 1994),                    # J: 1979 → 1994
    (st("K") - 0.04, 1994), (st("K") + 0.80, 2025),                # K: bugün
    (st("L") - 0.04, 2025), (st("L") + 0.65, 1977), (T + 1.0, 1977),   # kapanış: 1977'ye sar (kare 0 ile aynı)
]


def year(t):
    if t <= YEAR_KF[0][0]:
        return float(YEAR_KF[0][1])
    for (t0, y0), (t1, y1) in zip(YEAR_KF[:-1], YEAR_KF[1:]):
        if t0 <= t < t1:
            return y0 + (y1 - y0) * ease_io((t - t0) / max(1e-6, t1 - t0))
    return float(YEAR_KF[-1][1])


def year_ticks():
    """Sayaç 5 yıl sınırını geçtikçe tık zamanları (ses için)"""
    out, prev, tt = [], int(round(year(0.0))) // 5, 0.0
    while tt < T - 0.2:
        tt += 1 / 96
        k = int(round(year(tt))) // 5
        if k != prev:
            out.append(round(tt, 3))
            prev = k
    return out


# Vaka noktaları (şematik: 1 nokta ≈ 300 vaka). Gerçek sayılar: 1970 → 1.263, 1977 → 115.512, 1979 → 29.324, 1994 → 84.345
N_1923, N_1970, N_1977, N_1979, N_1994 = 380, 4, 385, 98, 281
CASES = dict(c70=1263, c77=115512, c79=29324, c94=84345)

FLASH = [(wt("A", 6), 0.40, 0.12), (wt("D", 4), 0.55, 0.14), (wt("J", 5), 0.55, 0.14), (st("L") - 0.04 + 0.17, 0.30, 0.12)]
SHAKES = [(wt("A", 6), 12, 0.3), (wt("D", 4), 18, 0.4), (wt("J", 5), 18, 0.4), (st("L") - 0.04 + 0.17, 10, 0.25)]
STAMPS = [(wt("H", 2), 1.0), (wt("K", 6), 0.7)]
PULSES = [wt("A", 6), wt("D", 4), wt("J", 5)]          # HUD titreşimi


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
