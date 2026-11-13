"""Emu Savaşı (1932) — 11 sahne. Her fonksiyon t için 1080x1920 RGB döndürür (kömür dokusu uygulanmış)."""
import math

import cues
from art import *  # noqa
from art import _circle_pts, D2R
from ui import fmt
from cues import st, wt, we, en
from engine import *  # noqa
from sketch import *  # noqa

GY = 1130  # yer çizgisi


def new_ctx(t, cam=(W / 2, H / 2, 1.0), shake=True):
    ctx = Ctx()
    sx, sy = cues.shake(t) if shake else (0, 0)
    ctx.cam(cam[0], cam[1], cam[2], (sx, sy))
    paper_bg(ctx)
    return ctx


def big_text(ctx, x, y, s, px, col=INK, path=FONT_POP, rot_jit=True, t=0.0, stroke=0):
    b = bucket(t)
    ctx.text(x + 4, y + 5, s, px, mix(PAPER, INK, 0.28), path=path)
    ctx.text(x + (rng_hash(7, b) - 0.5) * 2, y + (rng_hash(8, b) - 0.5) * 2, s, px, col, path=path,
             stroke=stroke, stroke_fill=PAPER if stroke else None)


def underline(ctx, x0, x1, y, t, reveal=1.0, col=ACC, seed=3):
    sline(ctx, [(x0, y), ((x0 + x1) / 2, y + 8), (x1, y - 4)], 9, col, seed, t, amp=2.0, passes=2, reveal=reveal, smooth=True)


def ground(ctx, y, t, scroll=0.0, x0=-300, x1=1400, tufts=True):
    sline(ctx, [(x0, y), (x1, y + 6)], 6, INK, 5, t, amp=2.5, passes=2, step=40)
    for i in range(-2, 40):
        x = (i * 88 + 30 - scroll) % (x1 - x0 + 200) + x0 - 100
        h = 10 + 12 * rng_hash(i, 5)
        sline(ctx, [(x, y + 24 + 6 * rng_hash(i, 6)), (x + 26, y + 24 + 6 * rng_hash(i, 6))], 3.5, GREY, i, t, amp=0.8, passes=1, soft=False)
        if tufts and i % 2 == 0:
            for k in (-6, 0, 6):
                sline(ctx, [(x + 40 + k, y + 2), (x + 40 + k * 1.6, y - h)], 3.2, INK2, i + k, t, amp=0.6, passes=1, soft=False)


def puff(ctx, x, y, r, age, t, col=LIGHT, seed=0):
    if age < 0 or age > 1:
        return
    k = ease_out(age, 2)
    rr = r * (0.5 + k)
    pts = _circle_pts(x, y - 30 * k, rr, rr * 0.8, 9)
    wash(ctx, pts, col, 0.55 * (1 - age), t=t, seed=seed, off=(0, 0))
    shape(ctx, pts, GREY, 4, seed, t, 2.0, alpha=1 - age, passes=1)


def rays(ctx, cx, cy, t, n=14, inner=520, outer=900, col=ACC, alpha=0.9):
    b = bucket(t)
    for i in range(n):
        a = i * 2 * math.pi / n + 0.1
        r0 = inner + rng_hash(i, b, 3) * 30
        r1 = outer + rng_hash(i, b, 4) * 90
        sline(ctx, [(cx + math.cos(a) * r0, cy + math.sin(a) * r0 * 0.75), (cx + math.cos(a) * r1, cy + math.sin(a) * r1 * 0.75)], 6, col, i, t,
              amp=1.5, passes=1, alpha=alpha, soft=False)


