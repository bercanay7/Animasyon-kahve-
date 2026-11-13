"""Kara kalem karakterler ve nesneler (emu, asker, Lewis tüfeği, kamyon, buğday, çiftçi, dosya, harita, skor tabelası)."""
import math

from engine import *  # noqa
from sketch import *  # noqa

D2R = math.pi / 180


def _circle_pts(cx, cy, rx, ry, n=14, a0=0.0):
    return [(cx + math.cos(a0 + i * 2 * math.pi / n) * rx, cy + math.sin(a0 + i * 2 * math.pi / n) * ry) for i in range(n)]


def _leg(ctx, X, hx, hy, ang, bend, up, lo, w, col, seed, t, foot=14):
    a1 = ang * D2R
    kx, ky = hx + math.sin(a1) * up, hy + math.cos(a1) * up
    a2 = (ang - bend) * D2R
    fx, fy = kx + math.sin(a2) * lo, ky + math.cos(a2) * lo
    sline(ctx, X.pts([(hx, hy), (kx, ky), (fx, fy)]), X.len(w), col, seed, t, amp=1.8, passes=2)
    # üç parmaklı ayak
    sline(ctx, X.pts([(fx - 4, fy), (fx + foot, fy + 2)]), X.len(w * 0.7), col, seed + 1, t, amp=1.2, passes=1)
    sline(ctx, X.pts([(fx - 4, fy), (fx + foot * 0.6, fy - 7)]), X.len(w * 0.5), col, seed + 2, t, amp=1.0, passes=1)
    return fx, fy


