"""figs_lab — Şarlken figür-lab: kâğıt-kesim / gölge-tiyatrosu siluet figürleri (zengin figx).

Kayıt: stage.figx(ad) → fn(h, lean) -> (sınır_yolu, çiz(canvas, col, rim)). Tür adları STIL_REHBERI.md bölüm 6 ile aynıdır.
Tüm figürler SAĞA bakar (face=+1); face=-1 ayna. Ayak (0,0), yukarı −y, h ≈ boy (şapka/tüy ile ≈1.0–1.1 h; mızrak vb. daha yüksek olabilir).
Araç takımı: figs_kit (geometri, Fig), figs_parts (şapka/baş/kol/cüppe). Savaş/atlı/yerli figürleri: figs_war.py, ek türler: figs_more.py.
"""
import math

import skia

import sk
import stage as ST
import figs_kit as K
from figs_parts import ruff as _ruff
from figs_kit import K as KC, Fig, bar, ell, feather_path, lens, limb, place, poly, shoe, sp
from figs_parts import add_arm, add_hat, add_head, add_leg, fur_band, hair_path, hem_band, hem_slits, robe_folds, robe_path, ruff


def fx(name):
    return ST.figx(name)


# ───────────────────────────── noble (orta boy, dişli etekli, kürk klapalı; belde el) ─────────────────────────────
@fx("noble")
def _noble(h, lean):
    F = Fig(h, lean)
    hh = 0.135 * h
    hx, hy = 0.035 * h, -0.93 * h + 0.5 * hh
    # uzak kol (cüppenin arkasında; eldiven tutar)
    add_arm(F, [(0.06 * h, -0.73 * h), (0.118 * h, -0.62 * h), (0.14 * h, -0.505 * h)], [0.056 * h, 0.052 * h, 0.034 * h], hand="open", hand_len=0.082 * h, hand_rot=95)
    # çorap bacaklar + kare burun ayakkabı
    add_leg(F, h, (-0.035, -0.34), (-0.065, -0.19), (-0.10, -0.046), (0.074, 0.05, 0.032), 1, "square", 0.10, 0.7)
    add_leg(F, h, (0.04, -0.34), (0.085, -0.19), (0.125, -0.046), (0.08, 0.052, 0.034), 1, "square", 0.105, 0.9)
    # dizüstü cüppe, dişli (dagged) etek
    F.fill(robe_path(h, sh_y=-0.745, nb_y=-0.768, back_sh=-0.115, front_sh=0.105, chest=(-0.122, 0.108, -0.65), waist=(-0.10, 0.097, -0.50),
                     hip=(-0.158, 0.162, -0.39), hem=(-0.222, 0.222, -0.265), nfold=3, dag=0.024, wave_b=0.008, wave_f=0.008, swing=0.01), rim=0.9, glow=0.10)
    robe_folds(F, h, -0.07, 0.075, -0.50, -0.30, 7, 0.011, bend=0.010, seed=3)
    hem_band(F, h, -0.17, 0.18, -0.305, n=9, size=0.0085, alpha=0.42)
    # kürk yaka + klapalar
    F.fill(fur_band([(-0.116 * h, -0.716 * h), (-0.10 * h, -0.757 * h), (-0.04 * h, -0.78 * h), (0.05 * h, -0.78 * h), (0.10 * h, -0.757 * h), (0.11 * h, -0.716 * h)], 0.05 * h, 0.02 * h, side=1), rim=1.0)
    F.fill(fur_band([(0.065 * h, -0.765 * h), (0.098 * h, -0.70 * h), (0.108 * h, -0.60 * h), (0.10 * h, -0.45 * h), (0.118 * h, -0.34 * h)], 0.044 * h, 0.018 * h, side=-1), rim=1.0)
    F.fill(fur_band([(-0.05 * h, -0.77 * h), (-0.105 * h, -0.725 * h), (-0.128 * h, -0.64 * h)], 0.044 * h, 0.018 * h, side=1), rim=0.8)
    F.line(sp([(-0.095 * h, -0.62 * h), (0.0, -0.565 * h), (0.095 * h, -0.60 * h)], False), h * 0.004, tone=1.0, alpha=0.75)
    F.fill(ell(0.0, -0.563 * h, 0.011 * h, 0.011 * h), rim=0.0, tone=1.0, alpha=0.8, bound=False)
    # yakın kol: omuzda kabarık, dirsekte daralan, belde el
    F.fill(ell(-0.06 * h, -0.725 * h, 0.055 * h, 0.036 * h, -28), rim=1.0)
    add_arm(F, [(-0.04 * h, -0.725 * h), (-0.132 * h, -0.612 * h), (-0.045 * h, -0.508 * h)], [0.064 * h, 0.07 * h, 0.044 * h], hand="open", hand_len=0.088 * h, hand_rot=8)
    F.crease((-0.085 * h, -0.70 * h), (-0.132 * h, -0.60 * h), 0.006 * h, 0.01 * h)
    F.crease((-0.06 * h, -0.69 * h), (-0.105 * h, -0.56 * h), 0.006 * h, -0.006 * h)
    add_head(F, hx, hy, hh, "m", rot=-3, beard="point", hat="beret", neck_to=(0.0, -0.77 * h), hat_rot=8)
    return F.build()


