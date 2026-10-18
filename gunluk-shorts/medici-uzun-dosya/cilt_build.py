"""cilt_build — ZAMAN ATLAMALI YAPIM çekimleri (`build` çekim türü).

  build="dome"   : Brunelleschi'nin kubbesi (1420–36). Katedral gövdesi + tambur üstünde sekizgen sivri çift kabuk; balık kılçığı (spina pesce) tuğla SIRA SIRA yükselir
                   (her sırada tuğlalar rastgele sırayla yerleşir), beyaz mermer nervürler, asma iskele halkaları + dikmeler, çarklı vinç (çarkın içinde yürüyen adam,
                   halatta sallanan yük), platformda mala/çekiç/halat çeken işçiler, tuğla taşıyıcılar, kireç ocağı dumanı, kuşlar; sonunda fener yükselir, iskele söker,
                   kamera geri çekilir. Kamera `crane up` (üst kenarı izler) + yavaş `orbit`; güneş yayı/gökyüzü/yüz parlaklığı ilerler (şafak → öğle → gün batımı).
  build="uffizi" : tek noktalı perspektifte iki kanatlı Uffizi avlusu (Vasari, 1560–80) ve Arno ucundaki revak; temel → portico → ara kat → piano nobile → çatı katı yükselir
                   (kaba duvar → sıva/pietra serena), iskele + çarklı vinç + taş yığınları + avluyu enine geçen taşıyıcılar + iskelede mala/çekiç işçileri + toz;
                   kamera avluya doğru ilerler ve yükselir; gün ışığı ilerler.
`shot("build", a, build="dome", p=(çapa_başlangıç, çapa_bitiş), orbit=10, tod="day"|"night", kick=…, caption=…)` — p verilmezse tüm çekim; p tek sayıysa sabit ilerleme;
cam/link/longtake/montage kabul edilir ve yok sayılır.
"""
import math

import numpy as np
import skia

import cilt_anim as FA
import cilt_city as CT
import cilt_medici as CM
import cilt_pano as PN
import sk
from cilt_medici import TH, ckind
from sk import C, H, W, clamp, ease_io, mix, smooth

INK = "#2A1A0C"
LIN = skia.SamplingOptions(skia.FilterMode.kLinear)
NEAR = skia.SamplingOptions()
D2R = math.pi / 180.0
BH = 800                               # çekim bandı yüksekliği (yerel koordinat 0..800)


# ═════════════════════════════ küçük yardımcılar ═════════════════════════════
_PC = {}


def pf(col, a=255):
    k = (col, a)
    p = _PC.get(k)
    if p is None:
        p = _PC[k] = skia.Paint(AntiAlias=True, Color=C(col, a))
    return p


def ps(col, w, a=255, cap=False):
    k = ("s", col, round(w, 1), a, cap)
    p = _PC.get(k)
    if p is None:
        p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, a))
        p.setStrokeJoin(skia.Paint.kRound_Join)
        if cap:
            p.setStrokeCap(skia.Paint.kRound_Cap)
        _PC[k] = p
    return p


def lerp(a, b, t):
    return a + (b - a) * t


def qn(x, n=20):
    return round(clamp(x) * n) / n


def path_of(pts, close=True):
    pa = skia.Path()
    pa.moveTo(*pts[0])
    for q in pts[1:]:
        pa.lineTo(*q)
    if close:
        pa.close()
    return pa


def poly(c, pts, paint):
    c.drawPath(path_of(pts), paint)


def seg(c, x0, y0, x1, y1, paint):
    c.drawLine(x0, y0, x1, y1, paint)


def mid(qa, qb, u):
    return (qa[0] + (qb[0] - qa[0]) * u, qa[1] + (qb[1] - qa[1]) * u)


# ═════════════════════════════ gökyüzü / güneş / bulut / tepe ═════════════════════════════
SKY_KEYS = [  # (p, üst, orta, ufuk, güneş)
    (0.00, "#6C7FB8", "#F0B49A", "#FBD9A0", "#FFD08A"),
    (0.25, "#6F9ED6", "#BCD2E2", "#F4E8C8", "#FFF0C8"),
    (0.55, "#5E92D0", "#B4CEE2", "#F6EEDA", "#FFF8E0"),
    (0.80, "#7A8FC4", "#E8B896", "#FAD9A0", "#FFD79A"),
    (1.00, "#5A5C9C", "#E8946A", "#F6C58A", "#FFB86A"),
]
NIGHT_SKY = ("#080F2A", "#17285A", "#34457A", "#EDE8D0")


def sky_cols(p, night=False):
    if night:
        return NIGHT_SKY
    for i in range(len(SKY_KEYS) - 1):
        a, b = SKY_KEYS[i], SKY_KEYS[i + 1]
        if p <= b[0] + 1e-9:
            t = clamp((p - a[0]) / max(1e-6, b[0] - a[0]))
            t = t * t * (3 - 2 * t)
            return tuple(mix(a[k], b[k], t) for k in range(1, 5))
    return SKY_KEYS[-1][1:]


_SKY = {}


def sky_img(p, night):
    key = (int(round(p * 100)), night)
    im = _SKY.get(key)
    if im is None:
        top, mid_, hor, _ = sky_cols(key[0] / 100.0, night)
        fr = sk.Frame(1, BH)
        sh = skia.GradientShader.MakeLinear([(0, 0), (0, BH * 0.80)], [C(top), C(mid_), C(hor)], [0.0, 0.60, 1.0])
        fr.c.drawRect(skia.Rect.MakeWH(1, BH), skia.Paint(Shader=sh))
        im = _SKY[key] = fr.surf.makeImageSnapshot()
    return im


def draw_sky(c, p, night, hz=0.80 * BH):
    """Gökyüzü degradesi (1 px'lik sütun görüntüsü, yatay uzatma): ufuk rengi hz çizgisine oturur."""
    im = sky_img(p, night)
    dy = hz - 0.80 * BH
    if dy > 0:
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, dy + 1), pf(sky_cols(p, night)[0]))
    c.drawImageRect(im, skia.Rect.MakeWH(1, BH), skia.Rect.MakeXYWH(0, dy, W, BH), NEAR, None)


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


def glow(c, x, y, r, col, a, plus=True):
    """Önbellekli, ÖNCEDEN RENKLENDİRİLMİŞ radyal parıltı (renk filtresi/kPlus bu CPU'da ≈6× yavaş; srcover + LIN ≈5 ms)."""
    _GP.setAlphaf(clamp(a))
    c.drawImageRect(glow_sprite(col), SRC128, skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), LIN, _GP)


def draw_sun(c, x, y, col, night=False, k=1.0):
    if night:
        glow(c, x, y, 230, "#9CB4E8", 0.34 * k)
        c.drawCircle(x, y, 28, pf("#F2EEDC"))
        for (dx, dy, rr) in ((-8, -6, 6), (9, 4, 8), (-3, 11, 4.5)):
            c.drawCircle(x + dx, y + dy, rr, pf("#D8D4C0", 150))
        return
    glow(c, x, y, 380, col, 0.34 * k)
    glow(c, x, y, 150, col, 0.60 * k)
    c.drawCircle(x, y, 30, pf("#FFFBE8"))


_STARS = {}


def draw_stars(c, t):
    im = _STARS.get("s")
    if im is None:
        fr = sk.Frame(W, 520)
        fr.clear(skia.ColorTRANSPARENT)
        rs = np.random.RandomState(5)
        for _ in range(170):
            x, y, r = rs.uniform(0, W), rs.uniform(0, 520), rs.uniform(0.6, 1.8)
            fr.c.drawCircle(x, y, r, pf("#F2EEDC", int(rs.uniform(110, 230))))
        im = _STARS["s"] = fr.surf.makeImageSnapshot()
    pt = skia.Paint()
    pt.setAlphaf(0.75 + 0.2 * math.sin(t * 1.3))
    c.drawImage(im, 0, 0, NEAR, pt)


_CL = {}


def draw_clouds(c, t, night, y_shift=0.0, seed=3, n=8, speed=1.0, ymin=90, ymax=330):
    cs = PN.cloud_sprite()
    key = (seed, n, ymin, ymax)
    L = _CL.get(key)
    if L is None:
        rs = np.random.RandomState(seed)
        L = _CL[key] = [(rs.uniform(0, 2600), rs.uniform(ymin, ymax), rs.uniform(220, 460), rs.uniform(7, 16), rs.uniform(0.55, 0.95)) for _ in range(n)]
    pt = skia.Paint()
    src = skia.Rect.MakeWH(cs.width(), cs.height())
    for (x0, y, Ln, sp, al) in L:
        x = (x0 + t * sp * speed) % (W + 900) - 450
        pt.setAlphaf(al * (0.30 if night else 0.9))
        c.drawImageRect(cs, src, skia.Rect.MakeXYWH(x, y + y_shift, Ln, Ln * 0.22), LIN, pt)


_HILL = {}


def hill_path(name, base, amp, sc, ph):
    pa = _HILL.get(name)
    if pa is None:
        pts = [(x, PN.ridge_y(x, base, amp, sc, ph)) for x in range(-480, W + 489, 8)]
        pa = skia.Path()
        pa.moveTo(*pts[0])
        for q in pts[1:]:
            pa.lineTo(*q)
        pa.lineTo(W + 488, 1500)
        pa.lineTo(-480, 1500)
        pa.close()
        _HILL[name] = pa
    return pa


def grade(c, p, night):
    """Gün ışığı sıcaklığı: şafak soğuk-leylak, öğle nötr, akşam sıcak amber (düşük alfalı örtü; srcover — çarpma kipi yavaş)."""
    if night:
        return
    kd = smooth((0.24 - p) / 0.24)
    ku = smooth((p - 0.70) / 0.30)
    if kd > 0.01:
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, BH), pf("#C8A0D0", int(46 * kd)))
    if ku > 0.01:
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, BH), pf("#FF8C3C", int(66 * ku)))


# ═════════════════════════════ ortak: yürüyüş mekik, çark, yük ═════════════════════════════
def _act_kw(kw, sd):
    kw = dict(kw or {})
    ph = kw.pop("phase", (sd * 0.13) % 1.0)
    return ph, kw


def shuttle(f, kind, t, xa, xb, yfn, h, v, pause=1.8, seed=0, t0=0.0, prop_ab=None, prop_ba=None, alpha=1.0, act="idle"):
    """xa→xb→xa mekik yürüyüşü (bacak içinde sabit hız v px/sn; uçlarda bekleme). Adım evresi her bacakta 'geçiş' pozuyla başlar. yfn(x) → ayak y'si."""
    L = abs(xb - xa)
    s = 1 if xb >= xa else -1
    if L < 8 or v < 3:
        FA.actor(f, kind, xa, yfn(xa), h, t, action=act, dir=s, seed=seed, phase=(seed * 0.37) % 1.0, alpha=alpha)
        return
    Tl = L / v
    cyc = 2 * (Tl + pause)
    tt = (t + t0) % cyc
    if tt < Tl:
        x, d, walk, lt, prop = xa + s * v * tt, s, True, tt, prop_ab
    elif tt < Tl + pause:
        x, d, walk, lt, prop = xb, s, False, tt, prop_ab
    elif tt < 2 * Tl + pause:
        lt = tt - Tl - pause
        x, d, walk, prop = xb - s * v * lt, -s, True, prop_ba
    else:
        x, d, walk, lt, prop = xa, -s, False, tt, prop_ba
    y = yfn(x)
    if walk:
        FA.walker(f, kind, x, y, h, lt, speed=v, dir=d, phase=0.31, seed=seed, prop=prop, alpha=alpha)
    else:
        FA.actor(f, kind, x, y, h, t, action=act, dir=d, seed=seed, phase=(seed * 0.37) % 1.0, alpha=alpha, prop=prop)


