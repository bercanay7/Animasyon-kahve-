#!/usr/bin/env python3
"""Medici kapakları (küçük resim). Parça 1 (kurul tur 1, KURUL.md §D): K1 "SON MEDİCİ / MİRASI KİLİTLEDİ", K2 "FAİZ YASAKTI".

Zemin = motorun KENDİ çizimi: iki kapak sahnesi türü bu dosyada kayıtlıdır (kapak_kilit, kapak_kese); yazı Pillow ile, Cinzel Black 900
(fonts/Cinzel_900Black.ttf: Cinzel değişken yazı tipinin wght=900 sabit örneği, latin + latin-ext birleşik → noktalı İ, Ş, Ğ).

  python3 kapak_medici.py --part 1             # K1 + K2 → yayin/studio_paketi_P1/kapak_P1_K1.jpg, _K2.jpg (1280×720, sRGB, <2 MB)
                                               #           out_p1/kapak/kapak_P1_K1.png, _K2.png (1920×1080) + *.yerlesim.json (kapak_qa okur)
  python3 kapak_medici.py --part 1 --kod K2    # tek kapak
  python3 kapak_medici.py --part 1 --kontrol   # kapak_qa.py (246/168/120, gri, akış maketi, bölge, kontrast) → out_p1/kapak/kapak_qa_P1.png/json

KAPAK YANKISI (videonun ilk 0,3–3,5 sn'si; kapağın vaadi ilk 5 sn'de görünsün):
    from kapak_medici import kapak_sahne_shot
    shot = kapak_sahne_shot("K1", a=("c0s1", -0.1), yazi=True)   # kapakla AYNI bileşim: tür + parametre + kamera (yavaş itme) + tek ışık
    # yazi=True → kapak yazısı motorda (aynı yazı tipi/yerleşim); yazi_at/yazi_out ile girer-söner. Tüm alanlar KAPAK_SAHNE'de.

Kurallar (CLAUDE.md "Kapak dersleri", PK1 §3a/3b/6, SA1, PK2): kahraman yazı büyük harf ≥ %18 (130 px @720p), ikincil ≥ %10 ya da yok;
süre rozeti bölgesi x 960–1250 × y 553–689 tamamen boş; sağ üst fare simgeleri x ≥ 1170, y ≤ 110 yazısız; parça rozeti "1/7" 150×74 sol altta;
tek parlak odak (kilit / kesenin ağzı), geri kalan karanlık ve sakin; yüz yok (motorun en zayıf yeri); P1 dönemi (1397–1429) armada mavi
zambaklı top YOK (1465 bahşişi; K2 palle = altın alan + 6 kırmızı top). K1 1743'te geçer: belgedeki mühür sonraki armayı taşıyabilir.
Kapak videonun söylemediğini vaat etmez: "Hiçbir şey buradan çıkmayacak" ve "çifte defter" kapakta yok."""
import argparse
import base64
import functools
import inspect
import io
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import skia  # noqa: E402

import cilt_city as CT  # noqa: E402
import cilt_medici as CM  # noqa: E402
import cilt_oda as OD  # noqa: E402
import cilt_props as CP  # noqa: E402
import shots as SH  # noqa: E402
import sk  # noqa: E402
from cilt_medici import ckind  # noqa: E402
from sk import H, W, back_out, clamp, lerp, mix, smooth  # noqa: E402

YAYIN = os.path.join(HERE, "yayin")
FONT_FILE = "Cinzel_900Black.ttf"
FONT_PATH = os.path.join(HERE, "fonts", FONT_FILE)
sk.FONT_FILES.setdefault("kapak", FONT_FILE)          # motor yüzü "kapak" (yankıdaki yazı aynı dosyadan)
CAP = 0.700                                           # Cinzel büyük harf yüksekliği / punto (OS/2 sCapHeight 700/1000)
DOT = 0.212                                           # İ noktasının büyük harf üstüne taşması / punto
K = 1.5                                               # 1280 birimi → 1920 tuval

# renkler (PK1 §3a-6: altın ≈ #F0CD73 / krem #FAEEC8, zemin sıcak yakın-siyah)
GOLD_T, GOLD_B = (253, 230, 160), (228, 172, 68)      # kahraman: üstten alta yaldız degradesi
CREAM = (250, 238, 204)
INK = (26, 13, 6)
BADGE_FILL, BADGE_EDGE = (14, 22, 62), (240, 205, 115)

# yasak bölgeler (1280×720): YouTube süre rozeti + masaüstü fare üstü simgeleri (Sonra izle / Sıraya ekle)
SURE_ROZETI = (960, 553, 1250, 689)
FARE_SIMGE = (1170, 0, 1280, 110)
PARCA_ROZETI = (26, 620, 176, 694)                    # 150×74, sol alt

sk.METAL.setdefault("demir", [("#0E1014", 0.0), ("#2E333B", 0.28), ("#8E959E", 0.54), ("#3A3F47", 0.78), ("#101216", 1.0)])
sk.METAL.setdefault("pirinc", [("#5A3A0E", 0.0), ("#B07A22", 0.24), ("#FFE7A0", 0.50), ("#D49A30", 0.72), ("#6E4614", 1.0)])
# deri yayınık (mat) yüzey: rampa tekdüze artar (metal rampaları gibi iki ucu koyu DEĞİL; yoksa ışığa bakan yan kararır)
sk.METAL.setdefault("kese_deri", [("#1A0C05", 0.0), ("#4A2A12", 0.24), ("#7C4A24", 0.44), ("#A86C38", 0.60), ("#D49A5C", 0.78), ("#EEC07E", 1.0)])

