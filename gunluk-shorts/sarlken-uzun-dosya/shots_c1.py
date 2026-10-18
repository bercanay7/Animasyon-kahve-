"""Bölüm 1 (Dört Tahtın Çocuğu) özel çekim türleri — hepsi c1_ önekli. kit_a yardımcılarını kullanır."""
import math

import numpy as np
import skia

import icons
import shots as SH
import sk
import stage as ST
import kit_a as K
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth, back_out


def bump(t, t0, dur):
    return math.sin(math.pi * clamp((t - t0) / dur))


def _base(cx, rays=0.3, dust=45):
    f = cx.f
    f.bg("night")
    f.rays(alpha=rays)
    sk.dust(f, cx.t, n=dust, alpha=0.4)
    return f


# ───────────────────────────── c1s4: miras yolu ─────────────────────────────
_YOL = [(330, 800), (580, 790), (700, 650), (860, 590), (1060, 610), (1230, 510), (1320, 380), (1470, 310), (1570, 280)]


@SH.kind("c1_yol")
def k_c1_yol(cx, t_far=0.0, t_name=0.0, t_five=0.0, t_cousin=0.0, t_age=None, t_die=0.0, t_open=0.0):
    f = _base(cx, 0.28, 40)
    t = cx.t
    path = sk.smooth_path(_YOL, False, 0.5)
    pm = skia.PathMeasure(path, False)
    L = pm.getLength()
    far = ease_io(clamp((t - cx.at(t_far, off=-0.4)) / 2.4))
    opened = ease_io(clamp((t - cx.at(t_open, off=-0.3)) / 1.1))
    # tacın yeri: soluk → altın
    cxw, cyw = _YOL[-1][0] + 10, _YOL[-1][1] - 40
    g = smooth(clamp((t - cx.at(t_open, off=0.4)) / 0.7))
    na = cx.amt(t_name, 0.7)
    if na > 0:
        icons.draw_icon(f, "crown", cxw, cyw, size=300, metal="bronze", alpha=0.55 * na * (1 - g), shadow=False)
        if g > 0:
            K.glow_disc(f, cxw, cyw, 330, "#F0D27A", 0.55 * g)
            icons.draw_icon(f, "crown", cxw, cyw, size=300 * (1 + 0.04 * math.sin(t * 2)), metal="gold", alpha=g, glow=0.5 * g)
        K.txt(f, "İSPANYA TAHTI", cxw, cyw + 205, face="title_m", size=34, color="#E3CF98", track=9, alpha=na)
    # kesikli yol (uzaklık)
    if far > 0:
        part = skia.Path()
        pm.getSegment(0, L * far, part, True)
        p = f.paint("#C9B27A", style="stroke", sw=6, alpha=0.8 * (1 - 0.4 * opened), cap="butt")
        p.setPathEffect(skia.DashPathEffect.Make([20, 16], -t * 26))
        f.c.drawPath(part, p)
    # açılan altın yol
    if opened > 0:
        seg = skia.Path()
        pm.getSegment(0, L * opened, seg, True)
        f.path(seg, style="stroke", sw=26, color="#F0D27A", alpha=0.22, blur=12)
        f.path(seg, style="stroke", sw=11, color="#2A1A0C", alpha=0.6)
        f.path(seg, style="stroke", sw=6.5, color="#F6DC8A")
        pos, _ = pm.getPosTan(L * opened)
        if pos is not None and opened < 0.999:
            K.glow_disc(f, pos.x(), pos.y(), 60, "#FFE9A8", 0.8)
    # Şarlken
    ka = cx.amt(0.0, 0.8)
    SH.draw_medal(f, K.mkey("karl_cocuk"), _YOL[0][0] - 20, _YOL[0][1] - 20, 300, "gold", alpha=ka, inscription=False, tilt=0.18 * math.sin(t * 0.6))
    # bebek kuzen: mum
    pos, _ = pm.getPosTan(L * 0.47)
    bx, by = pos.x(), pos.y()
    ap = cx.amt(t_cousin, 0.7, off=-0.1)
    snuff = smooth(clamp((t - cx.at(t_die, off=-0.1)) / 0.4))
    if ap > 0:
        K.candle(f, bx, by + 16, 150, t, lit=ap * (1 - snuff), alpha=ap, dim=snuff, seed=2.0)
        K.smoke_wisp(f, bx, by - 175, cx.at(t_die, off=-0.05), t, h=150, alpha=0.6)
        la = cx.amt(t_age if t_age is not None else t_cousin, 0.6, off=0.1) * (1 - 0.35 * snuff)
        K.txt(f, "İKİ YAŞINA BASMAMIŞ KUZEN", bx, by + 92, face="cap_i", size=40, color="#EFE2B8", alpha=la)
    # 5 AY sayacı
    fa = cx.amt(t_five, 0.5) * (1 - smooth(clamp((t - cx.at(t_open, off=0.2)) / 0.6)))
    if fa > 0:
        x0 = 960 - 2 * 48
        for i in range(5):
            k = smooth(clamp((t - cx.at(t_five, off=0.05 + i * 0.2)) / 0.3))
            f.circle(x0 + i * 48, 905, 15, style="stroke", sw=2.5, color="#C9962B", alpha=0.8 * fa)
            f.circle(x0 + i * 48, 905, 11 * k, shader=f.rad(x0 + i * 48, 905, 12, [("#FFF1B8", 0.0), ("#E3B54A", 1.0)]), alpha=fa)
        K.txt(f, "5 AY", 960, 985, face="title", size=64, color="#F3DE9A", track=10, alpha=fa)
    # ölüm anında kısa kararma
    dd = bump(t, cx.at(t_die, off=-0.1), 0.7)
    if dd > 0:
        f.rect(0, 0, W, H, color="#000000", alpha=0.28 * dd)
    f.vig(0.6)


