"""cilt_pano — UZUN PLAN PANORAMASI (`pano` çekim türü).

Tek, kesintisiz kamera yolu boyunca kayan, ≥5–8 ekran genişliğinde fresk şeridi:
  * prosedürel KATMANLAR (≥3 derinlik, paralaks) — gökyüzü / tepe / uzak şehir / orta bina / nehir / ana düzlem / ön plan; ağır katmanlar 1024 px'lik
    KAREAŞ (tile) olarak tembel pişirilir ve `out/_cache/world` altında diske önbelleklenir (ilk çalıştırmada bake, sonra yalnız okuma);
  * KAMERA YOLU anahtar karelidir: `cams=[(çapa,(x,y,zoom)),…]` (çapa = saniye | ("c7s5",“sözcük”,−0.1)), PCHIP + uçlarda yumuşak başlama/bitiş (ease_io);
    `longtake=True` ile uyumlu (≤28 sn); çapa verilmezse dünyaya özgü varsayılan yol çekim süresine yayılır;
  * İSTASYONLAR `stations=[dict(x=…, at=çapa, fn=…)]`: o noktada canlanan animasyonlu sahneler (bankacı masası, boyahane, kaçan kalabalık …);
  * HAZIR YAPILAR: pano="florence" (Arno kıyısı/Ponte Vecchio/boyahane/tezgâhlar/bankacı/Duomo'ya yürüyüş; tod day|dusk|night), pano="nave" (katedral nefi içi:
    sütun sırası, tonoz, pencereden ışık huzmesi, diz çöken/ayakta kalabalık, çan sarkacı, kaçan figürler), pano="corridor" (Vasari Koridoru: pencerelerden akan nehir/şehir).
`shot("pano", a, pano="florence", cams=[…], stations=[…], tod="day", dur-bağımsız)` — cam/link/longtake/montage kabul edilir ve yok sayılır / uyumludur.
"""
import functools
import math
import os
import time

import cv2
import numpy as np
import skia

import cilt_anim as FA
import cilt_city as CT
import cilt_medici as CM
import cilt_scene as SC
import sk
from cilt_medici import TH, ckind
from sk import C, H, W, clamp, mix, smooth

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "out", "_cache", "world")
VER = "p1"
OV = 70                         # dikey taşma (kamera y kayması)
TW = 1024                       # kareaş genişliği (px)
LIN = skia.SamplingOptions(skia.FilterMode.kLinear)
INK = "#2A1A0C"


# ═════════════════════════════ küçük çizim yardımcıları ═════════════════════════════
def _RS(n):
    return np.random.RandomState(int(n) & 0x7FFFFFFF)


def R(c, x0, y0, x1, y1, col, a=255):
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.Paint(Color=C(col, a)))


def RA(c, x0, y0, x1, y1, col, a=255):
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.Paint(AntiAlias=True, Color=C(col, a)))


def INKP(c, path, w=1.2, a=170, col=INK):
    c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, a), StrokeJoin=skia.Paint.kRound_Join))


def INKR(c, x0, y0, x1, y1, w=1.2, a=170, col=INK):
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, a)))


def LINE(c, x0, y0, x1, y1, col=INK, w=1.2, a=255, cap=True):
    c.drawLine(x0, y0, x1, y1, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, a), StrokeCap=skia.Paint.kRound_Cap if cap else skia.Paint.kButt_Cap))


def POLY(c, pts, col, a=255, ink=0, inka=170):
    p = sk.poly_path(pts)
    c.drawPath(p, skia.Paint(AntiAlias=True, Color=C(col, a)))
    if ink:
        INKP(c, p, ink, inka)
    return p


def OVAL(c, cx, cy, rx, ry, col, a=255):
    c.drawOval(skia.Rect.MakeLTRB(cx - rx, cy - ry, cx + rx, cy + ry), skia.Paint(AntiAlias=True, Color=C(col, a)))


def GRAD_V(c, x0, y0, x1, y1, stops):
    """Dikey degrade dikdörtgen. stops=[(renk, konum 0..1[, alfa])]."""
    cols = [C(s[0], s[2] if len(s) > 2 else 255) for s in stops]
    pos = [s[1] for s in stops]
    sh = skia.GradientShader.MakeLinear([(0, y0), (0, y1)], cols, pos)
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.Paint(Shader=sh))


def shade_right(c, x0, y0, x1, y1, a=38):
    """Işık sol-üstten: sağ kenarda koyulaşma (sprite gölgesi)."""
    sh = skia.GradientShader.MakeLinear([(x0 + (x1 - x0) * 0.55, 0), (x1, 0)], [C("#1A1008", 0), C("#1A1008", a)], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.Paint(Shader=sh))


def ridge_y(x, base, amp, scale, ph):
    """Deterministik tepe çizgisi (tile'lar arası süreklilik için x'in saf fonksiyonu)."""
    return base + amp * (0.6 * math.sin(x / scale + ph) + 0.4 * math.sin(x / (scale * 0.37) + ph * 1.7) + 0.2 * math.sin(x / (scale * 0.13) + ph * 2.3)) / 1.2


def fresco_wear(c, rs, xa, xb, h, cracks=7, edge_loss=0.0, top=0, bottom=0):
    """İnce çatlak çizgileri (açık sıva) + isteğe bağlı kenar boya kayıpları (alfa deliği → duvar görünür)."""
    for i in range(cracks):
        x = rs.uniform(xa, xb)
        y = rs.uniform(OV, h - OV)
        pts = [(x, y)]
        ang = rs.uniform(-1.2, 1.2)
        for k in range(rs.randint(5, 12)):
            ang += rs.normal(0, 0.55)
            x += math.cos(ang) * rs.uniform(10, 28)
            y += math.sin(ang) * rs.uniform(10, 28)
            pts.append((x, y))
        p = skia.Path()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#E9DFC4", 62)))
    if edge_loss > 0:
        n = int(edge_loss * (xb - xa) / 40)
        for i in range(n):
            x = rs.uniform(xa, xb)
            edge_y = OV + rs.uniform(-6, 26) if rs.rand() < 0.5 else h - OV + rs.uniform(-26, 6)
            r = rs.uniform(5, 26)
            pts = []
            for k in range(9):
                a = k / 9 * 6.283
                rr = r * rs.uniform(0.55, 1.1)
                pts.append((x + math.cos(a) * rr * 1.5, edge_y + math.sin(a) * rr * 0.8))
            p = sk.poly_path(pts)
            c.drawPath(p, skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kClear))
            c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#D9CDB0", 150), BlendMode=skia.BlendMode.kDstOver))


# ═════════════════════════════ katman + kareaş önbelleği ═════════════════════════════
class Layer:
    """Paralaks katmanı: `draw(fr, xa, xb)` katman koordinatında [xa,xb] aralığındaki nesneleri çizer (fr: sk.Frame; fr.c ötelenmiş+kırpılmış).
    Kareaşlar TW px (scale<1 ise daha geniş katman aralığı) — tembel; disk önbelleği out/_cache/world."""

    def __init__(self, world, name, f, width, draw, scale=1.0, opaque=False, h=None, wear=0, loss=0.0, tod="day", yr=None):
        self.world, self.name, self.f, self.width, self.draw, self.scale, self.opaque = world, name, f, int(width), draw, scale, opaque
        self.h = h or (800 + 2 * OV)
        self.y0, self.y1 = yr if yr else (0, self.h)
        self.TWL = TW / scale
        self.wear, self.loss, self.tod = wear, loss, tod
        self.tiles = {}
        self.pad = 3.0 / scale

    def n_tiles(self):
        return max(1, int(math.ceil(self.width / self.TWL)))

    def _path(self, i):
        return os.path.join(CACHE, f"{self.world}_{self.tod}_{self.name}_{i}_{VER}.png")

    def tile(self, i):
        t = self.tiles.get(i)
        if t is None:
            t = self.tiles[i] = self._bake(i)
        return t

    def _bake(self, i):
        x0 = i * self.TWL - self.pad
        x1 = (i + 1) * self.TWL + self.pad
        path = self._path(i)
        try:
            if os.path.exists(path):
                a = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                if a is not None and a.shape[2] == 4:
                    a = cv2.cvtColor(a, cv2.COLOR_BGRA2RGBA)
                    return sk.np_to_image(a), x0
        except Exception:
            pass
        wpx, hpx = int(round(TW + 2 * 3)), int(round((self.y1 - self.y0) * self.scale))
        fr = sk.Frame(wpx, hpx)
        fr.clear("#000000" if self.opaque else None)
        c = fr.c
        c.scale(self.scale, self.scale)
        c.translate(-x0, -self.y0)
        c.clipRect(skia.Rect.MakeLTRB(x0, self.y0, x1, self.y1))
        self.draw(fr, x0, x1)
        if self.wear:
            fresco_wear(c, _RS(i * 131 + 7), x0, x1, self.h, cracks=self.wear, edge_loss=self.loss)
        img = fr.surf.makeImageSnapshot()
        try:
            os.makedirs(CACHE, exist_ok=True)
            arr = img.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kUnpremul_AlphaType)
            cv2.imwrite(path, cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA), [cv2.IMWRITE_PNG_COMPRESSION, 1])
        except Exception:
            pass
        return img, x0

    def draw_view(self, c, xa, xb):
        """Görünür aralıktaki kareaşları çiz (c: katman dönüşümü uygulanmış tuval)."""
        i0 = max(0, int(math.floor(xa / self.TWL)))
        i1 = min(self.n_tiles() - 1, int(math.floor(xb / self.TWL)))
        inv = 1.0 / self.scale
        for i in range(i0, i1 + 1):
            img, x0 = self.tile(i)
            c.save()
            c.translate(x0, self.y0)
            if inv != 1.0:
                c.scale(inv, inv)
            c.drawImage(img, 0, 0, LIN)
            c.restore()


# ═════════════════════════════ kamera yolu ═════════════════════════════
def pchip(ts, vs):
    """Tekdüze kübik Hermite (uçlarda eğim 0 → yumuşak başlama/bitiş). Dönüş: f(t)."""
    n = len(ts)
    ts = [float(t) for t in ts]
    vs = [float(v) for v in vs]
    if n == 1:
        return lambda t: vs[0]
    h = [ts[i + 1] - ts[i] for i in range(n - 1)]
    d = [(vs[i + 1] - vs[i]) / max(1e-9, h[i]) for i in range(n - 1)]
    m = [0.0] * n
    for i in range(1, n - 1):
        if d[i - 1] * d[i] <= 0:
            m[i] = 0.0
        else:
            w1 = 2 * h[i] + h[i - 1]
            w2 = h[i] + 2 * h[i - 1]
            m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i])

    def f(t):
        if t <= ts[0]:
            return vs[0]
        if t >= ts[-1]:
            return vs[-1]
        lo, hi = 0, n - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if ts[mid] <= t:
                lo = mid
            else:
                hi = mid
        u = (t - ts[lo]) / h[lo]
        u2, u3 = u * u, u * u * u
        return (2 * u3 - 3 * u2 + 1) * vs[lo] + (u3 - 2 * u2 + u) * h[lo] * m[lo] + (-2 * u3 + 3 * u2) * vs[lo + 1] + (u3 - u2) * h[lo] * m[lo + 1]
    return f


class PanoCam:
    """Anahtar karelerden (t,x,y,zoom) kamera. cams: [(çapa,(x,y[,zoom])),…] → cx.at ile yerel sn."""

    def __init__(self, cx, cams, default, dur):
        keys = []
        if cams:
            for a, v in cams:
                try:
                    t = cx.at(a)
                except Exception:
                    t = float(a) if isinstance(a, (int, float)) else 0.0
                keys.append((t, float(v[0]), float(v[1]) if len(v) > 1 else 0.0, float(v[2]) if len(v) > 2 else 1.0))
        else:
            for fr_, v in default:
                keys.append((fr_ * dur, float(v[0]), float(v[1]) if len(v) > 1 else 0.0, float(v[2]) if len(v) > 2 else 1.0))
        keys.sort(key=lambda k: k[0])
        # aynı zamanlı anahtar yok; en az 2
        if len(keys) == 1:
            keys.append((keys[0][0] + 1.0,) + keys[0][1:])
        self.keys = keys
        ts = [k[0] for k in keys]
        self.fx = pchip(ts, [k[1] for k in keys])
        self.fy = pchip(ts, [k[2] for k in keys])
        self.fz = pchip(ts, [k[3] for k in keys])

    def at(self, t):
        return self.fx(t), self.fy(t), max(0.5, self.fz(t))


# ═════════════════════════════ çekim bağlamı ═════════════════════════════
class Ctx:
    """Çekim içi çizim bağlamı: katman dönüşümü, görünür aralık, zaman, tod."""

    def __init__(self, f, cx, world, camx, camy, z, band, tod, alpha):
        self.f, self.c, self.cx, self.t = f, f.c, cx, cx.t
        self.world, self.camx, self.camy, self.z = world, camx, camy, z
        self.band = band                      # (y0, h)
        self.tod = tod
        self.night = tod == "night"
        self.alpha = alpha
        self.hc = 800 / 2 + OV                # görüntü merkezi (katman y)

    def Cx(self, fct):
        return W / 2 + (self.camx - W / 2) * fct

    def Cy(self, fct, dy=0.0):
        return self.hc + self.camy * fct + dy

    def view(self, fct, m=40):
        cxl = self.Cx(fct)
        half = W / (2 * self.z)
        return cxl - half - m, cxl + half + m

    def xf(self, fct, dy=0.0):
        """Katman dönüşümünü uygula (save'li; çağıran restore eder). dy>0: katman içeriği yukarı kayar."""
        c = self.c
        c.save()
        by0, bh = self.band
        c.translate(W / 2, by0 + bh / 2)
        c.scale(self.z, self.z)
        c.translate(-self.Cx(fct), -self.Cy(fct, dy))
        FA.set_scale_hint(self.z)

    def end(self):
        self.c.restore()
        FA.set_scale_hint(1.0)

    def to_screen(self, fct, x, y):
        by0, bh = self.band
        return W / 2 + (x - self.Cx(fct)) * self.z, by0 + bh / 2 + (y - self.Cy(fct)) * self.z


# ═════════════════════════════ dünya taban sınıfı ═════════════════════════════
class World:
    name = "base"
    PW = 8000
    interior = False

    def __init__(self, tod="day"):
        self.tod = tod
        self.T = CT.Tint(tod)
        self.layers = {}
        self.build()

    def build(self):
        pass

    def default_cams(self):
        return [(0.0, (960, 0, 1.0)), (1.0, (3000, 0, 1.0))]

    def default_stations(self):
        return []

    def interior_finish(self, ctx):
        pass

    def layer(self, name, f, width, draw, **kw):
        L = Layer(self.name, name, f, width, draw, tod=self.tod, **kw)
        self.layers[name] = L
        return L

    def bake_all(self, cam_x_range=None):
        """Tüm kareaşları önceden pişir (süre ölçümü / önbellek ısıtma)."""
        n = 0
        for L in self.layers.values():
            for i in range(L.n_tiles()):
                L.tile(i)
                n += 1
        return n


_WORLDS = {}


def get_world(name, tod):
    key = (name, tod)
    if key not in _WORLDS:
        _WORLDS[key] = WORLDS[name](tod)
    return _WORLDS[key]


WORLDS = {}


