"""cilt_deniz — DENİZ, LİMAN ve GEMİ DÜNYASI (Lab-C): `deniz`, `liman` çekim türleri + yeniden kullanılabilir çizim işlevleri.

"Fresk ve defter" cildi (mürekkep dış hatlı, pigmentli, kâğıt-kesim kukla stili; fresk bandı y 150–950, asma bandı + altın filet).
Çekim türleri (hepsi `cilt_cam.OWN_CAMERA`'ya çalışma anında eklenir; `cams=[(çapa,(x,y,zoom)),…]` ya da `cam=`):
  * `deniz` (scene="acik"|"rota"|"filo"|"kiyi") + takma türler `deniz_rota`, `deniz_filo`, `deniz_kiyi`:
      acik — paralaks dalga sıraları, güneş/ay + dönen huzme + parıltı yolu, bulut/martı, gemiler (kadırga: senkron kürek çekişi, flama, tente, fener; nao/karrak: üç direk, şişen yelken, bayrak,
             halat çeken denizciler; tekne/kayık); rota — gemi `route=[(x,y),…]` boyunca ilerler (kamera izler, kuyruk köpüğü, yaldız "iplik"); filo — n kadırgalı iki filo karşılıklı yaklaşır
             (vurgulu altın flamalar, isteğe bağlı duman perdesi; şiddet yok); kiyi — Otranto: tepede kale-kent, stilize alev + duman, turuncu→altın ışık (insan/kan yok).
  * `liman` (variant = marsilya | pera | napoli | livorno | generic; year=): rıhtım, ambar, çarklı vinç, bayrak, yeldeğirmeni, duman; gemi yanaşır/ayrılır (halat atılır, tahta iner, kürekler kalkar),
      rıhtım kalabalığı el sallar, iskele işçileri halat çeker; marsilya 1533/1600 AYNI kadraj ve kamera yolu (yalnız yıl damgası, bayrak, kıyafet, gemi tipi, ışık değişir).
  * Bağımsız işlevler: `ship(...)`, `wave_layers(...)`, `flag(...)`, `gulls(...)`, `sky_image/draw_sun/draw_clouds`, `draw_smoke_column`, `flame_cluster`, `draw_route_thread` (bkz. notlar_deniz.md §2).
Mimari: analitik dalga satırları (tepe konumları kapalı formda: köpük/parıltı/gemi sallanması aynı dalgayı sürer); ağır katmanlar (gök, uzak siluet, liman yapıları, rıhtım) tembel pişirilir →
`out/_cache/world/deniz_*.png` (sürüm = dosya özeti); gemi gövdeleri ölçek kovalarında önceden renklendirilmiş sprite (kPlus/renk filtresi yok); yelken/bayrak `drawVertices` mesh;
uzak filo gemileri sprite sayfası (LOD). Kare başına yalnız dalga yolları, kürekler, mesh'ler, figürler çizilir. Deterministik (seed). Şiddet yok: çarpışma/ateşleme/ölü/kan gösterilmez.
"""
import collections
import functools
import math
import os
import re
import time

import cv2
import numpy as np
import skia

import cilt_anim as FA
import cilt_cam as CAM
import cilt_medici as CM
import sk
from cilt_medici import TH, ckind
from sk import C, H, W, clamp, mix, smooth

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "out", "_cache", "world")
def _ver():
    """Önbellek sürümü = bu dosyanın içerik özeti (kod değişince eski kareaşlar otomatik geçersiz olur)."""
    import zlib
    try:
        with open(os.path.abspath(__file__), "rb") as fh:
            return "d%06x" % (zlib.crc32(fh.read()) & 0xFFFFFF)
    except Exception:
        return "d0"


VER = _ver()
_STALE_DONE = [False]


def _purge_stale():
    """Eski sürümlerin deniz_* önbellek dosyalarını sil (bir kez)."""
    if _STALE_DONE[0]:
        return
    _STALE_DONE[0] = True
    try:
        for fn in os.listdir(CACHE):
            if fn.startswith("deniz_") and f"_{VER}_" not in fn:
                os.remove(os.path.join(CACHE, fn))
    except Exception:
        pass
OV = 70                                 # dikey taşma (kamera y kayması)
BAND = (150, 800)                       # fresk bandı: (y0, yükseklik) — cilt_pano ile aynı
INK = "#2A1A0C"
LIN = skia.SamplingOptions(skia.FilterMode.kLinear)
NEAR = skia.SamplingOptions(skia.FilterMode.kNearest)
D2R = math.pi / 180.0
TAU = 2.0 * math.pi


# ═════════════════════════════ küçük yardımcılar ═════════════════════════════
def _RS(n):
    return np.random.RandomState(int(n) & 0x7FFFFFFF)


def sstep(a, b, x):
    t = clamp((x - a) / (b - a)) if b != a else (1.0 if x >= b else 0.0)
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def hash01(*a):
    return FA.hash01(*a)


def _P(col, a=255, aa=True, style=None, sw=1.0, cap=None, join=None, shader=None, blur=0.0):
    p = skia.Paint(AntiAlias=aa)
    if shader is not None:
        p.setShader(shader)
    else:
        p.setColor(C(col, a) if isinstance(col, str) else col)
    if style == "stroke":
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(sw)
        p.setStrokeCap(cap or skia.Paint.kRound_Cap)
        p.setStrokeJoin(join or skia.Paint.kRound_Join)
    if blur > 0:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p


def fillp(c, path, col, a=255):
    c.drawPath(path, _P(col, a))


def inkp(c, path, w=1.4, a=190, col=INK):
    c.drawPath(path, _P(col, a, style="stroke", sw=w))


def fink(c, path, col, w=1.4, a=255, ia=190):
    """Dolgu + mürekkep dış hat."""
    c.drawPath(path, _P(col, a))
    c.drawPath(path, _P(INK, ia, style="stroke", sw=w))


def poly(pts, close=True):
    if len(pts) < 2:
        return skia.Path()
    return skia.Path.Polygon([(float(x), float(y)) for x, y in pts], close)


def smoothp(pts, close=False, ten=0.5):
    return sk.smooth_path([(float(x), float(y)) for x, y in pts], close, ten)


def line(c, x0, y0, x1, y1, col=INK, w=1.2, a=255, cap=True):
    c.drawLine(x0, y0, x1, y1, _P(col, a, style="stroke", sw=w, cap=skia.Paint.kRound_Cap if cap else skia.Paint.kButt_Cap))


def oval(c, cx, cy, rx, ry, col, a=255):
    c.drawOval(skia.Rect.MakeLTRB(cx - rx, cy - ry, cx + rx, cy + ry), _P(col, a))


def ovalink(c, cx, cy, rx, ry, col, w=1.2, a=255, ia=170):
    r = skia.Rect.MakeLTRB(cx - rx, cy - ry, cx + rx, cy + ry)
    c.drawOval(r, _P(col, a))
    c.drawOval(r, _P(INK, ia, style="stroke", sw=w))


def rect(c, x0, y0, x1, y1, col, a=255):
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), _P(col, a, aa=False))


def rectink(c, x0, y0, x1, y1, col, w=1.2, a=255, ia=170):
    r = skia.Rect.MakeLTRB(x0, y0, x1, y1)
    c.drawRect(r, _P(col, a))
    c.drawRect(r, _P(INK, ia, style="stroke", sw=w))


def grad_v(c, x0, y0, x1, y1, stops):
    cols = [C(s[0], s[2] if len(s) > 2 else 255) for s in stops]
    sh = skia.GradientShader.MakeLinear([(0, y0), (0, y1)], cols, [s[1] for s in stops])
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.Paint(Shader=sh))


def ncol(col, a):
    return C(col, int(clamp(a) * 255))


# ═════════════════════════════ zaman dilimi paletleri ═════════════════════════════
PALS = {
    "day": dict(
        sky=[("#5F93CF", 0.0), ("#A9C9DE", 0.58), ("#F2E8C8", 1.0)], haze="#EAE6CE",
        sea=["#CFE0DA", "#9DC2C0", "#68A0B0", "#3E7497", "#285785", "#1D4476"], crest="#F5FAF2", ink="#1D3548", foam="#FFFFFF", glint="#FFFFFF",
        sun=("#FFF4CC", "#FFE8A6"), sun_a=0.9, shade="#243A5A", glow_k=0.55, ray_a=0.10, cloud=("#FFFFFF", "#DDE3EE", "#B9C3D8"), land=("#B8CFC4", "#9DB8AC", "#7F9E90")),
    "dusk": dict(
        sky=[("#4E5E9E", 0.0), ("#D98E86", 0.52), ("#F8D9A0", 1.0)], haze="#F3C998",
        sea=["#F2CC9E", "#E2A98C", "#B58A98", "#6C74A2", "#40508A", "#2C3C78"], crest="#FCE7C8", ink="#2A2A52", foam="#FFF3DC", glint="#FFE2A0",
        sun=("#FFE2A0", "#FFC27A"), sun_a=1.0, shade="#2A2C58", glow_k=0.85, ray_a=0.16, cloud=("#FCD7B0", "#E49A86", "#9C6E8E"), land=("#B79AA2", "#9A7E92", "#7A6684")),
    "night": dict(
        sky=[("#080F30", 0.0), ("#17286A", 0.55), ("#4F6AA8", 1.0)], haze="#4F6AA8",
        sea=["#4F6AA8", "#3A5390", "#2A4278", "#1D3262", "#14244E", "#0C1838"], crest="#A9BEE8", ink="#08102A", foam="#D9E4FA", glint="#FFF1C4",
        sun=("#FFF3CE", "#FFF0C0"), sun_a=0.8, shade="#050A20", glow_k=0.40, ray_a=0.05, cloud=("#6C7FB5", "#41558C", "#24336A"), land=("#1E2E5A", "#16244A", "#0E1938")),
    "fire": dict(
        sky=[("#5C2C40", 0.0), ("#E0743A", 0.50), ("#FFD27A", 1.0)], haze="#F5B25E",
        sea=["#F3B866", "#E39A58", "#B8705C", "#7A4A62", "#4A3052", "#2E2040"], crest="#FFD9A0", ink="#2A1428", foam="#FFE9C0", glint="#FFC060",
        sun=("#FFE9A8", "#FFB45A"), sun_a=1.0, shade="#2A1428", glow_k=1.0, ray_a=0.20, cloud=("#F6B070", "#B8584E", "#6A3A52"), land=("#B07060", "#8A5A5A", "#6A4854")),
}


def pal(tod):
    return PALS.get(tod, PALS["day"])


class Tint:
    """Gemi/yapı renk uyarlaması: day (olduğu gibi), dusk (sıcak), night (lacivert), fire (turuncu). depth 0 = ön, 1 = uzak (hava perspektifi)."""

    def __init__(self, tod="day"):
        self.tod = tod
        self.P = pal(tod)

    def __call__(self, col, depth=0.0):
        t = self.tod
        if t == "night":
            c = mix(col, "#10204A", 0.58)
            return mix(c, "#2A3C74", depth * 0.34)
        if t == "dusk":
            c = mix(col, "#E58A55", 0.20)
            return mix(c, "#B89AA0", depth * 0.36)
        if t == "fire":
            c = mix(col, "#E9843A", 0.24)
            c = mix(c, "#3A1A1C", 0.10)
            return mix(c, "#D89A6A", depth * 0.34)
        return mix(col, "#B6C8C8", depth * 0.40)


# ═════════════════════════════ pişirilmiş görüntüler (disk önbelleği) ═════════════════════════════
_IMGS = {}


def baked(key, w, h, draw, scale=1.0, disk=True):
    """(w×h dünya piksel) × scale boyutunda tuval; draw(c) dünya koordinatında (0..w, 0..h) çizer. Dönüş: skia.Image (scale ile pişmiş)."""
    k = (key, round(scale, 3))
    im = _IMGS.get(k)
    if im is not None:
        return im
    path = os.path.join(CACHE, f"deniz_{key}_{VER}_{int(round(scale * 100))}.png")
    if disk:
        _purge_stale()
        try:
            if os.path.exists(path):
                a = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                if a is not None and a.ndim == 3 and a.shape[2] == 4:
                    a = cv2.cvtColor(a, cv2.COLOR_BGRA2RGBA)
                    im = _IMGS[k] = sk.np_to_image(np.ascontiguousarray(a))
                    return im
        except Exception:
            pass
    fr = sk.Frame(int(round(w * scale)), int(round(h * scale)))
    fr.clear(skia.ColorTRANSPARENT)
    fr.c.scale(scale, scale)
    draw(fr.c)
    im = fr.surf.makeImageSnapshot()
    if disk:
        try:
            os.makedirs(CACHE, exist_ok=True)
            arr = im.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kUnpremul_AlphaType)
            cv2.imwrite(path, cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA), [cv2.IMWRITE_PNG_COMPRESSION, 1])
        except Exception:
            pass
    _IMGS[k] = im
    return im


def blit_baked(c, im, x, y, w, h, alpha=1.0):
    p = skia.Paint()
    if alpha < 1.0:
        p.setAlphaf(alpha)
    c.drawImageRect(im, skia.Rect.MakeWH(im.width(), im.height()), skia.Rect.MakeXYWH(x, y, w, h), LIN, p)


# ═════════════════════════════ parıltı sprite'ı (önceden renklendirilmiş; srcover) ═════════════════════════════
_GS = {}
_GP = skia.Paint()
SRC128 = skia.Rect.MakeWH(128, 128)


def glow_sprite(col):
    im = _GS.get(col)
    if im is None:
        n = 128
        fr = sk.Frame(n, n)
        fr.clear(skia.ColorTRANSPARENT)
        sh = skia.GradientShader.MakeRadial((n / 2, n / 2), n / 2, [C(col, 255), C(col, 96), C(col, 0)], [0.0, 0.28, 1.0])
        fr.c.drawCircle(n / 2, n / 2, n / 2, skia.Paint(Shader=sh))
        im = _GS[col] = fr.surf.makeImageSnapshot()
    return im


def glow(c, x, y, r, col, a):
    if a <= 0.004 or r <= 0.5:
        return
    _GP.setAlphaf(clamp(a))
    c.drawImageRect(glow_sprite(col), SRC128, skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), LIN, _GP)


# ═════════════════════════════ kamera / katman bağlamı ═════════════════════════════
class Ctx:
    """Çekim içi çizim bağlamı. Katman dönüşümü: ekran = (W/2, by0+bh/2) + z·(p − (Cx(f), Cy(f))), Cx(f) = W/2 + (camx − W/2)·f, Cy(f) = bh/2 + camy·f.
    f = paralaks çarpanı (1 = ana düzlem, <1 uzak, >1 yakın). Katman koordinatı: x = ekran pikseli (kamera nötr iken), y = bant yerel (0..800)."""

    def __init__(self, f, cx, camx, camy, z, band, tod, alpha=1.0, t=None):
        self.f, self.c, self.cx = f, f.c, cx
        self.t = cx.t if t is None else t
        self.camx, self.camy, self.z = camx, camy, z
        self.band = band
        self.tod = tod
        self.P = pal(tod)
        self.T = Tint(tod)
        self.night = tod == "night"
        self.alpha = alpha
        self.depth = 0
        self.deferred = {}

    def Cx(self, fct):
        return W / 2 + (self.camx - W / 2) * fct

    def Cy(self, fct, dy=0.0):
        return self.band[1] / 2 + self.camy * fct + dy

    def view(self, fct, m=60):
        cxl = self.Cx(fct)
        half = W / (2 * self.z)
        return cxl - half - m, cxl + half + m

    def push(self, fct, dy=0.0):
        c = self.c
        c.save()
        by0, bh = self.band
        c.translate(W / 2, by0 + bh / 2)
        c.scale(self.z, self.z)
        c.translate(-self.Cx(fct), -self.Cy(fct, dy))
        self.depth += 1

    def pop(self):
        self.c.restore()
        self.depth -= 1

    def to_screen(self, fct, x, y):
        by0, bh = self.band
        return W / 2 + (x - self.Cx(fct)) * self.z, by0 + bh / 2 + (y - self.Cy(fct)) * self.z

    def visible(self, fct, x0, x1, m=0.0):
        a, b = self.view(fct, m)
        return x1 >= a and x0 <= b


# ═════════════════════════════ gökyüzü ═════════════════════════════
SKY_W = 2400                       # gökyüzü görüntüsü genişliği (f≈0,04 → kamera ±~120 px)


def _draw_sky_img(c, tod, yh, seed):
    P = pal(tod)
    top, mid, hor = [s[0] for s in P["sky"]]
    grad_v(c, 0, -OV, SKY_W, yh + 40, [(top, 0.0), (mid, 0.50), (hor, 1.0)])
    rect(c, 0, yh + 38, SKY_W, yh + 300, hor)
    rs = _RS(seed + 5)
    if tod == "night":
        for i in range(260):
            c.drawCircle(rs.uniform(0, SKY_W), rs.uniform(-OV, yh - 10) ** 1.0, rs.uniform(0.7, 1.9), _P("#FFF2C4", int(rs.uniform(70, 220))))
    else:
        # ufuk bulutları: ince, yumuşak yatay bantlar
        for i in range(34):
            x = rs.uniform(-100, SKY_W)
            y = rs.uniform(yh * 0.42, yh - 6)
            ln = rs.uniform(180, 420)
            ya = (y - yh * 0.4) / (yh * 0.6)
            col = P["cloud"][0] if tod != "fire" else "#FFB070"
            c.drawOval(skia.Rect.MakeLTRB(x, y - 5, x + ln, y + 6), _P(col, int(34 + 40 * ya), blur=7))
    # ufuk sisi: ufka doğru ışıma
    sh = skia.GradientShader.MakeLinear([(0, yh - 120), (0, yh + 8)], [C(P["haze"], 0), C(P["haze"], 150 if tod != "night" else 80)], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(0, yh - 120, SKY_W, yh + 8), skia.Paint(Shader=sh))


def sky_image(tod, yh, seed=1):
    return baked(f"sky_{tod}_{int(yh)}_{seed}", SKY_W, yh + 300 + OV, lambda c: (c.translate(0, OV), _draw_sky_img(c, tod, yh, seed)), 0.5, disk=True)


@functools.lru_cache(maxsize=8)
def _rays_image(col, n=14):
    """Güneş huzmeleri: dönen yarı saydam kama çemberi (önceden pişirilmiş)."""
    S = 640
    fr = sk.Frame(S, S)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    c.translate(S / 2, S / 2)
    for i in range(n):
        a0 = i / n * TAU
        w = TAU / n * 0.34
        p = skia.Path()
        p.moveTo(0, 0)
        p.lineTo(math.cos(a0 - w / 2) * S * 0.5, math.sin(a0 - w / 2) * S * 0.5)
        p.lineTo(math.cos(a0 + w / 2) * S * 0.5, math.sin(a0 + w / 2) * S * 0.5)
        p.close()
        sh = skia.GradientShader.MakeRadial((0, 0), S * 0.5, [C(col, 120), C(col, 40), C(col, 0)], [0.0, 0.5, 1.0])
        c.drawPath(p, skia.Paint(AntiAlias=True, Shader=sh))
    return fr.surf.makeImageSnapshot()


@functools.lru_cache(maxsize=32)
def cloud_sprite(tod, variant=0):
    P = pal(tod)
    rs = _RS(41 + variant * 17)
    wd, ht = 560, 190
    fr = sk.Frame(wd, ht)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    base = ht - 40
    nb = 6 + variant % 3
    union = None
    for i in range(nb):
        cx_ = 110 + i * (wd - 220) / max(1, nb - 1) + rs.uniform(-18, 18)
        r = rs.uniform(38, 74) * (1.0 - abs(i - (nb - 1) / 2) / nb * 0.9)
        cy_ = base - r * 0.55 - rs.uniform(0, 30)
        pc = skia.Path()
        pc.addCircle(cx_, cy_, r)
        union = pc if union is None else (skia.Op(union, pc, skia.PathOp.kUnion_PathOp) or union)
    flat = skia.Path()
    flat.addRect(skia.Rect.MakeLTRB(0, 0, wd, base))
    union = skia.Op(union, flat, skia.PathOp.kIntersect_PathOp) or union
    top, mid, bot = P["cloud"]
    sh = skia.GradientShader.MakeLinear([(0, base - 120), (0, base)], [C(top), C(mid), C(bot)], [0.0, 0.55, 1.0])
    c.drawPath(union, skia.Paint(AntiAlias=True, Shader=sh))
    c.save()
    c.clipPath(union, skia.ClipOp.kIntersect, True)
    # alt gölge şeridi (ışık sol-üstten) ve yumuşak lekeler
    c.drawRect(skia.Rect.MakeLTRB(0, base - 18, wd, base), _P(bot, 90))
    for i in range(7):
        c.drawOval(skia.Rect.MakeXYWH(rs.uniform(40, wd - 160), base - rs.uniform(30, 90), rs.uniform(70, 150), rs.uniform(14, 28)), _P(bot, 36, blur=5))
    c.restore()
    c.drawPath(union, _P(P["ink"], 70 if tod != "night" else 40, style="stroke", sw=1.4))
    return FA.Spr(fr.surf.makeImageSnapshot(), 0, ht)


def draw_clouds(ctx, n=9, seed=4, wind=1.0, y_rng=(40, 250), fct=0.06, scale=(0.5, 1.1), alpha=0.95):
    """Sürüklenen bulut sprite'ları (iki derinlik, rüzgâra göre hız). ctx dönüşümü uygulanmış değil: kendi push'unu yapar."""
    if ctx.tod == "night":
        alpha *= 0.75
    rs = _RS(seed)
    ctx.push(fct)
    xa, xb = ctx.view(fct, 200)
    span = SKY_W + 700
    pt = skia.Paint()
    for i in range(n):
        spr = cloud_sprite(ctx.tod, i % 5)
        x0 = rs.uniform(0, span)
        y = rs.uniform(*y_rng)
        sc = rs.uniform(*scale)
        sp = rs.uniform(6, 15) * wind * (0.6 + sc * 0.7)
        x = (x0 + ctx.t * sp) % span - 350
        wd, ht = spr.w * sc, spr.h * sc
        if x + wd < xa or x > xb:
            continue
        pt.setAlphaf(alpha * rs.uniform(0.7, 1.0))
        c = ctx.c
        c.drawImageRect(spr.img, skia.Rect.MakeWH(spr.w, spr.h), skia.Rect.MakeXYWH(x, y - ht + ht * 0.0, wd, ht), LIN, pt)
    ctx.pop()


@functools.lru_cache(maxsize=16)
def sun_sprite(tod, r):
    """Güneş/ay + parıltı halkaları tek sprite (önceden pişirilmiş; kare başına tek blit). Dönüş: (Image, yarı_boy)."""
    P = pal(tod)
    core, glowc = P["sun"]
    k = P["glow_k"]
    half = int(r * 7.5)
    fr = sk.Frame(2 * half, 2 * half)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    c.translate(half, half)
    if tod == "night":
        glow(c, 0, 0, r * 7.0, "#7F96D6", 0.34)
        glow(c, 0, 0, r * 3.3, "#C8D6F6", 0.50)
        c.drawCircle(0, 0, r, _P("#FFF3CE"))
        c.drawCircle(-r * 0.36, -r * 0.18, r * 0.82, _P("#E6D9AA", 70))
        c.drawCircle(0, 0, r, _P(INK, 90, style="stroke", sw=1.4))
        for (dx, dy, rr) in ((0.28, 0.20, 0.16), (-0.1, 0.45, 0.1), (0.4, -0.2, 0.08)):
            c.drawCircle(dx * r, dy * r, rr * r, _P("#CFC096", 60))
    else:
        glow(c, 0, 0, r * 7.4, glowc, 0.30 * k)
        glow(c, 0, 0, r * 4.6, glowc, 0.46 * k)
        glow(c, 0, 0, r * 2.6, glowc, 0.80 * k)
        c.drawCircle(0, 0, r, _P(core))
        c.drawCircle(0, 0, r, _P("#B07A22", 110, style="stroke", sw=1.6))
        c.drawCircle(-r * 0.25, -r * 0.28, r * 0.42, _P("#FFFFFF", 90))
    return fr.surf.makeImageSnapshot(), half


@functools.lru_cache(maxsize=8)
def _rays_small(col):
    S = 320
    fr = sk.Frame(S, S)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    c.translate(S / 2, S / 2)
    n = 14
    for i in range(n):
        a0 = i / n * TAU
        w = TAU / n * 0.34
        p = skia.Path()
        p.moveTo(0, 0)
        p.lineTo(math.cos(a0 - w / 2) * S * 0.5, math.sin(a0 - w / 2) * S * 0.5)
        p.lineTo(math.cos(a0 + w / 2) * S * 0.5, math.sin(a0 + w / 2) * S * 0.5)
        p.close()
        sh = skia.GradientShader.MakeRadial((0, 0), S * 0.5, [C(col, 130), C(col, 44), C(col, 0)], [0.0, 0.5, 1.0])
        c.drawPath(p, skia.Paint(AntiAlias=True, Shader=sh))
    return fr.surf.makeImageSnapshot()


_RAY_PH = 24
_RAY_PERIOD = 360.0 / 14.0


@functools.lru_cache(maxsize=96)
def _ray_phase(col, r, k):
    """Huzme sprite'ının k. dönüş evresi (son boyutta, r*11 px kare)."""
    base = _rays_small(col)
    S = int(r * 11.0)
    fr = sk.Frame(S, S)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    c.translate(S / 2.0, S / 2.0)
    c.rotate(k * _RAY_PERIOD / _RAY_PH)
    s_ = S / base.width()
    c.scale(s_, s_)
    c.drawImage(base, -base.width() / 2.0, -base.height() / 2.0, LIN, skia.Paint())
    return fr.surf.makeImageSnapshot()


def draw_sun(ctx, sx, sy, r=46, rays=True, fct=0.04):
    """Güneş (gündüz/alacakaranlık/ateş) ya da ay (gece): disk + parıltı (tek sprite) + yavaş dönen huzmeler. (sx, sy) gökyüzü koordinatı."""
    P = ctx.P
    t = ctx.t
    ctx.push(fct)
    c = ctx.c
    pulse = 1.0 + 0.012 * math.sin(t * 1.3) + 0.008 * math.sin(t * 3.1 + 1.0)
    if ctx.tod != "night" and rays and P["ray_a"] > 0:
        # huzmeler: 14 kollu simetri → dönme periyodu 360/14°; _RAY_PH önceden döndürülmüş evre, iki komşu evre çapraz geçişle (eksen hizalı ucuz blit; döndürerek örnekleme yok)
        u = (((t * 1.8) % _RAY_PERIOD) / _RAY_PERIOD) * _RAY_PH
        k0 = int(u) % _RAY_PH
        wgt = u - int(u)
        a0 = P["ray_a"] * (0.8 + 0.2 * math.sin(t * 0.7))
        col_ = P["sun"][1]
        for kk, ww in ((k0, 1.0 - wgt), ((k0 + 1) % _RAY_PH, wgt)):
            if ww < 0.02:
                continue
            im = _ray_phase(col_, float(r), kk)
            pp = skia.Paint()
            pp.setAlphaf(a0 * ww)
            c.drawImage(im, sx - im.width() / 2, sy - im.height() / 2, LIN, pp)
    im, half = sun_sprite(ctx.tod, float(r))
    sc = pulse
    c.drawImageRect(im, skia.Rect.MakeWH(im.width(), im.height()), skia.Rect.MakeXYWH(sx - half * sc, sy - half * sc, 2 * half * sc, 2 * half * sc), LIN, skia.Paint())
    ctx.pop()


def draw_stars(ctx, n=40, seed=8, fct=0.04):
    """Gece: yanıp sönen yıldızlar (statik yıldızlar gökyüzü görüntüsünde)."""
    ctx.push(fct)
    c = ctx.c
    rs = _RS(seed)
    xa, xb = ctx.view(fct, 20)
    for i in range(n):
        x = rs.uniform(0, SKY_W)
        y = rs.uniform(-OV * 0.5, 250)
        ph = rs.uniform(0, TAU)
        a = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(ctx.t * rs.uniform(1.2, 3.4) + ph)) ** 2
        if x < xa or x > xb:
            continue
        r = rs.uniform(1.4, 3.0)
        glow(c, x, y, r * 4.0, "#FFF4D0", 0.22 * a)
        c.drawCircle(x, y, r * 0.55, _P("#FFFBE8", int(255 * a)))
    ctx.pop()


# ═════════════════════════════ kuşlar (martılar) ═════════════════════════════
def gull(c, x, y, s, t, ph, glide=0.0, col=INK, a=230, flip=1):
    """Tek martı: kanat çırpışı (iki yaylı kanat + gövde). glide 0..1: süzülme (kanat düz, yavaş)."""
    beat = math.sin(t * (7.5 - 4.5 * glide) + ph)
    up = (0.45 - 0.55 * glide) * beat + glide * 0.12
    for sgn in (-1, 1):
        p = skia.Path()
        p.moveTo(x, y)
        tipx = x + sgn * 20 * s * flip
        tipy = y - 14 * s * up - 2 * s
        midx = x + sgn * 10 * s * flip
        midy = y - 8 * s * up - 4.2 * s * (1 - 0.6 * glide)
        p.quadTo(midx, midy, tipx, tipy)
        p.quadTo(midx + sgn * 1.2 * s, midy + 3.6 * s, x, y + 1.6 * s)
        c.drawPath(p, _P(col, a))
    c.drawOval(skia.Rect.MakeLTRB(x - 5.2 * s, y - 1.6 * s, x + 6.0 * s, y + 2.6 * s), _P(col, a))


def gulls(ctx, n=7, seed=3, fct=0.5, y_rng=(70, 300), size=(0.8, 1.7), speed=(20, 52), wind=1.0, tint=INK):
    """Martı sürüsü: farklı derinlik/boy/hız; kimi süzülür, kimi çırpar. Katman push'unu kendi yapar."""
    rs = _RS(seed)
    ctx.push(fct)
    xa, xb = ctx.view(fct, 150)
    span = 3400
    col = tint if ctx.tod != "night" else "#C4D2F0"
    for i in range(n):
        sp = rs.uniform(*speed) * (1 if rs.rand() < 0.75 else -1) * wind
        x = (rs.uniform(0, span) + ctx.t * sp) % span - 700
        y0 = rs.uniform(*y_rng)
        y = y0 + math.sin(ctx.t * rs.uniform(0.4, 0.9) + i * 1.9) * rs.uniform(10, 26)
        if x < xa or x > xb:
            continue
        gull(ctx.c, x, y, rs.uniform(*size), ctx.t, rs.uniform(0, TAU), glide=rs.uniform(0, 1) ** 2 * 0.9, col=col, a=215, flip=1 if sp > 0 else -1)
    ctx.pop()


# ═════════════════════════════ DENİZ: analitik dalga sıraları ═════════════════════════════
YREF = 640.0                          # ana düzlem su hattı (persp = 1)


def persp(y, yh):
    """Perspektif çarpanı: su hattı y'nin ufuktan uzaklığına orantılı (boy ve paralaks). y = YREF → 1."""
    return clamp((y - yh) / (YREF - yh), 0.10, 2.4)


def _ramp(cols, u):
    """Renk rampası (u 0..1)."""
    n = len(cols) - 1
    x = clamp(u) * n
    i = min(int(x), n - 1)
    return mix(cols[i], cols[i + 1], x - i)


class Row:
    __slots__ = ("k", "y", "d", "f", "A", "lam", "k1", "v", "ph", "col", "crest", "n", "ybot", "sc", "foam_p", "skip")


