"""c5_kinds — c5 «Konsil, Kitap, Platon» özel çekim türleri (Parça 2 sahne yazarı). `scenes_c5.py` içinde import edilir; `@CM.ckind` ile kaydolur.

Dünya koordinatı = nötr kamerada ekran koordinatı (1920×1080). Kamera: `cam=[(çapa, look(wx, wy, z)), …]`.
Kaynak disiplini: yüz yok (siluet), şiddet yok; konsil mekân/tören betimi YOK (brif §10); yalnız söylenen adlar/sayılar.
Ortak yardımcılar `p2_lib` (L), `c3_kinds` (K3) ve `c4_kinds` (K4) içindedir.
"""
import math

import numpy as np
import skia

import cilt_city as CT
import cilt_medici as CM
import cilt_sehir as SE
import icons
import p2_lib as L
import sk
import c3_kinds as K3
import c4_kinds as K4
from cilt_medici import TH
from p2_lib import (INK, P, S, GRAD_V, INKP, INKR, LINE, OVAL, POLY, R, RA, SOFT, FILLP, PT, STK, _RS, bake, blit, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth)
from c3_kinds import look, table_persp, dashed, arm_to, draw_palle_badge, PP_sheet, PP_hand
from c4_kinds import draw_calendar, draw_cross, draw_check, draw_bubble, draw_palazzo, draw_key, draw_shelf, draw_book_block
from sk import C, H, W


# ───────────────────────────── ortak küçük çizimler ─────────────────────────────
def draw_plague_cloud(c, x, y, s=1.0, a=255, t=0.0):
    """Veba korkusu: yeşilimsi bulut + benekler (şiddet/ceset yok)."""
    for i, (dx, dy, r) in enumerate(((-60, 10, 54), (0, -14, 70), (62, 8, 56), (-24, 36, 46), (34, 38, 48))):
        dr = 4 * math.sin(t * 1.8 + i)
        c.drawCircle(x + dx * s, y + dy * s + dr, r * s, P("#9AA878", a))
    for i, (dx, dy, r) in enumerate(((-60, 10, 54), (0, -14, 70), (62, 8, 56))):
        c.drawCircle(x + dx * s, y + dy * s, r * s, S("#4A5A38", 2.0, a))
    rs = _RS(3)
    for i in range(10):
        c.drawCircle(x + rs.uniform(-80, 80) * s, y + rs.uniform(-30, 50) * s, rs.uniform(3, 6) * s, P("#3A4A28", int(a * 0.8)))


def draw_lyre(c, x, y, s=1.0, a=255, t=0.0, glow=0.0):
    """Orfik lir (yeniden çizim): iki kıvrık kol + çapraz kiriş + teller."""
    if glow > 0.01:
        SOFT(c, x, y, 130 * s, 150 * s, "#FFD060", 120 * glow)
    for sg in (-1, 1):
        p = skia.Path()
        p.moveTo(x + sg * 30 * s, y + 90 * s)
        p.cubicTo(x + sg * 120 * s, y + 60 * s, x + sg * 130 * s, y - 40 * s, x + sg * 80 * s, y - 120 * s)
        c.drawPath(p, S("#8A5A38", 14 * s, a))
        c.drawPath(p, S("#2A1A0C", 2.0, a))
        c.drawCircle(x + sg * 80 * s, y - 120 * s, 11 * s, P("#C79A3C", a))
    c.drawLine(x - 82 * s, y - 112 * s, x + 82 * s, y - 112 * s, S("#C79A3C", 10 * s, a))
    c.drawPath(sk.poly_path([(x - 52 * s, y + 80 * s), (x + 52 * s, y + 80 * s), (x + 36 * s, y + 118 * s), (x - 36 * s, y + 118 * s)]), P("#6E4524", a))
    for i in range(7):
        xx = x + (i - 3) * 22 * s
        c.drawLine(xx, y - 112 * s, xx * 0.9 + x * 0.1, y + 82 * s, S("#F4E9CB", 1.8, int(a * 0.9)))


def draw_tiny_crowd(c, x0, y0, w, h, n, t, seed=3, a=255, bob=2.0, col="#2A1C10", flip=1):
    """Çok sayıda minik figür (baş + gövde): tek yol, hızlı. Dikdörtgen dağılım; x0,y0 sol-üst."""
    rs = _RS(seed)
    heads = skia.Path()
    bodies = skia.Path()
    cols_ = max(1, int(math.sqrt(n * w / max(h, 1.0))))
    rows_ = max(1, int(math.ceil(n / cols_)))
    k = 0
    for r in range(rows_):
        for q in range(cols_):
            if k >= n:
                break
            fx = x0 + (q + 0.5 + rs.uniform(-0.3, 0.3)) * w / cols_
            fy = y0 + (r + 0.5 + rs.uniform(-0.25, 0.25)) * h / rows_ + bob * math.sin(t * 6.0 + k * 1.3)
            sc = 0.8 + 0.5 * (r / max(1, rows_ - 1))
            heads.addCircle(fx, fy - 15 * sc, 4.6 * sc)
            bodies.moveTo(fx - 6 * sc, fy + 6 * sc)
            bodies.lineTo(fx, fy - 10 * sc)
            bodies.lineTo(fx + 6 * sc, fy + 6 * sc)
            bodies.close()
            k += 1
    c.drawPath(bodies, skia.Paint(AntiAlias=True, Color=C(col, a)))
    c.drawPath(heads, skia.Paint(AntiAlias=True, Color=C(col, a)))


def draw_church_east(c, x, yb, s=1.0, a=255, dim=0.0):
    """Doğu kilisesi (yeniden çizim): kare gövde + büyük kubbe + yunan haçı."""
    cl = lambda col: mix(col, "#5A4A34", dim * 0.5)
    R(c, x - 160 * s, yb - 170 * s, x + 160 * s, yb, cl("#E3D3AE"), a)
    INKR(c, x - 160 * s, yb - 170 * s, x + 160 * s, yb, 2.4, 230)
    dp = skia.Path()
    dp.moveTo(x - 120 * s, yb - 170 * s)
    dp.cubicTo(x - 120 * s, yb - 340 * s, x + 120 * s, yb - 340 * s, x + 120 * s, yb - 170 * s)
    dp.close()
    c.drawPath(dp, P(cl("#C65B33"), a))
    INKP(c, dp, 2.2, 230)
    for i in range(1, 5):
        c.drawLine(x - 120 * s + i * 48 * s, yb - 170 * s, x + (i - 2.5) * 12 * s, yb - 300 * s, S("#5A2412", 1.2, 110))
    c.drawLine(x, yb - 320 * s, x, yb - 380 * s, S("#C79A3C", 6 * s, a))
    c.drawLine(x - 22 * s, yb - 358 * s, x + 22 * s, yb - 358 * s, S("#C79A3C", 6 * s, a))
    c.drawLine(x - 16 * s, yb - 340 * s, x + 16 * s, yb - 340 * s, S("#C79A3C", 4 * s, a))
    for sg in (-1, 0, 1):
        pth = skia.Path()
        pth.moveTo(x + sg * 80 * s - 22 * s, yb)
        pth.lineTo(x + sg * 80 * s - 22 * s, yb - 80 * s)
        pth.cubicTo(x + sg * 80 * s - 22 * s, yb - 116 * s, x + sg * 80 * s + 22 * s, yb - 116 * s, x + sg * 80 * s + 22 * s, yb - 80 * s)
        pth.lineTo(x + sg * 80 * s + 22 * s, yb)
        pth.close()
        c.drawPath(pth, P("#2A1C10", 235))


def draw_church_west(c, x, yb, s=1.0, a=255, dim=0.0):
    """Batı kilisesi (yeniden çizim): üçgen alınlıklı bazilika + çan kulesi + latin haçı."""
    cl = lambda col: mix(col, "#5A4A34", dim * 0.5)
    R(c, x - 190 * s, yb - 190 * s, x + 190 * s, yb, cl("#EDE5D0"), a)
    INKR(c, x - 190 * s, yb - 190 * s, x + 190 * s, yb, 2.4, 230)
    gp = skia.Path()
    gp.moveTo(x - 210 * s, yb - 190 * s)
    gp.lineTo(x, yb - 300 * s)
    gp.lineTo(x + 210 * s, yb - 190 * s)
    gp.close()
    c.drawPath(gp, P(cl("#C65B33"), a))
    INKP(c, gp, 2.2, 230)
    R(c, x + 210 * s, yb - 330 * s, x + 280 * s, yb, cl("#EDE5D0"), a)
    INKR(c, x + 210 * s, yb - 330 * s, x + 280 * s, yb, 2.2, 230)
    tp = skia.Path()
    tp.moveTo(x + 204 * s, yb - 330 * s)
    tp.lineTo(x + 245 * s, yb - 400 * s)
    tp.lineTo(x + 286 * s, yb - 330 * s)
    tp.close()
    c.drawPath(tp, P(cl("#C65B33"), a))
    INKP(c, tp, 2.0, 230)
    c.drawLine(x, yb - 296 * s, x, yb - 372 * s, S("#C79A3C", 6 * s, a))
    c.drawLine(x - 18 * s, yb - 348 * s, x + 18 * s, yb - 348 * s, S("#C79A3C", 6 * s, a))
    for sg in (-1, 1):
        for q in range(2):
            R(c, x + sg * (60 + 70 * q) * s - 10 * s, yb - 150 * s, x + sg * (60 + 70 * q) * s + 10 * s, yb - 70 * s, "#2A1C10", 235)
    pth = skia.Path()
    pth.moveTo(x - 36 * s, yb)
    pth.lineTo(x - 36 * s, yb - 100 * s)
    pth.cubicTo(x - 36 * s, yb - 150 * s, x + 36 * s, yb - 150 * s, x + 36 * s, yb - 100 * s)
    pth.lineTo(x + 36 * s, yb)
    pth.close()
    c.drawPath(pth, P("#2A1C10", 240))