# ═════════════════════════════ ortak: kumaş (boyahane/tente) ═════════════════════════════
@functools.lru_cache(maxsize=128)
def cloth_sprite(col, col2, w, h, kind="dye", seed=0):
    """Asılı kumaş şeridi: üst kenarı sırığa bağlı; boya geçişi (üstte açık, altta doygun), dikey lif çizgileri, ink kenar."""
    fr = sk.Frame(int(w) + 12, int(h) + 12)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    c.translate(6, 6)
    rs = _RS(seed)
    if kind == "dye":
        sh = skia.GradientShader.MakeLinear([(0, 0), (0, h)], [C(mix(col, "#F2EBD9", 0.42)), C(col), C(mix(col, "#1A1008", 0.18))], [0.0, 0.45, 1.0])
        # alt kenar hafif dalgalı
        pts = [(0, 0), (w, 0)]
        n = 6
        for i in range(n + 1):
            pts.append((w - w * i / n, h + (4 if i % 2 else -3) * 0.9))
        path = sk.poly_path(pts)
        c.drawPath(path, skia.Paint(AntiAlias=True, Shader=sh))
        c.save()
        c.clipPath(path, skia.ClipOp.kIntersect, True)
        for i in range(int(w / 7)):
            x = rs.uniform(2, w - 2)
            c.drawLine(x, 0, x + rs.uniform(-3, 3), h, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=rs.uniform(0.8, 2.2), Color=C("#1A1008" if rs.rand() < 0.5 else "#FFFFFF", int(rs.uniform(14, 36)))))
        # boya damlama lekeleri (altta)
        for i in range(5):
            x = rs.uniform(4, w - 4)
            c.drawOval(skia.Rect.MakeXYWH(x, h - rs.uniform(10, 40), rs.uniform(4, 10), rs.uniform(10, 26)), skia.Paint(AntiAlias=True, Color=C(mix(col, "#000000", 0.25), 70)))
        # ikinci renk: alt şerit (daldırma çizgisi)
        c.drawRect(skia.Rect.MakeLTRB(0, h * 0.72, w, h * 0.76), skia.Paint(Color=C(col2, 120)))
        c.restore()
        INKP(c, path, 1.3, 190)
    else:   # tente: dikey şeritli
        n = max(4, int(w / 22))
        path = sk.poly_path([(0, 0), (w, 0), (w, h), (0, h)])
        for i in range(n):
            c.drawRect(skia.Rect.MakeLTRB(w * i / n, 0, w * (i + 1) / n, h), skia.Paint(Color=C(col if i % 2 == 0 else col2)))
        INKP(c, path, 1.3, 190)
    return FA.Spr(fr.surf.makeImageSnapshot(), 6, 6)


class ClothStrips:
    """Asılı kumaş: yatay şerit; dx(y) = genlik·(y/h)^1.5·sin(ωt − k y + φ) (rüzgâr dalgası; üst kenar sabit)."""
    _cache = {}

    @classmethod
    def get(cls, col, col2, w, h, kind="dye", seed=0):
        key = (col, col2, int(w), int(h), kind, seed)
        if key not in cls._cache:
            spr = cloth_sprite(col, col2, int(w), int(h), kind, seed)
            cls._cache[key] = FA.Strips(spr, 0, h + 8, step=max(5.0, h / 26.0))
        return cls._cache[key]


def draw_cloth(c, x, y_top, col, col2, w, h, t, ph=0.0, wind=1.0, kind="dye", seed=0, alpha=1.0):
    """(x = sol kenar, y_top = asılma çizgisi). Dönüş: yok."""
    cs = ClothStrips.get(col, col2, w, h, kind, seed)
    ycen = cs.ycen
    u = np.clip(ycen / max(1.0, h), 0.0, 1.0)
    amp = w * 0.13 * wind
    dx = amp * (u ** 1.5) * np.sin(t * 2.3 - u * 3.1 + ph) + 0.35 * amp * (u ** 1.2) * np.sin(t * 4.1 - u * 5.0 + ph * 1.7) + w * 0.03 * wind * u
    dy = np.zeros_like(u)
    exl = -w * 0.03 * u * np.sin(t * 1.9 + ph + u * 2.0) * wind
    exr = w * 0.03 * u * np.sin(t * 2.1 + ph + 1.0 + u * 2.0) * wind
    c.save()
    c.translate(x + cs.ox, y_top + cs.oy)
    cs.draw(c, dx, dy, exl, exr, alpha)
    c.restore()


# ═════════════════════════════ yardımcı yapı çizimleri (ana düzlem) ═════════════════════════════
STONE = "#B7A47C"
STONE_D = "#8E7C58"
PLASTER = "#E4D5AE"


def draw_parapet(c, x0, x1, ytop, ybot, T, seed=0):
    """Rıhtım korkuluk duvarı: taş bloklar + silme + ayaklar (top finial)."""
    R(c, x0, ytop, x1, ybot, T(STONE, 0.0))
    # taş sıraları
    rs = _RS(seed)
    nrow = max(2, int((ybot - ytop) / 16))
    for r in range(nrow):
        yy = ytop + r * (ybot - ytop) / nrow
        c.drawLine(x0, yy, x1, yy, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#4A3A22", 110)))
        off = (r % 2) * 30
        x = x0 - (x0 % 60) + off
        while x < x1:
            c.drawLine(x, yy, x, yy + (ybot - ytop) / nrow, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#4A3A22", 90)))
            x += 60
    # silme (coping)
    R(c, x0, ytop - 9, x1, ytop + 2, T("#CDBD94", 0.0))
    c.drawLine(x0, ytop - 9, x1, ytop - 9, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 170)))
    c.drawLine(x0, ytop + 2, x1, ytop + 2, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C(INK, 130)))
    # ayaklar
    px = x0 - (x0 % 520) + 260
    while px < x1 + 40:
        R(c, px - 22, ytop - 34, px + 22, ybot, T("#C4B288", 0.0))
        INKR(c, px - 22, ytop - 34, px + 22, ybot, 1.2, 150)
        R(c, px - 26, ytop - 40, px + 26, ytop - 32, T("#D6C8A0", 0.0))
        INKR(c, px - 26, ytop - 40, px + 26, ytop - 32, 1.0, 140)
        OVAL(c, px, ytop - 52, 11, 11, T("#CDBD94", 0.0))
        c.drawOval(skia.Rect.MakeLTRB(px - 11, ytop - 63, px + 11, ytop - 41), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.1, Color=C(INK, 150)))
        shade_right(c, px - 22, ytop - 34, px + 22, ybot, 40)
        px += 520


def draw_pavement(c, x0, x1, ytop, ybot, T, seed=0):
    """Kaldırım: taş döşeme sıraları (perspektif gibi aralık büyür) + çatlak."""
    R(c, x0, ytop, x1, ybot, T("#BCAC86", 0.0))
    sh = skia.GradientShader.MakeLinear([(0, ytop), (0, ybot)], [C("#3A2A18", 70), C("#3A2A18", 0)], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(x0, ytop, x1, ytop + 24), skia.Paint(Shader=sh))
    y = ytop
    k = 0
    gap = 12.0
    while y < ybot:
        c.drawLine(x0, y, x1, y, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.0 + k * 0.18, Color=C("#4A3A22", 100)))
        off = (k % 2) * 45
        x = x0 - (x0 % 90) + off
        while x < x1:
            c.drawLine(x, y, x - 4 - k, y + gap * 1.3, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#4A3A22", 80)))
            x += 90 + k * 4
        y += gap
        gap *= 1.20
        k += 1
    rs = _RS(seed)
    for i in range(int((x1 - x0) / 60)):
        x = rs.uniform(x0, x1)
        y = rs.uniform(ytop + 4, ybot)
        OVAL(c, x, y, rs.uniform(2, 5), rs.uniform(1, 2.5), "#6A5A3A", 90)


def draw_pole(c, x, ybase, ytop, w=9, col="#6A4A2C"):
    R(c, x - w / 2, ytop, x + w / 2, ybase, col)
    INKR(c, x - w / 2, ytop, x + w / 2, ybase, 1.1, 150)
    c.drawRect(skia.Rect.MakeLTRB(x + w * 0.15, ytop, x + w / 2, ybase), skia.Paint(Color=C("#1A1008", 40)))


def draw_roundel(c, x, y, r, col="#B33620", rim="#E0B84E"):
    OVAL(c, x, y, r, r, rim)
    OVAL(c, x, y, r * 0.72, r * 0.72, col)
    c.drawOval(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.1, Color=C(INK, 150)))
    OVAL(c, x - r * 0.25, y - r * 0.28, r * 0.24, r * 0.2, "#FFFFFF", 70)


def draw_arch_opening(c, x, ybase, w, h, T, inner="#3A2A1C", ink=True):
    """Yuvarlak kemerli açıklık (koyu iç)."""
    p = skia.Path()
    r = w / 2
    p.moveTo(x - r, ybase)
    p.lineTo(x - r, ybase - h + r)
    p.arcTo(skia.Rect.MakeLTRB(x - r, ybase - h, x + r, ybase - h + 2 * r), 180, 180, False)
    p.lineTo(x + r, ybase)
    p.close()
    c.drawPath(p, skia.Paint(AntiAlias=True, Color=C(T(inner, 0.0))))
    if ink:
        INKP(c, p, 1.4, 190)
    return p


def draw_column(c, x, ybase, h, w, T, col="#A9A89C", capital=True):
    """Pietra serena sütun: gövde + taban + başlık (Brunelleschi tarzı)."""
    R(c, x - w / 2, ybase - h, x + w / 2, ybase, T(col, 0.0))
    sh = skia.GradientShader.MakeLinear([(x - w / 2, 0), (x + w / 2, 0)], [C("#FFFFFF", 50), C("#FFFFFF", 0), C("#1A1008", 55)], [0, 0.35, 1.0])
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, ybase - h, x + w / 2, ybase), skia.Paint(Shader=sh))
    INKR(c, x - w / 2, ybase - h, x + w / 2, ybase, 1.2, 160)
    # taban
    R(c, x - w * 0.68, ybase - w * 0.34, x + w * 0.68, ybase, T("#9C9B90", 0.0))
    INKR(c, x - w * 0.68, ybase - w * 0.34, x + w * 0.68, ybase, 1.1, 150)
    if capital:
        R(c, x - w * 0.72, ybase - h - w * 0.18, x + w * 0.72, ybase - h + 2, T("#B4B3A6", 0.0))
        INKR(c, x - w * 0.72, ybase - h - w * 0.18, x + w * 0.72, ybase - h + 2, 1.1, 150)
        R(c, x - w * 0.9, ybase - h - w * 0.34, x + w * 0.9, ybase - h - w * 0.18, T("#BDBCAE", 0.0))
        INKR(c, x - w * 0.9, ybase - h - w * 0.34, x + w * 0.9, ybase - h - w * 0.18, 1.1, 150)


_CLOUD = {}


def cloud_sprite():
    """Yumuşak bulut sprite'ı (bir kez pişirilir)."""
    if "c" not in _CLOUD:
        fr = sk.Frame(460, 100)
        fr.clear(skia.ColorTRANSPARENT)
        rs = _RS(3)
        for k in range(5):
            x = 40 + k * 70 + rs.uniform(-10, 10)
            fr.c.drawOval(skia.Rect.MakeLTRB(x, 50 - 22 - rs.uniform(0, 8) - (k % 2) * 6, x + 190, 50 + 20), skia.Paint(AntiAlias=True, Color=C("#FFFFFF", 80), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 9)))
        _CLOUD["c"] = fr.surf.makeImageSnapshot()
    return _CLOUD["c"]


_GS = {}
_GP = skia.Paint()
SRC128 = skia.Rect.MakeWH(128, 128)


def glow_sprite(col):
    """Önceden renklendirilmiş 128² radyal parıltı sprite'ı (renk filtresi/kPlus bu CPU'da ≈6× yavaş; srcover + LIN ≈ 2–5 ms)."""
    im = _GS.get(col)
    if im is None:
        n = 128
        fr = sk.Frame(n, n)
        fr.clear(skia.ColorTRANSPARENT)
        sh = skia.GradientShader.MakeRadial((n / 2, n / 2), n / 2, [C(col, 255), C(col, 96), C(col, 0)], [0.0, 0.28, 1.0])
        fr.c.drawCircle(n / 2, n / 2, n / 2, skia.Paint(Shader=sh))
        im = _GS[col] = fr.surf.makeImageSnapshot()
    return im


def glow(c, x, y, r, col, a, plus=True):
    _GP.setAlphaf(clamp(a))
    c.drawImageRect(glow_sprite(col), SRC128, skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), LIN, _GP)


def tint_mode(tod):
    return "night" if tod == "night" else "day"


# ═════════════════════════════ çekim türü ═════════════════════════════
_FRAME_BAND = (150, 800)


def _wall_and_frame(f, cx, band, frame, a, seed, mode_night):
    """Duvar arka planı + (isteğe bağlı) asma bandı çerçevesi. Dönüş: yok."""
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)


@ckind("pano")
def k_pano(cx, pano="florence", tod=None, cams=None, stations=None, kick=None, caption=None, at=0.0, frame=True, seed=1, band=None, **_):
    """Uzun plan panoraması. pano: florence | nave | corridor. tod: day | dusk | night (yoksa moda göre).
    cams=[(çapa,(x,y,zoom)),…]: x = görüntü merkezinin ana düzlem x'i (başlangıç ≈ 960), y = dikey kayma (px, + aşağı), zoom ≥ 1 (≈1,0–1,5);
    çapa saniye ya da ("c7s5","sözcük",−0.1) olabilir; verilmezse dünyaya özgü varsayılan yol çekim süresine yayılır (ease_io ile başlar/biter).
    stations=[dict(x=…, at=çapa, fn=callable(ctx, st), …)]: ana düzlemde x noktasında canlanan sahne; verilmezse dünyanın varsayılanları. stations=[] → yok.
    frame=True: duvar + asma bantlı fresk şeridi (y 150–950); False: tam ekran. cam/link/longtake/montage yok sayılır; kick/caption: metin."""
    f = cx.f
    night_theme = not TH.day
    tod = tod or ("night" if night_theme else "day")
    if band is None:
        band = (150, 800) if frame else (0, 800)
    world = get_world(pano, tod)
    c = f.c
    a = cx.amt(at, 0.9) if at else 1.0
    dur = max(cx.dur, 1e-3)
    pc = PanoCam(cx, cams, world.default_cams(), dur)
    t_cam = clamp(cx.t, 0.0, dur)
    camx, camy, z = pc.at(t_cam)
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    c.save()
    mb0, mbh = band
    c.clipRect(skia.Rect.MakeLTRB(0, 0, W, mb0 + 2))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    c.restore()
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, mb0 + mbh - 2, W, H))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    c.restore()
    ctx = Ctx(f, cx, world, camx, camy, z, band if frame else (0, 800), tod, a)
    ctx.band = (band[0], band[1])
    if not frame:
        ctx.band = (140, 800)
    sts = stations if stations is not None else world.default_stations()
    ctx.stations = []
    for s_ in sts:
        s2 = dict(s_)
        if "at_frac" in s2 and "at" not in s2:
            s2["_at"] = float(s2["at_frac"]) * dur
        else:
            try:
                s2["_at"] = cx.at(s2.get("at", 0.0))
            except Exception:
                s2["_at"] = float(s2.get("at", 0.0)) if isinstance(s2.get("at", 0.0), (int, float)) else 0.0
        ctx.stations.append(s2)
    by0, bh = ctx.band
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, by0, W, by0 + bh))
    for item in world.stack(ctx):
        kind = item[0]
        if kind == "L":
            L = world.layers[item[1]]
            dy_ = item[2] if len(item) > 2 else 0.0
            ctx.xf(L.f, dy_)
            xa, xb = ctx.view(L.f)
            L.draw_view(c, xa, xb)
            ctx.end()
        elif kind == "D":
            fct = item[2]
            dy_ = item[3] if len(item) > 3 else 0.0
            ctx.xf(fct, dy_)
            xa, xb = ctx.view(fct)
            ctx.xa, ctx.xb = xa, xb
            getattr(world, item[1])(ctx)
            ctx.end()
    c.restore()
    if frame:
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
    if world.interior:
        world.interior_finish(ctx)
        CM.vig(f, 0.55 if tod != "night" else 0.78)
    elif tod == "night":
        CM.finish(f, cx, motes_n=22, light=CM.candle_light(cx.t, seed, base=(W * 0.5, H * 0.46), r=1500.0, sway=12.0))
    else:
        CM.finish(f, cx, motes_n=26)


