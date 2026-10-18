"""cilt_figs — Medici cildi: Quattrocento boyalı FRİZ figürleri (Gozzoli'nin Medici Şapeli "Magi Alayı"ndan esinli yatay alay).

Silüet değil: düz ama pigment kenarlı boyalı figürler — mürekkep dış çizgi, kenarda pigment birikimi (koyu iç kenar + açık vurgu), kumaş desenleri
(brokar baklava/nokta/çizgi/zambak), altın filet (sgraffito altın çizgiler), parti-colored çorap, mazzocchio şapkalar, at örtüleri.
Geometri `figs_kit` / `figs_parts` / `figs_horse` yardımcılarından (profil baş, şapka parçaları, at bacağı/gövde/yele) alınır; boyama bu modülde.
Her figür tek bir önbellekli sprite (img, ox, oy); kare başına yalnız dönüşüm.
"""
import functools
import math

import numpy as np
import skia

import cilt_medici as CM
import figs_horse as FH
import figs_kit as K
import figs_parts as FP
import sk
from figs_kit import Fig, K as KC, bar, ell, lens, limb, place, poly, shoe, sp
from sk import C, mix

PIG = CM.PIG
INK = "#1E150C"
LIGHT = "#F3E9CC"


# ───────────────────────────── desen karoları ─────────────────────────────
@functools.lru_cache(maxsize=64)
def pattern_tile(kind, color, bg=None, size=34):
    """Kumaş deseni için 'size'×'size' tekrarlayan karo (skia.Image)."""
    fr = sk.Frame(size, size)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    pa = skia.Paint(AntiAlias=True, Color=C(color, 235))
    ps = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=C(color, 235))
    s = size
    if kind == "diamond":
        for (x, y) in ((s / 2, s / 2), (0, 0), (s, 0), (0, s), (s, s)):
            c.drawPath(sk.poly_path([(x, y - s * 0.30), (x + s * 0.22, y), (x, y + s * 0.30), (x - s * 0.22, y)]), pa)
    elif kind == "dots":
        for (x, y) in ((s * 0.25, s * 0.25), (s * 0.75, s * 0.75)):
            c.drawCircle(x, y, s * 0.10, pa)
            c.drawCircle(x, y, s * 0.20, ps)
    elif kind == "quatrefoil":
        for (x, y) in ((s / 2, s / 2),):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                c.drawCircle(x + dx * s * 0.14, y + dy * s * 0.14, s * 0.11, pa)
        for (x, y) in ((0, 0), (s, 0), (0, s), (s, s)):
            c.drawCircle(x, y, s * 0.12, ps)
    elif kind == "stripe":
        c.drawRect(skia.Rect.MakeXYWH(0, 0, s * 0.30, s), pa)
    elif kind == "fleur":
        for (x, y) in ((s / 2, s / 2),):
            c.drawPath(sk.smooth_path([(x, y - s * 0.34), (x + s * 0.10, y - s * 0.10), (x + s * 0.06, y + s * 0.18), (x, y + s * 0.30), (x - s * 0.06, y + s * 0.18), (x - s * 0.10, y - s * 0.10)], True, 0.5), pa)
            c.drawCircle(x - s * 0.18, y - s * 0.02, s * 0.07, pa)
            c.drawCircle(x + s * 0.18, y - s * 0.02, s * 0.07, pa)
        c.drawCircle(0, 0, s * 0.06, pa); c.drawCircle(s, 0, s * 0.06, pa); c.drawCircle(0, s, s * 0.06, pa); c.drawCircle(s, s, s * 0.06, pa)
    elif kind == "pomegranate":
        for (x, y) in ((s / 2, s * 0.55),):
            c.drawCircle(x, y, s * 0.20, pa)
            c.drawPath(sk.poly_path([(x - s * 0.08, y - s * 0.20), (x, y - s * 0.30), (x + s * 0.08, y - s * 0.20)]), pa)
            c.drawCircle(x, y, s * 0.30, ps)
        c.drawCircle(0, 0, s * 0.08, pa); c.drawCircle(s, 0, s * 0.08, pa); c.drawCircle(0, s, s * 0.08, pa); c.drawCircle(s, s, s * 0.08, pa)
    return fr.surf.makeImageSnapshot()


