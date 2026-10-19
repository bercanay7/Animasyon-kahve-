"""p5_lib — PARÇA 5 (c10 Rahip ve Kral · c11 Papa Oğulları) ortak çizim/yardımcı işlevleri (Parça 5 sahne yazarı modülü).
Yalnız `scenes_c10.py`, `scenes_c11.py`, `c10_kinds.py`, `c11_kinds.py` kullanır; motor/dünya dosyalarına DOKUNMAZ, onların işlevlerini ÇAĞIRIR.

İçerik
  1) `p5_<tür>` sarmalayıcıları: stok türü AYNEN çağırır, ardından `ovl(cx)` ile üstüne çizer (ekran uzayı; ışıktan SONRA).
     `p5g_<tür>`: aynı, ama gravür (siyah-beyaz sepya) filtresi altında — ANEKDOT/rivayet çekimleri (renk = belge, gravür = rivayet; Parça 2–4 ile aynı sözleşme);
     `acc=` gravürden SONRA renkli vurgu çizer (ör. sinabar şapka).
  2) ovl kurucuları: etiket / levha / damga / tarih plakası / oyma yazı / sayaç / karartma / ışıltı / üstü çizili yazı / fırça yazısı …
  3) özel tür iskeleti (`begin/end`), kamera anahtar karesi (`look`), gravür filtresi (`mono_begin/mono_end`)
  4) SİLÜET MADALYA (`sil_medal`): yüz çizilmez — profil siluet + başlık (kukuleta, kardinal şapkası, tiara, külah …) bronz diskte.
Olgu disiplini: bu modül kendi başına metin üretmez; metinler sahne dosyasından gelir. Şiddet/kan yok.
"""
import functools
import math

import numpy as np
import skia

import cilt_anim as FA
import cilt_cam
import cilt_medici as CM
import cilt_oda as OD
import cilt_pano as PN
import cilt_paper as PP
import icons
import shots as SH
import sk
from cilt_medici import PIG, TH
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth

INK = "#2A1A0C"
INK_S = "#3A2616"
INK_BROWN = "#2A180D"
PAPER_T = (238, 228, 198)
_RS = PN._RS
R, RA, INKP, INKR, LINE, POLY, OVAL, GRAD_V = PN.R, PN.RA, PN.INKP, PN.INKR, PN.LINE, PN.POLY, PN.OVAL, PN.GRAD_V
PT, STK, SOFT, FILLP, RRECT = OD.PT, OD.STK, OD.SOFT, OD.FILLP, OD.RRECT
LIN = CM._LIN


def P(col, a=255, **kw):
    return skia.Paint(AntiAlias=True, Color=C(col, int(a)), **kw)


def S(col, w=1.5, a=255, cap=True):
    return STK(col, w, int(a), cap)


def smooth_pts(pts, close=False, tension=0.5):
    return sk.smooth_path(pts, close, tension)


def look(wx, wy, z=1.0, rot=0.0):
    """Anahtar kare: dünya (wx,wy) noktası ekran merkezinde, zoom z (cam=[(çapa, look(...)), …])."""
    return (z * (wx - W / 2), z * (wy - H / 2), z, rot)


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


# ───────────────────────────── 1) sarmalayıcı türler ─────────────────────────────
_OWN = {"oda", "pano", "sehir", "build", "deniz", "deniz_rota", "deniz_filo", "deniz_kiyi", "liman"}
_BASES = ("oda", "pano", "sehir", "build", "map", "procession", "frieze", "skyline", "ledger", "letter", "doc", "quote", "counter", "stacked", "bars", "network", "tree",
          "timeline", "medal", "medals", "palle", "emblem", "coin", "iconrow", "deniz", "deniz_rota", "deniz_filo", "deniz_kiyi", "liman")


def _wrap(base):
    name = "p5_" + base

    def fn(cx, ovl=None, **kw):
        SH.KINDS[base](cx, **kw)
        if ovl is not None:
            ovl(cx)
    fn.__name__ = "k_" + name
    SH.KINDS[name] = fn
    if base in _OWN or base in cilt_cam.OWN_CAMERA:
        cilt_cam.OWN_CAMERA.add(name)

    gname = "p5g_" + base

    def gfn(cx, ovl=None, mono=1.0, mono_at=None, mono_dur=1.2, acc=None, tone=(1.00, 0.93, 0.80), contrast=1.10, **kw):
        k = mono if mono_at is None else mono * cx.amt(mono_at, mono_dur)
        mono_begin(cx.f, k, tone, contrast)
        SH.KINDS[base](cx, **kw)
        mono_end(cx.f)
        if acc is not None:
            acc(cx)
        if ovl is not None:
            ovl(cx)
    gfn.__name__ = "k_" + gname
    SH.KINDS[gname] = gfn
    if base in _OWN or base in cilt_cam.OWN_CAMERA:
        cilt_cam.OWN_CAMERA.add(gname)


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


def tag(text, x, y, at, size=34, face="title_m", track=6.0, sub=None, w=None, dur=0.55, align="c", off=0.0, out=None, color=None, corner=8, out_dur=0.4):
    """Çapaya bağlı isim/etiket levhası (tablet + yazı). (x,y) levha merkezi."""
    def fn(cx):
        k = _kk(cx, at, dur, out, out_dur, off)
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


def stamp(text, x, y, at, rot=-0.10, size=52, color=None, out=None, dur=0.3, off=0.0, out_dur=0.5):
    """Damga çarpması (0,3 sn)."""
    def fn(cx):
        t = cx.amt(at, dur, off=off)
        if t <= 0:
            return
        al = 1.0 - (cx.amt(out, out_dur) if out is not None else 0.0)
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


