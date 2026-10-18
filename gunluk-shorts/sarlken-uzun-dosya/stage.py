"""Kâğıt-tiyatro dioramaları: katmanlar (parallaks) + siluet figürler + mimari/dekor ilkelleri + atmosfer.

Kullanım (çekim şablonunda):
    sc = stage.scene("hall_brussels", build_fn)      # katmanlar bir kez pişirilir (skia.Image), önbelleğe alınır
    stage.draw(f, sc, cam=stage.SCam(x, y, z), t=cx.t, dyn={depth: fn(f, t)})  # kare başına yalnız dönüşüm
Koordinatlar: sahne tuvali 1920×1080 (merkez 960,540); derinlik d: 0=sonsuz uzak (kaymaz), 1=odak düzlemi, >1 yakın (daha çok kayar).
Figürler: stage.figure(f, kind, x, y_ayak, h, ...) — siluet + kenar ışığı; önbellekli sprite.
"""
import math
import os
from functools import lru_cache

import numpy as np
import skia

import sk
from sk import C, Frame, H, W, clamp, lerp, mix

MARGIN = 220


class SCam:
    def __init__(self, x=W / 2, y=H / 2, z=1.0):
        self.x, self.y, self.z = x, y, z


def bake(draw_fn, m=MARGIN):
    f = Frame(W + 2 * m, H + 2 * m)
    f.clear(skia.ColorTRANSPARENT)
    f.c.translate(m, m)
    draw_fn(f)
    return f.surf.makeImageSnapshot()


_SCENES = {}


class Scene:
    def __init__(self, name, layers):
        self.name = name
        self.layers = layers     # [(depth, Image)]


def scene(name, builder):
    """builder() → [(depth, draw_fn(f))]  — her katman kendi Frame'ine (1920×1080 koordinatı) çizer."""
    if name not in _SCENES:
        if len(_SCENES) > 4:
            _SCENES.pop(next(iter(_SCENES)))
        _SCENES[name] = Scene(name, [(d, bake(fn)) for d, fn in builder()])
    return _SCENES[name]


def layer_transform(f, cam, depth):
    s = 1 + (cam.z - 1) * depth
    f.c.translate(W / 2, H / 2)
    f.c.scale(s, s)
    f.c.translate(-W / 2 - (cam.x - W / 2) * depth, -H / 2 - (cam.y - H / 2) * depth)


def draw(f, sc, cam, t=0.0, dyn=None, alpha=1.0):
    """Katmanları arkadan öne çiz; dyn = {katman_indeksi: fn(f, t)} dinamik öğeler (aynı dönüşümle)."""
    for i, (depth, img) in enumerate(sc.layers):
        f.c.save()
        layer_transform(f, cam, depth)
        p = skia.Paint(AntiAlias=True)
        if alpha < 1:
            p.setAlphaf(alpha)
        f.c.drawImage(img, -MARGIN, -MARGIN, skia.SamplingOptions(skia.FilterMode.kLinear), p)
        if dyn and i in dyn:
            dyn[i](f, t)
        f.c.restore()


# ───────────────────────────── renk/derinlik ─────────────────────────────
def fog(col, depth, fogc="#3A2616", k=0.65):
    """Uzak katman = sise doğru karışım. depth 0..1."""
    return mix(col, fogc, k * (1 - clamp(depth)))


# ───────────────────────────── mimari ilkeller ─────────────────────────────
def pointed_arch_path(cx, base_y, w, h, thick=0):
    """Sivri kemer (iki daire yayı). w: açıklık, h: toplam yükseklik (tepe)."""
    hw = w / 2
    spring = base_y - (h - hw * 0.9)
    p = skia.Path()
    p.moveTo(cx - hw - thick, base_y)
    p.lineTo(cx - hw - thick, spring)
    p.cubicTo(cx - hw - thick, spring - hw * 0.75, cx - hw * 0.35, base_y - h - thick * 0.5, cx, base_y - h - thick)
    p.cubicTo(cx + hw * 0.35, base_y - h - thick * 0.5, cx + hw + thick, spring - hw * 0.75, cx + hw + thick, spring)
    p.lineTo(cx + hw + thick, base_y)
    p.close()
    return p


def arch(f, cx, base_y, w, h, stone="#4A3220", edge="#8A6338", glow=None, depth=1.0, thick=34):
    outer = pointed_arch_path(cx, base_y, w + 2 * thick, h + thick * 1.2)
    inner = pointed_arch_path(cx, base_y, w, h)
    f.path(outer, shader=f.lin(cx - w / 2, base_y - h, cx + w / 2, base_y, [(mix(stone, "#FFFFFF", 0.08), 0.0), (stone, 0.5), (mix(stone, "#000000", 0.35), 1.0)]))
    f.c.save()
    f.c.clipPath(inner, skia.ClipOp.kIntersect, True)
    if glow:
        f.rect(cx - w / 2 - 10, base_y - h - 10, w + 20, h + 20, shader=f.lin(0, base_y - h, 0, base_y, [(glow[0], 0.0), (glow[1], 1.0)]))
    else:
        f.rect(cx - w / 2 - 10, base_y - h - 10, w + 20, h + 20, color=mix(stone, "#000000", 0.7))
    f.c.restore()
    f.path(inner, style="stroke", sw=4, color=edge, alpha=0.75)
    f.path(outer, style="stroke", sw=3, color=mix(edge, "#000000", 0.4), alpha=0.8)


