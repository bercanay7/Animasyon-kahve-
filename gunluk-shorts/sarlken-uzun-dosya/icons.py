"""Kabartmalı metal/emaye simgeler: maske (beyaz şekil + siyah kesikler) → relief_sprite → önbellekli skia.Image.

    img = icon_image("crown", metal="gold", size=256)      # RGBA, 256 px
    f.image(img, x, y, sx=0.8, ax=.5, ay=.5)
Yeni simge: @icon("ad") ile 512×512 tuvale beyaz dolgu/siyah (silinen) çizgi çizen fonksiyon yaz (merkez 256,256).
"""
import math
from functools import lru_cache

import numpy as np
import skia

import sk
from sk import np_to_image, relief_sprite

N = 512
_ICONS = {}

# ek metal rampaları (emaye/boyalı görünüm)
sk.METAL.update(dict(
    crimson=[("#2E0A0E", 0.0), ("#8E1F26", 0.32), ("#E26A5A", 0.55), ("#8E1F26", 0.78), ("#3A0D12", 1.0)],
    royal=[("#0E1A3A", 0.0), ("#27427A", 0.32), ("#6C92E0", 0.55), ("#27427A", 0.78), ("#0E1A3A", 1.0)],
    forest=[("#0E2414", 0.0), ("#2F5232", 0.32), ("#7FBF74", 0.55), ("#2F5232", 0.78), ("#0E2414", 1.0)],
    violet=[("#1E1030", 0.0), ("#4B2D63", 0.32), ("#A67DD0", 0.55), ("#4B2D63", 0.78), ("#1E1030", 1.0)],
    onyx=[("#050505", 0.0), ("#26211E", 0.4), ("#7A7068", 0.58), ("#26211E", 0.8), ("#050505", 1.0)],
    teal=[("#07262C", 0.0), ("#1E5560", 0.32), ("#6CC4CE", 0.55), ("#1E5560", 0.78), ("#07262C", 1.0)],
))


def icon(name):
    def deco(fn):
        _ICONS[name] = fn
        return fn
    return deco


class _M:
    """Maske tuvali: fill() beyaz, cut() siyah (oyuk)."""

    def __init__(self):
        self.s = skia.Surface(N, N)
        self.c = self.s.getCanvas()
        self.c.clear(skia.ColorBLACK)

    def _p(self, v, style="fill", w=1.0, blur=0):
        p = skia.Paint(AntiAlias=True, Color=skia.Color(v, v, v, 255))
        if style == "stroke":
            p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(w); p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
        if blur:
            p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
        return p

    def fill(self, path, v=255):
        self.c.drawPath(path, self._p(v))

    def stroke(self, path, w=8, v=255):
        self.c.drawPath(path, self._p(v, "stroke", w))

    def cut(self, path, w=0):
        if w:
            self.c.drawPath(path, self._p(0, "stroke", w))
        else:
            self.c.drawPath(path, self._p(0))

    def line(self, x0, y0, x1, y1, w=8, v=255):
        self.c.drawLine(x0, y0, x1, y1, self._p(v, "stroke", w))

    def circle(self, x, y, r, v=255):
        self.c.drawCircle(x, y, r, self._p(v))

    def oval(self, x, y, rx, ry, v=255):
        self.c.drawOval(skia.Rect.MakeLTRB(x - rx, y - ry, x + rx, y + ry), self._p(v))

    def rect(self, x, y, w, h, v=255, r=0):
        if r:
            self.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), self._p(v))
        else:
            self.c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), self._p(v))

    def poly(self, pts, v=255, close=True):
        self.fill(sk.poly_path(pts, close), v)

    def smooth(self, pts, v=255, close=True, t=0.5):
        self.fill(sk.smooth_path(pts, close, t), v)

    def arr(self):
        return self.s.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)[..., 0].astype(np.float32) / 255.0


def P(*pts):
    return list(pts)


