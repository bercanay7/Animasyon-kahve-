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
import icons_b  # noqa: F401  (b_ simgeleri: b_flame vb.)
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
    """Damga çarpması (0,3 sn). Not: Cinzel'de '○' (U+25CB) glifi YOK (tofu çıkar) → başındaki '○ ' sessizce atılır; anlam sözcüklerde (TEK KAYNAK, YAKLAŞIK ÖZET)."""
    text = text[2:] if text.startswith("○ ") else text

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


# ───────────────────────────── 5) harita yardımcıları (`map` türünün extra= kancası: fn(cx, cam, mv)) ─────────────────────────────
def mx(*fns):
    """Birden çok harita extra'sını art arda çalıştırır."""
    fns = [x for x in fns if x]

    def fn(cx, cam, mv):
        for it in fns:
            it(cx, cam, mv)
    return fn


def mpin(lon, lat, at, color="#B33620", label=None, side="r", size=30, r=11.0, out=None, ring=True, txt=None, dx=18, dy=-10):
    """İğneyle dikilen harita pimi: baş yukarıdan iner, iğne saplanır, halka yayılır; isteğe bağlı etiket. out: pim söner (kararır)."""
    def fn(cx, cam, mv):
        k = cx.amt(at, 0.40, ease=lambda u: ease_out(u, 3))
        if k <= 0.003:
            return
        f = cx.f
        x, y = cam.ll(lon, lat)
        dim_ = 1.0 - (cx.amt(out, 0.7) if out is not None else 0.0) * 0.72
        hy = y - 18 - 90.0 * (1 - k)
        sc = 1.0 + 0.7 * (1 - k)
        a = k
        c = f.c
        f.circle(x, y + 2, 5.0 * k, color="#000000", alpha=0.35 * a, blur=2.5)
        c.drawLine(x, hy + r * sc * 0.6, x, y, S("#2A1A0C", 2.4, int(230 * a)))
        col = mix(color, "#303030", 1.0 - dim_)
        f.circle(x + 2, hy + 3, r * sc * 1.15, color="#000000", alpha=0.30 * a, blur=3.0)
        f.circle(x, hy, r * sc, shader=f.rad(x - r * 0.35, hy - r * 0.4, r * sc * 1.8, [(mix(col, "#FFFFFF", 0.55), 0.0), (col, 0.5), (mix(col, "#000000", 0.45), 1.0)]), alpha=a)
        f.circle(x, hy, r * sc, style="stroke", sw=1.6, color="#2A1A0C", alpha=0.85 * a)
        if ring:
            u = (cx.t - cx.at(at) - 0.30) / 0.9
            if 0 < u < 1:
                f.circle(x, y, 10 + 54 * ease_out(u, 2), style="stroke", sw=2.4, color=color, alpha=0.65 * (1 - u))
        if label:
            ka = clamp((k - 0.4) / 0.6)
            shd = (0, 0, 3.2, "#F3EAD2") if TH.day else (2, 2, 3, "#000000")
            tx = x + (dx if side == "r" else -dx if side == "l" else 0)
            ty = y + dy + size * 0.3 + (-34 if side == "t" else 36 if side == "b" else 0)
            f.text(label, tx, ty, face="cap_b", size=size, color=txt or (TH.fg if TH.day else "#F6ECCB"), align="l" if side == "r" else "r" if side == "l" else "c", alpha=ka * (0.55 + 0.45 * dim_), shadow=shd)
    return fn


def mflag(lon, lat, at, color="#B33620", emblem="plain", h=70.0, out=None, w=46.0, flip=False):
    """Harita üstünde direkli, dalgalanan küçük sancak."""
    def fn(cx, cam, mv):
        k = cx.amt(at, 0.4)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k <= 0.003:
            return
        f = cx.f
        c = f.c
        x, y = cam.ll(lon, lat)
        top = y - h * k
        c.drawLine(x, y, x, top, S("#2A1A0C", 3.2, int(240 * k)))
        pts = [(x, top)]
        n = 8
        for i in range(1, n + 1):
            u = i / n
            wv = math.sin(cx.t * 5.2 - u * 3.6) * 4.2 * u
            pts.append((x + (-1 if flip else 1) * u * w, top + wv))
        pts2 = [(x + (-1 if flip else 1) * u_ * w, top + 0.52 * h * 0.55 + math.sin(cx.t * 5.2 - u_ * 3.6) * 4.2 * u_) for u_ in (1.0, 0.875, 0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.0)]
        poly = sk.poly_path(pts + pts2)
        c.drawPath(poly, P(color, int(255 * k)))
        c.drawPath(poly, S("#2A1A0C", 1.4, int(210 * k)))
        if emblem == "crescent":
            f.circle(x + (-1 if flip else 1) * w * 0.40, top + h * 0.15, 7.5 * k, color="#F4E4B0", alpha=k)
            f.circle(x + (-1 if flip else 1) * w * 0.45, top + h * 0.15, 6.0 * k, color=color, alpha=k)
        elif emblem == "palle":
            f.circle(x + (-1 if flip else 1) * w * 0.40, top + h * 0.15, 5.5 * k, color="#E8C25A", alpha=k)
    return fn


