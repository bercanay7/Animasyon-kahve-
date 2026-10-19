"""p6_lib — PARÇA 6 (c12 Dük · c13 İki Kraliçe) ortak çizim/yardımcı işlevleri. Yalnız Parça 6 sahne dosyaları (`scenes_c12.py`, `scenes_c13.py`,
`c12_kinds.py`, `c13_kinds.py`) kullanır; motor/dünya dosyalarına dokunmaz, onların işlevlerini ÇAĞIRIR (cilt_medici, cilt_oda, cilt_pano, cilt_sehir, cilt_deniz, cilt_anim).

İçerik
  1) `p6_<tür>` sarmalayıcıları: stok türü AYNEN çağırır, ardından `ovl(cx)` ile üstüne çizer. `mono=k` verilirse (0..1) stok tür GRAVÜR (siyah-beyaz sepya) katmanında çizilir
     (film sözleşmesi: renk = belge, gravür = rivayet/anekdot); ovl her zaman renklidir. Kendi kamerası olan türler `cilt_cam.OWN_CAMERA`'ya eklenir.
  2) ovl kurucuları (çapaya bağlı etiket, levha, damga, tarih plakası, oyma yazı, karartma, sayaç, İPLİK …) — her biri `fn(cx)` döndürür; `ovl=ov(...)`.
  3) stilize madalya anahtarları (yüz iddiası YOK; üretilmiş profil): m_cosimo1, m_cosimo1_o, m_eleonora, m_francesco, m_catherine, m_catherine_dul, m_marie, m_henri2, m_charles9.
  4) özel tür iskeleti (`begin/end`), `look` kamera anahtarı, `mono_begin/mono_end`.
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
import medal
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


def _num(cx, v):
    """Çapa (sayı değilse) → bu çekimin yerel saniyesi (sayısal `at` bekleyen stok türler için)."""
    return v if isinstance(v, (int, float)) or v is None else cx.at(v)


def _fix_anchors(cx, base, kw):
    if base == "medals" and kw.get("items"):
        kw["items"] = [dict(it, at=_num(cx, it.get("at", 0.2 + 0.35 * i))) for i, it in enumerate(kw["items"])]
    if base in ("quote", "counter") and "at" in kw:
        kw["at"] = _num(cx, kw["at"])
    if base == "medal":
        for k_ in ("at", "plate_at"):
            if k_ in kw:
                kw[k_] = _num(cx, kw[k_])
    return kw


def _wrap(base):
    name = "p6_" + base

    def fn(cx, ovl=None, mono=0.0, **kw):
        kw = _fix_anchors(cx, base, kw)
        if callable(mono):
            mono = float(mono(cx))
        if mono and mono > 0.001:
            mono_begin(cx.f, mono)
            try:
                SH.KINDS[base](cx, **kw)
            finally:
                mono_end(cx.f)
        else:
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


def tag(text, x, y, at, size=34, face="title_m", track=6.0, sub=None, w=None, dur=0.55, align="c", off=0.0, out=None, color=None, corner=8, sub_color=None):
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
            CM.ink(f, sub, xx + wd / 2, yy + 8 + size * 1.02 + size * 0.86, face="cap_i", size=size * 0.74, color=sub_color or TH.fg2, align="c", alpha=k, emboss=False)
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


def count_up(x, y, at, value, dur=1.4, unit=None, size=150, face="title", color=None, prefix="", suffix="", unit_size=44, shadow=True, fmt=None, out=None, bg=False):
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
        if bg:
            wd = max(sk.text_width(txt, face, sz, 6.0), 420) + 120
            hh_ = sz * 0.95 + (unit_size * 1.7 if unit else 40) + 40
            CM.tablet(cx.f, x - wd / 2, y - sz * 0.80, wd, hh_, alpha=0.93 * k0, corner=14)
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


def desat(a_from, a_to, k_max=0.92, dark=0.0, tint="#6E7480", tint_a=0.0, k_start=0.0):
    """Doygunluk söner (sıtma/veba dili: renk solar): a_from→a_to arası k_start→1 (×k_max); isteğe bağlı kararma ve soğuk ton."""
    def fn(cx):
        t0, t1 = cx.at(a_from), cx.at(a_to)
        k = k_start + (1.0 - k_start) * smooth(clamp((cx.t - t0) / max(1e-3, t1 - t0)))
        if k <= 0.003:
            return
        cx.f.rect(0, 0, W, H, color="#808080", alpha=k * k_max, blend=skia.BlendMode.kSaturation)
        if tint_a > 0:
            cx.f.rect(0, 0, W, H, color=tint, alpha=tint_a * k)
        if dark > 0:
            cx.f.rect(0, 0, W, H, shader=cx.f.rad(W / 2, H / 2, H * 0.95, [("#0A0810", 0.0, int(255 * dark * 0.35 * k)), ("#0A0810", 1.0, int(255 * dark * k))]))
    return fn


def icon_at(name, x, y, at, size=160, metal="gold", out=None, rot=0.0, dur=0.5, glow=False, bob=0.0, flip=False):
    """Ekran uzayında simge (çapada pop ile girer)."""
    def fn(cx):
        k = _kk(cx, at, dur, out, 0.4)
        if k <= 0.003:
            return
        sc = 0.7 + 0.3 * sk.back_out(k)
        yy = y + bob * math.sin(cx.t * 2.0)
        if glow:
            cx.f.circle(x, yy, size * 0.8, shader=cx.f.rad(x, yy, size * 0.8, [("#F0D27A", 0.0, int(80 * k)), ("#F0D27A", 1.0, 0)]))
        icons.draw_icon(cx.f, name, x, yy, size=size * sc, metal=metal, alpha=k, rot=rot, glow=0.0, flip=flip)
    return fn


def icon_move(name, p0, p1, at, dur=1.2, size=120, metal="gold", out=None, glow=True, arc=60.0, rot=0.0, hold_before=False):
    """Simge p0'dan p1'e uçar (yay biçimli; ease_io). hold_before: hareketten önce p0'da görünür."""
    def fn(cx):
        u = clamp((cx.t - cx.at(at)) / dur)
        if u <= 0 and not hold_before:
            return
        e = ease_io(u)
        x = lerp(p0[0], p1[0], e)
        y = lerp(p0[1], p1[1], e) - arc * math.sin(math.pi * e)
        al = 1.0 if hold_before else clamp(u * 6.0)
        if out is not None:
            al *= 1.0 - cx.amt(out, 0.4)
        if al <= 0.003:
            return
        if glow:
            cx.f.circle(x, y, size * 0.75, shader=cx.f.rad(x, y, size * 0.75, [("#F0D27A", 0.0, int(70 * al)), ("#F0D27A", 1.0, 0)]))
        icons.draw_icon(cx.f, name, x, y, size=size, metal=metal, alpha=al, rot=rot * e, glow=0.0)
    return fn