# ───────────────────────────── simgeler ─────────────────────────────
@icon("crown")
def _crown(m):
    m.smooth([(96, 380), (96, 300), (130, 170), (190, 270), (256, 130), (322, 270), (382, 170), (416, 300), (416, 380)], close=True, t=0.25)
    m.rect(92, 360, 328, 56, r=14)
    for x, y in [(130, 160), (256, 118), (382, 160)]:
        m.circle(x, y, 20)
    m.rect(247, 66, 18, 52)
    m.rect(228, 82, 56, 16)
    m.cut(sk.smooth_path([(120, 388), (256, 372), (392, 388)], False), 8)
    for x in (170, 256, 342):
        m.circle(x, 392, 11, 0)
    m.cut(sk.smooth_path([(150, 340), (256, 322), (362, 340)], False), 6)


@icon("imperial_crown")
def _icrown(m):
    _crown(m)
    m.stroke(sk.smooth_path([(128, 196), (180, 90), (256, 56), (332, 90), (384, 196)], False, 0.5), 20)
    m.circle(256, 50, 24)
    m.rect(247, 4, 18, 40)
    m.rect(232, 14, 48, 14)


@icon("cross")
def _cross(m):
    m.rect(226, 70, 60, 372, r=8)
    m.rect(120, 150, 272, 56, r=8)
    for (x, y) in [(256, 70), (256, 442), (120, 178), (392, 178)]:
        m.circle(x, y, 26)


@icon("crescent")
def _crescent(m):
    outer = skia.Path(); outer.addCircle(240, 256, 190)
    inner = skia.Path(); inner.addCircle(300, 240, 160)
    path = skia.Op(outer, inner, skia.PathOp.kDifference_PathOp)
    m.fill(path)
    star = [(380 + (60 if i % 2 == 0 else 24) * math.cos(math.pi * i / 5 - math.pi / 2), 250 + (60 if i % 2 == 0 else 24) * math.sin(math.pi * i / 5 - math.pi / 2)) for i in range(10)]
    m.poly(star)


@icon("fleur")
def _fleur(m):
    m.smooth([(256, 56), (292, 130), (292, 250), (256, 330), (220, 250), (220, 130)], close=True, t=0.5)
    for sgn in (-1, 1):
        m.smooth([(256 + sgn * 24, 300), (256 + sgn * 130, 270), (256 + sgn * 190, 200), (256 + sgn * 200, 150), (256 + sgn * 160, 120),
                  (256 + sgn * 130, 160), (256 + sgn * 120, 210), (256 + sgn * 70, 250), (256 + sgn * 30, 262)], close=True, t=0.4)
        m.smooth([(256 + sgn * 40, 330), (256 + sgn * 120, 340), (256 + sgn * 160, 400), (256 + sgn * 130, 450), (256 + sgn * 90, 420), (256 + sgn * 60, 390)], close=True, t=0.4)
    m.rect(176, 318, 160, 34, r=10)
    m.smooth([(224, 352), (288, 352), (300, 440), (256, 470), (212, 440)], close=True, t=0.4)
    m.cut(sk.smooth_path([(256, 90), (256, 250)], False), 5)


@icon("castle")
def _castle(m):
    m.rect(130, 230, 252, 200)
    for x in (120, 214, 308):
        m.rect(x, 150, 84, 120)
        for k in range(4):
            m.rect(x + k * 24 - 2, 124, 16, 40)
    for k in range(3):
        m.rect(176 + k * 54, 200, 24, 38)
    m.cut(sk.poly_path([(220, 430), (220, 350), (256, 320), (292, 350), (292, 430)], True))
    for x in (160, 340):
        m.cut(sk.poly_path([(x, 330), (x, 290), (x + 16, 276), (x + 32, 290), (x + 32, 330)], True))
    m.cut(sk.poly_path([(150, 230), (362, 230)], False), 5)


