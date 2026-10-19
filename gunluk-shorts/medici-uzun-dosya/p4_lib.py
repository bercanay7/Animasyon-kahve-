"""p4_lib — PARÇA 4 (c8 Aslanın İni · c9 Defter Kapanıyor) ortak çizim/yardımcı işlevleri. Yalnız Parça 4 sahne dosyaları (`scenes_c8.py`, `scenes_c9.py`,
`c8_kinds.py`, `c9_kinds.py`) kullanır; motor/dünya dosyalarına dokunmaz, onların işlevlerini ÇAĞIRIR (cilt_medici, cilt_oda, cilt_pano, cilt_sehir, cilt_deniz, mapsk).

İçerik
  1) `p4_<tür>` sarmalayıcıları: stok türü AYNEN çağırır, ardından `ovl(cx)` ile üstüne çizer (kamera/duvar/ışık iç türde; ovl ekran uzayında).
     Kendi kamerası olan türler (oda/pano/sehir/build/deniz*/liman) `cilt_cam.OWN_CAMERA`'ya eklenir → `cams=/path=` iç türe verilir.
  2) ovl kurucuları (çapaya bağlı etiket, levha, damga, tarih plakası, oyma yazı, karartma …) — her biri `fn(cx)` döndürür; `ovl=ov(...)`.
  3) harita yardımcıları (`map` türünün `extra=` kancası: iğne, ordu oku, şube ışığı, kâğıt/mektup yolculuğu …).
  4) küçük nesneler (kurşun mühür/bulla, sikke yığını, kâğıt tomarı …).
Olgu disiplini: bu modül kendi başına metin üretmez; metinler sahne dosyasından gelir.
"""
import math

import numpy as np
import skia

import cilt_cam
import cilt_medici as CM
import cilt_oda as OD
import cilt_pano as PN
import icons
import shots as SH
import sk
from cilt_medici import PIG, TH
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth

INK = "#2A1A0C"
INK_S = "#3A2616"
_RS = PN._RS
R, RA, INKP, INKR, LINE, POLY, OVAL, GRAD_V = PN.R, PN.RA, PN.INKP, PN.INKR, PN.LINE, PN.POLY, PN.OVAL, PN.GRAD_V
PT, STK, SOFT, FILLP, RRECT = OD.PT, OD.STK, OD.SOFT, OD.FILLP, OD.RRECT
LIN = CM._LIN


def P(col, a=255, **kw):
    return skia.Paint(AntiAlias=True, Color=C(col, int(a)), **kw)


def S(col, w=1.5, a=255, cap=True):
    return STK(col, w, int(a), cap)


# ───────────────────────────── 1) sarmalayıcı türler ─────────────────────────────
_OWN = {"oda", "pano", "sehir", "build", "deniz", "deniz_rota", "deniz_filo", "deniz_kiyi", "liman"}
_BASES = ("oda", "pano", "sehir", "build", "map", "procession", "frieze", "skyline", "ledger", "letter", "doc", "quote", "counter", "stacked", "bars", "network", "tree",
          "timeline", "medal", "medals", "palle", "emblem", "coin", "iconrow", "deniz", "deniz_rota", "deniz_filo", "deniz_kiyi", "liman")


def _wrap(base):
    name = "p4_" + base

    def fn(cx, ovl=None, **kw):
        SH.KINDS[base](cx, **kw)
        if ovl is not None:
            ovl(cx)
    fn.__name__ = "k_" + name
    SH.KINDS[name] = fn
    if base in _OWN or base in cilt_cam.OWN_CAMERA:
        cilt_cam.OWN_CAMERA.add(name)


for _b in _BASES:
    if _b in SH.KINDS:
        _wrap(_b)


# ───────────────────────────── 2) ovl kurucuları ─────────────────────────────
def ov(*items):
    items = [i for i in items if i]

    def fn(cx):
        for it in items:
            it(cx)
    return fn


