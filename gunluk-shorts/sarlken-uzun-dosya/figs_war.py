"""figs_war — asker/silahlı/yerli figürleri (figür-lab): pikeman, landsknecht, janissary, knight, conquistador, sailor, native ve grup-2 asker türleri.
Hepsi sağa bakar; h ≈ boy (mızrak/pike h'ın 1.7 katına kadar çıkar). Araç: figs_kit, figs_parts, figs_lab.add_leg."""
import math

import skia

import stage as ST
import figs_kit as K
from figs_kit import K as KC, Fig, bar, ell, feather_path, lens, limb, place, poly, shoe, sp
from figs_parts import add_arm, add_head, add_leg, fur_band, hem_slits, robe_folds, robe_path


def fx(name):
    return ST.figx(name)


def torso(F, h, back=-0.105, front=0.10, sh=-0.745, nb=-0.775, chest=(-0.108, 0.108, -0.65), waist=(-0.085, 0.092, -0.53), hem=(-0.12, 0.125, -0.45), rim=0.9, glow=0.10):
    """Gömlek/zırh gövdesi: boyun→omuz→göğüs→bel→etek ucu (köşeli)."""
    p = sp([KC(-0.04 * h, nb * h), (back * h, sh * h), (chest[0] * h, chest[2] * h), (waist[0] * h, waist[2] * h), KC(hem[0] * h, hem[2] * h), KC(hem[1] * h, hem[2] * h),
            (waist[1] * h, waist[2] * h), (chest[1] * h, chest[2] * h), (front * h, sh * h), (0.05 * h, nb * h)], True, 0.95)
    F.fill(p, rim=rim, glow=glow)
    return p


def pike(F, h, x, top=-1.74, base=0.0, lean_x=0.0, head="leaf", w=0.0125):
    """Uzun mızrak/pike: x'te dikey (lean_x: üst uç x kayması)."""
    F.fill(bar(x * h, base * h, (x + lean_x) * h, top * h, w * h, w * h * 0.85), rim=0.9)
    tx = (x + lean_x) * h
    ty = top * h
    if head == "leaf":
        F.fill(sp([KC(tx - 0.012 * h, ty + 0.004 * h), (tx - 0.02 * h, ty - 0.03 * h), (tx, ty - 0.085 * h), (tx + 0.02 * h, ty - 0.03 * h), KC(tx + 0.012 * h, ty + 0.004 * h)], True), rim=1.0)
        F.fill(poly([(tx - 0.02 * h, ty + 0.004 * h), (tx + 0.02 * h, ty + 0.004 * h), (tx + 0.014 * h, ty + 0.018 * h), (tx - 0.014 * h, ty + 0.018 * h)]), rim=1.0)