# ───────────────────────────── merchant ─────────────────────────────
@fx("merchant")
def _merchant(h, lean):
    F = Fig(h, lean)
    hh = 0.135 * h
    hx, hy = 0.05 * h, -0.925 * h + 0.5 * hh
    F.fill(robe_path(h, sh_y=-0.74, nb_y=-0.762, back_sh=-0.112, front_sh=0.108, chest=(-0.124, 0.122, -0.64), waist=(-0.108, 0.11, -0.50), belly=0.022,
                     hip=(-0.15, 0.158, -0.30), hem=(-0.198, 0.195, -0.012), nfold=3, amp=0.006, lift=0.03, wave_b=0.006, wave_f=0.008), rim=0.9, glow=0.10)
    F.fill(shoe(0.125 * h, 0, 0.095 * h, 0.032 * h, 1, "square"), rim=0.8)
    robe_folds(F, h, -0.06, 0.07, -0.50, -0.03, 5, 0.010, bend=0.008, seed=5)
    hem_slits(F, h, [-0.14, -0.04, 0.07, 0.16], -0.008, depth=0.06)
    F.fill(fur_band([(-0.112 * h, -0.715 * h), (-0.095 * h, -0.752 * h), (-0.04 * h, -0.772 * h), (0.05 * h, -0.772 * h), (0.098 * h, -0.752 * h), (0.108 * h, -0.715 * h)], 0.036 * h, 0.013 * h, side=1), rim=1.0)
    F.fill(fur_band([(0.06 * h, -0.76 * h), (0.10 * h, -0.70 * h), (0.118 * h, -0.60 * h), (0.118 * h, -0.45 * h)], 0.03 * h, 0.012 * h, side=-1), rim=1.0)
    F.fill(poly([(-0.105 * h, -0.515 * h), (0.118 * h, -0.515 * h), (0.118 * h, -0.49 * h), (-0.105 * h, -0.49 * h)]), rim=0.5, tone=0.18, bound=False)
    F.fill(ell(0.0, -0.502 * h, 0.012 * h, 0.012 * h), rim=0.0, tone=1.0, alpha=0.7, bound=False)
    F.line(sp([(0.04 * h, -0.50 * h), (0.07 * h, -0.45 * h)], False), h * 0.004, tone=0.35, alpha=0.7)
    F.fill(sp([(0.052 * h, -0.455 * h), (0.095 * h, -0.45 * h), (0.105 * h, -0.405 * h), (0.075 * h, -0.375 * h), (0.045 * h, -0.40 * h)], True), rim=0.9)
    F.line(poly([(0.06 * h, -0.45 * h), (0.092 * h, -0.45 * h)], False), h * 0.004, tone=1.0, alpha=0.5)
    F.fill(poly([(0.045 * h, -0.655 * h), (0.145 * h, -0.64 * h), (0.14 * h, -0.555 * h), (0.04 * h, -0.57 * h)]), rim=0.9)
    F.line(sp([(0.052 * h, -0.567 * h), (0.136 * h, -0.553 * h)], False), h * 0.004, tone=1.0, alpha=0.55)
    add_arm(F, [(-0.03 * h, -0.725 * h), (-0.085 * h, -0.62 * h), (0.045 * h, -0.585 * h)], [0.064 * h, 0.07 * h, 0.044 * h], hand="open", hand_len=0.082 * h, hand_rot=-8)
    F.crease((-0.05 * h, -0.70 * h), (-0.07 * h, -0.62 * h), 0.006 * h, 0.006 * h)
    add_head(F, hx, hy, hh, "m", rot=2, beard=None, hat="flatcap", nose=1.12, chin=0.02, neck_to=(0.0, -0.762 * h), hat_rot=3)
    return F.build()


# ───────────────────────────── cardinal ─────────────────────────────
@fx("cardinal")
def _cardinal(h, lean):
    F = Fig(h, lean)
    hh = 0.135 * h
    hx, hy = 0.04 * h, -0.915 * h + 0.5 * hh
    F.fill(robe_path(h, sh_y=-0.745, nb_y=-0.768, back_sh=-0.12, front_sh=0.112, chest=(-0.13, 0.115, -0.64), waist=(-0.108, 0.10, -0.50),
                     hip=(-0.17, 0.155, -0.30), hem=(-0.31, 0.215, -0.01), nfold=4, amp=0.009, lift=0.03, swing=-0.02, wave_b=0.016, wave_f=0.008), rim=0.9, glow=0.10)
    F.fill(shoe(0.125 * h, 0, 0.09 * h, 0.03 * h, 1, "round"), rim=0.7)
    robe_folds(F, h, -0.07, 0.06, -0.50, -0.03, 8, 0.011, bend=0.010, seed=8)
    hem_slits(F, h, [-0.24, -0.15, -0.06, 0.03, 0.12, 0.18], -0.008, depth=0.08)
    hem_band(F, h, -0.22, 0.17, -0.045, n=11, size=0.009, alpha=0.38, lift=0.02)
    F.fill(bar(0.045 * h, -0.545 * h, 0.205 * h, -0.64 * h, 0.022 * h, 0.022 * h, True, True), rim=1.0)
    F.line(poly([(0.19 * h, -0.64 * h), (0.205 * h, -0.633 * h)], False), h * 0.003, tone=1.0, alpha=0.5)
    add_arm(F, [(0.02 * h, -0.72 * h), (-0.03 * h, -0.60 * h), (0.075 * h, -0.55 * h)], [0.062 * h, 0.064 * h, 0.044 * h], hand="fist", hand_len=0.072 * h, hand_rot=-15)
    # mozzetta (kısa pelerin) kıvrık kenarlı
    F.fill(sp([KC(-0.045 * h, -0.775 * h), (-0.115 * h, -0.752 * h), (-0.158 * h, -0.68 * h), (-0.162 * h, -0.60 * h), (-0.10 * h, -0.575 * h), (-0.04 * h, -0.585 * h), (0.02 * h, -0.575 * h),
               (0.085 * h, -0.59 * h), (0.14 * h, -0.60 * h), (0.145 * h, -0.68 * h), (0.11 * h, -0.752 * h), KC(0.05 * h, -0.775 * h), (0.0 * h, -0.70 * h)], True, 0.95), rim=1.0, glow=0.08)
    for x in (-0.12, -0.075, -0.03, 0.02, 0.07, 0.115):
        F.crease((x * h, -0.745 * h), ((x - 0.01) * h, -0.60 * h), 0.006 * h, 0.004 * h, alpha=0.55)
    F.line(poly([(0.015 * h, -0.765 * h), (0.02 * h, -0.60 * h)], False), h * 0.004, tone=1.0, alpha=0.5)
    for yy in (-0.74, -0.70, -0.66, -0.62):
        F.fill(ell(0.017 * h, yy * h, 0.0042 * h, 0.0042 * h), rim=0.0, tone=1.0, alpha=0.7, bound=False)
    F.fill(poly([(-0.045 * h, -0.778 * h), (0.055 * h, -0.778 * h), (0.05 * h, -0.752 * h), (-0.04 * h, -0.752 * h)]), rim=0.7, tone=0.1)
    add_head(F, hx, hy, hh, "o", rot=-2, beard=None, hat="galero", nose=1.15, chin=0.025, neck_to=(0.0, -0.768 * h), hat_rot=0)
    for (x0, sx_) in ((-0.12, -1), (0.20, 1)):
        F.line(sp([(x0 * h, -0.862 * h), ((x0 + 0.012 * sx_) * h, -0.78 * h), ((x0 + 0.018 * sx_) * h, -0.70 * h)], False), h * 0.004, tone=0.8, alpha=0.9)
        cx_, cy_ = (x0 + 0.018 * sx_) * h, -0.69 * h
        for row, cnt in enumerate((1, 2, 3)):
            for k in range(cnt):
                F.fill(ell(cx_ + (k - (cnt - 1) / 2) * 0.016 * h, cy_ + row * 0.026 * h, 0.0085 * h, 0.017 * h), rim=0.8)
    return F.build()


