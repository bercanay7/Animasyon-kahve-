"""Rönesans madalya portreleri: parametrik profil kafa → yükseklik haritası → kabartmalı metal (altın/bronz/gümüş).

Kullanım:
    spr = medal_image("karl_genc", metal="gold", size=640)   # skia.Image (RGBA), önbellekli
    f.image(spr, x, y, sx, ax=.5, ay=.5)
`PEOPLE` kayıtları: yüz çizgileri (burun/dudak/çene/alın) + saç/başlık/sakal/giysi parametreleri.
Hepsi YAKLAŞIK/üslup çalışmasıdır; fotogerçekçi benzerlik iddiası yok (tarihî portrelerdeki ayırt edici özelliklerden esinli).
"""
import math
import os
from functools import lru_cache

import cv2
import numpy as np
import skia

import sk
from sk import C, np_to_image

S = 1000                      # çalışma tuvali
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "_cache")


# ───────────────────────────── kişiler ─────────────────────────────
# yüz parametreleri: nose (burun uzunluğu dx), hook (kanca eğimi), brow, lip (üst dudak), lip2 (alt dudak), chin (çene öne çıkıklığı),
# jaw (çene kalınlığı), fore (alın eğimi), age (0..1 kırışıklık), jowl (yanak sarkması), neck (boyun kalınlığı)
PEOPLE = {
    # Charles V — genç: sakalsız, düz küt saç, yassı bere; Habsburg çenesi, kalın alt dudak
    "karl_genc": dict(nose=10, hook=6, brow=4, lip=3, lip2=10, chin=26, jaw=1.0, fore=0, age=0.0, jowl=0.0, neck=1.0,
                      hair="bob", hat="flatcap", beard=None, garment="fleece", mouth_open=0.35, hair_c=0.0),
    "karl_olgun": dict(nose=12, hook=8, brow=5, lip=3, lip2=11, chin=30, jaw=1.05, fore=0, age=0.45, jowl=0.1, neck=1.05,
                       hair="short", hat="cap", beard="short", garment="fleece", mouth_open=0.3),
    "karl_yasli": dict(nose=13, hook=9, brow=5, lip=2, lip2=12, chin=32, jaw=1.0, fore=-2, age=0.9, jowl=0.35, neck=0.95,
                       hair="thin", hat="skull", beard="full", garment="mourning", mouth_open=0.4),
    "fransuva": dict(nose=34, hook=-6, brow=4, lip=4, lip2=5, chin=2, jaw=1.05, fore=2, age=0.2, jowl=0.1, neck=1.0,
                     hair="long", hat="beret_f", beard="goatee", garment="fur_doublet", mouth_open=0.0),
    "henri8": dict(nose=2, hook=0, brow=2, lip=-4, lip2=-2, chin=-4, jaw=1.5, fore=4, age=0.3, jowl=0.6, neck=1.5,
                   hair="short", hat="beret_f", beard="short", garment="fur_doublet", mouth_open=0.0),
    "luther": dict(nose=8, hook=2, brow=3, lip=2, lip2=4, chin=0, jaw=1.4, fore=3, age=0.35, jowl=0.7, neck=1.4,
                   hair="monk", hat="cap_black", beard=None, garment="robe_white", mouth_open=0.0),
    "melanchthon": dict(nose=8, hook=3, brow=3, lip=1, lip2=2, chin=-2, jaw=0.9, fore=3, age=0.4, jowl=0.1, neck=0.9,
                        hair="long", hat="cap_black", beard="short", garment="robe", mouth_open=0.0),
    "suleyman": dict(nose=18, hook=-8, brow=4, lip=2, lip2=2, chin=-2, jaw=0.95, fore=0, age=0.2, jowl=0.0, neck=1.0,
                     hair="none", hat="turban_big", beard="mustache", garment="kaftan", mouth_open=0.0, scale=0.98, dy=120),
    "barbaros": dict(nose=16, hook=-4, brow=5, lip=3, lip2=3, chin=4, jaw=1.1, fore=0, age=0.5, jowl=0.1, neck=1.1,
                     hair="none", hat="turban_small", beard="long_pointed", garment="kaftan", mouth_open=0.0, scale=1.1, dy=70),
    "fugger": dict(nose=16, hook=4, brow=3, lip=1, lip2=2, chin=2, jaw=0.9, fore=2, age=0.5, jowl=0.1, neck=0.95,
                   hair="long", hat="cap_gold", beard=None, garment="fur_robe", mouth_open=0.0),
    "klemens": dict(nose=14, hook=5, brow=4, lip=2, lip2=3, chin=0, jaw=1.0, fore=2, age=0.6, jowl=0.2, neck=1.0,
                    hair="none", hat="camauro", beard="long", garment="cassock", mouth_open=0.0),
    "felipe2": dict(nose=10, hook=5, brow=3, lip=3, lip2=9, chin=22, jaw=0.95, fore=2, age=0.1, jowl=0.0, neck=1.0,
                    hair="short", hat="cap", beard="pointed", garment="ruff_black", mouth_open=0.25),
    "juana": dict(nose=10, hook=2, brow=2, lip=2, lip2=6, chin=14, jaw=0.9, fore=2, age=0.4, jowl=0.0, neck=0.9,
                  hair="veil", hat="widow_hood", beard=None, garment="mourning_f", mouth_open=0.0),
    "isabel": dict(nose=8, hook=0, brow=1, lip=2, lip2=4, chin=8, jaw=0.8, fore=3, age=0.0, jowl=0.0, neck=0.85,
                   hair="veil", hat="gable_hood", beard=None, garment="gown_f", mouth_open=0.0),
    "ferdinand": dict(nose=12, hook=5, brow=4, lip=2, lip2=8, chin=18, jaw=1.0, fore=0, age=0.2, jowl=0.05, neck=1.0,
                      hair="long", hat="flatcap", beard=None, garment="fur_doublet", mouth_open=0.2),
    "maksimilyan": dict(nose=28, hook=10, brow=5, lip=2, lip2=5, chin=12, jaw=0.95, fore=0, age=0.55, jowl=0.1, neck=1.0,
                        hair="long", hat="flatcap", beard=None, garment="fleece", mouth_open=0.0),
    "kortes": dict(nose=10, hook=2, brow=4, lip=2, lip2=3, chin=4, jaw=1.1, fore=0, age=0.3, jowl=0.05, neck=1.1,
                   hair="short", hat="cap", beard="full", garment="doublet", mouth_open=0.0),
    "pizarro": dict(nose=12, hook=4, brow=6, lip=1, lip2=2, chin=2, jaw=1.15, fore=-2, age=0.6, jowl=0.1, neck=1.15,
                    hair="none", hat="morion", beard="long", garment="armor", mouth_open=0.0, scale=1.1, dy=50),
    "lascasas": dict(nose=9, hook=3, brow=3, lip=1, lip2=2, chin=0, jaw=0.9, fore=3, age=0.7, jowl=0.05, neck=0.9,
                     hair="monk", hat="none", beard="short", garment="robe_white", mouth_open=0.0),
    "moritz": dict(nose=14, hook=2, brow=3, lip=2, lip2=3, chin=2, jaw=1.0, fore=0, age=0.1, jowl=0.0, neck=1.0,
                   hair="long", hat="beret_f", beard="short", garment="armor", mouth_open=0.0),
    "orange": dict(nose=12, hook=2, brow=3, lip=2, lip2=3, chin=2, jaw=0.9, fore=2, age=0.0, jowl=0.0, neck=0.95,
                   hair="long", hat="beret_f", beard="short", garment="fur_doublet", mouth_open=0.0),
    "margareta": dict(nose=10, hook=2, brow=2, lip=2, lip2=7, chin=14, jaw=0.9, fore=2, age=0.35, jowl=0.0, neck=0.9,
                      hair="veil", hat="widow_hood", beard=None, garment="mourning_f", mouth_open=0.0),
    "tiziano": dict(nose=12, hook=2, brow=3, lip=1, lip2=2, chin=0, jaw=0.9, fore=2, age=0.7, jowl=0.05, neck=0.9,
                    hair="thin", hat="cap_black", beard="long", garment="robe", mouth_open=0.0),
    "durer": dict(nose=12, hook=2, brow=3, lip=1, lip2=2, chin=0, jaw=0.9, fore=2, age=0.3, jowl=0.0, neck=0.95,
                  hair="long_wave", hat="none", beard="short", garment="fur_robe", mouth_open=0.0),
    "elkano": dict(nose=12, hook=2, brow=4, lip=2, lip2=3, chin=2, jaw=1.1, fore=0, age=0.3, jowl=0.05, neck=1.1,
                   hair="short", hat="cap", beard="short", garment="doublet", mouth_open=0.0),
    "makedonya": dict(nose=10, hook=0, brow=3, lip=2, lip2=3, chin=0, jaw=1.0, fore=2, age=0.2, jowl=0.0, neck=1.0,
                      hair="short", hat="none", beard=None, garment="doublet", mouth_open=0.0),
}


