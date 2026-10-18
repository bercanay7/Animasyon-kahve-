"""Bölüm 12 (Bırakmak) özel çekim türleri. Ad öntek: c12_. c0'ın aynası: aynı salon, ağır altın ışık, vedaya dönük."""
import math

import numpy as np
import skia

import d_common as D
import icons
import scenes_d as SD
import shots as SH
import sk
from d_common import A, AE, icn, tag, nplate, draw_medal_plain, glow_dot, kick_rule, ring_pulse, tw, vignette_dark
from sk import W, H, C, back_out, clamp, ease_io, ease_out, lerp, mix, smooth

ROMAN = ["XII", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]


# ───────────────────────────── saat kadranı ─────────────────────────────
def _dial_builder(cx_, cy_, R):
    def b(f):
        f.circle(cx_ + 9, cy_ + 16, R * 1.05, color="#000000", alpha=0.5, blur=20)
        f.circle(cx_, cy_, R, shader=f.lin(cx_ - R, cy_ - R, cx_ + R, cy_ + R, [("#FFF0B8", 0.0), ("#D4A23A", 0.45), ("#6B4A12", 1.0)]))
        f.circle(cx_, cy_, R * 0.935, shader=f.lin(cx_ + R, cy_ + R, cx_ - R, cy_ - R, [("#FFF0B8", 0.0), ("#B8862A", 0.5), ("#4A3210", 1.0)]))
        f.circle(cx_, cy_, R * 0.895, shader=f.rad(cx_ - R * 0.1, cy_ - R * 0.25, R * 1.05, [("#33201A", 0.0), ("#1B1009", 0.6), ("#0E0805", 1.0)]))
        for i in range(60):
            a = math.radians(i * 6 - 90)
            hr = (i % 5 == 0)
            r0, r1 = R * (0.78 if hr else 0.82), R * 0.86
            f.line(cx_ + math.cos(a) * r0, cy_ + math.sin(a) * r0, cx_ + math.cos(a) * r1, cy_ + math.sin(a) * r1, color="#D9B14A", sw=3.2 if hr else 1.4, alpha=0.9 if hr else 0.55)
        f.circle(cx_, cy_, R * 0.60, style="stroke", sw=1.6, color="#C9962B", alpha=0.45)
        f.circle(cx_, cy_, R * 0.585, style="stroke", sw=0.8, color="#C9962B", alpha=0.35)
        for i, rn in enumerate(ROMAN):
            a = math.radians(i * 30 - 90)
            x, y = cx_ + math.cos(a) * R * 0.69, cy_ + math.sin(a) * R * 0.69
            sz = R * 0.15
            f.gold(rn, x, y + sz * 0.36, face="title", size=sz, track=1.5)
        # güneş/ay süsü (kadran iç halkası)
        f.circle(cx_, cy_ + R * 0.30, R * 0.055, color="#C9962B", alpha=0.35)
    return b


def _hand(f, cx_, cy_, ang_deg, L, w, col_a="#FBE9A6", col_b="#B8862A", tail=0.2):
    f.c.save()
    f.c.translate(cx_, cy_)
    f.c.rotate(ang_deg)
    pts = [(-L * tail, 0), (L * 0.06, -w * 0.9), (L * 0.40, -w * 1.55), (L * 0.52, -w * 0.5), (L * 1.0, 0), (L * 0.52, w * 0.5), (L * 0.40, w * 1.55), (L * 0.06, w * 0.9)]
    path = sk.smooth_path(pts, True, 0.18)
    f.path(skia.Path(path), shader=skia.GradientShader.MakeLinear([(0, -w), (0, w)], [C(col_a), C(col_b)], [0, 1]))
    f.path(path, style="stroke", sw=2.0, color="#3A2610", alpha=0.9)
    f.c.restore()