# ═══════════════════════════ c5s1b: masraf + veba korkusu + Cosimo'nun teklifi birlikte etkili oldu ═══════════════════════════
def k_etkenler_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=31, dress=None)
    t = cx.t
    import cilt_props as CP
    plates = (("MASRAF", 440.0, ("c5s1", "masraf,", -0.1)), ("VEBA KORKUSU", 960.0, ("c5s1", "veba", -0.1)), ("COSİMO'NUN TEKLİFİ", 1480.0, ("c5s1", "Cosimo'nun", -0.1)))
    kj = ease_io(cx.amt(("c5s1", "birlikte", -0.1), 0.9), 2)
    for i, (txt, xx, an) in enumerate(plates):
        kp = ease_out(cx.amt(an, 0.7), 3)
        if kp <= 0.003:
            continue
        x = xx
        y = 470 + (1 - kp) * 120
        CM.tablet(f, x - 240, y + 130, 480, 90, alpha=kp, corner=10)
        CM.ink(f, txt, x, y + 190, face="title_m", size=34 if i != 2 else 30, color=TH.fg, align="c", track=6, alpha=kp, emboss=False)
        if i == 0:
            icons.draw_icon(f, "coins", x, y - 20 + 6 * math.sin(t * 1.8), size=230 * (0.8 + 0.2 * kp), metal="gold", alpha=kp, shadow=True)
        elif i == 1:
            draw_plague_cloud(c, x, y - 10, s=1.3 * kp, a=int(255 * kp), t=t)
        else:
            CP.draw_arms(f, x, y - 10, 200 * (0.9 + 0.1 * kp), alpha=kp, shadow=0.5, glow=0.0, glint=None)
    # birlikte: artı işaretleri → altın ayraç
    for xx in (700.0, 1220.0):
        kk = cx.amt(("c5s1", "veba", 0.2), 0.5) * (1.0 - kj)
        if kk > 0.003:
            c.drawLine(xx - 24, 470, xx + 24, 470, S("#8A6A2A", 8.0, int(235 * kk)))
            c.drawLine(xx, 446, xx, 494, S("#8A6A2A", 8.0, int(235 * kk)))
    if kj > 0.003:
        pth = skia.Path()
        pth.moveTo(330, 350)
        pth.cubicTo(330, 270, 1590, 270, 1590, 350)
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=9.0, Color=C("#C79A3C", int(240 * kj)), StrokeCap=skia.Paint.kRound_Cap))
        sp = CM.gilt("BİRLİKTE", "title", 82, 14.0)
        CM.draw_spr(f, sp, 960, 230, "c", alpha=kj, shadow=0.4)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "TEK NEDEN DEĞİL", 960, 840, at=("c5s1", "etkili", -0.1), size=40, w=560)
    L.engr(f, cx, "1439", 960, 130, ("c5s1", "oldu.", -1.6), size=84, track=14, dur=0.9, glow=0.15) if False else None


@CM.ckind("c5_etkenler")
def k_etkenler(cx, **kw):
    k_etkenler_impl(cx, **kw)


# ═══════════════════════════ c5s2: yedi yüz kişilik Rum heyeti — cömert ev sahibi, kalabalık misafir ═══════════════════════════
def k_heyet_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=32, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -600, 2600, FY, 1300)
    # ev sahibi: Floransa sarayı + siluet
    kh = ease_out(cx.amt(("c5s2", -0.1), 0.8), 2.4)
    draw_palazzo(c, 360, FY, 460, 520, style="medici", build=kh)
    L.sil(f, "soylu", 680, FY + 4, 380, t, action="idle", dir=1, seed=4, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kh)
    # kalabalık: sağdan gelir, yaklaşık yedi yüz kişi
    ka = ease_io(clamp((t - cx.at(("c5s2", "yaklaşık", -0.4))) / 3.0), 1.5)
    xoff = (1.0 - ka) * 1100.0
    if ka > 0.003:
        draw_tiny_crowd(c, 960 + xoff, FY - 360, 880, 360, 700, t, seed=11, a=255)
    # sayaç ve etiketler
    k7 = cx.amt(("c5s2", "yedi", -0.1), 0.6)
    if k7 > 0.003:
        sp = CM.engraved("700", "title", 120, 12.0, TH.fg)
        CM.draw_spr(f, sp, 1400, 250, "c", alpha=k7, shadow=0.0)
        CM.ink(f, "YAKLAŞIK", 1400, 168, face="title_m", size=34, color=TH.fg2, align="c", track=10, alpha=k7, emboss=False)
    # ev sahibi keseyi açar: florinler heyete akar
    t_p = cx.at(("c5s2", "masraflarını", -0.2))
    kp = ease_out(clamp((t - t_p) / 0.8), 3)
    if kp > 0.003:
        L.draw_bag(c, 800, FY - 300 + (1 - kp) * 60, s=1.0 * kp, seed=6, sway=2.0 * math.sin(t * 2.0), slips=0)
        for i in range(10):
            ph = ((t - t_p) * 0.55 + i * 0.1) % 1.0
            L.draw_coin_flat(c, 800 + 700 * ph, FY - 300 - 60 * math.sin(math.pi * ph) + 60 * ph, r=18, a=int(255 * kp * (1 - clamp((ph - 0.85) * 6.0))))
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "RUM HEYETİ", 1400, 140, at=("c5s2", "Rum", -0.1), size=38, w=420) if False else None
    L.tag(f, cx, "RUM HEYETİ", 1400, 350, at=("c5s2", "Rum", -0.1), size=36, w=380)
    L.tag(f, cx, "FLORANSA", 360, 140, at=("c5s2", "Floransa,", -0.1), size=38, w=380)
    L.stamp_at(f, cx, "AKTARILANA GÖRE", 960, 140, at=("c5s2", "Aktarılana", -0.1), size=40, rot=-0.04, hold=("c5s2", "yedi", 0.0))
    L.stamp_src(f, cx, "TEK KAYNAK", 1540, 480, at=("c5s2", "yedi", 0.1), size=36, rot=-0.06)
    L.tag(f, cx, "EV SAHİBİ", 680, 330, at=("c5s2", "ev", -0.1), size=34, w=300)


@CM.ckind("c5_heyet")
def k_heyet(cx, **kw):
    k_heyet_impl(cx, **kw)


# ═══════════════════════════ c5s3: Temmuzda Doğu–Batı kiliselerinin birliği ilan edildi; Bizans Osmanlı tehdidi yüzünden istemişti ═══════════════════════════
def k_birlik_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=33, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -600, 2600, FY, 1300)
    # tehdit gölgesi: 'Osmanlı' ile Doğu tarafına
    kt = ease_out(cx.amt(("c5s3", "Osmanlı", -0.2), 1.0), 2)
    ke = ease_out(cx.amt(("c5s3", -0.1), 0.8), 2.4)
    draw_church_east(c, 520, FY, s=1.25, a=255, dim=0.5 * kt) if ke > 0.003 else None
    kw_ = ease_out(cx.amt(("c5s3", "Batı", -0.4), 0.8), 2.4)
    if kw_ > 0.003:
        draw_church_west(c, 1380, FY, s=1.2, a=255)
    # birlik köprüsü: iki kapı arasında altın kemer
    kb = ease_io(cx.amt(("c5s3", "birliği", -0.2), 1.0), 2)
    if kb > 0.003:
        pth = skia.Path()
        pth.moveTo(620, FY - 40)
        pth.cubicTo(760, FY - 380, 1140, FY - 380, 1280, FY - 40)
        pm = skia.PathMeasure(pth, False)
        seg = skia.Path()
        pm.getSegment(0, pm.getLength() * kb, seg, True)
        c.drawPath(seg, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=18.0, Color=C("#C79A3C", 245), StrokeCap=skia.Paint.kRound_Cap))
        c.drawPath(seg, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.0, Color=C("#FFF0B0", 230), StrokeCap=skia.Paint.kRound_Cap))
    # bulla: lacivert/kurşun mühürlü belge; ilk satır
    kd = ease_out(cx.amt(("c5s3", "ilan", -0.3), 0.9), 3)
    if kd > 0.003:
        PP_sheet(340, 230, seed=95).draw(f, 960, 810 + (1 - kd) * 100, rot=-0.02, scale=1.0, alpha=kd, shadow=0.55)
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(780, 740, 780 + 360 * clamp((kd - 0.3) * 1.5), 880))
        PP_hand(f, "LAETENTUR CAELI", 960, 800 + (1 - kd) * 100, 34, "#2A1A0E", 1.0, seed=3)
        c.restore()
        c.drawLine(820, 830, 1100, 830, S("#3A2616", 2.2, int(190 * kd)))
        c.drawLine(820, 856, 1040, 856, S("#3A2616", 2.2, int(150 * kd)))
        CM.wax_seal(f, 1090, 880 + (1 - kd) * 100, 24, "#6A6A72", alpha=1.0, t=clamp((kd - 0.5) * 2.0), mono=None)
    # Osmanlı tehdidi: hilal Doğu'nun üstüne çöker; yardım umudu oku
    if kt > 0.003:
        SOFT(c, 420, 260, 380, 240, "#1A0E08", 120 * kt)
        icons.draw_icon(f, "crescent", 360 + 40 * math.sin(t * 1.2), 230 - 60 * (1 - kt), size=250 * (0.7 + 0.3 * kt), metal="bronze", alpha=kt, shadow=True)
    ky = cx.amt(("c5s3", "istemişti.", -0.7), 0.7)
    if ky > 0.003:
        dashed(c, 700, FY - 460, 1100, FY - 460, col="#8E2A1E", w=6.0, a=int(235 * ky), dash=(18.0, 12.0), phase=-t * 40)
        c.drawPath(sk.poly_path([(1100, FY - 478), (1140, FY - 460), (1100, FY - 442)]), P("#8E2A1E", int(235 * ky)))
    L.end(cx, cam, motes_n=14)
    L.engr(f, cx, "TEMMUZ 1439", 960, 150, ("c5s3", "Temmuzda", -0.1), size=70, track=14, dur=1.0, glow=0.15)
    L.tag(f, cx, "BİZANS", 520, 330, at=("c5s3", "Doğu", -0.1), size=34, w=300) if False else None
    L.tag(f, cx, "DOĞU", 520, 300, at=("c5s3", "Doğu", -0.1), size=34, w=260)
    L.tag(f, cx, "BATI", 1380, 300, at=("c5s3", "Batı", -0.1), size=34, w=260)
    L.tag(f, cx, "OSMANLI TEHDİDİ", 400, 480, at=("c5s3", "Osmanlı", -0.1), size=30, w=420)


