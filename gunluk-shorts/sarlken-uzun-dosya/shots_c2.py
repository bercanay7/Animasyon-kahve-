"""Bölüm 2 (Taç Satılık) özel çekim türleri — hepsi c2_ önekli. Ton: para altını + koyu yeşil, entrika."""
import math

import numpy as np
import skia

import icons
import kit_a as K
import shots as SH
import sk
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth, back_out


def _base(cx, tone="green", rays=0.3, dust=45):
    f = cx.f
    K.bg(f, tone)
    K.rays(f, tone, rays)
    sk.dust(f, cx.t, n=dust, alpha=0.4)
    return f


def hat_pos(i, n=7, cx_=960, cy=500, rx=520, ry=250, start=-math.pi / 2):
    a = start + i * 2 * math.pi / n
    return cx_ + rx * math.cos(a), cy + ry * math.sin(a)


# ───────────────────────────── yedi seçmen (koltuk/şapka halkası) ─────────────────────────────
@SH.kind("c2_yedi_koltuk")
def k_c2_yedi(cx, mode="intro", t_crown=0.0, t_fam=0.0, t_cross=0.0, t_hats=0.0, t_label=0.0, t_vote=0.0, t_count=0.0, t_pulse=None):
    f = _base(cx, "green", 0.32, 50)
    t = cx.t
    vote = mode == "vote"
    ca = cx.amt(t_crown, 0.8)
    shrink = 1.0 if vote else smooth((t - cx.at(t_hats, off=-0.25)) / 0.7)
    cy_ = 500
    if not vote:
        # taç + üstü çizili "kalıtsal"
        csz = lerp(360, 260, shrink)
        if ca > 0:
            K.glow_disc(f, 960, cy_, csz * 0.8, "#F0D27A", 0.4 * ca)
            icons.draw_icon(f, "imperial_crown", 960, cy_ - 10 * (1 - ca), size=csz * (0.9 + 0.1 * back_out(ca)), metal="gold", alpha=ca, glow=0.35 * ca)
        fa = cx.amt(t_fam, 0.5) * (1 - shrink)
        if fa > 0:
            fx, fy = lerp(560, 330, 0.0), 520
            icons.draw_icon(f, "family", fx, fy, size=230, metal="ivory", alpha=fa)
            K.txt(f, "KALITSAL", fx, fy + 205, face="title_m", size=42, color="#E7D5A0", track=8, alpha=fa)
            K.x_mark(f, fx, fy, 125, clamp((t - cx.at(t_cross)) / 0.45), alpha=fa)
    else:
        pa = cx.amt(t_crown, 0.8)
        csz = 190
        if pa > 0:
            K.glow_disc(f, 960, 400, 220, "#F0D27A", 0.35 * pa)
            icons.draw_icon(f, "imperial_crown", 960, 398, size=csz * (0.9 + 0.1 * back_out(pa)), metal="gold", alpha=pa, glow=0.3 * pa)
    # yedi koltuk / şapka
    for i in range(7):
        a = smooth(clamp((t - cx.at(t_hats, off=i * 0.15)) / 0.45))
        if a <= 0:
            continue
        x, y = hat_pos(i, cy=cy_ if not vote else 520, rx=520 if not vote else 560, ry=250 if not vote else 280)
        pulse = 0.0
        if t_pulse is not None:
            pulse = max(0.0, math.sin((t - cx.at(t_pulse, off=i * 0.07)) * 5.0)) * (1 if t >= cx.at(t_pulse) else 0) * 0.35
        K.glow_disc(f, x, y, 125, "#F0D27A", (0.3 + pulse) * a)
        f.circle(x, y, 92, style="stroke", sw=2.2, color="#C9962B", alpha=0.55 * a)
        icons.draw_icon(f, "elector_hat", x, y - 12 * (1 - a), size=160 * (0.82 + 0.18 * back_out(a)), metal="crimson", alpha=a, glow=0.28 * a + pulse)
        if vote:
            tv = smooth(clamp((t - cx.at(t_vote, off=i * 0.07)) / 0.35))
            if tv > 0:
                tx, ty = x, y - 112 - 10 * (1 - tv)
                K.coin(f, tx, ty, 30 * (0.7 + 0.3 * back_out(tv)), alpha=tv, col="#E3B54A")
                f.text("K", tx, ty + 11, face="title", size=32, color="#3A2610", align="c", alpha=tv)
    if not vote:
        la = cx.amt(t_label, 0.6)
        if la > 0:
            SH.gold_flat(f, "YEDİ SEÇMEN", 960, 968, face="title", size=70, track=14, alpha=la)
    else:
        na = cx.amt(t_count, 0.45)
        if na > 0:
            sc = 0.85 + 0.15 * back_out(na)
            SH.gold_flat(f, "7 / 7", 960, 600 + 6 * (1 - na), face="title", size=int(190 * sc), track=12, alpha=na)
    f.vig(0.58)


