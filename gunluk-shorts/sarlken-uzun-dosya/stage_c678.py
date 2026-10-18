"""Bölüm yazarı C (c6, c7, c8) ortak yardımcıları ve ortak çekim türleri.

Ortak dosyalara dokunmadan (sk, shots, stage, scenes_lib, mapsk, medal, icons) kendi çekim türlerimiz için yardımcılar:
  W(sid, "sözcük", off, fb)  -> sözcük çapası; sözcük (ses yaması sırasında) zaman çizelgesinde yoksa cümle başından fb sn'ye düşer
  ic(f, ad, x, y, ...)       -> simge çiz; simge adı henüz yoksa yedek simge
  ov_*                       -> theatre çekimleri için kaplama (overlay) üreticileri (tarih levhası, kicker, damga, madalya...)
  c678_sahne                 -> theatre sarmalayıcı: sahne yoksa yer tutucu + kaplama yine çizilir
  c678_cift                  -> yan yana 1–3 sayaç (aralık/yaklaşık destekli, damga ve asker bandı seçenekli)
"""
import math

import numpy as np
import skia

import icons
import medal
import shots as SH
import sk
import stage as ST
from sk import C, H, W as SW, back_out, clamp, ease_in, ease_io, ease_out, lerp, mix, seg, smooth

Wd = SW          # ekran genişliği (W adı çapa yardımcısına ayrıldı)


# ───────────────────────────── çapa yardımcısı ─────────────────────────────
def W(sid, key, off=0.0, fb=0.0, nth=0):
    """Sözcük çapası. Sözcük zaman çizelgesinde yoksa (ses yaması beklerken) cümle başından fb sn'ye düşer."""
    tl = SH.timeline()
    try:
        tl.word(sid, key, nth)
    except KeyError:
        return (sid, fb + off)
    return (sid, key, nth, off) if nth else (sid, key, off)


def S(sid, off=0.0):
    return (sid, off)


# ───────────────────────────── küçük yardımcılar ─────────────────────────────
def up(s):
    """Türkçe büyük harf."""
    return s.replace("i", "İ").replace("ı", "I").upper()


def ic(f, name, x, y, size=120, fallback="shield", **kw):
    n = name if name in icons._ICONS else fallback
    icons.draw_icon(f, n, x, y, size=size, **kw)


def has_icon(name):
    return name in icons._ICONS


def glow(f, x, y, r, color="#E3B54A", a=0.25):
    f.circle(x, y, r, shader=f.rad(x, y, r, [(color, 0.0, int(255 * clamp(a))), (color, 1.0, 0)]))


def txt(f, s, x, y, size=34, color="#F2E4B8", face="cap_b", align="c", track=0.0, alpha=1.0, shadow=(2, 2, 3, "#000000")):
    return f.text(s, x, y, face=face, size=size, color=color, align=align, track=track, alpha=alpha, shadow=shadow)


def chip(f, text, x, y, k=1.0, size=28, fill="#150D08", edge="#C9962B", color="#F4E6BC", padx=26, face="title_m", track=5, h=None, align="c"):
    """Altın kenarlı küçük etiket levhası (x,y = orta; y = metin taban çizgisinin üstü kabaca merkez)."""
    if k <= 0:
        return 0
    wt = sk.text_width(text, face, size, track)
    ww = wt + 2 * padx
    hh = h or size * 1.9
    x0 = x - ww / 2 if align == "c" else (x if align == "l" else x - ww)
    yy = y - hh / 2 + (1 - k) * 8
    f.rrect(x0, yy, ww, hh, 12, color=fill, alpha=0.86 * k)
    f.rrect(x0, yy, ww, hh, 12, style="stroke", sw=2.2, color=edge, alpha=0.95 * k)
    f.text(text, x0 + ww / 2, yy + hh / 2 + size * 0.34, face=face, size=size, color=color, align="c", track=track, alpha=k, shadow=(1, 2, 2, "#000000"))
    return ww


def ink_rule(f, x0, x1, y, color="#C9962B", sw=2.0, alpha=0.8, k=1.0):
    f.line(x0, y, lerp(x0, x1, clamp(k)), y, color=color, sw=sw, alpha=alpha)


