"""BÖLÜM YAZARI A (c1, c2, c3, c10) ortak yardımcıları: çapa sarmalayıcı, arka planlar, levha/işaret/para/zincir/mum/terazi çizimleri,
kendi kabartma simgeleri (c1_*, c2_*, c10_* önekli) ve taban çekim türlerinin renk tonlu varyantları.
Ortak dosyalara (sk/shots/stage/...) dokunmaz; yalnız onların API'sini kullanır.
"""
import math

import numpy as np
import skia

import icons
import medal
import shots as SH
import sk
import stage as ST
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, seg, smooth, back_out


# ───────────────────────────── çapa sarmalayıcı ─────────────────────────────
def A(sid, key=None, off=0.0, fb=None, nth=0):
    """Çapa üretir. `key` sözcüğü timeline'da yoksa (metin yaması gelmeden önce) cümle başlangıcı + fb sn'ye düşer;
    yama gelince otomatik sözcüğe döner. key=None → cümle başlangıcı + off."""
    if key is None:
        return (sid, off)
    s = SH.timeline().sent[sid]
    k = SH.Timeline._n(key)
    if any(k in SH.Timeline._n(w["w"]) for w in s["words"]):
        return (sid, key, nth, off) if nth else (sid, key, off)
    return (sid, (fb if fb is not None else 0.0) + off)


def rel(a, base):
    """İki çapa arası (sn): `a` anının, `base` çekim başlangıç çapasına göre yerel saniyesi (diorama `p` zaman parametreleri için)."""
    t = SH.timeline()
    return round(t.resolve(a) - t.resolve(base), 3)


def tr_upper(s):
    return s.replace("i", "İ").replace("ı", "I").upper()


def mkey(key, fb="karl_genc"):
    """Madalya anahtarı yoksa (lab henüz eklemediyse) yedek anahtar."""
    return key if key in medal.PEOPLE else fb


def iname(name, fb="coin"):
    return name if name in icons.names() else fb


# ───────────────────────────── arka planlar ─────────────────────────────
def _b_cold(f):
    f.rect(0, 0, W, H, shader=f.rad(W * 0.5, H * 0.42, H * 1.1, [("#22403F", 0.0), ("#122625", 0.5), ("#050A0A", 1.0)]))
    for y in range(110, H, 54):                       # defter satırları
        f.line(0, y, W, y, color="#A5D6CC", sw=1.2, alpha=0.055)
    for x in (212, 220):                               # defter kenar çizgisi
        f.line(x, 0, x, H, color="#B04848", sw=1.4, alpha=0.12)
    sk.texture_overlay(f, "night", amp=0.05, seed=5)
    sk.vignette(f, 0.62)


def _b_green(f):
    f.rect(0, 0, W, H, shader=f.rad(W * 0.5, H * 0.40, H * 1.1, [("#3C4220", 0.0), ("#232915", 0.5), ("#090B05", 1.0)]))
    sk.texture_overlay(f, "night", amp=0.06, seed=7)
    sk.vignette(f, 0.6)


def _b_blood(f):
    f.rect(0, 0, W, H, shader=f.rad(W * 0.5, H * 0.42, H * 1.1, [("#4C1618", 0.0), ("#2A0C0E", 0.5), ("#090304", 1.0)]))
    sk.texture_overlay(f, "night", amp=0.06, seed=9)
    sk.vignette(f, 0.62)


def _b_dusk(f):
    f.rect(0, 0, W, H, shader=f.lin(0, 0, 0, H, [("#1B2230", 0.0), ("#4A3322", 0.62), ("#150C07", 1.0)]))
    sk.texture_overlay(f, "night", amp=0.05, seed=11)
    sk.vignette(f, 0.6)


_BGS = {"cold": _b_cold, "green": _b_green, "blood": _b_blood, "dusk": _b_dusk}


def bg(f, name):
    if name == "night":
        sk._fast_blit(f, sk.bg_image("night"))
        return
    sk._fast_blit(f, sk.baked(("a_bg", name), _BGS[name]))


def cool_rays(f, alpha=0.3, color="#CFE8E0"):
    sk._fast_blit(f, sk.rays_image(color=color), alpha=alpha, blend=skia.BlendMode.kPlus)


_RAYC = {"cold": "#CFE8E0", "green": "#EAE6A8", "blood": "#FFC4A8", "dusk": "#FFD9A8"}


def variant(name, base, bgname, rays_color=None):
    """Taban çekim türünün (SH.KINDS[base]) arka planı/ışığı değişik varyantını kaydeder: kind(name)."""
    rc = rays_color or _RAYC.get(bgname)

    def k(cx, **kw):
        f = cx.f
        f.bg = lambda kind="night", *a, **kk: bg(f, bgname)
        f.rays = lambda alpha=1.0, dx=0, dy=0, **kk: sk._fast_blit(f, sk.rays_image(color=rc), alpha=alpha, blend=skia.BlendMode.kPlus, dx=dx, dy=dy)
        try:
            SH.KINDS[base](cx, **kw)
        finally:
            del f.bg
            del f.rays
    SH.KINDS[name] = k
    return k


# ───────────────────────────── yazı / levha ─────────────────────────────
def txt(f, s, x, y, face="cap_b", size=40, color="#F0E6C8", align="c", track=0.0, alpha=1.0, shadow=True):
    if alpha <= 0:
        return 0
    return f.text(s, x, y, face=face, size=size, color=color, align=align, track=track, alpha=alpha, shadow=(2, 3, 3, "#000000") if shadow else None)


def tag(f, s, x, y, alpha=1.0, size=34, face="title_m", track=6, color="#F3DE9A", pad=34, edge="#C9962B", fill="#150D08", align="c", sub=None, subsize=24):
    """Metne göre boyutlanan altın çerçeveli levha. (x,y) = ana metnin taban çizgisinin merkezi/solu/sağı."""
    if alpha <= 0:
        return 0
    wd = sk.text_width(s, face, size, track) + pad * 2
    if sub:
        wd = max(wd, sk.text_width(sub, "cap_i", subsize, 1) + pad * 2)
    hh = size * 1.75 + (subsize * 1.25 if sub else 0)
    x0 = x - wd / 2 if align == "c" else (x if align == "l" else x - wd)
    y0 = y - size * 1.15
    SH.plate(f, x0, y0, wd, hh, alpha=alpha, fill=fill, edge=edge, corner=14, glow=True)
    f.text(s, x0 + wd / 2, y, face=face, size=size, color=color, align="c", track=track, alpha=alpha, shadow=(2, 2, 3, "#000000"))
    if sub:
        f.text(sub, x0 + wd / 2, y + size * 0.62 + subsize * 0.6, face="cap_i", size=subsize, color="#C9B27A", align="c", alpha=alpha)
    return wd


def vtext(f, s, x, y, size, face="title", color="#F4DD92", align="c", track=6, alpha=1.0):
    """Gölgeli altın-düz başlık (dinamik/sayaç dışı)."""
    return SH.gold_flat(f, s, x, y, face=face, size=size, track=track, alpha=alpha, align=align)