def marrow(pts, at, dur=1.6, color="#A8321E", width=8.0, dash=None, out=None, alpha=1.0, label=None, arrow=True):
    """Rota oku (çizilir); out çapasında çekilir (kuyruktan silinir)."""
    def fn(cx, cam, mv):
        k = ease_io(clamp((cx.t - cx.at(at)) / dur))
        if k <= 0.002:
            return
        al = alpha * (1.0 - (cx.amt(out, 0.6) if out is not None else 0.0))
        if al <= 0.01:
            return
        end = mv.route(cx.f, cam, pts, prog=k, color=color, width=width, dash=dash, arrow=arrow, alpha=al, dash_phase=-cx.t * 36)
        if label and end is not None and k > 0.5:
            CM.ink(cx.f, label, end[0] + 18, end[1] - 14, face="cap_b", size=30, color=TH.fg if TH.day else "#FFF1C4", align="l", alpha=al * cx.amt(at, 0.4, off=dur * 0.5), emboss=TH.day)
    return fn


def mimpact(lon, lat, at, dur=1.4, color="#C0392B", n=3):
    """Çatışma/olay halkaları (kan YOK: yayılan halka + kor)."""
    def fn(cx, cam, mv):
        u0 = (cx.t - cx.at(at)) / dur
        if u0 < 0:
            return
        x, y = cam.ll(lon, lat)
        for i in range(n):
            u = u0 - i * 0.22
            if 0 < u < 1:
                cx.f.circle(x, y, 14 + 90 * ease_out(u, 2), style="stroke", sw=3.2, color=color, alpha=0.7 * (1 - u))
        if u0 < 1.6:
            cx.f.circle(x, y, 30, color=color, alpha=0.20 * (1 - clamp(u0 / 1.6)), blur=10)
    return fn


def mglow(lon, lat, at, out=None, color="#FFD27A", r=44.0, dur=0.5, pulse=0.0):
    """Şube ışığı: yanar (a), out'ta söner (karanlıkta kor). Haritada mum/kandil."""
    def fn(cx, cam, mv):
        k = cx.amt(at, dur)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.7)
        if k <= 0.003:
            return
        x, y = cam.ll(lon, lat)
        fl = 1.0 + 0.10 * math.sin(cx.t * 7.3 + lon) + 0.06 * math.sin(cx.t * 11.1 + lat)
        cx.f.circle(x, y, r * 2.4 * fl, shader=cx.f.rad(x, y, r * 2.4 * fl, [(color, 0.0, int(120 * k)), (color, 1.0, 0)]))
        cx.f.circle(x, y, r * 0.5 * fl, color="#FFF4CC", alpha=0.95 * k)
    return fn


def mbadge(pts, at, dur=2.4, size=56.0, out=None, ease=None):
    """Rota üstünde ilerleyen Medici rozeti (altın yuvarlak + altı top); rota ucunda durur."""
    def fn(cx, cam, mv):
        k = (cx.t - cx.at(at)) / dur
        if k <= 0.0:
            return
        ke = (ease or ease_io)(clamp(k))
        (x, y), ang = mv.point_on(cam, pts, ke)
        a = clamp(k * 6.0) * (1.0 - (cx.amt(out, 0.5) if out is not None else 0.0))
        f = cx.f
        f.circle(x + 3, y + 6, size * 0.56, color="#000000", alpha=0.33 * a, blur=4.0)
        f.circle(x, y, size * 0.54, shader=f.rad(x - size * 0.15, y - size * 0.2, size * 0.9, [("#FFF0A8", 0.0), ("#E0B040", 0.55), ("#8A6420", 1.0)]), alpha=a)
        f.circle(x, y, size * 0.54, style="stroke", sw=2.2, color="#3A2808", alpha=0.9 * a)
        CM.mini_palle(f, x, y, size * 0.78, mono=True, color="#8A2018", alpha=0.95 * a)
    return fn


