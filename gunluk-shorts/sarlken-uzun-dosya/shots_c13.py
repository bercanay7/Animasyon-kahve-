"""Bölüm 13 (Hesap) özel çekim türleri. Ad öntek: c13_. Son bölüm: kapanış compose.py'de c13 sonrası 7 sn eklenir."""
import math

import numpy as np
import skia

import d_common as D
import icons
import mapsk
import shots as SH
import shots_c12 as S12
import sk
from d_common import A, AE, icn, tag, nplate, draw_medal_plain, glow_dot, kick_rule, ring_pulse, tw, vignette_dark, draw_globe
from sk import W, H, C, back_out, clamp, ease_io, ease_out, lerp, mix, smooth

FRONTS = [("coinbag", "BANKACI"), ("monk", "KEŞİŞ"), ("crown", "KRAL"), ("crescent", "SULTAN"), ("family", "MİRAS")]


# ───────────────────────────── s1: beşinci cephe ─────────────────────────────
@SH.kind("c13_open")
def k_c13_open(cx, at_kick=0.0, at_icon=0.0, at_word=0.0):
    f = cx.f
    f.bg("night"); f.rays(alpha=0.4)
    sk.dust(f, cx.t, n=65, alpha=0.5)
    kk = cx.amt(at_kick, 0.9)
    # beş cephe sırası: dördü sönük, beşinci yanar
    gap = 150
    x0 = W / 2 - gap * 2
    for i, (ic, nm) in enumerate(FRONTS):
        on = i == 4
        a = (1.0 if on else 0.30) * cx.amt(at_kick, 0.8, off=0.05 * i)
        if on:
            glow_dot(f, x0 + i * gap, 235, 120, "#F0D27A", 0.7 * a)
        icons.draw_icon(f, ic, x0 + i * gap, 235, size=78 * (1.15 if on else 1.0), metal="gold" if on else "bronze", alpha=a, shadow=False)
    kick_rule(f, "BEŞİNCİ CEPHE", W / 2, 345, k=kk, size=32, track=20, span=150)
    ki = cx.amt(at_icon, 1.0)
    glow_dot(f, W / 2, 600, 520, "#E3B54A", 0.5 * ki)
    icons.draw_icon(f, "family", W / 2, 590, size=420 * (0.9 + 0.1 * ease_out(ki)) * (1.0 + 0.03 * cx.u), metal="gold", alpha=ki, glow=0.4 * ki)
    kw = cx.amt(at_word, 0.9)
    if kw > 0:
        f.gold("MİRAS", W / 2, 920, face="title", size=112, track=22, alpha=kw, glow=0.5 * kw)
    f.vig(0.6)


# ───────────────────────────── s2: dört taht, bir akrabalık ağı ─────────────────────────────
THRONES = [("BURGONYA", "burgonya", 0.20, 0.34), ("AVUSTURYA", "avusturya", 0.80, 0.34), ("ARAGON", "#C9962B", 0.23, 0.76), ("KASTİLYA", "ispanya", 0.77, 0.76)]