# ───────────────────────────── landsknecht ─────────────────────────────
@fx("landsknecht")
def _landsknecht(h, lean):
    F = Fig(h, lean)
    hh = 0.13 * h
    hx, hy = 0.055 * h, -0.925 * h + 0.5 * hh
    # kılıç (Katzbalger) — kalçada, geriye
    F.fill(bar(-0.04 * h, -0.50 * h, -0.255 * h, -0.435 * h, 0.022 * h, 0.014 * h, True, True), rim=0.9)
    F.fill(sp([(-0.065 * h, -0.55 * h), (-0.035 * h, -0.52 * h), (-0.07 * h, -0.49 * h), (-0.035 * h, -0.465 * h)], False), rim=0.0)
    F.line(sp([(-0.065 * h, -0.55 * h), (-0.04 * h, -0.52 * h), (-0.07 * h, -0.49 * h), (-0.04 * h, -0.463 * h)], False), h * 0.006, tone=0.5, alpha=0.9)
    # bacaklar (geniş duruş) + şişkin yırtmaçlı pantolon
    add_leg(F, h, (-0.035, -0.44), (-0.09, -0.255), (-0.145, -0.046), (0.075, 0.048, 0.032), 1, "square", 0.10, 0.7)
    add_leg(F, h, (0.045, -0.44), (0.10, -0.265), (0.165, -0.046), (0.08, 0.05, 0.034), 1, "square", 0.105, 0.9)
    for (cx, cy, rx, ry, rt) in ((-0.075, -0.385, 0.085, 0.07, 20), (0.085, -0.39, 0.09, 0.075, -15)):
        F.fill(ell(cx * h, cy * h, rx * h, ry * h, rt), rim=0.9)
        for k in range(4):
            dx = (k - 1.5) * 0.028
            F.crease(((cx + dx) * h, (cy - 0.06) * h), ((cx + dx * 1.2) * h, (cy + 0.06) * h), 0.006 * h, 0.005 * h, alpha=0.6)
    F.fill(poly([(-0.12 * h, -0.50 * h), (0.13 * h, -0.50 * h), (0.12 * h, -0.42 * h), (-0.11 * h, -0.42 * h)]), rim=0.9)
    # gövde
    torso(F, h, back=-0.112, front=0.108, chest=(-0.115, 0.116, -0.655), waist=(-0.09, 0.098, -0.53), hem=(-0.125, 0.13, -0.47))
    for k in range(5):
        F.crease((-0.06 * h + k * 0.03 * h, -0.70 * h), ((-0.065 + k * 0.032) * h, -0.52 * h), 0.006 * h, 0.004 * h, alpha=0.55)
    F.fill(fur_band([(-0.04 * h, -0.77 * h), (0.0, -0.785 * h), (0.055 * h, -0.775 * h)], 0.022 * h, 0.011 * h, side=1, jag=0.8), rim=1.0)
    # şişkin kollu (yırtmaçlı), uzak kol da ensede
    F.fill(ell(-0.045 * h, -0.725 * h, 0.07 * h, 0.05 * h, -25), rim=1.0)
    add_arm(F, [(-0.04 * h, -0.725 * h), (-0.125 * h, -0.625 * h), (-0.02 * h, -0.535 * h)], [0.09 * h, 0.095 * h, 0.05 * h], hand="fist", hand_len=0.07 * h, hand_rot=5)
    for k in range(4):
        F.crease((-0.12 * h + k * 0.02 * h, -0.70 * h + k * 0.012 * h), (-0.15 * h + k * 0.03 * h, -0.58 * h), 0.006 * h, 0.004 * h, alpha=0.65)
    # pike: omuzda diyagonal (tabanı geride aşağıda, ucu öne-yukarı); ön el göğüs hizasında kavrar
    ax, ay, bx, by = -0.02, -0.22, 0.60, -1.74
    F.fill(bar(ax * h, ay * h, bx * h, by * h, 0.0125 * h, 0.011 * h), rim=0.9)
    dx_, dy_ = bx - ax, by - ay
    Ln = math.hypot(dx_, dy_)
    ux, uy = dx_ / Ln, dy_ / Ln
    nx, ny = -uy, ux
    tx, ty = bx * h, by * h
    F.fill(sp([KC(tx - ux * 0.01 * h - nx * 0.012 * h, ty - uy * 0.01 * h - ny * 0.012 * h), (tx + ux * 0.04 * h - nx * 0.02 * h, ty + uy * 0.04 * h - ny * 0.02 * h), KC(tx + ux * 0.11 * h, ty + uy * 0.11 * h),
               (tx + ux * 0.04 * h + nx * 0.02 * h, ty + uy * 0.04 * h + ny * 0.02 * h), KC(tx - ux * 0.01 * h + nx * 0.012 * h, ty - uy * 0.01 * h + ny * 0.012 * h)], True), rim=1.0)
    add_arm(F, [(0.03 * h, -0.72 * h), (0.10 * h, -0.65 * h), (0.16 * h, -0.64 * h)], [0.07 * h, 0.07 * h, 0.046 * h], hand="fist", hand_len=0.07 * h, hand_rot=-10)
    add_head(F, hx, hy, hh, "m", rot=-2, beard="short", hat="plume", nose=1.1, neck_to=(0.0, -0.775 * h), hat_rot=6)
    return F.build()