def pattern_shader(kind, color, scale=1.0, rot=0.0):
    tile = pattern_tile(kind, color)
    m = skia.Matrix()
    m.setScale(scale, scale)
    if rot:
        m.postRotate(rot)
    return tile.makeShader(skia.TileMode.kRepeat, skia.TileMode.kRepeat, skia.SamplingOptions(skia.FilterMode.kLinear), m)


# ───────────────────────────── Floransa şapkaları (mazzocchio, brokar yüksek şapka) ─────────────────────────────
def hat_parts2(kind):
    """Baş-birimli ek şapkalar: [(path, rim, tone, 'back'?)]. mazzocchio: yastıklı halka + omuza sarkan kuyruk (foggia); tall: yüksek brokar şapka."""
    P = []
    if kind == "mazzocchio":
        P.append((sp([KC(-0.40, -0.40), (-0.58, -0.30), (-0.74, 0.10), (-0.80, 0.62), (-0.66, 0.92), (-0.50, 0.70), (-0.42, 0.24), (-0.30, -0.10)], True, 0.8), 0.85, 0.0, "back"))
        P.append((sp([KC(-0.46, -0.30), (-0.52, -0.54), (-0.34, -0.80), (0.04, -0.88), (0.38, -0.76), (0.50, -0.50), (0.44, -0.32), (0.20, -0.26), (-0.10, -0.24)], True, 0.9), 1.0, 0.0))
        for t in (-0.30, -0.08, 0.14, 0.34):
            P.append((lens((t, -0.30), (t + 0.04, -0.84), 0.022, 0.03), 0.0, 0.2))
    elif kind == "tall":
        P.append((sp([KC(-0.36, -0.42), (-0.40, -0.80), (-0.36, -1.20), KC(0.30, -1.22), (0.38, -0.80), KC(0.36, -0.42), (0.0, -0.36)], True, 0.7), 1.0, 0.0))
        P.append((sp([KC(-0.44, -0.40), (0.0, -0.34), KC(0.44, -0.40), (0.44, -0.50), (0.0, -0.44), (-0.44, -0.50)], True, 0.6), 1.0, 0.1))
        P.append((sp([KC(-0.38, -1.20), (0.0, -1.26), KC(0.32, -1.20), (0.0, -1.14)], True, 0.6), 0.0, 0.2))
    return P


def add_hat2(F, kind, hx, hy, hh, rot=0.0, back=None):
    if kind in ("mazzocchio", "tall"):
        for part in hat_parts2(kind):
            path, rim, tone = part[0], part[1], part[2]
            is_back = len(part) > 3 and part[3] == "back"
            if back is None or back == is_back:
                F.fill(place(path, hx, hy, hh, rot), rim=rim, tone=tone)
    else:
        FP.add_hat(F, kind, hx, hy, hh, rot, back)