def tablet_text(text, x, y, at, size=40, face="cap_b", pad=34, dur=0.5, out=None, rot=0.0, color=None, fill=None):
    """Yazılı sıva levha (ekran uzayı; x,y = levha merkezi)."""
    def fn(cx):
        k = _kk(cx, at, dur, out, 0.4)
        if k <= 0.003:
            return
        wd = sk.text_width(text, face, size) + 2 * pad
        hh = size + 44
        CM.tablet(cx.f, x - wd / 2, y - hh / 2 + (1 - k) * 12, wd, hh, alpha=k, rot=rot, fill=fill)
        CM.ink(cx.f, text, x, y + size * 0.34 + (1 - k) * 12, face=face, size=size, color=color or TH.fg, align="c", alpha=k, emboss=False)
    return fn


def dots_row(x0, y, n, at, step=0.28, r=22, gap=64, col="#B33620", out=None, ring="#7A3A24", dur=0.35):
    """n adet palle benzeri yuvarlak, çapadan itibaren sırayla dolar (ör. 10 çocuksuz yıl)."""
    def fn(cx):
        base = cx.at(at)
        for i in range(n):
            k = clamp((cx.t - (base + i * step)) / dur)
            ko = 1.0 - (cx.amt(out, 0.4) if out is not None else 0.0)
            xx = x0 + i * gap
            cx.f.circle(xx, y, r, style="stroke", sw=3, color=ring, alpha=0.8 * ko)
            if k > 0.003:
                rr = r * (0.2 + 0.8 * sk.back_out(k))
                cx.f.circle(xx, y, rr, color=col, alpha=0.95 * ko)
                cx.f.circle(xx - rr * 0.28, y - rr * 0.30, rr * 0.28, color="#FFFFFF", alpha=0.25 * ko)
    return fn


