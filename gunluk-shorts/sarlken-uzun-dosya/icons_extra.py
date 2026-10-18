"""MADALYA-LAB ek kabartma simgeleri (Şarlken dosyası): icons.py'nin @icon sözleşmesiyle (512×512 maske, merkez 256,256).

Kayıt: `import icons` + `@icons.icon("ad")` → icons.names(), icons.draw_icon(...), shots 'emblem'/'iconrow'/map icons_ otomatik kullanır.
Silüet önce (kalın, ≥ 26 px kütleler), iç ayrıntılar çentik (cut) olarak: 120 px'te okunur, 460 px'te zengindir.
Önizleme: `icons_extra.sheet(keys=None, metals=("gold",), cols=8, size=200, out="out/frames/icons_extra_sheet.png")`.
Takma adlar: gun → arquebus, sun → sun_disc.
"""
import math
from contextlib import contextmanager

import cv2
import numpy as np
import skia

import icons
import sk
from icons import icon, _M, N

NEW = ["press", "chest", "globe", "compass", "helmet", "horse", "arquebus", "flag", "candle", "sun_disc", "feather", "bell", "ballot",
       "gavel", "pillars", "cane", "pickaxe", "galley", "litter", "chains", "lightning", "heart", "fist", "mountain", "elector_hat",
       "foot_gout", "bed", "tent", "ladder", "crown_cracked", "sack", "book_open"]


# ───────────────────────────── yardımcılar ─────────────────────────────
def sm(pts, close=True, t=0.4):
    return sk.smooth_path(pts, close, t)


def pl(pts, close=True):
    return sk.poly_path(pts, close)


def cutl(m, pts, w=5, smooth=False, t=0.5):
    m.cut(sm(pts, False, t) if smooth else pl(pts, False), w)


def ring(m, x, y, r, w, v=255):
    p = skia.Path()
    p.addCircle(x, y, r)
    m.stroke(p, w, v)


def cring(m, x, y, r, w):
    p = skia.Path()
    p.addCircle(x, y, r)
    m.cut(p, w)


def rr_cut(m, x, y, w, h, r, wd):
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r))
    m.cut(p, wd)


def oval_stroke(m, x, y, rx, ry, w, v=255, rot=0.0):
    m.c.save()
    m.c.translate(x, y)
    if rot:
        m.c.rotate(rot)
    p = skia.Path()
    p.addOval(skia.Rect.MakeLTRB(-rx, -ry, rx, ry))
    m.c.drawPath(p, m._p(v, "stroke", w))
    m.c.restore()


def oval_rot(m, x, y, rx, ry, rot=0.0, v=255):
    m.c.save()
    m.c.translate(x, y)
    if rot:
        m.c.rotate(rot)
    m.c.drawOval(skia.Rect.MakeLTRB(-rx, -ry, rx, ry), m._p(v))
    m.c.restore()


@contextmanager
def clipm(m, path):
    m.c.save()
    m.c.clipPath(path, skia.ClipOp.kIntersect, True)
    try:
        yield
    finally:
        m.c.restore()


@contextmanager
def xform(m, tx=0, ty=0, rot=0.0, sc=1.0, cx=256, cy=256):
    m.c.save()
    m.c.translate(cx + tx, cy + ty)
    if rot:
        m.c.rotate(rot)
    if sc != 1.0:
        m.c.scale(sc, sc)
    m.c.translate(-cx, -cy)
    try:
        yield
    finally:
        m.c.restore()


def crs(pts, n=14):
    p = np.asarray(pts, float)
    out = []
    for i in range(len(p) - 1):
        p0 = p[i - 1] if i > 0 else p[i]
        p1, p2 = p[i], p[i + 1]
        p3 = p[i + 2] if i + 2 < len(p) else p[i + 1]
        for k in range(n):
            t = k / n
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(p[-1])
    return np.array(out)


def leaf(m, spine, w, prof=None, v=255, skew=0.0):
    """Omurga eğrisi boyunca değişken genişlikli dolu şekil → (omurga, normaller, yarım genişlikler)."""
    a = crs(spine, 16)
    t = np.gradient(a, axis=0)
    t /= (np.hypot(t[:, 0], t[:, 1])[:, None] + 1e-6)
    nr = np.stack([-t[:, 1], t[:, 0]], 1)
    n = len(a)
    ws = np.array([w * (prof(i / (n - 1)) if prof else math.sin(math.pi * i / (n - 1)) ** 0.8) / 2 for i in range(n)])[:, None]
    L = a + nr * ws * (1 + skew)
    R = a - nr * ws * (1 - skew)
    m.fill(pl([tuple(map(float, p)) for p in np.vstack([L, R[::-1]])]), v)
    return a, nr, ws


# ═════════════════════════════ simgeler ═════════════════════════════
@icon("press")
def _press(m):
    m.rect(66, 438, 380, 34, r=10)                    # taban
    m.rect(102, 96, 46, 352, r=8)                     # sol direk
    m.rect(364, 96, 46, 352, r=8)                     # sağ direk
    m.rect(80, 66, 352, 54, r=12)                     # üst kiriş
    m.rect(230, 116, 52, 176, r=8)                    # vida mili
    m.rect(174, 284, 164, 40, r=8)                    # baskı levhası
    m.rect(120, 356, 272, 40, r=10)                   # mürekkepli tabla
    m.line(146, 204, 470, 166, 20)                    # uzun kol
    m.circle(480, 164, 28)
    m.circle(142, 206, 18)
    for y in range(138, 280, 20):                     # vida dişleri
        m.cut(pl([(230, y), (282, y + 9)], False), 5)
    m.cut(pl([(230, 120), (282, 120)], False), 5)
    m.cut(pl([(174, 326), (338, 326)], False), 5)
    m.cut(pl([(120, 360), (392, 360)], False), 5)
    m.cut(pl([(148, 380), (366, 380)], False), 4)
    m.cut(pl([(148, 250), (230, 250)], False), 4)     # direkle vida arası boşluk
    m.cut(pl([(282, 250), (364, 250)], False), 4)
    for x in (125, 387):
        m.cut(pl([(x, 140), (x, 420)], False), 4)
    m.cut(pl([(80, 120), (432, 120)], False), 5)


