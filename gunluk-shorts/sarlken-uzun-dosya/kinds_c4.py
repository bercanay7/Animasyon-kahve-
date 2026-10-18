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
from bw_lib import draw_medal2  # noqa: E402
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
        draw_medal2(f, it["key"], x + slide, y, size * sc, it.get("metal", "gold"), it.get("flip", False), alpha=a,
                      tilt=(0.22 if i == 0 else -0.22) * math.sin(cx.t * 0.5 + i) + (0.12 if i == 0 else -0.12), glint=(gl if gl < 1 else None))
        pa = cx.amt(it.get("plate_at", shift(it.get("at", 0.2), 0.5)), 0.6)
        if pa > 0:
            fit_plate(f, it["name"], it.get("role"), x, y + size * 0.53, w=min(gap - 40, 600), t=pa)
    # aradaki kılıçlar
    k = cx.amt(vs_at, 0.45)
    if k > 0:
        glow(f, W / 2, y, 170, "#FFE2A0", 0.35 * k)
        icons.draw_icon(f, "swords", W / 2, y, size=190 * (0.7 + 0.3 * back_out(k)), metal="silver", alpha=k, glow=0.3)
    sk.dust(f, cx.t, n=55)
    f.vig(0.58)


# ───────────────────────────── 95 madde ─────────────────────────────
def _theses_prog(cx, at, write_at, write_dur):
    """İlk satırlar yavaşça (yazılmakta olan metin), 'maddelik' sözcüğünde hızlanır."""
    t_c = cx.at(write_at)
    slow = smooth((cx.t - (cx.at(at) + 0.9)) / max(0.5, t_c - cx.at(at) - 0.9))
    fast = clamp((cx.t - t_c) / write_dur)
    return min(1.0, 0.16 * slow + 0.84 * fast)


@SH.kind("c4_theses")
def k_theses(cx, at=0.0, year_at=0.4, against_at=2.0, slash_at=2.9, count_at=3.2, write_at=3.8, write_dur=2.2):
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.28)
    duo_glow(f, PETROL, "#6B3F1E", a=0.22, y=H * 0.55)
    a = cx.amt(at, 0.8)
    with push(cx, 1.0, 1.05, pan=(-30, 0)):
        # parşömen (solda), alttan süzülerek girer
        yy = H * 0.575 + (1 - ease_out(a)) * 160
        with paper(f, 640, yy, 800, 800, rot=-0.025, alpha=a, seed=11):
            hk = cx.amt(count_at, 0.5)
            reveal(f, "95 MADDE", 0, -400 + 112, clamp((cx.t - cx.at(count_at)) / 0.8), face="fell", size=70, align="c", alpha=a)
            f.line(-250, -400 + 134, 250, -400 + 134, color=INK, sw=2, alpha=0.55 * a * hk)
            wp = _theses_prog(cx, at, write_at, write_dur)
            scribbles(f, -330, -400 + 205, 300, 14, prog=clamp(wp * 2.0), seed=4, line_h=44, thick=6.4, alpha=0.66 * a)
            scribbles(f, 30, -400 + 205, 300, 14, prog=clamp(wp * 2.0 - 1.0), seed=9, line_h=44, thick=6.4, alpha=0.66 * a)
            # numaralar
            for r in range(14):
                if wp * 2.0 * 14 > r:
                    f.text(str(r + 1), -352, -400 + 213 + r * 44, face="fell_i", size=24, color=INK, align="r", alpha=0.55 * a)
        # kuğu tüyü kalemi yazarken ilerler
        wp = _theses_prog(cx, at, write_at, write_dur)
        if 0 < wp < 1:
            col = 0 if wp < 0.5 else 1
            u = (wp * 2.0 if col == 0 else wp * 2.0 - 1.0)
            row = min(13.99, u * 14)
            qx = 640 + (-330 if col == 0 else 30) + 300 * ((row % 1.0))
            qy = yy - 400 + 205 + int(row) * 44
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
        tag(f, "DÖRT YIL ÖNCE  ·  1517", 640, 96, size=28, alpha=ya, track=7)


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
    gw = cols * (cw + gap) - gap
    gx0 = 1350 - gw / 2
    gy0 = 560
    ka = cx.amt(days_at, 0.6, off=-0.4)
    if ka > 0:
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
        big_gold(f, str(max(1, v)), 1350, 400, size=250, alpha=smooth(kc * 4), track=6, glow_a=0.12)
        f.text("GÜN", 1350, 472, face="title_m", size=46, color="#E0C682", align="c", track=18, alpha=cx.amt(days_at, 0.5, off=0.3))
    f.vig(0.58)


# ───────────────────────────── Yardımcı: isim levhası (genişliğe sığar) ─────────────────────────────
def fit_plate(f, name, role, cx_, y, w=560, t=1.0):
    """Madalya altı levha; ad metni levha genişliğine sığdırılır."""
    a = smooth(t)
    if a <= 0:
        return
    nsz = SH.fit_size(name, "title_m", 54, w - 90, 6)
    hh = 96 + (34 if role else 0)
    x0 = cx_ - w / 2
    yy = y + (1 - a) * 18
    SH.plate(f, x0, yy, w, hh, alpha=a)
    f.text(name, cx_, yy + 56, face="title_m", size=nsz, color="#F3DE9A", align="c", track=6, alpha=a, shadow=(2, 3, 3, "#000000"))
    if role:
        f.text(role, cx_, yy + 88, face="cap_i", size=28, color="#D9C795", align="c", alpha=a)


# ───────────────────────────── kitaplar masada ─────────────────────────────
_BOOKS = [  # (x, ysıra, w, h, d, renk, rot)
    (640, 0, 300, 78, 150, "#4A2A18", -0.010), (960, 0, 280, 72, 150, "#1F3F48", 0.012), (1250, 0, 250, 70, 150, "#5A1E24", -0.008),
    (690, 1, 270, 74, 140, "#2A2A1E", 0.020), (1000, 1, 300, 76, 140, "#5C3B22", -0.015), (1330, 1, 190, 66, 130, "#1F3F48", 0.010),
    (780, 2, 280, 72, 140, "#5A1E24", -0.020), (1090, 2, 240, 70, 130, "#4A2A18", 0.018),
    (880, 3, 260, 70, 130, "#1F3F48", 0.012),
]


