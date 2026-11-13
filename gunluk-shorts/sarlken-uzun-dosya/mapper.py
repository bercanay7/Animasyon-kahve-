"""Harita çizimi: vektör kıyılar (numpy ile hızlı dönüşüm), tarihsel bölge boyaları, dağ simgeleri, etiketler, şehirler, rotalar, gemiler, ordular.
Kamera = engine.Ctx kamerası; harita dünyası `mapdata` (Mercator; zoom=1'de 1° boylam = 32 px).
Çizim sırası: deniz → dalga çizgileri → kara gölgesi → kara → bölge boyaları → kıyı mürekkebi → dağlar → (etiket/şehir/rota)."""
import math
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw

import mapdata as MD
from engine import *  # noqa
from inkpaint import *  # noqa

SEA_TOP = Hx("#C2D0C8")
SEA_BOT = Hx("#A9BDB8")
LAND = Hx("#F3E8C6")
LAND_SH = Hx("#7D9494")
COAST = Hx("#4A3322")

_D = {}


def _data():
    if not _D:
        d = MD.data()
        _D["d"] = d
        bb = {}
        for k, lv in d["regions"].items():
            bb[k] = {z: [(r, (float(r[0][:, 0].min()), float(r[0][:, 1].min()), float(r[0][:, 0].max()), float(r[0][:, 1].max()))) for r in rings]
                     for z, rings in lv.items()}
        _D["reg"] = bb
        _D["rip"] = [(dd, [(r, (float(r[:, 0].min()), float(r[:, 1].min()), float(r[:, 0].max()), float(r[:, 1].max()))) for r in rs])
                     for dd, rs in d["ripples"]]
        _D["mount"] = d["mount"]
    return _D


def _level(zoom):
    best, bd = MD.LEVELS[0], 9e9
    for z in MD.LEVELS:
        dd = abs(math.log(z) - math.log(max(zoom, 1e-3)))
        if dd < bd:
            best, bd = z, dd
    return best


def _view(ctx, margin=60.0):
    zp, cxp, cyp = ctx._k()
    hw, hh = W / 2 / zp + margin, H / 2 / zp + margin
    return cxp - hw, cyp - hh, cxp + hw, cyp + hh


def _xf(ctx, arr):
    zp, cxp, cyp = ctx._k()
    k = zp * SS
    ox = (W / 2 + ctx.shx) * SS
    oy = (H / 2 + ctx.shy) * SS
    q = (arr.astype(np.float64) - np.array([cxp, cyp])) * k + np.array([ox, oy])
    return [tuple(p) for p in q.tolist()]


def _vis(bb, v):
    return not (bb[2] < v[0] or bb[0] > v[2] or bb[3] < v[1] or bb[1] > v[3])


# ───────────────────────── kamera ─────────────────────────
def cam_geo(ctx, lon, lat, zoom, shake=(0.0, 0.0)):
    x, y = MD.to_world(lon, lat)
    ctx.cam(x, y, zoom, shake)


def wx(lon, lat):
    return MD.to_world(lon, lat)


# ───────────────────────── zemin ─────────────────────────
def sea(ctx, t=0.0, top=SEA_TOP, bot=SEA_BOT):
    ctx.im.paste(Image.new("RGB", ctx.im.size, top), (0, 0))
    ctx.vgrad(0, 0, W, H, [(0.0, top), (1.0, bot)])
    # sönük dalga işaretleri (ekran uzayında sabit; haritayla kayar gibi görünmesin diye çok hafif)
    rs = np.random.RandomState(5)
    col = mix(top, SEAW_DD, 0.30)
    for i in range(46):
        x = rs.rand() * W
        y = rs.rand() * H
        L = 24 + rs.rand() * 30
        ctx.line([(x, y), (x + L * 0.5, y - 2.5), (x + L, y)], 1.4, col, 1.0, cap=False)


def ripples(ctx, ripple_col=None):
    D = _data()
    v = _view(ctx, 120)
    z = ctx.z
    cols = [mix(SEA_TOP, SEAW_DD, 0.62), mix(SEA_TOP, SEAW_DD, 0.45), mix(SEA_TOP, SEAW_DD, 0.30)]
    wd = [1.5, 1.3, 1.2]
    for (dd, rings), col, w in zip(D["rip"], cols, wd):
        for r, bb in rings:
            if _vis(bb, v):
                q = _xf(ctx, r)
                ctx.d.line(q, fill=col, width=max(1, int(w * z * SS)))