_TINT = {}


def tint_overlay(c, y0, h, stops, pos):
    """Bant boyunca dikey degrade örtü — bir kez pişirilir (degrade dolgusu kare başına 25 ms; blit ≈2 ms)."""
    key = (int(y0), int(h), tuple(stops), tuple(pos))
    img = _TINT.get(key)
    if img is None:
        fr = sk.Frame(W, int(h))
        fr.clear(skia.ColorTRANSPARENT)
        sh = skia.GradientShader.MakeLinear([(0, 0), (0, h)], [C(c_, a_) for c_, a_ in stops], list(pos))
        fr.c.drawRect(skia.Rect.MakeLTRB(0, 0, W, h), skia.Paint(Shader=sh))
        img = _TINT[key] = fr.surf.makeImageSnapshot()
    c.drawImage(img, 0, y0)


def bake_world(pano, tod="day"):
    """Tüm kareaşları pişir; (kareaş sayısı, sn)."""
    t0 = time.perf_counter()
    w = get_world(pano, tod)
    n = w.bake_all()
    return n, time.perf_counter() - t0


# ═════════════════════════════ FLORANSA (Arno kıyısı, Ponte Vecchio, boyahane, tezgâhlar, bankacı, Duomo'ya yürüyüş) ═════════════════════════════
YG = 846            # ana düzlem ayak hizası (görüntü y)
Y_PARA_TOP, Y_PARA_BOT = 768, 824
Y_WATER = 652       # su hattı (uzak kıyı tabanı)
Y_FAR = 548         # uzak şehir tabanı
DYE_COLS = [("#1E3A8A", "#7FA3E8"), ("#B3361F", "#E8745A"), ("#E2A83A", "#F4DE90"), ("#3E7A8A", "#9CC8C0"), ("#6E3A7A", "#B88ABE"), ("#4E7A3A", "#A8C078"), ("#8E3342", "#D88A96"), ("#2F5FB8", "#9CB8E8")]


def _lit_boxes(c, rs, boxes, night, p):
    """Pencere ışıkları (gece): boxes=[(x,y,w,h)] → yanan kutular."""
    out = []
    if not night:
        return out
    for (x, y, w, h) in boxes:
        if rs.rand() < p:
            c.drawRect(skia.Rect.MakeXYWH(x - 3, y - 3, w + 6, h + 6), skia.Paint(AntiAlias=True, Color=C("#FFB04A", 55), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 3)))
            c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), skia.Paint(AntiAlias=True, Color=C("#FFD27A")))
            out.append((x, y, w, h))
    return out


