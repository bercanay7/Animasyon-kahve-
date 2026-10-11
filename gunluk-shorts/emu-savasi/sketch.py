"""Kara kalem / kömür çizim stili: titreyen (boiling) çizgiler, tarama, renk lekeleri, kağıt dokusu."""
import math

import numpy as np
from PIL import Image, ImageFilter

from engine import *  # noqa

PAPER = (241, 233, 214)
INK = (30, 28, 30)
INK2 = (62, 58, 58)
GREY = (104, 99, 96)
LIGHT = (176, 168, 156)
ACC = (216, 62, 40)       # tek vurgu rengi: kırmızı-turuncu
HL = (255, 214, 72)       # fosforlu kalem sarısı
KHAKI = (190, 168, 98)
WHEAT = (230, 188, 86)
SKYW = (186, 206, 212)
EMUW = (150, 110, 84)
SKIN = (236, 190, 150)

FPS_BOIL = 8


def bucket(t):
    return int(t * FPS_BOIL)


def subdivide(pts, step=26.0):
    out = [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(L / step))
        for k in range(1, n + 1):
            u = k / n
            out.append((x0 + (x1 - x0) * u, y0 + (y1 - y0) * u))
    return out


def catmull(pts, n=6, closed=False):
    """Catmull-Rom ile yumuşatılmış nokta dizisi"""
    P = list(pts)
    if closed:
        P = [P[-1]] + P + [P[0], P[1]]
    else:
        P = [P[0]] + P + [P[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append((0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
                        0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)))
    out.append(P[-2])
    if closed:
        out.append(out[0])
    return out


def _cut(pts, frac):
    if frac >= 0.999:
        return pts
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


def sline(ctx, pts, w=5.0, col=INK, seed=0, t=0.0, amp=2.4, passes=2, alpha=1.0, reveal=1.0, step=24.0, smooth=False, soft=True):
    """Titreyen kömür çizgisi. pts dünya koordinatı; reveal: çizilme oranı"""
    if len(pts) < 2 or reveal <= 0:
        return
    if smooth:
        pts = catmull(pts, 5)
    pts = _cut(subdivide(pts, step), reveal)
    if len(pts) < 2:
        return
    b = bucket(t)
    if soft:
        ctx.line([(x + (rng_hash(seed, i, b) - 0.5) * amp, y + (rng_hash(seed, i, b, 9) - 0.5) * amp) for i, (x, y) in enumerate(pts)],
                 w * 2.6, mix(PAPER, col, 0.40), 0.16 * alpha)
    for p in range(passes):
        jp = [(x + (rng_hash(seed + p * 31, i, b) - 0.5) * 2 * amp * (1 + 0.4 * p),
               y + (rng_hash(seed + p * 31, i, b, 5) - 0.5) * 2 * amp * (1 + 0.4 * p)) for i, (x, y) in enumerate(pts)]
        ctx.line(jp, w * (1.0 if p == 0 else 0.55), col, alpha * (0.92 if p == 0 else 0.5))


def shape(ctx, pts, col=INK, w=5.0, seed=0, t=0.0, amp=2.4, closed=True, smooth=True, reveal=1.0, passes=2, alpha=1.0):
    P = list(pts)
    if smooth:
        P = catmull(P, 5, closed=closed)
    elif closed:
        P = P + [P[0]]
    sline(ctx, P, w, col, seed, t, amp, passes, alpha, reveal)


def wash(ctx, pts, col, alpha=0.55, off=(5, 4), smooth=True, t=0.0, seed=0, jit=1.5):
    """Çizginin hafif dışına taşan suluboya/kömür lekesi"""
    P = catmull(pts, 5, closed=True) if smooth else list(pts)
    b = bucket(t)
    P = [(x + off[0] + (rng_hash(seed, i, b) - 0.5) * jit, y + off[1] + (rng_hash(seed, i, b, 3) - 0.5) * jit) for i, (x, y) in enumerate(P)]
    ctx.poly(P, col, alpha)


def hatch(ctx, pts, angle=50.0, gap=10.0, w=3.0, col=INK2, seed=0, t=0.0, alpha=0.85, amp=1.6, smooth=True, reveal=1.0):
    """Çokgen içini taramalı doldur (kömür gölgeleme)"""
    P = catmull(pts, 4, closed=True) if smooth else list(pts)
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    R = [(x * ca + y * sa, -x * sa + y * ca) for x, y in P]
    ys = [p[1] for p in R]
    y0, y1 = min(ys), max(ys)
    segs = []
    yy = y0 + gap * 0.5
    k = 0
    while yy < y1:
        xs = []
        for (xa, ya), (xb, yb) in zip(R[:-1], R[1:]):
            if (ya <= yy < yb) or (yb <= yy < ya):
                u = (yy - ya) / (yb - ya)
                xs.append(xa + (xb - xa) * u)
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            segs.append((xs[i], xs[i + 1], yy, k))
        yy += gap
        k += 1
    n = len(segs)
    b = bucket(t)
    for j, (xa, xb, y, k) in enumerate(segs):
        if j / max(1, n) > reveal:
            break
        jx = (rng_hash(seed, k, b) - 0.5) * gap * 0.5
        p0 = (xa + jx, y + (rng_hash(seed, k, b, 2) - 0.5) * amp)
        p1 = (xb + jx, y + (rng_hash(seed, k, b, 3) - 0.5) * amp)
        q0 = (p0[0] * ca - p0[1] * sa, p0[0] * sa + p0[1] * ca)
        q1 = (p1[0] * ca - p1[1] * sa, p1[0] * sa + p1[1] * ca)
        ctx.line([q0, q1], w, col, alpha)


def dot(ctx, x, y, r, col=INK, seed=0, t=0.0):
    b = bucket(t)
    ctx.circ(x + (rng_hash(seed, 1, b) - 0.5), y + (rng_hash(seed, 2, b) - 0.5), r, col)


def paper_bg(ctx, tint=None):
    """Ekran uzayında kağıt zemini"""
    par = ctx.par
    ctx.parallax(0)
    top = PAPER if tint is None else mix(PAPER, tint, 0.0)
    ctx.vgrad(0, 0, W, H, [(0, (247, 240, 224)), (1, (232, 222, 200))])
    ctx.parallax(par)


# ───────────────────────── son işlem: kömür/kağıt dokusu ─────────────────────────
_TEX = None


def _textures():
    global _TEX
    if _TEX is None:
        rng = np.random.default_rng(42)
        out = []
        for k in range(3):
            n1 = rng.standard_normal((H // 2, W // 2)).astype(np.float32)
            n1 = np.asarray(Image.fromarray(((n1 - n1.min()) / (n1.max() - n1.min()) * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR),
                            dtype=np.float32) / 255.0
            n2 = rng.random((H, W)).astype(np.float32)
            out.append((n1, n2))
        # kağıt lifleri (statik)
        fib = rng.random((H, W)).astype(np.float32)
        fib = np.asarray(Image.fromarray((fib * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.1)), dtype=np.float32) / 255.0
        fib = (fib - fib.mean()) / (fib.std() + 1e-6)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.hypot((xx - W / 2) / (W * 0.7), (yy - H * 0.46) / (H * 0.62))
        vig = 1 - 0.20 * np.clip(r - 0.5, 0, 1) ** 1.5
        _TEX = (out, fib, vig.astype(np.float32))
    return _TEX


def charcoal_post(img, t, still=False):
    """Kağıt lifi + kömür tanesi: koyu çizgiler tane tane aşınır, her 3 karede doku oynar."""
    tex, fib, vig = _textures()
    n1, n2 = tex[0 if still else (int(t * 8) % 3)]
    a = np.asarray(img, dtype=np.float32)
    lum = a.mean(axis=2)
    dark = np.clip((200.0 - lum) / 170.0, 0, 1)            # çizgi yoğunluğu
    erode = np.clip((n2 * 0.65 + n1 * 0.55) - 0.55, 0, 1) * 1.5 * dark   # tane tane aşınma
    paper = np.array(PAPER, np.float32)
    a = a + (paper - a) * erode[..., None] * 0.75
    a = a * (1 + fib[..., None] * 0.012)                      # kağıt lifi
    a = a * vig[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
