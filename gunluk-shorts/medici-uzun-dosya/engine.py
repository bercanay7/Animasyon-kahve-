"""
Zaman Kuryesi · Uzun Dosya #1 (Şarlken) — 16:9 çizim motoru (Pellagra/Dune motorunun yatay uyarlaması)

* Dünya 2x süper örneklemeli tuvale (3840x2160) çizilir, kamera dönüşümü (zoom/kaydırma/sarsıntı)
  her çizim çağrısında uygulanır. Önizleme için SS=1 ortam değişkeni (4x hızlı, daha pürüzlü).
* Tuval 1920x1080'e indirildikten SONRA yazılar/HUD 1x tuvale çizilir (kamera zoom'undan etkilenmez).
"""
import math
import os
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops

W, H = 1920, 1080
SS = int(os.environ.get("SS", "2"))
FPS = 24

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "fonts")
FONT_TITLE = os.path.join(FD, "Cinzel_700Bold.ttf")          # başlık, bölüm kartı, damga
FONT_TITLE_M = os.path.join(FD, "Cinzel_600SemiBold.ttf")
FONT_TITLE_L = os.path.join(FD, "Cinzel_400Regular.ttf")
FONT_CAP = os.path.join(FD, "CormorantGaramond_700Bold.ttf")  # altyazı
FONT_CAP_M = os.path.join(FD, "CormorantGaramond_600SemiBold.ttf")
FONT_CAP_IT = os.path.join(FD, "CormorantGaramond_600SemiBold_Italic.ttf")
FONT_BODY = os.path.join(FD, "EBGaramond_500Medium.ttf")
FONT_BODY_IT = os.path.join(FD, "EBGaramond_400Regular_Italic.ttf")
FONT_MAP = os.path.join(FD, "IMFellEnglish_400Regular.ttf")     # harita etiketi
FONT_MAP_IT = os.path.join(FD, "IMFellEnglish_400Regular_Italic.ttf")
FONT_FELL = os.path.join(FD, "IMFellDWPica_400Regular.ttf")     # belge/el yazısı
FONT_FELL_IT = os.path.join(FD, "IMFellDWPica_400Regular_Italic.ttf")
FONT_POP = FONT_TITLE


# ───────────────────────── yardımcılar ─────────────────────────
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, t):
    return a + (b - a) * t


def prog(t, a, b):
    """t, [a,b] aralığında 0..1"""
    if b == a:
        return 1.0 if t >= b else 0.0
    return clamp((t - a) / (b - a))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x, p=3):
    x = clamp(x)
    return 1 - (1 - x) ** p


def ease_in(x, p=3):
    return clamp(x) ** p


def ease_io(x):
    x = clamp(x)
    return 4 * x * x * x if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def back_out(x, s=1.70158):
    x = clamp(x)
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def elastic_out(x):
    x = clamp(x)
    if x in (0.0, 1.0):
        return x
    return 2 ** (-9 * x) * math.sin((x * 10 - 0.75) * (2 * math.pi) / 3) + 1


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(c1, c2, t):
    t = clamp(t)
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c1, c2))


def shade(c, k):
    """k<0 koyulaştır, k>0 aydınlat"""
    if k >= 0:
        return mix(c, (255, 255, 255), k)
    return mix(c, (0, 0, 0), -k)


def rng_hash(*a):
    """Deterministik 0..1 sahte rastgele"""
    h = 2166136261
    for v in a:
        h ^= int(v * 1000003) & 0xFFFFFFFF
        h = (h * 16777619) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * 0x5bd1e995) & 0xFFFFFFFF
    h ^= h >> 15
    return (h & 0xFFFFFF) / float(0x1000000)


@lru_cache(maxsize=256)
def font(path, px):
    return ImageFont.truetype(path, max(1, int(round(px))))


