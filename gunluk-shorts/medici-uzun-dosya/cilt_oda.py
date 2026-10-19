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
OVER = "o2"                      # önbellek sürümü (çizim kodu değişince artır)
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
        fh = s * 0.46 * fl * lit
        PN.glow(c, fx0, fy0 - fh * 0.5, s * 3.6 * lit + 30, "#FFB454", 0.34 * br * lit)
        c.drawPath(_flame_path(fx0, fy0, fh, s * 0.20, lean * fh * 0.25), PT("#FF9A3A", 235))
        c.drawPath(_flame_path(fx0, fy0, fh * 0.78, s * 0.12, lean * fh * 0.18), PT("#FFD66B", 250))
        c.drawPath(_flame_path(fx0, fy0, fh * 0.42, s * 0.06, 0), PT("#FFF6D6", 255))
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
def _bronze_leaf(w, h, seed, rows=5):
    """Tek kanat sprite'ı: tunç degrade + panel çerçeveleri + kabartma (yuvarlak madalyon, rozet, haçvari) + perçin sırası. Orijin sol-üst."""
    pad = 6
    fr = sk.Frame(int(w) + 2 * pad, int(h) + 2 * pad)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
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
    img, pad = _bronze_leaf(int(lw), int(h), seed)
    for sgn in (-1, 1):
        hinge = x + sgn * lw
        far = hinge - sgn * ew
        q = sk.poly_path([(hinge, top), (far, top + sk_), (far, y - sk_), (hinge, y)])
        c.save()
        c.clipPath(q, skia.ClipOp.kIntersect, True)
        c.translate(hinge, top)
        c.scale((ew / lw) if sgn < 0 else -(ew / lw), 1.0)
        c.drawImage(img, -pad, -pad, LIN)
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
    for off, cf in ((rim_w, warm), (0.0, flat)):
        if cf is None:
            continue
        c.save()
        c.translate(off * rim_dir * 0.9, -off * 0.5)
        if walker is not None:
            FA.walker(f, kind, x, y, h, t, speed=walker, dir=dir, seed=seed, phase=phase, alpha=alpha, cf=cf, prop=prop, **p)
        else:
            FA.actor(f, kind, x, y, h, t, action=action, dir=dir, seed=seed, phase=phase, alpha=alpha, cf=cf, prop=prop, **p)
        c.restore()


def seated(f, kind, x, y, h, t, action="write", dir=1, seed=0, phase=0.0, sil=None, rim="#E8A860", rim_dir=1, t0=0.0, alpha=1.0, **stil):
    """Masa başında oturan figür (masa/sandalye odanın kendi çizimidir; FA masası ÇİZİLMEZ). action: write | count | idle(oturan) …
    sil=renk → siluet. Dönüş: act_write ek bilgisi (satır, ilerleme) — belge yazılışını elle eşlemek için."""
    kit, bh = FA.kit_for(kind, seed, h, **stil)
    fn = FA.ACTIONS[action]
    pz = fn(kit, t, phase=phase, t0=t0) if action in ("write", "count") else fn(kit, t, phase=phase)
    ex = dict(pz.extra) if getattr(pz, "extra", None) else {}
    FA.cloth_for(kit, pz, t, phase * 6.28, lag=0.0, wave=0.0)
    c = f.c
    passes = [(0.0, None)] if not sil else [(1.5, flat_cf(rim)), (0.0, flat_cf(sil))]
    for off, cf in passes:
        c.save()
        c.translate(off * rim_dir * 0.9, -off * 0.5)
        c.save()
        FA.place_fig(c, x, y, h, bh, dir)
        FA.draw_fig(c, kit, pz, alpha, cf)
        c.restore()
        c.restore()
    return ex


