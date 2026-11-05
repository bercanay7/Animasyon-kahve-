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

# ── harita sarmalayıcısı: ROTA UCUNU İZLEYEN KAMERA (ENG-D, kurul tur 2 AN1-Y2) ─────────────────────────────
# p1_map çekimlerinde kamera, çizilmekte olan rotanın ucunu izler: rota ucunun dünya yolunun MAP_FOLLOW kadarı kadar harita merkezi kayar
# (rota başladığında hızı 0, rota bittiğinde orada kalır; birden çok rota toplanır — gidiş-dönüşte kamera da gider ve döner). Ekrandaki kayma
# yumuşak sınırla en çok MAP_FOLLOW_MAX·genişlik. Beyan edilen cam= (push/pull/pan) ve sahnenin cams= anahtar kareleri aynen üstüne biner.
# KADRAJ KORUMASI: başlamış rotaların noktaları (kentler: rotanın başı/ara/sonu) izleme yüzünden güvenli alanın (MAP_KEEP kenar payları) dışına
# itilemez; nokta sahnenin kendi kamerasında zaten pay dışındaysa izleme onu daha da dışarı itemez (ör. #63 kur farkı: BRUGGE üst kenarda).
MAP_FOLLOW = 0.34
MAP_FOLLOW_MAX = 0.14
MAP_KEEP = (170.0, 160.0, 330.0, 190.0)       # sol, üst, sağ (kent adı sağa yazılır), alt — px
_RT = {}


def _route_world(pts):
    """Rota (lon,lat) noktaları → dünya pikselinde mapsk.route ile aynı yumuşak eğri (benzerlik dönüşümüne göre eşdeğer) → (PathMeasure, uzunluk). Önbellekli."""
    key = tuple((float(a), float(b)) for a, b in pts)
    v = _RT.get(key)
    if v is None:
        import mapdata
        wp = [mapdata.to_world(a, b) for a, b in key]
        path = sk.smooth_path(wp, close=False, tension=0.5) if len(wp) > 2 else sk.poly_path(wp, close=False)
        pm = skia.PathMeasure(path, False)
        v = _RT[key] = (pm, pm.getLength())
    return v


def map_follow(cx, routes):
    """Rotaların çizim ilerlemesine göre izleme kayması (dünya pikseli) ve kadrajda tutulacak noktalar.
    Dönüş: ((dx, dy) = Σ (uç(ilerleme) − uç(0))·MAP_FOLLOW, [başlamış rotaların dünya noktaları])."""
    import mapdata
    fx = fy = 0.0
    keep = []
    for r in routes or ():
        pts = r.get("pts")
        if not pts or len(pts) < 2:
            continue
        try:
            t0 = cx.at(r.get("at", 0.0))
        except Exception:
            continue
        pr = ease_io(clamp((cx.t - t0) / max(1e-3, float(r.get("dur", 1.8)))))
        if pr <= 0.0:
            continue
        pm, L = _route_world(pts)
        p0, _ = pm.getPosTan(0.0)
        p1, _ = pm.getPosTan(L * pr)
        fx += (p1.x() - p0.x()) * MAP_FOLLOW
        fy += (p1.y() - p0.y()) * MAP_FOLLOW
        keep += [mapdata.to_world(float(a), float(b)) for a, b in pts]
    return (fx, fy), keep


class _follow_patch:
    """mapsk.Cam'e rota izleme kaymasını ekler (iç map türünün cilt_cam.map_patch'i bunun ÜSTÜNE kurulur: beyan edilen kamera da uygulanır).
    Kadraj koruması: izleme, `keep` noktalarını güvenli alanın (MAP_KEEP) dışına itmez (zaten dışındaysa daha da dışarı itmez)."""

    def __init__(self, fk):
        self.fw, self.keep = fk

    def __enter__(self):
        import mapsk
        self.orig = mapsk.Cam
        fwx, fwy = self.fw
        keep = list(self.keep)
        lim = MAP_FOLLOW_MAX * W
        ml, mt, mr, mb = MAP_KEEP

        class _Cam(self.orig):
            def __init__(s_, lon, lat, zoom, rot=0.0, cx=W / 2, cy=H / 2):
                super().__init__(lon, lat, zoom, rot, cx, cy)
                z = max(1e-6, s_.zoom)
                m = math.hypot(fwx, fwy) * z                         # ekrandaki kayma (px) → yumuşak sınır
                k_ = (lim * math.tanh(m / lim) / m) if m > 1e-6 else 1.0
                fx, fy = fwx * k_, fwy * k_
                lo_x = lo_y = -1e9
                hi_x = hi_y = 1e9
                for (px_, py_) in keep:                             # ekran x(F) = x0 − F·z: payın dışına itme yok
                    x0, y0 = s_.cx + (px_ - s_.wx) * z, s_.cy + (py_ - s_.wy) * z
                    hi_x = min(hi_x, (x0 - min(x0, ml)) / z)
                    lo_x = max(lo_x, (x0 - max(x0, W - mr)) / z)
                    hi_y = min(hi_y, (y0 - min(y0, mt)) / z)
                    lo_y = max(lo_y, (y0 - max(y0, H - mb)) / z)
                s_.wx += min(max(fx, lo_x), hi_x)
                s_.wy += min(max(fy, lo_y), hi_y)
        mapsk.Cam = _Cam
        return self

    def __exit__(self, *exc):
        import mapsk
        mapsk.Cam = self.orig
        return False


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
        if inner == "map":                                       # kadraj koruması: beyan edilen ön ayar rota/kent noktalarını payın dışına itemez
            import mapdata
            cx._map_keep = ([mapdata.to_world(float(a), float(b)) for r in (kw.get("routes") or ()) for a, b in (r.get("pts") or ())] +
                            [mapdata.to_world(float(c_["lon"]), float(c_["lat"])) for c_ in (kw.get("cities") or ()) if "lon" in c_ and "lat" in c_])
        if inner == "map" and kw.get("routes") and MAP_FOLLOW > 0:   # harita: kamera çizilen rotanın ucunu izler
            with _follow_patch(map_follow(cx, kw["routes"])):
                SH.KINDS[inner](cx, **kw)
        else:
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


