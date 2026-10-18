"""figs_parts — şapka/başlık, baş montajı, kürk, kol-el montajı, cüppe taslağı (figür-lab ortak parçaları).

Şapkalar baş-biriminde (baş yüksekliği 1; merkez 0; yüz +x; kafatası tepesi y=-0.5) yol listesi döndürür: [(yol, rim_gücü, ton)].
"""
import math

import skia

import figs_kit as K
from figs_kit import K as KC, Fig, bar, ell, feather_path, lens, limb, place, poly, sp

# ───────────────────────────── şapkalar ─────────────────────────────


def hat_parts(kind):
    """Baş-birimli şapka parçaları [(path, rim, tone)] (arkadan öne)."""
    P = []
    if kind == "beret":                       # Rönesans bareti: yassı, yana yatık, sol arkaya tüy
        P.append((feather_path(0.02, -0.70, -0.78, -0.98, 0.15, bend=-0.16), 1.0, 0.0))
        P.append((feather_path(0.10, -0.70, -0.55, -1.12, 0.12, bend=-0.20), 0.8, 0.0))
        P.append((sp([KC(0.37, -0.22), (0.47, -0.37), (0.38, -0.58), (0.12, -0.74), (-0.22, -0.72), (-0.50, -0.55), (-0.58, -0.30), KC(-0.50, -0.10), (-0.32, -0.22),
                      (-0.05, -0.28), (0.20, -0.25)], True, 0.9), 1.0, 0.0))
    elif kind == "flatcap":                   # tüccar/katip: yumuşak yuvarlak şapka, kıvrık kenarlı
        P.append((sp([KC(0.40, -0.17), (0.43, -0.30), (0.30, -0.52), (0.02, -0.62), (-0.30, -0.58), (-0.48, -0.36), (-0.46, -0.14), KC(-0.40, -0.05),
                      (-0.20, -0.17), (0.10, -0.20)], True, 0.9), 1.0, 0.0))
        P.append((sp([KC(0.44, -0.20), (0.46, -0.27), (0.36, -0.29), KC(0.30, -0.21)], True, 0.6), 0.9, 0.06))
    elif kind == "plume":                     # Landsknecht: geniş tabak şapka + tüyler
        for i, (dx, dy, wd, bd) in enumerate([(-0.95, -1.05, 0.26, -0.28), (-1.12, -0.80, 0.24, -0.30), (-0.78, -1.22, 0.22, -0.22), (-1.20, -0.55, 0.20, -0.26)]):
            P.append((feather_path(-0.02 - i * 0.04, -0.66, dx, dy, wd, bend=bd), 0.9, 0.0))
        P.append((sp([KC(0.46, -0.28), (0.82, -0.40), (0.78, -0.52), (0.30, -0.60), (-0.30, -0.66), (-0.84, -0.50), (-0.92, -0.36), KC(-0.60, -0.22), (-0.10, -0.30)], True, 0.9), 1.0, 0.0))
        P.append((sp([KC(0.30, -0.40), (0.26, -0.78), (-0.10, -0.90), (-0.46, -0.76), (-0.50, -0.50), KC(-0.20, -0.46)], True, 0.8), 1.0, 0.0))
    elif kind == "galero":                    # kardinal şapkası: çok geniş yassı kenar, alçak yuvarlak tepe, püsküllü kordonlar
        P.append((sp([KC(-1.25, -0.38), (-0.80, -0.47), (-0.2, -0.50), (0.5, -0.49), (1.0, -0.45), KC(1.30, -0.36), (1.0, -0.30), (0.5, -0.31), (-0.2, -0.31), (-0.8, -0.32)], True, 0.85), 1.0, 0.0))
        P.append((sp([KC(-0.46, -0.44), (-0.46, -0.62), (-0.22, -0.74), (0.12, -0.74), (0.40, -0.62), KC(0.48, -0.44)], True, 0.85), 1.0, 0.0))
        P.append((sp([KC(-0.46, -0.40), (0.0, -0.36), KC(0.48, -0.40), (0.48, -0.44), (0.0, -0.45), (-0.46, -0.44)], True, 0.6), 0.0, 0.14))
    elif kind == "cowl":                      # keşiş kukuletası: kafayı saran kütle + omuzlara düşen kıvrım + alın kenarı bandı
        P.append((sp([KC(0.20, -0.40), (0.02, -0.76), (-0.36, -0.86), (-0.66, -0.58), (-0.78, -0.12), (-0.92, 0.46), (-0.92, 1.00), (-0.66, 1.22), (-0.34, 1.12), KC(-0.14, 0.78),
                      (-0.30, 0.46), (-0.34, 0.20), (-0.20, -0.10)], True, 0.9), 1.0, 0.0, "back"))
        P.append((sp([KC(0.36, -0.30), (0.30, -0.50), (0.12, -0.68), (-0.14, -0.74), (-0.42, -0.62), (-0.52, -0.34), (-0.36, -0.40), (-0.12, -0.50), (0.10, -0.42), KC(0.24, -0.26)], True, 0.8), 1.0, 0.05))
    elif kind == "veil":                      # kadın örtüsü/tokası: alından omuza düşen kumaş
        P.append((sp([KC(0.33, -0.26), (0.22, -0.56), (-0.10, -0.66), (-0.44, -0.52), (-0.60, -0.10), (-0.70, 0.55), (-0.76, 1.25), (-0.50, 1.36), (-0.34, 0.95),
                      (-0.22, 0.55), KC(-0.16, 0.30), (-0.34, 0.10), (-0.34, -0.12), (0.0, -0.20)], True, 0.9), 1.0, 0.0))
        P.append((sp([KC(0.34, -0.26), (0.40, -0.10), KC(0.33, 0.10), (0.22, -0.10), (0.0, -0.20)], True, 0.7), 0.7, 0.0)) if False else None
    elif kind == "frenchhood":                # Fransız başlığı: arkada kavisli, kıvrık kenar + sarkan örtü
        P.append((sp([KC(0.20, -0.36), (0.02, -0.60), (-0.28, -0.64), (-0.52, -0.40), (-0.58, -0.05), (-0.66, 0.50), (-0.58, 1.05), KC(-0.30, 0.92), (-0.34, 0.40),
                      (-0.30, 0.02), (-0.14, -0.20), (0.04, -0.30)], True, 0.9), 1.0, 0.0))
        P.append((sp([KC(0.30, -0.30), (0.26, -0.52), (0.04, -0.66), (-0.22, -0.68), (-0.30, -0.60), (-0.06, -0.52), (0.14, -0.42)], True, 0.7), 1.0, 0.12))
    elif kind == "coif":                      # yakın kep (keten başlık)
        P.append((sp([KC(0.34, -0.28), (0.22, -0.54), (-0.10, -0.62), (-0.42, -0.46), (-0.52, -0.08), (-0.50, 0.30), (-0.36, 0.42), KC(-0.12, 0.32), (-0.30, 0.10),
                      (-0.28, -0.14), (0.0, -0.22)], True, 0.9), 1.0, 0.0))
    elif kind == "turban":                    # sarık
        P.append((sp([(0.0, -0.98), (0.40, -0.92), (0.66, -0.64), (0.70, -0.36), KC(0.44, -0.24), (0.0, -0.26), (-0.44, -0.24), KC(-0.66, -0.34), (-0.66, -0.62), (-0.40, -0.90)], True, 0.9), 1.0, 0.0))
        P.append((sp([KC(-0.50, -0.30), (-0.66, -0.12), (-0.70, 0.18), (-0.56, 0.20), KC(-0.46, -0.05)], True, 0.7), 0.9, 0.0))
    elif kind == "kavuk":                     # Osmanlı yüksek kavuk
        P.append((sp([KC(0.40, -0.22), (0.46, -0.50), (0.50, -0.90), (0.36, -1.16), (0.0, -1.22), (-0.36, -1.16), (-0.46, -0.90), (-0.44, -0.50), KC(-0.40, -0.22)], True, 0.9), 1.0, 0.0))
        P.append((sp([KC(0.42, -0.36), (0.0, -0.31), KC(-0.42, -0.36), (-0.42, -0.30), (0.0, -0.25), (0.42, -0.30)], True, 0.6), 0.0, 0.14))
    elif kind == "bork":                      # yeniçeri börkü: kısa koni gövde, sırtta sarkan geniş kollu uç, önde kaşıklık
        P.append((sp([KC(-0.30, -0.66), (-0.50, -0.50), (-0.72, -0.10), (-0.88, 0.40), (-0.92, 0.82), KC(-0.64, 0.98), (-0.40, 0.84), (-0.32, 0.40), (-0.30, 0.05), KC(-0.28, -0.12)], True, 0.9), 0.85, 0.0, "back"))
        P.append((sp([KC(0.34, -0.22), (0.42, -0.45), (0.40, -0.78), (0.24, -1.02), (-0.06, -1.10), (-0.34, -0.98), (-0.48, -0.70), (-0.50, -0.38), KC(-0.46, -0.16)], True, 0.9), 1.0, 0.0))
        P.append((sp([KC(0.30, -0.14), (0.46, -0.20), (0.52, -0.38), (0.42, -0.50), KC(0.30, -0.38)], True, 0.6), 1.0, 0.0))
        P.append((sp([KC(-0.46, -0.20), (0.0, -0.16), KC(0.34, -0.20), (0.34, -0.30), (0.0, -0.26), (-0.46, -0.30)], True, 0.6), 0.0, 0.14))
    elif kind == "morion":                    # İspanyol morion: yüksek sırt (comb), kayık biçimli kalkık kenar
        P.append((sp([KC(-0.82, -0.58), (-0.52, -0.34), (-0.12, -0.27), (0.30, -0.30), (0.62, -0.40), KC(0.95, -0.66), (0.66, -0.38), (0.30, -0.22), (-0.10, -0.19), (-0.50, -0.25)], True, 0.8), 1.0, 0.0))
        P.append((sp([KC(-0.42, -0.30), (-0.44, -0.58), (-0.22, -0.78), (0.10, -0.80), (0.36, -0.66), KC(0.44, -0.32)], True, 0.8), 1.0, 0.0))
        P.append((sp([KC(-0.38, -0.74), (-0.20, -0.96), (0.02, -1.10), (0.20, -0.96), (0.34, -0.74), (0.16, -0.78), (-0.04, -0.82), (-0.22, -0.80)], True, 0.8), 1.0, 0.0))
    elif kind == "sallet":                    # kasket (zırhsız piyade)
        P.append((sp([KC(-0.50, -0.20), (-0.50, -0.58), (-0.20, -0.80), (0.16, -0.78), (0.38, -0.55), KC(0.44, -0.22), (0.10, -0.30), (-0.30, -0.24)], True, 0.8), 1.0, 0.0))
        P.append((sp([KC(-0.40, -0.18), (-0.56, 0.06), (-0.62, 0.34), KC(-0.40, 0.30), (-0.34, 0.08)], True, 0.7), 0.9, 0.0))
    elif kind == "crown":                     # taç (açık kenar + haç)
        P.append((poly([(-0.34, -0.42), (-0.38, -0.82), (-0.20, -0.62), (-0.04, -0.92), (0.14, -0.62), (0.30, -0.84), (0.34, -0.42)]), 1.0, 0.0))
        P.append((poly([(-0.36, -0.42), (0.36, -0.42), (0.36, -0.34), (-0.36, -0.34)]), 1.0, 0.1))
    elif kind == "crown_i":                   # imparatorluk tacı: yay + haç
        P.append((sp([KC(-0.38, -0.40), (-0.40, -0.70), (-0.18, -0.96), (0.10, -1.02), (0.34, -0.84), KC(0.38, -0.40), (0.34, -0.60), (0.14, -0.84), (-0.12, -0.80), (-0.30, -0.62)], True, 0.9), 1.0, 0.0))
        P.append((poly([(-0.40, -0.44), (0.40, -0.44), (0.42, -0.30), (-0.42, -0.30)]), 1.0, 0.08))
        P.append((poly([(-0.02, -1.02), (0.02, -1.02), (0.02, -1.24), (-0.02, -1.24)]), 1.0, 0.0))
        P.append((poly([(-0.10, -1.14), (0.10, -1.14), (0.10, -1.10), (-0.10, -1.10)]), 1.0, 0.0))
    elif kind == "barrete_k":                 # kardinal/papaz bareti: üç dilimli kare
        P.append((poly([(-0.38, -0.30), (-0.40, -0.62), (-0.18, -0.70), (0.20, -0.70), (0.40, -0.62), (0.40, -0.30)]), 1.0, 0.0))
        P.append((poly([(-0.10, -0.70), (-0.08, -0.80), (0.10, -0.80), (0.12, -0.70)]), 1.0, 0.0))
    elif kind == "headband":                  # alın bandı + arkada dik tüy yelpazesi (Mezoamerika soylusu)
        P.append((feather_path(-0.30, -0.42, -0.78, -1.28, 0.20, bend=0.10), 1.0, 0.0, "back"))
        P.append((feather_path(-0.18, -0.44, -0.40, -1.40, 0.22, bend=0.05), 1.0, 0.0, "back"))
        P.append((feather_path(-0.05, -0.46, 0.00, -1.38, 0.20, bend=-0.05), 1.0, 0.0, "back"))
        P.append((sp([KC(0.35, -0.36), (0.20, -0.46), (-0.15, -0.50), (-0.44, -0.40), (-0.44, -0.30), (-0.14, -0.38), (0.20, -0.34), KC(0.34, -0.26)], True, 0.8), 1.0, 0.1))
    elif kind == "llauto":                    # İnka: sarılı baş bandı (llautu) + alında kırmızı saçak (mascaypacha) + öne dik iki tüy
        P.append((feather_path(0.18, -0.52, 0.34, -1.30, 0.17, bend=-0.10), 1.0, 0.0))
        P.append((feather_path(0.04, -0.52, 0.04, -1.36, 0.17, bend=0.08), 1.0, 0.0))
        P.append((sp([KC(0.36, -0.40), (0.26, -0.50), (-0.14, -0.54), (-0.47, -0.42), (-0.47, -0.22), (-0.16, -0.30), (0.26, -0.28), KC(0.37, -0.22)], True, 0.8), 1.0, 0.1))
        P.append((sp([KC(0.30, -0.30), (0.36, -0.20), (0.35, -0.04), (0.31, -0.02), (0.29, -0.16), KC(0.25, -0.28)], True, 0.6), 0.9, 0.0))
    elif kind == "crest":                     # Aztek savaşçı: geniş tüy yelpazesi (quetzal) + alın bandı
        for k in range(9):
            a = -1.15 + k * 0.30
            ex, ey = 0.10 + math.sin(a) * 1.15, -0.55 - math.cos(a) * 1.20
            P.append((feather_path(0.0 + 0.04 * k, -0.50, ex, ey, 0.17, bend=0.10 * math.sin(a)), 1.0, 0.0, "back"))
        P.append((sp([KC(0.36, -0.38), (0.24, -0.50), (-0.14, -0.55), (-0.46, -0.44), (-0.46, -0.26), (-0.14, -0.35), (0.24, -0.31), KC(0.36, -0.25)], True, 0.8), 1.0, 0.1))
    elif kind == "slouch":                    # sarkık kenarlı yüksek yumuşak şapka + tüy (arkebüzcü)
        P.append((feather_path(-0.1, -0.78, -0.88, -0.88, 0.18, bend=-0.20), 0.9, 0.0))
        P.append((sp([KC(-0.80, -0.30), (-0.50, -0.46), (0.0, -0.50), (0.55, -0.46), KC(0.92, -0.30), (0.60, -0.34), (0.0, -0.34), (-0.52, -0.36)], True, 0.8), 1.0, 0.0))
        P.append((sp([KC(-0.40, -0.40), (-0.40, -0.70), (-0.18, -0.92), (0.16, -0.94), (0.38, -0.74), KC(0.42, -0.40)], True, 0.8), 1.0, 0.0))
    elif kind == "straw":                     # köylü hasır şapkası
        P.append((sp([KC(-0.96, -0.30), (-0.56, -0.44), (0.0, -0.48), (0.56, -0.42), KC(1.0, -0.28), (0.56, -0.24), (0.0, -0.22), (-0.56, -0.24)], True, 0.8), 1.0, 0.0))
        P.append((sp([KC(-0.40, -0.40), (-0.36, -0.70), (-0.08, -0.82), (0.26, -0.72), KC(0.40, -0.40)], True, 0.8), 1.0, 0.0))
    elif kind == "woolcap":                   # balıkçı/denizci yün bere (öne eğik uç)
        P.append((sp([KC(0.38, -0.20), (0.40, -0.40), (0.24, -0.62), (-0.06, -0.72), (-0.36, -0.60), (-0.50, -0.34), (-0.48, -0.10), KC(-0.30, -0.14), (0.0, -0.24)], True, 0.9), 1.0, 0.0))
        P.append((sp([KC(0.30, -0.56), (0.44, -0.70), (0.60, -0.66), (0.66, -0.50), (0.50, -0.56), (0.36, -0.46)], True, 0.7), 1.0, 0.0))
    elif kind == "biretta":                   # alim/öğrenci dört köşeli bareti
        P.append((poly([(-0.40, -0.28), (-0.38, -0.60), (0.40, -0.62), (0.42, -0.30)]), 1.0, 0.0))
        P.append((poly([(-0.34, -0.60), (-0.30, -0.70), (0.36, -0.70), (0.40, -0.62)]), 1.0, 0.0))
    elif kind == "scholar":                   # bilgin kepi (yan kulaklıklı)
        P.append((sp([KC(0.38, -0.18), (0.40, -0.40), (0.20, -0.62), (-0.10, -0.68), (-0.40, -0.52), (-0.50, -0.20), (-0.46, 0.18), KC(-0.30, 0.20), (-0.30, -0.06), (0.0, -0.22)], True, 0.9), 1.0, 0.0))
    return [p for p in P if p]