def lying_sil(f, x, y, t, scale=1.0, color="#1A1008", rim="#E8A860", rim_dir=1, breath=1.0):
    """Yatakta yatan kadın SİLÜETİ (yandan; baş solda yastıkta, örtü altında gövde; yüz/ayrıntı yok): yavaş nefes. (x,y) = yastığın alt-sol köşesi."""
    c = f.c
    b = 1.0 + 0.012 * math.sin(t * 1.15) * breath
    s = scale
    # örtü yığını (omuz → ayak): düz koyu + kenar ışığı
    def mound(dx, dy, col, a=255):
        p = skia.Path()
        p.moveTo(x + 40 * s + dx, y - 6 * s + dy)
        p.cubicTo(x + 60 * s + dx, y - 62 * s * b + dy, x + 110 * s + dx, y - 66 * s * b + dy, x + 170 * s + dx, y - 54 * s * b + dy)
        p.cubicTo(x + 240 * s + dx, y - 44 * s * b + dy, x + 330 * s + dx, y - 38 * s * b + dy, x + 410 * s + dx, y - 22 * s + dy)
        p.lineTo(x + 410 * s + dx, y - 4 * s + dy)
        p.lineTo(x + 40 * s + dx, y - 4 * s + dy)
        p.close()
        c.drawPath(p, PT(col, a))
        # baş (yandan, yastıkta) + omuz hattı
        hd = skia.Path()
        hd.addOval(skia.Rect.MakeLTRB(x + 4 * s + dx, y - 62 * s + dy, x + 58 * s + dx, y - 14 * s + dy))
        c.drawPath(hd, PT(col, a))
        # tülbent/bone (başın arkası)
        bn = skia.Path()
        bn.moveTo(x + 2 * s + dx, y - 40 * s + dy)
        bn.quadTo(x + 4 * s + dx, y - 74 * s + dy, x + 40 * s + dx, y - 70 * s + dy)
        bn.quadTo(x + 60 * s + dx, y - 56 * s + dy, x + 50 * s + dx, y - 38 * s + dy)
        bn.close()
        c.drawPath(bn, PT(col, a))
    if rim:
        mound(1.4 * rim_dir, -1.6, rim)
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
        if sil:
            sil_actor(f, kind, x, y, h, t, dir=dirn, seed=seed, phase=phase, color=sil if isinstance(sil, str) else "#1A1008", rim_dir=rim_dir, walker=v_now, **d)
        else:
            FA.walker(f, kind, x, y, h, t, speed=v_now, dir=dirn, seed=seed, phase=phase, **d)
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
    world.actors_extra = actors or []
    world.props_extra = props or []
    a = cx.amt(at, 0.9) if at else 1.0
    dur = max(cx.dur, 1e-3)
    default = world.get_path(path or "default") if not cams else None
    pc = PN.PanoCam(cx, cams, default, dur)
    t_cam = clamp(cx.t, 0.0, dur)
    camx, camy, z = pc.at(t_cam)
    st = getattr(cx, "cam_state", None)
    if st is not None and not cams and not path:
        camx += st.x
        camy += st.y
        z *= st.zoom
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
    lt = world.light(ctx)
    if tod == "night" or (lt is not None and lt[3] > 0 and tod != "day"):
        if lt is not None:
            lx, ly, lr, lk = lt
            sx, sy = ctx.to_screen(1.0, lx, ly)
            base = CM.candle_light(cx.t, seed, base=(sx, sy), r=lr * z, sway=2.0 * z)
            CM.finish(f, cx, motes_n=10, light=(base[0], base[1], base[2], base[3] * 1.0), k=lk)
        else:
            CM.finish(f, cx, motes_n=10, light=CM.candle_light(cx.t, seed, base=(W * 0.5, H * 0.5), r=1200.0, sway=6.0))
    else:
        CM.finish(f, cx, motes_n=14)


# ───────────────────────────── ortak canlı katman parçaları ─────────────────────────────
def draw_extra(ctx, layer):
    """Çağıranın verdiği actors/props (layer='back' → dyn_main; 'front' → dyn_front)."""
    room = ctx.room
    for d in sorted([a for a in getattr(room, "actors_extra", []) if a.get("layer", "back") == layer], key=lambda q: q.get("y", 0)):
        x = d["x"]
        if ctx.xa - 700 < x < ctx.xb + 700:
            draw_actor(ctx, d)
    if layer == "back":
        for d in getattr(room, "props_extra", []):
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


