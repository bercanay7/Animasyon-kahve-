"""p1_ortak — Parça 1 (c0–c2) ortak yardımcılar. Yalnız Parça 1 sahne dosyaları kullanır (ana motor dosyalarına dokunmaz).

1) Sarmalayıcı türler `p1_<tür>` (oda, pano, sehir, build, coin, medal, emblem, ...): iç türü AYNEN çağırır, ardından `ovl(cx)` ile üstüne çizer
   (kamera/duvar/ışık iç türde; ovl ekran uzayında: sayaç, levha, damga, etiket). Kendi kamerası olan türler (oda/pano/sehir/build) `cilt_cam.OWN_CAMERA`'ya
   çalışma anında eklenir (cilt_sehir ile aynı yöntem) → `cam=` uygulanmaz, `cams=/path=` iç türe verilir.
2) Küçük "ovl" kurucuları (levha, etiket, damga, vuruş yazısı, sayaç ...): her biri `fn(cx)` döndürür; `ovl=ov(...)` ile birleştirilir.
3) Ortak çizim işlevleri (parıltı süpürmesi, mühür, boya şeridi vb.).
Olgu disiplini: bu modül kendi başına metin üretmez; metinler sahne dosyasından gelir.
"""
import math

import skia

import cilt_cam
import cilt_medici as CM
import shots as SH
import sk
from cilt_medici import TH, ckind
from sk import H, W, clamp, ease_io, ease_out, lerp, mix, smooth

_OWN = {"oda", "pano", "sehir", "build"}


def _wrap(inner):
    name = "p1_" + inner

    @ckind(name)
    def k(cx, ovl=None, **kw):
        SH.KINDS[inner](cx, **kw)
        if ovl is not None:
            ovl(cx)

    k.__name__ = "k_" + name
    if inner in _OWN:
        cilt_cam.OWN_CAMERA.add(name)
    return k


for _n in ("oda", "pano", "sehir", "build", "coin", "medal", "emblem", "palle", "map", "frieze", "procession", "iconrow", "counter", "bars", "doc", "ledger", "quote",
           "skyline", "network", "timeline", "stacked", "tree", "medals", "letter"):
    if _n in SH.KINDS:
        _wrap(_n)


def add_ovl(names):
    """Verilen (ckind ile kayıtlı) türleri YERİNDE sarar: `ovl=` parametresi türün tüm çizimi (ışık/vinyet dahil) bittikten sonra çalışır."""
    for n in names:
        orig = SH.KINDS[n]

        def mk(orig):
            def k(cx, ovl=None, **kw):
                orig(cx, **kw)
                if ovl is not None:
                    ovl(cx)
            k._raw = getattr(orig, "_raw", orig)
            return k
        SH.KINDS[n] = mk(orig)


# ───────────────────────────── ovl kurucuları ─────────────────────────────
def ov(*items):
    """Birden çok ovl'u art arda çalıştırır."""
    items = [i for i in items if i]

    def fn(cx):
        for it in items:
            it(cx)
    return fn


def label(text, x, y, at, size=44, face="title_m", color=None, align="c", track=8.0, dur=0.7, out=None, out_dur=0.5, rise=14, emboss=False, alpha=1.0):
    """Zamanı çapaya bağlı yazı: `at`'ta yukarı doğru belirir, isteğe bağlı `out` çapasında solar. color None → tema."""
    def fn(cx):
        k = cx.amt(at, dur)
        if out is not None:
            k *= 1.0 - cx.amt(out, out_dur)
        if k <= 0.003:
            return
        CM.ink(cx.f, text, x, y + (1 - k) * rise, face=face, size=size, color=color or TH.fg, align=align, track=track, alpha=k * alpha, emboss=emboss)
    return fn


def plate(name, x, y, at, role=None, dates=None, w=None, dur=0.6, out=None, out_dur=0.5):
    """Madalya levhası (isim tabelası) — `at`'ta açılır."""
    def fn(cx):
        k = cx.amt(at, dur)
        if out is not None:
            k *= 1.0 - cx.amt(out, out_dur)
        if k <= 0.003:
            return
        CM.name_plate(cx.f, name, role, dates, cx_=x, y=y, t=k, w=w)
    return fn


def stamp(text, x, y, at, rot=-0.10, size=56, color=None, out=None, dur=0.3):
    """Damga çarpması (0,3 sn)."""
    def fn(cx):
        t = cx.amt(at, dur)
        if out is not None:
            t_out = 1.0 - cx.amt(out, 0.4)
        else:
            t_out = 1.0
        if t <= 0 or t_out <= 0.01:
            return
        CM.stamp(cx.f, text, x, y, rot=rot, size=size, color=color, alpha=t_out, t=t)
    return fn