@icon("chest")
def _chest(m):
    m.rect(64, 238, 384, 206, r=12)                   # gövde
    m.smooth([(64, 244), (72, 192), (130, 142), (256, 116), (382, 142), (440, 192), (448, 244)], close=True, t=0.35)   # kavisli kapak
    m.rect(50, 430, 412, 30, r=10)                    # taban kuşağı
    m.cut(pl([(64, 246), (448, 246)], False), 7)
    for x in (150, 362):
        m.cut(pl([(x, 134), (x, 432)], False), 9)
    for (x, y) in [(107, 180), (107, 300), (107, 400), (405, 180), (405, 300), (405, 400)]:
        cring(m, x, y, 6, 4)
    m.rect(218, 210, 76, 100, r=14)                   # kilit plakası
    rr_cut(m, 218, 210, 76, 100, 14, 5)
    m.circle(256, 252, 12, 0)
    m.rect(251, 252, 10, 34, 0, r=4)
    cutl(m, [(100, 138), (256, 100), (412, 138)], 5, smooth=True)


@icon("globe")
def _globe(m):
    cx, cy, R = 256, 218, 150
    m.circle(cx, cy, R)
    ring(m, cx, cy, 190, 18)
    cring(m, cx, cy, 168, 8)
    m.circle(cx, cy - 190, 16)
    m.circle(cx, cy + 190, 16)
    m.rect(238, 398, 36, 46, r=6)
    m.smooth([(148, 478), (170, 446), (342, 446), (364, 478)], close=True, t=0.2)
    clip = skia.Path()
    clip.addCircle(cx, cy, R + 1)
    with clipm(m, clip):
        for rx in (52, 112):
            p = skia.Path()
            p.addOval(skia.Rect.MakeLTRB(cx - rx, cy - R, cx + rx, cy + R))
            m.cut(p, 5)
        m.cut(pl([(cx, cy - R), (cx, cy + R)], False), 5)
        for dy in (-84, 0, 84):
            cutl(m, [(cx - R, cy + dy), (cx, cy + dy + (14 if dy else 0)), (cx + R, cy + dy)], 5, smooth=True)
        # kıta kenarları (kabaca, çentik çizgisi)
        m.cut(sm([(196, 160), (232, 148), (246, 186), (222, 230), (190, 206)], True, 0.5), 7)
        m.cut(sm([(286, 200), (336, 186), (350, 240), (318, 290), (290, 258)], True, 0.5), 7)
        m.cut(sm([(310, 120), (350, 128), (360, 156), (326, 160)], True, 0.5), 6)
    cutl(m, [(188, 428), (256, 440), (324, 428)], 4, smooth=True)


@icon("compass")
def _compass(m):
    cx, cy = 256, 256
    ring(m, cx, cy, 196, 28)
    for i in range(32):
        a = math.radians(i * 11.25)
        r = 196
        m.cut(pl([(cx + math.cos(a) * (r - 2), cy + math.sin(a) * (r - 2)), (cx + math.cos(a) * (r + 2), cy + math.sin(a) * (r + 2))], False), 0)
    pts = []
    for i in range(16):
        a = math.radians(-90 + i * 22.5)
        r = 170 if i % 4 == 0 else (112 if i % 4 == 2 else 46)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    m.poly(pts)
    for i in range(0, 16, 4):
        a = math.radians(-90 + i * 22.5)
        m.cut(pl([(cx, cy), (cx + 168 * math.cos(a), cy + 168 * math.sin(a))], False), 4)
    for i in range(2, 16, 4):
        a = math.radians(-90 + i * 22.5)
        m.cut(pl([(cx, cy), (cx + 110 * math.cos(a), cy + 110 * math.sin(a))], False), 3)
    cring(m, cx, cy, 128, 4)
    m.circle(cx, cy, 24, 0)
    m.circle(cx, cy, 11)
    for i in range(16):
        a = math.radians(i * 22.5)
        cring_pt = (cx + 196 * math.cos(a), cy + 196 * math.sin(a))
        m.circle(cring_pt[0], cring_pt[1], 5, 0)
    m.smooth([(256, 38), (276, 70), (256, 62), (236, 70)], close=True, t=0.2)           # kuzey zambağı


@icon("helmet")
def _helmet(m):
    # morion: yüksek tepelik + öne/arkaya kalkık kayık siperlik
    m.smooth([(118, 330), (126, 250), (184, 196), (256, 184), (328, 196), (386, 250), (394, 330)], close=True, t=0.4)   # kubbe
    m.smooth([(126, 262), (148, 168), (206, 116), (256, 96), (306, 116), (364, 168), (386, 262), (330, 190), (256, 176), (182, 190)], close=True, t=0.4)   # tepelik (kubbeye gömülü)
    m.smooth([(34, 252), (70, 336), (170, 372), (256, 378), (342, 372), (442, 336), (478, 252), (426, 316), (342, 338), (256, 342),
              (170, 338), (86, 316)], close=True, t=0.32)                                                               # siperlik
    m.rect(106, 318, 300, 24, r=10)
    m.cut(sm([(150, 250), (176, 178), (222, 132), (256, 118), (290, 132), (336, 178), (362, 250)], False, 0.5), 5)       # tepelik oluğu
    m.cut(pl([(112, 330), (400, 330)], False), 5)
    for k in range(7):
        m.circle(150 + k * 35, 330, 6, 0)
    m.cut(sm([(186, 222), (256, 206), (326, 222)], False, 0.5), 4)
    m.cut(sm([(136, 280), (150, 300)], False, 0.5), 4)
    m.cut(sm([(376, 280), (362, 300)], False, 0.5), 4)


