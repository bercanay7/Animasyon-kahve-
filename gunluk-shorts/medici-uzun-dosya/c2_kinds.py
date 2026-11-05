"""c2_kinds — c2 (Defterin Sihri) için özel çekim türleri. Tümü `c2_` önekli; ana motor dosyalarına dokunmaz.

c2_nolist   : BORÇ ✗ · FAİZ ✗ · KUR FARKI ✓ (üç levha)
c2_hediye   : "faiz değil, hediye" — hediye paketi açılır, FAİZ etiketi çizilir
c2_kasa     : Roma şubesi: ayrı sermaye YOK; kasayı Kilise'nin parası doldurur
c2_borc     : Giovanni → Cossa'ya borç; Cossa papa olur; Konstanz'da indirilir
c2_ayrim    : kefalet mi fidye mi — kaynaklar ayrışıyor (yol ayrımı)
c2_mezar    : Vaftizhane'deki mezar: "ESKİ PAPA" yazıtı oyulur; itiraz damgası; yazıt kalır
c2_rivayet  : rivayet — mitra borca karşılık bırakılır, aforoz tehdidi
c2_katasto  : catasto: 9.780 hane kutusu satır satır yazılır
c2_yil      : 20 Şubat 1429 · Floransa takvimine göre 1428 (yıl ruloları)
c2_kalemler : iki kalem, iki ayrı biçim (Machiavelli · Cavalcanti)
c2_sadaka   : yoksulun ihtiyacını kimse istemeden gideren biri (rivayet; Medici'nin kalemi)
Olgu disiplini: yalnız script'te / brif §7'de geçen ad-sayı-tarih; yüz yok; ölüm/şiddet gösterilmez.
"""
import math

import skia

import cilt_anim as FA
import cilt_cam
import cilt_medal as CMD
import cilt_medici as CM
import cilt_oda as OD
import cilt_paper as PP
import cilt_props as CP
import icons
import sk
from cilt_medici import TH, ckind
from sk import H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth

import c0_kinds as K0
import c1_kinds as K1
import p1_ortak as _P


def _paper_stamp(*a, **k):
    """P1'de bütün damgalar tek dilde: kâğıt fişli, ≥4,5:1 mürekkep (anim.paper_stamp = CM.stamp imzası; kurul tur 2 TE2-Y5, ENG-C isteği)."""
    import anim as _AN
    return _AN.paper_stamp(*a, **k)

_shield = K1._shield


def _bg(f, cx, seed, dress="both"):
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=dress)
    cam.begin(f)
    return cam


def _gilt_or_ink(txt, face, size, track, color=None):
    return K0._gilt_or_ink(txt, face, size, track, color)


# ─────────────────────────────────────────────────────────────────────────────
# c2_nolist — BORÇ ✗ · FAİZ ✗ · KUR FARKI ✓
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c2_nolist")
def k_nolist(cx, borc_at=None, borc_x=None, faiz_at=None, faiz_x=None, kur_at=None, borc_hit=None, seed=2, **_):
    """Kurul tur 3 (AN1-Y-N1): BORÇ levhası çekimin İLK karesinde hazır (borc_at kesmeden önce) — boş parşömen yok; borc_hit: 'borç' sözcüğünde hafif vurgu."""
    f = cx.f
    c = f.c
    cam = _bg(f, cx, seed)
    items = [("BORÇ", borc_at, borc_x, 300, False), ("FAİZ", faiz_at, faiz_x, 860, False), ("KUR FARKI", kur_at, None, 1470, True)]
    for txt, at, xx, x, ok in items:
        k = cx.amt(at, 0.45) if at is not None else 0.0
        if k <= 0.003:
            continue
        w = 460 if not ok else 600
        h = 250
        y = 470
        sc = 0.8 + 0.2 * sk.back_out(k)
        if txt == "BORÇ" and borc_hit is not None:
            sc *= 1.0 + 0.045 * _A.wobble(cx.t, cx.at(borc_hit), 1.0, 1.4, 4.5)
        c.save(); c.translate(x, y); c.scale(sc, sc); c.translate(-x, -y)
        if ok:                                               # parıltı levhanın ARKASINDA (yazının üstünü örtmez; kurul tur 2 TE2-Y5)
            f.circle(x, y, 360, shader=f.rad(x, y, 360, [("#F0D27A", 0.0, int(90 * k)), ("#F0D27A", 1.0, 0)]))
        CM.tablet(f, x - w / 2, y - h / 2, w, h, alpha=k, corner=14, fill=("#F2E5BC", "#DCC58C") if ok else None)
        if ok:                                               # KUR FARKI: koyu mürekkep, düz (oyma değil) → ≥4,5:1 (eski oyma yaldız ≈2,8:1)
            szk = CM.fit_size(txt, "title", 92, w - 70, 8)
            CM.ink(f, txt, x, y + szk * 0.36, face="title", size=szk, color="#2E1C06", align="c", track=8, alpha=k, emboss=False, scrim=False)
        else:
            sp = CM.engraved(txt, "title", int(CM.fit_size(txt, "title", 92, w - 70, 8)), 8.0, TH.fg)
            CM.draw_spr(f, sp, x, y + 32, "c", alpha=k)
        c.restore()
    # çarpılar (BORÇ ve FAİZ) — "yok" sözcüklerinde; yarı saydam ve ince (sözcük çarpının altından okunur kalır; TE2-K6)
    for x, ca in ((300, borc_x), (860, faiz_x)):
        kx = cx.amt(ca, 0.32) if ca is not None else 0.0
        if kx > 0.003:
            p1 = clamp(kx * 2.0)
            p2 = clamp(kx * 2.0 - 1.0)
            y = 470
            R = 130
            f.line(x - R, y - R * 0.55, x - R + 2 * R * p1, y - R * 0.55 + 1.1 * R * p1, color="#A8201A", sw=13, alpha=0.78)
            if p2 > 0:
                f.line(x + R, y - R * 0.55, x + R - 2 * R * p2, y - R * 0.55 + 1.1 * R * p2, color="#A8201A", sw=13, alpha=0.78)
    # KUR FARKI: onay işareti + parıltı
    kc = cx.amt(kur_at, 0.5, off=0.35) if kur_at is not None else 0.0
    if kc > 0.003:
        x, y = 1470, 470
        pth = skia.Path(); pth.moveTo(x - 90, y + 170); pth.lineTo(x - 40, y + 225); pth.lineTo(x + 100, y + 120)
        pm = skia.PathMeasure(pth, False); part = skia.Path(); pm.getSegment(0, pm.getLength() * ease_out(kc, 2), part, True)
        c.drawPath(part, f.paint("#3E7A3A", style="stroke", sw=22, alpha=0.95))
        if kc > 0.5:
            ph = (cx.t * 0.9) % 1.0
            f.circle(x, y, 250 + 120 * ph, style="stroke", sw=4, color="#E8C468", alpha=0.55 * (1 - ph))
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# c2_hediye — "faiz değil, hediye"
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c2_hediye")
def k_hediye(cx, open_at=None, tag_at=None, strike_at=None, gift_at=None, seed=3, **_):
    """'Faiz değil, hediye' — DERİ KESE (kurul SA2-K2: modern hediye kutusu yerine); FAİZ etiketi çizilir, HEDİYE yaldız gelir."""
    f = cx.f
    cam = _bg(f, cx, seed)
    x0, y0 = 960, 560
    kb = cx.amt(tag_at if tag_at is not None else 0.0, 0.45)
    ko = ease_out(clamp((cx.t - cx.at(open_at)) / 0.5), 2) if open_at is not None else 0.0
    bob = 6 * math.sin(cx.t * 3.0)
    f.oval(x0 + 10, y0 + 230, 230, 34, color="#000000", alpha=0.3, blur=8)
    f.circle(x0, y0, 330, shader=f.rad(x0, y0, 330, [("#F0D27A", 0.0, int(60 + 50 * ko)), ("#F0D27A", 1.0, 0)]))
    icons.draw_icon(f, "p1_kese", x0, y0 + bob, size=440 * (0.94 + 0.06 * ko), metal="bronze", alpha=1.0, glow=0.0)
    if ko > 0.2:
        vmax = 0.0
        for i in range(14):
            ph = ((cx.t - cx.at(open_at)) * 0.85 + i * 0.137) % 1.0
            xx = x0 + 170 * math.sin(i * 2.4) * ph
            yy = y0 - 170 - 360 * ph
            CP.draw_coin(f, xx, yy, 66 * (0.7 + 0.3 * ((i % 3) / 2)), spin=cx.t * 9 + i, alpha=min(1.0, ko) * (1 - ph) * 0.95, shadow=0.0)
            vmax = max(vmax, math.hypot(170 * math.sin(i * 2.4), 360.0) * 0.85 / 24.0)     # px/kare (ph hızı 0,85/sn)
        st_ = getattr(cx, "cam_state", None)
        _A.hint_speed(cx, vmax * (getattr(st_, "s", 1.0) or 1.0))        # küçük hızlı nesne: alt-kare deklanşör (AN1-Y7; eşik compose.SHUTTER_V_HINT)
    cam.end(f)
    if kb > 0.003:
        ty = 760
        f.rrect(1180, ty - 70, 360, 120, 12, color="#120C08", alpha=0.72 * kb)
        CM.ink(f, "FAİZ", 1360, ty + 16, face="title", size=72, color="#FFF4D6", align="c", track=10, alpha=kb, emboss=False)
        ks = cx.amt(strike_at, 0.3) if strike_at is not None else 0.0
        if ks > 0.003:
            f.line(1210, ty - 40, 1210 + 300 * ks, ty + 30 * ks, color="#D8382A", sw=12, alpha=0.95)
    kg = cx.amt(gift_at, 0.35) if gift_at is not None else 0.0
    if kg > 0.003:
        sp = _gilt_or_ink("HEDİYE", "title", 140, 12.0)
        CM.draw_spr(f, sp, 960, 190, "c", alpha=kg, scale=0.7 + 0.3 * sk.back_out(kg), shadow=0.5 if not TH.day else 0.0, glow=0.25 * kg if not TH.day else 0.0)
    CM.finish(f, cx, motes_n=26)


# ─────────────────────────────────────────────────────────────────────────────
# c2_kasa — Roma şubesi: ayrı sermaye verilmedi; kasayı Kilise'nin parası doldurdu
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c2_kasa")
def k_kasa(cx, branch_at=None, nocap_at=None, church_at=None, fill_at=None, fill_to=None, seed=4, **_):
    f = cx.f
    c = f.c
    cam = _bg(f, cx, seed)
    cxm, cym = 1100, 560
    # şube levhası
    kb = cx.amt(branch_at, 0.5) if branch_at is not None else 1.0
    if kb > 0.003:
        CM.name_plate(f, "ROMA ŞUBESİ", None, None, cx_=cxm, y=150, t=kb)
    # sermaye kutusu (boş çerçeve): AYRI SERMAYE ✗
    kn = cx.amt(nocap_at, 0.5) if nocap_at is not None else 0.0
    if kn > 0.003:
        # kurul tur 2 (KA2-D7 / TE2-Y4): çarpı YALNIZ kese simgesinin üstünde; "SERMAYE" ve "1426'DA ÇEKİLDİ" (≥36 px) çarpının DIŞINDA, altında
        x, y = 470, 500
        CM.tablet(f, x - 250, y - 150, 500, 330, alpha=kn, corner=12)
        icons.draw_icon(f, "coinbag", x, y - 50, size=150, metal="gold", alpha=kn * 0.85, glow=0.0)
        CM.ink(f, "SERMAYE", x, y + 76, face="title_m", size=40, color=TH.fg, align="c", track=7, alpha=kn, emboss=False, scrim=False)
        CM.ink(f, "1426'DA ÇEKİLDİ", x, y + 132, face="title_m", size=38, color="#7A1A12", align="c", track=4, alpha=kn, emboss=False, scrim=False)   # KA2-Y1 (de Roover)
        kx = cx.amt(nocap_at, 0.32, off=0.35)
        if kx > 0.003:
            for sg in (1, -1):
                f.line(x - 92 * kx, y - 50 - 80 * sg * kx, x + 92 * kx, y - 50 + 80 * sg * kx, color="#A8201A", sw=14, alpha=0.92)
    # kasa (sandık) ve dolan florinler
    prog = ease_io(clamp((cx.t - cx.at(fill_at)) / max(0.4, cx.at(fill_to) - cx.at(fill_at))), 1.6) if fill_at is not None else 0.0
    f.oval(cxm + 8, cym + 270, 330, 44, color="#000000", alpha=0.3, blur=10)
    icons.draw_icon(f, "chest", cxm, cym + 40, size=520, metal="bronze", alpha=1.0, glow=0.0)
    # kasa içi yığın (kapaktan görünür): dolum seviyesiyle büyüyen florin kümesi
    nco = int(prog * 24)
    if nco > 0:
        OD.draw_coins(c, cxm, cym - 60 - 20 * (prog), nco, 2.4, cx.t, seed=3, glint=True)
    # Kilise: haç → florin akışı
    kc = cx.amt(church_at, 0.6) if church_at is not None else 0.0
    if kc > 0.003:
        icons.draw_icon(f, "cross", 1660, 420, size=300 * (0.8 + 0.2 * sk.back_out(kc)), metal="gold", alpha=kc, glow=0.0)
        f.circle(1660, 420, 260, shader=f.rad(1660, 420, 260, [("#F0D27A", 0.0, int(70 * kc)), ("#F0D27A", 1.0, 0)]))
        CM.ink(f, "KİLİSE", 1660, 620, face="title_m", size=40, color=TH.fg, align="c", track=12, alpha=kc, emboss=False)
        if fill_at is not None:
            t0 = cx.at(fill_at)
            for i in range(10):
                u = ((cx.t - t0) * 0.8 + i / 10.0) % 1.0
                if cx.t < t0:
                    break
                e = ease_io(u, 1.4)
                x = lerp(1660, cxm + 40, e)
                y = lerp(420, cym - 120, e) - 150 * math.sin(math.pi * e)
                CP.draw_coin(f, x, y, 60, spin=cx.t * 12 + i, alpha=min(1, u * 5) * min(1, (1 - u) * 5 + 0.2), shadow=0.0)
    cam.end(f)
    CM.finish(f, cx, motes_n=24)



# ─────────────────────────────────────────────────────────────────────────────
# c2_borc — Giovanni → Cossa'ya borç; papa olur; Konstanz'da indirilir
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c2_borc")
def k_borc(cx, give_at=None, pope_at=None, fall_at=None, council_at=None, names_at=None, toff=0.0, seed=3, **_):
    """Sol: Giovanni (bronz madalya). Sağ: Cossa (siluet kardinal). give_at: borç (florin yayı). pope_at: taç gelir. fall_at: taç düşer. council_at: Konstanz levhası + inip vuran tokmak."""
    f = cx.f
    c = f.c
    T = cx.t + toff
    cam = _bg(f, cx, seed)
    # Giovanni
    kg = cx.amt(names_at[0], 0.6) if names_at else 1.0
    CMD.draw_medal_b(f, "m_giovanni", 500, 500, 480, "bronze", False, alpha=kg, tilt=0.14 * math.sin(T * 0.5), glint=((T * 0.26 + 0.2) % 1.8) if ((T * 0.26 + 0.2) % 1.8) < 1 else None)
    if names_at:
        CM.name_plate(f, "GİOVANNİ", "BORÇ VEREN", None, cx_=500, y=720, t=kg, w=500)
    # Cossa: siluet kardinal
    kc = cx.amt(names_at[1], 0.6) if names_at else 1.0
    if kc > 0.003:
        OD.sil_actor(f, "kardinal", 1300, 800, 430, T, action="idle", dir=-1, seed=7, color="#1A1210", rim="#E8B070", rim_dir=-1)
        if names_at:
            CM.name_plate(f, "BALDASSARRE COSSA", "KİLİSE ADAMI", None, cx_=1300, y=95, t=kc, w=680)
    # borç: florin yayı
    if give_at is not None:
        t0 = cx.at(give_at)
        for i in range(7):
            u = (cx.t - (t0 + 0.13 * i)) / 0.95
            if 0 < u < 1:
                e = ease_io(u, 1.6)
                x = lerp(640, 1230, e)
                y = lerp(500, 520, e) - 190 * math.sin(math.pi * e)
                CP.draw_coin(f, x, y, 70, spin=T * 13 + i, alpha=min(1, u * 6) * min(1, (1 - u) * 6 + 0.1), shadow=0.2)
        kb = cx.amt(give_at, 0.4, off=-0.1)
        if kb > 0.003:
            CM.ink(f, "BORÇ", 900, 690, face="title", size=64, color=TH.acc, align="c", track=22, alpha=kb, emboss=False)
    # taç (papa) — Cossa'nın başı üstünde
    cr_x, cr_y = 1300, 320
    kp = cx.amt(pope_at, 0.6) if pope_at is not None else 0.0
    kf = ease_in(clamp((cx.t - cx.at(fall_at)) / 0.9), 2.2) if fall_at is not None else 0.0
    if kp > 0.003 and kf < 1.0:
        yy = cr_y + 620 * kf
        rot = 0.9 * kf * (1 if kf else 0)
        f.circle(cr_x, cr_y, 150, shader=f.rad(cr_x, cr_y, 150, [("#F0D27A", 0.0, int(110 * kp * (1 - kf))), ("#F0D27A", 1.0, 0)]))
        icons.draw_icon(f, "crown", cr_x, yy + 8 * math.sin(T * 2.4) * (1 - kf), size=200 * (0.7 + 0.3 * sk.back_out(kp)), metal="gold", alpha=kp * (1 - 0.7 * kf), rot=rot, glow=0.0)
        if names_at and len(names_at) > 2:
            CM.name_plate(f, "XXIII. JOHANNES", "PAPA", None, cx_=1650, y=440, t=kp * (1 - kf), w=480)
    # Konstanz: konsil levhası + tokmak
    kk = cx.amt(council_at, 0.5) if council_at is not None else 0.0
    if kk > 0.003:
        CM.tablet(f, 100, 50, 760, 110, alpha=kk, corner=10)
        CM.ink(f, "KONSTANZ KONSİLİ · 1415", 480, 125, face="title_m", size=46, color=TH.fg, align="c", track=8, alpha=kk, emboss=False)
        if fall_at is not None:
            kh = clamp((cx.t - cx.at(fall_at) + 0.5) / 0.35)
            hy = lerp(180, 430, ease_in(kh, 2.0))
            if 0 < kh < 1.3:
                icons.draw_icon(f, "gavel", 1300, hy, size=170, metal="gold", alpha=min(1, kh * 3) * (1 - clamp((kh - 1.0) * 3)), rot=-0.5 + 0.9 * clamp(kh), glow=0.0)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# c2_ayrim — kefalet mi, fidye mi: kaynaklar ayrışıyor
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c2_ayrim")
def k_ayrim(cx, walk_at=None, fork_at=None, left_at=None, right_at=None, stamp_at=None, seed=5, **_):
    f = cx.f
    c = f.c
    cam = _bg(f, cx, seed, dress="both")
    gy = 880
    # yol: ayrımdan iki yana açılan şerit
    fx, fy = 960, 520
    road = "#CDB98A"
    def band(p0, p1, w0, w1):
        a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        nx, ny = -math.sin(a), math.cos(a)
        return sk.poly_path([(p0[0] + nx * w0, p0[1] + ny * w0), (p1[0] + nx * w1, p1[1] + ny * w1), (p1[0] - nx * w1, p1[1] - ny * w1), (p0[0] - nx * w0, p0[1] - ny * w0)])
    kf = cx.amt(fork_at, 0.8) if fork_at is not None else 1.0
    c.drawPath(band((960, 960), (fx, fy), 150, 60), f.paint(road))
    for sg in (-1, 1):
        c.drawPath(band((fx, fy), (fx + sg * 520 * kf, fy - 230 * kf), 60, 40), f.paint(road, alpha=kf))
    for sg in (-1, 1):
        f.line(960 + sg * 150, 960, fx + sg * 60, fy, color="#8A7650", sw=4, alpha=0.8)
    # yön levhaları
    for (txt, ic, at, sg, x) in (("KEFALET", "scroll", left_at, -1, 380), ("FİDYE", "coinbag", right_at, 1, 1540)):
        k = cx.amt(at, 0.5) if at is not None else 0.0
        if k <= 0.003:
            continue
        y = 330
        f.rect(x - 8, y, 16, 330, color="#6A4A2A", alpha=k)
        CM.tablet(f, x - 190, y - 120, 380, 150, alpha=k, corner=10)
        icons.draw_icon(f, ic, x - 110, y - 46, size=92, metal="gold", alpha=k, glow=0.0)
        CM.ink(f, txt, x + 30, y - 36, face="title_m", size=40, color=TH.fg, align="c", track=8, alpha=k, emboss=False)
        # ok
        f.poly([(x + sg * 160, y + 150), (x + sg * 230, y + 190), (x + sg * 160, y + 230)], color="#A8321E", alpha=k)
    # yürüyen siluet; ayrımda iki "hayalet" ayrılır
    t0 = cx.at(walk_at) if walk_at is not None else 0.0
    u = clamp((cx.t - t0) / 4.5)
    if cx.t >= t0 - 0.1:
        e = ease_io(clamp(u / 0.55), 1.5)
        x = 960
        y = lerp(980, 600, e)
        h = lerp(520, 260, e)
        if u < 0.55:
            K0._sil_person(f, x, y, h, T0 := cx.t * 5.0, 0.55, "plain", alpha=1.0, col="#2A1E15")
        else:
            s2 = ease_out(clamp((u - 0.55) / 0.45), 2)
            for sg in (-1, 1):
                K0._sil_person(f, 960 + sg * 280 * s2, 600 - 80 * s2, 260 - 30 * s2, cx.t * 5.0 + sg, 0.55, "plain", alpha=0.78, col="#2A1E15")
    # ? ve damga
    ks = cx.amt(stamp_at, 0.3) if stamp_at is not None else 0.0
    if ks > 0.003:
        _paper_stamp(f, "KAYNAKLAR AYRIŞIYOR", 960, 130 + 20, rot=-0.04, size=56, t=ks)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# c2_mezar — Vaftizhane'deki mezar: yazıt oyulur; itiraz damgası; yazıt kalır