@icon("coin")
def _coin(m):
    m.circle(256, 256, 196)
    ring = skia.Path(); ring.addCircle(256, 256, 166)
    m.cut(ring, 10)
    ring2 = skia.Path(); ring2.addCircle(256, 256, 184)
    m.cut(ring2, 4)
    # zambak
    m.c.save(); m.c.translate(256, 262); m.c.scale(0.62, 0.62); m.c.translate(-256, -256)
    _fleur(m)
    m.c.restore()
    for i in range(24):
        a = math.radians(i * 15)
        m.circle(256 + 176 * math.cos(a), 256 + 176 * math.sin(a), 6, 0)


@icon("coins")
def _coins(m):
    for i, (x, y) in enumerate([(256, 400), (256, 350), (256, 300), (256, 250), (256, 200)]):
        m.oval(x, y, 150, 44)
        m.cut(sk.poly_path([(106, y), (406, y)], False), 5)
    m.oval(256, 190, 150, 44)
    m.oval(256, 190, 114, 30, 0)
    m.oval(256, 190, 100, 24)
    m.oval(120, 440, 90, 28)
    m.oval(360, 450, 96, 30)


@icon("coinbag")
def _bag(m):
    m.smooth([(256, 90), (330, 110), (396, 220), (410, 330), (380, 420), (256, 450), (132, 420), (102, 330), (116, 220), (182, 110)], close=True, t=0.5)
    m.smooth([(190, 96), (256, 66), (322, 96), (300, 128), (256, 118), (212, 128)], close=True)
    m.cut(sk.smooth_path([(190, 130), (256, 150), (322, 130)], False), 10)
    m.cut(sk.smooth_path([(190, 300), (256, 320), (322, 300)], False), 0)
    m.smooth([(256, 230), (274, 270), (256, 330), (238, 270)], close=True, v=0)
    m.oval(256, 280, 18, 44, 255)
    m.cut(sk.smooth_path([(256, 250), (256, 320)], False), 6)


@icon("monk")
def _monk(m):
    m.smooth([(256, 70), (330, 100), (356, 190), (340, 260), (400, 330), (420, 460), (92, 460), (112, 330), (172, 260), (156, 190), (182, 100)], close=True, t=0.5)
    m.smooth([(256, 150), (300, 170), (310, 230), (256, 270), (202, 230), (212, 170)], close=True, v=0)
    m.circle(256, 218, 38)
    m.cut(sk.smooth_path([(240, 212), (252, 218)], False), 5)
    m.cut(sk.smooth_path([(262, 212), (274, 218)], False), 5)
    m.cut(sk.smooth_path([(240, 242), (256, 250), (272, 242)], False), 4)
    m.rect(240, 330, 32, 100)
    m.rect(206, 362, 100, 28)
    m.cut(sk.smooth_path([(256, 260), (256, 330)], False), 0)


@icon("scroll")
def _scroll(m):
    m.rect(120, 110, 272, 292, r=10)
    for x in (120, 392):
        m.oval(x, 110, 24, 40)
        m.oval(x, 402, 24, 40)
    m.cut(sk.poly_path([(120, 110), (392, 110)], False), 4)
    for i in range(7):
        m.cut(sk.poly_path([(160, 170 + i * 32), (352 - (60 if i == 6 else 0), 170 + i * 32)], False), 7)
    m.circle(350, 380, 40)
    m.circle(350, 380, 24, 0)
    m.circle(350, 380, 14)


@icon("sword")
def _sword(m):
    m.poly([(256, 40), (284, 110), (278, 360), (234, 360), (228, 110)])
    m.cut(sk.poly_path([(256, 70), (256, 350)], False), 6)
    m.rect(150, 360, 212, 30, r=12)
    m.rect(240, 390, 32, 90, r=10)
    m.circle(256, 494, 22)


@icon("swords")
def _swords(m):
    for ang in (-35, 35):
        m.c.save()
        m.c.translate(256, 256)
        m.c.rotate(ang)
        m.c.scale(0.92, 0.92)
        m.c.translate(-256, -256)
        _sword(m)
        m.c.restore()


