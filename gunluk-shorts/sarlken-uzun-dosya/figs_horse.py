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
HORSE_STAND = dict(
    legs=dict(
        fn=[(0.30, -0.50), (0.325, -0.30), (0.335, -0.21), (0.34, -0.10), (0.345, 0.0)],            # ön yakın
        ff=[(0.235, -0.50), (0.228, -0.30), (0.222, -0.21), (0.22, -0.10), (0.218, 0.0)],           # ön uzak
        hn=[(-0.405, -0.62), (-0.46, -0.40), (-0.54, -0.255), (-0.495, -0.14), (-0.478, -0.065), (-0.47, 0.0)],   # arka yakın
        hf=[(-0.34, -0.58), (-0.36, -0.38), (-0.405, -0.26), (-0.365, -0.14), (-0.35, -0.065), (-0.345, 0.0)]),  # arka uzak
    head=0.0, tail=0.0)

HORSE_WALK = dict(
    legs=dict(
        fn=[(0.30, -0.50), (0.37, -0.31), (0.42, -0.245), (0.40, -0.13), (0.385, -0.07)],            # ön yakın: havada, diz bükük
        ff=[(0.235, -0.50), (0.225, -0.30), (0.215, -0.21), (0.21, -0.10), (0.205, 0.0)],
        hn=[(-0.405, -0.62), (-0.50, -0.40), (-0.60, -0.28), (-0.63, -0.15), (-0.645, -0.07), (-0.65, 0.0)],      # arka yakın: geride itiş
        hf=[(-0.34, -0.58), (-0.33, -0.38), (-0.34, -0.26), (-0.30, -0.14), (-0.285, -0.065), (-0.28, 0.0)]),
    head=-0.02, tail=0.0)


def _leg(F, pts, w, h, rim=0.9, hoof=True, tone=0.0):
    """At bacağı: pts (x,y) h oranı, w=(üst, diz/hock, bilek, tırnak). Tırnak sonda."""
    P = [(x * h, y * h) for (x, y) in pts]
    n = len(P)
    ws = []
    for i in range(n):
        u = i / (n - 1)
        if u < 0.3:
            ww = w[0] + (w[1] - w[0]) * (u / 0.3)
        elif u < 0.62:
            ww = w[1] + (w[2] - w[1]) * ((u - 0.3) / 0.32)
        elif u < 0.88:
            ww = w[2] * 1.2
        else:
            ww = w[3]
        ws.append(ww * h)
    F.fill(limb(P, ws, cap0=0.4, cap1=0.0 if hoof else 0.4), rim=rim, tone=tone)
    if hoof:
        x, y = P[-1]
        F.fill(sp([KC(x - ws[-1] * 0.55, y - ws[-1] * 0.9), (x + ws[-1] * 0.60, y - ws[-1] * 0.85), KC(x + ws[-1] * 0.95, y), KC(x - ws[-1] * 0.60, y)], True, 0.8), rim=rim)


def _hp(pts, h):
    return [((q[0] * h, q[1] * h, "c") if len(q) > 2 else (q[0] * h, q[1] * h)) for q in pts]


