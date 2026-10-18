"""Bölüm 6 (Kral, Esir, Düello) özel çekim türleri ve sahneleri. Ad önteki: c6_*"""
import math

import numpy as np
import skia

import icons
import medal
import props_war as PW
import scenes_lib as SL
import shots as SH
import sk
import stage as ST
import stage_c678 as X
from sk import C, H, clamp, ease_in, ease_io, ease_out, back_out, lerp, mix, seg, smooth
from sk import W as SW
from stage import MARGIN

CX = SW / 2


# ───────────────────────────── kâğıt yardımcısı ─────────────────────────────
class Paper:
    """with Paper(f, x, y, w, h, ...) as p: içinde (0,0) = kâğıt merkezi."""

    def __init__(self, f, x, y, w, h, seed=3, tone="#DCCB9E", rot=0.0, sc=1.0, alpha=1.0, tx=0.0, ty=0.0):
        self.f, self.x, self.y, self.w, self.h = f, x, y, w, h
        self.seed, self.tone, self.rot, self.sc, self.alpha = seed, tone, rot, sc, alpha

    def __enter__(self):
        f = self.f
        img, pad = SH.paper_sprite(self.w, self.h, seed=self.seed, tone=self.tone)
        f.c.save()
        f.c.translate(self.x, self.y)
        if self.rot:
            f.c.rotate(math.degrees(self.rot))
        f.c.scale(self.sc, self.sc)
        p = skia.Paint(AntiAlias=True)
        p.setAlphaf(clamp(self.alpha))
        f.c.drawImage(img, -self.w / 2 - pad, -self.h / 2 - pad, skia.SamplingOptions(skia.FilterMode.kLinear), p)
        return self

    def __exit__(self, *a):
        self.f.c.restore()


INK = "#2A1A0C"


def scribble(f, x0, x1, y, k=1.0, seed=1, amp=3.2, color=INK, sw=2.2, alpha=0.5):
    """El yazısı izlenimi veren dalgalı mürekkep çizgisi (okunur metin değil)."""
    if k <= 0:
        return
    rs = np.random.RandomState(seed)
    pts = []
    x = x0
    while x < lerp(x0, x1, clamp(k)):
        pts.append((x, y + math.sin(x * 0.22 + seed) * amp + (rs.rand() - 0.5) * amp * 1.2))
        x += 7
    if len(pts) > 2:
        f.path(sk.smooth_path(pts, False, 0.4), style="stroke", sw=sw, color=color, alpha=alpha)


def treaty(f, x, y, w, h, t_strike=1.0, t_seal=1.0, strike_at=(1.0, 1.0), rot=-0.015, sc=1.0, alpha=1.0, lines_k=1.0, seal_col="#27427A", title_k=1.0):
    """Madrid Antlaşması belgesi (okunur satırlar: iddia vazgeçişleri). t_strike: üstü çizme ilerlemesi (2 satır için ayrı)."""
    with Paper(f, x, y, w, h, seed=21, rot=rot, sc=sc, alpha=alpha):
        yy = -h / 2 + 96
        f.text("MADRİD ANTLAŞMASI", 0, yy, face="fell", size=SH.fit_size("MADRİD ANTLAŞMASI", "fell", 50, w - 140, 2), color=INK, align="c", track=2, alpha=alpha * title_k)
        f.line(-w * 0.34, yy + 20, w * 0.34, yy + 20, color=INK, sw=1.6, alpha=0.6 * alpha * title_k)
        f.text("1526", 0, yy + 66, face="fell_i", size=34, color="#5A3E1E", align="c", alpha=alpha * 0.85 * title_k)
        items = [("İtalya üzerindeki iddia", lines_k if not isinstance(lines_k, (tuple, list)) else lines_k[0]),
                 ("Flandre üzerindeki iddia", lines_k if not isinstance(lines_k, (tuple, list)) else lines_k[1])]
        y0 = yy + 150
        for i, (s, kk) in enumerate(items):
            ya = y0 + i * 96
            if kk > 0:
                wt = sk.text_width(s, "fell", 40, 0)
                f.c.save()
                f.c.clipRect(skia.Rect.MakeXYWH(-w / 2 + 60, ya - 44, (wt + 40) * clamp(kk), 70))
                f.text(s, -w / 2 + 84, ya, face="fell", size=40, color=INK, align="l", alpha=alpha)
                f.c.restore()
                f.circle(-w / 2 + 62, ya - 12, 5, color=INK, alpha=0.8 * alpha * clamp(kk))
            ks = t_strike if not isinstance(t_strike, (tuple, list)) else t_strike[i]
            X.strike_line(f, -w / 2 + 70, ya - 12, -w / 2 + 84 + sk.text_width(s, "fell", 40, 0) + 20, ya - 16, ks, sw=7, alpha=0.92 * alpha)
        # imza karalaması + mühür
        scribble(f, -w / 2 + 110, -w / 2 + 360, h / 2 - 96, k=clamp(t_seal * 1.4), seed=7, amp=7, sw=3, alpha=0.7 * alpha)
        SH.wax_seal(f, w / 2 - 150, h / 2 - 100, 62, color=seal_col, t=t_seal, alpha=alpha, mono="F")


