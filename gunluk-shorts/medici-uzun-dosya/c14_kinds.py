"""c14_kinds — c14 «Yıldızlar, Notalar, Taşlar» özel çekim türleri (Parça 7 sahne yazarı). `scenes_c14.py` içinde import edilir; `@CM.ckind` ile kaydolur.

Dünya koordinatı = nötr kamerada ekran koordinatı (1920×1080). Kamera: `cam=[(çapa, look(wx, wy, z)), …]` (p7_lib.look) ya da `cam=("push", …)`.
Olgu disiplini: yüz yok (siluet/simge/levha); şiddet yok; Arapça harfler STİLİZE biçimlerdir (okunur metin iddiası yok, bir sözcük/ayet yazılmaz);
ekrana yalnız script/brif sözcükleri yazılır (metinler sahne dosyasından parametreyle gelir).
Her tür `ovl=` (çapaya bağlı bindirme: etiket, damga, tarih plakası …) kabul eder; ovl ışıktan SONRA çizilir.
"""
import math

import numpy as np
import skia

import cilt_anim as FA
import cilt_medici as CM
import cilt_oda as OD
import cilt_paper as PP
import icons
import p7_lib as L
import sk
from cilt_medici import TH
from p7_lib import INK, P, S, SOFT, look, ov
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth


def A(a):
    return int(max(0, min(255, a)))


# ═══════════════════════════ ortak: ahşap, metal, stilize Arapça harf ═══════════════════════════
def wood_floor(c, y0, a=255, seed=1, x0=-700, x1=4300):
    """Tezgâh/zemin: ahşap levhalar (degrade + damar + derz)."""
    sh = skia.GradientShader.MakeLinear([(0, y0), (0, H + 200)], [C("#8A5E36", a), C("#4E301A", a)], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, H + 300), skia.Paint(Shader=sh))
    rs = np.random.RandomState(seed)
    for i in range(34):
        yy = y0 + 8 + rs.rand() * (H - y0 + 120)
        xs = x0 + rs.rand() * (x1 - x0)
        c.drawLine(xs, yy, xs + 160 + rs.rand() * 420, yy + rs.randn() * 2.0, S("#2A1608", 1.3, A(52 * a / 255)))
    xx = x0
    while xx < x1:
        c.drawLine(xx, y0, xx - 120, H + 300, S("#2A1608", 1.6, A(95 * a / 255)))
        xx += 360
    c.drawLine(x0, y0, x1, y0, S("#2A1608", 3.0, A(230 * a / 255)))
    c.drawLine(x0, y0 + 4, x1, y0 + 4, S("#E8C58A", 1.2, A(70 * a / 255)))


def metal_rect(c, x0, y0, x1, y1, base="#8E9096", a=255, r=0, ink=1.4, horiz=True):
    cols = [C(mix(base, "#FFFFFF", 0.45), a), C(base, a), C(mix(base, "#000000", 0.45), a)]
    if horiz:
        sh = skia.GradientShader.MakeLinear([(x0, 0), (x1, 0)], cols, [0.0, 0.42, 1.0])
    else:
        sh = skia.GradientShader.MakeLinear([(0, y0), (0, y1)], cols, [0.0, 0.42, 1.0])
    rc = skia.Rect.MakeLTRB(x0, y0, x1, y1)
    if r:
        c.drawRoundRect(rc, r, r, skia.Paint(AntiAlias=True, Shader=sh))
        if ink:
            c.drawRoundRect(rc, r, r, S("#15110C", ink, A(0.78 * a)))
    else:
        c.drawRect(rc, skia.Paint(AntiAlias=True, Shader=sh))
        if ink:
            c.drawRect(rc, S("#15110C", ink, A(0.78 * a), cap=False))


def glyph_path(kind, x, y, s):
    """Stilize Arapça harf biçimi yolu: (path, noktalar). Okunur sözcük DEĞİL; yalnız yazı karakteri hissi (gövde, kuyruk, nokta)."""
    pa = skia.Path()
    dots = []
    k = kind % 8
    if k == 0:      # elif: dik, hafif ince uca
        pa.moveTo(x + s * 0.02, y - s * 0.50)
        pa.quadTo(x + s * 0.05, y, x - s * 0.01, y + s * 0.50)
    elif k == 1:    # be: sığ kâse + alt nokta
        pa.moveTo(x - s * 0.52, y - s * 0.02)
        pa.quadTo(x - s * 0.34, y + s * 0.22, x, y + s * 0.20)
        pa.quadTo(x + s * 0.36, y + s * 0.18, x + s * 0.50, y - s * 0.26)
        dots.append((x - s * 0.02, y + s * 0.44))
    elif k == 2:    # lam: dik gövde + sola kıvrık kuyruk
        pa.moveTo(x + s * 0.14, y - s * 0.52)
        pa.lineTo(x + s * 0.14, y + s * 0.14)
        pa.quadTo(x + s * 0.14, y + s * 0.44, x - s * 0.36, y + s * 0.32)
    elif k == 3:    # mim: küçük halka + inen kuyruk
        pa.addCircle(x, y - s * 0.10, s * 0.17)
        pa.moveTo(x + s * 0.17, y - s * 0.08)
        pa.quadTo(x + s * 0.12, y + s * 0.30, x + s * 0.02, y + s * 0.52)
    elif k == 4:    # nun: derin kâse + üst nokta
        pa.moveTo(x - s * 0.44, y - s * 0.12)
        pa.quadTo(x - s * 0.40, y + s * 0.36, x, y + s * 0.36)
        pa.quadTo(x + s * 0.42, y + s * 0.34, x + s * 0.44, y - s * 0.22)
        dots.append((x + s * 0.0, y - s * 0.30))
    elif k == 5:    # dal: açık kanca
        pa.moveTo(x - s * 0.40, y - s * 0.18)
        pa.quadTo(x + s * 0.32, y - s * 0.22, x + s * 0.30, y + s * 0.12)
        pa.quadTo(x + s * 0.28, y + s * 0.34, x + s * 0.02, y + s * 0.40)
    elif k == 6:    # ha: çift halka
        pa.addOval(skia.Rect.MakeLTRB(x - s * 0.20, y - s * 0.30, x + s * 0.20, y + s * 0.02))
        pa.addOval(skia.Rect.MakeLTRB(x - s * 0.12, y + s * 0.06, x + s * 0.12, y + s * 0.28))
    else:           # ye: kuyruk geriye + iki alt nokta
        pa.moveTo(x - s * 0.55, y + s * 0.10)
        pa.quadTo(x - s * 0.10, y + s * 0.34, x + s * 0.22, y + s * 0.20)
        pa.quadTo(x + s * 0.44, y + s * 0.10, x + s * 0.40, y - s * 0.30)
        dots += [(x - s * 0.10, y + s * 0.50), (x + s * 0.10, y + s * 0.50)]
    return pa, dots


def arab_glyph(c, kind, x, y, s, col="#0E0A06", a=255, w=None):
    w = w or s * 0.12
    pa, dots = glyph_path(kind, x, y, s)
    c.drawPath(pa, S(col, w, a))
    for dx, dy in dots:
        c.drawCircle(dx, dy, w * 0.62, skia.Paint(AntiAlias=True, Color=C(col, a)))


def lead_sort(c, x, y, w=62, h=96, kind=0, a=255, face_on=True):
    """Kurşun harf blok (ön yüz görünür): (x,y) alt orta. Üst yüzde tersine kabartma harf."""
    x0, x1 = x - w / 2, x + w / 2
    sh = skia.GradientShader.MakeLinear([(x0, 0), (x1, 0)], [C("#C4C7CE", a), C("#8A8E98", a), C("#50545E", a)], [0.0, 0.45, 1.0])
    c.drawRoundRect(skia.Rect.MakeLTRB(x0, y - h, x1, y), 4, 4, skia.Paint(AntiAlias=True, Shader=sh))
    c.drawRoundRect(skia.Rect.MakeLTRB(x0, y - h, x1, y), 4, 4, S("#15110C", 1.3, A(0.8 * a)))
    c.drawRect(skia.Rect.MakeLTRB(x0 + 3, y - h + 3, x1 - 3, y - h + 8), P("#E6E8EE", A(0.7 * a)))
    if face_on:
        c.save()
        c.translate(x, y - h * 0.50)
        c.scale(-1, 1)                                   # kalıp harf: ayna
        arab_glyph(c, kind, 0, 0, h * 0.58, "#14100C", A(0.95 * a), w=h * 0.075)
        c.restore()


def card_pane(f, x0, y0, x1, y1, a=1.0, col="#EFE5CC"):
    """Küçük krem kâğıt/levha (gölgeli)."""
    f.rrect(x0 + 4, y0 + 8, x1 - x0, y1 - y0, 6, color="#000000", alpha=0.28 * a, blur=8)
    f.rrect(x0, y0, x1 - x0, y1 - y0, 6, shader=f.lin(x0, y0, x0, y1, [(mix(col, "#FFFFFF", 0.35), 0.0), (col, 1.0)]), alpha=a)
    f.rrect(x0, y0, x1 - x0, y1 - y0, 6, style="stroke", sw=1.6, color="#7A5C32", alpha=0.8 * a)


# ═══════════════════════════ baskı presi ═══════════════════════════
def draw_press(c, x, y, s=1.0, k_down=0.0, bar=0.0, a=255, palle=True):
    """Ahşap vidalı pres (yan görünüm). (x,y) taban orta. k_down: tabla inişi 0..1; bar: kol evresi (açı, rad). Dönüş: tabla üstü y."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    wood = ["#9A6A3C", "#6B4424"]
    ink = S("#1E1008", 2.4, A(0.92 * a), cap=False)
    # ayaklar + gövde
    for dx in (-132, 112):
        sh = skia.GradientShader.MakeLinear([(dx, 0), (dx + 34, 0)], [C(wood[0], a), C(wood[1], a)], [0, 1])
        c.drawRect(skia.Rect.MakeLTRB(dx, -560, dx + 34, 0), skia.Paint(Shader=sh))
        c.drawRect(skia.Rect.MakeLTRB(dx, -560, dx + 34, 0), ink)
    # alt kiriş (yatak) ve üst kiriş
    c.drawRect(skia.Rect.MakeLTRB(-170, -118, 180, -78), P("#5A3818", a))
    c.drawRect(skia.Rect.MakeLTRB(-170, -118, 180, -78), ink)
    sh2 = skia.GradientShader.MakeLinear([(0, -586), (0, -520)], [C("#A8774A", a), C("#6B4424", a)], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(-172, -586, 184, -520), skia.Paint(Shader=sh2))
    c.drawRect(skia.Rect.MakeLTRB(-172, -586, 184, -520), ink)
    # vida (mil) — tabla ile birlikte iner
    y_pl = -330 + 164 * k_down                                  # tabla üst y
    c.drawRect(skia.Rect.MakeLTRB(-14, -640, 14, y_pl), P("#6A6E78", a))
    c.drawRect(skia.Rect.MakeLTRB(-14, -640, 14, y_pl), S("#15110C", 1.6, A(0.8 * a), cap=False))
    for i in range(12):
        yy = -630 + i * 26 + (k_down * 82) % 26
        if yy < y_pl:
            c.drawLine(-14, yy, 14, yy + 9, S("#2A2C32", 2.0, A(0.8 * a)))
    # kol (bar): dikey eksende döner → yatay izdüşüm cos
    ang = bar
    xe = math.cos(ang) * 230
    ye = -640 + math.sin(ang) * 16
    c.drawLine(-xe, -640 - math.sin(ang) * 16, xe, ye, S("#4A2E14", 18, a))
    c.drawLine(-xe, -640 - math.sin(ang) * 16, xe, ye, S("#9A6A3C", 8, a))
    for sx_, sy_ in ((-xe, -640 - math.sin(ang) * 16), (xe, ye)):
        c.drawCircle(sx_, sy_, 17, P("#3A3C44", a))
        c.drawCircle(sx_, sy_, 17, S("#15110C", 1.6, A(0.8 * a)))
    # tabla
    sh3 = skia.GradientShader.MakeLinear([(0, y_pl), (0, y_pl + 34)], [C("#B0804E", a), C("#6B4424", a)], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(-96, y_pl, 98, y_pl + 34), skia.Paint(Shader=sh3))
    c.drawRect(skia.Rect.MakeLTRB(-96, y_pl, 98, y_pl + 34), ink)
    c.restore()
    return y + (y_pl + 34) * s


def palle_mark(c, x, y, s, a=255, col="#7A2018"):
    for (dx, dy, rr) in CM.PALLE_POS:
        px, py = x + (dx - 0.5) * s * 0.78, y + (dy - 0.52) * s * 0.78
        c.drawCircle(px, py, rr * s * 0.78, P(col, a))


def type_forme(c, x, y, w=250, a=255, nlines=3, ink_k=0.0, seed=2):
    """Tabla altındaki dizgi çerçevesi (forme): koyu kasa + sıralı stilize harfler."""
    c.drawRoundRect(skia.Rect.MakeLTRB(x - w / 2 - 14, y - 40, x + w / 2 + 14, y + 8), 5, 5, P("#3A2410", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - w / 2 - 14, y - 40, x + w / 2 + 14, y + 8), 5, 5, S("#15110C", 1.6, A(0.8 * a)))
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, y - 34, x + w / 2, y), P("#6F7480", a))
    rs = np.random.RandomState(seed)
    for r_ in range(nlines):
        yy = y - 26 + r_ * 11
        for i in range(int(w / 15)):
            if rs.rand() > 0.12:
                c.drawRect(skia.Rect.MakeLTRB(x - w / 2 + 3 + i * 15, yy, x - w / 2 + 3 + i * 15 + 10, yy + 7), P("#C9CCD4", A(0.85 * a)))
    if ink_k > 0:
        c.drawRect(skia.Rect.MakeLTRB(x - w / 2, y - 34, x + w / 2, y), P("#0E0A06", A(0.55 * ink_k * a)))


def book_closed(c, x, y, w=210, h=64, col="#8A2E1E", a=255, band="#D8B25A", tilt=0.0):
    """Kapalı kitap (yandan; sırt): (x,y) alt orta."""
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(tilt))
    sh = skia.GradientShader.MakeLinear([(0, -h), (0, 0)], [C(mix(col, "#FFFFFF", 0.22), a), C(col, a), C(mix(col, "#000000", 0.4), a)], [0, 0.5, 1])
    c.drawRoundRect(skia.Rect.MakeLTRB(-w / 2, -h, w / 2, 0), 5, 5, skia.Paint(AntiAlias=True, Shader=sh))
    c.drawRoundRect(skia.Rect.MakeLTRB(-w / 2, -h, w / 2, 0), 5, 5, S("#1E1008", 2.0, A(0.9 * a)))
    c.drawRect(skia.Rect.MakeLTRB(-w / 2 + 6, -h + 3, w / 2 - 6, -h + 7), P("#F2E8CC", A(0.9 * a)))
    c.drawRect(skia.Rect.MakeLTRB(-w / 2 + 6, -7, w / 2 - 6, -3), P("#F2E8CC", A(0.9 * a)))
    for fx in (-w * 0.32, -w * 0.30, w * 0.30, w * 0.32):
        c.drawLine(fx, -h + 8, fx, -8, S(band, 2.0, A(0.85 * a)))
    c.drawRect(skia.Rect.MakeLTRB(-w * 0.22, -h * 0.62, w * 0.22, -h * 0.38), P(band, A(0.8 * a)))
    c.restore()


# ═══════════════════════════ c14_baski: matbaa atölyesi + pres + kitaplar ═══════════════════════════
@CM.ckind("c14_baski")
def k_baski(cx, thumps=(), books=(), seed=3, ovl=None, workers=True, **_):
    """Matbaa atölyesi (geniş) ya da pres yakını: pres koluna her `thumps` çapasında çekilir (tabla iner, forme basılır), her `books` öğesi
    (dict(at, col, tag)) baskı atmasıyla sağdaki rafa/yığına eklenir. Pencere ışığı + toz + dizgi dolabı + siluet çalışan."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    wood_floor(c, 800, seed=seed)
    # pencere + ışık huzmesi
    c.drawRect(skia.Rect.MakeLTRB(130, 120, 400, 560), P("#1E1008"))
    c.drawRect(skia.Rect.MakeLTRB(144, 134, 386, 546), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 134), (0, 546)], [C("#CFE0EC"), C("#F2E6C4")], [0, 1])))
    for yy in (270, 410):
        c.drawLine(144, yy, 386, yy, S("#3A2410", 7))
    c.drawLine(265, 134, 265, 546, S("#3A2410", 7))
    c.drawRect(skia.Rect.MakeLTRB(130, 120, 400, 560), S("#1E1008", 5, 255, cap=False))
    shaft = sk.poly_path([(144, 134), (386, 134), (1010, 830), (560, 830)])
    c.drawPath(shaft, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(260, 140), (780, 830)], [C("#FFF3C4", 70), C("#FFF3C4", 14)], [0, 1])))
    # dizgi dolabı (sol) + sıralı gözler
    cx0, cy0 = 520, 800
    c.drawPath(sk.poly_path([(cx0 - 190, cy0 - 330), (cx0 + 190, cy0 - 300), (cx0 + 190, cy0 - 140), (cx0 - 190, cy0 - 170)]), P("#5E3C1E"))
    c.drawPath(sk.poly_path([(cx0 - 190, cy0 - 330), (cx0 + 190, cy0 - 300), (cx0 + 190, cy0 - 140), (cx0 - 190, cy0 - 170)]), S("#1E1008", 2.4))
    for i in range(8):
        for j in range(3):
            xa = cx0 - 178 + i * 46
            ya = cy0 - 318 + j * 52 + i * 4
            c.drawRect(skia.Rect.MakeLTRB(xa, ya, xa + 40, ya + 44), P("#3A2410"))
            c.drawRect(skia.Rect.MakeLTRB(xa + 3, ya + 6, xa + 37, ya + 40), P("#1E1209"))
            if (i + j) % 2 == 0:
                lead_sort(c, xa + 20, ya + 42, w=14, h=30, kind=i + j * 3, a=230, face_on=False)
    for dx in (-170, 170):
        c.drawLine(cx0 + dx, cy0 - 170 + (0 if dx < 0 else 24), cx0 + dx * 0.9, cy0, S("#3A2410", 14))
    # kurutma ipi: asılı baskı tabakaları (hafif sallanır)
    c.drawLine(640, 196, 1500, 250, S("#3A2410", 3.0, 230))
    for i in range(8):
        u = (i + 0.5) / 8
        xx = lerp(660, 1480, u)
        yy = lerp(196, 250, u) + 2
        sw = math.sin(t * 1.7 + i * 1.3) * 3.0
        c.save()
        c.translate(xx, yy)
        c.rotate(sw)
        c.drawRect(skia.Rect.MakeLTRB(-23, 0, 23, 70), P("#F3EBD6"))
        c.drawRect(skia.Rect.MakeLTRB(-23, 0, 23, 70), S("#7A5C32", 1.2, 200, cap=False))
        for r_ in range(5):
            c.drawLine(-16, 12 + r_ * 11, 16, 12 + r_ * 11, S("#20160C", 2.2, 170))
        c.restore()
    # mürekkep taşı + tampon (sol-orta)
    c.drawRect(skia.Rect.MakeLTRB(820, 700, 1000, 800), P("#5E3C1E"))
    c.drawRect(skia.Rect.MakeLTRB(820, 700, 1000, 800), S("#1E1008", 2.0, 230, cap=False))
    c.drawRect(skia.Rect.MakeLTRB(810, 688, 1010, 706), P("#7E5430"))
    c.drawOval(skia.Rect.MakeLTRB(850, 668, 960, 696), P("#15100A"))
    for bx_ in (870, 930):
        c.drawCircle(bx_, 664, 14, P("#6B4424"))
        c.drawCircle(bx_, 664, 14, S("#1E1008", 1.6, 220))
    # pres
    ph = [cx.at(a) for a in thumps]
    bar, kd = 0.0, 0.0
    for tp in ph:
        u = (t - tp) / 0.72
        if -0.25 < u < 1.0:
            if u < 0:
                bar = lerp(0.0, 0.5, ease_out(1 + u / 0.25) * 0 + (u + 0.25) / 0.25)
            elif u < 0.38:
                kd = max(kd, ease_in(u / 0.38, 2.2))
                bar = lerp(0.5, 1.45, ease_in(u / 0.38, 2.0))
            else:
                kd = max(kd, 1.0 - ease_out((u - 0.38) / 0.62, 2.0))
                bar = lerp(1.45, 0.0, ease_out((u - 0.38) / 0.62, 2.0))
    px, py_ = 1230, 800
    y_pl = draw_press(c, px, py_, 1.0, k_down=kd, bar=bar)
    palle_mark(c, px + 6, py_ - 553, 46, 235)
    type_forme(c, px, py_ - 92, w=190, a=255, ink_k=1.0 if kd > 0.8 else 0.0)
    # baskı vuruş tozu / titreşim
    for tp in ph:
        uu = t - tp - 0.34
        if 0 < uu < 0.7:
            for i in range(10):
                r3 = np.random.RandomState(900 + i)
                ang = r3.rand() * math.pi
                dd = (30 + 150 * r3.rand()) * ease_out(clamp(uu / 0.7), 2)
                SOFT(c, px + math.cos(ang) * dd * (1 if i % 2 else -1), py_ - 96 - math.sin(ang) * dd * 0.30, 22 + 18 * uu, 14 + 10 * uu, "#D8C49C", 90 * (1 - clamp(uu / 0.7)))
    # kitap yığını (sağ)
    base_y = 800
    bx = 1630
    c.drawRect(skia.Rect.MakeLTRB(bx - 150, base_y - 120, bx + 150, base_y), P("#5E3C1E"))
    c.drawRect(skia.Rect.MakeLTRB(bx - 150, base_y - 120, bx + 150, base_y), S("#1E1008", 2.2, 230, cap=False))
    c.drawRect(skia.Rect.MakeLTRB(bx - 162, base_y - 134, bx + 162, base_y - 118), P("#7E5430"))
    c.drawRect(skia.Rect.MakeLTRB(bx - 162, base_y - 134, bx + 162, base_y - 118), S("#1E1008", 2.2, 230, cap=False))
    for i, b in enumerate(books):
        k = cx.amt(b["at"], 0.55, ease=lambda u: ease_out(u, 3))
        if k <= 0.003:
            continue
        yy = base_y - 134 - i * 70 - (1 - k) * 220
        xx = bx + (1 - k) * -280 + math.sin(i * 2.1) * 6
        book_closed(c, xx, yy, w=236 - i * 10, h=64, col=b.get("col", "#8A2E1E"), a=A(255 * min(1, k * 2)), tilt=(1 - k) * -0.25 + math.sin(i * 1.7) * 0.012)
    # çalışanlar
    if workers:
        FA.actor(f, "banker", 700, 800, 330, t, action="work", mode="lay", period=1.6, seed=5, dir=1)
        FA.actor(f, "tuccar", 1020, 800, 330, t, action="idle", seed=9, dir=-1)
    cam.end(f)
    CM.finish(f, cx, motes_n=26, light=None, vig_s=0.4)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c14_harf: punç oyma + dizgi (sağdan sola) ═══════════════════════════