@icon("horse")
def _horse(m):
    # gövde
    m.smooth([(96, 236), (122, 196), (196, 184), (268, 192), (318, 206), (346, 238), (336, 282), (284, 306), (196, 308), (128, 292), (100, 268)], close=True, t=0.45)
    # boyun
    m.smooth([(300, 214), (330, 150), (366, 96), (404, 70), (430, 86), (424, 128), (402, 176), (392, 236), (340, 266)], close=True, t=0.4)
    # baş + burun
    m.smooth([(396, 84), (440, 72), (484, 114), (498, 156), (482, 176), (448, 170), (418, 142), (396, 138)], close=True, t=0.4)
    m.smooth([(400, 80), (414, 40), (432, 78)], close=True, t=0.2)           # kulak
    # yele
    for (x, y) in [(318, 196), (330, 162), (346, 130), (364, 102), (386, 78)]:
        m.circle(x - 14, y, 15)
    # bacaklar (yürüyüş: ön uzak bacak kalkık)
    m.stroke(sk.smooth_path([(330, 276), (342, 352), (336, 424)], False, 0.4), 32)
    m.rect(318, 424, 46, 24, r=8)
    m.stroke(sk.smooth_path([(364, 262), (410, 322), (394, 372)], False, 0.4), 28)
    m.rect(374, 366, 44, 22, r=8)
    m.stroke(sk.smooth_path([(160, 280), (140, 352), (156, 424)], False, 0.4), 36)
    m.rect(134, 424, 50, 24, r=8)
    m.stroke(sk.smooth_path([(212, 296), (242, 360), (232, 424)], False, 0.4), 30)
    m.rect(210, 424, 46, 24, r=8)
    # kuyruk
    m.smooth([(110, 206), (74, 224), (52, 280), (50, 346), (66, 392), (82, 346), (88, 280), (116, 236)], close=True, t=0.45)
    # çentikler
    m.circle(452, 108, 6, 0)
    cutl(m, [(486, 150), (470, 160), (452, 156)], 4, smooth=True)
    cutl(m, [(334, 288), (350, 300)], 4)
    m.cut(pl([(208, 296), (214, 310)], False), 4)
    cutl(m, [(396, 98), (380, 140), (372, 190)], 4, smooth=True)
    cutl(m, [(190, 222), (250, 214), (310, 226)], 4, smooth=True)
    cutl(m, [(70, 250), (62, 330), (72, 372)], 3, smooth=True)


@icon("arquebus")
def _arquebus(m):
    with xform(m, tx=-30, ty=16, rot=-26, sc=0.92, cx=256, cy=250):
        m.rect(18, 232, 314, 32, r=12)                                # namlu
        m.rect(6, 224, 28, 48, r=9)                                   # ağız
        stock = [(300, 224), (380, 226), (432, 238), (490, 266), (524, 314), (524, 376), (488, 384), (446, 334), (390, 298), (300, 284)]
        m.smooth(stock, close=True, t=0.3)                            # kundak
        m.rect(316, 252, 86, 54, r=12)                                # çakmak plakası
        m.stroke(sk.smooth_path([(362, 254), (376, 206), (410, 178), (440, 194)], False, 0.5), 20)   # horoz (S kolu)
        m.circle(442, 196, 13)
        m.rect(60, 270, 250, 12, r=5)                                 # çubuk (ramrod)
        guard = skia.Path()
        guard.addArc(skia.Rect.MakeLTRB(342, 286, 436, 362), 0, 180)
        m.stroke(guard, 13)
        m.rect(380, 302, 11, 32, r=4)                                 # tetik
        for x in (80, 150, 220, 290):
            m.cut(pl([(x, 232), (x, 264)], False), 5)
        m.cut(pl([(24, 248), (326, 248)], False), 3)
        cring(m, 358, 279, 12, 4)
        m.cut(pl([(326, 270), (396, 270)], False), 4)
        cutl(m, [(404, 238), (444, 276), (470, 336)], 4, smooth=True)
        m.cut(pl([(70, 276), (300, 276)], False), 3)


@icon("flag")
def _flag(m):
    m.rect(76, 52, 20, 428, r=8)
    m.circle(86, 44, 22)
    xs = [94 + i * 20 for i in range(19)]
    top = [(x, 92 + 26 * math.sin((x - 94) * 0.0275)) for x in xs]
    bot = [(x, 282 + 26 * math.sin((x - 94) * 0.0275 + 0.45)) for x in xs]
    notch = ((top[-1][0] - 52), (top[-1][1] + bot[-1][1]) / 2)
    m.poly(top + [notch] + bot[::-1])
    for i in (4, 9, 14):
        x0, t0, b0 = xs[i], top[i][1], bot[i][1]
        m.cut(sm([(x0, t0 + 6), (x0 + 12, (t0 + b0) / 2), (x0, b0 - 6)], False, 0.5), 5)
    m.cut(sm([(108, 186), (200, 196), (300, 176), (400, 192)], False, 0.5), 4)
    for (x, y) in [(108, 112), (108, 262)]:
        cring(m, x, y, 6, 3)


