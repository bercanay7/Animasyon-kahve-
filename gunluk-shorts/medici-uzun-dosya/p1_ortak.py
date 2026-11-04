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
        if inner == "sehir" and kw.get("actors"):
            acts = []
            for d in kw["actors"]:
                d = dict(d)
                an = d.pop("at", None)
                if an is not None:
                    d["t0"] = cx.at(an)
                acts.append(d)
            kw["actors"] = acts
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


def count_up(x, y, at, value, dur=1.4, unit=None, size=150, face="title", color=None, prefix="", suffix="", unit_size=44, shadow=True, align="c", fmt=None, out=None, bg=False, min_w=420):
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
            wd = max(sk.text_width(txt, face, sz, 6.0), min_w) + 120
            hh_ = sz * 0.95 + (unit_size * 1.7 if unit else 40) + 40
            CM.tablet(cx.f, x - wd / 2, y - sz * 0.80, wd, hh_, alpha=0.93 * k0, corner=14)
        CM.draw_spr(cx.f, sp, x, y, "c" if align == "c" else "l", alpha=k0, shadow=0.5 if shadow and not TH.day else 0.0)
        if unit:
            CM.ink(cx.f, unit, x, y + unit_size * 1.25 + 8, face="title_m", size=unit_size, color=TH.acc, align="c", track=14, alpha=k0 * cx.amt(at, min(0.8, 0.8 * dur), off=min(0.3, 0.3 * dur)), emboss=False)
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


# ───────────────────────────── kurul tur 1: ekran-uzayı yardımcıları ─────────────────────────────
SAFE_X0, SAFE_X1 = 96, 1824            # başlık güvenli alanı
SUB_Y0 = 930                           # altyazı bandı (938–1042) — bunun altına yazı/damga yok
HUD_RECT = (1440, 0, 1920, 124)        # yıl rulosu (küçülse de geniş tutulur)


def tag(text, x, y, at, size=40, face="title_m", out=None, dur=0.45, dark=True, track=6.0, pad=26, align="c", alpha=1.0):
    """Okunur etiket: koyu yarı saydam zemin üstüne açık krem yazı (kontrast ≥7:1) ya da açık zemin üstüne mürekkep (dark=False)."""
    def fn(cx):
        k = cx.amt(at, dur)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k <= 0.003:
            return
        f = cx.f
        sz = CM.fit_size(text, face, size, SAFE_X1 - SAFE_X0 - 2 * pad, track)
        wd = sk.text_width(text, face, sz, track) + 2 * pad
        hh = sz * 1.05 + 2 * pad * 0.62
        x0 = x - wd / 2 if align == "c" else x
        x0 = max(SAFE_X0, min(SAFE_X1 - wd, x0))
        yy = min(y, SUB_Y0 - hh / 2 - 6)
        a = k * alpha
        if dark:
            f.rrect(x0, yy - hh / 2, wd, hh, 12, color="#120C08", alpha=0.74 * a)
            f.rrect(x0, yy - hh / 2, wd, hh, 12, style="stroke", sw=2.0, color="#C9A45A", alpha=0.75 * a)
            col = "#FFF4D6"
        else:
            CM.tablet(f, x0, yy - hh / 2, wd, hh, alpha=a, corner=10)
            col = "#2A1A0C"
        CM.ink(f, text, x0 + wd / 2, yy + sz * 0.36, face=face, size=sz, color=col, align="c", track=track, alpha=a, emboss=False)
    return fn


def prop_arc(icon, p0, p1, at, dur=0.9, size=110, lift=120, metal="gold", show_from=None, out=None, rot0=0.0, rot1=0.0, glow=False):
    """Tek nesne (kese, poliçe, anahtar, mitra…) `at`'ta p0'dan p1'e yayla geçer; `show_from` verilirse o andan önce p0'da görünür, sonra p1'de kalır (`out`'a dek)."""
    import icons

    def fn(cx):
        t = cx.t
        t_at = cx.at(at)
        t_vis = cx.at(show_from) if show_from is not None else t_at
        k = clamp((t - t_vis) / 0.3)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.35)
        if k <= 0.003:
            return
        u = clamp((t - t_at) / dur)
        e = ease_io(u, 1.7)
        x = p0[0] + (p1[0] - p0[0]) * e
        y = p0[1] + (p1[1] - p0[1]) * e - lift * math.sin(math.pi * e)
        r = rot0 + (rot1 - rot0) * e
        bob = 3.0 * math.sin(t * 2.6) * (1.0 - math.sin(math.pi * e))
        if glow:
            cx.f.circle(x, y, size * 0.9, shader=cx.f.rad(x, y, size * 0.9, [("#F0D27A", 0.0, int(70 * k)), ("#F0D27A", 1.0, 0)]))
        icons.draw_icon(cx.f, icon, x, y + bob, size=size, metal=metal, alpha=k, rot=r, glow=0.0)
    return fn