@SH.kind("c13_network")
def k_c13_network(cx, at_thrones=(0.0, 0.0, 0.0, 0.0), at_karl=0.0, at_mesh=0.0, at_blob=0.0, at_blob_off=0.0, at_net=0.0):
    f = cx.f
    f.bg("night"); f.rays(alpha=0.28)
    sk.dust(f, cx.t, n=50)
    pos = [(W * px, H * py) for _, _, px, py in THRONES]
    center = (W / 2, H * 0.53)
    # tek ülke gibi bir leke (değil)
    kb = cx.amt(at_blob, 0.7) * (1 - cx.amt(at_blob_off, 0.8))
    if kb > 0:
        blob = sk.smooth_path([(pos[0][0] - 120, pos[0][1] - 60), (W / 2, pos[0][1] - 130), (pos[1][0] + 120, pos[1][1] - 60), (pos[1][0] + 150, H * 0.55),
                               (pos[3][0] + 120, pos[3][1] + 80), (W / 2, pos[3][1] + 140), (pos[2][0] - 120, pos[2][1] + 80), (pos[2][0] - 150, H * 0.55)], True, 0.5)
        f.path(blob, color="#C9962B", alpha=0.20 * kb)
        f.path(blob, style="stroke", sw=4, color="#F0D27A", alpha=0.8 * kb)
    # akrabalık çizgileri: evlilikler
    edges = [(0, 1, "ring"), (2, 3, "ring"), (0, 3, "ring")]
    kn = cx.amt(at_net, 1.0)
    km = ease_out(clamp((cx.t - cx.at(at_mesh)) / 1.0), 2)
    for (a, b, ic) in edges:
        if km <= 0:
            break
        (xa, ya), (xb, yb) = pos[a], pos[b]
        xm, ym = lerp(xa, xb, 0.5), lerp(ya, yb, 0.5)
        f.line(xa, ya, lerp(xa, xb, km), lerp(ya, yb, km), color="#E3B54A", sw=3.4, alpha=0.85)
        if km > 0.95:
            icons.draw_icon(f, "ring", xm, ym, size=64, metal="gold", alpha=smooth((km - 0.95) / 0.05), glow=0.3)
    # her taht Karl'a bağlanır
    kk = cx.amt(at_karl, 0.8)
    for i, (xa, ya) in enumerate(pos):
        kc = ease_out(clamp((cx.t - cx.at(at_karl) - 0.12 * i) / 0.9), 2)
        if kc > 0:
            f.line(xa, ya, lerp(xa, center[0], kc), lerp(ya, center[1], kc), color="#C9962B", sw=2.4, alpha=0.7)
    # tahtlar
    for i, ((nm, col, px, py), (x, y)) in enumerate(zip(THRONES, pos)):
        k = cx.amt(at_thrones[i], 0.7)
        if k <= 0:
            continue
        c1 = sk.FAC[col][0] if col in sk.FAC else col
        glow_dot(f, x, y, 150, c1, 0.6 * k)
        f.circle(x, y, 78 * (0.8 + 0.2 * back_out(k)), shader=f.rad(x, y, 78, [(mix(c1, "#FFFFFF", 0.15), 0.0, int(255 * k)), (mix(c1, "#000000", 0.45), 1.0, int(255 * k))]))
        f.circle(x, y, 78 * (0.8 + 0.2 * back_out(k)), style="stroke", sw=3, color="#E3B54A", alpha=k)
        icons.draw_icon(f, "crown", x, y - 4, size=104 * (0.8 + 0.2 * back_out(k)), metal="gold", alpha=k, shadow=False)
        f.text(nm, x, y + 128, face="title_m", size=32, color="#F0DDA0", align="c", track=7, alpha=k, shadow=(2, 2, 3, "#000000"))
    if kk > 0:
        draw_medal_plain(f, "karl_genc", center[0], center[1], 330 * (0.9 + 0.1 * ease_out(kk)), "gold", alpha=kk, t=cx.t)
    if kn > 0:
        for j in range(3):
            ring_pulse(f, center[0], center[1], cx.at(at_net) + 0.35 * j, cx.t, r0=190, r1=520, dur=1.8, color="#F0D27A", sw=3, a=0.5)
        kick_rule(f, "AKRABALIK AĞI", W / 2, 150, k=kn, size=34, track=20, span=150)
    f.vig(0.58)


