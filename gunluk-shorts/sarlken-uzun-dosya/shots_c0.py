"""Bölüm 0 (soğuk açılış) özel çekim türleri. Ad öntek: c0_."""
import math

import numpy as np
import skia

import d_common as D
import icons
import shots as SH
import sk
from d_common import A, glow_dot, kick_rule, ring_pulse, tag
from sk import W, H, back_out, clamp, ease_io, ease_out, lerp, mix, smooth


# ───────────────────────────── kırk yıl: kum saati + sayaç ─────────────────────────────
@SH.kind("c0_forty")
def k_c0_forty(cx, at_num=0.0, at_unit=0.0, count_dur=0.55, value=40, unit="YIL", fill_to=0.58):
    """Solda kum saati (kum akıyor), sağda '40' ('kırk' sözünde sayar, kısa sürede oturur) + 'YIL' ('yıldır' sözünde)."""
    f = cx.f
    f.bg("night"); f.rays(alpha=0.32)
    sk.dust(f, cx.t, n=50)
    k_in = smooth(clamp(cx.t / 0.6))
    hx, hy, hh = 640, H * 0.50, 560
    glow_dot(f, hx, hy, hh * 0.95, "#FFC46E", 0.20 * k_in)
    D.draw_hourglass(f, hx, hy, h=hh * (0.96 + 0.04 * k_in), fill_bottom=fill_to * clamp(cx.u), alpha=k_in, glass_a=0.34)
    # sayaç
    nx, ny, size = 1290, H * 0.5, 330
    t_n = cx.at(at_num)
    a = cx.amt(at_num, 0.35)
    k = ease_out(clamp((cx.t - t_n) / count_dur), 3)
    if a > 0:
        glow_dot(f, nx, ny + 10, 430, "#E3B54A", 0.20 * a)
        sc = 1.0 + 0.05 * (1 - k)
        f.c.save(); f.c.translate(nx, ny); f.c.scale(sc, sc); f.c.translate(-nx, -ny)
        SH.gold_flat(f, SH.fmt_int(value * k), nx, ny + size * 0.3, face="title", size=size, track=6, alpha=a)
        f.c.restore()
        ring_pulse(f, nx, ny, t_n + count_dur * 0.8, cx.t, r0=120, r1=330, dur=1.0, color="#FFE7A0", sw=3, a=0.7)
    ku = cx.amt(at_unit, 0.45)
    if ku > 0:
        f.text(unit, nx, ny + size * 0.3 + 92, face="title_m", size=58, color="#E8CF8A", align="c", track=18, alpha=ku, shadow=(2, 2, 3, "#000000"))
    f.vig(0.6)


# ───────────────────────────── beş cephe ─────────────────────────────
FRONTS = [("coinbag", "BANKACI", "I"), ("monk", "KEŞİŞ", "II"), ("crown", "KRAL", "III"), ("crescent", "SULTAN", "IV"), ("family", "MİRAS", "V")]