# ═══════════════════════════ EMU ═══════════════════════════
def emu(ctx, x, y, s=1.0, t=0.0, phase=0.0, flip=1, mood=0, seed=1, run=True, hat=None, medal=False, alpha=1.0, rot=0.0, eye=1.0):
    """Sağa bakan emu. y: yer çizgisi. mood: -1 kızgın, 0 nötr, 1 sırıtan"""
    X = Xf(x, y, s, flip=flip, rot=rot)
    bob = -7 * abs(math.sin(phase * 0.5)) if run else 2 * math.sin(t * 3 + seed)
    # arka bacak
    sw = lambda o: math.sin(phase + o)
    lf = lambda o: max(0.0, math.cos(phase + o))
    if run:
        _leg(ctx, X, -20, -140 + bob, 30 * sw(2.6) + 4, 10 + 70 * lf(2.6), 70, 80, 8, GREY, seed, t)
        _leg(ctx, X, 16, -140 + bob, 30 * sw(0.0) + 4, 10 + 70 * lf(0.0), 70, 80, 9, INK2, seed + 3, t)
    else:
        _leg(ctx, X, -20, -140 + bob, 3, 8, 70, 80, 8, GREY, seed, t)
        _leg(ctx, X, 16, -140 + bob, -2, 4, 70, 80, 9, INK2, seed + 3, t)
    # gövde
    body = [(-92, -172 + bob), (-62, -236 + bob), (8, -258 + bob), (72, -236 + bob), (98, -184 + bob), (82, -126 + bob), (30, -98 + bob),
            (-42, -104 + bob), (-88, -134 + bob)]
    wash(ctx, X.pts(body), EMUW, 0.55 * alpha, t=t, seed=seed)
    hatch(ctx, X.pts(body), 52, 9 * s, 2.6 * s, INK2, seed, t, 0.55 * alpha)
    shape(ctx, X.pts(body), INK, X.len(5), seed, t, 2.2)
    # tüy püskülleri
    for i in range(9):
        a = 3.7 + i * 0.28
        bx, by = 8 + math.cos(a) * 88, -178 + bob + math.sin(a) * 72
        tx, ty = bx + math.cos(a) * 26 + (rng_hash(seed, i, bucket(t)) - 0.5) * 8, by + math.sin(a) * 26
        sline(ctx, X.pts([(bx, by), (tx, ty)]), X.len(3.5), INK, seed + i, t, amp=1.2, passes=1)
    # boyun
    nk_l = [(46, -226 + bob), (82, -296 + bob), (100, -352 + bob)]
    nk_r = [(86, -214 + bob), (120, -284 + bob), (132, -346 + bob)]
    wash(ctx, X.pts(nk_l + nk_r[::-1]), EMUW, 0.5 * alpha, t=t, seed=seed + 2)
    sline(ctx, X.pts(nk_l), X.len(5), INK, seed + 4, t, smooth=True)
    sline(ctx, X.pts(nk_r), X.len(5), INK, seed + 5, t, smooth=True)
    for k in range(5):
        u = 0.12 + k * 0.19
        a = (nk_l[0][0] + (nk_l[2][0] - nk_l[0][0]) * u, nk_l[0][1] + (nk_l[2][1] - nk_l[0][1]) * u + bob * 0)
        sline(ctx, X.pts([a, (a[0] + 26, a[1] + 8)]), X.len(2.4), GREY, seed + k, t, amp=1, passes=1)
    # baş
    head = _circle_pts(120, -364 + bob, 28, 19, 12)
    wash(ctx, X.pts(head), EMUW, 0.6 * alpha, t=t, seed=seed + 7)
    shape(ctx, X.pts(head), INK, X.len(5), seed + 8, t, 1.6)
    sline(ctx, X.pts([(144, -368 + bob), (184, -358 + bob), (146, -350 + bob)]), X.len(5), INK, seed + 9, t, smooth=True)
    ctx.circ(*X.p(126, -370 + bob), X.len(8 * eye), PAPER)
    ctx.circ(*X.p(128, -370 + bob), X.len(3.6 * eye), INK)
    brow = {-1: (-8, 4), 0: (-3, -3), 1: (2, -6)}[mood]
    sline(ctx, X.pts([(114, -382 + bob + brow[0]), (136, -382 + bob + brow[1])]), X.len(4.5), INK, seed + 10, t, amp=0.8, passes=1)
    if mood == 1:  # sırıtış
        sline(ctx, X.pts([(150, -356 + bob), (166, -352 + bob)]), X.len(3), INK, seed + 11, t, amp=0.6, passes=1)
    # şapka / madalya
    if hat == "helmet":
        hp = [(92, -372 + bob), (96, -398 + bob), (118, -412 + bob), (142, -398 + bob), (146, -372 + bob)]
        wash(ctx, X.pts(hp), KHAKI, 0.9 * alpha, t=t, seed=seed + 12)
        shape(ctx, X.pts(hp), INK, X.len(4.5), seed + 13, t, 1.4)
        sline(ctx, X.pts([(88, -372 + bob), (152, -372 + bob)]), X.len(5), INK, seed + 14, t, amp=0.8, passes=1)
    elif hat == "general":
        hp = [(92, -376 + bob), (100, -408 + bob), (140, -408 + bob), (150, -376 + bob)]
        wash(ctx, X.pts(hp), (60, 70, 100), 0.95 * alpha, t=t, seed=seed + 12)
        shape(ctx, X.pts(hp), INK, X.len(4.5), seed + 13, t, 1.2)
        sline(ctx, X.pts([(84, -376 + bob), (160, -380 + bob)]), X.len(6), INK, seed + 14, t, amp=0.8, passes=1)
        ctx.circ(*X.p(120, -395 + bob), X.len(7), HL)
    if medal:
        mx, my = 70, -214 + bob
        sline(ctx, X.pts([(mx - 14, my - 34), (mx, my), (mx + 14, my - 34)]), X.len(5), ACC, seed + 20, t, amp=0.6, passes=1)
        ctx.circ(*X.p(mx, my + 8), X.len(17), HL)
        shape(ctx, X.pts(_circle_pts(mx, my + 8, 17, 17, 10)), INK, X.len(3.5), seed + 21, t, 0.8)
        sline(ctx, X.pts([(mx - 7, my + 8), (mx, my + 1), (mx + 7, my + 8), (mx, my + 15), (mx - 7, my + 8)]), X.len(2.5), INK, seed + 22, t, amp=0.4, passes=1)
    # ön bacak (en üstte)
    if run:
        pass