def treadwheel(f, x, y, R, ang, omega, t, night=False, alpha=1.0, seed=21):
    """Çift halkalı ahşap çark (merkez x,y; yarıçap R px). ang = dönüş (derece, + = saat yönü), omega = °/sn. İçinde yürüyen adam çarkın hızıyla yürür
    (saat yönünde dönüşte sağa yürür, ters dönüşte döner ve sola yürür)."""
    c = f.c
    wood = "#7A5230" if not night else "#4A3A32"
    dark = "#3A2410"
    sw = max(2.0, R * 0.075)
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.drawCircle(0, 0, R, ps(dark, sw + 2.4, int(200 * alpha)))
    c.drawCircle(0, 0, R, ps(wood, sw, int(235 * alpha)))
    for k in range(8):
        a_ = k * math.pi / 4
        seg(c, 0, 0, R * math.cos(a_), R * math.sin(a_), ps(wood, sw * 0.62, int(170 * alpha)))
    for k in range(24):
        a_ = k * math.pi / 12
        seg(c, R * 0.90 * math.cos(a_), R * 0.90 * math.sin(a_), R * math.cos(a_), R * math.sin(a_), ps(dark, sw * 0.7, int(190 * alpha)))
    c.restore()
    v = abs(omega) * D2R * R * 0.90
    hw = R * 0.80
    d = 1 if omega >= 0 else -1
    xf = x + 0.10 * R * d
    yf = y + R * 0.90 - 0.04 * R
    if v > 3.0:
        FA.walker(f, "halk", xf, yf, hw, t, speed=v, dir=d, phase=0.31, seed=seed, alpha=alpha)
    else:
        FA.actor(f, "halk", xf, yf, hw, t, action="idle", dir=d, seed=seed, alpha=alpha)
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.drawCircle(0, 0, R, ps(wood, sw * 0.9, int(120 * alpha)))
    for k in range(4):
        a_ = k * math.pi / 4 + math.pi / 8
        seg(c, -R * math.cos(a_), -R * math.sin(a_), R * math.cos(a_), R * math.sin(a_), ps(wood, sw * 0.5, int(105 * alpha)))
    c.restore()
    c.drawCircle(x, y, R * 0.13, pf(dark, int(255 * alpha)))
    c.drawCircle(x, y, R * 0.07, pf("#B8863A", int(255 * alpha)))


def load_block(c, x, y, w, kind="brick", alpha=1.0):
    """Halatta sarkan yük (üst orta = halat ucu): tuğla paketi veya kesme taş."""
    col, lo = ("#B8553A", "#8A3A24") if kind == "brick" else ("#C9B88C", "#9C8A68")
    hh = w * 0.72
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, y, x + w / 2, y + hh), pf(col, int(255 * alpha)))
    c.drawRect(skia.Rect.MakeLTRB(x + w * 0.18, y, x + w / 2, y + hh), pf(lo, int(110 * alpha)))
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, y, x + w / 2, y + hh), ps(INK, 1.2, int(200 * alpha)))
    if kind == "brick":
        for k in range(1, 4):
            seg(c, x - w / 2, y + hh * k / 4, x + w / 2, y + hh * k / 4, ps("#5A2412", 0.9, int(150 * alpha)))
    seg(c, x - w * 0.5, y + hh, x, y - w * 0.18, ps("#6A5A3A", 1.4, int(220 * alpha)))
    seg(c, x + w * 0.5, y + hh, x, y - w * 0.18, ps("#6A5A3A", 1.4, int(220 * alpha)))


def hoist_cycle(t, period=11.0, t0=0.0):
    """Yük döngüsü: (yükseklik oranı 0..1, çark yön işareti). Alçakta bekler → çıkar → üstte durur → iner."""
    u = ((t + t0) % period) / period
    if u < 0.06:
        return 0.0, 0.0
    if u < 0.46:
        return smooth((u - 0.06) / 0.40), 1.0
    if u < 0.56:
        return 1.0, 0.0
    if u < 0.94:
        return 1.0 - smooth((u - 0.56) / 0.38), -1.0
    return 0.0, 0.0


# ═════════════════════════════ şehir katmanı (bir kez pişirilir) ═════════════════════════════
FAR_Y = -60.0                  # uzak sıra tabanı (kubbe ekseninin gerisi; zemin çizgisine göre yerel y)
NEAR_Y = 118.0                 # ön sıra tabanı (kubbenin önü)


class Town:
    """Kubbenin çevresindeki Floransa: uzak sıra (tepeler, kuleler, çan kulesi, evler) ve ön sıra evler (orta boşluk = Piazza). Görüntü olarak bir kez pişirilir."""
    EX = 520                           # yan taşma (zum-out)
    HT = 560

    def __init__(self, seed, night):
        self.night = night
        self.T = CT.Tint("night" if night else "day")
        rs = np.random.RandomState(seed)

        def row(h0, h1, w0, w1, gap, hole=None):
            out, x = [], -self.EX - 60.0
            while x < W + self.EX + 60:
                w = rs.uniform(w0, w1)
                if hole is None or not (hole[0] < x + w / 2 < hole[1]):
                    out.append((x, w, rs.uniform(h0, h1), int(rs.randint(1, 10 ** 6))))
                x += w + rs.uniform(*gap)
            return out
        self.far = row(70, 135, 60, 120, (-8, 6))
        self.near = row(46, 92, 78, 150, (-14, 4), hole=(W / 2 - 460, W / 2 + 460))
        self._img = {}

    def _bake(self, which):
        EX, T, HT = self.EX, self.T, self.HT
        fr = sk.Frame(W + 2 * EX, HT)
        fr.clear(skia.ColorTRANSPARENT)
        c = fr.c
        c.translate(EX, HT - 30)                  # (0,0) = sahne x=0, taban çizgisi
        lit = []
        if which == "far":
            for nm, base, amp, sc, ph, col in (("h1", -190, 38, 540, 0.0, "#A9BDB6"), ("h2", -140, 44, 360, 2.0, "#93AFA5")):
                c.drawPath(hill_path(nm, base, amp, sc, ph), pf(T(col, 0.25)))
            for (x, w, h_, sd) in self.far:
                CT.draw_house(c, x, -2, w, h_, np.random.RandomState(sd), T, 0.55, lit)
            CT.draw_tower(c, -780, -2, 46, 340, T, 0.45, False)                        # Palazzo Vecchio kulesi (uzak)
            CT.draw_campanile(c, W / 2 + 640, -2, 92, 380, T, 0.28)                    # Giotto çan kulesi
            CT.draw_tower(c, W + 640, -2, 40, 270, T, 0.5, True)
        else:
            for (x, w, h_, sd) in self.near:
                CT.draw_house(c, x, 0, w, h_, np.random.RandomState(sd), T, 0.0, lit)
            CT.draw_bapt(c, W / 2 - 560, 0, 210, 90, T, 0.0)                           # vaftizhane (ön-sol)
            rs = np.random.RandomState(9)
            for i in range(12):
                x = rs.uniform(-EX, W + EX)
                if W / 2 - 440 < x < W / 2 + 440:
                    continue
                hh = rs.uniform(70, 130)
                c.drawPath(sk.poly_path([(x - 9, 0), (x, -hh), (x + 9, 0)]), pf(T("#4E6A3E", 0.1)))
        if self.night:
            CT._lit_windows(c, np.random.RandomState(4), lit, True, 0.5)
        return fr.surf.makeImageSnapshot()

    def draw(self, c, which):
        im = self._img.get(which)
        if im is None:
            im = self._img[which] = self._bake(which)
        base = FAR_Y if which == "far" else NEAR_Y
        c.drawImage(im, -self.EX, base - (self.HT - 30), LIN)


_TOWN = {}


def town_for(seed, night):
    k = (seed, night)
    if k not in _TOWN:
        _TOWN[k] = Town(seed, night)
    return _TOWN[k]


# ═════════════════════════════ KUBBE ═════════════════════════════
NC = 44                                  # kabuk sıra sayısı
NZ = 12                                  # sıra başına balık kılçığı bölmesi
R0 = 285.0                               # kubbe tabanı (sekizgen iç teğet yarıçapı)
COSR = math.cos(22.5 * D2R)
HB = 150.0                               # katedral gövde yüksekliği
RB = 392.0                               # gövde iç teğet yarıçapı
ROOF_H = 36.0
DRUM_H = 150.0
Y_D0 = HB + ROOF_H                       # tambur tabanı
Y_D1 = Y_D0 + DRUM_H                     # tambur üstü = kubbe tabanı
H_DOME = 430.0
LANT_H = 190.0
R_TOP = 42.0
E_DEG = 13.0
CE, SE = math.cos(E_DEG * D2R), math.sin(E_DEG * D2R)
VY0 = 300.0                              # başlangıç kamera (zemin çizgisi y = 400 + VY0 = 700)
ZS_END = 0.68

U_ = np.linspace(0.0, 1.0, NC + 1)
PROF = R0 * np.power(np.clip(1.0 - np.power(U_, 1.75), 0.0, 1.0), 0.60) + R_TOP * U_
RAD = PROF / COSR                         # köşe yarıçapı (sıra seviyesi başına)
YS = Y_D1 + U_ * H_DOME
PSI8 = np.arange(9) * 45.0 - 22.5         # köşe açıları (8 ≡ 0)
DELAY = np.random.RandomState(7).rand(8, NC + 1, NZ) * 0.70


def prof_at(u):
    u = clamp(u)
    return R0 * (max(0.0, 1.0 - u ** 1.75) ** 0.60) + R_TOP * u


class VCam:
    __slots__ = ("a", "vy", "zs")

    def __init__(self, a, vy, zs):
        self.a, self.vy, self.zs = a, vy, zs

    def P(self, rho, psi, Y):
        pp = (psi - self.a) * D2R
        return (W / 2 + rho * math.sin(pp) * self.zs, 400.0 - ((Y * CE - rho * math.cos(pp) * SE) - self.vy) * self.zs)

    def R(self, rho, th, Y):
        """Halka noktası (th = kameraya göre açı; 0 = en önde)."""
        pp = th * D2R
        return (W / 2 + rho * math.sin(pp) * self.zs, 400.0 - ((Y * CE - rho * math.cos(pp) * SE) - self.vy) * self.zs)


def lit_of(psi_n, a, az_sun):
    """Yüz parlaklığı 0..1 (ışık sol-üstten + güneş azimutuna göre kayar; hiçbir yüz tam karanlık değil)."""
    front = math.cos((psi_n - a) * D2R)
    ang = (psi_n - a - az_sun * 0.85 - 18.0) * D2R
    return clamp(0.30 * max(front, 0.0) + 0.78 * max(math.cos(ang), 0.0) - 0.04)


def sun_state(p):
    az = lerp(-70.0, 70.0, p)
    el = 0.18 + 0.82 * math.sin(math.pi * clamp(p)) ** 0.8
    return az, el, sky_cols(round(clamp(p) * 50) / 50.0)[3]


class Shot:
    """Sahne durumu (gün/gece tonu + şehir)."""

    def __init__(self, tod, seed, town=False):
        self.tod = tod
        self.night = tod == "night"
        self.T = CT.Tint("night" if self.night else "day")
        self.town = town_for(seed, self.night) if town else None

    def col(self, lo, hi, lit):
        c = mix(lo, hi, qn(lit, 20))
        return self.T(c, 0.0) if self.night else c

    def tc(self, c):
        return self.T(c, 0.0) if self.night else c


def _face_poly(SXl, SYl, k, j0, j1):
    pa = skia.Path()
    pa.moveTo(SXl[j0][k], SYl[j0][k])
    for j in range(j0 + 1, j1 + 1):
        pa.lineTo(SXl[j][k], SYl[j][k])
    for j in range(j1, j0 - 1, -1):
        pa.lineTo(SXl[j][k + 1], SYl[j][k + 1])
    pa.close()
    return pa


