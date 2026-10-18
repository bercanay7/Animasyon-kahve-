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
        tp = [(-0.55, -0.70 + dy), (-0.61, -0.65 + dy), (-0.70, -0.55), (-0.735, -0.43), (-0.72, -0.31), (-0.69, -0.23)]
        F.fill(limb([(x * h, y * h) for x, y in tp], [0.04 * h, 0.085 * h, 0.095 * h, 0.08 * h, 0.045 * h, 0.01 * h], cap0=0.4, cap1=0.0), rim=0.9)
        F.crease((-0.64 * h, -0.60 * h), (-0.73 * h, -0.30 * h), 0.008 * h, 0.012 * h, alpha=0.5)
        F.crease((-0.67 * h, -0.62 * h), (-0.70 * h, -0.28 * h), 0.006 * h, -0.01 * h, alpha=0.4)
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
        F.fill(_mane(h, ey), rim=1.0)
        F.fill(sp(_hp([KC(0.545, -1.0 + ey), (0.59, -1.02 + ey), (0.612, -0.97 + ey), (0.59, -0.93 + ey), (0.565, -0.965 + ey)], h), True, 0.8), rim=1.0)          # perçem
    for k in ("hn", "fn"):
        _leg(F, L[k], (0.095, 0.058, 0.034, 0.052), h, rim=1.0)
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
