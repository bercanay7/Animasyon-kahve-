"""cilt_medal — Medici cildi: bronz Rönesans portre madalyası (Pisanello / Niccolò Fiorentino tarzı: profil + kenar yazısı).

medal.py'nin parametrik profil başı (yükseklik haritası) korunur; yüzey: dökme bronz (koyu umber → altın-bronz tepeler), çukurlarda yeşil patina,
döküm gözenekleri, kenar halkası. Gerçek kişi benzerliği iddiası yok: stilize "madalya portresi".
Önbellekli yerel biçimli görüntü + bulanık gölge. draw_medal_b(): tilt (dikey eksen dönüşü), bant sınırlı parlama.
"""
import functools
import math

import cv2
import numpy as np
import skia

import cilt_medici as CM
import cilt_wall as CW
import donem as DN
import medal
import sk
from sk import C, clamp

# Gösterim amaçlı stilize kişiler ("m_" önekli; madalya-lab'ın gerçek anahtarlarıyla çakışmaz)
medal.PEOPLE.setdefault("m_cosimo", dict(nose=26, hook=12, brow=3, lip=0, lip2=2, chin=-2, jaw=0.9, fore=3, age=0.75, jowl=0.12, neck=0.95,
                                          hair="thin", hat="cap_black", beard=None, garment="robe", mouth_open=0.0))
medal.PEOPLE.setdefault("m_lorenzo", dict(nose=4, hook=0, brow=4, lip=3, lip2=12, chin=26, jaw=1.35, fore=1, age=0.3, jowl=0.05, neck=1.2,
                                           hair="long", hat="none", beard=None, garment="fur_doublet", mouth_open=0.0))
medal.PEOPLE.setdefault("m_giovanni", dict(nose=14, hook=2, brow=3, lip=1, lip2=3, chin=0, jaw=1.1, fore=2, age=0.8, jowl=0.4, neck=1.1,
                                            hair="none", hat="flatcap", beard=None, garment="robe", mouth_open=0.0))
medal.PEOPLE.setdefault("m_lucrezia", dict(nose=10, hook=0, brow=1, lip=2, lip2=5, chin=8, jaw=0.85, fore=3, age=0.5, jowl=0.0, neck=0.9,
                                            hair="veil", hat="widow_hood", beard=None, garment="mourning_f", mouth_open=0.0))
medal.INSCR.setdefault("m_cosimo", "COSMVS · MEDICES · PATER · PATRIAE ·")
medal.INSCR.setdefault("m_lorenzo", "LAVRENTIVS · MEDICES · FLORENTINVS ·")
medal.INSCR.setdefault("m_giovanni", "IOHANNES · DE · MEDICIS ·")
medal.INSCR.setdefault("m_lucrezia", "LVCRETIA · TORNABONA ·")
V2 = True                       # erkek profilleri v2 üreteçle (False → eski medal.py profili)
V2_FRAME = "v1"                 # "v1": yüz v1 ile aynı yerde/ölçekte (sahnelerdeki kalibre işaretler korunur) | "bust": omuzlu büst çerçevesi


# ═════════════════════════════ PORTRE ÜRETECİ v2 (ENG-A; SA1-Ö6) ═════════════════════════════
# Erkek profil madalyası: kafatası (yuvarlak artkafa → ense), alın-kaş-burun-dudak-çene hattı (medal.face_points), belirgin çene
# açısı + çene altı, C biçimli kulak (helix + lob), boyun (gırtlak), omuz/büst + madalya kesimi (alt yay), yaka/giysi.
# Yükseklik: her parça maskeden mesafe dönüşümü → kubbe (yumuşak kabartma); saç bukle demetleri (S eğrili oluklar), şapka kıvrımları,
# göz çukuru/kaş/burun sırtı/dudak oluğu yerel modülasyonları. Kadın/örtülü profiller (veil/hood) v1 üreteçte kalır.
V2_SKIP_HATS = {"widow_hood", "gable_hood"}
V2_SKIP_HAIR = {"veil"}


def _mask(paths, blur=0.0):
    cv = medal._Canvas()
    for p_ in paths:
        cv.fill(p_, 255, blur=blur)
    return cv.arr()


def _dome(m, r=None, power=0.5):
    """Maskeden yumuşak kubbe (0..1): iç mesafe / r → sqrt profili."""
    b = (m > 0.5).astype(np.uint8)
    if b.sum() == 0:
        return np.zeros_like(m)
    d = cv2.distanceTransform(b, cv2.DIST_L2, 5).astype(np.float32)
    r = r or max(1.0, float(d.max()))
    return np.clip(d / r, 0, 1) ** power


