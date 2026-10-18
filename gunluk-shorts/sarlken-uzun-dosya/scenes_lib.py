"""Diorama sahne kitaplığı: her sahne = (katman listesi üretici, dinamik öğe fonksiyonu).
`theatre` çekim şablonu (aşağıda) sahneyi adıyla çağırır:  shot("theatre", a=..., scene="hall", cams=[(0,(960,540,1.0)),(8,(980,600,1.4))], p=dict(...))
Yeni sahne: @sc("ad") ile  build(p) -> [(depth, fn(f))]  ve isteğe bağlı  dyn(p) -> {katman_idx: fn(f,t)}  tanımla.
"""
import math

import numpy as np
import skia

import shots as SH
import sk
import stage as ST
from sk import C, H, W, clamp, ease_io, lerp, mix, smooth
from stage import MARGIN, SCam

SCENES = {}


def sc(name):
    def deco(cls):
        SCENES[name] = cls
        return cls
    return deco


# ───────────────────────────── SALON ─────────────────────────────
@sc("hall")
class Hall:
    """Gotik saray salonu: merkezde koridor, iki yanda kemerli sütunlar, ardında tahtlı sahne, yanlarda kalabalık.
    p: dict(crowd=True, banners=("crimson"), emperor=True, throne=True, warm=1.0, window_glow=...)"""

    def __init__(self, p):
        self.p = p
        self.warm = p.get("warm", 1.0)

    def layers(self):
        p = self.p
        stone = "#4A3220"
        fogc = "#2A170C"

        def L0(f):         # uzak duvar + büyük arka pencere
            f.rect(-MARGIN, -MARGIN, W + 2 * MARGIN, H + 2 * MARGIN, color="#150C07")
            sk.background(f, "night") if False else None
            f.rect(-MARGIN, -MARGIN, W + 2 * MARGIN, 700 + MARGIN, shader=f.lin(0, -MARGIN, 0, 700, [("#1B0F08", 0.0), ("#3A2312", 1.0)]))
            # arka duvarın taş blokları
            for r in range(10):
                yy = -60 + r * 76
                f.line(-MARGIN, yy, W + MARGIN, yy, color="#000000", sw=1.6, alpha=0.20)
            ST.gothic_window(f, W / 2, 330, 330, 520, glow=(p.get("glow0", "#FFEFC2"), p.get("glow1", "#E7992F")), stone="#2B190C", edge="#8A6338", k=1.0)
            f.circle(W / 2, 330, 520, shader=f.rad(W / 2, 330, 520, [("#FFE8B0", 0.0, 120), ("#FFB347", 0.4, 50), ("#FFB347", 1.0, 0)]), blend=skia.BlendMode.kPlus)

        def L1(f):         # arka duvar önü: tahtlı sahne, yan pencereler, sancaklar
            for sx in (-1, 1):
                ST.gothic_window(f, W / 2 + sx * 560, 340, 170, 380, glow=("#FFE3A0", "#D9822A"), stone="#2B190C")
                ST.banner(f, W / 2 + sx * 360, -40, 120, 380, color="#7B1B22", icon="eagle", wave=sx * 2)
                ST.banner(f, W / 2 + sx * 760, -40, 120, 340, color="#6B1D24", icon="castle")
            ST.floor_hall(f, 640, 700, "#1F130B", "#2C1B10", tile=False)
            if p.get("throne", True):
                ST.dais(f, W / 2, 700, 420, 66, steps=3)
                ST.throne(f, W / 2, 640, 0.9, c="#6A1E26")
            for sx in (-1, 1):
                for k in range(3):
                    ST.column(f, W / 2 + sx * (330 + k * 150), 200 - k * 10, 660, 48 - k * 4, stone="#3A2415")

        def L2(f):         # orta plan: kemerli yan galeriler
            for sx in (-1, 1):
                for k, (xx, w, hh) in enumerate([(400, 260, 600), (200, 250, 740)]):
                    ST.arch(f, W / 2 + sx * (xx + 150) * 1.0, 800 - k * 20, w, hh, stone="#3E2818", edge="#8A6338", glow=("#1A0F08", "#2A170C"))
            for sx in (-1, 1):
                for xx in (230, 470, 700):
                    ST.column(f, W / 2 + sx * xx, 160, 760, 64, stone="#4A3220")
            # ışık huzmeleri: statik, katmanla birlikte pişer (dinamik çizmek ~150 ms/kare)
            ST.god_rays(f, (W / 2 - 360, 120), math.radians(70), 0.8, 1300, n=7, alpha=0.11)
            ST.god_rays(f, (W / 2 + 360, 120), math.radians(110), 0.8, 1300, n=7, alpha=0.11)

        def L3(f):         # zemin (kemerlerin önünde)
            ST.floor_hall(f, 700, 1080, "#241509", "#4A2F18", vp_x=W / 2, sheen=("#FFD58A", 0.16))
            # ortada ışık şeridi (halı)
            f.path(sk.poly_path([(W / 2 - 70, 700), (W / 2 + 70, 700), (W / 2 + 420, 1090), (W / 2 - 420, 1090)], True), shader=f.lin(0, 700, 0, 1090, [("#5A141A", 0.0, 220), ("#8B1E27", 1.0, 235)]))
            f.path(sk.poly_path([(W / 2 - 70, 700), (W / 2 - 58, 700), (W / 2 - 360, 1090), (W / 2 - 420, 1090)], True), color="#C9962B", alpha=0.7)
            f.path(sk.poly_path([(W / 2 + 58, 700), (W / 2 + 70, 700), (W / 2 + 420, 1090), (W / 2 + 360, 1090)], True), color="#C9962B", alpha=0.7)

        def L4(f):         # yan kalabalık (iki taraf)
            if p.get("crowd", True):
                for sx, (x0, x1) in ((-1, (-60, 700)), (1, (1220, 1980))):
                    ST.crowd(f, 3, x0, x1, 780, 70, 360, 1.14, ["noble", "noble", "merchant", "pikeman", "cardinal", "scribe", "woman"], seed=7 if sx < 0 else 11, dens=84, face=1 if sx < 0 else -1, depth_fog="#2A170C")

        def L5(f):         # yakın plan: karanlık sütunlar
            for sx in (-1, 1):
                ST.column(f, W / 2 + sx * 880, -60, 1180, 140, stone="#1B0F08", edge="#5A3C1E")
            f.rect(-MARGIN, -MARGIN, W + 2 * MARGIN, 120, color="#0D0704", alpha=0.85)

        return [(0.05, L0), (0.35, L1), (0.62, L2), (0.8, L3), (1.0, L4), (1.35, L5)]

    def dyn(self):
        p = self.p
        rs_t = {}

        def D4(f, t):   # figürler + şamdan alevleri
            for (cx_, cy_, r) in ((W / 2 - 300, 120, 90), (W / 2 + 300, 120, 90), (W / 2, 200, 120)):
                ST.chandelier(f, cx_, cy_, r)
                ST.candle_flames(f, cx_, cy_, r, t, seed=int(cx_))
            if p.get("emperor", True):
                ex, ey = p.get("emp_xy", (W / 2 + 40, 985))
                walk = p.get("walk", 0.0) * 40
                sw = math.sin(t * 1.6) * 0.012
                ST.figure(f, "pair_old_prince", ex + walk, ey, p.get("emp_h", 520), col="#0A0604", rim="#C58A44", face=1, sway=sw, bob=abs(math.sin(t * 1.6)) * -4 * (1 if p.get("walk", 0) else 0))
            if p.get("extra"):
                p["extra"](f, t)

        return {4: D4}


