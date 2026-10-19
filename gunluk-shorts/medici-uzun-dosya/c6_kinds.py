"""c6_kinds — c6 «Lorenzo» özel çekim türleri (Parça 3 sahne yazarı). `scenes_c6.py` içinde import edilir; `@CM.ckind` ile kaydolur.

Dil: gündüz, sıcak sıva-kâğıt (perde ALTIN); anlatı sıcak ve hafif; Giostra'dan sonra ışık soğur (kapı: Giuliano).
Kaynak disiplini: yüz yok (stilize madalya/siluet), şiddet yok; ekrana yalnız script/brif sözcükleri yazılır. Ten rengi/ses/koku alayı YOK.
Tüm zamanlar cümle/sözcük çapalı (cx.at / cx.amt); mutlak saniye yok.
"""
import math

import numpy as np
import skia

import cilt_anim as FA
import cilt_kinds2 as K2
import cilt_medal as CMD
import cilt_medici as CM
import cilt_paper as PP
import icons
import p3_lib as L
import sk
from cilt_medici import TH
from p3_lib import INK, P, S, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth
from sk import C, H, W

INK_BROWN = "#2A180D"


def look(wx, wy, z=1.0, rot=0.0):
    """Anahtar kare: dünya (wx,wy) noktası ekran merkezinde, zoom z (cam=[(çapa, look(...)), …])."""
    return (z * (wx - W / 2), z * (wy - H / 2), z, rot)


def _glint(cx, at, period=1.0):
    k = clamp((cx.t - cx.at(at)) / period)
    return k if 0.0 < k < 1.0 else None


