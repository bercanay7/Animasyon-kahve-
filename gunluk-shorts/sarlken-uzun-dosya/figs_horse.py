"""figs_horse — at ve atlılar (figür-lab): horse, horse_walk, horse_rider, cavalry_charge (+ cavalry_charge_b), sipahi.
Hepsi sağa bakar. horse: h = kulak ucu yüksekliği (≈ baş kalkık). Binicili türlerde h = zeminden binicinin başlığına (mızrak/tüy hariç) toplam boy.
Dörtnala animasyonu: cavalry_charge ile cavalry_charge_b'yi 5–7 karede bir dönüşümlü çiz (iki poz)."""
import math

import skia

import stage as ST
import figs_kit as K
from figs_kit import K as KC, Fig, bar, ell, feather_path, lens, limb, place, poly, shoe, sp
from figs_parts import add_arm, add_head, fur_band


def fx(name):
    return ST.figx(name)


# ───────────────────────────── at gövdesi ─────────────────────────────
# ───────────────────────────── at: gövde, boyun, baş, bacaklar ─────────────────────────────
# Birim: h = kulak ucu yüksekliği; withers y≈−0.765, kulak ucu ≈ −1.09. Bacak eklemleri (h oranı): ön: [üst, diz, bilek(fetlock), toynak tabanı]; arka: [üst, hok, bilek, toynak].
HORSE_STAND = dict(
    fn=[(0.30, -0.50), (0.315, -0.265), (0.325, -0.075), (0.335, 0.0)],
    ff=[(0.235, -0.50), (0.235, -0.265), (0.24, -0.075), (0.25, 0.0)],
    hn=[(-0.40, -0.58), (-0.50, -0.29), (-0.47, -0.075), (-0.46, 0.0)],
    hf=[(-0.34, -0.55), (-0.40, -0.30), (-0.37, -0.075), (-0.36, 0.0)],
    poll=(0.52, -0.98), head_ang=38.0, tail="hang", mane_flick=0.0, mane_long=0.8, rot=0.0)

HORSE_WALK = dict(
    fn=[(0.30, -0.50), (0.405, -0.335), (0.345, -0.205), (0.335, -0.14)],
    ff=[(0.235, -0.50), (0.23, -0.27), (0.225, -0.085), (0.225, 0.0)],
    hn=[(-0.40, -0.58), (-0.57, -0.31), (-0.625, -0.10), (-0.64, 0.0)],
    hf=[(-0.34, -0.55), (-0.395, -0.29), (-0.355, -0.085), (-0.345, 0.0)],
    poll=(0.535, -0.955), head_ang=41.0, tail="hang", mane_flick=0.2, mane_long=0.9, rot=0.0)

GALLOP_A = dict(     # uzamış: ön bacaklar ileri, arka bacaklar geriye gerilmiş
    fn=[(0.30, -0.50), (0.50, -0.405), (0.685, -0.325), (0.755, -0.29)],
    ff=[(0.235, -0.50), (0.40, -0.36), (0.52, -0.21), (0.565, -0.145)],
    hn=[(-0.40, -0.60), (-0.62, -0.50), (-0.80, -0.37), (-0.885, -0.31)],
    hf=[(-0.34, -0.57), (-0.52, -0.43), (-0.66, -0.26), (-0.71, -0.185)],
    poll=(0.625, -0.91), head_ang=28.0, tail="stream", mane_flick=1.0, mane_long=1.5, rot=2.5)

GALLOP_B = dict(     # toplanmış: bacaklar gövdenin altında, ön yakın bacak iniyor
    fn=[(0.30, -0.50), (0.385, -0.34), (0.425, -0.15), (0.435, -0.075)],
    ff=[(0.235, -0.50), (0.31, -0.33), (0.265, -0.205), (0.205, -0.165)],
    hn=[(-0.40, -0.60), (-0.47, -0.40), (-0.30, -0.255), (-0.235, -0.20)],
    hf=[(-0.34, -0.57), (-0.39, -0.365), (-0.225, -0.225), (-0.165, -0.185)],
    poll=(0.565, -0.945), head_ang=35.0, tail="stream", mane_flick=0.8, mane_long=1.3, rot=-3.5)


