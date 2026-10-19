"""cilt_oda — İÇ MEKÂN DÜNYASI (`oda` çekim türü; Lab-D). Oda, salon, banka, hücre/kütüphane/studiolo, sakristi, boş oda, sahne.

`shot("oda", a, room="oda1743"|"salon"|"banka"|"calisma"|"sakristi"|"bos"|"perde", variant=…, tod="day|dusk|night" (ya da mode=), path="in"|"out"|…,
      cams=[(çapa,(x,y,zoom)),…], actors=[dict(kind, x, y, h, action, at, …)], props=[…], kick=, caption=, at=, frame=True|False|"auto", seed=, **oda_parametreleri)`
Mimari cilt_pano ile aynıdır: ağır statik katmanlar (duvar 0,9 · ana düzlem 1,0 · ön plan 1,18 paralaks) 1024 px kareaş olarak TEMBEL pişirilir
(out/_cache/world/oda_*.png); mum alevi, ışık huzmesi, toz, perde, figür, kapı gibi canlı şeyler kare başına vektör çizilir (zumda keskin kalır).
Kamera: `cams` (x = ekran merkezinin oda x'i, y = dikey kayma, zoom) ya da odanın adlı yolu `path=`. Çerçeve bandı zum 1,5'i aşınca tam ekrana açılır (belge dokusuna girerken).
Yeniden kullanılabilir küçük işlevler (ekran/tuval koordinatında): `candle`, `window_light`, `table`, `door_bronze`, `quill`, `inkwell`, `doc_sheet`, `sil_actor`.
Kısıt: yüz çizilmez (siluet), şiddet/kan yok, kaynaksız etiket yok (yazı yalnız parametreyle gelir).
"""
import functools
import math
import os

import cv2
import numpy as np
import skia

import cilt_anim as FA
import cilt_medici as CM
import cilt_pano as PN
import cilt_paper as PP
import sk
from cilt_medici import TH, ckind
from sk import C, H, W, clamp, ease_io, mix, smooth

HERE = os.path.dirname(os.path.abspath(__file__))
OVER = "o3"                      # önbellek sürümü (çizim kodu değişince artır)
OV = PN.OV
LIN = PN.LIN
INK = PN.INK
_RS = PN._RS
R, RA, INKP, INKR, LINE, POLY, OVAL, GRAD_V = PN.R, PN.RA, PN.INKP, PN.INKR, PN.LINE, PN.POLY, PN.OVAL, PN.GRAD_V
F_WALL, F_FG = 0.90, 1.18        # paralaks çarpanları
Y_FL = 700                       # duvar/zemin kesişimi (katman y)
LH = 800 + 2 * OV                # katman yüksekliği
GOLD = "#D2A33E"


# ═════════════════════════════ renk uyarlaması ═════════════════════════════
class OTint:
    """Gece iç mekân: renkler sıcak kalır (karanlığı `CM.relight` mum havuzu getirir); dusk sıcak turuncu."""

    def __init__(self, tod="day"):
        self.tod = tod

    def __call__(self, col, depth=0.0):
        if self.tod == "night":
            c = mix(col, "#3A2616", 0.08)
        elif self.tod == "dusk":
            c = mix(col, "#E58A55", 0.16)
        else:
            c = col
        if depth:
            c = mix(c, "#1A1A2A" if self.tod == "night" else "#B6A88C", clamp(depth) * 0.30)
        return c


# ═════════════════════════════ küçük çizim yardımcıları ═════════════════════════════
def PT(col, a=255, **kw):
    return skia.Paint(AntiAlias=True, Color=C(col, a), **kw)


def STK(col, w=1.2, a=255, cap=True):
    return skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, a), StrokeCap=skia.Paint.kRound_Cap if cap else skia.Paint.kButt_Cap,
                      StrokeJoin=skia.Paint.kRound_Join)


def HGRAD(c, x0, y0, x1, y1, stops):
    cols = [C(s[0], s[2] if len(s) > 2 else 255) for s in stops]
    sh = skia.GradientShader.MakeLinear([(x0, 0), (x1, 0)], cols, [s[1] for s in stops])
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.Paint(Shader=sh))


def LGP(p0, p1, stops):
    """Doğrusal degrade boya."""
    cols = [C(s[0], s[2] if len(s) > 2 else 255) for s in stops]
    return skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([p0, p1], cols, [s[1] for s in stops]))


def SOFT(c, x, y, rx, ry, col, a=120):
    """Yumuşak elips (radyal degrade): gölge/ışık lekesi."""
    if rx < 1 or ry < 1 or a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(1.0, ry / rx)
    sh = skia.GradientShader.MakeRadial((0, 0), rx, [C(col, int(a)), C(col, int(a * 0.42)), C(col, 0)], [0.0, 0.5, 1.0])
    c.drawCircle(0, 0, rx, skia.Paint(AntiAlias=True, Shader=sh))
    c.restore()


def FILLP(c, path, col, a=255, ink=1.4, inka=190, icol=INK, shader=None):
    p = skia.Paint(AntiAlias=True, Color=C(col, a))
    if shader is not None:
        p.setShader(shader.getShader() if isinstance(shader, skia.Paint) else shader)
    c.drawPath(path, p)
    if ink:
        INKP(c, path, ink, inka, icol)


def RRECT(c, x0, y0, x1, y1, r, col, a=255, ink=1.3, inka=180):
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x0, y0, x1, y1), r, r)
    c.drawRRect(rr, PT(col, a))
    if ink:
        c.drawRRect(rr, STK(INK, ink, inka))


def BOX(c, x0, y0, x1, y1, col, T, hl=0.16, sh=0.22, ink=1.3, a=255, depth=0.0):
    """Işık sol-üstten: yatay degradeli (açık→koyu) kutu + mürekkep çerçeve."""
    cc = T(col, depth)
    HGRAD(c, x0, y0, x1, y1, [(mix(cc, "#FFFFFF", hl), 0.0, a), (cc, 0.38, a), (mix(cc, "#000000", sh), 1.0, a)])
    if ink:
        INKR(c, x0, y0, x1, y1, ink, 170)


def WOOD(c, x0, y0, x1, y1, T, col="#8A5A38", seed=0, ink=1.3, vertical=False, grain=5):
    """Ahşap yüzey: degrade + lif çizgileri + mürekkep kenar."""
    BOX(c, x0, y0, x1, y1, col, T, ink=ink) if not vertical else None
    if vertical:
        GRAD_V(c, x0, y0, x1, y1, [(mix(T(col), "#FFFFFF", 0.14), 0.0), (T(col), 0.4), (mix(T(col), "#000000", 0.22), 1.0)])
        if ink:
            INKR(c, x0, y0, x1, y1, ink, 170)
    rs = _RS(seed * 17 + int(x0) + int(y0) * 3)
    for i in range(grain):
        if vertical:
            xx = rs.uniform(x0 + 2, x1 - 2)
            c.drawLine(xx, y0 + 2, xx + rs.uniform(-2, 2), y1 - 2, STK("#2A1A0C", rs.uniform(0.6, 1.3), int(rs.uniform(26, 58))))
        else:
            yy = rs.uniform(y0 + 2, y1 - 2)
            c.drawLine(x0 + 2, yy, x1 - 2, yy + rs.uniform(-1.5, 1.5), STK("#2A1A0C", rs.uniform(0.6, 1.3), int(rs.uniform(26, 58))))


def SHADE_R(c, x0, y0, x1, y1, a=40):
    PN.shade_right(c, x0, y0, x1, y1, a)


# ═════════════════════════════ süreklilik gürültüsü, sıva, zemin ═════════════════════════════
_NW = []


def _nwaves():
    if not _NW:
        rs = np.random.RandomState(77)
        for k in range(16):
            lam = 26.0 * (1.5 ** k)
            ang = rs.uniform(0, math.pi)
            _NW.append((2 * math.pi / lam * math.cos(ang), 2 * math.pi / lam * math.sin(ang), rs.uniform(0, 6.28), 1.0 / (1.0 + 0.45 * k)))
    return _NW


def noise_field(xa, ya, w, h, k0=0, k1=12, step=4):
    """Mutlak koordinatlı (kareaşlar arası kesintisiz) düşük frekanslı gürültü, birim std."""
    gw, gh = int(w) // step + 3, int(h) // step + 3
    xs = xa + np.arange(gw) * step
    ys = ya + np.arange(gh) * step
    out = np.zeros((gh, gw), np.float32)
    for fx, fy, ph, a in _nwaves()[k0:k1]:
        out += a * np.sin(fx * xs[None, :] + fy * ys[:, None] + ph)
    out = cv2.resize(out, (gw * step, gh * step), interpolation=cv2.INTER_CUBIC)[:int(h), :int(w)]
    return out / (out.std() + 1e-6)


def plaster(c, xa, xb, y0, y1, T, top, bot, amp=0.05, warm=(255, 246, 222), cool=(96, 66, 38)):
    """Boyalı sıva duvar: dikey degrade + kesintisiz lekeli doku."""
    GRAD_V(c, xa, y0, xb, y1, [(T(top), 0.0), (T(bot), 1.0)])
    w, h = int(xb - xa) + 1, int(y1 - y0) + 1
    f = noise_field(xa, y0, w, h, 1, 11, 4) + 0.45 * noise_field(xa, y0, w, h, 7, 14, 2)
    arr = np.zeros((h, w, 4), np.uint8)
    pos = f > 0
    arr[..., 0] = np.where(pos, warm[0], cool[0])
    arr[..., 1] = np.where(pos, warm[1], cool[1])
    arr[..., 2] = np.where(pos, warm[2], cool[2])
    arr[..., 3] = np.clip(np.abs(f) * amp * 255, 0, 96).astype(np.uint8)
    c.drawImage(sk.np_to_image(np.ascontiguousarray(arr)), xa, y0, LIN)


def floor_tiles(c, xa, xb, y0, y1, T, c1="#B5603A", c2="#A5522F", seed=3, w0=60.0, grow=1.16, rowh=12.0, joint=70, shade=True):
    """Perspektifli terrakota/kâğıt döşeme: sıra yüksekliği ve karo genişliği aşağı doğru büyür; karolar mutlak x'e göre (kareaşlar arası kesintisiz)."""
    GRAD_V(c, xa, y0 - 2, xb, y1, [(T(mix(c1, "#000000", 0.28)), 0.0), (T(c1), 0.5), (T(mix(c1, "#FFFFFF", 0.08)), 1.0)])
    y, k = y0, 0
    wk = w0
    rh = rowh
    while y < y1:
        off = (k % 2) * wk / 2
        x = xa - (xa % wk) - wk + off
        while x < xb + wk:
            idx = int(round((x - off) / wk))
            h_ = (idx * 7919 + k * 104729 + seed * 31) & 0xFF
            a_ = 40 + (h_ % 5) * 14
            col = c2 if (idx + k) % 2 == 0 else c1
            c.drawRect(skia.Rect.MakeLTRB(x, y, x + wk, y + rh), PT(T(mix(col, "#2A1408" if h_ % 3 == 0 else "#FFE9C8", 0.08)), a_ + 80))
            x += wk
        c.drawLine(xa, y, xb, y, STK("#2A1608", 1.0 + k * 0.10, joint, False))
        x = xa - (xa % wk) - wk + off
        while x < xb + wk:
            c.drawLine(x, y, x - 1.5, y + rh, STK("#2A1608", 0.9, int(joint * 0.8), False))
            x += wk
        y += rh
        rh *= grow
        wk *= 1.045
        k += 1
    if shade:
        sh = LGP((0, y0), (0, y0 + 46), [("#1A0F06", 0.0, 110), ("#1A0F06", 1.0, 0)])
        c.drawRect(skia.Rect.MakeLTRB(xa, y0, xb, y0 + 46), sh)


def floor_planks(c, xa, xb, y0, y1, T, col="#8A6038", seed=5, w0=210.0, rowh=14.0, grow=1.17):
    """Perspektifli tahta döşeme (uzun tahtalar, rastgele ton, uç birleşimleri)."""
    GRAD_V(c, xa, y0 - 2, xb, y1, [(T(mix(col, "#000000", 0.30)), 0.0), (T(col), 0.5), (T(mix(col, "#FFFFFF", 0.06)), 1.0)])
    y, k = y0, 0
    rh = rowh
    wk = w0
    while y < y1:
        off = ((k * 83) % 100) / 100.0 * wk
        x = xa - ((xa - off) % wk) - wk
        while x < xb + wk:
            idx = int(round((x - off) / wk))
            h_ = (idx * 7919 + k * 104729 + seed * 31) & 0xFF
            tone = mix(col, "#2A1408" if h_ % 2 == 0 else "#E8C896", 0.05 + (h_ % 5) * 0.015)
            c.drawRect(skia.Rect.MakeLTRB(x, y, x + wk, y + rh), PT(T(tone), 120))
            c.drawLine(x, y, x - 1.0, y + rh, STK("#1E1006", 1.0, 120, False))
            # lif
            c.drawLine(x + wk * 0.1, y + rh * 0.5, x + wk * 0.9, y + rh * 0.5 + ((h_ % 3) - 1) * 1.2, STK("#2A1608", 0.8, 40, False))
            x += wk
        c.drawLine(xa, y, xb, y, STK("#1E1006", 1.0 + k * 0.1, 150, False))
        y += rh
        rh *= grow
        wk *= 1.04
        k += 1
    sh = LGP((0, y0), (0, y0 + 50), [("#1A0F06", 0.0, 120), ("#1A0F06", 1.0, 0)])
    c.drawRect(skia.Rect.MakeLTRB(xa, y0, xb, y0 + 50), sh)


def rug(c, x0, x1, yt, yb, T, field="#9A2A22", border="#233C8C", trim="#D2A33E", inset=0.10):
    """Perspektifli halı (üst kenar dar): bordür + ince altın şerit + baklava deseni."""
    dx = (x1 - x0) * inset
    q = lambda u, v: (x0 + dx * (1 - v) + (x1 - x0 - 2 * dx * (1 - v)) * u, yt + (yb - yt) * v)

    def poly(u0, u1, v0, v1):
        return sk.poly_path([q(u0, v0), q(u1, v0), q(u1, v1), q(u0, v1)])
    SOFT(c, (x0 + x1) / 2 + 6, yb + 6, (x1 - x0) * 0.52, 16, "#000000", 70)
    FILLP(c, poly(0, 1, 0, 1), border, 255, 1.4)
    FILLP(c, poly(0.035, 0.965, 0.13, 0.87), trim, 255, 0.0)
    FILLP(c, poly(0.05, 0.95, 0.20, 0.80), field, 255, 1.0)
    # baklava deseni
    for i in range(5):
        u = 0.14 + i * 0.18
        pts = [q(u, 0.50), q(u + 0.07, 0.30), q(u + 0.14, 0.50), q(u + 0.07, 0.70)]
        c.drawPath(sk.poly_path(pts), PT(T("#E8C25A"), 150))
        c.drawPath(sk.poly_path(pts), STK("#3A1008", 1.1, 140))
        p2 = [q(u + 0.07, 0.42), q(u + 0.10, 0.50), q(u + 0.07, 0.58), q(u + 0.04, 0.50)]
        c.drawPath(sk.poly_path(p2), PT(T("#233C8C"), 190))
    for v in (0.24, 0.76):
        a, b = q(0.07, v), q(0.93, v)
        c.drawLine(a[0], a[1], b[0], b[1], STK("#E8C25A", 1.4, 160))
    # saçak
    for i in range(18):
        u = (i + 0.5) / 18
        a = q(u, 0.0)
        c.drawLine(a[0], a[1], a[0] + 0.5, a[1] - 7, STK("#E2D6B0", 1.2, 200))
        b = q(u, 1.0)
        c.drawLine(b[0], b[1], b[0], b[1] + 8, STK("#E2D6B0", 1.4, 220))


# ═════════════════════════════ alev, mum, ışık ═════════════════════════════
def _flame_path(x, y, fh, w, lean):
    p = skia.Path()
    p.moveTo(x - w * 0.5, y)
    p.quadTo(x - w * 1.05, y - fh * 0.50, x + lean, y - fh)
    p.quadTo(x + w * 1.05, y - fh * 0.50, x + w * 0.5, y)
    p.quadTo(x, y + fh * 0.16, x - w * 0.5, y)
    p.close()
    return p


def flicker(t, seed=0.0):
    """(yükseklik çarpanı, eğim −1..1, parlaklık): kesintisiz sinüs toplamı + seyrek esinti."""
    a1 = math.sin(t * 9.1 + seed)
    a2 = math.sin(t * 14.9 + seed * 2.3)
    a3 = math.sin(t * 3.3 + seed * 0.7)
    gust = max(0.0, math.sin(t * 0.83 + seed * 1.9)) ** 14
    fl = 1.0 + 0.07 * a1 + 0.05 * a2 - 0.10 * gust
    lean = 0.35 * a3 + 0.20 * a1 * 0.5 + 0.55 * gust * math.sin(t * 2.6 + seed)
    br = 1.0 + 0.10 * a1 + 0.06 * a2 - 0.12 * gust
    return fl, lean, br


def candle(f, x, y, h, t, seed=0, lit=1.0, holder=True, wax="#EFE6CE", halo=1.0, smoke=True, night=True):
    """Mum: (x,y) taban ortası, h mum boyu (px). Alev titrer/eğilir (esinti), çevresinde sıcak ışıma, ince duman. lit 0..1 (söner/yanar). Dönüş: (alev x, alev y, parlaklık)."""
    c = f.c
    w = max(5.0, h * 0.13)
    top = y - h
    if holder:
        # pirinç şamdan tabanı
        c.drawOval(skia.Rect.MakeLTRB(x - w * 2.0, y - w * 0.55, x + w * 2.0, y + w * 0.45), PT("#B8903A"))
        c.drawOval(skia.Rect.MakeLTRB(x - w * 2.0, y - w * 0.55, x + w * 2.0, y + w * 0.45), STK(INK, 1.0, 170))
        c.drawRect(skia.Rect.MakeLTRB(x - w * 0.75, y - w * 1.4, x + w * 0.75, y - w * 0.3), PT("#A47E30"))
        c.drawRect(skia.Rect.MakeLTRB(x - w * 0.75, y - w * 1.4, x + w * 0.75, y - w * 0.3), STK(INK, 0.9, 150))
    HGRAD(c, x - w * 0.5, top, x + w * 0.5, y - w * 1.2, [(mix(wax, "#FFFFFF", 0.5), 0.0), (wax, 0.35), (mix(wax, "#7A6A4A", 0.45), 1.0)])
    INKR(c, x - w * 0.5, top, x + w * 0.5, y - w * 1.2, 0.9, 150)
    # mum damlası
    c.drawOval(skia.Rect.MakeLTRB(x + w * 0.18, top + 2, x + w * 0.58, top + 4 + h * 0.20), PT(mix(wax, "#FFFFFF", 0.35), 235))
    c.drawOval(skia.Rect.MakeLTRB(x - w * 0.5, top - 1.5, x + w * 0.5, top + 2.5), PT(mix(wax, "#FFFFFF", 0.55)))
    fl, lean, br = flicker(t, seed)
    fh = max(0.0, h * 0.50 * fl * lit)
    fx, fy = x + lean * 0.20 * fh * 0.4, top - fh * 0.55
    if lit > 0.02:
        # fitil
        c.drawLine(x, top - 1, x + lean * 0.9, top - 7 * lit, STK("#1A1008", 1.4, 230))
        if halo > 0:
            PN.glow(c, x + lean * 0.3, top - fh * 0.5, 2.6 * h * lit + 40, "#FFB454", 0.30 * br * halo * lit)
            PN.glow(c, x + lean * 0.3, top - fh * 0.5, 1.1 * h * lit + 16, "#FFD27A", 0.34 * br * halo * lit)
        fw = w * 0.95
        c.drawPath(_flame_path(x, top - 1, fh, fw, lean * fh * 0.22), PT("#FF9A3A", int(235 * min(1, lit * 1.4))))
        c.drawPath(_flame_path(x, top - 1, fh * 0.80, fw * 0.62, lean * fh * 0.16), PT("#FFD66B", 250))
        c.drawPath(_flame_path(x, top - 1, fh * 0.46, fw * 0.30, lean * fh * 0.08), PT("#FFF6D6", 255))
    if smoke and lit < 0.98:
        # söndükten sonra ince duman
        for q in range(6):
            ph = (t * 0.30 + q / 6.0 + seed * 0.13) % 1.0
            FA._puff(c, x + math.sin(ph * 6 + q + seed) * (6 + 14 * ph) + 4 * lean, top - 8 - ph * 130, 4 + 18 * ph, 0.34 * (1 - ph) ** 1.3 * (1.0 - lit), "#C8C0B0")
    elif smoke and lit > 0.3:
        for q in range(3):
            ph = (t * 0.18 + q / 3.0 + seed * 0.21) % 1.0
            FA._puff(c, x + math.sin(ph * 5 + q) * (5 + 9 * ph) + 6 * lean * ph, top - fh - ph * 70, 3 + 9 * ph, 0.10 * (1 - ph) ** 1.4, "#D8D0C0")
    return fx, fy, br


def moth(c, x, y, t, seed=0.0, r=34.0, a=1.0):
    """Alevin çevresinde dönen küçük güve: gevşek Lissajous yolu, kanat çırpışı (hızlı), arada alevden uzaklaşır. (x,y) = alev merkezi."""
    ph = t * 1.7 + seed * 2.3
    far = 0.6 + 0.4 * math.sin(t * 0.35 + seed)
    mx = x + math.cos(ph) * r * far * 1.15 + math.sin(ph * 2.3) * r * 0.25
    my = y + math.sin(ph * 1.3) * r * far * 0.8 + math.cos(ph * 3.1) * r * 0.2
    fl = abs(math.sin(t * 46.0 + seed * 5.0))
    ang = math.degrees(math.atan2(math.cos(ph * 1.3) * 1.3, -math.sin(ph))) * 0.25
    c.save()
    c.translate(mx, my)
    c.rotate(ang)
    for sg in (-1, 1):
        c.drawOval(skia.Rect.MakeLTRB(-6.5 if sg < 0 else 0.5, -2.2 - 5.5 * fl, -0.5 if sg < 0 else 6.5, 2.2), PT("#E8DCC0", int(215 * a)))
    c.drawOval(skia.Rect.MakeLTRB(-1.2, -1.8, 1.2, 3.4), PT("#3A2A18", int(240 * a)))
    c.restore()


def oil_lamp(f, x, y, s, t, seed=0, lit=1.0, hang=0.0):
    """Yağ kandili (San Marco hücresi): kil/pirinç kandil, kısa kalın alev. x,y = taban; s = ölçek (≈ yükseklik px). hang>0: zincirden sarkar (tavandan y−hang)."""
    c = f.c
    if hang > 0:
        c.drawLine(x, y - s * 0.9 - hang, x, y - s * 0.9, STK("#3A2A18", 1.6, 220))
    # gövde (boğumlu kap)
    p = skia.Path()
    p.moveTo(x - s * 0.42, y - s * 0.55)
    p.quadTo(x - s * 0.55, y - s * 0.05, x - s * 0.18, y)
    p.lineTo(x + s * 0.20, y)
    p.quadTo(x + s * 0.55, y - s * 0.05, x + s * 0.42, y - s * 0.55)
    p.close()
    FILLP(c, p, "#9A7A38", 255, 1.2, 190, shader=LGP((x - s * 0.5, 0), (x + s * 0.5, 0), [("#D9B860", 0.0), ("#9A7A38", 0.5), ("#5E4620", 1.0)]))
    # ağız + gaga
    q = skia.Path()
    q.moveTo(x + s * 0.30, y - s * 0.52)
    q.quadTo(x + s * 0.62, y - s * 0.62, x + s * 0.80, y - s * 0.50)
    q.quadTo(x + s * 0.62, y - s * 0.40, x + s * 0.34, y - s * 0.40)
    q.close()
    FILLP(c, q, "#8A6A30", 255, 1.0, 190)
    c.drawOval(skia.Rect.MakeLTRB(x - s * 0.42, y - s * 0.62, x + s * 0.42, y - s * 0.48), PT("#3A2A12"))
    fl, lean, br = flicker(t, seed + 3.3)
    fx0, fy0 = x + s * 0.80, y - s * 0.52
    if lit > 0.02:
        fh = s * 0.62 * fl * lit
        PN.glow(c, fx0, fy0 - fh * 0.5, s * 3.6 * lit + 30, "#FFB454", 0.34 * br * lit)
        c.drawPath(_flame_path(fx0, fy0, fh, s * 0.26, lean * fh * 0.25), PT("#FF9A3A", 235))
        c.drawPath(_flame_path(fx0, fy0, fh * 0.78, s * 0.16, lean * fh * 0.18), PT("#FFD66B", 250))
        c.drawPath(_flame_path(fx0, fy0, fh * 0.42, s * 0.08, 0), PT("#FFF6D6", 255))
    return fx0, fy0 - s * 0.2, br


def dust_motes(c, t, x0, y0, x1, y1, n=18, seed=5, a=0.7, size=2.2, drift=(5.0, 3.0), col="#FFF3D0"):
    """Dikdörtgen içinde süzülen toz zerreleri (srcover; parıltılı)."""
    rs = _RS(seed)
    w, h = max(1.0, x1 - x0), max(1.0, y1 - y0)
    for k in range(n):
        d = 0.5 + 0.7 * rs.rand()
        px = x0 + (rs.rand() * w + t * drift[0] * d + math.sin(t * 0.5 + k) * 10 * d) % w
        py = y0 + (rs.rand() * h + t * drift[1] * d + math.cos(t * 0.37 + k * 1.7) * 8 * d) % h
        tw = 0.35 + 0.65 * abs(math.sin(t * 0.9 + k * 2.1))
        r = size * (0.6 + 0.8 * rs.rand())
        c.drawCircle(px, py, r, PT(col, int(255 * clamp(a * tw))))


def window_light(f, x, y, w, h, t, dx=260.0, y_floor=Y_FL + 120, col="#FFE9A8", a=0.16, seed=1, cross=True, patch=True, dust=18, drift=24.0, night=False, part="all", patch_h=96):
    """Pencereden süzülen ışık huzmesi. (x,y,w,h) = pencere açıklığı (x orta). Huzme dx kadar eğik iner (yavaşça kayar: drift), zeminde pencere şeklinde
    ışık lekesi + çıta gölgeleri (cross), toz zerreleri huzmenin içinde süzülür. night=True: soğuk ay ışığı. part: 'all' | 'shaft' (hava) | 'patch' (zemin lekesi)."""
    c = f.c
    col = "#BFD0F5" if night else col
    a = a * (0.55 if night else 1.0)
    sl = dx + drift * math.sin(t * 0.13 + seed)
    br = 0.88 + 0.12 * math.sin(t * 0.29 + seed * 2.0) * math.sin(t * 0.11 + seed)     # bulut geçişi
    x0, x1 = x - w / 2, x + w / 2
    if part in ("all", "shaft"):
        shaft = sk.poly_path([(x0, y), (x1, y), (x1 + sl, y_floor), (x0 + sl, y_floor)])
        c.drawPath(shaft, LGP((0, y), (0, y_floor), [(col, 0.0, int(255 * a * 1.5 * br)), (col, 0.55, int(255 * a * 0.75 * br)), (col, 1.0, int(255 * a * 0.30 * br))]))
        nb = 3 if cross else 2
        for i in range(nb):
            u0, u1 = (i + 0.10) / nb, (i + 0.90) / nb
            ax, bx = x0 + w * u0, x0 + w * u1
            q = sk.poly_path([(ax, y), (bx, y), (bx + sl, y_floor), (ax + sl, y_floor)])
            c.drawPath(q, LGP((0, y), (0, y_floor), [(col, 0.0, int(255 * a * 0.7 * br)), (col, 1.0, int(255 * a * 0.10 * br))]))
        if dust:
            dust_motes(c, t, min(x0, x0 + sl) - 10, y + 30, max(x1, x1 + sl) + 10, y_floor, n=dust, seed=seed + 11, a=0.7 * (0.6 if night else 1.0), size=2.0, col=col if night else "#FFF3D0")
    if patch and part in ("all", "patch"):
        pw = w * 1.05
        px0 = x0 + sl * 1.02
        yp0, yp1 = y_floor, y_floor + patch_h
        pp = sk.poly_path([(px0, yp0), (px0 + pw, yp0), (px0 + pw + sl * 0.26, yp1), (px0 + sl * 0.26, yp1)])
        c.drawPath(pp, PT(col, int(255 * a * 1.9 * br)))
        if cross:
            mid = px0 + pw / 2
            c.drawPath(sk.poly_path([(mid - 5, yp0), (mid + 5, yp0), (mid + 5 + sl * 0.26, yp1), (mid - 5 + sl * 0.26, yp1)]), PT("#2A1608", 52))
            ym = yp0 + (yp1 - yp0) * 0.45
            c.drawRect(skia.Rect.MakeLTRB(px0 + sl * 0.12, ym - 4, px0 + pw + sl * 0.12, ym + 4), PT("#2A1608", 50))


# ═════════════════════════════ kâğıt, belge, tüy kalem, hokka, mühür ═════════════════════════════
@functools.lru_cache(maxsize=8)
def _paper(seed, tone, w=1100, h=760):
    return PP.paper_image(w, h, seed, tone, "deckle", (), 44, 1.0)


@functools.lru_cache(maxsize=6)
def _script_img(seed, n, w=1100, h=760, ink="#3A2616"):
    """Okunmaz el yazısı: n satır (kıvrık kısa vuruşlardan sözcükler), başlık satırı. RGBA görüntü (belge uzayı w×h; orijin sol-üst)."""
    fr = sk.Frame(w, h)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    rs = _RS(seed * 977 + n)
    L, Rr = 150, w - 150
    # başlık
    pth = skia.Path()
    xx = w * 0.30
    pth.moveTo(xx, 88)
    while xx < w * 0.70:
        xx += 5
        pth.lineTo(xx, 88 + 5 * math.sin(xx * 0.45) + rs.normal(0, 0.8))
    c.drawPath(pth, STK("#2A1608", 5.2, 230))
    top, step = 150, (h - 150 - 190) / max(1, n - 1) if n > 1 else 40
    for i in range(n):
        y = top + i * min(step, 40)
        x = L + (36 if i == 0 or rs.rand() < 0.12 else 0)
        end = Rr - (rs.uniform(30, 260) if (i == n - 1 or rs.rand() < 0.15) else rs.uniform(0, 30))
        while x < end:
            wl = rs.uniform(26, 86)
            if x + wl > end:
                wl = end - x
                if wl < 12:
                    break
            p = skia.Path()
            p.moveTo(x, y)
            k = 0.0
            while k < wl:
                k += 5
                p.lineTo(x + k, y + 5.0 * math.sin((x + k) * 0.42 + i) * rs.uniform(0.5, 1.2) + rs.normal(0, 0.9) - (3.0 if rs.rand() < 0.08 else 0))
            c.drawPath(p, STK(ink, 3.4, int(rs.uniform(190, 235))))
            x += wl + rs.uniform(11, 20)
    return fr.surf.makeImageSnapshot()


def doc_sheet(f, x, y, scale, t=0.0, n=13, shown=None, seed=3, rot=-0.012, tone=(238, 228, 198), seal=True, seal_t=1.0, alpha=1.0, shadow=0.55, curl=0.0):
    """Masa üstünde belge (orijin = belge merkezi). `doc` türünün kâğıdıyla aynı (paper_image 1100×760, aynı ton/kenar) → zoomthru ile uyumlu.
    n = satır sayısı (13 madde), shown = görünen satır (None = hepsi; kesirli = o satır yazılıyor). Dönüş: yok."""
    c = f.c
    pp = _paper(seed, tone)
    pp.draw(f, x, y, rot=rot, scale=scale, alpha=alpha, shadow=shadow)
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(rot))
    c.scale(scale, scale)
    img = _script_img(seed, n)
    sh = n if shown is None else clamp(shown, 0, n)
    c.save()
    c.translate(-550, -380)
    full = int(math.floor(sh))
    frac = sh - full
    top, step = 150.0, min((760 - 150 - 190) / max(1, n - 1), 40.0)
    # başlık her zaman; satırlar: üstten full satırlar tam, sıradaki kesirli (soldan açılır)
    ylim = top + (full - 1) * step + step * 0.55 if full >= 1 else 120
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, 0, 1100, ylim if sh < n else 760))
    p_ = skia.Paint(AntiAlias=True)
    p_.setAlphaf(alpha)
    c.drawImage(img, 0, 0, LIN, p_)
    c.restore()
    if sh < n and frac > 0.01:
        ycur = top + full * step
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(150, ycur - step * 0.55, 150 + (1100 - 300) * frac, ycur + step * 0.45))
        c.drawImage(img, 0, 0, LIN, p_)
        c.restore()
    c.restore()
    if seal:
        CM.wax_seal(f, 330, 262, 58, "#A52A1C", alpha=alpha, t=seal_t, palle=True)
    c.restore()


def quill(c, x, y, ang=-62.0, s=1.0, alpha=1.0):
    """Tüy kalem (uç x,y noktasında; ang = derece, yukarı-sağa yatık): gövde + tüy yelpazesi + ince mürekkep ucu."""
    c.save()
    c.translate(x, y)
    c.rotate(ang + 90.0)
    c.scale(s, s)
    # sap
    c.drawLine(0, 0, 0, -120, STK("#8A7048", 3.0, int(255 * alpha)))
    # tüy: iki yüz
    for sgn, col in ((-1, "#EDE4CC"), (1, "#DDD2B4")):
        p = skia.Path()
        p.moveTo(0, -42)
        p.cubicTo(sgn * 22, -66, sgn * 24, -112, sgn * 2, -168)
        p.cubicTo(sgn * 4, -120, sgn * 2, -80, 0, -42)
        p.close()
        c.drawPath(p, PT(col, int(255 * alpha)))
        c.drawPath(p, STK(INK, 1.0, int(170 * alpha)))
        for q in range(6):
            yy = -60 - q * 16
            c.drawLine(sgn * 1.5, yy, sgn * (15 - q * 1.6), yy - 9, STK("#8A7A5A", 0.8, int(110 * alpha)))
    c.drawLine(0, 0, 0, -26, STK("#1A1008", 1.6, int(255 * alpha)))
    c.restore()


def inkwell(c, x, y, s=1.0, t=0.0):
    """Hokka: koyu kap + pirinç kapak + yarım batmış tüy için karanlık ağız. (x,y) taban ortası."""
    w, h = 24 * s, 24 * s
    c.drawOval(skia.Rect.MakeLTRB(x - w * 0.75, y - 4 * s, x + w * 0.75, y + 4 * s), PT("#000000", 70))
    p = skia.Path()
    p.moveTo(x - w * 0.62, y)
    p.quadTo(x - w * 0.75, y - h * 0.6, x - w * 0.45, y - h)
    p.lineTo(x + w * 0.45, y - h)
    p.quadTo(x + w * 0.75, y - h * 0.6, x + w * 0.62, y)
    p.close()
    FILLP(c, p, "#262020", 255, 1.2, 190, shader=LGP((x - w, 0), (x + w, 0), [("#5A4A44", 0.0), ("#262020", 0.45), ("#0E0A0A", 1.0)]))
    c.drawOval(skia.Rect.MakeLTRB(x - w * 0.46, y - h - 3 * s, x + w * 0.46, y - h + 4 * s), PT("#0A0606"))
    c.drawOval(skia.Rect.MakeLTRB(x - w * 0.46, y - h - 3 * s, x + w * 0.46, y - h + 4 * s), STK("#B8903A", 1.6 * s, 230))


# ═════════════════════════════ masa (ters perspektif: tabla izleyiciye eğik) ═════════════════════════════
class TGeom:
    """Masa tablası geometrisi: ön kenar (x..x+w, y), derinlik; arka kenar daralır (ters perspektif değil, hafif yakınsama). pt(u,v): u 0..1 genişlik, v 0..1 derinlik."""

    def __init__(self, x, y, w, depth=130.0, inset=0.055):
        self.x, self.y, self.w, self.depth, self.inset = x, y, w, depth, inset

    def pt(self, u, v):
        ins = self.inset * self.w * v
        return self.x + ins + u * (self.w - 2 * ins), self.y - v * self.depth

    def sc(self, v):
        return 1.0 - 2.0 * self.inset * v