def _books_bg(f):
    """Duvar + gotik pencere + masa (statik, bir kez pişer)."""
    import stage as ST
    f.rect(0, 0, W, H, shader=f.lin(0, 0, 0, H, [("#1B0F08", 0.0), ("#2A170C", 0.7), ("#120A05", 1.0)]))
    for r in range(11):
        f.line(0, 40 + r * 78, W, 40 + r * 78, color="#000000", sw=1.6, alpha=0.22)
    ST.gothic_window(f, 1450, 330, 250, 460, glow=("#FFEFC2", "#E7992F"), stone="#2B190C", edge="#8A6338")
    f.circle(1450, 330, 520, shader=f.rad(1450, 330, 520, [("#FFE8B0", 0.0, 90), ("#FFB347", 0.4, 40), ("#FFB347", 1.0, 0)]), blend=skia.BlendMode.kPlus)
    ST.column(f, 170, 80, 790, 80, stone="#3A2415")
    ST.column(f, 1800, 80, 790, 80, stone="#3A2415")
    # masa
    f.rect(0, 790, W, H - 790, shader=f.lin(0, 790, 0, H, [("#4A2F1A", 0.0), ("#2A190D", 0.35), ("#0F0805", 1.0)]))
    f.line(0, 790, W, 790, color="#B88A3A", sw=3, alpha=0.55)
    rs = np.random.RandomState(5)
    for _ in range(26):
        yy = 800 + rs.rand() * 270
        f.line(rs.rand() * W * 0.4, yy, rs.rand() * W * 0.6 + W * 0.4, yy + rs.randn() * 3, color="#000000", sw=1.2 + rs.rand() * 2, alpha=0.20)
    f.rect(0, 786, W, 10, color="#C58A44", alpha=0.18)


@SH.kind("c4_books")
def k_books(cx, drop_at=0.3, drop_dt=0.34, q1_at=3.5, q2_at=5.0):
    import stage as ST
    f = cx.f
    f.c.drawImage(sk.baked("c4_books_bg", _books_bg), 0, 0)
    f.rays(alpha=0.2)
    with push(cx, 1.0, 1.07, pan=(-30, 10)):
        # keşiş, masanın arkasında (ışık sağdan)
        ST.figure(f, "monk", 350, 800, 560, col="#0A0604", rim="#C58A44", face=1, sway=math.sin(cx.t * 0.9) * 0.004)
        glow(f, 1450, 700, 300, "#FFB347", 0.14)
        # kitaplar sırayla düşer
        n = len(_BOOKS)
        for i, (bx, row, bw, bh, bd, col, rot) in enumerate(_BOOKS):
            k = clamp((cx.t - cx.at(drop_at, off=i * drop_dt)) / 0.42)
            if k <= 0:
                continue
            yb = 872 - sum(_BOOKS[j][3] - 6 for j in range(n) if _BOOKS[j][1] < row and abs(_BOOKS[j][0] - bx) < 400) / max(1, 1) * 0
            base = 872 - row * 70
            off = -(1 - ease_out(k)) * 360
            shadow_a = 0.45 * k
            f.oval(bx + bw / 2 + bd * 0.28, base + 8, bw * 0.62, 20, color="#000000", alpha=shadow_a, blur=14) if row == 0 else None
            book_box(f, bx, base + off, bw, bh, bd, col, alpha=k, rot=rot)
        # mum
        flame(f, 1760, 760, s=1.6, t=cx.t, seed=3)
        f.rect(1744, 770, 32, 66, shader=f.lin(1744, 0, 1776, 0, [("#C9B890", 0.0), ("#EADCB5", 0.5), ("#9C8559", 1.0)]))
        f.rect(1736, 832, 48, 10, color="#7A5518")
        # soru işareti
        q1 = cx.amt(q1_at, 0.6)
        q2 = cx.amt(q2_at, 0.6)
        if q1 > 0:
            bob = math.sin(cx.t * 2.0) * 8
            glow(f, 960, 330 + bob, 260, "#FFD27A", 0.22 * q1 * (1 - 0.5 * q2))
            icons.draw_icon(f, "question", 960, 330 + bob, size=300 * (0.8 + 0.2 * back_out(q1)), metal="gold", alpha=q1, glow=0.35)
    # metinler (kameradan bağımsız)
    a1 = cx.amt(q1_at, 0.5) * (1 - cx.amt(q2_at, 0.35))
    if a1 > 0:
        f.text("SENİN Mİ?", 960, 140, face="title", size=84, color="#F4DD92", align="c", track=14, alpha=a1, shadow=(3, 4, 5, "#000000"))
    a2 = cx.amt(q2_at, 0.5)
    if a2 > 0:
        f.text("HEPSİ?", 960, 140, face="title", size=96, color="#F4DD92", align="c", track=20, alpha=a2, shadow=(3, 4, 5, "#000000"))
    f.vig(0.62)


from bw_lib import book_box, chain_links, draw_hourglass, flame  # noqa: E402


# ───────────────────────────── bir gün süre → Almanca / Latince → vazgeçmiyor ─────────────────────────────
@SH.kind("c4_answer")
def k_answer(cx, day_at=1.0, flip_at=3.0, de_at=4.2, la_at=5.5, hold_at=7.0):
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.3)
    duo_glow(f, PETROL, "#6B3F1E", a=0.22)
    sk.dust(f, cx.t, n=55)
    t_flip = cx.at(flip_at)
    k_flip = clamp((cx.t - t_flip) / 0.9)
    # kum saati: önce merkezde büyük, çevrilince küçülüp ortada kalır
    fl = ease_io(k_flip)
    big = 1.0 - fl
    size = lerp(430, 250, fl)
    ypos = lerp(480, 440, fl)
    fb = clamp((cx.t - cx.at(day_at)) / max(0.5, t_flip - cx.at(day_at)))  # alt hazneye akış
    fill_before = 0.05 + 0.85 * fb
    fill_after = 0.90 - 0.55 * clamp((cx.t - t_flip - 0.9) / 3.5)
    fill = fill_before if cx.t < t_flip + 0.45 else fill_after
    draw_hourglass(f, W / 2, ypos, size, fill_bottom=fill, rot=math.pi * fl, alpha=1.0)
    # "BİR GÜN" yazısı
    ka = cx.amt(day_at, 0.6) * (1 - 0.0)
    if ka > 0:
        txt_a = ka * (1 - smooth((cx.t - t_flip) / 0.6))
        if txt_a > 0:
            f.gold("BİR GÜN", W / 2, 870, face="title", size=110, track=14, alpha=txt_a, glow=0.3 * txt_a)
    # parşömenler: Almanca (sol) / Latince (sağ)
    for (label, ta, xc, seed) in (("ALMANCA", de_at, 470, 31), ("LATİNCE", la_at, 1450, 47)):
        k = cx.amt(ta, 0.7)
        if k <= 0:
            continue
        yy = 440 + (1 - ease_out(k)) * 120
        with paper(f, xc, yy, 560, 600, rot=(-0.03 if xc < W / 2 else 0.03), alpha=k, seed=seed):
            reveal(f, label, 0, -300 + 104, clamp((cx.t - cx.at(ta)) / 0.7), face="fell", size=62, align="c", alpha=k)
            f.line(-190, -300 + 128, 190, -300 + 128, color=INK, sw=2, alpha=0.55 * k)
            scribbles(f, -230, -300 + 190, 460, 8, prog=clamp((cx.t - cx.at(ta, off=0.3)) / 1.4), seed=seed, line_h=50, thick=6.4, alpha=0.62 * k)
    # vazgeçmiyor
    kh = cx.amt(hold_at, 0.5)
    if kh > 0:
        f.rect(0, H * 0.74, W, 220, shader=f.lin(0, H * 0.74, 0, H * 0.74 + 220, [("#000000", 0.0, 0), ("#000000", 0.5, int(170 * kh)), ("#000000", 1.0, 0)]))
        glow(f, W / 2, H * 0.86, 520, "#FFD27A", 0.18 * kh)
        f.gold("VAZGEÇMİYOR", W / 2, H * 0.905, face="title", size=112, track=16, alpha=kh, glow=0.4 * kh, scale=1.0 + (1 - kh) * 0.08)
    f.vig(0.6)