@SH.kind("c12_clock")
def k_c12_clock(cx, at_city=0.0, at_date=0.0, at_clock=0.0, at_hand=0.0, at_three=0.0):
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.5 + 0.12 * math.sin(cx.t * 0.5))
    sk.dust(f, cx.t, n=80, alpha=0.5)
    R, ccx, ccy = 205, W / 2, H * 0.665
    kc = cx.amt(at_city, 0.8)
    kick_rule(f, "BRÜKSEL", W / 2, 175, k=kc, size=34, track=22, span=170)
    ka = cx.amt(at_date, 1.0)
    f.gold("25 EKİM 1555", W / 2, 322, face="title", size=118, track=14, alpha=ka, scale=1.05 - 0.05 * ease_out(clamp(cx.t / 6.0), 2), glow=0.5 * ka)
    kd = cx.amt(at_clock, 1.0)
    if kd > 0:
        img = sk.baked(("c12_dial", R, int(ccx), int(ccy)), _dial_builder(ccx, ccy, R))
        p = skia.Paint(AntiAlias=True)
        p.setAlphaf(kd)
        f.c.drawImage(img, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear), p)
        # akrep: XII → III ('saat üç')
        t_h = cx.at(at_hand)
        t_3 = cx.at(at_three)
        k = ease_io(clamp((cx.t - t_h) / max(0.4, (t_3 + 0.35 - t_h))), 2.2)
        over = 0.0 if k < 1 else 0.0
        ang = -90 + 90 * k
        # yelkovan XII'de, hafif titreme
        _hand(f, ccx, ccy, -90 + 0.6 * math.sin(cx.t * 3.1), R * 0.78, 6.0, tail=0.16)
        _hand(f, ccx, ccy, ang, R * 0.55, 8.5, col_a="#FFF0B8", col_b="#C9962B")
        f.circle(ccx, ccy, 15, shader=f.rad(ccx - 4, ccy - 4, 18, [("#FFF0B8", 0.0), ("#B8862A", 1.0)]))
        f.circle(ccx, ccy, 15, style="stroke", sw=2, color="#3A2610")
        if k >= 1:
            glow_dot(f, ccx + R * 0.45, ccy, 110, "#FFE7A0", 0.55 * (1 - smooth((cx.t - t_3 - 0.9) / 1.2)))
            for j in range(3):
                ring_pulse(f, ccx, ccy, t_3 + 0.35 + 0.45 * j, cx.t, r0=R * 0.9, r1=R * 1.5, dur=1.5, color="#F0D27A", sw=3, a=0.55)
        kt = cx.amt(at_three, 0.7)
        if kt > 0:
            f.gold("≈ 15.00", ccx + R + 230, ccy + 26, face="title", size=84, track=8, alpha=kt)
    f.vig(0.6)