def shell_face(c, S, k, SXl, SYl, n_done, lit, interior=False):
    """Kubbe kabuğunun bir yüzü: tamamlanmış sıralar (tek dolgu + sıra çizgileri + balık kılçığı) + büyümekte olan sıra (tuğlalar rastgele sırayla yerleşir)."""
    jt = min(int(n_done), NC)
    frac = n_done - int(n_done) if jt < NC else 0.0
    if interior:
        jt = min(NC, jt + (1 if frac > 0.5 else 0))
        frac = 0.0
        fill = S.col("#4A2024", "#7A3A34", lit * 0.5)
    else:
        fill = S.col("#7A3236", "#D6693A", lit)
    if jt >= 1:
        c.drawPath(_face_poly(SXl, SYl, k, 0, jt), pf(fill))
        alt = skia.Path()
        for j in range(1, jt, 2):
            alt.moveTo(SXl[j][k], SYl[j][k])
            alt.lineTo(SXl[j][k + 1], SYl[j][k + 1])
            alt.lineTo(SXl[j + 1][k + 1], SYl[j + 1][k + 1])
            alt.lineTo(SXl[j + 1][k], SYl[j + 1][k])
            alt.close()
        c.drawPath(alt, pf("#1A0A06", 26 if not interior else 40))
        ln = skia.Path()
        zz = skia.Path()
        for j in range(0, jt + 1):
            ln.moveTo(SXl[j][k], SYl[j][k])
            ln.lineTo(SXl[j][k + 1], SYl[j][k + 1])
        for j in range(0, jt):
            ax, ay, bx, by = SXl[j][k], SYl[j][k], SXl[j][k + 1], SYl[j][k + 1]
            cx_, cy_, dx_, dy_ = SXl[j + 1][k], SYl[j + 1][k], SXl[j + 1][k + 1], SYl[j + 1][k + 1]
            zz.moveTo(ax, ay)
            for i in range(1, NZ + 1):
                u = i / NZ
                if i % 2 == 1:
                    zz.lineTo(cx_ + (dx_ - cx_) * u, cy_ + (dy_ - cy_) * u)
                else:
                    zz.lineTo(ax + (bx - ax) * u, ay + (by - ay) * u)
        c.drawPath(ln, ps("#3A1608", 0.9, 120 if not interior else 150))
        c.drawPath(zz, ps("#4A1C0C", 0.8, 96 if not interior else 130))
        if not interior:
            c.drawPath(_face_poly(SXl, SYl, k, 0, jt), ps(INK, 1.3, 170))
    if frac > 0.0 and jt < NC and not interior:
        ax, ay, bx, by = SXl[jt][k], SYl[jt][k], SXl[jt][k + 1], SYl[jt][k + 1]
        cx_, cy_, dx_, dy_ = SXl[jt + 1][k], SYl[jt + 1][k], SXl[jt + 1][k + 1], SYl[jt + 1][k + 1]
        hs = np.clip((frac - DELAY[k, jt]) / 0.30, 0.0, 1.0)
        pa = skia.Path()
        pa.moveTo(ax, ay)
        pa.lineTo(bx, by)
        for i in range(NZ - 1, -1, -1):
            h_ = float(hs[i])
            u1, u0 = (i + 1) / NZ, i / NZ
            b1 = (ax + (bx - ax) * u1, ay + (by - ay) * u1)
            b0 = (ax + (bx - ax) * u0, ay + (by - ay) * u0)
            t1 = (cx_ + (dx_ - cx_) * u1, cy_ + (dy_ - cy_) * u1)
            t0 = (cx_ + (dx_ - cx_) * u0, cy_ + (dy_ - cy_) * u0)
            pa.lineTo(b1[0] + (t1[0] - b1[0]) * h_, b1[1] + (t1[1] - b1[1]) * h_)
            pa.lineTo(b0[0] + (t0[0] - b0[0]) * h_, b0[1] + (t0[1] - b0[1]) * h_)
        pa.close()
        c.drawPath(pa, pf(S.col("#9A4A40", "#F08A54", lit)))
        c.drawPath(pa, ps("#3A1608", 0.9, 130))


def prism_faces(cam, k_list, r, Y0, Y1, az_sun):
    """Sekizgen prizma yüzleri (köşe yarıçapı r/COSR): [(k, quad(BL,BR,TR,TL), lit)]."""
    out = []
    rho = r / COSR
    for k in k_list:
        q = [cam.P(rho, PSI8[k], Y0), cam.P(rho, PSI8[k + 1], Y0), cam.P(rho, PSI8[k + 1], Y1), cam.P(rho, PSI8[k], Y1)]
        out.append((k, q, lit_of(45.0 * k, cam.a, az_sun)))
    return out


def qpt(q, u, v):
    return (q[0][0] + (q[1][0] - q[0][0]) * u + (q[3][0] - q[0][0]) * v, q[0][1] + (q[1][1] - q[0][1]) * u + (q[3][1] - q[0][1]) * v)


def arch_pts(q, u0, u1, v0, v1, n=7):
    """Yuvarlak kemerli açıklık (yüz paralelkenarı içinde): dikdörtgen + yarım daire üst."""
    um, ru = (u0 + u1) / 2, (u1 - u0) / 2
    wpx = abs(q[1][0] - q[0][0])
    hpx = max(1.0, abs(q[3][1] - q[0][1]))
    rv = ru * wpx / hpx
    pts = [qpt(q, u0, v0), qpt(q, u0, v1)]
    for i in range(1, n):
        a_ = math.pi * (1 - i / n)
        pts.append(qpt(q, um + ru * math.cos(a_), v1 + rv * math.sin(a_)))
    pts += [qpt(q, u1, v1), qpt(q, u1, v0)]
    return pts


def draw_base(c, S, cam, az_sun):
    """Katedral gövdesi (çok renkli mermer) + eğimli kiremit çatı halkası + tambur (yeşil bantlar, gözler, köşe pilastrları)."""
    a = cam.a
    fr_ks = [k for k in range(8) if math.cos((45.0 * k - a) * D2R) > 0.02]
    for (k, q, lit) in prism_faces(cam, fr_ks, RB, 0.0, HB, az_sun):
        poly(c, q, pf(S.col("#B7AD92", "#EFE6CE", lit)))
        for (v0, v1) in ((0.30, 0.37), (0.66, 0.73)):
            poly(c, [qpt(q, 0, v0), qpt(q, 1, v0), qpt(q, 1, v1), qpt(q, 0, v1)], pf(S.col("#4E7A5C", "#7CA286", lit), 235))
        for (u0, u1) in ((0.16, 0.30), (0.70, 0.84)):
            poly(c, arch_pts(q, u0, u1, 0.42, 0.56, 6), pf(S.tc("#3A2A1C"), 215))
        for u in (0.0, 1.0):
            seg(c, *qpt(q, u, 0.0), *qpt(q, u, 1.0), ps(S.col("#CFC6AE", "#FFF7E2", lit), 4.0))
        poly(c, q, ps(INK, 1.3, 170))
    rho0, rho1 = RB / COSR, (R0 * 1.02) / COSR
    for k in sorted(range(8), key=lambda k: math.cos((45.0 * k - a) * D2R)):
        q = [cam.P(rho0, PSI8[k], HB), cam.P(rho0, PSI8[k + 1], HB), cam.P(rho1, PSI8[k + 1], Y_D0), cam.P(rho1, PSI8[k], Y_D0)]
        lit = lit_of(45.0 * k, a, az_sun)
        poly(c, q, pf(S.col("#7A3A2A", "#C45E36", lit)))
        for u in (0.2, 0.4, 0.6, 0.8):
            seg(c, *mid(q[0], q[1], u), *mid(q[3], q[2], u), ps("#3A1608", 0.9, 100))
        poly(c, q, ps(INK, 1.1, 150))
    for (k, q, lit) in prism_faces(cam, fr_ks, R0, Y_D0, Y_D1, az_sun):
        poly(c, q, pf(S.col("#BDB29A", "#F4EBD4", lit)))
        for (v0, v1) in ((0.20, 0.27), (0.74, 0.81)):
            poly(c, [qpt(q, 0, v0), qpt(q, 1, v0), qpt(q, 1, v1), qpt(q, 0, v1)], pf(S.col("#4E7A5C", "#79A284", lit), 240))
        wf = abs(q[1][0] - q[0][0])
        mx, my = qpt(q, 0.5, 0.52)
        rr = max(2.0, 0.17 * wf)
        oc = skia.Rect.MakeLTRB(mx - rr * 0.95, my - rr * 1.35, mx + rr * 0.95, my + rr * 1.35)
        c.drawOval(oc, pf(S.tc("#2A2018"), 235))
        c.drawOval(oc, ps(S.col("#CFC6AE", "#FFF7E2", lit), max(1.5, wf * 0.018)))
        for u in (0.0, 1.0):
            seg(c, *qpt(q, u, 0.0), *qpt(q, u, 1.0), ps(S.col("#D8CFB6", "#FFFAEA", lit), max(2.0, min(10.0, wf * 0.045))))
        poly(c, q, ps(INK, 1.4, 190))


def draw_lantern(c, S, cam, lp, az_sun):
    """Fener (tempietto): sekizgen mermer kule, kemerli pencereler, konik çatı, yaldızlı küre ve haç — alttan yukarı yükselir (lp 0..1)."""
    if lp <= 0.0:
        return
    Yb = Y_D1 + H_DOME
    ytop = cam.P(0.0, 0.0, Yb + lp * (LANT_H + 60.0))[1]
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, ytop, W, BH))
    a = cam.a
    fr_ks = [k for k in range(8) if math.cos((45.0 * k - a) * D2R) > 0.02]
    for (r, y0, y1, base_col) in ((54.0, 0.0, 14.0, "#CFC6AE"), (46.0, 14.0, 132.0, "#F6EEDA"), (53.0, 132.0, 146.0, "#D8CFB6")):
        for (k, q, lit) in prism_faces(cam, fr_ks, r, Yb + y0, Yb + y1, az_sun):
            poly(c, q, pf(S.col("#B0A68E", base_col, lit)))
            if y0 == 14.0:
                pts = arch_pts(q, 0.22, 0.78, 0.18, 0.62, 8)
                poly(c, pts, pf(S.tc("#2A2018"), 235))
                poly(c, pts, ps(S.col("#CFC6AE", "#FFF7E2", lit), 1.4))
                for u in (0.0, 1.0):
                    seg(c, *qpt(q, u, 0.0), *qpt(q, u, 1.0), ps(S.col("#D8CFB6", "#FFFAEA", lit), 4.0))
            poly(c, q, ps(INK, 1.2, 180))
    apex = cam.P(0.0, 0.0, Yb + 196.0)
    rho = 53.0 / COSR
    for k in sorted(range(8), key=lambda k: math.cos((45.0 * k - a) * D2R)):
        if math.cos((45.0 * k - a) * D2R) < -0.2:
            continue
        p0, p1 = cam.P(rho, PSI8[k], Yb + 146.0), cam.P(rho, PSI8[k + 1], Yb + 146.0)
        lit = lit_of(45.0 * k, a, az_sun)
        poly(c, [p0, p1, apex], pf(S.col("#B8B0A0", "#EFE8D6", lit)))
        poly(c, [p0, p1, apex], ps(INK, 1.1, 170))
    bx, by = cam.P(0.0, 0.0, Yb + 204.0)
    z_ = cam.zs
    c.drawCircle(bx, by, 9.0 * z_, pf("#D8A63A"))
    c.drawCircle(bx - 2.5 * z_, by - 3 * z_, 3.2 * z_, pf("#FFF0B0", 190))
    seg(c, bx, by - 8 * z_, bx, by - 40 * z_, ps("#D8A63A", 3.2 * z_, 255, True))
    seg(c, bx - 9 * z_, by - 28 * z_, bx + 9 * z_, by - 28 * z_, ps("#D8A63A", 3.0 * z_, 255, True))
    c.restore()