# ───────────────────────────── 'Ben buradayım' — rivayet / tutanakta yok / sonradan eklenmiş ─────────────────────────────
@SH.kind("c4_protocol")
def k_protocol(cx, words=(), ghost_at=4.1, rumor_at=4.4, swap_at=6.6, gap_at=7.0, add_at=8.2, stamp1_at=7.0, stamp2_at=8.3):
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.28)
    duo_glow(f, PETROL, CRIM, a=0.26)
    sk.dust(f, cx.t, n=50)
    # --- Faz A/B: alıntı kelime kelime
    swap = cx.amt(swap_at, 0.7)
    ghost = cx.amt(ghost_at, 0.8)
    qa = (1 - swap) * (1 - 0.62 * ghost)
    lines = [["Ben", "buradayım,"], ["başka", "türlü", "yapamam"]]
    if qa > 0.01:
        size = 104
        yline = [420, 560]
        wl = []
        for ln in lines:
            ws_ = [sk.text_width(w_, "cap_i", size, 0) for w_ in ln]
            wl.append(sum(ws_) + size * 0.28 * (len(ln) - 1))
        f.text("“", W / 2 - wl[0] / 2 - 110, 470, face="title", size=240, color="#C9962B", align="l", alpha=0.55 * qa)
        f.text("”", W / 2 + wl[1] / 2 + 30, 660, face="title", size=240, color="#C9962B", align="l", alpha=0.55 * qa)
        for li, ln in enumerate(lines):
            ws = [sk.text_width(w_, "cap_i", size, 0) for w_ in ln]
            sp = size * 0.28
            tot = sum(ws) + sp * (len(ln) - 1)
            x = W / 2 - tot / 2
            for w_, wd in zip(ln, ws):
                ta = None
                for (txt, anchor) in words:
                    if txt == w_:
                        ta = anchor
                k = cx.amt(ta, 0.45) if ta is not None else 1.0
                if k > 0:
                    f.text(w_, x, yline[li] + (1 - ease_out(k)) * 24, face="cap_i", size=size, color="#F1E3B8", align="l", alpha=k * qa, shadow=(2, 4, 6, "#000000"))
                x += wd + sp
        # belirsizlik: soru işareti
        if ghost > 0:
            icons.draw_icon(f, "question", 1530, 260, size=210, metal="silver", alpha=0.5 * ghost * (1 - swap), glow=0.1)
    # RİVAYET damgası
    r = cx.amt(rumor_at, 0.3)
    if r > 0 and swap < 1:
        stamp2(f, "RİVAYET", 960, 790, rot=-0.07, size=76, t=r, alpha=(1 - swap))
    # --- Faz C/D: resmî tutanak (parşömen) + boşluk + sonradan eklenen satır
    pk = swap
    if pk > 0:
        yy = 520 + (1 - ease_out(pk)) * 200
        with paper(f, 960, yy, 1240, 720, rot=-0.012, alpha=pk, seed=61, tone="#DCC896"):
            f.text("RESMÎ TUTANAK", 0, -720 / 2 + 92, face="fell", size=56, color=INK, align="c", track=4, alpha=pk)
            f.line(-330, -720 / 2 + 116, 330, -720 / 2 + 116, color=INK, sw=2, alpha=0.55 * pk)
            # satırlar (baskı gibi düzgün gri çubuklar) — ortada boşluk bırakılır
            ys = [-190, -130, -70, 50, 110, 170, 230]
            for i, y_ in enumerate(ys):
                wl = 980 - (i % 3) * 140
                f.rrect(-wl / 2, y_ - 7, wl, 11, 5, color=INK, alpha=0.30 * pk)
            # boşluk (kesikli kutu)
            ga = cx.amt(gap_at, 0.5)
            if ga > 0:
                dash = skia.DashPathEffect.Make([16, 11], 0)
                p = f.paint("#8E1F26", style="stroke", sw=3.2, alpha=0.9 * ga)
                p.setPathEffect(dash)
                f.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-520, -36, 1040, 82), 10, 10), p)
            # sonradan eklenen: farklı mürekkep (kenar notu) + işaret
            aa = cx.amt(add_at, 0.7)
            if aa > 0:
                reveal(f, "“Ben buradayım, başka türlü yapamam”", 0, 24, aa, face="fell_i", size=46, color="#3A2A6A", align="c", alpha=0.95)
                # ^ işareti
                f.line(-40, 62, -22, 40, color="#3A2A6A", sw=3.0, alpha=0.9 * aa)
                f.line(-22, 40, -4, 62, color="#3A2A6A", sw=3.0, alpha=0.9 * aa)
        s1 = cx.amt(stamp1_at, 0.3)
        if s1 > 0:
            stamp2(f, "TUTANAKTA YOK", 640, 318 if False else 760, rot=-0.10, size=62, t=s1, seed=8)
        s2 = cx.amt(stamp2_at, 0.3)
        if s2 > 0:
            stamp2(f, "SONRADAN EKLENMİŞ", 1250, 850, rot=0.07, size=58, t=s2, seed=13, color="#3A5AB5")
    f.vig(0.6)