# ───────────────────────────── pikeman ─────────────────────────────
@fx("pikeman")
def _pikeman(h, lean):
    """Pike piyadesi: sallet/kasket, göğüs zırhı, dizüstü kısa şişkin pantolon + üstüne binen 3 uyluk levhası (tassets), iki elle dik pike; hafif ileri adım."""
    F = Fig(h, lean)
    hh = 0.13 * h
    hx, hy = 0.05 * h, -0.925 * h + 0.5 * hh
    add_leg(F, h, (-0.03, -0.44), (-0.07, -0.255), (-0.09, -0.046), (0.075, 0.048, 0.032), 1, "round", 0.09, 0.7)
    add_leg(F, h, (0.03, -0.44), (0.065, -0.265), (0.10, -0.046), (0.08, 0.05, 0.034), 1, "round", 0.095, 0.9)
    pike(F, h, 0.17, top=-1.72, lean_x=0.006)
    # dizüstü pantolon (kısa, hafif şişkin) — tassets bunun üstünde
    F.fill(sp([KC(-0.095 * h, -0.50 * h), (-0.112 * h, -0.43 * h), (-0.095 * h, -0.355 * h), (0.0, -0.34 * h), (0.09 * h, -0.355 * h), (0.118 * h, -0.43 * h), KC(0.108 * h, -0.50 * h)], True), rim=0.9)
    for k in range(3):                                   # uyluk levhaları: aşağı doğru kısalan, ucu sivri
        y0 = -0.50 + k * 0.034
        F.fill(sp([KC(-0.108 * h, y0 * h), (0.0, (y0 - 0.008) * h), KC(0.118 * h, y0 * h), (0.105 * h, (y0 + 0.028) * h), (0.0, (y0 + 0.040) * h), (-0.095 * h, (y0 + 0.028) * h)], True, 0.8), rim=0.9)
    torso(F, h, back=-0.108, front=0.105, chest=(-0.112, 0.112, -0.655), waist=(-0.085, 0.092, -0.53), hem=(-0.11, 0.115, -0.49))
    F.line(sp([(0.02 * h, -0.755 * h), (0.045 * h, -0.62 * h), (0.025 * h, -0.50 * h)], False), h * 0.005, tone=1.0, alpha=0.55)
    F.line(sp([(-0.10 * h, -0.72 * h), (-0.02 * h, -0.70 * h), (0.10 * h, -0.72 * h)], False), h * 0.0035, tone=1.0, alpha=0.4)
    F.fill(sp([(-0.115 * h, -0.755 * h), (-0.07 * h, -0.795 * h), (0.0 * h, -0.795 * h), (0.02 * h, -0.74 * h), (-0.04 * h, -0.70 * h), (-0.115 * h, -0.70 * h)], True), rim=1.0)
    add_arm(F, [(-0.03 * h, -0.725 * h), (-0.04 * h, -0.60 * h), (0.10 * h, -0.55 * h)], [0.065 * h, 0.06 * h, 0.044 * h], hand="fist", hand_len=0.07 * h, hand_rot=-5)
    add_arm(F, [(0.045 * h, -0.725 * h), (0.11 * h, -0.65 * h), (0.172 * h, -0.64 * h)], [0.055 * h, 0.055 * h, 0.04 * h], hand="fist", hand_len=0.065 * h, hand_rot=-3)
    add_head(F, hx, hy, hh, "m", rot=0, beard="short", hat="sallet", nose=1.08, neck_to=(0.0, -0.775 * h), hat_rot=2)
    return F.build()


# ───────────────────────────── janissary ─────────────────────────────
@fx("janissary")
def _janissary(h, lean):
    F = Fig(h, lean)
    hh = 0.125 * h
    hx, hy = 0.04 * h, -0.88 * h + 0.5 * hh          # börk yüksek: kafa biraz düşük
    # kılıç (kilij): kalçada, geride
    F.fill(sp([KC(-0.03 * h, -0.50 * h), (-0.13 * h, -0.46 * h), (-0.22 * h, -0.36 * h), (-0.265 * h, -0.255 * h), (-0.255 * h, -0.245 * h), (-0.205 * h, -0.33 * h), (-0.12 * h, -0.435 * h), KC(-0.03 * h, -0.475 * h)], True), rim=0.9)
    # tüfek (fitilli): yerde, önde dikey
    F.fill(bar(0.185 * h, 0.0, 0.20 * h, -1.02 * h, 0.021 * h, 0.014 * h), rim=0.9)
    F.fill(bar(0.20 * h, -0.62 * h, 0.205 * h, -1.30 * h, 0.011 * h, 0.011 * h), rim=0.9)
    F.fill(poly([(0.178 * h, 0.0), (0.205 * h, 0.0), (0.21 * h, -0.07 * h), (0.172 * h, -0.07 * h)]), rim=0.9)
    # uzun kaftan: biraz dar etek, yürüyüş
    F.fill(shoe(0.115 * h, 0, 0.09 * h, 0.03 * h, 1, "sharp"), rim=0.8)
    F.fill(robe_path(h, sh_y=-0.742, nb_y=-0.765, back_sh=-0.108, front_sh=0.102, chest=(-0.115, 0.108, -0.65), waist=(-0.09, 0.092, -0.52),
                     hip=(-0.125, 0.125, -0.32), hem=(-0.17, 0.165, -0.15), nfold=3, amp=0.006, lift=0.012), rim=0.9, glow=0.10)
    robe_folds(F, h, -0.05, 0.05, -0.50, -0.18, 5, 0.009, bend=0.007, seed=51)
    # alt bacak/çizme
    F.fill(limb([(-0.03 * h, -0.17 * h), (-0.02 * h, -0.08 * h), (-0.015 * h, -0.02 * h)], [0.08 * h, 0.065 * h, 0.055 * h], cap0=0.0, cap1=0.2), rim=0.7)
    F.fill(limb([(0.07 * h, -0.17 * h), (0.10 * h, -0.08 * h), (0.115 * h, -0.02 * h)], [0.08 * h, 0.065 * h, 0.055 * h], cap0=0.0, cap1=0.2), rim=0.8)
    F.fill(shoe(-0.03 * h, 0, 0.09 * h, 0.03 * h, 1, "sharp"), rim=0.7)
    hem_slits(F, h, [-0.11, -0.03, 0.06, 0.13], -0.145, depth=0.045)
    # kuşak (kemer) ve önde kıvrık uç
    F.fill(poly([(-0.10 * h, -0.545 * h), (0.10 * h, -0.545 * h), (0.10 * h, -0.50 * h), (-0.10 * h, -0.50 * h)]), rim=0.8, tone=0.16, bound=False)
    F.crease((0.04 * h, -0.50 * h), (0.07 * h, -0.36 * h), 0.008 * h, 0.006 * h)
    F.line(poly([(-0.02 * h, -0.755 * h), (0.0, -0.545 * h)], False), h * 0.0035, tone=1.0, alpha=0.5)
    for k in range(4):
        F.fill(ell(0.012 * h, (-0.72 + k * 0.045) * h, 0.004 * h, 0.004 * h), rim=0, tone=0.8, alpha=0.7, bound=False)
    # kollar: biri tüfeği tutar, diğeri bele
    add_arm(F, [(-0.03 * h, -0.725 * h), (-0.09 * h, -0.62 * h), (-0.04 * h, -0.52 * h)], [0.06 * h, 0.066 * h, 0.044 * h], hand="fist", hand_len=0.065 * h, hand_rot=10)
    add_arm(F, [(0.045 * h, -0.725 * h), (0.12 * h, -0.65 * h), (0.195 * h, -0.64 * h)], [0.06 * h, 0.058 * h, 0.042 * h], hand="fist", hand_len=0.065 * h, hand_rot=-3)
    add_head(F, hx, hy, hh, "m", rot=-1, beard="stache", hat="bork", nose=1.1, neck_to=(0.0, -0.765 * h), hat_rot=0)
    return F.build()