# ─────────────────────────────────────────────────────────────────────────────
# Parça yazıları (1280×720 birimi): satır = (rol, parçalar [(metin, büyük harf px)], x, taban çizgisi, dolgu)
# K1 kahraman satırı iki boylu tek satır: "SON" 92 + "MEDİCİ" 132 (aynı taban). Tek boyda 130 px "SON MEDİCİ" 1259 px tutar ve sağ uçta
# fare simgesi bölgesine (x ≥ 1170, y ≤ 110) girer; PK1'in önerdiği 120 px'lik tek satır sapmasına da gerek kalmaz: "MEDİCİ" ≥ %18.
# ─────────────────────────────────────────────────────────────────────────────
PART_TEXT = {
    1: {
        "K1": [dict(rol="kahraman", parcalar=[("SON", 92), (" ", 92), ("MEDİCİ", 132)], x=36, taban=190, dolgu="altin"),
               dict(rol="ikincil", parcalar=[("MİRASI KİLİTLEDİ", 74)], x=38, taban=306, dolgu="krem")],
        "K2": [dict(rol="kahraman", parcalar=[("FAİZ", 160)], x=44, taban=252, dolgu="altin"),
               dict(rol="ikincil", parcalar=[("YASAKTI", 104)], x=46, taban=392, dolgu="krem")],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# KAPAK_SAHNE: kapak bileşimi = çekim türü + parametreler (kamera, ışık, nesne yerleşimi). Koordinatlar 1920×1080 (motor tuvali).
# Sahne yazarı: kapak_sahne_shot("K1", a=…, yazi=True) → videonun ilk 0,3–3,5 sn'sinde aynı kare (kapak yankısı).
# ─────────────────────────────────────────────────────────────────────────────
KAPAK_SAHNE = {
    "K1": dict(
        tur="kapak_kilit",
        aciklama="1743 odası, imza masası yakın plan: Aile Antlaşması belgesi (mühürlü) + belgeyi saran demir zincir + pirinç asma kilit. "
                 "Tek ışık kilitte (tek parlak odak); duvar ve masa kenarları sıcak karanlığa batar. Yüz yok.",
        zaman=1.6,                                     # kapak karesi: çekimin yerel saniyesi (kulp kapanmış, parıltı yerinde)
        params=dict(
            mode="night", perde=1, seed=3,
            belge=(900, 812, 0.66, -0.035),            # belge merkezi x, y, ölçek (1100×760 kâğıt), dönüş (rad); mühür belgede (sağ alt)
            kilit=(900, 700, 290),                     # asma kilit: gövde üst-orta x, y, gövde genişliği B (px)
            zincir=((-80, 612), (2000, 622), 70),      # zincirin iki ucu (kare dışında: belgeyi sarar) + sarkma (px)
            kamera=("itme", 0.025),                    # kilide doğru yavaş itme: çekim boyunca +%2,5 (kapak karesinde ≈ +%1)
            isik=(900, 732, 640, 1.0),                 # tek ışık havuzu: merkez x, y, yarıçap, şiddet (kilit üstünde)
            ton=(18, 10, 15),                          # karanlığın rengi: sıcak yakın-siyah (perde I laciverti değil)
            kapan_at=0.45,                             # kulp bu yerel saniyede kapanır (yankıda "tık"; kapakta kapalı)
            duvar_y=470,                               # duvar/masa arka kenarı (y)
            hokka=(330, 700),                          # mürekkep hokkası (masa solu)
        ),
    ),
    "K2": dict(
        tur="kapak_kese",
        aciklama="1397–1429 Floransa banko masası (yeşil çuha): ağzı açık deri kese, içine yağan florinler; kese bağında P1 dönemi palle "
                 "(altın alan, 6 kırmızı top; mavi zambaklı top YOK). Tek ışık kesenin ağzında. Yüz yok.",
        zaman=1.35,
        params=dict(
            mode="night", perde=1, seed=4,
            kese=(1400, 792, 440),                     # kese taban ortası x, y, genişlik (px)
            yagmur=16,                                 # yağan florin sayısı (kesenin ağzına düşer)
            masa_sikke=((1010, 846, 118, 4), (880, 880, 104, 2), (1120, 900, 96, 1)),   # masada yatık florin yığınları (x, y, boy, adet)
            kamera=("itme", 0.02),
            isik=(1400, 430, 720, 1.0),
            ton=(16, 10, 14),
            masa_y=800,
        ),
    ),
}
# Yalnız kapak karesi (JPG) için zemin ayarı; videodaki yankı (0–3,3 sn) KAPAK_SAHNE parametreleriyle kalır (yazı ve kilit aynı, yankı kapağı tanıtır).
# Kurul tur 2, PK1-Y4: koyu temada kapak kenarı sayfaya karışıyordu (168 px'te 4 px kenar halkası ort. gri ≈ 18, gri < 25 payı %57;
# YouTube koyu tema ≈ 15) → karanlık sıcak kahve, dış vinyet hafif (ışık havuzu zaten merkezde toplar). Hedef: kenar ≥ 35, < 25 payı ≤ %35 (kapak_qa).
# PK1-Y5: parıltının kolları yok, yumuşak parlama kalır (en parlak nokta yine kilit / kese ağzı).
KAPAK_ZEMIN = {
    "K1": dict(ton=(52, 32, 26), vinyet=0.30, isinlar=False),
    "K2": dict(ton=(50, 32, 26), vinyet=0.30, isinlar=False),
}
KAPAK_GOLGE = (34, 21, 16)     # yazı zemini karartmasının hedef rengi (Pillow `shade`); eski yakın-siyah (8, 5, 4)
KUTU = {}          # son çizilen kapak sahnesinin öğe kutuları (1920 tuvali): kapak_qa bölge denetimi bunları kullanır


def kapak_sahne_shot(kod="K1", a=0.0, yazi=False, yazi_at=0.3, yazi_out=3.2, part=1, label=None, **ust):
    """KAPAK_SAHNE[kod] bileşimini `shots.shot(...)` olarak döndürür (sahne dosyasına doğrudan konur).
    yazi=True: kapak yazısı motorda çizilir (yazi_at'ta girer, yazi_out'ta söner; yerel sn). ust: parametreleri ezer (ör. tr=…, kamera=("itme", 0.04)).
    Not: tür kendi kamerasını (`kamera`) kullanır; cam= ön ayarı yalnız qa_flow kaydı içindir."""
    sp = KAPAK_SAHNE[kod]
    params = dict(sp["params"])
    tr = ust.pop("tr", None)
    cam = ust.pop("cam", None)
    link = ust.pop("link", None)
    params.update(ust)
    if yazi:
        params["yazi"] = dict(satirlar=PART_TEXT[part][kod], at=yazi_at, out=yazi_out)
    return SH.shot(sp["tur"], a, tr=tr, cam=cam, link=link, label=label or f"kapak yankısı {kod}", **params)


# ═════════════════════════════ motor: yardımcı çizimler ═════════════════════════════
def _mask(w, h, draw):
    s = skia.Surface(int(w), int(h))
    c = s.getCanvas()
    c.clear(skia.ColorBLACK)
    draw(c)
    return s.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)[..., 0].astype(np.float32) / 255.0


def _wp(v=255, style="fill", w=1.0):
    p = skia.Paint(AntiAlias=True, Color=skia.Color(v, v, v, 255))
    if style == "stroke":
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(w)
        p.setStrokeCap(skia.Paint.kRound_Cap)
    return p


def relief_ink(mask, metal, bevel, strength=1.2, spec=0.85, ink=3.0, ink_col=(22, 12, 6)):
    """relief_sprite (kabartma metal) + koyu mürekkep dış hattı (videodaki kâğıt-kesme çizgisi). RGBA uint8."""
    spr = sk.relief_sprite(mask, metal, bevel=bevel, strength=strength, spec=spec).astype(np.float32)
    if ink <= 0:
        return spr.astype(np.uint8)
    k = int(round(ink)) * 2 + 1
    dil = cv2.GaussianBlur(cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))), (0, 0), 0.7)
    a = spr[..., 3:4] / 255.0
    col = spr[..., :3] * a + np.array(ink_col, np.float32) * (1 - a)
    return np.clip(np.dstack([col, np.maximum(spr[..., 3], dil * 255)]), 0, 255).astype(np.uint8)


def _img(arr):
    return sk.np_to_image(np.ascontiguousarray(arr))