# ═══════════ A: skor tabelası → yürüyen ordu vs emuların sürüsü ═══════════
def scene_A(t, still=False):
    u = t - 0.5
    ctx = new_ctx(t, (W / 2, H / 2, 1.0 + 0.012 * min(t, 3.4)))
    # skor tabelası düşer
    fall = clamp(u / 0.65)
    if t >= 0.45:
        ground(ctx, GY, t, scroll=t * 40)
        # emu sürüsü (sağ)
        k = back_out(prog(t, 0.55, 1.05), 1.8)
        for i, (ex, ey, es) in enumerate(((1010, GY - 4, 0.80), (860, GY - 4, 0.70), (730, GY - 60, 0.50), (940, GY - 70, 0.45), (640, GY - 84, 0.38),
                                          (800, GY - 96, 0.36), (1040, GY - 100, 0.34))):
            if k > 0.05:
                step_in = 120 * (1 - k)
                emu(ctx, ex + step_in - (t - 1.0) * 14, ey, es * 1.25 * (0.9 + 0.1 * k), t, phase=0, flip=-1, mood=-1 if es > 0.6 else 0, seed=10 + i, run=False)
        # yürüyen askerler
        fell = prog(t, wt("A", 8), wt("A", 8) + 0.35)
        for i in range(5):
            sx = 40 + i * 132 + (t - 1.0) * 70
            sy = GY + 2 - 3 * i % 2
            if fell <= 0:
                soldier(ctx, sx, sy, 1.2, t, phase=t * 9 + i, pose="run", seed=30 + i, mood=0)
            else:
                ang = -86 * ease_out(fell, 3) * (1 if i % 2 == 0 else 1)
                soldier(ctx, sx + 40 * fell, sy - 20 * math.sin(fell * math.pi) * (1 if i % 2 else 0.5), 1.2, t, phase=0, pose="slump", seed=30 + i,
                        rot=ang, mood=1)
                puff(ctx, sx + 60, sy, 50, (t - wt("A", 8) - 0.2 - i * 0.04) / 0.8, t, seed=i)
        # 20.000
        a2 = max(wt("A", 2), 0.95)
        if t >= a2 - 0.05:
            k2 = back_out(prog(t, a2 - 0.05, a2 + 0.25), 2.2)
            big_text(ctx, 540, 600, "20.000", 230 * max(0.01, k2), ACC, FONT_LORA, t=t)
            underline(ctx, 220, 860, 700, t, ease_out(prog(t, a2 + 0.1, a2 + 0.6)), INK)
            big_text(ctx, 540, 770, "EMU", 90 * max(0.01, k2), INK, FONT_POP, t=t)
        if t >= wt("A", 8):
            k3 = back_out(prog(t, wt("A", 8), wt("A", 8) + 0.25), 2.5)
            sline(ctx, [(120, 930), (560, 1110)], 18 * k3, ACC, 5, t, amp=3, passes=2)
            sline(ctx, [(560, 930), (120, 1110)], 18 * k3, ACC, 6, t, amp=3, passes=2)
    # tabela
    ctx.parallax(0)
    if t < 1.5:
        rot = 0.0
        yo = 0.0
        if u > 0:
            rot = -16 * ease_in(fall, 2)
            yo = 2300 * ease_in(fall, 2.4)
        else:
            rot = 1.6 * math.sin(t * 7) * (t / 1.0) if not still else 0.0
        if t < 1.4:
            rays(ctx, 540, 840, 0.0 if still else t, alpha=1.0 if u < 0 else 1 - fall * 1.6)
            scoreboard(ctx, 540, 840 + yo, 1.06, 0.0 if still else t, emu_score=1, rot=rot)
    ctx.parallax(1)
    return charcoal_post(ctx.finish(), 0.0 if still else t, still=still)


# ═══════════ B: gizli rapor dosyası ═══════════
def scene_B(t):
    u = t - st("B")
    ctx = new_ctx(t, (W / 2, H / 2, 1.0 + 0.03 * prog(t, st("B"), en("B"))))
    # arka plan serpiştirmeleri
    rays(ctx, 540, 800, t, n=10, inner=480, outer=640, col=LIGHT, alpha=0.8)
    k = back_out(prog(u, 0.0, 0.4), 2.4)
    wob = 4 * math.sin(u * 16) * math.exp(-u / 1.4) + 1.4 * math.sin(u * 5)
    drop = (1 - ease_out(prog(u, 0, 0.4), 3)) * -500
    if k > 0.02:
        folder(ctx, 540, 800 + drop, 1.55 * k, t, wob=wob)
    # GİZLİ damgası
    ts = wt("B", 4)
    if t >= ts:
        k2 = ease_out(prog(t, ts, ts + 0.14), 3)
        X = Xf(600, 650, 1.0, rot=-14)
        pts = X.pts([(-200, -62), (200, -62), (200, 62), (-200, 62)])
        shape(ctx, pts, ACC, 10, 77, t, 2.0, smooth=False)
        ctx.text(*X.p(0, 4), "GİZLİ", 120 * (2.2 - 1.2 * k2), ACC, path=FONT_LORA)
    # büyüteç
    mx, my = 540 + 260 * math.sin(u * 2.1), 800 + 160 * math.sin(u * 3.3 + 1)
    shape(ctx, _circle_pts(mx, my, 88, 88, 14), INK, 11, 12, t, 2.0)
    ctx.circ(mx, my, 84, (200, 225, 232), 0.35)
    sline(ctx, [(mx + 62, my + 62), (mx + 140, my + 140)], 20, INK2, 13, t, amp=1.5)
    # sona kadar izle oku
    if t >= wt("B", 2):
        k3 = back_out(prog(t, wt("B", 2), wt("B", 2) + 0.3), 2.0)
        big_text(ctx, 540, 1130, "SONA KADAR İZLE", 62 * max(0.01, k3), INK, FONT_POP, t=t)
        sline(ctx, [(540, 1170), (540, 1230 + 8 * math.sin(t * 10))], 9, ACC, 14, t, amp=1.0, passes=1)
        sline(ctx, [(510, 1206 + 8 * math.sin(t * 10)), (540, 1238 + 8 * math.sin(t * 10)), (570, 1206 + 8 * math.sin(t * 10))], 9, ACC, 15, t, amp=1.0, passes=1)
    return charcoal_post(ctx.finish(), t)