# ───────────────────────────── boyalı figür ─────────────────────────────
class PFig(Fig):
    """Fig'in boyalı sürümü: fill() çağrıları o anki `col`/`pat` ile kaydedilir; render() pigment kenar + mürekkep çizgi uygular."""

    def __init__(self, h, lean=0.0):
        super().__init__(h, lean)
        self.col = "#8A7A66"
        self.pat = None            # (tür, renk, ölçek)

    def fill(self, path, rim=1.0, tone=0.0, alpha=1.0, bound=True, glow=0.0):
        self.ops.append(("pfill", path, self.col, rim, tone, alpha, bound, self.pat))
        if bound:
            self.bound.addPath(path)
        return path

    def line(self, path, width, tone=0.3, alpha=0.6, cap="round"):
        self.ops.append(("pline", path, width, tone, alpha, self.col))

    def cut(self, path):
        pass

    def solid(self, path, color, alpha=1.0, bound=False):
        self.ops.append(("psolid", path, color, alpha))
        if bound:
            self.bound.addPath(path)

    def glowdot(self, *a, **k):
        pass

    def gold(self, path, w, color="#D6A93E", alpha=0.95):
        """Altın filet (sgraffito altın çizgi)."""
        self.ops.append(("pgold", path, w, color, alpha))

    def merge(self, other, dx=0.0, dy=0.0, s=1.0, flip=False, rot=0.0):
        m = skia.Matrix()
        m.setScale(-s if flip else s, s)
        if rot:
            m.postRotate(rot)
        m.postTranslate(dx, dy)

        def T(p):
            q = skia.Path(p)
            q.transform(m)
            return q
        for op in other.ops:
            k = op[0]
            if k == "pfill":
                self.ops.append(("pfill", T(op[1])) + op[2:])
            elif k == "pline":
                self.ops.append(("pline", T(op[1]), op[2] * s) + op[3:])
            elif k == "psolid":
                self.ops.append(("psolid", T(op[1])) + op[2:])
            elif k == "pgold":
                self.ops.append(("pgold", T(op[1]), op[2] * s) + op[3:])
        self.bound.addPath(T(other.bound))

    # --- çizim
    def render(self, c, outline=True, edge=True):
        h = self.h
        ow = max(1.3, h * 0.0044)
        for op in self.ops:
            k = op[0]
            if k == "pfill":
                _, path, col, rim, tone, alpha, bound, pat = op
                cc = col
                if rim < 1.0:
                    cc = mix(col, "#2A1A0C", (1.0 - rim) * 0.42)
                detail = (not bound) and rim <= 0.01
                if detail:
                    cc = mix(col, "#1C1208", 0.50) if tone <= 0.5 else mix(col, LIGHT, 0.55)
                elif tone > 0:
                    cc = mix(cc, LIGHT, min(0.8, tone * 0.8))
                p = skia.Paint(AntiAlias=True, Color=C(cc))
                if alpha < 1:
                    p.setAlphaf(alpha)
                c.drawPath(path, p)
                if pat and not detail:
                    c.save()
                    c.clipPath(path, skia.ClipOp.kIntersect, True)
                    pp = skia.Paint(AntiAlias=True)
                    pp.setShader(pattern_shader(pat[0], pat[1], pat[2] * h / 520.0 if len(pat) > 2 else h / 520.0))
                    pp.setAlphaf(0.85)
                    c.drawPaint(pp)
                    c.restore()
                if edge and bound and not detail:
                    c.save()
                    c.clipPath(path, skia.ClipOp.kIntersect, True)
                    c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=ow * 5.0, Color=C("#1C1208", 46)))
                    c.save(); c.translate(-ow * 0.9, -ow * 0.9)
                    c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=ow * 1.8, Color=C("#FFF6DC", 70)))
                    c.restore()
                    c.restore()
                if outline and bound and not detail:
                    c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=ow, Color=C(INK, 205), StrokeJoin=skia.Paint.kRound_Join))
            elif k == "pline":
                _, path, width, tone, alpha, col = op
                lc = mix(col, "#1C1208", 0.6) if tone <= 0.5 else mix(col, LIGHT, 0.65)
                c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(0.9, width), Color=C(lc, int(255 * alpha)), StrokeCap=skia.Paint.kRound_Cap))
            elif k == "psolid":
                _, path, color, alpha = op
                p = skia.Paint(AntiAlias=True, Color=C(color))
                if alpha < 1:
                    p.setAlphaf(alpha)
                c.drawPath(path, p)
            elif k == "pgold":
                _, path, w, color, alpha = op
                c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.0, w), Color=C("#5A3A10", int(150 * alpha)), StrokeCap=skia.Paint.kRound_Cap))
                c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(0.8, w * 0.62), Color=C(color, int(255 * alpha)), StrokeCap=skia.Paint.kRound_Cap))

    def sprite(self, pad=8):
        """Sıkı kırpılmış yerel biçimli sprite: (img, ox, oy)."""
        b = self.bound.getBounds()
        l, t = int(math.floor(b.left())) - pad, int(math.floor(b.top())) - pad
        r, bt = int(math.ceil(b.right())) + pad, int(math.ceil(b.bottom())) + pad
        fr = sk.Frame(max(2, r - l), max(2, bt - t))
        fr.clear(skia.ColorTRANSPARENT)
        fr.c.translate(-l, -t)
        self.render(fr.c)
        return fr.surf.makeImageSnapshot(), -l, -t