def strike(f, x0, x1, y, prog, color="#C0392B", sw=9, alpha=1.0, wob=3.0):
    """Yazının üstünü çizen el yapımı çizgi (soldan sağa ilerler)."""
    if prog <= 0:
        return
    xe = lerp(x0, x1, clamp(prog))
    p = skia.Path()
    p.moveTo(x0, y + wob)
    n = 8
    for i in range(1, n + 1):
        u = i / n
        xx = lerp(x0, x1, u)
        if xx > xe:
            p.lineTo(xe, y + math.sin(u * 5) * wob)
            break
        p.lineTo(xx, y + (wob if i % 2 else -wob) * 0.8)
    f.path(p, style="stroke", sw=sw + 4, color="#000000", alpha=0.45 * alpha)
    f.path(p, style="stroke", sw=sw, color=color, alpha=alpha)


def x_mark(f, x, y, r, prog, color="#C0392B", sw=12, alpha=1.0):
    """Üstü çizili işareti (X)."""
    if prog <= 0:
        return
    k1 = clamp(prog * 2)
    k2 = clamp(prog * 2 - 1)
    for (ax, ay, bx, by, k) in ((x - r, y - r, x + r, y + r, k1), (x + r, y - r, x - r, y + r, k2)):
        if k <= 0:
            continue
        ex, ey = lerp(ax, bx, k), lerp(ay, by, k)
        f.line(ax, ay, ex, ey, color="#000000", sw=sw + 5, alpha=0.5 * alpha)
        f.line(ax, ay, ex, ey, color=color, sw=sw, alpha=alpha)


def glow_disc(f, x, y, r, color="#F0D27A", a=0.5):
    f.circle(x, y, r, shader=f.rad(x, y, r, [(color, 0.0, int(255 * clamp(a))), (color, 1.0, 0)]), blend=skia.BlendMode.kPlus)


def beacon(f, x, y, t, amt=1.0, color="#F0D27A", r=15, rings=3, period=2.6):
    """Haritada konum işareti: nabız halkaları + sekizgen yıldız."""
    if amt <= 0:
        return
    glow_disc(f, x, y, r * 4.2, color, 0.42 * amt)
    for i in range(rings):
        ph = ((t / period) + i / rings) % 1.0
        f.circle(x, y, r * (0.8 + 4.6 * ph), style="stroke", sw=2.6, color=color, alpha=(1 - ph) ** 1.6 * 0.8 * amt)
    star = [(x + (r * 1.7 if i % 2 == 0 else r * 0.62) * math.cos(math.pi * i / 4 - math.pi / 2),
             y + (r * 1.7 if i % 2 == 0 else r * 0.62) * math.sin(math.pi * i / 4 - math.pi / 2)) for i in range(8)]
    f.poly(star, color=color, alpha=amt)
    f.poly(star, style="stroke", sw=1.8, color="#2A1A0C", alpha=0.85 * amt)
    f.circle(x, y, r * 0.3, color="#FFF7DC", alpha=amt)


def place(f, cm, lon, lat, name, t, amt=1.0, side="r", size=34, color="#F0D27A", sub=None, dx=44, dy=0, r=15):
    """Konum işareti + isim levhası (harita çekimi `extra` içinde)."""
    if amt <= 0:
        return None
    x, y = cm.ll(lon, lat)
    beacon(f, x, y, t, amt, color=color, r=r)
    if name:
        sl = amt * smooth(amt)
        if side == "r":
            tag(f, name, x + dx, y + size * 0.36 + dy, alpha=sl, size=size, align="l", pad=22, sub=sub)
        elif side == "l":
            tag(f, name, x - dx, y + size * 0.36 + dy, alpha=sl, size=size, align="r", pad=22, sub=sub)
        elif side == "t":
            tag(f, name, x, y - dx - 10 + dy, alpha=sl, size=size, align="c", pad=22, sub=sub)
        else:
            tag(f, name, x, y + dx + size * 0.9 + dy, alpha=sl, size=size, align="c", pad=22, sub=sub)
    return x, y


# ───────────────────────────── para / zincir / mum ─────────────────────────────
def coin(f, x, y, r, alpha=1.0, rot=0.0, squash=1.0, col="#E3B54A"):
    if alpha <= 0:
        return
    f.c.save()
    f.c.translate(x, y)
    if rot:
        f.c.rotate(math.degrees(rot))
    ry = max(1.5, r * squash)
    f.oval(0, r * 0.14, r, ry, color=mix(col, "#000000", 0.55), alpha=alpha)                       # kalınlık
    f.oval(0, 0, r, ry, shader=f.rad(-r * 0.35, -ry * 0.4, r * 1.7, [(mix(col, "#FFFFFF", 0.55), 0.0), (col, 0.5), (mix(col, "#000000", 0.4), 1.0)]), alpha=alpha)
    f.oval(0, 0, r, ry, style="stroke", sw=max(1.2, r * 0.09), color=mix(col, "#000000", 0.5), alpha=0.9 * alpha)
    f.oval(0, 0, r * 0.68, ry * 0.68, style="stroke", sw=max(1.0, r * 0.06), color=mix(col, "#FFFFFF", 0.35), alpha=0.7 * alpha)
    f.c.restore()


def pile_spec(n=120, seed=3, width=500.0, height=260.0, rmin=15, rmax=22):
    rs = np.random.RandomState(seed)
    out = []
    for i in range(n):
        v = rs.rand() ** 1.5
        hw = width / 2 * (1 - v) ** 0.85
        x = (rs.rand() * 2 - 1) * hw
        y = -v * height + rs.randn() * 3
        out.append((v, x, y, rmin + rs.rand() * (rmax - rmin), (rs.rand() - 0.5) * 0.6, 0.45 + rs.rand() * 0.3, rs.rand()))
    out.sort(key=lambda q: q[0])
    return out


def draw_pile(f, cx_, base_y, frac, spec, col="#E3B54A", alpha=1.0, scale=1.0, tarnish=0.0):
    """Para yığını: spec'in ilk frac oranı kadar para çizilir (alttan üste büyür)."""
    k = int(len(spec) * clamp(frac))
    sub = sorted(spec[:k], key=lambda q: q[2])
    for (v, x, y, r, rot, sq, tone) in sub:
        c = mix(col, "#7A7468", tarnish) if tarnish > 0 else col
        c = mix(c, "#000000", 0.18 * tone) if tone > 0.6 else c
        coin(f, cx_ + x * scale, base_y + y * scale, r * scale, alpha=alpha, rot=rot, squash=sq, col=c)


