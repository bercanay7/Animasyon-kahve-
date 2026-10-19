"""p3_lib — PARÇA 3 (c6 Lorenzo · c7 26 Nisan 1478) ortak çizim/yardımcı işlevleri (Parça 3 sahne yazarı modülü).

Motor/dünya dosyalarına DOKUNMAZ; yalnız onların işlevlerini çağırır (cilt_medici, cilt_anim, cilt_pano, cilt_oda, cilt_paper, cilt_kinds2, cilt_medal).
İçerik:
  * boya kısayolları, `bake` (statik katman önbelleği), `blit`
  * gravür filtresi (`mono_begin/mono_end`): ANEKDOT/rivayet çekimleri siyah-beyaz sepya gravür dilinde (Parça 2 ile aynı sözleşme: renk = belge, gravür = rivayet)
  * etiket/levha/damga/tarih yardımcıları (çapaya bağlı)
  * stilize madalya anahtarları (yüz iddiası YOK; üretilmiş profil): c6_piero, c6_giuliano, c6_simonetta, c6_clarice, c7_riario
  * `world_to_screen` (oda/pano dünyası x,y → ekran) ve `cam_probe` (kamera yolu önizlemesi)
Kural: yüz çizilmez (siluet/madalya), şiddet/kan yok; ekrana yalnız script/brif sözcükleri yazılır.
"""
import functools
import math

import numpy as np
import skia

import cilt_anim as FA
import cilt_medici as CM
import cilt_oda as OD
import cilt_pano as PN
import cilt_paper as PP
import medal
import sk
from cilt_medici import TH
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


# ───────────────────────────── stilize madalya anahtarları ─────────────────────────────
def _reg_medals():
    base = dict(mouth_open=0.0, _x=True, ear=False)
    medal.PEOPLE.setdefault("c6_piero", dict(base, nose=16, hook=3, brow=3, lip=1, lip2=2, chin=-2, jaw=0.9, fore=3, age=0.7, jowl=0.25, neck=0.95,
                                              hair="thin_back", hat="merchant_cap", beard=None, garment="fur_gown_merchant", scale=1.04, dy=-6, eye="std", brow_style="std"))
    medal.PEOPLE.setdefault("c6_giuliano", dict(base, nose=9, hook=0, brow=2, lip=3, lip2=7, chin=9, jaw=0.95, fore=2, age=0.0, jowl=0.0, neck=1.0,
                                                 hair="wavy", hat="none", beard=None, garment="courtly_jacket", scale=1.04, dy=-8, eye="std", brow_style="arch"))
    medal.PEOPLE.setdefault("c6_simonetta", dict(base, nose=7, hook=0, brow=1, lip=2, lip2=5, chin=7, jaw=0.8, fore=3, age=0.0, jowl=0.0, neck=0.85,
                                                  hair="none", hat="jeweled_net", beard=None, garment="jeweled_gown", scale=1.08, dy=-12, nback=380, gv="tudor", eye="almond", lash=True, brow_style="arch"))
    medal.PEOPLE.setdefault("c6_clarice", dict(base, nose=8, hook=0, brow=1, lip=2, lip2=6, chin=9, jaw=0.82, fore=2, age=0.0, jowl=0.0, neck=0.86,
                                                hair="none", hat="gold_haube", beard=None, garment="dark_gown_collar", scale=1.06, dy=-10, nback=384, eye="almond", lash=True, brow_style="arch"))
    medal.PEOPLE.setdefault("c7_riario", dict(base, nose=9, hook=0, brow=2, lip=2, lip2=5, chin=6, jaw=0.9, fore=3, age=0.0, jowl=0.0, neck=0.95,
                                               hair="none", hat="biretta", beard=None, garment="cassock_x", scale=1.04, dy=-12, eye="std", brow_style="std"))
    medal.INSCR.setdefault("c6_piero", "PETRVS · MEDICES · COSMI · F ·")
    medal.INSCR.setdefault("c6_giuliano", "IVLIANVS · MEDICES ·")
    medal.INSCR.setdefault("c6_simonetta", "· · · · · · ·")
    medal.INSCR.setdefault("c6_clarice", "· · · · · · ·")
    medal.INSCR.setdefault("c7_riario", "· · · · · · ·")


_reg_medals()


# ───────────────────────────── önbellek / blit ─────────────────────────────
_BAKED = {}


def bake(key, w, h, draw):
    """Statik katmanı bir kez görüntüye pişir (key ile önbellek). draw(frame) → tuval (0,0)–(w,h)."""
    im = _BAKED.get(key)
    if im is None:
        fr = sk.Frame(int(w), int(h))
        fr.clear(skia.ColorTRANSPARENT)
        draw(fr)
        im = _BAKED[key] = fr.surf.makeImageSnapshot()
    return im