# ─────────────────────────────────────────────────────────────────────────────
MEZAR_YAZIT = "IOANNES QVONDAM PAPA"     # kurul tur 2 (SA2-Y8, KA1, KA2-D5; başkan kararı): taşta özgün Latince; Türkçesi altta levhada ("ESKİ PAPA · ÇEVİRİ BİZE AİT")


@ckind("c2_mezar")
def k_mezar(cx, place_at=None, carve_at=None, carve_to=None, protest_at=None, stay_at=None, seed=2, text=MEZAR_YAZIT, **_):
    """Vaftizhane duvar anıtı (sadeleştirilmiş Donatello–Michelozzo düzeni): kemerli niş, iki yana açılan perde (baldaken), yatan tunç figür (gisant),
    lahdin önünde AÇIK KREM yazıt levhası, harfler KOYU oyma (kontrast ≥7:1) ve ortalı. Martinus itirazı: mühür (anahtarlar bow aşağıda) + İTİRAZ."""
    f = cx.f
    c = f.c
    cam = _bg(f, cx, seed, dress="top")
    gy = 900
    # duvar: taş + mermer şeritleri
    f.rect(230, 170, 1460, gy - 170, shader=f.lin(0, 170, 0, gy, [("#C9BB98", 0.0), ("#A99A76", 1.0)]))
    for yy in range(210, gy, 92):
        c.drawLine(230, yy, 1690, yy, f.paint("#7A6A4C", style="stroke", sw=1.4, alpha=0.35))
    # niş (kemer) — koyu iç, ışıklı kenar
    arch = skia.Path(); arch.moveTo(500, gy - 60); arch.lineTo(500, 470); arch.arcTo(skia.Rect.MakeLTRB(500, 230, 1420, 710), 180, 180, False); arch.lineTo(1420, gy - 60); arch.close()
    c.drawPath(arch, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 230), (0, gy)], [sk.C("#3E3226"), sk.C("#5E4E3A")], [0, 1])))
    c.drawPath(arch, f.paint("#E6D8B4", style="stroke", sw=18))
    c.drawPath(arch, f.paint("#2A1A0C", style="stroke", sw=3, alpha=0.8))
    # baldaken: tepedeki halkadan iki yana açılan perde
    f.circle(960, 252, 16, color="#D2A33E")
    for sg, ph in ((-1, 0.2), (1, 1.3)):
        OD.draw_drape(c, 960 + sg * 300 - 80, 262, 160, 330, cx.t, col="#3E5A44", col2="#C9A45A", amp=0.035, seed=4, ph=ph, tie=0.75)
    # lahit + üstünde sedir üzerinde yatan tunç figür
    f.rect(600, 610, 720, 52, color="#D8CBA6")
    f.rect(600, 610, 720, 52, style="stroke", sw=3, color="#3A2A18", alpha=0.85)
    OD.lying_sil(f, 690, 600, cx.t, 1.05, color="#5A3A1E", rim="#E8C470", rim_dir=1, breath=0.0)
    f.rect(570, 662, 780, 190, shader=f.lin(0, 662, 0, 852, [("#E2D6B2", 0.0), ("#B4A57E", 1.0)]))
    f.rect(570, 662, 780, 190, style="stroke", sw=3, color="#3A2A18", alpha=0.85)
    # yazıt levhası: açık krem, ortalı; harfler koyu oyma, harf harf (Latince özgün yazıt; tek satır)
    pw, ph = 740, 104
    px, py = 960 - pw / 2, 700
    f.rect(px, py, pw, ph, shader=f.lin(0, py, 0, py + ph, [("#F6EED6", 0.0), ("#E6DAB8", 1.0)]))
    f.rect(px, py, pw, ph, style="stroke", sw=3, color="#2A1A0C", alpha=0.9)
    txt = text
    ta = cx.at(carve_at) if carve_at is not None else 0.0
    tb = cx.at(carve_to) if carve_to is not None else ta + 1.2
    p = clamp((cx.t - ta) / max(0.3, tb - ta))
    n = len(txt)
    trk = 5.0
    sz = int(CM.fit_size(txt, "title", 54, pw - 64, trk))
    wid = sk.text_width(txt, "title", sz, trk)
    pos = 960 - wid / 2
    for i, ch in enumerate(txt):
        wch = sk.text_width(ch, "title", sz, trk)
        ki = clamp(p * (n + 2) - i)
        if ki > 0 and ch != " ":
            CM.ink(f, ch, pos + wch / 2 + 1.8, py + ph / 2 + sz * 0.36 + 1.8, face="title", size=sz, color="#FFF8E0", align="c", track=0.0, alpha=0.85 * ki, emboss=False, scrim=False, log=False)
            CM.ink(f, ch, pos + wch / 2, py + ph / 2 + sz * 0.36, face="title", size=sz, color="#1E1006", align="c", track=0.0, alpha=ki, emboss=False, scrim=False)
        pos += wch
    gl = ((cx.t - ta - 1.0) * 0.5) % 2.2
    if cx.t > ta + 1.0 and gl < 1.0:
        gxp = px + pw * gl
        f.rect(gxp - 22, py, 44, ph, shader=f.lin(gxp - 22, 0, gxp + 22, 0, [("#FFF4C0", 0.0, 0), ("#FFF4C0", 0.5, 120), ("#FFF4C0", 1.0, 0)]))
    for cxx, sd in ((440, 3.1), (1480, 5.2)):
        OD.candle(f, cxx, 860, 130, cx.t, sd, lit=1.0, holder=True)
    kpr = cx.amt(protest_at, 0.3) if protest_at is not None else 0.0
    cam.end(f)
    kpl = cx.amt(place_at, 0.6) if place_at is not None else 1.0
    if kpl > 0.003:
        CM.name_plate(f, "VAFTİZHANE", "COSSA'NIN MEZARI", None, cx_=760, y=150, t=kpl, w=640)
    if kpr > 0.003:
        CM.wax_seal(f, 1560, 420, 74, "#7A1A14", alpha=1.0, t=kpr, palle=False)
        icons.draw_icon(f, "p1_anahtar", 1560, 420, size=78, metal="gold", alpha=kpr, glow=0.0, shadow=False)
        CM.ink(f, "V. MARTİNUS", 1560, 540, face="title_m", size=36, color="#FFF4D6", align="c", track=8, alpha=kpr, emboss=False)
        _paper_stamp(f, "İTİRAZ", 1520, 640, rot=-0.10, size=72, t=kpr)
    ks = cx.amt(stay_at, 0.8) if stay_at is not None else 0.0
    if ks > 0.003:
        gg = (cx.t * 0.7) % 1.6
        if gg < 1.0:
            a = math.sin(gg * math.pi)
            R = 120
            f.circle(960, py + 52, R * (0.6 + 0.7 * gg), shader=f.rad(960, py + 52, R * 1.4, [("#FFF1B8", 0.0, int(110 * a * ks)), ("#FFF1B8", 1.0, 0)]))
    CM.finish(f, cx, motes_n=24)


# ─────────────────────────────────────────────────────────────────────────────
# yardımcı: mitra simgesi
# ─────────────────────────────────────────────────────────────────────────────
@icons.icon("c2_mitra")
def _i_mitra(m):
    """Mitra (rehin bırakılan; de Roover n. 45): gövde, ortada işlemeli dikey kuşak (titulus), tabanda yatay kuşak (circulus), kuşaklarda
    inci dizisi, titulusun üstünde küçük Latin haçı. Kurul tur 3 SA2-Y10: eski çizimdeki dikey çizgi + baklava + ters V, Othala rününe (ᛟ)
    benzeyen uydurma bir işaret oluşturuyordu → tamamen kaldırıldı; yalnız gerçek mitra süslemesi."""
    def ring(x, y, r):
        pth = skia.Path()
        pth.addCircle(x, y, r)
        return pth
    m.smooth([(120, 440), (140, 200), (256, 70), (372, 200), (392, 440)], close=True, t=0.25, v=205)   # gövde (kuşaklardan alçak)
    m.poly([(230, 98), (282, 98), (288, 410), (224, 410)], v=255)                                       # titulus (yükseltilmiş kuşak)
    m.rect(104, 404, 304, 60, r=12, v=255)                                                              # circulus
    m.cut(sk.poly_path([(230, 104), (225, 404)], False), 4)
    m.cut(sk.poly_path([(282, 104), (287, 404)], False), 4)
    m.cut(sk.poly_path([(110, 405), (402, 405)], False), 4)
    m.cut(sk.poly_path([(256, 122), (256, 186)], False), 7)                                             # Latin haçı (dikey)
    m.cut(sk.poly_path([(236, 144), (276, 144)], False), 7)                                             # Latin haçı (yatay)
    for yy in range(222, 396, 34):                                                                       # titulus incileri
        m.cut(ring(256, yy, 9), 3)
    for xx in (138, 176, 214, 298, 336, 374):                                                            # circulus incileri
        m.cut(ring(xx, 434, 9), 3)


@icons.icon("c2_bulla")
def _i_bulla(m):
    m.rect(120, 90, 272, 330, r=18)
    for i in range(7):
        m.cut(sk.poly_path([(160, 150 + i * 36), (352, 150 + i * 36)], False), 6)
    m.circle(256, 440, 52)
    m.cut(sk.poly_path([(256, 418), (256, 462)], False), 6)


# ─────────────────────────────────────────────────────────────────────────────
# c2_rivayet — mitra borca karşılık bırakılır; Martinus aforozla tehdit eder (BELGELİ: de Roover n. 45 — teyit_P1; eski adı korunur)
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c2_rivayet")
def k_rivayet(cx, src_at=None, med_at=None, pawn_at=None, ask_at=None, threat_at=None, medal=True, src=("DE ROOVER", "ANDIĞI ARŞİV BELGELERİ"),
              src_stamp="BELGE · DE ROOVER", pawn_label="BORÇ", seed=4, **_):
    f = cx.f
    c = f.c
    cam = _bg(f, cx, seed)
    ks = cx.amt(src_at, 0.6) if src_at is not None else 0.0
    # sol: Giovanni madalyası (isteğe bağlı), orta: mitra (yastıkta, etiket), sağ: Martinus siluet
    if medal:
        kmed = cx.amt(med_at, 0.6) if med_at is not None else 1.0
        CMD.draw_medal_b(f, "m_giovanni", 400, 560, 430 * (0.92 + 0.08 * kmed), "bronze", False, alpha=kmed, tilt=0.12 * math.sin(cx.t * 0.5), glint=None)
    kp = cx.amt(pawn_at, 0.6) if pawn_at is not None else 0.0
    mx, my = 960, 600
    if kp > 0.003:
        # yastık
        f.oval(mx, my + 120, 190, 38, color="#000000", alpha=0.3 * kp, blur=8)
        f.rrect(mx - 170, my + 70, 340, 70, 30, shader=f.lin(0, my + 70, 0, my + 140, [("#8E2A30", 0.0), ("#5A1A20", 1.0)]), alpha=kp)
        f.rrect(mx - 170, my + 70, 340, 70, 30, style="stroke", sw=3, color="#D8B25A", alpha=0.9 * kp)
        icons.draw_icon(f, "c2_mitra", mx, my - 40 + 6 * math.sin(cx.t * 2.0), size=300 * (0.8 + 0.2 * sk.back_out(kp)), metal="gold", alpha=kp, glow=0.0)
        f.circle(mx, my - 40, 230, shader=f.rad(mx, my - 40, 230, [("#F0D27A", 0.0, int(70 * kp)), ("#F0D27A", 1.0, 0)]))
        lw_ = max(240.0, sk.text_width(pawn_label, "title_m", 40, 8) + 70)
        CM.tablet(f, mx - lw_ / 2, my + 160, lw_, 74, alpha=kp, rot=-0.04, corner=8)
        CM.ink(f, pawn_label, mx, my + 212, face="title_m", size=40, color=TH.fg, align="c", track=8, alpha=kp, emboss=False)
    # Martinus: siluet, sağ elini uzatır (işaret)
    kq = cx.amt(ask_at, 0.6) if ask_at is not None else 0.0
    if kq > 0.003:
        OD.sil_actor(f, "papa", 1520, 880, 430, cx.t, action="point", dir=-1, seed=9, color="#1A1210", rim="#E8B070", rim_dir=-1, alpha=kq)
        CM.name_plate(f, "V. MARTİNUS", "PAPA", None, cx_=1520, y=250, t=kq, w=520)
    # geri alma: mitra Martinus'a doğru kayar (talep), sonra aforoz tehdidi: mühürlü ferman Giovanni'ye iner
    kt = cx.amt(threat_at, 0.5) if threat_at is not None else 0.0
    if kt > 0.003:
        u = ease_io(clamp((cx.t - cx.at(threat_at)) / 1.3), 1.7)
        bx = lerp(1350, 560, u)
        by = lerp(380, 400, u) - 140 * math.sin(math.pi * u)
        icons.draw_icon(f, "c2_bulla", bx, by, size=220 * (0.7 + 0.3 * kt), metal="gold", alpha=kt, rot=-0.18 + 0.4 * u, glow=0.0)
        _paper_stamp(f, "AFOROZ TEHDİDİ", 1000, 845, rot=-0.04, size=56, t=cx.amt(threat_at, 0.3, off=0.5))
    cam.end(f)
    CM.finish(f, cx, motes_n=24)
    # kaynak levhası + kaynak damgası EKRAN UZAYINDA (kamera eğmesiyle kenardan taşmasın; HUD'dan uzak) — kurul teyit: olay belgeli → ANEKDOT/RİVAYET değil
    if ks > 0.003:
        CM.name_plate(f, src[0], src[1], None, cx_=600, y=170, t=ks, w=640)
        if src_stamp:
            _paper_stamp(f, src_stamp, 1180, 300, rot=-0.06, size=54, t=cx.amt(src_at, 0.3, off=0.6))


# ─────────────────────────────────────────────────────────────────────────────
# c2_katasto — 9.780 hane kutusu satır satır yazılır
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c2_katasto")
def k_katasto(cx, write_at=None, write_to=None, title_at=None, card_at=None, seed=3, **_):
    f = cx.f
    c = f.c
    cam = _bg(f, cx, seed, dress="both")
    COLS, ROWS = 163, 60
    cw, ch = 10.4, 9.0
    x0 = 960 - COLS * cw / 2
    y0 = 300
    ta = cx.at(write_at) if write_at is not None else 0.0
    tb = cx.at(write_to) if write_to is not None else ta + 4.0
    p = ease_io(clamp((cx.t - ta) / max(0.4, tb - ta)), 1.3)
    total = COLS * ROWS
    nshow = int(total * p)
    # çerçeve + kâğıt
    f.rrect(x0 - 28, y0 - 24, COLS * cw + 56, ROWS * ch + 48, 10, color="#EADFBE", alpha=0.96)
    f.rrect(x0 - 28, y0 - 24, COLS * cw + 56, ROWS * ch + 48, 10, style="stroke", sw=3, color="#5A3E22", alpha=0.85)
    # hane kutuları (kolon kolon yazılır: soldan sağa akan şerit)
    full_cols = nshow // ROWS
    for ci in range(min(COLS, full_cols + 1)):
        rows_here = ROWS if ci < full_cols else nshow % ROWS
        xx = x0 + ci * cw
        for ri in range(rows_here):
            h = (ci * 131 + ri * 17) % 11
            col = "#6A4A2A" if h > 1 else "#8A6A3E"
            c.drawRect(skia.Rect.MakeXYWH(xx + 1.2, y0 + ri * ch + 1.2, cw - 2.6, ch - 2.6), f.paint(col, alpha=0.85))
    # kalem: yazım ucu
    if 0 < p < 1:
        ci = min(COLS - 1, nshow // ROWS)
        ri = nshow % ROWS
        OD.quill(c, x0 + ci * cw + 4, y0 + ri * ch + 6, -58.0, 0.9)
    # sayaç: hane sayısı
    kt = cx.amt(title_at, 0.5) if title_at is not None else 1.0
    if kt > 0.003:
        CM.ink(f, "CATASTO · 1427", 960, 180, face="title", size=64, color=TH.fg, align="c", track=16, alpha=kt, emboss=False)
    cnt = int(9780 * p)
    CM.ink(f, f"{CM.fmt_int(cnt)} HANE", 960, 905, face="title_m", size=46, color=TH.acc, align="c", track=10, alpha=0.95, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=20)


# ─────────────────────────────────────────────────────────────────────────────
# c2_yil — 20 Şubat 1429 · Floransa takvimine göre hâlâ 1428
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c2_yil")
def k_yil(cx, date_at=None, snuff_at=None, roll_at=None, cal_at=None, seed=2, **_):
    f = cx.f
    c = f.c
    cam = _bg(f, cx, seed)
    # sol: mum (öldü → söner)
    cxm, cym = 420, 820
    lit = 1.0 - (cx.amt(snuff_at, 0.5) if snuff_at is not None else 0.0)
    OD.candle(f, cxm, cym, 330, cx.t, 6.1, lit=lit, holder=True)
    # tarih levhası
    kd = cx.amt(date_at, 0.6) if date_at is not None else 1.0
    if kd > 0.003:
        CM.tablet(f, 700, 230, 1000, 360, alpha=kd, corner=16)
        CM.ink(f, "20 ŞUBAT", 1200, 340, face="title_m", size=54, color=TH.fg, align="c", track=14, alpha=kd, emboss=False)
        # yıl ruloları
        yr_old, yr_new = "1429", "1428"
        e = ease_io(clamp((cx.t - cx.at(roll_at)) / 1.1), 2.0) if roll_at is not None else 0.0
        size = 170
        cwid = sk.text_width("0", "title", size, 4) + 4
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(900, 360, 1500, 560))
        for i in range(4):
            xx = 1200 - cwid * 4 / 2 + cwid / 2 + i * cwid
            if yr_old[i] != yr_new[i] and e < 1.0:
                CM.ink(f, yr_old[i], xx, 520 + 150 * e, face="title", size=size, color=TH.fg, align="c", alpha=kd * (1 - e), emboss=False)
                CM.ink(f, yr_new[i], xx, 520 - 150 * (1 - e), face="title", size=size, color=TH.acc, align="c", alpha=kd * e, emboss=False)
            else:
                CM.ink(f, yr_new[i] if e >= 1.0 else yr_old[i], xx, 520, face="title", size=size, color=TH.acc if (e >= 1.0 and yr_old[i] != yr_new[i]) else TH.fg, align="c", alpha=kd, emboss=False)
        c.restore()
    kc = cx.amt(cal_at, 0.6) if cal_at is not None else 0.0
    if kc > 0.003:
        CM.tablet(f, 700, 650, 1000, 120, alpha=kc, corner=10)
        CM.ink(f, "FLORANSA TAKVİMİ · YILBAŞI 25 MART", 1200, 730, face="title_m", size=34, color=TH.fg, align="c", track=8, alpha=kc, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=24, light=CM.candle_light(cx.t, 3, base=(W * 0.5, H * 0.5), r=1400.0, sway=6.0))