# ───────────────────────────── scribe (baldır boyu gömlek, çorap bacaklar) ─────────────────────────────
@fx("scribe")
def _scribe(h, lean):
    F = Fig(h, lean)
    hh = 0.135 * h
    hx, hy = 0.075 * h, -0.905 * h + 0.5 * hh
    add_leg(F, h, (-0.03, -0.27), (-0.055, -0.15), (-0.085, -0.046), (0.07, 0.046, 0.03), 1, "round", 0.09, 0.7, calf=0.004)
    add_leg(F, h, (0.025, -0.27), (0.055, -0.15), (0.095, -0.046), (0.074, 0.048, 0.032), 1, "round", 0.095, 0.9, calf=0.004)
    F.fill(robe_path(h, sh_y=-0.725, nb_y=-0.75, back_sh=-0.115, front_sh=0.098, chest=(-0.138, 0.105, -0.64), waist=(-0.112, 0.092, -0.50),
                     hip=(-0.135, 0.13, -0.34), hem=(-0.175, 0.17, -0.19), nfold=3, amp=0.007, lift=0.015, wave_b=0.005, wave_f=0.006), rim=0.9, glow=0.08)
    robe_folds(F, h, -0.05, 0.05, -0.50, -0.20, 5, 0.009, bend=0.008, seed=11)
    hem_slits(F, h, [-0.12, -0.03, 0.06, 0.13], -0.19, depth=0.05)
    F.fill(bar(0.02 * h, -0.52 * h, 0.05 * h, -0.43 * h, 0.012 * h, 0.012 * h, True, True), rim=0.8)
    F.fill(ell(-0.04 * h, -0.465 * h, 0.012 * h, 0.017 * h), rim=0.8)
    F.fill(poly([(0.03 * h, -0.60 * h), (0.158 * h, -0.655 * h), (0.172 * h, -0.62 * h), (0.045 * h, -0.565 * h)]), rim=1.0)
    F.line(sp([(0.052 * h, -0.576 * h), (0.166 * h, -0.628 * h)], False), h * 0.004, tone=1.0, alpha=0.55)
    add_arm(F, [(-0.025 * h, -0.715 * h), (-0.085 * h, -0.605 * h), (0.09 * h, -0.60 * h)], [0.058 * h, 0.066 * h, 0.042 * h], hand="open", hand_len=0.078 * h, hand_rot=-14)
    F.fill(feather_path(0.15 * h, -0.62 * h, 0.255 * h, -0.755 * h, 0.032 * h, bend=-0.02 * h), rim=1.0)
    F.fill(bar(0.145 * h, -0.617 * h, 0.17 * h, -0.642 * h, 0.004 * h, 0.003 * h), rim=0.8)
    add_head(F, hx, hy, hh, "m", rot=10, beard=None, hat="scholar", nose=1.1, chin=0.0, neck_to=(0.005 * h, -0.75 * h), hat_rot=8, hair="bob")
    return F.build()