def add_hat(F, kind, hx, hy, hh, rot=0.0, back=None):
    """back=None: hepsi; back=True: yalnız 'back' (kafanın arkasında) parçalar; back=False: ön parçalar."""
    for part in hat_parts(kind):
        path, rim, tone = part[0], part[1], part[2]
        is_back = len(part) > 3 and part[3] == "back"
        if back is None or back == is_back:
            F.fill(place(path, hx, hy, hh, rot), rim=rim, tone=tone)


def add_head(F, hx, hy, hh, kind="m", rot=0.0, beard=None, hat=None, nose=1.0, chin=0.0, hair=None, neck_to=None, neck_w=(0.52, 0.72), bald=False, hat_rot=None, brow=1.0):
    """Boyun + baş (+sakal, saç, şapka). neck_to=(bx,by): boyun tabanı. rot: baş eğimi (derece, + = öne eğik)."""
    if neck_to is not None:
        bx, by = neck_to
        F.fill(limb([(hx - 0.08 * hh, hy + 0.30 * hh), (bx, by)], [neck_w[0] * hh, neck_w[1] * hh], cap0=0, cap1=0), rim=0.9)
    if hat:
        add_hat(F, hat, hx, hy, hh, rot if hat_rot is None else hat_rot, back=True)
    if hair:
        F.fill(place(hair_path(hair), hx, hy, hh, rot), rim=1.0)
    F.fill(place(K.head_path(kind, nose=nose, chin=chin, brow=brow), hx, hy, hh, rot), rim=1.0)
    if beard:
        F.fill(place(K.beard_path(beard, chin=chin), hx, hy, hh, rot), rim=0.9)
    if hat:
        add_hat(F, hat, hx, hy, hh, rot if hat_rot is None else hat_rot, back=False)