def isik_havuzu(f, x, y, r, hue=(18, 10, 15), gain=1.0):
    """Tek ışık havuzu (CM.relight'ın renk tonu seçilebilir sürümü): merkez sıcak-açık, dışı `hue` yakın-siyaha batar."""
    n = 640
    img = CM._pool_img(tuple(hue), n)
    D = 1.3 * r
    p = skia.Paint()
    p.setAlphaf(clamp(gain))
    c = f.c
    c.drawImageRect(img, skia.Rect.MakeWH(n, n), skia.Rect.MakeLTRB(x - D, y - D, x + D, y + D), CM._LIN, p)
    edge = skia.Paint(Color=skia.Color(hue[0], hue[1], hue[2], int(255 * 0.945 * gain)))
    L, T_, R_, B_ = x - D, y - D, x + D, y + D
    if L > 0:
        c.drawRect(skia.Rect.MakeLTRB(0, 0, L, H), edge)
    if R_ < W:
        c.drawRect(skia.Rect.MakeLTRB(R_, 0, W, H), edge)
    if T_ > 0:
        c.drawRect(skia.Rect.MakeLTRB(max(0, L), 0, min(W, R_), T_), edge)
    if B_ < H:
        c.drawRect(skia.Rect.MakeLTRB(max(0, L), B_, min(W, R_), H), edge)


def parilti(f, x, y, r, a=1.0, col="#FFF6DA", isinlar=True):
    """Metal parıltısı (toplamsal): karenin en parlak noktası. isinlar=True: dört kollu yıldız (videodaki kilit "tık"ı);
    isinlar=False: yalnız yumuşak parlama (kapak karesi; kurul tur 2, PK1-Y5: kollu yıldız stok/YZ kapak klişesi)."""
    c = f.c
    if not isinlar:
        f.circle(x, y, r * 0.62, shader=f.rad(x, y, r * 0.62 + 0.1, [(col, 0.0, int(120 * a)), (col, 0.40, int(46 * a)), (col, 1.0, 0)]),
                 blend=skia.BlendMode.kPlus)
        f.circle(x, y, r * 0.18, shader=f.rad(x, y, r * 0.18 + 0.1, [(col, 0.0, int(255 * a)), (col, 1.0, 0)]), blend=skia.BlendMode.kPlus)
        return
    for ang, ln in ((0, 1.0), (90, 1.0), (45, 0.42), (135, 0.42)):
        c.save()
        c.translate(x, y)
        c.rotate(ang)
        shd = skia.GradientShader.MakeLinear([(-r * ln, 0), (r * ln, 0)], [sk.C(col, 0), sk.C(col, int(255 * a)), sk.C(col, 0)], [0, 0.5, 1])
        c.drawRect(skia.Rect.MakeLTRB(-r * ln, -2.4, r * ln, 2.4), skia.Paint(Shader=shd, AntiAlias=True, BlendMode=skia.BlendMode.kPlus))
        c.restore()
    f.circle(x, y, r * 0.18, shader=f.rad(x, y, r * 0.18 + 0.1, [(col, 0.0, int(255 * a)), (col, 1.0, 0)]), blend=skia.BlendMode.kPlus)


def _itme(cx, oran):
    return 1.0 + oran * smooth(cx.t / max(1e-6, cx.dur))


def _kutu_x(b, piv, k):
    """Kutu (x0,y0,x1,y1) → piv merkezli k ölçekli kameradan sonra ekran kutusu."""
    px, py = piv
    return (px + (b[0] - px) * k, py + (b[1] - py) * k, px + (b[2] - px) * k, py + (b[3] - py) * k)


# ── asma kilit ─────────────────────────────────────────────────────────────
@functools.lru_cache(maxsize=8)
def padlock_sprites(B=290):
    """Asma kilit: (gövde, kulp) skia.Image + ölçüler. Gövde pirinç (çan biçimi, oluklu kenar, damla ayna, perçin), kulp demir.
    Orijin: gövde üst-orta = (ox, top)."""
    cw, ch = int(B * 1.5), int(B * 1.9)
    ox, top = cw / 2, B * 0.62
    bh = B * 0.86
    ky = top + bh * 0.42

    def body_path(inset=0.0):
        x0, x1 = ox - B / 2 + inset, ox + B / 2 - inset
        y0, y1 = top + inset, top + bh - inset
        r = B * 0.13
        p = skia.Path()
        p.moveTo(x0 + r, y0)
        p.lineTo(x1 - r, y0)
        p.quadTo(x1, y0, x1 + B * 0.004, y0 + r)
        p.cubicTo(x1 + B * 0.03, y0 + (y1 - y0) * 0.45, x1 + B * 0.01, y1 - (y1 - y0) * 0.18, x1 - B * 0.16, y1 - B * 0.005)
        p.quadTo(ox, y1 + B * 0.07 - inset * 0.5, x0 + B * 0.16, y1 - B * 0.005)
        p.cubicTo(x0 - B * 0.01, y1 - (y1 - y0) * 0.18, x0 - B * 0.03, y0 + (y1 - y0) * 0.45, x0 - B * 0.004, y0 + r)
        p.quadTo(x0, y0, x0 + r, y0)
        p.close()
        return p

    def keyhole(c, v, grow=0.0):
        c.drawCircle(ox, ky, B * (0.07 + grow), _wp(v))
        c.drawPath(sk.poly_path([(ox - B * (0.032 + grow), ky + B * 0.02), (ox + B * (0.032 + grow), ky + B * 0.02),
                                 (ox + B * (0.058 + grow), ky + B * (0.22 + grow)), (ox - B * (0.058 + grow), ky + B * (0.22 + grow))]), _wp(v))

    def body(c):
        c.drawPath(body_path(0), _wp(255))
        c.drawPath(body_path(B * 0.075), _wp(0, "stroke", B * 0.02))
        for sx in (-1, 1):                                      # kulp yuvaları (üst bilezikler)
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(ox + sx * B * 0.30 - B * 0.085, top - B * 0.05, ox + sx * B * 0.30 + B * 0.085, top + B * 0.05),
                                              B * 0.03, B * 0.03), _wp(255))
        esc = sk.smooth_path([(ox, ky - B * 0.19), (ox + B * 0.15, ky - B * 0.02), (ox + B * 0.11, ky + B * 0.24), (ox, ky + B * 0.33),
                              (ox - B * 0.11, ky + B * 0.24), (ox - B * 0.15, ky - B * 0.02)], True, 0.5)
        c.drawPath(esc, _wp(0, "stroke", B * 0.016))            # anahtar deliği aynası (damla)
        for dy in (-0.13, 0.26):
            c.drawCircle(ox, ky + dy * B, B * 0.022, _wp(0))
        for dx, dy in ((-0.34, 0.16), (0.34, 0.16), (-0.30, 0.80), (0.30, 0.80)):   # perçinler
            c.drawCircle(ox + dx * B, top + dy * bh, B * 0.03, _wp(0))
            c.drawCircle(ox + dx * B, top + dy * bh, B * 0.022, _wp(255))
        keyhole(c, 0)

    def shackle(c):
        R = B * 0.30
        p = skia.Path()
        p.moveTo(ox - R, top + B * 0.18)
        p.lineTo(ox - R, top - B * 0.02)
        p.arcTo(skia.Rect.MakeLTRB(ox - R, top - B * 0.02 - R, ox + R, top - B * 0.02 + R), 180, 180, False)
        p.lineTo(ox + R, top + B * 0.18)
        c.drawPath(p, _wp(255, "stroke", B * 0.115))

    spr_b = relief_ink(_mask(cw, ch, body), "pirinc", B / 34.0, 1.25, 0.95, ink=B / 80.0).astype(np.float32)
    spr_s = relief_ink(_mask(cw, ch, shackle), "demir", B / 40.0, 1.2, 0.85, ink=B / 80.0)
    hole = cv2.GaussianBlur(_mask(cw, ch, lambda c: keyhole(c, 255, -0.004)), (0, 0), 0.8)
    spr_b[..., :3] = spr_b[..., :3] * (1 - hole[..., None]) + np.array([5, 3, 2], np.float32) * hole[..., None]      # derin, opak anahtar deliği
    spr_b[..., 3] = np.maximum(spr_b[..., 3], hole * 255)
    g = dict(cw=cw, ch=ch, ox=ox, top=top, bh=bh, B=B, R=B * 0.30)
    return _img(np.clip(spr_b, 0, 255).astype(np.uint8)), _img(spr_s), g