def arrow(f, p0, p1, prog, color="#F0D27A", width=7.0, bend=0.0, alpha=1.0, dash=None, head=None, glowa=0.18):
    """Quadratic eğri ok (kısmen çizilir). Dönüş: ucun ekran konumu."""
    if prog <= 0:
        return None
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1.0
    cxp, cyp = mx - dy / L * bend, my + dx / L * bend
    path = skia.Path()
    path.moveTo(*p0)
    path.quadTo(cxp, cyp, *p1)
    pm = skia.PathMeasure(path, False)
    total = pm.getLength()
    d = total * clamp(prog)
    part = skia.Path()
    pm.getSegment(0, d, part, True)
    f.path(part, style="stroke", sw=width * 2.6, color=color, alpha=glowa * alpha, blur=width)
    if not dash:
        f.path(part, style="stroke", sw=width + 3, color="#1A0F08", alpha=0.55 * alpha)
    p = f.paint(color, style="stroke", sw=width, alpha=alpha)
    if dash:
        p.setPathEffect(skia.DashPathEffect.Make([dash[0], dash[1]], 0))
    f.c.drawPath(part, p)
    pos, tan = pm.getPosTan(max(0.0, d - 0.5))
    if pos is None:
        return None
    ang = math.atan2(tan.y(), tan.x())
    ah = head or width * 3.2
    tip = (pos.x() + math.cos(ang), pos.y() + math.sin(ang))
    a1 = (tip[0] - ah * math.cos(ang - 0.45), tip[1] - ah * math.sin(ang - 0.45))
    a2 = (tip[0] - ah * math.cos(ang + 0.45), tip[1] - ah * math.sin(ang + 0.45))
    f.poly([tip, a1, a2], color=color, alpha=alpha)
    f.poly([tip, a1, a2], style="stroke", sw=1.6, color="#2A1A0C", alpha=0.8 * alpha)
    return tip


def jag_points(x0, y0, x1, y1, n=14, amp=18, seed=3):
    """(x0,y0)→(x1,y1) arası pürüzlü (yırtık) çizgi noktaları."""
    rs = np.random.RandomState(seed)
    pts = []
    L = math.hypot(x1 - x0, y1 - y0)
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    for i in range(n + 1):
        u = i / n
        o = 0 if i in (0, n) else (rs.rand() - 0.5) * 2 * amp
        pts.append((lerp(x0, x1, u) + nx * o, lerp(y0, y1, u) + ny * o))
    return pts


def strike_line(f, x0, y0, x1, y1, k, color="#B02A2A", sw=9, alpha=1.0):
    """Elle çizilmiş gibi kırmızı çizgi (üstünü çizme)."""
    if k <= 0:
        return
    xe, ye = lerp(x0, x1, clamp(k)), lerp(y0, y1, clamp(k))
    f.line(x0, y0, xe, ye, color="#000000", sw=sw + 4, alpha=0.35 * alpha)
    f.line(x0, y0, xe, ye, color=color, sw=sw, alpha=alpha)


def tone(f, color, a=0.18, cy=0.45, r=1.0):
    """Çekime bölüm tonu: büyük yumuşak renkli ışıma."""
    x, y = Wd / 2, H * cy
    R = H * r * 1.15
    f.rect(0, 0, Wd, H, shader=f.rad(x, y, R, [(color, 0.0, int(255 * a)), (color, 1.0, 0)]), blend=skia.BlendMode.kPlus)


def kick(cx, text, anchor, y=120, size=30, color="#E0C682", out=None):
    """Çapa anında beliren kicker (isteğe bağlı: out anında söner)."""
    k = cx.amt(anchor, 0.7)
    if out is not None:
        k *= 1 - cx.amt(out, 0.5)
    if k > 0:
        SH.kicker(cx.f, text, Wd / 2, y, alpha=k, size=size, track=12, face="title_m", color=color)


# ───────────────────────────── theatre kaplamaları ─────────────────────────────
def ov_date(text, anchor):
    def fn(cx):
        SH._date_stamp(cx.f, (text, anchor), cx)
    return fn


def ov_kick(text, anchor, y=118, size=30, out=None, color="#E0C682"):
    def fn(cx):
        kick(cx, text, anchor, y=y, size=size, color=color, out=out)
    return fn


