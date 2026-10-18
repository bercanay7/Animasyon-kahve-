"""Skia tabanlı çizim çekirdeği (Şarlken uzun dosyası) — 1920×1080, 24 fps.

Bu modül: renkler/yazı tipleri, `Frame` (Skia yüzeyi + yardımcılar), kabartma (relief) sprite üretimi, gürültü dokuları,
ışık/toz/duman efektleri, kolay hareket fonksiyonları. Şablonlar (shots_*.py) yalnızca bunu kullanır.
Hız kuralı: durağan/ağır şeyleri `cache`'e al (sprite), kare başına yalnız dönüşüm + alfa uygula.
"""
import math
import os
from functools import lru_cache

import cv2
import numpy as np
import skia
import uharfbuzz as hb

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "fonts")
W, H = 1920, 1080
FPS = 24


# ───────────────────────────── renk ─────────────────────────────
def C(h, a=255):
    """'#RRGGBB' veya (r,g,b) → skia renk."""
    if isinstance(h, str):
        h = h.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    else:
        r, g, b = h[:3]
    return skia.Color(int(r), int(g), int(b), int(a))


def rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def mix(a, b, t):
    ra, rb = rgb(a), rgb(b)
    return "#%02X%02X%02X" % tuple(int(round(x + (y - x) * t)) for x, y in zip(ra, rb))


PAL = dict(
    INK="#150D08", UMBER="#24160D", UMBER2="#3A2415", SEPIA="#5C3B22", BROWN="#7A5230",
    GOLD="#C9962B", GOLD_L="#F0D27A", GOLD_D="#7A5518", GOLD_DD="#4A3210",
    PARCH="#EADCB5", PARCH_L="#F6EDD0", PARCH_D="#CDB88A", PARCH_DD="#9C8559",
    CRIMSON="#8E1F26", CRIMSON_L="#C0392B", CRIMSON_D="#561016",
    ROYAL="#27427A", ROYAL_L="#4B6DB5", TEAL="#1E5560", TEAL_L="#3F8C96", FOREST="#2F5232", FOREST_L="#5A8A52",
    VIOLET="#4B2D63", VIOLET_L="#7D5A9E", ORANGE="#C2682A", BONE="#E8E0CC", SEA_D="#0E1A24", SEA="#16293A", SEA_L="#27455C",
    WHITE="#FFFFFF", BLACK="#000000",
)
P = PAL

# fraksiyon renkleri (haritada kim kimdir)
FAC = dict(
    habsburg=("#8E1F26", "#E8C25A"), ispanya=("#9A2430", "#E8C25A"), burgonya=("#7B1E2B", "#E8C25A"), avusturya=("#A33A2E", "#F0E0B0"),
    fransa=("#27427A", "#F0D27A"), osmanli=("#2F6B4A", "#E8D8A0"), papalik=("#D4B64E", "#3A2A10"), protestan=("#1E5560", "#F6EDD0"),
    venedik=("#2F7A8A", "#F6EDD0"), ingiliz=("#A8352C", "#F6EDD0"), portekiz=("#2D5A8E", "#F6EDD0"), macar=("#6A7A38", "#F6EDD0"),
    nötr=("#5C3B22", "#CDB88A"),
)

# ───────────────────────────── yazı tipleri ─────────────────────────────
FONT_FILES = dict(
    title="Cinzel_700Bold.ttf", title_m="Cinzel_600SemiBold.ttf", title_l="Cinzel_400Regular.ttf",
    cap="CormorantGaramond_600SemiBold.ttf", cap_b="CormorantGaramond_700Bold.ttf", cap_m="CormorantGaramond_500Medium.ttf",
    cap_i="CormorantGaramond_600SemiBold_Italic.ttf", cap_il="CormorantGaramond_400Regular_Italic.ttf",
    body="EBGaramond_500Medium.ttf", body_i="EBGaramond_400Regular_Italic.ttf",
    map="IMFellEnglish_400Regular.ttf", map_i="IMFellEnglish_400Regular_Italic.ttf",
    fell="IMFellDWPica_400Regular.ttf", fell_i="IMFellDWPica_400Regular_Italic.ttf",
)
_TF, _HB = {}, {}


def _typeface(name):
    if name not in _TF:
        _TF[name] = skia.Typeface.MakeFromFile(os.path.join(FD, FONT_FILES[name]))
    return _TF[name]