def _kk(cx, at, dur, out=None, out_dur=0.5, off=0.0):
    k = cx.amt(at, dur, off=off)
    if out is not None:
        k *= 1.0 - cx.amt(out, out_dur)
    return k


def label(text, x, y, at, size=44, face="title_m", color=None, align="c", track=8.0, dur=0.7, out=None, out_dur=0.5, rise=14, emboss=False, alpha=1.0, off=0.0):
    """Zamanı çapaya bağlı yazı: `at`'ta yukarı doğru belirir, isteğe bağlı `out` çapasında solar."""
    def fn(cx):
        k = _kk(cx, at, dur, out, out_dur, off)
        if k <= 0.003:
            return
        CM.ink(cx.f, text, x, y + (1 - k) * rise, face=face, size=size, color=color or TH.fg, align=align, track=track, alpha=k * alpha, emboss=emboss)
    return fn


def kick(text, at, out=None, y=128, size=32, track=12, dur=0.7):
    def fn(cx):
        k = _kk(cx, at, dur, out)
        if k > 0.003:
            CM.kick(cx.f, text, W / 2, y, alpha=k, size=size, track=track)
    return fn


def tag(text, x, y, at, size=34, face="title_m", track=6.0, sub=None, w=None, dur=0.55, align="c", off=0.0, out=None, color=None, corner=8):
    """Çapaya bağlı isim/etiket levhası (tablet + yazı). (x,y) levha merkezi."""
    def fn(cx):
        k = _kk(cx, at, dur, out, 0.4, off)
        if k <= 0.003:
            return
        f = cx.f
        wd = (w if w is not None else sk.text_width(text, face, size, track) + 76)
        hh = size + 44 + (size * 0.78 if sub else 0)
        xx = x - wd / 2 if align == "c" else x
        yy = y - hh / 2 + (1 - k) * 10
        CM.tablet(f, xx, yy, wd, hh, alpha=k, corner=corner)
        CM.ink(f, text, xx + wd / 2, yy + 8 + size * 1.02, face=face, size=size, color=color or TH.fg, align="c", track=track, alpha=k, emboss=False)
        if sub:
            CM.ink(f, sub, xx + wd / 2, yy + 8 + size * 1.02 + size * 0.86, face="cap_i", size=size * 0.74, color=TH.fg2, align="c", alpha=k, emboss=False)
    return fn


def stamp(text, x, y, at, rot=-0.10, size=52, color=None, out=None, dur=0.3, off=0.0):
    """Damga çarpması (0,3 sn)."""
    def fn(cx):
        t = cx.amt(at, dur, off=off)
        if t <= 0:
            return
        al = 1.0 - (cx.amt(out, 0.5) if out is not None else 0.0)
        if al <= 0.01:
            return
        CM.stamp(cx.f, text, x, y, rot=rot, size=size, color=color, alpha=al, t=t)
    return fn


def date_plate(text, at, x=96, y=860, size=50, out=None):
    """Sol altta tarih levhası (altyazı bölgesi y≈938–1042 dışında; y=860 → levha 796–886)."""
    def fn(cx):
        k = _kk(cx, at, 0.55, out, 0.5)
        if k <= 0.003:
            return
        wd = sk.text_width(text, "title", size, 6) + 76
        CM.tablet(cx.f, x, y - 64 * k, wd, 90, alpha=k, corner=10)
        CM.ink(cx.f, text, x + wd / 2, y - 6 * k, face="title", size=size * 0.80, color=TH.fg, align="c", track=6, alpha=k, emboss=False)
    return fn


def engr(text, x, y, at, size=70, track=10.0, color=None, style="engraved", dur=1.0, face="title", off=0.0, alpha=1.0, glow=0.0, out=None, scale=1.0):
    """Çapaya bağlı oyma/yaldız yazı (soldan açılır)."""
    def fn(cx):
        k = cx.amt(at, dur, off=off)
        if k <= 0.003:
            return
        al = alpha * (1.0 - (cx.amt(out, 0.5) if out is not None else 0.0))
        if al <= 0.01:
            return
        sp = CM.gilt(text, face, int(size), float(track)) if style == "gilt" else CM.engraved(text, face, int(size), float(track), color or TH.fg)
        CM.draw_spr(cx.f, sp, x, y, "c", alpha=al * min(1.0, k * 2.0), reveal=clamp(k * 1.12), glow=glow * k, scale=scale)
    return fn


