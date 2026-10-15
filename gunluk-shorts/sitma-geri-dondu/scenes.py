"""Sıtma Geri Döndü — 12 sahne, mavi baskı (blueprint) stili. Her fonksiyon t için 1080x1920 RGB döndürür.
Ortak görsel dil: Türkiye taslağı + vaka noktaları (1 nokta ≈ 300 vaka, şematik) + doğrusal çubuk; HUD'da yıl sayacı."""
import math

import cues
import turkiye as TK
from bp import *  # noqa
from cues import st, wt, we, en
from engine import *  # noqa
from icons import *  # noqa

WHITE = (255, 255, 255)
MAP_S, MAP_CY = 0.90, 810          # istatistik düzeninde harita ölçeği / merkez y


def new(t, z=1.0, cx=W / 2, cy=H / 2, shake=True, tint=0.0):
    ctx = Ctx()
    sx, sy = cues.shake(t) if shake else (0.0, 0.0)
    ctx.cam(cx, cy, z, (sx, sy))
    bg(ctx, t, tint)
    return ctx


def finish(ctx, t):
    return bp_post(ctx.finish(), t)


def thou(v):
    return f"{int(round(v)):,}".replace(",", ".")


# ───────────── harita + noktalar ─────────────
def draw_map(ctx, cx, cy, s, n, layout, t, dot_col=RED, outline=LINE, pulse=1.0, r=6.0, fill=True):
    pts = TK.outline(cx, cy, s)
    if fill:
        ctx.poly(pts, (10, 38, 78), 0.9)
    L(ctx, pts, 5, outline, 1.0, 1.0, closed=True)
    pos = TK.dots(layout)
    k = int(n)
    for i in range(min(k + 1, len(pos))):
        a = 1.0 if i < k else (n - k)
        if a <= 0.02:
            continue
        x, y = TK.xy(pos[i][0], pos[i][1], cx, cy, s)
        rr = r * s * (1 + 0.16 * float(pulse) * math.sin(t * 7 + i * 1.7))
        ctx.circ(x, y, rr * 1.9, dot_col, 0.20 * a)
        ctx.circ(x, y, rr, dot_col, a)


def scan(ctx, t, t0, t1, x0=70, x1=1010, y0=820, y1=1220, a=0.85):
    """Haritanın üzerinden geçen plotter tarama çizgisi (kart bekleme anlarında hareket verir; başta/sonda görünmez)"""
    u = prog(t, t0, t1)
    if u <= 0 or u >= 1:
        return
    x = lerp(x0, x1, u)
    L(ctx, [(x, y0), (x, y1)], 4, AMBER, a * math.sin(math.pi * u) ** 0.7, 1.0)


def bar(ctx, v, col, y=1120, x0=100, x1=980, vmax=cues.CASES["c77"], h=56):
    L(ctx, [(x0, y - h / 2), (x1, y - h / 2), (x1, y + h / 2), (x0, y + h / 2)], 2.5, LINE_DIM, 0.6, 1.0, closed=True, glow=False)
    w = max(4.0, (x1 - x0) * v / vmax)
    ctx.poly([(x0 + 4, y - h / 2 + 4), (x0 + w - 4, y - h / 2 + 4), (x0 + w - 4, y + h / 2 - 4), (x0 + 4, y + h / 2 - 4)], col, 0.92)
    L(ctx, [(x0 + w, y - h / 2 - 10), (x0 + w, y + h / 2 + 10)], 4, col, 1.0, 1.0, glow=False)


def legend(ctx, a=1.0, y=1035):
    ctx.circ(160, y, 8, RED, a)
    txt(ctx, 190, y, "1 NOKTA ≈ 300 VAKA · ŞEMATİK", 44, LINE, a, anchor="lm")