class Florence(World):
    name = "florence"
    PW = 13400
    interior = False

    # ── dünya kurulumu ──────────────────────────────────────────────────────
    def build(self):
        PW = self.PW
        rs = _RS(11)
        cam_span = PW - W

        def Lw(f):
            return int(W + cam_span * f + 500)
        self.XD = 3700                                                    # Duomo x (şehir katmanında; kamera x≈9300'de ekranın biraz sağında)
        self.XB = int(960 + (4500 - 960) * 0.55)                         # köprü x (banka katmanında)
        self.layer("sky", 0.05, Lw(0.05), self._draw_sky, opaque=True, scale=0.5, wear=3, loss=0.5, yr=(0, 700))
        self.layer("hills", 0.14, Lw(0.14), self._draw_hills, scale=0.5, wear=2, yr=(330, 800))
        # şehir silueti
        self.city_houses = []
        x = -40
        rr = _RS(5)
        while x < Lw(0.30) + 60:
            bw, bh = rr.uniform(34, 74), rr.uniform(30, 70)
            self.city_houses.append((x, bw, bh, int(rr.randint(1, 10 ** 6)), 0.46, 0))
            x += bw + rr.uniform(-4, 8)
        x = 20
        while x < Lw(0.30) + 60:
            bw, bh = rr.uniform(40, 80), rr.uniform(34, 76)
            self.city_houses.append((x, bw, bh, int(rr.randint(1, 10 ** 6)), 0.26, 20))
            x += bw + rr.uniform(-6, 6)
        self.layer("city", 0.30, Lw(0.30), self._draw_city, wear=2, yr=(60, 620))
        # uzak kıyı + köprü + su
        self.bank_houses = []
        x = -30
        rr = _RS(9)
        while x < Lw(0.55) + 60:
            bw, bh = rr.uniform(58, 118), rr.uniform(46, 104)
            if abs((x + bw / 2) - self.XB) < 480:
                x += bw
                continue
            self.bank_houses.append((x, bw, bh, int(rr.randint(1, 10 ** 6))))
            x += bw + rr.uniform(-10, 6)
        self.layer("bank", 0.55, Lw(0.55), self._draw_bank, wear=3, yr=(300, 812))
        self.layer("river", 0.80, Lw(0.80), self._draw_river, yr=(640, 800))
        # ana düzlem: raflar, tezgâhlar, revak
        self.racks = []
        for (x0, n) in ((560, 4), (1300, 4), (2050, 2)):
            self.racks.append(dict(x0=x0, n=n, dx=210))
        self.stalls = []
        for i, x in enumerate((2300, 2900, 3500, 7100, 7700, 8300)):
            self.stalls.append(dict(x=x, w=230, kind=["cloth", "fruit", "pots", "bread", "cloth", "fruit"][i % 6], seed=i))
        self.LOG = (5100, 6460)
        self.lamps = [900, 2500, 4300, 6700, 8200, 9800, 11400, 12900]
        self.layer("main", 1.0, PW, self._draw_main, wear=4)
        # çevre yaşamı (ambient yürüyenler)
        rr = _RS(21)
        self.walkers = []
        kinds = ["halk", "tuccar", "soylu", "soylu_f", "cocuk", "denizci", "banker", "kesis", "asker", "halk", "rahip"]
        x = 400
        while x < PW - 400:
            k = kinds[rr.randint(len(kinds))]
            h = rr.uniform(215, 262) if k != "cocuk" else rr.uniform(225, 250)
            self.walkers.append(dict(x0=x + rr.uniform(-120, 120), dir=1 if rr.rand() < 0.68 else -1, w=rr.uniform(52, 105), kind=k, seed=int(rr.randint(0, 999)), h=h, y=YG + rr.uniform(-4, 18),
                                     phase=rr.rand(), prop=(["sack", "basket", "book", "staff"][rr.randint(4)] if rr.rand() < 0.28 and k in ("halk", "tuccar", "kesis", "banker", "soylu_f") else None)))
            x += rr.uniform(320, 640)
        # çocuklar / koşan
        self.boats = [dict(x0=2400, v=34.0, kind="barge", seed=1), dict(x0=6300, v=-26.0, kind="barge", seed=2), dict(x0=9800, v=30.0, kind="boat", seed=3)]
        self.cloud_seed = 4

    def default_cams(self):
        return [(0.0, (960, 0, 1.0)), (0.20, (2150, 0, 1.0)), (0.44, (4450, 0, 1.0)), (0.60, (5620, 60, 1.38)), (0.74, (5860, 52, 1.34)), (0.88, (7900, 0, 1.06)), (1.0, (9300, -10, 1.0))]

    def default_stations(self):
        return [dict(x=1500, fn=st_dyers), dict(x=2950, fn=st_market), dict(x=5600, fn=st_banker), dict(x=8100, fn=st_duomo_walk)]

    def stack(self, ctx):
        return [("L", "sky"), ("D", "dyn_sky", 0.05), ("L", "hills"), ("L", "city"), ("D", "dyn_city", 0.30), ("L", "bank"), ("D", "dyn_bank", 0.55), ("L", "river"), ("D", "dyn_river", 0.80),
                ("L", "main"), ("D", "dyn_main", 1.0), ("D", "dyn_front", 1.38)]

    # ── katman boyaları ─────────────────────────────────────────────────────
    def _draw_sky(self, fr, xa, xb):
        c = fr.c
        T = self.T
        top, mid, hor = {"day": ("#6F9ED6", "#BDD0DC", "#F4E8C8"), "dusk": ("#4E5E9E", "#E8A07A", "#F8D9A0"), "night": ("#080F30", "#17286A", "#4F6AA8")}[self.tod]
        GRAD_V(c, xa, 0, xb, 760, [(top, 0.0), (mid, 0.55), (hor, 1.0)])
        R(c, xa, 759, xb, 960, hor)
        rs = _RS(int(xa) // 7 + 3)
        if self.tod == "night":
            for i in range(int((xb - xa) / 10)):
                c.drawCircle(rs.uniform(xa, xb), rs.uniform(OV, 520), rs.uniform(0.8, 2.1), skia.Paint(AntiAlias=True, Color=C("#FFF2C4", int(rs.uniform(80, 235)))))
            # hilal: sabit katman x'inde
            mx, my = 1500, 210
            if xa - 120 < mx < xb + 120:
                c.drawCircle(mx, my, 80, skia.Paint(AntiAlias=True, Color=C("#FFF1C0", 36), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 34)))
                disc = skia.Path()
                disc.addCircle(mx, my, 36)
                cut = skia.Path()
                cut.addCircle(mx - 15, my - 9, 31)
                try:
                    cres = skia.Op(disc, cut, skia.PathOp.kDifference_PathOp)
                except Exception:
                    cres = disc
                c.drawPath(cres or disc, skia.Paint(AntiAlias=True, Color=C("#FFF3CE")))
        else:
            # yumuşak ufuk bulutları (statik ince bantlar)
            for i in range(int((xb - xa) / 380) + 1):
                x = xa + rs.uniform(0, 380) + i * 380
                y = rs.uniform(OV + 40, 420)
                for k in range(3):
                    c.drawOval(skia.Rect.MakeLTRB(x + k * 70, y - 8, x + k * 70 + 210, y + 12), skia.Paint(AntiAlias=True, Color=C("#FFFFFF", 42), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8)))

    def _draw_hills(self, fr, xa, xb):
        c = fr.c
        T = self.T
        for (col, amp, sc, base, ph) in (("#A9BDB6", 40, 600, 392, 0.0), ("#93AFA5", 46, 420, 440, 2.1), ("#7F9E92", 52, 300, 486, 4.3)):
            cc = T(col, 0.2)
            pts = []
            x = xa - 8
            while x <= xb + 8:
                pts.append((x, ridge_y(x, base, amp, sc, ph)))
                x += 8
            poly = pts + [(pts[-1][0], 960), (pts[0][0], 960)]
            c.drawPath(sk.poly_path(poly), skia.Paint(AntiAlias=True, Color=C(cc)))
            c.drawPath(sk.poly_path(pts, False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, Color=C(mix(cc, "#1A2A22", 0.5), 150)))
            gx0 = int(xa // 150) - 1
            for gi in range(gx0, int(xb // 150) + 2):
                r_ = _RS(gi * 7 + int(ph * 10))
                if r_.rand() < 0.55:
                    x = gi * 150 + r_.uniform(0, 150)
                    y = ridge_y(x, base, amp, sc, ph)
                    SC.cypress(c, x, y + 3, r_.uniform(28, 52), T("#2E4A33", 0.3), T("#4F6E4A", 0.3))
                if r_.rand() < 0.10:
                    SC.castle(c, gi * 150 + 70, ridge_y(gi * 150 + 70, base, amp, sc, ph) + 3, r_.uniform(28, 40), T("#E6D9B8", 0.3), T("#B4552E", 0.3))

    def _draw_city(self, fr, xa, xb):
        c = fr.c
        T = self.T
        night = self.tod == "night"
        wins = []
        for (x, bw, bh, sd, dep, dy) in self.city_houses:
            if x + bw < xa - 60 or x > xb + 60:
                continue
            rs = _RS(sd)
            CT.draw_house(c, x, Y_FAR + dy + (rs.rand() * 8 - 4), bw, bh, rs, T, dep, wins)
        XD = self.XD
        base = Y_FAR
        # anıtlar: (x, çizici)
        def at(x0, x1):
            return x1 > xa - 700 and x0 < xb + 700
        if at(XD - 2300, XD + 1400):
            # Santa Croce, kuleler, Palazzo Vecchio
            c.save()
            draw = CT.draw_tower
            draw(c, XD - 1800, base, 32, 190, T, 0.30, spire=True)
            for tx, th in ((XD - 1500, 130), (XD - 880, 150), (XD - 520, 140), (XD + 940, 156), (XD + 1260, 126)):
                draw(c, tx, base, 30, th, T, 0.35)
            c.save()
            c.translate(XD - 1150, base)
            c.scale(1.18, 1.18)
            c.translate(-(XD - 1150), -base)
            self.flag = CT.draw_pv(c, XD - 1150, base + 4, 1.0, T, 0.18)
            self.flag = (XD - 1150 + (self.flag[0] - (XD - 1150)) * 1.18, base + (self.flag[1] - base) * 1.18)
            c.restore()
            # Duomo grubu (ölçek 1,25)
            c.save()
            c.translate(XD, base)
            c.scale(1.25, 1.25)
            c.translate(-XD, -base)
            CT.draw_dome(c, XD + 1000, base - 18, 120, 82, 32, 44, T, 0.28)
            CT.draw_nave(c, XD + 70, XD + 640, base + 4, 124, T, 0.16)
            CT.draw_bapt(c, XD + 700, base + 6, 96, 64, T, 0.12)
            CT.draw_dome(c, XD, base - 108, 214, 132, 48, 74, T, 0.12)
            CT.draw_campanile(c, XD + 205, base + 4, 54, 262, T, 0.12)
            c.restore()
            c.restore()
        if night:
            _lit_boxes(c, _RS(int(xa) % 997 + 1), [b for b in wins], True, 0.42)

    def _draw_bank(self, fr, xa, xb):
        c = fr.c
        T = self.T
        night = self.tod == "night"
        # su gövdesi (uzak kıyı tabanından aşağı)
        GRAD_V(c, xa, Y_WATER - 2, xb, 800, [(T("#8FB0B0", 0.1), 0.0), (T("#4E7C86", 0.0), 0.5), (T("#2E566A", 0.0), 1.0)])
        wins = []
        rec = []
        for (x, bw, bh, sd) in self.bank_houses:
            if x + bw < xa - 60 or x > xb + 60:
                continue
            rs = _RS(sd)
            CT.draw_house(c, x, Y_WATER - 8 + rs.uniform(-3, 2), bw, bh, rs, T, 0.06, wins, rec=rec)
        # kıyı duvarı
        R(c, xa, Y_WATER - 10, xb, Y_WATER + 4, T("#9C8B6C", 0.0))
        c.drawLine(xa, Y_WATER + 4, xb, Y_WATER + 4, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=C(INK, 150)))
        # servi
        for gi in range(int(xa // 230) - 1, int(xb // 230) + 2):
            r_ = _RS(gi * 13 + 5)
            if r_.rand() < 0.45:
                x = gi * 230 + r_.uniform(0, 230)
                if abs(x - self.XB) < 480:
                    continue
                SC.cypress(c, x, Y_WATER - 8, r_.uniform(90, 150), T("#2E4A33", 0.0), T("#4F6E4A", 0.0))
        # Ponte Vecchio (ölçek 1,55)
        XB = self.XB
        if xb > XB - 800 and xa < XB + 800:
            c.save()
            c.translate(XB, Y_WATER + 2)
            c.scale(1.9, 1.9)
            bw_ = []
            CT.draw_bridge(c, 0, -66, 430, T, _RS(3), bw_)
            if night:
                _lit_boxes(c, _RS(8), bw_, True, 0.7)
            c.restore()
        if night:
            _lit_boxes(c, _RS(int(xa) % 991 + 2), wins, True, 0.5)
        # yansıma: kıyı + köprü satırının suya ters kopyası (dalga şeritleri)
        self._cur_y0 = self.layers["bank"].y0
        self._reflect(fr, xa, xb, Y_WATER + 4, 150)

    def _reflect(self, fr, xa, xb, yw, depth):
        c = fr.c
        # tuvalin yerel görüntüsünden (şu ana kadar çizilen) yansıma
        img = fr.surf.makeImageSnapshot()
        s = 1.0
        # kaynak: piksel uzayı (tile: ölçek 1, c.translate(-x0)) → x0 = xa
        x0px = 0
        wpx = img.width()
        ytop = int(yw - depth - self._cur_y0)
        sub = img.makeSubset(skia.IRect.MakeLTRB(0, ytop, wpx, int(yw - self._cur_y0)))
        for k in range(int(depth / 5)):
            yy = yw + k * 5
            srcy0 = depth - (k + 1) * 5
            dxw = math.sin(yy * 0.37 + xa * 0.01) * 2.2 * (0.4 + k / 30.0)
            a = 0.34 * (1 - k / (depth / 5.0)) ** 1.2
            pt = skia.Paint()
            pt.setAlphaf(a)
            c.save()
            c.resetMatrix()
            c.drawImageRect(sub, skia.Rect.MakeLTRB(0, srcy0, wpx, srcy0 + 5), skia.Rect.MakeLTRB(dxw, yy - self._cur_y0, wpx + dxw, yy - self._cur_y0 + 5.6), LIN, pt)
            c.restore()

    def _draw_river(self, fr, xa, xb):
        """Yakın su: yarı saydam dalga çizgileri + köpük (paralaks derinliği)."""
        c = fr.c
        T = self.T
        rs = _RS(int(xa) // 3 + 77)
        for i in range(int((xb - xa) / 14)):
            yy = rs.uniform(Y_WATER + 22, 770)
            k = (yy - Y_WATER) / 118.0
            x = rs.uniform(xa, xb)
            L = rs.uniform(14, 60) * (0.7 + k)
            col = "#FFFFFF" if rs.rand() < 0.6 else "#1E3A4A"
            c.drawLine(x, yy, x + L, yy, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2 + 1.3 * k, Color=C(col, int(rs.uniform(30, 80))), StrokeCap=skia.Paint.kRound_Cap))

    def _draw_main(self, fr, xa, xb):
        c = fr.c
        T = self.T
        night = self.tod == "night"
        draw_pavement(c, xa, xb, Y_PARA_BOT, 960, T, seed=int(xa) // 1024)
        draw_parapet(c, xa, xb, Y_PARA_TOP, Y_PARA_BOT, T, seed=3)
        # kayıt: kıyıya inen merdiven boşlukları (koyu)
        # boya rafları: direkler + ip
        for rk in self.racks:
            n, dx = rk["n"], rk["dx"]
            xs = [rk["x0"] + i * dx for i in range(n + 1)]
            if xs[-1] < xa - 60 or xs[0] > xb + 60:
                continue
            for x in xs:
                draw_pole(c, x, YG - 6, YG - 340, 11)
                R(c, x - 12, YG - 12, x + 12, YG - 4, T("#7A5A34", 0.0))
            for i in range(n):
                LINE(c, xs[i], YG - 336, xs[i + 1], YG - 336, "#4A3220", 2.6, 255)
                LINE(c, xs[i], YG - 336, xs[i + 1], YG - 330, "#4A3220", 1.0, 160)
        # tezgâh direkleri + tente
        for s_ in self.stalls:
            x, w = s_["x"], s_["w"]
            if x + w < xa - 60 or x > xb + 60:
                continue
            draw_pole(c, x, Y_PARA_BOT + 12, YG - 258, 10)
            draw_pole(c, x + w, Y_PARA_BOT + 12, YG - 258, 10)
            rs = _RS(s_["seed"] + 3)
            c1, c2 = [("#B3361F", "#EDE4CC"), ("#233C8C", "#EDE4CC"), ("#2E6A4F", "#EDE4CC"), ("#C79A3C", "#EDE4CC")][rs.randint(4)]
            ytp = YG - 262
            ten = [(x - 20, ytp), (x + w + 20, ytp), (x + w + 36, ytp + 50), (x - 36, ytp + 50)]
            p = sk.poly_path(ten)
            c.drawPath(p, skia.Paint(AntiAlias=True, Color=C(T(c1, 0.0))))
            c.save()
            c.clipPath(p, skia.ClipOp.kIntersect, True)
            nst = int((w + 72) / 24)
            for i in range(0, nst, 2):
                c.drawRect(skia.Rect.MakeLTRB(x - 36 + i * (w + 72) / nst, ytp, x - 36 + (i + 1) * (w + 72) / nst, ytp + 52), skia.Paint(Color=C(T(c2, 0.0))))
            c.restore()
            INKP(c, p, 1.4, 190)
            # saçak (kavisli)
            for i in range(nst):
                xx = x - 36 + (i + 0.5) * (w + 72) / nst
                c.drawOval(skia.Rect.MakeLTRB(xx - (w + 72) / nst / 2, ytp + 44, xx + (w + 72) / nst / 2, ytp + 62), skia.Paint(AntiAlias=True, Color=C(T(c1 if i % 2 == 0 else c2, 0.0))))
                c.drawOval(skia.Rect.MakeLTRB(xx - (w + 72) / nst / 2, ytp + 44, xx + (w + 72) / nst / 2, ytp + 62), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C(INK, 150)))
        # revak (bankacı)
        L0, L1 = self.LOG
        if L1 > xa - 80 and L0 < xb + 80:
            self._draw_loggia(c, L0, L1, T)
        # sokak lambaları (direk + fener)
        for lx in self.lamps:
            if lx < xa - 40 or lx > xb + 40:
                continue
            draw_pole(c, lx, Y_PARA_BOT + 8, YG - 300, 9, "#3A2A1C")
            R(c, lx - 14, YG - 330, lx + 14, YG - 300, T("#8A7A5A", 0.0))
            INKR(c, lx - 14, YG - 330, lx + 14, YG - 300, 1.2, 170)
            POLY(c, [(lx - 18, YG - 330), (lx, YG - 346), (lx + 18, YG - 330)], T("#6E3A22", 0.0), 255, 1.2)
            if not night:
                R(c, lx - 9, YG - 326, lx + 9, YG - 304, "#F6E8B8", 200)
        # üst: çatılı pencereler yok (kıyı); uçta Duomo meydanı sütunları
        for ci in (9400, 9640, 9880):
            if xa - 60 < ci < xb + 60:
                draw_column(c, ci, YG - 6, 230, 34, T)
        if xa - 80 < 9400 < xb + 80 or xa - 80 < 9880 < xb + 80:
            R(c, 9400 - 30, YG - 6 - 230 - 28, 9880 + 30, YG - 6 - 230 - 8, T("#B4B3A6", 0.0))
            INKR(c, 9400 - 30, YG - 6 - 230 - 28, 9880 + 30, YG - 6 - 230 - 8, 1.2, 160)

    def _draw_loggia(self, c, L0, L1, T):
        base = YG - 6
        h_ar = 262
        top = base - h_ar
        # arkadaki sağır duvar (kemer aralıkları + revak içi)
        R(c, L0, top - 12, L1, base, T("#D3C198", 0.0))
        # üst kat duvarı + çatı
        GRAD_V(c, L0, top - 112, L1, top - 10, [(T("#E4D5AE", 0.0), 0.0), (T("#CDBB92", 0.0), 1.0)])
        POLY(c, [(L0 - 24, top - 110), (L0 + 70, top - 152), (L1 - 70, top - 152), (L1 + 24, top - 110)], T("#B4552E", 0.0), 255, 1.4)
        for k in range(1, 7):
            yy = top - 110 - k * 6.2
            c.drawLine(L0 - 18 + k * 11, yy, L1 + 18 - k * 11, yy, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#5A2412", 70)))
        INKR(c, L0, top - 110, L1, top - 10, 1.4, 170)
        # palle frizi
        R(c, L0, top - 46, L1, top - 10, T("#E0C98A", 0.0))
        n = int((L1 - L0) / 56)
        for i in range(n):
            draw_roundel(c, L0 + 28 + i * (L1 - L0 - 56) / max(1, n - 1), top - 28, 13, T("#B33620", 0.0))
        c.drawLine(L0, top - 46, L1, top - 46, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 170)))
        c.drawLine(L0, top - 10, L1, top - 10, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 170)))
        # üst kat pencereleri
        nw = int((L1 - L0) / 150)
        for i in range(nw):
            wx = L0 + 90 + i * (L1 - L0 - 180) / max(1, nw - 1)
            draw_arch_opening(c, wx, top - 60, 36, 44, T, "#3A2A1C")
        # alt katın kemerleri: koyu iç + sütunlar
        nar = 6
        step = (L1 - L0) / nar
        for i in range(nar):
            ax = L0 + (i + 0.5) * step
            draw_arch_opening(c, ax, base, step - 54, h_ar - 36, T, "#4A3826")
            if i % 2 == 0:
                for sy in (base - 120, base - 165):
                    R(c, ax - 36, sy, ax + 36, sy + 5, "#6A4A2C", 230)
        for i in range(nar + 1):
            draw_column(c, L0 + i * step, base, h_ar - 32, 34, T)
        for i in range(nar):
            ax = L0 + (i + 0.5) * step
            rr = (step - 54) / 2 + 8
            p = skia.Path()
            p.moveTo(ax - rr, base - h_ar + 36 + rr)
            p.arcTo(skia.Rect.MakeLTRB(ax - rr, base - h_ar + 36, ax + rr, base - h_ar + 36 + 2 * rr), 180, 180, False)
            c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5.0, Color=C(T("#C9C6B4", 0.0))))
            INKP(c, p, 1.2, 150)

    # ── dinamik geçişler ────────────────────────────────────────────────────
    def dyn_sky(self, ctx):
        c = ctx.c
        t = ctx.t
        if ctx.night:
            return
        xa, xb = ctx.xa, ctx.xb
        rs = _RS(self.cloud_seed)
        spr = cloud_sprite()
        pt = skia.Paint()
        for i in range(14):
            x0 = rs.uniform(0, self.layers["sky"].width)
            y = rs.uniform(OV + 40, 330)
            L = rs.uniform(220, 460)
            sp = rs.uniform(5, 13)
            a = rs.uniform(0.55, 0.95)
            x = (x0 + t * sp) % (self.layers["sky"].width + 400) - 200
            if x + L < xa - 20 or x > xb + 20:
                continue
            pt.setAlphaf(a)
            c.drawImageRect(spr, skia.Rect.MakeWH(spr.width(), spr.height()), skia.Rect.MakeXYWH(x, y - L * 0.11, L, L * 0.22), LIN, pt)

    def dyn_city(self, ctx):
        c, t = ctx.c, ctx.t
        fl = getattr(self, "flag", None)
        if fl is not None:
            from cilt_kinds4 import _pennant
            _pennant(ctx.f, fl[0] + 1.0, fl[1] + 3, t, 1.0)
        # Duomo üstünde kuş sürüsü
        xa, xb = ctx.xa, ctx.xb
        FA.atmo_birds(c, t, 9, 1.0, xa, xb, 200, 380, speed=22.0, night=ctx.night, seed=3, size=0.8)
        # bacalardan duman
        rs = _RS(31)
        for i in range(10):
            x = self.XD - 1700 + i * 330 + rs.uniform(-60, 60)
            if x < xa - 60 or x > xb + 60:
                continue
            for k in range(5):
                ph = (t * 0.16 + k / 5.0 + i * 0.37) % 1.0
                FA._puff(c, x + math.sin(ph * 6 + i) * 8 * ph, Y_FAR - 56 - ph * 90, 5 + 14 * ph, 0.26 * (1 - ph), "#C8C0B4" if not ctx.night else "#6A7A9A")

    def dyn_bank(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        # Ponte Vecchio üstünde küçük yürüyenler + dükkân ışıkları titremesi
        XB = self.XB
        if xb > XB - 500 and xa < XB + 500:
            for i in range(9):
                dirn = 1 if i % 3 else -1
                sp = 22.0 + 9 * (i % 4)
                x = XB - 330 + ((i * 97 + t * sp * dirn + 5000) % 660)
                if abs(x - XB) < 40:
                    continue
                FA.walker(ctx.f, ["halk", "tuccar", "soylu", "halk", "cocuk"][i % 5], x, Y_WATER - 66 * 1.55 - 6 + 0, 52, t, speed=sp, dir=dirn, phase=i * 0.17, seed=i + 40)
        # nehirde yansıma parıltıları sürer (river katmanı); uzak kıyı bacaları
        rs = _RS(52)
        for i in range(16):
            x = 80 + i * 410 + rs.uniform(-60, 60)
            if x < xa - 60 or x > xb + 60:
                continue
            for k in range(4):
                ph = (t * 0.2 + k / 4.0 + i * 0.29) % 1.0
                FA._puff(c, x + math.sin(ph * 5 + i) * 6 * ph, Y_WATER - 150 - ph * 70, 4 + 10 * ph, 0.22 * (1 - ph), "#C8C0B4" if not ctx.night else "#6A7A9A")

    def dyn_river(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        night = ctx.night
        # parıltılar
        col = "#FFF4D0" if night else "#FFFFFF"
        rs = _RS(14)
        n = 46
        for i in range(n):
            yy = Y_WATER + 14 + rs.uniform(0, 106)
            k = (yy - Y_WATER) / 120.0
            L = 16 + 44 * k
            span = (xb - xa) + 200
            xx = xa - 100 + (rs.uniform(0, span) + t * (6 + 14 * k)) % span
            al = (0.22 + 0.22 * math.sin(t * 1.7 + i * 1.3) ** 2) * (0.55 if night else 1.0)
            c.drawLine(xx, yy, xx + L, yy, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4 + 1.3 * k, Color=C(col, int(255 * al)), StrokeCap=skia.Paint.kRound_Cap))
        # tekneler
        for b in self.boats:
            L = self.layers["river"]
            x = b["x0"] + b["v"] * t
            if x < xa - 260 or x > xb + 260:
                continue
            draw_boat(ctx, x, 722 + b["seed"] * 5, t, b)

    def dyn_main(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        night = ctx.night
        # asılı boyalı kumaşlar
        for ri, rk in enumerate(self.racks):
            n, dx = rk["n"], rk["dx"]
            xs0 = rk["x0"]
            if xs0 + n * dx < xa - 120 or xs0 > xb + 120:
                continue
            for i in range(n):
                for j in range(2):
                    sd = ri * 31 + i * 5 + j
                    col, col2 = DYE_COLS[sd % len(DYE_COLS)]
                    w_ = 70 + (sd * 13) % 36
                    h_ = 190 + (sd * 29) % 110
                    x = xs0 + i * dx + 16 + j * (dx * 0.46)
                    if x < xa - 120 or x > xb + 60:
                        continue
                    draw_cloth(c, x, YG - 333, col, col2, w_, h_, t, ph=sd * 1.3, wind=1.0, seed=sd)
        # tezgâhlar: satıcı + önde tezgâh
        for s_ in self.stalls:
            x, w = s_["x"], s_["w"]
            if x + w < xa - 120 or x > xb + 120:
                continue
            stall_front(ctx, s_)
        # çevre yürüyenleri (y sırası)
        vis = [wk for wk in self.walkers if xa - 220 < wk["x0"] + wk["dir"] * wk["w"] * t < xb + 220]
        vis.sort(key=lambda wk: wk["y"])
        for wk in vis:
            x = wk["x0"] + wk["dir"] * wk["w"] * t
            FA.walker(f, wk["kind"], x, wk["y"], wk["h"], t, speed=wk["w"], dir=wk["dir"], phase=wk["phase"], seed=wk["seed"], prop=wk["prop"])
        # istasyonlar
        for st in ctx.stations:
            fn = st.get("fn")
            if fn is None:
                continue
            x = st.get("x", 0)
            if x < xa - 700 or x > xb + 700:
                continue
            ctx.st = st
            fn(ctx, st)
        # lamba alevleri (gece)
        if night:
            for lx in self.lamps:
                if lx < xa - 60 or lx > xb + 60:
                    continue
                fl = 0.85 + 0.15 * math.sin(t * 9.0 + lx * 0.01) + 0.08 * math.sin(t * 23 + lx)
                for (r, a_) in ((90, 40), (46, 80), (20, 190)):
                    c.drawCircle(lx, YG - 316, r * fl, skia.Paint(AntiAlias=True, Color=C("#FFB04A" if r > 20 else "#FFF0B0", int(a_)), BlendMode=skia.BlendMode.kPlus, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r * 0.45) if r > 20 else None))

    def dyn_front(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        # ön planda hızla geçen büyük kumaşlar (paralaks 1,38)
        rs = _RS(77)
        for i in range(24):
            x = 700 + i * 760 + rs.uniform(-120, 120)
            if x < xa - 260 or x > xb + 100 or (i % 2):
                continue
            col, col2 = DYE_COLS[(i * 3) % len(DYE_COLS)]
            draw_pole(c, x - 20, 960, 40, 12)
            LINE(c, x - 20, 52, x + 190, 52, "#4A3220", 3.0, 255)
            draw_cloth(c, x, 52, col, col2, 150, 380 + (i * 37) % 120, t, ph=i * 0.9, wind=1.2, seed=100 + i)
        FA.atmo_birds(c, t, 4, 1.0, xa, xb, 90, 220, speed=40.0, night=ctx.night, seed=9, size=1.5)


# ═════════════════════════════ tezgâh, tekne ═════════════════════════════
def stall_front(ctx, s_):
    """Tezgâh: satıcı (konuşan/jest) + önde tezgâh paneli + mallar."""
    f, c, t = ctx.f, ctx.c, ctx.t
    T = ctx.world.T
    x, w = s_["x"], s_["w"]
    yg = YG - 14
    rs = _RS(s_["seed"] + 9)
    kind_m = ["tuccar", "halk", "banker", "halk", "tuccar", "soylu_f"][s_["seed"] % 6]
    FA.actor(f, kind_m, x + w * 0.45, yg, 236, t, action="talk", dir=1 if s_["seed"] % 2 == 0 else -1, seed=s_["seed"] + 5, phase=s_["seed"] * 0.23, energy=1.0)
    # tezgâh paneli
    cy0 = yg - 100
    R(c, x - 8, cy0, x + w + 8, cy0 + 16, T("#9A6A3A", 0.0))
    INKR(c, x - 8, cy0, x + w + 8, cy0 + 16, 1.3, 180)
    R(c, x, cy0 + 16, x + w, yg + 6, T("#7A5230", 0.0))
    for i in range(1, 5):
        c.drawLine(x + i * w / 5, cy0 + 16, x + i * w / 5, yg + 6, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C(INK, 120)))
    INKR(c, x, cy0 + 16, x + w, yg + 6, 1.3, 170)
    # mallar
    kind = s_["kind"]
    if kind == "cloth":
        for i in range(5):
            col, col2 = DYE_COLS[(s_["seed"] * 2 + i) % len(DYE_COLS)]
            bx = x + 18 + i * (w - 36) / 4.0
            OVAL(c, bx, cy0 - 10, 14, 16, col)
            c.drawOval(skia.Rect.MakeLTRB(bx - 14, cy0 - 26, bx + 14, cy0 + 6), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.1, Color=C(INK, 160)))
            OVAL(c, bx, cy0 - 12, 5, 7, col2, 200)
    elif kind == "fruit":
        for i in range(3):
            bx = x + 38 + i * (w - 76) / 2.0
            R(c, bx - 30, cy0 - 20, bx + 30, cy0, T("#8A6A3A", 0.0))
            INKR(c, bx - 30, cy0 - 20, bx + 30, cy0, 1.1, 160)
            for k in range(7):
                ang = k / 7.0 * 6.283
                OVAL(c, bx + math.cos(ang) * 16 * (0.4 + (k % 3) * 0.3), cy0 - 22 - math.sin(ang) * 6 - (k % 2) * 5, 8, 8, ["#D8483A", "#E08A2E", "#E8B93A", "#4C7A3C"][(k + i) % 4])
    elif kind == "pots":
        for i in range(6):
            bx = x + 22 + i * (w - 44) / 5.0
            hh = 28 + (i * 7) % 22
            p = sk.smooth_path([(bx - 12, cy0), (bx - 16, cy0 - hh * 0.5), (bx - 8, cy0 - hh), (bx + 8, cy0 - hh), (bx + 16, cy0 - hh * 0.5), (bx + 12, cy0)], True, 0.5)
            c.drawPath(p, skia.Paint(AntiAlias=True, Color=C(["#B8553A", "#C98A5A", "#8A6A48"][i % 3])))
            INKP(c, p, 1.1, 160)
    else:
        for i in range(6):
            bx = x + 22 + i * (w - 44) / 5.0
            OVAL(c, bx, cy0 - 8, 16, 8, "#D8B070")
            c.drawOval(skia.Rect.MakeLTRB(bx - 16, cy0 - 16, bx + 16, cy0), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.1, Color=C(INK, 160)))