def ring_poly(cam, R_in, R_out, th0, th1, Y, n=26):
    outer = [cam.R(R_out, th0 + (th1 - th0) * i / n, Y) for i in range(n + 1)]
    inner = [cam.R(R_in, th1 + (th0 - th1) * i / n, Y) for i in range(n + 1)]
    return outer + inner


def draw_deck_back(c, S, cam, Yp, R_in, R_out, al):
    """Arka yarım platform (gök karşısında görünen kısım) + arka dikmeler."""
    if al <= 0.01:
        return
    z_ = cam.zs
    pts = ring_poly(cam, R_in, R_out, 100.0, 260.0, Yp)
    poly(c, pts, pf(S.tc("#6A4426"), int(255 * al)))
    poly(c, pts, ps(INK, 1.1, int(150 * al)))
    for th in range(110, 260, 14):
        x0, y0 = cam.R(R_out, th, Yp)
        x1, y1 = cam.R(R_out, th, Yp + 44.0)
        seg(c, x0, y0, x1, y1, ps("#3A2410", 2.4 * z_, int(200 * al), True))
    c.drawPath(path_of([cam.R(R_out, th, Yp + 44.0) for th in range(100, 261, 8)], False), ps("#3A2410", 2.0 * z_, int(190 * al), True))


def draw_deck_front(c, S, cam, Yp, R_in, R_out, al, night, t):
    """Ön yarım platform: plank dolgusu + tahta çizgileri + alt halkalar (eski platformlar) + korkuluk dikmeleri/halat + tuğla yığınları (+ gece meşaleleri)."""
    if al <= 0.01:
        return
    z_ = cam.zs
    a8 = int(255 * al)
    c.drawPath(path_of([cam.R(R_in - 6, th, Yp - 26.0) for th in range(-96, 97, 8)], False), ps("#1A0A06", 22.0 * z_, int(46 * al)))
    pts = ring_poly(cam, R_in, R_out, -100.0, 100.0, Yp)
    poly(c, pts, pf(S.tc("#7A5230"), a8))
    for th in range(-96, 97, 6):
        x0, y0 = cam.R(R_in, th, Yp)
        x1, y1 = cam.R(R_out, th, Yp)
        seg(c, x0, y0, x1, y1, ps("#3A2410", 1.0, int(110 * al)))
    c.drawPath(path_of([cam.R(R_out, th, Yp) for th in range(-100, 101, 8)], False), ps("#3A2410", 3.0 * z_, int(230 * al), True))
    poly(c, pts, ps(INK, 1.1, int(150 * al)))
    for dY, Yup in ((-118.0, Yp), (-236.0, Yp - 118.0)):
        Yl = Yp + dY
        if Yl < Y_D1 - 80:
            continue
        c.drawPath(path_of([cam.R(R_out + 10, th, Yl) for th in range(-100, 101, 8)], False), ps("#3A2410", 4.4 * z_, int(210 * al), True))
        c.drawPath(path_of([cam.R(R_out + 10, th, Yl) for th in range(-100, 101, 8)], False), ps(S.tc("#7A5230"), 2.6 * z_, a8, True))
        for th in range(-90, 91, 30):
            x0, y0 = cam.R(R_out + 10, th, Yl)
            x1, y1 = cam.R(R_out, th, Yup)
            seg(c, x0, y0, x1, y1, ps("#3A2410", 2.0 * z_, int(190 * al), True))
    tops = []
    for th in range(-96, 97, 12):
        x0, y0 = cam.R(R_out, th, Yp)
        x1, y1 = cam.R(R_out, th, Yp + 40.0)
        seg(c, x0, y0, x1, y1, ps("#3A2410", 3.4 * z_, int(230 * al), True))
        seg(c, x0, y0, x1, y1, ps(S.tc("#7A5230"), 2.0 * z_, a8, True))
        tops.append((x1, y1))
    c.drawPath(path_of(tops, False), ps("#6A5A3A", 1.6 * z_, int(200 * al)))
    for th in (-30, 12, 44):
        x, y = cam.R(0.5 * (R_in + R_out), th, Yp)
        for r_ in range(3):
            for k_ in range(3 - r_):
                bx = x - (3 - r_) * 6 * z_ + k_ * 12 * z_
                rc = skia.Rect.MakeXYWH(bx, y - (r_ + 1) * 8 * z_, 11 * z_, 7 * z_)
                c.drawRect(rc, pf(S.tc("#B8553A"), a8))
                c.drawRect(rc, ps(INK, 0.8, int(150 * al)))
    if night:
        for th in (-84, -42, 0, 42, 84):
            x, y = cam.R(R_out, th, Yp + 40.0)
            fl = 1.0 + 0.1 * math.sin(t * 9.0 + th)
            glow(c, x, y - 6, 52 * fl * z_, "#FFB04A", 0.55 * al)
            c.drawCircle(x, y - 5 * z_, 3.4 * z_, pf("#FFE08A"))


CREW = [
    (-66, "halk", "work", dict(mode="lay", period=1.9, phase=0.10), 1, 11),
    (-47, "denizci", "work", dict(mode="strike"), -1, 12),
    (-27, "halk", "work", dict(mode="lay", period=1.7, phase=0.55, high=0.4), 1, 13),
    (-4, "soylu", "point", None, -1, 14),
    (17, "tuccar", "talk", dict(energy=0.9), 1, 15),
    (37, "halk", "work", dict(mode="lay", period=2.0, phase=0.30), -1, 16),
    (53, "halk", "work", dict(mode="haul", period=1.6, phase=0.0), 1, 17),
    (60, "denizci", "work", dict(mode="haul", period=1.6, phase=0.12), 1, 18),
]
CARRY = [(-70, 34, 30.0, 31, 0.0, "basket", "halk"), (-58, 24, 26.0, 32, 5.5, "sack", "cocuk"), (30, -62, 28.0, 33, 2.4, "basket", "denizci")]


def draw_crew(f, S, cam, Yp, R_mid, t, al):
    z_ = cam.zs
    h_ = 58.0 * z_
    FA.set_scale_hint(z_)
    for (th, kind, act, kw, dr, sd) in CREW:
        x, y = cam.R(R_mid, th, Yp)
        if act == "point":
            FA.actor(f, kind, x, y + 2, h_, t % 9.0, action="point", dir=dr, seed=sd, phase=0.2, alpha=al, t0=1.2, dur=3.4, target=(0.55, -0.8))
        else:
            ph, kw2 = _act_kw(kw, sd)
            FA.actor(f, kind, x, y + 2, h_, t, action=act, dir=dr, seed=sd, phase=ph, alpha=al, **kw2)
    for (a0, a1, v, sd, t0, prop, kind) in CARRY:
        xs0, xs1 = cam.R(R_mid, a0, Yp)[0], cam.R(R_mid, a1, Yp)[0]

        def yfn(x):
            s_ = clamp((x - W / 2) / max(1.0, R_mid * z_), -0.99, 0.99)
            return cam.R(R_mid, math.degrees(math.asin(s_)), Yp)[1] + 2
        shuttle(f, kind, t, xs0, xs1, yfn, h_ * (0.86 if kind == "cocuk" else 1.0), v * z_, pause=2.2, seed=sd, t0=t0, prop_ab=prop, prop_ba=None, alpha=al)
    FA.set_scale_hint(1.0)


def draw_crane(f, S, cam, Yp, R_mid, t, al, night):
    """Çarklı vinç: A-çerçeve direk + bom + halat + yük; çarkın içindeki adam yük çıkarken ileri, inerken geri yürür."""
    c = f.c
    z_ = cam.zs
    xc, yc = cam.R(R_mid, 70.0, Yp)
    a8 = int(255 * al)
    wood = S.tc("#7A5230")
    dark = "#3A2410"
    k, sgn = hoist_cycle(t, 11.0)
    k2, _ = hoist_cycle(t + 0.05, 11.0)
    omega = (k2 - k) / 0.05 * 150.0
    apex = (xc, yc - 250 * z_)
    tip = (xc + 190 * z_, yc - 214 * z_)
    for dx in (-34, 34):
        seg(c, xc + dx * z_, yc + 3, apex[0] + dx * 0.10 * z_, apex[1], ps(dark, 7.0 * z_, int(235 * al), True))
        seg(c, xc + dx * z_, yc + 3, apex[0] + dx * 0.10 * z_, apex[1], ps(wood, 4.4 * z_, a8, True))
    seg(c, xc - 30 * z_, yc - 90 * z_, xc + 30 * z_, yc - 150 * z_, ps(wood, 2.8 * z_, a8))
    seg(c, xc + 30 * z_, yc - 90 * z_, xc - 30 * z_, yc - 150 * z_, ps(wood, 2.8 * z_, a8))
    seg(c, apex[0], apex[1], tip[0], tip[1], ps(dark, 7.0 * z_, int(235 * al), True))
    seg(c, apex[0], apex[1], tip[0], tip[1], ps(wood, 4.4 * z_, a8, True))
    seg(c, xc + 24 * z_, yc - 80 * z_, tip[0] - 26 * z_, tip[1] + 4 * z_, ps(wood, 3.0 * z_, a8))
    R = 60.0 * z_
    wx, wy = xc - 128 * z_, yc - 62 * z_
    treadwheel(f, wx, wy, R, k * 150.0, omega, t, night, al)
    seg(c, wx + R * 0.1, wy - R * 0.1, apex[0] - 6 * z_, apex[1] + 3 * z_, ps("#6A5A3A", 1.8 * z_, int(215 * al)))
    y_low = yc + 540 * z_
    y_hi = tip[1] + 56 * z_
    ly = lerp(y_low, y_hi, k)
    sway = math.sin(t * 1.4) * 4.0 * z_ * min(1.0, k * 2.0) * (1 - 0.5 * abs(sgn))
    seg(c, tip[0], tip[1], tip[0] + sway, ly, ps("#6A5A3A", 1.8 * z_, int(235 * al)))
    c.drawCircle(tip[0], tip[1], 6.0 * z_, pf(dark, a8))
    load_block(c, tip[0] + sway, ly, 34.0 * z_, "brick", al)
    for q in range(5):
        ph = (t * 0.2 + q / 5.0) % 1.0
        FA._puff(c, tip[0] + sway + (q - 2) * 8 * z_, ly + 20 * z_ + ph * 40 * z_, (8 + 18 * ph) * z_, 0.18 * (1 - ph) * al * min(1.0, k * 3), "#D8C8A8")


def dome_cam(p, a_orbit):
    """Kamera: üst kenarı izleyen crane-up; sonda geri çekilme (zum-out + alçalma). Dönüş: (cam, n_done, lp, scaffold_alpha)."""
    q = clamp(p / 0.78)
    lp = clamp((p - 0.78) / 0.12)
    r = smooth((p - 0.88) / 0.12)
    Yw = (Y_D1 + q * H_DOME) * CE + lp * (LANT_H + 30.0) * CE
    k = 22.0
    vy_follow = VY0 + k * math.log1p(math.exp((Yw - 100.0 - VY0) / k))
    vy_end = VY0 / ZS_END
    vy = lerp(vy_follow, vy_end, r)
    zs = lerp(1.0, ZS_END, r)
    return VCam(a_orbit, vy, zs), q * NC, lp, 1.0 - smooth((p - 0.86) / 0.07)