def strike(text, x, y, at, strike_at, size=60, face="title_m", track=8.0, color=None, dur=0.5, sdur=0.45, out=None, col_line="#A8321E", align="c"):
    """Yazı `at`'ta belirir; `strike_at`'ta üstüne mürekkep çizgisi çekilir (üstü çizili)."""
    def fn(cx):
        k = _kk(cx, at, dur, out, 0.4)
        if k <= 0.003:
            return
        wd = sk.text_width(text, face, size, track)
        CM.ink(cx.f, text, x, y, face=face, size=size, color=color or TH.fg, align=align, track=track, alpha=k, emboss=False)
        ks = ease_out(clamp((cx.t - cx.at(strike_at)) / sdur), 2.0) * k
        if ks > 0.005:
            x0 = x - wd / 2 if align == "c" else x
            p = cx.f.paint(col_line, style="stroke", sw=7.0, alpha=0.92 * ks)
            CM.wobble(p, 9.0, 1.4, 5)
            cx.f.c.drawLine(x0 - 10, y - size * 0.30, x0 - 10 + (wd + 20) * ks, y - size * 0.36, p)
    return fn


@functools.lru_cache(maxsize=32)
def _painted(text, face, size, track, color, rough, seed):
    return CM.painted(text, face, size, track, color, rough, seed)


def brush(text, x, y, at, size=120, track=10.0, color="#A8321E", dur=1.3, face="title", rough=1.5, seed=7, out=None, alpha=1.0, rot=0.0):
    """Fırça yazısı (boyalı sprite, soldan açılır) — duvara yazılmış slogan."""
    def fn(cx):
        k = cx.amt(at, dur)
        if k <= 0.003:
            return
        al = alpha * (1.0 - (cx.amt(out, 0.6) if out is not None else 0.0))
        if al <= 0.01:
            return
        sp = _painted(text, face, int(size), float(track), color, rough, seed)
        if rot:
            cx.f.c.save()
            cx.f.c.translate(x, y)
            cx.f.c.rotate(math.degrees(rot))
            CM.draw_spr(cx.f, sp, 0, 0, "c", alpha=al * min(1.0, k * 2.0), reveal=clamp(k * 1.1))
            cx.f.c.restore()
        else:
            CM.draw_spr(cx.f, sp, x, y, "c", alpha=al * min(1.0, k * 2.0), reveal=clamp(k * 1.1))
    return fn


# ───────────────────────────── 3) özel tür iskeleti ─────────────────────────────
def begin(cx, bg="wall", seed=0, dress=None, push=0.0, drift=(0.0, 0.0), clear="#0B0A08", mono=0.0):
    """Özel tür iskeleti: arka plan (duvar/siyah) + kamera dönüşü. mono>0 → gravür katmanı açılır (duvar dâhil). Dönüş: (f, c, cam)."""
    f = cx.f
    cam = CM.Cam(cx, push=push, drift=drift)
    if mono > 0.001:
        mono_begin(f, mono)
    if bg == "wall":
        CM.bgfill(f, cx, seed=seed, cam=cam, dress=dress)
    else:
        f.clear(clear)
    cam.begin(f)
    return f, f.c, cam


def end(cx, cam, mono=0.0, motes_n=26, light=None, vig_s=None, dust=True):
    cam.end(cx.f)
    CM.finish(cx.f, cx, motes_n=motes_n, light=light, vig_s=vig_s, dust=dust)
    if mono > 0.001:
        mono_end(cx.f)


def breath(cx, a=0.008, hz=0.45, ph=0.0):
    return 1.0 + a * math.sin(cx.t * hz * 6.283 + ph)


def wob(t, hz, amp, ph=0.0):
    return amp * math.sin(t * hz * 6.283 + ph)


def hand_at(f, cx, text, x, y, at, face="fell_i", size=44, color=INK_BROWN, alpha=1.0, dur=None, seed=0, align="l"):
    """Tüy kalemle satır yazımı (cilt_kinds2.write_line): çapa anında başlar. Dönüş: (ilerleme, kalem_x, kalem_y)."""
    import cilt_kinds2 as K2
    return K2.write_line(f, cx, text, x, y, cx.at(at), face, size, color, alpha, dur=dur, seed=seed, align=align)


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


# ───────────────────────────── 4) SİLÜET MADALYA (yüz çizilmez) ─────────────────────────────
sk.METAL.setdefault("lead", [("#2A2C32", 0.0), ("#5C6068", 0.24), ("#A6AAB2", 0.52), ("#6A6E76", 0.76), ("#2A2C32", 1.0)])

# başlık kataloğu: ad → (renk, açıklama). Çizim `_gear` içinde.
HEAD_COLORS = dict(galero="#A8321E", camauro="#A8321E", tiara="#D6AE4A", mitre="#E8DDB8", hood="#15100C", cap="#2E2418", berretto="#6E1A22",
                   beret="#2A3A78", helm="#6A6E76", laurel="#6E8A4A", bare=None)

_PROFILE = [(-0.44, -0.10), (-0.40, -0.38), (-0.20, -0.56), (0.06, -0.60), (0.28, -0.48), (0.40, -0.30), (0.425, -0.16), (0.415, -0.08),
            (0.54, 0.06), (0.47, 0.11), (0.455, 0.17), (0.47, 0.22), (0.445, 0.27), (0.435, 0.36), (0.34, 0.47), (0.14, 0.45)]
_NECK_BODY = [(0.12, 0.54), (0.15, 0.90), (0.62, 1.12), (0.66, 1.55), (-0.78, 1.55), (-0.70, 1.12), (-0.24, 0.88), (-0.30, 0.46), (-0.38, 0.30)]