# ───────────────────────── çizim bağlamı ─────────────────────────
@lru_cache(maxsize=1)
def _radial_mask():
    n = 256
    y, x = np.mgrid[0:n, 0:n]
    r = np.hypot(x - n / 2 + 0.5, y - n / 2 + 0.5) / (n / 2)
    a = np.clip(1 - r, 0, 1) ** 2
    return Image.fromarray((a * 255).astype(np.uint8), "L")


class Ctx:
    """Kamera destekli, 2x süper örneklemeli çizim bağlamı. Tüm koordinatlar dünya (≈ ekran 1x) koordinatıdır."""

    def __init__(self):
        self.im = Image.new("RGB", (W * SS, H * SS), (0, 0, 0))
        self.d = ImageDraw.Draw(self.im)
        self.cx, self.cy, self.z = W / 2, H / 2, 1.0
        self.shx = self.shy = 0.0
        self.par = 1.0

    # --- kamera ---
    def cam(self, cx=W / 2, cy=H / 2, z=1.0, shake=(0.0, 0.0)):
        self.cx, self.cy, self.z = cx, cy, z
        self.shx, self.shy = shake
        self.par = 1.0

    def parallax(self, p):
        self.par = p

    def _k(self):
        p = self.par
        zp = 1 + (self.z - 1) * p
        cxp = W / 2 + (self.cx - W / 2) * p
        cyp = H / 2 + (self.cy - H / 2) * p
        return zp, cxp, cyp

    def X(self, x, y):
        zp, cxp, cyp = self._k()
        return ((x - cxp) * zp + W / 2 + self.shx) * SS, ((y - cyp) * zp + H / 2 + self.shy) * SS

    def S(self, v):
        """dünya uzunluğu → tuval pikseli"""
        return v * self._k()[0] * SS

    def pts(self, p):
        zp, cxp, cyp = self._k()
        ox = (W / 2 + self.shx) * SS
        oy = (H / 2 + self.shy) * SS
        k = zp * SS
        return [((x - cxp) * k + ox, (y - cyp) * k + oy) for x, y in p]

    # --- alfa destekli maskeli çizim ---
    def _masked(self, bbox, fn, color, alpha):
        x0, y0, x1, y1 = bbox
        x0 = max(0, int(math.floor(x0)))
        y0 = max(0, int(math.floor(y0)))
        x1 = min(self.im.width, int(math.ceil(x1)))
        y1 = min(self.im.height, int(math.ceil(y1)))
        if x1 <= x0 or y1 <= y0:
            return
        m = Image.new("L", (x1 - x0, y1 - y0), 0)
        fn(ImageDraw.Draw(m), x0, y0, int(round(255 * alpha)))
        self.im.paste(color, (x0, y0), m)

    # --- ilkel şekiller ---
    def poly(self, p, fill, alpha=1.0):
        q = self.pts(p)
        if alpha >= 0.999:
            self.d.polygon(q, fill=fill)
            return
        xs = [a for a, _ in q]
        ys = [b for _, b in q]
        self._masked((min(xs) - 1, min(ys) - 1, max(xs) + 1, max(ys) + 1),
                     lambda d, ox, oy, v: d.polygon([(a - ox, b - oy) for a, b in q], fill=v), fill, alpha)

    def ell(self, cx, cy, rx, ry, fill, alpha=1.0):
        x0, y0 = self.X(cx - rx, cy - ry)
        x1, y1 = self.X(cx + rx, cy + ry)
        if alpha >= 0.999:
            self.d.ellipse([x0, y0, x1, y1], fill=fill)
            return
        self._masked((x0 - 1, y0 - 1, x1 + 1, y1 + 1),
                     lambda d, ox, oy, v: d.ellipse([x0 - ox, y0 - oy, x1 - ox, y1 - oy], fill=v), fill, alpha)

    def circ(self, cx, cy, r, fill, alpha=1.0):
        self.ell(cx, cy, r, r, fill, alpha)

    def rect(self, x0, y0, x1, y1, fill, alpha=1.0):
        a, b = self.X(x0, y0)
        c, d = self.X(x1, y1)
        if c < a:
            a, c = c, a
        if d < b:
            b, d = d, b
        if alpha >= 0.999:
            self.d.rectangle([a, b, c, d], fill=fill)
            return
        self._masked((a, b, c, d),
                     lambda dr, ox, oy, v: dr.rectangle([a - ox, b - oy, c - ox, d - oy], fill=v), fill, alpha)

    def rrect(self, x0, y0, x1, y1, r, fill, alpha=1.0):
        a, b = self.X(x0, y0)
        c, d = self.X(x1, y1)
        rr = self.S(r)
        if alpha >= 0.999:
            self.d.rounded_rectangle([a, b, c, d], radius=rr, fill=fill)
            return
        self._masked((a, b, c, d),
                     lambda dr, ox, oy, v: dr.rounded_rectangle([a - ox, b - oy, c - ox, d - oy], radius=rr, fill=v),
                     fill, alpha)

    def ring(self, cx, cy, r, width, color, alpha=1.0):
        x0, y0 = self.X(cx - r, cy - r)
        x1, y1 = self.X(cx + r, cy + r)
        w = max(1, int(self.S(width)))
        if alpha >= 0.999:
            self.d.ellipse([x0, y0, x1, y1], outline=color, width=w)
            return
        self._masked((x0 - 1, y0 - 1, x1 + 1, y1 + 1),
                     lambda d, ox, oy, v: d.ellipse([x0 - ox, y0 - oy, x1 - ox, y1 - oy], outline=v, width=w),
                     color, alpha)

    def line(self, p, width, fill, alpha=1.0, cap=True):
        q = self.pts(p)
        w = max(1, int(round(self.S(width))))

        def go(d, ox, oy, v):
            qq = [(a - ox, b - oy) for a, b in q]
            d.line(qq, fill=v, width=w, joint="curve")
            if cap and w > 2:
                r = w / 2
                for a, b in (qq[0], qq[-1]):
                    d.ellipse([a - r, b - r, a + r, b + r], fill=v)

        if alpha >= 0.999:
            go(self.d, 0, 0, fill)
            return
        xs = [a for a, _ in q]
        ys = [b for _, b in q]
        pad = w + 2
        self._masked((min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad), go, fill, alpha)

    def arc(self, cx, cy, r, a0, a1, width, fill):
        x0, y0 = self.X(cx - r, cy - r)
        x1, y1 = self.X(cx + r, cy + r)
        self.d.arc([x0, y0, x1, y1], a0, a1, fill=fill, width=max(1, int(self.S(width))))

    def glow(self, cx, cy, r, color, alpha=1.0):
        x, y = self.X(cx, cy)
        rr = self.S(r)
        x0, y0, x1, y1 = int(x - rr), int(y - rr), int(x + rr) + 1, int(y + rr) + 1
        cx0, cy0 = max(0, x0), max(0, y0)
        cx1, cy1 = min(self.im.width, x1), min(self.im.height, y1)
        if cx1 <= cx0 or cy1 <= cy0 or x1 - x0 < 2:
            return
        m = _radial_mask().resize((x1 - x0, y1 - y0), Image.BILINEAR)
        m = m.crop((cx0 - x0, cy0 - y0, cx1 - x0, cy1 - y0))
        if alpha < 0.999:
            m = m.point(lambda v: int(v * alpha))
        self.im.paste(color, (cx0, cy0), m)

    def vgrad(self, x0, y0, x1, y1, stops, alpha=1.0):
        """Dikey gradyan; stops=[(0.0,rgb),(1.0,rgb),...]. Yalnızca görünen satırlar hesaplanır."""
        a, b = self.X(x0, y0)
        c, d = self.X(x1, y1)
        a, b, c, d = int(a), int(b), int(math.ceil(c)), int(math.ceil(d))
        ca, cb = max(0, a), max(0, b)
        cc, cd = min(self.im.width, c), min(self.im.height, d)
        if cc <= ca or cd <= cb or d <= b:
            return
        ys = (np.arange(cb, cd, dtype=np.float32) + 0.5 - b) / float(d - b)
        arr = np.zeros((cd - cb, 1, 3), np.uint8)
        xs = [s[0] for s in stops]
        for ch in range(3):
            arr[:, 0, ch] = np.interp(ys, xs, [s[1][ch] for s in stops])
        g = Image.fromarray(arr, "RGB").resize((cc - ca, cd - cb), Image.NEAREST)
        if alpha < 0.999:
            self.im.paste(g, (ca, cb), Image.new("L", g.size, int(255 * clamp(alpha))))
        else:
            self.im.paste(g, (ca, cb))

    def text(self, x, y, s, px, fill, path=FONT_TITLE, anchor="mm", stroke=0, stroke_fill=None):
        f = font(path, self.S(px))
        kw = {}
        if stroke:
            kw = dict(stroke_width=max(1, int(self.S(stroke))), stroke_fill=stroke_fill)
        cx, cy = self.X(x, y)
        self.d.text((cx, cy), s, font=f, fill=fill, anchor=anchor, **kw)

    def overlay_rgb(self, color, alpha):
        if alpha <= 0:
            return
        self.im.paste(Image.new("RGB", self.im.size, color), (0, 0), Image.new("L", self.im.size, int(255 * clamp(alpha))))

    def finish(self):
        return self.im.reduce(SS) if SS > 1 else self.im  # 1920x1080 RGB