def _lp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _hleg(F, joints, kind, h, rim=1.0, tone=0.0):
    """At bacağı: eklemlerden (üst, diz/hok, bilek, toynak tabanı) kas kütleli, ince kemikli, bilekte şişkin bacak + toynak."""
    top, j1, j2, j3 = joints
    if kind == "f":
        pts = [top, _lp(top, j1, 0.5), j1, _lp(j1, j2, 0.45), j2, _lp(j2, j3, 0.45)]
        ws = [0.125, 0.088, 0.056, 0.040, 0.050, 0.040]
    else:
        pts = [top, _lp(top, j1, 0.5), j1, _lp(j1, j2, 0.45), j2, _lp(j2, j3, 0.45)]
        ws = [0.205, 0.098, 0.066, 0.041, 0.050, 0.040]
    P = [(x * h, y * h) for x, y in pts]
    F.fill(limb(P, [w * h for w in ws], cap0=0.4, cap1=0.0), rim=rim, tone=tone)
    if kind == "h":                              # hokun arkaya çıkıntısı
        hx_, hy_ = j1[0] * h - 0.012 * h, j1[1] * h
        F.fill(ell(hx_, hy_, 0.017 * h, 0.028 * h, 16), rim=rim * 0.55)
    # toynak: pastern ucundan sole'a doğru genişleyen yamuk
    dx, dy = j3[0] - j2[0], j3[1] - j2[1]
    Ln = math.hypot(dx, dy) or 1.0
    dx, dy = dx / Ln, dy / Ln
    nx, ny = -dy, dx
    if nx < 0:
        nx, ny = -nx, -ny
    hh_ = 0.040 * h
    cx_, cy_ = j3[0] * h - dx * hh_, j3[1] * h - dy * hh_
    wc, ws_ = 0.046 * h, 0.064 * h
    F.fill(poly([(cx_ - nx * wc * 0.45, cy_ - ny * wc * 0.45), (cx_ + nx * wc * 0.55, cy_ + ny * wc * 0.55),
                 (j3[0] * h + nx * ws_ * 0.62, j3[1] * h + ny * ws_ * 0.62), (j3[0] * h - nx * ws_ * 0.38, j3[1] * h - ny * ws_ * 0.38)]), rim=rim)


def _hp(pts, h):
    return [((q[0] * h, q[1] * h, "c") if len(q) > 2 else (q[0] * h, q[1] * h)) for q in pts]


def _head_geometry(poll, L, ang_deg):
    """Baş yerel profilini (u: eksen boyunca 0..1, v: çene tarafına dik) dünya noktalarına çevirir. Dönüş: top[], bottom[], throat, eye, nostril, muzzle."""
    th = math.radians(ang_deg)
    ax, ay = math.cos(th), math.sin(th)
    nx, ny = -math.sin(th), math.cos(th)

    def W(u, v):
        return (poll[0] + L * (u * ax + v * nx), poll[1] + L * (u * ay + v * ny))
    top = [W(0.0, -0.045), W(0.09, -0.078), W(0.28, -0.062), W(0.52, -0.030), W(0.76, -0.004), W(0.92, 0.018)]
    muz = [W(0.985, 0.060), W(1.025, 0.105), W(1.03, 0.160), (-9, -9, "lip")]
    muz = [W(0.985, 0.060), W(1.030, 0.110), W(1.035, 0.165), W(1.00, 0.205), W(0.965, 0.228)]
    bot = [W(0.90, 0.238), W(0.80, 0.240), W(0.66, 0.272), W(0.52, 0.335), W(0.38, 0.435), W(0.26, 0.460), W(0.15, 0.405), W(0.07, 0.30)]
    return top, muz, bot, W(0.05, 0.22), W(0.30, 0.045), W(0.985, 0.115), W(1.0, 0.2), (ax, ay, nx, ny)


def _ear(F, base, ang, ln, wd, h, rim):
    bx, by = base
    th = math.radians(ang)
    tx, ty = bx + math.cos(th) * ln, by + math.sin(th) * ln
    nx, ny = -math.sin(th), math.cos(th)
    F.fill(sp([KC(bx - nx * wd * 0.5, by - ny * wd * 0.5), (bx + math.cos(th) * ln * 0.55 - nx * wd * 0.5, by + math.sin(th) * ln * 0.55 - ny * wd * 0.5), KC(tx, ty),
               (bx + math.cos(th) * ln * 0.55 + nx * wd * 0.42, by + math.sin(th) * ln * 0.55 + ny * wd * 0.42), KC(bx + nx * wd * 0.5, by + ny * wd * 0.5)], True, 0.8), rim=rim)


def _mane_locks(F, W0, P0, h, n=7, long=0.9, flick=0.0, rim=1.0):
    """Yele: ense çizgisi (W0 withers → P0 poll) boyunca üst üste binen, geriye ve aşağıya akan geniş S-eğrili tutamlar."""
    for i in range(n):
        t = 0.02 + 0.96 * i / (n - 1)
        bx = W0[0] + (P0[0] - W0[0]) * t
        by = W0[1] + (P0[1] - W0[1]) * t
        ln = (0.15 + 0.035 * math.sin(t * 3.1 + 1.0)) * long
        back = 0.46 + 0.62 * flick
        drop = (0.88 - 0.55 * flick)
        tip = (bx - back * ln, by + drop * ln * (1.0 if flick < 0.6 else 0.6))
        base_a = (bx + 0.015, by - 0.016)
        base_b = (bx - 0.040, by + 0.040)
        c1 = (bx - back * ln * 0.30 + 0.030, by + drop * ln * 0.28 - 0.006)       # üst kenar: dışa kabarık
        c2 = (bx - back * ln * 0.62 - 0.012, by + drop * ln * 0.66 + 0.034)       # alt kenar: içe
        F.fill(sp([KC(base_a[0] * h, base_a[1] * h), (c1[0] * h, c1[1] * h), KC(tip[0] * h, tip[1] * h), (c2[0] * h, c2[1] * h), KC(base_b[0] * h, base_b[1] * h)], True, 0.95), rim=rim)