def count_up(x, y, at, value, dur=1.4, unit=None, size=150, face="title", color=None, prefix="", suffix="", unit_size=44, shadow=True, align="c", fmt=None, out=None, bg=False, min_w=420,
             step=None, suffix_final=False, count=True):
    """Sayı sayar (0→value, ease_out). Büyük Cinzel; altında birim. Yaldız (gece) / oyma (gündüz).
    Kurul tur 2 (KA2-D10, AN2-K4): step → ara değerler yuvarlak adımla (ör. 5.000; "143.194" gibi kesin görünen ara sayı yok) ·
    suffix_final → sonek ("+") yalnız son değerde · count=False → sayma yok, değer doğrudan (yalnız belirme)."""
    def fn(cx):
        k0 = cx.amt(at, 0.35)
        if out is not None:
            k0 *= 1.0 - cx.amt(out, 0.4)
        if k0 <= 0.003:
            return
        k = ease_out(clamp((cx.t - cx.at(at)) / dur), 3) if count else 1.0
        v = value * k
        if step and k < 0.999:
            v = math.floor(v / step) * step
        s = (fmt(v) if fmt else CM.fmt_int(v))
        txt = prefix + s + (suffix if (not suffix_final or k >= 0.999) else "")
        sz = CM.fit_size(txt, face, size, 1500, 6)
        sp = CM.gilt(txt, face, int(sz), 6.0) if not TH.day else CM.engraved(txt, face, int(sz), 6.0, color or TH.fg)
        if bg:
            wd = max(sk.text_width(txt, face, sz, 6.0), min_w) + 120
            hh_ = sz * 0.95 + (unit_size * 1.7 if unit else 40) + 40
            CM.tablet(cx.f, x - wd / 2, y - sz * 0.80, wd, hh_, alpha=0.93 * k0, corner=14)
        CM.draw_spr(cx.f, sp, x, y, "c" if align == "c" else "l", alpha=k0, shadow=0.5 if shadow and not TH.day else 0.0)
        if CM.LOG_TEXT:                                   # qa_yerlesim: büyük sayının ekran kutusu (yazı–yazı çakışma denetimi; kurul tur 2 SA1-Y2)
            x0_ = x - sp.wid / 2 if align == "c" else x
            CM._log_text(cx.f, "sayi", txt, x0_, y - sz * 0.80, x0_ + sp.wid, y + sz * 0.06, sz, k0)
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
        if callable(icon):                                  # çizim işlevi (ör. tiara_draw: iki renkli nesne)
            icon(cx.f, x, y + bob, size, k, r)
        else:
            icons.draw_icon(cx.f, icon, x, y + bob, size=size, metal=metal, alpha=k, rot=r, glow=0.0)
    return fn


def tiara_draw(f, x, y, size, alpha=1.0, rot=0.0):
    """Papalık tacı (triregnum) — kurul tur 2 SA2-Y7: Martinus'unki gibi BEYAZ kovan gövde + üç ALTIN taç halkası + tepede küre-haç
    (figür kitindeki 'tiara' başlığıyla aynı biçim dili). x,y merkez; size ≈ yükseklik."""
    if alpha <= 0.003:
        return
    c = f.c
    s = size / 2.0
    c.save()
    c.translate(x, y)
    if rot:
        c.rotate(math.degrees(rot))
    ink_ = "#2A1A0C"
    body = sk.smooth_path([(-0.62 * s, 0.70 * s), (-0.66 * s, 0.18 * s), (-0.50 * s, -0.42 * s), (-0.18 * s, -0.86 * s), (0.18 * s, -0.86 * s), (0.50 * s, -0.42 * s),
                           (0.66 * s, 0.18 * s), (0.62 * s, 0.70 * s), (0.0, 0.78 * s)], True, 0.45)
    f.path(body, color="#000000", alpha=0.22 * alpha, blur=6)
    f.path(body, shader=f.lin(-0.6 * s, 0, 0.6 * s, 0, [("#FBF6E8", 0.0), ("#EDE4CC", 0.55), ("#C9BFA4", 1.0)]), alpha=alpha)
    f.path(body, style="stroke", sw=max(1.6, size / 90), color=ink_, alpha=0.9 * alpha)
    for (yy, wd) in ((0.52, 0.64), (0.04, 0.60), (-0.44, 0.46)):          # üç taç: altın bant + diş sırası
        band = sk.smooth_path([(-wd * s, yy * s), (0.0, (yy + 0.07) * s), (wd * s, yy * s), (wd * 0.98 * s, (yy - 0.13) * s), (0.0, (yy - 0.06) * s), (-wd * 0.98 * s, (yy - 0.13) * s)], True, 0.35)
        f.path(band, shader=f.lin(0, (yy - 0.13) * s, 0, (yy + 0.07) * s, [("#F6DC8C", 0.0), ("#C9A23A", 0.6), ("#8A6620", 1.0)]), alpha=alpha)
        f.path(band, style="stroke", sw=max(1.2, size / 130), color=ink_, alpha=0.85 * alpha)
        for i in range(-3, 4):
            px = i * wd * 0.27 * s
            f.circle(px, (yy - 0.16) * s + abs(i) * 0.012 * s, 0.045 * s, color="#E8C25A", alpha=alpha)
    f.circle(0, -0.95 * s, 0.10 * s, shader=f.rad(-0.03 * s, -0.98 * s, 0.14 * s, [("#FBE9A6", 0.0), ("#B8862E", 1.0)]), alpha=alpha)
    f.circle(0, -0.95 * s, 0.10 * s, style="stroke", sw=1.2, color=ink_, alpha=0.8 * alpha)
    f.rect(-0.022 * s, -1.22 * s, 0.044 * s, 0.20 * s, color="#C9A23A", alpha=alpha)
    f.rect(-0.08 * s, -1.15 * s, 0.16 * s, 0.04 * s, color="#C9A23A", alpha=alpha)
    c.restore()


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


def lily_path(x, y, s):
    """Küçük zambak (fleur-de-lis) yolu: orta yaprak, iki kıvrık yan yaprak, bağ ve kısa sap. (x,y) = bağın ortası; s ≈ yükseklik."""
    p = skia.Path()
    p.moveTo(x, y - 0.62 * s)
    p.cubicTo(x + 0.16 * s, y - 0.40 * s, x + 0.13 * s, y - 0.12 * s, x + 0.05 * s, y)
    p.lineTo(x - 0.05 * s, y)
    p.cubicTo(x - 0.13 * s, y - 0.12 * s, x - 0.16 * s, y - 0.40 * s, x, y - 0.62 * s)
    p.close()
    for sg in (-1, 1):
        q = skia.Path()
        q.moveTo(x + sg * 0.06 * s, y - 0.02 * s)
        q.cubicTo(x + sg * 0.20 * s, y - 0.34 * s, x + sg * 0.46 * s, y - 0.34 * s, x + sg * 0.44 * s, y - 0.10 * s)
        q.cubicTo(x + sg * 0.42 * s, y + 0.02 * s, x + sg * 0.30 * s, y + 0.02 * s, x + sg * 0.30 * s, y - 0.08 * s)
        q.cubicTo(x + sg * 0.26 * s, y - 0.02 * s, x + sg * 0.16 * s, y + 0.02 * s, x + sg * 0.06 * s, y + 0.04 * s)
        q.close()
        p.addPath(q)
    p.addRect(skia.Rect.MakeLTRB(x - 0.24 * s, y - 0.01 * s, x + 0.24 * s, y + 0.07 * s))
    p.addRect(skia.Rect.MakeLTRB(x - 0.05 * s, y + 0.07 * s, x + 0.05 * s, y + 0.30 * s))
    return p