# ─────────────────────────────────────────────────────────────────────────────
# c2_kalemler — iki kalem, iki ayrı biçim
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c2_kalemler")
def k_kalemler(cx, left_at=None, right_at=None, q_at=None, stamp_at=None, write_a=None, write_b=None, only=None, seed=5, lines_a=None, lines_b=None,
               full=False, orig=True, plate=True, **_):
    """İki kalem, iki biçim. Sayfalar kamera uzayında; İSİM LEVHALARI ve ANEKDOT damgası EKRAN uzayında.
    Kurul tur 2 (AN2-K2, TE2 §5): dalgalı 'yer tutucu' çizgiler YOK — sayfada GERÇEK harfler: anahtar söz anlatımdakiyle BİREBİR (Türkçe, mürekkep el yazısı;
    lines_a/lines_b = [(metin, çapa, vurgu)] satır satır çapada yazılır; full=True → tamamı yazılmış). orig=True: sayfa başında kaynağın kendi sözleri
    (İtalyanca, soluk el yazısı dokusu; teyit_P1 c2s29 MAC IV 'Muoio contento' · c2s30 CAV IV 'per passare ai perpetuali riposi'), write_a/write_b çapasında akar.
    Ölü açılış yok (AN1-Y6/SA1-Y4): left_at/right_at verilmezse sayfalar çekimin İLK karesinde hazırdır.
    Kurul tur 3: Machiavelli sayfasında 'invidia' (kıskançlık) geçen özgün cümle (teyit_P1.md:92, MAC IV — sözcükler ve noktalama birebir); İtalyanca
    satırlar 27 px / 34 px aralık (dört satır Türkçe blokla çakışmaz). plate=False: ad levhası çizilmez (sahne önceki çekimle AYNI levhayı ovl'da verir)."""
    f = cx.f
    c = f.c
    cam = _bg(f, cx, seed)
    ORIG = {"a": ["…Muoio contento…", "…non vi recherà mai né invidia né pericolo,", "perché quello che l'uomo si toglie,", "non quello che all'uomo è dato…"],
            "b": ["…non debbe aver dolore del partimento", "dalle mondane sollecitudini,", "per passare ai perpetuali riposi…"]}
    OSZ, OSP = 27, 34                                         # İtalyanca punto ve satır aralığı (eskisi 30 / 40)
    pages = ((520, "MACHİAVELLİ", "BİR ASRA YAKIN SONRA", left_at, write_a, lines_a, 11, "a"), (1400, "CAVALCANTİ", "1430'LAR · HAPİSTE", right_at, write_b, lines_b, 17, "b"))
    ks_ = {}
    for (x, name, role, at, wa, lines, sd, key) in pages:
        if only and key != only:
            continue
        k = cx.amt(at, 0.6) if at is not None else 1.0
        ks_[key] = k
        if k <= 0.003:
            continue
        pw, ph, py = 620, 560, 300
        yy = py + (1 - k) * 40
        x0 = x - pw / 2
        f.rrect(x0 + 8, yy + 12, pw, ph, 10, color="#000000", alpha=0.28 * k, blur=10)
        f.rrect(x0, yy, pw, ph, 8, shader=f.lin(0, yy, 0, yy + ph, [("#F3E9C9", 0.0), ("#E3D4A6", 1.0)]), alpha=k)
        f.rrect(x0, yy, pw, ph, 8, style="stroke", sw=3, color="#5A3E22", alpha=0.85 * k)
        tip = None
        if orig:                                              # kaynağın kendi sözleri: soluk el yazısı (sayfanın üst kısmı)
            ta = cx.at(wa) if wa is not None else -1e9
            ol = ORIG[key]
            for i, ln in enumerate(ol):
                pr = 1.0 if full else clamp((cx.t - ta - i * 0.75) / 0.85)
                if pr <= 0:
                    continue
                ly = yy + 66 + i * OSP
                wl = sk.text_width(ln, "fell_i", OSZ)
                c.save()
                c.clipRect(skia.Rect.MakeLTRB(x0 + 40, ly - 36, x0 + 46 + wl * pr, ly + 12))
                PP.hand(f, ln, x0 + 46, ly, face="fell_i", size=OSZ, color="#5A4630", alpha=0.62 * k, jitter=0.8, seed=sd + i)
                c.restore()
                if 0 < pr < 1:
                    tip = (x0 + 46 + wl * pr, ly)
        for i, it in enumerate(lines or ()):                    # anahtar söz: anlatımdakiyle birebir, satır satır
            txt, la = it[0], it[1]
            hl = it[2] if len(it) > 2 else False
            ly = yy + (230 if orig else 110) + i * (64 if orig else 74)     # özgün alıntının altında sıkı aralık: 4. satır, altyazı bandının
                                                                            # üstündeki 'ÖZET' levhalarına binmesin (başkan, tur 3 → v3.1)
            wl = sk.text_width(txt, "fell_i", 46)
            dur_ = max(0.5, min(1.1, 0.055 * len(txt)))
            pr = 1.0 if full else clamp((cx.t - cx.at(la)) / dur_)
            if pr <= 0:
                continue
            xl = x0 + 44
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(xl - 6, ly - 52, xl + 4 + wl * pr, ly + 18))
            PP.hand(f, txt, xl, ly, face="fell_i", size=46, color="#24160A", alpha=k, jitter=1.0, seed=sd * 3 + i)
            c.restore()
            if hl and pr >= 1.0:                               # vurgu: kızıl mürekkep alt çizgi
                ku = 1.0 if full else clamp((cx.t - cx.at(la) - dur_) / 0.4)
                c.drawLine(xl, ly + 10, xl + wl * ku, ly + 12, f.paint("#A8321E", style="stroke", sw=3.2, alpha=0.9 * k))
            if 0 < pr < 1:
                tip = (xl + wl * pr, ly)
        if tip is not None:
            OD.quill(c, tip[0] + 6, tip[1] + 4, -58.0, 0.9)
    kq = cx.amt(q_at, 0.5) if q_at is not None else 0.0
    if kq > 0.003:
        f.circle(960, 560, 220, shader=f.rad(960, 560, 220, [("#F0D27A", 0.0, int(90 * kq)), ("#F0D27A", 1.0, 0)]))
        icons.draw_icon(f, "question", 960, 560, size=300 * (0.8 + 0.2 * sk.back_out(kq)), metal="gold", alpha=kq, rot=0.08 * math.sin(cx.t * 3.0), glow=0.0)
    cam.end(f)
    # ekran uzayı: levhalar (tek sayfa çekiminde ortada) + damga
    for (x, name, role, at, wa, lines, sd, key) in pages:
        if not plate or key not in ks_ or ks_[key] <= 0.003:
            continue
        xx = 960 if only else (560 if key == "a" else 1300)
        CM.name_plate(f, name, role, None, cx_=xx, y=158, t=ks_[key], w=600)
    ks = cx.amt(stamp_at, 0.3) if stamp_at is not None else 0.0
    if ks > 0.003:
        _paper_stamp(f, "ANEKDOT", 1560 if only else 960, 330 if only else 840, rot=-0.05, size=56, t=ks)    # tek sayfada sağ üstte: alttaki etiketlerle çakışmaz, altyazı bandının dışında
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# c2_sadaka — yoksulun ihtiyacını kimse istemeden gideren biri (Machiavelli'nin çizdiği)
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c2_sadaka")
def k_sadaka(cx, who_at=None, give_at=None, stamp_at=None, seed=4, **_):
    """Kurul tur 2 (SA1-Y5, KA2-D13): eşit aralıklı üç özdeş figür YOK — derinlik: biri ÖN PLANDA, büyük ve kare kenarıyla KESİK; ikisi arkada,
    küçük ve üst üste (biri ötekinin önünde, kısmen örter); aralıklar eşit değil; jestler farklı zamanda (figür çeşitlemesi ENG-C kitinde)."""
    f = cx.f
    c = f.c
    cam = _bg(f, cx, seed, dress="both")
    gy = 900
    f.rect(-100, gy, W + 200, 300, shader=f.lin(0, gy, 0, gy + 200, [("#8A6038", 0.0), ("#563820", 1.0)]))
    for i in range(-2, 16):
        c.drawLine(i * 140, gy, i * 140 - 70, gy + 200, f.paint("#3A2410", style="stroke", sw=2.5, alpha=0.5))
    t0 = cx.at(give_at) if give_at is not None else 0.0
    # arka plan ikilisi (küçük, üst üste): (x, ayak y, boy, tohum, eylem gecikmesi)
    back = ((1268, gy - 34, 372, 32, 1.35), (1392, gy - 22, 396, 33, 0.55))
    for (x, y, h, sd, dl) in back:
        FA.actor(f, "halk", x, y, h, cx.t, action="bow", dir=-1, seed=sd, phase=0.37 * sd, t0=t0 + dl + 0.5, dur=1.3, depth=14.0)
    # sol: verici (Giovanni; insan çapası kit seed 5)
    FA.actor(f, "banker", 520, gy + 20, 560, cx.t, action="idle", dir=1, seed=5, prop="sack")
    # florin yayları: verici → her yoksul, kimse istemeden (sıra: arka-sağ, ön, arka-sol)
    targets = ((1392, 470, 0.55), (1690, 560, 1.15), (1268, 480, 1.95))
    for i, (x, yt, dl) in enumerate(targets):
        for rep in range(2):
            u = (cx.t - (t0 + dl + rep * 2.6)) / 0.9
            if cx.t < t0 or not (0 < u < 1):
                continue
            e = ease_io(u, 1.5)
            px = lerp(700, x - 30, e)
            py = lerp(520, yt, e) - 150 * math.sin(math.pi * e)
            CP.draw_coin(f, px, py, 68, spin=cx.t * 12 + i, alpha=min(1, u * 6) * min(1, (1 - u) * 6 + 0.1), shadow=0.2)
            e2 = ease_io(min(1.0, u + 1.0 / 24.0 / 0.9), 1.5)
            _A.hint_speed(cx, _A.speed_of((px, py), (lerp(700, x - 30, e2), lerp(520, yt, e2) - 150 * math.sin(math.pi * e2)), 1.0 / 24.0))
    # ön plan: büyük, sağ kare kenarıyla kesik, hafif öne eğik (teşekkür) — ayak kadrajın altında
    FA.actor(f, "halk", 1790, gy + 210, 760, cx.t, action="bow", dir=-1, seed=34, phase=0.8, t0=t0 + 1.15 + 0.5, dur=1.5, depth=10.0)
    kw = cx.amt(who_at, 0.6) if who_at is not None else 0.0
    if kw > 0.003:
        CM.name_plate(f, "MACHİAVELLİ'NİN ÇİZDİĞİ", "KİMSE İSTEMEDEN DE", None, cx_=880, y=160, t=kw, w=920)
    ks = cx.amt(stamp_at, 0.3) if stamp_at is not None else 0.0
    if ks > 0.003:
        _paper_stamp(f, "ANEKDOT", 1520, 300, rot=-0.07, size=60, t=ks)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# kurul tur 1 — sahne bindirmeleri (ovl): çifte kayıt defteri, yıl rulosu, konuşma tomarı
# ─────────────────────────────────────────────────────────────────────────────
_ASEMIC = {}


def _asemic(c, x, y, w, k=1.0, seed=1, col="#2E1C0C", sw=3.0, a=1.0, xh=11.0):
    """Okunmaz el yazısı izi (bitişik halkalar, sözcük ARALARI, ara sıra üst uzantı, hafif sağa eğim; sözcük oluşturmaz — tutar/ad UYDURULMAZ).
    Dalgalı 'yer tutucu' çizginin yerine (kurul tur 3: defter içinde arayüz/yer tutucu dili yok). k: soldan yazılan pay. Dönüş: kalem ucu."""
    key = (seed, round(w), round(xh))
    pth = _ASEMIC.get(key)
    if pth is None:
        rs = _PN._RS(seed)
        pth = skia.Path()
        cx_ = 0.0
        while cx_ < w - 14:
            pth.moveTo(cx_, rs.uniform(-1.0, 1.0))
            for j in range(int(rs.uniform(3, 7))):
                h_ = xh * rs.uniform(0.65, 1.15) * (1.9 if rs.uniform(0, 1) < 0.16 else 1.0)
                lw = rs.uniform(7.0, 12.0)
                pth.cubicTo(cx_ + lw * 0.15 + 3.0, -h_, cx_ + lw * 0.85 + 3.0, -h_, cx_ + lw, rs.uniform(-0.8, 0.8))
                cx_ += lw
                if cx_ > w - 8:
                    break
            cx_ += rs.uniform(10.0, 17.0)
        _ASEMIC[key] = pth
    if k <= 0:
        return None
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(x - 4, y - 3 * xh, x + w * k, y + xh))
    c.translate(x, y)
    c.drawPath(pth, OD.STK(col, sw, int(255 * a)))
    c.restore()
    return (x + w * k, y) if k < 1 else None


def cifte_panel(a_at, b_at, bal_at, x0=1010, y0=236, w=800, h=560, out=None):
    """Çifte kayıt (partita doppia): aynı florin önce DEBITORI, sonra CREDITORI sayfasına yazılır; iki sütun eşitlenir (terazi dengelenir).
    Tutar/ad uydurulmaz: satırlar okunmaz el yazısı izi (iki sütunda AYNI iz: aynı kayıt) + florin simgesi.
    Kurul tur 3 (PK2-Y7): başlıkların altında küçük Türkçe karşılık BORÇLULAR / ALACAKLILAR; uçan florin deklanşör ipucu verir (AN1-Y7)."""
    def fn(cx):
        f = cx.f
        c = f.c
        kp = cx.amt(a_at, 0.45, off=-0.6)
        if out is not None:
            kp *= 1.0 - cx.amt(out, 0.4)
        if kp <= 0.003:
            return
        yy = y0 + (1 - kp) * 30
        f.rrect(x0 + 10, yy + 14, w, h, 12, color="#000000", alpha=0.30 * kp, blur=12)
        for i in range(2):
            px = x0 + i * w / 2
            f.rect(px, yy, w / 2, h, shader=f.lin(px, 0, px + w / 2, 0, [("#EFE3BF", 0.0), ("#F8EFD6", 0.5), ("#E2D3A8", 1.0)] if i == 0 else [("#E2D3A8", 0.0), ("#F8EFD6", 0.5), ("#EFE3BF", 1.0)]), alpha=kp)
        f.rect(x0, yy, w, h, style="stroke", sw=3, color="#4A3018", alpha=0.85 * kp)
        c.drawLine(x0 + w / 2, yy + 6, x0 + w / 2, yy + h - 6, f.paint("#7A5A32", style="stroke", sw=3, alpha=0.8 * kp))
        for i, (hd, tr_) in enumerate((("DEBITORI", "BORÇLULAR"), ("CREDITORI", "ALACAKLILAR"))):
            cxp = x0 + w / 4 + i * w / 2
            CM.ink(f, hd, cxp, yy + 62, face="title", size=40, color="#2A1608", align="c", track=6, alpha=kp, emboss=False)
            c.drawLine(cxp - 150, yy + 80, cxp + 150, yy + 80, f.paint("#8A2A1E", style="stroke", sw=2.4, alpha=0.8 * kp))
            CM.ink(f, tr_, cxp, yy + 114, face="title_m", size=32, color="#5A3A1E", align="c", track=4, alpha=kp, emboss=False)
            for r in range(6):
                ly = yy + 140 + r * 62
                c.drawLine(x0 + i * w / 2 + 40, ly + 14, x0 + i * w / 2 + w / 2 - 40, ly + 14, f.paint("#B8A27A", style="stroke", sw=1.2, alpha=0.6 * kp))
        # yazım: sol satır → sağ satır (aynı florin iki kez)
        for i, at in enumerate((a_at, b_at)):
            ta = cx.at(at)
            pr = clamp((cx.t - ta) / 0.8)
            if pr <= 0:
                continue
            lx = x0 + i * w / 2 + 50
            ly = yy + 140 + 62 * 1
            tp = _asemic(c, lx, ly + 8, w / 2 - 190, k=ease_io(pr, 1.4), seed=1402, sw=2.8, a=0.9 * kp)     # iki sütunda aynı iz: aynı kayıt
            if tp is not None:
                OD.quill(c, tp[0] + 6, tp[1] - 2, -58.0, 0.8)
            kc = clamp((cx.t - ta - 0.6) / 0.3)
            if kc > 0:
                CP.draw_coin(f, x0 + i * w / 2 + w / 2 - 80, ly - 2, 64, spin=0.0, alpha=kc * kp, shadow=0.2)
        # florin: önce sola iner, sonra yarısı sağa yansır (aynı tutar iki sütunda)
        t_a, t_b = cx.at(a_at), cx.at(b_at)
        for (ts, xa, xb) in ((t_a - 0.7, x0 + w / 2, x0 + w / 2 - 80), (t_b - 0.5, x0 + w / 2 - 80, x0 + w - 80)):
            u = (cx.t - ts) / 0.7
            if 0 < u < 1:
                e = ease_io(u, 1.6)
                p_ = (lerp(xa, xb, e), lerp(yy - 40, yy + 200, e) - 120 * math.sin(math.pi * e))
                CP.draw_coin(f, p_[0], p_[1], 70, spin=cx.t * 12, alpha=min(1, u * 5), shadow=0.25)
                e2 = ease_io(min(1.0, u + 1.0 / 24.0 / 0.7), 1.6)
                _A.hint_speed(cx, _A.speed_of(p_, (lerp(xa, xb, e2), lerp(yy - 40, yy + 200, e2) - 120 * math.sin(math.pi * e2)), 1.0 / 24.0))
        # denge: alt satır toplamları + terazi
        kb = cx.amt(bal_at, 0.5)
        if kb > 0.003:
            for i in range(2):
                cxp = x0 + w / 4 + i * w / 2
                c.drawLine(cxp - 130, yy + h - 92, cxp + 130, yy + h - 92, f.paint("#2E1C0C", style="stroke", sw=2.6, alpha=kp * kb))
                CP.draw_coin(f, cxp, yy + h - 50, 58, spin=0.0, alpha=kp * kb, shadow=0.2)
            CM.ink(f, "=", x0 + w / 2, yy + h - 34, face="title", size=64, color="#8A2A1E", align="c", alpha=kp * kb, emboss=False)
            tilt = 0.18 * (1.0 - ease_out(kb, 2)) * math.cos(cx.t * 5.0)
            icons.draw_icon(f, "scales", x0 + w / 2, yy - 70, size=140, metal="gold", alpha=kp * kb, rot=tilt, glow=0.0)
    return fn


def yil_panel(date_at, roll_at, cal_at, x=1420, y=300):
    """Koyu zemin üstünde: '20 ŞUBAT' · '1429' → '1428' rulo · 'FLORANSA TAKVİMİ · YILBAŞI 25 MART' (kontrast ≥7:1)."""
    def fn(cx):
        f = cx.f
        kd = cx.amt(date_at, 0.5)
        if kd <= 0.003:
            return
        w, h = 560, 330
        f.rrect(x - w / 2, y, w, h, 14, color="#0E0A08", alpha=0.72 * kd)
        f.rrect(x - w / 2, y, w, h, 14, style="stroke", sw=2.0, color="#C9A45A", alpha=0.8 * kd)
        CM.ink(f, "20 ŞUBAT", x, y + 70, face="title_m", size=50, color="#FFF4D6", align="c", track=14, alpha=kd, emboss=False)
        yr_old, yr_new = "1429", "1428"
        e = ease_io(clamp((cx.t - cx.at(roll_at)) / 0.9), 1.6) if roll_at is not None else 0.0
        size = 104
        wid = sk.text_width("1429", "title", size, 6)
        x0 = x - wid / 2
        f.c.save()
        f.c.clipRect(skia.Rect.MakeLTRB(x - w / 2 + 10, y + 96, x + w / 2 - 10, y + 230))
        for i in range(4):
            wch = sk.text_width(yr_old[i], "title", size, 6)
            xx = x0 + sum(sk.text_width(yr_old[j], "title", size, 6) for j in range(i)) + wch / 2
            if yr_old[i] != yr_new[i] and e > 0:
                CM.ink(f, yr_old[i], xx, y + 200 + 120 * e, face="title", size=size, color="#FFF4D6", align="c", alpha=kd * (1 - e), emboss=False)
                CM.ink(f, yr_new[i], xx, y + 200 - 120 * (1 - e), face="title", size=size, color="#F2C66A", align="c", alpha=kd * e, emboss=False)
            else:
                CM.ink(f, yr_old[i], xx, y + 200, face="title", size=size, color="#FFF4D6", align="c", alpha=kd, emboss=False)
        f.c.restore()
        kc = cx.amt(cal_at, 0.5) if cal_at is not None else 0.0
        if kc > 0.003:
            CM.ink(f, "FLORANSA TAKVİMİ", x, y + 268, face="title_m", size=36, color="#FFF4D6", align="c", track=8, alpha=kd * kc, emboss=False)
            CM.ink(f, "YILBAŞI 25 MART", x, y + 312, face="title_m", size=34, color="#F2C66A", align="c", track=8, alpha=kd * kc, emboss=False)
    return fn


def tomar(x, y, at, to, w=520, dirn=1, lines=5, out=None, words=None):
    """Konuşma tomarı: (x,y)'den yana açılan parşömen şerit. Kurul tur 2 (AN2-K2): words=[(metin, çapa)] verilirse dalgalı çizgi yerine GERÇEK harfler —
    anlatımdaki söz BİREBİR, satır satır kendi sözcüğünde yazılır (mürekkep el yazısı); verilmezse eski okunmaz satırlar."""
    def fn(cx):
        f = cx.f
        c = f.c
        k = cx.amt(at, 0.3)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k <= 0.003:
            return
        ta, tb = cx.at(at), cx.at(to)
        p = ease_io(clamp((cx.t - ta) / max(0.4, tb - ta)), 1.4)
        ww = 40 + (w - 40) * p
        nl = len(words) if words else lines
        lh = 52 if words else 34
        hh = 46 + lh * nl
        x0 = x if dirn > 0 else x - ww
        f.rrect(x0 + 6, y - hh / 2 + 10, ww, hh, 10, color="#000000", alpha=0.25 * k, blur=8)
        f.rrect(x0, y - hh / 2, ww, hh, 10, shader=f.lin(0, y - hh / 2, 0, y + hh / 2, [("#F4EAC8", 0.0), ("#DCCB98", 1.0)]), alpha=k)
        f.rrect(x0, y - hh / 2, ww, hh, 10, style="stroke", sw=2.5, color="#5A3E22", alpha=0.85 * k)
        if words:
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(x0 + 8, y - hh / 2, x0 + ww - 8, y + hh / 2))
            for i, (txt, la) in enumerate(words):
                ly = y - hh / 2 + 24 + lh * (i + 0.75)
                wl = sk.text_width(txt, "fell_i", 38)
                dur_ = max(0.45, min(1.0, 0.05 * len(txt)))
                pr = clamp((cx.t - cx.at(la)) / dur_)
                if pr <= 0:
                    continue
                c.save()
                c.clipRect(skia.Rect.MakeLTRB(x0 + 20, ly - 44, x0 + 30 + wl * pr, ly + 16))
                PP.hand(f, txt, x0 + 28, ly, face="fell_i", size=38, color="#24160A", alpha=k, jitter=0.9, seed=7 + i)
                c.restore()
            c.restore()
        else:
            for i in range(lines):
                ly = y - hh / 2 + 34 + i * 34
                wl = max(0.0, ww - 60) * (0.95 if i % 2 == 0 else 0.75)
                pth = skia.Path(); pth.moveTo(x0 + 30, ly)
                nn = max(2, int(wl / 12))
                for q in range(1, nn + 1):
                    pth.lineTo(x0 + 30 + q * wl / nn, ly + 4 * math.sin(q * 1.8 + i))
                c.drawPath(pth, f.paint("#3A2410", style="stroke", sw=2.6, alpha=0.8 * k))
        for xe in (x0, x0 + ww):
            f.rrect(xe - 10, y - hh / 2 - 8, 20, hh + 16, 8, shader=f.lin(xe - 10, 0, xe + 10, 0, [("#B89A62", 0.0), ("#E8D4A0", 0.5), ("#9A7A44", 1.0)]), alpha=k)
    return fn


