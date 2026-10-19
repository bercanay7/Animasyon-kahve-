"""p2_lib — PARÇA 2 (c3 Kule ve Sürgün · c4 Kubbe ve Kefaret · c5 Konsil, Kitap, Platon) ortak çizim/yardımcı işlevleri.

Sahne yazarı (Parça 2) modülü. Motor/dünya dosyalarına dokunmaz; yalnız onların işlevlerini ÇAĞIRIR (cilt_medici, cilt_oda, cilt_pano, cilt_anim, cilt_sehir).
İçerik:
  * boya kısayolları (P, S), `bake` (statik katmanı görüntüye pişirme önbelleği)
  * `mono_begin/mono_end` — GRAVÜR (siyah-beyaz sepya mürekkep) katmanı: rivayet/anekdot bölümleri bu filtreyle çizilir (renk = belge, gravür = rivayet)
  * etiket/levha/damga yardımcıları (çapaya bağlı, `cx.amt` ile)
  * küçük nesneler: el, ekmek, kâse, kâğıt pusulası, torba, yumurta, mühür vb. (gravür dilinde)
Kural: yüz çizilmez (siluet), kan/şiddet yok; ekrana yalnız script/brif sözcükleri yazılır.
"""
import functools
import math

import numpy as np
import skia

import cilt_anim as FA
import cilt_medici as CM
import cilt_oda as OD
import cilt_pano as PN
import cilt_paper as PP
import sk
from cilt_medici import PIG, TH
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth

INK = "#2A1A0C"
INK_S = "#3A2616"
PAPER_T = (236, 224, 192)
_RS = PN._RS
R, RA, INKP, INKR, LINE, POLY, OVAL, GRAD_V = PN.R, PN.RA, PN.INKP, PN.INKR, PN.LINE, PN.POLY, PN.OVAL, PN.GRAD_V
PT, STK, SOFT, FILLP, RRECT = OD.PT, OD.STK, OD.SOFT, OD.FILLP, OD.RRECT
LIN = CM._LIN


# ───────────────────────────── boya / yol kısayolları ─────────────────────────────
def P(col, a=255, **kw):
    return skia.Paint(AntiAlias=True, Color=C(col, int(a)), **kw)


def S(col, w=1.5, a=255, cap=True):
    return STK(col, w, int(a), cap)


def path_pts(pts, close=True):
    return sk.poly_path(pts, close)


def smooth_pts(pts, close=False, tension=0.5):
    return sk.smooth_path(pts, close, tension)


_BAKED = {}


def bake(key, w, h, draw, pad=0):
    """Statik katmanı bir kez görüntüye pişir (key ile önbellek). draw(frame) → tuval (0,0)–(w,h)."""
    im = _BAKED.get(key)
    if im is None:
        fr = sk.Frame(int(w), int(h))
        fr.clear(skia.ColorTRANSPARENT)
        draw(fr)
        im = _BAKED[key] = fr.surf.makeImageSnapshot()
    return im


def blit(c, im, x, y, a=1.0, sx=1.0, sy=None, rot=0.0, ax=0.5, ay=0.5):
    """Görüntüyü (x,y) noktasına (ax, ay) çapayla yerleştir."""
    sy = sx if sy is None else sy
    p = skia.Paint(AntiAlias=True)
    if a < 1.0:
        p.setAlphaf(clamp(a))
    c.save()
    c.translate(x, y)
    if rot:
        c.rotate(rot)
    c.scale(sx, sy)
    c.drawImage(im, -ax * im.width(), -ay * im.height(), LIN, p)
    c.restore()


# ───────────────────────────── gravür filtresi (siyah-beyaz sepya) ─────────────────────────────
_MONO = {}


def _mono_filter(k=1.0, tone=(1.00, 0.93, 0.80), contrast=1.10):
    key = (round(k, 2), tone, contrast)
    cf = _MONO.get(key)
    if cf is None:
        lr, lg, lb = 0.30, 0.59, 0.11
        rows = []
        for ti in tone:
            a = ti * contrast
            rows.append([lr * a, lg * a, lb * a, 0, (1 - contrast) * 0.5 * ti * 0.8])
        # k: 0 = özdeş, 1 = tam gravür
        ident = [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0]]
        m = []
        for r_i in range(3):
            m += [ident[r_i][j] * (1 - k) + rows[r_i][j] * k for j in range(5)]
        m += [0, 0, 0, 1, 0]
        cf = _MONO[key] = skia.ColorFilters.Matrix(m)
    return cf


def mono_begin(f, k=1.0, tone=(1.00, 0.93, 0.80), contrast=1.10):
    """Gravür katmanı aç: içinde çizilen her şey siyah-beyaz sepya mürekkebe çevrilir. k<1 → renkten gravüre geçiş."""
    if k <= 0.001:
        f.c.save()
        return False
    f.c.saveLayer(None, skia.Paint(ColorFilter=_mono_filter(k, tone, contrast)))
    return True


def mono_end(f):
    f.c.restore()


# ───────────────────────────── yazı / etiket / damga ─────────────────────────────
def tag(f, cx, text, x, y, at=0.0, size=34, face="title_m", track=6.0, sub=None, w=None, dur=0.55, align="c", off=0.0, hold=None, color=None):
    """Çapaya bağlı isim/etiket levhası (tablet + oyma yazı). Yerleşim (x,y) levha merkezi. hold=(çıkış çapası) verilirse sonra solar."""
    k = cx.amt(at, dur, off=off)
    if hold is not None:
        k *= 1.0 - cx.amt(hold, 0.4)
    if k <= 0.003:
        return
    wd = (w if w is not None else sk.text_width(text, face, size, track) + 76)
    hh = size + 44 + (size * 0.78 if sub else 0)
    xx = x - wd / 2 if align == "c" else x
    yy = y - hh / 2 + (1 - k) * 10
    CM.tablet(f, xx, yy, wd, hh, alpha=k, corner=8)
    CM.ink(f, text, xx + wd / 2, yy + 8 + size * 1.02, face=face, size=size, color=color or TH.fg, align="c", track=track, alpha=k, emboss=False)
    if sub:
        CM.ink(f, sub, xx + wd / 2, yy + 8 + size * 1.02 + size * 0.86, face="cap_i", size=size * 0.74, color=TH.fg2, align="c", alpha=k, emboss=False)