def chain(f, pts, prog=1.0, link=40, thick=9, col="#A9B0BA", alpha=1.0):
    """Verilen noktalardan geçen zincir (halkalar dönüşümlü)."""
    if prog <= 0:
        return
    path = sk.smooth_path(pts, False, 0.5) if len(pts) > 2 else sk.poly_path(pts, False)
    pm = skia.PathMeasure(path, False)
    L = pm.getLength() * clamp(prog)
    step = link * 0.72
    n = int(L / step) + 1
    for i in range(n):
        d = min(L, i * step)
        pos, tan = pm.getPosTan(d)
        if pos is None:
            continue
        ang = math.degrees(math.atan2(tan.y(), tan.x()))
        w = link if i % 2 == 0 else link * 0.46
        f.c.save()
        f.c.translate(pos.x(), pos.y())
        f.c.rotate(ang)
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -link * 0.3, w, link * 0.6), link * 0.3, link * 0.3)
        f.c.drawRRect(rr, f.paint("#000000", style="stroke", sw=thick + 3.5, alpha=0.55 * alpha))
        f.c.drawRRect(rr, f.paint(col, style="stroke", sw=thick, alpha=alpha))
        f.c.drawRRect(rr, f.paint(mix(col, "#FFFFFF", 0.55), style="stroke", sw=max(1.2, thick * 0.28), alpha=0.8 * alpha))
        f.c.restore()


def flame(f, x, y, h, t, lit=1.0, seed=0.0):
    """Mum alevi (tabanı (x,y))."""
    if lit <= 0:
        return
    fl = lit * (0.9 + 0.1 * math.sin(t * 11 + seed) + 0.05 * math.sin(t * 23 + seed * 2.3))
    fh, fw = h * fl, h * 0.34 * fl
    glow_disc(f, x, y - fh * 0.5, fh * 2.6, "#FFB347", 0.34 * lit)
    glow_disc(f, x, y - fh * 0.5, fh * 1.3, "#FFE0A0", 0.35 * lit)
    sway = math.sin(t * 7 + seed) * fw * 0.18
    p = skia.Path()
    p.moveTo(x + sway, y - fh)
    p.cubicTo(x + fw, y - fh * 0.45, x + fw * 0.9, y, x, y)
    p.cubicTo(x - fw * 0.9, y, x - fw, y - fh * 0.45, x + sway, y - fh)
    f.path(p, shader=f.lin(x, y - fh, x, y, [("#FFD36A", 0.0), ("#FF9A2E", 0.55), ("#C8501E", 1.0)]), alpha=lit)
    q = skia.Path()
    q.moveTo(x + sway * 0.6, y - fh * 0.62)
    q.cubicTo(x + fw * 0.45, y - fh * 0.3, x + fw * 0.4, y, x, y)
    q.cubicTo(x - fw * 0.4, y, x - fw * 0.45, y - fh * 0.3, x + sway * 0.6, y - fh * 0.62)
    f.path(q, color="#FFF4D0", alpha=0.9 * lit)


def candle(f, x, y, h, t, lit=1.0, w=None, wax="#EADCB5", seed=0.0, alpha=1.0, dim=0.0):
    """Mum: gövde tabanı (x,y), yükseklik h. lit 0..1 alev; dim 0..1 solukluk."""
    w = w or h * 0.26
    a = alpha * (1 - 0.6 * dim)
    wc = mix(wax, "#554A3A", dim)
    f.rect(x - w / 2, y - h, w, h, shader=f.lin(x - w / 2, 0, x + w / 2, 0, [(mix(wc, "#000000", 0.4), 0.0), (wc, 0.42), (mix(wc, "#000000", 0.55), 1.0)]), alpha=a)
    f.oval(x, y - h, w / 2, w * 0.17, color=mix(wc, "#FFFFFF", 0.18), alpha=a)
    f.line(x, y - h, x, y - h - h * 0.12, color="#1A1210", sw=max(2.0, w * 0.08), alpha=a)
    f.oval(x, y, w * 0.78, w * 0.2, color="#000000", alpha=0.35 * a, blur=4)
    if lit > 0:
        flame(f, x, y - h - h * 0.12, h * 0.55, t, lit=lit * alpha, seed=seed)


def smoke_wisp(f, x, y, t0, t, h=130, n=5, alpha=0.5, seed=1):
    """Sönen mumun dumanı: t0'dan sonra yükselen soluk lekeler."""
    dt = t - t0
    if dt <= 0:
        return
    rs = np.random.RandomState(seed)
    for i in range(n):
        ph = clamp((dt - i * 0.18) / 2.2)
        if ph <= 0 or ph >= 1:
            continue
        px = x + math.sin(ph * 5 + i * 1.7) * 16 * ph + (rs.rand() - 0.5) * 10
        py = y - ph * h
        r = 6 + ph * 22
        f.circle(px, py, r, color="#B8B2A8", alpha=alpha * (1 - ph) * math.sin(math.pi * min(1, ph * 3)) * 0.8, blur=r * 0.5)


def rays(f, name="night", alpha=0.3):
    """Ton adına göre ışık huzmesi (warm/cold/green/blood)."""
    sk._fast_blit(f, sk.rays_image(color=_RAYC.get(name, "#FFE2A0")), alpha=alpha, blend=skia.BlendMode.kPlus)


def ribbon(f, x, y, w, h, alpha=1.0, color="#EBDDB5", ink="#2A1A0C", notch=None):
    """Kırlangıç kuyruklu şerit (deviz bandı). (x,y) = merkez."""
    if alpha <= 0:
        return
    nt = notch if notch is not None else h * 0.5
    p = skia.Path()
    p.moveTo(x - w / 2, y - h / 2)
    p.quadTo(x, y - h / 2 + 16, x + w / 2, y - h / 2)
    p.lineTo(x + w / 2 - nt, y)
    p.lineTo(x + w / 2, y + h / 2)
    p.quadTo(x, y + h / 2 + 16, x - w / 2, y + h / 2)
    p.lineTo(x - w / 2 + nt, y)
    p.close()
    f.path(p, color="#000000", alpha=0.4 * alpha, blur=10)
    f.path(p, shader=f.lin(0, y - h / 2, 0, y + h / 2, [(mix(color, "#FFFFFF", 0.25), 0.0), (color, 0.5), (mix(color, "#6A5430", 0.5), 1.0)]), alpha=alpha)
    f.path(p, style="stroke", sw=4, color=ink, alpha=0.85 * alpha)
    q = skia.Path()
    q.moveTo(x - w / 2 + nt + 8, y - h / 2 + 12)
    q.quadTo(x, y - h / 2 + 24, x + w / 2 - nt - 8, y - h / 2 + 12)
    f.path(q, style="stroke", sw=1.6, color=ink, alpha=0.45 * alpha)


def puffs(f, x, y, t, w=220, h=380, n=8, seed=4, color="#1A1410", alpha=0.35):
    """Hafif duman: katman bulanıklığı yok, daire başına maske bulanıklığı (sk.smoke'tan ~5x hızlı)."""
    rs = np.random.RandomState(seed)
    for i in range(n):
        ph = (t * 0.18 + rs.rand()) % 1.0
        px = x + (rs.rand() - 0.5) * w * 0.5 + math.sin(ph * 6 + i) * w * 0.18 * ph
        py = y - ph * h
        r = 26 + ph * 90 + rs.rand() * 18
        a = alpha * math.sin(math.pi * ph) ** 1.2
        f.circle(px, py, r, color=color, alpha=a, blur=r * 0.55)


# ───────────────────────────── terazi ─────────────────────────────
def _gold_grad(f, x0, x1, y0=0, y1=0, metal="gold"):
    st = sk.METAL[metal]
    return f.lin(x0, y0, x1, y1, [(c, p) for c, p in st])