# ───────────────────────────── s3: Habsburg kartalı ikiye ayrılır ─────────────────────────────
@SH.kind("c13_split")
def k_c13_split(cx, at_karl=0.0, at_eagle=0.0, at_word=0.0, at_crack=0.0, at_split=0.0, at_color=0.0):
    f = cx.f
    f.bg("night"); f.rays(alpha=0.34)
    sk.dust(f, cx.t, n=60)
    kk = cx.amt(at_karl, 0.8) * (1 - cx.amt(at_eagle, 0.8, off=-0.2))
    if kk > 0:
        draw_medal_plain(f, "karl_yasli", W / 2, H * 0.47, 440 * (0.94 + 0.06 * ease_out(kk)), "gold", alpha=kk, t=cx.t)
    ke = cx.amt(at_eagle, 0.9)
    if ke > 0:
        sp = ease_out(clamp((cx.t - cx.at(at_split)) / 1.1), 2.2)
        kc = ease_out(clamp((cx.t - cx.at(at_crack)) / 0.6), 2)
        kcol = smooth((cx.t - cx.at(at_color)) / 0.8)
        cxm, cym, sz = W / 2, H * 0.47, 560 * (0.9 + 0.1 * ease_out(ke))
        glow_dot(f, cxm, cym, 520, "#E3B54A", 0.45 * ke * (1 - 0.5 * sp))
        for side in (-1, 1):
            f.c.save()
            f.c.translate(cxm + side * sp * 165, cym + (sp * 14 if side > 0 else 0))
            f.c.rotate(side * sp * 4.0)
            f.c.translate(-cxm, -cym)
            f.c.clipRect(skia.Rect.MakeLTRB(cxm if side > 0 else 0, 0, W if side > 0 else cxm, H))
            icons.draw_icon(f, "eagle", cxm, cym, size=sz, metal="gold", alpha=ke * (1 - kcol), glow=0.25)
            if kcol > 0:
                icons.draw_icon(f, "eagle", cxm, cym, size=sz, metal="crimson" if side < 0 else "bronze", alpha=ke * kcol, glow=0.25)
            f.c.restore()
        if kc > 0 and sp < 0.05:
            f.line(cxm, cym - sz * 0.46, cxm, lerp(cym - sz * 0.46, cym + sz * 0.46, kc), color="#FFE7A0", sw=4, alpha=0.9)
        kw = cx.amt(at_word, 0.8)
        f.text("HABSBURG HANEDANI", cxm, cym + sz * 0.5 + 92, face="title", size=54, color="#F4DD92", align="c", track=12, alpha=kw, shadow=(2, 3, 4, "#000000"))
    f.vig(0.6)


# ───────────────────────────── s3b: iki kolun haritası ─────────────────────────────
def branches_extra(at_sp, at_fel, at_aus, at_ferd):
    def extra(cx, cam, mv):
        f = cx.f
        tag(f, "İSPANYA KOLU", 96, 150, cx.amt(at_sp, 0.7), size=38, accent="#C0392B")
        tag(f, "AVUSTURYA KOLU", W - 96, 150, cx.amt(at_aus, 0.7), size=38, align="r", accent="#E07A3A")
        D.cameo(f, cx, "felipe2", 250, 440, 300, at_fel, metal="crimson", name="FELİPE", role="Oğlu", i=0, plate_dy=170)
        D.cameo(f, cx, "ferdinand", W - 250, 440, 300, at_ferd, metal="bronze", name="FERDİNAND", role="Kardeşi", i=1, plate_dy=170)
    return extra


# ───────────────────────────── s4a: çatlayan taç ─────────────────────────────
@SH.kind("c13_crown")
def k_c13_crown(cx, at_kick=0.0, at_crown=0.0, at_crack=0.0):
    f = cx.f
    f.bg("night"); f.rays(alpha=0.38)
    sk.dust(f, cx.t, n=60)
    kk = cx.amt(at_kick, 0.9)
    kick_rule(f, "EVRENSEL HIRİSTİYAN İMPARATORLUK", W / 2, 200, k=kk, size=30, track=15, span=110)
    kc = cx.amt(at_crown, 1.0)
    cxm, cym, sz = W / 2, 560, 560
    kcr = ease_out(clamp((cx.t - cx.at(at_crack)) / 1.1), 2.2)
    ksp = smooth((cx.t - cx.at(at_crack) - 0.8) / 1.4)
    glow_dot(f, cxm, cym, 560, "#E3B54A", 0.5 * kc * (1 - 0.7 * ksp))
    pts = S12.crack_pts(cxm, cym, sz * 0.42, 5)
    for side in (-1, 1):
        f.c.save()
        f.c.translate(cxm + side * ksp * 26, cym + (ksp * 14 if side > 0 else -ksp * 3))
        f.c.rotate(side * ksp * 4.0)
        f.c.translate(-cxm, -cym)
        edge = [(W if side > 0 else 0, -50)] + pts + [(W if side > 0 else 0, H + 50)]
        f.c.clipPath(sk.poly_path(edge, True), skia.ClipOp.kIntersect, True)
        icons.draw_icon(f, "imperial_crown", cxm, cym + math.sin(cx.t * 1.3) * 4 * (1 - ksp), size=sz * (0.9 + 0.1 * ease_out(kc)), metal="gold", alpha=kc, glow=0.3)
        f.c.restore()
    if kcr > 0 and ksp < 0.05:
        S12._crack(f, cxm, cym, sz * 0.42, kcr, seed=5, sw=8)
    f.vig(0.62)


