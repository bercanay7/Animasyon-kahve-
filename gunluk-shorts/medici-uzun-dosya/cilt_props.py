"""cilt_props — Medici cildi rekvizitleri: palle arması, florin (zambak / Vaftizci Yahya), zambak (giglio), yaldızlı-minelı kabartma yardımcıları.

Yaklaşım: her nesne bir YÜKSEKLİK HARİTASI (maskelerden) + bölge renk maskeleri; tek ışık (sol-üst) ile gölgelendirilir;
bölge başına metal/mine rampası (yaldız, sinabar mine, lapis mine) seçilir. Sonuç RGBA sprite (önbellekli).
"""
import functools
import math

import cv2
import numpy as np
import skia

import cilt_medici as CM
import sk
from sk import C, Frame, H, W, clamp, smooth

LX, LY = -0.55, -0.62
LZ = math.sqrt(1 - LX * LX - LY * LY)


# ───────────────────────────── çizim → maske ─────────────────────────────
class Mask:
    """S×S tek kanallı çizim yüzeyi (beyaz = dolu)."""

    def __init__(self, S):
        self.S = S
        self.s = skia.Surface(S, S)
        self.c = self.s.getCanvas()
        self.c.clear(skia.ColorBLACK)

    def paint(self, v=255, style="fill", w=1.0):
        p = skia.Paint(AntiAlias=True, Color=skia.Color(v, v, v, 255))
        if style == "stroke":
            p.setStyle(skia.Paint.kStroke_Style)
            p.setStrokeWidth(w)
            p.setStrokeCap(skia.Paint.kRound_Cap)
            p.setStrokeJoin(skia.Paint.kRound_Join)
        return p

    def fill(self, path, v=255):
        self.c.drawPath(path, self.paint(v))

    def stroke(self, path, w, v=255):
        self.c.drawPath(path, self.paint(v, "stroke", w))

    def circle(self, x, y, r, v=255):
        self.c.drawCircle(x, y, r, self.paint(v))

    def ring(self, x, y, r, w, v=255):
        self.c.drawCircle(x, y, r, self.paint(v, "stroke", w))

    def arr(self):
        a = self.s.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)[..., 0]
        return a.astype(np.float32) / 255.0


def shade_height(Hh, strength=1.0, spec_pow=30.0, blur=1.0):
    """Yükseklikten (px biriminde) Lambert + özgül parlama. Dönüş: (shade 0..1 (0.5=düz), spec 0..1)."""
    Hh = Hh.astype(np.float32)
    h = cv2.GaussianBlur(Hh, (0, 0), blur) if blur > 0 else Hh
    gx = cv2.Sobel(h, cv2.CV_32F, 1, 0, ksize=3) * 0.125 * strength
    gy = cv2.Sobel(h, cv2.CV_32F, 0, 1, ksize=3) * 0.125 * strength
    inv = 1.0 / np.sqrt(gx * gx + gy * gy + 1.0)
    nx, ny, nz = -gx * inv, -gy * inv, inv
    dif = np.clip(nx * LX + ny * LY + nz * LZ, 0, 1)
    shade = np.clip(0.5 + (dif - LZ) * 2.4, 0, 1)
    hx, hy, hz = LX, LY, LZ + 1.0
    hn = math.sqrt(hx * hx + hy * hy + hz * hz)
    sp = np.clip((nx * hx + ny * hy + nz * hz) / hn, 0, 1) ** spec_pow
    return shade, sp


ENAMEL = dict(
    red=[("#1E0504", 0.0), ("#5E140E", 0.28), ("#A02A1C", 0.52), ("#C84A32", 0.78), ("#EE9A82", 1.0)],
    blue=[("#060A22", 0.0), ("#112468", 0.28), ("#2447A0", 0.55), ("#587FD6", 0.82), ("#A6C0F4", 1.0)],
    green=[("#0C1A10", 0.0), ("#2A4A30", 0.30), ("#4F7E50", 0.58), ("#86B27C", 0.85), ("#CCE4B4", 1.0)],
)