# ───────────────────────────── monk ─────────────────────────────
@fx("monk")
def _monk(h, lean):
    F = Fig(h, lean)
    hh = 0.135 * h
    hx, hy = 0.06 * h, -0.90 * h + 0.5 * hh
    F.fill(robe_path(h, sh_y=-0.74, nb_y=-0.765, back_sh=-0.125, front_sh=0.108, chest=(-0.135, 0.118, -0.64), waist=(-0.115, 0.11, -0.50),
                     hip=(-0.17, 0.165, -0.30), hem=(-0.225, 0.215, -0.012), nfold=4, amp=0.008, lift=0.035, wave_b=0.010, wave_f=0.008, swing=0.01), rim=0.9, glow=0.09)
    F.fill(shoe(0.125 * h, 0, 0.09 * h, 0.026 * h, 1, "round"), rim=0.8)
    robe_folds(F, h, -0.06, 0.07, -0.50, -0.03, 8, 0.011, bend=0.010, seed=21)
    hem_slits(F, h, [-0.17, -0.09, -0.01, 0.08, 0.16], -0.008, depth=0.07)
    F.fill(poly([(-0.115 * h, -0.52 * h), (0.118 * h, -0.52 * h), (0.118 * h, -0.50 * h), (-0.115 * h, -0.50 * h)]), rim=0.5, tone=0.2, bound=False)
    F.line(sp([(0.06 * h, -0.51 * h), (0.075 * h, -0.42 * h), (0.07 * h, -0.30 * h)], False), h * 0.0055, tone=0.5, alpha=0.85)
    F.line(sp([(0.075 * h, -0.51 * h), (0.095 * h, -0.40 * h), (0.098 * h, -0.28 * h)], False), h * 0.0055, tone=0.5, alpha=0.85)
    for (x, y) in ((0.072, -0.40), (0.07, -0.33), (0.097, -0.34), (0.098, -0.29)):
        F.fill(ell(x * h, y * h, 0.007 * h, 0.007 * h), rim=0.6, bound=False)
    F.line(sp([(-0.09 * h, -0.50 * h), (-0.115 * h, -0.42 * h), (-0.10 * h, -0.34 * h)], False), h * 0.0035, tone=0.9, alpha=0.6)
    for yy in (-0.47, -0.43, -0.39, -0.35):
        F.fill(ell(-0.108 * h + (0.0 if yy > -0.4 else 0.004) * h, yy * h, 0.005 * h, 0.005 * h), rim=0.0, tone=1.0, alpha=0.6, bound=False)
    F.fill(sp([KC(-0.06 * h, -0.70 * h), (0.0 * h, -0.62 * h), (0.075 * h, -0.575 * h), (0.15 * h, -0.55 * h), (0.172 * h, -0.52 * h), (0.15 * h, -0.49 * h), (0.07 * h, -0.50 * h),
               (-0.02 * h, -0.54 * h), (-0.10 * h, -0.60 * h), (-0.12 * h, -0.68 * h)], True, 0.95), rim=1.0)
    F.crease((-0.05 * h, -0.66 * h), (0.10 * h, -0.53 * h), 0.008 * h, 0.01 * h)
    F.crease((-0.09 * h, -0.64 * h), (0.05 * h, -0.52 * h), 0.006 * h, 0.008 * h, alpha=0.5)
    add_head(F, hx, hy, hh, "m", rot=12, beard="short", hat="cowl", nose=1.05, neck_to=(0.02 * h, -0.765 * h), hat_rot=0)
    return F.build()


# ───────────────────────────── woman ─────────────────────────────
@fx("woman")
def _woman(h, lean):
    F = Fig(h, lean)
    S = 0.905
    hh = 0.13 * h
    hx, hy = 0.03 * h, -S * h + 0.5 * hh
    F.fill(robe_path(h, sh_y=-0.735, nb_y=-0.758, back_sh=-0.088, front_sh=0.082, chest=(-0.098, 0.088, -0.655), waist=(-0.07, 0.066, -0.545),
                     hip=(-0.19, 0.178, -0.36), hem=(-0.285, 0.255, -0.012), nfold=4, amp=0.009, lift=0.02, wave_b=0.012, wave_f=0.012, k=1.0), rim=0.9, glow=0.10)
    F.fill(shoe(0.14 * h, 0, 0.08 * h, 0.024 * h, 1, "round"), rim=0.7)
    robe_folds(F, h, -0.05, 0.05, -0.54, -0.03, 9, 0.011, bend=0.012, seed=31, spread=1.15)
    hem_slits(F, h, [-0.21, -0.12, -0.03, 0.06, 0.15, 0.22], -0.008, depth=0.08)
    hem_band(F, h, -0.23, 0.2, -0.05, n=12, size=0.009, alpha=0.38, lift=0.02)
    F.fill(poly([(-0.07 * h, -0.545 * h), (0.066 * h, -0.545 * h), (0.0, -0.49 * h)]), rim=0.6, tone=0.12, bound=False)
    F.line(poly([(-0.07 * h, -0.545 * h), (0.0, -0.49 * h), (0.066 * h, -0.545 * h)], False), h * 0.0035, tone=1.0, alpha=0.55)
    for k in range(5):
        F.fill(ell(0.0, (-0.69 + k * 0.032) * h, 0.0042 * h, 0.0042 * h), rim=0.0, tone=1.0, alpha=0.6, bound=False)
    add_arm(F, [(-0.02 * h, -0.718 * h), (-0.07 * h, -0.615 * h), (0.05 * h, -0.545 * h)], [0.046 * h, 0.05 * h, 0.034 * h], hand="open", hand_len=0.068 * h, hand_rot=10)
    F.fill(ell(0.082 * h, -0.543 * h, 0.03 * h, 0.018 * h, 10), rim=1.0)
    add_head(F, hx, hy, hh, "f", rot=3, hat="veil", hair="bun", neck_to=(0.0, -0.758 * h), neck_w=(0.42, 0.6), hat_rot=0)
    return F.build()