# ───────────────────────────── knight ─────────────────────────────
@fx("knight")
def _knight(h, lean):
    F = Fig(h, lean)
    hh = 0.135 * h
    hx, hy = 0.045 * h, -0.915 * h + 0.5 * hh
    # kılıç (önde, ucu yere): iki el kabzada
    F.fill(bar(0.175 * h, 0.0, 0.175 * h, -0.55 * h, 0.012 * h, 0.016 * h), rim=1.0)
    F.fill(poly([(0.125 * h, -0.55 * h), (0.225 * h, -0.55 * h), (0.225 * h, -0.567 * h), (0.125 * h, -0.567 * h)]), rim=1.0)
    F.fill(bar(0.175 * h, -0.567 * h, 0.175 * h, -0.62 * h, 0.014 * h, 0.014 * h, False, True), rim=1.0)
    # bacaklar (zırh)
    for (hxp, kx, ax, wdk, sc) in (((-0.025, -0.44), (-0.06, -0.255), (-0.10, -0.05), 0.7, 0.7), ((0.035, -0.44), (0.075, -0.265), (0.115, -0.05), 0.9, 0.95)):
        pass
    add_leg(F, h, (-0.025, -0.44), (-0.06, -0.255), (-0.10, -0.05), (0.085, 0.058, 0.04), 1, "sharp", 0.11, 0.7, calf=0.008)
    add_leg(F, h, (0.035, -0.44), (0.075, -0.265), (0.115, -0.05), (0.09, 0.06, 0.042), 1, "sharp", 0.115, 1.0, calf=0.008)
    F.fill(sp([KC(0.045 * h, -0.285 * h), (0.095 * h, -0.30 * h), (0.115 * h, -0.265 * h), (0.095 * h, -0.235 * h), KC(0.05 * h, -0.24 * h)], True), rim=1.0)   # diz levhası
    F.fill(sp([KC(-0.095 * h, -0.275 * h), (-0.045 * h, -0.29 * h), (-0.03 * h, -0.255 * h), (-0.05 * h, -0.225 * h), KC(-0.09 * h, -0.23 * h)], True), rim=0.7)
    # tassets
    for k in range(3):
        F.fill(sp([KC((-0.115 + k * 0.004) * h, (-0.50 + k * 0.042) * h), (0.0 * h, (-0.485 + k * 0.042) * h), KC((0.125 - k * 0.004) * h, (-0.50 + k * 0.042) * h), ((0.12 - k * 0.004) * h, (-0.465 + k * 0.042) * h), (0.0, (-0.45 + k * 0.042) * h), ((-0.11 + k * 0.004) * h, (-0.465 + k * 0.042) * h)], True), rim=0.9)
    # göğüslük (globose) + omuzluklar
    F.fill(sp([KC(-0.04 * h, -0.775 * h), (-0.10 * h, -0.745 * h), (-0.108 * h, -0.65 * h), (-0.085 * h, -0.54 * h), KC(-0.10 * h, -0.50 * h), KC(0.12 * h, -0.50 * h),
               (0.095 * h, -0.55 * h), (0.125 * h, -0.64 * h), (0.10 * h, -0.74 * h), (0.05 * h, -0.775 * h)], True, 0.95), rim=1.0, glow=0.12)
    F.line(sp([(0.04 * h, -0.755 * h), (0.07 * h, -0.64 * h), (0.045 * h, -0.52 * h)], False), h * 0.005, tone=1.0, alpha=0.5)
    F.fill(sp([(-0.12 * h, -0.76 * h), (-0.07 * h, -0.805 * h), (0.0, -0.80 * h), (0.025 * h, -0.74 * h), (-0.03 * h, -0.695 * h), (-0.12 * h, -0.70 * h)], True), rim=1.0)
    add_arm(F, [(-0.03 * h, -0.72 * h), (-0.075 * h, -0.62 * h), (0.11 * h, -0.575 * h)], [0.07 * h, 0.07 * h, 0.05 * h], hand="fist", hand_len=0.065 * h, hand_rot=-8)
    add_arm(F, [(0.05 * h, -0.725 * h), (0.12 * h, -0.64 * h), (0.172 * h, -0.60 * h)], [0.06 * h, 0.06 * h, 0.044 * h], hand="fist", hand_len=0.06 * h, hand_rot=20)
    # armet miğferi + tüy
    top_y = hy - 0.58 * hh
    F.fill(feather_path(hx - 0.02 * hh, top_y + 0.02 * hh, hx - 1.9 * hh, top_y - 0.50 * hh, 0.42 * hh, bend=0.36 * hh), rim=1.0)
    F.fill(feather_path(hx + 0.04 * hh, top_y + 0.02 * hh, hx - 1.1 * hh, top_y - 1.05 * hh, 0.40 * hh, bend=0.30 * hh), rim=1.0)
    F.fill(feather_path(hx + 0.10 * hh, top_y + 0.03 * hh, hx - 0.2 * hh, top_y - 1.15 * hh, 0.36 * hh, bend=0.15 * hh), rim=1.0)
    F.fill(place(sp([KC(-0.36, 0.52), (-0.50, 0.15), (-0.46, -0.28), (-0.20, -0.56), (0.12, -0.60), (0.36, -0.46), (0.50, -0.12), (0.62, 0.14), (0.54, 0.36), (0.40, 0.58), (0.10, 0.66), KC(-0.14, 0.58)], True, 0.95), hx, hy, hh, 0), rim=1.0, glow=0.10)
    F.cut(place(sp([KC(0.16, -0.05), (0.42, -0.07), KC(0.60, 0.02), (0.58, 0.07), (0.40, 0.01), KC(0.16, 0.0)], True, 0.6), hx, hy, hh, 0))
    F.line(place(sp([(-0.10, -0.58), (0.0, -0.50), (0.20, -0.30), (0.34, -0.10)], False), hx, hy, hh, 0), h * 0.004, tone=1.0, alpha=0.5)
    F.fill(place(poly([(-0.12, -0.58), (0.10, -0.62), (0.02, -0.74), (-0.18, -0.70)]), hx, hy, hh, 0), rim=1.0)
    F.fill(limb([(0.0, -0.80 * h), (0.0, -0.76 * h)], [0.12 * h, 0.15 * h], cap0=0, cap1=0), rim=0.9)     # gorget
    return F.build()