def _mane(h, ey=0.0, flick=0.55, long=0.85):
    """Yele: boyun üst çizgisine yapışık, geriye savrulan sivri tutamlı dalgalı şerit."""
    T = [(0.20, -0.755), (0.28, -0.82), (0.35, -0.90), (0.42, -0.96), (0.485, -0.995), (0.525, -1.005 + ey)]
    out_pts, in_pts = [], []
    for i, (x, y) in enumerate(T):
        j0, j1 = max(0, i - 1), min(len(T) - 1, i + 1)
        tx, ty = T[j1][0] - T[j0][0], T[j1][1] - T[j0][1]
        L = math.hypot(tx, ty) or 1
        nx, ny = ty / L, -tx / L
        in_pts.append((x - nx * 0.03, y - ny * 0.03))
        d = (0.055 + (0.022 if i % 2 == 0 else 0.0)) * long
        out_pts.append(((x + nx * d - 0.05 * flick * (0.4 if i == 0 else 1.0)) * h, (y + ny * d + 0.012 * (0.0 if i == 0 else 1.0)) * h))
        if i < len(T) - 1:
            mx, my = (x + T[i + 1][0]) / 2, (y + T[i + 1][1]) / 2
            out_pts.append(((mx + nx * 0.025 - 0.012) * h, (my + ny * 0.025) * h, "c") if False else ((mx + nx * 0.026 - 0.014 * flick) * h, (my + ny * 0.026) * h))
    pts = [KC(*in_pts[-1])] if False else []
    seq = [(in_pts[-1][0] * h, in_pts[-1][1] * h, "c")]
    seq += [((q[0], q[1], "c") if (k % 2 == 0) else (q[0], q[1])) for k, q in enumerate(out_pts[::-1])]
    seq += [(q[0] * h, q[1] * h) for q in in_pts[::-1]]
    return sp(seq, True, 0.9)


def horse_body(F, h, pose=HORSE_STAND, mane=True, tail=True, bridle=True, dy=0.0):
    """At: bacaklar + gövde/boyun/baş + yele + kuyruk. h = kulak ucu yüksekliği."""
    L = pose["legs"]
    hd = pose.get("head", 0.0)
    for k in ("ff", "hf"):
        _leg(F, L[k], (0.085, 0.052, 0.032, 0.05), h, rim=0.45)
    if tail:
        if pose.get("tail_stream", 0.0) > 0:      # dörtnalada kuyruk arkaya savrulur
            ts = pose["tail_stream"]
            tp = [(-0.55, -0.70 + dy), (-0.66, -0.71 + dy), (-0.80, -0.69 + 0.02 * ts), (-0.93, -0.64 + 0.04 * ts), (-1.04, -0.60 + 0.05 * ts), (-1.12, -0.62)]
            F.fill(limb([(x * h, y * h) for x, y in tp], [0.045 * h, 0.085 * h, 0.095 * h, 0.08 * h, 0.05 * h, 0.012 * h], cap0=0.4, cap1=0.0), rim=0.9)
            F.crease((-0.70 * h, -0.72 * h), (-1.02 * h, -0.62 * h), 0.008 * h, 0.012 * h, alpha=0.5)
            F.crease((-0.72 * h, -0.67 * h), (-1.05 * h, -0.60 * h), 0.006 * h, -0.01 * h, alpha=0.4)
        else:
            tp = [(-0.55, -0.70 + dy), (-0.61, -0.65 + dy), (-0.70, -0.55), (-0.735, -0.43), (-0.72, -0.31), (-0.69, -0.23)]
            F.fill(limb([(x * h, y * h) for x, y in tp], [0.04 * h, 0.085 * h, 0.095 * h, 0.08 * h, 0.045 * h, 0.01 * h], cap0=0.4, cap1=0.0), rim=0.9)
            F.crease((-0.64 * h, -0.60 * h), (-0.73 * h, -0.30 * h), 0.008 * h, 0.012 * h, alpha=0.5)
            F.crease((-0.67 * h, -0.62 * h), (-0.70 * h, -0.28 * h), 0.006 * h, -0.01 * h, alpha=0.4)
    for k in ("hn", "fn"):
        _leg(F, L[k], (0.095, 0.058, 0.034, 0.052), h, rim=1.0)
    pts = [
        (-0.555, -0.70 + dy), (-0.50, -0.74 + dy), (-0.40, -0.76 + dy), (-0.20, -0.745 + dy), (0.0, -0.72 + dy), (0.12, -0.735 + dy), (0.205, -0.75 + dy),      # sırt → omuz başı
        (0.28, -0.815), (0.35, -0.90), (0.42, -0.96), (0.48, -0.995), (0.525, -1.005 + hd * 0.2),                                                           # boyun üstü (kavisli) → ense
        (0.575, -0.995 + hd * 0.3), (0.62, -0.955 + hd * 0.6), (0.665, -0.905 + hd), (0.71, -0.85 + hd), (0.745, -0.805 + hd),                               # alın → burun köprüsü
        (0.765, -0.775 + hd), (0.757, -0.735 + hd), (0.722, -0.715 + hd), (0.686, -0.726 + hd * 0.9),                                                          # burun ucu, dudak, çene
        (0.652, -0.765 + hd * 0.5), (0.62, -0.80 + hd * 0.2), (0.58, -0.845), (0.54, -0.865),                                                                  # alt çene, yanak, boğaz
        (0.49, -0.80), (0.458, -0.71), (0.44, -0.62), (0.43, -0.52),                                                                                            # boyun altı → göğüs
        (0.385, -0.42), (0.30, -0.37), (0.15, -0.335), (0.0, -0.335), (-0.15, -0.36), (-0.28, -0.41), (-0.42, -0.45),                                          # göğüs altı → karın → kasık
        (-0.54, -0.50), (-0.60, -0.58), (-0.60, -0.65),
    ]
    # kulaklar (başın arkasında, iri yaprak biçimli)
    ey = hd * 0.2
    F.fill(sp(_hp([KC(0.485, -0.99 + ey), (0.472, -1.05 + ey), KC(0.497, -1.11 + ey), (0.526, -1.05 + ey), KC(0.54, -0.995 + ey)], h), True, 0.8), rim=0.8)
    F.fill(sp(_hp([KC(0.535, -0.995 + ey), (0.535, -1.05 + ey), KC(0.568, -1.105 + ey), (0.59, -1.04 + ey), KC(0.59, -0.99 + ey)], h), True, 0.8), rim=1.0)
    F.fill(sp(_hp(pts, h), True, 1.0), rim=1.0, glow=0.08)
    if mane:
        F.fill(_mane(h, ey, flick=pose.get('mane_flick', 0.55), long=pose.get('mane_long', 0.85)), rim=1.0)
        F.fill(sp(_hp([KC(0.545, -1.0 + ey), (0.59, -1.02 + ey), (0.612, -0.97 + ey), (0.59, -0.93 + ey), (0.565, -0.965 + ey)], h), True, 0.8), rim=1.0)          # perçem
    # kafa kayışı + göz çizgisi
    if bridle:
        F.line(sp(_hp([(0.655, -0.905 + hd), (0.605, -0.865 + hd * 0.3), (0.56, -0.88)], h), False), h * 0.0035, tone=0.9, alpha=0.6)
        F.line(sp(_hp([(0.705, -0.80 + hd), (0.64, -0.83 + hd * 0.4)], h), False), h * 0.0035, tone=0.9, alpha=0.6)
        F.line(sp(_hp([(0.60, -0.95 + hd * 0.5), (0.575, -0.89)], h), False), h * 0.0035, tone=0.9, alpha=0.5)


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


