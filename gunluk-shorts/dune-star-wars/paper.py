"""Kâğıt kesme (paper-cut) diorama stili: katmanlı kumullar, gölgeli kâğıt şekiller, kâğıt tanesi ve vinyet.
Bu videoya özgü görsel dil — mavi baskı / kara kalem / düz renkli illüstrasyon ciltlerinden bilerek ayrıdır."""
import math
import os
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from engine import *  # noqa

FONT_TITLE = os.path.join(HERE, "fonts", "InterDisplay-Black.otf")
FONT_BOLD = os.path.join(HERE, "fonts", "InterDisplay-ExtraBold.otf")
FONT_SERIF = os.path.join(HERE, "fonts", "Lora-Bold.ttf")
FONT_TYPE = "/usr/share/fonts/truetype/freefont/FreeMono.ttf"
if not os.path.exists(FONT_TYPE):
    FONT_TYPE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def Hx(s):
    return hexc(s)


CREAM = Hx("#F7ECD2")
CREAM_SH = Hx("#E3D2A8")
INK = Hx("#2A160E")
RED = Hx("#C8372D")
GOLD = Hx("#F2B63D")
SPICE = Hx("#5BD0FF")      # "mavinin içinde mavi" — Dune baharat rengi
SWYEL = Hx("#FFE45C")      # Star Wars yazı sarısı
WHITE = (255, 255, 255)

PAL = {
    # sıcak, Arrakis
    "dune": dict(sky=[(0, Hx("#C24F1E")), (0.5, Hx("#EE9A4B")), (1.0, Hx("#FBD79A"))],
                 ridges=[Hx("#F5CE92"), Hx("#ECB06A"), Hx("#DC8C47"), Hx("#BA6430"), Hx("#8C4027"), Hx("#5A281F")],
                 sun=Hx("#FFF3D4"), halo=Hx("#FFC47A"), ink=INK, acc=SPICE),
    # soğuk, Tatooine / uzay
    "sw": dict(sky=[(0, Hx("#0A1431")), (0.55, Hx("#27507F")), (1.0, Hx("#8FC9C7"))],
               ridges=[Hx("#EADCAB"), Hx("#CEBC86"), Hx("#AA9B63"), Hx("#7E7249"), Hx("#53492F"), Hx("#2F2B1D")],
               sun=Hx("#FFF7CC"), halo=Hx("#FFD47C"), ink=Hx("#0C1020"), acc=SWYEL),
    # kanca: iki dünyanın karışımı (alacakaranlık)
    "mash": dict(sky=[(0, Hx("#0D2447")), (0.42, Hx("#35557F")), (0.72, Hx("#C86B3C")), (1.0, Hx("#F7BE6A"))],
                 ridges=[Hx("#F0C37D"), Hx("#E3A25D"), Hx("#CB7B3E"), Hx("#A3532C"), Hx("#7A3623"), Hx("#4A2219")],
                 sun=Hx("#FFF1CB"), halo=Hx("#FFB765"), ink=INK, acc=SPICE),
    # Oregon kıyısı
    "oregon": dict(sky=[(0, Hx("#6E8CA0")), (0.55, Hx("#B7C7C4")), (1.0, Hx("#EFE3C5"))],
                   ridges=[Hx("#EFE0B8"), Hx("#E0CC98"), Hx("#C9B27A"), Hx("#9E8C58"), Hx("#6F6A3E"), Hx("#3F4A2D")],
                   sun=Hx("#FFFBEA"), halo=Hx("#FFF0C4"), ink=Hx("#26301F"), acc=GOLD),
}
DESK = {
    "warm": [(0, Hx("#4A2E1D")), (1.0, Hx("#1F120B"))],
    "cool": [(0, Hx("#22344F")), (1.0, Hx("#0C1320"))],
    "ink": [(0, Hx("#2B2420")), (1.0, Hx("#120E0C"))],
}


# ───────────────────────── yardımcılar ─────────────────────────
def tint(c, k):
    return shade(c, k)


def sky(ctx, stops, alpha=1.0):
    ctx.vgrad(0, 0, W, H, stops, alpha)


def ridge_pts(y0, amp, k, ph, x0=-80, x1=W + 80, step=14):
    pts = []
    x = x0
    while x <= x1 + 1e-6:
        y = y0 + amp * (math.sin(x * k + ph) + 0.45 * math.sin(x * k * 2.37 + ph * 1.71 + 1.3) + 0.2 * math.sin(x * k * 4.3 + ph * 0.63 + 2.1))
        pts.append((x, y))
        x += step
    return pts


def layer(ctx, pts, col, bottom=H + 100, shadow=0.22, edge=True, edge_k=0.20):
    """Kâğıt katmanı: üst kenarın gölgesi (arkadaki katmanın üzerine), katman, ince aydınlık kenar çizgisi"""
    if shadow > 0:
        for dy, a in ((-22, 0.45), (-12, 0.7), (-5, 1.0)):
            band = [(x, y + dy) for x, y in pts] + [(x, y + 3) for x, y in reversed(pts)]
            ctx.poly(band, (10, 4, 2), shadow * a * 0.5)
    ctx.poly(pts + [(pts[-1][0], bottom), (pts[0][0], bottom)], col)
    if edge:
        ctx.line(pts, 3, tint(col, edge_k), 0.85, cap=False)