# ───────────────────────────── c6_antlasma ─────────────────────────────
@SH.kind("c6_antlasma")
def k_antlasma(cx, key="fransuva", metal="royal", at_medal=0.0, at_title=0.0, at_l1=0.0, at_l2=0.0, at_strike=0.0, at_seal=0.0, at_chip=0.0):
    """François madalyası (ESİR) + Madrid Antlaşması: iki iddia tek tek yazılır, vazgeçilir, mühür basılır."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.28)
    X.tone(f, "#27427A", 0.16, cy=0.5)
    sk.dust(f, cx.t, n=50)
    am = cx.amt(at_medal, 0.8)
    mx, my = 470, 520
    X.glow(f, mx, my, 330, "#6C92E0", 0.16 * am)
    SH.draw_medal(f, key, mx, my, 520 * (0.94 + 0.06 * ease_out(am)) * (1 + 0.03 * cx.u), metal, False, alpha=am, tilt=0.18 * math.sin(cx.t * 0.55 + 0.4))
    X.chip(f, "ESİR", mx, my + 330, k=cx.amt(at_chip, 0.4), size=32, edge="#B02A2A", color="#F4D6CF")
    # belge
    ta = cx.amt(at_title, 0.7)
    l1 = cx.amt(at_l1, 0.7)
    l2 = cx.amt(at_l2, 0.7)
    s1 = ease_out(clamp((cx.t - cx.at(at_strike)) / 0.5))
    s2 = ease_out(clamp((cx.t - cx.at(at_strike, off=0.35)) / 0.5))
    sl = cx.amt(at_seal, 0.35)
    sc = (0.94 + 0.06 * ease_out(ta)) * (1 + 0.04 * cx.u)
    treaty(f, 1290, 540, 820, 700, t_strike=(s1, s2), t_seal=sl, rot=-0.02 * (1 - 0.4 * cx.u), sc=sc, alpha=ta, lines_k=(l1, l2), title_k=ta)
    f.vig(0.6)


# ───────────────────────────── c6_rehin ─────────────────────────────
def _bars(f, x0, x1, y0, y1, step=118, w=17, alpha=1.0):
    n = int((x1 - x0) / step) + 1
    for i in range(n):
        x = x0 + i * step
        f.rect(x - w / 2 + 5, y0, w, y1 - y0, color="#000000", alpha=0.35 * alpha, blur=5)
        f.rect(x - w / 2, y0, w, y1 - y0, shader=f.lin(x - w / 2, 0, x + w / 2, 0, [("#16181B", 0.0), ("#6E747C", 0.35), ("#2B2F34", 0.7), ("#0D0E10", 1.0)]), alpha=alpha)
        f.rect(x - w / 2 + 2, y0, 2.5, y1 - y0, color="#C8D0D8", alpha=0.25 * alpha)
    for yy in (y0 + 40, y1 - 130):
        f.rect(x0 - 40, yy - 12, (x1 - x0) + 80, 24, shader=f.lin(0, yy - 12, 0, yy + 12, [("#6E747C", 0.0), ("#1A1C1F", 1.0)]), alpha=alpha)


def _cell_back(f):
    f.rect(0, 0, SW, H, shader=f.lin(0, 0, 0, H, [("#2C231C", 0.0), ("#120D0A", 1.0)]))
    for r in range(11):
        yy = r * 100
        f.line(0, yy, SW, yy, color="#000000", sw=2.0, alpha=0.35)
        off = 0 if r % 2 == 0 else 120
        for c in range(0, 18):
            f.line(off + c * 240, yy, off + c * 240, yy + 100, color="#000000", sw=2.0, alpha=0.3)
    # yüksek pencere + soğuk ay ışığı huzmesi
    wx, wy = 1250, 330
    f.path(ST.pointed_arch_path(wx, wy + 150, 190, 330), color="#05060A")
    f.path(ST.pointed_arch_path(wx, wy + 150, 150, 290), shader=f.lin(0, wy - 140, 0, wy + 150, [("#9CB8D8", 0.0), ("#3A5578", 1.0)]))
    sk.light_rays(f, (wx, wy + 80), math.radians(104), 0.36, 1300, n=6, alpha=0.20, color="#9CB8D8", seed=4, blur=22)
    f.rect(0, 0, SW, H, shader=f.rad(wx - 250, wy + 300, 1200, [("#000000", 0.0, 0), ("#000000", 0.55, 40), ("#000000", 1.0, 170)]))


@SH.kind("c6_rehin")
@X.pushy(0.035)
def k_rehin(cx, at=0.0, at_stamp=0.0, at_chip=None):
    """Hücre: iki oğul (siluet), demir parmaklıklar, soğuk ay ışığı; REHİN damgası."""
    f = cx.f
    f.c.drawImage(sk.baked(("c6_cell",), _cell_back), 0, 0)
    a = cx.amt(at, 0.7)
    sway = math.sin(cx.t * 1.1) * 0.006
    # ay ışığı lekesi zeminde
    f.path(sk.poly_path([(1150, 880), (1350, 880), (1500, 1100), (1000, 1100)]), color="#9CB8D8", alpha=0.07 * a)
    ST.figure(f, "page", 880, 1040 + (1 - a) * 30, 720, col="#070505", rim="#8EA8C8", face=1, alpha=a, sway=sway)        # iki oğul: biri ergenliğe yakın, biri çocuk
    ST.figure(f, "child", 1250, 1050 + (1 - a) * 30, 660, col="#070505", rim="#8EA8C8", face=-1, alpha=a, sway=-sway)
    _bars(f, 130, 1790, -30, H + 10, alpha=1.0)
    SH.kicker(f, "İKİ OĞLU", CX, 168, alpha=cx.amt(at, 0.7, off=0.15), size=34, track=14, face="title_m", color="#E0C682")
    t = cx.amt(at_stamp, 0.3)
    if t > 0:
        SH.stamp(f, "REHİN", CX, H * 0.74, rot=-0.07, size=96, t=t)
    f.vig(0.6)


# ───────────────────────────── c6_yirt ─────────────────────────────
def _treaty_base():
    def b(f):
        f.clear(skia.ColorTRANSPARENT)
        treaty(f, CX, 540, 820, 700, t_strike=(1.0, 1.0), t_seal=1.0, rot=0.0, lines_k=(1.0, 1.0))
    return sk.baked(("c6_treaty_base",), b)


@SH.kind("c6_yirt")
def k_yirt(cx, at_flare=0.0, at_tear=0.0, at_stamp=0.0, at_note=None):
    """Antlaşma yırtılır: çatlak büyür, iki yarı ayrılır, GEÇERSİZ damgası."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.25)
    X.tone(f, "#8E1F26", 0.10, cy=0.5)
    sk.dust(f, cx.t, n=40)
    img = _treaty_base()
    t_tear = cx.at(at_tear)
    crack = clamp((cx.t - (t_tear - 0.4)) / 0.4)
    sep = ease_out(clamp((cx.t - t_tear) / 1.0), 3)
    # özgürlük ışığı (sol üstten)
    fl = cx.amt(at_flare, 0.5) * (1 - cx.amt(at_flare, 0.9, off=0.9))
    if fl > 0:
        sk.light_rays(f, (-100, -80), math.radians(40), 0.8, 1600, n=5, alpha=0.16 * fl, color="#FFE2A0", seed=2, blur=18)
    top, bot = 540 - 350, 540 + 350
    # çatlak çizgisi (pürüzlü, yukarıdan aşağı)
    pts = X.jag_points(CX + 10, top - 20, CX - 14, bot + 20, n=16, amp=22, seed=5)
    left_poly = [(CX - 440, top - 60)] + pts + [(CX - 440, bot + 60)]
    right_poly = [(CX + 440, top - 60)] + pts + [(CX + 440, bot + 60)]
    dx = sep * 130
    for side, poly, sgn in (("l", left_poly, -1), ("r", right_poly, 1)):
        f.c.save()
        f.c.translate(CX + sgn * dx, 540 + sep * 18 * sgn)
        f.c.rotate(sgn * 7.0 * sep)
        f.c.translate(-CX, -540)
        if sep > 0:
            f.c.save()
            f.c.translate(sgn * 10, 18)
            f.path(X_poly(poly), color="#000000", alpha=0.55 * sep, blur=14)
            f.c.restore()
        f.c.clipPath(X_poly(poly), skia.ClipOp.kIntersect, True)
        f.c.drawImage(img, 0, 0)
        f.c.restore()
    if crack > 0 and sep < 0.02:
        n = max(2, int(len(pts) * crack))
        f.path(sk.poly_path(pts[:n], False), style="stroke", sw=5, color="#1A0F08", alpha=0.9)
    t = cx.amt(at_stamp, 0.3)
    if t > 0:
        SH.stamp(f, "GEÇERSİZ", CX, 560, rot=-0.17, size=150, t=t)
    if at_note is not None:
        kk = cx.amt(at_note, 0.7)
        if kk > 0:
            SH.kicker(f, "ESİRİN SÖZÜ", CX, 150, alpha=kk, size=34, track=14, face="title_m", color="#E0C682")
    f.vig(0.62)


def X_poly(pts):
    return sk.poly_path(pts, True)