def table_top(c, g, T, cloth=("#8E2A30", "#D2A33E"), seed=0):
    """Örtülü masa tablası (vektör, zumda keskin): bordür şeridi, baklava deseni, ön kenarda saçak."""
    quad = sk.poly_path([g.pt(0, 0), g.pt(1, 0), g.pt(1, 1), g.pt(0, 1)])
    c1, c2 = cloth
    sh = LGP((0, g.y - g.depth), (0, g.y), [(mix(T(c1), "#000000", 0.20), 0.0), (T(c1), 0.55), (mix(T(c1), "#FFFFFF", 0.07), 1.0)])
    c.drawPath(quad, sh)
    # bordür
    inner = sk.poly_path([g.pt(0.045, 0.10), g.pt(0.955, 0.10), g.pt(0.955, 0.90), g.pt(0.045, 0.90)])
    c.drawPath(inner, STK(T(c2), 3.2, 230))
    inner2 = sk.poly_path([g.pt(0.06, 0.18), g.pt(0.94, 0.18), g.pt(0.94, 0.82), g.pt(0.06, 0.82)])
    c.drawPath(inner2, STK(T(c2), 1.1, 150))
    # baklava deseni
    n = 9
    for i in range(n):
        u = (i + 0.5) / n
        for v in (0.30, 0.65):
            a, b, cc, d = g.pt(u - 0.03, v), g.pt(u, v + 0.10), g.pt(u + 0.03, v), g.pt(u, v - 0.10)
            c.drawPath(sk.poly_path([a, b, cc, d]), PT(T(c2), 70))
    INKP(c, quad, 1.5, 200)
    # ön kenar saçak
    x0, y0 = g.pt(0, 0)
    x1, _ = g.pt(1, 0)
    k = int(g.w / 9)
    for i in range(k):
        xx = x0 + (x1 - x0) * (i + 0.5) / k
        c.drawLine(xx, y0, xx + 0.4, y0 + 9, STK(T(c2), 1.4, 220))


def table_front(c, g, y_floor, T, cloth=("#8E2A30", "#D2A33E"), apron=30, leg="#6E4524"):
    """Masa ön yüzü: sarkan örtü (kıvrımlı), saçak, iki bacak. Figürün bacaklarını örter (figürden SONRA çizilir)."""
    x0, y0 = g.pt(0, 0)
    x1, _ = g.pt(1, 0)
    c1, c2 = cloth
    # bacaklar (örtünün altında)
    for lx in (x0 + 10, x1 - 10):
        p = skia.Path()
        p.moveTo(lx - 10, y0 + apron)
        p.lineTo(lx + 10, y0 + apron)
        p.quadTo(lx + 6, y0 + apron + (y_floor - y0 - apron) * 0.5, lx + 8, y_floor)
        p.lineTo(lx - 8, y_floor)
        p.quadTo(lx - 6, y0 + apron + (y_floor - y0 - apron) * 0.5, lx - 10, y0 + apron)
        FILLP(c, p, T(leg), 255, 1.3, 190, shader=LGP((lx - 10, 0), (lx + 10, 0), [(mix(T(leg), "#FFFFFF", 0.18), 0.0), (T(leg), 0.45), (mix(T(leg), "#000000", 0.28), 1.0)]))
        for yy in (y0 + apron + 22, y0 + apron + (y_floor - y0 - apron) * 0.55):
            c.drawOval(skia.Rect.MakeLTRB(lx - 12, yy - 5, lx + 12, yy + 5), PT(T(mix(leg, "#000000", 0.1))))
            c.drawOval(skia.Rect.MakeLTRB(lx - 12, yy - 5, lx + 12, yy + 5), STK(INK, 1.0, 170))
        c.drawOval(skia.Rect.MakeLTRB(lx - 14, y_floor - 5, lx + 14, y_floor + 3), PT("#000000", 60))
    SOFT(c, (x0 + x1) / 2 + 20, y_floor + 2, (x1 - x0) * 0.55, 12, "#000000", 70)
    # sarkan örtü
    path = skia.Path()
    path.moveTo(x0, y0)
    path.lineTo(x1, y0)
    n = 14
    for i in range(n + 1):
        xx = x1 - (x1 - x0) * i / n
        path.lineTo(xx, y0 + apron + (5 if i % 2 else -3))
    path.close()
    c.drawPath(path, LGP((0, y0), (0, y0 + apron), [(T(c1), 0.0), (mix(T(c1), "#000000", 0.30), 1.0)]))
    for i in range(1, n):
        xx = x0 + (x1 - x0) * i / n
        c.drawLine(xx, y0 + 1, xx + 0.5, y0 + apron - 1, STK("#1A0A08", 1.3, 80 + (i % 2) * 40, False))
        c.drawLine(xx + 3, y0 + 2, xx + 3, y0 + apron * 0.55, STK("#FFFFFF", 1.6, 24, False))
    c.drawLine(x0, y0 + apron - 8, x1, y0 + apron - 8, STK(T(c2), 2.2, 200))
    INKP(c, path, 1.3, 190)


def table(f, x, y, w, depth=130.0, y_floor=None, cloth=("#8E2A30", "#D2A33E"), T=None, front=True, top=True, apron=30):
    """Yeniden kullanılabilir masa (tuval koordinatı: x = sol uç, y = tabla ÖN kenarı). Dönüş: TGeom (nesne yerleştirmek için `g.pt(u, v)`)."""
    T = T or OTint("day")
    g = TGeom(x, y, w, depth)
    if top:
        table_top(f.c, g, T, cloth)
    if front:
        table_front(f.c, g, y_floor if y_floor is not None else y + 116, T, cloth, apron)
    return g


# ═════════════════════════════ tunç kapı (iki kanat, kabartma paneller) ═════════════════════════════
@functools.lru_cache(maxsize=24)
def _bronze_leaf(w, h, seed, rows=5, res=1):
    """Tek kanat sprite'ı: tunç degrade + panel çerçeveleri + kabartma (yuvarlak madalyon, rozet, haçvari) + perçin sırası. Orijin sol-üst. res: çözünürlük çarpanı (zumda keskin)."""
    pad = 6
    fr = sk.Frame(int((w + 2 * pad) * res), int((h + 2 * pad) * res))
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    c.scale(res, res)
    c.translate(pad, pad)
    base = "#8A5E32"
    c.drawRect(skia.Rect.MakeLTRB(0, 0, w, h), LGP((0, 0), (w, 0), [("#D8A868", 0.0), ("#9A6A38", 0.30), ("#7A4E26", 0.70), ("#4A2C14", 1.0)]))
    # yatay hafif fırçalama
    rs = _RS(seed)
    for i in range(70):
        yy = rs.uniform(2, h - 2)
        c.drawLine(2, yy, w - 2, yy + rs.uniform(-1, 1), STK("#2A1608" if rs.rand() < 0.5 else "#F0C98A", rs.uniform(0.5, 1.1), int(rs.uniform(14, 38)), False))
    ph = (h - 36) / rows
    for r_ in range(rows):
        y0 = 18 + r_ * ph
        px0, px1, py0, py1 = 16, w - 16, y0 + 6, y0 + ph - 6
        # panel çerçevesi: çift çizgi + iç gölge
        c.drawRect(skia.Rect.MakeLTRB(px0, py0, px1, py1), PT("#5C3A1C", 150))
        c.drawRect(skia.Rect.MakeLTRB(px0 + 5, py0 + 5, px1 - 5, py1 - 5), LGP((0, py0), (0, py1), [("#B88848", 0.0), ("#8A5C30", 0.5), ("#5C3A1C", 1.0)]))
        c.drawRect(skia.Rect.MakeLTRB(px0, py0, px1, py1), STK("#E0B070", 1.6, 190, False))
        c.drawRect(skia.Rect.MakeLTRB(px0 + 5, py0 + 5, px1 - 5, py1 - 5), STK("#2A1608", 1.6, 220, False))
        # kabartma: ortada madalyon + yanlarda rozetler (soyut)
        cx_, cy_ = (px0 + px1) / 2, (py0 + py1) / 2
        rr = min(px1 - px0, py1 - py0) * 0.30
        kind = (r_ + seed) % 3
        c.drawCircle(cx_ + 2, cy_ + 3, rr, PT("#2A1608", 120))
        c.drawCircle(cx_, cy_, rr, LGP((cx_ - rr, cy_ - rr), (cx_ + rr, cy_ + rr), [("#EBC587", 0.0), ("#B8884A", 0.5), ("#6A4220", 1.0)]))
        c.drawCircle(cx_, cy_, rr, STK("#2A1608", 1.4, 200))
        c.drawCircle(cx_, cy_, rr * 0.72, STK("#2A1608", 1.0, 150))
        if kind == 0:
            for k in range(8):
                a_ = k * math.pi / 4
                c.drawLine(cx_ + math.cos(a_) * rr * 0.2, cy_ + math.sin(a_) * rr * 0.2, cx_ + math.cos(a_) * rr * 0.68, cy_ + math.sin(a_) * rr * 0.68, STK("#2A1608", 2.2, 180))
            c.drawCircle(cx_, cy_, rr * 0.16, PT("#E8C58A"))
        elif kind == 1:
            c.drawLine(cx_, cy_ - rr * 0.6, cx_, cy_ + rr * 0.6, STK("#2A1608", 3.0, 190))
            c.drawLine(cx_ - rr * 0.6, cy_, cx_ + rr * 0.6, cy_, STK("#2A1608", 3.0, 190))
            c.drawCircle(cx_, cy_, rr * 0.2, PT("#E8C58A"))
        else:
            pth = skia.Path()
            pth.moveTo(cx_, cy_ - rr * 0.6)
            pth.cubicTo(cx_ + rr * 0.9, cy_ - rr * 0.2, cx_ + rr * 0.3, cy_ + rr * 0.7, cx_, cy_ + rr * 0.4)
            pth.cubicTo(cx_ - rr * 0.3, cy_ + rr * 0.7, cx_ - rr * 0.9, cy_ - rr * 0.2, cx_, cy_ - rr * 0.6)
            c.drawPath(pth, PT("#D8A868", 230))
            c.drawPath(pth, STK("#2A1608", 1.5, 200))
        # iç köşe perçinleri
        for (qx, qy) in ((px0 + 12, py0 + 12), (px1 - 12, py0 + 12), (px0 + 12, py1 - 12), (px1 - 12, py1 - 12)):
            c.drawCircle(qx, qy, 3.2, PT("#E0B070"))
            c.drawCircle(qx, qy, 3.2, STK("#2A1608", 0.9, 200))
    # dış çerçeve
    c.drawRect(skia.Rect.MakeLTRB(0, 0, w, h), STK(INK, 3.0, 230, False))
    c.drawRect(skia.Rect.MakeLTRB(5, 5, w - 5, h - 5), STK("#E8C58A", 1.2, 160, False))
    return fr.surf.makeImageSnapshot(), pad


def door_bronze(f, x, y, h, open_amount=0.0, w=None, seed=1, light=True, t=0.0, gap_col="#FFE2A0"):
    """Tunç kapı (iki kanat, kabartma paneller). x = kapı orta çizgisi, y = eşik, h = yükseklik, w yoksa 0,56·h. open_amount 0 = kapalı … 1 = tam açık:
    kanatlar menteşede (dış kenarlar) döner → ekranda yatay daralır, serbest kenar hafif kısalır; açıklıktan arkadaki sıcak ışık görünür.
    Dönüş: (sol kanat serbest kenar x, sağ kanat serbest kenar x, kapalılık 0..1)."""
    c = f.c
    w = w or h * 0.56
    lw = w / 2.0
    oa = clamp(open_amount)
    ew = lw * max(0.08, math.cos(oa * 1.32))      # kanadın ekrandaki genişliği
    sk_ = 0.06 * oa * h                            # serbest kenarın kısalması (uzaklaşma)
    top = y - h
    if oa > 0.01:
        if light:
            c.drawRect(skia.Rect.MakeLTRB(x - lw, top, x + lw, y), LGP((0, top), (0, y), [("#2A1A10", 0.0), (gap_col, 0.55, 240), ("#8A5A30", 1.0)]))
        else:
            c.drawRect(skia.Rect.MakeLTRB(x - lw, top, x + lw, y), PT("#1A0F08"))
    hint = FA.SCALE_HINT
    res = 1 if hint < 1.6 else (2 if hint < 3.2 else 4)
    img, pad = _bronze_leaf(int(lw), int(h), seed, 5, res)
    for sgn in (-1, 1):
        hinge = x + sgn * lw
        far = hinge - sgn * ew
        q = sk.poly_path([(hinge, top), (far, top + sk_), (far, y - sk_), (hinge, y)])
        c.save()
        c.clipPath(q, skia.ClipOp.kIntersect, True)
        c.translate(hinge, top)
        c.scale(((ew / lw) if sgn < 0 else -(ew / lw)) / res, 1.0 / res)
        c.drawImage(img, -pad * res, -pad * res, LIN)
        c.restore()
        c.save()
        c.clipPath(q, skia.ClipOp.kIntersect, True)
        shd = LGP((hinge, 0), (far, 0), [("#FFFFFF", 0.0, 16), ("#000000", 1.0, int(80 * oa))])
        c.drawRect(skia.Rect.MakeLTRB(min(hinge, far) - 2, top - 2, max(hinge, far) + 2, y + 2), shd)
        c.restore()
        INKP(c, q, 2.4, 230)
    if oa < 0.25:
        c.drawLine(x, top + 2, x, y - 2, STK("#1A0F08", 3.0, 230, False))
    c.drawRect(skia.Rect.MakeLTRB(x - lw - 14, y - 2, x + lw + 14, y + 12), PT("#8E8576"))
    c.drawRect(skia.Rect.MakeLTRB(x - lw - 14, y - 2, x + lw + 14, y + 12), STK(INK, 1.4, 190))
    return x - lw + ew, x + lw - ew, 1.0 - oa


# ═════════════════════════════ siluet ve masa başı figürler ═════════════════════════════
_CF = {}
_SILCF = [None]
_BLIT0 = FA.blit if not getattr(FA.blit, "_oda_cf", False) else FA.blit._orig


def _blit_cf(c, spr, jx, jy, X, Y, ang=0.0, sx=1.0):
    """FA.blit yaması: siluet bağlamında (_SILCF) baş/ayakkabı sprite'larına da renk filtresi uygular (FA.draw_fig bunları süzmez)."""
    cf = _SILCF[0]
    if cf is None:
        return _BLIT0(c, spr, jx, jy, X, Y, ang, sx)
    ix, iy = spr.ox + jx, spr.oy + jy
    pt = skia.Paint(AntiAlias=False)
    pt.setColorFilter(cf)
    c.save()
    c.translate(X, Y)
    if ang:
        c.rotate(ang)
    if sx != 1.0:
        c.scale(sx, 1.0)
    c.drawImage(spr.img, -ix, -iy, LIN, pt)
    c.restore()


_blit_cf._oda_cf = True
_blit_cf._orig = _BLIT0
FA.blit = _blit_cf


def flat_cf(color="#1A1008"):
    if color not in _CF:
        _CF[color] = skia.ColorFilters.Blend(C(color), skia.BlendMode.kSrcIn)
    return _CF[color]


def sil_actor(f, kind, x, y, h, t, action="idle", dir=1, seed=0, phase=0.0, color="#1A1008", rim="#E8A860", rim_dir=1, rim_w=1.5, alpha=1.0, walker=None, prop=None, **p):
    """Siluet figür (yüz yok): düz koyu doldurma + ışığa dönük sıcak kenar ışığı (ofsetli ikinci geçiş). rim_dir=+1: ışık sağda (kenar ışığı sağ kenarda).
    walker=(hız) verilirse yürüyen figür (FA.walker), aksi hâlde FA.actor eylemi."""
    flat = flat_cf(color)
    warm = flat_cf(rim) if rim else None
    c = f.c
    rim_w = rim_w * 1.4 / max(1.0, FA.SCALE_HINT ** 0.6)
    for off, cf in ((rim_w, warm), (0.0, flat)):
        if cf is None:
            continue
        c.save()
        c.translate(off * rim_dir * 0.9, -off * 0.5)
        _SILCF[0] = cf
        try:
            if walker is not None:
                FA.walker(f, kind, x, y, h, t, speed=walker, dir=dir, seed=seed, phase=phase, alpha=alpha, cf=cf, prop=prop, **p)
            else:
                FA.actor(f, kind, x, y, h, t, action=action, dir=dir, seed=seed, phase=phase, alpha=alpha, cf=cf, prop=prop, **p)
        finally:
            _SILCF[0] = None
        c.restore()


def act_sit_talk(kit, T, phase=0.0, t0=0.0, energy=1.0, **_):
    """Masa başında OTURAN konuşma: bir el masada, öteki el jestle kalkıp iner; baş hafif sallanır, gövde öne-arkaya."""
    hb = kit.B["hb"]
    ph = phase * 6.283
    cyc = 3.1 / max(0.4, energy)
    u = ((T - t0 + phase * 2.0) % cyc) / cyc
    k = math.sin(math.pi * min(1.0, u * 1.25)) ** 1.4 if u < 0.8 else 0.0
    wob = math.sin(T * 5.3 + ph) * 0.004 * k

    def arms(sho):
        far = ("ik", (0.215 * hb, (FA.DESK_Y - 0.003) * hb))
        near = ("ik", ((0.28 + 0.13 * k + wob) * hb, (FA.DESK_Y - 0.035 - 0.15 * k) * hb))
        return far, near, "open", "open"
    lean = 6.0 + 3.0 * k + 1.5 * math.sin(T * 0.8 + ph)
    head = 13.0 + 3.5 * math.sin(T * 1.7 + ph) * (0.5 + 0.5 * k) - 2.0 * k
    p = FA._sit_base(kit, T, phase, lean, head, arms)
    p.extra = None
    return p


def act_sit_listen(kit, T, phase=0.0, t0=0.0, **_):
    """Oturan dinleyen: iki el masada/dizde, baş hafif eğik, ara sıra başını sallar."""
    hb = kit.B["hb"]
    ph = phase * 6.283
    nod = max(0.0, math.sin(T * 0.9 + ph)) ** 6

    def arms(sho):
        return ("ik", (0.22 * hb, (FA.DESK_Y - 0.003) * hb)), ("ik", (0.33 * hb, (FA.DESK_Y - 0.004) * hb)), "open", "fist"
    p = FA._sit_base(kit, T, phase, 5.0, 14.0 + 4.0 * nod, arms)
    p.extra = None
    return p


def act_sit_read(kit, T, phase=0.0, t0=0.0, **_):
    """Oturan okuyan: iki el masa üstünde kâğıdı tutar, baş aşağı eğik, yavaş kayar."""
    hb = kit.B["hb"]
    ph = phase * 6.283
    sl = 0.03 * math.sin(T * 0.5 + ph)

    def arms(sho):
        return ("ik", ((0.27 + sl) * hb, (FA.DESK_Y - 0.01) * hb)), ("ik", ((0.35 + sl) * hb, (FA.DESK_Y - 0.012) * hb)), "open", "open"
    p = FA._sit_base(kit, T, phase, 11.0, 26.0 + 2.0 * math.sin(T * 0.7 + ph), arms)
    p.extra = None
    return p


SEATED_ACTS = {}


def seated_act(name):
    if not SEATED_ACTS:
        SEATED_ACTS.update(write=FA.act_write, count=FA.act_count, talk=act_sit_talk, listen=act_sit_listen, read=act_sit_read)
    return SEATED_ACTS[name]


def seated(f, kind, x, y, h, t, action="write", dir=1, seed=0, phase=0.0, sil=None, rim="#E8A860", rim_dir=1, t0=0.0, alpha=1.0, energy=1.0, desk_top=False, **stil):
    """Masa başında oturan figür (masa/sandalye odanın kendi çizimidir; FA masası ÇİZİLMEZ). action: write | count | idle(oturan) …
    sil=renk → siluet. Dönüş: act_write ek bilgisi (satır, ilerleme) — belge yazılışını elle eşlemek için."""
    kit, bh = FA.kit_for(kind, seed, h, **stil)
    fn = seated_act(action)
    pz = fn(kit, t, phase=phase, t0=t0, **({'energy': energy} if action == 'talk' else {}))
    ex = dict(pz.extra) if getattr(pz, "extra", None) else {}
    FA.cloth_for(kit, pz, t, phase * 6.28, lag=0.0, wave=0.0)
    c = f.c
    rw = 2.1 / max(1.0, FA.SCALE_HINT ** 0.6)
    passes = [(0.0, None)] if not sil else [(rw, flat_cf(rim)), (0.0, flat_cf(sil))]
    for off, cf in passes:
        c.save()
        c.translate(off * rim_dir * 0.9, -off * 0.5)
        c.save()
        FA.place_fig(c, x, y, h, bh, dir)
        _SILCF[0] = cf
        try:
            FA.draw_fig(c, kit, pz, alpha, cf)
        finally:
            _SILCF[0] = None
        if desk_top and cf is None and getattr(pz, "extra", None):
            FA.draw_desk_top(c, kit, pz, t, alpha)
        c.restore()
        c.restore()
    ex["s"] = h / bh
    ex["hb"] = kit.B["hb"]
    return ex


def lying_sil(f, x, y, t, scale=1.0, color="#1A1008", rim="#E8A860", rim_dir=1, breath=1.0):
    """Yatakta yatan kadın SİLÜETİ (yandan; baş solda yastıkta, örtü altında omuz/kalça/diz/ayak kabarıklıkları; yüz/ayrıntı yok): yavaş nefes.
    (x,y) = yastığın alt-sol köşesi (mindere değdiği çizgi)."""
    c = f.c
    b = 1.0 + 0.045 * math.sin(t * 1.15) * breath
    s = scale
    pts = [(40, 8), (46, -22), (64, -52), (96, -62), (136, -58), (176, -46), (214, -50), (252, -48), (292, -40), (330, -44), (366, -34), (398, -24), (410, -6), (410, 8)]

    def mound(dx, dy, col):
        q = [(x + (px * s) + dx, y + (py * s * (b if py < -4 else 1.0)) + dy) for px, py in pts]
        p = sk.smooth_path(q, True, 0.42)
        c.drawPath(p, PT(col))
        hd = skia.Path()
        hd.addOval(skia.Rect.MakeLTRB(x + 4 * s + dx, y - 64 * s + dy, x + 62 * s + dx, y - 12 * s + dy))
        c.drawPath(hd, PT(col))
        bn = skia.Path()
        bn.moveTo(x + 2 * s + dx, y - 40 * s + dy)
        bn.quadTo(x + 2 * s + dx, y - 78 * s + dy, x + 40 * s + dx, y - 72 * s + dy)
        bn.quadTo(x + 64 * s + dx, y - 58 * s + dy, x + 54 * s + dx, y - 36 * s + dy)
        bn.close()
        c.drawPath(bn, PT(col))
    if rim:
        mound(1.6 * rim_dir, -1.8, rim)
    mound(0, 0, color)


# ═════════════════════════════ sahne motoru ═════════════════════════════
class OLayer(PN.Layer):
    def _path(self, i):
        return os.path.join(PN.CACHE, f"oda_{self.world}_{self.tod}_{self.name}_{i}_{OVER}.png")


class Room:
    """Oda taban sınıfı. build() katmanları tanımlar; stack() çizim sırası; dyn_* canlı katmanlar; light() mum havuzu (ana katman koordinatı)."""
    name = "room"
    PW = 2600
    interior = True

    def __init__(self, variant, tod):
        self.variant = variant or ""
        self.tod = tod
        self.T = OTint(tod)
        self.layers = {}
        self.opts = {}
        self.key = f"{self.name}{self.variant}"
        self.build()

    def layer(self, name, f, width, draw, **kw):
        L = OLayer(self.key, name, f, width, draw, tod=self.tod, **kw)
        self.layers[name] = L
        return L

    def Lw(self, f):
        return int(W + (self.PW - W) * f + 500)

    def wx(self, x):
        """Ana düzlem x'ini duvar katmanı x'ine çevir (kamera x=960'da hizalı)."""
        return W / 2 + (x - W / 2) * F_WALL

    def build(self):
        pass

    def paths(self):
        return {"default": [(0.0, (1000, 0, 1.0)), (1.0, (self.PW - 1000, 0, 1.0))]}

    def get_path(self, name):
        ps = self.paths()
        if name in ps:
            return ps[name]
        if name == "out" and "in" in ps:
            return [(1.0 - fr, v) for fr, v in reversed(ps["in"])]
        if name == "in" and "out" in ps:
            return [(1.0 - fr, v) for fr, v in reversed(ps["out"])]
        return ps.get("default") or next(iter(ps.values()))

    def stack(self, ctx):
        return [("L", "wall", F_WALL), ("D", "dyn_wall", F_WALL), ("L", "main", 1.0), ("D", "dyn_main", 1.0), ("L", "front", 1.0), ("D", "dyn_front", 1.0), ("L", "fg", F_FG), ("D", "dyn_fg", F_FG)]

    def light(self, ctx):
        return None

    def post_light(self, ctx):
        pass

    def default_actors(self, ctx=None):
        return []

    def bake_all(self):
        n = 0
        for L in self.layers.values():
            for i in range(L.n_tiles()):
                L.tile(i)
                n += 1
        return n

    # boş varsayılanlar
    def dyn_wall(self, ctx):
        pass

    def dyn_main(self, ctx):
        pass

    def dyn_front(self, ctx):
        pass

    def dyn_fg(self, ctx):
        pass


ROOMS = {}
_ROOM_CACHE = {}


def get_room(name, variant, tod):
    key = (name, variant or "", tod)
    r = _ROOM_CACHE.get(key)
    if r is None:
        r = _ROOM_CACHE[key] = ROOMS[name](variant, tod)
    return r


# ═════════════════════════════ actors / props ═════════════════════════════
_ONE_SHOT = ("bow", "kneel", "point", "handshake", "threat", "write", "count")


def _anchor_t(ctx, a, default=0.0):
    if a is None:
        return default
    try:
        return ctx.cx.at(a)
    except Exception:
        return float(a) if isinstance(a, (int, float)) else default


def draw_actor(ctx, d):
    """actors öğesi: dict(kind, x, y, h, action, at, dir, seed, sil, prop, walk=(x_son, hız), t0, rise_at, …). x,y = ana düzlem koordinatı (ayak)."""
    f, t = ctx.f, ctx.t
    d = dict(d)
    kind = d.pop("kind", "halk")
    x, y, h = d.pop("x"), d.pop("y"), d.pop("h", 260)
    action = d.pop("action", "idle")
    at = d.pop("at", None)
    dirn = d.pop("dir", 1)
    seed = d.pop("seed", 0)
    phase = d.pop("phase", 0.0)
    sil = d.pop("sil", None)
    d.pop("layer", None)
    walk = d.pop("walk", None)
    rim_dir = d.pop("rim_dir", 1)
    if d.pop("seated", False):
        stil = {k: v for k, v in d.items() if k in FA.STIL_KEYS}
        seated(f, kind, x, y, h, t, action if action in ("write", "count", "talk", "listen", "read") else "listen", dirn, seed=seed, phase=phase,
               sil=(sil if isinstance(sil, str) else "#1A1008") if sil else None, rim_dir=rim_dir if rim_dir else (1 if dirn > 0 else -1), t0=_anchor_t(ctx, at, 0.0), energy=d.get("energy", 1.0), **stil)
        return
    t_at = _anchor_t(ctx, at, 0.0)
    for k in ("rise_at", "t_exit", "exit_at"):
        if k in d and not isinstance(d[k], (int, float)):
            d[k] = _anchor_t(ctx, d[k])
    if walk is not None:
        x1, v = walk[0], walk[1]
        wt = d.pop("walk_at", None)
        w0 = _anchor_t(ctx, wt, t_at) if wt is not None else t_at
        dist = x1 - x
        sp = abs(v)
        u = clamp((t - w0) * sp / max(1.0, abs(dist)))
        x = x + dist * u
        dirn = 1 if dist >= 0 else -1
        v_now = sp if 0 < u < 1 else 0.0
        al = 1.0
        if "fade_x" in d:
            xa_, xb_ = d.pop("fade_x")
            al = clamp((xb_ - x) / (xb_ - xa_)) if xb_ > xa_ else clamp((x - xb_) / (xa_ - xb_))
        if al <= 0.01:
            return
        if sil:
            sil_actor(f, kind, x, y, h, t, dir=dirn, seed=seed, phase=phase, color=sil if isinstance(sil, str) else "#1A1008", rim_dir=rim_dir, walker=v_now, alpha=al, **d)
        else:
            FA.walker(f, kind, x, y, h, t, speed=v_now, dir=dirn, seed=seed, phase=phase, alpha=al, **d)
        return
    if "fade_out_at" in d:
        fo = _anchor_t(ctx, d.pop("fade_out_at"))
        fd_ = d.pop("fade_out_dur", 1.6)
        al_ = 1.0 - smooth(clamp((t - fo) / fd_))
        if al_ <= 0.01:
            return
        d["alpha"] = al_
    if action == "handshake":
        FA.handshake(f, kind, d.pop("kind2", "tuccar"), x, y, h, t, gap=d.pop("gap", 0.6), t0=t_at if at is not None else d.pop("t0", 0.5), seedA=seed, seedB=d.pop("seed2", seed + 1))
        return
    if action in _ONE_SHOT and "t0" not in d and at is not None:
        d["t0"] = t_at
    if sil:
        sil_actor(f, kind, x, y, h, t, action=action, dir=dirn, seed=seed, phase=phase, color=sil if isinstance(sil, str) else "#1A1008", rim_dir=rim_dir, **d)
    else:
        FA.actor(f, kind, x, y, h, t, action=action, dir=dirn, seed=seed, phase=phase, **d)


def draw_prop(ctx, d):
    """props öğesi: dict(kind="candle"|"coins"|"book"|"scroll"|"quill"|"inkwell"|"doc"|"flask"|"goblet", x, y, h|s, …) — ana düzlem koordinatı (taban)."""
    f, c, t = ctx.f, ctx.c, ctx.t
    k = d.get("kind")
    x, y = d["x"], d["y"]
    if k == "candle":
        candle(f, x, y, d.get("h", 70), t, d.get("seed", 1), lit=d.get("lit", 1.0), holder=d.get("holder", True))
    elif k == "oil":
        oil_lamp(f, x, y, d.get("s", 30), t, d.get("seed", 1), lit=d.get("lit", 1.0))
    elif k == "inkwell":
        inkwell(c, x, y, d.get("s", 1.0), t)
    elif k == "quill":
        quill(c, x, y, d.get("ang", -62.0), d.get("s", 0.5))
    elif k == "doc":
        doc_sheet(f, x, y, d.get("scale", 0.2), t, n=d.get("n", 13), shown=d.get("shown"), seed=d.get("seed", 3), rot=d.get("rot", -0.012), seal=d.get("seal", True))
    elif k == "coins":
        draw_coins(c, x, y, d.get("n", 8), d.get("s", 1.0), t, d.get("seed", 1), d.get("glint", True))
    elif k == "book":
        draw_book(c, x, y, d.get("w", 70), d.get("hgt", 14), d.get("col", "#6A2E24"), d.get("open", False))
    elif k == "scroll":
        draw_scroll(c, x, y, d.get("w", 80), d.get("s", 1.0))
    elif k == "goblet":
        draw_goblet(c, x, y, d.get("s", 1.0))
    elif k == "flask":
        draw_flask(c, x, y, d.get("s", 1.0), t, d.get("col", "#6E9A8A"))


def draw_coins(c, x, y, n, s=1.0, t=0.0, seed=1, glint=True):
    """Florin yığını (yan yana istifli sütunlar) + zaman zaman ışıltı."""
    rs = _RS(seed)
    rx, ry, th = 13 * s, 4.6 * s, 4.0 * s
    cols = max(1, int(round(n / 5)))
    k = 0
    for ci in range(cols):
        cx_ = x + (ci - (cols - 1) / 2) * rx * 2.1
        hh = int(min(5, n - ci * 5)) if ci < cols - 1 or n % 5 == 0 else n % 5
        hh = max(1, min(5, n - ci * 5))
        for j in range(hh):
            yy = y - j * th
            c.drawOval(skia.Rect.MakeLTRB(cx_ - rx, yy - ry * 0.4, cx_ + rx, yy + ry), PT("#8A6422"))
            c.drawOval(skia.Rect.MakeLTRB(cx_ - rx, yy - ry * 1.2, cx_ + rx, yy + ry * 0.3), PT("#E8C25A"))
            c.drawOval(skia.Rect.MakeLTRB(cx_ - rx * 0.5, yy - ry * 1.0, cx_ + rx * 0.1, yy - ry * 0.1), PT("#FFF0B0", 150))
            c.drawOval(skia.Rect.MakeLTRB(cx_ - rx, yy - ry * 1.2, cx_ + rx, yy + ry * 0.3), STK("#3A2610", 0.8, 160))
        if glint:
            ph = (t * 0.7 + ci * 0.37 + rs.rand()) % 1.0
            if ph < 0.18:
                a = math.sin(ph / 0.18 * math.pi)
                gx, gy = cx_ + rx * 0.3, y - hh * th - ry
                c.drawLine(gx - 9 * s * a, gy, gx + 9 * s * a, gy, STK("#FFF6D0", 1.6, int(230 * a)))
                c.drawLine(gx, gy - 9 * s * a, gx, gy + 9 * s * a, STK("#FFF6D0", 1.6, int(230 * a)))
                PN.glow(c, gx, gy, 16 * s, "#FFE9A0", 0.5 * a)


def draw_book(c, x, y, w=70, hgt=14, col="#6A2E24", open_=False):
    """Kapalı (yığın) ya da açık kitap: (x,y) taban ortası."""
    if open_:
        for sg in (-1, 1):
            p = sk.poly_path([(x, y), (x + sg * w * 0.5, y - hgt * 0.4), (x + sg * w * 0.5, y - hgt * 1.5), (x, y - hgt * 1.0)])
            FILLP(c, p, "#EDE4C8", 255, 1.0, 170)
            for i in range(4):
                yy = y - hgt * (0.35 + i * 0.22)
                c.drawLine(x + sg * 4, yy, x + sg * w * 0.45, yy - hgt * 0.35, STK("#4A3A22", 0.8, 130))
    else:
        BOX(c, x - w / 2, y - hgt, x + w / 2, y, col, OTint("day"), ink=1.1)
        c.drawRect(skia.Rect.MakeLTRB(x - w / 2 + 3, y - hgt + 3, x + w / 2 - 3, y - 3), PT("#E8DDBC", 235))
        c.drawLine(x - w / 2 + 3, y - hgt + 3, x - w / 2 + 3, y - 3, STK(col, 2.0))
        c.drawLine(x - w / 2, y - hgt * 0.5, x + w / 2, y - hgt * 0.5, STK("#D2A33E", 1.0, 160))


def draw_scroll(c, x, y, w=80, s=1.0):
    """Sarılı parşömen rulosu (yan yatan)."""
    r = 7 * s
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - w / 2, y - 2 * r, x + w / 2, y), r, r)
    c.drawRRect(rr, PT("#E8DDBC"))
    c.drawRRect(rr, STK(INK, 1.0, 170))
    for e in (-1, 1):
        c.drawOval(skia.Rect.MakeLTRB(x + e * w / 2 - 4, y - 2 * r, x + e * w / 2 + 4, y), PT("#CDBE98"))
        c.drawOval(skia.Rect.MakeLTRB(x + e * w / 2 - 4, y - 2 * r, x + e * w / 2 + 4, y), STK(INK, 0.9, 170))
    c.drawLine(x - w * 0.08, y - 2 * r, x - w * 0.08, y, STK("#A52A1C", 2.4, 230))


def draw_goblet(c, x, y, s=1.0):
    p = skia.Path()
    p.moveTo(x - 9 * s, y - 36 * s)
    p.quadTo(x - 11 * s, y - 20 * s, x - 2 * s, y - 16 * s)
    p.lineTo(x - 2 * s, y - 5 * s)
    p.lineTo(x - 10 * s, y)
    p.lineTo(x + 10 * s, y)
    p.lineTo(x + 2 * s, y - 5 * s)
    p.lineTo(x + 2 * s, y - 16 * s)
    p.quadTo(x + 11 * s, y - 20 * s, x + 9 * s, y - 36 * s)
    p.close()
    FILLP(c, p, "#C4A04A", 255, 1.0, 190, shader=LGP((x - 10 * s, 0), (x + 10 * s, 0), [("#F4DE90", 0.0), ("#C4A04A", 0.5), ("#7A5A1E", 1.0)]))