# ───────────────────────────── at ─────────────────────────────
def paint_horse(F, h, pose, coat="#EFE6D2", mane="#6B5A44", bridle="#A8321E", tail=True, dy=0.0):
    """figs_horse.horse_body'nin boyalı yeniden yazımı (aynı geometri): h = kulak ucu yüksekliği."""
    P = pose
    poll = P["poll"]
    L = 0.31
    top, muz, bot, throat, eye, nostril, lip, (ax, ay, nx, ny) = FH._head_geometry(poll, L, P["head_ang"])
    shade = mix(coat, "#3A2A18", 0.20)
    F.col = shade
    FH._hleg(F, P["ff"], "f", h, rim=0.40)
    FH._hleg(F, P["hf"], "h", h, rim=0.40)
    F.col = coat
    FH._hleg(F, P["hn"], "h", h, rim=1.0)
    FH._hleg(F, P["fn"], "f", h, rim=1.0)
    if tail:
        F.col = mane
        if P["tail"] == "stream":
            tp = [(-0.52, -0.745 + dy), (-0.62, -0.745 + dy), (-0.76, -0.725), (-0.90, -0.69), (-1.02, -0.65), (-1.12, -0.63)]
            wd = [0.045, 0.085, 0.095, 0.085, 0.055, 0.012]
        else:
            tp = [(-0.52, -0.745 + dy), (-0.585, -0.70 + dy), (-0.665, -0.60), (-0.705, -0.48), (-0.70, -0.36), (-0.675, -0.27)]
            wd = [0.04, 0.085, 0.095, 0.085, 0.05, 0.012]
        F.fill(limb([(x * h, y * h) for x, y in tp], [w * h for w in wd], cap0=0.4, cap1=0.0), rim=1.0)
        F.crease((-0.62 * h, -0.64 * h), (-0.70 * h, -0.32 * h), 0.008 * h, 0.012 * h, alpha=0.5)
    ex = poll[0] - 0.020
    ey = poll[1] - 0.005
    F.col = shade
    F.fill(sp(FH._hp([KC(ex - 0.016, ey), (ex - 0.026, ey - 0.055), KC(ex - 0.008, ey - 0.118), (ex + 0.020, ey - 0.056), KC(ex + 0.022, ey)], h), True, 0.8), rim=0.6)
    W0 = (0.20, -0.765)
    crest = []
    dxn, dyn = poll[0] - W0[0], poll[1] - W0[1]
    Ln = math.hypot(dxn, dyn)
    cnx, cny = dyn / Ln, -dxn / Ln
    for t in (0.18, 0.38, 0.58, 0.78):
        b = 0.040 * math.sin(math.pi * t)
        crest.append((W0[0] + dxn * t + cnx * b, W0[1] + dyn * t + cny * b))
    B0 = (0.425, -0.60)
    under = []
    for t in (0.22, 0.48, 0.74):
        tx_, ty_ = throat
        q = (tx_ + (B0[0] - tx_) * t, ty_ + (B0[1] - ty_) * t)
        bulge = -0.018 * math.sin(math.pi * t)
        under.append((q[0] + bulge * 0.7, q[1] + bulge * 0.6))
    under = under[::-1]
    body = [KC(-0.515, -0.755 + dy), (-0.45, -0.780 + dy), (-0.34, -0.785 + dy), (-0.20, -0.755 + dy), (-0.02, -0.738 + dy), (0.10, -0.745 + dy), (0.20, -0.766 + dy)] + crest + top + muz + bot + [throat] + under + [
        B0, (0.438, -0.535), (0.405, -0.455), (0.32, -0.418), (0.18, -0.402), (0.02, -0.402), (-0.14, -0.425), (-0.27, -0.452), (-0.38, -0.49), (-0.50, -0.545), (-0.552, -0.625), (-0.548, -0.70)]
    body = [(q[0] * h, q[1] * h, "c") if len(q) > 2 else (q[0] * h, q[1] * h) for q in body]
    F.col = coat
    F.fill(sp(body, True, 1.0), rim=1.0)
    F.col = shade
    F.line(sp(FH._hp([(-0.36, -0.77), (-0.31, -0.62), (-0.30, -0.49)], h), False), h * 0.004, tone=0.0, alpha=0.30)
    F.line(sp(FH._hp([(0.16, -0.755), (0.25, -0.62), (0.30, -0.50)], h), False), h * 0.004, tone=0.0, alpha=0.30)
    F.col = coat
    F.fill(sp(FH._hp([KC(ex - 0.020 + 0.032, ey + 0.004), (ex - 0.030 + 0.032, ey - 0.054), KC(ex - 0.008 + 0.032, ey - 0.121), (ex + 0.024 + 0.032, ey - 0.056), KC(ex + 0.026 + 0.032, ey + 0.004)], h), True, 0.8), rim=1.0)
    F.col = mane
    F.fill(sp(FH._hp([KC(poll[0] + 0.03, poll[1] - 0.012), (poll[0] + 0.07, poll[1] + 0.005), (poll[0] + 0.065, poll[1] + 0.055), (poll[0] + 0.04, poll[1] + 0.07), (poll[0] + 0.035, poll[1] + 0.03)], h), True, 0.8), rim=1.0, bound=False)
    FH._mane_locks(F, (W0[0] + 0.02, W0[1] - 0.012), (poll[0] - 0.015, poll[1] + 0.005), h, n=7, long=P["mane_long"], flick=P["mane_flick"])
    F.col = INK
    F.fill(ell(eye[0] * h, eye[1] * h, 0.010 * h, 0.0075 * h, -20), rim=0.0, tone=0.2, alpha=0.9, bound=False)
    F.fill(ell(nostril[0] * h, nostril[1] * h, 0.0085 * h, 0.0125 * h, -30), rim=0.0, tone=0.2, alpha=0.55, bound=False)
    F.col = bridle
    mx, my = lip

    def Wh(u, v):
        return (poll[0] + L * (u * ax + v * nx), poll[1] + L * (u * ay + v * ny))
    for pts in ([Wh(0.34, -0.06), Wh(0.30, 0.20), Wh(0.30, 0.45)], [Wh(0.12, -0.06), Wh(0.10, 0.12), Wh(0.14, 0.28)], [Wh(0.78, -0.002), Wh(0.77, 0.12), Wh(0.80, 0.24)]):
        F.gold(sp(FH._hp(pts, h), False), h * 0.0042, "#C23A24", 0.95)