# ───────────────────────────── s4b: Reform haritada yayılır ─────────────────────────────
def reform_extra(at_ref, at_aug, at_peace, at_tan):
    def extra(cx, cam, mv):
        f = cx.f
        t0 = cx.at(at_ref)
        wx, wy = cam.ll(12.65, 51.87)
        mv.city(f, cam, 12.65, 51.87, "REFORM", kind="town", t=cx.t, amt=cx.amt(at_ref, 0.5), color="#9FD8E0", size=28, name_side="t")   # kaynak kapısı: şehir adı yok (araştırmada Wittenberg geçmiyor)
        for j in range(4):
            ring_pulse(f, wx, wy, t0 + 0.0 + 0.55 * j, cx.t, r0=14, r1=520, dur=2.4, color="#6CC4CE", sw=3.5, a=0.8)
        ka = cx.amt(at_aug, 0.6)
        mv.city(f, cam, 10.9, 48.37, "AUGSBURG", kind="capital", t=cx.t, amt=ka, size=30, name_side="b")
        tag(f, "AUGSBURG BARIŞI", 96, 150, cx.amt(at_peace, 0.7), size=38, accent="#3F8C96")
        kt = cx.amt(at_tan, 0.7)
        if kt > 0:
            tag(f, "LUTHERCİLİK TANINDI", 96, 262, kt, size=34, accent="#6CC4CE")
    return extra


# ───────────────────────────── s5: denge (terazi) ─────────────────────────────
SHIELD_METALS = ["royal", "forest", "crimson", "violet", "teal", "bronze", "silver", "gold"]