# ═══════════════════════════ ASKER ═══════════════════════════
def soldier(ctx, x, y, s=1.0, t=0.0, phase=0.0, flip=1, pose="run", seed=5, rot=0.0, mood=0, alpha=1.0):
    X = Xf(x, y, s, flip=flip, rot=rot)
    sw = lambda o: math.sin(phase + o)
    lf = lambda o: max(0.0, math.cos(phase + o))
    run = pose in ("run", "slump")
    k = 0.6 if pose == "slump" else 1.0
    bob = -5 * abs(math.sin(phase * 0.5)) * k if run else 0
    hip = (0, -92 + bob)
    if run:
        _leg(ctx, X, 0, hip[1], 34 * sw(0.0) * k, 8 + 56 * lf(0.0) * k, 44, 50, 8, INK2, seed, t, foot=11)
        _leg(ctx, X, 0, hip[1], 34 * sw(math.pi) * k, 8 + 56 * lf(math.pi) * k, 44, 50, 8, INK, seed + 3, t, foot=11)
    else:
        _leg(ctx, X, -6, hip[1], -6, 4, 44, 50, 8, INK2, seed, t, foot=11)
        _leg(ctx, X, 6, hip[1], 8, 5, 44, 50, 8, INK, seed + 3, t, foot=11)
    lean = 12 if pose == "slump" else (-4 if pose == "aim" else 4)
    sh = (lean * 0.5, -154 + bob)
    torso = [(-16, hip[1]), (16, hip[1]), (sh[0] + 16, sh[1]), (sh[0] - 16, sh[1])]
    wash(ctx, X.pts(torso), KHAKI, 0.8 * alpha, t=t, seed=seed)
    shape(ctx, X.pts(torso), INK, X.len(4.5), seed, t, 1.6, smooth=False)
    # kafa
    hc = (sh[0] + (8 if pose == "slump" else 0), sh[1] - 30 + (6 if pose == "slump" else 0))
    head = _circle_pts(hc[0], hc[1], 21, 22, 11)
    wash(ctx, X.pts(head), SKIN, 0.9 * alpha, t=t, seed=seed + 4)
    shape(ctx, X.pts(head), INK, X.len(4.5), seed + 5, t, 1.2)
    ctx.circ(*X.p(hc[0] + 8, hc[1] - 2), X.len(2.8), INK)
    ctx.circ(*X.p(hc[0] - 6, hc[1] - 2), X.len(2.4), INK)
    if mood == 1 or pose == "slump":
        sline(ctx, X.pts([(hc[0] - 3, hc[1] + 12), (hc[0] + 6, hc[1] + (8 if pose == "slump" else 14)), (hc[0] + 12, hc[1] + 12)]), X.len(2.8), INK, seed + 6, t,
              amp=0.4, passes=1)
    else:
        sline(ctx, X.pts([(hc[0] - 3, hc[1] + 11), (hc[0] + 11, hc[1] + 11)]), X.len(2.8), INK, seed + 6, t, amp=0.4, passes=1)
    # şapka (Avustralya "slouch hat": geniş kenar, bir yanı kalkık)
    hy = hc[1] - 15
    crown = [(hc[0] - 17, hy), (hc[0] - 13, hy - 24), (hc[0] + 15, hy - 24), (hc[0] + 19, hy)]
    brim = [(hc[0] - 46, hy - 12), (hc[0] - 30, hy + 2), (hc[0] + 42, hy + 5), (hc[0] + 50, hy + 1), (hc[0] + 30, hy - 3), (hc[0] - 24, hy - 2)]
    wash(ctx, X.pts(brim), KHAKI, 0.95 * alpha, t=t, seed=seed + 7, smooth=False)
    shape(ctx, X.pts(brim), INK, X.len(4.5), seed + 8, t, 1.2, smooth=False)
    wash(ctx, X.pts(crown), KHAKI, 0.95 * alpha, t=t, seed=seed + 9, smooth=False)
    shape(ctx, X.pts(crown), INK, X.len(4.5), seed + 10, t, 1.2, smooth=False)
    sline(ctx, X.pts([(hc[0] - 15, hy - 10), (hc[0] + 17, hy - 10)]), X.len(4), INK, seed + 11, t, amp=0.6, passes=1)
    # kollar + tüfek
    if pose == "aim":
        hand = (sh[0] + 62, sh[1] + 6)
        sline(ctx, X.pts([sh, (sh[0] + 32, sh[1] + 20), hand]), X.len(8), INK, seed + 12, t, amp=1.2, passes=1)
        sline(ctx, X.pts([(sh[0] - 30, sh[1] + 16), (sh[0] + 150, sh[1] - 4)]), X.len(7), INK, seed + 13, t, amp=1.0, passes=2)
    elif pose == "salute":
        sline(ctx, X.pts([sh, (sh[0] + 30, sh[1] - 10), (hc[0] + 28, hy - 8)]), X.len(8), INK, seed + 12, t, amp=1.0, passes=1)
        sline(ctx, X.pts([(sh[0] - 6, sh[1]), (sh[0] - 22, sh[1] + 50)]), X.len(8), INK, seed + 14, t, amp=1.0, passes=1)
    else:
        sw2 = 24 * math.sin(phase) * k
        sline(ctx, X.pts([sh, (sh[0] + 10 + sw2, sh[1] + 38), (sh[0] + 22 + sw2, sh[1] + 66)]), X.len(8), INK, seed + 12, t, amp=1.0, passes=1)
        sline(ctx, X.pts([(sh[0] - 4, sh[1]), (sh[0] - 14 - sw2 * 0.6, sh[1] + 40)]), X.len(8), INK2, seed + 14, t, amp=1.0, passes=1)
        sline(ctx, X.pts([(sh[0] + 34, sh[1] - 20), (sh[0] + 6, sh[1] + 72)]), X.len(6), INK, seed + 13, t, amp=1.0, passes=1)  # omuzda tüfek


