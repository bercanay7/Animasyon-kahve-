"""Titanik'in Kehaneti — 12 sahne, mavi baskı (blueprint) stili. Her fonksiyon t için 1080x1920 RGB döndürür."""
import math

import cues
from bp import *  # noqa
from cues import st, wt, we, en
from engine import *  # noqa


def new(t, z=1.0, cx=W / 2, cy=H / 2, shake=True, tint=0.0):
    ctx = Ctx()
    sx, sy = cues.shake(t) if shake else (0.0, 0.0)
    ctx.cam(cx, cy, z, (sx, sy))
    bg(ctx, t, tint)
    return ctx


def finish(ctx, t):
    return bp_post(ctx.finish(), t)


# ───────────── açılış/kapanış kartı (ilk kare = son kare) ─────────────
def title_card(ctx, dy=0.0, t=0.0, wave_t=0.0):
    txt(ctx, 540, 372 + dy, "TİTANİK’TEN", 82, LINE)
    txt(ctx, 540, 505 + dy, "14 YIL ÖNCE", 140, AMBER)
    txt(ctx, 540, 660 + dy, "YAZILDI!", 170, (255, 255, 255))
    L(ctx, [(120, 765 + dy), (960, 765 + dy)], 5, AMBER, 1.0, 1.0)
    ship(ctx, 540, 1040 + dy, 0.62, 1.0, funnels=4, col=LINE, alpha=0.95)
    waves_line(ctx, 1080 + dy, wave_t, x0=100, x1=980, amp=7, rows=2)
    txt(ctx, 540, 1190 + dy, "6 BENZERLİK", 76, GREEN)


# ═══════════ A: kart → 1898 ile 1912 arası ═══════════
def scene_A(t, still=False):
    tt_ = 0.0 if still else t
    ctx = new(tt_, shake=not still)
    fall = ease_in(prog(tt_, 0.85, 1.3), 2.0)
    if tt_ < 1.35:
        title_card(ctx, dy=-2300 * fall if not still else 0.0, t=tt_, wave_t=0.0)
    if tt_ >= 0.95:
        u = tt_ - 0.95
        k = ease_out(prog(tt_, 0.95, 1.5), 3)
        # yıl sayacı 1898 → 1912
        yr = int(1898 + 14 * ease_io(prog(tt_, 1.3, wt("A", 9) + 0.1)))
        txt(ctx, 540, 560, str(yr), 210 * max(0.02, k), AMBER)
        # zaman çizelgesi
        x0, x1, y = 120, 960, 880
        L(ctx, [(x0, y), (x1, y)], 4, LINE, 1.0, ease_out(prog(tt_, 1.0, 1.6)))
        for i in range(15):
            xx = x0 + (x1 - x0) * i / 14
            r = prog(tt_, 1.3 + i * 0.05, 1.45 + i * 0.05)
            L(ctx, [(xx, y - (24 if i in (0, 14) else 12)), (xx, y + (24 if i in (0, 14) else 12))], 3.5, AMBER if yr >= 1898 + i else LINE_DIM, 1.0, r, glow=False)
        txt(ctx, x0, y + 70, "1898", 54, LINE, ease_out(prog(tt_, 1.4, 1.8)))
        txt(ctx, x1, y + 70, "1912", 54, LINE, ease_out(prog(tt_, 1.4, 1.8)))
        # kitap -> gemi simgesi
        L(ctx, [(x0 - 20, y - 130), (x0 + 80, y - 130), (x0 + 80, y - 40), (x0 - 20, y - 40), (x0 - 20, y - 130)], 4, LINE, 1.0, prog(tt_, 1.6, 2.3))
        L(ctx, [(x0 + 80, y - 118), (x0 + 96, y - 118), (x0 + 96, y - 52), (x0 + 80, y - 52)], 3, LINE_DIM, 1.0, prog(tt_, 1.9, 2.4), glow=False)
        ship(ctx, x1 - 40, y - 60, 0.16, prog(tt_, 2.0, 3.0), funnels=4)
        # 14 YIL ölçü çizgisi
        dim_line(ctx, x0 + 120, x1 - 180, y - 90, "14 YIL", 60, AMBER, ease_out(prog(tt_, 2.6, 3.4)))
        ship(ctx, 540, 1230, 0.6, prog(tt_, 2.2, 3.9), funnels=4, alpha=0.85)
        waves_line(ctx, 1275, tt_, rows=2)
    return finish(ctx, tt_)