def stat_block(ctx, t, value, col, label, n, layout, bar_v, cy=MAP_CY, s=MAP_S, dots_col=RED, pulse=1.0, a=1.0, bar_col=None, hide_counter=False):
    """Üstte etiket + büyük sayaç, ortada harita, altta açıklama + doğrusal çubuk"""
    txt(ctx, 540, 385, label, 52, LINE_DIM, a)
    if not hide_counter:
        txt(ctx, 540, 500, thou(value), 150, col, a)
    draw_map(ctx, 540, cy, s, n, layout, t, dots_col, pulse=pulse)
    legend(ctx, a)
    bar(ctx, bar_v, bar_col or col)
    txt(ctx, 540, 1190, "ÇUBUK: DOĞRUSAL ÖLÇEK", 44, LINE_DIM, a)


# ───────────── açılış/kapanış kartı (ilk kare = son kare) ─────────────
def title_card(ctx, dy=0.0):
    """Kanca kartı: 5 kelime, ≥84 px, 3 satır, güvenli alan y 290–1250"""
    txt(ctx, 540, 430 + dy, "SITMA", 190, AMBER)
    txt(ctx, 540, 580 + dy, "NEREDEYSE BİTMİŞTİ", 84, WHITE)
    txt(ctx, 540, 705 + dy, "NEDEN DÖNDÜ?", 140, WHITE)
    L(ctx, [(120, 800 + dy), (960, 800 + dy)], 5, AMBER, 1.0, 1.0)


# ═══════════ A: kart → "neredeyse bitmişti" (1970) → "geri döndü!" (1977) ═══════════
def n_A(t):
    sh0, sh1 = 1.30, max(we("A", 3), 2.15)
    b0, b1 = wt("A", 5), wt("A", 6) + 0.45
    if t < sh0:
        return float(cues.N_1977)
    if t < sh1:
        return lerp(cues.N_1977, cues.N_1970, ease_io(prog(t, sh0, sh1)))
    if t < b0:
        return float(cues.N_1970)
    return lerp(cues.N_1970, cues.N_1977, ease_out(prog(t, b0, b1), 2.5))


def scene_A(t, still=False):
    tt_ = 0.0 if still else t
    ctx = new(tt_, shake=not still)
    fall = ease_in(prog(tt_, 0.85, 1.30), 2.0)
    mv = ease_io(prog(tt_, 0.95, 1.55))
    n = n_A(tt_)
    cy, sc = lerp(1020, MAP_CY, mv), lerp(0.98, MAP_S, mv)
    pa = 0.0 if still else (prog(tt_, 0.0, 0.35) if tt_ < 1.4 else 1.0)
    draw_map(ctx, 540, cy, sc, n, "salgin77", tt_, pulse=pa)
    if not still and tt_ < 0.9:
        scan(ctx, tt_, 0.12, 0.85)
    if tt_ < 1.35:
        title_card(ctx, dy=-2300 * fall if not still else 0.0)
    if tt_ >= 1.0:
        a = ease_out(prog(tt_, 1.1, 1.6), 3)
        v = lerp(cues.CASES["c70"], cues.CASES["c77"], clamp((n - cues.N_1970) / (cues.N_1977 - cues.N_1970)))
        col = RED if v > 20000 else AMBER
        txt(ctx, 540, 385, "KAYITLI VAKA / YIL", 52, LINE_DIM, a)
        txt(ctx, 540, 500, thou(v), 150, col, a)
        legend(ctx, a)
    return finish(ctx, tt_)