def fleet_bar(at, n_hi=12, n_all=200, x=960, y=170, w=980, dur=1.4, hi_at=None, hi_label="TOSKANA", all_label="≈200", out=None):
    """Lepanto kadırga çubuğu: uzun bar (≈200) içinde altın payı (12). İki etiket: sağda toplam, solda Toskana. Rakam yalnız script'in söylediği (12, ≈200)."""
    def fn(cx):
        k = _kk(cx, at, dur, out, 0.5)
        if k <= 0.003:
            return
        f = cx.f
        h = 54
        x0 = x - w / 2
        CM.tablet(f, x0 - 26, y - h / 2 - 66, w + 52, h + 150, alpha=0.9 * k, corner=14)
        f.rrect(x0, y - h / 2, w, h, 10, color="#2A2C32", alpha=0.35 * k)
        fill = ease_out(clamp((cx.t - cx.at(at)) / dur), 3)
        f.rrect(x0, y - h / 2, w * fill, h, 10, shader=f.lin(x0, y - h / 2, x0, y + h / 2, [("#4468C0", 0.0), ("#233C8C", 1.0)]), alpha=k)
        kh = cx.amt(hi_at if hi_at is not None else at, 0.6, off=dur * 0.9 if hi_at is None else 0.0)
        wh = w * (n_hi / n_all) * 2.2 * kh
        f.rrect(x0, y - h / 2, max(0.0, wh), h, 10, shader=f.lin(x0, y - h / 2, x0, y + h / 2, [("#F4DE90", 0.0), ("#B07F22", 1.0)]), alpha=k)
        f.rrect(x0, y - h / 2, w, h, 10, style="stroke", sw=3, color=TH.plate_edge, alpha=0.9 * k)
        CM.ink(f, all_label + " KADIRGA", x0 + w, y + h / 2 + 52, face="title_m", size=34, color=TH.fg, align="r", track=6, alpha=k * fill, emboss=False)
        CM.ink(f, str(n_hi) + " " + hi_label, x0, y - h / 2 - 22, face="title_m", size=34, color=TH.acc, align="l", track=6, alpha=k * kh, emboss=False)
    return fn


def _catmull(pts, n=14):
    """Catmull-Rom yoğunlaştırma (uçlar sabit)."""
    if len(pts) < 3:
        return list(pts)
    P_ = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P_) - 2):
        p0, p1, p2, p3 = P_[i - 1], P_[i], P_[i + 1], P_[i + 2]
        for j in range(n):
            t = j / n
            t2, t3 = t * t, t * t * t
            out.append((0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
                        0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)))
    out.append(pts[-1])
    return out


