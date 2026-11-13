"""figs_parts — şapka/başlık, baş montajı, kürk, kol-el montajı, cüppe taslağı (figür-lab ortak parçaları).

Şapkalar baş-biriminde (baş yüksekliği 1; merkez 0; yüz +x; kafatası tepesi y=-0.5) yol listesi döndürür: [(yol, rim_gücü, ton)].
"""
import math

import skia

import figs_kit as K
from figs_kit import K as KC, Fig, bar, ell, feather_path, lens, limb, place, poly, shoe, sp

# ───────────────────────────── şapkalar ─────────────────────────────


def hat_parts(kind):
    """Baş-birimli şapka parçaları [(path, rim, tone)] (arkadan öne)."""
    P = []
    if kind == "beret":                       # Rönesans bareti: yassı, yana yatık, sol arkaya tüy
        P.append((feather_path(0.02, -0.70, -0.78, -0.98, 0.15, bend=-0.16), 1.0, 0.0))
        P.append((feather_path(0.10, -0.70, -0.55, -1.12, 0.12, bend=-0.20), 0.8, 0.0))
        P.append((sp([KC(0.37, -0.22), (0.47, -0.37), (0.38, -0.58), (0.12, -0.74), (-0.22, -0.72), (-0.50, -0.55), (-0.58, -0.30), KC(-0.50, -0.10), (-0.32, -0.22),
                      (-0.05, -0.28), (0.20, -0.25)], True, 0.9), 1.0, 0.0))
    elif kind == "flatcap":                   # tüccar/katip: yumuşak yuvarlak şapka; kafatasından belirgin taşan taç + kıvrık kenar bandı
        P.append((sp([KC(0.44, -0.30), (0.46, -0.50), (0.30, -0.68), (-0.04, -0.76), (-0.38, -0.68), (-0.54, -0.48), KC(-0.52, -0.30), (-0.2, -0.36), (0.1, -0.38)], True, 0.9), 1.0, 0.0))
        P.append((sp([KC(0.50, -0.14), (0.54, -0.24), (0.44, -0.33), (0.0, -0.36), (-0.42, -0.33), (-0.60, -0.22), KC(-0.56, -0.08), (-0.32, -0.14), (0.0, -0.17), (0.32, -0.14)], True, 0.9), 1.0, 0.06))
        P.append((sp([KC(-0.52, -0.31), (0.0, -0.37), KC(0.44, -0.31), (0.44, -0.34), (0.0, -0.40), (-0.52, -0.34)], True, 0.6), 0.0, 0.16))
    elif kind == "plume":                     # Landsknecht: geniş tabak şapka + tüyler
        for i, (dx, dy, wd, bd) in enumerate([(-0.95, -1.05, 0.26, -0.28), (-1.12, -0.80, 0.24, -0.30), (-0.78, -1.22, 0.22, -0.22), (-1.20, -0.55, 0.20, -0.26)]):
            P.append((feather_path(-0.02 - i * 0.04, -0.66, dx, dy, wd, bend=bd), 0.9, 0.0))
        P.append((sp([KC(0.46, -0.28), (0.82, -0.40), (0.78, -0.52), (0.30, -0.60), (-0.30, -0.66), (-0.84, -0.50), (-0.92, -0.36), KC(-0.60, -0.22), (-0.10, -0.30)], True, 0.9), 1.0, 0.0))
        P.append((sp([KC(0.30, -0.40), (0.26, -0.78), (-0.10, -0.90), (-0.46, -0.76), (-0.50, -0.50), KC(-0.20, -0.46)], True, 0.8), 1.0, 0.0))
    elif kind == "galero":                    # kardinal şapkası: çok geniş yassı kenar, alçak yuvarlak tepe, püsküllü kordonlar
        P.append((sp([KC(-1.25, -0.38), (-0.80, -0.47), (-0.2, -0.50), (0.5, -0.49), (1.0, -0.45), KC(1.30, -0.36), (1.0, -0.30), (0.5, -0.31), (-0.2, -0.31), (-0.8, -0.32)], True, 0.85), 1.0, 0.0))
        P.append((sp([KC(-0.46, -0.44), (-0.46, -0.62), (-0.22, -0.74), (0.12, -0.74), (0.40, -0.62), KC(0.48, -0.44)], True, 0.85), 1.0, 0.0))
        P.append((sp([KC(-0.46, -0.40), (0.0, -0.36), KC(0.48, -0.40), (0.48, -0.44), (0.0, -0.45), (-0.46, -0.44)], True, 0.6), 0.0, 0.14))
    elif kind == "cowl":                      # keşiş kukuletası: kafayı saran kütle + omuzlara düşen kıvrım + alın kenarı bandı (tek parça gibi)
        P.append((sp([KC(0.22, -0.38), (0.04, -0.70), (-0.34, -0.80), (-0.64, -0.58), (-0.78, -0.14), (-0.92, 0.44), (-0.92, 1.00), (-0.66, 1.22), (-0.34, 1.12), KC(-0.14, 0.78),
                      (-0.30, 0.46), (-0.34, 0.20), (-0.20, -0.10)], True, 0.9), 1.0, 0.0, "back"))
        P.append((sp([KC(0.37, -0.26), (0.30, -0.46), (0.14, -0.64), (-0.12, -0.70), (-0.40, -0.60), (-0.50, -0.40), (-0.30, -0.44), (-0.08, -0.50), (0.12, -0.42), KC(0.26, -0.24)], True, 0.8), 0.45, 0.04))
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
    elif kind == "turban":                    # Osmanlı sarığı: şişkin yuvarlak kütle, sarım şeritleri, geride sarkan uç, önde sorguç (tüy + taş)
        P.append((sp([KC(-0.30, -0.28), (-0.52, -0.10), (-0.62, 0.20), (-0.60, 0.46), (-0.50, 0.44), KC(-0.40, 0.14), (-0.34, -0.06)], True, 0.8), 0.85, 0.0, "back"))
        P.append((sp([KC(0.46, -0.20), (0.62, -0.38), (0.66, -0.66), (0.50, -0.92), (0.16, -1.04), (-0.22, -1.00), (-0.54, -0.82), (-0.68, -0.52), (-0.62, -0.28), KC(-0.46, -0.16),
                      (-0.10, -0.30), (0.22, -0.28)], True, 0.9), 1.0, 0.0))
        P.append((lens((-0.58, -0.40), (0.60, -0.50), 0.045, -0.10), 0.0, 0.20))
        P.append((lens((-0.50, -0.58), (0.56, -0.70), 0.04, -0.12), 0.0, 0.20))
        P.append((lens((-0.38, -0.78), (0.42, -0.86), 0.035, -0.10), 0.0, 0.20))
        P.append((feather_path(0.12, -0.92, 0.30, -1.62, 0.30, bend=-0.14), 1.0, 0.0))
        P.append((ell(0.12, -0.90, 0.075, 0.075), 1.0, 0.45))
    elif kind == "kavuk":                     # Osmanlı yüksek kavuk: üstü hafif genişleyen keçe silindir + tabanda kalın sarık sargısı
        P.append((sp([KC(0.40, -0.52), (0.46, -0.80), (0.54, -1.10), (0.50, -1.28), (0.26, -1.36), (-0.06, -1.38), (-0.36, -1.34), (-0.52, -1.20), (-0.50, -0.92), (-0.42, -0.60), KC(-0.34, -0.50)], True, 0.8), 1.0, 0.0))
        P.append((sp([KC(0.50, -0.22), (0.62, -0.34), (0.62, -0.56), (0.46, -0.70), (0.0, -0.74), (-0.46, -0.70), (-0.64, -0.54), (-0.66, -0.32), KC(-0.52, -0.16), (-0.1, -0.30), (0.26, -0.28)], True, 0.85), 1.0, 0.02))
        P.append((lens((-0.60, -0.40), (0.58, -0.46), 0.04, -0.07), 0.0, 0.20))
        P.append((lens((-0.54, -0.56), (0.52, -0.62), 0.04, -0.07), 0.0, 0.20))
    elif kind == "bork":                      # yeniçeri börkü: alın üstünde oturan kısa koni gövde, sırtta sarkan geniş kollu uç, önde (yukarıda) kaşıklık
        P.append((sp([KC(-0.30, -0.62), (-0.50, -0.48), (-0.72, -0.14), (-0.88, 0.34), (-0.92, 0.74), KC(-0.66, 0.90), (-0.42, 0.78), (-0.32, 0.36), (-0.30, 0.02), KC(-0.28, -0.14)], True, 0.9), 0.85, 0.0, "back"))
        P.append((sp([KC(0.33, -0.30), (0.40, -0.50), (0.38, -0.78), (0.24, -0.98), (-0.06, -1.06), (-0.32, -0.96), (-0.46, -0.72), (-0.50, -0.42), KC(-0.46, -0.20)], True, 0.9), 1.0, 0.0))
        P.append((sp([KC(0.30, -0.36), (0.44, -0.44), (0.50, -0.58), (0.40, -0.68), KC(0.30, -0.56)], True, 0.6), 1.0, 0.0))
        P.append((sp([KC(-0.46, -0.27), (0.0, -0.24), KC(0.33, -0.28), (0.33, -0.37), (0.0, -0.33), (-0.46, -0.36)], True, 0.6), 0.0, 0.14))
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
    elif kind == "woolcap":                   # Frig tipi yün bere (denizci/balıkçı): gövde alına oturur, ucu öne düşer
        P.append((sp([KC(0.40, -0.20), (0.44, -0.40), (0.30, -0.62), (0.02, -0.74), (-0.30, -0.66), (-0.48, -0.40), (-0.47, -0.12), KC(-0.30, -0.15), (0.0, -0.26)], True, 0.9), 1.0, 0.0))
        P.append((sp([KC(0.04, -0.74), (0.32, -0.98), (0.66, -0.96), (0.88, -0.76), (0.90, -0.50), (0.78, -0.40), (0.68, -0.52), (0.64, -0.66), (0.46, -0.70), (0.22, -0.64)], True, 0.85), 1.0, 0.0))
        P.append((sp([KC(-0.46, -0.22), (0.0, -0.18), KC(0.40, -0.24), (0.40, -0.31), (0.0, -0.26), (-0.46, -0.30)], True, 0.6), 0.0, 0.16))
    elif kind == "biretta":                   # alim/öğrenci dört köşeli bareti
        P.append((poly([(-0.40, -0.28), (-0.38, -0.60), (0.40, -0.62), (0.42, -0.30)]), 1.0, 0.0))
        P.append((poly([(-0.34, -0.60), (-0.30, -0.70), (0.36, -0.70), (0.40, -0.62)]), 1.0, 0.0))
    elif kind == "scholar":                   # bilgin/katip kepi: köşeli taç + kıvrık kenar + yan kulaklık
        P.append((sp([KC(0.40, -0.22), (0.44, -0.46), (0.34, -0.66), (0.0, -0.72), (-0.34, -0.66), (-0.50, -0.44), KC(-0.48, -0.22), (-0.2, -0.30), (0.1, -0.32)], True, 0.7), 1.0, 0.0))
        P.append((sp([KC(0.46, -0.12), (0.50, -0.22), (0.40, -0.30), (0.0, -0.33), (-0.46, -0.30), (-0.58, -0.18), KC(-0.54, 0.0), (-0.50, 0.24), KC(-0.34, 0.26), (-0.34, 0.02), (0.0, -0.14), (0.3, -0.12)], True, 0.8), 1.0, 0.05))
    return [p for p in P if p]