# ═══════════ B: kinin dağıtıldı, bataklıklar kurutuldu (1923 → 1970) ═══════════
def scene_B(t):
    ctx = new(t, 1.0 + 0.03 * prog(t, st("B"), en("B")))
    n = lerp(cues.N_1923, cues.N_1970, ease_io(prog(t, st("B") + 0.5, en("B") - 0.05)))
    draw_map(ctx, 540, 640, 0.80, n, "yayginlik", t)
    a1 = 1.0 - ease_out(prog(t, st("B") + 1.5, st("B") + 1.9))
    a2 = ease_out(prog(t, st("B") + 1.7, st("B") + 2.1))
    txt(ctx, 540, 395, "ÇOK YAYGIN", 84, AMBER, a1)
    txt(ctx, 540, 395, "AZALIYOR", 84, GREEN, a2)
    # kinin şişesi + haplar → haritaya
    tq = wt("B", 1)
    kq = ease_out(prog(t, tq - 0.1, tq + 0.5), 3)
    bottle(ctx, 290, 1010, 1.15, kq)
    if t >= tq:
        for i in range(7):
            u = ((t - tq) * 0.9 + i / 7.0) % 1.0
            ctx.circ(290 + 20 * math.sin(i * 2.1) + u * 60, 930 - u * 230, 8 * (1 - 0.4 * u), (255, 240, 200), 0.95 * (1 - u * 0.8))
    txt(ctx, 290, 1170, "KİNİN", 56, LINE, ease_out(prog(t, tq, tq + 0.3)))
    # bataklık kuruyor
    tm = wt("B", 3)
    km = ease_out(prog(t, tm - 0.1, tm + 0.5), 3)
    lvl = 1.0 - ease_io(prog(t, wt("B", 4), wt("B", 4) + 0.9))
    marsh(ctx, 790, 1000, 0.95, t, lvl, km)
    txt(ctx, 790, 1170, "BATAKLIK", 56, LINE, ease_out(prog(t, tm, tm + 0.3)))
    if t > wt("B", 4):
        check(ctx, 930, 930, 0.9, ease_out(prog(t, wt("B", 4) + 0.5, wt("B", 4) + 0.9)))
    return finish(ctx, t)


# ═══════════ C: vaka sayısı 1.263'e düştü (1970) ═══════════
def scene_C(t):
    ctx = new(t, 1.0 + 0.04 * prog(t, st("C"), en("C")))
    tn = wt("C", 2)
    k = ease_out(prog(t, tn - 0.05, tn + 0.55), 3)
    v = cues.CASES["c70"] * k
    stat_block(ctx, t, v, AMBER, "KAYITLI VAKA", cues.N_1970, "yayginlik", v, dots_col=AMBER, hide_counter=t < tn - 0.12)
    # düşüş oku
    arrow(ctx, 940, 450, 940, 560, GREEN, ease_out(prog(t, wt("C", 3) - 0.05, wt("C", 3) + 0.3)), 9, 30)
    # az sayıda nokta için sonar halkaları
    pos = TK.dots("yayginlik")
    for i in range(cues.N_1970):
        x, y = TK.xy(pos[i][0], pos[i][1], 540, MAP_CY, MAP_S)
        u = ((t * 0.9 + i * 0.27) % 1.0)
        ctx.ring(x, y, 12 + 40 * u, 3, AMBER, 0.8 * (1 - u))
    return finish(ctx, t)


# ═══════════ D: birkaç yıl sonra 115.000'i aştı! (1977) ═══════════
def scene_D(t):
    ctx = new(t, 1.0 + 0.02 * prog(t, st("D"), en("D")))
    t0, t1 = wt("D", 3) - 0.05, wt("D", 4) + 0.25
    k = ease_out(prog(t, t0, t1), 2.2)
    v = lerp(cues.CASES["c70"], cues.CASES["c77"], k)
    n = lerp(cues.N_1970, cues.N_1977, ease_in(prog(t, t0, t1), 1.4))
    col = RED if v > 20000 else AMBER
    stat_block(ctx, t, v, col, "KAYITLI VAKA", n, "salgin77", v)
    arrow(ctx, 940, 560, 940, 450, RED, ease_out(prog(t, wt("D", 4), wt("D", 4) + 0.3)), 9, 30)
    th = wt("D", 4) + 0.2
    if t >= th:
        a = ease_out(prog(t, th, th + 0.4))
        hx, hy = TK.xy(*TK.HUB_CUKUROVA, 540, MAP_CY, MAP_S)
        L(ctx, circ_pts(hx, hy, 46 + 8 * math.sin(t * 6), n=28), 4, AMBER, a, 1.0, glow=False)
        L(ctx, [(hx - 46, hy + 8), (hx - 84, hy + 22)], 3, AMBER, a, 1.0, glow=False)
        txt(ctx, hx - 220, hy + 22, "ÇUKUROVA", 44, AMBER, a)
    return finish(ctx, t)