def land(ctx, fill=LAND, shadow=True, coast=True, ow=1.7):
    D = _data()
    lv = _level(ctx.z)
    v = _view(ctx, 80)
    rings = [(r, bb) for r, bb in D["reg"]["__kara__"][lv] if _vis(bb, v)]
    if shadow:
        sh = 5.0 * ctx.z * SS
        for (r, holes), bb in rings:
            q = [(a + sh, b + sh * 1.15) for a, b in _xf(ctx, r)]
            ctx.d.polygon(q, fill=LAND_SH)
    sea_mid = mix(SEA_TOP, SEA_BOT, 0.5)
    for (r, holes), bb in rings:
        ctx.d.polygon(_xf(ctx, r), fill=fill)
        for h in holes:
            ctx.d.polygon(_xf(ctx, h), fill=sea_mid)
    if coast:
        w = max(1, int(ow * ctx.z * SS))
        for (r, holes), bb in rings:
            ctx.d.line(_xf(ctx, r), fill=COAST, width=w)
            for h in holes:
                ctx.d.line(_xf(ctx, h), fill=COAST, width=w)


class Layer:
    """Yarı saydam bölge boyaları için RGBA katman."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.im = Image.new("RGBA", ctx.im.size, (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)
        self.n = 0

    def region(self, name, color, alpha=0.55, outline=True, ow=2.4, ocol=None, level=None):
        if alpha <= 0.01:
            return
        D = _data()
        lv = level or _level(self.ctx.z)
        v = _view(self.ctx, 80)
        a = int(255 * clamp(alpha))
        oc = ocol or shade(color, -0.45)
        for (r, holes), bb in D["reg"][name][lv]:
            if not _vis(bb, v):
                continue
            q = _xf(self.ctx, r)
            self.d.polygon(q, fill=tuple(color) + (a,))
            for h in holes:
                self.d.polygon(_xf(self.ctx, h), fill=(0, 0, 0, 0))
            if outline:
                self.d.line(q, fill=tuple(oc) + (min(255, a + 60),), width=max(1, int(ow * self.ctx.z * SS)))
                self.n += 1
        self.n += 1

    def done(self):
        if self.n:
            self.ctx.im.paste(self.im, (0, 0), self.im.getchannel("A"))


def coast_ink(ctx, ow=1.7):
    D = _data()
    lv = _level(ctx.z)
    v = _view(ctx, 80)
    w = max(1, int(ow * ctx.z * SS))
    for (r, holes), bb in D["reg"]["__kara__"][lv]:
        if _vis(bb, v):
            ctx.d.line(_xf(ctx, r), fill=COAST, width=w)
            for h in holes:
                ctx.d.line(_xf(ctx, h), fill=COAST, width=w)


def mountains(ctx, col=None, alpha_fill=True):
    D = _data()
    m = D["mount"]
    v = _view(ctx, 40)
    sel = m[(m[:, 0] > v[0]) & (m[:, 0] < v[2]) & (m[:, 1] > v[1]) & (m[:, 1] < v[3])]
    ink = col or INK_L
    for x, y, s, sd in sel.tolist():
        pts = [(x - s * 1.15, y + s * 0.55), (x - s * 0.2, y - s * 0.75), (x + s * 0.15, y - s * 0.9), (x + s * 1.15, y + s * 0.55)]
        ctx.poly(pts, LAND)
        ctx.line(pts, 1.35, ink, 1.0, cap=False)
        ctx.line([(x + s * 0.12, y - s * 0.85), (x + s * 0.5, y + s * 0.35)], 1.0, ink, 0.8, cap=False)
        ctx.line([(x + s * 0.34, y - s * 0.4), (x + s * 0.9, y + s * 0.4)], 1.0, ink, 0.6, cap=False)


# ───────────────────────── yazı ─────────────────────────
@lru_cache(maxsize=512)
def _label_sprite(text, px, color, halo, tracking, path, halo_w):
    f = font(path, px * SS)
    adv = []
    for ch in text:
        adv.append(f.getlength(ch) + tracking * px * SS)
    total = int(sum(adv)) + 8 * SS + int(halo_w * SS * 2)
    h = int(px * SS * 1.7) + int(halo_w * SS * 2)
    lay = Image.new("RGBA", (max(8, total), h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x = int(halo_w * SS) + 4 * SS
    for ch, a in zip(text, adv):
        if halo:
            d.text((x, h // 2), ch, font=f, fill=tuple(halo) + (255,), anchor="lm", stroke_width=int(halo_w * SS), stroke_fill=tuple(halo) + (255,))
        d.text((x, h // 2), ch, font=f, fill=tuple(color) + (255,), anchor="lm")
        x += a
    return lay


def blit_world(ctx, sprite, x, y, scale=1.0, rot=0.0, alpha=1.0, anchor=(0.5, 0.5), zoom_scale=True):
    """Sprite'ı dünya konumuna yerleştir (kamera ölçeğiyle büyür)."""
    k = (ctx._k()[0] if zoom_scale else 1.0) * scale
    w = max(1, int(sprite.width * k))
    h = max(1, int(sprite.height * k))
    if w > 6000 or h > 6000 or w < 2:
        return
    sx, sy = ctx.X(x, y)
    s = sprite.resize((w, h), Image.BILINEAR if k < 1.0 else Image.BICUBIC)
    if rot:
        s = s.rotate(rot, resample=Image.BICUBIC, expand=True)
    a = s.getchannel("A")
    if alpha < 0.999:
        a = a.point(lambda v: int(v * alpha))
    ctx.im.paste(s.convert("RGB"), (int(sx - s.width * anchor[0]), int(sy - s.height * anchor[1])), a)