def thread_pts(pts, k0, k1, n=14):
    """Yoğunlaştırılmış yolun [k0,k1] oransal bölümü (uzunluğa göre)."""
    d = _catmull(pts, n)
    if len(d) < 2:
        return d
    cum = [0.0]
    for a, b in zip(d[:-1], d[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    L = cum[-1] or 1.0
    s0, s1 = L * clamp(k0), L * clamp(k1)
    out = []
    for i in range(len(d)):
        if cum[i] >= s0 and cum[i] <= s1:
            out.append(d[i])
    # uç noktaları interpolasyonla ekle
    def at_s(s):
        for i in range(1, len(d)):
            if cum[i] >= s:
                u = (s - cum[i - 1]) / max(1e-6, cum[i] - cum[i - 1])
                return (lerp(d[i - 1][0], d[i][0], u), lerp(d[i - 1][1], d[i][1], u))
        return d[-1]
    return [at_s(s0)] + out + [at_s(s1)]


def thread(pts, at, dur=2.2, w=3.4, w_end=None, col=None, glow=True, free_at=None, free_dur=2.6, break_at=None, bf=0.5, out=None, alpha=1.0, shimmer=0.0, wob=1.0, tip=True,
           sag=0.0):
    """İPLİK (Parklar'ın kader ipliği — c13'ün ortak motifi; c12 kapısında başlar): ekran uzayında ince, hafif titreyen çizgi; `at`'ta çizilmeye başlar (dur sn),
    w→w_end kalınlaşabilir. free_at: uç serbest kalır, aşağı süzülür (Blois). break_at: bf oranında KOPAR, iki yarı çekilir/sarkar. shimmer: parlama (Rubens ilk çerçeve).
    pts = [(x,y), …] ekran noktaları (Catmull-Rom ile yumuşatılır)."""
    def fn(cx):
        t = cx.t
        k = ease_io(clamp((t - cx.at(at)) / max(1e-3, dur)), 2.0)
        if k <= 0.002:
            return
        a_out = 1.0 - (cx.amt(out, 0.6) if out is not None else 0.0)
        if a_out <= 0.003:
            return
        c = cx.f.c
        cc = col or ("#8E3342" if TH.day else "#F4DE90")
        ww = w + (w_end - w) * k if w_end is not None else w
        pulse = 1.0 + shimmer * (0.5 + 0.5 * math.sin(t * 7.0))

        def draw(pp, a=1.0, wid=None):
            if len(pp) < 2:
                return
            path = sk.poly_path(pp, close=False)
            wd = (wid or ww) * pulse
            if glow:
                c.drawPath(path, cx.f.paint(cc, style="stroke", sw=wd * 4.2, alpha=0.10 * a * a_out * alpha * (1 + shimmer * 2), cap="round", blur=3.0))
            p = cx.f.paint(cc, style="stroke", sw=wd, alpha=0.95 * a * a_out * alpha, cap="round")
            if wob > 0:
                p.setPathEffect(skia.DiscretePathEffect.Make(26.0, 0.9 * wob, 3))
            c.drawPath(path, p)
        if break_at is not None and t >= cx.at(break_at):
            kb = clamp((t - cx.at(break_at)) / 2.6)
            e = ease_out(kb, 2.0)
            fade = 1.0 - 0.55 * smooth(clamp((kb - 0.4) / 0.6))
            A = thread_pts(pts, 0.0, bf * (1.0 - 0.30 * e))
            B = thread_pts(pts, bf + (1.0 - bf) * 0.30 * e, 1.0)
            # serbest uçlar aşağı süzülür (sarkıt)
            def droop(pp, from_end):
                n = len(pp)
                out_ = []
                for i, (x, y) in enumerate(pp):
                    s = (i / max(1, n - 1)) if from_end else (1 - i / max(1, n - 1))
                    out_.append((x + 14 * e * s * s * (1 if from_end else -1), y + 140 * e * s ** 2.2 + 6 * math.sin(t * 2.2 + s * 5) * e * s))
                return out_
            draw(droop(A, True), fade)
            draw(droop(B, False), fade)
            return
        if free_at is not None and t >= cx.at(free_at):
            kf = ease_out(clamp((t - cx.at(free_at)) / free_dur), 2.0)
            pp = thread_pts(pts, 0.0, 1.0)
            n = len(pp)
            q = []
            for i, (x, y) in enumerate(pp):
                s = i / max(1, n - 1)
                q.append((x + 10 * kf * s * math.sin(t * 1.6 + s * 4), y + 260 * kf * s ** 3 + 8 * kf * s * math.sin(t * 2.1 + s * 6)))
            draw(q, 1.0)
            return
        pp = thread_pts(pts, 0.0, k)
        if sag > 0 and len(pp) > 2:
            n = len(pp)
            pp = [(x, y + sag * 4 * (i / (n - 1)) * (1 - i / (n - 1))) for i, (x, y) in enumerate(pp)]
        draw(pp, 1.0)
        if tip and k < 0.995 and len(pp) > 1:
            x, y = pp[-1]
            c.drawCircle(x, y, 5.0 + 2.0 * math.sin(t * 9), cx.f.paint("#FFF1B8", alpha=0.9 * a_out))
            cx.f.circle(x, y, 20, shader=cx.f.rad(x, y, 20, [("#FFF1B8", 0.0, 120), ("#FFF1B8", 1.0, 0)]))
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


def end(cx, cam, mono=0.0, motes_n=26, light=None, vig_s=None, dust=True, k=1.0):
    cam.end(cx.f)
    CM.finish(cx.f, cx, motes_n=motes_n, light=light, vig_s=vig_s, dust=dust, k=k)
    if mono > 0.001:
        mono_end(cx.f)


def look(wx, wy, z=1.0, rot=0.0):
    """Anahtar kare: dünya (wx,wy) noktası ekran merkezinde, zoom z (cam=[(çapa, look(...)), …])."""
    return (z * (wx - W / 2), z * (wy - H / 2), z, rot)


def breath(cx, a=0.008, hz=0.45, ph=0.0):
    return 1.0 + a * math.sin(cx.t * hz * 6.283 + ph)


# ───────────────────────────── 4) stilize madalya anahtarları (yüz iddiası YOK) ─────────────────────────────
def _reg_medals():
    base = dict(mouth_open=0.0, beard=None)
    ppl = {
        # Cosimo I: genç (kentin başı, 17) ve olgun
        "m_cosimo1": dict(nose=20, hook=5, brow=3, lip=2, lip2=5, chin=8, jaw=1.0, fore=2, age=0.02, jowl=0.0, neck=0.95, hair="short", hat="cap", garment="doublet"),
        "m_cosimo1_o": dict(nose=22, hook=6, brow=4, lip=1, lip2=4, chin=10, jaw=1.1, fore=2, age=0.62, jowl=0.16, neck=1.05, hair="thin", hat="cap_black", beard="short", garment="robe"),
        "m_francesco": dict(nose=14, hook=2, brow=3, lip=3, lip2=8, chin=14, jaw=1.0, fore=1, age=0.12, jowl=0.0, neck=1.0, hair="short", hat="cap_black", garment="doublet"),
        # kadınlar: başlık/örtü profili (yüz ayrıntısı asgari, ayırt edici iddia yok)
        "m_eleonora": dict(nose=12, hook=2, brow=2, lip=2, lip2=5, chin=8, jaw=0.85, fore=3, age=0.15, jowl=0.0, neck=0.9, hair="veil", hat="gable_hood", garment="gown_f"),
        "m_catherine": dict(nose=14, hook=2, brow=2, lip=3, lip2=7, chin=10, jaw=0.95, fore=2, age=0.22, jowl=0.04, neck=0.95, hair="veil", hat="gable_hood", garment="gown_f"),
        "m_catherine_dul": dict(nose=14, hook=2, brow=2, lip=3, lip2=7, chin=10, jaw=0.98, fore=2, age=0.5, jowl=0.12, neck=1.0, hair="veil", hat="widow_hood", garment="mourning_f"),
        "m_marie": dict(nose=11, hook=0, brow=2, lip=3, lip2=8, chin=12, jaw=0.95, fore=2, age=0.25, jowl=0.08, neck=1.0, hair="veil", hat="gable_hood", garment="gown_f"),
        "m_henri2": dict(nose=16, hook=3, brow=3, lip=2, lip2=4, chin=6, jaw=1.1, fore=2, age=0.3, jowl=0.05, neck=1.05, hair="short", hat="beret_f", beard="short", garment="fur_doublet"),
        "m_charles9": dict(nose=8, hook=0, brow=2, lip=3, lip2=6, chin=6, jaw=0.85, fore=3, age=0.0, jowl=0.0, neck=0.85, hair="bob", hat="flatcap", garment="doublet"),
        "m_michelangelo": dict(nose=24, hook=8, brow=5, lip=1, lip2=3, chin=4, jaw=1.1, fore=1, age=0.85, jowl=0.2, neck=1.05, hair="thin", hat="cap_black", beard="full", garment="robe"),
    }
    insc = {
        "m_cosimo1": "COSMVS · MEDICES ·", "m_cosimo1_o": "COSMVS · MEDICES ·", "m_francesco": "FRANCISCVS · MEDICES ·",
        "m_eleonora": "ELEONORA · A · TOLEDO ·", "m_catherine": "CATERINA · MEDICES · REGINA ·", "m_catherine_dul": "CATERINA · MEDICES · REGINA ·",
        "m_marie": "MARIA · MEDICES · REGINA ·", "m_henri2": "HENRICVS · II · FRANCORVM · REX ·", "m_charles9": "CAROLVS · IX · FRANCORVM · REX ·",
        "m_michelangelo": "MICHAELANGELVS · BONAROTVS ·",
    }
    for k, d in ppl.items():
        dd = dict(base)
        dd.update(d)
        medal.PEOPLE.setdefault(k, dd)
        medal.INSCR.setdefault(k, insc[k])


_reg_medals()


# ───────────────────────────── 5) küçük sahne yardımcıları (ovl) ─────────────────────────────
def strings_down(xs, y0, tip, at, out=None, col="#3A2A18", sw=2.2, sway=10.0, cap=True):
    """Kukla ipleri: ekranın üstünden (xs) `tip` noktasında toplanır (yönetilebilir biri: YORUM); küçük bere/başlık simgesi uçta."""
    def fn(cx):
        k = _kk(cx, at, 0.8, out, 0.5)
        if k <= 0.003:
            return
        c = cx.f.c
        e = ease_out(k, 2.5)
        tx = tip[0] + math.sin(cx.t * 1.3) * sway * 0.4
        ty = lerp(y0, tip[1], e) + 6 * math.sin(cx.t * 2.1)
        for i, x in enumerate(xs):
            sx = x + math.sin(cx.t * 1.1 + i) * sway
            c.drawLine(sx, y0, tx + (i - (len(xs) - 1) / 2) * 12, ty, S(col, sw, int(235 * k)))
        if cap:
            c.drawOval(skia.Rect.MakeLTRB(tx - 34, ty - 6, tx + 34, ty + 24), P("#6A1E14", int(250 * k)))
            c.drawOval(skia.Rect.MakeLTRB(tx - 34, ty - 6, tx + 34, ty + 24), S("#2A0806", 2.0, int(230 * k)))
            c.drawRect(skia.Rect.MakeLTRB(tx - 38, ty + 16, tx + 38, ty + 28), P("#3A0806", int(250 * k)))
    return fn


def timeline_span(x0, x1, y, at, dur=2.2, l0="1560", l1="1769", at1=None, size=44):
    """Yıl cetveli bandı: x0'dan x1'e uzar (çok sonra); iki ucuna yıl etiketleri (ikincisi at1 çapasında)."""
    def fn(cx):
        k = ease_io(clamp((cx.t - cx.at(at)) / dur), 1.6)
        if k <= 0.003:
            return
        f = cx.f
        xe = lerp(x0, x1, k)
        f.line(x0, y, xe, y, color="#7A5A2E", sw=7, alpha=0.95)
        f.line(x0, y, xe, y, color="#E8C468", sw=3, alpha=0.95)
        f.line(x0, y - 22, x0, y + 22, color="#7A5A2E", sw=6, alpha=0.95)
        CM.tablet(f, x0 - 80, y - 118, 160, 72, alpha=min(1.0, k * 6), corner=8)
        CM.ink(f, l0, x0, y - 66, face="title", size=size, color=TH.fg, align="c", track=5, alpha=min(1.0, k * 6), emboss=False)
        k1 = cx.amt(at1, 0.5) if at1 is not None else clamp((k - 0.95) * 20)
        if k1 > 0.003:
            f.line(x1, y - 22, x1, y + 22, color="#7A5A2E", sw=6, alpha=0.95 * k1)
            CM.tablet(f, x1 - 80, y - 118, 160, 72, alpha=k1, corner=8)
            CM.ink(f, l1, x1, y - 66, face="title", size=size, color=TH.fg, align="c", track=5, alpha=k1, emboss=False)
        if k > 0.02:
            f.circle(xe, y, 9, color="#FFF1B8", alpha=0.95 if k < 0.99 else 0.0)
    return fn


def silhouette_queue(x0, y, n, at, speed=60.0, h=150, dir=1, step=120.0, seed=3, color="#14100A", out=None, kinds=("halk", "soylu", "cocuk", "soylu_f"), fade_x=None):
    """Silüet kuyruğu (c0'ın «bugünün kuyruğu»na yankı): n kişi yürür; fade_x=(a,b) aralığında solar (kapıdan girer)."""
    def fn(cx):
        k0 = _kk(cx, at, 0.6, out, 0.6)
        if k0 <= 0.003:
            return
        t = cx.t
        t0 = cx.at(at)
        for i in range(n):
            x = x0 + dir * (speed * (t - t0)) + dir * (-i * step)
            al = k0
            if fade_x is not None:
                a_, b_ = fade_x
                u = clamp((x - a_) / (b_ - a_)) if dir > 0 else clamp((a_ - x) / (a_ - b_))
                al *= 1.0 - u
            if al <= 0.01 or x < -200 or x > W + 200:
                continue
            OD.sil_actor(cx.f, kinds[(i + seed) % len(kinds)], x, y, h * (0.92 + 0.12 * ((i * 7 + seed) % 3) / 2), t, walker=speed, dir=dir, seed=seed * 13 + i, color=color, rim="#E8B070", rim_dir=1,
                         alpha=al, phase=0.21 * i)
    return fn


def mantle(at, cx_=960, y_=640, w=620, dur=1.2, out=None):
    """Şövalye mantosu (kızıl) sağdan kayarak omuzlara oturur; göğüste haç. (giydirildi)"""
    def fn(cx):
        k = _kk(cx, at, dur, out, 0.5)
        if k <= 0.003:
            return
        f = cx.f
        c = f.c
        e = ease_out(k, 2.4)
        dx = (1 - e) * 900
        pts = [(cx_ - w / 2 + dx, y_ + 40), (cx_ - w * 0.30 + dx, y_ - 40), (cx_ + w * 0.30 + dx, y_ - 40), (cx_ + w / 2 + dx, y_ + 40), (cx_ + w * 0.58 + dx, y_ + 420), (cx_ - w * 0.58 + dx, y_ + 420)]
        path = sk.smooth_path(pts, True, 0.35)
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(0, y_ - 80, W, H))
        c.drawPath(path, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(cx_, y_ - 40), (cx_, y_ + 420)], [C("#B8261A"), C("#6E100C")], [0, 1])))
        c.drawPath(path, S("#3A0806", 3.4, 235))
        # göğüste beyaz haç
        px_, py_ = cx_ - w * 0.20 + dx, y_ + 150
        c.drawRect(skia.Rect.MakeLTRB(px_ - 9, py_ - 52, px_ + 9, py_ + 52), P("#F4EAD0", 245))
        c.drawRect(skia.Rect.MakeLTRB(px_ - 52, py_ - 9, px_ + 52, py_ + 9), P("#F4EAD0", 245))
        c.restore()
    return fn