# ───────────────────────────── conquistador ─────────────────────────────
@fx("conquistador")
def _conquistador(h, lean):
    F = Fig(h, lean)
    hh = 0.13 * h
    hx, hy = 0.05 * h, -0.925 * h + 0.5 * hh
    # mızrak + flama (yan elde)
    pike(F, h, 0.225, top=-1.55, lean_x=0.01, head="leaf", w=0.011)
    F.fill(sp([KC(0.236 * h, -1.48 * h), (0.30 * h, -1.50 * h), (0.37 * h, -1.47 * h), (0.34 * h, -1.435 * h), (0.37 * h, -1.40 * h), (0.30 * h, -1.42 * h), KC(0.236 * h, -1.40 * h)], True, 0.8), rim=1.0)
    # pelerin (omuzdan geriye sarkan)
    F.fill(sp([KC(-0.04 * h, -0.775 * h), (-0.12 * h, -0.745 * h), (-0.16 * h, -0.60 * h), (-0.19 * h, -0.42 * h), (-0.215 * h, -0.28 * h), KC(-0.17 * h, -0.255 * h), (-0.12 * h, -0.32 * h), (-0.095 * h, -0.45 * h), (-0.07 * h, -0.60 * h)], True), rim=0.9, glow=0.08)
    F.crease((-0.12 * h, -0.70 * h), (-0.195 * h, -0.33 * h), 0.009 * h, 0.012 * h)
    F.crease((-0.095 * h, -0.67 * h), (-0.14 * h, -0.34 * h), 0.007 * h, -0.008 * h, alpha=0.5)
    # kılıç (rapier) geriye
    F.fill(bar(-0.06 * h, -0.49 * h, -0.30 * h, -0.30 * h, 0.011 * h, 0.006 * h, True, False), rim=0.9)
    F.fill(bar(-0.075 * h, -0.55 * h, -0.045 * h, -0.45 * h, 0.011 * h, 0.011 * h, True, True), rim=0.9)
    add_leg(F, h, (-0.025, -0.45), (-0.06, -0.26), (-0.10, -0.046), (0.075, 0.048, 0.032), 1, "round", 0.095, 0.7)
    add_leg(F, h, (0.035, -0.45), (0.08, -0.27), (0.12, -0.046), (0.08, 0.05, 0.034), 1, "round", 0.10, 0.9)
    F.fill(sp([KC(-0.09 * h, -0.50 * h), (-0.12 * h, -0.43 * h), (-0.10 * h, -0.345 * h), (-0.01 * h, -0.325 * h), (0.07 * h, -0.34 * h), (0.125 * h, -0.38 * h), (0.12 * h, -0.45 * h), KC(0.095 * h, -0.50 * h)], True), rim=0.9)
    # zırhlı göğüs (peascod)
    F.fill(sp([KC(-0.04 * h, -0.775 * h), (-0.10 * h, -0.745 * h), (-0.105 * h, -0.65 * h), (-0.085 * h, -0.545 * h), KC(-0.11 * h, -0.495 * h), KC(0.13 * h, -0.495 * h),
               (0.105 * h, -0.54 * h), (0.118 * h, -0.64 * h), (0.10 * h, -0.74 * h), (0.05 * h, -0.775 * h)], True, 0.95), rim=1.0, glow=0.12)
    F.line(sp([(0.04 * h, -0.755 * h), (0.075 * h, -0.64 * h), (0.075 * h, -0.52 * h)], False), h * 0.005, tone=1.0, alpha=0.5)
    F.fill(fur_band([(-0.05 * h, -0.775 * h), (0.0, -0.79 * h), (0.06 * h, -0.775 * h)], 0.03 * h, 0.013 * h, side=1, jag=0.8), rim=1.0)
    F.fill(ell(-0.04 * h, -0.735 * h, 0.05 * h, 0.032 * h, -15), rim=1.0)
    add_arm(F, [(-0.035 * h, -0.73 * h), (-0.14 * h, -0.62 * h), (-0.04 * h, -0.51 * h)], [0.064 * h, 0.07 * h, 0.044 * h], hand="fist", hand_len=0.065 * h, hand_rot=15)
    add_arm(F, [(0.05 * h, -0.725 * h), (0.12 * h, -0.64 * h), (0.222 * h, -0.62 * h)], [0.06 * h, 0.058 * h, 0.042 * h], hand="fist", hand_len=0.065 * h, hand_rot=0)
    add_head(F, hx, hy, hh, "m", rot=-2, beard="point", hat="morion", nose=1.15, chin=0.02, neck_to=(0.0, -0.775 * h), hat_rot=1)
    return F.build()