def stamp_at(f, cx, text, x, y, at, rot=-0.10, size=52, color=None, dur=0.3, off=0.0, hold=None):
    """Damga çarpması (CM.stamp t=0..1) — çapa anında vurur; hold çapasında solar."""
    k = cx.amt(at, dur, off=off)
    if k <= 0.003:
        return
    al = 1.0 - (cx.amt(hold, 0.5) if hold is not None else 0.0)
    CM.stamp(f, text, x, y, rot=rot, size=size, color=color, alpha=al, t=k)


def stamp_src(f, cx, text, x, y, at, rot=-0.08, size=44, color=None, dur=0.3, off=0.0, hold=None):
    """Kaynak sınıfı damgası '○ TEK KAYNAK': Cinzel'de ○ glifi yok → halka elle çizilir (damganın sol başında)."""
    k = cx.amt(at, dur, off=off)
    if k <= 0.003:
        return
    al = 1.0 - (cx.amt(hold, 0.5) if hold is not None else 0.0)
    lead = "   "
    full = lead + text
    CM.stamp(f, full, x, y, rot=rot, size=size, color=color, alpha=al, t=k)
    col = color or (TH.acc if TH.day else "#E56A52")
    wd = sk.text_width(full, "title", size, 7) + 64
    sw = sk.text_width(lead, "title", size, 7)
    x0 = -(wd - 64) / 2 + sw * 0.46
    sc = 1.0 + (1 - sk.back_out(k)) * 0.8 if k < 1 else 1.0
    a = al * min(1.0, k * 3)
    c = f.c
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(rot))
    c.scale(sc, sc)
    p = f.paint(col, style="stroke", sw=5.0, alpha=0.9 * a)
    CM.wobble(p, 7.0, 0.9, 7)
    c.drawCircle(x0, -size * 0.04, size * 0.27, p)
    c.restore()


def date_plate(f, cx, text, at, x=96, y=860, size=50):
    """Sol altta tarih levhası (HUD'a değil, sahneye ait; altyazı bölgesi y≈938–1042 dışında kalır)."""
    k = cx.amt(at, 0.55)
    if k <= 0.003:
        return
    wd = sk.text_width(text, "title", size, 6) + 76
    CM.tablet(f, x, y - 64 * k, wd, 90, alpha=k, corner=10)
    CM.ink(f, text, x + wd / 2, y - 6 * k, face="title", size=size * 0.80, color=TH.fg, align="c", track=6, alpha=k, emboss=False)


def engr(f, cx, text, x, y, at, size=70, track=10.0, color=None, style="engraved", dur=1.0, face="title", off=0.0, alpha=1.0, glow=0.0, scale=1.0):
    """Çapaya bağlı oyma/yaldız yazı (soldan açılır)."""
    k = cx.amt(at, dur, off=off)
    if k <= 0.003:
        return
    if style == "gilt":
        sp = CM.gilt(text, face, int(size), float(track))
    else:
        sp = CM.engraved(text, face, int(size), float(track), color or TH.fg)
    CM.draw_spr(f, sp, x, y, "c", alpha=alpha * min(1.0, k * 2.0), reveal=clamp(k * 1.12), glow=glow * k, scale=scale)
    return sp.wid


def breath(cx, a=0.008, hz=0.45, ph=0.0):
    return 1.0 + a * math.sin(cx.t * hz * 6.283 + ph)


def wob(t, hz, amp, ph=0.0):
    return amp * math.sin(t * hz * 6.283 + ph)


def draw_sticker(f, x, y, w, h, text, a=1.0, rot=0.0, scale=1.0, peel=0.0, tone="#F2F0E8", ink="#1B2A4A", size=62, track=6.0, face="title", sub=None):
    """«Sonradan eklenen» modern etiket (beyaz yapışkan): (x,y) merkez; peel 0..1 sol-alt köşeden kalkıp savrulur; a şeffaflık."""
    if a <= 0.003:
        return
    c = f.c
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(rot))
    c.scale(scale, scale)
    if peel > 0:
        px, py = -w / 2, h / 2
        c.translate(px, py)
        c.rotate(-math.degrees(1.25 * smooth(peel)))
        c.translate(-px + 40 * peel * peel, -py - 90 * peel * peel)
    if a < 0.999:
        _lp = skia.Paint()
        _lp.setAlphaf(clamp(a))
        c.saveLayer(None, _lp)
    SOFT(c, 6, 12, w * 0.52, h * 0.58, "#000000", 90)
    rr = skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, h / 2)
    sh = skia.GradientShader.MakeLinear([(0, -h / 2), (0, h / 2)], [C(mix(tone, "#FFFFFF", 0.5)), C(tone), C(mix(tone, "#9A9484", 0.25))], [0.0, 0.55, 1.0])
    c.drawRoundRect(rr, 14, 14, skia.Paint(AntiAlias=True, Shader=sh))
    c.drawRoundRect(skia.Rect.MakeLTRB(-w / 2 + 9, -h / 2 + 9, w / 2 - 9, h / 2 - 9), 9, 9, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0, Color=C(ink, 110)))
    c.drawRoundRect(rr, 14, 14, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C("#2A2A2A", 120)))
    CM.ink(f, text, 0, size * (0.12 if sub else 0.34), face=face, size=size, color=ink, align="c", track=track, alpha=1.0, emboss=False)
    if sub:
        CM.ink(f, sub, 0, h * 0.30, face="cap_b", size=max(20, size * 0.34), color=ink, align="c", track=3, alpha=0.8, emboss=False)
    cp = skia.Path()
    cp.moveTo(w / 2 - 54, h / 2)
    cp.lineTo(w / 2, h / 2 - 54)
    cp.lineTo(w / 2, h / 2)
    cp.close()
    c.drawPath(cp, skia.Paint(AntiAlias=True, Color=C("#FFFFFF", 150)))
    if a < 0.999:
        c.restore()
    c.restore()


