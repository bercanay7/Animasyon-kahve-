"""Mürekkep-parşömen cildi (Uzun Dosya #1, Şarlken): boyalı düz alanlar, sepya mürekkep kontur, yaldız, parşömen tanesi.
Pellagra'nın guaj kukla ilkelleri (`guaj.py`) 16:9'a ve parşömen paletine uyarlandı; karakterler `figures.py`'de."""
import math
import os
from functools import lru_cache

import numpy as np
from PIL import Image, ImageChops, ImageDraw

from engine import *  # noqa

FONT_SLAB = FONT_TITLE
FONT_SOFT = FONT_CAP
FONT_SOFT_BLACK = FONT_TITLE
FONT_SOFT_IT = FONT_CAP_IT


def Hx(s):
    return hexc(s)


# ───────────────────────── palet ─────────────────────────
# parşömen zemin + sepya mürekkep + yaldız; vurgu renkleri: kızıl (Habsburg), lacivert (Fransa), orman yeşili (Osmanlı)
PARCH = Hx("#EBDDB5")
PARCH_L = Hx("#F6EDCF")
PARCH_D = Hx("#D8C494")
PARCH_DD = Hx("#BBA571")
INK = Hx("#2A1A10")
INK_L = Hx("#5A3E26")
GOLD = Hx("#C9962B")
GOLD_L = Hx("#EBC65E")
GOLD_D = Hx("#8F6A18")
CRIMSON = Hx("#8E1F26")
CRIMSON_D = Hx("#5E1218")
CRIMSON_L = Hx("#B8434A")
ROYAL = Hx("#25437A")
ROYAL_D = Hx("#172B52")
ROYAL_L = Hx("#4C6FAE")
FOREST = Hx("#3F6445")
FOREST_D = Hx("#26402C")
FOREST_L = Hx("#6E9570")
VIOLET = Hx("#5B3F73")
TEAL = Hx("#2F7A7A")
SEAW = Hx("#B3C4BE")
SEAW_D = Hx("#8EA7A6")
SEAW_DD = Hx("#6C8788")
NIGHT = Hx("#1E1A26")
# kukla uyumluluğu (guaj adları)
CREAM = PARCH_L
CREAM_D = PARCH_D
OCHRE = GOLD
OCHRE_D = GOLD_D
OCHRE_L = GOLD_L
RUST = Hx("#A4502D")
RUST_D = Hx("#7A3820")
OLIVE = FOREST
OLIVE_D = FOREST_D
OLIVE_L = FOREST_L
BRICK = CRIMSON_L
BRICK_D = CRIMSON
SKIN = Hx("#EDB98C")
SKIN_D = Hx("#D4936A")
SKIN_SICK = Hx("#C9C58E")
NIGHT_L = Hx("#4B3A5C")
LAMP = Hx("#FFC95E")
SEA = Hx("#34506E")
SEA_D = Hx("#22364D")
SEA_L = Hx("#5F86A6")
WHITE = (255, 255, 255)


# ───────────────────────── zaman ─────────────────────────
def tq(t, k=3):
    """Karakter hareketi 'üçlü' karelerde (8 çizim/sn); kamera ve ortam akıcı kalır."""
    return math.floor(t * FPS / k + 1e-6) * k / FPS


def boil(t, rate=8.0):
    return int(math.floor(t * rate + 1e-6))


# ───────────────────────── gürültü / dalga ─────────────────────────
def noise1(seed, x):
    i = math.floor(x)
    f = x - i
    a = rng_hash(seed, i) * 2 - 1
    b = rng_hash(seed, i + 1) * 2 - 1
    f = f * f * (3 - 2 * f)
    return a + (b - a) * f


def densify(pts, step=24.0, closed=True):
    out = []
    n = len(pts)
    for k in range(n if closed else n - 1):
        p, q = pts[k], pts[(k + 1) % n]
        L = math.hypot(q[0] - p[0], q[1] - p[1])
        m = max(1, int(L / step))
        for j in range(m):
            u = j / m
            out.append((p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u))
    if not closed:
        out.append(pts[-1])
    return out


