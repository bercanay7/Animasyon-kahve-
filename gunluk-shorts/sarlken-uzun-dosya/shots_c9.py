"""Bölüm 9 (Yeni Dünya) özel çekim türleri ve yardımcıları. Ad öntekleri: c9_ / wd_ (d_common)."""
import math

import skia

import d_common as D
import icons
import shots as SH
import sk
from d_common import A, icn, tag, draw_medal_plain, cameo, glow_dot, kick_rule, reveal_text, ring_pulse, shield_path, ingot, draw_globe
from sk import W, H, C, back_out, clamp, ease_io, ease_out, lerp, mix, smooth


# ───────────────────────────── dünya turu verisi (c9s12 + c13s6 ortak) ─────────────────────────────
# Mercator tek kopya harita: Pasifik geçişi antimeridyende ikiye bölünür (sol kenardan çıkar, sağ kenardan girer).
CIRC_A = [(-6.35, 36.78), (-14.5, 31.5), (-25, 15), (-33, 3), (-39, -9), (-44, -23), (-57, -36), (-68, -49.5), (-72, -53), (-84, -48), (-110, -30), (-140, -12), (-165, 3), (-179, 9)]
CIRC_B = [(179, 10), (144.7, 13.4), (125, 11), (127.4, 0.8), (124, -9.5), (100, -20), (70, -31), (40, -36), (18.5, -35), (0, -26), (-17, -4), (-24, 14), (-14, 30), (-6.35, 36.78)]


def circum_extra(t_a, dur_a=2.5, dur_b=2.6, gap=0.0, color="#F0D27A", width=6, ship=True, flag_at=None, labels=True):
    """Dünya turu rotası çizen `map` extra'sı üretir. t_a: yerel sn başlangıç (çapa/float)."""
    def extra(cx, cam, mv):
        f = cx.f
        ta = cx.at(t_a)
        ka = ease_io(clamp((cx.t - ta) / dur_a))
        kb = ease_io(clamp((cx.t - (ta + dur_a + gap)) / dur_b))
        if ka > 0:
            mv.route(f, cam, CIRC_A, prog=ka, color=color, width=width, arrow=False)
        if kb > 0:
            mv.route(f, cam, CIRC_B, prog=kb, color=color, width=width, arrow=(kb < 1))
        if ship:
            for pts, k in ((CIRC_A, ka), (CIRC_B, kb)):
                if 0 < k < 1:
                    (x, y), ang = mv.point_on(cam, pts, k)
                    icons.draw_icon(f, "ship", x, y - 30, size=74, metal="gold", glow=0.35)
        if labels:
            for txt, lon, lat in (("ATLANTİK", -34, 18), ("PASİFİK", -136, -22), ("HİNT OKYANUSU", 78, -14)):
                x, y = cam.ll(lon, lat)
                f.text(txt, x, y, face="map_i", size=30, color="#8FA9BA", align="c", track=10, alpha=0.75 * smooth((cx.t - ta) / 0.8), shadow=(2, 2, 3, "#000000"))
        if flag_at is not None:
            kf = cx.amt(flag_at, 0.6)
            if kf > 0:
                x, y = cam.ll(-6.35, 36.78)
                icons.draw_icon(f, icn("flag", "shield"), x + 6, y - 66, size=100 * (0.8 + 0.2 * back_out(kf)), metal="crimson", alpha=kf, glow=0.35)
    return extra


# ───────────────────────────── c9s1: Atlantik, "hiç görmedi" ─────────────────────────────
def open_extra(cx, cam, mv):
    f = cx.f
    t_hic = cx.at(A("c9s1", "hiç"))
    t_ama = cx.at(A("c9s1", "Ama"))
    k = clamp((cx.t - t_hic) / 2.6)
    fade = 1 - smooth((cx.t - t_ama) / 0.5)
    if k > 0 and fade > 0:
        mv.route(f, cam, [(-6, 38), (-22, 35.5), (-42, 30), (-60, 25), (-78, 21)], prog=0.5 * ease_io(k), color="#D8C58E", width=4.5, dash=(12, 12), arrow=False, alpha=0.9 * fade, dash_phase=-cx.t * 30)
    cameo(f, cx, "karl_olgun", 1650, 380, 300, A("c9s1", "Şarlken", 0.0), metal="gold", name="ŞARLKEN", role="İmparator", i=0)
    kk = cx.amt(A("c9s1", "hiç", -0.1), 0.6)
    if kk > 0:
        tag(f, "HİÇ GÖRMEDİ", W * 0.5, 150, kk, size=40, align="c", accent="#C0392B", track=10)