# ───────────────────────────── emperor_old ─────────────────────────────
def emperor_fig(h, lean, cane=True, far_arm=False):
    F = Fig(h, lean)
    hh = 0.13 * h
    hx, hy = 0.085 * h, -0.875 * h + 0.5 * hh
    if cane:                      # baston (yakın el) — yere basar
        F.fill(bar(0.15 * h, -0.465 * h, 0.21 * h, 0.0, 0.011 * h, 0.009 * h, True, False), rim=0.9)
        F.fill(sp([(0.13 * h, -0.465 * h), (0.145 * h, -0.49 * h), (0.172 * h, -0.482 * h), (0.172 * h, -0.455 * h), (0.15 * h, -0.45 * h)], True), rim=1.0)
    F.fill(shoe(0.125 * h, 0, 0.09 * h, 0.03 * h, 1, "round"), rim=0.7)
    F.fill(shoe(-0.05 * h, 0, 0.08 * h, 0.028 * h, 1, "round"), rim=0.6)
    F.fill(robe_path(h, sh_y=-0.715, nb_y=-0.735, back_sh=-0.13, front_sh=0.105, chest=(-0.16, 0.11, -0.62), waist=(-0.125, 0.105, -0.49), belly=0.02,
                     hip=(-0.17, 0.15, -0.30), hem=(-0.215, 0.205, -0.012), nfold=4, amp=0.007, lift=0.02), rim=0.9, glow=0.10)
    robe_folds(F, h, -0.07, 0.07, -0.49, -0.03, 6, 0.011, bend=0.010, seed=41)
    hem_slits(F, h, [-0.16, -0.07, 0.02, 0.11], -0.008, depth=0.07)
    F.fill(fur_band([(-0.14 * h, -0.67 * h), (-0.12 * h, -0.72 * h), (-0.05 * h, -0.752 * h), (0.045 * h, -0.752 * h), (0.10 * h, -0.725 * h), (0.112 * h, -0.67 * h)], 0.05 * h, 0.016 * h, side=1), rim=1.0)
    F.fill(fur_band([(0.06 * h, -0.735 * h), (0.098 * h, -0.67 * h), (0.11 * h, -0.57 * h), (0.10 * h, -0.45 * h)], 0.04 * h, 0.015 * h, side=-1), rim=1.0)
    F.fill(fur_band([(-0.07 * h, -0.745 * h), (-0.13 * h, -0.70 * h), (-0.158 * h, -0.60 * h)], 0.04 * h, 0.015 * h, side=1), rim=0.8)
    add_arm(F, [(-0.03 * h, -0.70 * h), (-0.095 * h, -0.585 * h), (0.14 * h, -0.465 * h)], [0.074 * h, 0.082 * h, 0.05 * h], hand="fist", hand_len=0.075 * h, hand_rot=60)
    F.crease((-0.06 * h, -0.67 * h), (-0.09 * h, -0.58 * h), 0.007 * h, 0.006 * h)
    add_head(F, hx, hy, hh, "o", rot=12, beard="short", hat="flatcap", nose=1.2, chin=0.05, neck_to=(0.0, -0.735 * h), neck_w=(0.55, 0.78), hat_rot=6, hair="short")
    return F


@fx("emperor_old")
def _emperor_old(h, lean):
    return emperor_fig(h, lean).build()


# ───────────────────────────── prince ─────────────────────────────
def prince_fig(h, lean, sword=True, hat="beret", ruff_on=True):
    F = Fig(h, lean)
    hh = 0.13 * h
    hx, hy = 0.05 * h, -0.925 * h + 0.5 * hh
    # kılıç kını (gövdenin arkasından çapraz)
    if sword:
        F.fill(bar(-0.07 * h, -0.50 * h, -0.285 * h, -0.17 * h, 0.017 * h, 0.011 * h, True, True), rim=0.9)
        F.fill(bar(-0.045 * h, -0.538 * h, -0.095 * h, -0.462 * h, 0.011 * h, 0.011 * h, True, True), rim=0.9)
        F.fill(bar(-0.115 * h, -0.468 * h, -0.02 * h, -0.55 * h, 0.009 * h, 0.009 * h, True, True), rim=0.9)
    # kısa pelerin (arkada)
    F.fill(sp([KC(-0.045 * h, -0.775 * h), (-0.115 * h, -0.75 * h), (-0.15 * h, -0.64 * h), (-0.178 * h, -0.50 * h), (-0.195 * h, -0.37 * h), KC(-0.15 * h, -0.335 * h), (-0.115 * h, -0.40 * h), (-0.09 * h, -0.52 * h), (-0.06 * h, -0.64 * h)], True), rim=0.9, glow=0.08)
    F.crease((-0.115 * h, -0.70 * h), (-0.165 * h, -0.40 * h), 0.008 * h, 0.01 * h)
    F.crease((-0.09 * h, -0.68 * h), (-0.12 * h, -0.42 * h), 0.006 * h, -0.006 * h, alpha=0.5)
    # bacaklar (çorap): arka bacak
    add_leg(F, h, (-0.025, -0.46), (-0.055, -0.26), (-0.09, -0.046), (0.075, 0.048, 0.032), 1, "square", 0.085, 0.7)
    add_leg(F, h, (0.03, -0.46), (0.085, -0.27), (0.115, -0.046), (0.08, 0.052, 0.034), 1, "square", 0.09, 0.9)
    # şişkin pantolon (trunk hose)
    F.fill(sp([KC(-0.09 * h, -0.49 * h), (-0.125 * h, -0.43 * h), (-0.105 * h, -0.355 * h), (-0.02 * h, -0.325 * h), (0.07 * h, -0.335 * h), (0.13 * h, -0.375 * h), (0.125 * h, -0.45 * h), KC(0.09 * h, -0.49 * h)], True), rim=0.9)
    for x in (-0.07, -0.025, 0.02, 0.07):
        F.crease((x * h, -0.47 * h), ((x + 0.005) * h, -0.345 * h), 0.006 * h, 0.004 * h, alpha=0.5)
    # gövde (doublet)
    F.fill(sp([KC(-0.04 * h, -0.775 * h), (-0.10 * h, -0.745 * h), (-0.105 * h, -0.65 * h), (-0.085 * h, -0.54 * h), KC(-0.12 * h, -0.45 * h), KC(0.125 * h, -0.45 * h), (0.092 * h, -0.54 * h), (0.108 * h, -0.64 * h), (0.098 * h, -0.74 * h), (0.05 * h, -0.775 * h)], True, 0.95), rim=0.9, glow=0.10)
    F.line(poly([(0.0, -0.76 * h), (0.0, -0.46 * h)], False), h * 0.0035, tone=0.8, alpha=0.5)
    for k in range(6):
        F.fill(ell(0.012 * h, (-0.72 + k * 0.045) * h, 0.0045 * h, 0.0045 * h), rim=0.0, tone=0.8, alpha=0.7, bound=False)
    # yakın kol: kılıç kabzasında
    F.fill(ell(-0.04 * h, -0.735 * h, 0.05 * h, 0.032 * h, -15), rim=1.0)
    add_arm(F, [(-0.035 * h, -0.73 * h), (-0.125 * h, -0.60 * h), (-0.06 * h, -0.505 * h)], [0.066 * h, 0.072 * h, 0.044 * h], hand="fist", hand_len=0.07 * h, hand_rot=15)
    F.crease((-0.07 * h, -0.70 * h), (-0.12 * h, -0.60 * h), 0.006 * h, 0.006 * h)
    add_head(F, hx, hy, hh, "m", rot=-2, beard=None, hat=hat, neck_to=(0.0, -0.775 * h), hat_rot=-4)
    if ruff_on:
        _ruff(F, h, 0.012 * h, -0.775 * h, rx=0.072, ry=0.017)
    return F


