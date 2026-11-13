"""Boyalı nesneler: etiket, damga, kapsül/hap, mikrop, masa, pencere, çiftlik evi, pamuk, tabak ve yiyecekler, şişe, gemi ..."""
import math

from kukla import *  # noqa


def P(ctx, pts, fill, ow=7.0, seed=0, t=0.0, **kw):
    return shape(ctx, pts, fill, ow=ow, seed=seed, t=t, **kw)


def rrect_pts(x0, y0, x1, y1, r=14):
    return smooth_closed([(x0 + r, y0), (x1 - r, y0), (x1, y0 + r), (x1, y1 - r), (x1 - r, y1), (x0 + r, y1), (x0, y1 - r), (x0, y0 + r)], 4)


# ───────────────────────── işaretler ─────────────────────────
def sparkle(ctx, x, y, r, col=LAMP, a=1.0, rot=0.0):
    pts = []
    for i in range(8):
        ang = rot + i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.26
        pts.append((x + rr * math.cos(ang), y + rr * math.sin(ang)))
    ctx.poly(pts, col, a)


def check(ctx, x, y, s, k, col=OLIVE_D, t=0.0):
    """Boyalı onay işareti; k 0..1 çizilir."""
    if k <= 0:
        return
    pts = [(x - 34 * s, y + 2 * s), (x - 10 * s, y + 28 * s), (x + 40 * s, y - 34 * s)]
    ctx.line(cut_poly(pts, clamp(k * 1.4)), 17 * s, INK, 1.0, cap=True)
    ctx.line(cut_poly(pts, clamp(k * 1.4)), 10 * s, col, 1.0, cap=True)


def cross(ctx, x, y, s, k, col=BRICK):
    if k <= 0:
        return
    a = [(x - 46 * s, y - 46 * s), (x + 46 * s, y + 46 * s)]
    b = [(x + 46 * s, y - 46 * s), (x - 46 * s, y + 46 * s)]
    for seg, (u0, u1) in ((a, (0, 0.5)), (b, (0.5, 1.0))):
        q = clamp((k - u0) / (u1 - u0))
        if q > 0:
            pp = cut_poly(seg, q)
            ctx.line(pp, 26 * s, INK, 1.0, cap=True)
            ctx.line(pp, 17 * s, col, 1.0, cap=True)


def tag(ctx, cx, cy, text, px, col=CREAM, ink=INK, rot=0.0, k=1.0, path=FONT_SOFT_BLACK, seed=0, t=0.0, pad=(34, 20), fill_text=INK, hole=False):
    """Boyalı kâğıt etiket (pop girişli)."""
    if k <= 0:
        return
    f = font(path, px)
    w = f.getlength(text) + pad[0] * 2
    h = px * 1.15 + pad[1] * 2
    sc = back_out(clamp(k), 2.0) if k < 1 else 1.0
    X = Xf(cx, cy, max(0.05, sc), rot=rot)
    box = X.pts([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)])
    P(ctx, box, col, ow=6.5, seed=seed, t=t, wob_amp=1.2, smooth=False, shade=(shade(col, -0.18), 7, 0.45))
    if hole:
        ctx.circ(*X.p(-w / 2 + 24, 0), 8 * sc, INK)
    ctx.text(*X.p(0, px * 0.04), text, px * sc, fill_text, path=path)
    return w, h


def stamp(ctx, cx, cy, text, px, col=BRICK, rot=-8.0, k=1.0, path=FONT_SLAB, sub=None):
    """Lastik damga: çift çerçeve + yazı; k 0..1 giriş (büyükten oturur)."""
    if k <= 0:
        return
    sc = 1.0 + (1 - clamp(k)) * 0.9
    X = Xf(cx, cy, sc, rot=rot)
    rows = text.split("\n")
    f = font(path, px)
    wd = max(f.getlength(r) for r in rows)
    hh = px * 0.80 + (len(rows) - 1) * px * 0.56
    box = [(-wd / 2 - 30, -hh), (wd / 2 + 30, -hh), (wd / 2 + 30, hh), (-wd / 2 - 30, hh), (-wd / 2 - 30, -hh)]
    box2 = [(x * 0.965, y * 0.90) for x, y in box]
    a = clamp(k * 1.6)
    ctx.line(X.pts(box), 10 * sc, col, a)
    ctx.line(X.pts(box2), 3.5 * sc, col, a * 0.85)
    if k > 0.2:
        for i, r in enumerate(rows):
            ctx.text(*X.p(0, 3 + (i - (len(rows) - 1) / 2) * px * 1.08), r, px * sc, col, path=path)