def blit(c, im, x, y, a=1.0, sx=1.0, sy=None, rot=0.0, ax=0.5, ay=0.5):
    sy = sx if sy is None else sy
    p = skia.Paint(AntiAlias=True)
    if a < 1.0:
        p.setAlphaf(clamp(a))
    c.save()
    c.translate(x, y)
    if rot:
        c.rotate(rot)
    c.scale(sx, sy)
    c.drawImage(im, -ax * im.width(), -ay * im.height(), LIN, p)
    c.restore()


# ───────────────────────────── gravür filtresi (rivayet/ANEKDOT) ─────────────────────────────
_MONO = {}


def _mono_filter(k=1.0, tone=(1.00, 0.93, 0.80), contrast=1.10):
    key = (round(k, 2), tone, contrast)
    cf = _MONO.get(key)
    if cf is None:
        lr, lg, lb = 0.30, 0.59, 0.11
        rows = []
        for ti in tone:
            a = ti * contrast
            rows.append([lr * a, lg * a, lb * a, 0, (1 - contrast) * 0.5 * ti * 0.8])
        ident = [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0]]
        m = []
        for r_i in range(3):
            m += [ident[r_i][j] * (1 - k) + rows[r_i][j] * k for j in range(5)]
        m += [0, 0, 0, 1, 0]
        cf = _MONO[key] = skia.ColorFilters.Matrix(m)
    return cf


def mono_begin(f, k=1.0, tone=(1.00, 0.93, 0.80), contrast=1.10):
    """Gravür katmanı aç: içinde çizilen her şey siyah-beyaz sepya mürekkebe çevrilir (k<1: renkten gravüre geçiş)."""
    if k <= 0.001:
        f.c.save()
        return False
    f.c.saveLayer(None, skia.Paint(ColorFilter=_mono_filter(k, tone, contrast)))
    return True


def mono_end(f):
    f.c.restore()


# ───────────────────────────── yazı / etiket / damga ─────────────────────────────
def tag(f, cx, text, x, y, at=0.0, size=34, face="title_m", track=6.0, sub=None, w=None, dur=0.55, align="c", off=0.0, hold=None, color=None, hold_dur=0.4):
    """Çapaya bağlı isim/etiket levhası (tablet + oyma yazı). (x,y) levha merkezi. hold=(çıkış çapası) verilirse sonra solar."""
    k = cx.amt(at, dur, off=off)
    if hold is not None:
        k *= 1.0 - cx.amt(hold, hold_dur)
    if k <= 0.003:
        return 0.0
    wd = (w if w is not None else sk.text_width(text, face, size, track) + 76)
    hh = size + 44 + (size * 0.78 if sub else 0)
    xx = x - wd / 2 if align == "c" else x
    yy = y - hh / 2 + (1 - k) * 10
    CM.tablet(f, xx, yy, wd, hh, alpha=k, corner=8)
    CM.ink(f, text, xx + wd / 2, yy + 8 + size * 1.02, face=face, size=size, color=color or TH.fg, align="c", track=track, alpha=k, emboss=False)
    if sub:
        CM.ink(f, sub, xx + wd / 2, yy + 8 + size * 1.02 + size * 0.86, face="cap_i", size=size * 0.74, color=TH.fg2, align="c", alpha=k, emboss=False)
    return k


def stamp_at(f, cx, text, x, y, at, rot=-0.10, size=52, color=None, dur=0.3, off=0.0, hold=None):
    """Damga çarpması — çapa anında vurur; hold çapasında solar."""
    k = cx.amt(at, dur, off=off)
    if k <= 0.003:
        return
    al = 1.0 - (cx.amt(hold, 0.5) if hold is not None else 0.0)
    CM.stamp(f, text, x, y, rot=rot, size=size, color=color, alpha=al, t=k)


def date_plate(f, cx, text, at, x=96, y=860, size=50, hold=None):
    """Sol altta tarih levhası (altyazı bölgesi y≈938–1042 dışında kalır)."""
    k = cx.amt(at, 0.55)
    if hold is not None:
        k *= 1.0 - cx.amt(hold, 0.4)
    if k <= 0.003:
        return
    wd = sk.text_width(text, "title", size, 6) + 76
    CM.tablet(f, x, y - 64 * k, wd, 90, alpha=k, corner=10)
    CM.ink(f, text, x + wd / 2, y - 6 * k, face="title", size=size * 0.80, color=TH.fg, align="c", track=6, alpha=k, emboss=False)


def engr(f, cx, text, x, y, at, size=70, track=10.0, color=None, style="engraved", dur=1.0, face="title", off=0.0, alpha=1.0, glow=0.0, scale=1.0):
    """Çapaya bağlı oyma/yaldız yazı (soldan açılır)."""
    k = cx.amt(at, dur, off=off)
    if k <= 0.003:
        return 0.0
    if style == "gilt":
        sp = CM.gilt(text, face, int(size), float(track))
    else:
        sp = CM.engraved(text, face, int(size), float(track), color or TH.fg)
    CM.draw_spr(f, sp, x, y, "c", alpha=alpha * min(1.0, k * 2.0), reveal=clamp(k * 1.12), glow=glow * k, scale=scale)
    return sp.wid