# ───────────────────────────── gravür dilinde küçük nesneler ─────────────────────────────
def hand_arm(c, x, y, ang, reach, s=1.0, col="#D9B48A", sleeve="#3A2A1C", fingers=True, open_=0.0, a=255, cuff="#E8DCC0"):
    """Kol + el (mürekkep dış hatlı): (x,y) omuz/çıkış noktası, ang = yön (derece, 0 = sağ), reach = kol uzunluğu (bilek noktasına kadar).
    Kol kaftan yenli, bilekte açık renk manşet, ucu açık el (4 parmak + başparmak). Dönüş: parmak uçları noktası."""
    r = math.radians(ang)
    ex, ey = x + math.cos(r) * reach, y + math.sin(r) * reach
    nx, ny = -math.sin(r), math.cos(r)
    w0, w1 = 15 * s, 10 * s
    pts = [(x + nx * w0, y + ny * w0), (ex + nx * w1, ey + ny * w1), (ex - nx * w1, ey - ny * w1), (x - nx * w0, y - ny * w0)]
    p = path_pts(pts)
    c.drawPath(p, P(sleeve, a))
    INKP(c, p, 1.8, 215)
    # kıvrım çizgileri
    for k in (0.3, 0.55, 0.8):
        px_, py_ = x + (ex - x) * k, y + (ey - y) * k
        wk = lerp(w0, w1, k) * 0.85
        c.drawLine(px_ + nx * wk, py_ + ny * wk, px_ - nx * wk * 0.2, py_ - ny * wk * 0.2, S("#0E0804", 1.3, 80))
    # manşet
    cw = 12 * s
    cp = path_pts([(ex - math.cos(r) * cw + nx * w1 * 1.06, ey - math.sin(r) * cw + ny * w1 * 1.06), (ex + nx * w1 * 1.06, ey + ny * w1 * 1.06),
                   (ex - nx * w1 * 1.06, ey - ny * w1 * 1.06), (ex - math.cos(r) * cw - nx * w1 * 1.06, ey - math.sin(r) * cw - ny * w1 * 1.06)])
    c.drawPath(cp, P(cuff, a))
    INKP(c, cp, 1.4, 200)
    # el
    hl = 34 * s
    c.save()
    c.translate(ex, ey)
    c.rotate(ang)
    pm = skia.Path()
    pm.moveTo(0, -w1 * 0.95)
    pm.cubicTo(hl * 0.35, -w1 * 1.25, hl * 0.62, -w1 * 1.05, hl * 0.74, -w1 * 0.45)
    pm.lineTo(hl * 0.74, w1 * 0.55)
    pm.cubicTo(hl * 0.55, w1 * 1.20, hl * 0.28, w1 * 1.25, 0, w1 * 0.95)
    pm.close()
    c.drawPath(pm, P(col, a))
    INKP(c, pm, 1.5, 210)
    if fingers:
        for i in range(4):
            fy_ = -w1 * 0.80 + i * w1 * 0.52
            fo = open_ * (i - 1.5) * 5.0 * s
            fp = skia.Path()
            fp.moveTo(hl * 0.62, fy_)
            fp.quadTo(hl * 0.95, fy_ + fo * 0.5, hl * 1.14, fy_ + fo)
            c.drawPath(fp, S(col, 7.2 * s, a))
            c.drawPath(fp, S("#2A1608", 1.2, 140))
        tp = skia.Path()
        tp.moveTo(hl * 0.22, -w1 * 0.88)
        tp.quadTo(hl * 0.58, -w1 * 1.75 - open_ * 6, hl * 0.90, -w1 * 1.40 - open_ * 9)
        c.drawPath(tp, S(col, 8.0 * s, a))
        c.drawPath(tp, S("#2A1608", 1.2, 140))
    c.restore()
    return ex + math.cos(r) * hl * 1.05, ey + math.sin(r) * hl * 1.05


def draw_loaf(c, x, y, s=1.0, a=255, bit=0.0, crumbs=True):
    """Yuvarlak ekmek somunu (yandan): kabuk çizgileri; bit: ısırık büyüklüğü 0..1 (sağ üst yamaçtan)."""
    w, h = 112 * s, 62 * s
    p = skia.Path()
    p.moveTo(x - w, y)
    p.cubicTo(x - w * 0.98, y - h * 1.35, x + w * 0.98, y - h * 1.35, x + w, y)
    p.cubicTo(x + w * 0.9, y + h * 0.40, x - w * 0.9, y + h * 0.40, x - w, y)
    p.close()
    c.saveLayer(skia.Rect.MakeLTRB(x - w - 20, y - h * 1.6, x + w + 20, y + h * 0.7), None)
    c.drawPath(p, P("#8B5A2B", a))
    c.save()
    c.clipPath(p, skia.ClipOp.kIntersect, True)
    sh = skia.GradientShader.MakeLinear([(x - w * 0.5, y - h * 1.2), (x + w * 0.7, y + h * 0.4)], [C("#E2B26E", a), C("#B07838", a), C("#6E4220", a)], [0.0, 0.5, 1.0])
    c.drawRect(skia.Rect.MakeLTRB(x - w, y - h * 1.5, x + w, y + h * 0.6), skia.Paint(Shader=sh, AntiAlias=True))
    for i in range(3):
        xx = x - w * 0.55 + i * w * 0.55
        sc = skia.Path()
        sc.moveTo(xx - 18 * s, y - h * 0.95)
        sc.quadTo(xx, y - h * 0.62, xx + 22 * s, y - h * 0.15)
        c.drawPath(sc, S("#4A2A10", 3.2 * s, 150))
        c.drawPath(sc, S("#F0CE90", 1.6 * s, 120))
    c.restore()
    INKP(c, p, 2.0, 220)
    if bit > 0.01:
        br = bit * 46 * s
        bx, by = x + w * 0.72, y - h * 0.62
        c.drawCircle(bx, by, br, skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kClear))
        # ısırık kenarı (iç ekmek) + diş izleri
        c.save()
        c.clipPath(p, skia.ClipOp.kIntersect, True)
        c.drawCircle(bx, by, br + 4 * s, S("#F2DDB0", 5 * s, a))
        c.drawCircle(bx, by, br + 6 * s, S("#2A1A0C", 1.6, 200))
        c.restore()
    c.restore()
    if crumbs:
        rs = _RS(5)
        n = 7 + int(10 * bit)
        for i in range(n):
            c.drawCircle(x + rs.uniform(-w * 1.05, w * 1.05) + (w * 0.4 if i > 6 else 0), y + h * 0.30 + rs.uniform(-3, 10), rs.uniform(1.4, 2.8) * s, P("#C89A5A", 190))