@CM.ckind("c5_birlik")
def k_birlik(cx, **kw):
    k_birlik_impl(cx, **kw)


# ═══════════════════════════ c5s5: Ficino'ya göre Plethon'u dinlemesiyle Cosimo'nun Platon merakı uyandı; «ikinci Platon» (ANEKDOT, gravür) ═══════════════════════════
def k_plethon_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=34, dress=None, mono=1.0)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -600, 2600, FY, 1300)
    # kürsü + Plethon (Bizanslı filozof, siluet)
    R(c, 330, FY - 280, 470, FY, "#6E4524")
    INKR(c, 330, FY - 280, 470, FY, 2.0, 230)
    R(c, 300, FY - 296, 500, FY - 270, "#8A5A38")
    INKR(c, 300, FY - 296, 500, FY - 270, 2.0, 230)
    kp = ease_out(cx.amt(("c5s5", "Bizanslı", -0.6), 0.8), 2)
    t_t = cx.at(("c5s5", "Plethon'un", -0.2))
    if kp > 0.003:
        L.sil(f, "kesis", 400, FY + 4, 440, t, action="talk" if t >= t_t else "idle", dir=1, seed=23, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kp, energy=1.2)
    # Cosimo: dinleyen siluet (sağda), konuşmalar ses halkaları
    kc = ease_out(cx.amt(("c5s5", "Cosimo'nun", -0.2), 0.8), 2)
    if kc > 0.003:
        L.sil(f, "soylu", 1160, FY + 4, 400, t, action="idle", dir=-1, seed=4, color="#14100C", rim="#FFE2A0", rim_dir=-1, alpha=kc)
    ks = cx.amt(("c5s5", "konuşmalarını", -0.2), 0.6)
    if ks > 0.003:
        for q in range(4):
            ph = ((t * 0.7) + q * 0.25) % 1.0
            c.drawArc(skia.Rect.MakeLTRB(520 - 40 - ph * 360, 520 - 160 - ph * 160 + 160, 520 + 40 + ph * 360, 520 + 160 + ph * 160 + 160), -50, 100, False, S("#6A5A44", 3.0, int(180 * ks * (1 - ph))))
    # Platon merakı: kitap simgesi (Cosimo'nun üstünde)
    kb = cx.amt(("c5s5", "Platon", -0.2), 0.6)
    if kb > 0.003:
        icons.draw_icon(f, "book", 1160, 280 + 8 * math.sin(t * 1.8), size=150 * (0.8 + 0.2 * ease_out(kb)), metal="gold", alpha=kb, shadow=True)
    ku = ease_out(cx.amt(("c5s5", "uyandı;", -0.4), 0.7), 3)
    if ku > 0.003:
        SOFT(c, 1160, 280, 200, 200, "#FFE9A0", 170 * ku)
        for q in range(10):
            a_ = q * 0.6283
            c.drawLine(1160 + math.cos(a_) * 100, 280 + math.sin(a_) * 100, 1160 + math.cos(a_) * (150 + 20 * math.sin(t * 8 + q)), 280 + math.sin(a_) * (150 + 20 * math.sin(t * 8 + q)), S("#FFD060", 4.0, int(220 * ku)))
    # Floransalılar: sağdan üç siluet Plethon'u gösterir
    kf = ease_out(cx.amt(("c5s5", "Floransalılar", -0.3), 0.8), 2)
    for j, (kd, sd, xx) in enumerate((("halk", 41, 1500), ("tuccar", 42, 1640), ("soylu_f", 43, 1780))):
        if kf > 0.003:
            L.sil(f, kd, xx + (1 - kf) * 200, FY + 8 + 8 * j, 360, t, action="point", dir=-1, seed=sd, color="#14100C", rim="#FFE2A0", rim_dir=-1, alpha=kf, t0=cx.at(("c5s5", "Plethon'a", -0.3)))
    L.end(cx, cam, mono=1.0, motes_n=14, light=(1000.0, 560.0, 1500.0, 0.9))
    L.tag(f, cx, "FICINO'YA GÖRE", 560, 100, at=("c5s5", "Ficino'ya", -0.1), size=36, w=420)
    L.stamp_at(f, cx, "ANEKDOT", 1640, 210, at=("c5s5", "göre", 0.0), size=46, rot=-0.07)
    L.tag(f, cx, "PLETHON", 400, 200, at=("c5s5", "Plethon'un", -0.3), size=36, sub="BİZANSLI FİLOZOF", w=480, hold=("c5s5", "Floransalılar", 0.0))
    L.tag(f, cx, "KONSİL SIRASINDA", 1240, 100, at=("c5s5", "konsil", -0.1), size=32, w=520, hold=("c5s5", "uyandı;", 0.0))
    kq = cx.amt(("c5s5", "“ikinci", -0.2), 0.7)
    if kq > 0.003:
        sp = CM.gilt("“İKİNCİ PLATON”", "title", 74, 10.0)
        CM.draw_spr(f, sp, 960, 330, "c", alpha=kq, shadow=0.4)


@CM.ckind("c5_plethon")
def k_plethon(cx, **kw):
    k_plethon_impl(cx, **kw)


# ═══════════════════════════ c5s6: Floransa'da Yunanca öğretimi 1453'te başlamadı; Chrysoloras 1396–1397'de ders vermişti ═══════════════════════════
def k_yunanca_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=35, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -600, 2600, FY, 1300)
    # sol: 1453 levhası — MİT damgası ve çarpı
    k1 = ease_out(cx.amt(("c5s6", -0.1), 0.8), 3)
    ke = cx.amt(("c5s6", "1453'te", -0.1), 0.5)
    if k1 > 0.003:
        CM.tablet(f, 220, 340 + (1 - k1) * 60, 520, 260, alpha=k1, corner=14)
        sp = CM.engraved("1453", "title", 150, 12.0, TH.fg)
        CM.draw_spr(f, sp, 480, 500 + (1 - k1) * 60, "c", alpha=k1, shadow=0.0)
        kx = cx.amt(("c5s6", "başlamadı;", -0.4), 0.5)
        if kx > 0.003:
            draw_cross(c, 480, 470, 150, k=kx, w=14.0)
    # ders sahnesi: kürsü + öğrenci siluetleri (Chrysoloras 1396–97)
    kd = ease_out(cx.amt(("c5s6", "Manuel", -0.5), 0.8), 2)
    if kd > 0.003:
        R(c, 1040, FY - 270, 1160, FY, "#6E4524", int(255 * kd))
        INKR(c, 1040, FY - 270, 1160, FY, 2.0, 230)
        L.sil(f, "banker", 1100, FY + 4, 430, t, action="talk", dir=1, seed=17, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kd, energy=1.2)
        for j, (kd_, sd, xx) in enumerate((("soylu", 51, 1380), ("halk", 52, 1500), ("soylu_f", 53, 1620), ("tuccar", 54, 1740))):
            L.sil(f, kd_, xx + (1 - kd) * 240, FY + 8 + 6 * j, 340, t, action="idle", dir=-1, seed=sd, color="#14100C", rim="#FFE2A0", rim_dir=-1, alpha=kd)
        # tahta: Yunanca harfler yerine 'alfabe' çizgileri (yazı tipinde Yunanca glif yok)
        c.drawRect(skia.Rect.MakeLTRB(1280, 360, 1780, 560), P("#2E3A30", int(255 * kd)))
        INKR(c, 1280, 360, 1780, 560, 4.0, 235 * kd)
        rs = _RS(8)
        for i in range(4):
            kk = clamp((t - (cx.at(("c5s6", "ders", -0.8)) + 0.2 * i)) / 0.5)
            for q in range(9):
                if q / 9.0 > kk:
                    break
                c.drawLine(1310 + q * 52, 410 + i * 36, 1310 + q * 52 + 26, 410 + i * 36 - rs.uniform(-8, 8), S("#F4EAD2", 4.0, 220))
    L.end(cx, cam, motes_n=14)
    L.stamp_at(f, cx, "MİT", 480, 700, at=("c5s6", "başlamadı;", -0.5), size=64, rot=-0.07)
    L.tag(f, cx, "YUNANCA ÖĞRETİMİ", 480, 250, at=("c5s6", "Yunanca", -0.1), size=32, w=480)
    L.tag(f, cx, "MANUEL CHRYSOLORAS", 1300, 190, at=("c5s6", "Manuel", -0.2), size=34, w=560)
    L.engr(f, cx, "1396 – 1397", 1300, 280, ("c5s6", "1396", -0.2), size=68, track=12, dur=0.9, glow=0.15)


@CM.ckind("c5_yunanca")
def k_yunanca(cx, **kw):
    k_yunanca_impl(cx, **kw)


# ═══════════════════════════ c5s7–8: Niccoli borç içinde öldü; Cosimo borçları üstlendi, ≈800 el yazması San Marco'ya gitti; halka açık kitaplık doğdu ═══════════════════════════
def draw_library_hall(c, FY, filled=1.0, t=0.0, door_open=0.0):
    """Revaklı kütüphane salonu: kemerler, raflar (filled: 0 boş → 1 dolu kitap), okuma sehpaları."""
    R(c, -400, 0, 2400, FY, "#EDE3C8")
    for i in range(7):
        ax = 150 + i * 270
        p = skia.Path()
        p.moveTo(ax - 90, FY)
        p.lineTo(ax - 90, 420)
        p.cubicTo(ax - 90, 250, ax + 90, 250, ax + 90, 420)
        p.lineTo(ax + 90, FY)
        p.close()
        c.drawPath(p, P("#CFC4A2", 255))
        INKP(c, p, 2.4, 230)
        if filled > 0.01:
            c.save()
            c.clipPath(p, skia.ClipOp.kIntersect, True)
            rs = _RS(i + 5)
            for r in range(4):
                yb = 470 + r * 100
                x = ax - 80
                while x < ax + 74:
                    if rs.rand() < filled:
                        bw = rs.uniform(12, 22)
                        bh = rs.uniform(48, 84)
                        R(c, x, yb - bh, x + bw, yb, ["#8E2A1E", "#233C8C", "#3A7A52", "#C79A3C", "#6A4A8A", "#7A4A28"][int(rs.randint(0, 6))])
                        x += bw + 1
                    else:
                        x += 14
                c.drawLine(ax - 80, yb, ax + 80, yb, S("#6A4426", 6.0, 235))
            c.restore()
        else:
            for r in range(4):
                c.drawLine(ax - 76, 470 + r * 100, ax + 76, 470 + r * 100, S("#6A4426", 6.0, 235))
        R(c, ax - 105, 430, ax - 90, FY, "#B8AE94")
    R(c, -400, 380, 2400, 420, "#B8AE94")
    INKR(c, -400, 380, 2400, 420, 2.0, 220)