# ═══════════ C: 1932, Avustralya haritası ═══════════
def scene_C(t):
    u = t - st("C")
    zin = ease_io(prog(t, wt("C", 3), en("C")))
    # WA'ya zoom
    wa_c = (350, 760)
    cam = (lerp(540, 430, zin), lerp(960, 780, zin), lerp(1.0, 1.35, zin))
    ctx = new_ctx(t, cam)
    # harita çizimi
    reveal = ease_out(prog(t, st("C") - 0.15, st("C") + 0.85), 2)
    X = australia(ctx, 540, 760, 1.5, t, reveal=reveal, wa=ease_out(prog(t, wt("C", 3), wt("C", 3) + 0.5)))
    # eski kıtalar: küçük emu yürüyüşü (kıyıda)
    emu(ctx, 190 + 70 * math.sin(t * 0.8), 1030, 0.38, t, phase=t * 6, flip=1, mood=1, seed=3, run=True, alpha=0.9)
    # iğne: buğday kuşağı
    tp = wt("C", 4)
    if t >= tp:
        px_, py_ = X.p(*WHEATBELT)
        drop = (1 - ease_out(prog(t, tp, tp + 0.3), 3)) * 220
        pin(ctx, px_, py_ - drop, 1.0, t)
        if t > tp + 0.3:
            kk = ((t - tp - 0.3) * 1.3) % 1.0
            ctx.ring(px_, py_, 18 + 60 * kk, 5, ACC, 0.8 * (1 - kk))
    # GERÇEK damgası
    tg = wt("C", 1)
    if tg <= t < wt("C", 2) + 0.2:
        k2 = ease_out(prog(t, tg, tg + 0.14), 3)
        fade = 1 - prog(t, wt("C", 2), wt("C", 2) + 0.18)
        ctx.parallax(0)
        X2 = Xf(540, 520, 1.0, rot=-8)
        pts = X2.pts([(-320, -90), (320, -90), (320, 90), (-320, 90)])
        ctx.poly(pts, PAPER, 0.92 * fade)
        shape(ctx, pts, ACC, 12, 21, t, 2.4, smooth=False, alpha=fade)
        ctx.text(*X2.p(0, 6), "BU GERÇEK!", 128 * (2.0 - 1.0 * k2), ACC, path=FONT_POP)
        ctx.parallax(1)
    # 1932
    ty = wt("C", 3)
    if t >= ty - 0.05:
        ctx.parallax(0)
        k = back_out(prog(t, ty - 0.05, ty + 0.3), 2.2)
        # kilometre sayacı gibi dönen rakamlar
        yr = 1932 if t > ty + 0.35 else int(1900 + 32 * ease_out(prog(t, ty - 0.05, ty + 0.35)))
        big_text(ctx, 540, 470, str(yr), 250 * max(0.01, k), INK, FONT_LORA, t=t)
        underline(ctx, 200, 880, 590, t, ease_out(prog(t, ty + 0.2, ty + 0.7)), ACC)
        ctx.parallax(1)
    return charcoal_post(ctx.finish(), t)


# ═══════════ D: buğday tarlası + 20.000 emu ═══════════
def scene_D(t):
    u = t - st("D")
    z = 1.0 + 0.04 * prog(t, st("D"), en("D"))
    ctx = new_ctx(t, (540, 1000, z))
    xf = 1350 - 245 * u  # emu önü (sola doğru ilerler)
    eaten = lambda x: ease_out(clamp((x - xf) / 220.0), 2)
    ground(ctx, GY, t, tufts=False)
    wheat(ctx, -60, 1160, GY + 18, t, h=250, step=30, eaten=eaten)
    # emular
    offs = [(30, 0, 1.15), (190, -30, 0.92), (350, 10, 1.08), (110, -66, 0.74), (290, -84, 0.68), (480, -40, 0.8), (-60, -80, 0.7)]
    for i, (dx, dy, es) in enumerate(offs):
        ex = xf + dx + 30
        if -100 < ex < 1300:
            emu(ctx, ex, GY + 8 + dy, es, t, phase=t * 3 + i, flip=-1, mood=1, seed=50 + i, run=False)
    # çiftçi
    fk = back_out(prog(t, st("D") + 0.05, st("D") + 0.45), 2.2)
    farmer(ctx, 170, GY + 12 + (1 - fk) * 300, 1.75, t, anger=1.0)
    # 20.000 sayacı
    td = wt("D", 2)
    ctx.parallax(0)
    if t >= td - 0.05:
        val = int(20000 * ease_out(prog(t, td - 0.05, td + 0.9), 2))
        k = back_out(prog(t, td - 0.05, td + 0.25), 2.2)
        big_text(ctx, 600, 450, f"{val:,}".replace(",", "."), 190 * max(0.01, k), ACC, FONT_LORA, t=t)
        big_text(ctx, 600, 575, "EMU", 96 * max(0.01, k), INK, FONT_POP, t=t)
    # "yiyip bitiriyordu" : kemirme çizgileri
    if t >= wt("D", 6):
        for i in range(5):
            a = rng_hash(i, bucket(t)) * 6.28
            sline(ctx, [(850 + math.cos(a) * 60, 900 + math.sin(a) * 40), (850 + math.cos(a) * 100, 900 + math.sin(a) * 66)], 6, ACC, i, t, amp=1, passes=1)
    ctx.parallax(1)
    return charcoal_post(ctx.finish(), t)


