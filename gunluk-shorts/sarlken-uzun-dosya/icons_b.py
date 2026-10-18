"""Bölüm yazarı B (c4, c5, c11) — ek kabartma simgeler. Ad çakışmasın diye hepsi `b_` önekli.

icons.py'deki @icon API'si: 512×512 maske tuvali, merkez (256,256); fill = beyaz, cut = oyuk.
Kullanım: `import icons_b` (kendiliğinden kaydolur), sonra icons.draw_icon(f, "b_press", ...).
"""
import math

import skia

import icons
import sk
from icons import icon


# ───────────────────────────── matbaa (vida baskı makinesi) ─────────────────────────────
@icon("b_press")
def _press(m):
    m.rect(96, 438, 320, 38, r=8)                 # taban kirişi
    m.rect(142, 110, 44, 340, r=6)                # sol direk
    m.rect(326, 110, 44, 340, r=6)                # sağ direk
    m.rect(116, 84, 280, 52, r=10)                # üst kiriş
    m.rect(238, 40, 36, 300, r=8)                 # vida mili
    m.circle(256, 38, 22)                         # vida başı
    # kol (lever): vidanın içinden geçen eğik çubuk + top
    m.line(64, 250, 330, 196, 22)
    m.circle(60, 252, 26)
    m.circle(60, 252, 11, 0)
    # baskı levhası (platen) ve yatak
    m.rect(180, 322, 152, 34, r=6)
    m.rect(150, 372, 212, 50, r=6)
    # dizgi kalıbı çizgileri
    for i in range(5):
        m.cut(sk.poly_path([(166 + i * 44, 380), (166 + i * 44, 416)], False), 4)
    m.cut(sk.poly_path([(150, 365), (362, 365)], False), 5)
    m.cut(sk.poly_path([(116, 140), (396, 140)], False), 4)
    # basılı sayfa (sağda)
    m.poly([(384, 330), (452, 316), (468, 392), (398, 408)])
    for i in range(3):
        m.cut(sk.poly_path([(396 + i * 2, 346 + i * 17), (446 + i * 2, 336 + i * 17)], False), 5)


# ───────────────────────────── dostlar (iki kişi) ─────────────────────────────
@icon("b_friends")
def _friends(m):
    for cx, sc in ((170, 0.92), (342, 1.0)):
        m.circle(cx, 170, 64 * sc)
        m.smooth([(cx - 120 * sc, 450), (cx - 118 * sc, 330), (cx - 70 * sc, 262), (cx, 246), (cx + 70 * sc, 262), (cx + 118 * sc, 330), (cx + 120 * sc, 450)], close=True, t=0.4)
    # aradaki kesik (öndeki kişiyi ayırır)
    r = skia.Path(); r.addCircle(342, 170, 78)
    m.cut(r, 10)
    m.cut(sk.smooth_path([(222, 450), (226, 330), (262, 276), (342, 250)], False, 0.4), 9)


# ───────────────────────────── beden (ayakta insan) ─────────────────────────────
@icon("b_body")
def _body(m):
    m.circle(256, 100, 56)
    m.smooth([(176, 196), (336, 196), (372, 330), (338, 340), (318, 262), (314, 340), (306, 480), (262, 480), (256, 372), (250, 480), (206, 480), (198, 340), (194, 262), (174, 340), (140, 330)], close=True, t=0.25)
    m.cut(sk.poly_path([(256, 210), (256, 360)], False), 5)
    m.cut(sk.smooth_path([(206, 206), (256, 232), (306, 206)], False), 5)


# ───────────────────────────── kan (damla) ─────────────────────────────
@icon("b_drop")
def _drop(m):
    m.smooth([(256, 40), (330, 168), (392, 270), (384, 356), (330, 428), (256, 452), (182, 428), (128, 356), (120, 270), (182, 168)], close=True, t=0.5)
    m.cut(sk.smooth_path([(190, 330), (200, 372), (236, 402)], False, 0.5), 14)
    m.cut(sk.smooth_path([(196, 292), (206, 262)], False), 9)