def tablet_text(text, x, y, at, size=40, face="cap_b", pad=34, dur=0.5, out=None, rot=0.0, color=None, fill=None):
    """Yazılı sıva levha (ekran uzayı; x,y = levha merkezi)."""
    def fn(cx):
        k = cx.amt(at, dur)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k <= 0.003:
            return
        wd = sk.text_width(text, face, size) + 2 * pad
        hh = size + 44
        CM.tablet(cx.f, x - wd / 2, y - hh / 2 + (1 - k) * 12, wd, hh, alpha=k, rot=rot, fill=fill)
        CM.ink(cx.f, text, x, y + size * 0.34 + (1 - k) * 12, face=face, size=size, color=color or TH.fg, align="c", alpha=k, emboss=False)
    return fn


def count_up(x, y, at, value, dur=1.4, unit=None, size=150, face="title", color=None, prefix="", suffix="", unit_size=44, shadow=True, align="c", fmt=None, out=None, bg=False):
    """Sayı sayar (0→value, ease_out). Büyük Cinzel; altında birim. Yaldız (gece) / oyma (gündüz)."""
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
        CM.draw_spr(cx.f, sp, x, y, "c" if align == "c" else "l", alpha=k0, shadow=0.5 if shadow and not TH.day else 0.0)
        if unit:
            CM.ink(cx.f, unit, x, y + unit_size * 1.25 + 8, face="title_m", size=unit_size, color=TH.acc, align="c", track=14, alpha=k0 * cx.amt(at, 0.8, off=0.3), emboss=False)
    return fn


def scrim(a_from, a_to, col="#000000", alpha=0.35, dur=0.8):
    """Ekran örtüsü (vurgu için kenar karartma); a_from→a_to arası görünür."""
    def fn(cx):
        k = cx.amt(a_from, dur) * (1.0 - cx.amt(a_to, dur))
        if k > 0.003:
            cx.f.rect(0, 0, W, H, color=col, alpha=alpha * k)
    return fn


def glint(x, y, at, r=90, col="#FFF1B8", dur=0.9, alpha=0.9):
    """Işıltı: haç parıltısı + halka (altın/sikke vurgusu)."""
    def fn(cx):
        p = clamp((cx.t - cx.at(at)) / dur)
        if p <= 0 or p >= 1:
            return
        a = math.sin(p * math.pi)
        R = r * (0.4 + 0.8 * p)
        cx.f.circle(x, y, R, shader=cx.f.rad(x, y, R, [(col, 0.0, int(190 * a * alpha)), (col, 1.0, 0)]))
        c = cx.f.c
        for ang in (0, 90):
            dx, dy = math.cos(math.radians(ang)) * R * 1.25 * a, math.sin(math.radians(ang)) * R * 1.25 * a
            c.drawLine(x - dx, y - dy, x + dx, y + dy, cx.f.paint(col, style="stroke", sw=2.4, alpha=0.9 * a * alpha))
    return fn


# ───────────────────────────── genel çizim yardımcıları ─────────────────────────────
def pigment_band(f, y0, y1, color, alpha=0.5, p=1.0, seed=3, x0=0, x1=W):
    """Soldan sağa yayılan pigment şeridi (p: 0..1 yayılma); kenarı dalgalı."""
    if p <= 0.001:
        return
    c = f.c
    pts = [(x0, y0)]
    xr = x0 + (x1 - x0) * p
    n = 14
    for i in range(n + 1):
        u = i / n
        pts.append((x0 + (xr - x0) * u, y0 - 6 * math.sin(u * 7 + seed)))
    for i in range(n, -1, -1):
        u = i / n
        pts.append((x0 + (xr - x0) * u + 12 * math.sin(u * 5 + seed * 2) * (1 if i == n else 0), y1 + 6 * math.sin(u * 6 + seed * 1.3)))
    path = sk.poly_path(pts)
    c.drawPath(path, f.paint(color, alpha=alpha))


def hex_alpha(col, a):
    return sk.C(col, int(255 * clamp(a)))


def lerp_pt(a, b, t):
    return (lerp(a[0], b[0], t), lerp(a[1], b[1], t))


# ───────────────────────────── renk/atmosfer örtüleri ─────────────────────────────
def desat(a_from, a_to, k_max=0.92, dark=0.0, tint="#6E7480", tint_a=0.0, k_start=0.0):
    """Doygunluk söner (veba: renk solar): a_from→a_to arası k_start→1 (×k_max); isteğe bağlı kararma (dark) ve soğuk ton (tint_a)."""
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


def red_bleed(at, dur=1.5, alpha=0.5, col="#A8201A", from_right=True, seed=4):
    """Kızıl pigment (kan DEĞİL: boya yıkama) ekrana organik kenarla yayılır."""
    def fn(cx):
        k = ease_out(clamp((cx.t - cx.at(at)) / dur), 2.0)
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
        c.drawPath(path, cx.f.paint(col, alpha=alpha * 0.35 * min(1.0, k * 2.2)))
    return fn


def dim(a_from, a_to, alpha=0.5, dur=0.8, col="#06060C"):
    """Çekimin bir bölümünde ekranı kısıtlı karart (a_from→a_to)."""
    def fn(cx):
        k = cx.amt(a_from, dur) * (1.0 - cx.amt(a_to, dur))
        if k > 0.003:
            cx.f.rect(0, 0, W, H, color=col, alpha=alpha * k)
    return fn