def draw_scale(f, x, y, L, tilt, left=None, right=None, alpha=1.0, metal="gold", t=0.0):
    """Terazi. (x,y) = kolun ekseni; L = kolun yarı uzunluğu; tilt (rad, +: sağ kefe aşağı).
    left/right = fn(f, cx, cy) kefe merkezine (kefenin üstü) çizilen içerik."""
    if alpha <= 0:
        return
    base_y = y + L * 1.55
    if alpha < 1:
        f.layer_begin(alpha=alpha)
    # ayak/gövde
    f.oval(x, base_y + 6, L * 0.62, L * 0.1, color="#000000", alpha=0.4, blur=8)
    f.path(sk.smooth_path([(x - L * 0.55, base_y + 4), (x - L * 0.36, base_y - L * 0.1), (x + L * 0.36, base_y - L * 0.1), (x + L * 0.55, base_y + 4)], True, 0.25), shader=_gold_grad(f, x - L * 0.5, x + L * 0.5, metal=metal))
    f.path(sk.smooth_path([(x - L * 0.55, base_y + 4), (x - L * 0.36, base_y - L * 0.1), (x + L * 0.36, base_y - L * 0.1), (x + L * 0.55, base_y + 4)], True, 0.25), style="stroke", sw=3, color="#3A2610", alpha=0.8)
    f.rect(x - L * 0.045, y, L * 0.09, base_y - y, shader=_gold_grad(f, x - L * 0.05, x + L * 0.05, metal=metal))
    f.rect(x - L * 0.045, y, L * 0.09, base_y - y, style="stroke", sw=2.5, color="#3A2610", alpha=0.7)
    for k in range(3):
        yy = y + (base_y - y) * (0.3 + 0.2 * k)
        f.rect(x - L * 0.08, yy, L * 0.16, L * 0.05, shader=_gold_grad(f, x - L * 0.08, x + L * 0.08, metal=metal))
    # kol
    ca, sa = math.cos(tilt), math.sin(tilt)
    lx, ly, rx, ry = x - L * ca, y - L * sa, x + L * ca, y + L * sa
    S = L * 1.0
    for (px, py, fn_) in ((lx, ly, left), (rx, ry, right)):
        cx_, cy_ = px, py + S
        f.line(px, py, cx_ - L * 0.38, cy_, color="#000000", sw=5, alpha=0.5)
        f.line(px, py, cx_ + L * 0.38, cy_, color="#000000", sw=5, alpha=0.5)
        f.line(px, py, cx_ - L * 0.38, cy_, color="#D9B65A", sw=2.4, alpha=0.95)
        f.line(px, py, cx_ + L * 0.38, cy_, color="#D9B65A", sw=2.4, alpha=0.95)
        if fn_ is not None:
            fn_(f, cx_, cy_)
        pan = skia.Path()
        pan.moveTo(cx_ - L * 0.44, cy_)
        pan.cubicTo(cx_ - L * 0.36, cy_ + L * 0.2, cx_ + L * 0.36, cy_ + L * 0.2, cx_ + L * 0.44, cy_)
        pan.close()
        f.path(pan, shader=_gold_grad(f, cx_ - L * 0.44, cx_ + L * 0.44, metal=metal))
        f.path(pan, style="stroke", sw=3, color="#3A2610", alpha=0.85)
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(math.degrees(tilt))
    beam = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-L, -L * 0.045, L, L * 0.045), L * 0.045, L * 0.045)
    f.c.drawRRect(beam, skia.Paint(AntiAlias=True, Shader=_gold_grad(f, 0, 0, -L * 0.05, L * 0.05, metal=metal)))
    f.c.drawRRect(beam, f.paint("#3A2610", style="stroke", sw=2.5, alpha=0.85))
    for sg in (-1, 1):
        f.c.drawCircle(sg * L, 0, L * 0.06, f.paint("#E3B54A"))
        f.c.drawCircle(sg * L, 0, L * 0.06, f.paint("#3A2610", style="stroke", sw=2.2, alpha=0.9))
    f.c.restore()
    f.circle(x, y, L * 0.1, shader=f.rad(x - L * 0.03, y - L * 0.03, L * 0.16, [("#FBE9A6", 0.0), ("#C9962B", 0.6), ("#6B4A12", 1.0)]))
    f.circle(x, y, L * 0.1, style="stroke", sw=2.5, color="#3A2610", alpha=0.85)
    if alpha < 1:
        f.layer_end()


# ───────────────────────────── kabartma simgeler (kendi) ─────────────────────────────
@icons.icon("c2_kurhut")
def _i_kurhut(m):
    """Seçmen şapkası (Kurhut): kürk bant + kubbe + kemer + yuvarlak/haç."""
    m.smooth([(128, 340), (128, 246), (184, 158), (256, 128), (328, 158), (384, 246), (384, 340)], close=True, t=0.35)
    arc = skia.Path()
    arc.moveTo(150, 330)
    arc.cubicTo(150, 190, 220, 128, 256, 120)
    arc.cubicTo(292, 128, 362, 190, 362, 330)
    m.cut(arc, 7)
    m.rect(104, 318, 304, 112, r=48)
    for (x, y) in ((156, 384), (220, 396), (292, 396), (356, 384)):
        m.cut(sk.smooth_path([(x, y - 22), (x + 10, y), (x, y + 24), (x - 10, y)], True, 0.5))
        m.cut(sk.poly_path([(x - 3, y + 20), (x + 3, y + 20), (x + 2, y + 44), (x - 2, y + 44)], True))
    m.circle(256, 100, 24)
    m.rect(250, 52, 12, 34)
    m.rect(238, 62, 36, 11)


@icons.icon("c2_sutun")
def _i_sutun(m):
    """Herkül Sütunu: gövde (oluklu), başlık, kaide, tepede küçük taç."""
    m.poly([(212, 148), (300, 148), (310, 410), (202, 410)])
    for dx in (-30, -10, 10, 30):
        m.cut(sk.poly_path([(256 + dx * 0.8, 160), (256 + dx, 404)], False), 4)
    m.rect(170, 118, 172, 34, r=8)
    m.circle(186, 134, 17)
    m.circle(326, 134, 17)
    m.rect(158, 98, 196, 26, r=6)
    m.rect(184, 408, 144, 28, r=6)
    m.rect(164, 436, 184, 30, r=8)
    m.smooth([(196, 100), (196, 70), (224, 86), (256, 50), (288, 86), (316, 70), (316, 100)], close=True, t=0.2)
    m.circle(256, 46, 12)


@icons.icon("c1_sarmal")
def _i_sarmal(m):
    """Sarmal (delilik): halka içinde dönen spiral."""
    ring = skia.Path()
    ring.addCircle(256, 256, 196)
    m.stroke(ring, 20)
    pts = []
    for i in range(0, 135):
        th = i * 0.115
        r = 8 + th * 11.5
        pts.append((256 + r * math.cos(th), 256 + r * math.sin(th)))
    m.stroke(sk.smooth_path(pts, False, 0.5), 22)
    m.circle(pts[0][0], pts[0][1], 16)