def _head_pts(nose=1.0, chin=1.0, neck=1.0):
    pts = []
    for (x, y) in _PROFILE:
        if 0.50 > x > 0.40 and -0.10 < y < 0.30:       # burun / dudak / çene bölgesi: oranlanır
            x = 0.41 + (x - 0.41) * (nose if y < 0.12 else 1.0)
        if y > 0.30:
            x = x * chin if x > 0.2 else x
        pts.append((x, y))
    for (x, y) in _NECK_BODY:
        pts.append((x * (neck if abs(x) < 0.3 else 1.0), y))
    return pts


def _hat_paths(kind, s, beard_k=0.0):
    """Başlık parçaları: [(path, fill, stroke_a)] — yerel birim (baş yarıçapı≈0.5 → s px)."""
    out = []
    if kind == "galero":                                        # kardinal: geniş yassı kenar + sığ tepe + her iki yanda püskül
        brim = skia.Path()
        brim.addOval(skia.Rect.MakeLTRB(-0.72 * s, -0.70 * s, 0.80 * s, -0.46 * s))
        crown = skia.Path()
        crown.moveTo(-0.34 * s, -0.55 * s)
        crown.quadTo(-0.30 * s, -0.86 * s, 0.04 * s, -0.88 * s)
        crown.quadTo(0.34 * s, -0.86 * s, 0.40 * s, -0.55 * s)
        crown.close()
        out += [(brim, HEAD_COLORS["galero"], 0.9), (crown, HEAD_COLORS["galero"], 0.9)]
        for sx in (-0.62, 0.70):
            for j in range(4):
                tp = skia.Path()
                tp.addCircle(sx * s + (j % 2) * 0.05 * s, (-0.46 + j * 0.115) * s + 0.06 * s, 0.045 * s)
                out.append((tp, HEAD_COLORS["galero"], 0.8))
    elif kind == "camauro":                                     # kapalı kalpak (kırmızı) + beyaz kürk kenar
        cap = skia.Path()
        cap.moveTo(-0.46 * s, -0.04 * s)
        cap.quadTo(-0.50 * s, -0.66 * s, -0.04 * s, -0.70 * s)
        cap.quadTo(0.34 * s, -0.68 * s, 0.42 * s, -0.30 * s)
        cap.lineTo(0.40 * s, -0.22 * s)
        cap.quadTo(0.10 * s, -0.34 * s, -0.20 * s, -0.20 * s)
        cap.lineTo(-0.34 * s, 0.12 * s)
        cap.close()
        fur = skia.Path()
        fur.moveTo(0.42 * s, -0.30 * s)
        fur.quadTo(0.10 * s, -0.40 * s, -0.20 * s, -0.24 * s)
        fur.lineTo(-0.34 * s, 0.10 * s)
        fur.lineTo(-0.44 * s, 0.00 * s)
        fur.quadTo(-0.20 * s, -0.34 * s, 0.10 * s, -0.46 * s)
        fur.quadTo(0.34 * s, -0.42 * s, 0.46 * s, -0.30 * s)
        fur.close()
        out += [(cap, HEAD_COLORS["camauro"], 0.9), (fur, "#EFE6D2", 0.9)]
    elif kind == "tiara":                                       # üç katlı konik taç
        for i, (w0, w1, y0, y1, col) in enumerate(((0.42, 0.34, -0.50, -0.78, "#C9A23C"), (0.34, 0.25, -0.78, -1.02, "#D6AE4A"), (0.25, 0.14, -1.02, -1.24, "#E3BE5E"))):
            tp = skia.Path()
            tp.moveTo(-w0 * s * 0.9 + 0.02 * s, y0 * s)
            tp.lineTo(w0 * s * 0.9 + 0.02 * s, y0 * s)
            tp.lineTo(w1 * s * 0.9 + 0.02 * s, y1 * s)
            tp.lineTo(-w1 * s * 0.9 + 0.02 * s, y1 * s)
            tp.close()
            out.append((tp, col, 1.0))
            band = skia.Path()
            band.addRect(skia.Rect.MakeLTRB((-w1 * 0.9 + 0.02) * s, (y1 - 0.045) * s, (w1 * 0.9 + 0.02) * s, (y1 + 0.02) * s))
            out.append((band, "#7A5418", 0.7))
        gl = skia.Path()
        gl.addCircle(0.02 * s, -1.30 * s, 0.065 * s)
        out.append((gl, "#EBCB6E", 1.0))
        cr = skia.Path()
        cr.addRect(skia.Rect.MakeLTRB(0.005 * s, -1.50 * s, 0.035 * s, -1.34 * s))
        cr.addRect(skia.Rect.MakeLTRB(-0.04 * s, -1.45 * s, 0.08 * s, -1.42 * s))
        out.append((cr, "#EBCB6E", 1.0))
    elif kind == "mitre":                                       # piskopos külahı (iki dilimli)
        mp = skia.Path()
        mp.moveTo(-0.34 * s, -0.46 * s)
        mp.lineTo(0.38 * s, -0.46 * s)
        mp.lineTo(0.30 * s, -0.96 * s)
        mp.quadTo(0.02 * s, -1.20 * s, -0.26 * s, -0.96 * s)
        mp.close()
        out.append((mp, "#E9DDB4", 1.0))
        bp = skia.Path()
        bp.addRect(skia.Rect.MakeLTRB(-0.34 * s, -0.54 * s, 0.38 * s, -0.46 * s))
        out.append((bp, "#C9A23C", 0.9))
        cp = skia.Path()
        cp.addRect(skia.Rect.MakeLTRB(0.00 * s, -1.02 * s, 0.05 * s, -0.54 * s))
        out.append((cp, "#C9A23C", 0.8))
    elif kind == "berretto":                                    # yassı Floransa/dük kalpağı (kenarı kıvrık)
        bp = skia.Path()
        bp.moveTo(-0.46 * s, -0.40 * s)
        bp.quadTo(-0.40 * s, -0.76 * s, 0.00 * s, -0.78 * s)
        bp.quadTo(0.42 * s, -0.76 * s, 0.50 * s, -0.42 * s)
        bp.quadTo(0.10 * s, -0.34 * s, -0.46 * s, -0.40 * s)
        bp.close()
        out.append((bp, HEAD_COLORS["berretto"], 0.9))
        rim = skia.Path()
        rim.moveTo(-0.46 * s, -0.40 * s)
        rim.quadTo(0.10 * s, -0.34 * s, 0.50 * s, -0.42 * s)
        out.append((rim, "#C9A23C", -1.0))
    elif kind == "cap":                                         # düz yuvarlak kalpak
        bp = skia.Path()
        bp.moveTo(-0.44 * s, -0.34 * s)
        bp.quadTo(-0.42 * s, -0.72 * s, -0.02 * s, -0.72 * s)
        bp.quadTo(0.40 * s, -0.70 * s, 0.44 * s, -0.36 * s)
        bp.close()
        out.append((bp, HEAD_COLORS["cap"], 0.9))
    elif kind == "beret":                                       # tüylü bere
        bp = skia.Path()
        bp.moveTo(-0.50 * s, -0.36 * s)
        bp.quadTo(-0.46 * s, -0.78 * s, 0.04 * s, -0.78 * s)
        bp.quadTo(0.52 * s, -0.74 * s, 0.56 * s, -0.40 * s)
        bp.quadTo(0.06 * s, -0.30 * s, -0.50 * s, -0.36 * s)
        bp.close()
        out.append((bp, HEAD_COLORS["beret"], 0.9))
        fe = skia.Path()
        fe.moveTo(-0.28 * s, -0.70 * s)
        fe.quadTo(-0.60 * s, -1.00 * s, -0.78 * s, -0.62 * s)
        fe.quadTo(-0.52 * s, -0.80 * s, -0.22 * s, -0.66 * s)
        fe.close()
        out.append((fe, "#E8DCB4", 0.8))
    elif kind == "helm":                                        # miğfer (morion)
        hp = skia.Path()
        hp.moveTo(-0.46 * s, -0.20 * s)
        hp.quadTo(-0.50 * s, -0.72 * s, 0.02 * s, -0.74 * s)
        hp.quadTo(0.46 * s, -0.70 * s, 0.50 * s, -0.24 * s)
        hp.lineTo(0.62 * s, -0.20 * s)
        hp.lineTo(0.50 * s, -0.14 * s)
        hp.lineTo(-0.40 * s, -0.10 * s)
        hp.close()
        out.append((hp, "#7C8088", 1.0))
        cr = skia.Path()
        cr.moveTo(-0.30 * s, -0.66 * s)
        cr.quadTo(0.02 * s, -1.02 * s, 0.38 * s, -0.62 * s)
        cr.lineTo(0.30 * s, -0.62 * s)
        cr.quadTo(0.02 * s, -0.84 * s, -0.22 * s, -0.62 * s)
        cr.close()
        out.append((cr, "#8E9096", 0.9))
    elif kind == "laurel":                                      # defne çelengi (yaprak sırası)
        for i in range(9):
            a = -2.9 + i * 0.36
            lx, ly = 0.02 * s + math.cos(a) * 0.50 * s, -0.12 * s + math.sin(a) * 0.52 * s
            lp = skia.Path()
            lp.addOval(skia.Rect.MakeLTRB(lx - 0.10 * s, ly - 0.045 * s, lx + 0.10 * s, ly + 0.045 * s))
            out.append(("rot", (lp, a + 1.57, lx, ly), HEAD_COLORS["laurel"], 0.8))
    return out


