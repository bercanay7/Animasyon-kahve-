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
import cilt_props as CP
import icons
import sk
from cilt_medici import TH, ckind
from sk import H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth

import c0_kinds as K0
import c1_kinds as K1
import p1_ortak as _P

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
def k_nolist(cx, borc_at=None, borc_x=None, faiz_at=None, faiz_x=None, kur_at=None, seed=2, **_):
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
        c.save(); c.translate(x, y); c.scale(sc, sc); c.translate(-x, -y)
        CM.tablet(f, x - w / 2, y - h / 2, w, h, alpha=k, corner=14, fill=("#F2E5BC", "#DCC58C") if ok else None)
        sp = CM.engraved(txt, "title", int(CM.fit_size(txt, "title", 92, w - 70, 8)), 8.0, "#7A5410" if ok else TH.fg)
        CM.draw_spr(f, sp, x, y + 32, "c", alpha=k)
        if ok:
            f.circle(x, y, 360, shader=f.rad(x, y, 360, [("#F0D27A", 0.0, int(90 * k)), ("#F0D27A", 1.0, 0)]))
        c.restore()
    # çarpılar (BORÇ ve FAİZ) — "yok" sözcüklerinde
    for x, ca in ((300, borc_x), (860, faiz_x)):
        kx = cx.amt(ca, 0.32) if ca is not None else 0.0
        if kx > 0.003:
            p1 = clamp(kx * 2.0)
            p2 = clamp(kx * 2.0 - 1.0)
            y = 470
            R = 130
            f.line(x - R, y - R * 0.55, x - R + 2 * R * p1, y - R * 0.55 + 1.1 * R * p1, color="#A8201A", sw=18, alpha=0.95)
            if p2 > 0:
                f.line(x + R, y - R * 0.55, x + R - 2 * R * p2, y - R * 0.55 + 1.1 * R * p2, color="#A8201A", sw=18, alpha=0.95)
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
    f = cx.f
    c = f.c
    cam = _bg(f, cx, seed)
    x0, gy = 960, 780
    kb = cx.amt(tag_at if tag_at is not None else 0.0, 0.45)
    ko = ease_out(clamp((cx.t - cx.at(open_at)) / 0.5), 2) if open_at is not None else 0.0
    bob = 8 * math.sin(cx.t * 3.0)
    w, h = 400, 280
    # gölge
    f.oval(x0 + 10, gy + 4, 250, 36, color="#000000", alpha=0.3, blur=8)
    # kutu gövdesi
    f.rect(x0 - w / 2, gy - h, w, h, shader=f.lin(x0 - w / 2, 0, x0 + w / 2, 0, [("#A8321E", 0.0), ("#C8452A", 0.5), ("#8E2A1A", 1.0)]))
    f.rect(x0 - w / 2, gy - h, w, h, style="stroke", sw=4, color="#3A1008", alpha=0.85)
    f.rect(x0 - 34, gy - h, 68, h, color="#E8C468")
    # kapak (açılışta yukarı kalkar)
    lid_y = gy - h - 70 - 150 * ko
    rot = -22 * ko
    c.save(); c.translate(x0 - w / 2 - 20, lid_y + 70); c.rotate(rot); c.translate(-(x0 - w / 2 - 20), -(lid_y + 70))
    f.rect(x0 - w / 2 - 20, lid_y, w + 40, 70, shader=f.lin(0, lid_y, 0, lid_y + 70, [("#D8552E", 0.0), ("#A8321E", 1.0)]))
    f.rect(x0 - w / 2 - 20, lid_y, w + 40, 70, style="stroke", sw=4, color="#3A1008", alpha=0.85)
    f.rect(x0 - 34, lid_y, 68, 70, color="#F0D27A")
    # fiyonk
    for sg in (-1, 1):
        bw = skia.Path(); bw.moveTo(x0, lid_y); bw.cubicTo(x0 + sg * 40, lid_y - 100, x0 + sg * 160, lid_y - 70, x0 + sg * 110, lid_y + 6); bw.close()
        c.drawPath(bw, f.paint("#F0D27A")); c.drawPath(bw, f.paint("#7A5410", style="stroke", sw=3, alpha=0.8))
    f.circle(x0, lid_y - 4, 24, color="#E8C468")
    c.restore()
    # içinden florinler fışkırır
    if ko > 0.2:
        for i in range(16):
            ph = ((cx.t - cx.at(open_at)) * 0.9 + i * 0.137) % 1.0
            xx = x0 + 150 * math.sin(i * 2.4) * ph
            yy = gy - h - 40 - 420 * ph + 520 * ph * ph * 0.0
            CP.draw_coin(f, xx, yy, 70 * (0.7 + 0.3 * ((i % 3) / 2)), spin=cx.t * 9 + i, alpha=min(1.0, ko) * (1 - ph) * 0.95, shadow=0.0)
    # etiket: FAİZ (çizilir) → HEDİYE
    if kb > 0.003:
        ty = gy - h / 2 + bob
        CM.tablet(f, x0 + 250, ty - 150, 330, 120, alpha=kb, rot=0.12, corner=8)
        CM.ink(f, "FAİZ", x0 + 415, ty - 76 + 6, face="title", size=64, color=TH.fg, align="c", track=8, alpha=kb, emboss=False)
        ks = cx.amt(strike_at, 0.3) if strike_at is not None else 0.0
        if ks > 0.003:
            f.line(x0 + 280, ty - 112 + 40 * (1 - ks) * 0, x0 + 280 + 270 * ks, ty - 82, color="#A8201A", sw=10, alpha=0.95)
    kg = cx.amt(gift_at, 0.35) if gift_at is not None else 0.0
    if kg > 0.003:
        sp = _gilt_or_ink("HEDİYE", "title", 140, 12.0)
        CM.draw_spr(f, sp, 960, 150, "c", alpha=kg, scale=0.7 + 0.3 * sk.back_out(kg), shadow=0.5 if not TH.day else 0.0, glow=0.25 * kg if not TH.day else 0.0)
    cam.end(f)
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
        x, y = 470, 520
        CM.tablet(f, x - 230, y - 120, 460, 240, alpha=kn, corner=12)
        icons.draw_icon(f, "coinbag", x, y - 20, size=160, metal="gold", alpha=kn * 0.8, glow=0.0)
        CM.ink(f, "AYRI SERMAYE", x, y + 98, face="title_m", size=32, color=TH.fg, align="c", track=7, alpha=kn, emboss=False)
        kx = cx.amt(nocap_at, 0.32, off=0.35)
        if kx > 0.003:
            for sg in (1, -1):
                f.line(x - 150 * kx, y - 120 * sg * kx, x + 150 * kx, y + 120 * sg * kx, color="#A8201A", sw=18, alpha=0.95)
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
        CM.name_plate(f, "GIOVANNI", "BORÇ VEREN", None, cx_=500, y=720, t=kg, w=500)
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
            CM.name_plate(f, "XXIII. JOHANNES", "PAPA", None, cx_=1690, y=520, t=kp * (1 - kf), w=470)
    # Konstanz: konsil levhası + tokmak
    kk = cx.amt(council_at, 0.5) if council_at is not None else 0.0
    if kk > 0.003:
        CM.tablet(f, 160, 50, 800, 110, alpha=kk, corner=10)
        CM.ink(f, "KONSTANZ KONSİLİ · 1415", 560, 125, face="title_m", size=46, color=TH.fg, align="c", track=8, alpha=kk, emboss=False)
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
        CM.stamp(f, "KAYNAKLAR AYRIŞIYOR", 960, 130 + 20, rot=-0.04, size=56, t=ks)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# c2_mezar — Vaftizhane'deki mezar: yazıt oyulur; itiraz damgası; yazıt kalır
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c2_mezar")
def k_mezar(cx, place_at=None, carve_at=None, carve_to=None, protest_at=None, stay_at=None, seed=2, **_):
    f = cx.f
    c = f.c
    cam = _bg(f, cx, seed, dress="top")
    gx, gy = 960, 900
    # mekân: kemerli taş niş + sarkofaj + yazıt levhası
    f.rect(260, 250, 1400, gy - 250, shader=f.lin(0, 250, 0, gy, [("#B9AA86", 0.0), ("#9C8C68", 1.0)]))
    arch = skia.Path(); arch.moveTo(420, gy - 70); arch.lineTo(420, 560); arch.arcTo(skia.Rect.MakeLTRB(420, 280, 1500, 840), 180, 180, False); arch.lineTo(1500, gy - 70); arch.close()
    c.drawPath(arch, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 280), (0, gy)], [sk.C("#3A2E22"), sk.C("#5A4A38")], [0, 1])))
    c.drawPath(arch, f.paint("#E3D3AC", style="stroke", sw=16))
    c.drawPath(arch, f.paint("#2A1A0C", style="stroke", sw=3, alpha=0.8))
    # sarkofaj
    f.rect(560, 640, 800, 190, shader=f.lin(0, 640, 0, 830, [("#D8CBA6", 0.0), ("#A89A74", 1.0)]))
    f.rect(540, 610, 840, 44, color="#E8DCB8")
    f.rect(560, 640, 800, 190, style="stroke", sw=3, color="#3A2A18", alpha=0.8)
    f.rect(540, 610, 840, 44, style="stroke", sw=3, color="#3A2A18", alpha=0.8)
    # yazıt levhası
    px, py, pw, ph = 700, 700, 520, 90
    f.rect(px, py, pw, ph, color="#7A6A4C", alpha=0.9)
    f.rect(px, py, pw, ph, style="stroke", sw=3, color="#2A1A0C", alpha=0.9)
    # yazıt: harf harf oyulur (altın yaprak)
    txt = "ESKİ PAPA"
    ta = cx.at(carve_at) if carve_at is not None else 0.0
    tb = cx.at(carve_to) if carve_to is not None else ta + 1.2
    p = clamp((cx.t - ta) / max(0.3, tb - ta))
    n = len(txt)
    sz = 62
    wid = sk.text_width(txt, "title", sz, 8)
    xs = 960 - wid / 2
    pos = xs
    for i, ch in enumerate(txt):
        wch = sk.text_width(ch, "title", sz, 8)
        ki = clamp(p * (n + 2) - i)
        if ki > 0 and ch != " ":
            sp = CM.gilt(ch, "title", sz, 0.0)
            CM.draw_spr(f, sp, pos + wch / 2, py + 66, "c", alpha=ki, scale=0.8 + 0.2 * ki, shadow=0.4)
        pos += wch
    # parıltı süpürmesi
    gl = ((cx.t - ta - 1.0) * 0.5) % 2.2
    if cx.t > ta + 1.0 and gl < 1.0:
        gxp = px + pw * gl
        f.rect(gxp - 20, py, 40, ph, shader=f.lin(gxp - 20, 0, gxp + 20, 0, [("#FFF4C0", 0.0, 0), ("#FFF4C0", 0.5, 160), ("#FFF4C0", 1.0, 0)]))
    # mum ışığı (yaşayan ortam): iki yanda mum, tozlu ışık
    for cxx, sd in ((470, 3.1), (1450, 5.2)):
        OD.candle(f, cxx, 840, 130, cx.t, sd, lit=1.0, holder=True)
    # etiket: Vaftizhane + Cossa
    kpl = cx.amt(place_at, 0.6) if place_at is not None else 1.0
    if kpl > 0.003:
        CM.name_plate(f, "VAFTİZHANE", "COSSA'NIN MEZARI", None, cx_=960, y=100, t=kpl, w=640)
    # itiraz damgası + mühür (Martinus)
    kpr = cx.amt(protest_at, 0.3) if protest_at is not None else 0.0
    if kpr > 0.003:
        CM.wax_seal(f, 1500, 330, 70, "#7A1A14", alpha=1.0, t=kpr, palle=False)
        icons.draw_icon(f, "keys", 1500, 330, size=70, metal="gold", alpha=kpr, glow=0.0, shadow=False)
        CM.ink(f, "V. MARTINUS", 1500, 440, face="title_m", size=30, color=TH.fg, align="c", track=8, alpha=kpr, emboss=False)
        CM.stamp(f, "İTİRAZ", 1280, 560, rot=-0.12, size=72, t=kpr)
    ks = cx.amt(stay_at, 0.8) if stay_at is not None else 0.0
    if ks > 0.003:
        gg = (cx.t * 0.7) % 1.6
        if gg < 1.0:
            a = math.sin(gg * math.pi)
            R = 110
            f.circle(960, py + 48, R * (0.6 + 0.7 * gg), shader=f.rad(960, py + 48, R * 1.4, [("#FFF1B8", 0.0, int(120 * a * ks)), ("#FFF1B8", 1.0, 0)]))
    cam.end(f)
    CM.finish(f, cx, motes_n=24)