# ───────────────────────────── sailor ─────────────────────────────
@fx("sailor")
def _sailor(h, lean):
    F = Fig(h, lean)
    hh = 0.135 * h
    hx, hy = 0.06 * h, -0.92 * h + 0.5 * hh
    # halat kangı (omuzda) + sarkan uç
    F.fill(sp([(-0.08 * h, -0.75 * h), (-0.15 * h, -0.70 * h), (-0.165 * h, -0.60 * h), (-0.12 * h, -0.55 * h), (-0.07 * h, -0.60 * h), (-0.05 * h, -0.70 * h)], True), rim=1.0)
    for k in range(4):
        F.line(sp([(-0.14 * h + k * 0.01 * h, -0.70 * h + k * 0.02 * h), (-0.07 * h, -0.66 * h + k * 0.02 * h)], False), h * 0.004, tone=0.9, alpha=0.5)
    # çıplak ayak (kısa pantolon baldırda), yürüyüş
    for (hx_, kx, ax, rim) in (((-0.02, -0.44), (-0.055, -0.22), (-0.095, -0.03), 0.7), ((0.04, -0.44), (0.085, -0.23), (0.125, -0.03), 0.9)):
        F.fill(limb([(hx_[0] * h, hx_[1] * h), (kx[0] * h, kx[1] * h), (ax[0] * h, ax[1] * h)], [0.075 * h, 0.05 * h, 0.032 * h], cap0=0.3, cap1=0.3), rim=rim)
        F.fill(sp([KC((ax[0] - 0.02) * h, (ax[1] - 0.01) * h), ((ax[0] + 0.04) * h, (ax[1] - 0.012) * h), ((ax[0] + 0.075) * h, -0.004 * h), KC((ax[0] + 0.075) * h, 0.0), KC((ax[0] - 0.03) * h, 0.0)], True, 0.8), rim=rim)
    F.fill(sp([KC(-0.095 * h, -0.50 * h), (-0.115 * h, -0.42 * h), (-0.10 * h, -0.30 * h), KC(-0.07 * h, -0.255 * h), KC(0.0 * h, -0.255 * h), (0.02 * h, -0.30 * h), (0.075 * h, -0.255 * h), KC(0.13 * h, -0.28 * h), (0.125 * h, -0.40 * h), KC(0.11 * h, -0.50 * h)], True), rim=0.9)
    F.crease((-0.04 * h, -0.45 * h), (-0.05 * h, -0.27 * h), 0.007 * h, 0.005 * h)
    F.crease((0.06 * h, -0.45 * h), (0.07 * h, -0.28 * h), 0.007 * h, -0.005 * h)
    # gömlek (bol), kemerli
    F.fill(sp([KC(-0.04 * h, -0.775 * h), (-0.10 * h, -0.745 * h), (-0.115 * h, -0.64 * h), (-0.10 * h, -0.54 * h), KC(-0.105 * h, -0.48 * h), KC(0.115 * h, -0.48 * h), (0.105 * h, -0.54 * h), (0.118 * h, -0.64 * h), (0.10 * h, -0.74 * h), (0.05 * h, -0.775 * h)], True, 0.95), rim=0.9, glow=0.10)
    F.crease((-0.05 * h, -0.70 * h), (-0.06 * h, -0.52 * h), 0.007 * h, 0.006 * h)
    F.crease((0.03 * h, -0.72 * h), (0.045 * h, -0.52 * h), 0.007 * h, -0.005 * h)
    F.fill(poly([(-0.10 * h, -0.515 * h), (0.11 * h, -0.515 * h), (0.11 * h, -0.495 * h), (-0.10 * h, -0.495 * h)]), rim=0.5, tone=0.2, bound=False)
    F.fill(bar(0.045 * h, -0.50 * h, 0.075 * h, -0.42 * h, 0.012 * h, 0.01 * h, True, False), rim=0.9)    # bıçak
    # yakın kol: dirsek bükük, el belde; uzak kol halat tutar
    add_arm(F, [(-0.03 * h, -0.725 * h), (-0.115 * h, -0.62 * h), (-0.04 * h, -0.52 * h)], [0.068 * h, 0.07 * h, 0.044 * h], hand="fist", hand_len=0.07 * h, hand_rot=10)
    add_head(F, hx, hy, hh, "m", rot=2, beard="short", hat="woolcap", nose=1.1, neck_to=(0.0, -0.775 * h), hat_rot=2)
    return F.build()