# ───────────────────────────── c1s2: Juana & Filip ─────────────────────────────
@SH.kind("c1_evli")
def k_c1_evli(cx, a_j=0.3, a_f=1.0, a_ring=2.0, size=500, juana=("JUANA", "Kastilya Kraliçesi"), filip=("FİLİP", "Burgonyalı · “Yakışıklı”")):
    f = _base(cx, 0.3, 50)
    t = cx.t
    xj, xf, y = W * 0.30, W * 0.70, H * 0.44
    for (key, x, a_, nm, flip) in (("juana", xj, a_j, juana, False), (K.mkey("filip", "ferdinand"), xf, a_f, filip, True)):
        a = cx.amt(a_, 0.8)
        sc = (0.92 + 0.08 * ease_out(a)) * (1 + 0.03 * cx.u)
        SH.draw_medal(f, key, x, y, size * sc, "gold", flip, alpha=a, tilt=0.16 * math.sin(t * 0.55 + x * 0.002), glint=((t * 0.26 + x * 0.0004) % 2.0) if ((t * 0.26 + x * 0.0004) % 2.0) < 1 else None)
        SH.name_plate(f, nm[0], nm[1], None, cx_=x, y=y + size * 0.5, t=cx.amt(a_, 0.6, off=0.45), w=600)
    ra = cx.amt(a_ring, 0.7)
    if ra > 0:
        K.glow_disc(f, W / 2, y, 210, "#F0D27A", 0.5 * ra)
        icons.draw_icon(f, "ring", W / 2, y, size=190 * (0.8 + 0.2 * back_out(ra)), metal="gold", alpha=ra, glow=0.4 * ra)
        for sg in (-1, 1):
            f.line(W / 2 + sg * 120, y, W / 2 + sg * (120 + 130 * ra), y, color="#C9962B", sw=2.5, alpha=0.7 * ra)
    f.vig(0.55)


# ───────────────────────────── c1s5: evlilikle ve ölümle ─────────────────────────────
@SH.kind("c1_cift")
def k_c1_cift(cx, t_crowns=0.0, t_ring=1.0, t_skull=2.0):
    f = _base(cx, 0.3, 55)
    t = cx.t
    starts = [(-160, -120), (W + 160, -120), (-160, H + 120), (W + 160, H + 120)]
    for i in range(4):
        tx = W / 2 + (i - 1.5) * 235
        ty = 300 + abs(i - 1.5) * 38
        k = ease_out(clamp((t - cx.at(t_crowns, off=i * 0.16)) / 1.0), 3)
        if k <= 0:
            continue
        x = lerp(starts[i][0], tx, k)
        y = lerp(starts[i][1], ty, k) + math.sin(t * 1.4 + i) * 5 * k
        K.glow_disc(f, x, y, 150, "#F0D27A", 0.35 * k)
        icons.draw_icon(f, "crown", x, y, size=195, metal="gold", alpha=min(1.0, k * 1.5), rot=(1 - k) * (-0.9 if i % 2 == 0 else 0.9), glow=0.25 * k)
    # evlilik / ölüm
    for (ic, lab, ta, x, metal) in (("ring", "EVLİLİK", t_ring, W * 0.30, "gold"), ("skull", "ÖLÜM", t_skull, W * 0.70, "silver")):
        a = cx.amt(ta, 0.7, off=-0.1)
        if a <= 0:
            continue
        y = 700
        K.glow_disc(f, x, y, 240, "#F0D27A" if metal == "gold" else "#D0D8E0", 0.3 * a)
        icons.draw_icon(f, ic, x, y - 8 * (1 - a), size=270 * (0.82 + 0.18 * back_out(a)), metal=metal, alpha=a, glow=0.3 * a)
        K.txt(f, lab, x, y + 190, face="title", size=52, color="#F3DE9A", track=12, alpha=a)
    va = cx.amt(t_skull, 0.6, off=-0.4)
    K.txt(f, "VE", W / 2, 720, face="cap_i", size=64, color="#C9B27A", alpha=va)
    f.vig(0.58)