# ─────────────────────────────────────────────────────────────────────────────
# yardımcı: mitra simgesi
# ─────────────────────────────────────────────────────────────────────────────
@icons.icon("c2_mitra")
def _i_mitra(m):
    m.smooth([(120, 440), (140, 200), (256, 70), (372, 200), (392, 440)], close=True, t=0.25)
    m.rect(104, 410, 304, 54, r=12)
    m.cut(sk.poly_path([(256, 112), (256, 410)], False), 8)
    m.cut(sk.poly_path([(168, 330), (256, 250), (344, 330)], False), 7)
    m.cut(sk.poly_path([(256, 130), (200, 190), (256, 250), (312, 190), (256, 130)], False), 5)
    m.circle(256, 80, 24)


@icons.icon("c2_bulla")
def _i_bulla(m):
    m.rect(120, 90, 272, 330, r=18)
    for i in range(7):
        m.cut(sk.poly_path([(160, 150 + i * 36), (352, 150 + i * 36)], False), 6)
    m.circle(256, 440, 52)
    m.cut(sk.poly_path([(256, 418), (256, 462)], False), 6)


# ─────────────────────────────────────────────────────────────────────────────
# c2_rivayet — mitra borca karşılık bırakılır; Martinus aforozla tehdit eder (ANEKDOT)
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c2_rivayet")
def k_rivayet(cx, src_at=None, med_at=None, pawn_at=None, ask_at=None, threat_at=None, seed=4, **_):
    f = cx.f
    c = f.c
    cam = _bg(f, cx, seed)
    # kaynak: Treccani levhası + ANEKDOT damgası
    ks = cx.amt(src_at, 0.6) if src_at is not None else 0.0
    if ks > 0.003:
        CM.name_plate(f, "TRECCANI", "GIOVANNI MADDESİNDE", None, cx_=520, y=95, t=ks, w=620)
        CM.stamp(f, "ANEKDOT", 1130, 175, rot=-0.07, size=60, t=cx.amt(src_at, 0.3, off=0.6))
    # sol: Giovanni madalyası, orta: mitra (yastıkta, "BORÇ" etiketi), sağ: Martinus siluet
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
        CM.tablet(f, mx - 120, my + 160, 240, 74, alpha=kp, rot=-0.04, corner=8)
        CM.ink(f, "BORÇ", mx, my + 212, face="title_m", size=40, color=TH.fg, align="c", track=10, alpha=kp, emboss=False)
    # Martinus: siluet, sağ elini uzatır (işaret)
    kq = cx.amt(ask_at, 0.6) if ask_at is not None else 0.0
    if kq > 0.003:
        OD.sil_actor(f, "papa", 1520, 880, 430, cx.t, action="point", dir=-1, seed=9, color="#1A1210", rim="#E8B070", rim_dir=-1, alpha=kq)
        CM.name_plate(f, "V. MARTINUS", "PAPA", None, cx_=1520, y=250, t=kq, w=520)
    # geri alma: mitra Martinus'a doğru kayar (talep), sonra aforoz tehdidi: mühürlü ferman Giovanni'ye iner
    kt = cx.amt(threat_at, 0.5) if threat_at is not None else 0.0
    if kt > 0.003:
        u = ease_io(clamp((cx.t - cx.at(threat_at)) / 1.3), 1.7)
        bx = lerp(1350, 560, u)
        by = lerp(380, 400, u) - 140 * math.sin(math.pi * u)
        icons.draw_icon(f, "c2_bulla", bx, by, size=220 * (0.7 + 0.3 * kt), metal="gold", alpha=kt, rot=-0.18 + 0.4 * u, glow=0.0)
        CM.stamp(f, "AFOROZ TEHDİDİ", 900, 250, rot=-0.06, size=56, t=cx.amt(threat_at, 0.3, off=0.5))
    cam.end(f)
    CM.finish(f, cx, motes_n=24)


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
        CM.ink(f, "KATASTO · 1427", 960, 180, face="title", size=64, color=TH.fg, align="c", track=16, alpha=kt, emboss=False)
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
def k_kalemler(cx, left_at=None, right_at=None, q_at=None, stamp_at=None, write_a=None, write_b=None, seed=5, **_):
    f = cx.f
    c = f.c
    cam = _bg(f, cx, seed)
    for (x, name, role, at, wa, sd) in ((520, "MACHIAVELLİ", "BİR ASIR SONRA", left_at, write_a, 11), (1400, "CAVALCANTI", "1440'LARDA", right_at, write_b, 17)):
        k = cx.amt(at, 0.6) if at is not None else 1.0
        if k <= 0.003:
            continue
        pw, ph, py = 620, 560, 300
        yy = py + (1 - k) * 40
        f.rrect(x - pw / 2 + 8, yy + 12, pw, ph, 10, color="#000000", alpha=0.28 * k, blur=10)
        f.rrect(x - pw / 2, yy, pw, ph, 8, shader=f.lin(0, yy, 0, yy + ph, [("#F3E9C9", 0.0), ("#E3D4A6", 1.0)]), alpha=k)
        f.rrect(x - pw / 2, yy, pw, ph, 8, style="stroke", sw=3, color="#5A3E22", alpha=0.85 * k)
        CM.name_plate(f, name, role, None, cx_=x, y=110, t=k, w=560)
        # satırlar (kalem yazar)
        ta = cx.at(wa) if wa is not None else 1e9
        pr = clamp((cx.t - ta) / 3.0)
        nl = 8
        for i in range(nl):
            kl = clamp(pr * nl - i)
            if kl <= 0:
                continue
            ly = yy + 80 + i * 56
            wlen = (pw - 120) * (0.92 if i % 3 else 0.7) * ease_io(kl, 1.4)
            pth = skia.Path(); pth.moveTo(x - pw / 2 + 60, ly)
            n = max(2, int(wlen / 14))
            for q in range(1, n + 1):
                pth.lineTo(x - pw / 2 + 60 + q * wlen / n, ly + 6 * math.sin(q * 1.9 + i + sd))
            c.drawPath(pth, f.paint("#2E1C0C", style="stroke", sw=3.2, alpha=0.85 * k))
        if 0 < pr < 1:
            i = min(nl - 1, int(pr * nl))
            kl = clamp(pr * nl - i)
            ly = yy + 80 + i * 56
            wlen = (pw - 120) * (0.92 if i % 3 else 0.7) * ease_io(kl, 1.4)
            OD.quill(c, x - pw / 2 + 60 + wlen + 6, ly + 6, -58.0, 0.85)
    kq = cx.amt(q_at, 0.5) if q_at is not None else 0.0
    if kq > 0.003:
        f.circle(960, 560, 220, shader=f.rad(960, 560, 220, [("#F0D27A", 0.0, int(90 * kq)), ("#F0D27A", 1.0, 0)]))
        icons.draw_icon(f, "question", 960, 560, size=300 * (0.8 + 0.2 * sk.back_out(kq)), metal="gold", alpha=kq, rot=0.08 * math.sin(cx.t * 3.0), glow=0.0)
    ks = cx.amt(stamp_at, 0.3) if stamp_at is not None else 0.0
    if ks > 0.003:
        CM.stamp(f, "ANEKDOT", 960, 880, rot=-0.05, size=60, t=ks)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# c2_sadaka — yoksulun ihtiyacını kimse istemeden gideren biri (Machiavelli'nin çizdiği)
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c2_sadaka")
def k_sadaka(cx, who_at=None, give_at=None, stamp_at=None, seed=4, **_):
    f = cx.f
    c = f.c
    cam = _bg(f, cx, seed, dress="both")
    gy = 900
    f.rect(-100, gy, W + 200, 300, shader=f.lin(0, gy, 0, gy + 200, [("#8A6038", 0.0), ("#563820", 1.0)]))
    for i in range(-2, 16):
        c.drawLine(i * 140, gy, i * 140 - 70, gy + 200, f.paint("#3A2410", style="stroke", sw=2.5, alpha=0.5))
    # sol: verici (zengin tüccar; yüz yok — kit figürü, üslup)
    FA.actor(f, "tuccar", 520, gy + 20, 540, cx.t, action="idle", dir=1, seed=21, prop="sack")
    # sağ: üç yoksul; sırayla "bow" (teşekkür)
    t0 = cx.at(give_at) if give_at is not None else 0.0
    xs = (1150, 1420, 1690)
    for i, x in enumerate(xs):
        FA.actor(f, "halk", x, gy + 16 - i * 4, 470, cx.t, action="bow", dir=-1, seed=31 + i, phase=0.2 * i, t0=t0 + 0.55 + 0.9 * i + 0.5, dur=1.3, depth=18.0,
                 stil=dict(robe="#7A6A58", robe2="#9A8A72") if False else {})
    # florin yayları: tüccar → her yoksul, kimse istemeden (yoksulun eli boş)
    for i, x in enumerate(xs):
        for rep in range(2):
            u = (cx.t - (t0 + 0.55 + 0.9 * i + rep * 2.7)) / 0.9
            if cx.t < t0 or not (0 < u < 1):
                continue
            e = ease_io(u, 1.5)
            px = lerp(700, x - 30, e)
            py = lerp(520, 520, e) - 150 * math.sin(math.pi * e)
            CP.draw_coin(f, px, py, 68, spin=cx.t * 12 + i, alpha=min(1, u * 6) * min(1, (1 - u) * 6 + 0.1), shadow=0.2)
    kw = cx.amt(who_at, 0.6) if who_at is not None else 0.0
    if kw > 0.003:
        CM.name_plate(f, "MACHIAVELLİ'NİN ÇİZDİĞİ", "KİMSE İSTEMEDEN DE", None, cx_=960, y=100, t=kw, w=860)
    ks = cx.amt(stamp_at, 0.3) if stamp_at is not None else 0.0
    if ks > 0.003:
        CM.stamp(f, "ANEKDOT", 1560, 300, rot=-0.07, size=60, t=ks)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


import p1_ortak as _P2  # noqa: E402
_P2.add_ovl(["c2_nolist", "c2_hediye", "c2_kasa", "c2_borc", "c2_ayrim", "c2_mezar", "c2_rivayet", "c2_katasto", "c2_yil", "c2_kalemler", "c2_sadaka"])