def k_niccoli_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=36, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -600, 2600, FY, 1300)
    # ── A: Niccoli'nin çalışma odası, borç kâğıtları, Cosimo borçları üstlenir ──
    t_dead = cx.at(("c5s7", "öldü;", -0.2))
    t_cos = cx.at(("c5s7", "Cosimo", -0.2))
    t_800 = cx.at(("c5s7", "sekiz", -0.4))
    t_go = cx.at(("c5s7", "kitaplar", -0.3))
    t_lib = cx.at(("c5s8", -0.1))
    # raflar: dolu kodeksler (Niccoli'nin koleksiyonu) — arka duvar
    draw_library_hall(c, FY, filled=1.0, t=t)
    # masa + yığınlar
    table_persp(c, 560, 1360, 760, 870, apron=60, col="#7A4A28", depth=0.07)
    for i, (bx, col) in enumerate(((680, "#8E2A1E"), (740, "#233C8C"), (700, "#3A7A52"), (780, "#C79A3C"))):
        R(c, bx - 70, 742 - i * 22, bx + 70, 764 - i * 22, col)
        INKR(c, bx - 70, 742 - i * 22, bx + 70, 764 - i * 22, 1.4, 210)
    # Niccoli (siluet): çalışır; 'öldü'de solarak kaybolur (şiddet yok); koltuk boş kalır
    kn = ease_out(cx.amt(("c5s7", -0.1), 0.6), 2) * (1.0 - smooth(clamp((t - t_dead) / 1.2)))
    if kn > 0.003:
        L.OD.seated(f, "banker", 1000, 820, 380, t, action="write", dir=1, seed=19, sil="#14100C", rim="#FFE2A0", rim_dir=1, t0=cx.at(("c5s7", -0.1)), alpha=kn)
    # borç kâğıtları: 'borç içinde'
    kb = cx.amt(("c5s7", "borç", -0.2), 0.5)
    pay = clamp((t - (t_cos + 0.3)) / 1.6)
    if kb > 0.003:
        for i in range(12):
            ph = clamp((t - (cx.at(("c5s7", "borç", -0.2)) + 0.09 * i)) / 0.7)
            if ph <= 0:
                continue
            x = 760 + (i % 6) * 70 + 20 * math.sin(i * 2.0)
            y = lerp(180, 640 - (i // 6) * 54 + 10 * math.sin(i), ease_out(ph, 2))
            col = "#EFE3C2" if pay < (i / 12.0) else "#D8F0D0"
            L.draw_slip(c, x, y, w=96, h=64, rot=0.25 * math.sin(i * 1.7), lines=2, seed=i + 2, tone=col)
            if pay >= (i / 12.0) and pay > 0:
                draw_check(c, x, y, s=0.45, k=1.0, w=7.0)
    # Cosimo: borçları öder (siluet), palle işareti
    kcm = ease_out(cx.amt(("c5s7", "Cosimo", -0.2), 0.8), 2)
    if kcm > 0.003:
        L.sil(f, "soylu", 360 - (1 - kcm) * 200, FY + 4, 420, t, action="give", dir=1, seed=4, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kcm, t0=t_cos + 0.5)
    # ── B: sekiz yüz el yazması: sayaç + denetim mührü + San Marco'ya akış ──
    k8 = ease_out(clamp((t - t_800) / 1.4), 2.2)
    if k8 > 0.003:
        sp = CM.engraved(CM.fmt_int(800 * k8), "title", 150, 12.0, TH.fg)
        CM.draw_spr(f, sp, 960, 250, "c", alpha=smooth(k8 * 3), shadow=0.0)
        CM.ink(f, "EL YAZMASI", 960, 330, face="title_m", size=40, color=TH.fg2, align="c", track=10, alpha=smooth(k8 * 3), emboss=False)
    ks = ease_out(cx.amt(("c5s7", "denetimini", -0.2), 0.6), 3)
    if ks > 0.003:
        import cilt_props as CP
        CP.draw_arms(f, 960, 540, 130 * ks, alpha=ks, shadow=0.5, glow=0.0, glint=None)
    kg = clamp((t - t_go) / 2.0)
    if kg > 0:
        K4.draw_monastery(c, 1620, FY - 6, s=0.7, a=255, t=t, build=ease_out(clamp(kg * 2.0), 2))
        for i in range(12):
            ph = clamp(kg * 1.3 - i * 0.07)
            if 0 < ph < 1:
                K4.draw_book_block(c, lerp(900, 1620, ph), lerp(520, FY - 120, ph) - 140 * math.sin(math.pi * ph), 74, 22, ["#8E2A1E", "#233C8C", "#3A7A52", "#C79A3C"][i % 4], tilt=0.4 * math.sin(ph * 8 + i))
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "NICCOLÒ NICCOLI", 960, 140, at=("c5s7", "Niccolò", -0.2), size=38, w=560, hold=("c5s7", "Cosimo", 0.0))
    L.tag(f, cx, "BORÇ", 1500, 300, at=("c5s7", "borç", -0.2), size=40, w=260, hold=("c5s7", "denetimini", 0.0))
    L.tag(f, cx, "SAN MARCO", 1620, 330, at=("c5s7", "San", -0.2), size=34, w=380, hold=("c5s8", "halka", 0.0))


@CM.ckind("c5_niccoli")
def k_niccoli(cx, **kw):
    k_niccoli_impl(cx, **kw)


# ═══════════════════════════ c5s8: Floransa'nın halka açık bir kitaplığı doğdu ═══════════════════════════
def k_kutuphane_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=37, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -600, 2600, FY, 1300, col1="#D6C9A6", col2="#B8A67C")
    kfill = ease_out(cx.amt(("c5s8", -0.2), 1.0), 2)
    draw_library_hall(c, FY, filled=kfill, t=t)
    # okuma sehpaları ve kapı: halk içeri girer
    for xx in (420, 960, 1500):
        R(c, xx - 80, FY - 180, xx + 80, FY - 150, "#6E4524")
        c.drawLine(xx - 60, FY - 150, xx - 80, FY, S("#5A3C22", 8.0, 235))
        c.drawLine(xx + 60, FY - 150, xx + 80, FY, S("#5A3C22", 8.0, 235))
        INKR(c, xx - 80, FY - 180, xx + 80, FY - 150, 1.6, 220)
    t_in = cx.at(("c5s8", "halka", -0.4))
    for q, (kd, xe) in enumerate((("halk", 420), ("soylu_f", 960), ("tuccar", 1500), ("soylu", 700), ("halk", 1240))):
        ph = clamp((t - (t_in + 0.28 * q)) / 1.6)
        if ph <= 0:
            continue
        x = lerp(2100, xe + 20, ease_out(ph, 2))
        if ph < 0.98:
            L.sil(f, kd, x, FY + 8 + 6 * (q % 3), 330, t, dir=-1, seed=71 + q, color="#14100C", rim="#FFE2A0", rim_dir=-1, walker=120.0)
        else:
            L.sil(f, kd, xe + 20, FY + 8 + 6 * (q % 3), 330, t, action="idle", dir=-1, seed=71 + q, color="#14100C", rim="#FFE2A0", rim_dir=-1)
    L.end(cx, cam, motes_n=16)
    L.tag(f, cx, "HALKA AÇIK KİTAPLIK", 960, 150, at=("c5s8", "halka", -0.3), size=40, w=700)
    L.stamp_at(f, cx, "YORUM", 1560, 260, at=("c5s8", "Böylece", 0.0), size=44, rot=-0.07)


@CM.ckind("c5_kutuphane")
def k_kutuphane(cx, **kw):
    k_kutuphane_impl(cx, **kw)


# ═══════════════════════════ c5s9–10: 1463 dolaylarında Ficino'nun derlemesindeki mektup — Careggi'ye zihnini işlemek için geldi ═══════════════════════════
def careggi_scene(c, t, T):
    """Careggi tepesi: gökyüzü, tepeler, yamaç, villa, selviler (c3_careggi ile aynı dil)."""
    sh = skia.GradientShader.MakeLinear([(0, -500), (0, 780)], [C("#9CBBDC"), C("#EFE6C8")], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(-1200, -1000, 3200, 800), skia.Paint(Shader=sh))
    for i in range(5):
        cxx = ((i * 520 + t * (6 + i * 1.5)) % 2800) - 400
        cyy = 60 + (i * 97) % 340
        SOFT(c, cxx, cyy, 220 + 20 * i, 36, "#FFFFFF", 150)
    LH = 900.0
    for (col, amp, scl, base, ph) in (("#A9BDB6", 40, 600, 420, 0.0), ("#93AFA5", 46, 420, 340, 2.1), ("#7F9E92", 52, 300, 270, 4.3)):
        cc = T(col, 0.2)
        pts = []
        x = -1200
        while x <= 3200:
            pts.append((x, LH - L.PN.ridge_y(x, base, amp, scl, ph)))
            x += 10
        poly = pts + [(pts[-1][0], LH + 900), (pts[0][0], LH + 900)]
        c.drawPath(sk.poly_path(poly), skia.Paint(AntiAlias=True, Color=C(cc)))
    pts = []
    x = -1200
    while x <= 3200:
        pts.append((x, 760 - 40 * math.sin(x * 0.0021 + 0.6) - 24 * math.sin(x * 0.0057)))
        x += 12
    poly = pts + [(pts[-1][0], 1500), (pts[0][0], 1500)]
    c.drawPath(sk.poly_path(poly), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 700), (0, 1200)], [C("#8FA070"), C("#5E7A48")], [0, 1])))
    K3.draw_villa(c, T, 1000.0, 790.0, t)
    for (cxx, hh) in ((300, 300), (410, 250), (1620, 290), (1710, 240), (1830, 280), (190, 230)):
        SE.SC.cypress(c, cxx, 800 + (cxx % 7) * 4, hh, T("#2E4A33", 0.1), T("#4F6E4A", 0.1))


