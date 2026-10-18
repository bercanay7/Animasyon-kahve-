"""figs_more — grup-2 figürleri (figür-lab): child, peasant, fisherman, bearer, friar_writing, scholar_lectern, woman_seated, man_seated_bed, coffin,
inca_noble, aztec_warrior, arquebusier, halberdier, crowd_a…crowd_f. Hepsi sağa bakar; ayak (0,0), yukarı −y."""
import math

import skia

import stage as ST
import figs_kit as K
from figs_kit import K as KC, Fig, bar, ell, feather_path, lens, limb, place, poly, shoe, sp
from figs_parts import add_arm, add_head, add_leg, fur_band, hem_slits, robe_folds, robe_path
from figs_war import pike, torso


def fx(name):
    return ST.figx(name)


# ───────────────────────────── child (≈8 yaş) ─────────────────────────────
@fx("child")
def _child(h, lean):
    F = Fig(h, lean)
    hh = 0.175 * h
    hx, hy = 0.035 * h, -0.93 * h + 0.5 * hh
    # çıplak ayak/sade ayakkabı bacaklar
    for (a, b, c, rim) in (((-0.015, -0.36), (-0.04, -0.20), (-0.065, -0.03), 0.7), ((0.03, -0.36), (0.065, -0.20), (0.09, -0.03), 0.9)):
        F.fill(limb([(a[0] * h, a[1] * h), (b[0] * h, b[1] * h), (c[0] * h, c[1] * h)], [0.06 * h, 0.044 * h, 0.034 * h], cap0=0.3, cap1=0.3), rim=rim)
        F.fill(shoe((c[0] - 0.012) * h, 0, 0.075 * h, 0.032 * h, 1, "round"), rim=rim)
    # tunik (dize kadar), kemerli, hafif çan
    F.fill(sp([KC(-0.03 * h, -0.755 * h), (-0.085 * h, -0.735 * h), (-0.09 * h, -0.64 * h), (-0.08 * h, -0.55 * h), KC(-0.115 * h, -0.34 * h), KC(0.112 * h, -0.34 * h), (0.082 * h, -0.55 * h), (0.092 * h, -0.64 * h), (0.082 * h, -0.735 * h), (0.04 * h, -0.755 * h)], True, 0.95), rim=0.9, glow=0.10)
    F.fill(poly([(-0.082 * h, -0.55 * h), (0.084 * h, -0.55 * h), (0.084 * h, -0.532 * h), (-0.082 * h, -0.532 * h)]), rim=0.5, tone=0.2, bound=False)
    for x in (-0.06, -0.02, 0.03, 0.075):
        F.crease((x * h, -0.53 * h), ((x - 0.01) * h, -0.36 * h), 0.006 * h, 0.004 * h, alpha=0.55)
    # kollar: biri sallanır, biri havada (merak / el sallıyor)
    add_arm(F, [(-0.02 * h, -0.735 * h), (-0.07 * h, -0.64 * h), (-0.06 * h, -0.54 * h)], [0.05 * h, 0.046 * h, 0.034 * h], hand="open", hand_len=0.062 * h, hand_rot=95)
    add_arm(F, [(0.03 * h, -0.735 * h), (0.10 * h, -0.70 * h), (0.15 * h, -0.775 * h)], [0.05 * h, 0.046 * h, 0.034 * h], hand="open", hand_len=0.062 * h, hand_rot=-70)
    add_head(F, hx, hy, hh, "c", rot=-6, hair="bob", neck_to=(0.0, -0.76 * h), neck_w=(0.48, 0.66), hat_rot=0)
    return F.build()


# ───────────────────────────── peasant (yaba taşıyan köylü) ─────────────────────────────
def _fork(F, h, x0, y0, x1, y1):
    F.fill(bar(x0 * h, y0 * h, x1 * h, y1 * h, 0.011 * h, 0.009 * h), rim=0.9)
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    bx, by = x1 * h, y1 * h
    F.fill(bar(bx - nx * 0.03 * h, by - ny * 0.03 * h, bx + nx * 0.03 * h, by + ny * 0.03 * h, 0.008 * h, 0.008 * h), rim=0.9)
    for k in (-1, 0, 1):
        F.fill(bar(bx + nx * 0.03 * k * h, by + ny * 0.03 * k * h, bx + nx * 0.03 * k * h + ux * 0.1 * h, by + ny * 0.03 * k * h + uy * 0.1 * h, 0.007 * h, 0.003 * h), rim=1.0)


@fx("peasant")
def _peasant(h, lean):
    F = Fig(h, lean)
    hh = 0.135 * h
    hx, hy = 0.06 * h, -0.905 * h + 0.5 * hh
    # yaba omuzda, el belde
    _fork(F, h, 0.19, 0.0, 0.215, -1.02)
    for (a, b, c, rim) in (((-0.02, -0.46), (-0.06, -0.24), (-0.10, -0.03), 0.7), ((0.04, -0.46), (0.085, -0.25), (0.125, -0.03), 0.9)):
        F.fill(limb([(a[0] * h, a[1] * h), (b[0] * h, b[1] * h), (c[0] * h, c[1] * h)], [0.074 * h, 0.05 * h, 0.034 * h], cap0=0.3, cap1=0.3), rim=rim)
        F.fill(sp([KC((c[0] - 0.02) * h, (c[1] - 0.01) * h), ((c[0] + 0.05) * h, (c[1] - 0.012) * h), KC((c[0] + 0.075) * h, 0.0), KC((c[0] - 0.03) * h, 0.0)], True, 0.8), rim=rim)
    # dizlik pantolon bandı
    F.fill(sp([KC(-0.10 * h, -0.50 * h), (-0.11 * h, -0.42 * h), (-0.09 * h, -0.34 * h), KC(0.0, -0.31 * h), KC(0.13 * h, -0.34 * h), (0.125 * h, -0.42 * h), KC(0.11 * h, -0.50 * h)], True), rim=0.9)
    # bol gömlek/yelek, kambur
    F.fill(sp([KC(-0.04 * h, -0.755 * h), (-0.105 * h, -0.725 * h), (-0.118 * h, -0.63 * h), (-0.10 * h, -0.54 * h), KC(-0.115 * h, -0.46 * h), KC(0.12 * h, -0.46 * h), (0.10 * h, -0.54 * h), (0.115 * h, -0.64 * h), (0.098 * h, -0.725 * h), (0.05 * h, -0.755 * h)], True, 0.95), rim=0.9, glow=0.10)
    F.crease((-0.05 * h, -0.70 * h), (-0.07 * h, -0.50 * h), 0.007 * h, 0.006 * h)
    F.crease((0.03 * h, -0.70 * h), (0.045 * h, -0.50 * h), 0.007 * h, -0.005 * h)
    F.fill(poly([(-0.105 * h, -0.52 * h), (0.11 * h, -0.52 * h), (0.11 * h, -0.50 * h), (-0.105 * h, -0.50 * h)]), rim=0.5, tone=0.2, bound=False)
    add_arm(F, [(-0.03 * h, -0.72 * h), (-0.115 * h, -0.62 * h), (-0.04 * h, -0.50 * h)], [0.066 * h, 0.07 * h, 0.044 * h], hand="fist", hand_len=0.066 * h, hand_rot=30)
    add_arm(F, [(0.04 * h, -0.725 * h), (0.11 * h, -0.64 * h), (0.205 * h, -0.62 * h)], [0.058 * h, 0.056 * h, 0.042 * h], hand="fist", hand_len=0.06 * h, hand_rot=-3)
    add_head(F, hx, hy, hh, "m", rot=8, beard="short", hat="straw", nose=1.12, neck_to=(0.01 * h, -0.755 * h), hat_rot=3)
    return F.build()