def draw_flask(c, x, y, s=1.0, t=0.0, col="#6E9A8A"):
    """Damıtma/kimya şişesi: yuvarlak gövde + boyun + sıvı + kabarcık."""
    r = 20 * s
    p = skia.Path()
    p.addCircle(x, y - r, r)
    p.addRect(skia.Rect.MakeLTRB(x - 5 * s, y - r * 2 - 22 * s, x + 5 * s, y - r * 2 + 6 * s))
    c.drawPath(p, PT("#DDEAE6", 120))
    c.save()
    c.clipPath(p, skia.ClipOp.kIntersect, True)
    c.drawRect(skia.Rect.MakeLTRB(x - r, y - r * 1.05 + math.sin(t * 2.0) * 1.0, x + r, y), PT(col, 210))
    c.restore()
    INKP(c, p, 1.2, 190)
    for q in range(3):
        ph = (t * 0.6 + q / 3.0) % 1.0
        c.drawCircle(x + math.sin(ph * 7 + q) * 6 * s, y - 4 * s - ph * r * 1.7, (1.8 + 1.4 * ph) * s, PT("#FFFFFF", int(200 * (1 - ph))))


# ═════════════════════════════ çekim türü ═════════════════════════════
_FRAME_BAND = (150, 800)


def _band_for(z, frame):
    """frame=True: sabit (150,800); False: tam ekran (140→0..1080 değil: pano gibi 140,800); 'auto': zum 1,5→2,3 arasında tam ekrana açılır."""
    if frame is True:
        return (150, 800), 0.0
    if frame is False:
        return (140, 800), 1.0
    k = smooth(clamp((z - 1.55) / 0.85))
    by0 = 150 + (0 - 150) * k
    bh = 800 + (1080 - 800) * k
    return (by0, bh), k


@ckind("oda")
def k_oda(cx, room="oda1743", variant=None, tod=None, path=None, cams=None, actors=None, props=None, kick=None, caption=None, at=0.0, frame="auto", seed=1, **opts):
    """İç mekân dünyası. room: oda1743 | salon | banka | calisma | sakristi | bos | perde (variant=… ayrıntı için notlar_oda.md).
    tod: day | dusk | night (verilmezse mode'a göre). path: odanın adlı kamera yolu ('in','out','default',…); cams=[(çapa,(x,y,zoom)),…]
    actors=[dict(kind, x, y, h, action, at, dir, seed, sil, walk, prop, layer='back'|'front')], props=[dict(kind, x, y, …)]; oda parametreleri **opts ile (figure=, close_at=, thread_at= …)."""
    f = cx.f
    c = f.c
    night_theme = not TH.day
    tod = tod or ("night" if night_theme else "day")
    world = get_room(room, variant, tod)
    world.opts = opts
    world.actors_extra = actors            # None → odanın varsayılan figürleri; liste (boş dâhil) → onları kullan
    world.props_extra = props or []
    a = cx.amt(at, 0.9) if at else 1.0
    dur = max(cx.dur, 1e-3)
    if not cams and hasattr(world, "cams_for"):
        cams = world.cams_for(cx, path, opts)
    default = world.get_path(path or "default") if not cams else None
    pc = PN.PanoCam(cx, cams, default, dur)
    t_cam = clamp(cx.t, 0.0, dur)
    camx, camy, z = pc.at(t_cam)
    st = getattr(cx, "cam_state", None)
    if st is not None and not cams and not path:
        camx += st.x
        camy += st.y
        z *= st.zoom
    sh_ = getattr(world, "cam_shake", None)
    if sh_ is not None:
        shx, shy = sh_(cx, t_cam)
        camx += shx
        camy += shy
    band, kfull = _band_for(z, frame)
    # duvar arka planı (bant dışı)
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    if kfull < 0.999:
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(0, 0, W, band[0] + 2))
        CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
        c.restore()
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(0, band[0] + band[1] - 2, W, H))
        CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
        c.restore()
    ctx = PN.Ctx(f, cx, world, camx, camy, z, band, tod, a)
    ctx.band = band
    ctx.room = world
    ctx.opts = opts
    ctx.stations = []
    by0, bh = band
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, by0, W, by0 + bh))
    for item in world.stack(ctx):
        kind = item[0]
        fct = item[2] if len(item) > 2 else 1.0
        if kind == "L":
            L = world.layers.get(item[1])
            if L is None:
                continue
            ctx.xf(L.f)
            xa, xb = ctx.view(L.f)
            L.draw_view(c, xa, xb)
            ctx.end()
        else:
            ctx.xf(fct)
            xa, xb = ctx.view(fct)
            ctx.xa, ctx.xb = xa, xb
            getattr(world, item[1])(ctx)
            ctx.end()
    c.restore()
    # çerçeve: asma bantları + altın şerit (zum açıldıkça kaybolur)
    if kfull < 0.98:
        for yy in (by0 - 40, by0 + bh):
            FA.vine_band(f, yy, a)
            c.drawLine(-40, yy + (40 if yy < by0 else 0), W + 40, yy + (40 if yy < by0 else 0), f.paint(TH.gold, style="stroke", sw=2.6, alpha=0.9 * a))
    if kick:
        CM.kick(f, kick, W / 2, 104, alpha=cx.amt(at + 0.4, 0.8) * (1 - kfull), size=34, track=14)
    if caption:
        wd = sk.text_width(caption, "cap_i", 44) + 100
        cyy = by0 + bh - 70
        CM.tablet(f, W / 2 - wd / 2, cyy - 36, wd, 76, alpha=cx.amt(at + 0.8, 0.7) * (1 - kfull), corner=10)
        CM.ink(f, caption, W / 2, cyy + 14, face="cap_i", size=44, color=TH.fg, align="c", alpha=cx.amt(at + 0.8, 0.7) * (1 - kfull), emboss=False)
    world.post_light(ctx)
    if getattr(world, "finish", None) is not None and world.finish(ctx):
        af = getattr(world, "after_finish", None)
        if af is not None:
            af(ctx)
        return
    lt = world.light(ctx)
    forced = getattr(world, "always_lit", False) and TH.day
    if forced:
        _th = (TH.mode, TH.perde)
        TH.set("night", TH.perde)
    if tod == "night" or forced or (lt is not None and lt[3] > 0 and tod != "day"):
        if lt is not None:
            lx, ly, lr, lk = lt
            sx, sy = ctx.to_screen(1.0, lx, ly)
            spread = clamp((abs(sx - W / 2) - 350) / 900.0, 0.0, 1.0)        # mum ekran dışına çıktıkça havuz genişler ve merkeze kayar
            sx = sx + (W / 2 - sx) * spread * 0.72
            sy = sy + (H / 2 - sy) * spread * 0.4
            base = CM.candle_light(cx.t, seed, base=(sx, sy), r=lr * z * (1.0 + 0.85 * spread), sway=2.0 * z)
            CM.finish(f, cx, motes_n=10, light=(base[0], base[1], base[2], base[3] * 1.0), k=lk)
        else:
            CM.finish(f, cx, motes_n=10, light=CM.candle_light(cx.t, seed, base=(W * 0.5, H * 0.5), r=1200.0, sway=6.0))
    else:
        CM.finish(f, cx, motes_n=14)
    if forced:
        TH.set(*_th)
    af = getattr(world, "after_finish", None)
    if af is not None:
        af(ctx)


# ───────────────────────────── ortak canlı katman parçaları ─────────────────────────────
def draw_extra(ctx, layer):
    """Çağıranın verdiği actors/props (layer='back' → dyn_main; 'front' → dyn_front)."""
    room = ctx.room
    lst = room.actors_extra if getattr(room, "actors_extra", None) is not None else room.default_actors(ctx)
    for d in sorted([a for a in lst if a.get("layer", "back") == layer], key=lambda q: q.get("y", 0)):
        x = d["x"]
        if ctx.xa - 700 < x < ctx.xb + 700:
            draw_actor(ctx, d)
    if layer == "back":
        for d in (getattr(room, "props_extra", None) or []):
            if ctx.xa - 300 < d["x"] < ctx.xb + 300:
                draw_prop(ctx, d)


# ═════════════════════════════ statik süs/mobilya çizimleri (kareaş pişirme; ortak) ═════════════════════════════
def cornice(c, xa, xb, y, T, col="#6A4228", plaster="#CDB98F", gold=True):
    """Tavan silmesi (üst): gölge + sıva silme + diş sırası + koyu ahşap kuşak + altın çizgi. y = silmenin üst kenarı."""
    GRAD_V(c, xa, y - 40, xb, y, [(T("#2A1A10"), 0.0), (T("#4A3220"), 1.0)])
    R(c, xa, y, xb, y + 22, T(mix(plaster, "#FFFFFF", 0.18)))
    c.drawLine(xa, y, xb, y, STK(INK, 1.3, 170, False))
    R(c, xa, y + 22, xb, y + 34, T(mix(col, "#FFFFFF", 0.1)))
    x = xa - (xa % 26)
    while x < xb:
        R(c, x, y + 22, x + 13, y + 34, T(mix(col, "#000000", 0.12)))
        x += 26
    R(c, xa, y + 34, xb, y + 52, T(col))
    HGRAD(c, xa, y + 34, xb, y + 52, [("#000000", 0.0, 0), ("#000000", 1.0, 0)])
    c.drawLine(xa, y + 52, xb, y + 52, STK(INK, 1.4, 190, False))
    if gold:
        c.drawLine(xa, y + 43, xb, y + 43, STK(T(GOLD), 2.0, 210, False))
    sh = LGP((0, y + 52), (0, y + 110), [("#1A0F06", 0.0, 90), ("#1A0F06", 1.0, 0)])
    c.drawRect(skia.Rect.MakeLTRB(xa, y + 52, xb, y + 110), sh)


def wainscot(c, xa, xb, y0, y1, T, col="#8A5A38", pw=170.0, seed=1):
    """Duvar lambrisi: korkuluk silmesi + yükseltilmiş paneller + süpürgelik. y0 = üst, y1 = alt (zemin)."""
    R(c, xa, y0, xb, y1, T(mix(col, "#000000", 0.18)))
    rail_h = 16
    WOOD(c, xa, y0, xb, y0 + rail_h, T, mix(col, "#FFFFFF", 0.10), seed, 1.3)
    R(c, xa, y1 - 20, xb, y1, T(mix(col, "#000000", 0.25)))
    c.drawLine(xa, y1 - 20, xb, y1 - 20, STK(INK, 1.2, 170, False))
    c.drawLine(xa, y1, xb, y1, STK(INK, 1.4, 200, False))
    i0 = int(math.floor(xa / pw)) - 1
    i1 = int(math.ceil(xb / pw)) + 1
    for i in range(i0, i1 + 1):
        px0, px1 = i * pw + 12, (i + 1) * pw - 12
        py0, py1 = y0 + rail_h + 10, y1 - 30
        BOX(c, px0, py0, px1, py1, mix(col, "#000000", 0.05), T, hl=0.12, sh=0.20, ink=1.2)
        BOX(c, px0 + 12, py0 + 12, px1 - 12, py1 - 12, mix(col, "#FFFFFF", 0.06), T, hl=0.10, sh=0.18, ink=1.0)
        rs = _RS(seed * 31 + i)
        for k in range(3):
            xx = rs.uniform(px0 + 18, px1 - 18)
            c.drawLine(xx, py0 + 14, xx + rs.uniform(-2, 2), py1 - 14, STK("#2A1A0C", 0.8, 38))


def draw_window(c, T, x, y, w, h, night=False, arch=True, shutters=True, glass=None, mullion=True, sill=True, stone=("#CBBB96", "#E6DAB8", "#D7C9A4", "#B8A880")):
    """İç mekân penceresi: taş çerçeve, kurşun çıtalı baklava camlar, ortada çıta, iç panjurlar, denizlik. (x orta, y üst). Gündüz parlak cam, gece koyu lacivert + ay."""
    x0, x1 = x - w / 2, x + w / 2
    r = w / 2
    yb = y + h

    def opening(grow):
        p = skia.Path()
        if arch:
            p.moveTo(x0 - grow, yb + grow)
            p.lineTo(x0 - grow, y + r)
            p.arcTo(skia.Rect.MakeLTRB(x0 - grow, y - grow, x1 + grow, y + 2 * r + grow), 180, 180, False)
            p.lineTo(x1 + grow, yb + grow)
        else:
            p.moveTo(x0 - grow, yb + grow)
            p.lineTo(x0 - grow, y - grow)
            p.lineTo(x1 + grow, y - grow)
            p.lineTo(x1 + grow, yb + grow)
        p.close()
        return p
    # taş çerçeve + iç şev (sol açık, sağ koyu)
    SOFT(c, x + 10, yb + 24, w * 0.9, 18, "#000000", 70)
    FILLP(c, opening(18), T(stone[0]), 255, 1.6, 200)
    FILLP(c, opening(9), T(stone[1] if not night else mix(stone[1], "#000000", 0.2)), 255, 1.0, 160)
    gc = glass or (("#F7F2DC", "#D6E4E4") if not night else ("#20325E", "#0F1A3A"))
    op = opening(0)
    c.save()
    c.clipPath(op, skia.ClipOp.kIntersect, True)
    GRAD_V(c, x0 - 4, y - 4, x1 + 4, yb + 4, [(gc[0], 0.0), (gc[1], 1.0)])
    if night:
        SOFT(c, x + w * 0.18, y + h * 0.28, w * 0.55, w * 0.55, "#D8E2FF", 120)
        c.drawCircle(x + w * 0.18, y + h * 0.28, w * 0.09, PT("#F2F4FF", 230))
        rs = _RS(11)
        for i in range(7):
            c.drawCircle(rs.uniform(x0, x1), rs.uniform(y, y + h * 0.5), rs.uniform(0.8, 1.6), PT("#F0F0FF", int(rs.uniform(110, 220))))
    else:
        SOFT(c, x - w * 0.15, y + h * 0.2, w * 0.7, w * 0.7, "#FFFFFF", 140)
    lead = "#3E3426" if not night else "#8A8466"
    step = 24
    k = -int((h + w) / step)
    while k < int((h + w) / step):
        c.drawLine(x0, y + k * step, x1, y + k * step + w * 1.0, STK(lead, 1.5, 170 if not night else 120, False))
        c.drawLine(x0, y + k * step + w * 1.0, x1, y + k * step, STK(lead, 1.5, 170 if not night else 120, False))
        k += 1
    if mullion:
        c.drawLine(x, y - 8, x, yb, STK(T(stone[3]), 8.0, 255, False))
        c.drawLine(x, y - 8, x, yb, STK(INK, 1.0, 180, False))
        ty = y + h * 0.42
        c.drawLine(x0, ty, x1, ty, STK(T(stone[3]), 8.0, 255, False))
        c.drawLine(x0, ty, x1, ty, STK(INK, 1.0, 180, False))
    # iç şev gölgesi (sağ)
    HGRAD(c, x1 - 22, y, x1 + 2, yb, [("#000000", 0.0, 0), ("#000000", 1.0, 70)])
    HGRAD(c, x0 - 2, y, x0 + 14, yb, [("#FFFFFF", 0.0, 40), ("#FFFFFF", 1.0, 0)])
    c.restore()
    INKP(c, op, 2.2, 230)
    if sill:
        FILLP(c, sk.poly_path([(x0 - 30, yb + 10), (x1 + 30, yb + 10), (x1 + 38, yb + 26), (x0 - 38, yb + 26)]), T(stone[2]), 255, 1.4, 200)
        R(c, x0 - 38, yb + 26, x1 + 38, yb + 34, T("#A8987A"))
        c.drawLine(x0 - 38, yb + 34, x1 + 38, yb + 34, STK(INK, 1.2, 170, False))
    if shutters:
        for sgn in (-1, 1):
            sx0 = x0 - 52 if sgn < 0 else x1 + 8
            sx1 = sx0 + 44
            BOX(c, sx0, y - 4, sx1, yb + 6, "#6E4A2A", T, ink=1.5)
            for yy in (y + h * 0.18, y + h * 0.5, y + h * 0.82):
                c.drawRect(skia.Rect.MakeLTRB(sx0 + 7, yy - 24, sx1 - 7, yy + 24), STK("#2A1A0C", 1.3, 170, False))
            c.drawLine(sx0 + 4, y + 18, sx0 + 4, yb - 14, STK("#FFFFFF", 1.4, 26, False))


def draw_hanging(c, T, x0, x1, y0, y1, col="#8E2A30", col2="#D2A33E", seed=1, pleat=22, damask=True, rod=True):
    """Duvar kumaşı / yatak arkalığı: sarkan, kıvrımlı (dikey ışık-gölge) kumaş + damasko motifleri + altın saçak + üst çubuk."""
    HGRAD(c, x0, y0, x1, y1, [(T(mix(col, "#FFFFFF", 0.10)), 0.0), (T(col), 1.0)])
    n = max(2, int((x1 - x0) / pleat))
    for i in range(n):
        a, b = x0 + (x1 - x0) * i / n, x0 + (x1 - x0) * (i + 1) / n
        HGRAD(c, a, y0, b, y1, [("#FFFFFF", 0.0, 34), ("#FFFFFF", 0.25, 0), ("#000000", 0.70, 0), ("#000000", 1.0, 58)])
        if i:
            c.drawLine(a, y0, a + 0.6, y1, STK("#1A0A08", 1.0, 60, False))
    if damask:
        rs = _RS(seed)
        for yy in np.arange(y0 + 40, y1 - 40, 54):
            for xx in np.arange(x0 + 26 + (int(yy / 54) % 2) * 27, x1 - 20, 54):
                p = sk.poly_path([(xx, yy - 17), (xx + 11, yy), (xx, yy + 17), (xx - 11, yy)])
                c.drawPath(p, PT(T(col2), 52))
                c.drawCircle(xx, yy, 2.4, PT(T(col2), 90))
    # saçak
    c.drawLine(x0, y1 - 6, x1, y1 - 6, STK(T(col2), 3.0, 230, False))
    xx = x0
    while xx < x1:
        c.drawLine(xx, y1 - 6, xx + 0.5, y1 + 6, STK(T(col2), 1.4, 220))
        xx += 4.0
    INKR(c, x0, y0, x1, y1, 1.3, 150)
    if rod:
        R(c, x0 - 14, y0 - 10, x1 + 14, y0 + 2, "#5A3A20")
        INKR(c, x0 - 14, y0 - 10, x1 + 14, y0 + 2, 1.2, 190)
        for ex in (x0 - 16, x1 + 16):
            c.drawCircle(ex, y0 - 4, 8, PT(T(GOLD)))
            c.drawCircle(ex, y0 - 4, 8, STK(INK, 1.0, 190))


def draw_tapestry(c, T, x, y0, w, h, seed=1, field="#2F5A5A", border="#B88A32", accent="#8E2A30", motif="tree"):
    """Goblen (duvar halısı): asma çubuğu + halkalar, bordür, millefleurs zemin, ortada ağaç/hayvan motifi, saçak."""
    x0, x1 = x - w / 2, x + w / 2
    y1 = y0 + h
    R(c, x0 - 16, y0 - 12, x1 + 16, y0 - 2, "#4A3220")
    INKR(c, x0 - 16, y0 - 12, x1 + 16, y0 - 2, 1.2, 190)
    for ex in (x0 - 18, x1 + 18):
        c.drawCircle(ex, y0 - 7, 8, PT(T(GOLD)))
        c.drawCircle(ex, y0 - 7, 8, STK(INK, 1.0, 190))
    for rx in np.arange(x0 + 14, x1, 46):
        c.drawOval(skia.Rect.MakeLTRB(rx - 5, y0 - 18, rx + 5, y0 + 2), STK("#5A4A30", 2.0, 220))
    BOX(c, x0, y0, x1, y1, border, T, ink=1.5, hl=0.10, sh=0.18)
    fx0, fy0, fx1, fy1 = x0 + 20, y0 + 20, x1 - 20, y1 - 20
    HGRAD(c, fx0, fy0, fx1, fy1, [(T(mix(field, "#FFFFFF", 0.08)), 0.0), (T(field), 0.5), (T(mix(field, "#000000", 0.22)), 1.0)])
    INKR(c, fx0, fy0, fx1, fy1, 1.2, 190)
    # bordür dama
    k = 0
    for xx in np.arange(x0 + 2, x1 - 2, 18):
        if k % 2 == 0:
            c.drawRect(skia.Rect.MakeLTRB(xx, y0 + 3, xx + 14, y0 + 17), PT(T("#233C8C"), 200))
            c.drawRect(skia.Rect.MakeLTRB(xx, y1 - 17, xx + 14, y1 - 3), PT(T("#233C8C"), 200))
        k += 1
    k = 0
    for yy in np.arange(y0 + 2, y1 - 2, 18):
        if k % 2 == 0:
            c.drawRect(skia.Rect.MakeLTRB(x0 + 3, yy, x0 + 17, yy + 14), PT(T(accent), 200))
            c.drawRect(skia.Rect.MakeLTRB(x1 - 17, yy, x1 - 3, yy + 14), PT(T(accent), 200))
        k += 1
    rs = _RS(seed)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(fx0, fy0, fx1, fy1))
    cols = ["#E8C25A", "#C84A38", "#E8DEC0", "#7FA3C8", "#D8788A"]
    for i in range(int(w * h / 1700)):
        px, py = rs.uniform(fx0, fx1), rs.uniform(fy0, fy1)
        col = cols[rs.randint(len(cols))]
        c.drawLine(px, py, px + rs.uniform(-3, 3), py + 9, STK("#3E6A4A", 1.4, 200))
        for a_ in range(5):
            ang = a_ * 1.2566
            c.drawCircle(px + math.cos(ang) * 3.4, py + math.sin(ang) * 3.4, 2.4, PT(T(col), 230))
        c.drawCircle(px, py, 1.8, PT("#F6E8A0"))
    if motif == "tree":
        tx, ty = x, y1 - 36
        c.drawPath(sk.poly_path([(tx - 9, ty), (tx - 5, ty - h * 0.46), (tx + 5, ty - h * 0.46), (tx + 9, ty)]), PT(T("#6A4224")))
        INKP(c, sk.poly_path([(tx - 9, ty), (tx - 5, ty - h * 0.46), (tx + 5, ty - h * 0.46), (tx + 9, ty)]), 1.2, 190)
        for (qx, qy, qr) in ((tx, ty - h * 0.62, w * 0.20), (tx - w * 0.14, ty - h * 0.48, w * 0.13), (tx + w * 0.14, ty - h * 0.50, w * 0.13)):
            c.drawCircle(qx, qy, qr, PT(T("#2E7A4A")))
            c.drawCircle(qx, qy, qr, STK(INK, 1.3, 190))
            for j in range(7):
                a_ = j * 0.9 + qx * 0.1
                c.drawCircle(qx + math.cos(a_) * qr * 0.55, qy + math.sin(a_) * qr * 0.5, 3.6, PT(T(accent)))
        for bx, by in ((tx - w * 0.28, ty - h * 0.30), (tx + w * 0.27, ty - h * 0.36)):
            c.drawOval(skia.Rect.MakeLTRB(bx - 11, by - 7, bx + 11, by + 7), PT(T("#E8DEC0")))
            c.drawOval(skia.Rect.MakeLTRB(bx - 11, by - 7, bx + 11, by + 7), STK(INK, 1.0, 180))
    c.restore()
    # saçak
    for fxx in np.arange(x0 + 3, x1 - 2, 6):
        c.drawLine(fxx, y1, fxx + 0.5, y1 + 11, STK(T(border), 1.5, 230))
    HGRAD(c, x0, y0, x1, y1, [("#FFFFFF", 0.0, 20), ("#000000", 0.55, 0), ("#000000", 1.0, 56)])


def draw_arms(c, T, x, y, s=1.0, frame=True):
    """Medici arması (palle): altın zemin, altı top (üstte lapis büyük, 5 sinabar), kabartma çerçeveli kalkan. (x,y) = üst orta, s ≈ genişlik/120."""
    wd, hg = 120 * s, 138 * s
    if frame:
        FILLP(c, sk.poly_path([(x - wd * 0.62, y - 12 * s), (x + wd * 0.62, y - 12 * s), (x + wd * 0.62, y + hg * 0.72), (x, y + hg + 26 * s), (x - wd * 0.62, y + hg * 0.72)]),
              T("#7A5A22"), 255, 1.4, 200)
    p = skia.Path()
    p.moveTo(x - wd / 2, y)
    p.lineTo(x + wd / 2, y)
    p.lineTo(x + wd / 2, y + hg * 0.55)
    p.cubicTo(x + wd / 2, y + hg * 0.86, x + wd * 0.2, y + hg * 0.98, x, y + hg)
    p.cubicTo(x - wd * 0.2, y + hg * 0.98, x - wd / 2, y + hg * 0.86, x - wd / 2, y + hg * 0.55)
    p.close()
    FILLP(c, p, T(GOLD), 255, 1.6, 210, shader=LGP((x - wd / 2, y), (x + wd / 2, y + hg), [(T("#F4DE90"), 0.0), (T(GOLD), 0.5), (T("#86601F"), 1.0)]))
    for i, (dx, dy, rr) in enumerate(CM.PALLE_POS):
        px, py = x + (dx - 0.5) * wd * 0.92, y + dy * hg * 0.92 + 4 * s
        col = "#233C8C" if i == 0 else "#B33620"
        c.drawCircle(px, py, rr * wd * 0.93, PT(T(col)))
        c.drawCircle(px, py, rr * wd * 0.93, STK(INK, 1.1, 190))
        c.drawCircle(px - rr * wd * 0.25, py - rr * wd * 0.25, rr * wd * 0.28, PT("#FFFFFF", 70))
        if i == 0:
            c.drawLine(px, py - rr * wd * 0.5, px, py + rr * wd * 0.5, STK("#E8C25A", 1.6 * s, 200))
            c.drawLine(px - rr * wd * 0.4, py, px + rr * wd * 0.4, py, STK("#E8C25A", 1.6 * s, 200))


def draw_crucifix(c, T, x, y, s=1.0):
    """Sade ahşap haç (altın uçlu); gövde figürsüz."""
    R(c, x - 4 * s, y, x + 4 * s, y + 70 * s, T("#5A3A20"))
    R(c, x - 24 * s, y + 16 * s, x + 24 * s, y + 24 * s, T("#5A3A20"))
    INKR(c, x - 4 * s, y, x + 4 * s, y + 70 * s, 1.0, 190)
    INKR(c, x - 24 * s, y + 16 * s, x + 24 * s, y + 24 * s, 1.0, 190)
    for (px, py) in ((x, y), (x - 24 * s, y + 20 * s), (x + 24 * s, y + 20 * s), (x, y + 70 * s)):
        c.drawCircle(px, py, 4.0 * s, PT(T(GOLD)))
        c.drawCircle(px, py, 4.0 * s, STK(INK, 0.8, 190))


def draw_bed(c, T, x0, yb, length=560, head_h=500, foot_h=190, cover=("#8E2A30", "#D2A33E"), tester=True, plain=False, linen="#EDE4CC", wood="#6E4524"):
    """Yatak (YAN görünüm): sol başlık (oymalı/düz), sağ ayak ucu, yan tahta, minder + örtü (baklava desenli, saçaklı), yastık; isteğe bağlı tavan çerçevesi (tester) + saçaklı perde.
    x0 = başlığın sol kenarı, yb = zemin teması. Dönüş: (yastık sol x, yatak üstü y)."""
    xe = x0 + length
    SOFT(c, (x0 + xe) / 2 + 10, yb + 6, length * 0.62, 20, "#000000", 85)
    wcol = T(wood)
    # başlık
    hw = 62
    hp = skia.Path()
    top = yb - head_h
    hp.moveTo(x0, yb)
    hp.lineTo(x0, top + 70)
    if plain:
        hp.lineTo(x0, top + 20)
        hp.lineTo(x0 + hw, top + 20)
    else:
        hp.cubicTo(x0 - 6, top + 40, x0 + 8, top + 8, x0 + 20, top + 28)
        hp.cubicTo(x0 + 28, top + 6, x0 + 46, top + 4, x0 + hw * 0.82, top + 26)
        hp.cubicTo(x0 + hw + 6, top + 30, x0 + hw + 2, top + 52, x0 + hw, top + 70)
    hp.lineTo(x0 + hw, yb)
    hp.close()
    FILLP(c, hp, wcol, 255, 1.7, 210, shader=LGP((x0, 0), (x0 + hw, 0), [(mix(wcol, "#FFFFFF", 0.16), 0.0), (wcol, 0.45), (mix(wcol, "#000000", 0.3), 1.0)]))
    if not plain:
        BOX(c, x0 + 12, top + 96, x0 + hw - 12, yb - 250, wood, T, hl=0.20, sh=0.10, ink=1.2)
        BOX(c, x0 + 12, yb - 232, x0 + hw - 12, yb - 40, wood, T, hl=0.20, sh=0.10, ink=1.2)
        c.drawLine(x0 + 8, top + 80, x0 + hw - 8, top + 80, STK(T(GOLD), 2.0, 210, False))
        for fx in (x0 + 8, x0 + hw - 8):
            c.drawCircle(fx, top + 12, 7.5, PT(T(GOLD)))
            c.drawCircle(fx, top + 12, 7.5, STK(INK, 1.0, 190))
    # sol yan: yatak tahtası + bacak
    rail0, rail1 = yb - 96, yb - 62
    WOOD(c, x0 + hw - 4, rail0, xe, rail1, T, wood, 3, 1.4, grain=6)
    c.drawLine(x0 + hw, rail0 + 5, xe, rail0 + 5, STK(T(GOLD), 1.4, 170, False))
    # minder
    top_m = yb - 156
    mp = skia.Path()
    mp.moveTo(x0 + hw - 2, rail0)
    mp.cubicTo(x0 + hw, top_m + 8, x0 + hw + 30, top_m - 6, x0 + 150, top_m - 4)
    mp.cubicTo(x0 + 300, top_m, xe - 120, top_m - 2, xe - 46, top_m + 8)
    mp.lineTo(xe - 46, rail0)
    mp.close()
    FILLP(c, mp, T(linen), 255, 1.4, 190, shader=LGP((0, top_m), (0, rail0), [(T("#F4EEDC"), 0.0), (T(linen), 1.0)]))
    # örtü (yatak üstü + yana sarkan, saçaklı)
    c1, c2 = cover
    cp = skia.Path()
    cx0 = x0 + 214
    cp.moveTo(cx0, top_m - 10)
    cp.cubicTo(cx0 + 100, top_m - 26, cx0 + 240, top_m - 20, xe - 40, top_m + 2)
    cp.lineTo(xe - 40, rail0 + 40)
    n = 16
    for i in range(n + 1):
        xx = (xe - 40) - (xe - 40 - cx0) * i / n
        cp.lineTo(xx, rail0 + 40 + (7 if i % 2 else -2))
    cp.close()
    FILLP(c, cp, T(c1), 255, 1.6, 200, shader=LGP((0, top_m - 20), (0, rail0 + 40), [(T(mix(c1, "#FFFFFF", 0.10)), 0.0), (T(c1), 0.5), (T(mix(c1, "#000000", 0.30)), 1.0)]))
    c.save()
    c.clipPath(cp, skia.ClipOp.kIntersect, True)
    for xx in np.arange(cx0 + 20, xe - 40, 52):
        for yy in (top_m + 14, top_m + 50, top_m + 86):
            c.drawPath(sk.poly_path([(xx, yy - 13), (xx + 16, yy), (xx, yy + 13), (xx - 16, yy)]), PT(T(c2), 90))
            c.drawPath(sk.poly_path([(xx, yy - 13), (xx + 16, yy), (xx, yy + 13), (xx - 16, yy)]), STK(T(c2), 1.0, 130))
    c.drawLine(cx0 - 10, top_m + 6, xe - 40, top_m + 20, STK(T(c2), 3.0, 200))
    c.restore()
    for xx in np.arange(cx0, xe - 40, 5):
        c.drawLine(xx, rail0 + 42, xx + 0.4, rail0 + 52, STK(T(c2), 1.4, 220))
    # yastık
    pil = skia.Path()
    px0, px1, py0, py1 = x0 + hw + 6, x0 + hw + 150, top_m - 56, top_m + 6
    pil.moveTo(px0, py1)
    pil.cubicTo(px0 - 6, py0 + 22, px0 + 14, py0, px0 + 70, py0 + 2)
    pil.cubicTo(px1 - 10, py0 - 4, px1 + 10, py0 + 34, px1 - 4, py1)
    pil.close()
    FILLP(c, pil, T("#F4EEDC"), 255, 1.4, 180, shader=LGP((px0, py0), (px1, py1), [(T("#FFFFFF"), 0.0), (T("#E4DAC0"), 1.0)]))
    c.drawLine(px0 + 24, py0 + 18, px1 - 30, py0 + 30, STK("#8A7A5A", 1.0, 100))
    # ayak ucu + bacak
    fp = skia.Path()
    ftop = yb - foot_h
    fp.moveTo(xe - 46, yb)
    fp.lineTo(xe - 46, ftop + 24)
    fp.cubicTo(xe - 44, ftop + 4, xe - 30, ftop - 6, xe - 22, ftop)
    fp.cubicTo(xe - 8, ftop - 6, xe + 4, ftop + 6, xe + 2, ftop + 24)
    fp.lineTo(xe + 2, yb)
    fp.close()
    FILLP(c, fp, wcol, 255, 1.7, 210, shader=LGP((xe - 46, 0), (xe + 2, 0), [(mix(wcol, "#FFFFFF", 0.16), 0.0), (wcol, 0.5), (mix(wcol, "#000000", 0.3), 1.0)]))
    BOX(c, xe - 36, ftop + 38, xe - 8, yb - 44, wood, T, hl=0.2, sh=0.1, ink=1.1)
    if tester:
        ttop = yb - head_h + 8
        # ayak direği (tester'a kadar)
        post = skia.Path()
        post.moveTo(xe - 30, ftop)
        post.lineTo(xe - 30, ttop + 20)
        post.lineTo(xe - 10, ttop + 20)
        post.lineTo(xe - 10, ftop)
        post.close()
        FILLP(c, post, wcol, 255, 1.5, 200, shader=LGP((xe - 30, 0), (xe - 10, 0), [(mix(wcol, "#FFFFFF", 0.18), 0.0), (wcol, 0.5), (mix(wcol, "#000000", 0.3), 1.0)]))
        for yy in (ttop + 60, ttop + 140, ftop - 40):
            c.drawOval(skia.Rect.MakeLTRB(xe - 34, yy - 8, xe - 6, yy + 8), PT(T(mix(wood, "#000000", 0.1))))
            c.drawOval(skia.Rect.MakeLTRB(xe - 34, yy - 8, xe - 6, yy + 8), STK(INK, 1.0, 170))
        # tester kuşağı + saçaklı püsküllü perdelik (valance)
        WOOD(c, x0 - 8, ttop - 14, xe + 6, ttop + 20, T, wood, 5, 1.6, grain=4)
        c.drawLine(x0 - 4, ttop - 4, xe + 2, ttop - 4, STK(T(GOLD), 2.0, 200, False))
        vp = skia.Path()
        vp.moveTo(x0 + hw, ttop + 20)
        vp.lineTo(xe - 10, ttop + 20)
        m = 12
        for i in range(m + 1):
            xx = (xe - 10) - (xe - 10 - x0 - hw) * i / m
            vp.lineTo(xx, ttop + 20 + 56)
            if i < m:
                xx2 = xx - (xe - 10 - x0 - hw) / m / 2
                vp.quadTo(xx2, ttop + 20 + 90, xx - (xe - 10 - x0 - hw) / m, ttop + 20 + 56)
        vp.close()
        FILLP(c, vp, T(c1), 255, 1.4, 200, shader=LGP((0, ttop + 20), (0, ttop + 110), [(T(mix(c1, "#000000", 0.2)), 0.0), (T(c1), 1.0)]))
        c.drawLine(x0 + hw, ttop + 36, xe - 10, ttop + 36, STK(T(c2), 2.0, 200, False))
    return x0 + hw + 6, top_m