def add_hat(F, kind, hx, hy, hh, rot=0.0, back=None):
    """back=None: hepsi; back=True: yalnız 'back' (kafanın arkasında) parçalar; back=False: ön parçalar."""
    for part in hat_parts(kind):
        path, rim, tone = part[0], part[1], part[2]
        is_back = len(part) > 3 and part[3] == "back"
        if back is None or back == is_back:
            F.fill(place(path, hx, hy, hh, rot), rim=rim, tone=tone)


def add_head(F, hx, hy, hh, kind="m", rot=0.0, beard=None, hat=None, nose=1.0, chin=0.0, hair=None, neck_to=None, neck_w=(0.52, 0.72), bald=False, hat_rot=None, brow=1.0, head_rim=None):
    """Boyun + baş (+sakal, saç, şapka). neck_to=(bx,by): boyun tabanı. rot: baş eğimi (derece, + = öne eğik)."""
    if neck_to is not None:
        bx, by = neck_to
        F.fill(limb([(hx - 0.08 * hh, hy + 0.30 * hh), (bx, by)], [neck_w[0] * hh, neck_w[1] * hh], cap0=0, cap1=0), rim=0.9)
    if hat:
        add_hat(F, hat, hx, hy, hh, rot if hat_rot is None else hat_rot, back=True)
    if hair:
        F.fill(place(hair_path(hair), hx, hy, hh, rot), rim=1.0)
    hr = head_rim if head_rim is not None else (0.35 if hat == "cowl" else 1.0)
    F.fill(place(K.head_path(kind, nose=nose, chin=chin, brow=brow), hx, hy, hh, rot), rim=hr)
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