def draw_window(c, T, x, y, w, h, night=False, arch=True, shutters=True, glass=None, mullion=True, sill=True):
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
    FILLP(c, opening(18), T("#CBBB96"), 255, 1.6, 200)
    FILLP(c, opening(9), T("#E6DAB8" if not night else "#B8AC8C"), 255, 1.0, 160)
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
        c.drawLine(x, y - 8, x, yb, STK(T("#B8A880"), 8.0, 255, False))
        c.drawLine(x, y - 8, x, yb, STK(INK, 1.0, 180, False))
        ty = y + h * 0.42
        c.drawLine(x0, ty, x1, ty, STK(T("#B8A880"), 8.0, 255, False))
        c.drawLine(x0, ty, x1, ty, STK(INK, 1.0, 180, False))
    # iç şev gölgesi (sağ)
    HGRAD(c, x1 - 22, y, x1 + 2, yb, [("#000000", 0.0, 0), ("#000000", 1.0, 70)])
    HGRAD(c, x0 - 2, y, x0 + 14, yb, [("#FFFFFF", 0.0, 40), ("#FFFFFF", 1.0, 0)])
    c.restore()
    INKP(c, op, 2.2, 230)
    if sill:
        FILLP(c, sk.poly_path([(x0 - 30, yb + 10), (x1 + 30, yb + 10), (x1 + 38, yb + 26), (x0 - 38, yb + 26)]), T("#D7C9A4"), 255, 1.4, 200)
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
    """Duvar şamdanı (demir kol + kap); mum canlı çizilir. (x,y) duvara bağlantı."""
    p = skia.Path()
    p.moveTo(x, y)
    p.cubicTo(x + side * 20 * s, y - 6 * s, x + side * 34 * s, y + 14 * s, x + side * 40 * s, y + 4 * s)
    c.drawPath(p, STK("#2A2018", 4.0 * s, 255))
    c.drawOval(skia.Rect.MakeLTRB(x + side * 40 * s - 14 * s, y + 2 * s, x + side * 40 * s + 14 * s, y + 10 * s), PT("#3A2A1C"))
    c.drawOval(skia.Rect.MakeLTRB(x + side * 40 * s - 14 * s, y + 2 * s, x + side * 40 * s + 14 * s, y + 10 * s), STK(INK, 1.0, 190))
    c.drawCircle(x, y, 7 * s, PT("#3A2A1C"))
    c.drawCircle(x, y, 7 * s, STK(INK, 1.0, 190))
    return x + side * 40 * s, y + 4 * s


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
        if _vis(wx(1660), 60, xa, xb):
            sconce(c, T, wx(1660), 330, 1.0, 1)
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
        if _vis(x, 60, xa, xb):
            # yüksek demir şamdan siluet (ön plan, koyu)
            col = "#1E140C"
            R(c, x - 4, 330, x + 4, 880, col)
            c.drawOval(skia.Rect.MakeLTRB(x - 36, 862, x + 36, 892), PT(col))
            for yy in (500, 700):
                c.drawOval(skia.Rect.MakeLTRB(x - 11, yy - 8, x + 11, yy + 8), PT(col))
            p = skia.Path()
            p.moveTo(x - 46, 322)
            p.quadTo(x - 46, 346, x, 348)
            p.quadTo(x + 46, 346, x + 46, 322)
            c.drawPath(p, STK(col, 5.0, 255))
            R(c, x - 3, 308, x + 3, 330, "#2A1E14")

    # ── canlı katmanlar ─────────────────────────────────────────────────
    def dyn_wall(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        night = ctx.tod == "night"
        wx = self.wx
        if ctx.tod in ("day", "dusk"):
            window_light(f, wx(1010), 232, 170, 300, t, dx=-330 if False else 300, y_floor=Y_FL + 40, a=0.17 if ctx.tod == "day" else 0.12, seed=3, patch=False, dust=16, night=False, part="shaft")
        elif night:
            window_light(f, wx(1010), 232, 170, 300, t, dx=260, y_floor=Y_FL + 40, a=0.10, seed=3, patch=False, dust=6, night=True, part="shaft")
        # duvar şamdanı mumu
        sx, sy = wx(1660) + 40, 334
        candle(f, sx, sy, 46, t, seed=4.7, holder=False, wax="#EAE0C4", lit=1.0 if night or ctx.tod == "dusk" else 0.0, smoke=False, halo=0.9)

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
            lying_sil(f, px + 8, py + 2, t, 1.0, color="#1A1008", rim="#E8A860" if night else "#C79A5A", rim_dir=1)
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
        candle(f, fx(1560), 310, 38, t, seed=8.8, holder=False, lit=1.0 if night else 0.0, smoke=False, halo=0.8, wax="#D8CDB0")
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


# ═════════════════════════════ #### ODALAR ####
# (aşağıya odalar eklenir)