@icons.icon("c1_gul")
def _i_gul(m):
    """Gül (üstten görünüm): tırtıklı taç yapraklar + sarmal çizgiler."""
    for k in range(9):
        a = k * math.tau / 9
        m.circle(256 + 118 * math.cos(a), 256 + 118 * math.sin(a), 66)
    m.circle(256, 256, 150)
    pts = []
    for i in range(0, 90):
        th = i * 0.17
        r = 6 + th * 8.2
        pts.append((256 + r * math.cos(th), 256 + r * math.sin(th)))
    m.cut(sk.smooth_path(pts, False, 0.5), 7)
    for k in range(9):
        a = k * math.tau / 9 + 0.3
        m.cut(sk.smooth_path([(256 + 110 * math.cos(a), 256 + 110 * math.sin(a)), (256 + 168 * math.cos(a + 0.35), 256 + 168 * math.sin(a + 0.35))], False), 6)


@icons.icon("c1_at")
def _i_at(m):
    """At başı (satranç atı profili, sola bakar)."""
    pts = [(286, 58), (266, 92), (236, 108), (184, 172), (120, 252), (100, 282), (116, 312), (160, 308), (198, 282),
           (238, 308), (272, 352), (250, 410), (394, 410), (410, 330), (396, 250), (360, 172), (330, 112), (306, 82)]
    m.smooth(pts, close=True, t=0.3)
    m.poly([(286, 52), (262, 98), (300, 90)])
    m.rect(120, 408, 292, 40, r=12)
    m.rect(146, 440, 240, 30, r=10)
    m.cut(sk.smooth_path([(104, 292), (130, 296), (156, 290)], False), 5)
    m.cut(sk.smooth_path([(210, 182), (222, 176), (234, 184)], False), 6)
    m.circle(222, 188, 8, 0)
    m.circle(114, 278, 6, 0)
    for k in range(6):
        y = 130 + k * 42
        m.cut(sk.smooth_path([(352 + k * 3, y), (330 + k * 3, y + 40)], False), 5)


@icons.icon("c10_sandik")
def _i_sandik(m):
    """Sandık: kubbeli kapak, bantlar, kilit."""
    lid = skia.Path()
    lid.moveTo(92, 258)
    lid.cubicTo(92, 170, 170, 138, 256, 138)
    lid.cubicTo(342, 138, 420, 170, 420, 258)
    lid.close()
    m.fill(lid)
    m.rect(92, 252, 328, 176, r=14)
    m.cut(sk.smooth_path([(92, 256), (256, 270), (420, 256)], False), 7)
    for x in (168, 344):
        m.cut(sk.poly_path([(x, 150), (x, 428)], False), 8)
    m.rect(222, 236, 68, 74, r=10, v=255)
    m.cut(sk.poly_path([(222, 236), (290, 236), (290, 310), (222, 310)], True), 6)
    m.circle(256, 266, 10, 0)
    m.poly([(250, 270), (262, 270), (264, 294), (248, 294)], 0)
    for (x, y) in ((118, 290), (394, 290), (118, 400), (394, 400)):
        m.circle(x, y, 8, 0)


@icons.icon("c10_dag")
def _i_dag(m):
    """Dağ (Potosí tepesi): iri zirve + yan zirve + maden ağzı."""
    m.poly([(36, 430), (150, 262), (196, 300), (286, 100), (344, 206), (386, 170), (476, 430)])
    m.cut(sk.poly_path([(286, 100), (262, 190), (296, 250), (270, 330)], False), 6)
    m.cut(sk.poly_path([(150, 262), (176, 330), (150, 390)], False), 5)
    m.cut(sk.poly_path([(386, 170), (364, 260), (400, 340)], False), 5)
    arch = skia.Path()
    arch.moveTo(236, 430)
    arch.lineTo(236, 372)
    arch.cubicTo(236, 336, 296, 336, 296, 372)
    arch.lineTo(296, 430)
    arch.close()
    m.cut(arch)


@icons.icon("c1_besik")
def _i_besik(m):
    """Beşik: yay tabanlı sepet + başlık."""
    bowl = skia.Path()
    bowl.moveTo(86, 238)
    bowl.cubicTo(110, 360, 190, 388, 256, 388)
    bowl.cubicTo(322, 388, 402, 360, 426, 238)
    bowl.close()
    m.fill(bowl)
    hood = skia.Path()
    hood.moveTo(86, 238)
    hood.cubicTo(80, 140, 150, 110, 200, 130)
    hood.cubicTo(180, 170, 186, 210, 206, 238)
    hood.close()
    m.fill(hood)
    m.cut(sk.smooth_path([(120, 262), (256, 292), (392, 262)], False), 7)
    m.stroke(sk.smooth_path([(96, 410), (256, 448), (416, 410)], False, 0.5), 16)
    m.circle(256, 300, 4, 0)


# ───────────────────────────── güvenli figür çizimi ─────────────────────────────
_FW = set()


def fig(f, kind, x, y, h, **kw):
    """ST.figure sarmalayıcı: figür-lab modülü yarım/hatalıysa tek uyarı basıp o figürü atlar (önizleme çökmesin)."""
    try:
        ST.figure(f, kind, x, y, h, **kw)
    except Exception as e:  # noqa: BLE001
        key = (kind, type(e).__name__)
        if key not in _FW:
            _FW.add(key)
            import sys
            print(f"[kit_a.fig] '{kind}' figürü hata verdi: {type(e).__name__}: {e}", file=sys.stderr)


def crowd(f, rows, x0, x1, y0, dy, h0, hs, kinds, col="#0C0705", rim="#8A5A2A", seed=1, dens=70, face=1, depth_fog=None):
    """ST.crowd ile aynı, K.fig üzerinden."""
    rs = np.random.RandomState(seed)
    for r in range(rows):
        y = y0 + r * dy
        h = h0 * (hs ** r)
        n = int((x1 - x0) / (dens * (hs ** r)))
        for k in range(n):
            x = x0 + (k + rs.rand() * 0.8) * (x1 - x0) / max(1, n)
            kind = kinds[rs.randint(len(kinds))]
            cc = col if depth_fog is None else mix(col, depth_fog, 0.5 * (1 - r / max(1, rows - 1)))
            fig(f, kind, x, y + rs.randn() * 3, h * (0.92 + 0.16 * rs.rand()), col=cc, rim=rim, face=face if rs.rand() > 0.15 else -face, alpha=1.0, lean=(rs.rand() - 0.5) * 0.04)


# ───────────────────────────── güvenli diorama sarmalayıcı ─────────────────────────────
_WARNED = set()


@SH.kind("a_theatre")
def k_a_theatre(cx, **kw):
    """Diorama çekimi; lab sahnesi yarım/hatalıysa yer tutucu çizer (önizleme/Program çökmesin)."""
    try:
        SH.KINDS["theatre"](cx, **kw)
    except Exception as e:  # noqa: BLE001
        f = cx.f
        key = (kw.get("scene"), type(e).__name__)
        if key not in _WARNED:
            _WARNED.add(key)
            import sys
            print(f"[a_theatre] '{kw.get('scene')}' sahnesi hata verdi: {type(e).__name__}: {e}", file=sys.stderr)
        f.rect(0, 0, W, H, shader=f.lin(0, 0, 0, H, [("#241509", 0.0), ("#0D0704", 1.0)]))
        f.text(f"[sahne hata: {kw.get('scene')}]", W / 2, H / 2, face="cap_i", size=44, color="#8A7A55", align="c")
        f.vig(0.6)