# ═══════════ E: askerler + makineli tüfek + 10.000 mermi ═══════════
def scene_E(t):
    u = t - st("E")
    ctx = new_ctx(t, (540, 1000, 1.0 + 0.04 * prog(t, st("E"), en("E"))))
    ground(ctx, GY, t, tufts=False)
    ts = wt("E", 2)
    # ÇÖZÜM? (başta)
    if t < ts + 0.15:
        k = back_out(prog(t, st("E"), st("E") + 0.25), 2.4)
        big_text(ctx, 540, 600, "ÇÖZÜM?", 190 * max(0.01, k), ACC, FONT_LORA, t=t)
        bulb = back_out(prog(t, st("E") + 0.4, st("E") + 0.7), 2.2)
        shape(ctx, _circle_pts(540, 760, 34 * bulb, 40 * bulb, 12), INK, 6, 90, t, 1.5)
    # askerler koşarak girer, "Askerler" kelimesinde selam
    for i, (sx, pose) in enumerate(((90, "salute"), (240, "aim"), (390, "salute"))):
        run_k = ease_out(prog(t, st("E"), ts), 2)
        x = sx - 520 * (1 - run_k)
        if t < ts:
            soldier(ctx, x, GY + 8, 1.55, t, phase=t * 10 + i, pose="run", seed=60 + i, mood=1)
        else:
            hop = 14 * math.exp(-(t - ts) * 7) * abs(math.sin((t - ts) * 14))
            soldier(ctx, sx, GY + 8 - hop, 1.55, t, 0.0, 1, pose, seed=60 + i, mood=1)
    tl = wt("E", 3)
    kl = ease_out(prog(t, tl, tl + 0.3), 3)
    gx = 640
    if kl > 0.01:
        fl = 1.0 if cues.firing(t, 0.05) else 0.0
        lewis(ctx, gx - (1 - kl) * 800, GY + 10, 1.7, t, flash=fl, recoil=fl)
        for s0 in cues.SHOTS:
            a = t - s0
            if 0 <= a < 0.28:
                bx = gx + 300 * 1.0 + a * 2600
                bullet(ctx, bx, GY - 124, 1.2, 0, 7)
                sline(ctx, [(bx - 180, GY - 124), (bx - 30, GY - 124)], 3, GREY, 8, t, amp=0.4, passes=1, alpha=0.6, soft=False)
    # mermi sandığı (yukarıdan düşer, havada sallanır)
    tc = wt("E", 6)
    if t >= tc:
        drop = (1 - ease_out(prog(t, tc, tc + 0.35), 2.2)) * -900
        sway = 6 * math.sin((t - tc) * 3.4)
        cx, cy = 790, 640 + drop + 8 * math.sin((t - tc) * 5)
        X = Xf(cx, cy, 1.25, rot=sway)
        sline(ctx, [X.p(-90, -100), (cx - 40, 330)], 6, INK2, 4, t, amp=1.0, passes=1)
        sline(ctx, [X.p(90, -100), (cx + 40, 330)], 6, INK2, 5, t, amp=1.0, passes=1)
        box = X.pts([(-130, -100), (130, -100), (130, 100), (-130, 100)])
        wash(ctx, box, (190, 150, 90), 0.95, t=t, seed=3, smooth=False)
        shape(ctx, box, INK, 8, 4, t, 2.0, smooth=False)
        for j in range(3):
            sline(ctx, X.pts([(-130, -100 + j * 70), (130, -100 + j * 70)]), 4, INK2, 5 + j, t, amp=1.0, passes=1)
        ctx.poly(X.pts([(-105, -38), (105, -38), (105, 36), (-105, 36)]), PAPER)
        ctx.text(*X.p(0, -2), "10.000", 88, INK, path=FONT_POP)
        for j in range(7):
            bullet(ctx, *X.p(-100 + j * 33, -126 + (j % 2) * 4), 1.1, -90, 20 + j, t)
    last = max([s0 for s0 in cues.SHOTS if s0 <= t] or [-9])
    if 0 <= t - last < 0.45 and ts + 0.5 < t:
        k = back_out(prog(t - last, 0, 0.12), 2.5)
        big_text(ctx, 350, 520 + 8 * math.sin(t * 60), "TAK TAK TAK!", 92 * max(0.01, k), ACC, FONT_POP, t=t)
    return charcoal_post(ctx.finish(), t)


