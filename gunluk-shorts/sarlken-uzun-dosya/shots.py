"""Çekim şablonları + çalışma zamanı. Sahne dosyaları (scenes_cN.py) yalnızca `shot(...)` çağırır.

Zaman: her çekimin yerel saati `cx.t` (sn). Anlatıma bağlama: `cx.at("c2s6")`, `cx.at("c2s6","florin")` → o cümlenin/sözcüğün
YEREL başlangıç zamanı (sn). `cx.amt(anchor, dur)` → o andan itibaren 0→1 yumuşak ilerleme. Çekim başlangıcı `a=("c2s6", -0.2)`.
Şablon: @kind("ad") ile kayıtlı fonksiyon fn(cx, **params). Çizim: cx.f (sk.Frame). Kamera/hareket: sk.ease_*, mapsk.cam_move.
"""
import json
import math
import os
import re

import numpy as np
import skia

import icons
import medal
import sk
from sk import C, Frame, H, W, clamp, ease_io, ease_out, lerp, mix, seg, smooth

HERE = os.path.dirname(os.path.abspath(__file__))
KINDS = {}
for _m in ("medal_extra", "icons_extra"):      # madalya-lab ekleri (varsa)
    sk.optional_import(_m)


def kind(name):
    def deco(fn):
        KINDS[name] = fn
        return fn
    return deco


# ───────────────────────────── zaman çizelgesi erişimi ─────────────────────────────
class Timeline:
    def __init__(self, path=None):
        d = json.load(open(path or os.path.join(HERE, "out", "timeline.json"), encoding="utf-8"))
        self.total = d["total"]
        self.chapters = {c["id"]: c for c in d["chapters"]}
        self.sent = {s["id"]: s for s in d["sentences"]}
        self.order = [s["id"] for s in d["sentences"]]

    @staticmethod
    def _n(x):
        x = x.replace("İ", "i").replace("I", "ı").lower()
        return re.sub(r"[^\w]", "", x)

    def word(self, sid, key=None, nth=0, end=False):
        s = self.sent[sid]
        if key is None:
            w = s["words"][0] if not end else s["words"][-1]
            return w["t1"] if end else w["t0"]
        if isinstance(key, int):
            w = s["words"][key]
            return w["t1"] if end else w["t0"]
        k = self._n(key)
        hits = [w for w in s["words"] if k in self._n(w["w"])]
        if not hits:
            raise KeyError(f"{sid}: '{key}' sözcüğü yok → {[w['w'] for w in s['words']]}")
        w = hits[min(nth, len(hits) - 1)]
        return w["t1"] if end else w["t0"]

    def t0(self, sid):
        return self.sent[sid]["t0"]

    def t1(self, sid):
        return self.sent[sid]["t1"]

    def resolve(self, a):
        """a: float | (sid, off) | (sid, key, off) | (sid, key, nth, off) → global saniye."""
        if isinstance(a, (int, float)):
            return float(a)
        if len(a) == 2:
            return self.t0(a[0]) + a[1]
        if len(a) == 3:
            return self.word(a[0], a[1]) + a[2]
        return self.word(a[0], a[1], nth=a[2]) + a[3]


TL = None


def timeline():
    global TL
    if TL is None:
        TL = Timeline()
    return TL


class Shot:
    def __init__(self, kind_name, a, params, tr=None, label=""):
        self.kind, self.a, self.params, self.tr, self.label = kind_name, a, params, tr, label
        self.t0 = 0.0
        self.t1 = 0.0
        self.i = 0

    @property
    def dur(self):
        return self.t1 - self.t0


def shot(kind_name, a, tr=None, label="", **params):
    return Shot(kind_name, a, params, tr, label)


class Ctx:
    """Bir çekimin kare başına bağlamı."""

    def __init__(self, f, t, sh, tl):
        self.f, self.t, self.sh, self.tl = f, t, sh, tl
        self.dur = sh.dur
        self.u = clamp(t / max(1e-6, sh.dur))
        self.g = sh.t0 + t               # global saniye
        self.seed = sh.i * 7 + 3

    def at(self, a, key=None, off=0.0):
        """Anlatımdaki an → bu çekimin yerel saniyesi."""
        if isinstance(a, (int, float)):
            return float(a) + off
        if isinstance(a, str):
            s = self.tl.word(a, key) if key is not None else self.tl.t0(a)
            return s - self.sh.t0 + off
        return self.tl.resolve(a) - self.sh.t0 + off

    def amt(self, a, dur=0.5, key=None, off=0.0, ease=smooth):
        return ease(clamp((self.t - self.at(a, key, off)) / dur))

    def fade(self, i=0.5, o=0.5):
        return smooth(self.t / i) * (1 - smooth((self.t - (self.dur - o)) / o)) if self.dur > i + o else smooth(self.t / i)

    def pulse(self, hz=0.6, lo=0.7):
        return lo + (1 - lo) * (0.5 + 0.5 * math.sin(self.t * hz * 2 * math.pi))


# ───────────────────────────── yardımcı çizimler ─────────────────────────────
def gold_flat(f, text, x, y, face="title", size=90, track=4.0, align="c", alpha=1.0, outline=True):
    """Hızlı altın yazı (kabartmasız): dikey degrade + koyu dış hat + üst kenar parlaması."""
    blob, wid = sk.text_blob(face, text, size, track)
    ox = x - (wid / 2 if align == "c" else wid if align == "r" else 0)
    f.c.save(); f.c.translate(ox, y)
    if outline:
        f.c.drawTextBlob(blob, 1.5, 3.0, f.paint("#000000", style="fill", alpha=0.55 * alpha, blur=2.0))
        f.c.drawTextBlob(blob, 0, 0, f.paint("#3A2610", style="stroke", sw=max(1.5, size / 28), alpha=alpha))
    sh = skia.GradientShader.MakeLinear([(0, -size * 0.8), (0, size * 0.15)], [C("#FBE9A6", int(255 * alpha)), C("#E3B54A", int(255 * alpha)), C("#9A6B1A", int(255 * alpha))], [0, 0.55, 1])
    f.c.drawTextBlob(blob, 0, 0, skia.Paint(AntiAlias=True, Shader=sh))
    f.c.restore()
    return wid


def fit_size(text, face, size, max_w, track=0.0):
    w = sk.text_width(text, face, size, track)
    return size if w <= max_w else size * max_w / w