# ───────────────────────────── fisherman ─────────────────────────────
@fx("fisherman")
def _fisherman(h, lean):
    F = Fig(h, lean)
    hh = 0.135 * h
    hx, hy = 0.055 * h, -0.915 * h + 0.5 * hh
    # olta (omuzda, öne uzanan ince sırık + ip) ve balık dizisi
    F.fill(bar(-0.04 * h, -0.50 * h, 0.50 * h, -1.20 * h, 0.010 * h, 0.004 * h), rim=0.9)
    F.line(sp([(0.50 * h, -1.20 * h), (0.56 * h, -1.0 * h), (0.55 * h, -0.80 * h)], False), h * 0.0025, tone=0.8, alpha=0.7)
    F.fill(sp([KC(0.55 * h, -0.80 * h), (0.58 * h, -0.815 * h), (0.605 * h, -0.795 * h), KC(0.595 * h, -0.775 * h), (0.58 * h, -0.785 * h), (0.555 * h, -0.775 * h)], True), rim=0.8)
    # bacaklar: çıplak, paçaları sıvalı
    for (a, b, c, rim) in (((-0.02, -0.44), (-0.05, -0.21), (-0.09, -0.03), 0.7), ((0.04, -0.44), (0.085, -0.22), (0.125, -0.03), 0.9)):
        F.fill(limb([(a[0] * h, a[1] * h), (b[0] * h, b[1] * h), (c[0] * h, c[1] * h)], [0.07 * h, 0.046 * h, 0.032 * h], cap0=0.3, cap1=0.3), rim=rim)
        F.fill(sp([KC((c[0] - 0.02) * h, (c[1] - 0.01) * h), ((c[0] + 0.05) * h, (c[1] - 0.012) * h), KC((c[0] + 0.075) * h, 0.0), KC((c[0] - 0.03) * h, 0.0)], True, 0.8), rim=rim)
    F.fill(sp([KC(-0.10 * h, -0.50 * h), (-0.115 * h, -0.42 * h), (-0.10 * h, -0.30 * h), KC(-0.07 * h, -0.255 * h), KC(0.0, -0.255 * h), (0.02 * h, -0.30 * h), (0.075 * h, -0.255 * h), KC(0.13 * h, -0.28 * h), (0.125 * h, -0.40 * h), KC(0.11 * h, -0.50 * h)], True), rim=0.9)
    # gömlek + yağmurluk/yelek
    F.fill(sp([KC(-0.04 * h, -0.765 * h), (-0.105 * h, -0.735 * h), (-0.12 * h, -0.63 * h), (-0.105 * h, -0.54 * h), KC(-0.11 * h, -0.47 * h), KC(0.118 * h, -0.47 * h), (0.105 * h, -0.54 * h), (0.118 * h, -0.64 * h), (0.10 * h, -0.735 * h), (0.05 * h, -0.765 * h)], True, 0.95), rim=0.9, glow=0.10)
    F.crease((-0.05 * h, -0.71 * h), (-0.065 * h, -0.50 * h), 0.007 * h, 0.006 * h)
    F.crease((0.035 * h, -0.72 * h), (0.05 * h, -0.50 * h), 0.007 * h, -0.005 * h)
    F.fill(poly([(-0.105 * h, -0.52 * h), (0.11 * h, -0.52 * h), (0.11 * h, -0.50 * h), (-0.105 * h, -0.50 * h)]), rim=0.5, tone=0.2, bound=False)
    # yakın kol: sırığı tutar; uzak kol önde sepet
    add_arm(F, [(-0.03 * h, -0.73 * h), (-0.06 * h, -0.63 * h), (0.075 * h, -0.60 * h)], [0.066 * h, 0.07 * h, 0.044 * h], hand="fist", hand_len=0.066 * h, hand_rot=-15)
    F.fill(sp([KC(0.10 * h, -0.50 * h), (0.15 * h, -0.49 * h), (0.17 * h, -0.42 * h), (0.14 * h, -0.36 * h), (0.09 * h, -0.38 * h)], True), rim=1.0)
    for k in range(3):
        F.line(poly([(0.105 * h + k * 0.02 * h, -0.49 * h), (0.10 * h + k * 0.02 * h, -0.38 * h)], False), h * 0.003, tone=1.0, alpha=0.4)
    add_arm(F, [(0.045 * h, -0.725 * h), (0.10 * h, -0.62 * h), (0.115 * h, -0.52 * h)], [0.056 * h, 0.054 * h, 0.04 * h], hand="fist", hand_len=0.058 * h, hand_rot=95)
    add_head(F, hx, hy, hh, "m", rot=2, beard="short", hat="woolcap", nose=1.14, neck_to=(0.005 * h, -0.765 * h), hat_rot=2)
    return F.build()


# ───────────────────────────── bearer (sedye/tahtırevan taşıyıcısı) ─────────────────────────────
@fx("bearer")
def _bearer(h, lean):
    F = Fig(h, lean)
    hh = 0.135 * h
    hx, hy = 0.10 * h, -0.875 * h + 0.5 * hh
    # taşıma sırığı: omuzda, ön-arka uzar (iki uçta bağ halkası)
    F.fill(bar(-0.46 * h, -0.755 * h, 0.52 * h, -0.775 * h, 0.022 * h, 0.022 * h, True, True), rim=1.0)
    for x in (-0.38, 0.44):
        F.line(sp([(x * h, -0.74 * h), ((x + 0.005) * h, -0.68 * h)], False), h * 0.004, tone=0.7, alpha=0.8)
        F.fill(ell((x + 0.005) * h, -0.665 * h, 0.014 * h, 0.014 * h), rim=0.7)
    # bacaklar (yürüyüş, hafif çömelik)
    add_leg(F, h, (-0.045, -0.43), (-0.105, -0.25), (-0.15, -0.046), (0.075, 0.05, 0.034), 1, "round", 0.085, 0.7, calf=0.016)
    add_leg(F, h, (0.035, -0.43), (0.105, -0.25), (0.155, -0.046), (0.08, 0.052, 0.036), 1, "round", 0.09, 0.9, calf=0.016)
    # kısa tunik + kemer
    F.fill(sp([KC(-0.045 * h, -0.755 * h), (-0.115 * h, -0.725 * h), (-0.13 * h, -0.62 * h), (-0.115 * h, -0.52 * h), KC(-0.14 * h, -0.36 * h), KC(0.125 * h, -0.36 * h), (0.10 * h, -0.52 * h), (0.118 * h, -0.62 * h), (0.10 * h, -0.725 * h), (0.045 * h, -0.755 * h)], True, 0.95), rim=0.9, glow=0.10)
    F.fill(poly([(-0.115 * h, -0.52 * h), (0.10 * h, -0.52 * h), (0.10 * h, -0.50 * h), (-0.115 * h, -0.50 * h)]), rim=0.5, tone=0.2, bound=False)
    for x in (-0.08, -0.03, 0.03, 0.08):
        F.crease((x * h, -0.50 * h), ((x - 0.01) * h, -0.37 * h), 0.006 * h, 0.004 * h, alpha=0.55)
    F.crease((-0.06 * h, -0.70 * h), (-0.09 * h, -0.53 * h), 0.007 * h, 0.006 * h)
    # kollar: biri sırığı yukarıdan kavrar, diğeri destekler
    add_arm(F, [(-0.04 * h, -0.725 * h), (-0.13 * h, -0.66 * h), (-0.12 * h, -0.755 * h)], [0.064 * h, 0.066 * h, 0.044 * h], hand="fist", hand_len=0.064 * h, hand_rot=-60)
    add_arm(F, [(0.05 * h, -0.72 * h), (0.15 * h, -0.65 * h), (0.24 * h, -0.755 * h)], [0.056 * h, 0.054 * h, 0.04 * h], hand="fist", hand_len=0.058 * h, hand_rot=-60)
    add_head(F, hx, hy, hh, "m", rot=10, beard="stache", hat="woolcap", nose=1.1, neck_to=(0.03 * h, -0.755 * h), hat_rot=6)
    return F.build()


# ───────────────────────────── friar_writing (kandil/mum ışığında eğilmiş yazan keşiş) ─────────────────────────────
@fx("friar_writing")
def _friar_writing(h, lean):
    F = Fig(h, lean)
    hh = 0.13 * h
    # tabure + yazı masası (eğik levha) + mum
    F.fill(poly([(0.14 * h, -0.40 * h), (0.43 * h, -0.45 * h), (0.43 * h, -0.435 * h), (0.14 * h, -0.385 * h)]), rim=1.0)          # eğik levha
    F.fill(bar(0.17 * h, -0.39 * h, 0.17 * h, 0.0, 0.018 * h, 0.018 * h), rim=0.8)
    F.fill(bar(0.40 * h, -0.44 * h, 0.40 * h, 0.0, 0.018 * h, 0.018 * h), rim=0.7)
    F.fill(poly([(-0.14 * h, -0.30 * h), (0.04 * h, -0.30 * h), (0.04 * h, -0.28 * h), (-0.14 * h, -0.28 * h)]), rim=0.8)        # tabure
    F.fill(bar(-0.12 * h, -0.28 * h, -0.12 * h, 0.0, 0.016 * h, 0.016 * h), rim=0.6)
    F.fill(bar(0.02 * h, -0.28 * h, 0.02 * h, 0.0, 0.016 * h, 0.016 * h), rim=0.7)
    # mum (masanın ön ucunda) + alev parıltısı
    F.fill(poly([(0.395 * h, -0.445 * h), (0.415 * h, -0.445 * h), (0.415 * h, -0.52 * h), (0.395 * h, -0.52 * h)]), rim=1.0)
    F.fill(sp([KC(0.385 * h, -0.445 * h), (0.405 * h, -0.435 * h), KC(0.425 * h, -0.445 * h)], True), rim=0.6, bound=False)
    F.solid(ell(0.405 * h, -0.545 * h, 0.007 * h, 0.016 * h), "#FFE7A8", 0.98, bound=True)
    F.glowdot(0.405 * h, -0.545 * h, 0.09 * h, "#FFB347", 0.9)
    # cüppe (oturan: eğik gövde, dizler önde)
    F.fill(sp([KC(0.0 * h, -0.60 * h), (-0.09 * h, -0.56 * h), (-0.15 * h, -0.42 * h), (-0.19 * h, -0.28 * h), (-0.25 * h, -0.10 * h), KC(-0.29 * h, 0.0), KC(0.12 * h, 0.0),
               (0.13 * h, -0.10 * h), (0.12 * h, -0.26 * h), KC(0.15 * h, -0.31 * h), (0.10 * h, -0.36 * h), (0.07 * h, -0.45 * h), (0.095 * h, -0.55 * h), (0.07 * h, -0.60 * h)], True, 0.95), rim=0.9, glow=0.10)
    robe_folds_ = [(-0.18, -0.22, -0.30, -0.02), (-0.12, -0.28, -0.20, -0.02), (-0.05, -0.30, -0.10, -0.02), (0.02, -0.26, 0.04, -0.02)]
    for (a, b, c, d) in robe_folds_:
        F.crease((a * h, b * h), (c * h, d * h), 0.008 * h, 0.01 * h)
    # kollar: biri levhada tüy kalemle yazar, diğeri sayfayı tutar
    add_arm(F, [(-0.02 * h, -0.575 * h), (0.07 * h, -0.50 * h), (0.20 * h, -0.45 * h)], [0.06 * h, 0.056 * h, 0.04 * h], hand="open", hand_len=0.07 * h, hand_rot=15)
    F.fill(feather_path(0.24 * h, -0.465 * h, 0.34 * h, -0.60 * h, 0.03 * h, bend=-0.02 * h), rim=1.0)
    F.fill(bar(0.235 * h, -0.455 * h, 0.255 * h, -0.475 * h, 0.004 * h, 0.003 * h), rim=0.8)
    # başlık: kukuleta, kafa levhaya eğik
    add_head(F, 0.10 * h, -0.70 * h + 0.5 * hh, hh, "m", rot=26, beard="short", hat="cowl", nose=1.05, neck_to=(0.0 * h, -0.60 * h), hat_rot=10)
    return F.build()