class Sea:
    """Paralaks dalga sıraları (ufuk → yakın). Her sıra analitik: y(x,t) = y0 + A·(0,62 sin θ + 0,26 sin(2,03 θ′) + 0,12 sin(3,1 θ″)); tepe konumları kapalı formda bilindiği için
    köpük başlıkları, parıltılar ve gemi sallanması aynı dalgayı izler. swell: genlik çarpanı; wdir: dalga yönü (+1 sağa); foam: köpük yoğunluğu 0..1."""

    def __init__(self, tod, yh=330.0, ybot=860.0, n=24, seed=1, swell=1.0, wdir=1, foam=0.55, speed=1.0, tint=None):
        self.tod, self.yh, self.ybot, self.n = tod, float(yh), float(ybot), n
        self.P = pal(tod)
        self.swell, self.wdir, self.foam, self.speed = swell, wdir, foam, speed
        P = self.P
        cols = P["sea"]
        rs = _RS(seed * 31 + 7)
        self.rows = []
        for k in range(n):
            u = (k + 1) / n
            y = yh + (ybot - yh) * u ** 1.8
            r = Row()
            r.k, r.y = k, y
            r.d = d = (y - yh) / (ybot - yh)
            r.f = clamp((y - yh) / (YREF - yh), 0.10, 1.75)
            r.sc = clamp((y - yh) / (YREF - yh), 0.10, 1.8)                  # görsel ölçek (köpük, çizgi kalınlığı)
            r.A = (1.1 + 12.5 * d ** 1.05) * swell
            r.lam = 30 + 400 * d ** 1.12
            r.k1 = TAU / r.lam
            r.v = (20 + 92 * d) * speed * wdir
            r.ph = (rs.uniform(0, TAU), rs.uniform(0, TAU), rs.uniform(0, TAU))
            base = _ramp(cols, d ** 0.80)
            alt = 0.045 * (1 if k % 2 else -1)
            r.col = mix(base, "#FFFFFF", alt) if alt > 0 else mix(base, "#102030", -alt)
            r.crest = mix(base, P["crest"], 0.55 + 0.2 * (1 - d))
            r.foam_p = foam * (0.0 if d < 0.10 else (0.35 + 0.65 * d))
            r.skip = (d < 0.085 and k % 2 == 1)
            self.rows.append(r)
        self.ys = [r.y for r in self.rows]

    # ── dalga fonksiyonu ───────────────────────────────────────────────
    def wave(self, r, x, t):
        """Sıra r'nin x'teki (dizi/skaler) düşey sapması (px; negatif = yukarı)."""
        k1 = r.k1
        th1 = k1 * x - k1 * r.v * t + r.ph[0]
        th2 = 2.03 * k1 * x - 2.03 * k1 * r.v * 1.09 * t + r.ph[1]
        th3 = 3.1 * k1 * x - 3.1 * k1 * r.v * 0.93 * t + r.ph[2]
        return -r.A * (0.62 * np.sin(th1) + 0.26 * np.sin(th2) + 0.12 * np.sin(th3))

    def slope(self, r, x, t):
        e = 2.0
        return (self.wave(r, x + e, t) - self.wave(r, x - e, t)) / (2 * e)

    def row_before(self, y):
        """Su hattı y olan nesne için: önünde çizilecek ilk sıranın indeksi (nesne bu sıradan ÖNCE çizilir)."""
        for k, yy in enumerate(self.ys):
            if yy >= y + 2.0:
                return k
        return self.n

    def row_of(self, y):
        k = self.row_before(y) - 1
        return self.rows[max(0, k)]

    # ── çizim ──────────────────────────────────────────────────────────
    def draw_base(self, ctx):
        """Ufuk altındaki dolgu (ilk sıranın arkası)."""
        ctx.push(0.08)
        xa, xb = ctx.view(0.08, 80)
        rect(ctx.c, xa - 200, self.yh - 1.5, xb + 200, self.yh + 60, self.rows[0].col)
        ctx.pop()

    def draw_row(self, ctx, k, t, sun_sx=None, glitter=0.0):
        r = self.rows[k]
        if r.skip:
            return
        c = ctx.c
        ctx.push(r.f)
        xa, xb = ctx.view(r.f, 50)
        step = clamp(r.lam / 8.0, 10.0, 24.0)
        xs = np.arange(xa - step * 2, xb + step * 2, step)
        ys = r.y + self.wave(r, xs, t)
        kn = k + 1
        while kn < self.n and self.rows[kn].skip:
            kn += 1
        nxt = self.rows[kn].y + self.rows[kn].A + 8 if kn < self.n else self.ybot + 90
        pts = np.stack([xs, ys], 1)
        pl = skia.Path.Polygon([(float(a), float(b)) for a, b in pts], False)
        body = skia.Path(pl)
        body.lineTo(float(xs[-1]), nxt)
        body.lineTo(float(xs[0]), nxt)
        body.close()
        c.drawPath(body, _P(r.col))
        d = r.d
        # çukur gölgesi (bir sonraki sıranın hemen önü) + ışıklı bant (tepenin hemen altı) + mürekkep çizgisi
        gap = max(3.0, (self.rows[kn].y - r.y) if kn < self.n else 30.0)
        if d > 0.16:
            c.save()
            c.translate(0, gap * 0.62)
            c.drawPath(pl, _P(self.P["shade"], int(255 * (0.10 + 0.08 * d)), style="stroke", sw=gap * 0.55, cap=skia.Paint.kButt_Cap))
            c.restore()
        wl = 1.0 + 5.2 * d
        c.save()
        c.translate(0, wl * 0.9)
        c.drawPath(pl, _P(r.crest, int(255 * (0.30 + 0.18 * d)), style="stroke", sw=wl * 1.8, cap=skia.Paint.kButt_Cap))
        c.restore()
        if d > 0.05:
            c.drawPath(pl, _P(self.P["ink"], int(255 * (0.20 + 0.22 * d)), style="stroke", sw=0.8 + 1.5 * d))
        # köpük başlıkları + parıltılar (tepe konumları kapalı formda)
        if d > 0.07:
            self._crests(ctx, r, t, xa, xb, sun_sx, glitter)
        ctx.pop()

    def _crests(self, ctx, r, t, xa, xb, sun_sx, glitter):
        c = ctx.c
        k1 = r.k1
        # θ1 = k1 x − k1 v t + p1 = π/2 + 2π m  → x_m
        m0 = int(math.floor((k1 * xa - k1 * r.v * t + r.ph[0] - math.pi / 2) / TAU)) - 1
        m1 = int(math.ceil((k1 * xb - k1 * r.v * t + r.ph[0] - math.pi / 2) / TAU)) + 1
        sc = r.sc
        P = self.P
        foam_col, ink = P["foam"], P["ink"]
        night = ctx.tod == "night"
        for m in range(m0, m1 + 1):
            xm = (math.pi / 2 + TAU * m + k1 * r.v * t - r.ph[0]) / k1
            h = hash01(m, r.k, 7)
            ym = r.y + float(self.wave(r, xm, t))
            # köpük başlığı
            if h < r.foam_p:
                life = 0.55 + 0.45 * math.sin(t * (0.35 + 0.5 * h) + h * 40.0)
                if life > 0.18:
                    wcap = (10 + 26 * h) * sc * (0.7 + 0.5 * life)
                    hcap = (3.2 + 4.2 * h) * sc * (0.6 + 0.6 * life)
                    p = skia.Path()
                    p.moveTo(xm - wcap, ym + 1.4 * sc)
                    p.quadTo(xm - wcap * 0.35, ym - hcap * 1.5, xm + wcap * 0.15, ym - hcap)
                    p.quadTo(xm + wcap * 0.85, ym - hcap * 0.4, xm + wcap, ym + 1.6 * sc)
                    p.quadTo(xm + wcap * 0.2, ym + 0.8 * sc, xm - wcap, ym + 1.4 * sc)
                    a = int(255 * clamp(0.80 * life * (0.75 if night else 1.0)))
                    c.drawPath(p, _P(foam_col, a))
                    c.drawPath(p, _P(ink, int(a * 0.30), style="stroke", sw=0.9 * max(0.6, sc)))
                    if h < r.foam_p * 0.45 and sc > 0.45:                      # köpük damlacıkları (sıçrama)
                        for q in range(3):
                            ph = (t * 0.9 + h * 9 + q * 0.33) % 1.0
                            c.drawCircle(xm + wcap * (0.2 + 0.5 * q / 3) + ph * 6, ym - hcap * (1.0 + 2.2 * math.sin(ph * math.pi)) - 1, 1.2 * sc, _P(foam_col, int(210 * (1 - ph))))
            # güneş/ay parıltısı: tepelerde kısa çizgiler
            if sun_sx is not None and glitter > 0:
                span = (150 + 330 * r.d) * glitter
                dx = xm - sun_sx
                if abs(dx) < span:
                    k = 1.0 - abs(dx) / span
                    tw = 0.5 + 0.5 * math.sin(t * (3.2 + 4 * h) + h * 50.0)
                    a = clamp(0.95 * k * tw * (0.5 + 0.5 * h) * glitter * (1.35 if night else 1.0))
                    if a > 0.05:
                        ln = (10 + 34 * h) * sc * (0.5 + k)
                        c.drawLine(xm - ln / 2, ym - 0.6 * sc, xm + ln / 2, ym - 0.6 * sc, _P(P["glint"], int(255 * a), style="stroke", sw=(1.6 + 2.6 * r.d) * max(0.7, sc * 0.6)))

    def skirt(self, ctx, r, x0, x1, y_ship, t, col=None, foam_a=0.85, depth=34.0):
        """Gemi/rıhtım kaidesinde su eteği: dalgalı kenarlı su dolgusu + köpük çizgisi (gövdenin düz alt kenarını örter). Katman dönüşümü uygulanmış (r.f) olmalı."""
        c = ctx.c
        n = max(8, int((x1 - x0) / 8))
        xs = np.linspace(x0, x1, n)
        wob = 0.8 * self.wave(r, xs, t) + 1.4 * np.sin(xs * 0.07 - t * 2.2) * r.sc
        ys = y_ship - 3.0 * r.sc + wob
        pl = skia.Path.Polygon([(float(a), float(b)) for a, b in zip(xs, ys)], False)
        body = skia.Path(pl)
        body.lineTo(float(xs[-1]), y_ship + depth)
        body.lineTo(float(xs[0]), y_ship + depth)
        body.close()
        c.drawPath(body, _P(col or r.col))
        c.drawPath(pl, _P(self.P["crest"], int(255 * 0.55), style="stroke", sw=3.0 * r.sc + 1.0))
        c.drawPath(pl, _P(self.P["foam"], int(255 * foam_a), style="stroke", sw=1.5 * r.sc + 0.8))
        c.drawPath(pl, _P(self.P["ink"], 50, style="stroke", sw=0.8))


def draw_sea(ctx, sea, t, ship_cb=None, sun_sx=None, glitter=0.0):
    """Tüm sıraları arkadan öne çiz; ship_cb(k) → k. sıradan ÖNCE çizilecek nesneleri çizer (k = n: tüm sıraların önü). sun_sx: güneşin EKRAN x'i (parıltı yolu için)."""
    sea.draw_base(ctx)
    for k in range(sea.n):
        if ship_cb is not None:
            ship_cb(k)
        for fn in ctx.deferred.pop(k, ()):
            fn()
        sx = None
        if sun_sx is not None:
            r = sea.rows[k]
            sx = ctx.Cx(r.f) + (sun_sx - W / 2) / ctx.z
        sea.draw_row(ctx, k, t, sx, glitter)
    if ship_cb is not None:
        ship_cb(sea.n)
    for kk in sorted(ctx.deferred):
        for fn in ctx.deferred.pop(kk, ()):
            fn()


def wave_layers(f, t, tod="day", yh=330.0, band=BAND, camx=960.0, camy=0.0, z=1.0, swell=1.0, seed=1, foam=0.55, wdir=1, sun_sx=None, glitter=0.0, sky=True):
    """BAĞIMSIZ kullanım: f (sk.Frame) üzerine bant içinde gökyüzü + dalga sıralarını çizer (haritaya/başka çekime serpiştirme). Dönüş: (Sea, Ctx)."""
    class _CX:
        pass
    cx = _CX()
    cx.t = t
    ctx = Ctx(f, cx, camx, camy, z, band, tod)
    c = f.c
    by0, bh = band
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, by0, W, by0 + bh))
    if sky:
        ctx.push(0.04)
        im = sky_image(tod, int(yh), seed)
        blit_baked(c, im, 0, -OV, SKY_W, im.height() * 2)
        ctx.pop()
    sea = Sea(tod, yh, seed=seed, swell=swell, wdir=wdir, foam=foam)
    draw_sea(ctx, sea, t, None, sun_sx, glitter)
    c.restore()
    return sea, ctx


# ═════════════════════════════ MESH: yelken / bayrak kumaşı ═════════════════════════════
class Mesh:
    """Önceden boyanmış kumaş sprite'ını (nu×nv ızgara) düğüm düğüm oynatan mesh. draw(c, X, Y, shade): X,Y: (nv+1, nu+1) ekran düğümleri; shade: aynı şekil 0..1+ (köşe rengi çarpanı: kıvrım gölgesi)."""
    __slots__ = ("img", "nu", "nv", "tex", "idx", "paint", "w", "h")

    def __init__(self, img, nu, nv, rect=None):
        self.img, self.nu, self.nv = img, nu, nv
        iw, ih = img.width(), img.height()
        x0, y0, x1, y1 = rect if rect else (0, 0, iw, ih)
        self.w, self.h = iw, ih
        tex = []
        for j in range(nv + 1):
            for i in range(nu + 1):
                tex.append(skia.Point(x0 + (x1 - x0) * i / nu, y0 + (y1 - y0) * j / nv))
        self.tex = tex
        idx = []
        for j in range(nv):
            for i in range(nu):
                a = j * (nu + 1) + i
                b, c2, d = a + 1, a + nu + 1, a + nu + 2
                idx += [a, b, c2, b, d, c2]
        self.idx = idx
        sh = img.makeShader(skia.TileMode.kClamp, skia.TileMode.kClamp, LIN)
        self.paint = skia.Paint(AntiAlias=True, Shader=sh)

    def draw(self, c, X, Y, shade=None, alpha=1.0):
        P_ = skia.Point
        xl, yl = X.ravel().tolist(), Y.ravel().tolist()
        pos = [P_(a, b) for a, b in zip(xl, yl)]
        if shade is None:
            cols = None
        else:
            g = np.clip(shade.ravel() * 255.0, 0, 255).astype(int).tolist()
            al = int(255 * alpha)
            cols = [skia.Color(v, v, v, al) for v in g]
        vt = skia.Vertices.MakeCopy(skia.Vertices.kTriangles_VertexMode, pos, self.tex, cols, self.idx)
        self.paint.setAlphaf(alpha if cols is None else 1.0)
        c.drawVertices(vt, self.paint, skia.BlendMode.kModulate)


# ── devre/arma çizimleri (bayrak ve yelken sprite'larında) ─────────────────────────────
def _crescent_path(cx, cy, r, tilt=0.0):
    a = skia.Path()
    a.addCircle(cx, cy, r)
    b = skia.Path()
    b.addCircle(cx + r * 0.38 * math.cos(tilt), cy + r * 0.38 * math.sin(tilt), r * 0.82)
    return skia.Op(a, b, skia.PathOp.kDifference_PathOp) or a


def _star_path(cx, cy, r, n=5, rot=-math.pi / 2):
    pts = []
    for i in range(2 * n):
        rr = r if i % 2 == 0 else r * 0.42
        a = rot + i * math.pi / n
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return poly(pts)


def _lily_path(cx, cy, s):
    """Fleur-de-lis (zambak) — basit üç yapraklı biçim."""
    p = skia.Path()
    p.moveTo(cx, cy - s * 0.95)
    p.cubicTo(cx + s * 0.34, cy - s * 0.55, cx + s * 0.30, cy - s * 0.10, cx + s * 0.06, cy + s * 0.12)
    p.lineTo(cx + s * 0.06, cy + s * 0.34)
    p.lineTo(cx - s * 0.06, cy + s * 0.34)
    p.lineTo(cx - s * 0.06, cy + s * 0.12)
    p.cubicTo(cx - s * 0.30, cy - s * 0.10, cx - s * 0.34, cy - s * 0.55, cx, cy - s * 0.95)
    p.close()
    for sgn in (-1, 1):
        q = skia.Path()
        q.moveTo(cx + sgn * s * 0.05, cy + s * 0.12)
        q.cubicTo(cx + sgn * s * 0.40, cy - s * 0.22, cx + sgn * s * 0.82, cy - s * 0.10, cx + sgn * s * 0.74, cy + s * 0.26)
        q.cubicTo(cx + sgn * s * 0.66, cy + s * 0.50, cx + sgn * s * 0.30, cy + s * 0.42, cx + sgn * s * 0.12, cy + s * 0.34)
        q.close()
        p.addPath(q)
    b = skia.Path()
    b.addRect(skia.Rect.MakeLTRB(cx - s * 0.34, cy + s * 0.30, cx + s * 0.34, cy + s * 0.43))
    p.addPath(b)
    return p


def draw_device(c, dev, cx, cy, s, col, col2=None, a=255):
    """Bayrak/yelken devresi (merkez cx,cy; yarım boy s). dev: cross | crescent | crescent_star | medici | lily | palle | lion(yok) | None."""
    if dev == "cross":
        w = s * 0.34
        pth = poly([(cx - w / 2, cy - s), (cx + w / 2, cy - s), (cx + w / 2, cy - w / 2), (cx + s, cy - w / 2), (cx + s, cy + w / 2), (cx + w / 2, cy + w / 2),
                    (cx + w / 2, cy + s), (cx - w / 2, cy + s), (cx - w / 2, cy + w / 2), (cx - s, cy + w / 2), (cx - s, cy - w / 2), (cx - w / 2, cy - w / 2)])
        fink(c, pth, col, 1.0, a, 150)
    elif dev in ("crescent", "crescent_star"):
        pth = _crescent_path(cx, cy, s * 0.92, 0.0)
        fink(c, pth, col, 1.0, a, 140)
        if dev == "crescent_star":
            fink(c, _star_path(cx + s * 0.42, cy, s * 0.30), col, 0.8, a, 120)
    elif dev == "lily":
        fink(c, _lily_path(cx, cy, s), col, 1.0, a, 140)
    elif dev in ("medici", "palle"):
        r = s * 0.30
        for (dx, dy) in ((0, -0.62), (-0.60, -0.10), (0.60, -0.10), (-0.36, 0.52), (0.36, 0.52), (0.0, 0.14)):
            if dev == "medici" and dx == 0 and dy == 0.14:
                continue
            fink(c, _circ(cx + dx * s, cy + dy * s, r), col, 0.9, a, 130)
    elif dev == "star":
        fink(c, _star_path(cx, cy, s), col, 0.9, a, 130)


def _circ(cx, cy, r):
    p = skia.Path()
    p.addCircle(cx, cy, r)
    return p


@functools.lru_cache(maxsize=96)
def flag_sprite(shape, dev, c1, c2, c3, w, h):
    """Bayrak/flama kumaşı (sol = sancak direği kenarı, sağ = serbest uç). shape: rect | swallow | pennant | gold. Dönüş: skia.Image."""
    fr = sk.Frame(int(w) + 6, int(h) + 6)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    c.translate(3, 3)
    if shape == "pennant":                                  # uzun, kırlangıç kuyruklu flama (üst/alt kenar uca doğru daralır)
        pth = poly([(0, 0), (w * 0.62, h * 0.18), (w, 0.0), (w * 0.84, h * 0.5), (w, h), (w * 0.62, h * 0.82), (0, h)])
    elif shape == "swallow":
        pth = poly([(0, 0), (w, 0), (w * 0.82, h * 0.5), (w, h), (0, h)])
    else:
        pth = poly([(0, 0), (w, 0), (w, h), (0, h)])
    c.save()
    c.clipPath(pth, skia.ClipOp.kIntersect, True)
    sh = skia.GradientShader.MakeLinear([(0, 0), (0, h)], [C(mix(c1, "#FFFFFF", 0.16)), C(c1), C(mix(c1, "#1A1008", 0.14))], [0.0, 0.5, 1.0])
    c.drawRect(skia.Rect.MakeWH(w, h), skia.Paint(Shader=sh))
    if dev == "stripes":
        for k in range(3):
            c.drawRect(skia.Rect.MakeLTRB(w * (0.18 + 0.26 * k), 0, w * (0.18 + 0.26 * k + 0.12), h), _P(c2))
    elif dev == "bands":                                    # yatay bantlı
        c.drawRect(skia.Rect.MakeLTRB(0, h * 0.34, w, h * 0.66), _P(c2))
    elif dev in ("lily", "lily_field"):
        n = max(2, int(w / (h * 1.05)))
        for i in range(n):
            for j in range(2):
                draw_device(c, "lily", w * (i + 0.5) / n + (h * 0.45 if j else 0) * 0, h * (0.28 + 0.44 * j), h * 0.20, c2, None, 255)
    elif dev in ("cross", "crescent", "crescent_star", "medici", "palle", "star"):
        draw_device(c, dev, w * 0.5 if shape != "pennant" else w * 0.30, h * 0.5, h * 0.36 if shape != "pennant" else h * 0.40, c2, c3)
    if shape == "gold":
        pass
    c.restore()
    c.drawPath(pth, _P(INK, 200, style="stroke", sw=1.5))
    return fr.surf.makeImageSnapshot()


@functools.lru_cache(maxsize=96)
def flag_mesh(shape, dev, c1, c2, c3, w, h, nu=16, nv=2):
    return Mesh(flag_sprite(shape, dev, c1, c2, c3, int(w), int(h)), nu, nv, rect=(3, 3, 3 + int(w), 3 + int(h)))


def flag(c, x, y, w, h, t, shape="swallow", dev="plain", c1="#B33620", c2="#F2E6C2", c3=None, wind=1.0, ph=0.0, droop=0.0, amp=1.0, flipx=1):
    """Dalgalanan bayrak/flama. (x,y) = direğe bağlı sol-üst köşe; w×h px; wind: rüzgâr şiddeti (genlik/hız); flipx=-1: sol yöne uzanır. droop: 0..1 sarkma."""
    c3 = c3 or c2
    m = flag_mesh(shape, dev, c1, c2, c3, int(w), int(h))
    nu, nv = m.nu, m.nv
    u = np.linspace(0, 1, nu + 1)[None, :]
    v = np.linspace(0, 1, nv + 1)[:, None]
    sp = 3.4 + 2.2 * wind
    A = h * (0.13 + 0.15 * wind) * amp
    wav = A * (u ** 1.1) * np.sin(t * sp - u * 4.6 + ph) + 0.25 * A * (u ** 1.3) * np.sin(t * sp * 1.6 - u * 7.5 + ph * 1.9)
    X = x + flipx * (w * u * (1.0 - 0.06 * np.abs(wav) / max(A, 1.0))) + 0 * v
    Y = y + h * v + wav + h * droop * (u ** 1.5) * 1.2
    sh = 0.92 + 0.14 * np.cos(t * sp - u * 4.6 + ph) * np.minimum(1.0, u * 2) + 0 * v
    m.draw(c, X, Y, sh)


# ── yelken sprite + mesh ─────────────────────────────────────────────────
@functools.lru_cache(maxsize=48)
def sail_sprite(kind, w, h, col, trim, dev, devcol, seed=0):
    """Kumaş: sıva-beyaz tonlu bez, dikey dikişler, camadan şeritleri (reef), kenar bolt-ropu, isteğe bağlı devre. kind: square | lateen."""
    fr = sk.Frame(int(w) + 8, int(h) + 8)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    c.translate(4, 4)
    rs = _RS(seed + 3)
    sh = skia.GradientShader.MakeLinear([(0, 0), (w, h * 0.4)], [C(mix(col, "#FFFFFF", 0.35)), C(col), C(mix(col, "#7A5A3A", 0.32))], [0.0, 0.55, 1.0])
    c.drawRect(skia.Rect.MakeWH(w, h), skia.Paint(Shader=sh))
    # dikişler (dikey) ve hafif kıvrım gölgeleri
    nseam = max(4, int(w / 26))
    for i in range(1, nseam):
        x = w * i / nseam + rs.uniform(-1.5, 1.5)
        c.drawLine(x, 0, x + rs.uniform(-2, 2), h, _P(INK, 46, style="stroke", sw=0.9))
        c.drawRect(skia.Rect.MakeLTRB(x + 1, 0, x + 4 + rs.uniform(0, 5), h), _P("#FFFFFF", 18, aa=False))
    # yatay bağlama şeritleri
    for yy in (0.34, 0.66):
        c.drawLine(0, h * yy, w, h * yy, _P(INK, 60, style="stroke", sw=1.0))
        for i in range(int(w / 15)):
            c.drawLine(8 + i * 15, h * yy, 8 + i * 15 + 1, h * yy + 11, _P(INK, 70, style="stroke", sw=1.0))
    # leke/yaşlanma
    for i in range(10):
        c.drawOval(skia.Rect.MakeXYWH(rs.uniform(0, w - 40), rs.uniform(h * 0.05, h * 0.9), rs.uniform(20, 70), rs.uniform(8, 26)), _P("#8A6A3A", 16, blur=5))
    if dev:
        draw_device(c, dev, w / 2, h * 0.5, min(w, h) * 0.30, devcol, None)
    # bolt-ropu kenarı
    bw = max(2.5, w * 0.014)
    c.drawRect(skia.Rect.MakeLTRB(0, 0, w, bw * 1.6), _P(trim, 255))
    c.drawRect(skia.Rect.MakeLTRB(0, h - bw, w, h), _P(trim, 200))
    c.drawRect(skia.Rect.MakeLTRB(0, 0, bw, h), _P(trim, 200))
    c.drawRect(skia.Rect.MakeLTRB(w - bw, 0, w, h), _P(trim, 200))
    c.drawRect(skia.Rect.MakeWH(w, h), _P(INK, 200, style="stroke", sw=1.5))
    return fr.surf.makeImageSnapshot()


@functools.lru_cache(maxsize=64)
def sail_mesh(kind, w, h, col, trim, dev, devcol, seed=0, nu=9, nv=7):
    return Mesh(sail_sprite(kind, int(w), int(h), col, trim, dev, devcol, seed), nu, nv, rect=(4, 4, 4 + int(w), 4 + int(h)))


def square_sail(c, cx, ytop, ybot, wtop, wbot, t, wind=1.0, ph=0.0, col="#EDE4CC", trim="#B33620", dev=None, devcol="#B33620", seed=0, set_=1.0, sway=0.0, sheet=0.0):
    """Kare yelken (düz bakış, ortalanmış cx): şişer (yanlar dışarı yay), alt kenar içbükey kalkar, enine kıvrım dalgası akar. set_: 0 (toplanmış) … 1 (tam açık). wind: şişme/dalga şiddeti."""
    m = sail_mesh("square", int(max(wtop, wbot)), int(max(8, ybot - ytop)), col, trim, dev, devcol, seed)
    nu, nv = m.nu, m.nv
    u = np.linspace(-0.5, 0.5, nu + 1)[None, :]
    v = np.linspace(0, 1, nv + 1)[:, None]
    br = 0.5 + 0.5 * math.sin(t * (1.1 + 0.4 * wind) + ph)                        # soluk (şişme nabzı)
    br2 = 0.5 + 0.5 * math.sin(t * 2.3 + ph * 1.7)
    bulge = (0.045 + 0.05 * wind * (0.55 + 0.45 * br)) * set_
    wdt = (wtop + (wbot - wtop) * v) * (1.0 + bulge * np.sin(math.pi * np.clip(v, 0, 1)) ** 0.8 * (1.0 + 0.0 * u))
    rip = (2.2 + 2.6 * wind) * np.sin(TAU * (v * 1.15 - t * (0.45 + 0.2 * wind)) + ph + u * 4.0) * np.sin(math.pi * np.clip(v, 0, 1)) * (1 - 4 * u ** 2 * 0.6)
    X = cx + u * wdt + rip + sway * v + sheet * 0
    foot_up = h_hollow = (ybot - ytop) * 0.055 * (1 + 0.4 * br2)
    Y = ytop + (ybot - ytop) * v * set_ - foot_up * (1 - 4 * u ** 2) * v ** 3 - (ybot - ytop) * (1 - set_) * 0 + 1.2 * np.sin(t * 2.9 + u * 6 + ph) * v
    shade = 0.93 + 0.12 * np.sin(TAU * (u * 1.8 + v * 0.35 - t * 0.28) + ph) + 0.08 * (v - 0.5) * (0.5 + br) + 0 * u
    m.draw(c, X, Y, np.clip(shade, 0.62, 1.12))


def lateen_sail(c, tack, peak, clew, t, wind=1.0, ph=0.0, col="#EDE4CC", trim="#B33620", dev=None, devcol="#B33620", seed=0):
    """Üçgen (latin) yelken: tack (ön-alt), peak (arka-üst, antenna ucu), clew (arka-alt). Şişme: arka kenar (leech) ve alt kenar dışa yaylanır; kumaş dalgası."""
    L = math.hypot(peak[0] - tack[0], peak[1] - tack[1])
    m = sail_mesh("lateen", int(L), int(L * 0.55), col, trim, dev, devcol, seed, nu=10, nv=6)
    nu, nv = m.nu, m.nv
    a = np.linspace(0, 1, nu + 1)[None, :]
    b = np.linspace(0, 1, nv + 1)[:, None]
    tx, ty = tack
    px, py = peak
    cx_, cy_ = clew
    yx, yy = tx + (px - tx) * a, ty + (py - ty) * a
    fx, fy = tx + (cx_ - tx) * a, ty + (cy_ - ty) * a
    X = yx + (fx - yx) * b
    Y = yy + (fy - yy) * b
    br = 0.5 + 0.5 * math.sin(t * (1.0 + 0.4 * wind) + ph)
    bel = (10 + 16 * wind * (0.55 + 0.45 * br))
    prof = np.sin(math.pi * np.clip(a, 0, 1)) * np.sin(math.pi * np.clip(b, 0, 1))
    nxv, nyv = (cy_ - py), -(cx_ - px)                                              # leech normali (yaklaşık)
    nl = math.hypot(nxv, nyv) or 1.0
    X = X + prof * bel * (-1.0) * (nxv / nl) * 0.0 + prof * bel * 0.9
    Y = Y + prof * bel * 0.15 + 2.0 * np.sin(t * 3.1 + a * 8 + b * 4 + ph) * b * a
    sh = 0.94 + 0.12 * np.sin(TAU * (a * 1.3 + b * 0.5 - t * 0.3) + ph)
    m.draw(c, X, Y, np.clip(sh, 0.62, 1.12))


# ═════════════════════════════ GEMİ: ortak (livery, yerel sprite, yardımcılar) ═════════════════════════════
LIVERY = {
    # kadırga/nao boyası ve bayrak: hull, wale (üst şerit), trim (yaldız), awn (tente 2 renk), flag=(şekil, devre, c1, c2, c3), pen=(flama c1, c2/devre), sail (yelken bezi, bolt-ropu, devre)
    "hristiyan": dict(hull="#6A4226", wale="#B33620", trim="#D2A33E", awn=("#B33620", "#F2E6C2"), flag=("swallow", "cross", "#F4EEDC", "#B33620", "#B33620"), pen=("#F4EEDC", "#B33620", "cross"), sail=("#EDE4CC", "#B33620", "cross", "#B33620")),
    "osmanli": dict(hull="#6A4226", wale="#2E6A4F", trim="#E0B84E", awn=("#A8321E", "#E0B84E"), flag=("swallow", "crescent", "#A8321E", "#E0B84E", "#E0B84E"), pen=("#A8321E", "#E0B84E", "crescent"), sail=("#EDE4CC", "#2E6A4F", None, "#2E6A4F")),
    "toskana": dict(hull="#6A4226", wale="#B33620", trim="#E0B84E", awn=("#B33620", "#F2E6C2"), flag=("swallow", "medici", "#E0B84E", "#B33620", "#B33620"), pen=("#E0B84E", "#B33620", "medici"), sail=("#EDE4CC", "#B33620", "medici", "#B33620")),
    "papalik": dict(hull="#6A4226", wale="#E0B84E", trim="#E0B84E", awn=("#E0B84E", "#F2E6C2"), flag=("swallow", "plain", "#E0B84E", "#F4EEDC", "#F4EEDC"), pen=("#E0B84E", "#F4EEDC", None), sail=("#EDE4CC", "#C79A3C", "cross", "#A8321E")),
    "fransa": dict(hull="#5A3A22", wale="#233C8C", trim="#E0B84E", awn=("#233C8C", "#E0B84E"), flag=("swallow", "lily", "#233C8C", "#E0B84E", "#E0B84E"), pen=("#233C8C", "#E0B84E", "lily"), sail=("#EDE4CC", "#233C8C", "lily", "#233C8C")),
    "venedik": dict(hull="#6A4226", wale="#233C8C", trim="#E0B84E", awn=("#B33620", "#E0B84E"), flag=("swallow", "bands", "#B33620", "#E0B84E", "#E0B84E"), pen=("#B33620", "#E0B84E", "bands"), sail=("#EDE4CC", "#B33620", None, "#B33620")),
    "genel": dict(hull="#5A3A22", wale="#8A6A3A", trim="#C79A3C", awn=("#C79A3C", "#EDE4CC"), flag=("swallow", "stripes", "#233C8C", "#E0B84E", "#E0B84E"), pen=("#233C8C", "#E0B84E", None), sail=("#EDE4CC", "#8A6A3A", None, "#8A6A3A")),
}
LIVERY["hristiyan"]["name"] = "hristiyan"
ALIAS_LIV = dict(kutsal_birlik="hristiyan", haclı="hristiyan", turk="osmanli", turk_="osmanli", ottoman="osmanli", medici="toskana", tuscan="toskana", france="fransa", french="fransa",
                 papa="papalik", papal="papalik", venice="venedik", gold="toskana", plain="genel")


def livery(flag, side=None):
    """flag/side adından LIVERY sözlüğü (bilinmeyene 'genel'). Sözlük verilirse olduğu gibi (eksikleri 'genel'den)."""
    if isinstance(flag, dict):
        base = dict(LIVERY["genel"])
        base.update(flag)
        return base
    k = (flag or side or "genel")
    k = ALIAS_LIV.get(k, k)
    return LIVERY.get(k, LIVERY["genel"])


class LSpr:
    """Yerel koordinatlı sprite: (x0,y0) yerel birim, bs pişirme ölçeği."""
    __slots__ = ("img", "x0", "y0", "bs", "w", "h")

    def __init__(self, img, x0, y0, bs):
        self.img, self.x0, self.y0, self.bs = img, x0, y0, bs
        self.w, self.h = img.width() / bs, img.height() / bs

    def draw(self, c, alpha=1.0, paint=None):
        p = paint or skia.Paint()
        if alpha < 1.0:
            p.setAlphaf(alpha)
        c.drawImageRect(self.img, skia.Rect.MakeWH(self.img.width(), self.img.height()), skia.Rect.MakeXYWH(self.x0, self.y0, self.w, self.h), LIN, p)


def bake_local(bbox, bs, fn):
    x0, y0, x1, y1 = bbox
    fr = sk.Frame(int(math.ceil((x1 - x0) * bs)), int(math.ceil((y1 - y0) * bs)))
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    c.scale(bs, bs)
    c.translate(-x0, -y0)
    fn(c)
    return LSpr(fr.surf.makeImageSnapshot(), x0, y0, bs)


def _lit(c, path, a=46, a2=38, top_left=True):
    """Hull/yapı üzerine tek ışık yönü (sol-üst): üstte açık, altta ve sağda koyu overlay (path içine kırpılı)."""
    c.save()
    c.clipPath(path, skia.ClipOp.kIntersect, True)
    b = path.getBounds()
    sh = skia.GradientShader.MakeLinear([(b.left(), b.top()), (b.left() + b.width() * 0.35, b.bottom())],
                                        [C("#FFF4D0", a), C("#FFF4D0", 0), C("#1A1008", a2)], [0.0, 0.40, 1.0])
    c.drawRect(b, skia.Paint(Shader=sh))
    c.restore()


def _plank_lines(c, path, y_top_fn, xs, offs, col=INK, a=70, w=1.0):
    c.save()
    c.clipPath(path, skia.ClipOp.kIntersect, True)
    for o in offs:
        pts = [(float(x), float(y_top_fn(x) + o)) for x in xs]
        c.drawPath(poly(pts, False), _P(col, a, style="stroke", sw=w))
    c.restore()


def _mast(c, x, y0, y1, w0, w1, col="#6A4A2C"):
    p = poly([(x - w0 / 2, y0), (x + w0 / 2, y0), (x + w1 / 2, y1), (x - w1 / 2, y1)])
    fink(c, p, col, 1.2, 255, 190)
    c.drawLine(x - w0 * 0.15, y0, x - w1 * 0.15, y1, _P("#C9A06A", 90, style="stroke", sw=1.0))
    c.drawLine(x + w0 * 0.30, y0, x + w1 * 0.30, y1, _P("#1A1008", 80, style="stroke", sw=1.2))


def _yard(c, x0, y0, x1, y1, w=5.0, col="#7A5A34"):
    a = math.atan2(y1 - y0, x1 - x0)
    nx, ny = -math.sin(a) * w / 2, math.cos(a) * w / 2
    p = poly([(x0 + nx, y0 + ny), (x1 + nx * 0.6, y1 + ny * 0.6), (x1 - nx * 0.6, y1 - ny * 0.6), (x0 - nx, y0 - ny)])
    fink(c, p, col, 1.1, 255, 190)


# ═════════════════════════════ KADIRGA ═════════════════════════════
GAL_L = 600.0                 # nominal gövde boyu (kıç-baş, gaga hariç) — ship(h=…) bu boya göre ölçeklenir
GAL_OARS = np.linspace(-112.0, 212.0, 24)
GAL_PORT_Y = -34.0            # kürek lumbozu yüksekliği (yerel; su hattı 0)


def _gal_top(x):
    """Bel güvertesi üst kenarı (yerel y; negatif yukarı): sırtı bellerde alçak, başa doğru yükselir (rembata)."""
    return np.interp(x, [-150, -112, -20, 100, 214, 262, 290, 310], [-84, -50, -47, -48, -56, -65, -72, -70])