# ───────────────────────────── c1s9: delilik mi, siyaset mi ─────────────────────────────
@SH.kind("c1_delilik")
def k_c1_delilik(cx, t_l=0.0, t_r=1.0, t_q=2.0, t_stamp=3.0):
    f = _base(cx, 0.3, 50)
    t = cx.t
    xl, xr, y = 540, 1380, 500
    qa = cx.amt(t_q, 0.6, off=-0.6)
    # bağlayan kesikli yay
    if qa > 0:
        arc = skia.Path()
        arc.moveTo(xl + 190, y)
        arc.quadTo(960, y - 120, xr - 190, y)
        p = f.paint("#C9B27A", style="stroke", sw=4, alpha=0.7 * qa, cap="butt")
        p.setPathEffect(skia.DashPathEffect.Make([14, 12], -t * 20))
        f.c.drawPath(arc, p)
    for (ic, lab, ta, x, metal) in (("c1_sarmal", "DELİLİK?", t_l, xl, "gold"), ("crown", "SİYASET?", t_r, xr, "gold")):
        a = cx.amt(ta, 0.7, off=-0.1)
        if a <= 0:
            continue
        K.glow_disc(f, x, y, 270, "#F0D27A", 0.28 * a)
        f.circle(x, y, 210, style="stroke", sw=3, color="#C9962B", alpha=0.7 * a)
        f.circle(x, y, 222, style="stroke", sw=1.2, color="#C9962B", alpha=0.5 * a)
        icons.draw_icon(f, ic, x, y, size=300 * (0.85 + 0.15 * back_out(a)), metal=metal, alpha=a, glow=0.25 * a, rot=(0.05 * math.sin(t * 1.3) if ic == "c1_sarmal" else 0))
        K.txt(f, lab, x, y + 300, face="title", size=54, color="#F3DE9A", track=10, alpha=a)
    if qa > 0:
        icons.draw_icon(f, "question", 960, y - 40 + math.sin(t * 1.6) * 8, size=200 * (0.8 + 0.2 * back_out(qa)), metal="silver", alpha=qa, glow=0.3 * qa)
    SH.stamp(f, "TARTIŞMALI", 960, 910, rot=-0.07, size=78, t=cx.amt(t_stamp, 0.3))
    f.vig(0.58)


# ───────────────────────────── c1s11: dört dil ─────────────────────────────
@SH.kind("c1_dort_dil")
def k_c1_dort_dil(cx, items=(), t_stamp=0.0):
    """items: [dict(icon, metal, who, lang, t_who, t_lang)]"""
    f = _base(cx, 0.3, 55)
    t = cx.t
    n = len(items)
    xs = [W * (0.5 + (i - (n - 1) / 2) * 0.22) for i in range(n)]
    f.text("“", 150, 330, face="title", size=300, color="#C9962B", align="l", alpha=0.18)
    for i, it in enumerate(items):
        x = xs[i]
        a = cx.amt(it["t_who"], 0.7, off=-0.1)
        b = cx.amt(it["t_lang"], 0.6, off=-0.05)
        if a <= 0:
            continue
        K.glow_disc(f, x, 470, 230, "#F0D27A", 0.28 * a)
        f.circle(x, 470, 168, style="stroke", sw=2.5, color="#C9962B", alpha=0.65 * a)
        icons.draw_icon(f, it["icon"], x, 470 - 10 * (1 - a), size=210 * (0.85 + 0.15 * back_out(a)), metal=it.get("metal", "gold"), alpha=a, glow=0.25 * a)
        K.txt(f, it["who"], x, 715, face="cap_i", size=42, color="#E3D3A4", alpha=a)
        if b > 0:
            f.line(x - 90 * b, 750, x + 90 * b, 750, color="#C9962B", sw=2, alpha=0.7)
            SH.gold_flat(f, it["lang"], x, 830 + 8 * (1 - b), face="title", size=52, track=7, alpha=b)
    SH.stamp(f, "RİVAYET", W - 330, 195, rot=-0.1, size=62, t=cx.amt(t_stamp, 0.3))
    f.vig(0.58)


