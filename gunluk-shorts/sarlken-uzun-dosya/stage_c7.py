"""Bölüm 7 (Sultan: Hiç Karşılaşmadılar) özel çekim türleri. Ad önteki: c7_*"""
import math

import numpy as np
import skia

import icons
import shots as SH
import sk
import stage as ST
import stage_c678 as X
from sk import C, H, back_out, clamp, ease_in, ease_io, ease_out, lerp, mix, seg, smooth
from sk import W as SW

CX = SW / 2
GREEN = "#2F6B4A"
GREEN_L = "#5FA878"


# ───────────────────────────── c7_hukum: iki saltanat, aynı yıllar ─────────────────────────────
@SH.kind("c7_hukum")
@X.pushy(0.035)
def k_hukum(cx, at_axis=0.0, at_bars=0.0, at_overlap=0.0, at_title=None, a0=1510, a1=1560):
    """Şarlken (1516 → 1556) ve Süleyman (1520 →) saltanat çubukları; kesişim = AYNI YILLAR."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.25)
    X.tone(f, GREEN, 0.12, cy=0.5)
    sk.dust(f, cx.t, n=40)
    x0, x1 = 230, 1690
    y_axis = 760

    def XX(yr):
        return lerp(x0, x1, (yr - a0) / (a1 - a0))

    ka = ease_out(clamp((cx.t - cx.at(at_axis)) / 0.9))
    f.line(x0, y_axis, x0 + (x1 - x0) * ka, y_axis, color="#C9962B", sw=4, alpha=0.9)
    for yr in range(a0, a1 + 1, 5):
        xx = XX(yr)
        if xx <= x0 + (x1 - x0) * ka + 1:
            L = 20 if yr % 10 == 0 else 11
            f.line(xx, y_axis - L, xx, y_axis + L, color="#C9962B", sw=2, alpha=0.8)
            if yr % 10 == 0:
                f.text(str(yr), xx, y_axis + 62, face="title_m", size=28, color="#CDBB86", align="c", track=3, alpha=0.9)
    # kesişim bandı
    ko = ease_out(clamp((cx.t - cx.at(at_overlap)) / 0.8))
    xa, xb = XX(1520), XX(1556)
    if ko > 0:
        f.rect(xa, 330, (xb - xa) * ko, y_axis - 330, shader=f.lin(0, 330, 0, y_axis, [("#F0D27A", 0.0, 46), ("#F0D27A", 1.0, 14)]), blend=skia.BlendMode.kPlus)
        for xx in (xa, xb):
            f.line(xx, 340, xx, y_axis, color="#F0D27A", sw=2, alpha=0.7 * ko)
        SH.gold_flat(f, "AYNI YILLAR", (xa + xb) / 2, 290, face="title", size=64, track=10, alpha=ko)
    # çubuklar
    kb = ease_out(clamp((cx.t - cx.at(at_bars)) / 1.0), 2)
    kb2 = ease_out(clamp((cx.t - cx.at(at_bars, off=0.5)) / 1.0), 2)
    # Karl: 1516–1556
    ya = 470
    wa = (XX(1556) - XX(1516)) * kb
    f.rrect(XX(1516), ya, max(1, wa), 84, 14, shader=f.lin(0, ya, 0, ya + 84, [("#F4DC8C", 0.0), ("#C9962B", 0.55), ("#7A5518", 1.0)]), alpha=0.95 * min(1, kb * 3))
    f.rrect(XX(1516), ya, max(1, wa), 84, 14, style="stroke", sw=2.5, color="#FFF1C2", alpha=0.7 * min(1, kb * 3))
    if kb > 0.5:
        f.text("ŞARLKEN", XX(1516) + 24, ya + 56, face="title_m", size=34, color="#2A1A0C", align="l", track=6, alpha=smooth((kb - 0.5) * 3))
    # Süleyman: 1520 → (açık uç)
    yb = 580
    wb = (XX(1560) - XX(1520)) * kb2
    f.rrect(XX(1520), yb, max(1, wb), 84, 14, shader=f.lin(0, yb, 0, yb + 84, [("#7FBF94", 0.0), ("#2F6B4A", 0.55), ("#17382A", 1.0)]), alpha=0.95 * min(1, kb2 * 3))
    f.rrect(XX(1520), yb, max(1, wb), 84, 14, style="stroke", sw=2.5, color="#C6F0D4", alpha=0.7 * min(1, kb2 * 3))
    if kb2 > 0.5:
        f.text("SÜLEYMAN", XX(1520) + 24, yb + 56, face="title_m", size=34, color="#F0FFF4", align="l", track=6, alpha=smooth((kb2 - 0.5) * 3))
        # açık uç oku
        f.poly([(XX(1560) - 30, yb + 10), (XX(1560) + 4, yb + 42), (XX(1560) - 30, yb + 74)], color="#5FA878", alpha=smooth((kb2 - 0.7) * 3))
    # başlangıç yılları
    for yr, yy, col in ((1516, ya, "#F4DD92"), (1520, yb, "#B6E6C6")):
        k = cx.amt(at_bars, 0.5, off=0.2 if yr == 1516 else 0.7)
        if k > 0:
            f.text(str(yr), XX(yr) - 14, yy + 56, face="title", size=36, color=col, align="r", track=3, alpha=k, shadow=(2, 2, 3, "#000000"))
    kk = ease_out(clamp((cx.t - cx.at(at_bars, off=1.1)) / 0.7))
    if kk > 0:
        f.text("1556", XX(1556) + 14, ya + 56, face="title", size=36, color="#F4DD92", align="l", track=3, alpha=kk, shadow=(2, 2, 3, "#000000"))
    f.vig(0.6)


# ───────────────────────────── c7_taht: boş taç + Ferdinand ─────────────────────────────
@SH.kind("c7_taht")
@X.pushy(0.035)
def k_taht(cx, at_crown=0.0, at_title=0.0, at_ferd=0.0, at_plate=None):
    """Çocuğu yoktu: boş taç (soru işaretiyle) → Ferdinand öne çıkar."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.3)
    X.tone(f, "#6A7A38", 0.10, cy=0.5)
    sk.dust(f, cx.t, n=55)
    ac = cx.amt(at_crown, 0.9)
    kf = cx.amt(at_ferd, 0.9)
    xc = lerp(CX, 640, ease_io(kf))
    X.glow(f, xc, 500, 360, "#E3B54A", 0.20 * ac)
    X.ic(f, "crown", xc, 500 + math.sin(cx.t * 1.3) * 7, size=430 * (0.9 + 0.1 * back_out(ac)), metal="gold", alpha=ac, glow=0.35 * ac)
    kq = cx.amt(at_crown, 0.9, off=0.6) * (1 - kf)
    if kq > 0:
        X.ic(f, "question", xc + 250 + math.sin(cx.t * 1.1) * 8, 330, size=150, metal="silver", alpha=0.85 * kq)
    kt = cx.amt(at_title, 0.7)
    if kt > 0:
        SH.kicker(f, "MACARİSTAN TAHTI", CX, 190, alpha=kt, size=34, track=14, face="title_m", color="#E0C682")
    if kf > 0:
        mx = 1330
        SH.draw_medal(f, "ferdinand", mx + (1 - ease_out(kf)) * 260, 480, 520 * (0.94 + 0.06 * ease_out(kf)), "gold", True, alpha=kf, tilt=-0.14 * math.sin(cx.t * 0.55))
        pl = cx.amt(at_plate if at_plate is not None else at_ferd, 0.6, off=0.4)
        SH.name_plate(f, "FERDİNAND", "Şarlken'in kardeşi", None, cx_=mx, y=H * 0.80, t=pl, w=520)
        X.arrow(f, (mx - 290, 480), (xc + 250, 500), ease_out(kf), color="#E3B54A", width=7, bend=-40, alpha=0.9)
    f.vig(0.6)