def add_leg(F, h, hip, knee, ankle, wd=(0.070, 0.050, 0.032), toe=1, shoe_kind="square", shoe_w=0.09, rim=0.8, tone=0.0, calf=0.009):
    """Çorap bacak (uyluk→diz→baldır kabarıklığı→bilek) + ayakkabı. hip/knee/ankle (x,y) h oranı."""
    hx, hy = hip
    kx, ky = knee
    ax, ay = ankle
    mx, my = hx + (kx - hx) * 0.45, hy + (ky - hy) * 0.45
    cx, cy = kx + (ax - kx) * 0.28 - calf * toe, ky + (ay - ky) * 0.28
    qx, qy = kx + (ax - kx) * 0.70, ky + (ay - ky) * 0.70
    P = [(hx * h, hy * h), (mx * h, my * h), (kx * h, ky * h), (cx * h, cy * h), (qx * h, qy * h), (ax * h, ay * h)]
    W = [wd[0] * h * 1.04, wd[0] * h * 0.92, wd[1] * h * 0.92, wd[1] * h * 1.12, wd[2] * h * 1.08, wd[2] * h * 0.9]
    F.fill(limb(P, W, cap0=0.3, cap1=0.25), rim=rim, tone=tone)
    F.fill(shoe((ankle[0] - 0.014) * h, 0, shoe_w * h, 0.036 * h, toe, shoe_kind), rim=rim)


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
        elif hand == "fist":
            F.fill(K.hand_pt("thumb_fist", x1 - math.cos(math.radians(ang)) * hand_len * 0.12, y1 - math.sin(math.radians(ang)) * hand_len * 0.12, hand_len, ang, flip), rim=1.0)