@fx("prince")
def _prince(h, lean):
    return prince_fig(h, lean).build()


# ───────────────────────────── page ─────────────────────────────
@fx("page")
def _page(h, lean):
    F = Fig(h, lean)
    hh = 0.152 * h
    hx, hy = 0.04 * h, -0.93 * h + 0.5 * hh
    add_leg(F, h, (-0.02, -0.40), (-0.045, -0.23), (-0.075, -0.045), (0.07, 0.044, 0.03), 1, "round", 0.08, 0.7)
    add_leg(F, h, (0.03, -0.40), (0.075, -0.23), (0.10, -0.045), (0.07, 0.046, 0.032), 1, "round", 0.085, 0.9)
    # tunik (dize kadar), kemerli
    F.fill(sp([KC(-0.035 * h, -0.745 * h), (-0.092 * h, -0.72 * h), (-0.096 * h, -0.62 * h), (-0.082 * h, -0.52 * h), KC(-0.125 * h, -0.34 * h), KC(0.12 * h, -0.34 * h), (0.088 * h, -0.52 * h), (0.098 * h, -0.62 * h), (0.09 * h, -0.72 * h), (0.045 * h, -0.745 * h)], True, 0.95), rim=0.9, glow=0.10)
    F.fill(poly([(-0.085 * h, -0.535 * h), (0.092 * h, -0.535 * h), (0.092 * h, -0.515 * h), (-0.085 * h, -0.515 * h)]), rim=0.5, tone=0.2, bound=False)
    for x in (-0.07, -0.03, 0.02, 0.07):
        F.crease((x * h, -0.51 * h), ((x - 0.01) * h, -0.35 * h), 0.006 * h, 0.004 * h, alpha=0.55)
    # kol: rulo mektubu uzatır
    add_arm(F, [(-0.02 * h, -0.715 * h), (0.045 * h, -0.62 * h), (0.15 * h, -0.60 * h)], [0.05 * h, 0.05 * h, 0.034 * h], hand="fist", hand_len=0.07 * h, hand_rot=-5)
    F.fill(bar(0.145 * h, -0.575 * h, 0.168 * h, -0.655 * h, 0.017 * h, 0.017 * h, True, True), rim=1.0)
    F.line(poly([(0.152 * h, -0.60 * h), (0.162 * h, -0.64 * h)], False), h * 0.003, tone=1.0, alpha=0.45)
    # hafif sayfa pelerini (tabard) önü
    add_head(F, hx, hy, hh, "c", rot=6, hat="flatcap", neck_to=(0.0, -0.745 * h), neck_w=(0.5, 0.7), hat_rot=4, hair="bob")
    return F.build()