# ───────────────────────────── c7_vasal: Zapolya → Osmanlı ─────────────────────────────
@SH.kind("c7_vasal")
@X.pushy(0.035)
def k_vasal(cx, at_medal=0.0, at_ott=0.0, at_link=0.0, at_chip=0.0):
    """Rakip aday Zapolya; Osmanlı hilali; aralarında zincir (vasal)."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.3)
    X.tone(f, GREEN, 0.14, cy=0.5)
    sk.dust(f, cx.t, n=55)
    am = cx.amt(at_medal, 0.8)
    SH.draw_medal(f, "zapolya", 560, 490, 500 * (0.94 + 0.06 * ease_out(am)) * (1 + 0.03 * cx.u), "forest", False, alpha=am, tilt=0.14 * math.sin(cx.t * 0.55))
    SH.name_plate(f, "ZAPOLYA", "Rakip aday", None, cx_=560, y=H * 0.80, t=cx.amt(at_medal, 0.6, off=0.4), w=480)
    ao = cx.amt(at_ott, 0.8)
    if ao > 0:
        X.glow(f, 1370, 480, 330, "#5FA878", 0.20 * ao)
        X.ic(f, "crescent", 1370, 480 + math.sin(cx.t * 1.2) * 6, size=380 * (0.9 + 0.1 * back_out(ao)), metal="forest", alpha=ao, glow=0.35 * ao)
        f.text("OSMANLI", 1370, 750, face="title_m", size=42, color="#B6E6C6", align="c", track=12, alpha=ao, shadow=(2, 3, 3, "#000000"))
    # zincir halkaları
    kl = ease_out(clamp((cx.t - cx.at(at_link)) / 0.9))
    if kl > 0:
        x0, x1, y = 830, 1180, 490
        n = 9
        for i in range(n):
            u = (i + 0.5) / n
            if u > kl:
                break
            xx = lerp(x0, x1, u)
            yy = y + math.sin(u * math.pi) * 26
            f.oval(xx, yy, 22, 13, style="stroke", sw=6, color="#B6E6C6" if i % 2 == 0 else "#7FBF94", alpha=0.95)
    kc = cx.amt(at_chip, 0.4)
    if kc > 0:
        X.chip(f, "VASAL", 1005, 420, k=kc, size=34, edge="#5FA878", color="#E6FFF0", padx=34)
    f.vig(0.6)


# ───────────────────────────── c7_unvan: İMPARATOR üstü çizilir → İSPANYA KRALI ─────────────────────────────
@SH.kind("c7_unvan")
@X.pushy(0.035)
def k_unvan(cx, at_doc=None, at_gen=None, at_karl=0.0, at_imp=0.0, at_strike=0.0, at_king=0.0, at_sultan=0.0, at_crown=0.0):
    """Osmanlı belgelerinde Şarlken'in unvanı: İMPARATOR üstü çizilir, İSPANYA KRALI yazılır; imparator = sultan."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.3)
    X.tone(f, GREEN, 0.12, cy=0.5)
    sk.dust(f, cx.t, n=55)
    ak = cx.amt(at_karl, 0.8)
    if at_doc is not None:
        kd = cx.amt(at_doc, 0.7)
        if kd > 0:
            SH.kicker(f, "OSMANLI BELGELERİ", CX, 150, alpha=kd, size=34, track=14, face="title_m", color="#B6E6C6")
            X.ic(f, "scroll", CX, 500, size=340 * (0.9 + 0.1 * back_out(kd)), metal="forest", alpha=kd * (1 - ak), glow=0.3 * kd)
    xk, ys = 520, 430
    SH.draw_medal(f, "karl_olgun", xk, ys, 430 * (0.94 + 0.06 * ease_out(ak)) * (1 + 0.03 * cx.u), "gold", False, alpha=ak, tilt=0.14 * math.sin(cx.t * 0.55))
    # unvan levhası (Karl altı)
    py = H * 0.695
    ai = cx.amt(at_imp, 0.5)
    ks = ease_out(clamp((cx.t - cx.at(at_strike)) / 0.5))
    kk = cx.amt(at_king, 0.5)
    if at_gen is not None:
        kg_ = cx.amt(at_gen, 0.5)
        if kg_ > 0:
            f.text("GENELLİKLE", xk, py - 26, face="cap_i", size=34, color="#C9B27A", align="c", track=8, alpha=kg_, shadow=(2, 2, 3, "#000000"))
    if ai > 0:
        SH.plate(f, xk - 330, py, 660, 130, alpha=ai)
        t1 = "İMPARATOR"
        w1 = sk.text_width(t1, "title", 56, 8)
        f.text(t1, xk, py + 82, face="title", size=56, color="#F4DD92", align="c", track=8, alpha=ai * (1 - 0.55 * ks))
        X.strike_line(f, xk - w1 / 2 - 14, py + 62, xk + w1 / 2 + 14, py + 56, ks, sw=10)
    if kk > 0:
        t2 = "İSPANYA KRALI"
        f.rrect(xk - 330, py + 146, 660, 110, 14, color="#150D08", alpha=0.9 * kk)
        f.rrect(xk - 330, py + 146, 660, 110, 14, style="stroke", sw=3, color="#E3B54A", alpha=kk)
        f.text(t2, xk, py + 220, face="title", size=SH.fit_size(t2, "title", 52, 620, 8), color="#FFF1C2", align="c", track=8, alpha=kk, shadow=(2, 3, 3, "#000000"))
    # sultan
    asu = cx.amt(at_sultan, 0.9)
    if asu > 0:
        xs_ = 1400
        X.glow(f, xs_, ys, 360, "#5FA878", 0.20 * asu)
        SH.draw_medal(f, "suleyman", xs_, ys, 430 * (0.94 + 0.06 * ease_out(asu)), "forest", True, alpha=asu, tilt=-0.14 * math.sin(cx.t * 0.55 + 1))
        kc = cx.amt(at_crown, 0.7)
        if kc > 0:
            X.ic(f, "imperial_crown", xs_, 150 + (1 - ease_out(kc)) * -60, size=160, metal="gold", alpha=kc, glow=0.5 * kc)
            X.chip(f, "İMPARATOR", xs_, H * 0.82, k=kc, size=46, edge="#F0D27A", color="#F4DD92", padx=44, h=100)
            f.text("YALNIZCA SULTAN", xs_, H * 0.82 + 92, face="cap_i", size=32, color="#B6E6C6", align="c", alpha=kc)
    f.vig(0.6)