def draw_padlock(f, x, y, B=290, drop=0.0):
    """(x, y) = gövde üst-orta; drop: kulp açıklığı (px, + = yukarıda). Dönüş: ekran kutusu (kulp dâhil)."""
    ib, is_, g = padlock_sprites(int(B))
    f.rrect(x - B * 0.46 + 14, y + 26, B * 0.92, g["bh"] * 0.96, B * 0.2, color="#000000", alpha=0.45, blur=18)
    ax, ay = g["ox"] / g["cw"], g["top"] / g["ch"]
    f.image(is_, x, y - drop, ax=ax, ay=ay)
    f.image(ib, x, y, ax=ax, ay=ay)
    return (x - B * 0.53, y - B * 0.02 - B * 0.30 - B * 0.06 - drop, x + B * 0.53, y + g["bh"] + B * 0.07)


# ── zincir ─────────────────────────────────────────────────────────────────
@functools.lru_cache(maxsize=8)
def link_sprites(L=116):
    """Zincir halkası: (ön halka, yan halka) skia.Image, orijin merkez, uzun eksen x."""
    wd, sw = L * 0.66, L * 0.23
    n = int(L * 1.4)

    def ring(c):
        c.drawOval(skia.Rect.MakeLTRB(n / 2 - L / 2 + sw / 2, n / 2 - wd / 2 + sw / 2, n / 2 + L / 2 - sw / 2, n / 2 + wd / 2 - sw / 2), _wp(255, "stroke", sw))

    def side(c):
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(n / 2 - L * 0.47, n / 2 - sw * 0.55, n / 2 + L * 0.47, n / 2 + sw * 0.55), sw * 0.55, sw * 0.55), _wp(255))
    r = relief_ink(_mask(n, n, ring), "demir", L / 26.0, 1.3, 0.9, ink=L / 40.0)
    s_ = relief_ink(_mask(n, n, side), "demir", L / 26.0, 1.3, 0.9, ink=L / 40.0)
    return _img(r), _img(s_), n