_BOAT = {}


def boat_sprite(kind, tod):
    key = (kind, tod)
    if key not in _BOAT:
        wd, ht = (300, 40) if kind == "barge" else (200, 34)
        fr = sk.Frame(wd + 40, ht + 40)
        fr.clear(skia.ColorTRANSPARENT)
        c = fr.c
        c.translate(20, 20)
        p = skia.Path()
        p.moveTo(0, 0)
        p.lineTo(wd, 0)
        p.lineTo(wd - 22, ht)
        p.lineTo(24, ht)
        p.close()
        c.drawPath(p, skia.Paint(AntiAlias=True, Color=C("#6A4A2C" if tod != "night" else "#3A2A1C")))
        INKP(c, p, 1.5, 200)
        for i in range(1, 4):
            c.drawLine(10 + i * 4, i * ht / 4.0, wd - 10 - i * 4, i * ht / 4.0, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C(INK, 110)))
        R(c, 0, -5, wd, 3, "#8A6A3A" if tod != "night" else "#4A3A22")
        _BOAT[key] = (FA.Spr(fr.surf.makeImageSnapshot(), 20, 20), wd, ht)
    return _BOAT[key]


def draw_boat(ctx, x, y, t, b):
    """Nehirde süzülen tekne: dalgalanma + yalpa, yolcular ve sırıkla iten kayıkçı."""
    f, c = ctx.f, ctx.c
    spr, wd, ht = boat_sprite(b["kind"], ctx.tod)
    bob = math.sin(t * 1.3 + b["seed"]) * 2.4
    rl = math.sin(t * 0.9 + b["seed"] * 2) * 1.0
    c.save()
    c.translate(x, y + bob)
    c.rotate(rl)
    c.drawImage(spr.img, -spr.ox - wd / 2, -spr.oy - 6, LIN)
    dirn = 1 if b["v"] > 0 else -1
    # yolcular
    people = [("halk", -0.28, "talk"), ("tuccar", 0.05, "talk")] if b["kind"] == "barge" else [("denizci", 0.0, "talk")]
    for i, (k, fx, act) in enumerate(people):
        FA.actor(f, k, fx * wd, -8, 118, t, action=act, dir=dirn, seed=b["seed"] * 3 + i, phase=0.3 * i)
    # kayıkçı (sırık)
    pk = "denizci"
    px = (-dirn) * wd * 0.40
    FA.actor(f, pk, px, -8, 122, t, action="idle", dir=dirn, seed=b["seed"] + 7, phase=0.5)
    # sırık
    ph = t * 2.2 + b["seed"]
    tip = (px + dirn * 70, 70)
    top = (px + dirn * (22 + 6 * math.sin(ph)), -104)
    c.drawLine(tip[0], tip[1], top[0], top[1], skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.4, Color=C("#6A4A2C"), StrokeCap=skia.Paint.kRound_Cap))
    c.restore()


# ═════════════════════════════ istasyonlar ═════════════════════════════
def _ts(ctx, st):
    return ctx.t - st.get("_at", 0.0)


def st_banker(ctx, st):
    """Bankacı masası (revak kemeri altında): defter yazan bankacı, karşısında konuşan müşteri, koşan çırak. `at` anında yazma başlar."""
    f, t = ctx.f, ctx.t
    x = st["x"]
    ts = _ts(ctx, st)
    yg = YG - 20
    # masa/oturak kemer iç duvarına yaslı
    FA.actor(f, "banker", x - 10, yg, 232, t, action="write", dir=1, seed=4, phase=0.0, t0=st.get("_at", 0.0) - 0.5)
    # karşıda müşteri
    FA.actor(f, "tuccar", x + 270, yg + 6, 228, t, action="talk", dir=-1, seed=6, phase=0.4, energy=1.3)
    # arkadaki çırak
    FA.walker(f, "cocuk", x + 560 - 55 * (t % 14.0), yg + 20, 200, t, speed=55.0, dir=-1, seed=8, phase=0.1)
    if ctx.night:
        # masa üstü mum: titreyen sıcak ışık havuzu + alev
        c = ctx.c
        fl = 1.0 + 0.07 * math.sin(t * 9.0) + 0.04 * math.sin(t * 13.7 + 1.0)
        cxg, cyg = x + 150, yg - 96
        c.drawRect(skia.Rect.MakeLTRB(cxg - 3, cyg - 22, cxg + 3, cyg), skia.Paint(Color=C("#EFE6CE")))
        c.drawOval(skia.Rect.MakeLTRB(cxg - 3.2 * fl, cyg - 40 * fl, cxg + 3.2 * fl, cyg - 20), skia.Paint(AntiAlias=True, Color=C("#FF9A3A")))
        c.drawOval(skia.Rect.MakeLTRB(cxg - 1.6, cyg - 34 * fl, cxg + 1.6, cyg - 21), skia.Paint(AntiAlias=True, Color=C("#FFE9A0")))
        glow(c, cxg, cyg - 28, 210 * fl, "#FFB454", 0.50)


def st_dyers(ctx, st):
    """Boyahane: kazanı karıştıran boyacılar + yükselen buhar; sırık/ip altında bez taşıyan işçi."""
    f, c, t = ctx.f, ctx.c, ctx.t
    T = ctx.world.T
    x = st["x"]
    yg = YG - 6
    for k, (vx, col) in enumerate(((0, "#1E3A8A"), (250, "#B3361F"))):
        vxx = x + vx
        # kazan
        p = sk.smooth_path([(vxx - 70, yg - 70), (vxx - 76, yg - 18), (vxx - 56, yg + 4), (vxx + 56, yg + 4), (vxx + 76, yg - 18), (vxx + 70, yg - 70)], True, 0.3)
        c.drawPath(p, skia.Paint(AntiAlias=True, Color=C(T("#7A5230", 0.0))))
        INKP(c, p, 1.6, 200)
        for i in (-40, -14, 14, 40):
            LINE(c, vxx + i, yg - 66, vxx + i * 1.05, yg + 2, "#4A3220", 1.4, 150)
        c.drawOval(skia.Rect.MakeLTRB(vxx - 70, yg - 80, vxx + 70, yg - 58), skia.Paint(AntiAlias=True, Color=C(col)))
        c.drawOval(skia.Rect.MakeLTRB(vxx - 70, yg - 80, vxx + 70, yg - 58), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=C(INK, 200)))
        OVAL(c, vxx - 22, yg - 72, 24, 4, "#FFFFFF", 70)
        for q in range(6):
            ph = (t * 0.3 + q / 6.0 + k * 0.4) % 1.0
            FA._puff(c, vxx + math.sin(ph * 5 + q) * 14 * ph - 10, yg - 84 - ph * 150, 8 + 26 * ph, 0.28 * (1 - ph) ** 1.2, "#EDEDED" if not ctx.night else "#9AAAC8")
    FA.actor(f, "halk", x + 112, yg + 4, 240, t, action="talk", dir=1, seed=12, phase=0.1, energy=1.4, prop=None)
    FA.walker(f, "halk", x + 470 - 70 * (t % 14.0), yg + 20, 236, t, speed=70.0, dir=-1, seed=14, prop="sack", phase=0.3)
    FA.walker(f, "denizci", x + 380 - 62 * (t % 18.0), yg + 12, 236, t, speed=62.0, dir=-1, seed=15, prop="basket", phase=0.5)