def draw_dome(f, cx, p, t, night, S, a_orbit):
    c = f.c
    cam, n_done, lp, sc_al = dome_cam(p, a_orbit)
    az_sun, el, sun_col = sun_state(p)
    z_ = cam.zs
    gy = 400.0 + cam.vy * z_
    draw_sky(c, p, night, hz=gy - 200.0 * z_)
    if night:
        draw_stars(c, t)
        draw_sun(c, W * 0.78, 150, sun_col, True)
    else:
        sx = W / 2 + az_sun / 70.0 * 800.0
        sy = lerp(gy - 190.0, 150.0, el) - 40.0 * (1 - el)
        draw_sun(c, sx, sy, sun_col, False, 1.0)
    draw_clouds(c, t, night, y_shift=(gy - 700.0) * 0.12, speed=1.6)
    FA.atmo_birds(c, t, 6, 1.0, 0, W, 190, 420, 24.0, night, 3, 1.1)
    # şehir: uzak sıra + zemin
    c.save()
    c.translate(W / 2, gy)
    c.scale(z_, z_)
    c.translate(-W / 2, 0)
    S.town.draw(c, "far")
    c.drawRect(skia.Rect.MakeLTRB(-S.town.EX, FAR_Y - 2, W + S.town.EX, 700), pf(S.tc("#A89870")))
    for i in range(26):
        xx = ((i * 233 + 40) % (W + 600)) - 300
        yy = FAR_Y + 6 + ((i * 97) % 170)
        seg(c, xx, yy, xx + 34 + (i % 5) * 8, yy, ps("#3A2A18", 1.2, 60))
    c.restore()
    # gövde + çatı + tambur
    draw_base(c, S, cam, az_sun)
    # kabuk, iç yüzey, nervürler
    a = cam.a
    pp = (PSI8 - a) * D2R
    SIN, COS = np.sin(pp), np.cos(pp)
    SX = (W / 2 + (RAD[:, None] * SIN[None, :]) * z_).tolist()
    SY = (400.0 - ((YS[:, None] * CE - (RAD[:, None] * COS[None, :]) * SE) - cam.vy) * z_).tolist()
    fr_ks = [k for k in range(8) if math.cos((45.0 * k - a) * D2R) > 0.02]
    bk_ks = [k for k in range(8) if k not in fr_ks]
    u_top = clamp(n_done / NC)
    Y_top = Y_D1 + u_top * H_DOME
    rho_top = prof_at(u_top) / COSR
    R_in = max(rho_top + 4.0, 105.0)
    R_out = R_in + 46.0
    Rm = 0.5 * (R_in + R_out)
    Yp = Y_top - 6.0
    scaf = sc_al > 0.01 and p < 0.93
    if scaf:
        draw_deck_back(c, S, cam, Yp, R_in, R_out, sc_al)
    for k in bk_ks:
        shell_face(c, S, k, SX, SY, n_done, lit_of(45.0 * k, a, az_sun), interior=True)
    for k in fr_ks:
        shell_face(c, S, k, SX, SY, n_done, lit_of(45.0 * k, a, az_sun))
    if 0.5 < n_done < NC:
        outer = [cam.P(rho_top, PSI8[k], Y_top) for k in range(8)]
        cen = cam.P(0.0, 0.0, Y_top)
        inner = [(cen[0] + (px - cen[0]) * 0.86, cen[1] + (py - cen[1]) * 0.86) for (px, py) in outer]
        pa = path_of(outer)
        pa.addPath(path_of(inner))
        pa.setFillType(skia.PathFillType.kEvenOdd)
        c.drawPath(pa, pf(S.col("#A8503A", "#F2A074", 0.7)))
        c.drawPath(pa, ps(INK, 1.0, 140))
    jt = min(int(n_done), NC)
    fr_p = clamp(n_done - jt) if jt < NC else 0.0
    for kc in range(8):
        cw = math.cos((PSI8[kc] - a) * D2R)
        if cw < -0.12:
            continue
        pts = [(SX[j][kc], SY[j][kc]) for j in range(0, jt + 1)]
        if jt < NC:
            pts.append((SX[jt][kc] + (SX[jt + 1][kc] - SX[jt][kc]) * fr_p, SY[jt][kc] + (SY[jt + 1][kc] - SY[jt][kc]) * fr_p))
        if len(pts) < 2:
            continue
        w_ = (3.0 + 9.0 * max(0.0, cw)) * z_
        pa = path_of(pts, False)
        lit_c = lit_of(PSI8[kc], a, az_sun)
        c.drawPath(pa, ps(INK, w_ + 2.4, 130, True))
        c.drawPath(pa, ps(S.col("#CFC6AE", "#FFF8E4", lit_c + 0.2), w_, 255, True))
    draw_lantern(c, S, cam, lp, az_sun)
    if scaf:
        draw_deck_front(c, S, cam, Yp, R_in, R_out, sc_al, night, t)
        draw_crew(f, S, cam, Yp, Rm, t, sc_al)
        draw_crane(f, S, cam, Yp, Rm, t, sc_al, night)
        for qd in range(7):
            ph = (t * 0.16 + qd / 7.0) % 1.0
            x, y = cam.R(Rm, -80 + qd * 27, Yp)
            FA._puff(c, x + math.sin(ph * 4 + qd) * 14 * z_, y - 20 * z_ - ph * 120 * z_, (7 + 26 * ph) * z_, 0.16 * (1 - ph) * sc_al, "#D8C8A8")
    # ön sıra evler, piazza yaşamı, kireç ocağı + duman
    c.save()
    c.translate(W / 2, gy)
    c.scale(z_, z_)
    c.translate(-W / 2, 0)
    S.town.draw(c, "near")
    c.drawRect(skia.Rect.MakeLTRB(-S.town.EX, NEAR_Y, W + S.town.EX, 700), pf(S.tc("#A09068")))
    kx = 190
    ky = 62.0
    c.drawRect(skia.Rect.MakeLTRB(kx - 46, ky - 66, kx + 46, ky), pf(S.tc("#8A6A48")))
    c.drawRect(skia.Rect.MakeLTRB(kx - 46, ky - 66, kx + 46, ky), ps(INK, 1.4, 190))
    c.drawOval(skia.Rect.MakeLTRB(kx - 15, ky - 40, kx + 15, ky - 2), pf("#FF9A3A", 235))
    glow(c, kx, ky - 22, 90, "#FF8A2A", 0.35 + 0.1 * math.sin(t * 8.0))
    for q in range(8):
        ph = (t * 0.13 + q / 8.0) % 1.0
        FA._puff(c, kx + 8 + math.sin(ph * 5 + q) * 18 * ph + ph * 44 * (1 + 0.6 * math.sin(t * 0.3)), ky - 74 - ph * 280, 10 + 38 * ph, 0.36 * (1 - ph), "#9C968A" if not night else "#6A7A9A")
    FA.set_scale_hint(z_)
    for i, (xa, xb, v, sd, t0, prop) in enumerate(((W / 2 - 420, W / 2 + 430, 34.0, 41, 0.0, "basket"), (W / 2 + 440, W / 2 - 150, 30.0, 42, 3.0, "sack"), (W / 2 - 460, W / 2 - 180, 28.0, 43, 6.0, "basket"))):
        shuttle(f, ("halk", "denizci", "halk")[i], t, xa, xb, lambda x, _i=i: 92.0 + 8 * math.sin(x * 0.01 + _i), 50.0, v, pause=3.0, seed=sd, t0=t0, prop_ab=prop, prop_ba=None)
    FA.set_scale_hint(1.0)
    c.restore()
    grade(c, p, night)


# ═════════════════════════════ UFFIZI ═════════════════════════════
HWC = 6.5                      # avlu yarı genişliği (m)
Z_END = 130.0                  # kanat sonu (Arno revağı)
BAY = 4.4
NB = int(Z_END / BAY)          # kanat başına bay sayısı
LVLS = [(0.0, 7.2, "portico"), (7.2, 11.0, "mezz"), (11.0, 18.6, "nobile"), (18.6, 23.4, "attic")]
HFIN = 23.4
STONE_RAW = "#B09A74"
PLASTER = "#E4D4AA"
SERENA = "#ADA898"


class Persp:
    """Tek noktalı perspektif: X yanal, Y yukarı, Z derinlik; kamera (0, camy, zc), odak f, ufuk hz."""
    __slots__ = ("f", "hz", "camy", "zc")

    def __init__(self, f, hz, camy, zc):
        self.f, self.hz, self.camy, self.zc = f, hz, camy, zc

    def pt(self, X, Y, Z):
        s = self.f / max(0.05, Z - self.zc)
        return W / 2 + X * s, self.hz - (Y - self.camy) * s

    def sc(self, Z):
        return self.f / max(0.05, Z - self.zc)


class UffShot(Shot):
    def __init__(self, tod, seed):
        Shot.__init__(self, tod, seed)
        rs = np.random.RandomState(seed)
        self.noise = rs.rand(2, NB)
        self.side = []                       # [taraf][sıra] → ev listesi
        for sd in (-1, 1):
            rows = []
            for r_ in (0, 1):
                z = -10.0 - 3.0 * r_
                row = []
                while z < Z_END + 30:
                    w = rs.uniform(5.5, 9.0)
                    hh = rs.uniform(8.0, 15.5) if r_ == 0 else rs.uniform(13.0, 24.0)
                    row.append((z, w, hh, CT.WALLS[rs.randint(len(CT.WALLS))], CT.ROOFS[rs.randint(len(CT.ROOFS))]))
                    z += w + rs.uniform(0.0, 0.8)
                rows.append(row)
            self.side.append(rows)
        self.piles = [(rs.uniform(-4.3, 4.3), 8.0 + i * 11.5 + rs.uniform(0, 5.0), int(rs.randint(3, 6))) for i in range(11)]
        self.crew = [
            (8.0, 2, "halk", "work", dict(mode="lay", period=1.9, phase=0.1), 51), (12.5, 1, "denizci", "work", dict(mode="strike"), 52),
            (17.0, 3, "halk", "work", dict(mode="lay", period=1.7, phase=0.5, high=0.5), 53), (22.0, 2, "soylu", "point", None, 54),
            (27.5, 4, "tuccar", "talk", dict(energy=0.8), 55), (33.0, 1, "halk", "work", dict(mode="lay", period=2.0, phase=0.3), 56),
            (40.0, 3, "halk", "work", dict(mode="strike", phase=0.4), 57), (47.0, 2, "halk", "talk", dict(energy=0.7), 58),
            (56.0, 4, "denizci", "work", dict(mode="lay", period=1.8, phase=0.7), 59), (65.0, 3, "halk", "work", dict(mode="strike", phase=0.2), 60),
            (74.0, 2, "halk", "work", dict(mode="lay", period=2.1, phase=0.4), 67), (10.0, 0, "halk", "work", dict(mode="strike", phase=0.6), 68),
            (36.0, 0, "denizci", "work", dict(mode="strike", phase=0.1), 69)]
        self.carry = [(14.0, -4.4, 4.4, 1.15, "sack", "halk", 61), (19.5, 4.4, -4.4, 1.05, "basket", "cocuk", 62), (25.0, -4.3, 4.3, 1.20, "basket", "denizci", 63),
                      (33.0, 4.3, -4.3, 1.10, "sack", "halk", 64), (45.0, -4.2, 4.2, 1.18, "basket", "halk", 65), (60.0, 4.2, -4.2, 1.12, "sack", "denizci", 66)]
        self.stones = [(rs.uniform(-6.3, 6.3), rs.uniform(-12.0, 70.0), rs.uniform(0.05, 0.16)) for _ in range(170)]
        self.timbers = [(rs.uniform(-5.2, 5.2), 4.0 + i * 15.0 + rs.uniform(0, 6.0), rs.uniform(3.5, 7.0)) for i in range(5)]


def wall_heights(p, side, S):
    """Bay başına duvar yüksekliği (m). side: 0 = sol, 1 = sağ. Uzak uç biraz geride; bay başına küçük sapma."""
    base = clamp((p - 0.03) / 0.80)
    i = np.arange(NB)
    g = np.clip(base * 1.16 - 0.16 * (i / NB) + 0.045 * (S.noise[side] - 0.5) * smooth(min(base * 4, 1.0)) - 0.03 * (1 - side), 0.0, 1.0)
    return g * HFIN