# ───────────────────────────── çekim şablonu ─────────────────────────────
def _cam_at(cx, cams):
    ks = [(cx.at(a), v) for a, v in cams]
    if cx.t <= ks[0][0]:
        return SCam(*ks[0][1])
    if cx.t >= ks[-1][0]:
        return SCam(*ks[-1][1])
    for (ta, va), (tb, vb) in zip(ks[:-1], ks[1:]):
        if ta <= cx.t <= tb:
            u = ease_io((cx.t - ta) / max(1e-6, tb - ta), 2)
            return SCam(lerp(va[0], vb[0], u), lerp(va[1], vb[1], u), math.exp(lerp(math.log(va[2]), math.log(vb[2]), u)))
    return SCam(*ks[-1][1])


@SH.kind("theatre")
def k_theatre(cx, scene="hall", cams=((0.0, (960, 540, 1.0)),), p=None, vig=0.6, rays=0.0, dust_n=70, overlay=None, fade_in=0.0, tint=None):
    p = p or {}
    f = cx.f
    S = SCENES[scene](p)
    key = scene + repr(sorted((k, v) for k, v in p.items() if isinstance(v, (str, int, float, bool, tuple))))
    sc_ = ST.scene(key, S.layers)
    cam = _cam_at(cx, cams)
    ST.draw(f, sc_, cam, t=cx.t, dyn=S.dyn())
    if dust_n:
        sk.dust(f, cx.t, n=dust_n, alpha=0.45)
    if overlay:
        overlay(cx)
    if tint:
        f.rect(0, 0, W, H, color=tint[0], alpha=tint[1])
    f.vig(vig)
    if fade_in:
        f.rect(0, 0, W, H, color="#000000", alpha=1 - smooth(cx.t / fade_in))