# ───────────────────────────── perde / gösteri (VIII. Henry) ─────────────────────────────
def _curtain(f, side, w, t, alpha=1.0):
    """Kadife perde: dikey şeritler (kıvrım), üstte toplanma. side=-1 sol, +1 sağ."""
    n = 14
    x0 = 0 if side < 0 else W - w
    sw = w / n
    for i in range(n):
        u = i / (n - 1)
        fold = 0.5 + 0.5 * math.sin(i * 1.55 + (0.4 if side < 0 else 2.1) + math.sin(t * 0.6 + i) * 0.08)
        base = mix("#5A1018", "#C03038", 0.15 + 0.7 * fold)
        shade = 0.55 + 0.45 * (1 - abs(u - (1.0 if side < 0 else 0.0)) * 0.6)
        col = mix("#0A0203", base, clamp(shade))
        f.rect(x0 + i * sw, 0, sw + 1.5, H, shader=f.lin(0, 0, 0, H, [(mix(col, "#FFFFFF", 0.07), 0.0), (col, 0.5), (mix(col, "#000000", 0.5), 1.0)]), alpha=alpha)
    # iç kenar altın saçak
    ex = x0 + (w if side < 0 else 0)
    f.line(ex, 0, ex, H, color="#E3B54A", sw=5, alpha=0.8 * alpha)
    f.line(ex + (3 if side < 0 else -3), 0, ex + (3 if side < 0 else -3), H, color="#7A5518", sw=3, alpha=0.8 * alpha)