def _hood_path(s):
    """Kukuleta: kafayı örten, sivri tepeli, omuzlara dökülen tek koyu kütle (başın dışına taşar)."""
    p = skia.Path()
    p.moveTo(0.68 * s, 1.12 * s)                  # ön omuz
    p.quadTo(0.46 * s, 0.72 * s, 0.46 * s, 0.34 * s)   # çene önü (kukuleta kenarı)
    p.quadTo(0.64 * s, 0.00 * s, 0.56 * s, -0.20 * s)  # yüz önü
    p.quadTo(0.50 * s, -0.62 * s, 0.00 * s, -0.84 * s) # alın üstü → tepe
    p.quadTo(-0.30 * s, -1.02 * s, -0.46 * s, -0.78 * s)   # sivri tepe (geri kıvrık)
    p.quadTo(-0.78 * s, -0.50 * s, -0.74 * s, 0.00 * s)
    p.quadTo(-0.86 * s, 0.60 * s, -0.96 * s, 1.20 * s)
    p.lineTo(0.68 * s, 1.12 * s)
    p.close()
    return p


def _beard_path(s, k):
    p = skia.Path()
    p.moveTo(0.30 * s, 0.30 * s)
    p.quadTo(0.52 * s, 0.40 * s + 0.20 * s * k, 0.30 * s, 0.50 * s + 0.62 * s * k)
    p.quadTo(0.14 * s, 0.50 * s + 0.76 * s * k, 0.06 * s, 0.44 * s + 0.20 * s * k)
    p.quadTo(0.04 * s, 0.36 * s, 0.14 * s, 0.34 * s)
    p.close()
    return p