@icon("ship")
def _ship(m):
    # gövde (kıç kasarası + pruva)
    m.smooth([(34, 330), (60, 420), (130, 456), (390, 456), (456, 410), (476, 300), (440, 318), (418, 372), (370, 392), (150, 392), (96, 372), (70, 320)], close=True, t=0.3)
    m.rect(344, 318, 96, 40, r=6)             # kıç kasarası
    m.rect(48, 336, 70, 30, r=6)               # pruva kasarası
    m.cut(sk.poly_path([(96, 424), (420, 424)], False), 5)
    # direk ve yelkenler (aralarında boşluk)
    m.rect(250, 70, 12, 330)
    m.rect(140, 160, 10, 230)
    m.rect(362, 180, 10, 210)
    m.smooth([(172, 118), (344, 114), (352, 236), (256, 262), (162, 236)], close=True, t=0.55)        # ana yelken
    m.smooth([(196, 60), (316, 58), (322, 106), (256, 118), (190, 106)], close=True, t=0.55)           # üst yelken
    m.smooth([(66, 180), (122, 176), (130, 266), (98, 280), (62, 262)], close=True, t=0.5)
    m.smooth([(380, 196), (452, 192), (456, 268), (418, 284), (376, 268)], close=True, t=0.5)
    m.cut(sk.smooth_path([(258, 122), (258, 252)], False), 5)
    m.cut(sk.smooth_path([(214, 120), (212, 240)], False), 3)
    m.cut(sk.smooth_path([(302, 120), (304, 240)], False), 3)
    m.cut(sk.poly_path([(176, 168), (340, 164)], False), 4)
    m.poly([(262, 66), (350, 44), (330, 76), (350, 100), (262, 92)])      # flama


@icon("skull")
def _skull(m):
    m.smooth([(256, 70), (352, 100), (390, 190), (370, 270), (336, 310), (330, 380), (182, 380), (176, 310), (142, 270), (122, 190), (160, 100)], close=True, t=0.5)
    m.oval(206, 210, 38, 44, 0)
    m.oval(306, 210, 38, 44, 0)
    m.poly([(256, 250), (236, 296), (276, 296)], 0)
    for x in (212, 240, 268, 296):
        m.rect(x - 4, 340, 8, 40, 0)
    m.line(120, 430, 392, 480, 22)
    m.line(392, 430, 120, 480, 22)


@icon("ring")
def _ring(m):
    for cx in (200, 312):
        r = skia.Path(); r.addCircle(cx, 280, 120)
        m.stroke(r, 34)
    m.poly([(256, 120), (300, 160), (256, 210), (212, 160)])
    m.cut(sk.poly_path([(256, 130), (256, 200)], False), 4)


@icon("keys")
def _keys(m):
    for ang in (-32, 32):
        m.c.save()
        m.c.translate(256, 256)
        m.c.rotate(ang)
        m.c.translate(-256, -256)
        r = skia.Path(); r.addCircle(256, 120, 62)
        m.stroke(r, 30)
        m.rect(242, 170, 28, 270, r=6)
        m.rect(270, 380, 60, 24)
        m.rect(270, 420, 44, 22)
        m.c.restore()


@icon("book")
def _book(m):
    m.smooth([(256, 150), (180, 120), (80, 128), (70, 380), (180, 372), (256, 400)], close=True, t=0.3)
    m.smooth([(256, 150), (332, 120), (432, 128), (442, 380), (332, 372), (256, 400)], close=True, t=0.3)
    m.cut(sk.poly_path([(256, 150), (256, 400)], False), 6)
    for i in range(6):
        m.cut(sk.poly_path([(100, 170 + i * 30), (232, 184 + i * 30)], False), 5)
        m.cut(sk.poly_path([(280, 184 + i * 30), (412, 170 + i * 30)], False), 5)