# ═════════════════════════════ c6s1–c6s2: Valori sayfası + Lorenzo madalyası ═════════════════════════════
@CM.ckind("c6_valori")
def k_valori(cx, a_page=0.0, a_med=0.0, l1=None, l2=None, l3=None, l4=None, a_gl=None, seed=3, **_):
    """Parşömen sayfa (sol) + Lorenzo madalyası (sağ). Sayfa: «NİCCOLÒ VALORİ — yakın dost», satırlar tüy kalemle yazılır; madalya mürekkep çizgisinden bronza dönüşür.
    l1..l4 = (metin, çapa): 1–2 → c6s1 (üvey ana / şefkatli ana), 3–4 → c6s2 (yüzü güzel sayılmazdı / vakarlıydı). a_med: madalyanın bronzlaştığı an; a_gl: yaldız parıltısı."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_page, 0.9)
    pw, ph = 860, 700
    pcx, pcy = 600, 520
    pp = PP.paper_image(pw, ph, seed, (238, 228, 198), "deckle", (), 44, 1.0)
    rot = -0.014 + 0.006 * math.sin(cx.t * 0.5)
    pp.draw(f, pcx, pcy, rot=rot, scale=0.97 + 0.03 * ease_out(a), alpha=a, shadow=0.6)
    c.save()
    c.translate(pcx, pcy)
    c.rotate(math.degrees(rot))
    # başlık: NİCCOLÒ VALORİ (oyma) + alt çizgi + "yakın dost"
    y = -ph / 2 + 112
    sp = CM.engraved("NİCCOLÒ VALORİ", "title_m", 50, 6.0, "#3A2616", 0.7)
    CM.draw_spr(f, sp, 0, y, "c", alpha=a * cx.amt(a_page, 0.7, off=0.3))
    CM.flourish_rule(f, 0, y + 30, 520, alpha=0.8 * a, color="#7A5A2E", grow=cx.amt(a_page, 0.8, off=0.5))
    CM.ink(f, "yakın dost", 0, y + 74, face="cap_i", size=34, color=TH.fg2, align="c", alpha=a * cx.amt(a_page, 0.6, off=0.7), emboss=False)
    ys = [y + 168, y + 244, y + 360, y + 436]
    lines = [l1, l2, l3, l4]
    quill = None
    for i, ln in enumerate(lines):
        if ln is None:
            continue
        txt, an = ln
        sz = 52 if i in (0, 2) else 50
        col = INK_BROWN
        res = K2.write_line(f, cx, txt, -ph * 0.5 + 76, ys[i], cx.at(an), "fell_i", sz, col, a, seed=60 + i, align="l")
        if res and 0.0 < res[0] < 1.0:
            quill = (res[1], res[2])
    # c6s2 ayracı: ince mürekkep çizgisi
    kk = cx.amt(l3[1], 0.5, off=-0.3) if l3 else 0.0
    if kk > 0:
        c.drawLine(-ph * 0.5 + 76, y + 300, -ph * 0.5 + 76 + 540 * kk, y + 300, S("#7A5A2E", 1.6, 150))
    c.restore()
    if quill is not None and quill[0] is not None:
        # kalem sayfa dönüşümünde; ekran koordinatına çevir
        ca, sa = math.cos(rot), math.sin(rot)
        qx = pcx + quill[0] * ca - quill[1] * sa
        qy = pcy + quill[0] * sa + quill[1] * ca
        K2.draw_quill(f, qx, qy, ang=-38.0, alpha=a)
    # madalya: önce mürekkep halka (çizim), sonra bronz
    mx, my, ms = 1440, 500, 600
    km = cx.amt(a_med, 1.1)
    ring_a = cx.amt(a_page, 0.9, off=0.6) * (1.0 - 0.85 * km)
    if ring_a > 0.01:
        pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.0, Color=C("#5A3E22", int(190 * ring_a)), StrokeCap=skia.Paint.kRound_Cap)
        pr.setPathEffect(skia.DashPathEffect.Make([18, 12], -cx.t * 22))
        c.drawCircle(mx, my, ms * 0.47, pr)
    if km > 0.01:
        gl = _glint(cx, a_gl, 1.3) if a_gl is not None else None
        CMD.draw_medal_b(f, "m_lorenzo", mx, my, ms * (0.93 + 0.07 * ease_out(km)), "bronze", alpha=km, tilt=0.16 * math.sin(cx.t * 0.55 + 0.4), glint=gl)
        CM.name_plate(f, "LORENZO DE' MEDİCİ", None, None, cx_=mx, y=my + ms * 0.54, t=cx.amt(a_med, 0.7, off=0.4), w=560)
    cam.end(f)
    CM.finish(f, cx, motes_n=24)


# ═════════════════════════════ c6s3–c6s4: ansiklopedi tarifi (ölçü çizgileri) + koku göstergesi ═════════════════════════════
@CM.ckind("c6_tarif")
def k_tarif(cx, a_head=0.0, a_nose=None, a_chin=None, a_eye=None, a_smell=None, a_attr=None, seed=5, **_):
    """Lorenzo madalyası + ince mürekkep ölçü çizgileri (Rönesans etüt sayfası): BASIK BURUN · ÖNE ÇIKIK ALT ÇENE · ZAYIF GÖRME (c6s3);
    ardından KOKU DUYUSU göstergesi (neredeyse boş) + «Valori'ye atfedilen tarif» (c6s4). Sakin, alaysız."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    mx, my, ms = 640, 530, 740
    ka = cx.amt(a_head, 0.9)
    s = ms / 640.0
    # madalya merkezine göre öznitelik noktaları (kalibre)
    P_nose = (mx + 156 * s, my + 16 * s)
    P_chin = (mx + 130 * s, my + 124 * s)
    P_eye = (mx + 80 * s, my - 50 * s)
    CMD.draw_medal_b(f, "m_lorenzo", mx, my, ms * (0.96 + 0.04 * ease_out(ka)), "bronze", alpha=ka, tilt=0.10 * math.sin(cx.t * 0.5), glint=None)
    # üst başlık
    hx = 1420
    kh = cx.amt(a_head, 0.7, off=0.4)
    if kh > 0.01:
        CM.ink(f, "ANSİKLOPEDİLERİN TARİFİ", hx, 238, face="title_m", size=34, color=TH.fg2, align="c", track=7, alpha=kh, emboss=False)
        CM.flourish_rule(f, hx, 262, 520, alpha=0.7 * kh, color="#7A5A2E", grow=kh)
    items = [("BASIK BURUN", P_nose, a_nose, 500), ("ÖNE ÇIKIK ALT ÇENE", P_chin, a_chin, 660), ("ZAYIF GÖRME", P_eye, a_eye, 340)]
    for name, pt, an, ly in items:
        if an is None:
            continue
        k = cx.amt(an, 0.7)
        if k <= 0.003:
            continue
        # kılavuz: özellikten etikete ince çizgi (çiziliyormuş gibi)
        lx = hx - 230
        kk_ = ease_io(k)
        ex = pt[0] + (lx - 14 - pt[0]) * kk_
        ey = pt[1] + (ly - pt[1]) * kk_
        c.drawLine(pt[0], pt[1], ex, ey, S("#4A3420", 2.0, 210))
        c.drawCircle(pt[0], pt[1], 7.5, P("#A8321E", 235 * k))
        c.drawCircle(pt[0], pt[1], 7.5, S(INK, 1.5, 210 * k))
        wd = sk.text_width(name, "cap_b", 40) + 64
        kk = cx.amt(an, 0.5, off=0.35)
        CM.tablet(f, lx, ly - 36 + (1 - kk) * 8, wd, 72, alpha=kk, corner=8)
        CM.ink(f, name, lx + wd / 2, ly + 12 + (1 - kk) * 8, face="cap_b", size=40, color=TH.fg, align="c", alpha=kk, emboss=False)
    # koku göstergesi
    if a_smell is not None:
        k = cx.amt(a_smell, 0.8)
        if k > 0.003:
            gx, gy, gw = hx - 250, 800, 500
            CM.ink(f, "Valori'ye atfedilen tarif", gx + gw / 2, gy - 98, face="cap_i", size=34, color=TH.fg3, align="c", alpha=0.95 * k, emboss=False)
            CM.ink(f, "KOKU DUYUSU", gx + gw / 2, gy - 44, face="title_m", size=36, color=TH.fg, align="c", track=7, alpha=k, emboss=False)
            c.save()
            c.translate(gx, gy)
            c.drawRoundRect(skia.Rect.MakeWH(gw, 26), 13, 13, P("#E8DCB8", 230 * k))
            c.drawRoundRect(skia.Rect.MakeWH(gw, 26), 13, 13, S("#4A3420", 2.0, 220 * k))
            fill = (0.045 + 0.012 * math.sin(cx.t * 1.7)) * ease_out(clamp((cx.t - cx.at(a_smell)) / 1.2))
            c.drawRoundRect(skia.Rect.MakeWH(max(8, gw * fill), 26), 13, 13, P("#A8321E", 235 * k))
            for i in range(1, 5):
                c.drawLine(gw * i / 5, 26, gw * i / 5, 36, S("#4A3420", 1.6, 160 * k))
            c.restore()
            CM.ink(f, "neredeyse yok", gx + gw / 2, gy + 82, face="cap_i", size=40, color=TH.fg2, align="c", alpha=cx.amt(a_smell, 0.6, off=0.6), emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)