def palle_relief(f, x, y, s, variant="std", color="#A52A1C", alpha=1.0):
    """Balmumu üstünde KABARTMA palle (tek renk): her top üst-sol ışıklı, alt-sağ gölgeli. variant 'std' (≥1465: üstte büyük top + ÜÇ ZAMBAK kabartması,
    5 top) | 'red8' (≤1464: 8 top kenar boyunca). Geometri CM.mini_palle ile aynı (s = mühür yarıçapı × 1,05)."""
    pos = CM.PALLE_POS if variant == "std" else CM.PALLE_POS_RED8
    dark, lite = mix(color, "#000000", 0.50), mix(color, "#FFFFFF", 0.30)
    for i, (dx, dy, rr) in enumerate(pos):
        px, py = x + (dx - 0.5) * s * 0.78, y + (dy - 0.52) * s * 0.78
        R = rr * s * 0.78
        f.circle(px + R * 0.10, py + R * 0.12, R, color=dark, alpha=0.85 * alpha)
        f.circle(px, py, R, shader=f.rad(px - R * 0.35, py - R * 0.40, R * 1.6, [(lite, 0.0), (color, 0.55), (mix(color, "#000000", 0.30), 1.0)]), alpha=alpha)
        f.circle(px, py, R, style="stroke", sw=max(1.0, R * 0.08), color=dark, alpha=0.7 * alpha)
        if variant == "std" and i == 0:                       # üst top: Fransa zambakları (XI. Louis, 1465) — tek renk balmumunda kabartma
            for (lx, ly) in ((-0.36, -0.10), (0.36, -0.10), (0.0, 0.42)):
                lp = lily_path(px + lx * R, py + ly * R, R * 0.62)
                f.c.save(); f.c.translate(R * 0.05, R * 0.06)
                f.c.drawPath(lp, f.paint(dark, alpha=0.75 * alpha))
                f.c.restore()
                f.c.drawPath(lp, f.paint(lite, alpha=0.95 * alpha))


def nesne_yili(y, kind=None):
    """NESNE YILI bağlamı (kurul tur 2 SA2-Y4): sahnede HUD yılından FARKLI bir yıla ait nesne (ör. 1429 sahnesinde 1520 siparişinin mührü).
    `with nesne_yili(1520): ...` — resmî API'ye devreder (donem.nesne_yili). Eski yerel çözüm çıkışta donem.pop() ile 'son bağlam'ı iç çerçeveye
    çeviriyordu; ekran kaplamasında kullanılınca aynı karede sonra çizilen katmanlar 1520'yi görüyordu (SCN-1 bulgusu). Resmî API yığını ve
    'son bağlam'ı girişteki hâline döndürür."""
    import donem as DN
    return DN.nesne_yili(y, kind)


def seal_drop(x, y, at, r=120, label=None, label_size=44, out=None, col="#A52A1C", variant=None, year=None):
    """Balmumu mühür (palle) `at`'ta yukarıdan düşer, oturur (anim.settle), halka dalgası; altında koyu levhalı etiket. Ekran uzayı.
    Kurul tur 2 (SA2-Y4/KA1-Ö3): `year` = NESNE YILI (ör. 1520, Machiavelli siparişi) — arma HUD yılına değil o yıla göre çizilir ve dönem kaydına
    o yılla yazılır (nesne_yili); `variant` açık verilirse ('std' | 'red8') o kullanılır. Palle tek renk KABARTMA (std: üst topta üç zambak)."""
    import anim
    import contextlib
    import donem as DN

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
        with (nesne_yili(year) if year is not None else contextlib.nullcontext()):
            v = variant or DN.arms_variant()
            CM.wax_seal(f, x, yy, r, col, alpha=k, t=1.0, palle=False)
            palle_relief(f, x, yy, r * 1.05, v, mix(col, "#000000", 0.18), alpha=0.95 * k)
            DN.note_once_per_frame("arms", where="muhur", variant=v, blue=False, mono=True, nesne_yili=year)
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


# ═════════════════════════════ kurul tur 2 (SCN-2): YER BAŞINA SET FARKI ═════════════════════════════
# AN2-Ö3 / SA1 §6 / SA2 §4 / KA1: 'salon/napoli' üç ayrı yeri (Roma bankası, Brugge, kâtip) oynuyordu; Medici ağaçlı goblen papalık ve Konstanz
# salonlarında da asılıydı. Her yer kendi duvarı, penceresi, mobilyası ve ışığıyla ayrışır (cilt_oda.SALON_HOOKS kancaları; önbellek anahtarı = varyant adı).
STK, PT, FILLP, BOX, LGP, SOFT, HGRAD = OD.STK, OD.PT, OD.FILLP, OD.BOX, OD.LGP, OD.SOFT, OD.HGRAD


def icon_tint(f, name, x, y, size, col, alpha=1.0, metal="silver", rot=0.0):
    """Simgeyi kabartmasını koruyarak tek renge boya (ör. altın zemin üstünde SİYAH imparatorluk kartalı)."""
    img = _icons.icon_image(name, metal, 512)
    s = size / 512.0
    p = skia.Paint(AntiAlias=True)
    p.setColorFilter(skia.ColorFilters.Blend(sk.C(col), skia.BlendMode.kModulate))
    p.setAlphaf(max(0.0, min(1.0, alpha)))
    f.c.save()
    f.c.translate(x, y)
    if rot:
        f.c.rotate(math.degrees(rot))
    f.c.scale(s, s)
    f.c.drawImage(img, -256, -256, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    f.c.restore()


def _beams(c, T, xa, xb, y0=60, y1=118, col="#3A2C20", step=120):
    """Ahşap kirişli tavan kuşağı (Flaman evi): koyu kiriş + kiriş başları."""
    OD.R(c, xa, y0, xb, y1, T(col))
    c.drawLine(xa, y1, xb, y1, STK(OD.INK, 1.6, 210, False))
    i0 = int(math.floor(xa / step)) - 1
    for i in range(i0, int(math.ceil(xb / step)) + 2):
        x = i * step
        BOX(c, x - 16, y1 - 6, x + 16, y1 + 22, mix(col, "#000000", 0.1), T, hl=0.18, sh=0.25, ink=1.2)


def _flemish_window(c, T, x, y, w, h, night=False, seed=1):
    """Flaman haç kasalı pencere (kruiskozijn): dikdörtgen koyu meşe kasa; üst camlar yuvarlak 'göz' camlı, alt kanatlar açık → kanal,
    basamaklı çatılı (trapgevel) tuğla evler, soğuk kuzey göğü. (x orta, y üst)"""
    x0, x1, yb = x - w / 2, x + w / 2, y + h
    SOFT(c, x + 10, yb + 22, w * 0.9, 16, "#000000", 70)
    BOX(c, x0 - 22, y - 22, x1 + 22, yb + 22, "#3A2E24", T, hl=0.14, sh=0.24, ink=1.6)
    op = skia.Path(); op.addRect(skia.Rect.MakeLTRB(x0, y, x1, yb))
    c.save()
    c.clipPath(op, skia.ClipOp.kIntersect, True)
    sky = ("#B9C9D6", "#E4EAEC") if not night else ("#1A2440", "#2A3658")
    OD.GRAD_V(c, x0, y, x1, yb, [(sky[0], 0.0), (sky[1], 0.62)])
    rs = OD._RS(seed * 17 + 3)
    wl = yb - h * 0.20                                      # kanal su çizgisi
    xx = x0 - 20
    k = 0
    while xx < x1 + 10:                                     # basamaklı alınlıklı evler
        bw = rs.uniform(w * 0.28, w * 0.40)
        bh = rs.uniform(h * 0.28, h * 0.42)
        col = ["#8A4A34", "#7A3E2E", "#9A6A4A", "#6E3A2A"][k % 4]
        top = wl - bh
        steps = 3
        pts = [(xx, wl), (xx, top)]
        for sidx in range(steps):
            sx = xx + bw * (sidx + 1) / (2 * steps + 1)
            pts += [(sx, top - bh * 0.12 * sidx), (sx, top - bh * 0.12 * (sidx + 1))]
        pk = top - bh * 0.12 * (steps + 0.4)
        pts += [(xx + bw / 2 - 4, pk), (xx + bw / 2 + 4, pk)]
        for sidx in range(steps, 0, -1):
            sx = xx + bw - bw * sidx / (2 * steps + 1)
            pts += [(sx, top - bh * 0.12 * sidx), (sx, top - bh * 0.12 * (sidx - 1))]
        pts += [(xx + bw, top), (xx + bw, wl)]
        pth = sk.poly_path(pts)
        c.drawPath(pth, PT(T(col) if not night else mix(col, "#0A1020", 0.6)))
        c.drawPath(pth, STK(OD.INK, 1.0, 150))
        for wy in (top + bh * 0.22, top + bh * 0.55):
            for wx_ in (xx + bw * 0.28, xx + bw * 0.62):
                OD.R(c, wx_, wy, wx_ + bw * 0.12, wy + bh * 0.16, "#E9E4D4" if not night else "#E8C470", 220)
        xx += bw + rs.uniform(-2, 4)
        k += 1
    OD.GRAD_V(c, x0, wl, x1, yb, [("#7E95A2" if not night else "#16203A", 0.0), ("#5C7482" if not night else "#0C1428", 1.0)])
    for i in range(5):                                      # su dalgası çizgileri
        yy = wl + 6 + i * (yb - wl) / 5.5
        c.drawLine(x0 + rs.uniform(4, 30), yy, x0 + rs.uniform(w * 0.4, w * 0.9), yy, STK("#E4EEF2", 1.1, 110, False))
    c.restore()
    # haç kasa (kalın meşe) + üst camlarda 'göz' camları
    yt = y + h * 0.40
    for (a0, b0, a1, b1) in ((x - 7, y, x + 7, yb), (x0, yt - 7, x1, yt + 7)):
        BOX(c, a0, b0, a1, b1, "#3A2E24", T, hl=0.12, sh=0.2, ink=1.2)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(x0, y, x1, yt - 7))
    r_ = 11.0
    yy = y + r_
    row = 0
    while yy < yt:
        xx = x0 + (row % 2) * r_
        while xx < x1 + r_:
            c.drawCircle(xx, yy, r_, STK("#5A5040", 1.2, 150))
            c.drawCircle(xx - 3, yy - 3, r_ * 0.35, PT("#FFFFFF", 60))
            xx += 2 * r_
        yy += r_ * 1.75
        row += 1
    c.restore()
    for sgn in (-1, 1):                                     # alt iç kanatlar: açık, koyu yeşil boyalı
        sx0 = x0 - 46 if sgn < 0 else x1 + 6
        BOX(c, sx0, yt + 4, sx0 + 40, yb, "#2E4A3A", T, hl=0.14, sh=0.22, ink=1.4)
    OD.INKR(c, x0, y, x1, yb, 2.0, 220)


