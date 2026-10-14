"""Mavi baskı (blueprint) teknik çizim stili: parlayan çizgiler, çizilerek beliren gemiler, ölçü çizgileri."""
import math
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from engine import *  # noqa

import os
FONT_MONO = os.path.join(HERE, "fonts", "IBMPlexMono-Bold.ttf")

BG1, BG2 = (14, 52, 98), (6, 22, 48)
LINE = (196, 238, 255)
LINE_DIM = (104, 168, 214)
GRID = (96, 154, 204)
AMBER = (255, 196, 76)
RED = (255, 98, 88)
GREEN = (124, 255, 184)
NAVY_DK = (4, 16, 36)


def _cut(pts, frac):
    if frac >= 0.999:
        return pts
    if frac <= 0:
        return []
    L = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts[:-1], pts[1:])]
    tot = sum(L) * frac
    out, acc = [pts[0]], 0.0
    for (a, b), l in zip(zip(pts[:-1], pts[1:]), L):
        if acc + l >= tot:
            u = (tot - acc) / max(l, 1e-6)
            out.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u))
            return out
        out.append(b)
        acc += l
    return out


def bg(ctx, t=0.0, tint=0.0):
    """Izgaralı lacivert zemin (ekran uzayı)"""
    par = ctx.par
    ctx.parallax(0)
    top = mix(BG1, (60, 20, 40), tint)
    bot = mix(BG2, (30, 8, 20), tint)
    ctx.vgrad(0, 0, W, H, [(0, top), (1, bot)])
    for x in range(0, W + 1, 40):
        major = x % 200 == 0
        ctx.line([(x, 0), (x, H)], 2 if major else 1.2, GRID, 0.20 if major else 0.09, cap=False)
    for y in range(0, H + 1, 40):
        major = y % 200 == 0
        ctx.line([(0, y), (W, y)], 2 if major else 1.2, GRID, 0.20 if major else 0.09, cap=False)
    ctx.parallax(par)


def L(ctx, pts, w=4.0, col=LINE, alpha=1.0, reveal=1.0, glow=True, closed=False):
    if closed:
        pts = list(pts) + [pts[0]]
    p = _cut(pts, reveal)
    if len(p) < 2:
        return
    if glow:
        ctx.line(p, w * 3.2, col, 0.12 * alpha, cap=True)
    ctx.line(p, w, col, alpha, cap=True)


def draw_seq(ctx, polys, reveal, w=4.0, col=LINE, alpha=1.0, glow=True):
    """Çizgi listesini sırayla çizerek ortaya çıkar (reveal 0..1)"""
    n = len(polys)
    for i, pl in enumerate(polys):
        pts = pl[0] if isinstance(pl, tuple) else pl
        ww = pl[1] if isinstance(pl, tuple) else w
        r = clamp(reveal * n - i)
        if r > 0:
            L(ctx, pts, ww, col, alpha, r, glow)


def txt(ctx, x, y, s, px, col=LINE, alpha=1.0, anchor="mm", path=FONT_MONO, stroke=0):
    if alpha <= 0.01:
        return
    if alpha < 0.99:
        # alfalı metin: kısa süreli solma için renk karışımı
        col = mix((10, 34, 70), col, alpha)
    ctx.text(x, y, s, px, col, path=path, anchor=anchor, stroke=stroke, stroke_fill=NAVY_DK if stroke else None)


def check(ctx, x, y, s, reveal=1.0, col=GREEN):
    L(ctx, [(x - 24 * s, y), (x - 6 * s, y + 20 * s), (x + 28 * s, y - 24 * s)], 9 * s, col, 1.0, reveal)


def cross(ctx, x, y, s, reveal=1.0, col=RED):
    L(ctx, [(x - 24 * s, y - 24 * s), (x + 24 * s, y + 24 * s)], 9 * s, col, 1.0, clamp(reveal * 2))
    L(ctx, [(x + 24 * s, y - 24 * s), (x - 24 * s, y + 24 * s)], 9 * s, col, 1.0, clamp(reveal * 2 - 1))