# ───────────────────────────── scholar_lectern (kürsüde konuşan) ─────────────────────────────
@fx("scholar_lectern")
def _scholar_lectern(h, lean):
    F = Fig(h, lean)
    hh = 0.13 * h
    hx, hy = 0.04 * h, -0.925 * h + 0.5 * hh
    # kürsü: sütun gövde + eğik üst + açık kitap
    F.fill(sp([KC(0.215 * h, 0.0), KC(0.395 * h, 0.0), (0.37 * h, -0.10 * h), (0.345 * h, -0.30 * h), (0.36 * h, -0.55 * h), KC(0.24 * h, -0.55 * h), (0.255 * h, -0.30 * h), (0.23 * h, -0.10 * h)], True, 0.8), rim=1.0)
    F.fill(poly([(0.20 * h, -0.575 * h), (0.43 * h, -0.64 * h), (0.43 * h, -0.62 * h), (0.20 * h, -0.553 * h)]), rim=1.0)
    F.fill(poly([(0.22 * h, -0.585 * h), (0.31 * h, -0.62 * h), (0.40 * h, -0.655 * h), (0.40 * h, -0.64 * h), (0.31 * h, -0.605 * h), (0.22 * h, -0.57 * h)]), rim=1.0, tone=0.1, bound=False)
    F.line(poly([(0.31 * h, -0.62 * h), (0.31 * h, -0.605 * h)], False), h * 0.004, tone=0.8, alpha=0.7)
    F.line(poly([(0.24 * h, -0.575 * h), (0.38 * h, -0.62 * h)], False), h * 0.003, tone=1.0, alpha=0.4)
    for (a, b) in ((0.235, -0.50), (0.24, -0.35), (0.235, -0.18)):
        F.line(poly([(a * h, b * h), ((a + 0.13) * h, (b - 0.0) * h)], False), h * 0.003, tone=1.0, alpha=0.25)
    # ayaklar + cüppe
    F.fill(shoe(0.095 * h, 0, 0.09 * h, 0.03 * h, 1, "round"), rim=0.8)
    F.fill(robe_path(h, sh_y=-0.745, nb_y=-0.768, back_sh=-0.118, front_sh=0.108, chest=(-0.128, 0.114, -0.65), waist=(-0.105, 0.10, -0.50),
                     hip=(-0.155, 0.15, -0.31), hem=(-0.215, 0.195, -0.012), nfold=4, amp=0.008, lift=0.018), rim=0.9, glow=0.10)
    robe_folds(F, h, -0.07, 0.07, -0.50, -0.03, 7, 0.011, bend=0.010, seed=61)
    hem_slits(F, h, [-0.17, -0.09, -0.01, 0.07, 0.14], -0.008, depth=0.07)
    # omuz pelerini (hood/kürk) ve yaka
    F.fill(fur_band([(-0.125 * h, -0.70 * h), (-0.105 * h, -0.752 * h), (-0.04 * h, -0.782 * h), (0.05 * h, -0.782 * h), (0.10 * h, -0.752 * h), (0.114 * h, -0.70 * h)], 0.046 * h, 0.015 * h, side=1), rim=1.0)
    F.fill(fur_band([(0.06 * h, -0.765 * h), (0.10 * h, -0.70 * h), (0.114 * h, -0.60 * h), (0.10 * h, -0.50 * h)], 0.04 * h, 0.014 * h, side=-1), rim=1.0)
    # kollar: yakın kol kitaba uzanır; uzak kol konuşma jesti (yukarı)
    add_arm(F, [(0.03 * h, -0.725 * h), (0.14 * h, -0.67 * h), (0.24 * h, -0.62 * h)], [0.064 * h, 0.062 * h, 0.044 * h], hand="open", hand_len=0.075 * h, hand_rot=18)
    add_arm(F, [(-0.03 * h, -0.725 * h), (-0.12 * h, -0.64 * h), (-0.05 * h, -0.60 * h)], [0.064 * h, 0.068 * h, 0.044 * h], hand="open", hand_len=0.07 * h, hand_rot=-10)
    add_head(F, hx, hy, hh, "o", rot=-4, beard="short", hat="biretta", nose=1.15, chin=0.03, neck_to=(0.0, -0.768 * h), hat_rot=-3)
    return F.build()


# ───────────────────────────── woman_seated (peçeli oturan kadın; pencere önü) ─────────────────────────────
@fx("woman_seated")
def _woman_seated(h, lean):
    F = Fig(h, lean)
    hh = 0.125 * h
    hx, hy = 0.045 * h, -0.775 * h + 0.5 * hh
    # etek (kucak + yere dökülen), taburenin üstünde
    F.fill(shoe(0.20 * h, 0, 0.085 * h, 0.032 * h, 1, "round"), rim=0.7)
    F.fill(sp([KC(-0.03 * h, -0.62 * h), (-0.10 * h, -0.58 * h), (-0.13 * h, -0.44 * h), (-0.19 * h, -0.30 * h), (-0.27 * h, -0.12 * h), KC(-0.30 * h, 0.0), KC(0.24 * h, 0.0),
               (0.245 * h, -0.07 * h), (0.255 * h, -0.17 * h), (0.285 * h, -0.255 * h), (0.30 * h, -0.30 * h), (0.265 * h, -0.34 * h), (0.20 * h, -0.355 * h), (0.10 * h, -0.355 * h), (0.07 * h, -0.45 * h),
               (0.075 * h, -0.55 * h), (0.06 * h, -0.62 * h)], True, 0.95), rim=0.9, glow=0.10)
    for (a, b, c, d, bb) in ((-0.12, -0.34, -0.22, -0.03, 0.012), (-0.05, -0.34, -0.12, -0.03, 0.01), (0.03, -0.33, 0.02, -0.03, 0.01), (0.12, -0.32, 0.14, -0.03, 0.008), (0.19, -0.30, 0.22, -0.04, 0.008)):
        F.crease((a * h, b * h), (c * h, d * h), 0.009 * h, bb * h)
    hem_slits(F, h, [-0.26, -0.17, -0.08, 0.0, 0.09, 0.18], -0.006, depth=0.06)
    # korse + eller kucakta (tespih/kitap)
    F.fill(sp([KC(-0.03 * h, -0.625 * h), (-0.08 * h, -0.60 * h), (-0.075 * h, -0.50 * h), (-0.05 * h, -0.40 * h), KC(0.0, -0.34 * h), (0.07 * h, -0.36 * h), (0.075 * h, -0.45 * h), (0.07 * h, -0.55 * h), (0.055 * h, -0.62 * h)], True), rim=0.0, tone=0.06, bound=False)
    F.line(sp([(0.02 * h, -0.415 * h), (0.10 * h, -0.395 * h), (0.15 * h, -0.36 * h)], False), h * 0.004, tone=1.0, alpha=0.5)
    add_arm(F, [(-0.01 * h, -0.60 * h), (-0.04 * h, -0.50 * h), (0.075 * h, -0.40 * h)], [0.05 * h, 0.05 * h, 0.036 * h], hand="open", hand_len=0.065 * h, hand_rot=20)
    F.fill(ell(0.12 * h, -0.37 * h, 0.03 * h, 0.018 * h, 15), rim=1.0)
    add_head(F, hx, hy, hh, "f", rot=12, hat="veil", hair="bun", neck_to=(0.0, -0.625 * h), neck_w=(0.42, 0.6), hat_rot=6)
    return F.build()