def _sp(pts, close=True, t=0.5):
    return sk.smooth_path(pts, close=close, tension=t)


def _line_mask(paths_w, blur=1.2):
    cv = medal._Canvas()
    for (p_, w_) in paths_w:
        cv.stroke(p_, 255, w_, blur=blur)
    return cv.arr()


def portrait_height_v2(d, flip=False):
    """Sağa bakan erkek madalya profili → yükseklik haritası (S×S, 0..~1.2)."""
    S_ = medal.S
    fp = medal.face_points(d)
    jw, jowl, nk = d.get("jaw", 1.0), d.get("jowl", 0.0), d.get("neck", 1.0)
    age = d.get("age", 0.3)
    hair, hat, beard = d.get("hair"), d.get("hat"), d.get("beard")
    fo = d.get("fore", 0)
    # ── baş dış hattı: yüz profili (alın→çene altı) + çene altı → gırtlak + ense + artkafa + tepe
    chin_under = fp[-1]
    gon_x, gon_y = 452 - 10 * (jw - 1), 584 + 16 * jowl
    head = list(fp) + [(chin_under[0] - 26, chin_under[1] + 16 + 10 * jowl), (gon_x + 40, 652 + 10 * jowl), (gon_x - 8, gon_y + 34),
                       (392, 600), (346, 520), (336, 440), (352, 340), (402, 262), (470, 214), (540, 212), (568 + fo * 0.5, 238)]
    m_head = _mask([_sp(head, True, 0.42)])
    # ── boyun (gırtlak hafif çıkıntı) + büst/omuz + madalya kesimi
    nx = (nk - 1.0) * 28
    neck = [(548, 636), (562 + nx * 0.4, 672), (574 + nx * 0.5, 696), (572 + nx, 720), (584 + nx, 748), (370 - nx, 756), (378 - nx, 690), (396, 612)]
    m_neck = _mask([_sp(neck, True, 0.45)])
    bust = [(584 + nx, 728), (664 + nx, 752), (734, 800), (772, 872), (560, 918), (300, 908), (212, 862), (246, 790), (330, 752), (376 - nx, 734)]
    m_bust = _mask([_sp(bust, True, 0.40)])
    # ── kulak (C: sarmal kenar + lob), saç altında kalsa da kabartma verir
    ex, ey = 456, 436
    ear_out = [(ex + 4, ey - 44), (ex + 24, ey - 30), (ex + 26, ey - 2), (ex + 18, ey + 28), (ex + 6, ey + 46), (ex - 10, ey + 44), (ex - 18, ey + 24),
               (ex - 20, ey - 10), (ex - 14, ey - 38)]
    m_ear = _mask([_sp(ear_out, True, 0.5)])
    # ── saç
    m_hair = np.zeros((S_, S_), np.float32)
    strands = []
    if hair in ("long", "long_wave", "bob"):
        hp = [(566 + fo * 0.5, 236), (520, 204), (450, 196), (380, 232), (340, 300), (322, 392), (326, 500), (346, 590), (380, 646), (420, 662), (452, 640),
              (470, 590), (478, 520), (500, 470), (514, 420), (520, 360), (540, 300), (562, 262)]
        m_hair = _mask([_sp(hp, True, 0.45)])
        for i in range(11):                                              # bukle demetleri: S eğrili, uçlarda içe kıvrık
            x0 = 548 - i * 20
            pts = [(x0, 228 + i * 4), (x0 - 40 - i * 3, 300), (x0 - 52 - i * 2, 420), (x0 - 40 - i * 4, 520), (x0 - 60 - i * 3, 600), (x0 - 40 - i * 3, 640)]
            strands.append((_sp(pts, False, 0.5), 5.0))
        for j in range(6):                                               # uçlarda bukle halkaları
            cx_, cy_ = 352 + j * 20, 628 + (j % 2) * 10
            strands.append((_sp([(cx_ - 12, cy_ - 8), (cx_, cy_ + 10), (cx_ + 12, cy_ - 4)], False, 0.6), 4.0))
    elif hair in ("short", "monk", "thin"):
        thin = hair == "thin"
        hp = [(560 + fo * 0.5, 240), (500, 206), (420, 212), (366, 262), (342, 340), (340, 430), (360, 520), (392, 580), (424, 560), (430, 470), (450, 400),
              (470, 330), (512, 268)] if not thin else [(470, 222), (400, 240), (354, 300), (344, 400), (362, 500), (396, 560), (418, 520), (420, 440), (436, 360), (456, 290)]
        m_hair = _mask([_sp(hp, True, 0.45)])
        for i in range(14 if not thin else 7):
            x0 = 520 - i * 14
            strands.append((_sp([(x0, 232 + i * 3), (x0 - 30, 300 + i * 6), (x0 - 34 - i, 380 + i * 8)], False, 0.5), 3.4))
    # ── şapka
    m_hat = np.zeros((S_, S_), np.float32)
    folds = []
    if hat in ("cap_black", "cap", "cap_gold", "skull"):
        cap = [(338, 300), (350, 228), (404, 176), (480, 156), (556, 168), (606, 206), (612, 246), (590, 262), (520, 248), (450, 252), (392, 270), (356, 300)]
        m_hat = _mask([_sp(cap, True, 0.42)])
        folds = [(_sp([(370, 268), (450, 236), (530, 232), (600, 250)], False, 0.5), 7.0), (_sp([(430, 180), (470, 230)], False, 0.5), 4.0),
                 (_sp([(520, 176), (540, 226)], False, 0.5), 4.0)]
    elif hat in ("flatcap", "beret_f"):
        cap = [(316, 262), (330, 214), (400, 184), (500, 180), (590, 198), (636, 226), (630, 252), (586, 262), (500, 248), (420, 256), (360, 280)]
        m_hat = _mask([_sp(cap, True, 0.42)])
        folds = [(_sp([(340, 248), (420, 226), (520, 226), (612, 240)], False, 0.5), 6.0)]
    elif hat not in (None, "none"):
        cv = medal._Canvas()
        medal._hat(cv, d)
        m_hat = (cv.arr() > 0.05).astype(np.float32)
    # ── sakal (v1 biçimi maske olarak)
    m_beard = np.zeros((S_, S_), np.float32)
    if beard:
        cv = medal._Canvas()
        medal._beard(cv, d)
        m_beard = (cv.arr() > 0.05).astype(np.float32)
    # ── yükseklik bileşimi
    H = np.zeros((S_, S_), np.float32)
    H = np.maximum(H, m_bust * (0.16 + 0.22 * _dome(m_bust, 90)))
    H = np.maximum(H, m_neck * (0.30 + 0.24 * _dome(m_neck, 60)))
    hd = _dome(m_head, 120, 0.55)
    H = np.maximum(H, m_head * (0.40 + 0.46 * hd))
    # yüz modülasyonları (Gauss tümsek/çukur)
    yy, xx = np.mgrid[0:S_, 0:S_].astype(np.float32)

    def g(cx_, cy_, rx, ry, a):
        return a * np.exp(-(((xx - cx_) / rx) ** 2 + ((yy - cy_) / ry) ** 2))
    br = d.get("brow", 3)
    mod = (g(566, 348, 34, 14, 0.06 + 0.005 * br) - g(560, 380, 26, 16, 0.07) + g(520, 470, 60, 50, 0.07) + g(594 + d.get("nose", 12) * 0.5, 440, 12, 34, 0.05)
           - g(600, 527, 18, 5, 0.05) + g(596, 594, 24, 18, 0.04) + g(470, 300, 70, 60, 0.04))
    if age > 0.3:
        mod -= g(574, 520, 8, 24, 0.03 * age)
    H += mod * m_head
    # kulak: sarmal kenar yüksek, iç oyuk
    ed = _dome(m_ear, 18, 0.7)
    ear_h = m_ear * (0.86 + 0.10 * ed - 0.16 * np.exp(-(((xx - ex - 4) / 12) ** 2 + ((yy - ey) / 22) ** 2)))
    H = np.where(m_ear > 0.5, np.maximum(H, ear_h), H)
    # saç (kubbe + demet olukları)
    if m_hair.max() > 0:
        hh = m_hair * (0.62 + 0.30 * _dome(m_hair, 70, 0.6))
        if strands:
            sm = _line_mask(strands, 1.4)
            hh -= 0.07 * sm * m_hair
        H = np.where(m_hair > 0.5, np.maximum(H * 0.3 + hh * 0.9, hh), H)
    if m_beard.max() > 0:
        bh = m_beard * (0.80 + 0.18 * _dome(m_beard, 40, 0.6))
        H = np.where(m_beard > 0.5, np.maximum(H, bh), H)
    if m_hat.max() > 0:
        th = m_hat * (0.84 + 0.28 * _dome(m_hat, 60, 0.6))
        if folds:
            th -= 0.06 * _line_mask(folds, 2.0) * m_hat
        H = np.where(m_hat > 0.5, np.maximum(H, th), H)
    # giysi: yaka bandı + kıvrımlar
    col_band = _line_mask([(_sp([(368, 740), (470, 764), (588, 744)], False, 0.5), 22.0)], 2.0)
    H += 0.08 * col_band * m_bust
    H -= 0.05 * _line_mask([(_sp([(280, 826), (420, 858), (600, 862)], False, 0.5), 4.0), (_sp([(470, 770), (482, 912)], False, 0.5), 4.0),
                            (_sp([(330, 760), (300, 820), (290, 900)], False, 0.5), 3.0), (_sp([(640, 770), (690, 830), (700, 890)], False, 0.5), 3.0)], 1.5) * m_bust
    # kazınmış çizgiler (göz, kaş, burun kanadı, dudak) — v1 ile aynı yerler, daha ince
    cvf = medal._Canvas()
    medal._features(cvf, d)
    feat = cvf.arr()
    fmask = (feat > 0.02).astype(np.float32) * m_head * (1 - m_hair) * (1 - m_hat)
    H = H - fmask * np.clip(0.50 - feat, 0, 0.5) * 0.30
    H = cv2.GaussianBlur(H, (0, 0), 1.2)
    if flip:
        H = H[:, ::-1]
    return H