def label(ctx, text, lon, lat, px=18, color=INK, halo=PARCH_L, tracking=0.0, rot=0.0, path=None, alpha=1.0, halo_w=2.2, anchor=(0.5, 0.5), dx=0.0, dy=0.0):
    path = path or FONT_MAP_IT
    spr = _label_sprite(text, px, tuple(color), tuple(halo) if halo else None, tracking, path, halo_w)
    x, y = wx(lon, lat)
    blit_world(ctx, spr, x + dx, y + dy, 1.0 / SS, rot, alpha, anchor)


def label_xy(ctx, text, x, y, px=18, color=INK, halo=PARCH_L, tracking=0.0, rot=0.0, path=None, alpha=1.0, halo_w=2.2, anchor=(0.5, 0.5)):
    path = path or FONT_MAP_IT
    spr = _label_sprite(text, px, tuple(color), tuple(halo) if halo else None, tracking, path, halo_w)
    blit_world(ctx, spr, x, y, 1.0 / SS, rot, alpha, anchor)


def region_name(ctx, text, lon, lat, px=22, color=INK_L, tracking=0.35, rot=0.0, alpha=0.9):
    label(ctx, text, lon, lat, px, color, None, tracking, rot, FONT_TITLE_M, alpha)


# ───────────────────────── şehir / simgeler ─────────────────────────
def city(ctx, lon, lat, name=None, kind="town", s=1.0, px=17, dx=12, dy=-8, anchor=(0.0, 0.5), col=INK, alpha=1.0, halo=PARCH_L):
    x, y = wx(lon, lat)
    z = 1.0
    if kind == "capital":
        pts = [(x - 7 * s, y + 5 * s), (x - 7 * s, y - 5 * s), (x - 4.5 * s, y - 5 * s), (x - 4.5 * s, y - 8 * s), (x - 2 * s, y - 8 * s), (x - 2 * s, y - 5 * s),
               (x + 2 * s, y - 5 * s), (x + 2 * s, y - 8 * s), (x + 4.5 * s, y - 8 * s), (x + 4.5 * s, y - 5 * s), (x + 7 * s, y - 5 * s), (x + 7 * s, y + 5 * s)]
        ctx.poly(pts, PARCH_L)
        ctx.line(pts + [pts[0]], 1.6 * s, col, 1.0)
        ctx.rect(x - 1.8 * s, y - 1 * s, x + 1.8 * s, y + 5 * s, col)
    elif kind == "battle":
        ctx.line([(x - 8 * s, y - 8 * s), (x + 8 * s, y + 8 * s)], 3.2 * s, CRIMSON_D, 1.0)
        ctx.line([(x + 8 * s, y - 8 * s), (x - 8 * s, y + 8 * s)], 3.2 * s, CRIMSON_D, 1.0)
        ctx.circ(x, y, 3.0 * s, CRIMSON_D)
    elif kind == "siege":
        ctx.ring(x, y, 9 * s, 2.6 * s, CRIMSON_D)
        ctx.circ(x, y, 3.2 * s, CRIMSON_D)
    else:
        ctx.circ(x, y, 4.2 * s, PARCH_L)
        ctx.ring(x, y, 4.2 * s, 1.8 * s, col)
        ctx.circ(x, y, 1.5 * s, col)
    if name:
        label(ctx, name, lon, lat, px, col, halo, 0.0, 0.0, FONT_MAP, alpha, 2.4, anchor, dx * s, dy * s)