def circ_pts(cx, cy, rx, ry=None, n=24):
    ry = rx if ry is None else ry
    return [(cx + math.cos(i * 2 * math.pi / n) * rx, cy + math.sin(i * 2 * math.pi / n) * ry) for i in range(n + 1)]


# ═══════════════════════════ GEMİ ═══════════════════════════
@lru_cache(maxsize=4)
def ship_polys(funnels=4):
    P = []
    # gövde
    P.append(([(-505, -88), (-498, -20), (-470, 28), (-400, 46), (380, 46), (452, 12), (512, -88), (-505, -88)], 5))
    P.append(([(-505, -88), (-470, -102), (480, -102), (512, -88)], 4))        # güverte kenarı
    P.append(([(-470, -45), (430, -45)], 2.5))                                  # su hattı şeridi
    # üst yapı
    P.append(([(-390, -102), (-390, -158), (360, -158), (360, -102)], 4))
    P.append(([(-300, -158), (-300, -214), (290, -214), (290, -158)], 4))
    P.append(([(190, -214), (190, -262), (290, -262), (290, -214)], 4))
    # pencere şeritleri
    for yy in (-130, -186):
        P.append(([(-370 if yy == -130 else -280, yy), (340 if yy == -130 else 270, yy)], 2))
    # bacalar
    xs = {4: (-210, -70, 70, 210), 3: (-150, 0, 150)}[funnels]
    for x in xs:
        P.append(([(x - 30, -214), (x - 26, -340), (x + 26, -340), (x + 30, -214)], 4))
        P.append(([(x - 28, -322), (x + 28, -322)], 2.5))
    # direkler ve halat
    P.append(([(330, -102), (330, -330)], 3))
    P.append(([(-440, -102), (-440, -260)], 3))
    P.append(([(330, -330), (505, -100)], 1.8))
    P.append(([(330, -330), (200, -262)], 1.8))
    P.append(([(-440, -260), (-500, -92)], 1.8))
    # iç hatlar
    for k in range(18):
        x = -440 + k * 50
        P.append(([(x, -78), (x, -66)], 3))
    return tuple(P)


def ship(ctx, cx, cy, s, reveal=1.0, funnels=4, col=LINE, w=4.0, alpha=1.0, flip=1, t=0.0, bob=0.0):
    polys = []
    for pts, ww in ship_polys(funnels):
        polys.append(([(cx + flip * x * s, cy + y * s + bob) for x, y in pts], ww * s * 1.2))
    draw_seq(ctx, polys, reveal, w, col, alpha)


def waves_line(ctx, y, t, x0=-100, x1=W + 100, amp=8, wl=160, col=LINE_DIM, rows=3, alpha=0.8, reveal=1.0):
    for r in range(rows):
        pts = []
        x = x0
        while x <= x1:
            pts.append((x, y + r * 26 + math.sin(x / wl * 6.283 + t * 1.4 + r * 1.3) * amp))
            x += 24
        L(ctx, pts, 3, col, alpha * (1 - 0.25 * r), reveal, glow=False)