# ───────────────────────────── can (kalp) ─────────────────────────────
@icon("b_heart")
def _heart(m):
    m.smooth([(256, 440), (150, 340), (74, 262), (66, 178), (118, 108), (190, 98), (240, 140), (256, 176),
              (272, 140), (322, 98), (394, 108), (446, 178), (438, 262), (362, 340)], close=True, t=0.5)
    m.cut(sk.smooth_path([(128, 168), (152, 140), (186, 134)], False, 0.5), 11)
    m.cut(sk.poly_path([(100, 262), (176, 262), (206, 214), (244, 316), (282, 240), (302, 262), (410, 262)], False), 9)


# ───────────────────────────── ruh / fikir (alev) ─────────────────────────────
@icon("b_flame")
def _flame(m):
    m.smooth([(256, 30), (300, 110), (372, 190), (402, 290), (370, 392), (300, 454), (256, 466), (212, 454), (142, 392), (110, 290), (140, 214), (186, 160), (216, 110), (220, 64)], close=True, t=0.5)
    m.smooth([(256, 258), (292, 318), (318, 372), (290, 420), (256, 432), (222, 420), (194, 372), (222, 318)], close=True, t=0.5, v=0)
    m.smooth([(256, 316), (276, 360), (270, 404), (256, 414), (242, 404), (236, 360)], close=True, t=0.5, v=255)


# ───────────────────────────── Burgonya haçı (tırtıklı çapraz) ─────────────────────────────
@icon("b_saltire")
def _saltire(m):
    for ang in (-45, 45):
        m.c.save()
        m.c.translate(256, 256)
        m.c.rotate(ang)
        m.c.translate(-256, -256)
        m.rect(222, 40, 68, 432, r=10)
        # budak kütükleri
        for y in (120, 380):
            m.rect(190, y - 10, 38, 22, r=6)
            m.rect(284, y + 6, 38, 22, r=6)
        m.c.restore()
    m.cut(sk.poly_path([(256, 256), (256, 256)], False), 0)


# ───────────────────────────── çark (imparatorluk makinesi) ─────────────────────────────
@icon("b_gear")
def _gear(m):
    n = 14
    cx = cy = 256
    R, r = 232, 188
    pts = []
    for i in range(n):
        a0 = 2 * math.pi * i / n
        da = 2 * math.pi / n
        for f_, rr in ((0.00, r), (0.14, R), (0.52, R), (0.66, r)):
            a = a0 + f_ * da
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    m.poly(pts)
    ring = skia.Path(); ring.addCircle(cx, cy, 150)
    m.cut(ring, 16)
    hub = skia.Path(); hub.addCircle(cx, cy, 52)
    m.cut(hub)
    m.circle(cx, cy, 34)
    # kollar arası oyuklar
    for k in range(6):
        a = 2 * math.pi * k / 6 + math.pi / 6
        pa = skia.Path()
        pa.addArc(skia.Rect.MakeLTRB(cx - 128, cy - 128, cx + 128, cy + 128), math.degrees(a) - 20, 40)
        m.cut(pa, 46)


# ───────────────────────────── tek tek eski/yeni zincir halkası ─────────────────────────────
@icon("b_chain")
def _chain(m):
    for cx, ang in ((150, 0), (256, 90), (362, 0)):
        m.c.save(); m.c.translate(cx, 256); m.c.rotate(ang); m.c.translate(-cx, -256)
        p = skia.Path()
        p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(cx - 78, 190, cx + 78, 322), 60, 60))
        m.stroke(p, 30)
        m.c.restore()


# ───────────────────────────── yasak (daire-çizgi) ─────────────────────────────
@icon("b_forbid")
def _forbid(m):
    p = skia.Path(); p.addCircle(256, 256, 206)
    m.stroke(p, 52)
    m.line(110, 110, 402, 402, 56)


# ───────────────────────────── çatlak taç / kırık bağ ─────────────────────────────
@icon("b_gavel")
def _gavel(m):
    m.c.save(); m.c.translate(256, 256); m.c.rotate(-32); m.c.translate(-256, -256)
    m.rect(150, 96, 212, 104, r=20)               # tokmak başı
    m.rect(236, 190, 40, 260, r=14)               # sap
    m.cut(sk.poly_path([(150, 148), (362, 148)], False), 5)
    m.c.restore()
    m.rect(60, 440, 260, 34, r=10)                # kürsü tahtası