def draw_wing(c, S, P, side, Hs, plast, lit):
    """Bir kanat cephesi (side=+1 sağ, −1 sol): ham duvar (adım adım) → sıva + pietra serena + açıklıklar (çerçeve, alınlık, denizlik, kayıt çıtaları) + silme gölgeleri."""
    X = side * HWC
    zc = P.zc
    zb_ = [b * BAY for b in range(NB + 1)]
    b0 = max(0, int(zc / BAY) - 1)
    bays = [b for b in range(b0, NB) if (b + 1) * BAY > zc + 0.7 and Hs[b] > 0.02]
    if not bays:
        return
    raw = S.col("#7C6A4C", STONE_RAW, lit)
    pla = S.col("#BDB08A", PLASTER, lit)
    ser = S.col("#807A6C", SERENA, lit)
    dark = S.tc("#33281D")
    runs, cur = [], [bays[0]]
    for b in bays[1:]:
        if b == cur[-1] + 1:
            cur.append(b)
        else:
            runs.append(cur)
            cur = [b]
    runs.append(cur)

    def zclip(b):
        return max(zb_[b], zc + 0.7), zb_[b + 1]

    def quad(path, X_, ya, yb, za, zb):
        path.moveTo(*P.pt(X_, ya, za))
        path.lineTo(*P.pt(X_, ya, zb))
        path.lineTo(*P.pt(X_, yb, zb))
        path.lineTo(*P.pt(X_, yb, za))
        path.close()

    def arch(path, X_, y_spring, y_base, za, zb, n):
        path.moveTo(*P.pt(X_, y_base, za))
        path.lineTo(*P.pt(X_, y_spring, za))
        rz = (zb - za) / 2
        for i in range(1, n):
            th = math.pi * i / n
            path.lineTo(*P.pt(X_, y_spring + rz * math.sin(th), (za + zb) / 2 - rz * math.cos(th)))
        path.lineTo(*P.pt(X_, y_spring, zb))
        path.lineTo(*P.pt(X_, y_base, zb))
        path.close()
    for run in runs:
        base_pts, top_pts = [], []
        for b in run:
            za, zb = zclip(b)
            h = float(Hs[b])
            base_pts += [P.pt(X, 0.0, za), P.pt(X, 0.0, zb)]
            top_pts += [P.pt(X, h, za), P.pt(X, h, zb)]
        poly(c, [base_pts[0], base_pts[-1]] + top_pts[::-1], pf(raw))
    ln = skia.Path()
    for b in bays:
        za, zb = zclip(b)
        if zb - zc > 60:
            continue
        h, ph_ = float(Hs[b]), float(plast[b])
        yy = math.ceil(max(0.0, ph_) / 0.5) * 0.5
        n = 0
        while yy < h and n < 9:
            ln.moveTo(*P.pt(X, yy, za))
            ln.lineTo(*P.pt(X, yy, zb))
            yy += 0.5
            n += 1
    c.drawPath(ln, ps("#3A2A18", 0.9, 90))
    openings, frames, peds, mull = skia.Path(), skia.Path(), skia.Path(), skia.Path()
    for (y0, y1, nm) in LVLS:
        for run in runs:
            base_pts, top_pts = [], []
            for b in run:
                if plast[b] <= y0 + 0.05:
                    continue
                za, zb = zclip(b)
                top = min(float(plast[b]), y1)
                base_pts += [P.pt(X, y0, za), P.pt(X, y0, zb)]
                top_pts += [P.pt(X, top, za), P.pt(X, top, zb)]
            if len(base_pts) >= 2:
                poly(c, [base_pts[0], base_pts[-1]] + top_pts[::-1], pf(ser if nm == "portico" else pla))
        for b in bays:
            d0 = zb_[b] - zc
            if d0 > 85:
                continue
            h, pl = float(Hs[b]), float(plast[b])
            zA, zB = zb_[b] + BAY * 0.22, zb_[b] + BAY * 0.78
            if zA < zc + 0.7:
                continue
            small = d0 > 38
            na = 14 if d0 < 16 else (9 if d0 < 40 else 5)
            if nm == "portico" and h > 6.3:
                arch(openings, X, 5.2, 0.0, zA, zB, na)
                if not small:
                    arch(frames, X, 5.2 + 0.0, 0.0, zA - 0.28, zB + 0.28, na)
            elif nm == "mezz" and h > 10.0 and pl > 10.3:
                za2, zb2 = zb_[b] + BAY * 0.38, zb_[b] + BAY * 0.62
                ya, yb = y0 + 0.9, y1 - 0.9
                quad(openings, X, ya, yb, za2, zb2)
                if not small:
                    quad(frames, X, ya - 0.18, yb + 0.18, za2 - 0.16, zb2 + 0.16)
            elif nm == "nobile" and h > 17.0:
                za2, zb2 = zb_[b] + BAY * 0.30, zb_[b] + BAY * 0.70
                ya, yb = y0 + 1.5, y1 - 1.6
                if pl > yb + 0.9:
                    quad(openings, X, ya, yb, za2, zb2)
                    if not small:
                        zz0, zz1 = za2 - BAY * 0.05, zb2 + BAY * 0.05
                        quad(frames, X, ya - 0.45, yb + 0.20, zz0, zz1)            # çerçeve + denizlik
                        if b % 2 == 0:                                              # üçgen alınlık
                            peds.moveTo(*P.pt(X, yb + 0.20, zz0 - 0.12))
                            peds.lineTo(*P.pt(X, yb + 0.20, zz1 + 0.12))
                            peds.lineTo(*P.pt(X, yb + 1.15, (zz0 + zz1) / 2))
                        else:                                                       # kemerli (segmental) alınlık
                            peds.moveTo(*P.pt(X, yb + 0.20, zz0 - 0.12))
                            for i in range(0, 7):
                                u = i / 6.0
                                peds.lineTo(*P.pt(X, yb + 0.20 + 0.75 * math.sin(math.pi * u), zz0 - 0.12 + (zz1 - zz0 + 0.24) * u))
                        peds.close()
                        if d0 < 30:
                            mull.moveTo(*P.pt(X, ya, (za2 + zb2) / 2))
                            mull.lineTo(*P.pt(X, yb, (za2 + zb2) / 2))
                            mull.moveTo(*P.pt(X, ya + (yb - ya) * 0.62, za2))
                            mull.lineTo(*P.pt(X, ya + (yb - ya) * 0.62, zb2))
            elif nm == "attic" and h > 22.4 and pl > 21.6:
                arch(openings, X, y1 - 2.4, y0 + 0.5, zA, zB, na)
    sh = skia.Path()
    for (yy, th_) in ((7.2, 0.45), (11.0, 0.40), (18.6, 0.50), (23.0, 0.80)):
        for run in runs:
            pa_, pb_, ps_ = [], [], []
            for b in run:
                if plast[b] < yy + th_ * 0.5:
                    continue
                za, zb = zclip(b)
                pa_ += [P.pt(X, yy - th_ * 0.5, za), P.pt(X, yy - th_ * 0.5, zb)]
                pb_ += [P.pt(X, yy + th_ * 0.5, za), P.pt(X, yy + th_ * 0.5, zb)]
                ps_ += [P.pt(X, yy - th_ * 0.5 - 0.55, za), P.pt(X, yy - th_ * 0.5 - 0.55, zb)]
            if len(pa_) >= 2:
                sh.moveTo(*pa_[0])
                for q in pa_[1:]:
                    sh.lineTo(*q)
                for q in ps_[::-1]:
                    sh.lineTo(*q)
                sh.close()
    c.drawPath(sh, pf("#1A0E06", 40))
    c.drawPath(frames, pf(ser))
    c.drawPath(frames, ps(INK, 0.9, 120))
    c.drawPath(openings, pf(dark, 238))
    c.drawPath(openings, ps(INK, 0.8, 110))
    c.drawPath(peds, pf(ser))
    c.drawPath(peds, ps(INK, 0.9, 150))
    c.drawPath(mull, ps(ser, 1.6, 230))
    for (yy, th_) in ((7.2, 0.45), (11.0, 0.40), (18.6, 0.50), (23.0, 0.80)):
        for run in runs:
            pa_, pb_ = [], []
            for b in run:
                if plast[b] < yy + th_ * 0.5:
                    continue
                za, zb = zclip(b)
                pa_ += [P.pt(X, yy - th_ * 0.5, za), P.pt(X, yy - th_ * 0.5, zb)]
                pb_ += [P.pt(X, yy + th_ * 0.5, za), P.pt(X, yy + th_ * 0.5, zb)]
            if len(pa_) >= 2:
                poly(c, [pa_[0], pa_[-1]] + pb_[::-1], pf(ser))
    pil = skia.Path()
    for b in bays:
        zz = zb_[b]
        if Hs[b] < 6.0 or zz < zc + 0.8 or zz - zc > 85:
            continue
        hh = min(float(plast[b]), 7.2)
        if hh < 1.0:
            continue
        pil.moveTo(*P.pt(X, 0.0, zz))
        pil.lineTo(*P.pt(X, hh, zz))
    c.drawPath(pil, ps(S.col("#6E6A5E", "#BDB8A6", lit), 3.0, 230))
    for run in runs:
        tp = []
        for b in run:
            za, zb = zclip(b)
            h = float(Hs[b])
            tp += [P.pt(X, h, za), P.pt(X, h, zb)]
        c.drawPath(path_of(tp, False), ps(INK, 1.6, 200, True))


def draw_scaffold(c, S, P, side, Hs, al):
    wood = S.tc("#7A5230")
    dark = "#3A2410"
    hmax = float(np.max(Hs))
    if hmax < 0.6 or al <= 0.01:
        return
    X, Xw = side * (HWC - 1.4), side * (HWC - 0.1)
    zc = P.zc
    top = hmax + 3.0
    za = max(zc + 1.0, 2.0)
    zfar = min(Z_END, zc + 90)
    # tabla (4 m aralıkla, yükseklik duvarı geçince)
    lv = 1
    while 4.0 * lv + 0.3 < hmax + 0.5:
        y = 4.0 * lv + 0.3
        q = [P.pt(Xw, y, za), P.pt(Xw, y, zfar), P.pt(X, y, zfar), P.pt(X, y, za)]
        poly(c, q, pf(S.tc("#8A6238"), int(225 * al)))
        poly(c, q, ps(INK, 0.9, int(130 * al)))
        lv += 1
    for b in range(0, NB, 2):
        zz = b * BAY + 2.0
        if zz < zc + 1.0 or zz - zc > 90:
            continue
        hh = min(top, float(Hs[min(NB - 1, b)]) + 3.0)
        x0, y0 = P.pt(X, 0.0, zz)
        x1, y1 = P.pt(X, hh, zz)
        w_ = max(1.2, 0.20 * P.sc(zz))
        c.drawLine(x0, y0, x1, y1, ps(dark, w_ + 1.6, int(220 * al), True))
        c.drawLine(x0, y0, x1, y1, ps(wood, w_, int(240 * al), True))
        xa, ya = P.pt(Xw, min(hh, 3.0), zz)
        c.drawLine(x0, P.pt(X, min(hh, 4.0), zz)[1], xa, ya, ps(dark, max(1.0, w_ * 0.6), int(160 * al)))
    y = 4.0
    while y < top:
        a_, b_ = P.pt(X, y, za), P.pt(X, y, zfar)
        wl = max(1.4, 0.15 * P.sc(za + 12))
        c.drawLine(a_[0], a_[1], b_[0], b_[1], ps(dark, wl + 1.2, int(205 * al)))
        c.drawLine(a_[0], a_[1], b_[0], b_[1], ps(wood, wl, int(235 * al)))
        y += 4.0
    yd = hmax + 0.4
    Xi = side * (HWC - 1.0)
    q = [P.pt(Xw, yd, za), P.pt(Xw, yd, zfar), P.pt(Xi, yd, zfar), P.pt(Xi, yd, za)]
    poly(c, q, pf(S.tc("#8A6238"), int(205 * al)))
    poly(c, q, ps(INK, 1.0, int(150 * al)))