def _trim(path, k):
    pm = skia.PathMeasure(path, False)
    out = skia.Path()
    pm.getSegment(0, pm.getLength() * clamp(k), out, True)
    return out, pm


def _graver(c, x, y, ang=-38.0, a=255, press=0.0):
    """Oyma kalemi (burin): uç (x,y); gövde sağ-alta uzanır, ahşap saplı."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.drawRoundRect(skia.Rect.MakeLTRB(0, -7, 300, 7), 5, 5, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -7), (0, 7)], [C("#E8EAF0", a), C("#7C808A", a), C("#3C4048", a)], [0, 0.5, 1])))
    c.drawPath(sk.poly_path([(0, 0), (34, -7), (34, 7)]), P("#D8DAE0", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(300, -21, 470, 21), 21, 21, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -21), (0, 21)], [C("#B88A5A", a), C("#6B4424", a)], [0, 1])))
    c.drawRoundRect(skia.Rect.MakeLTRB(300, -21, 470, 21), 21, 21, S("#1E1008", 2.0, A(0.9 * a)))
    c.drawRect(skia.Rect.MakeLTRB(292, -10, 306, 10), P("#C9A24A", a))
    c.restore()


@CM.ckind("c14_harf")
def k_harf(cx, cut_at=0.4, cut_dur=1.6, set_at=2.0, set_dt=0.26, n=9, glyph=2, seed=4, ovl=None, **_):
    """Granjon'un punç oyması (çelik yüzde harf oluğu açılır, kıvılcım) → matris/hazır harfler → dizgi tabancı: kurşun harfler SAĞDAN SOLA dizilir.
    Dünya: punç (x≈620) · hazır harf yığını + matris (x≈1250) · dizgi çerçevesi (x≈2050–2750). Kamera `cam=[…look…]` ile soldan sağa."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    wood_floor(c, 760, seed=seed)
    # ── istasyon 1: punç + mengene
    px, py = 620.0, 470.0
    SOFT(c, px, 790, 330, 36, "#000000", 120)
    c.drawRect(skia.Rect.MakeLTRB(px - 250, 640, px + 250, 770), P("#4A2E16"))
    c.drawRect(skia.Rect.MakeLTRB(px - 250, 640, px + 250, 770), S("#1E1008", 2.2, 230, cap=False))
    for jx in (-1, 1):                                     # mengene çeneleri
        metal_rect(c, px + jx * 168 - 34, 290, px + jx * 168 + 34, 660, "#3A3C44", r=6)
    metal_rect(c, px - 140, 330, px + 140, 650, "#8E94A0", r=8)      # punç gövdesi (çelik)
    c.drawRect(skia.Rect.MakeLTRB(px - 122, 348, px + 122, 632), skia.Paint(Shader=skia.GradientShader.MakeLinear([(px - 122, 348), (px + 122, 632)], [C("#B8BEC8"), C("#7C838F"), C("#59606C")], [0, 0.5, 1])))
    gp_, gd_ = glyph_path(glyph, px, py + 12, 216)
    k = clamp((t - cx.at(cut_at)) / cut_dur)
    part, pm = _trim(gp_, ease_io(k, 2.0))
    c.drawPath(part, S("#14161C", 15, 255))                    # oyuk (derin)
    c.drawPath(part, S("#E8ECF4", 3.0, 140))                   # oluk yan parıltısı
    if k >= 1.0:
        for dx, dy in gd_:
            c.drawCircle(dx, dy, 10, P("#14161C"))
    tip = None
    if 0 < k < 1:
        pos, tan = pm.getPosTan(pm.getLength() * ease_io(k, 2.0))
        tip = (pos.x(), pos.y())
    elif k >= 1.0:
        tip = (px + 150, py + 210)
    if tip:
        _graver(c, tip[0], tip[1], ang=-34.0 + 4 * math.sin(t * 9.0))
        if 0 < k < 1:
            rs = np.random.RandomState(int(t * 24) % 97)
            for i in range(7):
                a_ = rs.rand() * 6.28
                d_ = rs.rand() * 34
                c.drawCircle(tip[0] + math.cos(a_) * d_, tip[1] + math.sin(a_) * d_ * 0.7 - 6, 1.8 + rs.rand() * 1.4, P("#FFF2C8", A(120 + 100 * rs.rand())))
    # ── istasyon 2: matris + hazır harf yığını (statik, panoramada geçilir)
    mx = 1250.0
    SOFT(c, mx, 790, 280, 30, "#000000", 110)
    c.drawRect(skia.Rect.MakeLTRB(mx - 190, 700, mx + 190, 770), P("#4A2E16"))
    c.drawRect(skia.Rect.MakeLTRB(mx - 190, 700, mx + 190, 770), S("#1E1008", 2.2, 230, cap=False))
    metal_rect(c, mx - 110, 540, mx + 10, 700, "#B8723C", r=6)                      # bakır matris
    c.save()
    c.translate(mx - 50, 622)
    c.scale(-1, 1)
    arab_glyph(c, glyph, 0, 0, 110, "#3A1E0C", 220, w=11)
    c.restore()
    for i in range(6):
        lead_sort(c, mx + 70 + (i % 3) * 52, 700 - (i // 3) * 98, w=44, h=90, kind=glyph + i, a=255)
    # ── istasyon 3: dizgi çerçevesi (stick)
    sx0, sx1, sy = 2020.0, 2800.0, 760.0
    SOFT(c, (sx0 + sx1) / 2, 790, 460, 34, "#000000", 120)
    metal_rect(c, sx0, sy - 22, sx1, sy + 8, "#7F8590", r=3)
    metal_rect(c, sx0, sy - 150, sx1, sy - 22, "#5A606C", r=3, horiz=False)
    c.drawRect(skia.Rect.MakeLTRB(sx0, sy - 150, sx1, sy - 142), P("#C9CEDA", 170))
    metal_rect(c, sx0 - 26, sy - 190, sx0 + 4, sy + 8, "#8E94A0", r=4)                 # sol sabit dayanak
    metal_rect(c, sx1 - 4, sy - 190, sx1 + 26, sy + 8, "#8E94A0", r=4)                 # sağ dayanak
    pitch = 70.0
    for i in range(n):
        ti = cx.at(set_at) + i * set_dt
        u = (t - ti) / 0.42
        xi = sx1 - 44 - i * pitch
        if u < 0:
            continue
        if u < 1:
            e = ease_out(u, 2.2)
            xx = lerp(xi + 300, xi, e)
            yy = sy - 8 - 380 * (1 - e) ** 2
            # cımbız
            c.drawLine(xx + 120, yy - 330, xx + 10, yy - 98, S("#2A2C32", 5, 230))
            c.drawLine(xx + 150, yy - 330, xx + 24, yy - 98, S("#2A2C32", 5, 230))
            lead_sort(c, xx, yy, w=60, h=96, kind=glyph + i * 3 + 1, a=255)
        else:
            bob = 3.5 * math.exp(-(u - 1) * 6) * math.sin((u - 1) * 40) if u < 1.6 else 0.0
            lead_sort(c, xi, sy - 8 + bob, w=60, h=96, kind=glyph + i * 3 + 1, a=255)
            if u < 1.5:                                                  # tık halkası
                k2 = (u - 1) / 0.5
                c.drawCircle(xi, sy - 4, 12 + 40 * k2, S("#FFF2C8", 2.2, A(150 * (1 - k2))))
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None, vig_s=0.42)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ yazı satırı (stilize Arapça/Fars yazı hissi) ═══════════════════════════
def script_line(c, x0, x1, y, k, size=30, seed=0, col="#1A120A", a=210):
    """Sağdan sola akan stilize yazı satırı (x1 → x0, k oranında yazılmış): ortak taban çizgisi + harf gövdeleri/noktalar. Okunur metin DEĞİL."""
    if k <= 0.003:
        return (x1, y)
    rs = np.random.RandomState(seed)
    xe = x1 - (x1 - x0) * k
    x = x1
    p = S(col, size * 0.11, a)
    base = skia.Path()
    base.moveTo(x1, y)
    while x > xe:
        wd = size * (0.55 + rs.rand() * 0.55)
        x2 = max(xe, x - wd)
        kind = int(rs.randint(0, 8))
        base.lineTo(x2 + wd * 0.2, y + rs.randn() * 0.8)
        pa, dots = glyph_path(kind, (x + x2) / 2, y - size * 0.1, size * 0.9)
        c.drawPath(pa, p)
        for dx, dy in dots:
            c.drawCircle(dx, dy, size * 0.07, skia.Paint(AntiAlias=True, Color=C(col, a)))
        x = x2 - size * 0.12
        if rs.rand() < 0.18:
            x -= size * 0.5
    c.drawPath(base, S(col, size * 0.07, A(a * 0.8)))
    return (xe, y)


def seal_ring(c, x, y, r, col="#7A1E16", a=255, seed=3, t=1.0):
    """Daire mühür: halkalar + stilize yıldız-rozet + kenar noktaları (resmî mühür temsili; yazı yok)."""
    sc = 1.0 + (1 - sk.back_out(clamp(t))) * 0.5 if t < 1 else 1.0
    if t <= 0:
        return
    c.save()
    c.translate(x, y)
    c.scale(sc, sc)
    c.drawCircle(3, 5, r * 1.04, P("#000000", A(70 * a / 255)))
    c.drawCircle(0, 0, r, S(col, 5.5, a))
    c.drawCircle(0, 0, r * 0.82, S(col, 2.2, a))
    for i in range(24):
        an = i * math.tau / 24 if hasattr(math, "tau") else i * 2 * math.pi / 24
        c.drawCircle(math.cos(an) * r * 0.91, math.sin(an) * r * 0.91, 2.4, P(col, a))
    pts = []
    for i in range(16):
        rr = r * (0.62 if i % 2 == 0 else 0.30)
        an = -math.pi / 2 + i * math.pi / 8
        pts.append((math.cos(an) * rr, math.sin(an) * rr))
    c.drawPath(sk.poly_path(pts), P(col, A(0.82 * a)))
    c.drawCircle(0, 0, r * 0.14, P("#F3E8CC", A(0.9 * a)))
    c.restore()


import functools


@functools.lru_cache(maxsize=8)
def _script_layer(w, h, nlines, size, seed, pad=40):
    """Önceden pişirilmiş stilize yazı katmanı (şeffaf): satırlar w×h içinde, üstten başlar. Dönüş: (image, [satır y'leri])."""
    sf = skia.Surface(int(w), int(h))
    cc = sf.getCanvas()
    cc.clear(skia.ColorTRANSPARENT)
    ys = []
    for i in range(nlines):
        y = pad + i * (size * 1.7)
        ys.append(y)
        script_line(cc, pad, w - pad, y, 1.0, size=size, seed=seed + i)
    return sf.makeImageSnapshot(), ys


def draw_script_reveal(c, x, y, w, h, ks, size=30, seed=40, nlines=None, pad=40):
    """Satırlar sağdan sola yazılır (ks[i] 0..1); katman önbellekli."""
    nlines = nlines or len(ks)
    img, ys = _script_layer(int(w), int(h), nlines, size, seed, pad)
    p = skia.Paint(AntiAlias=True)
    for i, k in enumerate(ks):
        if k <= 0.003:
            continue
        xr = w - pad * 0.5
        xl = xr - (w - pad) * k
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(x + xl, y + ys[i] - size * 1.0, x + xr, y + ys[i] + size * 0.9))
        c.drawImage(img, x, y, skia.SamplingOptions(skia.FilterMode.kLinear), p)
        c.restore()