# ═══════════ F: emular akıllı — zikzak ═══════════
def scene_F(t):
    u = t - st("F")
    ctx = new_ctx(t, (540, 1000, 1.0))
    HZ = 960
    ground(ctx, HZ, t, scroll=u * 250, tufts=False)
    SOLD = [(60, 1215), (190, 1215)]
    for i, (sx, sy) in enumerate(SOLD):
        soldier(ctx, sx, sy, 1.35, t, 0.0, 1, "aim", seed=70 + i)
    tb = wt("F", 3)
    split = ease_io(prog(t, wt("F", 4), wt("F", 6)))
    zz = ease_in(prog(t, wt("F", 7), wt("F", 7) + 0.4), 1.5)
    lanes = [(1040, 0.78), (1130, 0.98), (1222, 1.18)]
    members = [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)]
    for m, (lane, idx) in enumerate(members):
        base_y = lerp(1150 - 24 * idx, lanes[lane][0] - 10 * idx, split)
        sc = lerp(0.98, lanes[lane][1], split)
        ex = -160 + m * 150 + (t - st("F")) * 290 + 50 * (idx % 2)
        ez = ((ex + 260) % 1700) - 260
        zig = 60 * math.sin((t - wt("F", 7)) * 5.5 + m) * zz
        if -260 < ez < 1340:
            emu(ctx, ez, base_y + zig, sc, t, phase=t * 11 + m * 1.3, flip=1, mood=1, seed=80 + m, run=True)
    if t >= tb:
        k = back_out(prog(t, tb, tb + 0.3), 2.5)
        bx, by = 560, 560
        shape(ctx, _circle_pts(bx, by, 52 * k, 60 * k, 12), INK, 7, 90, t, 1.5)
        ctx.circ(bx, by, 47 * k, HL)
        sline(ctx, [(bx - 18 * k, by + 76 * k), (bx + 18 * k, by + 76 * k)], 10, INK, 91, t, amp=0.5, passes=1)
        for a_ in range(-60, 61, 30):
            sline(ctx, [(bx + math.sin(a_ * D2R) * 76 * k, by - math.cos(a_ * D2R) * 76 * k), (bx + math.sin(a_ * D2R) * 108 * k, by - math.cos(a_ * D2R) * 108 * k)],
                  7, ACC, a_, t, amp=1, passes=1)
    if t >= wt("F", 7) - 0.1:
        r = ease_out(prog(t, wt("F", 7) - 0.1, wt("F", 7) + 0.9), 2)
        pts = [(120 + i * 135, 700 + (80 if i % 2 else -40)) for i in range(8)]
        sline(ctx, pts, 12, ACC, 93, t, amp=1.8, passes=2, reveal=r)
    for s0 in cues.SHOTS:
        a = t - s0
        if 0 <= a < 0.3 and st("F") < s0 < en("F") + 0.2:
            tx = 480 + 520 * rng_hash(s0, 1)
            ty = 1100 + 120 * rng_hash(s0, 2)
            sx0, sy0 = 300, 1010
            k = a / 0.3
            bullet(ctx, lerp(sx0, tx, k), lerp(sy0, ty, k), 1.0, math.degrees(math.atan2(ty - sy0, tx - sx0)), 3, t)
            puff(ctx, tx, ty + 10, 44, (a - 0.2) / 0.5 if a > 0.2 else -1, t, col=LIGHT, seed=int(s0 * 10))
    for s0 in cues.SHOTS:
        if st("F") < s0 < en("F") + 0.2 and 0 <= t - s0 < 0.05:
            for sx, sy in SOLD:
                ctx.poly([(sx + 196, sy - 220), (sx + 250, sy - 244), (sx + 236, sy - 210), (sx + 276, sy - 194), (sx + 206, sy - 198)], HL)
    return charcoal_post(ctx.finish(), t)


