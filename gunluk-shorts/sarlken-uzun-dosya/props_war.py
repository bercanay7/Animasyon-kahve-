"""Sahne-lab ortak ilkelleri (deniz / savaş alanı / kuşatma): yumuşak sprite'lar, parçacıklar, bulut dokusu, dalga şeritleri, sancak, gemi.

Kural: ağır işler (gürültü dokusu, bulanıklık, degrade) yalnız önbellekli `*_sprite`/`bake` işlevlerinde; kare başına yalnız drawImage + küçük yol.
"""
import math
from functools import lru_cache

import cv2
import numpy as np
import skia

import sk
import stage as ST
from sk import C, H, W, clamp, lerp, mix, smooth
from stage import MARGIN

LIN = skia.SamplingOptions(skia.FilterMode.kLinear)
LINMIP = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)
PLUS = skia.BlendMode.kPlus


def RS(seed):
    return np.random.RandomState(seed & 0x7FFFFFFF)


def lighten(c, k):
    return mix(c, "#FFFFFF", k)


def darken(c, k):
    return mix(c, "#000000", k)


def hex_rgb(c):
    return sk.rgb(c)


# ───────────────────────────── numpy → skia ─────────────────────────────
def img_from_rgba(arr, mip=False):
    """uint8 RGBA (unpremul) → premultiplied raster skia.Image (kare başına çizime uygun)."""
    src = sk.np_to_image(arr)
    s = skia.Surface(src.width(), src.height())
    c = s.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    c.drawImage(src, 0, 0)
    im = s.makeImageSnapshot()
    return im.withDefaultMipmaps() if mip else im