# ───────────────────────────── yardımcılar ─────────────────────────────
def _sp(pts, close=False, t=0.5):
    return sk.smooth_path(pts, close=close, tension=t)


def _pp(points, close=True):
    return sk.poly_path(points, close)


class _Canvas:
    def __init__(self):
        self.s = skia.Surface(S, S)
        self.c = self.s.getCanvas()
        self.c.clear(skia.ColorBLACK)

    def fill(self, path, g, blur=0.0, aa=True):
        p = skia.Paint(AntiAlias=aa, Color=skia.Color(int(g), int(g), int(g), 255))
        if blur > 0:
            p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
        self.c.drawPath(path, p)

    def stroke(self, path, g, w, blur=0.0, cap="round"):
        p = skia.Paint(AntiAlias=True, Color=skia.Color(int(g), int(g), int(g), 255), Style=skia.Paint.kStroke_Style, StrokeWidth=w)
        p.setStrokeCap(skia.Paint.kRound_Cap if cap == "round" else skia.Paint.kButt_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
        if blur > 0:
            p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
        self.c.drawPath(path, p)

    def arr(self):
        return self.s.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)[..., 0].astype(np.float32) / 255.0


# ───────────────────────────── profil geometrisi ─────────────────────────────
def face_points(d):
    """Sağa bakan yüz profil konturu (alın → boyun). Kişi parametreleriyle değişir. Mutlak koordinat (S=1000 tuvali)."""
    n, hk, br, lip, lip2, ch, jw, fo = d["nose"], d["hook"], d["brow"], d["lip"], d["lip2"], d["chin"], d["jaw"], d["fore"]
    age, jowl = d["age"], d["jowl"]
    pts = [
        (572 + fo, 262),                       # saç çizgisi
        (596 + fo * 0.6, 312),                 # alın
        (604 + br * 0.9, 346),                 # kaş çıkıntısı
        (590 + br * 0.2, 376),                 # burun kökü (çukur)
        (602 + n * 0.25, 410 + hk * 0.4),      # burun sırtı
        (630 + n * 0.8, 452 + hk * 0.9),       # burun ucuna yaklaşım
        (646 + n, 470 + hk * 0.6),             # burun ucu
        (632 + n * 0.7, 486),                  # burun altı (kanat)
        (610, 492),                            # subnasale
        (614 + lip, 512),                      # üst dudak
        (602 + lip * 0.5, 528),                # ağız hattı
        (612 + lip2, 544),                     # alt dudak
        (596 + lip2 * 0.3, 566),               # çene çukuru
        (606 + ch, 598),                       # çene ucu
        (580 + ch * 0.7, 632 + 4 * (jw - 1)),  # çene altı
    ]
    return pts