# ───────────────────────────── c9s2: Cortés rotası ─────────────────────────────
def cortes_extra(cx, cam, mv):
    f = cx.f
    cameo(f, cx, "kortes", 1560, 560, 300, A("c9s2", "Hernán", -0.2), metal="bronze", name="HERNÁN CORTÉS", role="Konkistador", i=1, plate_dy=170)
    # "izni olmadan" vurgusu: Küba üzerinde kırmızı yasak halkası
    kk = cx.amt(A("c9s2", "izni", -0.1), 0.5)
    if kk > 0:
        x, y = cam.ll(-79.5, 21.8)
        ring_pulse(f, x, y, cx.at(A("c9s2", "izni", -0.1)), cx.t, r0=18, r1=130, dur=1.6, color="#E0503C", sw=4, a=0.9)
        f.circle(x, y, 26 * kk, style="stroke", sw=4, color="#E0503C", alpha=0.85)
        f.line(x - 18 * kk, y + 18 * kk, x + 18 * kk, y - 18 * kk, color="#E0503C", sw=4, alpha=0.85)


# ───────────────────────────── c9s2b: Tenochtitlan kaplaması ─────────────────────────────
def tenoch_overlay(cx):
    f = cx.f
    k = cx.amt(A("c9s2", "13", -0.15), 0.7)
    if k > 0:
        f.rect(0, H - 330, W, 330, shader=f.lin(0, H - 330, 0, H, [("#000000", 0.0, 0), ("#000000", 1.0, int(200 * k))]))
        f.gold("13 AĞUSTOS 1521", 130 + sk.text_width("13 AĞUSTOS 1521", "title", 62, 6) / 2, H - 112, face="title", size=62, track=6, alpha=k)
    kt = cx.amt(A("c9s2", "Tenochtitlan", -0.15), 0.9)
    if kt > 0:
        kick_rule(f, "AZTEK BAŞKENTİ", W / 2, 205, k=kt, size=26, track=14, span=110)
        reveal_text(f, "TENOCHTİTLAN", W / 2, 292, kt, face="title", size=84, color="#F4DD92", track=12)


# ───────────────────────────── c9s4: Dürer ve Aztek eserleri ─────────────────────────────
@SH.kind("c9_durer")
def k_c9_durer(cx, at_br=0.0, at_az=0.0, at_ob=0.0, at_ch=0.0):
    """Solda Dürer madalyası; sağda Brüksel'de sergilenen Aztek eserleri (spot ışıklı kadife tezgâh)."""
    f = cx.f
    f.bg("night"); f.rays(alpha=0.32)
    sk.dust(f, cx.t, n=55)
    a = cx.amt(0.1, 0.8)
    xm, ym = W * 0.29, H * 0.46
    sc = (0.94 + 0.06 * ease_out(a)) * (1.0 + 0.04 * cx.u)
    draw_medal_plain(f, "durer", xm, ym, 560 * sc, "ivory", alpha=a, t=cx.t)
    SH.name_plate(f, "ALBRECHT DÜRER", "Ressam", None, cx_=xm, y=ym + 292, t=cx.amt(0.5, 0.6))
    kb = cx.amt(at_br, 0.6)
    ko = cx.amt(at_az, 0.9)
    cxr = W * 0.70
    if kb > 0:
        tag(f, "BRÜKSEL", cxr, 170, kb, size=36, align="c", track=12)
    if ko > 0:
        f.path(sk.poly_path([(cxr - 40, 250), (cxr + 40, 250), (cxr + 340, 790), (cxr - 340, 790)], True), shader=f.lin(0, 250, 0, 790, [("#FFE8B0", 0.0, int(60 * ko)), ("#FFE8B0", 1.0, 0)]), blend=skia.BlendMode.kPlus, blur=14)
        f.rrect(cxr - 410, 782, 820, 54, 12, shader=f.lin(0, 782, 0, 836, [("#5A1A20", 0.0), ("#2A0A0E", 1.0)]), alpha=ko)
        f.rect(cxr - 410, 782, 820, 5, color="#C9962B", alpha=0.9 * ko)
        icons.draw_icon(f, icn("sun_disc", "star"), cxr + 10, 560, size=340 * (0.9 + 0.1 * ease_out(ko)), metal="gold", alpha=ko, glow=0.45)
        kf = cx.amt(at_ob, 0.8)
        if kf > 0:
            icons.draw_icon(f, icn("feather", "quill"), cxr - 262, 650, size=220 * (0.9 + 0.1 * ease_out(kf)), metal="gold", alpha=kf, rot=-0.25, glow=0.3)
        k3 = cx.amt(at_ch, 0.8)
        if k3 > 0:
            icons.draw_icon(f, icn("chest", "coinbag"), cxr + 282, 690, size=200 * (0.9 + 0.1 * ease_out(k3)), metal="bronze", alpha=k3, glow=0.25)
    f.vig(0.6)