def st_market(ctx, st):
    """Pazar: pazarlık eden iki müşteri, koşuşan çocuk, yük taşıyan hamal."""
    f, c, t = ctx.f, ctx.c, ctx.t
    x = st["x"]
    yg = YG + 6
    FA.actor(f, "soylu_f", x - 60, yg + 14, 242, t, action="point", dir=1, seed=21, phase=0.2, t0=0.5 + (t // 6) * 6, dur=2.5, target=(1.0, -0.2))
    FA.actor(f, "halk", x + 20, yg + 10, 240, t, action="talk", dir=-1, seed=22, phase=0.7, energy=1.2)
    FA.walker(f, "cocuk", x + 800 - 190 * (t % 6.0), yg + 28, 208, t, speed=190.0, dir=-1, seed=23, run=True, phase=0.4)
    FA.walker(f, "halk", x + 140 + 74 * (t % 20.0), yg + 20, 238, t, speed=74.0, dir=1, seed=24, prop="sack", phase=0.1)


def st_duomo_walk(ctx, st):
    """Duomo'ya yürüyüş: din adamı, tüccar, soylu hanım ve çocuk bir arada ağır ağır yürür (kamera onları geçer)."""
    f, t = ctx.f, ctx.t
    x = st["x"]
    yg = YG + 4
    grp = [("rahip", 0, 250, "book"), ("tuccar", 130, 246, None), ("soylu_f", 250, 244, None), ("cocuk", 330, 215, None), ("banker", 460, 248, None), ("kesis", 600, 252, "staff")]
    for i, (k, dx, h, pr) in enumerate(grp):
        xx = x + dx + 88 * t * 0.0 + 66 * (t % 40.0)
        FA.walker(f, k, xx, yg + (i % 3) * 9, h, t, speed=66.0, dir=1, seed=40 + i, phase=0.13 * i, prop=pr)


WORLDS["florence"] = Florence


# ═════════════════════════════ NEF (katedral içi: tek uzun plan) ═════════════════════════════
Y_FLOOR = 700                   # zemin / arka duvar kesişimi (görüntü y)
Y_VCUT = 208                    # tonoz yayı başlangıcı
BAY = 380


class Nave(World):
    name = "nave"
    PW = 11200
    interior = True

    def build(self):
        PW = self.PW
        span = PW - W

        def Lw(f):
            return int(W + span * f + 500)
        self.layer("wall", 0.35, Lw(0.35), self._draw_wall, wear=3)
        self.layer("main", 1.0, PW, self._draw_floor, wear=2)
        self.layer("fg", 1.38, Lw(1.38), self._draw_fg)
        rr = _RS(5)
        self.candles = [int(x) for x in np.arange(700, PW, 780) + rr.randint(-80, 80, len(np.arange(700, PW, 780)))]
        self.kneel1 = (1400, 3500)
        self.stand1 = (3900, 6000)
        self.kneel2 = (6200, 8200)

    def default_cams(self):
        return [(0.0, (960, 0, 1.0)), (0.30, (2900, 0, 1.0)), (0.55, (5000, 18, 1.10)), (0.80, (7500, 0, 1.0)), (1.0, (9400, 0, 1.0))]

    def default_stations(self):
        return [dict(x=2300, fn=st_celebrant, at_frac=0.0), dict(x=4700, fn=st_bell, at_frac=0.42), dict(x=8100, fn=st_flee, at_frac=0.74)]

    def stack(self, ctx):
        return [("L", "wall"), ("D", "dyn_wall", 0.35), ("L", "main"), ("D", "dyn_main", 1.0), ("L", "fg"), ("D", "dyn_fg", 1.38)]

    def interior_finish(self, ctx):
        by0, bh = ctx.band
        a = 0.18 if ctx.tod != "night" else 0.30
        tint_overlay(ctx.c, by0, bh, [("#1A1008", int(255 * a * 1.3)), ("#3A2410", 0), ("#5A3A1C", int(255 * a * 0.6))], [0, 0.45, 1])

    # ── katman boyaları ─────────────────────────────────────────────────────
    def _draw_wall(self, fr, xa, xb):
        c = fr.c
        T = self.T
        night = self.tod == "night"
        wall_c = T("#D3C7A6", 0.25)
        stone = T("#8F928A", 0.2)
        # arka duvar zemin
        GRAD_V(c, xa, OV - 30, xb, Y_FLOOR + 40, [(T("#BDB295", 0.3), 0.0), (wall_c, 0.45), (T("#C9BC9A", 0.2), 1.0)])
        i0 = int(math.floor(xa / BAY)) - 1
        i1 = int(math.ceil(xb / BAY)) + 1
        for i in range(i0, i1 + 1):
            x0 = i * BAY
            xc = x0 + BAY / 2
            # tonoz: sivri kemer + dolgu (ribs)
            ap = skia.Path()
            ap.moveTo(x0, Y_VCUT)
            ap.cubicTo(x0 + 16, Y_VCUT - 90, x0 + BAY * 0.30, OV - 40, xc, OV - 70)
            ap.cubicTo(x0 + BAY * 0.70, OV - 40, x0 + BAY - 16, Y_VCUT - 90, x0 + BAY, Y_VCUT)
            ap.lineTo(x0 + BAY, OV - 90)
            ap.lineTo(x0, OV - 90)
            ap.close()
            c.drawPath(ap, skia.Paint(AntiAlias=True, Color=C(T("#9A9684", 0.2))))
            rib = skia.Path()
            rib.moveTo(x0, Y_VCUT)
            rib.cubicTo(x0 + 16, Y_VCUT - 90, x0 + BAY * 0.30, OV - 40, xc, OV - 70)
            rib.cubicTo(x0 + BAY * 0.70, OV - 40, x0 + BAY - 16, Y_VCUT - 90, x0 + BAY, Y_VCUT)
            c.drawPath(rib, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=11, Color=C(stone)))
            INKP(c, rib, 1.2, 150)
            # çapraz nervür
            for sgn in (-1, 1):
                p = skia.Path()
                p.moveTo(x0 if sgn > 0 else x0 + BAY, Y_VCUT)
                p.quadTo(xc - sgn * BAY * 0.12, OV - 20, xc, OV - 62)
                c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=C(mix(stone, "#FFFFFF", 0.12), 200)))
            # klerestori penceresi (yüksek, sivri) + vitray
            wx, wy0, wy1, ww = xc, 232, 380, 76
            wp = skia.Path()
            wp.moveTo(wx - ww / 2, wy1)
            wp.lineTo(wx - ww / 2, wy0 + 34)
            wp.quadTo(wx - ww / 2, wy0, wx, wy0 - 16)
            wp.quadTo(wx + ww / 2, wy0, wx + ww / 2, wy0 + 34)
            wp.lineTo(wx + ww / 2, wy1)
            wp.close()
            glow = "#FFF1C0" if not night else "#2A3A6E"
            c.drawPath(wp, skia.Paint(AntiAlias=True, Color=C(glow)))
            c.save()
            c.clipPath(wp, skia.ClipOp.kIntersect, True)
            rs = _RS(i * 17 + 3)
            for k in range(6):
                gy = wy0 - 10 + k * 26
                for q in range(2):
                    col = ["#2F5FB8", "#B3361F", "#E2A83A", "#3E7A5A", "#6E3A7A"][rs.randint(5)]
                    if rs.rand() < 0.55:
                        c.drawRect(skia.Rect.MakeLTRB(wx - ww / 2 + q * ww / 2 + 2, gy, wx - ww / 2 + (q + 1) * ww / 2 - 2, gy + 22), skia.Paint(Color=C(col, 150 if not night else 110)))
            c.restore()
            LINE(c, wx, wy0 - 16, wx, wy1, "#4A3A28", 2.0, 220)
            for gy in (wy0 + 38, wy0 + 78, wy0 + 116):
                LINE(c, wx - ww / 2, gy, wx + ww / 2, gy, "#4A3A28", 1.6, 200)
            INKP(c, wp, 2.6, 220, "#6A6A60")
            # alt sıra: kör kemer (yan nef girişi: koyu)
            ao = draw_arch_opening(c, xc, Y_FLOOR, 292, 250, T, "#2C221A", ink=True)
            c.drawPath(ao, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=9, Color=C(stone)))
            # kemerin içinde ikinci sıra sütun silueti + kandil
            for kx in (xc - 90, xc + 90):
                R(c, kx - 9, Y_FLOOR - 190, kx + 9, Y_FLOOR, "#3C3026", 230)
            if night or i % 2 == 0:
                OVAL(c, xc, Y_FLOOR - 120, 4, 6, "#FFC561", 230)
                c.drawCircle(xc, Y_FLOOR - 120, 38, skia.Paint(AntiAlias=True, Color=C("#FFB04A", 45), BlendMode=skia.BlendMode.kPlus))
            # kornişler
            R(c, x0, 392, x0 + BAY, 406, T("#A8A89C", 0.2))
            c.drawLine(x0, 392, x0 + BAY, 392, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 150)))
            c.drawLine(x0, 406, x0 + BAY, 406, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 120)))
            # pilaster (gövde + başlık) — yarım sütun, tonoza kadar uzanır
            px = x0
            R(c, px - 26, Y_VCUT, px + 26, Y_FLOOR, stone)
            sh = skia.GradientShader.MakeLinear([(px - 26, 0), (px + 26, 0)], [C("#FFFFFF", 55), C("#FFFFFF", 0), C("#1A1008", 60)], [0, 0.4, 1.0])
            c.drawRect(skia.Rect.MakeLTRB(px - 26, Y_VCUT, px + 26, Y_FLOOR), skia.Paint(Shader=sh))
            INKR(c, px - 26, Y_VCUT, px + 26, Y_FLOOR, 1.2, 150)
            for cy_ in (Y_VCUT + 6, 392):
                R(c, px - 33, cy_ - 8, px + 33, cy_ + 8, T("#A3A396", 0.15))
                INKR(c, px - 33, cy_ - 8, px + 33, cy_ + 8, 1.1, 140)
            # zemin silme
            R(c, px - 34, Y_FLOOR - 16, px + 34, Y_FLOOR, T("#7E8078", 0.15))
        # sıva çizgileri (taş sıraları)
        for yy in range(430, Y_FLOOR, 46):
            pass

    def _draw_floor(self, fr, xa, xb):
        c = fr.c
        T = self.T
        # zemin: perspektifli elmas/dama
        y = Y_FLOOR
        k = 0
        rowh = 13.0
        GRAD_V(c, xa, Y_FLOOR - 4, xb, 960, [(T("#7A6A4C", 0.0), 0.0), (T("#B9A47A", 0.0), 1.0)])
        while y < 960:
            wk = 46 + k * 15
            off = (k % 2) * wk / 2
            x = xa - (xa % wk) - wk + off
            while x < xb + wk:
                if (int(round((x - off) / wk)) + k) % 2 == 0:
                    R(c, x, y, x + wk, y + rowh, T("#9A4A32", 0.0), 90)
                x += wk
            c.drawLine(xa, y, xb, y, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#3A2A18", 70)))
            y += rowh
            rowh *= 1.14
            k += 1
        # kayıt: duvar dibine gölge
        sh = skia.GradientShader.MakeLinear([(0, Y_FLOOR - 2), (0, Y_FLOOR + 40)], [C("#1A1008", 90), C("#1A1008", 0)], [0, 1])
        c.drawRect(skia.Rect.MakeLTRB(xa, Y_FLOOR - 2, xb, Y_FLOOR + 40), skia.Paint(Shader=sh))
        # kandillik (şamdan) gövdeleri
        for cxp in self.candles:
            if cxp < xa - 40 or cxp > xb + 40:
                continue
            draw_candelabra(c, cxp, 805, T)
        # mezar taşı levhaları
        rr = _RS(int(xa) // 1024 + 9)
        for i in range(2):
            x = xa + rr.uniform(40, 980)
            yy = rr.uniform(838, 880)
            p = sk.poly_path([(x, yy), (x + 150, yy), (x + 176, yy + 22), (x - 26, yy + 22)])
            c.drawPath(p, skia.Paint(AntiAlias=True, Color=C(T("#8A8878", 0.0), 150)))
            INKP(c, p, 1.0, 110)

    def _draw_fg(self, fr, xa, xb):
        c = fr.c
        T = self.T
        # ön plan sütunları (karanlık, paralaks 1,38): gövde 120 px, başlık + ayak
        step = 1180
        i0 = int(math.floor(xa / step)) - 1
        for i in range(i0, i0 + int((xb - xa) / step) + 3):
            x = i * step + 540
            if x < xa - 200 or x > xb + 200:
                continue
            w = 118
            col = T("#5C5C56", 0.0)
            R(c, x - w / 2, OV - 40, x + w / 2, 960, col)
            sh = skia.GradientShader.MakeLinear([(x - w / 2, 0), (x + w / 2, 0)], [C("#FFFFFF", 48), C("#FFFFFF", 0), C("#000000", 90)], [0, 0.33, 1.0])
            c.drawRect(skia.Rect.MakeLTRB(x - w / 2, OV - 40, x + w / 2, 960), skia.Paint(Shader=sh))
            INKR(c, x - w / 2, OV - 40, x + w / 2, 960, 1.5, 190)
            for yy in (150, 176, 196):
                R(c, x - w * 0.7, yy, x + w * 0.7, yy + (18 if yy == 150 else 12), T("#6A6A62", 0.0))
                INKR(c, x - w * 0.7, yy, x + w * 0.7, yy + (18 if yy == 150 else 12), 1.2, 180)
            R(c, x - w * 0.72, 830, x + w * 0.72, 960, T("#4A4A44", 0.0))
            INKR(c, x - w * 0.72, 830, x + w * 0.72, 960, 1.4, 190)
            # kıvrık çizgi: sütun oluğu
            for k in range(-2, 3):
                c.drawLine(x + k * 20, 220, x + k * 20, 822, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#000000", 36)))

    # ── dinamik ─────────────────────────────────────────────────────────────
    def dyn_wall(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        night = ctx.night
        i0 = int(math.floor(xa / BAY)) - 1
        i1 = int(math.ceil(xb / BAY)) + 1
        for i in range(i0, i1 + 1):
            xc = i * BAY + BAY / 2
            fl = 0.85 + 0.15 * math.sin(t * 0.35 + i * 1.7)
            if night:
                fl *= 0.45
            base_a = 0.20 * fl
            top_l, top_r = xc - 38, xc + 38
            dx = -230
            y0, y1 = 372, Y_FLOOR + 90
            sh = skia.GradientShader.MakeLinear([(0, y0), (0, y1)], [C("#FFE9A8", int(255 * base_a * 1.6)), C("#FFE9A8", int(255 * base_a * 0.5)), C("#FFE9A8", int(255 * base_a * 0.15))], [0, 0.6, 1])
            p = sk.poly_path([(top_l, y0), (top_r, y0), (top_r + dx + 20, y1), (top_l + dx - 20, y1)])
            c.drawPath(p, skia.Paint(AntiAlias=True, Shader=sh, BlendMode=skia.BlendMode.kPlus))
            # zeminde ışık lekesi (yumuşak sprite)
            for (rx_, ry_, aa_) in ((130, 24, 0.5), (86, 16, 0.5)):
                c.drawOval(skia.Rect.MakeLTRB(xc + dx - 30 - rx_, Y_FLOOR + 66 - ry_, xc + dx - 30 + rx_, Y_FLOOR + 66 + ry_), skia.Paint(Color=C("#FFE9A8", int(255 * base_a * aa_ * 0.6)), BlendMode=skia.BlendMode.kPlus))
            # huzmedeki toz zerreleri
            rs = _RS(i * 5 + 1)
            for k in range(9):
                u = (rs.rand() + t * (0.012 + 0.01 * rs.rand())) % 1.0
                yy = y0 + (y1 - y0) * u
                xx = lerp_(top_l + 6, top_l + dx, u) + (rs.rand() * 70) * (1 - 0.25 * u) + math.sin(t * 0.8 + k + i) * 6
                r = 1.4 + 1.8 * rs.rand()
                c.drawCircle(xx, yy, r, skia.Paint(AntiAlias=True, Color=C("#FFF3D0", int(200 * fl * (0.4 + 0.6 * abs(math.sin(t * 1.3 + k * 2.1))))), BlendMode=skia.BlendMode.kPlus))
        # asılı kandiller (tonozdan zincirle)
        for i in range(i0, i1 + 1):
            if i % 2:
                continue
            xc = i * BAY + BAY / 2 + 190
            ang = 3.0 * math.sin(t * 0.9 + i * 0.7) * math.pi / 180
            draw_hang_lamp(c, xc, OV - 20, 180, ang, t, night)

    def dyn_main(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        night = ctx.night
        # şamdan alevleri
        for cxp in self.candles:
            if cxp < xa - 40 or cxp > xb + 40:
                continue
            for k in range(5):
                fx = cxp + (k - 2) * 15
                fl = 0.8 + 0.2 * math.sin(t * 11 + cxp * 0.03 + k * 1.9) + 0.1 * math.sin(t * 27 + k)
                OVAL(c, fx, 805 - 168 - 6 * fl, 4.0, 8.5 * fl, "#FFC561", 240)
                OVAL(c, fx, 805 - 166, 2.0, 5.0 * fl, "#FFF4C0", 255)
                c.drawCircle(fx, 805 - 170, 30 * fl, skia.Paint(AntiAlias=True, Color=C("#FFB04A", 48 if not night else 80), BlendMode=skia.BlendMode.kPlus))
        # kalabalıklar (diz çökmüş / ayakta)
        FA.crowd(f, t, (self.kneel1[0], 770, self.kneel1[1], 858), 30, seed=11, wave=0.5, mode="kneel", h=(214, 252), view=(xa, xb), cull=200)
        FA.crowd(f, t, (self.stand1[0], 770, self.stand1[1], 858), 26, seed=12, wave=0.6, mode="mill", h=(214, 252), view=(xa, xb), cull=200)
        at2 = None
        for st in ctx.stations:
            if st.get("fn") is st_bell:
                at2 = st["_at"]
        FA.crowd(f, t, (self.kneel2[0], 770, self.kneel2[1], 858), 28, seed=13, wave=0.5, mode="kneel", h=(214, 252), view=(xa, xb), cull=200, rise_at=(at2 + 0.4) if at2 is not None else None)
        for st in ctx.stations:
            fn = st.get("fn")
            if fn is None:
                continue
            x = st.get("x", 0)
            if x < xa - 800 or x > xb + 800:
                continue
            ctx.st = st
            fn(ctx, st)

    def dyn_fg(self, ctx):
        c, t = ctx.c, ctx.t
        # ön plandan geçen toz/ışık parçacıkları
        xa, xb = ctx.xa, ctx.xb
        rs = _RS(44)
        for k in range(26):
            x = xa + ((rs.rand() * (xb - xa) + t * 18 * (0.5 + rs.rand())) % (xb - xa))
            y = 100 + rs.rand() * 760 + math.sin(t * 0.6 + k) * 14
            c.drawCircle(x, y, 1.6 + 2.6 * rs.rand(), skia.Paint(AntiAlias=True, Color=C("#FFEFC4", int(70 + 90 * rs.rand())), BlendMode=skia.BlendMode.kPlus))


def lerp_(a, b, t):
    return a + (b - a) * t


def draw_candelabra(c, x, yb, T):
    """Demir şamdan: ayak + gövde + kol + 5 mum (alev dinamik)."""
    col = T("#2A2018", 0.0)
    R(c, x - 3, yb - 168, x + 3, yb, col)
    c.drawOval(skia.Rect.MakeLTRB(x - 26, yb - 12, x + 26, yb + 6), skia.Paint(AntiAlias=True, Color=C(col)))
    p = skia.Path()
    p.moveTo(x - 36, yb - 150)
    p.quadTo(x - 36, yb - 130, x, yb - 128)
    p.quadTo(x + 36, yb - 130, x + 36, yb - 150)
    c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.2, Color=C(col)))
    for k in range(5):
        fx = x + (k - 2) * 15
        yy = yb - 150 + (abs(k - 2) * 0.0)
        R(c, fx - 2.4, yy - 20, fx + 2.4, yy, "#F1E8CF")
        INKR(c, fx - 2.4, yy - 20, fx + 2.4, yy, 0.9, 150)


def draw_hang_lamp(c, x, ytop, L, ang, t, night):
    """Tonozdan zincirle sarkan kandil: sarkaç."""
    px, py = x + L * math.sin(ang), ytop + L * math.cos(ang)
    LINE(c, x, ytop, px, py, "#3A2A18", 1.8, 230)
    for k in range(1, 6):
        u = k / 6.0
        OVAL(c, x + (px - x) * u, ytop + (py - ytop) * u, 2.4, 3.4, "#5A4A30", 220)
    c.save()
    c.translate(px, py)
    c.rotate(math.degrees(ang) * 0.3)
    p = sk.smooth_path([(-13, 0), (-17, 18), (-9, 28), (9, 28), (17, 18), (13, 0)], True, 0.5)
    c.drawPath(p, skia.Paint(AntiAlias=True, Color=C("#8A6A30")))
    INKP(c, p, 1.2, 190)
    fl = 0.85 + 0.15 * math.sin(t * 8 + x * 0.02)
    c.drawOval(skia.Rect.MakeLTRB(-5, 4, 5, 22 * fl), skia.Paint(AntiAlias=True, Color=C("#FFD27A", 240)))
    c.drawCircle(0, 16, 54 * fl, skia.Paint(AntiAlias=True, Color=C("#FFB04A", 52 if not night else 90), BlendMode=skia.BlendMode.kPlus))
    c.restore()


def st_bell(ctx, st):
    """Çan sarkacı: büyük bronz çan zincirle sallanır; her vuruşta görsel ses halkaları (dalga) yayılır; `at` anında çalmaya başlar (öncesinde yavaş sallanır)."""
    c, t = ctx.c, ctx.t
    T = ctx.world.T
    ts = _ts(ctx, st)
    x = st["x"]
    top = OV + 10
    L = 400
    ring = clamp(ts / 0.8)
    amp = (4.0 + 22.0 * smooth(ring)) * math.exp(-max(0.0, ts - 7.0) * 0.1)
    ph = t * 2.0 * math.pi / 3.3
    ang = math.radians(amp) * math.sin(ph)
    px, py = x + L * math.sin(ang), top + L * math.cos(ang)
    # taşıyıcı kiriş
    R(c, x - 80, top - 16, x + 80, top + 4, "#4A3220")
    INKR(c, x - 80, top - 16, x + 80, top + 4, 1.4, 190)
    LINE(c, x, top, px, py - 36, "#3A2A18", 3.2, 240)
    # çan
    c.save()
    c.translate(px, py)
    c.rotate(math.degrees(ang) * 0.85)
    p = skia.Path()
    p.moveTo(-18, -44)
    p.cubicTo(-30, -30, -40, 10, -62, 56)
    p.lineTo(62, 56)
    p.cubicTo(40, 10, 30, -30, 18, -44)
    p.close()
    sh = skia.GradientShader.MakeLinear([(-60, 0), (60, 0)], [C("#E8C478"), C("#C4893A"), C("#7A4E1C")], [0, 0.5, 1])
    c.drawPath(p, skia.Paint(AntiAlias=True, Shader=sh))
    INKP(c, p, 1.8, 210)
    c.drawLine(-48, 36, 48, 36, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.0, Color=C("#5A3A12", 190)))
    c.drawLine(-38, 18, 38, 18, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0, Color=C("#5A3A12", 150)))
    OVAL(c, -4 + 18 * math.sin(ph + 1.0) * 0.6, 60, 9, 9, "#4A2A10")
    c.restore()
    # ses halkaları: sarkaç uç noktalarında
    if ts > 0:
        period = 3.3
        k0 = math.floor(ts / (period / 2))
        for k in (k0, k0 - 1, k0 - 2):
            if k < 0:
                continue
            te = k * period / 2
            age = ts - te
            if 0 <= age < 1.5:
                r = 70 + 330 * age ** 0.8
                for j in range(3):
                    rr = r - j * 34
                    if rr > 20:
                        c.drawCircle(px * 0 + x + L * math.sin(math.radians(amp) * (1 if k % 2 == 0 else -1)), py * 0 + top + L, rr, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.2, Color=C("#FFF1C8", int(70 * (1 - age / 1.5) * (1 - j * 0.3))), BlendMode=skia.BlendMode.kPlus))
    # çan çalan çocuk (ipi çeker): zemin
    FA.actor(ctx.f, "cocuk", x + 130, 840, 210, t, action="idle", dir=-1, seed=77, phase=0.2)