# ═══════════ E: neden? Uzmanlara göre faktörler üst üste bindi ═══════════
def scene_E(t):
    ctx = new(t, 1.0 + 0.02 * prog(t, st("E"), en("E")))
    k = back_out(prog(t, st("E"), st("E") + 0.3), 2.0)
    txt(ctx, 540, 430, "NEDEN?", 160 * max(0.05, k), AMBER)
    ta = wt("E", 1)
    txt(ctx, 540, 580, "UZMANLARA GÖRE", 64, LINE, ease_out(prog(t, ta, ta + 0.3)))
    finals = [760, 890, 1020]
    ids = [4, 5, 6]
    for i in range(3):
        a_ = ease_out(prog(t, st("E") + 0.35 + 0.12 * i, st("E") + 0.7 + 0.12 * i)) * 0.45
        y = finals[i]
        if a_ > 0 and t < wt("E", ids[i]) + 0.35:
            L(ctx, [(160, y - 52), (920, y - 52), (920, y + 52), (160, y + 52)], 3, LINE_DIM, a_, 1.0, closed=True, glow=False)
            txt(ctx, 240, y + 2, "?", 80, LINE_DIM, a_)
    for i in range(3):
        ts = wt("E", ids[i]) - 0.05
        u = prog(t, ts, ts + 0.42)
        if u <= 0:
            continue
        y = finals[i] - (1 - back_out(u, 1.6)) * 700
        L(ctx, [(160, y - 52), (920, y - 52), (920, y + 52), (160, y + 52)], 5, LINE, 1.0, 1.0, closed=True)
        ctx.poly([(163, y - 49), (917, y - 49), (917, y + 49), (163, y + 49)], (10, 38, 78), 0.8)
        txt(ctx, 240, y + 2, "?", 90, AMBER)
        txt(ctx, 330, y + 2, "FAKTÖR", 60, LINE_DIM, anchor="lm")
        L(ctx, [(560, y + 2), (880, y + 2)], 3, LINE_DIM, 0.7, 1.0, glow=False)
    return finish(ctx, t)


# ═══════════ F: sulu tarım yayıldı, sivrisinek sayısı keskin arttı ═══════════
def scene_F(t):
    ctx = new(t, 1.0 + 0.02 * prog(t, st("F"), en("F")))
    tl = ease_out(prog(t, st("F") + 0.02, st("F") + 0.36), 3)
    txt(ctx, 540, 395, "SULU TARIM", 100 * max(0.05, tl), AMBER)
    # tarla büyür (yayıldı)
    t0, t1 = st("F") + 0.15, wt("F", 3) + 0.2
    for i, (cx, w_) in enumerate(((330, 380), (790, 380))):
        u = ease_out(prog(t, t0 + i * (t1 - t0) * 0.45, t0 + 0.5 + i * (t1 - t0) * 0.45), 3)
        if u > 0:
            field(ctx, cx, 600, w_, 260, t, u)
    # sivrisinek sayısı çubukları
    tb = wt("F", 5)
    txt(ctx, 430, 850, "SİVRİSİNEK SAYISI", 50, LINE, ease_out(prog(t, tb - 0.05, tb + 0.3)))
    hs = [26, 40, 62, 98, 154, 240]
    for i, h in enumerate(hs):
        ts = wt("F", 6) - 0.1 + i * 0.09
        u = ease_out(prog(t, ts, ts + 0.3), 3)
        if u <= 0:
            continue
        x = 150 + i * 90
        hh = h * u
        col = AMBER if i < 4 else RED
        ctx.poly([(x, 1190), (x + 60, 1190), (x + 60, 1190 - hh), (x, 1190 - hh)], col, 0.9)
    L(ctx, [(130, 1192), (700, 1192)], 3, LINE, 1.0, ease_out(prog(t, tb, tb + 0.3)), glow=False)
    arrow(ctx, 160, 1100, 690, 940, RED, ease_out(prog(t, wt("F", 6), wt("F", 7) + 0.3)), 6, 28)
    km = ease_out(prog(t, tb, tb + 0.6), 3)
    mosquito(ctx, 850, 1030, 0.86, km, rot=22, flap=t, w=4.4)
    return finish(ctx, t)