def dimline(x0, x1, y, at, text, size=34, out=None):
    """Ölçü çizgisi (uçlarda çentik; ortada etiket)."""
    def fn(cx):
        k = cx.amt(at, 0.6)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k <= 0.003:
            return
        f = cx.f
        xm = (x0 + x1) / 2
        e = ease_out(k, 2)
        xa, xb = xm - (xm - x0) * e, xm + (x1 - xm) * e
        col = TH.fg if TH.day else "#F0D27A"
        f.line(xa, y, xb, y, color=col, sw=3, alpha=0.9 * k)
        for xx in (xa, xb):
            f.line(xx, y - 16, xx, y + 16, color=col, sw=3, alpha=0.9 * k)
        wd = sk.text_width(text, "title_m", size, 6) + 30
        f.rrect(xm - wd / 2, y - 24, wd, 48, 8, color="#E9DDBB" if TH.day else "#10162E", alpha=0.96 * k)
        CM.ink(f, text, xm, y + size * 0.36, face="title_m", size=size, color=col, align="c", track=6, alpha=k, emboss=False)
    return fn


def crossout(x, y, r, at, out=None, col="#A8201A", sw=16, dur=0.32):
    """Kırmızı çarpı (iki çizgi sırayla çizilir)."""
    def fn(cx):
        k = cx.amt(at, dur)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k <= 0.003:
            return
        f = cx.f
        p1 = clamp(k * 2.0)
        p2 = clamp(k * 2.0 - 1.0)
        f.line(x - r, y - r, x - r + 2 * r * p1, y - r + 2 * r * p1, color=col, sw=sw, alpha=0.95)
        if p2 > 0:
            f.line(x + r, y - r, x + r - 2 * r * p2, y - r + 2 * r * p2, color=col, sw=sw, alpha=0.95)
    return fn


def icon_at(name, x, y, at, size=160, metal="gold", out=None, rot=0.0, dur=0.5, glow=False, bob=0.0):
    """Ekran uzayında simge (çapada pop ile girer)."""
    import icons

    def fn(cx):
        k = cx.amt(at, dur)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k <= 0.003:
            return
        sc = 0.7 + 0.3 * sk.back_out(k)
        yy = y + bob * math.sin(cx.t * 2.0)
        if glow:
            cx.f.circle(x, yy, size * 0.8, shader=cx.f.rad(x, yy, size * 0.8, [("#F0D27A", 0.0, int(80 * k)), ("#F0D27A", 1.0, 0)]))
        icons.draw_icon(cx.f, name, x, yy, size=size * sc, metal=metal, alpha=k, rot=rot, glow=0.0)
    return fn


def tablet_icon(icon, text, x, y, at, size=38, w=620, out=None, metal="gold", dur=0.5):
    """Soldan kayarak giren sıva levha: sol simge + Cinzel metin (x,y = levha merkezi)."""
    import icons

    def fn(cx):
        k = cx.amt(at, dur)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k <= 0.003:
            return
        e = ease_out(k, 3)
        xx = x - (1 - e) * 260
        hh = 104
        CM.tablet(cx.f, xx - w / 2, y - hh / 2, w, hh, alpha=k, corner=10)
        icons.draw_icon(cx.f, icon, xx - w / 2 + 62, y, size=74, metal=metal, alpha=k, glow=0.0)
        sz = CM.fit_size(text, "title_m", size, w - 190, 5)
        CM.ink(cx.f, text, xx - w / 2 + 120, y + sz * 0.36, face="title_m", size=sz, color=TH.fg, align="l", track=5, alpha=k, emboss=False)
    return fn


def coin_arc(p0, p1, at, n=6, dur=1.0, gap=0.16, lift=170, size=64, out=None):
    """Florinler p0 → p1 yayında uçar (ekran uzayı); n tane, `gap` aralıkla; iner inmez solar."""
    import cilt_props as CP

    def fn(cx):
        t0 = cx.at(at)
        for i in range(n):
            u = (cx.t - (t0 + gap * i)) / dur
            if u <= 0 or u >= 1.0:
                continue
            e = ease_io(u, 1.6)
            x = p0[0] + (p1[0] - p0[0]) * e
            y = p0[1] + (p1[1] - p0[1]) * e - lift * math.sin(math.pi * e)
            a = min(1.0, u * 6) * min(1.0, (1 - u) * 6 + 0.2)
            CP.draw_coin(cx.f, x, y, size, spin=cx.t * 14 + i, alpha=a, shadow=0.25)
    return fn


def pop_label(text, x, y, at, size=56, face="title", color=None, out=None, track=12.0):
    """Çarpma ölçekli (back_out) büyük yazı."""
    def fn(cx):
        k = cx.amt(at, 0.3)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k <= 0.003:
            return
        sc = 0.6 + 0.4 * sk.back_out(k)
        f = cx.f
        sz = CM.fit_size(text, face, size, 1500, track)
        sp = CM.gilt(text, face, int(sz), track) if not TH.day else CM.engraved(text, face, int(sz), track, color or TH.fg)
        CM.draw_spr(f, sp, x, y, "c", alpha=k, scale=sc, shadow=0.0)
    return fn