def _lambert(Hh, strength=1.0, blur=1.1):
    h = cv2.GaussianBlur(Hh.astype(np.float32), (0, 0), blur)
    gx = cv2.Sobel(h, cv2.CV_32F, 1, 0, ksize=3) * 0.125 * strength
    gy = cv2.Sobel(h, cv2.CV_32F, 0, 1, ksize=3) * 0.125 * strength
    inv = 1.0 / np.sqrt(gx * gx + gy * gy + 1.0)
    return np.clip(-gx * inv * LX + -gy * inv * LY + inv * LZ, 0, 1)


def ramp_enamel(name, dif):
    ramp = sk._grad_ramp(ENAMEL[name])
    return ramp[np.clip(dif * 255, 0, 255).astype(np.int32)]


def ramp_color(metal, shade):
    ramp = sk._grad_ramp(sk.METAL[metal])
    return ramp[np.clip(shade * 255, 0, 255).astype(np.int32)]


def _soft(m, s=1.2):
    return cv2.GaussianBlur(m, (0, 0), s)


def ring_text(S, text, radius, size_px, track=4.0, face="title", cx=None, cy=None, start=-math.pi / 2, center=True):
    """Daire boyunca yazı maskesi (üstten ortalı, saat yönünde). S×S float32."""
    cx = S / 2 if cx is None else cx
    cy = S / 2 if cy is None else cy
    s = skia.Surface(S, S)
    c = s.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    wid = sk.text_width(text, face, size_px, track)
    ang0 = start - (wid / radius / 2 if center else 0)
    x = 0.0
    for ch in text:
        w = sk.text_width(ch, face, size_px, 0)
        a = ang0 + (x + w / 2) / radius
        c.save()
        c.translate(cx + math.cos(a) * radius, cy + math.sin(a) * radius)
        c.rotate(math.degrees(a + math.pi / 2))
        blob, _ = sk.text_blob(face, ch, size_px, 0)
        c.drawTextBlob(blob, -w / 2, size_px * 0.36, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
        c.restore()
        x += w + track
    return s.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)[..., 3].astype(np.float32) / 255.0


# ───────────────────────────── zambak (giglio) ─────────────────────────────
def lily_path(cx, cy, s):
    """Floransa zambağı (giglio): ortada petal, iki yanda kıvrık petal, aralarda organ çubukları, bant ve taban. Yükseklik ≈ s."""
    p = skia.Path()

    def P(x, y):
        return (cx + x * s, cy + y * s)

    def sm(pts, close=True, t=0.5):
        return sk.smooth_path([P(*q) for q in pts], close, t)
    p.addPath(sm([(0, -0.50), (0.06, -0.38), (0.085, -0.22), (0.07, -0.08), (0.03, 0.03), (0, 0.06), (-0.03, 0.03), (-0.07, -0.08), (-0.085, -0.22), (-0.06, -0.38)], True, 0.5))
    for sg in (-1, 1):
        p.addPath(sm([(sg * 0.03, 0.02), (sg * 0.13, -0.02), (sg * 0.25, -0.10), (sg * 0.34, -0.22), (sg * 0.37, -0.33), (sg * 0.33, -0.40), (sg * 0.27, -0.37),
                      (sg * 0.27, -0.30), (sg * 0.22, -0.20), (sg * 0.15, -0.10), (sg * 0.07, -0.04)], True, 0.5))
        # organ çubukları
        p.addRect(skia.Rect.MakeLTRB(*P(sg * 0.125 - 0.012, -0.28), *P(sg * 0.125 + 0.012, -0.04)))
        p.addCircle(*P(sg * 0.125, -0.30), 0.028 * s)
        # alt kıvrımlar (yaprak)
        p.addPath(sm([(sg * 0.05, 0.14), (sg * 0.16, 0.16), (sg * 0.26, 0.24), (sg * 0.28, 0.34), (sg * 0.22, 0.38), (sg * 0.17, 0.32), (sg * 0.10, 0.25)], True, 0.5))
    p.addRoundRect(skia.Rect.MakeLTRB(*P(-0.20, 0.060), *P(0.20, 0.135)), 0.02 * s, 0.02 * s)
    p.addPath(sm([(-0.06, 0.13), (0.06, 0.13), (0.075, 0.30), (0.0, 0.50), (-0.075, 0.30)], True, 0.4))
    return p