@icon("tower")
def _tower(m):
    m.rect(176, 140, 160, 330)
    m.rect(156, 100, 200, 56)
    for k in range(5):
        m.rect(156 + k * 44, 70, 24, 44)
    m.cut(sk.poly_path([(230, 470), (230, 380), (256, 350), (282, 380), (282, 470)], True))
    m.cut(sk.poly_path([(240, 230), (240, 190), (256, 176), (272, 190), (272, 230)], True))
    for y in (260, 310):
        m.cut(sk.poly_path([(200, y), (312, y)], False), 5)


@icon("cannon")
def _cannon(m):
    m.smooth([(70, 250), (390, 190), (440, 200), (440, 270), (390, 280), (70, 310)], close=True, t=0.3)
    m.rect(396, 186, 30, 100, r=8)
    m.circle(190, 380, 80)
    m.circle(190, 380, 56, 0)
    m.circle(190, 380, 22)
    for a in range(0, 360, 45):
        m.line(190, 380, 190 + 56 * math.cos(math.radians(a)), 380 + 56 * math.sin(math.radians(a)), 6)
    m.rect(150, 300, 160, 28)


@icon("eagle")
def _eagle(m):
    # çift başlı kartal (sade, tanınır siluet)
    m.smooth([(256, 190), (310, 230), (330, 330), (300, 420), (256, 450), (212, 420), (182, 330), (202, 230)], close=True, t=0.5)
    for sgn in (-1, 1):
        # kanat: kademeli tüy katmanları
        for k, (dy, ln) in enumerate([(0, 210), (36, 190), (72, 168), (108, 142)]):
            pts = [(256 + sgn * 40, 240 + dy), (256 + sgn * 110, 190 + dy * 0.6), (256 + sgn * (ln + 20), 170 + dy * 0.5),
                   (256 + sgn * ln, 214 + dy * 0.6), (256 + sgn * (ln - 14), 260 + dy * 0.7), (256 + sgn * (ln - 40), 296 + dy * 0.7),
                   (256 + sgn * 90, 300 + dy * 0.5)]
            m.smooth(pts, close=True, t=0.35)
            m.cut(sk.smooth_path([(256 + sgn * 50, 262 + dy), (256 + sgn * (ln - 6), 232 + dy * 0.6)], False), 4)
        # baş
        hx = 256 + sgn * 78
        m.smooth([(256 + sgn * 22, 236), (hx - sgn * 8, 186), (hx, 140), (hx + sgn * 18, 112), (hx + sgn * 52, 126), (hx + sgn * 34, 144), (hx + sgn * 20, 160), (hx + sgn * 24, 198), (256 + sgn * 46, 240)], close=True, t=0.45)
        m.circle(hx + sgn * 12, 138, 4.5, 0)
    # kuyruk
    for k in range(5):
        a = math.radians(-20 + k * 10)
        m.line(256, 420, 256 + 90 * math.sin(a), 420 + 70 * math.cos(a), 22)
    # taç
    m.smooth([(222, 110), (222, 80), (240, 94), (256, 66), (272, 94), (290, 80), (290, 110)], close=True, t=0.2)
    m.cut(sk.poly_path([(222, 108), (290, 108)], False), 4)
    # pençe
    for sgn in (-1, 1):
        m.line(256 + sgn * 54, 400, 256 + sgn * 100, 452, 10)
        for q in (-1, 0, 1):
            m.line(256 + sgn * 100, 452, 256 + sgn * (100 + 22 * (q + 1)), 460 + q * 8, 7)
    m.cut(sk.smooth_path([(256, 220), (256, 430)], False), 4)


@icon("shield")
def _shield(m):
    m.smooth([(100, 90), (412, 90), (412, 260), (380, 360), (256, 450), (132, 360), (100, 260)], close=True, t=0.35)