# ═══════════════════════════ c14_ferman: İstanbul fermanı — yasak değil, koruma ═══════════════════════════
@CM.ckind("c14_ferman")
def k_ferman(cx, unroll_at=0.2, seal_at=1.4, men_at=2.2, shield_at=4.6, no_at=5.8, ok_at=6.6, seed=5, ovl=None, **_):
    """Fermanın tomarı açılır (stilize yazı satırları satır satır yazılır, daire mühür basılır); iki Avrupalı tüccar kitap denkleriyle yürüyüp gelir,
    koruma kalkanı üstlerine açılır; «YASAK» damgası çizilir ve «KORUMA» damgası çakılır (sözcükler script'ten)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    wood_floor(c, 880, seed=seed)
    # tomar
    pw, ph = 860, 560
    pcx, pcy = 700.0, 420.0
    pp = PP.paper_image(pw, ph, seed, (236, 226, 196), "deckle", (("h", 0.5),), 44, 1.1)
    k_un = ease_out(clamp((t - cx.at(unroll_at)) / 1.3), 2.4)
    vis = max(8.0, pw * k_un)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(pcx - pw / 2 - 60, 0, pcx - pw / 2 + vis, H))
    pp.draw(f, pcx, pcy, rot=-0.012, scale=1.0, alpha=1.0, shadow=0.6)
    # satırlar (sağdan sola yazılır; katman önbellekli)
    draw_script_reveal(c, pcx - pw / 2, pcy - ph / 2 + 70, pw, ph - 90, [clamp((t - cx.at(unroll_at) - 0.5 - i * 0.22) / 0.6) for i in range(8)], size=30, seed=40, nlines=8, pad=60)
    # üst süs (stilize tuğra benzeri kıvrım; resmî tuğra iddiası yok)
    ka = clamp((t - cx.at(unroll_at) - 0.3) / 0.8)
    if ka > 0:
        c.save()
        c.translate(pcx + 60, pcy - 222)
        c.scale(1.0, 1.0)
        pth = skia.Path()
        pth.moveTo(-200, 20)
        pth.cubicTo(-140, -60, -60, 30, 0, -10)
        pth.cubicTo(60, -50, 140, 30, 210, 10)
        for xx in (-80, 0, 80):
            pth.moveTo(xx, 24)
            pth.lineTo(xx + 4, -62)
        pm = skia.PathMeasure(pth, False)
        seg = skia.Path()
        pm.getSegment(0, pm.getLength() * ka, seg, True)
        c.drawPath(seg, S("#7A1E16", 7, A(210)))
        c.restore()
    c.restore()
    # tomar ucu (silindir)
    ex = pcx - pw / 2 + vis
    if k_un < 0.999:
        c.drawRoundRect(skia.Rect.MakeLTRB(ex - 8, pcy - ph / 2 - 8, ex + 44, pcy + ph / 2 + 8), 22, 22,
                        skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(ex - 8, 0), (ex + 44, 0)], [C("#B49A66"), C("#EADFC0"), C("#8A7344")], [0, 0.45, 1])))
        c.drawRoundRect(skia.Rect.MakeLTRB(ex - 8, pcy - ph / 2 - 8, ex + 44, pcy + ph / 2 + 8), 22, 22, S("#3A2A12", 2.0, 220))
    seal_ring(c, pcx + pw / 2 - 150, pcy + ph / 2 - 110, 62, "#8A1E16", 235, t=clamp((t - cx.at(seal_at)) / 0.4))
    # tüccarlar
    tm = cx.at(men_at)
    stand = {0: 1330.0, 1: 1560.0}
    for j, (xe, sd) in enumerate(((1330.0, 11), (1570.0, 14))):
        dur_w = 2.6
        u = clamp((t - tm - j * 0.45) / dur_w)
        xx = lerp(2160.0 + 160 * j, xe, ease_out(u, 1.5))
        walking = 0.0 < (t - tm - j * 0.45) < dur_w
        FA.walker(f, "tuccar", xx, 880, 330, t, speed=(190.0 if walking else 0.0), dir=-1, seed=sd, prop="sack", phase=0.1 * j)
    # koruma kalkanı (altın yarım küre) + kalkan simgesi
    ks = cx.amt(shield_at, 0.7)
    if ks > 0.003:
        rr = 330 * (0.6 + 0.4 * ease_out(ks))
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(1050, 300, 1900, 900))
        c.drawCircle(1450, 880, rr, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((1450, 880), rr, [C("#F6DE90", 0), C("#F6DE90", A(70 * ks)), C("#D8B25A", A(210 * ks))], [0.0, 0.8, 1.0])))
        c.drawCircle(1450, 880, rr, S("#B88A2E", 5, A(220 * ks)))
        c.restore()
        icons.draw_icon(f, "shield", 1450, 520 + (1 - ks) * -40, size=160, metal="gold", alpha=ks)
    # YASAK çizilir, KORUMA çakılır
    kn = cx.amt(no_at, 0.3)
    if kn > 0:
        CM.stamp(f, "YASAK", 1420, 250, rot=-0.07, size=70, color="#A8321E", alpha=1.0 - 0.45 * cx.amt(ok_at, 0.4), t=kn)
        ks2 = ease_out(clamp((t - cx.at(no_at) - 0.25) / 0.35), 2)
        if ks2 > 0:
            c.drawLine(1290, 262, 1290 + 260 * ks2, 232 - 4, S("#1A0F08", 9, 235))
    ko = cx.amt(ok_at, 0.3)
    if ko > 0:
        CM.stamp(f, "KORUMA", 1590, 372, rot=0.06, size=78, color="#2E6A46", alpha=1.0, t=ko)
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None, vig_s=0.42)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ küçük çizimler: büst siluet, levha ═══════════════════════════
def bust(c, x, y, s=1.0, hat="cap", col="#1C1209", rim="#E0A860", a=255):
    """Yüzsüz büst silueti: baş + başlık + omuz (kenar ışığıyla). (x,y) boyun tabanı orta."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for off, cc in ((2.5, rim), (0.0, col)):
        c.save()
        c.translate(off, -off * 0.5)
        pa = skia.Path()
        pa.moveTo(-150, 0)
        pa.cubicTo(-150, -70, -90, -90, -34, -100)
        pa.lineTo(34, -100)
        pa.cubicTo(90, -90, 150, -70, 150, 0)
        pa.close()
        c.drawPath(pa, P(cc, a))
        c.drawRoundRect(skia.Rect.MakeLTRB(-24, -150, 24, -90), 14, 14, P(cc, a))          # boyun
        c.drawOval(skia.Rect.MakeLTRB(-52, -262, 52, -128), P(cc, a))                          # baş
        if hat == "cap":
            c.drawOval(skia.Rect.MakeLTRB(-60, -282, 60, -206), P(cc, a))
            c.drawRect(skia.Rect.MakeLTRB(-62, -226, 62, -210), P(cc, a))
        elif hat == "beret":
            c.drawOval(skia.Rect.MakeLTRB(-82, -292, 66, -214), P(cc, a))
        elif hat == "hood":
            c.drawPath(sk.poly_path([(-66, -190), (-56, -290), (0, -310), (56, -290), (66, -190), (40, -150), (-40, -150)]), P(cc, a))
        c.restore()
    c.restore()


def plate_t(f, x, y, w, h, a=1.0, rot=0.0):
    CM.tablet(f, x - w / 2, y - h / 2, w, h, alpha=a, rot=rot, corner=12)