def draw_chest(c, T, x0, x1, yb, h=130, col="#6E4524", lid=True):
    """Sandık/cassone: ön yüz (oyma paneller, altın şerit, pirinç kilit) + kapak + ayaklar. yb = taban."""
    SOFT(c, (x0 + x1) / 2 + 8, yb + 4, (x1 - x0) * 0.6, 12, "#000000", 80)
    top = yb - h
    BOX(c, x0, top + 24, x1, yb - 12, col, T, ink=1.5)
    n = max(2, int((x1 - x0) / 90))
    for i in range(n):
        a, b = x0 + 10 + (x1 - x0 - 20) * i / n, x0 + 10 + (x1 - x0 - 20) * (i + 1) / n - 8
        BOX(c, a, top + 40, b, yb - 28, col, T, hl=0.18, sh=0.10, ink=1.0)
        c.drawLine((a + b) / 2, top + 48, (a + b) / 2, yb - 36, STK(T(GOLD), 1.0, 120, False))
    if lid:
        FILLP(c, sk.poly_path([(x0 - 8, top + 24), (x1 + 8, top + 24), (x1 + 2, top + 2), (x0 - 2, top + 2)]), T(mix(col, "#FFFFFF", 0.12)), 255, 1.6, 200)
    c.drawRect(skia.Rect.MakeLTRB((x0 + x1) / 2 - 11, top + 22, (x0 + x1) / 2 + 11, top + 56), PT(T("#C4A04A")))
    c.drawRect(skia.Rect.MakeLTRB((x0 + x1) / 2 - 11, top + 22, (x0 + x1) / 2 + 11, top + 56), STK(INK, 1.1, 190))
    c.drawCircle((x0 + x1) / 2, top + 42, 3, PT("#2A1A0C"))
    for fx in (x0 + 10, x1 - 22):
        R(c, fx, yb - 12, fx + 14, yb, T(mix(col, "#000000", 0.25)))
    R(c, x0, top + 24, x1, top + 31, T(mix(col, "#000000", 0.22)))


def draw_chair(c, T, x, yb, back_h=270, seat_h=74, w=92, facing=1, col="#6E4524", cushion="#8E2A30"):
    """Yüksek arkalıklı sandalye (YAN görünüm): arka bacak+arkalık, oturak (minderli), ön bacak, bağlantı çubuğu. x = oturak ortası, facing=1: sağa bakar."""
    d = facing
    bx = x - d * w / 2          # arka
    fx = x + d * w / 2          # ön
    SOFT(c, x, yb + 4, w * 0.8, 10, "#000000", 80)
    wcol = T(col)
    # arka bacak + arkalık direği
    def post(xp, y0, y1, wd):
        p0, p1 = sorted((xp - wd / 2, xp + wd / 2))
        BOX(c, p0, y0, p1, y1, col, T, ink=1.3)
    post(bx, yb - back_h, yb, 11)
    # arkalık tablası (oymalı)
    p0, p1 = sorted((bx - d * 4, bx + d * 20))
    BOX(c, p0, yb - back_h + 18, p1, yb - seat_h - 18, col, T, hl=0.2, sh=0.12, ink=1.3)
    c.drawLine((p0 + p1) / 2, yb - back_h + 28, (p0 + p1) / 2, yb - seat_h - 28, STK(T(GOLD), 1.0, 140, False))
    c.drawCircle(bx, yb - back_h - 2, 7, PT(T(GOLD)))
    c.drawCircle(bx, yb - back_h - 2, 7, STK(INK, 1.0, 180))
    # oturak
    s0, s1 = sorted((bx - d * 6, fx + d * 6))
    BOX(c, s0, yb - seat_h - 10, s1, yb - seat_h + 8, col, T, ink=1.3)
    cp = skia.Path()
    cp.addRoundRect(skia.Rect.MakeLTRB(s0 + 2, yb - seat_h - 22, s1 - 2, yb - seat_h - 8), 6, 6)
    FILLP(c, cp, T(cushion), 255, 1.2, 190)
    # ön bacak, bağ
    post(fx, yb - seat_h + 8, yb, 10)
    a, b = sorted((bx, fx))
    R(c, a, yb - 30, b, yb - 24, T(mix(col, "#000000", 0.1)))
    INKR(c, a, yb - 30, b, yb - 24, 1.0, 170)


def sconce(c, T, x, y, s=1.0, side=1):
    """Duvar şamdanı: pirinç arka plaka + S kıvrımlı kol + damla tabla. (x,y) = plaka merkezi. Dönüş: mum tabanı (x,y) — canlı mum buraya çizilir."""
    pl = skia.Path()
    pl.addOval(skia.Rect.MakeLTRB(x - 12 * s, y - 24 * s, x + 12 * s, y + 24 * s))
    FILLP(c, pl, "#B8903A", 255, 1.2, 200, shader=LGP((x - 12 * s, y - 24 * s), (x + 12 * s, y + 24 * s), [("#F0D27A", 0.0), ("#B8903A", 0.5), ("#6A4E1A", 1.0)]))
    c.drawCircle(x, y - 10 * s, 2.6 * s, PT("#3A2A12"))
    c.drawCircle(x, y + 10 * s, 2.6 * s, PT("#3A2A12"))
    ex, ey = x + side * 40 * s, y + 20 * s
    p = skia.Path()
    p.moveTo(x, y + 2 * s)
    p.cubicTo(x + side * 8 * s, y + 24 * s, x + side * 30 * s, y - 6 * s, ex, ey)
    c.drawPath(p, STK("#2A2018", 5.2 * s, 255))
    c.drawPath(p, STK("#B8903A", 2.2 * s, 255))
    dish = skia.Path()
    dish.moveTo(ex - 17 * s, ey)
    dish.quadTo(ex, ey + 9 * s, ex + 17 * s, ey)
    dish.quadTo(ex, ey - 4 * s, ex - 17 * s, ey)
    FILLP(c, dish, "#B8903A", 255, 1.1, 200)
    c.drawLine(ex, ey + 6 * s, ex, ey + 20 * s, STK("#2A2018", 3.0 * s, 255))
    return ex, ey


def candelabra_floor(c, x, ytop, ybase, col="#1E140C", arms=3, spread=46.0):
    """Demir yer şamdanı (koyu siluet; ön plan): üç ayaklı taban, boğumlu gövde, kıvrık kollar + kupalar. Dönüş: mum tabanları [(x,y)…]."""
    R(c, x - 4, ytop + 24, x + 4, ybase, col)
    for yy in (ytop + 150, ytop + 330, ytop + 470):
        c.drawOval(skia.Rect.MakeLTRB(x - 12, yy - 9, x + 12, yy + 9), PT(col))
    for sg in (-1, 0, 1):
        p = skia.Path()
        p.moveTo(x, ybase - 34)
        p.quadTo(x + sg * 30, ybase - 10, x + sg * 46, ybase + 6)
        c.drawPath(p, STK(col, 6.0, 255))
    c.drawOval(skia.Rect.MakeLTRB(x - 20, ybase - 40, x + 20, ybase - 24), PT(col))
    bases = []
    n = arms
    for i in range(n):
        u = (i - (n - 1) / 2) / max(1.0, (n - 1) / 2)
        bx = x + u * spread
        by = ytop + 14 + abs(u) * 18
        p = skia.Path()
        p.moveTo(x, ytop + 52)
        p.cubicTo(x + u * 8, ytop + 52, bx - u * 4, ytop + 44 + abs(u) * 10, bx, by + 8)
        c.drawPath(p, STK(col, 4.6, 255))
        c.drawOval(skia.Rect.MakeLTRB(bx - 13, by + 6, bx + 13, by + 15), PT(col))
        bases.append((bx, by + 8))
    return bases


@functools.lru_cache(maxsize=32)
def _drape_spr(w, h, col, col2, seed):
    """Sarkan perde sprite'ı (dikey kıvrımlar, saçak). FA.Strips ile dalgalandırılır."""
    pad = 8
    fr = sk.Frame(int(w) + 2 * pad, int(h) + 2 * pad)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    c.translate(pad, pad)
    HGRAD(c, 0, 0, w, h, [(mix(col, "#FFFFFF", 0.10), 0.0), (col, 1.0)])
    n = max(3, int(w / 16))
    for i in range(n):
        a, b = w * i / n, w * (i + 1) / n
        HGRAD(c, a, 0, b, h, [("#FFFFFF", 0.0, 40), ("#FFFFFF", 0.3, 0), ("#000000", 0.7, 0), ("#000000", 1.0, 70)])
        if i:
            c.drawLine(a, 0, a + 0.8, h, STK("#1A0A08", 1.1, 70, False))
    rs = _RS(seed)
    for yy in np.arange(30, h - 20, 48):
        for xx in np.arange(18 + (int(yy / 48) % 2) * 22, w - 10, 44):
            c.drawPath(sk.poly_path([(xx, yy - 14), (xx + 9, yy), (xx, yy + 14), (xx - 9, yy)]), PT(col2, 50))
    c.drawLine(0, h - 10, w, h - 10, STK(col2, 3.0, 230, False))
    xx = 0.0
    while xx < w:
        c.drawLine(xx, h - 10, xx + 0.5, h + 2, STK(col2, 1.4, 230))
        xx += 4.0
    c.drawRect(skia.Rect.MakeLTRB(0, 0, w, h - 2), STK(INK, 1.3, 170, False))
    return FA.Spr(fr.surf.makeImageSnapshot(), pad, pad)


_STRIPS = {}


def draw_drape(c, x, y_top, w, h, t, col="#8E2A30", col2="#D2A33E", amp=0.045, seed=0, ph=0.0, tie=None):
    """Hafif dalgalanan perde: (x sol kenar, y_top asılma çizgisi). tie = bağ yüksekliği oranı (0..1) → orada daralır (bağlı perde)."""
    key = (int(w), int(h), col, col2, seed)
    cs = _STRIPS.get(key)
    if cs is None:
        spr = _drape_spr(int(w), int(h), col, col2, seed)
        cs = _STRIPS[key] = FA.Strips(spr, 0, h + 8, step=max(5.0, h / 24.0))
    u = np.clip(cs.ycen / max(1.0, h), 0.0, 1.0)
    a = w * amp
    dx = a * (u ** 1.3) * np.sin(t * 1.1 - u * 2.6 + ph) + 0.4 * a * (u ** 1.1) * np.sin(t * 2.3 - u * 4.0 + ph * 1.7)
    dy = np.zeros_like(u)
    exl = -w * 0.02 * u * np.sin(t * 1.3 + ph + u * 2.0)
    exr = w * 0.02 * u * np.sin(t * 1.5 + ph + 1.0 + u * 2.0)
    if tie is not None:
        sq = np.exp(-((u - tie) / 0.07) ** 2) * w * 0.30
        exl = exl + sq
        exr = exr - sq
    c.save()
    c.translate(x + cs.ox, y_top + cs.oy)
    cs.draw(c, dx, dy, exl, exr, 1.0)
    c.restore()


# ═════════════════════════════ ODA 1743 (Anna Maria Luisa'nın odası; c0 açılışı / c16 kapanışı) ═════════════════════════════
def _vis(xc, half, xa, xb):
    return xc + half >= xa and xc - half <= xb