def head_paths(d):
    """(yüz kontur yolu, kafatası/saç hacmi yolu, çene altı & boyun). Hepsi sağa bakan."""
    pts = face_points(d)
    jw, jowl = d["jaw"], d["jowl"]
    # çene altı → çene köşesi → kulak altı
    under = [(560, 640 + 6 * jowl * 10), (500 - 18 * jowl, 640 + 28 * jowl), (430 - 14 * jowl, 590 + 18 * jowl), (396, 520)]
    face = pts + under
    # yüzün arkası: kulak, şakak, saç çizgisi
    back = [(372, 430), (400, 330), (470, 270)]
    outline = face + back
    return outline


# ───────────────────────────── çizim parçaları ─────────────────────────────
def _skin(cv, d):
    outline = head_paths(d)
    p = _sp(outline, close=True, t=0.45)
    # kafatası
    cv.fill(p, 120)
    skull = skia.Path()
    skull.addOval(skia.Rect.MakeLTRB(344, 168, 624, 560))
    cv.fill(skull, 120)
    # boyun
    nk = d["neck"]
    neck = _sp([(430, 560), (560 - (nk - 1) * 14, 628), (578 + (nk - 1) * 26, 700), (606 + (nk - 1) * 30, 770), (560, 830),
                (420, 830), (356, 760), (352, 620)], close=True, t=0.35)
    cv.fill(neck, 96)
    cv.fill(p, 128, blur=2.0)
    # yanak hacmi
    cheek = skia.Path()
    cheek.addOval(skia.Rect.MakeLTRB(430, 420, 590, 600))
    cv.fill(cheek, 150, blur=22)
    if d["jowl"] > 0:
        j = skia.Path(); j.addOval(skia.Rect.MakeLTRB(430, 560, 570, 660 + d["jowl"] * 20))
        cv.fill(j, 140, blur=16)
    # alın / kaş hacmi
    br = skia.Path(); br.addOval(skia.Rect.MakeLTRB(470, 290, 610, 380))
    cv.fill(br, 150, blur=16)
    return p


def _features(cv, d):
    """Kazıma çizgileri: göz, kaş, burun deliği, dudak, kulak, kırışıklıklar (yükseklik azaltır → oluk)."""
    a = d["age"]
    # kaş
    brow = _sp([(520, 360 + 2 * d["brow"] * 0), (556, 348), (594, 350 + d["brow"] * 0.2)], close=False)
    cv.stroke(brow, 66, 9 + d["brow"] * 0.5)
    # göz
    eye = _sp([(534, 378), (556, 368), (582, 376), (556, 384)], close=True)
    cv.fill(eye, 60)
    cv.stroke(_sp([(530, 374), (556, 363), (586, 372)], close=False), 90, 4)
    cv.stroke(_sp([(534, 392), (558, 398), (582, 392)], close=False), 90, 3 + a * 2)
    # göz bebeği
    ir = skia.Path(); ir.addCircle(560, 376, 6)
    cv.fill(ir, 30)
    # burun kanadı / delik
    nos = _sp([(626 + d["nose"] * 0.5, 480), (616, 486), (606, 484)], close=False)
    cv.stroke(nos, 70, 5)
    cv.stroke(_sp([(604, 440 + d["hook"]), (592, 470), (600, 488)], close=False), 100, 3)
    # dudaklar
    mo = d["mouth_open"]
    lipline = _sp([(560, 528 + 1), (580, 526), (602 + d["lip"] * 0.5, 526 + mo * 6)], close=False)
    cv.stroke(lipline, 56, 6)
    cv.stroke(_sp([(578, 556), (600 + d["lip2"] * 0.3, 556)], close=False), 98, 3)
    # kulak
    ear = _sp([(440, 412), (452, 396), (472, 402), (472, 440), (456, 470), (444, 454)], close=True)
    cv.stroke(ear, 78, 5.5)
    cv.stroke(_sp([(452, 414), (462, 420), (460, 448)], close=False), 90, 3)
    # yanak/ağız kıvrımı (yaşa göre)
    if a > 0.2:
        cv.stroke(_sp([(590, 492), (578, 520), (572, 548)], close=False), 92, 2.5 + a * 3)
    if a > 0.4:
        cv.stroke(_sp([(500, 380), (486, 390), (484, 410)], close=False), 98, 2 + a * 2)
        cv.stroke(_sp([(530, 400), (520, 424)], close=False), 104, 1.8 + a * 1.5)
    if a > 0.6:
        cv.stroke(_sp([(500, 346), (540, 338)], close=False), 108, 2)
        cv.stroke(_sp([(495, 322), (550, 312)], close=False), 110, 2)