def bubble(ctx, x, y, w, h, tail, col=CREAM, thought=False, seed=0, t=0.0, k=1.0):
    """Konuşma/düşünce balonu; tail = (tx, ty)."""
    if k <= 0:
        return
    sc = back_out(clamp(k), 1.8)
    cx, cy = x, y
    pts = blob(cx, cy, w / 2 * sc, h / 2 * sc, 14, 0.06, seed)
    if thought:
        tx, ty = tail
        for i, r in enumerate((16, 11, 7)):
            u = (i + 1) / 4.0
            P(ctx, ellipse_pts(cx + (tx - cx) * (0.55 + 0.4 * u) , cy + h / 2 * sc + (ty - cy - h / 2 * sc) * u * 1.0, r * sc, r * sc, 14), col, ow=5, seed=seed + i, t=t, wob_amp=0.5)
    else:
        tx, ty = tail
        tri = [(cx - 28 * sc, cy + h / 2 * sc - 10), (cx + 28 * sc, cy + h / 2 * sc - 10), (tx, ty)]
        P(ctx, tri, col, ow=7, seed=seed + 9, t=t, wob_amp=0.6)
    P(ctx, pts, col, ow=7, seed=seed, t=t, wob_amp=1.2)
    if not thought:
        ctx.poly([(cx - 22 * sc, cy + h / 2 * sc - 6), (cx + 22 * sc, cy + h / 2 * sc - 6), (cx + 18 * sc, cy + h / 2 * sc + 8), (cx - 18 * sc, cy + h / 2 * sc + 8)], col)


# ───────────────────────── kapsül / hap / mikrop ─────────────────────────
def capsule_icon(ctx, cx, cy, w, h, rot=-18.0, c1=CREAM, c2=BRICK, ow=9.0, seed=0, t=0.0, split=0.5):
    X = Xf(cx, cy, 1.0, rot=rot)
    r = h / 2
    x0, x1 = -w / 2, w / 2
    xm = x0 + w * split
    # tek parça gövde (kontur) + iki renkli yarı
    body = [(x0 + r + r * math.cos(math.pi / 2 + math.pi * i / 12), r * math.sin(math.pi / 2 + math.pi * i / 12)) for i in range(13)]
    body += [(x1 - r + r * math.cos(-math.pi / 2 + math.pi * i / 12), r * math.sin(-math.pi / 2 + math.pi * i / 12)) for i in range(13)]
    Pw = wob(X.pts(body), 1.1, seed, t)
    outline(ctx, Pw, ow, INK, seed)
    ctx.poly(Pw, c2)
    c = Clip(ctx, Pw)
    if c.ok:
        left = [(x0 - 4, -r - 4), (xm, -r - 4), (xm, r + 4), (x0 - 4, r + 4)]
        c.poly(X.pts(left), c1)
        c.poly(X.pts([(x0 + 14, -r * 0.62), (x1 - 14, -r * 0.62), (x1 - 14, -r * 0.34), (x0 + 14, -r * 0.34)]), WHITE, 0.30)
        c.line(X.pts([(xm, -r), (xm, r)]), 4, INK, 0.7)
        c.done()


DOUGH = Hx("#E2CC9C")


def pill(ctx, x, y, r, rot=0.0, col=None, seed=0, t=0.0, ow=5.0):
    """Un-hamur hap: kırıntılı hamur topu (tabak/kraker kırıntısıyla karıştırılmış)."""
    col = col or DOUGH
    P(ctx, blob(x, y, r, r * 0.9, 9, 0.12, seed, rot), col, ow=ow, seed=seed, t=t, wob_amp=0.6, shade=(shade(col, -0.24), r * 0.30, 0.55))
    for i in range(4):
        ctx.circ(x + (rng_hash(seed, i, 1) - 0.5) * r * 1.0, y + (rng_hash(seed, i, 2) - 0.5) * r * 0.8, max(1.6, r * 0.10), Hx("#8A6A3E"), 0.7)
    ctx.poly(blob(x - r * 0.3, y - r * 0.32, r * 0.2, r * 0.12, 6, 0.1, seed), WHITE, 0.5)


def germ(ctx, x, y, r, t=0.0, col=OLIVE, seed=0, eyes=True, mood="mean", wiggle=1.0, ow=8.0):
    """Mikrop kuklası: dikenli yeşil top, kızgın gözler."""
    tt = tq(t)
    pts = []
    n = 16
    for i in range(n * 2):
        a = i * math.pi / n
        rr = r * (1.0 if i % 2 == 0 else 1.0 + 0.30 + 0.06 * math.sin(tt * 5 + i))
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    P(ctx, pts, col, ow=ow, seed=seed, t=tt, wob_amp=1.0, shade=(shade(col, -0.28), r * 0.14, 0.5))
    # dikenlerin ucuna damlalar
    for i in range(0, n * 2, 4):
        a = i * math.pi / n
        ctx.circ(x + r * 1.34 * math.cos(a), y + r * 1.34 * math.sin(a), r * 0.07, INK)
    P(ctx, blob(x, y, r * 0.86, r * 0.86, 12, 0.03, seed + 2), col, ow=0, seed=seed, t=tt, wob_amp=0.4)
    if eyes:
        for sx in (-1, 1):
            ex, ey = x + sx * r * 0.30, y - r * 0.12
            P(ctx, ellipse_pts(ex, ey, r * 0.19, r * 0.22, 12), CREAM, ow=4.5, seed=seed + 3 + sx, t=tt, wob_amp=0.4)
            ctx.poly(ellipse_pts(ex + sx * r * 0.02, ey + r * 0.03, r * 0.08, r * 0.1, 8), INK)
        if mood == "mean":
            ink_line(ctx, [(x - r * 0.55, y - r * 0.50), (x - r * 0.1, y - r * 0.33)], 7, INK, seed + 5, tt, 0.3)
            ink_line(ctx, [(x + r * 0.55, y - r * 0.50), (x + r * 0.1, y - r * 0.33)], 7, INK, seed + 6, tt, 0.3)
            ink_line(ctx, [(x - r * 0.30, y + r * 0.40), (x - r * 0.1, y + r * 0.30), (x + r * 0.1, y + r * 0.40), (x + r * 0.3, y + r * 0.30)], 6, INK, seed + 7, tt, 0.4, smooth=True)
        else:
            ink_line(ctx, [(x - r * 0.28, y + r * 0.34), (x, y + r * 0.46), (x + r * 0.28, y + r * 0.34)], 6, INK, seed + 7, tt, 0.4, smooth=True)