class Oda1743(Room):
    """Mumlu masa (belge · tüy kalem · mühür), pencere (gün ışığı huzmesi / ay), yatak (yan görünüm, başlık + tester), goblen, Medici arması, sandık.
    Parametreler: figure = "seated" (masada oturan kadın SİLÜETİ, belge yazar: 31 Ekim 1737 imza masası) | "lying" (yatakta yatan silüet: 18 Şubat 1743) | "both" | None;
    doc_lines (13), doc_shown (satır; verilmezse figür yazarken ~9+ilerleme, figür yoksa hepsi), seal_at (mühür basılışı çapası), candle_lit (0..1) / snuff_at (söndür çapası)."""
    name = "oda1743"
    PW = 2700
    BX0, BYB = 150, 785
    TX0, TW, TY, TD = 1800, 640, 692, 128
    CHAIR_X, FIG_Y = 1742, 808
    FIG_H = 282
    DOC_UV = (0.28, 0.50)
    DOC_S = 0.17
    CANDLE_UV = (0.64, 0.66)
    CLOTH = ("#8E2A30", "#D2A33E")

    def build(self):
        self.g = TGeom(self.TX0, self.TY, self.TW, self.TD)
        self.layer("wall", F_WALL, self.Lw(F_WALL), self._draw_wall, wear=3)
        self.layer("main", 1.0, self.PW, self._draw_main, wear=0, scale=1.4)
        self.layer("front", 1.0, self.PW, self._draw_front)
        self.layer("fg", F_FG, self.Lw(F_FG), self._draw_fg)
        self.doc_xy = self.g.pt(*self.DOC_UV)
        self.candle_xy = self.g.pt(*self.CANDLE_UV)

    def paths(self):
        dx, dy = self.doc_xy
        zf = 1.0 / self.DOC_S * 0.97          # belge 1100×760'ı doldurur
        return {
            "default": [(0.0, (1150, 0, 1.0)), (1.0, (1560, 0, 1.12))],
            "in": [(0.0, (1050, 0, 1.0)), (0.28, (1280, 0, 1.0)), (0.52, (1760, 8, 1.24)), (0.76, (dx - 20, 70, 2.3)), (1.0, (dx, dy - 470 + 20 / zf, zf))],
            "sweep_r": [(0.0, (1000, 0, 1.04)), (1.0, (1860, 8, 1.04))],
            "sweep_l": [(0.0, (1860, 8, 1.04)), (1.0, (1000, 0, 1.04))],
            "bed": [(0.0, (1150, 0, 1.0)), (1.0, (620, 50, 1.5))],
            "table": [(0.0, (1450, 0, 1.0)), (1.0, (1960, 70, 1.65))],
            "doc": [(0.0, (1960, 40, 1.4)), (1.0, (dx, dy - 470 + 20 / zf, zf))],
        }

    # ── statik katmanlar ────────────────────────────────────────────────
    def _draw_wall(self, fr, xa, xb):
        c, T = fr.c, self.T
        night = self.tod == "night"
        wx = self.wx
        plaster(c, xa, xb, OV - 40, Y_FL + 30, T, "#CDBA92", "#DCCDA8", amp=0.05)
        cornice(c, xa, xb, 72, T)
        wainscot(c, xa, xb, Y_FL - 150, Y_FL + 18, T, "#8A5A38", seed=2)
        if _vis(wx(430), 360, xa, xb):
            draw_hanging(c, T, wx(110), wx(760), 205, 548, "#8E2A30", GOLD, seed=4)
        if _vis(wx(1010), 120, xa, xb):
            draw_window(c, T, wx(1010), 215, 190, 330, night=night)
        if _vis(wx(790), 40, xa, xb):
            draw_crucifix(c, T, wx(800), 262, 1.0) if False else None
        if _vis(wx(1420), 180, xa, xb):
            draw_tapestry(c, T, wx(1420), 178, 250, 310, seed=3, field="#2F5A5A", accent="#8E2A30")
        if _vis(wx(1660), 80, xa, xb):
            sconce(c, T, wx(1660), 300, 1.1, 1)
        if _vis(wx(2150), 100, xa, xb):
            draw_arms(c, T, wx(2150), 208, 1.0)
        if _vis(wx(2560), 70, xa, xb):
            draw_crucifix(c, T, wx(2560), 250, 1.1)
        # zemin gölgesi (duvar dibi)
        sh = LGP((0, Y_FL - 30), (0, Y_FL + 30), [("#1A0F06", 0.0, 0), ("#1A0F06", 1.0, 70)])
        c.drawRect(skia.Rect.MakeLTRB(xa, Y_FL - 30, xb, Y_FL + 30), sh)

    def _draw_main(self, fr, xa, xb):
        c, T = fr.c, self.T
        floor_tiles(c, xa, xb, Y_FL, LH, T, "#B5603A", "#A5522F", seed=2)
        if _vis(2130, 800, xa, xb):
            rug(c, 1730, 2540, 748, 858, T, field="#9A2A22", border="#233C8C")
        if _vis(430, 330, xa, xb):
            self.pillow = draw_bed(c, T, self.BX0, self.BYB, 560, 500, 190, cover=("#8E2A30", GOLD))
        if _vis(1010, 150, xa, xb):
            draw_chest(c, T, 880, 1140, 772, 118)
        if _vis(self.CHAIR_X, 70, xa, xb):
            draw_chair(c, T, self.CHAIR_X, self.FIG_Y, 270, 74, 92, facing=1)

    def _draw_front(self, fr, xa, xb):
        c, T = fr.c, self.T
        if _vis(self.TX0 + self.TW / 2, self.TW / 2 + 60, xa, xb):
            table_front(c, self.g, 818, T, self.CLOTH)

    def _draw_fg(self, fr, xa, xb):
        c, T = fr.c, self.T
        fx = lambda x: W / 2 + (x - W / 2) * F_FG
        x = fx(1560)
        if _vis(x, 90, xa, xb):
            candelabra_floor(c, x, 300, 878, "#1E140C", 3, 48.0)

    # ── canlı katmanlar ─────────────────────────────────────────────────
    def dyn_wall(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        night = ctx.tod == "night"
        wx = self.wx
        if ctx.tod in ("day", "dusk"):
            window_light(f, wx(1010), 232, 170, 300, t, dx=-330 if False else 300, y_floor=Y_FL + 40, a=0.23 if ctx.tod == "day" else 0.14, seed=3, patch=False, dust=16, night=False, part="shaft")
        elif night:
            window_light(f, wx(1010), 232, 170, 300, t, dx=260, y_floor=Y_FL + 40, a=0.10, seed=3, patch=False, dust=6, night=True, part="shaft")
        # duvar şamdanı mumu
        if _vis(wx(1660), 120, ctx.xa, ctx.xb):
            sx, sy = wx(1660) + 44, 300 + 22
            candle(f, sx, sy, 54, t, seed=4.7, holder=False, wax="#EAE0C4", lit=1.0 if night or ctx.tod == "dusk" else 0.0, smoke=night, halo=0.9)

    def _fig_state(self, ctx):
        fig = ctx.opts.get("figure", "seated")
        return fig

    def dyn_main(self, ctx):
        f, c, t, cx = ctx.f, ctx.c, ctx.t, ctx.cx
        T = self.T
        o = ctx.opts
        night = ctx.tod == "night"
        g = self.g
        wx = self.wx
        fig = o.get("figure", "seated")
        # pencere ışık lekesi (zemin + sandık)
        if ctx.tod in ("day", "dusk"):
            window_light(f, 1010, 232, 170, 300, t, dx=300, y_floor=Y_FL + 70, a=0.17 if ctx.tod == "day" else 0.12, seed=3, patch=True, dust=0, part="patch", patch_h=110)
        elif night:
            window_light(f, 1010, 232, 170, 300, t, dx=260, y_floor=Y_FL + 70, a=0.10, seed=3, patch=True, dust=0, night=True, part="patch", patch_h=110)
        # yatak perdesi (ayak ucu, hafif dalgalı)
        bx0 = self.BX0
        # yatan siluet
        if fig in ("lying", "both"):
            px, py = getattr(self, "pillow", (self.BX0 + 68, self.BYB - 156))
            lying_sil(f, px + 8, py + 10, t, 1.0, color="#1A1008", rim="#E8A860" if night else "#C79A5A", rim_dir=1)
        # masa tablası + eşyalar
        table_top(c, g, T, self.CLOTH)
        dxx, dyy = self.doc_xy
        cx_, cy_ = self.candle_xy
        t_seal = cx.amt(o["seal_at"], 0.5) if "seal_at" in o else 1.0
        # belge yazılışı: figür yazıyorsa ek bilgi sonra; önce çiz
        n_lines = int(o.get("doc_lines", 13))
        ex = {}
        shown = o.get("doc_shown", None)
        if fig in ("seated", "both"):
            sil = "#1A1008"
            hip_x = self.CHAIR_X + 18
            ex = seated_probe(self.FIG_H, t, t0=0.0)
            if shown is None:
                shown = 8.0 + ex.get("line", 0) % 4 + ex.get("prog", 0.0)
        doc_sheet(f, dxx, dyy, self.DOC_S, t, n=n_lines, shown=shown, seed=o.get("doc_seed", 3), seal=True, seal_t=t_seal, shadow=0.55)
        # küçük eşyalar (uzaktan yakına)
        ix, iy = g.pt(0.09, 0.66)
        inkwell(c, ix, iy, 0.95 * g.sc(0.66), t)
        if fig not in ("seated", "both"):
            qx, qy = g.pt(0.44, 0.22)
            quill(c, qx, qy, -14.0, 0.50)
        bx_, by_ = g.pt(0.80, 0.42)
        draw_book(c, bx_, by_, 90, 16, "#6A2E24")
        draw_book(c, bx_ + 4, by_ - 16, 80, 12, "#233C8C")
        sx_, sy_ = g.pt(0.50, 0.14)
        draw_scroll(c, sx_, sy_, 80, 0.9)
        gx_, gy_ = g.pt(0.93, 0.74)
        draw_goblet(c, gx_, gy_, 1.0)
        # oturan siluet (belge/tablanın ÜZERİNE: kollar belgenin üstünde)
        if fig in ("seated", "both"):
            seated(f, "soylu_f", self.CHAIR_X + 24, self.FIG_Y, self.FIG_H, t, "write", 1, seed=5, phase=0.0, sil="#1A1008", rim="#E8A860", rim_dir=1, t0=0.0)
        # mum (en önde)
        lit = float(o.get("candle_lit", 1.0))
        if "snuff_at" in o:
            lit *= 1.0 - cx.amt(o["snuff_at"], 0.35)
        if ctx.tod == "day":
            lit = max(lit * 0.0, 0.0) if o.get("candle_day", False) is False else lit
        candle(f, cx_, cy_, 96 * g.sc(self.CANDLE_UV[1]), t, seed=1.3, lit=lit, holder=True)
        if night and lit > 0.3:
            moth(c, cx_ + 4, cy_ - 118, t, seed=1.0, r=38)
        draw_extra(ctx, "back")
        # sıcak toz (mum çevresi)
        if night:
            dust_motes(c, t, cx_ - 260, cy_ - 240, cx_ + 260, cy_ + 40, n=14, seed=21, a=0.55, size=1.8, drift=(4, -2), col="#FFE2A0")

    def dyn_front(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        draw_extra(ctx, "front")
        # bağlı yatak perdesi: ayak ucunda, yavaş dalga
        bx0 = self.BX0 + 560
        draw_drape(c, bx0 + 14, self.BYB - 492 + 28 + 30, 74, 395, t, col="#8E2A30", col2=GOLD, amp=0.04, seed=2, ph=0.5, tie=0.62)

    def dyn_fg(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        fx = lambda x: W / 2 + (x - W / 2) * F_FG
        # şamdan mumu (ön plan; koyu siluet üstünde küçük alev)
        night = ctx.tod != "day"
        for i, (bx, by) in enumerate(((fx(1560) - 48, 322), (fx(1560), 314), (fx(1560) + 48, 322))):
            if _vis(bx, 80, ctx.xa, ctx.xb):
                candle(f, bx, by + 6, 42, t, seed=8.8 + i * 1.7, holder=False, lit=1.0 if night else 0.0, smoke=False, halo=0.8, wax="#D8CDB0")
        rs = _RS(44)
        xa, xb = ctx.xa, ctx.xb
        for k in range(14):
            x = xa + ((rs.rand() * (xb - xa) + t * 14 * (0.5 + rs.rand())) % (xb - xa))
            y = 120 + rs.rand() * 700 + math.sin(t * 0.6 + k) * 14
            c.drawCircle(x, y, 1.6 + 2.2 * rs.rand(), PT("#FFEFC4", int(40 + 70 * rs.rand())))

    def light(self, ctx):
        x, y = self.candle_xy
        return (x, y - 100, 820.0, 1.0)


ROOMS["oda1743"] = Oda1743
ROOMS["oda"] = Oda1743


def seated_probe(h, t, t0=0.0):
    """act_write'ın (satır, ilerleme) bilgisini figür çizmeden hesaplar (belge yazılışını elle eşlemek için)."""
    kit, bh = FA.kit_for("soylu_f", 5, h)
    pz = FA.act_write(kit, t, phase=0.0, t0=t0)
    return dict(pz.extra or {})


# ═════════════════════════════ SALON (saray / Signoria / Napoli sarayı / Pitti) ═════════════════════════════
def chandelier(f, x, ytop, ring_y, t, r=78.0, n=6, seed=0, lit=1.0, sway=1.6):
    """Tavandan zincirle sarkan demir avize (halka + mumlar): sarkaç gibi hafif sallanır; mumlar titrer. (x orta, ytop tavan, ring_y halka yüksekliği)."""
    c = f.c
    ang = math.radians(sway * math.sin(t * 0.55 + seed) + 0.5 * math.sin(t * 1.3 + seed * 2.0))
    L = ring_y - ytop
    px, py = x + L * math.sin(ang), ytop + L * math.cos(ang)
    ry = r * 0.20
    # zincirler (apeks → halka noktaları)
    c.drawLine(x, ytop, px, py - 40, STK("#2A2018", 2.6, 235))
    for k in range(1, 6):
        u = k / 6.0
        c.drawOval(skia.Rect.MakeLTRB(x + (px - x) * u - 3, ytop + (py - 40 - ytop) * u - 4, x + (px - x) * u + 3, ytop + (py - 40 - ytop) * u + 4), STK("#4A3A22", 1.4, 220))
    for sgn in (-1, 1):
        c.drawLine(px, py - 40, px + sgn * r * 0.92, py - 2, STK("#2A2018", 1.8, 230))
    # halka (ön/arka yay)
    c.drawOval(skia.Rect.MakeLTRB(px - r, py - ry, px + r, py + ry), STK("#2A1E10", 8.0, 255))
    c.drawOval(skia.Rect.MakeLTRB(px - r, py - ry, px + r, py + ry), STK("#B8903A", 3.4, 240))
    # mumlar (arkadakiler önce)
    items = []
    for i in range(n):
        a = 2 * math.pi * i / n + 0.3
        items.append((math.sin(a), px + r * math.cos(a), py + ry * math.sin(a)))
    items.sort()
    for depth, cxp, cyp in items:
        sc = 0.86 + 0.14 * depth
        candle(f, cxp, cyp + 4, 38 * sc, t, seed=seed + cxp * 0.013, lit=lit, holder=False, wax="#EFE6CE", halo=0.8, smoke=False)
    # alt sarkık küre
    c.drawCircle(px, py + ry + 10, 8, PT("#B8903A"))
    c.drawCircle(px, py + ry + 10, 8, STK(INK, 1.0, 190))
    return px, py


def candelabra_table(f, x, y, h, t, seed=0, arms=3, lit=1.0, col="#C4A04A"):
    """Masa üstü gümüş/pirinç şamdan (üç kollu): (x,y) taban. Mumlar canlı. Dönüş: orta alev konumu."""
    c = f.c
    # taban + gövde
    c.drawOval(skia.Rect.MakeLTRB(x - 20, y - 6, x + 20, y + 5), PT(col))
    c.drawOval(skia.Rect.MakeLTRB(x - 20, y - 6, x + 20, y + 5), STK(INK, 1.0, 180))
    R(c, x - 3.5, y - h * 0.62, x + 3.5, y - 4, col)
    for yy in (y - h * 0.18, y - h * 0.42):
        c.drawOval(skia.Rect.MakeLTRB(x - 8, yy - 5, x + 8, yy + 5), PT(col))
        c.drawOval(skia.Rect.MakeLTRB(x - 8, yy - 5, x + 8, yy + 5), STK(INK, 0.9, 170))
    top = y - h * 0.62
    bases = []
    for i in range(arms):
        u = (i - (arms - 1) / 2) / max(1.0, (arms - 1) / 2)
        bx = x + u * h * 0.30
        by = top - abs(u) * 6 + (0 if u == 0 else 12)
        p = skia.Path()
        p.moveTo(x, top + 8)
        p.cubicTo(x + u * 10, top + 12, bx - u * 6, top + 16, bx, by + 6)
        c.drawPath(p, STK(col, 3.2, 255))
        c.drawPath(p, STK(INK, 0.9, 120))
        c.drawOval(skia.Rect.MakeLTRB(bx - 8, by + 2, bx + 8, by + 8), PT(col))
        bases.append((bx, by + 4))
    fl = None
    for i, (bx, by) in enumerate(bases):
        r = candle(f, bx, by, 36 + (8 if i == len(bases) // 2 else 0), t, seed=seed + i * 2.1, lit=lit, holder=False, halo=0.9, smoke=False)
        if i == len(bases) // 2:
            fl = r
    return fl


@functools.lru_cache(maxsize=4)
def _map_paper(seed):
    return PP.paper_image(660, 440, seed, (242, 232, 202), "deckle", (("v", 0.5), ("h", 0.5)), 30, 0.8)


def map_sheet(f, x, y, scale, t=0.0, seed=7, rot=0.0, route=None, alpha=1.0):
    """Masada açık harita/portolan levhası (yazısız): kara kütleleri, dalgalı deniz çizgileri, pusula gülü; route=(0..1) ilerlemeli kesikli rota. (x,y) merkez."""
    c = f.c
    pp = _map_paper(seed)
    pp.draw(f, x, y, rot=rot, scale=scale, alpha=alpha, shadow=0.5)
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(rot))
    c.scale(scale, scale)
    c.clipRect(skia.Rect.MakeLTRB(-320, -210, 320, 210))
    rs = _RS(seed * 13)
    for i in range(7):
        yy = -180 + i * 58
        pth = skia.Path()
        pth.moveTo(-320, yy)
        for xx in range(-320, 321, 16):
            pth.lineTo(xx, yy + 5 * math.sin(xx * 0.05 + i + t * 0.4))
        c.drawPath(pth, STK("#5C7C92", 1.4, 80))
    land = [[(-320, -210), (-150, -210), (-120, -120), (-190, -40), (-150, 40), (-230, 120), (-320, 130)],
            [(40, -210), (320, -210), (320, -60), (230, -90), (170, -30), (110, -100)],
            [(60, 210), (110, 110), (190, 70), (250, 120), (320, 90), (320, 210)]]
    for L in land:
        p = sk.smooth_path(L, True, 0.4)
        c.drawPath(p, PT("#D8C48C", 255))
        c.drawPath(p, STK("#4A3220", 2.6, 220))
        c.drawPath(p, STK("#8AA0AE", 9.0, 60))
    # pusula gülü
    cx_, cy_ = 230, 150
    for k in range(8):
        a = k * math.pi / 4
        c.drawLine(cx_, cy_, cx_ + math.cos(a) * (34 if k % 2 == 0 else 20), cy_ + math.sin(a) * (34 if k % 2 == 0 else 20), STK("#7A2A1C", 2.4, 220))
    c.drawCircle(cx_, cy_, 7, STK("#4A3220", 1.6, 220))
    # rota
    if route is not None:
        pts = [(-130, 30), (-60, -20), (10, 20), (70, -10), (130, 40), (190, 10)]
        n = len(pts) - 1
        pr = clamp(route) * n
        pth = skia.Path()
        pth.moveTo(*pts[0])
        for i in range(n):
            u = clamp(pr - i)
            if u <= 0:
                break
            x0_, y0_ = pts[i]
            x1_, y1_ = pts[i + 1]
            pth.lineTo(x0_ + (x1_ - x0_) * u, y0_ + (y1_ - y0_) * u)
        p2 = STK("#A52A1C", 3.4, 235)
        p2.setPathEffect(skia.DashPathEffect.Make([10, 8], 0))
        c.drawPath(pth, p2)
    c.restore()


def chair_back(c, T, x, yb, w=72, h=250, col="#6E4524", cushion="#7A2E2A"):
    """Önden görünen yüksek arkalıklı sandalye (masanın arkasında, yalnız sırt kısmı): iki direk, minderli panel, başlık kuşağı, topuz."""
    for sg in (-1, 1):
        BOX(c, x + sg * w / 2 - 6, yb - h, x + sg * w / 2 + 6, yb, col, T, ink=1.2)
        c.drawCircle(x + sg * w / 2, yb - h - 3, 6, PT(T(GOLD)))
        c.drawCircle(x + sg * w / 2, yb - h - 3, 6, STK(INK, 0.9, 190))
    BOX(c, x - w / 2 - 4, yb - h + 6, x + w / 2 + 4, yb - h + 26, col, T, ink=1.2)
    p = skia.Path()
    p.addRoundRect(skia.Rect.MakeLTRB(x - w / 2 + 6, yb - h + 34, x + w / 2 - 6, yb - 70), 8, 8)
    FILLP(c, p, T(cushion), 255, 1.2, 190, shader=LGP((0, yb - h), (0, yb - 70), [(T(mix(cushion, "#FFFFFF", 0.12)), 0.0), (T(cushion), 1.0)]))
    for qx in (x - w / 2 + 14, x + w / 2 - 14):
        for qy in (yb - h + 44, yb - 80):
            c.drawCircle(qx, qy, 2.0, PT(T(GOLD)))
    BOX(c, x - w / 2 - 2, yb - 66, x + w / 2 + 2, yb - 52, col, T, ink=1.1)


def draw_mirror(c, T, x, y0, w, h):
    """Yaldız çerçeveli büyük ayna (Pitti): mavi-gümüş yüzey, çapraz parıltı şeritleri."""
    FILLP(c, sk.poly_path([(x - w / 2 - 14, y0 - 14), (x + w / 2 + 14, y0 - 14), (x + w / 2 + 14, y0 + h + 14), (x - w / 2 - 14, y0 + h + 14)]), T("#C79A3C"), 255, 1.6, 210)
    for k in range(6):
        c.drawCircle(x - w / 2 - 7 + (w + 14) * k / 5, y0 - 7, 5, PT(T("#F0D27A")))
        c.drawCircle(x - w / 2 - 7 + (w + 14) * k / 5, y0 + h + 7, 5, PT(T("#F0D27A")))
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, y0, x + w / 2, y0 + h), LGP((x - w / 2, y0), (x + w / 2, y0 + h), [("#DCE8F0", 0.0), ("#9DB4C8", 0.5), ("#C8D8E4", 1.0)]))
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(x - w / 2, y0, x + w / 2, y0 + h))
    for k, (u, wd, a) in enumerate(((0.2, 26, 90), (0.55, 14, 70), (0.8, 40, 60))):
        c.drawPath(sk.poly_path([(x - w / 2 + w * u, y0), (x - w / 2 + w * u + wd, y0), (x - w / 2 + w * u + wd - 90, y0 + h), (x - w / 2 + w * u - 90, y0 + h)]), PT("#FFFFFF", a))
    c.restore()
    INKR(c, x - w / 2, y0, x + w / 2, y0 + h, 1.4, 190)


def palle_frieze(c, T, xa, xb, y, r=17.0, step=52.0):
    """Palle frizi: altın zemin şeridinde sinabar toplar (Medici motifi)."""
    R(c, xa, y - r - 8, xb, y + r + 8, T("#D9B860"))
    c.drawLine(xa, y - r - 8, xb, y - r - 8, STK(INK, 1.2, 170, False))
    c.drawLine(xa, y + r + 8, xb, y + r + 8, STK(INK, 1.2, 170, False))
    x = xa - (xa % step)
    while x < xb + step:
        c.drawCircle(x + step / 2, y, r, PT(T("#B33620")))
        c.drawCircle(x + step / 2, y, r, STK(INK, 1.0, 190))
        c.drawCircle(x + step / 2 - r * 0.3, y - r * 0.3, r * 0.28, PT("#FFFFFF", 80))
        x += step


SALON_PAL = {
    "medici": dict(wall=("#D8C08C", "#E4D2A8"), dado="#8A5A38", tap=("#8E2A30", "#B88A32"), floor=("#B5603A", "#A5522F"), cloth=("#233C8C", "#D2A33E"), deco="palle", seat="#7A2E2A"),
    "napoli": dict(wall=("#BDB8A0", "#D3CDB4"), dado="#4A6A70", tap=("#2A6E7A", "#C79A3C"), floor=("#93A3A0", "#738688"), cloth=("#1F5A7A", "#D2A33E"), deco="tap", seat="#1F5A7A"),
    "signoria": dict(wall=("#B88A62", "#CDA57A"), dado="#6A3A28", tap=("#8E2A30", "#F0E6CC"), floor=("#D2BE92", "#8E3A2A"), cloth=("#8E2A30", "#F0E6CC"), deco="banner", seat="#8E2A30"),
    "pitti": dict(wall=("#E6DFCB", "#F0EAD8"), dado="#B8A070", tap=("#4468C0", "#D2A33E"), floor=("#DCD0AE", "#B8A27A"), cloth=("#4468C0", "#E8C25A"), deco="mirror", seat="#4468C0"),
    "taht": dict(wall=("#9A7A5C", "#B89A74"), dado="#5A3A28", tap=("#8E2A30", "#B88A32"), floor=("#C9B58A", "#7A3A2A"), cloth=("#8E2A30", "#D2A33E"), deco="palle", seat="#7A2E2A"),
}


def draw_throne(c, T, x, yb, s=1.0):
    """Boş taht: üç basamaklı kürsü, yüksek oymalı arkalıklı yaldızlı koltuk, kırmızı kadife minder, kolçaklar. (x orta, yb kürsü tabanı)."""
    SOFT(c, x, yb + 6, 300 * s, 16, "#000000", 90)
    for i in range(3):
        BOX(c, x - (250 - i * 36) * s, yb - (i + 1) * 20 * s, x + (250 - i * 36) * s, yb - i * 20 * s, "#7A4A2A", T, hl=0.14, sh=0.2, ink=1.4)
        R(c, x - (250 - i * 36) * s, yb - (i + 1) * 20 * s, x + (250 - i * 36) * s, yb - (i + 1) * 20 * s + 5 * s, T("#C9A468"))
    y0 = yb - 60 * s
    # arkalık
    bp = skia.Path()
    bp.moveTo(x - 66 * s, y0)
    bp.lineTo(x - 70 * s, y0 - 250 * s)
    bp.cubicTo(x - 70 * s, y0 - 300 * s, x - 30 * s, y0 - 318 * s, x, y0 - 330 * s)
    bp.cubicTo(x + 30 * s, y0 - 318 * s, x + 70 * s, y0 - 300 * s, x + 70 * s, y0 - 250 * s)
    bp.lineTo(x + 66 * s, y0)
    bp.close()
    FILLP(c, bp, T("#C79A3C"), 255, 1.8, 210, shader=LGP((x - 70 * s, 0), (x + 70 * s, 0), [(T("#F4DE90"), 0.0), (T("#C79A3C"), 0.45), (T("#7A5A22"), 1.0)]))
    ip = skia.Path()
    ip.moveTo(x - 46 * s, y0 - 64 * s)
    ip.lineTo(x - 48 * s, y0 - 250 * s)
    ip.cubicTo(x - 48 * s, y0 - 282 * s, x - 22 * s, y0 - 296 * s, x, y0 - 302 * s)
    ip.cubicTo(x + 22 * s, y0 - 296 * s, x + 48 * s, y0 - 282 * s, x + 48 * s, y0 - 250 * s)
    ip.lineTo(x + 46 * s, y0 - 64 * s)
    ip.close()
    FILLP(c, ip, T("#8E1F26"), 255, 1.4, 200, shader=LGP((0, y0 - 300 * s), (0, y0), [(T("#A82A30"), 0.0), (T("#6A1018"), 1.0)]))
    for k in range(4):
        c.drawCircle(x - 38 * s + (k % 2) * 76 * s, y0 - 80 * s - (k // 2) * 150 * s, 3.4 * s, PT(T(GOLD)))
    c.drawCircle(x, y0 - 336 * s, 10 * s, PT(T(GOLD)))
    c.drawCircle(x, y0 - 336 * s, 10 * s, STK(INK, 1.0, 190))
    # oturak + kolçaklar
    BOX(c, x - 78 * s, y0 - 70 * s, x + 78 * s, y0 - 40 * s, "#8E1F26", T, hl=0.2, sh=0.2, ink=1.4)
    for sg in (-1, 1):
        BOX(c, x + sg * 78 * s - 9 * s, y0 - 120 * s, x + sg * 78 * s + 9 * s, y0 - 10 * s, "#C79A3C", T, hl=0.22, sh=0.24, ink=1.4)
        c.drawCircle(x + sg * 78 * s, y0 - 124 * s, 10 * s, PT(T(GOLD)))
        c.drawCircle(x + sg * 78 * s, y0 - 124 * s, 10 * s, STK(INK, 1.0, 190))
    BOX(c, x - 70 * s, y0 - 40 * s, x + 70 * s, y0, "#7A5A22", T, hl=0.2, sh=0.2, ink=1.3)


class Salon(Room):
    """Saray / Signoria salonu: uzun masa (ters perspektif tabla), tavandan avize, uzun pencereler (gün huzmesi / ay), goblen–sancak–ayna, sandalye sırtları, masa uçlarında OTURAN figürler.
    variant: "medici" (Palazzo Medici; palle frizi) | "napoli" (Napoli sarayı: serin tonlar, Lorenzo–Ferrante masa başı iki siluet) | "signoria" (Palazzo Vecchio: kızıl-beyaz sancaklar) | "pitti" (aynalı, beyaz-altın).
    actors verilmezse varsayılan figürler; verilirse (boş liste dâhil) yalnız onlar. Parametreler: map_route (0..1: masadaki haritada rota ilerler), speaker ("a"|"b"|"alt": konuşan), sil (True/False: oturanlar siluet)."""
    name = "salon"
    PW = 3400
    TX0, TW, TY, TD = 1050, 1300, 706, 108
    FIG_H = 282

    def __init__(self, variant, tod):
        v = variant or "medici"
        self.pal = SALON_PAL.get(v, SALON_PAL["medici"])
        super().__init__(v, tod)

    def build(self):
        self.g = TGeom(self.TX0, self.TY, self.TW, self.TD, 0.04)
        self.layer("wall", F_WALL, self.Lw(F_WALL), self._draw_wall, wear=3)
        self.layer("main", 1.0, self.PW, self._draw_main, scale=1.2)
        self.layer("front", 1.0, self.PW, self._draw_front)
        self.layer("fg", F_FG, self.Lw(F_FG), self._draw_fg)
        self.win_x = [640, 1420, 2200, 2980]
        self.tap_x = [1030, 1810, 2590]

    def paths(self):
        return {
            "default": [(0.0, (1300, 0, 1.0)), (1.0, (2100, 0, 1.12))],
            "in": [(0.0, (1100, 0, 1.0)), (0.5, (1500, 10, 1.15)), (1.0, (1700, 40, 1.55))],
            "sweep_r": [(0.0, (1000, 0, 1.0)), (1.0, (2400, 0, 1.0))],
            "sweep_l": [(0.0, (2400, 0, 1.0)), (1.0, (1000, 0, 1.0))],
            "table": [(0.0, (1700, 0, 1.0)), (1.0, (1700, 50, 1.5))],
            "heads": [(0.0, (1050, 80, 1.6)), (0.5, (1700, 70, 1.45)), (1.0, (2350, 80, 1.6))],
            "pull": [(0.0, (1700, 40, 1.5)), (1.0, (1700, 0, 1.0))],
            "taht": [(0.0, (1700, 60, 1.7)), (1.0, (1700, 0, 1.0))],
            "taht_in": [(0.0, (1500, 0, 1.0)), (1.0, (1700, 90, 1.9))],
        }

    def default_actors(self, ctx=None):
        v = self.variant
        if v == "taht":
            return []
        sil = bool(self.opts.get("sil", v == "napoli"))
        t = ctx.t if ctx is not None else 0.0
        sp = self.opts.get("speaker", "alt")
        if sp == "alt":
            k = int(t // 5.5) % 2
            a_act, b_act = ("talk", "listen") if k == 0 else ("listen", "talk")
        else:
            a_act, b_act = ("talk", "listen") if sp == "a" else ("listen", "talk")
        fy = self.TY + 117
        fa, fb = self.TX0 - 34, self.TX0 + self.TW + 34
        out = [dict(kind="soylu", x=fa, y=fy, h=self.FIG_H, action=a_act, seated=True, sil=sil, seed=11, dir=1, phase=0.1),
               dict(kind="soylu" if v != "medici" else "banker", x=fb, y=fy, h=self.FIG_H, action=b_act, seated=True, sil=sil, seed=14, dir=-1, phase=0.6, rim_dir=-1)]
        if v == "signoria":
            out += [dict(kind="rahip", x=1500, y=690, h=262, action="talk", seed=21, layer="behind", phase=0.3), dict(kind="soylu", x=1980, y=690, h=262, action="point", seed=23, layer="behind", t0=1.0)]
        elif v == "medici":
            out += [dict(kind="tuccar", x=1700, y=690, h=262, action="talk", seed=24, layer="behind", phase=0.4)]
        elif v == "pitti":
            out = [dict(kind="soylu", x=1500, y=800, h=270, action="talk", seed=31, dir=1, layer="front"), dict(kind="soylu_f", x=1760, y=806, h=262, action="talk", seed=32, dir=-1, layer="front", phase=0.5),
                   dict(kind="soylu", x=2200, y=796, h=270, action="idle", seed=33, dir=-1, layer="front")]
        return out

    # ── statik ───────────────────────────────────────────────────────────
    def _draw_wall(self, fr, xa, xb):
        c, T, P = fr.c, self.T, self.pal
        night = self.tod == "night"
        wx = self.wx
        plaster(c, xa, xb, OV - 40, Y_FL + 30, T, P["wall"][0], P["wall"][1], amp=0.05)
        cornice(c, xa, xb, 72, T, col=mix(P["dado"], "#000000", 0.1), plaster=P["wall"][1])
        wainscot(c, xa, xb, Y_FL - 118, Y_FL + 18, T, P["dado"], seed=3)
        if P["deco"] == "palle":
            palle_frieze(c, T, xa, xb, 176)
        for x in self.win_x:
            if _vis(wx(x), 130, xa, xb):
                draw_window(c, T, wx(x), 226, 176, 336, night=night)
        for x in self.tap_x:
            if _vis(wx(x), 150, xa, xb):
                if P["deco"] in ("tap", "palle"):
                    draw_tapestry(c, T, wx(x), 238, 236, 318, seed=int(x) % 7, field=P["tap"][0] if P["deco"] == "tap" else "#2F5A5A", accent="#8E2A30" if P["deco"] == "palle" else "#D8788A", border=P["tap"][1])
                elif P["deco"] == "mirror":
                    draw_mirror(c, T, wx(x), 240, 150, 300)
                # banner: dinamik
        if P["deco"] in ("tap", "palle") and _vis(wx(240), 150, xa, xb):
            draw_tapestry(c, T, wx(240), 238, 236, 318, seed=2, field=P["tap"][0] if P["deco"] == "tap" else "#2F5A5A", accent="#8E2A30", border=P["tap"][1])
        if P["deco"] in ("tap", "palle") and _vis(wx(3300), 150, xa, xb):
            draw_tapestry(c, T, wx(3300), 238, 236, 318, seed=5, field=P["tap"][0] if P["deco"] == "tap" else "#2F5A5A", accent="#8E2A30", border=P["tap"][1])
        if P["deco"] == "palle":
            for x in (1030, 2590):
                if _vis(wx(x), 80, xa, xb):
                    pass
        if _vis(wx(1810), 90, xa, xb) and P["deco"] == "palle":
            draw_arms(c, T, wx(1810), 90, 0.001) if False else None
        sh = LGP((0, Y_FL - 30), (0, Y_FL + 30), [("#1A0F06", 0.0, 0), ("#1A0F06", 1.0, 70)])
        c.drawRect(skia.Rect.MakeLTRB(xa, Y_FL - 30, xb, Y_FL + 30), sh)

    def _draw_main(self, fr, xa, xb):
        c, T, P = fr.c, self.T, self.pal
        floor_tiles(c, xa, xb, Y_FL, LH, T, P["floor"][0], P["floor"][1], seed=4, w0=74.0, grow=1.13)
        # masanın arkasındaki sandalye sırtları
        if self.variant == "taht":
            if _vis(1700, 420, xa, xb):
                rug(c, 1450, 1950, 752, 880, T, field="#8E2A30", border="#C79A3C", inset=0.16)
                draw_throne(c, T, 1700, 760, 1.0)
                pel = skia.Path()
                pel.moveTo(1440, 120)
                pel.lineTo(1960, 120)
                n = 10
                for i in range(n + 1):
                    xx = 1960 - 520 * i / n
                    pel.lineTo(xx, 176)
                    if i < n:
                        pel.quadTo(xx - 26, 214, xx - 52, 176)
                pel.close()
                FILLP(c, pel, T("#8E1F26"), 255, 1.5, 200, shader=LGP((0, 120), (0, 214), [(T("#6A1018"), 0.0), (T("#A82A30"), 1.0)]))
                BOX(c, 1430, 100, 1970, 124, "#C79A3C", T, hl=0.22, sh=0.22, ink=1.5)
            for x in (700, 2700):
                if _vis(x, 100, xa, xb):
                    chair_back(c, T, x, 730, 72, 230, cushion=P["seat"])
            return
        for i in range(6):
            x = self.TX0 + 130 + i * 208
            if _vis(x, 60, xa, xb):
                chair_back(c, T, x, 700, 72, 252, cushion=P["seat"])
        # uç sandalyeler (oturanların)
        fa, fb = self.TX0 - 34, self.TX0 + self.TW + 34
        if _vis(fa, 80, xa, xb):
            draw_chair(c, T, fa - 24, self.TY + 117 - 8, 270, 74, 92, facing=1, cushion=P["seat"])
        if _vis(fb, 80, xa, xb):
            draw_chair(c, T, fb + 24, self.TY + 117 - 8, 270, 74, 92, facing=-1, cushion=P["seat"])
        rug(c, self.TX0 - 120, self.TX0 + self.TW + 120, 744, 868, T, field=P["tap"][0] if P["deco"] != "mirror" else "#8E2A30", border=mix(P["cloth"][0], "#000000", 0.15))

    def _draw_front(self, fr, xa, xb):
        c, T, P = fr.c, self.T, self.pal
        if self.variant == "taht":
            return
        if _vis(self.TX0 + self.TW / 2, self.TW / 2 + 80, xa, xb):
            table_front(c, self.g, self.TY + 112, T, P["cloth"], apron=32)

    def _draw_fg(self, fr, xa, xb):
        c, T = fr.c, self.T
        fx = lambda x: W / 2 + (x - W / 2) * F_FG
        for x in (560, 3040):
            if _vis(fx(x), 90, xa, xb):
                candelabra_floor(c, fx(x), 340, 880, "#1E140C", 3, 46.0)

    # ── canlı ────────────────────────────────────────────────────────────
    def dyn_wall(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        wx = self.wx
        night = ctx.tod == "night"
        for i, x in enumerate(self.win_x):
            if _vis(wx(x), 400, ctx.xa, ctx.xb):
                window_light(f, wx(x), 244, 150, 306, t, dx=300, y_floor=Y_FL + 30, a=0.20 if ctx.tod == "day" else (0.12 if ctx.tod == "dusk" else 0.09), seed=2 + i, patch=False,
                             dust=10, night=night, part="shaft")
        if self.pal["deco"] == "banner":
            for i, x in enumerate(self.tap_x + [240, 3300]):
                if _vis(wx(x), 140, ctx.xa, ctx.xb):
                    PN.draw_cloth(c, wx(x) - 50, 150, "#8E2A30" if i % 2 == 0 else "#F0E6CC", "#F0E6CC" if i % 2 == 0 else "#8E2A30", 100, 330, t, ph=i * 1.3, wind=0.5, kind="tente")
                    R(c, wx(x) - 62, 142, wx(x) + 62, 152, "#4A3220")
                    INKR(c, wx(x) - 62, 142, wx(x) + 62, 152, 1.2, 190)

    def dyn_main(self, ctx):
        f, c, t, cx = ctx.f, ctx.c, ctx.t, ctx.cx
        T, P, g = self.T, self.pal, self.g
        night = ctx.tod == "night"
        for i, x in enumerate(self.win_x):
            if _vis(x, 400, ctx.xa, ctx.xb):
                window_light(f, x, 244, 150, 306, t, dx=300, y_floor=Y_FL + 70, a=0.20 if ctx.tod == "day" else (0.12 if ctx.tod == "dusk" else 0.09), seed=2 + i, patch=True, dust=0, night=night, part="patch", patch_h=110)
        if self.variant == "taht":
            self._dyn_taht(ctx)
            return
        # avizeler
        lit = 1.0 if ctx.tod != "day" else float(self.opts.get("chandelier_day", 0.0))
        for i, x in enumerate((1450, 2300)):
            if _vis(x, 200, ctx.xa, ctx.xb):
                chandelier(f, x, 62, 250 + 10 * i, t, r=80, n=6, seed=i * 3.1, lit=lit)
        draw_extra(ctx, "behind")
        table_top(c, g, T, P["cloth"])
        mid = self.TX0 + self.TW / 2
        # harita (masanın ortası), evraklar, hokka
        mx, my = g.pt(0.40, 0.50)
        rt = self.opts.get("map_route", None)
        if rt is not None and "map_at" in self.opts:
            rt = clamp((t - cx.at(self.opts["map_at"])) / 5.0)
        map_sheet(f, mx, my, 0.30, t, seed=7, rot=-0.03, route=rt if rt is not None else 1.0)
        px, py = g.pt(0.60, 0.56)
        doc_sheet(f, px, py, 0.085, t, n=9, seed=5, rot=0.05, seal=True)
        ix, iy = g.pt(0.20, 0.30)
        inkwell(c, ix, iy, 0.9, t)
        qx, qy = g.pt(0.23, 0.22)
        quill(c, qx, qy, -12.0, 0.42)
        gx, gy = g.pt(0.76, 0.34)
        draw_goblet(c, gx, gy, 1.0)
        gx, gy = g.pt(0.81, 0.30)
        draw_goblet(c, gx, gy, 0.9)
        bx_, by_ = g.pt(0.10, 0.62)
        draw_book(c, bx_, by_, 70, 13, "#6A2E24")
        cl = candelabra_table(f, *g.pt(0.50, 0.80), 78, t, seed=1.0, lit=1.0 if ctx.tod != "day" else float(self.opts.get("candle_day", 0.0)))
        if night and cl is not None:
            moth(c, cl[0], cl[1] - 8, t, seed=3.0, r=30)
        draw_extra(ctx, "back")
        if night:
            dust_motes(c, t, mid - 380, 450, mid + 380, 690, n=14, seed=9, a=0.5, size=1.8, drift=(4, -2), col="#FFE2A0")

    def _dyn_taht(self, ctx):
        """Boş taht odası: pencere ışığı huzmesi tahta düşer, toz süzülür, tavan perdesi (baldaken) hafif dalgalanır; kimse yok."""
        f, c, t = ctx.f, ctx.c, ctx.t
        night = ctx.tod == "night"
        x0 = 1700
        # taht üzerine ışık lekesi
        k = 0.6 + 0.4 * math.sin(t * 0.21)
        c.drawPath(sk.poly_path([(x0 - 70, 250), (x0 + 70, 250), (x0 + 120, 740), (x0 - 120, 740)]), LGP((0, 250), (0, 740), [("#FFE9A8", 0.0, int(36 * k)), ("#FFE9A8", 1.0, int(70 * k))]))
        dust_motes(c, t, x0 - 220, 240, x0 + 220, 760, n=26, seed=14, a=0.8, size=2.2, drift=(3, 5), col="#FFF3D0" if not night else "#BFD0F5")
        # baldaken: iki yan perde
        for sg, ph in ((-1, 0.3), (1, 1.4)):
            draw_drape(c, x0 + sg * 200 - 34, 160, 68, 520, t, col="#8E2A30", col2=GOLD, amp=0.045, seed=5, ph=ph, tie=0.7)
        draw_extra(ctx, "back")

    def dyn_front(self, ctx):
        draw_extra(ctx, "front")

    def dyn_fg(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        fx = lambda x: W / 2 + (x - W / 2) * F_FG
        lit = 1.0 if ctx.tod != "day" else 0.0
        for k, x in enumerate((560, 3040)):
            for i, off in enumerate((-46, 0, 46)):
                bx = fx(x) + off
                by = 340 + 14 + (18 if off else 0) + 8
                if _vis(bx, 80, ctx.xa, ctx.xb):
                    candle(f, bx, by, 40, t, seed=5.5 + k * 3 + i, holder=False, lit=lit, smoke=False, halo=0.7, wax="#D8CDB0")
        rs = _RS(45)
        xa, xb = ctx.xa, ctx.xb
        for k in range(12):
            x = xa + ((rs.rand() * (xb - xa) + t * 12 * (0.5 + rs.rand())) % (xb - xa))
            y = 120 + rs.rand() * 700 + math.sin(t * 0.6 + k) * 14
            c.drawCircle(x, y, 1.6 + 2.0 * rs.rand(), PT("#FFEFC4", int(36 + 60 * rs.rand())))

    def light(self, ctx):
        if self.variant == "taht":
            return (1700, 480, 860.0, 1.0)
        return (self.TX0 + self.TW / 2, 560, 900.0, 1.0)


ROOMS["salon"] = Salon


# ═════════════════════════════ BANKA SALONU ═════════════════════════════
def ashlar(c, xa, xb, y0, y1, T, col="#C9B994", course=62.0, seed=1):
    """Kesme taş duvar: sıra çizgileri + kaymalı derz + tek tek ton oynaması (mutlak koordinat → kareaşlar arası kesintisiz)."""
    r0 = int(math.floor(y0 / course))
    r1 = int(math.ceil(y1 / course))
    for r in range(r0, r1 + 1):
        ya, yb = r * course, (r + 1) * course
        if yb < y0 or ya > y1:
            continue
        off = (r % 2) * course * 1.1
        bw = course * 2.2
        k0 = int(math.floor((xa - off) / bw))
        k1 = int(math.ceil((xb - off) / bw))
        for k in range(k0, k1 + 1):
            h_ = (k * 7919 + r * 104729 + seed * 31) & 0xFF
            tone = mix(col, "#3A2A18" if h_ % 3 == 0 else "#FFF4D8", 0.03 + (h_ % 5) * 0.012)
            c.drawRect(skia.Rect.MakeLTRB(off + k * bw, max(ya, y0), off + (k + 1) * bw, min(yb, y1)), PT(T(tone), 70))
            c.drawLine(off + k * bw, ya, off + k * bw + 0.5, yb, STK("#3A2A18", 1.0, 70, False))
        c.drawLine(xa, ya, xb, ya, STK("#3A2A18", 1.1, 85, False))


def draw_alcove(c, T, x, y0, w, h, seed=1, rows=3, empty=(), col="#C9B994"):
    """Kemerli raf nişi (defter/ruloların durduğu): taş çerçeve, koyu iç, raflar, sırt renkli defterler, rulolar. empty = boş bırakılan (satır, sıra) yuvalar."""
    x0, x1 = x - w / 2, x + w / 2
    r = w / 2
    yb = y0 + h
    p = skia.Path()
    p.moveTo(x0 - 16, yb + 4)
    p.lineTo(x0 - 16, y0 + r)
    p.arcTo(skia.Rect.MakeLTRB(x0 - 16, y0 - 16, x1 + 16, y0 + 2 * r + 16), 180, 180, False)
    p.lineTo(x1 + 16, yb + 4)
    p.close()
    FILLP(c, p, T(mix(col, "#FFFFFF", 0.12)), 255, 1.6, 200)
    q = skia.Path()
    q.moveTo(x0, yb)
    q.lineTo(x0, y0 + r)
    q.arcTo(skia.Rect.MakeLTRB(x0, y0, x1, y0 + 2 * r), 180, 180, False)
    q.lineTo(x1, yb)
    q.close()
    c.drawPath(q, LGP((0, y0), (0, yb), [("#2A1C12", 0.0), ("#4A3220", 1.0)]))
    c.save()
    c.clipPath(q, skia.ClipOp.kIntersect, True)
    rs = _RS(seed * 53)
    sh_h = (h - r * 0.55) / rows
    cols_b = ["#6A2E24", "#233C8C", "#2E5A3A", "#8A5A2A", "#3A2A44", "#7A2E2A", "#2F4A5A"]
    for ri in range(rows):
        ys = y0 + r * 0.55 + (ri + 1) * sh_h
        # raf tahtası
        R(c, x0, ys - 6, x1, ys + 2, T("#6E4524"))
        c.drawLine(x0, ys - 6, x1, ys - 6, STK("#C9A468", 1.2, 140, False))
        xx = x0 + 10
        k = 0
        while xx < x1 - 14:
            if (ri, k) in empty:
                xx += 40
                k += 1
                continue
            bw = rs.uniform(14, 30)
            bh = sh_h - 18 - rs.uniform(0, 16)
            if rs.rand() < 0.22:
                # rulo (yatık)
                c.drawRoundRect(skia.Rect.MakeLTRB(xx, ys - 20, xx + 44, ys - 6), 7, 7, PT("#E4D8B8")) if False else None
                rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(xx, ys - 22, xx + 46, ys - 8), 7, 7)
                c.drawRRect(rr, PT(T("#E4D8B8")))
                c.drawRRect(rr, STK(INK, 0.9, 170))
                xx += 52
            else:
                col_b = T(cols_b[rs.randint(len(cols_b))])
                if rs.rand() < 0.15 and xx + bw < x1 - 20:
                    c.save()
                    c.translate(xx + bw, ys - 6)
                    c.rotate(8)
                    BOX(c, -bw, -bh, 0, 0, col_b, T, ink=1.0)
                    c.restore()
                else:
                    BOX(c, xx, ys - 6 - bh, xx + bw, ys - 6, col_b, T, ink=1.0)
                    c.drawLine(xx + bw * 0.5, ys - 6 - bh + 8, xx + bw * 0.5, ys - 6 - 8, STK(T(GOLD), 1.0, 130, False))
                xx += bw + 3
            k += 1
    c.restore()
    c.drawPath(q, STK(INK, 1.6, 220))
    HGRAD(c, x0, y0, x1, yb, [("#000000", 0.0, 60), ("#000000", 0.25, 0)])


def balance_scale(c, x, y, s, t, seed=0.0):
    """Terazi (masa üstü): direk + ibre + iki kefe; ibre yavaşça sallanır (florin tartılıyor)."""
    ang = math.radians(3.2 * math.sin(t * 0.9 + seed) + 1.1 * math.sin(t * 2.3 + seed))
    R(c, x - 4 * s, y - 70 * s, x + 4 * s, y, "#7A5A22")
    c.drawOval(skia.Rect.MakeLTRB(x - 22 * s, y - 5 * s, x + 22 * s, y + 4 * s), PT("#5A4018"))
    px, py = x, y - 70 * s
    L = 46 * s
    ex1, ey1 = px - L * math.cos(ang), py - L * math.sin(ang)
    ex2, ey2 = px + L * math.cos(ang), py + L * math.sin(ang)
    c.drawLine(ex1, ey1, ex2, ey2, STK("#C4A04A", 3.4 * s, 255))
    c.drawLine(ex1, ey1, ex2, ey2, STK(INK, 0.9, 140))
    c.drawCircle(px, py, 4.4 * s, PT("#E8C25A"))
    for (ex, ey) in ((ex1, ey1), (ex2, ey2)):
        pw = 24 * s
        c.drawLine(ex, ey, ex - pw * 0.7, ey + 36 * s, STK("#8A6A30", 1.0, 230))
        c.drawLine(ex, ey, ex + pw * 0.7, ey + 36 * s, STK("#8A6A30", 1.0, 230))
        p = skia.Path()
        p.moveTo(ex - pw, ey + 36 * s)
        p.quadTo(ex, ey + 50 * s, ex + pw, ey + 36 * s)
        p.close()
        FILLP(c, p, "#C4A04A", 255, 1.0, 190)
    # florin kefede
    c.drawOval(skia.Rect.MakeLTRB(ex2 - 9 * s, ey2 + 28 * s, ex2 + 9 * s, ey2 + 38 * s), PT("#E8C25A"))
    c.drawOval(skia.Rect.MakeLTRB(ex2 - 9 * s, ey2 + 28 * s, ex2 + 9 * s, ey2 + 38 * s), STK("#3A2610", 0.8, 160))


def sparkle(c, x, y, a, s=1.0, col="#FFF6D0"):
    """Florin ışıltısı: dört kollu parıltı + yumuşak ışıma (a 0..1)."""
    if a <= 0.02:
        return
    r = 11 * s * (0.5 + a)
    c.drawLine(x - r, y, x + r, y, STK(col, 1.8, int(235 * a)))
    c.drawLine(x, y - r, x, y + r, STK(col, 1.8, int(235 * a)))
    c.drawLine(x - r * 0.5, y - r * 0.5, x + r * 0.5, y + r * 0.5, STK(col, 1.0, int(160 * a)))
    c.drawLine(x - r * 0.5, y + r * 0.5, x + r * 0.5, y - r * 0.5, STK(col, 1.0, int(160 * a)))
    PN.glow(c, x, y, 22 * s * (0.6 + a), "#FFE9A0", 0.55 * a)


class Banka(Room):
    """Banka salonu (kemerli taş salon): arka duvarda defter nişleri, asılı kandiller, dört masa istasyonu (oturan bankacı: yazar / florin sayar; ayakta müşteri), terazi, demir kasa.
    Parametreler: close_at (çapa) + close_dur (sn, 7): ŞUBE KAPANIŞI — kandiller sırayla söner (duman), defterler kapanır, ışık havuzu son kandile çekilir;
    empty_alcoves (boş raf yuvaları) ; customers (True)."""
    name = "banka"
    PW = 3000
    ST = [dict(x=330, act="write", seed=3), dict(x=1010, act="count", seed=8), dict(x=1690, act="write", seed=12), dict(x=2370, act="count", seed=17)]
    TW, TY, TD = 400, 700, 104
    FIG_H = 280
    LAMPS = [700, 1380, 2060, 2740]

    def build(self):
        self.gs = [TGeom(st["x"], self.TY, self.TW, self.TD, 0.05) for st in self.ST]
        self.layer("wall", F_WALL, self.Lw(F_WALL), self._draw_wall, wear=3)
        self.layer("main", 1.0, self.PW, self._draw_main, scale=1.2)
        self.layer("front", 1.0, self.PW, self._draw_front)
        self.layer("fg", F_FG, self.Lw(F_FG), self._draw_fg)

    def paths(self):
        return {
            "default": [(0.0, (1100, 0, 1.0)), (1.0, (1900, 0, 1.1))],
            "sweep_r": [(0.0, (1000, 0, 1.0)), (1.0, (2000, 0, 1.0))],
            "sweep_l": [(0.0, (2000, 0, 1.0)), (1.0, (1000, 0, 1.0))],
            "corner": [(0.0, (900, 40, 1.15)), (1.0, (620, 70, 1.5))],      # c1: Giovanni'nin köşesi
            "count": [(0.0, (1300, 20, 1.2)), (1.0, (1120, 80, 1.9))],
            "close": [(0.0, (1000, 0, 1.0)), (0.5, (1700, 0, 1.0)), (1.0, (2400, 10, 1.1))],
            "in": [(0.0, (1000, 0, 1.0)), (1.0, (1000 + 5, 80, 1.8))],
        }

    def _close_info(self, ctx):
        o = self.opts
        if "close_at" not in o:
            return 0.0, [1.0] * 4, 0.0
        tc = ctx.cx.at(o["close_at"])
        d = float(o.get("close_dur", 7.0))
        lits, k = [], clamp((ctx.t - tc) / d)
        for i in range(4):
            ti = tc + d * (i + 0.5) / 4.0 * 0.92
            lits.append(1.0 - smooth(clamp((ctx.t - ti) / 0.9)))
        return k, lits, tc

    def default_actors(self, ctx=None):
        out = []
        if not self.opts.get("customers", True):
            return out
        for i, st in enumerate(self.ST):
            out.append(dict(kind=["tuccar", "soylu", "halk", "soylu_f"][i % 4], x=st["x"] + self.TW + 74, y=self.TY + 124 + (i % 2) * 6, h=262, action="talk", dir=-1, seed=40 + i,
                            phase=0.2 * i, energy=1.0, prop="sack" if i % 2 == 0 else None, layer="back"))
        return out

    # ── statik ───────────────────────────────────────────────────────────
    def _draw_wall(self, fr, xa, xb):
        c, T = fr.c, self.T
        night = self.tod == "night"
        wx = self.wx
        GRAD_V(c, xa, OV - 40, xb, Y_FL + 30, [(T("#BFB090"), 0.0), (T("#D2C4A2"), 1.0)])
        ashlar(c, xa, xb, OV - 40, Y_FL + 30, T, "#CFC09C", 64.0, seed=2)
        w = int(xb - xa) + 1
        h = int(Y_FL + 30 - (OV - 40)) + 1
        f_ = noise_field(xa, OV - 40, w, h, 1, 10, 4)
        arr = np.zeros((h, w, 4), np.uint8)
        arr[..., 0] = np.where(f_ > 0, 255, 90)
        arr[..., 1] = np.where(f_ > 0, 246, 62)
        arr[..., 2] = np.where(f_ > 0, 220, 36)
        arr[..., 3] = np.clip(np.abs(f_) * 18, 0, 70).astype(np.uint8)
        c.drawImage(sk.np_to_image(np.ascontiguousarray(arr)), xa, OV - 40, LIN)
        cornice(c, xa, xb, 72, T, col="#8A7650", plaster="#D8CBA8")
        for i in range(5):
            x = 330 + 600 * i
            if _vis(wx(x), 200, xa, xb):
                draw_alcove(c, T, wx(x), 250, 320, 340, seed=i + 1, rows=3, empty=((1, 2),) if i == 3 else ())
        for i in range(4):
            x = 630 + 600 * i
            if _vis(wx(x), 100, xa, xb):
                draw_window(c, T, wx(x), 150, 110, 250, night=night, shutters=False, mullion=True)
        # lambri/taş kaide
        wainscot(c, xa, xb, Y_FL - 70, Y_FL + 18, T, "#7A5A3A", pw=190, seed=4)
        sh = LGP((0, Y_FL - 30), (0, Y_FL + 30), [("#1A0F06", 0.0, 0), ("#1A0F06", 1.0, 70)])
        c.drawRect(skia.Rect.MakeLTRB(xa, Y_FL - 30, xb, Y_FL + 30), sh)

    def _draw_main(self, fr, xa, xb):
        c, T = fr.c, self.T
        floor_tiles(c, xa, xb, Y_FL, LH, T, "#A39278", "#8E7E66", seed=6, w0=84.0, grow=1.13)
        # kasa (demir bantlı sandık) sağ uçta
        if _vis(2860, 140, xa, xb):
            draw_chest(c, T, 2780, 2960, 800, 150, "#4A3A2A")
            for xx in (2800, 2870, 2940):
                R(c, xx - 5, 668, xx + 5, 790, "#2A2622")
                c.drawCircle(xx, 690, 3, PT("#6A6258"))
                c.drawCircle(xx, 770, 3, PT("#6A6258"))
        for st in self.ST:
            if _vis(st["x"] + 200, 420, xa, xb):
                rug(c, st["x"] - 90, st["x"] + self.TW + 120, 752, 866, T, field="#6A2E24", border="#233C8C")
        for st in self.ST:
            fx_ = st["x"] - 34
            if _vis(fx_, 80, xa, xb):
                draw_chair(c, T, fx_ - 24, self.TY + 117 - 8, 250, 72, 90, facing=1, col="#5E3A20", cushion="#6A2E24")

    def _draw_front(self, fr, xa, xb):
        c, T = fr.c, self.T
        for st, g in zip(self.ST, self.gs):
            if _vis(st["x"] + self.TW / 2, self.TW / 2 + 80, xa, xb):
                table_front(c, g, self.TY + 112, T, ("#2E5A3A", "#D2A33E"), apron=30)

    def _draw_fg(self, fr, xa, xb):
        c, T = fr.c, self.T
        fx = lambda x: W / 2 + (x - W / 2) * F_FG
        for x in (610, 2250):
            if _vis(fx(x), 80, xa, xb):
                xx = fx(x)
                R(c, xx - 30, OV - 40, xx + 30, 900, "#2A2018")
                HGRAD(c, xx - 30, OV - 40, xx + 30, 900, [("#FFFFFF", 0.0, 34), ("#000000", 0.45, 0), ("#000000", 1.0, 100)])
                INKR(c, xx - 30, OV - 40, xx + 30, 900, 1.5, 200)
                for yy in (140, 168, 190):
                    R(c, xx - 44, yy, xx + 44, yy + (20 if yy == 140 else 12), "#3A2E22")
                    INKR(c, xx - 44, yy, xx + 44, yy + (20 if yy == 140 else 12), 1.2, 200)
                R(c, xx - 42, 820, xx + 42, 900, "#32261A")
                INKR(c, xx - 42, 820, xx + 42, 900, 1.4, 200)
                for k in range(-2, 3):
                    c.drawLine(xx + k * 12, 210, xx + k * 12, 812, STK("#000000", 1.0, 40, False))

    # ── canlı ────────────────────────────────────────────────────────────
    def dyn_wall(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        wx = self.wx
        night = ctx.tod == "night"
        for i in range(4):
            x = 630 + 600 * i
            if _vis(wx(x), 400, ctx.xa, ctx.xb):
                window_light(f, wx(x), 168, 90, 210, t, dx=260, y_floor=Y_FL + 20, a=0.22 if ctx.tod == "day" else 0.08, seed=i + 4, patch=False, dust=8, night=night, part="shaft")

    def dyn_main(self, ctx):
        f, c, t, cx = ctx.f, ctx.c, ctx.t, ctx.cx
        T = self.T
        night = ctx.tod != "day"
        kc, lits, tc = self._close_info(ctx)
        for i in range(4):
            x = 630 + 600 * i
            if _vis(x, 400, ctx.xa, ctx.xb) and ctx.tod == "day":
                window_light(f, x, 168, 90, 210, t, dx=260, y_floor=Y_FL + 60, a=0.22, seed=i + 4, patch=True, dust=0, part="patch", patch_h=100)
        # asılı kandiller
        for i, x in enumerate(self.LAMPS):
            if _vis(x, 120, ctx.xa, ctx.xb):
                lit = (lits[i] if night else 0.0)
                oil_lamp(f, x - 16, 300, 34, t, seed=i * 2.7, lit=lit, hang=300 - 34 * 0.9 - 62)
                if night and lits[i] < 0.98 and "close_at" in self.opts:
                    # sönen kandilden duman
                    for q in range(5):
                        ph = (t * 0.28 + q / 5.0 + i * 0.17) % 1.0
                        FA._puff(c, x + 14 + math.sin(ph * 6 + q) * (5 + 14 * ph), 270 - ph * 160, 5 + 20 * ph, 0.32 * (1 - ph) ** 1.3 * (1.0 - lits[i]), "#C8C0B0")
        # istasyonlar
        closed_n = 0
        for si, (st, g) in enumerate(zip(self.ST, self.gs)):
            if not _vis(st["x"] + 200, 560, ctx.xa, ctx.xb):
                continue
            table_top(c, g, T, ("#2E5A3A", "#D2A33E"))
            fig_x = st["x"] - 34
            fy = self.TY + 117
            # defter kapanışı: bu istasyonun kendi zamanı
            tcl = tc + (si + 0.3) * float(self.opts.get("close_dur", 7.0)) / 4.0 * 0.9 if "close_at" in self.opts else 1e9
            kb = clamp((t - tcl) / 0.7)
            open_desk = kb < 0.02
            if st["act"] == "count":
                tt0 = st["seed"] * 0.37
                ex = seated(f, "banker", fig_x, fy, self.FIG_H, t, "count", 1, seed=st["seed"], phase=(si * 0.21) % 1.0, t0=tt0, desk_top=open_desk)
                cn = ex.get("coins")
                if cn and open_desk:
                    s_, hb_ = ex["s"], ex["hb"]
                    ydesk = fy - 0.415 * hb_ * s_
                    xt = fig_x + cn["xb"] * s_
                    if 0.70 < cn["u"] < 0.95:
                        a = math.sin((cn["u"] - 0.70) / 0.25 * math.pi)
                        sparkle(c, xt + 6, ydesk - cn["stackh"] * s_ - 8, a, 1.0)
                    if night and (int(t * 2.3 + si) % 3 == 0):
                        sparkle(c, fig_x + cn["xa"] * s_ - 4, ydesk - 24, 0.5 + 0.5 * math.sin(t * 7 + si), 0.8)
            else:
                seated(f, "banker", fig_x, fy, self.FIG_H, t, "write", 1, seed=st["seed"], phase=(si * 0.21) % 1.0, t0=0.0, desk_top=open_desk)
            if not open_desk:
                self._closed_ledger(c, fig_x, fy, kb, si)
            # tabla eşyaları
            if si == 1:
                bx, by = g.pt(0.74, 0.55)
                balance_scale(c, bx, by, 0.82, t, seed=si)
            if si == 3:
                bx, by = g.pt(0.60, 0.5)
                draw_coins(c, bx, by, 18, 1.1, t, 5, True)
            if si in (0, 2):
                ix, iy = g.pt(0.78, 0.45)
                draw_coins(c, ix, iy, 5 + si * 2, 1.0, t, 9 + si, True)
        draw_extra(ctx, "back")

    def _closed_ledger(self, c, fig_x, fy, kb, si):
        """Kapanan defter: sayfa çevrilir (kb 0..1), sonra kapalı defter masada kalır."""
        hb = 280.0
        yt = fy - 0.415 * hb
        x0 = fig_x + 0.20 * hb
        x1 = fig_x + 0.40 * hb
        if kb < 1.0:
            # sayfa dönüyor: sağ sayfa sola dikey eksende daralır
            xm = (x0 + x1) / 2
            wd = (x1 - x0) / 2
            k = math.cos(kb * math.pi)
            p = sk.poly_path([(xm, yt), (xm + wd * k, yt - 0.03 * hb * abs(math.sin(kb * math.pi)) - 3), (xm + wd * k, yt - 0.026 * hb - 12 * abs(math.sin(kb * math.pi))), (xm, yt - 0.02 * hb)])
            FILLP(c, p, "#EDE4C8", 255, 1.0, 170)
        BOX(c, x0 + 4, yt - 0.034 * hb, x1 - 2, yt, "#6A2E24", OTint("day"), ink=1.1, a=int(255 * smooth(kb)))
        c.drawLine(x0 + 4, yt - 0.017 * hb, x1 - 2, yt - 0.017 * hb, STK(GOLD, 1.0, int(160 * smooth(kb)), False))

    def dyn_front(self, ctx):
        draw_extra(ctx, "front")

    def dyn_fg(self, ctx):
        c, t = ctx.c, ctx.t
        rs = _RS(46)
        xa, xb = ctx.xa, ctx.xb
        for k in range(12):
            x = xa + ((rs.rand() * (xb - xa) + t * 12 * (0.5 + rs.rand())) % (xb - xa))
            y = 120 + rs.rand() * 700 + math.sin(t * 0.6 + k) * 14
            c.drawCircle(x, y, 1.6 + 2.0 * rs.rand(), PT("#FFEFC4", int(34 + 56 * rs.rand())))

    def light(self, ctx):
        kc, lits, tc = self._close_info(ctx)
        tot = sum(lits)
        if tot < 0.02:
            return (self.LAMPS[-1] - 16, 330, 30.0, 1.0)
        cxl = sum(l * x for l, x in zip(lits, self.LAMPS)) / tot
        return (cxl - 16, 330, 520.0 + 560.0 * (tot / 4.0), 1.0)

    def after_finish(self, ctx):
        """Karanlık havuzun ÜSTÜNE kandil başına küçük sıcak ışıma (her kandil kendi çevresini aydınlatır)."""
        if ctx.tod != "night":
            return
        c = ctx.c
        kc, lits, tc = self._close_info(ctx)
        z = ctx.z
        for i, x in enumerate(self.LAMPS):
            if lits[i] > 0.02:
                sx, sy = ctx.to_screen(1.0, x + 6, 300)
                if -300 < sx < W + 300:
                    PN.glow(c, sx, sy + 30 * z, 320 * z, "#FFB454", 0.20 * lits[i])


ROOMS["banka"] = Banka


# ═════════════════════════════ ÇALIŞMA ODALARI: hücre · kütüphane · studiolo ═════════════════════════════
def draw_lectern(c, T, x, yb, w=130, h=190, col="#6E4524"):
    """Okuma kürsüsü (yan görünüm): iki bacak, alt raf, eğimli tabla; üstünde açık elyazması + zincir."""
    SOFT(c, x, yb + 3, w * 0.7, 9, "#000000", 80)
    for dx in (-w * 0.36, w * 0.36):
        p = skia.Path()
        p.moveTo(x + dx - 7, yb)
        p.lineTo(x + dx * 0.8 - 6, yb - h + 20)
        p.lineTo(x + dx * 0.8 + 6, yb - h + 20)
        p.lineTo(x + dx + 7, yb)
        p.close()
        FILLP(c, p, T(col), 255, 1.2, 190)
    BOX(c, x - w * 0.40, yb - h * 0.34, x + w * 0.40, yb - h * 0.34 + 10, col, T, ink=1.1)
    top = sk.poly_path([(x - w / 2, yb - h + 22), (x + w / 2, yb - h + 2), (x + w / 2 + 2, yb - h + 18), (x - w / 2 - 2, yb - h + 40)])
    FILLP(c, top, T(mix(col, "#FFFFFF", 0.10)), 255, 1.4, 200)
    # açık elyazması
    bx0, bx1 = x - w * 0.36, x + w * 0.36
    for sg in (0, 1):
        xa_, xb_ = (bx0, x) if sg == 0 else (x, bx1)
        ya0 = yb - h + 22 - (xa_ - (x - w / 2)) / w * 20
        yb0 = yb - h + 22 - (xb_ - (x - w / 2)) / w * 20
        p = sk.poly_path([(xa_, ya0 + 8), (xb_, yb0 + 8), (xb_, yb0 - 16), (xa_, ya0 - 16)])
        FILLP(c, p, T("#EDE4C8"), 255, 1.0, 170)
        for k in range(5):
            u = (k + 1) / 6
            c.drawLine(xa_ + 4, ya0 - 16 + 24 * u, xb_ - 4, yb0 - 16 + 24 * u, STK("#4A3A22", 0.9, 140))
    c.drawLine(x, yb - h + 22, x, yb - h + 2, STK("#8A2A1C", 2.0, 220))
    # zincir
    pth = skia.Path()
    pth.moveTo(x + w * 0.3, yb - h + 12)
    pth.quadTo(x + w * 0.5, yb - h * 0.55, x + w * 0.42, yb - h * 0.36)
    c.drawPath(pth, STK("#6A6258", 1.6, 220))


def draw_bookcase(c, T, x, y0, w, h, rows=5, seed=1, empty_frac=0.0, col="#5E3A20", tall=True):
    """Kitaplık (önden): ahşap çerçeve, bölmeli raflar (göz), sırtları renkli/yaldız çizgili ciltler, rulolar. empty_frac: boş (karanlık, toz izli) yuva oranı."""
    x0, x1 = x - w / 2, x + w / 2
    yb = y0 + h
    BOX(c, x0 - 14, y0 - 14, x1 + 14, yb + 6, col, T, hl=0.10, sh=0.18, ink=1.6)
    R(c, x0, y0, x1, yb, T("#2A1C12"))
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, yb), LGP((0, y0), (0, yb), [("#1A100A", 0.0, 255), ("#3A2818", 1.0, 255)]))
    rs = _RS(seed * 71)
    rh = h / rows
    ncol = max(2, int(w / 118))
    cw = w / ncol
    cols_b = ["#6A2E24", "#233C8C", "#2E5A3A", "#8A5A2A", "#3A2A44", "#7A2E2A", "#2F4A5A", "#9A7A3A", "#4A2A1A"]
    for r_ in range(rows):
        ys = y0 + (r_ + 1) * rh
        for k in range(ncol):
            xa_, xb_ = x0 + k * cw + 3, x0 + (k + 1) * cw - 3
            if rs.rand() < empty_frac:
                # boş yuva: karanlık + toz izleri + tek yaslı kitap izi
                c.drawRect(skia.Rect.MakeLTRB(xa_, ys - rh + 6, xb_, ys - 6), PT("#120A06", 200))
                for q in range(3):
                    xx = xa_ + rs.uniform(8, cw - 14)
                    c.drawLine(xx, ys - 10, xx + rs.uniform(-2, 2), ys - rs.uniform(30, rh - 22), STK("#8A7A60", rs.uniform(0.8, 2.2), int(rs.uniform(14, 34))))
                continue
            xx = xa_ + 3
            while xx < xb_ - 8:
                if rs.rand() < 0.14:
                    rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(xx, ys - 26, min(xb_, xx + 40), ys - 8), 8, 8)
                    c.drawRRect(rr, PT(T("#E4D8B8")))
                    c.drawRRect(rr, STK(INK, 0.9, 170))
                    xx += 44
                    continue
                bw = rs.uniform(12, 24)
                bh = rh - 22 - rs.uniform(0, rh * 0.28)
                colb = T(cols_b[rs.randint(len(cols_b))])
                if xx + bw > xb_ - 4:
                    break
                BOX(c, xx, ys - 8 - bh, xx + bw, ys - 8, colb, T, ink=0.9, hl=0.14, sh=0.2)
                c.drawLine(xx + 2, ys - 8 - bh + 8, xx + bw - 2, ys - 8 - bh + 8, STK(T(GOLD), 0.9, 150, False))
                c.drawLine(xx + 2, ys - 8 - 8, xx + bw - 2, ys - 8 - 8, STK(T(GOLD), 0.9, 120, False))
                xx += bw + 1.5
        R(c, x0, ys - 6, x1, ys + 2, T("#6E4524"))
        c.drawLine(x0, ys - 6, x1, ys - 6, STK("#C9A468", 1.1, 130, False))
    for k in range(1, ncol):
        R(c, x0 + k * cw - 3, y0, x0 + k * cw + 3, yb, T("#6E4524"))
    INKR(c, x0, y0, x1, yb, 1.4, 210)
    HGRAD(c, x0, y0, x1, yb, [("#000000", 0.0, 70), ("#000000", 0.18, 0), ("#000000", 0.85, 0), ("#000000", 1.0, 60)])


PAINT_COLS = ["#B8884A", "#7A8A5A", "#9A5A3A", "#5A7A8A", "#A89060", "#6A4A5A"]


def cabinet_wall(c, T, xa, xb, y0, y1, seed=1, pw=150.0):
    """Studiolo duvarı: boyalı dolap kapıları (iki sıra panel, her birinde küçük boyalı motif) + altında çekmece sırası (topuzlu). Kesintisiz (mutlak x)."""
    R(c, xa, y0, xb, y1, T("#3A2A1A"))
    i0 = int(math.floor(xa / pw)) - 1
    i1 = int(math.ceil(xb / pw)) + 1
    ph = (y1 - y0 - 150) / 2
    for i in range(i0, i1 + 1):
        for r_ in range(2):
            px0, px1 = i * pw + 8, (i + 1) * pw - 8
            py0 = y0 + 8 + r_ * (ph + 6)
            py1 = py0 + ph - 8
            h_ = (i * 7919 + r_ * 104729 + seed * 31) & 0xFF
            colp = PAINT_COLS[h_ % len(PAINT_COLS)]
            BOX(c, px0, py0, px1, py1, "#6E4524", T, hl=0.10, sh=0.16, ink=1.3)
            c.drawRect(skia.Rect.MakeLTRB(px0 + 9, py0 + 9, px1 - 9, py1 - 9), LGP((0, py0), (0, py1), [(T(mix(colp, "#FFFFFF", 0.18)), 0.0), (T(colp), 1.0)]))
            INKR(c, px0 + 9, py0 + 9, px1 - 9, py1 - 9, 1.0, 190)
            cx_, cy_ = (px0 + px1) / 2, (py0 + py1) / 2
            m = h_ % 4
            if m == 0:      # güneş + tepe
                c.drawCircle(cx_ + 18, cy_ - 22, 16, PT(T("#F0D27A")))
                c.drawPath(sk.poly_path([(px0 + 9, py1 - 9), (cx_ - 14, cy_ + 6), (cx_ + 24, py1 - 9)]), PT(T("#4A6A3A")))
            elif m == 1:    # gemi
                c.drawPath(sk.poly_path([(cx_ - 30, cy_ + 26), (cx_ + 30, cy_ + 26), (cx_ + 20, cy_ + 40), (cx_ - 20, cy_ + 40)]), PT(T("#5A3A20")))
                c.drawPath(sk.poly_path([(cx_, cy_ - 36), (cx_ + 26, cy_ + 20), (cx_, cy_ + 20)]), PT(T("#F4EEDC")))
                c.drawLine(cx_, cy_ - 38, cx_, cy_ + 26, STK(INK, 1.4, 220))
            elif m == 2:    # çiçek/yıldız
                for k in range(8):
                    a = k * math.pi / 4
                    c.drawCircle(cx_ + math.cos(a) * 20, cy_ + math.sin(a) * 20, 8, PT(T("#C84A38")))
                c.drawCircle(cx_, cy_, 9, PT(T("#F0D27A")))
            else:           # ağaç
                c.drawRect(skia.Rect.MakeLTRB(cx_ - 4, cy_ + 4, cx_ + 4, py1 - 14), PT(T("#5A3A20")))
                c.drawCircle(cx_, cy_ - 8, 26, PT(T("#3E7A4A")))
            c.drawCircle(px1 - 18 if (i + r_) % 2 else px0 + 18, cy_ + ph * 0.28, 4, PT(T(GOLD)))
    # çekmeceler
    dy0 = y1 - 140
    R(c, xa, dy0, xb, y1, T("#4A3220"))
    c.drawLine(xa, dy0, xb, dy0, STK(INK, 1.4, 200, False))
    dw = 112.0
    for i in range(int(math.floor(xa / dw)) - 1, int(math.ceil(xb / dw)) + 1):
        for r_ in range(2):
            qx0, qx1 = i * dw + 6, (i + 1) * dw - 6
            qy0 = dy0 + 8 + r_ * 62
            BOX(c, qx0, qy0, qx1, qy0 + 54, "#6E4524", T, hl=0.14, sh=0.16, ink=1.1)
            c.drawCircle((qx0 + qx1) / 2, qy0 + 27, 4.2, PT(T(GOLD)))
            c.drawCircle((qx0 + qx1) / 2, qy0 + 27, 4.2, STK(INK, 0.8, 190))


def furnace(c, T, x, yb, w=190, h=210):
    """Tuğla ocak (kimya): kemerli ateş gözü (içi koyu; ateş canlı çizilir), üstte tuğla dolgu, yan baca borusu."""
    SOFT(c, x, yb + 4, w * 0.7, 10, "#000000", 90)
    BOX(c, x - w / 2, yb - h, x + w / 2, yb, "#8A4A32", T, hl=0.12, sh=0.22, ink=1.5)
    for r_ in range(int(h / 22)):
        yy = yb - h + r_ * 22
        c.drawLine(x - w / 2, yy, x + w / 2, yy, STK("#3A1A10", 1.0, 110, False))
        off = (r_ % 2) * 26
        for xx in np.arange(x - w / 2 + off, x + w / 2, 52):
            c.drawLine(xx, yy, xx, yy + 22, STK("#3A1A10", 1.0, 90, False))
    ox0, ox1 = x - w * 0.28, x + w * 0.28
    oy1, oy0 = yb - 6, yb - h * 0.52
    p = skia.Path()
    p.moveTo(ox0, oy1)
    p.lineTo(ox0, oy0 + (ox1 - ox0) / 2)
    p.arcTo(skia.Rect.MakeLTRB(ox0, oy0, ox1, oy0 + (ox1 - ox0)), 180, 180, False)
    p.lineTo(ox1, oy1)
    p.close()
    c.drawPath(p, PT("#140A06"))
    INKP(c, p, 2.0, 230)
    # baca
    R(c, x + w / 2 - 34, yb - h - 110, x + w / 2 - 6, yb - h, T("#7A4430"))
    INKR(c, x + w / 2 - 34, yb - h - 110, x + w / 2 - 6, yb - h, 1.3, 200)
    return (x, (oy0 + oy1) / 2 + 20, ox1 - ox0, oy1 - oy0)


def furnace_fire(f, x, y, w, t, seed=0.0, lit=1.0):
    """Ocak ateşi: titreyen alev dilleri + közler + ışıma."""
    c = f.c
    if lit <= 0.02:
        return
    PN.glow(c, x, y, w * 1.5, "#FF8A2A", 0.45 * lit)
    for k in range(5):
        u = (k - 2) / 2.5
        fl, lean, br = flicker(t * 1.3 + k * 0.7, seed + k)
        fh = (46 + 22 * (1 - abs(u))) * fl * lit
        bx = x + u * w * 0.36
        c.drawPath(_flame_path(bx, y + 28, fh, 30, lean * fh * 0.3), PT("#FF8A2A", 240))
        c.drawPath(_flame_path(bx, y + 28, fh * 0.72, 18, lean * fh * 0.2), PT("#FFD66B", 250))
    c.drawOval(skia.Rect.MakeLTRB(x - w * 0.38, y + 24, x + w * 0.38, y + 40), PT("#6A1E0A", 230))
    rs = _RS(int(seed * 10) + 3)
    for k in range(7):
        c.drawCircle(x + rs.uniform(-w * 0.3, w * 0.3), y + 32 + rs.uniform(-3, 4), 2.0 + 1.2 * abs(math.sin(t * 5 + k)), PT("#FFB04A", int(210 * lit)))


def alembic(f, x, y, s, t, lit=1.0, col="#6E9A8A"):
    """Damıtma düzeneği (kimya): yuvarlak balon + uzun boyun + eğik damıtma borusu + alıcı şişe; sıvı kabarcıklanır, buhar yükselir, damlalar akar. (x,y) = balon altı."""
    c = f.c
    r = 34 * s
    # balon
    bal = skia.Path()
    bal.addCircle(x, y - r, r)
    c.drawPath(bal, PT("#DDEAE6", 110))
    c.save()
    c.clipPath(bal, skia.ClipOp.kIntersect, True)
    c.drawRect(skia.Rect.MakeLTRB(x - r, y - r * 1.1 + math.sin(t * 2.5) * 1.5, x + r, y), PT(col, 215))
    for q in range(6):
        ph = (t * 0.8 * (0.6 + 0.2 * q) + q / 6.0) % 1.0
        c.drawCircle(x + math.sin(ph * 9 + q) * r * 0.5, y - 4 * s - ph * r * 1.1, (1.6 + 2.0 * ph) * s, PT("#FFFFFF", int(210 * (1 - ph) * lit + 20)))
    c.restore()
    INKP(c, bal, 1.4, 200)
    # boyun + boru
    neck = skia.Path()
    neck.moveTo(x - 7 * s, y - r * 1.9)
    neck.lineTo(x - 7 * s, y - r * 2.9)
    neck.cubicTo(x - 7 * s, y - r * 3.4, x + 30 * s, y - r * 3.6, x + 74 * s, y - r * 2.9)
    c.drawPath(neck, STK("#DDEAE6", 11 * s, 150))
    c.drawPath(neck, STK(INK, 1.1, 190))
    tube = skia.Path()
    tube.moveTo(x + 74 * s, y - r * 2.9)
    tube.lineTo(x + 112 * s, y - r * 1.3)
    c.drawPath(tube, STK("#DDEAE6", 9 * s, 150))
    c.drawPath(tube, STK(INK, 1.0, 190))
    # alıcı şişe
    rx, ry = x + 118 * s, y
    rp = skia.Path()
    rp.moveTo(rx - 5 * s, ry - r * 1.0)
    rp.lineTo(rx - 5 * s, ry - r * 0.7)
    rp.quadTo(rx - 22 * s, ry - r * 0.5, rx - 22 * s, ry - 2)
    rp.lineTo(rx + 22 * s, ry - 2)
    rp.quadTo(rx + 22 * s, ry - r * 0.5, rx + 5 * s, ry - r * 0.7)
    rp.lineTo(rx + 5 * s, ry - r * 1.0)
    rp.close()
    c.drawPath(rp, PT("#DDEAE6", 120))
    fill = (0.18 + 0.12 * (0.5 + 0.5 * math.sin(t * 0.2))) * r
    c.drawRect(skia.Rect.MakeLTRB(rx - 21 * s, ry - 2 - fill, rx + 21 * s, ry - 2), PT(col, 200))
    INKP(c, rp, 1.2, 190)
    dr = (t * 1.6) % 1.0
    c.drawOval(skia.Rect.MakeLTRB(rx - 2, ry - r * 1.3 + dr * r * 0.9, rx + 2, ry - r * 1.3 + dr * r * 0.9 + 6), PT(col, int(220 * (1 - dr * 0.5))))
    # buhar
    for q in range(5):
        ph = (t * 0.32 + q / 5.0) % 1.0
        FA._puff(c, x + 10 * s + math.sin(ph * 5 + q) * 8 * s, y - r * 3.2 - ph * 80 * s, (5 + 20 * ph) * s, 0.30 * (1 - ph) ** 1.2 * lit, "#E8E8E8")


def armillary(f, x, y, r, t, seed=0.0):
    """Armiller küre (merak kabini): sabit ayak + eğik eksen; halkalar yavaş döner (elips genişliği salınır)."""
    c = f.c
    c.drawRect(skia.Rect.MakeLTRB(x - 3, y, x + 3, y + r * 0.9), PT("#6E4524"))
    c.drawOval(skia.Rect.MakeLTRB(x - r * 0.5, y + r * 0.85, x + r * 0.5, y + r * 1.05), PT("#6E4524"))
    c.drawOval(skia.Rect.MakeLTRB(x - r * 0.5, y + r * 0.85, x + r * 0.5, y + r * 1.05), STK(INK, 1.0, 190))
    c.save()
    c.translate(x, y)
    c.rotate(-23)
    for k in range(4):
        ph = t * 0.55 + k * 0.8 + seed
        rx = max(0.08, abs(math.cos(ph))) * r
        c.drawOval(skia.Rect.MakeLTRB(-rx, -r, rx, r), STK("#C4A04A", 3.2, 255))
        c.drawOval(skia.Rect.MakeLTRB(-rx, -r, rx, r), STK(INK, 0.9, 120))
    c.drawOval(skia.Rect.MakeLTRB(-r, -r * 0.18, r, r * 0.18), STK("#C4A04A", 3.2, 255))
    c.drawCircle(0, 0, r * 0.22, PT("#3E7A8A"))
    c.drawCircle(0, 0, r * 0.22, STK(INK, 1.0, 190))
    c.drawLine(0, -r * 1.18, 0, r * 1.18, STK("#8A6A30", 2.4, 255))
    c.restore()


def shell(c, x, y, s=1.0, col="#E8D2B0"):
    """Deniz kabuğu (spiral, kıvrımlı); merak kabini eşyası."""
    p = skia.Path()
    p.moveTo(x - 18 * s, y)
    p.cubicTo(x - 20 * s, y - 24 * s, x + 6 * s, y - 34 * s, x + 20 * s, y - 14 * s)
    p.cubicTo(x + 28 * s, y - 4 * s, x + 12 * s, y + 2 * s, x - 18 * s, y)
    FILLP(c, p, col, 255, 1.1, 190, shader=LGP((x - 20 * s, y - 30 * s), (x + 24 * s, y), [("#FFF4E0", 0.0), (col, 0.5), ("#B8956A", 1.0)]))
    for k in range(4):
        c.drawLine(x - 14 * s + k * 8 * s, y - 2 * s, x - 6 * s + k * 6 * s, y - 24 * s + k * 3 * s, STK("#8A6A40", 0.9, 150))


def coral(c, x, y, s=1.0, col="#C84A38"):
    """Mercan dalı."""
    def br(x0, y0, ang, L, d):
        if d == 0 or L < 5:
            return
        x1, y1 = x0 + math.sin(ang) * L, y0 - math.cos(ang) * L
        c.drawLine(x0, y0, x1, y1, STK(col, max(1.6, L * 0.17), 255))
        br(x1, y1, ang - 0.5, L * 0.68, d - 1)
        br(x1, y1, ang + 0.45, L * 0.66, d - 1)
    br(x, y, 0.0, 26 * s, 4)


class Calisma(Room):
    """Çalışma odaları. variant="hucre" (San Marco hücresi: yağ kandili, ahşap yazı masası, sade yatak, küçük pencere; figure="desk"|"kneel" KUKULETALI SİLUET),
    "kutuphane" (Niccoli/Medici kütüphanesi: kitaplık nişleri, okuma kürsüleri, yazıcı; variant "bos"/empty_frac → BOŞ RAF YUVALARI, c10 V1),
    "studiolo" (Francesco I: dolap duvarı, çekmeceler, DÖRT BÖLGE: ofis · laboratuvar · saklanma yeri · merak kabini; zone_at=[a,b,c,d] kamera/ışık turu; ZONES)."""
    name = "calisma"

    def __init__(self, variant, tod):
        v = variant or "hucre"
        self.PW = {"hucre": 2300, "kutuphane": 3200, "studiolo": 3600}.get(v, 2400)
        self.always_lit = v == "studiolo"
        super().__init__(v, tod)

    ZONES = {"studiolo": [(760, 240, 1240, 800), (1420, 240, 2040, 800), (2130, 240, 2370, 800), (2570, 240, 2910, 800)]}

    def build(self):
        v = self.variant
        if v == "hucre":
            self.g = TGeom(980, 706, 430, 96, 0.04)
            self.CH_X = 930
            self.lamp_xy = None
        elif v == "kutuphane":
            self.g = TGeom(1400, 706, 420, 104, 0.04)
        else:
            self.g = TGeom(830, 706, 380, 96, 0.04)
        self.layer("wall", F_WALL, self.Lw(F_WALL), self._draw_wall, wear=3 if v != "studiolo" else 0)
        self.layer("main", 1.0, self.PW, self._draw_main, scale=1.2)
        self.layer("front", 1.0, self.PW, self._draw_front)
        self.layer("fg", F_FG, self.Lw(F_FG), self._draw_fg)

    # ── yollar ───────────────────────────────────────────────────────────
    def paths(self):
        v = self.variant
        if v == "hucre":
            lx, ly = self.lamp_pos()
            return {"default": [(0.0, (1050, 0, 1.0)), (1.0, (1250, 0, 1.12))],
                    "in": [(0.0, (1150, 0, 1.0)), (1.0, (lx, ly - 470 + 10, 2.6))],
                    "lamp": [(0.0, (lx, ly - 470 + 10, 2.0)), (1.0, (lx, ly - 470 + 10, 2.6))],
                    "sweep_r": [(0.0, (1000, 0, 1.04)), (1.0, (1500, 0, 1.04))],
                    "pull": [(0.0, (lx, ly - 470, 2.2)), (1.0, (1150, 0, 1.0))]}
        if v == "kutuphane":
            return {"default": [(0.0, (1100, 0, 1.0)), (1.0, (2100, 0, 1.0))],
                    "sweep_r": [(0.0, (1000, 0, 1.0)), (1.0, (2200, 0, 1.0))],
                    "sweep_l": [(0.0, (2200, 0, 1.0)), (1.0, (1000, 0, 1.0))],
                    "scribe": [(0.0, (1300, 0, 1.0)), (1.0, (1560, 60, 1.6))],
                    "in": [(0.0, (1000, 0, 1.0)), (0.6, (1500, 20, 1.3)), (1.0, (1620, 90, 2.1))]}
        return {"default": [(0.0, (1800, 0, 1.0)), (1.0, (1800, 0, 1.0))],
                "tour": [(0.0, (960, 40, 1.35)), (0.33, (1760, 40, 1.35)), (0.66, (2250, 40, 1.35)), (1.0, (2740, 40, 1.35))],
                "sweep_r": [(0.0, (960, 0, 1.0)), (1.0, (2640, 0, 1.0))],
                "wide": [(1.0, (1800, 0, 1.0)), (0.0, (1800, 0, 1.0))]}

    def zone_centers(self):
        return [((z[0] + z[2]) / 2, (z[1] + z[3]) / 2) for z in self.ZONES.get(self.variant, [])]

    def cams_for(self, cx, path, opts):
        if self.variant == "studiolo" and "zone_at" in opts and (path in (None, "tour", "default")):
            ks = []
            for i, a in enumerate(opts["zone_at"][:4]):
                zx, zy = self.zone_centers()[i]
                ks.append((a, (zx, 40, float(opts.get("zone_zoom", 1.4)))))
            return ks
        return None

    def lamp_pos(self):
        g = self.g
        x, y = g.pt(0.74, 0.50)
        return x + 40, y - 36

    def default_actors(self, ctx=None):
        v = self.variant
        fig = self.opts.get("figure", "desk" if v in ("hucre", "kutuphane") else None)
        sil = self.opts.get("sil", v == "hucre")
        out = []
        if v == "hucre":
            if fig == "kneel":
                out.append(dict(kind="kesis", x=730, y=808, h=270, action="kneel", sil="#1A1008", seed=3, t0=0.6, pray=1.0, dir=1, rim_dir=1))
        return out

    # ── statik ───────────────────────────────────────────────────────────
    def _draw_wall(self, fr, xa, xb):
        c, T = fr.c, self.T
        v = self.variant
        night = self.tod == "night"
        wx = self.wx
        if v == "hucre":
            plaster(c, xa, xb, OV - 40, Y_FL + 30, T, "#D2CCB4", "#E2DCC6", amp=0.055)
            # tonoz gölgesi (üst)
            c.drawRect(skia.Rect.MakeLTRB(xa, OV - 40, xb, 250), LGP((0, OV - 40), (0, 250), [("#2A1C10", 0.0, 150), ("#2A1C10", 1.0, 0)]))
            R(c, xa, Y_FL - 18, xb, Y_FL + 30, T("#7A6A52"))
            c.drawLine(xa, Y_FL - 18, xb, Y_FL - 18, STK(INK, 1.2, 170, False))
            if _vis(wx(1750), 100, xa, xb):
                draw_window(c, T, wx(1750), 250, 120, 210, night=night, shutters=False, mullion=True)
            if _vis(wx(1120), 100, xa, xb):
                draw_crucifix(c, T, wx(1120), 230, 2.0)
            if _vis(wx(1700), 60, xa, xb):
                pass
            if _vis(wx(360), 90, xa, xb):
                draw_crucifix(c, T, wx(360), 330, 0.8)
        elif v == "kutuphane":
            plaster(c, xa, xb, OV - 40, Y_FL + 30, T, "#C9B58A", "#D8C8A0", amp=0.05)
            cornice(c, xa, xb, 72, T, col="#6A4A2A", plaster="#CDB98F")
            for i in range(4):
                x = 300 + 740 * i
                if _vis(wx(x), 260, xa, xb):
                    draw_bookcase(c, T, wx(x), 168, 460, 520, rows=5, seed=i + 1, empty_frac=self._empty_frac(), col="#5E3A20")
            for i in range(3):
                x = 670 + 740 * i
                if _vis(wx(x), 130, xa, xb):
                    draw_window(c, T, wx(x), 214, 150, 330, night=night, shutters=True)
            wainscot(c, xa, xb, Y_FL - 36, Y_FL + 18, T, "#6E4524", pw=170, seed=5)
        else:
            cabinet_wall(c, T, xa, xb, 200, Y_FL + 18, seed=3)
            # tonoz: boyalı tavan şeridi + kasnak
            GRAD_V(c, xa, OV - 40, xb, 200, [(T("#1E3A6A"), 0.0), (T("#2A4A80"), 1.0)])
            rs = _RS(5)
            for k in range(int((xb - xa) / 90) + 2):
                x = xa - (xa % 90) + k * 90
                c.drawPath(sk.poly_path([(x, 150), (x + 8, 166), (x, 182), (x - 8, 166)]), PT(T("#E8C25A"), 200))
            R(c, xa, 188, xb, 206, T("#8A6A32"))
            c.drawLine(xa, 188, xb, 188, STK(INK, 1.2, 190, False))
            c.drawLine(xa, 206, xb, 206, STK(INK, 1.4, 200, False))
            c.drawLine(xa, 197, xb, 197, STK(T(GOLD), 2.0, 220, False))
        sh = LGP((0, Y_FL - 30), (0, Y_FL + 30), [("#1A0F06", 0.0, 0), ("#1A0F06", 1.0, 70)])
        c.drawRect(skia.Rect.MakeLTRB(xa, Y_FL - 30, xb, Y_FL + 30), sh)

    def _empty_frac(self):
        o = self.opts
        return float(o.get("empty_frac", 0.0))

    def _draw_main(self, fr, xa, xb):
        c, T = fr.c, self.T
        v = self.variant
        if v == "hucre":
            floor_tiles(c, xa, xb, Y_FL, LH, T, "#8E8878", "#7A7466", seed=7, w0=80.0, grow=1.12)
            if _vis(330, 330, xa, xb):
                draw_bed(c, T, 120, 785, 440, 250, 150, cover=("#8A7A66", "#6A5A46"), tester=False, plain=True, linen="#E4DCC4", wood="#5A3A20")
            if _vis(self.CH_X, 70, xa, xb):
                draw_chair(c, T, self.CH_X - 24, 808, 220, 72, 84, facing=1, col="#5A3A20", cushion="#6A5A46")
        elif v == "kutuphane":
            floor_planks(c, xa, xb, Y_FL, LH, T, "#7A5634", seed=3)
            for x, sd in ((880, 1), (2500, 2)):
                if _vis(x, 120, xa, xb):
                    draw_lectern(c, T, x, 800, 140, 200)
            if _vis(1330, 80, xa, xb):
                draw_chair(c, T, 1330 - 24, 808, 240, 72, 90, facing=1, col="#5A3A20", cushion="#6A5A46")
            if _vis(2150, 130, xa, xb):
                for k, (dx, cw_) in enumerate(((0, 90), (4, 80), (-3, 100))):
                    draw_book(c, 2150 + dx, 790 - k * 17, cw_, 15, ["#6A2E24", "#233C8C", "#4A3A2A"][k])
            if _vis(3000, 120, xa, xb):
                draw_chest(c, T, 2940, 3100, 790, 120, "#5A3A24")
        else:
            floor_tiles(c, xa, xb, Y_FL, LH, T, "#6A5238", "#5A4430", seed=9, w0=70.0, grow=1.12)
            rug(c, 690, 1290, 752, 862, T, field="#2A4A80", border="#8A2A22")
            if _vis(830 - 34, 80, xa, xb):
                draw_chair(c, T, 830 - 34 - 24, 808, 250, 72, 90, facing=1, col="#5A3A20", cushion="#8A2A22")
            if _vis(1540, 140, xa, xb):
                furnace(c, T, 1540, 790, 200, 216)
            if _vis(1860, 200, xa, xb):
                # laboratuvar masası
                BOX(c, 1700, 690, 2020, 704, "#6E4524", T, ink=1.4)
                for lx in (1710, 2000):
                    R(c, lx - 5, 704, lx + 5, 800, T("#5A3A20"))
                    INKR(c, lx - 5, 704, lx + 5, 800, 1.1, 190)

    def _draw_front(self, fr, xa, xb):
        c, T = fr.c, self.T
        v = self.variant
        g = self.g
        if v == "hucre":
            if _vis(g.x + g.w / 2, g.w / 2 + 60, xa, xb):
                table_front(c, g, 818, T, ("#8A5A38", "#6A4524"), apron=26, leg="#5A3A20")
        elif v == "kutuphane":
            if _vis(g.x + g.w / 2, g.w / 2 + 60, xa, xb):
                table_front(c, g, 818, T, ("#7A5A38", "#5A3A20"), apron=26, leg="#5A3A20")
        else:
            if _vis(g.x + g.w / 2, g.w / 2 + 60, xa, xb):
                table_front(c, g, 818, T, ("#6A4A2A", "#8A6A32"), apron=26, leg="#4A3020")

    def _draw_fg(self, fr, xa, xb):
        c, T = fr.c, self.T
        fx = lambda x: W / 2 + (x - W / 2) * F_FG
        v = self.variant
        if v == "kutuphane":
            for x in (1230, 2750):
                if _vis(fx(x), 90, xa, xb):
                    candelabra_floor(c, fx(x), 360, 880, "#1E140C", 3, 44.0)

    # ── canlı ────────────────────────────────────────────────────────────
    def dyn_wall(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        v = self.variant
        wx = self.wx
        night = ctx.tod == "night"
        if v == "hucre" and _vis(wx(1750), 400, ctx.xa, ctx.xb):
            window_light(f, wx(1750), 262, 100, 190, t, dx=-240, y_floor=Y_FL + 20, a=0.20 if ctx.tod == "day" else 0.08, seed=2, patch=False, dust=10, night=night, part="shaft")
        elif v == "kutuphane":
            for i in range(3):
                x = 670 + 740 * i
                if _vis(wx(x), 400, ctx.xa, ctx.xb):
                    window_light(f, wx(x), 232, 128, 296, t, dx=300, y_floor=Y_FL + 20, a=0.20 if ctx.tod == "day" else 0.08, seed=i + 2, patch=False, dust=10, night=night, part="shaft")

    def dyn_main(self, ctx):
        v = self.variant
        if v == "hucre":
            self._dyn_hucre(ctx)
        elif v == "kutuphane":
            self._dyn_kutuphane(ctx)
        else:
            self._dyn_studiolo(ctx)

    def _lit(self, ctx, key="lamp_lit"):
        lit = float(self.opts.get(key, 1.0))
        if "snuff_at" in self.opts:
            lit *= 1.0 - ctx.cx.amt(self.opts["snuff_at"], 0.35)
        return lit

    def _dyn_hucre(self, ctx):
        f, c, t, cx = ctx.f, ctx.c, ctx.t, ctx.cx
        T, g = self.T, self.g
        night = ctx.tod != "day"
        fig = self.opts.get("figure", "desk")
        if ctx.tod == "day":
            window_light(f, 1750, 262, 100, 190, t, dx=-240, y_floor=Y_FL + 60, a=0.20, seed=2, patch=True, dust=0, part="patch", patch_h=100)
        table_top(c, g, T, ("#8A5A38", "#6A4524"))
        bx, by = g.pt(0.38, 0.46)
        draw_book(c, bx, by, 150, 22, "#6A2E24", open_=True)
        ix, iy = g.pt(0.14, 0.60)
        inkwell(c, ix, iy, 0.9, t)
        qx, qy = g.pt(0.22, 0.20)
        if fig != "desk":
            quill(c, qx, qy, -14.0, 0.45)
        if fig == "desk":
            seated(f, "kesis", g.x - 34, 823, 280, t, "write", 1, seed=3, phase=0.0, sil="#1A1008", rim="#E8A860", rim_dir=1)
        lx, ly = g.pt(0.74, 0.50)
        lit = self._lit(ctx)
        if ctx.tod == "day":
            lit *= float(self.opts.get("lamp_day", 0.35))
        fxl, fyl, _b = oil_lamp(f, lx, ly, 50, t, seed=1.7, lit=lit)
        if night and lit > 0.3:
            moth(c, fxl, fyl - 6, t, seed=2.0, r=34)
        draw_extra(ctx, "back")
        if night:
            dust_motes(c, t, lx - 220, ly - 220, lx + 220, ly + 20, n=12, seed=21, a=0.5, size=1.7, drift=(4, -2), col="#FFE2A0")

    def _dyn_kutuphane(self, ctx):
        f, c, t, cx = ctx.f, ctx.c, ctx.t, ctx.cx
        T, g = self.T, self.g
        night = ctx.tod != "day"
        fig = self.opts.get("figure", "desk")
        for i in range(3):
            x = 670 + 740 * i
            if _vis(x, 400, ctx.xa, ctx.xb) and ctx.tod == "day":
                window_light(f, x, 232, 128, 296, t, dx=300, y_floor=Y_FL + 70, a=0.20, seed=i + 2, patch=True, dust=0, part="patch", patch_h=104)
        # kürsülerdeki mumlar
        for x, sd in ((880, 1.1), (2500, 2.4)):
            if _vis(x, 100, ctx.xa, ctx.xb):
                candle(f, x + 52, 800 - 200 + 18, 56, t, seed=sd, lit=1.0 if night else 0.0, holder=True, smoke=night)
        table_top(c, g, T, ("#7A5A38", "#5A3A20"))
        bx, by = g.pt(0.40, 0.46)
        draw_book(c, bx, by, 130, 20, "#233C8C", open_=True)
        ix, iy = g.pt(0.12, 0.60)
        inkwell(c, ix, iy, 0.9, t)
        if fig == "desk":
            seated(f, "kesis", g.x - 34, 823, 280, t, "write", 1, seed=6, phase=0.2, sil=("#1A1008" if self.opts.get("sil", False) else None), rim="#E8A860", rim_dir=1, desk_top=not self.opts.get("sil", False))
        cx_, cy_ = g.pt(0.72, 0.58)
        candle(f, cx_, cy_, 70, t, seed=3.3, lit=1.0 if night else 0.0, holder=True)
        draw_extra(ctx, "back")
        if night:
            dust_motes(c, t, cx_ - 260, cy_ - 240, cx_ + 260, cy_ + 30, n=12, seed=22, a=0.5, size=1.7, drift=(4, -2), col="#FFE2A0")

    def _active_zone(self, ctx):
        zc = self.zone_centers()
        o = self.opts
        if "zone_at" in o:
            ts = [ctx.cx.at(a) for a in o["zone_at"][:4]]
            t = ctx.t
            if t <= ts[0]:
                return zc[0][0], zc[0][1], 0
            for i in range(3):
                if t < ts[i + 1]:
                    u = smooth(clamp((t - (ts[i] + ts[i + 1]) / 2 + 0.6) / 1.2))
                    j = i if u < 0.5 else i + 1
                    return zc[i][0] + (zc[i + 1][0] - zc[i][0]) * u, zc[i][1] + (zc[i + 1][1] - zc[i][1]) * u, j
            return zc[3][0], zc[3][1], 3
        return 1250.0, 480.0, -1

    def _dyn_studiolo(self, ctx):
        f, c, t, cx = ctx.f, ctx.c, ctx.t, ctx.cx
        T, g = self.T, self.g
        o = self.opts
        zx, zy, zi = self._active_zone(ctx)
        # ZONE 1 — ofis: masa + kâğıtlar + (isteğe bağlı) oturan siluet
        table_top(c, g, T, ("#6A4A2A", "#8A6A32"))
        px, py = g.pt(0.36, 0.5)
        doc_sheet(f, px, py, 0.12, t, n=10, seed=4, rot=-0.03, seal=True)
        ix, iy = g.pt(0.78, 0.40)
        inkwell(c, ix, iy, 0.9, t)
        qx, qy = g.pt(0.70, 0.62)
        quill(c, qx, qy, -12.0, 0.42)
        if o.get("figure") == "desk":
            seated(f, "banker", g.x - 34, 823, 280, t, "write", 1, seed=7, sil="#1A1008", rim="#E8A860", rim_dir=1)
        ox, oy = g.pt(0.54, 0.74)
        oil_lamp(f, ox, oy, 30, t, seed=2.2, lit=1.0)
        # ZONE 2 — laboratuvar: ocak + alembik + şişeler
        fx, fy = 1540, 790 - 216 * 0.26
        furnace_fire(f, fx, fy, 100, t, seed=1.0, lit=1.0)
        alembic(f, 1830, 690, 1.0, t, lit=1.0)
        draw_flask(c, 1760, 690, 0.9, t, "#B8604A")
        draw_flask(c, 1990, 690, 0.7, t + 1.0, "#6E9A8A")
        draw_book(c, 1930, 690, 70, 12, "#2E5A3A")
        # ZONE 3 — saklanma yeri: gizli dolap kapısı açılır
        sa = o.get("secret_at", None)
        ko = smooth(clamp((t - (cx.at(sa) if sa is not None else 3.0)) / 1.3)) if sa is not None or True else 0.0
        self._secret(c, T, 2250, ko, t)
        # ZONE 4 — merak kabini
        self._curio(f, c, T, 2740, t)
        # lambalar
        for i, x in enumerate((1050, 2000, 2500)):
            oil_lamp(f, x - 14, 330, 34, t, seed=i * 3.1, lit=1.0, hang=330 - 34 * 0.9 - 62)
        draw_extra(ctx, "back")

    def _secret(self, c, T, x, ko, t):
        """Saklanma yeri: dolap kapısı (sol menteşe) açılır → arkada karanlık oyuk + küçük kutu/parşömen."""
        x0, x1 = x - 90, x + 90
        y0, y1 = 250, 640
        c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), PT("#0E0806"))
        c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), LGP((0, y0), (0, y1), [("#0A0504", 0.0), ("#241610", 1.0)]))
        INKR(c, x0, y0, x1, y1, 2.0, 230)
        if ko > 0.15:
            # oyuk içi: kutu + rulo
            draw_chest(c, T, x - 54, x + 54, 630, 70, "#4A3420")
            draw_scroll(c, x - 20, 540, 70, 0.9)
        wd = (x1 - x0) * max(0.10, math.cos(ko * 1.30))
        p = sk.poly_path([(x0, y0), (x0 + wd, y0 + 10 * ko), (x0 + wd, y1 - 10 * ko), (x0, y1)])
        c.save()
        c.clipPath(p, skia.ClipOp.kIntersect, True)
        BOX(c, x0, y0, x0 + wd, y1, "#6E4524", T, hl=0.12, sh=0.2 * (1 + ko), ink=0)
        c.drawRect(skia.Rect.MakeLTRB(x0 + 8, y0 + 8, x0 + wd - 8, y1 - 8), LGP((0, y0), (0, y1), [(T("#B8884A"), 0.0), (T("#9A5A3A"), 1.0)]))
        c.drawCircle(x0 + wd - 14, (y0 + y1) / 2, 4, PT(T(GOLD)))
        c.restore()
        INKP(c, p, 2.0, 230)

    def _curio(self, f, c, T, x, t):
        """Merak kabini: raflı vitrin; armiller küre, kabuklar, mercan, şişe, kitap yığını."""
        x0, x1 = x - 150, x + 150
        y0, y1 = 250, 700
        R(c, x0, y0, x1, y1, T("#1E140C"))
        c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), LGP((0, y0), (0, y1), [("#120A06", 0.0), ("#3A2818", 1.0)]))
        for ys in (430, 560, 690):
            BOX(c, x0, ys, x1, ys + 12, "#6E4524", T, ink=1.2)
        INKR(c, x0, y0, x1, y1, 2.0, 230)
        armillary(f, x - 60, 330, 46, t, 0.4)
        shell(c, x + 60, 428, 1.1)
        shell(c, x + 100, 428, 0.8, "#F0DCC0")
        coral(c, x + 20, 428, 1.2)
        draw_flask(c, x - 80, 558, 0.7, t, "#6E9A8A")
        draw_book(c, x + 40, 558, 80, 14, "#7A2E2A")
        draw_book(c, x + 44, 544, 70, 12, "#233C8C")
        coral(c, x - 100, 688, 0.9, "#B33620")
        shell(c, x, 688, 1.2)
        c.drawCircle(x + 90, 664, 22, PT(T("#3E6A8A")))
        c.drawCircle(x + 90, 664, 22, STK(INK, 1.1, 200))
        c.drawLine(x + 70, 664, x + 110, 664, STK("#C4A04A", 1.6, 220))

    def dyn_front(self, ctx):
        draw_extra(ctx, "front")

    def dyn_fg(self, ctx):
        c, t = ctx.c, ctx.t
        f = ctx.f
        fx = lambda x: W / 2 + (x - W / 2) * F_FG
        night = ctx.tod != "day"
        if self.variant == "kutuphane":
            for k, x in enumerate((1230, 2750)):
                for i, off in enumerate((-44, 0, 44)):
                    bx = fx(x) + off
                    by = 360 + 14 + (18 if off else 0) + 8
                    if _vis(bx, 80, ctx.xa, ctx.xb):
                        candle(f, bx, by, 40, t, seed=5.5 + k * 3 + i, holder=False, lit=1.0 if night else 0.0, smoke=False, halo=0.7, wax="#D8CDB0")
        rs = _RS(47)
        xa, xb = ctx.xa, ctx.xb
        for k in range(12):
            x = xa + ((rs.rand() * (xb - xa) + t * 12 * (0.5 + rs.rand())) % (xb - xa))
            y = 120 + rs.rand() * 700 + math.sin(t * 0.6 + k) * 14
            c.drawCircle(x, y, 1.6 + 2.0 * rs.rand(), PT("#FFEFC4", int(34 + 56 * rs.rand())))

    def light(self, ctx):
        v = self.variant
        if v == "hucre":
            lx, ly = self.lamp_pos()
            return (lx, ly, 820.0 * (0.35 + 0.65 * self._lit(ctx)) if self._lit(ctx) > 0.02 else 30.0, 1.0)
        if v == "kutuphane":
            x, y = self.g.pt(0.72, 0.58)
            return (x, y - 80, 880.0, 1.0)
        zx, zy, zi = self._active_zone(ctx)
        return (zx, zy, 980.0 if zi >= 0 else 1500.0, 1.0)