def hair_path(kind):
    if kind == "bob":                         # kulak altı, sayfa kesimi
        return sp([KC(0.10, -0.50), (-0.20, -0.52), (-0.48, -0.30), (-0.58, 0.05), (-0.52, 0.42), KC(-0.30, 0.40), (-0.18, 0.12), (0.05, -0.20), (0.26, -0.36)], True, 0.9)
    if kind == "long":
        return sp([KC(0.10, -0.50), (-0.24, -0.52), (-0.52, -0.28), (-0.64, 0.20), (-0.66, 0.80), KC(-0.40, 0.92), (-0.28, 0.40), (-0.14, 0.10), (0.05, -0.20), (0.26, -0.36)], True, 0.9)
    if kind == "bun":
        return sp([(-0.55, 0.05), (-0.72, 0.10), (-0.76, 0.34), (-0.58, 0.46), (-0.42, 0.32), (-0.42, 0.10)], True, 0.9)
    return sp([KC(0.10, -0.50), (-0.20, -0.52), (-0.46, -0.30), (-0.50, 0.00), KC(-0.30, 0.10), (0.02, -0.26), (0.26, -0.40)], True, 0.9)


# ───────────────────────────── kol & el montajı ─────────────────────────────

def add_arm(F, pts, widths, hand=None, hand_len=0.1, hand_rot=None, flip=False, rim=0.9, cuff=None, tone=0.0):
    """Kol (omurga noktaları pts, genişlikler) + el. hand: None | 'open' | 'fist'. Elin yönü son segmentin yönü (hand_rot ile değişir)."""
    F.fill(limb(pts, widths, cap0=0.5, cap1=0.2 if hand else 0.45), rim=rim, tone=tone)
    if hand:
        x0, y0 = pts[-2]
        x1, y1 = pts[-1]
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0)) if hand_rot is None else hand_rot
        F.fill(K.hand_pt(hand, x1 - math.cos(math.radians(ang)) * hand_len * 0.12, y1 - math.sin(math.radians(ang)) * hand_len * 0.12, hand_len, ang, flip), rim=1.0)
        if hand == "open":
            F.fill(K.hand_pt("thumb", x1, y1, hand_len, ang, flip), rim=1.0)


