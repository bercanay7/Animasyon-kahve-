"""cilt_medal — Medici cildi: dökme bronz Rönesans portre madalyası (Pisanello / Matteo de' Pasti / Niccolò Fiorentino / Bertoldo çizgisi).

v3 (MDL, Kasım 2026; kurul SA1-Ö6/E4, PK2, AN2, KA1-V9 — ayrıntı ve kaynaklar: notlar_madalya.md)
  Yükseklik alanı (px) → normal → üst-sol yönlü ışık + zayıf dolgu + metal yansıması, çok ölçekli ortam kapanması, yükseklik alanı gölgesi,
  patina (çukurda koyu kahve/yeşilimsi, yüksek ve dışbükey yerde el değmiş parlak bronz, benekli), döküm dokusu + gözenekler; kenar halkası,
  ince iç fileto, kabartma harfli yazıt. Portre: gerçek kafa oranı (derinlik ≈ 0,86 × yükseklik; v1/v2'de kafatası kulağın arkasında ~130 px kısaydı
  → "kutu kafa"), katmanlı kabartma (büst → boyun → baş → kulak → giysi → saç → başlık; her katman alttakinden yuvarlak duvarla yükselir),
  anatomik modelaj (alın, kaş kemeri, göz çukuru + kapaklar, elmacık, yanak çukuru/dolgunluğu, burun kanadı, nazolabial, dudaklar, çene, çene kemiği,
  gırtlak, boyun kası, yaş kırışıkları); saç = tepe girdabından yayılan, alttan oyulmuş örtüşen tutamlar; başlık/giysi = kumaş kütlesi + kıvrımlar.
  Kişiye özgü profiller (PROFILES): m_giovanni · m_cosimo (+ m_cosimo_genc, age=) · m_lorenzo · m_cossa · m_cossa_tiara · c6_piero (= m_piero) ·
  m_savonarola. Diğer ERKEK anahtarlar medal.PEOPLE parametrelerinden genel v3 yüze çevrilir; örtülü/kadın profilleri eski üreteçte kalır (v2/v1).
  Benzerlik iddiası YOK: tarihsel portrelerin genel karakteri (burun/çene/başlık), "madalya stili".
API (eski imzalar aynen): medal_img(key, metal, inscription, flip, size) · medal_array_b(...) · medal_shadow(...) ·
  draw_medal_b(f, key, x, y, size, metal, flip, alpha, tilt, glint, inscription, shadow)
Yeni seçenekler (varsayılanları eski çağrıları bozmaz): age= (yaş; None → AUTO_AGE açıkken çekim yılı − doğum yılı, yoksa kanonik yaş) ·
  stamp= (None → çekim yılı < 1438 ise otomatik "TEMSİLÎ" damgası [donem.portrait_medal_is_anachronistic]; False → yok; True/metin → zorla).
Bayraklar: V3 (False → v2/v1 üreteç), AUTO_AGE, STAMP_AUTO, MEDAL_VER (önbellek sürümü; görünüm değişince artır).
v2 (ENG-A) ve v1 (medal.py) kodu yedek olarak durur (V3=False ya da kadın/örtülü profil).
"""
import functools
import math
import zlib

import cv2
import numpy as np
import skia

import cilt_medici as CM
import cilt_wall as CW
import donem as DN
import medal
import sk
from sk import clamp

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
# v3 ek anahtarlar (eski üreteçle de çizilebilsin diye v1 uyumlu parametreler; v3 görünüşü PROFILES'tan gelir)
medal.PEOPLE.setdefault("m_cossa", dict(nose=11, hook=2, brow=2, lip=3, lip2=5, chin=3, jaw=1.15, fore=2, age=0.55, jowl=0.7, neck=1.3,
                                         hair="none", hat="camauro", beard=None, garment="cassock", mouth_open=0.0))
medal.PEOPLE.setdefault("m_cossa_tiara", dict(medal.PEOPLE["m_cossa"]))
medal.PEOPLE.setdefault("m_savonarola", dict(nose=34, hook=12, brow=6, lip=4, lip2=7, chin=8, jaw=1.12, fore=0, age=0.45, jowl=0.05, neck=1.0,
                                              hair="none", hat="cap_black", beard=None, garment="robe", mouth_open=0.0))
medal.PEOPLE.setdefault("m_piero", dict(nose=14, hook=4, brow=3, lip=2, lip2=4, chin=4, jaw=1.12, fore=2, age=0.55, jowl=0.5, neck=1.25,
                                         hair="short", hat="none", beard=None, garment="robe", mouth_open=0.0))
medal.PEOPLE.setdefault("m_cosimo_genc", dict(medal.PEOPLE["m_cosimo"], age=0.3, jowl=0.04))
# Cossa: Vaftizhane'deki mezar yazıtı "IOANNES QVONDAM PAPA XXIII" (Donatello–Michelozzo) → madalya yazıtı ondan; Savonarola: dönemin madalya yazıtı kısaltması
medal.INSCR.setdefault("m_cossa", "IOANNES · QVONDAM · PAPA · XXIII ·")
medal.INSCR.setdefault("m_cossa_tiara", "IOANNES · QVONDAM · PAPA · XXIII ·")
medal.INSCR.setdefault("m_savonarola", "HIERONYMVS · SAVO · FER · ORD · PRAED ·")
medal.INSCR.setdefault("m_piero", "PETRVS · MEDICES · COSMI · F ·")
medal.INSCR.setdefault("m_cosimo_genc", "COSMVS · MEDICES ·")
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




# ═════════════════════════════ PORTRE ÜRETECİ v3 (MDL) ═════════════════════════════
V3 = True                       # False → v2/v1 üreteç (eski görünüş)
MEDAL_VER = 3                   # önbellek sürümü (lru anahtarlarına girer; görünüş değişince artır)
AUTO_AGE = True                 # draw_medal_b: age verilmemişse çekim yılı − doğum yılı (PROFILES 'born' + 'young' olan kişiler; 5 yıla yuvarlı)
STAMP_AUTO = True               # draw_medal_b: çekim yılı < 1438 → "TEMSİLÎ" damgası (KA1-V9; donem.portrait_medal_is_anachronistic)
STAMP_TEXT = "TEMSİLÎ"
STAMP_SAFE = (90.0, 60.0, 1830.0, 924.0)          # damga ekran güvenli alanı (altyazı bandı 930'un üstü; HUD dışı)
STAMP_ANGLE = 58.0              # damga yönü (derece; 90 = tam alt): ekran merkezine bakan yana 25° kaydırılır → gece mum havuzunda kalır (≥4,5:1)
PROFILE_ALIAS = {"c7_pazzi_lor": "m_lorenzo", "m_piero": "c6_piero", "m_cosimo_genc": "m_cosimo"}
AGE_FIXED = {"m_cosimo_genc": 40.0}             # sabit yaşlı anahtar (sahne türleri age= geçiremese de genç Cosimo seçilebilsin)

S = medal.S
_INFO = skia.ImageInfo.Make(S, S, skia.ColorType.kRGBA_F16_ColorType, skia.AlphaType.kPremul_AlphaType)
YY, XX = np.mgrid[0:S, 0:S].astype(np.float32)


# ───────────────────────────── tuval / yol ─────────────────────────────
class T:
    """F16 gri tuval: değerler doğrudan px yüksekliği olabilir (>1 serbest)."""

    def __init__(self):
        self.s = skia.Surface.MakeRaster(_INFO)
        self.c = self.s.getCanvas()
        self.c.clear(skia.Color4f(0, 0, 0, 1))

    @staticmethod
    def paint(v=1.0, w=0.0, blur=0.0, mode=None, cap="round"):
        p = skia.Paint(AntiAlias=True)
        p.setColor4f(skia.Color4f(float(v), float(v), float(v), 1.0))
        if w:
            p.setStyle(skia.Paint.kStroke_Style)
            p.setStrokeWidth(float(w))
            p.setStrokeCap(skia.Paint.kRound_Cap if cap == "round" else skia.Paint.kButt_Cap)
            p.setStrokeJoin(skia.Paint.kRound_Join)
        if blur > 0:
            p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, float(blur)))
        if mode == "max":
            p.setBlendMode(skia.BlendMode.kLighten)
        elif mode == "min":
            p.setBlendMode(skia.BlendMode.kDarken)
        return p

    def fill(self, path, v=1.0, blur=0.0, mode=None):
        self.c.drawPath(path, self.paint(v, 0, blur, mode))
        return self

    def line(self, path, w, v=1.0, blur=0.0, mode=None, cap="round"):
        self.c.drawPath(path, self.paint(v, w, blur, mode, cap))
        return self

    def arr(self):
        return self.s.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_F16_ColorType)[..., 0].astype(np.float32)


def P(pts, close=False, t=0.5):
    return sk.smooth_path([tuple(map(float, q)) for q in pts], close, t)


def cr(pts, n=40, closed=False):
    """Catmull-Rom örnekleme → (k,2)."""
    Q = np.asarray(pts, np.float32)
    Q = np.vstack([Q[-1:], Q, Q[:2]]) if closed else np.vstack([Q[:1], Q, Q[-1:]])
    segs = len(Q) - 3
    m = max(2, int(round(n / max(1, segs))))
    out = []
    for i in range(segs):
        p0, p1, p2, p3 = Q[i], Q[i + 1], Q[i + 2], Q[i + 3]
        for j in range(m):
            t = j / m
            out.append(0.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (3 * p1 - p0 - 3 * p2 + p3) * t ** 3))
    if not closed:
        out.append(Q[-2])
    return np.array(out, np.float32)


def band(pts, w, n=48):
    """Merkez çizgisi etrafında şerit (kapalı yol). w: sayı | (w0, w1) | işlev(t)."""
    c = cr(pts, n)
    tg = np.gradient(c, axis=0)
    tg /= np.linalg.norm(tg, axis=1, keepdims=True) + 1e-6
    nr = np.stack([-tg[:, 1], tg[:, 0]], 1)
    t = np.linspace(0, 1, len(c))
    if callable(w):
        ww = np.array([w(x) for x in t], np.float32)
    elif isinstance(w, tuple):
        ww = w[0] + (w[1] - w[0]) * t
    else:
        ww = np.full(len(c), float(w), np.float32)
    L = c + nr * (ww[:, None] / 2)
    R = c - nr * (ww[:, None] / 2)
    poly = np.vstack([L, R[::-1]])
    return sk.poly_path([tuple(map(float, q)) for q in poly], True)


def mask(*paths, blur=0.0):
    t = T()
    for p_ in paths:
        t.fill(p_, 1.0, blur)
    return np.clip(t.arr(), 0, 1)