# ───────────────────────────── c1s13: ortak kral ─────────────────────────────
def _shield_path(x, y, w, h):
    p = skia.Path()
    p.moveTo(x - w / 2, y - h / 2)
    p.lineTo(x + w / 2, y - h / 2)
    p.lineTo(x + w / 2, y + h * 0.08)
    p.cubicTo(x + w / 2, y + h * 0.34, x + w * 0.22, y + h * 0.48, x, y + h / 2)
    p.cubicTo(x - w * 0.22, y + h * 0.48, x - w / 2, y + h * 0.34, x - w / 2, y + h * 0.08)
    p.close()
    return p


def draw_shield(f, x, y, w, h, kind, alpha=1.0, scale=1.0):
    """Kastilya (kırmızı zemin, altın kale) / Aragon (altın zemin, dört kırmızı şerit) kalkanı."""
    if alpha <= 0:
        return
    f.c.save()
    f.c.translate(x, y)
    f.c.scale(scale, scale)
    path = _shield_path(0, 0, w, h)
    f.path(path, color="#000000", alpha=0.35 * alpha, blur=12)
    f.c.save()
    f.c.clipPath(path, skia.ClipOp.kIntersect, True)
    if kind == "kastilya":
        f.rect(-w / 2, -h / 2, w, h, shader=f.lin(0, -h / 2, 0, h / 2, [("#B8303C", 0.0), ("#8E1F26", 0.6), ("#5E1218", 1.0)]), alpha=alpha)
    else:
        f.rect(-w / 2, -h / 2, w, h, shader=f.lin(0, -h / 2, 0, h / 2, [("#F2CF6A", 0.0), ("#D9A63A", 0.6), ("#A87A22", 1.0)]), alpha=alpha)
        for i in range(4):
            bx = -w / 2 + w * (0.10 + i * 0.2) + w * 0.0
            f.rect(bx, -h / 2, w * 0.1, h, color="#A52A2A", alpha=0.95 * alpha)
    f.c.restore()
    if kind == "kastilya":
        icons.draw_icon(f, "castle", 0, -h * 0.03, size=w * 0.72, metal="gold", alpha=alpha, shadow=False)
    f.path(path, style="stroke", sw=7, color="#2A1A0C", alpha=0.85 * alpha)
    f.path(path, style="stroke", sw=3.5, color="#E3B54A", alpha=alpha)
    f.c.restore()