def fur_band(P, w, tuft, side=1, n=None, jag=1.0, phase=0.0):
    """Kürk şeridi: omurga P boyunca genişlik w; dış kenar (side=±1) yuvarlak 'bulut' kabarcıklı, çukurlar köşe."""
    pts = list(P)
    seglen = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    total = sum(seglen) or 1.0
    n = n or max(3, int(total / (tuft * 1.5)))

    def at(u):
        d = u * total
        for i, L in enumerate(seglen):
            if d <= L or i == len(seglen) - 1:
                t = min(1.0, d / L) if L else 0
                return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t,
                        (pts[i + 1][0] - pts[i][0]) / (L or 1), (pts[i + 1][1] - pts[i][1]) / (L or 1))
            d -= L
    out, inner = [], []
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n
        x0, y0, tx, ty = at(u0)
        xm, ym, tmx, tmy = at((u0 + u1) / 2)
        nx, ny = -ty * side, tx * side
        nmx, nmy = -tmy * side, tmx * side
        out.append(KC(x0 + nx * w / 2, y0 + ny * w / 2))
        out.append((xm + nmx * (w / 2 + tuft * jag), ym + nmy * (w / 2 + tuft * jag)))
    xe, ye, tx, ty = at(1.0)
    nx, ny = -ty * side, tx * side
    out.append(KC(xe + nx * w / 2, ye + ny * w / 2))
    for i in range(n, -1, -1):
        x, y, tx, ty = at(i / n)
        nx, ny = -ty * side, tx * side
        out.append((x - nx * w / 2, y - ny * w / 2))
    return sp(out, True, 1.0)