def _hair(cv, d):
    kind = d["hair"]
    if kind in (None, "none"):
        return
    if kind in ("bob", "long", "long_wave", "monk", "short", "thin"):
        if kind == "bob":      # Charles'ın gençlik saçı: yanlarda düz, çene hizasına
            pts = [(560, 262), (470, 222), (380, 250), (344, 340), (338, 480), (352, 600), (420, 626), (448, 560), (470, 470), (500, 390), (540, 320)]
            cv.fill(_sp(pts, close=True, t=0.45), 190)
            for i in range(9):
                x = 360 + i * 20
                cv.stroke(_sp([(x + 30, 262 + i * 3), (x - 6, 410), (x - 14, 560)], close=False), 150, 2.4)
        elif kind == "long":
            pts = [(566, 258), (470, 214), (372, 250), (330, 350), (326, 500), (338, 640), (420, 690), (452, 600), (476, 500), (504, 400), (544, 316)]
            cv.fill(_sp(pts, close=True, t=0.45), 188)
            for i in range(10):
                x = 346 + i * 18
                cv.stroke(_sp([(x + 40, 252), (x - 12, 420), (x - 22, 650)], close=False), 148, 2.2)
        elif kind == "long_wave":
            pts = [(566, 256), (470, 206), (366, 244), (322, 350), (316, 520), (340, 680), (410, 720), (452, 620), (478, 500), (504, 400), (544, 316)]
            cv.fill(_sp(pts, close=True, t=0.45), 188)
            for i in range(12):
                x = 336 + i * 15
                cv.stroke(_sp([(x + 36, 250), (x - 18, 400), (x + 8, 530), (x - 16, 690)], close=False), 150, 2.4)
        elif kind == "monk":   # tonsür etrafı saç
            pts = [(520, 292), (430, 268), (366, 330), (352, 450), (380, 520), (430, 470), (470, 380), (506, 330)]
            cv.fill(_sp(pts, close=True, t=0.45), 182)
            for i in range(8):
                cv.stroke(_sp([(500 - i * 18, 300 + i * 6), (440 - i * 12, 400), (400 - i * 8, 500)], close=False), 146, 2.2)
        elif kind == "short":
            pts = [(574, 262), (500, 214), (410, 226), (356, 300), (350, 400), (392, 456), (420, 400), (460, 330), (520, 284)]
            cv.fill(_sp(pts, close=True, t=0.45), 186)
            for i in range(10):
                cv.stroke(_sp([(560 - i * 22, 252 + i * 3), (470 - i * 10, 270 + i * 5), (400, 330 + i * 8)], close=False), 148, 2)
        elif kind == "thin":
            pts = [(470, 224), (400, 250), (360, 330), (358, 420), (400, 440), (428, 370), (446, 300)]
            cv.fill(_sp(pts, close=True, t=0.45), 176)
            for i in range(6):
                cv.stroke(_sp([(440 - i * 14, 236 + i * 8), (400 - i * 8, 340), (386 - i * 5, 420)], close=False), 140, 2)
        return
    if kind == "veil":
        pass