def horse_body(F, h, pose=HORSE_STAND, mane=True, tail=True, bridle=True, dy=0.0):
    """At: bacaklar + gövde/boyun/baş + yele + kuyruk. h = kulak ucu yüksekliği."""
    P = pose
    poll = P["poll"]
    L = 0.31
    top, muz, bot, throat, eye, nostril, lip, (ax, ay, nx, ny) = _head_geometry(poll, L, P["head_ang"])
    # --- bacaklar (gövde üstlerini örter): uzaklar soluk, yakınlar parlak
    _hleg(F, P["ff"], "f", h, rim=0.40)
    _hleg(F, P["hf"], "h", h, rim=0.40)
    _hleg(F, P["hn"], "h", h, rim=1.0)
    _hleg(F, P["fn"], "f", h, rim=1.0)
    # --- kuyruk
    if tail:
        if P["tail"] == "stream":
            tp = [(-0.52, -0.745 + dy), (-0.62, -0.745 + dy), (-0.76, -0.725), (-0.90, -0.69), (-1.02, -0.65), (-1.12, -0.63)]
            wd = [0.045, 0.085, 0.095, 0.085, 0.055, 0.012]
        else:
            tp = [(-0.52, -0.745 + dy), (-0.585, -0.70 + dy), (-0.665, -0.60), (-0.705, -0.48), (-0.70, -0.36), (-0.675, -0.27)]
            wd = [0.04, 0.085, 0.095, 0.085, 0.05, 0.012]
        F.fill(limb([(x * h, y * h) for x, y in tp], [w * h for w in wd], cap0=0.4, cap1=0.0), rim=0.9)
        if P["tail"] == "stream":
            F.crease((-0.64 * h, -0.74 * h), (-1.04 * h, -0.64 * h), 0.008 * h, 0.012 * h, alpha=0.5)
            F.crease((-0.70 * h, -0.70 * h), (-1.08 * h, -0.62 * h), 0.006 * h, -0.010 * h, alpha=0.4)
        else:
            F.crease((-0.62 * h, -0.64 * h), (-0.70 * h, -0.32 * h), 0.008 * h, 0.012 * h, alpha=0.5)
            F.crease((-0.66 * h, -0.62 * h), (-0.69 * h, -0.30 * h), 0.006 * h, -0.010 * h, alpha=0.4)
    # --- uzak kulak
    _ear(F, W_ := (poll[0] - 0.010, poll[1] - 0.005), -80.0, 0.105, 0.040, h, 0.5) if False else None
    ex = poll[0] - 0.020
    ey = poll[1] - 0.005
    F.fill(sp(_hp([KC(ex - 0.016, ey), (ex - 0.026, ey - 0.055), KC(ex - 0.008, ey - 0.118), (ex + 0.020, ey - 0.056), KC(ex + 0.022, ey)], h), True, 0.8), rim=0.5)
    # --- gövde + boyun + baş (tek kapalı eğri)
    W0 = (0.20, -0.765)
    crest = []
    dxn, dyn = poll[0] - W0[0], poll[1] - W0[1]
    Ln = math.hypot(dxn, dyn)
    cnx, cny = dyn / Ln, -dxn / Ln                     # sol-yukarı normal
    for t in (0.18, 0.38, 0.58, 0.78):
        b = 0.040 * math.sin(math.pi * t)
        crest.append((W0[0] + dxn * t + cnx * b, W0[1] + dyn * t + cny * b))
    B0 = (0.425, -0.60)
    under = []
    for t in (0.22, 0.48, 0.74):
        # boğaz altından göğse: hafif içbükey
        tx_, ty_ = throat
        q = (tx_ + (B0[0] - tx_) * t, ty_ + (B0[1] - ty_) * t)
        bulge = -0.018 * math.sin(math.pi * t)
        under.append((q[0] + bulge * 0.7, q[1] + bulge * 0.6))
    under = under[::-1]
    body = [
        KC(-0.515, -0.755 + dy), (-0.45, -0.780 + dy), (-0.34, -0.785 + dy), (-0.20, -0.755 + dy), (-0.02, -0.738 + dy), (0.10, -0.745 + dy), (0.20, -0.766 + dy),
    ] + crest + top + muz + bot[::-1][::-1] + [throat] + under[::-1][::-1] + [
        B0, (0.438, -0.535), (0.405, -0.455), (0.32, -0.418), (0.18, -0.402), (0.02, -0.402), (-0.14, -0.425), (-0.27, -0.452), (-0.38, -0.49),
        (-0.50, -0.545), (-0.552, -0.625), (-0.548, -0.70),
    ]
    body = [(q[0] * h, q[1] * h, "c") if len(q) > 2 else (q[0] * h, q[1] * h) for q in body]
    F.fill(sp(body, True, 1.0), rim=1.0, glow=0.06)
    # --- sağrı/omuz kas çizgileri
    F.line(sp(_hp([(-0.36, -0.77), (-0.31, -0.62), (-0.30, -0.49)], h), False), h * 0.0035, tone=1.0, alpha=0.30)
    F.line(sp(_hp([(0.16, -0.755), (0.25, -0.62), (0.30, -0.50)], h), False), h * 0.0035, tone=1.0, alpha=0.30)
    # --- yakın kulak, perçem, yele
    ex = poll[0] + 0.012
    F.fill(sp(_hp([KC(ex - 0.020, ey + 0.004), (ex - 0.030, ey - 0.054), KC(ex - 0.008, ey - 0.121), (ex + 0.024, ey - 0.056), KC(ex + 0.026, ey + 0.004)], h), True, 0.8), rim=1.0)
    F.fill(sp(_hp([KC(poll[0] + 0.03, poll[1] - 0.012), (poll[0] + 0.07, poll[1] + 0.005), (poll[0] + 0.065, poll[1] + 0.055), (poll[0] + 0.04, poll[1] + 0.07), (poll[0] + 0.035, poll[1] + 0.03)], h), True, 0.8), rim=1.0, bound=False)
    if mane:
        _mane_locks(F, (W0[0] + 0.02, W0[1] - 0.012), (poll[0] - 0.015, poll[1] + 0.005), h, n=7, long=P["mane_long"], flick=P["mane_flick"])
    # --- yüz ayrıntıları: göz parıltısı, burun deliği, ağız çizgisi, boyunluk/kayış
    F.fill(ell(eye[0] * h, eye[1] * h, 0.010 * h, 0.0075 * h, -20), rim=0.0, tone=1.0, alpha=0.65, bound=False)
    F.fill(ell(nostril[0] * h, nostril[1] * h, 0.0085 * h, 0.0125 * h, -30), rim=0.0, tone=1.0, alpha=0.40, bound=False)
    mx, my = lip
    F.line(sp(_hp([(mx - 0.002, my), (mx - 0.05 * ax * 1.0, my - 0.05 * ay * 1.0)], h), False), h * 0.0030, tone=1.0, alpha=0.5)
    if bridle:
        def Wh(u, v):
            return (poll[0] + L * (u * ax + v * nx), poll[1] + L * (u * ay + v * ny))
        F.line(sp(_hp([Wh(0.34, -0.06), Wh(0.30, 0.20), Wh(0.30, 0.45)], h), False), h * 0.0035, tone=0.9, alpha=0.65)       # yanak kayışı
        F.line(sp(_hp([Wh(0.12, -0.06), Wh(0.10, 0.12), Wh(0.14, 0.28)], h), False), h * 0.0035, tone=0.9, alpha=0.55)       # alınlık
        F.line(sp(_hp([Wh(0.78, -0.002), Wh(0.77, 0.12), Wh(0.80, 0.24)], h), False), h * 0.0035, tone=0.9, alpha=0.65)      # burun kayışı