def plate(f, x, y, w, h, alpha=1.0, fill="#1B120B", edge="#C9962B", corner=18, glow=True):
    """Altın çerçeveli koyu levha (isim levhası)."""
    if glow:
        f.rrect(x - 6, y - 6, w + 12, h + 12, corner + 4, color="#000000", alpha=0.35 * alpha, blur=10)
    f.rrect(x, y, w, h, corner, shader=f.lin(x, y, x, y + h, [("#2A1A0F", 0.0), ("#150E08", 1.0)]), alpha=alpha)
    f.rrect(x, y, w, h, corner, style="stroke", sw=3, color=edge, alpha=0.95 * alpha)
    f.rrect(x + 8, y + 8, w - 16, h - 16, corner - 6, style="stroke", sw=1.2, color=edge, alpha=0.6 * alpha)
    for cx_, cy_ in ((x + 8, y + 8), (x + w - 8, y + 8), (x + 8, y + h - 8), (x + w - 8, y + h - 8)):
        f.circle(cx_, cy_, 3.2, color=edge, alpha=0.9 * alpha)


def name_plate(f, name, role=None, dates=None, cx_=W / 2, y=800, alpha=1.0, w=None, t=1.0):
    """Madalya altı isim levhası; t (0..1) açılış animasyonu."""
    a = alpha * smooth(t)
    nsz = fit_size(name, "title_m", 54, 760, 6)
    wn = sk.text_width(name, "title_m", nsz, 6)
    ww = max(wn + 100, 440) if w is None else w
    hh = 96 + (34 if role else 0) + (0 if not dates else 0)
    x = cx_ - ww / 2
    yy = y + (1 - smooth(t)) * 18
    plate(f, x, yy, ww, hh, alpha=a)
    f.text(name, cx_, yy + 56, face="title_m", size=nsz, color="#F3DE9A", align="c", track=6, alpha=a, shadow=(2, 3, 3, "#000000"))
    if role:
        f.text(role, cx_, yy + 88, face="cap_i", size=28, color="#D9C795", align="c", alpha=a)
    if dates:
        f.text(dates, cx_, yy + (88 if not role else 110) + (8 if role else 0), face="cap", size=24, color="#B9A674", align="c", track=3, alpha=a * 0.9)


def kicker(f, text, x, y, alpha=1.0, color="#C9B27A", size=26, track=9, align="c", face="cap"):
    f.text(text, x, y, face=face, size=size, color=color, align=align, track=track, alpha=alpha, shadow=(1, 2, 2, "#000000"))


def stamp(f, text, x, y, rot=-0.12, size=64, color="#B02A2A", alpha=1.0, t=1.0):
    """Kırmızı mühür/damga (RİVAYET, KANIT...). t: 0..1 çarpma animasyonu."""
    if t <= 0:
        return
    sc = 1.0 + (1 - sk.back_out(t)) * 0.9 if t < 1 else 1.0
    a = alpha * min(1.0, t * 3)
    wd = sk.text_width(text, "title", size, 8) + 60
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(math.degrees(rot))
    f.c.scale(sc, sc)
    f.rrect(-wd / 2, -size * 0.85, wd, size * 1.5, 10, style="stroke", sw=6, color=color, alpha=0.9 * a)
    f.rrect(-wd / 2 + 8, -size * 0.85 + 8, wd - 16, size * 1.5 - 16, 6, style="stroke", sw=2.2, color=color, alpha=0.8 * a)
    f.text(text, 0, size * 0.28, face="title", size=size, color=color, align="c", track=8, alpha=0.92 * a)
    f.c.restore()


def velvet(f, hue="#2A1710", glow=("#6B3F1E", 0.5), cx_=W / 2, cy=H * 0.46):
    f.bg("night")
    f.circle(cx_, cy, 520, shader=f.rad(cx_, cy, 520, [("#8A5A2A", 0.0, 90), ("#3A2312", 0.5, 40), ("#000000", 1.0, 0)]))


# ───────────────────────────── çekimler ─────────────────────────────
@kind("title")
def k_title(cx, text="ŞARLKEN", sub=None, kick=None, at=0.0, size=190, glow=True, face="title", rays=True, sub_at=None, kick_at=None, y=0.52):
    f = cx.f
    f.bg("night")
    if rays:
        f.rays(alpha=0.6 + 0.2 * math.sin(cx.t * 0.5))
    sk.dust(f, cx.t, n=80, alpha=0.5)
    a = cx.amt(at, 1.2)
    sc = 1.06 - 0.06 * ease_out(clamp(cx.t / max(0.1, cx.dur)), 2)
    if kick:
        kicker(f, kick, W / 2, H * (y - 0.21), alpha=cx.amt(kick_at if kick_at is not None else at, 0.9, off=0.0 if kick_at is not None else 0.4))
    f.gold(text, W / 2, H * y, face=face, size=size, track=size * 0.12, alpha=a, scale=sc, glow=0.55 * a if glow else 0)
    if sub:
        f.gold(sub, W / 2, H * (y + 0.10), face="title_m", size=40, track=11, alpha=cx.amt(sub_at if sub_at is not None else at, 1.0, off=0.0 if sub_at is not None else 0.7))
    f.vig(0.6)


@kind("emblem")
def k_emblem(cx, icon="imperial_crown", metal="gold", size=460, at=0.0, kick=None, sub=None, stampt=None, pos=(W / 2, H * 0.46), glow=0.45, bgk="night",
             caption=None, bob=6.0, extra=None):
    """Tek büyük kabartma simge + üst/alt yazı + isteğe bağlı damga."""
    f = cx.f
    f.bg(bgk); f.rays(alpha=0.35)
    sk.dust(f, cx.t, n=55)
    a = cx.amt(at, 0.8)
    f.circle(pos[0], pos[1], size * 0.95, shader=f.rad(pos[0], pos[1], size * 0.95, [("#E3B54A", 0.0, int(70 * a)), ("#E3B54A", 1.0, 0)]))
    sc = (0.9 + 0.1 * sk.back_out(a)) * (1.0 + 0.04 * cx.u)
    icons.draw_icon(f, icon, pos[0], pos[1] + math.sin(cx.t * 1.3) * bob, size=size * sc, metal=metal, alpha=a, glow=glow * a)
    if kick:
        kicker(f, kick, W / 2, 130, alpha=cx.amt(at + 0.3, 0.6), size=30, track=12, face="title_m", color="#E0C682")
    if sub:
        f.gold(sub, W / 2, H * 0.84, face="title_m", size=46, track=10, alpha=cx.amt(at + 0.5, 0.8))
    if caption:
        kicker(f, caption, W / 2, H * 0.92, alpha=cx.amt(at + 0.8, 0.6), size=26, track=5, face="cap_i", color="#B9A674")
    if stampt:
        stamp(f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 64)
    if extra:
        extra(cx)
    f.vig(0.6)