# ═══════════ B: 6 benzerlik kontrol listesi ═══════════
def scene_B(t):
    u = t - st("B")
    ctx = new(t, 1.0 + 0.03 * prog(t, st("B"), en("B")))
    rows = ["01  ....................", "02  ....................", "03  ....................", "04  ....................", "05  ....................", "06  ???????????????????"]
    for i in range(6):
        y = 460 + i * 118
        ts = st("B") + 0.12 + i * 0.16
        k = ease_out(prog(t, ts, ts + 0.25), 3)
        if k <= 0:
            continue
        x0 = 90
        L(ctx, [(x0, y - 36), (x0 + 74, y - 36), (x0 + 74, y + 38), (x0, y + 38)], 4, LINE if i < 5 else RED, 1.0, k, closed=True)
        txt(ctx, x0 + 37, y + 2, f"{i+1}", 54, LINE if i < 5 else RED, k)
        L(ctx, [(x0 + 120, y + 30), (x0 + 120 + 780 * k, y + 30)], 3, LINE_DIM if i < 5 else RED, 0.9, 1.0, glow=False)
        if i < 5:
            txt(ctx, x0 + 150, y - 4, "· · ·", 56, LINE_DIM, k, anchor="lm")
        else:
            blink = 0.5 + 0.5 * math.sin(t * 9)
            txt(ctx, x0 + 150, y - 4, "? ? ? ?", 64, mix(RED, (255, 255, 255), blink * 0.5), k, anchor="lm")
    tw = wt("B", 6)
    if t >= tw - 0.05:
        kk = back_out(prog(t, tw - 0.05, tw + 0.2), 2.2)
        stamp(ctx, 760, 1210, "SON: ÜRKÜTÜCÜ", 56, RED, -6.0, kk)
    return finish(ctx, t)


# ═══════════ C: Futility romanı ═══════════
def scene_C(t):
    u = t - st("C")
    k = back_out(prog(u, 0.0, 0.4), 1.8)
    ctx = new(t, 1.0 + 0.05 * prog(t, st("C"), en("C")))
    X = Xf(540, 800, 1.0)
    bx = [(-290, -380), (290, -380), (290, 380), (-290, 380)]
    pts = [(540 + x * k, 800 + y * k) for x, y in bx]
    ctx.poly(pts, (10, 38, 78), 0.9)
    L(ctx, pts, 6, LINE, 1.0, 1.0, closed=True)
    L(ctx, [(540 + x * k * 0.92, 800 + y * k * 0.93) for x, y in bx], 3, LINE_DIM, 0.8, 1.0, closed=True, glow=False)
    ty = wt("C", 3)
    title = typed("FUTILITY", wt("C", 3) - 0.35, t, 11.0)
    txt(ctx, 540, 560, title + ("_" if int(t * 3) % 2 == 0 and len(title) < 8 else ""), 92, AMBER)
    year = typed("1898", wt("C", 0), t, 6.0)
    txt(ctx, 540, 690, year, 70, LINE)
    L(ctx, [(300, 740), (780, 740)], 3, LINE_DIM, 1.0, prog(t, st("C") + 0.5, st("C") + 1.0), glow=False)
    txt(ctx, 540, 800, "M. ROBERTSON", 46, LINE_DIM, ease_out(prog(t, wt("C", 3), wt("C", 3) + 0.3)))
    ship(ctx, 540, 1000, 0.42, prog(t, st("C") + 0.4, st("C") + 2.8), funnels=3, alpha=0.95)
    waves_line(ctx, 1030, t, 300, 780, rows=2, amp=5)
    return finish(ctx, t)


# ═══════════ D: batmaz ═══════════
def scene_D(t):
    u = t - st("D")
    ctx = new(t)
    rev = prog(t, st("D"), st("D") + 1.4)
    txt(ctx, 160, 430, "ROMAN · 1898", 44, LINE_DIM, ease_out(prog(t, st("D"), st("D") + 0.3)), anchor="lm")
    ship(ctx, 540, 740, 0.7, rev, funnels=3, alpha=0.95)
    waves_line(ctx, 780, t, rows=2)
    txt(ctx, 160, 840, "GERÇEK · 1912", 44, LINE_DIM, ease_out(prog(t, st("D") + 0.3, st("D") + 0.6)), anchor="lm")
    ship(ctx, 540, 1150, 0.7, prog(t, st("D") + 0.25, st("D") + 1.6), funnels=4, alpha=0.95)
    waves_line(ctx, 1190, t, rows=2)
    tb = wt("D", 3)
    if t >= tb - 0.02:
        k = ease_out(prog(t, tb - 0.02, tb + 0.14), 3)
        stamp(ctx, 400, 640, "BATMAZ!", 100 * (2.0 - 1.0 * k), RED, -10.0, 1.0)
        stamp(ctx, 700, 1050, "BATMAZ!", 100 * (2.0 - 1.0 * k), RED, 8.0, 1.0)
    return finish(ctx, t)