# ───────────────────────────── ertesi sabah: imparatorun bildirisi ─────────────────────────────
def _roller(f, x, y, w, alpha=1.0):
    """Parşömen silindiri (yatay)."""
    f.rrect(x - w / 2, y - 16, w, 32, 14, shader=f.lin(0, y - 16, 0, y + 16, [("#F4DC8C", 0.0), ("#C9962B", 0.5), ("#6B4A12", 1.0)]), alpha=alpha)
    for sx in (-1, 1):
        f.circle(x + sx * (w / 2 + 6), y, 20, shader=f.rad(x + sx * (w / 2 + 6) - 5, y - 5, 26, [("#FBE9A6", 0.0), ("#B88A3A", 0.6), ("#4A3210", 1.0)]), alpha=alpha)


@SH.kind("c4_dawn_scroll")
def k_dawn_scroll(cx, at=0.0, unroll_at=0.6, read_at=1.6, seal_at=2.4):
    f = cx.f
    # şafak gökyüzü
    k = smooth(cx.t / max(0.1, cx.dur))
    f.rect(0, 0, W, H, shader=f.lin(0, 0, 0, H, [("#1B2A3A", 0.0), (mix("#6B3F2A", "#E7992F", k), 0.55), ("#120A05", 1.0)]))
    # güneş yükselir
    sy = lerp(H * 0.78, H * 0.56, ease_out(k, 2))
    glow(f, W / 2, sy, 800, "#FFC070", 0.55)
    f.circle(W / 2, sy, 120, shader=f.rad(W / 2, sy, 120, [("#FFF5D0", 0.0), ("#FFD27A", 0.7), ("#FFB347", 1.0)]))
    f.rays(alpha=0.35)
    # ufuk silueti (şehir)
    import stage as ST
    ST.skyline(f, H * 0.80, ["spire", "tower", "tower", "spire"], 0, W, 180, "#0C0705", seed=3)
    f.rect(0, H * 0.80, W, H * 0.2, color="#0C0705")
    sk.dust(f, cx.t, n=40)
    a = cx.amt(at, 0.6)
    uk = clamp((cx.t - cx.at(unroll_at)) / 1.3)
    ph = 760 * ease_out(uk, 2)       # açılan yükseklik
    y_top = 90 + (1 - ease_out(a)) * 40
    cxm, wid = 960, 760
    if a > 0:
        # kağıt gövdesi
        f.c.save()
        f.c.clipRect(skia.Rect.MakeXYWH(cxm - wid / 2 - 10, y_top, wid + 20, ph + 4))
        f.rect(cxm - wid / 2, y_top, wid, 760, shader=f.lin(cxm - wid / 2, 0, cxm + wid / 2, 0, [("#C8B07C", 0.0), ("#F0E2B8", 0.5), ("#C0A870", 1.0)]), alpha=a)
        reveal(f, "İMPARATORUN BİLDİRİSİ", cxm, y_top + 96, clamp((cx.t - cx.at(read_at)) / 0.9), face="fell", size=50, align="c", alpha=a)
        f.line(cxm - 260, y_top + 120, cxm + 260, y_top + 120, color=INK, sw=2, alpha=0.5 * a)
        scribbles(f, cxm - 300, y_top + 190, 600, 10, prog=clamp((cx.t - cx.at(read_at, off=0.4)) / 1.6), seed=77, line_h=48, thick=6.4, alpha=0.6 * a)
        f.c.restore()
        _roller(f, cxm, y_top, wid + 30, alpha=a)
        _roller(f, cxm, y_top + ph, wid + 30, alpha=a)
        SH.wax_seal(f, cxm + 250, y_top + ph - 90, 62, color="#8E1F26", t=cx.amt(seal_at, 0.35), alpha=a, mono="K")
    f.vig(0.6)


# ───────────────────────────── atalar: üç niş + Roma anahtarları ─────────────────────────────
def _arcade_bg(f):
    import stage as ST
    f.rect(0, 0, W, H, shader=f.lin(0, 0, 0, H, [("#1B0F08", 0.0), ("#2B1A0F", 0.6), ("#0F0805", 1.0)]))
    for r in range(12):
        f.line(0, 30 + r * 78, W, 30 + r * 78, color="#000000", sw=1.6, alpha=0.22)
    for cxm in (450, 960, 1470):
        ST.arch(f, cxm, 905, 380, 600, stone="#4A3220", edge="#9A7340", glow=("#2A1608", "#573314"), thick=38)
    f.rect(0, 905, W, H - 905, shader=f.lin(0, 905, 0, H, [("#3A2415", 0.0), ("#0F0805", 1.0)]))
    f.line(0, 905, W, 905, color="#B88A3A", sw=2.5, alpha=0.5)
    for cxm in (450, 960, 1470):    # kaide kaideli taban
        f.rrect(cxm - 190, 880, 380, 34, 8, color="#5A3E24")
    for xx in (190, 705, 1215, 1730):
        ST.column(f, xx, 220, 880, 52, stone="#3A2415")


@SH.kind("c4_ancestors")
def k_ancestors(cx, ger_at=0.0, esp_at=0.0, bur_at=0.0, keys_at=0.0, chain_at=0.0):
    f = cx.f
    f.c.drawImage(sk.baked("c4_arcade_bg", _arcade_bg), 0, 0)
    f.rays(alpha=0.18)
    with push(cx, 1.0, 1.05, pan=(0, 10)):
        items = [(450, ger_at, "eagle", "gold", ["ALMAN", "İMPARATORLARI"]), (960, esp_at, "castle", "gold", ["İSPANYA", "KRALLARI"]), (1470, bur_at, "b_saltire", "crimson", ["BURGONYA", "DÜKLERİ"])]
        kk = cx.amt(keys_at, 0.8)
        for (xc, ta, ic, metal, lab) in items:
            k = cx.amt(ta, 0.7)
            if k > 0:
                glow(f, xc, 640, 260, "#FFB347", 0.22 * k)
                icons.draw_icon(f, ic, xc, 640 - (1 - ease_out(k)) * 40, size=300 * (0.85 + 0.15 * back_out(k)), metal=metal, alpha=k, glow=0.2 + 0.25 * kk)
                for li, tx in enumerate(lab):
                    f.text(tx, xc, 955 + li * 46 - 4, face="title_m", size=(38 if li == 0 else 32), color="#F0DDA0", align="c", track=6, alpha=k, shadow=(2, 3, 3, "#000000"))
        # Roma anahtarları ve zincirler
        if kk > 0:
            for (xc, _, _, _, _) in items:
                ck = clamp((cx.t - cx.at(chain_at)) / 0.9)
                if ck > 0:
                    chain_links(f, (960, 240), (xc, 300), bend=(0 if xc == 960 else (60 if xc < 960 else -60)), prog=ck, color="#C9A5F0", link=30, alpha=0.95)
            glow(f, 960, 160, 220, "#B58AD8", 0.35 * kk)
            icons.draw_icon(f, "keys", 960, 165 - (1 - ease_out(kk)) * 60, size=200, metal="violet", alpha=kk, glow=0.35)
    f.vig(0.62)