ROOMS["calisma"] = Calisma


# ═════════════════════════════ SAKRİSTİ (tunç kapı) ═════════════════════════════
def door_frame_stone(c, T, x, yb, w, h, col="#B4AE9A"):
    """Taş kapı çerçevesi (pietra serena): iki dikme + lento + üstte yarım daire lünet (mavi zemin, altın yıldız deseni). x orta, yb eşik, w/h kapı açıklığı."""
    x0, x1 = x - w / 2, x + w / 2
    top = yb - h
    fw = 46
    for sx0, sx1 in ((x0 - fw, x0), (x1, x1 + fw)):
        BOX(c, sx0, top - 30, sx1, yb, col, T, hl=0.16, sh=0.22, ink=1.6)
        for yy in np.arange(top, yb, 64):
            c.drawLine(sx0, yy, sx1, yy, STK("#3A3428", 1.0, 90, False))
        R(c, sx0 - 6, top - 38, sx1 + 6, top - 24, T(mix(col, "#FFFFFF", 0.1)))
        INKR(c, sx0 - 6, top - 38, sx1 + 6, top - 24, 1.3, 190)
        R(c, sx0 - 8, yb - 22, sx1 + 8, yb, T(mix(col, "#000000", 0.12)))
        INKR(c, sx0 - 8, yb - 22, sx1 + 8, yb, 1.3, 190)
    BOX(c, x0 - fw - 14, top - 80, x1 + fw + 14, top - 36, col, T, hl=0.18, sh=0.18, ink=1.6)
    c.drawLine(x0 - fw - 14, top - 62, x1 + fw + 14, top - 62, STK(T(GOLD), 2.0, 200, False))
    # lünet (basık yarım elips; mavi zemin, altın yıldızlar)
    lr = (w + 2 * fw) / 2 + 6
    ry = lr * 0.40
    ly = top - 82
    lp = skia.Path()
    lp.moveTo(x - lr, ly)
    lp.arcTo(skia.Rect.MakeLTRB(x - lr, ly - ry, x + lr, ly + ry), 180, 180, False)
    lp.close()
    FILLP(c, lp, T(col), 255, 1.8, 210)
    ip = skia.Path()
    ip.moveTo(x - lr + 12, ly)
    ip.arcTo(skia.Rect.MakeLTRB(x - lr + 12, ly - ry + 12, x + lr - 12, ly + ry - 12), 180, 180, False)
    ip.close()
    c.drawPath(ip, LGP((0, ly - ry), (0, ly), [(T("#2A4A8A"), 0.0), (T("#1E3A70"), 1.0)]))
    c.save()
    c.clipPath(ip, skia.ClipOp.kIntersect, True)
    for k in range(11):
        a = math.pi + (k + 0.5) * math.pi / 11
        sx_, sy_ = x + math.cos(a) * lr * 0.74, ly + math.sin(a) * ry * 0.70
        c.drawPath(sk.poly_path([(sx_, sy_ - 6), (sx_ + 2, sy_ - 2), (sx_ + 6, sy_), (sx_ + 2, sy_ + 2), (sx_, sy_ + 6), (sx_ - 2, sy_ + 2), (sx_ - 6, sy_), (sx_ - 2, sy_ - 2)]), PT(T("#E8C25A"), 220))
    c.drawCircle(x, ly - ry * 0.25, ry * 0.30, PT(T("#E8C25A"), 235))
    c.restore()
    INKP(c, ip, 1.4, 200)