@SH.kind("c13_balance")
def k_c13_balance(cx, at_av=0.0, at_crown=0.0, at_crown_off=0.0, at_shields=0.0, step=0.38, at_word=0.0):
    f = cx.f
    f.bg("night"); f.rays(alpha=0.3)
    sk.dust(f, cx.t, n=55)
    kav = cx.amt(at_av, 0.8)
    kick_rule(f, "AVRUPA", W / 2, 175, k=kav, size=36, track=24, span=150)
    t = cx.t
    t_c, t_co = cx.at(at_crown), cx.at(at_crown_off)
    t_s = cx.at(at_shields)
    # kiriş eğimi: taç sol kefede ağır → eğim; taç kalkınca damped salınım → yatay
    base = -9.0 * smooth((t - t_c) / 0.5) * (1 - smooth((t - t_co) / 0.5))
    osc = 0.0
    for t_ev, amp in ((t_co, -9.0),):
        if t > t_ev:
            osc += amp * math.exp(-2.6 * (t - t_ev)) * math.cos(6.2 * (t - t_ev)) * 0.9
    ships = []
    n_sh = 8
    for i in range(n_sh):
        ti = t_s + step * i
        ships.append(ti)
        if t > ti:
            osc += (1.6 if i % 2 == 0 else -1.6) * math.exp(-3.2 * (t - ti)) * math.cos(8.0 * (t - ti))
    ang = base + osc
    th = math.radians(ang)
    cxm, cym = W / 2, 330
    L = 520
    lx, ly = cxm - L * math.cos(th), cym - L * math.sin(th)
    rx, ry = cxm + L * math.cos(th), cym + L * math.sin(th)
    # sütun + kaide
    f.rrect(cxm - 20, cym, 40, 560, 10, shader=f.lin(cxm - 20, 0, cxm + 20, 0, [("#6B4A12", 0.0), ("#F0D27A", 0.4), ("#B8862A", 0.7), ("#4A3210", 1.0)]))
    f.rrect(cxm - 190, 880, 380, 40, 12, shader=f.lin(0, 880, 0, 920, [("#F0D27A", 0.0), ("#8A6420", 1.0)]))
    f.rrect(cxm - 130, 850, 260, 36, 10, shader=f.lin(0, 850, 0, 886, [("#E8C25A", 0.0), ("#7A5518", 1.0)]))
    # kiriş
    f.c.save(); f.c.translate(cxm, cym); f.c.rotate(ang)
    f.rrect(-L - 14, -13, 2 * L + 28, 26, 13, shader=f.lin(0, -13, 0, 13, [("#FFF0B8", 0.0), ("#C9962B", 0.5), ("#6B4A12", 1.0)]))
    f.c.restore()
    f.circle(cxm, cym, 30, shader=f.rad(cxm - 8, cym - 8, 40, [("#FFF0B8", 0.0), ("#B8862A", 1.0)]))
    f.circle(cxm, cym, 30, style="stroke", sw=3, color="#4A3210")
    # kefeler
    for side, (ex, ey) in ((-1, (lx, ly)), (1, (rx, ry))):
        py = ey + 270
        f.line(ex, ey, ex - 150, py - 20, color="#C9962B", sw=2.4, alpha=0.85)
        f.line(ex, ey, ex + 150, py - 20, color="#C9962B", sw=2.4, alpha=0.85)
        pan = skia.Path(); pan.moveTo(ex - 190, py - 20); pan.cubicTo(ex - 150, py + 40, ex + 150, py + 40, ex + 190, py - 20); pan.close()
        f.path(pan, shader=f.lin(0, py - 20, 0, py + 40, [("#F0D27A", 0.0), ("#8A6420", 1.0)]))
        f.path(pan, style="stroke", sw=2.5, color="#3A2610", alpha=0.8)
    # taç (sol kefede)
    kcw = cx.amt(at_crown, 0.6) * (1 - cx.amt(at_crown_off, 0.7))
    if kcw > 0:
        icons.draw_icon(f, "imperial_crown", lx, ly + 270 - 80 - 60 * (1 - kcw), size=190, metal="gold", alpha=kcw, glow=0.3)
    # küçük devlet kalkanları: sırayla düşer (sol, sağ, sol, ...)
    cnt = [0, 0]
    for i, ti in enumerate(ships):
        k = clamp((t - ti) / 0.45)
        if k <= 0:
            continue
        side = 0 if i % 2 == 0 else 1
        ex, ey = (lx, ly) if side == 0 else (rx, ry)
        j = cnt[side]
        cnt[side] += 1
        row, col = divmod(j, 2)
        sx = ex + (col - 0.5) * 78
        sy = ey + 270 - 44 - row * 66 - (1 - ease_out(k)) * 220
        icons.draw_icon(f, "shield", sx, sy, size=88, metal=SHIELD_METALS[i % len(SHIELD_METALS)], alpha=min(1.0, k * 2), shadow=True)
    kw = cx.amt(at_word, 0.9)
    if kw > 0:
        f.gold("DENGE", W / 2, 1010, face="title", size=64, track=22, alpha=kw, glow=0.5 * kw)
    f.vig(0.6)


# ───────────────────────────── s7: strateji oyunu paneli ─────────────────────────────
# Yalnız Karl'ın kendi hükmettiği devletler (Avusturya/Bohemya Ferdinand'ındı: listeye KONMAZ)
STATES = [("KASTİLYA", "ispanya"), ("ARAGON", "#C9962B"), ("NAPOLİ", "papalik"), ("SARDUNYA", "ispanya"), ("HOLLANDA", "burgonya"), ("MİLANO", "venedik")]
STATE_REGIONS = [("ispanya", "ispanya"), ("napoli", "papalik"), ("sardunya", "ispanya"), ("hollanda", "burgonya"), ("milano", "venedik"), ("franche_comte", "burgonya")]