# ═══════════════════════════ LEWIS TÜFEĞİ ═══════════════════════════
def lewis(ctx, x, y, s=1.0, t=0.0, flash=0.0, recoil=0.0, flip=1, seed=9):
    X = Xf(x, y, s, flip=flip)
    ox = -8 * recoil
    for a, b in (((0, -62), (-44, 0)), ((0, -62), (46, 0)), ((0, -62), (4, 0))):
        sline(ctx, X.pts([a, b]), X.len(6), INK2, seed, t, amp=1.2, passes=1)
    jacket = [(-32 + ox, -84), (110 + ox, -80), (112 + ox, -62), (-30 + ox, -62)]
    wash(ctx, X.pts(jacket), (150, 150, 150), 0.7, t=t, seed=seed, smooth=False)
    shape(ctx, X.pts(jacket), INK, X.len(4.5), seed, t, 1.2, smooth=False)
    sline(ctx, X.pts([(112 + ox, -72), (170 + ox, -72)]), X.len(6), INK, seed + 1, t, amp=0.8, passes=1)
    sline(ctx, X.pts([(-32 + ox, -72), (-72 + ox, -66), (-82 + ox, -52)]), X.len(8), INK, seed + 2, t, amp=1.0, passes=1)
    drum = _circle_pts(22 + ox, -112, 28, 28, 12)
    wash(ctx, X.pts(drum), KHAKI, 0.8, t=t, seed=seed + 3)
    shape(ctx, X.pts(drum), INK, X.len(4.5), seed + 4, t, 1.2)
    for a in range(0, 360, 60):
        sline(ctx, X.pts([(22 + ox, -112), (22 + ox + math.cos(a * D2R) * 24, -112 + math.sin(a * D2R) * 24)]), X.len(2.2), INK2, seed + a, t, amp=0.5, passes=1)
    if flash > 0:
        tx, ty = 176 + ox, -72
        k = flash
        pts = []
        for i in range(12):
            a = i * math.pi / 6
            r = (62 if i % 2 == 0 else 24) * k * (0.9 + 0.2 * rng_hash(seed, i, bucket(t)))
            pts.append((tx + math.cos(a) * r * (1.5 if abs(math.cos(a)) > 0.7 else 1.0), ty + math.sin(a) * r))
        ctx.poly(X.pts(pts), HL)
        ctx.poly(X.pts([(tx + (p[0] - tx) * 0.5, ty + (p[1] - ty) * 0.5) for p in pts]), (255, 250, 230))
        shape(ctx, X.pts(pts), ACC, X.len(3.5), seed + 30, t, 1.5, smooth=False)