# ═════════════════════════════════════════════════════════════════════════════
# KURUL TUR 2 (SCN-2) — "DEFTER DÜNYADIR": masa üstü defter çekimi (c2_masa) ve nesne/el yakın planı (c2_yakin)
# AN1-Y3/Y4/Y6, AN2-Ö1/Ö3/K2, SA1-Y6: aynı karta sıçrayan kesme, sessiz cep, boş açılış ve "infografik slayt" yerine grafik DÜNYAYA yerleşir:
# masadaki açık defterde mürekkeple yazılır/dolar, anahtarları bir el bırakır, tüy kalem satırı izler; ön planda nesne katmanı (bulanık şamdan).
# Kamera kendi yolunda (cams=[(çapa, (x, y, zum))], dünya koordinatı; cilt_cam.OWN_CAMERA). Dünya 2600×1700, defter ortası (1300, 860).
# ═════════════════════════════════════════════════════════════════════════════
import cilt_pano as _PN  # noqa: E402

MW, MH = 2600, 1700
BOOK_C = (1300.0, 860.0)
PG_W, PG_H = 790.0, 1000.0
_MASA_IMG = {}
_MS = 1.25                                   # taban görüntüsü ölçeği (yakınlaşmada keskin kalsın)
INK_C = "#24160A"
INK_R = "#8E2A1E"

MASA_V = {
    "iz": dict(surface="walnut", cover="#5A2A1E", props=("books", "inkwell"), candle=(330, 420), fg=("candle", "l")),
    "catasto": dict(surface="pine", cover="#6A4A2A", props=("bundles", "inkwell"), candle=None, fg=("roll", "l")),
}


def _page_origin(side):
    return (BOOK_C[0] - PG_W if side == "l" else BOOK_C[0], BOOK_C[1] - PG_H / 2)