def _uses_v2(d):
    return d is not None and d.get("hat") not in V2_SKIP_HATS and d.get("hair") not in V2_SKIP_HAIR and d.get("garment") not in ("mourning_f", "gown_f")


@functools.lru_cache(maxsize=48)
def medal_array_v2(key, metal="gold", inscription=None, flip=False):
    """medal.medal_array ile aynı madalya düzeni (alan, kenar halkası, boncuk, yazı) + v2 profil yüksekliği. RGBA uint8 (S×S)."""
    d = medal.PEOPLE.get(key) or medal.PEOPLE["_anon"]
    S_ = medal.S
    por = portrait_height_v2(d, flip)
    # ÇERÇEVE: v1 ile AYNI (ölçek 1,22, aynı öteleme) → yüz öğeleri (burun, çene, göz) madalyada v1'deki yerinde kalır: sahne dosyalarındaki
    # kalibre işaretler (ör. c6_tarif BASIK BURUN / ÖNE ÇIKIK ALT ÇENE) bozulmaz. Büst bu ölçekte iç halkayla kesilir (madalya kesimi).
    dy = d.get("dy", 0)
    if V2_FRAME == "bust":                      # büst çerçevesi (omuz + madalya kesimi görünür; yüz öğeleri v1'den farklı yerde)
        sc = 1.08 * (d.get("scale", 1.22) / 1.22)
        tx = (S_ / 2 - (S_ - 500) * sc + 10) if flip else (S_ / 2 - 500 * sc - 10)
        Mtx = np.float32([[sc, 0, tx], [0, sc, S_ / 2 - 520 * sc + dy * 0.5]])
    else:
        sc = d.get("scale", 1.22)
        tx = (S_ / 2 - 480 * sc - 85) if flip else (S_ / 2 - 520 * sc + 85)
        Mtx = np.float32([[sc, 0, tx], [0, sc, S_ / 2 - 470 * sc + 20 + dy]])
    por = cv2.warpAffine(por, Mtx, (S_, S_), flags=cv2.INTER_LINEAR, borderValue=0)
    yy, xx = np.mgrid[0:S_, 0:S_].astype(np.float32)
    rr = np.hypot(xx - S_ / 2, yy - S_ / 2)
    disc = (rr <= 484).astype(np.float32)
    pmask = cv2.GaussianBlur((por > 0.02).astype(np.float32), (0, 0), 5)
    pat = 0.006 * np.cos(rr * 0.40) + 0.004 * np.cos(np.arctan2(yy - S_ / 2, xx - S_ / 2) * 60) * np.clip(rr / 484, 0, 1)
    field = 0.10 + 0.04 * np.clip(1 - rr / 484, 0, 1) + pat * (1 - pmask)
    ring = np.exp(-((rr - 466) / 12.0) ** 2) * 0.5 + np.exp(-((rr - 408) / 5.0) ** 2) * 0.28
    ang = np.arctan2(yy - S_ / 2, xx - S_ / 2)
    beads = np.exp(-((rr - 437) / 8.0) ** 2) * (0.5 + 0.5 * np.cos(ang * 72)) * 0.22
    ins = np.zeros_like(rr)
    if inscription:
        m = medal.ring_text_mask(inscription, 440, 54, track=5.0)
        ins = cv2.GaussianBlur(m, (0, 0), 1.0) * 0.55
    inner = cv2.GaussianBlur((rr <= 400).astype(np.float32), (0, 0), 6)
    Hh = field + ring + beads + ins + por * 0.82 * inner
    Hh = np.where(disc > 0, Hh, 0)
    return medal._relief_from_height(Hh, disc, metal, strength=2.2)