# ───────────────────────────── c6_maas ─────────────────────────────
@SH.kind("c6_maas")
@X.pushy(0.035)
def k_maas(cx, at=0.0, at_strike=0.0, at_men=0.0):
    """Maaş ödenmedi: para yığını üstü çizilir; alttan öfkeli asker siluetleri yükselir."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.3)
    X.tone(f, "#C0391B", 0.14, cy=0.55)
    sk.dust(f, cx.t, n=60)
    # asker siluetleri (arkada, alttan yükselir)
    am = ease_out(clamp((cx.t - cx.at(at_men)) / 1.1), 2)
    kinds = ["landsknecht", "pikeman", "landsknecht", "pikeman", "landsknecht", "pikeman", "landsknecht", "pikeman", "landsknecht"]
    for i, kd in enumerate(kinds):
        xx = 170 + i * 200 + (i % 2) * 40
        hh = 400 + (i % 3) * 26
        ST.figure(f, kd, xx, H + 90 - am * 130 + math.sin(cx.t * 3 + i) * 3, hh, col="#080504", rim="#C58A44", face=1 if i < 5 else -1, alpha=am)
    f.rect(0, 0, SW, H, shader=f.lin(0, H * 0.45, 0, H * 0.75, [("#000000", 0.0, 0), ("#000000", 1.0, 0)]))
    a = cx.amt(at, 0.6)
    ks = ease_out(clamp((cx.t - cx.at(at_strike)) / 0.45))
    shake = math.sin(cx.t * 30) * 5 * (1 - cx.amt(at_strike, 0.5, off=0.5)) * ks
    cxp, cyp = CX + shake, 400
    X.glow(f, cxp, cyp, 360, "#E3B54A", 0.24 * a * (1 - 0.7 * ks))
    X.ic(f, "coins", cxp, cyp, size=470 * (0.9 + 0.1 * back_out(a)), metal="gold", alpha=a * (1 - 0.30 * ks), glow=0.35 * a)
    X.strike_line(f, cxp - 260, cyp - 220, cxp + 260, cyp + 220, ks, sw=22)
    X.strike_line(f, cxp + 260, cyp - 220, cxp - 260, cyp + 220, clamp(ks * 1.6 - 0.6), sw=22)
    X.chip(f, "MAAŞ ALINAMADI", CX, 690, k=cx.amt(at_strike, 0.5, off=0.2), size=46, edge="#B02A2A", color="#F8E2D8", padx=34)
    f.vig(0.65)


# ───────────────────────────── c6_mektup ─────────────────────────────
@SH.kind("c6_mektup")
def k_mektup(cx, key="fransuva", at_a="bana", at_b="kaldı", at_hedge=0.0, at_seal=0.0, at_slip=0.0, at_stamp=0.0, slogan="ŞEREF DIŞINDA HER ŞEY KAYIP"):
    """1) Annesine mektup (okunur tek satır: aktarılan söz; gerisi karalama). 2) Üstüne yapıştırılmış 'sonradan' kâğıt şeridi: ünlü söz + damga."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.28)
    X.tone(f, "#27427A", 0.12, cy=0.5)
    sk.dust(f, cx.t, n=50)
    k2 = ease_io(clamp((cx.t - cx.at(at_slip)) / 0.9))
    a1 = clamp(cx.amt(0.0, 0.8))
    # François küçük madalya (sol)
    SH.draw_medal(f, key, 340, 520, 380 * (0.94 + 0.06 * ease_out(a1)), "royal", False, alpha=a1 * (1 - 0.85 * k2), tilt=0.16 * math.sin(cx.t * 0.55))
    # mektup
    px = lerp(1180, 960, k2 * 0.0) - k2 * 90
    sc = (0.96 + 0.04 * ease_out(a1)) * (1 + 0.03 * cx.u) * (1 - 0.1 * k2)
    with Paper(f, px, 520 + k2 * 40, 1000, 660, seed=31, rot=-0.02 + 0.02 * k2, sc=sc, alpha=a1 * (1 - 0.72 * k2)) as p:
        f.text("ANNESİNE MEKTUP", 0, -250, face="fell", size=46, color=INK, align="c", track=2, alpha=cx.amt(0.4, 0.5))
        f.line(-300, -230, 300, -230, color=INK, sw=1.6, alpha=0.6)
        for i in range(2):
            scribble(f, -400, 330 - i * 90, -170 + i * 52, k=clamp((cx.t - (0.7 + i * 0.35)) / 0.8), seed=3 + i)
        # aktarılan söz
        s = "“bana şeref ve canım kaldı”"
        wt = sk.text_width(s, "fell_i", 62, 0)
        ta, tb = cx.at(at_a), cx.at(at_b, off=0.55)
        rv = clamp((cx.t - ta) / max(0.2, tb - ta))
        f.c.save()
        f.c.clipRect(skia.Rect.MakeXYWH(-wt / 2 - 16, -52, (wt + 32) * rv, 100))
        f.text(s, 0, 10, face="fell_i", size=62, color="#1C0F06", align="c", alpha=1.0)
        f.c.restore()
        hl = clamp((cx.t - tb) / 0.5)
        f.rect(-wt / 2, 18, wt * hl, 6, color="#C9962B", alpha=0.9 * hl)
        for i in range(3):
            scribble(f, -400, 360 - i * 110, 110 + i * 54, k=clamp((cx.t - (tb + 0.2 + i * 0.3)) / 0.8), seed=8 + i)
        SH.wax_seal(f, 330, 235, 56, color="#27427A", t=cx.amt(at_seal, 0.35), mono="F")
    # 'aktarıldığına göre' notu
    hk = cx.amt(at_hedge, 0.7) * (1 - k2)
    if hk > 0:
        SH.kicker(f, "AKTARILDIĞINA GÖRE", 1180 - 50, 930, alpha=hk, size=28, track=9, face="cap_i", color="#C9B27A")
    # 2) sonradan eklenen şerit
    if k2 > 0:
        sy = lerp(H * 0.62, H * 0.5, k2)
        with Paper(f, CX, sy, 1420, 230, seed=44, tone="#F6F0DE", rot=0.03 * (1 - 0.3 * k2), sc=0.92 + 0.08 * k2, alpha=k2) as p2:
            sz = SH.fit_size(slogan, "title", 60, 1280, 4)
            f.text(slogan, 0, 22, face="title", size=sz, color="#2B1D10", align="c", track=4, alpha=k2)
            for sx in (-1, 1):
                f.rect(sx * 700 - 40, -118, 80, 36, color="#E3B54A", alpha=0.55 * k2)
        # sınıf damgası
        t = cx.amt(at_stamp, 0.3)
        if t > 0:
            SH.stamp(f, "SONRADAN YAYGINLAŞTI", CX + 20, H * 0.885, rot=-0.05, size=62, t=t)
    f.vig(0.6)


# ───────────────────────────── c6_muhafiz (189 / 147) ─────────────────────────────
_GUARD = {}


def guard_sprite(h, col, rim):
    key = (int(h), col, rim)
    if key in _GUARD:
        return _GUARD[key]
    w, hh = int(h * 0.95), int(h * 1.5)
    s = skia.Surface(w, hh)
    c = s.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    ox, oy = w * 0.42, hh - 3

    def body(dx, dy, color):
        pa = skia.Paint(AntiAlias=True, Color=C(color))
        c.save()
        c.translate(ox + dx, oy + dy)
        P = skia.Path()
        # gövde
        P.addPoly([(-0.15 * h, -0.76 * h), (0.15 * h, -0.76 * h), (0.14 * h, -0.42 * h), (-0.14 * h, -0.42 * h)], True)
        # bacaklar
        for sx in (-1, 1):
            P.addPoly([(sx * 0.02 * h, -0.42 * h), (sx * 0.13 * h, -0.42 * h), (sx * 0.11 * h, -0.02 * h), (sx * 0.15 * h, 0), (sx * 0.02 * h, 0)], True)
        # kafa + bere
        P.addCircle(0, -0.86 * h, 0.07 * h)
        P.addOval(skia.Rect.MakeLTRB(-0.15 * h, -1.0 * h, 0.12 * h, -0.9 * h))
        # kol + kargı (halberd)
        P.addPoly([(0.12 * h, -0.72 * h), (0.24 * h, -0.62 * h), (0.24 * h, -0.56 * h), (0.12 * h, -0.64 * h)], True)
        P.addRect(skia.Rect.MakeLTRB(0.225 * h, -1.34 * h, 0.255 * h, 0.0))
        P.addPoly([(0.24 * h, -1.46 * h), (0.27 * h, -1.32 * h), (0.21 * h, -1.32 * h)], True)
        P.addPoly([(0.255 * h, -1.30 * h), (0.40 * h, -1.20 * h), (0.255 * h, -1.12 * h)], True)
        c.drawPath(P, pa)
        c.restore()

    body(-1.4, -1.4, rim)
    body(0, 0, col)
    img = s.makeImageSnapshot()
    _GUARD[key] = (img, ox, oy)
    return _GUARD[key]