# ═══════════ E: Nisan gecesi, buzdağı ═══════════
def scene_E(t):
    u = t - st("E")
    ctx = new(t, tint=0.15)
    # takvim + ay
    L(ctx, [(110, 400), (390, 400), (390, 560), (110, 560), (110, 400)], 4, LINE, 1.0, prog(t, st("E"), st("E") + 0.6))
    L(ctx, [(110, 450), (390, 450)], 3, LINE_DIM, 1.0, prog(t, st("E") + 0.2, st("E") + 0.6), glow=False)
    txt(ctx, 250, 425, "NİSAN", 38, AMBER, ease_out(prog(t, st("E") + 0.2, st("E") + 0.6)))
    txt(ctx, 250, 520, "GECE", 52, LINE, ease_out(prog(t, st("E") + 0.3, st("E") + 0.7)))
    moon = circ_pts(800, 470, 70)
    L(ctx, moon, 5, LINE, 1.0, prog(t, st("E") + 0.1, st("E") + 0.9))
    L(ctx, circ_pts(830, 450, 58), 4, LINE_DIM, 0.9, prog(t, st("E") + 0.5, st("E") + 1.2), glow=False)
    # gemi yaklaşıyor, buzdağı
    th = wt("E", 5)
    approach = ease_in(prog(t, st("E") + 0.6, th), 1.6)
    sx = lerp(130, 360, approach)
    iceberg(ctx, 860, 1000, 0.9, prog(t, st("E") + 0.4, st("E") + 1.5), t)
    ship(ctx, sx, 1000, 0.55, prog(t, st("E") + 0.3, st("E") + 1.4), funnels=4, bob=3 * math.sin(t * 2))
    waves_line(ctx, 1000, t, rows=3)
    txt(ctx, 540, 720, "KUZEY ATLANTİK", 56, LINE_DIM, ease_out(prog(t, st("E") + 1.0, st("E") + 1.5)))
    if t >= th:
        a = t - th
        for i in range(14):
            ang = i * 0.45
            r0, r1 = 40 + 20 * (i % 2), 200 + 90 * (i % 3)
            k = ease_out(prog(a, 0, 0.35), 2)
            L(ctx, [(sx + 270 + math.cos(ang) * r0, 960 + math.sin(ang) * r0 * 0.8), (sx + 270 + math.cos(ang) * r1 * k, 960 + math.sin(ang) * r1 * 0.8 * k)], 5, AMBER if i % 2 else RED,
              1 - prog(a, 0.2, 0.7), 1.0, glow=False)
    return finish(ctx, t)


# ═══════════ F: sancak tarafı ═══════════
def scene_F(t):
    u = t - st("F")
    ctx = new(t)
    for j, (y, lab) in enumerate(((640, "ROMAN"), (980, "GERÇEK"))):
        k = prog(t, st("F") + 0.1 * j, st("F") + 0.8 + 0.1 * j)
        txt(ctx, 110, y - 120, lab, 44, LINE_DIM, k, anchor="lm")
        topdown_ship(ctx, 460, y, 0.75, k)
        # buzdağı (sağ taraf = sancak, ekranda alt kenar)
        ice = circ_pts(300, y + 98, 52, 40, 9)
        L(ctx, ice, 5, LINE, 1.0, prog(t, st("F") + 0.5, st("F") + 1.0))
    ts = wt("F", 3)
    if t >= ts - 0.05:
        k = ease_out(prog(t, ts - 0.05, ts + 0.4), 2)
        for y in (640, 980):
            L(ctx, [(460 - 340 * 0.75, y + 38), (460 + 200 * 0.75, y + 38)], 9, RED, 1.0, k)
        txt(ctx, 540, 790, "SANCAK", 86 * max(0.02, k), RED)
        txt(ctx, 540, 1150, "(sağ taraf)", 48, LINE_DIM, k)
    return finish(ctx, t)