# ───────────────────────────── yükseklik yardımcıları ─────────────────────────────
def G(a, s):
    if s <= 0:
        return a
    if s > 8:
        f = max(2, int(s // 4))
        h, w = a.shape
        sm = cv2.resize(a, (w // f, h // f), interpolation=cv2.INTER_AREA)
        sm = cv2.GaussianBlur(sm, (0, 0), s / f)
        up = cv2.resize(sm, (w, h), interpolation=cv2.INTER_LINEAR)
        return cv2.GaussianBlur(up, (0, 0), f * 0.6)
    return cv2.GaussianBlur(a, (0, 0), s)


def dt(m):
    return cv2.distanceTransform((m > 0.5).astype(np.uint8), cv2.DIST_L2, 5)


def edge(m, r, d=None):
    """Yuvarlak kenar (çeyrek daire): kontur 0 → r px içeride 1."""
    d = dt(m) if d is None else d
    t = np.clip((d + 0.5) / r, 0, 1)
    return np.sqrt(np.clip(1 - (1 - t) ** 2, 0, 1)) * np.clip(m, 0, 1)


def pillow(m, s):
    p = G(m, s) * m
    mx = float(p.max())
    return p / mx if mx > 0 else p


def bump(H, cx, cy, rx, ry, a, rot=0.0):
    r = 3.0 * max(rx, ry)
    x0, x1 = int(max(0, cx - r)), int(min(S, cx + r + 1))
    y0, y1 = int(max(0, cy - r)), int(min(S, cy + r + 1))
    if x1 <= x0 or y1 <= y0:
        return
    xx = XX[y0:y1, x0:x1] - cx
    yy = YY[y0:y1, x0:x1] - cy
    if rot:
        c_, s_ = math.cos(rot), math.sin(rot)
        xx, yy = xx * c_ + yy * s_, -xx * s_ + yy * c_
    H[y0:y1, x0:x1] += a * np.exp(-((xx / rx) ** 2 + (yy / ry) ** 2))


def ridges(items, mode="max"):
    """items: [(yol, genişlik, genlik)] → bulanık çizgi tepeleri (Gauss kesit; tepe = genlik). mode: max | over."""
    t = T()
    for (p_, w, a) in items:
        sg = max(0.8, w / 2.6)
        core = max(1.0, w * 0.35)
        pk = math.erf(core / (2 * math.sqrt(2) * sg))
        t.line(p_, core, a / max(1e-3, pk), sg, "max" if mode == "max" else None)
    return t.arr()


def grooves(items):
    """items: [(yol, genişlik, derinlik)] → pozitif oluk derinliği alanı (H'den çıkar)."""
    return ridges(items, "max")


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def noise(seed, s, amp=1.0):
    rs = np.random.RandomState(seed)
    n = rs.standard_normal((S, S)).astype(np.float32)
    n = G(n, s)
    sd = float(n.std()) + 1e-6
    return n / sd * amp


# ───────────────────────────── malzeme: dökme bronz ─────────────────────────────
METALS = {
    # (çıplak/aşınmış metal, ana ton, patina koyu, patina yeşil, parlama rengi)
    "bronze": ((0.92, 0.68, 0.40), (0.58, 0.39, 0.215), (0.165, 0.125, 0.078), (0.15, 0.185, 0.13), (1.00, 0.85, 0.60)),
    "gold": ((1.00, 0.88, 0.52), (0.84, 0.64, 0.27), (0.38, 0.26, 0.09), (0.36, 0.30, 0.12), (1.00, 0.95, 0.75)),
    "silver": ((0.95, 0.95, 0.97), (0.68, 0.68, 0.71), (0.22, 0.22, 0.24), (0.22, 0.24, 0.25), (1.00, 1.00, 1.00)),
}
LIGHT = (-0.50, -0.62, 0.60)          # üst-sol ışık (x sağ, y aşağı, z izleyiciye)


def _norm3(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def cast_shadow(H, light=LIGHT, steps=56, step=1.4, slope=0.95, soft=2.4):
    """Yükseklik alanı gölgesi: ışığa doğru ilerleyen ışın üstünde daha yüksek nokta → gölge. 1 = aydınlık."""
    lx, ly, _ = light
    hl = math.hypot(lx, ly)
    dx, dy = lx / hl, ly / hl
    occ = np.full(H.shape, -1e9, np.float32)
    h, w = H.shape
    for k in range(1, steps + 1):
        sx, sy = int(round(dx * k * step)), int(round(dy * k * step))
        # kaydırılmış[p] = H[p + (sx, sy)]
        sh = np.full(H.shape, 0.0, np.float32)
        ys0, ys1 = max(0, -sy), min(h, h - sy)
        xs0, xs1 = max(0, -sx), min(w, w - sx)
        sh[ys0:ys1, xs0:xs1] = H[ys0 + sy:ys1 + sy, xs0 + sx:xs1 + sx]
        np.maximum(occ, sh - k * step * slope, out=occ)
    m = occ - H
    lit = 1.0 - np.clip(m / soft, 0, 1)
    return cv2.GaussianBlur(lit, (0, 0), 1.6)


def shade(H, alpha, metal="bronze", seed=11, wear=1.0, patina=1.0, cast=True):
    """H: px yüksekliği (S×S). → RGBA float (0..1)."""
    bare, base, pat_d, pat_g, spc = [np.array(c, np.float32) for c in METALS.get(metal, METALS["bronze"])]
    h = cv2.GaussianBlur(H, (0, 0), 0.9)
    gx = cv2.Sobel(h, cv2.CV_32F, 1, 0, ksize=3) / 8.0
    gy = cv2.Sobel(h, cv2.CV_32F, 0, 1, ksize=3) / 8.0
    inv = 1.0 / np.sqrt(gx * gx + gy * gy + 1.0)
    nx, ny, nz = -gx * inv, -gy * inv, inv
    lx, ly, lz = _norm3(LIGHT)
    ndl = nx * lx + ny * ly + nz * lz
    dif = np.clip((ndl + 0.10) / 1.10, 0, 1)
    hx, hy, hz = _norm3((lx, ly, lz + 1.0))
    ndh = np.clip(nx * hx + ny * hy + nz * hz, 0, 1)
    # ikinci (dolgu) ışık: sağ-alt, zayıf → kabartmanın gölgeli yanı tümden kör olmasın
    fx, fy, fz = _norm3((0.55, 0.35, 0.75))
    fil = np.clip(nx * fx + ny * fy + nz * fz, 0, 1)
    # boşluk (AO) ve dışbükeylik (aşınma)
    c1 = np.clip((G(h, 3.0) - h) / 1.6, 0, 1)
    c2 = np.clip((G(h, 12.0) - h) / 6.0, 0, 1)
    c3 = np.clip((G(h, 34.0) - h) / 14.0, 0, 1)
    cav = np.clip(0.45 * c1 + 0.35 * c2 + 0.30 * c3, 0, 1)
    cvx = np.clip((h - G(h, 4.0)) / 1.3, 0, 1)
    top = smoothstep(26, 62, h)
    sh = cast_shadow(h) if cast else np.ones_like(h)
    # patina: genel koyu kahve + çukurlarda yeşilimsi; yüksek, dışbükey yerler el değmiş (aşınmış) parlak bronz
    mot = noise(seed, 26.0, 1.0) * 0.5 + noise(seed + 1, 7.0, 1.0) * 0.25
    p = np.clip(0.56 * patina + 0.95 * cav + 0.16 * mot - wear * (0.60 * cvx + 0.42 * top), 0, 1)
    pg = np.clip(cav * 1.6 - 0.25 + 0.2 * noise(seed + 2, 10.0, 1.0), 0, 1) * p
    metal_c = base[None, None, :] * (1 - top[..., None] * 0.35 * wear) + bare[None, None, :] * (top[..., None] * 0.35 * wear)
    metal_c = metal_c * (1 - cvx[..., None] * 0.30 * wear) + bare[None, None, :] * (cvx[..., None] * 0.30 * wear)
    patc = pat_d[None, None, :] * (1 - pg[..., None]) + pat_g[None, None, :] * pg[..., None]
    alb = metal_c * (1 - p[..., None]) + patc * p[..., None]
    ao = 1.0 - 0.55 * cav
    light = 0.20 + 0.95 * dif * (0.30 + 0.70 * sh) + 0.16 * fil
    col = alb * (light * ao)[..., None]
    spec = (0.22 * ndh ** 10 + 0.55 * ndh ** 60) * (0.35 + 0.65 * sh) * (1 - 0.75 * p) * ao
    col = col + spc[None, None, :] * spec[..., None]
    col = np.clip(col, 0, 1)
    return np.dstack([col, np.clip(alpha, 0, 1)]).astype(np.float32)


# ───────────────────────────── madalya gövdesi ─────────────────────────────
R_DISC, R_RIM_IN, R_FIELD = 484.0, 450.0, 404.0
RR = np.hypot(XX - S / 2, YY - S / 2)
ANG = np.arctan2(YY - S / 2, XX - S / 2)


def body_height(inscription=None, seed=5, legend_r=429.0, legend_px=50, track=4.0):
    """Alan (hafif içbükey, döküm dokusu) + kenar halkası + iç ince fileto + kabartma yazı. → (H, alfa)."""
    r = RR
    alpha = np.clip(R_DISC + 0.5 - r, 0, 1)
    # alan: kenara doğru hafif yükselen çanak + düşük frekans dalga (el işi döküm)
    field = 5.0 * (r / R_RIM_IN) ** 2 + noise(seed, 40.0, 0.9) + noise(seed + 3, 9.0, 0.35)
    # döküm dokusu: ince tane + gözenekler
    grain = noise(seed + 5, 0.9, 0.10) + noise(seed + 6, 2.4, 0.12)
    rs = np.random.RandomState(seed + 9)
    pits = np.zeros((S, S), np.float32)
    for _ in range(60):
        a_ = rs.uniform(0, 2 * math.pi)
        rr_ = R_FIELD * math.sqrt(rs.uniform(0, 1))
        bump(pits, S / 2 + rr_ * math.cos(a_), S / 2 + rr_ * math.sin(a_), rs.uniform(1.0, 2.6), rs.uniform(1.0, 2.4), -rs.uniform(0.6, 1.8))
    # kenar halkası: iç duvar (yumuşak), düz tepe, dış pah
    rim_in = smoothstep(R_RIM_IN - 4, R_RIM_IN + 7, r)
    rim_top = 30.0 + 1.6 * np.cos(ANG * 3 + 0.7) + noise(seed + 11, 14.0, 0.8)
    bevel = 1.0 - 0.45 * smoothstep(R_DISC - 12, R_DISC + 0.5, r) ** 1.6
    rim = rim_in * rim_top * bevel
    # iç fileto (ince kabarık çizgi)
    fil = 4.2 * np.exp(-((r - R_FIELD) / 2.4) ** 2)
    Hh = np.maximum(field + grain + pits + fil, rim + grain * 0.6)
    if inscription:
        m = medal.ring_text_mask(inscription, legend_r, legend_px, track=track)
        m = cv2.GaussianBlur(m, (0, 0), 0.6)
        lt = 8.5 * edge(m, 2.2) + 0.6 * noise(seed + 13, 3.0, 1.0) * (m > 0.5)
        Hh = np.maximum(Hh, field + lt)
    return Hh.astype(np.float32), alpha


# ───────────────────────────── katman bindirme ─────────────────────────────
def over(H, X, m, r=8.0, lift=6.0, smooth_under=0.0):
    """X katmanını H'nin üstüne koy: kenarda H'den başlayan yuvarlak duvar, içeride max(X, H+lift).
    smooth_under > 0: kalın örtü (kukuleta, takke) alttaki biçimi yalnız YUMUŞATILMIŞ olarak izler (kulak/burun ayrıntısı kumaştan sızmaz)."""
    e = edge(m, r)
    Hu = G(H, smooth_under) if smooth_under > 0 else H
    X2 = np.maximum(X, Hu + lift)
    return H + (X2 - H) * e


# ───────────────────────────── profil geometrisi (sağa bakan; v1 profil uzayı) ─────────────────────────────
DEF = dict(nose=12, hook=2, hump=None, flat=0.0, tipr=1.0, alaw=1.0, brow=3, fore=2, nasion=4,
           lip=1, lip2=3, lipt=1.0, chin=2, jaw=1.0, age=0.4, jowl=0.05, neck=1.0, face_len=1.0,
           cheekbone=0.5, hollow=0.3, full=0.0, dbl=0.0, eye_deep=0.5, lids=0.4, adam=0.6, skull=1.0, mouth_w=1.0,
           hair="short", hat=None, beard=None, garment="lucco", scale=1.0, dy=0.0, dx=0.0)


def head_geom(p):
    fl = p["face_len"]
    YB = 333.0

    def Y(y):
        return YB + (y - YB) * fl if y > YB else y
    n, hk, br, fo = p["nose"], p["hook"], p["brow"], p["fore"]
    hump = p["hump"] if p["hump"] is not None else max(0.0, hk * 0.7)
    lip, lip2, ch, jw = p["lip"], p["lip2"], p["chin"], p["jaw"]
    dbl, flat, sk_ = p["dbl"], p["flat"], p["skull"]
    F = {}
    bx = 214 - 30 * (sk_ - 1)
    F["vertex"] = (432, 163 - 10 * (sk_ - 1))
    F["crown_f"] = (532 + fo * 0.4, 187)
    F["fore_top"] = (578 + fo, 233)
    F["fore_mid"] = (599 + fo * 0.6, 283)
    F["brow"] = (607 + br * 0.9, Y(334))
    F["nasion"] = (597 + br * 0.3 - p["nasion"] * 0.5, Y(362))
    tip = (642 + n, Y(466) + hk * 0.8 - flat * 3)
    N = F["nasion"]
    dx_, dy_ = tip[0] - N[0], tip[1] - N[1]
    L = math.hypot(dx_, dy_)
    ux, uy = dx_ / L, dy_ / L
    ox, oy = uy, -ux
    dors = []
    for t in (0.20, 0.42, 0.64, 0.84):
        b = hump * math.sin(math.pi * min(1.0, t / 0.92)) - flat * 6.0 * math.sin(math.pi * t)
        dors.append((N[0] + dx_ * t + ox * b, N[1] + dy_ * t + oy * b))
    F["dorsum"] = dors
    F["tip"] = tip
    tr_ = 9.0 * p["tipr"]
    F["infratip"] = (tip[0] - 4 - tr_ * 0.35, tip[1] + 10 + tr_ * 0.45 - hk * 0.25)
    F["columella"] = (tip[0] - 18 - tr_ * 0.6, Y(488) + hk * 0.2)
    F["subnasale"] = (608 + lip * 0.3, Y(494))
    F["philtrum"] = (610 + lip * 0.6, Y(503))
    F["ls"] = (614 + lip, Y(515))
    F["sto"] = (605 + lip * 0.4 + lip2 * 0.15, Y(528))
    F["li"] = (610 + lip2, Y(540))
    F["li_b"] = (603 + lip2 * 0.55, Y(551))
    F["sulcus"] = (597 + ch * 0.25 + lip2 * 0.1, Y(565))
    F["pog"] = (606 + ch, Y(594))
    F["gn"] = (598 + ch * 0.85, Y(615))
    F["me"] = (579 + ch * 0.6, Y(629))
    F["subm"] = (552 + ch * 0.3, Y(637) + dbl * 15)
    F["cerv"] = (528 - dbl * 6, Y(652) + dbl * 22)
    gon = (420 - 16 * (jw - 1), Y(582) + 18 * (jw - 1) + 12 * p["jowl"])
    F["gonion"] = gon
    front = [F["crown_f"], F["fore_top"], F["fore_mid"], F["brow"], F["nasion"]] + dors + [tip, F["infratip"], F["columella"],
             F["subnasale"], F["philtrum"], F["ls"], F["sto"], F["li"], F["li_b"], F["sulcus"], F["pog"], F["gn"], F["me"]]
    jaw_line = [(548, Y(634) + 2 * (jw - 1)), (500, Y(624) + 6 * (jw - 1)), (456, Y(606) + 10 * (jw - 1) + 6 * p["jowl"]), gon,
                (406, Y(548)), (400, Y(508))]
    backc = [(352, Y(508)), (300, 506), (252, 494), (bx + 6, 450), (bx, 372), (bx + 16, 292), (272, 222), (346, 174), F["vertex"]]
    F["head"] = front + jaw_line + backc
    # kulak
    ex, ey = 380.0, Y(418)
    eh = 64.0 * (1 + 0.12 * p["age"]) * (fl ** 0.5)
    F["ear_c"] = (ex, ey)
    F["ear_h"] = eh
    F["ear"] = [(ex + 24, ey - eh * 0.84), (ex + 4, ey - eh * 1.0), (ex - 18, ey - eh * 0.92), (ex - 30, ey - eh * 0.58), (ex - 33, ey - eh * 0.06),
                (ex - 27, ey + eh * 0.44), (ex - 15, ey + eh * 0.80), (ex + 2, ey + eh * 1.0), (ex + 17, ey + eh * 0.93), (ex + 25, ey + eh * 0.64),
                (ex + 29, ey + eh * 0.12), (ex + 31, ey - eh * 0.44)]
    # boyun
    nk = p["neck"]
    nx = (nk - 1.0) * 34
    F["throat"] = (534 + nx * 0.3, Y(692))
    F["neck_front"] = [F["me"], F["subm"], F["cerv"], (530 + nx * 0.3, Y(672)), F["throat"], (548 + nx * 0.6, Y(730)), (572 + nx, Y(772)), (596 + nx, 820)]
    F["neck_back"] = [(250 - nx, 820), (252 - nx, 700), (258 - nx * 0.6, 620), (254, 556), (246, 490)]
    F["neck"] = F["neck_front"] + F["neck_back"] + [(330, 470), (420, 520), (500, 600)]
    yb = Y(760)
    F["bust"] = [(590 + nx, yb - 18), (628 + nx, yb + 26), (658 + nx, yb + 86), (674 + nx * 0.5, yb + 160), (680, 1000), (70, 1000), (74, yb + 150),
                 (92, yb + 50), (124, yb - 32), (170, yb - 92), (214, yb - 124), (256 - nx, yb - 140)]
    F["yb"] = yb
    F["eye"] = (N[0] - 33, N[1] + 12)
    F["Y"] = Y
    return F


def sculpt_face(H, F, p):
    """Yüz modelajı: yerel tümsek/çukur + yumuşak oluklar (px)."""
    a = p["age"]
    E = F["eye"]
    ex, ey = E
    N, tip = F["nasion"], F["tip"]
    br = p["brow"]
    # alın tümseği, kaş kemeri, şakak
    fm = F["fore_mid"]
    bump(H, fm[0] - 48, fm[1] - 6, 46, 40, 5.0)
    bump(H, ex + 14, F["brow"][1] + 6, 30, 8.5, 3.2 + 0.7 * br, rot=-0.10)
    bump(H, ex - 56, ey - 26, 24, 34, -(2.0 + 5.0 * p["hollow"] * (0.4 + a)))
    # göz çukuru, göz küresi, kapaklar (es: göz ölçeği — madalya okunurluğu için gerçekten biraz iri)
    es = p.get("eye_s", 1.28)

    def e(dx, dy):
        return (ex + dx * es, ey + dy * es)
    bump(H, ex + 2 * es, ey - 3 * es, 25 * es, 17 * es, -(4.5 + 4.0 * p["eye_deep"]))
    bump(H, ex + 7 * es, ey + 1 * es, 12.5 * es, 9.5 * es, 5.5)
    rid = [(P([e(-15, 1), e(-3, -8), e(11, -7.5), e(19, -1)]), (5.0 + 2.0 * p["lids"]) * es, 2.6 + 1.3 * p["lids"]),
           (P([e(-12, 4), e(3, 9), e(17, 5)]), 3.6 * es, 1.6)]
    gro = [(P([e(-15, 1), e(1, -3.5), e(18, 0.5)]), 2.2 * es, 3.0),
           (P([e(-12, -7), e(2, -15 + 2 * p["lids"]), e(16, -11)]), 2.6 * es, 1.4 + 1.2 * a)]
    if a > 0.3:
        gro += [(P([e(-10, 15), e(6, 20), e(21, 15)]), 3.5 * es, 0.6 + 2.2 * a)]
        for k in (-9, 1, 11):
            gro.append((P([e(-17, 1 + k * 0.2), e(-28, -1 + k * 0.6), e(-38, -3 + k)]), 1.8, 1.1 * a))
    q = e(13, -0.5)
    bump(H, q[0], q[1], 2.8 * es, 4.2 * es, -1.6)                       # göz bebeği izi
    # elmacık, yanak çukuru / dolgunluğu, gıdı
    cb = p["cheekbone"]
    bump(H, ex - 26, ey + 36, 44, 16, 3.5 + 6.0 * cb, rot=-0.12)
    bump(H, ex - 8, ey + 92, 34, 30, -7.5 * p["hollow"] + 8.0 * p["full"])
    bump(H, ex + 6, ey + 74, 40, 40, 6.0 * p["full"])
    me = F["me"]
    bump(H, ex + 0, me[1] - 26, 32, 22, 9.0 * p["jowl"] + 4.0 * p["full"])
    # burun: yan yüz, kanat, kanat oluğu, burun deliği, uç
    mx_, my_ = N[0] + (tip[0] - N[0]) * 0.55 - 9, N[1] + (tip[1] - N[1]) * 0.55 + 2
    ang = math.atan2(tip[1] - N[1], tip[0] - N[0])
    bump(H, mx_, my_, 30, 8.5, 3.0, rot=ang)
    aw = p["alaw"]
    al = (tip[0] - 27 - 3 * aw, tip[1] + 9 + 2 * aw)
    bump(H, al[0], al[1], 13.0 * aw, 10.5, 6.0)
    gro.append((P([(al[0] + 6, al[1] - 13), (al[0] - 9, al[1] - 12.5 * (0.9 + 0.1 * aw)), (al[0] - 15 * aw, al[1] + 1), (al[0] - 8, al[1] + 11)]), 3.0, 2.6))
    bump(H, al[0] + 7, al[1] + 9, 7.0, 3.4, -3.2)
    bump(H, tip[0] - 9, tip[1] - 2, 9.0 * p["tipr"], 8.5 * p["tipr"], 2.0)
    # nazolabial oluk + yanak sırtı
    sto = F["sto"]
    nl = [(al[0] - 14, al[1] + 3), (al[0] - 19, al[1] + 22), (sto[0] - 27, sto[1] + 4), (sto[0] - 24, sto[1] + 19)]
    gro.append((P(nl), 4.0 + 2.0 * a, 1.0 + 3.6 * a))
    rid.append((P([(q[0] - 9, q[1]) for q in nl[:3]]), 10.0, 1.2 + 2.2 * a))
    # ağız
    ls, li = F["ls"], F["li"]
    mw = p["mouth_w"]
    bump(H, ls[0] - 10, ls[1] - 2, 12 * mw, 7.5 * p["lipt"], 2.4 * p["lipt"])
    bump(H, li[0] - 10, li[1], 12 * mw, 8 * p["lipt"], 3.0 * p["lipt"])
    gro.append((P([(sto[0] + 1, sto[1]), (sto[0] - 12 * mw, sto[1] + 1), (sto[0] - 24 * mw, sto[1] + 3)]), 2.3, 3.0))
    bump(H, sto[0] - 25 * mw, sto[1] + 3, 4.2, 4.2, -2.6)
    gro.append((P([F["subnasale"], (F["philtrum"][0] - 4, F["philtrum"][1]), (ls[0] - 4, ls[1] - 4)]), 4.0, 0.8))
    # çene
    su, pg = F["sulcus"], F["pog"]
    gro.append((P([(su[0] - 2, su[1]), (su[0] - 12, su[1] + 1), (su[0] - 22, su[1] + 4)]), 5.0, 2.4))
    bump(H, pg[0] - 13, pg[1] - 2, 14, 15, 4.0)
    # çene kemiği sırtı (alt kenar boyunca)
    gon = F["gonion"]
    rid.append((P([(me[0] - 6, me[1] - 7), (500, F["Y"](616) + 5 * (p["jaw"] - 1)), (456, F["Y"](598) + 9 * (p["jaw"] - 1)), (gon[0] + 6, gon[1] - 8), (gon[0] + 2, gon[1] - 40)]),
                10.0, 2.2 + 2.5 * (p["jaw"] - 0.8)))
    # yaş: alın kırışıkları
    if a > 0.5:
        for k in range(3):
            yk = F["fore_mid"][1] - 22 + k * 16
            gro.append((P([(fm[0] - 92, yk + 4), (fm[0] - 52, yk - 2), (fm[0] - 12, yk + 1)]), 2.2, 0.9 * (a - 0.4) * 2.0))
    H += ridges(rid)
    H -= grooves(gro)
    return H


def ear_height(Hloc, F, p):
    """Kulak: dış sarmal (helix) kenarı yüksek, içinde scapha oluğu, Y biçimli karşı sarmal, ön-altta küçük kepçe (concha), tragus, lob."""
    ex, ey = F["ear_c"]
    eh = F["ear_h"]
    m = mask(P(F["ear"], True, 0.5))
    X = Hloc + 3.5 + 3.0 * pillow(m, 12)
    E = np.zeros_like(X)
    bump(E, ex + 12, ey + eh * 0.08, 10, eh * 0.20, -6.0)                # kepçe (alt-ön)
    bump(E, ex + 8, ey - eh * 0.30, 8, eh * 0.12, -3.0)                  # üst kepçe (cymba)
    bump(E, ex + 25, ey + eh * 0.12, 5, 9, 3.0)                          # tragus
    bump(E, ex + 2, ey + eh * 0.80, 13, 11, 2.5)                         # lob
    rid = [(P([(ex + 24, ey - eh * 0.78), (ex + 4, ey - eh * 0.93), (ex - 17, ey - eh * 0.84), (ex - 27, ey - eh * 0.50), (ex - 28, ey + eh * 0.02),
               (ex - 21, ey + eh * 0.42), (ex - 8, ey + eh * 0.62)]), 10.0, 4.2),
           (P([(ex + 12, ey - eh * 0.66), (ex - 8, ey - eh * 0.56), (ex - 13, ey - eh * 0.18), (ex - 9, ey + eh * 0.22), (ex + 2, ey + eh * 0.44),
               (ex + 12, ey + eh * 0.50)]), 7.0, 2.8),
           (P([(ex - 8, ey - eh * 0.56), (ex + 6, ey - eh * 0.46), (ex + 18, ey - eh * 0.44)]), 5.0, 1.8)]
    gro = [(P([(ex + 16, ey - eh * 0.80), (ex - 4, ey - eh * 0.80), (ex - 20, ey - eh * 0.60), (ex - 21, ey - eh * 0.02), (ex - 14, ey + eh * 0.38)]), 3.6, 2.4)]
    E += ridges(rid) - grooves(gro)
    return X + E, m


# ───────────────────────────── portre bileşimi ─────────────────────────────
def merged(p):
    q = dict(DEF)
    q.update(p or {})
    return q


def portrait_base(p):
    """Gövde (büst → boyun → baş) + yüz + kulak. Dönüş: (H, F, masks)."""
    F = head_geom(p)
    m_bust = mask(P(F["bust"], True, 0.42))
    m_neck = mask(P(F["neck"], True, 0.42))
    m_head = mask(P(F["head"], True, 0.40))
    H = np.zeros((S, S), np.float32)
    Hb = 16.0 + 14.0 * pillow(m_bust, 70)
    H = over(H, Hb, m_bust, r=10, lift=0)
    Hn = 24.0 + 12.0 * pillow(m_neck, 40)
    H = over(H, Hn, m_neck, r=10, lift=4)
    Hh = 22.0 + 30.0 * pillow(m_head, 80)
    Hh = sculpt_face(Hh, F, p)
    # boyun kası (göğüs-köprücük-meme), gırtlak, yaşlı boyun
    Nn = np.zeros_like(H)
    ex, ey = F["ear_c"]
    th = F["throat"]
    Nn += ridges([(P([(ex - 4, ey + 78), (ex + 60, ey + 170), (th[0] - 10, 760), (th[0] + 6, 820)]), 30.0, 3.4)])
    bump(Nn, th[0] - 7, th[1], 9, 14, 4.0 * p["adam"])
    if p["age"] > 0.5:
        Nn -= grooves([(P([(F["cerv"][0] - 6, F["cerv"][1] + 6), (F["cerv"][0] - 40, F["cerv"][1] + 2)]), 3.0, 1.6 * p["age"]),
                       (P([(th[0] - 6, th[1] + 24), (th[0] - 50, th[1] + 18)]), 3.0, 1.4 * p["age"])])
    H = H + Nn * m_neck * (1 - m_head)
    H = over(H, Hh, m_head, r=13, lift=5)
    # çene kolu (ramus) ve kulak altı → ense geçişi yumuşak (yalnız çene ALT kenarı keskin okunur)
    gon = F["gonion"]
    w_s = mask(band([(gon[0] + 4, gon[1] - 6), (gon[0] - 4, gon[1] - 50), (F["ear_c"][0] + 10, F["ear_c"][1] + 80), (330, 506), (262, 496)], 46.0, 40), blur=10)
    H = H * (1 - w_s) + G(H, 9.0) * w_s
    He, m_ear = ear_height(H, F, p)
    H = over(H, He, m_ear, r=4, lift=3)
    return H, F, dict(bust=m_bust, neck=m_neck, head=m_head, ear=m_ear)


def frame_mtx(p):
    s = 1.0 * p.get("scale", 1.0)
    return np.float32([[s, 0, 86 + p.get("dx", 0.0) + (1 - s) * 470], [0, s, 7 + p.get("dy", 0.0) + (1 - s) * 420]])


def to_medal(Hp, p, flip=False):
    M = frame_mtx(p)
    Hm = cv2.warpAffine(Hp, M, (S, S), flags=cv2.INTER_LINEAR, borderValue=0)
    if flip:
        Hm = Hm[:, ::-1].copy()
    clip = smoothstep(398.0, 384.0, RR)
    return Hm * clip


# ───────────────────────────── saç ─────────────────────────────
def family(A, B, n, jit=0.0, seed=1):
    """İki kılavuz eğri arasında n tutam merkez çizgisi (aynı nokta sayılı)."""
    A, B = np.asarray(A, np.float32), np.asarray(B, np.float32)
    rs = np.random.RandomState(seed)
    out = []
    for i in range(n):
        t = i / max(1, n - 1)
        c = A * (1 - t) + B * t
        if jit:
            c = c + rs.uniform(-jit, jit, c.shape).astype(np.float32) * np.linspace(0.2, 1.0, len(c))[:, None]
        out.append([tuple(q) for q in c])
    return out


def wave_line(pts, amp, freq=1.0, phase=0.0, n=24):
    """Merkez çizgisine dik yönde S dalgası ekle (uçlarda sönen)."""
    c = cr(pts, n)
    tg = np.gradient(c, axis=0)
    tg /= np.linalg.norm(tg, axis=1, keepdims=True) + 1e-6
    nr = np.stack([-tg[:, 1], tg[:, 0]], 1)
    t = np.linspace(0, 1, len(c))
    off = amp * np.sin(2 * np.pi * freq * t + phase) * np.sin(np.pi * np.clip(t * 1.1, 0, 1))
    return [tuple(q) for q in (c + nr * off[:, None])[::2]]


def lock_layers2(locks, seed=3, amp=7.0, crest=4.5, fine=1):
    """Tutamlar ÖRTÜŞEREK (arkadan öne) çizilir: her tutam kendi yuvarlak sırtıyla öncekini örter → tutam sınırları kademe olarak okunur."""
    t = T()
    tm = T()
    gro = []
    rs = np.random.RandomState(seed)
    for (pts, w) in locks:
        def W(k, add=0.0, w_=w):
            return lambda u: k * w_ * (0.60 + 0.40 * math.sin(math.pi * min(1.0, 0.10 + u))) * (1 - 0.74 * u ** 2.0) + add
        b = band(pts, W(1.0), n=56)
        a = amp * rs.uniform(0.85, 1.15) + 0.05 * len(gro)
        t.fill(band(pts, W(1.0, 5.0), n=56), max(0.0, a - 4.2), blur=1.8)            # alttan oyma (tutam sınırı oluğu)
        t.fill(b, a - 2.0, blur=max(1.6, w * 0.08))
        t.fill(band(pts, W(0.66), n=56), a + crest, blur=max(3.0, w * 0.22))
        tm.fill(b, 1.0)
        c = cr(pts, 40)
        tg = np.gradient(c, axis=0)
        tg /= np.linalg.norm(tg, axis=1, keepdims=True) + 1e-6
        nr = np.stack([-tg[:, 1], tg[:, 0]], 1)
        for k in range(fine):
            off = (k - (fine - 1) / 2.0) * w * 0.30 + rs.uniform(-2.0, 2.0)
            q = c + nr * off
            q = q[int(len(q) * 0.10):int(len(q) * rs.uniform(0.70, 0.92))]
            if len(q) > 3:
                gro.append((P([tuple(v) for v in q[::4]]), 1.5, 0.9))
    R_ = t.arr()
    if gro:
        R_ -= grooves(gro)
    return R_, np.clip(tm.arr(), 0, 1)


def hair_layer(H, locks, thick=4.0, amp=7.0, seed=3, fine=1):
    """Uzun saç katmanı: örtüşen tutamlar + ince kabarıklık; başın üstünden yuvarlak duvarla yükselir."""
    R_, m = lock_layers2(locks, seed=seed, amp=amp, fine=fine)
    m = np.clip(G(m, 1.0) * 1.15, 0, 1)
    X = G(H, 14.0) + thick + 2.5 * pillow(m, 26) + R_
    return over(H, X, m, r=5, lift=3.0), m


GUIDES_LONG = [                                                                                    # hepsi tepe girdabından (≈420,174) yayılır
    [(432, 172), (500, 176), (556, 204), (588, 244), (598, 280), (596, 308)],                       # ön kâkül
    [(428, 174), (476, 192), (512, 234), (528, 276), (530, 302), (526, 322)],                       # arka kâkül / şakak
    [(422, 176), (452, 214), (472, 290), (466, 380), (444, 462), (410, 540), (384, 606)],           # yüzü çerçeveleyen (çene köşesinin ARKASINDAN)
    [(416, 178), (420, 232), (422, 324), (410, 440), (386, 540), (364, 630), (350, 690)],           # kulak üstü
    [(410, 178), (380, 228), (348, 330), (326, 446), (308, 556), (300, 650), (302, 722)],           # yan arka
    [(404, 176), (322, 186), (254, 232), (222, 318), (216, 420), (228, 530), (246, 640), (270, 724)],  # ense dış (omuza)
]


def _rs_guide(g, n=9):
    c = cr(g, 60)
    idx = np.linspace(0, len(c) - 1, n).round().astype(int)
    return [tuple(c[i]) for i in idx]


def locks_lorenzo(F, p, seed=5):
    """Arkadan öne sıralı (örtüşme sırası): ense → yan → kulak üstü → yüz çerçevesi → kâkül. Uçlar dışa hafif kıvrılır."""
    G_ = [_rs_guide(g) for g in GUIDES_LONG]
    rs = np.random.RandomState(seed)
    out = []
    for (a, b, n, w) in ((4, 5, 4, 44.0), (3, 4, 4, 44.0), (2, 3, 4, 42.0), (1, 2, 2, 36.0), (0, 1, 4, 30.0)):
        fam = family(G_[b], G_[a], n, 2.0, seed + a)
        for i, c in enumerate(fam):
            c = [tuple(q) for q in c]
            if a >= 2:
                x, y = c[-1]
                dl = rs.uniform(-14, 12)
                c[-1] = (x + rs.uniform(-4, 4), y + dl)
                c.append((x - 10 - rs.uniform(0, 10), y + dl + 10))           # uç dışa (arkaya) kıvrık
            if a == 0:                                        # kâkül uçları: düzensiz boy, hafif öne-aşağı
                x, y = c[-1]
                c[-1] = (x + rs.uniform(-3, 5), y + rs.uniform(-12, 6))
            amp_w = rs.uniform(3.0, 6.0) if a >= 2 else rs.uniform(1.0, 2.5)
            c = wave_line(c, amp_w, freq=rs.uniform(0.6, 1.1), phase=rs.uniform(0, 6.28), n=30)
            out.append((c, w + rs.uniform(-5, 5)))
    return out


WHORL = (420.0, 182.0)


def short_hair_pts(F, p, kind="short"):
    hl = {"short": 238, "crop": 242, "bowl": 290, "thin": 262}.get(kind, 240)
    return [(560, 194), (588, hl - 6), (588, hl + 4), (566, hl + 22), (538, hl + 44), (514, hl + 68), (498, 330), (474, 344), (458, 378), (452, 414),
            (436, 418), (424, 380), (404, 354), (380, 342), (352, 348), (334, 372), (322, 422), (304, 470), (280, 498), (250, 502), (230, 472),
            (214, 400), (214, 300), (246, 230), (310, 182), (380, 160), (460, 160), (520, 174)]


def locks_short(F, p, kind="short", seed=21):
    """Kısa saç: tepe girdabından dışa (ve yerçekimiyle aşağı) bakan virgül tutamlar; dıştakiler önce çizilir (içteki ucu üstüne biner)."""
    m = mask(P(short_hair_pts(F, p, kind), True, 0.45))
    rs = np.random.RandomState(seed)
    ys_, xs_ = np.nonzero(m[::18, ::18] > 0.5)
    pts = [(x * 18 + rs.uniform(-7, 7), y * 18 + rs.uniform(-7, 7)) for y, x in zip(ys_, xs_)]
    wx, wy = WHORL
    pts.sort(key=lambda q: -math.hypot(q[0] - wx, q[1] - wy))
    L0 = {"bowl": 54.0, "thin": 34.0}.get(kind, 44.0)
    locks = []
    for (x, y) in pts:
        d = math.hypot(x - wx, y - wy)
        if d < 10:
            continue
        ux, uy = (x - wx) / d, (y - wy) / d
        g = min(1.0, d / 160.0)                                   # uzaklaştıkça aşağı döner
        vx, vy = ux * (1 - 0.55 * g), uy * (1 - 0.55 * g) + 0.85 * g
        n_ = math.hypot(vx, vy)
        vx, vy = vx / n_, vy / n_
        L_ = L0 * rs.uniform(0.8, 1.2)
        cv_ = rs.uniform(-0.5, 0.5)
        x1, y1 = x + vx * L_, y + vy * L_
        mx_, my_ = (x + x1) / 2 - vy * L_ * 0.18 * (1 + cv_), (y + y1) / 2 + vx * L_ * 0.18 * (1 + cv_)
        x2, y2 = x1 - vy * 6 * (1 + cv_), y1 + vx * 6 * (1 + cv_)
        locks.append(([(x, y), (mx_, my_), (x1, y1), (x2, y2)], rs.uniform(20, 26)))
    return locks, m


def short_hair(H, F, p, thick=5.0, amp=4.0, kind="short"):
    locks, m = locks_short(F, p, kind)
    R_, _ = lock_layers2(locks, seed=9, amp=amp, crest=2.6, fine=1)
    m2 = np.clip(G(m, 1.2) * 1.1, 0, 1)
    X = G(H, 12.0) + thick + 2.0 * pillow(m2, 24) + R_ * m2
    return over(H, X, m2, r=4, lift=2.5), m2


# ───────────────────────────── başlıklar ─────────────────────────────
def tube_height(m, t):
    """Şerit maskesi → yuvarlak (boru) kesit yüksekliği 0..1."""
    d = dt(m)
    u = np.clip(d / (t * 0.5), 0, 1)
    return np.sqrt(np.clip(1 - (1 - u) ** 2, 0, 1)) * m


def cloth_folds(m, folds, valleys=(), base_s=40):
    """Kumaş: yumuşak kütle + geniş kıvrım sırtları + dar vadiler (yalnız maske içinde)."""
    R_ = ridges(folds) if folds else np.zeros((S, S), np.float32)
    V_ = grooves(list(valleys)) if valleys else 0.0
    return (R_ - V_) * m


def _roll(H, Cl, t, base=44.0, amp=32.0, n_pl=13, slant=18.0, seed=0):
    """Mazzocchio: yuvarlak uçlu, neredeyse dairesel kesitli dolgulu halka; burgulu dolgu dikişleri arasında kabarık dilimler."""
    tt = T()
    tt.line(P(Cl), t, 1.0)
    m_roll = np.clip(tt.arr(), 0, 1)
    roll_t = tube_height(m_roll, t)
    xs = np.clip((XX - Cl[-1][0]) / (Cl[0][0] - Cl[-1][0]), 0, 1)
    lat = 0.80 + 0.20 * np.sin(np.pi * xs)
    Xr = base + amp * roll_t * lat
    pl = []
    c_ = cr(Cl, 120)
    puff = np.zeros_like(H)
    for k in range(n_pl):
        u = (k + 0.5) / n_pl
        i = int(u * (len(c_) - 1))
        cxp, cyp = c_[i]
        pl.append((P([(cxp - slant, cyp - t * 0.50), (cxp - slant * 0.2, cyp - t * 0.18), (cxp + slant * 0.25, cyp + t * 0.18), (cxp + slant * 0.6, cyp + t * 0.50)]), 5.0, 5.0))
        u2 = (k + 1.0) / n_pl
        if u2 < 1.0:
            j = int(u2 * (len(c_) - 1))
            bump(puff, c_[j][0], c_[j][1], t * 0.16, t * 0.36, 3.0, rot=0.25)
    Xr = Xr + (puff - grooves(pl) * roll_t) * m_roll
    return over(H, Xr, m_roll, r=8, lift=6), m_roll


def _foggia_lobe(H, pts, flows, base=40.0, seed=0):
    """Foggia: rulonun üstünden kalkıp arkaya devrilen kumaş lobu; akış boyunca uzun kıvrımlar."""
    rs = np.random.RandomState(seed)
    m_fog = mask(P(pts, True, 0.40))
    Xf = G(H, 20) * 0.4 + base + 18.0 * pillow(m_fog, 46)
    fr, vl = [], []
    for k, fl in enumerate(flows):
        fr.append((P(fl), rs.uniform(26, 40), rs.uniform(4.5, 7.0)))
        q = [(x + rs.uniform(14, 20), y + rs.uniform(6, 12)) for (x, y) in fl]
        vl.append((P(q), 6.0, 3.6))
    Xf = Xf + cloth_folds(m_fog, fr, vl)
    return over(H, Xf, m_fog, r=8, lift=5), m_fog


def hat_cappuccio(H, F, p, style="tall"):
    """Floransa cappuccio'su.
    tall (Giovanni; Masaccio/Uccello freskolarındaki biçim): alnın üstünde kalın mazzocchio (öne ve arkaya taşar) + üstte buruşuk foggia + arkadan
         omuza sarkan becchetto; kulak açık, rulonun altında kısa kır saç.
    low  (Cosimo; Pontormo'nun ölüm sonrası portresindeki biçim): kulakları saran, çene/ense hizasında biten kumaş başlık (cuffia) + orta boy halka
         + alçak tepe + omza dökülen becchetto."""
    tall = style == "tall"
    hm = None
    if tall:
        tc = [(246, 300), (214, 400), (198, 510), (202, 620), (220, 730), (240, 840), (252, 920)]
        m_tail = mask(band(tc, (112.0, 92.0), n=60))
        Xt = G(H, 10) + 6.0 + 10.0 * tube_height(m_tail, 96.0)
        Xt = Xt + cloth_folds(m_tail, [(P([(q[0] + o, q[1]) for q in tc[1:]]), 18.0, 3.8) for o in (-26, 0, 24)],
                              [(P([(q[0] + o, q[1]) for q in tc[1:]]), 4.0, 2.6) for o in (-13, 13)])
        H = over(H, Xt, m_tail, r=7, lift=5)
        fog = [(604, 236), (608, 190), (594, 138), (556, 94), (496, 66), (424, 58), (356, 70), (296, 100), (250, 146), (222, 202), (214, 252),
               (330, 258), (480, 254)]
        flows = [[(590, 214), (560, 150), (490, 112), (400, 104), (316, 128), (256, 180), (232, 240)],
                 [(596, 238), (566, 186), (500, 150), (414, 142), (334, 160), (276, 210), (250, 262)],
                 [(560, 120), (490, 92), (410, 88), (330, 104), (272, 146), (240, 196)],
                 [(520, 196), (450, 184), (380, 190), (318, 220), (286, 262)]]
        H, m_fog = _foggia_lobe(H, fog, flows, base=42.0, seed=31)
        Cl = [(626, 286), (570, 276), (482, 268), (392, 266), (300, 272), (220, 288)]
        H, m_roll = _roll(H, Cl, 112.0, base=44.0, amp=34.0, n_pl=13, slant=26.0)
        hm = np.maximum(m_roll, m_fog)
    else:
        cap = [(590, 252), (568, 266), (540, 294), (516, 338), (500, 392), (490, 448), (484, 502), (478, 556), (456, 584), (404, 596), (340, 600),
               (276, 596), (220, 572), (184, 512), (172, 430), (180, 340), (212, 262), (276, 198), (360, 160), (456, 148), (538, 166), (580, 206)]
        m_cap = mask(P(cap, True, 0.42))
        X = G(H, 18.0) + 10.0 + 10.0 * pillow(m_cap, 60)
        rs = np.random.RandomState(39)
        fr, vl = [], []
        for k, (x0, w_, a_, bend) in enumerate(((262, 54.0, 5.0, -30), (330, 40.0, 3.6, -18), (402, 48.0, 4.4, -6), (452, 30.0, 2.6, 4))):
            fr.append((P([(x0 + 26, 258), (x0 + 4 + bend * 0.3, 350), (x0 - 12 + bend, 460), (x0 - 24 + bend * 1.4, 570 + rs.uniform(-12, 12))]), w_, a_))
            if k < 3:
                vl.append((P([(x0 + 52, 262), (x0 + 30 + bend * 0.3, 356), (x0 + 16 + bend, 466), (x0 + 6 + bend * 1.3, 566)]), 9.0, 2.6))
        fr.append((P([(300, 300), (380, 288), (460, 296)]), 30.0, 2.0))                 # rulonun altında yatay sarkma
        vl.append((P([(310, 322), (390, 312), (452, 318)]), 8.0, 1.6))
        X = X + cloth_folds(m_cap, fr, vl)
        # yüz kenarı: yuvarlak kask kenarı DEĞİL — hafif kalınlaşan, buruşuk kumaş kenarı
        edge_c = [(592, 250), (568, 266), (540, 294), (516, 338), (500, 392), (490, 448), (484, 502), (478, 556), (456, 586)]
        m_hem = mask(band(edge_c, 18.0, n=60)) * m_cap
        crumple = np.zeros_like(H)
        c_ = cr(edge_c, 40)
        for q in c_[::3]:
            bump(crumple, q[0] - 4, q[1], 7, 10, rs.uniform(1.2, 2.6), rot=rs.uniform(-0.8, 0.8))
        X = X + (3.0 * tube_height(np.clip(m_hem, 0, 1), 18.0) + crumple) * m_cap
        H = over(H, X, m_cap, r=6, lift=5, smooth_under=16.0)
        tc = [(262, 540), (236, 620), (232, 720), (252, 820), (282, 920)]
        m_tail = mask(band(tc, (78.0, 70.0), n=50))
        Xt = G(H, 10) + 6.0 + 9.0 * tube_height(m_tail, 78.0)
        Xt = Xt + cloth_folds(m_tail, [(P([(q[0] + o, q[1]) for q in tc]), 16.0, 3.4) for o in (-20, 2, 22)], [(P([(q[0] + o, q[1]) for q in tc]), 4.0, 2.2) for o in (-10, 12)])
        H = over(H, Xt, m_tail, r=6, lift=5)
        fog = [(540, 196), (530, 170), (500, 152), (450, 144), (396, 146), (346, 158), (308, 182), (292, 210), (340, 214), (460, 206)]
        flows = [[(530, 182), (496, 160), (440, 154), (380, 158), (330, 176), (304, 204)]]
        H, m_fog = _foggia_lobe(H, fog, flows, base=36.0, seed=37)
        Cl = [(552, 214), (510, 200), (450, 192), (390, 194), (334, 206), (296, 224)]       # tepede, siluetten taşmayan kısa halka
        H, m_roll = _roll(H, Cl, 64.0, base=42.0, amp=22.0, n_pl=10, slant=14.0)
        hm = np.maximum(np.maximum(m_roll, m_fog), m_cap)
    return H, hm


def fur_band(H, Cl, w, seed=41, base_add=4.0, amp=7.0, dens=0.6, tuft=(3.0, 5.5)):
    """Kürk (ermin) şerit: boru kesit + sık tutam benekleri (kısa, dağınık yönlü)."""
    tt = T()
    tt.line(P(Cl), w, 1.0)
    m_t = np.clip(tt.arr(), 0, 1)
    Xt = G(H, 8) + base_add + amp * tube_height(m_t, w)
    rs = np.random.RandomState(seed)
    fur = np.zeros_like(H)
    ys_, xs_ = np.nonzero(m_t[::4, ::4] > 0.5)
    for yy_, xx_ in zip(ys_, xs_):
        if rs.rand() < dens:
            bump(fur, xx_ * 4 + rs.uniform(-2, 2), yy_ * 4 + rs.uniform(-2, 2), rs.uniform(1.8, tuft[0]), rs.uniform(3.0, tuft[1]), rs.uniform(0.9, 2.0),
                 rot=rs.uniform(-0.9, 0.9))
    fur = fur - G(fur, 3.0) * 0.6
    return over(H, Xt + fur * m_t, m_t, r=5, lift=4), m_t


def hat_camauro(H, F, p):
    """Papalık camauro'su: bol kadife takke (kulakları ve enseyi örter) + kalın ermin kürk kenar."""
    cap = [(598, 248), (592, 204), (562, 160), (500, 128), (420, 116), (340, 126), (272, 160), (222, 222), (198, 302), (194, 392), (206, 470), (238, 520),
           (300, 540), (372, 538), (432, 512), (462, 462), (482, 400), (502, 340), (532, 296), (568, 268)]
    m_cap = mask(P(cap, True, 0.45))
    X = G(H, 18) + 11.0 + 9.0 * pillow(m_cap, 50)
    fr = [(P([(520, 150), (440, 200), (380, 290), (350, 400)]), 40.0, 3.0), (P([(420, 126), (330, 190), (270, 290), (250, 400)]), 46.0, 3.5),
          (P([(560, 200), (500, 240), (460, 300)]), 30.0, 2.0)]
    vl = [(P([(470, 140), (390, 200), (330, 300), (300, 420)]), 9.0, 2.2), (P([(560, 176), (480, 222), (420, 300)]), 7.0, 1.6)]
    X = X + cloth_folds(m_cap, fr, vl)
    H = over(H, X, m_cap, r=8, lift=5, smooth_under=16.0)
    Cl = [(606, 254), (574, 272), (536, 300), (506, 344), (486, 404), (466, 464), (436, 512), (380, 540), (310, 544), (250, 526), (208, 488)]
    H, m_t = fur_band(H, Cl, 84.0, seed=41, amp=9.0, dens=0.75, tuft=(3.4, 6.5))
    return H, np.maximum(m_cap, m_t)


def hat_tiara(H, F, p):
    """Üç taçlı papalık tiarası (arı kovanı) — üç belirgin taç bandı + yaprak süsleri, tepede küre ve haç, arkada iki infula."""
    base_y = 268.0
    top_y = 52.0
    prof = [(608, base_y + 6), (606, 214), (596, 160), (574, 112), (540, 76), (490, top_y + 6), (430, top_y), (372, top_y + 8), (322, 80), (282, 118),
            (252, 168), (234, 222), (226, base_y + 16), (320, base_y + 10), (440, base_y + 4), (540, base_y + 2)]
    m_t = mask(P(prof, True, 0.40))
    X = 40.0 + 24.0 * pillow(m_t, 70)
    rs = np.random.RandomState(51)
    yk_list = (base_y - 14, 178, 104)
    crowns = []
    fl = np.zeros_like(X)
    for k, yk in enumerate(yk_list):
        xl = {0: 230, 1: 248, 2: 300}[k]
        xr = {0: 606, 1: 600, 2: 566}[k]
        crowns.append((P([(xr, yk + 6), ((xl + xr) / 2, yk - 6), (xl, yk + 6)]), 26.0, 7.0))
        nfl = 6
        for j in range(nfl):
            u = (j + 0.5) / nfl
            fx = xr - (xr - xl) * u
            fy = yk - 6 - 8 * math.sin(math.pi * u) - 12
            bump(fl, fx, fy - 6, 7.0, 13.0, 6.0)                     # orta yaprak
            bump(fl, fx - 10, fy + 2, 5.0, 7.0, 4.0, rot=0.5)
            bump(fl, fx + 10, fy + 2, 5.0, 7.0, 4.0, rot=-0.5)
    X = X + ridges(crowns) + fl * m_t
    orb_c = (432, top_y - 16)
    orb = mask(P([(orb_c[0] + 20 * math.cos(a), orb_c[1] + 20 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 24, endpoint=False)], True, 0.5))
    X = np.maximum(X, (56.0 + 10.0 * pillow(orb, 8)) * orb)
    m_t = np.maximum(m_t, orb)
    cross = mask(band([(432, top_y - 34), (432, top_y - 74)], 9.0, 8), band([(414, top_y - 58), (450, top_y - 58)], 9.0, 8))
    X = np.maximum(X, 54.0 * cross)
    m_t = np.maximum(m_t, cross)
    for k, x0 in enumerate((246, 276)):
        tc = [(x0, base_y + 4), (x0 - 20, 380), (x0 - 26, 500), (x0 - 18 + 8 * k, 620)]
        m_i = mask(band(tc, 40.0, n=40))
        Xi = 36.0 + 7.0 * tube_height(m_i, 40.0) + 4 * k
        for j in range(3):
            q = cr(tc, 6)[1 + j]
            bump(Xi, q[0], q[1] + 40, 9, 9, 2.5)
        H = over(H, Xi, m_i, r=5, lift=4)
    H = over(H, X, m_t, r=7, lift=6)
    return H, m_t


def hat_hood(H, F, p):
    """Dominiken kukuletası (Savonarola; Fra Bartolomeo'nun profil portresindeki biçim): alnı kaşa dek örten, yanağı çerçeveleyen kalın yün;
    tepede geriye düşen sivri uç; omuzlarda pelerine (cappa) bağlanır."""
    hood = [(600, 312), (604, 270), (594, 222), (566, 172), (510, 134), (440, 116), (370, 112), (300, 98), (250, 82), (236, 120), (210, 190), (184, 260),
            (172, 350), (180, 450), (194, 530), (196, 600), (150, 650), (96, 720), (70, 820), (90, 900), (600, 900), (668, 846), (622, 796),
            (574, 766), (536, 718), (516, 656), (506, 586), (502, 506), (508, 436), (524, 380), (556, 334)]
    m_h = mask(P(hood, True, 0.40))
    X = 32.0 + 24.0 * pillow(m_h, 70)
    fr = [(P([(470, 128), (380, 160), (296, 236), (244, 340), (224, 460), (222, 580)]), 46.0, 6.0),
          (P([(540, 170), (470, 220), (406, 310), (370, 430), (356, 560), (360, 660)]), 40.0, 5.0),
          (P([(200, 640), (160, 720), (130, 840)]), 50.0, 6.0), (P([(320, 700), (300, 790), (300, 900)]), 46.0, 5.0),
          (P([(470, 740), (480, 820), (500, 900)]), 40.0, 4.0)]
    vl = [(P([(510, 146), (420, 196), (340, 284), (290, 400), (270, 520), (266, 620)]), 8.0, 5.0),
          (P([(250, 690), (220, 780), (206, 880)]), 8.0, 4.0), (P([(400, 720), (392, 810), (396, 900)]), 7.0, 3.5),
          (P([(200, 628), (300, 650), (420, 690), (520, 744)]), 7.0, 3.0)]
    X = X + cloth_folds(m_h, fr, vl)
    # kenar: yüzü çerçeveleyen kalın, kıvrık yün
    hem = [(606, 268), (600, 306), (562, 336), (528, 382), (510, 440), (504, 508), (506, 586), (516, 654), (536, 716), (572, 764), (618, 798)]
    m_hem = mask(band(hem, 34.0, n=70)) * m_h
    X = X + 8.0 * tube_height(np.clip(m_hem, 0, 1), 34.0)
    H = over(H, X, m_h, r=9, lift=6, smooth_under=18.0)
    return H, m_h


# ───────────────────────────── giysi ─────────────────────────────
def garment(H, F, p, kind="lucco"):
    """Büst üstü giysi: yaka bandı + kıvrımlar (+ kürk / brokar / cüppe şeridi)."""
    yb = F["yb"]
    nx = (p["neck"] - 1.0) * 34
    m_b = mask(P(F["bust"], True, 0.42))
    X = H.copy()
    rid, gro = [], []
    if kind in ("lucco", "fur", "brocade", "doublet"):
        # dik yaka: boyun tabanını saran bant
        col = [(598 + nx, yb - 22), (560, yb - 40), (490, yb - 60), (410, yb - 80), (330, yb - 104), (262 - nx, yb - 130)]
        m_col = mask(band(col, 34.0 if kind != "fur" else 54.0, n=60))
        Xc = G(H, 6) + 6.0 + (7.0 if kind != "fur" else 9.0) * tube_height(m_col, 34.0 if kind != "fur" else 54.0)
        if kind == "fur":
            rs = np.random.RandomState(71)
            fur = np.zeros_like(H)
            ys_, xs_ = np.nonzero(m_col[::5, ::5] > 0.5)
            for yy_, xx_ in zip(ys_, xs_):
                if rs.rand() < 0.6:
                    bump(fur, xx_ * 5 + rs.uniform(-2, 2), yy_ * 5 + rs.uniform(-2, 2), rs.uniform(2.0, 3.0), rs.uniform(3.5, 5.5), rs.uniform(0.9, 1.8), rot=rs.uniform(-0.6, 0.6))
            Xc = Xc + fur
        # omuz kütlesi (deltoid) + yakadan omza çekilen verev kıvrımlar + omuzdan sarkan uzun kıvrım; vadiler geniş ve sığ (çizgi değil)
        bump(X, 196, yb + 22, 96, 84, 6.5)
        rid += [(P([(300, yb - 96), (262, yb - 30), (236, yb + 60), (226, yb + 210)]), 54.0, 4.2),
                (P([(424, yb - 66), (384, yb + 10), (356, yb + 120), (348, yb + 260)]), 46.0, 3.4),
                (P([(526, yb - 40), (504, yb + 60), (498, yb + 200)]), 40.0, 2.6),
                (P([(606 + nx, yb + 4), (626, yb + 90), (634, yb + 220)]), 30.0, 2.8)]
        gro += [(P([(364, yb - 80), (324, yb - 6), (302, yb + 90), (294, yb + 230)]), 12.0, 2.0),
                (P([(474, yb - 52), (444, yb + 30), (428, yb + 160)]), 10.0, 1.6),
                (P([(578, yb - 4), (588, yb + 110), (592, yb + 240)]), 7.0, 2.4)]
        X = X + (ridges(rid) - grooves(gro)) * m_b
        if kind == "brocade":
            rs = np.random.RandomState(73)
            pat = np.zeros_like(H)
            for gy in range(int(yb - 10), 1000, 46):
                for gx in range(100 + (23 if (gy // 46) % 2 else 0), 680, 46):
                    bump(pat, gx, gy, 8.0, 10.0, 2.2)                                       # nar motifi: göbek + iki yaprak
                    bump(pat, gx - 9, gy - 9, 4.0, 6.0, 1.2, rot=0.6)
                    bump(pat, gx + 9, gy - 9, 4.0, 6.0, 1.2, rot=-0.6)
            X = X + pat * m_b
        H = X
        H = over(H, Xc, m_col, r=5, lift=4)
    elif kind == "cope":
        # papalık cüppesi (piviale): ön kenarda işlemeli şerit (orphrey) + göğüste mors (yuvarlak toka)
        orph = [(600 + nx, yb + 10), (560, yb + 60), (520, yb + 160), (500, yb + 260)]
        m_o = mask(band(orph, 56.0, n=40)) * m_b
        Xo = G(H, 6) + 5.0 + 4.0 * tube_height(np.clip(m_o, 0, 1), 56.0)
        for k in range(6):
            q = cr(orph, 6)[min(5, k)]
            bump(Xo, q[0], q[1], 9, 9, 3.0)
            bump(Xo, q[0], q[1], 4, 4, -1.4)
        for k in range(4):
            x0 = 180 + k * 70
            rid.append((P([(x0 + 40, yb - 50), (x0 + 6, yb + 80), (x0 - 10, yb + 220)]), 34.0, 5.0))
        H = H + ridges(rid) * m_b
        H = over(H, Xo, np.clip(m_o, 0, 1), r=4, lift=3)
        mx_, my_ = 566 + nx, yb + 40
        m_m = mask(P([(mx_ + 30 * math.cos(a), my_ + 30 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 24, endpoint=False)], True, 0.5))
        Xm = G(H, 4) + 6.0 + 6.0 * pillow(m_m, 10)
        bump(Xm, mx_, my_, 10, 10, 3.0)
        H = over(H, Xm, m_m, r=4, lift=4)
    elif kind == "habit":
        for k in range(4):
            x0 = 200 + k * 80
            rid.append((P([(x0 + 30, yb - 40), (x0, yb + 90), (x0 - 12, yb + 220)]), 40.0, 5.0))
            gro.append((P([(x0 + 70, yb - 30), (x0 + 44, yb + 100), (x0 + 36, yb + 230)]), 6.0, 3.0))
        H = H + (ridges(rid) - grooves(gro)) * m_b
    return H


PROFILES = {
    # Giovanni di Bicci (1360–1429): yaşlı, ince uzun yüz, sıkı dudak, çökük yanak; uzun cappuccio + becchetto
    "m_giovanni": dict(nose=17, hook=3, hump=2.5, brow=4, fore=1, nasion=5, lip=-1, lip2=0, lipt=0.6, chin=3, jaw=0.92, age=0.88, jowl=0.22,
                       neck=0.92, face_len=1.10, cheekbone=0.75, hollow=0.95, full=0.0, dbl=0.0, eye_deep=0.9, lids=0.8, adam=0.8, mouth_w=1.1,
                       hair="nape", hat="cappuccio_tall", garment="lucco", scale=0.90, dy=76, dx=16, born=1360, died=1429, age_range=(40.0, 69.0),
                       young=dict(age=0.32, hollow=0.40, jowl=0.05, lids=0.50, eye_deep=0.60, cheekbone=0.65)),
    # Cosimo (1389–1464): kartal burun, ince dudak, belirgin elmacık; alçak cappuccio, kürk yaka
    "m_cosimo": dict(nose=28, hook=11, hump=7, brow=4, fore=1, nasion=6, lip=-1, lip2=1, lipt=0.7, chin=2, jaw=0.98, age=0.85, jowl=0.18,
                     neck=0.98, face_len=1.03, cheekbone=1.0, hollow=0.8, full=0.0, dbl=0.0, eye_deep=0.8, lids=0.7, adam=0.7, mouth_w=1.0,
                     hair=None, hat="cappuccio_low", garment="fur", scale=0.97, dy=34, dx=-4, born=1389, died=1464, age_range=(40.0, 72.0),
                     young=dict(age=0.30, hollow=0.30, jowl=0.04, lids=0.45, eye_deep=0.55, full=0.12, cheekbone=0.85, neck=1.04)),
    # Lorenzo (1449–1492): basık geniş burun, öne çıkık alt çene, omuza dökülen düz saç + kâkül, güçlü boyun
    "m_lorenzo": dict(nose=13, hook=4, hump=-2.0, flat=1.3, alaw=1.65, tipr=1.55, brow=7, fore=0, nasion=9, lip=1, lip2=11, lipt=1.15, chin=23,
                      jaw=1.42, age=0.42, jowl=0.06, neck=1.34, face_len=1.07, cheekbone=0.85, hollow=0.45, full=0.05, eye_deep=0.95, lids=0.85, adam=1.4,
                      hair="long", hat=None, garment="lucco", scale=1.0, dy=20, dx=-8, born=1449, died=1492, age_range=(20.0, 38.0),
                      young=dict(age=0.14, hollow=0.25, eye_deep=0.65, lids=0.55, adam=1.1)),
    # Baldassarre Cossa / XXIII. Johannes (†1419): tıraşlı, dolgun yuvarlak yüz, gıdı; camauro + cüppe
    "m_cossa": dict(nose=11, hook=2, hump=1, tipr=1.45, alaw=1.2, brow=2, fore=2, nasion=3, lip=3, lip2=5, lipt=1.25, chin=3, jaw=1.15, age=0.55,
                    jowl=0.7, neck=1.3, face_len=1.0, cheekbone=0.15, hollow=0.0, full=1.0, dbl=1.0, eye_deep=0.4, lids=1.0, adam=0.2, mouth_w=0.9,
                    hair=None, hat="camauro", garment="cope", scale=0.98, dy=34, dx=-4),
    "m_cossa_tiara": dict(nose=11, hook=2, hump=1, tipr=1.45, alaw=1.2, brow=2, fore=2, nasion=3, lip=3, lip2=5, lipt=1.25, chin=3, jaw=1.15, age=0.55,
                          jowl=0.7, neck=1.3, face_len=1.0, cheekbone=0.15, hollow=0.0, full=1.0, dbl=1.0, eye_deep=0.4, lids=1.0, adam=0.2, mouth_w=0.9,
                          hair=None, hat="tiara", garment="cope", scale=0.84, dy=118, dx=24),
    # Piero di Cosimo "Gottoso" (1416–1469): dolgun yüz, kısa saç, kalın boyun; brokar giysi
    "c6_piero": dict(nose=14, hook=4, hump=2, tipr=1.2, brow=3, fore=2, nasion=4, lip=2, lip2=4, lipt=1.1, chin=4, jaw=1.12, age=0.55, jowl=0.5,
                     neck=1.25, face_len=0.98, cheekbone=0.3, hollow=0.0, full=0.8, dbl=0.7, eye_deep=0.5, lids=0.8, adam=0.3, mouth_w=0.95,
                     hair="short", hat=None, garment="brocade", scale=1.0, dy=22, dx=-4, born=1416, died=1469, age_range=(30.0, 53.0),
                     young=dict(age=0.22, jowl=0.22, full=0.5, dbl=0.3)),
    # Savonarola (1452–1498): çengel burun, dolgun dudak, çökük yanak, derin göz; Dominiken kukuletası
    "m_savonarola": dict(nose=36, hook=15, hump=10, tipr=1.15, alaw=1.15, brow=6, fore=0, nasion=8, lip=4, lip2=7, lipt=1.3, chin=8, jaw=1.12,
                         age=0.45, jowl=0.05, neck=1.0, face_len=1.04, cheekbone=0.95, hollow=1.0, full=0.0, eye_deep=1.0, lids=0.9, adam=0.8,
                         mouth_w=1.0, hair=None, hat="hood", garment="habit", scale=0.97, dy=30, dx=-20),
}


# ───────────────────────────── genel başlıklar / sakal / eski maske yedeği ─────────────────────────────
def hat_berretta(H, F, p, kind="cap"):
    """Yumuşak yuvarlak takke (berretta): başın üstünü örter, kulak üstünden geçen kıvrık kenar. kind: cap | skull | tall | biretta."""
    top = {"skull": 150, "tall": 92, "biretta": 108}.get(kind, 126)
    cap = [(596, 250), (598, 210), (578, 170), (536, top + 22), (470, top), (394, top + 2), (322, top + 20), (262, 196), (222, 250), (206, 310),
           (214, 350), (300, 330), (400, 314), (500, 290), (560, 270)]
    m_cap = mask(P(cap, True, 0.42))
    X = G(H, 16) + 9.0 + 10.0 * pillow(m_cap, 46)
    rs = np.random.RandomState(81)
    fr, vl = [], []
    for k in range(5):
        x0 = 300 + k * 60
        fr.append((P([(x0 + 10, top + 16), (x0 - 6, (top + 300) / 2), (x0 - 20, 300 - k * 8)]), 30.0, 3.0))
        vl.append((P([(x0 + 38, top + 20), (x0 + 22, (top + 300) / 2), (x0 + 10, 296 - k * 8)]), 6.0, 2.0))
    if kind == "biretta":
        for k in range(3):
            x0 = 330 + k * 100
            fr.append((P([(x0, top - 14), (x0 + 6, top + 40)]), 18.0, 9.0))
    X = X + cloth_folds(m_cap, fr, vl)
    H = over(H, X, m_cap, r=7, lift=5, smooth_under=14.0)
    if kind not in ("skull",):
        Cl = [(604, 250), (560, 274), (500, 292), (420, 312), (330, 328), (246, 334), (204, 316)]
        tt = T()
        tt.line(P(Cl), 30.0, 1.0)
        m_b = np.clip(tt.arr(), 0, 1)
        Xb = G(H, 8) + 4.0 + 9.0 * tube_height(m_b, 30.0)
        H = over(H, Xb, m_b, r=5, lift=4)
        m_cap = np.maximum(m_cap, m_b)
    return H, m_cap


def hat_beret(H, F, p):
    """Yassı geniş bere (Rönesans): kafanın üstünde yana taşan disk, ışınsal pli."""
    pts = [(650, 236), (640, 196), (600, 160), (530, 134), (440, 124), (350, 130), (270, 152), (210, 186), (184, 226), (198, 256), (280, 262), (380, 258),
           (480, 252), (580, 252)]
    m_b = mask(P(pts, True, 0.42))
    X = 44.0 + 12.0 * pillow(m_b, 30)
    fr, vl = [], []
    for k in range(9):
        x0 = 220 + k * 50
        fr.append((P([(x0, 150 + abs(k - 4) * 3), (x0 + 10, 248)]), 26.0, 3.2))
        vl.append((P([(x0 + 24, 150 + abs(k - 4) * 3), (x0 + 32, 248)]), 5.0, 2.4))
    X = X + cloth_folds(m_b, fr, vl)
    H = over(H, X, m_b, r=7, lift=6)
    return H, m_b


def hat_turban(H, F, p, big=True):
    """Sarık: başı saran iri yuvarlak kütle; verev sarım bantları + tepede kavuk."""
    sc = 1.0 if big else 0.86
    cx, cy = 420.0, 220.0
    pts = [(cx + 196 * sc, cy + 70), (cx + 206 * sc, cy - 20), (cx + 170 * sc, cy - 110 * sc), (cx + 90 * sc, cy - 160 * sc), (cx, cy - 172 * sc),
           (cx - 100 * sc, cy - 160 * sc), (cx - 180 * sc, cy - 110 * sc), (cx - 226 * sc, cy - 20), (cx - 220 * sc, cy + 80), (cx - 160 * sc, cy + 130),
           (cx, cy + 116), (cx + 120 * sc, cy + 100)]
    m_t = mask(P(pts, True, 0.45))
    X = 40.0 + 22.0 * pillow(m_t, 70)
    rid, gro = [], []
    for k in range(7):
        y0 = cy + 110 - k * 40 * sc
        rid.append((P([(cx - 230 * sc, y0 + 40), (cx - 40, y0 - 20), (cx + 210 * sc, y0 - 40)]), 34.0 * sc, 6.0))
        gro.append((P([(cx - 230 * sc, y0 + 60), (cx - 40, y0), (cx + 210 * sc, y0 - 20)]), 6.0, 4.0))
    X = X + cloth_folds(m_t, rid, gro)
    top = mask(P([(cx + 40, cy - 150 * sc), (cx + 50, cy - 200 * sc), (cx, cy - 214 * sc), (cx - 50, cy - 200 * sc), (cx - 40, cy - 150 * sc)], True, 0.5))
    X = np.maximum(X, (54.0 + 8.0 * pillow(top, 14)) * top)
    m_t = np.maximum(m_t, top)
    H = over(H, X, m_t, r=8, lift=6, smooth_under=16.0)
    return H, m_t


def legacy_mask_layer(H, d, what, base_add=8.0, amp=10.0, detail=18.0):
    """Eski (medal.py / medal_extra) başlık·sakal çizimini MASKE + ayrıntı olarak kullan; v3 kumaş/kıl gölgelemesi."""
    cv = medal._Canvas()
    fn = None
    name = d.get(what)
    if what == "hat":
        try:
            import medal_extra as ME
            fn = ME.HAT.get(name)
        except Exception:
            fn = None
        fn = fn or medal._hat
    elif what == "beard":
        try:
            import medal_extra as ME
            fn = ME.BEARD.get(name)
        except Exception:
            fn = None
        fn = fn or medal._beard
    try:
        fn(cv, d)
    except Exception:
        return H, np.zeros_like(H)
    a = cv.arr()
    m = np.clip((a > 0.04).astype(np.float32), 0, 1)
    if m.sum() < 50:
        return H, m
    det = (a - G(a, 6.0)) * detail
    X = G(H, 12) + base_add + amp * pillow(m, 24) + det * m
    return over(H, X, m, r=5, lift=4), m


def beard_layer(H, F, p, d):
    """Sakal/bıyık: eski çizimin maskesi + aşağı akan kısa tutamlar."""
    cv = medal._Canvas()
    try:
        import medal_extra as ME
        fn = ME.BEARD.get(d.get("beard")) or medal._beard
    except Exception:
        fn = medal._beard
    try:
        fn(cv, d)
    except Exception:
        return H
    m = (cv.arr() > 0.04).astype(np.float32)
    if m.sum() < 50:
        return H
    rs = np.random.RandomState(91)
    ys_, xs_ = np.nonzero(m[::14, ::14] > 0.5)
    locks = []
    for y, x in sorted(zip(ys_, xs_)):
        x0, y0 = x * 14 + rs.uniform(-5, 5), y * 14 + rs.uniform(-5, 5)
        L_ = rs.uniform(26, 40)
        locks.append(([(x0, y0), (x0 + rs.uniform(-4, 4), y0 + L_ * 0.5), (x0 + rs.uniform(-8, 4), y0 + L_)], rs.uniform(14, 20)))
    R_, _ = lock_layers2(locks, seed=93, amp=3.5, crest=2.0, fine=1)
    m2 = np.clip(G(m, 1.2) * 1.1, 0, 1)
    X = G(H, 10) + 5.0 + 3.0 * pillow(m2, 20) + R_ * m2
    return over(H, X, m2, r=4, lift=3)


HAIR_MAP = {"long": "long", "long_wave": "long", "long_flow": "long", "bob": "long", "wavy": "long",
            "short": "short", "crop": "short", "child": "short", "sides": "short", "thin_back": "short", "inca": "short", "nape": "nape",
            "bowl": "bowl", "thin": "thin", "monk": "tonsure", "tonsure": "tonsure"}
HAT_MAP = {"cap": "berretta", "cap_black": "skull", "skull": "skull", "cap_gold": "berretta", "merchant_cap": "tall", "barrete": "berretta",
           "biretta": "biretta", "child_cap": "skull", "plain_coif": "skull", "kalot": "skull",
           "flatcap": "beret", "beret_f": "beret", "flatcap_x": "beret", "beret_wide": "beret", "feather_beret": "beret", "beret_feathers": "beret",
           "burg_bonnet": "beret", "toque_brim": "beret", "seaman_cap": "beret",
           "camauro": "camauro", "camauro_x": "camauro", "turban_big": "turban", "turban_x": "turban", "turban_small": "turban_s", "turban_small_x": "turban_s",
           "cappuccio_tall": "cappuccio_tall", "cappuccio_low": "cappuccio_low", "tiara": "tiara", "hood": "hood"}
GARMENT_MAP = {"robe": "lucco", "robe_white": "habit", "fur_gown_merchant": "fur", "academic_robe": "lucco", "dark_robe": "lucco", "lawyer_robe": "lucco",
               "mantle_brooch": "lucco", "cloak_buttons": "lucco", "fur_doublet": "fur", "fur_robe": "fur", "fur_gown_wide": "fur", "fur_jacket": "fur",
               "gown_fur": "fur", "fleece": "fur", "doublet": "lucco", "dark_doublet": "lucco", "courtly_jacket": "lucco", "explorer_doublet": "lucco",
               "leather_jerkin": "lucco", "child_doublet": "lucco", "ruff_black": "lucco", "cassock": "habit", "cassock_x": "habit", "monk_habit": "habit",
               "habit": "habit", "kaftan": "lucco", "dolama": "lucco", "tilmatli": "lucco", "tunic_inca": "lucco", "armor": "lucco", "armor_x": "lucco",
               "brocade": "brocade", "cope": "cope", "lucco": "lucco", "fur": "fur"}
FEMALE_HATS = {"widow_hood", "gable_hood", "jeweled_net", "gold_haube", "hennin", "castilian_veil", "french_hood", "toca", "widow_wimple"}
FEMALE_GARM = {"mourning_f", "gown_f", "jeweled_gown", "dark_gown_collar", "dark_gown_plain", "black_dress", "gown_fur"}


def is_v3(d):
    if d is None:
        return False
    if d.get("hair") == "veil" or d.get("hat") in FEMALE_HATS or d.get("garment") in FEMALE_GARM or d.get("lash"):
        return False
    return True


def params_for(key, d, age=None):
    """Kişi parametreleri: PROFILES (özel) ya da medal.PEOPLE kaydından türetilmiş genel v3 yüz. age: yıl cinsinden (None → kişinin kanonik yaşı)."""
    if key in PROFILES:
        p = merged(PROFILES[key])
    else:
        p = merged({})
        for k_ in ("nose", "hook", "brow", "lip", "lip2", "chin", "jaw", "fore", "age", "jowl", "neck"):
            if k_ in d:
                p[k_] = d[k_]
        p["hump"] = max(0.0, d.get("hook", 2) * 0.6)
        p["cheekbone"] = 0.4 + 0.5 * d.get("cheek", 0.0)
        p["full"] = 0.6 * d.get("puff", 0.0) + (0.5 if d.get("jowl", 0) > 0.4 else 0.0)
        p["hollow"] = 0.2 + 0.5 * max(0.0, d.get("age", 0.3) - 0.4)
        p["dbl"] = 0.6 if d.get("jowl", 0) > 0.5 else 0.0
        p["hair"] = HAIR_MAP.get(d.get("hair"), None if d.get("hair") in (None, "none") else "short")
        hat = d.get("hat")
        p["hat"] = HAT_MAP.get(hat, None if hat in (None, "none") else "legacy")
        p["beard"] = d.get("beard")
        p["must"] = d.get("must")
        p["garment"] = GARMENT_MAP.get(d.get("garment"), "lucco")
        if p["hat"] in ("turban", "turban_s"):
            p["scale"], p["dy"] = 0.90, 70.0
        elif p["hat"] in ("beret", "tall", "biretta", "legacy"):
            p["scale"], p["dy"] = 0.96, 34.0
        elif p["hat"] is not None:
            p["scale"], p["dy"] = 0.98, 26.0
        else:
            p["scale"], p["dy"] = 1.0, 20.0
        p["_legacy"] = d
    if age is not None and "young" in p:
        a0, a1 = p.get("age_range", (40.0, 70.0))          # (genç sürüm yaşı, kanonik yaş) arası doğrusal
        t = float(np.clip((age - a0) / (a1 - a0), 0.0, 1.0))
        y = p["young"]
        for k_, v in y.items():
            p[k_] = v + (p[k_] - v) * t
    return p


def portrait_any(p):
    """Genel v3 portre: gövde → giysi → saç → sakal → başlık."""
    H, F, Ms = portrait_base(p)
    H = garment(H, F, p, p.get("garment") or "lucco")
    hair = p.get("hair")
    hat = p.get("hat")
    if hair == "long":
        H, _ = hair_layer(H, locks_lorenzo(F, p), thick=4.0, amp=7.0, seed=5, fine=1)
    elif hair in ("short", "nape", "bowl", "thin"):
        kind = {"nape": "short"}.get(hair, hair)
        H, _ = short_hair(H, F, p, thick=5.0 if hair != "nape" else 3.5, amp=4.2 if hair != "nape" else 3.0, kind=kind)
    elif hair == "tonsure":
        m_c = mask(P([(WHORL[0] + 120 * math.cos(a), WHORL[1] + 10 + 70 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 20, endpoint=False)], True, 0.5))
        H0 = H.copy()
        H, mh = short_hair(H, F, p, thick=5.0, amp=4.0, kind="short")
        H = H * (1 - m_c) + H0 * m_c
    lg = p.get("_legacy") or {}
    if lg.get("beard") or lg.get("must"):
        H = beard_layer(H, F, p, lg)
    if hat == "cappuccio_tall":
        H, _ = hat_cappuccio(H, F, p, "tall")
    elif hat == "cappuccio_low":
        H, _ = hat_cappuccio(H, F, p, "low")
    elif hat == "camauro":
        H, _ = hat_camauro(H, F, p)
    elif hat == "tiara":
        H, _ = hat_tiara(H, F, p)
    elif hat == "hood":
        H, _ = hat_hood(H, F, p)
    elif hat in ("berretta", "skull", "tall", "biretta"):
        H, _ = hat_berretta(H, F, p, {"berretta": "cap"}.get(hat, hat))
    elif hat == "beret":
        H, _ = hat_beret(H, F, p)
    elif hat in ("turban", "turban_s"):
        H, _ = hat_turban(H, F, p, big=hat == "turban")
    elif hat == "legacy":
        H, _ = legacy_mask_layer(H, lg, "hat")
    return H, F, None


# ═════════════════════════════ API ═════════════════════════════
@functools.lru_cache(maxsize=16)
def _v3_rgba(key, metal="bronze", inscription=None, flip=False, age=None, ver=MEDAL_VER):
    """v3 madalya (S×S RGBA uint8) ya da None (kadın/örtülü profil → eski üreteç)."""
    d = medal.PEOPLE.get(key) or medal.PEOPLE["_anon"]           # bilinmeyen anahtar → genel v3 erkek yüz (eski: v1 _anon)
    pk = PROFILE_ALIAS.get(key, key)
    if pk not in PROFILES and not is_v3(d):
        return None
    if age is None and key in AGE_FIXED:
        age = AGE_FIXED[key]
    p = params_for(pk, d or {}, age)
    seed = zlib.crc32(key.encode("utf-8")) % 997
    Hp, F, _ = portrait_any(p)
    Hb, alpha = body_height(inscription, seed=seed)
    Hm = to_medal(Hp, p, flip)
    rgba = shade(Hb + Hm, alpha, metal if metal in METALS else "bronze", seed=seed + 6)
    return (np.clip(rgba, 0, 1) * 255 + 0.5).astype(np.uint8)


def resolve_age(key, age=None):
    """Madalyadaki yaş: açık `age` > sabit yaşlı anahtar (m_cosimo_genc) > AUTO_AGE (çekim yılı − doğum, ölümden sonra ölüm yaşı; 15–95 dışında
    ya da doğumdan önce yok; 5 yıla yuvarlı) > None (kanonik yaş)."""
    if age is not None:
        return float(age)
    if key in AGE_FIXED:
        return AGE_FIXED[key]
    pr = PROFILES.get(PROFILE_ALIAS.get(key, key))
    if not AUTO_AGE or not pr or "born" not in pr or "young" not in pr:
        return None
    y = DN.year()
    if y is None:
        return None
    a = min(y, pr.get("died", y)) - pr["born"]            # ölümden sonraki yıllarda: ölüm yaşı
    if a < 15 or a > 95:
        return None
    return float(int(round(a / 5.0) * 5))


def feature_point(key, which="nose", flip=False, age=None):
    """Yüz öğesinin madalya merkezine göre konumu, madalya ÇAPI biriminde (dx, dy) — sahnelerde kalibre işaretler için
    (ekranda: x + dx * size, y + dy * size). which: nose | chin | eye | mouth | ear. v3 dışı anahtar → None."""
    d = medal.PEOPLE.get(key)
    pk = PROFILE_ALIAS.get(key, key)
    if not V3 or (pk not in PROFILES and not is_v3(d)):
        return None
    p = params_for(pk, d or {}, age)
    F = head_geom(p)
    q = {"nose": F["tip"], "chin": F["pog"], "eye": F["eye"], "mouth": F["sto"], "ear": F["ear_c"]}[which]
    M = frame_mtx(p)
    mx = M[0, 0] * q[0] + M[0, 2]
    my = M[1, 1] * q[1] + M[1, 2]
    dx = (mx - S / 2) / S
    return (-dx if flip else dx), (my - S / 2) / S


@functools.lru_cache(maxsize=12)
def _v3_legacy_rgba(key, metal="bronze", inscription=None, flip=False, ver=MEDAL_VER):
    """Kadın/örtülü profiller: ESKİ portre çizimi (medal.py; `_x` anahtarlarında medal_extra'nın genişletilmiş hattı — fileli başlık, kolye…)
    yükseklik olarak alınır, v3 madalya gövdesi + malzemesiyle gölgelenir (yan yana duran madalyalar aynı bronz; eski v2 yolu `_x` başlığını
    çizemiyor, örn. Simonetta kel erkek başı gibi çıkıyordu)."""
    try:
        import medal_extra  # noqa: F401  (yan etki: medal.portrait_height `_x` anahtarları için genişletilir)
    except Exception:
        pass
    d = medal.PEOPLE.get(key) or medal.PEOPLE["_anon"]
    por = medal.portrait_height(key, flip)
    sc, dy = d.get("scale", 1.22), d.get("dy", 0)
    M = np.float32([[sc, 0, S / 2 - 520 * sc + 85], [0, sc, S / 2 - 470 * sc + 20 + dy]])
    if flip:
        M[0, 2] = S / 2 - 480 * sc - 85
    por = cv2.warpAffine(por, M, (S, S), flags=cv2.INTER_LINEAR, borderValue=0)
    Hp = G(por, 1.3) * 60.0 + G(por, 10.0) * 14.0 * (por > 0.02)
    Hm = Hp * smoothstep(398.0, 384.0, RR)
    seed = zlib.crc32(key.encode("utf-8")) % 997
    Hb, alpha = body_height(inscription, seed=seed)
    rgba = shade(Hb + Hm, alpha, metal if metal in METALS else "bronze", seed=seed + 6)
    return (np.clip(rgba, 0, 1) * 255 + 0.5).astype(np.uint8)


@functools.lru_cache(maxsize=32)
def medal_array_b(key, metal="bronze", inscription=None, flip=False, size=720, age=None):
    """RGBA uint8 (size²): dökme bronz + patina. v3 (varsayılan) ya da eski v2/v1 + patina sonrası işlemi."""
    arr = None
    if V3:
        arr = _v3_rgba(key, metal, inscription, flip, age)
        if arr is None:
            arr = _v3_legacy_rgba(key, metal, inscription, flip)
    if arr is None:
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
        arr = np.dstack([np.clip(rgb, 0, 255), a]).astype(np.uint8)
    out = arr
    if size != out.shape[0]:
        out = cv2.resize(out, (size, size), interpolation=cv2.INTER_AREA)
    return out


@functools.lru_cache(maxsize=32)
def medal_img(key, metal="bronze", inscription=None, flip=False, size=720, age=None):
    return sk.np_to_image(medal_array_b(key, metal, inscription, flip, size, age))


@functools.lru_cache(maxsize=32)
def medal_shadow(key, metal="bronze", inscription=None, flip=False, size=720, age=None):
    return CM.blur_sil(medal_array_b(key, metal, inscription, flip, size, age)[..., 3], 16.0, (14, 8, 2))


def draw_temsili(f, x, y, size, alpha=1.0, text=STAMP_TEXT):
    """Madalyanın ALTINA küçük, okunur "TEMSİLÎ" levhası (koyu zemin, ince yaldız çerçeve, krem Cinzel ≥30 px; kontrast ≥7:1).
    Kenar yazıtıyla çakışmaz (diskin dışında); ekran uzayında güvenli alana / altyazı bandının üstüne / HUD dışına kıstırılır."""
    a = clamp(alpha)
    if a <= 0.02:
        return
    fs = clamp(size * 0.066, 30.0, 46.0)
    tr = fs * 0.20
    tw = sk.text_width(text, "title_m", fs, tr)
    pad = fs * 0.62
    w, h = tw + 2 * pad, fs * 1.05 + 2 * pad * 0.55
    # yer: diskin alt kenarında, EKRAN MERKEZİNE bakan yanda (gece çekiminde mum havuzu ekran ortasında: kenara düşen damga kararır).
    # Levha, diskten `gap` kadar dışarıda kalacak en küçük uzaklıkta (kenar yazıtıyla çakışmaz).
    M = f.c.getTotalMatrix()
    sxm = M.mapXY(x, y).x() / max(1e-6, CM._frame_scale(f)[0])
    th = math.radians(STAMP_ANGLE if sxm <= sk.W * 0.5 + 0.02 * size else 180.0 - STAMP_ANGLE)
    ux, uy = math.cos(th), math.sin(th)
    R_ = 0.484 * size + max(8.0, 0.02 * size)
    d = R_
    for _ in range(120):
        cxs, cys = x + ux * d, y + uy * d
        qx = min(max(x, cxs - w / 2), cxs + w / 2)
        qy = min(max(y, cys - h / 2), cys + h / 2)
        if math.hypot(qx - x, qy - y) >= R_:
            break
        d += 4.0
    cx_, cy = x + ux * d, y + uy * d
    x0, y0 = cx_ - w / 2, cy - h / 2
    x = cx_
    dx, dy, k, _info = CM.screen_fit(f, x0, y0, x0 + w, y0 + h, safe=STAMP_SAFE)
    c = f.c
    c.save()
    if dx or dy:
        c.translate(dx, dy)
    if k < 0.999:
        c.translate(x, cy)
        c.scale(k, k)
        c.translate(-x, -cy)
    f.rrect(x0, y0, w, h, 10, color="#120C08", alpha=0.86 * a)
    f.rrect(x0, y0, w, h, 10, style="stroke", sw=2.0, color="#C9A45A", alpha=0.85 * a)
    CM.ink(f, text, x, cy + fs * 0.36, face="title_m", size=fs, color="#FFFFFF", align="c", track=tr, alpha=a, emboss=False, scrim=False)
    c.restore()


def draw_medal_b(f, key, x, y, size, metal="bronze", flip=False, alpha=1.0, tilt=0.0, glint=None, inscription=True, shadow=0.6, age=None, stamp=None):
    """Madalya merkezi (x,y); tilt: -1..1 (dikey eksen); glint: 0..1 yatay parlama bandı.
    Kenar yazısı dönem kuralından geçer (donem.medal_inscription: 'PATER PATRIAE' yalnız ≥1464).
    age: yaş (None → resolve_age: AUTO_AGE ile çekim yılından ya da kanonik). stamp: None → yıl < 1438 ise otomatik TEMSİLÎ (KA1-V9) |
    False → yok | True/metin → zorla."""
    ins = medal.INSCR.get(key) if inscription else None
    st = stamp
    if st is None:
        st = bool(STAMP_AUTO and DN.portrait_medal_is_anachronistic())
    if ins:
        ins0 = ins
        ins = DN.medal_inscription(ins)
        DN.note_once_per_frame("medal", key=key, text=ins, req=ins0, stamp=bool(st))
    ag = resolve_age(key, age) if V3 else None
    img = medal_img(key, metal, ins, flip, 720, ag)
    s = size / 720.0
    cs = max(0.05, math.cos(tilt * 0.55))
    c = f.c
    if shadow > 0:
        c.save(); c.translate(x + size * 0.035, y + size * 0.055); c.scale(s * cs, s)
        p = skia.Paint(AntiAlias=True); p.setAlphaf(clamp(shadow * alpha))
        c.drawImage(medal_shadow(key, metal, ins, flip, 720, ag), -360, -360, CM._LIN, p)
        c.restore()
    c.save(); c.translate(x, y); c.scale(s * cs, s)
    p = skia.Paint(AntiAlias=True); p.setAlphaf(clamp(alpha))
    c.drawImage(img, -360, -360, CM._LIN, p)
    if glint is not None:
        # yumuşak kenarlı eğik parlama, madalya alfasıyla maskeli (eski sürüm sert kenarlı şerit + çift çizim → dikdörtgen artefakt; SA1-E4)
        gx = -520 + 1040 * glint
        CM.soft_glint(c, img, -360, -360, (max(-380.0, gx - 200), -380, min(380.0, gx + 200), 380), gx, 150, alpha, "#FFE6B0", 110)
    c.restore()
    if st:
        txt = st if isinstance(st, str) else STAMP_TEXT
        draw_temsili(f, x, y, size, alpha, txt)
        DN.note_once_per_frame("medal_stamp", key=key, text=txt)