# ───────────────────────────── gallop pozları ─────────────────────────────
GALLOP_A = dict(     # uzamış (iki ön bacak ileri, arka bacaklar geride, arka toynak itişte)
    legs=dict(
        fn=[(0.30, -0.50), (0.40, -0.43), (0.55, -0.37), (0.67, -0.31), (0.745, -0.28)],
        ff=[(0.235, -0.50), (0.33, -0.45), (0.46, -0.41), (0.58, -0.36), (0.655, -0.33)],
        hn=[(-0.405, -0.62), (-0.52, -0.50), (-0.65, -0.37), (-0.76, -0.22), (-0.815, -0.075)],
        hf=[(-0.34, -0.58), (-0.44, -0.48), (-0.56, -0.38), (-0.66, -0.28), (-0.72, -0.16)]),
    head=0.045, tail_stream=1.0, mane_flick=1.5, mane_long=1.0, rot=2.0)

GALLOP_B = dict(     # toplanmış (bacaklar gövde altında, ön yakın bacak iniyor)
    legs=dict(
        fn=[(0.30, -0.50), (0.37, -0.36), (0.40, -0.22), (0.415, -0.10), (0.42, -0.03)],
        ff=[(0.235, -0.50), (0.30, -0.40), (0.385, -0.31), (0.335, -0.20), (0.285, -0.155)],
        hn=[(-0.405, -0.62), (-0.355, -0.46), (-0.295, -0.32), (-0.34, -0.20), (-0.275, -0.16)],
        hf=[(-0.34, -0.58), (-0.28, -0.45), (-0.20, -0.34), (-0.25, -0.22), (-0.17, -0.18)]),
    head=-0.04, tail_stream=0.6, mane_flick=1.2, mane_long=1.0, rot=-3.0)


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
    if lance == "up":
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
    hand = P(0.22, -0.98) if sword_up else P(0.34, -0.30)
    elbow = P(0.14, -0.80) if sword_up else P(-0.14, -0.40)
    R.fill(limb([P(0.0, -0.63), elbow, hand], [0.19 * u, 0.18 * u, 0.12 * u], cap0=0.4, cap1=0.3), rim=1.0)
    R.fill(K.hand_pt("fist", hand[0] - 0.02 * u, hand[1] + 0.02 * u, 0.2 * u, -90 if sword_up else -10), rim=1.0)
    # boyun + sarık + sorguç (tüy)
    R.fill(limb([P(0.02, -0.80), P(0.02, -0.72)], [0.13 * u, 0.17 * u], cap0=0, cap1=0), rim=0.9)
    add_head(R, 0.06 * u, -0.91 * u, 0.215 * u, "m", rot=-3.0, beard="stache", hat="turban", nose=1.1, hat_rot=-3.0)
    R.fill(feather_path(0.10 * u, -1.22 * u, 0.20 * u, -1.52 * u, 0.07 * u, bend=-0.03 * u), rim=1.0)
    R.fill(ell(0.10 * u, -1.22 * u, 0.025 * u, 0.025 * u), rim=1.0, tone=0.4)
    # kılıç (kilij): kavisli bıçak
    if sword_up:
        bx, by = P(0.22, -0.98)
        R.fill(sp([KC(bx - 0.03 * u, by - 0.02 * u), (bx + 0.10 * u, by - 0.22 * u), (bx + 0.30 * u, by - 0.40 * u), (bx + 0.55 * u, by - 0.50 * u), KC(bx + 0.78 * u, by - 0.50 * u),
                   (bx + 0.58 * u, by - 0.39 * u), (bx + 0.34 * u, by - 0.29 * u), (bx + 0.16 * u, by - 0.13 * u), KC(bx + 0.04 * u, by + 0.0)], True, 0.9), rim=1.0)
        R.fill(bar(bx - 0.08 * u, by + 0.0 * u, bx + 0.10 * u, by - 0.08 * u, 0.035 * u, 0.035 * u, True, True), rim=1.0)
    F.merge(R, dx=px, dy=py, rot=lean_deg)


def _horse_with_rider(h, lean, pose, lance, cloth=False, charge=0.0, rot=None, sipahi=False):
    """h = zeminden binici başlığına toplam boy; at ölçeği atın kulak yüksekliği 0.70 h olacak biçimde."""
    F = Fig(h, lean)
    hs = h * 0.70
    H = Fig(hs)
    horse_body(H, hs, pose, mane=True, tail=True, bridle=True)
    if cloth:
        _caparison(H, hs)
    R = pose.get("rot", 0.0) if rot is None else rot
    F.merge(H, 0, 0, 1.0, rot=R)
    m = skia.Matrix()
    m.setRotate(R)
    q = m.mapXY(-0.045 * hs, -0.735 * hs)
    u = 0.56 * hs
    if sipahi:
        _rider_sipahi(F, q.x(), q.y(), u, lean_deg=5.0)
    else:
        _rider(F, q.x(), q.y(), u, lance=lance, charge=charge, lean_deg=(7.0 if lance == 'couched' else 0.0))
    return F


@fx("horse_rider")
def _horse_rider(h, lean):
    return _horse_with_rider(h, lean, HORSE_STAND, "up", cloth=True).build()


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