def galley_hull(tod, liv, bs=1.0):
    """Kadırga gövdesi sprite'ı (yerel: x ileri → +; su hattı y=0; kıç solda): gövde + kuşak/yaldız + kürek lumbozları + apostis + kıç kamarası + tente + fener + gaga + rembata kalkanları."""
    key = ("gal_hull", tod, liv["wale"], liv["hull"], liv["trim"], liv["awn"], round(bs, 2))
    if key in _SPR:
        return _SPR[key]
    T = Tint(tod)
    hull, wale, trim = T(liv["hull"]), T(liv["wale"]), T(liv["trim"])
    dk = T("#2A180C")

    def draw(c):
        # ── gövde ──
        body = skia.Path()
        body.moveTo(-250, 4)
        body.quadTo(-286, -6, -292, -50)
        body.quadTo(-296, -92, -282, -112)
        body.quadTo(-272, -122, -250, -120)
        body.lineTo(-150, -116)
        body.lineTo(-144, -78)
        body.quadTo(-140, -52, -112, -49)
        body.cubicTo(-20, -45, 120, -47, 214, -55)
        body.quadTo(262, -64, 290, -72)
        body.quadTo(308, -72, 312, -52)
        body.quadTo(308, -22, 288, -2)
        body.quadTo(268, 8, 236, 6)
        body.cubicTo(120, 9, -120, 10, -250, 4)
        body.close()
        sh = skia.GradientShader.MakeLinear([(0, -120), (0, 10)], [C(mix(hull, "#FFFFFF", 0.16)), C(hull), C(mix(hull, "#000000", 0.28))], [0.0, 0.55, 1.0])
        c.drawPath(body, skia.Paint(AntiAlias=True, Shader=sh))
        xs = np.linspace(-110, 300, 60)
        _plank_lines(c, body, _gal_top, xs, (13, 25, 37), "#1A0E06", 90, 1.1)
        xp = np.linspace(-270, -150, 20)
        _plank_lines(c, body, lambda x: -118.0 + 0 * x, xp, (12, 24, 36, 48, 60, 72, 84), "#1A0E06", 70, 1.0)
        # üst kuşak (apostis kirişi): koyu geniş şerit + kuşak rengi şeridi + yaldız çizgi
        c.save()
        c.clipPath(body, skia.ClipOp.kIntersect, True)
        xx = np.linspace(-146, 312, 70)
        top = [(float(x), float(_gal_top(x))) for x in xx]
        for off, col_, a_ in ((0, dk, 255), (9, wale, 255), (20, wale, 255)):
            pass
        # kuşak: üst kenardan 8–20 px aşağıda renkli şerit
        up = poly(top + [(float(x), float(_gal_top(x)) + 19) for x in xx[::-1]], True)
        c.drawPath(up, _P(wale))
        up2 = poly([(float(x), float(_gal_top(x))) for x in xx] + [(float(x), float(_gal_top(x)) + 7) for x in xx[::-1]], True)
        c.drawPath(up2, _P(dk))
        c.drawPath(poly([(float(x), float(_gal_top(x)) + 21) for x in xx], False), _P(trim, 255, style="stroke", sw=2.4))
        c.drawPath(poly([(float(x), float(_gal_top(x)) + 19) for x in xx], False), _P(INK, 150, style="stroke", sw=1.0))
        # kürek lumbozları
        for ox in GAL_OARS:
            yy = float(_gal_top(ox)) + 30
            c.drawOval(skia.Rect.MakeLTRB(ox - 4.2, yy - 3.2, ox + 4.2, yy + 3.2), _P("#0E0804", 235))
            c.drawOval(skia.Rect.MakeLTRB(ox - 4.2, yy - 3.2, ox + 4.2, yy + 3.2), _P(trim, 130, style="stroke", sw=0.9))
        # su hattı yosun/ıslaklık bandı
        wl = skia.GradientShader.MakeLinear([(0, -14), (0, 12)], [C("#1B2A1A", 0), C("#1B2A1A", 150)], [0.0, 1.0])
        c.drawRect(skia.Rect.MakeLTRB(-320, -14, 340, 14), skia.Paint(Shader=wl))
        c.restore()
        # ── kıç kamarası (poop): panolar, kemerli pencereler, yaldız çerçeve ──
        cab = poly([(-286, -112), (-262, -120), (-152, -116), (-146, -80), (-286, -78)])
        c.save()
        c.clipPath(body, skia.ClipOp.kIntersect, True)
        c.drawPath(cab, _P(T(mix(liv["hull"], "#7A5030", 0.35))))
        for i, wx in enumerate((-250, -212, -174)):
            ww = 26
            wp = skia.Path()
            wp.moveTo(wx - ww / 2, -82)
            wp.lineTo(wx - ww / 2, -100)
            wp.arcTo(skia.Rect.MakeLTRB(wx - ww / 2, -100 - ww / 2, wx + ww / 2, -100 + ww / 2), 180, 180, False)
            wp.lineTo(wx + ww / 2, -82)
            wp.close()
            c.drawPath(wp, _P(T("#1C1208")))
            c.drawPath(wp, _P(trim, 255, style="stroke", sw=2.4))
            if tod in ("night", "dusk", "fire"):
                c.drawPath(wp, _P("#FFC060", 190 if tod == "night" else 90))
            c.drawLine(wx, -82, wx, -113, _P(trim, 200, style="stroke", sw=1.0))
        c.drawLine(-288, -90, -146, -90, _P(trim, 255, style="stroke", sw=2.0))
        c.drawLine(-288, -112, -150, -108, _P(trim, 255, style="stroke", sw=3.0))
        c.restore()
        _lit(c, body, 52, 44)
        c.drawPath(body, _P(INK, 215, style="stroke", sw=2.1))
        # kıç kıvrımı (yaldız volüt) + bayrak soketi
        sc = skia.Path()
        sc.moveTo(-282, -114)
        sc.cubicTo(-300, -140, -318, -148, -314, -170)
        sc.cubicTo(-310, -182, -292, -180, -292, -168)
        sc.cubicTo(-292, -158, -304, -156, -304, -164)
        c.drawPath(sc, _P(trim, 255, style="stroke", sw=5.0))
        c.drawPath(sc, _P(INK, 170, style="stroke", sw=1.2))
        # ── baş: gaga (sperone) + rembata platformu + kalkanlar ──
        beak = poly([(296, -58), (372, -50), (374, -44), (296, -40)])
        fink(c, beak, T("#6A4A2C"), 1.4, 255, 200)
        c.drawPath(poly([(364, -52), (378, -49), (378, -44), (364, -44)]), _P(T("#9AA0A8")))
        c.drawPath(poly([(364, -52), (378, -49), (378, -44), (364, -44)]), _P(INK, 170, style="stroke", sw=1.0))
        plat = poly([(212, -56), (300, -72), (300, -84), (212, -70)])
        c.drawPath(plat, _P(dk))
        n = 6
        for i in range(n):
            sx = 224 + i * 13.2
            sy = -69 - i * 2.0
            c.drawCircle(sx, sy - 4, 6.0, _P(T([wale, trim][i % 2])))
            c.drawCircle(sx, sy - 4, 6.0, _P(INK, 170, style="stroke", sw=0.9))
            c.drawCircle(sx, sy - 4, 1.8, _P(T("#F4EEDC"), 220))
        # baş süsü (yaldız kıvrım)
        bs_ = skia.Path()
        bs_.moveTo(312, -52)
        bs_.cubicTo(326, -62, 330, -78, 318, -88)
        c.drawPath(bs_, _P(trim, 255, style="stroke", sw=3.6))
        c.drawPath(bs_, _P(INK, 150, style="stroke", sw=1.0))
        # ── kıç direkleri/tente ──
        for px in (-268, -226, -188, -156):
            _mast(c, px, -228, -116, 2.6, 3.0, T("#6A4A2C"))
        awn = skia.Path()
        awn.moveTo(-296, -212)
        awn.quadTo(-218, -240, -150, -216)
        awn.lineTo(-146, -184)
        n_s = 9
        for i in range(n_s + 1):
            x_ = -146 + (-150) * i / n_s
            awn.quadTo(x_ + 8, -174 + (3 if i % 2 else 0), x_ - 8, -184 + (4 if i % 2 else -2))
        awn.close()
        c.save()
        c.clipPath(awn, skia.ClipOp.kIntersect, True)
        a1, a2 = T(liv["awn"][0]), T(liv["awn"][1])
        c.drawPath(awn, _P(a1))
        for i in range(0, 18, 2):
            c.drawRect(skia.Rect.MakeLTRB(-296 + i * 8.5, -250, -296 + (i + 1) * 8.5, -156), _P(a2))
        _lit(c, awn, 60, 50)
        c.restore()
        c.drawPath(awn, _P(INK, 200, style="stroke", sw=1.6))
        # fener (kıçta)
        _mast(c, -300, -226, -166, 3.4, 3.6, T("#6A4A2C"))
        lp = poly([(-308, -256), (-292, -256), (-290, -232), (-310, -232)])
        fink(c, lp, T("#C79A3C"), 1.1, 255, 190)
        c.drawPath(poly([(-306, -252), (-294, -252), (-294, -236), (-306, -236)]), _P(T("#FFE9B0") if tod != "day" else T("#E8D6A0")))
        c.drawPath(poly([(-310, -256), (-300, -268), (-290, -256)]), _P(T("#8A6422")))
        c.drawPath(poly([(-310, -256), (-300, -268), (-290, -256)]), _P(INK, 180, style="stroke", sw=1.0))

    spr = bake_local((-322, -276, 392, 22), bs, draw)
    _spr_put(key, spr)
    return spr


def _nbytes(v):
    """Sprite / sprite listesi bellek tahmini (RGBA bayt)."""
    if isinstance(v, LSpr):
        return v.img.width() * v.img.height() * 4
    if isinstance(v, (list, tuple)):
        return sum(_nbytes(e) for e in v)
    return 0


class _LRU(collections.OrderedDict):
    """Bayt bütçeli LRU önbellek: bütçe aşılınca en az kullanılan sprite atılır (tembel yeniden pişer); tümünü silip yeniden pişirme (takılma) yok."""

    def __init__(self, budget):
        super().__init__()
        self.budget = budget
        self.size = 0

    def __getitem__(self, k):
        v = super().__getitem__(k)
        self.move_to_end(k)
        return v

    def get(self, k, d=None):
        return self[k] if k in self else d

    def put(self, k, v):
        if k in self:
            self.size -= _nbytes(super().__getitem__(k))
        super().__setitem__(k, v)
        self.move_to_end(k)
        self.size += _nbytes(v)
        while self.size > self.budget and len(self) > 1:
            _, old = self.popitem(last=False)
            self.size -= _nbytes(old)


_SPR = _LRU(150 * 1024 * 1024)


def _spr_put(key, spr):
    """Gemi sprite önbelleği (bayt bütçeli LRU: 150 MB)."""
    _SPR.put(key, spr)


def galley_rig(tod, liv, sails=True, bs=1.0):
    """Kadırga direkleri (ana + baş) ve antenalar; sails=False → toplanmış yelken sarımı; True → çıplak antena (yelken mesh ayrı çizilir)."""
    key = ("gal_rig", tod, bool(sails), liv["trim"], round(bs, 2))
    if key in _SPR:
        return _SPR[key]
    T = Tint(tod)

    def draw(c):
        mm = T("#6A4A2C")
        _mast(c, 30, -48, -298, 7.5, 5.0, mm)                           # ana direk
        _mast(c, 190, -66, -226, 5.6, 3.6, mm)                          # baş direk (trinket)
        c.drawCircle(30, -300, 4.6, _P(T(liv["trim"])))
        c.drawCircle(30, -300, 4.6, _P(INK, 170, style="stroke", sw=1.0))
        # ana antena: ön-alt uçtan arka-üste (dümen yönünde yükselir), direğe bağlı
        tack, peak = (212, -80), (-132, -292)
        _yard(c, tack[0], tack[1], peak[0], peak[1], 5.2, T("#7A5A34"))
        if not sails:
            # toplanmış yelken sarımı: antenanın altında kalın bez + bağlar
            a = math.atan2(peak[1] - tack[1], peak[0] - tack[0])
            nx, ny = -math.sin(a), math.cos(a)
            pts = []
            for i in range(0, 41):
                u = 0.04 + 0.92 * i / 40
                px_, py_ = tack[0] + (peak[0] - tack[0]) * u, tack[1] + (peak[1] - tack[1]) * u
                bulge = 5.5 + 2.2 * math.sin(u * 17.0)
                pts.append((px_ + nx * bulge, py_ + ny * bulge))
            pts2 = [(tack[0] + (peak[0] - tack[0]) * (0.04 + 0.92 * i / 40), tack[1] + (peak[1] - tack[1]) * (0.04 + 0.92 * i / 40)) for i in range(40, -1, -1)]
            roll = poly(pts + pts2, True)
            fink(c, roll, T("#E4D8B8"), 1.2, 255, 190)
            for i in range(1, 11):
                u = 0.04 + 0.92 * i / 11
                px_, py_ = tack[0] + (peak[0] - tack[0]) * u, tack[1] + (peak[1] - tack[1]) * u
                c.drawLine(px_ + nx * 9, py_ + ny * 9, px_ - nx * 2, py_ - ny * 2, _P("#6A4A2C", 230, style="stroke", sw=1.8))
        # baş direk antenası (küçük)
        _yard(c, 252, -88, 118, -214, 4.2, T("#7A5A34"))
        # direk ipleri: ana direk tepesinden gövdeye, kıç ve başa
        for (x1, y1) in ((-140, -140), (-40, -84), (110, -62), (214, -62)):
            c.drawLine(30, -296, x1, y1, _P(INK, 150, style="stroke", sw=0.9))
        for (x1, y1) in ((190, -226), (236, -80), (150, -64)):
            c.drawLine(190, -224, x1, y1, _P(INK, 140, style="stroke", sw=0.8))

    spr = bake_local((-160, -322, 280, -30), bs, draw)
    _spr_put(key, spr)
    return spr


# ═════════════════════════════ GEMİ SPESİFİKASYONU / HAREKET ═════════════════════════════
KIND_ALIAS = dict(kadirga="kadirga", galley="kadirga", galera="kadirga", nao="nao", karrak="nao", carrack="nao", karaka="nao", tekne="tekne", boat="tekne", kayik="kayik", kayık="kayik", caique="kayik")
KIND_LEN = dict(kadirga=GAL_L, nao=430.0, tekne=190.0, kayik=210.0)


def _tcall(cx, a, default=0.0):
    """Çapa/saniye → yerel sn."""
    if a is None:
        return default
    if isinstance(a, (int, float)):
        return float(a)
    try:
        return float(cx.at(a))
    except Exception:
        return default


def _ease(name, u):
    u = clamp(u)
    if name == "io":
        return u * u * (3 - 2 * u)
    if name == "out":
        return 1 - (1 - u) ** 2.2
    if name == "in":
        return u ** 1.8
    return u


class ShipSpec:
    """Normalleştirilmiş gemi tarifi. dict anahtarları: kind, x0, x1 | dir+speed, y, scale, flag/side, t0, t1, sails, oars, crew, seed, hz, highlight, ensign, route, ease, arms, name…"""

    def __init__(self, d, cx=None, dur=10.0, idx=0):
        d = dict(d)
        self.kind = KIND_ALIAS.get(d.get("kind", "kadirga"), "kadirga")
        self.raw = d
        self.idx = idx
        self.seed = int(d.get("seed", idx * 7 + 3))
        self.y = float(d.get("y", 640.0))
        self.scale = float(d.get("scale", 1.0))
        self.x0 = float(d.get("x0", 960.0))
        self.speed = float(d.get("speed", 60.0))
        self.t0 = _tcall(cx, d.get("t0", 0.0), 0.0) if cx is not None else float(d.get("t0", 0.0) or 0.0)
        self.t1 = _tcall(cx, d.get("t1"), None) if cx is not None and d.get("t1") is not None else (float(d["t1"]) if d.get("t1") is not None else None)
        self.ease = d.get("ease", "lin")
        self.route = d.get("route")
        self.x1 = d.get("x1")
        self.dirn = int(d.get("dir", 0)) or 0
        if self.route:
            r = [(float(a), float(b)) for a, b in self.route]
            self.route = r
            self.x0, self.y = r[0]
            self._rb = _route_build(r)
            if not self.dirn:
                self.dirn = 1 if r[-1][0] >= r[0][0] else -1
        elif self.x1 is not None:
            self.x1 = float(self.x1)
            if not self.dirn:
                self.dirn = 1 if self.x1 >= self.x0 else -1
            if self.t1 is None:
                self.t1 = self.t0 + abs(self.x1 - self.x0) / max(1.0, self.speed)
        else:
            if not self.dirn:
                self.dirn = 1
        self.flag = d.get("flag", d.get("side"))
        self.liv = livery(self.flag, d.get("side"))
        self.sails = d.get("sails", True)
        self.oars = d.get("oars", True)
        self.crew = d.get("crew", True)
        self.hz = float(d.get("hz", 0.80))
        self.highlight = bool(d.get("highlight", False))
        self.ensign = d.get("ensign", True)
        self.wind = float(d.get("wind", 1.0))
        self.arms = d.get("arms")
        self.sail_set = d.get("sail_set")
        self.label = d.get("label")
        self.tilt = float(d.get("tilt", 1.0))
        self.wake = float(d.get("wake", 1.0))
        self.ph = hash01(self.seed, 5)
        self.extra = d

    def length(self):
        return KIND_LEN[self.kind] * self.scale

    def pos(self, t):
        """(x, y, dirn, hız_px_s) — t yerel saniye (negatif: ön-tur, doğrusal uzatma)."""
        if self.route:
            u = _ease(self.ease if self.ease != "lin" else "io", (t - self.t0) / max(1e-6, (self.t1 - self.t0))) if self.t1 is not None else clamp((t - self.t0) / 10.0)
            x, y, tx = _route_at(self._rb, u)
            dirn = self.dirn if abs(tx) < 0.25 else (1 if tx > 0 else -1)
            sp = 0.0
            if self.t1 is not None:
                x2, y2, _ = _route_at(self._rb, _ease(self.ease if self.ease != "lin" else "io", (t + 0.1 - self.t0) / max(1e-6, (self.t1 - self.t0))))
                sp = math.hypot(x2 - x, y2 - y) / 0.1
            return x, y, dirn, sp
        if self.x1 is not None:
            span = max(1e-6, (self.t1 - self.t0))
            u = (t - self.t0) / span
            ee = _ease(self.ease, u) + ((u - clamp(u)) if self.ease == "lin" else 0.0)
            x = self.x0 + (self.x1 - self.x0) * ee
            du = 0.05 / span
            sp = abs(self.x1 - self.x0) * abs(_ease(self.ease, u + du) - _ease(self.ease, u)) / 0.05 if 0.0 <= u < 1.0 else (self.speed if (u < 0 and self.ease == "lin") else 0.0)
            return x, self.y, self.dirn, sp
        return self.x0 + self.dirn * self.speed * (t - self.t0), self.y, self.dirn, abs(self.speed)