# ───────────────────────── mobilya / mekân ─────────────────────────
def table(ctx, x0, x1, ytop, col=OCHRE_D, depth=84, seed=0, t=0.0, edge=58, bottom=H + 60):
    top = [(x0 + 36, ytop), (x1 - 36, ytop), (x1, ytop + depth), (x0, ytop + depth)]
    P(ctx, top, shade(col, 0.14), ow=7, seed=seed, wob_amp=1.0, wash=(shade(col, 0.2), shade(col, 0.06), 0.4), dry=(shade(col, -0.2), 16, 0.30))
    front = [(x0, ytop + depth), (x1, ytop + depth), (x1, ytop + depth + edge), (x0, ytop + depth + edge)]
    P(ctx, front, shade(col, -0.06), ow=7, seed=seed + 1, wob_amp=1.0, dry=(shade(col, -0.3), 10, 0.30))
    under = [(x0, ytop + depth + edge - 2), (x1, ytop + depth + edge - 2), (x1, bottom), (x0, bottom)]
    c = Clip(ctx, under)
    if c.ok:
        c.gradient(shade(col, -0.50), Hx("#140B06"), 1.0)
        c.done()


def plank_wall(ctx, y0, y1, col, seed=0, gap=118):
    ctx.rect(0, y0, W, y1, col)
    x = 0
    k = 0
    while x < W:
        w = gap * (0.85 + 0.3 * rng_hash(seed, k, 1))
        ctx.line([(x, y0), (x + (rng_hash(seed, k, 2) - 0.5) * 4, y1)], 5, shade(col, -0.30), 0.55, cap=False)
        x += w
        k += 1
    for i in range(60):
        yy = y0 + (y1 - y0) * rng_hash(seed, i, 3)
        xx = rng_hash(seed, i, 4) * W
        ctx.line([(xx, yy), (xx + 60 + 160 * rng_hash(seed, i, 5), yy + (rng_hash(seed, i, 6) - 0.5) * 6)], 4, shade(col, 0.16 if i % 2 else -0.16), 0.22, cap=True)


def window(ctx, x, y, w, h, sky=Hx("#CFE3E8"), frame=INK_L, seed=0, light=True, t=0.0):
    P(ctx, rrect_pts(x - 18, y - 18, x + w + 18, y + h + 18, 8), shade(frame, 0.05), ow=8, seed=seed, wob_amp=1.0)
    ctx.poly(rrect_pts(x, y, x + w, y + h, 4), sky)
    c = Clip(ctx, rrect_pts(x, y, x + w, y + h, 4))
    if c.ok:
        c.gradient(shade(sky, 0.2), shade(sky, -0.08), 0.8)
        c.poly([(x + w * 0.1, y + h * 0.1), (x + w * 0.46, y + h * 0.1), (x + w * 0.2, y + h * 0.5)], WHITE, 0.35)
        c.done()
    mx, my = x + w / 2, y + h / 2
    ctx.line([(mx, y), (mx, y + h)], 11, frame, 1.0, cap=False)
    ctx.line([(x, my), (x + w, my)], 11, frame, 1.0, cap=False)
    P(ctx, rrect_pts(x - 30, y + h + 6, x + w + 30, y + h + 30, 6), shade(frame, 0.12), ow=6, seed=seed + 2, wob_amp=0.8)


def light_shaft(ctx, x, y, w, h, tx, ty, col=(255, 236, 190), a=0.20, t=0.0):
    """Pencereden zemine uzanan ışık demeti (yarı saydam)."""
    Clip_ = Clip(ctx, [(x, y), (x + w, y), (tx + w * 1.3, ty), (tx - w * 0.2, ty)])
    if Clip_.ok:
        Clip_.fill_all(col, a)
        Clip_.done()
    for i in range(14):
        u = (t * 0.05 + rng_hash(7, i, 1)) % 1.0
        px = lerp(x + w * rng_hash(7, i, 2), tx + w * 0.5 * rng_hash(7, i, 3), u)
        py = lerp(y + h * 0.5, ty, u)
        ctx.circ(px, py, 3 + 3 * rng_hash(7, i, 4), (255, 245, 214), 0.35 * math.sin(math.pi * u))