def _convex_mirror(c, T, x, y, r):
    """Flaman dışbükey ayna (yuvarlak koyu çerçeve; içinde odanın bükülmüş yansısı: pencere parıltısı)."""
    SOFT(c, x + 6, y + 10, r * 1.2, r * 1.2, "#000000", 60)
    c.drawCircle(x, y, r + 18, PT(T("#3A2A1C")))
    c.drawCircle(x, y, r + 18, STK(OD.INK, 1.4, 200))
    for i in range(10):
        a = i * math.tau / 10
        c.drawCircle(x + math.cos(a) * (r + 9), y + math.sin(a) * (r + 9), 6.5, PT(T("#6A5038")))
        c.drawCircle(x + math.cos(a) * (r + 9), y + math.sin(a) * (r + 9), 6.5, STK(OD.INK, 0.9, 170))
    c.drawCircle(x, y, r, OD.LGP((x - r, y - r), (x + r, y + r), [("#DCE4E2", 0.0), ("#8A9A9C", 0.6), ("#4A5458", 1.0)]))
    c.drawCircle(x - r * 0.22, y - r * 0.30, r * 0.30, PT("#FFFFFF", 70))
    c.drawLine(x - r * 0.75, y + r * 0.10, x + r * 0.70, y + r * 0.18, STK("#3A3028", 1.6, 120))
    c.drawCircle(x, y, r, STK(OD.INK, 1.4, 200))


def _panel_painting(c, T, x, y0, w, h, seed=1, tone=("#3A4A3A", "#8A7A4A")):
    """Küçük çerçeveli pano resmi (adsız; kopya değil): koyu zemin, ufuk, iki ağaç lekesi."""
    OD.BOX(c, x - w / 2 - 16, y0 - 16, x + w / 2 + 16, y0 + h + 16, "#4A3220", T, hl=0.18, sh=0.24, ink=1.4)
    OD.GRAD_V(c, x - w / 2, y0, x + w / 2, y0 + h, [(T(tone[1]), 0.0), (T(tone[0]), 0.7)])
    rs = OD._RS(seed)
    for k in range(3):
        tx = x - w / 2 + rs.uniform(0.15, 0.85) * w
        OD.SOFT(c, tx, y0 + h * 0.55, w * 0.10, h * 0.16, "#2A3A26", 180)
    c.drawLine(x - w / 2, y0 + h * 0.62, x + w / 2, y0 + h * 0.62, STK("#C9B07A", 1.2, 120, False))
    OD.INKR(c, x - w / 2, y0, x + w / 2, y0 + h, 1.2, 200)


def _brugge_wall(room, fr, xa, xb):
    """BRUGGE (c2s3): soğuk badana, koyu meşe kiriş ve lambri, Flaman haç kasalı pencereler (kanal + basamaklı çatılar), dışbükey ayna, pano resimleri."""
    c, T = fr.c, room.T
    night = room.tod == "night"
    wx = room.wx
    OD.plaster(c, xa, xb, OD.OV - 40, OD.Y_FL + 30, T, "#D3D7D2", "#E5E8E3", amp=0.04, warm=(236, 242, 246), cool=(70, 78, 86))
    _beams(c, T, xa, xb, 54, 112, "#3A2C20", 128)
    OD.wainscot(c, xa, xb, OD.Y_FL - 150, OD.Y_FL + 18, T, "#3E3226", pw=150, seed=7)
    for i, x in enumerate(room.win_x):
        if OD._vis(wx(x), 140, xa, xb):
            _flemish_window(c, T, wx(x), 214, 190, 330, night=night, seed=i + 2)
    for i, x in enumerate(room.tap_x):
        if OD._vis(wx(x), 140, xa, xb):
            if i == 1:
                _convex_mirror(c, T, wx(x), 360, 70)
            else:
                _panel_painting(c, T, wx(x), 300, 150, 120, seed=i + 5)
    for x in (240, 3300):
        if OD._vis(wx(x), 150, xa, xb):
            OD.draw_hanging(c, T, wx(x) - 110, wx(x) + 110, 190, 520, "#2E4A3A", "#B8A070", seed=4)
    sh = LGP((0, OD.Y_FL - 30), (0, OD.Y_FL + 30), [("#0E1218", 0.0, 0), ("#0E1218", 1.0, 70)])
    c.drawRect(skia.Rect.MakeLTRB(xa, OD.Y_FL - 30, xb, OD.Y_FL + 30), sh)