# ───────────────────────────── cüppe taslağı ─────────────────────────────

def robe_path(h, sh_y=-0.755, nb=(-0.04, 0.05), back_sh=-0.105, front_sh=0.095, chest=(-0.115, 0.10, -0.66), waist=(-0.095, 0.092, -0.50),
              hip=(-0.14, 0.14, -0.30), hem=(-0.20, 0.19, -0.012), nfold=4, amp=0.008, ph=0.0, lift=0.0, swing=0.0, nb_y=-0.775, belly=0.0, k=0.95):
    """Uzun cüppe/elbise gövdesi (omuz→etek). Tüm değerler h oranı. lift: ön (sağ) etek ucunu kaldırır (ayak görünür), swing: adım kayması."""
    pts = [(nb[0] * h, nb_y * h), (back_sh * h, sh_y * h), (chest[0] * h, chest[2] * h), (waist[0] * h, waist[2] * h), (hip[0] * h, hip[2] * h)]
    pts.append(KC((hem[0] + swing * 0.5) * h, (hem[2] - 0.004) * h))
    for i, (x, y) in enumerate(K.hem_wave(hem[0] * 0.78 + swing * 0.3, hem[1] * 0.80 + swing * 0.3, hem[2], nfold, amp, ph)):
        u = i / max(1, nfold * 2)
        pts.append((x * h, (y - lift * (u ** 2.2)) * h))
    pts.append(KC((hem[1] + swing * 0.5) * h, (hem[2] - 0.004 - lift) * h))
    pts += [((hip[1] + belly * 0.5) * h, hip[2] * h), ((waist[1] + belly) * h, waist[2] * h), ((chest[1] + belly * 0.4) * h, chest[2] * h), (front_sh * h, sh_y * h), (nb[1] * h, nb_y * h)]
    return sp(pts, True, k)