# ───────────────────────────── 40 YIL ─────────────────────────────
@SH.kind("c12_forty")
def k_c12_forty(cx, at_old=0.0, at_back=0.0, at_young=0.0, at_crown=0.0, x0=330, x1=1590, y=H * 0.66):
    """1555 (solda yaşlı Karl) ← kırk yıl geri → 1515 (15 yaşında genç Karl). Bar sağdan sola uzar."""
    f = cx.f
    f.bg("night"); f.rays(alpha=0.3)
    sk.dust(f, cx.t, n=50)
    ko = cx.amt(at_old, 0.8)
    # çizgi + yıl işaretleri
    f.line(x0, y, x1, y, color="#C9962B", sw=3, alpha=0.7 * ko)
    for yr in range(1515, 1556, 5):
        x = lerp(x0, x1, (yr - 1515) / 40.0)
        big = yr in (1515, 1555)
        f.line(x, y - (16 if big else 9), x, y + (16 if big else 9), color="#C9962B", sw=2.6 if big else 1.6, alpha=0.8 * ko)
    f.text("1555", x1, y + 70, face="title_m", size=36, color="#F0DDA0", align="c", track=5, alpha=ko, shadow=(2, 2, 3, "#000000"))
    kk = ease_out(clamp((cx.t - cx.at(at_back)) / 1.7), 2.4)
    kyg = cx.amt(at_young, 0.8)
    f.text("1515", x0, y + 70, face="title_m", size=36, color="#F0DDA0", align="c", track=5, alpha=cx.amt(at_back, 0.6) * 1.0, shadow=(2, 2, 3, "#000000"))
    if kk > 0:
        xb = x1 - (x1 - x0) * kk
        f.rrect(xb, y - 12, x1 - xb, 24, 12, color="#C0392B", alpha=0.65)
        f.rrect(xb, y - 12, x1 - xb, 24, 12, style="stroke", sw=2, color="#FFB0A0", alpha=0.6)
        mid = (xb + x1) / 2
        if kk > 0.25:
            SH.gold_flat(f, "40 YIL", (x0 + x1) / 2, y - 76, face="title", size=104, track=8, alpha=smooth((kk - 0.25) / 0.5))
    # medalyonlar
    if ko > 0:
        draw_medal_plain(f, "karl_yasli", x1, y - 320, 380 * (0.92 + 0.08 * ease_out(ko)), "gold", alpha=ko, t=cx.t, i=0)
        f.line(x1, y - 124, x1, y, color="#C9962B", sw=2, alpha=0.5 * ko)
    if kyg > 0:
        draw_medal_plain(f, "karl_genc", x0, y - 320, 380 * (0.92 + 0.08 * ease_out(kyg)), "gold", alpha=kyg, t=cx.t, i=1)
        f.line(x0, y - 124, x0, y, color="#C9962B", sw=2, alpha=0.5 * kyg)
        nplate(f, "15 YAŞINDA", None, cx_=x0, y=y - 320 + 200, t=cx.amt(at_young, 0.6, off=0.25), size=36, min_w=300)
        kcr = cx.amt(at_crown, 0.7)
        if kcr > 0:
            icons.draw_icon(f, "crown", x0 + 150, y - 320 - 150, size=100 * (0.8 + 0.2 * back_out(kcr)), metal="gold", alpha=kcr, glow=0.35)
    f.vig(0.58)


# ───────────────────────────── devir şeması ─────────────────────────────
@SH.kind("c12_transfer")
def k_c12_transfer(cx, at_r1=0.0, at_r2=0.0, at_r3=0.0, at_dates=(0.0, 0.0, 0.0), at_who3=None, at_title=None):
    f = cx.f
    f.bg("night"); f.rays(alpha=0.28)
    sk.dust(f, cx.t, n=45)
    # sol: Şarlken
    kk = cx.amt(0.0, 0.8)
    kx, ky = 330, H * 0.5
    draw_medal_plain(f, "karl_yasli", kx, ky, 400 * (0.94 + 0.06 * ease_out(kk)), "gold", alpha=kk, t=cx.t, i=0)
    nplate(f, "ŞARLKEN", None, cx_=kx, y=ky + 226, t=cx.amt(0.3, 0.6), size=40, min_w=300)
    rows = [
        dict(at=at_r1, y=H * 0.275, icon="castle", title="HOLLANDA", key="felipe2", who="FELİPE", date="25 EKİM 1555  ·  ŞİMDİ", dt=at_dates[0], whoat=at_r1),
        dict(at=at_r2, y=H * 0.5, icon="shield", title="İSPANYA", key="felipe2", who="FELİPE", date="OCAK 1556", dt=at_dates[1], whoat=at_r2),
        dict(at=at_r3, y=H * 0.725, icon="imperial_crown", title="İMPARATORLUK UNVANI", key="ferdinand", who="FERDİNAND", date="1556 – 1558", dt=at_dates[2], whoat=(at_who3 if at_who3 is not None else at_r3)),
    ]
    for ri, r in enumerate(rows):
        k = cx.amt(r["at"], 0.7)
        if k <= 0:
            continue
        x0, w, h = 610, 1210, 150
        yy = r["y"] - h / 2
        # ok: Karl'dan karta
        ka = ease_out(clamp((cx.t - cx.at(r["at"])) / 0.9), 2.4)
        ax0, ax1 = kx + 215, x0 - 8
        ay0, ay1 = ky + (r["y"] - ky) * 0.15, r["y"]
        p = skia.Path(); p.moveTo(ax0, ay0); p.cubicTo(ax0 + 90, ay0, ax1 - 90, ay1, ax1, ay1)
        pm = skia.PathMeasure(p, False); part = skia.Path(); pm.getSegment(0, pm.getLength() * ka, part, True)
        f.path(part, style="stroke", sw=9, color="#000000", alpha=0.4)
        f.path(part, style="stroke", sw=3.6, color="#E3B54A", alpha=0.95)
        SH.plate(f, x0, yy, w, h, alpha=k)
        icons.draw_icon(f, icn(r["icon"], "shield"), x0 + 86, r["y"], size=104, metal="gold", alpha=k, glow=0.2, shadow=False)
        tsz = SH.fit_size(r["title"], "title_m", 38, 560, 6)
        f.text(r["title"], x0 + 168, r["y"] + 8, face="title_m", size=tsz, color="#F3DE9A", align="l", track=6, alpha=k, shadow=(2, 2, 3, "#000000"))
        kd = cx.amt(r["dt"], 0.6)
        if kd > 0:
            f.text(r["date"], x0 + 168, r["y"] + 52, face="cap_b", size=28, color="#CDB97F", align="l", track=2, alpha=kd)
        # alıcı madalya (sağ uç)
        kw = cx.amt(r["whoat"], 0.7)
        if kw > 0:
            mx = x0 + w - 100
            draw_medal_plain(f, r["key"], mx, r["y"], 150 * (0.9 + 0.1 * ease_out(kw)), "gold", alpha=kw, t=cx.t, i=ri + 2, glint=False)
            f.text(r["who"], mx - 100, r["y"] + 10, face="title_m", size=30, color="#F0DDA0", align="r", track=5, alpha=kw, shadow=(2, 2, 3, "#000000"))
            f.line(x0 + 168 + 640, r["y"], mx - 200, r["y"], color="#C9962B", sw=1.2, alpha=0.0)
    f.vig(0.58)