def count_up(x, y, at, value, dur=1.4, unit=None, size=150, face="title", color=None, prefix="", suffix="", unit_size=44, shadow=True, fmt=None, out=None):
    """Sayı sayar (0→value, ease_out)."""
    def fn(cx):
        k0 = cx.amt(at, 0.35)
        if out is not None:
            k0 *= 1.0 - cx.amt(out, 0.4)
        if k0 <= 0.003:
            return
        k = ease_out(clamp((cx.t - cx.at(at)) / dur), 3)
        v = value * k
        s = (fmt(v) if fmt else CM.fmt_int(v))
        txt = prefix + s + suffix
        sz = CM.fit_size(txt, face, size, 1500, 6)
        sp = CM.gilt(txt, face, int(sz), 6.0) if not TH.day else CM.engraved(txt, face, int(sz), 6.0, color or TH.fg)
        CM.draw_spr(cx.f, sp, x, y, "c", alpha=k0, shadow=0.5 if shadow and not TH.day else 0.0)
        if unit:
            CM.ink(cx.f, unit, x, y + unit_size * 1.25 + 8, face="title_m", size=unit_size, color=TH.acc, align="c", track=14, alpha=k0 * cx.amt(at, 0.8, off=0.3), emboss=False)
    return fn


def scrim(a_from, a_to, col="#000000", alpha=0.35, dur=0.8):
    def fn(cx):
        k = cx.amt(a_from, dur) * (1.0 - cx.amt(a_to, dur))
        if k > 0.003:
            cx.f.rect(0, 0, W, H, color=col, alpha=alpha * k)
    return fn


def dim(a_from, a_to=None, alpha=0.5, dur=0.8, col="#06060C"):
    """a_from'dan itibaren ekranı karartır; a_to verilirse sonra açılır."""
    def fn(cx):
        k = cx.amt(a_from, dur) * ((1.0 - cx.amt(a_to, dur)) if a_to is not None else 1.0)
        if k > 0.003:
            cx.f.rect(0, 0, W, H, color=col, alpha=alpha * k)
    return fn


def glint(x, y, at, r=90, col="#FFF1B8", dur=0.9, alpha=0.9):
    """Işıltı: haç parıltısı + halka."""
    def fn(cx):
        p = clamp((cx.t - cx.at(at)) / dur)
        if p <= 0 or p >= 1:
            return
        a = math.sin(p * math.pi)
        Rr = r * (0.4 + 0.8 * p)
        cx.f.circle(x, y, Rr, shader=cx.f.rad(x, y, Rr, [(col, 0.0, int(190 * a * alpha)), (col, 1.0, 0)]))
        c = cx.f.c
        for ang in (0, 90):
            dx, dy = math.cos(math.radians(ang)) * Rr * 1.25 * a, math.sin(math.radians(ang)) * Rr * 1.25 * a
            c.drawLine(x - dx, y - dy, x + dx, y + dy, cx.f.paint(col, style="stroke", sw=2.4, alpha=0.9 * a * alpha))
    return fn