# ───────────────────────────── çoklu madalya (çapa destekli) ─────────────────────────────
@SH.kind("a_medals")
def k_a_medals(cx, items=(), size=520, y=H * 0.46, gap=None, bgname=None, vs=None, vs_icon="swords", vs_size=120, plates=True, stampt=None, rays=0.3, dust_n=50, vig=0.55, date=None, ghost=True):
    """Yan yana madalyalar; `at` değerleri çapa olabilir. items: dict(key,name,role,dates,at,metal,flip,size,dx,y)."""
    f = cx.f
    if bgname:
        bg(f, bgname)
        f.rays = lambda alpha=1.0, **kk: sk._fast_blit(f, sk.rays_image(color=_RAYC[bgname]), alpha=alpha, blend=skia.BlendMode.kPlus)
        f.rays(alpha=rays)
        del f.rays
    else:
        f.bg("night")
        f.rays(alpha=rays)
    n = len(items)
    gap = gap or min(size * 1.15, (W - 200) / max(1, n))
    x0 = W / 2 - gap * (n - 1) / 2
    for i, it in enumerate(items):
        a_ = it.get("at", 0.2 + 0.3 * i)
        a = cx.amt(a_, 0.7)
        x = x0 + i * gap + it.get("dx", 0)
        yy = it.get("y", y)
        sz = it.get("size", size)
        if ghost and a < 1:
            f.circle(x, yy, sz * 0.46, style="stroke", sw=3, color="#C9962B", alpha=0.35 * (1 - a))
            f.circle(x, yy, sz * 0.46, color="#000000", alpha=0.25 * (1 - a))
        if a <= 0:
            continue
        sc = (0.92 + 0.08 * ease_out(a)) * (1.0 + 0.03 * cx.u)
        gl = (cx.t * 0.25 + 0.2 * i) % 2.0
        SH.draw_medal(f, it["key"], x, yy, sz * sc, it.get("metal", "gold"), it.get("flip", False), alpha=a, tilt=0.15 * math.sin(cx.t * 0.5 + i), glint=gl if gl < 1 else None,
                      inscription=it.get("ins", True))
        if plates and it.get("name"):
            SH.name_plate(f, it["name"], it.get("role"), it.get("dates"), cx_=x, y=yy + sz * 0.52, t=cx.amt(a_, 0.5, off=0.4), w=min(gap - 20, it.get("pw", 520)))
    if vs is not None:
        icons.draw_icon(f, vs_icon, W / 2, y, size=vs_size, metal="silver", alpha=cx.amt(vs, 0.4), glow=0.3)
    sk.dust(f, cx.t, n=dust_n)
    f.vig(vig)
    if date:
        SH._date_stamp(f, date, cx)
    if stampt:
        SH.stamp(f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 64)


# ───────────────────────────── ek harita bölgeleri (lon/lat → dünya pikseli; kıyıya gerçek ülke çokgenleriyle kırpılır) ─────────────────────────────
_CNT = None


def countries():
    global _CNT
    if _CNT is None:
        import mapdata
        _CNT = mapdata._countries()
    return _CNT


def _region_builders():
    from shapely.geometry import Polygon
    from shapely.ops import unary_union

    def P(pts):
        return Polygon(pts).buffer(0)
    aragon = [(-1.8, 42.8), (0.7, 42.95), (3.4, 42.5), (4.6, 42.0), (4.6, 38.3), (0.3, 37.6), (-0.9, 37.7), (-1.3, 38.4), (-1.55, 39.6), (-1.95, 40.8), (-2.0, 41.8)]
    B = {
        "c1_flandre": lambda C: unary_union([C["France"], C["Belgium"], C["Netherlands"]]).intersection(
            P([(2.4, 51.2), (3.6, 51.7), (4.3, 51.5), (4.15, 51.0), (4.15, 50.85), (3.85, 50.6), (3.3, 50.5), (2.9, 50.68), (2.55, 50.8), (2.4, 51.0)])),
        "c1_aragon": lambda C: C["Spain"].intersection(P(aragon)),
        # Navarra (1500'de bağımsız; Kastilya'ya 1512–15'te katıldı) kuzeydoğuda ince bir kama bırakıyordu: çıkarılır
        "c1_kastilya": lambda C: C["Spain"].difference(P(aragon)).difference(P([(-1.85, 42.45), (-1.85, 44.2), (1.0, 44.2), (1.0, 42.45)])),
        "c3_castilla_leon": lambda C: C["Spain"].intersection(P([(-6.9, 42.9), (-6.0, 43.3), (-4.5, 43.3), (-3.2, 43.1), (-3.0, 42.7), (-2.6, 42.3), (-2.0, 42.1), (-1.9, 41.3),
                                                                  (-2.5, 41.1), (-3.2, 41.0), (-3.8, 40.7), (-4.6, 40.2), (-5.2, 40.0), (-5.9, 40.3), (-6.7, 40.3), (-6.9, 40.9), (-6.5, 41.5), (-6.9, 41.9), (-7.1, 42.5)])),
        "c3_valensiya": lambda C: C["Spain"].intersection(P([(-0.3, 40.9), (0.8, 40.9), (1.4, 39.0), (0.2, 37.8), (-0.8, 37.8), (-1.3, 38.4), (-1.45, 39.4), (-1.2, 40.3)])),
        "c10_venezuela": lambda C: C["Venezuela"],
    }
    return B


_RB = None


def ensure_region(name):
    global _RB
    mv = SH.mapview()
    if name in mv.D["regions"]:
        return
    import mapdata
    if _RB is None:
        _RB = _region_builders()
    g = _RB[name](countries())
    mv.D["regions"][name] = mapdata._levels(mapdata._project(g))
    for k in [k for k in mv._paths if isinstance(k, tuple) and k[0] == name]:
        del mv._paths[k]


_RELIEF = {}


def _relief_shader():
    """Dünya koordinatında kusursuz döşenen (FFT, periyodik) kesirli arazi + gölgelendirme (hillshade): kara üstüne tepe/sırt dokusu."""
    if "sh" not in _RELIEF:
        N = 1024
        rs = np.random.RandomState(11)
        F = np.fft.rfft2(rs.randn(N, N).astype(np.float32))
        fy = np.fft.fftfreq(N)[:, None]
        fx = np.fft.rfftfreq(N)[None, :]
        fr = np.sqrt(fx * fx + fy * fy)
        fr[0, 0] = 1.0
        filt = 1.0 / fr ** 1.75
        filt[0, 0] = 0.0
        h = np.fft.irfft2(F * filt, s=(N, N)).astype(np.float32)
        h = (h - h.mean()) / (h.std() + 1e-6)
        t = np.tanh(h * 0.85)
        hh = 0.62 * (1.0 - np.abs(t)) ** 1.5 + 0.38 * (t * 0.5 + 0.5)
        dx = (np.roll(hh, -1, 1) - np.roll(hh, 1, 1)) * 0.5
        dy = (np.roll(hh, -1, 0) - np.roll(hh, 1, 0)) * 0.5
        shade = -(dx * 0.72 + dy * 0.69)
        shade = shade / (shade.std() + 1e-6)
        g = 128.0 + shade * 26.0 + t * 15.0
        img = sk.gray_to_image(np.clip(g, 0, 255).astype(np.uint8))
        _RELIEF["sh"] = img.makeShader(skia.TileMode.kRepeat, skia.TileMode.kRepeat, skia.SamplingOptions(skia.FilterMode.kLinear))
    return _RELIEF["sh"]