@kind("chapter_card")
def k_chapter_card(cx, n="I", title="", years="", front=None, fronts=None, fnow=None):
    f = cx.f
    f.bg("night")
    f.rays(alpha=0.35)
    sk.dust(f, cx.t, n=60, alpha=0.4)
    a = cx.fade(0.35, 0.35)
    kk = cx.amt(0.1, 0.5)
    kicker(f, f"BÖLÜM  {n}", W / 2, H * 0.37, alpha=kk, size=30, track=14)
    # süs çizgisi
    ww = 360 * ease_out(clamp(cx.t / 0.9))
    f.line(W / 2 - ww, H * 0.405, W / 2 + ww, H * 0.405, color="#C9962B", sw=2, alpha=0.8 * a)
    f.circle(W / 2, H * 0.405, 7, color="#C9962B", alpha=a)
    f.circle(W / 2, H * 0.405, 3, color="#1B120B", alpha=a)
    sz = fit_size(title.upper(), "title", 76, 1560, 8)
    f.gold(title.upper(), W / 2, H * 0.54, face="title", size=sz, track=8, alpha=cx.amt(0.25, 0.7))
    if years:
        kicker(f, years, W / 2, H * 0.62, alpha=cx.amt(0.5, 0.6), size=34, track=10, face="cap_i", color="#C9B27A")
    if fronts:
        cephe_row(f, fronts, fnow, y=H * 0.80, alpha=cx.amt(0.6, 0.6), t=cx.t)
    f.vig(0.55)


FRONT_ICONS = [("coinbag", "BANKACI"), ("monk", "KEŞİŞ"), ("crown", "KRAL"), ("crescent", "SULTAN"), ("family", "MİRAS")]


def cephe_row(f, fronts, now, y=860, alpha=1.0, t=0.0, size=74, gap=250, x0=None):
    """Beş cephe göstergesi: fronts = açık (yanmış) indeksler; now = vurgulu indeks."""
    n = len(FRONT_ICONS)
    x0 = W / 2 - gap * (n - 1) / 2 if x0 is None else x0
    for i, (ic, nm) in enumerate(FRONT_ICONS):
        x = x0 + i * gap
        on = i in (fronts or [])
        cur = (i == now)
        a = alpha * (1.0 if on else 0.28)
        if cur:
            f.circle(x, y, size * 0.9, shader=f.rad(x, y, size * 0.9, [("#F0D27A", 0.0, int(120 + 50 * math.sin(t * 4))), ("#F0D27A", 1.0, 0)]))
        icons.draw_icon(f, ic, x, y, size=size * (1.12 if cur else 1.0), metal="gold" if on else "bronze", alpha=a, shadow=False)
        f.text(nm, x, y + size * 0.78, face="cap_b", size=22, color="#E8D49A" if on else "#8A7A55", align="c", track=5, alpha=alpha * (1.0 if on else 0.7))


@kind("cephe")
def k_cephe(cx, fronts=(0,), now=0, big=True):
    """Beş cephe sahnesi (çekimin başında kısa tanıtım)."""
    f = cx.f
    f.bg("night"); f.rays(alpha=0.3)
    sk.dust(f, cx.t, n=50)
    cephe_row(f, fronts, now, y=H * 0.5, alpha=cx.fade(0.4, 0.4), t=cx.t, size=130, gap=330)
    f.vig(0.55)


# ───────────────────────────── MADALYA ─────────────────────────────
def draw_medal(f, key, x, y, size, metal="gold", flip=False, alpha=1.0, tilt=0.0, glint=None, inscription=True, shadow=True):
    """Madalyayı (x,y) merkezine çiz; tilt: -1..1 (y ekseni etrafında dönme hissi); glint: 0..1 parlama bandı konumu."""
    ins = medal.INSCR.get(key) if inscription else None
    img = medal.medal_image(key, metal, ins, flip, size=720)
    s = size / 720.0
    cs = math.cos(tilt * 0.55)
    if shadow:
        f.c.save(); f.c.translate(x + size * 0.03, y + size * 0.05); f.c.scale(s * cs, s)
        p = skia.Paint(AntiAlias=True)
        p.setImageFilter(skia.ImageFilters.Blur(18, 18))
        p.setColorFilter(skia.ColorFilters.Matrix([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.6 * alpha, 0]))
        f.c.drawImage(img, -360, -360, skia.SamplingOptions(skia.FilterMode.kLinear), p)
        f.c.restore()
    f.c.save(); f.c.translate(x, y); f.c.scale(s * cs, s)
    if glint is not None:
        f.c.saveLayer(skia.Rect.MakeLTRB(-380, -380, 380, 380), None)
    p = skia.Paint(AntiAlias=True); p.setAlphaf(clamp(alpha))
    f.c.drawImage(img, -360, -360, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    if glint is not None:
        gx = lerp(-520, 520, glint)
        sh = skia.GradientShader.MakeLinear([(gx - 110, -300), (gx + 110, 300)], [C("#FFFFFF", 0), C("#FFE9A8", int(105 * alpha)), C("#FFFFFF", 0)], [0, 0.5, 1])
        f.c.drawRect(skia.Rect.MakeLTRB(-380, -380, 380, 380), skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kSrcATop))
        f.c.restore()
    f.c.restore()


@kind("medal")
def k_medal(cx, key="karl_genc", metal="gold", name=None, role=None, dates=None, pos="c", size=700, flip=False,
            at=0.0, plate_at=0.5, bgk="night", note=None, stampt=None, zoom=0.05, extra=None):
    f = cx.f
    f.bg(bgk)
    xc = {"c": W / 2, "l": W * 0.34, "r": W * 0.66}[pos]
    yc = H * 0.46 if (name) else H * 0.5
    f.rays(alpha=0.35 + 0.1 * math.sin(cx.t * 0.7))
    a = cx.amt(at, 0.8)
    sc = (1.0 + zoom * cx.u) * (0.94 + 0.06 * ease_out(a))
    tl = 0.22 * math.sin(cx.t * 0.55 + 0.4)
    gl = (cx.t * 0.28 + 0.15) % 1.8
    draw_medal(f, key, xc, yc, size * sc, metal, flip, alpha=a, tilt=tl, glint=(gl if gl < 1 else None))
    sk.dust(f, cx.t, n=60, alpha=0.45)
    if name:
        tx = xc if pos == "c" else (W * 0.78 if pos == "l" else W * 0.22)
        if pos == "c":
            name_plate(f, name, role, dates, cx_=W / 2, y=H * 0.80, t=cx.amt(plate_at, 0.6))
        else:
            name_plate(f, name, role, dates, cx_=tx, y=H * 0.44, t=cx.amt(plate_at, 0.6), w=560)
    if extra:
        extra(cx)
    if stampt:
        stamp(f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 64)
    f.vig(0.55)