def paint_caparison(F, h, hem=-0.30, cloth="#A8321E", pat=("diamond", "#E0B84E"), trim="#D6A93E"):
    """At örtüsü (kapariş): sırt-sağrı-karın boyunca asılı, dilimli etek; desen + altın kenar."""
    F.col = cloth
    pts = [KC(0.18 * h, -0.755 * h), (0.0 * h, -0.735 * h), (-0.25 * h, -0.755 * h), (-0.48 * h, -0.74 * h), (-0.58 * h, -0.62 * h), (-0.57 * h, -0.45 * h)]
    n = 8
    for i in range(n + 1):
        u = i / n
        x = -0.56 + (0.37 - -0.56) * u
        y = hem + 0.03 * math.sin(u * math.pi * n)
        pts.append((x * h, y * h) if (i % 2 == 0) else (x * h, (y + 0.05) * h))
    pts += [(0.34 * h, -0.44 * h), (0.31 * h, -0.62 * h)]
    F.pat = (pat[0], pat[1], 0.9) if pat else None
    F.fill(sp(pts, True, 0.9), rim=1.0)
    F.pat = None
    F.gold(sp([(-0.57 * h, -0.45 * h), (-0.40 * h, hem * h), (-0.2 * h, (hem + 0.03) * h), (0.0, hem * h), (0.2 * h, (hem + 0.03) * h), (0.35 * h, -0.44 * h)], False), h * 0.006, trim, 0.95)
    for x in (-0.38, -0.22, -0.06, 0.10, 0.24):
        F.crease((x * h, -0.72 * h), ((x - 0.01) * h, (hem + 0.02) * h), 0.008 * h, 0.01 * h, alpha=0.5)