@SH.kind("c6_muhafiz")
@X.pushy(0.035)
def k_muhafiz(cx, at_total=0.0, at_dead=0.0, dead_dur=1.5, cols=27, rows=7, dead_cols=21, label="İSVİÇRELİ MUHAFIZLAR", total=189, dead=147):
    """189 küçük muhafız siluet; 147'si (21 sütun) soldan sağa devrilir. Sayaç: 189 → 147 / 189."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.25)
    X.tone(f, "#4B2D63", 0.14, cy=0.5)
    sk.dust(f, cx.t, n=45)
    gh, dx, dy = 72, 58, 84
    x0 = CX - (cols - 1) * dx / 2
    y0 = 290
    a_t = cx.amt(at_total, 0.6)
    SH.kicker(f, label, CX, 190, alpha=a_t, size=34, track=14, face="title_m", color="#E0C682")
    t_build = cx.at(at_total)
    t_dead = cx.at(at_dead)
    f.line(x0 - 60, y0 + rows * dy - 4, x0 + (cols - 1) * dx + 60, y0 + rows * dy - 4, color="#7A5518", sw=2, alpha=0.5 * a_t)
    alive_img, ox, oy = guard_sprite(gh, "#D9A83A", "#FBE7A0")
    dead_img, dox, doy = guard_sprite(gh, "#5A2020", "#8A3A32")
    for c_ in range(cols):
        for r in range(rows):
            xx = x0 + c_ * dx
            yy = y0 + r * dy + gh + 10
            tb = t_build + c_ * 0.028 + r * 0.012
            ka = clamp((cx.t - tb) / 0.28)
            if ka <= 0:
                continue
            kd = clamp((cx.t - (t_dead + c_ / dead_cols * dead_dur + r * 0.035)) / 0.4) if c_ < dead_cols else 0.0
            f.c.save()
            f.c.translate(xx, yy + (1 - ease_out(ka)) * 16)
            p = skia.Paint(AntiAlias=True)
            if kd > 0:
                f.c.rotate(86 * ease_in(kd, 2) * (1 if (r + c_) % 2 == 0 else -1) * 0.92)
                p.setAlphaf(ka * (1 - 0.35 * kd))
                im, ix, iy = (dead_img, dox, doy) if kd > 0.35 else (alive_img, ox, oy)
                f.c.drawImage(im, -ix, -iy, skia.SamplingOptions(skia.FilterMode.kLinear), p)
            else:
                p.setAlphaf(ka)
                f.c.drawImage(alive_img, -ox, -oy, skia.SamplingOptions(skia.FilterMode.kLinear), p)
            f.c.restore()
    # hayatta kalanların yumuşak parıltısı (radyal)
    kd_all = clamp((cx.t - (t_dead + dead_dur)) / 0.6)
    if kd_all > 0:
        xs = x0 + dead_cols * dx - dx / 2
        xe = x0 + (cols - 1) * dx + dx / 2
        xm, ym = (xs + xe) / 2, y0 + rows * dy / 2
        pulse = 0.65 + 0.35 * math.sin(cx.t * 3.0)
        f.circle(xm, ym, 340, shader=f.rad(xm, ym, 340, [("#F0D27A", 0.0, int(60 * kd_all * pulse)), ("#F0D27A", 1.0, 0)]), blend=skia.BlendMode.kPlus)
    # sayaçlar: 189 → 147 / 189
    sw_ = ease_io(clamp((cx.t - t_dead) / 0.6))
    ky = ease_out(clamp((cx.t - t_dead) / dead_dur), 2)
    yb = 1000
    if a_t > 0:
        w84 = sk.text_width(str(total), "title", 84, 6)
        c_final = CX + 92 + w84 / 2
        SH.gold_flat(f, str(total), lerp(CX, c_final, sw_), yb, face="title", size=lerp(120, 84, sw_), track=6, alpha=a_t * (1 - 0.15 * sw_))
        if sw_ > 0:
            SH.gold_flat(f, "/", CX + 38, yb, face="title", size=84, track=6, alpha=sw_ * 0.8)
            col = mix("#F0D27A", "#E0624A", ky)
            f.text(str(int(round(dead * ky))), CX - 6, yb, face="title", size=130, color=col, align="r", track=6, alpha=sw_, shadow=(3, 4, 5, "#000000"))
            X.chip(f, "ÖLDÜ", CX + 92 + w84 + 46, yb - 34, k=sw_, size=30, edge="#B02A2A", color="#F8E2D8", align="l")
    f.vig(0.62)


# ───────────────────────────── c6_emir / c6_aylar ─────────────────────────────
@SH.kind("c6_emir")
@X.pushy(0.035)
def k_emir(cx, at_medal=0.0, at_paper=0.0, at_stamp=0.0, key="karl_olgun"):
    """Karl madalyası + BOŞ emir kâğıdı (mühürsüz) + EMİR YOK damgası."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.28)
    X.tone(f, "#8E1F26", 0.10, cy=0.5)
    sk.dust(f, cx.t, n=50)
    am = cx.amt(at_medal, 0.7)
    SH.draw_medal(f, key, 560, 500, 520 * (0.94 + 0.06 * ease_out(am)) * (1 + 0.03 * cx.u), "gold", False, alpha=am, tilt=0.16 * math.sin(cx.t * 0.55 + 1.0))
    SH.name_plate(f, "V. KARL", "İmparator", None, cx_=560, y=H * 0.80, t=cx.amt(at_medal, 0.6, off=0.3), w=420)
    ap = cx.amt(at_paper, 0.7)
    with Paper(f, 1290, 520, 640, 780, seed=17, rot=0.02 * (1 - 0.4 * cx.u), sc=(0.94 + 0.06 * ease_out(ap)) * (1 + 0.03 * cx.u), alpha=ap):
        f.text("EMİR", 0, -280, face="fell", size=58, color=INK, align="c", track=6, alpha=ap)
        f.line(-180, -258, 180, -258, color=INK, sw=1.6, alpha=0.6 * ap)
        for i in range(6):
            f.line(-230, -170 + i * 60, 230, -170 + i * 60, color=INK, sw=1.4, alpha=0.18 * ap)
        # mühür yeri: kesik çizgili boş daire
        p = f.paint("#7A5518", style="stroke", sw=3, alpha=0.7 * ap)
        p.setPathEffect(skia.DashPathEffect.Make([10, 9], 0))
        f.c.drawCircle(150, 270, 70, p)
    t = cx.amt(at_stamp, 0.3)
    if t > 0:
        SH.stamp(f, "EMİR YOK", 1290, 560, rot=-0.15, size=104, t=t)
    f.vig(0.62)