def draw_head_profile(c, x, y, s=1.0, a=255, col="#14100C"):
    """Baş profili silueti (yüz çizgisi yok): kafa + boyun + omuz; (x,y) kafa merkezi."""
    p = skia.Path()
    p.moveTo(x - 60 * s, y + 160 * s)
    p.lineTo(x - 50 * s, y + 70 * s)
    p.cubicTo(x - 100 * s, y + 20 * s, x - 90 * s, y - 120 * s, x + 10 * s, y - 130 * s)
    p.cubicTo(x + 100 * s, y - 130 * s, x + 120 * s, y - 40 * s, x + 96 * s, y + 10 * s)
    p.lineTo(x + 112 * s, y + 24 * s)
    p.lineTo(x + 92 * s, y + 38 * s)
    p.cubicTo(x + 90 * s, y + 70 * s, x + 60 * s, y + 80 * s, x + 50 * s, y + 90 * s)
    p.lineTo(x + 70 * s, y + 160 * s)
    p.close()
    c.drawPath(p, P(col, a))
    return p


def k_careggi5_impl(cx, **_):
    f = cx.f
    c = f.c
    t = cx.t
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    cam.begin(f)
    T = CT.Tint("day")
    careggi_scene(c, t, T)
    # A: derleme + mektup; B: mektup + tarla/zihin
    kA = ease_out(cx.amt(("c5s9", "Ficino'nun", -0.3), 0.8), 3)
    if kA > 0.003:
        icons.draw_icon(f, "book_open", 420, 860 - (1 - kA) * 120, size=300 * (0.8 + 0.2 * kA), metal="gold", alpha=kA, shadow=True)
    kl = ease_out(cx.amt(("c5s9", "mektupta", -0.4), 0.9), 3)
    if kl > 0.003:
        PP_sheet(320, 220, seed=97).draw(f, 460, 660 - 60 * kl, rot=-0.06, scale=1.0, alpha=kl, shadow=0.55)
        for i in range(5):
            c.drawLine(340, 600 - 60 * kl + i * 26, 580 - (i % 3) * 30, 600 - 60 * kl + i * 26, S("#3A2616", 2.2, int(190 * kl)))
        ks = clamp((t - cx.at(("c5s9", "Cosimo,", -0.2))) / 0.4)
        if ks > 0:
            CM.wax_seal(f, 580, 720 - 60 * kl, 26, "#A52A1C", alpha=1.0, t=ks, mono=None)
    cam.end(f)
    CM.finish(f, cx, motes_n=12)
    L.date_plate(f, cx, "1463 DOLAYLARI", ("c5s9", "1463", -0.2), x=96, y=860, size=46)
    L.tag(f, cx, "FICINO'NUN DERLEMESİ", 420, 420, at=("c5s9", "Ficino'nun", -0.2), size=32, w=560, hold=("c5s9", "Careggi'ye", 0.0))
    L.tag(f, cx, "MEKTUP", 460, 480, at=("c5s9", "mektupta", -0.2), size=36, w=300, hold=("c5s9", "Careggi'ye", 0.0))
    L.tag(f, cx, "CAREGGİ", 960, 520, at=("c5s9", "Careggi'ye", -0.3), size=38, w=420)
    # B: tarla ✗ / zihin ✓ (mektubun içeriği)
    kt = ease_out(cx.amt(("c5s9", "tarlasını", -0.3), 0.8), 3)
    if kt > 0.003:
        f.c.save()
        # tarla: sıra sıra karık
        R(f.c, 300, 130, 720, 330, "#8A6A3A", int(255 * kt))
        INKR(f.c, 300, 130, 720, 330, 3.0, 235 * kt)
        for i in range(7):
            f.c.drawLine(310, 150 + i * 28, 710, 150 + i * 28 + (6 if i % 2 else -6), S("#4A3418", 4.0, int(220 * kt)))
        kx = cx.amt(("c5s9", "değil,", -0.3), 0.5)
        if kx > 0.003:
            draw_cross(f.c, 510, 230, 150, k=kx, w=14.0)
        f.c.restore()
    kz = ease_out(cx.amt(("c5s9", "zihnini", -0.3), 0.8), 3)
    if kz > 0.003:
        R(f.c, 1200, 130, 1620, 330, "#EFE5CC", int(255 * kz))
        INKR(f.c, 1200, 130, 1620, 330, 3.0, 235 * kz)
        draw_head_profile(f.c, 1410, 210, s=0.8, a=int(255 * kz))
        f.c.save()
        hp = skia.Path()
        hp.addOval(skia.Rect.MakeLTRB(1330, 150, 1470, 230))
        f.c.clipPath(hp, skia.ClipOp.kIntersect, True)
        for i in range(6):
            f.c.drawLine(1320, 160 + i * 14, 1480, 160 + i * 14 + 4 * math.sin(t * 3 + i), S("#E0B84E", 3.0, int(255 * kz)))
        f.c.restore()
        kq = clamp((t - cx.at(("c5s9", "işlemek", -0.3))) / 0.5)
        if kq > 0.003:
            icons.draw_icon(f, "feather", 1290 + 40 * math.sin(t * 2.0), 130 + 10 * math.sin(t * 5.0), size=110 * kq, metal="gold", alpha=kq, shadow=True)
    L.tag(f, cx, "TARLA", 510, 400, at=("c5s9", "tarlasını", -0.2), size=36, w=260)
    L.tag(f, cx, "ZİHİN", 1410, 400, at=("c5s9", "zihnini", -0.2), size=36, w=260)


@CM.ckind("c5_careggi")
def k_careggi5(cx, **kw):
    k_careggi5_impl(cx, **kw)


# ═══════════════════════════ c5s10: Ficino'dan Platon'un En Yüksek İyi üzerine kitabını ve Orfik lirini getirmesini ister ═══════════════════════════
def k_lir_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=38, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -600, 2600, FY, 1300)
    # Cosimo (solda, ister) ve Ficino (sağda, getirir)
    kc = ease_out(cx.amt(("c5s10", -0.1), 0.6), 2)
    t_ask = cx.at(("c5s10", "ister.", -0.6))
    L.sil(f, "soylu", 360, FY + 4, 420, t, action="point" if t >= t_ask else "idle", dir=1, seed=4, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kc, t0=t_ask)
    kf = ease_out(cx.amt(("c5s10", "Ficino'dan", -0.3), 0.8), 2)
    if kf > 0.003:
        L.sil(f, "banker", 1560 + (1 - kf) * 260, FY + 4, 410, t, action="idle", dir=-1, seed=22, color="#14100C", rim="#FFE2A0", rim_dir=-1, alpha=kf)
    # masa: kitap + lir
    table_persp(c, 700, 1260, 720, 830, apron=60, col="#7A4A28", depth=0.07)
    kb = ease_out(cx.amt(("c5s10", "kitabını", -0.9), 0.8), 3)
    if kb > 0.003:
        icons.draw_icon(f, "book", 860, 640 - (1 - kb) * 120, size=250 * (0.8 + 0.2 * kb), metal="gold", alpha=kb, shadow=True)
        SOFT(c, 860, 640, 190, 150, "#FFE9A0", 100 * kb)
    kl = ease_out(cx.amt(("c5s10", "Orfik", -0.2), 0.8), 3)
    if kl > 0.003:
        draw_lyre(c, 1090, 590 - (1 - kl) * 120, s=0.9 * kl, a=int(255 * kl), t=t, glow=0.5 * kl)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "PLATON", 760, 330, at=("c5s10", "Platon'un", -0.2), size=38, w=300)
    L.tag(f, cx, "EN YÜKSEK İYİ", 760, 420, at=("c5s10", "Yüksek", -0.3), size=34, w=420)
    L.tag(f, cx, "ORFİK LİR", 1260, 330, at=("c5s10", "Orfik", -0.2), size=36, w=360)
    L.tag(f, cx, "FICINO", 1560, 200, at=("c5s10", "Ficino'dan", -0.2), size=36, w=300)


@CM.ckind("c5_lir")
def k_lir(cx, **kw):
    k_lir_impl(cx, **kw)


# ═══════════════════════════ c5s11: Bir bankacı için fena bir alışveriş listesi değil: en yüksek iyi, bir de lir ═══════════════════════════
def k_liste_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=39, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -600, 2600, FY, 1300)
    # banker (siluet) elinde kese ile; karşısında liste
    kb = ease_out(cx.amt(("c5s11", -0.1), 0.7), 2)
    L.sil(f, "banker", 520, FY + 4, 440, t, action="idle", dir=1, seed=19, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kb)
    if kb > 0.003:
        L.draw_bag(c, 380, 700, s=0.9 * kb, seed=6, sway=2.0 * math.sin(t * 2.0), slips=0)
    # liste (parşömen)
    kl = ease_out(cx.amt(("c5s11", "alışveriş", -0.6), 0.8), 3)
    if kl > 0.003:
        PP_sheet(560, 700, seed=101).draw(f, 1260, 500 + (1 - kl) * 80, rot=-0.02, scale=1.0, alpha=kl, shadow=0.55)
        PP_hand(f, "LİSTE", 1260, 260 + (1 - kl) * 80, 70, "#2A1A0E", kl, seed=2)
        c.drawLine(1040, 300 + (1 - kl) * 80, 1480, 300 + (1 - kl) * 80, S("#3A2616", 3.0, int(200 * kl)))
        for i, (txt, an) in enumerate((("EN YÜKSEK İYİ", ("c5s11", "en", -0.1)), ("BİR LİR", ("c5s11", "bir", -0.1)))):
            ki = clamp((t - cx.at(an)) / 0.9)
            y = 420 + i * 120 + (1 - kl) * 80
            R(c, 1060, y - 26, 1104, y + 18, "#F4EAD2", int(255 * kl))
            INKR(c, 1060, y - 26, 1104, y + 18, 2.2, 230 * kl)
            if ki > 0.0:
                c.save()
                c.clipRect(skia.Rect.MakeLTRB(1120, y - 50, 1120 + 380 * ease_io(ki, 1.5), y + 40))
                PP_hand(f, txt, 1320, y + 6, 44, "#2A1A0E", 1.0, seed=7 + i)
                c.restore()
            kt = clamp((t - cx.at(an) - 0.9) / 0.35)
            if kt > 0.0:
                draw_check(c, 1082, y - 4, s=0.55, k=kt, w=8.0)
    # sıradan bankacı listesi (soluk, üstü çizili): kumaş, baharat… hayalet
    kg = cx.amt(("c5s11", "fena", -0.2), 0.6) * (1.0 - cx.amt(("c5s11", "değil:", 0.0), 0.5))
    if kg > 0.003:
        for i, txt in enumerate(("KUMAŞ", "BAHARAT", "ŞARAP")):
            PP_hand(f, txt, 960, 330 + i * 70, 48, "#6A5A44", 0.5 * kg, seed=30 + i)
    L.end(cx, cam, motes_n=14)
    L.stamp_at(f, cx, "YORUM", 520, 190, at=("c5s11", "fena", -0.2), size=46, rot=-0.07)
    L.tag(f, cx, "BANKACI", 520, 270, at=("c5s11", "bankacı", -0.2), size=34, w=300)