def oda_xy(x, y, cam):
    """oda/pano ana düzlem noktası → ekran (cam=(camx, camy, zoom); frame='auto', zoom<1,55 bandı)."""
    camx, camy, z = cam
    return W / 2 + (x - camx) * z, 550 + (y - 470 - camy) * z


# ───────────────────────────── kurul tur 1: P1 iç mekân setleri (cilt_oda alt sınıfları; çalışma anında kayıt) ─────────────────────────────
import icons as _icons
import cilt_oda as OD

GIOVANNI = dict(kind="banker", seed=5)     # tekrar eden insan çapası: koyu kızıl cüppe (lucco), koyu berretta (kit kostümü seed=5; p1banka 0. masa da bu)
COSIMO = dict(kind="banker", seed=33)      # lacivert cüppe, kısa sakal
LORENZO_V = dict(kind="banker", seed=13)   # Giovanni'nin küçük oğlu (Lorenzo di Giovanni): kahverengi cüppe
MACHIAVELLI = dict(kind="soylu", seed=52)  # c1s20 ve c2s29/c2s33: aynı çalışma odası (calisma kutuphane), aynı figür (görsel geri çağırma)


def actor(base, **kw):
    d = dict(base)
    d.update(kw)
    return d


class P1Ofis(OD.Calisma):
    """Sayım odası / Medici evi çalışma odası (Calisma 'hucre' yerleşimi; haçsız, yataksız): sıcak sıva, kemerli pencere, yatık defter rafları, para sandığı, goblen."""
    name = "p1ofis"

    def __init__(self, variant, tod):
        self.p1v = variant or "ofis"
        self.PW = 2300
        self.always_lit = False
        self.variant = "hucre"
        self.tod = tod
        self.T = OD.OTint(tod)
        self.layers = {}
        self.opts = {}
        self.key = f"{self.name}{self.p1v}"
        self.build()

    def _draw_wall(self, fr, xa, xb):
        c, T = fr.c, self.T
        night = self.tod == "night"
        wx = self.wx
        top, bot = {"ofis": ("#D6BE92", "#E4D0A8"), "ev": ("#CDB89A", "#DCCBB0")}.get(self.p1v, ("#C8B48C", "#D8C6A0"))
        OD.plaster(c, xa, xb, OD.OV - 40, OD.Y_FL + 30, T, top, bot, amp=0.05)
        OD.cornice(c, xa, xb, 72, T, col="#6A4228", plaster=bot)
        OD.wainscot(c, xa, xb, OD.Y_FL - 120, OD.Y_FL + 18, T, "#7A4A2C", pw=170, seed=4)
        if OD._vis(wx(1760), 120, xa, xb):
            OD.draw_window(c, T, wx(1760), 214, 170, 300, night=night, shutters=True)
        # defter rafı: yatık ciltler (15. yy: sırt dışarı dizilmez)
        if OD._vis(wx(520), 300, xa, xb) and self.p1v != "ev":
            x0, x1 = wx(300), wx(760)
            for yy in (300, 420):
                OD.BOX(c, x0, yy, x1, yy + 16, "#5E3A20", T, hl=0.16, sh=0.24, ink=1.3)
                rs = OD._RS(int(yy))
                xx = x0 + 22
                while xx < x1 - 90:
                    n = 2 + rs.randint(3)
                    w_ = 70 + rs.randint(30)
                    for k in range(n):
                        OD.draw_book(c, xx + w_ / 2 + (k % 2) * 3, yy - 8 - k * 15, w_, 14, ["#6A2E24", "#2E4A6A", "#4A3A2A", "#7A5A2A"][(k + int(xx)) % 4])
                    xx += w_ + 18 + rs.randint(16)
        if OD._vis(wx(1230), 160, xa, xb) and self.p1v == "ofis":
            OD.draw_tapestry(c, T, wx(1230), 196, 230, 290, seed=6, field="#2E4A3A", border="#B88A32", accent="#8E2A30")
        if OD._vis(wx(1230), 160, xa, xb) and self.p1v not in ("ofis", "ev"):
            OD.draw_hanging(c, T, wx(1080), wx(1400), 190, 470, "#2E3E5A", "#C9A45A", seed=3)
        if self.p1v == "ev":                     # mütevazı ev (c1s25): defter rafı yok; sade duvar nişi + küçük tahta raf (testi/kâse)
            if OD._vis(wx(560), 200, xa, xb):
                OD.BOX(c, wx(380), 330, wx(740), 346, "#6A4A2C", T, hl=0.16, sh=0.24, ink=1.3)
                for k, xx in enumerate((wx(430), wx(520), wx(610), wx(690))):
                    c.drawOval(skia.Rect.MakeLTRB(xx - 22, 270 + 10 * (k % 2), xx + 22, 330), OD.PT(T(["#9A5A32", "#7A6A4A", "#A8743E", "#6A4A2C"][k]), 255))
            if OD._vis(wx(1230), 160, xa, xb):
                OD.draw_tapestry(c, T, wx(1230), 196, 230, 290, seed=9, field="#5A2E24", border="#9A7A3A", accent="#2E4A3A")
        sh = OD.LGP((0, OD.Y_FL - 30), (0, OD.Y_FL + 30), [("#1A0F06", 0.0, 0), ("#1A0F06", 1.0, 70)])
        c.drawRect(skia.Rect.MakeLTRB(xa, OD.Y_FL - 30, xb, OD.Y_FL + 30), sh)

    def _draw_main(self, fr, xa, xb):
        c, T = fr.c, self.T
        OD.floor_tiles(c, xa, xb, OD.Y_FL, OD.LH, T, "#A8603A", "#94522F", seed=8, w0=74.0, grow=1.13)
        if OD._vis(520, 200, xa, xb):
            OD.draw_chest(c, T, 380, 660, 792, 128, "#5A3A24")
        if OD._vis(self.CH_X, 70, xa, xb):
            OD.draw_chair(c, T, self.CH_X - 24, 808, 240, 72, 88, facing=1, col="#5A3A20", cushion="#7A2E2A")