def crown_icon(ctx, x, y, s=1.0, col=GOLD, ink=INK):
    pts = [(x - 12 * s, y + 7 * s), (x - 14 * s, y - 9 * s), (x - 6 * s, y - 2 * s), (x, y - 12 * s), (x + 6 * s, y - 2 * s), (x + 14 * s, y - 9 * s), (x + 12 * s, y + 7 * s)]
    ctx.poly(pts, col)
    ctx.line(pts + [pts[0]], 1.8 * s, ink, 1.0)
    for dx_ in (-14, 0, 14):
        ctx.circ(x + dx_ * s, y - (9 if dx_ else 12) * s, 2.2 * s, CRIMSON_L)


def ship(ctx, x, y, s=1.0, flip=1, hull=INK_L, sail=PARCH_L, flag=None, t=0.0, bob=1.0, cross=True, galley=False):
    """Küçük karaka / kadırga simgesi (dünya px)."""
    b = math.sin(t * 2.2 + x * 0.05) * 2.0 * s * bob
    X = Xf(x, y + b, s, flip, math.sin(t * 1.6 + y * 0.03) * 2.0 * bob)
    hull_p = X.pts([(-20, 4), (20, 4), (15, 13), (-14, 13)]) if not galley else X.pts([(-26, 5), (26, 3), (20, 11), (-20, 11)])
    ctx.poly(hull_p, hull)
    ctx.line(hull_p + [hull_p[0]], 1.4 * s, INK, 1.0)
    if galley:
        for i in range(-3, 4):
            a = X.p(i * 7, 8)
            bb = X.p(i * 7 - 3, 20)
            ctx.line([a, bb], 1.2 * s, INK, 0.9, cap=False)
        ctx.line([X.p(0, 4), X.p(0, -24)], 1.6 * s, INK, 1.0)
        sp = X.pts([(0, -22), (18, -8), (0, 0)])
    else:
        ctx.line([X.p(0, 4), X.p(0, -26)], 1.8 * s, INK, 1.0)
        sp = X.pts([(-13, -22), (13, -22), (11, -4), (-11, -4)])
    ctx.poly(sp, sail)
    ctx.line(sp + [sp[0]], 1.3 * s, INK, 1.0)
    if cross and not galley:
        ctx.line([X.p(0, -20), X.p(0, -6)], 2.0 * s, CRIMSON, 1.0, cap=False)
        ctx.line([X.p(-6, -14), X.p(6, -14)], 2.0 * s, CRIMSON, 1.0, cap=False)
    if flag is not None:
        fl = X.pts([(0, -26), (14, -23), (0, -20)]) if not galley else X.pts([(0, -24), (13, -21), (0, -18)])
        ctx.poly(fl, flag)


def army(ctx, x, y, w=60, h=26, col=CRIMSON, n=3, s=1.0, alpha=1.0, flag=None):
    """Blok ordu simgesi: sıralı küçük dikdörtgenler."""
    cols = max(2, int(w / (9 * s)))
    for r in range(n):
        for c in range(cols):
            xx = x - w / 2 + (c + 0.5) * w / cols
            yy = y - h / 2 + (r + 0.5) * h / n
            ctx.rect(xx - 3.2 * s, yy - 3.0 * s, xx + 3.2 * s, yy + 3.0 * s, col)
            ctx.rect(xx - 3.2 * s, yy - 3.0 * s, xx + 3.2 * s, yy + 3.0 * s, shade(col, 0.25), 0.0)
    ctx.line([(x - w / 2 - 2 * s, y - h / 2 - 2 * s), (x + w / 2 + 2 * s, y - h / 2 - 2 * s), (x + w / 2 + 2 * s, y + h / 2 + 2 * s), (x - w / 2 - 2 * s, y + h / 2 + 2 * s),
              (x - w / 2 - 2 * s, y - h / 2 - 2 * s)], 1.3 * s, INK, 0.8, cap=False)
    if flag is not None:
        ctx.line([(x, y - h / 2 - 2 * s), (x, y - h / 2 - 22 * s)], 1.6 * s, INK, 1.0, cap=False)
        ctx.poly([(x, y - h / 2 - 22 * s), (x + 16 * s, y - h / 2 - 18 * s), (x, y - h / 2 - 13 * s)], flag)