# ═══════════════════════════ KAMYON ═══════════════════════════
def truck(ctx, x, y, s=1.0, t=0.0, wheel=0.0, bounce=0.0, seed=11):
    X = Xf(x, y + bounce, s)
    bed = [(-170, -112), (36, -112), (36, -54), (-170, -54)]
    cab = [(36, -138), (112, -138), (128, -96), (150, -88), (150, -54), (36, -54)]
    wash(ctx, X.pts(bed), (170, 150, 100), 0.85, t=t, seed=seed, smooth=False)
    wash(ctx, X.pts(cab), KHAKI, 0.9, t=t, seed=seed + 1, smooth=False)
    shape(ctx, X.pts(bed), INK, X.len(5), seed, t, 1.6, smooth=False)
    shape(ctx, X.pts(cab), INK, X.len(5), seed + 1, t, 1.6, smooth=False)
    win = [(46, -128), (104, -128), (118, -98), (46, -98)]
    wash(ctx, X.pts(win), SKYW, 0.9, t=t, seed=seed + 2, smooth=False)
    shape(ctx, X.pts(win), INK, X.len(3.5), seed + 2, t, 1.0, smooth=False)
    for i in range(5):
        sline(ctx, X.pts([(-160 + i * 40, -108), (-160 + i * 40, -58)]), X.len(2.6), INK2, seed + i, t, amp=0.8, passes=1)
    for wx in (-112, 86):
        wy = -34
        circ = _circle_pts(wx, wy, 36, 36, 12)
        wash(ctx, X.pts(circ), INK2, 0.9, t=t, seed=seed + 5, smooth=True, off=(0, 0))
        shape(ctx, X.pts(circ), INK, X.len(5), seed + 6, t, 1.2)
        ctx.circ(*X.p(wx, wy), X.len(14), PAPER)
        for k in range(4):
            a = wheel + k * math.pi / 2
            sline(ctx, X.pts([(wx, wy), (wx + math.cos(a) * 30, wy + math.sin(a) * 30)]), X.len(3.2), PAPER, seed + k, t, amp=0.4, passes=1, soft=False)
        ctx.circ(*X.p(wx, wy), X.len(5), INK)
    return X


# ═══════════════════════════ BUĞDAY / ÇİFTÇİ ═══════════════════════════
def wheat(ctx, x0, x1, y, t, h=130, step=26, eaten=None, seed=3, sway=1.0):
    """eaten: x -> 0..1 (başak yenme oranı)"""
    k = 0
    xx = x0
    while xx <= x1:
        hh = h * (0.8 + 0.4 * rng_hash(seed, k))
        sw = math.sin(t * 2.2 + k * 0.7) * 5 * sway
        e = eaten(xx) if eaten else 0.0
        top = (xx + sw, y - hh * (1 - 0.7 * e))
        sline(ctx, [(xx, y), (xx + sw * 0.5, y - hh * 0.5 * (1 - 0.7 * e)), top], 3.4, INK2, seed + k, t, amp=0.8, passes=1, soft=False)
        if e < 0.95:
            for j in range(4):
                gy = top[1] - 6 + j * 15
                for sgn in (-1, 1):
                    gx = top[0] + sgn * 9
                    ctx.poly([(top[0], gy + 8), (gx, gy - 6), (gx + sgn * 4, gy + 2)], WHEAT, 0.95)
                    sline(ctx, [(top[0], gy + 8), (gx, gy - 6)], 2.4, INK2, seed + k + j, t, amp=0.5, passes=1, soft=False)
        xx += step
        k += 1