def deck_y(level):
    return 0.0 if level == 0 else 4.0 * level + 0.3


def draw_wing_crew(f, S, P, side, Hs, t, al):
    """İskele katlarında (zemin, 4, 8, 12, 16 m) çalışan işçiler: duvar yüksekliği kata erişince belirir (alfa); mala/çekiç/konuşma/işaret."""
    X = side * (HWC - 0.75)
    zc = P.zc
    for (Z0, lvl, kind, act, kw, sd0) in S.crew:
        Z = Z0 + (2.5 if side < 0 else 0.0)
        if Z < zc + 3.2 or Z - zc > 80:
            continue
        h = float(Hs[min(NB - 1, int(Z / BAY))])
        dy_ = deck_y(lvl)
        if h < dy_ + 1.0 or h < 0.8:
            continue
        x, y = P.pt(X, dy_, Z)
        hh = 1.72 * P.sc(Z)
        if y - hh > BH or y < -40:
            continue
        FA.set_scale_hint(max(0.2, hh / 56.0))
        dr = 1 if side > 0 else -1
        sd = sd0 + (7 if side < 0 else 0)
        a_ = al * smooth((h - dy_ - 0.6) / 1.4)
        if act == "point":
            FA.actor(f, kind, x, y, hh, t % 9.0, action="point", dir=dr, seed=sd, phase=0.2, alpha=a_, t0=1.3, dur=3.2, target=(0.6, -0.75))
        else:
            ph, kw2 = _act_kw(kw, sd)
            FA.actor(f, kind, x, y, hh, t, action=act, dir=dr, seed=sd, phase=ph, alpha=a_, **kw2)
    FA.set_scale_hint(1.0)


def _uffizi_end(c, S, P):
    Z = Z_END
    xl, yl = P.pt(-HWC, 0.0, Z)
    xr, _ = P.pt(HWC, 0.0, Z)
    yt = P.pt(0.0, 11.5, Z)[1]
    c.drawRect(skia.Rect.MakeLTRB(xl, yt, xr, yl), pf(S.tc("#D8C8A0")))
    n = 3
    for i in range(n):
        x0 = xl + (xr - xl) * (i + 0.15) / n
        x1 = xl + (xr - xl) * (i + 0.85) / n
        ya = yt + (yl - yt) * 0.42
        pa = skia.Path()
        pa.moveTo(x0, yl)
        pa.lineTo(x0, ya)
        pa.arcTo(skia.Rect.MakeLTRB(x0, ya - (x1 - x0) / 2, x1, ya + (x1 - x0) / 2), 180, 180, False)
        pa.lineTo(x1, yl)
        pa.close()
        c.drawPath(pa, pf(S.tc("#9CB8C0")))
    c.drawRect(skia.Rect.MakeLTRB(xl, yt, xr, yl), ps(INK, 1.2, 150))


def _uffizi_crane(f, S, P, t, Hl, Hr, sc_al, night):
    """Avlu vinci (sol kanada yakın): A-çerçeve direk duvarla birlikte uzar; bom duvarın üzerine uzanır; yük duvar boyunca çıkar; çarkta yürüyen adam."""
    c = f.c
    Z = 19.0
    if Z - P.zc < 2.5:
        return
    X = -3.9
    s = P.sc(Z)
    hmax = float(max(np.max(Hl), np.max(Hr)))
    mast_h = clamp(hmax + 5.5, 8.0, 26.0)
    wood = S.tc("#7A5230")
    dark = "#3A2410"
    bx, by = P.pt(X, 0.0, Z)
    ax, ay = P.pt(X - 0.3, mast_h, Z)
    for dx in (-1.1, 1.1):
        c.drawLine(bx + dx * s, by + 2, ax + dx * 0.12 * s, ay, ps(dark, max(2.0, 0.28 * s), 235, True))
        c.drawLine(bx + dx * s, by + 2, ax + dx * 0.12 * s, ay, ps(wood, max(1.4, 0.17 * s), 245, True))
    for yy in (mast_h * 0.25, mast_h * 0.55):
        xa, ya_ = P.pt(X, yy, Z)
        yb_ = P.pt(X, yy + mast_h * 0.18, Z)[1]
        c.drawLine(xa - 1.05 * s, ya_, xa + 1.05 * s, yb_, ps(wood, max(1.0, 0.10 * s), 235))
        c.drawLine(xa + 1.05 * s, ya_, xa - 1.05 * s, yb_, ps(wood, max(1.0, 0.10 * s), 235))
    tx, ty = P.pt(X - 3.8, mast_h - 0.8, Z)
    c.drawLine(ax, ay, tx, ty, ps(dark, max(2.0, 0.28 * s), 235, True))
    c.drawLine(ax, ay, tx, ty, ps(wood, max(1.4, 0.17 * s), 245, True))
    k, sgn = hoist_cycle(t, 12.0, 1.0)
    k2, _ = hoist_cycle(t + 0.05, 12.0, 1.0)
    omega = (k2 - k) / 0.05 * 140.0
    R = 2.0 * s
    wx, wy = P.pt(X + 2.6, 2.3, Z)
    treadwheel(f, wx, wy, R, k * 140.0, omega, t, night, 1.0)
    seg(c, wx + R * 0.1, wy - R * 0.1, ax + 0.2 * s, ay + 0.2 * s, ps("#6A5A3A", max(1.0, 0.07 * s), 215))
    ly = lerp(by - 0.6 * s, ty + 1.8 * s, k)
    sw = math.sin(t * 1.3) * 0.12 * s * min(1.0, k * 2)
    seg(c, tx, ty, tx + sw, ly, ps("#6A5A3A", max(1.0, 0.07 * s), 235))
    load_block(c, tx + sw, ly, 1.4 * s, "stone", 1.0)