def lily_mask(m, cx, cy, s, v=255):
    m.fill(lily_path(cx, cy, s), v)


# ───────────────────────────── PALLE ARMASI ─────────────────────────────
ARMS_S = 1000
SHIELD_BOX = (100, 60, 900, 960)
BALLS = [(500, 232, 124, "blue"), (276, 346, 102, "red"), (724, 346, 102, "red"), (318, 600, 102, "red"), (682, 600, 102, "red"), (500, 790, 102, "red")]


def shield_path(inset=0.0):
    x0, y0, x1, y1 = SHIELD_BOX
    x0, y0, x1, y1 = x0 + inset, y0 + inset, x1 - inset, y1 - inset
    p = skia.Path()
    r = 46
    p.moveTo(x0 + r, y0)
    p.lineTo(x1 - r, y0)
    p.quadTo(x1, y0, x1, y0 + r)
    p.lineTo(x1, y0 + (y1 - y0) * 0.50)
    p.cubicTo(x1, y0 + (y1 - y0) * 0.78, (x0 + x1) / 2 + (x1 - x0) * 0.20, y1 - (y1 - y0) * 0.08, (x0 + x1) / 2, y1)
    p.cubicTo((x0 + x1) / 2 - (x1 - x0) * 0.20, y1 - (y1 - y0) * 0.08, x0, y0 + (y1 - y0) * 0.78, x0, y0 + (y1 - y0) * 0.50)
    p.lineTo(x0, y0 + r)
    p.quadTo(x0, y0, x0 + r, y0)
    p.close()
    return p