P1_SALON_PAL = {
    "papa": dict(wall=("#A88468", "#C09C7E"), dado="#5A2A20", tap=("#7A1E24", "#C79A3C"), floor=("#C9B58A", "#7A3A2A"), cloth=("#8E2A30", "#D2A33E"), deco="tap", seat="#7A2E2A"),
    "konstanz": dict(wall=("#A4A6A0", "#BCBDB4"), dado="#3A4650", tap=("#2A3E6E", "#C79A3C"), floor=("#B0AC9C", "#5E5A50"), cloth=("#2A3E6E", "#C79A3C"), deco="tap", seat="#2A3E6E"),
}


class P1Salon(OD.Salon):
    """Taht salonu (Salon 'taht' yerleşimi) — palle frizi YOK (Medici dışı mekânlar): 'papa' (papalık kabul salonu, kızıl-altın), 'konstanz' (konsil salonu, serin taş)."""
    name = "p1salon"

    def __init__(self, variant, tod):
        self.p1v = variant or "papa"
        self.pal = P1_SALON_PAL.get(self.p1v, P1_SALON_PAL["papa"])
        self.variant = "taht"
        self.tod = tod
        self.T = OD.OTint(tod)
        self.layers = {}
        self.opts = {}
        self.key = f"{self.name}{self.p1v}"
        self.build()

    THRONE_S = 1.35

    def _draw_main(self, fr, xa, xb):
        """Taht büyük (s=1,35: oturan figür ölçeğine uysun), baldaken daha yukarıda; palle yok."""
        c, T, P = fr.c, self.T, self.pal
        s = self.THRONE_S
        OD.floor_tiles(c, xa, xb, OD.Y_FL, OD.LH, T, P["floor"][0], P["floor"][1], seed=4, w0=74.0, grow=1.13)
        if OD._vis(1700, 480, xa, xb):
            OD.rug(c, 1360, 2040, 752, 900, T, field=P["tap"][0], border="#C79A3C", inset=0.16)
            OD.draw_throne(c, T, 1700, 770, s)
            pel = skia.Path()
            pel.moveTo(1400, 60)
            pel.lineTo(2000, 60)
            n = 12
            for i in range(n + 1):
                xx = 2000 - 600 * i / n
                pel.lineTo(xx, 116)
                if i < n:
                    pel.quadTo(xx - 25, 150, xx - 50, 116)
            pel.close()
            OD.FILLP(c, pel, T("#8E1F26"), 255, 1.5, 200, shader=OD.LGP((0, 60), (0, 150), [(T("#6A1018"), 0.0), (T("#A82A30"), 1.0)]))
            OD.BOX(c, 1390, 40, 2010, 64, "#C79A3C", T, hl=0.22, sh=0.22, ink=1.5)
        for x in (700, 2700):
            if OD._vis(x, 100, xa, xb):
                OD.chair_back(c, T, x, 730, 72, 230, cushion=P["seat"])

    def seat_xy(self):
        """Tahtta oturan figür için ayak noktası (ana düzlem) ve önerilen boy."""
        s = self.THRONE_S
        return 1700, 770 - 60 * s, 282 * (55 * s) / 74