# ═══════════ G: kamyon kovalamacası ═══════════
def scene_G(t):
    u = t - st("G")
    ctx = new_ctx(t, (540, 1000, 1.0))
    stop = ease_out(prog(t, wt("G", 5), wt("G", 7) + 0.3), 2)
    scroll = u * 700 * (1 - 0.95 * stop)
    ground(ctx, GY + 20, t, scroll=scroll)
    # hız çizgileri
    for i in range(7):
        ph = (u * 3 + i * 0.37) % 1.0
        ly = 700 + i * 70
        lx = 1200 - ph * 1500
        sline(ctx, [(lx, ly), (lx + 200, ly)], 5, LIGHT, i, t, amp=0.8, passes=1, alpha=0.8 * (1 - stop), soft=False)
    # emular (kamyondan hızlı)
    for i in range(5):
        ex = 640 + i * 70 + 380 * u * (0.9 + 0.1 * i / 4) * 1.2 + (-i % 2) * 20
        ey = GY + 22 + (i % 3) * 12 - 10 * i % 2
        if ex < 1400:
            emu(ctx, ex, ey, 0.92 + 0.07 * (i % 3), t, phase=t * 13 + i, flip=1, mood=1, seed=95 + i)
    # kamyon (sol) — kısa süre sonra durur
    sway = 7 * math.sin(t * 17) * (1 - stop)
    tx = 350 - 130 * stop
    X = truck(ctx, tx, GY + 20, 1.45, t, wheel=t * 18 * (1 - 0.9 * stop), bounce=sway)
    # kasada asker
    soldier(ctx, tx - 150, GY + 20 - 150 + sway - 30 * stop, 1.2, t, 0.0, 1, "aim" if stop < 0.5 else "slump", seed=100, rot=-30 * stop)
    # egzoz / buhar
    if stop > 0.1:
        for k in range(5):
            age = ((t * 1.2 + k * 0.2) % 1.0)
            puff(ctx, tx + 200 + k * 8, GY - 90, 52, age, t, col=LIGHT, seed=k)
    # tüfek ateşi ve izler
    for s0 in cues.SHOTS:
        a = t - s0
        if st("G") <= s0 < st("G") + 3.4 and 0 <= a < 0.25:
            k = a / 0.25
            sx0, sy0 = tx - 20, GY - 230
            tx2, ty2 = 900 + 200 * rng_hash(s0, 3), GY - 20 + 40 * rng_hash(s0, 4)
            bullet(ctx, lerp(sx0, tx2, k), lerp(sy0, ty2, k), 0.8, math.degrees(math.atan2(ty2 - sy0, tx2 - sx0)), 3, t)
    # 50 km/sa
    t50 = wt("G", 2)
    ctx.parallax(0)
    if t >= t50 - 0.05:
        k = back_out(prog(t, t50 - 0.05, t50 + 0.25), 2.3)
        big_text(ctx, 540, 470, "50 km/sa", 168 * max(0.01, k), ACC, FONT_LORA, t=t)
        underline(ctx, 150, 930, 560, t, ease_out(prog(t, t50 + 0.1, t50 + 0.6)), INK)
    if t >= wt("G", 7) - 0.1:
        k = back_out(prog(t, wt("G", 7) - 0.1, wt("G", 7) + 0.2), 2.3)
        big_text(ctx, 540, 700, "YETİŞEMEDİ", 96 * max(0.01, k), INK, FONT_POP, t=t)
    ctx.parallax(1)
    return charcoal_post(ctx.finish(), t)


# ═══════════ H: kaç mermi? ═══════════
def draw_H(ctx, t, k=1.0, fade=0.0):
    u = t - st("H")
    for i in range(18):
        ph = (u * (1.5 + 0.06 * i) + rng_hash(i, 1)) % 1.0
        x = 40 + rng_hash(i, 2) * 1000
        y = 330 - 80 + ph * 1100
        bullet(ctx, x, y, 0.9, 90, 5 + i, t)
    val = cues.ammo(t)
    rnd = lambda q: int(rng_hash(q, bucket(t * 3)) * 9)
    txt = fmt(val)
    if t < we("H", 4):
        digits = list(txt)
        n = 0
        for j in range(len(digits) - 1, -1, -1):
            if digits[j].isdigit() and n < 2:
                digits[j] = str(rnd(j + 5))
                n += 1
        txt = "".join(digits)
    box = [(60, 650), (1020, 646), (1024, 990), (56, 996)]
    ctx.poly(box, PAPER)
    shape(ctx, box, INK, 12, 6, t, 3.0, smooth=False)
    big_text(ctx, 540, 830, txt, 230 * max(0.01, k), INK, FONT_POP, t=t)
    big_text(ctx, 540, 1070, "MERMİ", 90 * max(0.01, k), ACC, FONT_POP, t=t)
    ctx.text(540 + 8 * math.sin(t * 20), 500 + 12 * math.sin(t * 9), "?", 280 * max(0.01, k), ACC, path=FONT_LORA, stroke=8, stroke_fill=INK)


