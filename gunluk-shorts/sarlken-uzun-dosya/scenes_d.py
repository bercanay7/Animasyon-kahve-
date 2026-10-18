"""Bölüm yazarı D (c0/c12) ortak diorama parçaları:
* `d_pair`      : kolunu genç prensin omzuna dayamış yaşlı imparator — BASTONSUZ (kaynak kapısı: baston kaynaksız). figs_lab bileşenlerinden kurulur.
* `d_hall_gold` : c12'nin "ağır altın ışık" salonu = aynı `hall` + uzun güneş huzmeleri + sıcak zemin yansıması (c0'ın aynası).
* `pair_walker` / `follow_cam` yardımcıları.
Ortak dosyalara dokunmaz; yalnız kanca (ST.figx, SL.sc) kullanır."""
import math

import numpy as np
import skia

import d_common as D
import figs_lab as FL
import scenes_lib as SL
import shots as SH
import sk
import stage as ST
from sk import H, W, clamp, ease_io, lerp, smooth
from stage import MARGIN


# ───────────────────────────── bastonsuz çift figür ─────────────────────────────
def _pair_nocane(h, lean):
    F = FL.Fig(h, lean)
    es = 0.955
    ex = -0.215 * h
    px = 0.225 * h
    F.merge(FL.emperor_fig(h * es, 0, cane=False), dx=ex)
    F.merge(FL.prince_fig(h, 0, sword=True, hat="beret"), dx=px)
    sx, sy = ex + 0.045 * h, -0.70 * h * es
    tx, ty = px - 0.045 * h, -0.752 * h
    F.fill(FL.limb([(sx, sy), (sx + (tx - sx) * 0.50, sy + 0.075 * h), (tx - 0.030 * h, ty + 0.045 * h)], [0.074 * h, 0.07 * h, 0.046 * h], cap0=0.5, cap1=0.2), rim=1.0)
    F.crease((sx + 0.02 * h, sy - 0.005 * h), (sx + (tx - sx) * 0.55, sy + 0.06 * h), 0.006 * h, 0.006 * h)
    F.fill(FL.K.hand_pt("open", tx - 0.032 * h, ty + 0.05 * h, 0.088 * h, -22), rim=1.0)
    F.fill(FL.K.hand_pt("thumb", tx - 0.032 * h, ty + 0.05 * h, 0.088 * h, -22), rim=1.0)
    return F.build()


ST.figx("d_pair")(_pair_nocane)


def draw_pair(f, x, y, h, t=0.0, walk=False, face=1, alpha=1.0, col="#0A0604", rim="#C58A44", blur=0.0):
    """d_pair figürünü çizer; walk=True → yürüme salınımı (hafif sağ-sol + zıplama)."""
    sway = math.sin(t * 1.7) * 0.010 if walk else math.sin(t * 0.8) * 0.003
    bob = -abs(math.sin(t * 1.7)) * 5.0 * (h / 520.0) if walk else 0.0
    ST.figure(f, "d_pair", x, y + bob, h, col=col, rim=rim, face=face, alpha=alpha, sway=sway, blur=blur)


def lead_figure(f, kind, x, y, h, t=0.0, walk=True, face=1, alpha=1.0, col="#0A0604", rim="#C58A44"):
    sway = math.sin(t * 1.9 + x * 0.01) * 0.008 if walk else 0.0
    bob = -abs(math.sin(t * 1.9 + x * 0.01)) * 4.0 * (h / 520.0) if walk else 0.0
    ST.figure(f, kind, x, y + bob, h, col=col, rim=rim, face=face, alpha=alpha, sway=sway)


# ───────────────────────────── kamera / ekran dönüşümü ─────────────────────────────
def cam_at(t, keys):
    """keys: [(yerel_sn, (x,y,zoom))] → (x,y,z) yumuşak (SL._cam_at ile aynı eğri)."""
    if t <= keys[0][0]:
        return keys[0][1]
    if t >= keys[-1][0]:
        return keys[-1][1]
    for (ta, va), (tb, vb) in zip(keys[:-1], keys[1:]):
        if ta <= t <= tb:
            u = ease_io((t - ta) / max(1e-6, tb - ta), 2)
            return (lerp(va[0], vb[0], u), lerp(va[1], vb[1], u), math.exp(lerp(math.log(va[2]), math.log(vb[2]), u)))
    return keys[-1][1]


def scene_to_screen(x, y, cam, depth=1.0):
    """Sahne tuvali (x,y) → ekran px (derinlik d katmanı). cam=(x,y,zoom)."""
    cx_, cy_, z = cam
    s = 1 + (z - 1) * depth
    sx = W / 2 + (x - W / 2 - (cx_ - W / 2) * depth - 0) * s
    sy = H / 2 + (y - H / 2 - (cy_ - H / 2) * depth) * s
    return sx, sy


def keys_local(tl_keys, start_anchor):
    """[(çapa, değer)] → [(yerel_sn, değer)]; start_anchor: çekimin başlangıç çapası."""
    tl = SH.timeline()
    t0 = tl.resolve(start_anchor)
    return [((tl.resolve(a) - t0) if not isinstance(a, (int, float)) else float(a), v) for a, v in tl_keys]


def local_time(anchor, start_anchor):
    tl = SH.timeline()
    return tl.resolve(anchor) - tl.resolve(start_anchor)


# ───────────────────────────── c12 salonu: ağır altın ışık ─────────────────────────────
@SL.sc("d_hall_gold")
class HallGold(SL.Hall):
    """`hall` + uzun alçak-güneş huzmeleri ve zeminde sıcak yansıma. p: hall ile aynı (glow0/glow1 pencere rengi...)."""

    def layers(self):
        base = list(super().layers())

        def Lbeam(f):
            ST.god_rays(f, (W / 2, 330), math.radians(90), 1.25, 1150, n=10, alpha=0.17, color="#FFC46E", seed=5, blur=26)
            ST.god_rays(f, (W / 2 - 40, 330), math.radians(78), 0.9, 1250, n=6, alpha=0.12, color="#FFB555", seed=9, blur=30)
            f.path(sk.poly_path([(W / 2 - 150, 700), (W / 2 + 150, 700), (W / 2 + 600, 1090), (W / 2 - 600, 1090)], True),
                   shader=f.lin(0, 700, 0, 1090, [("#FFD58A", 0.0, 95), ("#FFB04A", 1.0, 20)]), blend=skia.BlendMode.kPlus)
            f.circle(W / 2, 760, 460, shader=f.rad(W / 2, 760, 460, [("#FFD58A", 0.0, 70), ("#FFD58A", 1.0, 0)]), blend=skia.BlendMode.kPlus)

        base.insert(4, (0.9, Lbeam))
        return base

    def dyn(self):
        d = super().dyn()
        return {k + 1: v for k, v in d.items()}