class P1Yatak(OD.Oda1743):
    """Ölüm döşeği odası (Oda1743 yerleşimi; arma/goblen YOK, koyu yeşil örtü, sade duvar). Yalnız siluet; figure='lying'."""
    name = "p1yatak"

    def __init__(self, variant, tod):
        self.p1v = variant or "olum"
        self.variant = self.p1v
        self.tod = tod
        self.T = OD.OTint(tod)
        self.layers = {}
        self.opts = {}
        self.key = f"{self.name}{self.p1v}"
        self.build()

    def _draw_wall(self, fr, xa, xb):
        c, T = fr.c, self.T
        night = self.tod == "night"
        wx = self.wx
        OD.plaster(c, xa, xb, OD.OV - 40, OD.Y_FL + 30, T, "#C2B08A", "#D2C29E", amp=0.05)
        OD.cornice(c, xa, xb, 72, T)
        OD.wainscot(c, xa, xb, OD.Y_FL - 150, OD.Y_FL + 18, T, "#6E4A30", seed=5)
        if OD._vis(wx(430), 360, xa, xb):
            OD.draw_hanging(c, T, wx(110), wx(760), 205, 548, "#2E4A3A", "#C9A45A", seed=7)
        if OD._vis(wx(1010), 120, xa, xb):
            OD.draw_window(c, T, wx(1010), 215, 190, 330, night=night)
        if OD._vis(wx(1660), 80, xa, xb):
            OD.sconce(c, T, wx(1660), 300, 1.1, 1)
        if OD._vis(wx(2400), 70, xa, xb):
            OD.draw_crucifix(c, T, wx(2400), 250, 1.0)
        sh = OD.LGP((0, OD.Y_FL - 30), (0, OD.Y_FL + 30), [("#1A0F06", 0.0, 0), ("#1A0F06", 1.0, 70)])
        c.drawRect(skia.Rect.MakeLTRB(xa, OD.Y_FL - 30, xb, OD.Y_FL + 30), sh)

    def _draw_main(self, fr, xa, xb):
        c, T = fr.c, self.T
        OD.floor_tiles(c, xa, xb, OD.Y_FL, OD.LH, T, "#9A6A48", "#8A5C3E", seed=6)
        if OD._vis(430, 330, xa, xb):
            self.pillow = OD.draw_bed(c, T, self.BX0, self.BYB, 560, 500, 190, cover=("#2E4A3A", "#C9A45A"))
        if OD._vis(1010, 150, xa, xb):
            OD.draw_chest(c, T, 880, 1140, 772, 118)
        if OD._vis(self.CHAIR_X, 70, xa, xb):
            OD.draw_chair(c, T, self.CHAIR_X, self.FIG_Y, 270, 74, 92, facing=1)