def scene_H(t):
    u = t - st("H")
    ctx = new_ctx(t, (540, 960, 1.0 + 0.05 * prog(t, st("H"), en("H"))))
    draw_H(ctx, t, back_out(prog(u, 0.0, 0.3), 2.2))
    return charcoal_post(ctx.finish(), t)


# ═══════════ I: matematik ═══════════
def scene_I(t):
    u = t - st("I")
    ctx = new_ctx(t, (540, 960, 1.0))
    t1 = wt("I", 1)
    if t < t1 + 0.15:
        draw_H(ctx, t, 1.0)
        ctx.parallax(0)
        ctx.overlay_rgb(PAPER, ease_out(prog(t, t1 - 0.12, t1 + 0.12), 2))
        ctx.parallax(1)
    # satır 1: ≈10.000 mermi
    if t >= t1 - 0.05:
        k = back_out(prog(t, t1 - 0.05, t1 + 0.25), 2.3)
        big_text(ctx, 540, 440, "≈ 10.000", 176 * max(0.01, k), ACC, FONT_LORA, t=t)
        big_text(ctx, 540, 580, "MERMİ", 76 * max(0.01, k), INK, FONT_POP, t=t)
        for j in range(24):
            if t > t1 + 0.12 + j * 0.018:
                bullet(ctx, 130 + (j % 12) * 74, 660 + (j // 12) * 44, 1.2, -90, 30 + j, t)
    # satır 2: ≈1.000 EMU
    t2 = wt("I", 4)
    if t >= t2 - 0.05:
        k = back_out(prog(t, t2 - 0.05, t2 + 0.25), 2.3)
        big_text(ctx, 540, 840, "≈ 1.000 EMU", 128 * max(0.01, k), INK, FONT_LORA, t=t)
        for j in range(8):
            if t > t2 + 0.1 + j * 0.03:
                emu(ctx, 80 + j * 125, 1010, 0.2, t, flip=1, mood=1, seed=40 + j, run=False)
    # satır 3: kuş başına 10 mermi
    t3 = wt("I", 6)
    if t >= t3 - 0.05:
        ctx.parallax(0)
        ctx.overlay_rgb(PAPER, 1.0 * ease_out(prog(t, t3 - 0.05, t3 + 0.2)))
        ctx.parallax(1)
        ground(ctx, 1190, t, tufts=False)
        emu(ctx, 760, 1190, 1.1, t, flip=-1, mood=1, seed=77, run=False, hat=None)
        if t >= wt("I", 7):
            kk = back_out(prog(t, wt("I", 7), wt("I", 7) + 0.25), 2.3)
            big_text(ctx, 540, 480, "KUŞ BAŞINA", 124 * max(0.01, kk), INK, FONT_POP, t=t)
            underline(ctx, 140, 940, 560, t, ease_out(prog(t, wt("I", 7) + 0.1, wt("I", 7) + 0.5)), ACC)
        for j in range(10):
            tj = wt("I", 9) + j * 0.09
            a = t - tj
            if 0 <= a < 0.7:
                # kurşun gelir, sekip döner
                if a < 0.22:
                    bx = lerp(60, 590, a / 0.22)
                    by = 930 + (j % 5) * 26
                    bullet(ctx, bx, by, 1.2, 0, 31 + j, t)
                else:
                    kk = (a - 0.22) / 0.48
                    bx = lerp(590, 380, kk)
                    by = 930 + (j % 5) * 26 - 140 * math.sin(kk * math.pi) + 190 * kk * kk
                    bullet(ctx, bx, by, 1.2, 180 + 140 * kk, 31 + j, t)
                    if kk < 0.2:
                        ctx.glow(590, by, 50, HL, 0.9 * (1 - kk / 0.2))
        if t >= wt("I", 10):
            k = back_out(prog(t, wt("I", 10), wt("I", 10) + 0.25), 2.5)
            big_text(ctx, 260, 760, "10", 300 * max(0.01, k), ACC, FONT_LORA, t=t)
            big_text(ctx, 260, 930, "MERMİ", 70 * max(0.01, k), INK, FONT_POP, t=t)
            big_text(ctx, 260, 1010, "/ EMU", 70 * max(0.01, k), INK, FONT_POP, t=t)
    return charcoal_post(ctx.finish(), t)


# ═══════════ J: geri çekilme + komutanın itirafı ═══════════
def scene_J(t):
    u = t - st("J")
    ctx = new_ctx(t, (540, 1000, 1.0 + 0.03 * prog(t, st("J"), en("J"))))
    ground(ctx, GY, t, scroll=u * 90, tufts=False)
    ts = wt("J", 3)
    # yağmur bulutu
    cloud_doodle(ctx, 250, 520, 1.5, t, col=GREY)
    for k in range(14):
        ph = (t * 2.2 + k * 0.17) % 1.0
        x = 110 + k * 28
        sline(ctx, [(x, 580 + ph * 460), (x - 8, 600 + ph * 460)], 4, (90, 120, 160), k, t, amp=0.4, passes=1, soft=False)
    # geri çekilen askerler
    for i in range(4):
        sx = 780 - u * 135 - i * 170
        pose = "slump"
        soldier(ctx, sx, GY + 8, 1.4, t, phase=t * 6 + i, flip=-1, pose=pose, seed=110 + i, mood=0)
    # beyaz bayrak
    fx = 780 - u * 135 + 40
    sline(ctx, [(fx, GY - 90), (fx, GY - 280)], 7, INK2, 120, t, amp=1, passes=1)
    ctx.poly([(fx, GY - 280), (fx - 110, GY - 262 + 10 * math.sin(t * 7)), (fx - 100, GY - 220 + 10 * math.sin(t * 7)), (fx, GY - 232)], (252, 252, 248))
    shape(ctx, [(fx, GY - 280), (fx - 110, GY - 262 + 10 * math.sin(t * 7)), (fx - 100, GY - 220 + 10 * math.sin(t * 7)), (fx, GY - 232)], INK, 4, 121, t, 1.2, smooth=False)
    # gururlu emu (sağ)
    hat = "general" if t >= ts + 0.4 else None
    emu(ctx, 900, GY + 6, 1.3, t, phase=0, flip=-1, mood=1, seed=130, run=False, hat=hat, medal=t >= ts + 0.4)
    # komutan
    kc = back_out(prog(t, ts, ts + 0.35), 2.0)
    if kc > 0.02:
        soldier(ctx, 190, GY + 8 + (1 - kc) * 300, 1.85, t, 0.0, 1, "salute", seed=140, mood=1)
        # komutan şapka bandı
        ctx.circ(190 + 14, GY - 390 + (1 - kc) * 300, 11, HL)
    # düşünce balonu
    tb = wt("J", 7)
    if t >= tb:
        k = back_out(prog(t, tb, tb + 0.35), 2.2)
        thought_bubble(ctx, 540, 520, 380 * k, 190 * k, (300, 760), t)
        if k > 0.9:
            for j in range(5):
                ex = 250 + j * 150 + 18 * math.sin(t * 6 + j)
                emu(ctx, ex, 600 + 30 * math.sin(t * 9 + j) * 0.4, 0.27, t, phase=t * 8 + j, flip=1, mood=0, seed=150 + j, run=True, hat="helmet")
            if t >= wt("J", 13):
                ctx.glow(540, 520, 420, HL, 0.35 * (0.5 + 0.5 * math.sin(t * 14)))
    return charcoal_post(ctx.finish(), t)


# ═══════════ K: son skor ═══════════
def scene_K(t, still=False):
    u = t - st("K")
    ctx = new_ctx(t, (W / 2, H / 2, 1.0), shake=not still)
    k = back_out(prog(t, st("K") - 0.04, st("K") + 0.45), 1.5)
    sc = lerp(0.25, 1.06, k)
    rot = (1 - ease_out(prog(t, st("K") - 0.04, st("K") + 0.5), 3)) * 340
    tsc = wt("K", 4)
    emu_score = 1 if t >= tsc else 0
    pulse = math.exp(-(t - tsc) / 0.15) if t >= tsc else 0.0
    rays(ctx, 540, 840, t, alpha=clamp(k))
    scoreboard(ctx, 540, 840, sc, t, emu_score=emu_score, rot=rot, pulse=pulse)
    # konfeti çizgileri
    if t >= tsc:
        for i in range(16):
            a = i * 2 * math.pi / 16 + 0.3
            r = 380 + 520 * ease_out(prog(t, tsc, tsc + 0.6), 2)
            sline(ctx, [(540 + math.cos(a) * r, 840 + math.sin(a) * r * 0.8), (540 + math.cos(a) * (r + 40), 840 + math.sin(a) * (r + 40) * 0.8)], 8,
                  ACC if i % 2 else HL, i, t, amp=0.8, passes=1, alpha=1 - prog(t, tsc + 0.3, tsc + 0.9), soft=False)
    return charcoal_post(ctx.finish(), t, still=still)


def _scene_funcs():
    return [scene_A, scene_B, scene_C, scene_D, scene_E, scene_F, scene_G, scene_H, scene_I, scene_J, scene_K]


def render_group(g, t):
    return _scene_funcs()[g](t)