# ───────────────────────────── c9s6: Rescate odası kaplaması ─────────────────────────────
def ransom_overlay(cx):
    f = cx.f
    t0 = cx.at(A("c9s6", "1.326.539", -0.05, alt=("peso",)))
    k = cx.amt(A("c9s6", "1.326.539", -0.2, alt=("peso",)), 0.7)
    if k > 0:
        f.rect(0, H - 360, W, 360, shader=f.lin(0, H - 360, 0, H, [("#000000", 0.0, 0), ("#000000", 1.0, int(215 * k))]))
        kk = ease_out(clamp((cx.t - t0) / 3.3), 2)
        v = 1326539 * kk
        s = SH.fmt_int(v)
        SH.gold_flat(f, s, W / 2 - 110, H - 128, face="title", size=118, track=5, alpha=k)
        wd = sk.text_width(s, "title", 118, 5)
        f.text("PESO", W / 2 - 110 + wd / 2 + 30, H - 128, face="title_m", size=50, color="#E0C682", align="l", track=12, alpha=cx.amt(A("c9s6", "peso", -0.3), 0.4) * k)
        kick_rule(f, "ALTIN", W / 2, H - 252, k=k, size=26, track=16, span=90)


# ───────────────────────────── c9s8: beşte bir ─────────────────────────────
@SH.kind("c9_fifth")
def k_c9_fifth(cx, at_g=0.0, at_one=0.0):
    f = cx.f
    f.bg("night"); f.rays(alpha=0.32)
    sk.dust(f, cx.t, n=55)
    kg = cx.amt(at_g, 0.6)
    kone = cx.amt(at_one, 0.7)
    kick_rule(f, "GANİMET", W / 2, 215, k=kg, size=32, track=18, span=140)
    y0 = H * 0.66
    for i in range(5):
        ki = cx.amt(at_g, 0.5, off=0.12 * i)
        if ki <= 0:
            continue
        x = W / 2 + (i - 2) * 280
        lift = 0.0
        metal = "gold"
        if i == 0:
            lift = 120 * ease_out(kone)
            metal = "gold"
        dim = 0.55 + 0.45 * (1 - kone) if i else 1.0
        ingot(f, x, y0 + (1 - ease_out(ki)) * 50 - lift, w=236, h=112, metal=metal, alpha=ki * (dim if i else 1.0), lit=(0.5 * kone if i == 0 else 0.0))
    if kone > 0:
        x0 = W / 2 - 2 * 280
        yy = y0 - 120 * ease_out(kone)
        icons.draw_icon(f, "imperial_crown", x0, yy - 240, size=190 * (0.85 + 0.15 * back_out(kone)), metal="gold", alpha=kone, glow=0.45)
        SH.gold_flat(f, "1/5", x0 + 240, yy - 40, face="title", size=110, track=4, alpha=kone)
        f.text("KRALİYETİN PAYI", x0, y0 + 74, face="title_m", size=30, color="#F0DDA0", align="c", track=7, alpha=kone, shadow=(2, 2, 3, "#000000"))
        ring_pulse(f, x0, yy - 56, cx.at(at_one), cx.t, r0=40, r1=230, dur=1.2, color="#FFE7A0", sw=3)
    f.vig(0.6)


