"""Armalar ve nişanlar (kodla çizilmiş, özgün): Habsburg çift başlı kartal, Avusturya, Kastilya (kale), Aragon (kızıl çubuklar),
Burgonya (çapraz şeritler), Fransa (zambak), Osmanlı (hilâl), Papalık (anahtarlar), Luther gülü, Tudor gülü, Plus Ultra sütunları,
Altın Post koçu. Gerçek arma çizimleri kopyalanmadı; sadeleştirilmiş şematik biçimlerdir."""
import math

from inkpaint import *  # noqa

SILVER = Hx("#D9D9D2")
STEEL = Hx("#9AA3A8")


def shield_pts(w=150.0, h=182.0, cx=0.0, cy=0.0, s=1.0):
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h * 0.05), (w * 0.40, h * 0.30), (0, h / 2), (-w * 0.40, h * 0.30), (-w / 2, h * 0.05)]
    return [(cx + x * s, cy + y * s) for x, y in pts]


def _castle(ctx, x, y, s, col, ink=INK):
    pts = [(-30, 26), (-30, -4), (-30, -14), (-22, -14), (-22, -8), (-14, -8), (-14, -22), (-6, -22), (-6, -30), (6, -30), (6, -22), (14, -22), (14, -8), (22, -8), (22, -14), (30, -14),
           (30, 26)]
    P = [(x + a * s, y + b * s) for a, b in pts]
    ctx.poly(P, col)
    ctx.line(P + [P[0]], 2.4 * s, ink, 1.0)
    ctx.rect(x - 6 * s, y + 6 * s, x + 6 * s, y + 26 * s, ink)
    for dx in (-22, 22):
        ctx.rect(x + (dx - 3) * s, y - 3 * s, x + (dx + 3) * s, y + 5 * s, ink)
    ctx.rect(x - 3 * s, y - 16 * s, x + 3 * s, y - 8 * s, ink)


def fleur(ctx, x, y, s, col, ink=INK):
    mid = [(0, -34), (8, -22), (8, -4), (3, 8), (-3, 8), (-8, -4), (-8, -22)]
    L = [(-4, 2), (-30, -14), (-34, 4), (-22, 14), (-10, 8)]
    R = [(-a, b) for a, b in L]
    for pts in (mid, L, R):
        P = [(x + a * s, y + b * s) for a, b in pts]
        ctx.poly(smooth_closed(P, 4), col)
        ctx.line(smooth_closed(P, 4) + [smooth_closed(P, 4)[0]], 1.8 * s, ink, 1.0)
    ctx.rect(x - 14 * s, y + 8 * s, x + 14 * s, y + 15 * s, col)
    ctx.line([(x - 14 * s, y + 8 * s), (x + 14 * s, y + 8 * s), (x + 14 * s, y + 15 * s), (x - 14 * s, y + 15 * s), (x - 14 * s, y + 8 * s)], 1.8 * s, ink, 1.0)
    P = [(x + a * s, y + b * s) for a, b in [(-9, 15), (9, 15), (6, 30), (-6, 30)]]
    ctx.poly(P, col)
    ctx.line(P + [P[0]], 1.8 * s, ink, 1.0)


def eagle(ctx, x, y, s, col=INK, hl=GOLD_L, ink=INK_L):
    half = [(0, -52), (8, -60), (14, -80), (24, -94), (38, -88), (54, -76), (40, -72), (31, -66), (30, -52), (62, -66), (94, -84), (102, -60), (93, -48), (101, -30), (88, -24),
            (92, -6), (78, -4), (80, 14), (64, 12), (58, 34), (44, 36), (44, 58), (54, 92), (36, 84), (28, 98), (16, 70), (8, 70), (0, 92)]
    P = half + [(-a, b) for a, b in reversed(half)]
    P = [(x + a * s, y + b * s) for a, b in P]
    ctx.poly(P, col)
    ctx.line(P + [P[0]], 2.2 * s, ink, 1.0)
    for sx in (-1, 1):                         # kafa halesi + gaga rengi
        ctx.ring(x + sx * 30 * s, y - 86 * s, 11 * s, 2.4 * s, hl)
        ctx.poly([(x + sx * 52 * s, y - 76 * s), (x + sx * 40 * s, y - 72 * s), (x + sx * 48 * s, y - 68 * s)], hl)
    ctx.circ(x, y - 8 * s, 10 * s, hl)         # göğüs


def eagle_hl(ctx, x, y, s):
    eagle(ctx, x, y, s)


def _clip_shield(ctx, x, y, s, fill, ow, seed):
    P = shield_pts(150, 182, x, y, s)
    base = shape(ctx, P, fill, ow=ow * s, seed=seed, wob_amp=1.0, smooth=False)
    return Clip(ctx, base), P