def _beard(cv, d):
    kind = d["beard"]
    if not kind:
        return
    base = [(486, 520), (520, 560), (560, 620)]
    if kind == "short":
        pts = [(468, 440), (530, 470), (580, 506), (596, 560), (604 + d["chin"], 604), (580 + d["chin"] * 0.6, 640), (540, 660), (470, 640), (420, 580), (410, 500)]
        cv.fill(_sp(pts, close=True, t=0.45), 170)
        for i in range(16):
            x = 450 + i * 9
            cv.stroke(_sp([(x, 500 + (i % 3) * 8), (x + 8, 580), (x + 6, 640 + (i % 4) * 5)], close=False), 140, 1.8)
    elif kind == "full":
        pts = [(452, 430), (528, 474), (582, 508), (598, 570), (606 + d["chin"], 640), (584 + d["chin"] * 0.6, 700), (548, 742), (500, 748), (452, 700), (418, 610), (404, 510)]
        cv.fill(_sp(pts, close=True, t=0.45), 172)
        for i in range(20):
            x = 440 + i * 8
            cv.stroke(_sp([(x, 500 + (i % 3) * 8), (x + 10, 610), (x + 4, 700 + (i % 5) * 6)], close=False), 142, 1.9)
    elif kind == "long":
        pts = [(452, 430), (528, 474), (582, 508), (598, 570), (610 + d["chin"], 650), (596 + d["chin"] * 0.6, 740), (560, 830), (520, 880), (480, 820), (440, 720), (416, 620), (404, 520)]
        cv.fill(_sp(pts, close=True, t=0.45), 172)
        for i in range(22):
            x = 436 + i * 8
            cv.stroke(_sp([(x, 500), (x + 12, 650), (x + 8, 800 + (i % 5) * 8)], close=False), 142, 1.9)
    elif kind in ("long_pointed", "pointed", "goatee"):
        ln = {"long_pointed": 120, "pointed": 70, "goatee": 40}[kind]
        pts = [(560, 560), (600 + d["chin"], 598), (608 + d["chin"], 640), (570 + d["chin"] * 0.5, 650 + ln), (540, 650), (520, 600)]
        cv.fill(_sp(pts, close=True, t=0.45), 172)
        for i in range(10):
            cv.stroke(_sp([(560 + i * 5, 570), (574 + d["chin"] * 0.5, 620 + ln * 0.5), (566 + d["chin"] * 0.4, 640 + ln * (0.8 + 0.02 * i))], close=False), 142, 1.8)
        # favoriler (long_pointed için yanak sakalı)
        if kind == "long_pointed":
            pts2 = [(468, 440), (530, 470), (560, 520), (540, 580), (480, 560), (420, 500), (410, 450)]
            cv.fill(_sp(pts2, close=True, t=0.45), 166)
    if kind == "mustache" or kind == "long_pointed" or kind in ("goatee",):
        m = _sp([(612, 504), (590, 506), (562, 514), (550, 530)], close=False)
        cv.stroke(m, 172, 11)
        cv.stroke(_sp([(604, 500), (580, 502), (556, 512)], close=False), 140, 2.4)
    if kind == "mustache":
        m = _sp([(616, 500), (596, 496), (566, 504), (540, 526)], close=False)
        cv.stroke(m, 175, 14)
        cv.stroke(_sp([(560, 520), (590, 522), (606, 530)], close=False), 120, 3)
        # ince sakal
        pts = [(566, 586), (598 + d["chin"], 616), (590, 650), (560, 610)]
        cv.fill(_sp(pts, close=True, t=0.5), 160)