# ═══════════ G: işçi göçü hastalığı yeni bölgelere taşıdı ═══════════
def scene_G(t):
    ctx = new(t, 1.0 + 0.02 * prog(t, st("G"), en("G")))
    tl = ease_out(prog(t, wt("G", 1) - 0.05, wt("G", 1) + 0.35), 3)
    txt(ctx, 540, 395, "İŞÇİ GÖÇÜ", 100 * max(0.05, tl), AMBER)
    cy, s = 800, 1.0
    draw_map(ctx, 540, cy, s, 70, "cukurova", t, pulse=1.0)
    hx, hy = TK.xy(*TK.HUB_CUKUROVA, 540, cy, s)
    L(ctx, circ_pts(hx, hy, 40 + 10 * math.sin(t * 6), n=28), 4, AMBER, 1.0, 1.0, glow=False)
    targets = [(28.2, 38.6), (31.5, 40.2), (35.0, 40.6), (40.5, 38.4)]
    t0 = wt("G", 4)
    for i, (lo, la) in enumerate(targets):
        tx, ty = TK.xy(lo, la, 540, cy, s)
        k = ease_in_ease(prog(t, t0 + i * 0.16, t0 + i * 0.16 + 0.75))
        if k > 0:
            ex, ey = lerp(hx, tx, k), lerp(hy, ty, k)
            arrow(ctx, hx, hy, ex, ey, AMBER, 1.0, 5, 24 if k > 0.97 else 0.1)
            person(ctx, ex, ey + 40, 0.42, 1.0, LINE, walk=t * 9 + i)
        if k > 0.97:
            u = prog(t, t0 + i * 0.16 + 0.75, t0 + i * 0.16 + 1.1)
            for j in range(7):
                a_ = j * 0.9 + i
                ctx.circ(tx + math.cos(a_) * 26 * u * (0.5 + 0.2 * j % 3), ty + math.sin(a_) * 18 * u, 6, RED, 0.9 * u)
    txt(ctx, 540, 1075, "ŞEMATİK GÖSTERİM", 44, LINE_DIM, 1.0)
    return finish(ctx, t)


def ease_in_ease(x):
    return ease_io(x)