def lamp(ctx, x, y, s=1.0, t=0.0, glow=1.0):
    ctx.glow(x, y - 60 * s, 380 * s, (255, 200, 110), 0.55 * glow)
    P(ctx, rrect_pts(x - 36 * s, y - 20 * s, x + 36 * s, y + 52 * s, 16 * s), Hx("#6A4A2A"), ow=6 * s, seed=3, wob_amp=0.8, shade=(Hx("#3E2A18"), 6 * s, 0.5))
    P(ctx, rrect_pts(x - 30 * s, y - 100 * s, x + 30 * s, y - 20 * s, 14 * s), Hx("#F7DC9A"), ow=5 * s, seed=4, wob_amp=0.6)
    fl = 1.0 + 0.10 * math.sin(tq(t) * 11.0)
    ctx.poly(smooth_closed([(x, y - 92 * s * fl), (x + 15 * s, y - 56 * s), (x, y - 36 * s), (x - 15 * s, y - 56 * s)], 5), LAMP)
    ctx.poly(smooth_closed([(x, y - 70 * s * fl), (x + 7 * s, y - 52 * s), (x, y - 44 * s), (x - 7 * s, y - 52 * s)], 5), Hx("#FFF0B8"))


def jar(ctx, x, y, s=1.0, label=None, liquid=OCHRE, seed=0, t=0.0, lid=Hx("#8A5A3A")):
    """Cam kavanoz: ışık yansıması + etiket."""
    body = rrect_pts(x - 52 * s, y - 100 * s, x + 52 * s, y + 70 * s, 26 * s)
    P(ctx, body, Hx("#D9ECE6"), ow=7 * s, seed=seed, t=t, wob_amp=0.8)
    c = Clip(ctx, body)
    if c.ok:
        c.poly([(x - 60 * s, y - 40 * s), (x + 60 * s, y - 40 * s), (x + 60 * s, y + 80 * s), (x - 60 * s, y + 80 * s)], liquid, 0.92)
        c.poly([(x - 40 * s, y - 80 * s), (x - 26 * s, y - 80 * s), (x - 30 * s, y + 40 * s), (x - 44 * s, y + 40 * s)], WHITE, 0.45)
        c.done()
    P(ctx, rrect_pts(x - 40 * s, y - 128 * s, x + 40 * s, y - 100 * s, 10 * s), lid, ow=6 * s, seed=seed + 1, wob_amp=0.6)
    if label:
        tag(ctx, x, y + 6 * s, label, 30 * s, col=CREAM, rot=-3, seed=seed + 2, pad=(14 * s, 8 * s), path=FONT_SOFT_BLACK)


def microscope(ctx, x, y, s=1.0, seed=0, t=0.0):
    col = Hx("#8A6A3A")
    P(ctx, rrect_pts(x - 90 * s, y + 150 * s, x + 90 * s, y + 190 * s, 14 * s), shade(col, -0.2), ow=7 * s, seed=seed, wob_amp=0.8)
    P(ctx, [(x - 14 * s, y + 150 * s), (x + 14 * s, y + 150 * s), (x + 40 * s, y - 80 * s), (x + 10 * s, y - 90 * s)], col, ow=7 * s, seed=seed + 1, wob_amp=0.8)
    P(ctx, rrect_pts(x - 70 * s, y + 80 * s, x + 70 * s, y + 100 * s, 8 * s), shade(col, -0.1), ow=6 * s, seed=seed + 2, wob_amp=0.8)
    P(ctx, [(x - 22 * s, y - 100 * s), (x + 60 * s, y - 52 * s), (x + 48 * s, y - 20 * s), (x - 34 * s, y - 68 * s)], Hx("#C9A24A"), ow=7 * s, seed=seed + 3, wob_amp=0.8)
    P(ctx, ellipse_pts(x - 40 * s, y - 112 * s, 20 * s, 14 * s, 14), shade(col, -0.3), ow=6 * s, seed=seed + 4, wob_amp=0.6)


def lens_inset(ctx, cx, cy, r, t=0.0, seed=0, content=None):
    """Mercek: içinde büyütülmüş görüntü."""
    ctx.circ(cx, cy, r + 14, INK)
    ctx.circ(cx, cy, r + 4, Hx("#C9A24A"))
    ctx.circ(cx, cy, r - 6, Hx("#E8F0E2"))
    if content:
        content(cx, cy, r)
    ctx.line([(cx + r * 0.62, cy + r * 0.62), (cx + r * 1.7, cy + r * 1.7)], 28, INK, 1.0)
    ctx.line([(cx + r * 0.62, cy + r * 0.62), (cx + r * 1.7, cy + r * 1.7)], 17, Hx("#8A6A3A"), 1.0)


# ───────────────────────── yiyecek ─────────────────────────
def plate(ctx, cx, cy, rx, ry, seed=0, t=0.0, rim=Hx("#EFE7D2"), rim2=Hx("#3E5E86")):
    P(ctx, ellipse_pts(cx, cy, rx, ry, 36), rim, ow=7, seed=seed, wob_amp=0.9, shade=(shade(rim, -0.2), 8, 0.5))
    ctx.line(ellipse_pts(cx, cy, rx * 0.93, ry * 0.93, 36) + [ellipse_pts(cx, cy, rx * 0.93, ry * 0.93, 36)[0]], 6, rim2, 0.9, cap=False)
    ctx.poly(ellipse_pts(cx, cy + ry * 0.04, rx * 0.74, ry * 0.72, 32), shade(rim, -0.06))