def _hat(cv, d):
    k = d["hat"]
    if k in (None, "none"):
        return
    if k == "flatcap":        # düz, geniş bere (Rönesans)
        base = _sp([(330, 262), (350, 212), (420, 190), (520, 196), (592, 220), (610, 250), (580, 270), (500, 250), (420, 262), (360, 290)], close=True, t=0.45)
        cv.fill(base, 220)
        cv.stroke(_sp([(350, 250), (420, 226), (520, 232), (590, 252)], close=False), 150, 3)
        cv.stroke(_sp([(560, 226), (620, 200), (660, 170)], close=False), 205, 10)         # tüy sapı
        cv.stroke(_sp([(560, 226), (620, 190), (680, 176)], close=False), 150, 2)
    elif k == "cap":
        base = _sp([(340, 280), (360, 214), (440, 178), (540, 196), (592, 240), (590, 276), (500, 256), (410, 268)], close=True, t=0.45)
        cv.fill(base, 214)
        cv.stroke(_sp([(360, 262), (440, 240), (540, 246), (590, 268)], close=False), 140, 3)
    elif k == "beret_f":      # geniş yassı bere + tüy
        base = _sp([(310, 270), (322, 200), (410, 150), (540, 156), (640, 196), (670, 250), (620, 282), (540, 262), (440, 270), (360, 296)], close=True, t=0.45)
        cv.fill(base, 224)
        for i in range(5):
            cv.stroke(_sp([(350 + i * 60, 252), (400 + i * 50, 200), (470 + i * 40, 180)], close=False), 160, 2.5)
        cv.stroke(_sp([(600, 190), (680, 150), (740, 160), (770, 215), (730, 250)], close=False), 214, 12)
        cv.stroke(_sp([(600, 190), (690, 150), (744, 170)], close=False), 160, 2)
    elif k == "cap_black":    # Luther'in/ alimlerin siyah kep'i
        base = _sp([(344, 262), (366, 196), (450, 160), (546, 170), (598, 220), (592, 262), (500, 240), (420, 252)], close=True, t=0.45)
        cv.fill(base, 212)
        cv.stroke(_sp([(366, 246), (450, 226), (546, 232), (592, 256)], close=False), 150, 3)
    elif k == "cap_gold":
        base = _sp([(344, 262), (368, 198), (450, 164), (544, 172), (598, 220), (592, 262), (500, 244), (420, 254)], close=True, t=0.45)
        cv.fill(base, 218)
        for i in range(8):
            cv.stroke(_sp([(380 + i * 26, 246), (390 + i * 24, 210), (410 + i * 22, 186)], close=False), 160, 2)
        cv.stroke(_sp([(366, 246), (450, 230), (546, 236), (592, 258)], close=False), 235, 6)
    elif k == "skull":        # yaşlı Charles: kapalı küçük takke
        base = _sp([(350, 300), (370, 220), (450, 180), (540, 200), (586, 252), (572, 286), (500, 262), (420, 278)], close=True, t=0.45)
        cv.fill(base, 208)
        cv.stroke(_sp([(372, 270), (450, 246), (540, 252), (576, 274)], close=False), 150, 3)
    elif k in ("turban_big", "turban_small"):
        big = k == "turban_big"
        sc = 1.0 if big else 0.8
        cx, cy = 482, 262
        W2, H2 = 190 * sc, 250 * sc
        dome = skia.Path(); dome.addOval(skia.Rect.MakeLTRB(cx - W2, cy - H2, cx + W2, cy + 46 * sc))
        cv.fill(dome, 212, blur=1.0)
        n = 7 if big else 5
        for i in range(n):
            t = i / (n - 1)
            y0 = cy - H2 * 0.88 + t * (H2 * 1.0)
            w0 = W2 * math.sqrt(max(0.06, 1 - ((y0 - (cy - H2 * 0.40)) / (H2 * 0.62)) ** 2))
            cv.stroke(_sp([(cx - w0, y0 + 36 * sc), (cx - w0 * 0.1, y0 - 16 * sc), (cx + w0 * 0.85, y0 + 24 * sc)], close=False), 120, 5.5 * sc + 1.5)
            cv.stroke(_sp([(cx - w0 * 0.92, y0 + 50 * sc), (cx, y0 + 6 * sc), (cx + w0 * 0.92, y0 + 40 * sc)], close=False), 250, 3.6 * sc + 1.0)
        band = _sp([(cx - W2 * 1.02, cy + 6 * sc), (cx - 100 * sc, cy + 44 * sc), (cx + 180 * sc, cy + 40 * sc), (cx + W2 * 1.04, cy - 4 * sc)], close=False)
        cv.stroke(band, 236, 16 * sc + 4)
        if big:
            cv.fill(_sp([(cx + 30, cy - H2 * 0.92), (cx + 62, cy - H2 * 1.28), (cx + 96, cy - H2 * 0.92)], close=True), 242)
            cv.stroke(_sp([(cx + 62, cy - H2 * 1.28), (cx + 62, cy - H2 * 0.95)], close=False), 150, 3)
    elif k == "camauro":      # papalık takkesi
        base = _sp([(344, 330), (356, 230), (440, 190), (540, 214), (590, 270), (566, 300), (500, 280), (440, 300), (400, 440), (392, 540), (350, 480)], close=True, t=0.45)
        cv.fill(base, 214)
        cv.stroke(_sp([(366, 290), (450, 250), (560, 276)], close=False), 150, 3)
    elif k == "morion":       # fatih miğferi
        base = _sp([(330, 330), (350, 224), (440, 150), (540, 130), (620, 170), (680, 250), (640, 270), (560, 250), (460, 270), (390, 310)], close=True, t=0.45)
        cv.fill(base, 232)
        cv.stroke(_sp([(380, 270), (470, 240), (600, 236), (650, 262)], close=False), 150, 3)
        cv.stroke(_sp([(420, 190), (520, 130), (600, 140)], close=False), 252, 10)       # tepelik
    elif k in ("widow_hood", "gable_hood"):
        pts = [(560, 262), (480, 190), (380, 200), (320, 320), (300, 520), (320, 700), (400, 760), (440, 620), (456, 480), (510, 360)]
        cv.fill(_sp(pts, close=True, t=0.4), 206)
        cv.stroke(_sp([(560, 262), (500, 230), (420, 244), (370, 330)], close=False), 150, 3)
        for i in range(6):
            cv.stroke(_sp([(340 + i * 14, 300), (326 + i * 12, 500), (330 + i * 12, 700)], close=False), 150, 2.2)
        if k == "gable_hood":
            cv.stroke(_sp([(566, 270), (600, 240), (620, 200)], close=False), 240, 6)


def _garment(cv, d):
    k = d["garment"]
    # temel omuz/gövde
    body = _sp([(250, 1040), (262, 900), (330, 800), (450, 770), (590, 770), (690, 820), (770, 900), (800, 1040)], close=True, t=0.4)
    cv.fill(body, 74)
    if k in ("fleece", "fur_doublet", "doublet", "robe", "robe_white", "fur_robe", "mourning", "mourning_f", "gown_f", "kaftan", "cassock", "armor", "ruff_black"):
        cv.fill(body, 80, blur=6)
    if k == "fleece":         # Altın Post zinciri + kürk yaka
        cv.stroke(_sp([(380, 770), (470, 840), (560, 860), (650, 820)], close=False), 150, 26)
        for i in range(16):
            t = i / 15.0
            x = 390 + t * 260
            y = 770 + math.sin(t * math.pi) * 96 + t * 40
            r = skia.Path(); r.addOval(skia.Rect.MakeLTRB(x - 13, y - 9, x + 13, y + 9))
            cv.stroke(r, 230, 4)
        cv.fill(_sp([(520, 890), (560, 940), (500, 980), (470, 930)], close=True), 232)
        cv.fill(_sp([(520, 900), (545, 940), (505, 965)], close=True), 100)
    elif k in ("fur_doublet", "fur_robe"):
        cv.stroke(_sp([(370, 770), (470, 800), (570, 790), (660, 810)], close=False), 160, 34, blur=1.5)
        for i in range(30):
            x = 380 + i * 10
            cv.stroke(_sp([(x, 770 + (i % 2) * 6), (x + 3, 810)], close=False), 190, 2)
    elif k == "ruff_black":   # fırfır yaka
        for i in range(14):
            x = 320 + i * 30
            r = skia.Path(); r.addOval(skia.Rect.MakeLTRB(x - 24, 742, x + 24, 800 + (i % 2) * 10))
            cv.fill(r, 200)
            cv.stroke(r, 120, 2.4)
    elif k in ("robe_white",):
        cv.stroke(_sp([(430, 770), (520, 850), (600, 780)], close=False), 190, 14)
        cv.stroke(_sp([(520, 850), (520, 1000)], close=False), 150, 4)
    elif k in ("mourning", "mourning_f", "robe", "gown_f"):
        cv.stroke(_sp([(430, 764), (500, 790), (570, 764)], close=False), 160, 12)
        cv.stroke(_sp([(500, 790), (500, 1000)], close=False), 130, 3)
    elif k == "kaftan":
        cv.stroke(_sp([(420, 770), (500, 830), (590, 780)], close=False), 160, 18)
        for i in range(5):
            cv.stroke(_sp([(520 + i * 6, 840 + i * 30), (540 + i * 6, 940 + i * 20)], close=False), 190, 2.5)
    elif k == "cassock":
        cv.stroke(_sp([(430, 764), (520, 830), (600, 770)], close=False), 175, 22)
        cv.stroke(_sp([(520, 830), (520, 1000)], close=False), 140, 3)
        cv.fill(_sp([(470, 800), (520, 880), (570, 800)], close=True), 190)     # omuz mozetta
    elif k == "armor":
        for i in range(6):
            cv.stroke(_sp([(330 + i * 6, 800 + i * 34), (500, 780 + i * 36), (690 - i * 6, 810 + i * 34)], close=False), 170, 3)
        cv.stroke(_sp([(420, 770), (520, 790), (610, 770)], close=False), 200, 16)       # gorget
        for i in range(10):
            cv.fill(_sp(sk.ngon(380 + i * 30, 842, 4, 6), close=True), 230)