def st_celebrant(ctx, st):
    """Ayin alayı: haçlı rahip, buhurdanlı yardımcı çocuk, mum taşıyıcılar; buhurdan sarkaç gibi sallanır, dumanı iz bırakır."""
    f, c, t = ctx.f, ctx.c, ctx.t
    x = st["x"]
    yg = 836
    base = x + 52 * (t % 60.0)
    FA.walker(f, "rahip", base + 260, yg, 252, t, speed=52.0, dir=1, seed=51, prop="cross", phase=0.0)
    FA.walker(f, "kardinal", base + 130, yg + 6, 250, t, speed=52.0, dir=1, seed=52, prop="book", phase=0.35)

    def thurible(c_, p, kit):
        hb = kit.B["hb"]
        s_, e_, w_ = p.arms[1]
        ang = math.sin(t * 3.3) * 0.62
        L = 0.24 * hb
        ex, ey = w_[0] + L * math.sin(ang), w_[1] + L * math.cos(ang)
        LINE(c_, w_[0], w_[1], ex, ey, "#6A5A38", max(1.0, hb * 0.006), 255)
        c_.drawOval(skia.Rect.MakeLTRB(ex - 0.028 * hb, ey - 0.02 * hb, ex + 0.028 * hb, ey + 0.036 * hb), skia.Paint(AntiAlias=True, Color=C("#B8903A")))
        c_.drawOval(skia.Rect.MakeLTRB(ex - 0.028 * hb, ey - 0.02 * hb, ex + 0.028 * hb, ey + 0.036 * hb), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C(INK, 190)))
        for q in range(7):
            ph = (t * 0.55 + q / 7.0) % 1.0
            FA._puff(c_, ex - ph * 0.30 * hb + math.sin(ph * 6 + q) * 0.012 * hb, ey - ph * 0.30 * hb, (0.02 + 0.07 * ph) * hb, 0.30 * (1 - ph) ** 1.2, "#D8D4CC")
    FA.walker(f, "cocuk", base, yg + 12, 214, t, speed=52.0, dir=1, seed=53, phase=0.1, prop=None, extra=thurible)
    FA.walker(f, "halk", base - 120, yg + 16, 226, t, speed=52.0, dir=1, seed=54, phase=0.6, prop="torch")


def st_flee(ctx, st):
    """Kaçan figürler: çan/hançer işaretinden sonra diz çökmüş/ayaktaki kalabalık kalkar, sağdan sola (tehdit yönü) koşar; sendeleyen, bir çocuğu çeken biri."""
    f, c, t = ctx.f, ctx.c, ctx.t
    ts = _ts(ctx, st)
    x = st["x"]
    mem = FA.crowd_members(77, 12, (x - 360, 776, x + 360, 858), (222, 250))
    for m in mem:
        dly = 0.25 * (m["i"] % 7) + 0.1 * m["r"]
        kit, bh = FA.kit_for(m["kind"], m["seed"], m["h"])
        s_ = m["h"] / bh
        T = t + m["r2"] * 3.0
        if ts < dly + 0.9:
            p = FA.act_kneel(kit, T, m["phase"], t0=-3.0, dur=0.1, rise_at=st["_at"] + dly)
            xs = m["x"]
            FA.cloth_for(kit, p, T, m["phase"] * 6.28, lag=0.0, wave=0.0)
            FA._draw_pose(f, kit, bh, p, xs, m["y"], m["h"], -1, 1.0, None)
        else:
            v = 230 + 70 * m["r"]
            xs = m["x"] - v * (ts - dly - 0.9)
            if xs < ctx.xa - 300:
                continue
            p = FA.gait(kit, T, v / s_, m["phase"], run=True, stride=kit.d.get("stride", 1.0))
            FA.cloth_for(kit, p, T, m["phase"] * 6.28, lag=min(v / s_ * 0.06, 0.22 * bh) * 1.5, wave=0.0)
            FA._draw_pose(f, kit, bh, p, xs, m["y"], m["h"], -1, 1.0, None)
            # toz
            FA._puff(c, xs + 40, m["y"] - 6, 14 + 6 * ((ts * 3 + m["i"]) % 1.0), 0.20, "#BDAF92")


WORLDS["nave"] = Nave


# ═════════════════════════════ VASARI KORİDORU (Arno üstünde pencereli koridor) ═════════════════════════════
Y_WIN0, Y_WIN1 = 190, 580         # pencere üst/alt (görüntü y)
WIN_STEP = 560
Y_CFLOOR = 800


def draw_portrait(c, x, y, w, h, seed, T):
    """Koridor duvarında altın çerçeveli portre (basit büst: zemin + omuz + baş + şapka)."""
    rs = _RS(seed)
    R(c, x - 7, y - 7, x + w + 7, y + h + 7, T("#B8893A", 0.0))
    INKR(c, x - 7, y - 7, x + w + 7, y + h + 7, 1.4, 190)
    R(c, x - 2, y - 2, x + w + 2, y + h + 2, T("#7A5A22", 0.0))
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(x, y, x + w, y + h))
    bg = ["#3A4A3A", "#2A3248", "#4A3A2C", "#5A3A32", "#2E3A44"][rs.randint(5)]
    R(c, x, y, x + w, y + h, T(bg, 0.0))
    robe = ["#8E2A20", "#233C8C", "#1E1A18", "#6A3A7A", "#2E6A4F"][rs.randint(5)]
    skin = ["#E7C4A0", "#DDB48C", "#D3A57C"][rs.randint(3)]
    cx_ = x + w * 0.5
    # omuzlar (geniş yarım elips) + yaka + boyun + baş (profile yakın 3/4)
    sp_ = sk.smooth_path([(cx_ - w * 0.50, y + h + 4), (cx_ - w * 0.46, y + h * 0.80), (cx_ - w * 0.26, y + h * 0.66), (cx_ + w * 0.26, y + h * 0.66), (cx_ + w * 0.46, y + h * 0.80), (cx_ + w * 0.50, y + h + 4)], True, 0.5)
    c.drawPath(sp_, skia.Paint(AntiAlias=True, Color=C(T(robe, 0.0))))
    INKP(c, sp_, 1.0, 130)
    R(c, cx_ - w * 0.06, y + h * 0.54, cx_ + w * 0.06, y + h * 0.68, T(skin, 0.0))
    OVAL(c, cx_ + w * 0.02, y + h * 0.40, w * 0.15, h * 0.15, T(skin, 0.0))
    c.drawOval(skia.Rect.MakeLTRB(cx_ + w * 0.02 - w * 0.15, y + h * 0.40 - h * 0.15, cx_ + w * 0.02 + w * 0.15, y + h * 0.40 + h * 0.15), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C(INK, 140)))
    OVAL(c, cx_ + w * 0.06, y + h * 0.38, w * 0.02, h * 0.012, "#1E150C", 220)
    if rs.rand() < 0.75:
        hc_ = T(["#1E1A18", "#8E2A20", "#233C8C"][rs.randint(3)], 0.0)
        c.drawOval(skia.Rect.MakeLTRB(cx_ - w * 0.19, y + h * 0.18, cx_ + w * 0.24, y + h * 0.36), skia.Paint(AntiAlias=True, Color=C(hc_)))
        c.drawOval(skia.Rect.MakeLTRB(cx_ - w * 0.19, y + h * 0.18, cx_ + w * 0.24, y + h * 0.36), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C(INK, 140)))
    sh = skia.GradientShader.MakeLinear([(x, y), (x + w, y + h)], [C("#FFFFFF", 30), C("#000000", 0), C("#000000", 60)], [0, 0.5, 1])
    c.drawRect(skia.Rect.MakeLTRB(x, y, x + w, y + h), skia.Paint(Shader=sh))
    c.restore()
    INKR(c, x, y, x + w, y + h, 1.2, 170)