def mush(ctx, cx, cy, rx, ry, seed=0, t=0.0):
    """Mısır lapası: sarı tepecik + kaşık izleri."""
    P(ctx, blob(cx, cy, rx, ry, 12, 0.08, seed), OCHRE_L, ow=6, seed=seed, wob_amp=1.0, shade=(OCHRE_D, 7, 0.45), dry=(OCHRE_D, 9, 0.35))
    for i in range(7):
        ctx.circ(cx + (rng_hash(seed, i, 1) - 0.5) * rx * 1.3, cy + (rng_hash(seed, i, 2) - 0.5) * ry * 1.1, 3.4, OCHRE_D, 0.6)


def molasses(ctx, cx, cy, rx, ry, seed=0, t=0.0):
    P(ctx, blob(cx, cy, rx, ry, 10, 0.12, seed), Hx("#4A2A14"), ow=5, seed=seed, wob_amp=0.8)
    ctx.poly(blob(cx - rx * 0.25, cy - ry * 0.3, rx * 0.3, ry * 0.2, 6, 0.1, seed), Hx("#8A5A2E"), 0.6)


def egg(ctx, x, y, r, seed=0, rot=0.0, yolk=False):
    P(ctx, ellipse_pts(x, y, r * 0.78, r, 18, rot), CREAM, ow=5.5, seed=seed, wob_amp=0.6, shade=(shade(CREAM, -0.18), r * 0.14, 0.5))
    ctx.poly(blob(x - r * 0.22, y - r * 0.3, r * 0.14, r * 0.26, 6, 0.1, seed, rot), WHITE, 0.6)


def meat(ctx, x, y, s=1.0, seed=0):
    """Pirzola: kiremit et, beyaz yağ kenarı, kemik."""
    P(ctx, smooth_closed([(x - 76 * s, y - 6 * s), (x - 40 * s, y - 52 * s), (x + 26 * s, y - 58 * s), (x + 74 * s, y - 20 * s), (x + 66 * s, y + 38 * s), (x + 8 * s, y + 56 * s), (x - 56 * s, y + 38 * s)], 5),
      Hx("#C0654A"), ow=6.5 * s, seed=seed, wob_amp=1.0, shade=(Hx("#8F3F2E"), 8 * s, 0.5), hatch=(Hx("#9C4A36"), 16 * s, 0.30))
    P(ctx, ellipse_pts(x + 20 * s, y - 6 * s, 20 * s, 15 * s, 12), CREAM, ow=4.5 * s, seed=seed + 1, wob_amp=0.5)


def milk(ctx, x, y, s=1.0, seed=0):
    body = rrect_pts(x - 34 * s, y - 70 * s, x + 34 * s, y + 70 * s, 18 * s)
    P(ctx, body, Hx("#F7F2E6"), ow=6.5 * s, seed=seed, wob_amp=0.8, shade=(Hx("#D8CFB8"), 8 * s, 0.5))
    P(ctx, rrect_pts(x - 20 * s, y - 100 * s, x + 20 * s, y - 70 * s, 8 * s), Hx("#F7F2E6"), ow=5.5 * s, seed=seed + 1, wob_amp=0.6)
    P(ctx, rrect_pts(x - 22 * s, y - 108 * s, x + 22 * s, y - 94 * s, 6 * s), Hx("#4F7EA8"), ow=5 * s, seed=seed + 2, wob_amp=0.5)
    ctx.poly(rrect_pts(x - 20 * s, y - 40 * s, x + 20 * s, y + 24 * s, 8 * s), Hx("#4F7EA8"), 0.22)


def jug(ctx, x, y, s=1.0, label=None, seed=0):
    """Pekmez testisi."""
    P(ctx, smooth_closed([(x - 30 * s, y - 100 * s), (x + 30 * s, y - 100 * s), (x + 62 * s, y - 50 * s), (x + 68 * s, y + 40 * s), (x + 40 * s, y + 80 * s), (x - 40 * s, y + 80 * s), (x - 68 * s, y + 40 * s), (x - 62 * s, y - 50 * s)], 5),
      Hx("#8A5A34"), ow=7 * s, seed=seed, wob_amp=1.0, shade=(Hx("#5A3A20"), 10 * s, 0.5), dry=(Hx("#5A3A20"), 12, 0.3))
    P(ctx, ellipse_pts(x + 76 * s, y - 20 * s, 30 * s, 40 * s, 14), Hx("#8A5A34"), ow=7 * s, seed=seed + 1, wob_amp=0.8)
    ctx.poly(ellipse_pts(x + 76 * s, y - 20 * s, 14 * s, 22 * s, 12), Hx("#6A4A2A"))
    P(ctx, rrect_pts(x - 24 * s, y - 120 * s, x + 24 * s, y - 100 * s, 6 * s), Hx("#3E2A18"), ow=5 * s, seed=seed + 2, wob_amp=0.5)
    if label:
        tag(ctx, x, y + 10 * s, label, 26 * s, col=CREAM, rot=-4, seed=seed + 3, pad=(12 * s, 7 * s))


def cornbread(ctx, x, y, w, h, seed=0):
    P(ctx, rrect_pts(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 14), OCHRE_L, ow=6, seed=seed, wob_amp=1.0, shade=(OCHRE_D, 8, 0.5), dry=(OCHRE_D, 10, 0.35))
    for i in range(9):
        ctx.circ(x + (rng_hash(seed, i, 1) - 0.5) * w * 0.8, y + (rng_hash(seed, i, 2) - 0.5) * h * 0.7, 3, OCHRE_D, 0.55)