@SH.kind("c2_gosteri")
def k_c2_gosteri(cx, t_h=0.0, t_show=0.0, t_plate=None, size=470):
    f = cx.f
    t = cx.t
    f.bg("night")
    # sahne zemini
    f.rect(0, 870, W, 210, shader=f.lin(0, 870, 0, H, [("#2A180C", 0.0), ("#0E0805", 1.0)]))
    for i in range(14):
        f.line(i * 150 - 60, 870, i * 150 - 330 + (i * 70), H, color="#000000", sw=2, alpha=0.3)
    f.line(0, 870, W, 870, color="#8A5A2A", sw=3, alpha=0.6)
    # spot ışığı
    open_k = ease_io(clamp((t - cx.at(t_h, off=-0.5)) / 1.0))
    f.path(sk.poly_path([(900, 0), (1020, 0), (1330, 905), (590, 905)], True), shader=f.lin(0, 0, 0, 905, [("#FFF0D0", 0.0, int(70 * open_k)), ("#FFE2A0", 1.0, int(26 * open_k))]), blend=skia.BlendMode.kPlus)
    f.oval(960, 915, 400, 52, shader=f.rad(960, 915, 400, [("#FFE2A0", 0.0, int(110 * open_k)), ("#FFE2A0", 1.0, 0)]), blend=skia.BlendMode.kPlus)
    # silik rakipler (kulis)
    for (key, x, metal) in (("karl_genc", 250, "gold"), ("fransuva", 1670, "royal")):
        pass
    # Henry
    a = cx.amt(t_h, 0.9)
    if a > 0:
        SH.draw_medal(f, "henri8", 960, 545, size * (0.92 + 0.08 * ease_out(a)), "crimson", alpha=a, tilt=0.14 * math.sin(t * 0.6), glint=((t * 0.27) % 2.0) if ((t * 0.27) % 2.0) < 1 else None)
        SH.name_plate(f, "VIII. HENRY", "İngiltere Kralı", None, cx_=960, y=H * 0.77, t=cx.amt(t_plate if t_plate is not None else t_h, 0.6, off=0.5), w=640)
    # perdeler (açılır)
    w = lerp(W * 0.46, W * 0.15, open_k)
    _curtain(f, -1, w, t)
    _curtain(f, 1, w, t)
    # üst kuşak (valans) + saçaklar
    # (koyu bordo: sağ üstteki HUD simgeleri kırmızı üzerinde kaybolmasın)
    f.rect(0, 0, W, 96, shader=f.lin(0, 0, 0, 96, [("#2E0A10", 0.0), ("#1C0609", 1.0)]))
    for i in range(int(W / 120) + 2):
        f.circle(i * 120 - 10, 96, 62, color="#2A080D")
        f.circle(i * 120 - 10, 96, 62, style="stroke", sw=3, color="#C9962B", alpha=0.5)
    f.rect(0, 92, W, 6, color="#C9962B", alpha=0.8)
    # GÖSTERİ
    sa = cx.amt(t_show, 0.5)
    if sa > 0:
        SH.gold_flat(f, "GÖSTERİ", 960, 236 + 8 * (1 - sa), face="title", size=int(92 * (0.9 + 0.1 * back_out(sa))), track=22, alpha=sa)
    for (key, x, metal) in (("karl_genc", 430, "gold"), ("fransuva", 1490, "royal")):
        SH.draw_medal(f, key, x, 800, 210, metal, alpha=0.34 * smooth(t / 0.8), inscription=False)
    sk.dust(f, t, n=45, alpha=0.4)
    f.vig(0.6)


# ───────────────────────────── terazi: oylar × altın ─────────────────────────────
_PILE = K.pile_spec(n=90, seed=5, width=250.0, height=110.0, rmin=13, rmax=18)


@SH.kind("c2_terazi")
def k_c2_terazi(cx, t_scale=0.0, t_votes=0.0, t_coins=1.0):
    f = _base(cx, "green", 0.3, 45)
    t = cx.t
    a = cx.amt(t_scale, 0.7)
    kc = ease_io(clamp((t - cx.at(t_coins)) / 1.3))
    tilt = 0.02 * math.sin(t * 1.4) * (1 - kc) + 0.2 * kc

    def left(f, x, y):
        n = 7
        for i in range(n):
            ta = smooth(clamp((t - cx.at(t_votes, off=i * 0.08)) / 0.35))
            if ta <= 0:
                continue
            row = 0 if i < 4 else 1
            col = i if i < 4 else i - 4
            xx = x + (col - (1.5 if row == 0 else 1.0)) * 46
            yy = y - 14 - row * 24 - 14 * (1 - ta)
            K.coin(f, xx, yy, 21, alpha=ta, col="#E8E0CC", squash=0.55)

    def right(f, x, y):
        K.draw_pile(f, x, y - 4, ease_out(clamp((t - cx.at(t_coins, off=0.1)) / 1.5)), _PILE, alpha=1.0, scale=0.9)

    K.draw_scale(f, 960, 300, 370, tilt, left, right, alpha=a, t=t)
    f.vig(0.58)