# ═══════════ G: cankurtaran botları ═══════════
def scene_G(t):
    u = t - st("G")
    ctx = new(t)
    txt(ctx, 270, 470, "ROMAN", 44, LINE_DIM, ease_out(prog(t, st("G"), st("G") + 0.3)))
    txt(ctx, 810, 470, "GERÇEK", 44, LINE_DIM, ease_out(prog(t, st("G"), st("G") + 0.3)))
    L(ctx, [(540, 430), (540, 1200)], 3, LINE_DIM, 0.7, ease_out(prog(t, st("G"), st("G") + 0.5)), glow=False)
    for side, n, cx0 in ((0, 24, 270), (1, 20, 810)):
        for i in range(n):
            r, c = divmod(i, 4)
            tsx = st("G") + 0.3 + i * 0.045
            k = prog(t, tsx, tsx + 0.12)
            if k > 0:
                lifeboat(ctx, cx0 - 150 + c * 100, 600 + r * 104, 0.9, k)
        cnt = int(clamp((t - st("G") - 0.3) / (n * 0.045), 0, 1) * n)
        txt(ctx, cx0, 1215, str(cnt), 110, AMBER if cnt == n else LINE, 1.0)
    tw = wt("G", 5)
    if t >= tw - 0.05:
        kk = back_out(prog(t, tw - 0.05, tw + 0.25), 2.2)
        stamp(ctx, 540, 1090, "YETERSİZ!", 96, RED, -6.0, kk)
    return finish(ctx, t)


# ═══════════ H: boy karşılaştırması ═══════════
def scene_H(t):
    u = t - st("H")
    ctx = new(t, 1.0 + 0.12 * prog(t, st("H"), en("H")), cx=540, cy=900)
    base = 880
    ship(ctx, 540, base, 0.95, prog(t, st("H"), st("H") + 1.3), funnels=4, alpha=0.6, col=GREEN, bob=5 * math.sin(t * 2.2))
    ship(ctx, 540 + 0.0, base, 0.95 * 244 / 269, prog(t, st("H") + 0.2, st("H") + 1.5), funnels=3, alpha=1.0, col=AMBER, bob=5 * math.sin(t * 2.2 + 0.6))
    waves_line(ctx, base + 46, t, rows=2)
    sx_ = 80 + 920 * (((t - st("H")) * 0.55) % 1.0)
    L(ctx, [(sx_, 520), (sx_, 960)], 3, AMBER, 0.55, 1.0, glow=False)
    t1, t2 = wt("H", 4), wt("H", 7)
    L_t = 505 * 0.95 * 244 / 269
    L_T = 505 * 0.95
    if t >= t1 - 0.05:
        dim_line(ctx, 540 - L_t, 540 + L_t, base + 190, "244 m", 56, AMBER, ease_out(prog(t, t1 - 0.05, t1 + 0.5)))
    if t >= t2 - 0.05:
        dim_line(ctx, 540 - L_T, 540 + L_T, base + 330, "269 m", 56, GREEN, ease_out(prog(t, t2 - 0.05, t2 + 0.5)))
    txt(ctx, 110, 440, "ROMAN", 44, AMBER, 1.0, anchor="lm")
    txt(ctx, 110, 495, "GERÇEK", 44, GREEN, 1.0, anchor="lm")
    return finish(ctx, t)


# ═══════════ I: Titan ═══════════
def scene_I(t):
    u = t - st("I")
    ctx = new(t, 1.0 + 0.04 * prog(t, st("I"), en("I")))
    ts = wt("I", 5)
    word = typed("TİTAN", wt("I", 0), t, 7.0) if t < ts else "TİTAN"
    k = back_out(prog(t, ts, ts + 0.22), 2.2) if t >= ts else 1.0
    sz = 200 * (max(0.02, k) if t >= ts else 1.0)
    txt(ctx, 540, 760, word, sz, AMBER)
    L(ctx, [(120, 900), (960, 900)], 6, AMBER, 1.0, ease_out(prog(t, wt("I", 3), wt("I", 5) + 0.3)))
    txt(ctx, 540, 520, "ROMANDAKİ GEMİ", 50, LINE_DIM, ease_out(prog(t, wt("I", 2), wt("I", 3))))
    ship(ctx, 540, 1190, 0.7, prog(t, st("I"), st("I") + 1.8), funnels=3, alpha=0.9)
    waves_line(ctx, 1230, t, rows=2)
    if t >= ts:
        for i in range(12):
            a = i * math.pi / 6
            r0 = 300 + 40 * k
            L(ctx, [(540 + math.cos(a) * r0, 760 + math.sin(a) * r0 * 0.6), (540 + math.cos(a) * (r0 + 60), 760 + math.sin(a) * (r0 + 60) * 0.6)], 5, AMBER,
              clamp(1 - (t - ts) * 2), 1.0, glow=False)
    return finish(ctx, t)