# ───────────────────────────── 6) küçük çizimler: alev, gül, kristal ─────────────────────────────
def flame(f, x, y, h, t, seed=0, k=1.0, col_in="#FFF4CC", col_out="#FF9A2A"):
    """Küçük mum alevi (taban (x,y), boy h): titreşir/eğilir; k: 0..1 (söner)."""
    if k <= 0.003:
        return
    c = f.c
    fl = math.sin(t * 9.1 + seed) * 0.5 + math.sin(t * 13.7 + seed * 2.3) * 0.35
    hh = h * k * (1.0 + 0.06 * fl)
    sway = fl * h * 0.07
    p = skia.Path()
    p.moveTo(x, y)
    p.cubicTo(x - h * 0.26, y - hh * 0.35, x - h * 0.10 + sway * 0.4, y - hh * 0.72, x + sway, y - hh)
    p.cubicTo(x + h * 0.10 + sway * 0.4, y - hh * 0.72, x + h * 0.26, y - hh * 0.35, x, y)
    f.circle(x + sway * 0.5, y - hh * 0.5, h * 1.5, shader=f.rad(x + sway * 0.5, y - hh * 0.5, h * 1.5, [("#FFB55A", 0.0, int(120 * k)), ("#FFB55A", 1.0, 0)]))
    c.drawPath(p, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(x, y), (x, y - hh)], [C(col_out, int(240 * k)), C(col_in, int(255 * k))], [0.0, 1.0])))


def rose(c, x, y, r, col="#B3301F", edge="#5A1209", a=255):
    """Gül (Güller Savaşı): yarım örtüşen taç yapraklar + iç sarmal."""
    for i in range(5):
        ang = i * 2 * math.pi / 5 - math.pi / 2
        px, py = x + math.cos(ang) * r * 0.52, y + math.sin(ang) * r * 0.52
        c.drawCircle(px, py, r * 0.52, P(col, a))
        c.drawCircle(px, py, r * 0.52, S(edge, max(1.2, r * 0.04), int(a * 0.8)))
    c.drawCircle(x, y, r * 0.45, P(mix(col, "#FFFFFF", 0.12), a))
    p = skia.Path()
    for i in range(40):
        u = i / 39.0
        ang = u * 11.0
        rr = r * (0.04 + 0.36 * u)
        px, py = x + math.cos(ang) * rr, y + math.sin(ang) * rr
        p.moveTo(px, py) if i == 0 else p.lineTo(px, py)
    c.drawPath(p, S(edge, max(1.4, r * 0.05), int(a * 0.85)))
    c.drawCircle(x, y, r * 0.1, P("#E8C25A", a))


def crystal(c, x, y, ang, length, w, a=255, tint="#EAF2F0", seed=0):
    """Altıgen prizma kristal (şap): taban (x,y), açı ang (derece, 0 = yukarı), uzunluk/genişlik."""
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    hw = w / 2
    tipy = -length
    body_top = -length * 0.84
    left = sk.poly_path([(-hw, 0), (-hw * 0.12, 0), (-hw * 0.12, body_top), (-hw, body_top * 0.96)])
    mid = sk.poly_path([(-hw * 0.12, 0), (hw * 0.55, 0), (hw * 0.55, body_top * 0.98), (-hw * 0.12, body_top)])
    right = sk.poly_path([(hw * 0.55, 0), (hw, 0), (hw, body_top * 0.94), (hw * 0.55, body_top * 0.98)])
    for pth, col in ((left, mix(tint, "#FFFFFF", 0.45)), (mid, tint), (right, mix(tint, "#8FA8B8", 0.45))):
        c.drawPath(pth, P(col, a))
    tip = sk.poly_path([(-hw, body_top * 0.96), (-hw * 0.12, body_top), (hw * 0.55, body_top * 0.98), (hw, body_top * 0.94), (hw * 0.2, tipy)])
    c.drawPath(tip, P(mix(tint, "#FFFFFF", 0.3), a))
    for pth in (left, mid, right, tip):
        c.drawPath(pth, S("#6A7E86", max(1.2, w * 0.035), int(a * 0.9)))
    c.drawLine(-hw * 0.5, -length * 0.1, -hw * 0.5, -length * 0.7, S("#FFFFFF", max(1.5, w * 0.05), int(a * 0.65)))
    c.restore()