@CM.ckind("c5_liste")
def k_liste(cx, **kw):
    k_liste_impl(cx, **kw)


# ═══════════════════════════ c5s12: Ficino'ya Platon'un bütün eserlerinin el yazması, şehirde bir ev ve Careggi yakınında bir ev armağan ═══════════════════════════
def k_armagan_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=40, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -600, 2600, FY, 1300)
    kc = ease_out(cx.amt(("c5s12", -0.1), 0.6), 2)
    t_gv = cx.at(("c5s12", "Platon'un", -0.8))
    L.sil(f, "soylu", 420, FY + 4, 420, t, action="give", dir=1, seed=4, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kc, t0=t_gv, slip=False)
    L.sil(f, "banker", 1000, FY + 4, 410, t, action="idle", dir=-1, seed=22, color="#14100C", rim="#FFE2A0", rim_dir=-1, alpha=kc)
    # büyük el yazması: Cosimo'dan Ficino'ya uzanır
    kb = ease_out(cx.amt(("c5s12", "bütün", -0.5), 0.9), 3)
    if kb > 0.003:
        xx = lerp(560, 860, ease_io(clamp((t - cx.at(("c5s12", "eserlerinin", -0.2))) / 0.9), 1.5))
        K4.draw_book_block(c, xx, 640 - (1 - kb) * 120, 230, 60, "#7A4A28")
        K4.draw_book_block(c, xx, 580 - (1 - kb) * 120, 220, 54, "#8E2A1E")
        K4.draw_book_block(c, xx, 526 - (1 - kb) * 120, 210, 50, "#233C8C")
        SOFT(c, xx, 540, 190, 140, "#FFE9A0", 90 * kb)
    # iki ev: şehirdeki ev + Careggi yakınında ev; anahtarlar
    k1 = ease_out(cx.amt(("c5s12", "şehirde", -0.3), 0.9), 2.4)
    k2 = ease_out(cx.amt(("c5s12", "Careggi", -0.3), 0.9), 2.4)
    if k1 > 0.003:
        draw_palazzo(c, 1380, FY, 360, 360, style="rucellai", build=k1)
        K4.draw_key(c, 1380 + 90 * (1 - k1), 380, s=1.0 * k1, rot=-0.3)
    if k2 > 0.003:
        K3.draw_villa(c, CT.Tint("day"), 1730, FY - 30, t) if False else None
        c.save()
        c.translate(1730 - 1000 * 0.42, FY - 30 - 790 * 0.42 + 0.0)
        c.scale(0.42, 0.42)
        c.translate(0, 0)
        K3.draw_villa(c, CT.Tint("day"), 1000.0, 790.0, t)
        c.restore()
        K4.draw_key(c, 1730, 380, s=1.0 * k2, rot=-0.3)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "PLATON'UN BÜTÜN ESERLERİ", 760, 190, at=("c5s12", "bütün", -0.3), size=32, w=640, hold=("c5s12", "şehirde", 0.0))
    L.tag(f, cx, "ŞEHİRDE BİR EV", 1380, 190, at=("c5s12", "şehirde", -0.2), size=32, w=420)
    L.tag(f, cx, "CAREGGİ YAKININDA", 1680, 290, at=("c5s12", "Careggi", -0.2), size=28, sub="BİR EV DAHA", w=400)
    L.tag(f, cx, "FICINO", 1000, 330, at=("c5s12", "Ficino'ya", -0.3), size=34, w=300)


@CM.ckind("c5_armagan")
def k_armagan(cx, **kw):
    k_armagan_impl(cx, **kw)


# ═══════════════════════════ c5s13: Buna sonradan «Platon Akademisi» dendi; ama tüzüğü yoktu, üye kaydı tutulmadı ═══════════════════════════
def k_akademi_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=41, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -600, 2600, FY, 1300)
    T = CT.Tint("day")
    # A: bir ev (Careggi) + 'sonradan' yapışan etiket
    kh = ease_out(cx.amt(("c5s13", -0.1), 0.8), 2.4)
    t_hit = cx.at(("c5s13", "Akademisi”", -0.3))
    t_pl = cx.at(("c5s13", "ama", -0.1))
    if kh > 0.003:
        draw_palazzo(c, 960, FY, 520, 440, style="rucellai", build=kh, dim=0.0)
    kfall = ease_in(clamp((t - (t_hit - 0.55)) / 0.55), 2)
    if t < t_hit:
        px_, py_ = lerp(1500.0, 960.0, kfall), lerp(160.0, 340.0, kfall)
        sc, rot, a, peel = lerp(1.4, 1.0, kfall), lerp(-0.22, -0.03, kfall), clamp((t - (t_hit - 0.6)) / 0.2), 0.0
    else:
        kp_ = clamp((t - t_pl) / 0.9)
        px_, py_, sc, rot = 960.0, 340.0, 1.0, -0.03
        peel = kp_
        a = 1.0 - clamp((kp_ - 0.5) / 0.5)
    if a > 0.003:
        L.draw_sticker(f, px_, py_, 900, 170, "“PLATON AKADEMİSİ”", a=a, rot=rot, scale=sc, peel=peel, size=62, track=6.0)
    if t >= t_hit and t < t_hit + 0.45:
        kk = (t - t_hit) / 0.45
        c.drawCircle(960, 340, 160 + 250 * kk, S("#FFF2B0", 4.0, int(160 * (1 - kk))))
    # B: boş tüzük + boş üye defteri
    kd = ease_out(cx.amt(("c5s13", "tüzüğü", -0.5), 0.9), 3)
    if kd > 0.003:
        PP_sheet(560, 700, seed=111).draw(f, 560, 560 + (1 - kd) * 100, rot=-0.02, scale=1.0, alpha=kd, shadow=0.55)
        PP_hand(f, "TÜZÜK", 560, 300 + (1 - kd) * 100, 76, "#2A1A0E", kd, seed=2)
        for i in range(8):
            c.drawLine(330, 380 + i * 52 + (1 - kd) * 100, 790, 380 + i * 52 + (1 - kd) * 100, S("#8A7A58", 1.6, int(150 * kd)))
        kx = cx.amt(("c5s13", "yoktu,", -0.3), 0.5)
        if kx > 0.003:
            draw_cross(c, 560, 560, 190, k=kx, w=14.0)
    ky = ease_out(cx.amt(("c5s13", "üye", -0.4), 0.9), 3)
    if ky > 0.003:
        PP_sheet(560, 700, seed=112).draw(f, 1360, 560 + (1 - ky) * 100, rot=0.02, scale=1.0, alpha=ky, shadow=0.55)
        PP_hand(f, "ÜYE KAYDI", 1360, 300 + (1 - ky) * 100, 64, "#2A1A0E", ky, seed=3)
        for i in range(8):
            c.drawLine(1130, 380 + i * 52 + (1 - ky) * 100, 1590, 380 + i * 52 + (1 - ky) * 100, S("#8A7A58", 1.6, int(150 * ky)))
        c.drawLine(1260, 360 + (1 - ky) * 100, 1260, 790 + (1 - ky) * 100, S("#8A7A58", 1.6, int(150 * ky)))
        kz = cx.amt(("c5s13", "tutulmadı.", -0.5), 0.5)
        if kz > 0.003:
            draw_cross(c, 1360, 560, 190, k=kz, w=14.0)
    L.end(cx, cam, motes_n=14)
    L.stamp_at(f, cx, "SONRADAN", 520, 190, at=("c5s13", "sonradan", -0.1), size=52, rot=-0.07, hold=("c5s13", "ama", 0.0))
    L.tag(f, cx, "TÜZÜK YOK", 560, 880, at=("c5s13", "yoktu,", -0.2), size=34, w=320) if False else None


@CM.ckind("c5_akademi")
def k_akademi(cx, **kw):
    k_akademi_impl(cx, **kw)


# ═══════════════════════════ c5s14: Cosimo bu mektuptan yaklaşık bir yıl sonra öldü ═══════════════════════════
def k_yil5_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=42, dress=None)
    t = cx.t
    # mektup (solda, sakin) + kum saati (ortada) — ölüm gösterilmez
    kl = ease_out(cx.amt(("c5s14", -0.1), 0.8), 3)
    PP_sheet(520, 660, seed=97).draw(f, 600, 540 + (1 - kl) * 80, rot=-0.04, scale=1.0, alpha=kl, shadow=0.55)
    for i in range(9):
        c.drawLine(380, 340 + i * 44 + (1 - kl) * 80, 820 - (i % 3) * 40, 340 + i * 44 + (1 - kl) * 80, S("#3A2616", 2.4, int(190 * kl)))
    CM.wax_seal(f, 780, 790 + (1 - kl) * 80, 30, "#A52A1C", alpha=1.0, t=clamp((kl - 0.4) * 1.6), mono=None)
    kh = ease_out(cx.amt(("c5s14", "yaklaşık", -0.4), 0.8), 3)
    if kh > 0.003:
        K3.draw_hourglass_anim(c, 1290, 500, 2.0 * kh, t, cx.at(("c5s14", "yıl", -0.1)), a=int(255 * kh))
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "YAKLAŞIK BİR YIL", 1290, 190, at=("c5s14", "yaklaşık", -0.2), size=40, w=520)