# ───────────────────────────── nedenler ─────────────────────────────
def crack_pts(cx_, cy_, r, seed=3, n=9):
    rs = np.random.RandomState(seed)
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append((cx_ + (rs.rand() - 0.5) * r * 0.55 + math.sin(t * 5) * r * 0.08, cy_ - r * 1.05 + t * r * 2.1))
    return pts


def _crack(f, cx_, cy_, r, k, seed=3, color="#0A0604", glow="#FFD58A", sw=7):
    """Küreyi/sikkeyi boydan boya çatlatan çizgi (k: 0..1 ilerleme)."""
    pts = crack_pts(cx_, cy_, r, seed)
    path = sk.poly_path(pts, False)
    pm = skia.PathMeasure(path, False)
    part = skia.Path()
    pm.getSegment(0, pm.getLength() * clamp(k), part, True)
    f.path(part, style="stroke", sw=sw + 8, color=glow, alpha=0.5, blur=6)
    f.path(part, style="stroke", sw=sw, color=color, alpha=0.95, join="miter")
    f.path(part, style="stroke", sw=2, color=glow, alpha=0.7)
    if k > 0.4:                     # yan çatlaklar
        for j, (sx, sy, ex, ey) in enumerate(((0.0, -0.1, -0.45, 0.05), (0.05, 0.25, 0.5, 0.4), (-0.05, 0.55, -0.4, 0.7))):
            kk = clamp((k - 0.4 - 0.15 * j) / 0.35)
            if kk > 0:
                f.line(cx_ + sx * r, cy_ + sy * r, cx_ + lerp(sx, ex, kk) * r, cy_ + lerp(sy, ey, kk) * r, color=color, sw=sw * 0.55, alpha=0.9, join="miter")