# ═══════════ J: Titanik ═══════════
def scene_J(t):
    u = t - st("J")
    ctx = new(t, 1.0 + 0.07 * prog(t, st("J"), en("J")), tint=0.10)
    ts = wt("J", 4)
    txt(ctx, 540, 520, "GERÇEK GEMİ", 50, LINE_DIM, ease_out(prog(t, st("J"), st("J") + 0.3)))
    txt(ctx, 120, 760, "TİTAN", 200, AMBER, 1.0, anchor="lm")
    k = ease_out(prog(t, ts, ts + 0.12), 3)
    if t >= ts - 0.02:
        txt(ctx, 720, 760, "İK", 200 * (2.2 - 1.2 * k), RED, 1.0, anchor="lm")
    ship(ctx, 540, 1190, 0.7, prog(t, st("J"), st("J") + 1.4), funnels=4, alpha=0.9, bob=5 * math.sin(t * 2.2))
    waves_line(ctx, 1235, t, rows=2)
    return finish(ctx, t)


# ═══════════ K: kehanet mi? hayır — denizcilik ═══════════
def scene_K(t):
    u = t - st("K")
    ctx = new(t, 1.0 + 0.03 * prog(t, st("K"), en("K")))
    k0 = ease_out(prog(t, st("K"), st("K") + 0.25), 2)
    txt(ctx, 540, 500, "KEHANET?", 130 * max(0.02, k0), LINE)
    tx = wt("K", 2)
    if t >= tx:
        cross(ctx, 540, 500, 3.6, ease_out(prog(t, tx, tx + 0.3)), RED)
    # dümen simidi
    td = wt("K", 4)
    r = ease_out(prog(t, td, td + 0.9), 2)
    cx, cy, R = 540, 1000, 200
    L(ctx, circ_pts(cx, cy, R), 6, AMBER, 1.0, r)
    L(ctx, circ_pts(cx, cy, R * 0.28), 5, AMBER, 1.0, r)
    for i in range(8):
        a = i * math.pi / 4 + t * 0.35
        L(ctx, [(cx + math.cos(a) * R * 0.28, cy + math.sin(a) * R * 0.28), (cx + math.cos(a) * (R + 70), cy + math.sin(a) * (R + 70))], 6, AMBER, 1.0, r)
        L(ctx, circ_pts(cx + math.cos(a) * (R + 80), cy + math.sin(a) * (R + 80), 14, n=10), 4, AMBER, 1.0, r, glow=False)
    tb = wt("K", 7)
    if t >= tb - 0.1:
        check(ctx, 540, 1000, 1.6, ease_out(prog(t, tb - 0.1, tb + 0.35)))
        txt(ctx, 540, 650, "DENİZCİLİK BİLGİSİ", 52, GREEN, ease_out(prog(t, tb - 0.1, tb + 0.3)), stroke=6)
    return finish(ctx, t)


# ═══════════ L: başa dönüş — kart ═══════════
def scene_L(t):
    u = t - st("L")
    ctx = new(t)
    k = ease_out(prog(t, st("L") - 0.04, st("L") + 0.35), 3)
    shiver = (rng_hash(int(t * 24), 1) - 0.5) * 6 * (1 - prog(t, st("L") + 0.4, cues.FINAL_T)) if t > st("L") else 0.0
    title_card(ctx, dy=(1 - k) * 1500 + shiver, t=t, wave_t=0.0)
    return finish(ctx, t)


def _funcs():
    return [scene_A, scene_B, scene_C, scene_D, scene_E, scene_F, scene_G, scene_H, scene_I, scene_J, scene_K, scene_L]


def render_group(g, t):
    return _funcs()[g](t)