def wob(pts, amp=1.6, seed=0, t=0.0, closed=True, step=24.0, freq=0.045, rate=8.0):
    """El kesimi dalgalanma (sabit) + boil (zamanla değişen, ~%45)."""
    D = densify(pts, step, closed)
    if amp <= 0:
        return D
    ph = boil(t, rate) * 0.731
    out, s = [], 0.0
    for i, (x, y) in enumerate(D):
        if i:
            s += math.hypot(x - D[i - 1][0], y - D[i - 1][1])
        dx = amp * (0.75 * noise1(seed * 3 + 1, s * freq) + 0.45 * noise1(seed * 3 + 7, s * freq * 2.3 + ph))
        dy = amp * (0.75 * noise1(seed * 3 + 2, s * freq + 9.1) + 0.45 * noise1(seed * 3 + 8, s * freq * 2.3 + ph + 4.7))
        out.append((x + dx, y + dy))
    return out


def smooth_closed(pts, n=7):
    """Kapalı Catmull-Rom: organik kâğıt biçimleri."""
    m = len(pts)
    out = []
    for i in range(m):
        p0, p1, p2, p3 = pts[(i - 1) % m], pts[i], pts[(i + 1) % m], pts[(i + 2) % m]
        for j in range(n):
            u = j / n
            u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * u + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u2
                                    + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * u3) for k in (0, 1)))
    return out


def smooth_open(pts, n=7):
    m = len(pts)
    out = []
    P = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, m):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[min(i + 2, m + 1)]
        for j in range(n):
            u = j / n
            u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * u + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u2
                                    + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * u3) for k in (0, 1)))
    out.append(pts[-1])
    return out


def blob(cx, cy, rx, ry, n=12, amp=0.14, seed=0, rot=0.0):
    pts = []
    for i in range(n):
        a = i * 2 * math.pi / n
        k = 1 + amp * (rng_hash(seed, i) * 2 - 1)
        x, y = math.cos(a) * rx * k, math.sin(a) * ry * k
        c, s = math.cos(rot), math.sin(rot)
        pts.append((cx + x * c - y * s, cy + x * s + y * c))
    return smooth_closed(pts, 5)


def ellipse_pts(cx, cy, rx, ry, n=28, rot=0.0):
    c, s = math.cos(rot), math.sin(rot)
    out = []
    for i in range(n):
        a = i * 2 * math.pi / n
        x, y = math.cos(a) * rx, math.sin(a) * ry
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out


def capsule(p0, p1, r0, r1=None, n=10):
    """Uçları yuvarlak, konik kol/bacak çokgeni."""
    r1 = r0 if r1 is None else r1
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    pts = []
    for i in range(n + 1):
        a = ang + math.pi / 2 + math.pi * i / n
        pts.append((p1[0] + r1 * math.cos(a), p1[1] + r1 * math.sin(a)))
    for i in range(n + 1):
        a = ang - math.pi / 2 + math.pi * i / n
        pts.append((p0[0] + r0 * math.cos(a), p0[1] + r0 * math.sin(a)))
    return pts