def draw_uffizi(f, cx, p, t, night, S, u_cam):
    c = f.c
    az, el, sun_col = sun_state(p)
    zc = lerp(-13.0, 7.5, u_cam)
    camy = lerp(1.9, 8.6, smooth(u_cam))
    foc = lerp(560.0, 640.0, u_cam)
    hz = lerp(430.0, 470.0, u_cam)
    P = Persp(foc, hz, camy, zc)
    T = S.T
    draw_sky(c, p, night, hz=hz + 30.0)
    if night:
        draw_stars(c, t)
        draw_sun(c, W * 0.30, 130, sun_col, True)
    else:
        sx = W / 2 + az / 70.0 * 760.0
        sy = lerp(hz - 40.0, 120.0, el)
        draw_sun(c, sx, sy, sun_col, False, 1.0)
    draw_clouds(c, t, night, speed=1.7, seed=8)
    FA.atmo_birds(c, t, 5, 1.0, 0, W, 150, 330, 22.0, night, 5, 1.0)
    c.save()
    c.translate(0, hz + 14.0)
    for nm, base, amp, sc, ph, col in (("u1", -58, 26, 520, 0.0, "#A9BDB6"), ("u2", -30, 30, 360, 2.0, "#93AFA5")):
        c.drawPath(hill_path(nm, base, amp, sc, ph), pf(T(col, 0.3)))
    c.restore()
    # yer düzlemi (avlu dışı) + Arno şeridi (uç duvarın ötesi) + karşı kıyı silueti
    c.drawRect(skia.Rect.MakeLTRB(0, hz + 4.0, W, BH), pf(S.tc("#B4A47E")))
    rv = [P.pt(-420.0, 0.0, Z_END + 8.0), P.pt(420.0, 0.0, Z_END + 8.0), P.pt(420.0, 0.0, Z_END + 70.0), P.pt(-420.0, 0.0, Z_END + 70.0)]
    poly(c, rv, pf(S.tc("#8FB0B0")))
    for k in range(14):
        yy = rv[2][1] + (rv[0][1] - rv[2][1]) * ((k * 0.37) % 1.0)
        xx = (k * 190 + t * (8 + k % 4)) % (W + 100) - 50
        seg(c, xx, yy, xx + 28, yy, ps("#FFFFFF", 1.2, 90))
    rs = np.random.RandomState(2)
    for i in range(46):
        X = -190 + i * 8.3 + rs.uniform(-2, 2)
        hh = rs.uniform(4.0, 13.0)
        a_, b_ = P.pt(X, 0.0, Z_END + 80.0), P.pt(X + 7.5, hh, Z_END + 80.0)
        c.drawRect(skia.Rect.MakeLTRB(a_[0], b_[1], b_[0] + 1, a_[1]), pf(T(CT.WALLS[i % len(CT.WALLS)], 0.45)))
    # yan sokak evleri (iki sıra; kanatların gerisinde) — pencere/kapı dizileri
    dk = S.tc("#33281D")
    for si, sd in enumerate((-1, 1)):
        for r_ in (1, 0):
            X0 = sd * (HWC + 2.6 + 6.0 * r_)
            wins, doors, wfr = skia.Path(), skia.Path(), skia.Path()
            for (z, w, h, wc, rc) in S.side[si][r_]:
                if z + w < zc + 1.0 or z - zc > Z_END + 30:
                    continue
                za, zb = max(z, zc + 1.0), z + w
                q = [P.pt(X0, 0.0, za), P.pt(X0, 0.0, zb), P.pt(X0, h, zb), P.pt(X0, h, za)]
                poly(c, q, pf(T(wc, 0.15 * r_ + 0.1) if night else mix(wc, "#B6C8C8", 0.12 * r_)))
                rr = [P.pt(X0, h, za), P.pt(X0, h, zb), P.pt(X0 + sd * 2.2, h + 2.2, zb), P.pt(X0 + sd * 2.2, h + 2.2, za)]
                poly(c, rr, pf(S.tc(rc)))
                poly(c, q, ps(INK, 1.0, 120))
                if z - zc < 60:
                    nfl = max(1, int((h - 0.5) / 3.3))
                    nwz = max(1, int(w / 2.7))
                    for fl_ in range(nfl):
                        y0_ = 1.0 + fl_ * 3.3 + (1.0 if fl_ == 0 and r_ == 0 else 0.0)
                        for k_ in range(nwz):
                            zc0 = z + (k_ + 0.5) * w / nwz
                            if zc0 - 0.55 < za or zc0 + 0.55 > zb:
                                continue
                            wfr.moveTo(*P.pt(X0, y0_ - 0.18, zc0 - 0.66))
                            wfr.lineTo(*P.pt(X0, y0_ - 0.18, zc0 + 0.66))
                            wfr.lineTo(*P.pt(X0, y0_ + 1.66, zc0 + 0.66))
                            wfr.lineTo(*P.pt(X0, y0_ + 1.66, zc0 - 0.66))
                            wfr.close()
                            wins.moveTo(*P.pt(X0, y0_, zc0 - 0.5))
                            wins.lineTo(*P.pt(X0, y0_, zc0 + 0.5))
                            wins.lineTo(*P.pt(X0, y0_ + 1.5, zc0 + 0.5))
                            wins.lineTo(*P.pt(X0, y0_ + 1.5, zc0 - 0.5))
                            wins.close()
                    if r_ == 0:
                        zc1 = z + w * 0.5
                        if zc1 - 0.7 > za and zc1 + 0.7 < zb:
                            doors.moveTo(*P.pt(X0, 0.0, zc1 - 0.65))
                            doors.lineTo(*P.pt(X0, 0.0, zc1 + 0.65))
                            doors.lineTo(*P.pt(X0, 2.4, zc1 + 0.65))
                            doors.lineTo(*P.pt(X0, 2.4, zc1 - 0.65))
                            doors.close()
            c.drawPath(wfr, pf(S.tc("#EFE6CE"), 200))
            c.drawPath(wins, pf(dk, 215))
            c.drawPath(doors, pf(S.tc("#4A3420"), 235))
    # avlu zemini
    zn = max(zc + 0.6, 0.0)
    poly(c, [P.pt(-HWC, 0.0, zn), P.pt(HWC, 0.0, zn), P.pt(HWC, 0.0, Z_END), P.pt(-HWC, 0.0, Z_END)], pf(S.tc("#BFAE86")))
    gl = skia.Path()
    for i in range(-6, 7):
        gl.moveTo(*P.pt(i * HWC / 6.0, 0.0, zn))
        gl.lineTo(*P.pt(i * HWC / 6.0, 0.0, Z_END))
    zz = math.floor(zn / 2.0) * 2.0 + 2.0
    while zz < Z_END:
        gl.moveTo(*P.pt(-HWC, 0.0, zz))
        gl.lineTo(*P.pt(HWC, 0.0, zz))
        zz += 2.0 if zz - zc < 30 else 6.0
    c.drawPath(gl, ps("#4A3A22", 0.9, 70))
    # zemin dokusu: araba izleri, taş kırıntıları, yatan kereste
    for rx in (-1.15, 1.15):
        pts_l, pts_r = [], []
        z_ = max(zn, -2.0)
        while z_ < min(Z_END, zc + 75):
            xo = rx + 0.35 * math.sin(z_ * 0.05 + rx)
            pts_l.append(P.pt(xo - 0.14, 0.0, z_))
            pts_r.append(P.pt(xo + 0.14, 0.0, z_))
            z_ += 3.0
        if len(pts_l) > 2:
            poly(c, pts_l + pts_r[::-1], pf("#5A4A32", 70))
    st = skia.Path()
    for (X_, Z_, r_) in S.stones:
        if Z_ <= zn + 0.8 or Z_ - zc > 70:
            continue
        x_, y_ = P.pt(X_, 0.0, Z_)
        s_ = P.sc(Z_)
        st.addOval(skia.Rect.MakeXYWH(x_ - r_ * s_, y_ - 0.35 * r_ * s_, 2 * r_ * s_, 0.7 * r_ * s_))
    c.drawPath(st, pf(S.tc("#8A7A58"), 160))
    for (X_, Z_, L_) in S.timbers:
        if Z_ <= zc + 1.2 or Z_ - zc > 85:
            continue
        top = [P.pt(X_ - 0.16, 0.26, Z_), P.pt(X_ + 0.16, 0.26, Z_), P.pt(X_ + 0.16, 0.26, Z_ + L_), P.pt(X_ - 0.16, 0.26, Z_ + L_)]
        sd_ = [P.pt(X_ - 0.16, 0.0, Z_), P.pt(X_ - 0.16, 0.26, Z_), P.pt(X_ - 0.16, 0.26, Z_ + L_), P.pt(X_ - 0.16, 0.0, Z_ + L_)]
        poly(c, sd_, pf(S.tc("#6A4A2C")))
        poly(c, top, pf(S.tc("#8A6238")))
        poly(c, top, ps(INK, 0.8, 130))
    _uffizi_end(c, S, P)
    h0 = max(float(np.max(wall_heights(p, 0, S))), float(np.max(wall_heights(p, 1, S))))
    if h0 < 3.0:
        fa = int(215 * (1.0 - smooth(h0 / 3.0)))
        for side in (-1, 1):
            qf = [P.pt(side * (HWC - 0.7), 0.0, zn), P.pt(side * (HWC + 0.7), 0.0, zn), P.pt(side * (HWC + 0.7), 0.0, Z_END), P.pt(side * (HWC - 0.7), 0.0, Z_END)]
            poly(c, qf, pf(S.tc("#5A4A34"), fa))
            seg(c, *P.pt(side * (HWC - 0.7), 0.0, zn), *P.pt(side * (HWC - 0.7), 0.0, Z_END), ps("#EFE6CE", 1.4, int(fa * 0.6)))
            seg(c, *P.pt(side * (HWC + 0.7), 0.0, zn), *P.pt(side * (HWC + 0.7), 0.0, Z_END), ps("#EFE6CE", 1.4, int(fa * 0.6)))
    fin = smooth((p - 0.80) / 0.12)
    sc_al = 1.0 - fin
    Hs_ = (wall_heights(p, 0, S), wall_heights(p, 1, S))
    for side in (-1, 1):
        si = 0 if side < 0 else 1
        Hs = Hs_[si]
        plast = np.maximum(0.0, Hs - 3.6 * (1.0 - fin))
        lit = clamp(0.5 + 0.5 * math.sin(az * 0.014) * (-side) + 0.1)
        draw_wing(c, S, P, side, Hs, plast, lit)
    for side in (-1, 1):
        draw_scaffold(c, S, P, side, Hs_[0 if side < 0 else 1], sc_al)
    items = []
    for (X, Z, nlay) in S.piles:
        if Z > zc + 1.5:
            items.append((Z, "pile", (X, Z, nlay)))
    for cr in S.carry:
        if cr[0] > zc + 2.5:
            items.append((cr[0], "carry", cr))
    items.append((19.0, "crane", None))
    items.append((24.0, "lime", None))
    items.sort(key=lambda z: -z[0])
    for (Z, kind, data) in items:
        if Z - zc > 95:
            continue
        s = P.sc(Z)
        if kind == "pile":
            X, Z, nl = data
            x, y = P.pt(X, 0.0, Z)
            for qq in range(nl):
                for kk in range(nl - qq):
                    rc = skia.Rect.MakeXYWH(x - (nl - qq) * 0.7 * s + kk * 1.4 * s, y - (qq + 1) * 0.7 * s, 1.35 * s, 0.68 * s)
                    c.drawRect(rc, pf(S.tc(("#B8A47A", "#A8946A", "#C9B88C")[(qq + kk) % 3])))
                    c.drawRect(rc, ps(INK, max(0.7, 0.05 * s), 150))
        elif kind == "lime":
            x, y = P.pt(0.9, 0.0, Z)
            ov = skia.Rect.MakeXYWH(x - 1.8 * s, y - 0.5 * s, 3.6 * s, 1.0 * s)
            c.drawOval(ov, pf(S.tc("#E8E2D0")))
            c.drawOval(ov, ps(INK, max(0.8, 0.05 * s), 140))
        elif kind == "carry":
            (Z0, xa_, xb_, w_, prop, kd, sd) = data
            hh = 1.72 * s
            FA.set_scale_hint(max(0.2, hh / 56.0))
            xs0, ys0 = P.pt(xa_, 0.0, Z0)
            xs1, _ = P.pt(xb_, 0.0, Z0)
            shuttle(f, kd, t, xs0, xs1, lambda x, _y=ys0: _y, hh * (0.8 if kd == "cocuk" else 1.0), w_ / 1.72 * hh * 0.62, pause=2.6, seed=sd, t0=sd * 1.7, prop_ab=prop, prop_ba=None)
            FA.set_scale_hint(1.0)
        elif kind == "crane":
            _uffizi_crane(f, S, P, t, Hs_[0], Hs_[1], sc_al, night)
    for side in (-1, 1):
        draw_wing_crew(f, S, P, side, Hs_[0 if side < 0 else 1], t, sc_al)
    for side in (-1, 1):
        Hs = Hs_[0 if side < 0 else 1]
        for q in range(6):
            ph = (t * 0.18 + q / 6.0 + side * 0.11) % 1.0
            Z = max(zc + 6.0, 6.0) + q * 13.0 + 3.0 * math.sin(q + t * 0.2)
            h = float(Hs[min(NB - 1, int(Z / BAY))])
            if h < 0.8 or Z - zc > 85:
                continue
            x, y = P.pt(side * (HWC - 1.4 + 2.5 * ph), h + 0.8 + ph * 3.2, Z)
            FA._puff(c, x, y, (0.7 + 2.6 * ph) * P.sc(Z), 0.20 * (1 - ph) * sc_al, "#D8C8A8")
    if night:
        for side in (-1, 1):
            for q in range(6):
                Z = max(zc + 5.0, 5.0) + q * 12.0
                if Z - zc > 80:
                    continue
                x, y = P.pt(side * (HWC - 1.2), 3.6, Z)
                fl = 1.0 + 0.12 * math.sin(t * 8.0 + q * 2.0 + side)
                glow(c, x, y, 2.6 * P.sc(Z) * fl, "#FFB04A", 0.6)
    vx, vy = P.pt(0.0, camy * 0.35, Z_END)
    glow(c, vx, vy, 70.0 + 160.0 * (1 - u_cam), sun_col if not night else "#9CB4E8", 0.30 + (0.0 if night else 0.25 * el))
    grade(c, p, night)


# ═════════════════════════════ çekim türü ═════════════════════════════
_SCENES = {}


@ckind("build")
def k_build(cx, build="dome", p=None, orbit=10.0, tod=None, kick=None, caption=None, at=0.0, seed=3, frame=True, **_):
    """Zaman atlamalı yapım. build: dome | uffizi. p=(çapa_başlangıç, çapa_bitiş): ilerleme 0→1 (ease_io; çapa = saniye | ("c7s5","sözcük",−0.1));
    p=None → tüm çekim; p tek sayı → sabit ilerleme. orbit: kubbede kamera yörüngesi (°, ≤12). tod: day | night (yoksa moda göre). Güneş yayı, gökyüzü rengi, yüz parlaklığı ilerlemeyle akar;
    toz/duman/kuş/vinç/çark her an çalışır. kick/caption: metin. cam/link/longtake/montage kabul edilir ve yok sayılır."""
    f = cx.f
    c = f.c
    tod = tod or ("night" if not TH.day else "day")
    night = tod == "night"
    dur = max(cx.dur, 1e-3)
    if p is None:
        pr = ease_io(clamp(cx.t / dur))
    elif isinstance(p, (int, float)):
        pr = clamp(float(p))
    else:
        try:
            ta, tb = cx.at(p[0]), cx.at(p[1])
        except Exception:
            ta, tb = float(p[0]), float(p[1])
        pr = ease_io(clamp((cx.t - ta) / max(1e-6, tb - ta)))
    band = (150, BH)
    a = cx.amt(at, 0.9) if at else 1.0
    cam0 = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    for (y0, y1) in ((0, band[0] + 2), (band[0] + band[1] - 2, H)):
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(0, y0, W, y1))
        CM.bgfill(f, cx, seed=seed, cam=cam0, dress=None)
        c.restore()
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, band[0], W, band[0] + band[1]))
    c.translate(0, band[0])
    key = (build, tod, seed)
    S = _SCENES.get(key)
    if S is None:
        S = _SCENES[key] = Shot(tod, seed, town=True) if build == "dome" else UffShot(tod, seed)
    if build == "dome":
        draw_dome(f, cx, pr, cx.t, night, S, (clamp(cx.t / dur) - 0.5) * min(12.0, abs(orbit)))
    else:
        draw_uffizi(f, cx, pr, cx.t, night, S, pr)
    c.restore()
    FA.set_scale_hint(1.0)
    if frame:
        for yy in (band[0] - 40, band[0] + band[1]):
            FA.vine_band(f, yy, a)
            c.drawLine(-40, yy + (40 if yy < band[0] else 0), W + 40, yy + (40 if yy < band[0] else 0), f.paint(TH.gold, style="stroke", sw=2.6, alpha=0.9 * a))
    if kick:
        CM.kick(f, kick, W / 2, 104, alpha=cx.amt(at + 0.4, 0.8), size=34, track=14)
    if caption:
        wd = sk.text_width(caption, "cap_i", 44) + 100
        cyy = band[0] + band[1] - 70
        CM.tablet(f, W / 2 - wd / 2, cyy - 36, wd, 76, alpha=cx.amt(at + 0.8, 0.7), corner=10)
        CM.ink(f, caption, W / 2, cyy + 14, face="cap_i", size=44, color=TH.fg, align="c", alpha=cx.amt(at + 0.8, 0.7), emboss=False)
    if night:
        CM.finish(f, cx, motes_n=18, light=CM.candle_light(cx.t, seed, base=(W * 0.5, H * 0.46), r=1500.0, sway=10.0))
    else:
        CM.finish(f, cx, motes_n=22)