@icon("candle")
def _candle(m):
    m.smooth([(256, 30), (292, 92), (300, 148), (256, 188), (212, 148), (220, 92)], close=True, t=0.5)         # alev
    m.smooth([(256, 92), (276, 128), (256, 164), (238, 128)], close=True, v=0, t=0.5)
    m.rect(251, 186, 10, 26, r=4)                                                                           # fitil
    m.rect(206, 208, 100, 200, r=16)                                                                       # mum
    for (x, y, r) in [(222, 214, 18), (262, 212, 16), (294, 216, 14)]:
        m.circle(x, y, r)
    m.rect(212, 214, 18, 82, r=9)
    m.cut(pl([(238, 236), (238, 380)], False), 6)
    m.cut(pl([(206, 214), (306, 214)], False), 3)
    m.rect(146, 402, 220, 28, r=12)                                                                        # tabla
    m.rect(224, 428, 64, 32, r=8)
    m.rect(168, 456, 176, 26, r=10)
    ring(m, 134, 424, 34, 16)
    m.cut(pl([(150, 416), (362, 416)], False), 4)


@icon("sun_disc")
def _sun(m):
    cx, cy = 256, 256
    for i in range(16):
        a = math.radians(i * 22.5 - 90)
        ca, sa = math.cos(a), math.sin(a)
        nx, ny = -sa, ca
        if i % 2 == 0:
            m.poly([(cx + 118 * ca + 24 * nx, cy + 118 * sa + 24 * ny), (cx + 238 * ca, cy + 238 * sa),
                    (cx + 118 * ca - 24 * nx, cy + 118 * sa - 24 * ny)])
        else:
            pts = []
            for k in range(9):
                r = 118 + k * 13
                off = 15 * math.sin(k * 1.35) * (1 - k / 14)
                pts.append((cx + r * ca + off * nx, cy + r * sa + off * ny))
            m.stroke(sk.smooth_path(pts, False, 0.5), 20)
    m.circle(cx, cy, 116)
    cring(m, cx, cy, 124, 7)
    cring(m, cx, cy, 100, 4)
    # yüz
    for sx in (-1, 1):
        m.oval(cx + sx * 36, 238, 17, 10, 0)
        cutl(m, [(cx + sx * 56, 214), (cx + sx * 34, 206), (cx + sx * 14, 214)], 5, smooth=True)
    cutl(m, [(cx, 232), (cx - 6, 278), (cx + 14, 284)], 6, smooth=True)
    m.cut(sm([(212, 312), (256, 326), (300, 312)], False, 0.5), 7)
    cutl(m, [(150, 196), (256, 176), (362, 196)], 5, smooth=True)
    for sx in (-1, 1):
        cring(m, cx + sx * 104, 268, 13, 4)


@icon("feather")
def _feather(m):
    spine = [(122, 438), (168, 332), (244, 216), (334, 124), (430, 58)]
    a, nr, ws = leaf(m, spine, 112, prof=lambda s: (math.sin(math.pi * min(1, s * 1.1 + 0.08)) ** 0.7) * (0.55 + 0.45 * (1 - abs(s - 0.45) * 1.4)), skew=0.18)
    m.stroke(sk.smooth_path([(122, 438), (100, 474), (84, 492)], False, 0.5), 14)                      # kalem ucu
    m.poly([(76, 506), (96, 480), (108, 494)])
    m.cut(sk.smooth_path(spine[:], False, 0.5), 6)
    n = len(a)
    for k in range(14):
        i = int((k + 1) / 15 * (n - 1))
        for sgn in (-1, 1):
            p0 = a[i]
            p1 = a[min(n - 1, i + 7)] + nr[i] * ws[i] * sgn * 0.92
            m.cut(pl([(float(p0[0]), float(p0[1])), (float(p1[0]), float(p1[1]))], False), 3)
    cutl(m, [(250, 232), (276, 236), (290, 216)], 6, smooth=True)                                    # tüy yarığı


@icon("bell")
def _bell(m):
    m.smooth([(256, 92), (300, 108), (324, 170), (336, 250), (364, 330), (404, 380), (424, 402), (88, 402), (108, 380), (148, 330),
              (176, 250), (188, 170), (212, 108)], close=True, t=0.4)
    m.rect(80, 384, 352, 36, r=16)
    m.rect(232, 94, 48, 38, r=8)
    ring(m, 256, 66, 30, 20)
    m.circle(256, 450, 28)
    m.cut(sm([(180, 300), (256, 312), (332, 300)], False, 0.5), 6)
    m.cut(sm([(150, 340), (256, 354), (362, 340)], False, 0.5), 6)
    m.cut(pl([(84, 384), (428, 384)], False), 5)
    cutl(m, [(214, 150), (206, 220), (192, 280)], 5, smooth=True)
    m.cut(pl([(256, 424), (256, 432)], False), 4)


@icon("ballot")
def _ballot(m):
    with xform(m, rot=-9, cx=256, cy=190):
        m.rect(176, 66, 160, 190, r=10)                          # oy pusulası
        for y in range(104, 200, 26):
            m.cut(pl([(200, y), (312, y)], False), 5)
        m.cut(sk.poly_path([(206, 218), (226, 238), (266, 190)], False), 8)     # onay işareti
    m.rect(84, 244, 344, 212, r=16)                              # kutu
    m.rect(68, 222, 376, 44, r=14)                               # kapak
    m.cut(pl([(70, 224), (442, 224)], False), 6)
    m.rect(160, 234, 192, 16, 0, r=8)                            # yuva
    rr_cut(m, 188, 316, 136, 96, 12, 5)
    m.cut(pl([(226, 346), (290, 386)], False), 7)
    m.cut(pl([(290, 346), (226, 386)], False), 7)
    for x in (110, 402):
        m.circle(x, 238, 6, 0)
        m.circle(x, 430, 6, 0)
    m.cut(pl([(84, 440), (428, 440)], False), 4)