# ───────────────────────── kırpmalı katman ─────────────────────────
class Clip:
    """Çokgenin içine sınırlanmış boya katmanı: gölge bandı, fırça darbeleri, tarama çizgileri, gradyan."""

    def __init__(self, ctx, pts_world):
        self.ctx = ctx
        q = ctx.pts(pts_world)
        xs = [a for a, _ in q]
        ys = [b for _, b in q]
        self.x0 = max(0, int(min(xs)) - 1)
        self.y0 = max(0, int(min(ys)) - 1)
        self.x1 = min(ctx.im.width, int(max(xs)) + 2)
        self.y1 = min(ctx.im.height, int(max(ys)) + 2)
        self.ok = self.x1 > self.x0 and self.y1 > self.y0
        if not self.ok:
            return
        self.size = (self.x1 - self.x0, self.y1 - self.y0)
        self.layer = Image.new("RGBA", self.size, (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.layer)
        self.q = [(a - self.x0, b - self.y0) for a, b in q]

    def _c(self, pts):
        return [(a - self.x0, b - self.y0) for a, b in self.ctx.pts(pts)]

    def poly(self, pts, col, a=1.0):
        if self.ok:
            self.d.polygon(self._c(pts), fill=tuple(col) + (int(255 * a),))

    def erase(self, pts):
        if self.ok:
            self.d.polygon(self._c(pts), fill=(0, 0, 0, 0))

    def line(self, pts, w, col, a=1.0):
        if self.ok:
            self.d.line(self._c(pts), fill=tuple(col) + (int(255 * a),), width=max(1, int(self.ctx.S(w))), joint="curve")

    def ell(self, cx, cy, rx, ry, col, a=1.0):
        if self.ok:
            x0, y0 = self.ctx.X(cx - rx, cy - ry)
            x1, y1 = self.ctx.X(cx + rx, cy + ry)
            self.d.ellipse([x0 - self.x0, y0 - self.y0, x1 - self.x0, y1 - self.y0], fill=tuple(col) + (int(255 * a),))

    def fill_all(self, col, a=1.0):
        if self.ok:
            self.d.rectangle([0, 0, self.size[0], self.size[1]], fill=tuple(col) + (int(255 * a),))

    def gradient(self, c_top, c_bot, a=1.0):
        if not self.ok:
            return
        h = self.size[1]
        arr = np.zeros((h, 1, 4), np.uint8)
        u = np.linspace(0, 1, h, dtype=np.float32)
        for ch in range(3):
            arr[:, 0, ch] = c_top[ch] + (c_bot[ch] - c_top[ch]) * u
        arr[:, 0, 3] = int(255 * a)
        g = Image.fromarray(arr, "RGBA").resize(self.size, Image.NEAREST)
        self.layer.paste(g, (0, 0))

    def done(self):
        if not self.ok:
            return
        m = Image.new("L", self.size, 0)
        ImageDraw.Draw(m).polygon(self.q, fill=255)
        self.layer.putalpha(ImageChops.multiply(self.layer.getchannel("A"), m))
        self.ctx.im.paste(self.layer, (self.x0, self.y0), self.layer)


def _shift(pts, dx, dy):
    return [(x + dx, y + dy) for x, y in pts]


# ───────────────────────── boyalı şekil ─────────────────────────
def outline(ctx, P, ow, col=INK, seed=0):
    """Çokgenin dışına fırça konturu: yol boyunca 6–9 noktalık parçalar, her parça farklı kalınlıkta, yuvarlak uçlu.
    Çizgi yolun ortasından geçer; iç yarısını dolgu örter, dışta kalınlığı `ow` kalır."""
    if ow <= 0:
        return
    n = len(P)
    i, k = 0, 0
    while i < n:
        m = 6 + int(3 * rng_hash(seed, k, 3))
        chunk = [P[(i + j) % n] for j in range(m + 1)]
        w = 2.0 * ow * (0.78 + 0.44 * rng_hash(seed, k, 5))
        ctx.line(chunk, w, col, 1.0, cap=True)
        i += m
        k += 1


def shape(ctx, pts, fill, ow=8.0, ink=INK, seed=0, t=0.0, wob_amp=1.6, shade=None, wash=None, hatch=None, dry=None,
          closed=True, smooth=False):
    """Boyalı kâğıt kukla parçası: kontur + dolgu + (gölge bandı | yıkama | tarama | kuru fırça)."""
    base = smooth_closed(pts, 6) if smooth else pts
    P = wob(base, wob_amp, seed, t, closed=True)
    outline(ctx, P, ow, ink, seed)
    ctx.poly(P, fill)
    if wash or shade or hatch or dry:
        c = Clip(ctx, P)
        if c.ok:
            if wash:       # üstten alta ton geçişi (üst, alt, alfa)
                c.gradient(wash[0], wash[1], wash[2] if len(wash) > 2 else 0.5)
            if shade:      # sağ-alt kenarda koyu band: shade=(renk, kalınlık, alfa)
                col, d, a = shade
                c.fill_all(col, a)
                c.erase(_shift(P, -d, -d * 1.1))
            if dry:        # kuru fırça çizgileri: dry=(renk, adet, alfa)
                col, n, a = dry
                xs = [p[0] for p in P]
                ys = [p[1] for p in P]
                bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
                for i in range(n):
                    yy = by0 + (by1 - by0) * rng_hash(seed, i, 11)
                    xx = bx0 + (bx1 - bx0) * rng_hash(seed, i, 12) * 0.8
                    ln = (bx1 - bx0) * (0.18 + 0.4 * rng_hash(seed, i, 13))
                    c.line([(xx, yy), (xx + ln, yy + (rng_hash(seed, i, 14) - 0.5) * 6)], 2.4 + 2 * rng_hash(seed, i, 15), col, a * (0.5 + 0.5 * rng_hash(seed, i, 16)))
            if hatch:      # tarama: hatch=(renk, aralık, alfa)
                col, sp, a = hatch
                xs = [p[0] for p in P]
                ys = [p[1] for p in P]
                bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
                x = bx0 - (by1 - by0)
                while x < bx1:
                    c.line([(x, by1), (x + (by1 - by0) * 0.7, by0)], 3.2, col, a)
                    x += sp
            c.done()
    return P


def ink_line(ctx, pts, w=6.0, col=INK, seed=0, t=0.0, wob_amp=1.0, smooth=False, alpha=1.0):
    P = smooth_open(pts, 6) if smooth else pts
    P = wob(P, wob_amp, seed, t, closed=False, step=30.0)
    ctx.line(P, w, col, alpha, cap=True)
    return P


# ───────────────────────── son işlem (parşömen tanesi) ─────────────────────────
_TEX = {}


def _tex():
    if _TEX:
        return _TEX
    rs = np.random.RandomState(11)
    fine = rs.randn(H // 2, W // 2).astype(np.float32)
    fine = np.kron(fine, np.ones((2, 2), np.float32))
    low = rs.randn(H // 90 + 2, W // 90 + 2).astype(np.float32)
    lowi = np.array(Image.fromarray(low, "F").resize((W, H), Image.BICUBIC), dtype=np.float32)
    st = rs.randn(H // 3, W // 40 + 2).astype(np.float32)
    sti = np.array(Image.fromarray(st, "F").resize((W, H), Image.BICUBIC), dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.hypot((xx - W / 2) / (W * 0.62), (yy - H * 0.5) / (H * 0.66))
    vig = (1 - 0.30 * np.clip(r - 0.42, 0, 1) ** 1.4).astype(np.float32)
    _TEX["g"] = 0.0075 * fine + 0.030 * lowi + 0.006 * sti
    _TEX["v"] = vig
    return _TEX


def paint_post(img, strength=1.0, warm=0.0):
    """Parşömen tanesi + hafif vinyet. Zamana bağlı DEĞİL (bit hızı korunur)."""
    tx = _tex()
    a = np.asarray(img, dtype=np.float32)
    a = a * (1 + strength * tx["g"][..., None]) * tx["v"][..., None]
    if warm:
        a[..., 0] *= 1 + warm
        a[..., 2] *= 1 - warm
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


# ───────────────────────── yazı ─────────────────────────
def fit_font(text, path, px, maxw):
    f = font(path, px)
    w = f.getlength(text)
    return px * maxw / w if w > maxw else px


def tr_up(s):
    return s.replace("i", "İ").replace("ı", "I").upper()


def slab(ctx, x, y, s, px, col=CREAM, stroke=0.0, stroke_col=INK, maxw=960, path=FONT_SLAB, anchor="mm"):
    px = fit_font(s, path, px, maxw)
    ctx.text(x, y, s, px, col, path=path, anchor=anchor, stroke=stroke, stroke_fill=stroke_col if stroke else None)
    return px


@lru_cache(maxsize=512)
def word_sprite(word, color, px, path=FONT_SOFT, stroke=7, stroke_fill=INK, shadow=True):
    """2x boyutta kenarlıklı kelime sprite'ı (RGBA)."""
    f = font(path, px * 2)
    st = stroke * 2
    l, t, r, b = f.getbbox(word, stroke_width=st)
    pad = 14 * 2
    w = int(r - l + pad * 2)
    h = int(f.size * 1.5 + pad * 2)
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cx, cy = w // 2, h // 2
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((cx, cy + 8), word, font=f, fill=(20, 8, 2, 150), anchor="mm", stroke_width=st, stroke_fill=(20, 8, 2, 150))
        lay = Image.alpha_composite(lay, sh)
    ImageDraw.Draw(lay).text((cx, cy), word, font=f, fill=tuple(color) + (255,), anchor="mm", stroke_width=st, stroke_fill=tuple(stroke_fill) + (255,))
    return lay


# ───────────────────────── paneller ─────────────────────────
class Patch(Ctx):
    """Kendi boyutunda 2x tuval; yerel koordinat = piksel."""

    def __init__(self, w, h, bg=(0, 0, 0)):
        self.im = Image.new("RGB", (int(w * SS), int(h * SS)), bg)
        self.d = ImageDraw.Draw(self.im)
        self.cx, self.cy, self.z = W / 2, H / 2, 1.0
        self.shx = self.shy = 0.0
        self.par = 1.0
        self.size = (int(w), int(h))

    def finish(self):
        return self.im.reduce(SS)


def cut_poly(pts, frac):
    if frac >= 0.999:
        return list(pts)
    if frac <= 0.001:
        return [pts[0], (pts[0][0] + 0.01, pts[0][1])]
    L = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts[:-1], pts[1:])]
    tot, acc, out = sum(L) * frac, 0.0, [pts[0]]
    for (a, b), l in zip(zip(pts[:-1], pts[1:]), L):
        if acc + l >= tot:
            u = (tot - acc) / max(l, 1e-6)
            out.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u))
            return out
        out.append(b)
        acc += l
    return out