@functools.lru_cache(maxsize=32)
def medal_array_b(key, metal="bronze", inscription=None, flip=False, size=720):
    """RGBA uint8 (size²): dökme bronz + patina."""
    d_ = medal.PEOPLE.get(key)
    arr = medal_array_v2(key, metal, inscription, flip) if (V2 and _uses_v2(d_)) else medal.medal_array(key, metal, inscription, flip)
    a = arr[..., 3]
    rgb = arr[..., :3].astype(np.float32)
    lum = rgb.mean(-1) / 255.0
    rs = np.random.RandomState(7)
    if metal == "bronze":
        pat = np.clip((0.40 - lum) / 0.26, 0, 1)
        pc = np.array([62, 96, 82], np.float32)
        rgb = rgb * (1 - 0.34 * pat[..., None]) + pc * 0.34 * pat[..., None]
        cast = CW.gn(rs, arr.shape[0], arr.shape[1], 1.1) * 0.05 + CW.lf(rs, arr.shape[0], arr.shape[1], 30) * 0.03
        rgb *= (1 + cast)[..., None]
    out = np.dstack([np.clip(rgb, 0, 255), a]).astype(np.uint8)
    if size != out.shape[0]:
        out = cv2.resize(out, (size, size), interpolation=cv2.INTER_AREA)
    return out