@fx("horse")
def _horse(h, lean):
    F = Fig(h, lean)
    horse_body(F, h, HORSE_STAND)
    return F.build()


@fx("horse_walk")
def _horse_walk(h, lean):
    F = Fig(h, lean)
    horse_body(F, h, HORSE_WALK)
    return F.build()


def _armet(F, hx, hy, hh, plume=True, rot=0.0, crest_col=None):
    """Kapalı miğfer (armet) + tüy. hx,hy baş merkezi (px), hh baş yüksekliği (px)."""
    top_y = hy - 0.58 * hh
    if plume:
        F.fill(feather_path(hx - 0.02 * hh, top_y + 0.02 * hh, hx - 1.9 * hh, top_y - 0.50 * hh + rot * 0.02 * hh, 0.42 * hh, bend=0.36 * hh), rim=1.0)
        F.fill(feather_path(hx + 0.04 * hh, top_y + 0.02 * hh, hx - 1.1 * hh, top_y - 1.05 * hh, 0.40 * hh, bend=0.30 * hh), rim=1.0)
    F.fill(place(sp([KC(-0.36, 0.52), (-0.50, 0.15), (-0.46, -0.28), (-0.20, -0.56), (0.12, -0.60), (0.36, -0.46), (0.50, -0.12), (0.62, 0.14), (0.54, 0.36), (0.40, 0.58), (0.10, 0.66), KC(-0.14, 0.58)], True, 0.95), hx, hy, hh, rot), rim=1.0, glow=0.10)
    F.cut(place(sp([KC(0.16, -0.05), (0.42, -0.07), KC(0.60, 0.02), (0.58, 0.07), (0.40, 0.01), KC(0.16, 0.0)], True, 0.6), hx, hy, hh, rot))
    F.line(place(sp([(-0.10, -0.58), (0.0, -0.50), (0.20, -0.30), (0.34, -0.10)], False), hx, hy, hh, rot), hh * 0.03, tone=1.0, alpha=0.5)