@functools.lru_cache(maxsize=64)
def _field_img(R_px, tint):
    """Madalya tabanı: bronz disk (halka + iç alan), önceden pişmiş (RGBA)."""
    n = int(R_px * 2 + 8)
    fr = sk.Frame(n, n)
    fr.clear(skia.ColorTRANSPARENT)
    cc = n / 2.0
    c = fr.c
    ramp = [("#3B220F", 0.0), ("#8A5A2C", 0.18), ("#D9A868", 0.44), ("#8A5A2C", 0.72), ("#33200F", 1.0)]
    if tint == "lead":
        ramp = sk.METAL["lead"]
    elif tint == "gold":
        ramp = [("#4F3510", 0.0), ("#A87C28", 0.22), ("#F0D480", 0.48), ("#B98A2E", 0.74), ("#4F3510", 1.0)]
    elif tint == "lapis":
        ramp = [("#0B1236", 0.0), ("#1E3680", 0.30), ("#6C90DA", 0.52), ("#1E3680", 0.80), ("#0B1236", 1.0)]
    c.drawCircle(cc + 5, cc + 9, R_px, skia.Paint(AntiAlias=True, Color=C("#000000", 120), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 9)))
    sh = skia.GradientShader.MakeLinear([(cc - R_px * 0.7, cc - R_px * 0.8), (cc + R_px * 0.8, cc + R_px * 0.8)], [C(col) for col, _ in ramp], [p for _, p in ramp])
    c.drawCircle(cc, cc, R_px, skia.Paint(AntiAlias=True, Shader=sh))
    c.drawCircle(cc, cc, R_px, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0, Color=C("#1A0F06", 200)))
    for q in range(48):                                           # boncuk halka
        a = q * 2 * math.pi / 48
        c.drawCircle(cc + math.cos(a) * R_px * 0.93, cc + math.sin(a) * R_px * 0.93, R_px * 0.014, skia.Paint(AntiAlias=True, Color=C("#F2D9A4", 150)))
    fld = skia.GradientShader.MakeRadial((cc - R_px * 0.25, cc - R_px * 0.3), R_px * 1.0, [C("#6A4526"), C("#3C2312"), C("#24150A")], [0.0, 0.65, 1.0])
    if tint == "lapis":
        fld = skia.GradientShader.MakeRadial((cc - R_px * 0.25, cc - R_px * 0.3), R_px * 1.0, [C("#223C86"), C("#142566"), C("#0A1440")], [0.0, 0.65, 1.0])
    c.drawCircle(cc, cc, R_px * 0.84, skia.Paint(AntiAlias=True, Shader=fld))
    c.drawCircle(cc, cc, R_px * 0.84, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6, Color=C("#E6C58A", 150)))
    c.drawCircle(cc, cc, R_px * 0.84 - 2.5, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C("#10090A", 190)))
    return fr.surf.makeImageSnapshot()


_HAT_FIT = dict(hood=(0.70, 0.20), galero=(0.72, 0.26), tiara=(0.56, 0.36), camauro=(0.76, 0.16), mitre=(0.62, 0.34), berretto=(0.76, 0.16), cap=(0.76, 0.16),
                beret=(0.72, 0.20), helm=(0.70, 0.22), laurel=(0.76, 0.14), bare=(0.78, 0.12))


def sil_medal(f, x, y, R_px, hat="bare", alpha=1.0, tilt=0.0, flip=False, beard=0.0, nose=1.0, chin=1.0, neck=1.0, tint="bronze", glint_k=None,
              body="#120A06", rim_col="#E8B878", hat_k=1.0, scale_in=1.0, shadow=True):
    """SİLÜET MADALYA — yüz çizilmez: bronz diskte düz koyu profil + başlık (hat: hood | galero | camauro | tiara | mitre | berretto | cap | beret | helm | laurel | bare).
    (x,y) disk merkezi, R_px yarıçap; tilt radyan (hafif sallanma); flip: sola bakar; beard: 0..1 sakal uzunluğu; hat_k: başlığın belirme oranı (0..1)."""
    if alpha <= 0.003:
        return
    c = f.c
    img = _field_img(int(R_px), tint)
    c.save()
    c.translate(x, y)
    if tilt:
        c.rotate(math.degrees(tilt))
    sc = scale_in
    c.scale(sc, sc)
    p = skia.Paint(AntiAlias=True)
    if alpha < 1.0:
        p.setAlphaf(clamp(alpha))
    c.drawImage(img, -img.width() / 2, -img.height() / 2, LIN, p)
    # içerik: disk iç alanına kırpılı
    clip = skia.Path()
    clip.addCircle(0, 0, R_px * 0.835)
    c.save()
    c.clipPath(clip, skia.ClipOp.kIntersect, True)
    hs_, hdy = _HAT_FIT.get(hat, (0.76, 0.14))
    s = R_px * hs_                                                # birim → px (baş yarıçapı ≈ 0.5 birim)
    c.translate(-R_px * 0.04 * (-1 if flip else 1), R_px * hdy)
    if flip:
        c.scale(-1, 1)
    pts = _head_pts(nose, chin, neck)
    spts = [(px * s, py * s) for px, py in pts]
    sil = sk.smooth_path(spts, True, 0.42)
    pa = clamp(alpha)
    if hat == "hood":
        hp = _hood_path(s)
        c.drawPath(hp, skia.Paint(AntiAlias=True, Color=C(body, int(255 * pa))))
        # kukuletanın iç boşluğu: baş siluetinin biraz daha açık kahvesi (kukuleta/yüz ayrımı; yüz ayrıntısı YOK)
        c.drawPath(sil, skia.Paint(AntiAlias=True, Color=C("#2A190D", int(235 * pa))))
        c.drawPath(sil, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(2.0, R_px * 0.02), Color=C("#000000", int(210 * pa))))
        fold = skia.Path()
        for q in range(3):
            fold.moveTo((-0.55 + q * 0.16) * s, 0.55 * s)
            fold.quadTo((-0.60 + q * 0.18) * s, 0.9 * s, (-0.72 + q * 0.2) * s, 1.3 * s)
        c.drawPath(fold, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.4, R_px * 0.012), Color=C("#3A2414", int(160 * pa))))
    else:
        c.drawPath(sil, skia.Paint(AntiAlias=True, Color=C(body, int(255 * pa))))
        if beard > 0.003:
            c.drawPath(_beard_path(s, beard), skia.Paint(AntiAlias=True, Color=C(body, int(255 * pa))))
    # kenar ışığı: sol-üstten gelen sıcak çizgi (degradeli kontur)
    rim = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.6, R_px * 0.014))
    rim.setShader(skia.GradientShader.MakeLinear([(-0.6 * s, -0.9 * s), (0.7 * s, 0.4 * s)], [C(rim_col, int(230 * pa)), C(rim_col, 0)], [0.0, 0.7]))
    c.drawPath(_hood_path(s) if hat == "hood" else sil, rim)
    if hat not in ("hood", "bare") and hat_k > 0.003:
        hs = s
        c.save()
        dy = (1.0 - ease_out(hat_k)) * -0.55 * hs                  # şapka yukarıdan konar
        c.translate(0, dy)
        for item in _hat_paths(hat, hs):
            if item[0] == "rot":
                _, (lp, ang, lx, ly), col, sa = item
                c.save()
                c.translate(lx, ly)
                c.rotate(math.degrees(ang))
                c.translate(-lx, -ly)
                c.drawPath(lp, skia.Paint(AntiAlias=True, Color=C(col, int(255 * pa * hat_k))))
                c.restore()
                continue
            path, col, sa = item
            if sa < 0:
                c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(2.0, R_px * 0.02), Color=C(col, int(255 * pa * hat_k))))
                continue
            c.drawPath(path, skia.Paint(AntiAlias=True, Color=C(col, int(255 * pa * hat_k))))
            c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.4, R_px * 0.010), Color=C("#1A0F06", int(210 * pa * hat_k * sa))))
        c.restore()
    c.restore()
    if glint_k is not None and 0.0 < glint_k < 1.0:                  # yaldız ışıltısı: diske çapraz parlama
        a = math.sin(glint_k * math.pi)
        gx = -R_px * 0.9 + glint_k * R_px * 1.8
        gp = skia.Paint(AntiAlias=True)
        gp.setShader(skia.GradientShader.MakeLinear([(gx - R_px * 0.18, gx - R_px * 0.18), (gx + R_px * 0.18, gx + R_px * 0.18)],
                                                    [C("#FFF4D0", 0), C("#FFF4D0", int(150 * a)), C("#FFF4D0", 0)], [0.0, 0.5, 1.0]))
        gc = skia.Path()
        gc.addCircle(0, 0, R_px * 0.83)
        c.save()
        c.clipPath(gc, skia.ClipOp.kIntersect, True)
        c.drawRect(skia.Rect.MakeLTRB(-R_px, -R_px, R_px, R_px), gp)
        c.restore()
    c.restore()