# ═══════════════════════════ c14_bandini: soyadı göz kırpması ═══════════════════════════
@CM.ckind("c14_bandini")
def k_bandini(cx, a1=0.3, a2=3.0, link_at=5.0, no_at=6.6, seed=4, ovl=None, sub1="TÜCCARLARDAN BİRİ", sub2="GİULİANO'YU VURANLARDAN BİRİ", yr="1478", **_):
    """Sol levha: ferman tüccarı Orazio Bandini; sağ levha: 1478 — aynı soyadı. İki «BANDINI» aynı altın çizgiyle işaretlenir; kesik çizgili bağ uzanır ama KAPANMAZ;
    «KAYIT YOK» damgası (mizah: göz kırpması, kısa ve kesin; zamanlama oynar). Yüz yok: büst silueti."""
    f = cx.f
    cam = CM.Cam(cx, push=0.045, drift=(6.0, 2.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    L_, R_ = (520.0, 560.0), (1400.0, 560.0)
    for (xc, yc), a_t, nm, sub, hat, big in ((L_, a1, "ORAZIO BANDINI", sub1, "cap", None), (R_, a2, "BANDINI", sub2, "beret", yr)):
        k = cx.amt(a_t, 0.6, ease=lambda u: ease_out(u, 3))
        if k <= 0.003:
            continue
        yy = yc + (1 - k) * 40
        plate_t(f, xc, yy - 30, 700, 560, a=k)
        f.circle(xc, yy - 150, 150, shader=f.rad(xc, yy - 150, 150, [("#F7E7B0", 0.0, int(170 * k)), ("#F7E7B0", 1.0, 0)]))
        bust(c, xc, yy - 60, 1.0, hat=hat, a=A(255 * k))
        if big:
            CM.ink(f, big, xc + 232, yy - 238, face="title", size=82, color=TH.acc, align="c", track=4, alpha=k, emboss=False)
        wn = sk.text_width(nm, "title_m", 56 if big is None else 64, 6)
        CM.ink(f, nm, xc, yy + 118, face="title_m", size=56 if big is None else 64, color=TH.fg, align="c", track=6, alpha=k, emboss=False)
        # aynı altın çizgi (soyadı vurgusu)
        kk = cx.amt(a_t, 1.0, off=0.5)
        x_end = xc + wn / 2
        x_beg = x_end - sk.text_width("BANDINI", "title_m", 56 if big is None else 64, 6)
        c.drawLine(x_beg, yy + 134, x_beg + (x_end - x_beg) * kk, yy + 134, S("#D8A63A", 5, A(255 * k)))
        CM.ink(f, sub, xc, yy + 188, face="cap_i", size=34, color=TH.fg2, align="c", alpha=k, emboss=False)
    # bağ: kesik çizgi uzanır ve yarıda kalır
    kl = cx.amt(link_at, 1.2, ease=lambda u: ease_io(u, 2))
    if kl > 0.003:
        x0_, x1_ = L_[0] + 372, R_[0] - 372
        y_ = 560
        reach = x0_ + (x1_ - x0_) * 0.62 * kl
        fade = 1.0 - cx.amt(no_at, 0.5)
        pa = S("#6A4A2A", 6, A(255 * max(fade, 0.35)))
        pa.setPathEffect(skia.DashPathEffect.Make([16, 12], -t * 22))
        c.drawLine(x0_, y_, reach, y_, pa)
        if kl > 0.99:
            c.drawCircle(reach, y_, 7, P("#6A4A2A", A(255 * max(fade, 0.35))))
    kn = cx.amt(no_at, 0.3)
    if kn > 0:
        CM.stamp(f, "KAYIT YOK", 960, 440, rot=-0.07, size=66, color="#A8321E", alpha=1.0, t=kn)
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c14_pietra: sert taş kakma (commesso) ═══════════════════════════
def _petal(cx_, cy_, ang, r0, r1, wd):
    """Yaprak/taçyaprağı çokgeni: merkezden ang yönünde r0..r1, genişlik wd."""
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    n = 10
    for i in range(n + 1):
        u = i / n
        r = lerp(r0, r1, u)
        w = math.sin(u * math.pi) ** 0.85 * wd
        pts.append((cx_ + ca * r - sa * w, cy_ + sa * r + ca * w))
    for i in range(n, -1, -1):
        u = i / n
        r = lerp(r0, r1, u)
        w = math.sin(u * math.pi) ** 0.85 * wd
        pts.append((cx_ + ca * r + sa * w, cy_ + sa * r - ca * w))
    return pts


STONES = dict(lapis=("#1B3A8F", "#4E72C8"), malachite=("#2F7A52", "#7ABF98"), jasper=("#A8361F", "#E27A58"), onyx=("#2A2B30", "#6A6C76"), amber=("#C8892A", "#F2C46A"),
              agate=("#C9A98A", "#F4E4CC"), rose=("#B86A74", "#E8B2B6"))


def _stone_piece(c, pts, kind, a=255, seed=1, rim=True):
    base, hi = STONES[kind]
    pa = sk.poly_path(pts)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    sh = skia.GradientShader.MakeLinear([(min(xs), min(ys)), (max(xs), max(ys))], [C(hi, a), C(base, a), C(mix(base, "#000000", 0.35), a)], [0.0, 0.5, 1.0])
    c.drawPath(pa, skia.Paint(AntiAlias=True, Shader=sh))
    c.save()
    c.clipPath(pa, skia.ClipOp.kIntersect, True)
    rs = np.random.RandomState(seed)
    for i in range(7):                                        # damar (taş deseni)
        x0 = min(xs) + rs.rand() * (max(xs) - min(xs))
        y0 = min(ys) + rs.rand() * (max(ys) - min(ys))
        c.drawLine(x0 - 40, y0 - 20, x0 + 60, y0 + 30 + rs.randn() * 10, S(hi, 2.0 + rs.rand() * 2, A(70 * a / 255)))
    c.restore()
    if rim:
        c.drawPath(pa, S("#0E0C10", 2.0, A(0.85 * a)))


@CM.ckind("c14_pietra")
def k_pietra(cx, start_at=0.4, dt=0.34, polish_at=None, seed=6, ovl=None, **_):
    """Opificio: kara taş zemine renkli sert taş parçalar (lapis, malakit, jasper, oniks, kehribar) tek tek kayarak yerine oturur: çiçek + yapraklar + sap.
    Sonunda cila parıltısı. Atölye tezgâhı: yan tepsi, kalem/eğe. Parça sırası start_at'tan dt aralıkla."""
    f = cx.f
    cam = CM.Cam(cx, push=0.05, drift=(4.0, 2.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    wood_floor(c, 800, seed=seed)
    px, py, pw, ph = 960.0, 470.0, 720.0, 600.0
    # çerçeve + kara taş zemin
    f.rrect(px - pw / 2 + 8, py - ph / 2 + 14, pw, ph, 10, color="#000000", alpha=0.35, blur=14)
    c.drawRoundRect(skia.Rect.MakeLTRB(px - pw / 2 - 26, py - ph / 2 - 26, px + pw / 2 + 26, py + ph / 2 + 26), 12, 12, P("#7A5430"))
    c.drawRoundRect(skia.Rect.MakeLTRB(px - pw / 2 - 26, py - ph / 2 - 26, px + pw / 2 + 26, py + ph / 2 + 26), 12, 12, S("#E8C25A", 3.0, 220))
    c.drawRoundRect(skia.Rect.MakeLTRB(px - pw / 2, py - ph / 2, px + pw / 2, py + ph / 2), 6, 6, skia.Paint(Shader=skia.GradientShader.MakeLinear([(px - pw / 2, py - ph / 2), (px + pw / 2, py + ph / 2)], [C("#2A2B32"), C("#14151A")], [0, 1])))
    ccx, ccy = px, py - 90
    pieces = []
    # sap + yapraklar (malakit)
    stem = [(ccx - 14, ccy + 70), (ccx + 16, ccy + 70), (ccx + 20, ccy + 200), (ccx + 12, ccy + 262), (ccx - 14, ccy + 262), (ccx - 18, ccy + 200)]
    pieces.append((stem, "malachite", (0, 300), 0.0))
    pieces.append((_petal(ccx + 16, ccy + 190, -0.35, 8, 190, 62), "malachite", (320, 120), 0.5))
    pieces.append((_petal(ccx - 14, ccy + 150, math.pi + 0.3, 8, 180, 56), "malachite", (-320, 140), 0.5))
    # taçyaprakları (jasper / lapis / rose)
    for i in range(8):
        ang = i * math.pi / 4 + math.pi / 8
        kind = ("jasper", "lapis")[i % 2]
        pieces.append((_petal(ccx, ccy, ang, 52, 215, 58), kind, (math.cos(ang) * 480, math.sin(ang) * 480 - 80), 0.0))
    pieces.append(([(ccx + math.cos(a_ * math.pi / 8) * 56, ccy + math.sin(a_ * math.pi / 8) * 56) for a_ in range(16)], "amber", (0, -420), 0.0))
    pieces.append(([(ccx + math.cos(a_ * math.pi / 6) * 118, ccy + math.sin(a_ * math.pi / 6) * 118) for a_ in range(12)], "onyx", (0, -520), 0.0))
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11]
    # tepsi: bekleyen parçalar solda
    tray_x, tray_y = 250.0, 760.0
    c.drawRoundRect(skia.Rect.MakeLTRB(tray_x - 170, tray_y - 30, tray_x + 170, tray_y + 36), 8, 8, P("#5E3C1E"))
    c.drawRoundRect(skia.Rect.MakeLTRB(tray_x - 170, tray_y - 30, tray_x + 170, tray_y + 36), 8, 8, S("#1E1008", 2.0, 230))
    for j, kd in enumerate(("lapis", "malachite", "jasper", "onyx", "amber", "agate")):
        _stone_piece(c, [(tray_x - 150 + j * 52 + dx, tray_y - 12 + dy) for dx, dy in ((0, 0), (40, -4), (46, 22), (10, 26))], kd, seed=j)
    # parçalar
    for oi, pi in enumerate(order):
        pts, kind, (ox, oy), _ = pieces[pi]
        ti = cx.at(start_at) + oi * dt
        u = clamp((t - ti) / 0.75)
        if u <= 0:
            continue
        e = ease_out(u, 3.0)
        dx, dy = ox * (1 - e), oy * (1 - e)
        rot = (1 - e) * (0.5 if oi % 2 else -0.5)
        c.save()
        mxp = sum(p[0] for p in pts) / len(pts)
        myp = sum(p[1] for p in pts) / len(pts)
        c.translate(mxp + dx, myp + dy)
        c.rotate(math.degrees(rot))
        c.translate(-mxp, -myp)
        _stone_piece(c, pts, kind, a=A(255 * min(1, u * 3)), seed=pi + 3)
        c.restore()
        if 0.92 < u <= 1.0 or (u >= 1.0 and t - ti < 1.1):
            kk = clamp((t - ti - 0.55) / 0.5)
            if 0 < kk < 1:
                c.drawCircle(mxp, myp, 18 + 36 * kk, S("#FFF2C8", 2.0, A(160 * (1 - kk))))
    # cila: parıltı şeridi
    if polish_at is not None:
        kp = clamp((t - cx.at(polish_at)) / 1.1)
        if 0 < kp < 1:
            xg = lerp(px - pw / 2 - 140, px + pw / 2 + 60, kp)
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(px - pw / 2, py - ph / 2, px + pw / 2, py + ph / 2))
            c.drawPath(sk.poly_path([(xg - 20, py - ph / 2), (xg + 40, py - ph / 2), (xg + 40 - 140, py + ph / 2), (xg - 20 - 140, py + ph / 2)]), P("#FFFFFF", 70))
            c.restore()
    cam.end(f)
    CM.finish(f, cx, motes_n=20, light=None, vig_s=0.42)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ nota sayfaları (c14_nota) ═══════════════════════════
def clef(c, x, y, s=1.0, col="#1A120A", a=255):
    """Stilize sol anahtarı (G)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    p = skia.Path()
    p.moveTo(8, 40)
    p.cubicTo(-30, 18, -22, -26, 4, -34)
    p.cubicTo(30, -40, 36, -6, 10, 4)
    p.cubicTo(-14, 14, -26, 4, -22, -14)
    p.moveTo(6, -66)
    p.lineTo(6, 62)
    p.cubicTo(6, 84, -22, 84, -22, 66)
    c.drawPath(p, S(col, 5.0, a))
    c.drawCircle(-15, 66, 6, P(col, a))
    c.restore()


def staff_page(f, x, y, w=620, h=780, seed=3, notes_k=1.0, ink="#1A120A", a=1.0, scr=2, tone=(238, 228, 198), t=0.0, notes_seed=7, fade=0.0, print_pop=0.0):
    """Nota kâğıdı: 4 sistem × 5 çizgi, anahtar, recitativo notaları (aynı perdede tekrarlar + küçük adımlar). notes_k 0..1 yazılma oranı; fade: notalar solar."""
    c = f.c
    pp = PP.paper_image(int(w), int(h), seed, tone, "deckle", (), 44, 1.0)
    sc = 1.0 + 0.035 * print_pop
    pp.draw(f, x, y, rot=-0.008, scale=sc, alpha=a, shadow=0.6)
    c.save()
    c.translate(x, y)
    c.scale(sc, sc)
    rs = np.random.RandomState(notes_seed)
    nsys = 4
    per = 9
    total = nsys * per
    shown = notes_k * total
    pitch = rs.randint(0, 3, size=total)
    cur = 3
    steps = []
    for i in range(total):
        cur = int(np.clip(cur + rs.choice([-1, 0, 0, 0, 1]), 0, 7))
        steps.append(cur)
    for si in range(nsys):
        y0 = -h / 2 + 150 + si * 164
        for li in range(5):
            c.drawLine(-w / 2 + 70, y0 + li * 14, w / 2 - 54, y0 + li * 14, S(ink, 1.6, A(190 * a)))
        c.drawLine(-w / 2 + 70, y0, -w / 2 + 70, y0 + 56, S(ink, 2.0, A(200 * a)))
        clef(c, -w / 2 + 104, y0 + 30, 0.62, ink, A(230 * a))
        for ni in range(per):
            idx = si * per + ni
            if idx >= shown:
                break
            kk = clamp(shown - idx)
            xn = -w / 2 + 160 + ni * ((w - 240) / per)
            yn = y0 + 56 - steps[idx] * 7.0
            al = A(255 * a * kk * (1.0 - fade))
            c.save()
            c.translate(xn, yn)
            c.scale(0.7 + 0.3 * kk, 0.7 + 0.3 * kk)
            c.rotate(-18)
            c.drawOval(skia.Rect.MakeLTRB(-8, -5.6, 8, 5.6), P(ink, al))
            c.restore()
            c.drawLine(xn + 7, yn - 1, xn + 7, yn - 44, S(ink, 2.2, al))
            if idx % 5 == 2:
                c.drawLine(xn + 7, yn - 44, xn + 17, yn - 33, S(ink, 3.0, al))
    c.restore()


def calendar_leaves(f, x, y, n=6, k=0.0, w=200, h=230):
    """Takvim yaprakları: k 0..1 boyunca n yaprak sırayla çevrilir (haftalar); üstte sayı."""
    c = f.c
    cur = min(n, int(k * n))
    kk = (k * n) % 1.0 if k < 1 else 1.0
    f.rrect(x - w / 2 + 4, y - h / 2 + 8, w, h, 8, color="#000000", alpha=0.3, blur=8)
    f.rrect(x - w / 2, y - h / 2, w, h, 8, shader=f.lin(x, y - h / 2, x, y + h / 2, [("#F6EEDA", 0.0), ("#E6D8B4", 1.0)]))
    f.rrect(x - w / 2, y - h / 2, w, h, 8, style="stroke", sw=2.4, color="#7A5C32")
    f.rrect(x - w / 2, y - h / 2, w, 44, 8, color="#A8321E", alpha=0.9)
    num = str(min(n, cur + (1 if kk > 0.5 or cur >= n else 0)) if k > 0 else 0)
    if k > 0:
        c.save()
        c.translate(x, y + 28)
        sy = abs(math.cos(kk * math.pi)) if (k < 1 and cur < n) else 1.0
        c.scale(1.0, 0.25 + 0.75 * sy)
        CM.ink(f, num, 0, 40, face="title", size=118, color=TH.fg, align="c", track=0, alpha=1.0, emboss=False)
        c.restore()


@CM.ckind("c14_nota")
def k_nota(cx, pages=(), weeks=None, seed=4, ovl=None, **_):
    """İki nota sayfası yan yana. pages=[dict(x, y, at, write=(anchor, dur), print_at, fade_at, title, tone, stamp=(text, anchor, color), seed)].
    weeks=dict(at, dur, x, y): ortada altı yaprak takvim çevrilir («altı hafta»). Basılı sayfa `print_at`'ta tabla vuruşuyla belirir."""
    f = cx.f
    cam = CM.Cam(cx, push=0.04, drift=(5.0, 2.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    for i, pg in enumerate(pages):
        k_in = cx.amt(pg.get("at", 0.0), 0.7, ease=lambda u: ease_out(u, 3))
        if k_in <= 0.003:
            continue
        x, y = pg.get("x", 960), pg.get("y", 500) + (1 - k_in) * 40
        nk = 1.0
        pop = 0.0
        if "write" in pg and pg["write"] is not None:
            wa, wd = pg["write"]
            nk = clamp((t - cx.at(wa)) / wd)
        if "print_at" in pg:
            up = (t - cx.at(pg["print_at"]))
            nk = 1.0 if up >= 0 else 0.0
            pop = math.exp(-max(0.0, up) * 7.0) if up >= 0 else 0.0
        fade = cx.amt(pg["fade_at"], 1.4) if pg.get("fade_at") is not None else 0.0
        staff_page(f, x, y, w=pg.get("w", 620), h=pg.get("h", 780), seed=pg.get("seed", 3 + i * 5), notes_k=nk, a=k_in, t=t, notes_seed=pg.get("nseed", 7 + i), fade=fade, print_pop=pop,
                   tone=pg.get("tone", (238, 228, 198)))
        if pg.get("title"):
            kt = cx.amt(pg.get("title_at", pg.get("at", 0.0)), 0.6, off=0.3)
            wd = sk.text_width(pg["title"], "title_m", 44, 8) + 80
            CM.tablet(f, x - wd / 2, y + pg.get("h", 780) / 2 - 40, wd, 82, alpha=kt, corner=10)
            CM.ink(f, pg["title"], x, y + pg.get("h", 780) / 2 + 18, face="title_m", size=44, color=TH.fg, align="c", track=8, alpha=kt, emboss=False)
        if pg.get("stamp"):
            tx, ta, tc = pg["stamp"]
            ks = cx.amt(ta, 0.3)
            if ks > 0:
                CM.stamp(f, tx, x - 10, y - 20, rot=-0.10, size=60, color=tc, alpha=1.0, t=ks)
    if weeks:
        kw = clamp((t - cx.at(weeks["at"])) / weeks.get("dur", 3.0))
        ka = cx.amt(weeks["at"], 0.4)
        if ka > 0:
            calendar_leaves(f, weeks.get("x", 960), weeks.get("y", 500), 6, kw if ka > 0.4 else 0.0)
    cam.end(f)
    CM.finish(f, cx, motes_n=24, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c14_baba_oglu: lavta ↔ teleskop ═══════════════════════════
def draw_lute(c, x, y, s=1.0, ang=-32.0, t=0.0, a=255, vib=1.0):
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    body = skia.Path()
    body.moveTo(0, 190)
    body.cubicTo(-150, 170, -170, -20, -30, -70)
    body.cubicTo(20, -88, 100, -60, 140, 20)
    body.cubicTo(180, 130, 90, 200, 0, 190)
    c.drawPath(body, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-120, -60), (140, 200)], [C("#D9A765", a), C("#A8703A", a), C("#6B4424", a)], [0, 0.55, 1])))
    c.drawPath(body, S("#2A1608", 3.0, A(0.9 * a)))
    for i in range(7):                                                   # dilimler
        c.drawLine(-20 + i * 12, -64, -92 + i * 28, 186, S("#6B4424", 1.4, A(120 * a / 255)))
    c.drawCircle(18, 58, 44, P("#2A1608", a))
    c.drawCircle(18, 58, 52, S("#E8C25A", 3, a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-16, -430, 52, -60), 6, 6, P("#4A2E14", a))                    # sap
    c.drawPath(sk.poly_path([(-16, -430), (52, -430), (74, -520), (-6, -540)]), P("#4A2E14", a))      # kafa (geri kıvrık)
    for i in range(3):
        c.drawLine(-8 - 14, -460 - i * 26, -8 + 28 + 14, -460 - i * 26, S("#D8B25A", 4, a))
    for j, off in enumerate((-9, -3, 3, 9)):                             # teller (titreşir)
        pa = skia.Path()
        pa.moveTo(18 + off, -420)
        for u in range(1, 13):
            yy = -420 + u * 41
            pa.lineTo(18 + off + vib * math.sin(t * 38 + j + u * 0.7) * (1.8 if 3 < u < 10 else 0.5), yy)
        c.drawPath(pa, S("#F4ECD0", 1.6, A(220 * a / 255)))
    c.restore()


def draw_telescope(c, x, y, s=1.0, ang=-38.0, a=255):
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(s, s)
    sh = skia.GradientShader.MakeLinear([(0, -26), (0, 26)], [C("#F2D9A0", a), C("#B88A3A", a), C("#6A4A1A", a)], [0, 0.5, 1])
    c.drawRoundRect(skia.Rect.MakeLTRB(-260, -24, 300, 24), 4, 4, skia.Paint(AntiAlias=True, Shader=sh))
    c.drawRoundRect(skia.Rect.MakeLTRB(-260, -24, 300, 24), 4, 4, S("#2A1608", 3, A(0.9 * a)))
    for bx in (-250, -60, 120, 280):
        c.drawRect(skia.Rect.MakeLTRB(bx - 18, -30, bx + 18, 30), P("#6B3E22", a))
        c.drawRect(skia.Rect.MakeLTRB(bx - 18, -30, bx + 18, 30), S("#1E1008", 2, A(0.9 * a)))
    c.drawRoundRect(skia.Rect.MakeLTRB(300, -32, 342, 32), 6, 6, P("#B88A3A", a))
    c.drawOval(skia.Rect.MakeLTRB(332, -28, 350, 28), P("#8EC4E0", A(0.8 * a)))
    c.drawOval(skia.Rect.MakeLTRB(-268, -14, -250, 14), P("#1A2A3A", a))
    c.restore()


@CM.ckind("c14_baba_oglu")
def k_baba_oglu(cx, a1=0.3, a2=2.2, link_at=3.0, seed=5, ovl=None, **_):
    """İkiye bölünmüş çekim: solda lavta (telleri titreşir, ses halkaları — «konuşur gibi şarkı»), sağda tripodlu teleskop (yıldız parıltısı);
    aralarında ince altın bir bağ çizilir (baba–oğul). Yüz/kişi yok: nesneler. Kamera soldan sağa kayar → bir sonraki çekim gökyüzü."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    k1 = cx.amt(a1, 0.7)
    k2 = cx.amt(a2, 0.7)
    wood_floor(c, 860, seed=seed)
    if k1 > 0.003:
        SOFT(c, 520, 868, 240, 28, "#000000", 110 * k1)
        draw_lute(c, 520, 640 + (1 - k1) * 40, 0.82, -26.0 + 1.5 * math.sin(t * 1.3), t, A(255 * k1))
        for i in range(4):                                       # ses halkaları
            u = (t * 0.55 + i * 0.25) % 1.0
            c.drawCircle(560, 610, 130 + u * 300, S("#B88A2E", 3.0, A(190 * (1 - u) * k1)))
    if k2 > 0.003:
        SOFT(c, 1450, 880, 260, 28, "#000000", 110 * k2)
        c.drawLine(1450, 680, 1330, 878, S("#4A2E14", 12, A(255 * k2)))
        c.drawLine(1450, 680, 1570, 878, S("#4A2E14", 12, A(255 * k2)))
        c.drawLine(1450, 680, 1450, 878, S("#4A2E14", 12, A(255 * k2)))
        draw_telescope(c, 1420, 620 + (1 - k2) * 30, 1.0, -36.0 + math.sin(t * 0.8) * 1.2, A(255 * k2))
        for i, (sx_, sy_) in enumerate(((1810, 240), (1700, 160), (1840, 350), (1620, 300))):
            tw = 0.6 + 0.4 * math.sin(t * 2.0 + i * 1.7)
            cc = k2 * tw
            c.drawCircle(sx_, sy_, 5 + 3 * tw, P("#FFF1B8", A(255 * cc)))
            c.drawLine(sx_ - 16, sy_, sx_ + 16, sy_, S("#FFF1B8", 1.6, A(190 * cc)))
            c.drawLine(sx_, sy_ - 16, sx_, sy_ + 16, S("#FFF1B8", 1.6, A(190 * cc)))
    kl = ease_io(clamp((t - cx.at(link_at)) / 1.5), 2.0)
    if kl > 0.003:
        pa = skia.Path()
        pa.moveTo(560, 430)
        pa.quadTo(960, 250, 1420, 430)
        pm = skia.PathMeasure(pa, False)
        seg = skia.Path()
        pm.getSegment(0, pm.getLength() * kl, seg, True)
        c.drawPath(seg, S("#D8A63A", 6, 240))
        c.drawPath(seg, S("#FFF1B8", 2, 160))
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None, vig_s=0.42)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c14_gok: Galileo'nun mercek görüntüsü ═══════════════════════════
def jupiter(c, x, y, r, t=0.0, a=255):
    """Jüpiter: kuşaklı disk (kuşaklar yavaş kayar), kenar kararması."""
    c.save()
    pa = skia.Path()
    pa.addCircle(x, y, r)
    c.clipPath(pa, skia.ClipOp.kIntersect, True)
    c.drawRect(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), P("#D8B78A", a))
    bands = [(-0.78, 0.10, "#9A6B44"), (-0.52, 0.12, "#C98F5A"), (-0.28, 0.10, "#8A5A38"), (-0.04, 0.16, "#E2C08E"), (0.22, 0.12, "#A06A42"), (0.46, 0.10, "#C98F5A"), (0.70, 0.12, "#8A5A38")]
    for off, wd, col in bands:
        yy = y + off * r
        wv = math.sin(t * 0.4 + off * 5) * r * 0.012
        c.drawRect(skia.Rect.MakeLTRB(x - r, yy - wd * r + wv, x + r, yy + wd * r + wv), P(col, A(0.85 * a)))
    sh = skia.GradientShader.MakeRadial((x - r * 0.35, y - r * 0.35), r * 1.5, [C("#FFFFFF", A(70 * a / 255)), C("#000000", 0), C("#000000", A(170 * a / 255))], [0.0, 0.45, 1.0])
    c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Shader=sh))
    c.restore()
    c.drawCircle(x, y, r, S("#3A2410", 2.2, A(0.9 * a)))


def moon_dot(c, x, y, r=9.0, a=255, glow=1.0):
    c.drawCircle(x, y, r * 3.6, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((x, y), r * 3.6, [C("#FFF3C4", A(120 * glow * a / 255)), C("#FFF3C4", 0)], [0, 1])))
    c.drawCircle(x, y, r, P("#FFF8E0", a))


def starfield(c, t, x0, y0, x1, y1, n=170, seed=3, a=1.0):
    rs = np.random.RandomState(seed)
    for i in range(n):
        x = x0 + rs.rand() * (x1 - x0)
        y = y0 + rs.rand() * (y1 - y0)
        r = 0.8 + rs.rand() * 1.8
        tw = 0.55 + 0.45 * math.sin(t * (0.8 + rs.rand() * 2.2) + i * 1.7)
        c.drawCircle(x, y, r, P("#F4F0E0", A(210 * tw * a)))
        if r > 2.2:
            c.drawLine(x - 7, y, x + 7, y, S("#F4F0E0", 1.1, A(120 * tw * a)))
            c.drawLine(x, y - 7, x, y + 7, S("#F4F0E0", 1.1, A(120 * tw * a)))


MOONS = [(190.0, 5.6, 0.4), (290.0, 9.6, 2.0), (390.0, 15.0, 4.1), (470.0, 26.0, 5.5)]       # yarıçap, periyot, evre (görünür salınım; gerçek yörünge hızı DEĞİL)


def moon_pos(i, t, cxj, cyj, scale=1.0):
    r, T, ph = MOONS[i]
    th = 2 * math.pi * t / T + ph
    return cxj + r * scale * math.sin(th), cyj + 0.05 * r * scale * math.cos(th) + (i - 1.5) * 3.0 * scale, math.cos(th)


@CM.ckind("c14_gok")
def k_gok(cx, view="gok", moons_at=(), jup=(960.0, 540.0), jr=100.0, rows=(), tags=("MEDİCİ", "MARIUS"), drop_at=None, seed=7, ovl=None, count=True, **_):
    """mode='gok': mercek görüntüsü (yıldız tarlası + Jüpiter + uyduların salınımı; uydular moons_at çapalarında belirir; sayı 3→4);
    mode='defter': gözlem defteri (satır satır Jüpiter + nokta çizimleri; rows=[(çapa, [x ofsetleri])]);
    mode='adlar': dört uydu; her birine «MEDİCİ» etiketi asılı, drop_at'ta etiketler düşer, «MARIUS» etiketleri gelir.
    Gecenin havası/ışığı/ay yok (kaynakta yok): düz yıldız tarlası."""
    f = cx.f
    c = f.c
    t = cx.t
    mode_gok = view == "gok"
    if view == "defter":
        cam = CM.Cam(cx, push=0.05, drift=(4.0, 2.0))
        CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
        cam.begin(f)
        pp = PP.paper_image(1240, 800, seed, (238, 228, 198), "deckle", (("v", 0.5),), 44, 1.1)
        pp.draw(f, 960, 520, rot=-0.01, scale=1.0, alpha=1.0, shadow=0.6)
        for i, (an, xs) in enumerate(rows):
            kk = cx.amt(an, 0.6)
            if kk <= 0.003:
                continue
            yy = 236 + i * 128
            xl = 520 + (i % 2) * 0
            c.drawCircle(960, yy, 32, S("#2A1A0E", 4.0, A(255 * kk)))
            c.drawCircle(960, yy, 32, P("#EBD9B0", A(120 * kk)))
            for j, xo in enumerate(xs):
                kd = clamp((kk - j * 0.12) * 1.6)
                c.drawCircle(960 + xo * 1.55, yy, 9.5 * (0.4 + 0.6 * kd), P("#2A1A0E", A(255 * kd)))
            n_ = len(xs)
            CM.ink(f, str(n_), 1500, yy + 26, face="title", size=78, color=TH.acc, align="c", track=0, alpha=kk, emboss=False)
        cam.end(f)
        CM.finish(f, cx, motes_n=22, light=None, vig_s=0.45)
        if ovl is not None:
            ovl(cx)
        return
    # ── gece mercek görüntüsü
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, H)], [C("#04061A"), C("#0C1740"), C("#060A22")], [0, 0.55, 1])))
    st = getattr(cx, "cam_state", None)
    cam = CM.Cam(cx, push=0.06, drift=(0.0, 0.0))
    cam.begin(f)
    starfield(c, t, -200, -150, W + 200, H + 150, n=210, seed=seed)
    jx, jy = jup
    if mode_gok:
        jupiter(c, jx, jy, jr, t)
        nvis = 0
        for i in range(4):
            if i < len(moons_at):
                k = cx.amt(moons_at[i], 0.5)
            else:
                k = 1.0
            if k <= 0.003:
                continue
            nvis += 1 if k > 0.5 else 0
            mx, my, dep = moon_pos(i, t, jx, jy, 1.0)
            if abs(mx - jx) < jr * 0.9 and dep < 0:
                continue                                              # diskin arkasından geçerken gizlen
            moon_dot(c, mx, my, 10.5, A(255 * k), glow=k)
            if k < 1.0:
                c.drawCircle(mx, my, 20 + 60 * (1 - k), S("#FFF3C4", 2.4, A(200 * k)))
    else:                                       # adlar
        jupiter(c, jx, jy, jr * 1.35, t)
        drop = cx.at(drop_at) if drop_at is not None else 1e9
        for i in range(4):
            mx, my, dep = moon_pos(i, t, jx, jy, 1.45)
            if abs(mx - jx) < jr * 1.2 and dep < 0:
                continue
            moon_dot(c, mx, my, 11.0, 255)
            # etiket
            u = t - drop - i * 0.12
            ty = my + 78 + (i % 2) * 40
            if u < 0:
                pre = ("MEDİCİ", "#1F2F78", "#F0D27A")
            else:
                pre = None
            if pre:
                c.drawLine(mx, my + 10, mx, ty - 24, S("#C9B27A", 1.6, 220))
                c.drawRoundRect(skia.Rect.MakeLTRB(mx - 62, ty - 24, mx + 62, ty + 22), 6, 6, P(pre[1], 245))
                c.drawRoundRect(skia.Rect.MakeLTRB(mx - 62, ty - 24, mx + 62, ty + 22), 6, 6, S("#D8B25A", 2.0, 240))
                f.text(tags[0], mx, ty + 8, face="title_m", size=22, color=pre[2], align="c", track=3)
            else:
                g = 2200.0
                ky = ty + 0.5 * g * u * u
                rot = 18 * u * (1 if i % 2 else -1)
                if ky < H + 120:
                    c.save()
                    c.translate(mx + 40 * u * (1 if i % 2 else -1), ky)
                    c.rotate(rot)
                    c.drawRoundRect(skia.Rect.MakeLTRB(-62, -24, 62, 22), 6, 6, P("#1F2F78", 245))
                    c.drawRoundRect(skia.Rect.MakeLTRB(-62, -24, 62, 22), 6, 6, S("#D8B25A", 2.0, 240))
                    f.text(tags[0], 0, 8, face="title_m", size=22, color="#F0D27A", align="c", track=3)
                    c.restore()
                kn = clamp((u - 0.35) / 0.4)
                if kn > 0:
                    c.drawLine(mx, my + 10, mx, ty - 24, S("#C9B27A", 1.6, A(220 * kn)))
                    c.drawRoundRect(skia.Rect.MakeLTRB(mx - 62, ty - 24, mx + 62, ty + 22), 6, 6, P("#EDE2C6", A(250 * kn)))
                    c.drawRoundRect(skia.Rect.MakeLTRB(mx - 62, ty - 24, mx + 62, ty + 22), 6, 6, S("#5A3E1E", 2.0, A(240 * kn)))
                    f.text(tags[1], mx, ty + 8, face="title_m", size=22, color="#2A1A0C", align="c", track=3, alpha=kn)
    cam.end(f)
    # mercek halkası (kamera dışı, ekran uzayı)
    R0 = 505.0
    c.save()
    pr = skia.Path()
    pr.addRect(skia.Rect.MakeLTRB(-10, -10, W + 10, H + 10))
    pr.addCircle(W / 2, H / 2, R0)
    pr.setFillType(skia.PathFillType.kEvenOdd)
    c.drawPath(pr, P("#04050A", 255))
    c.restore()
    c.drawCircle(W / 2, H / 2, R0 + 12, S("#C9962B", 24, 255))
    c.drawCircle(W / 2, H / 2, R0 + 12, S("#F6E2A0", 5, 200))
    c.drawCircle(W / 2, H / 2, R0 - 8, S("#0A0A0E", 6, 230))
    c.drawArc(skia.Rect.MakeLTRB(W / 2 - R0 + 40, H / 2 - R0 + 40, W / 2 + R0 - 40, H / 2 + R0 - 40), 200, 34, False, S("#FFFFFF", 5.0, 70))
    CM.finish(f, cx, motes_n=0, light=None, vig_s=0.35, dust=False)
    if view == "gok" and count:
        n = sum(1 for i in range(4) if (i >= len(moons_at)) or cx.amt(moons_at[i], 0.5) > 0.5)
        if n > 0:
            tl = [cx.at(moons_at[i]) for i in range(len(moons_at))] if moons_at else [0.0]
            tpop = max([x for x in tl if t >= x] or [0.0])
            pop = math.exp(-(t - tpop) * 5.0)
            sp = CM.gilt(str(n), "title", 140, 4.0)
            CM.draw_spr(f, sp, 1620, 330, "c", alpha=1.0, scale=1.0 + 0.18 * pop, glow=0.25)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c14_mektup: iki seçenek, iki sütun ═══════════════════════════
@CM.ckind("c14_mektup")
def k_mektup(cx, hdr_at=0.3, left_at=0.9, right_at=3.0, q_at=5.4, pick_at=7.0, heads=("COSMICA", "MEDICEA"), left_txt="II. COSIMO", seed=6, ovl=None, **_):
    """Sarayın önüne konan iki seçenek: sol sütun «COSMICA» (tek yıldız + II. Cosimo), sağ sütun «MEDICEA» (dört yıldız, dört kardeş).
    Ortada soru işareti; pick_at'ta sağ sütun altın parlar + onay mührü, sol sütun solar (seçimi kimin yaptığı söylenmez: kişi yok)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.05, drift=(4.0, 2.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    pw, ph = 1540, 800
    ka = cx.amt(hdr_at, 0.7)
    pp = PP.paper_image(pw, ph, seed, (238, 228, 198), "deckle", (("v", 0.5),), 44, 1.1)
    pp.draw(f, 960, 520, rot=-0.008, scale=0.96 + 0.04 * ka, alpha=ka, shadow=0.6)
    kp = cx.amt(pick_at, 0.9)
    dimL = 1.0 - 0.58 * kp
    cL, cR = 600.0, 1320.0
    for i, (xc, hd) in enumerate(((cL, heads[0]), (cR, heads[1]))):
        k = cx.amt(hdr_at, 0.8, off=0.3 * i)
        al = k * (dimL if i == 0 else 1.0)
        sp = CM.engraved(hd, "title", 66, 8.0, "#3A2616", 0.7)
        CM.draw_spr(f, sp, xc, 262, "c", alpha=al)
        CM.flourish_rule(f, xc, 296, 420, alpha=0.8 * al, color="#7A5A2E", grow=k)
    c.drawLine(960, 220, 960, 800, S("#7A5A2E", 2.0, A(150 * ka)))
    # sol: tek yıldız
    kl = cx.amt(left_at, 0.7, ease=lambda u: ease_out(u, 3))
    if kl > 0.003:
        icons.draw_icon(f, "star", cL, 520, size=230 * (0.8 + 0.2 * kl), metal="gold", alpha=kl * dimL, glow=0.0)
        wd = sk.text_width(left_txt, "title_m", 46, 6) + 70
        CM.tablet(f, cL - wd / 2, 686, wd, 78, alpha=kl * dimL, corner=10)
        CM.ink(f, left_txt, cL, 740, face="title_m", size=46, color=TH.fg, align="c", track=6, alpha=kl * dimL, emboss=False)
    # sağ: dört yıldız
    for j in range(4):
        kr = cx.amt(right_at, 0.55, ease=lambda u: ease_out(u, 3), off=0.28 * j)
        if kr <= 0.003:
            continue
        xx = cR - 195 + (j % 2) * 390
        yy = 450 + (j // 2) * 210
        icons.draw_icon(f, "star", xx, yy, size=150 * (0.8 + 0.2 * kr), metal="gold", alpha=kr, glow=0.0)
    if kp > 0.003:
        f.circle(cR, 520, 430, shader=f.rad(cR, 520, 430, [("#F7DF8E", 0.0, int(80 * kp)), ("#F7DF8E", 1.0, 0)]))
        seal_ring(c, cR + 250, 700, 70, "#2E6A46", A(235), t=clamp((t - cx.at(pick_at) - 0.3) / 0.4))
    kq = cx.amt(q_at, 0.5)
    if kq > 0.003 and kp < 0.99:
        icons.draw_icon(f, "question", 960, 520, size=140 * (0.8 + 0.2 * kq), metal="gold", alpha=kq * (1 - kp), glow=0.0)
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c14_kapak: Sidereus Nuncius kapak sayfası (kodla yeniden çizim) ═══════════════════════════
@CM.ckind("c14_kapak")
def k_kapak(cx, title_at=0.4, band_at=3.6, seed=8, ovl=None, **_):
    """Kitap kapak sayfası (stilize, kopya değil): çift çerçeve, iri «SIDEREUS NUNCIUS», küçük satır blokları, ortada «MEDICEA SIDERA» bandı
    (band_at'ta altın parlar, yıldızlar bandın çevresinde belirir). Kamera bant üstüne iner."""
    f = cx.f
    cam = CM.Cam(cx, push=0.06, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    pw, ph = 800, 960
    pp = PP.paper_image(pw, ph, seed, (240, 230, 200), "deckle", (), 44, 1.0)
    k0 = cx.amt(0.0, 0.8)
    pp.draw(f, 960, 520, rot=0.0, scale=1.0, alpha=k0, shadow=0.7)
    ka = cx.amt(title_at, 0.9)
    ORN = None
    c.drawRect(skia.Rect.MakeLTRB(960 - pw / 2 + 50, 520 - ph / 2 + 50, 960 + pw / 2 - 50, 520 + ph / 2 - 50), S("#2A1A0E", 3.0, A(220 * k0), cap=False))
    c.drawRect(skia.Rect.MakeLTRB(960 - pw / 2 + 62, 520 - ph / 2 + 62, 960 + pw / 2 - 62, 520 + ph / 2 - 62), S("#2A1A0E", 1.2, A(200 * k0), cap=False))
    sp = CM.engraved("SIDEREUS", "title", 78, 8.0, "#2A1A0E", 0.8)
    CM.draw_spr(f, sp, 960, 250, "c", alpha=ka, reveal=clamp(ka * 1.2))
    sp2 = CM.engraved("NUNCIUS", "title", 78, 8.0, "#2A1A0E", 0.8)
    CM.draw_spr(f, sp2, 960, 346, "c", alpha=cx.amt(title_at, 0.9, off=0.4), reveal=clamp(cx.amt(title_at, 1.0, off=0.4) * 1.2))
    CM.flourish_rule(f, 960, 392, 520, alpha=0.8 * ka, color="#6A4A2A", grow=ka)
    for blk, (y0, n) in enumerate(((430, 4), (700, 5))):               # küçük satır blokları (okunmaz)
        for i in range(n):
            kk = cx.amt(title_at, 0.5, off=0.9 + blk * 0.3 + i * 0.12)
            wdl = 480 - (i % 2) * 90 - (60 if i == n - 1 else 0)
            c.drawLine(960 - wdl / 2, y0 + i * 30, 960 - wdl / 2 + wdl * kk, y0 + i * 30, S("#2A1A0E", 3.0, A(150 * kk)))
    # MEDICEA SIDERA bandı
    kb = cx.amt(band_at, 0.8)
    yb = 590
    if kb > 0.003:
        c.drawRect(skia.Rect.MakeLTRB(960 - 340, yb - 54, 960 + 340, yb + 54), P("#F3E3AA", A(130 * kb)))
        f.circle(960, yb, 400, shader=f.rad(960, yb, 400, [("#F7DF8E", 0.0, int(70 * kb)), ("#F7DF8E", 1.0, 0)]))
    sp3 = CM.gilt("MEDICEA SIDERA", "title", 56, 6.0) if kb > 0.5 else CM.engraved("MEDICEA SIDERA", "title", 56, 6.0, "#2A1A0E", 0.8)
    CM.draw_spr(f, sp3, 960, yb + 20, "c", alpha=cx.amt(title_at, 0.8, off=1.2), glow=0.25 * kb)
    for j in range(4):
        kr = cx.amt(band_at, 0.5, ease=lambda u: ease_out(u, 3), off=0.3 + 0.2 * j)
        if kr > 0.003:
            icons.draw_icon(f, "star", 960 - 290 + j * 193, yb + 100, size=52 * (0.7 + 0.3 * kr), metal="gold", alpha=kr, glow=0.0)
    cam.end(f)
    CM.finish(f, cx, motes_n=20, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c14_paket: kitap + alet paketi ═══════════════════════════
@CM.ckind("c14_paket")
def k_paket(cx, book_at=0.2, scope_at=1.6, tie_at=3.2, seal_at=4.6, send_at=5.4, seed=9, ovl=None, **_):
    """Masa üstünde kitap (kapakta palle) ve teleskop yan yana gelir; keten bez örtülür, ip dolanır, mühür basılır, paket sağa yola çıkar
    («kitap + alet paketi»; kurye/teslimat çerçevesi, ekranda sıra no YOK)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    wood_floor(c, 720, seed=seed)
    send = ease_in(clamp((t - cx.at(send_at)) / 1.5), 2.0)
    ox = send * 1700.0
    SOFT(c, 960 + ox, 760, 520, 40, "#000000", 120)
    kb = cx.amt(book_at, 0.6, ease=lambda u: ease_out(u, 3))
    ks = cx.amt(scope_at, 0.6, ease=lambda u: ease_out(u, 3))
    kt = cx.amt(tie_at, 0.9)
    c.save()
    c.translate(ox, 0)
    if kt < 0.999:
        if kb > 0.003:                                                   # kitap (kapak)
            bx, by = 640 - (1 - kb) * 300, 560
            c.save()
            c.translate(bx, by)
            c.rotate(-3 * (1 - kb))
            c.drawRoundRect(skia.Rect.MakeLTRB(-190, -250, 190, 250), 8, 8, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-190, -250), (190, 250)], [C("#2A4AA8"), C("#1B2F7A"), C("#101E54")], [0, 0.5, 1])))
            c.drawRoundRect(skia.Rect.MakeLTRB(-190, -250, 190, 250), 8, 8, S("#0A1030", 3.0, 240))
            c.drawRoundRect(skia.Rect.MakeLTRB(-160, -220, 160, 220), 4, 4, S("#D8B25A", 3.0, 230))
            palle_mark(c, 0, -20, 190, 240, "#C0392B")
            c.restore()
        if ks > 0.003:                                                   # teleskop
            tx_, ty_ = 1230 + (1 - ks) * 420, 560
            draw_telescope(c, tx_, ty_, 1.05, -8.0 + 8 * (1 - ks), A(255 * ks))
    # keten bez örtüsü + ip
    if kt > 0.003:
        cw0, cw1 = 320 + (1 - kt) * 120, 1640 - (1 - kt) * 120
        c.drawRoundRect(skia.Rect.MakeLTRB(cw0, 400, cw1, 740), 26, 26, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 400), (0, 740)], [C("#E8DCC0", A(255 * kt)), C("#C9B88E", A(255 * kt)), C("#9C8A5E", A(255 * kt))], [0, 0.5, 1])))
        c.drawRoundRect(skia.Rect.MakeLTRB(cw0, 400, cw1, 740), 26, 26, S("#5A4A2A", 2.4, A(230 * kt)))
        for xx in range(int(cw0) + 40, int(cw1) - 20, 90):
            c.drawLine(xx, 410, xx + 14, 730, S("#7A6A42", 2.0, A(90 * kt)))
        for xx in (700, 960, 1230):                                      # ip: dik sargılar
            kk = clamp(kt * 1.6 - (xx - 700) / 1400)
            c.drawLine(xx, 392, xx, 392 + 358 * kk, S("#6A4A22", 8, A(255 * kt)))
        c.drawLine(cw0 + 20, 570, cw0 + 20 + (cw1 - cw0 - 40) * clamp(kt * 1.3), 570, S("#6A4A22", 8, A(255 * kt)))
        seal_ring_wax = clamp((t - cx.at(seal_at)) / 0.4)
        if seal_ring_wax > 0:
            CM.wax_seal(f, 960, 570, 66, "#A52A1C", alpha=1.0, t=seal_ring_wax, palle=True)
        # etiket (askıda)
        if cx.amt(seal_at, 0.5, off=0.3) > 0.003:
            kk = cx.amt(seal_at, 0.5, off=0.3)
            c.drawLine(1230, 740, 1250, 800, S("#6A4A22", 3.0, A(255 * kk)))
            c.drawRoundRect(skia.Rect.MakeLTRB(1160, 800, 1340, 870), 6, 6, P("#EFE5CC", A(255 * kk)))
            c.drawRoundRect(skia.Rect.MakeLTRB(1160, 800, 1340, 870), 6, 6, S("#5A3E1E", 2.0, A(255 * kk)))
            f.text("BÜYÜK DÜK", 1250, 846, face="title_m", size=26, color="#2A1A0C", align="c", track=3, alpha=kk)
    c.restore()
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None, vig_s=0.42)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c14_dava: 1633 (ağır, süssüz) ═══════════════════════════
def book_front(c, x, y, w, h, col="#1B2F7A", a=255, title=None, f=None, seal_k=0.0):
    c.drawRoundRect(skia.Rect.MakeLTRB(x - w / 2 + 10, y - h / 2 + 14, x + w / 2 + 10, y + h / 2 + 14), 8, 8, P("#000000", A(90 * a / 255)))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - w / 2, y - h / 2, x + w / 2, y + h / 2), 8, 8, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(x - w / 2, y - h / 2), (x + w / 2, y + h / 2)], [C(mix(col, "#FFFFFF", 0.18), a), C(col, a), C(mix(col, "#000000", 0.45), a)], [0, 0.5, 1])))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - w / 2, y - h / 2, x + w / 2, y + h / 2), 8, 8, S("#080C26", 3.0, A(0.9 * a)))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - w / 2 + 28, y - h / 2 + 28, x + w / 2 - 28, y + h / 2 - 28), 4, 4, S("#C9A24A", 2.4, A(0.85 * a)))
    if title and f is not None:
        sp = CM.gilt(title, "title", int(w * 0.13), 6.0)
        CM.draw_spr(f, sp, x, y - h * 0.12, "c", alpha=a / 255.0, glow=0.0)


@CM.ckind("c14_dava")
def k_dava(cx, sahne="terazi", date_at=0.3, book_at=0.4, seal_at=3.0, letters_at=(0.8, 2.6, 4.4), lamp_shrink_at=None, date_txt="1633", title="DIALOGO", seed=3, ovl=None, **_):
    """Ağır sahne (mizah kapalı): sahne='terazi' (karanlık oda, tek ışık, yavaş sallanan terazi + altın «1633»); 'kitap' (lamba havuzunda DIALOGO kitabı, palle ithaf mührü);
    'dilekce' (kapı aralığına ağır ağır kayan üç mühürlü mektup: temkinli girişimler); 'isik' (lamba havuzu tablanın bir yerine kadar erişir; uzaktaki eşyalar karanlıkta).
    Şiddet/figür yok; yalnız eşya ve ışık."""
    f = cx.f
    cam = CM.Cam(cx, push=0.045, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    wood_floor(c, 760, seed=seed)
    lamp_x, lamp_y = 480.0, 760.0
    lit_base = (960.0, 520.0, 900.0)
    if sahne == "terazi":
        k = cx.amt(date_at, 1.2)
        sw = 2.8 * math.sin(t * 0.55) + 1.0
        SOFT(c, 960, 800, 360, 34, "#000000", 140)
        icons.draw_icon(f, "scales", 960, 540, size=470, metal="gold", alpha=0.95, rot=math.radians(sw), glow=0.12)
        sp = CM.gilt(date_txt, "title", 190, 10.0)
        CM.draw_spr(f, sp, 960, 285, "c", alpha=k * 0.9, glow=0.2 * k, reveal=clamp(k * 1.2))
        light = CM.candle_light(t, seed, base=(960, 480), r=780.0, sway=6.0)
    elif sahne == "kitap":
        kb = cx.amt(book_at, 0.9, ease=lambda u: ease_out(u, 3))
        c.drawRect(skia.Rect.MakeLTRB(300, 700, 1620, 784), P("#4A2E16"))
        c.drawRect(skia.Rect.MakeLTRB(300, 700, 1620, 784), S("#1E1008", 2.4, 230, cap=False))
        SOFT(c, 960, 706, 420, 26, "#000000", 140)
        book_front(c, 960, 430 + (1 - kb) * 60, 520, 660, "#1B2F7A", A(255 * kb), title if kb > 0.4 else None, f)
        kseal = clamp((t - cx.at(seal_at)) / 0.4)
        if kseal > 0:
            CM.wax_seal(f, 1180, 640, 62, "#A52A1C", alpha=1.0, t=kseal, palle=True)
        OD.candle(f, 520, 760, 150, t, seed=4, lit=1.0)
        light = CM.candle_light(t, seed, base=(760, 560), r=860.0, sway=8.0)
    elif sahne == "dilekce":
        # kapı (sağ) + alttan ışık sızıntısı; üç mühürlü mektup kayar
        dx0, dx1 = 1340, 1640
        c.drawRect(skia.Rect.MakeLTRB(dx0, 220, dx1, 760), skia.Paint(Shader=skia.GradientShader.MakeLinear([(dx0, 0), (dx1, 0)], [C("#5A3818"), C("#3A2410")], [0, 1])))
        c.drawRect(skia.Rect.MakeLTRB(dx0, 220, dx1, 760), S("#150C05", 4, 240, cap=False))
        c.drawRect(skia.Rect.MakeLTRB(dx0 + 36, 270, dx1 - 36, 470), S("#150C05", 2.4, 200, cap=False))
        c.drawRect(skia.Rect.MakeLTRB(dx0 + 36, 510, dx1 - 36, 720), S("#150C05", 2.4, 200, cap=False))
        c.drawCircle(dx1 - 30, 500, 10, P("#C9A24A"))
        c.drawRect(skia.Rect.MakeLTRB(dx0 + 10, 754, dx1 - 10, 764), P("#FFE3A0", 210))                      # kapı altı ışık
        c.drawPath(sk.poly_path([(dx0 + 10, 764), (dx1 - 10, 764), (dx1 + 160, 830), (dx0 - 160, 830)]), P("#FFE3A0", 52))
        for i, la in enumerate(letters_at):
            u = clamp((t - cx.at(la)) / 2.2)
            if u <= 0:
                continue
            e = ease_io(u, 2.0)
            xx = lerp(560, dx0 + 40, e)
            yy = 790 + 6 * math.sin(u * 3)
            sc = 1.0 - 0.55 * clamp((xx - 1180) / 160)
            al = 1.0 - clamp((u - 0.88) / 0.12)
            c.save()
            c.translate(xx, yy)
            c.scale(sc, sc * 0.5)
            c.drawRoundRect(skia.Rect.MakeLTRB(-90, -60, 90, 60), 6, 6, P("#EFE5CC", A(255 * al)))
            c.drawRoundRect(skia.Rect.MakeLTRB(-90, -60, 90, 60), 6, 6, S("#5A3E1E", 2.4, A(240 * al)))
            c.drawLine(-90, -60, 0, 8, S("#8A6A3A", 2.0, A(200 * al)))
            c.drawLine(90, -60, 0, 8, S("#8A6A3A", 2.0, A(200 * al)))
            c.drawCircle(0, 6, 17, P("#A52A1C", A(255 * al)))
            c.restore()
        OD.candle(f, 440, 760, 140, t, seed=5, lit=1.0)
        light = CM.candle_light(t, seed, base=(1000, 600), r=900.0, sway=8.0)
    else:                                                                   # 'isik': kollayabildiği yere kadar
        c.drawRect(skia.Rect.MakeLTRB(200, 700, 1720, 784), P("#4A2E16"))
        c.drawRect(skia.Rect.MakeLTRB(200, 700, 1720, 784), S("#1E1008", 2.4, 230, cap=False))
        book_closed(c, 560, 700, w=300, h=82, col="#1B2F7A")
        book_closed(c, 1000, 700, w=260, h=70, col="#8A2E1E")
        draw_telescope(c, 1420, 640, 0.82, -4.0)
        c.drawRect(skia.Rect.MakeLTRB(1600, 640, 1700, 700), P("#EFE5CC"))
        OD.candle(f, 300, 700, 140, t, seed=6, lit=1.0)
        shrink = cx.amt(lamp_shrink_at, 2.4) if lamp_shrink_at is not None else 0.0
        light = CM.candle_light(t, seed, base=(560, 560), r=lerp(1150.0, 640.0, shrink), sway=6.0)
    cam.end(f)
    CM.finish(f, cx, motes_n=26, light=light, vig_s=0.6)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ klavsen / piyano ═══════════════════════════
def draw_harpsichord(c, x, y, s=1.0, a=255, col="#7A4C26", lid_col="#233C8C"):
    """Klavsen (önden, çalan kişinin görüşü): açık kapak (iç yüz boyalı lapis + altın çerçeve), gövde, klavye, pano, dört ayak. (x,y) zemin orta."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for lx in (-250, -176, 176, 250):
        c.drawRoundRect(skia.Rect.MakeLTRB(lx - 9, -250, lx + 9, 0), 6, 6, P("#4A2E14", a))
        c.drawRoundRect(skia.Rect.MakeLTRB(lx - 9, -250, lx + 9, 0), 6, 6, S("#1E1008", 2, A(0.9 * a)))
    # kapak (arkada, yukarı açık)
    lid = sk.poly_path([(-250, -318), (250, -318), (214, -640), (-214, -640)])
    c.drawPath(lid, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -640), (0, -318)], [C(mix(lid_col, "#FFFFFF", 0.25), a), C(lid_col, a), C(mix(lid_col, "#000000", 0.35), a)], [0, 0.5, 1])))
    c.drawPath(lid, S("#0A1030", 3.0, A(0.92 * a)))
    inner = sk.poly_path([(-212, -338), (212, -338), (184, -612), (-184, -612)])
    c.drawPath(inner, S("#D8B25A", 3.0, A(0.9 * a)))
    c.drawCircle(0, -480, 54, S("#D8B25A", 3.0, A(0.8 * a)))
    for i in range(8):
        an = i * math.pi / 4
        c.drawLine(math.cos(an) * 22, -480 + math.sin(an) * 22, math.cos(an) * 46, -480 + math.sin(an) * 46, S("#D8B25A", 2.6, A(0.8 * a)))
    # gövde
    c.drawRoundRect(skia.Rect.MakeLTRB(-270, -330, 270, -208), 6, 6, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -330), (0, -208)], [C(mix(col, "#FFFFFF", 0.25), a), C(col, a), C(mix(col, "#000000", 0.4), a)], [0, 0.5, 1])))
    c.drawRoundRect(skia.Rect.MakeLTRB(-270, -330, 270, -208), 6, 6, S("#1E1008", 3.0, A(0.92 * a)))
    c.drawRect(skia.Rect.MakeLTRB(-250, -226, 250, -218), P("#D8B25A", A(0.8 * a)))
    # klavye
    c.drawRect(skia.Rect.MakeLTRB(-215, -332, 215, -292), P("#F4ECD6", A(a)))
    c.drawRect(skia.Rect.MakeLTRB(-215, -332, 215, -292), S("#1E1008", 1.8, A(0.9 * a), cap=False))
    for i in range(1, 18):
        c.drawLine(-215 + i * 24.3, -332, -215 + i * 24.3, -292, S("#1E1008", 1.2, A(0.8 * a)))
    for i in range(17):
        if i % 7 in (2, 6):
            continue
        c.drawRect(skia.Rect.MakeLTRB(-215 + i * 24.3 + 17, -332, -215 + i * 24.3 + 31, -312), P("#1A120A", A(a)))
    c.restore()


