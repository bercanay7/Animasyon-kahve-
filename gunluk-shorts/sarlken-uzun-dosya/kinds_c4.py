"""Bölüm 4 (Worms'ta Bir Keşiş) — özel çekim türleri. Hepsi `c4_` önekli.

Ton: yargı salonu — petrol (Protestan) ↔ kırmızı (Habsburg); gerilim, mum ışığı.
"""
import math

import numpy as np
import skia

import icons
import shots as SH
import sk
from bw_lib import (INK, anc, backdrop, big_gold, curve_arrow, duo_glow, fadeout, glow, paper, plate_text, push, reveal, scribbles,
                    shift, spot, stamp2, strike, tag)
from sk import C, H, W, back_out, clamp, ease_io, ease_out, lerp, mix, smooth

PETROL = "#1E5560"
PETROL_L = "#3F8C96"
CRIM = "#8E1F26"
CRIM_L = "#C0392B"


# ───────────────────────────── ikili: Karl ↔ Luther ─────────────────────────────
@SH.kind("c4_duel")
def k_duel(cx, left=None, right=None, vs_at=0.6, size=560, y=H * 0.46, tint_a=0.34, age_at=None):
    """İki madalya karşı karşıya; sol Habsburg kırmızısı, sağ Protestan petrolü ışığı. left/right: dict(key,name,role,at,metal,flip)."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.28)
    duo_glow(f, CRIM, PETROL, a=tint_a, y=y)
    gap = 650
    for i, it in enumerate((left, right)):
        x = W / 2 + (-gap / 2 if i == 0 else gap / 2)
        a = cx.amt(it.get("at", 0.2), 0.8)
        slide = (1 - ease_out(a)) * (-140 if i == 0 else 140)
        sc = (0.93 + 0.07 * ease_out(a)) * (1.0 + 0.035 * cx.u)
        gl = (cx.t * 0.25 + 0.2 * i) % 2.0
        SH.draw_medal(f, it["key"], x + slide, y, size * sc, it.get("metal", "gold"), it.get("flip", False), alpha=a,
                      tilt=(0.22 if i == 0 else -0.22) * math.sin(cx.t * 0.5 + i) + (0.12 if i == 0 else -0.12), glint=(gl if gl < 1 else None))
        pa = cx.amt(it.get("plate_at", shift(it.get("at", 0.2), 0.5)), 0.6)
        if pa > 0:
            SH.name_plate(f, it["name"], it.get("role"), it.get("dates"), cx_=x, y=y + size * 0.53, t=pa, w=min(gap - 40, 560))
    # aradaki kılıçlar
    k = cx.amt(vs_at, 0.45)
    if k > 0:
        glow(f, W / 2, y, 170, "#FFE2A0", 0.35 * k)
        icons.draw_icon(f, "swords", W / 2, y, size=150 * (0.7 + 0.3 * back_out(k)), metal="silver", alpha=k, glow=0.25)
    sk.dust(f, cx.t, n=55)
    f.vig(0.58)


# ───────────────────────────── 95 madde ─────────────────────────────
@SH.kind("c4_theses")
def k_theses(cx, at=0.0, year_at=0.4, against_at=2.0, slash_at=2.9, count_at=3.2, write_at=3.8, write_dur=2.2):
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.28)
    duo_glow(f, PETROL, "#6B3F1E", a=0.22, y=H * 0.55)
    a = cx.amt(at, 0.8)
    with push(cx, 1.0, 1.05, pan=(-30, 0)):
        # parşömen (solda), alttan süzülerek girer
        yy = H * 0.52 + (1 - ease_out(a)) * 160
        with paper(f, 640, yy, 800, 880, rot=-0.025, alpha=a, seed=11):
            hk = cx.amt(count_at, 0.5)
            reveal(f, "95 MADDE", 0, -440 + 118, clamp((cx.t - cx.at(count_at)) / 0.8), face="fell", size=70, align="c", alpha=a)
            f.line(-250, -440 + 140, 250, -440 + 140, color=INK, sw=2, alpha=0.55 * a * hk)
            wp = clamp((cx.t - cx.at(write_at)) / write_dur)
            scribbles(f, -330, -440 + 215, 300, 15, prog=clamp(wp * 2.0), seed=4, line_h=44, thick=6.4, alpha=0.66 * a)
            scribbles(f, 30, -440 + 215, 300, 15, prog=clamp(wp * 2.0 - 1.0), seed=9, line_h=44, thick=6.4, alpha=0.66 * a)
            # numaralar
            for r in range(15):
                if wp * 2.0 * 15 > r:
                    f.text(str(r + 1), -352, -440 + 223 + r * 44, face="fell_i", size=24, color=INK, align="r", alpha=0.55 * a)
        # kuğu tüyü kalemi yazarken ilerler
        if 0 < wp < 1:
            col = 0 if wp < 0.5 else 1
            u = (wp * 2.0 if col == 0 else wp * 2.0 - 1.0)
            row = min(14.0, u * 15)
            qx = 640 + (-330 if col == 0 else 30) + 300 * ((row % 1.0))
            qy = yy - 440 + 215 + int(row) * 44
            icons.draw_icon(f, "quill", qx + 60, qy - 36, size=120, metal="gold", alpha=a, rot=0.45, shadow=True)
    # sağ panel: günah affı satışı ↔ yasak
    ka = cx.amt(against_at, 0.6)
    if ka > 0:
        px = 1430
        glow(f, px, 330, 220, "#FFB347", 0.18 * ka)
        icons.draw_icon(f, "scroll", px - 100, 330, size=190, metal="ivory", alpha=ka, rot=-0.12)
        icons.draw_icon(f, "coins", px + 100, 350, size=170, metal="gold", alpha=ka, rot=0.08)
        sl = cx.amt(slash_at, 0.4)
        if sl > 0:
            icons.draw_icon(f, "b_forbid", px, 340, size=290 * (1.15 - 0.15 * ease_out(sl)), metal="crimson", alpha=sl, glow=0.25)
        f.text("GÜNAH AFFI SATIŞI", px, 520, face="title_m", size=34, color="#E7D5A0", align="c", track=6, alpha=ka, shadow=(2, 3, 3, "#000000"))
    # büyük sayaç
    kc = clamp((cx.t - cx.at(count_at)) / 1.1)
    if kc > 0:
        v = int(round(95 * ease_out(kc, 2.2)))
        big_gold(f, str(v), 1430, 800, size=250, alpha=smooth(kc * 3), track=6, glow_a=0.15)
        f.text("MADDE", 1430, 878, face="title_m", size=46, color="#E0C682", align="c", track=14, alpha=cx.amt(count_at, 0.5, off=0.35))
    # tarih notu
    ya = cx.amt(year_at, 0.7)
    f.vig(0.58)
    # üst sol: 'DÖRT YIL ÖNCE · 1517' (HUD'a girmez)
    if ya > 0:
        tag(f, "DÖRT YIL ÖNCE  ·  1517", 640, 92, size=28, alpha=ya, track=7)


# ───────────────────────────── Güvenli geçiş + 21 gün ─────────────────────────────
@SH.kind("c4_safeconduct")
def k_safeconduct(cx, at=0.0, seal_at=1.6, days_at=3.0, days_dur=1.3):
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.28)
    duo_glow(f, "#6B3F1E", CRIM, a=0.2, y=H * 0.5)
    a = cx.amt(at, 0.8)
    with push(cx, 1.0, 1.05, pan=(-24, 6)):
        yy = H * 0.50 + (1 - ease_out(a)) * 130
        with paper(f, 560, yy, 840, 640, rot=-0.03, alpha=a, seed=23):
            reveal(f, "GÜVENLİ GEÇİŞ", 0, -640 / 2 + 100, clamp((cx.t - cx.at(at, off=0.3)) / 0.9), face="fell", size=58, align="c", alpha=a)
            f.line(-260, -640 / 2 + 124, 260, -640 / 2 + 124, color=INK, sw=2, alpha=0.55 * a)
            scribbles(f, -330, -640 / 2 + 190, 640, 7, prog=clamp((cx.t - cx.at(at, off=0.6)) / 1.6), seed=14, line_h=52, thick=6.6, alpha=0.62 * a)
            SH.wax_seal(f, 230, 190, 70, color="#8E1F26", t=cx.amt(seal_at, 0.35), alpha=a, mono="K")
    # takvim ızgarası: 3 sıra × 7 gün
    cols, rows = 7, 3
    cw, gap = 74, 16
    gx0 = 1040
    gy0 = 470
    ka = cx.amt(days_at, 0.6, off=-0.4)
    if ka > 0:
        f.text("GÜN", gx0 + (cols * (cw + gap) - gap) / 2, gy0 - 62, face="title_m", size=28, color="#B9A674", align="c", track=16, alpha=ka)
        for i in range(cols * rows):
            r, c = divmod(i, cols)
            x = gx0 + c * (cw + gap)
            y = gy0 + r * (cw + gap)
            k = clamp((cx.t - cx.at(days_at, off=days_dur * i / (cols * rows))) / 0.22)
            f.rrect(x, y, cw, cw, 12, color="#150D08", alpha=0.85 * ka)
            f.rrect(x, y, cw, cw, 12, style="stroke", sw=2, color="#7A5518", alpha=0.9 * ka)
            if k > 0:
                f.rrect(x + 5, y + 5, cw - 10, cw - 10, 8, shader=f.lin(x, y, x, y + cw, [("#F4DC8C", 0.0), ("#C9962B", 0.6), ("#7A5518", 1.0)]), alpha=k)
                f.text(str(i + 1), x + cw / 2, y + cw * 0.67, face="title_m", size=30, color="#2A1A0C", align="c", alpha=k)
    # büyük 21
    kc = clamp((cx.t - cx.at(days_at)) / days_dur)
    if kc > 0:
        v = int(round(21 * ease_out(kc, 1.6)))
        big_gold(f, str(max(1, v)), 1230, 330, size=250, alpha=smooth(kc * 4), track=6, glow_a=0.12)
    f.vig(0.58)