def chain_points(p0, p1, sag, pitch):
    """p0→p1 sarkık zincir (parabol): eşit yay aralıklı (x, y, açı)."""
    (x0, y0), (x1, y1) = p0, p1
    N = 400
    pts = [(lerp(x0, x1, i / N), lerp(y0, y1, i / N) + sag * 4 * (i / N) * (1 - i / N)) for i in range(N + 1)]
    d = [0.0]
    for i in range(1, len(pts)):
        d.append(d[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    out, s, j = [], 0.0, 0
    while s <= d[-1]:
        while j < len(d) - 2 and d[j + 1] < s:
            j += 1
        k = (s - d[j]) / max(1e-6, d[j + 1] - d[j])
        out.append((lerp(pts[j][0], pts[j + 1][0], k), lerp(pts[j][1], pts[j + 1][1], k), math.atan2(pts[j + 1][1] - pts[j][1], pts[j + 1][0] - pts[j][0])))
        s += pitch
    return out


def draw_chain(f, p0, p1, sag=40, L=116):
    ring, side, n = link_sprites(int(L))
    pts = chain_points(p0, p1, sag, L * 0.66)
    for (x, y, a) in pts:
        f.oval(x + 10, y + 22, L * 0.48, L * 0.22, color="#000000", alpha=0.30, blur=10)
    for pass_ in (1, 0):                                        # önce yan halkalar (arkada), sonra ön halkalar
        for i, (x, y, a) in enumerate(pts):
            if i % 2 == pass_:
                f.image(side if pass_ == 1 else ring, x, y, rot=a, ax=0.5, ay=0.5)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return (min(xs) - L / 2, min(ys) - L / 2, max(xs) + L / 2, max(ys) + L / 2)


# ── palle (P1 dönemi), kese, ip ────────────────────────────────────────────
@functools.lru_cache(maxsize=4)
def palle_erken(size=150, n_balls=6):
    """1397–1429 palle kalkanı: altın alan + kırmızı mine toplar (mavi zambaklı top YOK: XI. Louis'nin 1465 bahşişi; KA1-G2). RGBA uint8."""
    S_ = CP.ARMS_S
    Msh = CP.Mask(S_)
    Msh.fill(CP.shield_path(0))
    msh = Msh.arr()
    Mr = CP.Mask(S_)
    Mr.stroke(CP.shield_path(26), 30)
    mrim = Mr.arr()
    balls = [(500, 236, 104), (276, 350, 102), (724, 350, 102), (318, 600, 102), (682, 600, 102), (500, 792, 102)][:n_balls]
    yy, xx = np.mgrid[0:S_, 0:S_].astype(np.float32)
    Hh = np.zeros((S_, S_), np.float32)
    red_m = np.zeros((S_, S_), np.float32)
    for (bx, by, br) in balls:
        d = np.hypot(xx - bx, yy - by)
        inside = d < br
        Hh = np.maximum(Hh, np.where(inside, np.sqrt(np.clip(1 - (d / br) ** 2, 0, 1)) * br * 0.62, 0) + inside * 10)
        red_m = np.maximum(red_m, np.clip((br - d) / 1.6, 0, 1))
    Hh = (Hh + 26.0 * msh + 34 * CP._soft(mrim, 3.0)) * (msh > 0.02)
    sh_g, sp_g = CP.shade_height(Hh, strength=1.25, spec_pow=26.0, blur=1.1)
    _, sp_e = CP.shade_height(Hh, strength=1.0, spec_pow=70.0, blur=1.1)
    gold = CP.ramp_color("leaf", sh_g) + sp_g[..., None] * 255 * 0.62
    red = CP.ramp_enamel("red", CP._lambert(Hh, 1.0)) + sp_e[..., None] * 255 * 0.95
    col = gold * (1 - red_m[..., None]) + red * red_m[..., None]
    a = np.clip(msh, 0, 1)
    k = 19
    dil = cv2.dilate(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    col = col * a[..., None] + np.array(INK, np.float32) * (1 - a[..., None])
    out = np.dstack([np.clip(col, 0, 255), np.maximum(a, dil) * 255]).astype(np.uint8)
    return cv2.resize(out, (size, size), interpolation=cv2.INTER_AREA)


@functools.lru_cache(maxsize=4)
def kese_sprite(Wp=440):
    """Deri kese: ağzı açık, boynu büzgülü; gövde kubbesi + boyundan yayılan büzgü pilileri + yan dikiş + ince deri dokusu. (skia.Image, ölçüler)."""
    w = Wp
    cw, ch = int(w * 1.30), int(w * 1.42)
    ox = cw / 2
    neck_y, rim_y, bot_y = ch * 0.31, ch * 0.135, ch * 0.965

    def P(u, v):
        return (ox + u * w, v)

    body = [P(-0.19, neck_y + 4), P(-0.32, neck_y + w * 0.09), P(-0.46, neck_y + w * 0.30), P(-0.50, neck_y + w * 0.52), P(-0.47, bot_y - w * 0.17),
            P(-0.31, bot_y - w * 0.035), P(0.0, bot_y), P(0.31, bot_y - w * 0.035), P(0.47, bot_y - w * 0.17), P(0.50, neck_y + w * 0.52),
            P(0.46, neck_y + w * 0.30), P(0.32, neck_y + w * 0.09), P(0.19, neck_y + 4)]
    top = [P(-0.19, neck_y + 6), P(-0.25, neck_y - w * 0.07), P(-0.34, rim_y + w * 0.05)]
    nfr = 11
    for i in range(nfr + 1):
        top.append(P(-0.34 + 0.68 * i / nfr, rim_y + (w * 0.020 if i % 2 else -w * 0.014)))
    top += [P(0.25, neck_y - w * 0.07), P(0.19, neck_y + 6)]
    mb = _mask(cw, ch, lambda c: c.drawPath(sk.smooth_path(body, True, 0.45), _wp(255)))
    mt = _mask(cw, ch, lambda c: c.drawPath(sk.smooth_path(top, True, 0.35), _wp(255)))
    mouth = _mask(cw, ch, lambda c: c.drawOval(skia.Rect.MakeLTRB(ox - w * 0.285, rim_y - w * 0.03, ox + w * 0.285, rim_y + w * 0.085), _wp(255)))
    yy, xx = np.mgrid[0:ch, 0:cw].astype(np.float32)
    dome = cv2.GaussianBlur(mb, (0, 0), w * 0.10) * w * 0.20
    ang = np.arctan2(yy - neck_y, xx - ox)
    rr = np.hypot(xx - ox, yy - neck_y)
    pleat = np.cos(ang * 14.0) * np.clip(1 - rr / (w * 0.42), 0, 1) ** 1.5 * w * 0.022 * (yy > neck_y)
    rs = np.random.RandomState(7)
    big = cv2.GaussianBlur(rs.randn(ch, cw).astype(np.float32), (0, 0), w * 0.05)
    big = big / (big.std() + 1e-6) * w * 0.0035
    grain = cv2.GaussianBlur(rs.randn(ch, cw).astype(np.float32), (0, 0), 1.3)
    grain = grain / (grain.std() + 1e-6) * 0.12
    Hb = (dome + pleat + big + grain) * (mb > 0.02)
    Ht = (cv2.GaussianBlur(mt, (0, 0), w * 0.03) * w * 0.07 + np.cos((xx - ox) / w * 40.0) * w * 0.006 + grain) * (mt > 0.02)
    sh_b, sp_b = CP.shade_height(Hb, strength=0.85, spec_pow=14.0, blur=1.6)
    sh_t, sp_t = CP.shade_height(Ht, strength=1.0, spec_pow=16.0, blur=1.0)
    col_b = CP.ramp_color("kese_deri", sh_b) + sp_b[..., None] * 255 * 0.28
    col_t = CP.ramp_color("kese_deri", np.clip(sh_t * 0.92 + 0.04, 0, 1)) + sp_t[..., None] * 255 * 0.18
    seam = _mask(cw, ch, lambda c: [c.drawLine(*P(0.36 + 0.10 * (k_ / 12) ** 1.2, neck_y + w * (0.16 + 0.05 * k_)),
                                               *P(0.36 + 0.10 * ((k_ + 0.5) / 12) ** 1.2, neck_y + w * (0.16 + 0.05 * k_ + 0.028)), _wp(255, "stroke", w * 0.010))
                                    for k_ in range(12)])
    col_b = col_b * (1 - 0.55 * seam[..., None])
    a_t = mt[..., None]
    col = col_b * mb[..., None] * (1 - a_t) + col_t * a_t
    alpha = np.maximum(mb, mt)
    col = col * (1 - mouth[..., None]) + np.array([30, 15, 6], np.float32) * mouth[..., None]
    k = max(3, int(w / 120)) * 2 + 1
    dil = cv2.GaussianBlur(cv2.dilate(alpha, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))), (0, 0), 0.7)
    col = col * alpha[..., None] + np.array(INK, np.float32) * (1 - alpha[..., None])
    out = np.dstack([np.clip(col, 0, 255), np.maximum(alpha, dil) * 255]).astype(np.uint8)
    g = dict(cw=cw, ch=ch, ox=ox, neck_y=neck_y, rim_y=rim_y, bot_y=bot_y, w=w, mouth=(ox, rim_y + w * 0.028), mouth_rx=w * 0.28, mouth_ry=w * 0.055)
    return _img(out), g


def rope(f, pts, wd, col="#B8873A", ink="#1E1006"):
    """Bükülmüş ip: koyu hat + ana renk + çapraz bükülme çizgileri."""
    path = sk.smooth_path(pts, False, 0.5)
    f.path(path, color=ink, style="stroke", sw=wd + 4)
    f.path(path, color=col, style="stroke", sw=wd)
    pm = skia.PathMeasure(path, False)
    L = pm.getLength()
    n = max(1, int(L / (wd * 0.9)))
    for i in range(n):
        pos, tan = pm.getPosTan(L * (i + 0.5) / n)
        x, y, tx, ty = pos.x(), pos.y(), tan.x(), tan.y()
        nx, ny = -ty, tx
        f.line(x - nx * wd * 0.45 - tx * wd * 0.25, y - ny * wd * 0.45 - ty * wd * 0.25, x + nx * wd * 0.45 + tx * wd * 0.25, y + ny * wd * 0.45 + ty * wd * 0.25,
               color=ink, sw=1.6, alpha=0.75)
        f.line(x - nx * wd * 0.30 - tx * wd * 0.10, y - ny * wd * 0.30 - ty * wd * 0.10, x + nx * wd * 0.10, y + ny * wd * 0.10, color="#F2D08A", sw=1.4, alpha=0.6)


def draw_kese(f, x, y, Wp=440, palle=True):
    """(x, y) = kesenin taban ortası. Dönüş: (ağız x, ağız y, ölçüler, kese kutusu, palle kutusu)."""
    img, g = kese_sprite(int(Wp))
    x0, y0 = x - g["ox"], y - g["bot_y"]
    f.oval(x + 18, y - 4, Wp * 0.56, Wp * 0.085, color="#000000", alpha=0.6, blur=16)
    f.image(img, x0, y0)
    mx, my = x0 + g["mouth"][0], y0 + g["mouth"][1]
    rs = np.random.RandomState(3)
    for i in range(8):                                          # ağızda parlayan florinler
        u = (i - 3.5) / 4.0
        cx_, cy_ = mx + u * g["mouth_rx"] * 0.80, my + rs.uniform(-0.1, 0.55) * g["mouth_ry"]
        f.oval(cx_, cy_, g["mouth_rx"] * 0.16, g["mouth_ry"] * 0.40, color=mix("#F2C455", "#8A5A18", rs.rand() * 0.5))
        f.oval(cx_ - 3, cy_ - 2, g["mouth_rx"] * 0.07, g["mouth_ry"] * 0.14, color="#FFF2C0", alpha=0.7)
    w = g["w"]
    ny = y0 + g["neck_y"]
    rope(f, [(x - w * 0.205, ny - 6), (x - w * 0.08, ny + 6), (x + w * 0.08, ny + 6), (x + w * 0.205, ny - 6)], w * 0.040)
    rope(f, [(x - w * 0.20, ny + 12), (x - w * 0.06, ny + 22), (x + w * 0.10, ny + 20), (x + w * 0.20, ny + 10)], w * 0.036)
    kx_, ky_ = x - w * 0.09, ny + 16
    rope(f, [(kx_, ky_), (kx_ - w * 0.06, ky_ + w * 0.10), (kx_ - w * 0.10, ky_ + w * 0.20), (kx_ - w * 0.13, ky_ + w * 0.29)], w * 0.032)
    rope(f, [(kx_ + 6, ky_), (kx_ + w * 0.02, ky_ + w * 0.11), (kx_ - w * 0.01, ky_ + w * 0.19)], w * 0.030)
    f.circle(kx_, ky_, w * 0.035, color="#1E1006")
    f.circle(kx_, ky_, w * 0.027, color="#B8873A")
    pal = None
    if palle:
        ps = int(w * 0.34)
        px, py = kx_ - w * 0.13, ky_ + w * 0.29 + ps * 0.42
        f.image(_img(palle_erken(ps)), px, py, ax=0.5, ay=0.5, rot=0.06)
        pal = (px - ps * 0.45, py - ps * 0.5, px + ps * 0.45, py + ps * 0.5)
    kutu = (x - w * 0.52, y0 + g["rim_y"] - w * 0.05, x + w * 0.52, y)
    return mx, my, g, kutu, pal


# ── motor yazısı (yalnız yankı; kapakta yazı Pillow ile) ───────────────────
def _yazi_motor(f, satirlar, alpha):
    """Kapak yazısını motorda çizer (aynı yazı tipi/yerleşim; yalnız yankı için — kapakta yazı Pillow ile). f.text taban çizgisine taşınmış
    yerel koordinatta çizdiği için degrade yerel y'de kurulur (−büyük harf … 0)."""
    if alpha <= 0.003:
        return
    for st in satirlar:
        x, base = st["x"] * K, st["taban"] * K
        cap_max = max(c for _, c in st["parcalar"]) * K
        if st["dolgu"] == "altin":
            shd = f.lin(0, -cap_max, 0, 0, [("#FDE6A0", 0.0), ("#E4AC44", 1.0)])
            color = "#F0CD73"
        else:
            shd, color = None, "#FAEECC"
        for txt, cap in st["parcalar"]:
            wid = f.text(txt, x, base, face="kapak", size=cap * K / CAP, color=color, shader=shd, alpha=alpha,
                         shadow=(4 * K, 7 * K, 10, "#060302"), outline=(3 * K * 2, "#1A0D06"))
            x += wid


# ═════════════════════════════ kapak sahnesi türleri ═════════════════════════════
@ckind("kapak_kilit")
def k_kapak_kilit(cx, belge=(900, 812, 0.66, -0.035), kilit=(900, 700, 290), zincir=((-80, 612), (2000, 622), 70), kamera=("itme", 0.025),
                  isik=(900, 732, 640, 1.0), ton=(18, 10, 15), kapan_at=0.45, duvar_y=470, hokka=(330, 700), yazi=None, seed=3,
                  vinyet=0.75, isinlar=True, **_):
    """K1 kapak sahnesi: 1743 imza masası yakın plan (oda1743'ün sıva/lambri/örtü/belge/mühür/hokka çizimleriyle), belgeyi saran demir zincir,
    pirinç asma kilit. kapan_at'ta kulp kapanır (geri sekme + parıltı). Tek ışık kilitte. yazi: kapak_sahne_shot(yazi=True) doldurur."""
    f, c = cx.f, cx.f.c
    T = CT.Tint("dusk")
    kx, ky, B = kilit
    k = _itme(cx, kamera[1] if kamera else 0.0)
    piv = (kx, ky)
    c.save()
    c.translate(kx, ky)
    c.scale(k, k)
    c.translate(-kx, -ky)
    OD.plaster(c, -40, W + 40, -40, duvar_y + 20, T, "#8C7458", "#7A6048", amp=0.05)
    OD.wainscot(c, -40, W + 40, duvar_y - 250, duvar_y + 10, T, "#6E4A30", pw=300.0, seed=2)
    OD.table_top(c, OD.TGeom(-260, H + 150, W + 520, H + 150 - duvar_y, 0.035), T, ("#8E2A30", "#D2A33E"))
    bx, by, bs, br = belge
    OD.doc_sheet(f, bx, by, bs, cx.t, n=13, seed=3, rot=br, seal=True, seal_t=1.0, shadow=0.6)
    if hokka:
        OD.inkwell(c, hokka[0], hokka[1], 4.0, cx.t)
    p0, p1, sag = zincir
    R = B * 0.30
    leg_y = ky - B * 0.10
    z1 = draw_chain(f, p0, (kx - R - B * 0.02, leg_y), sag=sag, L=B * 0.40)
    z2 = draw_chain(f, (kx + R + B * 0.02, leg_y), p1, sag=sag, L=B * 0.40)
    c.restore()
    isik_x, isik_y, isik_r, isik_k = isik
    isik_havuzu(f, isik_x, isik_y, isik_r, hue=ton, gain=isik_k)
    t_cl = clamp((cx.t - kapan_at) / 0.25) if kapan_at is not None else 1.0
    drop = (1.0 - back_out(t_cl)) * B * 0.10
    c.save()
    c.translate(kx, ky)
    c.scale(k, k)
    c.translate(-kx, -ky)
    OD.PN.glow(c, kx, ky + B * 0.35, B * 2.0, "#FFB454", 0.20)
    kb = draw_padlock(f, kx, ky, B, drop=drop)
    c.restore()
    flash = 1.0 + 0.6 * math.exp(-max(0.0, cx.t - (kapan_at or 0.0)) * 5.0) * (1.0 if cx.t >= (kapan_at or 0.0) else 0.0)
    sx, sy = piv[0] + (kx - B * 0.30 - piv[0]) * k, piv[1] + (ky + B * 0.06 - piv[1]) * k
    parilti(f, sx, sy, B * 0.45 * (0.85 + 0.15 * math.sin(cx.t * 2.0)) * min(1.6, flash), a=min(1.0, 0.8 * flash), isinlar=isinlar)
    CM.motes(f, cx.t, n=8, seed=seed)
    if vinyet:
        CM.vig(f, vinyet)
    if yazi:
        a = smooth((cx.t - yazi.get("at", 0.3)) / 0.35) * (1 - smooth((cx.t - yazi.get("out", 3.2)) / 0.45))
        _yazi_motor(f, yazi["satirlar"], a)
    # öğe kutuları (ekran): odak = asma kilit (kulp dâhil); mühür belgenin sağ altında
    ms = (bx + (330 * math.cos(br) - 262 * math.sin(br)) * bs, by + (330 * math.sin(br) + 262 * math.cos(br)) * bs)
    mr = 58 * bs * 1.1
    KUTU["kapak_kilit"] = dict(odak=_kutu_x(kb, piv, k), belge=_kutu_x((bx - 550 * bs, by - 380 * bs, bx + 550 * bs, by + 380 * bs), piv, k),
                               muhur=_kutu_x((ms[0] - mr, ms[1] - mr, ms[0] + mr, ms[1] + mr), piv, k),
                               zincir=_kutu_x((min(z1[0], z2[0]), min(z1[1], z2[1]), max(z1[2], z2[2]), max(z1[3], z2[3])), piv, k))



@ckind("kapak_kese")
def k_kapak_kese(cx, kese=(1400, 792, 440), yagmur=24, masa_sikke=(), kamera=("itme", 0.02), isik=(1400, 430, 720, 1.0), ton=(16, 10, 14),
                 masa_y=800, yazi=None, seed=4, vinyet=0.75, isinlar=True, **_):
    """K2 kapak sahnesi: banko masası (yeşil çuha, taş duvar), ağzı açık deri kese, boyun ipinde P1 palle kalkanı, ağza yağan florinler
    (CP.draw_coin: zambak / Vaftizci Yahya). Florinler sürekli düşer (döngü); tek ışık kesenin ağzında."""
    f, c = cx.f, cx.f.c
    T = CT.Tint("dusk")
    kx, ky, Wp = kese
    k = _itme(cx, kamera[1] if kamera else 0.0)
    piv = (kx, ky - 300)
    c.save()
    c.translate(*piv)
    c.scale(k, k)
    c.translate(-piv[0], -piv[1])
    OD.plaster(c, -40, W + 40, -40, masa_y + 20, T, "#7A6448", "#6A5238", amp=0.05)
    OD.ashlar(c, -40, W + 40, -40, masa_y - 40, T, "#857152", 96.0, seed=2)
    OD.table_top(c, OD.TGeom(-260, H + 200, W + 520, H + 200 - masa_y, 0.03), T, ("#1F4A2E", "#C9962B"))
    mx, my, g, kk, pal = draw_kese(f, kx, ky, Wp)
    xs = []
    for (x, y, s, n_) in masa_sikke:                            # masada yatık florin yığınları (x, y, boy, adet)
        f.oval(x + 6, y + 8, s * 0.56, s * 0.17, color="#000000", alpha=0.55, blur=8)
        for j in range(int(n_)):
            yy_ = y - j * s * 0.075
            f.oval(x, yy_ + s * 0.035, s * 0.5, s * 0.16, color="#6A4A14")
            c.save()
            c.translate(x, yy_)
            c.scale(1.0, 0.32)
            CP.draw_coin(f, 0, 0, s, spin=0.0, tilt=0.4 * j, shadow=0.0)
            c.restore()
        xs.append((x - s / 2, y - s * 0.2 - n_ * s * 0.075, x + s / 2, y + s * 0.2))
    c.restore()
    isik_x, isik_y, isik_r, isik_k = isik
    isik_havuzu(f, isik_x, isik_y, isik_r, hue=ton, gain=isik_k)
    smx, smy = piv[0] + (mx - piv[0]) * k, piv[1] + (my - piv[1]) * k
    OD.PN.glow(c, smx, smy, Wp * 0.95, "#FFC860", 0.42)
    rs = np.random.RandomState(seed)
    yb = [1e9, 1e9, -1e9, -1e9]
    for i in range(yagmur):
        fall = (cx.t * (0.55 + 0.25 * rs.rand()) + rs.rand()) % 1.0
        y = lerp(-120, smy - 40, fall * fall * 0.35 + fall * 0.65)
        x = smx + (rs.rand() - 0.5) * ((1 - fall) * 300 + 50) * 2       # ağza daralan koni
        s = rs.uniform(66, 118) * (0.85 + 0.3 * (1 - fall))
        sp, tl = rs.rand() * 6.28 + cx.t * 3, rs.uniform(-0.6, 0.6)
        a = (1.0 - smooth((y - (smy - 70)) / 40.0)) * (0.55 + 0.45 * smooth(fall * 1.6))   # ağza girerken kaybolur; yukarıdakiler sönük
        if a <= 0.01:
            continue
        f.rect(x - s * 0.10, y - s * 1.3, s * 0.20, s * 1.1, shader=f.lin(x, y - s * 1.3, x, y - s * 0.2, [("#FFE9A8", 0.0, 0), ("#FFE9A8", 1.0, int(34 * a))]),
               blend=skia.BlendMode.kPlus, blur=5.0)
        CP.draw_coin(f, x, y, s, spin=sp, tilt=tl, shadow=0.0, thick=0.10, glow=0.12, alpha=a)
        yb = [min(yb[0], x - s / 2), min(yb[1], y - s / 2), max(yb[2], x + s / 2), max(yb[3], y + s / 2)]
    OD.PN.glow(c, smx, smy - 10, Wp * 0.55, "#FFF0C0", 0.55)
    parilti(f, smx - 30, smy - 20, Wp * 0.30, a=0.85, isinlar=isinlar)
    CM.motes(f, cx.t, n=10, seed=seed)
    if vinyet:
        CM.vig(f, vinyet)
    if yazi:
        a = smooth((cx.t - yazi.get("at", 0.3)) / 0.35) * (1 - smooth((cx.t - yazi.get("out", 3.2)) / 0.45))
        _yazi_motor(f, yazi["satirlar"], a)
    r_ = Wp * 0.36
    od = (smx - r_, smy - r_ * 0.8, smx + r_, smy + r_ * 0.5)
    if yb[2] > yb[0]:
        od = (min(od[0], yb[0]), max(0.0, min(od[1], yb[1])), max(od[2], yb[2]), od[3])
    KUTU["kapak_kese"] = dict(odak=od, kese=_kutu_x(kk, piv, k),
                              palle=_kutu_x(pal, piv, k) if pal else None, yagmur=tuple(yb) if yb[2] > yb[0] else None,
                              masa_sikke=_kutu_x((min(b[0] for b in xs), min(b[1] for b in xs), max(b[2] for b in xs), max(b[3] for b in xs)), piv, k) if xs else None)


# ═════════════════════════════ kapak: motor karesi + Pillow yazı ═════════════════════════════
def engine_frame(shot, t):
    """Tek çekimi motorda çizip t saniyedeki kareyi (1920×1080 RGB, post uygulanmış) döndürür. Kapak durağan: seçici deklanşör kapalı."""
    import compose
    kw = {"shutter": False} if "shutter" in inspect.signature(compose.Program.__init__).parameters else {}
    prog = compose.Program(shots=[shot], end=t + 1.0, **kw)
    return prog.frame(int(round(t * sk.FPS)))


@functools.lru_cache(maxsize=32)
def font(cap1280):
    """Cinzel Black 900, büyük harf yüksekliği cap1280 px (1280×720 biriminde) olacak puntoda (1920 tuvali için)."""
    return ImageFont.truetype(FONT_PATH, int(round(cap1280 * K / CAP)))


def text_line(im, satir):
    """Bir satırı (aynı taban çizgisinde bir/çok boylu parçalar) yazar: yumuşak gölge + koyu dış hat + dolgu (altın degrade | krem).
    Dönüş: (mürekkep kutusu 1280 biriminde, maske L 1920×1080)."""
    mask = Image.new("L", im.size, 0)
    md = ImageDraw.Draw(mask)
    x = satir["x"] * K
    base = satir["taban"] * K
    for txt, cap in satir["parcalar"]:
        f = font(cap)
        md.text((x, base), txt, font=f, fill=255, anchor="ls")
        x += f.getlength(txt)
    bb = mask.getbbox()
    sh = mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(10))
    im.paste(Image.new("RGB", im.size, (6, 3, 2)), (int(4 * K), int(7 * K)), sh.point(lambda v: int(v * 0.85)))
    im.paste(Image.new("RGB", im.size, INK), (0, 0), mask.filter(ImageFilter.MaxFilter(2 * int(3 * K) + 1)))
    if satir["dolgu"] == "altin":
        Wd, Hd = im.size
        yy = np.clip((np.arange(Hd, dtype=np.float32) - bb[1]) / max(1, bb[3] - bb[1]), 0, 1)[:, None, None]
        grad = np.array(GOLD_T, np.float32)[None, None] * (1 - yy) + np.array(GOLD_B, np.float32)[None, None] * yy
        fill = Image.fromarray(np.repeat(grad, Wd, axis=1).astype(np.uint8))
    else:
        fill = Image.new("RGB", im.size, CREAM)
    im.paste(fill, (0, 0), mask)
    return tuple(round(v / K, 1) for v in bb), mask