@icon("gavel")
def _gavel(m):
    with xform(m, rot=-34, cx=256, cy=190):
        m.rect(104, 112, 304, 124, r=28)
        m.cut(pl([(158, 112), (158, 236)], False), 7)
        m.cut(pl([(354, 112), (354, 236)], False), 7)
        m.cut(pl([(120, 160), (392, 160)], False), 3)
        m.rect(236, 232, 42, 262, r=14)
        m.circle(257, 494, 24)
        m.cut(pl([(250, 300), (250, 440)], False), 4)
    m.rect(60, 432, 288, 44, r=14)
    m.cut(pl([(64, 454), (344, 454)], False), 4)
    m.rect(40, 470, 328, 20, r=8)


@icon("pillars")
def _pillars(m):
    for cx in (136, 376):
        m.rect(cx - 30, 124, 60, 312, r=8)                       # gövde
        m.rect(cx - 52, 98, 104, 34, r=8)                         # başlık
        m.rect(cx - 40, 76, 80, 28, r=8)
        m.rect(cx - 52, 428, 104, 34, r=8)                        # kaide
        m.rect(cx - 62, 456, 124, 22, r=8)
        for dx in (-14, 0, 14):
            m.cut(pl([(cx + dx, 140), (cx + dx, 422)], False), 4)
    # ruloyu andıran bant (PLUS ULTRA)
    top = [(92, 222), (150, 244), (214, 220), (256, 196), (298, 220), (362, 244), (420, 222)]
    bot = [(420, 270), (362, 294), (298, 268), (256, 244), (214, 268), (150, 294), (92, 270)]
    m.smooth(top + bot, close=True, t=0.45)
    m.cut(sm(top, False, 0.45), 6)
    m.cut(sm(bot, False, 0.45), 6)
    for i in range(6):
        x = 120 + i * 54
        m.cut(pl([(x, 244 + (i % 2) * 6), (x + 22, 250 - (i % 2) * 6)], False), 6)
    cutl(m, [(214, 220), (214, 268)], 4)
    cutl(m, [(298, 220), (298, 268)], 4)


@icon("cane")
def _cane(m):
    m.stroke(sk.smooth_path([(214, 470), (214, 330), (216, 190)], False, 0.4), 40)               # gövde
    m.stroke(sk.smooth_path([(216, 190), (214, 120), (252, 74), (314, 66), (366, 100), (368, 160)], False, 0.5), 44)   # kıvrık sap
    m.circle(368, 168, 24)
    m.rect(194, 440, 42, 44, r=10)                                # uç demiri
    m.rect(190, 196, 50, 26, r=8)                                 # halka
    m.rect(190, 246, 50, 18, r=8)
    m.cut(pl([(194, 462), (236, 462)], False), 5)
    m.cut(pl([(190, 209), (240, 209)], False), 4)
    cutl(m, [(206, 280), (206, 420)], 4)
    cutl(m, [(234, 120), (262, 90), (310, 82)], 4, smooth=True)
    m.circle(368, 168, 10, 0)


@icon("pickaxe")
def _pickaxe(m):
    with xform(m, rot=30, cx=256, cy=256):
        m.rect(234, 118, 44, 364, r=16)
        m.smooth([(40, 196), (96, 124), (176, 92), (256, 84), (336, 92), (416, 124), (472, 196), (410, 164), (336, 140), (256, 132),
                  (176, 140), (102, 164)], close=True, t=0.3)
        m.rect(218, 100, 76, 90, r=14)
        m.cut(pl([(218, 126), (294, 126)], False), 5)
        m.cut(pl([(218, 166), (294, 166)], False), 5)
        cutl(m, [(250, 210), (250, 450)], 4)
        cutl(m, [(70, 190), (140, 130), (250, 100)], 4, smooth=True)
        cutl(m, [(442, 190), (372, 130), (262, 100)], 4, smooth=True)


@icon("galley")
def _galley(m):
    m.smooth([(28, 326), (56, 390), (150, 418), (360, 418), (440, 394), (478, 352), (508, 336), (470, 328), (432, 338), (110, 342), (64, 330)], close=True, t=0.25)
    m.rect(38, 280, 78, 68, r=8)                                  # kıç kasarası
    m.rect(242, 72, 18, 276, r=5)                                 # direk
    m.line(104, 304, 438, 98, 13)                                 # lateen seren
    m.poly([(112, 300), (430, 106), (316, 340), (112, 340)])      # yelken
    m.poly([(252, 74), (322, 60), (252, 100)])                    # flama
    for i in range(8):                                            # kürekler
        x = 134 + i * 38
        m.line(x, 394, x - 34, 468, 9)
    m.cut(pl([(60, 350), (440, 350)], False), 5)
    for i in range(8):
        cring(m, 134 + i * 38, 394, 4, 3)
    for t in (0.3, 0.55, 0.78):
        x0 = 112 + (316 - 112) * t
        m.cut(pl([(112 + (430 - 112) * t, 300 + (106 - 300) * t + 10), (x0 + 6, 330)], False), 4)
    m.cut(pl([(122, 328), (310, 328)], False), 4)
    m.rect(52, 296, 18, 26, 0, r=4)
    m.rect(84, 296, 18, 26, 0, r=4)