# ───────────────────────────── man_seated_bed (yatakta oturan hasta yaşlı adam) ─────────────────────────────
@fx("man_seated_bed")
def _man_seated_bed(h, lean):
    F = Fig(h, lean)
    hh = 0.14 * h
    hx, hy = 0.0 * h, -0.60 * h + 0.5 * hh
    # yastık yığını (arkada) + battaniye (belden ileriye uzanan dalgalı dağ)
    F.fill(sp([KC(-0.20 * h, -0.20 * h), (-0.24 * h, -0.36 * h), (-0.20 * h, -0.56 * h), (-0.10 * h, -0.62 * h), (-0.02 * h, -0.50 * h), (-0.04 * h, -0.30 * h), KC(0.0 * h, -0.20 * h)], True, 0.95), rim=0.9)
    F.fill(sp([KC(-0.30 * h, -0.20 * h), (-0.31 * h, -0.30 * h), (-0.27 * h, -0.42 * h), (-0.22 * h, -0.44 * h), (-0.22 * h, -0.30 * h), KC(-0.2 * h, -0.20 * h)], True), rim=0.8)
    # gövde (gecelik), yaslanmış
    F.fill(sp([KC(-0.065 * h, -0.52 * h), (-0.115 * h, -0.48 * h), (-0.115 * h, -0.38 * h), (-0.09 * h, -0.28 * h), KC(0.09 * h, -0.28 * h), (0.095 * h, -0.36 * h), (0.095 * h, -0.45 * h), (0.07 * h, -0.52 * h)], True), rim=0.9, glow=0.10)
    # battaniye: dizlerde tepe, ayaklara inen
    F.fill(sp([KC(0.0 * h, -0.30 * h), (0.10 * h, -0.34 * h), (0.22 * h, -0.28 * h), (0.34 * h, -0.30 * h), (0.46 * h, -0.20 * h), (0.52 * h, -0.10 * h), KC(0.50 * h, 0.0), KC(-0.20 * h, 0.0), KC(-0.22 * h, -0.20 * h), (-0.12 * h, -0.28 * h)], True, 0.95), rim=0.9, glow=0.08)
    for (a, b, c, d) in ((0.06, -0.31, 0.10, -0.02), (0.18, -0.30, 0.22, -0.02), (0.30, -0.29, 0.36, -0.03), (0.42, -0.22, 0.46, -0.03)):
        F.crease((a * h, b * h), (c * h, d * h), 0.01 * h, 0.01 * h, alpha=0.6)
    F.line(sp([(-0.19 * h, -0.20 * h), (-0.05 * h, -0.31 * h), (0.10 * h, -0.34 * h), (0.24 * h, -0.285 * h), (0.36 * h, -0.30 * h)], False), h * 0.005, tone=1.0, alpha=0.5)    # battaniye kıvrık üst kenarı
    # kollar: biri battaniyede, diğeri tespih/bardak
    add_arm(F, [(-0.03 * h, -0.49 * h), (0.04 * h, -0.40 * h), (0.13 * h, -0.355 * h)], [0.05 * h, 0.048 * h, 0.034 * h], hand="open", hand_len=0.06 * h, hand_rot=20)
    add_arm(F, [(0.02 * h, -0.50 * h), (0.10 * h, -0.45 * h), (0.15 * h, -0.50 * h)], [0.046 * h, 0.044 * h, 0.032 * h], hand="fist", hand_len=0.055 * h, hand_rot=-40)
    F.fill(sp([KC(0.16 * h, -0.55 * h), (0.19 * h, -0.55 * h), (0.185 * h, -0.49 * h), KC(0.165 * h, -0.49 * h)], True), rim=1.0)
    # baş: gece takkesi, sakal, hafif geriye yaslı
    add_head(F, hx, hy, hh, "o", rot=-6, beard="short", hat="coif", nose=1.2, chin=0.04, neck_to=(-0.01 * h, -0.52 * h), neck_w=(0.5, 0.72), hat_rot=-4)
    return F.build()


# ───────────────────────────── coffin (tabut: yan görünüş, çapraz işli kapak, sehpada) ─────────────────────────────
@fx("coffin")
def _coffin(h, lean):
    F = Fig(h, lean)
    L = 1.9 * h
    x0, x1 = -L / 2, L / 2
    ht = 0.34 * h
    # sehpa/bier (ayaklı, örtülü)
    F.fill(sp([KC(x0 + 0.06 * h, -0.30 * h), KC(x1 - 0.02 * h, -0.30 * h), (x1 - 0.04 * h, -0.14 * h), KC(x1 - 0.10 * h, 0.0), KC(x0 + 0.12 * h, 0.0), (x0 + 0.08 * h, -0.14 * h)], True, 0.8), rim=0.8)
    for xx in (x0 + 0.14 * h, x1 - 0.14 * h):
        F.fill(bar(xx, -0.05 * h, xx, 0.0, 0.05 * h, 0.07 * h), rim=0.7)
    for k in range(7):
        xx = x0 + 0.18 * h + k * (L - 0.36 * h) / 6
        F.crease((xx, -0.28 * h), (xx + 0.01 * h, -0.03 * h), 0.008 * h, 0.006 * h, alpha=0.5)
    # tabut gövdesi: omuz tarafı (sağ) geniş, ayak (sol) dar — altıgen yan kesit
    top_y = -0.30 * h - ht
    F.fill(sp([KC(x0 + 0.02 * h, -0.30 * h - 0.18 * h), KC(x0 + 0.26 * h, top_y + 0.06 * h), KC(x1 - 0.50 * h, top_y), KC(x1 - 0.12 * h, top_y - 0.015 * h), KC(x1 + 0.02 * h, -0.30 * h - 0.20 * h),
               KC(x1, -0.30 * h), KC(x0 + 0.04 * h, -0.30 * h)], True, 0.5), rim=1.0, glow=0.10)
    # kapak (üst yüz) eğimli ince şerit
    F.fill(sp([KC(x0 + 0.30 * h, top_y + 0.05 * h), KC(x1 - 0.50 * h, top_y - 0.02 * h), KC(x1 - 0.10 * h, top_y - 0.035 * h), KC(x1 - 0.14 * h, top_y + 0.02 * h), KC(x1 - 0.50 * h, top_y + 0.03 * h), KC(x0 + 0.32 * h, top_y + 0.09 * h)], True, 0.5), rim=1.0, tone=0.08, bound=False)
    # haç (açık ton) + kenar süsü
    cx_, cy_ = (x0 + x1) / 2 + 0.12 * h, top_y + 0.17 * h
    F.line(poly([(cx_, cy_ - 0.10 * h), (cx_, cy_ + 0.10 * h)], False), h * 0.012, tone=1.0, alpha=0.5, cap="butt")
    F.line(poly([(cx_ - 0.06 * h, cy_ - 0.04 * h), (cx_ + 0.06 * h, cy_ - 0.04 * h)], False), h * 0.012, tone=1.0, alpha=0.5, cap="butt")
    F.line(poly([(x0 + 0.06 * h, -0.30 * h - 0.16 * h), (x0 + 0.28 * h, top_y + 0.10 * h), (x1 - 0.50 * h, top_y + 0.07 * h), (x1 - 0.10 * h, top_y + 0.06 * h), (x1 - 0.03 * h, -0.30 * h - 0.18 * h)], False), h * 0.006, tone=1.0, alpha=0.45)
    for xx in (-0.55, -0.25, 0.05, 0.35, 0.65):
        F.fill(ell(xx * h, -0.30 * h - 0.065 * h, 0.012 * h, 0.012 * h), rim=0.0, tone=1.0, alpha=0.6, bound=False)
    return F.build()


# ───────────────────────────── inca_noble ─────────────────────────────
def _tocapu_band(F, h, x0, x1, y0, y1, n=7, alpha=0.38):
    """Bir bant boyunca satranç/tocapu desenli açık-ton kareler."""
    sx = (x1 - x0) / n
    rows = 2
    sy = (y1 - y0) / rows
    for r in range(rows):
        for c in range(n):
            if (r + c) % 2 == 0:
                F.fill(poly([((x0 + c * sx) * h, (y0 + r * sy) * h), ((x0 + (c + 1) * sx) * h, (y0 + r * sy) * h), ((x0 + (c + 1) * sx) * h, (y0 + (r + 1) * sy) * h), ((x0 + c * sx) * h, (y0 + (r + 1) * sy) * h)]),
                       rim=0.0, tone=1.0, alpha=alpha, bound=False)