@icon("scales")
def _scales(m):
    m.rect(246, 90, 20, 330)
    m.rect(150, 100, 212, 14, r=6)
    m.rect(190, 410, 132, 24, r=10)
    for sgn in (-1, 1):
        cx = 256 + sgn * 130
        m.line(cx, 108, cx - 52, 250, 5)
        m.line(cx, 108, cx + 52, 250, 5)
        m.smooth([(cx - 66, 250), (cx + 66, 250), (cx + 44, 296), (cx - 44, 296)], close=True, t=0.2)
    m.circle(256, 96, 22)


@icon("hourglass")
def _hourglass(m):
    m.rect(120, 76, 272, 28, r=8)
    m.rect(120, 408, 272, 28, r=8)
    m.smooth([(140, 104), (372, 104), (290, 256), (372, 408), (140, 408), (222, 256)], close=True, t=0.1)
    m.poly([(210, 360), (302, 360), (256, 300)], 0)
    m.poly([(240, 230), (272, 230), (256, 256)], 0)
    m.cut(sk.poly_path([(256, 256), (256, 350)], False), 5)


@icon("quill")
def _quill(m):
    m.smooth([(430, 60), (340, 120), (240, 230), (170, 340), (150, 430), (200, 360), (270, 280), (340, 200), (410, 130)], close=True, t=0.4)
    m.cut(sk.smooth_path([(420, 70), (300, 190), (170, 400)], False), 5)
    for k in range(7):
        t = k / 6
        m.cut(sk.poly_path([(400 - 230 * t, 90 + 280 * t), (340 - 190 * t, 140 + 280 * t)], False), 3)
    m.poly([(150, 430), (120, 480), (170, 450)])


@icon("torch")
def _torch(m):
    m.rect(236, 220, 40, 250, r=10)
    m.smooth([(256, 40), (320, 120), (330, 190), (256, 240), (182, 190), (192, 120)], close=True, t=0.5)
    m.smooth([(256, 110), (292, 160), (256, 210), (222, 160)], close=True, v=0)
    m.rect(200, 206, 112, 26, r=10)


@icon("anchor")
def _anchor(m):
    r = skia.Path(); r.addCircle(256, 90, 40)
    m.stroke(r, 22)
    m.rect(246, 130, 20, 300)
    m.rect(176, 170, 160, 20, r=8)
    m.stroke(sk.smooth_path([(96, 330), (150, 450), (256, 460), (362, 450), (416, 330)], False, 0.4), 24)
    m.poly([(70, 320), (130, 310), (110, 366)])
    m.poly([(442, 320), (382, 310), (402, 366)])


@icon("pyramid")
def _pyr(m):
    m.poly([(60, 440), (130, 380), (180, 330), (230, 280), (256, 120), (282, 280), (332, 330), (382, 380), (452, 440)])
    for y in (380, 330, 280):
        m.cut(sk.poly_path([(100, y + 10), (412, y + 10)], False), 4)
    m.cut(sk.poly_path([(244, 440), (244, 360), (268, 360), (268, 440)], True))
    m.rect(232, 108, 48, 30, r=4)


@icon("family")
def _family(m):
    m.line(256, 110, 256, 240, 12)
    m.line(120, 240, 392, 240, 12)
    for x in (120, 256, 392):
        m.line(x, 240, x, 320, 12)
        m.circle(x, 370, 54)
    m.circle(256, 90, 48)


@icon("question")
def _question(m):
    m.stroke(sk.smooth_path([(150, 170), (170, 110), (256, 86), (340, 112), (352, 180), (320, 240), (270, 280), (256, 330)], False, 0.5), 46)
    m.circle(256, 430, 30)


@icon("star")
def _star(m):
    pts = [(256 + (200 if i % 2 == 0 else 84) * math.cos(math.pi * i / 4 - math.pi / 2), 256 + (200 if i % 2 == 0 else 84) * math.sin(math.pi * i / 4 - math.pi / 2)) for i in range(16)]
    m.poly(pts)
    m.circle(256, 256, 34, 0)