def _alcove_flat(c, T, x, y0, w, h, seed=1, rows=3):
    """Kemerli raf nişi — 1397–1430 için YATIK defter yığınları (sırt dışarı dizme 16. yy; kurul SA2-K5) + birkaç rulo."""
    x0, x1 = x - w / 2, x + w / 2
    r = w / 2
    yb = y0 + h
    p = skia.Path()
    p.moveTo(x0 - 16, yb + 4)
    p.lineTo(x0 - 16, y0 + r)
    p.arcTo(skia.Rect.MakeLTRB(x0 - 16, y0 - 16, x1 + 16, y0 + 2 * r + 16), 180, 180, False)
    p.lineTo(x1 + 16, yb + 4)
    p.close()
    OD.FILLP(c, p, T(mix("#C9B994", "#FFFFFF", 0.12)), 255, 1.6, 200)
    q = skia.Path()
    q.moveTo(x0, yb)
    q.lineTo(x0, y0 + r)
    q.arcTo(skia.Rect.MakeLTRB(x0, y0, x1, y0 + 2 * r), 180, 180, False)
    q.lineTo(x1, yb)
    q.close()
    c.drawPath(q, OD.LGP((0, y0), (0, yb), [("#2A1C12", 0.0), ("#4A3220", 1.0)]))
    c.save()
    c.clipPath(q, skia.ClipOp.kIntersect, True)
    rs = OD._RS(seed * 53)
    sh_h = (h - r * 0.55) / rows
    cols_b = ["#6A2E24", "#233C8C", "#2E5A3A", "#8A5A2A", "#3A2A44", "#7A2E2A", "#E4D8B8"]
    for ri in range(rows):
        ys = y0 + r * 0.55 + (ri + 1) * sh_h
        OD.R(c, x0, ys - 6, x1, ys + 2, T("#6E4524"))
        xx = x0 + 12
        while xx < x1 - 60:
            bw = rs.uniform(56, 92)
            n = 2 + int(rs.uniform(0, 3.99))
            for k in range(n):
                OD.draw_book(c, xx + bw / 2 + (k % 2) * 2, ys - 13 - k * 13, bw, 12, cols_b[int(rs.uniform(0, 6.99))])
            xx += bw + rs.uniform(10, 22)
    c.restore()


class P1Banka(OD.Banka):
    """Banka salonu; 0. masadaki (köşe) yazan bankacı = GIOVANNI (kit seed 5) — c1 sonu / c2 başı aynı kişi.
    Raf nişlerinde YATIK defter yığınları (kurul SA2-K5: 1397–1402'de sırt dışarı dizme yok)."""
    name = "p1banka"
    ST = [dict(x=330, act="write", seed=5), dict(x=1010, act="count", seed=8), dict(x=1690, act="write", seed=12), dict(x=2370, act="count", seed=17)]

    def _draw_wall(self, fr, xa, xb):
        c, T = fr.c, self.T
        night = self.tod == "night"
        wx = self.wx
        OD.GRAD_V(c, xa, OD.OV - 40, xb, OD.Y_FL + 30, [(T("#BFB090"), 0.0), (T("#D2C4A2"), 1.0)])
        OD.ashlar(c, xa, xb, OD.OV - 40, OD.Y_FL + 30, T, "#CFC09C", 64.0, seed=2)
        OD.cornice(c, xa, xb, 72, T, col="#8A7650", plaster="#D8CBA8")
        for i in range(5):
            x = 330 + 600 * i
            if OD._vis(wx(x), 200, xa, xb):
                _alcove_flat(c, T, wx(x), 250, 320, 340, seed=i + 1, rows=3)
        for i in range(4):
            x = 630 + 600 * i
            if OD._vis(wx(x), 100, xa, xb):
                OD.draw_window(c, T, wx(x), 150, 110, 250, night=night, shutters=False, mullion=True)
        OD.wainscot(c, xa, xb, OD.Y_FL - 70, OD.Y_FL + 18, T, "#7A5A3A", pw=190, seed=4)
        sh = OD.LGP((0, OD.Y_FL - 30), (0, OD.Y_FL + 30), [("#1A0F06", 0.0, 0), ("#1A0F06", 1.0, 70)])
        c.drawRect(skia.Rect.MakeLTRB(xa, OD.Y_FL - 30, xb, OD.Y_FL + 30), sh)


OD.ROOMS["p1banka"] = P1Banka
OD.ROOMS["p1ofis"] = P1Ofis
OD.ROOMS["p1salon"] = P1Salon
OD.ROOMS["p1yatak"] = P1Yatak


@_icons.icon("p1_tiara")
def _i_tiara(m):
    """Papalık tacı (üç katlı, kovan biçimli) + üstte küre-haç."""
    m.smooth([(150, 450), (160, 300), (190, 190), (256, 120), (322, 190), (352, 300), (362, 450)], close=True, t=0.22)
    for yy in (420, 330, 240):
        m.cut(sk.poly_path([(150, yy), (362, yy)], False), 9)
    m.circle(256, 100, 22)
    m.rect(250, 40, 12, 52, r=3)
    m.rect(234, 56, 44, 10, r=3)