def _salon_main_generic(room, fr, xa, xb, floor, chair="#4A3828", rug_=None, planks=None, extra=None):
    """Salon ana katmanı (zemin + masa arkası sandalyeler + uç sandalyeler) — renkler varyanttan."""
    c, T, P = fr.c, room.T, room.pal
    if planks:
        OD.floor_planks(c, xa, xb, OD.Y_FL, OD.LH, T, col=planks, seed=6)
    else:
        OD.floor_tiles(c, xa, xb, OD.Y_FL, OD.LH, T, floor[0], floor[1], seed=4, w0=floor[2] if len(floor) > 2 else 74.0, grow=1.13)
    for i in range(6):
        x = room.TX0 + 130 + i * 208
        if OD._vis(x, 60, xa, xb):
            OD.chair_back(c, T, x, 700, 72, 252, col=chair, cushion=P["seat"])
    fa, fb = room.TX0 - 34, room.TX0 + room.TW + 34
    if OD._vis(fa, 80, xa, xb):
        OD.draw_chair(c, T, fa - 24, room.TY + 117 - 8, 270, 74, 92, facing=1, col=chair, cushion=P["seat"])
    if OD._vis(fb, 80, xa, xb):
        OD.draw_chair(c, T, fb + 24, room.TY + 117 - 8, 270, 74, 92, facing=-1, col=chair, cushion=P["seat"])
    if rug_:
        OD.rug(c, room.TX0 - 120, room.TX0 + room.TW + 120, 744, 868, T, field=rug_[0], border=rug_[1])
    if extra:
        extra(c, T, xa, xb)


def _brugge_main(room, fr, xa, xb):
    """Brugge zemini: siyah-beyaz dama taş (Flaman iç mekânı); halı yok; koyu meşe sandalyeler."""
    _salon_main_generic(room, fr, xa, xb, ("#E4E0D4", "#2C2A28", 82.0), chair="#3A2C20")


def _roma_wall(room, fr, xa, xb):
    """ROMA (Vieri'nin bankası, 1390'lar): sıcak toprak sıvası, Roma meander frizi, dikdörtgen taş HAÇ KASALI (croce guelfa) pencereler, raf nişlerinde defterler."""
    c, T = fr.c, room.T
    night = room.tod == "night"
    wx = room.wx
    OD.plaster(c, xa, xb, OD.OV - 40, OD.Y_FL + 30, T, "#C4865C", "#D69E74", amp=0.06)
    OD.cornice(c, xa, xb, 72, T, col="#5A3420", plaster="#D69E74")
    y0, y1 = 150, 186                                        # meander frizi (krem bant, kızıl meander)
    OD.R(c, xa, y0, xb, y1, T("#E6D2A8"))
    c.drawLine(xa, y0, xb, y0, STK(OD.INK, 1.2, 180, False))
    c.drawLine(xa, y1, xb, y1, STK(OD.INK, 1.2, 180, False))
    st = 40.0
    i0 = int(math.floor(xa / st)) - 1
    for i in range(i0, int(math.ceil(xb / st)) + 1):
        x = i * st
        pth = sk.poly_path([(x, y1 - 7), (x, y0 + 7), (x + 28, y0 + 7), (x + 28, y1 - 14), (x + 14, y1 - 14), (x + 14, y0 + 16)], False)
        c.drawPath(pth, STK(T("#9A2E1E"), 4.0, 230, False))
    OD.wainscot(c, xa, xb, OD.Y_FL - 120, OD.Y_FL + 18, T, "#4A2C1C", pw=190, seed=2)
    for x in room.win_x:
        if OD._vis(wx(x), 130, xa, xb):
            OD.draw_window(c, T, wx(x), 250, 170, 270, night=night, arch=False, shutters=True, mullion=True, stone=("#D8CCB0", "#EDE4CC", "#E2D6BA", "#BCAE8E"))
    for i, x in enumerate(room.tap_x):
        if OD._vis(wx(x), 180, xa, xb):
            _alcove_flat(c, T, wx(x), 236, 230, 330, seed=i + 7, rows=3)
    sh = LGP((0, OD.Y_FL - 30), (0, OD.Y_FL + 30), [("#1A0F06", 0.0, 0), ("#1A0F06", 1.0, 70)])
    c.drawRect(skia.Rect.MakeLTRB(xa, OD.Y_FL - 30, xb, OD.Y_FL + 30), sh)


def _roma_main(room, fr, xa, xb):
    """Roma bankası zemini: küçük terrakota tuğla döşeme; arkada kemerli kapaklı para sandığı (banco); yeşil çuha masa örtüsü paletten."""
    def extra(c, T, xa_, xb_):
        if OD._vis(2480, 200, xa_, xb_):
            OD.draw_chest(c, T, 2330, 2640, 712, 120, "#4A2C1C")
    _salon_main_generic(room, fr, xa, xb, ("#B8673F", "#A1552F", 52.0), chair="#4A2C1C", rug_=None, extra=extra)


def _oculus(c, T, x, y, r, night=False):
    """Yuvarlak 'göz' pencere (oculus): taş halka, kurşun çıtalı yuvarlak camlar."""
    SOFT(c, x + 6, y + r + 14, r * 0.9, 12, "#000000", 60)
    c.drawCircle(x, y, r + 20, PT(T("#B8B09A")))
    c.drawCircle(x, y, r + 20, STK(OD.INK, 1.4, 200))
    c.drawCircle(x, y, r, OD.LGP((x - r, y - r), (x + r, y + r), [("#F2F0DE", 0.0), ("#C8D8D4", 1.0)]) if not night else PT("#1A2648"))
    c.save()
    pth = skia.Path(); pth.addCircle(x, y, r)
    c.clipPath(pth, skia.ClipOp.kIntersect, True)
    rr = r / 3.2
    for gy in range(-4, 5):
        for gx in range(-4, 5):
            cx_, cy_ = x + gx * rr * 1.7 + (gy % 2) * rr * 0.85, y + gy * rr * 1.5
            c.drawCircle(cx_, cy_, rr * 0.82, STK("#5A5444", 1.2, 140))
    c.restore()
    c.drawCircle(x, y, r, STK(OD.INK, 1.6, 210))


def _scales_hanging(c, T, x, y, s=1.0):
    """Duvarda çivide asılı terazi (durağan)."""
    c.drawLine(x, y, x, y + 40 * s, STK("#3A2A18", 2.0, 220))
    c.drawLine(x - 60 * s, y + 40 * s, x + 60 * s, y + 40 * s, STK(T("#8A6A32"), 4.0 * s, 255))
    for sg in (-1, 1):
        c.drawLine(x + sg * 60 * s, y + 40 * s, x + sg * 48 * s, y + 92 * s, STK("#3A2A18", 1.2, 200))
        c.drawLine(x + sg * 60 * s, y + 40 * s, x + sg * 72 * s, y + 92 * s, STK("#3A2A18", 1.2, 200))
        c.drawOval(skia.Rect.MakeLTRB(x + sg * 60 * s - 26 * s, y + 88 * s, x + sg * 60 * s + 26 * s, y + 100 * s), PT(T("#A8823A")))
        c.drawOval(skia.Rect.MakeLTRB(x + sg * 60 * s - 26 * s, y + 88 * s, x + sg * 60 * s + 26 * s, y + 100 * s), STK(OD.INK, 1.0, 190))