def farmer(ctx, x, y, s=1.0, t=0.0, anger=1.0, seed=21, flip=1):
    X = Xf(x, y, s, flip=flip)
    sh = math.sin(t * 22) * 3 * anger
    for dx, a in ((-8, -4), (10, 6)):
        sline(ctx, X.pts([(dx, -96), (dx + a, -50), (dx + a * 1.3, 0)]), X.len(9), INK2, seed + dx, t, amp=1.2, passes=1)
    torso = [(-18, -96), (18, -96), (16, -166), (-16, -166)]
    wash(ctx, X.pts(torso), (96, 120, 170), 0.8, t=t, seed=seed, smooth=False)
    shape(ctx, X.pts(torso), INK, X.len(4.5), seed, t, 1.4, smooth=False)
    sline(ctx, X.pts([(-10, -166), (-8, -128)]), X.len(3), INK, seed + 1, t, amp=0.5, passes=1)
    sline(ctx, X.pts([(10, -166), (8, -128)]), X.len(3), INK, seed + 2, t, amp=0.5, passes=1)
    # kollar havada yumruk
    sline(ctx, X.pts([(-14, -158), (-40 + sh, -190), (-34 + sh, -226)]), X.len(8), INK, seed + 3, t, amp=1.0, passes=1)
    sline(ctx, X.pts([(14, -158), (42 - sh, -192), (36 - sh, -230)]), X.len(8), INK, seed + 4, t, amp=1.0, passes=1)
    ctx.circ(*X.p(-34 + sh, -232), X.len(11), SKIN)
    ctx.circ(*X.p(36 - sh, -236), X.len(11), SKIN)
    hc = (0, -196)
    head = _circle_pts(hc[0], hc[1], 22, 24, 11)
    wash(ctx, X.pts(head), SKIN, 0.95, t=t, seed=seed + 5)
    shape(ctx, X.pts(head), INK, X.len(4.5), seed + 6, t, 1.2)
    sline(ctx, X.pts([(-12, hc[1] - 6), (-2, hc[1] - 2)]), X.len(3.5), INK, seed + 7, t, amp=0.4, passes=1)
    sline(ctx, X.pts([(12, hc[1] - 6), (2, hc[1] - 2)]), X.len(3.5), INK, seed + 8, t, amp=0.4, passes=1)
    ctx.circ(*X.p(-7, hc[1] + 2), X.len(2.6), INK)
    ctx.circ(*X.p(7, hc[1] + 2), X.len(2.6), INK)
    sline(ctx, X.pts([(-8, hc[1] + 16), (0, hc[1] + 10), (8, hc[1] + 16)]), X.len(3), INK, seed + 9, t, amp=0.4, passes=1)
    # hasır şapka
    brim = [(-46, hc[1] - 18), (0, hc[1] - 26), (46, hc[1] - 18), (0, hc[1] - 8)]
    wash(ctx, X.pts(brim), WHEAT, 0.95, t=t, seed=seed + 10)
    shape(ctx, X.pts(brim), INK, X.len(4), seed + 11, t, 1.2)
    crown = [(-16, hc[1] - 22), (-12, hc[1] - 44), (12, hc[1] - 44), (16, hc[1] - 22)]
    wash(ctx, X.pts(crown), WHEAT, 0.95, t=t, seed=seed + 12, smooth=False)
    shape(ctx, X.pts(crown), INK, X.len(4), seed + 13, t, 1.0, smooth=False)
    # ter damlaları + öfke çizgileri
    for i in range(3):
        ph = (t * 1.6 + i / 3) % 1.0
        ctx.poly(X.pts([(36 + i * 6, hc[1] - 30 + ph * 30), (31 + i * 6, hc[1] - 18 + ph * 30), (41 + i * 6, hc[1] - 18 + ph * 30)]), (120, 170, 220), 1 - ph)
    for a in (-60, -90, -120):
        sline(ctx, X.pts([(math.cos(a * D2R) * 60, hc[1] - 50 + math.sin(a * D2R) * 40 - 6), (math.cos(a * D2R) * 82, hc[1] - 50 + math.sin(a * D2R) * 56 - 10)]),
              X.len(4), ACC, seed + a, t, amp=1.5, passes=1)