# ───────────────────────────── dünya-uzaylı bindirmeler (oda/pano/sehir `after=` kancası: ctx.to_screen) ─────────────────────────────
def after_ov(*items):
    """oda/pano/sehir türlerinin `after=` kancası: item(ctx) → ctx dünya bağlamı (ctx.cx = çekim bağlamı, ctx.to_screen(fct, x, y))."""
    items = [i for i in items if i]

    def fn(ctx):
        for it in items:
            it(ctx)
    return fn


def wtag(text, wx, wy, at, fct=1.0, dx=0.0, dy=0.0, **kw):
    """Dünya noktasına (wx,wy) bağlı isim levhası (kamera hareket ederken noktayı izler)."""
    def fn(ctx):
        sx, sy = ctx.to_screen(fct, wx, wy)
        tag(text, sx + dx, sy + dy, at, **kw)(ctx.cx)
    return fn


def wstamp(text, wx, wy, at, fct=1.0, dx=0.0, dy=0.0, **kw):
    def fn(ctx):
        sx, sy = ctx.to_screen(fct, wx, wy)
        stamp(text, sx + dx, sy + dy, at, **kw)(ctx.cx)
    return fn


def wfn(draw, fct=1.0):
    """Serbest çizim: draw(ctx, to_screen) — ekran uzayında çizer."""
    def fn(ctx):
        draw(ctx, lambda x, y: ctx.to_screen(fct, x, y))
    return fn