def column(f, x, y0, y1, w, stone="#4A3220", edge="#9A7340", cap=True):
    f.rect(x - w / 2, y0, w, y1 - y0, shader=f.lin(x - w / 2, 0, x + w / 2, 0, [(mix(stone, "#000000", 0.45), 0.0), (mix(stone, "#FFFFFF", 0.10), 0.35), (stone, 0.7), (mix(stone, "#000000", 0.5), 1.0)]))
    for k in range(-2, 3):                                  # oluklar
        f.line(x + k * w * 0.18, y0, x + k * w * 0.18, y1, color="#000000", sw=1.4, alpha=0.22)
    if cap:
        f.rect(x - w * 0.78, y0 - w * 0.22, w * 1.56, w * 0.26, color=mix(stone, "#FFFFFF", 0.06))
        f.rect(x - w * 0.64, y0 - w * 0.42, w * 1.28, w * 0.22, color=mix(stone, "#FFFFFF", 0.1))
        f.rect(x - w * 0.8, y1 - w * 0.1, w * 1.6, w * 0.24, color=mix(stone, "#FFFFFF", 0.05))
        f.rect(x - w * 0.9, y1 + w * 0.12, w * 1.8, w * 0.22, color=mix(stone, "#000000", 0.2))
    f.line(x - w / 2, y0, x - w / 2, y1, color=edge, sw=1.6, alpha=0.5)


def gothic_window(f, cx, cy, w, h, glow=("#FFE3A0", "#E0902E"), stone="#3A2415", edge="#8A6338", tracery=True, k=1.0):
    """Sivri vitray pencere: sıcak parlak iç + taş kafes."""
    inner = pointed_arch_path(cx, cy + h / 2, w, h)
    f.path(pointed_arch_path(cx, cy + h / 2, w + 36, h + 40), color=stone)
    f.c.save(); f.c.clipPath(inner, skia.ClipOp.kIntersect, True)
    f.rect(cx - w / 2, cy - h / 2 - 20, w, h + 40, shader=f.lin(0, cy - h / 2, 0, cy + h / 2, [(glow[0], 0.0), (glow[1], 1.0)]))
    f.circle(cx, cy - h * 0.1, w * 0.9, shader=f.rad(cx, cy - h * 0.1, w * 0.9, [("#FFFFFF", 0.0, int(140 * k)), ("#FFFFFF", 1.0, 0)]))
    if tracery:
        for dx in (-w * 0.17, w * 0.17):
            f.line(cx + dx, cy - h / 2, cx + dx, cy + h / 2, color=stone, sw=7)
        for yy in (-0.2, 0.15, 0.45):
            f.line(cx - w / 2, cy + h * yy, cx + w / 2, cy + h * yy, color=stone, sw=5)
        f.circle(cx, cy - h * 0.28, w * 0.2, style="stroke", sw=6, color=stone)
    f.c.restore()
    f.path(inner, style="stroke", sw=6, color=edge, alpha=0.9)


def banner(f, x, y, w, h, color="#8E1F26", trim="#C9962B", icon=None, wave=0.0, seed=0):
    """Asılı sancak (uçları dilimli)."""
    pts = [(x - w / 2, y), (x + w / 2, y), (x + w / 2 + wave * 3, y + h * 0.45), (x + w / 2 - wave * 2, y + h * 0.85), (x, y + h), (x - w / 2 + wave * 2, y + h * 0.85), (x - w / 2 - wave * 3, y + h * 0.45)]
    path = sk.smooth_path(pts, True, 0.25)
    f.path(path, shader=f.lin(x, y, x, y + h, [(mix(color, "#FFFFFF", 0.1), 0.0), (color, 0.5), (mix(color, "#000000", 0.4), 1.0)]))
    f.path(path, style="stroke", sw=4, color=trim, alpha=0.9)
    f.line(x - w / 2 - 10, y, x + w / 2 + 10, y, color="#B88A3A", sw=8)
    if icon:
        import icons
        icons.draw_icon(f, icon, x, y + h * 0.42, size=w * 0.62, metal="gold", shadow=False)


def floor_hall(f, y0, y1, c0="#1A100A", c1="#3B2616", vp_x=W / 2, tile=True, sheen=("#FFD58A", 0.10)):
    """Perspektifli taş zemin: ufuktan öne koyulaşan→aydınlanan, çatlak/kare çizgileri ve yansıma."""
    f.rect(-MARGIN, y0, W + 2 * MARGIN, y1 - y0 + MARGIN, shader=f.lin(0, y0, 0, y1, [(c0, 0.0), (c1, 1.0)]))
    if tile:
        n = 14
        for i in range(n + 1):
            u = i / n
            yy = y0 + (y1 - y0) * (u ** 1.8)
            f.line(-MARGIN, yy, W + MARGIN, yy, color="#000000", sw=1.2 + 2 * u, alpha=0.30)
        for i in range(-12, 13):
            xb = vp_x + i * 260
            f.line(vp_x + (xb - vp_x) * 0.05, y0, xb * 1.0 + (xb - vp_x) * 0.6, y1 + 60, color="#000000", sw=1.6, alpha=0.26)
    f.rect(-MARGIN, y0, W + 2 * MARGIN, (y1 - y0), shader=f.lin(0, y0, 0, y1, [(C(sheen[0], 0), 0.0) if False else ("#FFFFFF", 0.0, 0), (sheen[0], 1.0, int(255 * sheen[1]))]))


def dais(f, x, y, w, h, steps=3, c="#5A3A22", edge="#B88A3A"):
    for i in range(steps):
        ww = w * (1 - i * 0.12)
        yy = y - i * h / steps
        f.rect(x - ww / 2, yy - h / steps, ww, h / steps, shader=f.lin(0, yy - h / steps, 0, yy, [(mix(c, "#FFFFFF", 0.12), 0.0), (mix(c, "#000000", 0.35), 1.0)]))
        f.line(x - ww / 2, yy - h / steps, x + ww / 2, yy - h / steps, color=edge, sw=2, alpha=0.7)