class Corridor(World):
    name = "corridor"
    PW = 11600
    interior = True

    def build(self):
        PW = self.PW
        span = PW - W
        F = Florence.__new__(Florence)
        F.tod, F.T, F.layers = self.tod, self.T, {}
        F.build()
        F.XD, F.XB = 2250, 2913
        self.F = F

        def Lw(f):
            return int(W + span * f + 500)
        self.layer("sky", 0.05, Lw(0.05), F._draw_sky, opaque=True, scale=0.5, yr=(0, 700))
        self.layer("hills", 0.12, Lw(0.12), F._draw_hills, scale=0.5, yr=(330, 800))
        self.layer("city", 0.22, Lw(0.22), F._draw_city, yr=(60, 620))
        self.layer("bank", 0.45, Lw(0.45), F._draw_bank, yr=(300, 812))
        self.layer("wall", 1.0, PW, self._draw_wall, wear=3)
        self.layer("fg", 1.30, Lw(1.30), self._draw_fg)
        rr = _RS(33)
        self.people = []
        x = 700
        kinds = ["soylu", "soylu_f", "banker", "asker", "cocuk", "tuccar", "soylu", "kesis", "rahip", "soylu_f"]
        while x < PW - 500:
            k = kinds[rr.randint(len(kinds))]
            run = (k == "cocuk" and rr.rand() < 0.6)
            self.people.append(dict(x0=x, dir=1 if rr.rand() < 0.62 else -1, w=(150 if run else rr.uniform(48, 92)), run=run, kind=k, seed=int(rr.randint(0, 999)), h=rr.uniform(236, 262) if k != "cocuk" else 220,
                                    y=Y_CFLOOR + 44 + rr.uniform(-6, 14), phase=rr.rand(), idle=(rr.rand() < 0.25), prop=("book" if k in ("banker", "kesis") and rr.rand() < 0.5 else None)))
            x += rr.uniform(420, 820)
        self.DY = 170

    def default_cams(self):
        return [(0.0, (960, 0, 1.0)), (0.25, (3000, 0, 1.0)), (0.55, (6000, 0, 1.0)), (0.80, (8700, 0, 1.0)), (1.0, (10300, 0, 1.0))]

    def default_stations(self):
        return []

    def stack(self, ctx):
        d = self.DY
        return [("L", "sky", d), ("D", "dyn_out_sky", 0.05, d), ("L", "hills", d), ("L", "city", d), ("D", "dyn_out_city", 0.22, d), ("L", "bank", d), ("D", "dyn_out_bank", 0.45, d),
                ("L", "wall"), ("D", "dyn_people", 1.0), ("D", "dyn_light", 1.0), ("L", "fg"), ("D", "dyn_fg", 1.30)]

    def interior_finish(self, ctx):
        by0, bh = ctx.band
        a = 0.16 if ctx.tod != "night" else 0.26
        tint_overlay(ctx.c, by0, bh, [("#1A1008", int(255 * a * 1.2)), ("#3A2410", 0), ("#5A3A1C", int(255 * a * 0.7))], [0, 0.5, 1])

    def _draw_wall(self, fr, xa, xb):
        c = fr.c
        T = self.T
        night = self.tod == "night"
        # tavan kirişleri
        R(c, xa, 0, xb, 188, T("#4A3220", 0.0))
        for jx in range(int(xa // 120) * 120 - 120, int(xb) + 120, 120):
            R(c, jx, 70, jx + 18, 170, T("#2E2014", 0.0))
        c.drawRect(skia.Rect.MakeLTRB(xa, 150, xb, 170), skia.Paint(Color=C(T("#3A2818", 0.0))))
        sh = skia.GradientShader.MakeLinear([(0, 70), (0, 188)], [C("#000000", 110), C("#000000", 0)], [0, 1])
        c.drawRect(skia.Rect.MakeLTRB(xa, 70, xb, 188), skia.Paint(Shader=sh))
        # korniş
        R(c, xa, 170, xb, 192, T("#D8C79A", 0.0))
        c.drawLine(xa, 192, xb, 192, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 170)))
        # duvar sıvası
        GRAD_V(c, xa, 192, xb, Y_CFLOOR - 28, [(T("#E3D3AA", 0.0), 0.0), (T("#D2BE90", 0.0), 1.0)])
        # lambri
        R(c, xa, Y_CFLOOR - 28, xb, Y_CFLOOR, T("#8A6A44", 0.0))
        c.drawLine(xa, Y_CFLOOR - 28, xb, Y_CFLOOR - 28, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 170)))
        # zemin (terrakota karolar, perspektif)
        y = Y_CFLOOR
        k = 0
        rowh = 12.0
        GRAD_V(c, xa, Y_CFLOOR, xb, 960, [(T("#7A4A32", 0.0), 0.0), (T("#B8754A", 0.0), 1.0)])
        while y < 960:
            wk = 70 + k * 20
            off = (k % 2) * wk / 2
            x = xa - (xa % wk) - wk + off
            while x < xb + wk:
                if (int(round((x - off) / wk)) + k) % 2 == 0:
                    R(c, x, y, x + wk, y + rowh, T("#8A4A30", 0.0), 90)
                x += wk
            c.drawLine(xa, y, xb, y, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#3A2418", 80)))
            y += rowh
            rowh *= 1.15
            k += 1
        # pencereler (delik) + çerçeve + eşik; arasında portreler, aplikler
        i0 = int(math.floor(xa / WIN_STEP)) - 1
        i1 = int(math.ceil(xb / WIN_STEP)) + 1
        for i in range(i0, i1 + 1):
            xc = i * WIN_STEP + 280
            ww = 190
            wx0, wx1 = xc - ww / 2, xc + ww / 2
            # delik (alfa) — arkadaki dış katmanlar görünsün
            hole = sk.poly_path([(wx0, Y_WIN0), (wx1, Y_WIN0), (wx1, Y_WIN1), (wx0, Y_WIN1)])
            c.drawPath(hole, skia.Paint(BlendMode=skia.BlendMode.kClear))
            # taş çerçeve
            for (a_, b_, c_, d_) in ((wx0 - 16, Y_WIN0 - 16, wx1 + 16, Y_WIN0), (wx0 - 16, Y_WIN1, wx1 + 16, Y_WIN1 + 18), (wx0 - 16, Y_WIN0, wx0, Y_WIN1), (wx1, Y_WIN0, wx1 + 16, Y_WIN1)):
                R(c, a_, b_, c_, d_, T("#C9C0A4", 0.0))
            INKR(c, wx0 - 16, Y_WIN0 - 16, wx1 + 16, Y_WIN1 + 18, 1.4, 180)
            INKR(c, wx0, Y_WIN0, wx1, Y_WIN1, 1.2, 160)
            # sol iç pervaz gölgesi (derinlik)
            sh = skia.GradientShader.MakeLinear([(wx0, 0), (wx0 + 34, 0)], [C("#000000", 80), C("#000000", 0)], [0, 1])
            c.drawRect(skia.Rect.MakeLTRB(wx0, Y_WIN0, wx0 + 34, Y_WIN1), skia.Paint(Shader=sh))
            # eşik
            R(c, wx0 - 24, Y_WIN1 + 18, wx1 + 24, Y_WIN1 + 32, T("#B9B096", 0.0))
            INKR(c, wx0 - 24, Y_WIN1 + 18, wx1 + 24, Y_WIN1 + 32, 1.2, 160)
            # ahşap kafes / ortada dikey çıta
            LINE(c, xc, Y_WIN0, xc, Y_WIN1, "#4A3A28", 3.0, 230)
            LINE(c, wx0, (Y_WIN0 + Y_WIN1) / 2 - 30, wx1, (Y_WIN0 + Y_WIN1) / 2 - 30, "#4A3A28", 2.4, 220)
            # portreler (pencere arası)
            xm = xc + WIN_STEP / 2
            rs = _RS(i * 11 + 4)
            if rs.rand() < 0.85:
                draw_portrait(c, xm - 62 - rs.randint(0, 10), 262 + rs.randint(0, 40), 124, 168 + rs.randint(0, 40), i * 7 + 1, T)
            if rs.rand() < 0.4:
                draw_portrait(c, xm + 82, 330 + rs.randint(0, 30), 84, 110, i * 7 + 2, T)
            # aplik (şamdan)
            sx = xm - 150
            R(c, sx - 3, 440, sx + 3, 476, T("#3A2A18", 0.0))
            R(c, sx - 10, 476, sx + 10, 484, T("#7A5A22", 0.0))
            R(c, sx - 2.4, 422, sx + 2.4, 440, "#F1E8CF")
            INKR(c, sx - 2.4, 422, sx + 2.4, 440, 0.9, 150)
        # baseboard gölgesi
        sh = skia.GradientShader.MakeLinear([(0, Y_CFLOOR), (0, Y_CFLOOR + 40)], [C("#1A1008", 90), C("#1A1008", 0)], [0, 1])
        c.drawRect(skia.Rect.MakeLTRB(xa, Y_CFLOOR, xb, Y_CFLOOR + 40), skia.Paint(Shader=sh))

    def _draw_fg(self, fr, xa, xb):
        c = fr.c
        T = self.T
        step = 1500
        i0 = int(math.floor(xa / step)) - 1
        for i in range(i0, i0 + int((xb - xa) / step) + 3):
            x = i * step + 820
            if x < xa - 200 or x > xb + 200:
                continue
            w = 96
            R(c, x - w / 2, OV - 40, x + w / 2, 960, T("#3A2A1C", 0.0))
            sh = skia.GradientShader.MakeLinear([(x - w / 2, 0), (x + w / 2, 0)], [C("#FFFFFF", 36), C("#FFFFFF", 0), C("#000000", 100)], [0, 0.3, 1.0])
            c.drawRect(skia.Rect.MakeLTRB(x - w / 2, OV - 40, x + w / 2, 960), skia.Paint(Shader=sh))
            INKR(c, x - w / 2, OV - 40, x + w / 2, 960, 1.6, 200)
            R(c, x - w * 0.75, 150, x + w * 0.75, 190, T("#4A3424", 0.0))
            INKR(c, x - w * 0.75, 150, x + w * 0.75, 190, 1.3, 190)

    # ── dinamik ─────────────────────────────────────────────────────────────
    def dyn_out_sky(self, ctx):
        c, t = ctx.c, ctx.t
        if ctx.night:
            return
        xa, xb = ctx.xa, ctx.xb
        rs = _RS(7)
        spr = cloud_sprite()
        pt = skia.Paint()
        for i in range(12):
            x0 = rs.uniform(0, self.layers["sky"].width)
            y = rs.uniform(OV + 100, 380)
            L = rs.uniform(240, 480)
            sp = rs.uniform(6, 14)
            pt.setAlphaf(rs.uniform(0.6, 0.95))
            x = (x0 + t * sp) % (self.layers["sky"].width + 400) - 200
            if x + L < xa - 20 or x > xb + 20:
                continue
            c.drawImageRect(spr, skia.Rect.MakeWH(spr.width(), spr.height()), skia.Rect.MakeXYWH(x, y - L * 0.11, L, L * 0.22), LIN, pt)

    def dyn_out_city(self, ctx):
        fl = getattr(self.F, "flag", None)
        if fl is not None:
            from cilt_kinds4 import _pennant
            _pennant(ctx.f, fl[0] + 1.0, fl[1] + 3, ctx.t, 1.0)
        FA.atmo_birds(ctx.c, ctx.t, 8, 1.0, ctx.xa, ctx.xb, 220, 420, speed=26.0, night=ctx.night, seed=5, size=0.9)

    def dyn_out_bank(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        col = "#FFF4D0" if ctx.night else "#FFFFFF"
        rs = _RS(14)
        for i in range(30):
            yy = Y_WATER + 14 + rs.uniform(0, 118)
            k = (yy - Y_WATER) / 130.0
            L = 16 + 40 * k
            span = (xb - xa) + 200
            xx = xa - 100 + (rs.uniform(0, span) + t * (6 + 14 * k)) % span
            al = (0.22 + 0.22 * math.sin(t * 1.7 + i * 1.3) ** 2) * (0.55 if ctx.night else 1.0)
            c.drawLine(xx, yy, xx + L, yy, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4 + 1.3 * k, Color=C(col, int(255 * al)), StrokeCap=skia.Paint.kRound_Cap))
        # nehirde tekneler (uzak, küçük)
        for j, (x0, v) in enumerate(((1800, 22.0), (4600, -18.0), (7200, 20.0))):
            x = x0 * 0.45 + v * t
            if xa - 200 < x < xb + 200:
                spr, wd, ht = boat_sprite("boat", ctx.tod)
                bob = math.sin(t * 1.2 + j) * 1.6
                c.save()
                c.translate(x, Y_WATER + 54 + j * 8 + bob)
                c.scale(0.6, 0.6)
                c.drawImage(spr.img, -spr.ox - wd / 2, -spr.oy, LIN)
                dirn = 1 if v > 0 else -1
                FA.actor(ctx.f, "denizci", 0, -4, 130, t, action="idle", dir=dirn, seed=j + 5)
                c.restore()

    def dyn_people(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        vis = [p for p in self.people if xa - 240 < p["x0"] + (0 if p["idle"] else p["dir"] * p["w"] * t) < xb + 240]
        vis.sort(key=lambda p: p["y"])
        for p in vis:
            if p["idle"]:
                FA.actor(f, p["kind"], p["x0"], p["y"], p["h"], t, action="talk", dir=p["dir"], seed=p["seed"], phase=p["phase"], energy=1.0)
            else:
                x = p["x0"] + p["dir"] * p["w"] * t
                FA.walker(f, p["kind"], x, p["y"], p["h"], t, speed=p["w"], dir=p["dir"], seed=p["seed"], phase=p["phase"], run=p["run"], prop=p["prop"])

    def dyn_light(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        night = ctx.night
        i0 = int(math.floor(xa / WIN_STEP)) - 1
        i1 = int(math.ceil(xb / WIN_STEP)) + 1
        for i in range(i0, i1 + 1):
            xc = i * WIN_STEP + 280
            fl = 0.88 + 0.12 * math.sin(t * 0.3 + i * 1.3)
            if not night:
                a = 0.17 * fl
                # zemine düşen güneş yaması (paralelkenar)
                p = sk.poly_path([(xc - 70, Y_CFLOOR + 6), (xc + 90, Y_CFLOOR + 6), (xc + 190, 940), (xc + 20, 940)])
                c.drawPath(p, skia.Paint(AntiAlias=True, Color=C("#FFE9A8", int(255 * a)), BlendMode=skia.BlendMode.kPlus))
                # pencere önünde hafif toz ışığı
                for k in range(8):
                    rs = _RS(i * 3 + k)
                    u = (rs.rand() + t * (0.01 + 0.01 * rs.rand())) % 1.0
                    xx = xc - 80 + rs.rand() * 160 + u * 60
                    yy = Y_WIN0 + 20 + (Y_CFLOOR - Y_WIN0 - 40) * u
                    c.drawCircle(xx, yy, 1.4 + 1.6 * rs.rand(), skia.Paint(AntiAlias=True, Color=C("#FFF3D0", int(150 * fl * (0.4 + 0.6 * abs(math.sin(t * 1.2 + k * 2.3))))), BlendMode=skia.BlendMode.kPlus))
            # aplik alevi
            sx = xc + WIN_STEP / 2 - 150
            flame = 0.82 + 0.18 * math.sin(t * 10 + i) + 0.08 * math.sin(t * 25 + i * 3)
            OVAL(c, sx, 416 - 5 * flame, 3.6, 9 * flame, "#FFC561", 240)
            OVAL(c, sx, 420, 1.8, 5 * flame, "#FFF4C0", 255)
            for (r, a_) in ((84, 34), (44, 60)):
                c.drawCircle(sx, 420, r * flame, skia.Paint(AntiAlias=True, Color=C("#FFB04A", a_ if not night else int(a_ * 1.9)), BlendMode=skia.BlendMode.kPlus))

    def dyn_fg(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        rs = _RS(45)
        for k in range(18):
            x = xa + ((rs.rand() * (xb - xa) + t * 16 * (0.5 + rs.rand())) % (xb - xa))
            y = 120 + rs.rand() * 700 + math.sin(t * 0.6 + k) * 12
            c.drawCircle(x, y, 1.5 + 2.2 * rs.rand(), skia.Paint(AntiAlias=True, Color=C("#FFEFC4", int(60 + 80 * rs.rand())), BlendMode=skia.BlendMode.kPlus))


WORLDS["corridor"] = Corridor