@functools.lru_cache(maxsize=8)
def arms_array(size=1000, field="gold", flat=False):
    """Palle arması RGBA uint8 (size×size). Yaldızlı sivri-tane (punch) zeminli altın alan, boncuklu kenar, kırmızı mine toplar,
    üstte lapis top üzerinde 3 zambak. field: 'gold' | 'bone' (sıvaya boyalı beyaz alan)."""
    S = ARMS_S
    Msh = Mask(S); Msh.fill(shield_path(0))
    msh = Msh.arr()
    # kenar bandı + boncuk halkası
    Mr = Mask(S); Mr.stroke(shield_path(26), 26)
    mrim = Mr.arr()
    Mi = Mask(S); Mi.stroke(shield_path(62), 4)
    minner = Mi.arr()
    Mb = Mask(S)
    pm = skia.PathMeasure(shield_path(44), True)
    L = pm.getLength()
    n = int(L / 22)
    for i in range(n):
        pos, _ = pm.getPosTan(L * i / n)
        Mb.circle(pos.x(), pos.y(), 6.5)
    mbead = Mb.arr()
    # toplar
    Hh = np.zeros((S, S), np.float32)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    red_m = np.zeros((S, S), np.float32)
    blue_m = np.zeros((S, S), np.float32)
    collar = np.zeros((S, S), np.float32)
    for (bx, by, br, kind) in BALLS:
        d = np.hypot(xx - bx, yy - by)
        inside = d < br
        dome = np.where(inside, np.sqrt(np.clip(1 - (d / br) ** 2, 0, 1)) * br * 0.62, 0)
        Hh = np.maximum(Hh, dome + inside * 10)
        a = np.clip((br - d) / 1.6, 0, 1)
        (blue_m if kind == "blue" else red_m)[:] = np.maximum(blue_m if kind == "blue" else red_m, a)
        collar = np.maximum(collar, np.clip(1 - np.abs(d - (br + 7)) / 5.0, 0, 1))
    # zambaklar (mavi topta, 2 üstte + 1 altta)
    Ml = Mask(S)
    bx, by, br, _ = BALLS[0]
    for (dx, dy, sc) in ((-0.36, -0.14, 0.80), (0.36, -0.14, 0.80), (0.0, 0.34, 0.84)):
        lily_mask(Ml, bx + dx * br, by + dy * br, br * sc)
    mlily = Ml.arr()
    # yükseklik bileşimi
    base = 26.0
    Hh = Hh + base * msh
    Hh += 34 * _soft(mrim, 3.0) + 26 * _soft(mbead, 1.0) + 8 * _soft(minner, 1.5)
    Hh += 22 * collar
    Hh += mlily * 16.0
    # sivri-tane (punch) deseni: altın alanda ince nokta ızgarası (çukur)
    pun = np.zeros((S, S), np.float32)
    if not flat:
        step = 17
        Mpn = Mask(S)
        for j in range(0, S, step):
            for i in range(0, S, step):
                ox = (step // 2 if (j // step) % 2 else 0)
                Mpn.circle(i + ox, j, 1.7)
        pun = Mpn.arr()
        field_zone = np.clip(msh - _soft(mrim, 8.0) * 1.3, 0, 1) * (1 - np.clip(red_m + blue_m + collar * 1.5, 0, 1))
        Hh -= pun * field_zone * 4.0
    Hh = Hh * (msh > 0.02)
    # gölgelendirme
    sh_g, sp_g = shade_height(Hh, strength=1.25, spec_pow=26.0, blur=1.1)
    sh_e, sp_e = shade_height(Hh, strength=1.0, spec_pow=70.0, blur=1.1)
    tex = CM._crinkle((S, S), 5, 1.0)
    gold = ramp_color("leaf", sh_g) * (0.90 + 0.20 * tex[..., None]) + sp_g[..., None] * 255 * 0.62
    if field == "bone":
        gold = ramp_color("leaf_dim", sh_g) * 0.0 + np.array([232, 224, 200], np.float32) * (0.55 + 0.9 * sh_g[..., None] * 0.6) + sp_g[..., None] * 40
    dif_e = _lambert(Hh, 1.0)
    red = ramp_enamel("red", dif_e) + sp_e[..., None] * 255 * 0.95
    blue = ramp_enamel("blue", dif_e) + sp_e[..., None] * 255 * 0.9
    lil = ramp_color("leaf", sh_g) * (0.92 + 0.16 * tex[..., None]) + sp_g[..., None] * 255 * 0.7
    col = gold
    col = col * (1 - red_m[..., None]) + red * red_m[..., None]
    col = col * (1 - blue_m[..., None]) + blue * blue_m[..., None]
    lm = np.clip(mlily, 0, 1)[..., None]
    col = col * (1 - lm) + lil * lm
    # sivri-tane çukurlarının içi biraz koyu (derin) + parıltı
    col *= (1 - 0.30 * pun[..., None] * (1 - np.clip(red_m + blue_m, 0, 1))[..., None])
    a = np.clip(msh, 0, 1) * 255
    out = np.dstack([np.clip(col, 0, 255), a]).astype(np.uint8)
    if size != S:
        out = cv2.resize(out, (size, size), interpolation=cv2.INTER_AREA)
    return out


@functools.lru_cache(maxsize=8)
def arms_image(size=1000, field="gold", flat=False):
    return sk.np_to_image(arms_array(size, field, flat))


@functools.lru_cache(maxsize=8)
def arms_soft(kind="shadow"):
    """Önbellekli bulanık gölge / sıcak ışıma (1000×1000 uzayında)."""
    a = arms_array(1000)[..., 3]
    if kind == "shadow":
        return CM.blur_sil(a, 14.0, (0, 0, 0))
    return CM.blur_sil(a, 24.0, (255, 214, 140))


def draw_arms(f, x, y, size=400, alpha=1.0, rot=0.0, shadow=0.55, glow=0.0, field="gold", glint=None):
    """Palle armasını (x,y) merkezine çiz. glint: 0..1 yaldız üzerinde gezinen parlama bandı."""
    img = arms_image(1000, field)
    s = size / 1000.0
    c = f.c
    if shadow > 0:
        c.save(); c.translate(x + size * 0.018, y + size * 0.035)
        if rot:
            c.rotate(math.degrees(rot))
        c.scale(s, s)
        p = skia.Paint(AntiAlias=True)
        p.setAlphaf(clamp(shadow * alpha))
        c.drawImage(arms_soft("shadow"), -500, -515, CM._LIN, p)
        c.restore()
    if glow > 0:
        c.save(); c.translate(x, y); c.scale(s * 1.03, s * 1.03)
        p = skia.Paint(AntiAlias=True)
        p.setAlphaf(clamp(glow * alpha))
        c.drawImage(arms_soft("glow"), -500, -515, CM._LIN, p)
        c.restore()
    c.save(); c.translate(x, y)
    if rot:
        c.rotate(math.degrees(rot))
    c.scale(s, s)
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(clamp(alpha))
    c.drawImage(img, -500, -515, CM._LIN, p)
    if glint is not None:
        gx = -700 + 1400 * glint
        L_, R_ = max(-520.0, gx - 170), min(520.0, gx + 170)
        if R_ > L_:
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(L_, -540, R_, 540))
            c.saveLayer(skia.Rect.MakeLTRB(L_, -540, R_, 540), None)
            c.drawImage(img, -500, -515, CM._LIN, skia.Paint(AntiAlias=True))
            sh = skia.GradientShader.MakeLinear([(gx - 150, -400), (gx + 150, 400)], [C("#FFFFFF", 0), C("#FFF1BE", int(150 * alpha)), C("#FFFFFF", 0)], [0, 0.5, 1])
            c.drawRect(skia.Rect.MakeLTRB(L_, -540, R_, 540), skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kSrcATop))
            c.restore()
            c.restore()
    c.restore()