@SH.kind("c6_aylar")
@X.pushy(0.035)
def k_aylar(cx, at=0.0, at_start=0.0, at_end=0.0, at_word=0.0, at_stamp=None, key="klemens"):
    """Papa madalyası + MAYIS→ARALIK ay şeridi (1527) dolar; AYLARCA."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.28)
    X.tone(f, "#4B2D63", 0.14, cy=0.4)
    sk.dust(f, cx.t, n=50)
    am = cx.amt(at, 0.7)
    SH.draw_medal(f, key, 500, 340, 470 * (0.94 + 0.06 * ease_out(am)), "violet", False, alpha=am, tilt=0.16 * math.sin(cx.t * 0.5))
    X.ic(f, "chains" if X.has_icon("chains") else "keys", 860, 430, size=240, metal="violet", alpha=am, glow=0.2)
    months = ["MAYIS", "HAZİRAN", "TEMMUZ", "AĞUSTOS", "EYLÜL", "EKİM", "KASIM", "ARALIK"]
    n = len(months)
    cw, y = 190, 760
    x0 = CX - cw * n / 2
    ta, tb = cx.at(at_start), cx.at(at_end)
    prog = clamp((cx.t - ta) / max(0.3, tb - ta))
    SH.kicker(f, "1527", x0 - 10, y - 74, alpha=am, size=34, track=10, face="title_m", color="#C9B27A", align="l")
    for i, m in enumerate(months):
        xx = x0 + i * cw
        lit = clamp(prog * n - i)
        f.rrect(xx + 6, y, cw - 12, 96, 10, color="#150D08", alpha=0.85 * am)
        if lit > 0:
            f.rrect(xx + 6, y, (cw - 12) * lit, 96, 10, shader=f.lin(0, y, 0, y + 96, [("#C0392B", 0.0), ("#7A1F1A", 1.0)]), alpha=0.9)
        f.rrect(xx + 6, y, cw - 12, 96, 10, style="stroke", sw=2.2, color="#C9962B", alpha=0.9 * am)
        f.text(m, xx + cw / 2, y + 60, face="cap_b", size=30, color="#F4E6BC" if lit > 0.5 else "#8A7A55", align="c", track=3, alpha=am)
    kw = cx.amt(at_word, 0.7)
    if kw > 0:
        SH.gold_flat(f, "AYLARCA", 1360, 400, face="title", size=130, track=10, alpha=kw)
    if at_stamp is not None:
        t = cx.amt(at_stamp, 0.3)
        if t > 0:
            SH.stamp(f, "YAKLAŞIK", 1620, 640, rot=-0.08, size=36, t=t, color="#8A6A30")
    f.vig(0.6)


# ───────────────────────────── c6_zincir ─────────────────────────────
@SH.kind("c6_zincir")
@X.pushy(0.035)
def k_zincir(cx, at_n1=0.0, at_n2=0.0, at_n3=0.0, at_n4=0.0, at_x=0.0, at_break=0.0, at_teyze=0.0, at_stamp=0.0, at_hdr=None):
    """Neden-sonuç zinciri: ROMA 1527 → PAPA → CATHERINE (teyze) → HENRY (kırık anahtar). Damga: SIKÇA ANLATILIR."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.28)
    X.tone(f, "#8E1F26", 0.10, cy=0.5)
    sk.dust(f, cx.t, n=50)
    xs = [230, 690, 1150, 1610]
    y = 480
    sz = 330
    # kenarlar
    X.arrow(f, (xs[0] + 105, y), (xs[1] - sz * 0.5 - 10, y), ease_io(clamp((cx.t - max(0.05, cx.at(at_n2, off=-0.5))) / 0.7)), color="#E3B54A", width=7)
    X.arrow(f, (xs[1] + sz * 0.5 + 10, y), (xs[2] - sz * 0.5 - 10, y), ease_io(clamp((cx.t - max(0.05, cx.at(at_n3, off=-0.5))) / 0.7)), color="#E3B54A", width=7)
    X.arrow(f, (xs[2] + sz * 0.5 + 10, y), (xs[3] - sz * 0.5 - 10, y), ease_io(clamp((cx.t - max(0.05, cx.at(at_n4, off=-0.5))) / 0.7)), color="#E3B54A", width=7)
    # düğüm 1: Roma (kılıçlar)
    k1 = cx.amt(at_n1, 0.6)
    if k1 > 0:
        X.glow(f, xs[0], y, 190, "#C0391B", 0.30 * k1)
        X.ic(f, "swords", xs[0], y, size=210 * (0.9 + 0.1 * back_out(k1)), metal="crimson", alpha=k1, glow=0.3 * k1)
        f.text("ROMA", xs[0], y + 190, face="title_m", size=32, color="#F0DDA0", align="c", track=6, alpha=k1, shadow=(2, 2, 3, "#000000"))
        f.text("1527", xs[0], y + 232, face="cap_i", size=28, color="#B9A674", align="c", alpha=k1)
    # düğüm 2: papa
    for (xk, key, metal, at_, name, sub) in ((xs[1], "klemens", "violet", at_n2, "PAPA", "KLEMENS VII"),
                                              (xs[2], "catherine_aragon", "crimson", at_n3, "ARAGONLU CATHERINE", None),
                                              (xs[3], "henri8", "crimson", at_n4, "HENRY VIII", None)):
        k = cx.amt(at_, 0.7)
        if k <= 0:
            continue
        SH.draw_medal(f, key, xk, y, sz * (0.9 + 0.1 * ease_out(k)), metal, key == "henri8", alpha=k, tilt=0.14 * math.sin(cx.t * 0.55 + xk))
        f.text(name, xk, y + sz * 0.5 + 44, face="title_m", size=SH.fit_size(name, "title_m", 30, 400, 5), color="#F0DDA0", align="c", track=5, alpha=k, shadow=(2, 2, 3, "#000000"))
        if sub:
            f.text(sub, xk, y + sz * 0.5 + 84, face="cap_i", size=26, color="#B9A674", align="c", alpha=k)
    # Catherine: TEYZE etiketi
    kt = cx.amt(at_teyze, 0.5)
    if kt > 0:
        X.chip(f, "İMPARATORUN TEYZESİ", xs[2], y + sz * 0.5 + 138, k=kt, size=26, edge="#C9962B", color="#F4E6BC")
    # onaylanamadı (papa → Catherine oku üstünde)
    kx = cx.amt(at_x, 0.35)
    if kx > 0:
        xm = (xs[1] + xs[2]) / 2
        f.circle(xm, y, 40 * back_out(kx), color="#150D08", alpha=0.9)
        f.circle(xm, y, 40 * back_out(kx), style="stroke", sw=4, color="#B02A2A")
        X.strike_line(f, xm - 18, y - 18, xm + 18, y + 18, kx, sw=8)
        X.strike_line(f, xm + 18, y - 18, xm - 18, y + 18, kx, sw=8)
        X.chip(f, "BOŞANMA ONAYLANAMADI", xm, y - sz * 0.5 - 56, k=kx, size=26, edge="#B02A2A", color="#F8E2D8")
    # kırık anahtar (Henry: Roma'dan koptu)
    kb = ease_out(clamp((cx.t - cx.at(at_break)) / 0.6))
    ka = cx.amt(at_n4, 0.6, off=0.2)
    if ka > 0:
        yk = y - sz * 0.5 - 66
        xk0 = xs[3]
        if kb <= 0:
            X.ic(f, "keys", xk0, yk, size=130, metal="violet", alpha=ka)
        else:
            for sgn in (-1, 1):
                f.c.save()
                f.c.translate(xk0 + sgn * 56 * kb, yk + 10 * kb)
                f.c.rotate(sgn * 18 * kb)
                f.c.clipRect(skia.Rect.MakeXYWH(-80 if sgn < 0 else 0, -80, 80, 160))
                X.ic(f, "keys", 0, 0, size=130, metal="violet", alpha=ka)
                f.c.restore()
            f.text("ROMA'DAN KOPTU", xk0, yk - 84, face="title_m", size=26, color="#E7B8AA", align="c", track=5, alpha=kb)
    # damga
    t = cx.amt(at_stamp, 0.3)
    if t > 0:
        SH.stamp(f, "SIKÇA ANLATILIR", CX, 180, rot=-0.04, size=54, t=t, color="#B02A2A")
    f.vig(0.6)


# ───────────────────────────── c6_duello ─────────────────────────────
def _bubble(f, x, y, text, k, tail_dx=0, flipx=1, size=54):
    """Bağıran konuşma balonu (diş dişli kenar), kuyruk aşağıda."""
    if k <= 0:
        return
    sc = 0.7 + 0.3 * back_out(k)
    wt = sk.text_width(text, "title", size, 4)
    w, h = wt + 90, size * 1.9
    f.c.save()
    f.c.translate(x, y)
    f.c.scale(sc, sc)
    pts = []
    n = 26
    for i in range(n):
        a = 2 * math.pi * i / n
        r = 1.0 if i % 2 == 0 else 0.86
        pts.append(((w / 2) * r * math.cos(a) * 1.12, (h / 2) * r * math.sin(a) * 1.25))
    P = sk.poly_path(pts, True)
    f.path(P, color="#000000", alpha=0.4 * k, blur=6)
    f.path(P, color="#F6EBC8", alpha=0.97 * k)
    f.path(P, style="stroke", sw=4, color="#7A1F1A", alpha=k)
    tail = sk.poly_path([(-26 + tail_dx * 0.1, h * 0.5), (30 + tail_dx * 0.1, h * 0.5), (tail_dx, h * 0.5 + 80)], True)
    f.path(tail, color="#F6EBC8", alpha=0.97 * k)
    f.path(tail, style="stroke", sw=4, color="#7A1F1A", alpha=k)
    f.rect(-24 + tail_dx * 0.1, h * 0.5 - 6, 52, 10, color="#F6EBC8", alpha=0.97 * k)
    f.text(text, 0, size * 0.36, face="title", size=size, color="#7A1F1A", align="c", track=4, alpha=k)
    f.c.restore()