def _masa_base(v):
    """Masa + açık defter + durağan nesneler (bir kez pişirilir)."""
    img = _MASA_IMG.get(v)
    if img is not None:
        return img
    V = MASA_V[v]
    fr = sk.Frame(int(MW * _MS), int(MH * _MS))
    c = fr.c
    c.scale(_MS, _MS)
    T = OD.OTint("day")
    if V["surface"] == "velvet":
        c0, c1 = V["cloth"]
        OD.GRAD_V(c, 0, 0, MW, MH, [(c0, 0.0), (c1, 1.0)])
        rs = OD._RS(7)
        for k in range(26):                                   # kadife kıvrım gölgeleri
            x = rs.uniform(0, MW)
            c.drawLine(x, 0, x + rs.uniform(-120, 120), MH, OD.STK("#000000", rs.uniform(18, 46), int(rs.uniform(10, 26))))
        for yy in range(60, MH, 120):                          # soluk damasko
            for xx in range(60 + (yy // 120 % 2) * 60, MW, 120):
                c.drawPath(sk.poly_path([(xx, yy - 16), (xx + 10, yy), (xx, yy + 16), (xx - 10, yy)]), OD.PT("#D2A33E", 28))
    else:
        col = "#6A4228" if V["surface"] == "walnut" else "#B48C5C"
        y = 0
        k = 0
        while y < MH:
            hh = 190
            OD.WOOD(c, -10, y, MW + 10, y + hh, T, mix(col, "#000000" if k % 2 else "#FFFFFF", 0.06), seed=k + 3, ink=1.1, grain=9)
            y += hh
            k += 1
    # defter: kapak, sayfa kalınlığı, sayfalar (cilde doğru gölge), çizgiler
    bx, by = BOOK_C
    cv = skia.Path(); cv.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(bx - PG_W - 34, by - PG_H / 2 - 30, bx + PG_W + 34, by + PG_H / 2 + 34), 18, 18))
    fr.path(cv, color="#000000", alpha=0.45, blur=18)
    c.drawPath(cv, OD.PT(V["cover"]))
    c.drawPath(cv, OD.STK(OD.INK, 2.0, 210))
    for i in range(7):                                         # sayfa kenarları (kalınlık)
        for side in (-1, 1):
            xo = bx + side * (PG_W + 6 + i * 3.2)
            c.drawLine(xo, by - PG_H / 2 + 8 + i, xo, by + PG_H / 2 - 8 + i * 1.5, OD.STK("#D8C9A2" if i % 2 else "#B8A47A", 2.0, 230))
    for side in ("l", "r"):
        x0, y0 = _page_origin(side)
        pg = skia.Path()
        if side == "l":
            pg.moveTo(x0, y0 + 6); pg.quadTo(x0 + PG_W * 0.6, y0 - 4, x0 + PG_W, y0 + 10); pg.lineTo(x0 + PG_W, y0 + PG_H - 4)
            pg.quadTo(x0 + PG_W * 0.6, y0 + PG_H + 8, x0, y0 + PG_H); pg.close()
            sh = OD.LGP((x0, 0), (x0 + PG_W, 0), [("#F4EBCF", 0.0), ("#EFE3C2", 0.78), ("#C9B68A", 1.0)])
        else:
            pg.moveTo(x0, y0 + 10); pg.quadTo(x0 + PG_W * 0.4, y0 - 4, x0 + PG_W, y0 + 6); pg.lineTo(x0 + PG_W, y0 + PG_H)
            pg.quadTo(x0 + PG_W * 0.4, y0 + PG_H + 8, x0, y0 + PG_H - 4); pg.close()
            sh = OD.LGP((x0, 0), (x0 + PG_W, 0), [("#C9B68A", 0.0), ("#EFE3C2", 0.22), ("#F4EBCF", 1.0)])
        c.drawPath(pg, sh)
        c.drawPath(pg, OD.STK(OD.INK, 1.4, 190))
        for yy in range(int(y0 + 210), int(y0 + PG_H - 50), 48):
            c.drawLine(x0 + 36, yy, x0 + PG_W - 36, yy, OD.STK("#B8A47A", 1.1, 120, False))
        xm = x0 + (PG_W - 150 if side == "l" else 150)
        c.drawLine(xm, y0 + 190, xm, y0 + PG_H - 40, OD.STK("#C48A7A", 1.3, 130, False))
    c.drawLine(bx, by - PG_H / 2 + 8, bx, by + PG_H / 2 - 4, OD.STK("#5A4630", 2.0, 170))
    # durağan nesneler
    props = V["props"]
    if "books" in props:
        for k, (xx, yy, w_, col) in enumerate(((2310, 1240, 300, "#6A2E24"), (2300, 1200, 280, "#2E4A3A"), (2316, 1162, 290, "#5A3A24"))):
            OD.BOX(c, xx - w_ / 2, yy - 30, xx + w_ / 2, yy + 30, col, T, hl=0.18, sh=0.26, ink=1.4)
    if "chest" in props:
        _icons_draw(fr, "chest", 300, 520, 330, "bronze")
    if "coins" in props:
        OD.draw_coins(c, 2260, 1240, 18, 3.2, 0.0, seed=4, glint=False)
        OD.draw_coins(c, 2420, 1300, 10, 3.2, 0.0, seed=9, glint=False)
    if "bundles" in props:
        rs = OD._RS(21)
        for k in range(9):
            xx, yy = 250 + (k % 3) * 70 + rs.uniform(-10, 10), 330 + (k // 3) * 46
            c.drawOval(skia.Rect.MakeLTRB(xx - 110, yy - 22, xx + 110, yy + 22), OD.PT(["#E8DCB8", "#DCCB98", "#EFE4C4"][k % 3]))
            c.drawOval(skia.Rect.MakeLTRB(xx - 110, yy - 22, xx + 110, yy + 22), OD.STK(OD.INK, 1.2, 170))
            c.drawLine(xx, yy - 22, xx, yy + 22, OD.STK("#8E2A1E", 4.0, 230))
        for k in range(6):
            xx, yy = 2240 + (k % 2) * 160, 1180 + (k // 2) * 52
            c.drawOval(skia.Rect.MakeLTRB(xx - 100, yy - 22, xx + 100, yy + 22), OD.PT(["#E8DCB8", "#EFE4C4"][k % 2]))
            c.drawOval(skia.Rect.MakeLTRB(xx - 100, yy - 22, xx + 100, yy + 22), OD.STK(OD.INK, 1.2, 170))
            c.drawLine(xx, yy - 22, xx, yy + 22, OD.STK("#8E2A1E", 4.0, 230))
    if "inkwell" in props:
        ix = 2280 if v != "catasto" else 2300
        OD.inkwell(c, ix, 520, 3.4, 0.0)
    img = fr.surf.makeImageSnapshot()
    _MASA_IMG[v] = img
    return img


def _icons_draw(f, name, x, y, size, metal="gold", alpha=1.0, rot=0.0, shadow=True):
    icons.draw_icon(f, name, x, y, size=size, metal=metal, alpha=alpha, rot=rot, glow=0.0, shadow=shadow)


HAND_K = {"open": 0.0885, "fist": 0.064, "point": 0.1115}     # kit el sprite'ı: bilekten parmak ucuna uzunluk / h


def arm_hand(f, x, y, ang, size, sleeve="#6E1C1E", cuff="#C9A23A", kind="open", skin="#E2BD97", alpha=1.0, flip=False, fur=False, reach=4.0):
    """Büyük el + yen (yakın plan): (x,y) = bilek; ang = parmak yönü (derece); yen bilekten geriye `reach`×size uzanır (kadraj dışına).
    size = el boyu (bilek→parmak ucu, px). Yen eli sarmalayacak kadar geniş, bileğe doğru daralır; kol ağzı kürk ya da sırma."""
    if alpha <= 0.003:
        return
    c = f.c
    a = math.radians(ang)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    L = size * reach
    thick = size * 0.62                                        # elin kalınlığı ≈ 0,6 × boy
    w0, w1 = thick * 0.62, thick * 0.95                        # yen yarı genişliği: bilekte → omuza doğru
    ex, ey = x - dx * size * 0.10, y - dy * size * 0.10
    bx, by = x - dx * L, y - dy * L
    sl = sk.poly_path([(ex + nx * w0, ey + ny * w0), (bx + nx * w1, by + ny * w1), (bx - nx * w1, by - ny * w1), (ex - nx * w0, ey - ny * w0)])
    f.path(sl, color="#000000", alpha=0.26 * alpha, blur=12)
    c.drawPath(sl, f.paint(sleeve, alpha=alpha, shader=f.lin(ex + nx * w0, ey + ny * w0, ex - nx * w0, ey - ny * w0,
                                                             [(mix(sleeve, "#FFFFFF", 0.14), 0.0), (sleeve, 0.45), (mix(sleeve, "#000000", 0.30), 1.0)])))
    c.drawPath(sl, f.paint(mix(sleeve, "#000000", 0.55), style="stroke", sw=max(1.5, size / 100), alpha=0.9 * alpha))
    for k in range(3):                                         # kumaş kıvrımları (yen boyunca)
        u = 0.30 + 0.20 * k
        px_, py_ = ex - dx * L * u, ey - dy * L * u
        ww = w0 + (w1 - w0) * u
        c.drawLine(px_ + nx * ww * 0.7, py_ + ny * ww * 0.7, px_ - nx * ww * 0.1 + dx * size * 0.35, py_ - ny * ww * 0.1 + dy * size * 0.35,
                   f.paint(mix(sleeve, "#000000", 0.38), style="stroke", sw=max(1.2, size / 110), alpha=0.65 * alpha))
    cw = size * 0.16                                           # kol ağzı
    cf = sk.poly_path([(ex + dx * cw * 0.2 + nx * w0 * 1.05, ey + dy * cw * 0.2 + ny * w0 * 1.05), (ex - dx * cw + nx * w0 * 1.12, ey - dy * cw + ny * w0 * 1.12),
                       (ex - dx * cw - nx * w0 * 1.12, ey - dy * cw - ny * w0 * 1.12), (ex + dx * cw * 0.2 - nx * w0 * 1.05, ey + dy * cw * 0.2 - ny * w0 * 1.05)])
    c.drawPath(cf, f.paint(cuff, alpha=alpha))
    if fur:
        # kürk tutamları kol ağzının İÇİNE kırpılır (kurul tur 3 SA1-N2: daireler kol ağzının dışına taşıyordu)
        c.save()
        c.clipPath(cf, skia.ClipOp.kIntersect, True)
        for k in range(11):
            u = k / 10.0
            for side, sh_ in ((0.0, 0.0), (0.55, 0.18)):
                qx = ex - dx * cw * (0.15 + side) + nx * w0 * (1.15 - 2.3 * u)
                qy = ey - dy * cw * (0.15 + side) + ny * w0 * (1.15 - 2.3 * u)
                f.circle(qx, qy, cw * (0.55 - 0.1 * side), color=mix(cuff, "#FFFFFF" if k % 2 else "#000000", 0.12 + sh_), alpha=alpha)
        c.restore()
    c.drawPath(cf, f.paint(mix(cuff, "#000000", 0.5), style="stroke", sw=max(1.2, size / 120), alpha=0.85 * alpha))
    hb = size / HAND_K.get(kind, 0.0885)
    spr = FA.hand_sprite(skin, int(round(hb)), kind)
    if alpha < 0.999:
        c.saveLayerAlpha(None, int(255 * alpha))
    FA.blit(c, spr, 0, 0, x, y, ang + (180.0 if flip else 0.0), -1.0 if flip else 1.0)     # flip: ayna el, parmaklar yine `ang` yönünde
    if alpha < 0.999:
        c.restore()


def _ends(cx, cut_only=False):
    """Kendi kameralı c2 türlerinde uç eğimleri — motordaki cilt_cam mantığı (motor DEĞİŞMEZ; SCN-3, kurul tur 3 AN1-Y-N3):
    SERT KESMEYLE birleşen uçta en az cilt_cam.CUT_SLOPE (kamera kesmede durmaz: 'hareket üstünde kesme'), geçişle birleşen uçta cilt_cam.CARRY
    (cut_only=True ise 0: geçiş uçları eskisi gibi yumuşak durur), serbest uçta 0. Dönüş: (e0, e1) = ortalama hıza göre uç eğimleri."""
    cut = float(getattr(cilt_cam, "CUT_SLOPE", 1.0))
    car = 0.0 if cut_only else float(getattr(cilt_cam, "CARRY", 0.65))
    kin, kout = bool(getattr(cx, "cut_in", False)), bool(getattr(cx, "cut_out", False))
    cin, cout = bool(getattr(cx, "cam_in", False)), bool(getattr(cx, "cam_out", False))
    return (cut if kin else (car if cin else 0.0)), (cut if kout else (car if cout else 0.0))


def _herm(u, s0, s1):
    """g(0)=0, g(1)=1, g'(0)=s0, g'(1)=s1 (cilt_cam.hermite ile aynı); u<0 ve u>1'de doğrusal uzatma (eğim sürekli)."""
    if u <= 0.0:
        return s0 * u
    if u >= 1.0:
        return 1.0 + s1 * (u - 1.0)
    u2 = u * u
    u3 = u2 * u
    return (u3 - 2 * u2 + u) * s0 + (-2 * u3 + 3 * u2) + (u3 - u2) * s1


def _wcam(cx, cams, dur, ends=(0.0, 0.0)):
    """Dünya kamerası (x, y, zum): anahtar kareler çapalı, tekdüze kübik Hermite. ends=(e0, e1): uç eğimi (0 → uçta yumuşak duruş;
    _ends(cx) → sert kesmede CUT_SLOPE: kamera anahtar karenin ötesinde de o eğimle sürer, cilt_pano.pchip)."""
    ks = sorted(((cx.at(a) if not isinstance(a, (int, float)) else float(a)), v) for a, v in cams)
    ts = [k[0] for k in ks]
    e0, e1 = ends
    fx = _PN.pchip(ts, [k[1][0] for k in ks], e0=e0, e1=e1)
    fy = _PN.pchip(ts, [k[1][1] for k in ks], e0=e0, e1=e1)
    fz = _PN.pchip(ts, [k[1][2] for k in ks], e0=e0, e1=e1)
    t = clamp(cx.t, -1.0, dur + 1.0)
    return fx(t), fy(t), fz(t)


EDGE_PAD = 90.0           # kurul tur 3 TE2-G1: kadraj kenarında yarım sözcük/sayı yok — yazı ya ≥90 px payla içeride ya da söner


def _edge_k(c, x0, y0, x1, y1, pad=EDGE_PAD):
    """Dünya kutusunun (x0,y0,x1,y1) EKRAN kutusu kadraj kenarına `pad` px'ten yakınsa söndürme çarpanı (1 → tam içeride; 0 → kenarda kesik).
    Kamera bir sayfadan ayrılırken o sayfanın yazıları kenarda yarım kalmaz, yumuşakça söner (TE2-G1)."""
    r = c.getTotalMatrix().mapRect(skia.Rect.MakeLTRB(x0, y0, x1, y1))
    kx = smooth(clamp(min(r.left(), W - r.right()) / pad))                # yatay: ≥pad içeride tam, kenarda 0
    ky = smooth(clamp(min(r.top() / 30.0, (H - r.bottom()) / 30.0)))       # dikey: üst/alt kenardan taşan yazı da söner (30 px pay)
    return kx * ky


def _write(f, text, x, y, size, pr, face="title_m", color=INK_C, track=4.0, align="c", alpha=1.0, edge=True):
    """Mürekkep yazımı: metin soldan sağa açılır (pr 0..1). Dönüş: kalem ucu (x, y) ya da None.
    edge=True: kadraj kenarında yarım kalan yazı söner (_edge_k; TE2-G1) — kalem ucu yine döner."""
    if pr <= 0:
        return None
    wid = sk.text_width(text, face, size, track)
    x0 = x - (wid / 2 if align == "c" else 0)
    c = f.c
    a = alpha * (_edge_k(c, x0, y - size * 0.8, x0 + wid * min(1.0, pr), y + size * 0.25) if edge else 1.0)     # yalnız görünen (yazılmış) kısım
    if a > 0.003:
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(x0 - 8, y - size * 1.1, x0 + wid * pr + 2, y + size * 0.45))
        CM.ink(f, text, x0, y, face=face, size=size, color=color, align="l", track=track, alpha=a, emboss=False, scrim=False)
        c.restore()
    return (x0 + wid * pr, y) if pr < 1 else None


def _ink_e(f, text, x, y, face="title_m", size=40, color=INK_C, align="c", track=4.0, alpha=1.0):
    """CM.ink (mürekkep, kabartmasız) + kadraj kenarı söndürmesi (_edge_k)."""
    wid = sk.text_width(text, face, size, track)
    x0 = x - (wid / 2 if align == "c" else (wid if align == "r" else 0))
    a = alpha * _edge_k(f.c, x0, y - size * 0.8, x0 + wid, y + size * 0.25)
    if a > 0.003:
        CM.ink(f, text, x, y, face=face, size=size, color=color, align=align, track=track, alpha=a, emboss=False, scrim=False)


def _hand_line(c, pts, col=INK_C, w=3.0, a=1.0, seed=1, wob=1.6, k=1.0):
    """Tüy kalemle çekilmiş çizgi: noktalar arası hafif titrek (tohumlu), basınca göre değişen kalınlık ve mürekkep yoğunluğu. k: çizilen pay (0..1)."""
    if k <= 0 or len(pts) < 2:
        return
    rs = _PN._RS(seed)
    segs = []
    for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
        L = math.hypot(xb - xa, yb - ya)
        n = max(2, int(L / 18))
        for i in range(n):
            u0, u1 = i / n, (i + 1) / n
            segs.append(((lerp(xa, xb, u0), lerp(ya, yb, u0)), (lerp(xa, xb, u1), lerp(ya, yb, u1))))
    nseg = len(segs)
    lim = k * nseg
    off = [rs.uniform(-wob, wob) for _ in range(nseg + 1)]
    for i, ((xa, ya), (xb, yb)) in enumerate(segs):
        if i >= lim:
            break
        uu = min(1.0, lim - i)
        dx, dy = xb - xa, yb - ya
        L = max(1e-6, math.hypot(dx, dy))
        nx, ny = -dy / L, dx / L
        xe, ye = xa + dx * uu, ya + dy * uu
        pr = 0.75 + 0.5 * abs(math.sin(i * 0.37 + seed))                  # basınç: kalınlık + yoğunluk birlikte değişir
        c.drawLine(xa + nx * off[i], ya + ny * off[i], xe + nx * off[i + 1] * uu, ye + ny * off[i + 1] * uu,
                   OD.STK(col, w * pr, int(255 * a * min(1.0, 0.70 + 0.35 * pr))))


def _wp(cx, a, dur=0.8):
    return clamp((cx.t - cx.at(a)) / dur) if a is not None else 0.0


def _stamp_e(f, text, x, y, rot, size, t):
    """Kâğıt fişli damga (_paper_stamp) + kadraj kenarı söndürmesi: fiş kutusu kenarda yarım kalırsa söner (TE2-G1)."""
    if t <= 0:
        return
    wd = sk.text_width(text, "title", size, 6.0) * 1.08 + 70
    a = _edge_k(f.c, x - wd / 2, y - size * 0.95, x + wd / 2, y + size * 0.75)
    if a > 0.003:
        _paper_stamp(f, text, x, y, rot=rot, size=size, t=t, alpha=a)


def _masa_iz(cx, f, P):
    """İZ (c2s13–c2s14): sol sayfa çifte kaydın izi (zaman çizgisi), sağ sayfa Medici'nin farkı: yapı.
    Kurul tur 3: sayfalar BAŞLIĞI YAZILI açılır, kalem yalnız yeni veriyi yazar (PK2-N1.4, AN2-Ö1); eksen tüy kalemle elle çekilmiş, yıllar el yazısıyla
    (SA1-Y6-k: tik etiketli arayüz ekseni yok); ETMEDİLER ve sağ sayfanın alt etiketleri altyazı bandının üstünde (TE2-G2, G7); kenarda yarım kalan yazı söner (G1)."""
    tip = None
    c = f.c
    # ── sol sayfa ── başlık ve eksen ilk karede hazır
    x0, y0 = _page_origin("l")
    _ink_e(f, "ÇİFTE KAYDIN İZİ", x0 + 395, y0 + 110, face="title_m", size=42)
    ly = y0 + 500
    lx0, lx1 = x0 + 70, x0 + 720
    _hand_line(c, [(lx0 - 6, ly + 3), (lx0 + 210, ly - 2), (lx0 + 430, ly + 2), (lx1 + 8, ly - 3)], w=3.6, seed=13, wob=1.4)
    for k in range(6):                                          # elle atılmış çentikler + el yazısıyla yıllar (her 40 yıl)
        yr = 1320 + 40 * k
        xx = lx0 + (yr - 1320) / 200.0 * (lx1 - lx0) + (2.5 if k % 2 else -2.0)
        _hand_line(c, [(xx - 1.5, ly - 14 - (k % 3) * 2), (xx + 1.5, ly + 13)], w=2.4, seed=40 + k, wob=0.8)
        wy = sk.text_width(str(yr), "fell_i", 36)
        ke = _edge_k(c, xx - wy / 2, ly + 22, xx + wy / 2, ly + 58)
        if ke > 0.003:
            PP.hand(f, str(yr), xx, ly + 50 + (k % 2) * 3, face="fell_i", size=36, color="#4A3420", alpha=0.92 * ke, jitter=0.9, seed=60 + k, align="c")
    for (yr, lab, a, up) in P.get("events", ()):
        k = _wp(cx, a, 0.7)
        if k <= 0:
            continue
        xx = lx0 + (yr - 1320) / 200.0 * (lx1 - lx0)
        f.circle(xx, ly, 13 * min(1.0, k * 2), color=INK_R)
        r = _write(f, str(yr), xx, ly - 64, 42, k, face="title", color=INK_R, track=2)
        tip = r or tip
        r = _write(f, lab, xx, ly - 114, 36, _wp(cx, a, 0.9), face="title_m", color=INK_C, track=3)
        tip = r or tip
    if P.get("myth_at") is not None:
        k = _wp(cx, P["myth_at"], 0.8)
        my = y0 + 290
        r = _write(f, "MEDİCİ İCADI", x0 + 395, my, 38, k)
        tip = r or tip
        ks = _wp(cx, P.get("myth_x"), 0.35)
        if ks > 0:
            wd = sk.text_width("MEDİCİ İCADI", "title_m", 38, 4.0)
            ke = _edge_k(c, x0 + 395 - wd / 2 - 12, my - 30, x0 + 395 + wd / 2 + 12, my + 10)
            _hand_line(c, [(x0 + 395 - wd / 2 - 12, my - 8), (x0 + 395 + wd / 2 + 12, my - 16)], col="#A8201A", w=6.5, a=0.9 * ke, seed=7, wob=1.0, k=ks)
    if P.get("stamp_at") is not None:                           # TE2-G2: harflerin altı ekranda ≤870 (eskisi sayfa dibinde, altyazı bandındaydı)
        _stamp_e(f, "ETMEDİLER", x0 + 395, y0 + 650, -0.05, 68, _wp(cx, P["stamp_at"], 0.3))
    # ── sağ sayfa ── başlık ilk karede "MEDİCİ'NİN FARKI"; kalem ": YAPI"yı 'yapıdaydı'da ekler (metin aynı: MEDİCİ'NİN FARKI: YAPI)
    x0, y0 = _page_origin("r")
    full_h, pre_h = "MEDİCİ'NİN FARKI: YAPI", "MEDİCİ'NİN FARKI"
    p0 = sk.text_width(pre_h, "title_m", 40, 4.0) / sk.text_width(full_h, "title_m", 40, 4.0)
    ky = _wp(cx, P.get("yapi_at"), 0.6) if P.get("yapi_at") is not None else 1.0
    r = _write(f, full_h, x0 + 395, y0 + 110, 40, p0 + (1.0 - p0) * ky)
    tip = (r if 0 < ky < 1 else None) or tip
    kd = _wp(cx, P.get("book_at"), 0.5)
    if kd > 0:
        bx_, by_ = x0 + 170, y0 + 270
        _icons_draw(f, "book", bx_, by_, 130, "bronze", alpha=kd * _edge_k(c, bx_ - 70, by_ - 60, bx_ + 70, by_ + 60), shadow=False)
        r = _write(f, "DEFTER DEĞİL", bx_, by_ + 110, 30, _wp(cx, P.get("book_at"), 0.8), face="title_m")
        tip = r or tip
        kx = _wp(cx, P.get("book_x"), 0.32)
        if kx > 0:
            for sg in (1, -1):
                _hand_line(c, [(bx_ - 66, by_ - 56 * sg), (bx_ + 66, by_ + 56 * sg)], col="#A8201A", w=8.0, a=0.9, seed=21 + sg, wob=1.2, k=kx)
    nodes = {"f": (x0 + 480, y0 + 300, "FLORANSA", "coinbag"), "r": (x0 + 230, y0 + 560, "ROMA", "book"), "v": (x0 + 640, y0 + 560, "VENEDİK", "book")}
    for (a_, b_, ea) in P.get("edges", ()):
        k = _wp(cx, ea, 0.9)
        if k <= 0:
            continue
        (xa, ya, _, _), (xb, yb, _, _) = nodes[a_], nodes[b_]
        _hand_line(c, [(xa, ya), (xb, yb)], w=4.2, a=0.95, seed=31 + ord(b_), wob=1.3, k=ease_io(k, 1.5))
        if k < 1:
            tip = (xa + (xb - xa) * ease_io(k, 1.5), ya + (yb - ya) * ease_io(k, 1.5))
    for nid, na in P.get("nodes", ()):
        k = _wp(cx, na, 0.5)
        if k <= 0:
            continue
        x, y, name, ic = nodes[nid]
        R_ = 74 if nid == "f" else 62
        f.circle(x, y, R_ * (0.85 + 0.15 * ease_out(k)), color="#F4EBCF", alpha=k)
        f.circle(x, y, R_ * (0.85 + 0.15 * ease_out(k)), style="stroke", sw=4, color=INK_C, alpha=k)
        _icons_draw(f, ic, x, y, R_ * 1.25, "gold" if nid == "f" else "bronze", alpha=k, shadow=False)
        r = _write(f, name, x, y + R_ + 46, 34, _wp(cx, na, 0.7), face="title_m")
        tip = r or tip
    for (txt, la, yy) in P.get("labels", ()):
        r = _write(f, txt, x0 + 395, y0 + yy, 34, _wp(cx, la, 0.9), face="title_m", color=INK_R)
        tip = r or tip
    return tip


TALLY_N, TALLY_GOLD = 9780, 137
_TALLY = {}


def _tally_img(gw=600.0, gh=380.0, sc=2.0):
    """9.780 hane: elle çekilmiş BEŞLİ ÇETELE (dört dik çentik + bir çapraz), satır satır (kurul tur 3 SA1-Y6-k, AN2: 'düz kahverengi blok / barkod' yerine).
    Satır sonları düzensiz, mürekkep yoğunluğu satıra ve gruba göre değişir; ilk 137 çentik ayrı yaldız katmanında. Bir kez pişirilir (sc× çözünürlük).
    Dönüş: (mürekkep görüntüsü, yaldız görüntüsü, satırlar=[(y_üst, y_alt, [çentik x'leri])], ölçek)."""
    v = _TALLY.get((gw, gh, sc))
    if v is not None:
        return v
    rs = _PN._RS(1427)
    pitch, row_h = 12.6, 9.0
    rows, n_left = [], TALLY_N
    y = 2.0
    while n_left > 0:
        ind = rs.uniform(0.0, 7.0)                                  # satır başı girintisi ve satır sonu düzensiz
        ng = int((gw - ind - rs.uniform(0.0, 38.0)) // pitch)
        cnt = min(n_left, ng * 5)
        rows.append((y, ind, cnt, rs.uniform(-0.6, 0.6), rs.uniform(0.62, 0.98)))    # (y, girinti, çentik sayısı, eğim, mürekkep yoğunluğu)
        n_left -= cnt
        y += row_h + rs.uniform(-0.5, 0.7)
    fi = sk.Frame(int((gw + 4) * sc), int((gh + 4) * sc))
    fg = sk.Frame(int((gw + 4) * sc), int((gh + 4) * sc))
    for fr_ in (fi, fg):
        fr_.c.scale(sc, sc)
        fr_.c.translate(2.0, 2.0)                                   # yerel (x, y) → görüntüde (x+2, y+2): kenar çentikleri kırpılmasın
    out_rows = []
    idx = 0
    for (yy, ind, cnt, sl, dens) in rows:
        xs = []
        x = ind
        for m in range(cnt):
            gi, mi = divmod(m, 5)
            if mi == 0:
                x = ind + gi * pitch + rs.uniform(-0.6, 0.6)
                gdy = rs.uniform(-0.7, 0.7)
                gd = dens * rs.uniform(0.80, 1.08)
            a = int(255 * min(1.0, gd))
            top, bot = yy + gdy + rs.uniform(-0.6, 0.5), yy + row_h - 2.0 + gdy + rs.uniform(-0.5, 0.6)
            w_ = rs.uniform(0.85, 1.25)
            tg = [(fi.c, INK_C, a)] + ([(fg.c, "#B07A1C", 255)] if idx < TALLY_GOLD else [])      # ilk 137: mürekkep + üstte yaldız katmanı
            if mi < 4:
                xm = x + mi * 2.1
                for (cc_, col, aa) in tg:
                    cc_.drawLine(xm + sl, top, xm - sl * 0.3, bot, OD.STK(col, w_ * (1.25 if cc_ is fg.c else 1.0), aa))
                xs.append(xm)
            else:                                                   # beşinci: dört çentiği çapraz keser
                for (cc_, col, aa) in tg:
                    cc_.drawLine(x - 1.4, bot - 1.0, x + 7.6, top + 1.2, OD.STK(col, w_ * (1.25 if cc_ is fg.c else 1.0), aa))
                xs.append(x + 7.6)
            idx += 1
        out_rows.append((yy - 1.0, yy + row_h, xs))
    v = (fi.surf.makeImageSnapshot(), fg.surf.makeImageSnapshot(), out_rows, sc)
    _TALLY[(gw, gh, sc)] = v
    return v


def _hatch_band(f, bx0, by0, bw, bh, frac, uf, seed=29):
    """Elle cetvellenmiş bant (titrek kenarlı kalem çizgisi) + payın (frac) mürekkep çapraz taraması; tarama soldan uf ile ilerler, sağ kenarı titrek."""
    c = f.c
    rs = _PN._RS(seed)
    xr = bx0 + bw * frac * uf
    if uf > 0:
        c.save()
        clip = skia.Path()
        clip.moveTo(bx0 + 2, by0 + 2)
        nn = 9
        for i in range(nn + 1):                                     # titrek sağ kenar
            clip.lineTo(xr + rs.uniform(-3.0, 3.0), by0 + 2 + (bh - 4) * i / nn)
        clip.lineTo(bx0 + 2, by0 + bh - 2)
        clip.close()
        c.clipPath(clip, skia.ClipOp.kIntersect, True)
        x = bx0 - bh
        k = 0
        while x < xr + 6:
            c.drawLine(x, by0 + bh + 2, x + bh + 4, by0 - 2, OD.STK("#3A2412", rs.uniform(1.3, 2.0), int(rs.uniform(170, 235))))
            if k % 2 == 0:                                          # çapraz tarama (seyrek)
                c.drawLine(x + 2, by0 - 2, x + bh + 6, by0 + bh + 2, OD.STK("#5A3A1E", rs.uniform(0.9, 1.3), int(rs.uniform(110, 170))))
            x += 7.5 + rs.uniform(-1.0, 1.0)
            k += 1
        c.restore()
    return (xr, by0 + bh / 2)


def _masa_catasto(cx, f, P):
    """CATASTO (c2s23): sol sayfa 9.780 hane (beşli çetele) + ilk 137'si yaldızlı + elle cetvellenmiş KAYITLI SERVET bandında %29,8 mürekkep taraması;
    sağ sayfa en zengin: Palla Strozzi. Kurul tur 3: başlık İLK KAREDE yazılı (PK2-N1.4); arayüz grafiği yok (SA1-Y6-k); bant ve %29,8 altyazı bandının
    üstünde (TE2-G7); kamera sağ sayfaya geçince sol sayfanın kenarda kalan yazıları söner (TE2-G1)."""
    tip = None
    c = f.c
    x0, y0 = _page_origin("l")
    _ink_e(f, "CATASTO · 1427", x0 + 395, y0 + 100, face="title", size=42)
    gx0, gy0 = x0 + 95, y0 + 175
    img_i, img_g, rows, sc = _tally_img()
    p = ease_io(clamp((cx.t - cx.at(P["fill_at"])) / max(0.4, cx.at(P["fill_to"]) - cx.at(P["fill_at"]))), 1.2)
    nshow = int(TALLY_N * p)
    if nshow > 0:
        acc, nfull, part = 0, 0, None                               # tam satırlar tek kırpmada, yarım satır ayrı kırpmada
        for (ya, yb, xs) in rows:
            if acc + len(xs) <= nshow:
                acc += len(xs)
                nfull += 1
                continue
            if nshow > acc:
                part = (ya, yb, xs, nshow - acc)
            break
        clips = []
        if nfull:
            clips.append(skia.Rect.MakeLTRB(gx0 - 4, gy0 + rows[0][0], gx0 + 610.0, gy0 + rows[nfull - 1][1] + 1.0))
        if part is not None:
            ya, yb, xs, nh = part
            clips.append(skia.Rect.MakeLTRB(gx0 - 4, gy0 + ya, gx0 + xs[nh - 1] + 3.0, gy0 + yb + 1.0))
        kg = _wp(cx, P.get("h137_at"), 0.5)                         # ilk 137 'yüz otuz yedi'de yaldızlanır (önce düz mürekkep)
        for rc in clips:
            c.save()
            c.clipRect(rc)
            c.drawImageRect(img_i, skia.Rect.MakeXYWH(gx0 - 2, gy0 - 2, img_i.width() / sc, img_i.height() / sc), skia.SamplingOptions(skia.FilterMode.kLinear))
            if kg > 0:
                c.drawImageRect(img_g, skia.Rect.MakeXYWH(gx0 - 2, gy0 - 2, img_g.width() / sc, img_g.height() / sc), skia.SamplingOptions(skia.FilterMode.kLinear),
                                skia.Paint(Alphaf=kg))
            c.restore()
        if 0 < p < 1:
            if part is not None:
                ya, yb, xs, nh = part
                tip = (gx0 + xs[nh - 1] + 6, gy0 + (ya + yb) / 2 + 4)
            elif nfull:
                ya, yb, xs = rows[nfull - 1]
                tip = (gx0 + xs[-1] + 6, gy0 + (ya + yb) / 2 + 4)
    kh = _wp(cx, P.get("h137_at"), 0.5)
    if kh > 0:                                                  # ilk 137 çentik yaldız (en zengin 137 hane): yaldız parıltısı + kızıl kalem işareti
        ya, yb, xs = rows[0]
        xg = gx0 + xs[min(len(xs), TALLY_GOLD) - 1] + 6
        f.rect(gx0 - 4, gy0 + ya - 1, xg - gx0 + 6, yb - ya + 3, color="#F0D27A", alpha=0.30 * kh, blur=3)
        _hand_line(c, [(gx0 - 2, gy0 + yb + 3), (xg, gy0 + yb + 2)], col=INK_R, w=2.6, a=kh, seed=137, wob=0.8, k=kh)
        r = _write(f, "137 HANE", xg, gy0 - 14, 32, _wp(cx, P.get("h137_at"), 0.7), face="title_m", color=INK_R, align="c")
        tip = r or tip
    cnt = int(math.floor(TALLY_N * p / 60.0) * 60) if p < 0.999 else TALLY_N
    if p > 0:
        _ink_e(f, f"{CM.fmt_int(cnt)} HANE", x0 + 395, y0 + 612, face="title_m", size=40, track=6)
    # kayıtlı servet: elle cetvellenmiş bant (%100) içinde 137 hanenin payı %29,8 — mürekkep taraması (dolum çubuğu değil)
    kb = _wp(cx, P.get("bar_at"), 0.6)
    if kb > 0:
        bx0, by0, bw, bh = x0 + 95, y0 + 712, 600.0, 46.0
        ke = _edge_k(c, bx0, by0, bx0 + bw, by0 + bh)
        _hand_line(c, [(bx0, by0), (bx0 + bw, by0 + 1), (bx0 + bw - 1, by0 + bh), (bx0 + 1, by0 + bh - 1), (bx0, by0)], w=2.6, a=0.9 * ke, seed=298, wob=1.1, k=kb)
        r = _write(f, "KAYITLI SERVET", bx0 + bw / 2, by0 - 22, 32, kb, face="title_m")
        tip = r or tip
        uf = ease_io(_wp(cx, P.get("fill_bar_at"), 0.9), 1.5)
        if uf > 0:
            xr, yr = _hatch_band(f, bx0, by0, bw, bh, 0.298, uf)
            if uf < 1:
                tip = (xr, yr)
            _ink_e(f, "%29,8 · 137 HANE", bx0, by0 + bh + 54, face="title", size=40, color=INK_R, align="l", track=3, alpha=clamp(uf * 1.5))
    if P.get("stamp_at") is not None:                           # kayıtların üstüne basılmış damga (çetele bloğunun sağ altı)
        _stamp_e(f, "BİR HESABA GÖRE", x0 + 520, y0 + 470, -0.07, 38, _wp(cx, P["stamp_at"], 0.3))
    # sağ sayfa: en zengini
    x0, y0 = _page_origin("r")
    r = _write(f, "PALLA STROZZİ", x0 + 395, y0 + 260, 50, _wp(cx, P.get("name_at"), 0.9), face="title")
    tip = r or tip
    r = _write(f, "1427'NİN EN ZENGİNİ", x0 + 395, y0 + 330, 34, _wp(cx, P.get("role_at"), 0.9), face="title_m", color="#4A3420")
    tip = r or tip
    kn = _wp(cx, P.get("num_at"), 0.35)
    if kn > 0:
        e = ease_out(clamp((cx.t - cx.at(P["num_at"])) / 0.8), 3)
        v = 163000 if e >= 0.999 else math.floor(163000 * e / 1000.0) * 1000
        _ink_e(f, CM.fmt_int(v), x0 + 395, y0 + 520, face="title", size=104, alpha=kn)
        _write(f, "FLORİN · YAKLAŞIK", x0 + 395, y0 + 600, 34, _wp(cx, P.get("num_at"), 1.0), face="title_m", color=INK_R)
        _hand_line(c, [(x0 + 150, y0 + 640), (x0 + 640, y0 + 638)], w=2.2, a=0.7 * kn, seed=163, wob=0.9)
    return tip


_MASA_FN = {"iz": _masa_iz, "catasto": _masa_catasto}      # kurul tur 3: "kasa" artık c2_yakin scene="kasa" (≥2× yakın plan; AN2-Ö1, PK2-N1)


@ckind("c2_masa")
def k_masa(cx, v="iz", cams=None, seed=3, **P):
    """Masa üstü açık defter (üstten bakış). v: iz | catasto (kurul tur 3: bölümde üstten tam açılım EN ÇOK İKİ — kasa ≥2× yakın plana, 150.000+
    kapalı defterlere taşındı; AN2-Ö1, PK2-N1). P: içerik çapaları (bkz. _masa_*). Ön plan: bulanık şamdan (paralaks). Gündüz ışığı + mum hâlesi;
    kamera kendi yolunda (cams); sert kesmeyle birleşen uçta kamera durmaz (CUT_SLOPE; geçiş uçları eskisi gibi yumuşak)."""
    f = cx.f
    c = f.c
    dur = max(cx.dur, 1e-3)
    camx, camy, z = _wcam(cx, cams or [(0.0, (1300.0, 860.0, 1.0))], dur, ends=_ends(cx, cut_only=True))
    camx += 3.0 * math.sin(cx.t * 0.9 + 1.3)                   # elde tutulan hafif salınım
    camy += 2.0 * math.sin(cx.t * 0.7)
    f.clear("#1A120C")
    c.save()
    c.translate(W / 2, H / 2)
    c.scale(z, z)
    c.translate(-camx, -camy)
    img = _masa_base(v)
    c.drawImageRect(img, skia.Rect.MakeWH(img.width(), img.height()), skia.Rect.MakeWH(MW, MH), skia.SamplingOptions(skia.FilterMode.kLinear))
    V = MASA_V[v]
    if V.get("candle"):
        cxm, cym = V["candle"]
        f.circle(cxm, cym - 120, 420, shader=f.rad(cxm, cym - 120, 420, [("#FFD68A", 0.0, 70), ("#FFD68A", 1.0, 0)]))
        OD.candle(f, cxm, cym, 230, cx.t, 2.3, lit=1.0, holder=True, smoke=False, halo=1.0, night=False)
    tip = _MASA_FN[v](cx, f, P)
    if tip is not None:                                        # tüy kalem: yazının ucunu izler
        OD.quill(c, tip[0] + 10, tip[1] + 6, -58.0, 2.0)
        _A.hint_speed(cx, 4.0)
    c.restore()
    # ön plan nesne katmanı (SA1-Y6): kadraj kenarında bulanık nesne; kamera kayınca daha hızlı ters kayar (paralaks), gerekirse kadrajdan çıkar
    cams_ = cams or [(0.0, (1300.0, 860.0, 1.0))]
    fg = V.get("fg", ("candle", "l"))
    base_x = 130.0 if fg[1] == "l" else W - 130.0
    k0 = sorted(((cx.at(a) if not isinstance(a, (int, float)) else float(a)), v_) for a, v_ in cams_)[0][1]
    fgx = base_x - (camx - k0[0]) * z * 0.45
    if -200 < fgx < W + 200:
        fgy = H + 40
        if fg[0] == "candle":
            f.rect(fgx - 34, fgy - 560, 68, 600, color="#1A120A", alpha=0.88, blur=12)
            f.oval(fgx, fgy - 580, 74, 26, color="#2A1E12", alpha=0.88, blur=9)
            f.circle(fgx + 4, fgy - 650, 170, shader=f.rad(fgx + 4, fgy - 650, 170, [("#FFE0A0", 0.0, 120), ("#FFE0A0", 1.0, 0)]))
            f.oval(fgx + 4, fgy - 664, 16, 40, color="#FFF2C8", alpha=0.85, blur=7)
        else:
            for k_ in range(3):
                f.oval(fgx + (k_ - 1) * 60, fgy - 120 - k_ * 70, 260, 70, color=["#CDBB90", "#BFAE84", "#D8C8A0"][k_], alpha=0.92, blur=10)
                f.rect(fgx + (k_ - 1) * 60 - 6, fgy - 190 - k_ * 70, 12, 140, color="#7A2418", alpha=0.85, blur=8)
    CM.finish(f, cx, motes_n=16)


# ─────────────────────────────────────────────────────────────────────────────
# c2_yakin — NESNE + EL YAKIN PLANI (≥2× ara plan; AN2-Ö3 "598 sn'de tek el/nesne yakın planı yok"). Yüz yok; el ve nesne.
# ─────────────────────────────────────────────────────────────────────────────
def _soft_bg(f, cols, seed=1, t=0.0, spots=None):
    """Alan derinliği: yumuşak renk alanı + bulanık ışık lekeleri (bokeh) — arkadaki odanın renkleri."""
    f.rect(0, 0, W, H, shader=f.lin(0, 0, W, H, [(cols[0], 0.0), (cols[1], 0.55), (cols[2], 1.0)]))
    rs = _PN._RS(seed)
    for k in range(9):
        x, y = rs.uniform(0, W), rs.uniform(0, H * 0.7)
        r = rs.uniform(60, 180)
        col = (spots or ["#FFE6B0", "#F0D27A"])[k % len(spots or ["#FFE6B0", "#F0D27A"])]
        f.circle(x + 6 * math.sin(t * 0.4 + k), y, r, color=col, alpha=rs.uniform(0.06, 0.16), blur=r * 0.35)


def _letter(f, x, y, w, h, rot=0.0, alpha=1.0, seal=True):
    """Katlanmış poliçe/mektup (masada): krem kâğıt, kat izleri, okunmaz satırlar, kırmızı mühür."""
    c = f.c
    c.save(); c.translate(x, y); c.rotate(math.degrees(rot))
    f.rrect(-w / 2 + 8, -h / 2 + 10, w, h, 6, color="#000000", alpha=0.30 * alpha, blur=10)
    f.rrect(-w / 2, -h / 2, w, h, 6, shader=f.lin(0, -h / 2, 0, h / 2, [("#F6EDD0", 0.0), ("#E2D3A6", 1.0)]), alpha=alpha)
    f.rrect(-w / 2, -h / 2, w, h, 6, style="stroke", sw=2.4, color="#5A3E22", alpha=0.85 * alpha)
    for k in (1, 2):
        c.drawLine(-w / 2 + w * k / 3, -h / 2 + 4, -w / 2 + w * k / 3, h / 2 - 4, f.paint("#B8A47A", style="stroke", sw=1.4, alpha=0.7 * alpha))
    for i in range(4):
        c.drawLine(-w / 2 + 28, -h / 2 + 34 + i * 26, w / 2 - 40 - (i % 2) * 50, -h / 2 + 34 + i * 26, f.paint("#5A4630", style="stroke", sw=2.0, alpha=0.45 * alpha))
    if seal:
        CM.wax_seal(f, w / 2 - 46, h / 2 - 40, 26, "#A52A1C", alpha=alpha, t=1.0)
    c.restore()


# ── kurul tur 3: c2_yakin kasa yakın planı (≥2×; #83) — dünya 2600×1460, kendi kamerası (cams) ──
KW, KH = 2600, 1460
_KASA_IMG = {}
KASA_STRIP = (220.0, 440.0, 2300.0, 830.0)                   # kâğıt şerit (cartellino): x0, y0, x1, y1 (dünya)
KASA_KEYS = (1460.0, 1035.0)                                 # anahtarların kapaktaki yeri (şeridin hemen altında: yazım boyunca kadrajda)


def _kasa_base():
    """Papalık kasası yakın planı (bir kez pişirilir): kızıl kadife kaplı sandık kapağı — yaldızlı demir kuşaklar, çiviler, ön kenarda kilit aynası;
    arkada koyu ceviz masa ve uzakta mum ışığı (bulanık). Kâğıt şerit ayrı (her karede; yazılar kenar söndürmesiyle)."""
    img = _KASA_IMG.get("k")
    if img is not None:
        return img
    sc = 1.25
    fr = sk.Frame(int(KW * sc), int(KH * sc))
    c = fr.c
    c.scale(sc, sc)
    lid = 300.0
    OD.GRAD_V(c, 0, 0, KW, lid + 20, [("#22140C", 0.0), ("#3E2618", 1.0)])               # uzak masa (ceviz)
    rs = OD._RS(83)
    for k in range(9):
        y = rs.uniform(20, lid)
        c.drawLine(0, y, KW, y + rs.uniform(-6, 6), OD.STK("#140A04", rs.uniform(1.0, 2.2), int(rs.uniform(30, 70))))
    fr.circle(2250, 120, 260, color="#FFD68A", alpha=0.22, blur=90)                       # uzak mum (alan derinliği)
    fr.circle(2250, 150, 34, color="#FFF0C0", alpha=0.65, blur=14)
    fr.circle(420, 90, 140, color="#C9A23A", alpha=0.10, blur=60)
    OD.GRAD_V(c, 0, lid, KW, KH, [("#93283A", 0.0), ("#6E1824", 0.5), ("#4C0E18", 1.0)])  # kızıl kadife kapak
    for k in range(30):                                                                     # kadife tüy yönü / hafif kıvrım gölgesi
        x = rs.uniform(-200, KW)
        c.drawLine(x, lid, x + rs.uniform(-160, 160), KH, OD.STK("#000000", rs.uniform(16, 44), int(rs.uniform(8, 20))))
    for yy in range(int(lid) + 70, KH, 120):                                               # soluk damasko (sırma)
        for xx in range(60 + (yy // 120 % 2) * 60, KW, 120):
            c.drawPath(sk.poly_path([(xx, yy - 15), (xx + 10, yy), (xx, yy + 15), (xx - 10, yy)]), OD.PT("#D2A33E", 26))
    def gilt_band(x0, y0, x1, y1):
        c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), OD.LGP((x0, 0), (x1, 0), [("#E8C25A", 0.0), ("#B8862E", 0.45), ("#7A5418", 1.0)]))
        c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), OD.STK(OD.INK, 2.0, 200))
    fr.rect(0, lid - 2, KW, 30, color="#000000", alpha=0.35, blur=8)
    gilt_band(0, lid - 14, KW, lid + 14)                                                    # kapak kenarı (yaldızlı demir)
    for xs in (410.0, 2190.0):                                                              # demir kuşaklar (yaldız)
        fr.rect(xs - 30, lid, 80, KH - lid, color="#000000", alpha=0.30, blur=10)
        gilt_band(xs - 36, lid + 14, xs + 36, KH)
        for yy in range(int(lid) + 70, KH, 96):
            fr.circle(xs, yy, 11, color="#F4DE90")
            fr.circle(xs, yy, 11, style="stroke", sw=2.0, color=OD.INK, alpha=0.8)
    for xx in range(60, KW, 110):                                                           # kenar çivileri
        fr.circle(xx, lid, 7, color="#F4DE90")
        fr.circle(xx, lid, 7, style="stroke", sw=1.6, color=OD.INK, alpha=0.8)
    kx0, ky0 = 1180.0, 1320.0                                                               # ön kenarda kilit aynası (anahtar deliği)
    fr.rrect(kx0 + 8, ky0 + 12, 240, 170, 16, color="#000000", alpha=0.35, blur=10)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(kx0, ky0, kx0 + 240, ky0 + 170), 16, 16),
                OD.LGP((kx0, 0), (kx0 + 240, 0), [("#F0D27A", 0.0), ("#B8862E", 0.5), ("#7A5418", 1.0)]))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(kx0, ky0, kx0 + 240, ky0 + 170), 16, 16), OD.STK(OD.INK, 2.4, 210))
    kh = skia.Path()
    kh.addCircle(kx0 + 120, ky0 + 62, 18)
    kh.addRect(skia.Rect.MakeLTRB(kx0 + 112, ky0 + 66, kx0 + 128, ky0 + 120))
    c.drawPath(kh, OD.PT("#1A0E06"))
    img = fr.surf.makeImageSnapshot()
    _KASA_IMG["k"] = img
    return img