# ═══════════════════════════ DOSYA / HARİTA / İŞARETLER ═══════════════════════════
def folder(ctx, cx, cy, s=1.0, t=0.0, seed=31, wob=0.0):
    X = Xf(cx, cy, s, rot=wob)
    body = [(-230, -160), (230, -160), (230, 170), (-230, 170)]
    tab = [(-230, -160), (-230, -196), (-90, -196), (-60, -160)]
    wash(ctx, X.pts(body), (222, 190, 120), 0.95, t=t, seed=seed, smooth=False)
    wash(ctx, X.pts(tab), (222, 190, 120), 0.95, t=t, seed=seed + 1, smooth=False)
    shape(ctx, X.pts(body), INK, X.len(6), seed, t, 2.0, smooth=False)
    shape(ctx, X.pts(tab), INK, X.len(6), seed + 1, t, 2.0, smooth=False)
    lab = [(-150, -110), (150, -110), (150, -20), (-150, -20)]
    ctx.poly(X.pts(lab), PAPER)
    shape(ctx, X.pts(lab), INK, X.len(4), seed + 2, t, 1.4, smooth=False)
    ctx.text(*X.p(0, -66), "RAPOR", 70 * s, INK, path=FONT_LORA)
    ctx.text(*X.p(0, 92), "?", 190 * s, ACC, path=FONT_LORA, stroke=6 * s, stroke_fill=INK)
    sline(ctx, X.pts([(170, -196), (170, -130), (194, -130), (194, -190)]), X.len(5), GREY, seed + 3, t, amp=0.8, passes=1)  # ataş


def _ll(lon, lat):
    return ((lon - 113.0) * 14.6, (-lat - 10.0) * 18.2)


_AUS_LL = [(126.9, -13.7), (129.0, -14.9), (130.8, -12.4), (132.6, -11.5), (136.8, -11.0), (136.9, -12.3), (135.5, -14.8), (135.9, -15.8),
           (139.5, -17.5), (140.8, -17.4), (141.5, -13.0), (142.5, -10.7), (143.4, -14.0), (145.3, -15.5), (145.8, -16.9), (146.8, -19.3),
           (149.2, -21.1), (150.5, -23.4), (153.1, -27.5), (153.6, -28.7), (151.2, -33.9), (150.0, -37.1), (146.4, -39.1), (144.9, -38.3),
           (143.5, -38.9), (140.5, -38.0), (138.5, -35.5), (137.8, -33.0), (135.8, -34.7), (133.7, -32.1), (128.9, -31.7), (121.9, -33.9),
           (117.9, -35.0), (115.1, -34.4), (115.7, -32.0), (114.6, -28.8), (113.4, -25.5), (114.1, -21.8), (118.6, -20.3), (122.2, -18.0),
           (122.9, -16.4), (125.0, -14.5)]
AUS = [_ll(*p) for p in _AUS_LL]
_WA_LL = [(126.9, -13.7), (129.0, -14.9), (129.0, -31.7), (121.9, -33.9), (117.9, -35.0), (115.1, -34.4), (115.7, -32.0), (114.6, -28.8),
          (113.4, -25.5), (114.1, -21.8), (118.6, -20.3), (122.2, -18.0), (122.9, -16.4), (125.0, -14.5)]
WA = [_ll(*p) for p in _WA_LL]
WHEATBELT = _ll(117.5, -31.0)


def australia(ctx, cx, cy, s=1.0, t=0.0, reveal=1.0, seed=41, wa=0.0):
    X = Xf(cx - 300 * s, cy - 260 * s, s)
    if reveal >= 1:
        wash(ctx, X.pts(AUS), (232, 204, 130), 0.9, t=t, seed=seed)
        if wa > 0:
            wash(ctx, X.pts(WA), ACC, 0.35 * wa, t=t, seed=seed + 5, off=(0, 0))
        hatch(ctx, X.pts(AUS), 55, 18 * s, 2 * s, GREY, seed, t, 0.35)
    shape(ctx, X.pts(AUS), INK, X.len(6), seed, t, 2.2, reveal=reveal, smooth=True)
    return X


def pin(ctx, x, y, s=1.0, t=0.0, seed=51):
    sline(ctx, [(x, y), (x, y - 56 * s)], 6 * s, INK, seed, t, amp=0.8, passes=1)
    ctx.circ(x, y - 66 * s, 24 * s, ACC)
    shape(ctx, _circle_pts(x, y - 66 * s, 24 * s, 24 * s, 10), INK, 4 * s, seed + 1, t, 1.0)
    ctx.circ(x - 7 * s, y - 74 * s, 6 * s, (255, 200, 190))