@icon("litter")
def _litter(m):
    for x in (70, 442):                                                                              # taşıyıcılar (omuz sırık hizasında)
        m.circle(x, 292, 24)
        m.rect(x - 30, 330, 60, 104, r=20)
        m.rect(x - 28, 428, 24, 70, r=8)
        m.rect(x + 4, 428, 24, 70, r=8)
    m.smooth([(100, 200), (130, 150), (200, 112), (256, 94), (312, 112), (382, 150), (412, 200), (384, 190), (256, 168), (128, 190)], close=True, t=0.35)   # çatı
    m.circle(256, 82, 17)
    m.rect(150, 188, 212, 112, r=10)
    m.cut(pl([(146, 196), (366, 196)], False), 6)
    m.smooth([(192, 298), (192, 244), (214, 216), (256, 208), (298, 216), (320, 244), (320, 298)], close=True, v=0, t=0.4)   # açıklık
    m.smooth([(192, 298), (192, 252), (206, 234), (216, 272), (212, 298)], close=True, t=0.4)       # sol perde
    m.smooth([(320, 298), (320, 252), (306, 234), (296, 272), (300, 298)], close=True, t=0.4)       # sağ perde
    m.rect(158, 296, 18, 40, r=5)
    m.rect(336, 296, 18, 40, r=5)
    m.rect(22, 322, 468, 24, r=12)                                                                   # sırıklar
    m.circle(22, 334, 18)
    m.circle(490, 334, 18)
    for x in (70, 442):
        m.cut(pl([(x - 34, 322), (x + 34, 322)], False), 4)
        m.cut(pl([(x - 34, 346), (x + 34, 346)], False), 4)
        m.cut(pl([(x, 440), (x, 498)], False), 4)
    for x in (146, 366):
        m.cut(pl([(x, 204), (x + 4, 236)], False), 3)
    cutl(m, [(150, 138), (256, 110), (362, 138)], 4, smooth=True)


@icon("chains")
def _chains(m):
    n = 6
    ang = -52
    for i in range(n):
        t = i / (n - 1)
        cx, cy = 104 + 304 * t, 424 - 336 * t
        if i % 2 == 0:
            oval_stroke(m, cx, cy, 66, 36, 28, rot=ang)
        else:
            oval_rot(m, cx, cy, 68, 17, ang)
            m.c.save()
            m.c.translate(cx, cy)
            m.c.rotate(ang)
            m.c.drawLine(-52, 0, 52, 0, m._p(0, "stroke", 4))
            m.c.restore()


@icon("lightning")
def _lightning(m):
    m.poly([(318, 30), (132, 290), (234, 290), (184, 482), (392, 200), (288, 200), (360, 30)])
    m.cut(pl([(316, 62), (222, 290)], False), 5)
    m.cut(pl([(238, 302), (200, 440)], False), 5)
    m.cut(pl([(196, 270), (290, 270)], False), 0)
    for (x, y) in [(112, 120), (86, 170), (420, 330), (452, 290)]:
        m.poly([(x, y - 22), (x + 8, y - 6), (x + 24, y), (x + 8, y + 6), (x, y + 22), (x - 8, y + 6), (x - 24, y), (x - 8, y - 6)])


@icon("heart")
def _heart(m):
    pts = [(256, 448), (148, 362), (84, 286), (74, 208), (114, 142), (182, 124), (232, 150), (256, 192), (280, 150), (330, 124),
           (398, 142), (438, 208), (428, 286), (364, 362)]
    m.smooth(pts, close=True, t=0.4)
    cx, cy = 256, 270
    inner = [(cx + (x - cx) * 0.74, cy + (y - cy) * 0.74) for x, y in pts]
    m.cut(sm(inner, True, 0.4), 6)
    cutl(m, [(134, 190), (158, 160), (196, 150)], 8, smooth=True)


@icon("fist")
def _fist(m):
    m.rect(194, 384, 124, 100, r=20)                              # bilek
    m.rect(138, 226, 236, 176, r=58)                              # el sırtı/avuç
    for i in range(4):
        m.rect(138 + i * 59, 132, 60, 156, r=29)                  # parmak boğumları
    for x in (198, 256, 314):
        m.cut(pl([(x, 158), (x, 300)], False), 5)
    for i in range(4):
        m.cut(sm([(152 + i * 59, 214), (168 + i * 59, 222), (186 + i * 59, 214)], False, 0.5), 4)
    with xform(m, rot=-12, cx=256, cy=334):
        m.rect(134, 306, 236, 66, r=33)                           # başparmak
        rr_cut(m, 134, 306, 236, 66, 33, 5)
        m.cut(sm([(160, 330), (220, 322), (290, 326)], False, 0.5), 4)
    m.cut(pl([(206, 398), (306, 398)], False), 4)


@icon("mountain")
def _mountain(m):
    m.smooth([(20, 458), (80, 392), (136, 330), (186, 262), (224, 182), (258, 110), (282, 66), (312, 124), (346, 196), (392, 272), (444, 352), (496, 458)], close=True, t=0.12)
    m.smooth([(8, 458), (66, 360), (112, 308), (170, 380), (240, 458)], close=True, t=0.15)
    m.smooth([(300, 458), (372, 370), (432, 314), (490, 388), (508, 458)], close=True, t=0.15)
    m.rect(8, 440, 500, 36, r=12)
    cutl(m, [(282, 70), (262, 142), (292, 204), (250, 282), (286, 356), (240, 440)], 6, smooth=True)       # ana sırt
    for k in range(7):                                                                                     # gölge tarafı taraması
        y = 150 + k * 40
        x0 = 296 + k * 14
        m.cut(pl([(x0, y), (x0 + 26 + k * 4, y + 22)], False), 5)
    cutl(m, [(112, 310), (140, 360), (130, 420)], 4, smooth=True)
    cutl(m, [(432, 316), (410, 372), (426, 430)], 4, smooth=True)
    m.cut(sm([(212, 210), (240, 226), (262, 206)], False, 0.5), 4)
    # kıvrımlı yol + galeri girişleri
    cutl(m, [(150, 438), (200, 402), (170, 372), (222, 340), (196, 306), (240, 278)], 5, smooth=True)
    for (x, y) in [(330, 412), (206, 400)]:
        m.rect(x - 20, y - 22, 40, 44, 0, r=4)
        m.cut(pl([(x - 26, y - 24), (x + 26, y - 24)], False), 5)