# ───────────────────────────── ana sprite ─────────────────────────────
def portrait_height(key, flip=False):
    d = PEOPLE[key]
    cv = _Canvas()
    _garment(cv, d)
    _skin(cv, d)
    _hair(cv, d)
    _beard(cv, d)
    _features(cv, d)
    _hat(cv, d)
    h = cv.arr()
    if flip:
        h = h[:, ::-1]
    return h


def ring_text_mask(text, radius, size_px, track=4.0, face="title"):
    """Daire boyunca yazı (üstten başlayıp saat yönünde ortalı). S×S float maske."""
    s = skia.Surface(S, S)
    c = s.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    wid = sk.text_width(text, face, size_px, track)
    total_ang = wid / radius
    ang0 = -math.pi / 2 - total_ang / 2
    x = 0.0
    for ch in text:
        w = sk.text_width(ch, face, size_px, 0)
        a = ang0 + (x + w / 2) / radius
        c.save()
        c.translate(S / 2 + math.cos(a) * radius, S / 2 + math.sin(a) * radius)
        c.rotate(math.degrees(a + math.pi / 2))
        blob, _ = sk.text_blob(face, ch, size_px, 0)
        c.drawTextBlob(blob, -w / 2, size_px * 0.36, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
        c.restore()
        x += sk.text_width(ch, face, size_px, 0) + track
    return s.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)[..., 3].astype(np.float32) / 255.0


@lru_cache(maxsize=64)
def medal_array(key, metal="gold", inscription=None, flip=False, rim=True, size=1000):
    """RGBA uint8 (S×S) madalya sprite."""
    d = PEOPLE[key]
    por = portrait_height(key, flip)
    # portreyi büyüt ve ortala (başın merkezi ≈ (500, 420) → medalin görsel merkezine)
    sc = d.get("scale", 1.22)
    dy = d.get("dy", 0)
    shift_x = -(-85 if not flip else 85)
    Mtx = np.float32([[sc, 0, S / 2 - 520 * sc + (shift_x if not flip else shift_x)], [0, sc, S / 2 - 470 * sc + 20 + dy]])
    if flip:
        Mtx[0, 2] = S / 2 - 480 * sc - 85
    por = cv2.warpAffine(por, Mtx, (S, S), flags=cv2.INTER_LINEAR, borderValue=0)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    rr = np.hypot(xx - S / 2, yy - S / 2)
    disc = (rr <= 484).astype(np.float32)
    # alan: hafif içbükey; kenar halkası yüksek
    pmask = cv2.GaussianBlur((por > 0.02).astype(np.float32), (0, 0), 5)
    pat = 0.006 * np.cos(rr * 0.40) + 0.004 * np.cos(np.arctan2(yy - S / 2, xx - S / 2) * 60) * np.clip(rr / 484, 0, 1)
    field = 0.10 + 0.04 * np.clip(1 - rr / 484, 0, 1) + pat * (1 - pmask)
    ring = np.exp(-((rr - 466) / 12.0) ** 2) * 0.5 + np.exp(-((rr - 408) / 5.0) ** 2) * 0.28
    beads = np.zeros_like(rr)
    if rim:
        ang = np.arctan2(yy - S / 2, xx - S / 2)
        beads = np.exp(-((rr - 437) / 8.0) ** 2) * (0.5 + 0.5 * np.cos(ang * 72)) * 0.22
    ins = np.zeros_like(rr)
    if inscription:
        m = ring_text_mask(inscription, 440, 54, track=5.0)
        ins = cv2.GaussianBlur(m, (0, 0), 1.0) * 0.55
    # portre: daire içine kırp + merkezi hafifçe kaydır
    inner = (rr <= 400).astype(np.float32)
    inner = cv2.GaussianBlur(inner, (0, 0), 6)
    H = field + ring + beads + ins
    h2 = por * 0.95
    h2 = cv2.GaussianBlur(h2, (0, 0), 2.2)
    portrait_mask = (por > 0.02).astype(np.float32)
    H = H + h2 * inner * 1.0 + 0.10 * portrait_mask * inner
    H = np.where(disc > 0, H, 0)
    # eğim → gölgelendirme (relief_sprite yüksekliği doğrudan kullansın)
    return _relief_from_height(H, disc, metal)