# ───────────────────────── rota / ok ─────────────────────────
def path_world(pts_lonlat, smooth=True):
    pts = [wx(*p) for p in pts_lonlat]
    return smooth_open(pts, 6) if smooth and len(pts) > 2 else pts


def route(ctx, pts_world, frac=1.0, w=4.0, col=CRIMSON, dash=True, head=True, alpha=1.0, glow=True):
    """Rota çizgisi: kesikli (yürüyen) mürekkep + ok başı. pts_world: dünya px listesi."""
    if frac <= 0.001 or len(pts_world) < 2:
        return None
    P = cut_poly(pts_world, frac)
    if len(P) < 2:
        return None
    if glow:
        ctx.line(P, w * 2.6, PARCH_L, 0.55 * alpha, cap=True)
    if dash:
        # kesik kesik: yol uzunluğu boyunca 18 px çizgi, 9 px boşluk
        acc, on = 0.0, True
        seg = [P[0]]
        out = []
        for a, b in zip(P[:-1], P[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            pos = 0.0
            while pos < L:
                need = (16.0 if on else 8.0) - acc
                step = min(need, L - pos)
                u = (pos + step) / max(L, 1e-6)
                p = (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
                if on:
                    seg.append(p)
                pos += step
                acc += step
                if acc >= (16.0 if on else 8.0) - 1e-6:
                    if on and len(seg) > 1:
                        out.append(seg)
                    on = not on
                    acc = 0.0
                    seg = [p] if on else []
        if on and len(seg) > 1:
            out.append(seg)
        for sg in out:
            ctx.line(sg, w, col, alpha, cap=True)
    else:
        ctx.line(P, w, col, alpha, cap=True)
    if head and len(P) >= 2:
        a, b = P[-2], P[-1]
        if math.hypot(b[0] - a[0], b[1] - a[1]) < 1e-3 and len(P) >= 3:
            a = P[-3]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        L, Wd = w * 4.4, w * 2.6
        tip = (b[0] + math.cos(ang) * L * 0.4, b[1] + math.sin(ang) * L * 0.4)
        bl = (b[0] - math.cos(ang) * L * 0.6 + math.sin(ang) * Wd, b[1] - math.sin(ang) * L * 0.6 - math.cos(ang) * Wd)
        br = (b[0] - math.cos(ang) * L * 0.6 - math.sin(ang) * Wd, b[1] - math.sin(ang) * L * 0.6 + math.cos(ang) * Wd)
        ctx.poly([tip, bl, br], col, alpha)
    return P[-1]


def point_on(pts_world, frac):
    P = cut_poly(pts_world, clamp(frac, 0.0001, 1.0))
    return P[-1]


def compass_rose(ctx, x, y, r=70, t=0.0, alpha=1.0):
    cols = (INK, CRIMSON_D)
    for k, (rr, cc) in enumerate(((r, INK), (r * 0.62, CRIMSON_D))):
        for i in range(4):
            a = i * math.pi / 2 + (math.pi / 4 if k else 0.0)
            tip = (x + math.cos(a) * rr, y + math.sin(a) * rr)
            l = (x + math.cos(a + 0.34) * rr * 0.28, y + math.sin(a + 0.34) * rr * 0.28)
            rgt = (x + math.cos(a - 0.34) * rr * 0.28, y + math.sin(a - 0.34) * rr * 0.28)
            ctx.poly([tip, l, (x, y), rgt], mix(PARCH_L, cc, 0.9) if i % 2 == 0 else PARCH_D, alpha)
            ctx.line([tip, l, (x, y), rgt, tip], 1.4, cc, alpha, cap=False)
    ctx.ring(x, y, r * 0.30, 1.6, INK, alpha)
    ctx.circ(x, y, 4, INK, alpha)
    ctx.text(x, y - r - 16, "K", 20, INK, path=FONT_TITLE_M)