def bullet(ctx, x, y, s=1.0, ang=0.0, seed=61, t=0.0, col=(196, 150, 60)):
    X = Xf(x, y, s, rot=ang)
    body = [(-22, -7), (10, -7), (24, 0), (10, 7), (-22, 7)]
    ctx.poly(X.pts(body), col)
    ctx.poly(X.pts([(10, -7), (24, 0), (10, 7)]), (150, 100, 50))
    shape(ctx, X.pts(body), INK, X.len(2.4), seed, t, 0.5, smooth=False, passes=1)


def cloud_doodle(ctx, x, y, s, t, col=GREY, seed=71, alpha=0.9):
    pts = []
    for i, (dx, dy, r) in enumerate(((-60, 6, 36), (-20, -16, 46), (32, -10, 40), (72, 8, 30), (6, 16, 40))):
        pass
    outline = [(-96, 24), (-92, -4), (-60, -30), (-20, -48), (24, -40), (60, -26), (96, -2), (100, 24)]
    wash(ctx, [(x + px * s, y + py * s) for px, py in outline], col, alpha * 0.6, t=t, seed=seed)
    shape(ctx, [(x + px * s, y + py * s) for px, py in outline], INK, 4 * s, seed, t, 1.6)


def thought_bubble(ctx, cx, cy, rx, ry, tail_to, t, seed=81):
    pts = _circle_pts(cx, cy, rx, ry, 22)
    # dalgalı bulut kenarı
    cl = []
    for i in range(22):
        a = i * 2 * math.pi / 22
        r = 1.0 + 0.07 * (1 if i % 2 else -1)
        cl.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r))
    ctx.poly(cl, PAPER)
    shape(ctx, cl, INK, 5, seed, t, 1.6, smooth=True)
    tx, ty = tail_to
    for k, (u, r) in enumerate(((0.80, 22), (0.58, 15), (0.38, 10))):
        px, py = cx + (tx - cx) * u, cy + (ty - cy) * u
        ctx.circ(px, py, r, PAPER)
        shape(ctx, _circle_pts(px, py, r, r, 9), INK, 4, seed + k, t, 0.8)


# ═══════════════════════════ SKOR TABELASI ═══════════════════════════
def scoreboard(ctx, cx, cy, s, t, emu_score=1, rot=0.0, seed=91, pulse=0.0):
    X = Xf(cx, cy, s, rot=rot)
    frame = [(-410, -250), (410, -250), (410, 250), (-410, 250)]
    ctx.poly(X.pts([(-398, -238), (422, -238), (422, 262), (-398, 262)]), (0, 0, 0), 0.20)
    wash(ctx, X.pts(frame), (120, 86, 56), 0.95, t=t, seed=seed, smooth=False, off=(0, 0))
    shape(ctx, X.pts(frame), INK, X.len(8), seed, t, 2.2, smooth=False)
    inner = [(-380, -220), (380, -220), (380, 220), (-380, 220)]
    ctx.poly(X.pts(inner), (232, 224, 204))
    shape(ctx, X.pts(inner), INK, X.len(4), seed + 1, t, 1.6, smooth=False)
    sline(ctx, X.pts([(0, -220), (0, 220)]), X.len(5), INK, seed + 2, t, amp=1.4, passes=1)
    ctx.text(*X.p(-190, -156), "ORDU", 86 * s, INK, path=FONT_POP)
    ctx.text(*X.p(190, -156), "EMU", 86 * s, ACC, path=FONT_POP)
    ctx.text(*X.p(-190, 50), "0", 330 * s, INK, path=FONT_POP)
    k = 1.0 + 0.10 * pulse
    ctx.text(*X.p(190, 50), str(emu_score), 330 * s * k, ACC, path=FONT_POP)
    # asma ipleri
    for sx in (-300, 300):
        sline(ctx, X.pts([(sx, -250), (sx * 0.55, -520)]), X.len(5), INK2, seed + 8 + sx, t, amp=1.0, passes=1)