def chain_break(x, y, at_in, at_break, size=260, out=None):
    """Zincir simgesi çıkar; kırılma anında iki yarı ayrılır (Hristiyan esirleri kurtarmak: yalnız simge)."""
    def fn(cx):
        k = _kk(cx, at_in, 0.6, out, 0.5)
        if k <= 0.003:
            return
        u = ease_out(clamp((cx.t - cx.at(at_break)) / 0.9), 2.2) if at_break is not None else 0.0
        f = cx.f
        c = f.c
        sc = 0.7 + 0.3 * sk.back_out(k)
        for sg in (-1, 1):
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(x - 400 if sg < 0 else x, y - 300, x if sg < 0 else x + 400, y + 300))
            c.translate(sg * u * 70, u * u * 40 * 1.0)
            c.translate(x, y)
            c.rotate(sg * u * 14.0)
            c.translate(-x, -y)
            icons.draw_icon(f, "chains", x, y, size=size * sc, metal="gold", alpha=k * (1.0 - 0.35 * u), glow=0.0)
            c.restore()
        if u > 0.02 and u < 0.8:
            f.circle(x, y, 40 + 150 * u, style="stroke", sw=3, color="#FFF1B8", alpha=0.7 * (1 - u / 0.8))
    return fn


def vignette_in(at, out=None, col="#06060C", a=0.55):
    """Kenarlardan kararan vinyet (ağır an)."""
    def fn(cx):
        k = _kk(cx, at, 1.0, out, 0.8)
        if k > 0.003:
            cx.f.rect(0, 0, W, H, shader=cx.f.rad(W / 2, H / 2, H * 0.95, [(col, 0.2, 0), (col, 1.0, int(255 * a * k))]))
    return fn