# ───────────────────────────── mektup sayfası (okunmaz satırlar kendini yazar; tüy kalem) ─────────────────────────────
def draw_letter(f, cx, x, y, w, h, at, rot=-0.04, n=9, dur=6.0, seed=3, k=1.0, scale=1.0, alpha=1.0, off=0.5, quill=True, ghosts=(), tone=PAPER_T, line_seed=None, pad_x=64, top=108, gap=52):
    """Kâğıt sayfa + `at` çapasından itibaren `dur` sn boyunca n okunmaz satır sırayla yazılır (tüy kalem uçta). ghosts: [dict(text, dy, at, out, size, x)] — kenar boşluğuna
    soluk mürekkep işaretleri (ör. «I II III»); yazılmaz, belirir ve çapaya göre solar (mektupta YOK olanı göstermek için). (x,y) sayfa merkezi."""
    if k <= 0.003:
        return
    pp = PP.paper_image(int(w), int(h), seed, tone, "deckle", (("h", 0.5),), 44, 1.0)
    c = f.c
    yy = y + (1.0 - ease_out(k)) * 70
    pp.draw(f, x, yy, rot=rot, scale=scale * (0.96 + 0.04 * ease_out(k)), alpha=alpha * k, shadow=0.6)
    t0 = cx.at(at) + off
    c.save()
    c.translate(x, yy)
    c.rotate(math.degrees(rot))
    c.scale(scale, scale)
    x0, x1 = -w / 2 + pad_x, w / 2 - pad_x
    qpos = None
    dt = dur / max(1, n)
    for i in range(n):
        ly = -h / 2 + top + i * gap
        prog = clamp((cx.t - (t0 + i * dt)) / max(0.2, dt * 0.95))
        if prog <= 0:
            continue
        xe = x1 - (i % 3 == 2) * 150 * (0.6 + 0.4 * ((seed + i) % 3) / 2)
        endx = scribble(c, x0, xe, ly, seed=(line_seed or seed) * 31 + i, col="#2A180D", a=int(200 * alpha * k), amp=3.4, prog=ease_io(prog, 1.3), w=2.2)
        if 0.0 < prog < 1.0:
            qpos = (endx, ly)
    for gd in ghosts:
        ga = cx.amt(gd["at"], 0.7)
        if gd.get("out") is not None:
            ga *= 1.0 - cx.amt(gd["out"], 0.9)
        if ga > 0.01:
            fs = gd.get("size", 54)
            gx = gd.get("x", w / 2 - 90)
            gy = -h / 2 + top + gd.get("dy", 0.0)
            wob_ = math.sin(cx.t * 1.3 + gd.get("dy", 0.0)) * 1.5
            CM.ink(f, gd["text"], gx, gy + wob_, face="fell_i", size=fs, color="#6A4E38", align="c", alpha=0.55 * ga * alpha, emboss=False)
    c.restore()
    if quill and qpos is not None and alpha * k > 0.2:
        ca, sa = math.cos(rot), math.sin(rot)
        qx = x + (qpos[0] * ca - qpos[1] * sa) * scale
        qy = yy + (qpos[0] * sa + qpos[1] * ca) * scale
        import cilt_kinds2 as K2
        K2.draw_quill(f, qx + 4, qy + math.sin(cx.t * 9.0) * 1.5, ang=-56.0, alpha=1.0, scale=0.9)


def letter_ovl(x, y, w, h, at, out=None, **kw):
    """Ekran-uzayı mektup sayfası bindirmesi (oda/map vb. çekimlerin üstünde kayarak girer)."""
    def fn(cx):
        k = cx.amt(at, 0.8)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.6)
        draw_letter(cx.f, cx, x, y, w, h, at, k=k, **kw)
    return fn


def walk_x(cx, x0, x1, speed, at):
    """oda/sehir `actors` walk=(x1, hız), walk_at=at ile aynı yürüyüş eğrisi: t anındaki x (etiketi figüre bağlamak için)."""
    w0 = cx.at(at)
    dist = x1 - x0
    u = clamp((cx.t - w0) * abs(speed) / max(1.0, abs(dist)))
    return x0 + dist * u


def wtagf(text, fx, wy, at, fct=1.0, dx=0.0, dy=0.0, **kw):
    """Hareketli dünya noktasına bağlı levha: fx(cx) → x (ör. yürüyen figür)."""
    def fn(ctx):
        sx, sy = ctx.to_screen(fct, fx(ctx.cx), wy)
        tag(text, sx + dx, sy + dy, at, **kw)(ctx.cx)
    return fn


def tick(x, y, at, s=34.0, col="#A8321E", dur=0.45, w=7.0, out=None):
    """Elle çizilmiş onay işareti (✓): çapada çizilmeye başlar."""
    def fn(cx):
        k = clamp((cx.t - cx.at(at)) / dur)
        if out is not None:
            k2 = 1.0 - cx.amt(out, 0.5)
        else:
            k2 = 1.0
        if k <= 0.003 or k2 <= 0.01:
            return
        pts = [(x - 0.55 * s, y + 0.05 * s), (x - 0.15 * s, y + 0.50 * s), (x + 0.62 * s, y - 0.60 * s)]
        L1 = math.hypot(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1])
        L2 = math.hypot(pts[2][0] - pts[1][0], pts[2][1] - pts[1][1])
        d = ease_io(k) * (L1 + L2)
        p = skia.Path()
        p.moveTo(*pts[0])
        if d <= L1:
            u = d / L1
            p.lineTo(pts[0][0] + (pts[1][0] - pts[0][0]) * u, pts[0][1] + (pts[1][1] - pts[0][1]) * u)
        else:
            p.lineTo(*pts[1])
            u = (d - L1) / L2
            p.lineTo(pts[1][0] + (pts[2][0] - pts[1][0]) * u, pts[1][1] + (pts[2][1] - pts[1][1]) * u)
        pa = cx.f.paint(col, style="stroke", sw=w, alpha=0.95 * k2, cap="round", join="round")
        CM.wobble(pa, 8.0, 1.0, 3)
        cx.f.c.drawPath(p, pa)
    return fn


class PanoProbe:
    """pano/oda/sehir dünya kamerasının kare anındaki dönüşümü: x,y (dünya) → ekran. (cilt_pano.Ctx.to_screen ile aynı formül)"""

    def __init__(self, cx, cams, default, band=(150, 800)):
        self.cx = cx
        self.pc = PN.PanoCam(cx, cams, default, max(cx.dur, 1e-3))
        self.band = band

    def to_screen(self, x, y, fct=1.0, t=None):
        cx = self.cx
        tt = clamp(cx.t if t is None else t, 0.0, max(cx.dur, 1e-3))
        camx, camy, z = self.pc.at(tt)
        by0, bh = self.band
        hc = 800 / 2 + PN.OV
        Cx = W / 2 + (camx - W / 2) * fct
        Cy = hc + camy * fct
        return W / 2 + (x - Cx) * z, by0 + bh / 2 + (y - Cy) * z, z


# ───────────────────────────── harita `extra=` parçaları (cm.ll: boylam/enlem → ekran; mv.point_on: rota üstü nokta) ─────────────────────────────
def map_extra(*parts):
    parts = [p for p in parts if p]

    def fn(cx, cm, mv):
        for p in parts:
            p(cx, cm, mv)
    return fn