@SH.kind("c13_game")
def k_c13_game(cx, at_ui=0.0, at_tip=0.0, at_one=0.0, at_many=0.0, step=0.28, at_dim=None, dim_dur=1.6):
    """Jenerik strateji-oyunu arayüzü (gerçek bir oyunun arayüzü/markası DEĞİL): üst kaynak çubuğu, mini harita, ülke listesi, ipucu kartı."""
    f = cx.f
    f.bg("night"); f.rays(alpha=0.2)
    sk.dust(f, cx.t, n=35, alpha=0.35)
    ku = cx.amt(at_ui, 0.9)
    dim = cx.amt(at_dim, dim_dur) if at_dim is not None else 0.0
    ui_a = ku * (1 - 0.82 * dim)
    X0, Y0, WW, HH = 190, 118, 1540, 726
    f.rrect(X0 - 8, Y0 - 8, WW + 16, HH + 16, 22, color="#000000", alpha=0.45 * ui_a, blur=14)
    f.rrect(X0, Y0, WW, HH, 18, shader=f.lin(0, Y0, 0, Y0 + HH, [("#241812", 0.0, int(255 * ui_a)), ("#140D09", 1.0, int(255 * ui_a))]))
    f.rrect(X0, Y0, WW, HH, 18, style="stroke", sw=3, color="#8A6A3A", alpha=0.9 * ui_a)
    f.rrect(X0 + 10, Y0 + 10, WW - 20, HH - 20, 12, style="stroke", sw=1.2, color="#8A6A3A", alpha=0.5 * ui_a)
    # üst çubuk: kaynaklar (yalnız simge + dolgu çubuğu, sayı yok)
    f.rect(X0 + 14, Y0 + 14, WW - 28, 74, color="#0E0906", alpha=0.85 * ui_a)
    res = [("coin", "#E3B54A", 0.78), ("sword", "#C0392B", 0.55), ("star", "#7FBF74", 0.66), ("scales", "#6CC4CE", 0.42)]
    for i, (ic, col, v) in enumerate(res):
        x = X0 + 70 + i * 250
        icons.draw_icon(f, ic, x, Y0 + 51, size=48, metal="gold", alpha=ui_a, shadow=False)
        f.rrect(x + 36, Y0 + 40, 150, 20, 10, color="#000000", alpha=0.55 * ui_a)
        f.rrect(x + 36, Y0 + 40, 150 * v * ease_out(clamp((cx.t - cx.at(at_ui)) / 1.4)), 20, 10, color=col, alpha=0.9 * ui_a)
    f.text("HÜKÜMDAR", X0 + WW - 60, Y0 + 62, face="title_m", size=28, color="#D9C48A", align="r", track=8, alpha=ui_a)
    # mini harita paneli (sol)
    mx0, my0, mw, mh = X0 + 30, Y0 + 106, 960, 560
    f.rrect(mx0, my0, mw, mh, 10, color="#0B1620", alpha=0.95 * ui_a)
    mv = SH.mapview()
    cam = mapsk.Cam(5.2, 45.0, 0.92)
    f.c.save()
    f.c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(mx0, my0, mw, mh), 10, 10), skia.ClipOp.kIntersect, True)
    f.c.translate(mx0 + mw / 2 - W / 2, my0 + mh / 2 - H / 2)       # harita ekran-merkezli çizilir, panele kaydırılır
    f.layer_begin(alpha=ui_a)
    mv.base(f, cam, "night", t=cx.t, mountains=False, ripples=False)
    kmany = [cx.amt(at_many, 0.6, off=step * i) for i in range(len(STATE_REGIONS))]
    for i, (rn, col) in enumerate(STATE_REGIONS):
        if kmany[i] > 0:
            mv.region(f, cam, rn, SH._fac(col), alpha=0.62, amt=kmany[i], glow=True)
    # tek hükümdarın taç simgesi → tüm devletlere ince çizgiler
    kone = cx.amt(at_one, 0.8)
    if kone > 0:
        cxx, cyy = cam.ll(5.5, 41.0)          # hükümdar simgesi denizde (hiçbir devletin üstünde değil)
        for i, (rn, col) in enumerate(STATE_REGIONS):
            if kmany[i] > 0:
                lon_lat = {"ispanya": (-3.5, 40.2), "napoli": (14.8, 40.8), "sardunya": (9.0, 40.0), "hollanda": (5.0, 52.0), "milano": (9.2, 45.3), "franche_comte": (5.9, 46.9)}[rn]
                tx, ty = cam.ll(*lon_lat)
                f.line(cxx, cyy, lerp(cxx, tx, ease_out(kmany[i])), lerp(cyy, ty, ease_out(kmany[i])), color="#FFE7A0", sw=2.2, alpha=0.8)
                f.circle(tx, ty, 6, color="#FFE7A0", alpha=0.9 * kmany[i])
        glow_dot(f, cxx, cyy, 90, "#FFE7A0", 0.8 * kone)
        icons.draw_icon(f, "imperial_crown", cxx, cyy, size=84 * (0.8 + 0.2 * back_out(kone)), metal="gold", alpha=kone, glow=0.35)
    f.layer_end()
    f.c.restore()
    f.rrect(mx0, my0, mw, mh, 10, style="stroke", sw=2, color="#8A6A3A", alpha=0.8 * ui_a)
    # ülke listesi (sağ): her satırda aynı hükümdar
    lx0, ly0, lw = mx0 + mw + 28, my0, WW - mw - 88
    f.rrect(lx0, ly0, lw, mh, 10, color="#0E0906", alpha=0.9 * ui_a)
    f.text("DEVLETLER", lx0 + lw / 2, ly0 + 46, face="title_m", size=26, color="#CDB97F", align="c", track=10, alpha=ui_a)
    for i, (nm, col) in enumerate(STATES):
        kr = cx.amt(at_many, 0.6, off=step * i * 0.9)
        yy = ly0 + 74 + i * 79
        if kr <= 0:
            continue
        f.rrect(lx0 + 14, yy, lw - 28, 66, 8, color="#1C130D", alpha=0.95 * kr * ui_a)
        f.rrect(lx0 + 14, yy, 10, 66, 4, color=SH._fac(col), alpha=kr * ui_a)
        f.text(nm, lx0 + 44, yy + 44, face="title_m", size=28, color="#F0DDA0", align="l", track=4, alpha=kr * ui_a)
        draw_medal_plain(f, "karl_olgun", lx0 + lw - 58, yy + 33, 56, "gold", alpha=kr * ui_a, t=cx.t, i=i, glint=False, shadow=False)
    # ipucu kartı
    kt = cx.amt(at_tip, 0.7) * (1 - 0.7 * dim)
    if kt > 0:
        tx, ty, tw_, th_ = W / 2 - 360, 866 + (1 - smooth(kt)) * 18, 720, 176
        f.rrect(tx - 6, ty - 6, tw_ + 12, th_ + 12, 16, color="#000000", alpha=0.5 * kt, blur=12)
        f.rrect(tx, ty, tw_, th_, 14, shader=f.lin(0, ty, 0, ty + th_, [("#2E2018", 0.0, int(250 * kt)), ("#1A100B", 1.0, int(250 * kt))]))
        f.rrect(tx, ty, tw_, th_, 14, style="stroke", sw=2.6, color="#E3B54A", alpha=0.95 * kt)
        f.gold("KİŞİSEL BİRLİK", tx + tw_ / 2, ty + 80, face="title", size=64, track=10, alpha=kt)
        k2 = cx.amt(at_one, 0.7)
        f.text("1 HÜKÜMDAR  —  ÇOK DEVLET", tx + tw_ / 2, ty + 138, face="title_m", size=30, color="#E0C682", align="c", track=8, alpha=kt * k2)
    f.vig(0.58)