def _hbfont(name):
    if name not in _HB:
        data = open(os.path.join(FD, FONT_FILES[name]), "rb").read()
        face = hb.Face(data)
        font = hb.Font(face)
        _HB[name] = (font, face.upem)
    return _HB[name]


@lru_cache(maxsize=4096)
def _shape(name, text, size, track):
    """HarfBuzz ile kernlu konumlar: (glyph id'leri, x konumları, toplam genişlik)."""
    font, upem = _hbfont(name)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"liga": False, "clig": False, "kern": True})
    sc = size / upem
    xs, gl, x = [], [], 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gl.append(info.codepoint)
        xs.append(x + pos.x_offset * sc)
        x += pos.x_advance * sc + track
    return tuple(gl), tuple(xs), x - (track if gl else 0.0)


def text_width(text, face, size, track=0.0):
    return _shape(face, text, float(size), float(track))[2]


@lru_cache(maxsize=2048)
def _blob(face, text, size, track):
    gl, xs, wid = _shape(face, text, float(size), float(track))
    font = skia.Font(_typeface(face), size)
    font.setSubpixel(True)
    font.setHinting(skia.FontHinting.kNone)
    b = skia.TextBlobBuilder()
    b.allocRunPosH(font, list(gl), list(xs), 0)
    return b.make(), wid


def text_blob(face, text, size, track=0.0):
    return _blob(face, text, float(size), float(track))


def wrap_text(text, face, size, max_w, track=0.0):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_width(t, face, size, track) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


# ───────────────────────────── kolay hareket ─────────────────────────────
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, t):
    return a + (b - a) * t


