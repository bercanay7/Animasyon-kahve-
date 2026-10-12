"""Kâğıt-kesme kolaj stili: kesik parçalar (kenarlık + gölge), eklemli kuklalar, stop-motion titreşimi, kâğıt dokusu."""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from engine import *  # noqa

# ortaçağ elyazması paleti
PARCH = (232, 216, 176)
PARCH_LT = (244, 232, 200)
PARCH_DK = (205, 184, 138)
INK = (38, 28, 26)
RED = (158, 42, 43)
RED_LT = (196, 70, 60)
OCHRE = (214, 160, 66)
GOLD = (236, 190, 70)
GREEN = (62, 108, 72)
GREEN_DK = (42, 80, 54)
BLUE = (50, 72, 112)
BLUE_DK = (30, 44, 74)
BROWN = (110, 74, 48)
BROWN_DK = (72, 48, 34)
STONE = (198, 128, 104)
STONE_DK = (160, 98, 80)
SKIN = (236, 192, 154)
ROSE = (226, 128, 120)
NIGHT = (36, 46, 82)
PURPLE = (96, 62, 104)

FPS_SM = 12  # stop-motion hızı


def tq(t):
    """Stop-motion: zamanı 12 fps'e yuvarla"""
    return math.floor(t * FPS_SM + 1e-6) / FPS_SM


def sb(t):
    return int(math.floor(t * FPS_SM + 1e-6))


class Cut:
    """Parça listesi: önce hepsinin gölgesi, sonra kenarlık+dolgu çizilir (kâğıt kesme görünümü)."""

    def __init__(self, ctx, t=0.0, shadow=(7, 9), shadow_a=0.30, rim=2.6, wob=1.1):
        self.ctx, self.t, self.sh, self.sha, self.rim, self.wob = ctx, t, shadow, shadow_a, rim, wob
        self.parts = []

    def add(self, pts, col, seed=0, rim=True, hi=0.0):
        self.parts.append((pts, col, seed, rim, hi))
        return self

    def _wobble(self, pts, seed):
        b = sb(self.t)
        return [(x + (rng_hash(seed, i, b) - 0.5) * 2 * self.wob, y + (rng_hash(seed, i, b, 9) - 0.5) * 2 * self.wob) for i, (x, y) in enumerate(pts)]

    def flush(self):
        ctx = self.ctx
        wp = [(self._wobble(p, s), c, s, r, h) for p, c, s, r, h in self.parts]
        for pts, c, s, r, h in wp:
            ctx.poly([(x + self.sh[0], y + self.sh[1]) for x, y in pts], (20, 12, 8), self.sha)
        for pts, c, s, r, h in wp:
            if r:
                cx = sum(p[0] for p in pts) / len(pts)
                cy = sum(p[1] for p in pts) / len(pts)
                ex = []
                for x, y in pts:
                    d = math.hypot(x - cx, y - cy) + 1e-6
                    ex.append((x + (x - cx) / d * self.rim, y + (y - cy) / d * self.rim))
                ctx.poly(ex, PARCH_LT)
            ctx.poly(pts, c)
            if h:  # üst kenar açık ton (kâğıt kalınlığı)
                ctx.poly(pts, mix(c, (255, 255, 255), h), 0.0)
        self.parts = []


def limb(p0, p1, w0, w1=None):
    """İki nokta arası kapsül (köşeli uç) çokgeni"""
    w1 = w0 if w1 is None else w1
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) + 1e-6
    nx, ny = -dy / L, dx / L
    return [(p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2), (p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2),
            (p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2), (p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2)]


def circle(cx, cy, rx, ry=None, n=14, a0=0.0):
    ry = rx if ry is None else ry
    return [(cx + math.cos(a0 + i * 2 * math.pi / n) * rx, cy + math.sin(a0 + i * 2 * math.pi / n) * ry) for i in range(n)]


def rot_pts(pts, ang, c=(0, 0)):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


# ───────────────────────── kâğıt dokusu / son işlem ─────────────────────────
_TEX = None


def _tex():
    global _TEX
    if _TEX is None:
        rng = np.random.default_rng(1518)
        outs = []
        for k in range(3):
            n = rng.random((H, W)).astype(np.float32)
            n = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), dtype=np.float32) / 255.0
            n = (n - n.mean()) / (n.std() + 1e-6)
            outs.append(n)
        big = rng.random((H // 8, W // 8)).astype(np.float32)
        big = np.asarray(Image.fromarray((big * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), dtype=np.float32) / 255.0
        big = (big - big.mean()) / (big.std() + 1e-6)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.hypot((xx - W / 2) / (W * 0.72), (yy - H * 0.46) / (H * 0.62))
        vig = 1 - 0.30 * np.clip(r - 0.45, 0, 1) ** 1.5
        _TEX = (outs, big, vig.astype(np.float32))
    return _TEX


def paper_post(img, t, still=False, desat=0.0, tint=None):
    outs, big, vig = _tex()
    n = outs[0 if still else (sb(t) % 3)]
    a = np.asarray(img, dtype=np.float32)
    a = a * (1 + n[..., None] * 0.030 + big[..., None] * 0.020)
    if desat > 0:
        g = a.mean(axis=2, keepdims=True)
        a = a + (g - a) * desat
    a = a * vig[..., None]
    if tint is not None:
        a = a * (np.array(tint, np.float32) / 255.0)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