# ───────────────────────────── binici ─────────────────────────────
def paint_rider(F, px, py, u, robe="#2A4A9A", robe2="#E0B84E", hat="flatcap", hat_col="#A8321E", skin="#E7C4A0", hair="#5A3A22", pat=("diamond", "#E0B84E"), sleeve=None, hose="#8A2A2A", beard=None, lean=0.0, feather=None):
    """Gozzoli tarzı binici: dik gövde, geniş kollu brokar giysi, atın sırtına dökülen etek, üzengide sivri ayakkabı, profil baş + şapka.
    (px,py) = eyerdeki kalça noktası; u = oturma boyu (kalça → baş tepesi)."""
    R = PFig(F.h)

    def P(x, y):
        return (x * u, y * u)

    def KP(x, y):
        return KC(x * u, y * u)
    # uzak bacak (at gövdesinin arkasında) + yakın bacak: çorap + sivri ayakkabı
    R.col = mix(hose, "#2A1A0C", 0.25)
    R.fill(limb([P(0.02, 0.05), P(0.26, 0.34), P(0.17, 0.86)], [0.26 * u, 0.20 * u, 0.15 * u], cap0=0.4, cap1=0.3), rim=0.6)
    R.col = hose
    R.fill(limb([P(0.04, 0.06), P(0.32, 0.34), P(0.21, 0.88)], [0.28 * u, 0.22 * u, 0.16 * u], cap0=0.4, cap1=0.3), rim=1.0)
    R.col = "#2C1C10"
    R.fill(K.shoe(0.17 * u, 0.93 * u, 0.34 * u, 0.10 * u, 1, "sharp"), rim=1.0)
    # etek (atın sırtına dökülür)
    R.col = robe
    R.pat = (pat[0], pat[1], 0.8) if pat else None
    R.fill(sp([KP(-0.12, -0.12), P(-0.40, -0.02), P(-0.60, 0.20), P(-0.56, 0.50), KP(-0.20, 0.52), P(0.06, 0.44), P(0.26, 0.20), P(0.22, -0.04)], True, 0.9), rim=1.0)
    R.pat = None
    R.gold(sp([P(-0.56, 0.50), P(-0.38, 0.54), P(-0.20, 0.52), P(0.06, 0.44)], False), u * 0.016, robe2, 0.95)
    R.crease(P(-0.20, -0.06), P(-0.42, 0.46), 0.020 * u, 0.04 * u)
    R.crease(P(-0.04, -0.04), P(-0.14, 0.48), 0.016 * u, 0.03 * u)
    # gövde
    R.col = robe
    R.pat = (pat[0], pat[1], 0.8) if pat else None
    R.fill(sp([KP(-0.12, -0.04), P(-0.20, -0.30), P(-0.18, -0.58), KP(-0.06, -0.72), KP(0.12, -0.70), P(0.22, -0.58), P(0.22, -0.30), P(0.20, -0.06)], True, 0.9), rim=1.0)
    R.pat = None
    # kemer + altın düğme sırası
    R.col = robe2
    R.fill(poly([P(-0.14, -0.20), P(0.22, -0.20), P(0.22, -0.13), P(-0.14, -0.13)]), rim=1.0, bound=False)
    # kol: geniş kollu, dirsekten rene doğru
    R.col = sleeve or robe
    R.pat = (pat[0], pat[1], 0.7) if pat else None
    R.fill(sp([P(-0.02, -0.64), P(0.20, -0.60), P(0.34, -0.40), P(0.34, -0.22), P(0.20, -0.18), P(0.12, -0.34), P(0.02, -0.44)], True, 0.9), rim=1.0)
    R.pat = None
    R.col = skin
    R.fill(K.hand_pt("fist", 0.30 * u, -0.26 * u, 0.20 * u, -10), rim=1.0)
    # boyun + baş
    R.col = skin
    R.fill(limb([P(0.03, -0.80), P(0.03, -0.70)], [0.14 * u, 0.17 * u], cap0=0, cap1=0), rim=0.9)
    hx, hy, hh = 0.08 * u, -0.935 * u, 0.28 * u
    R.col = hat_col
    add_hat2(R, hat, hx, hy, hh, -2.0, back=True) if hat in ("mazzocchio", "tall") else None
    R.col = hair
    R.fill(place(FP.hair_path("long" if hair != "none" else "bob"), hx, hy, hh, -2.0), rim=1.0) if hair != "none" else None
    R.col = skin
    R.fill(place(K.head_path("m", nose=1.05, chin=0.0), hx, hy, hh, -2.0), rim=1.0)
    if beard:
        R.col = hair
        R.fill(place(K.beard_path(beard), hx, hy, hh, -2.0), rim=0.9)
    # şapka
    R.col = hat_col
    if hat in ("mazzocchio", "tall"):
        add_hat2(R, hat, hx, hy, hh, -2.0, back=False)
    else:
        FP.add_hat(R, hat, hx, hy, hh, -2.0)
    F.merge(R, dx=px, dy=py, rot=lean)