def _kasa_strip(f, alpha=1.0):
    """Kâğıt şerit (cartellino): krem kâğıt, tırtıklı kenar, kenar gölgesi, iki uçta yaldız çivi (sandığın kapağına iğneli)."""
    x0, y0, x1, y1 = KASA_STRIP
    rs = _PN._RS(422)
    pts = []
    n = 40
    for i in range(n + 1):
        pts.append((lerp(x0, x1, i / n), y0 + rs.uniform(-3.5, 3.5)))
    for i in range(10 + 1):
        pts.append((x1 + rs.uniform(-4, 4), lerp(y0, y1, i / 10)))
    for i in range(n, -1, -1):
        pts.append((lerp(x0, x1, i / n), y1 + rs.uniform(-3.5, 3.5)))
    for i in range(10, -1, -1):
        pts.append((x0 + rs.uniform(-4, 4), lerp(y0, y1, i / 10)))
    pth = sk.poly_path(pts)
    sh = skia.Path(pth)
    sh.offset(12, 16)
    f.path(sh, color="#000000", alpha=0.38 * alpha, blur=12)
    f.c.drawPath(pth, f.paint(alpha=alpha, shader=f.lin(0, y0, 0, y1, [("#F6EDD0", 0.0), ("#EADBB0", 0.6), ("#DCCB98", 1.0)])))
    f.c.drawPath(pth, f.paint("#6A4E2E", style="stroke", sw=2.2, alpha=0.8 * alpha))
    for i in range(7):                                                 # kâğıt lifleri / leke
        xx, yy = rs.uniform(x0 + 40, x1 - 40), rs.uniform(y0 + 20, y1 - 20)
        f.circle(xx, yy, rs.uniform(18, 46), color="#C9B07A", alpha=0.10 * alpha, blur=14)
    for xx in (x0 + 34, x1 - 34):                                      # yaldız çiviler
        f.circle(xx + 3, (y0 + y1) / 2 + 5, 17, color="#000000", alpha=0.35 * alpha, blur=4)
        f.circle(xx, (y0 + y1) / 2, 15, shader=f.rad(xx - 4, (y0 + y1) / 2 - 5, 18, [("#FFF0B0", 0.0), ("#C9962B", 0.6), ("#7A5418", 1.0)]), alpha=alpha)


def _notch(c, x, y_top, y_bot, broken, seed, k=1.0, col=INK_C):
    """Tek çentik (tüy kalem): düz (kesintisiz) ya da ortası boş iki parça (aralıklı). k: çizilen pay."""
    if k <= 0:
        return
    rs = _PN._RS(seed)
    dx = rs.uniform(-2.5, 2.5)
    if not broken:
        _hand_line(c, [(x, y_top + rs.uniform(-2, 2)), (x + dx, y_bot + rs.uniform(-2, 2))], col=col, w=4.2, seed=seed, wob=0.6, k=k)
    else:
        ym1, ym2 = lerp(y_top, y_bot, 0.40), lerp(y_top, y_bot, 0.62)
        k1, k2 = clamp(k * 2.0), clamp(k * 2.0 - 1.0)
        _hand_line(c, [(x, y_top), (x + dx * 0.4, ym1)], col=col, w=4.0, seed=seed, wob=0.5, k=k1)
        _hand_line(c, [(x + dx * 0.6, ym2), (x + dx, y_bot)], col=col, w=4.0, seed=seed + 1, wob=0.5, k=k2)


def _yakin_kasa(cx, f, P):
    """KASA (c2s21) — ≥2× yakın plan: kızıl kadife kaplı papalık kasası; baş öğe EL ve ANAHTARLAR (el anahtarları 'memurluğu'nda kapağa bırakır,
    açılıp kadrajdan çekilir); bilgi sandığın kapağına iğneli kâğıt şeritte (cartellino), tüy kalem diliyle: başlık İLK KAREDE yazılı, '1422', 22 düz çentik
    (KESİNTİSİZ), ardından 18 kesikli çentik (ARALIKLI), MEDİCİ'DE KALDI. Altın kapsül dolum çubuğu YOK (SA1-Y6-k). Sözcük ve sayılar eskisiyle aynı."""
    c = f.c
    img = _kasa_base()
    c.drawImageRect(img, skia.Rect.MakeWH(img.width(), img.height()), skia.Rect.MakeWH(KW, KH), skia.SamplingOptions(skia.FilterMode.kLinear))
    _kasa_strip(f)
    x0s, y0s, x1s, y1s = KASA_STRIP
    tip = None
    tsz = CM.fit_size("PAPALIĞIN RESMÎ KASA MEMURLUĞU", "title_m", 58, 1560, 5.0)
    _ink_e(f, "PAPALIĞIN RESMÎ KASA MEMURLUĞU", 1260.0, 516.0, face="title_m", size=tsz, track=5.0)       # başlık ilk karede yazılı
    _hand_line(c, [(470, 542), (2050, 540)], col="#8E6A3E", w=1.6, a=0.55, seed=5, wob=0.7)              # başlık altı kalem çizgisi
    yt, yb, ybase = 622.0, 690.0, 702.0
    xa0, step, xb0 = 600.0, 24.0, 1175.0
    # 1422 + başlangıç çentiği
    k14 = _wp(cx, P.get("start_at"), 0.45)
    if k14 > 0:
        w14 = sk.text_width("1422", "title", 58, 3.0)
        r = _write(f, "1422", 548.0 - w14, 678.0, 58, k14, face="title", color=INK_R, track=3.0, align="l")
        tip = r or tip
        _hand_line(c, [(568, yt - 16), (566, yb + 16)], col=INK_R, w=5.0, seed=14, wob=0.5, k=clamp(k14 * 1.6 - 0.6))
    # 22 düz çentik (kesintisiz) + sürekli cetvel çizgisi
    ta, tb = P.get("a_at"), P.get("a_to")
    if ta is not None:
        pa = clamp((cx.t - cx.at(ta)) / max(0.2, cx.at(tb) - cx.at(ta))) if tb is not None else _wp(cx, ta, 0.8)
        if pa > 0:
            na = 22 * pa
            _hand_line(c, [(566, ybase), (xa0 + 21 * step + 14, ybase + 1)], w=2.6, seed=221, wob=0.8, k=clamp(na / 22.0))
            for i in range(22):
                if i >= na:
                    break
                _notch(c, xa0 + i * step, yt, yb, False, 300 + i, k=clamp(na - i))
            if pa < 1:
                tip = (xa0 + min(21, int(na)) * step, yt + 30)
        r = _write(f, "22 YIL", xa0 + 10.5 * step, 592.0, 50, _wp(cx, P.get("a_lab"), 0.4), face="title", color=INK_C, track=4.0)
        tip = r or tip
        r = _write(f, "KESİNTİSİZ", xa0 + 10.5 * step, 762.0, 40, _wp(cx, P.get("a_word"), 0.6), face="title_m", color=INK_C, track=4.0)
        tip = r or tip
    # 18 kesikli çentik (aralıklı) + kesik kesik cetvel çizgisi
    tb0, tb1 = P.get("b_at"), P.get("b_to")
    if tb0 is not None:
        pb = clamp((cx.t - cx.at(tb0)) / max(0.2, cx.at(tb1) - cx.at(tb0))) if tb1 is not None else _wp(cx, tb0, 0.8)
        if pb > 0:
            nb = 18 * pb
            for i in range(18):
                if i >= nb:
                    break
                ki = clamp(nb - i)
                _notch(c, xb0 + i * step, yt, yb, True, 500 + i, k=ki)
                if i % 2 == 0:                                         # cetvel çizgisi de kesik kesik
                    _hand_line(c, [(xb0 + i * step - 8, ybase), (xb0 + i * step + step + 4, ybase + 1)], w=2.4, seed=520 + i, wob=0.6, k=ki)
            if pb < 1:
                tip = (xb0 + min(17, int(nb)) * step, yt + 30)
        r = _write(f, "+ 18 YIL", xb0 + 8.5 * step, 592.0, 50, _wp(cx, P.get("b_lab"), 0.45), face="title", color=INK_C, track=4.0)
        tip = r or tip
        r = _write(f, "ARALIKLI", xb0 + 8.5 * step, 762.0, 40, _wp(cx, P.get("b_word"), 0.6), face="title_m", color=INK_C, track=4.0)
        tip = r or tip
    km = _wp(cx, P.get("medici_at"), 0.8)
    if km > 0:
        r = _write(f, "MEDİCİ'DE KALDI", 1660.0, 676.0, 50, km, face="title", color=INK_R, track=4.0, align="l")
        tip = r or tip
        wdm = sk.text_width("MEDİCİ'DE KALDI", "title", 50, 4.0)
        ku = _wp(cx, P.get("kaldi_at"), 0.45)
        if ku > 0:
            ke = _edge_k(c, 1660.0, 640.0, 1660.0 + wdm, 700.0)
            _hand_line(c, [(1660, 696), (1660 + wdm, 699)], col=INK_R, w=3.4, a=0.9 * ke, seed=88, wob=0.9, k=ku)
            if ku < 1:
                tip = (1660 + wdm * ku, 698)
    return tip


def _kasa_keys(cx, f, P):
    """El anahtarları getirir (çan eğrisi + %8 aşmalı oturma: anim.settle; yolda ≈10° bilek dönüşü), 'memurluğu'nda kapağa bırakır,
    açılıp kadrajdan çekilir (soldurma YOK; SA1-N4 ilkesi). Taşınırken anahtarlar kameraya yakın: biraz büyük, gölge uzak."""
    t_in, t_rel = cx.at(P["keys_at"]), cx.at(P["release_at"])
    kx1, ky1 = KASA_KEYS
    kx0, ky0 = 2620.0, 960.0
    st = _A.settle(cx.t, t_in, P.get("keys_dur", 1.35), 0.08)
    u = clamp(st)
    kx = lerp(kx0, kx1, st)
    ky = lerp(ky0, ky1, st) - 70.0 * math.sin(math.pi * u)
    lift = 1.0 - smooth(clamp((cx.t - (t_in + P.get("keys_dur", 1.35) * 0.75)) / 0.35))   # bırakmaya yakın kapağa iner
    ksz = 580.0 * (1.0 + 0.07 * lift)
    rot = lerp(-0.12, -0.30, smooth(u)) + 0.025 * _A.wobble(cx.t, t_in + P.get("keys_dur", 1.35), 1.0, 3.2, 6.0)
    f.oval(kx + 18 + 40 * lift, ky + 30 + 46 * lift, 250 * (1.0 + 0.2 * lift), 120, color="#000000", alpha=0.30 - 0.10 * lift, blur=10 + 14 * lift)
    _icons_draw(f, "p1_anahtar", kx, ky, ksz, "gold", rot=rot, shadow=False)
    # el: anahtarların kesişim noktasını kavrar; bıraktıktan sonra açılır ve sağa-aşağı kadraj dışına çekilir
    ho = ease_io(clamp((cx.t - t_rel) / 0.85), 1.8)
    ang = lerp(196.0, 186.0, smooth(u)) + 6.0 * ho                   # yolda ≈10° bilek dönüşü
    hx = kx + 120.0 + ho * 1200.0
    hy = ky + 40.0 + ho * 260.0
    if ho < 1.0 and hx < KW + 1200:
        arm_hand(f, hx, hy, ang, 360.0, sleeve=P.get("sleeve", "#6E1C1E"), cuff=P.get("cuff", "#C9A23A"), kind="fist" if cx.t < t_rel else "open", flip=True, reach=5.0)
    v = 0.0
    dt = 1.0 / 24.0
    st2 = _A.settle(cx.t + dt, t_in, P.get("keys_dur", 1.35), 0.08)
    v = max(v, _A.speed_of((kx, ky), (lerp(kx0, kx1, st2), lerp(ky0, ky1, st2)), dt))
    v = max(v, 1200.0 * (ease_io(clamp((cx.t + dt - t_rel) / 0.85), 1.8) - ho) / dt / 24.0)
    return v