def _relief_from_height(Hh, alpha, metal="gold", strength=2.6, light=(-0.55, -0.62)):
    h = cv2.GaussianBlur(Hh, (0, 0), 1.3)
    gx = cv2.Sobel(h, cv2.CV_32F, 1, 0, ksize=3) * strength
    gy = cv2.Sobel(h, cv2.CV_32F, 0, 1, ksize=3) * strength
    nz = np.ones_like(h)
    inv = 1.0 / np.sqrt(gx * gx + gy * gy + 1.0)
    nx, ny, nz = -gx * inv, -gy * inv, inv
    lx, ly = light
    lz = math.sqrt(max(0.05, 1 - lx * lx - ly * ly))
    dif = np.clip(nx * lx + ny * ly + nz * lz, 0, 1)
    shade = np.clip(0.5 + (dif - lz) * 2.6, 0, 1)
    hx, hy, hz = lx, ly, lz + 1.0
    hn = math.sqrt(hx * hx + hy * hy + hz * hz)
    sp = np.clip((nx * hx + ny * hy + nz * hz) / hn, 0, 1) ** 34
    ramp = sk._grad_ramp(sk.METAL[metal])
    col = ramp[np.clip(shade * 255, 0, 255).astype(np.int32)]
    # yüksekliğe göre hafif aydınlık (ön plan öğeler parlak)
    col = col * (0.64 + 0.62 * np.clip(Hh, 0, 1.3)[..., None])
    col = col + sp[..., None] * 255 * 0.55
    a = np.clip(alpha, 0, 1) * 255
    return np.dstack([np.clip(col, 0, 255), a]).astype(np.uint8)


def medal_image(key, metal="gold", inscription=None, flip=False, size=700):
    arr = medal_array(key, metal, inscription, flip)
    if size != S:
        arr = cv2.resize(arr, (size, size), interpolation=cv2.INTER_AREA)
    return np_to_image(arr)


INSCR = {
    "karl_genc": "CAROLVS · V · ROM · IMP · SEMPER · AVG ·", "karl_olgun": "CAROLVS · V · ROM · IMP · SEMPER · AVG ·",
    "karl_yasli": "CAROLVS · V · ROM · IMP · SEMPER · AVG ·", "fransuva": "FRANCISCVS · I · FRANCORVM · REX ·",
    "henri8": "HENRICVS · VIII · ANGLIAE · REX ·", "luther": "MARTINVS · LVTHERVS · ANNO · MDXXI ·",
    "melanchthon": "PHILIPPVS · MELANTHON ·", "suleyman": "SVLTAN · SOLYMAN · TVRCARVM · IMP ·",
    "barbaros": "BARBAROSSA · CHAIRADINVS · ·", "fugger": "IACOBVS · FVGGER · AVGVSTANVS ·", "klemens": "CLEMENS · VII · PONT · MAX ·",
    "felipe2": "PHILIPPVS · II · HISPANIARVM · REX ·", "juana": "IOANNA · CASTELLAE · REGINA ·", "isabel": "ISABELLA · LVSITANIAE ·",
    "ferdinand": "FERDINANDVS · ROM · REX ·", "maksimilian": "MAXIMILIANVS · ROM · IMP ·", "kortes": "FERDINANDVS · CORTES ·",
    "pizarro": "FRANCISCVS · PIZARRO ·", "lascasas": "BARTOLOME · DE · LAS · CASAS ·", "moritz": "MAVRITIVS · DVX · SAXONIAE ·",
    "orange": "GVILELMVS · PRINCEPS · AVRIACVS ·", "margareta": "MARGARITA · AVSTRIACA ·", "tiziano": "TITIANVS · VECELLIVS ·",
    "durer": "ALBERTVS · DVRER · NORICVS ·", "elkano": "IOANNES · SEBASTIANVS · ELCANO ·", "makedonya": "· · ·",
}


def medal_sheet(keys, metal="gold", cols=5, size=360, out="medals_sheet.png"):
    rows = (len(keys) + cols - 1) // cols
    img = np.zeros((rows * size, cols * size, 3), np.uint8)
    img[:] = (28, 18, 12)
    for i, k in enumerate(keys):
        a = cv2.resize(medal_array(k, metal, INSCR.get(k)), (size, size), interpolation=cv2.INTER_AREA)
        al = a[..., 3:4].astype(np.float32) / 255
        r, c = divmod(i, cols)
        sl = img[r * size:(r + 1) * size, c * size:(c + 1) * size]
        sl[:] = (sl * (1 - al) + a[..., :3] * al).astype(np.uint8)
    cv2.imwrite(out, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    return out