@fx("inca_noble")
def _inca_noble(h, lean):
    F = Fig(h, lean)
    hh = 0.13 * h
    hx, hy = 0.04 * h, -0.915 * h + 0.5 * hh
    # tören asası: düz, üstünde disk ve tüy
    F.fill(bar(0.17 * h, 0.0, 0.18 * h, -1.0 * h, 0.014 * h, 0.012 * h, False, True), rim=0.9)
    F.fill(ell(0.182 * h, -1.03 * h, 0.032 * h, 0.032 * h), rim=1.0)
    F.fill(feather_path(0.18 * h, -1.05 * h, 0.20 * h, -1.14 * h, 0.03 * h, bend=0.01 * h), rim=1.0)
    # bacaklar: çıplak, sandaletli
    for (a, b, c, rim) in (((-0.02, -0.40), (-0.05, -0.22), (-0.085, -0.03), 0.7), ((0.035, -0.40), (0.075, -0.23), (0.11, -0.03), 0.9)):
        F.fill(limb([(a[0] * h, a[1] * h), (b[0] * h, b[1] * h), (c[0] * h, c[1] * h)], [0.07 * h, 0.048 * h, 0.03 * h], cap0=0.3, cap1=0.3), rim=rim)
        F.fill(sp([KC((c[0] - 0.02) * h, (c[1]) * h), ((c[0] + 0.05) * h, (c[1] - 0.004) * h), KC((c[0] + 0.07) * h, 0.0), KC((c[0] - 0.03) * h, 0.0)], True, 0.8), rim=rim)
    # yacolla (omuzdan geriye düşen mantı)
    F.fill(sp([KC(-0.045 * h, -0.775 * h), (-0.11 * h, -0.745 * h), (-0.13 * h, -0.62 * h), (-0.135 * h, -0.50 * h), (-0.13 * h, -0.38 * h), KC(-0.09 * h, -0.34 * h), (-0.06 * h, -0.45 * h), (-0.05 * h, -0.62 * h)], True), rim=0.9)
    F.crease((-0.095 * h, -0.70 * h), (-0.115 * h, -0.40 * h), 0.008 * h, 0.01 * h, alpha=0.55)
    # unku: kolsuz, diz boyu tunik; kemer bandı + etek şeridi tocapu
    F.fill(sp([KC(-0.04 * h, -0.775 * h), (-0.10 * h, -0.745 * h), (-0.10 * h, -0.64 * h), (-0.095 * h, -0.53 * h), KC(-0.11 * h, -0.34 * h), KC(0.105 * h, -0.34 * h), (0.09 * h, -0.53 * h), (0.10 * h, -0.64 * h), (0.095 * h, -0.745 * h), (0.045 * h, -0.775 * h)], True, 0.95), rim=0.9, glow=0.10)
    _tocapu_band(F, h, -0.10, 0.10, -0.595, -0.555, 8, 0.40)
    _tocapu_band(F, h, -0.108, 0.103, -0.385, -0.345, 9, 0.40)
    F.line(poly([(-0.10 * h, -0.60 * h), (0.10 * h, -0.60 * h)], False), h * 0.003, tone=1.0, alpha=0.5)
    F.line(poly([(-0.10 * h, -0.55 * h), (0.10 * h, -0.55 * h)], False), h * 0.003, tone=1.0, alpha=0.5)
    F.crease((-0.04 * h, -0.52 * h), (-0.05 * h, -0.39 * h), 0.006 * h, 0.004 * h, alpha=0.5)
    # kollar: biri asada, diğeri göğüste; bilezikler
    add_arm(F, [(0.045 * h, -0.725 * h), (0.11 * h, -0.62 * h), (0.172 * h, -0.60 * h)], [0.052 * h, 0.05 * h, 0.04 * h], hand="fist", hand_len=0.06 * h, hand_rot=5)
    add_arm(F, [(-0.03 * h, -0.725 * h), (-0.085 * h, -0.64 * h), (0.0 * h, -0.60 * h)], [0.052 * h, 0.052 * h, 0.04 * h], hand="open", hand_len=0.058 * h, hand_rot=0)
    F.line(poly([(0.125 * h, -0.60 * h), (0.14 * h, -0.605 * h)], False), h * 0.006, tone=1.0, alpha=0.7)
    # baş: llautu bandı, saçak, tüyler; büyük kulak diski
    add_head(F, hx, hy, hh, "m", rot=-2, hair="bob", hat="llauto", neck_to=(0.0, -0.775 * h), nose=1.12, hat_rot=0)
    F.fill(ell(hx - 0.01 * hh, hy + 0.06 * hh, 0.10 * hh, 0.10 * hh), rim=1.0, tone=0.45)
    F.fill(ell(hx - 0.01 * hh, hy + 0.06 * hh, 0.05 * hh, 0.05 * hh), rim=0.0, tone=1.0, alpha=0.5, bound=False)
    return F.build()


# ───────────────────────────── aztec_warrior ─────────────────────────────
@fx("aztec_warrior")
def _aztec_warrior(h, lean):
    F = Fig(h, lean)
    hh = 0.13 * h
    hx, hy = 0.045 * h, -0.915 * h + 0.5 * hh
    # sırtta tüy standardı (arka süs): dik, düzenli yelpaze + merkez disk
    for k in range(9):
        a = -0.95 + k * 0.2375
        ex, ey = -0.08 * h + math.sin(a) * 0.20 * h, -0.70 * h - math.cos(a) * 0.27 * h
        F.fill(feather_path(-0.08 * h, -0.64 * h, ex, ey, 0.045 * h, bend=0.0, barbs=False), rim=0.9)
    F.fill(ell(-0.08 * h, -0.64 * h, 0.058 * h, 0.058 * h), rim=1.0, tone=0.25)
    F.fill(ell(-0.08 * h, -0.64 * h, 0.03 * h, 0.03 * h), rim=0.0, tone=1.0, alpha=0.45, bound=False)
    # bacaklar (çıplak, sandaletli), maxtlatl uçları
    for (a, b, c, rim) in (((-0.02, -0.42), (-0.05, -0.23), (-0.09, -0.03), 0.7), ((0.04, -0.42), (0.08, -0.24), (0.12, -0.03), 0.9)):
        F.fill(limb([(a[0] * h, a[1] * h), (b[0] * h, b[1] * h), (c[0] * h, c[1] * h)], [0.074 * h, 0.05 * h, 0.032 * h], cap0=0.3, cap1=0.3), rim=rim)
        F.fill(sp([KC((c[0] - 0.02) * h, (c[1]) * h), ((c[0] + 0.05) * h, (c[1] - 0.004) * h), KC((c[0] + 0.07) * h, 0.0), KC((c[0] - 0.03) * h, 0.0)], True, 0.8), rim=rim)
    F.fill(sp([KC(-0.045 * h, -0.46 * h), (-0.05 * h, -0.36 * h), (-0.045 * h, -0.27 * h), KC(0.0, -0.26 * h), KC(0.04 * h, -0.27 * h), (0.055 * h, -0.36 * h), KC(0.05 * h, -0.46 * h)], True), rim=0.9)
    _tocapu_band(F, h, -0.047, 0.052, -0.305, -0.27, 4, 0.5)
    # ichcahuipilli (kapitone pamuk zırh): kısa tunik, süslü kenar
    F.fill(sp([KC(-0.04 * h, -0.775 * h), (-0.105 * h, -0.745 * h), (-0.108 * h, -0.64 * h), (-0.095 * h, -0.54 * h), KC(-0.12 * h, -0.43 * h), KC(0.125 * h, -0.43 * h), (0.098 * h, -0.54 * h), (0.112 * h, -0.64 * h), (0.10 * h, -0.745 * h), (0.05 * h, -0.775 * h)], True, 0.95), rim=0.9, glow=0.10)
    for k in range(5):
        F.line(poly([(-0.10 * h, (-0.72 + k * 0.05) * h), (0.105 * h, (-0.72 + k * 0.05) * h)], False), h * 0.003, tone=1.0, alpha=0.30)
    _tocapu_band(F, h, -0.118, 0.12, -0.46, -0.425, 10, 0.45)
    # macuahuitl: önde dik tutulan obsidyen dişli tahta kılıç (uzak kol)
    mx0, my0, mx1, my1 = 0.185, -0.50, 0.235, -1.02
    F.fill(bar(mx0 * h, my0 * h, mx1 * h, my1 * h, 0.034 * h, 0.05 * h, True, True), rim=1.0)
    for k in range(9):
        u = 0.22 + k * 0.085
        cx_, cy_ = (mx0 + (mx1 - mx0) * u) * h, (my0 + (my1 - my0) * u) * h
        F.fill(poly([(cx_ + 0.012 * h, cy_ - 0.012 * h), (cx_ + 0.04 * h, cy_ + 0.002 * h), (cx_ + 0.012 * h, cy_ + 0.016 * h)]), rim=1.0)
    add_arm(F, [(0.05 * h, -0.72 * h), (0.12 * h, -0.64 * h), (0.19 * h, -0.575 * h)], [0.055 * h, 0.052 * h, 0.04 * h], hand="fist", hand_len=0.06 * h, hand_rot=-25)
    # yuvarlak kalkan (chimalli): yakın kolda gövde önünde; tüy saçaklı
    sx_, sy_, sr = 0.02 * h, -0.55 * h, 0.115 * h
    for k in range(14):
        a = math.pi * 0.10 + k * math.pi * 0.135
        F.fill(feather_path(sx_ + math.cos(a) * sr * 0.95, sy_ + math.sin(a) * sr * 0.95, sx_ + math.cos(a) * sr * 1.30, sy_ + math.sin(a) * sr * 1.30, 0.03 * h, barbs=False), rim=0.9)
    F.fill(ell(sx_, sy_, sr, sr), rim=1.0, glow=0.08)
    F.line(sp([(sx_ - sr * 0.72, sy_), (sx_, sy_ - sr * 0.72), (sx_ + sr * 0.72, sy_), (sx_, sy_ + sr * 0.72), (sx_ - sr * 0.72, sy_)], False), h * 0.004, tone=1.0, alpha=0.6)
    F.fill(ell(sx_, sy_, sr * 0.34, sr * 0.34), rim=0.0, tone=1.0, alpha=0.4, bound=False)
    F.fill(ell(sx_, sy_, sr * 0.16, sr * 0.16), rim=0.0, tone=0.0, alpha=1.0, bound=False)
    add_arm(F, [(-0.02 * h, -0.725 * h), (-0.07 * h, -0.64 * h), (-0.04 * h, -0.57 * h)], [0.058 * h, 0.058 * h, 0.042 * h], hand=None)
    F.line(poly([(-0.045 * h, -0.64 * h), (-0.06 * h, -0.66 * h)], False), h * 0.006, tone=1.0, alpha=0.7)
    # baş: tüy tacı, alın bandı; dik duruş
    add_head(F, hx, hy, hh, "m", rot=-5, hair="long", hat="crest", neck_to=(0.0, -0.775 * h), nose=1.1, hat_rot=0)
    return F.build()