def ink_wash(at, dur=1.4, col="#A8201A", alpha=0.42, from_right=True, seed=4, out=None):
    """Pigment yıkama (kan DEĞİL: kızıl boya): ekrana organik kenarla yayılır; out çapasında çekilir."""
    def fn(cx):
        k = ease_out(clamp((cx.t - cx.at(at)) / dur), 2.0)
        if out is not None:
            k *= 1.0 - ease_io(clamp((cx.t - cx.at(out)) / 1.0))
        if k <= 0.003:
            return
        c = cx.f.c
        xe = W * (1.15 - 1.25 * k) if from_right else W * (-0.15 + 1.25 * k)
        pts = []
        n = 22
        for i in range(n + 1):
            y = H * i / n
            wob = 70 * math.sin(i * 0.9 + seed) + 40 * math.sin(i * 2.1 + cx.t * 0.6 + seed * 2)
            pts.append((xe + wob, y))
        edge = W + 40 if from_right else -40
        pts += [(edge, H), (edge, 0)]
        path = sk.poly_path(pts)
        c.drawPath(path, cx.f.paint(col, alpha=alpha * min(1.0, k * 2.2), blend=skia.BlendMode.kMultiply))
    return fn


# ───────────────────────────── 3) özel tür iskeleti ─────────────────────────────
def begin(cx, bg="wall", seed=0, dress=None, push=0.0, drift=(0.0, 0.0), clear="#0B0A08"):
    """Özel tür iskeleti: arka plan (duvar/siyah) + kamera dönüşü. Dönüş: (f, c, cam)."""
    f = cx.f
    cam = CM.Cam(cx, push=push, drift=drift)
    if bg == "wall":
        CM.bgfill(f, cx, seed=seed, cam=cam, dress=dress)
    else:
        f.clear(clear)
    cam.begin(f)
    return f, f.c, cam


def end(cx, cam, motes_n=26, light=None, vig_s=None, dust=True):
    cam.end(cx.f)
    CM.finish(cx.f, cx, motes_n=motes_n, light=light, vig_s=vig_s, dust=dust)


def look(wx, wy, z=1.0, rot=0.0):
    """Anahtar kare: dünya (wx,wy) noktası ekran merkezinde, zoom z (cam=[(çapa, look(...)), …])."""
    return (z * (wx - W / 2), z * (wy - H / 2), z, rot)


def breath(cx, a=0.008, hz=0.45, ph=0.0):
    return 1.0 + a * math.sin(cx.t * hz * 6.283 + ph)


# ───────────────────────────── 4) küçük nesneler ─────────────────────────────
sk.METAL["lead"] = [("#2A2C32", 0.0), ("#5C6068", 0.24), ("#A6AAB2", 0.52), ("#6A6E76", 0.76), ("#2A2C32", 1.0)]


def coin_stack(c, x, y, n, r=34.0, a=255, ph=0.0, gap=7.0):
    """Altın sikke yığını (yandan): n sikke alt alta; (x,y) taban."""
    for i in range(int(n)):
        yy = y - i * gap
        jit = math.sin(i * 2.7 + ph) * 1.8
        c.drawOval(skia.Rect.MakeLTRB(x - r + jit, yy - r * 0.30, x + r + jit, yy + r * 0.30), P("#B08828", a))
        c.drawOval(skia.Rect.MakeLTRB(x - r + jit, yy - r * 0.30 - 3, x + r + jit, yy + r * 0.30 - 3), P("#E8C25A", a))
        c.drawOval(skia.Rect.MakeLTRB(x - r + jit, yy - r * 0.30 - 3, x + r + jit, yy + r * 0.30 - 3), S("#4A3410", 1.1, 200))


def coin_flat(c, x, y, r=18.0, a=255):
    """Altın florin (üstten, basit)."""
    sh = skia.GradientShader.MakeRadial((x - r * 0.3, y - r * 0.3), r * 1.5, [C("#FFF0A8", a), C("#E0B040", a), C("#8A6420", a)], [0.0, 0.5, 1.0])
    c.drawCircle(x, y, r, skia.Paint(Shader=sh, AntiAlias=True))
    c.drawCircle(x, y, r, S("#4A3410", 1.4, 220))
    c.drawCircle(x, y, r * 0.66, S("#8A6420", 1.0, 170))
    c.drawLine(x, y - r * 0.42, x, y + r * 0.38, S("#7A5418", 2.0, 170))
    c.drawLine(x - r * 0.28, y - r * 0.12, x + r * 0.28, y - r * 0.12, S("#7A5418", 1.6, 170))