# ───────────────────────────── c9s14: arma ─────────────────────────────
@SH.kind("c9_arma")
def k_c9_arma(cx, at_arma=0.0, at_globe=1.0, at_motto=2.0, words=(), at_tr=6.0, trans="Beni ilk dolaşan sensin."):
    """Elcano'ya verilen arma: kalkan + altın küre + 'Primus circumdedisti me' kuşağı. words=[(sözcük, çapa)]; trans: çeviri."""
    f = cx.f
    f.bg("night"); f.rays(alpha=0.42 + 0.08 * math.sin(cx.t * 0.6))
    sk.dust(f, cx.t, n=70, alpha=0.5)
    ka = cx.amt(at_arma, 0.9)
    kg = cx.amt(at_globe, 0.9)
    km = cx.amt(at_motto, 0.9)
    scx, scy, sw_, sh_ = W / 2, 400, 430, 520
    sc = (0.88 + 0.12 * ease_out(ka)) * (1.0 + 0.03 * cx.u)
    f.c.save(); f.c.translate(scx, scy); f.c.scale(sc, sc); f.c.translate(-scx, -scy)
    if ka > 0:
        path = shield_path(scx, scy, sw_, sh_)
        sp_ = skia.Path(path)
        sp_.offset(8, 14)
        f.path(sp_, color="#000000", alpha=0.4 * ka, blur=14)
        f.path(path, shader=f.lin(scx, scy - sh_ / 2, scx, scy + sh_ / 2, [("#1D3A55", 0.0, int(255 * ka)), ("#10243A", 0.6, int(255 * ka)), ("#08141F", 1.0, int(255 * ka))]))
        f.c.save(); f.c.clipPath(path, skia.ClipOp.kIntersect, True)
        for yy in range(int(scy - sh_ / 2), int(scy + sh_ / 2), 26):       # su dalgası kazıması
            f.path(sk.smooth_path([(scx - sw_ / 2 + xx, yy + 5 * math.sin(xx * 0.05 + yy * 0.2)) for xx in range(0, int(sw_) + 30, 30)], False, 0.5), style="stroke", sw=1.3, color="#4B7C9C", alpha=0.20 * ka)
        f.circle(scx, scy - 30, 300, shader=f.rad(scx, scy - 30, 300, [("#4B7C9C", 0.0, int(90 * ka)), ("#4B7C9C", 1.0, 0)]))
        f.c.restore()
        f.path(path, style="stroke", sw=11, color="#C9962B", alpha=0.95 * ka)
        f.path(path, style="stroke", sw=3, color="#FFF0B8", alpha=0.6 * ka)
        f.path(shield_path(scx, scy, sw_ - 40, sh_ - 44), style="stroke", sw=2.2, color="#C9962B", alpha=0.7 * ka)
    f.c.restore()
    if kg > 0:
        gy = scy - 14
        draw_globe(f, scx, gy, 150 * (0.85 + 0.15 * ease_out(kg)), rot=cx.t * 0.45, alpha=kg, glow=0.35)
        ring_pulse(f, scx, gy, cx.at(at_globe), cx.t, r0=90, r1=330, dur=1.6, color="#FFE7A0", sw=3)
    # kuşak (ribbon)
    if km > 0:
        ry, rw, rh = 770, 1280, 120
        half = (rw / 2 + 70) * ease_out(km)
        f.c.save()
        f.c.clipRect(skia.Rect.MakeLTRB(W / 2 - half, ry - 90, W / 2 + half, ry + 90))
        body = [(W / 2 - rw / 2 + 60, ry - rh / 2), (W / 2 + rw / 2 - 60, ry - rh / 2), (W / 2 + rw / 2 - 10, ry), (W / 2 + rw / 2 - 60, ry + rh / 2), (W / 2 - rw / 2 + 60, ry + rh / 2), (W / 2 - rw / 2 + 10, ry)]
        # kuyruklar
        tails = [[(W / 2 - rw / 2 + 60, ry - rh / 2), (W / 2 - rw / 2 - 40, ry - rh / 2 + 22), (W / 2 - rw / 2 - 4, ry + 4), (W / 2 - rw / 2 - 40, ry + rh / 2 + 22), (W / 2 - rw / 2 + 60, ry + rh / 2)],
                 [(W / 2 + rw / 2 - 60, ry - rh / 2), (W / 2 + rw / 2 + 40, ry - rh / 2 + 22), (W / 2 + rw / 2 + 4, ry + 4), (W / 2 + rw / 2 + 40, ry + rh / 2 + 22), (W / 2 + rw / 2 - 60, ry + rh / 2)]]
        for tl_ in tails:
            f.poly(tl_, color="#5A1218", alpha=0.95)
            f.poly(tl_, style="stroke", sw=3, color="#C9962B", alpha=0.9)
        f.path(sk.poly_path(body, True), shader=f.lin(0, ry - rh / 2, 0, ry + rh / 2, [("#B02A33", 0.0), ("#8E1F26", 0.5), ("#4A0E14", 1.0)]))
        f.path(sk.poly_path(body, True), style="stroke", sw=4, color="#C9962B", alpha=0.95)
        f.line(W / 2 - rw / 2 + 80, ry - rh / 2 + 10, W / 2 + rw / 2 - 80, ry - rh / 2 + 10, color="#E8C25A", sw=1.6, alpha=0.7)
        f.line(W / 2 - rw / 2 + 80, ry + rh / 2 - 10, W / 2 + rw / 2 - 80, ry + rh / 2 - 10, color="#E8C25A", sw=1.6, alpha=0.7)
        f.c.restore()
        # sözcükler: kendi çapalarında belirir
        sizes = 56
        tracks = 7
        ws = [sk.text_width(w_[0], "title", sizes, tracks) for w_ in words]
        spc = 36
        tot = sum(ws) + spc * (len(words) - 1)
        x = W / 2 - tot / 2
        for (wtxt, wat), wd in zip(words, ws):
            kw = cx.amt(wat, 0.5)
            if kw > 0:
                f.text(wtxt, x, ry + sizes * 0.34 + (1 - kw) * 12, face="title", size=sizes, color="#F6DE96", align="l", track=tracks, alpha=kw, shadow=(2, 3, 3, "#000000"))
            x += wd + spc
    kt = cx.amt(at_tr, 0.9)
    if kt > 0:
        f.text("“" + trans + "”", W / 2, 925, face="cap_i", size=58, color="#F1E3B8", align="c", alpha=kt, shadow=(2, 3, 4, "#000000"))
        f.line(W / 2 - 140, 880, W / 2 + 140, 880, color="#C9962B", sw=2, alpha=0.7 * kt)
    f.vig(0.62)