@CM.ckind("c14_atolye")
def k_atolye(cx, a_master=0.4, n=3, seed=5, ovl=None, **_):
    """Prensin sarayında klavsenler sırası (kamera sağa kayar); aralarında dolaşıp onlara bakan usta (siluet, yüz yok). Padovalı klavsen ustası."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="top")
    cam.begin(f)
    c = f.c
    t = cx.t
    wood_floor(c, 800, seed=seed)
    cols = ("#7A4C26", "#8A5A2E", "#6A3E1E")
    lids = ("#233C8C", "#2F6A93", "#7A2E3A")
    for i in range(n):
        k = cx.amt(0.0 + i * 0.4, 0.8)
        xi = 560 + i * 760
        SOFT(c, xi, 806, 340, 30, "#000000", 120)
        draw_harpsichord(c, xi, 800, 1.18, A(255 * min(1, k * 2)), col=cols[i % 3], lid_col=lids[i % 3])
    km = cx.amt(a_master, 0.8)
    if km > 0.003:
        walk = clamp((t - cx.at(a_master)) / 5.5)
        xm = lerp(180.0, 560 + 760 * (n - 1) + 380, ease_io(walk, 1.5))
        OD.sil_actor(f, "banker", xm, 800, 380, t, "idle", dir=1, seed=7, walker=(90.0 if 0 < walk < 1 else None), alpha=km)
    cam.end(f)
    CM.finish(f, cx, motes_n=24, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c14_piyano: çekiç mekanizması (kesit) ═══════════════════════════
def _hammer_u(t, presses):
    """Basış olayları → (tuş inişi 0..1, çekiç evresi 0..1, tel genliği, son vuruş zamanı, şiddet)."""
    key, ham, amp, last, vel = 0.0, 0.0, 0.0, -1e9, 0.0
    for (tp, tr, v) in presses:                                 # tp: basış, tr: bırakış, v: 0..1 şiddet
        if t < tp:
            continue
        u = t - tp
        if t < tr:
            key = max(key, ease_out(clamp(u / 0.10), 2))
        else:
            key = max(key, 1.0 - ease_out(clamp((t - tr) / 0.25), 2)) if (t - tr) < 0.25 else key
        hit = 0.05 + 0.04 * (1 - v)
        if u < hit:
            ham = max(ham, ease_in(u / hit, 1.6))
        elif u < 0.35:
            r = (u - hit) / (0.35 - hit)
            ham = max(ham, 1.0 - ease_out(r, 1.6) * 0.92)
        if u >= hit:
            last = max(last, tp + hit)
            vel = v if tp + hit >= last - 1e-9 else vel
            amp = max(amp, (0.35 + 0.9 * v) * math.exp(-(t - tp - hit) * (2.4 + 1.0 * (1 - v))))
    return key, ham, amp, last, vel


@CM.ckind("c14_piyano")
def k_piyano(cx, presses=(), tags=(), seed=3, ovl=None, **_):
    """Çekiçli mekanizma kesiti (tuş → itici/kaçış → çekiç → tel; sönümleyici tel üstünden kalkar). presses=[(basış, bırakış, şiddet 0..1)] çapaları;
    tel titreşimi + ses halkaları şiddetle büyür (piano ↔ forte). tags=[(metin, (x,y) hedef, (lx,ly) etiket, çapa)] çağrı çizgileri."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    pr = [(cx.at(a), cx.at(b), v) for (a, b, v) in presses]
    key, ham, amp, last, vel = _hammer_u(t, pr)
    # kasa + ses tablası
    c.drawRect(skia.Rect.MakeLTRB(140, 760, 1780, 860), P("#5E3C1E"))
    c.drawRect(skia.Rect.MakeLTRB(140, 760, 1780, 860), S("#1E1008", 2.6, 235, cap=False))
    c.drawRect(skia.Rect.MakeLTRB(140, 330, 1780, 760), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 330), (0, 760)], [C("#2A1A0E", 235), C("#3A2410", 235)], [0, 1])))
    c.drawRect(skia.Rect.MakeLTRB(140, 330, 1780, 760), S("#150C05", 3, 255, cap=False))
    # tel (titreşir)
    yS = 440.0
    pa = skia.Path()
    pa.moveTo(250, yS)
    nseg = 60
    for i in range(1, nseg + 1):
        x = 250 + (1500) * i / nseg
        env = math.sin(math.pi * i / nseg)
        pa.lineTo(x, yS + amp * 26 * env * math.sin(t * 90 + i * 0.4))
    c.drawPath(pa, S("#E8D9A0", 3.2, 255))
    c.drawPath(pa, S("#8A6A20", 1.2, 255))
    for xx in (250, 1750):
        c.drawCircle(xx, yS, 9, P("#B8903A"))
    # ses halkaları
    if t - last < 1.6 and last > -1e8:
        for i in range(3):
            u = (t - last - i * 0.16) / 1.1
            if 0 < u < 1:
                c.drawCircle(1000, yS - 40, 60 + 380 * ease_out(u, 2) * (0.6 + 0.8 * vel), S("#F0D27A", 2.4 + 3 * vel, A(190 * (1 - u))))
    # tuş (kaldıraç)
    pivx, pivy = 700.0, 780.0
    ang = math.radians(4.2 * key)                  # ön uç iner
    c.save()
    c.translate(pivx, pivy)
    c.rotate(math.degrees(ang))
    c.drawRoundRect(skia.Rect.MakeLTRB(-520, -34, 280, 6), 5, 5, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -34), (0, 6)], [C("#F4E8CC"), C("#D8C79A")], [0, 1])))
    c.drawRoundRect(skia.Rect.MakeLTRB(-520, -34, 280, 6), 5, 5, S("#1E1008", 2.6, 240))
    c.restore()
    c.drawCircle(pivx, pivy + 10, 12, P("#6B4424"))
    # itici (jack) – tuşun arka ucunda; vuruş anında kayar (kaçış)
    rx = pivx + 240 * math.cos(ang)
    ry = pivy - 240 * math.sin(ang) * -1 - 30 + 0
    ry = pivy + math.sin(ang) * 240 - 30
    slip = 16 * clamp((ham - 0.55) / 0.4)
    c.save()
    c.translate(rx, ry)
    c.drawRect(skia.Rect.MakeLTRB(-8, -110, 8, 6), P("#8A5A2E"))
    c.drawPath(sk.poly_path([(-8 - slip, -110), (8 - slip, -110), (8 - slip + 18, -126), (-8 - slip, -128)]), P("#C9A24A"))
    c.drawRect(skia.Rect.MakeLTRB(-8, -110, 8, 6), S("#1E1008", 1.8, 220, cap=False))
    c.restore()
    # çekiç
    P0 = (1010.0, 740.0)
    L_ = 305.0
    a0, a1 = -146.0, -104.0
    th = math.radians(lerp(a0, a1, ham))
    hx, hy = P0[0] + L_ * math.cos(th), P0[1] + L_ * math.sin(th)
    c.drawLine(P0[0], P0[1], hx, hy, S("#4A2E14", 14, 255))
    c.drawLine(P0[0], P0[1], hx, hy, S("#9A6A3C", 6, 255))
    c.drawCircle(P0[0], P0[1], 14, P("#C9A24A"))
    hd = skia.Path()
    hd.addOval(skia.Rect.MakeLTRB(hx - 26, hy - 34, hx + 26, hy + 22))
    c.save()
    c.translate(0, 0)
    c.drawPath(hd, P("#E8D2A8"))                           # keçe başlık
    c.drawPath(hd, S("#6A4A22", 3.0, 240))
    c.drawRect(skia.Rect.MakeLTRB(hx - 14, hy + 18, hx + 14, hy + 40), P("#7A4A22"))
    c.restore()
    # sönümleyici (tuş basılıyken kalkar)
    dk = clamp(key * 1.6)
    dy_ = 12 - 52 * dk
    c.drawRect(skia.Rect.MakeLTRB(1180, yS + dy_ - 36, 1260, yS + dy_ + 2), P("#A8321E"))
    c.drawRect(skia.Rect.MakeLTRB(1180, yS + dy_ - 36, 1260, yS + dy_ + 2), S("#3A0E08", 2.2, 240, cap=False))
    c.drawLine(1220, yS + dy_ - 36, 1220, yS - 150, S("#2A2C32", 4, 230))
    # ince çağrı etiketleri
    for (txt, tp_, lp_, an) in tags:
        k = cx.amt(an, 0.5)
        if k <= 0.003:
            continue
        c.drawLine(lp_[0], lp_[1] + 14, lerp(lp_[0], tp_[0], k), lerp(lp_[1] + 14, tp_[1], k), S("#F0D27A", 2.6, A(230 * k)))
        wd = sk.text_width(txt, "title_m", 34, 6) + 60
        CM.tablet(f, lp_[0] - wd / 2, lp_[1] - 36, wd, 64, alpha=k, corner=8)
        CM.ink(f, txt, lp_[0], lp_[1] + 10, face="title_m", size=34, color=TH.fg, align="c", track=6, alpha=k, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=16, light=None, vig_s=0.5)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c14_gazete: Maffei'nin gazete makalesi (piano · forte) ═══════════════════════════