def inlay_cabinet(c, T, x0, x1, yb, h, seed=1, col="#7A4A28"):
    """Sakristi dolabı (intarsia): ceviz gövde, çift kapak, geometrik kakma desenleri (baklava/yıldız), pirinç kulplar, üst silme."""
    SOFT(c, (x0 + x1) / 2 + 6, yb + 3, (x1 - x0) * 0.55, 10, "#000000", 80)
    top = yb - h
    BOX(c, x0, top, x1, yb, col, T, hl=0.12, sh=0.20, ink=1.6)
    R(c, x0 - 8, top - 16, x1 + 8, top + 2, T(mix(col, "#FFFFFF", 0.08)))
    INKR(c, x0 - 8, top - 16, x1 + 8, top + 2, 1.3, 190)
    cols = 2
    cw = (x1 - x0) / cols
    for i in range(cols):
        for r_ in range(2):
            px0, px1 = x0 + i * cw + 12, x0 + (i + 1) * cw - 12
            ph = (h - 70) / 2
            py0 = top + 18 + r_ * (ph + 10)
            py1 = py0 + ph - 8
            BOX(c, px0, py0, px1, py1, mix(col, "#FFFFFF", 0.1), T, hl=0.10, sh=0.16, ink=1.2)
            cx_, cy_ = (px0 + px1) / 2, (py0 + py1) / 2
            rr = min(px1 - px0, py1 - py0) * 0.32
            for k, col_i in ((0, "#C8A060"), (1, "#5A3A20")):
                a = rr * (1 - 0.45 * k)
                c.drawPath(sk.poly_path([(cx_, cy_ - a), (cx_ + a, cy_), (cx_, cy_ + a), (cx_ - a, cy_)]), PT(T(col_i)))
            c.drawPath(sk.poly_path([(cx_, cy_ - rr), (cx_ + rr, cy_), (cx_, cy_ + rr), (cx_ - rr, cy_)]), STK("#2A1A0C", 1.0, 190))
            for q in range(4):
                a = q * math.pi / 2 + math.pi / 4
                c.drawCircle(cx_ + math.cos(a) * rr * 1.5, cy_ + math.sin(a) * rr * 1.5, 3.0, PT(T("#C8A060")))
    c.drawLine((x0 + x1) / 2, top + 6, (x0 + x1) / 2, yb - 6, STK(INK, 1.8, 220, False))
    for kx in ((x0 + x1) / 2 - 12, (x0 + x1) / 2 + 12):
        c.drawCircle(kx, top + h * 0.5, 4.2, PT(T(GOLD)))
        c.drawCircle(kx, top + h * 0.5, 4.2, STK(INK, 0.9, 190))


class Sakristi(Room):
    """Duomo kuzey sakristisi: taş duvar, MERKEZDE TUNÇ KAPI (iki kanat, kabartma paneller; kapı çerçevesi + lünet), yanlarda intarsia dolaplar, yüksek küçük pencereler, asılı kandiller, içeride SİLUET figürler.
    Kapı animasyonu: open0 (başlangıç açıklığı, 0,9) → `close_at` (çapa) + `close_dur` (1,7 sn) ile KAPANIR; kapanma anında kamera hafifçe sarsılır; açıklıktan nef'in sıcak ışığı sızar ve daralıp söner.
    path="close": kamera kapıya girer (z≈6'da kanat ekranı doldurur → Lab-A whip/zoomthru ile kes). shadow_at: kapıdan uzanan uzun gölge (siluet, şiddet yok).
    actors verilmezse üç siluet: soldan kapıya yürüyen, kapıda duran, sağda bekleyen."""
    name = "sakristi"
    PW = 2800
    DX, DYB, DH = 1400, 700, 470

    def build(self):
        self.layer("wall", F_WALL, self.Lw(F_WALL), self._draw_wall, wear=3)
        self.layer("main", 1.0, self.PW, self._draw_main, scale=1.2)
        self.layer("fg", F_FG, self.Lw(F_FG), self._draw_fg)

    def paths(self):
        return {
            "default": [(0.0, (1250, 0, 1.0)), (1.0, (1400, 10, 1.18))],
            "close": [(0.0, (1300, 0, 1.0)), (0.55, (1400, 20, 1.3)), (1.0, (1400, 40, 7.4))],
            "push": [(0.0, (1400, 0, 1.0)), (1.0, (1400, 60, 2.2))],
            "sweep_r": [(0.0, (1000, 0, 1.04)), (1.0, (1800, 0, 1.04))],
            "pull": [(0.0, (1400, 30, 2.0)), (1.0, (1400, 0, 1.0))],
        }

    def open_amt(self, ctx):
        o = self.opts
        o0 = float(o.get("open0", 0.9))
        if "close_at" not in o:
            return float(o.get("open", o0))
        tc = ctx.cx.at(o["close_at"])
        d = float(o.get("close_dur", 1.7))
        u = clamp((ctx.t - tc) / d)
        a = o0 * (1.0 - u * u * (3 - 2 * u) ** 1.0) if u < 1.0 else 0.0
        # kapanıştan sonra küçük geri tepme
        if u >= 1.0:
            dt = ctx.t - tc - d
            a = 0.035 * math.exp(-dt * 7.0) * max(0.0, math.sin(dt * 22.0))
        return clamp(a)

    def cam_shake(self, cx, t):
        o = self.opts
        if "close_at" not in o:
            return 0.0, 0.0
        try:
            tc = cx.at(o["close_at"]) + float(o.get("close_dur", 1.7))
        except Exception:
            return 0.0, 0.0
        dt = t - tc
        if dt < 0 or dt > 0.9:
            return 0.0, 0.0
        a = 9.0 * math.exp(-dt * 6.5)
        return a * 0.5 * math.sin(dt * 47.0), a * math.sin(dt * 39.0 + 1.0)

    def default_actors(self, ctx=None):
        d = self.DX
        return [dict(kind="soylu", x=d - 640, y=806, h=268, action="idle", sil="#120A06", seed=5, dir=1, walk=(d - 250, 70.0), walk_at=0.4, rim_dir=1),
                dict(kind="rahip", x=d - 260, y=812, h=268, action="point", sil="#120A06", seed=9, dir=1, at=0.8, rim_dir=1, layer="front"),
                dict(kind="kardinal", x=d + 470, y=800, h=268, action="idle", sil="#120A06", seed=14, dir=-1, rim_dir=-1)]

    # ── statik ───────────────────────────────────────────────────────────
    def _draw_wall(self, fr, xa, xb):
        c, T = fr.c, self.T
        night = self.tod == "night"
        wx = self.wx
        GRAD_V(c, xa, OV - 40, xb, Y_FL + 30, [(T("#A7A28F"), 0.0), (T("#BDB7A2"), 1.0)])
        ashlar(c, xa, xb, OV - 40, Y_FL + 30, T, "#B4AE98", 70.0, seed=4)
        w = int(xb - xa) + 1
        h = int(Y_FL + 30 - (OV - 40)) + 1
        f_ = noise_field(xa, OV - 40, w, h, 1, 10, 4)
        arr = np.zeros((h, w, 4), np.uint8)
        arr[..., 0] = np.where(f_ > 0, 255, 70)
        arr[..., 1] = np.where(f_ > 0, 248, 56)
        arr[..., 2] = np.where(f_ > 0, 226, 40)
        arr[..., 3] = np.clip(np.abs(f_) * 18, 0, 70).astype(np.uint8)
        c.drawImage(sk.np_to_image(np.ascontiguousarray(arr)), xa, OV - 40, LIN)
        cornice(c, xa, xb, 72, T, col="#8E8878", plaster="#BDB7A2", gold=False)
        for x in (780, 2020):
            if _vis(wx(x), 80, xa, xb):
                draw_window(c, T, wx(x), 196, 96, 170, night=night, shutters=False, mullion=True)
        R(c, xa, Y_FL - 24, xb, Y_FL + 30, T("#8A8472"))
        c.drawLine(xa, Y_FL - 24, xb, Y_FL - 24, STK(INK, 1.3, 190, False))
        sh = LGP((0, Y_FL - 30), (0, Y_FL + 30), [("#1A0F06", 0.0, 0), ("#1A0F06", 1.0, 80)])
        c.drawRect(skia.Rect.MakeLTRB(xa, Y_FL - 30, xb, Y_FL + 30), sh)

    def _draw_main(self, fr, xa, xb):
        c, T = fr.c, self.T
        floor_tiles(c, xa, xb, Y_FL, LH, T, "#D2C8AE", "#8E8470", seed=2, w0=88.0, grow=1.12)
        if _vis(self.DX, 320, xa, xb):
            door_frame_stone(c, T, self.DX, self.DYB, self.DH * 0.56, self.DH)
        for (x0, x1, sd) in ((560, 1000, 1), (1800, 2240, 2)):
            if _vis((x0 + x1) / 2, 300, xa, xb):
                inlay_cabinet(c, T, x0, x1, 790, 380, seed=sd)

    def _draw_fg(self, fr, xa, xb):
        c, T = fr.c, self.T
        fx = lambda x: W / 2 + (x - W / 2) * F_FG
        for x in (260, 2560):
            if _vis(fx(x), 90, xa, xb):
                xx = fx(x)
                R(c, xx - 30, OV - 40, xx + 30, 900, "#3A342A")
                HGRAD(c, xx - 30, OV - 40, xx + 30, 900, [("#FFFFFF", 0.0, 34), ("#000000", 0.45, 0), ("#000000", 1.0, 100)])
                INKR(c, xx - 30, OV - 40, xx + 30, 900, 1.5, 200)

    # ── canlı ────────────────────────────────────────────────────────────
    def dyn_wall(self, ctx):
        f, t = ctx.f, ctx.t
        wx = self.wx
        night = ctx.tod == "night"
        for i, x in enumerate((780, 2020)):
            if _vis(wx(x), 400, ctx.xa, ctx.xb):
                window_light(f, wx(x), 208, 82, 140, t, dx=300 if i == 0 else -300, y_floor=Y_FL + 20, a=0.24 if ctx.tod == "day" else 0.10, seed=i + 1, patch=False, dust=10, night=night, part="shaft")

    def dyn_main(self, ctx):
        f, c, t, cx = ctx.f, ctx.c, ctx.t, ctx.cx
        T = self.T
        oa = self.open_amt(ctx)
        self._oa = oa
        night = ctx.tod != "day"
        # pencere lekesi (gündüz)
        for i, x in enumerate((780, 2020)):
            if _vis(x, 400, ctx.xa, ctx.xb) and ctx.tod == "day":
                window_light(f, x, 208, 82, 140, t, dx=300 if i == 0 else -300, y_floor=Y_FL + 60, a=0.24, seed=i + 1, patch=True, dust=0, part="patch", patch_h=96)
        # kapı: nefin sıcak ışığı eşiğe sızar (kapı açıklığıyla orantılı)
        if oa > 0.01:
            spill = oa
            c.drawPath(sk.poly_path([(self.DX - 150 * spill - 20, self.DYB), (self.DX + 150 * spill + 20, self.DYB), (self.DX + 520 * spill, 880), (self.DX - 520 * spill, 880)]),
                       LGP((0, self.DYB), (0, 880), [("#FFE2A0", 0.0, int(210 * spill)), ("#FFE2A0", 1.0, int(40 * spill))]))
        if self.opts.get("door", "bronze") == "wood":
            wdt = self.DH * 0.56
            door_leaf(f, self.DX, self.DYB, self.DH, wdt, oa, T, seed=3, light=("#3A2A18", "#FFE2A0"), hinge=1)
        else:
            door_bronze(f, self.DX, self.DYB, self.DH, oa, seed=3, light=True, t=t)
        if oa > 0.02:
            PN.glow(c, self.DX, self.DYB - self.DH * 0.45, 380 * (0.4 + oa), "#FFD27A", 0.32 * oa)
            dust_motes(c, t, self.DX - 160, self.DYB - self.DH, self.DX + 160, self.DYB, n=int(14 * oa) + 2, seed=31, a=0.8, size=2.0, drift=(3, 6))
        # uzun gölge (siluet, şiddet yok)
        if "shadow_at" in self.opts:
            ks = smooth(clamp((t - cx.at(self.opts["shadow_at"])) / 1.6))
            if ks > 0.01:
                self._long_shadow(f, ks, oa)
        # asılı kandiller
        for i, x in enumerate((900, 1900)):
            if _vis(x, 100, ctx.xa, ctx.xb):
                oil_lamp(f, x - 16, 320, 34, t, seed=i * 3.3, lit=1.0, hang=320 - 34 * 0.9 - 62)
        draw_extra(ctx, "back")

    def _long_shadow(self, f, k, oa):
        """Kapıdan nef ışığı arkadan vurunca zemine, izleyiciye doğru uzanan ayakta bir kişinin UZUN GÖLGESİ (yumuşak koyu siluet; yüz/ayrıntı yok, şiddet yok)."""
        c = f.c
        a = clamp(oa * 1.5) * 0.62 * k
        L = 300.0 * k
        x0, y0 = self.DX - 10, self.DYB + 8
        pts = [(-22, 0), (-30, 0.14), (-24, 0.34), (-36, 0.56), (-16, 0.78), (-9, 0.88), (0, 0.97), (9, 0.88), (16, 0.78), (36, 0.56), (24, 0.34), (30, 0.14), (22, 0)]
        for grow, al in ((10, 0.35), (4, 0.6), (0, 1.0)):
            q = [(x0 + px * (1 + grow / 30.0) + 0.55 * L * py, y0 + L * py * 0.52) for px, py in pts]
            c.drawPath(sk.smooth_path(q, True, 0.4), PT("#0A0604", int(255 * a * al)))
        hx, hy = x0 + 0.55 * L * 0.99, y0 + L * 0.99 * 0.52
        c.drawOval(skia.Rect.MakeLTRB(hx - 16, hy - 8, hx + 16, hy + 12), PT("#0A0604", int(255 * a)))

    def dyn_front(self, ctx):
        draw_extra(ctx, "front")

    def dyn_fg(self, ctx):
        c, t = ctx.c, ctx.t
        rs = _RS(48)
        xa, xb = ctx.xa, ctx.xb
        for k in range(12):
            x = xa + ((rs.rand() * (xb - xa) + t * 12 * (0.5 + rs.rand())) % (xb - xa))
            y = 120 + rs.rand() * 700 + math.sin(t * 0.6 + k) * 14
            c.drawCircle(x, y, 1.6 + 2.0 * rs.rand(), PT("#FFEFC4", int(34 + 56 * rs.rand())))

    def light(self, ctx):
        oa = getattr(self, "_oa", 0.9)
        return (self.DX, 520, 760.0 + 260.0 * oa, 1.0)


ROOMS["sakristi"] = Sakristi


# ═════════════════════════════ BOŞ ODA: Blois gece odası · Köln soğuk oda ═════════════════════════════
def doorway_stone(c, T, x, yb, w, h, col="#A8A28E"):
    """Yuvarlak kemerli taş kapı çerçevesi (iç açıklık dinamik çizilir). Dönüş: açıklık yolu (clip için)."""
    x0, x1 = x - w / 2, x + w / 2
    r = w / 2
    def arch(g):
        p = skia.Path()
        p.moveTo(x0 - g, yb)
        p.lineTo(x0 - g, yb - h + r)
        p.arcTo(skia.Rect.MakeLTRB(x0 - g, yb - h - g, x1 + g, yb - h + 2 * r + g), 180, 180, False)
        p.lineTo(x1 + g, yb)
        p.close()
        return p
    FILLP(c, arch(22), T(col), 255, 1.8, 210)
    for k in range(9):
        a = math.pi + (k + 0.5) * math.pi / 9
        c.drawLine(x + math.cos(a) * (r + 2), yb - h + r + math.sin(a) * (r + 2), x + math.cos(a) * (r + 22), yb - h + r + math.sin(a) * (r + 22), STK("#3A3428", 1.2, 140, False))
    return arch(0)


def door_leaf(f, x, yb, h, w, oa, T, seed=1, light=("#1A2440", "#3A4A78"), hinge=1, iron=True):
    """Tek kanatlı ahşap kapı (demir bantlı): menteşe sağda (hinge=1) / solda; oa 0..1 açılma (yatay daralma + serbest kenar kısalır). Açıklıkta dim ışık."""
    c = f.c
    x0, x1 = x - w / 2, x + w / 2
    top = yb - h
    if oa > 0.01:
        c.drawRect(skia.Rect.MakeLTRB(x0, top - 6, x1, yb), LGP((0, top), (0, yb), [(light[0], 0.0), (light[1], 1.0)]))
        PN.glow(c, x, yb - h * 0.35, w * 1.6, "#9FB4E8", 0.12 * oa)
    ew = w * max(0.10, math.cos(oa * 1.25))
    sk_ = 0.05 * oa * h
    hx = x1 if hinge > 0 else x0
    fx = hx - hinge * ew
    q = sk.poly_path([(hx, top), (fx, top + sk_), (fx, yb - sk_), (hx, yb)])
    c.save()
    c.clipPath(q, skia.ClipOp.kIntersect, True)
    HGRAD(c, min(hx, fx), top, max(hx, fx), yb, [(T("#6E4524"), 0.0), (T("#5A3820"), 1.0)] if hinge > 0 else [(T("#5A3820"), 0.0), (T("#6E4524"), 1.0)])
    n = 5
    for i in range(1, n):
        xx = fx + (hx - fx) * i / n
        c.drawLine(xx, top, xx, yb, STK("#1E1006", 1.4, 170, False))
    rs = _RS(seed)
    for i in range(40):
        xx = rs.uniform(min(hx, fx), max(hx, fx))
        yy = rs.uniform(top, yb)
        c.drawLine(xx, yy, xx + rs.uniform(-1, 1), yy + rs.uniform(10, 40), STK("#2A1608", 0.8, 50, False))
    if iron:
        for yy in (top + h * 0.16, top + h * 0.5, top + h * 0.84):
            R(c, min(hx, fx), yy - 8, max(hx, fx), yy + 8, "#2E2A26")
            for k in range(4):
                c.drawCircle(fx + (hx - fx) * (k + 0.5) / 4, yy, 2.6, PT("#6A6258"))
    c.drawCircle(fx + hinge * 0.0 + (-hinge) * 16 * (ew / w), top + h * 0.52, 9 * (ew / w), STK("#2E2A26", 3.0, 255))
    shd = LGP((hx, 0), (fx, 0), [("#FFFFFF", 0.0, 14), ("#000000", 1.0, int(80 * oa))])
    c.drawRect(skia.Rect.MakeLTRB(min(hx, fx) - 2, top - 2, max(hx, fx) + 2, yb + 2), shd)
    c.restore()
    INKP(c, q, 2.2, 230)