# ───────────────────────────── FLORİN ─────────────────────────────
COIN_S = 760


def _john_figure(m, cx, cy, s):
    """Vaftizci Yahya (florin arka yüz): hale, baş, deve tüyü cüppe, haçlı asa, kaldırılmış sağ el. Sola bakar. s = figür boyu."""
    def P(x, y):
        return (cx + x * s, cy + y * s)
    m.ring(*P(0.005, -0.405), 0.082 * s, 0.014 * s)                                     # hale
    m.fill(sk.smooth_path([P(-0.040, -0.452), P(0.005, -0.478), P(0.045, -0.452), P(0.045, -0.395), P(0.018, -0.352), P(-0.026, -0.352), P(-0.052, -0.385)], True, 0.5))  # baş
    m.fill(sk.smooth_path([P(-0.056, -0.385), P(-0.026, -0.352), P(0.018, -0.352), P(0.004, -0.298), P(-0.030, -0.290), P(-0.060, -0.335)], True, 0.5))                   # sakal
    # cüppe: omuz → bel → dalgalı etek
    m.fill(sk.smooth_path([P(-0.045, -0.335), P(0.050, -0.335), P(0.078, -0.20), P(0.088, -0.02), P(0.104, 0.16), P(0.098, 0.31), P(0.060, 0.345), P(0.0, 0.325),
                           P(-0.06, 0.345), P(-0.104, 0.31), P(-0.098, 0.16), P(-0.082, -0.02), P(-0.074, -0.20)], True, 0.4))
    # kollar: sol kol asayı tutar, sağ kol kutsama
    m.stroke(sk.poly_path([P(-0.060, -0.28), P(-0.115, -0.15), P(-0.140, -0.04)], False), 0.032 * s)
    m.stroke(sk.poly_path([P(0.055, -0.28), P(0.125, -0.33), P(0.150, -0.405)], False), 0.030 * s)
    m.circle(*P(0.153, -0.418), 0.019 * s)
    # asa + haç
    m.stroke(sk.poly_path([P(-0.165, 0.40), P(-0.145, -0.56)], False), 0.016 * s)
    m.stroke(sk.poly_path([P(-0.215, -0.50), P(-0.090, -0.505)], False), 0.016 * s)
    m.circle(*P(-0.1495, -0.575), 0.016 * s)
    # ayaklar
    m.fill(sk.smooth_path([P(-0.090, 0.335), P(-0.010, 0.335), P(-0.020, 0.375), P(-0.130, 0.375)], True, 0.2))
    m.fill(sk.smooth_path([P(0.010, 0.335), P(0.088, 0.335), P(0.120, 0.375), P(0.0, 0.375)], True, 0.2))


def _john_cuts(Hh, cx, cy, s, depth):
    """Cüppe kıvrımları ve kemer: yüksekliği oyarak (çizgiler)."""
    Mk = Mask(Hh.shape[0])
    def P(x, y):
        return (cx + x * s, cy + y * s)
    for (x0, x1) in ((-0.045, -0.060), (0.0, 0.0), (0.045, 0.058)):
        Mk.stroke(sk.smooth_path([P(x0, -0.05), P((x0 + x1) / 2, 0.15), P(x1, 0.32)], False, 0.5), 0.0085 * s)
    Mk.stroke(sk.poly_path([P(-0.085, -0.045), P(0.085, -0.055)], False), 0.011 * s)
    return Hh - Mk.arr() * depth