def draw_bowl(c, x, y, s=1.0, a=255, fill="#7A5A3A", steam=None, t=0.0):
    """Çorba kâsesi (yandan, ahşap/pişmiş toprak) + isteğe bağlı buhar."""
    w, h = 78 * s, 34 * s
    p = skia.Path()
    p.moveTo(x - w, y - h * 0.55)
    p.cubicTo(x - w * 0.95, y + h * 0.9, x + w * 0.95, y + h * 0.9, x + w, y - h * 0.55)
    p.close()
    c.drawPath(p, P("#9A6A3A", a))
    FILLP(c, p, "#9A6A3A", a, 1.8, 220, shader=skia.GradientShader.MakeLinear([(x - w, y - h), (x + w, y + h)], [C("#C89460", a), C("#8A5A2E", a), C("#4E3016", a)], [0.0, 0.5, 1.0]))
    c.drawOval(skia.Rect.MakeLTRB(x - w, y - h * 0.80, x + w, y - h * 0.30), P(fill, a))
    c.drawOval(skia.Rect.MakeLTRB(x - w, y - h * 0.80, x + w, y - h * 0.30), S("#2A1A0C", 1.6, 210))
    if steam is not None:
        for i in range(3):
            ph = (t * 0.5 + i * 0.33 + steam) % 1.0
            sx = x + (i - 1) * 24 * s + math.sin(ph * 6 + i) * 8 * s
            sy = y - h * 0.8 - ph * 90 * s
            SOFT(c, sx, sy, 15 * s * (0.8 + ph), 20 * s * (0.8 + ph), "#FFFFFF", 70 * (1 - ph))


def draw_spoon(c, x, y, ang=-30.0, s=1.0, a=255):
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.drawLine(0, 0, 82 * s, 0, S("#6A4A2A", 7 * s, a))
    c.drawLine(0, 0, 82 * s, 0, S("#2A1A0C", 1.0, 140))
    c.drawOval(skia.Rect.MakeLTRB(-22 * s, -12 * s, 6 * s, 12 * s), P("#9A6A3A", a))
    c.drawOval(skia.Rect.MakeLTRB(-22 * s, -12 * s, 6 * s, 12 * s), S("#2A1A0C", 1.3, 200))
    c.restore()


def draw_slip(c, x, y, w=120, h=76, rot=0.0, a=255, lines=3, seed=1, tone="#EFE3C2", glow=0.0, curl=0.0):
    """Küçük kâğıt pusulası (el yazısı satırları okunmaz çizgiler). (x,y) merkez."""
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    if glow > 0.01:
        SOFT(c, 0, 0, w * 1.1, h * 1.1, "#FFE8A0", 190 * glow)
    sh = skia.Path()
    sh.addRect(skia.Rect.MakeLTRB(-w / 2 + 6, -h / 2 + 9, w / 2 + 6, h / 2 + 9))
    c.drawPath(sh, skia.Paint(Color=C("#000000", int(60 * a / 255)), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 5)))
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2 + curl * 4), (w / 2 - 3, h / 2), (-w / 2 + 2, h / 2 - curl * 3)]
    p = path_pts(pts)
    c.drawPath(p, P(tone, a))
    INKP(c, p, 1.4, 190)
    rs = _RS(seed)
    for i in range(lines):
        yy = -h / 2 + 15 + i * (h - 26) / max(1, lines)
        L = w * rs.uniform(0.45, 0.82)
        wp = skia.Path()
        wp.moveTo(-w / 2 + 12, yy)
        n = int(L / 9)
        for j in range(n):
            wp.quadTo(-w / 2 + 12 + j * 9 + 4.5, yy + rs.uniform(-4.5, 4.5), -w / 2 + 12 + (j + 1) * 9, yy + rs.uniform(-1.5, 1.5))
        c.drawPath(wp, S("#3A2616", 1.5, 190 * a / 255))
    c.restore()