def _katip_wall(room, fr, xa, xb):
    """KÂTİP ODASI (c2s12 çifte kayıt): yeşilimsi gri badana, koyu yeşil lambri, yuvarlak 'göz' pencereler, uzun defter rafları, asılı terazi."""
    c, T = fr.c, room.T
    night = room.tod == "night"
    wx = room.wx
    OD.plaster(c, xa, xb, OD.OV - 40, OD.Y_FL + 30, T, "#BFC6AE", "#D0D5BF", amp=0.05)
    OD.cornice(c, xa, xb, 72, T, col="#3E4A34", plaster="#D0D5BF")
    OD.wainscot(c, xa, xb, OD.Y_FL - 132, OD.Y_FL + 18, T, "#3E4A34", pw=140, seed=5)
    for x in room.win_x:
        if OD._vis(wx(x), 120, xa, xb):
            _oculus(c, T, wx(x), 300, 82, night=night)
    for i, x in enumerate(room.tap_x):
        if OD._vis(wx(x), 220, xa, xb):
            x0, x1 = wx(x) - 190, wx(x) + 190
            for k, yy in enumerate((330, 440, 550)):
                OD.BOX(c, x0, yy, x1, yy + 14, "#4A3420", T, hl=0.16, sh=0.24, ink=1.3)
                rs = OD._RS(int(yy) + i * 7)
                xx = x0 + 14
                while xx < x1 - 70:
                    n = 1 + rs.randint(4)
                    w_ = 56 + rs.randint(26)
                    for kk in range(n):
                        OD.draw_book(c, xx + w_ / 2 + (kk % 2) * 3, yy - 7 - kk * 13, w_, 12, ["#2E4A3A", "#6A2E24", "#4A3A2A", "#8A6A3A", "#E4D8B8"][(kk + int(xx)) % 5])
                    xx += w_ + 14 + rs.randint(14)
            if i == 1:
                _scales_hanging(c, T, wx(x), 196, 1.0)
    sh = LGP((0, OD.Y_FL - 30), (0, OD.Y_FL + 30), [("#101408", 0.0, 0), ("#101408", 1.0, 70)])
    c.drawRect(skia.Rect.MakeLTRB(xa, OD.Y_FL - 30, xb, OD.Y_FL + 30), sh)


def _katip_main(room, fr, xa, xb):
    """Kâtip odası zemini: ahşap tahta döşeme; koyu yeşil minderli sandalyeler."""
    _salon_main_generic(room, fr, xa, xb, None, chair="#4A3420", planks="#8A6038")


def comune_shield(c, T, x, y, s=1.0):
    """Floransa Komünü kalkanı: BEYAZ zeminde KIRMIZI zambak (giglio) — sıvaya boyalı."""
    p = skia.Path()
    w, h = 110 * s, 130 * s
    p.moveTo(x - w / 2, y)
    p.lineTo(x + w / 2, y)
    p.lineTo(x + w / 2, y + h * 0.55)
    p.cubicTo(x + w / 2, y + h * 0.86, x + w * 0.2, y + h * 0.98, x, y + h)
    p.cubicTo(x - w * 0.2, y + h * 0.98, x - w / 2, y + h * 0.86, x - w / 2, y + h * 0.55)
    p.close()
    FILLP(c, p, T("#F2ECDC"), 255, 1.6, 210)
    lp = lily_path(x, y + h * 0.58, h * 0.62)
    c.drawPath(lp, PT(T("#B33620")))
    c.drawPath(lp, STK(OD.INK, 1.0, 170))


def _bundle_shelf(c, T, x0, x1, y, rows=3, seed=1):
    """Raf: iple bağlı rulo beyanname (portata) demetleri."""
    rs = OD._RS(seed)
    for r in range(rows):
        yy = y + r * 110
        OD.BOX(c, x0, yy, x1, yy + 14, "#5A3A22", T, hl=0.16, sh=0.24, ink=1.3)
        xx = x0 + 16
        while xx < x1 - 50:
            n = 2 + rs.randint(3)
            for k in range(n):
                ry = yy - 12 - k * 15
                c.drawOval(skia.Rect.MakeLTRB(xx, ry - 8, xx + 44, ry + 8), PT(T(["#E8DCB8", "#DCCB98", "#EFE4C4"][(k + int(xx)) % 3])))
                c.drawOval(skia.Rect.MakeLTRB(xx, ry - 8, xx + 44, ry + 8), STK(OD.INK, 1.0, 170))
            c.drawLine(xx + 22, yy - 4, xx + 22, yy - 12 - n * 15, STK("#8A2A1E", 2.0, 220))
            xx += 56 + rs.randint(10)


def _catasto_wall(room, fr, xa, xb):
    """CATASTO DAİRESİ (1427, c2s22): açık kireç sıva, Floransa kırmızısı lambri, ikiz kemerli pencereler, Komün kalkanları (kırmızı zambak),
    iple bağlı beyanname (portata) rafları."""
    c, T = fr.c, room.T
    night = room.tod == "night"
    wx = room.wx
    OD.plaster(c, xa, xb, OD.OV - 40, OD.Y_FL + 30, T, "#DCCDAA", "#E8DCC0", amp=0.05)
    OD.cornice(c, xa, xb, 72, T, col="#6A2A20", plaster="#E8DCC0")
    OD.wainscot(c, xa, xb, OD.Y_FL - 110, OD.Y_FL + 18, T, "#7A2E22", pw=160, seed=9)
    for x in room.win_x:
        if OD._vis(wx(x), 140, xa, xb):
            arch = skia.Path()
            x0_, x1_, yt = wx(x) - 96, wx(x) + 96, 224
            arch.moveTo(x0_, 560); arch.lineTo(x0_, yt + 96); arch.arcTo(skia.Rect.MakeLTRB(x0_, yt, x1_, yt + 192), 180, 180, False); arch.lineTo(x1_, 560); arch.close()
            FILLP(c, arch, T("#CDBF9C"), 255, 1.6, 200)
            for sg in (-1, 1):
                OD.draw_window(c, T, wx(x) + sg * 46, 268, 70, 280, night=night, shutters=False, mullion=False, sill=False, stone=("#CDBF9C", "#E2D6B8", "#D7C9A4", "#B8A880"))
    for i, x in enumerate(room.tap_x):
        if OD._vis(wx(x), 220, xa, xb):
            if i == 1:
                comune_shield(c, T, wx(x), 250, 1.3)
            else:
                _bundle_shelf(c, T, wx(x) - 180, wx(x) + 180, 330, rows=3, seed=i + 11)
    for x in (240, 3300):
        if OD._vis(wx(x), 120, xa, xb):
            comune_shield(c, T, wx(x), 260, 1.0)
    sh = LGP((0, OD.Y_FL - 30), (0, OD.Y_FL + 30), [("#1A0F06", 0.0, 0), ("#1A0F06", 1.0, 70)])
    c.drawRect(skia.Rect.MakeLTRB(xa, OD.Y_FL - 30, xb, OD.Y_FL + 30), sh)


def _catasto_main(room, fr, xa, xb):
    _salon_main_generic(room, fr, xa, xb, ("#C47248", "#AC5C3A", 70.0), chair="#5A3A22", rug_=None)