# ───────────────────────────── 543.000 / üçte iki ─────────────────────────────
@SH.kind("c2_pay")
def k_c2_pay(cx, t_bar=0.0, t_third=0.0, t_lab=0.0, t_num=0.0, t_unit=0.0):
    f = _base(cx, "green", 0.3, 45)
    t = cx.t
    x0, x1, y, h = 320, 1600, 690, 112
    w = x1 - x0
    a = cx.amt(t_bar, 0.6)
    # çerçeve
    f.rrect(x0 - 8, y - 8, w + 16, h + 16, 18, style="stroke", sw=3.5, color="#C9962B", alpha=0.85 * a)
    f.rrect(x0, y, w, h, 12, color="#000000", alpha=0.45 * a)
    # doluluk (≈ %64)
    fill = (543.0 / 850.0) * ease_out(clamp((t - cx.at(t_num)) / 1.4), 3)
    if fill > 0:
        bw = w * fill
        f.rrect(x0, y, max(2, bw), h, 12, shader=f.lin(0, y, 0, y + h, [("#FBE9A6", 0.0), ("#E3B54A", 0.45), ("#9A6B1A", 1.0)]), alpha=a)
        f.rrect(x0, y, max(2, bw), h, 12, style="stroke", sw=2.5, color="#FFF1C2", alpha=0.7 * a)
        for k in range(8):
            f.rect(x0 + bw * (k + 0.4) / 8 - 4, y + 8, 8, h - 16, color="#FFFFFF", alpha=0.05)
        gx = x0 + ((t * 420) % (bw + 240)) - 120
        f.c.save()
        f.c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, y, max(2, bw), h), 12, 12), skia.ClipOp.kIntersect, True)
        f.rect(gx - 40, y, 80, h, shader=f.lin(gx - 40, 0, gx + 40, 0, [("#FFFFFF", 0.0, 0), ("#FFFFFF", 0.5, 90), ("#FFFFFF", 1.0, 0)]))
        f.c.restore()
        # ön kenara düşen paralar
        if fill < 0.62:
            for q in range(10):
                u = ((t * 1.3) + q * 0.1) % 1.0
                xx = x0 + bw - 20 - q * 14 + math.sin(q * 2.3) * 16
                K.coin(f, xx, y - 200 + u * 190, 13, alpha=(1 - u) ** 0.5 * a, rot=u * 5 + q, squash=abs(math.cos(u * 8 + q)) * 0.7 + 0.3)
    # ücte iki işareti
    tx = x0 + w * 2 / 3
    ta = cx.amt(t_third, 0.5)
    if ta > 0:
        p = f.paint("#F4DD92", style="stroke", sw=3.5, alpha=0.9 * ta, cap="butt")
        p.setPathEffect(skia.DashPathEffect.Make([10, 8], -t * 18))
        f.c.drawLine(tx, y - 60 * ta, tx, y + h + 38, p)
        K.txt(f, "ÜÇTE İKİ", tx, y + h + 86, face="title_m", size=36, color="#F4DD92", track=8, alpha=ta)
    # toplam
    f.text("850.000", x1, y - 22, face="cap_b", size=34, color="#C9B27A", align="r", alpha=0.85 * a, shadow=(2, 2, 3, "#000000"))
    # sayaç
    na = cx.amt(t_lab, 0.5)
    if na > 0:
        K.txt(f, "YAKLAŞIK", 960, 330, face="cap_i", size=48, color="#E7D5A0", alpha=na)
        v = 543000 * ease_out(clamp((t - cx.at(t_num)) / 1.4), 3)
        SH.gold_flat(f, SH.fmt_int(v), 960, 470, face="title", size=170, track=8, alpha=cx.amt(t_num, 0.4, off=-0.05))
        ua = cx.amt(t_unit, 0.5)
        K.txt(f, "FLORİN", 960, 556, face="title_m", size=52, color="#E0C682", track=16, alpha=max(ua, 0.0))
    f.vig(0.58)