def dunes(ctx, pal, t, base=1010, spread=118, n=6, drift=0.0, amp=26, speed=0.35, shadow=0.24, k0=0.0052):
    """Parallaks kumul katmanları (uzak → yakın). drift: yatay kayma (px), speed: faz hızı"""
    cols = pal["ridges"]
    for i in range(n):
        y0 = base + i * spread * (0.55 + 0.1 * i) / 1.0
        a = amp * (0.7 + 0.28 * i)
        k = k0 * (1.0 + 0.16 * i)
        ph = 1.7 * i + t * speed * (0.25 + 0.2 * i) + drift * 0.0016 * (1 + i)
        pts = ridge_pts(y0, a, k, ph)
        layer(ctx, pts, cols[min(i, len(cols) - 1)], shadow=shadow)


def sun(ctx, x, y, r, pal, a=1.0, rings=True):
    ctx.glow(x, y, r * 3.4, pal["halo"], 0.55 * a)
    if rings:
        ctx.circ(x, y, r * 1.28, pal["halo"], 0.28 * a)
        ctx.circ(x, y, r * 1.12, pal["halo"], 0.38 * a)
    ctx.circ(x, y, r, pal["sun"], a)


def stars(ctx, n, seed, y0=0, y1=700, a=0.9, t=0.0, cols=((255, 255, 255), (255, 236, 190))):
    for i in range(n):
        x = rng_hash(i, seed, 1) * W
        y = y0 + rng_hash(i, seed, 2) * (y1 - y0)
        r = 1.2 + 2.4 * rng_hash(i, seed, 3) ** 2
        tw = 0.6 + 0.4 * math.sin(t * (1.5 + 2 * rng_hash(i, seed, 4)) + i)
        ctx.circ(x, y, r, cols[i % 2], a * tw)


def sand_streaks(ctx, t, col, n=26, y0=900, y1=1500, a=0.22, speed=160, seed=5):
    for i in range(n):
        y = y0 + rng_hash(i, seed, 1) * (y1 - y0)
        ln = 90 + 200 * rng_hash(i, seed, 2)
        x = ((rng_hash(i, seed, 3) * (W + 600) + t * speed * (0.6 + rng_hash(i, seed, 4))) % (W + 600)) - 300
        ctx.line([(x, y), (x + ln, y - 6)], 2.4, col, a * (0.5 + 0.5 * rng_hash(i, seed, 6)), cap=True)


def pshape(ctx, pts, col, sh=(8, 12), sh_a=0.30, edge=0.18, closed=True):
    """Gölgeli kâğıt çokgen"""
    if sh_a > 0:
        ctx.poly([(x + sh[0], y + sh[1]) for x, y in pts], (8, 4, 2), sh_a)
    ctx.poly(pts, col)
    if edge:
        e = list(pts) + [pts[0]] if closed else list(pts)
        ctx.line(e, 2.4, tint(col, edge), 0.9, cap=False)


def prect(ctx, x0, y0, x1, y1, col, sh=(8, 12), sh_a=0.30, edge=0.18, r=0):
    pshape(ctx, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col, sh, sh_a, edge)


def pcirc(ctx, x, y, r, col, sh=(6, 9), sh_a=0.28, edge=0.15, n=36):
    pts = circ_poly(x, y, r, n)
    pshape(ctx, pts, col, sh, sh_a, edge)


def circ_poly(cx, cy, rx, ry=None, n=36, rot=0.0):
    ry = rx if ry is None else ry
    c, s = math.cos(rot), math.sin(rot)
    out = []
    for i in range(n):
        a = i * 2 * math.pi / n
        px, py = math.cos(a) * rx, math.sin(a) * ry
        out.append((cx + px * c - py * s, cy + px * s + py * c))
    return out


def ptext(ctx, x, y, s, px, col=INK, path=FONT_TITLE, anchor="mm", shadow=None, stroke=0, stroke_col=None):
    """Kâğıt metin; shadow=(dx,dy,renk) verilirse altına kesik gölge"""
    if shadow:
        ctx.text(x + shadow[0], y + shadow[1], s, px, shadow[2], path=path, anchor=anchor, stroke=stroke, stroke_fill=shadow[2] if stroke else None)
    ctx.text(x, y, s, px, col, path=path, anchor=anchor, stroke=stroke, stroke_fill=stroke_col)