# ───────────────────────── manzara parçaları ─────────────────────────
def cotton(ctx, x, y, s=1.0, t=0.0, seed=0, sway=1.0):
    """Pamuk bitkisi: yapraklı koyu yeşil gövde, ucunda kahverengi kozalıkta kabarık beyaz koza."""
    sw = math.sin(t * 1.4 + seed) * 5 * sway
    for j in range(3):
        a = (j - 1) * 0.62
        bx = x + math.sin(a) * 78 * s + sw
        by = y - (118 + 22 * (j % 2)) * s
        ctx.line([(x, y), (x + math.sin(a) * 26 * s, y - 62 * s), (bx, by)], 11 * s, INK, 1.0, cap=True)
        ctx.line([(x, y), (x + math.sin(a) * 26 * s, y - 62 * s), (bx, by)], 6.5 * s, OLIVE_D, 1.0, cap=True)
        for lf in range(2):                               # yapraklar
            lx, ly = x + math.sin(a) * (20 + 18 * lf) * s * 1.2 + (14 if lf else -14) * s, y - (36 + 30 * lf) * s
            P(ctx, smooth_closed([(lx, ly), (lx + (24 if lf else -24) * s, ly - 18 * s), (lx + (44 if lf else -44) * s, ly + 2 * s), (lx + (22 if lf else -22) * s, ly + 14 * s)], 4),
              OLIVE if lf else OLIVE_L, ow=4 * s, seed=seed + j * 4 + lf, wob_amp=0.6)
        P(ctx, [(bx - 24 * s, by + 18 * s), (bx - 13 * s, by - 2 * s), (bx, by + 8 * s), (bx + 13 * s, by - 2 * s), (bx + 24 * s, by + 18 * s), (bx, by + 30 * s)], Hx("#7A5232"),
          ow=4.5 * s, seed=seed + j, wob_amp=0.5)
        for q, (dx, dy, r) in enumerate(((-13, -16, 21), (13, -17, 21), (0, -30, 22))):
            P(ctx, blob(bx + dx * s, by + dy * s, r * s, r * 0.92 * s, 9, 0.12, seed + j * 3 + q), Hx("#FFFBF0"), ow=4 * s, seed=seed + j + q, wob_amp=0.5,
              shade=(Hx("#E4D8BE"), 4 * s, 0.5))


def fence(ctx, x0, x1, y, s=1.0, seed=0, col=Hx("#8A6A44")):
    n = int((x1 - x0) / (84 * s)) + 1
    for i in range(n):
        x = x0 + i * 84 * s
        P(ctx, [(x - 11 * s, y), (x + 11 * s, y), (x + 9 * s, y + 130 * s), (x - 9 * s, y + 130 * s)], col, ow=5 * s, seed=seed + i, wob_amp=0.9, dry=(shade(col, -0.3), 4, 0.3))
    ctx.line([(x0 - 20, y + 36 * s), (x1 + 20, y + 40 * s)], 14 * s, INK, 1.0, cap=True)
    ctx.line([(x0 - 20, y + 36 * s), (x1 + 20, y + 40 * s)], 8 * s, shade(col, 0.1), 1.0, cap=True)
    ctx.line([(x0 - 20, y + 84 * s), (x1 + 20, y + 88 * s)], 14 * s, INK, 1.0, cap=True)
    ctx.line([(x0 - 20, y + 84 * s), (x1 + 20, y + 88 * s)], 8 * s, shade(col, 0.1), 1.0, cap=True)


def farmhouse(ctx, x, y, s=1.0, seed=0):
    """Dar uzun 'shotgun' çiftlik evi: teneke çatı, sundurma, kapı ve pencere."""
    wall = Hx("#E8D8B0")
    P(ctx, [(x - 150 * s, y), (x + 150 * s, y), (x + 150 * s, y + 130 * s), (x - 150 * s, y + 130 * s)], wall, ow=7 * s, seed=seed, wob_amp=1.0, shade=(CREAM_D, 8 * s, 0.5))
    for i in range(1, 11):
        ctx.line([(x - 150 * s + i * 27 * s, y + 4), (x - 150 * s + i * 27 * s, y + 126 * s)], 3 * s, shade(wall, -0.25), 0.55, cap=False)
    P(ctx, [(x - 176 * s, y + 4), (x, y - 96 * s), (x + 176 * s, y + 4)], Hx("#8C8C84"), ow=8 * s, seed=seed + 1, wob_amp=1.0, hatch=(Hx("#6A6A62"), 14 * s, 0.4), shade=(Hx("#5E5E58"), 8 * s, 0.45))
    P(ctx, [(x - 24 * s, y + 130 * s), (x - 24 * s, y + 40 * s), (x + 24 * s, y + 40 * s), (x + 24 * s, y + 130 * s)], Hx("#7A5438"), ow=6 * s, seed=seed + 2, wob_amp=0.8)
    P(ctx, rrect_pts(x - 118 * s, y + 38 * s, x - 62 * s, y + 90 * s, 4), Hx("#8FB3C2"), ow=5.5 * s, seed=seed + 3, wob_amp=0.7)
    P(ctx, rrect_pts(x + 62 * s, y + 38 * s, x + 118 * s, y + 90 * s, 4), Hx("#8FB3C2"), ow=5.5 * s, seed=seed + 4, wob_amp=0.7)
    P(ctx, [(x - 70 * s, y + 130 * s), (x + 70 * s, y + 130 * s), (x + 80 * s, y + 146 * s), (x - 80 * s, y + 146 * s)], Hx("#8A6A44"), ow=5.5 * s, seed=seed + 5, wob_amp=0.7)