@SH.kind("c12_reason")
def k_c12_reason(cx, which="gut", at_kick=0.0, at_stamp=None, at_w1=0.0, at_w2=None, at_crack=None, at_icon=0.0):
    f = cx.f
    f.bg("night"); f.rays(alpha=0.32)
    sk.dust(f, cx.t, n=55)
    kk = cx.amt(at_kick, 0.8)
    kick_rule(f, "TARİHÇİLERİN SAYDIĞI NEDENLER", W / 2, 180, k=kk, size=30, track=14, span=110)
    ki = cx.amt(at_icon, 0.9)
    cxm, cym = W / 2, 520
    if which == "gut":
        glow_dot(f, cxm, cym, 420, "#E3B54A", 0.4 * ki)
        icons.draw_icon(f, icn("foot_gout", "hourglass"), cxm - 210, cym, size=340 * (0.9 + 0.1 * ease_out(ki)), metal="gold", alpha=ki, glow=0.35)
        icons.draw_icon(f, "hourglass", cxm + 230, cym + 10, size=270 * (0.9 + 0.1 * ease_out(ki)), metal="bronze", alpha=ki * cx.amt(at_w2 if at_w2 is not None else at_w1, 0.8), glow=0.2)
        k1 = cx.amt(at_w1, 0.6)
        k2 = cx.amt(at_w2 if at_w2 is not None else at_w1, 0.6, off=0.0)
        f.text("GUT", cxm - 210, cym + 262, face="title", size=64, color="#F4DD92", align="c", track=12, alpha=k1, shadow=(2, 3, 4, "#000000"))
        f.text("YORGUNLUK", cxm + 230, cym + 262, face="title", size=64, color="#F4DD92", align="c", track=12, alpha=k2, shadow=(2, 3, 4, "#000000"))
    else:
        R = 205
        cym = 590
        glow_dot(f, cxm, cym, 470, "#E3B54A", 0.4 * ki)
        kc = ease_out(clamp((cx.t - cx.at(at_crack)) / 1.1), 2.2) if at_crack is not None else 0.0
        ksplit = smooth((cx.t - cx.at(at_crack) - 0.9) / 1.3) if at_crack is not None else 0.0
        pts = crack_pts(cxm, cym, R, 3)
        gsz = R * (0.9 + 0.1 * ease_out(ki))
        for side in (-1, 1):
            f.c.save()
            f.c.translate(cxm + side * ksplit * 30, cym + (ksplit * 12 if side > 0 else -ksplit * 4))
            f.c.rotate(side * ksplit * 4.5)
            f.c.translate(-cxm, -cym)
            edge = [(W if side > 0 else 0, -50)] + pts + [(W if side > 0 else 0, H + 50)]
            f.c.clipPath(sk.poly_path(edge, True), skia.ClipOp.kIntersect, True)
            D.draw_globe(f, cxm, cym, gsz, rot=cx.t * 0.25, alpha=ki, glow=0.0)
            f.c.restore()
        kcr = cx.amt(A("c12s6", "Hıristiyan", -0.1), 0.7)
        if kcr > 0:
            icons.draw_icon(f, "cross", cxm, cym - R - 78, size=150 * (0.8 + 0.2 * back_out(kcr)), metal="gold", alpha=kcr, glow=0.3)
        if kc > 0 and ksplit < 0.05:
            _crack(f, cxm, cym, R, kc)
        k1 = cx.amt(at_w1, 0.7)
        f.text("EVRENSEL İMPARATORLUK", cxm, cym + R + 112, face="title", size=56, color="#F4DD92", align="c", track=10, alpha=k1 * (1 - 0.5 * ksplit), shadow=(2, 3, 4, "#000000"))
    if at_stamp is not None:
        SH.stamp(f, "YORUM", W * 0.80, 330, rot=-0.12, size=62, t=cx.amt(at_stamp, 0.3))
    f.vig(0.6)