def throne(f, x, y, s=1.0, c="#6A1E26", gold="#C9962B"):
    f.path(sk.smooth_path([(x - 70 * s, y), (x - 76 * s, y - 220 * s), (x - 52 * s, y - 330 * s), (x, y - 360 * s), (x + 52 * s, y - 330 * s), (x + 76 * s, y - 220 * s), (x + 70 * s, y)], True, 0.3),
           shader=f.lin(x, y - 360 * s, x, y, [(mix(c, "#FFFFFF", 0.15), 0.0), (c, 0.5), (mix(c, "#000000", 0.45), 1.0)]))
    f.rect(x - 96 * s, y - 118 * s, 192 * s, 28 * s, color=gold)
    f.rect(x - 104 * s, y - 8 * s, 208 * s, 24 * s, color=mix(gold, "#000000", 0.35))
    for sx in (-1, 1):
        f.rect(x + sx * 84 * s - 8 * s, y - 140 * s, 16 * s, 140 * s, color=gold)
        f.circle(x + sx * 84 * s, y - 150 * s, 14 * s, color=gold)
    import icons
    icons.draw_icon(f, "eagle", x, y - 250 * s, size=120 * s, metal="gold", shadow=False)
    f.path(sk.smooth_path([(x - 70 * s, y), (x - 76 * s, y - 220 * s), (x - 52 * s, y - 330 * s), (x, y - 360 * s), (x + 52 * s, y - 330 * s), (x + 76 * s, y - 220 * s), (x + 70 * s, y)], True, 0.3), style="stroke", sw=4, color=gold, alpha=0.85)


def chandelier(f, x, y, r=90, t=0.0, n=8, seed=0):
    f.line(x, -MARGIN, x, y - 30, color="#2A1A0C", sw=4)
    f.oval(x, y, r, r * 0.22, style="stroke", sw=7, color="#B88A3A")
    f.oval(x, y, r * 0.55, r * 0.12, style="stroke", sw=4, color="#B88A3A")
    f.circle(x, y + 16, 10, color="#B88A3A")
    for i in range(n):
        a = math.pi * 2 * i / n
        cx_, cy_ = x + math.cos(a) * r, y + math.sin(a) * r * 0.22
        f.rect(cx_ - 4, cy_ - 22, 8, 22, color="#EADCB5")
    return


def candle_flames(f, x, y, r=90, t=0.0, n=8, seed=0, glow=1.0):
    rs = np.random.RandomState(seed)
    for i in range(n):
        a = math.pi * 2 * i / n
        cx_, cy_ = x + math.cos(a) * r, y + math.sin(a) * r * 0.22
        fl = 0.8 + 0.2 * math.sin(t * 9 + i * 1.9 + rs.rand() * 6)
        f.circle(cx_, cy_ - 30, 46 * fl * glow, shader=f.rad(cx_, cy_ - 30, 46 * fl * glow, [("#FFD58A", 0.0, int(130 * glow)), ("#FFB347", 0.4, int(50 * glow)), ("#FFB347", 1.0, 0)]), blend=skia.BlendMode.kPlus)
        f.oval(cx_, cy_ - 30, 4.5 * fl, 11 * fl, color="#FFF1C2")


def god_rays(f, src, ang, spread, length, n=6, alpha=0.14, color="#FFE2A0", seed=2, blur=20):
    """Işık huzmeleri. PAHALI (bulanıklık katmanları, ~80 ms): yalnız katman pişirme (builder) içinde çağır, dyn() içinde ASLA."""
    sk.light_rays(f, src, ang, spread, length, n=n, alpha=alpha, color=color, seed=seed, blur=blur)


# ───────────────────────────── figürler (siluet) ─────────────────────────────
# Ölçü birimi: h = tam boy. Ayaklar (0,0), yukarı −y. Her tür: (gövde çizen fonksiyon).
def _P(*pts, t=0.4, close=True):
    return sk.smooth_path(pts, close, t)


def _head(p, x, y, r, ry=None):
    ry = ry or r * 1.18
    p.addOval(skia.Rect.MakeLTRB(x - r, y - ry, x + r, y + ry))


FIG = {}


def fig(name):
    def deco(fn):
        FIG[name] = fn
        return fn
    return deco


FIGX = {}


def figx(name):
    """Zengin figür: fn(h, lean) -> (sınır_yolu, çiz(canvas, col, rim)). Canvas orijini ayakta (0,0), yukarı −y; iç ayrıntı/degrade/kenar ışığı serbest."""
    def deco(fn):
        FIGX[name] = fn
        return fn
    return deco