def smooth(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def smoother(t):
    t = clamp(t)
    return t * t * t * (t * (t * 6 - 15) + 10)


def ease_out(t, p=3):
    return 1 - (1 - clamp(t)) ** p


def ease_in(t, p=3):
    return clamp(t) ** p


def ease_io(t, p=3):
    t = clamp(t)
    return 0.5 * (2 * t) ** p if t < 0.5 else 1 - 0.5 * (2 * (1 - t)) ** p


def back_out(t, s=1.70158):
    t = clamp(t) - 1
    return t * t * ((s + 1) * t + s) + 1


def pulse(t, a, b, fade=0.3):
    """a..b arasında 1, kenarlarda fade sn'de yumuşak geçiş."""
    return smooth((t - a) / fade) * (1 - smooth((t - b) / fade)) if b is not None else smooth((t - a) / fade)


def seg(t, a, b):
    """[a,b] aralığında 0→1."""
    return clamp((t - a) / max(1e-6, b - a))


# ───────────────────────────── dokular (numpy) ─────────────────────────────
@lru_cache(maxsize=32)
def noise_tex(w, h, scale, octaves, seed):
    """0..1 float32 çok oktavlı değer gürültüsü (cv2 ile hızlı)."""
    rs = np.random.RandomState(seed)
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        s = max(2, int(scale / (2 ** o)))
        gh, gw = max(2, h // s + 2), max(2, w // s + 2)
        g = rs.rand(gh, gw).astype(np.float32)
        up = cv2.resize(g, (gw * s, gh * s), interpolation=cv2.INTER_CUBIC)[:h, :w]
        out += up * amp
        tot += amp
        amp *= 0.5
    out /= tot
    out = (out - out.min()) / (out.max() - out.min() + 1e-6)
    return out


def np_to_image(arr):
    """uint8 (H,W,4 RGBA, premultiplied olmayan) → skia.Image."""
    a = np.ascontiguousarray(arr)
    if a.shape[2] == 3:
        a = np.concatenate([a, np.full(a.shape[:2] + (1,), 255, np.uint8)], 2)
    return skia.Image.fromarray(a, colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kUnpremul_AlphaType)


def gray_to_image(g):
    return np_to_image(np.stack([g, g, g, np.full_like(g, 255)], 2).astype(np.uint8))


# ───────────────────────────── kabartma (relief) ─────────────────────────────
METAL = dict(
    gold=[("#6B4A12", 0.0), ("#C9962B", 0.25), ("#F4DC8C", 0.5), ("#C9962B", 0.72), ("#7A5518", 1.0)],
    bronze=[("#4A2C14", 0.0), ("#9A6A3A", 0.3), ("#D9A56A", 0.55), ("#9A6A3A", 0.8), ("#4A2C14", 1.0)],
    silver=[("#4A4F56", 0.0), ("#A8AFB8", 0.3), ("#F0F4F8", 0.55), ("#A8AFB8", 0.8), ("#4A4F56", 1.0)],
    ivory=[("#8F8466", 0.0), ("#D8CCA8", 0.4), ("#F8F0D6", 0.6), ("#CDBF98", 1.0)],
)


def _grad_ramp(stops, n=256):
    xs = np.array([s[1] for s in stops])
    cols = np.array([rgb(s[0]) for s in stops], np.float32)
    t = np.linspace(0, 1, n)
    return np.stack([np.interp(t, xs, cols[:, i]) for i in range(3)], 1)


def relief_sprite(mask, metal="gold", bevel=4.0, strength=1.0, light=(-0.55, -0.65), spec=0.7, tex=None, tilt=0.35):
    """mask: float32 (h,w) 0..1 (şeklin alfa'sı). Çıktı: uint8 RGBA — kabartmalı metal.
    Yükseklik = bulanık maske; normal → Lambert + özgül parlaklık; renk = metal rampası (parlaklığa göre)."""
    m = mask.astype(np.float32)
    h = cv2.GaussianBlur(m, (0, 0), bevel) * 1.0 + 0.6 * cv2.GaussianBlur(m, (0, 0), bevel * 2.2)
    gx = cv2.Sobel(h, cv2.CV_32F, 1, 0, ksize=3) * strength * 0.9
    gy = cv2.Sobel(h, cv2.CV_32F, 0, 1, ksize=3) * strength * 0.9
    nz = np.ones_like(h)
    inv = 1.0 / np.sqrt(gx * gx + gy * gy + nz * nz)
    nx, ny, nz = -gx * inv, -gy * inv, nz * inv
    lx, ly = light
    lz = math.sqrt(max(0.05, 1 - lx * lx - ly * ly))
    dif = np.clip(nx * lx + ny * ly + nz * lz, 0, 1)
    base = lz
    shade = np.clip(0.5 + (dif - base) * 2.2 * 1.0, 0, 1)         # 0.5 = düz yüzey
    # özgül parlama
    hx, hy, hz = lx, ly, lz + 1.0
    hn = math.sqrt(hx * hx + hy * hy + hz * hz)
    sp = np.clip((nx * hx + ny * hy + nz * hz) / hn, 0, 1) ** 28
    ramp = _grad_ramp(METAL[metal])
    idx = np.clip(shade * 255, 0, 255).astype(np.int32)
    col = ramp[idx]
    if tex is not None:
        col = col * (0.88 + 0.24 * tex[..., None])
    col = col + sp[..., None] * 255 * spec
    a = np.clip(m * 1.0, 0, 1)
    out = np.dstack([np.clip(col, 0, 255), a * 255]).astype(np.uint8)
    return out


def text_mask(text, face, size, track=0.0, pad=24):
    """Metin → (mask float32, (ox, oy)): ox,oy = taban çizgisi başlangıcı maske içinde."""
    blob, wid = text_blob(face, text, size, track)
    w, h = int(wid + 2 * pad), int(size * 1.6 + 2 * pad)
    s = skia.Surface(w, h)
    c = s.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    c.drawTextBlob(blob, pad, pad + size * 1.15, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    a = s.makeImageSnapshot().toarray()[..., 3].astype(np.float32) / 255.0
    return a, (pad, pad + size * 1.15)


@lru_cache(maxsize=256)
def gold_text(text, face="title", size=96, track=4.0, metal="gold", bevel=None, spec=0.7):
    """Kabartmalı altın (veya başka metal) yazı sprite'ı → (skia.Image, ox, oy, w, h)."""
    m, (ox, oy) = text_mask(text, face, size, track)
    bev = bevel if bevel else max(1.2, size / 30.0)
    spr = relief_sprite(m, metal, bevel=bev, strength=1.0, spec=spec)
    return np_to_image(spr), ox, oy, spr.shape[1], spr.shape[0]


# ───────────────────────────── Frame ─────────────────────────────
class Frame:
    """Bir kare çizim yüzeyi + sık kullanılan çizimler."""

    def __init__(self, w=W, h=H):
        self.w, self.h = w, h
        self.surf = skia.Surface(w, h)
        self.c = self.surf.getCanvas()

    # --- temel
    def clear(self, color=None):
        self.c.clear(C(color) if isinstance(color, (str, tuple)) else (color if color is not None else skia.ColorTRANSPARENT))

    def paint(self, color=None, aa=True, style="fill", sw=1.0, shader=None, alpha=1.0, blend=None, blur=0.0, cap="round", join="round"):
        p = skia.Paint(AntiAlias=aa)
        if shader is not None:
            p.setShader(shader)
        elif color is not None:
            col = C(color) if isinstance(color, (str, tuple, list)) else color
            p.setColor(col)
        if alpha < 1.0:
            p.setAlphaf(clamp(alpha) * p.getAlphaf())
        if style == "stroke":
            p.setStyle(skia.Paint.kStroke_Style)
            p.setStrokeWidth(sw)
            p.setStrokeCap({"round": skia.Paint.kRound_Cap, "butt": skia.Paint.kButt_Cap, "square": skia.Paint.kSquare_Cap}[cap])
            p.setStrokeJoin({"round": skia.Paint.kRound_Join, "miter": skia.Paint.kMiter_Join, "bevel": skia.Paint.kBevel_Join}[join])
        if blend is not None:
            p.setBlendMode(blend)
        if blur > 0:
            p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
        return p

    def rect(self, x, y, w, h, **kw):
        self.c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), self.paint(**kw))

    def rrect(self, x, y, w, h, r, **kw):
        self.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), self.paint(**kw))

    def circle(self, x, y, r, **kw):
        self.c.drawCircle(x, y, r, self.paint(**kw))

    def oval(self, x, y, rx, ry, **kw):
        self.c.drawOval(skia.Rect.MakeLTRB(x - rx, y - ry, x + rx, y + ry), self.paint(**kw))

    def line(self, x0, y0, x1, y1, **kw):
        kw.setdefault("style", "stroke")
        self.c.drawLine(x0, y0, x1, y1, self.paint(**kw))

    def poly(self, pts, close=True, **kw):
        p = skia.Path()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        if close:
            p.close()
        self.c.drawPath(p, self.paint(**kw))

    def path(self, path, **kw):
        self.c.drawPath(path, self.paint(**kw))

    def smooth_path(self, pts, close=True, tension=0.5):
        return smooth_path(pts, close, tension)

    # --- degrade
    def lin(self, x0, y0, x1, y1, stops):
        return skia.GradientShader.MakeLinear([(x0, y0), (x1, y1)], [C(c, a) if not isinstance(c, int) else c for c, a in [(s[0], s[2] if len(s) > 2 else 255) for s in stops]], [s[1] for s in stops])

    def rad(self, x, y, r, stops):
        return skia.GradientShader.MakeRadial((x, y), r, [C(s[0], s[2] if len(s) > 2 else 255) for s in stops], [s[1] for s in stops])

    # --- metin
    def text(self, s, x, y, face="cap", size=40, color="#F0E6C8", align="l", track=0.0, alpha=1.0, shadow=None, shader=None, blend=None, outline=None):
        blob, wid = text_blob(face, s, size, track)
        ox = x - (wid / 2 if align == "c" else wid if align == "r" else 0)
        if shadow:
            dx, dy, bl, sc = shadow
            self.c.save(); self.c.translate(ox + dx, y + dy)
            self.c.drawTextBlob(blob, 0, 0, self.paint(sc, blur=bl, alpha=alpha))
            self.c.restore()
        if outline:
            ow, oc = outline
            self.c.save(); self.c.translate(ox, y)
            self.c.drawTextBlob(blob, 0, 0, self.paint(oc, style="stroke", sw=ow, alpha=alpha))
            self.c.restore()
        self.c.save(); self.c.translate(ox, y)
        self.c.drawTextBlob(blob, 0, 0, self.paint(color, alpha=alpha, shader=shader, blend=blend))
        self.c.restore()
        return wid

    def gold(self, s, x, y, face="title", size=96, track=4.0, align="c", alpha=1.0, metal="gold", scale=1.0, glow=0.0):
        img, ox, oy, w, h = gold_text(s, face, size, track, metal)
        wid = text_width(s, face, size, track)
        sx = x - (wid / 2 if align == "c" else wid if align == "r" else 0)
        self.c.save()
        self.c.translate(x, y)
        self.c.scale(scale, scale)
        self.c.translate(sx - x - ox, -oy)
        if glow > 0:
            gp = skia.Paint(AntiAlias=True, Alpha=int(255 * alpha * glow))
            gp.setImageFilter(skia.ImageFilters.Blur(size * 0.12, size * 0.12))
            gp.setColorFilter(skia.ColorFilters.Matrix([1.2, 0, 0, 0, 0.1, 0, 1.0, 0, 0, 0.05, 0, 0, 0.6, 0, 0, 0, 0, 0, 1, 0]))
            self.c.drawImage(img, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear), gp)
        pp = skia.Paint(AntiAlias=True, Alpha=int(255 * clamp(alpha)))
        self.c.drawImage(img, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear), pp)
        self.c.restore()
        return wid * scale

    # --- görüntü
    def image(self, img, x, y, sx=1.0, sy=None, rot=0.0, alpha=1.0, blend=None, ax=0.0, ay=0.0, blur=0.0, flt=True):
        """img'i (x,y) noktasına, (ax,ay)=(0..1) çapa ile yerleştirir."""
        sy = sx if sy is None else sy
        self.c.save()
        self.c.translate(x, y)
        if rot:
            self.c.rotate(math.degrees(rot))
        self.c.scale(sx, sy)
        p = skia.Paint(AntiAlias=True)
        if alpha < 1:
            p.setAlphaf(clamp(alpha))
        if blend is not None:
            p.setBlendMode(blend)
        if blur > 0:
            p.setImageFilter(skia.ImageFilters.Blur(blur, blur))
        self.c.drawImage(img, -ax * img.width(), -ay * img.height(), skia.SamplingOptions(skia.FilterMode.kLinear if flt else skia.FilterMode.kNearest), p)
        self.c.restore()

    def blit(self, other, alpha=1.0, blend=None, x=0, y=0):
        p = skia.Paint(AntiAlias=True)
        if alpha < 1:
            p.setAlphaf(clamp(alpha))
        if blend is not None:
            p.setBlendMode(blend)
        self.c.drawImage(other.surf.makeImageSnapshot(), x, y, skia.SamplingOptions(), p)

    # --- grup (katman)
    def layer_begin(self, alpha=1.0, blur=0.0, blend=None):
        p = skia.Paint()
        if alpha < 1:
            p.setAlphaf(clamp(alpha))
        if blend is not None:
            p.setBlendMode(blend)
        if blur > 0:
            p.setImageFilter(skia.ImageFilters.Blur(blur, blur))
        self.c.saveLayer(None, p)

    def layer_end(self):
        self.c.restore()

    # --- çıktı
    def rgb(self):
        a = self.surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kUnpremul_AlphaType)
        return a[..., :3]

    def rgba(self):
        return self.surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kUnpremul_AlphaType)