@kind("medals")
def k_medals(cx, items=(), size=520, y=H * 0.46, gap=None, bgk="night", title=None, vs=None, plates=True):
    """Yan yana birden çok madalya. items: [dict(key, name, role, dates, at, metal, flip)]."""
    f = cx.f
    f.bg(bgk); f.rays(alpha=0.3)
    n = len(items)
    gap = gap or min(size * 1.15, (W - 200) / n)
    x0 = W / 2 - gap * (n - 1) / 2
    for i, it in enumerate(items):
        a = cx.amt(it.get("at", 0.2 + 0.3 * i), 0.7)
        x = x0 + i * gap
        sc = (0.92 + 0.08 * ease_out(a)) * (1.0 + 0.03 * cx.u)
        draw_medal(f, it["key"], x, y, size * sc, it.get("metal", "gold"), it.get("flip", False), alpha=a,
                   tilt=0.15 * math.sin(cx.t * 0.5 + i), glint=((cx.t * 0.25 + 0.2 * i) % 2.0) if ((cx.t * 0.25 + 0.2 * i) % 2.0) < 1 else None)
        if plates and it.get("name"):
            name_plate(f, it["name"], it.get("role"), it.get("dates"), cx_=x, y=y + size * 0.52, t=cx.amt(it.get("at", 0.2 + 0.3 * i) + 0.4, 0.5), w=min(gap - 20, 520))
    if vs:
        icons.draw_icon(f, "swords", W / 2, y, size=120, metal="silver", alpha=cx.amt(vs, 0.4))
    if title:
        kicker(f, title, W / 2, 120, alpha=cx.fade(0.6, 0.4), size=30, track=12)
    sk.dust(f, cx.t, n=50)
    f.vig(0.55)


# ───────────────────────────── BELGE ─────────────────────────────
_PAPER = {}


def paper_sprite(w, h, seed=3, tone="#EBDDB5"):
    """Yırtık kenarlı parşömen levha sprite (önbellekli)."""
    key = (w, h, seed, tone)
    if key in _PAPER:
        return _PAPER[key]
    pad = 40
    ww, hh = w + 2 * pad, h + 2 * pad
    rs = np.random.RandomState(seed)
    # kenar gürültüsü
    pts = []
    n = 120
    perim = []
    for i in range(n):
        perim.append((pad + w * i / n, pad))
    for i in range(n):
        perim.append((pad + w, pad + h * i / n))
    for i in range(n):
        perim.append((pad + w - w * i / n, pad + h))
    for i in range(n):
        perim.append((pad, pad + h - h * i / n))
    for (x, y) in perim:
        pts.append((x + rs.randn() * 2.2, y + rs.randn() * 2.2))
    path = sk.smooth_path(pts, True, 0.3)
    s = skia.Surface(ww, hh)
    c = s.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    # gölge
    c.drawPath(path, skia.Paint(AntiAlias=True, Color=C("#000000", 130), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14)))
    c.save(); c.translate(0, 0)
    sh = skia.GradientShader.MakeRadial((ww / 2, hh / 2), max(ww, hh) * 0.72, [C(mix(tone, "#FFFFFF", 0.12)), C(mix(tone, "#9C8052", 0.12)), C(mix(tone, "#7A5E30", 0.6))], [0, 0.6, 1])
    c.drawPath(path, skia.Paint(AntiAlias=True, Shader=sh))
    c.clipPath(path, skia.ClipOp.kIntersect, True)
    # leke ve lifler
    for i in range(14):
        x, y, r = rs.rand() * ww, rs.rand() * hh, 30 + rs.rand() * 90
        c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=C("#8C6A30", int(10 + rs.rand() * 22)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r * 0.5)))
    c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=26, Color=C("#6E5028", 90), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14)))
    c.restore()
    img = s.makeImageSnapshot()
    _PAPER[key] = (img, pad)
    return _PAPER[key]


def wax_seal(f, x, y, r=54, color="#8E1F26", alpha=1.0, t=1.0, mono="K"):
    if t <= 0:
        return
    sc = 1.0 + (1 - sk.back_out(t)) * 0.6 if t < 1 else 1.0
    a = alpha * min(1.0, t * 4)
    f.c.save(); f.c.translate(x, y); f.c.scale(sc, sc)
    f.circle(4, 8, r * 1.05, color="#000000", alpha=0.4 * a, blur=6)
    pts = [(math.cos(i * 0.52 + 0.3) * r * (1 + 0.07 * math.sin(i * 3.1)), math.sin(i * 0.52 + 0.3) * r * (1 + 0.07 * math.cos(i * 2.3))) for i in range(13)]
    f.path(sk.smooth_path(pts, True, 0.5), shader=f.rad(-r * 0.3, -r * 0.3, r * 1.6, [(mix(color, "#FFFFFF", 0.35), 0.0), (color, 0.5), (mix(color, "#000000", 0.5), 1.0)]), alpha=a)
    f.circle(0, 0, r * 0.7, style="stroke", sw=3, color=mix(color, "#000000", 0.4), alpha=0.8 * a)
    f.circle(0, 0, r * 0.7, style="stroke", sw=1.5, color=mix(color, "#FFFFFF", 0.4), alpha=0.5 * a)
    f.text(mono, 0, r * 0.28, face="title", size=r * 0.95, color=mix(color, "#000000", 0.45), align="c", alpha=0.9 * a)
    f.c.restore()