def draw_bag(c, x, y, s=1.0, a=255, fill=0.0, col="#7A4A28", tie="#C79A3C", seed=1, sway=0.0, slips=0, mark=None):
    """Deri torba (borsa): yuvarlak karınlı, boğazdan bağlı; slips: ağzından görünen kâğıt uçları; mark: üstünde Medici işareti (palle) 0..1."""
    c.save()
    c.translate(x, y)
    c.rotate(sway)
    w, h = 58 * s, 76 * s
    p = skia.Path()
    p.moveTo(-w * 0.28, -h * 0.82)
    p.cubicTo(-w * 0.70, -h * 0.62, -w * 1.34, -h * 0.12, -w * 1.20, h * 0.66)
    p.cubicTo(-w * 1.15, h * 0.92, -w * 0.62, h * 1.00, 0, h * 1.00)
    p.cubicTo(w * 0.62, h * 1.00, w * 1.15, h * 0.92, w * 1.20, h * 0.66)
    p.cubicTo(w * 1.34, -h * 0.12, w * 0.70, -h * 0.62, w * 0.28, -h * 0.82)
    p.close()
    sh = skia.GradientShader.MakeRadial((-w * 0.3, -h * 0.2), w * 1.7, [C(mix(col, "#FFFFFF", 0.30), a), C(col, a), C(mix(col, "#000000", 0.5), a)], [0.0, 0.5, 1.0])
    c.drawPath(p, skia.Paint(Shader=sh, AntiAlias=True))
    INKP(c, p, 2.0, 220)
    # kırışıklık
    rs = _RS(seed)
    for i in range(5):
        yy = rs.uniform(-h * 0.5, h * 0.7)
        xa = rs.uniform(-w * 0.8, -w * 0.1)
        qp = skia.Path()
        qp.moveTo(xa, yy)
        qp.quadTo(xa + w * 0.4, yy + rs.uniform(-8, 8) * s, xa + w * rs.uniform(0.6, 1.1), yy + rs.uniform(-3, 5) * s)
        c.drawPath(qp, S("#2A1608", 1.2 * s, 70))
    # ağız (içi karanlık) + kâğıt uçları + kıvrık yaka + bağ
    mo = skia.Path()
    mo.addOval(skia.Rect.MakeLTRB(-w * 0.56, -h * 1.17, w * 0.56, -h * 1.05))
    c.drawPath(mo, P(mix(col, "#000000", 0.78), a))
    if slips:
        for i in range(slips):
            rr = _RS(seed * 5 + i)
            sx = rr.uniform(-w * 0.22, w * 0.22)
            c.save()
            c.translate(sx, -h * 1.08)
            c.rotate(rr.uniform(-0.5, 0.5))
            c.drawRect(skia.Rect.MakeLTRB(-8 * s, -24 * s, 8 * s, 6 * s), P("#EFE3C2", a))
            INKR(c, -8 * s, -24 * s, 8 * s, 6 * s, 0.9, 160)
            c.restore()
    fl = skia.Path()
    fl.moveTo(-w * 0.30, -h * 0.80)
    fl.quadTo(-w * 0.42, -h * 0.95, -w * 0.58, -h * 1.12)
    fl.quadTo(-w * 0.38, -h * 1.03, -w * 0.20, -h * 1.12)
    fl.quadTo(0, -h * 1.01, w * 0.20, -h * 1.12)
    fl.quadTo(w * 0.38, -h * 1.03, w * 0.58, -h * 1.12)
    fl.quadTo(w * 0.42, -h * 0.95, w * 0.30, -h * 0.80)
    fl.close()
    c.drawPath(fl, P(mix(col, "#000000", 0.18), a))
    INKP(c, fl, 1.5, 200)
    for fx in (-0.34, -0.12, 0.12, 0.34):
        c.drawLine(w * fx * 0.9, -h * 0.84, w * fx * 1.35, -h * 1.08, S("#2A1608", 1.0 * s, 90))
    c.drawLine(-w * 0.34, -h * 0.80, w * 0.34, -h * 0.80, S(tie, 6 * s, a))
    c.drawLine(-w * 0.34, -h * 0.80, w * 0.34, -h * 0.80, S("#2A1A0C", 0.9, 160))
    for sg in (-1, 1):
        cp = skia.Path()
        cp.moveTo(sg * w * 0.05, -h * 0.80)
        cp.quadTo(sg * w * 0.30, -h * 0.60, sg * w * 0.20, -h * 0.40)
        c.drawPath(cp, S(tie, 3.2 * s, a))
    c.drawCircle(0, -h * 0.80, 5.5 * s, P(tie, a))
    # yan dikiş
    sm = skia.Path()
    sm.moveTo(w * 0.70, -h * 0.20)
    sm.quadTo(w * 0.92, h * 0.28, w * 0.74, h * 0.86)
    c.drawLine(-w * 0.70, h * 0.88, w * 0.70, h * 0.88, S("#2A1608", 1.2 * s, 90))
    c.drawPath(sm, S("#2A1608", 1.2 * s, 110))
    if mark and mark > 0.02:
        sc = s * 0.55 * mark
        CM.mini_palle(f_dummy(c), 0, h * 0.18, 56 * sc * 2.0, color="#8A2A1E", alpha=0.85)
    c.restore()


class _Dummy:
    """CM.mini_palle `f.circle` ister; tuvale yönlendiren ince kabuk."""

    def __init__(self, c):
        self.c = c

    def circle(self, x, y, r, color="#000", alpha=1.0, **kw):
        self.c.drawCircle(x, y, r, P(color, 255 * alpha))


def f_dummy(c):
    return _Dummy(c)


def draw_egg(c, x, y, s=1.0, tilt=0.0, a=255, shadow=True, crack=0.0, col="#F4EAD2"):
    """Yumurta (yandan, sivri ucu yukarı; tilt radyan; taban (x,y)). crack: taban kırılması 0..1 (düz taban)."""
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(tilt))
    h, w = 62 * s, 44 * s
    if shadow:
        SOFT(c, 6 * s, 2, w * 0.95, 8 * s, "#000000", 90 * a / 255)
    p = skia.Path()
    p.moveTo(0, 0)
    flat = crack * 14 * s
    p.cubicTo(-w * 0.95, -h * 0.05, -w * 1.05, -h * 1.15, 0, -h * 1.18)
    p.cubicTo(w * 1.05, -h * 1.15, w * 0.95, -h * 0.05, 0, 0)
    p.close()
    if flat > 0.1:
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(-w * 2, -h * 2, w * 2, -flat))
    sh = skia.GradientShader.MakeRadial((-w * 0.30, -h * 0.80), w * 1.5, [C(mix(col, "#FFFFFF", 0.6), a), C(col, a), C(mix(col, "#7A6038", 0.5), a)], [0.0, 0.5, 1.0])
    c.drawPath(p, skia.Paint(Shader=sh, AntiAlias=True))
    INKP(c, p, 1.8, 210)
    if flat > 0.1:
        c.restore()
        # kırık taban çizgisi
        c.drawLine(-w * 0.70, -flat, w * 0.70, -flat, S("#2A1A0C", 2.0, 220))
        zp = skia.Path()
        zp.moveTo(-w * 0.70, -flat)
        for k in range(1, 6):
            zp.lineTo(-w * 0.70 + k * w * 1.4 / 5, -flat + (4 if k % 2 else -1) * s)
        c.drawPath(zp, S("#2A1A0C", 1.2, 180))
    c.restore()


def draw_coin_flat(c, x, y, r=18.0, a=255, rot=0.0):
    """Altın florin (üstten, basit): ışıltılı yuvarlak + zambak benzeri iz."""
    sh = skia.GradientShader.MakeRadial((x - r * 0.3, y - r * 0.3), r * 1.5, [C("#FFF0A8", a), C("#E0B040", a), C("#8A6420", a)], [0.0, 0.5, 1.0])
    c.drawCircle(x, y, r, skia.Paint(Shader=sh, AntiAlias=True))
    c.drawCircle(x, y, r, S("#4A3410", 1.4, 220))
    c.drawCircle(x, y, r * 0.66, S("#8A6420", 1.0, 170))
    c.drawLine(x, y - r * 0.42, x, y + r * 0.38, S("#7A5418", 2.0, 170))
    c.drawLine(x - r * 0.28, y - r * 0.12, x + r * 0.28, y - r * 0.12, S("#7A5418", 1.6, 170))