def stamp(ctx, cx, cy, text, px, col=RED, rot=-8.0, k=1.0, path=FONT_TITLE):
    """Lastik damga: çift çerçeve + yazı; k 0..1 giriş (büyükten oturur)"""
    if k <= 0:
        return
    sc = 1.0 + (1 - clamp(k)) * 0.9
    X = Xf(cx, cy, sc, rot=rot)
    f = font(path, px)
    rows = text.split("\n")
    wd = max(f.getlength(r) for r in rows)
    hh = px * 0.78 + (len(rows) - 1) * px * 0.53
    box = [(-wd / 2 - 26, -hh), (wd / 2 + 26, -hh), (wd / 2 + 26, hh), (-wd / 2 - 26, hh), (-wd / 2 - 26, -hh)]
    box2 = [(x * 0.97, y * 0.9) for x, y in box]
    a = clamp(k * 1.6)
    ctx.line(X.pts(box), 7 * sc, col, a)
    ctx.line(X.pts(box2), 2.5 * sc, col, a * 0.8)
    if k > 0.2:
        for i, r in enumerate(rows):
            ctx.text(*X.p(0, 3 + (i - (len(rows) - 1) / 2) * px * 1.06), r, px * sc, col, path=path)


# ───────────────────────── paneller ─────────────────────────
class Patch(Ctx):
    """Kendi boyutunda 2x tuval; yerel koordinat = piksel"""

    def __init__(self, w, h, bg=(0, 0, 0)):
        self.im = Image.new("RGB", (int(w * SS), int(h * SS)), bg)
        self.d = ImageDraw.Draw(self.im)
        self.cx, self.cy, self.z = W / 2, H / 2, 1.0
        self.shx = self.shy = 0.0
        self.par = 1.0
        self.size = (int(w), int(h))

    def finish(self):
        return self.im.reduce(SS)


@lru_cache(maxsize=16)
def _rr_mask(w, h, r):
    m = Image.new("L", (w * 2, h * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * 2 - 1, h * 2 - 1], radius=r * 2, fill=255)
    return m.resize((w, h), Image.LANCZOS)


@lru_cache(maxsize=16)
def _rr_shadow(w, h, r):
    pad = 40
    m = Image.new("L", (w + pad * 2, h + pad * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([pad, pad, pad + w, pad + h], radius=r, fill=150)
    return m.filter(ImageFilter.GaussianBlur(14))


def paste_panel(img, patch, x, y, r=28, shadow=True, alpha=1.0):
    w, h = patch.size
    if shadow:
        sm = _rr_shadow(w, h, r)
        if alpha < 1:
            sm = sm.point(lambda v: int(v * alpha))
        img.paste((6, 3, 2), (int(x) - 40 + 8, int(y) - 40 + 14), sm)
    m = _rr_mask(w, h, r)
    if alpha < 1:
        m = m.point(lambda v: int(v * alpha))
    img.paste(patch, (int(x), int(y)), m)


def desk(ctx, kind="warm", t=0.0):
    ctx.vgrad(0, 0, W, H, DESK[kind])
    # süzülen toz zerrecikleri (hareket hissi)
    for i in range(26):
        x = (rng_hash(i, 21, 1) * W + t * (8 + 10 * rng_hash(i, 21, 2))) % W
        y = (rng_hash(i, 21, 3) * H - t * (6 + 8 * rng_hash(i, 21, 4))) % H
        ctx.circ(x, y, 2 + 3 * rng_hash(i, 21, 5), (255, 236, 200), 0.07 + 0.08 * rng_hash(i, 21, 6))
    # tahta damarı: çok hafif yatay çizgiler
    for i in range(0, 64):
        y = i * 32 + (rng_hash(i, 11, 1) * 14)
        ctx.line([(0, y), (W, y + (rng_hash(i, 11, 2) - 0.5) * 10)], 2, (0, 0, 0), 0.06 + 0.05 * rng_hash(i, 11, 3), cap=False)


# ───────────────────────── son işlem ─────────────────────────
_GR = None
_VG = None


def paper_post(img, t=0.0, grain=0.0075, vig=0.30, warm=0.0):
    """Vinyet + çok hafif tane (bantlanmayı kırar). Tane hareketli sahnede bit hızını katlar: 0,05 → 134 MB, 0,0075 → ~65 MB."""
    global _GR, _VG
    if _GR is None:
        rs = np.random.RandomState(7)
        g = rs.randn(H // 2, W // 2).astype(np.float32)
        g = np.kron(g, np.ones((2, 2), np.float32))
        _GR = g
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.hypot((xx - W / 2) / (W * 0.74), (yy - H * 0.47) / (H * 0.62))
        _VG = (1 - vig * np.clip(r - 0.38, 0, 1) ** 1.5).astype(np.float32)
    a = np.asarray(img, dtype=np.float32)
    a = a * _VG[..., None] * (1 + grain * _GR[..., None])
    if warm:
        a[..., 0] *= 1 + warm
        a[..., 2] *= 1 - warm
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


def tr_up(s):
    return s.replace("i", "İ").replace("ı", "I").upper()


def cut_poly(pts, frac):
    """Çoklu çizgiyi başlangıçtan frac oranında keser"""
    if frac >= 0.999:
        return list(pts)
    if frac <= 0.001:
        return [pts[0], (pts[0][0] + 0.01, pts[0][1])]
    L = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts[:-1], pts[1:])]
    tot, acc, out = sum(L) * frac, 0.0, [pts[0]]
    for (a, b), l in zip(zip(pts[:-1], pts[1:]), L):
        if acc + l >= tot:
            u = (tot - acc) / max(l, 1e-6)
            out.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u))
            return out
        out.append(b)
        acc += l
    return out