# ───────────────────────────── çatlayan sikke ─────────────────────────────
@SH.kind("c12_crackcoin")
def k_c12_crackcoin(cx, at_med=0.0, at_war=0.0, at_crack=0.0, at_broke=0.0):
    f = cx.f
    f.bg("night"); f.rays(alpha=0.3)
    sk.dust(f, cx.t, n=55)
    km = cx.amt(at_med, 0.8)
    mx, my = W * 0.285, H * 0.47
    if km > 0:
        draw_medal_plain(f, "felipe2", mx, my, 520 * (0.93 + 0.07 * ease_out(km)) * (1 + 0.03 * cx.u), "gold", alpha=km, t=cx.t)
        nplate(f, "FELİPE", None, cx_=mx, y=my + 290, t=cx.amt(at_med, 0.6, off=0.4), size=44, min_w=320)
    kw = cx.amt(at_war, 0.8)
    cxr, cyr = W * 0.69, H * 0.46
    if kw > 0:
        icons.draw_icon(f, "swords", cxr, cyr - 6, size=600 * (0.9 + 0.1 * ease_out(kw)), metal="bronze", alpha=0.5 * kw, rot=0.0, shadow=False)
    kc = cx.amt(at_war, 0.9)
    if kc > 0:
        kb = cx.amt(at_broke, 1.0)
        glow_dot(f, cxr, cyr, 330, "#E3B54A", 0.35 * kc * (1 - 0.6 * kb))
        icons.draw_icon(f, "coin", cxr, cyr, size=440 * (0.9 + 0.1 * ease_out(kc)), metal="gold" if kb < 0.5 else "bronze", alpha=kc, glow=0.3 * (1 - kb))
        kcr = ease_out(clamp((cx.t - cx.at(at_crack)) / 0.9), 2.4)
        if kcr > 0:
            _crack(f, cxr, cyr, 215, kcr, seed=8, sw=9)
    f.text("SAVAŞTA", cxr, cyr - 300, face="title", size=58, color="#F4DD92", align="c", track=12, alpha=cx.amt(at_war, 0.6), shadow=(2, 3, 4, "#000000"))
    f.text("İFLASA YAKIN", cxr, cyr + 320, face="title", size=58, color="#E8A08A", align="c", track=10, alpha=cx.amt(at_crack, 0.6), shadow=(2, 3, 4, "#000000"))
    f.vig(0.6)


# ───────────────────────────── mum (prosedürel) ─────────────────────────────
def candle_draw(f, x, yb, h=320, w=46, flame=1.0, t=0.0, glow=1.0, seed=0.0, alpha=1.0):
    top = yb - h
    f.rrect(x - w / 2, top, w, h, 9, shader=f.lin(x - w / 2, 0, x + w / 2, 0, [("#8F7A4E", 0.0), ("#F3E6BC", 0.4), ("#E3D2A0", 0.7), ("#7E6A40", 1.0)]), alpha=alpha)
    for dx, dl in ((-0.28, 0.20), (0.20, 0.32), (0.36, 0.14)):
        f.rrect(x + dx * w - 5, top - 2, 10, h * dl, 5, color="#F8EDCB", alpha=0.9 * alpha)
    f.oval(x, top, w / 2, 7, color="#FFF6D6", alpha=alpha)
    f.line(x, top, x, top - 16, color="#2A1A0C", sw=3, alpha=alpha)
    f.rrect(x - w * 0.95, yb - 4, w * 1.9, 16, 6, color="#B88A3A", alpha=alpha)
    f.rrect(x - w * 0.55, yb + 10, w * 1.1, 90, 6, color="#8A6A2A", alpha=alpha)
    if flame > 0.01:
        fy = top - 14
        fl = flame * (0.92 + 0.08 * math.sin(t * 11 + seed) + 0.04 * math.sin(t * 23 + seed * 2))
        sway = math.sin(t * 7 + seed) * 3.5 * flame
        glow_dot(f, x, fy - 36 * fl, 330 * fl * glow, "#FFB347", 0.55 * flame * alpha)
        glow_dot(f, x, fy - 36 * fl, 110 * fl * glow, "#FFE7A0", 0.85 * flame * alpha)
        p = skia.Path()
        p.moveTo(x, fy)
        p.cubicTo(x - 21 * fl, fy - 14 * fl, x - 12 * fl, fy - 54 * fl, x + sway, fy - 92 * fl)
        p.cubicTo(x + 15 * fl, fy - 54 * fl, x + 21 * fl, fy - 14 * fl, x, fy)
        f.path(p, shader=f.lin(x, fy - 92 * fl, x, fy, [("#FFF6D0", 0.0), ("#FFC45A", 0.5), ("#E0701A", 1.0)]), alpha=alpha)
        q = skia.Path()
        q.moveTo(x, fy - 2)
        q.cubicTo(x - 8 * fl, fy - 10 * fl, x - 5 * fl, fy - 28 * fl, x + sway * 0.5, fy - 40 * fl)
        q.cubicTo(x + 6 * fl, fy - 28 * fl, x + 8 * fl, fy - 10 * fl, x, fy - 2)
        f.path(q, color="#FFFFFF", alpha=0.85 * alpha)