# ───────────────────────── dönüşüm yardımcısı ─────────────────────────
class Xf:
    """Yerel koordinat → dünya (konum, ölçek, yatay çevirme, döndürme[derece])"""

    def __init__(self, ox, oy, s=1.0, flip=1, rot=0.0):
        self.ox, self.oy, self.s, self.flip = ox, oy, s, flip
        a = math.radians(rot)
        self.c, self.sn = math.cos(a), math.sin(a)

    def p(self, x, y):
        x *= self.flip * self.s
        y *= self.s
        return (self.ox + x * self.c - y * self.sn, self.oy + x * self.sn + y * self.c)

    def pts(self, lst):
        return [self.p(x, y) for x, y in lst]

    def len(self, v):
        return v * self.s


# ───────────────────────── 1x yazı sistemi ─────────────────────────
@lru_cache(maxsize=512)
def word_sprite(word, color, px, path=FONT_TITLE, stroke=5, stroke_fill=(10, 27, 46), shadow=True):
    """2x boyutta (px*2) çizilmiş kenarlıklı kelime sprite'ı (RGBA)."""
    f = font(path, px * 2)
    st = stroke * 2
    l, t, r, b = f.getbbox(word, stroke_width=st)
    pad = 14 * 2
    w = int(r - l + pad * 2)
    h = int(f.size * 1.5 + pad * 2)
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cx, cy = w // 2, h // 2
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((cx + 0, cy + 9), word, font=f, fill=(0, 0, 0, 120), anchor="mm",
                                stroke_width=st, stroke_fill=(0, 0, 0, 120))
        lay = Image.alpha_composite(lay, sh)
        d = ImageDraw.Draw(lay)
    d.text((cx, cy), word, font=f, fill=color + (255,), anchor="mm", stroke_width=st, stroke_fill=stroke_fill + (255,))
    return lay


def blit(img, sprite, cx, cy, scale=1.0, alpha=1.0, rot=0.0, base=0.5):
    """2x sprite'ı 1x tuvale (img: RGB 1920x1080) ölçek/döndürme/saydamlıkla yerleştir. base: sprite 2x ise 0.5."""
    if alpha <= 0.003 or scale <= 0.003:
        return
    k = base * scale
    w = max(1, int(round(sprite.width * k)))
    h = max(1, int(round(sprite.height * k)))
    s = sprite.resize((w, h), Image.LANCZOS)
    if rot:
        s = s.rotate(rot, resample=Image.BICUBIC, expand=True)
    a = s.getchannel("A")
    if alpha < 0.999:
        a = a.point(lambda v: int(v * alpha))
    img.paste(s.convert("RGB"), (int(round(cx - s.width / 2)), int(round(cy - s.height / 2))), a)