def fur_band(P, w, tuft, side=1, n=None, jag=0.78, phase=0.0, seed=3):
    """Kürk şeridi: omurga P boyunca genişlik w; dış kenar (side=±1) yuvarlak 'bulut' kabarcıklı (yükseklik/konum hafif rastgele), çukurlar köşe."""
    import random
    rs = random.Random(seed)
    pts = list(P)
    seglen = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    total = sum(seglen) or 1.0
    n = n or max(3, int(total / (tuft * 1.25)))

    def at(u):
        d = u * total
        for i, L in enumerate(seglen):
            if d <= L or i == len(seglen) - 1:
                t = min(1.0, d / L) if L else 0
                return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t,
                        (pts[i + 1][0] - pts[i][0]) / (L or 1), (pts[i + 1][1] - pts[i][1]) / (L or 1))
            d -= L
    out = []
    edges = [0.0] + sorted(((i / n) + (rs.random() - 0.5) * 0.45 / n) for i in range(1, n)) + [1.0]
    for i in range(n):
        u0, u1 = edges[i], edges[i + 1]
        x0, y0, tx, ty = at(u0)
        um = (u0 + u1) / 2 + (rs.random() - 0.5) * 0.25 * (u1 - u0)
        xm, ym, tmx, tmy = at(um)
        nx, ny = -ty * side, tx * side
        nmx, nmy = -tmy * side, tmx * side
        hgt = (0.62 + 0.76 * rs.random()) * tuft * jag
        out.append(KC(x0 + nx * (w / 2 - tuft * 0.08), y0 + ny * (w / 2 - tuft * 0.08)))
        out.append((xm + nmx * (w / 2 + hgt), ym + nmy * (w / 2 + hgt)))
    xe, ye, tx, ty = at(1.0)
    nx, ny = -ty * side, tx * side
    out.append(KC(xe + nx * w / 2, ye + ny * w / 2))
    inner = []
    for i in range(n, -1, -1):
        x, y, tx, ty = at(i / n)
        nx, ny = -ty * side, tx * side
        inner.append((x - nx * w / 2, y - ny * w / 2))
    return sp(out + inner, True, 1.0)


# ───────────────────────────── cüppe taslağı ─────────────────────────────