def arms(ctx, kind, x, y, s=1.0, t=0.0, alpha=1.0, ow=5.5, seed=3):
    """Kalkan + yük. (x,y) kalkan merkezi, s ölçek (s=1: 150×182 px)."""
    if kind == "plus_ultra":
        return plus_ultra(ctx, x, y, s)
    if kind == "post":
        return fleece(ctx, x, y, s)
    if kind == "luther":
        return luther_rose(ctx, x, y, s)
    if kind == "tudor":
        return tudor_rose(ctx, x, y, s)
    fills = {"habsburg": GOLD_L, "austria": CRIMSON, "kastilya": CRIMSON, "aragon": GOLD_L, "burgonya": ROYAL, "fransa": ROYAL, "osmanli": FOREST, "papalik": CRIMSON,
             "ispanya": CRIMSON, "hollanda": GOLD_L, "bohemya": PARCH_L, "macar": CRIMSON}
    fill = fills.get(kind, PARCH_L)
    c, P = _clip_shield(ctx, x, y, s, fill, ow, seed)
    # shape() zaten dolguyu çizdi; yükler için Clip kullan
    if kind == "austria":
        if c.ok:
            c.poly([(x - 80 * s, y - 20 * s), (x + 80 * s, y - 20 * s), (x + 80 * s, y + 28 * s), (x - 80 * s, y + 28 * s)], PARCH_L)
            c.done()
    elif kind == "aragon":
        if c.ok:
            for i in range(4):
                xx = x + (-56 + i * 37.5) * s
                c.poly([(xx - 9 * s, y - 100 * s), (xx + 9 * s, y - 100 * s), (xx + 9 * s, y + 100 * s), (xx - 9 * s, y + 100 * s)], CRIMSON)
            c.done()
    elif kind == "burgonya":
        if c.ok:
            for i in range(-4, 5):
                off = i * 36 * s
                c.poly([(x - 100 * s + off, y - 110 * s), (x - 70 * s + off, y - 110 * s), (x + 110 * s + off, y + 110 * s), (x + 80 * s + off, y + 110 * s)], GOLD_L)
            c.done()
        ctx.line(P + [P[0]], 9 * s, CRIMSON, 1.0)
    elif kind == "kastilya":
        if c.ok:
            c.done()
        _castle(ctx, x, y + 6 * s, 1.55 * s, GOLD_L)
    elif kind == "fransa":
        if c.ok:
            c.done()
        for dx, dy in ((0, -38), (-36, 16), (36, 16)):
            fleur(ctx, x + dx * s, y + dy * s, 1.0 * s, GOLD_L)
    elif kind == "habsburg":
        if c.ok:
            c.done()
        eagle(ctx, x, y + 6 * s, 0.82 * s)
    elif kind == "osmanli":
        if c.ok:
            c.done()
        ctx.circ(x - 6 * s, y - 4 * s, 44 * s, PARCH_L)
        ctx.circ(x + 6 * s, y - 4 * s, 38 * s, FOREST)
        _star(ctx, x + 38 * s, y - 4 * s, 15 * s, PARCH_L)
    elif kind == "papalik":
        if c.ok:
            c.done()
        for sx, col in ((-1, GOLD_L), (1, SILVER)):
            ctx.line([(x + sx * 34 * s, y - 62 * s), (x - sx * 22 * s, y + 66 * s)], 12 * s, INK, 1.0)
            ctx.line([(x + sx * 34 * s, y - 62 * s), (x - sx * 22 * s, y + 66 * s)], 7 * s, col, 1.0)
            ctx.ring(x + sx * 34 * s, y - 66 * s, 14 * s, 6 * s, col)
    elif kind == "ispanya":
        if c.ok:
            c.done()
        _castle(ctx, x - 0 * s, y - 30 * s, 1.2 * s, GOLD_L)
        for i in range(4):
            xx = x + (-45 + i * 30) * s
            ctx.rect(xx - 7 * s, y + 24 * s, xx + 7 * s, y + 74 * s, GOLD_L)
            ctx.rect(xx - 4 * s, y + 24 * s, xx + 1 * s, y + 74 * s, CRIMSON_D, 0.0)
    elif kind == "hollanda":
        if c.ok:
            c.done()
        ctx.poly([(x - 30 * s, y + 40 * s), (x - 40 * s, y - 20 * s), (x - 10 * s, y - 50 * s), (x + 24 * s, y - 40 * s), (x + 40 * s, y), (x + 20 * s, y + 40 * s)], INK)
    else:
        if c.ok:
            c.done()
    return None


def _star(ctx, x, y, r, col):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    ctx.poly(pts, col)


def luther_rose(ctx, x, y, s):
    ctx.circ(x, y, 74 * s, ROYAL)
    ctx.ring(x, y, 74 * s, 7 * s, INK)
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        ctx.circ(x + math.cos(a) * 34 * s, y + math.sin(a) * 34 * s, 22 * s, PARCH_L)
        ctx.ring(x + math.cos(a) * 34 * s, y + math.sin(a) * 34 * s, 22 * s, 2.2 * s, INK)
    ctx.circ(x, y, 26 * s, CRIMSON_L)
    ctx.ring(x, y, 26 * s, 2.4 * s, INK)
    ctx.rect(x - 3.5 * s, y - 18 * s, x + 3.5 * s, y + 18 * s, INK)
    ctx.rect(x - 14 * s, y - 8 * s, x + 14 * s, y - 1 * s, INK)