def _hat(p, kind, x, y, s):
    """Başlık (y: baş merkezi). s: baş yarıçapı ölçeği."""
    r = s
    if kind == "beret":
        p.addPath(_P((x - r * 1.9, y - r * 0.5), (x - r * 1.5, y - r * 1.5), (x + r * 0.4, y - r * 2.0), (x + r * 1.9, y - r * 1.1), (x + r * 1.5, y - r * 0.5), (x, y - r * 0.8), t=0.4))
        p.moveTo(x + r * 1.3, y - r * 1.6)
        p.cubicTo(x + r * 2.2, y - r * 2.8, x + r * 3.0, y - r * 2.4, x + r * 2.8, y - r * 1.3)
        p.cubicTo(x + r * 2.6, y - r * 2.0, x + r * 2.0, y - r * 2.1, x + r * 1.3, y - r * 1.6)
    elif kind == "cap":
        p.addPath(_P((x - r * 1.2, y - r * 0.3), (x - r * 1.0, y - r * 1.5), (x + r * 0.2, y - r * 1.9), (x + r * 1.3, y - r * 1.2), (x + r * 1.1, y - r * 0.4), (x, y - r * 0.7), t=0.4))
    elif kind == "plume":     # Landsknecht: geniş kenarlı şapka + tüy
        p.addPath(_P((x - r * 2.6, y - r * 0.6), (x - r * 1.4, y - r * 1.3), (x + r * 1.4, y - r * 1.3), (x + r * 2.8, y - r * 0.6), (x + r * 1.4, y - r * 0.9), (x - r * 1.4, y - r * 0.9), t=0.3))
        p.addPath(_P((x - r * 1.2, y - r * 1.2), (x - r * 0.9, y - r * 2.2), (x + r * 0.9, y - r * 2.2), (x + r * 1.2, y - r * 1.2), t=0.3))
        for k in range(4):
            p.moveTo(x + r * 0.6 + k * r * 0.2, y - r * 2.1)
            p.cubicTo(x + r * 1.6 + k * r * 0.6, y - r * 3.2, x + r * 2.4 + k * r * 0.7, y - r * 3.0, x + r * 2.6 + k * r * 0.5, y - r * 2.0)
    elif kind == "turban":
        p.addOval(skia.Rect.MakeLTRB(x - r * 1.6, y - r * 2.7, x + r * 1.6, y - r * 0.4))
        p.addOval(skia.Rect.MakeLTRB(x - r * 1.8, y - r * 1.3, x + r * 1.8, y - r * 0.2))
    elif kind == "kavuk":     # yeniçeri bork
        p.addPath(_P((x - r * 1.0, y - r * 0.5), (x - r * 0.9, y - r * 2.6), (x + r * 0.9, y - r * 2.6), (x + r * 1.0, y - r * 0.5), t=0.2))
        p.addPath(_P((x - r * 1.0, y - r * 0.9), (x - r * 2.0, y - r * 1.6), (x - r * 2.2, y + r * 0.8), (x - r * 1.0, y + r * 0.3), t=0.3))
    elif kind == "helmet":    # morion
        p.addPath(_P((x - r * 1.3, y - r * 0.3), (x - r * 1.1, y - r * 1.5), (x, y - r * 2.2), (x + r * 1.1, y - r * 1.5), (x + r * 1.3, y - r * 0.3), (x + r * 2.3, y - r * 0.5), (x + r * 1.0, y - r * 0.9), (x - r * 2.3, y - r * 0.5), t=0.3))
    elif kind == "cowl":
        p.addPath(_P((x - r * 1.5, y + r * 1.4), (x - r * 1.5, y - r * 0.8), (x, y - r * 1.9), (x + r * 1.5, y - r * 0.8), (x + r * 1.5, y + r * 1.4), (x + r * 0.9, y + r * 0.5), (x - r * 0.9, y + r * 0.5), t=0.3))
    elif kind == "crown":
        p.addPath(sk.poly_path([(x - r * 1.1, y - r * 0.5), (x - r * 1.2, y - r * 1.7), (x - r * 0.6, y - r * 1.1), (x, y - r * 1.9), (x + r * 0.6, y - r * 1.1), (x + r * 1.2, y - r * 1.7), (x + r * 1.1, y - r * 0.5)], True))
    elif kind == "galero":    # kardinal şapkası
        p.addPath(_P((x - r * 2.6, y - r * 0.6), (x, y - r * 1.2), (x + r * 2.6, y - r * 0.6), (x + r * 1.2, y - r * 1.8), (x - r * 1.2, y - r * 1.8), t=0.3))
    elif kind == "veil":
        p.addPath(_P((x - r * 1.4, y + r * 1.6), (x - r * 1.5, y - r * 0.8), (x, y - r * 1.6), (x + r * 1.5, y - r * 0.8), (x + r * 1.3, y + r * 3.2), (x + r * 0.2, y + r * 0.6), (x - r * 0.9, y + r * 2.6), t=0.3))
    elif kind == "feather":
        for k in range(5):
            a = -0.9 + k * 0.4
            p.moveTo(x, y - r * 0.8)
            p.cubicTo(x + math.sin(a) * r * 2.5, y - r * 2.2, x + math.sin(a) * r * 3.5, y - r * 3.6, x + math.sin(a) * r * 3.2 + r * 0.2, y - r * 4.4)
            p.cubicTo(x + math.sin(a) * r * 3.0, y - r * 3.2, x + math.sin(a) * r * 2.0, y - r * 2.0, x + r * 0.15, y - r * 0.8)


def _robe(h, w_sh=0.17, w_hem=0.22, waist=0.46, lean=0.0, flare=1.0):
    """Uzun cüppe gövdesi (omuz→etek)."""
    H_ = h
    return _P((-w_sh * H_, -0.745 * H_), (w_sh * H_, -0.745 * H_), ((w_sh * 1.1 + lean * 0.5) * H_, -0.60 * H_), ((w_sh * 0.85 + lean * 0.2) * H_, -waist * H_), (w_hem * flare * H_, -0.04 * H_), (w_hem * flare * 0.5 * H_, 0), (-w_hem * flare * 0.5 * H_, 0), (-w_hem * flare * H_, -0.04 * H_), (-w_sh * 0.85 * H_, -waist * H_), (-w_sh * 1.1 * H_, -0.60 * H_), t=0.35)