@icon("elector_hat")
def _elector_hat(m):
    m.smooth([(108, 330), (122, 236), (186, 158), (256, 132), (326, 158), (390, 236), (404, 330)], close=True, t=0.4)       # kubbe
    m.rect(66, 312, 380, 112, r=50)                               # ermin kenar
    m.circle(256, 114, 20)
    m.rect(250, 70, 12, 40, r=4)
    m.rect(236, 80, 40, 12, r=4)
    cutl(m, [(256, 134), (206, 220), (164, 310)], 6, smooth=True)
    cutl(m, [(256, 134), (306, 220), (348, 310)], 6, smooth=True)
    cutl(m, [(256, 134), (256, 310)], 5)
    m.cut(pl([(84, 322), (428, 322)], False), 5)
    for i in range(6):                                            # ermin kuyrukları
        x = 110 + i * 58
        m.smooth([(x, 346), (x + 12, 346), (x + 14, 372), (x + 6, 396), (x - 2, 372)], close=True, v=0, t=0.4)
    m.cut(pl([(84, 424), (428, 424)], False), 4)


@icon("foot_gout")
def _foot(m):
    # çıplak ayak (yandan): topuk solda, parmaklar sağda; kemer kavisli
    m.smooth([(150, 150), (262, 132), (284, 212), (340, 258), (410, 282), (462, 306), (492, 346), (484, 386), (440, 404), (380, 400),
              (330, 384), (270, 372), (216, 392), (160, 408), (122, 382), (114, 300), (130, 214)], close=True, t=0.4)
    m.rect(138, 96, 126, 74, r=24)                                # bilek
    m.circle(408, 292, 34)                                        # şişmiş eklem
    m.circle(462, 350, 36)                                        # başparmak
    for (x, y, r) in [(414, 372, 22), (372, 366, 19)]:           # diğer parmaklar
        m.circle(x, y, r)
    for (x, y, s_) in [(404, 196, 1.0), (346, 214, 0.74), (456, 224, 0.7)]:
        m.smooth([(x + 4 * s_, y - 84 * s_), (x + 30 * s_, y - 40 * s_), (x + 24 * s_, y + 8 * s_), (x, y + 30 * s_), (x - 24 * s_, y + 8 * s_),
                  (x - 26 * s_, y - 24 * s_), (x - 6 * s_, y - 40 * s_)], close=True, t=0.5)
        m.smooth([(x + 2 * s_, y - 36 * s_), (x + 12 * s_, y - 8 * s_), (x, y + 12 * s_), (x - 12 * s_, y - 8 * s_)], close=True, v=0, t=0.5)
    for k in range(4):                                            # bandaj
        m.cut(pl([(140, 130 + k * 24), (258, 114 + k * 24)], False), 6)
    cring(m, 408, 292, 34, 4)
    cring(m, 462, 350, 36, 4)
    cring(m, 414, 372, 22, 3)
    cutl(m, [(150, 346), (214, 384), (300, 380)], 4, smooth=True)
    for a in range(7):                                            # şişlik ışınları
        ang = math.radians(-100 + a * 24)
        m.cut(pl([(408 + 42 * math.cos(ang), 292 + 42 * math.sin(ang)), (408 + 56 * math.cos(ang), 292 + 56 * math.sin(ang))], False), 4)


@icon("bed")
def _bed(m):
    m.rect(84, 60, 344, 52, r=12)                                 # tepelik
    for i in range(10):                                           # saçak
        m.poly([(94 + i * 33.5, 108), (118 + i * 33.5, 108), (106 + i * 33.5, 134)])
    m.rect(90, 60, 28, 420, r=8)                                  # direkler
    m.rect(394, 60, 28, 420, r=8)
    m.smooth([(118, 112), (186, 130), (172, 240), (146, 322), (118, 326)], close=True, t=0.4)        # sol perde
    m.smooth([(394, 112), (326, 130), (340, 240), (366, 322), (394, 326)], close=True, t=0.4)        # sağ perde
    m.rect(118, 330, 276, 76, r=16)                               # yatak
    m.oval(190, 330, 62, 26)                                      # yastık
    m.rect(104, 406, 304, 56, r=12)                               # ayak ucu
    cutl(m, [(150, 140), (150, 300)], 4, smooth=True)
    cutl(m, [(364, 140), (364, 300)], 4, smooth=True)
    m.cut(sm([(128, 360), (256, 372), (386, 358)], False, 0.5), 5)
    m.cut(pl([(104, 410), (408, 410)], False), 5)
    m.cut(pl([(84, 112), (428, 112)], False), 5)
    m.cut(pl([(118, 330), (394, 330)], False), 4)


@icon("tent")
def _tent(m):
    m.smooth([(256, 74), (230, 130), (176, 190), (100, 238), (412, 238), (336, 190), (282, 130)], close=True, t=0.3)    # çatı
    m.rect(110, 232, 292, 176, r=8)                               # gövde
    m.circle(256, 56, 14)                                         # alem topu
    ring(m, 256, 36, 18, 8)
    for i in range(10):                                           # saçak
        m.oval(118 + i * 30, 242, 16, 12, 0)
    m.smooth([(212, 408), (212, 336), (232, 302), (256, 294), (280, 302), (300, 336), (300, 408)], close=True, v=0, t=0.4)    # giriş
    m.cut(pl([(112, 276), (400, 276)], False), 5)
    m.cut(pl([(112, 292), (400, 292)], False), 3)
    cutl(m, [(256, 80), (230, 160), (170, 214)], 4, smooth=True)
    cutl(m, [(256, 80), (282, 160), (342, 214)], 4, smooth=True)
    m.line(110, 236, 40, 440, 9)                                  # ip ve kazıklar
    m.line(402, 236, 472, 440, 9)
    m.poly([(26, 452), (54, 452), (40, 430)])
    m.poly([(458, 452), (486, 452), (472, 430)])
    m.cut(pl([(110, 408), (402, 408)], False), 5)