@_icons.icon("p1_kese")
def _i_kese(m):
    """Bağcıklı para kesesi (deri)."""
    m.smooth([(256, 170), (360, 230), (410, 360), (360, 450), (256, 470), (152, 450), (102, 360), (152, 230)], close=True, t=0.28)
    m.smooth([(206, 170), (232, 110), (256, 96), (280, 110), (306, 170)], close=True, t=0.3)
    m.cut(sk.poly_path([(196, 176), (316, 176)], False), 10)


@_icons.icon("p1_anahtar")
def _i_anahtar(m):
    """Papalık anahtarları (çapraz): halka (bow) AŞAĞIDA, diş (ward) YUKARIDA — kurul SA2-K4."""
    for ang in (-32, 32):
        m.c.save()
        m.c.translate(256, 256)
        m.c.rotate(ang)
        m.c.translate(-256, -256)
        r = skia.Path(); r.addCircle(256, 392, 62)
        m.stroke(r, 30)
        m.rect(242, 72, 28, 270, r=6)
        m.rect(270, 108, 60, 24)
        m.rect(270, 70, 44, 22)
        m.c.restore()



def candle_ovl(x, y, h=110, snuff_at=None, seed=1.3, lit=1.0):
    """Ekran uzayında mum (alev titrer; snuff_at'ta söner, ince duman). Ölüm anının yalnız SEMBOLÜ — saat/tanık iddiası değil."""
    def fn(cx):
        k = lit
        if snuff_at is not None:
            k *= 1.0 - cx.amt(snuff_at, 0.45)
        OD.candle(cx.f, x, y, h, cx.t, seed, lit=k, holder=True, smoke=True, halo=1.0)
    return fn


# ───────────────────────────── kurul tur 1: 1737 Vasari koridoru — yürüyenler SİLUET (Quattrocento kostümü 1737'de yanlış; KA1-V2, SA1-K2) ─────────────────────────────
import cilt_pano as _PN


class P1Corridor(_PN.Corridor):
    name = "p1corridor"

    def dyn_people(self, ctx):
        f, t = ctx.f, ctx.t
        xa, xb = ctx.xa, ctx.xb
        vis = [p for p in self.people if xa - 240 < p["x0"] + (0 if p["idle"] else p["dir"] * p["w"] * t) < xb + 240]
        vis.sort(key=lambda p: p["y"])
        for p in vis:
            if p["idle"]:
                OD.sil_actor(f, p["kind"], p["x0"], p["y"], p["h"], t, action="talk", dir=p["dir"], seed=p["seed"], phase=p["phase"], color="#2A1E16", rim="#E8B070", rim_dir=p["dir"])
            else:
                x = p["x0"] + p["dir"] * p["w"] * t
                OD.sil_actor(f, p["kind"], x, p["y"], p["h"], t, dir=p["dir"], seed=p["seed"], phase=p["phase"], color="#2A1E16", rim="#E8B070", rim_dir=p["dir"], walker=p["w"])


_PN.WORLDS["p1corridor"] = P1Corridor


def seal_drop(x, y, at, r=120, label=None, label_size=44, out=None, col="#A52A1C"):
    """Balmumu mühür (palle) `at`'ta yukarıdan düşer, oturur (anim.settle), halka dalgası; altında koyu levhalı etiket. Ekran uzayı."""
    import anim

    def fn(cx):
        f = cx.f
        t_at = cx.at(at)
        k = clamp((cx.t - (t_at - 0.25)) / 0.25)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k <= 0.003:
            return
        e = anim.settle(cx.t, t_at - 0.25, 0.45, 0.10)
        yy = y - 240 * (1.0 - e)
        f.circle(x + 8, y + r * 0.9, r * 0.9, color="#000000", alpha=0.25 * k * e, blur=10)
        CM.wax_seal(f, x, yy, r, col, alpha=k, t=1.0, palle=True)
        if cx.t >= t_at:
            ph = clamp((cx.t - t_at) / 0.8)
            if ph < 1.0:
                f.circle(x, y, r * (1.05 + 0.8 * ph), style="stroke", sw=4, color="#E8C468", alpha=0.6 * (1 - ph))
        if label:
            kl = clamp((cx.t - t_at - 0.15) / 0.35) * k
            if kl > 0.003:
                wd = sk.text_width(label, "title_m", label_size, 8) + 56
                ly = y + r + 74
                f.rrect(x - wd / 2, ly - label_size - 4, wd, label_size + 30, 10, color="#120C08", alpha=0.78 * kl)
                CM.ink(f, label, x, ly, face="title_m", size=label_size, color="#FFF4D6", align="c", track=8, alpha=kl, emboss=False)
    return fn