# ───────────────────────────── seated (tahtta, taçlı) ─────────────────────────────
@fx("seated")
def _seated(h, lean):
    F = Fig(h, lean)
    hh = 0.13 * h
    hx, hy = 0.03 * h, -0.795 * h + 0.5 * hh
    # arkadan dökülen mantı (arkalığın gerisinden yere)
    F.fill(sp([KC(-0.08 * h, -0.63 * h), (-0.165 * h, -0.59 * h), (-0.23 * h, -0.42 * h), (-0.265 * h, -0.18 * h), KC(-0.29 * h, 0.0), KC(-0.02 * h, 0.0), (-0.05 * h, -0.20 * h), (-0.07 * h, -0.40 * h)], True), rim=0.8, glow=0.08)
    F.crease((-0.15 * h, -0.55 * h), (-0.24 * h, -0.05 * h), 0.009 * h, 0.01 * h)
    # alt bacak + ayakkabı
    F.fill(limb([(0.17 * h, -0.26 * h), (0.19 * h, -0.13 * h), (0.20 * h, -0.04 * h)], [0.085 * h, 0.07 * h, 0.05 * h], cap0=0.3, cap1=0.2), rim=0.8)
    F.fill(shoe(0.185 * h, 0, 0.10 * h, 0.036 * h, 1, "round"), rim=0.8)
    # dik oturan gövde + kucak (diz örtüsü)
    F.fill(sp([KC(-0.045 * h, -0.64 * h), (-0.11 * h, -0.61 * h), (-0.125 * h, -0.50 * h), (-0.12 * h, -0.34 * h), KC(-0.115 * h, -0.255 * h), (0.0 * h, -0.245 * h), (0.12 * h, -0.255 * h), (0.215 * h, -0.275 * h),
               KC(0.238 * h, -0.30 * h), (0.225 * h, -0.34 * h), (0.15 * h, -0.355 * h), (0.115 * h, -0.45 * h), (0.118 * h, -0.56 * h), (0.105 * h, -0.62 * h), (0.055 * h, -0.64 * h)], True, 0.95), rim=0.9, glow=0.10)
    for (a, b, c) in ((0.0, -0.33, 0.01), (0.07, -0.34, 0.008), (0.14, -0.33, 0.008), (0.2, -0.31, 0.007)):
        F.crease((a * h, b * h), ((a + 0.02) * h, -0.255 * h), c * h, 0.006 * h, alpha=0.6)
    F.crease((-0.06 * h, -0.55 * h), (-0.075 * h, -0.30 * h), 0.008 * h, 0.01 * h)
    # asa (yakın el) ve küre (uzak el, dizde)
    F.fill(bar(0.215 * h, -0.30 * h, 0.25 * h, -0.93 * h, 0.011 * h, 0.011 * h, True, True), rim=0.9)
    F.fill(ell(0.253 * h, -0.955 * h, 0.022 * h, 0.022 * h), rim=1.0)
    F.fill(poly([(0.241 * h, -0.985 * h), (0.265 * h, -0.985 * h), (0.265 * h, -0.977 * h), (0.241 * h, -0.977 * h)]), rim=1.0)
    F.fill(poly([(0.2485 * h, -1.0 * h), (0.2575 * h, -1.0 * h), (0.2575 * h, -0.965 * h), (0.2485 * h, -0.965 * h)]), rim=1.0)
    F.fill(ell(0.168 * h, -0.335 * h, 0.034 * h, 0.034 * h), rim=1.0)
    F.fill(poly([(0.163 * h, -0.385 * h), (0.173 * h, -0.385 * h), (0.173 * h, -0.34 * h), (0.163 * h, -0.34 * h)]), rim=1.0)
    F.fill(poly([(0.152 * h, -0.372 * h), (0.184 * h, -0.372 * h), (0.184 * h, -0.364 * h), (0.152 * h, -0.364 * h)]), rim=1.0)
    # ermin yaka + ön klapa
    F.fill(fur_band([(-0.125 * h, -0.60 * h), (-0.105 * h, -0.64 * h), (-0.04 * h, -0.668 * h), (0.055 * h, -0.668 * h), (0.105 * h, -0.64 * h), (0.118 * h, -0.60 * h)], 0.056 * h, 0.018 * h, side=1), rim=1.0)
    F.fill(fur_band([(0.06 * h, -0.655 * h), (0.105 * h, -0.58 * h), (0.115 * h, -0.45 * h), (0.15 * h, -0.36 * h), (0.225 * h, -0.335 * h)], 0.046 * h, 0.016 * h, side=-1), rim=1.0)
    # ermin benekleri (kürk şeridi üzerinde açık-ton küçük kuyruk uçları)
    for (ex_, ey_) in ((0.075, -0.60), (0.095, -0.52), (0.112, -0.44), (0.16, -0.375), (0.205, -0.35), (-0.075, -0.655), (-0.01, -0.672), (0.04, -0.668)):
        F.fill(lens(((ex_ - 0.004) * h, (ey_ - 0.012) * h), ((ex_ + 0.004) * h, (ey_ + 0.012) * h), 0.007 * h, 0.0), rim=0.0, tone=1.0, alpha=0.55, bound=False)
    # yakın kol: asayı tutar (dirsek yanda, el önde)
    add_arm(F, [(-0.03 * h, -0.625 * h), (-0.045 * h, -0.49 * h), (0.105 * h, -0.415 * h)], [0.066 * h, 0.07 * h, 0.046 * h], hand="fist", hand_len=0.065 * h, hand_rot=-20)
    add_head(F, hx, hy, hh, "m", rot=-3, beard="short", hat="crown_i", nose=1.1, chin=0.04, neck_to=(0.0, -0.645 * h), hat_rot=-3)
    return F.build()