def coin_stack(c, x, y, n, r=34.0, a=255, ph=0.0, tilt=0.0, gap=7.0):
    """Altın sikke yığını (yandan): n sikke alt alta; (x,y) taban."""
    for i in range(int(n)):
        yy = y - i * gap
        jit = math.sin(i * 2.7 + ph) * 1.8
        c.drawOval(skia.Rect.MakeLTRB(x - r + jit, yy - r * 0.30, x + r + jit, yy + r * 0.30), P("#B08828", a))
        c.drawOval(skia.Rect.MakeLTRB(x - r + jit, yy - r * 0.30 - 3, x + r + jit, yy + r * 0.30 - 3), P("#E8C25A", a))
        c.drawOval(skia.Rect.MakeLTRB(x - r + jit, yy - r * 0.30 - 3, x + r + jit, yy + r * 0.30 - 3), S("#4A3410", 1.1, 200))


# ───────────────────────────── sahne yardımcıları ─────────────────────────────
def night_pool(cx, x, y, r=900.0, seed=0):
    return CM.candle_light(cx.t, seed, base=(x, y), r=r, sway=10.0)


def sil(f, kind, x, y, h, t, action="idle", dir=1, seed=0, color="#1A1008", rim="#E8A860", rim_dir=1, **kw):
    """Siluet figür (yüz yok) kısayolu."""
    OD.sil_actor(f, kind, x, y, h, t, action=action, dir=dir, seed=seed, color=color, rim=rim, rim_dir=rim_dir, **kw)


def walker(f, kind, x, y, h, t, speed=90.0, dir=1, phase=0.0, seed=0, **kw):
    FA.walker(f, kind, x, y, h, t, speed=speed, dir=dir, phase=phase, seed=seed, **kw)


def actor(f, kind, x, y, h, t, action="idle", dir=1, seed=0, phase=0.0, **kw):
    FA.actor(f, kind, x, y, h, t, action=action, dir=dir, seed=seed, phase=phase, **kw)


def stone_wall(c, xa, xb, y0, y1, T, col="#8E8A80", course=64.0, seed=3):
    """Taş duvar: zemin dolgusu + OD.ashlar (mutlak koordinat)."""
    c.drawRect(skia.Rect.MakeLTRB(xa, y0, xb, y1), P(T(col)))
    OD.ashlar(c, xa, xb, y0, y1, T, col=col, course=course, seed=seed)


# ───────────────────────────── sahne iskeleti ─────────────────────────────
def begin(cx, bg="wall", seed=0, dress=None, push=0.0, drift=(0.0, 0.0), clear="#0B0A08", mono=0.0):
    """Özel tür iskeleti: arka plan (duvar/siyah) + kamera dönüşü. mono>0 → gravür katmanı açılır (duvar dâhil). Dönüş: (f, c, cam)."""
    f = cx.f
    if mono > 0.001:
        mono_begin(f, mono)
    cam = CM.Cam(cx, push=push, drift=drift)
    if bg == "wall":
        CM.bgfill(f, cx, seed=seed, cam=cam, dress=dress)
    else:
        f.clear(clear)
    cam.begin(f)
    return f, f.c, cam


def end(cx, cam, mono=0.0, motes_n=26, light=None, vig_s=None, dust=True):
    cam.end(cx.f)
    if mono > 0.001:
        mono_end(cx.f)
    CM.finish(cx.f, cx, motes_n=motes_n, light=light, vig_s=vig_s, dust=dust)


def grid_floor(c, x0, x1, y0, y1, col1="#CDBB92", col2="#A8946A", lines=True, seed=3):
    """Düz zemin şeridi (fresk zemini): degrade + ince derz çizgileri."""
    GRAD_V(c, x0, y0, x1, y1, [(col1, 0.0), (col2, 1.0)])
    c.drawLine(x0, y0, x1, y0, S("#2A1A0C", 2.0, 170))
    if lines:
        rs = _RS(seed)
        y = y0
        step = 18.0
        while y < y1:
            y += step
            step *= 1.18
            c.drawLine(x0, y, x1, y, S("#2A1A0C", 1.0, 60))
        for i in range(int((x1 - x0) / 150)):
            xx = x0 + i * 150 + rs.uniform(-8, 8)
            c.drawLine(xx, y0, xx - (xx - (x0 + x1) / 2) * 0.12, y1, S("#2A1A0C", 1.0, 45))


