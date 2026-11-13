"""Türkiye'nin sadeleştirilmiş (şematik) taslağı + vaka noktaları. Koordinatlar yaklaşıktır (boylam, enlem)."""
import math
from functools import lru_cache

from engine import rng_hash

# saat yönünde, KB'dan (Trakya) başlayarak
TR = [
    (26.35, 41.72), (26.60, 42.00), (27.20, 42.07), (27.70, 42.05), (28.02, 41.97),            # Bulgaristan sınırı
    (28.15, 41.58), (28.95, 41.25), (29.60, 41.18), (30.30, 41.15), (31.10, 41.10),            # Karadeniz kıyısı
    (31.80, 41.45), (32.40, 41.75), (33.00, 41.92), (33.75, 41.98), (34.50, 41.98),
    (35.05, 42.10), (35.45, 41.90), (35.95, 41.70), (36.35, 41.30), (37.00, 41.20),
    (37.90, 41.00), (38.40, 40.95), (39.70, 41.00), (40.50, 41.03), (41.40, 41.42),
    (42.00, 41.55), (42.60, 41.50), (42.90, 41.22), (43.40, 41.10),                           # Gürcistan sınırı
    (43.60, 40.70), (43.75, 40.25), (44.20, 39.95), (44.80, 39.65),                           # Ermenistan / Nahçıvan
    (44.40, 39.40), (44.20, 38.90), (44.05, 38.40), (44.40, 38.20), (44.10, 37.90),
    (44.35, 37.65), (44.75, 37.20),                                                            # İran sınırı
    (44.30, 37.05), (43.20, 37.30), (42.40, 37.12), (41.20, 37.08), (40.00, 36.90),           # Irak / Suriye sınırı
    (38.95, 36.75), (38.00, 36.85), (37.20, 36.65), (36.65, 36.20), (36.20, 35.95), (35.95, 35.88),
    (35.95, 36.10), (36.05, 36.40), (36.17, 36.60), (35.78, 36.77), (35.35, 36.57),           # Akdeniz kıyısı
    (35.00, 36.75), (34.15, 36.45), (33.90, 36.35), (32.80, 36.05), (32.30, 36.27),
    (32.00, 36.50), (30.70, 36.85), (30.55, 36.60), (30.15, 36.30), (29.65, 36.20),
    (29.10, 36.62), (28.65, 36.80), (28.25, 36.85), (27.30, 36.70), (27.40, 37.03),
    (27.25, 37.40), (27.25, 37.85), (26.30, 38.30), (26.50, 38.65), (26.88, 39.07),           # Ege kıyısı
    (26.70, 39.30), (26.07, 39.48), (26.15, 39.85), (26.17, 40.05),
    (26.45, 40.50), (26.05, 40.75), (26.38, 40.92), (26.62, 41.32), (26.55, 41.68),           # Trakya / Meriç
]

LON_C, LAT_C = 35.45, 39.0
KX = 63.3 * math.cos(math.radians(39.0))      # px / derece boylam (ölçek 1.0 → ~940 px genişlik)
KY = 63.3                                      # px / derece enlem


def xy(lon, lat, cx=540.0, cy=1000.0, s=1.0):
    return (cx + (lon - LON_C) * KX * s, cy + (LAT_C - lat) * KY * s)


def outline(cx=540.0, cy=1000.0, s=1.0):
    return [xy(lo, la, cx, cy, s) for lo, la in TR]


def _inside(lon, lat):
    c = False
    n = len(TR)
    j = n - 1
    for i in range(n):
        xi, yi = TR[i]
        xj, yj = TR[j]
        if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi + 1e-12) + xi:
            c = not c
        j = i
    return c


def _gauss(a, b, seed):
    u = max(1e-6, rng_hash(a, b, seed, 1))
    v = rng_hash(a, b, seed, 2)
    return math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * v)


N_MAX = 420


@lru_cache(maxsize=8)
def dots(layout):
    """(boylam, enlem) listesi — ilk n tanesi gösterilir. Tüm noktalar taslağın içindedir."""
    out, k = [], 0
    while len(out) < N_MAX and k < 20000:
        k += 1
        r = rng_hash(k, 9, 3)
        if layout == "yayginlik":
            lon = 26.0 + 18.6 * rng_hash(k, 1, 5)
            lat = 36.0 + 6.0 * rng_hash(k, 2, 5)
        elif layout == "salgin77":
            if r < 0.70:
                hub = (35.3, 37.0) if rng_hash(k, 4, 4) < 0.55 else (36.3, 36.5)
                lon = hub[0] + 0.75 * _gauss(k, 1, 6)
                lat = hub[1] + 0.40 * _gauss(k, 2, 6)
            else:
                lon = 26.0 + 18.6 * rng_hash(k, 1, 5)
                lat = 36.0 + 6.0 * rng_hash(k, 2, 5)
        elif layout == "cukurova":
            hub = (35.5, 36.85) if rng_hash(k, 4, 4) < 0.7 else (36.3, 36.45)
            lon = hub[0] + 0.55 * _gauss(k, 1, 8)
            lat = hub[1] + 0.28 * _gauss(k, 2, 8)
        elif layout == "salgin94":
            if r < 0.82:
                lon = 40.9 + 1.7 * _gauss(k, 1, 7)
                lat = 37.45 + 0.42 * _gauss(k, 2, 7)
            else:
                lon = 26.0 + 18.6 * rng_hash(k, 1, 5)
                lat = 36.0 + 6.0 * rng_hash(k, 2, 5)
        else:
            raise ValueError(layout)
        if _inside(lon, lat) and 36.0 < lat < 42.0:
            out.append((lon, lat))
    return tuple(out)


HUB_CUKUROVA = (35.6, 36.9)