# ───────────────────────────── c9s13b: tek gemi + Elcano ─────────────────────────────
def fleet_extra(at_ships, at_one, at_medal, at_num):
    """5 gemiden 4'ü solar, 1'i ışır; sağda '18' (Elcano madalyası wd_counter içinde)."""
    def extra(cx):
        f = cx.f
        k = cx.amt(at_ships, 0.8)
        if k <= 0:
            return
        k1 = cx.amt(at_one, 0.9)
        for i in range(5):
            x = W / 2 + (i - 2) * 190
            y = 215
            a = k * (1.0 - 0.82 * k1) if i != 2 else k
            icons.draw_icon(f, "ship", x, y, size=118 * (1.0 + (0.25 * ease_out(k1) if i == 2 else 0.0)), metal="gold" if i == 2 else "bronze", alpha=a, glow=(0.5 * k1 if i == 2 else 0.0), shadow=False)
        if k1 > 0:
            f.text("TEK GEMİ", W / 2, 322, face="title_m", size=28, color="#F0DDA0", align="c", track=10, alpha=k1, shadow=(2, 2, 3, "#000000"))
    return extra


# ───────────────────────────── c9s11: tartışma kaplaması ─────────────────────────────
def debate_overlay(cx):
    f = cx.f
    kl = cx.amt(A("c9s11", "yerlilerin", -0.25), 0.7)
    kr = cx.amt(A("c9s11", "öbürü", -0.3), 0.7)
    tag(f, "SEPÚLVEDA", 110, 790, kl, size=34, sub="Savı: köleliğe layık", align="l", accent="#9AA3AD")
    tag(f, "LAS CASAS", W - 110, 790, kr, size=34, sub="Savı: fetih bir suç", align="r", accent="#E8D8A0")
    SH.stamp(f, "RESMÎ KAZANAN YOK", W / 2, 250, rot=-0.05, size=64, t=cx.amt(A("c9s11", "Resmî", -0.1), 0.3))