def _patched_base(mv, relief):
    """mv.base yerine geçer: kara kabartması ve renk tonu (tint) döşeme önbelleğine pişirilir (kare başına ek maliyet yok).
    Yalnız bu çekim süresince, yalnız bu MapView örneğinde; stil adı 'night_rel…' ile ayrı döşeme anahtarı."""
    orig = type(mv).base

    def base2(f, cam, style="night", t=0.0, mountains=True, ripples=True, tint=None):
        if style != "night" or cam.rot:
            return orig(mv, f, cam, style, t=t, mountains=mountains, ripples=ripples, tint=tint)
        o_dbv, o_sea = type(mv)._draw_base_vector, type(mv).sea
        tcol, talpha = (tint[0], float(tint[1])) if tint else (None, 0.0)
        sname = "night_rel%d_%s_%d" % (int(round(relief * 100)), (tcol or "none").lstrip("#"), int(round(talpha * 100)))

        def dbv(fr, cam_apply, z, st, mtn, rip):
            if st != sname:
                return o_dbv(mv, fr, cam_apply, z, st, mtn, rip)
            o_dbv(mv, fr, cam_apply, z, "night", mtn, rip)
            c = fr.c
            c.save()
            cam_apply(c)
            land = mv.path("__kara__", z)
            pt = skia.Paint(AntiAlias=True)
            pt.setShader(_relief_shader())
            pt.setBlendMode(skia.BlendMode.kSoftLight)
            pt.setAlphaf(relief)
            c.drawPath(land, pt)
            if tcol:
                c.drawPath(land, fr.paint(tcol, alpha=talpha))
            c.restore()

        def sea2(ff, st="night"):
            return o_sea(mv, ff, "night" if st == sname else st)
        mv._draw_base_vector, mv.sea = dbv, sea2
        try:
            orig(mv, f, cam, sname, t=t, mountains=mountains, ripples=ripples, tint=None)
        finally:
            del mv._draw_base_vector, mv.sea
    return base2


_PREBAKED = set()
_SCRATCH = {}


def _prebake_tiles(cx, mv, kw):
    """Kamera yolu boyunca örnekleyip gerekli harita döşemelerini çekimin ilk karesinde pişirir:
    sonraki karelerde döşeme üretimi (≈0.4–1.2 sn'lik sıçrama) olmaz → kare süreleri düzgün."""
    import mapsk
    cams = kw.get("cams")
    if not cams or kw.get("style", "night") != "night":
        return
    ks = [(cx.at(a), v) for a, v in cams]
    t0, t1 = max(0.0, ks[0][0]), min(float(cx.dur), ks[-1][0])
    if t1 - t0 < 0.05:
        return
    if "f" not in _SCRATCH:
        _SCRATCH["f"] = sk.Frame(W, H)
    fr = _SCRATCH["f"]
    n = min(40, int((t1 - t0) / 0.12) + 1)
    for q in range(n + 1):
        t = t0 + (t1 - t0) * q / n
        if t <= ks[0][0]:
            cm = mapsk.Cam(*ks[0][1])
        elif t >= ks[-1][0]:
            cm = mapsk.Cam(*ks[-1][1])
        else:
            cm = mapsk.Cam(*ks[0][1])
            for (ta, va), (tb, vb) in zip(ks[:-1], ks[1:]):
                if ta <= t <= tb:
                    cm = mapsk.cam_move(va, vb, (t - ta) / max(1e-6, tb - ta))
                    break
        mv.base(fr, cm, "night", t=t, mountains=kw.get("mountains", True), ripples=kw.get("ripples", True), tint=kw.get("tint"))


@SH.kind("a_map")
def k_a_map(cx, need=(), stampt=None, relief=0.55, **kw):
    """Harita çekimi + gerekli özel bölgeleri (c1_aragon …) ilk kullanımda üretir; kara üstüne (döşemeye pişmiş) kabartma dokusu ve ton;
    kamera yolundaki döşemeler çekimin ilk karesinde önceden pişirilir; isteğe bağlı damga."""
    for n in need:
        ensure_region(n)
    mv = SH.mapview()
    if relief:
        mv.base = _patched_base(mv, relief)
        key = (repr(kw.get("cams")), repr(kw.get("tint")), relief, repr(kw.get("mountains", True)), repr(kw.get("ripples", True)))
        if key not in _PREBAKED:
            _PREBAKED.add(key)
            try:
                _prebake_tiles(cx, mv, kw)
            except Exception as e:  # noqa: BLE001  (ön pişirme yalnız hız içindir; hata kareyi bozmasın)
                import sys
                print(f"[a_map] ön pişirme atlandı: {type(e).__name__}: {e}", file=sys.stderr)
    try:
        SH.KINDS["map"](cx, **kw)
    finally:
        if relief and "base" in mv.__dict__:
            del mv.base
    if stampt:
        SH.stamp(cx.f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 64)


def _with_stamp(name, base):
    def k(cx, stampt=None, **kw):
        SH.KINDS[base](cx, **kw)
        if stampt:
            SH.stamp(cx.f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 64)
    SH.KINDS[name] = k


for _b in ("timeline", "bars", "counter", "stacked", "tree", "iconrow"):
    _with_stamp(f"a_{_b}_s", _b)


# ───────────────────────────── soy ağacı (dirsekli bağlantılar, etiketlerin altından) ─────────────────────────────
def _bracket(xa, y0, xb, y1, ybus, r=16):
    """(xa,y0) → aşağı → yatay (ybus) → aşağı (xb,y1): yuvarlak köşeli dirsekli bağlantı."""
    p = skia.Path()
    p.moveTo(xa, y0)
    if abs(xb - xa) < 2 * r:
        p.lineTo(xa, ybus)
        p.lineTo(xb, ybus)
        p.lineTo(xb, y1)
        return p
    d = 1.0 if xb > xa else -1.0
    p.lineTo(xa, ybus - r)
    p.quadTo(xa, ybus, xa + d * r, ybus)
    p.lineTo(xb - d * r, ybus)
    p.quadTo(xb, ybus, xb, ybus + r)
    p.lineTo(xb, y1)
    return p