def fireplace(c, T, x, yb, w=300, h=330, cold=True, col="#A8A08A", seed=1):
    """Taş şömine: yan dikmeler (başlıklı), tonoz/başlık, korkuluk rafı (mantel), karanlık ocak ağzı; soğuk: kurum + kül yığını + demir ocak taşları (andiron)."""
    x0, x1 = x - w / 2, x + w / 2
    top = yb - h
    SOFT(c, x, yb + 4, w * 0.7, 10, "#000000", 80)
    BOX(c, x0 - 30, top - 36, x1 + 30, top - 6, col, T, hl=0.18, sh=0.18, ink=1.5)       # mantel rafı
    BOX(c, x0, top - 6, x1, top + 70, col, T, hl=0.14, sh=0.22, ink=1.4)                   # başlık
    for sx0, sx1 in ((x0, x0 + 48), (x1 - 48, x1)):
        BOX(c, sx0, top + 70, sx1, yb, col, T, hl=0.18, sh=0.24, ink=1.5)
        R(c, sx0 - 6, top + 62, sx1 + 6, top + 82, T(mix(col, "#FFFFFF", 0.1)))
        INKR(c, sx0 - 6, top + 62, sx1 + 6, top + 82, 1.2, 190)
        for yy in np.arange(top + 100, yb - 20, 54):
            c.drawLine(sx0, yy, sx1, yy, STK("#3A3428", 1.0, 90, False))
    ox0, ox1 = x0 + 48, x1 - 48
    oy0 = top + 70
    c.drawRect(skia.Rect.MakeLTRB(ox0, oy0, ox1, yb), LGP((0, oy0), (0, yb), [("#0A0806", 0.0), ("#1E1814", 1.0)]))
    if cold:
        rs = _RS(seed * 17)
        c.drawRect(skia.Rect.MakeLTRB(ox0, oy0, ox1, oy0 + 30), PT("#050403", 200))
        for k in range(14):
            sx = rs.uniform(ox0 + 4, ox1 - 4)
            c.drawLine(sx, oy0 + 30, sx + rs.uniform(-6, 6), oy0 + rs.uniform(60, 140), STK("#050403", rs.uniform(2, 8), 90))
        # kül yığını
        p = skia.Path()
        p.moveTo(ox0 + 14, yb)
        p.quadTo((ox0 + ox1) / 2, yb - 36, ox1 - 14, yb)
        c.drawPath(p, PT("#6A665E", 255))
        for k in range(10):
            c.drawCircle(rs.uniform(ox0 + 40, ox1 - 40), yb - rs.uniform(2, 18), rs.uniform(1.5, 4), PT("#8A867E", 200))
        # demir ocak taşları
        for ex in (ox0 + 24, ox1 - 24):
            R(c, ex - 4, yb - 70, ex + 4, yb, "#2A2622")
            c.drawCircle(ex, yb - 74, 7, PT("#2A2622"))
        c.drawLine(ox0 + 24, yb - 40, ox1 - 24, yb - 40, STK("#2A2622", 5.0, 255))
    INKR(c, ox0, oy0, ox1, yb, 1.8, 230)


def thread_line(f, pA, pB, t, ts=None, sag=14.0, col="#E6EEFF", w=1.8):
    """İPLİK/ÇİZGİ: iki çapa arasında ince, gergin çizgi (hafif titrer). ts verilirse (yerel sn) orada KOPAR: iki yarı çapalarından serbest kalır, uçları yavaşça aşağı süzülür/salınır.
    pA, pB = (x,y) oda koordinatı. Dönüş: yok."""
    c = f.c
    N = 36

    def curve(a, b, sagv, vib):
        pts = []
        for i in range(N + 1):
            u = i / N
            x = a[0] + (b[0] - a[0]) * u
            y = a[1] + (b[1] - a[1]) * u + sagv * 4 * u * (1 - u) + vib * math.sin(math.pi * u) * math.sin(t * 13.0 + u * 6.0)
            pts.append((x, y))
        return pts

    def draw(pts, a=235):
        p = skia.Path()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        c.drawPath(p, STK(col, w * 4.5, int(a * 0.12)))
        c.drawPath(p, STK(col, w, a))
    if ts is None or t < ts:
        tension = 0.6 if ts is None else clamp(1.0 - (ts - t) / 1.2) * 1.4
        draw(curve(pA, pB, sag, 0.6 + 2.2 * tension * (1.0 if ts is not None else 0.0)))
        return
    dt = t - ts
    mid = ((pA[0] + pB[0]) / 2, (pA[1] + pB[1]) / 2 + sag)
    for (anc, other, sg) in ((pA, mid, 1), (pB, mid, -1)):
        L = math.hypot(other[0] - anc[0], other[1] - anc[1]) * (1.0 - 0.10 * clamp(dt / 1.5))
        th0 = math.atan2(other[1] - anc[1], other[0] - anc[0])
        thd = math.pi / 2
        k = math.exp(-0.9 * dt)
        sw = math.cos(2.2 * dt + (0.0 if sg > 0 else 1.1)) * k
        th = thd + (th0 - thd) * (k * sw if sw > 0 else k * sw * 0.8) + 0.05 * math.sin(1.7 * dt + sg) * (1 - k)
        ex, ey = anc[0] + L * math.cos(th), anc[1] + L * math.sin(th)
        bend = (0.42 * k + 0.05) * L * math.sin(1.3 * dt + sg)
        ctrl = ((anc[0] + ex) / 2 + bend * math.cos(th + math.pi / 2), (anc[1] + ey) / 2 + bend * math.sin(th + math.pi / 2))
        pts = []
        for i in range(N + 1):
            u = i / N
            x_ = (1 - u) ** 2 * anc[0] + 2 * (1 - u) * u * ctrl[0] + u * u * ex
            y_ = (1 - u) ** 2 * anc[1] + 2 * (1 - u) * u * ctrl[1] + u * u * ey
            pts.append((x_, y_))
        draw(pts, 235)
    # kopma anında iki küçük parıltı
    if dt < 0.5:
        a = 1.0 - dt / 0.5
        for sg in (-1, 1):
            PN.glow(c, mid[0], mid[1], 26 * (0.5 + dt * 3), "#DCE8FF", 0.7 * a)


class Bos(Room):
    """Boş/sessiz odalar. variant="blois" (Blois şatosunda gece odası: tek pencere (ay ışığı), yatak, taş şömine, mum, ahşap kapı; bir SİLUET pencereden/kapıdan çıkıp gider: exit="door"|"window", exit_at=çapa, exit_dur=sn)
    ve "koln" (Köln'de soğuk BOŞ oda: gri-lapis, soğuk ocak, tek pencere; pencere ışığı yavaş SOLAR: fade_at, fade_dur).
    Her ikisinde thread_at=çapa: odanın ortasından ince bir çizgi geçer, thread_at'te kopar ve uçları aşağı süzülür. Yüz/ceset/son söz YOK."""
    name = "bos"

    def __init__(self, variant, tod):
        v = variant or "blois"
        self.PW = 2500
        super().__init__(v, tod)

    def build(self):
        v = self.variant
        self.layer("wall", F_WALL, self.Lw(F_WALL), self._draw_wall, wear=3)
        self.layer("main", 1.0, self.PW, self._draw_main, scale=1.2)
        self.layer("fg", F_FG, self.Lw(F_FG), self._draw_fg)
        if v == "blois":
            self.WIN_X, self.DOOR_X, self.FP_X, self.TBL = 1650, 2250, 1030, (1330, 1430)
            self.thr = ((780, 280), (2160, 390))
        else:
            self.WIN_X, self.DOOR_X, self.FP_X, self.TBL = 1250, None, 560, None
            self.thr = ((520, 300), (1960, 392))

    def paths(self):
        if self.variant == "blois":
            return {"default": [(0.0, (1150, 0, 1.0)), (1.0, (1500, 0, 1.12))],
                    "window": [(0.0, (1200, 0, 1.0)), (1.0, (1620, 30, 1.45))],
                    "exit": [(0.0, (1500, 0, 1.0)), (1.0, (1980, 20, 1.2))],
                    "sweep_r": [(0.0, (1000, 0, 1.03)), (1.0, (1540, 0, 1.03))],
                    "pull": [(0.0, (1500, 20, 1.5)), (1.0, (1200, 0, 1.0))]}
        return {"default": [(0.0, (1250, 0, 1.0)), (1.0, (1250, 0, 1.06))],
                "in": [(0.0, (1250, 0, 1.0)), (1.0, (1250, 40, 1.5))],
                "pull": [(0.0, (1250, 50, 1.7)), (1.0, (1250, 0, 1.0))],
                "sweep_r": [(0.0, (1000, 0, 1.03)), (1.0, (1500, 0, 1.03))]}

    # ── zaman ────────────────────────────────────────────────────────────
    def _exit_t(self, ctx):
        o = self.opts
        return ctx.cx.at(o["exit_at"]) if "exit_at" in o else 3.0

    def default_actors(self, ctx=None):
        if self.variant != "blois" or self.opts.get("figure", True) in (False, None):
            return []
        o = self.opts
        ex = o.get("exit", "door")
        te = self._exit_t(ctx) if ctx is not None else 3.0
        if ex == "window":
            return [dict(kind="soylu_f", x=1380, y=806, h=268, action="idle", sil="#0E0806", seed=5, dir=1, walk=(self.WIN_X - 120, 70.0), walk_at=te - (self.WIN_X - 120 - 1380) / 70.0, rim_dir=1,
                         fade_out_at=te + float(o.get("exit_dur", 2.4)), fade_out_dur=1.8)]
        dist = self.DOOR_X + 30 - 1380
        return [dict(kind="soylu_f", x=1380, y=806, h=268, action="idle", sil="#0E0806", seed=5, dir=1, walk=(self.DOOR_X + 30, 92.0), walk_at=te - dist / 92.0, rim_dir=1, fade_x=(self.DOOR_X - 60, self.DOOR_X + 20))]

    def _door_oa(self, ctx):
        if self.variant != "blois":
            return 0.0
        o = self.opts
        if o.get("exit", "door") == "window":
            return 0.0
        te = self._exit_t(ctx)
        t = ctx.t
        op = 0.62 * smooth(clamp((t - (te - 1.5)) / 0.9))
        cl = 1.0 - 0.85 * smooth(clamp((t - (te + 0.6)) / 1.6))
        return op * cl

    def _fade_k(self, ctx):
        if self.variant != "koln":
            return 0.0
        o = self.opts
        fa = ctx.cx.at(o["fade_at"]) if "fade_at" in o else 1.5
        fd = float(o.get("fade_dur", 9.0))
        return smooth(clamp((ctx.t - fa) / fd))

    # ── statik ───────────────────────────────────────────────────────────
    def _draw_wall(self, fr, xa, xb):
        c, T = fr.c, self.T
        v = self.variant
        wx = self.wx
        night = self.tod == "night"
        if v == "blois":
            GRAD_V(c, xa, OV - 40, xb, Y_FL + 30, [(T("#8C8472"), 0.0), (T("#A39A86"), 1.0)])
            ashlar(c, xa, xb, OV - 40, Y_FL + 30, T, "#9C9480", 70.0, seed=7)
            cornice(c, xa, xb, 72, T, col="#5A4A34", plaster="#A8A08C", gold=False)
            wainscot(c, xa, xb, Y_FL - 120, Y_FL + 18, T, "#5E3E26", pw=180, seed=6)
            if _vis(wx(560), 160, xa, xb):
                draw_hanging(c, T, wx(110), wx(760), 205, 548, "#233C8C", GOLD, seed=9)
            if _vis(wx(1650), 130, xa, xb):
                draw_window(c, T, wx(1650), 210, 170, 340, night=night, shutters=True)
            if _vis(wx(1030), 160, xa, xb):
                draw_tapestry(c, T, wx(1030), 190, 220, 250, seed=11, field="#3A4A6A", accent="#8E2A30", border="#8A6A32")
        else:
            GRAD_V(c, xa, OV - 40, xb, Y_FL + 30, [(T("#8E96A6"), 0.0), (T("#AEB4C0"), 1.0)])
            plaster(c, xa, xb, OV - 40, Y_FL + 30, T, "#8E96A6", "#B0B6C2", amp=0.05, warm=(236, 240, 252), cool=(60, 70, 96))
            cornice(c, xa, xb, 72, T, col="#6A7488", plaster="#A8AEBC", gold=False)
            wainscot(c, xa, xb, Y_FL - 110, Y_FL + 18, T, "#58647A", pw=190, seed=8)
            if _vis(wx(1250), 130, xa, xb):
                draw_window(c, T, wx(1250), 190, 190, 380, night=False, shutters=False, glass=("#E8EEF8", "#C6D2E4"), stone=("#8E98AA", "#A8B0C0", "#9AA2B2", "#7A8498"))
            for gx_, gw_ in ((wx(600), 130), (wx(1760), 170)):
                if _vis(gx_, 120, xa, xb):
                    c.drawRect(skia.Rect.MakeLTRB(gx_ - gw_ / 2, 230, gx_ + gw_ / 2, 230 + gw_ * 1.25), PT("#C6CCD8", 70))
                    c.drawRect(skia.Rect.MakeLTRB(gx_ - gw_ / 2, 230, gx_ + gw_ / 2, 230 + gw_ * 1.25), STK("#7A8498", 1.2, 90, False))
                    c.drawCircle(gx_, 226, 3, PT("#4A5266"))
        sh = LGP((0, Y_FL - 30), (0, Y_FL + 30), [("#0A0F1A", 0.0, 0), ("#0A0F1A", 1.0, 80)])
        c.drawRect(skia.Rect.MakeLTRB(xa, Y_FL - 30, xb, Y_FL + 30), sh)

    def _draw_main(self, fr, xa, xb):
        c, T = fr.c, self.T
        v = self.variant
        if v == "blois":
            floor_planks(c, xa, xb, Y_FL, LH, T, "#5E4228", seed=4)
            if _vis(400, 330, xa, xb):
                draw_bed(c, T, 110, 785, 560, 500, 190, cover=("#233C8C", "#C79A3C"), tester=True, wood="#4A2E1A")
            if _vis(self.FP_X, 220, xa, xb):
                fireplace(c, T, self.FP_X, 790, 300, 330, cold=True, seed=2)
            if _vis(self.DOOR_X, 140, xa, xb):
                doorway_stone(c, T, self.DOOR_X, 790, 170, 440)
            if _vis(1380, 120, xa, xb):
                x0t, x1t = 1290, 1470
                BOX(c, x0t, 700, x1t, 716, "#5A3820", T, ink=1.4)
                for lx in (x0t + 14, x1t - 14):
                    R(c, lx - 5, 716, lx + 5, 800, T("#4A2E1A"))
                    INKR(c, lx - 5, 716, lx + 5, 800, 1.1, 190)
            if _vis(1800, 100, xa, xb):
                draw_chest(c, T, 1730, 1930, 790, 110, "#4A2E1A")
        else:
            floor_planks(c, xa, xb, Y_FL, LH, T, "#667282", seed=5, w0=230.0)
            if _vis(self.FP_X, 220, xa, xb):
                fireplace(c, T, self.FP_X, 790, 300, 330, cold=True, col="#8E96A4", seed=3)

    def _draw_fg(self, fr, xa, xb):
        c, T = fr.c, self.T
        fx = lambda x: W / 2 + (x - W / 2) * F_FG
        col = "#10141E" if self.variant == "koln" else "#1E140C"
        for x in (60, 2440):
            if _vis(fx(x), 90, xa, xb):
                xx = fx(x)
                R(c, xx - 26, OV - 40, xx + 26, 900, col)
                HGRAD(c, xx - 26, OV - 40, xx + 26, 900, [("#FFFFFF", 0.0, 24), ("#000000", 1.0, 80)])

    # ── canlı ────────────────────────────────────────────────────────────
    def dyn_wall(self, ctx):
        f, t = ctx.f, ctx.t
        wx = self.wx
        if self.variant == "blois":
            if _vis(wx(1650), 400, ctx.xa, ctx.xb):
                window_light(f, wx(1650), 226, 150, 300, t, dx=-300, y_floor=Y_FL + 20, a=0.12, seed=3, patch=False, dust=8, night=True, part="shaft")
        else:
            if _vis(wx(1250), 400, ctx.xa, ctx.xb):
                k = 1.0 - self._fade_k(ctx)
                window_light(f, wx(1250), 206, 160, 350, t, dx=320, y_floor=Y_FL + 20, a=0.28 * k, seed=3, patch=False, dust=int(10 * k), night=True, part="shaft", col="#DCE6FF")

    def dyn_main(self, ctx):
        f, c, t, cx = ctx.f, ctx.c, ctx.t, ctx.cx
        T = self.T
        v = self.variant
        if v == "blois":
            window_light(f, 1650, 226, 150, 300, t, dx=-300, y_floor=Y_FL + 70, a=0.12, seed=3, patch=True, dust=0, night=True, part="patch", patch_h=110)
            # şömine közü: çok sönük
            for k in range(5):
                a = 0.5 + 0.5 * math.sin(t * 1.3 + k * 1.7)
                c.drawCircle(self.FP_X - 56 + k * 28, 782, 3.0 + a, PT("#FF8A2A", int(60 + 90 * a)))
            PN.glow(c, self.FP_X, 770, 120, "#FF7A20", 0.10)
            oa = self._door_oa(ctx)
            self._oa = oa
            if _vis(self.DOOR_X, 140, ctx.xa, ctx.xb):
                op = skia.Path()
                x0, x1 = self.DOOR_X - 85, self.DOOR_X + 85
                r = 85
                op.moveTo(x0, 790)
                op.lineTo(x0, 790 - 440 + r)
                op.arcTo(skia.Rect.MakeLTRB(x0, 790 - 440, x1, 790 - 440 + 2 * r), 180, 180, False)
                op.lineTo(x1, 790)
                op.close()
                c.save()
                c.clipPath(op, skia.ClipOp.kIntersect, True)
                door_leaf(f, self.DOOR_X, 790, 440, 170, oa, T, seed=3, light=("#141C34", "#34447A"), hinge=1)
                c.restore()
            # masa: mum + kâse
            cx_, cy_ = 1380, 700
            lit = float(self.opts.get("candle_lit", 1.0))
            if "snuff_at" in self.opts:
                lit *= 1.0 - cx.amt(self.opts["snuff_at"], 0.35)
            candle(f, cx_, cy_, 60, t, seed=2.2, lit=lit, holder=True)
            draw_goblet(c, 1432, 700, 0.9)
            draw_extra(ctx, "back")
            dust_motes(c, t, cx_ - 220, cy_ - 220, cx_ + 220, cy_ + 20, n=12, seed=31, a=0.5, size=1.7, drift=(4, -2), col="#FFE2A0")
        else:
            k = 1.0 - self._fade_k(ctx)
            window_light(f, 1250, 206, 160, 350, t, dx=320, y_floor=Y_FL + 70, a=0.30 * k, seed=3, patch=True, dust=0, night=True, part="patch", patch_h=120, col="#DCE6FF")
            draw_extra(ctx, "back")

    def dyn_front(self, ctx):
        f, t, cx = ctx.f, ctx.t, ctx.cx
        draw_extra(ctx, "front")
        if self.variant == "blois" and _vis(780, 2000, ctx.xa, ctx.xb) or self.variant == "koln":
            pass
        o = self.opts
        if "thread_at" in o or o.get("thread", False):
            ts = cx.at(o["thread_at"]) if "thread_at" in o else None
            pA, pB = self.thr
            if "thread_from" in o:
                pA = tuple(o["thread_from"])
            if "thread_to" in o:
                pB = tuple(o["thread_to"])
            thread_line(f, pA, pB, t, ts)
        # blois: bağlı yatak perdesi
        if self.variant == "blois" and _vis(700, 200, ctx.xa, ctx.xb):
            draw_drape(ctx.c, 110 + 560 + 14, 785 - 492 + 28 + 30, 74, 395, t, col="#233C8C", col2=GOLD, amp=0.04, seed=4, ph=1.1, tie=0.62)

    def dyn_fg(self, ctx):
        c, t = ctx.c, ctx.t
        rs = _RS(49)
        xa, xb = ctx.xa, ctx.xb
        for k in range(12):
            x = xa + ((rs.rand() * (xb - xa) + t * 10 * (0.5 + rs.rand())) % (xb - xa))
            y = 120 + rs.rand() * 700 + math.sin(t * 0.6 + k) * 14
            c.drawCircle(x, y, 1.6 + 2.0 * rs.rand(), PT("#DCE6FF" if self.variant == "koln" else "#FFEFC4", int(30 + 50 * rs.rand())))

    def light(self, ctx):
        if self.variant == "blois":
            return (1380, 640, 760.0, 1.0)
        return (1250, 460, 1000.0, 1.0)

    def finish(self, ctx):
        """Köln: soğuk lapis örtü + pencere ışığı solarken kararma; Blois standart mum havuzu."""
        if self.variant != "koln":
            return False
        f, cx = ctx.f, ctx.cx
        c = f.c
        k = self._fade_k(ctx)
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), PT("#3A4A7C", 84))
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), PT("#060A16", int(255 * 0.80 * k)))
        CM.vig(f, 0.60, mode="night")
        return True


ROOMS["bos"] = Bos


# ═════════════════════════════ SAHNE (Pitti sarayı, Euridice) ═════════════════════════════
def audience_row(c, x0, x1, y, seed=1, col="#120A06", scale=1.0, rim=None):
    """İzleyici sırası (arkadan siluet): omuz yuvarlakları + baş + zaman zaman şapka/tüy; (y = omuz alt çizgisi)."""
    rs = _RS(seed)
    x = x0
    while x < x1:
        w = rs.uniform(54, 74) * scale
        hr = rs.uniform(19, 25) * scale
        c.drawOval(skia.Rect.MakeLTRB(x - w / 2, y - 46 * scale, x + w / 2, y + 40 * scale), PT(col))
        c.drawCircle(x + rs.uniform(-4, 4), y - 46 * scale - hr * 0.7, hr, PT(col))
        k = rs.rand()
        if k < 0.25:
            c.drawPath(sk.poly_path([(x - hr * 1.1, y - 50 * scale - hr * 1.2), (x + hr * 1.1, y - 50 * scale - hr * 1.2), (x + hr * 0.8, y - 50 * scale - hr * 1.9), (x - hr * 0.8, y - 50 * scale - hr * 1.9)]), PT(col))
        elif k < 0.40:
            p = skia.Path()
            p.moveTo(x + hr * 0.2, y - 50 * scale - hr * 1.6)
            p.quadTo(x + hr * 1.6, y - 50 * scale - hr * 2.8, x + hr * 2.2, y - 50 * scale - hr * 1.2)
            c.drawPath(p, STK(col, 3.0 * scale, 255))
        if rim:
            c.drawArc(skia.Rect.MakeLTRB(x - w / 2, y - 46 * scale, x + w / 2, y + 40 * scale), 200, 100, False, STK(rim, 1.6, 150)) if hasattr(c, "drawArc") else None
        x += w * 0.82


def box_tier(c, T, x0, x1, y0, y1, seed=1, spect=True):
    """Yaldız korkuluklu loca katı: kırmızı kadife iç, altın balüstr, silüet seyirciler."""
    R(c, x0, y0, x1, y1, T("#3A1A18"))
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), LGP((0, y0), (0, y1), [("#2A1210", 0.0, 255), ("#5A2A24", 1.0, 255)]))
    if spect:
        audience_row(c, x0 + 40, x1 - 20, y1 - 6, seed, "#150C08", 0.8)
    BOX(c, x0 - 8, y1 - 6, x1 + 8, y1 + 26, "#C79A3C", T, hl=0.2, sh=0.2, ink=1.4)
    for xx in np.arange(x0 + 10, x1, 26):
        c.drawLine(xx, y1 + 2, xx, y1 + 22, STK(T("#8A6422"), 4.0, 255, False))
    INKR(c, x0 - 8, y0 - 6, x1 + 8, y1 + 26, 1.6, 210)
    BOX(c, x0 - 8, y0 - 14, x1 + 8, y0 + 2, "#C79A3C", T, hl=0.2, sh=0.2, ink=1.4)


class Perde(Room):
    """Pitti sarayı sahnesi (Euridice): çerçeveli sahne ağzı (yaldız sütun + kadife saçaklı başlık, Medici arması), boyalı pastoral fon (tepeler, ağaçlar, güneş, akan bulut), ayak ışığı (mum sırası),
    PERDE AÇILIR (open_at çapa, open_dur sn): iki yarı yana toplanır; sahnede iki SİLUET (Orfeo / Euridice: sing/gesture); iki yanda locaların seyirci siluetleri, önde arkadan izleyici sıraları.
    actors verilmezse sahne figürleri; stage=False → boş sahne."""
    name = "perde"
    PW = 2400
    SX0, SX1, SY0, SYB = 700, 1700, 170, 662

    def build(self):
        self.layer("wall", F_WALL, self.Lw(F_WALL), self._draw_wall, wear=3)
        self.layer("main", 1.0, self.PW, self._draw_main, scale=1.2)
        self.layer("front", 1.0, self.PW, self._draw_front)
        self.layer("fg", F_FG, self.Lw(F_FG), self._draw_fg)

    def paths(self):
        return {"default": [(0.0, (1200, 0, 1.0)), (1.0, (1200, 10, 1.14))],
                "in": [(0.0, (1200, 0, 1.0)), (1.0, (1200, 60, 1.75))],
                "stage": [(0.0, (1200, 40, 1.4)), (1.0, (1200, 60, 1.6))],
                "sweep_r": [(0.0, (1000, 0, 1.0)), (1.0, (1400, 0, 1.0))],
                "pull": [(0.0, (1200, 60, 1.7)), (1.0, (1200, 0, 1.0))]}

    def default_actors(self, ctx=None):
        if self.opts.get("stage", True) is False:
            return []
        return [dict(kind="soylu", x=1090, y=655, h=250, action="point", sil="#0E0806", seed=5, dir=1, rim_dir=1, t0=1.0),
                dict(kind="soylu_f", x=1340, y=662, h=244, action="talk", sil="#0E0806", seed=9, dir=-1, rim_dir=-1, phase=0.4, energy=0.8)]

    def open_k(self, ctx):
        o = self.opts
        if "open_at" not in o:
            return float(o.get("open", 1.0))
        return smooth(clamp((ctx.t - ctx.cx.at(o["open_at"])) / float(o.get("open_dur", 3.2))))

    def _draw_wall(self, fr, xa, xb):
        c, T = fr.c, self.T
        wx = self.wx
        plaster(c, xa, xb, OV - 40, Y_FL + 30, T, "#6A4A38", "#8A6A52", amp=0.05)
        cornice(c, xa, xb, 72, T, col="#8A6422", plaster="#9A7A5C")
        for side, (a, b) in enumerate(((100, 600), (1800, 2300))):
            for tier in range(3):
                y0 = 210 + tier * 150
                if _vis(wx((a + b) / 2), 340, xa, xb):
                    box_tier(c, T, wx(a), wx(b), y0, y0 + 110, seed=side * 7 + tier)
        sh = LGP((0, Y_FL - 30), (0, Y_FL + 30), [("#1A0F06", 0.0, 0), ("#1A0F06", 1.0, 80)])
        c.drawRect(skia.Rect.MakeLTRB(xa, Y_FL - 30, xb, Y_FL + 30), sh)

    def _draw_main(self, fr, xa, xb):
        c, T = fr.c, self.T
        x0, x1, y0, yb = self.SX0, self.SX1, self.SY0, self.SYB
        floor_planks(c, xa, xb, Y_FL, LH, T, "#5E4228", seed=11, w0=260.0)
        # sahne zemini (daha açık tahta) + pervaz
        if _vis(1200, 560, xa, xb):
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(x0 - 40, yb - 10, x1 + 40, 712))
            floor_planks(c, x0 - 40, x1 + 40, yb - 10, 712, T, "#8A6038", seed=13, w0=180.0, rowh=12.0, grow=1.12)
            c.restore()
            BOX(c, x0 - 60, 706, x1 + 60, 734, "#7A5A22", T, hl=0.2, sh=0.2, ink=1.5)
            c.drawLine(x0 - 60, 718, x1 + 60, 718, STK(T(GOLD), 2.0, 220, False))
            # boyalı fon (sahne ağzı içi)
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(x0, y0, x1, yb))
            GRAD_V(c, x0, y0, x1, yb, [(T("#9FC4E8"), 0.0), (T("#F2E4B8"), 0.7), (T("#E8D8A0"), 1.0)])
            c.drawCircle(1380, 330, 44, PT(T("#FFF0B0"), 235))
            for k, (base, col, amp) in enumerate(((470, "#8AA0B0", 38), (530, "#6E9A7A", 46), (590, "#4E7A58", 54))):
                pth = skia.Path()
                pth.moveTo(x0, yb)
                for xx in range(x0, x1 + 8, 8):
                    pth.lineTo(xx, base + amp * math.sin(xx * 0.008 + k * 2.0) + amp * 0.5 * math.sin(xx * 0.021 + k))
                pth.lineTo(x1, yb)
                pth.close()
                c.drawPath(pth, PT(T(col)))
                c.drawPath(pth, STK(INK, 1.2, 120))
            for tx, th in ((850, 150), (1010, 120), (1530, 160), (1620, 110)):
                R(c, tx - 6, yb - th, tx + 6, yb - 6, T("#5A3A20"))
                for (qx, qy, qr) in ((tx, yb - th - 20, 44), (tx - 28, yb - th + 6, 32), (tx + 28, yb - th + 8, 32)):
                    c.drawCircle(qx, qy, qr, PT(T("#2E7A4A")))
                    c.drawCircle(qx, qy, qr, STK(INK, 1.2, 160))
            c.restore()
            # kulis (yan paravanlar)
            for sg in (-1, 1):
                px = x0 - 4 if sg < 0 else x1 + 4
                BOX(c, px - (46 if sg < 0 else 0), y0 + 20, px + (0 if sg < 0 else 46), 706, "#2A1A18", T, ink=1.5)
            # sahne ağzı: yaldız sütunlar + kadife başlık
            for sx0, sx1 in ((x0 - 74, x0 - 6), (x1 + 6, x1 + 74)):
                BOX(c, sx0, y0 - 40, sx1, 712, "#C79A3C", T, hl=0.22, sh=0.28, ink=1.6)
                for yy in np.arange(y0, 700, 46):
                    c.drawLine(sx0 + 12, yy, sx0 + 12, yy + 34, STK(T("#8A6422"), 2.0, 160, False))
                R(c, sx0 - 8, y0 - 56, sx1 + 8, y0 - 36, T("#D8B25A"))
                INKR(c, sx0 - 8, y0 - 56, sx1 + 8, y0 - 36, 1.3, 190)
            BOX(c, x0 - 82, y0 - 70, x1 + 82, y0 - 38, "#C79A3C", T, hl=0.22, sh=0.22, ink=1.6)
            pel = skia.Path()
            pel.moveTo(x0 - 74, y0 - 38)
            pel.lineTo(x1 + 74, y0 - 38)
            n = 14
            for i in range(n + 1):
                xx = (x1 + 74) - (x1 - x0 + 148) * i / n
                pel.lineTo(xx, y0 + 38)
                if i < n:
                    pel.quadTo(xx - (x1 - x0 + 148) / n / 2, y0 + 78, xx - (x1 - x0 + 148) / n, y0 + 38)
            pel.close()
            FILLP(c, pel, T("#8E1F26"), 255, 1.5, 200, shader=LGP((0, y0 - 38), (0, y0 + 80), [(T("#6A1018"), 0.0), (T("#A82A30"), 1.0)]))
            c.drawLine(x0 - 74, y0 + 6, x1 + 74, y0 + 6, STK(T(GOLD), 2.6, 220, False))
            draw_arms(c, T, 1200, y0 - 126, 0.9, frame=False) if False else None

    def _draw_front(self, fr, xa, xb):
        c, T = fr.c, self.T
        # ayak ışığı sırası tabanı
        if _vis(1200, 600, xa, xb):
            BOX(c, self.SX0 - 20, 690, self.SX1 + 20, 710, "#3A2A18", T, ink=1.4)
            for xx in np.linspace(self.SX0 + 30, self.SX1 - 30, 9):
                c.drawOval(skia.Rect.MakeLTRB(xx - 10, 684, xx + 10, 694), PT(T("#B8903A")))
                c.drawOval(skia.Rect.MakeLTRB(xx - 10, 684, xx + 10, 694), STK(INK, 0.9, 180))

    def _draw_fg(self, fr, xa, xb):
        c, T = fr.c, self.T
        fx = lambda x: W / 2 + (x - W / 2) * F_FG
        # arkadan izleyici sıraları (önde, koyu)
        for k, (a, b) in enumerate(((130, 640), (1760, 2290))):
            if _vis(fx((a + b) / 2), 360, xa, xb):
                audience_row(c, fx(a), fx(b), 905, 31 + k, "#0E0806", 1.25)
                audience_row(c, fx(a) + 30, fx(b) - 20, 1000, 41 + k, "#0A0604", 1.45)

    def dyn_wall(self, ctx):
        pass

    def dyn_main(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        # akan bulutlar (fon; bant içine kırpılı)
        x0, x1, y0, yb = self.SX0, self.SX1, self.SY0, self.SYB
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(x0, y0, x1, yb))
        cl = PN.cloud_sprite()
        for k in range(3):
            xx = x0 - 460 + ((t * (9 + 4 * k) + k * 480) % (x1 - x0 + 920))
            c.save()
            c.translate(xx, y0 + 70 + k * 46)
            c.scale(1.2 - 0.2 * k, 1.2 - 0.2 * k)
            c.drawImage(cl, 0, 0, LIN)
            c.restore()
        c.restore()
        draw_extra(ctx, "back")

    def dyn_front(self, ctx):
        f, c, t, cx = ctx.f, ctx.c, ctx.t, ctx.cx
        T = self.T
        draw_extra(ctx, "front")
        x0, x1, y0, yb = self.SX0, self.SX1, self.SY0, self.SYB
        # ayak ışığı mumları
        for i, xx in enumerate(np.linspace(self.SX0 + 30, self.SX1 - 30, 9)):
            candle(f, xx, 690, 26, t, seed=i * 1.9, holder=False, lit=1.0, smoke=False, halo=0.8, wax="#EFE6CE")
        # perde: iki yarı; k = açılma
        k = self.open_k(ctx)
        half = (x1 - x0) / 2
        gather = 110
        wL = max(gather, half * (1 - k) + gather * k) if k < 1.0 else gather
        wL = gather + (half - gather) * (1 - k)
        hh = yb - y0 + 40
        ph = 0.0
        for sgn in (-1, 1):
            c.save()
            if sgn < 0:
                c.translate(x0 - 0, y0 - 6)
                c.scale(wL / 400.0, 1.0)
                draw_drape(c, 0, 0, 400, hh, t, col="#8E1F26", col2=GOLD, amp=0.03, seed=3, ph=ph + 0.4)
            else:
                c.translate(x1 - wL, y0 - 6)
                c.scale(wL / 400.0, 1.0)
                draw_drape(c, 0, 0, 400, hh, t, col="#8E1F26", col2=GOLD, amp=0.03, seed=3, ph=ph + 1.7)
            c.restore()
        # kapalıyken orta dikiş
        if k < 0.04:
            c.drawLine((x0 + x1) / 2, y0 - 6, (x0 + x1) / 2, yb + 34, STK("#2A0A0C", 3.0, 220, False))

    def dyn_fg(self, ctx):
        c, t = ctx.c, ctx.t
        rs = _RS(50)
        xa, xb = ctx.xa, ctx.xb
        for k in range(12):
            x = xa + ((rs.rand() * (xb - xa) + t * 10 * (0.5 + rs.rand())) % (xb - xa))
            y = 120 + rs.rand() * 700 + math.sin(t * 0.6 + k) * 14
            c.drawCircle(x, y, 1.6 + 2.0 * rs.rand(), PT("#FFEFC4", int(30 + 50 * rs.rand())))

    def light(self, ctx):
        return (1200, 640, 980.0, 1.0)


ROOMS["perde"] = Perde


# ═════════════════════════════ #### ODALAR ####
# (aşağıya odalar eklenir)