@functools.lru_cache(maxsize=8)
def coin_array(face="obv", size=760):
    """Florin yüzü RGBA. obv: zambak + 'FLORENTIA'; rev: Vaftizci Yahya + 'S IOHANNES B'. Elle basılmış hafif düzensiz kenar, boncuk halka."""
    S = COIN_S
    cx = cy = S / 2
    R = S * 0.46
    rs = np.random.RandomState(4 if face == "obv" else 9)
    ang = np.linspace(0, 2 * math.pi, 120, endpoint=False)
    rr = R * (1 + 0.006 * np.sin(ang * 3 + 1) + 0.004 * np.sin(ang * 7) + 0.0025 * rs.randn(len(ang)))
    outline = sk.smooth_path([(cx + math.cos(a) * r, cy + math.sin(a) * r) for a, r in zip(ang, rr)], True, 0.5)
    Md = Mask(S); Md.fill(outline)
    disc = Md.arr()
    Hh = np.zeros((S, S), np.float32)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    d = np.hypot(xx - cx, yy - cy)
    Hh += disc * 12
    Hh += np.exp(-((d - R * 0.972) / (S * 0.017)) ** 2) * 30            # dış çıkıntılı kenar
    Hh += np.exp(-((d - R * 0.66) / (S * 0.0075)) ** 2) * 18            # iç halka
    Mb = Mask(S)
    n = 60
    for i in range(n):
        a = 2 * math.pi * i / n
        Mb.circle(cx + math.cos(a) * R * 0.915, cy + math.sin(a) * R * 0.915, S * 0.0085)
    Hh += _soft(Mb.arr(), 0.7) * 22
    Ms = Mask(S)
    if face == "obv":
        lily_mask(Ms, cx, cy + S * 0.004, S * 0.46)
    else:
        _john_figure(Ms, cx + S * 0.012, cy + S * 0.020, S * 0.52)
    sym = Ms.arr()
    Hh += _soft(sym, 0.9) * 40
    if face == "rev":
        Hh = _john_cuts(Hh, cx + S * 0.012, cy + S * 0.020, S * 0.52, 16)
    text = " FLORENTIA " if face == "obv" else " S · IOHANNES · B "
    mm = ring_text(S, text, R * 0.795, int(S * 0.064), track=S * 0.011, face="title")
    Hh += _soft(mm, 0.7) * 34
    Hh += (CM.CW.lf(rs, S, S, 70) * 0.9 + CM.CW.gn(rs, S, S, 2.0) * 0.18) * disc
    Hh *= (disc > 0.02)
    sh, sp = shade_height(Hh, strength=1.35, spec_pow=26.0, blur=0.9)
    tex = CM._crinkle((S, S), 13, 0.45)
    col = ramp_color("leaf", sh) * (0.94 + 0.12 * tex[..., None]) + sp[..., None] * 255 * 0.50
    a = np.clip(disc, 0, 1) * 255
    out = np.dstack([np.clip(col, 0, 255), a]).astype(np.uint8)
    if size != S:
        out = cv2.resize(out, (size, size), interpolation=cv2.INTER_AREA)
    return out


@functools.lru_cache(maxsize=8)
def coin_image(face="obv", size=760):
    return sk.np_to_image(coin_array(face, size))


@functools.lru_cache(maxsize=8)
def coin_soft(kind="shadow"):
    a = coin_array("obv", 760)[..., 3]
    if kind == "shadow":
        return CM.blur_sil(a, 10.0, (0, 0, 0))
    return CM.blur_sil(a, 18.0, (255, 214, 140))