# ───────────────────────────── bin yıllık Hıristiyanlık: nef perspektifi ─────────────────────────────
import scenes_lib as SL  # noqa: E402
import stage as ST  # noqa: E402


@SL.sc("c4_nave")
class Nave:
    """Tek noktalı perspektifle uzayan gotik nef; sonda ışıklı pencere, önde küçük bir keşiş."""

    def __init__(self, p):
        self.p = p

    def layers(self):
        VP = (960, 455)
        N = 11
        zs = [1.0 + 0.62 * k for k in range(N)]

        def arch_params(k):
            s = 1.0 / zs[k]
            return s, 1150 * s, 980 * s, VP[1] + 540 * s

        def L_far(f):
            f.rect(-ST.MARGIN, -ST.MARGIN, W + 2 * ST.MARGIN, H + 2 * ST.MARGIN, color="#0B0604")
            s, w, h, by = arch_params(N - 1)
            inner = ST.pointed_arch_path(960, by, w, h)
            f.c.save(); f.c.clipPath(inner, skia.ClipOp.kIntersect, True)
            f.rect(960 - w, by - h - 40, 2 * w, h + 80, shader=f.lin(0, by - h, 0, by, [("#FFF2CC", 0.0), ("#FFC070", 0.6), ("#E7992F", 1.0)]))
            f.c.restore()
            glow(f, 960, VP[1], 420, "#FFD9A0", 0.55)
            # zemin
            fl = sk.poly_path([(960 - w, by), (960 + w, by), (W + 900, H + 300), (-900, H + 300)], True)
            f.path(fl, shader=f.lin(0, by, 0, H, [("#3A2415", 0.0), ("#241509", 0.5), ("#150C07", 1.0)]))
            # merkez ışık yolu
            lp = sk.poly_path([(960 - w * 0.6, by), (960 + w * 0.6, by), (960 + 360, H + 200), (960 - 360, H + 200)], True)
            f.path(lp, shader=f.lin(0, by, 0, H, [("#FFD58A", 0.0, 120), ("#FFB347", 0.5, 50), ("#FFB347", 1.0, 20)]), blend=skia.BlendMode.kPlus)

        def L_arches(f):
            for k in range(N - 1, -1, -1):
                s, w, h, by = arch_params(k)
                t = 150 * s
                outer = ST.pointed_arch_path(960, by, w + 2 * t, h + t * 1.2)
                inner = ST.pointed_arch_path(960, by, w, h)
                ring = skia.Op(outer, inner, skia.PathOp.kDifference_PathOp)
                dark = mix("#5A3E24", "#1B0F08", clamp(k / (N - 1)) ** 0.7)
                f.path(ring, shader=f.lin(960 - w, 0, 960 + w, 0, [(mix(dark, "#000000", 0.35), 0.0), (mix(dark, "#FFFFFF", 0.08), 0.5), (mix(dark, "#000000", 0.35), 1.0)]))
                f.path(ring, style="stroke", sw=max(1.2, 3 * s), color="#B88A3A", alpha=0.35 * (1 - k / N))
                # yan duvar: kemer halkasının dışındaki boşluğu koyulaştır (derinlik)
            ST.god_rays(f, (960, VP[1]), math.radians(90), 1.3, 1300, n=8, alpha=0.10, seed=4)

        def L_cols(f):
            for sx in (-1, 1):
                ST.column(f, 960 + sx * 930, -80, 1160, 190, stone="#150C07", edge="#5A3C1E")
            f.rect(-ST.MARGIN, -ST.MARGIN, W + 2 * ST.MARGIN, 100, color="#0B0604", alpha=0.7)

        def L_floorlight(f):
            spot(f, 960, 990, 240, 36, "#FFE2A0", 0.30)

        return [(0.15, L_far), (0.45, L_arches), (0.85, L_floorlight), (1.4, L_cols)]

    def dyn(self):
        def D(f, t):
            ST.figure(f, "monk", 960, 996, 330, col="#080503", rim="#C58A44", face=1, sway=math.sin(t * 1.1) * 0.004)
        return {2: D}


@SH.kind("c4_nave_over")
def _unused_placeholder(cx):  # pragma: no cover
    pass


def nave_overlay(cx, thou_at, one_at, wrong_at):
    f = cx.f
    k = cx.amt(thou_at, 0.8)
    if k > 0:
        f.gold("BİN YIL", W / 2, 215, face="title", size=130, track=22, alpha=k, glow=0.35 * k, scale=1.0 + (1 - k) * 0.06)
    o = cx.amt(one_at, 0.7)
    if o > 0:
        # tek keşiş: parıltı halkası
        r = 80 + 60 * ease_out(o)
        f.oval(W / 2, 1005, r * 1.9, r * 0.28, style="stroke", sw=3, color="#FFE2A0", alpha=0.7 * (1 - o * 0.5))
    w = cx.amt(wrong_at, 0.8)
    if w > 0:
        glow(f, W / 2, 470, 320, "#FFD27A", 0.20 * w)
        icons.draw_icon(f, "question", W / 2, 470, size=330 * (0.85 + 0.15 * back_out(w)), metal="silver", alpha=0.85 * w, glow=0.3)