@CM.ckind("c5_yil")
def k_yil5(cx, **kw):
    k_yil5_impl(cx, **kw)


# ═══════════════════════════ c5s15a: Torunu Lorenzo, Janus Lascaris'i gönderdi ═══════════════════════════
def k_lascaris_giris_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=43, dress=None)
    t = cx.t
    import cilt_props as CP
    FY = 880.0
    L.grid_floor(c, -600, 2600, FY, 1300)
    kl = ease_out(cx.amt(("c5s15", -0.1), 0.7), 2)
    t_give = cx.at(("c5s15", "Lascaris'i", -0.8))
    L.sil(f, "soylu", 560, FY + 4, 430, t, action="give", dir=1, seed=4, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kl, t0=t_give)
    if kl > 0.003:
        CP.draw_arms(f, 560, 250, 120 * kl, alpha=kl, shadow=0.4, glow=0.0, glint=None)
    kj = ease_out(cx.amt(("c5s15", "Lascaris'i", -0.5), 0.8), 2)
    if kj > 0.003:
        L.sil(f, "tuccar", 1100 + (1 - kj) * 300, FY + 4, 410, t, action="take", dir=-1, seed=27, color="#14100C", rim="#FFE2A0", rim_dir=-1, alpha=kj, t0=t_give + 0.2, got_at=t_give + 1.4)
    # doğu oku
    ka = ease_out(cx.amt(("c5s15", "1490", -0.6), 0.8), 3)
    if ka > 0.003:
        c.drawLine(1300, 520, 1300 + 360 * ka, 520, S("#C79A3C", 14.0, 245))
        c.drawPath(sk.poly_path([(1300 + 360 * ka, 480), (1300 + 360 * ka + 70, 520), (1300 + 360 * ka, 560)]), P("#C79A3C", 245))
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "LORENZO", 560, 130, at=("c5s15", "Lorenzo,", -0.5), size=38, sub="TORUNU", w=360)
    L.tag(f, cx, "JANUS LASCARIS", 1100, 190, at=("c5s15", "Lascaris'i", -0.3), size=36, w=480)
    L.tag(f, cx, "DOĞU", 1560, 430, at=("c5s15", "1490", -0.5), size=40, w=260)


@CM.ckind("c5_lascaris_giris")
def k_lascaris_giris(cx, **kw):
    k_lascaris_giris_impl(cx, **kw)


# ═══════════════════════════ c5s15c: el yazması toplasın, II. Bayezid'le de pazarlık yapsın ═══════════════════════════
def draw_ottoman(c, x, yb, s=1.0, a=255):
    """Osmanlı yapısı (genel temsil): kare gövde + büyük kubbe + ince minare + hilal."""
    R(c, x - 150 * s, yb - 170 * s, x + 150 * s, yb, "#E8DEC0", a)
    INKR(c, x - 150 * s, yb - 170 * s, x + 150 * s, yb, 2.4, 230)
    dp = skia.Path()
    dp.moveTo(x - 120 * s, yb - 170 * s)
    dp.cubicTo(x - 120 * s, yb - 330 * s, x + 120 * s, yb - 330 * s, x + 120 * s, yb - 170 * s)
    dp.close()
    c.drawPath(dp, P("#8FA8B8", a))
    INKP(c, dp, 2.2, 230)
    R(c, x + 160 * s, yb - 380 * s, x + 186 * s, yb, "#E8DEC0", a)
    INKR(c, x + 160 * s, yb - 380 * s, x + 186 * s, yb, 2.0, 230)
    tp = skia.Path()
    tp.moveTo(x + 154 * s, yb - 380 * s)
    tp.lineTo(x + 173 * s, yb - 450 * s)
    tp.lineTo(x + 192 * s, yb - 380 * s)
    tp.close()
    c.drawPath(tp, P("#8FA8B8", a))
    INKP(c, tp, 1.8, 230)
    for q in range(3):
        pth = skia.Path()
        pth.moveTo(x - 90 * s + q * 90 * s - 22 * s, yb)
        pth.lineTo(x - 90 * s + q * 90 * s - 22 * s, yb - 80 * s)
        pth.cubicTo(x - 90 * s + q * 90 * s - 22 * s, yb - 116 * s, x - 90 * s + q * 90 * s + 22 * s, yb - 116 * s, x - 90 * s + q * 90 * s + 22 * s, yb - 80 * s)
        pth.lineTo(x - 90 * s + q * 90 * s + 22 * s, yb)
        pth.close()
        c.drawPath(pth, P("#2A1C10", 235))


def k_pazarlik_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=44, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -600, 2600, FY, 1300)
    # sağda Osmanlı yapısı + hilal
    ko = ease_out(cx.amt(("c5s15", "Bayezid'le", -0.6), 0.9), 2.4)
    if ko > 0.003:
        c.save()
        c.translate((1 - ko) * 300, 0)
        draw_ottoman(c, 1560, FY, s=1.25, a=int(255 * ko))
        icons.draw_icon(f, "crescent", 1560 + 200, 250, size=120 * ko, metal="gold", alpha=ko, shadow=True)
        c.restore()
    # solda Lascaris: el yazması toplar (kitaplar çuvala)
    kl = ease_out(cx.amt(("c5s15", "el", -0.2), 0.7), 2)
    L.sil(f, "tuccar", 420, FY + 4, 420, t, action="idle", dir=1, seed=27, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kl)
    t_c = cx.at(("c5s15", "toplasın,", -0.6))
    for i in range(8):
        ph = clamp((t - (t_c + 0.17 * i)) / 0.7)
        if 0 < ph < 1.0:
            K4.draw_book_block(c, lerp(560, 400, ph), lerp(300, 600, ph * ph), 96, 28, ["#8E2A1E", "#233C8C", "#3A7A52", "#C79A3C"][i % 4], tilt=0.5 * math.sin(ph * 6 + i))
    kb = clamp((t - t_c) / 1.6)
    if kb > 0:
        K4.draw_book_block(c, 640, FY - 40, 130, 34, "#8E2A1E")
        K4.draw_book_block(c, 640, FY - 74, 120, 32, "#233C8C")
        K4.draw_book_block(c, 640, FY - 106, 110, 30, "#C79A3C")
    # pazarlık: terazi
    kp = ease_out(cx.amt(("c5s15", "pazarlık", -0.4), 0.8), 3)
    if kp > 0.003:
        tl = 0.10 * math.sin(clamp(t - cx.at(("c5s15", "pazarlık", -0.2)), 0, 9) * 3.0) * min(1.0, (t - cx.at(("c5s15", "pazarlık", -0.4))) / 0.6)
        K4.draw_balance(f, 1010, 330, tl, s=0.6 * kp, a=int(255 * kp), lab_l=None, lab_r=None, t=t)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "EL YAZMASI", 560, 190, at=("c5s15", "el", -0.2), size=36, w=360, hold=("c5s15", "pazarlık", -0.3))
    L.tag(f, cx, "II. BAYEZİD", 1560, 190, at=("c5s15", "Bayezid'le", -0.4), size=38, w=420)
    L.tag(f, cx, "PAZARLIK", 1010, 780, at=("c5s15", "pazarlık", -0.3), size=40, w=360)


@CM.ckind("c5_pazarlik")
def k_pazarlik(cx, **kw):
    k_pazarlik_impl(cx, **kw)


# ═══════════════════════════ c5s17: cep defterinde iki şey — istenen metinlerin listesi ve kütüphanenin o günkü içeriği ═══════════════════════════
def k_defter5_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=45, dress=None)
    t = cx.t
    kp = ease_out(cx.amt(("c5s17", -0.1), 0.8), 3)
    # iki sayfa: cep defteri
    PP_sheet(640, 780, seed=121).draw(f, 640, 560 + (1 - kp) * 80, rot=-0.01, scale=1.0, alpha=kp, shadow=0.6)
    PP_sheet(640, 780, seed=122).draw(f, 1280, 560 + (1 - kp) * 80, rot=0.01, scale=1.0, alpha=kp, shadow=0.6)
    c.drawLine(960, 190 + (1 - kp) * 80, 960, 930 + (1 - kp) * 80, S("#3A2616", 4.0, int(200 * kp)))
    k1 = cx.amt(("c5s17", "iki", -0.2), 0.6)
    k2 = cx.amt(("c5s17", "Lorenzo'nun", -0.3), 0.6)
    k3 = cx.amt(("c5s17", "Medici", -0.3), 0.6)
    PP_hand(f, "İSTENEN METİNLER", 640, 300, 50, "#2A1A0E", k2 * kp, seed=2)
    PP_hand(f, "KÜTÜPHANENİN İÇERİĞİ", 1280, 300, 46, "#2A1A0E", k3 * kp, seed=3)
    for side, t0n, n in ((0, cx.at(("c5s17", "iki", 0.4)), 15), (1, cx.at(("c5s17", "kütüphanesinin", -0.3)), 15)):
        for i in range(n):
            kk = clamp((t - (t0n + 0.14 * i)) / 0.5)
            if kk <= 0:
                continue
            xb = 400 if side == 0 else 1040
            y = 380 + i * 36
            R(c, xb, y - 8, xb + 14, y + 6, "#8A6A3A", int(230 * kp))
            rs = _RS(side * 50 + i)
            c.drawLine(xb + 34, y - 1, xb + 34 + rs.uniform(160, 420) * ease_out(kk, 2), y - 1 + rs.uniform(-1.5, 1.5), S("#3A2616", 3.0, int(190 * kp)))
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "CEP DEFTERİ", 640, 120, at=("c5s17", "Cep", -0.2), size=40, sub="JANUS LASCARIS", w=460)
    L.tag(f, cx, "VAT. GR. 1412", 1280, 120, at=("c5s17", "defterinde", -0.2), size=38, w=440)


@CM.ckind("c5_defter")
def k_defter5(cx, **kw):
    k_defter5_impl(cx, **kw)