def draw_coin(f, x, y, size=420, spin=0.0, alpha=1.0, shadow=0.5, glow=0.0, thick=0.075, tilt=0.0, glint=None):
    """Florin: spin (radyan, dikey eksen etrafında): cos>0 → ön yüz (zambak), cos<0 → arka (Yahya). Kalınlık kenarı koyu altın bant."""
    cs = math.cos(spin)
    sn = math.sin(spin)
    front = "obv" if cs >= 0 else "rev"
    img = coin_image(front, 760)
    k = size / 760.0
    sx = max(0.012, abs(cs))
    thk = size * thick * abs(sn)
    c = f.c
    if shadow > 0:
        c.save(); c.translate(x + size * 0.03, y + size * 0.06 + size * 0.02)
        c.scale(k * sx, k)
        p = skia.Paint(AntiAlias=True)
        p.setAlphaf(clamp(shadow * alpha))
        c.drawImage(coin_soft("shadow"), -380, -380, CM._LIN, p)
        c.restore()
    if glow > 0:
        c.save(); c.translate(x, y); c.scale(k * sx * 1.04, k * 1.04)
        p = skia.Paint(AntiAlias=True)
        p.setAlphaf(clamp(glow * alpha))
        c.drawImage(coin_soft("glow"), -380, -380, CM._LIN, p)
        c.restore()
    c.save(); c.translate(x, y)
    if tilt:
        c.rotate(math.degrees(tilt))
    # kalınlık: arka kopya (koyu) ters yöne kaydırılmış
    if thk > 0.5:
        sgn = 1 if cs >= 0 else -1
        n = 6
        for i in range(n, 0, -1):
            off = -sgn * thk * i / n
            c.save(); c.translate(off, 0); c.scale(k * sx, k)
            p = skia.Paint(AntiAlias=True)
            p.setColorFilter(skia.ColorFilters.Matrix([0.62, 0, 0, 0, 0, 0, 0.52, 0, 0, 0, 0, 0, 0.40, 0, 0, 0, 0, 0, alpha, 0]))
            c.drawImage(img, -380, -380, CM._LIN, p)
            c.restore()
    c.save(); c.scale(k * sx, k)
    p = skia.Paint(AntiAlias=True)
    # açıya bağlı parlaklık (dönerken ışığı yakalar)
    br = 0.78 + 0.30 * abs(cs) + 0.25 * max(0.0, math.sin(spin * 2 + 0.6)) ** 3
    p.setColorFilter(skia.ColorFilters.Matrix([br, 0, 0, 0, 0, 0, br, 0, 0, 0, 0, 0, br, 0, 0, 0, 0, 0, alpha, 0]))
    c.drawImage(img, -380, -380, CM._LIN, p)
    if glint is not None:
        gx = -520 + 1040 * glint
        L_, R_ = max(-390.0, gx - 130), min(390.0, gx + 130)
        if R_ > L_:
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(L_, -390, R_, 390))
            c.saveLayer(skia.Rect.MakeLTRB(L_, -390, R_, 390), None)
            c.drawImage(img, -380, -380, CM._LIN, skia.Paint(AntiAlias=True))
            sh = skia.GradientShader.MakeLinear([(gx - 110, -300), (gx + 110, 300)], [C("#FFFFFF", 0), C("#FFF4C8", int(190 * alpha)), C("#FFFFFF", 0)], [0, 0.5, 1])
            c.drawRect(skia.Rect.MakeLTRB(L_, -390, R_, 390), skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kSrcATop))
            c.restore()
            c.restore()
    c.restore()
    c.restore()


if __name__ == "__main__":
    import time
    t = time.time()
    a = arms_array(700)
    print("arms", time.time() - t)
    t = time.time()
    c1 = coin_array("obv", 520)
    c2 = coin_array("rev", 520)
    print("coin", time.time() - t)
    bg = np.full((720, 1820, 3), (60, 52, 44), np.uint8)
    def paste(bgi, arr, x, y):
        h, w = arr.shape[:2]
        al = arr[..., 3:4].astype(np.float32) / 255
        bgi[y:y + h, x:x + w] = (bgi[y:y + h, x:x + w] * (1 - al) + arr[..., :3] * al).astype(np.uint8)
    paste(bg, a, 10, 10)
    paste(bg, c1, 740, 100)
    paste(bg, c2, 1270, 100)
    cv2.imwrite("out/frames/_props1.png", cv2.cvtColor(bg, cv2.COLOR_RGB2BGR))