# ───────────────────────────── çok sayıda seçmen: para → kese ─────────────────────────────
@SH.kind("c2_para")
def k_c2_para(cx, t_stamp=0.0, t_coins=0.0, t_take=0.0):
    f = _base(cx, "green", 0.3, 45)
    t = cx.t
    cxw, cyw = 960, 590
    taken = smooth((t - cx.at(t_take)) / 0.8)
    for i in range(7):
        x, y = hat_pos(i, cx_=cxw, cy=cyw - 20, rx=470, ry=210, start=-math.pi / 2)
        a = smooth(clamp((t - 0.1 * i) / 0.5))
        K.glow_disc(f, x, y, 110, "#F0D27A", 0.25 * a + 0.3 * taken * a)
        icons.draw_icon(f, "elector_hat", x, y, size=140, metal="crimson", alpha=a * (0.7 + 0.3 * taken), glow=0.2 * a + 0.35 * taken)
    # kese
    ba = cx.amt(t_coins, 0.6, off=-0.3)
    if ba > 0:
        bounce = 1.0 + 0.04 * math.sin(t * 9) * max(0.0, 1 - abs(t - cx.at(t_take)) / 0.6)
        K.glow_disc(f, cxw, cyw, 250, "#F0D27A", 0.35 * ba * (0.6 + 0.4 * taken))
        icons.draw_icon(f, "coinbag", cxw, cyw + 20, size=290 * bounce * (0.85 + 0.15 * back_out(ba)), metal="gold", alpha=ba, glow=0.3 * ba)
    # düşen paralar
    rs = np.random.RandomState(7)
    for i in range(46):
        t0 = cx.at(t_coins, off=i * 0.045)
        u = clamp((t - t0) / 0.85)
        if u <= 0 or u >= 1:
            continue
        x = cxw + (rs.rand() - 0.5) * 90 * (1 - u * 0.6) + math.sin(i) * 22 * (1 - u)
        y = lerp(-40, 505, u * u)
        K.coin(f, x, y, 17, alpha=1.0 if u < 0.92 else (1 - u) / 0.08, rot=u * 6 + i, squash=abs(math.cos(u * 9 + i)) * 0.8 + 0.2)
    SH.stamp(f, "BAZI TARİHÇİLERE GÖRE", 960, 940, rot=-0.03, size=54, t=cx.amt(t_stamp, 0.3))
    f.vig(0.58)