@SH.kind("c6_duello")
@X.pushy(0.035)
def k_duello(cx, at_year=0.0, at_b1=0.0, at_b2=0.0, at_swords=0.0, at_gone=0.0, at_stamp=0.0, left="karl_olgun", right="fransuva", at_names=None):
    """İki hükümdar yüz yüze: 'YALANCI!' balonları, düello kılıçları, DÜELLO YAPILMADI."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.3)
    X.tone(f, "#8E1F26", 0.12, cy=0.55)
    sk.dust(f, cx.t, n=55)
    ay = cx.amt(at_year, 0.7)
    if ay > 0:
        SH.gold_flat(f, "1528", CX, 190, face="title", size=96, track=12, alpha=ay)
    a1 = cx.amt(0.0, 0.8)
    xl, xr, ym, ms = 470, 1450, 600, 470
    SH.draw_medal(f, left, xl, ym, ms * (0.94 + 0.06 * ease_out(a1)) * (1 + 0.03 * cx.u), "gold", False, alpha=a1, tilt=0.12 * math.sin(cx.t * 0.6))
    SH.draw_medal(f, right, xr, ym, ms * (0.94 + 0.06 * ease_out(a1)) * (1 + 0.03 * cx.u), "royal", True, alpha=a1, tilt=-0.12 * math.sin(cx.t * 0.6 + 1))
    # isim levhaları ("iki hükümdar"): düello damgası gelince sönükleşir
    if at_names is not None:
        kn = cx.amt(at_names, 0.6)
        if kn > 0:
            fade = 1 - cx.amt(at_stamp, 0.3, off=-0.1)
            if fade > 0.01:
                SH.name_plate(f, "V. KARL", "İmparator", None, cx_=xl, y=ym + ms * 0.52, alpha=fade, t=kn)
                SH.name_plate(f, "I. FRANÇOIS", "Fransa Kralı", None, cx_=xr, y=ym + ms * 0.52, alpha=fade, t=kn)
    # balonlar
    _bubble(f, xl + 120, ym - 340, "YALANCI!", cx.amt(at_b1, 0.28), tail_dx=-30)
    _bubble(f, xr - 120, ym - 340, "YALANCI!", cx.amt(at_b2, 0.28), tail_dx=30)
    # kılıçlar: iki yandan gelir, ortada çarpışır, sonra kırılıp söner
    ks = ease_out(clamp((cx.t - cx.at(at_swords)) / 0.55), 3)
    kg = cx.amt(at_gone, 0.7)
    if ks > 0:
        cl = 1 - kg
        for sgn in (-1, 1):
            xx = CX + sgn * lerp(420, 40, ks)
            X.ic(f, "sword", xx, ym + 40 + kg * 80, size=330, metal="silver", alpha=cl, rot=sgn * (0.7 - 0.12 * ks) + kg * sgn * 0.6, flip=(sgn < 0), glow=0.2 * cl)
        if 0.85 < ks and kg < 0.3:
            sp = (cx.t * 9) % 1
            f.circle(CX, ym + 10, 60 + 30 * sp, shader=f.rad(CX, ym + 10, 60 + 30 * sp, [("#FFF1C2", 0.0, int(180 * (1 - sp))), ("#FFB347", 0.5, int(80 * (1 - sp))), ("#FFB347", 1.0, 0)]), blend=skia.BlendMode.kPlus)
    t = cx.amt(at_stamp, 0.3)
    if t > 0:
        SH.stamp(f, "DÜELLO YAPILMADI", CX, H * 0.90, rot=-0.05, size=78, t=t)
    f.vig(0.62)


# ───────────────────────────── c6_hanimlar ─────────────────────────────
@SH.kind("c6_hanimlar")
@X.pushy(0.035)
def k_hanimlar(cx, at_two=0.0, at_l=0.0, at_r=0.0, at_title=0.0, at_olive=None):
    """İki kadın: François'nın annesi (Louise de Savoie) ve Şarlken'in halası (Margareta). Başlık: HANIMLAR BARIŞI."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.3)
    X.tone(f, "#2F7A8A", 0.10, cy=0.5)
    sk.dust(f, cx.t, n=55)
    kt = cx.amt(at_two, 0.7)
    if kt > 0:
        SH.kicker(f, "İKİ KADIN", CX, 140, alpha=kt * (1 - cx.amt(at_title, 0.6)), size=34, track=16, face="title_m", color="#E0C682")
    xl, xr, ym, ms = 520, 1400, 500, 470
    for (x, key, metal, at_, flip, name, role) in ((xl, "louise_savoy", "royal", at_l, False, "LOUISE DE SAVOIE", "François'nın annesi"),
                                                   (xr, "margareta", "gold", at_r, True, "MARGARETA", "Şarlken'in halası")):
        k = cx.amt(at_, 0.8)
        if k <= 0:
            # henüz isimsiz: siluet kadın
            ks = cx.amt(at_two, 0.8)
            if ks > 0:
                ST.figure(f, "woman", x, ym + 270, 580, col="#140B07", rim="#E3A55C", face=1 if x < CX else -1, alpha=ks * 0.95)
            continue
        X.glow(f, x, ym, 330, "#E3B54A", 0.18 * k)
        SH.draw_medal(f, key, x, ym, ms * (0.92 + 0.08 * ease_out(k)) * (1 + 0.03 * cx.u), metal, flip, alpha=k, tilt=0.12 * math.sin(cx.t * 0.6 + x))
        SH.name_plate(f, name, role, None, cx_=x, y=ym + ms * 0.52, t=cx.amt(at_, 0.6, off=0.3))
    # ortada zeytin dalı / defne
    ko = cx.amt(at_title, 0.9)
    X.ic(f, "laurel", CX, ym, size=330 * (0.8 + 0.2 * back_out(ko)), metal="gold", alpha=ko, glow=0.35 * ko)
    if ko > 0:
        X.chip(f, "HANIMLAR BARIŞI", CX, H * 0.86, k=ko, size=52, edge="#C9962B", color="#F4DD92", padx=44, h=100)
        SH.kicker(f, "CAMBRAI · 1529", CX, H * 0.86 + 96, alpha=ko, size=28, track=12, face="cap", color="#B9A674")
    f.vig(0.6)