OD.SALON_PAL.update({
    "brugge": dict(wall=("#D3D7D2", "#E5E8E3"), dado="#3E3226", tap=("#2E4A3A", "#B8A070"), floor=("#E4E0D4", "#2C2A28"), cloth=("#2E3E4A", "#B8A070"), deco="flemish", seat="#2E4A3A",
                   light="#DCE8F4"),
    "roma": dict(wall=("#C4865C", "#D69E74"), dado="#4A2C1C", tap=("#2E5A3A", "#C9A45A"), floor=("#B8673F", "#A1552F"), cloth=("#2E5A3A", "#C9A45A"), deco="roma", seat="#7A2E2A",
                 light="#FFE2A0"),
    "katip": dict(wall=("#BFC6AE", "#D0D5BF"), dado="#3E4A34", tap=("#3E4A34", "#B89A5A"), floor=("#8A6038", "#7A5030"), cloth=("#5A2A20", "#C9A45A"), deco="katip", seat="#3E4A34",
                  light="#F4EED2"),
    "catasto": dict(wall=("#DCCDAA", "#E8DCC0"), dado="#7A2E22", tap=("#7A2E22", "#E8DCC0"), floor=("#C47248", "#AC5C3A"), cloth=("#2E4A3A", "#D2A33E"), deco="catasto", seat="#7A2E22",
                    light="#FFEFC0"),
})
OD.SALON_HOOKS.update({("brugge", "wall"): _brugge_wall, ("brugge", "main"): _brugge_main,
                       ("roma", "wall"): _roma_wall, ("roma", "main"): _roma_main,
                       ("katip", "wall"): _katip_wall, ("katip", "main"): _katip_main,
                       ("catasto", "wall"): _catasto_wall, ("catasto", "main"): _catasto_main})


# ── papalık salonu ve Konstanz konsil salonu (P1Salon): Medici ağaçlı goblen YOK ──
def _papal_hanging(c, T, f, x, y0, w, h):
    """Papalık kumaşı: koyu kızıl damasko + ortada papalık nişanı (çapraz ANAHTARLAR + üstte TİARA), altın saçak."""
    OD.draw_hanging(c, T, x - w / 2, x + w / 2, y0, y0 + h, "#6E1A22", "#D2A33E", seed=8)
    _icons.draw_icon(f, "p1_anahtar", x, y0 + h * 0.60, size=w * 0.62, metal="gold", alpha=1.0, glow=0.0, shadow=True)
    tiara_draw(f, x, y0 + h * 0.28, w * 0.34, 1.0)


def eagle_single(c, x, y, s, col="#1E1A18", arm="#A8321E"):
    """Hanedan armasında TEK BAŞLI kartal (1415'te Sigismund 'Romalıların kralı'; çift başlı kartal imparatorluk taç giyme sonrası, 1433):
    açık kanatlar (5 tüy parmağı), sağa (seyirciye göre sola) bakan baş, yelpaze kuyruk; gaga ve pençeler kırmızı. s ≈ kanat açıklığı/2."""
    p = skia.Path()
    for sg in (-1, 1):                                          # kanatlar
        w = skia.Path()
        w.moveTo(x + sg * 0.10 * s, y - 0.18 * s)
        w.cubicTo(x + sg * 0.45 * s, y - 0.62 * s, x + sg * 0.85 * s, y - 0.60 * s, x + sg * 1.00 * s, y - 0.50 * s)
        for k in range(5):
            u = k / 4.0
            ex, ey = x + sg * (1.00 - 0.16 * u) * s, y + (-0.50 + 0.62 * u) * s
            w.lineTo(ex, ey)
            w.lineTo(x + sg * (0.80 - 0.15 * u) * s, y + (-0.36 + 0.60 * u) * s)
        w.lineTo(x + sg * 0.12 * s, y + 0.18 * s)
        w.close()
        p.addPath(w)
    p.addOval(skia.Rect.MakeLTRB(x - 0.17 * s, y - 0.34 * s, x + 0.17 * s, y + 0.34 * s))             # gövde
    p.addCircle(x - 0.06 * s, y - 0.46 * s, 0.13 * s)                                                 # baş (sola bakar)
    p.addRect(skia.Rect.MakeLTRB(x - 0.07 * s, y - 0.40 * s, x + 0.07 * s, y - 0.28 * s))              # boyun
    t = skia.Path()                                                                                  # kuyruk
    t.moveTo(x - 0.10 * s, y + 0.28 * s); t.lineTo(x - 0.26 * s, y + 0.62 * s); t.lineTo(x - 0.09 * s, y + 0.54 * s)
    t.lineTo(x, y + 0.66 * s); t.lineTo(x + 0.09 * s, y + 0.54 * s); t.lineTo(x + 0.26 * s, y + 0.62 * s); t.lineTo(x + 0.10 * s, y + 0.28 * s); t.close()
    p.addPath(t)
    c.drawPath(p, PT(col))
    c.drawPath(p, STK("#0A0806", 1.2, 200))
    beak = sk.poly_path([(x - 0.17 * s, y - 0.50 * s), (x - 0.30 * s, y - 0.46 * s), (x - 0.18 * s, y - 0.41 * s)])
    c.drawPath(beak, PT(arm))
    for sg in (-1, 1):                                          # bacak + pençe
        c.drawLine(x + sg * 0.08 * s, y + 0.26 * s, x + sg * 0.22 * s, y + 0.44 * s, STK(col, 0.07 * s, 255))
        for k in (-1, 0, 1):
            c.drawLine(x + sg * 0.22 * s, y + 0.44 * s, x + sg * 0.22 * s + k * 0.06 * s, y + 0.52 * s, STK(arm, 0.025 * s, 255))
    c.drawCircle(x - 0.10 * s, y - 0.49 * s, 0.022 * s, PT("#E8C25A"))


def _imperial_hanging(c, T, f, x, y0, w, h):
    """İmparatorluk kumaşı (Konstanz 1415): ALTIN zeminde SİYAH TEK BAŞLI kartal (Romalıların kralı Sigismund), kırmızı saçak."""
    OD.draw_hanging(c, T, x - w / 2, x + w / 2, y0, y0 + h, "#C9A23A", "#7A5A1A", seed=9, damask=False)
    eagle_single(c, x, y0 + h * 0.46, w * 0.40)
    c.drawLine(x - w / 2, y0 + h - 6, x + w / 2, y0 + h - 6, STK(T("#A8321E"), 4.0, 230, False))