def _pair_path(h):
    """İmparator (yaşlı, kambur, baston) + genç prens yardımı. Koordinatlar imparator boyuna (h) göre; sol=prens."""
    p = skia.Path()
    S_ = h
    def pt(x, y):
        return (x * S_, y * S_)
    # prens
    p.addPath(_P(pt(-0.78, -0.835), pt(-0.46, -0.84), pt(-0.45, -0.60), pt(-0.46, -0.50), pt(-0.40, -0.40), pt(-0.84, -0.40), pt(-0.78, -0.50), pt(-0.79, -0.62), t=0.3))
    for sx0, sx1 in ((-0.80, -0.66), (-0.62, -0.46)):
        p.addPath(_P(pt(sx0, -0.41), pt(sx1, -0.41), pt(sx1 - 0.02, -0.12), pt(sx1 + 0.01, -0.02), pt(sx1 + 0.05, 0), pt(sx0 - 0.02, 0), pt(sx0 + 0.02, -0.12), t=0.3))
    _head(p, -0.60 * S_, -0.925 * S_, 0.058 * S_)
    p.addRect(skia.Rect.MakeLTRB(-0.64 * S_, -0.88 * S_, -0.56 * S_, -0.83 * S_))
    _hat(p, "beret", -0.60 * S_, -0.925 * S_, 0.058 * S_)
    # imparator
    p.addPath(_P(pt(-0.30, -0.70), pt(-0.12, -0.78), pt(0.12, -0.76), pt(0.22, -0.66), pt(0.22, -0.46), pt(0.30, -0.04), pt(0.14, 0), pt(-0.14, 0), pt(-0.30, -0.04), pt(-0.22, -0.46), pt(-0.30, -0.60), t=0.35))
    _head(p, 0.07 * S_, -0.835 * S_, 0.060 * S_)
    p.addRect(skia.Rect.MakeLTRB(0.02 * S_, -0.80 * S_, 0.11 * S_, -0.74 * S_))
    _hat(p, "cap", 0.07 * S_, -0.835 * S_, 0.060 * S_)
    # sol kol → prensin omzunda
    p.addPath(_P(pt(-0.14, -0.74), pt(-0.30, -0.72), pt(-0.50, -0.84), pt(-0.55, -0.82), pt(-0.52, -0.78), pt(-0.32, -0.64), pt(-0.12, -0.62), t=0.3))
    # sağ kol + baston
    p.addPath(_P(pt(0.16, -0.72), pt(0.28, -0.60), pt(0.31, -0.46), pt(0.26, -0.45), pt(0.20, -0.56), pt(0.12, -0.64), t=0.3))
    p.addPath(sk.poly_path([pt(0.29, -0.48), pt(0.31, -0.48), pt(0.40, 0.0), pt(0.375, 0.0)], True))
    p.addCircle(0.30 * S_, -0.485 * S_, 0.018 * S_)
    return p