def part_badge(im, part, n=7):
    """Parça rozeti: "1/7", 150×74 (1280 biriminde), sol alt. Kutusunu döndürür (1280)."""
    x0, y0, x1, y1 = (v * K for v in PARCA_ROZETI)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, y0, x1, y1), int(12 * K), fill=BADGE_FILL, outline=BADGE_EDGE, width=int(4 * K))
    d.text(((x0 + x1) / 2, (y0 + y1) / 2 + 2 * K), f"{part}/{n}", font=font(33), fill=CREAM, anchor="mm")
    return PARCA_ROZETI


def shade(im, kind="ust", y1=330, x1=780, a=0.55, renk=(8, 5, 4)):
    """Yazı zemini için yumuşak sıcak-siyah karartma: 'ust' (üst bant, y < y1) ya da 'sol' (sol bölge, x < x1). Ölçüler 1280 biriminde."""
    arr = np.asarray(im).astype(np.float32)
    Hd, Wd = arr.shape[:2]
    if kind == "ust":
        v = np.arange(Hd, dtype=np.float32)[:, None] / K
        m = np.clip(1 - (v - (y1 - 140)) / 140, 0, 1) * a
        m = np.repeat(m, Wd, axis=1)
    else:
        u = np.arange(Wd, dtype=np.float32)[None, :] / K
        m = np.clip(1 - (u - (x1 - 260)) / 260, 0, 1) * a
        m = np.repeat(m, Hd, axis=0)
    arr = arr * (1 - m[..., None]) + np.array(renk, np.float32) * m[..., None]
    return Image.fromarray(arr.astype(np.uint8))