@SH.kind("a_tree")
def k_a_tree(cx, nodes=(), edges=(), at=0.0, bgk="night", title=None, size=210, edge_dur=0.8):
    """shots.tree'nin düzeltilmiş kopyası: bağlantılar ebeveynin ad/tarih etiketinin ALTINDAN başlar, yatay bir dirsekle çocuğun
    madalyasının üstüne iner (özgün sürümde eğriler ad yazılarının içinden geçiyordu); çizgiler madalyaların arkasında çizilir."""
    f = cx.f
    f.bg(bgk)
    f.rays(alpha=0.25)
    sk.dust(f, cx.t, n=40, alpha=0.4)
    pos = {n["id"]: (n["x"] * W, n["y"] * H) for n in nodes}
    sz = {n["id"]: n.get("size", size) for n in nodes}
    has_dates = {n["id"]: bool(n.get("dates")) for n in nodes}
    if title:
        SH.kicker(f, title, W / 2, 110, alpha=cx.amt(at, 0.6), size=30, track=10, face="title_m", color="#E0C682")

    def y_start(i):
        return pos[i][1] + sz[i] / 2 + (84 if has_dates[i] else 58)
    bus = {}
    for e in edges:
        b_ = e[1]
        bus[b_] = max(bus.get(b_, 0), y_start(e[0]))
    for e in edges:
        a_, b_ = e[0], e[1]
        ta = e[2] if len(e) > 2 else at
        col = e[3] if len(e) > 3 else "#C9962B"
        k = ease_out(clamp((cx.t - cx.at(ta)) / edge_dur), 2)
        if k <= 0:
            continue
        (xa, ya), (xb, yb) = pos[a_], pos[b_]
        y0 = y_start(a_)
        y1 = yb - sz[b_] / 2 - 10
        ybus = bus[b_] + (y1 - bus[b_]) * 0.45
        p = _bracket(xa, y0, xb, y1, ybus)
        pm = skia.PathMeasure(p, False)
        part = skia.Path()
        pm.getSegment(0, pm.getLength() * k, part, True)
        f.path(part, style="stroke", sw=9, color="#000000", alpha=0.45)
        f.path(part, style="stroke", sw=4, color=col, alpha=0.95)
        if k > 0.98:
            f.circle(xb, y1, 5, color=col, alpha=0.95)
    for n in nodes:
        ta = n.get("at", at)
        k = cx.amt(ta, 0.6)
        if k <= 0:
            continue
        x, y = pos[n["id"]]
        s_ = n.get("size", size) * (0.88 + 0.12 * ease_out(k))
        if n.get("key"):
            SH.draw_medal(f, n["key"], x, y, s_, n.get("metal", "gold"), n.get("flip", False), alpha=k, inscription=n.get("ins", False))
        elif n.get("icon"):
            icons.draw_icon(f, n["icon"], x, y, size=s_ * 0.8, metal=n.get("metal", "gold"), alpha=k, glow=0.25)
        if n.get("name"):
            f.text(n["name"], x, y + s_ / 2 + 38, face="title_m", size=n.get("nsize", 25), color="#F0DDA0", align="c", track=3, alpha=k, shadow=(2, 2, 3, "#000000"))
        if n.get("dates"):
            f.text(n["dates"], x, y + s_ / 2 + 68, face="cap_i", size=22, color="#B9A674", align="c", alpha=k * 0.9)
        if n.get("tag"):
            f.text(n["tag"], x, y - s_ / 2 - 16, face="cap_b", size=24, color="#F6D77A", align="c", track=4, alpha=k)
    f.vig(0.55)


# ───────────────────────────── düzeltilmiş belge (doc) ─────────────────────────────
@SH.kind("a_doc")
def k_a_doc(cx, title="", lines=(), w=1100, h=760, at=0.0, line_dt=0.35, ink="#2A1A0C", seal=None, seal_at=None, tone="#EBDDB5",
            rot=-0.015, zoom=0.06, hl=None, hl_at=None, hl_color="#C9962B", face="fell", size=40, head_size=50, bgk="night", pan=(0, 0),
            caption=None, stampt=None, date=None, align="l"):
    """shots.doc'un düzeltilmiş kopyası: (1) kâğıt tohumu süreçler arası kararlı (crc32; hash() her süreçte değişir → kâğıt kenarı titrerdi),
    (2) ortalı (align='c') satırlarda açılış kırpması metnin kendi sol kenarından başlar (özgün sürüm satırın sağını hiç açmıyordu)."""
    import zlib
    f = cx.f
    f.bg(bgk)
    f.rays(alpha=0.25)
    img, pad = SH.paper_sprite(w, h, seed=zlib.crc32(title.encode("utf-8")) % 97 + 3, tone=tone)
    a = cx.amt(at, 0.7)
    sc = (1.0 + zoom * cx.u) * (0.96 + 0.04 * ease_out(a))
    cxp, cyp = W / 2 + pan[0] * cx.u, H * 0.5 + pan[1] * cx.u
    f.c.save()
    f.c.translate(cxp, cyp)
    f.c.rotate(math.degrees(rot * (1 - 0.4 * cx.u)))
    f.c.scale(sc, sc)
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(a)
    f.c.drawImage(img, -w / 2 - pad, -h / 2 - pad, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    y = -h / 2 + 90
    if title:
        tsz = SH.fit_size(title, "fell", head_size, w - 160, 2)
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
            x_left = (-wt / 2) if align == "c" else xs
            f.c.save()
            f.c.clipRect(skia.Rect.MakeXYWH(x_left - 8, y - size, (wt + 24) * prog, size * 1.6))
            if align == "c":
                f.text(text, 0, y, face=face, size=size, color=ink, align="c", alpha=a)
            else:
                f.text(text, xs, y, face=face, size=size, color=ink, align="l", alpha=a)
            f.c.restore()
        y += size * 1.42
    if hl and hl_at is not None:
        k = clamp((cx.t - cx.at(hl_at)) / 0.6)
        hx, hy, hw = hl
        f.rect(hx, hy - size * 0.9, hw * k, size * 1.25, color=hl_color, alpha=0.22 * a, blur=6)
        f.line(hx, hy + 8, hx + hw * k, hy + 8, color=hl_color, sw=4.5, alpha=0.95 * a)
    if date:
        f.text(date, w / 2 - 90, h / 2 - 54, face="fell_i", size=34, color=ink, align="r", alpha=a * 0.9)
    if seal:
        SH.wax_seal(f, w / 2 - 150, h / 2 - 90, 58, color=seal if isinstance(seal, str) else "#8E1F26", t=cx.amt(seal_at if seal_at is not None else at + 1.4, 0.35), alpha=a, mono="K")
    f.c.restore()
    if caption:
        SH.kicker(f, caption, W / 2, H - 70, alpha=cx.amt(at + 0.6, 0.6), size=24, track=6, face="cap_i", color="#B9A674")
    if stampt:
        SH.stamp(f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 60)
    sk.dust(f, cx.t, n=40, alpha=0.35)
    f.vig(0.5)


# ───────────────────────────── taban türlerin tonlu varyantları ─────────────────────────────
def register_variants():
    for base in ("medal", "medals", "doc", "quote", "counter", "bars", "stacked", "timeline", "emblem", "tree", "iconrow"):
        for pre, bgn in (("g_", "green"), ("c_", "cold"), ("r_", "blood")):
            variant(f"a_{pre}{base}", "a_doc" if base == "doc" else base, bgn)


register_variants()