# ───────────────────────────── c7_yuk: yükü kardeşi taşıdı ─────────────────────────────
@SH.kind("c7_yuk")
@X.pushy(0.035)
def k_yuk(cx, at_title=0.0, at_karl=0.0, at_not=0.0, at_ferd=0.0):
    """Yükün çoğunu Şarlken değil, kardeşi taşıdı: Karl soluk (üstü çizili), Ferdinand parlak."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.3)
    X.tone(f, "#6A7A38", 0.10, cy=0.5)
    sk.dust(f, cx.t, n=55)
    kt = cx.amt(at_title, 0.8)
    if kt > 0:
        SH.gold_flat(f, "YÜKÜN ÇOĞU", CX, 200, face="title", size=82, track=12, alpha=kt)
    ak = cx.amt(at_karl, 0.8)
    kn = ease_out(clamp((cx.t - cx.at(at_not)) / 0.5))
    SH.draw_medal(f, "karl_olgun", 520, 560, 400 * (0.94 + 0.06 * ease_out(ak)), "gold", False, alpha=ak * (1 - 0.55 * kn), tilt=0.1 * math.sin(cx.t * 0.55))
    X.strike_line(f, 360, 420, 680, 700, kn, sw=16)
    if kn > 0:
        X.chip(f, "ŞARLKEN DEĞİL", 520, H * 0.84, k=kn, size=32, edge="#B02A2A", color="#F8E2D8", padx=34)
    af = cx.amt(at_ferd, 0.9)
    if af > 0:
        X.glow(f, 1400, 560, 400, "#E3B54A", 0.24 * af)
        SH.draw_medal(f, "ferdinand", 1400, 560, 540 * (0.92 + 0.08 * ease_out(af)) * (1 + 0.03 * cx.u), "gold", True, alpha=af, tilt=-0.14 * math.sin(cx.t * 0.55))
        SH.name_plate(f, "FERDİNAND", "Kardeşi", None, cx_=1400, y=H * 0.81, t=cx.amt(at_ferd, 0.6, off=0.4), w=480)
    f.vig(0.6)


# ───────────────────────────── c7_gunluk: Osmanlı sefer günlüğü ─────────────────────────────
@SH.kind("c7_gunluk")
def k_gunluk(cx, at=0.0, at_quote=0.0, at_hl=None):
    """Sefer günlüğü sayfası: okunmaz satırlar (karalama) + tek okunur ifade: “İspanya kralı”."""
    from stage_c6 import Paper, scribble, INK
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.28)
    X.tone(f, GREEN, 0.14, cy=0.5)
    sk.dust(f, cx.t, n=45)
    a = cx.amt(at, 0.8)
    sc = (0.95 + 0.05 * ease_out(a)) * (1 + 0.04 * cx.u)
    with Paper(f, CX, 540, 1180, 740, seed=61, tone="#D6C393", rot=-0.012 * (1 - 0.4 * cx.u), sc=sc, alpha=a):
        f.text("OSMANLI SEFER GÜNLÜĞÜ", 0, -285, face="fell", size=50, color=INK, align="c", track=3, alpha=a)
        f.text("1532", 0, -232, face="fell_i", size=36, color="#5A3E1E", align="c", alpha=a * 0.9)
        f.line(-330, -214, 330, -214, color=INK, sw=1.6, alpha=0.6 * a)
        for i in range(3):
            scribble(f, -480, 470 - i * 70, -150 + i * 54, k=clamp((cx.t - (cx.at(at) + 0.5 + i * 0.35)) / 0.8), seed=11 + i)
        f.text("hedef:", -480, 80, face="fell_i", size=44, color="#5A3E1E", align="l", alpha=cx.amt(at_quote, 0.6, off=-0.2))
        s = "“İspanya kralı”"
        wt = sk.text_width(s, "fell", 104, 0)
        k = clamp((cx.t - cx.at(at_quote)) / 0.9)
        f.c.save()
        f.c.clipRect(skia.Rect.MakeXYWH(-wt / 2 - 20, -40, (wt + 40) * k, 190))
        f.text(s, 20, 90, face="fell", size=104, color="#1C0F06", align="c", alpha=1.0)
        f.c.restore()
        hk = clamp((cx.t - cx.at(at_hl if at_hl is not None else at_quote, off=0.5)) / 0.6)
        f.rect(-wt / 2 + 20, 118, wt * hk, 8, color="#C9962B", alpha=0.95 * hk)
        for i in range(2):
            scribble(f, -480, 470 - i * 90, 200 + i * 54, k=clamp((cx.t - (cx.at(at_quote) + 1.0 + i * 0.3)) / 0.8), seed=21 + i)
        SH.wax_seal(f, 440, 285, 56, color=GREEN, t=cx.amt(at_quote, 0.35, off=1.2), mono="S")
    f.vig(0.6)


# ───────────────────────────── c7_ates: ateşkes belgesi ─────────────────────────────
@SH.kind("c7_ates")
def k_ates(cx, at=0.0, at_len=0.0, at_seal=0.0):
    """1547: beş yıllık ateşkes; iki mühür (Süleyman, Ferdinand)."""
    from stage_c6 import Paper, scribble, INK
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.28)
    X.tone(f, GREEN, 0.12, cy=0.5)
    sk.dust(f, cx.t, n=45)
    a = cx.amt(at, 0.8)
    sc = (0.95 + 0.05 * ease_out(a)) * (1 + 0.04 * cx.u)
    with Paper(f, CX, 540, 1120, 700, seed=71, tone="#D9C79A", rot=0.012 * (1 - 0.4 * cx.u), sc=sc, alpha=a):
        f.text("ATEŞKES", 0, -230, face="fell", size=70, color=INK, align="c", track=8, alpha=a)
        f.text("1547", 0, -172, face="fell_i", size=44, color="#5A3E1E", align="c", alpha=a)
        f.line(-320, -150, 320, -150, color=INK, sw=1.8, alpha=0.6 * a)
        for i in range(2):
            scribble(f, -430, 430 - i * 60, -90 + i * 52, k=clamp((cx.t - (cx.at(at) + 0.6 + i * 0.3)) / 0.8), seed=31 + i)
        kl = cx.amt(at_len, 0.6)
        f.text("SÜRE: BEŞ YIL", 0, 70, face="fell", size=84, color="#1C0F06", align="c", alpha=kl)
        f.rect(-300, 96, 600 * clamp((cx.t - cx.at(at_len, off=0.3)) / 0.6), 7, color="#C9962B", alpha=0.95 * kl)
        for i in range(2):
            scribble(f, -430, 430 - i * 90, 170 + i * 50, k=clamp((cx.t - (cx.at(at_len) + 0.9 + i * 0.3)) / 0.8), seed=41 + i)
        ks = cx.amt(at_seal, 0.35)
        SH.wax_seal(f, -250, 285, 58, color=GREEN, t=ks, mono="S")
        SH.wax_seal(f, 250, 285, 58, color="#8E1F26", t=cx.amt(at_seal, 0.35, off=0.25), mono="F")
    f.vig(0.6)