# ───────────────────────────── yol yardımcıları ─────────────────────────────
def smooth_path(pts, close=True, tension=0.5):
    """Catmull-Rom → Bezier yumuşak yol."""
    pts = [tuple(map(float, p)) for p in pts]
    n = len(pts)
    p = skia.Path()
    if n < 3:
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        return p
    p.moveTo(*pts[0])
    rng = range(n) if close else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (close or i > 0) else pts[i]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (close or i + 2 < n) else pts[(i + 1) % n]
        t = tension / 3 * 2
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 2, p1[1] + (p2[1] - p0[1]) * t / 2)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 2, p2[1] - (p3[1] - p1[1]) * t / 2)
        p.cubicTo(*c1, *c2, *p2)
    if close:
        p.close()
    return p


def ngon(cx, cy, r, n, rot=0.0):
    return [(cx + r * math.cos(rot + 2 * math.pi * i / n), cy + r * math.sin(rot + 2 * math.pi * i / n)) for i in range(n)]


def poly_path(pts, close=True):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if close:
        p.close()
    return p


# ───────────────────────────── atmosfer efektleri ─────────────────────────────
def background(f, kind="night", t=0.0, tone=0):
    """Temel arka plan: 'night' (kehribar-siyah), 'paper' (parşömen), 'sea' (derin mavi), 'ink' (düz mürekkep)."""
    w, h = f.w, f.h
    if kind == "night":
        f.rect(0, 0, w, h, shader=f.rad(w * 0.5, h * 0.40, h * 1.05, [("#4B2F1B", 0.0), ("#2B1A0F", 0.5), ("#0E0906", 1.0)]))
    elif kind == "paper":
        f.rect(0, 0, w, h, shader=f.rad(w * 0.5, h * 0.45, h * 1.05, [("#F3E8C8", 0.0), ("#E3D0A2", 0.6), ("#B79E6C", 1.0)]))
    elif kind == "sea":
        f.rect(0, 0, w, h, shader=f.lin(0, 0, 0, h, [("#1B3347", 0.0), ("#0F1D2A", 1.0)]))
    else:
        f.rect(0, 0, w, h, color=P["INK"])


