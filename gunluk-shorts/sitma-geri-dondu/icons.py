"""Mavi baskı simgeleri: sivrisinek, kinin şişesi, bataklık, tarla, insan, büyüteç, ok, ilaçlama pompası."""
import math

from bp import *  # noqa
from engine import *  # noqa


def arrow(ctx, x0, y0, x1, y1, col=LINE, reveal=1.0, w=5.0, head=26.0, glow=True):
    L(ctx, [(x0, y0), (x1, y1)], w, col, 1.0, reveal, glow=glow)
    if reveal >= 0.98:
        a = math.atan2(y1 - y0, x1 - x0)
        for da in (2.6, -2.6):
            L(ctx, [(x1, y1), (x1 + math.cos(a + da) * head, y1 + math.sin(a + da) * head)], w, col, 1.0, 1.0, glow=False)


def mosquito(ctx, cx, cy, s=1.0, reveal=1.0, rot=22.0, flap=0.0, col=LINE, w=3.6):
    """Yandan Anopheles: baş sağda, uzun hortum, karın yukarı eğik; yerel birim ≈ px (s=1'de ~330 px genişlik)"""
    X = Xf(cx, cy, s, rot=rot)
    ww = w * s

    def E(x, y, rx, ry, n=20, a=0.0):
        pts = circ_pts(0, 0, rx, ry, n)
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        return X.pts([(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts])

    fa = math.sin(flap * 38.0) * 9.0
    polys = [
        (E(22, -2, 36, 24), ww),                                   # göğüs
        (E(-84, -8, 82, 12, 24), ww),                              # karın
        (E(60, 4, 11, 11, 14), ww),                                # baş
        (X.pts([(69, 8), (160, 30)]), ww),                         # hortum
        (X.pts([(68, 3), (150, 18)]), ww * 0.7),                   # palp
        (X.pts([(62, -6), (92, -30)]), ww * 0.7),                  # anten
        (E(-14, -46, 84, 11, 22, -16 + fa), ww),                   # kanat
        (X.pts([(42, 18), (82, 58), (104, 116)]), ww * 0.8),       # ön bacak
        (X.pts([(22, 22), (8, 74), (24, 134)]), ww * 0.8),         # orta bacak
        (X.pts([(2, 20), (-56, 58), (-84, 118)]), ww * 0.8),       # arka bacak
    ]
    draw_seq(ctx, polys, reveal, ww, col)


def bottle(ctx, cx, cy, s=1.0, reveal=1.0, col=LINE, w=4.0):
    X = Xf(cx, cy, s)
    polys = [
        (X.pts([(-44, -30), (-44, 110), (44, 110), (44, -30), (-44, -30)]), w * s),
        (X.pts([(-20, -30), (-20, -62), (20, -62), (20, -30)]), w * s),
        (X.pts([(-26, -62), (-26, -92), (26, -92), (26, -62), (-26, -62)]), w * s),
        (X.pts([(-44, 8), (44, 8)]), 2.5 * s),
        (X.pts([(-44, 74), (44, 74)]), 2.5 * s),
        (X.pts([(-24, 30), (24, 30)]), 2.5 * s), (X.pts([(-24, 44), (14, 44)]), 2.5 * s), (X.pts([(-24, 58), (20, 58)]), 2.5 * s),
    ]
    draw_seq(ctx, polys, reveal, w * s, col)


def marsh(ctx, cx, cy, s=1.0, t=0.0, level=1.0, reveal=1.0, col=LINE):
    """Sazlıklı bataklık; level 1 → su dolu, 0 → kurumuş"""
    X = Xf(cx, cy, s)
    L(ctx, X.pts([(-210, 60), (210, 60)]), 4 * s, col, 1.0, reveal)
    for i, dx in enumerate((-160, -100, -40, 30, 100, 160)):
        h = 70 + 26 * ((i * 37) % 3)
        L(ctx, X.pts([(dx, 60), (dx + 4, 60 - h)]), 3.4 * s, GREEN, 0.9, reveal, glow=False)
        L(ctx, X.pts([(dx + 3, 60 - h * 0.7), (dx + 26, 60 - h * 0.95)]), 2.6 * s, GREEN, 0.9, reveal, glow=False)
        L(ctx, X.pts([(dx + 2, 60 - h * 0.5), (dx - 22, 60 - h * 0.78)]), 2.6 * s, GREEN, 0.9, reveal, glow=False)
    if level > 0.02:
        for r in range(3):
            pts = []
            for k in range(0, 18):
                x = -200 + k * 400 / 17
                pts.append((x, 38 + r * 9 - (1 - level) * 6 + math.sin(x / 40 + t * 1.8 + r) * 4 * level))
            L(ctx, X.pts(pts), 3 * s, LINE_DIM, 0.85 * level * reveal, 1.0, glow=False)


def field(ctx, cx, cy, w, h, t=0.0, reveal=1.0, col=LINE):
    """Sulu tarla: üstten görünüm, ekin sıraları + sulama kanalları (akan kesik çizgiler)"""
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    L(ctx, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 4.5, col, 1.0, reveal, closed=True)
    r = clamp(reveal * 1.4 - 0.2)
    xs = x0 + 28
    while xs < x1 - 20:
        L(ctx, [(xs, y0 + 14), (xs, y1 - 14)], 2.2, GREEN, 0.55 * r, 1.0, glow=False)
        xs += 34
    for fy in (y0 + h * 0.33, y0 + h * 0.67):
        L(ctx, [(x0 - 28, fy - 8), (x1 + 28, fy - 8)], 3.4, LINE, 1.0, r)
        L(ctx, [(x0 - 28, fy + 8), (x1 + 28, fy + 8)], 3.4, LINE, 1.0, r)
        x = x0 - 28 + ((t * 70) % 40)
        while x < x1 + 20:
            L(ctx, [(x, fy), (x + 18, fy)], 4, (120, 200, 255), 0.9 * r, 1.0, glow=False)
            x += 40


def person(ctx, x, y, s=1.0, reveal=1.0, col=LINE, walk=0.0, w=4.0):
    """Çöpten adam; y = ayak hizası; sırtta bohça"""
    sw = math.sin(walk) * 14 * s
    ww = w * s
    polys = [
        (circ_pts(x, y - 150 * s, 16 * s, n=14), ww),
        ([(x, y - 134 * s), (x, y - 70 * s)], ww),
        ([(x, y - 122 * s), (x - 26 * s, y - 94 * s + sw * 0.3), (x - 20 * s, y - 72 * s)], ww),
        ([(x, y - 122 * s), (x + 28 * s, y - 98 * s - sw * 0.3), (x + 36 * s, y - 76 * s)], ww),
        ([(x, y - 70 * s), (x - 18 * s + sw, y - 34 * s), (x - 20 * s + sw, y)], ww),
        ([(x, y - 70 * s), (x + 18 * s - sw, y - 34 * s), (x + 22 * s - sw, y)], ww),
        ([(x - 14 * s, y - 130 * s), (x - 44 * s, y - 134 * s), (x - 46 * s, y - 98 * s), (x - 16 * s, y - 94 * s), (x - 14 * s, y - 130 * s)], ww),
    ]
    draw_seq(ctx, polys, reveal, ww, col)


def magnifier(ctx, cx, cy, s=1.0, reveal=1.0, col=AMBER, w=7.0):
    L(ctx, circ_pts(cx, cy, 58 * s, n=28), w * s, col, 1.0, reveal)
    L(ctx, [(cx + 41 * s, cy + 41 * s), (cx + 104 * s, cy + 104 * s)], w * 1.6 * s, col, 1.0, clamp(reveal * 2 - 0.6))


def sprayer(ctx, cx, cy, s=1.0, reveal=1.0, t=0.0, col=LINE, w=4.0):
    X = Xf(cx, cy, s)
    ww = w * s
    polys = [
        (X.pts([(-40, -110), (40, -110), (40, 0), (-40, 0), (-40, -110)]), ww),
        (X.pts([(-40, -80), (40, -80)]), 2.5 * s),
        (X.pts([(0, -110), (0, -140), (30, -150)]), ww),
        (X.pts([(40, -40), (90, -40), (120, -90), (170, -80)]), ww),
        (X.pts([(170, -80), (190, -100), (190, -60), (170, -80)]), ww),
    ]
    draw_seq(ctx, polys, reveal, ww, col)
    if reveal > 0.95:
        for i in range(9):
            u = ((t * 1.6 + i / 9.0) % 1.0)
            ang = -0.45 + 0.9 * ((i * 5) % 9) / 8.0
            x, y = X.p(190 + u * 140, -80 + math.sin(ang) * u * 110 + u * u * 40)
            ctx.circ(x, y, 5 * s * (1 - 0.5 * u), (150, 215, 255), 0.9 * (1 - u))