def _kese(cx, f, P):
    """Brugge kesesi (c2s3) — kurul tur 3 (AN1-Y-N2, SA1-N4): el kesmenin İÇİNDE zaten hareketli (hareket üstünde kesme), keseyi çan eğrisiyle sürer ve
    %8 aşmayla OTURUR (anim.settle); yolda ≈10° bilek dönüşü. Tüccar poliçeyi sürer, sonra keseyi alıp kadrajdan ÇIKAR (kol solmaz, geri çekilir);
    banker poliçeyi kendine çeker. Dönüş: bu karedeki en büyük nesne hızı (px/kare; deklanşör ipucu)."""
    c = f.c
    f.rect(-60, -60, W + 120, 620, shader=f.lin(0, 0, 0, 560, [("#AEB6B6", 0.0), ("#C9CEC9", 1.0)]))
    f.rrect(150, 40, 330, 420, 10, color="#EEF4F6", alpha=0.85, blur=26)
    f.rect(305, 40, 20, 420, color="#3A2E24", alpha=0.6, blur=14)
    f.rect(150, 210, 330, 18, color="#3A2E24", alpha=0.6, blur=14)
    f.circle(1500, 230, 70, color="#5A6468", alpha=0.7, blur=18)
    f.rect(-60, 520, W + 120, 620, shader=f.lin(0, 520, 0, H, [("#2C3640", 0.0), ("#1A2028", 1.0)]))           # Brugge masa örtüsü (koyu arduvaz)
    f.line(-60, 522, W + 60, 522, color="#B8A070", sw=4, alpha=0.85)
    _letter(f, 1600, 930, 360, 230, rot=0.10, alpha=0.9, seal=False)
    OD.inkwell(c, 1690, 560, 2.6, cx.t)
    OD.draw_coins(c, 300, 880, 12, 2.6, cx.t, seed=3, glint=True)
    t_push, t_pol = cx.at(P["push_at"]), cx.at(P["pol_at"])
    t_take, t_get = cx.at(P["take_at"]), cx.at(P["get_at"])
    dt = 1.0 / 24.0

    def purse(t):
        sp = _A.settle(t, t_push, 1.0, 0.08)                         # banker sürer: çan eğrisi + oturma
        x = lerp(430.0, 1080.0, sp)
        y = 760.0 - 34.0 * math.sin(math.pi * clamp(sp))
        tk = ease_in(clamp((t - t_take) / 0.9), 2.2)                  # tüccar alır, sağa kadraj dışına çeker (hızlanarak)
        return x + tk * 1500.0, y - 10.0 * math.sin(math.pi * tk), sp, tk

    def letter(t):
        sl = _A.settle(t, t_pol, 0.95, 0.08)                         # tüccar poliçeyi sola sürer, oturur
        x = lerp(2250.0, 900.0, sl)
        g = _A.settle(t, t_get, 0.8, 0.07)                           # banker poliçeyi kendine çeker
        return x - 230.0 * g, 560.0 + 30.0 * g, sl, g

    px, py, sp, tk = purse(cx.t)
    lx, ly, sl, g = letter(cx.t)
    f.oval(px + 16, py + 66, 150, 30, color="#000000", alpha=0.32, blur=10)
    _icons_draw(f, "p1_kese", px, py, 300, "bronze")
    if cx.t >= t_pol - 0.2 and lx < W + 400:
        _letter(f, lx, ly, 300, 190, rot=-0.06 + 0.05 * clamp(sl) - 0.04 * g)
    # banker (sol, lacivert yen): keseyi sürer → bırakır, hafif geri çekilir → poliçeyi kendine çeker
    rel = ease_io(clamp((cx.t - (t_push + 1.15)) / 0.6), 1.6)
    reach = _A.settle(cx.t, t_get - 0.45, 0.45, 0.08)
    hbx = (px - 250.0) * (1.0 - rel) + 520.0 * rel
    hbx = hbx + (lx - 280.0 - hbx) * clamp(reach) if cx.t >= t_get - 0.45 else hbx
    hby = 800.0 - 8.0 * math.sin(cx.t * 1.7) * rel
    hby = lerp(hby, ly + 40.0, clamp(reach)) if cx.t >= t_get - 0.45 else hby
    ang_b = lerp(-16.0, -6.0, smooth(clamp(sp))) + 4.0 * rel - 6.0 * clamp(reach)
    arm_hand(f, hbx, hby, ang_b, 250, sleeve="#3E4C8C", cuff="#5A4030", kind="open")
    # tüccar (sağ, açık mavi yen): poliçeyi sürer (elde), bırakır, keseye uzanır, keseyle birlikte kadrajdan çıkar
    if cx.t >= t_pol - 0.2:
        to_purse = ease_io(clamp((cx.t - (t_pol + 1.0)) / 0.55), 1.6)
        if cx.t < t_pol + 1.0:
            hmx, hmy = lx + 270.0, 580.0
            angm = lerp(188.0, 178.0, smooth(clamp(sl)))
        else:
            hmx = lerp(lx + 270.0, px + 230.0, to_purse) if tk <= 0 else px + 230.0
            hmy = lerp(580.0, py + 20.0, to_purse) if tk <= 0 else py + 20.0
            angm = lerp(178.0, 184.0, to_purse)
        if hmx < W + 1100:
            arm_hand(f, hmx, hmy, angm, 250, sleeve="#5A7EC0", cuff="#E0B84E", kind="fist" if cx.t >= t_take - 0.05 else "open", flip=True)
    p2 = purse(cx.t + dt)
    l2 = letter(cx.t + dt)
    return max(_A.speed_of((px, py), p2[:2], dt), _A.speed_of((lx, ly), l2[:2], dt) if cx.t >= t_pol - 0.2 else 0.0)


def _mitra(cx, f, P):
    """Rehin mitra (c2s20) — kurul tur 3 (AN1-Y-N2): papalık eli çan eğrisiyle gelip %8 aşmayla OTURUR, yolda ≈8° bilek dönüşü; Giovanni'nin elleri
    nefes alır ve el yaklaşınca mitrayı hafifçe kendine çeker (oturmalı). Kamera: itme + sağa kayma (k_yakin). Dönüş: en büyük nesne hızı (px/kare)."""
    f.rect(-60, -60, W + 120, H + 120, shader=f.lin(0, 0, W, H, [("#6A2420", 0.0), ("#8E3A2C", 0.5), ("#3A1414", 1.0)]))
    for (x_, y_, r_, col_) in ((300, 200, 160, "#F0D27A"), (1620, 160, 120, "#FFE6B0"), (1500, 760, 200, "#C9A23A"), (220, 820, 140, "#FFFFFF")):
        f.circle(x_, y_, r_, color=col_, alpha=0.10, blur=r_ * 0.4)
    tr_ = cx.at(P["reach_at"])
    dt = 1.0 / 24.0

    def papal(t):
        s = _A.settle(t, tr_, 0.70, 0.08)                           # varış ≈0,7 sn; oturma çekim içinde görünür
        return lerp(2250.0, 1370.0, s), lerp(360.0, 400.0, s), s

    pxh, pyh, sh_ = papal(cx.t)
    draw = _A.settle(cx.t, tr_ + 0.45, 0.45, 0.10)                  # Giovanni el yaklaşınca mitrayı kendine çeker
    breath = 3.0 * math.sin(cx.t * 1.9)
    ox, oy = -26.0 * draw, 14.0 * draw + breath
    mx, my = 900 + ox, 500 + oy
    f.circle(mx, my - 20, 360, shader=f.rad(mx, my - 20, 360, [("#F0D27A", 0.0, 70), ("#F0D27A", 1.0, 0)]))
    _icons_draw(f, "c2_mitra", mx, my + 2 * math.sin(cx.t * 1.6), 480, "gold", rot=-0.035 * draw)
    arm_hand(f, mx - 210 + 1.5 * breath, my + 270, -38.0 - 3.0 * draw, 250, sleeve="#6E1C1E", cuff="#7A5A3A", kind="open", fur=True)     # Giovanni: koyu kızıl yen
    arm_hand(f, mx + 210 - 1.5 * breath, my + 275, 218.0 + 3.0 * draw, 250, sleeve="#6E1C1E", cuff="#7A5A3A", kind="open", flip=True, fur=True)
    if cx.t >= tr_ - 0.05:                                          # papalık eli (beyaz yen, altın ağız) sağdan uzanır: "geri almak için"
        arm_hand(f, pxh, pyh, lerp(194.0, 186.0, smooth(clamp(sh_))), 270, sleeve="#EDE4CC", cuff="#C9A23A", kind="point", flip=True)
    p2 = papal(cx.t + dt)
    return _A.speed_of((pxh, pyh), p2[:2], dt) if cx.t >= tr_ - 0.05 else 0.0


@ckind("c2_yakin")
def k_yakin(cx, scene="kese", push=0.06, seed=4, cams=None, drift=(0.0, 0.0), **P):
    """NESNE + EL YAKIN PLANI (≥2× ara plan; yüz yok). scene: 'kese' (Brugge: kese peşin verilir, karşılığında poliçe) · 'mitra' (rehin mitra
    Giovanni'nin elinde; papalık eli uzanır) · 'kalem' (tüy kalem eseri yazar; Medici siparişinin mührü — NESNE YILI 1520) · 'kasa' (kurul tur 3:
    papalık kasası, el anahtarları bırakır, kâğıt şeritte 22 + 18 yıl — eski üstten açık 'kasa' defterinin yerine; AN2-Ö1, PK2-N1).
    Kamera (kurul tur 3 AN1-Y-N3): uç eğimleri motordaki cilt_cam mantığıyla — SERT KESMEYLE birleşen uçta en az CUT_SLOPE (kesmede durmaz),
    geçişte CARRY; push (ekran ortasına itme) + drift (px, aynı eğriyle kayma) ya da cams=[(çapa, (x, y, zum))] dünya kamerası (kasa: 2600×1460)."""
    f = cx.f
    c = f.c
    dur = max(cx.dur, 1e-3)
    kin, kout = bool(getattr(cx, "cut_in", False)), bool(getattr(cx, "cut_out", False))
    e0, e1 = _ends(cx)
    if cams:
        camx, camy, zz = _wcam(cx, cams, dur, ends=(e0, e1))
        c.save()
        c.translate(W / 2, H / 2)
        c.scale(zz, zz)
        c.translate(-camx - 3.0 * math.sin(cx.t * 0.9 + 1.3), -camy - 2.0 * math.sin(cx.t * 0.7))
    else:
        s0, s1 = (max(1.8, e0), e1) if (kin and not kout) else ((e0, max(1.8, e1)) if (kout and not kin) else (e0, e1))
        u = _herm(cx.t / dur, s0, s1)                                # kesmeye giren/çıkan uçta kamera hareketli (eski: ease_out/ease_in, push=0'da duruyordu)
        zz = 1.0 + push * u
        c.save()
        c.translate(W / 2 + drift[0] * u, H / 2 + drift[1] * u)
        c.scale(zz, zz)
        c.translate(-W / 2 + 4 * math.sin(cx.t * 0.8), -H / 2 + 3 * math.sin(cx.t * 0.6))
    v = 0.0
    if scene == "kese":
        v = _kese(cx, f, P)
    elif scene == "mitra":
        v = _mitra(cx, f, P)
    elif scene == "kasa":
        tip = _yakin_kasa(cx, f, P)
        v = _kasa_keys(cx, f, P)
        if tip is not None:                                         # tüy kalem: yazının ucunu izler (masa defterleriyle aynı dil)
            OD.quill(c, tip[0] + 12, tip[1] + 8, -58.0, 2.3)
    elif scene == "kalem":
        f.rect(-60, -60, W + 120, H + 120, shader=f.lin(0, 0, W, H, [("#5A4630", 0.0), ("#6E583A", 0.5), ("#3A2C1E", 1.0)]))
        f.circle(1700, 160, 260, color="#FFE6B0", alpha=0.10, blur=90)
        px0, py0, pw, ph = 300, 170, 1300, 880                 # sipariş/eser kâğıdı
        f.rrect(px0 + 14, py0 + 18, pw, ph, 8, color="#000000", alpha=0.35, blur=14)
        f.rrect(px0, py0, pw, ph, 8, shader=f.lin(0, py0, 0, py0 + ph, [("#F4EAC8", 0.0), ("#E2D2A2", 1.0)]))
        f.rrect(px0, py0, pw, ph, 8, style="stroke", sw=3, color="#5A3E22", alpha=0.85)
        tw = cx.at(P.get("write_at", 0.0))
        ln = "Istorie fiorentine"                              # eserin adı (teyit_P1 kaynakları: MAC, Istorie fiorentine); belge metni UYDURULMAZ
        pr = clamp((cx.t - tw) / 1.2)
        wl = sk.text_width(ln, "fell_i", 74)
        if pr > 0:
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(px0 + 80, py0 + 80, px0 + 92 + wl * pr, py0 + 300))
            PP.hand(f, ln, px0 + 90, py0 + 230, face="fell_i", size=74, color="#24160A", alpha=1.0, jitter=1.0, seed=31)
            c.restore()
        tip = (px0 + 90 + wl * pr, py0 + 230)
        wd_ = ease_io(clamp((cx.t - tw - 1.25) / 0.6), 1.6)        # yazı bitince el kalemle sağa-yukarı çekilir (mühüre yer açılır)
        hx_, hy_ = tip[0] + 900 * wd_, tip[1] - 320 * wd_
        if wd_ < 0.999:
            arm_hand(f, hx_ + 120, hy_ - 30, 168.0, 190, sleeve="#C9A23A", cuff="#2E4A8A", kind="fist", reach=6.0)       # Machiavelli'nin eli (sarı cüppe, mavi ağız)
            OD.quill(c, hx_ + 6, hy_ + 4, -58.0, 2.6)                                                                    # tüy, elin üstünden yükselir
        if 0 < wd_ < 1:
            v = 900.0 * 1.6 / 0.6 / 24.0 * math.sin(math.pi * wd_)    # el çekilirken hız (yaklaşık; deklanşör ipucu)
    c.restore()
    if v > 0:
        _A.hint_speed(cx, v * zz)                                    # küçük hızlı nesne (el, kese, poliçe, anahtar): deklanşör (AN1-Y7)
    if scene == "kalem" and P.get("seal_at") is not None:       # mühür EKRAN uzayında (kabartma okunur: r=170)
        _P.seal_drop(P.get("seal_x", 1240), P.get("seal_y", 660), P["seal_at"], r=170, label=P.get("seal_label"), label_size=44, year=P.get("seal_year"),
                     variant=P.get("seal_variant"))(cx)
    CM.finish(f, cx, motes_n=14)


# ═════════════════════════════════════════════════════════════════════════════
# c2_defterler — KAPALI, CİLTLİ DEFTERLER (üç çeyrek eğik açı) + sandık: "1397'den o yıla kadar defterler yüz elli bini aşkın florin kâr gösterir"
# Kurul tur 3 (AN2-Ö1, PK2-N1): bölümde üstten tam açılım en çok iki (#72, #85); #88 artık üstten açık defter DEĞİL. Olgu disiplini: sırtlarda yalnız
# ilk ve son yıl (1397, 1420; aradaki sırtlar yazısız), defter adı / kişi adı / tutar YOK; "1397 – 1420" ilk deftere bağlı kâğıt etikette.
# Basit perspektif (iğne deliği kamera, aşağı bakış): yüzler yerel dikdörtgende çizilip ekran dörtgenine eşlenir (skia setPolyToPoly).
# ═════════════════════════════════════════════════════════════════════════════
DEF_BOOKS = (                                  # (kalınlık, yükseklik, deri rengi, sırt etiketi) — cm
    (12.0, 42.0, "#6A2E24", "1397"),
    (11.0, 40.5, "#4A3A24", None),
    (12.5, 43.0, "#2E4A3A", None),
    (11.5, 41.0, "#7A3424", None),
    (12.0, 42.5, "#5A3A24", None),
    (11.0, 40.0, "#3E2A1C", None),
    (12.5, 42.0, "#6E2A22", "1420"),
)
DEF_O = (-50.0, 0.0, 100.0)                     # ilk sırtın ön-sol-alt köşesi
DEF_TH = math.radians(22.0)                     # defter sırasının resim düzlemine açısı (sağa doğru uzaklaşır)
DEF_DEPTH = 30.0
DEF_F = 1500.0
DEF_PITCH = math.radians(15.0)
DEF_CHEST = (34.0, 94.0, 0.0, 34.0, 150.0, 188.0)   # x0, x1, y0, y1, z0, z1
_DEF_IMG = {}


class _Proj:
    """İğne deliği kamera: C = (X, Y, Z), aşağı bakış açısı DEF_PITCH. (X, Y, Z) → ekran (x, y)."""

    def __init__(self, X, Y, Z):
        self.C = (X, Y, Z)
        self.ca, self.sa = math.cos(DEF_PITCH), math.sin(DEF_PITCH)

    def __call__(self, X, Y, Z):
        dx, dy, dz = X - self.C[0], Y - self.C[1], Z - self.C[2]
        yp = dy * self.ca + dz * self.sa
        zp = max(1e-3, -dy * self.sa + dz * self.ca)
        return (960.0 + DEF_F * dx / zp, 540.0 - DEF_F * yp / zp)


def _face(c, quad, w, h, draw):
    """Yerel (0,0)–(w,h) dikdörtgeni ekran dörtgenine (sol üst, sağ üst, sağ alt, sol alt) eşlenir; draw(c) yerel koordinatta çizer."""
    m = skia.Matrix()
    if not m.setPolyToPoly([skia.Point(0, 0), skia.Point(w, 0), skia.Point(w, h), skia.Point(0, h)], [skia.Point(float(x), float(y)) for x, y in quad]):
        return
    c.save()
    c.concat(m)
    draw(c)
    c.restore()


def _def_bg():
    """Arka duvar (ofis: sıcak sıva, ceviz lambri, pencere ışığı, rafta bulanık defterler) — alan derinliği için bulanık, bir kez pişirilir."""
    img = _DEF_IMG.get("bg")
    if img is not None:
        return img
    fr = sk.Frame(2800, 1080)
    c = fr.c
    OD.GRAD_V(c, 0, 0, 2800, 1080, [("#D9C7A2", 0.0), ("#C8B08A", 0.55), ("#8E7254", 1.0)])
    fr.rrect(260, 70, 420, 470, 18, color="#FFF4D8", alpha=0.85)                 # pencere (sol üst)
    fr.rect(462, 70, 16, 470, color="#6A4E34", alpha=0.7)
    fr.rect(260, 290, 420, 14, color="#6A4E34", alpha=0.7)
    OD.GRAD_V(c, 0, 640, 2800, 1080, [("#5A3A22", 0.0), ("#3E2616", 1.0)])         # lambri
    for x in range(0, 2800, 230):
        c.drawLine(x, 650, x, 1080, OD.STK("#2A180C", 3.0, 120))
    rs = OD._RS(88)
    for row, yy in enumerate((250, 420)):                                           # rafta defterler (bulanık; yazısız)
        c.drawRect(skia.Rect.MakeLTRB(1650, yy + 4, 2600, yy + 20), OD.PT("#5A3A22"))
        x = 1670
        while x < 2580:
            w_ = rs.uniform(26, 44)
            h_ = rs.uniform(110, 150)
            c.drawRect(skia.Rect.MakeLTRB(x, yy - h_ + 4, x + w_, yy + 4), OD.PT(["#6A2E24", "#2E4A3A", "#5A3A24", "#7A5A34", "#3E2A1C"][int(rs.uniform(0, 4.99))]))
            x += w_ + rs.uniform(2, 6)
    img0 = fr.surf.makeImageSnapshot()
    fb = sk.Frame(2800, 1080)
    p = skia.Paint(ImageFilter=skia.ImageFilters.Blur(9.0, 9.0))
    fb.c.drawImage(img0, 0, 0, skia.SamplingOptions(), p)
    img = fb.surf.makeImageSnapshot()
    _DEF_IMG["bg"] = img
    return img


def _leather(c, w, h, col, light=1.0, seed=1):
    """Deri yüz (yerel w×h): yatay degrade (yuvarlak sırt hissi) + hafif leke dokusu."""
    cc = mix(col, "#FFFFFF", 0.10 * light) if light > 1 else mix(col, "#000000", 0.18 * (1 - light))
    c.drawRect(skia.Rect.MakeWH(w, h), OD.LGP((0, 0), (w, 0), [(mix(cc, "#000000", 0.30), 0.0), (mix(cc, "#FFFFFF", 0.10), 0.32),
                                                                                   (cc, 0.6), (mix(cc, "#000000", 0.35), 1.0)]))
    rs = _PN._RS(seed)
    for k in range(6):
        c.drawCircle(rs.uniform(0, w), rs.uniform(0, h), rs.uniform(w * 0.1, w * 0.3), OD.PT("#000000", int(rs.uniform(10, 26))))
    c.drawRect(skia.Rect.MakeWH(w, h), OD.STK(OD.INK, 2.4, 200))