# ───────────────────────────── arquebusier (fitilli tüfekli) ─────────────────────────────
@fx("arquebusier")
def _arquebusier(h, lean):
    F = Fig(h, lean)
    hh = 0.13 * h
    hx, hy = 0.05 * h, -0.925 * h + 0.5 * hh
    # arkebüz: omuzda, namlu öne-yukarı; dipçik geride omuz altında
    bx0, by0, bx1, by1 = -0.09, -0.60, 0.60, -1.22
    F.fill(bar(bx0 * h, by0 * h, bx1 * h, by1 * h, 0.028 * h, 0.016 * h, True, False), rim=0.9)
    F.fill(sp([KC(-0.19 * h, -0.55 * h), (-0.14 * h, -0.62 * h), (-0.07 * h, -0.62 * h), (-0.03 * h, -0.60 * h), (-0.07 * h, -0.575 * h), (-0.12 * h, -0.555 * h)], True), rim=0.9)
    F.fill(sp([KC(0.04 * h, -0.67 * h), (0.07 * h, -0.70 * h), (0.095 * h, -0.685 * h), (0.075 * h, -0.655 * h)], True), rim=1.0)       # fitil mekanizması
    # fitil: yanan uç
    F.line(sp([(0.08 * h, -0.685 * h), (0.14 * h, -0.64 * h), (0.15 * h, -0.55 * h), (0.13 * h, -0.45 * h)], False), h * 0.0035, tone=0.6, alpha=0.85)
    F.solid(ell(0.13 * h, -0.45 * h, 0.006 * h, 0.006 * h), "#FFD27A", 1.0, bound=True)
    F.glowdot(0.13 * h, -0.45 * h, 0.045 * h, "#FFB347", 0.95)
    add_leg(F, h, (-0.03, -0.45), (-0.065, -0.265), (-0.10, -0.046), (0.074, 0.048, 0.032), 1, "round", 0.09, 0.7)
    add_leg(F, h, (0.03, -0.45), (0.075, -0.265), (0.115, -0.046), (0.08, 0.05, 0.034), 1, "round", 0.095, 0.9)
    F.fill(sp([KC(-0.09 * h, -0.50 * h), (-0.12 * h, -0.43 * h), (-0.10 * h, -0.345 * h), (-0.01 * h, -0.325 * h), (0.07 * h, -0.34 * h), (0.125 * h, -0.38 * h), (0.12 * h, -0.45 * h), KC(0.095 * h, -0.50 * h)], True), rim=0.9)
    for x in (-0.06, -0.02, 0.03, 0.08):
        F.crease((x * h, -0.48 * h), ((x + 0.005) * h, -0.35 * h), 0.006 * h, 0.004 * h, alpha=0.5)
    torso(F, h, back=-0.108, front=0.104, chest=(-0.112, 0.112, -0.655), waist=(-0.085, 0.092, -0.53), hem=(-0.11, 0.115, -0.47))
    # bandolier: omuzdan çapraz kayış + barut tüpleri
    F.line(poly([(-0.07 * h, -0.76 * h), (0.095 * h, -0.50 * h)], False), h * 0.012, tone=0.35, alpha=0.85)
    for k in range(8):
        u = 0.1 + k * 0.11
        x, y = -0.07 + 0.165 * u * 1.0, -0.76 + 0.26 * u
        F.fill(bar(x * h, y * h, (x + 0.012) * h, (y + 0.04) * h, 0.011 * h, 0.011 * h, True, True), rim=0.9, bound=False)
    F.fill(fur_band([(-0.045 * h, -0.775 * h), (0.0, -0.787 * h), (0.055 * h, -0.775 * h)], 0.024 * h, 0.011 * h, side=1, jag=0.8), rim=1.0)
    # kollar: biri arkebüzü tutar (ön), diğeri dipçiği kavrar
    add_arm(F, [(0.05 * h, -0.725 * h), (0.12 * h, -0.65 * h), (0.19 * h, -0.775 * h)], [0.058 * h, 0.056 * h, 0.042 * h], hand="fist", hand_len=0.06 * h, hand_rot=-55)
    add_arm(F, [(-0.035 * h, -0.73 * h), (-0.115 * h, -0.62 * h), (-0.05 * h, -0.59 * h)], [0.064 * h, 0.07 * h, 0.044 * h], hand="fist", hand_len=0.064 * h, hand_rot=-10)
    add_head(F, hx, hy, hh, "m", rot=-2, beard="point", hat="slouch", nose=1.1, neck_to=(0.0, -0.775 * h), hat_rot=4)
    return F.build()


# ───────────────────────────── halberdier ─────────────────────────────
@fx("halberdier")
def _halberdier(h, lean):
    F = Fig(h, lean)
    hh = 0.13 * h
    hx, hy = 0.05 * h, -0.925 * h + 0.5 * hh
    px = 0.185
    # alebard: gövde + üstte mızrak ucu, balta bıçağı (ön), kanca (arka)
    top = -1.60
    F.fill(bar(px * h, 0.0, (px + 0.008) * h, top * h, 0.013 * h, 0.011 * h), rim=0.9)
    tx, ty = (px + 0.008) * h, top * h
    F.fill(sp([KC(tx - 0.011 * h, ty + 0.005 * h), (tx - 0.014 * h, ty - 0.06 * h), KC(tx, ty - 0.15 * h), (tx + 0.014 * h, ty - 0.06 * h), KC(tx + 0.011 * h, ty + 0.005 * h)], True), rim=1.0)
    F.fill(sp([KC(tx + 0.008 * h, ty + 0.01 * h), (tx + 0.07 * h, ty + 0.008 * h), (tx + 0.095 * h, ty + 0.06 * h), (tx + 0.075 * h, ty + 0.11 * h), (tx + 0.03 * h, ty + 0.115 * h), KC(tx + 0.008 * h, ty + 0.095 * h)], True, 0.9), rim=1.0)
    F.fill(sp([KC(tx - 0.008 * h, ty + 0.03 * h), (tx - 0.05 * h, ty + 0.045 * h), (tx - 0.075 * h, ty + 0.075 * h), (tx - 0.05 * h, ty + 0.07 * h), KC(tx - 0.008 * h, ty + 0.06 * h)], True), rim=0.9)
    # kılıç kalçada
    F.fill(bar(-0.04 * h, -0.49 * h, -0.20 * h, -0.30 * h, 0.014 * h, 0.009 * h, True, True), rim=0.9)
    add_leg(F, h, (-0.025, -0.44), (-0.06, -0.26), (-0.095, -0.046), (0.075, 0.048, 0.032), 1, "round", 0.09, 0.7)
    add_leg(F, h, (0.035, -0.44), (0.075, -0.265), (0.115, -0.046), (0.08, 0.05, 0.034), 1, "round", 0.095, 0.9)
    F.fill(sp([KC(-0.09 * h, -0.50 * h), (-0.12 * h, -0.43 * h), (-0.10 * h, -0.345 * h), (-0.01 * h, -0.325 * h), (0.07 * h, -0.34 * h), (0.125 * h, -0.38 * h), (0.12 * h, -0.45 * h), KC(0.095 * h, -0.50 * h)], True), rim=0.9)
    for x in (-0.06, -0.02, 0.03, 0.08):
        F.crease((x * h, -0.48 * h), ((x + 0.005) * h, -0.35 * h), 0.006 * h, 0.004 * h, alpha=0.5)
    torso(F, h, back=-0.108, front=0.106, chest=(-0.112, 0.116, -0.655), waist=(-0.085, 0.094, -0.53), hem=(-0.11, 0.115, -0.47))
    F.line(sp([(0.02 * h, -0.755 * h), (0.05 * h, -0.62 * h), (0.03 * h, -0.50 * h)], False), h * 0.005, tone=1.0, alpha=0.5)
    F.fill(sp([(-0.115 * h, -0.755 * h), (-0.07 * h, -0.792 * h), (0.0, -0.79 * h), (0.02 * h, -0.74 * h), (-0.04 * h, -0.70 * h), (-0.115 * h, -0.70 * h)], True), rim=1.0)
    add_arm(F, [(-0.03 * h, -0.725 * h), (-0.04 * h, -0.60 * h), (0.10 * h, -0.55 * h)], [0.066 * h, 0.06 * h, 0.044 * h], hand="fist", hand_len=0.066 * h, hand_rot=-5)
    add_arm(F, [(0.045 * h, -0.725 * h), (0.11 * h, -0.67 * h), (0.18 * h, -0.70 * h)], [0.056 * h, 0.055 * h, 0.04 * h], hand="fist", hand_len=0.062 * h, hand_rot=-5)
    add_head(F, hx, hy, hh, "m", rot=-1, beard="stache", hat="sallet", nose=1.12, neck_to=(0.0, -0.775 * h), hat_rot=2)
    return F.build()