@SH.kind("c0_fronts")
def k_c0_fronts(cx, at_title=0.0, at_slots=0.0, words=(), at_all=None, size=205, y=H * 0.52, gap=300):
    """Beş yuva (kesikli halka) → her cephe kendi sözcüğünde yuvaya oturur. words: 5 çapa. at_all: hepsinin birlikte parladığı an."""
    f = cx.f
    f.bg("night"); f.rays(alpha=0.34)
    sk.dust(f, cx.t, n=55)
    x0 = W / 2 - gap * 2
    kt = cx.amt(at_title, 0.8)
    kick_rule(f, "BEŞ CEPHE", W / 2, 215, k=kt, size=40, track=22, span=170)
    ks = cx.amt(at_slots, 0.8)
    # bağlayan ince çizgi (yuvalar arası), her cephe oturdukça uzar
    kk = [cx.amt(w, 0.55, off=-0.2) for w in words]
    n_in = sum(1 for k in kk if k > 0)
    prog = 0.0
    for i in range(4):
        prog += clamp(kk[i + 1] * 1.0) if kk[i + 1] > 0 else 0
    if ks > 0:
        f.line(x0, y, x0 + gap * min(4.0, prog), y, color="#C9962B", sw=2.2, alpha=0.65 * ks)
    pall = cx.amt(at_all, 1.2) if at_all is not None else 0.0
    for i, (ic, label, num) in enumerate(FRONTS):
        x = x0 + i * gap
        k = kk[i]
        if ks > 0:
            f.c.save()
            p = f.paint("#C9962B", style="stroke", sw=2.5, alpha=0.55 * ks * (1 - 0.85 * k))
            p.setPathEffect(skia.DashPathEffect.Make([10, 9], -cx.t * 18))
            f.c.drawCircle(x, y, size * 0.62, p)
            f.c.restore()
            f.text(num, x, y - size * 0.80, face="title_m", size=34, color="#B9A674", align="c", track=4, alpha=0.8 * ks)
        if k > 0:
            sc = 0.7 + 0.3 * back_out(k)
            glow_dot(f, x, y, size * 0.9, "#F0D27A", 0.35 * k + 0.35 * pall)
            icons.draw_icon(f, ic, x, y - 12 * (1 - k), size=size * sc * (1.0 + 0.06 * pall * math.sin(cx.t * 5 + i)), metal="gold", alpha=k, glow=0.25 + 0.3 * pall)
            f.text(label, x, y + size * 0.86, face="title_m", size=32, color="#F0DDA0", align="c", track=7, alpha=k, shadow=(2, 2, 3, "#000000"))
            ring_pulse(f, x, y, cx.at(words[i], off=-0.2), cx.t, r0=size * 0.4, r1=size * 0.95, dur=0.9, color="#FFE7A0", sw=3, a=0.8)
    f.vig(0.55)


# ───────────────────────────── taç borçla alındı ─────────────────────────────
@SH.kind("c0_borc")
def k_c0_borc(cx, at_coins=0.0, at_big=0.0, at_stamp=0.0, at_crown=0.0):
    """Taç; üstüne yağan sikkeler; 'BÜYÜK ÖLÇÜDE' + BORÇLA damgası."""
    f = cx.f
    f.bg("night"); f.rays(alpha=0.42)
    sk.dust(f, cx.t, n=60)
    kc = cx.amt(at_crown, 0.8)
    cx0, cy0 = W / 2, H * 0.50
    glow_dot(f, cx0, cy0, 420, "#E3B54A", 0.5 * kc)
    icons.draw_icon(f, "imperial_crown", cx0, cy0 + math.sin(cx.t * 1.3) * 5, size=440 * (0.92 + 0.08 * ease_out(kc)), metal="gold", alpha=kc, glow=0.4 * kc)
    rs = np.random.RandomState(11)
    t0 = cx.at(at_coins)
    for i in range(22):
        px = cx0 + (rs.rand() - 0.5) * 560
        dur = 0.75 + rs.rand() * 0.4
        sz = 62 + rs.rand() * 34
        spin = (rs.rand() - 0.5) * 10
        ti = t0 + 0.075 * i
        k = (cx.t - ti) / dur
        if k <= 0 or k >= 1.25:
            continue
        yy = lerp(-90, cy0 - 60 + (rs.rand() - 0.5) * 60, clamp(k) ** 1.7)
        a = 1.0 if k < 1 else clamp(1 - (k - 1) / 0.25)
        kind_ = "coins" if i % 4 == 0 else "coin"
        icons.draw_icon(f, kind_, px, yy, size=sz, metal="gold", alpha=a, rot=spin * k, glow=0.15, shadow=False)
        if 0.95 < k < 1.2:
            glow_dot(f, px, yy, 60, "#FFE7A0", 0.7 * (1 - (k - 0.95) / 0.25))
    kb = cx.amt(at_big, 0.6)
    if kb > 0:
        kick_rule(f, "BÜYÜK ÖLÇÜDE", W / 2, H * 0.70, k=kb, size=36, track=18, span=150)
    SH.stamp(f, "BORÇLA", W / 2, H * 0.80, rot=-0.10, size=104, t=cx.amt(at_stamp, 0.3))
    f.vig(0.58)