def mm_medal(route, at, dur=3.0, R_px=70, hat="bare", flip=False, alpha_in=0.6, hold=True, out=None, **kw):
    """Rota üstünde ilerleyen SİLÜET MADALYA (kişi işareti). route=[(lon,lat),…]; at: hareket başlangıcı; dur: sn; out: solma çapası."""
    def fn(cx, cm, mv):
        k = cx.amt(at, alpha_in, off=-0.5)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.6)
        if k <= 0.003:
            return
        pr = ease_io(clamp((cx.t - cx.at(at)) / dur))
        (x, y), ang = mv.point_on(cm, route, pr)
        sil_medal(cx.f, x, y - R_px * 0.2 + math.sin(cx.t * 2.0) * 2.0, R_px * (0.85 + 0.15 * ease_out(k)), hat=hat, alpha=k, flip=flip, tilt=0.03 * math.sin(cx.t * 1.5), **kw)
    return fn


def mm_icons(pts, kind, at, size=80, metal="gold", stagger=0.18, out=None, alpha=1.0, bob=0.0):
    """Haritada noktalara simgeler (sırayla belirir)."""
    def fn(cx, cm, mv):
        for i, (lon, lat) in enumerate(pts):
            k = cx.amt(at, 0.5, off=i * stagger)
            if out is not None:
                k *= 1.0 - cx.amt(out, 0.5)
            if k <= 0.003:
                continue
            x, y = cm.ll(lon, lat)
            icons.draw_icon(cx.f, kind, x, y + math.sin(cx.t * 2.0 + i) * bob, size=size * (0.8 + 0.2 * ease_out(k)), metal=metal, alpha=k * alpha)
    return fn


def mm_flip_icons(pts, kind, at_in, at_flip, metal_a, metal_b, size=88, stagger=0.15, flip_stagger=0.12):
    """Simgeler `at_in`'de belirir; `at_flip`'te metal_a → metal_b rengine döner (ör. Floransa kırmızısı → zambak mavisi)."""
    def fn(cx, cm, mv):
        for i, (lon, lat) in enumerate(pts):
            ki = cx.amt(at_in, 0.5, off=i * stagger)
            if ki <= 0.003:
                continue
            kf = ease_io(clamp((cx.t - cx.at(at_flip) - i * flip_stagger) / 0.8))
            x, y = cm.ll(lon, lat)
            sz = size * (0.8 + 0.2 * ease_out(ki)) * (1.0 + 0.18 * math.sin(kf * math.pi))
            icons.draw_icon(cx.f, kind, x, y, size=sz, metal=metal_a, alpha=ki * (1.0 - kf))
            if kf > 0.01:
                icons.draw_icon(cx.f, kind, x, y, size=sz, metal=metal_b, alpha=ki * kf)
    return fn


class WOv:
    """Dünya-uzaylı bindirme kurucusu (stok oda/pano/sehir çekimleri `after=` kancası taşımaz): AYNI `cams` ile kamera dönüşümünü yeniden kurar
    (PanoProbe) ve ekran-uzayı levha/damga/çizimleri dünya noktalarına bağlar. Kural: çekimde `cams` AÇIKÇA verilmeli."""

    def __init__(self, cams, band=(150, 800), default=None):
        self.cams, self.band, self.default = cams, band, default

    def at(self, cx, x, y, fct=1.0):
        pr = PanoProbe(cx, self.cams, self.default, self.band)
        return pr.to_screen(x, y, fct)

    def tag(self, text, x, y, at, fct=1.0, dx=0.0, dy=0.0, **kw):
        def fn(cx):
            sx, sy, z = self.at(cx, x, y, fct)
            tag(text, sx + dx, sy + dy, at, **kw)(cx)
        return fn

    def tagf(self, text, fx, y, at, fct=1.0, dx=0.0, dy=0.0, **kw):
        def fn(cx):
            sx, sy, z = self.at(cx, fx(cx), y, fct)
            tag(text, sx + dx, sy + dy, at, **kw)(cx)
        return fn

    def stamp(self, text, x, y, at, fct=1.0, dx=0.0, dy=0.0, **kw):
        def fn(cx):
            sx, sy, z = self.at(cx, x, y, fct)
            stamp(text, sx + dx, sy + dy, at, **kw)(cx)
        return fn

    def draw(self, fn_draw, x, y, fct=1.0):
        """fn_draw(cx, sx, sy, z) — (x,y) dünya noktasının ekran konumunda serbest çizim."""
        def fn(cx):
            sx, sy, z = self.at(cx, x, y, fct)
            fn_draw(cx, sx, sy, z)
        return fn


def mm_tag(lon, lat, text, at, strike_at=None, size=30, dx=0.0, dy=-70.0, w=None, out=None, sub=None):
    """Haritada koordinata bağlı levha (isteğe bağlı üstü çizilir)."""
    def fn(cx, cm, mv):
        x, y = cm.ll(lon, lat)
        tag(text, x + dx, y + dy, at, size=size, w=w, out=out, sub=sub)(cx)
        if strike_at is not None:
            ks = ease_out(clamp((cx.t - cx.at(strike_at)) / 0.45), 2.0) * cx.amt(at, 0.55)
            if out is not None:
                ks *= 1.0 - cx.amt(out, 0.4)
            if ks > 0.005:
                wd = (w if w is not None else sk.text_width(text, "title_m", size, 6) + 76)
                p = cx.f.paint("#A8321E", style="stroke", sw=8.0, alpha=0.95)
                CM.wobble(p, 9.0, 1.4, 5)
                cx.f.c.drawLine(x + dx - wd / 2 - 8, y + dy + 2, x + dx - wd / 2 - 8 + (wd + 16) * ks, y + dy - 6, p)
    return fn