def _rider(F, px, py, u, lance="up", charge=0.0, style="armor", lean_deg=0.0):
    """Zırhlı binici. (px,py) = eyerdeki kalça noktası (px), u = oturma boyu (kalça→baş tepesi, px). Sağa bakar.
    Gövde+bacak+kol alt-Fig'de çizilir (kalça etrafında lean_deg derece döner); mızrak dönmez."""
    R = Fig(F.h)

    def P(x, y):
        return (x * u, y * u)

    def KP(x, y):
        return KC(x * u, y * u)
    # uzak bacak (at gövdesinin arkasında; yalnız alt kısmı görünür)
    R.fill(limb([P(0.02, 0.05), P(0.30, 0.30), P(0.17, 0.88)], [0.30 * u, 0.23 * u, 0.17 * u], cap0=0.4, cap1=0.3), rim=0.4)
    R.fill(shoe(0.15 * u, 0.92 * u, 0.28 * u, 0.10 * u, 1, "sharp"), rim=0.4)
    # eyer: arka kabara + ön topuz
    R.fill(sp([KP(-0.30, -0.36), P(-0.34, -0.12), P(-0.22, 0.08), KP(0.0, 0.10), P(-0.12, -0.10), P(-0.16, -0.30)], True, 0.9), rim=1.0)
    R.fill(sp([KP(0.20, -0.10), P(0.26, 0.0), KP(0.24, 0.12), P(0.12, 0.10), P(0.14, -0.02)], True, 0.8), rim=0.9)
    # gövde (zırh): sırt-kalça-göğüs
    R.fill(sp([KP(-0.06, -0.72), P(-0.19, -0.64), P(-0.24, -0.42), P(-0.22, -0.18), KP(-0.18, 0.0), KP(0.21, 0.0), P(0.25, -0.20), P(0.26, -0.42), P(0.19, -0.64), P(0.09, -0.72)], True, 0.95), rim=1.0, glow=0.12)
    R.line(sp([P(0.07, -0.71), P(0.17, -0.42), P(0.11, -0.12)], False), u * 0.025, tone=1.0, alpha=0.5)
    for k in range(3):
        R.fill(sp([KP(-0.19 + k * 0.01, -0.02 + k * 0.10), P(0.0, 0.03 + k * 0.10), KP(0.26 - k * 0.01, -0.02 + k * 0.10), P(0.24, 0.08 + k * 0.10), P(0.0, 0.12 + k * 0.10), P(-0.17, 0.08 + k * 0.10)], True), rim=0.9)
    R.fill(sp([P(-0.23, -0.70), P(-0.11, -0.79), P(0.05, -0.77), P(0.07, -0.64), P(-0.07, -0.53), P(-0.23, -0.55)], True), rim=1.0)
    # yakın bacak: uyluk → diz (poleyn) → kaval → ayak (üzengide)
    R.fill(limb([P(0.0, 0.05), P(0.33, 0.30), P(0.20, 0.90)], [0.32 * u, 0.25 * u, 0.19 * u], cap0=0.4, cap1=0.3), rim=1.0)
    R.fill(sp([KP(0.26, 0.19), P(0.44, 0.23), P(0.46, 0.39), P(0.30, 0.45), KP(0.21, 0.34)], True, 0.8), rim=1.0)
    R.fill(shoe(0.17 * u, 0.95 * u, 0.32 * u, 0.11 * u, 1, "sharp"), rim=1.0)
    R.line(sp([P(0.08, 0.06), P(0.14, 0.50), P(0.20, 0.92)], False), u * 0.02, tone=0.9, alpha=0.7)
    # yakın kol
    hand = P(0.30, -0.30) if lance == "couched" else P(0.36, -0.22)
    R.fill(limb([P(-0.02, -0.63), P(-0.17, -0.38), hand], [0.20 * u, 0.20 * u, 0.14 * u], cap0=0.4, cap1=0.3), rim=1.0)
    R.fill(sp([P(-0.24, -0.46), P(-0.14, -0.50), P(-0.08, -0.40), P(-0.16, -0.30), P(-0.25, -0.34)], True), rim=1.0)
    R.fill(K.hand_pt("fist", hand[0] - 0.02 * u, hand[1], 0.22 * u, -10), rim=1.0)
    # boyun + miğfer
    R.fill(limb([P(0.02, -0.80), P(0.02, -0.72)], [0.13 * u, 0.17 * u], cap0=0, cap1=0), rim=0.9)
    _armet(R, 0.05 * u, -0.91 * u, 0.215 * u, plume=True, rot=-2.0 if lance == "couched" else 0.0)
    # lance (dönmeden): ayrı alt-Fig
    Lc = Fig(F.h)
    lx = lambda x, y: (x * u, y * u)
    if lance == "angled":                     # Tiziano tarzı: el eyerde, mızrak ileri-yukarı eğik; ucunda flama
        x0, y0 = lx(0.02, 0.80)
        x1, y1 = lx(1.10, -2.30)
        Lc.fill(bar(x0, y0, x1, y1, 0.07 * u, 0.045 * u), rim=0.95)
        dx, dy = x1 - x0, y1 - y0
        Ln = math.hypot(dx, dy)
        ux, uy = dx / Ln, dy / Ln
        nx, ny = -uy, ux
        Lc.fill(sp([KC(x1 - ux * 0.02 * u - nx * 0.05 * u, y1 - uy * 0.02 * u - ny * 0.05 * u), (x1 + ux * 0.14 * u - nx * 0.065 * u, y1 + uy * 0.14 * u - ny * 0.065 * u), KC(x1 + ux * 0.42 * u, y1 + uy * 0.42 * u),
                    (x1 + ux * 0.14 * u + nx * 0.065 * u, y1 + uy * 0.14 * u + ny * 0.065 * u), KC(x1 - ux * 0.02 * u + nx * 0.05 * u, y1 - uy * 0.02 * u + ny * 0.05 * u)], True), rim=1.0)
        bx, by = x1 - ux * 0.50 * u, y1 - uy * 0.50 * u
        Lc.fill(sp([KC(bx, by), (bx - 0.28 * u, by - 0.02 * u), KC(bx - 0.60 * u, by - 0.04 * u), (bx - 0.40 * u, by + 0.10 * u), KC(bx - 0.62 * u, by + 0.24 * u), (bx - 0.30 * u, by + 0.20 * u), KC(bx + 0.02 * u, by + 0.22 * u)], True, 0.8), rim=1.0)
    elif lance == "up":
        Lc.fill(bar(*lx(0.36, 0.55), *lx(0.40, -2.35), 0.07 * u, 0.05 * u), rim=0.95)
        tx, ty = lx(0.40, -2.35)
        Lc.fill(sp([KC(tx - 0.05 * u, ty + 0.01 * u), (tx - 0.065 * u, ty - 0.14 * u), KC(tx, ty - 0.40 * u), (tx + 0.065 * u, ty - 0.14 * u), KC(tx + 0.05 * u, ty + 0.01 * u)], True), rim=1.0)
        fy = ty + 0.30 * u
        Lc.fill(sp([KC(tx + 0.04 * u, fy), (tx + 0.40 * u, fy + 0.05 * u), (tx + 0.82 * u, fy - 0.02 * u), (tx + 0.62 * u, fy + 0.20 * u), (tx + 0.84 * u, fy + 0.40 * u), (tx + 0.42 * u, fy + 0.36 * u), KC(tx + 0.04 * u, fy + 0.42 * u)], True, 0.8), rim=1.0)
        Lc.line(poly([(tx + 0.10 * u, fy + 0.08 * u), (tx + 0.55 * u, fy + 0.12 * u)], False), u * 0.02, tone=1.0, alpha=0.5)
    else:
        x0, y0 = lx(-0.60, 0.05)
        x1, y1 = lx(3.5, 0.50 + charge)
        Lc.fill(bar(x0, y0, x1, y1, 0.085 * u, 0.04 * u), rim=0.95)
        dx, dy = x1 - x0, y1 - y0
        Ln = math.hypot(dx, dy)
        ux, uy = dx / Ln, dy / Ln
        nx, ny = -uy, ux
        Lc.fill(sp([KC(x1 - ux * 0.02 * u, y1 - uy * 0.02 * u), (x1 + ux * 0.22 * u + nx * 0.06 * u, y1 + uy * 0.22 * u + ny * 0.06 * u), KC(x1 + ux * 0.62 * u, y1 + uy * 0.62 * u), (x1 + ux * 0.22 * u - nx * 0.06 * u, y1 + uy * 0.22 * u - ny * 0.06 * u)], True), rim=1.0)
        # flama: mızrağa boydan bağlı kenarı (hoist) mızrak üzerinde; gövdesi rüzgârla geriye-aşağıya savrulan çatal kuyruklu
        bx, by = x1 - ux * 0.55 * u, y1 - uy * 0.55 * u
        Lc.fill(sp([KC(bx, by + 0.012 * u), (bx - 0.22 * u, by - 0.035 * u), KC(bx - 0.55 * u, by - 0.085 * u), (bx - 0.78 * u, by - 0.04 * u), KC(bx - 1.12 * u, by + 0.02 * u),
                    (bx - 0.93 * u, by + 0.14 * u), KC(bx - 1.16 * u, by + 0.30 * u), (bx - 0.80 * u, by + 0.26 * u), (bx - 0.45 * u, by + 0.21 * u), KC(bx, by + 0.20 * u)], True, 0.7), rim=1.0)
        Lc.line(poly([(bx - 0.08 * u, by + 0.07 * u), (bx - 0.62 * u, by + 0.05 * u)], False), u * 0.02, tone=1.0, alpha=0.5)
    F.merge(R, dx=px, dy=py, rot=lean_deg)
    F.merge(Lc, dx=px, dy=py)