def ship(ctx, x, y, s=1.0, t=0.0, seed=0, rock=0.0, sacks=True):
    """Yelkenli gemi: koyu gövde, çizgili yelken, mısır çuvalları (fırtınalı deniz paleti)."""
    ang = math.radians(rock)
    X = Xf(x, y, s, rot=rock)
    hull = [(-250, -10), (-210, 56), (-120, 84), (130, 84), (230, 40), (276, -30), (214, -6), (-250, -10)]
    mast_h = 380
    P(ctx, X.pts(smooth_closed([(-250, -30), (-210, 56), (-120, 84), (130, 84), (230, 40), (290, -50), (214, -8), (0, -16)], 4)), Hx("#2E3A52"), ow=9 * s, seed=seed, wob_amp=1.2,
      shade=(Hx("#1C2436"), 10 * s, 0.5), hatch=(Hx("#46567A"), 22 * s, 0.30))
    ctx.line(X.pts([(0, -10), (0, -mast_h)]), 14 * s, INK, 1.0)
    ctx.line(X.pts([(0, -10), (0, -mast_h)]), 8 * s, Hx("#8A6A44"), 1.0)
    sail = X.pts([(-170, -mast_h + 30), (170, -mast_h + 30), (150, -90), (-150, -90)])
    P(ctx, sail, CREAM, ow=8 * s, seed=seed + 1, wob_amp=1.4, shade=(CREAM_D, 12 * s, 0.5))
    c = Clip(ctx, sail)
    if c.ok:
        for i in range(4):
            c.poly(X.pts([(-200, -mast_h + 60 + i * 66), (200, -mast_h + 60 + i * 66), (200, -mast_h + 90 + i * 66), (-200, -mast_h + 90 + i * 66)]), BRICK, 0.85)
        c.done()
    if sacks:
        for i, sx_ in enumerate((-150, -80, -10, 60, 130)):
            P(ctx, X.pts(smooth_closed([(sx_ - 30, -4), (sx_ - 36, -50), (sx_ - 12, -74), (sx_ + 12, -74), (sx_ + 36, -50), (sx_ + 30, -4)], 4)), Hx("#C9A765"), ow=6 * s, seed=seed + 10 + i, wob_amp=0.9,
              shade=(Hx("#9A7C45"), 6 * s, 0.5))
            ctx.circ(*X.p(sx_, -48), 9 * s, OCHRE_L, 0.9)


def waves(ctx, y0, t, cols, amp=26, seed=0, speed=1.0, n=4):
    """Kıvrık tepeli dalga şeritleri (fırtına paleti)."""
    for i in range(n):
        yy = y0 + i * 110
        pts = []
        for k in range(0, int(W / 18) + 8):
            x = k * 18 - 60
            pts.append((x, yy + amp * (1 + 0.15 * i) * math.sin(x * 0.011 + t * speed * (1.3 + 0.2 * i) + i * 1.7) + 8 * math.sin(x * 0.031 + t * 2.1 + i)))
        poly = pts + [(pts[-1][0], H + 80), (pts[0][0], H + 80)]
        ctx.poly(poly, cols[min(i, len(cols) - 1)])
        ctx.line(pts, 7, shade(cols[min(i, len(cols) - 1)], 0.35), 0.9, cap=False)
        for k in range(0, len(pts), 7):
            x, y = pts[k]
            ctx.line([(x, y), (x + 20, y - 26), (x + 42, y - 18)], 6, shade(cols[min(i, len(cols) - 1)], 0.5), 0.8, cap=True)


def corn_cob(ctx, x, y, s=1.0, rot=0.0, seed=0, face=False, t=0.0, arms=0.0):
    X = Xf(x, y, s, rot=rot)
    if arms > 0:
        for sx in (-1, 1):
            sh = (sx * 38, -10)
            hd = (sx * (96 + 10 * arms), -10 - 120 * arms)
            el = (sx * (84 + 16 * arms), -10 - 54 * arms)
            P(ctx, X.pts(capsule(sh, el, 15, 13)), OLIVE, ow=6 * s, seed=seed + 20 + sx, wob_amp=0.7)
            P(ctx, X.pts(capsule(el, hd, 13, 12)), OLIVE_L, ow=6 * s, seed=seed + 22 + sx, wob_amp=0.7)
            P(ctx, X.pts(ellipse_pts(hd[0], hd[1] - 6, 20, 20, 12)), OLIVE_L, ow=5.5 * s, seed=seed + 24 + sx, wob_amp=0.6)
    husk_l = X.pts(smooth_closed([(-10, 110), (-64, 20), (-46, -90), (-8, -20)], 4))
    husk_r = X.pts(smooth_closed([(10, 110), (64, 20), (46, -90), (8, -20)], 4))
    P(ctx, husk_l, OLIVE, ow=6 * s, seed=seed + 1, wob_amp=0.9, shade=(OLIVE_D, 6 * s, 0.5))
    P(ctx, husk_r, OLIVE_L, ow=6 * s, seed=seed + 2, wob_amp=0.9, shade=(OLIVE, 6 * s, 0.5))
    cob = X.pts(smooth_closed([(0, -128), (34, -100), (42, -30), (28, 50), (0, 74), (-28, 50), (-42, -30), (-34, -100)], 5))
    P(ctx, cob, OCHRE_L, ow=7 * s, seed=seed, wob_amp=0.9, shade=(OCHRE_D, 8 * s, 0.5))
    c = Clip(ctx, cob)
    if c.ok:
        for r in range(8):
            for q in range(4):
                c.ell(*X.p(-24 + q * 16 + (r % 2) * 7, -108 + r * 22), 6.5 * s, 7.5 * s, OCHRE_D, 0.55)
        c.done()
    if face:
        for sx in (-1, 1):
            ctx.poly(ellipse_pts(*X.p(sx * 14, -52), 6 * s, 7.5 * s, 10), INK)
        ink_line(ctx, [X.p(-12, -22), X.p(0, -14), X.p(12, -22)], 6 * s, INK, seed + 5, t, 0.3, smooth=True)