# ───────────────────────────── native (Mezoamerika'dan onurlu bir soylu: omuzda düğümlü tilma, bel bezi, sandalet, tüylü alın bandı) ─────────────────────────────
@fx("native")
def _native(h, lean):
    F = Fig(h, lean)
    hh = 0.13 * h
    hx, hy = 0.045 * h, -0.925 * h + 0.5 * hh
    # asa (yere basan, süssüz, üstte küçük tüy bağı)
    F.fill(bar(0.175 * h, 0.0, 0.185 * h, -0.93 * h, 0.014 * h, 0.012 * h, False, True), rim=0.9)
    F.fill(feather_path(0.185 * h, -0.94 * h, 0.20 * h, -1.04 * h, 0.028 * h, bend=0.01 * h), rim=1.0)
    # bacaklar (çıplak), sandaletler (bağlı), bel bezi uçları (süslü)
    for (a, b, c, rim) in (((-0.02, -0.46), (-0.05, -0.24), (-0.085, -0.03), 0.7), ((0.035, -0.46), (0.075, -0.25), (0.11, -0.03), 0.9)):
        F.fill(limb([(a[0] * h, a[1] * h), (b[0] * h, b[1] * h), (c[0] * h, c[1] * h)], [0.07 * h, 0.048 * h, 0.03 * h], cap0=0.3, cap1=0.3), rim=rim)
        F.fill(sp([KC((c[0] - 0.02) * h, (c[1]) * h), ((c[0] + 0.05) * h, (c[1] - 0.004) * h), KC((c[0] + 0.07) * h, 0.0), KC((c[0] - 0.03) * h, 0.0)], True, 0.8), rim=rim)
        F.line(poly([(c[0] * h, (c[1] - 0.02) * h), ((c[0] + 0.03) * h, (c[1] - 0.005) * h)], False), h * 0.004, tone=1.0, alpha=0.45)
    F.fill(sp([KC(-0.06 * h, -0.45 * h), (-0.07 * h, -0.36 * h), (-0.06 * h, -0.28 * h), KC(-0.02 * h, -0.25 * h), KC(0.0, -0.36 * h), (0.02 * h, -0.28 * h), KC(0.075 * h, -0.28 * h), (0.075 * h, -0.36 * h), KC(0.07 * h, -0.45 * h)], True), rim=0.9)
    for (x0_, x1_) in ((-0.066, -0.01), (0.012, 0.074)):
        for k in range(3):
            F.fill(poly([((x0_ + k * (x1_ - x0_) / 3) * h, -0.30 * h), ((x0_ + (k + 0.6) * (x1_ - x0_) / 3) * h, -0.30 * h), ((x0_ + (k + 0.3) * (x1_ - x0_) / 3) * h, -0.272 * h)]), rim=0.0, tone=1.0, alpha=0.5, bound=False)
    # tilma: sağ omuzda düğümlü dikdörtgen mantı; kumaş çapraz iner, etek kenarı çapraz
    F.fill(sp([KC(-0.045 * h, -0.775 * h), (-0.10 * h, -0.745 * h), (-0.115 * h, -0.62 * h), (-0.112 * h, -0.45 * h), (-0.125 * h, -0.36 * h), KC(-0.11 * h, -0.335 * h), (-0.03 * h, -0.355 * h), (0.05 * h, -0.40 * h),
               (0.085 * h, -0.50 * h), (0.10 * h, -0.64 * h), (0.09 * h, -0.74 * h), (0.05 * h, -0.775 * h)], True, 0.95), rim=0.9, glow=0.10)
    F.line(sp([(-0.115 * h, -0.355 * h), (-0.03 * h, -0.375 * h), (0.05 * h, -0.42 * h), (0.087 * h, -0.50 * h)], False), h * 0.007, tone=1.0, alpha=0.55)       # basamaklı sınır bandı
    for k in range(7):
        t = k / 6
        x = -0.11 + t * 0.19
        y = -0.352 - t * 0.12 + (0.012 if k % 2 == 0 else 0.0)
        F.fill(poly([(x * h, y * h), ((x + 0.016) * h, y * h), ((x + 0.016) * h, (y - 0.012) * h), ((x + 0.03) * h, (y - 0.012) * h)]), rim=0.0, tone=1.0, alpha=0.5, bound=False)
    F.crease((-0.05 * h, -0.65 * h), (-0.07 * h, -0.38 * h), 0.008 * h, 0.01 * h)
    F.crease((0.0 * h, -0.62 * h), (-0.01 * h, -0.40 * h), 0.007 * h, -0.006 * h, alpha=0.5)
    F.fill(ell(0.072 * h, -0.735 * h, 0.019 * h, 0.019 * h), rim=1.0)
    # kollar + bilezik
    add_arm(F, [(0.045 * h, -0.725 * h), (0.11 * h, -0.62 * h), (0.178 * h, -0.60 * h)], [0.055 * h, 0.052 * h, 0.04 * h], hand="fist", hand_len=0.062 * h, hand_rot=5)
    add_arm(F, [(-0.03 * h, -0.725 * h), (-0.09 * h, -0.63 * h), (0.0 * h, -0.60 * h)], [0.055 * h, 0.055 * h, 0.04 * h], hand="open", hand_len=0.06 * h, hand_rot=0)
    F.line(poly([(0.14 * h, -0.612 * h), (0.152 * h, -0.608 * h)], False), h * 0.006, tone=1.0, alpha=0.7)
    add_head(F, hx, hy, hh, "m", rot=0, beard=None, hair="bob", hat="headband", neck_to=(0.0, -0.775 * h), nose=1.05, hat_rot=0)
    return F.build()


import sk  # noqa: E402

for _m in ("figs_horse", "figs_more"):          # grup-2 modülleri (varsa; hata olursa uyarı basılır, kit bozulmaz)
    sk.optional_import(_m)