@SH.kind("c1_ortak_kral")
def k_c1_ortak_kral(cx, a_karl=0.0, a_juana=1.0, a_bars=1.2, a_link=2.0, a_k=3.0, a_a=4.0, a_crown=5.0):
    f = _base(cx, 0.3, 50)
    t = cx.t
    xk, xj, ym = 690, 1230, 640
    ka = cx.amt(a_karl, 0.8)
    SH.draw_medal(f, "karl_genc", xk, ym, 430 * (0.94 + 0.06 * ease_out(ka)), "gold", alpha=ka, tilt=0.15 * math.sin(t * 0.5), inscription=False)
    ja = cx.amt(a_juana, 0.8)
    SH.draw_medal(f, "juana", xj, ym + 20, 340 * (0.94 + 0.06 * ease_out(ja)), "gold", alpha=ja, tilt=-0.12 * math.sin(t * 0.5 + 1), inscription=False)
    # demir parmaklık (tutsak)
    bk = ease_out(clamp((t - cx.at(a_bars)) / 0.7), 3)
    if bk > 0:
        r = 160
        f.c.save()
        cp = skia.Path()
        cp.addCircle(xj, ym + 20, r * 1.02)
        f.c.clipPath(cp, skia.ClipOp.kIntersect, True)
        for i in range(-3, 4):
            bx = xj + i * 46
            top = ym + 20 - r - 20
            hh = (2 * r + 40) * bk
            f.rect(bx - 7, top, 14, hh, shader=f.lin(bx - 7, 0, bx + 7, 0, [("#0E0C0A", 0.0), ("#6A665C", 0.45), ("#12100E", 1.0)]), alpha=0.92)
        f.rect(xj - r, ym + 20 - 60, 2 * r, 14 * bk, color="#1C1915", alpha=0.9)
        f.rect(xj - r, ym + 20 + 60, 2 * r, 14 * bk, color="#1C1915", alpha=0.9)
        f.c.restore()
        f.circle(xj, ym + 20, r * 1.02, style="stroke", sw=6, color="#14110E", alpha=0.8 * bk)
    la = cx.amt(a_link, 0.6)
    if la > 0:
        K.chain(f, [(xk + 205, ym + 8), ((xk + xj) / 2 + 10, ym + 52), (xj - 165, ym + 20)], prog=la, link=34, thick=8, col="#D9B65A", alpha=la)
    # kalkanlar ve taç
    for (kind, x, ta, lab) in (("kastilya", 560, a_k, "KASTİLYA"), ("aragon", 1360, a_a, "ARAGON")):
        s = cx.amt(ta, 0.6)
        if s <= 0:
            continue
        yy = 230 + (1 - ease_out(s)) * -120
        draw_shield(f, x, yy, 150, 180, kind, alpha=s)
        K.txt(f, lab, x, yy + 148, face="title_m", size=30, color="#F0DDA0", track=8, alpha=s)
    ca = cx.amt(a_crown, 0.8)
    if ca > 0:
        K.glow_disc(f, W / 2, 230, 260, "#F0D27A", 0.5 * ca)
        icons.draw_icon(f, "crown", W / 2, 230 - 40 * (1 - ease_out(ca)), size=230, metal="gold", alpha=ca, glow=0.5 * ca)
    f.vig(0.58)


# ───────────────────────────── c1s15: yeni halk ─────────────────────────────
@SH.kind("c1_halk")
def k_c1_halk(cx, a_q=(1.0, 1.5, 2.0), size=520):
    f = cx.f
    t = cx.t
    K.bg(f, "dusk")
    # ufuk: uzak tepeler + sıcak ufuk ışığı
    f.rect(0, 560, W, 520, shader=f.lin(0, 560, 0, H, [("#241812", 0.0), ("#0E0907", 1.0)]))
    f.circle(1450, 600, 520, shader=f.rad(1450, 600, 520, [("#FFB86B", 0.0, 120), ("#C9702A", 0.5, 45), ("#C9702A", 1.0, 0)]), blend=skia.BlendMode.kPlus)
    ST.hills(f, 600, 40, "#1A1210", seed=4, step=70, wavelength=0.006)
    ST.hills(f, 680, 30, "#120C09", seed=7, step=70, wavelength=0.009)
    f.rect(0, 700, W, 8, color="#8C5A2A", alpha=0.25)
    # kalabalık
    ST.crowd(f, 3, 960, 2000, 880, 62, 300, 1.12, ["peasant", "fisherman", "woman", "fisherman", "peasant", "child", "merchant"], col="#0A0604", rim="#B97A3A", seed=21, dens=70, face=-1, depth_fog="#2A170C")
    # soru işaretleri
    for i, (qx, qy) in enumerate(((1180, 500), (1440, 470), (1700, 520))):
        a = cx.amt(a_q[i], 0.5)
        if a > 0:
            yy = qy - 22 * (1 - a) + math.sin(t * 1.8 + i * 1.3) * 7
            f.text("?", qx, yy, face="title", size=118, color="#F0D27A", align="c", alpha=a, shadow=(2, 3, 5, "#000000"))
    # kral madalyası
    a = cx.amt(0.0, 0.8)
    SH.draw_medal(f, "karl_genc", 520, 470, size * (0.94 + 0.06 * ease_out(a)), "gold", alpha=a, tilt=0.18 * math.sin(t * 0.5), glint=((t * 0.27) % 2.0) if ((t * 0.27) % 2.0) < 1 else None)
    SH.name_plate(f, "17 YAŞINDA · KRAL", None, None, cx_=520, y=H * 0.80, t=cx.amt(0.5, 0.6), w=620)
    sk.dust(f, t, n=40, alpha=0.4)
    f.vig(0.62)