# ───────────────────────────── crowd_a…f (düşük ayrıntı, çeşitli kalabalık dolgusu) ─────────────────────────────
def _crowd(h, lean, kind):
    F = Fig(h, lean)
    hh = 0.135 * h
    hx, hy = 0.04 * h, -0.925 * h + 0.5 * hh
    if kind == "a":                     # kasketli adam, kısa pelerin, çorap bacak
        add_leg(F, h, (-0.02, -0.44), (-0.055, -0.25), (-0.09, -0.046), (0.07, 0.046, 0.03), 1, "round", 0.085, 0.7)
        add_leg(F, h, (0.035, -0.44), (0.075, -0.26), (0.11, -0.046), (0.074, 0.048, 0.032), 1, "round", 0.09, 0.8)
        F.fill(sp([KC(-0.04 * h, -0.775 * h), (-0.12 * h, -0.74 * h), (-0.15 * h, -0.60 * h), (-0.16 * h, -0.45 * h), KC(0.115 * h, -0.42 * h), (0.10 * h, -0.55 * h), (0.11 * h, -0.70 * h), (0.05 * h, -0.775 * h)], True), rim=0.9, glow=0.08)
        F.crease((-0.06 * h, -0.70 * h), (-0.09 * h, -0.45 * h), 0.008 * h, 0.006 * h)
        add_head(F, hx, hy, hh, "m", rot=2, hat="flatcap", neck_to=(0.0, -0.775 * h), hat_rot=3, beard=None)
    elif kind == "b":                   # peçeli kadın, uzun elbise
        F.fill(robe_path(h, sh_y=-0.74, nb_y=-0.765, back_sh=-0.09, front_sh=0.085, chest=(-0.10, 0.09, -0.66), waist=(-0.075, 0.07, -0.54), hip=(-0.16, 0.16, -0.34), hem=(-0.22, 0.21, -0.012), nfold=3, amp=0.007, lift=0.012), rim=0.9, glow=0.08)
        robe_folds(F, h, -0.05, 0.05, -0.54, -0.03, 5, 0.01, bend=0.01, seed=71)
        add_arm(F, [(-0.02 * h, -0.72 * h), (-0.06 * h, -0.62 * h), (0.05 * h, -0.55 * h)], [0.05 * h, 0.05 * h, 0.036 * h], hand=None)
        add_head(F, hx, hy, hh * 0.96, "f", rot=3, hat="veil", hair="bun", neck_to=(0.0, -0.765 * h), neck_w=(0.42, 0.6), hat_rot=0)
    elif kind == "c":                   # geniş şapkalı adam, uzun palto
        F.fill(robe_path(h, sh_y=-0.745, nb_y=-0.77, back_sh=-0.11, front_sh=0.10, chest=(-0.12, 0.108, -0.65), waist=(-0.10, 0.098, -0.50), hip=(-0.14, 0.14, -0.30), hem=(-0.185, 0.18, -0.15), nfold=3, amp=0.006, lift=0.01), rim=0.9, glow=0.08)
        F.fill(limb([(-0.03 * h, -0.17 * h), (-0.025 * h, -0.08 * h), (-0.02 * h, -0.02 * h)], [0.08 * h, 0.065 * h, 0.055 * h], cap0=0.0, cap1=0.2), rim=0.7)
        F.fill(limb([(0.07 * h, -0.17 * h), (0.10 * h, -0.08 * h), (0.115 * h, -0.02 * h)], [0.08 * h, 0.065 * h, 0.055 * h], cap0=0.0, cap1=0.2), rim=0.8)
        F.fill(shoe(-0.035 * h, 0, 0.09 * h, 0.03 * h, 1, "round"), rim=0.7)
        F.fill(shoe(0.095 * h, 0, 0.09 * h, 0.03 * h, 1, "round"), rim=0.8)
        add_arm(F, [(-0.03 * h, -0.73 * h), (-0.11 * h, -0.62 * h), (-0.04 * h, -0.52 * h)], [0.064 * h, 0.068 * h, 0.044 * h], hand="fist", hand_len=0.06 * h, hand_rot=10)
        add_head(F, hx, hy, hh, "m", rot=-1, hat="slouch", beard="short", neck_to=(0.0, -0.77 * h), hat_rot=3)
    elif kind == "d":                   # kukuletalı yoksul/keşiş
        F.fill(robe_path(h, sh_y=-0.74, nb_y=-0.765, back_sh=-0.12, front_sh=0.105, chest=(-0.13, 0.11, -0.64), waist=(-0.11, 0.104, -0.50), hip=(-0.16, 0.155, -0.30), hem=(-0.215, 0.2, -0.012), nfold=3, amp=0.008, lift=0.012), rim=0.9, glow=0.08)
        robe_folds(F, h, -0.06, 0.06, -0.50, -0.03, 5, 0.01, bend=0.01, seed=72)
        add_arm(F, [(-0.03 * h, -0.72 * h), (-0.09 * h, -0.62 * h), (0.07 * h, -0.55 * h)], [0.066 * h, 0.07 * h, 0.048 * h], hand=None)
        add_head(F, hx, hy, hh, "m", rot=10, hat="cowl", beard="short", neck_to=(0.01 * h, -0.765 * h), hat_rot=0)
    elif kind == "e":                   # miğferli asker, göğüslük, kısa asa
        F.fill(bar(0.17 * h, 0.0, 0.18 * h, -1.05 * h, 0.012 * h, 0.01 * h), rim=0.9)
        add_leg(F, h, (-0.025, -0.44), (-0.06, -0.26), (-0.095, -0.046), (0.074, 0.048, 0.032), 1, "round", 0.09, 0.7)
        add_leg(F, h, (0.035, -0.44), (0.075, -0.265), (0.115, -0.046), (0.08, 0.05, 0.034), 1, "round", 0.095, 0.9)
        F.fill(sp([KC(-0.09 * h, -0.50 * h), (-0.12 * h, -0.43 * h), (-0.10 * h, -0.345 * h), (0.0, -0.325 * h), (0.095 * h, -0.34 * h), (0.125 * h, -0.43 * h), KC(0.10 * h, -0.50 * h)], True), rim=0.9)
        torso(F, h, back=-0.108, front=0.104, chest=(-0.112, 0.112, -0.655), waist=(-0.085, 0.092, -0.53), hem=(-0.11, 0.115, -0.49))
        add_arm(F, [(0.045 * h, -0.725 * h), (0.11 * h, -0.66 * h), (0.172 * h, -0.64 * h)], [0.056 * h, 0.055 * h, 0.04 * h], hand="fist", hand_len=0.06 * h, hand_rot=-3)
        add_head(F, hx, hy, hh, "m", rot=0, hat="morion", beard="short", neck_to=(0.0, -0.775 * h), hat_rot=1)
    else:                               # f: baretli soylu, kürk yakalı uzun cüppe
        F.fill(robe_path(h, sh_y=-0.745, nb_y=-0.768, back_sh=-0.116, front_sh=0.106, chest=(-0.122, 0.108, -0.65), waist=(-0.10, 0.097, -0.50), hip=(-0.15, 0.15, -0.31), hem=(-0.205, 0.2, -0.012), nfold=3, amp=0.007, lift=0.02), rim=0.9, glow=0.08)
        robe_folds(F, h, -0.06, 0.06, -0.50, -0.03, 5, 0.01, bend=0.01, seed=73)
        F.fill(fur_band([(-0.116 * h, -0.716 * h), (-0.10 * h, -0.757 * h), (-0.04 * h, -0.78 * h), (0.05 * h, -0.78 * h), (0.10 * h, -0.757 * h), (0.11 * h, -0.716 * h)], 0.05 * h, 0.018 * h, side=1), rim=1.0)
        add_arm(F, [(-0.035 * h, -0.73 * h), (-0.12 * h, -0.62 * h), (-0.045 * h, -0.508 * h)], [0.07 * h, 0.078 * h, 0.05 * h], hand="fist", hand_len=0.06 * h, hand_rot=8)
        add_head(F, hx, hy, hh, "m", rot=-2, hat="beret", beard="point", neck_to=(0.0, -0.768 * h), hat_rot=7)
    return F.build()


for _k in "abcdef":
    fx("crowd_" + _k)((lambda kk: (lambda h, lean: _crowd(h, lean, kk)))(_k))


# ───────────────────────────── BONUS türler: torchbearer (meşaleci), standard_bearer (sancaktar), litter (sedye/tahtırevan) ─────────────────────────────
def _flame(F, x, y, s, glow=0.34, h=None):
    """Meşale/mum alevi: sıcak parlama (toplamsal) + damla biçimli açık alev gövdesi."""
    F.fill(sp([KC(x, y + 0.02 * s), (x - 0.035 * s, y - 0.02 * s), (x - 0.03 * s, y - 0.07 * s), (x, y - 0.14 * s), (x + 0.03 * s, y - 0.07 * s), (x + 0.035 * s, y - 0.02 * s)], True, 0.9), rim=0.0, tone=0.0, alpha=0.0, bound=True)
    F.solid(sp([KC(x, y + 0.02 * s), (x - 0.034 * s, y - 0.02 * s), (x - 0.028 * s, y - 0.07 * s), (x + 0.004 * s, y - 0.15 * s), (x + 0.03 * s, y - 0.07 * s), (x + 0.034 * s, y - 0.02 * s)], True, 0.9), "#FFE7A8", 0.98)
    F.solid(sp([KC(x, y + 0.012 * s), (x - 0.018 * s, y - 0.015 * s), (x, y - 0.075 * s), (x + 0.018 * s, y - 0.015 * s)], True, 0.9), "#FFB347", 0.9)
    F.glowdot(x, y - 0.05 * s, glow * s, "#FFB347", 0.95, bound=True)