def texture_overlay(f, kind="night", amp=0.10, seed=3):
    """Dokuyu kareye çarpar (multiply/overlay). Kare içinde önbellekli numpy gürültüsünden."""
    n = noise_tex(W // 2, H // 2, 22, 4, seed)
    fine = noise_tex(W // 2, H // 2, 5, 2, seed + 1)
    g = (0.65 * n + 0.35 * fine)
    g = (g - g.mean()) / (g.std() + 1e-6)
    g8 = np.clip(128 + g * 255 * amp * 0.5, 0, 255).astype(np.uint8)
    img = gray_to_image(cv2.resize(g8, (W, H), interpolation=cv2.INTER_LINEAR))
    f.c.drawImage(img, 0, 0, skia.SamplingOptions(), skia.Paint(BlendMode=skia.BlendMode.kOverlay))


def vignette(f, strength=0.6, inner=0.45, color="#000000"):
    r = max(f.w, f.h) * 0.78
    sh = skia.GradientShader.MakeRadial((f.w / 2, f.h / 2), r, [C(color, 0), C(color, 0), C(color, int(255 * strength))], [0.0, inner, 1.0])
    f.c.drawRect(skia.Rect.MakeWH(f.w, f.h), skia.Paint(Shader=sh))


def light_rays(f, src, angle, spread, length, n=7, alpha=0.18, color="#FFE2A0", t=0.0, seed=1, blur=14):
    """Pencereden/kaynaktan yayılan ışık şeritleri (additive)."""
    rs = np.random.RandomState(seed)
    f.layer_begin(alpha=1.0, blur=blur, blend=skia.BlendMode.kPlus)
    for i in range(n):
        a = angle + (rs.rand() - 0.5) * spread
        wdt = (0.02 + rs.rand() * 0.05) * (1 + 0.25 * math.sin(t * 0.7 + i))
        l = length * (0.7 + rs.rand() * 0.5)
        x0, y0 = src
        p1 = (x0 + math.cos(a - wdt) * l, y0 + math.sin(a - wdt) * l)
        p2 = (x0 + math.cos(a + wdt) * l, y0 + math.sin(a + wdt) * l)
        sh = skia.GradientShader.MakeLinear([(x0, y0), (x0 + math.cos(a) * l, y0 + math.sin(a) * l)], [C(color, int(255 * alpha * (0.6 + 0.4 * rs.rand()))), C(color, 0)], [0, 1])
        f.c.drawPath(poly_path([(x0, y0), p1, p2]), skia.Paint(Shader=sh, AntiAlias=True))
    f.layer_end()


def dust(f, t, n=70, seed=2, speed=(6, 3), depth=1.0, alpha=0.5, color="#FFE8B0", rect=None):
    rs = np.random.RandomState(seed)
    x0, y0, w, h = rect if rect else (0, 0, f.w, f.h)
    f.layer_begin(blend=skia.BlendMode.kPlus)
    for i in range(n):
        d = 0.3 + rs.rand() * 0.7
        px = (rs.rand() * w + t * speed[0] * d * depth + math.sin(t * 0.4 + i) * 12 * d) % w
        py = (rs.rand() * h + t * speed[1] * d * depth + math.cos(t * 0.31 + i * 1.7) * 10 * d) % h
        r = (1.0 + 3.2 * d) * (0.6 + 0.4 * math.sin(t * 1.3 + i))
        a = alpha * d * (0.4 + 0.6 * abs(math.sin(t * 0.5 + i * 2.1)))
        f.c.drawCircle(x0 + px, y0 + py, r, skia.Paint(AntiAlias=True, Color=C(color, int(255 * a)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 0.8 + 2.2 * d)))
    f.layer_end()


def smoke(f, x, y, t, w=220, h=380, n=9, seed=4, color="#1A1410", alpha=0.35, rise=60):
    rs = np.random.RandomState(seed)
    f.layer_begin(blur=16)
    for i in range(n):
        ph = (t * 0.18 + rs.rand()) % 1.0
        px = x + (rs.rand() - 0.5) * w * 0.5 + math.sin(ph * 6 + i) * w * 0.18 * ph
        py = y - ph * h
        r = 26 + ph * 90 + rs.rand() * 18
        a = alpha * math.sin(math.pi * ph) ** 1.2
        f.c.drawCircle(px, py, r, skia.Paint(AntiAlias=True, Color=C(color, int(255 * a))))
    f.layer_end()


def embers(f, t, n=60, seed=6, rect=None, color="#FFB347"):
    rs = np.random.RandomState(seed)
    x0, y0, w, h = rect if rect else (0, 0, f.w, f.h)
    f.layer_begin(blend=skia.BlendMode.kPlus)
    for i in range(n):
        ph = (t * (0.08 + 0.1 * rs.rand()) + rs.rand()) % 1.0
        px = x0 + (rs.rand() * w + math.sin(t * 0.9 + i) * 24 * ph) % w
        py = y0 + h * (1 - ph)
        a = (1 - ph) * (0.5 + 0.5 * abs(math.sin(t * 6 + i)))
        f.c.drawCircle(px, py, 1.2 + 1.8 * rs.rand(), skia.Paint(AntiAlias=True, Color=C(color, int(255 * a)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 1.2)))
    f.layer_end()


def rain(f, t, n=240, seed=8, angle=-0.28, length=34, alpha=0.35, color="#BFD0DC", speed=1500):
    rs = np.random.RandomState(seed)
    p = skia.Paint(AntiAlias=True, Color=C(color, int(255 * alpha)), StrokeWidth=1.4, Style=skia.Paint.kStroke_Style)
    dx, dy = math.sin(-angle), math.cos(angle)
    for i in range(n):
        d = 0.5 + rs.rand() * 0.5
        s = (t * speed * d / 1000.0 + rs.rand()) % 1.0
        px = (rs.rand() * (f.w + 400) - 200 + s * 400 * dx) % (f.w + 400) - 200
        py = (s * (f.h + 100)) - 50
        f.c.drawLine(px, py, px + dx * length * d, py + dy * length * d, p)


def snow(f, t, n=140, seed=9, alpha=0.8):
    rs = np.random.RandomState(seed)
    for i in range(n):
        d = 0.3 + rs.rand() * 0.7
        px = (rs.rand() * f.w + math.sin(t * 0.8 + i) * 30 * d) % f.w
        py = ((t * 45 * d) + rs.rand() * f.h) % f.h
        f.c.drawCircle(px, py, 1.2 + 2.6 * d, skia.Paint(AntiAlias=True, Color=C("#FFFFFF", int(255 * alpha * d))))


# ───────────────────────────── önbellekli tam-ekran katmanlar ─────────────────────────────
_BAKED = {}


def baked(key, builder):
    """builder(f: Frame) tam ekran bir Frame'e çizer; sonuç skia.Image olarak önbelleğe alınır."""
    if key not in _BAKED:
        f = Frame()
        f.clear(skia.ColorTRANSPARENT)
        builder(f)
        _BAKED[key] = f.surf.makeImageSnapshot()
    return _BAKED[key]


def bg_image(kind="night", amp=0.06, seed=3, vig=0.55):
    def b(f):
        background(f, kind)
        if amp > 0:
            texture_overlay(f, kind, amp=amp, seed=seed)
        if vig > 0:
            vignette(f, vig)
    return baked(("bg", kind, amp, seed, vig), b)


def vig_image(strength=0.6, inner=0.45):
    return baked(("vig", strength, inner), lambda f: vignette(f, strength, inner))


def rays_image(src=(300, -80), angle=1.1, spread=0.9, length=1500, n=8, alpha=0.12, color="#FFE2A0", seed=1, blur=14):
    return baked(("rays", src, angle, spread, length, n, alpha, color, seed, blur),
                 lambda f: light_rays(f, src, angle, spread, length, n=n, alpha=alpha, color=color, seed=seed, blur=blur))


def _fast_blit(f, img, alpha=1.0, blend=None, dx=0, dy=0):
    p = skia.Paint()
    if alpha < 1:
        p.setAlphaf(clamp(alpha))
    if blend is not None:
        p.setBlendMode(blend)
    f.c.drawImage(img, dx, dy, skia.SamplingOptions(), p)


Frame.bg = lambda self, kind="night", amp=0.06, seed=3, vig=0.55: _fast_blit(self, bg_image(kind, amp, seed, vig))
Frame.vig = lambda self, strength=0.6, inner=0.45: _fast_blit(self, vig_image(strength, inner))
Frame.rays = lambda self, alpha=1.0, dx=0, dy=0, **kw: _fast_blit(self, rays_image(**kw), alpha=alpha, blend=skia.BlendMode.kPlus, dx=dx, dy=dy)


# ───────────────────────────── kare sonrası (numpy/cv2, hızlı) ─────────────────────────────
_GR = None


def _grain_bank():
    """6 çift (pozitif, negatif) uint8 gren (H,W,3)."""
    global _GR
    if _GR is None:
        rs = np.random.RandomState(11)
        bank = []
        for _ in range(6):
            g = rs.randn(H // 2, W // 2).astype(np.float32)
            g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)
            pos = np.clip(g * 3.0, 0, 255).astype(np.uint8)
            neg = np.clip(-g * 3.0, 0, 255).astype(np.uint8)
            bank.append((cv2.merge([pos, pos, pos]), cv2.merge([neg, neg, neg])))
        _GR = bank
    return _GR


_LUT = {}


def grade_lut(contrast=1.06, warm=0.035, lift=2.0):
    key = (contrast, warm, lift)
    if key not in _LUT:
        x = np.arange(256, dtype=np.float32) / 255.0
        y = np.clip((x - 0.5) * contrast + 0.5, 0, 1)
        y = np.clip(y + (lift / 255.0) * (1 - y), 0, 1)
        r = np.clip(y * (1 + warm) + 0.004, 0, 1)
        b = np.clip(y * (1 - warm * 1.4), 0, 1)
        lut = np.stack([r, y, b], 1) * 255
        _LUT[key] = np.ascontiguousarray(np.clip(lut, 0, 255).astype(np.uint8).reshape(256, 1, 3))
    return _LUT[key]


def post(img, frame_idx=0, grain=1.0, bloom=0.22, grade=(1.06, 0.035, 2.0), fade=1.0):
    """img uint8 RGB (H,W,3) → uint8 RGB: ışıma + renk ayarı + film greni (~25 ms)."""
    a = img
    if bloom > 0:
        small = cv2.resize(a, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(small, cv2.COLOR_RGB2GRAY)
        mask = cv2.subtract(gray, 168)
        mask = cv2.multiply(mask, 3)
        hi = cv2.bitwise_and(small, small, mask=mask)  # parlak bölgeler
        hi = cv2.GaussianBlur(hi, (0, 0), 6)
        hi2 = cv2.GaussianBlur(hi, (0, 0), 14)
        hi = cv2.addWeighted(hi, 0.7, hi2, 0.7, 0)
        up = cv2.resize(hi, (W, H), interpolation=cv2.INTER_LINEAR)
        a = cv2.addWeighted(a, 1.0, up, bloom, 0)
    a = cv2.LUT(a, grade_lut(*grade))
    if grain > 0:
        pos, neg = _grain_bank()[frame_idx % 6]
        a = cv2.add(a, pos)
        a = cv2.subtract(a, neg)
    if fade < 1.0:
        a = cv2.convertScaleAbs(a, alpha=max(0.0, fade))
    return a


def to_rgb_f(f):
    return f.rgb()


def optional_import(name):
    """Başka ajanların yazdığı isteğe bağlı modülleri güvenle yükle (yarım kalmış/hatalı modül ortak kiti bozmasın)."""
    import importlib
    import sys
    import traceback
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as e:
        if e.name == name:
            return None
        print(f"[uyarı] {name} yüklenemedi: {e}", file=sys.stderr)
    except Exception:
        print(f"[uyarı] {name} yüklenemedi:\n" + traceback.format_exc(limit=3), file=sys.stderr)
    return None