def _p1salon_wall(self, fr, xa, xb):
    c, T, P = fr.c, self.T, self.pal
    night = self.tod == "night"
    wx = self.wx
    if self.p1v == "konstanz":
        OD.ashlar(c, xa, xb, OD.OV - 40, OD.Y_FL + 30, T, "#B4B3A8", 60.0, seed=3)
        OD.cornice(c, xa, xb, 72, T, col="#6E5434", plaster="#C9C6B8")
        OD.wainscot(c, xa, xb, OD.Y_FL - 160, OD.Y_FL + 18, T, "#9A7A4E", pw=130, seed=6)      # açık meşe/çam (papalık salonundan FARKLI ahşap)
        hang = _imperial_hanging
    else:
        OD.plaster(c, xa, xb, OD.OV - 40, OD.Y_FL + 30, T, P["wall"][0], P["wall"][1], amp=0.05)
        OD.cornice(c, xa, xb, 72, T, col="#3A1E14", plaster=P["wall"][1])
        OD.wainscot(c, xa, xb, OD.Y_FL - 118, OD.Y_FL + 18, T, "#3E2014", seed=3)                  # koyu ceviz
        hang = _papal_hanging
    for x in self.win_x:
        if OD._vis(wx(x), 130, xa, xb):
            OD.draw_window(c, T, wx(x), 226, 176, 336, night=night)
    for x in list(self.tap_x) + [240, 3300]:
        if OD._vis(wx(x), 150, xa, xb):
            hang(c, T, fr, wx(x), 214, 210, 360)
    sh = LGP((0, OD.Y_FL - 30), (0, OD.Y_FL + 30), [("#1A0F06", 0.0, 0), ("#1A0F06", 1.0, 70)])
    c.drawRect(skia.Rect.MakeLTRB(xa, OD.Y_FL - 30, xb, OD.Y_FL + 30), sh)


P1_DRAPE = {"papa": ("#EDE4CC", "#C9A23A"), "konstanz": ("#2A3E6E", "#C9A23A")}          # papalık: BEYAZ-altın perde · Konstanz: lacivert-altın


def _p1salon_dyn_taht(self, ctx):
    """Boş taht odası canlı katmanı (Salon._dyn_taht) — perde rengi yere göre (papalık beyaz-altın, Konstanz lacivert)."""
    f, c, t = ctx.f, ctx.c, ctx.t
    night = ctx.tod == "night"
    x0 = 1700
    k = 0.6 + 0.4 * math.sin(t * 0.21)
    c.drawPath(sk.poly_path([(x0 - 70, 250), (x0 + 70, 250), (x0 + 120, 740), (x0 - 120, 740)]), LGP((0, 250), (0, 740), [("#FFE9A8", 0.0, int(36 * k)), ("#FFE9A8", 1.0, int(70 * k))]))
    OD.dust_motes(c, t, x0 - 220, 240, x0 + 220, 760, n=26, seed=14, a=0.8, size=2.2, drift=(3, 5), col="#FFF3D0" if not night else "#BFD0F5")
    col, col2 = P1_DRAPE.get(self.p1v, ("#8E2A30", OD.GOLD))
    for sg, ph in ((-1, 0.3), (1, 1.4)):
        OD.draw_drape(c, x0 + sg * 200 - 34, 160, 68, 520, t, col=col, col2=col2, amp=0.045, seed=5, ph=ph, tie=0.7, side="l" if sg < 0 else "r")
    OD.draw_extra(ctx, "back")


P1Salon._draw_wall = _p1salon_wall
P1Salon._dyn_taht = _p1salon_dyn_taht
P1_SALON_PAL["konstanz"]["floor"] = ("#C2BCA8", "#6E6A5E")


def _p1salon_init(self, variant, tod):
    self.p1v = variant or "papa"
    self.pal = P1_SALON_PAL.get(self.p1v, P1_SALON_PAL["papa"])
    self.variant = "taht"
    self.tod = tod
    self.T = OD.OTint(tod)
    self.layers = {}
    self.opts = {}
    self.key = f"{self.name}{self.p1v}t2"                                          # tur 2 dekoru: yeni önbellek anahtarı
    self.build()


P1Salon.__init__ = _p1salon_init


# ── Cavalcanti'nin hücresi (Stinche hapishanesi, 1430'lar): taş duvar, PARMAKLIKLI yüksek pencere, saman yatak; haç/yatak/kitaplık yok (SA2-Y9) ──
class P1Zindan(OD.Calisma):
    """Hapis hücresi (Calisma 'hucre' yerleşimi): kaba taş duvar, yüksek küçük pencere + demir parmaklık, duvarda zincir halkası, saman şilte, sade masa."""
    name = "p1zindan"

    def __init__(self, variant, tod):
        self.p1v = variant or "stinche"
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
        OD.ashlar(c, xa, xb, OD.OV - 40, OD.Y_FL + 30, T, "#9C968A", 54.0, seed=7)
        c.drawRect(skia.Rect.MakeLTRB(xa, OD.OV - 40, xb, 240), LGP((0, OD.OV - 40), (0, 240), [("#1A140E", 0.0, 170), ("#1A140E", 1.0, 0)]))
        OD.R(c, xa, OD.Y_FL - 18, xb, OD.Y_FL + 30, T("#5E584C"))
        c.drawLine(xa, OD.Y_FL - 18, xb, OD.Y_FL - 18, STK(OD.INK, 1.2, 170, False))
        x = wx(1750)
        if OD._vis(x, 110, xa, xb):                                               # yüksek pencere + parmaklık
            OD.draw_window(c, T, x, 200, 120, 170, night=night, shutters=False, mullion=False, sill=True, stone=("#7E786C", "#A8A294", "#9C968A", "#6E685C"))
            for i in range(5):
                bx = x - 48 + i * 24
                c.drawLine(bx, 196, bx, 374, STK("#22201E", 7.0, 255, False))
                c.drawLine(bx - 1.5, 196, bx - 1.5, 374, STK("#8A8680", 1.2, 140, False))
            for by in (250, 320):
                c.drawLine(x - 64, by, x + 64, by, STK("#22201E", 7.0, 255, False))
        xr = wx(520)
        if OD._vis(xr, 60, xa, xb):                                               # duvar halkası + zincir
            c.drawCircle(xr, 360, 22, STK("#2A2622", 6.0, 255))
            OD.R(c, xr - 10, 334, xr + 10, 346, "#3A3630")
            for k in range(6):
                c.drawOval(skia.Rect.MakeLTRB(xr - 7, 382 + k * 18, xr + 7, 402 + k * 18), STK("#2A2622", 3.0, 240))
        sh = LGP((0, OD.Y_FL - 30), (0, OD.Y_FL + 30), [("#0E0C0A", 0.0, 0), ("#0E0C0A", 1.0, 90)])
        c.drawRect(skia.Rect.MakeLTRB(xa, OD.Y_FL - 30, xb, OD.Y_FL + 30), sh)

    def _draw_main(self, fr, xa, xb):
        c, T = fr.c, self.T
        OD.floor_tiles(c, xa, xb, OD.Y_FL, OD.LH, T, "#77736A", "#666258", seed=9, w0=96.0, grow=1.12)
        if OD._vis(330, 330, xa, xb):                                             # saman şilte (yatak yok)
            OD.SOFT(c, 330, 812, 250, 18, "#000000", 70)
            c.drawPath(sk.smooth_path([(110, 806), (130, 776), (330, 768), (540, 778), (560, 808), (330, 820)], True, 0.5), PT(T("#B89A5A")))
            for k in range(26):
                xx = 130 + k * 16
                c.drawLine(xx, 778 + (k % 3) * 4, xx + 10, 806, STK("#7A6234", 1.0, 150))
        if OD._vis(self.CH_X, 70, xa, xb):
            OD.draw_chair(c, T, self.CH_X - 24, 808, 200, 72, 84, facing=1, col="#4A3828", cushion="#5A4A3A")


OD.ROOMS["p1zindan"] = P1Zindan