def _caparison(F, h, hem=-0.30, col_tone=0.04, trim=True):
    """At örtüsü (kapariş): sırt-sağrı-karın boyunca asılı, ucu dilimli."""
    pts = [KC(0.18 * h, -0.755 * h), (0.0 * h, -0.735 * h), (-0.25 * h, -0.755 * h), (-0.48 * h, -0.74 * h), (-0.58 * h, -0.62 * h), (-0.57 * h, -0.45 * h)]
    # alt kenar dilimleri
    n = 8
    for i in range(n + 1):
        u = i / n
        x = -0.56 + (0.37 - -0.56) * u
        y = hem + 0.0 + 0.03 * math.sin(u * math.pi * n)
        pts.append((x * h, y * h) if (i % 2 == 0) else (x * h, (y + 0.05) * h))
    pts += [(0.34 * h, -0.44 * h), (0.31 * h, -0.62 * h)]
    F.fill(sp(pts, True, 0.9), rim=0.9, tone=col_tone)
    if trim:
        F.line(sp([(-0.57 * h, -0.45 * h), (-0.40 * h, hem * h), (-0.2 * h, (hem + 0.03) * h), (0.0, hem * h), (0.2 * h, (hem + 0.03) * h), (0.35 * h, -0.44 * h)], False), h * 0.005, tone=1.0, alpha=0.55)
    for x in (-0.38, -0.22, -0.06, 0.10, 0.24):
        F.crease((x * h, -0.72 * h), ((x - 0.01) * h, (hem + 0.02) * h), 0.008 * h, 0.01 * h, alpha=0.5)