# ═══════════ H: izleme zayıftı ═══════════
def scene_H(t):
    ctx = new(t, 1.0 + 0.02 * prog(t, st("H"), en("H")))
    tl = ease_out(prog(t, st("H") + 0.02, st("H") + 0.36), 3)
    txt(ctx, 540, 395, "İZLEME", 110 * max(0.05, tl), AMBER)
    txt(ctx, 540, 482, "(şematik gösterim)", 44, LINE_DIM, ease_out(prog(t, st("H") + 0.2, st("H") + 0.5)) * 0.9)
    cy, s = 800, 1.0
    draw_map(ctx, 540, cy, s, 0, "salgin77", t, pulse=0.0)
    cell = 80
    ci = 0
    for gy in range(5):
        for gx in range(12):
            x0 = 78 + gx * cell
            y0 = 604 + gy * cell
            lon = TK.LON_C + ((x0 + cell / 2) - 540) / TK.KX
            lat = TK.LAT_C - ((y0 + cell / 2) - cy) / TK.KY
            if not TK._inside(lon, lat):
                continue
            ci += 1
            on = rng_hash(gx, gy, 77) < 0.30
            ts = st("H") + 0.25 + ((x0 - 78) / 922.0) * 1.0
            u = ease_out(prog(t, ts, ts + 0.25), 2)
            if u <= 0:
                continue
            if on:
                ctx.poly([(x0 + 6, y0 + 6), (x0 + cell - 6, y0 + 6), (x0 + cell - 6, y0 + cell - 6), (x0 + 6, y0 + cell - 6)], GREEN, 0.45 * u)
                L(ctx, [(x0 + 6, y0 + 6), (x0 + cell - 6, y0 + 6), (x0 + cell - 6, y0 + cell - 6), (x0 + 6, y0 + cell - 6)], 2.5, GREEN, u, 1.0, closed=True, glow=False)
            else:
                L(ctx, [(x0 + 6, y0 + 6), (x0 + cell - 6, y0 + 6), (x0 + cell - 6, y0 + cell - 6), (x0 + 6, y0 + cell - 6)], 2.5, RED, 0.75 * u, 1.0, closed=True, glow=False)
                L(ctx, [(x0 + 16, y0 + 16), (x0 + cell - 16, y0 + cell - 16)], 2.2, RED, 0.5 * u, 1.0, glow=False)
                L(ctx, [(x0 + cell - 16, y0 + 16), (x0 + 16, y0 + cell - 16)], 2.2, RED, 0.5 * u, 1.0, glow=False)
    mx = lerp(130, 950, ease_io(prog(t, st("H") + 0.2, wt("H", 2) + 0.3)))
    magnifier(ctx, mx, 600 + 150 * math.sin(t * 2.4) + 120, 1.0, ease_out(prog(t, st("H") + 0.05, st("H") + 0.4)))
    ctx.poly([(120, 1037), (146, 1037), (146, 1063), (120, 1063)], GREEN, 0.6)
    txt(ctx, 160, 1050, "İZLENEN", 44, GREEN, 1.0, anchor="lm")
    L(ctx, [(520, 1037), (546, 1037), (546, 1063), (520, 1063)], 3, RED, 0.9, 1.0, closed=True, glow=False)
    txt(ctx, 560, 1050, "İZLENMEYEN", 44, RED, 1.0, anchor="lm")
    tw = wt("H", 2)
    if t >= tw - 0.05:
        kk = back_out(prog(t, tw - 0.05, tw + 0.25), 2.2)
        stamp(ctx, 540, 1150, "ZAYIF!", 84, RED, -5.0, kk)
    return finish(ctx, t)


# ═══════════ I: mücadele yeniden başlayınca salgın geriledi (1977 → 1979) ═══════════
def scene_I(t):
    ctx = new(t, 1.0 + 0.02 * prog(t, st("I"), en("I")))
    k = ease_io(prog(t, wt("I", 2), en("I") - 0.05))
    v = lerp(cues.CASES["c77"], cues.CASES["c79"], k)
    n = lerp(cues.N_1977, cues.N_1979, k)
    col = mix(RED, GREEN, k)
    stat_block(ctx, t, v, col, "MÜCADELE YENİDEN", n, "salgin77", v, bar_col=col)
    sprayer(ctx, 880, 545, 0.58, ease_out(prog(t, wt("I", 0), wt("I", 0) + 0.5)), t)
    return finish(ctx, t)


# ═══════════ J: sıtma tekrar patladı: 84.000'i aştı! (1994) ═══════════
def scene_J(t):
    ctx = new(t, 1.0 + 0.02 * prog(t, st("J"), en("J")), tint=0.05)
    t0, t1 = wt("J", 4) - 0.05, wt("J", 5) + 0.25
    k = ease_out(prog(t, t0, t1), 2.2)
    v = lerp(cues.CASES["c79"], cues.CASES["c94"], k)
    n = lerp(cues.N_1979, cues.N_1994, ease_in(prog(t, t0, t1), 1.4))
    stat_block(ctx, t, v, mix(GREEN, RED, clamp(k * 2)), "İKİNCİ SALGIN", n, "salgin94", v)
    arrow(ctx, 940, 560, 940, 450, RED, ease_out(prog(t, wt("J", 5), wt("J", 5) + 0.3)), 9, 30)
    th = wt("J", 5) + 0.2
    if t >= th:
        a = ease_out(prog(t, th, th + 0.4))
        gx, gy = TK.xy(41.2, 37.4, 540, MAP_CY, MAP_S)
        L(ctx, circ_pts(gx, gy, 120 + 10 * math.sin(t * 6), 60, n=30), 4, AMBER, a, 1.0, glow=False)
        txt(ctx, gx, 990, "GÜNEYDOĞU", 44, AMBER, a)
    return finish(ctx, t)