@lru_cache(maxsize=512)
def _fig_path(kind, hpx, lean=0.0):
    h = float(hpx)
    if kind in FIG:                       # dış modüllerin kayıtlı türleri: @ST.fig("ad") def f(h, lean) -> skia.Path
        return FIG[kind](h, lean)
    if kind == "pair_old_prince":
        return _pair_path(h)
    p = skia.Path()
    hr = 0.062 * h
    hy = -0.865 * h
    hx = lean * h * 0.3
    # varsayılan: ayakta bir kişi
    arm_l = arm_r = None
    if kind in ("noble", "merchant", "cardinal", "scribe", "monk", "woman"):
        wsh = {"noble": 0.185, "merchant": 0.17, "cardinal": 0.2, "scribe": 0.165, "monk": 0.2, "woman": 0.15}[kind] * h
        whem = {"noble": 0.25, "merchant": 0.22, "cardinal": 0.3, "scribe": 0.23, "monk": 0.26, "woman": 0.34}[kind] * h
        p.addPath(_robe(h, wsh / h, whem / h, 0.46, lean))
        _head(p, hx, hy, hr)
        p.addRect(skia.Rect.MakeLTRB(hx - hr * 0.5, hy + hr, hx + hr * 0.5, -0.745 * h))
        hat = {"noble": "beret", "merchant": "cap", "cardinal": "galero", "scribe": "cap", "monk": "cowl", "woman": "veil"}[kind]
        _hat(p, hat, hx, hy, hr)
        if kind == "noble":                              # kürk yaka
            p.addPath(_P((-wsh * 1.1, -0.745 * h), (0, -0.70 * h), (wsh * 1.1, -0.745 * h), (wsh * 0.9, -0.77 * h), (-wsh * 0.9, -0.77 * h), t=0.2))
    elif kind == "emperor_old":                         # yaşlı imparator: kambur, baston, geniş omuz
        p.addPath(_P((-0.20 * h, -0.70 * h), (0.10 * h, -0.74 * h), (0.20 * h, -0.62 * h), (0.17 * h, -0.45 * h), (0.25 * h, -0.04 * h), (0.10 * h, 0), (-0.14 * h, 0), (-0.26 * h, -0.04 * h), (-0.19 * h, -0.45 * h), (-0.24 * h, -0.62 * h), t=0.35))
        _head(p, 0.05 * h, -0.80 * h, hr * 1.02)
        _hat(p, "cap", 0.05 * h, -0.80 * h, hr)
        p.addRect(skia.Rect.MakeLTRB(0.01 * h, -0.76 * h, 0.09 * h, -0.70 * h))
        # baston
        p.moveTo(0.25 * h, -0.50 * h); p.lineTo(0.33 * h, -0.02 * h); p.lineTo(0.30 * h, -0.02 * h); p.lineTo(0.22 * h, -0.50 * h); p.close()
        p.addCircle(0.24 * h, -0.51 * h, 0.018 * h)
        # kol
        p.addPath(_P((0.16 * h, -0.66 * h), (0.24 * h, -0.55 * h), (0.25 * h, -0.49 * h), (0.20 * h, -0.50 * h), (0.14 * h, -0.60 * h), t=0.3))
    elif kind in ("prince", "page"):                    # genç, ince; çorap bacaklar
        p.addPath(_P((-0.14 * h, -0.745 * h), (0.14 * h, -0.745 * h), (0.15 * h, -0.55 * h), (0.14 * h, -0.45 * h), (0.16 * h, -0.36 * h), (-0.16 * h, -0.36 * h), (-0.14 * h, -0.45 * h), (-0.15 * h, -0.55 * h), t=0.3))
        for sx in (-1, 1):
            p.addPath(_P((sx * 0.02 * h, -0.38 * h), (sx * 0.12 * h, -0.38 * h), (sx * 0.10 * h, -0.10 * h), (sx * 0.12 * h, -0.02 * h), (sx * 0.15 * h, 0), (sx * 0.02 * h, 0), (sx * 0.05 * h, -0.10 * h), t=0.3))
        _head(p, hx, hy, hr)
        p.addRect(skia.Rect.MakeLTRB(hx - hr * 0.45, hy + hr, hx + hr * 0.45, -0.745 * h))
        _hat(p, "beret", hx, hy, hr)
        p.addPath(_P((-0.14 * h, -0.70 * h), (-0.24 * h, -0.55 * h), (-0.26 * h, -0.42 * h), (-0.20 * h, -0.44 * h), (-0.16 * h, -0.56 * h), t=0.3))
    elif kind in ("pikeman", "landsknecht", "janissary", "knight", "conquistador", "sailor", "native"):
        hat = {"pikeman": "cap", "landsknecht": "plume", "janissary": "kavuk", "knight": "helmet", "conquistador": "helmet", "sailor": "cap", "native": "feather"}[kind]
        wsh = 0.16 * h
        p.addPath(_P((-wsh, -0.745 * h), (wsh, -0.745 * h), (wsh * 1.05, -0.56 * h), (wsh * 0.95, -0.44 * h), (wsh * (1.5 if kind == "landsknecht" else 1.1), -0.34 * h), (-wsh * (1.5 if kind == "landsknecht" else 1.1), -0.34 * h), (-wsh * 0.95, -0.44 * h), (-wsh * 1.05, -0.56 * h), t=0.3))
        for sx in (-1, 1):
            if kind == "janissary":
                p.addPath(_P((sx * 0.0 * h, -0.40 * h), (sx * 0.17 * h, -0.40 * h), (sx * 0.19 * h, -0.02 * h), (sx * 0.02 * h, 0), t=0.3))
            else:
                p.addPath(_P((sx * 0.02 * h, -0.36 * h), (sx * 0.13 * h, -0.36 * h), (sx * 0.11 * h, -0.10 * h), (sx * 0.13 * h, -0.02 * h), (sx * 0.16 * h, 0), (sx * 0.02 * h, 0), (sx * 0.04 * h, -0.10 * h), t=0.3))
        _head(p, hx, hy, hr)
        p.addRect(skia.Rect.MakeLTRB(hx - hr * 0.45, hy + hr, hx + hr * 0.45, -0.745 * h))
        _hat(p, hat, hx, hy, hr)
        if kind == "landsknecht":
            for sx in (-1, 1):
                p.addOval(skia.Rect.MakeLTRB(sx * 0.17 * h - 0.07 * h, -0.70 * h, sx * 0.17 * h + 0.07 * h, -0.52 * h))
        # mızrak / pike / kılıç
        if kind in ("pikeman", "landsknecht", "janissary", "conquistador"):
            x = 0.22 * h
            p.addRect(skia.Rect.MakeLTRB(x - 0.006 * h, -1.65 * h, x + 0.006 * h, 0.0))
            p.addPath(sk.poly_path([(x, -1.74 * h), (x + 0.02 * h, -1.62 * h), (x - 0.02 * h, -1.62 * h)], True))
            p.addPath(_P((0.14 * h, -0.68 * h), (0.24 * h, -0.62 * h), (0.24 * h, -0.55 * h), (0.14 * h, -0.60 * h), t=0.3))
        if kind == "knight":
            x = 0.24 * h
            p.addRect(skia.Rect.MakeLTRB(x - 0.01 * h, -1.5 * h, x + 0.01 * h, -0.2 * h))
            p.addPath(sk.poly_path([(x, -1.62 * h), (x + 0.03 * h, -1.45 * h), (x - 0.03 * h, -1.45 * h)], True))
    elif kind == "seated":                              # tahtta oturan
        p.addPath(_P((-0.17 * h, -0.60 * h), (0.17 * h, -0.60 * h), (0.20 * h, -0.34 * h), (0.34 * h, -0.30 * h), (0.34 * h, -0.20 * h), (-0.22 * h, -0.20 * h), (-0.22 * h, -0.34 * h), t=0.3))
        p.addRect(skia.Rect.MakeLTRB(0.30 * h, -0.30 * h, 0.35 * h, 0.0))
        _head(p, 0, -0.72 * h, hr)
        _hat(p, "crown", 0, -0.72 * h, hr)
    elif kind == "kneel":
        p.addPath(_P((-0.14 * h, -0.55 * h), (0.14 * h, -0.55 * h), (0.16 * h, -0.30 * h), (0.28 * h, -0.20 * h), (0.28 * h, 0), (-0.20 * h, 0), (-0.20 * h, -0.20 * h), (-0.12 * h, -0.30 * h), t=0.3))
        _head(p, 0.02 * h, -0.64 * h, hr)
        _hat(p, "cap", 0.02 * h, -0.64 * h, hr)
    else:
        return _fig_path("noble", hpx, lean)
    return p