@functools.lru_cache(maxsize=32)
def medal_img(key, metal="bronze", inscription=None, flip=False, size=720):
    return sk.np_to_image(medal_array_b(key, metal, inscription, flip, size))


@functools.lru_cache(maxsize=32)
def medal_shadow(key, metal="bronze", inscription=None, flip=False, size=720):
    return CM.blur_sil(medal_array_b(key, metal, inscription, flip, size)[..., 3], 16.0, (14, 8, 2))


def draw_medal_b(f, key, x, y, size, metal="bronze", flip=False, alpha=1.0, tilt=0.0, glint=None, inscription=True, shadow=0.6):
    """Madalya merkezi (x,y); tilt: -1..1 (dikey eksen); glint: 0..1 yatay parlama bandı.
    Kenar yazısı dönem kuralından geçer (donem.medal_inscription: 'PATER PATRIAE' yalnız ≥1464)."""
    ins = medal.INSCR.get(key) if inscription else None
    if ins:
        ins0 = ins
        ins = DN.medal_inscription(ins)
        DN.note_once_per_frame("medal", key=key, text=ins, req=ins0)
    img = medal_img(key, metal, ins, flip, 720)
    s = size / 720.0
    cs = max(0.05, math.cos(tilt * 0.55))
    c = f.c
    if shadow > 0:
        c.save(); c.translate(x + size * 0.035, y + size * 0.055); c.scale(s * cs, s)
        p = skia.Paint(AntiAlias=True); p.setAlphaf(clamp(shadow * alpha))
        c.drawImage(medal_shadow(key, metal, ins, flip, 720), -360, -360, CM._LIN, p)
        c.restore()
    c.save(); c.translate(x, y); c.scale(s * cs, s)
    p = skia.Paint(AntiAlias=True); p.setAlphaf(clamp(alpha))
    c.drawImage(img, -360, -360, CM._LIN, p)
    if glint is not None:
        # yumuşak kenarlı eğik parlama, madalya alfasıyla maskeli (eski sürüm sert kenarlı şerit + çift çizim → dikdörtgen artefakt; SA1-E4)
        gx = -520 + 1040 * glint
        CM.soft_glint(c, img, -360, -360, (max(-380.0, gx - 200), -380, min(380.0, gx + 200), 380), gx, 150, alpha, "#FFE6B0", 110)
    c.restore()