# ═══════════ K: bugün yerli vaka yok (Bakanlık); ithal vakalar sürüyor ═══════════
def scene_K(t):
    ctx = new(t, 1.0 + 0.02 * prog(t, st("K"), en("K")))
    cy, s = 800, 1.0
    ty = wt("K", 4)
    ok = ease_out(prog(t, ty - 0.05, ty + 0.4), 3)
    ctx_col = mix(LINE, GREEN, ok)
    txt(ctx, 540, 385, "SAĞLIK BAKANLIĞI", 52, LINE_DIM, ease_out(prog(t, st("K") + 0.02, st("K") + 0.4)))
    k2 = back_out(prog(t, ty - 0.05, ty + 0.35), 2.0)
    if t >= ty - 0.04:
        txt(ctx, 540, 500, "YERLİ VAKA: 0", 110 * max(0.05, k2), GREEN if ok > 0.5 else LINE_DIM)
    nk = lerp(cues.N_1994, 0, ease_io(prog(t, st("K") + 0.1, st("K") + 1.9)))
    draw_map(ctx, 540, cy, s, nk, "salgin94", t, outline=ctx_col, pulse=1.0)
    # dışarıdan gelen ithal vakalar
    ti = wt("K", 7)
    srcs = [((40, 930), (260, 880)), ((1040, 760), (860, 810)), ((560, 1075), (560, 985))]
    for i, ((x0, y0), (x1, y1)) in enumerate(srcs):
        k = ease_io(prog(t, ti + i * 0.18, ti + i * 0.18 + 0.7))
        if k > 0:
            ex, ey = lerp(x0, x1, k), lerp(y0, y1, k)
            arrow(ctx, x0, y0, ex, ey, AMBER, 1.0, 5, 24 if k > 0.97 else 0.1)
            ctx.circ(ex, ey, 9, AMBER, 1.0)
            ctx.circ(ex, ey, 17, AMBER, 0.3)
    ta = ease_out(prog(t, ti, ti + 0.4))
    txt(ctx, 540, 1130, "İTHAL VAKA ≈ 200–250 / YIL", 50, AMBER, ta)
    txt(ctx, 540, 1188, "(HSGM: yıllık ortalama)", 44, LINE_DIM, ta * 0.9)
    return finish(ctx, t)


# ═══════════ L: ders — başa dönüş kartı ═══════════
def scene_L(t):
    ctx = new(t)
    k = ease_out(prog(t, st("L") - 0.04, st("L") + 0.35), 3)
    shiver = (rng_hash(int(t * 24), 1) - 0.5) * 6 * (1 - prog(t, st("L") + 0.4, cues.FINAL_T)) if t > st("L") else 0.0
    dy = (1 - k) * 1500 + shiver
    pa = prog(t, st("L") + 0.2, st("L") + 0.6) * (1.0 - prog(t, cues.FINAL_T - 0.7, cues.FINAL_T))
    draw_map(ctx, 540, 1020 + dy, 0.98, cues.N_1977, "salgin77", t, pulse=pa)
    title_card(ctx, dy=dy)
    scan(ctx, t, st("L") + 0.55, st("L") + 1.75)
    scan(ctx, t, st("L") + 1.75, st("L") + 2.95)
    return finish(ctx, t)


def _funcs():
    return [scene_A, scene_B, scene_C, scene_D, scene_E, scene_F, scene_G, scene_H, scene_I, scene_J, scene_K, scene_L]


def render_group(g, t):
    return _funcs()[g](t)