def _rider_sipahi(F, px, py, u, lean_deg=0.0, sword_up=True):
    """Osmanlı sipahisi: sarıklı, kaftanlı, sırtta yuvarlak kalkan, havada kılıç (kılıç = kavisli). Sağa bakar."""
    R = Fig(F.h)

    def P(x, y):
        return (x * u, y * u)

    def KP(x, y):
        return KC(x * u, y * u)
    # sırtta yuvarlak kalkan (arkada)
    cx_, cy_, rr = -0.34 * u, -0.38 * u, 0.30 * u
    R.fill(ell(cx_, cy_, rr, rr), rim=1.0, glow=0.10)
    R.line(sp([(cx_ - rr * 0.72, cy_), (cx_, cy_ - rr * 0.72), (cx_ + rr * 0.72, cy_), (cx_, cy_ + rr * 0.72), (cx_ - rr * 0.72, cy_)], False), u * 0.02, tone=1.0, alpha=0.55)
    R.fill(ell(cx_, cy_, rr * 0.28, rr * 0.28), rim=0.0, tone=1.0, alpha=0.45, bound=False)
    # uzak bacak (çizme)
    R.fill(limb([P(0.02, 0.05), P(0.28, 0.30), P(0.16, 0.88)], [0.26 * u, 0.19 * u, 0.14 * u], cap0=0.4, cap1=0.3), rim=0.4)
    R.fill(shoe(0.14 * u, 0.92 * u, 0.26 * u, 0.09 * u, 1, "sharp"), rim=0.4)
    # eyer
    R.fill(sp([KP(-0.28, -0.34), P(-0.32, -0.10), P(-0.20, 0.08), KP(0.0, 0.10), P(-0.12, -0.10), P(-0.15, -0.28)], True, 0.9), rim=1.0)
    R.fill(sp([KP(0.20, -0.10), P(0.26, 0.0), KP(0.24, 0.12), P(0.12, 0.10), P(0.14, -0.02)], True, 0.8), rim=0.9)
    # kaftan: omuzlar → bel → dalgalı etek (kalçayı örter, geriye savrulur)
    R.fill(sp([KP(-0.06, -0.72), P(-0.19, -0.64), P(-0.22, -0.40), P(-0.20, -0.18), P(-0.30, 0.0), KP(-0.46, 0.06), P(-0.30, 0.12), P(-0.10, 0.14), P(0.12, 0.16), P(0.30, 0.14), KP(0.38, 0.06),
               P(0.28, -0.10), P(0.24, -0.22), P(0.24, -0.42), P(0.18, -0.64), P(0.08, -0.72)], True, 0.95), rim=1.0, glow=0.10)
    R.fill(poly([P(-0.21, -0.26), P(0.25, -0.26), P(0.25, -0.17), P(-0.20, -0.17)]), rim=0.5, tone=0.2, bound=False)
    R.crease(P(-0.10, -0.15), P(-0.34, 0.08), 0.02 * u, 0.04 * u)
    R.crease(P(0.06, -0.15), P(0.04, 0.14), 0.018 * u, 0.02 * u)
    R.crease(P(0.20, -0.14), P(0.30, 0.10), 0.015 * u, -0.02 * u)
    # yakın bacak: çizme
    R.fill(limb([P(0.04, 0.10), P(0.32, 0.30), P(0.19, 0.90)], [0.28 * u, 0.20 * u, 0.15 * u], cap0=0.4, cap1=0.3), rim=1.0)
    R.fill(shoe(0.17 * u, 0.95 * u, 0.30 * u, 0.10 * u, 1, "sharp"), rim=1.0)
    R.line(sp([P(0.08, 0.10), P(0.14, 0.50), P(0.19, 0.92)], False), u * 0.02, tone=0.9, alpha=0.7)
    # kılıç kolu: yukarı kaldırılmış
    hand = P(0.50, -1.12) if sword_up else P(0.34, -0.30)
    elbow = P(0.34, -0.80) if sword_up else P(-0.14, -0.40)
    R.fill(limb([P(0.0, -0.63), elbow, hand], [0.19 * u, 0.18 * u, 0.12 * u], cap0=0.4, cap1=0.3), rim=1.0)
    R.fill(K.hand_pt("fist", hand[0] - 0.02 * u, hand[1] + 0.02 * u, 0.2 * u, -90 if sword_up else -10), rim=1.0)
    # boyun + sarık + sorguç (tüy)
    R.fill(limb([P(0.02, -0.80), P(0.02, -0.72)], [0.13 * u, 0.17 * u], cap0=0, cap1=0), rim=0.9)
    add_head(R, 0.07 * u, -0.935 * u, 0.25 * u, "m", rot=-3.0, beard="stache", hat="turban", nose=1.1, hat_rot=-3.0)
    # kılıç (kilij): kavisli bıçak
    if sword_up:
        bx, by = P(0.50, -1.12)
        R.fill(sp([KC(bx - 0.03 * u, by - 0.02 * u), (bx + 0.06 * u, by - 0.26 * u), (bx + 0.20 * u, by - 0.50 * u), (bx + 0.44 * u, by - 0.68 * u), KC(bx + 0.70 * u, by - 0.74 * u),
                   (bx + 0.50 * u, by - 0.56 * u), (bx + 0.28 * u, by - 0.38 * u), (bx + 0.14 * u, by - 0.16 * u), KC(bx + 0.04 * u, by + 0.0)], True, 0.9), rim=1.0)
        R.fill(bar(bx - 0.08 * u, by + 0.0 * u, bx + 0.10 * u, by - 0.08 * u, 0.035 * u, 0.035 * u, True, True), rim=1.0)
    F.merge(R, dx=px, dy=py, rot=lean_deg)