# ───────────────────────────── altı şey ortaya konur ─────────────────────────────
@SH.kind("c4_pledge")
def k_pledge(cx, items=(), settle_at=6.0, line_at=6.9):
    """items: [(etiket, simge, metal, çapa)] — altı madalyon, merkezde 'dava' haçı."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.3)
    duo_glow(f, CRIM, PETROL, a=0.22)
    sk.dust(f, cx.t, n=55)
    cxm, cym = W / 2, 520
    rx, ry = 730, 310
    # merkez: dava (haç)
    ck = cx.amt(0.2, 0.8)
    glow(f, cxm, cym, 330, "#FFD27A", 0.28 * ck + 0.2 * cx.amt(settle_at, 0.6))
    icons.draw_icon(f, "cross", cxm, cym, size=270 * (0.9 + 0.1 * ck), metal="gold", alpha=ck, glow=0.25)
    f.text("DAVA", cxm, cym + 205, face="title_m", size=34, color="#C9B27A", align="c", track=18, alpha=ck * 0.9)
    st = cx.amt(settle_at, 0.9)
    n = len(items)
    for i, (lab, ic, metal, ta) in enumerate(items):
        ang = math.radians(-90 + 360 * i / n + 30)
        tx, ty = cxm + rx * math.cos(ang), cym + ry * math.sin(ang)
        k = cx.amt(ta, 0.6)
        if k <= 0:
            continue
        # gelişi: dış kenardan süzülür, sonra 'koyma' anında merkeze biraz yaklaşır
        ex = lerp(tx + (tx - cxm) * 0.35, tx, ease_out(k))
        ey = lerp(ty + (ty - cym) * 0.35, ty, ease_out(k))
        ex = lerp(ex, cxm + (tx - cxm) * 0.82, st)
        ey = lerp(ey, cym + (ty - cym) * 0.82, st)
        r = 112
        f.circle(ex, ey, r + 14, color="#000000", alpha=0.38 * k, blur=14)
        f.circle(ex, ey, r, shader=f.rad(ex - 20, ey - 26, r * 1.5, [("#3A2415", 0.0), ("#150D08", 1.0)]), alpha=k)
        f.circle(ex, ey, r, style="stroke", sw=5, color="#C9962B", alpha=k)
        f.circle(ex, ey, r - 11, style="stroke", sw=1.6, color="#C9962B", alpha=0.6 * k)
        icons.draw_icon(f, ic, ex, ey, size=136, metal=metal, alpha=k, shadow=False, glow=0.18)
        f.text(lab, ex, ey + r + 48, face="title_m", size=32, color="#F0DDA0", align="c", track=6, alpha=k, shadow=(2, 3, 3, "#000000"))
        lk = clamp((cx.t - cx.at(line_at)) / 0.8)
        if lk > 0:
            dx, dy = cxm - ex, cym - ey
            L = math.hypot(dx, dy) or 1.0
            sx_, sy_ = ex + dx / L * (r + 6), ey + dy / L * (r + 6)
            ex2, ey2 = cxm - dx / L * 140, cym - dy / L * 140
            f.line(sx_, sy_, lerp(sx_, ex2, lk), lerp(sy_, ey2, lk), color="#F0D27A", sw=2.5, alpha=0.5 * k * (1 - 0.3 * lk))
    f.vig(0.6)


# ───────────────────────────── ferman: Luther gittikten sonra imzalandı, geriye dönük tarihlendi ─────────────────────────────
@SH.kind("c4_backdate")
def k_backdate(cx, at=0.0, leave_at=1.5, sign_at=3.4, back_at=4.7, stamp_at=5.0):
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.28)
    duo_glow(f, PETROL, CRIM, a=0.2, y=H * 0.55)
    a = cx.amt(at, 0.8)
    with push(cx, 1.0, 1.05, pan=(0, 8)):
        yy = H * 0.5 + (1 - ease_out(a)) * 120
        with paper(f, 960, yy, 1360, 780, rot=-0.012, alpha=a, seed=37, tone="#DFCB98"):
            reveal(f, "WORMS FERMANI", 0, -390 + 100, clamp((cx.t - cx.at(at, off=0.25)) / 0.9), face="fell", size=70, align="c", alpha=a)
            f.line(-330, -390 + 128, 330, -390 + 128, color=INK, sw=2.2, alpha=0.55 * a)
            scribbles(f, -520, -390 + 205, 1040, 3, prog=clamp((cx.t - cx.at(at, off=0.6)) / 1.2), seed=52, line_h=50, thick=6.4, alpha=0.6 * a)
            # zaman ekseni
            ay = 150
            f.line(-560, ay, 560, ay, color=INK, sw=4, alpha=0.7 * a)
            xA, xB, xC = -420, -20, 380
            for (xx, lab, ta, col) in ((xA, ["LUTHER", "AYRILDI"], leave_at, "#1E5560"), (xB, ["FERMANIN", "TARİHİ"], back_at, "#8E6A1A"), (xC, ["İMZA"], sign_at, "#8E1F26")):
                k = cx.amt(ta, 0.5)
                if k > 0:
                    f.line(xx, ay - 18, xx, ay + 18, color=col, sw=5, alpha=k)
                    f.circle(xx, ay, 11, color=col, alpha=k)
                    for li, tx in enumerate(lab):
                        f.text(tx, xx, ay + 62 + li * 38, face="fell", size=34, color=INK, align="c", alpha=0.9 * k)
            # Luther gider (küçük keşiş simgesi sağa yürür)
            kl = clamp((cx.t - cx.at(leave_at)) / 1.3)
            if kl > 0:
                mx = lerp(xA, xA + 150, ease_out(kl))
                icons.draw_icon(f, "monk", mx, ay - 76, size=96, metal="teal", alpha=a * (1 - 0.65 * kl), shadow=False)
            # mühür düşer
            SH.wax_seal(f, xC, ay - 104, 58, color="#8E1F26", t=cx.amt(sign_at, 0.35), alpha=a, mono="K")
            # geriye dönük ok: İmzadan tarihe geri
            bk = clamp((cx.t - cx.at(back_at)) / 0.9)
            if bk > 0:
                curve_arrow(f, (xC - 14, ay - 150), (xB + 6, ay - 22), bend=-150, prog=bk, color="#8E6A1A", sw=6, alpha=a, shadow=False)
    s = cx.amt(stamp_at, 0.3)
    if s > 0:
        stamp2(f, "GERİYE DÖNÜK TARİHLİ", 990, 872, rot=-0.045, size=62, t=s, seed=21, fill_bg="#150D08")
    f.vig(0.6)


# ───────────────────────────── kanun dışı + üç yasak ─────────────────────────────
@SH.kind("c4_banned")
def k_banned(cx, outlaw_at=1.0, rows=()):
    """rows: [(etiket, simge, metal, çapa)]"""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.28)
    duo_glow(f, PETROL, CRIM, a=0.28, y=H * 0.5)
    sk.dust(f, cx.t, n=50)
    a = cx.amt(0.0, 0.7)
    dim = 1.0 - 0.0 * cx.amt(outlaw_at, 0.6)
    with push(cx, 1.0, 1.04):
        draw_medal2(f, "luther", 520, 520, 520 * (0.95 + 0.05 * ease_out(a)), "teal", False, alpha=a * (1 - 0.18 * cx.amt(outlaw_at, 0.6)), tilt=0.12 * math.sin(cx.t * 0.6))
        fit_plate(f, "MARTIN LUTHER", None, 520, 820, w=520, t=cx.amt(0.4, 0.6))
        for i, (lab, ic, metal, ta) in enumerate(rows):
            y = 320 + i * 190
            k = cx.amt(ta, 0.5, off=-0.55)
            if k <= 0:
                continue
            x0 = 1070
            f.rrect(x0, y - 80, 640, 160, 18, color="#150D08", alpha=0.78 * k)
            f.rrect(x0, y - 80, 640, 160, 18, style="stroke", sw=2.5, color="#7A5518", alpha=0.9 * k)
            icons.draw_icon(f, ic, x0 + 90, y, size=124, metal=metal, alpha=k, shadow=False)
            f.text(lab, x0 + 190, y + 20, face="title", size=56, color="#F0DDA0", align="l", track=10, alpha=k, shadow=(2, 3, 3, "#000000"))
            sk_ = clamp((cx.t - cx.at(ta)) / 0.35)
            if sk_ > 0:
                strike(f, x0 + 24, y + 4, x0 + 616, y - 2, sk_, sw=11, seed=i + 3)
                icons.draw_icon(f, "b_forbid", x0 + 90, y, size=150 * (1.2 - 0.2 * ease_out(sk_)), metal="crimson", alpha=0.9 * sk_, shadow=False)
    o = cx.amt(outlaw_at, 0.3)
    if o > 0:
        stamp2(f, "KANUN DIŞI", 520, 480, rot=-0.13, size=86, t=o, seed=33, fill_bg="#150D08")
    f.vig(0.6)


# ───────────────────────────── bölüm sonu: ferman yanarken fikir parlar ─────────────────────────────
@SH.kind("c4_finale")
def k_finale(cx, seal_at=1.2, ignite_at=2.2):
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.25)
    sk.dust(f, cx.t, n=50)
    ik = cx.amt(ignite_at, 1.4)
    glow(f, W / 2, H * 0.62, 760, "#FFB347", 0.32 * ik)
    a = cx.amt(0.0, 0.6)
    with push(cx, 1.0, 1.06):
        yy = 500 + (1 - ease_out(a)) * 80
        with paper(f, 560, yy, 640, 780, rot=-0.04, alpha=a * (1 - 0.35 * ik), seed=41, tone="#D6C08A"):
            f.text("FERMAN", 0, -390 + 110, face="fell", size=64, color=INK, align="c", track=6, alpha=a)
            f.line(-200, -390 + 134, 200, -390 + 134, color=INK, sw=2, alpha=0.5 * a)
            scribbles(f, -250, -390 + 210, 500, 9, prog=clamp((cx.t - cx.at(0.3)) / 1.0), seed=17, line_h=52, thick=6.4, alpha=0.62 * a * (1 - 0.6 * ik))
            SH.wax_seal(f, 150, 250, 60, color="#8E1F26", t=cx.amt(seal_at, 0.35), alpha=a)
            # yanık kenar: alttan yukarı kömürleşme
            if ik > 0:
                rs = np.random.RandomState(9)
                ytop = 390 - 560 * ease_out(ik, 1.5)
                pts = [(-340, 400)]
                x = -340
                while x <= 340:
                    pts.append((x, ytop + rs.randn() * 14 + math.sin(x * 0.04) * 10))
                    x += 24
                pts.append((340, 400))
                f.c.save()
                f.c.clipRect(skia.Rect.MakeXYWH(-320, -390, 640, 780))
                f.path(sk.poly_path(pts, True), color="#0B0604", alpha=0.92)
                f.path(sk.poly_path(pts[1:-1], False), style="stroke", sw=9, color="#FF8A2A", alpha=0.9 * ik, blur=3)
                f.path(sk.poly_path(pts[1:-1], False), style="stroke", sw=3.5, color="#FFE6A0", alpha=0.95 * ik)
                f.c.restore()
        # fikir: büyük alev
        fk = cx.amt(ignite_at, 0.9)
        if fk > 0:
            glow(f, 1330, 480, 420, "#FFB347", 0.40 * fk)
            icons.draw_icon(f, "b_flame", 1330, 500 - 20 * math.sin(cx.t * 3), size=460 * (0.7 + 0.3 * back_out(fk)), metal="gold", alpha=fk, glow=0.55)
            f.gold("FİKİR", 1330, 840, face="title", size=96, track=18, alpha=cx.amt(ignite_at, 0.8, off=0.4), glow=0.4)
    sk.embers(f, cx.t, n=50, rect=(900, 300, 900, 760), color="#FFB347")
    f.vig(0.62)


# ───────────────────────────── matbaa: Wittenberg'den yayılma (harita extra) ─────────────────────────────
WITT = (12.65, 51.87)
SPREAD_TO = [(9.99, 53.55), (11.63, 52.12), (12.37, 51.34), (11.03, 50.98), (6.96, 50.94), (8.68, 50.11),
             (11.08, 49.45), (7.75, 48.57), (10.90, 48.37), (7.59, 47.56), (11.58, 48.14), (13.40, 52.52)]


def make_spread(press_at, spread_at, dur=1.25, stagger=0.13):
    def extra(cx, cam, mv):
        f = cx.f
        ox, oy = cam.ll(*WITT)
        pk = cx.amt(press_at, 0.5)
        if pk <= 0:
            return
        for i, (lon, lat) in enumerate(SPREAD_TO):
            ex, ey = cam.ll(lon, lat)
            k = clamp((cx.t - cx.at(spread_at, off=i * stagger)) / dur)
            if k <= 0:
                continue
            bend = (-1) ** i * 55
            curve_arrow(f, (ox, oy), (ex, ey), bend=bend, prog=ease_out(k, 2), color="#F0D27A", sw=3.4, head=False, alpha=0.85, shadow=True)
            if k > 0.98:
                pulse = clamp((cx.t - cx.at(spread_at, off=i * stagger + dur)) / 0.7)
                f.circle(ex, ey, 7, color="#F0D27A", alpha=1.0)
                f.circle(ex, ey, 7 + 34 * pulse, style="stroke", sw=2.2, color="#F0D27A", alpha=0.7 * (1 - pulse))
        glow(f, ox, oy - 40, 150, "#FFD27A", 0.4 * pk)
        icons.draw_icon(f, "b_press", ox, oy - 62, size=(118 * (0.8 + 0.2 * back_out(pk))), metal="gold", alpha=pk, glow=0.35)
    return extra


# ───────────────────────────── Worms: nabız halkaları (harita extra) ─────────────────────────────
def make_worms_pulse(at):
    def extra(cx, cam, mv):
        f = cx.f
        x, y = cam.ll(8.36, 49.63)
        t0 = cx.at(at)
        if cx.t < t0:
            return
        for i in range(3):
            ph = ((cx.t - t0) * 0.55 - i * 0.33) % 1.0
            if cx.t - t0 - i * 0.6 < 0:
                continue
            f.circle(x, y, 20 + 150 * ph, style="stroke", sw=3.0, color="#F0D27A", alpha=0.75 * (1 - ph))
        glow(f, x, y, 90, "#FFD27A", 0.5 * clamp((cx.t - t0) / 0.6))
    return extra


# ───────────────────────────── Wartburg: Yeni Ahit Almancaya (açık kitap) ─────────────────────────────
@SH.kind("c4_book")
def k_book(cx, head_at=0.6, de_at=1.6, write_at=2.2, write_dur=1.4):
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.2)
    glow(f, 1560, 330, 700, "#FFB347", 0.28)
    sk.dust(f, cx.t, n=50)
    a = cx.amt(0.0, 0.7)
    with push(cx, 1.0, 1.07, pan=(-20, -6)):
        cxm, cym = 900, 590
        # masa
        f.rect(0, 800, W, H - 800, shader=f.lin(0, 800, 0, H, [("#4A2F1A", 0.0), ("#1B0F08", 1.0)]), alpha=a)
        f.line(0, 800, W, 800, color="#B88A3A", sw=2.5, alpha=0.5 * a)
        # kitap: kapak + iki sayfa
        f.rrect(cxm - 640, cym - 330, 1280, 690, 26, color="#2A150A", alpha=a)
        f.rrect(cxm - 640, cym - 330, 1280, 690, 26, style="stroke", sw=4, color="#7A5518", alpha=0.9 * a)
        for side in (-1, 1):
            x0 = cxm if side == 1 else cxm - 590
            pg = sk.poly_path([(cxm, cym - 290), (cxm + side * 590, cym - 310), (cxm + side * 590, cym + 320), (cxm, cym + 340)], True)
            f.path(pg, shader=f.lin(cxm, 0, cxm + side * 590, 0, [("#8A7650", 0.0), ("#CDB985", 0.25), ("#C2AE7C", 1.0)]), alpha=a)
            for q in range(1, 5):
                f.line(cxm, cym + 340 + q * 4, cxm + side * 590, cym + 320 + q * 4, color="#7A5E30", sw=1.5, alpha=0.5 * a)
        f.line(cxm, cym - 290, cxm, cym + 340, color="#6E5028", sw=5, alpha=0.7 * a)
        # sol sayfa: Latince (kısık), sağ: Almanca yazılır
        scribbles(f, cxm - 520, cym - 190, 450, 12, prog=clamp(a * 2), seed=71, line_h=44, thick=6.0, alpha=0.50)
        wp = clamp((cx.t - cx.at(write_at)) / write_dur)
        scribbles(f, cxm + 70, cym - 190, 450, 12, prog=wp, seed=88, line_h=44, thick=6.4, alpha=0.78, color="#1A1208")
        # başlıklar
        dk = cx.amt(de_at, 0.7)
        if dk > 0:
            f.text("ALMANCA", cxm + 295, cym - 225, face="fell_i", size=38, color="#1A1208", align="c", alpha=0.95 * dk)
        # kalem
        if wp > 0:
            row = min(11.99, wp * 12)
            qx = cxm + 70 + 450 * (row % 1.0)
            qy = cym - 190 + int(row) * 44
            icons.draw_icon(f, "quill", qx + 70, qy - 54, size=150, metal="gold", alpha=a * (1 - smooth((wp - 0.95) / 0.05) * 0.0), rot=0.5)
        # mum (sağda)
        flame(f, 1640, 740, s=2.0, t=cx.t, seed=7)
        f.rect(1620, 750, 40, 100, shader=f.lin(1620, 0, 1660, 0, [("#C9B890", 0.0), ("#EADCB5", 0.5), ("#9C8559", 1.0)]))
        f.rect(1610, 846, 60, 12, color="#7A5518")
    # üst başlık
    tk = cx.amt(head_at, 0.8)
    if tk > 0:
        f.gold("YENİ AHİT", W / 2, 150, face="title", size=104, track=20, alpha=tk, glow=0.35 * tk, scale=1.0 + (1 - tk) * 0.06)
    f.vig(0.62)


# ───────────────────────────── theatre bindirmeleri (lab sahneleri üstüne) ─────────────────────────────
def road_overlay(kidnap_at, men_at):
    """Gece yolu: “KAÇIRILDI” (tırnaklı) + Saksonya Seçmeni'nin adamları ibaresi."""
    def ov(cx):
        f = cx.f
        k = cx.amt(kidnap_at, 0.5)
        if k > 0:
            f.rect(0, 0, W, 330, shader=f.lin(0, 0, 0, 330, [("#000000", 0.0, int(170 * k)), ("#000000", 1.0, 0)]))
            f.gold("“KAÇIRILDI”", W / 2 - 90, 215, face="title", size=104, track=14, alpha=k, glow=0.35 * k, scale=1.0 + (1 - k) * 0.06)
    return ov


def wartburg_overlay(castle_at, name_at):
    def ov(cx):
        f = cx.f
        k = cx.amt(castle_at, 0.6)
        if k > 0:
            f.rect(0, H * 0.72, W, H * 0.28, shader=f.lin(0, H * 0.72, 0, H, [("#000000", 0.0, 0), ("#000000", 1.0, int(205 * k))]))
            f.text("WARTBURG KALESİ", 120, H * 0.915, face="title_m", size=42, color="#C9B27A", align="l", track=14, alpha=k, shadow=(2, 3, 4, "#000000"))
        n = cx.amt(name_at, 0.8)
        if n > 0:
            f.gold("“ŞÖVALYE JÖRG”", W - 130, H * 0.93, face="title", size=84, track=10, alpha=n, glow=0.35 * n, align="r", scale=1.0)
    return ov