# ───────────────────────────── rivayet: hayaletimsi tabut ─────────────────────────────
@SH.kind("c12_rumor")
def k_c12_rumor(cx, at_coffin=0.0, at_fig=0.0, at_stamp=0.0):
    """'Tabutuna yatıp cenazesini prova etti' — yalnız rivayet: soğuk, kesik çizgili hayalet tabut (kanıtsız), yanında iki mum."""
    f = cx.f
    f.bg("night")
    f.rect(0, 0, W, H, color="#0E1C2A", alpha=0.35)
    f.rays(alpha=0.22)
    sk.dust(f, cx.t, n=50, color="#BFD0DC", alpha=0.35)
    k = cx.amt(at_coffin, 1.0)
    cxm, cym = W / 2, H * 0.55
    for sx, seed in ((-1, 0.3), (1, 2.1)):
        candle_draw(f, cxm + sx * 640, cym + 300, h=330, flame=1.0, t=cx.t, glow=0.8, seed=seed, alpha=0.9 * k)
    sc_ = 1.28
    pts = [(cxm + dx * sc_, cym + dy * sc_) for dx, dy in ((-340, -62), (-340, 62), (200, 104), (345, 44), (345, -44), (200, -104))]
    path = sk.poly_path(pts, True)
    f.path(path, shader=f.lin(0, cym - 104, 0, cym + 104, [("#2A3A4A", 0.0, int(160 * k)), ("#101822", 1.0, int(210 * k))]))
    p = f.paint("#9FB8C8", style="stroke", sw=3.4, alpha=0.85 * k)
    p.setPathEffect(skia.DashPathEffect.Make([16, 11], -cx.t * 22))
    f.c.drawPath(path, p)
    # iç çerçeve
    inner = sk.poly_path([(cxm + (px - cxm) * 0.88, cym + (py - cym) * 0.78) for px, py in pts], True)
    p2 = f.paint("#9FB8C8", style="stroke", sw=1.6, alpha=0.45 * k)
    p2.setPathEffect(skia.DashPathEffect.Make([8, 8], cx.t * 14))
    f.c.drawPath(inner, p2)
    icons.draw_icon(f, "cross", cxm - 150, cym, size=150, metal="silver", alpha=0.55 * k, shadow=False)
    # yatan hayalet figür (kesik çizgili siluet)
    kf = cx.amt(at_fig, 1.0)
    if kf > 0:
        fig = skia.Path()
        fig.addOval(skia.Rect.MakeLTRB(cxm + 208 * sc_, cym - 36 * sc_, cxm + 282 * sc_, cym + 36 * sc_))
        fig.addRoundRect(skia.Rect.MakeLTRB(cxm - 250 * sc_, cym - 34 * sc_, cxm + 215 * sc_, cym + 34 * sc_), 30, 30)
        pf = f.paint("#E8D8A0", style="stroke", sw=2.6, alpha=0.85 * kf)
        pf.setPathEffect(skia.DashPathEffect.Make([7, 8], -cx.t * 16))
        f.c.drawPath(fig, pf)
        f.path(fig, color="#E8D8A0", alpha=0.07 * kf)
    icons.draw_icon(f, "question", cxm + 20, cym - 270, size=190, metal="silver", alpha=0.7 * cx.amt(at_fig, 0.8), glow=0.2)
    SH.stamp(f, "RİVAYET", cxm, cym + 290, rot=-0.07, size=88, t=cx.amt(at_stamp, 0.3))
    f.vig(0.66)