@icon("laurel")
def _laurel(m):
    cx, cy, R = 256, 270, 170
    for sgn in (-1, 1):
        for k in range(11):
            t = k / 10
            ang = math.radians(100 + t * 150) if sgn < 0 else math.radians(80 - t * 150)
            x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
            tang = ang + (math.pi / 2 if sgn < 0 else -math.pi / 2)
            for off in (-1, 1):
                m.c.save(); m.c.translate(x, y); m.c.rotate(math.degrees(tang) + off * 38)
                m.oval(0, -26, 16, 44)
                m.c.restore()
        arc = skia.Path()
        rect = skia.Rect.MakeLTRB(cx - R, cy - R, cx + R, cy + R)
        if sgn < 0:
            arc.addArc(rect, 100, 150)
        else:
            arc.addArc(rect, -70, -150)
        m.stroke(arc, 8)
    m.poly([(256, 430), (226, 470), (286, 470)])


# ───────────────────────────── API ─────────────────────────────
@lru_cache(maxsize=256)
def icon_array(name, metal="gold", bevel=7.0, spec=0.7):
    m = _M()
    _ICONS[name](m)
    mask = m.arr()
    return relief_sprite(mask, metal, bevel=bevel, strength=1.0, spec=spec)


@lru_cache(maxsize=256)
def icon_image(name, metal="gold", size=512):
    a = icon_array(name, metal)
    if size != N:
        import cv2
        a = cv2.resize(a, (size, size), interpolation=cv2.INTER_AREA)
    return np_to_image(a)


def draw_icon(f, name, x, y, size=120, metal="gold", alpha=1.0, rot=0.0, shadow=True, glow=0.0, flip=False):
    img = icon_image(name, metal, 512)
    s = size / 512.0
    if shadow:
        f.c.save()
        f.c.translate(x + size * 0.04, y + size * 0.06)
        if rot:
            f.c.rotate(math.degrees(rot))
        f.c.scale(s * (-1 if flip else 1), s)
        p = skia.Paint(AntiAlias=True)
        p.setImageFilter(skia.ImageFilters.Blur(6 / max(s, 0.3), 6 / max(s, 0.3)))
        p.setColorFilter(skia.ColorFilters.Matrix([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.55 * alpha, 0]))
        f.c.drawImage(img, -256, -256, skia.SamplingOptions(skia.FilterMode.kLinear), p)
        f.c.restore()
    if glow > 0:
        f.c.save()
        f.c.translate(x, y)
        f.c.scale(s * 1.04, s * 1.04)
        p = skia.Paint(AntiAlias=True, Alpha=int(255 * glow * alpha))
        p.setImageFilter(skia.ImageFilters.Blur(10, 10))
        p.setBlendMode(skia.BlendMode.kPlus)
        f.c.drawImage(img, -256, -256, skia.SamplingOptions(skia.FilterMode.kLinear), p)
        f.c.restore()
    f.c.save()
    f.c.translate(x, y)
    if rot:
        f.c.rotate(math.degrees(rot))
    f.c.scale(s * (-1 if flip else 1), s)
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(max(0.0, min(1.0, alpha)))
    f.c.drawImage(img, -256, -256, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    f.c.restore()


def names():
    return sorted(_ICONS)


def icon_sheet(metals=("gold",), cols=8, size=150, out="out/frames/icons.png"):
    import cv2
    ks = names()
    rows = (len(ks) + cols - 1) // cols
    img = np.zeros((rows * size, cols * size, 3), np.uint8)
    img[:] = (28, 18, 12)
    for i, k in enumerate(ks):
        a = cv2.resize(icon_array(k, metals[i % len(metals)]), (size, size), interpolation=cv2.INTER_AREA)
        al = a[..., 3:4].astype(np.float32) / 255
        r, c = divmod(i, cols)
        sl = img[r * size:(r + 1) * size, c * size:(c + 1) * size]
        sl[:] = (sl * (1 - al) + a[..., :3] * al).astype(np.uint8)
    cv2.imwrite(out, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    return out