def ov_stamp(text, anchor, x=Wd / 2, y=H * 0.78, size=60, rot=-0.10, color="#B02A2A"):
    def fn(cx):
        t = cx.amt(anchor, 0.3)
        if t > 0:
            SH.stamp(cx.f, text, x, y, rot=rot, size=size, color=color, t=t)
    return fn


def ov_medal(key, anchor, x, y, size=300, metal="gold", flip=False, name=None, role=None, plate_dx=0, plate_y=None, out=None):
    """Köşeye küçük madalya (+isteğe bağlı levha)."""
    def fn(cx):
        k = cx.amt(anchor, 0.7)
        if out is not None:
            k *= 1 - cx.amt(out, 0.5)
        if k <= 0:
            return
        cx.f.circle(x, y, size * 0.62, shader=cx.f.rad(x, y, size * 0.62, [("#000000", 0.0, int(120 * k)), ("#000000", 1.0, 0)]))
        SH.draw_medal(cx.f, key, x, y + (1 - k) * 24, size * (0.9 + 0.1 * ease_out(k)), metal, flip, alpha=k, tilt=0.12 * math.sin(cx.t * 0.6))
        if name:
            SH.name_plate(cx.f, name, role, None, cx_=x + plate_dx, y=(plate_y if plate_y is not None else y + size * 0.5), alpha=1.0, w=min(520, max(340, size * 1.4)), t=k)
    return fn


def ov_chip(text, anchor, x=Wd / 2, y=H * 0.86, size=36, edge="#C9962B", color="#F4E6BC", padx=36, h=None, out=None):
    def fn(cx):
        k = cx.amt(anchor, 0.5)
        if out is not None:
            k *= 1 - cx.amt(out, 0.5)
        if k > 0:
            chip(cx.f, text, x, y, k=k, size=size, edge=edge, color=color, padx=padx, h=h)
    return fn


def ov_all(*fns):
    def fn(cx):
        for g in fns:
            g(cx)
    return fn


# ───────────────────────────── theatre sarmalayıcı ─────────────────────────────
@SH.kind("c678_sahne")
def k_sahne(cx, overlay_always=None, **kw):
    """theatre'a delege eder. Sahne kayıtsızsa (lab henüz teslim etmedi) yer tutucu çizer ama kaplamayı yine uygular."""
    import scenes_lib as SL
    SH.KINDS["theatre"](cx, **kw)
    if kw.get("scene") not in SL.SCENES and kw.get("overlay"):
        kw["overlay"](cx)


# ───────────────────────────── sayaçlar ─────────────────────────────
def _numstr(v, k, decimals=0):
    if isinstance(v, (tuple, list)):
        return f"{SH.fmt_int(v[0] * k)} – {SH.fmt_int(v[1] * k)}"
    return SH.fmt_int(v * k)