def _route_build(pts):
    """Rota: Catmull-Rom ile yumuşatılmış çokgen + yay uzunluğu tablosu."""
    P = np.array(pts, float)
    if len(P) == 2:
        P = np.array([P[0], (P[0] + P[1]) / 2, P[1]])
    # basit Catmull-Rom örnekleme
    Pe = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    for i in range(len(P) - 1):
        p0, p1, p2, p3 = Pe[i], Pe[i + 1], Pe[i + 2], Pe[i + 3]
        for k in range(40):
            u = k / 40.0
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3))
    out.append(P[-1])
    Q = np.array(out)
    seg = np.hypot(*(Q[1:] - Q[:-1]).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    return Q, cum


def _route_at(rb, u):
    Q, cum = rb
    s = clamp(u) * cum[-1]
    i = int(np.searchsorted(cum, s, side="right") - 1)
    i = max(0, min(len(Q) - 2, i))
    f = (s - cum[i]) / max(1e-9, cum[i + 1] - cum[i])
    p = Q[i] + (Q[i + 1] - Q[i]) * f
    tg = Q[min(len(Q) - 1, i + 3)] - Q[max(0, i - 1)]
    n = math.hypot(*tg) or 1.0
    return float(p[0]), float(p[1]), float(tg[0] / n)


# ═════════════════════════════ GEMİ ÇİZİMİ: ortak katman (dönüşüm, su eteği, iz, ripple) ═════════════════════════════
BUCKETS = (0.28, 0.42, 0.62, 0.9, 1.3, 1.9)


def bucket(sz):
    for b in BUCKETS:
        if b >= sz * 0.88:
            return b
    return BUCKETS[-1]


def xf_point(x, y, pitch_deg, s, dirn, lx, ly):
    """Gemi yerel (lx,ly) → katman koordinatı."""
    px, py = lx * dirn * s, ly * s
    a = pitch_deg * D2R
    ca, sa = math.cos(a), math.sin(a)
    return x + px * ca - py * sa, y + px * sa + py * ca


def ease_io(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


def _oar_pose(u, af=34.0, ab=-29.0, lift_h=34.0):
    """Kürek çekişi evresi u (0..1): (α derece, kaldırma 0..1). 0.00–0.44 çekiş (su altı), 0.44–0.54 çıkış, 0.54–0.90 geri dönüş (havada), 0.90–1.0 giriş."""
    if u < 0.44:
        a = af + (ab - af) * ease_io(u / 0.44)
    else:
        a = ab + (af - ab) * ease_io((u - 0.44) / 0.56)
    if u < 0.40:
        lf = 0.0
    elif u < 0.52:
        lf = ease_io((u - 0.40) / 0.12)
    elif u < 0.88:
        lf = 1.0
    elif u < 0.99:
        lf = 1.0 - ease_io((u - 0.88) / 0.11)
    else:
        lf = 0.0
    return a, lf


def galley_oars(c, t, S, tod, hz=0.8, state=0.0, detail=1.0, lit=True):
    """Yerel çerçevede (kıç solda) 24 küreği çizer; dönüş: [(yerel_x, yerel_y, yaş 0..1)] kürek ucu halka konumları (su ripple'ı). state: 0 çekiş … 1 kürekler dikey kaldırılmış."""
    T = Tint(tod)
    wood, bl = T("#9A6A3A"), T("#C99B5A")
    band = T(S.liv["wale"])
    out = []
    n = len(GAL_OARS)
    for i in range(n):
        ox = float(GAL_OARS[i])
        oy = float(_gal_top(ox)) + 30.0
        u = (t * hz + hash01(S.seed, i) * 0.035 + 0.0013 * i) % 1.0
        a, lf = _oar_pose(u)
        dx = 150.0 * math.sin(a * D2R)
        ty = 41.0 * math.cos(a * D2R) * (1.0 - 0.58 * lf) - 20.0 * lf          # su yüzeyine giriş noktası ekranda gövdenin ÖNÜNDE (perspektif): y > 0
        dy = ty - oy
        if state > 0.001:
            ang_up = math.sin(t * 1.3 + i * 0.7) * 2.0
            ux = ox + 6.0 + ang_up
            uy = oy - 175.0
            e = ease_io(state)
            dx = (ux - ox) * e + dx * (1 - e)
            dy = (uy - oy) * e + dy * (1 - e)
        tx, tyy = ox + dx, oy + dy
        L = math.hypot(dx, dy) or 1.0
        nx, ny = dx / L, dy / L
        # gövde
        c.drawLine(ox, oy, tx, tyy, _P(INK, 190, style="stroke", sw=3.8))
        c.drawLine(ox, oy, tx, tyy, _P(wood, 255, style="stroke", sw=2.3))
        c.drawLine(ox - nx * 0 - 0.6, oy - 0.6, tx - 0.6, tyy - 0.6, _P("#F6D9A0", 80, style="stroke", sw=1.0))
        # kürek yaprağı (son %26)
        bx0, by0 = tx - nx * L * 0.22, tyy - ny * L * 0.22
        px, py = -ny, nx
        bw = 3.6
        blade = poly([(bx0 + px * 2.2, by0 + py * 2.2), (tx + px * bw, tyy + py * bw), (tx - px * bw, tyy - py * bw), (bx0 - px * 2.2, by0 - py * 2.2)])
        c.drawPath(blade, _P(bl))
        c.drawPath(blade, _P(INK, 190, style="stroke", sw=1.2))
        bxm, bym = tx - nx * L * 0.12, tyy - ny * L * 0.12
        c.drawLine(bxm - px * 2.8, bym - py * 2.8, bxm + px * 2.8, bym + py * 2.8, _P(band, 255, style="stroke", sw=1.8))
        if state < 0.5 and lf < 0.5:
            out.append((tx, tyy, clamp(u / 0.44)))
        elif state < 0.5 and u > 0.40 and u < 0.62:
            out.append((tx, tyy, clamp(0.55 + (u - 0.40) * 2.0)))
    return out


def draw_ripples(c, pts, sc, col, a=0.6):
    """Kürek/gövde ripple halkaları: (x, y, yaş) listesi; yaş büyüdükçe halka açılır ve solar. Katman çerçevesinde (su yüzeyi)."""
    for (x, y, age) in pts:
        r = (4.0 + 34.0 * age) * sc
        al = clamp(a * (1.0 - age) ** 1.3)
        if al < 0.03:
            continue
        c.drawOval(skia.Rect.MakeLTRB(x - r, y - r * 0.22, x + r, y + r * 0.22), _P(col, int(255 * al), style="stroke", sw=max(0.8, 1.6 * sc)))


def draw_bow_wave(c, x, y, s, dirn, t, speed, tod, P):
    """Baş dalgası: kıç tarafa doğru akan köpük dilleri (hıza göre büyür). Katman çerçevesi."""
    k = clamp(speed / 70.0)
    if k < 0.05:
        return
    sc = s
    for j in range(4):
        ph = (t * (0.9 + 0.2 * j) + j * 0.27) % 1.0
        L = (26 + 58 * ph) * sc * k
        hh = (10 - 7 * ph) * sc * k * (1.0 - 0.15 * j)
        bx = x - dirn * (8 + 22 * j) * sc * 0.5
        p = skia.Path()
        p.moveTo(bx, y)
        p.quadTo(bx - dirn * L * 0.4, y - hh, bx - dirn * L, y - hh * 0.2 + 1)
        p.quadTo(bx - dirn * L * 0.5, y + 1.5 * sc, bx, y + 2.0 * sc)
        p.close()
        al = (1 - ph) ** 0.9 * 0.85 * k
        c.drawPath(p, _P(P["foam"], int(255 * al)))
        c.drawPath(p, _P(P["ink"], int(70 * al), style="stroke", sw=0.9))


def draw_wake(c, S, t, s, sea_row, P, stern_off, n=16, life=3.4, bump=0.0):
    """Kıçtan açılan iz: geçmiş konumlardan ('t − yaş') köpük lekeleri; hız arttıkça belirir. Katman çerçevesinde (geminin satırı)."""
    sc = sea_row.sc * 0.0 + s
    for k in range(n):
        age = (k + 1) * life / n
        x, y, d, sp = S.pos(t - age)
        sp = max(sp, 0.0) * S.wake
        if sp < 6.0:
            continue
        u = age / life
        kk = clamp(sp / 80.0)
        rx = (20 + 70 * u) * sc * (0.5 + 0.5 * kk)
        ry = (3.0 + 7.0 * u) * sc
        al = (1 - u) ** 1.25 * 0.72 * kk
        cx_ = x - d * stern_off * s + math.sin(age * 4.0 + k) * 2.0 * sc
        cy_ = y + 4.0 * sc
        c.drawOval(skia.Rect.MakeLTRB(cx_ - rx, cy_ - ry, cx_ + rx, cy_ + ry), _P(P["foam"], int(255 * al * 0.7)))
        c.drawOval(skia.Rect.MakeLTRB(cx_ - rx, cy_ - ry, cx_ + rx, cy_ + ry), _P(P["crest"], int(255 * al * 0.55), style="stroke", sw=max(0.8, 1.4 * sc)))


# ═════════════════════════════ KADIRGA ÇİZİMİ (dinamik) ═════════════════════════════
GAL_CREW = [  # (tür, x, y(ayak), eylem, boy, kw)
    ("soylu", -208, -112, "point", 62, dict(t0=0.5, dur=3.0)),
    ("denizci", -170, -112, "idle", 58, {}),
    ("denizci", -26, -42, "work", 56, dict(mode="haul", period=1.5)),
    ("denizci", 6, -42, "work", 56, dict(mode="haul", period=1.5)),
    ("asker", 238, -76, "idle", 54, dict(prop="spear")),
    ("asker", 268, -82, "idle", 54, {}),
]
OSM_ROBES = ["#2E6A4F", "#A8321E", "#233C8C", "#C79A3C", "#1F5A7A"]


def _crew_style(S, i, kind):
    """Safa göre kıyafet: Osmanlı için sarık + uzun cübbe tonları; Hristiyan için öntanımlı."""
    f = S.liv.get("name")
    if f == "osmanli":
        rs = _RS(S.seed * 13 + i)
        st = dict(hat="turban", hat_col=["#EDE4CC", "#A8321E", "#2E6A4F"][rs.randint(3)], robe=OSM_ROBES[rs.randint(len(OSM_ROBES))])
        if kind == "asker":
            st["hat_col"] = ["#EDE4CC", "#A8321E"][rs.randint(2)]
        return st
    return {}


def draw_crew(ctx, S, spots, t, s, dirn, lod_ok=True):
    if not lod_ok or not S.crew:
        return
    f = ctx.f
    FA.set_scale_hint(ctx.z * s)
    for i, (kind, x, y, act, h, kw) in enumerate(spots):
        kw = dict(kw)
        st = _crew_style(S, i, kind)
        try:
            FA.actor(f, kind, x, y, h, t, action=act, dir=1, seed=S.seed * 5 + i, phase=hash01(S.seed, i), **st, **kw)
        except Exception:
            pass
    FA.set_scale_hint(1.0)


def _oar_mode(S, t=0.0):
    """oars: True → çekiyor (0.0) · False → kürekler toplanmış, çizilmez (None) · sayı 0..1 → kısmen/tam kaldırılmış (1 = dikey) · callable(t) → yukarıdakilerden biri."""
    o = S.oars
    if callable(o):
        o = o(t)
    if o is True:
        return 0.0
    if o is False or o is None:
        return None
    if isinstance(o, str):
        return 1.0 if o in ("up", "kaldir", "kaldır") else 0.0
    return float(o)


def draw_flags_galley(c, S, t, fl, wind, tod):
    liv = S.liv
    pc1, pc2, pdev = liv["pen"]
    if S.highlight:
        pc1, pc2, pdev = "#E0B84E", "#B33620", None
    flip = 1 if fl > 0 else -1
    # direk tepesi flaması + baş direği flaması
    flag(c, 30, -310, 190, 32, t, "pennant", pdev or "plain", pc1, pc2, pc2, wind=wind, ph=S.seed * 1.3, flipx=flip)
    flag(c, 190, -234, 112, 21, t, "pennant", "plain", pc1, pc2, pc2, wind=wind, ph=S.seed * 2.1, flipx=flip)
    if S.ensign:
        # kıç sancağı: kalın direk + büyük bayrak
        c.drawLine(-246, -118, -246, -318, _P(INK, 200, style="stroke", sw=4.8))
        c.drawLine(-246, -118, -246, -318, _P(Tint(tod)("#8A6A3C"), 255, style="stroke", sw=3.0))
        c.drawCircle(-246, -320, 4.0, _P(Tint(tod)(liv["trim"])))
        fg = liv["flag"]
        flag(c, -246, -316, 104, 62, t, fg[0], fg[1], fg[2], fg[3], fg[4], wind=wind, ph=S.seed * 0.9, flipx=flip)


def draw_galley(ctx, sea, S, t, x, y, s, dirn, sp, pitch):
    """Kadırga (dinamik): [rig] → [mürettebat] → [gövde] → [yelken] → [kürekler] → [bayraklar]. Katman push'u çağıranda; gemi dönüşümü burada. Dönüş: ripple noktaları (yerel)."""
    c = ctx.c
    liv = S.liv
    z = ctx.z
    bs = bucket(s * z)
    tod = ctx.tod
    T = Tint(tod)
    fl = getattr(ctx, "wind_dir", 1) * dirn
    wind = S.wind * getattr(ctx, "wind", 1.0)
    c.save()
    c.translate(x, y)
    c.rotate(pitch)
    c.scale(dirn * s, s)
    sails_on = bool(S.sails)
    galley_rig(tod, liv, sails_on, bs).draw(c)
    if S.crew and s * z * GAL_L > 240:
        draw_crew(ctx, S, GAL_CREW, t, s, dirn)
    galley_hull(tod, liv, bs).draw(c)
    if sails_on:
        sl = liv["sail"]
        lateen_sail(c, (212, -80), (-132, -292), (-122, -104), t, wind, ph=S.seed * 0.7, col=T(sl[0]), trim=T(sl[1]), dev=None, devcol=T(sl[3]), seed=S.seed)
    draw_flags_galley(c, S, t, fl, wind, tod)
    if S.highlight:
        glow(c, 30 + fl * 70, -296, 90, "#FFE08A", 0.35 + 0.1 * math.sin(t * 3.0))
    if tod in ("night", "dusk", "fire"):
        fk = 0.8 + 0.2 * math.sin(t * 9.0 + S.seed) + 0.06 * math.sin(t * 23.0)
        glow(c, -300, -244, 80 * fk, "#FFC060", (0.62 if tod == "night" else 0.34) * fk)
    c.restore()
    om = _oar_mode(S, t)
    if om is None:
        return None

    def late(cl):
        hz = S.hz * (0.45 + 0.55 * clamp(sp / 60.0))
        return galley_oars(cl, t, S, tod, hz, om)
    return late


# ═════════════════════════════ GEMİ: katmana yerleştirme (dalga sürüşü, su eteği, iz, ripple) ═════════════════════════════
def _draw_by_kind(ctx, sea, S, t, x, y, s, dirn, sp, pitch):
    k = S.kind
    if k == "kadirga":
        return draw_galley(ctx, sea, S, t, x, y, s, dirn, sp, pitch)
    fn = KIND_DRAW.get(k)
    return fn(ctx, sea, S, t, x, y, s, dirn, sp, pitch) if fn else []


KIND_DRAW = {}


def _hull_for(S, tod, bs):
    if S.kind == "kadirga":
        return galley_hull(tod, S.liv, bs)
    if S.kind == "nao":
        return nao_hull(tod, S.liv, S.arms, bs)
    return None


def draw_reflection(c, hull, x, y, s, dirn, pitch, t, alpha=0.20, squash=0.42, seed=0):
    """Gövde yansıması: dikey çevrilmiş, sıkıştırılmış ve dalga şeritlerine bölünmüş (yatay salınım) soluk kopya. Katman çerçevesinde (su hattı y)."""
    if hull is None:
        return
    nb = 7
    ih, iw = hull.img.height(), hull.img.width()
    # yerel y aralığı: gövde su hattı üstünde [y0, 0]; yansıma 0 .. −y0·squash
    top = hull.y0
    seg_h = min(0.0, -top - 24.0) / nb if False else (-top) / nb
    p = skia.Paint()
    p.setAlphaf(alpha)
    c.save()
    c.translate(x, y)
    c.rotate(pitch)
    c.scale(dirn * s, s)
    for i in range(nb):
        y_a = -(i + 1) * seg_h * 1.0 + 0.0
        # kaynak şerit (görüntü pikseli): gövde y∈[−(i+1)h, −i h] → su hattından yukarı doğru
        sy0 = (hull.h + hull.y0 - (i + 1) * seg_h) * hull.bs if False else ((-(i + 1) * seg_h - hull.y0) * hull.bs)
        sy1 = ((-(i) * seg_h - hull.y0) * hull.bs)
        sy0, sy1 = max(0.0, sy0), min(float(ih), sy1)
        if sy1 - sy0 < 1:
            continue
        dy0 = i * seg_h * squash
        dy1 = (i + 1) * seg_h * squash
        dx = math.sin(t * 2.1 + i * 1.3 + seed) * (1.0 + 0.9 * i) * 1.2
        c.drawImageRect(hull.img, skia.Rect.MakeLTRB(0, sy0, iw, sy1), skia.Rect.MakeLTRB(hull.x0 + dx, dy0, hull.x0 + hull.w + dx, dy1 + 0.6), LIN, p)
    c.restore()


def render_ship(ctx, sea, S, t, fixed_scale=None, row=None, defer=True):
    """Bir gemiyi kendi su satırı çerçevesinde çiz: [iz] → gemi → su eteği; sonra (2 satır sonra, önündeki dalgaların ÜSTÜNE): yansıma, kürekler + ripple, baş dalgası.
    Satır, geminin su hattına göre (sea.row_before) seçilir."""
    x, y, dirn, sp = S.pos(t)
    k = sea.row_before(y)
    ru = row or sea.rows[max(0, k - 1)]
    s = fixed_scale if fixed_scale is not None else S.scale * persp(y, sea.yh)
    Lh = KIND_LEN[S.kind] * s
    if not ctx.visible(ru.f, x - Lh * 0.95, x + Lh * 0.95, 0.0):
        return
    P = ctx.P
    ctx.push(ru.f)
    c = ctx.c
    wy = float(sea.wave(ru, x, t))
    sl = float(sea.slope(ru, x, t))
    heave = 0.8 * wy
    pitch = clamp(math.degrees(math.atan(sl * 0.85)) * S.tilt, -5.0, 5.0)
    yy = y + heave
    draw_wake(c, S, t, s, ru, P, KIND_LEN[S.kind] * 0.46 / max(S.scale, 1e-6), n=14)
    late = _draw_by_kind(ctx, sea, S, t, x, yy, s, dirn, sp, pitch)
    sea.skirt(ctx, ru, x - Lh * 0.54, x + Lh * 0.58, yy, t, depth=10.0 * max(0.5, s))
    ctx.pop()

    def late_pass():
        ctx.push(ru.f)
        cc = ctx.c
        draw_reflection(cc, _hull_for(S, ctx.tod, bucket(s * ctx.z)), x, yy, s, dirn, pitch, t, 0.20 if ctx.tod != "night" else 0.30, seed=S.seed)
        if late is not None:
            cc.save()
            cc.translate(x, yy)
            cc.rotate(pitch)
            cc.scale(dirn * s, s)
            pts = late(cc)
            cc.restore()
            if pts:
                rp = []
                for (lx, ly, age) in pts:
                    px, py = xf_point(x, yy, pitch, s, dirn, lx, ly)
                    rp.append((px, py, age))
                draw_ripples(cc, rp, s * 0.9, P["crest"], 0.75)
        draw_bow_wave(cc, x + dirn * Lh * 0.50, yy, s, dirn, t, sp, ctx.tod, P)
        ctx.pop()
    if defer and not getattr(ctx, "no_defer", False):
        due = min(sea.n, k + 2)
        ctx.deferred.setdefault(due, []).append(late_pass)
    else:
        late_pass()


def ship(f, kind, x, y, h, t, dir=1, flag=None, sails=True, oars=True, tod="day", z=1.0, wind=1.0, wind_dir=-1, water=True, crew=True, speed=60.0, highlight=False, seed=3, swell=1.0, **kw):
    """BAĞIMSIZ gemi çizimi (haritaya/başka çekime serpiştirme): f (sk.Frame) üzerine, (x,y) = su hattı orta noktası, h = gövde BOYU (px; kadırga nominal 600, nao 430), t = sn, dir=±1,
    kind = kadirga|nao|tekne|kayik, flag = livery adı (hristiyan|osmanli|toskana|papalik|fransa|venedik|genel) ya da sözlük, sails/oars/crew açma-kapama (oars: True | False | 0..1 kaldırılmış),
    water=True: su eteği + iz + ripple (kendi küçük dalga satırı). Dönüş: None."""
    class _CX:
        pass
    cx = _CX()
    cx.t = t
    ctx = Ctx(f, cx, W / 2, 0.0, z, (0, H), tod)
    ctx.wind, ctx.wind_dir = wind, wind_dir
    kd = KIND_ALIAS.get(kind, "kadirga")
    d = dict(kind=kd, x0=x, y=y, scale=h / KIND_LEN[kd], dir=dir, flag=flag, sails=sails, oars=oars, crew=crew, speed=speed if (dir is not None) else 0.0, highlight=highlight, seed=seed)
    d.update(kw)
    S = ShipSpec(d, None)
    sea = Sea(tod, yh=y - 260.0, ybot=y + 120.0, n=10, seed=seed, swell=swell * 0.8)
    if water:
        # su satırı: geminin hemen altında bir dalga satırı (yalnız etek ve ritim için)
        rrow = sea.rows[max(0, sea.row_before(y) - 1)]
        rrow.f = 1.0
        render_ship(ctx, sea, S, t, fixed_scale=S.scale, row=rrow, defer=False)
    else:
        ctx.push(1.0)
        _draw_by_kind(ctx, sea, S, t, x, y, S.scale, S.dirn, speed, 0.0)
        ctx.pop()


# ═════════════════════════════ NAO / KARRAK ═════════════════════════════
NAO_L = 430.0


def _nao_top(x):
    """Bel güvertesi/küpeşte üst kenarı (yerel y)."""
    return np.interp(x, [-40, -34, 10, 90, 126, 134, 204, 226], [-150, -92, -86, -88, -96, -132, -136, -128])


def nao_hull(tod, liv, arms=None, bs=1.0):
    """Nao/karrak gövdesi (yerel: ileri → +x): yuvarlak karına, yüksek kıç kasarası (iki kat pencere), baş kasara, kuşaklar, top lumbozları, arma kalkanı, dümen, çıpa."""
    key = ("nao_hull", tod, liv["wale"], liv["hull"], liv["trim"], arms, round(bs, 2))
    if key in _SPR:
        return _SPR[key]
    T = Tint(tod)
    hull, wale, trim = T(liv["hull"]), T(liv["wale"]), T(liv["trim"])
    dk = T("#2A180C")
    ochre = T("#C79A3C")

    def draw(c):
        # dümen (gövdenin arkasında)
        rud = poly([(-208, -70), (-226, -62), (-240, 16), (-222, 16)])
        fink(c, rud, T("#5A3A20"), 1.2, 255, 190)
        # gövde
        body = skia.Path()
        body.moveTo(-176, 6)
        body.quadTo(-212, -8, -214, -62)
        body.quadTo(-218, -130, -206, -178)
        body.lineTo(-202, -198)
        body.lineTo(-92, -198)
        body.lineTo(-84, -152)
        body.lineTo(-40, -150)
        body.lineTo(-34, -92)
        body.cubicTo(10, -84, 90, -86, 126, -96)
        body.lineTo(134, -132)
        body.lineTo(204, -136)
        body.quadTo(226, -134, 229, -106)
        body.quadTo(229, -50, 206, -10)
        body.quadTo(188, 8, 150, 8)
        body.cubicTo(60, 12, -80, 12, -176, 6)
        body.close()
        sh = skia.GradientShader.MakeLinear([(0, -200), (0, 10)], [C(mix(hull, "#FFFFFF", 0.14)), C(hull), C(mix(hull, "#000000", 0.30))], [0.0, 0.55, 1.0])
        c.drawPath(body, skia.Paint(AntiAlias=True, Shader=sh))
        # kuşaklar (wales): bel boyunca iki geniş renkli şerit
        c.save()
        c.clipPath(body, skia.ClipOp.kIntersect, True)
        xs = np.linspace(-215, 230, 80)

        def sheer(x):
            return np.where(x < -92, -198.0, np.where(x < -40, -152.0, np.where(x < 126, _nao_top(x), -134.0)))
        # tahta çizgileri
        for off in (14, 28, 42, 56, 70, 84, 98, 112):
            pts = [(float(x), float(sheer(x) + off)) for x in xs]
            c.drawPath(poly(pts, False), _P("#1A0E06", 60, style="stroke", sw=1.0))
        # üst kuşak (koyu) + renkli kuşaklar
        for (o0, o1, col_, a_) in ((0, 12, dk, 255), (40, 54, wale, 255), (60, 66, ochre, 255), (86, 98, wale, 255)):
            up = poly([(float(x), float(sheer(x) + o0)) for x in xs] + [(float(x), float(sheer(x) + o1)) for x in xs[::-1]], True)
            c.drawPath(up, _P(col_, a_))
        # kıç kasarası panelleri + iki kat pencere
        for tier, wy in enumerate((-180, -146)):
            for i in range(4):
                wx = -184 + i * 24
                if wy == -146 and wx > -100:
                    continue
                ww = 15
                wp = skia.Path()
                wp.moveTo(wx - ww / 2, wy + 12)
                wp.lineTo(wx - ww / 2, wy)
                wp.arcTo(skia.Rect.MakeLTRB(wx - ww / 2, wy - ww / 2, wx + ww / 2, wy + ww / 2), 180, 180, False)
                wp.lineTo(wx + ww / 2, wy + 12)
                wp.close()
                c.drawPath(wp, _P(T("#1C1208")))
                c.drawPath(wp, _P(trim, 255, style="stroke", sw=2.0))
                if tod != "day":
                    c.drawPath(wp, _P("#FFC060", 200 if tod == "night" else 100))
        # top lumbozları (kapak açık: koyu kare + kapak)
        for gx in (-6, 28, 62, 96):
            c.drawRect(skia.Rect.MakeXYWH(gx, -64, 14, 12), _P("#0E0804", 235))
            c.drawRect(skia.Rect.MakeXYWH(gx, -64, 14, 12), _P(trim, 150, style="stroke", sw=1.0))
            c.drawRect(skia.Rect.MakeXYWH(gx, -78, 14, 9), _P(T("#5A3A20"), 255))
            c.drawRect(skia.Rect.MakeXYWH(gx, -78, 14, 9), _P(INK, 160, style="stroke", sw=0.9))
        for gx in (10, 52):
            c.drawRect(skia.Rect.MakeXYWH(gx, -36, 12, 10), _P("#0E0804", 235))
            c.drawRect(skia.Rect.MakeXYWH(gx, -36, 12, 10), _P(trim, 140, style="stroke", sw=0.9))
        wl = skia.GradientShader.MakeLinear([(0, -14), (0, 12)], [C("#1B2A1A", 0), C("#1B2A1A", 150)], [0.0, 1.0])
        c.drawRect(skia.Rect.MakeLTRB(-260, -14, 260, 14), skia.Paint(Shader=wl))
        # arma kalkanı (kıç kasarasının önünde, bel üstü)
        if arms:
            shp = skia.Path()
            shp.moveTo(-132, -178)
            shp.lineTo(-96, -178)
            shp.lineTo(-96, -152)
            shp.quadTo(-96, -134, -114, -126)
            shp.quadTo(-132, -134, -132, -152)
            shp.close()
            sc_ = {"medici": ("#E0B84E", "#B33620"), "cross": ("#F4EEDC", "#B33620"), "lily": ("#233C8C", "#E0B84E"), "crescent": ("#A8321E", "#E0B84E"), "palle": ("#E0B84E", "#B33620")}.get(arms, ("#F4EEDC", "#B33620"))
            fink(c, shp, T(sc_[0]), 1.4, 255, 220)
            draw_device(c, arms if arms != "medici" else "medici", -114, -156, 17, T(sc_[1]))
        _lit(c, body, 52, 46)
        c.drawPath(body, _P(INK, 215, style="stroke", sw=2.1))
        c.restore()
        # kıç volütü / korkuluk altın çizgisi / dekoratif frizi
        c.drawLine(-204, -196, -94, -196, _P(trim, 255, style="stroke", sw=3.0))
        for i in range(10):
            c.drawCircle(-196 + i * 11, -190, 2.0, _P(trim, 230))
        sc = skia.Path()
        sc.moveTo(-206, -178)
        sc.cubicTo(-232, -190, -244, -214, -232, -234)
        sc.cubicTo(-224, -246, -208, -240, -212, -226)
        c.drawPath(sc, _P(trim, 255, style="stroke", sw=5.0))
        c.drawPath(sc, _P(INK, 170, style="stroke", sw=1.2))
        # baş: kasara korkuluğu + çıpa + yaldız baş süsü
        c.drawLine(134, -138, 206, -142, _P(trim, 255, style="stroke", sw=3.0))
        anc = skia.Path()
        anc.moveTo(214, -86)
        anc.lineTo(214, -48)
        anc.moveTo(202, -52)
        anc.quadTo(214, -34, 226, -52)
        anc.moveTo(205, -80)
        anc.lineTo(223, -80)
        c.drawPath(anc, _P(INK, 230, style="stroke", sw=3.4))
        c.drawPath(anc, _P("#8A8E96", 255, style="stroke", sw=1.8))
        bsp = skia.Path()
        bsp.moveTo(229, -106)
        bsp.cubicTo(244, -116, 246, -134, 232, -144)
        c.drawPath(bsp, _P(trim, 255, style="stroke", sw=4.2))
        c.drawPath(bsp, _P(INK, 150, style="stroke", sw=1.0))
        # kıç feneri
        _mast(c, -200, -250, -198, 3.4, 3.6, T("#6A4A2C"))
        lp = poly([(-210, -280), (-190, -280), (-188, -252), (-212, -252)])
        fink(c, lp, T("#C79A3C"), 1.1, 255, 190)
        c.drawPath(poly([(-207, -276), (-193, -276), (-193, -256), (-207, -256)]), _P(T("#FFE9B0") if tod != "day" else T("#E8D6A0")))
        c.drawPath(poly([(-212, -280), (-200, -292), (-188, -280)]), _P(T("#8A6422")))
        c.drawPath(poly([(-212, -280), (-200, -292), (-188, -280)]), _P(INK, 180, style="stroke", sw=1.0))

    spr = bake_local((-262, -300, 262, 24), bs, draw)
    _spr_put(key, spr)
    return spr


NAO_MASTS = dict(main=(-14, -90, -434), fore=(104, -98, -352), miz=(-132, -152, -330))
NAO_YARDS = [  # (direk, y, yarım genişlik, adı)
    ("main", -238, 112, "course"), ("main", -328, 78, "top"), ("main", -398, 48, "gallant"),
    ("fore", -192, 84, "course"), ("fore", -284, 58, "top")]


def nao_rig(tod, liv, sails=True, bs=1.0):
    """Nao direkleri, kofa (mars), yardalar, bowsprit, babalar (shroud + ratline). sails=False → yardalarda sarılı yelken."""
    key = ("nao_rig", tod, bool(sails), liv["trim"], round(bs, 2))
    if key in _SPR:
        return _SPR[key]
    T = Tint(tod)
    mm = T("#6A4A2C")

    def draw(c):
        # bowsprit
        _yard(c, 196, -122, 334, -178, 8.0, T("#6A4A2C"))
        # direkler
        for nm, (mx, y0, y1) in NAO_MASTS.items():
            if nm == "miz":
                _mast(c, mx, y0, y1, 6.4, 3.4, mm)
            else:
                _mast(c, mx, y0, y1, 9.0 if nm == "main" else 7.4, 4.4, mm)
        # babalar: direk tepelerinden küpeşteye; ratline'lar
        def shrouds(mx, ytop, left, right, n=5):
            for k in range(n):
                f_ = k / max(1, n - 1)
                for side_x in (left, right):
                    xs_ = side_x + (f_ - 0.5) * 12
                    c.drawLine(mx, ytop + 18, xs_, float(_nao_top(xs_)), _P(INK, 150, style="stroke", sw=0.9))
            # ratline
            for k in range(1, 9):
                u = k / 9
                y_ = ytop + 18 + (float(_nao_top(left)) - (ytop + 18)) * u
                xl = mx + (left - mx) * u
                xr = mx + (right - mx) * u
                c.drawLine(xl, y_, xr, y_, _P(INK, 90, style="stroke", sw=0.8)) if False else None
                c.drawLine(xl, y_, xl + (xr - xl) * 0.0 + (-1 if False else 0) + 14 * (-1), y_ + 4, _P(INK, 0, style="stroke", sw=0.1)) if False else None
        shrouds(-14, -300, -62, 36, 5)
        shrouds(104, -230, 66, 144, 4)
        # mars (kofa) kasaları
        for (mx, my, w_) in ((-14, -312, 34), (104, -262, 28)):
            bowl = poly([(mx - w_ / 2, my), (mx + w_ / 2, my), (mx + w_ * 0.38, my + 15), (mx - w_ * 0.38, my + 15)])
            fink(c, bowl, T("#7A5A34"), 1.2, 255, 200)
            c.drawLine(mx - w_ / 2 - 2, my, mx + w_ / 2 + 2, my, _P(INK, 220, style="stroke", sw=2.2))
        # yardalar
        for (mn, yy, hw, nm) in NAO_YARDS:
            mx = NAO_MASTS[mn][0]
            _yard(c, mx - hw, yy, mx + hw, yy, 5.0 if nm == "course" else 4.2, T("#7A5A34"))
            if not sails:
                bw = 8 if nm == "course" else 6
                rl = poly([(mx - hw + 4, yy + 2), (mx + hw - 4, yy + 2), (mx + hw - 8, yy + 2 + bw), (mx - hw + 8, yy + 2 + bw)])
                fink(c, rl, T("#E4D8B8"), 1.0, 255, 170)
                for k in range(1, 9):
                    xk = mx - hw + 4 + (2 * hw - 8) * k / 9
                    c.drawLine(xk, yy + 1, xk, yy + 3 + bw, _P("#6A4A2C", 220, style="stroke", sw=1.6))
        # miz latin antenası
        _yard(c, -34, -152, -186, -306, 5.0, T("#7A5A34"))
        if not sails:
            a = math.atan2(-306 + 152, -186 + 34)
            nx, ny = -math.sin(a), math.cos(a)
            pts = []
            for i in range(0, 31):
                u = 0.05 + 0.9 * i / 30
                px_, py_ = -30 + (-170) * u, -152 + (-172) * u
                b_ = 5.0 + 2.0 * math.sin(u * 15)
                pts.append((px_ - nx * b_ * -1, py_ - ny * b_ * -1))
            pts2 = [(-30 + (-170) * (0.05 + 0.9 * i / 30), -152 + (-172) * (0.05 + 0.9 * i / 30)) for i in range(30, -1, -1)]
            fink(c, poly(pts + pts2, True), T("#E4D8B8"), 1.0, 255, 170)
        # forestay / backstay
        for (x1, y1, x2, y2) in ((-14, -430, 330, -178), (104, -350, 334, -178), (-14, -430, -204, -196), (104, -350, -14, -300)):
            c.drawLine(x1, y1, x2, y2, _P(INK, 130, style="stroke", sw=0.9))

    spr = bake_local((-262, -444, 346, -80), bs, draw)
    _spr_put(key, spr)
    return spr


NAO_CREW = [
    ("soylu", -150, -198, "idle", 56, {}),
    ("denizci", -122, -198, "idle", 50, {}),
    ("denizci", 12, -88, "work", 52, dict(mode="haul", period=1.6)),
    ("denizci", 44, -88, "work", 52, dict(mode="haul", period=1.6)),
    ("denizci", 76, -88, "idle", 52, {}),
    ("denizci", 168, -138, "point", 50, dict(t0=0.6, dur=3.0)),
]


def draw_nao(ctx, sea, S, t, x, y, s, dirn, sp, pitch):
    c = ctx.c
    liv = S.liv
    z = ctx.z
    bs = bucket(s * z)
    tod = ctx.tod
    T = Tint(tod)
    fl = getattr(ctx, "wind_dir", 1) * dirn
    flip = 1 if fl > 0 else -1
    wind = S.wind * getattr(ctx, "wind", 1.0)
    sails_on = bool(S.sails)
    roll = math.sin(t * 0.55 + S.seed) * 1.1 * S.tilt
    c.save()
    c.translate(x, y)
    c.rotate(pitch)
    c.scale(dirn * s, s)
    c.save()
    c.rotate(roll * 0.5 * dirn)                                                   # direkler gövdeden biraz fazla yalpalar
    nao_rig(tod, liv, sails_on, bs).draw(c)
    c.restore()
    if S.crew and s * z * NAO_L > 200:
        draw_crew(ctx, S, NAO_CREW, t, s, dirn)
    nao_hull(tod, liv, S.arms, bs).draw(c)
    if sails_on:
        sl = liv["sail"]
        col, trim, dev, devc = T(sl[0]), T(sl[1]), sl[2], T(sl[3])
        st = S.sails if isinstance(S.sails, str) else "full"
        sway = math.sin(t * 0.9 + S.seed) * 3.0 * min(1.0, wind)
        sset = S.sail_set(t) if callable(S.sail_set) else (1.0 if S.sail_set is None else float(S.sail_set))
        c.save()
        c.rotate(roll * 0.5 * dirn)
        # ana: course / topsail / gallant
        if st in ("full", "reduced"):
            square_sail(c, -14, -238, -132, 196, 236, t, wind, ph=S.seed * 0.7, col=col, trim=trim, dev=dev, devcol=devc, seed=S.seed, sway=sway, set_=max(0.12, sset))
            square_sail(c, -14, -328, -242, 140, 160, t, wind, ph=S.seed * 0.9 + 1.0, col=col, trim=trim, dev=None, devcol=devc, seed=S.seed + 1, sway=sway * 0.7, set_=max(0.12, sset))
            if st == "full":
                square_sail(c, -14, -398, -332, 88, 98, t, wind, ph=S.seed * 1.1 + 2.0, col=col, trim=trim, dev=None, devcol=devc, seed=S.seed + 2, sway=sway * 0.5, set_=max(0.12, sset))
            square_sail(c, 104, -192, -112, 150, 176, t, wind, ph=S.seed * 1.3 + 0.5, col=col, trim=trim, dev=dev, devcol=devc, seed=S.seed + 3, sway=sway, set_=max(0.12, sset))
            square_sail(c, 104, -284, -200, 112, 124, t, wind, ph=S.seed * 1.5 + 1.5, col=col, trim=trim, dev=None, devcol=devc, seed=S.seed + 4, sway=sway * 0.7, set_=max(0.12, sset))
        lateen_sail(c, (-34, -152), (-186, -306), (-178, -172), t, wind, ph=S.seed * 0.5 + 3.0, col=col, trim=trim, dev=None, devcol=devc, seed=S.seed + 5)
        c.restore()
    # bayraklar
    pc1, pc2, pdev = liv["pen"]
    if S.highlight:
        pc1, pc2, pdev = "#E0B84E", "#B33620", None
    flag(c, -14, -438, 230, 36, t, "pennant", pdev or "plain", pc1, pc2, pc2, wind=wind, ph=S.seed * 1.3, flipx=flip)
    flag(c, 104, -356, 150, 28, t, "pennant", "plain", pc1, pc2, pc2, wind=wind, ph=S.seed * 2.1, flipx=flip)
    flag(c, -186, -310, 130, 24, t, "pennant", "plain", pc1, pc2, pc2, wind=wind, ph=S.seed * 3.1, flipx=flip)
    fg = liv["flag"]
    flag(c, 332, -176, 62, 38, t, fg[0], fg[1], fg[2], fg[3], fg[4], wind=wind, ph=S.seed * 0.4, flipx=flip)
    if S.ensign:
        c.drawLine(-196, -198, -196, -318, _P(INK, 200, style="stroke", sw=4.8))
        c.drawLine(-196, -198, -196, -318, _P(T("#8A6A3C"), 255, style="stroke", sw=3.0))
        c.drawCircle(-196, -320, 4.0, _P(T(liv["trim"])))
        flag(c, -196, -316, 120, 70, t, fg[0], fg[1], fg[2], fg[3], fg[4], wind=wind, ph=S.seed * 0.9, flipx=flip)
    if S.highlight:
        glow(c, -14 + flip * 90, -420, 100, "#FFE08A", 0.35 + 0.1 * math.sin(t * 3.0))
    if tod in ("night", "dusk", "fire"):
        fk = 0.8 + 0.2 * math.sin(t * 9.0 + S.seed) + 0.06 * math.sin(t * 23.0)
        glow(c, -200, -266, 86 * fk, "#FFC060", (0.62 if tod == "night" else 0.34) * fk)
        glow(c, -146, -170, 46 * fk, "#FFB04A", 0.40 * fk) if tod == "night" else None
    c.restore()
    return None


KIND_DRAW["nao"] = draw_nao


# ═════════════════════════════ SAHNE ÇATISI (kare, kamera, katman sırası) ═════════════════════════════
import cilt_pano as PN                        # PanoCam (anahtar kareli kamera) ve çerçeve yardımcıları

# kendi kamera yolu olan türler (pano/build gibi): cam= alanı kabul edilir, burada `cams=`/`cam=` kendimiz çözülür (cilt_cam.OWN_CAMERA çalışma anı kaydı)
OWN_KINDS = ("deniz", "deniz_rota", "deniz_filo", "deniz_kiyi", "liman")
try:
    CAM.OWN_CAMERA.update(OWN_KINDS)
except Exception:
    pass


def _cam_for(cx, cams, default, kind):
    """(camx, camy, z): cams= anahtar kareleri > cam= ön ayarı > varsayılan (kesir, (x,y,zoom)) yolu."""
    dur = max(cx.dur, 1e-3)
    if cams:
        pc = PN.PanoCam(cx, cams, default, dur)
        return pc.at(clamp(cx.t, 0.0, dur))
    spec = getattr(cx, "cam_spec", None)
    if spec is not None:
        try:
            st = CAM.state(cx, spec, kind=kind)
            if st is not None:
                return W / 2 + st.x, st.y, max(0.5, st.zoom)
        except Exception:
            pass
    pc = PN.PanoCam(cx, None, default, dur)
    return pc.at(clamp(cx.t, 0.0, dur))


def _wall(f, cx, seed, band):
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    mb0, mbh = band
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, 0, W, mb0 + 2))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    c.restore()
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, mb0 + mbh - 2, W, H))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    c.restore()


def _frame_decor(f, cx, band, a, kick, caption, at, extra=None):
    c = f.c
    by0, bh = band
    for yy in (by0 - 40, by0 + bh):
        FA.vine_band(f, yy, a)
        c.drawLine(-40, yy + (40 if yy < by0 else 0), W + 40, yy + (40 if yy < by0 else 0), f.paint(TH.gold, style="stroke", sw=2.6, alpha=0.9 * a))
    if kick:
        CM.kick(f, kick, W / 2, 104, alpha=cx.amt(at + 0.4, 0.8), size=34, track=14)
    if caption:
        wd = sk.text_width(caption, "cap_i", 44) + 100
        cyy = by0 + bh - 70
        CM.tablet(f, W / 2 - wd / 2, cyy - 36, wd, 76, alpha=cx.amt(at + 0.8, 0.7), corner=10)
        CM.ink(f, caption, W / 2, cyy + 14, face="cap_i", size=44, color=TH.fg, align="c", alpha=cx.amt(at + 0.8, 0.7), emboss=False)
    if extra:
        extra(f, cx, band)


def _finish(f, cx, tod, seed, motes=24):
    if tod == "night":
        CM.finish(f, cx, motes_n=max(12, motes - 4), light=CM.candle_light(cx.t, seed, base=(W * 0.5, H * 0.46), r=1500.0, sway=12.0))
    else:
        CM.finish(f, cx, motes_n=motes)


def _label_plate(f, cx, text, x, y, at, size=34, anchor_x=None, anchor_y=None, a=1.0):
    """Ad levhası (yalnız parametreyle gelen metin): iğneli kılavuz çizgi + levha."""
    k = cx.amt(at, 0.7) * a
    if k <= 0.001 or not text:
        return
    c = f.c
    wd = sk.text_width(text, "cap_b", size) + 60
    px_ = clamp(x, 90 + wd / 2, W - 90 - wd / 2)
    if anchor_x is not None:
        ex, ey = px_, y + 30
        c.drawLine(anchor_x, anchor_y, ex, ey, f.paint(TH.fg, style="stroke", sw=2.0, alpha=0.75 * k))
        c.drawCircle(anchor_x, anchor_y, 5.5, f.paint(TH.acc, alpha=k))
        c.drawCircle(anchor_x, anchor_y, 5.5, f.paint(TH.fg, style="stroke", sw=1.2, alpha=0.8 * k))
    CM.tablet(f, px_ - wd / 2, y - 32 + (1 - k) * 8, wd, 64, alpha=k, corner=8)
    CM.ink(f, text, px_, y + 12 + (1 - k) * 8, face="cap_b", size=size, color=TH.fg, align="c", alpha=k, emboss=False)


# ═════════════════════════════ ÖN PLAN DALGALARI + SAHNE ÇİZİMİ ═════════════════════════════
def draw_fore(ctx, sea, t, ys=(772.0,), amp=1.0):
    """Ön plandaki iri dalgalar (f > 1: kamera kaymasında hızlı paralaks; derinlik hissi). ys: su hattı y'leri (bant yerel)."""
    P = sea.P
    for i, y0 in enumerate(ys):
        f_ = 1.28 + 0.34 * i
        ctx.push(f_)
        c = ctx.c
        xa, xb = ctx.view(f_, 60)
        xs = np.arange(xa - 40, xb + 40, 14.0)
        lam = 560.0 + 160 * i
        k1 = TAU / lam
        v = (60.0 + 20 * i) * sea.wdir * sea.speed
        A = (15.0 + 5 * i) * sea.swell * amp
        ph = 1.7 + 2.3 * i
        ys_ = y0 + -A * (0.64 * np.sin(k1 * xs - k1 * v * t + ph) + 0.26 * np.sin(2.1 * k1 * xs - 2.1 * k1 * v * 1.08 * t + ph * 1.7) + 0.10 * np.sin(3.3 * k1 * xs - 3.3 * k1 * v * 0.9 * t))
        pl = skia.Path.Polygon([(float(a), float(b)) for a, b in zip(xs, ys_)], False)
        body = skia.Path(pl)
        body.lineTo(float(xs[-1]), y0 + 300)
        body.lineTo(float(xs[0]), y0 + 300)
        body.close()
        col = mix(P["sea"][-1], "#08142A", 0.28 + 0.10 * i)
        c.drawPath(body, _P(col))
        c.save()
        c.translate(0, 3.0)
        c.drawPath(pl, _P(P["crest"], 120, style="stroke", sw=7.0, cap=skia.Paint.kButt_Cap))
        c.restore()
        c.drawPath(pl, _P(P["ink"], 130, style="stroke", sw=2.0))
        # köpük başlıkları
        m0 = int(math.floor((k1 * xa - k1 * v * t + ph - math.pi / 2) / TAU)) - 1
        m1 = int(math.ceil((k1 * xb - k1 * v * t + ph - math.pi / 2) / TAU)) + 1
        for m in range(m0, m1 + 1):
            xm = (math.pi / 2 + TAU * m + k1 * v * t - ph) / k1
            h = hash01(m, 91 + i)
            if h < 0.78:
                ym = y0 - A * (0.64 + 0.26 * math.sin(2.1 * k1 * xm - 2.1 * k1 * v * 1.08 * t + ph * 1.7) + 0.10 * math.sin(3.3 * k1 * xm - 3.3 * k1 * v * 0.9 * t))
                w_ = 30 + 40 * h
                p = skia.Path()
                p.moveTo(xm - w_, ym + 3)
                p.quadTo(xm - w_ * 0.3, ym - 10, xm + w_ * 0.2, ym - 8)
                p.quadTo(xm + w_ * 0.8, ym - 4, xm + w_, ym + 3)
                p.quadTo(xm, ym + 1, xm - w_, ym + 3)
                c.drawPath(p, _P(P["foam"], int(255 * 0.75)))
                c.drawPath(p, _P(P["ink"], 70, style="stroke", sw=1.0))
        ctx.pop()


_SEAS = {}


def get_sea(tod, yh, seed, swell, foam, wdir, speed=1.0):
    key = (tod, round(yh, 1), seed, round(swell, 2), round(foam, 2), wdir, round(speed, 2))
    s = _SEAS.get(key)
    if s is None:
        s = _SEAS[key] = Sea(tod, yh, seed=seed, swell=swell, foam=foam, wdir=wdir, speed=speed)
    return s


def default_sun(tod):
    return {"day": (1420, 190, 44), "dusk": (1180, 322, 74), "night": (500, 175, 40), "fire": (760, 318, 80)}.get(tod, (1420, 190, 44))


def draw_sky_stack(ctx, cfg, sea):
    """Gökyüzü katmanları: gökyüzü görüntüsü → yıldız → güneş/ay → bulut. Dönüş: güneşin ekran x'i (parıltı yolu için) ya da None."""
    tod, yh = ctx.tod, sea.yh
    c = ctx.c
    ctx.push(0.04)
    im = sky_image(tod, int(yh), cfg.get("seed", 1))
    blit_baked(c, im, -240, -OV, SKY_W, yh + 300 + OV)
    ctx.pop()
    if tod == "night":
        draw_stars(ctx, 46, cfg.get("seed", 1) + 2)
    sun = cfg.get("sun")
    sun_sx = None
    if sun is not False:
        sx, sy, r = sun if sun else default_sun(tod)
        draw_sun(ctx, sx, sy, r, rays=cfg.get("rays", True))
        sun_sx = ctx.to_screen(0.04, sx, sy)[0]
    nc = cfg.get("clouds", 8)
    if nc:
        draw_clouds(ctx, nc, seed=cfg.get("seed", 1) + 11, wind=cfg.get("wind", 1.0) * cfg.get("wind_dir", -1), y_rng=cfg.get("cloud_y", (60, max(120, yh - 90))))
    return sun_sx