# ───────────────────────────── terazi 2: rüşvet? × borç ─────────────────────────────
@SH.kind("c2_borc_terazi")
def k_c2_borc(cx, t_scale=0.0, t_rus=0.0, t_tart=0.0, t_borc=0.0, t_gercek=0.0, t_crown=0.0, t_chain=0.0):
    f = _base(cx, "green", 0.3, 45)
    t = cx.t
    a = cx.amt(t_scale, 0.7)
    kb = ease_out(clamp((t - cx.at(t_borc)) / 0.7), 3)
    bounce = math.sin(max(0.0, t - cx.at(t_borc)) * 9) * 0.05 * math.exp(-max(0.0, t - cx.at(t_borc)) * 2.2)
    tilt = (0.05 * math.sin(t * 1.9) + 0.03 * math.sin(t * 3.1)) * (1 - kb) + 0.2 * kb + bounce
    cc = smooth((t - cx.at(t_crown, off=-0.2)) / 0.9)       # taç gelirken terazi geri çekilir
    sc_alpha = a * (1 - 0.82 * cc)

    def left(f, x, y):
        ra = cx.amt(t_rus, 0.6)
        if ra > 0:
            lift = kb * 28
            pulse = 0.55 + 0.25 * math.sin(t * 3.0)
            icons.draw_icon(f, "coinbag", x, y - 62 - lift, size=130, metal="bronze", alpha=ra * pulse * (1 - 0.4 * kb), shadow=False)
            f.text("?", x, y - 40 - lift, face="title", size=84, color="#F0D27A", align="c", alpha=ra * (0.8 + 0.2 * math.sin(t * 4)) * (1 - 0.5 * kb), shadow=(2, 3, 4, "#000000"))
            K.txt(f, "RÜŞVET", x, y + 100, face="title_m", size=34, color="#D9C795", track=8, alpha=ra * (1 - 0.5 * kb))

    def right(f, x, y):
        if kb > 0:
            sc = 0.8 + 0.2 * back_out(kb)
            icons.draw_icon(f, "book", x, y - 82 + 12 * (1 - kb), size=190 * sc, metal="gold", alpha=kb, glow=0.3 * kb)
            K.txt(f, "BORÇ", x, y + 102, face="title", size=48, color="#F6DC8A", track=10, alpha=kb)

    K.draw_scale(f, 960, 300, 370, tilt, left, right, alpha=sc_alpha, t=t)
    if cx.amt(t_tart, 0.3) > 0 and cc < 0.5:
        SH.stamp(f, "TARTIŞMALI", 430, 880, rot=-0.08, size=54, t=cx.amt(t_tart, 0.3), alpha=1 - cc * 2)
    ga = cx.amt(t_gercek, 0.5)
    if ga > 0 and cc < 0.6:
        K.txt(f, "GERÇEK", 1322, 925, face="title_m", size=44, color="#F6DC8A", track=12, alpha=ga * (1 - cc))
    # taç + zincir
    ca = cx.amt(t_crown, 0.8)
    if ca > 0:
        cyc = 500
        K.glow_disc(f, 960, cyc, 300, "#F0D27A", 0.4 * ca)
        icons.draw_icon(f, "imperial_crown", 960, cyc - 30 * (1 - ease_out(ca)), size=380, metal="gold", alpha=ca, glow=0.4 * ca)
        k = clamp((t - cx.at(t_chain)) / 1.1)
        if k > 0:
            pts = []
            for j in range(25):
                ang = -math.pi * 0.62 + j * (2 * math.pi) / 24
                pts.append((960 + 290 * math.cos(ang), cyc + 14 + 150 * math.sin(ang)))
            K.chain(f, pts, prog=ease_out(k), link=44, thick=10, col="#B6BDC8", alpha=1.0)
    f.vig(0.58)


# ───────────────────────────── Plus Ultra: Herkül sütunları + deviz bandı ─────────────────────────────
@SH.kind("c2_plus_ultra")
def k_c2_plus_ultra(cx, t_pillars=0.0, t_motto=0.0, t_sub=0.0):
    f = _base(cx, "night", 0.35, 55)
    t = cx.t
    pa = cx.amt(t_pillars, 0.9)
    sc = 1.0 + 0.05 * cx.u
    f.c.save()
    f.c.translate(960, 540)
    f.c.scale(sc, sc)
    f.c.translate(-960, -540)
    def _pillars(ff):
        for x in (500, 1420):
            K.glow_disc(ff, x, 470, 330, "#F0D27A", 0.3)
            icons.draw_icon(ff, "c2_sutun", x, 470, size=700, metal="gold", alpha=1.0, glow=0.25)
    img = sk.baked(("c2_pillars",), _pillars)
    if pa > 0:
        pp = skia.Paint(AntiAlias=True)
        pp.setAlphaf(clamp(pa))
        f.c.drawImage(img, 0, 40 * (1 - ease_out(pa)), skia.SamplingOptions(skia.FilterMode.kLinear), pp)
    ma = cx.amt(t_motto, 0.7)
    if ma > 0:
        yb = 560
        K.ribbon(f, 960, yb, 1160, 150, alpha=ma)
        f.text("PLUS ULTRA", 960, yb + 28, face="title", size=84, color="#2A1A0C", align="c", track=16, alpha=ma)
    sa = cx.amt(t_sub, 0.7)
    if sa > 0:
        f.text("DAHA ÖTEYE", 960, 790 + 8 * (1 - sa), face="cap_i", size=76, color="#F3DE9A", align="c", alpha=sa, shadow=(2, 3, 5, "#000000"))
        ar = ease_out(sa)
        f.line(700, 830, 700 + 520 * ar, 830, color="#C9962B", sw=3, alpha=0.8 * sa)
    f.c.restore()
    f.vig(0.58)