def breath(cx, a=0.008, hz=0.45, ph=0.0):
    return 1.0 + a * math.sin(cx.t * hz * 6.283 + ph)


def wob(t, hz, amp, ph=0.0):
    return amp * math.sin(t * hz * 6.283 + ph)


def hand_at(f, cx, text, x, y, at, face="fell_i", size=44, color="#2A180D", alpha=1.0, dur=None, seed=0, align="l"):
    """Tüy kalemle satır yazımı (cilt_kinds2.write_line): çapa anında başlar. Dönüş: (yol, kalem_x, kalem_y) ya da None."""
    import cilt_kinds2 as K2
    t0 = cx.at(at)
    return K2.write_line(f, cx, text, x, y, t0, face, size, color, alpha, dur=dur, seed=seed, align=align)


# ───────────────────────────── kamera yardımcıları ─────────────────────────────
def cam_probe(cx, cams, default, t=None):
    """Oda/pano `cams=[(çapa,(x,y,zoom))…]` yolunda t anındaki (camx, camy, z)."""
    t = cx.t if t is None else t
    pc = PN.PanoCam(cx, cams, default, max(cx.dur, 1e-3))
    return pc.at(clamp(t, 0.0, max(cx.dur, 1e-3)))


def world_to_screen(camx, camy, z, x, y, band=(150, 800)):
    """Ana düzlem (x,y) → ekran (cilt_pano.Ctx.to_screen(1.0, x, y) ile aynı)."""
    by0, bh = band
    hc = 800 / 2 + PN.OV
    return W / 2 + (x - camx) * z, by0 + bh / 2 + (y - (hc + camy)) * z


# ───────────────────────────── küçük çizimler ─────────────────────────────
def dashed(c, x0, y0, x1, y1, col="#5A3E22", w=3.0, a=200, on=14.0, off=10.0, phase=0.0):
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, int(a)), StrokeCap=skia.Paint.kRound_Cap)
    p.setPathEffect(skia.DashPathEffect.Make([on, off], phase))
    c.drawLine(x0, y0, x1, y1, p)


def ink_line(c, pts, col="#3A2616", w=2.4, a=220, wob_seed=0, closed=False, jit=0.0):
    p = sk.smooth_path(pts, closed, 0.5)
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, int(a)), StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    if jit:
        pa.setPathEffect(skia.DiscretePathEffect.Make(11.0, jit, wob_seed))
    c.drawPath(p, pa)


def soft_veil(f, color="#0C0905", a=0.4, x=W / 2, y=H / 2, rx=1100, ry=700):
    """Okunurluk için yumuşak koyu elips (tek blit)."""
    c = f.c
    p = skia.Paint(AntiAlias=True)
    sh = skia.GradientShader.MakeRadial((x, y), max(rx, ry), [C(color, int(255 * a)), C(color, 0)], [0, 1])
    p.setShader(sh)
    c.save()
    c.translate(x, y)
    c.scale(1.0, ry / max(rx, 1))
    c.translate(-x, -y)
    c.drawCircle(x, y, rx, p)
    c.restore()


# ───────────────────────────── el yazısı çizgisi (okunmaz satır) ─────────────────────────────
def scribble(c, x0, x1, y, seed=1, col="#3A2616", a=190, amp=3.6, prog=1.0, w=2.1, step=9.0):
    """Okunmaz el yazısı satırı (dalgalı çizgi); prog 0..1 soldan açılır. Dönüş: ucun x'i."""
    n = max(2, int((x1 - x0) / step))
    rs = np.random.RandomState(int(seed) % 100000)
    ys = rs.uniform(-amp, amp, n)
    ys2 = rs.uniform(-amp * 0.35, amp * 0.35, n)
    m = max(0, min(n, int(math.ceil(n * clamp(prog)))))
    if m == 0:
        return x0
    path = skia.Path()
    path.moveTo(x0, y)
    for j in range(m):
        path.quadTo(x0 + j * step + step * 0.5, y + ys[j], x0 + (j + 1) * step, y + ys2[j])
    c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, int(a)), StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join))
    return x0 + m * step


_GRAY = {}


def gray_filter(k=1.0):
    """Gri/soluklaştırma renk filtresi (k=1 tam gri) — ölen/solan nesneler için."""
    key = round(k, 2)
    cf = _GRAY.get(key)
    if cf is None:
        lr, lg, lb = 0.30, 0.59, 0.11
        m = []
        for i in range(3):
            row = [0.0] * 5
            for j, wgt in enumerate((lr, lg, lb)):
                row[j] = wgt * k + (1.0 - k if i == j else 0.0)
            m += row
        m += [0, 0, 0, 1, 0]
        cf = _GRAY[key] = skia.ColorFilters.Matrix(m)
    return cf