def render_sea_scene(cx, f, cfg, ships, band=BAND, cams=None, default_cam=None, kind="deniz", pre=None, post=None, mid=None, cam_override=None, ship_fn=None):
    """Açık deniz çekirdeği: duvar → bant [gök → (pre) → deniz+gemiler (mid) → ön dalgalar → (post) → kuşlar] → çerçeve → metin → ışık.
    pre(ctx, sea): denizden ÖNCE (ör. uzak kara, kale); mid(ctx, sea, k): k. sıra çizilmeden önce ekstra nesneler; post(ctx, sea): sudan sonra."""
    tod = cfg["tod"]
    yh = cfg.get("horizon", 330.0)
    sea = get_sea(tod, yh, cfg.get("seed", 1), cfg.get("swell", 1.0), cfg.get("foam", 0.55), cfg.get("wind_dir", -1), cfg.get("wspeed", 1.0))
    dur = max(cx.dur, 1e-3)
    camx, camy, z = cam_override if cam_override else _cam_for(cx, cams, default_cam, kind)
    _wall(f, cx, cfg.get("seed", 1), band)
    ctx = Ctx(f, cx, camx, camy, z, band, tod, cx.amt(cfg.get("at", 0.0), 0.9) if cfg.get("at") else 1.0)
    ctx.wind = cfg.get("wind", 1.0)
    ctx.wind_dir = cfg.get("wind_dir", -1)
    c = f.c
    by0, bh = band
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, by0, W, by0 + bh))
    t = cx.t
    sun_sx = draw_sky_stack(ctx, cfg, sea)
    if pre:
        pre(ctx, sea)
    # gemiler: su hattına göre satır eşlemesi
    ordered = sorted(ships, key=lambda S: S.pos(t)[1])
    by_row = {}
    for S in ordered:
        k = sea.row_before(S.pos(t)[1])
        by_row.setdefault(k, []).append(S)

    def cb(k):
        if mid:
            mid(ctx, sea, k)
        for S in by_row.get(k, ()):
            (ship_fn or render_ship)(ctx, sea, S, t)
    draw_sea(ctx, sea, t, cb, sun_sx, cfg.get("glitter", 0.9 if tod in ("day", "dusk", "night", "fire") else 0.0))
    if cfg.get("fore", True):
        draw_fore(ctx, sea, t, cfg.get("fore_y", (782.0,)), amp=cfg.get("fore_amp", 1.0))
    if post:
        post(ctx, sea)
    nb = cfg.get("birds", 5)
    if nb:
        gulls(ctx, max(2, nb // 2), seed=cfg.get("seed", 1) + 3, fct=0.35, y_rng=(70, 250), size=(0.7, 1.1), wind=cfg.get("wind", 1.0))
        gulls(ctx, nb - max(2, nb // 2), seed=cfg.get("seed", 1) + 5, fct=0.9, y_rng=(110, 330), size=(1.2, 2.0), wind=cfg.get("wind", 1.0))
    c.restore()
    return ctx, sea


# ═════════════════════════════ UZAK KARA SİLUETLERİ (ada, burun, kasaba, kale) ═════════════════════════════
import cilt_city as CT                                    # ev/kule/kubbe çizicileri (aynı fresk dili)
import cilt_scene as SC                                   # servi, kale parçaları


def _ridge_pts(x0, x1, base, amp, scale, ph, step=8):
    xs = np.arange(x0, x1 + step, step)
    ys = base + amp * (0.6 * np.sin(xs / scale + ph) + 0.4 * np.sin(xs / (scale * 0.37) + ph * 1.7) + 0.2 * np.sin(xs / (scale * 0.13) + ph * 2.3)) / 1.2
    return xs, ys


@functools.lru_cache(maxsize=64)
def land_sprite(kind, w, h, tod, seed=1, depth=0.5):
    """Kara siluet sprite'ı (w×h px; alt kenar su hattı). kind: island | headland | town | castle | hills. depth: hava perspektifi (0 ön … 1 uzak). Dönüş: skia.Image."""
    T = Tint(tod)
    P = pal(tod)
    rs = _RS(seed * 17 + 3)
    fr = sk.Frame(int(w), int(h))
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    base = h - 2
    for li, (col, amp, sc_, dy) in enumerate(((P["land"][0], 0.36, 0.30, 0.0), (P["land"][1], 0.30, 0.20, 0.10), (P["land"][2], 0.22, 0.13, 0.20))):
        cc = T(col, depth * 0.5)
        if kind == "island":
            xs = np.linspace(0, w, 60)
            prof = np.sin(np.pi * xs / w) ** 0.8
            ys = base - (h * (0.26 + 0.74 * (1 - dy)) * amp * 1.9) * prof * (1 + 0.15 * np.sin(xs / 37 + li + seed))
        elif kind == "headland":
            xs = np.linspace(0, w, 60)
            prof = (1 - xs / w) ** 0.7 * np.clip(xs / (w * 0.06), 0, 1)
            ys = base - (h * (0.34 + 0.46 * (1 - dy))) * prof * (0.9 + 0.1 * np.sin(xs / 41 + li)) * amp * 2.4
        else:
            xs, ys = _ridge_pts(0, w, base - h * (0.18 + 0.10 * (1 - dy)), h * amp * 1.05, w * sc_ * 0.5, seed + li * 2.0, 10)
            env = np.sin(np.pi * np.clip(xs / w, 0, 1)) ** 0.55
            ys = base - (base - ys) * env
            ys = np.minimum(ys, base - 3)
        pts = list(zip(xs.tolist(), ys.tolist())) + [(float(xs[-1]), h), (float(xs[0]), h)]
        c.drawPath(poly(pts, True), _P(cc))
        c.drawPath(poly(list(zip(xs.tolist(), ys.tolist())), False), _P(T(P["ink"], 0.0), 70, style="stroke", sw=1.2))
        if li == 2:
            # servi ağaçları / çalılık
            for k in range(int(w / 60)):
                x = rs.uniform(10, w - 10)
                yy = float(np.interp(x, xs, ys))
                if rs.rand() < 0.65 and kind != "town":
                    SC.cypress(c, x, yy + 2, rs.uniform(22, 44) * (0.5 + h / 260.0), T("#2E4A33", depth * 0.4), T("#4F6E4A", depth * 0.4))
    if kind in ("town", "castle"):
        wins = []
        ycur = base - h * 0.28
        x = 12
        while x < w - 40:
            bw, bh = rs.uniform(26, 52), rs.uniform(22, 46)
            CT.draw_house(c, x, ycur + rs.uniform(-4, 4) - (bh * 0.0), bw, bh, rs, T, depth * 0.6, wins)
            x += bw + rs.uniform(-3, 5)
        if kind == "castle":
            cx_ = w * 0.58
            SC.castle(c, cx_, base - h * 0.30, h * 0.52, T("#E6D9B8", depth * 0.5), T("#B4552E", depth * 0.5))
        if tod == "night":
            for (wx, wy, ww, wh) in wins[::2]:
                c.drawRect(skia.Rect.MakeXYWH(wx, wy, ww, wh), _P("#FFD27A", 230))
    return fr.surf.makeImageSnapshot()


def draw_coast(ctx, items, t=0.0):
    """Uzak kara katmanı. items: [dict(x, kind, w, h, f, y, seed)] — x/y katman koordinatı (y = alt kenar = su hattı; bant yerel). f: paralaks çarpanı (0,08–0,6)."""
    c = ctx.c
    for it in sorted(items, key=lambda d: d.get("f", 0.1)):
        f_ = it.get("f", 0.12)
        w, h = it.get("w", 700), it.get("h", 120)
        depth = clamp(1.0 - f_ * 1.3, 0.0, 1.0)
        im = land_sprite(it.get("kind", "island"), int(w), int(h), ctx.tod, it.get("seed", 1), round(depth, 1))
        x, y = it["x"], it.get("y", 332.0)
        ctx.push(f_)
        if ctx.visible(f_, x, x + w, 20):
            c.drawImageRect(im, skia.Rect.MakeWH(im.width(), im.height()), skia.Rect.MakeXYWH(x, y - h, w, h), LIN, skia.Paint())
        ctx.pop()


def default_coast(yh, xr=(0, 3000), seed=3):
    rs = _RS(seed * 7 + 1)
    out = []
    x = xr[0] - 300
    kinds = ["island", "headland", "hills", "island"]
    while x < xr[1] + 600:
        w = rs.uniform(520, 1100)
        out.append(dict(x=x, kind=kinds[rs.randint(len(kinds))], w=w, h=rs.uniform(60, 130), f=rs.uniform(0.07, 0.13), y=yh + 2, seed=int(rs.randint(1, 99))))
        x += w * rs.uniform(0.7, 1.5) + rs.uniform(200, 900)
    return out


# ═════════════════════════════ ÇEKİM TÜRÜ: deniz ═════════════════════════════
def _norm_ships(cx, ships, dur):
    out = []
    for i, d in enumerate(ships or []):
        out.append(d if isinstance(d, ShipSpec) else ShipSpec(d, cx, dur, i))
    return out


def _default_tod(tod):
    return tod or ("night" if not TH.day else "day")


def _scene_cfg(scene, tod, kw):
    cfg = dict(tod=tod, seed=kw.get("seed", 1), wind=kw.get("wind", 1.0), wind_dir=kw.get("wind_dir", -1), swell=kw.get("swell", 1.0), foam=kw.get("foam", 0.55),
               horizon=kw.get("horizon", 330.0), sun=kw.get("sun"), glitter=kw.get("glitter", 0.9), birds=kw.get("birds", 5), clouds=kw.get("clouds", 8), rays=kw.get("rays", True),
               fore=kw.get("fore", True), at=kw.get("at", 0.0), wspeed=kw.get("wspeed", 1.0), fore_y=kw.get("fore_y", (782.0,)))
    return cfg


def _follow_cam(cx, S, sea, z=1.0, lead=170.0, camy_k=0.25):
    """Gemiyi izleyen kamera: gemi ekranda merkezin (ilerleme yönünün gerisinde) sabit durur; paralaks katmanlar kayar. Dönüş: (camx, camy, z)."""
    t = clamp(cx.t, -2.0, cx.dur + 2.0)
    x, y, d, sp = S.pos(t)
    xa, ya, _, _ = S.pos(t - 0.5)
    xb, yb, _, _ = S.pos(t + 0.5)
    vx = xb - xa
    lead_k = math.tanh(vx / 40.0)
    f = clamp(persp(y, sea.yh), 0.1, 1.7) if True else 1.0
    target = W / 2 - lead_k * lead
    Cx = x - (target - W / 2) / z
    camx = W / 2 + (Cx - W / 2) / max(0.1, sea.row_of(y).f)
    camy = (y - 640.0) * camy_k
    return camx, camy, z


def _deniz(cx, scene="acik", tod=None, ships=None, cams=None, kick=None, caption=None, at=0.0, frame=True, seed=1, band=None, labels=None, route=None, thread=False,
           coast=None, zoom=1.0, follow=True, n=None, **kw):
    """Deniz çekimi (bkz. notlar_deniz.md). scene: acik | rota | filo | kiyi (ya da deniz_rota / deniz_filo / deniz_kiyi türleri).
    Ortak: tod (day|dusk|night|fire), ships=[dict(kind, x0, x1 | dir+speed, y, scale, flag, t0, t1, sails, oars, crew, highlight, route…)], cams=[(çapa,(x,y,zoom)),…] | cam= ön ayarı,
    wind (şiddet), wind_dir (−1 sola, +1 sağa; bayrak/yelken/bulut/dalga yönü), swell, foam, horizon (ufuk y), sun=(x,y,r)|False, glitter, birds, clouds, coast=[…], kick, caption, labels=[…]."""
    f = cx.f
    dur = max(cx.dur, 1e-3)
    tod = _default_tod(tod)
    band = band or (BAND if frame else (0, 800))
    kw = dict(kw)
    kw.update(seed=seed, at=at)
    if scene == "filo":
        return _scene_filo(cx, f, tod, kw, cams, kick, caption, at, band, labels, n, ships)
    if scene == "kiyi":
        return _scene_kiyi(cx, f, tod, kw, cams, kick, caption, at, band, labels, ships)
    cfg = _scene_cfg(scene, tod, kw)
    yh = cfg["horizon"]
    if scene == "rota":
        d0 = dict(kind=kw.pop("ship_kind", "nao"), flag=kw.pop("flag", "hristiyan"), route=route or [(300, 650), (1500, 620), (2700, 660)], t0=kw.pop("t0", 0.0), t1=kw.pop("t1", dur), scale=kw.pop("scale", 0.8), ease=kw.pop("ease", "io"), sails=True)
        ship_list = _norm_ships(cx, ships if ships else [d0], dur)
        r0 = ship_list[0].route or [(300, 650), (2700, 660)]
        xr = (min(p[0] for p in r0), max(p[0] for p in r0))
        co = coast if coast is not None else (default_coast(yh, (xr[0] - 400, xr[1] + 400), seed) + [
            dict(x=xr[0] - 900, kind="town", w=1000, h=150, f=0.40, y=yh + 40, seed=2), dict(x=xr[1] + 500, kind="castle", w=1000, h=170, f=0.40, y=yh + 40, seed=5)])
        cfg["birds"] = kw.get("birds", 6)
        S0 = ship_list[0]
        sea0 = get_sea(tod, yh, cfg["seed"], cfg["swell"], cfg["foam"], cfg["wind_dir"], cfg["wspeed"])
        if cams is None and follow:
            default = None
            camf = lambda: _follow_cam(cx, S0, sea0, zoom)
        else:
            default = [(0.0, (960, 0, zoom)), (1.0, (1100, -6, zoom * 1.08))]
            camf = None
    else:
        d0 = dict(kind="kadirga", flag="hristiyan", x0=260, x1=1600, y=650, scale=1.0, t0=0.0, t1=dur, ease="lin")
        ship_list = _norm_ships(cx, ships if ships else [d0], dur)
        co = coast if coast is not None else []
        default = [(0.0, (820, 18, 1.0)), (0.55, (940, 4, 1.07)), (1.0, (1080, -12, 1.17))]
        camf = None
    pre = (lambda ctx, sea: draw_coast(ctx, co, ctx.t)) if co else None
    cam_override = camf() if camf is not None else None
    post = None
    if scene == "rota" and thread:
        post = lambda ctx, sea_: draw_route_thread(ctx, sea_, ship_list[0], ctx.t, thread if isinstance(thread, dict) else {})
    ctx, sea = render_sea_scene(cx, f, cfg, ship_list, band, cams, default, "deniz", pre=pre, post=post, cam_override=cam_override)
    _deco_labels(f, cx, ctx, sea, labels, at)
    _frame_decor(f, cx, band, 1.0, kick, caption, at)
    _finish(f, cx, tod, seed)


def _deco_labels(f, cx, ctx, sea, labels, at):
    for lb in (labels or []):
        x, y = lb.get("at_xy", (960, 300))
        k = lb.get("f", 0.4)
        sx, sy = ctx.to_screen(k, x, y)
        _label_plate(f, cx, lb["name"], sx + lb.get("dx", 0), sy + lb.get("dy", -120) + ctx.band[0] * 0, _tcall(cx, lb.get("t", 0.0), 0.0), lb.get("size", 34), sx, sy)


@ckind("deniz")
def k_deniz(cx, scene="acik", **kw):
    return _deniz(cx, scene=scene, **kw)


@ckind("deniz_rota")
def k_deniz_rota(cx, **kw):
    kw.pop("scene", None)
    return _deniz(cx, scene="rota", **kw)


@ckind("deniz_filo")
def k_deniz_filo(cx, **kw):
    kw.pop("scene", None)
    return _deniz(cx, scene="filo", **kw)


@ckind("deniz_kiyi")
def k_deniz_kiyi(cx, **kw):
    kw.pop("scene", None)
    return _deniz(cx, scene="kiyi", **kw)




# ═════════════════════════════ KIYI: Otranto (kale-kent silueti, stilize alev + duman) ═════════════════════════════
HILL_W, HILL_H = 1560, 450


def _prof_fn():
    pts = [(0, 30), (70, -14), (240, -130), (440, -246), (600, -312), (740, -338), (880, -304), (1060, -214), (1260, -122), (1450, -54), (1560, -30)]
    return PN.pchip([p[0] for p in pts], [p[1] for p in pts])


_HILLS = {}


def otranto_hill(tod):
    """Kıyı kasabası: tepede kale (yuvarlak kuleler) + katedral + sur + kat kat evler. Dönüş: (Image, bilgi{roofs, base}). Sprite koordinatı: sol-üst (0,0); alt kenar kıyı."""
    if tod in _HILLS:
        return _HILLS[tod]
    T = Tint(tod)
    P = pal(tod)
    prof = _prof_fn()
    base = HILL_H - 8
    fr = sk.Frame(HILL_W, HILL_H)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    rs = _RS(1480)
    roofs = []
    # kaya yüzü
    xs = np.arange(0, HILL_W + 1, 8)
    ys = np.array([base + prof(x) for x in xs])
    rock = poly(list(zip(xs.tolist(), ys.tolist())) + [(HILL_W, HILL_H), (0, HILL_H)], True)
    sh = skia.GradientShader.MakeLinear([(0, 40), (0, HILL_H)], [C(T("#C9B286")), C(T("#A58A62")), C(T("#6E5A44"))], [0.0, 0.55, 1.0])
    c.drawPath(rock, skia.Paint(AntiAlias=True, Shader=sh))
    c.save()
    c.clipPath(rock, skia.ClipOp.kIntersect, True)
    for i in range(46):
        x = rs.uniform(0, HILL_W)
        y = base + prof(x) + rs.uniform(20, 300)
        c.drawLine(x, y, x + rs.uniform(40, 130), y + rs.uniform(-6, 4), _P("#3A2A1C", 40, style="stroke", sw=1.3))
    c.restore()
    c.drawPath(poly(list(zip(xs.tolist(), ys.tolist())), False), _P(INK, 150, style="stroke", sw=1.6))
    # evler: kat kat teraslar (üstten alta; alttakiler önde)
    wins = []
    for r in range(6):
        x = 28 + rs.uniform(0, 30)
        while x < HILL_W - 60:
            bw, bh = rs.uniform(32, 58), rs.uniform(26, 46)
            yb = base + prof(x + bw / 2) + 16 + r * 36
            if yb < base + 4 and yb - bh > base + prof(x + bw / 2) - 60:
                hip = rs.rand() < 0.55
                rec = []
                CT.draw_house(c, x, yb, bw, bh, rs, T, 0.05, wins, hip=hip, rec=rec)
                roofs.append((x + bw / 2, yb - bh - 6))
            x += bw + rs.uniform(-2, 7)
    # sur: eğime paralel, mazgallı; yuvarlak kuleler
    wall_pts = [(float(x), float(base + prof(x) + 6)) for x in range(110, 1480, 10)]
    for (wx, wy) in wall_pts:
        c.drawRect(skia.Rect.MakeLTRB(wx - 5, wy - 20, wx + 5, wy + 2), _P(T("#D7C6A0")))
    c.drawPath(poly([(p[0], p[1] - 20) for p in wall_pts], False), _P(INK, 140, style="stroke", sw=1.2))
    for (wx, wy) in wall_pts[::2]:
        c.drawRect(skia.Rect.MakeLTRB(wx - 3, wy - 27, wx + 3, wy - 20), _P(T("#D7C6A0")))
    for tx in (190, 520, 880, 1180, 1420):
        ty = base + prof(tx) + 6
        c.drawRect(skia.Rect.MakeLTRB(tx - 17, ty - 64, tx + 17, ty + 4), _P(T("#CDBB92")))
        c.drawRect(skia.Rect.MakeLTRB(tx - 17, ty - 64, tx + 17, ty + 4), _P(INK, 160, style="stroke", sw=1.2))
        for k in range(4):
            c.drawRect(skia.Rect.MakeLTRB(tx - 19 + k * 12.5, ty - 74, tx - 19 + k * 12.5 + 7, ty - 64), _P(T("#CDBB92")))
        c.drawRect(skia.Rect.MakeLTRB(tx - 3, ty - 44, tx + 3, ty - 30), _P(T("#2A1C10")))
    # kale (denize bakan uçta): iki yuvarlak kule + kütle + alan
    kx = 150
    ky = base + prof(kx) + 14
    c.drawRect(skia.Rect.MakeLTRB(kx - 70, ky - 118, kx + 120, ky), _P(T("#D9C79E")))
    for k in range(10):
        c.drawRect(skia.Rect.MakeLTRB(kx - 70 + k * 19, ky - 130, kx - 70 + k * 19 + 11, ky - 118), _P(T("#D9C79E")))
    c.drawRect(skia.Rect.MakeLTRB(kx - 70, ky - 118, kx + 120, ky), _P(INK, 170, style="stroke", sw=1.6))
    for (tx, th, tr) in ((kx - 72, 168, 40), (kx + 124, 150, 36)):
        c.drawRect(skia.Rect.MakeLTRB(tx - tr, ky - th, tx + tr, ky), _P(T("#CDB98E")))
        c.drawRect(skia.Rect.MakeLTRB(tx - tr, ky - th, tx + tr, ky), _P(INK, 180, style="stroke", sw=1.6))
        c.drawRect(skia.Rect.MakeLTRB(tx + tr * 0.35, ky - th, tx + tr, ky), _P("#2A1A0C", 40))
        for k in range(5):
            c.drawRect(skia.Rect.MakeLTRB(tx - tr + k * tr * 0.44, ky - th - 12, tx - tr + k * tr * 0.44 + tr * 0.26, ky - th), _P(T("#CDB98E")))
        c.drawRect(skia.Rect.MakeLTRB(tx - 4, ky - th + 28, tx + 4, ky - th + 52), _P(T("#2A1C10")))
        roofs.append((tx, ky - th - 14))
    c.drawRect(skia.Rect.MakeLTRB(kx + 8, ky - 162, kx + 52, ky - 118), _P(T("#D2BE94")))
    c.drawRect(skia.Rect.MakeLTRB(kx + 8, ky - 162, kx + 52, ky - 118), _P(INK, 160, style="stroke", sw=1.3))
    # katedral (zirveye yakın): uzun nef + beşik çatı + gül pencere kabartması + küçük çan alınlığı
    cxm, cym = 740, base + prof(740) + 22
    c.drawRect(skia.Rect.MakeLTRB(cxm - 120, cym - 78, cxm + 120, cym), _P(T("#E4D5AE")))
    cp = poly([(cxm - 128, cym - 78), (cxm - 100, cym - 118), (cxm + 100, cym - 118), (cxm + 128, cym - 78)])
    c.drawPath(cp, _P(T("#B9552F")))
    c.drawPath(cp, _P(INK, 160, style="stroke", sw=1.4))
    c.drawRect(skia.Rect.MakeLTRB(cxm - 120, cym - 78, cxm + 120, cym), _P(INK, 160, style="stroke", sw=1.4))
    for k in range(7):
        ax = cxm - 100 + k * 33
        ap = skia.Path()
        ap.moveTo(ax - 8, cym)
        ap.lineTo(ax - 8, cym - 36)
        ap.arcTo(skia.Rect.MakeLTRB(ax - 8, cym - 44, ax + 8, cym - 28), 180, 180, False)
        ap.lineTo(ax + 8, cym)
        ap.close()
        c.drawPath(ap, _P(T("#3A2A1C"), 230))
    c.drawCircle(cxm + 102, cym - 98, 9, _P(T("#3A2A1C"), 200))
    c.drawRect(skia.Rect.MakeLTRB(cxm + 108, cym - 148, cxm + 130, cym - 118), _P(T("#E4D5AE")))
    c.drawRect(skia.Rect.MakeLTRB(cxm + 108, cym - 148, cxm + 130, cym - 118), _P(INK, 150, style="stroke", sw=1.2))
    roofs.append((cxm - 20, cym - 122))
    roofs.append((cxm + 60, cym - 122))
    # servi/çalı + kıyı kayaları
    for i in range(34):
        x = rs.uniform(120, HILL_W - 40)
        if rs.rand() < 0.5:
            yb = base + prof(x) + rs.uniform(220, 260)
            if yb < base:
                SC.cypress(c, x, yb, rs.uniform(30, 62), T("#2E4A33"), T("#4F6E4A"))
    for i in range(26):
        x = rs.uniform(0, HILL_W)
        r = rs.uniform(10, 26)
        yb = base + prof(x) + rs.uniform(120, 300)
        if yb > base - 4:
            c.drawOval(skia.Rect.MakeLTRB(x - r * 1.4, base - r * 0.7 + rs.uniform(-3, 3), x + r * 1.4, base + 8), _P(T("#5E4C3A")))
    if tod == "night" or tod == "fire":
        for (wx, wy, ww, wh) in wins[::3]:
            c.drawRect(skia.Rect.MakeXYWH(wx, wy, ww, wh), _P("#FFB04A", 120 if tod == "fire" else 220))
    img = fr.surf.makeImageSnapshot()
    _HILLS[tod] = (img, dict(roofs=roofs, base=base, prof=prof))
    return _HILLS[tod]


def flame(c, x, y, h, t, seed, w=None, a=1.0):
    """Stilize alev dili (kâğıt-kesim): dış kızıl, orta turuncu, iç altın; ucu sallanır; boy titreşir. Taban (x,y)."""
    w = w or h * 0.46
    fl = 0.78 + 0.22 * math.sin(t * (7.0 + 3 * hash01(seed, 1)) + seed * 3.1) + 0.08 * math.sin(t * 17.0 + seed)
    hh = h * fl
    sway = math.sin(t * (3.0 + hash01(seed, 2) * 2.0) + seed) * w * 0.38
    for (k, col, al) in ((1.0, "#B33620", 235), (0.74, "#E8742A", 245), (0.46, "#F6C94A", 250)):
        ww, h2 = w * k, hh * k
        sx = sway * k
        p = skia.Path()
        p.moveTo(x - ww * 0.55, y)
        p.cubicTo(x - ww * 0.80, y - h2 * 0.35, x - ww * 0.15 + sx * 0.5, y - h2 * 0.70, x + sx, y - h2)
        p.cubicTo(x + ww * 0.30 + sx * 0.6, y - h2 * 0.62, x + ww * 0.85, y - h2 * 0.30, x + ww * 0.55, y)
        p.quadTo(x, y + h2 * 0.07, x - ww * 0.55, y)
        c.drawPath(p, _P(col, int(al * a)))
        if k == 1.0:
            c.drawPath(p, _P("#3A1410", int(150 * a), style="stroke", sw=1.2))


def flame_cluster(c, x, y, s, t, seed, k=1.0):
    """Yanan çatı: 4 alev dili + parıltı + kıvılcım. s ölçek, k 0..1 (yanma şiddeti: alevler büyür)."""
    if k <= 0.01:
        return
    fl = 0.75 + 0.25 * math.sin(t * 8.0 + seed)
    glow(c, x, y - 30 * s, 110 * s * (0.6 + 0.5 * k), "#FF9A3A", 0.50 * k * fl)
    for i, (dx, hh) in enumerate(((-0.28, 0.80), (0.0, 1.20), (0.30, 0.90), (-0.06, 0.62))):
        flame(c, x + dx * 54 * s, y, 74 * s * hh * k, t, seed * 7 + i, 36 * s * k + 6)
    for i in range(7):
        ph = (t * (0.45 + 0.3 * hash01(seed, i)) + hash01(seed, i + 9)) % 1.0
        ex = x + (hash01(seed, i + 3) - 0.5) * 46 * s + math.sin(t * 2.0 + i) * 8 * s * ph - 28 * s * ph
        ey = y - 30 * s - ph * 150 * s * k
        c.drawCircle(ex, ey, (2.4 - 1.4 * ph) * s + 0.4, _P("#FFD070", int(255 * (1 - ph) * k)))


class DriftShip:
    """Basit hareketli filo üyesi (tek yön, hafif ivmeli): kıyıya yaklaşan donanma için. ShipSpec arayüzü."""

    def __init__(self, idx, liv, x0, y, scale, vx, seed, hl=False, hz=0.76, ease=None, tmax=None):
        self.kind = "kadirga"
        self.idx, self.liv, self.x0, self.y, self.scale, self.vx, self.seed = idx, liv, x0, y, scale, vx, seed
        self.highlight = hl
        self.hz, self.sails, self.oars, self.crew, self.ensign = hz, False, True, False, True
        self.wind, self.tilt, self.wake, self.arms = 1.0, 1.0, 0.9, None
        self.dirn = 1 if vx >= 0 else -1
        self.ph = hash01(seed, 5)
        self.ease, self.tmax = ease, tmax

    def pos(self, t):
        if self.ease and self.tmax:
            u = clamp(t / self.tmax)
            e = ease_io(u) * 0.5 + u * 0.5
            return self.x0 + self.vx * self.tmax * e, self.y, self.dirn, abs(self.vx) * (0.5 + 0.5 * (6 * u * (1 - u) * 0.5 + 0.5))
        return self.x0 + self.vx * t, self.y, self.dirn, abs(self.vx)


def make_armada(cx, dur, yh, n=16, liv="osmanli", x_from=-300.0, x_to=620.0, y_rng=(470.0, 690.0), scale=0.46, seed=11, nao=0):
    rs = _RS(seed * 19 + 5)
    out = []
    lv = livery(liv)
    for i in range(n):
        y = rs.uniform(*y_rng)
        p = persp(y, yh)
        x_end = x_to - rs.uniform(0, 900) * (0.6 + 0.4 * p)
        x0 = x_end - (x_to - x_from) * rs.uniform(0.40, 0.62)
        vx = (x_end - x0) / dur
        out.append(DriftShip(i, lv, x0, y, scale * rs.uniform(0.9, 1.1), vx, seed * 7 + i, False, 0.74 + rs.uniform(-0.03, 0.03), True, dur))
    out.sort(key=lambda S: S.y)
    return out


def _scene_kiyi(cx, f, tod, kw, cams, kick, caption, at, band, labels, ships):
    """Otranto kıyısı: tepede kale-kent silueti, kıyıya yaklaşan donanma (silüet), stilize alev + duman; turuncu→altın ışık. İnsan/kan/ceset YOK."""
    dur = max(cx.dur, 1e-3)
    kw = dict(kw)
    tod = kw.pop("tod_", None) or ("fire" if tod in ("day", "fire") else tod)
    cfg = _scene_cfg("kiyi", tod, kw)
    cfg["horizon"] = kw.get("horizon", 392.0)
    cfg["birds"] = kw.get("birds", 3)
    cfg["sun"] = kw.get("sun", (1250, 236, 84))
    cfg["glitter"] = kw.get("glitter", 1.0)
    cfg["clouds"] = kw.get("clouds", 5)
    cfg["swell"] = kw.get("swell", 0.9)
    yh = cfg["horizon"]
    hill_x = float(kw.get("hill_x", 640.0))
    shore_y = float(kw.get("shore_y", 548.0))
    hill_f = float(kw.get("hill_f", 0.66))
    fire_at = _tcall(cx, kw.get("fire_at", 0.0), 0.0)
    n_ships = int(kw.get("n", 16))
    arm = make_armada(cx, dur, yh, n_ships, kw.get("fleet", "osmanli"), -300.0, float(kw.get("x_to", 640.0)), (shore_y - 40.0, 700.0), float(kw.get("fscale", 0.46)), cfg["seed"])
    extra = _norm_ships(cx, ships or [], dur)
    all_ships = arm + extra
    img, info = otranto_hill(tod)
    roofs = info["roofs"]
    rs = _RS(cfg["seed"] * 3 + 9)
    # yanan çatılar: kale yanı ve orta yamaç ağırlıklı
    spots = [roofs[i] for i in rs.permutation(len(roofs))[: int(kw.get("n_fire", 10))]]
    default = [(0.0, (1130, 26, 1.0)), (0.6, (1000, 6, 1.10)), (1.0, (860, -12, 1.24))]
    hill_y0 = shore_y - HILL_H + 8                                   # sprite üstü (katman y)
    state = {"drawn": False}

    def mid(ctx, sea, k):
        # tepe, kıyıya (shore_y) en yakın satırdan önce çizilir (ön satırlar kayalık tabanı örter)
        if state.get("k0") is None:
            state["k0"] = sea.row_before(shore_y)
        if k == state["k0"] and not state["drawn"]:
            state["drawn"] = True
            ctx.push(hill_f)
            c = ctx.c
            if ctx.visible(hill_f, hill_x, hill_x + HILL_W, 60):
                c.drawImageRect(img, skia.Rect.MakeWH(img.width(), img.height()), skia.Rect.MakeXYWH(hill_x, hill_y0, HILL_W, HILL_H), LIN, skia.Paint())
                tt = ctx.t
                for i, (fx, fy) in enumerate(spots):
                    kk = sstep(fire_at + i * 0.30, fire_at + i * 0.30 + 1.6, tt)
                    s_ = 0.62 + 0.30 * hash01(i, 5)
                    flame_cluster(c, hill_x + fx, hill_y0 + fy + 8, s_, tt, i + 1, kk)
                for i, (fx, fy) in enumerate(spots[:4]):
                    kk = sstep(fire_at + i * 0.30 + 0.4, fire_at + i * 0.30 + 2.6, tt)
                    if kk > 0.02:
                        draw_smoke_column(c, hill_x + fx, hill_y0 + fy - 10, 230 + 90 * hash01(i, 8), tt, 40 + i, tod, wind_dx=-80.0, n=8, width=0.62, a=0.66 * kk, warm=0.8, grow=0.8 + 0.3 * kk, rise=0.13)
            ctx.pop()
    state2 = {}

    def post(ctx, sea):
        # alev yansıması: kıyıya yakın suda turuncu çizgiler (titreşen)
        c = ctx.c
        ctx.push(1.0)
        tt = ctx.t
        for i, (fx, fy) in enumerate(spots):
            kk = sstep(fire_at + i * 0.30, fire_at + i * 0.30 + 1.6, tt)
            if kk < 0.02:
                continue
            xx = ctx.Cx(hill_f) + (hill_x + fx - ctx.Cx(hill_f))  # katman 0,66 ↔ ana düzlem: yaklaşık
            for j in range(5):
                ph = (tt * 0.5 + j * 0.2 + hash01(i, j) * 0.3) % 1.0
                xs_ = xx * 1.0 + (hash01(i, j + 5) - 0.5) * 70
                ys_ = shore_y + 28 + j * 22 + hash01(i, j) * 8
                ln = 18 + 40 * hash01(i, j + 2)
                c.drawLine(xs_ - ln / 2, ys_, xs_ + ln / 2, ys_, _P("#FFB04A", int(255 * 0.55 * kk * (0.5 + 0.5 * math.sin(tt * 4 + i + j)) ** 2), style="stroke", sw=2.6))
        ctx.pop()
    ctx_, sea_ = _render_scene_custom(cx, f, cfg, all_ships, band, cams, default, "deniz_kiyi", post=post, mid=mid, ship_fn=lambda ctx, sea, S, t: (render_fleet_ship(ctx, sea, S, t)))
    _deco_labels(f, cx, ctx_, sea_, labels, at)
    _frame_decor(f, cx, band, 1.0, kick, caption, at)
    _finish(f, cx, tod, cfg["seed"], motes=34)


# ═════════════════════════════ FİLO: sprite sayfaları (LOD), formasyon, duman perdesi ═════════════════════════════
GAL_BBOX = (-326, -334, 398, 64)
_SHEETS = _LRU(220 * 1024 * 1024)
NPH = 14


class _Dummy:
    seed = 0


def galley_sheet(tod, liv, bs):
    """Küçük kadırgalar için sprite sayfası: NPH kürek evresi × (rig(sarılı yelken) + gövde + kürekler). Dönüş: [LSpr]. Anahtar: (tod, livery adı, kova)."""
    key = (tod, liv.get("name", "x"), liv["wale"], liv["flag"][2], round(bs, 2))
    sh = _SHEETS.get(key)
    if sh is not None:
        return sh
    rig = galley_rig(tod, liv, False, bs)
    hull = galley_hull(tod, liv, bs)
    d = _Dummy()
    d.liv = liv
    frames = []
    for p in range(NPH):
        def draw(c, p=p):
            rig.draw(c)
            hull.draw(c)
            galley_oars(c, p / NPH, d, tod, 1.0, 0.0)
        frames.append(bake_local(GAL_BBOX, bs, draw))
    _SHEETS.put(key, frames)
    return frames


def pennant_poly(c, x, y, L, h, t, col, ph=0.0, flip=1, a=255):
    """Tek çizimlik dalgalı flama (uzak gemiler için ucuz)."""
    n = 6
    top, bot = [], []
    for i in range(n + 1):
        u = i / n
        w = math.sin(t * 5.0 - u * 4.2 + ph) * h * 0.55 * u
        top.append((x + flip * u * L, y + w - h * 0.5 * (1 - 0.5 * u)))
        bot.append((x + flip * u * L, y + w + h * 0.5 * (1 - 0.5 * u)))
    nt = (x + flip * L * 0.86, y + math.sin(t * 5.0 - 3.6 + ph) * h * 0.3)
    pth = poly(top + [nt] + bot[::-1], True)
    c.drawPath(pth, _P(col, a))


class FleetShip:
    """Filo üyesi: analitik konum (iki cephe yaklaşır). ShipSpec arayüzü (pos, kind, liv, scale …)."""

    def __init__(self, idx, liv, side, y, scale, line_off, jit, g_fn, xc, seed, highlight=False, hz=0.78):
        self.kind = "kadirga"
        self.idx, self.liv, self.side = idx, liv, side
        self.y, self.scale, self.seed = y, scale, seed
        self.line_off, self.jit, self.g_fn, self.xc = line_off, jit, g_fn, xc
        self.highlight = highlight
        self.hz = hz
        self.sails = False
        self.oars = True
        self.crew = False
        self.ensign = True
        self.wind = 1.0
        self.tilt = 1.0
        self.wake = 0.8
        self.arms = None
        self.dirn = 1 if side < 0 else -1
        self.ph = hash01(seed, 5)

    def length(self):
        return GAL_L * self.scale

    def pos(self, t):
        g, gv = self.g_fn(t)
        if self.side < 0:
            x = self.xc - g / 2 - self.line_off + self.jit
        else:
            x = self.xc + g / 2 + self.line_off + self.jit
        return x, self.y, self.dirn, abs(gv) / 2.0


def make_fleet(cx, dur, yh, n=14, left="hristiyan", right="osmanli", highlight=0, gap=(1500.0, 380.0), approach=None, yfar=None, ynear=706.0, scale=None, seed=7, xc=960.0, lines=None):
    """İki filo: soldaki (left) sağa, sağdaki (right) sola yaklaşır. n = cephe başına kadırga. highlight = soldaki filoda altın flamalı (Toskana) gemi sayısı.
    Dönüş: [FleetShip]. Derinlik sıraları perspektife göre geometrik; yoğun filoda ikinci/üçüncü hatlar arkadan gelir."""
    rs = _RS(seed * 53 + 1)
    lines = lines or int(clamp(math.ceil(n / 8.0), 1, 6))
    m = max(3, int(math.ceil(n / lines)))
    sc = scale if scale is not None else min(0.9, 0.95 / lines) * 0.9
    yfar = yfar if yfar is not None else yh + 70.0
    pf, pn = persp(yfar, yh), persp(ynear, yh)
    t0, t1 = (0.0, dur * 0.92) if approach is None else (_tcall(cx, approach[0], 0.0), _tcall(cx, approach[1], dur * 0.92))
    g0, g1 = float(gap[0]), float(gap[1])

    def g_fn(t):
        u = (t - t0) / max(1e-6, t1 - t0)
        e = ease_io(u)
        g = g0 + (g1 - g0) * e
        gv = (g1 - g0) * (6 * clamp(u) * (1 - clamp(u))) / max(1e-6, (t1 - t0)) if 0 <= u <= 1 else 0.0
        return g, gv
    ships = []
    liv_l, liv_r = livery(left), livery(right)
    tus = livery("toskana")
    for side in (-1, 1):
        idx = 0
        for ln in range(lines):
            for j in range(m):
                if idx >= n:
                    break
                p = pn * (pf / pn) ** (j / max(1, m - 1))
                y = yh + p * (YREF - yh) + rs.uniform(-3, 3) * p
                L = GAL_L * sc * p
                off = ln * L * 1.12 + (0.5 * L * 0.55 if (j % 2) else 0.0) + (L * 0.10 if side > 0 else 0.0)
                jit = rs.uniform(-0.12, 0.12) * L
                hl = (side < 0 and highlight > 0 and ln == 0 and (j % max(1, m // max(1, highlight)) == 0) and sum(1 for q in ships if q.highlight) < highlight)
                liv = tus if hl else (liv_l if side < 0 else liv_r)
                ships.append(FleetShip(idx + (0 if side < 0 else 1000), liv, side, y, sc, off, jit, g_fn, xc, seed * 31 + idx + (7 if side > 0 else 0), hl, 0.74 + rs.uniform(-0.03, 0.03)))
                idx += 1
    need = highlight - sum(1 for q in ships if q.highlight)
    if need > 0:
        for q in ships:
            if need <= 0:
                break
            if q.side < 0 and not q.highlight:
                q.highlight, q.liv = True, tus
                need -= 1
    return ships


def render_fleet_ship(ctx, sea, S, t, force=False):
    """Küçük/uzak filo gemisi: sprite sayfasından tek blit + ucuz flama + köpük çizgisi. Büyükse render_ship (tam dinamik)."""
    x, y, dirn, sp = S.pos(t)
    k = sea.row_before(y)
    ru = sea.rows[max(0, k - 1)]
    s = S.scale * persp(y, sea.yh)
    Lh = GAL_L * s
    if Lh * ctx.z > 330 and not force:
        return render_ship(ctx, sea, S, t)
    if not ctx.visible(ru.f, x - Lh * 0.7, x + Lh * 0.7, 0.0):
        return
    P = ctx.P
    tod = ctx.tod
    bs = bucket(s * ctx.z)
    frames = galley_sheet(tod, S.liv, bs)
    ph = (t * S.hz * (0.5 + 0.5 * clamp(sp / 40.0)) + S.ph) % 1.0
    spr = frames[int(ph * NPH) % NPH]
    ctx.push(ru.f)
    c = ctx.c
    wy = float(sea.wave(ru, x, t))
    yy = y + 0.8 * wy
    sl = float(sea.slope(ru, x, t))
    pitch = clamp(math.degrees(math.atan(sl * 0.85)), -5.0, 5.0)
    c.save()
    c.translate(x, yy)
    c.rotate(pitch)
    c.scale(dirn * s, s)
    spr.draw(c)
    pc1, pc2, pdev = S.liv["pen"]
    if S.highlight:
        pc1 = "#E0B84E"
    fl = getattr(ctx, "wind_dir", 1) * dirn
    pennant_poly(c, 30, -312, 190, 34, t, Tint(tod)(pc1), S.seed * 0.7, 1 if fl > 0 else -1)
    if S.highlight:
        glow(c, 30 + (1 if fl > 0 else -1) * 80, -312, 120, "#FFE08A", 0.42 + 0.10 * math.sin(t * 3.0 + S.seed))
    c.restore()
    xa, xb = x - Lh * 0.52, x + Lh * 0.56
    c.drawLine(xa, yy + 1.0 * s, xb, yy + 1.0 * s, _P(P["foam"], 215, style="stroke", sw=max(1.2, 3.0 * s)))
    c.drawLine(xa, yy + 2.6 * s, xb, yy + 2.6 * s, _P(P["ink"], 70, style="stroke", sw=max(0.8, 1.0 * s)))
    if sp > 8.0:
        wl = Lh * 0.5
        x_st = x - dirn * Lh * 0.55
        c.drawOval(skia.Rect.MakeLTRB(min(x_st, x_st - dirn * wl), yy, max(x_st, x_st - dirn * wl), yy + 5 * s), _P(P["foam"], 120))
    ctx.pop()


# ── duman (şiddetsiz: yükselen yumuşak duman kütlesi) ──────────────────────
@functools.lru_cache(maxsize=24)
def smoke_sprite(variant, tod, warm=0.0):
    """Duman bulutu sprite'ı (önceden renklendirilmiş): üstte açık, altta koyu; sıcak ışık altta (ateş) ya da nötr."""
    rs = _RS(77 + variant * 13)
    S = 300
    fr = sk.Frame(S, S)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    base_lo = "#3A2A26" if tod != "night" else "#1A1A2E"
    base_hi = "#8A7A74" if tod != "night" else "#3A4468"
    if warm > 0:
        base_lo = mix(base_lo, "#8A3A22", warm * 0.5)
        base_hi = mix(base_hi, "#C8683A", warm * 0.35)
    union = None
    for i in range(9):
        cx_ = S / 2 + rs.uniform(-70, 70)
        cy_ = S / 2 + rs.uniform(-60, 60)
        r = rs.uniform(46, 86)
        pc = skia.Path()
        pc.addCircle(cx_, cy_, r)
        union = pc if union is None else (skia.Op(union, pc, skia.PathOp.kUnion_PathOp) or union)
    sh = skia.GradientShader.MakeLinear([(0, 40), (0, S - 40)], [C(base_hi), C(base_lo)], [0.0, 1.0])
    c.drawPath(union, skia.Paint(AntiAlias=True, Shader=sh))
    c.drawPath(union, _P("#1A100C", 90, style="stroke", sw=1.6))
    c.save()
    c.clipPath(union, skia.ClipOp.kIntersect, True)
    for i in range(6):
        c.drawOval(skia.Rect.MakeXYWH(rs.uniform(40, 170), rs.uniform(60, 220), rs.uniform(50, 120), rs.uniform(24, 60)), _P("#FFFFFF", 22, blur=8))
    c.restore()
    return fr.surf.makeImageSnapshot()


def draw_smoke_column(c, x, y_base, h, t, seed, tod, wind_dx=40.0, n=14, width=1.0, a=0.9, warm=0.0, grow=1.0, rise=0.18):
    """Yükselen duman sütunu: n bulut sprite'ı tabandan yukarı süzülür, büyür, solar; rüzgârla yan yatar. (x, y_base) taban; h sütun yüksekliği."""
    for i in range(n):
        ph = (t * rise + i / n + hash01(seed, i) * 0.07) % 1.0
        yy = y_base - ph * h
        xx = x + wind_dx * ph ** 1.4 + math.sin(t * 0.7 + i * 2.1 + seed) * 10 * ph
        r = (34 + 120 * ph) * width * grow
        al = a * math.sin(math.pi * min(1.0, ph * 1.0)) ** 0.7 * (1.0 - 0.15 * ph)
        if al < 0.03:
            continue
        im = smoke_sprite(i % 4, tod, round(warm * (1 - ph), 1))
        p = skia.Paint()
        p.setAlphaf(clamp(al))
        c.drawImageRect(im, skia.Rect.MakeWH(im.width(), im.height()), skia.Rect.MakeXYWH(xx - r, yy - r * 0.9, 2 * r, 2 * r * 0.9), LIN, p)


def draw_smoke_bank(ctx, cxm, y_base, k, t, width=520.0, h=360.0, seed=3, fct=1.0, cols=16):
    """Duman perdesi (filo karşılaşması): k 0..1 büyüme; su hattından göğe yükselen, yumuşak, yan yana duman sütunları (şiddet göstermez; yaklaşma ve dip ima edilir). Ana düzlemde (f=1)."""
    if k <= 0.003:
        return
    tod = ctx.tod
    ctx.push(fct)
    c = ctx.c
    for i in range(cols):
        u = (i + 0.5) / cols
        xc = cxm + (u - 0.5) * width * (0.45 + 0.75 * k)
        env = math.sin(math.pi * u) ** 0.8
        hc = h * k * (0.45 + 0.55 * env) * (0.85 + 0.30 * hash01(seed, i))
        draw_smoke_column(c, xc, y_base, hc, t + i * 0.7, seed * 13 + i, tod, wind_dx=-34.0 * k, n=6, width=0.95, a=0.88 * min(1.0, k * 1.6), grow=0.55 + 0.6 * k, rise=0.10 + 0.04 * hash01(seed, i + 9))
    ctx.pop()


def _scene_filo(cx, f, tod, kw, cams, kick, caption, at, band, labels, n, ships):
    """Filo: iki filo karşılıklı yaklaşır (İnebahtı/Lepanto). Şiddet yok: çarpışma/ateş/ölü gösterilmez; yaklaşma + sancak + (isteğe bağlı) duman perdesi."""
    dur = max(cx.dur, 1e-3)
    kw = dict(kw)
    cfg = _scene_cfg("filo", tod, kw)
    cfg["horizon"] = kw.get("horizon", 292.0)
    cfg["birds"] = kw.get("birds", 3)
    cfg["glitter"] = kw.get("glitter", 0.7)
    yh = cfg["horizon"]
    nn = int(n or kw.pop("n_side", 14))
    fl = make_fleet(cx, dur, yh, nn, kw.get("left", "hristiyan"), kw.get("right", "osmanli"), int(kw.get("highlight", 0) or 0), tuple(kw.get("gap", (1500.0, 380.0))),
                    kw.get("approach"), kw.get("yfar"), kw.get("ynear", 706.0), kw.get("fscale"), cfg["seed"], 960.0, kw.get("lines"))
    extra = _norm_ships(cx, ships or [], dur)
    all_ships = fl + extra
    smoke_at = kw.get("smoke_at")
    ts = _tcall(cx, smoke_at, None) if smoke_at is not None else None
    sdur = float(kw.get("smoke_dur", 4.0))
    default = [(0.0, (960, 14, 1.0)), (0.6, (960, 4, 1.10)), (1.0, (960, -6, 1.22))]
    dim = float(kw.get("dim", 0.0))

    def rs_ship(ctx, sea, S, t):
        if isinstance(S, FleetShip):
            render_fleet_ship(ctx, sea, S, t)
        else:
            render_ship(ctx, sea, S, t)

    def post(ctx, sea):
        if ts is not None:
            k = ease_io((ctx.t - ts) / max(1e-6, sdur))
            draw_smoke_bank(ctx, 960.0, float(kw.get("smoke_y", 668.0)), k, ctx.t, width=float(kw.get("smoke_w", 620.0)), h=float(kw.get("smoke_h", 400.0)), seed=cfg["seed"] + 4)
            if dim > 0 and k > 0:
                rect(ctx.c, -3000, -300, 5000, 1300, "#1A1620", int(255 * dim * k * 0.55))
    ctx_, sea_ = _render_scene_custom(cx, f, cfg, all_ships, band, cams, default, "deniz_filo", post=post, ship_fn=rs_ship, coast=kw.get("coast"))
    _deco_labels(f, cx, ctx_, sea_, labels, at)
    _frame_decor(f, cx, band, 1.0, kick, caption, at)
    _finish(f, cx, tod, cfg["seed"])


def _render_scene_custom(cx, f, cfg, ships, band, cams, default, kind, pre=None, post=None, mid=None, ship_fn=None, coast=None, cam_override=None):
    """render_sea_scene + özel gemi çizicisi + isteğe bağlı uzak kara (filo/rota/kıyı)."""
    if coast:
        pre0 = pre
        pre = (lambda ctx, sea: ((pre0(ctx, sea) if pre0 else None), draw_coast(ctx, coast, ctx.t)))
    return render_sea_scene(cx, f, cfg, ships, band, cams, default, kind, pre=pre, post=post, mid=mid, cam_override=cam_override, ship_fn=ship_fn)


# ═════════════════════════════ LİMAN: ortak yapı taşları ═════════════════════════════
import cilt_build as CB                                  # çarklı vinç (treadwheel), yük bloğu, yük döngüsü

LX0, LW = -500, 3600                                     # liman katmanları: x ∈ [−500, 3100] (nötr kamera ekran pikseli)
YH_L = 360.0                                             # liman ufku (bant yerel y)
PAVE_TOP, EDGE, WALL_BOT = 470.0, 506.0, 598.0           # rıhtım: yüzey üst (arka), ön kenar, su hattı (duvar dibi)
SHIP_Y = 652.0                                           # yanaşan geminin su hattı
QUAY_FEET = (486.0, 500.0)                               # kalabalığın ayak y aralığı (rıhtım yüzeyi üstü)


def bake_layer(key, fn, scale=1.0, w=LW, x0=LX0):
    """Liman katmanını (x0..x0+w × −OV..800+OV) önbellekli pişir; dönüş: (Image, x0, y0, w, h) yerleştirme bilgisi."""
    h = 800 + 2 * OV
    im = baked(key, w, h, lambda c: (c.translate(-x0, OV), fn(c)), scale)
    return im, x0, -OV, w, h


def blit_layer(c, L):
    im, x0, y0, w, h = L
    c.drawImageRect(im, skia.Rect.MakeWH(im.width(), im.height()), skia.Rect.MakeXYWH(x0, y0, w, h), LIN, skia.Paint())


def draw_quay_wall(c, T, x0, x1, seed=1, stone="#B7A47C", rings=True, bollards=True):
    """Taş rıhtım: arka kaldırım şeridi (derinlik derzleri) + ön kenar silmesi + blok sıralı duvar yüzü (alt kısım rutubetli) + halkalar + babalar."""
    rs = _RS(seed)
    grad_v(c, x0, PAVE_TOP, x1, EDGE, [(T("#D3C49E", 0.0), 0.0), (T("#BFAC84", 0.0), 1.0)])
    y, k, gap = PAVE_TOP, 0, 5.0
    while y < EDGE:
        c.drawLine(x0, y, x1, y, _P("#4A3A22", 55 + k * 8, style="stroke", sw=1.0 + k * 0.18))
        off = (k % 2) * 40
        xx = x0 - (x0 % 80) + off
        while xx < x1:
            c.drawLine(xx, y, xx - 2 - k, y + gap, _P("#4A3A22", 48, style="stroke", sw=0.9))
            xx += 80 + k * 6
        y += gap
        gap *= 1.22
        k += 1
    for i in range(int((x1 - x0) / 55)):
        x = rs.uniform(x0, x1)
        oval(c, x, rs.uniform(PAVE_TOP + 6, EDGE - 4), rs.uniform(2, 6), rs.uniform(1, 2.6), "#6A5A3A", 70)
    # ön kenar silmesi
    rect(c, x0, EDGE - 2, x1, EDGE + 11, T("#D9CBA4", 0.0))
    c.drawLine(x0, EDGE - 2, x1, EDGE - 2, _P(INK, 170, style="stroke", sw=1.4))
    c.drawLine(x0, EDGE + 11, x1, EDGE + 11, _P(INK, 150, style="stroke", sw=1.2))
    # duvar yüzü
    grad_v(c, x0, EDGE + 11, x1, WALL_BOT, [(T(stone, 0.0), 0.0), (T(mix(stone, "#6A5A44", 0.35), 0.0), 0.75), (T("#4A4A3A", 0.0), 1.0)])
    yy = EDGE + 11
    row = 0
    while yy < WALL_BOT:
        hh = 21.0
        c.drawLine(x0, yy, x1, yy, _P("#2A1A0C", 95, style="stroke", sw=1.1))
        off = (row % 2) * 36
        xx = x0 - (x0 % 72) + off
        while xx < x1:
            c.drawLine(xx, yy, xx, min(WALL_BOT, yy + hh), _P("#2A1A0C", 80, style="stroke", sw=1.0))
            if rs.rand() < 0.10:
                rect(c, xx + 3, yy + 3, xx + 28, yy + hh - 3, "#FFFFFF", 22)
            xx += 72
        yy += hh
        row += 1
    wl = skia.GradientShader.MakeLinear([(0, WALL_BOT - 26), (0, WALL_BOT)], [C("#1B2A1A", 0), C("#1B2A1A", 140)], [0.0, 1.0])
    c.drawRect(skia.Rect.MakeLTRB(x0, WALL_BOT - 26, x1, WALL_BOT), skia.Paint(Shader=wl))
    shade = skia.GradientShader.MakeLinear([(0, EDGE + 11), (0, EDGE + 30)], [C("#1A1008", 70), C("#1A1008", 0)], [0.0, 1.0])
    c.drawRect(skia.Rect.MakeLTRB(x0, EDGE + 11, x1, EDGE + 30), skia.Paint(Shader=shade))
    if rings:
        for x in np.arange(x0 + 140, x1, 236.0):
            c.drawCircle(float(x), EDGE + 42, 7.5, _P("#2A2A2A", 255, style="stroke", sw=2.6))
            c.drawCircle(float(x), EDGE + 34, 2.6, _P("#2A2A2A", 255))
    if bollards:
        for x in np.arange(x0 + 90, x1, 330.0):
            x = float(x)
            rect(c, x - 9, EDGE - 24, x + 9, EDGE, T("#8A8A7E", 0.0))
            oval(c, x, EDGE - 26, 12, 5, T("#9A9A8E", 0.0))
            c.drawRect(skia.Rect.MakeLTRB(x - 9, EDGE - 24, x + 9, EDGE), _P(INK, 170, style="stroke", sw=1.2))
            c.drawOval(skia.Rect.MakeLTRB(x - 12, EDGE - 31, x + 12, EDGE - 21), _P(INK, 150, style="stroke", sw=1.1))
    # sağ uca doğru kayma yok: sol ucu yuvarlak baş (kıyı başı)
    rect(c, x0 - 10, EDGE - 2, x0 + 8, WALL_BOT, T("#A99674", 0.0))
    c.drawRect(skia.Rect.MakeLTRB(x0 - 10, EDGE - 2, x0 + 8, WALL_BOT), _P(INK, 160, style="stroke", sw=1.3))


def draw_row_houses(c, T, x0, x1, yb, rs, hmin=90, hmax=170, wmin=54, wmax=96, depth=0.10, wins=None, roofs=None):
    """Bitişik sıra evler (kat kat pencereli; cilt_city.draw_house yeniden kullanılır). roofs: (x_orta, çatı_tepesi_y) kayıtları (duman/bayrak için)."""
    x = x0
    while x < x1:
        w = rs.uniform(wmin, wmax)
        h = rs.uniform(hmin, hmax)
        CT.draw_house(c, x, yb, w, h, rs, T, depth, wins, hip=(rs.rand() < 0.5))
        if roofs is not None:
            roofs.append((x + w / 2, yb - h - min(h * 0.45, w * 0.4) * 1.1))
        x += w + rs.uniform(-3, 2)


def draw_warehouse(c, T, x, yb, w, h, rs, hoist=True, arches=3):
    """Ambar: kalın taş duvar, ağır kemerli kapılar (karanlık iç), beşik/kiremit çatı, tepede makaralı çıkrık kirişi (halat + kanca) ve küçük pencereler."""
    wall = T(["#D8C79C", "#CDB486", "#E0CCA2"][rs.randint(3)], 0.05)
    roof = T(CT.ROOFS[rs.randint(len(CT.ROOFS))], 0.05)
    rect(c, x, yb - h, x + w, yb, wall)
    c.drawRect(skia.Rect.MakeLTRB(x + w * 0.74, yb - h, x + w, yb), _P("#2A1A0C", 36))
    rh = h * 0.40
    rp = poly([(x - 6, yb - h), (x + w * 0.5, yb - h - rh), (x + w + 6, yb - h)])
    fink(c, rp, roof, 1.3, 255, 170)
    for k in range(1, 6):
        yy = yb - h - rh + k * rh / 6
        c.drawLine(x + w * 0.5 - (w * 0.5 + 6) * k / 6, yy, x + w * 0.5 + (w * 0.5 + 6) * k / 6, yy, _P("#5A2412", 60, style="stroke", sw=0.9))
    aw = w / (arches + 0.6)
    for i in range(arches):
        ax = x + w * 0.5 + (i - (arches - 1) / 2) * (aw * 1.18)
        ah = h * 0.52
        p = skia.Path()
        p.moveTo(ax - aw / 2, yb)
        p.lineTo(ax - aw / 2, yb - ah + aw / 2)
        p.arcTo(skia.Rect.MakeLTRB(ax - aw / 2, yb - ah, ax + aw / 2, yb - ah + aw), 180, 180, False)
        p.lineTo(ax + aw / 2, yb)
        p.close()
        c.drawPath(p, _P(T("#2E2016", 0.0)))
        c.drawPath(p, _P(INK, 190, style="stroke", sw=1.4))
        c.drawRect(skia.Rect.MakeXYWH(ax - aw * 0.34, yb - ah * 0.36, aw * 0.68, ah * 0.30), _P(T("#8A6A3A", 0.0), 255))
    for wx in (x + w * 0.16, x + w * 0.84):
        c.drawRect(skia.Rect.MakeXYWH(wx - 5, yb - h + 12, 10, 16), _P(T("#3A2A1C", 0.0), 210))
    c.drawRect(skia.Rect.MakeLTRB(x, yb - h, x + w, yb), _P(INK, 150, style="stroke", sw=1.2))
    if hoist:
        bx = x + w * 0.5
        by = yb - h - rh + 3
        c.drawLine(bx, by, bx + 34, by - 6, _P(INK, 230, style="stroke", sw=5.4))
        c.drawLine(bx, by, bx + 34, by - 6, _P(T("#7A5230", 0.0), 255, style="stroke", sw=3.4))
        c.drawCircle(bx + 33, by - 6, 4.0, _P("#2A2A2A"))
    return (x + w / 2, yb - h - rh - 6)


def draw_tower_sq(c, T, x, yb, w, h, rs, cap="conical", crenel=True, base_w=None):
    """Kare kule/burç: taş sıraları, mazgal, aşağıya sarkık alçı gölgesi, dar pencereler, koni ya da kiremit külah. Dönüş: tepe noktası (bayrak için)."""
    stone = T(["#C9B68C", "#BCA67E", "#CDBB92"][rs.randint(3)], 0.04)
    rect(c, x - w / 2, yb - h, x + w / 2, yb, stone)
    for r in range(int(h / 15)):
        c.drawLine(x - w / 2, yb - h + r * 15, x + w / 2, yb - h + r * 15, _P("#6A5A3A", 70, style="stroke", sw=1.0))
    c.drawRect(skia.Rect.MakeLTRB(x + w * 0.2, yb - h, x + w / 2, yb), _P("#2A1A0C", 46))
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, yb - h, x + w / 2, yb), _P(INK, 170, style="stroke", sw=1.4))
    top = yb - h
    if crenel:
        n = max(3, int(w / 14))
        for k in range(n):
            xx = x - w / 2 - 2 + k * (w + 4) / n
            rect(c, xx, top - 11, xx + (w + 4) / n * 0.55, top, stone)
            c.drawRect(skia.Rect.MakeLTRB(xx, top - 11, xx + (w + 4) / n * 0.55, top), _P(INK, 150, style="stroke", sw=1.0))
        rect(c, x - w / 2 - 3, top, x + w / 2 + 3, top + 6, T("#8A7452", 0.04))
    for ry in (0.28, 0.58):
        yy = yb - h * (1 - ry)
        c.drawRect(skia.Rect.MakeXYWH(x - 3.2, yy, 6.4, 15), _P(T("#2A1C10", 0.0), 230))
    if cap == "conical":
        cp = poly([(x - w * 0.60, top - 10), (x, top - 10 - w * 1.05), (x + w * 0.60, top - 10)])
        fink(c, cp, T("#B4552E", 0.04), 1.3, 255, 170)
        return (x, top - 10 - w * 1.05)
    return (x, top - 11)


def draw_tower_round(c, T, x, yb, r, h, rs, cap="conical", crenel=True):
    stone = T(["#C4B088", "#B8A27A", "#CDBA90"][rs.randint(3)], 0.04)
    rect(c, x - r, yb - h, x + r, yb, stone)
    c.drawRect(skia.Rect.MakeLTRB(x + r * 0.30, yb - h, x + r, yb), _P("#2A1A0C", 54))
    c.drawRect(skia.Rect.MakeLTRB(x - r, yb - h + 2, x - r * 0.62, yb), _P("#FFF4D0", 26))
    for rr in range(int(h / 16)):
        c.drawLine(x - r, yb - h + rr * 16, x + r, yb - h + rr * 16, _P("#6A5A3A", 60, style="stroke", sw=0.9))
    c.drawRect(skia.Rect.MakeLTRB(x - r, yb - h, x + r, yb), _P(INK, 170, style="stroke", sw=1.4))
    top = yb - h
    if crenel:
        n = max(4, int(r * 2 / 9))
        for k in range(n):
            xx = x - r - 2 + k * (2 * r + 4) / n
            rect(c, xx, top - 10, xx + (2 * r + 4) / n * 0.55, top, stone)
            c.drawRect(skia.Rect.MakeLTRB(xx, top - 10, xx + (2 * r + 4) / n * 0.55, top), _P(INK, 150, style="stroke", sw=0.9))
        rect(c, x - r - 3, top, x + r + 3, top + 5, T("#8A7452", 0.04))
    c.drawRect(skia.Rect.MakeXYWH(x - 3, yb - h * 0.62, 6, 14), _P(T("#2A1C10", 0.0), 230))
    c.drawRect(skia.Rect.MakeXYWH(x - 3, yb - h * 0.34, 6, 14), _P(T("#2A1C10", 0.0), 230))
    if cap == "conical":
        cp = poly([(x - r * 1.12, top - 8), (x, top - 8 - r * 1.6), (x + r * 1.12, top - 8)])
        fink(c, cp, T("#B4552E", 0.04), 1.3, 255, 170)
        return (x, top - 8 - r * 1.6)
    return (x, top - 10)


def minaret(c, T, x, yb, h, w=9.0, cap_col="#9A8E7A", stone="#E4D8BC"):
    """İnce minare: gövde, şerefe (balkon) halkası, kurşun külah ve alem. Dönüş: tepe."""
    rect(c, x - w / 2, yb - h, x + w / 2, yb, T(stone, 0.2))
    c.drawRect(skia.Rect.MakeLTRB(x + w * 0.1, yb - h, x + w / 2, yb), _P("#2A1A0C", 44))
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, yb - h, x + w / 2, yb), _P(INK, 150, style="stroke", sw=1.0))
    sy = yb - h * 0.78
    rect(c, x - w * 1.05, sy, x + w * 1.05, sy + 5, T("#CFC2A2", 0.2))
    c.drawRect(skia.Rect.MakeLTRB(x - w * 1.05, sy, x + w * 1.05, sy + 5), _P(INK, 150, style="stroke", sw=0.9))
    c.drawLine(x - w * 1.05, sy - 5, x + w * 1.05, sy - 5, _P(INK, 120, style="stroke", sw=0.9))
    ct_ = poly([(x - w * 0.62, yb - h), (x, yb - h - w * 3.4), (x + w * 0.62, yb - h)])
    fink(c, ct_, T(cap_col, 0.2), 1.0, 255, 150)
    c.drawLine(x, yb - h - w * 3.4, x, yb - h - w * 4.4, _P("#C79A3C", 255, style="stroke", sw=1.6))
    return (x, yb - h - w * 4.4)


def dome_mass(c, T, x, yb, r, h_drum=14, col="#C9BFA4", lead="#8E8E8A", windows=True):
    """Kubbe: kısa tambur (pencere sırası) + yarım küre (kurşun) + alem. Dönüş: tepe."""
    rect(c, x - r, yb - h_drum, x + r, yb, T("#E0D4B4", 0.2))
    c.drawRect(skia.Rect.MakeLTRB(x - r, yb - h_drum, x + r, yb), _P(INK, 140, style="stroke", sw=1.0))
    if windows:
        for k in range(int(r / 9)):
            wx = x - r + 9 + k * (2 * r - 18) / max(1, int(r / 9) - 1)
            c.drawRect(skia.Rect.MakeXYWH(wx - 2.2, yb - h_drum + 3, 4.4, h_drum - 6), _P(T("#3A2A1C", 0.0), 190))
    p = skia.Path()
    p.moveTo(x - r, yb - h_drum)
    p.cubicTo(x - r, yb - h_drum - r * 1.15, x + r, yb - h_drum - r * 1.15, x + r, yb - h_drum)
    p.close()
    fink(c, p, T(lead, 0.2), 1.2, 255, 160)
    c.save()
    c.clipPath(p, skia.ClipOp.kIntersect, True)
    c.drawRect(skia.Rect.MakeLTRB(x + r * 0.25, yb - h_drum - r * 1.2, x + r, yb - h_drum), _P("#1A1008", 40))
    c.drawOval(skia.Rect.MakeLTRB(x - r * 0.7, yb - h_drum - r * 0.95, x - r * 0.1, yb - h_drum - r * 0.45), _P("#FFFFFF", 38, blur=3))
    c.restore()
    c.drawLine(x, yb - h_drum - r * 0.86, x, yb - h_drum - r * 1.12, _P("#C79A3C", 255, style="stroke", sw=1.6))
    return (x, yb - h_drum - r * 1.12)


def draw_stack(c, T, x, yb, w, h, rs, kind="bales"):
    """Rıhtım yığınları (kaldırım üstü): balya/çuval/varil/sandık."""
    if kind == "barrels":
        n = max(2, int(w / 20))
        for i in range(n):
            bx = x + i * 20 + 10
            hh = h * (0.7 + 0.3 * rs.rand())
            ovalink(c, bx, yb - hh / 2, 9.5, hh / 2, T("#9A6A3A", 0.0), 1.0, 255, 170)
            c.drawLine(bx - 9, yb - hh * 0.75, bx + 9, yb - hh * 0.75, _P("#3A2410", 190, style="stroke", sw=1.4))
            c.drawLine(bx - 9, yb - hh * 0.25, bx + 9, yb - hh * 0.25, _P("#3A2410", 190, style="stroke", sw=1.4))
    elif kind == "crates":
        rectink(c, x, yb - h, x + w, yb, T("#A87C4A", 0.0), 1.2, 255, 170)
        c.drawLine(x, yb - h, x + w, yb, _P("#4A2E16", 140, style="stroke", sw=1.2))
        c.drawLine(x + w, yb - h, x, yb, _P("#4A2E16", 140, style="stroke", sw=1.2))
        rectink(c, x + w * 0.2, yb - h * 1.7, x + w * 0.85, yb - h, T("#B88E58", 0.0), 1.2, 255, 170)
    else:
        for i in range(int(w / 24)):
            bx = x + i * 24 + 12
            hh = h * (0.7 + 0.5 * rs.rand())
            p = smoothp([(bx - 11, yb), (bx - 13, yb - hh * 0.6), (bx - 6, yb - hh), (bx + 6, yb - hh), (bx + 13, yb - hh * 0.6), (bx + 11, yb)], True, 0.5)
            fink(c, p, T(["#C8B27A", "#B89A62", "#D6C18E"][i % 3], 0.0), 1.2, 255, 170)
            c.drawLine(bx - 8, yb - hh * 0.62, bx + 8, yb - hh * 0.62, _P("#4A3A22", 120, style="stroke", sw=1.0))


# ═════════════════════════════ LİMAN: varyantlar (marsilya | napoli | livorno | pera | generic) ═════════════════════════════
def _ridge_fill(c, T, x0, x1, base, amp, scale, ph, col, depth, ink=True, step=10, trees=0, rs=None, tree_col=None):
    xs, ys = _ridge_pts(x0, x1, base, amp, scale, ph, step)
    ys = np.minimum(ys, base - 2)
    pts = list(zip(xs.tolist(), ys.tolist())) + [(float(xs[-1]), base + 80), (float(xs[0]), base + 80)]
    c.drawPath(poly(pts, True), _P(T(col, depth)))
    if ink:
        c.drawPath(poly(list(zip(xs.tolist(), ys.tolist())), False), _P(INK, 70, style="stroke", sw=1.2))
    if trees and rs is not None:
        for k in range(trees):
            x = rs.uniform(x0, x1)
            y = float(np.interp(x, xs, ys))
            SC.cypress(c, x, y + 2, rs.uniform(18, 40), T(tree_col or "#2E4A33", depth), T("#4F6E4A", depth))
    return xs, ys


def _haze(c, x0, x1, y0, y1, col, a0, a1):
    sh = skia.GradientShader.MakeLinear([(0, y0), (0, y1)], [C(col, a0), C(col, a1)], [0.0, 1.0])
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.Paint(Shader=sh))


class Harbor:
    """Liman dünyası: uzak siluet (f=0,30) + yapı katmanı (f=0,82) + rıhtım (f=1) önceden pişirilir; dinamik bayrak/duman/yeldeğirmeni/çark/kalabalık çağıran tarafta."""

    def __init__(self, variant, tod, year=None):
        self.v = variant if variant in ("marsilya", "napoli", "livorno", "pera", "generic") else "generic"
        self.tod = tod
        self.year = year
        self.T = Tint(tod)
        self.flags, self.smokes, self.mills, self.cranes = [], [], [], []
        self.quay_x0 = {"marsilya": 600.0, "napoli": 640.0, "livorno": 520.0, "pera": 480.0, "generic": 560.0}[self.v]
        self.yc = "y0"
        if self.v == "pera" and year:
            self.yc = "y1" if year < 1500 else ("y2" if year < 1574 else "y3")
        self.far = bake_layer(f"lm_{self.v}_{tod}_{self.yc}_far", self._draw_far, 1.0)
        self.bld = bake_layer(f"lm_{self.v}_{tod}_{self.yc}_bld", self._draw_bld, 1.0)
        self.quay = bake_layer(f"lm_{self.v}_{tod}_{self.yc}_quay", self._draw_quay, 1.2, x0=int(self.quay_x0 - 40), w=3140 - int(self.quay_x0 - 40) + 200)
        self.lit = tod in ("night", "dusk", "fire")

    # ── uzak siluet (f=0,30): ufuk tabanı YH_L ──────────────────────────────
    def _draw_far(self, c):
        T, v = self.T, self.v
        rs = _RS({"marsilya": 31, "napoli": 32, "livorno": 33, "pera": 34, "generic": 35}[v])
        yh = YH_L + 6
        if v == "marsilya":
            # kireçtaşı tepeler: açık, çıplak; solda iki yeldeğirmeni
            _ridge_fill(c, T, -500, 3100, yh, 130, 380, 0.4, "#D9D1B8", 0.55, trees=0)
            xs, ys = _ridge_fill(c, T, -500, 3100, yh, 96, 260, 2.1, "#C7BFA2", 0.38, trees=26, rs=rs, tree_col="#4A5E3E")
            xs2, ys2 = _ridge_fill(c, T, -500, 3100, yh, 60, 170, 4.1, "#B5AC8E", 0.22, trees=30, rs=rs, tree_col="#3A5236")
            for mx in (-60.0, 250.0, 520.0):
                my = float(np.interp(mx, xs, ys))
                self.mills.append((mx, my + 4.0, 38.0))
            for k in range(46):
                x = rs.uniform(-480, 3080)
                y = float(np.interp(x, xs2, ys2)) + rs.uniform(8, 40)
                if y < yh - 2:
                    CT.draw_house(c, x, y, rs.uniform(16, 28), rs.uniform(12, 22), rs, T, 0.45)
        elif v == "napoli":
            # Vezüv: Monte Somma (sol, yırtık kenar) + Vezüv konisi (sağ, kraterli) — soluk lila mavi
            lil = "#A59CC0"
            pts = [(1050, yh), (1180, yh - 90), (1300, yh - 168), (1420, yh - 214), (1520, yh - 196), (1580, yh - 150), (1640, yh - 198), (1700, yh - 262), (1760, yh - 282), (1800, yh - 270), (1850, yh - 286),
                   (1930, yh - 254), (2060, yh - 168), (2220, yh - 96), (2400, yh - 40), (2560, yh)]
            xs_, ys_ = zip(*pts)
            f_ = PN.pchip(list(xs_), list(ys_))
            xx = np.arange(1050, 2561, 8)
            yy = np.array([f_(x) for x in xx])
            c.drawPath(poly(list(zip(xx.tolist(), yy.tolist())) + [(2560, yh + 60), (1050, yh + 60)], True), _P(T(lil, 0.52)))
            c.drawPath(poly(list(zip(xx.tolist(), yy.tolist())), False), _P(INK, 80, style="stroke", sw=1.4))
            # yamaç gölgesi (ışık solda → sağ yamaç koyu)
            c.save()
            c.clipPath(poly(list(zip(xx.tolist(), yy.tolist())) + [(2560, yh + 60), (1050, yh + 60)], True), skia.ClipOp.kIntersect, True)
            c.drawPath(poly([(1760, yh - 284), (2100, yh - 150), (2560, yh), (1850, yh)], True), _P(T("#6E6490", 0.3), 120))
            for q in range(18):
                x = rs.uniform(1100, 2500)
                c.drawLine(x, yh - rs.uniform(30, 120), x + rs.uniform(10, 60), yh, _P("#4A3F68", 34, style="stroke", sw=1.4))
            c.restore()
            _ridge_fill(c, T, -500, 3100, yh, 70, 220, 1.3, "#B2B0A0", 0.36, trees=18, rs=rs)
            _ridge_fill(c, T, -500, 3100, yh, 46, 140, 3.7, "#9FA48C", 0.2, trees=26, rs=rs)
            for k in range(60):
                x = rs.uniform(1100, 2700)
                y = yh - rs.uniform(2, 26)
                CT.draw_house(c, x, y, rs.uniform(10, 20), rs.uniform(8, 16), rs, T, 0.45)
        elif v == "livorno":
            # alçak kıyı + uzak Apenin tepeleri (mavi)
            _ridge_fill(c, T, -500, 3100, yh - 6, 120, 520, 0.9, "#A9B7C4", 0.62)
            _ridge_fill(c, T, -500, 3100, yh, 60, 300, 2.7, "#9FAE9C", 0.4, trees=24, rs=rs)
            _ridge_fill(c, T, -500, 3100, yh, 24, 160, 4.2, "#94A58A", 0.22, trees=30, rs=rs)
        elif v == "pera":
            self._far_pera(c, T, rs, yh)
        else:
            _ridge_fill(c, T, -500, 3100, yh, 90, 360, 0.6, "#B8CFC4", 0.5)
            _ridge_fill(c, T, -500, 3100, yh, 60, 220, 2.6, "#9DB8AC", 0.3, trees=22, rs=rs)
        _haze(c, -500, 3100, yh - 110, yh + 10, T(pal(self.tod)["haze"], 0.0), 0, 130 if self.tod != "night" else 70)

    def _far_pera(self, c, T, rs, yh):
        """Tarihî yarımada silueti (Haliç karşı kıyısı): Ayasofya (ana kubbe + yarım kubbeler + payandalar + minare[ler]), cami grupları, Topkapı köşkleri, servi, sur."""
        yc = self.yc
        # arka plan: ikinci sıra (açık) — küçük camiler ve sur
        base = yh
        for k in range(14):
            x = -300 + k * 240 + rs.uniform(-40, 40)
            r = rs.uniform(18, 30)
            dome_mass(c, T, x, base - 18, r, 8, "#D9CFB0", "#9C9C98", True)
            if k % 2 == 0:
                minaret(c, T, x + r + 10, base - 18, rs.uniform(70, 96), 6.0)
        # sur (kıyı boyunca mazgallı, kuleli)
        rect(c, -500, base - 16, 3100, base + 6, T("#C9B68C", 0.3))
        for x in np.arange(-500, 3100, 14.0):
            rect(c, float(x), base - 22, float(x) + 7, base - 16, T("#C9B68C", 0.3))
        for x in np.arange(-440, 3100, 210.0):
            draw_tower_sq(c, T, float(x), base + 6, 18, 38, rs, cap="flat", crenel=True)
        c.drawLine(-500, base - 16, 3100, base - 16, _P(INK, 110, style="stroke", sw=1.0))
        # Topkapı: sivri külahlı köşkler + servi
        for k in range(7):
            x = 1500 + k * 78 + rs.uniform(-12, 12)
            h = rs.uniform(26, 42)
            rect(c, x - 16, base - 18 - h, x + 16, base - 18, T("#E7D6B0", 0.3))
            fink(c, poly([(x - 20, base - 18 - h), (x, base - 18 - h - 22), (x + 20, base - 18 - h)]), T("#9E5A3A", 0.3), 1.0, 255, 140)
        for k in range(26):
            x = rs.uniform(1380, 2240)
            SC.cypress(c, x, base - 16, rs.uniform(26, 50), T("#2E4A33", 0.3), T("#4F6E4A", 0.3))
        # Fatih Camii (sol): geniş kubbe + iki minare (1470'te tamamlanmış)
        xf = 340.0
        rect(c, xf - 120, base - 58, xf + 120, base - 16, T("#E2D5B4", 0.25))
        c.drawRect(skia.Rect.MakeLTRB(xf - 120, base - 58, xf + 120, base - 16), _P(INK, 130, style="stroke", sw=1.1))
        dome_mass(c, T, xf, base - 58, 62, 16, "#D9CFB0", "#8E918E")
        for sx in (-148.0, 148.0):
            minaret(c, T, xf + sx, base - 16, 160, 9.0)
        for sx in (-84.0, 84.0):
            dome_mass(c, T, xf + sx, base - 58, 26, 8, "#D9CFB0", "#8E918E", False)
        # Ayasofya (orta-sağ): ana kubbe, doğu/batı yarım kubbeler, payandalar, minare(ler)
        xa = 1010.0
        yb = base - 16
        rect(c, xa - 150, yb - 70, xa + 150, yb, T("#D9C7A2", 0.25))
        c.drawRect(skia.Rect.MakeLTRB(xa - 150, yb - 70, xa + 150, yb), _P(INK, 140, style="stroke", sw=1.2))
        for k in range(7):
            bx = xa - 140 + k * 46.7
            fink(c, poly([(bx - 9, yb), (bx - 4, yb - 66), (bx + 4, yb - 66), (bx + 9, yb)]), T("#B5A07C", 0.25), 1.0, 255, 130)
        for sx, rr in ((-96.0, 52.0), (96.0, 52.0)):                         # yarım kubbeler
            dome_mass(c, T, xa + sx, yb - 70, rr, 0, "#D9CFB0", "#9A9C98", False)
        dome_mass(c, T, xa, yb - 74, 70, 20, "#D9CFB0", "#8E918E", True)       # ana kubbe
        minarets = {"y1": [(xa + 168, 150)], "y2": [(xa + 168, 150), (xa - 168, 150)], "y3": [(xa + 168, 170), (xa - 168, 170), (xa + 214, 150), (xa - 214, 150)]}.get(yc, [(xa + 168, 150)])
        for (mx, mh) in minarets:
            minaret(c, T, mx, yb, mh, 10.0)
        # küçük cami grubu (sağ)
        for k in range(5):
            x = 2300 + k * 150 + rs.uniform(-20, 20)
            dome_mass(c, T, x, base - 20, rs.uniform(24, 36), 10, "#D9CFB0", "#9A9C98", True)
            minaret(c, T, x + 44, base - 20, rs.uniform(90, 130), 7.0)

    # ── yapı katmanı (f=0,82): kıyı yapıları; taban PAVE_TOP ────────────────
    def _draw_bld(self, c):
        T, v = self.T, self.v
        rs = _RS({"marsilya": 41, "napoli": 42, "livorno": 43, "pera": 44, "generic": 45}[v])
        yb = PAVE_TOP
        wins, roofs = [], []
        qx = self.quay_x0
        if v == "marsilya":
            # Fort Saint-Jean benzeri burç: kare kule + sivri kule + sur (limanın başında)
            draw_tower_sq(c, T, 420, yb + 4, 108, 210, rs, "flat", True)
            draw_tower_round(c, T, 340, yb + 4, 24, 150, rs)
            draw_tower_round(c, T, 500, yb + 4, 24, 160, rs)
            rect(c, 180, yb - 70, 380, yb + 6, T("#CBB88E", 0.04))
            c.drawRect(skia.Rect.MakeLTRB(180, yb - 70, 380, yb + 6), _P(INK, 160, style="stroke", sw=1.3))
            for k in range(14):
                rect(c, 180 + k * 15, yb - 80, 180 + k * 15 + 8, yb - 70, T("#CBB88E", 0.04))
            self.flags.append(dict(x=420, y=yb - 210 - 14, f=0.82, w=96, h=60, shape="swallow", dev="lily", c1="#233C8C", c2="#E0B84E", c3="#E0B84E", tag="fort"))
            draw_row_houses(c, T, qx + 40, 1280, yb, rs, 110, 190, 56, 98, 0.06, wins, roofs)
            # ambar grubu (çıkrıklı)
            wx_ = 1290
            for k, ww in enumerate((150, 130, 160)):
                top = draw_warehouse(c, T, wx_, yb, ww, 118 + 16 * k, rs, True, 3)
                wx_ += ww + 6
            draw_row_houses(c, T, wx_, 3120, yb, rs, 110, 200, 56, 100, 0.06, wins, roofs)
            # çan alınlıklı kilise (sağ)
            ch = draw_tower_sq(c, T, 2250, yb, 52, 250, rs, "conical", True)
        elif v == "napoli":
            T0 = T
            # Castel Nuovo: beş yuvarlak kule, sur, zafer kemeri (iki ön kule arasında)
            rect(c, 560, yb - 124, 1250, yb + 6, T("#BDA47C", 0.04))
            c.drawRect(skia.Rect.MakeLTRB(560, yb - 124, 1250, yb + 6), _P(INK, 160, style="stroke", sw=1.4))
            for k in range(46):
                rect(c, 560 + k * 15, yb - 134, 560 + k * 15 + 8, yb - 124, T("#BDA47C", 0.04))
            for r in range(8):
                c.drawLine(560, yb - 120 + r * 16, 1250, yb - 120 + r * 16, _P("#6A5A3A", 55, style="stroke", sw=1.0))
            tw = [(590, 56, 190), (770, 52, 170), (990, 52, 170), (1190, 56, 190), (880, 46, 236)]
            for (tx, tr, th) in sorted(tw, key=lambda q: -q[2]):
                top = draw_tower_round(c, T, tx, yb + 6, tr, th, rs, cap="flat", crenel=True)
            # zafer kemeri (beyaz mermer)
            ax = 880
            rect(c, ax - 72, yb - 150, ax + 72, yb + 6, T("#E6DFCC", 0.04))
            c.drawRect(skia.Rect.MakeLTRB(ax - 72, yb - 150, ax + 72, yb + 6), _P(INK, 160, style="stroke", sw=1.3))
            for lv, (yy0, ww) in enumerate(((yb + 6, 46), (yb - 78, 40))):
                ap = skia.Path()
                ap.moveTo(ax - ww / 2, yy0)
                ap.lineTo(ax - ww / 2, yy0 - 40 + ww / 2)
                ap.arcTo(skia.Rect.MakeLTRB(ax - ww / 2, yy0 - 40, ax + ww / 2, yy0 - 40 + ww), 180, 180, False)
                ap.lineTo(ax + ww / 2, yy0)
                ap.close()
                c.drawPath(ap, _P(T("#3A2A1C", 0.0), 235))
                c.drawPath(ap, _P(INK, 170, style="stroke", sw=1.3))
            for sx in (-52.0, 52.0):
                rect(c, ax + sx - 6, yb - 148, ax + sx + 6, yb - 126, T("#D6CDB4", 0.04))
            self.flags.append(dict(x=880, y=yb - 282, f=0.82, w=90, h=58, shape="swallow", dev="plain", c1="#E0B84E", c2="#B33620", c3="#B33620", tag="fort"))
            # şehir: teraslı yamaç, düz çatılı evler, majolika kubbe + çan kuleleri
            for r in range(4):
                x = 1290.0
                while x < 3120:
                    w_ = rs.uniform(50, 86)
                    h_ = rs.uniform(70, 130)
                    yb_ = yb - r * 10
                    CT.draw_house(c, x, yb_, w_, h_, rs, T, 0.05 + 0.03 * r, wins, hip=(rs.rand() < 0.15))
                    roofs.append((x + w_ / 2, yb_ - h_ - 14))
                    x += w_ + rs.uniform(-3, 2)
            dm = dome_mass(c, T, 1800, yb - 120, 46, 24, "#E4D8B8", "#4E8A6E")                       # majolika yeşil kubbe
            c.drawLine(1760, yb - 150, 1840, yb - 150, _P("#E0C04E", 255, style="stroke", sw=2.0))
            draw_tower_sq(c, T, 2280, yb, 46, 240, rs, "conical", True)
            draw_tower_sq(c, T, 2680, yb, 44, 210, rs, "conical", True)
        elif v == "livorno":
            # Fortezza Vecchia: tuğla-bej bastionlar, beyaz yuvarlak "Mastio", kare "Quadratura" kulesi
            def bastion(x0_, x1_, hgt):
                p = poly([(x0_, yb + 6), (x0_ + 26, yb - hgt), (x1_ - 26, yb - hgt), (x1_, yb + 6)])
                fink(c, p, T("#B98C68", 0.04), 1.5, 255, 175)
                c.save()
                c.clipPath(p, skia.ClipOp.kIntersect, True)
                for r in range(int(hgt / 14)):
                    c.drawLine(x0_, yb - hgt + r * 14, x1_, yb - hgt + r * 14, _P("#4A2412", 90, style="stroke", sw=1.1))
                c.drawRect(skia.Rect.MakeLTRB(x1_ - (x1_ - x0_) * 0.30, yb - hgt, x1_, yb + 6), _P("#2A1A0C", 50))
                c.restore()
            bastion(380, 700, 96)
            bastion(660, 1080, 120)
            top_m = draw_tower_round(c, T, 860, yb - 60, 54, 150, rs, cap="flat", crenel=True)
            top_q = draw_tower_sq(c, T, 1010, yb - 40, 66, 150, rs, "flat", True)
            for k in range(10):
                rect(c, 380 + k * 32, yb - 106, 380 + k * 32 + 17, yb - 96, T("#C9A98A", 0.04))
            self.flags.append(dict(x=860, y=yb - 60 - 150 - 20, f=0.82, w=84, h=54, shape="swallow", dev="medici", c1="#E0B84E", c2="#B33620", c3="#B33620", tag="fort"))
            # düzenli planlı şehir: dört katlı, birbirine benzer renkli cepheler; kanal boşluğu 1880–2060
            x = 1110.0
            while x < 3120:
                if 1860 < x < 2080:
                    x = 2080.0
                    continue
                w_ = rs.uniform(54, 74)
                h_ = rs.uniform(120, 150)
                CT.draw_house(c, x, yb, w_, h_, rs, T, 0.05, wins, hip=False)
                roofs.append((x + w_ / 2, yb - h_ - 18))
                x += w_ + rs.uniform(-2, 1)
            # kanal köprüsü kemeri (yapı katmanında arka plan)
            rect(c, 1850, yb - 20, 2090, yb + 6, T("#A99674", 0.04))
            # deniz feneri (Fanale): sekizgen kule + fener odası
            fx = 2860.0
            top_f = draw_tower_sq(c, T, fx, yb, 44, 280, rs, "flat", True)
            rect(c, fx - 20, yb - 280 - 40, fx + 20, yb - 280 - 10, T("#E4D8B8", 0.04))
            c.drawRect(skia.Rect.MakeLTRB(fx - 20, yb - 320, fx + 20, yb - 290), _P(INK, 160, style="stroke", sw=1.2))
            c.drawRect(skia.Rect.MakeLTRB(fx - 12, yb - 314, fx + 12, yb - 296), _P(T("#FFE9B0", 0.0) if self.tod != "day" else T("#E8D6A0", 0.0), 255))
            fink(c, poly([(fx - 24, yb - 320), (fx, yb - 348), (fx + 24, yb - 320)]), T("#8A6422", 0.04), 1.2, 255, 170)
            self.smokes.append(("fanal", fx, yb - 305))
        elif v == "pera":
            # Galata yamacı (sağ): kat kat taş/ahşap evler + Galata Kulesi; sol: rıhtım yapıları, gümrük ambarı
            for r in range(6):
                x = 1650.0 + (r % 2) * 20
                while x < 3120:
                    w_ = rs.uniform(40, 70)
                    h_ = rs.uniform(70, 120)
                    yb_ = yb - 14 - r * 22
                    CT.draw_house(c, x, yb_, w_, h_, rs, T, 0.05 + 0.02 * r, wins, hip=(rs.rand() < 0.5))
                    roofs.append((x + w_ / 2, yb_ - h_ - 12))
                    x += w_ + rs.uniform(-2, 3)
            # Galata kulesi: silindir gövde, çıkma, konik külah
            gx, gh, gr = 2300.0, 290.0, 36.0
            rect(c, gx - gr, yb - 140 - gh, gx + gr, yb - 140, T("#C8B692", 0.03))
            c.drawRect(skia.Rect.MakeLTRB(gx + gr * 0.3, yb - 140 - gh, gx + gr, yb - 140), _P("#2A1A0C", 56))
            c.drawRect(skia.Rect.MakeLTRB(gx - gr, yb - 140 - gh, gx - gr * 0.6, yb - 140), _P("#FFF4D0", 24))
            for r_ in range(int(gh / 15)):
                c.drawLine(gx - gr, yb - 140 - gh + r_ * 15, gx + gr, yb - 140 - gh + r_ * 15, _P("#6A5A3A", 55, style="stroke", sw=0.9))
            c.drawRect(skia.Rect.MakeLTRB(gx - gr, yb - 140 - gh, gx + gr, yb - 140), _P(INK, 170, style="stroke", sw=1.4))
            rect(c, gx - gr - 8, yb - 140 - gh, gx + gr + 8, yb - 140 - gh + 22, T("#B8A47E", 0.03))
            c.drawRect(skia.Rect.MakeLTRB(gx - gr - 8, yb - 140 - gh, gx + gr + 8, yb - 140 - gh + 22), _P(INK, 160, style="stroke", sw=1.2))
            for k in range(5):
                c.drawRect(skia.Rect.MakeXYWH(gx - gr - 3 + k * (2 * gr + 6) / 5, yb - 140 - gh + 4, 8, 14), _P(T("#2A1C10", 0.0), 230))
            fink(c, poly([(gx - gr - 10, yb - 140 - gh), (gx, yb - 140 - gh - 74), (gx + gr + 10, yb - 140 - gh)]), T("#8E5A3A", 0.04), 1.3, 255, 170)
            for k in range(3):
                c.drawRect(skia.Rect.MakeXYWH(gx - 4, yb - 140 - gh + 40 + k * 78, 8, 20), _P(T("#2A1C10", 0.0), 230))
            self.flags.append(dict(x=gx, y=yb - 140 - gh - 74 - 24, f=0.82, w=70, h=44, shape="swallow", dev="plain", c1="#E0B84E", c2="#B33620", c3="#B33620", tag="tower"))
            draw_row_houses(c, T, qx + 30, 1640, yb, rs, 80, 140, 52, 86, 0.06, wins, roofs)
            draw_warehouse(c, T, 1000, yb, 190, 120, rs, True, 3)
        else:
            draw_row_houses(c, T, qx + 30, 1500, yb, rs, 90, 150, 54, 90, 0.06, wins, roofs)
            draw_warehouse(c, T, 1500, yb, 170, 120, rs, True, 3)
            top_ = draw_tower_sq(c, T, 1840, yb, 70, 230, rs, "conical", True)
            self.flags.append(dict(x=1840, y=yb - 230 - 10 - 74 - 22, f=0.82, w=84, h=52, shape="swallow", dev="plain", c1="#233C8C", c2="#E0B84E", c3="#E0B84E", tag="tower"))
            draw_row_houses(c, T, 1930, 3120, yb, rs, 90, 160, 54, 92, 0.06, wins, roofs)
        # gece/alacakaranlık: pencere ışıkları
        if self.tod in ("night", "dusk", "fire"):
            p_ = 0.55 if self.tod == "night" else 0.22
            for (wx, wy, ww, wh) in wins:
                if rs.rand() < p_:
                    c.drawRect(skia.Rect.MakeXYWH(wx - 2, wy - 2, ww + 4, wh + 4), _P("#FFB04A", 55, blur=2.5))
                    c.drawRect(skia.Rect.MakeXYWH(wx, wy, ww, wh), _P("#FFD27A", 235))
        # baca dumanı: çatı kayıtlarından seç
        for i in range(0, len(roofs), 5):
            self.smokes.append(("house", roofs[i][0], roofs[i][1] + 4))

    # ── rıhtım katmanı (f=1,0) ───────────────────────────────────────────────
    def _draw_quay(self, c):
        T, v = self.T, self.v
        rs = _RS({"marsilya": 51, "napoli": 52, "livorno": 53, "pera": 54, "generic": 55}[v])
        qx = self.quay_x0
        x1 = 3140.0
        draw_quay_wall(c, T, qx, x1, seed=3)
        # kaldırım üstü yığınlar
        kinds = ["barrels", "bales", "crates", "bales", "barrels", "crates"]
        for i, x in enumerate(np.arange(qx + 160, x1 - 100, 260.0)):
            if rs.rand() < 0.55:
                draw_stack(c, T, float(x) + rs.uniform(-30, 30), rs.uniform(488, 496), rs.uniform(44, 84), rs.uniform(24, 40), rs, kinds[i % 6])
        if v == "livorno":                                                       # kanal ağzı: rıhtımda boşluk + köprü
            rect(c, 1900, PAVE_TOP - 4, 2060, WALL_BOT, T("#1E3A4A", 0.0))
            for r in range(10):
                c.drawLine(1900, EDGE + 11 + r * 9, 2060, EDGE + 11 + r * 9, _P("#FFFFFF", 22, style="stroke", sw=1.0))
            bp = skia.Path()
            bp.moveTo(1880, EDGE - 2)
            bp.lineTo(1880, EDGE - 36)
            bp.quadTo(1980, EDGE - 70, 2080, EDGE - 36)
            bp.lineTo(2080, EDGE - 2)
            bp.close()
            fink(c, bp, T("#B7A47C", 0.0), 1.5, 255, 180)
            ap = skia.Path()
            ap.moveTo(1912, EDGE + 11)
            ap.lineTo(1912, EDGE - 6)
            ap.quadTo(1980, EDGE - 40, 2048, EDGE - 6)
            ap.lineTo(2048, EDGE + 11)
            ap.close()
            c.drawPath(ap, _P(T("#1E3A4A", 0.0)))
            c.drawPath(ap, _P(INK, 170, style="stroke", sw=1.3))


# ═════════════════════════════ LİMAN: dinamik parçalar (halat, tahta, vinç, kalabalık, yeldeğirmeni) ═════════════════════════════
def ship_point(sea, S, t, lx, ly):
    """Geminin yerel (lx,ly) noktasının katman koordinatı (dalga sürüşü + eğim dâhil; render_ship ile aynı dönüşüm)."""
    x, y, dirn, sp = S.pos(t)
    ru = sea.rows[max(0, sea.row_before(y) - 1)]
    s = S.scale * persp(y, sea.yh)
    heave = 0.8 * float(sea.wave(ru, x, t))
    sl = float(sea.slope(ru, x, t))
    pitch = clamp(math.degrees(math.atan(sl * 0.85)) * S.tilt, -5.0, 5.0)
    px, py = xf_point(x, y + heave, pitch, s, dirn, lx, ly)
    return px, py, ru.f


def draw_rope(c, p0, p1, sag, t, col="#CDB57E", w=3.4, ph=0.0, sway=1.0):
    """Halat: iki nokta arası sarkan eğri (sag px); titreşim yavaşça sönen sinüs. Dönüş: yok."""
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    sg = sag + math.sin(t * 2.3 + ph) * 1.6 * sway * min(1.0, sag / 8.0 + 0.2)
    pth = skia.Path()
    pth.moveTo(*p0)
    pth.quadTo(mx, my + sg, *p1)
    c.drawPath(pth, _P(INK, 200, style="stroke", sw=w + 2.0))
    c.drawPath(pth, _P(col, 255, style="stroke", sw=w))


def rope_throw(c, p0, p1, u, t, arc=70.0, col="#CDB57E"):
    """Atılan halat: u 0..1; serbest uç p0→p1 parabolik süzülür, halat arkasından sarkar. u≥1: gergin bağ (kıç/baş)."""
    u = clamp(u)
    ex = p0[0] + (p1[0] - p0[0]) * u
    ey = p0[1] + (p1[1] - p0[1]) * u - arc * math.sin(math.pi * u) * (1.0 - 0.0 * u)
    sag = (1.0 - u) * 26.0 + (28.0 * (1 - u) ** 0.5 if u < 1 else 0.0) + (3.0 if u >= 1 else 0.0)
    draw_rope(c, p0, (ex, ey), sag, t, col, 3.4, 0.0, 1.0 if u < 1 else 0.4)


def draw_plank(c, a, b, k, t, wood="#8A6A3C"):
    """İniş tahtası: a = gemi küpeştesi, b = rıhtım kenarı; k 0..1 (0: dikine kaldırılmış, 1: yatmış). Tahta + iki korkuluk halatı + payandalar."""
    k = ease_io(k)
    # kaldırılmış konum: a'dan yukarı-geriye
    bx0 = a[0] + (b[0] - a[0]) * 0.18
    by0 = a[1] - 98.0
    bx = bx0 + (b[0] - bx0) * k
    by = by0 + (b[1] - by0) * k
    dx, dy = bx - a[0], by - a[1]
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    wd = 7.0
    quad = poly([(a[0] + nx * wd, a[1] + ny * wd), (bx + nx * wd, by + ny * wd), (bx - nx * wd, by - ny * wd), (a[0] - nx * wd, a[1] - ny * wd)])
    fink(c, quad, wood, 1.3, 255, 190)
    nsl = int(L / 14)
    for i in range(1, nsl):
        u = i / nsl
        c.drawLine(a[0] + dx * u + nx * wd, a[1] + dy * u + ny * wd, a[0] + dx * u - nx * wd, a[1] + dy * u - ny * wd, _P("#2A1A0C", 120, style="stroke", sw=1.2))
    if k > 0.85:
        ka = (k - 0.85) / 0.15
        for sgn in (-1.0, 1.0):
            pa = (a[0] + nx * sgn * 22 + 0, a[1] + ny * sgn * 22 - 24)
            pb = (bx + nx * sgn * 22 + 0, by + ny * sgn * 22 - 24)
            c.drawLine(pa[0], pa[1], pb[0], pb[1], _P("#6A5A3A", int(220 * ka), style="stroke", sw=1.6))
    # payanda (iki bağ halatı)
    c.drawLine(a[0] + dx * 0.5, a[1] + dy * 0.5, a[0] + dx * 0.5 + nx * 12, a[1] + dy * 0.5 + 40, _P("#6A5A3A", 130, style="stroke", sw=1.2)) if False else None


def draw_windmill(c, x, y, s, t, wind=1.0, seed=0, T=None):
    """Uzak yeldeğirmeni (tepe üstü): gövde + dönen dört kanat (kare kanat çerçevesi). Katman çerçevesinde."""
    T = T or (lambda col, d=0.0: col)
    body = poly([(x - 9 * s, y), (x + 9 * s, y), (x + 6 * s, y - 34 * s), (x - 6 * s, y - 34 * s)])
    fink(c, body, T("#D8CCA8", 0.4), 1.0, 255, 150)
    fink(c, poly([(x - 8 * s, y - 34 * s), (x, y - 46 * s), (x + 8 * s, y - 34 * s)]), T("#8E6A44", 0.4), 1.0, 255, 150)
    a0 = t * (0.55 + 0.35 * wind) + seed
    hx, hy = x, y - 36 * s
    for k in range(4):
        a = a0 + k * math.pi / 2
        ex, ey = hx + math.cos(a) * 34 * s, hy + math.sin(a) * 34 * s
        c.drawLine(hx, hy, ex, ey, _P(INK, 210, style="stroke", sw=max(1.0, 2.2 * s)))
        nx, ny = -math.sin(a), math.cos(a)
        sx, sy = hx + math.cos(a) * 12 * s, hy + math.sin(a) * 12 * s
        pth = poly([(sx, sy), (ex, ey), (ex + nx * 9 * s, ey + ny * 9 * s), (sx + nx * 9 * s, sy + ny * 9 * s)])
        c.drawPath(pth, _P(T("#EDE4CC", 0.4), 235))
        c.drawPath(pth, _P(INK, 150, style="stroke", sw=0.8))
    c.drawCircle(hx, hy, 2.6 * s, _P(INK, 255))


def draw_house_smoke(c, x, y, t, seed, tod, a=0.5, wind_dx=-30.0):
    """Baca dumanı: küçük yumuşak bulutlar (3–4 sprite) — ucuz."""
    for i in range(4):
        ph = (t * 0.16 + i / 4 + hash01(seed, i) * 0.1) % 1.0
        r = 8 + 20 * ph
        im = smoke_sprite(i % 4, tod, 0.0)
        p = skia.Paint()
        p.setAlphaf(clamp(a * (1 - ph) * math.sin(min(1.0, ph * 3.0) * math.pi / 2)))
        c.drawImageRect(im, skia.Rect.MakeWH(im.width(), im.height()), skia.Rect.MakeXYWH(x + wind_dx * ph + math.sin(t + i + seed) * 3 - r, y - ph * 70 - r, 2 * r, 2 * r), LIN, p)


def harbor_crane(ctx, x, yb, t, T, tod, wood="#7A5230", seed=3):
    """Çarklı liman vinci (çark + yürüyen adam, bom, yük bloğu): A-çerçeve direk, jib sola (denize doğru). Yük rıhtım yüzeyinden kalkar, sallanır, iner. Katman çerçevesinde (f=1)."""
    c = ctx.c
    f = ctx.f
    k, sgn = CB.hoist_cycle(t, 12.0, seed)
    k2, _ = CB.hoist_cycle(t + 0.05, 12.0, seed)
    omega = (k2 - k) / 0.05 * 150.0
    dk = "#3A2410"
    apex = (x, yb - 250)
    tip = (x - 190, yb - 218)
    for dx in (-34, 34):
        c.drawLine(x + dx, yb, apex[0] + dx * 0.10, apex[1], _P(dk, 235, style="stroke", sw=7.0))
        c.drawLine(x + dx, yb, apex[0] + dx * 0.10, apex[1], _P(T(wood, 0.0), 255, style="stroke", sw=4.4))
    c.drawLine(x - 30, yb - 90, x + 30, yb - 150, _P(T(wood, 0.0), 255, style="stroke", sw=2.8))
    c.drawLine(x + 30, yb - 90, x - 30, yb - 150, _P(T(wood, 0.0), 255, style="stroke", sw=2.8))
    c.drawLine(apex[0], apex[1], tip[0], tip[1], _P(dk, 235, style="stroke", sw=7.0))
    c.drawLine(apex[0], apex[1], tip[0], tip[1], _P(T(wood, 0.0), 255, style="stroke", sw=4.4))
    c.drawLine(x - 24, yb - 80, tip[0] + 26, tip[1] + 4, _P(T(wood, 0.0), 255, style="stroke", sw=3.0))
    R = 58.0
    wx, wy = x + 128, yb - 60
    CB.treadwheel(f, wx, wy, R, k * 150.0, omega, t, tod == "night", 1.0, seed=seed + 18)
    c.drawLine(wx - R * 0.1, wy - R * 0.1, apex[0] + 6, apex[1] + 3, _P("#6A5A3A", 215, style="stroke", sw=1.8))
    y_low = yb - 12
    y_hi = tip[1] + 56
    ly = y_low + (y_hi - y_low) * k
    sway = math.sin(t * 1.4 + seed) * 4.0 * min(1.0, k * 2.0) * (1 - 0.5 * abs(sgn))
    c.drawLine(tip[0], tip[1], tip[0] + sway, ly, _P("#6A5A3A", 235, style="stroke", sw=1.8))
    c.drawCircle(tip[0], tip[1], 6.0, _P(dk, 255))
    CB.load_block(c, tip[0] + sway, ly, 34.0, "brick" if int(t / 12.0 + seed) % 2 == 0 else "stone", 1.0)


STYLE_RICH = [dict(robe="#A8321E"), dict(robe="#233C8C"), dict(robe="#2E7A5A"), dict(robe="#7A2E56"), dict(robe="#C79A3C"), dict(robe="#1F5A7A")]


def person_style(variant, year, kind, i, rs):
    """Yöre/yıl kıyafeti: marsilya 1533 → bereli parlak Rönesans; 1600 → koyu, uzun şapkalı İspanyol modası; pera/livorno heyeti → sarık + uzun kaftan; diğerleri → öntanımlı karışım."""
    st = {}
    if variant == "pera" and kind in ("soylu", "tuccar", "halk", "asker"):
        st = dict(hat="turban", hat_col=["#EDE4CC", "#A8321E", "#2E6A4F", "#233C8C"][rs.randint(4)])
        if kind in ("soylu", "tuccar"):
            st["robe"] = ["#2E6A4F", "#A8321E", "#233C8C", "#7A2E56", "#C79A3C"][rs.randint(5)]
    elif variant == "marsilya" and year is not None:
        if year >= 1590 and kind in ("soylu", "tuccar", "soylu_f"):
            st = dict(robe=["#1E1A18", "#2A1F18", "#34261C", "#1E2438"][rs.randint(4)], hat_col="#1E1A18")
            if kind != "soylu_f":
                st["hat"] = "tall"
        elif kind in ("soylu", "tuccar", "soylu_f"):
            st = dict(robe=["#A8321E", "#233C8C", "#2E7A5A", "#7A2E56", "#C79A3C"][rs.randint(5)])
            if kind != "soylu_f":
                st["hat"] = "beret"
                st["hat_col"] = ["#A8321E", "#233C8C", "#1E1A18"][rs.randint(3)]
    return st


def make_quay_people(variant, year, x_land, n, seed, qx, side=1):
    """Rıhtım kalabalığı: iniş noktası çevresinde (±45 px koridor boş) n kişi; her biri dict(kind, x, y, h, st, ph, hop, amt0)."""
    rs = _RS(seed * 11 + 5)
    kinds = ["halk", "tuccar", "soylu", "soylu_f", "halk", "cocuk", "soylu", "halk", "tuccar", "soylu_f", "halk", "asker"]
    out = []
    for i in range(n):
        dx = rs.uniform(48, 430) * (1 if rs.rand() < 0.55 else -1)
        x = x_land + dx
        if x < qx + 40:
            x = x_land + abs(dx)
        kind = kinds[i % len(kinds)]
        y = rs.uniform(*QUAY_FEET)
        h = rs.uniform(86, 100) * (0.76 if kind == "cocuk" else 1.0) * (0.9 + 0.1 * (y - QUAY_FEET[0]) / (QUAY_FEET[1] - QUAY_FEET[0]))
        out.append(dict(kind=kind, x=x, y=y, h=h, st=person_style(variant, year, kind, i, rs), ph=rs.rand(), hop=rs.uniform(0.3, 0.9), seed=int(rs.randint(0, 999)), face=(1 if dx < 0 else -1)))
    out.sort(key=lambda d: d["y"])
    return out


def draw_people(ctx, people, t, t_wave, x_ship_fn=None):
    """Kalabalık: bekler → t_wave'den itibaren el sallar (cheer amount 0→1 yumuşak). Figürler gemiye (iniş noktasına) bakar."""
    f = ctx.f
    FA.set_scale_hint(ctx.z)
    amt = clamp((t - t_wave) / 1.4)
    for p in people:
        amount = ease_io(clamp((t - t_wave - p["ph"] * 0.9) / 1.2))
        try:
            if amount > 0.02:
                FA.actor(f, p["kind"], p["x"], p["y"], p["h"], t, action="cheer", dir=p["face"], seed=p["seed"], phase=p["ph"], amount=amount, hop=p["hop"] * amount, **p["st"])
            else:
                FA.actor(f, p["kind"], p["x"], p["y"], p["h"], t, action=("talk" if (int(p["seed"]) % 3 == 0) else "idle"), dir=p["face"], seed=p["seed"], phase=p["ph"], **p["st"])
        except Exception:
            pass
    FA.set_scale_hint(1.0)


# ═════════════════════════════ KÜÇÜK TEKNE ve KAYIK ═════════════════════════════
def tekne_hull(tod, liv, bs=1.0):
    """Küçük balıkçı/yük teknesi (yerel: ileri → +x; boy ≈190): yuvarlak karina, kıvrık baş, renkli kuşak."""
    key = ("tekne", tod, liv["wale"], liv["hull"], round(bs, 2))
    if key in _SPR:
        return _SPR[key]
    T = Tint(tod)

    def draw(c):
        p = skia.Path()
        p.moveTo(-90, -30)
        p.lineTo(90, -38)
        p.quadTo(106, -40, 100, -58)
        p.quadTo(98, -8, 66, 6)
        p.cubicTo(20, 12, -40, 12, -68, 4)
        p.quadTo(-98, -6, -90, -30)
        p.close()
        sh = skia.GradientShader.MakeLinear([(0, -40), (0, 10)], [C(mix(T(liv["hull"]), "#FFFFFF", 0.14)), C(T(liv["hull"])), C(mix(T(liv["hull"]), "#000000", 0.28))], [0.0, 0.55, 1.0])
        c.drawPath(p, skia.Paint(AntiAlias=True, Shader=sh))
        c.save()
        c.clipPath(p, skia.ClipOp.kIntersect, True)
        for off in (12, 22):
            c.drawLine(-100, -34 + off, 100, -40 + off, _P("#1A0E06", 80, style="stroke", sw=1.0))
        c.drawPath(poly([(-100, -34), (102, -42), (102, -34), (-100, -26)]), _P(T(liv["wale"])))
        c.drawLine(-100, -25, 102, -33, _P(T(liv["trim"]), 255, style="stroke", sw=1.6))
        c.restore()
        _lit(c, p, 46, 40)
        c.drawPath(p, _P(INK, 210, style="stroke", sw=1.8))

    spr = bake_local((-110, -64, 112, 18), bs, draw)
    _spr_put(key, spr)
    return spr


def draw_tekne(ctx, sea, S, t, x, y, s, dirn, sp, pitch):
    c = ctx.c
    liv = S.liv
    z = ctx.z
    bs = bucket(s * z)
    tod = ctx.tod
    T = Tint(tod)
    fl = getattr(ctx, "wind_dir", 1) * dirn
    wind = S.wind * getattr(ctx, "wind", 1.0)
    c.save()
    c.translate(x, y)
    c.rotate(pitch)
    c.scale(dirn * s, s)
    mm = T("#6A4A2C")
    _mast(c, 6, -34, -176, 5.0, 3.4, mm)
    _yard(c, 62, -38, -54, -172, 3.6, T("#7A5A34"))
    if S.crew and s * z * 190 > 90:
        draw_crew(ctx, S, [("denizci", -56, -28, "idle", 44, {}), ("halk", 14, -28, "work", 40, dict(mode="haul", period=1.7))], t, s, dirn)
    tekne_hull(tod, liv, bs).draw(c)
    if S.sails:
        sl = liv["sail"]
        lateen_sail(c, (62, -38), (-54, -172), (-50, -50), t, wind, ph=S.seed * 0.7, col=T(sl[0]), trim=T(sl[1]), dev=None, devcol=T(sl[3]), seed=S.seed)
    flag(c, 6, -180, 56, 14, t, "pennant", "plain", liv["pen"][0], liv["pen"][1], liv["pen"][1], wind=wind, ph=S.seed, flipx=1 if fl > 0 else -1)
    c.restore()
    return None


def kayik_hull(tod, liv, bs=1.0):
    """Kayık (İstanbul/Haliç): ince, iki ucu yükselen; yaldızlı kıvrım uçlar, renkli kuşak (yerel: ileri → +x; boy ≈210)."""
    key = ("kayik", tod, liv["wale"], liv["trim"], round(bs, 2))
    if key in _SPR:
        return _SPR[key]
    T = Tint(tod)

    def draw(c):
        p = skia.Path()
        p.moveTo(-104, -34)
        p.quadTo(0, -20, 104, -36)
        p.quadTo(118, -44, 114, -62)
        p.quadTo(104, -30, 80, -12)
        p.cubicTo(40, 6, -40, 6, -80, -6)
        p.quadTo(-108, -22, -104, -34)
        p.close()
        hull = T("#8A5A30")
        sh = skia.GradientShader.MakeLinear([(0, -40), (0, 8)], [C(mix(hull, "#FFFFFF", 0.18)), C(hull), C(mix(hull, "#000000", 0.28))], [0.0, 0.55, 1.0])
        c.drawPath(p, skia.Paint(AntiAlias=True, Shader=sh))
        c.save()
        c.clipPath(p, skia.ClipOp.kIntersect, True)
        c.drawLine(-110, -28, 112, -34, _P(T(liv["wale"]), 255, style="stroke", sw=7.0))
        c.drawLine(-110, -23, 112, -29, _P(T(liv["trim"]), 255, style="stroke", sw=2.0))
        for off in (6, 14):
            c.drawLine(-100, -20 + off, 100, -24 + off, _P("#1A0E06", 80, style="stroke", sw=1.0))
        c.restore()
        _lit(c, p, 46, 40)
        c.drawPath(p, _P(INK, 210, style="stroke", sw=1.8))
        for sx_, (a, b_) in ((1, (112, -62)), (-1, (-104, -50))):
            sc = skia.Path()
            sc.moveTo(a, b_)
            sc.cubicTo(a + sx_ * 10, b_ - 14, a + sx_ * 2, b_ - 24, a - sx_ * 4, b_ - 18)
            c.drawPath(sc, _P(T(liv["trim"]), 255, style="stroke", sw=3.0))

    spr = bake_local((-124, -90, 126, 14), bs, draw)
    _spr_put(key, spr)
    return spr


def draw_kayik(ctx, sea, S, t, x, y, s, dirn, sp, pitch):
    c = ctx.c
    liv = S.liv
    z = ctx.z
    bs = bucket(s * z)
    tod = ctx.tod
    c.save()
    c.translate(x, y)
    c.rotate(pitch)
    c.scale(dirn * s, s)
    if S.crew and s * z * 210 > 80:
        draw_crew(ctx, S, [("soylu", 30, -24, "idle", 46, dict(seed=0)), ("denizci", -46, -20, "idle", 44, {})], t, s, dirn)
    kayik_hull(tod, liv, bs).draw(c)
    c.restore()

    def late(cl):
        """İki kürek (yalnız yakın kenar): senkron çekiş; ripple noktaları döner."""
        wood = Tint(tod)("#9A6A3A")
        pts = []
        hz = 0.9 * (0.5 + 0.5 * clamp(sp / 40.0))
        for i, ox in enumerate((-30.0, 28.0)):
            u = (t * hz + 0.07 * i) % 1.0
            a, lf = _oar_pose(u)
            dx = 92.0 * math.sin(a * D2R)
            ty = 30.0 * math.cos(a * D2R) * (1.0 - 0.58 * lf) - 14.0 * lf
            oy = -26.0
            tx, tyy = ox + dx, ty
            cl.drawLine(ox, oy, tx, tyy, _P(INK, 190, style="stroke", sw=3.6))
            cl.drawLine(ox, oy, tx, tyy, _P(wood, 255, style="stroke", sw=2.2))
            L = math.hypot(tx - ox, tyy - oy) or 1.0
            nx, ny = (tx - ox) / L, (tyy - oy) / L
            px_, py_ = -ny, nx
            bx0, by0 = tx - nx * L * 0.22, tyy - ny * L * 0.22
            cl.drawPath(poly([(bx0 + px_ * 2.0, by0 + py_ * 2.0), (tx + px_ * 3.4, tyy + py_ * 3.4), (tx - px_ * 3.4, tyy - py_ * 3.4), (bx0 - px_ * 2.0, by0 - py_ * 2.0)]), _P(Tint(tod)("#C99B5A")))
            if lf < 0.5:
                pts.append((tx, tyy, clamp(u / 0.44)))
        return pts
    return late


KIND_DRAW["tekne"] = draw_tekne
KIND_DRAW["kayik"] = draw_kayik


def _hull_for(S, tod, bs):                                                   # noqa: F811  (kadırga/nao/tekne/kayık yansıması)
    if S.kind == "kadirga":
        return galley_hull(tod, S.liv, bs)
    if S.kind == "nao":
        return nao_hull(tod, S.liv, S.arms, bs)
    if S.kind == "tekne":
        return tekne_hull(tod, S.liv, bs)
    if S.kind == "kayik":
        return kayik_hull(tod, S.liv, bs)
    return None


# ═════════════════════════════ ÇEKİM TÜRÜ: liman ═════════════════════════════
_HARBORS = {}
LIMAN_CAMS = [(0.0, (770.0, 24.0, 1.0)), (0.40, (900.0, 12.0, 1.05)), (0.78, (1120.0, -6.0, 1.18)), (1.0, (1220.0, -16.0, 1.28))]      # marsilya 1533 = 1600: AYNI kamera yolu (kesir tabanlı)
DEPART_CAMS = [(0.0, (1200.0, 20.0, 1.20)), (0.45, (1090.0, 10.0, 1.10)), (1.0, (900.0, -8.0, 1.0))]
LIMAN_POLES = {"marsilya": (840.0, 1760.0, 2540.0), "napoli": (920.0, 1620.0, 2400.0), "livorno": (760.0, 1700.0, 2600.0), "pera": (760.0, 1500.0, 2200.0), "generic": (800.0, 1600.0, 2400.0)}
LIMAN_CRANE = {"marsilya": 2120.0, "napoli": 2060.0, "livorno": 2420.0, "pera": 1700.0, "generic": 2200.0}


def _harbor(variant, tod, year):
    yc = "y0"
    if variant == "pera" and year:
        yc = "y1" if year < 1500 else ("y2" if year < 1574 else "y3")
    key = (variant, tod, yc)
    h = _HARBORS.get(key)
    if h is None:
        if len(_HARBORS) > 3:
            _HARBORS.clear()                                  # bellek: aynı anda ≤4 liman katman takımı
            _IMGS.clear()
        h = _HARBORS[key] = Harbor(variant, tod, year)
    return h


def _hero_defaults(variant, year):
    y = year or 0
    if variant == "marsilya":
        return dict(kind="kadirga", flag="papalik" if y < 1590 else "toskana", highlight=(y >= 1590), mode="arrive", dir=1)
    if variant == "napoli":
        return dict(kind="kadirga", flag="toskana", highlight=False, mode="arrive", dir=1)
    if variant == "livorno":
        return dict(kind="kadirga", flag="osmanli", highlight=False, mode="arrive", dir=1)
    if variant == "pera":
        return dict(kind="nao", flag="toskana", highlight=False, mode="depart", dir=-1)
    return dict(kind="nao", flag="genel", highlight=False, mode="arrive", dir=1)


def _liman(cx, variant="generic", year=None, tod=None, ship=None, followers=0, cams=None, kick=None, caption=None, at=0.0, frame=True, seed=1, band=None, name=None, labels=None,
           crowd=14, delegation=None, x_dock=None, t_dock=None, wave_at=None, extra_ships=None, ambient=True, stamp=True, wind=1.0, wind_dir=-1, swell=0.8, foam=0.5, birds=5, clouds=7, sun=None, **kw):
    """Liman çekimi. variant: marsilya | pera | napoli | livorno | generic; year: yıl damgası (+ kıyafet/ışık ayrımı). ship=dict(...): hero gemi (yoksa varyanta özgü);
    mode "arrive": gemi soldan gelir → yanaşır (kürekler kaldırılır, halat atılır, tahta iner, kalabalık el sallar); "depart": ters (halat çözülür, tahta kalkar, gemi ayrılır).
    x_dock/t_dock: yanaşma konumu/anı (çapa olabilir). followers: arkadan gelen/giden ek kadırga sayısı. delegation=dict(side='osmanli', n=5, t0=…): rıhtımda yürüyen heyet (+ mektup rulosu).
    marsilya için 1533 ve 1600 AYNI kadraj/kamera yolunu paylaşır: yalnız yıl damgası, bayrak, kıyafet, gemi tipi ve ışık değişir."""
    f = cx.f
    dur = max(cx.dur, 1e-3)
    band = band or (BAND if frame else (0, 800))
    v = variant if variant in ("marsilya", "pera", "napoli", "livorno", "generic") else "generic"
    year_txt = None                                  # damga metni (parametre olduğu gibi); mantık için sayısal yıl
    if isinstance(year, str):
        year_txt = year.strip() or None
        _ys = re.findall(r"\d{4}", year)
        year = int(_ys[-1]) if _ys else None
    elif year is not None:
        year = int(year)
        year_txt = str(year)
    if tod is None:
        tod = "night" if not TH.day else ("dusk" if (v == "marsilya" and (year or 0) >= 1590) else "day")
    H_ = _harbor(v, tod, year)
    hd = _hero_defaults(v, year)
    sh = dict(hd)
    if ship:
        sh.update(ship)
    mode = sh.pop("mode", "arrive")
    qx = H_.quay_x0
    dirn = int(sh.pop("dir", hd["dir"]))
    if x_dock is None:
        m = round((1250.0 - (qx + 90 + 165)) / 330.0)
        x_dock = qx + 90 + 165 + 330 * m
        if dirn < 0:
            x_dock = qx + 90 + 165 + 330 * (m + 1)
    x_dock = float(x_dock)
    td = _tcall(cx, t_dock, None) if t_dock is not None else (dur * 0.60 if mode == "arrive" else dur * 0.30)
    kind = KIND_ALIAS.get(sh.pop("kind", hd["kind"]), "kadirga")
    scale = float(sh.pop("scale", 0.92 if kind == "kadirga" else 0.86))
    t0 = _tcall(cx, sh.pop("t0", 0.0), 0.0)
    if mode == "arrive":
        x0 = float(sh.pop("x0", -260.0 if dirn > 0 else 2300.0))
        sp_d = dict(kind=kind, x0=x0, x1=x_dock, t0=t0, t1=td, ease="out", y=SHIP_Y, scale=scale, dir=dirn, sails=(False if kind == "kadirga" else True), crew=True, highlight=sh.pop("highlight", False), flag=sh.pop("flag", "genel"))
        t_off_start = td - 2.0
        sp_d["oars"] = (lambda t, td=td: 0.0 if t < td - 2.2 else (ease_io((t - (td - 2.2)) / 1.1)))
        sp_d["sail_set"] = (lambda t, td=td: 1.0 - 0.88 * ease_io((t - (td - 3.6)) / 2.2))
        if kind != "kadirga":
            sp_d["sails"] = True
    else:
        tl = _tcall(cx, sh.pop("t_leave", None), td) if sh.get("t_leave") is not None else td
        x1 = float(sh.pop("x1", -700.0 if dirn < 0 else 2700.0))
        sp_d = dict(kind=kind, x0=x_dock, x1=x1, t0=tl, t1=tl + (dur - tl) * 0.98, ease="in", y=SHIP_Y, scale=scale, dir=dirn, sails=(False if kind == "kadirga" else True), crew=True, highlight=sh.pop("highlight", False), flag=sh.pop("flag", "genel"))
        sp_d["oars"] = (lambda t, tl=tl: 1.0 if t < tl - 0.2 else (1.0 - ease_io((t - (tl - 0.2)) / 0.9)))
        sp_d["sail_set"] = (lambda t, tl=tl: 0.14 + 0.86 * ease_io((t - tl) / 2.4))
        td = tl
    sp_d.update({k_: v_ for k_, v_ in sh.items() if k_ not in ("t_leave",)})
    hero = ShipSpec(sp_d, cx, dur, 0)
    ships = [hero]
    for i in range(int(followers)):
        d2 = dict(sp_d)
        d2.update(y=SHIP_Y - 12.0 - 13.0 * (i % 3), scale=scale * (0.9 - 0.04 * (i % 3)), seed=7 + i * 5, crew=False, highlight=False, flag=sp_d.get("flag"), lod=True, sails=False)
        lag = 0.9 * (i + 1)
        if mode == "arrive":
            d2.update(x0=sp_d["x0"] - dirn * 560 * (i + 1), x1=x_dock - dirn * 600 * (i + 1), t0=t0 + lag * 0.5, t1=td + lag * 0.6)
            d2["oars"] = (lambda t, tt=td + lag * 0.6: 0.0 if t < tt - 2.2 else ease_io((t - (tt - 2.2)) / 1.1))
        else:
            d2.update(x0=x_dock - dirn * 600 * (i + 1) * 0.0 - dirn * 560 * (i + 1), x1=sp_d["x1"] + dirn * 0, t0=sp_d["t0"] + lag, t1=sp_d["t1"] + lag * 0.5)
            d2["oars"] = True
        ships.append(ShipSpec(d2, cx, dur, 10 + i))
    # arka plan gemileri: açık suda demirli/yelken (ufka yakın)
    if ambient:
        bgs = _harbor_bg_ships(v, year, qx, tod)
        ships += _norm_ships(cx, bgs, dur)
    ships += _norm_ships(cx, extra_ships or [], dur)
    t_wave = _tcall(cx, wave_at, None) if wave_at is not None else (td - 2.6 if mode == "arrive" else td - 2.4)
    dock_dir = dirn
    x_land = x_dock + dock_dir * 92.0
    people = make_quay_people(v, year, x_land, int(crowd), seed + (year or 0) % 17, qx)
    cfg = dict(tod=tod, seed=seed, wind=wind, wind_dir=wind_dir, swell=swell, foam=foam, horizon=YH_L, sun=sun if sun is not None else ((1560, 170, 46) if tod == "day" else None), glitter=0.0 if tod != "dusk" else 0.7,
               birds=birds, clouds=clouds, rays=True, fore=True, at=at, fore_y=(792.0,), cloud_y=(40, 250))
    if v == "napoli" and tod == "day" and sun is None:
        cfg["sun"] = (260, 170, 46)
    sea = get_sea(tod, YH_L, seed, swell, foam, wind_dir, 1.0)
    k0 = sea.row_before(WALL_BOT + 2.0)
    T = H_.T
    state = {"mid": False}
    cranex = LIMAN_CRANE[v]
    # rıhtım bayrak direkleri (yıla göre bayrak)
    poles = []
    for px in LIMAN_POLES[v]:
        poles.append(px)
    fl_col = _quay_flag(v, year)
    por_rs = _RS(seed * 5 + 3)
    porters = [dict(x0=qx + 120 + i * 560 + por_rs.uniform(0, 200), v=por_rs.choice([-1, 1]) * por_rs.uniform(26, 38), y=por_rs.uniform(474, 484), kind=["halk", "tuccar", "halk", "banker"][i % 4], prop=["sack", "basket", "sack", "book"][i % 4], seed=40 + i) for i in range(4)]
    deleg = delegation

    def pre(ctx, sea_):
        c = ctx.c
        ctx.push(0.30)
        blit_layer(c, H_.far)
        for (mx, my, ms) in H_.mills:
            draw_windmill(c, mx, my, ms / 38.0, ctx.t, ctx.wind, mx * 0.01, T)
        ctx.pop()

    def mid(ctx, sea_, k):
        if k != k0 or state["mid"]:
            return
        state["mid"] = True
        c = ctx.c
        t = ctx.t
        # yapı katmanı (f=0,82) + bayrak/duman/yeldeğirmeni
        ctx.push(0.82)
        blit_layer(c, H_.bld)
        if ambient:
            for fg in H_.flags:
                if ctx.visible(0.82, fg["x"] - 120, fg["x"] + 160, 20):
                    c.drawLine(fg["x"], fg["y"] + 74, fg["x"], fg["y"] - 4, _P(INK, 220, style="stroke", sw=4.2))
                    c.drawLine(fg["x"], fg["y"] + 74, fg["x"], fg["y"] - 4, _P(T("#8A6A3C"), 255, style="stroke", sw=2.4))
                    flag(c, fg["x"], fg["y"], fg["w"], fg["h"], t, fg["shape"], fg["dev"], fg["c1"], fg["c2"], fg["c3"], wind=ctx.wind, ph=fg["x"] * 0.013, flipx=1 if ctx.wind_dir > 0 else -1)
            for i, (kd, sx, sy) in enumerate(H_.smokes):
                if ctx.visible(0.82, sx - 80, sx + 80, 20):
                    if kd == "fanal":
                        glow(c, sx, sy + 8, 46, "#FFC060", 0.5 + 0.12 * math.sin(t * 7 + i)) if tod != "day" else None
                    else:
                        draw_house_smoke(c, sx, sy, t, i, tod, 0.50 if tod != "night" else 0.30, -26.0 * (1 if ctx.wind_dir < 0 else -1))
        ctx.pop()
        # rıhtım (f=1)
        ctx.push(1.0)
        blit_layer(c, H_.quay)
        # direk bayrakları
        if ambient:
            for px in poles:
                if ctx.visible(1.0, px - 100, px + 130, 20):
                    c.drawLine(px, PAVE_TOP + 16, px, PAVE_TOP - 190, _P(INK, 220, style="stroke", sw=5.2))
                    c.drawLine(px, PAVE_TOP + 16, px, PAVE_TOP - 190, _P(T("#8A6A3C"), 255, style="stroke", sw=3.2))
                    c.drawCircle(px, PAVE_TOP - 192, 4.2, _P(T("#C79A3C")))
                    flag(c, px, PAVE_TOP - 188, 96, 60, t, "swallow", fl_col[0], fl_col[1], fl_col[2], fl_col[3], wind=ctx.wind, ph=px * 0.011, flipx=1 if ctx.wind_dir > 0 else -1)
            if ctx.visible(1.0, cranex - 330, cranex + 220, 20):
                harbor_crane(ctx, cranex, PAVE_TOP + 22, t, T, tod, seed=3)
        # taşıyıcılar (rıhtım boyunca yürür)
        FA.set_scale_hint(ctx.z)
        xa, xb = ctx.view(1.0, 60)
        for p in porters:
            span = 1500.0
            xx = qx + 60 + ((p["x0"] - qx - 60 + p["v"] * t) % span)
            if xx < xa - 60 or xx > xb + 60:
                continue
            try:
                FA.walker(f, p["kind"], xx, p["y"], 78, t, speed=abs(p["v"]), dir=1 if p["v"] > 0 else -1, phase=p["seed"] * 0.13 % 1.0, seed=p["seed"], prop=p["prop"], **person_style(v, year, p["kind"], p["seed"], _RS(p["seed"])))
            except Exception:
                pass
        # heyet (livorno / pera): yürüyüş → duruş → selam; mektup rulosu
        if deleg:
            _draw_delegation(ctx, f, deleg, x_land, dock_dir, t, td, qx, v, year, seed)
        # kalabalık + iskele işçileri
        if ctx.visible(1.0, x_land - 520, x_land + 520, 40):
            draw_people(ctx, people, t, t_wave)
            _draw_dockers(ctx, f, hero, sea_, t, td, mode, dock_dir, qx)
        FA.set_scale_hint(1.0)
        ctx.pop()
        # rıhtım dibi su köpüğü
        ru = sea_.row_of(WALL_BOT)
        ctx.push(ru.f)
        xa2, xb2 = ctx.view(ru.f, 60)
        sea_.skirt(ctx, ru, max(xa2, qx - 10), xb2, WALL_BOT + 2.0, t, depth=14.0)
        ctx.pop()

    th_spec = None
    if kw.get("thread"):
        th_spec = ShipSpec(dict(kind="tekne", route=[(sp_d["x0"] - 1100.0 * dirn, SHIP_Y + 16.0), (x_dock - dirn * 40.0, SHIP_Y + 16.0)], t0=sp_d["t0"], t1=sp_d["t1"], ease="out"), cx, dur, 99)
        th_spec.ease = "out"

    def post(ctx, sea_):
        t = ctx.t
        c = ctx.c
        _draw_moorings(ctx, c, hero, sea_, t, td, mode, dock_dir, qx, x_dock)
        if th_spec is not None and mode == "arrive":
            draw_route_thread(ctx, sea_, th_spec, t, kw.get("thread") if isinstance(kw.get("thread"), dict) else {})

    ship_fn = lambda ctx, sea_, S, t: (render_fleet_ship(ctx, sea_, S, t, force=True) if (S.extra.get("lod") and S.kind == "kadirga") else render_ship(ctx, sea_, S, t))
    cams_use = cams
    ctx_, sea_ = render_sea_scene(cx, f, cfg, ships, band, cams_use, (LIMAN_CAMS if mode == "arrive" else DEPART_CAMS), "liman", pre=pre, post=post, mid=mid, ship_fn=ship_fn)
    # etiketler
    def decor(f_, cx_, band_):
        by0, bh = band_
        if stamp and year_txt:
            txt = year_txt
            wd = sk.text_width(txt, "title_m", 56, 6) + 78
            CM.tablet(f_, 92, by0 + bh - 112, wd, 82, alpha=cx_.amt(at + 0.5, 0.7), corner=10)
            CM.ink(f_, txt, 92 + wd / 2, by0 + bh - 112 + 58, face="title_m", size=56, color=TH.fg, align="c", track=6, alpha=cx_.amt(at + 0.5, 0.7), emboss=False)
        if name:
            _label_plate(f_, cx_, name, W / 2, by0 + 92, at + 0.6, 40)
    _deco_labels(f, cx, ctx_, sea_, labels, at)
    _frame_decor(f, cx, band, 1.0, kick, caption, at, extra=decor)
    _finish(f, cx, tod, seed, motes=26)


def _quay_flag(v, year):
    y = year or 0
    if v == "marsilya":
        return ("lily", "#233C8C", "#E0B84E", "#E0B84E") if y < 1590 else ("lily", "#F4EEDC", "#E0B84E", "#E0B84E")
    if v == "napoli":
        return ("plain", "#F4EEDC", "#B33620", "#B33620")
    if v == "livorno":
        return ("medici", "#E0B84E", "#B33620", "#B33620")
    if v == "pera":
        return ("crescent", "#A8321E", "#E0B84E", "#E0B84E")
    return ("stripes", "#233C8C", "#E0B84E", "#E0B84E")


def _harbor_bg_ships(v, year, qx, tod):
    """Açık suda (rıhtımdan önceki boşluk) demirli/yelkenli arka plan gemileri."""
    liv = {"marsilya": ("fransa", "hristiyan"), "napoli": ("hristiyan", "papalik"), "livorno": ("toskana", "osmanli"), "pera": ("osmanli", "hristiyan"), "generic": ("genel", "genel")}[v]
    out = [dict(kind="nao", x0=qx - 230, y=432, scale=0.9, flag=liv[0], dir=1, speed=0.0, oars=False, crew=False, seed=11, sails=False),
           dict(kind="kadirga", x0=qx - 470, y=480, scale=0.8, flag=liv[1], dir=-1, speed=0.0, oars=False, crew=False, seed=12, sails=False, ensign=False)]
    if v == "pera":
        out += [dict(kind="kayik", x0=qx - 120, y=560, scale=0.8, flag="osmanli", dir=1, x1=qx + 420, t0=0.0, t1=14.0, ease="lin", crew=True, seed=21),
                dict(kind="kayik", x0=qx - 20, y=585, scale=0.76, flag="osmanli", dir=-1, x1=qx - 700, t0=0.0, t1=16.0, ease="lin", crew=True, seed=22)]
    elif v in ("marsilya", "livorno", "napoli"):
        out += [dict(kind="tekne", x0=qx - 160, y=545, scale=0.8, flag="genel", dir=1, x1=qx + 200, t0=0.0, t1=16.0, ease="lin", seed=31)]
    return out


def _draw_dockers(ctx, f, hero, sea, t, td, mode, dirn, qx):
    """İskele işçileri: halat başında bekler → halat atılınca çeker (work haul)."""
    L = KIND_LEN[hero.kind] * hero.scale * persp(hero.y, sea.yh)
    xs = [hero.pos(td)[0] + dirn * L * 0.34, hero.pos(td)[0] - dirn * L * 0.34]
    for i, bx in enumerate(xs):
        bx = qx + 90 + 330 * round((bx - (qx + 90)) / 330.0)
        for j in range(2):
            try:
                pulling = (t > td - (1.6 if i == 0 else 1.0)) and (t < td + 4.5 if mode == "arrive" else t < td + 0.2)
                if pulling:
                    FA.actor(f, "halk" if j == 0 else "denizci", bx + (j * 30 - 15) * (-dirn), 494 + j * 5, 90, t, action="work", dir=dirn if i == 0 else -dirn, seed=70 + i * 3 + j, phase=0.35 * j, mode="haul", period=1.5)
                else:
                    FA.actor(f, "halk" if j == 0 else "denizci", bx + (j * 30 - 15) * (-dirn), 494 + j * 5, 90, t, action="idle", dir=dirn if i == 0 else -dirn, seed=70 + i * 3 + j, phase=0.35 * j)
            except Exception:
                pass


def _draw_moorings(ctx, c, hero, sea, t, td, mode, dirn, qx, x_dock):
    """Halatlar (baş/kıç) ve iniş tahtası: gemi ve rıhtım noktaları arasında (gemi çizildikten SONRA)."""
    kind = hero.kind
    if kind == "kadirga":
        bow_l, stern_l, plank_l = (258.0, -66.0), (-250.0, -112.0), (-40.0, -52.0)
    else:
        bow_l, stern_l, plank_l = (204.0, -138.0), (-196.0, -198.0), (-30.0, -90.0)
    pb = ship_point(sea, hero, t, bow_l[0], bow_l[1])
    ps_ = ship_point(sea, hero, t, stern_l[0], stern_l[1])
    pk = ship_point(sea, hero, t, plank_l[0], plank_l[1])
    L = KIND_LEN[kind] * hero.scale * persp(hero.y, sea.yh)
    bx_bow = qx + 90 + 330 * round((x_dock + dirn * L * 0.34 - (qx + 90)) / 330.0)
    bx_str = qx + 90 + 330 * round((x_dock - dirn * L * 0.34 - (qx + 90)) / 330.0)
    q_bow = (bx_bow, EDGE - 22.0)
    q_str = (bx_str, EDGE - 22.0)
    q_land = (x_dock + dirn * 92.0, EDGE - 4.0)
    ctx.push(1.0)
    if mode == "arrive":
        ub = (t - (td - 1.7)) / 1.0
        us = (t - (td - 1.1)) / 1.0
        kp = (t - (td - 0.3)) / 1.3
    else:
        ub = 1.0 - (t - (td - 1.3)) / 1.0
        us = 1.0 - (t - (td - 0.9)) / 1.0
        kp = 1.0 - (t - (td - 2.2)) / 1.3
    if ub > 0.001:
        rope_throw(c, (pb[0], pb[1]), q_bow, ub, t, 80.0)
    if us > 0.001:
        rope_throw(c, (ps_[0], ps_[1]), q_str, us, t, 70.0)
    if kp > 0.001:
        draw_plank(c, (pk[0], pk[1]), q_land, kp, t, Tint(ctx.tod)("#8A6A3C"))
    ctx.pop()


def _draw_delegation(ctx, f, d, x_land, dirn, t, td, qx, v, year, seed):
    """Rıhtımda yürüyen heyet: sarıklı/uzun kaftanlı figürler (saygılı), önde mektup rulosu; iniş noktasına varınca durup selam verir."""
    n = int(d.get("n", 5))
    side = d.get("side", "osmanli")
    t0 = _tcall(ctx.cx, d.get("t0", 0.0), 0.0)
    x_stop = float(d.get("x_stop", x_land + dirn * 0.0 - 120.0))
    x_from = float(d.get("x_from", x_stop - 330.0))
    sp = 44.0
    c = ctx.c
    rs = _RS(seed * 3 + 1)
    for i in range(n):
        xi = x_from + i * 46.0
        xs = x_stop + i * 46.0 - (n - 1) * 46.0 * 0.0
        tt = t - t0
        x = min(xs, xi + sp * max(0.0, tt)) if tt > 0 else xi
        moving = x < xs - 0.5 and tt > 0
        kind = "soylu" if i < 2 else ("asker" if i == n - 1 else "halk")
        st = dict(hat="turban", hat_col=["#EDE4CC", "#A8321E", "#2E6A4F"][i % 3], robe=["#2E6A4F", "#233C8C", "#A8321E", "#7A2E56", "#1F5A7A"][i % 5], robe2="#E0B84E") if side == "osmanli" else {}
        y = 494.0 + (i % 2) * 5
        try:
            if moving:
                FA.walker(ctx.f, kind, x, y, 74, t, speed=sp, dir=1, phase=0.2 * i, seed=300 + i, **st)
            else:
                FA.actor(ctx.f, kind, x, y, 74, t, action=("bow" if i == 0 else "idle"), dir=1, seed=300 + i, phase=0.2 * i, t0=max(0.2, td - 0.5 - t0) if False else 0.4, **st)
        except Exception:
            pass
        if i == 0:                                   # mektup rulosu (el hizasında): krem silindir + kırmızı bağ
            hx, hy = x + 20.0, y - 74 * 0.52 + (math.sin(t * 6.0) * 1.6 if moving else 0.0)
            c.save()
            c.translate(hx, hy)
            c.rotate(-18)
            rr = skia.Rect.MakeLTRB(-14, -4, 14, 4)
            c.drawRoundRect(rr, 4, 4, _P("#EFE4C6"))
            c.drawRoundRect(rr, 4, 4, _P(INK, 190, style="stroke", sw=1.1))
            c.drawRect(skia.Rect.MakeLTRB(-2, -4.5, 2.5, 4.5), _P("#B33620"))
            c.restore()


@ckind("liman")
def k_liman(cx, **kw):
    return _liman(cx, **kw)


def draw_route_thread(ctx, sea, S, t, opt):                     # noqa: C901
    """Rota ipliği (c13 'iplik'): geminin kat ettiği yol boyunca denizin üstüne ince, yaldız-mürekkep kesik çizgi; gemiyle birlikte uzar. opt: col, w, dash, ahead (0..1: yolun tamamı soluk gösterilir)."""
    if not S.route:
        return
    Q, cum = S._rb
    u_now = clamp((t - S.t0) / max(1e-6, (S.t1 - S.t0))) if S.t1 is not None else 1.0
    u_now = _ease(S.ease if S.ease != "lin" else "io", u_now)
    n = len(Q)
    k_end = max(2, int(np.searchsorted(cum, u_now * cum[-1])))
    col = opt.get("col", "#E0B84E")
    w = opt.get("w", 3.0)
    c = ctx.c
    ymid = float(np.mean(Q[:, 1]))
    fr = sea.row_of(ymid).f
    ctx.push(fr)
    dash = skia.DashPathEffect.Make([12.0, 9.0], -t * 14.0)
    pts = [(float(a), float(b) + 8.0) for a, b in Q[:k_end]]
    if len(pts) >= 2:
        pth = skia.Path.Polygon(pts, False)
        p1 = _P(INK, 150, style="stroke", sw=w + 1.6, cap=skia.Paint.kButt_Cap)
        p1.setPathEffect(dash)
        c.drawPath(pth, p1)
        p2 = _P(col, 255, style="stroke", sw=w, cap=skia.Paint.kButt_Cap)
        p2.setPathEffect(dash)
        c.drawPath(pth, p2)
    if opt.get("ahead", 0.28) > 0 and k_end < n - 1:
        pts2 = [(float(a), float(b) + 8.0) for a, b in Q[k_end - 1:]]
        pth2 = skia.Path.Polygon(pts2, False)
        p3 = _P(col, int(255 * opt.get("ahead", 0.28)), style="stroke", sw=w * 0.7, cap=skia.Paint.kButt_Cap)
        p3.setPathEffect(skia.DashPathEffect.Make([4.0, 14.0], 0.0))
        c.drawPath(pth2, p3)
    ctx.pop()