def smoothstep_np(e0, e1, x):
    t = np.clip((x - e0) / max(1e-6, e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


# ───────────────────────────── yumuşak sprite'lar ─────────────────────────────
_R_STEPS = (12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512)


def _rq(r):
    for q in _R_STEPS:
        if r <= q:
            return q
    return _R_STEPS[-1]


@lru_cache(maxsize=512)
def glow_sprite(rq, col, a0=255, a1=90, mid=0.38):
    s = skia.Surface(2 * rq, 2 * rq)
    c = s.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    sh = skia.GradientShader.MakeRadial((rq, rq), rq, [C(col, a0), C(col, a1), C(col, 0)], [0.0, mid, 1.0])
    c.drawCircle(rq, rq, rq, skia.Paint(Shader=sh, AntiAlias=True))
    return s.makeImageSnapshot()


def glow(f, x, y, r, col="#FFB347", a=1.0, a0=255, a1=90, mid=0.38, blend=None):
    """Önbellekli radyal parıltı sprite'ı. dyn için HIZLI: SrcOver (kPlus + ölçekli bilinear çok yavaştır, ~7 ms/256px)."""
    if a <= 0.01 or r <= 0.5:
        return
    rq = _rq(r)
    img = glow_sprite(rq, col, a0, a1, mid)
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    if blend is not None:
        p.setBlendMode(blend)
    f.c.save()
    f.c.translate(x, y)
    k = r / rq
    f.c.scale(k, k)
    f.c.drawImage(img, -rq, -rq, LIN, p)
    f.c.restore()


def glow_add(f, x, y, r, col="#FFB347", a=1.0, a0=255, a1=90, mid=0.38):
    """Toplamalı (kPlus) parıltı: YALNIZ pişirme (layers()/sprite) içinde kullan."""
    glow(f, x, y, r, col, a, a0, a1, mid, blend=PLUS)


def shadow(f, x, y, rx, ry, a=0.35, col="#000000"):
    """Yumuşak elips gölge (ayakların altı): önbellekli radyal sprite'ı ölçekler — dyn'de ucuz."""
    g = glow_sprite(64, col, 230, 130, 0.5)
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    f.c.save()
    f.c.translate(x, y)
    f.c.scale(rx / 64.0, ry / 64.0)
    f.c.drawImage(g, -64, -64, LIN, p)
    f.c.restore()


@lru_cache(maxsize=64)
def puff_sprite(col="#2A2420", seed=3, size=160):
    """Düzensiz yumuşak duman kabarcığı (alfa: gürültülü radyal düşüş)."""
    rs = RS(seed)
    n = cv2.resize(rs.rand(10, 10).astype(np.float32), (size, size), interpolation=cv2.INTER_CUBIC)
    n2 = cv2.resize(rs.rand(24, 24).astype(np.float32), (size, size), interpolation=cv2.INTER_CUBIC)
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    r = np.sqrt((xx - size / 2) ** 2 + (yy - size / 2) ** 2) / (size / 2)
    a = np.clip(1.0 - r, 0, 1) ** 1.25
    a = a * (0.55 + 0.6 * n + 0.25 * n2)
    a = np.clip(a * 1.05, 0, 1)
    rgb_ = np.array(sk.rgb(col), np.float32)
    shade = (0.75 + 0.5 * (1 - yy / size))[..., None] * rgb_[None, None, :]
    out = np.dstack([np.clip(shade, 0, 255), a * 255]).astype(np.uint8)
    return img_from_rgba(out)


def puff(f, x, y, r, col="#2A2420", a=0.5, seed=0, rot=0.0):
    if a <= 0.01:
        return
    img = puff_sprite(col, 3 + (seed % 5), 160)
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    f.c.save()
    f.c.translate(x, y)
    if rot:
        f.c.rotate(math.degrees(rot))
    k = r / 80.0
    f.c.scale(k, k)
    f.c.drawImage(img, -80, -80, LIN, p)
    f.c.restore()


def smoke_column(f, x, y, t, n=10, h=300, w0=18, w1=90, col="#2A2420", a=0.5, rate=0.16, drift=40.0, seed=1, wobble=14.0):
    """Yükselen duman: n kabarcık (sprite)."""
    rs = RS(seed)
    for i in range(n):
        ph = (t * rate + i / n + rs.rand() * 0.02) % 1.0
        r = w0 + (w1 - w0) * ph ** 0.8
        px = x + drift * ph * ph + math.sin(ph * 5 + i * 1.7) * wobble * ph
        py = y - ph * h
        al = a * math.sin(math.pi * min(1.0, ph * 1.05)) ** 1.1
        puff(f, px, py, r, col, al, seed=i, rot=ph * 2 + i)


def sparks(f, x, y, t, n=14, h=160, spread=40, seed=5, col="#FFB347", size=2.0, rate=0.5):
    rs = RS(seed)
    p = skia.Paint(AntiAlias=True)
    p.setBlendMode(PLUS)
    for i in range(n):
        ph = (t * rate * (0.6 + rs.rand() * 0.8) + rs.rand()) % 1.0
        px = x + (rs.rand() - 0.5) * spread * (0.4 + ph) + math.sin(t * 3 + i) * 6 * ph
        py = y - ph * h * (0.6 + 0.8 * rs.rand())
        a = (1 - ph) ** 1.2 * (0.5 + 0.5 * abs(math.sin(t * 9 + i * 2.3)))
        p.setColor(C(col, int(255 * a)))
        f.c.drawCircle(px, py, size * (1.0 - 0.5 * ph) * (0.6 + 0.6 * rs.rand()), p)


def flame(f, x, y, s, t, seed=0, hot="#FFE9A8", mid="#FFA630", cold="#C9380E", glow_r=1.0, glow_a=0.9):
    """Küçük alev: 3 katmanlı damla + parıltı (kare başına yalnız path + sprite)."""
    fl = 0.78 + 0.22 * math.sin(t * 11 + seed * 1.9) * math.sin(t * 7.3 + seed)
    lean = math.sin(t * 5.1 + seed * 2.3) * 0.18
    glow(f, x, y - 26 * s, 90 * s * glow_r * fl, "#FF9A2E", glow_a * 0.55 * fl)
    for k, (col, sc, al) in enumerate(((cold, 1.0, 0.95), (mid, 0.72, 0.95), (hot, 0.42, 0.95))):
        hh = 62 * s * sc * fl
        ww = 17 * s * sc
        p = skia.Path()
        p.moveTo(x - ww, y)
        p.cubicTo(x - ww * 1.1, y - hh * 0.35, x - ww * 0.4 + lean * hh * 0.25, y - hh * 0.62, x + lean * hh, y - hh)
        p.cubicTo(x + ww * 0.5 + lean * hh * 0.3, y - hh * 0.6, x + ww * 1.1, y - hh * 0.32, x + ww, y)
        p.close()
        pa = skia.Paint(AntiAlias=True, Color=C(col, int(255 * al)))
        if k == 2:
            pa.setBlendMode(PLUS)
        f.c.drawPath(p, pa)


# ───────────────────────────── gürültü / bulut ─────────────────────────────
def fbm_periodic(w, h, scale, octaves, seed):
    n = sk.noise_tex(w, h, scale, octaves, seed)
    xs = np.arange(w, dtype=np.float32)
    a = (np.sin(np.pi * xs / w) ** 2)[None, :]
    n2 = n * a + np.roll(n, w // 2, axis=1) * (1 - a)
    n2 = (n2 - n2.min()) / (n2.max() - n2.min() + 1e-6)
    return n2.astype(np.float32)


def cloud_rgba(w, h, seed, cover=0.5, soft=0.22, scale=70, octaves=5, shadow="#3A3F4A", light="#F0E0C0", rim=None,
               light_dir=(-0.7, -0.7), vfade=None, gamma=1.0, gain=2.4, stretch=2.0, periodic=True, thick_dark=0.0, sigma=3.0, reach=14):
    """Bulut dokusu (RGBA uint8). cover: kaplama (0..1), light_dir: ışığın geldiği yön. periodic: yatay dikişsiz."""
    wn = max(8, int(w / stretch))
    n = fbm_periodic(wn, h, scale, octaves, seed) if periodic else sk.noise_tex(wn, h, scale, octaves, seed)
    if stretch != 1.0:
        n = cv2.resize(n, (w, h), interpolation=cv2.INTER_CUBIC)
    d = smoothstep_np(1 - cover - soft / 2, 1 - cover + soft / 2, n)
    if vfade is not None:
        d = d * vfade[:, None]
    db = cv2.GaussianBlur(d, (0, 0), sigma)
    dx, dy = light_dir
    sh = np.roll(db, (-int(round(dy * reach)), -int(round(dx * reach))), axis=(0, 1))
    lit = np.clip(0.5 + (db - sh) * gain, 0, 1)
    if thick_dark:
        lit = lit * (1 - thick_dark * np.clip(db, 0, 1) ** 2)
    sc_, lc_ = np.array(sk.rgb(shadow), np.float32), np.array(sk.rgb(light), np.float32)
    col = sc_[None, None, :] * (1 - lit[..., None]) + lc_[None, None, :] * lit[..., None]
    if rim:
        rc = np.array(sk.rgb(rim), np.float32)
        edge = np.clip(db - d, 0, 1) * 0 + np.clip(1 - np.abs(2 * d - 1), 0, 1) * np.clip(lit - 0.45, 0, 1) * 2.0
        col = col * (1 - 0.6 * edge[..., None]) + rc[None, None, :] * 0.6 * edge[..., None]
    a = np.clip(d ** gamma, 0, 1)
    return np.dstack([np.clip(col, 0, 255), a * 255]).astype(np.uint8)


def streak_rgba(w, h, seed, col="#FFFFFF", alpha=0.35, scale_x=260, scale_y=6, thr=0.55):
    """Yatay ince çizgi/pus dokusu (dalga parıltısı, ufuk buğusu)."""
    rs = RS(seed)
    g = rs.rand(max(2, h // scale_y + 2), max(2, w // scale_x + 2)).astype(np.float32)
    n = cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC)
    a = smoothstep_np(thr, 1.0, n) * alpha
    r, gr, b = sk.rgb(col)
    out = np.zeros((h, w, 4), np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = r, gr, b
    out[..., 3] = (np.clip(a, 0, 1) * 255).astype(np.uint8)
    return out


# ───────────────────────────── dalga şeritleri ─────────────────────────────
def _crest_fn(theta, sharp):
    """Keskin tepeli, yayvan çukurlu dalga profili (trokoid benzeri), 0..1 (1 = tepe)."""
    return ((np.cos(theta) + 1) * 0.5) ** sharp


@lru_cache(maxsize=96)
def wave_strip(period, hs, amp, body, crest, foam, seed, sharp=2.2, foam_amt=0.0, glint=None, glint_amt=0.0, facets=3, shade="#000000", comps=((2, 1.0), (3, 0.8), (5, 0.5), (8, 0.28), (13, 0.14)), lit_dir=1.0):
    """Yatay dikişsiz dalga şeridi (period × hs). Üst kenar = dalga profili (saydam üstü), gövde: crest→body degrade.
    Yüzey eğimine göre aydınlık/gölge (ışığa bakan yüzler parlak). Zamanla yatay kaydırılarak basılır. amp: tepeden çukura piksel."""
    rs = RS(seed)
    img = skia.Surface(period, hs)
    c = img.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    f = sk.Frame.__new__(sk.Frame)
    f.w, f.h, f.surf, f.c = period, hs, img, c
    step = 4
    xs = np.arange(0, period + 1, step, dtype=np.float32)
    prof = np.zeros_like(xs)
    for k, a in comps:
        ph = rs.rand() * 6.283
        prof += a * (0.6 + 0.8 * rs.rand()) * _crest_fn(2 * np.pi * k * xs / period + ph, sharp)
    prof = (prof - prof.min()) / max(1e-6, prof.max() - prof.min())
    ytop = amp * (1 - prof)               # tepe: y=0, çukur: y=amp
    pts = [(float(x), float(y)) for x, y in zip(xs, ytop)]
    slope = np.gradient(ytop, step)      # +: aşağı (sağa doğru çukur)

    def fill_path(dy=0.0):
        p = skia.Path()
        p.moveTo(-2, hs + 4)
        for (x, y) in pts:
            p.lineTo(x, y + dy)
        p.lineTo(period + 2, hs + 4)
        p.close()
        return p

    # gövde: üst açık → gövde rengi
    f.path(fill_path(), shader=f.lin(0, 0, 0, hs, [(mix(body, crest, 0.34), 0.0), (mix(body, crest, 0.10), min(0.5, 0.12 + amp / max(1, hs) * 0.8)), (body, min(0.95, 0.30 + amp / max(1, hs) * 1.4)), (body, 1.0)]))
    # çukur gölgeleri
    for q in range(facets):
        dy = amp * (0.30 + 0.30 * q)
        a_q = int(255 * (0.13 + 0.05 * q))
        yfade = min(hs - 2, amp * (1.5 + 0.5 * q) + dy)
        f.path(fill_path(dy), shader=f.lin(0, dy, 0, yfade + 6, [(shade, 0.0, a_q), (shade, 1.0, 0)]))
    # eğime göre parlak/gölgeli yüzler
    for pass_i, (th, al) in enumerate(((0.42, 0.40), (0.20, 0.55))):
        for i in range(len(xs) - 1):
            sl = float(slope[i]) * lit_dir
            br = max(0.0, min(1.0, 0.45 - sl * 0.07))           # ışığa dönük (eğim aşağı = sol yüz...) basit model
            col = mix(shade, crest, br)
            d = amp * th
            q = [pts[i], pts[i + 1], (pts[i + 1][0], pts[i + 1][1] + d), (pts[i][0], pts[i][1] + d)]
            f.poly(q, color=col, alpha=al * (0.35 + 0.65 * br) if pass_i == 0 else al * br)
    # tepe ışığı
    top = skia.Path()
    top.moveTo(*pts[0])
    for (x, y) in pts[1:]:
        top.lineTo(x, y)
    f.path(top, style="stroke", sw=max(1.2, hs * 0.028), color=crest, alpha=0.80)
    f.path(top, style="stroke", sw=max(3.0, hs * 0.07), color=crest, alpha=0.14)
    # köpük (fırtına)
    if foam_amt > 0:
        n = int(period / 12 * foam_amt)
        for _ in range(n):
            xi = rs.randint(0, len(xs) - 1)
            if prof[xi] < 0.55:
                continue
            x, y = pts[xi]
            L = 6 + rs.rand() * 30 * (0.4 + foam_amt)
            yy = y + 1 + rs.rand() * amp * 0.30
            f.line(x, yy, x + L, yy + (rs.rand() - 0.5) * 2, color=foam, sw=1.2 + rs.rand() * 2.2, alpha=0.25 + 0.55 * rs.rand())
        for _ in range(int(n * 0.9)):
            xi = rs.randint(0, len(xs) - 1)
            if prof[xi] < 0.5:
                continue
            x, y = pts[xi]
            f.circle(x + (rs.rand() - 0.5) * 20, y + rs.rand() * amp * 0.55, 0.8 + rs.rand() * 1.9, color=foam, alpha=0.3 + 0.55 * rs.rand())
    # ışık parıltıları
    if glint and glint_amt > 0:
        for _ in range(int(period / 16 * glint_amt)):
            xi = rs.randint(0, len(xs) - 1)
            if prof[xi] < 0.35:
                continue
            x, y = pts[xi]
            L = 4 + rs.rand() * 20
            yy = y + 2 + rs.rand() * amp * 0.7
            f.line(x, yy, x + L, yy, color=glint, sw=1.0 + rs.rand() * 1.6, alpha=0.2 + 0.6 * rs.rand())
    return img.makeImageSnapshot().withDefaultMipmaps()


def draw_strip(f, img, x_lo, x_hi, y, off, alpha=1.0, sy=1.0):
    """img'i [x_lo,x_hi] aralığına yatay döşe; off: kayma (piksel)."""
    P = img.width()
    p = skia.Paint()
    if alpha < 1:
        p.setAlphaf(alpha)
    start = x_lo - (off % P) - P
    x = start
    f.c.save()
    if sy != 1.0:
        f.c.translate(0, y)
        f.c.scale(1.0, sy)
        y = 0
    while x < x_hi:
        f.c.drawImage(img, x, y, LIN, p)
        x += P
    f.c.restore()


# ───────────────────────────── sancak ─────────────────────────────
def crescent_path(cx, cy, r, tilt=0.0):
    a = skia.Path()
    a.addCircle(cx, cy, r)
    b = skia.Path()
    b.addCircle(cx + r * 0.38 * math.cos(tilt), cy + r * 0.38 * math.sin(tilt), r * 0.82)
    return skia.Op(a, b, skia.PathOp.kDifference_PathOp)


def star_path(cx, cy, r, n=5, rot=-math.pi / 2):
    pts = []
    for i in range(n * 2):
        rr = r if i % 2 == 0 else r * 0.42
        a = rot + math.pi * i / n
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return sk.poly_path(pts, True)


def flag_cloth(f, x, y, w, h, col, t, emblem="cross", trim=None, wind=1, seed=0, amp=0.16, speed=4.2, nseg=10, cut=None, emb="#F2E6C4", pole=None):
    """Dalgalanan sancak: direk (x,y) noktasında, rüzgâr yönünde w uzunluğunda. emblem: cross|crescent|saltire|none.
    Kumaş gölgelendirmesi dalga türevinden. Yalnız küçük yollar çizer (dyn için uygun)."""
    wind = 1 if wind >= 0 else -1
    ph0 = seed * 1.7
    xs = [i / nseg for i in range(nseg + 1)]
    top, bot, mids = [], [], []
    for u in xs:
        rip = math.sin(t * speed - u * 5.2 + ph0) * h * amp * (0.2 + u) + math.sin(t * speed * 1.7 - u * 9.0 + ph0 * 2) * h * amp * 0.25 * u
        xx = x + wind * u * w * (1 - 0.06 * abs(math.sin(t * speed * 0.5 + ph0)) * u)
        fl = (h * (1 - 0.18 * u)) if cut == "taper" else h
        top.append((xx, y + rip))
        bot.append((xx, y + rip + fl))
        mids.append((xx, y + rip + fl * 0.5, math.cos(t * speed - u * 5.2 + ph0)))
    dark, light = darken(col, 0.38), lighten(col, 0.22)
    for i in range(nseg):
        sh = 0.5 + 0.5 * mids[i][2]
        cc = mix(dark, light, sh)
        q = [top[i], top[i + 1], bot[i + 1], bot[i]]
        if cut == "swallow" and i == nseg - 1:
            q = [top[i], top[i + 1], ((top[i + 1][0] + bot[i + 1][0]) / 2 - wind * w * 0.09, (top[i + 1][1] + bot[i + 1][1]) / 2), bot[i + 1], bot[i]]
        f.poly(q, color=cc)
    if trim:
        f.path(sk.poly_path(top, False), style="stroke", sw=max(1.2, h * 0.07), color=trim, alpha=0.9)
        f.path(sk.poly_path(bot, False), style="stroke", sw=max(1.2, h * 0.07), color=trim, alpha=0.9)
    # arma
    k = int(nseg * 0.5)
    ex, ey = mids[k][0], mids[k][1]
    if emblem == "cross":
        # yatay kol (u 0.18..0.82, v 0.42..0.58)
        a_, b_ = int(nseg * 0.18 + 0.5), int(nseg * 0.82 + 0.5)
        pa = [(top[i][0], top[i][1] + (bot[i][1] - top[i][1]) * 0.42) for i in range(a_, b_ + 1)]
        pb = [(top[i][0], top[i][1] + (bot[i][1] - top[i][1]) * 0.58) for i in range(b_, a_ - 1, -1)]
        if len(pa) >= 2:
            f.poly(pa + pb, color=emb, alpha=0.92)
        # dikey kol (u≈0.5 çevresi, v 0.12..0.88)
        i5 = nseg // 2
        i4, i6 = max(0, i5 - 1), min(nseg, i5 + 1)
        sl = (top[i6][1] - top[i4][1]) / (top[i6][0] - top[i4][0] + (1e-6 if top[i6][0] >= top[i4][0] else -1e-6))
        dx = wind * w * 0.05
        tx_, ty_ = top[i5]
        bx_, by_ = bot[i5]
        hgt = by_ - ty_
        f.poly([(tx_ - dx, ty_ + hgt * 0.12 - sl * dx), (tx_ + dx, ty_ + hgt * 0.12 + sl * dx), (bx_ + dx, ty_ + hgt * 0.88 + sl * dx), (bx_ - dx, ty_ + hgt * 0.88 - sl * dx)], color=emb, alpha=0.92)
    elif emblem == "saltire":
        for sgn in (1, -1):
            seq = []
            for i in range(int(nseg * 0.2), int(nseg * 0.85) + 1):
                u = (xs[i] - 0.2) / 0.65
                v = 0.5 + sgn * (u - 0.5) * 0.9
                seq.append((top[i][0], top[i][1] + (bot[i][1] - top[i][1]) * v))
            f.path(sk.poly_path(seq, False), style="stroke", sw=max(2.0, h * 0.13), color=emb, alpha=0.9, cap="butt")
    elif emblem == "crescent":
        rr = h * 0.27
        f.path(crescent_path(ex - wind * w * 0.04, ey, rr, 0.0 if wind > 0 else math.pi), color=emb, alpha=0.95)
        f.path(star_path(ex + wind * rr * 0.55, ey, rr * 0.34), color=emb, alpha=0.95)
    if pole:
        f.line(x, y - h * 0.15, x, y + h * 1.6, color=pole, sw=max(2, h * 0.07))


# ───────────────────────────── parçacık yardımcıları ─────────────────────────────
def rain_lines(f, t, n=240, seed=8, angle=-0.28, length=34, alpha=0.35, color="#BFD0DC", speed=1500, sw=1.4, rect=(-300, -300, 2520, 1680)):
    """Tek Path'te toplu yağmur çizgileri (kare başına 1 draw)."""
    rs = RS(seed)
    x0, y0, w, h = rect
    d = 0.5 + rs.rand(n) * 0.5
    s = (t * speed * d / 1000.0 + rs.rand(n)) % 1.0
    dx, dy = math.sin(-angle), math.cos(angle)
    px = (rs.rand(n) * (w + 400) + s * 400 * dx) % (w + 400) - 200 + x0
    py = s * (h + 100) - 50 + y0
    p = skia.Path()
    for i in range(n):
        p.moveTo(float(px[i]), float(py[i]))
        p.lineTo(float(px[i] + dx * length * d[i]), float(py[i] + dy * length * d[i]))
    pa = skia.Paint(AntiAlias=True, Color=C(color, int(255 * alpha)), StrokeWidth=sw, Style=skia.Paint.kStroke_Style)
    f.c.drawPath(p, pa)


def lightning_bolt_path(x0, y0, x1, y1, seed, jag=60, depth=5):
    rs = RS(seed)
    pts = [(x0, y0), (x1, y1)]
    for d in range(depth):
        new = [pts[0]]
        for (ax, ay), (bx, by) in zip(pts[:-1], pts[1:]):
            mx, my = (ax + bx) / 2, (ay + by) / 2
            L = math.hypot(bx - ax, by - ay)
            nx, ny = -(by - ay) / max(1e-6, L), (bx - ax) / max(1e-6, L)
            off = (rs.rand() - 0.5) * jag * (0.55 ** d) * 1.6
            new.append((mx + nx * off, my + ny * off))
            new.append((bx, by))
        pts = new
    return pts


@lru_cache(maxsize=24)
def bolt_sprite(seed, length=620, col="#DDE8FF"):
    """Şimşek: ana çatal + dallar; ışıma (bulanık) pişirmede."""
    rs = RS(seed)
    wd, ht = 560, int(length + 80)
    s = skia.Surface(wd, ht)
    c = s.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    f = sk.Frame.__new__(sk.Frame)
    f.w, f.h, f.surf, f.c = wd, ht, s, c
    main = lightning_bolt_path(wd * 0.5, 4, wd * 0.5 + (rs.rand() - 0.5) * 140, length, seed, jag=70)
    branches = []
    for k in range(3):
        i = rs.randint(len(main) // 5, len(main) * 3 // 4)
        bx, by = main[i]
        ex, ey = bx + (rs.rand() - 0.5) * 300, by + 90 + rs.rand() * 180
        branches.append(lightning_bolt_path(bx, by, ex, ey, seed + 10 + k, jag=40, depth=4))
    for blur, sw, a in ((16, 16, 0.55), (6, 7, 0.7)):
        for pts in [main] + branches:
            f.path(sk.poly_path(pts, False), style="stroke", sw=sw * (1 if pts is main else 0.6), color=col, alpha=a, blur=blur)
    for pts in [main] + branches:
        f.path(sk.poly_path(pts, False), style="stroke", sw=3.2 if pts is main else 1.8, color="#FFFFFF", alpha=1.0, join="round")
    return s.makeImageSnapshot()


def bake_sprite(draw_fn, w, h, ox, oy, mip=True):
    """draw_fn(f) → (img, ox, oy). Orijin (ox,oy) sprite içinde."""
    s = skia.Surface(int(w), int(h))
    c = s.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    f = sk.Frame.__new__(sk.Frame)
    f.w, f.h, f.surf, f.c = int(w), int(h), s, c
    c.translate(ox, oy)
    draw_fn(f)
    im = s.makeImageSnapshot()
    return im.withDefaultMipmaps() if mip else im


def draw_rolled(cs, img, ox, oy, theta, samp=None, paint=None, step=8.0, kx=1.0):
    """Küçük açılı 'dönme'yi dikey dilimlerle taklit eder (Skia'nın hızlı yolu: yalnız ölçek+öteleme; gerçek döndürme ~8× yavaş).
    cs: tuval — orijin (su hattı) çevirisi ve ölçek (görüntü piksel birimine) uygulanmış olmalı; theta: yerel eksende radyan (+: saat yönü).
    kx: görüntü pikselinin ekrandaki yaklaşık boyutu (dilim genişliğini ekranda ≈ step px yapmak için)."""
    samp = samp or LIN
    paint = paint or skia.Paint()
    w, h = img.width(), img.height()
    tn = math.tan(theta)
    sl = max(4, int(step / max(0.05, kx)))
    x0 = 0
    while x0 < w:
        x1 = min(w, x0 + sl)
        dy = tn * ((x0 + x1) * 0.5 - ox)
        cs.drawImageRect(img, skia.Rect.MakeLTRB(x0, 0, x1, h), skia.Rect.MakeLTRB(x0 - ox, -oy + dy, x1 - ox, h - oy + dy), samp, paint, skia.Canvas.kStrict_SrcRectConstraint)
        x0 = x1