@icon("ladder")
def _ladder(m):
    m.rect(344, 52, 142, 424, r=6)                                # sur
    for k in range(4):
        m.rect(344 + k * 38, 28, 26, 40)
    m.cut(pl([(344, 140), (486, 140)], False), 4)
    m.cut(pl([(344, 300), (486, 300)], False), 4)
    with xform(m, rot=-16, cx=230, cy=270):
        for x in (150, 298):
            m.rect(x, 50, 26, 440, r=8)
        for y in range(92, 470, 52):
            m.rect(156, y, 164, 20, r=6)
        m.rect(138, 40, 62, 22, r=8)
        m.rect(286, 40, 62, 22, r=8)
    cutl(m, [(340, 60), (340, 470)], 7)
    m.cut(pl([(30, 480), (320, 480)], False), 0)


@icon("crown_cracked")
def _crown_cracked(m):
    crack = [(262, -10), (236, 110), (280, 196), (240, 290), (272, 376), (244, 470), (252, 522)]
    right = crack + [(522, 522), (522, -10)]
    rp = skia.Path()
    rp.moveTo(*right[0])
    for q in right[1:]:
        rp.lineTo(*q)
    rp.close()
    left = [(-10, -10)] + crack + [(-10, 522)]
    lp = skia.Path()
    lp.moveTo(*left[0])
    for q in left[1:]:
        lp.lineTo(*q)
    lp.close()
    with clipm(m, lp):
        icons._icrown(m)
    with clipm(m, rp):
        with xform(m, tx=12, ty=18, cx=256, cy=256):
            icons._icrown(m)
    m.cut(sm(crack, False, 0.0), 11)


@icon("sack")
def _sack(m):
    m.smooth([(256, 160), (332, 176), (402, 262), (424, 362), (384, 442), (256, 466), (128, 442), (88, 362), (110, 262), (180, 176)], close=True, t=0.5)
    m.smooth([(198, 96), (230, 64), (256, 84), (284, 62), (316, 96), (306, 160), (206, 160)], close=True, t=0.4)       # büzülmüş ağız
    cutl(m, [(186, 162), (256, 176), (326, 160)], 11, smooth=True)                                                    # ip bağı
    m.stroke(sk.smooth_path([(256, 170), (232, 200), (236, 230)], False, 0.5), 12)                                  # ip ucu
    m.stroke(sk.smooth_path([(262, 172), (288, 196), (284, 226)], False, 0.5), 12)
    rr_cut(m, 150, 300, 88, 80, 6, 4)                              # yama
    for k in range(4):
        m.cut(pl([(150, 316 + k * 18), (238, 316 + k * 18)], False), 0)
    for y in (230, 280, 330, 380, 420):                           # dikiş
        m.cut(pl([(338 + (y - 230) * 0.12, y), (350 + (y - 230) * 0.12, y + 14)], False), 4)
    cutl(m, [(180, 210), (150, 280), (140, 340)], 4, smooth=True)
    cutl(m, [(270, 330), (306, 386), (296, 440)], 4, smooth=True)


@icon("book_open")
def _book_open(m):
    # kapak + sayfalar
    m.smooth([(34, 152), (130, 128), (256, 164), (382, 128), (478, 152), (478, 404), (382, 382), (256, 424), (130, 382), (34, 404)], close=True, t=0.25)
    m.cut(sm([(58, 142), (140, 120), (256, 156), (372, 120), (454, 142)], False, 0.5), 4)
    m.cut(pl([(256, 164), (256, 424)], False), 8)
    for i in range(7):                                            # satırlar (kavisli)
        y = 190 + i * 28
        m.cut(sm([(76, y - 16), (150, y - 22), (232, y + 10)], False, 0.5), 5)
        m.cut(sm([(280, y + 10), (362, y - 22), (436, y - 16)], False, 0.5), 5)
    for i in range(4):                                            # sayfa kenarları
        y = 404 + i * 9
        m.cut(sm([(48, y - 12), (130, y - 18), (256, y + 24 + i * 2)], False, 0.5), 3)
        m.cut(sm([(256, y + 24 + i * 2), (382, y - 18), (464, y - 12)], False, 0.5), 3)
    m.poly([(240, 424), (272, 424), (272, 496), (256, 478), (240, 496)])          # şerit


# ═════════════════════════════ takma adlar + önizleme ═════════════════════════════
icons._ICONS["gun"] = icons._ICONS["arquebus"]
icons._ICONS["sun"] = icons._ICONS["sun_disc"]


def sheet(keys=None, metals=("gold",), cols=8, size=200, out="out/frames/icons_extra_sheet.png"):
    keys = keys or NEW
    rows = (len(keys) + cols - 1) // cols
    img = np.zeros((rows * size, cols * size, 3), np.uint8)
    img[:] = (28, 18, 12)
    for i, k in enumerate(keys):
        a = cv2.resize(icons.icon_array(k, metals[i % len(metals)]), (size, size), interpolation=cv2.INTER_AREA)
        al = a[..., 3:4].astype(np.float32) / 255
        r, c = divmod(i, cols)
        sl = img[r * size:(r + 1) * size, c * size:(c + 1) * size]
        sl[:] = (sl * (1 - al) + a[..., :3] * al).astype(np.uint8)
    cv2.imwrite(out, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    return out