@fx("torchbearer")
def _torchbearer(h, lean):
    F = Fig(h, lean)
    hh = 0.135 * h
    hx, hy = 0.05 * h, -0.915 * h + 0.5 * hh
    # meşale: yüksekte tutulan çubuk + alev (parlama sprite sınırına dahil)
    tx0, ty0, tx1, ty1 = 0.15, -0.76, 0.19, -1.12
    F.fill(bar(tx0 * h, ty0 * h, tx1 * h, ty1 * h, 0.016 * h, 0.022 * h, False, True), rim=1.0)
    F.fill(sp([KC((tx1 - 0.03) * h, (ty1 + 0.01) * h), ((tx1 - 0.035) * h, (ty1 - 0.03) * h), ((tx1 + 0.035) * h, (ty1 - 0.03) * h), KC((tx1 + 0.03) * h, (ty1 + 0.01) * h)], True), rim=1.0)
    _flame(F, tx1 * h, (ty1 - 0.03) * h, h, glow=0.30)
    add_leg(F, h, (-0.025, -0.44), (-0.06, -0.26), (-0.10, -0.046), (0.074, 0.048, 0.032), 1, "round", 0.09, 0.7)
    add_leg(F, h, (0.035, -0.44), (0.08, -0.265), (0.12, -0.046), (0.078, 0.05, 0.034), 1, "round", 0.095, 0.9)
    # kısa pelerin + dizüstü tunik
    F.fill(sp([KC(-0.04 * h, -0.775 * h), (-0.12 * h, -0.74 * h), (-0.15 * h, -0.60 * h), (-0.17 * h, -0.45 * h), KC(0.11 * h, -0.40 * h), (0.10 * h, -0.55 * h), (0.11 * h, -0.70 * h), (0.05 * h, -0.775 * h)], True), rim=0.9, glow=0.10)
    F.crease((-0.06 * h, -0.70 * h), (-0.10 * h, -0.45 * h), 0.008 * h, 0.006 * h)
    F.fill(sp([KC(-0.10 * h, -0.50 * h), (-0.12 * h, -0.43 * h), (-0.10 * h, -0.345 * h), (0.0, -0.325 * h), (0.095 * h, -0.34 * h), (0.125 * h, -0.43 * h), KC(0.11 * h, -0.50 * h)], True), rim=0.9)
    # kollar: biri meşaleyi yüksekte tutar, diğeri yanda
    add_arm(F, [(0.04 * h, -0.73 * h), (0.11 * h, -0.70 * h), (0.16 * h, -0.80 * h)], [0.058 * h, 0.056 * h, 0.04 * h], hand="fist", hand_len=0.06 * h, hand_rot=-70)
    add_arm(F, [(-0.03 * h, -0.73 * h), (-0.115 * h, -0.62 * h), (-0.06 * h, -0.51 * h)], [0.064 * h, 0.07 * h, 0.044 * h], hand="fist", hand_len=0.062 * h, hand_rot=20)
    add_head(F, hx, hy, hh, "m", rot=-4, beard="short", hat="flatcap", neck_to=(0.0, -0.775 * h), hat_rot=2, nose=1.1)
    return F.build()


@fx("standard_bearer")
def _standard_bearer(h, lean):
    F = Fig(h, lean)
    hh = 0.13 * h
    hx, hy = 0.05 * h, -0.925 * h + 0.5 * hh
    # sancak: yüksek gönderde, geniş çatal kuyruklu bayrak; üzerinde açık tonlu çapraz (Burgonya haçı) çizgileri
    px = 0.20
    top = -1.78
    F.fill(bar(px * h, 0.0, px * h, top * h, 0.016 * h, 0.013 * h), rim=0.9)
    tx, ty = px * h, top * h
    F.fill(sp([KC(tx - 0.02 * h, ty + 0.01 * h), (tx - 0.025 * h, ty - 0.05 * h), KC(tx, ty - 0.13 * h), (tx + 0.025 * h, ty - 0.05 * h), KC(tx + 0.02 * h, ty + 0.01 * h)], True), rim=1.0)
    F.fill(ell(tx, ty + 0.025 * h, 0.022 * h, 0.022 * h), rim=1.0)
    fx0, fy0 = tx + 0.012 * h, ty + 0.06 * h
    fw, fh = 0.62 * h, 0.40 * h
    F.fill(sp([KC(fx0, fy0), (fx0 + fw * 0.35, fy0 + 0.018 * h), (fx0 + fw * 0.72, fy0 - 0.008 * h), KC(fx0 + fw, fy0 + 0.004 * h), (fx0 + fw * 0.86, fy0 + fh * 0.5), KC(fx0 + fw, fy0 + fh), (fx0 + fw * 0.72, fy0 + fh * 1.02),
               (fx0 + fw * 0.35, fy0 + fh * 0.98), KC(fx0, fy0 + fh)], True, 0.8), rim=1.0, glow=0.06)
    F.line(poly([(fx0 + 0.03 * h, fy0 + 0.04 * h), (fx0 + fw * 0.80, fy0 + fh * 0.92)], False), h * 0.022, tone=1.0, alpha=0.5, cap="butt")
    F.line(poly([(fx0 + 0.03 * h, fy0 + fh - 0.04 * h), (fx0 + fw * 0.80, fy0 + fh * 0.08)], False), h * 0.022, tone=1.0, alpha=0.5, cap="butt")
    F.line(sp([(fx0 + 0.015 * h, fy0 + 0.01 * h), (fx0 + fw * 0.34, fy0 + 0.03 * h), (fx0 + fw * 0.72, fy0 + 0.005 * h), (fx0 + fw * 0.97, fy0 + 0.012 * h)], False), h * 0.004, tone=1.0, alpha=0.5)
    # asker: bacaklar, pantolon, zırh yeleği
    add_leg(F, h, (-0.025, -0.45), (-0.06, -0.26), (-0.095, -0.046), (0.074, 0.048, 0.032), 1, "round", 0.09, 0.7)
    add_leg(F, h, (0.035, -0.45), (0.075, -0.265), (0.115, -0.046), (0.08, 0.05, 0.034), 1, "round", 0.095, 0.9)
    F.fill(sp([KC(-0.09 * h, -0.50 * h), (-0.12 * h, -0.43 * h), (-0.10 * h, -0.345 * h), (0.0, -0.325 * h), (0.095 * h, -0.34 * h), (0.125 * h, -0.43 * h), KC(0.10 * h, -0.50 * h)], True), rim=0.9)
    torso(F, h, back=-0.108, front=0.105, chest=(-0.112, 0.112, -0.655), waist=(-0.085, 0.092, -0.53), hem=(-0.11, 0.115, -0.47))
    F.fill(sp([(-0.115 * h, -0.755 * h), (-0.07 * h, -0.792 * h), (0.0, -0.79 * h), (0.02 * h, -0.74 * h), (-0.04 * h, -0.70 * h), (-0.115 * h, -0.70 * h)], True), rim=1.0)
    add_arm(F, [(-0.03 * h, -0.725 * h), (-0.04 * h, -0.60 * h), (0.12 * h, -0.55 * h)], [0.066 * h, 0.06 * h, 0.044 * h], hand="fist", hand_len=0.066 * h, hand_rot=-5)
    add_arm(F, [(0.045 * h, -0.725 * h), (0.11 * h, -0.70 * h), (0.185 * h, -0.77 * h)], [0.056 * h, 0.055 * h, 0.04 * h], hand="fist", hand_len=0.062 * h, hand_rot=-30)
    add_head(F, hx, hy, hh, "m", rot=-2, beard="point", hat="morion", nose=1.12, neck_to=(0.0, -0.775 * h), hat_rot=1)
    return F.build()


@fx("litter")
def _litter(h, lean):
    """Sedye/tahtırevan (h = taşıyıcı boyu): iki taşıyıcı (bearer) arasında asılı örtülü kabin. Sırıklar omuz hizasında (y=−0.765h) −0.95h…+0.95h; ön taşıyıcı +0.85h'a, arka taşıyıcı −0.85h'a konur."""
    F = Fig(h, lean)
    for (x0, x1) in ((-0.98, 0.98),):
        F.fill(bar(x0 * h, -0.765 * h, x1 * h, -0.785 * h, 0.022 * h, 0.022 * h, True, True), rim=1.0)
    # askılar
    for x in (-0.40, 0.40):
        F.line(poly([(x * h, -0.775 * h), ((x * 1.0 + 0.0) * h, -0.70 * h)], False), h * 0.006, tone=0.7, alpha=0.9)
    # kabin: çatı kıvrımı + perdeli gövde + taban
    F.fill(sp([KC(-0.52 * h, -0.70 * h), (-0.50 * h, -0.66 * h), (-0.34 * h, -0.62 * h), (0.0 * h, -0.60 * h), (0.34 * h, -0.62 * h), (0.50 * h, -0.66 * h), KC(0.52 * h, -0.70 * h)], True, 0.9), rim=1.0)
    F.fill(sp([KC(-0.46 * h, -0.62 * h), (-0.48 * h, -0.40 * h), (-0.45 * h, -0.18 * h), KC(-0.40 * h, -0.14 * h), KC(0.40 * h, -0.14 * h), (0.45 * h, -0.18 * h), (0.48 * h, -0.40 * h), KC(0.46 * h, -0.62 * h)], True, 0.7), rim=1.0, glow=0.08)
    for x in (-0.30, -0.14, 0.02, 0.18, 0.34):
        F.crease((x * h, -0.60 * h), ((x + 0.01) * h, -0.17 * h), 0.012 * h, 0.01 * h, alpha=0.55)
    F.fill(sp([KC(-0.40 * h, -0.62 * h), (-0.20 * h, -0.56 * h), (0.0 * h, -0.60 * h), (0.20 * h, -0.55 * h), KC(0.40 * h, -0.62 * h)], True, 0.8), rim=0.9, tone=0.05, bound=False)
    F.fill(sp([KC(-0.42 * h, -0.14 * h), (0.0 * h, -0.10 * h), KC(0.42 * h, -0.14 * h), (0.40 * h, -0.17 * h), (0.0 * h, -0.13 * h), (-0.40 * h, -0.17 * h)], True, 0.7), rim=0.8)
    # püsküller
    for x in (-0.44, -0.22, 0.0, 0.22, 0.44):
        F.fill(ell(x * h, -0.115 * h, 0.012 * h, 0.022 * h), rim=0.8)
    # kabinde yarı açık perde: aralık (negatif alan)
    F.cut(sp([KC(0.07 * h, -0.55 * h), (0.14 * h, -0.45 * h), (0.15 * h, -0.30 * h), KC(0.12 * h, -0.22 * h), (0.09 * h, -0.30 * h), (0.075 * h, -0.45 * h)], True, 0.8))
    return F.build()