@lru_cache(maxsize=1024)
def _fig_sprite(kind, hpx, col, rim, lean):
    """Sıkı kırpılmış sprite (boş alan çizim maliyetidir). Dönüş: (img, ox, oy) — ox,oy = yol orijininin sprite içindeki konumu."""
    hpx = int(hpx)
    xdraw = None
    if kind in FIGX:
        path, xdraw = FIGX[kind](float(hpx), lean)
    else:
        path = _fig_path(kind, hpx, lean)
    b = path.getBounds()
    pad = max(4, int(hpx * 0.03))
    l, t = int(math.floor(b.left())) - pad, int(math.floor(b.top())) - pad
    r, bt = int(math.ceil(b.right())) + pad, int(math.ceil(b.bottom())) + pad
    s = skia.Surface(max(2, r - l), max(2, bt - t))
    c = s.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    c.translate(-l, -t)
    if xdraw is not None:
        xdraw(c, col, rim)
        return s.makeImageSnapshot(), -l, -t
    if rim:
        c.save(); c.translate(-hpx * 0.012, -hpx * 0.010)
        c.drawPath(path, skia.Paint(AntiAlias=True, Color=C(rim)))
        c.restore()
    c.drawPath(path, skia.Paint(AntiAlias=True, Color=C(col)))
    return s.makeImageSnapshot(), -l, -t