def _png_b64(mask_l):
    buf = io.BytesIO()
    mask_l.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def _srgb_icc():
    try:
        from PIL import ImageCms
        return ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    except Exception:
        return None


def paths(part):
    paket = os.path.join(YAYIN, f"studio_paketi_P{part}")
    kapak = os.path.join(HERE, f"out_p{part}", "kapak")
    os.makedirs(paket, exist_ok=True)
    os.makedirs(kapak, exist_ok=True)
    return paket, kapak


def cover(part, kod):
    """Bir kapağı üretir: motor karesi (KAPAK_SAHNE) + yazı (PART_TEXT) + rozet → JPG 1280×720 + PNG 1920×1080 + yerleşim JSON."""
    sp = KAPAK_SAHNE[kod]
    arr = engine_frame(kapak_sahne_shot(kod, part=part, **KAPAK_ZEMIN.get(kod, {})), sp["zaman"])
    kutu = {k_: (None if v is None else tuple(round(x / K, 1) for x in v)) for k_, v in KUTU[sp["tur"]].items()}
    im = Image.fromarray(arr).convert("RGB")
    im = shade(im, "ust", y1=330, a=0.50, renk=KAPAK_GOLGE) if kod == "K1" else shade(im, "sol", x1=780, a=0.55, renk=KAPAK_GOLGE)
    ogeler = []
    for st in PART_TEXT[part][kod]:
        bb, m = text_line(im, st)
        caps = [c for t_, c in st["parcalar"] if t_.strip()]
        small = m.resize((1280, 720), Image.LANCZOS)
        ogeler.append(dict(ad=st["rol"], tur="yazi", metin="".join(t_ for t_, _ in st["parcalar"]), kutu=list(bb),
                           kap_px=max(caps), kap_px_min=min(caps), kap_oran=round(max(caps) / 720, 4), renk=list(GOLD_T if st["dolgu"] == "altin" else CREAM),
                           parcalar=[dict(metin=t_, kap_px=c) for t_, c in st["parcalar"] if t_.strip()], maske_png=_png_b64(small)))
    rz = part_badge(im, part)
    ogeler.append(dict(ad="parca_rozeti", tur="rozet", metin=f"{part}/7", kutu=list(rz)))
    for ad, b in kutu.items():
        if b is None:
            continue
        ogeler.append(dict(ad=ad, tur="odak" if ad == "odak" else "oge", kutu=list(b)))
    paket, kapak_dir = paths(part)
    png = os.path.join(kapak_dir, f"kapak_P{part}_{kod}.png")
    im.save(png, "PNG", optimize=True)
    small = im.resize((1280, 720), Image.LANCZOS)
    jpg = os.path.join(paket, f"kapak_P{part}_{kod}.jpg")
    icc = _srgb_icc()
    q = 94
    while True:
        kw = dict(quality=q, optimize=True, subsampling=0)
        if icc:
            kw["icc_profile"] = icc
        small.save(jpg, "JPEG", **kw)
        if os.path.getsize(jpg) < 1_900_000 or q <= 70:
            break
        q -= 4
    lay = dict(kapak=kod, parca=part, boyut=[1280, 720], jpg=os.path.relpath(jpg, HERE), png=os.path.relpath(png, HERE), jpg_kalite=q,
               tur=sp["tur"], zaman=sp["zaman"], aciklama=sp["aciklama"], yazi_tipi=f"fonts/{FONT_FILE} (Cinzel Black 900)",
               kapak_zemini=dict(KAPAK_ZEMIN.get(kod, {}), golge=list(KAPAK_GOLGE)),
               yasak_bolgeler=dict(sure_rozeti=list(SURE_ROZETI), fare_simgeleri=list(FARE_SIMGE)), ogeler=ogeler)
    with open(os.path.join(kapak_dir, f"kapak_P{part}_{kod}.yerlesim.json"), "w", encoding="utf-8") as fh:
        json.dump(lay, fh, ensure_ascii=False, indent=1)
    print(f"{jpg}  {os.path.getsize(jpg) // 1000} KB (q={q})   {png}")
    return jpg


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--part", type=int, default=1)
    ap.add_argument("--kod", choices=sorted(KAPAK_SAHNE), action="append", help="yalnız bu kapak(lar)")
    ap.add_argument("--kontrol", action="store_true", help="kapak_qa.py denetimi (üretmeden)")
    a = ap.parse_args()
    if a.part not in PART_TEXT:
        sys.exit(f"Parça {a.part} için kapak metni yok (PART_TEXT).")
    if not a.kontrol:
        for kod in (a.kod or sorted(PART_TEXT[a.part])):
            cover(a.part, kod)
    import kapak_qa
    sys.exit(kapak_qa.main(["--part", str(a.part)]))


if __name__ == "__main__":
    main()