# ═══════════════════════════ c5s18: Lascaris iki yüz el yazması getirdiğini söyler; defterdeki liste bunun neredeyse iki katı ═══════════════════════════
def k_sayac5_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=46, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -600, 2600, FY, 1300)
    cols = ["#8E2A1E", "#233C8C", "#3A7A52", "#C79A3C", "#6A4A8A", "#7A4A28"]
    # sol: Lascaris'in 200'ü (kitap yığını)
    t_a = cx.at(("c5s18", "iki", -0.2))
    n1 = int(20 * ease_out(clamp((t - t_a) / 2.0), 2.0))
    for i in range(n1):
        K4.draw_book_block(c, 560 + 12 * math.sin(i * 1.7), FY - 4 - i * 17, 250, 17, cols[i % len(cols)], tilt=0.015 * math.sin(i * 2.3))
    ks = ease_out(cx.amt(("c5s18", "iki", -0.3), 0.6), 3)
    if ks > 0.003:
        sp = CM.engraved(CM.fmt_int(200 * ease_out(clamp((t - t_a) / 2.0), 2.0)), "title", 120, 12.0, TH.fg)
        CM.draw_spr(f, sp, 560, 260, "c", alpha=ks, shadow=0.0)
        CM.ink(f, "EL YAZMASI", 560, 335, face="title_m", size=36, color=TH.fg2, align="c", track=10, alpha=ks, emboss=False)
    kb = cx.amt(("c5s18", "söyler;", -0.7), 0.6)
    if kb > 0.003:
        draw_bubble(f, 900, 260, 340, 120, ["“200”"], kb, tail=(-120, 100), size=54)
    # sağ: defterdeki liste: neredeyse iki katı (renksiz, listeleme çubukları)
    t_b = cx.at(("c5s18", "defterdeki", -0.2))
    n2 = int(38 * ease_out(clamp((t - t_b) / 2.2), 2.0))
    for i in range(n2):
        K4.draw_book_block(c, 1360 + 12 * math.sin(i * 1.3), FY - 4 - i * 17, 250, 17, mix(cols[i % len(cols)], "#E8DDBE", 0.55), tilt=0.015 * math.sin(i * 1.9))
    kl = cx.amt(("c5s18", "defterdeki", -0.3), 0.6)
    if kl > 0.003:
        CM.ink(f, "LİSTE", 1360, 150, face="title", size=64, color=TH.fg, align="c", track=14, alpha=kl, emboss=False)
        if n2 > 30:
            dashed(c, 460, FY - 4 - 20 * 17, 1500, FY - 4 - 20 * 17, col="#8E2A1E", w=3.0, a=int(220 * kl), dash=(12.0, 10.0), phase=-t * 30)
    ki = cx.amt(("c5s18", "iki", 1.0), 0.5) if False else cx.amt(("c5s18", "katı.", -0.7), 0.6)
    if ki > 0.003:
        L.tag(f, cx, "NEREDEYSE İKİ KAT", 960, 560, at=("c5s18", "katı.", -0.7), size=44, w=620)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "LASCARIS", 560, 130, at=("c5s18", "Lascaris", -0.2), size=38, w=340, hold=("c5s18", "defterdeki", 0.0))
    L.tag(f, cx, "YUNANİSTAN'DAN", 560, 430, at=("c5s18", "Yunanistan'dan", -0.2), size=30, w=420, hold=("c5s18", "defterdeki", 0.0))


@CM.ckind("c5_sayac")
def k_sayac5(cx, **kw):
    k_sayac5_impl(cx, **kw)


# ═══════════════════════════ c5s19: pazarlığın ayrıntısı bilinmiyor; ama tahtsız efendinin kitap hesabını Osmanlı topraklarında bir Rum bilgin yürütüyordu ═══════════════════════════
def k_bilinmiyor_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=47, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -600, 2600, FY, 1300)
    T = L.OD.OTint("day")
    # A: bulanık pazarlık (ayrıntı bilinmiyor)
    kA = 1.0 - cx.amt(("c5s19", "tahtsız", -0.5), 0.7)
    if kA > 0.003:
        bp = skia.Paint()
        bp.setImageFilter(skia.ImageFilters.Blur(7.0, 7.0))
        bp.setAlphaf(clamp(kA))
        c.saveLayer(skia.Rect.MakeLTRB(380, 200, 1560, 960), bp)
        L.sil(f, "tuccar", 700, FY + 4, 430, t, action="talk", dir=1, seed=27, color="#14100C", rim=None, rim_dir=1, energy=1.2)
        L.sil(f, "kardinal", 1220, FY + 4, 430, t, action="talk", dir=-1, seed=28, color="#14100C", rim=None, rim_dir=-1, energy=1.0)
        c.restore()
        kq = cx.amt(("c5s19", "bilmiyoruz;", -0.5), 0.5) * kA
        if kq > 0.003:
            for q in range(3):
                icons.draw_icon(f, "question", 840 + q * 120, 290 - 30 * (q % 2) + 8 * math.sin(t * 3.0 + q), size=110 * (0.8 + 0.2 * ease_out(kq)), metal="gold", alpha=kq, shadow=True)
    # B: iki yer, bir hesap: Floransa'da boş koltuk (tahtsız) + Osmanlı topraklarında Rum bilgin
    kB = ease_out(cx.amt(("c5s19", "tahtsız", -0.5), 0.9), 3)
    if kB > 0.003:
        import cilt_props as CP
        L.OD.draw_chair(c, T, 420, FY, back_h=360, seat_h=96, w=140, facing=1, col="#6E4524", cushion="#8E2A30")
        CP.draw_arms(f, 420, 280, 110 * kB, alpha=kB, shadow=0.4, glow=0.0, glint=None)
        draw_ottoman(c, 1500, FY, s=1.0, a=int(255 * kB))
        icons.draw_icon(f, "crescent", 1500 + 160, 330, size=100 * kB, metal="gold", alpha=kB, shadow=True)
        L.sil(f, "banker", 1080, FY + 4, 400, t, action="write", dir=1, seed=29, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kB, t0=cx.at(("c5s19", "kitap", -0.3)))
        kk = ease_io(cx.amt(("c5s19", "kitap", -0.1), 1.0), 2)
        if kk > 0.003:
            pth = skia.Path()
            pth.moveTo(520, 560)
            pth.cubicTo(700, 380, 900, 380, 1020, 600)
            pm = skia.PathMeasure(pth, False)
            seg = skia.Path()
            pm.getSegment(0, pm.getLength() * kk, seg, True)
            pp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7.0, Color=C("#C79A3C", 240), StrokeCap=skia.Paint.kRound_Cap)
            pp.setPathEffect(skia.DashPathEffect.Make([18.0, 12.0], -t * 40))
            c.drawPath(seg, pp)
            icons.draw_icon(f, "book_open", 1040, 520, size=130 * kk, metal="gold", alpha=kk, shadow=True)
    L.end(cx, cam, motes_n=14)
    L.stamp_at(f, cx, "KAYITTA YOK", 960, 160, at=("c5s19", "bilmiyoruz;", -0.5), size=56, rot=-0.05, hold=("c5s19", "tahtsız", -0.3))
    L.tag(f, cx, "FLORANSA'NIN TAHTSIZ EFENDİSİ", 480, 130, at=("c5s19", "tahtsız", -0.2), size=30, w=640)
    L.tag(f, cx, "OSMANLI TOPRAKLARI", 1500, 130, at=("c5s19", "Osmanlı", -0.2), size=32, w=520)
    L.tag(f, cx, "RUM BİLGİN", 1080, 190, at=("c5s19", "Rum", -0.2), size=34, w=340)


@CM.ckind("c5_bilinmiyor")
def k_bilinmiyor(cx, **kw):
    k_bilinmiyor_impl(cx, **kw)


# ═══════════════════════════ c5s20–21: Lascaris'in listesi Lorenzo için yazılmıştı; şimdi listenin sahibine, Lorenzo'ya bakalım (parça kapanış: palle) ═══════════════════════════
def k_liste_lorenzo_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=48, dress=None)
    t = cx.t
    kp = ease_out(cx.amt(("c5s20", -0.1), 0.8), 3)
    kf = ease_in(cx.amt(("c5s21", "listenin", -0.3), 0.9), 2)            # liste yukarı kayar ve söner
    y = 540 + (1 - kp) * 100 - 420 * kf
    PP_sheet(560, 740, seed=131).draw(f, 960, y, rot=-0.02 + 0.08 * kf, scale=1.0 - 0.15 * kf, alpha=kp * (1 - kf), shadow=0.6)
    for i in range(14):
        kk = clamp((t - (cx.at(("c5s20", -0.1)) + 0.1 * i)) / 0.5)
        if kk > 0:
            rs = _RS(i)
            c.drawLine(740, y - 270 + i * 38, 740 + rs.uniform(140, 380) * kk, y - 270 + i * 38, S("#3A2616", 2.8, int(190 * kp * (1 - kf))))
    # Lorenzo için: kurdele + mühür
    kr = ease_out(cx.amt(("c5s20", "Lorenzo", -0.3), 0.7), 3)
    if kr > 0.003 and kf < 0.99:
        CM.wax_seal(f, 1090, y + 270, 40, "#A52A1C", alpha=1.0 - kf, t=clamp(kr * 1.2), mono=None, palle=True)
    # kapı: tek palla (kırmızı küre) — iris geçişi buradan açılır (960,491 r=100)
    kg = ease_out(cx.amt(("c5s21", "sahibine,", -0.2), 1.2), 2.6)
    if kg > 0.003:
        SOFT(c, 960, 491, 230 * kg, 230 * kg, "#FFD060", 120 * kg)
        r_ = 100.0 * kg
        sh = skia.GradientShader.MakeRadial((960 - r_ * 0.3, 491 - r_ * 0.35), r_ * 1.6, [C("#FFB09A"), C("#B8261A"), C("#4A0E08")], [0.0, 0.55, 1.0])
        c.drawCircle(960, 491, r_, skia.Paint(AntiAlias=True, Shader=sh))
        c.drawCircle(960, 491, r_, S("#EBCB78", max(2.0, 0.07 * r_), 235))
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "LORENZO İÇİN", 960, 130, at=("c5s20", "Lorenzo", -0.3), size=40, w=480, hold=("c5s21", "listenin", -0.2))
    L.tag(f, cx, "LORENZO", 960, 700, at=("c5s21", "Lorenzo'ya", -0.2), size=48, w=380)


@CM.ckind("c5_liste_lorenzo")
def k_liste_lorenzo(cx, **kw):
    k_liste_lorenzo_impl(cx, **kw)