@SH.kind("c678_cift")
def k_cift(cx, items=(), title=None, bgk="night", y=H * 0.5, size=150, icon_size=170, stampt=None, band=None, kick_at=0.0, tone_col=None, sep=None, ykick=130):
    """1–3 sayaç yan yana. items: [dict(value|(a,b), unit, icon, at, dur, prefix, suffix, label, metal, sub)]
    band=("janissary", n, anchor): alt kenarda asker siluet bandı (sayı arttıkça kalabalıklaşır)."""
    f = cx.f
    f.bg(bgk)
    f.rays(alpha=0.28)
    if tone_col:
        tone(f, tone_col, 0.14)
    sk.dust(f, cx.t, n=50)
    n = len(items)
    colw = (Wd - 240) / max(1, n)
    if title:
        SH.kicker(f, title, Wd / 2, ykick, alpha=cx.amt(kick_at, 0.7), size=32, track=12, face="title_m", color="#E0C682")
    if band:
        kind, nb, at_b = band[0], band[1], band[2]
        kk = ease_out(clamp((cx.t - cx.at(at_b)) / 3.0), 2)
        rs = np.random.RandomState(5)
        cnt = int(nb * kk)
        for i in range(cnt):
            xx = 40 + (i + rs.rand() * 0.7) * (Wd - 80) / nb
            row = i % 3
            hh = 120 - row * 14
            ST.figure(f, kind, xx, H + 8 - row * 34, hh * 1.15, col="#0A0604", rim="#79B58C", face=-1 if rs.rand() > 0.5 else 1, alpha=0.95 - row * 0.12)
    for i, it in enumerate(items):
        xc = Wd / 2 - colw * (n - 1) / 2 + i * colw
        at = it.get("at", 0.0)
        a = cx.amt(at, 0.5)
        if a <= 0:
            continue
        k = ease_out(clamp((cx.t - cx.at(it.get("count_at", at))) / it.get("dur", 1.6)), 3)
        icon = it.get("icon")
        if icon:
            ic(f, icon, xc, y - size * 0.95, size=icon_size * (0.9 + 0.1 * back_out(a)), metal=it.get("metal", "gold"), alpha=a, glow=0.3 * a)
        s = it.get("prefix", "") + _numstr(it["value"], k) + it.get("suffix", "")
        smax = it.get("prefix", "") + _numstr(it["value"], 1.0) + it.get("suffix", "")
        sz = SH.fit_size(smax, "title", size, colw - 40, 6)
        SH.gold_flat(f, s, xc, y + size * 0.28, face="title", size=sz, track=6, alpha=a)
        if it.get("unit"):
            f.text(up(it["unit"]), xc, y + size * 0.28 + 74, face="title_m", size=46, color="#E0C682", align="c", track=12, alpha=cx.amt(at, 0.5, off=0.3))
        if it.get("label"):
            f.text(it["label"], xc, y + size * 0.28 + 128, face="cap_i", size=38, color="#C9B27A", align="c", alpha=cx.amt(at, 0.6, off=0.6))
        if it.get("sub"):
            f.text(it["sub"], xc, y + size * 0.28 + 176, face="cap", size=28, color="#A89868", align="c", alpha=cx.amt(at, 0.6, off=0.9), track=3)
        if i > 0 and sep:
            xs = xc - colw / 2
            f.text(sep, xs, y + size * 0.1, face="title", size=80, color="#C9962B", align="c", alpha=0.8 * a)
    if stampt:
        SH.stamp(f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 56,
                 rot=stampt[5] if len(stampt) > 5 else -0.1)
    f.vig(0.6)


# ───────────────────────────── çapa-güvenli madalya dizisi ─────────────────────────────
@SH.kind("c678_medals")
def k_medals2(cx, items=(), size=520, y=H * 0.46, gap=None, bgk="night", title=None, vs=None, vs_icon="swords", plates=True, tone_col=None, plate_w=None, vs_metal="silver", extra=None):
    """shots.medals'ın çapa-güvenli kopyası (orijinal `at + 0.4` ile demet çapada çöküyor). items: [dict(key,name,role,dates,at,metal,flip,dim)]"""
    f = cx.f
    f.bg(bgk)
    f.rays(alpha=0.3)
    if tone_col:
        tone(f, tone_col, 0.14)
    n = len(items)
    gap = gap or min(size * 1.15, (Wd - 200) / max(1, n))
    x0 = Wd / 2 - gap * (n - 1) / 2
    for i, it in enumerate(items):
        at = it.get("at", 0.2 + 0.3 * i)
        a = cx.amt(at, 0.7)
        if a <= 0:
            continue
        x = x0 + i * gap
        dim = it.get("dim", 1.0)
        sc = (0.92 + 0.08 * ease_out(a)) * (1.0 + 0.03 * cx.u) * it.get("scale", 1.0)
        gl = (cx.t * 0.25 + 0.2 * i) % 2.0
        SH.draw_medal(f, it["key"], x, it.get("y", y), size * sc, it.get("metal", "gold"), it.get("flip", False), alpha=a * dim,
                      tilt=0.15 * math.sin(cx.t * 0.5 + i), glint=(gl if gl < 1 else None))
        if plates and it.get("name"):
            SH.name_plate(f, it["name"], it.get("role"), it.get("dates"), cx_=x, y=it.get("y", y) + size * 0.52 * it.get("scale", 1.0), t=cx.amt(at, 0.5, off=0.4), w=plate_w)
    if vs:
        k = cx.amt(vs, 0.4)
        if k > 0:
            ic(f, vs_icon, Wd / 2, y, size=130 * (0.8 + 0.2 * back_out(k)), metal=vs_metal, alpha=k, glow=0.2 * k)
    if title:
        SH.kicker(f, title, Wd / 2, 120, alpha=cx.fade(0.6, 0.4), size=30, track=12)
    sk.dust(f, cx.t, n=50)
    if extra:
        extra(cx)
    f.vig(0.55)