def iceberg(ctx, cx, cy, s, reveal=1.0, t=0.0):
    top = [(-260, 0), (-210, -90), (-150, -70), (-100, -220), (-30, -150), (30, -330), (110, -190), (160, -230), (220, -90), (270, 0)]
    pts = [(cx + x * s, cy + y * s) for x, y in top]
    L(ctx, pts, 6 * s, LINE, 1.0, reveal)
    facets = [[(-100, -220), (-60, -90), (-150, -70)], [(30, -330), (0, -160), (110, -190)], [(30, -330), (60, -130), (110, -190)], [(-100, -220), (-30, -150), (0, -160)]]
    for k, f in enumerate(facets):
        L(ctx, [(cx + x * s, cy + y * s) for x, y in f], 3 * s, LINE_DIM, 0.9, clamp(reveal * 3 - k * 0.6), glow=False)
    # sualtı kısmı (kesik çizgi)
    below = [(-260, 0), (-220, 120), (-120, 260), (0, 330), (130, 250), (230, 130), (270, 0)]
    pb = [(cx + x * s, cy + y * s) for x, y in below]
    for i in range(0, len(pb) - 1):
        a, b = pb[i], pb[i + 1]
        for u in (0.0, 0.5):
            p0 = (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
            p1 = (a[0] + (b[0] - a[0]) * (u + 0.35), a[1] + (b[1] - a[1]) * (u + 0.35))
            L(ctx, [p0, p1], 3.5 * s, LINE_DIM, 0.7 * clamp(reveal * 2 - 0.5), 1.0, glow=False)


def lifeboat(ctx, x, y, s, reveal=1.0, col=LINE, w=3.5):
    hull = [(x - 36 * s, y - 10 * s), (x - 24 * s, y + 10 * s), (x + 24 * s, y + 10 * s), (x + 36 * s, y - 10 * s), (x - 36 * s, y - 10 * s)]
    L(ctx, hull, w * s, col, 1.0, reveal, glow=False)
    L(ctx, [(x - 44 * s, y - 14 * s), (x + 44 * s, y - 14 * s)], w * s, col, 1.0, reveal, glow=False)


def dim_line(ctx, x0, x1, y, label, px=44, col=AMBER, reveal=1.0, t=0.0):
    L(ctx, [(x0, y), (x1, y)], 3, col, 1.0, reveal, glow=False)
    for x, d in ((x0, 1), (x1, -1)):
        L(ctx, [(x, y - 18), (x, y + 18)], 3, col, 1.0, reveal, glow=False)
        L(ctx, [(x + d * 26, y - 10), (x, y), (x + d * 26, y + 10)], 3, col, 1.0, reveal, glow=False)
    if reveal > 0.9:
        txt(ctx, (x0 + x1) / 2, y - 34, label, px, col)


def stamp(ctx, cx, cy, text, px, col=RED, rot=-8.0, k=1.0):
    X = Xf(cx, cy, 1.0, rot=rot)
    f = font(FONT_MONO, px)
    wd = f.getlength(text)
    box = [(-wd / 2 - 28, -px * 0.8), (wd / 2 + 28, -px * 0.8), (wd / 2 + 28, px * 0.8), (-wd / 2 - 28, px * 0.8)]
    pts = X.pts(box)
    ctx.poly(pts, NAVY_DK, 0.55 * clamp(k * 2))
    L(ctx, pts, 8, col, 1.0, clamp(k * 1.5), closed=True)
    if k > 0.3:
        ctx.text(*X.p(0, 3), text, px, col, path=FONT_MONO)


def typed(s, t0, t, cps=18.0):
    n = int(clamp((t - t0) * cps, 0, len(s)))
    return s[:n]


def topdown_ship(ctx, cx, cy, s, reveal=1.0, col=LINE, w=4.0):
    """Üstten görünüm: sancak = sağ taraf (ekranda aşağı)"""
    hull = [(-480, -50), (-480, 50), (260, 50), (470, 0), (260, -50), (-480, -50)]
    L(ctx, [(cx + x * s, cy + y * s) for x, y in hull], w * s * 1.3, col, 1.0, reveal)
    for x in (-360, -200, -40, 120):
        L(ctx, [(cx + x * s, cy - 40 * s), (cx + x * s, cy + 40 * s)], 2.5 * s, LINE_DIM, 0.8, clamp(reveal * 2), glow=False)
    L(ctx, [(cx - 470 * s, cy), (cx + 440 * s, cy)], 2 * s, LINE_DIM, 0.6, reveal, glow=False)


# ═══════════════════════════ SON İŞLEM ═══════════════════════════
_G = None


def bp_post(img, t, glow=0.32, shift=0.0):
    a = np.asarray(img, dtype=np.float32)
    bl = np.asarray(img.filter(ImageFilter.GaussianBlur(7)), dtype=np.float32)
    a = np.clip(a + bl * glow, 0, 255)
    global _G
    if _G is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.hypot((xx - W / 2) / (W * 0.72), (yy - H * 0.46) / (H * 0.62))
        _G = (1 - 0.34 * np.clip(r - 0.4, 0, 1) ** 1.6).astype(np.float32)
    a = a * _G[..., None]
    # ince tarama çizgisi (CRT/plotter hissi)
    a[::3, :, :] *= 0.965
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