# ───────────────────────────── bildirimli bindirme (overlay) + stok türlerin sarmalayıcıları ─────────────────────────────
def draw_over(cx, over):
    """over = [dict(t="tag"|"stamp"|"date"|"engr"|"kick"|"counter", …)] — çapaya bağlı bindirmeler (stok türün üstüne, ışıktan SONRA çizilir)."""
    f = cx.f
    for o in over or ():
        t_ = o.get("t")
        if t_ == "tag":
            tag(f, cx, o["text"], o["x"], o["y"], at=o["at"], size=o.get("size", 34), face=o.get("face", "title_m"), track=o.get("track", 6.0), sub=o.get("sub"), w=o.get("w"),
                hold=o.get("hold"), off=o.get("off", 0.0))
        elif t_ == "stamp":
            stamp_at(f, cx, o["text"], o["x"], o["y"], o["at"], rot=o.get("rot", -0.10), size=o.get("size", 50), color=o.get("color"), hold=o.get("hold"), off=o.get("off", 0.0))
        elif t_ == "date":
            date_plate(f, cx, o["text"], o["at"], x=o.get("x", 96), y=o.get("y", 860), size=o.get("size", 50))
        elif t_ == "engr":
            engr(f, cx, o["text"], o["x"], o["y"], o["at"], size=o.get("size", 70), track=o.get("track", 10.0), style=o.get("style", "engraved"), dur=o.get("dur", 1.0), face=o.get("face", "title"),
                 off=o.get("off", 0.0), alpha=(1.0 - cx.amt(o["hold"], 0.5)) if o.get("hold") is not None else 1.0, color=o.get("color"), glow=o.get("glow", 0.0))
        elif t_ == "kick":
            k = cx.amt(o["at"], 0.7, off=o.get("off", 0.0))
            if o.get("hold") is not None:
                k *= 1.0 - cx.amt(o["hold"], 0.5)
            CM.kick(f, o["text"], o.get("x", W / 2), o.get("y", 128), alpha=k, size=o.get("size", 32), track=o.get("track", 12))
        elif t_ == "palle":
            import cilt_props as CP
            k = cx.amt(o["at"], 0.6, off=o.get("off", 0.0))
            if o.get("hold") is not None:
                k *= 1.0 - cx.amt(o["hold"], 0.5)
            if k > 0.003:
                CP.draw_arms(f, o["x"], o["y"], o.get("size", 160) * (0.9 + 0.1 * ease_out(k)), alpha=k, shadow=0.6, glow=o.get("glow", 0.2) * k, glint=None)
        elif t_ == "strike":
            k = ease_io(cx.amt(o["at"], o.get("dur", 0.5), off=o.get("off", 0.0)), 2)
            if k > 0.003:
                x, y, r = o["x"], o["y"], o.get("size", 90)
                pp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=o.get("w", 11.0), Color=C("#8E2A1E", 235), StrokeCap=skia.Paint.kRound_Cap)
                pp.setPathEffect(skia.DiscretePathEffect.Make(9.0, 1.6, 4))
                f.c.drawLine(x - r, y - r, lerp(x - r, x + r, min(1.0, k * 2)), lerp(y - r, y + r, min(1.0, k * 2)), pp)
                if k > 0.5:
                    kk = (k - 0.5) * 2
                    f.c.drawLine(x + r, y - r, lerp(x + r, x - r, kk), lerp(y - r, y + r, kk), pp)
        elif t_ == "icon":
            import icons as _ic
            k = cx.amt(o["at"], 0.5, off=o.get("off", 0.0))
            if o.get("hold") is not None:
                k *= 1.0 - cx.amt(o["hold"], 0.5)
            if k > 0.003:
                _ic.draw_icon(f, o["name"], o["x"], o["y"] + o.get("bob", 0.0) * math.sin(cx.t * 2.0), size=o.get("size", 100) * (0.8 + 0.2 * ease_out(k)), metal=o.get("metal", "gold"), alpha=k, shadow=o.get("shadow", True), glow=o.get("glow", 0.0))
        elif t_ == "counter":
            k = clamp((cx.t - cx.at(o["at"])) / o.get("dur", 1.6))
            if k <= 0:
                continue
            v = o["value"] * ease_out(k, 3)
            txt = o.get("prefix", "") + CM.fmt_int(v) + o.get("suffix", "")
            size = o.get("size", 96)
            a = smooth(k * 6)
            sp = CM.engraved(txt, "title", int(size), 6.0, TH.fg) if TH.day else CM.gilt(txt, "title", int(size), 6.0)
            CM.draw_spr(f, sp, o["x"], o["y"], "c", alpha=a, shadow=0.5 if not TH.day else 0.0)
            if o.get("unit"):
                CM.ink(f, o["unit"], o["x"], o["y"] + size * 0.62, face="title_m", size=size * 0.30, color=TH.acc, align="c", track=10, alpha=a, emboss=False)


def _register_wrappers():
    import shots as SH
    import cilt_cam

    def mk(base):
        def fn(cx, over=(), **kw):
            SH.KINDS[base](cx, **kw)
            draw_over(cx, over)
        fn.__name__ = "k_p2_" + base
        SH.KINDS["p2_" + base] = fn
        if base in cilt_cam.OWN_CAMERA or base in ("oda", "sehir"):
            cilt_cam.OWN_CAMERA.add("p2_" + base)
    for b in ("oda", "sehir", "pano", "build", "map", "procession", "ledger", "letter", "doc", "quote", "counter", "stacked", "network", "timeline", "frieze", "skyline", "medal", "palle", "emblem", "coin", "title"):
        if b in SH.KINDS:
            mk(b)


_register_wrappers()


# ───────────────────────────── özel figür eylemleri (FA.ACTIONS'a eklenir) ─────────────────────────────
def _prop_local(layer, fn):
    return (layer, fn)


def act_give(kit, T, phase=0.0, t0=0.5, dur=0.9, hold=1.2, slip=True, reach=0.31, **_):
    """Uzat (ver): yakın kol öne uzanır; elde küçük kâğıt pusulası; hold sn bekler; geri çeker (slip elden çıkınca çizilmez)."""
    hb = kit.B["hb"]
    u = (T - t0)
    k = FA.ease5(clamp(u / dur)) * (1.0 - FA.ease5(clamp((u - dur - hold) / dur)))

    def arms(sho):
        n0 = FA._relaxed(sho, hb, T, phase * 6.28, "n")
        tgt = (sho[0] + reach * hb, sho[1] + 0.07 * hb + 0.004 * hb * math.sin(T * 2.0))
        a = ("ik", (lerp(n0[1][0], tgt[0], k), lerp(n0[1][1], tgt[1], k)))
        return FA._relaxed(sho, hb, T, phase * 6.28, "f"), a, "open", "open"
    p = FA.stand(kit, T, phase, arms=arms, tor_add=2.0 * k, head_add=-2.0 * k)
    if slip and k > 0.02 and u < dur + hold + 0.05:
        w = p.arms[1][2]
        p.props.append(("near", lambda c, w=w: draw_slip(c, w[0] + 0.045 * hb, w[1] - 0.012 * hb, w=0.23 * hb, h=0.15 * hb, rot=-0.08, lines=2, seed=3)))
    return p


def act_take(kit, T, phase=0.0, t0=0.5, dur=0.9, hold=9.0, got_at=None, reach=0.31, slip=True, **_):
    """Al: yakın kol öne uzanır (açık avuç); got_at anından sonra elde pusula görünür."""
    hb = kit.B["hb"]
    u = (T - t0)
    k = FA.ease5(clamp(u / dur)) * (1.0 - FA.ease5(clamp((u - dur - hold) / dur)))

    def arms(sho):
        n0 = FA._relaxed(sho, hb, T, phase * 6.28, "n")
        tgt = (sho[0] + reach * hb, sho[1] + 0.07 * hb)
        a = ("ik", (lerp(n0[1][0], tgt[0], k), lerp(n0[1][1], tgt[1], k)))
        return FA._relaxed(sho, hb, T, phase * 6.28, "f"), a, "open", "open"
    p = FA.stand(kit, T, phase, arms=arms, tor_add=1.5 * k)
    if slip and got_at is not None and T >= got_at and k > 0.02:
        w = p.arms[1][2]
        p.props.append(("near", lambda c, w=w: draw_slip(c, w[0] + 0.04 * hb, w[1] - 0.012 * hb, w=0.23 * hb, h=0.15 * hb, rot=-0.08, lines=2, seed=3)))
    return p