# ───────────────────────────── s7b: oyun değil, ömür ─────────────────────────────
@SH.kind("c13_life")
def k_c13_life(cx, at_game=0.0, at_life=0.0, at_hour=0.0):
    f = cx.f
    f.bg("night"); f.rays(alpha=0.34)
    sk.dust(f, cx.t, n=60)
    kg = cx.amt(at_game, 0.6) * (1 - cx.amt(at_life, 0.9, off=-0.4))
    if kg > 0:
        # solan oyun çerçevesi: yalnız ince çerçeve + "OYUN" yazısı üstü çizili
        f.rrect(300, 250, W - 600, 580, 16, style="stroke", sw=3, color="#8A6A3A", alpha=0.5 * kg)
        f.text("OYUN", W / 2, 560, face="title", size=130, color="#8A7A55", align="c", track=26, alpha=0.7 * kg)
        f.line(W / 2 - 250, 520, W / 2 + 250, 520, color="#C0392B", sw=9, alpha=0.9 * kg)
    kl = cx.amt(at_life, 1.0)
    if kl > 0:
        glow_dot(f, W / 2, 480, 520, "#E3B54A", 0.5 * kl)
        icons.draw_icon(f, "hourglass", W / 2, 460, size=420 * (0.9 + 0.1 * ease_out(kl)), metal="gold", alpha=kl, glow=0.45 * kl)
        f.gold("ÖMÜR", W / 2, 840, face="title", size=118, track=30, alpha=kl, glow=0.5 * kl)
        kb = cx.amt(at_life, 1.4, off=0.5)
        x0, x1, y = 460, 1460, 935
        f.line(x0, y, x1, y, color="#C9962B", sw=3, alpha=0.6 * kb)
        f.line(x0, y, lerp(x0, x1, ease_out(kb, 2)), y, color="#F0D27A", sw=6, alpha=0.95 * kb)
        f.text("1500", x0, y + 52, face="title_m", size=30, color="#F0DDA0", align="c", track=5, alpha=kb)
        f.text("1558", x1, y + 52, face="title_m", size=30, color="#F0DDA0", align="c", track=5, alpha=kb)
    f.vig(0.6)