def _spine(c, w, h, col, label, seed, la=1.0):
    """Sırt (yerel w×h, 10 px/cm): deri, beş kabartma şerit, yaldız filetolar; label varsa şerit arasında kâğıt etiket + mürekkeple yıl."""
    _leather(c, w, h, col, 0.95, seed)
    bands = [0.12, 0.30, 0.50, 0.70, 0.88]
    for b in bands:
        y = h * b
        c.drawRect(skia.Rect.MakeLTRB(0, y - 9, w, y + 9), OD.PT(mix(col, "#000000", 0.25)))
        c.drawLine(2, y - 8, w - 2, y - 8, OD.STK(mix(col, "#FFFFFF", 0.35), 2.0, 200))
        c.drawLine(2, y + 8, w - 2, y + 8, OD.STK("#000000", 2.0, 150))
        c.drawLine(4, y - 14, w - 4, y - 14, OD.STK("#C9A23A", 1.4, 170))
        c.drawLine(4, y + 14, w - 4, y + 14, OD.STK("#C9A23A", 1.4, 170))
    if label:
        lx0, lx1, ly0, ly1 = w * 0.10, w * 0.90, h * 0.36, h * 0.46
        c.drawRect(skia.Rect.MakeLTRB(lx0 + 3, ly0 + 4, lx1 + 3, ly1 + 4), OD.PT("#000000", 70))
        c.drawRect(skia.Rect.MakeLTRB(lx0, ly0, lx1, ly1), OD.LGP((0, ly0), (0, ly1), [("#F2E6C4", 0.0), ("#DCC99C", 1.0)]))
        c.drawRect(skia.Rect.MakeLTRB(lx0, ly0, lx1, ly1), OD.STK("#5A3E22", 1.6, 200))
        sz = CM.fit_size(label, "title_m", 36, (lx1 - lx0) - 10, 2.0)
        blob, _ = sk.text_blob("title_m", label, sz, 2.0)
        wd = sk.text_width(label, "title_m", sz, 2.0)
        if la > 0.003:                                                  # kadraj kenarında yarım kalırsa yazı söner (TE2-G1)
            c.drawTextBlob(blob, (lx0 + lx1) / 2 - wd / 2, (ly0 + ly1) / 2 + sz * 0.36, OD.PT(INK_C, int(255 * la)))


def _book_top(c, w, d, col):
    """Üst yüz (yerel w×d; y=0 arka/ön kenar sayfalar, y=d sırt): krem sayfa bloğu, iki yanda kapak tahtası (deri), önde sırt."""
    c.drawRect(skia.Rect.MakeWH(w, d), OD.PT("#E8DCB8"))
    for k in range(1, 9):
        x = w * k / 9.0
        c.drawLine(x, 6, x, d - 18, OD.STK("#B8A47A", 1.0, 120))
    c.drawRect(skia.Rect.MakeLTRB(0, 0, 9, d), OD.PT(mix(col, "#FFFFFF", 0.08)))
    c.drawRect(skia.Rect.MakeLTRB(w - 9, 0, w, d), OD.PT(mix(col, "#000000", 0.10)))
    c.drawRect(skia.Rect.MakeLTRB(0, d - 16, w, d), OD.PT(mix(col, "#FFFFFF", 0.05)))
    c.drawRect(skia.Rect.MakeWH(w, d), OD.STK(OD.INK, 2.0, 190))


def _book_cover(c, d, h, col):
    """İlk defterin ön kapağı (yerel d×h): deri, kör baskı çift çerçeve, köşe madenleri, kopça kayışı (yazı yok)."""
    _leather(c, d, h, col, 1.12, 77)
    for ins, a in ((26, 150), (44, 110)):
        c.drawRect(skia.Rect.MakeLTRB(ins, ins, d - ins, h - ins), OD.STK(mix(col, "#000000", 0.45), 2.4, a))
        c.drawRect(skia.Rect.MakeLTRB(ins + 3, ins + 3, d - ins + 3, h - ins + 3), OD.STK(mix(col, "#FFFFFF", 0.25), 1.2, a))
    for (x, y) in ((0, 0), (d, 0), (d, h), (0, h)):
        p = sk.poly_path([(x, y), (x + (36 if x == 0 else -36), y), (x, y + (36 if y == 0 else -36))])
        c.drawPath(p, OD.PT("#B8862E"))
        c.drawPath(p, OD.STK(OD.INK, 1.6, 200))
    c.drawRect(skia.Rect.MakeLTRB(0, h * 0.46, 70, h * 0.54), OD.PT(mix(col, "#000000", 0.30)))          # kopça kayışı ön kesimde (sırtın karşısı)
    c.drawRect(skia.Rect.MakeLTRB(0, h * 0.46, 70, h * 0.54), OD.STK(OD.INK, 1.4, 190))
    c.drawCircle(50, h * 0.50, 9, OD.PT("#C9A23A"))


def _chest_front(c, w, h):
    """Sandık önü (yerel w×h): ceviz tahta, demir kuşaklar ve çiviler, ortada kilit aynası."""
    OD.WOOD(c, 0, 0, w, h, OD.OTint("day"), col="#6E4524", seed=5, ink=2.0, grain=9)
    for x in (w * 0.08, w * 0.92):
        c.drawRect(skia.Rect.MakeLTRB(x - 16, 0, x + 16, h), OD.PT("#3A3430"))
        c.drawRect(skia.Rect.MakeLTRB(x - 16, 0, x + 16, h), OD.STK(OD.INK, 1.6, 200))
        for yy in range(24, int(h), 56):
            c.drawCircle(x, yy, 6, OD.PT("#8A8278"))
    c.drawRect(skia.Rect.MakeLTRB(0, h * 0.12 - 12, w, h * 0.12 + 12), OD.PT("#3A3430"))
    c.drawRect(skia.Rect.MakeLTRB(w / 2 - 50, h * 0.12, w / 2 + 50, h * 0.48), OD.PT("#B8862E"))
    c.drawRect(skia.Rect.MakeLTRB(w / 2 - 50, h * 0.12, w / 2 + 50, h * 0.48), OD.STK(OD.INK, 2.0, 210))
    c.drawCircle(w / 2, h * 0.28, 11, OD.PT("#1A0E06"))
    c.drawRect(skia.Rect.MakeLTRB(w / 2 - 5, h * 0.28, w / 2 + 5, h * 0.40), OD.PT("#1A0E06"))


def _chest_top(c, w, d):
    OD.WOOD(c, 0, 0, w, d, OD.OTint("day"), col="#7A5030", seed=9, ink=2.0, grain=7)
    for x in (w * 0.08, w * 0.92):
        c.drawRect(skia.Rect.MakeLTRB(x - 16, 0, x + 16, d), OD.PT("#3A3430"))
        c.drawRect(skia.Rect.MakeLTRB(x - 16, 0, x + 16, d), OD.STK(OD.INK, 1.4, 190))


def _chest_side(c, d, h):
    OD.WOOD(c, 0, 0, d, h, OD.OTint("day"), col="#5A3820", seed=7, ink=2.0, grain=6)
    c.drawRect(skia.Rect.MakeLTRB(0, h * 0.12 - 12, d, h * 0.12 + 12), OD.PT("#2E2824"))
    c.drawRect(skia.Rect.MakeWH(d, h), OD.STK(OD.INK, 2.0, 190))


@ckind("c2_defterler")
def k_defterler(cx, cams=None, tag_text="1397 – 1420", seed=5, **P):
    """KAPALI, CİLTLİ DEFTERLER — üç çeyrek eğik açı (üstten açık defter DEĞİL; kurul tur 3 AN2-Ö1, PK2-N1): masada sırtları görünen defter sırası
    (ilk sırtta 1397, son sırtta 1420; aradakiler yazısız), yanında demir kuşaklı sandık ve florin istifleri; ilk deftere bağlı kâğıt etikette
    '1397 – 1420' (mürekkep). Kamera: cams=[(çapa, (X, Y, Z))] kamera konumu (cm; aşağı bakış 15°), sağa kayıp sıranın sonuna yaklaşır.
    Sayaç (150.000+) ve 'DEFTERLER GÖSTERİR' sahne dosyasında ekran uzayı ovl."""
    f = cx.f
    c = f.c
    dur = max(cx.dur, 1e-3)
    X, Y, Z = _wcam(cx, cams or [(0.0, (-20.0, 60.0, 8.0))], dur, ends=_ends(cx))
    X += 0.25 * math.sin(cx.t * 0.9 + 1.3)                               # elde tutulan hafif salınım (cm)
    Y += 0.18 * math.sin(cx.t * 0.7)
    pj = _Proj(X, Y, Z)
    # arka duvar (bulanık; yatay paralaks yavaş)
    bg = _def_bg()
    bx = -420.0 - X * DEF_F / 360.0
    c.drawImageRect(bg, skia.Rect.MakeXYWH(bx, -10.0 - (Y - 60.0) * 2.0, 2800, 1100), skia.SamplingOptions(skia.FilterMode.kLinear))
    # masa (ceviz) — üst düzlem Y=0
    tq = [pj(-170, 0, 330), pj(260, 0, 330), pj(260, 0, 74), pj(-170, 0, 74)]
    f.path(sk.poly_path(tq), shader=f.lin(0, tq[0][1], 0, H, [("#5A3A22", 0.0), ("#7A5232", 0.45), ("#5E3C22", 1.0)]))
    for k in range(14):                                                  # tahta lifi (perspektif)
        zz = 80 + k * 18.5
        a_, b_ = pj(-170, 0, zz), pj(260, 0, zz)
        c.drawLine(a_[0], a_[1], b_[0], b_[1], OD.STK("#2A180C", 1.2, 40 + (k % 3) * 18))
    a_, b_ = pj(-170, 0, 330), pj(260, 0, 330)
    c.drawLine(a_[0], a_[1], b_[0], b_[1], OD.STK("#1E1008", 3.0, 200))
    # sandık (sağda, arkada): sol yan, üst, ön
    x0, x1, y0, y1, z0, z1 = DEF_CHEST
    f.path(sk.poly_path([pj(x0 - 4, 0, z0 - 6), pj(x1 + 10, 0, z0 - 6), pj(x1 + 14, 0, z1 + 8), pj(x0 - 8, 0, z1 + 8)]), color="#000000", alpha=0.30, blur=14)
    if X < x0:
        _face(c, [pj(x0, y1, z1), pj(x0, y1, z0), pj(x0, y0, z0), pj(x0, y0, z1)], (z1 - z0) * 10, (y1 - y0) * 10, lambda cc: _chest_side(cc, (z1 - z0) * 10, (y1 - y0) * 10))
    _face(c, [pj(x0, y1, z1), pj(x1, y1, z1), pj(x1, y1, z0), pj(x0, y1, z0)], (x1 - x0) * 10, (z1 - z0) * 10, lambda cc: _chest_top(cc, (x1 - x0) * 10, (z1 - z0) * 10))
    _face(c, [pj(x0, y1, z0), pj(x1, y1, z0), pj(x1, y0, z0), pj(x0, y0, z0)], (x1 - x0) * 10, (y1 - y0) * 10, lambda cc: _chest_front(cc, (x1 - x0) * 10, (y1 - y0) * 10))
    for (cxw, czw, n, sd) in ((48.0, y1, 15, 4), (64.0, y1, 10, 9), (80.0, y1, 12, 13)):   # sandık kapağında florin istifleri (kâr)
        sx_, sy_ = pj(cxw, czw, (z0 + z1) / 2 + (sd % 3) * 4 - 4)
        OD.draw_coins(c, sx_, sy_, n, 1.8, cx.t, seed=sd, glint=True)
    # defter sırası: uzaktan yakına (sağdan sola)
    ux, uz = math.cos(DEF_TH), math.sin(DEF_TH)
    vx, vz = -math.sin(DEF_TH), math.cos(DEF_TH)
    ox, oy, oz = DEF_O
    starts = []
    a = 0.0
    for (t_, h_, col, lab) in DEF_BOOKS:
        starts.append(a)
        a += t_ + 0.35
    sh = [pj(ox + vx * DEF_DEPTH - 2, 0, oz + vz * DEF_DEPTH + 4), pj(ox + ux * a + vx * DEF_DEPTH + 6, 0, oz + uz * a + vz * DEF_DEPTH + 6),
          pj(ox + ux * a + 8, 0, oz + uz * a - 2), pj(ox - 4, 0, oz - 3)]
    f.path(sk.poly_path(sh), color="#000000", alpha=0.34, blur=12)
    for i in range(len(DEF_BOOKS) - 1, -1, -1):
        t_, h_, col, lab = DEF_BOOKS[i]
        a0, a1 = starts[i], starts[i] + t_
        P0 = (ox + ux * a0, oz + uz * a0)
        P1 = (ox + ux * a1, oz + uz * a1)
        B0 = (P0[0] + vx * DEF_DEPTH, P0[1] + vz * DEF_DEPTH)
        B1 = (P1[0] + vx * DEF_DEPTH, P1[1] + vz * DEF_DEPTH)
        if Y > h_:
            _face(c, [pj(B0[0], h_, B0[1]), pj(B1[0], h_, B1[1]), pj(P1[0], h_, P1[1]), pj(P0[0], h_, P0[1])], t_ * 10, DEF_DEPTH * 10,
                  lambda cc, t_=t_, col=col: _book_top(cc, t_ * 10, DEF_DEPTH * 10, col))
        if i == 0:                                                       # ilk defterin ön kapağı (sola-öne bakar)
            _face(c, [pj(B0[0], h_, B0[1]), pj(P0[0], h_, P0[1]), pj(P0[0], 0, P0[1]), pj(B0[0], 0, B0[1])], DEF_DEPTH * 10, h_ * 10,
                  lambda cc, h_=h_, col=col: _book_cover(cc, DEF_DEPTH * 10, h_ * 10, col))
        q = [pj(P0[0], h_, P0[1]), pj(P1[0], h_, P1[1]), pj(P1[0], 0, P1[1]), pj(P0[0], 0, P0[1])]
        ke = 1.0
        if lab:                                                         # yalnız etiketin kendi kutusu (sırtın dibi kadrajdan taşsa da etiket sönmez)
            la0, la1 = a0 + 0.1 * t_, a0 + 0.9 * t_
            lq = [pj(ox + ux * la, yy_, oz + uz * la) for la in (la0, la1) for yy_ in (h_ * 0.54, h_ * 0.64)]
            ke = _edge_k(c, min(p[0] for p in lq), min(p[1] for p in lq), max(p[0] for p in lq), max(p[1] for p in lq), pad=40.0)
        _face(c, q, t_ * 10, h_ * 10, lambda cc, t_=t_, h_=h_, col=col, lab=lab, i=i, ke=ke: _spine(cc, t_ * 10, h_ * 10, col, lab, 50 + i, la=ke))
    # ortadaki deftere (4.) iple asılı kâğıt etiket (cartellino): '1397 – 1420' (öne bakar; kamera kayarken çekim boyunca kadrajda)
    am = starts[3] + DEF_BOOKS[3][0] / 2
    mx_, mz_ = ox + ux * am, oz + uz * am
    tx0, tx1, ty0, ty1, tz = mx_ - 12.5, mx_ + 12.5, 26.5, 35.0, mz_ - 6.0
    k0 = pj(mx_ + 1.5, DEF_BOOKS[3][1] - 0.5, mz_)
    kt = pj(mx_ + 2.0, ty1, tz)
    _hand_line(c, [k0, kt], col="#9A2A1E", w=3.0, seed=97, wob=0.4)
    q = [pj(tx0, ty1, tz), pj(tx1, ty1, tz), pj(tx1, ty0, tz), pj(tx0, ty0, tz)]
    ke = _edge_k(c, min(p[0] for p in q), min(p[1] for p in q), max(p[0] for p in q), max(p[1] for p in q))

    def _tag(cc, w=(tx1 - tx0) * 10, h=(ty1 - ty0) * 10):
        rs = _PN._RS(14)
        pts = [(0, 0)] + [(w * k / 12, rs.uniform(-3, 3)) for k in range(1, 12)] + [(w, 0), (w, h)] + [(w * k / 12, h + rs.uniform(-3, 3)) for k in range(11, 0, -1)] + [(0, h)]
        pth = sk.poly_path(pts)
        sh_ = skia.Path(pth)
        sh_.offset(6, 8)
        cc.drawPath(sh_, OD.PT("#000000", 70))
        cc.drawPath(pth, OD.LGP((0, 0), (0, h), [("#F6EDD0", 0.0), ("#E2D2A2", 1.0)]))
        cc.drawPath(pth, OD.STK("#6A4E2E", 2.0, 210))
        cc.drawCircle(w / 2 + 20, 14, 6, OD.STK("#6A4E2E", 2.0, 200))
        if ke > 0.003:
            sz = CM.fit_size(tag_text, "title", 52, w - 40, 3.0)
            blob, _ = sk.text_blob("title", tag_text, sz, 3.0)
            wd = sk.text_width(tag_text, "title", sz, 3.0)
            cc.drawTextBlob(blob, w / 2 - wd / 2, h / 2 + sz * 0.42, OD.PT(INK_R, int(255 * ke)))
    _face(c, q, (tx1 - tx0) * 10, (ty1 - ty0) * 10, _tag)
    # pencere ışığı (soldan, sıcak) + finish
    f.circle(-80, 120, 1100, shader=f.rad(-80, 120, 1100, [("#FFE6B0", 0.0, 70), ("#FFE6B0", 1.0, 0)]), blend=skia.BlendMode.kScreen)
    CM.finish(f, cx, motes_n=18)


cilt_cam.OWN_CAMERA.update({"c2_masa", "c2_yakin", "c2_defterler"})
import anim as _A  # noqa: E402


import p1_ortak as _P2  # noqa: E402
_P2.add_ovl(["c2_nolist", "c2_hediye", "c2_kasa", "c2_borc", "c2_ayrim", "c2_mezar", "c2_rivayet", "c2_katasto", "c2_yil", "c2_kalemler", "c2_sadaka", "c2_masa", "c2_yakin", "c2_defterler"])


def kasa_cubuk(x0, y, w, start_at, a_at, b_at, n_a=22, n_b=18, start_label="1422", out=None):
    """Papalık kasa memurluğu (kurul teyit c2s21, DBI): düz yaldız şerit = n_a yıl KESİNTİSİZ, ardından kesikli şerit = n_b yıl ARALIKLI.
    Yalnız başlangıç yılı yazılır (bitiş yılı iddiası yok). Ekran uzayı; yazılar ≥38 px, koyu zemin üstünde."""
    def fn(cx):
        f = cx.f
        k0 = cx.amt(start_at, 0.5)
        if out is not None:
            k0 *= 1.0 - cx.amt(out, 0.4)
        if k0 <= 0.003:
            return
        tot = float(n_a + n_b)
        wa, wb = w * n_a / tot, w * n_b / tot
        hb = 46.0
        f.rrect(x0 - 110, y - 190, w + 150, 380, 18, color="#120C08", alpha=0.70 * k0)
        f.rrect(x0 - 110, y - 190, w + 150, 380, 18, style="stroke", sw=2.0, color="#C9A45A", alpha=0.7 * k0)
        f.line(x0, y + hb / 2 + 10, x0 + w * k0, y + hb / 2 + 10, color="#E8D4A0", sw=2.0, alpha=0.55 * k0)
        # başlangıç çentiği + yıl
        f.line(x0, y - hb / 2 - 18, x0, y + hb / 2 + 22, color="#F6D886", sw=4.0, alpha=k0)
        CM.ink(f, start_label, x0, y + hb / 2 + 76, face="title", size=46, color="#F6D886", align="c", track=6, alpha=k0, emboss=False)
        # düz şerit (kesintisiz)
        ta = cx.at(a_at)
        ua = ease_io(clamp((cx.t - ta) / 1.0), 1.8)
        if ua > 0.002:
            f.rrect(x0, y - hb / 2, wa * ua, hb, 8, shader=f.lin(0, y - hb / 2, 0, y + hb / 2, [("#F6D886", 0.0), ("#B8862E", 1.0)]), alpha=k0)
            ka = clamp((cx.t - ta - 0.2) / 0.4) * k0
            n = int(round(n_a * ua))
            CM.ink(f, f"{n} YIL", x0 + wa / 2, y - hb / 2 - 26, face="title", size=56, color="#FFF4D6", align="c", track=6, alpha=ka, emboss=False)
            CM.ink(f, "KESİNTİSİZ", x0 + wa / 2, y + hb / 2 + 76, face="title_m", size=38, color="#FFF4D6", align="c", track=6, alpha=clamp((cx.t - ta - 0.7) / 0.4) * k0, emboss=False)
        # kesikli şerit (aralıklı)
        tb = cx.at(b_at)
        ub = ease_io(clamp((cx.t - tb) / 1.0), 1.8)
        if ub > 0.002:
            xb = x0 + wa
            nseg = 7
            sw_ = wb / nseg
            for i in range(nseg):
                s0 = xb + i * sw_ + 6
                s1 = s0 + sw_ * 0.62
                lim = xb + wb * ub
                if s0 >= lim:
                    break
                f.rrect(s0, y - hb / 2 + 6, min(s1, lim) - s0, hb - 12, 6, color="#D8B25A", alpha=0.9 * k0)
            kb = clamp((cx.t - tb - 0.2) / 0.4) * k0
            CM.ink(f, "+", xb, y - hb / 2 - 30, face="title", size=56, color="#F6D886", align="c", alpha=kb, emboss=False)
            n = int(round(n_b * ub))
            CM.ink(f, f"{n} YIL", xb + wb / 2 + 10, y - hb / 2 - 26, face="title", size=56, color="#FFF4D6", align="c", track=6, alpha=kb, emboss=False)
            CM.ink(f, "ARALIKLI", xb + wb / 2 + 10, y + hb / 2 + 76, face="title_m", size=38, color="#FFF4D6", align="c", track=6, alpha=clamp((cx.t - tb - 0.7) / 0.4) * k0, emboss=False)
    return fn