# ───────────────────────────── yaya figürler ─────────────────────────────
def paint_walker(h, kind="noble", robe="#A8321E", robe2="#E0B84E", hat="flatcap", hat_col="#233C8C", skin="#E7C4A0", hair="#5A3A22", hose_l="#233C8C", hose_r="#A8321E",
                 pat=("fleur", "#E0B84E"), beard=None, stride=1.0, holds=None):
    """Yürüyen yaya figür: 'noble' (uzun cüppe) | 'page' (kısa tunik + parti-colored çorap) | 'elder' (uzun cüppe, sakallı). Sağa bakar."""
    F = PFig(h)
    if kind == "page":
        # bacaklar: sol bacak bir renk, sağ bacak başka renk
        F.col = hose_r
        FP.add_leg(F, h, (0.045, -0.40), (0.115 * stride, -0.205), (0.20 * stride, -0.036), wd=(0.062, 0.044, 0.030), toe=1, shoe_kind="sharp", shoe_w=0.14, rim=0.7)
        F.col = hose_l
        FP.add_leg(F, h, (-0.01, -0.40), (-0.095 * stride, -0.20), (-0.17 * stride, -0.034), wd=(0.066, 0.046, 0.030), toe=1, shoe_kind="sharp", shoe_w=0.14, rim=1.0)
        F.col = robe
        F.pat = (pat[0], pat[1], 0.7) if pat else None
        F.fill(FP.robe_path(h, sh_y=-0.755, nb=(-0.04, 0.05), back_sh=-0.095, front_sh=0.085, chest=(-0.105, 0.095, -0.66), waist=(-0.09, 0.09, -0.52), hip=(-0.115, 0.13, -0.46), hem=(-0.14, 0.17, -0.37), nfold=3, amp=0.01, dag=0.028), rim=1.0)
        F.pat = None
        F.col = robe2
        F.fill(poly([(-0.10 * h, -0.55 * h), (0.10 * h, -0.55 * h), (0.10 * h, -0.52 * h), (-0.10 * h, -0.52 * h)]), rim=1.0, bound=False)
        F.col = robe
        FP.add_arm(F, [(0.0, -0.69 * h), (0.07 * h, -0.56 * h), (0.14 * h, -0.47 * h)], [0.10 * h, 0.09 * h, 0.075 * h], hand=None)
        F.col = skin
        F.fill(K.hand_pt("open", 0.135 * h, -0.47 * h, 0.085 * h, 50), rim=1.0)
        hh = 0.115 * h
        hx, hy = 0.012 * h, -0.84 * h
    else:
        # uzun cüppe
        F.col = hose_r
        FP.add_leg(F, h, (0.03, -0.12), (0.05, -0.07), (0.14 * stride, -0.034), wd=(0.05, 0.04, 0.028), toe=1, shoe_kind="sharp", shoe_w=0.12, rim=0.7)
        F.col = robe
        F.pat = (pat[0], pat[1], 0.8) if pat else None
        F.fill(FP.robe_path(h, sh_y=-0.755, nb=(-0.04, 0.05), back_sh=-0.105, front_sh=0.095, chest=(-0.115, 0.10, -0.66), waist=(-0.10, 0.095, -0.50), hip=(-0.15, 0.15, -0.30), hem=(-0.215 * (1 if kind == "noble" else 1.05), 0.21, -0.012),
                                 nfold=4, amp=0.008, dag=0.0, wave_b=0.01, wave_f=0.01, swing=0.02 * stride), rim=1.0)
        F.pat = None
        FP.robe_folds(F, h, -0.06, 0.06, -0.48, -0.03, 4, 0.0075, seed=3)
        F.col = robe2
        F.fill(poly([(-0.10 * h, -0.50 * h), (0.095 * h, -0.50 * h), (0.095 * h, -0.465 * h), (-0.10 * h, -0.465 * h)]), rim=1.0, bound=False)
        F.gold(sp([(-0.21 * h, -0.025 * h), (-0.1 * h, -0.012 * h), (0.0, -0.025 * h), (0.1 * h, -0.012 * h), (0.2 * h, -0.025 * h)], False), h * 0.006, robe2, 0.95)
        F.col = robe
        FP.add_arm(F, [(0.0, -0.69 * h), (0.075 * h, -0.55 * h), (0.145 * h, -0.45 * h)], [0.11 * h, 0.10 * h, 0.085 * h], hand=None)
        F.col = skin
        F.fill(K.hand_pt("open", 0.140 * h, -0.455 * h, 0.085 * h, 50), rim=1.0)
        hh = 0.115 * h
        hx, hy = 0.012 * h, -0.84 * h
    F.col = skin
    F.fill(limb([(hx - 0.01 * h, hy + 0.04 * h), (hx - 0.012 * h, -0.745 * h)], [0.062 * h, 0.08 * h], cap0=0, cap1=0), rim=0.9)
    if hat in ("mazzocchio", "tall"):
        F.col = hat_col
        add_hat2(F, hat, hx, hy, hh, 0, back=True)
    if hair and hair != "none":
        F.col = hair
        F.fill(place(FP.hair_path("long" if kind != "page" else "bob"), hx, hy, hh, 0), rim=1.0)
    F.col = skin
    F.fill(place(K.head_path("m" if kind != "elder" else "o", nose=1.05), hx, hy, hh, 0), rim=1.0)
    if beard:
        F.col = hair or "#5A3A22"
        F.fill(place(K.beard_path(beard), hx, hy, hh, 0), rim=0.9)
    F.col = hat_col
    if hat in ("mazzocchio", "tall"):
        add_hat2(F, hat, hx, hy, hh, 0, back=False)
    else:
        FP.add_hat(F, hat, hx, hy, hh, 0)
    return F