def robe_folds(F, h, x0, x1, y0, y1, n, w, bend=0.008, seed=0, spread=1.0, hi=True, alpha=0.62):
    """Kıvrım fanı: üstte (x0..x1 @ y0) toplanır, altta (daha geniş) açılır; n çizgi."""
    import random
    r = random.Random(seed)
    for i in range(n):
        u = (i + 0.5) / n
        xt = x0 + (x1 - x0) * u
        xb = (x0 + (x1 - x0) * 0.5) + (xt - (x0 + (x1 - x0) * 0.5)) * 2.3 * spread
        yb = y1 - r.random() * 0.05
        yt = y0 + r.random() * 0.03
        F.crease((xt * h, yt * h), (xb * h, yb * h), w * h * (0.7 + 0.6 * r.random()), bend * h * (1 if i % 2 else -1) * (0.5 + r.random()), hi=hi, alpha=alpha)


def hem_slits(F, h, xs, y, depth=0.06, w=0.006, ph=0.0):
    """Etekte ince negatif-alan çentikler (kâğıt oyuğu)."""
    for i, x in enumerate(xs):
        top = (x * h, (y - depth * (0.7 + 0.3 * ((i * 37) % 5) / 5)) * h)
        F.cut(poly([(x * h - w * h, (y + 0.02) * h), (x * h + w * h * 0.15, (y + 0.02) * h), (top[0], top[1])]))