@CM.ckind("c14_gazete")
def k_gazete(cx, head_at=0.8, piano_at=2.4, forte_at=3.8, mast="GAZETE", seed=5, ovl=None, **_):
    """Basılı gazete sayfası: künye bandı, üç sütun (okunmaz satırlar), ortada başlık kutusu: «piano» küçük/soluk italik, «FORTE» iri/ağır (sayfa vuruşla titrer) —
    «piano e forte» ad oyunu. Maffei adı sahne dosyasından levhayla gelir."""
    f = cx.f
    cam = CM.Cam(cx, push=0.05, drift=(3.0, 2.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    pw, ph = 1340, 900
    shake = 0.0
    uf = t - cx.at(forte_at)
    if 0 <= uf < 0.5:
        shake = math.exp(-uf * 9) * math.sin(uf * 90)
    pp = PP.paper_image(pw, ph, seed, (232, 223, 196), "deckle", (("h", 0.5),), 44, 1.2)
    pp.draw(f, 960 + 5 * shake, 520 + 3 * shake, rot=-0.006, scale=1.0, alpha=cx.amt(0.0, 0.8), shadow=0.6)
    c.save()
    c.translate(960 + 5 * shake, 520 + 3 * shake)
    km = cx.amt(0.3, 0.8)
    sp = CM.engraved(mast, "title", 70, 14.0, "#2A1A0E", 0.8)
    CM.draw_spr(f, sp, 0, -ph / 2 + 110, "c", alpha=km)
    CM.flourish_rule(f, 0, -ph / 2 + 150, pw * 0.82, alpha=0.9 * km, color="#4A3420", grow=km)
    c.drawLine(-pw * 0.41, -ph / 2 + 162, pw * 0.41, -ph / 2 + 162, S("#2A1A0E", 2.0, A(180 * km)))
    # sütunlar
    for col in range(3):
        x0 = -pw / 2 + 80 + col * ((pw - 160) / 3)
        for r in range(11):
            if col == 1 and 2 <= r <= 5:
                continue
            kk = cx.amt(0.5 + 0.06 * r + 0.15 * col, 0.5)
            wdl = (pw - 160) / 3 - 40 - ((r * 37 + col * 11) % 60)
            c.drawLine(x0, -ph / 2 + 220 + r * 40, x0 + wdl * kk, -ph / 2 + 220 + r * 40, S("#2A1A0E", 3.0, A(120 * kk)))
        if col:
            c.drawLine(x0 - 22, -ph / 2 + 190, x0 - 22, ph / 2 - 70, S("#2A1A0E", 1.6, A(130 * km)))
    # başlık kutusu
    kh = cx.amt(head_at, 0.6)
    bx0, bx1, by0, by1 = -430, 430, -ph / 2 + 215, -ph / 2 + 470
    c.drawRect(skia.Rect.MakeLTRB(bx0, by0, bx1, by1), P("#EADFC0", A(235 * kh)))
    c.drawRect(skia.Rect.MakeLTRB(bx0, by0, bx1, by1), S("#2A1A0E", 4.0, A(230 * kh), cap=False))
    c.drawRect(skia.Rect.MakeLTRB(bx0 + 10, by0 + 10, bx1 - 10, by1 - 10), S("#2A1A0E", 1.4, A(180 * kh), cap=False))
    ky = (by0 + by1) / 2 + 36
    kp = cx.amt(piano_at, 0.7)
    kf = cx.amt(forte_at, 0.22, ease=lambda u: ease_out(u, 3))
    if kp > 0:
        f.text("piano", -250, ky, face="cap_i", size=74, color="#7A6A54", align="c", alpha=kp * 0.9)
    if kp > 0 and kf > 0:
        f.text("e", -88, ky - 6, face="cap_i", size=44, color="#7A6A54", align="c", alpha=min(kp, kf))
    if kf > 0:
        sc = 1.0 + (1 - kf) * 0.7
        c.save()
        c.translate(190, ky + 10)
        c.scale(sc, sc)
        f.text("FORTE", 0, 0, face="title", size=128, color="#7A1E16", align="c", track=4, alpha=kf)
        c.restore()
    km2 = cx.amt(forte_at, 0.9, off=0.5)
    if km2 > 0:
        c.drawRect(skia.Rect.MakeLTRB(bx0 + 24, ky - 92, bx0 + 24 + (bx1 - bx0 - 48) * km2, ky + 28), P("#F2D860", A(60 * km2)))
    c.restore()
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c14_vitrin: bugüne kalan üç piyano ═══════════════════════════
def draw_piano_sil(c, x, y, s=1.0, a=255, col="#14100C", rim="#E8B66A"):
    """Kuyruklu piyano silueti (yandan, kapak yarım açık). (x,y) zemin."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for off, cc in ((2.0, rim), (0.0, col)):
        c.save()
        c.translate(off, -off * 0.6)
        body = skia.Path()
        body.moveTo(-200, -190)
        body.lineTo(110, -190)
        body.cubicTo(190, -190, 240, -168, 230, -140)
        body.cubicTo(220, -118, 170, -126, 110, -126)
        body.lineTo(-200, -126)
        body.close()
        c.drawPath(body, P(cc, a))
        c.drawRect(skia.Rect.MakeLTRB(-232, -190, -198, -168), P(cc, a))
        for lx in (-170, 90, 190):
            c.drawLine(lx, -128, lx - 3, 0, S(cc, 10, a))
        c.drawPath(sk.poly_path([(-190, -192), (120, -192), (88, -266), (-150, -230)]), P(cc, a))
        c.drawLine(40, -192, 60, -250, S(cc, 4, a))
        c.restore()
    c.restore()


@CM.ckind("c14_vitrin")
def k_vitrin(cx, cases=(), seed=4, ovl=None, **_):
    """Müze duvarı boyunca üç vitrin (kamera `pan r`): her birinde Cristofori piyanosu silueti; kasa levhasında şehir + yıl; spot ışığı yanar.
    cases=[dict(x, city, year, at)]. Sıra: New York · Roma · Leipzig; yıllar 1720 · 1722 · 1726."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="top")
    cam.begin(f)
    c = f.c
    t = cx.t
    c.drawRect(skia.Rect.MakeLTRB(-700, 820, 4600, H + 300), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 820), (0, H + 200)], [C("#B9A98A"), C("#7A6A4A")], [0, 1])))
    c.drawLine(-700, 820, 4600, 820, S("#2A1A0E", 3, 220))
    for cs in cases:
        xx = cs["x"]
        k = cx.amt(cs["at"], 0.8, ease=lambda u: ease_out(u, 3))
        ksp = cx.amt(cs.get("spot", cs["at"]), 0.9)
        if ksp > 0.003:                                              # boş kaide + spot (piyanodan önce)
            SOFT(c, xx, 830, 360, 30, "#000000", 120 * ksp)
            c.drawRect(skia.Rect.MakeLTRB(xx - 300, 700, xx + 300, 820), P("#8A7A5A", A(255 * ksp)))
            c.drawRect(skia.Rect.MakeLTRB(xx - 300, 700, xx + 300, 820), S("#2A1A0E", 2.4, A(230 * ksp), cap=False))
            c.drawRect(skia.Rect.MakeLTRB(xx - 314, 688, xx + 314, 704), P("#A8946A", A(255 * ksp)))
            c.drawPath(sk.poly_path([(xx - 40, 150), (xx + 40, 150), (xx + 300, 700), (xx - 300, 700)]), P("#FFF2C8", A(34 * ksp)))
        if k <= 0.003:
            continue
        draw_piano_sil(c, xx, 700 - (1 - k) * 36, 1.28, A(255 * k))
        # cam
        c.drawRect(skia.Rect.MakeLTRB(xx - 290, 230, xx + 290, 700), P("#BEE0F0", A(26 * k)))
        c.drawRect(skia.Rect.MakeLTRB(xx - 290, 230, xx + 290, 700), S("#E8F4FA", 3.0, A(150 * k), cap=False))
        c.drawLine(xx - 230, 250, xx - 110, 520, S("#FFFFFF", 12, A(30 * k)))
        # levha
        wd = 400
        CM.tablet(f, xx - wd / 2, 726, wd, 78, alpha=k, corner=8)
        CM.ink(f, cs["city"], xx - 82, 774, face="title_m", size=30, color=TH.fg, align="c", track=3, alpha=k, emboss=False)
        CM.ink(f, cs["year"], xx + 128, 776, face="title", size=40, color=TH.acc, align="c", track=2, alpha=k, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None, vig_s=0.42)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c14_azalan: envanter satırları sürerken ailenin satırları azalır ═══════════════════════════