def robe_path(h, sh_y=-0.755, nb=(-0.04, 0.05), back_sh=-0.105, front_sh=0.095, chest=(-0.115, 0.10, -0.66), waist=(-0.095, 0.092, -0.50),
              hip=(-0.14, 0.14, -0.30), hem=(-0.20, 0.19, -0.012), nfold=4, amp=0.008, ph=0.0, lift=0.0, swing=0.0, nb_y=-0.775, belly=0.0, k=0.95,
              wave_b=0.0, wave_f=0.0, dag=0.0):
    """Uzun/orta boy cüppe gövdesi (omuz→etek). Tüm değerler h oranı.
    lift: ön (sağ) etek ucunu kaldırır (ayak görünür), swing: adım kayması, wave_b/wave_f: yan kenarlarda kumaş dalgası (S eğrisi),
    dag: dişli (yaprak biçimli, 'dagging') etek kenarı genliği."""
    pts = [(nb[0] * h, nb_y * h), (back_sh * h, sh_y * h), (chest[0] * h, chest[2] * h), (waist[0] * h, waist[2] * h), (hip[0] * h, hip[2] * h)]
    # kalça→etek arası ara noktalar (arka kenar): S eğrisi
    for u, sg in ((0.38, 1.0), (0.72, -0.6)):
        yy = hip[2] + (hem[2] - hip[2]) * u
        xx = hip[0] + (hem[0] - hip[0]) * (u ** 1.15) - wave_b * sg
        pts.append((xx * h, yy * h))
    pts.append(KC((hem[0] + swing * 0.5) * h, (hem[2] - 0.004) * h))
    x0, x1 = hem[0] * 0.78 + swing * 0.3, hem[1] * 0.80 + swing * 0.3
    if dag > 0:
        n = max(3, nfold * 2)
        for i in range(n + 1):
            u = i / n
            x = x0 + (x1 - x0) * u
            yy = hem[2] - lift * (u ** 2.2)
            pts.append(KC(x * h, (yy - dag * 0.35) * h))
            if i < n:
                pts.append(KC((x + (x1 - x0) / n * 0.5) * h, (yy + dag) * h))
    else:
        for i, (x, y) in enumerate(K.hem_wave(x0, x1, hem[2], nfold, amp, ph)):
            u = i / max(1, nfold * 2)
            pts.append((x * h, (y - lift * (u ** 2.2)) * h))
    pts.append(KC((hem[1] + swing * 0.5) * h, (hem[2] - 0.004 - lift) * h))
    for u, sg in ((0.72, -0.6), (0.38, 1.0)):
        yy = hip[2] + (hem[2] - hip[2]) * u
        xx = hip[1] + (hem[1] - hip[1]) * (u ** 1.15) + wave_f * sg
        pts.append((xx * h, yy * h))
    pts += [((hip[1] + belly * 0.5) * h, hip[2] * h), ((waist[1] + belly) * h, waist[2] * h), ((chest[1] + belly * 0.4) * h, chest[2] * h), (front_sh * h, sh_y * h), (nb[1] * h, nb_y * h)]
    return sp(pts, True, k)


def ruff(F, h, cx, cy, rx=0.075, ry=0.020, n=14, tilt=-8.0, rim=1.0):
    """Katlı yaka (ruff): boyun çevresinde yassı, tırtıklı elips (rim ışıklı); cx,cy px."""
    pts = []
    for i in range(n * 2):
        a = math.pi * 2 * i / (n * 2)
        r = 1.0 if i % 2 == 0 else 0.84
        pts.append((math.cos(a) * rx * h * r, math.sin(a) * ry * h * r))
    path = sp(pts, True, 0.9)
    q = skia.Matrix()
    q.setRotate(tilt)
    q.postTranslate(cx, cy)
    path.transform(q)
    F.fill(path, rim=rim, tone=0.05)
    return path


def hem_band(F, h, x0, x1, y, n=9, size=0.010, alpha=0.45, lift=0.0):
    """Etek şeridi süsü: küçük elmas dizisi (açık ton) + ince çizgi."""
    pts = []
    for i in range(n):
        u = (i + 0.5) / n
        x = x0 + (x1 - x0) * u
        yy = y - lift * (u ** 2.2)
        F.fill(poly([(x * h, (yy - size) * h), ((x + size * 0.8) * h, yy * h), (x * h, (yy + size) * h), ((x - size * 0.8) * h, yy * h)]), rim=0.0, tone=1.0, alpha=alpha, bound=False)
    F.line(poly([(x0 * h, (y - size * 1.6) * h), (x1 * h, (y - size * 1.6 - lift) * h)], False), h * 0.0025, tone=1.0, alpha=alpha * 0.8)


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