def clay_pot(ctx, x, y, s=1.0, t=0.0, seed=0, fill=True):
    body = smooth_closed([(-120, -80), (120, -80), (160, 10), (130, 100), (60, 140), (-60, 140), (-130, 100), (-160, 10)], 5)
    X = Xf(x, y, s)
    P(ctx, X.pts(body), Hx("#B8683E"), ow=9 * s, seed=seed, wob_amp=1.3, shade=(Hx("#7E4326"), 14 * s, 0.5), hatch=(Hx("#9C5532"), 22 * s, 0.30))
    P(ctx, X.pts(ellipse_pts(0, -80, 124, 26, 28)), Hx("#7E4326"), ow=8 * s, seed=seed + 1, wob_amp=0.9)
    if fill:
        ctx.poly(X.pts(ellipse_pts(0, -80, 108, 19, 26)), Hx("#F2E7CF"))      # kireçli süt gibi su
        for i in range(9):
            ctx.poly(blob(*X.p(-84 + i * 21 + 6 * math.sin(i), -82 + 3 * math.cos(i * 2)), 11 * s, 8 * s, 7, 0.2, seed + i), OCHRE_L)
    for j in range(3):                         # bant süsü
        ctx.line(X.pts([(-130 + j * 4, 30 + j * 20), (130 - j * 4, 30 + j * 20)]), 6 * s, CREAM, 0.7, cap=False)


def steam(ctx, x, y, t, n=5, col=(255, 250, 235), h=300, a=0.5):
    for i in range(n):
        u = (t * 0.35 + i / n) % 1.0
        xx = x + 36 * math.sin(u * 5 + i * 1.7) + (i - n / 2) * 18
        yy = y - u * h
        r = 22 + 46 * u
        ctx.circ(xx, yy, r, col, a * (1 - u) ** 1.2)


def tombstone(ctx, x, y, s=1.0, text="J. GOLDBERGER", year="1929", seed=0):
    body = [(x + a * s, y + b * s) for a, b in smooth_closed([(-90, 0), (-90, -190), (-60, -250), (0, -270), (60, -250), (90, -190), (90, 0)], 6)]
    P(ctx, body, Hx("#B9B2A4"), ow=8 * s, seed=seed, wob_amp=1.2, shade=(Hx("#8C857A"), 10 * s, 0.5), dry=(Hx("#8C857A"), 12, 0.3))
    ctx.text(x, y - 170 * s, text, 17 * s, INK, path=FONT_SOFT_BLACK)
    ctx.text(x, y - 108 * s, year, 46 * s, INK, path=FONT_SLAB)
    ctx.poly([(x - 120 * s, y), (x + 120 * s, y), (x + 150 * s, y + 24 * s), (x - 150 * s, y + 24 * s)], Hx("#6F7A3E"))


def bottle(ctx, x, y, s=1.0, label="NİASİN", seed=0):
    body = rrect_pts(x - 70 * s, y - 120 * s, x + 70 * s, y + 160 * s, 36 * s)
    P(ctx, body, Hx("#7A4A22"), ow=8 * s, seed=seed, wob_amp=1.0, shade=(Hx("#4A2A12"), 12 * s, 0.5))
    P(ctx, rrect_pts(x - 34 * s, y - 190 * s, x + 34 * s, y - 120 * s, 12 * s), Hx("#7A4A22"), ow=7 * s, seed=seed + 1, wob_amp=0.8)
    P(ctx, rrect_pts(x - 28 * s, y - 214 * s, x + 28 * s, y - 188 * s, 8 * s), Hx("#D9B070"), ow=6 * s, seed=seed + 2, wob_amp=0.7)
    ctx.poly([(x - 48 * s, y - 100 * s), (x - 30 * s, y - 100 * s), (x - 34 * s, y + 120 * s), (x - 50 * s, y + 120 * s)], WHITE, 0.30)
    tag(ctx, x, y + 14 * s, label, 38 * s, col=CREAM, rot=0, seed=seed + 3, pad=(20 * s, 12 * s), path=FONT_SLAB)
    ctx.text(x, y + 74 * s, "B3", 30 * s, BRICK_D, path=FONT_SLAB)