def _horse_with_rider(h, lean, pose, lance, cloth=False, charge=0.0, rot=None, sipahi=False):
    """h = zeminden binici başlığına toplam boy; at kulak yüksekliği hs = h/1.2, binici oturma boyu u = 0.45·hs (gerçekçi oran: ≈1.55 m withers, ≈0.9 m oturan gövde+baş)."""
    F = Fig(h, lean)
    hs = h / 1.2
    H = Fig(hs)
    horse_body(H, hs, pose, mane=True, tail=True, bridle=True)
    if cloth:
        _caparison(H, hs)
    R = pose.get("rot", 0.0) if rot is None else rot
    F.merge(H, 0, 0, 1.0, rot=R)
    m = skia.Matrix()
    m.setRotate(R)
    q = m.mapXY(-0.005 * hs, -0.735 * hs)
    u = 0.45 * hs
    if sipahi:
        _rider_sipahi(F, q.x(), q.y(), u, lean_deg=5.0)
    else:
        _rider(F, q.x(), q.y(), u, lance=lance, charge=charge, lean_deg=(7.0 if lance == 'couched' else 0.0))
    return F


@fx("horse_rider")
def _horse_rider(h, lean):
    return _horse_with_rider(h, lean, HORSE_STAND, "up", cloth=True).build()


@fx("horse_rider_walk")
def _horse_rider_walk(h, lean):
    """Yürüyen at + zırhlı binici, mızrak ileri-yukarı eğik (Mühlberg/Tiziano tarzı duruş)."""
    return _horse_with_rider(h, lean, HORSE_WALK, "angled", cloth=True).build()


@fx("cavalry_charge")
def _cavalry_charge(h, lean):
    return _horse_with_rider(h, lean, GALLOP_A, "couched", cloth=False, charge=0.12).build()


@fx("cavalry_charge_b")
def _cavalry_charge_b(h, lean):
    return _horse_with_rider(h, lean, GALLOP_B, "couched", cloth=False, charge=0.05).build()


@fx("sipahi")
def _sipahi(h, lean):
    return _horse_with_rider(h, lean, GALLOP_A, None, cloth=True, sipahi=True).build()


@fx("sipahi_b")
def _sipahi_b(h, lean):
    return _horse_with_rider(h, lean, GALLOP_B, None, cloth=True, sipahi=True).build()