@kind("doc")
def k_doc(cx, title="", lines=(), w=1100, h=760, at=0.0, line_dt=0.35, ink="#2A1A0C", seal=None, seal_at=None, tone="#EBDDB5",
          rot=-0.015, zoom=0.06, hl=None, hl_at=None, hl_color="#C9962B", face="fell", size=40, head_size=50, bgk="night", pan=(0, 0),
          caption=None, stampt=None, date=None, align="l"):
    """Parşömen belge: başlık + satır satır belirme + vurgulu ifade + mühür."""
    f = cx.f
    f.bg(bgk)
    f.rays(alpha=0.25)
    img, pad = paper_sprite(w, h, seed=hash(title) % 97 + 3, tone=tone)
    a = cx.amt(at, 0.7)
    sc = (1.0 + zoom * cx.u) * (0.96 + 0.04 * ease_out(a))
    cxp, cyp = W / 2 + pan[0] * cx.u, H * 0.5 + pan[1] * cx.u
    f.c.save(); f.c.translate(cxp, cyp); f.c.rotate(math.degrees(rot * (1 - 0.4 * cx.u))); f.c.scale(sc, sc)
    p = skia.Paint(AntiAlias=True); p.setAlphaf(a)
    f.c.drawImage(img, -w / 2 - pad, -h / 2 - pad, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    # içerik
    y = -h / 2 + 90
    if title:
        tsz = fit_size(title, "fell", head_size, w - 160, 2)
        f.text(title, 0, y, face="fell", size=tsz, color=ink, align="c", track=2, alpha=a * cx.amt(at + 0.3, 0.5))
        f.line(-w * 0.32, y + 18, w * 0.32, y + 18, color=ink, sw=1.6, alpha=0.6 * a)
        y += 76
    xs = -w / 2 + 90
    for i, ln in enumerate(lines):
        t_i = cx.at(at, off=0.5 + i * line_dt) if not isinstance(ln, tuple) else cx.at(ln[1], off=0.0)
        text = ln if not isinstance(ln, tuple) else ln[0]
        prog = clamp((cx.t - t_i) / 0.55)
        if prog > 0:
            wt = sk.text_width(text, face, size, 0)
            f.c.save()
            f.c.clipRect(skia.Rect.MakeXYWH(xs - 6, y - size, (wt + 20) * prog, size * 1.6))
            if align == "c":
                f.text(text, 0, y, face=face, size=size, color=ink, align="c", alpha=a)
            else:
                f.text(text, xs, y, face=face, size=size, color=ink, align="l", alpha=a)
            f.c.restore()
        y += size * 1.42
    if hl and hl_at is not None:
        # vurgulu ifade: altın alt çizgi + parıltı
        k = clamp((cx.t - cx.at(hl_at)) / 0.6)
        hx, hy, hw = hl
        f.rect(hx, hy - size * 0.9, hw * k, size * 1.25, color=hl_color, alpha=0.22 * a, blur=6)
        f.line(hx, hy + 8, hx + hw * k, hy + 8, color=hl_color, sw=4.5, alpha=0.95 * a)
    if date:
        f.text(date, w / 2 - 90, h / 2 - 54, face="fell_i", size=34, color=ink, align="r", alpha=a * 0.9)
    if seal:
        wax_seal(f, w / 2 - 150, h / 2 - 90, 58, color=seal if isinstance(seal, str) else "#8E1F26", t=cx.amt(seal_at if seal_at is not None else at + 1.4, 0.35), alpha=a, mono="K")
    f.c.restore()
    if caption:
        kicker(f, caption, W / 2, H - 70, alpha=cx.amt(at + 0.6, 0.6), size=24, track=6, face="cap_i", color="#B9A674")
    if stampt:
        stamp(f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 60)
    sk.dust(f, cx.t, n=40, alpha=0.35)
    f.vig(0.5)


# ───────────────────────────── ALINTI ─────────────────────────────
@kind("quote")
def k_quote(cx, text="", who=None, src=None, at=0.0, size=64, stampt=None, bgk="night", face="cap_i", color="#F1E3B8", mark=True, wrap=1500, y0=None, pos="c"):
    f = cx.f
    f.bg(bgk); f.rays(alpha=0.3)
    sk.dust(f, cx.t, n=50)
    lines = sk.wrap_text(text, face, size, wrap)
    a = cx.amt(at, 0.9)
    total = len(lines) * size * 1.3
    y = (y0 if y0 is not None else H * 0.5 - total / 2 + size * 0.6)
    if mark:
        f.text("“", W / 2 - wrap / 2 - 30, y - 10, face="title", size=200, color="#C9962B", align="l", alpha=0.55 * a)
    for i, ln in enumerate(lines):
        ai = cx.amt(at + 0.15 * i, 0.7)
        f.text(ln, W / 2, y + i * size * 1.3, face=face, size=size, color=color, align="c", alpha=ai, shadow=(2, 3, 4, "#000000"))
    yy = y + len(lines) * size * 1.3 + 20
    if who:
        f.line(W / 2 - 80, yy, W / 2 + 80, yy, color="#C9962B", sw=2, alpha=0.7 * a)
        kicker(f, who, W / 2, yy + 52, alpha=cx.amt(at + 0.5 + 0.15 * len(lines), 0.6), size=30, track=7, face="title_m", color="#D8C07A")
    if src:
        kicker(f, src, W / 2, yy + 100, alpha=cx.amt(at + 0.7 + 0.15 * len(lines), 0.6), size=24, track=4, face="cap_i", color="#A89868")
    if stampt:
        stamp(f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 64)
    f.vig(0.6)


# ───────────────────────────── SAYILAR ─────────────────────────────
def fmt_int(v):
    return f"{int(round(v)):,}".replace(",", ".")


@kind("counter")
def k_counter(cx, value=850000, unit="florin", label="", at=0.0, dur=1.6, icon=None, color="gold", sub=None, size=210, bgk="night", prefix="", suffix="", decimals=0, big_label=None, pos=(W / 2, H * 0.5)):
    f = cx.f
    f.bg(bgk); f.rays(alpha=0.3)
    sk.dust(f, cx.t, n=50)
    k = ease_out(clamp((cx.t - cx.at(at)) / dur), 3)
    v = value * k
    s = (f"{v:.{decimals}f}".replace(".", ",") if decimals else fmt_int(v))
    a = cx.amt(at, 0.4)
    if icon:
        icons.draw_icon(f, icon, pos[0], pos[1] - size * 1.0, size=size * 0.95, metal="gold", alpha=a, glow=0.3)
    wd = gold_flat(f, prefix + s + suffix, pos[0], pos[1] + size * 0.3, face="title", size=size, track=6, alpha=a)
    if unit:
        f.text(unit.upper(), pos[0], pos[1] + size * 0.3 + 76, face="title_m", size=48, color="#E0C682", align="c", track=14, alpha=cx.amt(at + 0.3, 0.5))
    if label:
        f.text(label, pos[0], pos[1] + size * 0.3 + 140, face="cap_i", size=40, color="#C9B27A", align="c", alpha=cx.amt(at + 0.6, 0.6))
    if sub:
        f.text(sub, pos[0], pos[1] + size * 0.3 + 190, face="cap", size=28, color="#A89868", align="c", alpha=cx.amt(at + 0.9, 0.6), track=3)
    f.vig(0.6)


@kind("bars")
def k_bars(cx, items=(), unit="", at=0.0, title=None, maxv=None, bgk="night", dur=1.4, x0=420, bar_h=62, gap=34, w=1000, y0=None, valfmt=None):
    """Yatay çubuklar. items: [(etiket, değer, renk, anahtarSöz?)]"""
    f = cx.f
    f.bg(bgk); f.rays(alpha=0.25)
    sk.dust(f, cx.t, n=40, alpha=0.4)
    n = len(items)
    maxv = maxv or max(i[1] for i in items)
    tot_h = n * bar_h + (n - 1) * gap
    y = (y0 if y0 is not None else H / 2 - tot_h / 2 + 30)
    if title:
        kicker(f, title, W / 2, y - 90, alpha=cx.amt(at, 0.6), size=34, track=10, face="title_m", color="#E0C682")
    for i, it in enumerate(items):
        lab, val, col = it[0], it[1], it[2]
        ta = it[3] if len(it) > 3 else at + 0.3 * i
        k = ease_out(clamp((cx.t - cx.at(ta)) / dur), 3)
        a = cx.amt(ta, 0.4)
        yy = y + i * (bar_h + gap)
        f.text(lab, x0 - 30, yy + bar_h * 0.66, face="title_m", size=30, color="#E7D5A0", align="r", track=4, alpha=a)
        f.rrect(x0, yy, w, bar_h, 12, color="#000000", alpha=0.35 * a)
        bw = max(0.1, w * val / maxv * k)
        f.rrect(x0, yy, bw, bar_h, 12, shader=f.lin(x0, yy, x0, yy + bar_h, [(mix(col, "#FFFFFF", 0.28), 0.0), (col, 0.55), (mix(col, "#000000", 0.35), 1.0)]), alpha=a)
        f.rrect(x0, yy, bw, bar_h, 12, style="stroke", sw=2, color=mix(col, "#FFFFFF", 0.5), alpha=0.7 * a)
        vs = (valfmt(val * k) if valfmt else fmt_int(val * k)) + (" " + unit if unit else "")
        f.text(vs, x0 + bw + 22, yy + bar_h * 0.68, face="title_m", size=34, color="#F4E3AA", align="l", alpha=a, shadow=(2, 2, 3, "#000000"))
    f.vig(0.55)


@kind("stacked")
def k_stacked(cx, parts=(), total_label=None, total=None, unit="florin", at=0.0, dur=1.6, bgk="night", title=None, y=H * 0.5, w=1500, h=120):
    """Parçalı tek çubuk: parts=[(etiket, değer, renk, anahtar)]; toplam üstte."""
    f = cx.f
    f.bg(bgk); f.rays(alpha=0.25); sk.dust(f, cx.t, n=40, alpha=0.4)
    tot = total or sum(p[1] for p in parts)
    x0 = W / 2 - w / 2
    if title:
        kicker(f, title, W / 2, y - 180, alpha=cx.amt(at, 0.6), size=34, track=10, face="title_m", color="#E0C682")
    f.rrect(x0 - 6, y - 6, w + 12, h + 12, 16, style="stroke", sw=3, color="#C9962B", alpha=0.8 * cx.amt(at, 0.5))
    x = x0
    for i, p in enumerate(parts):
        lab, val, col = p[0], p[1], p[2]
        ta = p[3] if len(p) > 3 else at + 0.5 * i
        k = ease_out(clamp((cx.t - cx.at(ta)) / dur), 3)
        a = cx.amt(ta, 0.4)
        pw = w * val / tot * k
        f.rect(x, y, pw, h, shader=f.lin(x, y, x, y + h, [(mix(col, "#FFFFFF", 0.3), 0.0), (col, 0.5), (mix(col, "#000000", 0.4), 1.0)]), alpha=a)
        f.line(x + pw, y, x + pw, y + h, color="#2A1A0C", sw=3, alpha=0.8 * a)
        if k > 0.55:
            f.text(fmt_int(val * k), x + pw / 2, y + h * 0.62, face="title_m", size=min(44, pw * 0.2), color="#FFF3CC", align="c", alpha=a)
            f.text(lab, x + pw / 2, y + h + 56, face="title_m", size=28, color="#E7D5A0", align="c", track=4, alpha=a)
        x += pw
    if total_label:
        a = cx.amt(at + 0.1, 0.6)
        f.text(total_label, W / 2, y - 60, face="title", size=64, color="#F4DD92", align="c", track=6, alpha=a, shadow=(2, 3, 4, "#000000"))
    f.vig(0.55)


@kind("timeline")
def k_timeline(cx, a0=1500, a1=1560, events=(), at=0.0, bgk="night", title=None, hl=None, y=H * 0.52, step=10, dur=1.0, w=1560):
    """Yıl cetveli: events=[(yıl, etiket, anahtar?, renk?)]; hl=(yıl0, yıl1, etiket) vurgulu aralık (örn. 43 yıl)."""
    f = cx.f
    f.bg(bgk); f.rays(alpha=0.25); sk.dust(f, cx.t, n=40, alpha=0.4)
    x0 = W / 2 - w / 2
    def X(yr):
        return x0 + (yr - a0) / (a1 - a0) * w
    a = cx.amt(at, 0.6)
    if title:
        kicker(f, title, W / 2, 140, alpha=a, size=32, track=10, face="title_m", color="#E0C682")
    f.line(x0, y, x0 + w * ease_out(clamp((cx.t - cx.at(at)) / 0.9)), y, color="#C9962B", sw=4, alpha=0.9)
    yr = a0
    while yr <= a1:
        xx = X(yr)
        if xx <= x0 + w * ease_out(clamp((cx.t - cx.at(at)) / 0.9)) + 1:
            L = 20 if yr % (step * 2) == 0 else 12
            f.line(xx, y - L, xx, y + L, color="#C9962B", sw=2, alpha=0.8)
            if yr % (step * 2) == 0:
                f.text(str(yr), xx, y + 62, face="title_m", size=26, color="#CDBB86", align="c", track=3, alpha=0.9)
        yr += step
    for i, ev in enumerate(events):
        yr_, lab = ev[0], ev[1]
        ta = ev[2] if len(ev) > 2 and ev[2] is not None else at + 0.5 + 0.4 * i
        col = ev[3] if len(ev) > 3 else "#F0D27A"
        k = cx.amt(ta, 0.5)
        xx = X(yr_)
        up = -1 if i % 2 == 0 else 1
        f.line(xx, y, xx, y + up * 100 * k, color=col, sw=2.5, alpha=0.9 * k)
        f.circle(xx, y, 11 * k, color=col, alpha=k)
        f.circle(xx, y, 11 * k, style="stroke", sw=2, color="#2A1A0C", alpha=k)
        ty = y + up * (150 if up > 0 else 128)
        f.text(str(yr_), xx, ty - 36, face="title", size=40, color=col, align="c", alpha=k, track=3, shadow=(2, 2, 3, "#000000"))
        f.text(lab, xx, ty + 4, face="cap_b", size=30, color="#F2E4B8", align="c", alpha=k, shadow=(2, 2, 3, "#000000"))
    if hl:
        y0_, y1_, lab = hl[0], hl[1], hl[2]
        ta = hl[3] if len(hl) > 3 else at + 2.0
        k = cx.amt(ta, 0.8)
        xa, xb = X(y0_), X(y1_)
        f.rrect(xa, y - 10, (xb - xa) * k, 20, 10, color="#C0392B", alpha=0.55)
        f.text(lab, (xa + xb) / 2, y - 60, face="title", size=54, color="#F4DD92", align="c", alpha=k, track=6, shadow=(2, 3, 4, "#000000"))
    f.vig(0.55)


# ───────────────────────────── SOY AĞACI ─────────────────────────────
@kind("tree")
def k_tree(cx, nodes=(), edges=(), at=0.0, bgk="night", title=None, size=210):
    """nodes=[dict(id, key (madalya anahtarı) | icon, name, dates, x, y (0..1), at, metal, size)];
    edges=[(a,b,at,renk?)] yukarıdan aşağı çizgiler (ebeveyn→çocuk)."""
    f = cx.f
    f.bg(bgk); f.rays(alpha=0.25); sk.dust(f, cx.t, n=40, alpha=0.4)
    pos = {n["id"]: (n["x"] * W, n["y"] * H) for n in nodes}
    if title:
        kicker(f, title, W / 2, 110, alpha=cx.amt(at, 0.6), size=30, track=10, face="title_m", color="#E0C682")
    for e in edges:
        a_, b_ = e[0], e[1]
        ta = e[2] if len(e) > 2 else at
        col = e[3] if len(e) > 3 else "#C9962B"
        k = ease_out(clamp((cx.t - cx.at(ta)) / 0.8), 2)
        if k <= 0:
            continue
        (xa, ya), (xb, yb) = pos[a_], pos[b_]
        ym = (ya + yb) / 2
        p = skia.Path(); p.moveTo(xa, ya + 20); p.cubicTo(xa, ym, xb, ym, xb, yb - 20)
        pm = skia.PathMeasure(p, False); part = skia.Path(); pm.getSegment(0, pm.getLength() * k, part, True)
        f.path(part, style="stroke", sw=9, color="#000000", alpha=0.45)
        f.path(part, style="stroke", sw=4, color=col, alpha=0.95)
    for n in nodes:
        ta = n.get("at", at)
        k = cx.amt(ta, 0.6)
        if k <= 0:
            continue
        x, y = pos[n["id"]]
        s = n.get("size", size) * (0.88 + 0.12 * ease_out(k))
        if n.get("key"):
            draw_medal(f, n["key"], x, y, s, n.get("metal", "gold"), n.get("flip", False), alpha=k, inscription=n.get("ins", False))
        elif n.get("icon"):
            icons.draw_icon(f, n["icon"], x, y, size=s * 0.8, metal=n.get("metal", "gold"), alpha=k, glow=0.25)
        if n.get("name"):
            f.text(n["name"], x, y + s / 2 + 38, face="title_m", size=n.get("nsize", 25), color="#F0DDA0", align="c", track=3, alpha=k, shadow=(2, 2, 3, "#000000"))
        if n.get("dates"):
            f.text(n["dates"], x, y + s / 2 + 68, face="cap_i", size=22, color="#B9A674", align="c", alpha=k * 0.9)
        if n.get("tag"):
            f.text(n["tag"], x, y - s / 2 - 16, face="cap_b", size=24, color="#F6D77A", align="c", track=4, alpha=k)
    f.vig(0.55)


# ───────────────────────────── HARİTA ŞABLONU ─────────────────────────────
_MV = None


def mapview():
    global _MV
    if _MV is None:
        import mapsk
        _MV = mapsk.MapView()
    return _MV


def _fac(c):
    if isinstance(c, str) and c in sk.FAC:
        return sk.FAC[c][0]
    return c


@kind("map")
def k_map(cx, cam=(8, 47, 1.5), cams=None, style="night", regions=(), cities=(), routes=(), labels=(), icons_=(), notes=(), date=None,
          frame=True, compass=None, mountains=True, drift=None, tint=None, ripples=True, grid=False, hud=None, vig=0.55, extra=None, kick=None, approx=True):
    """Genel harita çekimi.
    cams: [(an, (lon,lat,zoom)), ...] an = yerel sn veya anlatım çapası (cx.at ile çözülür) — aralarda yumuşak geçiş (zoom log).
    regions: [dict(name, color, at, alpha, hatch, glow)]; cities: [dict(lon,lat,name,kind,at,side)];
    routes: [dict(pts, at, dur, color, width, dash, label, arrow)]; labels: [dict(text,lon,lat,size,color,at,face,track,rot)];
    icons_: [dict(kind, lon, lat, size, at, metal, rot, bob)]; notes: [dict(text, x, y, at, w, size, sub)]"""
    import mapsk
    f = cx.f
    mv = mapview()
    if cams:
        ks = [(cx.at(a), v) for a, v in cams]
        c0 = ks[0][1]
        if cx.t <= ks[0][0]:
            cm = mapsk.Cam(*c0)
        elif cx.t >= ks[-1][0]:
            cm = mapsk.Cam(*ks[-1][1])
        else:
            for (ta, va), (tb, vb) in zip(ks[:-1], ks[1:]):
                if ta <= cx.t <= tb:
                    cm = mapsk.cam_move(va, vb, (cx.t - ta) / max(1e-6, tb - ta))
                    break
    else:
        lon, lat, z = cam
        if drift:
            lon, lat, z = lon + drift[0] * cx.u, lat + drift[1] * cx.u, z * (1 + drift[2] * cx.u)
        cm = mapsk.Cam(lon, lat, z)
    mv.base(f, cm, style, t=cx.t, mountains=mountains, ripples=ripples, tint=tint)
    nightp = style == "night"
    for r in regions:
        k = cx.amt(r.get("at", 0.0), r.get("dur", 0.8))
        if k > 0:
            mv.region(f, cm, r["name"], _fac(r["color"]), alpha=r.get("alpha", 0.62), amt=k, hatch=r.get("hatch", False), glow=r.get("glow", True))
    for l in labels:
        k = cx.amt(l.get("at", 0.0), 0.7)
        if k > 0:
            mv.label(f, cm, l["text"], l["lon"], l["lat"], size=l.get("size", 34), color=l.get("color", "#E8D7A4" if nightp else "#3B2814"), face=l.get("face", "title_m"),
                     track=l.get("track", 10), alpha=k * l.get("alpha", 1.0), rot=l.get("rot", 0.0), scale_with_zoom=l.get("swz", 0.0))
    for r in routes:
        ta = r.get("at", 0.0)
        k = ease_io(clamp((cx.t - cx.at(ta)) / r.get("dur", 1.8)))
        if k > 0:
            end = mv.route(f, cm, r["pts"], prog=k, color=_fac(r.get("color", "#F0D27A")), width=r.get("width", 5.0), dash=r.get("dash"), arrow=r.get("arrow", True),
                           alpha=r.get("alpha", 1.0), dash_phase=-cx.t * 30)
            if r.get("label") and end is not None and k > 0.5:
                f.text(r["label"], end[0] + 16, end[1] - 14, face="cap_b", size=r.get("lsize", 28), color="#FFF1C4", align="l", alpha=cx.amt(ta, 0.4, off=r.get("dur", 1.8) * 0.5), shadow=(2, 2, 3, "#000000"))
    for c in cities:
        mv.city(f, cm, c["lon"], c["lat"], c.get("name"), kind=c.get("kind", "town"), t=cx.t, color=c.get("color", "#F0D27A"), size=c.get("size", 26),
                name_side=c.get("side", "r"), amt=cx.amt(c.get("at", 0.0), 0.5))
    for ic in icons_:
        k = cx.amt(ic.get("at", 0.0), 0.5)
        if k <= 0:
            continue
        if "route" in ic:
            pr = ease_io(clamp((cx.t - cx.at(ic.get("move_at", ic.get("at", 0.0)))) / ic.get("move_dur", 3.0)))
            (x, y), ang = mv.point_on(cm, ic["route"], pr)
            rot = ic.get("rot", 0.0)
        else:
            x, y = cm.ll(ic["lon"], ic["lat"])
            rot = ic.get("rot", 0.0)
        bob = math.sin(cx.t * 2.0 + ic.get("lon", 0)) * ic.get("bob", 0.0)
        icons.draw_icon(f, ic["kind"], x, y + bob, size=ic.get("size", 70) * (0.8 + 0.2 * ease_out(k)), metal=ic.get("metal", "gold"), alpha=k, rot=rot, glow=ic.get("glow", 0.0), flip=ic.get("flip", False))
    if frame:
        mv.frame(f, style)
    if compass is not None or frame:
        cp = compass if compass else (1790, 920, 64)
        mv.compass(f, cp[0], cp[1], cp[2], alpha=0.85, style=style)
    if date:
        _date_stamp(f, date, cx)
    if approx and regions:
        f.text("SINIRLAR YAKLAŞIKTIR", W / 2, H - 62, face="cap_i", size=22, color="#B9A674", align="c", track=5, alpha=0.6 * cx.amt(0.8, 0.6))
    for n in notes:
        k = cx.amt(n.get("at", 0.0), 0.5)
        if k > 0:
            callout(f, n["text"], n["x"], n["y"], k, w=n.get("w", 520), size=n.get("size", 34), sub=n.get("sub"), align=n.get("align", "l"))
    if kick:
        kicker(f, kick, W / 2, 96, alpha=cx.fade(0.5, 0.4), size=28, track=11, face="title_m", color="#E0C682")
    if extra:
        extra(cx, cm, mv)
    f.vig(vig)


def _date_stamp(f, date, cx):
    txt, at_ = (date, 0.2) if isinstance(date, str) else date
    k = cx.amt(at_, 0.6)
    if k <= 0:
        return
    sz = 60
    wd = sk.text_width(txt, "title", sz, 6) + 80
    x, y = 90, H - 100
    f.rrect(x, y - 70 * k, wd, 90, 12, color="#150D08", alpha=0.78 * k)
    f.rrect(x, y - 70 * k, wd, 90, 12, style="stroke", sw=2.5, color="#C9962B", alpha=0.9 * k)
    f.text(txt, x + wd / 2, y - 6 * k, face="title", size=sz * 0.8, color="#F4DD92", align="c", track=6, alpha=k, shadow=(2, 2, 3, "#000000"))


def callout(f, text, x, y, k=1.0, w=520, size=34, sub=None, align="l"):
    lines = sk.wrap_text(text, "cap_b", size, w - 56)
    h = len(lines) * size * 1.22 + 36 + (size * 0.8 if sub else 0)
    xx = x if align == "l" else x - w
    f.rrect(xx, y - 10 + (1 - k) * 10, w, h, 14, color="#150D08", alpha=0.86 * k)
    f.rrect(xx, y - 10 + (1 - k) * 10, w, h, 14, style="stroke", sw=2.2, color="#C9962B", alpha=0.9 * k)
    for i, ln in enumerate(lines):
        f.text(ln, xx + 28, y + 30 + i * size * 1.22 + (1 - k) * 10, face="cap_b", size=size, color="#F4E6BC", align="l", alpha=k)
    if sub:
        f.text(sub, xx + 28, y + 30 + len(lines) * size * 1.22 + 6, face="cap_i", size=size * 0.74, color="#C9B27A", align="l", alpha=k)


@kind("iconrow")
def k_iconrow(cx, items=(), at=0.0, bgk="night", y=H * 0.5, size=190, gap=None, title=None, hl=None, metal="gold"):
    """items=[dict(icon, label, at, metal)] yan yana simgeler."""
    f = cx.f
    f.bg(bgk); f.rays(alpha=0.3); sk.dust(f, cx.t, n=50)
    n = len(items)
    gap = gap or min(size * 1.6, (W - 260) / max(1, n - 1 if n > 1 else 1))
    x0 = W / 2 - gap * (n - 1) / 2
    if title:
        kicker(f, title, W / 2, 130, alpha=cx.amt(at, 0.6), size=32, track=11, face="title_m", color="#E0C682")
    for i, it in enumerate(items):
        ta = it.get("at", at + 0.4 * i)
        k = cx.amt(ta, 0.55)
        x = x0 + i * gap
        sc = 0.8 + 0.2 * sk.back_out(k)
        if hl is not None and hl == i:
            f.circle(x, y, size * 0.9, shader=f.rad(x, y, size * 0.9, [("#F0D27A", 0.0, int(110 + 40 * math.sin(cx.t * 4))), ("#F0D27A", 1.0, 0)]))
        icons.draw_icon(f, it["icon"], x, y - 10 * (1 - k), size=size * sc, metal=it.get("metal", metal), alpha=k, glow=0.2)
        if it.get("label"):
            f.text(it["label"], x, y + size * 0.78, face="title_m", size=30, color="#F0DDA0", align="c", track=6, alpha=k, shadow=(2, 2, 3, "#000000"))
        if it.get("sub"):
            f.text(it["sub"], x, y + size * 0.78 + 40, face="cap_i", size=26, color="#B9A674", align="c", alpha=k)
    f.vig(0.55)


@kind("black")
def k_black(cx, text=None, at=0.0, size=60, color="#D9C795"):
    f = cx.f
    f.clear("#000000")
    if text:
        f.text(text, W / 2, H / 2, face="cap_i", size=size, color=color, align="c", alpha=cx.amt(at, 0.8))