def act_taste(kit, T, phase=0.0, t0=0.0, period=2.4, bowl=True, **_):
    """Tat (kâse + kaşık): sol (uzak) el kâseyi tutar; sağ el kaşığı kâseye daldırır, ağıza götürür, indirir. period: bir tur."""
    hb = kit.B["hb"]
    u = ((T - t0) / period) % 1.0 if T >= t0 else 0.0
    active = T >= t0
    bowl_pt = (0.20, 0.19)
    mouth_pt = (0.075, -0.115)
    rest_pt = (0.04, 0.27)
    if not active:
        kk = (0.0, 0.0, 0.0)
    if u < 0.30:
        a = FA.ease5(u / 0.30)
        tgt = (lerp(rest_pt[0], bowl_pt[0], a), lerp(rest_pt[1], bowl_pt[1], a))
    elif u < 0.52:
        tgt = bowl_pt
    elif u < 0.74:
        a = FA.ease5((u - 0.52) / 0.22)
        tgt = (lerp(bowl_pt[0], mouth_pt[0], a), lerp(bowl_pt[1], mouth_pt[1], a))
    elif u < 0.88:
        tgt = mouth_pt
    else:
        a = FA.ease5((u - 0.88) / 0.12)
        tgt = (lerp(mouth_pt[0], rest_pt[0], a), lerp(mouth_pt[1], rest_pt[1], a))
    if not active:
        tgt = rest_pt

    def arms(sho):
        far_t = (sho[0] + bowl_pt[0] * hb + 0.02 * hb, sho[1] + bowl_pt[1] * hb + 0.04 * hb) if (active and bowl) else FA._relaxed(sho, hb, T, phase * 6.28, "f")[1]
        return ("ik", far_t), ("ik", (sho[0] + tgt[0] * hb, sho[1] + tgt[1] * hb)), "open", "fist"
    hd = -4.0 * (1.0 if 0.60 < u < 0.82 else 0.0)
    p = FA.stand(kit, T, phase, arms=arms, head_add=hd if active else 0.0)
    if active and bowl:
        wf = p.arms[0][2]
        wn = p.arms[1][2]
        p.props.append(("far", lambda c, w=wf: draw_bowl(c, w[0] + 0.02 * hb, w[1] + 0.02 * hb, s=0.40, fill="#6A4A2A")))
        p.props.append(("near", lambda c, w=wn: draw_spoon(c, w[0], w[1], ang=-30 - 20 * (1 if u < 0.5 else 0), s=0.55)))
    return p


FA.ACTIONS.update(give=act_give, take=act_take, taste=act_taste)


# ───────────────────────────── oturan figür eylemleri (OD.SEATED_ACTS'a eklenir) ─────────────────────────────
def act_sit_eat(kit, T, phase=0.0, t0=0.0, period=1.4, from_x=0.40, **_):
    """Oturan: yakın el masadaki somundan (from_x·hb) lokma alıp ağza götürür, çiğner; far el masada."""
    hb = kit.B["hb"]
    ph = phase * 6.283
    active = T >= t0
    u = ((T - t0) / period) % 1.0 if active else 0.0
    mouth = (0.215, -0.700)
    loaf = (from_x, FA.DESK_Y - 0.012)
    rest = (0.33, FA.DESK_Y - 0.004)
    if not active:
        tgt = rest
    elif u < 0.28:
        a = FA.ease5(u / 0.28)
        tgt = (lerp(rest[0], loaf[0], a), lerp(rest[1], loaf[1], a))
    elif u < 0.42:
        tgt = loaf
    elif u < 0.62:
        a = FA.ease5((u - 0.42) / 0.20)
        tgt = (lerp(loaf[0], mouth[0], a), lerp(loaf[1], mouth[1], a))
    elif u < 0.78:
        tgt = mouth
    else:
        a = FA.ease5((u - 0.78) / 0.22)
        tgt = (lerp(mouth[0], rest[0], a), lerp(mouth[1], rest[1], a))

    def arms(sho):
        return ("ik", (0.22 * hb, (FA.DESK_Y - 0.003) * hb)), ("ik", (tgt[0] * hb, tgt[1] * hb)), "open", "fist"
    chew = 1.2 * math.sin(T * 14) if (active and 0.62 < u < 0.85) else 0.0
    p = FA._sit_base(kit, T, phase, 6.0 - 3.0 * (1.0 if 0.5 < u < 0.8 else 0.0), 14.0 + chew, arms)
    if active and 0.05 < u < 0.74:
        w = p.arms[1][2]
        p.props.append(("near", lambda c, w=w: draw_bread_piece(c, w[0] + 0.012 * hb, w[1] - 0.008 * hb, 0.07 * hb)))
    p.extra = None
    return p


def act_sit_fear(kit, T, phase=0.0, t0=0.0, **_):
    """Oturan korku: gövde geri çekilir, iki el yukarı (savunma), baş geri."""
    hb = kit.B["hb"]
    ph = phase * 6.283
    k = FA.ease5(clamp((T - t0) / 0.5))
    tr = math.sin(T * 21.0) * 0.004 * k

    def arms(sho):
        far = ("ik", (lerp(0.22, 0.30, k) * hb, lerp(FA.DESK_Y - 0.003, -0.60, k) * hb))
        near = ("ik", ((lerp(0.33, 0.40, k) + tr) * hb, lerp(FA.DESK_Y - 0.004, -0.63, k) * hb))
        return far, near, "open", "open"
    p = FA._sit_base(kit, T, phase, lerp(5.0, -7.0, k), lerp(14.0, 4.0, k), arms)
    p.extra = None
    return p


def draw_bread_piece(c, x, y, s):
    p = skia.Path()
    p.addOval(skia.Rect.MakeLTRB(x - s * 0.55, y - s * 0.40, x + s * 0.55, y + s * 0.40))
    c.drawPath(p, P("#C89A5A"))
    c.drawPath(p, S("#3A2410", 1.2, 200))


OD.seated_act("write")
OD.SEATED_ACTS.update(eat=act_sit_eat, fear=act_sit_fear)