def build_rider(h, coat, mane, cloth, robe, robe2, hat, hat_col, hose, hair, pat, pose=None, skin="#E7C4A0", beard=None, caparison=True, cl_pat=("diamond", "#E0B84E")):
    """Atlı: at (HORSE_WALK) + kapariş + binici. h = zeminden binici başlığına toplam boy (figs_horse ile aynı sözleşme)."""
    pose = pose or FH.HORSE_WALK
    F = PFig(h)
    hs = h / 1.2
    Hf = PFig(hs)
    paint_horse(Hf, hs, pose, coat, mane, "#A8321E")
    if caparison:
        paint_caparison(Hf, hs, cloth=cloth, pat=cl_pat)
    R = pose.get("rot", 0.0)
    F.merge(Hf, 0, 0, 1.0, rot=R)
    m = skia.Matrix()
    m.setRotate(R)
    q = m.mapXY(-0.005 * hs, -0.735 * hs)
    u = 0.45 * hs
    paint_rider(F, q.x(), q.y(), u, robe, robe2, hat, hat_col, skin, hair, pat, None, hose, beard)
    return F


@functools.lru_cache(maxsize=64)
def rider_sprite(h, spec):
    """spec: tuple(sorted(dict.items())) → (img, ox, oy)."""
    d = dict(spec)
    F = build_rider(h, d["coat"], d["mane"], d["cloth"], d["robe"], d["robe2"], d["hat"], d["hat_col"], d["hose"], d["hair"], d["pat"], pose=FH.HORSE_WALK if d.get("pose", "walk") == "walk" else FH.HORSE_STAND,
                    beard=d.get("beard"), caparison=d.get("capar", True), cl_pat=d.get("cl_pat", ("diamond", "#E0B84E")))
    return F.sprite(pad=10)


@functools.lru_cache(maxsize=64)
def walker_sprite(h, spec):
    d = dict(spec)
    F = paint_walker(h, d["kind"], d["robe"], d["robe2"], d["hat"], d["hat_col"], d.get("skin", "#E7C4A0"), d["hair"], d["hose_l"], d["hose_r"], d["pat"], d.get("beard"), d.get("stride", 1.0))
    return F.sprite(pad=10)


def spec(**kw):
    return tuple(sorted(kw.items()))