def figure(f, kind, x, y, h, col="#0C0705", rim="#B07A3A", face=1, alpha=1.0, sway=0.0, rot=0.0, lean=0.0, blur=0.0, bob=0.0):
    """Siluet figür: y = ayak hizası. face=-1 → ayna."""
    img, ox, oy = _fig_sprite(kind, int(round(h)), col, rim, round(lean, 2))
    f.c.save()
    f.c.translate(x, y + bob)
    if rot or sway:
        f.c.rotate(math.degrees(rot + sway))
    f.c.scale(face, 1)
    p = skia.Paint(AntiAlias=True)
    if alpha < 1:
        p.setAlphaf(alpha)
    if blur > 0:
        p.setImageFilter(skia.ImageFilters.Blur(blur, blur))
    f.c.drawImage(img, -ox, -oy, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    f.c.restore()


def crowd(f, rows, x0, x1, y0, dy, h0, hs, kinds, col="#0C0705", rim="#8A5A2A", seed=1, dens=70, face=1, depth_fog=None):
    """Sıralı kalabalık: rows satır; satır i ayak hizası y0 + i*dy, boy h0*hs**i, aralık dens."""
    rs = np.random.RandomState(seed)
    for r in range(rows):
        y = y0 + r * dy
        h = h0 * (hs ** r)
        n = int((x1 - x0) / (dens * (hs ** r)))
        for k in range(n):
            x = x0 + (k + rs.rand() * 0.8) * (x1 - x0) / max(1, n)
            kind = kinds[rs.randint(len(kinds))]
            cc = col if depth_fog is None else mix(col, depth_fog, 0.5 * (1 - r / max(1, rows - 1)))
            figure(f, kind, x, y + rs.randn() * 3, h * (0.92 + 0.16 * rs.rand()), cc, rim, face=face if rs.rand() > 0.15 else -face, alpha=1.0, lean=(rs.rand() - 0.5) * 0.04)


# ───────────────────────────── deniz & gemi ─────────────────────────────
def sea_layers(f, horizon, colors=("#1B3A4E", "#0B1C28"), t=0.0, amp=18, n=7, storm=0.0, foam=True, seed=1):
    f.rect(-MARGIN, horizon, W + 2 * MARGIN, H + MARGIN - horizon, shader=f.lin(0, horizon, 0, H, [(colors[0], 0.0), (colors[1], 1.0)]))
    rs = np.random.RandomState(seed)
    for i in range(n):
        u = i / max(1, n - 1)
        y = horizon + (H - horizon) * (u ** 1.6) + 8
        a = amp * (0.3 + 1.1 * u) * (1 + storm * 1.6)
        ph = t * (0.9 + 0.6 * u) * (1 + storm) + rs.rand() * 6
        pts = []
        for xx in range(-MARGIN, W + MARGIN + 60, 60):
            pts.append((xx, y + math.sin(xx * 0.0042 * (1 + 0.4 * u) + ph) * a + math.sin(xx * 0.011 + ph * 1.7) * a * 0.35))
        pts += [(W + MARGIN, H + MARGIN), (-MARGIN, H + MARGIN)]
        col = mix(colors[0], colors[1], u * 0.8 + 0.1)
        f.path(sk.poly_path(pts, True), color=col, alpha=0.9)
        f.path(sk.poly_path(pts[:-2], False), style="stroke", sw=2.5 + 3 * u, color=mix(col, "#C8E0EA", 0.35 + 0.25 * storm), alpha=0.55)


def carrack(f, x, y, s=1.0, col="#0C0705", sail="#D8C8A0", rim="#B07A3A", t=0.0, rock=0.0, flag="#8E1F26", pennants=True, lit=True):
    """Kervel/karaka (yandan görünüş): gövde, direkler, kabarık kare yelkenler, flama."""
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(math.degrees(rock))
    f.c.scale(s, s)
    # gövde
    hull = sk.smooth_path([(-210, -60), (-170, 10), (-80, 40), (110, 40), (190, 0), (230, -90), (200, -100), (170, -70), (-150, -70), (-190, -100)], True, 0.3)
    f.path(hull, color=col)
    f.path(sk.smooth_path([(-190, -100), (-150, -70), (170, -70), (200, -100), (230, -90), (210, -50), (-210, -50)], True, 0.2), color=mix(col, "#5C3B22", 0.35))
    f.rect(-225, -150, 70, 62, color=col)       # pruva kasarası
    f.rect(120, -170, 110, 84, color=col)       # kıç kasarası
    # direkler
    for mx, mt in ((-100, 330), (10, 420), (130, 300)):
        f.rect(mx - 5, -mt - 40, 10, mt - 40, color=col)
    # yelkenler: yan rüzgâr kabarması (t ile hafif nefes)
    br = 1.0 + 0.04 * math.sin(t * 1.7)
    def sail_shape(cx_, top, bot, w):
        pts = [(cx_ - w, top), (cx_ + w, top), (cx_ + w * 1.05 * br, (top + bot) * 0.5), (cx_ + w * 0.95, bot), (cx_, bot + 18 * br), (cx_ - w * 0.95, bot), (cx_ - w * 1.05 * br, (top + bot) * 0.5)]
        path = sk.smooth_path(pts, True, 0.35)
        f.path(path, shader=f.lin(cx_ - w, top, cx_ + w, bot, [(mix(sail, "#FFFFFF", 0.15), 0.0), (sail, 0.55), (mix(sail, "#000000", 0.35), 1.0)]))
        f.path(path, style="stroke", sw=2.5, color=mix(sail, "#000000", 0.5), alpha=0.6)
        f.line(cx_ - w * 0.5, top, cx_ - w * 0.45, bot, color="#000000", sw=1.2, alpha=0.18)
        f.line(cx_ + w * 0.5, top, cx_ + w * 0.45, bot, color="#000000", sw=1.2, alpha=0.18)
    sail_shape(10, -400, -170, 130)
    sail_shape(10, -460, -400, 82)
    sail_shape(-100, -330, -170, 92)
    sail_shape(130, -300, -176, 74)
    # kızıl haç/arma sembolü
    f.line(10, -380, 10, -200, color=flag, sw=22, alpha=0.9)
    f.line(-70, -300, 90, -300, color=flag, sw=22, alpha=0.9)
    if pennants:
        for mx, mt in ((10, 470), (-100, 372), (130, 342)):
            wv = math.sin(t * 5 + mx) * 6
            f.path(sk.smooth_path([(mx, -mt), (mx + 62, -mt + 8 + wv), (mx + 110, -mt + 4 + wv * 1.4), (mx + 62, -mt + 22), (mx, -mt + 24)], True, 0.3), color=flag)
    f.c.restore()


# ───────────────────────────── genel arka planlar ─────────────────────────────
def sky_gradient(f, top, bottom, y1=H, y0=-MARGIN):
    f.rect(-MARGIN, y0, W + 2 * MARGIN, y1 - y0 + MARGIN, shader=f.lin(0, y0, 0, y1, [(top, 0.0), (bottom, 1.0)]))


def hills(f, y, amp, col, seed=1, step=80, wavelength=0.004, edge=None):
    rs = np.random.RandomState(seed)
    ph = rs.rand() * 6
    pts = [(xx, y + math.sin(xx * wavelength + ph) * amp + math.sin(xx * wavelength * 2.7 + ph * 2) * amp * 0.4) for xx in range(-MARGIN, W + MARGIN + step, step)]
    pts += [(W + MARGIN, H + MARGIN), (-MARGIN, H + MARGIN)]
    f.path(sk.poly_path(pts, True), color=col)
    if edge:
        f.path(sk.poly_path(pts[:-2], False), style="stroke", sw=2, color=edge, alpha=0.5)


def skyline(f, y, kinds, x0, x1, h0, col, seed=1, win=None, gap=(60, 130)):
    """Şehir silueti: kuleler, kubbeler, minareler, kilise kuleleri."""
    rs = np.random.RandomState(seed)
    x = x0
    while x < x1:
        k = kinds[rs.randint(len(kinds))]
        w = 50 + rs.rand() * 90
        h = h0 * (0.5 + rs.rand() * 0.9)
        if k == "tower":
            f.rect(x, y - h, w, h, color=col)
            for q in range(4):
                f.rect(x + q * w / 4, y - h - 14, w / 7, 16, color=col)
        elif k == "spire":
            f.rect(x, y - h * 0.7, w * 0.7, h * 0.7, color=col)
            f.poly([(x - 4, y - h * 0.7), (x + w * 0.35, y - h * 1.5), (x + w * 0.7 + 4, y - h * 0.7)], color=col)
        elif k == "dome":
            f.rect(x, y - h * 0.55, w, h * 0.55, color=col)
            f.oval(x + w / 2, y - h * 0.55, w * 0.5, w * 0.42, color=col)
            f.rect(x + w / 2 - 2, y - h * 0.55 - w * 0.42 - 26, 4, 28, color=col)
        elif k == "minaret":
            f.rect(x + w * 0.35, y - h * 1.5, w * 0.12, h * 1.5, color=col)
            f.poly([(x + w * 0.31, y - h * 1.5), (x + w * 0.41, y - h * 1.8), (x + w * 0.51, y - h * 1.5)], color=col)
            f.rect(x + w * 0.28, y - h * 1.1, w * 0.26, 8, color=col)
        else:
            f.rect(x, y - h * 0.6, w, h * 0.6, color=col)
            f.poly([(x - 6, y - h * 0.6), (x + w / 2, y - h * 0.95), (x + w + 6, y - h * 0.6)], color=col)
        if win:
            for q in range(int(h / 40)):
                if rs.rand() > 0.55:
                    f.rect(x + w * 0.3 + rs.rand() * w * 0.3, y - h * 0.5 + q * 34, 6, 10, color=win, alpha=0.8)
        x += w + gap[0] + rs.rand() * (gap[1] - gap[0])


def pines(f, x0, x1, y, h, col, seed=1, dens=70):
    rs = np.random.RandomState(seed)
    x = x0
    while x < x1:
        hh = h * (0.6 + rs.rand() * 0.8)
        w = hh * 0.34
        for q in range(4):
            f.poly([(x - w * (1 - q * 0.18), y - hh * q * 0.22), (x, y - hh * (q * 0.22 + 0.4)), (x + w * (1 - q * 0.18), y - hh * q * 0.22)], color=col)
        f.rect(x - 3, y, 6, 14, color=col)
        x += dens * (0.5 + rs.rand())


for _m in ("figs_lab", "figs_war"):          # figür-lab / sahne-lab modülleri (varsa)
    sk.optional_import(_m)