# ───────────────────────────── yol haritası çipleri (kurul PK2-K7) ─────────────────────────────
ROADMAP_C1 = [("coin", "ALTIN"), ("book", "HESAP"), ("hourglass", "VEBA"), ("torch", "ÖFKE"), ("coinbag", "ASIL HİKÂYE: MEDİCİ")]


def roadmap(steps, items=None, x=72, y=96, dur=3.6):
    """Sol üst sessiz yol haritası: steps=[(çapa, i)] — her adımda şerit `dur` sn görünür; geçmiş adımlar soluk yaldız, etkin adım parlak + etiket,
    gelecek adımlar boş halka. Bölüm başı etiketi (y 28–82) altında; HUD'dan uzak. Ekran uzayı (ovl)."""
    import icons
    items = items or ROADMAP_C1

    def fn(cx):
        f = cx.f
        act = None
        for (an, i) in steps:
            t0 = cx.at(an)
            if t0 - 0.35 <= cx.t <= t0 + dur:
                act = (t0, i)
        if act is None:
            return
        t0, i = act
        a = smooth((cx.t - t0 + 0.35) / 0.35) * (1.0 - smooth((cx.t - t0 - dur + 0.4) / 0.4))
        if a <= 0.003:
            return
        n = len(items)
        gap, r = 62.0, 23.0
        lab = items[i][1]
        lsz = 34
        lw = sk.text_width(lab, "title_m", lsz, 5)
        wd = 30 + gap * (n - 1) + 2 * r + 28 + lw + 26
        hh = 66.0
        f.rrect(x + 3, y + 6, wd, hh, 12, color="#000000", alpha=0.35 * a, blur=6)
        f.rrect(x, y, wd, hh, 12, shader=f.lin(x, y, x, y + hh, [("#1E3282", 0.0), ("#0F1B52", 1.0)]), alpha=0.94 * a)
        f.rrect(x, y, wd, hh, 12, style="stroke", sw=1.8, color="#D8B25A", alpha=0.9 * a)
        cy = y + hh / 2
        x0 = x + 30 + r
        f.line(x0, cy, x0 + gap * (n - 1), cy, color="#D8B25A", sw=2.0, alpha=0.45 * a)
        for j, (ic, _l) in enumerate(items):
            px = x0 + gap * j
            if j < i:
                f.circle(px, cy, r, color="#3A3A5A", alpha=0.95 * a)
                icons.draw_icon(f, ic, px, cy, size=r * 1.5, metal="gold", alpha=0.55 * a, glow=0.0, shadow=False)
            elif j == i:
                pulse = 0.5 + 0.5 * math.sin((cx.t - t0) * 5.0)
                f.circle(px, cy, r + 10 + 4 * pulse, color="#F6D886", alpha=0.25 * a)
                f.circle(px, cy, r + 2, color="#F6D886", alpha=a)
                icons.draw_icon(f, ic, px, cy, size=r * 1.6, metal="bronze", alpha=a, glow=0.0, shadow=False)
            else:
                f.circle(px, cy, r - 2, style="stroke", sw=2.4, color="#C9A45A", alpha=0.7 * a)
        CM.ink(f, lab, x0 + gap * (n - 1) + r + 28, cy + lsz * 0.36, face="title_m", size=lsz, color="#F6E3A8", align="l", track=5, alpha=a, emboss=False, scrim=False)
    return fn


def with_ovl(shots, extra, kinds_prefix=("p1_", "c0_", "c1_", "c2_")):
    """Listeye toplu ovl ekler (ör. yol haritası): yalnız ovl destekleyen türler (p1_/cK_ sarmalayıcıları)."""
    for s in shots:
        if not s.kind.startswith(kinds_prefix):
            continue
        o = s.params.get("ovl")
        s.params["ovl"] = ov(o, extra) if o else extra
    return shots