# ───────────────────────────── kneel (tek dizi üstünde diz çökmüş dilekçi/biat eden; eller kavuşmuş, baş eğik) ─────────────────────────────
@fx("kneel")
def _kneel(h, lean):
    F = Fig(h, lean)
    hh = 0.13 * h
    hx, hy = 0.075 * h, -0.755 * h + 0.5 * hh
    # arka bacak: yerde diz, baldır geriye uzanır (cüppe altından ayakkabı ucu görünür)
    F.fill(shoe(-0.30 * h, -0.005 * h, 0.09 * h, 0.028 * h, -1, "round"), rim=0.6)
    # arkaya dökülen pelerin/cüppe (yerde sürünür)
    F.fill(sp([KC(0.0 * h, -0.62 * h), (-0.08 * h, -0.58 * h), (-0.14 * h, -0.44 * h), (-0.20 * h, -0.26 * h), (-0.30 * h, -0.10 * h), KC(-0.36 * h, 0.0), KC(-0.04 * h, 0.0),
               (-0.02 * h, -0.14 * h), (0.0 * h, -0.30 * h), (0.02 * h, -0.46 * h)], True, 0.95), rim=0.9, glow=0.08)
    F.crease((-0.05 * h, -0.48 * h), (-0.24 * h, -0.05 * h), 0.009 * h, 0.012 * h)
    F.crease((-0.02 * h, -0.40 * h), (-0.12 * h, -0.03 * h), 0.008 * h, 0.01 * h)
    F.crease((-0.09 * h, -0.52 * h), (-0.30 * h, -0.07 * h), 0.007 * h, 0.01 * h, alpha=0.5)
    # ön bacak: uyluk yatay, diz yukarıda; kaval dik; çorap + ayakkabı
    F.fill(limb([(0.12 * h, -0.285 * h), (0.19 * h, -0.14 * h), (0.205 * h, -0.04 * h)], [0.075 * h, 0.06 * h, 0.04 * h], cap0=0.4, cap1=0.3), rim=0.9)
    F.fill(shoe(0.185 * h, 0, 0.10 * h, 0.036 * h, 1, "square"), rim=0.9)
    # gövde + uyluğu örten cüppe, dizde yatay kıvrım
    F.fill(sp([KC(-0.02 * h, -0.64 * h), (-0.09 * h, -0.60 * h), (-0.115 * h, -0.46 * h), (-0.10 * h, -0.32 * h), KC(-0.08 * h, -0.26 * h), (0.04 * h, -0.255 * h), (0.14 * h, -0.275 * h), (0.215 * h, -0.30 * h),
               KC(0.235 * h, -0.325 * h), (0.20 * h, -0.36 * h), (0.12 * h, -0.375 * h), (0.075 * h, -0.45 * h), (0.09 * h, -0.55 * h), (0.075 * h, -0.62 * h), (0.03 * h, -0.64 * h)], True, 0.95), rim=0.9, glow=0.10)
    for (a, b, c, d, bb) in ((0.0, -0.33, -0.03, -0.26, 0.006), (0.07, -0.36, 0.08, -0.265, 0.006), (0.15, -0.355, 0.17, -0.285, 0.005)):
        F.crease((a * h, b * h), (c * h, d * h), 0.007 * h, bb * h, alpha=0.6)
    F.crease((-0.06 * h, -0.55 * h), (-0.075 * h, -0.34 * h), 0.008 * h, 0.01 * h)
    # omuzda pelerin kıvrımı
    F.fill(sp([KC(-0.005 * h, -0.635 * h), (-0.085 * h, -0.605 * h), (-0.13 * h, -0.52 * h), (-0.12 * h, -0.44 * h), (-0.06 * h, -0.47 * h), (-0.01 * h, -0.53 * h), (0.03 * h, -0.58 * h)], True), rim=0.9, tone=0.04)
    # eller kavuşmuş, dizde
    add_arm(F, [(0.0 * h, -0.60 * h), (0.045 * h, -0.47 * h), (0.15 * h, -0.385 * h)], [0.05 * h, 0.05 * h, 0.036 * h], hand="open", hand_len=0.07 * h, hand_rot=10)
    F.fill(ell(0.175 * h, -0.372 * h, 0.03 * h, 0.018 * h, 10), rim=1.0)
    add_head(F, hx, hy, hh, "m", rot=20, beard=None, hair="bob", neck_to=(0.03 * h, -0.635 * h), hat_rot=0, nose=1.05)
    return F.build()


# ───────────────────────────── pair_old_prince (c0/c12'nin kilit figürü) ─────────────────────────────
# Yaşlı, bükülmüş imparator (solda, geride) genç prensin omzuna yaslanır; bastonu önde yere basar. İkisi de sağa bakar; h ≈ prensin boyu.
def pair_fig(h, lean):
    F = Fig(h, lean)
    es = 0.955
    ex = -0.215 * h
    px = 0.225 * h
    F.merge(emperor_fig(h * es, 0, cane=True), dx=ex)
    F.merge(prince_fig(h, 0, sword=True, hat="beret"), dx=px)
    # imparatorun uzanan (uzak) kolu: omuzdan prensin omzuna; el omuz üstünde
    sx, sy = ex + 0.015 * h, -0.655 * h * es
    tx, ty = px - 0.045 * h, -0.752 * h
    F.fill(limb([(sx, sy), (sx + (tx - sx) * 0.52, sy + 0.050 * h), (tx - 0.030 * h, ty + 0.045 * h)], [0.060 * h, 0.056 * h, 0.038 * h], cap0=0.5, cap1=0.2), rim=1.0)
    F.crease((sx + 0.02 * h, sy - 0.008 * h), (sx + (tx - sx) * 0.55, sy + 0.04 * h), 0.005 * h, 0.006 * h)
    F.fill(lens((tx - 0.045 * h, ty + 0.06 * h), (tx - 0.015 * h, ty + 0.05 * h), 0.012 * h, 0.0), rim=0.0, tone=1.0, alpha=0.5, bound=False)
    F.fill(K.hand_pt("open", tx - 0.032 * h, ty + 0.05 * h, 0.088 * h, -22), rim=1.0)
    F.fill(K.hand_pt("thumb", tx - 0.032 * h, ty + 0.05 * h, 0.088 * h, -22), rim=1.0)
    return F.build()


@fx("pair_old_prince")
def _pair(h, lean):
    return pair_fig(h, lean)