# ───────────────────────────── c6_fidye ─────────────────────────────
@SH.kind("c6_fidye")
@X.pushy(0.035)
def k_fidye(cx, at=0.0, dur=1.7, at_boys=0.0):
    """İki oğul (siluet) ve 2.000.000 ALTIN ECÜ: yağan paralar; oğullar geri."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.3)
    X.tone(f, "#27427A", 0.12, cy=0.5)
    sk.dust(f, cx.t, n=50)
    a = cx.amt(at, 0.5)
    k = ease_out(clamp((cx.t - cx.at(at)) / dur), 3)
    # oğullar: önce ortada belirir, para gelince sola kayar
    kb = cx.amt(at_boys, 0.9)
    sl = ease_io(clamp((cx.t - cx.at(at)) / 0.9))
    if kb > 0:
        bx = lerp(CX - 130, 300, sl)
        bh = lerp(700, 520, sl)
        ST.figure(f, "page", bx - 120, H + 60, bh * 0.98, col="#0A0605", rim="#8EA8C8", face=1, alpha=kb)
        ST.figure(f, "child", bx + 120, H + 60, bh * 0.86, col="#0A0605", rim="#8EA8C8", face=-1, alpha=kb)
        X.chip(f, "İKİ OĞUL", bx, H - bh - 10 if sl > 0.5 else 190, k=kb, size=30, edge="#6C92E0", color="#E0ECFF")
    if a > 0:
        rs = np.random.RandomState(9)
        for i in range(46):
            px = rs.rand() * SW
            ph = (cx.t * (0.22 + 0.2 * rs.rand()) + rs.rand()) % 1.0
            py = -60 + ph * (H + 120)
            r = 14 + rs.rand() * 16
            al = a * (0.35 + 0.35 * rs.rand())
            sq = abs(math.cos(cx.t * 3 + i))
            f.oval(px, py, r, r * (0.25 + 0.75 * sq), shader=f.lin(px - r, py, px + r, py, [("#7A5518", 0.0), ("#F4DC8C", 0.5), ("#C9962B", 1.0)]), alpha=al)
        s_ = SH.fmt_int(int(round(2000000 * k)))
        xc = lerp(CX, 1130, 1.0)
        SH.gold_flat(f, s_, xc, 520, face="title", size=190, track=6, alpha=a)
        f.text("ALTIN ECÜ", xc, 610, face="title_m", size=52, color="#E0C682", align="c", track=16, alpha=cx.amt(at, 0.5, off=0.3))
        X.ic(f, "coinbag", xc, 270, size=260 * (0.9 + 0.1 * back_out(a)), metal="gold", alpha=a, glow=0.3 * a)
    f.vig(0.6)


# ───────────────────────────── c6_savas (kronoloji) ─────────────────────────────
@SH.kind("c6_savas")
@X.pushy(0.035)
def k_savas(cx, at_axis=0.0, at_peace=0.0, at_war=0.0, at_gap=0.0, at_end=0.0, at_death=None, a0=1520, a1=1560):
    """1521–1558 savaş dilimleri (kesintili kırmızı çubuklar). Barış (Cambrai) belirir ve çatlar; son: 1558."""
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.25)
    X.tone(f, "#8E1F26", 0.10, cy=0.5)
    sk.dust(f, cx.t, n=40)
    w = 1560
    x0 = CX - w / 2
    y = 600

    def XX(yr):
        return x0 + (yr - a0) / (a1 - a0) * w

    ka = ease_out(clamp((cx.t - cx.at(at_axis)) / 0.9))
    f.line(x0, y, x0 + w * ka, y, color="#C9962B", sw=4, alpha=0.9)
    for yr in range(a0, a1 + 1, 5):
        xx = XX(yr)
        if xx <= x0 + w * ka + 1:
            L = 20 if yr % 10 == 0 else 11
            f.line(xx, y - L, xx, y + L, color="#C9962B", sw=2, alpha=0.8)
            if yr % 10 == 0:
                f.text(str(yr), xx, y + 64, face="title_m", size=28, color="#CDBB86", align="c", track=3, alpha=0.9)
    # savaş dilimleri (yaklaşık)
    segs = [(1521, 1526), (1526, 1529), (1536, 1538), (1542, 1544), (1551, 1558)]
    tw = cx.at(at_war)
    for i, (s0, s1) in enumerate(segs):
        k = ease_out(clamp((cx.t - (tw + i * 0.55)) / 0.7), 2)
        if k <= 0:
            continue
        xa, xb = XX(s0), XX(s1)
        f.rrect(xa, y - 62, (xb - xa) * k, 50, 10, shader=f.lin(0, y - 62, 0, y - 12, [("#E26A5A", 0.0), ("#B0332B", 0.55), ("#6E1A16", 1.0)]), alpha=0.95)
        f.rrect(xa, y - 62, (xb - xa) * k, 50, 10, style="stroke", sw=2.0, color="#F4B4A8", alpha=0.7)
    f.text("SAVAŞ", XX(1523.5), y - 84, face="title_m", size=32, color="#E7B8AA", align="c", track=6, alpha=ease_out(clamp((cx.t - tw) / 0.6)))
    # olay işaretleri (belgelerdeki tarihler)
    marks = [(1525, "PAVIA", 0), (1526, "MADRİD", 1), (1529, "CAMBRAI", 0), (1544, "CRÉPY", 0)]
    for yr, name, lvl in marks:
        tm = tw + (yr - 1521) * 0.07 + 0.2
        k = cx.amt(tm, 0.5)
        if k > 0:
            xx = XX(yr)
            yy0 = y + 100 + lvl * 56
            f.line(xx, y + 8, xx, yy0 - 22, color="#B9A674", sw=1.5, alpha=0.7 * k)
            f.circle(xx, y, 7, color="#F0D27A", alpha=k)
            f.text(name, xx, yy0 + 8, face="cap_b", size=30, color="#EBDDB5", align="c", track=2, alpha=k, shadow=(1, 2, 2, "#000000"))
    # barış (Cambrai) defnesi: belirir, sonra çatlar/söner
    kp = cx.amt(at_peace, 0.7)
    kg = cx.amt(at_gap, 0.6)
    if kp > 0:
        X.ic(f, "laurel", XX(1531), y - 190, size=170 * (0.9 + 0.1 * back_out(kp)), metal="forest", alpha=kp * (1 - 0.8 * kg), glow=0.2 * kp)
        SH.kicker(f, "BARIŞ", XX(1531), y - 80, alpha=kp * (1 - 0.8 * kg), size=26, track=8, face="title_m", color="#9CCB94")
    # 'kesintilerle': boşluklar kesikli çizgi
    kk = cx.amt(at_gap, 0.7)
    if kk > 0:
        for (g0, g1) in ((1529, 1536), (1538, 1542), (1544, 1551)):
            p = f.paint("#9CCB94", style="stroke", sw=3, alpha=0.8 * kk)
            p.setPathEffect(skia.DashPathEffect.Make([8, 9], 0))
            f.c.drawLine(XX(g0), y - 28, XX(g1), y - 28, p)
    # son: 1558
    ke = ease_out(clamp((cx.t - cx.at(at_end)) / 0.9), 3)
    if ke > 0:
        xx = XX(1558)
        f.line(xx, y - 250 * ke, xx, y + 24, color="#F0D27A", sw=4, alpha=0.95)
        f.text("1558", xx, y - 270 * ke, face="title", size=56, color="#F4DD92", align="c", track=4, alpha=ke, shadow=(2, 3, 4, "#000000"))
        f.text("ÖMRÜNÜN SONU", xx, y - 270 * ke - 62, face="cap_i", size=32, color="#D9C795", align="c", alpha=ke, shadow=(2, 2, 3, "#000000"))
    tk = cx.amt(at_war, 0.3)
    if tk > 0:
        SH.stamp(f, "YAKLAŞIK", 400, 300, rot=-0.06, size=40, t=tk, color="#9A7A38")
    f.vig(0.58)


def _puffs(f, x, y, t, w=240, h=520, n=14, seed=1, color="#24100D", alpha=0.5):
    """Yükselen duman: radyal degrade pufları (blur katmanı yok → hızlı)."""
    rs = np.random.RandomState(seed)
    for i in range(n):
        ph = (t * 0.10 + rs.rand()) % 1.0
        px = x + (rs.rand() - 0.5) * w * 0.35 + math.sin(ph * 5 + i) * w * 0.22 * ph
        py = y - ph * h
        r = 44 + ph * 120 + rs.rand() * 22
        a = alpha * math.sin(math.pi * ph) ** 1.1
        f.circle(px, py, r, shader=f.rad(px, py, r, [(color, 0.0, int(255 * a)), (color, 0.55, int(185 * a)), (color, 1.0, 0)]))


# ───────────────────────────── c6_santangelo (diorama) ─────────────────────────────
@SL.sc("c6_santangelo")
class SantAngelo:
    """Roma 1527, gece: yanan şehir silueti, Tiber, taş köprü ve Castel Sant'Angelo (sığınak). p: fire=0..1, bx (kale x)."""

    def __init__(self, p):
        self.p = p

    def layers(self):
        fire = float(self.p.get("fire", 1.0))
        bx = float(self.p.get("bx", 1180))
        M = MARGIN

        def L0(f):          # gökyüzü + ufuk yangını + uzak şehir
            ST.sky_gradient(f, "#10070C", "#6E2410", y1=770)
            for (x, r, a) in ((330, 980, 190), (980, 800, 130), (1560, 900, 170)):
                f.circle(x, 750, r, shader=f.rad(x, 750, r, [("#FF8A33", 0.0, int(a * fire)), ("#C0391B", 0.5, int(80 * fire)), ("#C0391B", 1.0, 0)]), blend=skia.BlendMode.kPlus)
            ST.skyline(f, 770, ["tower", "spire", "dome", "house", "dome", "tower", "spire"], -260, SW + 260, 200, "#1C0C0A", seed=5, win="#FFB347")
            f.rect(-M, 765, SW + 2 * M, 60, color="#1C0C0A")

        def L1(f):          # yakın şehir + nehir + yansımalar
            ST.skyline(f, 812, ["house", "tower", "house", "spire", "house", "house"], -260, SW + 260, 150, "#0E0605", seed=9, win="#FFB347", gap=(24, 80))
            f.rect(-M, 808, SW + 2 * M, H + M - 808, shader=f.lin(0, 808, 0, H, [("#80300F", 0.0), ("#2C1210", 0.35), ("#0A0606", 1.0)]))
            rs = np.random.RandomState(3)
            for i in range(110):
                x = rs.rand() * (SW + 2 * M) - M
                y = 818 + rs.rand() ** 1.6 * 300
                w = 20 + rs.rand() * 130
                f.line(x, y, x + w, y, color="#FF9A4A" if rs.rand() > 0.4 else "#C0391B", sw=1.5 + rs.rand() * 2.2, alpha=0.30 * (1 - (y - 818) / 320))

        def L2(f):          # köprü + Castel Sant'Angelo
            yb = 812
            # taş köprü: güverte + kemer delikleri (even-odd)
            P = skia.Path()
            P.setFillType(skia.PathFillType.kEvenOdd)
            P.addRect(skia.Rect.MakeLTRB(-M, yb - 28, bx - 262, yb + 110))
            for i in range(5):
                cxp = -100 + i * 190
                yy = yb + 110
                P.moveTo(cxp - 72, yy)
                P.cubicTo(cxp - 72, yy - 62, cxp - 36, yy - 76, cxp, yy - 76)
                P.cubicTo(cxp + 36, yy - 76, cxp + 72, yy - 62, cxp + 72, yy)
                P.close()
            f.path(P, color="#0A0504")
            f.line(-M, yb - 28, bx - 262, yb - 28, color="#7A4A22", sw=2, alpha=0.5)
            # kıyı duvarı (köprü güvertesiyle aynı hatta oturur → köprü kaleye bağlanır)
            f.rect(bx - 340, yb + 30, 680, 80, shader=f.lin(0, yb + 30, 0, yb + 110, [("#1A0D08", 0.0), ("#0A0504", 1.0)]))
            for k in range(6):
                f.line(bx - 300 + k * 120, yb + 40, bx - 300 + k * 120, yb + 108, color="#000000", sw=2, alpha=0.5)
            # kale gövdesi: kare taban
            base = sk.poly_path([(bx - 310, yb + 30), (bx + 310, yb + 30), (bx + 262, yb - 96), (bx - 262, yb - 96)], True)
            f.path(base, shader=f.lin(bx - 310, 0, bx + 310, 0, [("#3A1D10", 0.0), ("#150A07", 0.6), ("#0A0504", 1.0)]))
            for sx in (-1, 1):                          # köşe burçları
                f.rect(bx + sx * 252 - 36, yb - 170, 72, 90, color="#120806")
                for k in range(3):
                    f.rect(bx + sx * 252 - 36 + k * 26, yb - 188, 20, 20, color="#120806")
            # silindirik gövde
            f.rect(bx - 178, yb - 360, 356, 264, shader=f.lin(bx - 178, 0, bx + 178, 0, [("#5A2C16", 0.0), ("#2A140B", 0.35), ("#0F0706", 0.8), ("#080403", 1.0)]))
            f.oval(bx, yb - 360, 178, 26, color="#2A140B")
            for k in range(12):
                f.rect(bx - 176 + k * 32, yb - 386, 17, 22, color="#1A0D08")
            # üst silindir + kubbe + melek
            f.rect(bx - 92, yb - 450, 184, 92, shader=f.lin(bx - 92, 0, bx + 92, 0, [("#4A2412", 0.0), ("#1A0D08", 0.5), ("#080403", 1.0)]))
            f.oval(bx, yb - 450, 92, 18, color="#2A140B")
            f.path(sk.poly_path([(bx - 70, yb - 452), (bx - 40, yb - 520), (bx + 40, yb - 520), (bx + 70, yb - 452)], True), color="#120806")
            f.rect(bx - 10, yb - 575, 20, 56, color="#120806")
            # melek (basit siluet): gövde + iki kanat + kılıç
            ax, ay = bx, yb - 600
            f.path(sk.poly_path([(ax - 7, ay + 26), (ax - 5, ay - 20), (ax + 5, ay - 20), (ax + 7, ay + 26)], True), color="#0B0605")
            f.circle(ax, ay - 28, 7, color="#0B0605")
            for sx in (-1, 1):
                f.path(sk.smooth_path([(ax, ay - 12), (ax + sx * 40, ay - 52), (ax + sx * 62, ay - 30), (ax + sx * 20, ay + 2)], True, 0.4), color="#0B0605")
            f.line(ax + 10, ay - 8, ax + 36, ay - 70, color="#0B0605", sw=3)
            # pencere yarıkları (sıcak)
            rs = np.random.RandomState(8)
            for k in range(11):
                wx = bx - 150 + k * 30 + rs.rand() * 6
                wy = yb - 300 + (k % 3) * 52 + rs.rand() * 10
                f.rect(wx, wy, 6, 22, color="#FFB347", alpha=0.85)
        def L3(f):          # ön plan: parapet + asker siluetleri
            f.rect(-M, H - 90, SW + 2 * M, 200, color="#060303")
            for k in range(14):
                f.rect(-M + k * 190, H - 130, 110, 60, color="#060303")
            for (x, kd, h, face) in ((150, "landsknecht", 400, 1), (420, "pikeman", 360, 1), (1640, "landsknecht", 390, -1), (1860, "pikeman", 350, -1)):
                ST.figure(f, kd, x, H + 70, h, col="#050302", rim="#C07838", face=face)

        return [(0.06, L0), (0.35, L1), (0.7, L2), (1.2, L3)]

    def dyn(self):
        def D1(f, t):
            for i, (x, y, s, dr) in enumerate(((330, 752, 1.4, 70), (960, 744, 1.3, -50), (1600, 756, 1.4, 60))):
                PW.smoke_column(f, x, y - 16, t, n=11, h=540, w0=28, w1=125, col="#1B0D0A", a=0.50, rate=0.10, drift=dr, seed=3 + i, wobble=24)
                for k in range(5):
                    PW.flame(f, x + (k - 2) * 40, y + (k % 2) * 7, s * (0.78 + 0.12 * (k % 3)), t, seed=i * 7 + k, glow_a=0.55)
            sk.embers(f, t, n=46, seed=6, rect=(-100, 220, SW + 200, 600))
        return {1: D1}