def scribble_line(c, x0, x1, y, k, seed=0, col="#2A1A0E", a=200, amp=4.0):
    if k <= 0.003:
        return
    rs = np.random.RandomState(seed)
    pth = skia.Path()
    pth.moveTo(x0, y)
    xcur = x0
    while xcur < x0 + (x1 - x0) * k:
        wl = rs.uniform(26, 90)
        xe = min(xcur + wl, x0 + (x1 - x0) * k)
        m = max(2, int((xe - xcur) / 8))
        for j in range(1, m + 1):
            px = xcur + (xe - xcur) * j / m
            pth.quadTo(px - (xe - xcur) / m * 0.5, y + rs.uniform(-amp, amp), px, y + (rs.uniform(-amp, amp) if j % 2 else 0))
        xcur = xe + rs.uniform(12, 22)
        pth.moveTo(xcur, y)
    c.drawPath(pth, S(col, 2.2, A(a)))


@CM.ckind("c14_azalan")
def k_azalan(cx, rows_at=0.3, row_dt=0.34, dim_at=3.0, dim_dt=0.55, n_fam=6, seed=3, ovl=None, **_):
    """Envanter defteri: sol sayfada satırlar sürmekte (yazılır); sağ sayfada ailenin satırları: altı palle nişi, her biri bir mum gibi sırayla söner. Kamera sağa kayar, karanlığa."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    pp = PP.paper_image(1500, 820, seed, (236, 224, 192), "deckle", (("v", 0.5),), 44, 1.1)
    pp.draw(f, 960, 520, rot=-0.008, scale=1.0, alpha=1.0, shadow=0.7)
    for i in range(12):
        kk = clamp((t - cx.at(rows_at) - i * row_dt) / 0.7)
        scribble_line(c, 290, 920, 236 + i * 52, kk, seed=20 + i, a=210 - i * 5)
        if kk > 0.99 or (kk > 0):
            pass
    for j in range(n_fam):
        xx = 1040 + (j % 3) * 230
        yy = 330 + (j // 3) * 290
        td = cx.at(dim_at) + j * dim_dt
        lit = 1.0 - ease_io(clamp((t - td) / 0.9), 2.0)
        c.drawRoundRect(skia.Rect.MakeLTRB(xx - 82, yy - 100, xx + 82, yy + 100), 14, 14, P("#2A1A0E", 150))
        c.drawRoundRect(skia.Rect.MakeLTRB(xx - 82, yy - 100, xx + 82, yy + 100), 14, 14, S("#7A5C32", 3.0, 230))
        fl = 0.85 + 0.15 * math.sin(t * 9 + j * 2.1)
        c.drawCircle(xx, yy, 110, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((xx, yy), 110, [C("#FFD27A", A(150 * lit * fl)), C("#FFD27A", 0)], [0, 1])))
        palle_mark(c, xx, yy, 112, A(255 * (0.35 + 0.65 * lit)), "#B33620")
        if 0 < t - td < 1.6:                               # söndükten sonra ince duman
            u = (t - td) / 1.6
            c.drawLine(xx, yy - 40 - 60 * u, xx + math.sin(u * 6) * 8, yy - 100 - 90 * u, S("#BEB3A0", 3, A(120 * (1 - u))))
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None, vig_s=0.5)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ «MEDİCİ'NİN PAYI» sayacı (ovl) ═══════════════════════════
def tracker(chips, x=1830, y=222, title="MEDİCİ'NİN PAYI", size=30):
    """Sağ altta sayaç: her chip kendi çapasında belirir ve damgalanır (chips=[(metin, çapa, 'ok'|'no')]); sağa yaslı, altyazı bandının (y≈938) üstünde."""
    def fn(cx):
        f = cx.f
        ks = [cx.amt(a, 0.35, ease=lambda u: ease_out(u, 3)) for (_, a, _) in chips]
        if not ks or max(ks) <= 0.003:
            return
        ws = [sk.text_width(tx, "title_m", size, 5) + 60 + (36 if st == "no" else 0) for (tx, _, st) in chips]
        xr = x
        kt = max(ks)
        wt = sk.text_width(title, "title_m", size * 0.9, 6)
        CM.ink(f, title, x, y - 64, face="title_m", size=size * 0.9, color=TH.fg2 if TH.day else "#E7D9AE", align="r", track=6, alpha=kt, emboss=False)
        for (tx, a, st), k, wd in reversed(list(zip(chips, ks, ws))):
            if k <= 0.003:
                continue
            xx = xr - wd
            yy = y - 36 + (1 - k) * 14
            CM.tablet(f, xx, yy, wd, 66, alpha=k, corner=8, edge="#2E6A46" if st == "ok" else "#A8321E")
            CM.ink(f, tx, xx + 30, yy + 44, face="title_m", size=size, color=TH.fg, align="l", track=5, alpha=k, emboss=False)
            if st == "no":
                CM.ink(f, "✕", xx + wd - 34, yy + 46, face="title_m", size=size + 6, color="#A8321E", align="c", alpha=k, emboss=False)
            xr = xx - 14
    return fn


# ═══════════════════════════ c14_pay: SAHNE · MAAŞ · ENVANTER — icat değil ═══════════════════════════
@CM.ckind("c14_pay")
def k_pay(cx, no_at=0.6, pay_at=2.0, inv_at=3.2, seed=4, ovl=None, **_):
    """Üç kart: «İCAT» (palle damgası piyanoya iner, geri sekip kırmızı ✕ bırakır — mizah, kısa), «MAAŞ» (altın sikke kesenin içine düşer), «ENVANTER» (satır yazılır ✓).
    Sol→sağ; her kart kendi sözcüğünde belirir."""
    f = cx.f
    cam = CM.Cam(cx, push=0.04, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    cards = [(400.0, "İCAT", no_at, "#A8321E"), (960.0, "MAAŞ", pay_at, "#2E6A46"), (1520.0, "ENVANTER", inv_at, "#2E6A46")]
    for i, (xc, hd, an, edge) in enumerate(cards):
        k = cx.amt(an, 0.5, ease=lambda u: ease_out(u, 3), off=-0.35)
        if k <= 0.003:
            continue
        yc = 520 + (1 - k) * 60
        CM.tablet(f, xc - 250, yc - 300, 500, 600, alpha=k, corner=14, edge=edge)
        sp = CM.engraved(hd, "title", 54, 8.0, "#2A1A0E", 0.8)
        CM.draw_spr(f, sp, xc, yc - 220, "c", alpha=k)
        CM.flourish_rule(f, xc, yc - 190, 360, alpha=0.8 * k, color="#7A5A2E", grow=k)
    # A: damga ↔ piyano
    kA = cx.amt(no_at, 0.5, off=-0.35)
    if kA > 0.003:
        draw_piano_sil(c, 400, 640, 0.95, A(255 * kA))
        u = clamp((t - cx.at(no_at)) / 1.3)
        if u > 0:
            if u < 0.40:
                sy = lerp(120.0, 330.0, ease_in(u / 0.40, 2.0))
            elif u < 0.62:
                sy = lerp(330.0, 250.0, ease_out((u - 0.40) / 0.22, 2.0))
            else:
                sy = lerp(250.0, 150.0, smooth((u - 0.62) / 0.38))
            c.save()
            c.translate(400, sy)
            c.drawRoundRect(skia.Rect.MakeLTRB(-26, -170, 26, -40), 12, 12, P("#7A4C26", A(255 * kA)))
            c.drawRoundRect(skia.Rect.MakeLTRB(-26, -170, 26, -40), 12, 12, S("#1E1008", 2.4, A(240 * kA)))
            c.drawRoundRect(skia.Rect.MakeLTRB(-96, -40, 96, 0), 6, 6, P("#3A3C44", A(255 * kA)))
            palle_mark(c, 0, -20, 74, A(255 * kA), "#C0392B")
            c.restore()
            kx = clamp((u - 0.42) / 0.2)
            if kx > 0:
                c.drawLine(300, 470, 300 + 200 * kx, 470 + 200 * kx, S("#A8321E", 18, A(235 * kx)))
                c.drawLine(500, 470, 500 - 200 * kx, 470 + 200 * kx, S("#A8321E", 18, A(235 * kx)))
    # B: sikke → kese
    kB = cx.amt(pay_at, 0.5, off=-0.35)
    if kB > 0.003:
        icons.draw_icon(f, "coinbag", 960, 640, size=250, metal="gold", alpha=kB)
        u = clamp((t - cx.at(pay_at)) / 0.8)
        if u > 0:
            cy_ = lerp(250.0, 560.0, ease_in(u, 2.0)) if u < 1 else 560.0
            if u < 1:
                c.save()
                c.translate(960, cy_)
                c.scale(abs(math.cos(u * 9.0)) * 0.8 + 0.2, 1.0)
                coin_flat = L.coin_flat
                coin_flat(c, 0, 0, r=44)
                c.restore()
            else:
                for j in range(3):
                    uu = (t - cx.at(pay_at) - 0.8 - j * 0.16) / 0.9
                    if 0 < uu < 1:
                        c.drawCircle(960, 600, 40 + 150 * ease_out(uu, 2), S("#D8A63A", 3.0, A(190 * (1 - uu))))
    # C: satır yazılır ✓
    kC = cx.amt(inv_at, 0.5, off=-0.35)
    if kC > 0.003:
        c.drawRect(skia.Rect.MakeLTRB(1300, 400, 1740, 700), P("#EFE5CC", A(255 * kC)))
        c.drawRect(skia.Rect.MakeLTRB(1300, 400, 1740, 700), S("#7A5C32", 2.0, A(230 * kC), cap=False))
        for r in range(5):
            c.drawLine(1330, 450 + r * 52, 1710, 450 + r * 52, S("#B8A678", 1.4, A(160 * kC)))
        k_w = clamp((t - cx.at(inv_at)) / 1.3)
        scribble_line(c, 1330, 1710, 446 + 2 * 52, k_w, seed=77, a=230)
        scribble_line(c, 1330, 1660, 446, 1.0 * kC, seed=70, a=120)
        scribble_line(c, 1330, 1690, 446 + 52, 1.0 * kC, seed=71, a=120)
        kk = clamp((t - cx.at(inv_at) - 1.3) / 0.35)
        if kk > 0:
            pa = skia.Path()
            pa.moveTo(1620, 640)
            pa.lineTo(1650, 670)
            pa.lineTo(1710, 590)
            seg = skia.Path()
            pm = skia.PathMeasure(pa, False)
            pm.getSegment(0, pm.getLength() * kk, seg, True)
            c.drawPath(seg, S("#2E6A46", 14, 255))
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)