def tudor_rose(ctx, x, y, s):
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        ctx.circ(x + math.cos(a) * 38 * s, y + math.sin(a) * 38 * s, 26 * s, CRIMSON_L)
        ctx.ring(x + math.cos(a) * 38 * s, y + math.sin(a) * 38 * s, 26 * s, 2.2 * s, INK)
    for i in range(5):
        a = -math.pi / 2 + math.pi / 5 + i * 2 * math.pi / 5
        ctx.circ(x + math.cos(a) * 22 * s, y + math.sin(a) * 22 * s, 17 * s, PARCH_L)
        ctx.ring(x + math.cos(a) * 22 * s, y + math.sin(a) * 22 * s, 17 * s, 2.0 * s, INK)
    ctx.circ(x, y, 11 * s, GOLD_L)
    ctx.ring(x, y, 11 * s, 2 * s, INK)


def plus_ultra(ctx, x, y, s):
    """Herkül Sütunları + 'PLUS ULTRA' kuşağı (Karl'ın devizi)."""
    for sx in (-1, 1):
        xx = x + sx * 62 * s
        ctx.rect(xx - 17 * s, y - 70 * s, xx + 17 * s, y + 80 * s, PARCH_L)
        ctx.rect(xx - 17 * s, y - 70 * s, xx - 6 * s, y + 80 * s, PARCH_D)
        ctx.line([(xx - 17 * s, y - 70 * s), (xx - 17 * s, y + 80 * s), (xx + 17 * s, y + 80 * s), (xx + 17 * s, y - 70 * s), (xx - 17 * s, y - 70 * s)], 3.0 * s, INK, 1.0)
        ctx.rect(xx - 24 * s, y - 84 * s, xx + 24 * s, y - 68 * s, GOLD_L)
        ctx.line([(xx - 24 * s, y - 84 * s), (xx + 24 * s, y - 84 * s), (xx + 24 * s, y - 68 * s), (xx - 24 * s, y - 68 * s), (xx - 24 * s, y - 84 * s)], 2.6 * s, INK, 1.0)
        crown_pts = [(xx - 20 * s, y - 84 * s), (xx - 24 * s, y - 108 * s), (xx - 8 * s, y - 96 * s), (xx, y - 112 * s), (xx + 8 * s, y - 96 * s), (xx + 24 * s, y - 108 * s), (xx + 20 * s, y - 84 * s)]
        ctx.poly(crown_pts, GOLD)
        ctx.line(crown_pts + [crown_pts[0]], 2.4 * s, INK, 1.0)
    # kuşak
    band = [(x - 120 * s, y + 8 * s), (x - 40 * s, y - 14 * s), (x + 40 * s, y - 14 * s), (x + 120 * s, y + 8 * s), (x + 40 * s, y + 30 * s), (x - 40 * s, y + 30 * s)]
    ctx.poly(smooth_closed(band, 5), CRIMSON_L)
    ctx.line(smooth_closed(band, 5) + [smooth_closed(band, 5)[0]], 3.0 * s, INK, 1.0)
    ctx.text(x, y + 8 * s, "PLUS ULTRA", 22 * s, PARCH_L, path=FONT_TITLE, stroke=0)


def fleece(ctx, x, y, s):
    """Altın Post (Toison d'Or) koçu: sadeleştirilmiş madalyon."""
    ctx.line([(x, y - 56 * s), (x, y - 18 * s)], 7 * s, GOLD_D, 1.0)
    ctx.ring(x, y - 62 * s, 8 * s, 3.5 * s, GOLD_D)
    body = [(-34, 0), (-28, -16), (-10, -22), (12, -20), (30, -10), (38, 8), (30, 24), (6, 30), (-18, 26), (-32, 16)]
    P = [(x + a * s, y + b * s) for a, b in body]
    ctx.poly(smooth_closed(P, 4), GOLD_L)
    ctx.line(smooth_closed(P, 4) + [smooth_closed(P, 4)[0]], 2.6 * s, GOLD_D, 1.0)
    ctx.line([(x - 20 * s, y + 4 * s), (x + 24 * s, y + 6 * s)], 2.0 * s, GOLD_D, 0.8)
    ctx.line([(x - 18 * s, y + 14 * s), (x + 20 * s, y + 16 * s)], 2.0 * s, GOLD_D, 0.8)
    ctx.ring(x - 14 * s, y - 14 * s, 14 * s, 4 * s, GOLD_D)
    ctx.circ(x - 22 * s, y - 14 * s, 3 * s, INK)