# ───────────────────────────── s9–s10: son çekim ─────────────────────────────
@SH.kind("c13_final")
def k_c13_final(cx, at_first=0.0, step=0.42, at_q=0.0, at_comment=0.0, at_cycle=0.0):
    """Beş cephe + 'HANGİSİNİ BIRAKIRDIN?'. at_first: ilk cephenin geldiği an; at_q: soru; at_comment: yorum balonu; at_cycle: dalgalanma başlangıcı."""
    f = cx.f
    f.bg("night"); f.rays(alpha=0.42 + 0.08 * math.sin(cx.t * 0.5))
    sk.dust(f, cx.t, n=75, alpha=0.55)
    gap = 300
    x0 = W / 2 - gap * 2
    y = H * 0.50
    cyc = clamp((cx.t - cx.at(at_cycle)) / 0.5) if at_cycle is not None else 0.0
    period = 1.05
    kq = cx.amt(at_q, 0.9)
    for i, (ic, nm) in enumerate(FRONTS):
        k = cx.amt(at_first, 0.7, off=step * i)
        if k <= 0:
            continue
        x = x0 + i * gap
        # sırayla süzülen vurgu (düşünüyormuş gibi)
        ph = (cx.t - cx.at(at_cycle)) / period
        idx = int(math.floor(ph)) % 5 if ph >= 0 else -1
        frac = ph - math.floor(ph) if ph >= 0 else 0.0
        hl = (math.sin(math.pi * frac) if i == idx else 0.0) * cyc
        glow_dot(f, x, y, 190, "#F0D27A", 0.30 * k + 0.55 * hl)
        sc = 0.8 + 0.2 * back_out(k)
        icons.draw_icon(f, ic, x, y - 8 * (1 - k), size=190 * sc * (1.0 + 0.07 * hl), metal="gold", alpha=k, glow=0.2 + 0.4 * hl)
        f.text(str(i + 1), x, y - 150, face="title", size=64, color="#F4DD92", align="c", track=4, alpha=k, shadow=(2, 3, 4, "#000000"))
        f.text(nm, x, y + 168, face="title_m", size=32, color="#F0DDA0", align="c", track=7, alpha=k, shadow=(2, 2, 3, "#000000"))
    if kq > 0:
        f.rect(0, H * 0.74, W, H * 0.26, shader=f.lin(0, H * 0.74, 0, H, [("#000000", 0.0, 0), ("#000000", 1.0, int(150 * kq))]))
        f.gold("HANGİSİNİ BIRAKIRDIN?", W / 2, H * 0.865, face="title", size=84, track=10, alpha=kq, glow=0.5 * kq, scale=1.0 + 0.02 * math.sin(cx.t * 1.2))
    kc = cx.amt(at_comment, 0.8)
    if kc > 0:
        bx, by, bw, bh = W / 2 - 250, H * 0.935 - 40, 500, 70
        f.rrect(bx, by, bw, bh, 34, color="#1B120B", alpha=0.9 * kc)
        f.rrect(bx, by, bw, bh, 34, style="stroke", sw=2.4, color="#E3B54A", alpha=0.95 * kc)
        f.poly([(bx + 90, by + bh - 2), (bx + 130, by + bh - 2), (bx + 80, by + bh + 26)], color="#1B120B", alpha=0.9 * kc)
        f.text("YORUMLARDA YAZ", W / 2, by + 47, face="title_m", size=30, color="#F3E2A8", align="c", track=10, alpha=kc)
    f.vig(0.58)
