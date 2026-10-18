"""Bölüm yazarı B (c4, c5, c11) — ortak yardımcılar (ortak kit dosyalarına dokunmadan).

İçerik: sağlam çapa üretici (anc), kamera itmesi (push), parşömen bağlamı (paper), damga (stamp2, doku/aşınmalı), etiket (tag),
mürekkep açılımı (reveal), karalama satırları (scribbles), kırmızı çizgi (strike), eğri ok (curve_arrow), parıltı (glow), siyaha çözülme (fadeout),
çift ışık (duo_glow) ve küçük çizim ilkelleri.
"""
import math
from contextlib import contextmanager

import numpy as np
import skia

import icons
import icons_b  # noqa: F401  (b_ simgelerini kaydeder)
import shots as SH
import sk
from sk import C, H, W, back_out, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth


# ───────────────────────────── çapalar ─────────────────────────────
def anc(sid, key=None, off=0.0, fb=None, nth=0):
    """Çapa: (sid, key, off). Sözcük zaman çizelgesinde yoksa (metin yaması öncesi/sonrası) cümle başından fb sn'ye düşer."""
    if key is None:
        return (sid, off)
    try:
        SH.timeline().word(sid, key, nth=nth)
    except KeyError:
        return (sid, (fb if fb is not None else 0.0) + off)
    return (sid, key, nth, off) if nth else (sid, key, off)


def shift(a, d):
    """Çapayı d sn kaydır (sayı: yerel sn; (sid,off) / (sid,key,off) / (sid,key,nth,off) biçimleri)."""
    if isinstance(a, (int, float)):
        return a + d
    a = tuple(a)
    return a[:-1] + (a[-1] + d,)


def t_end(cx, sid, key=None):
    """Cümlenin (ya da sözcüğün) BİTİŞİ → çekim-yerel sn."""
    tl = cx.tl
    if key is None:
        return tl.t1(sid) - cx.sh.t0
    return tl.word(sid, key, end=True) - cx.sh.t0


# ───────────────────────────── kamera ─────────────────────────────
@contextmanager
def push(cx, z0=1.0, z1=1.06, pan=(0.0, 0.0), c=(W / 2, H / 2), ease=smooth):
    """Çekim boyunca yavaş itme/çekme + kayma. `with push(cx, 1.0, 1.06): ...` — içine çizilenler dönüşür."""
    u = ease(cx.u)
    s = lerp(z0, z1, u)
    f = cx.f
    f.c.save()
    f.c.translate(c[0] + pan[0] * u, c[1] + pan[1] * u)
    f.c.scale(s, s)
    f.c.translate(-c[0], -c[1])
    try:
        yield s
    finally:
        f.c.restore()


def fadeout(cx, d=0.8, color="#000000", delay=0.0):
    """Çekimin son d sn'sinde siyaha (veya renge) çözül."""
    a = smooth((cx.t - (cx.dur - d - delay)) / d)
    if a > 0:
        cx.f.rect(0, 0, W, H, color=color, alpha=a)


def fadein(cx, d=0.6, color="#000000"):
    a = 1 - smooth(cx.t / d)
    if a > 0:
        cx.f.rect(0, 0, W, H, color=color, alpha=a)


# ───────────────────────────── ışık/atmosfer ─────────────────────────────
def glow(f, x, y, r, color="#FFB347", a=0.5, plus=True):
    if a <= 0:
        return
    stops = [(color, 0.0, int(255 * clamp(a))), (color, 0.45, int(255 * clamp(a) * 0.35)), (color, 1.0, 0)]
    f.circle(x, y, r, shader=f.rad(x, y, r, stops), blend=skia.BlendMode.kPlus if plus else None)


def duo_glow(f, left="#1E5560", right="#8E1F26", a=0.30, y=H * 0.5, r=900, lx=W * 0.2, rx=W * 0.8):
    """İki ucu iki renkle yıkayan zemin ışığı (protestan petrol ↔ Habsburg kırmızı)."""
    glow(f, lx, y, r, left, a)
    glow(f, rx, y, r, right, a)


def spot(f, x, y, rx, ry, color="#FFE2A0", a=0.2):
    """Yumuşak elips ışık havuzu (zemin)."""
    f.c.save()
    f.c.translate(x, y)
    f.c.scale(1.0, ry / rx)
    f.c.drawCircle(0, 0, rx, skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kPlus,
                                         Shader=skia.GradientShader.MakeRadial((0, 0), rx, [C(color, int(255 * a)), C(color, int(255 * a * 0.35)), C(color, 0)], [0, 0.5, 1])))
    f.c.restore()


def backdrop(f, cx, kind="night", tint=None, tint_a=0.0, rays=0.3, dust_n=50, dust_a=0.45):
    """Standart koyu zemin + ışın + toz; tint=(sol, sağ) çift ışık."""
    f.bg(kind)
    if rays:
        f.rays(alpha=rays)
    if tint:
        duo_glow(f, tint[0], tint[1], a=tint_a or 0.25)
    if dust_n:
        sk.dust(f, cx.t, n=dust_n, alpha=dust_a)


# ───────────────────────────── parşömen ─────────────────────────────
PAPER_TONE = "#C2A872"


@contextmanager
def paper(f, x, y, w, h, rot=0.0, sc=1.0, alpha=1.0, seed=3, tone=None, shade=0.38):
    """Parşömen levha (koyu sahneye uygun, kamaşmayan ton + mum ışığı düşüşü); yerel koordinatlar levha merkezinde
    (−w/2..w/2, −h/2..h/2). `with paper(...): f.text(...)`"""
    tone = tone or PAPER_TONE
    img, pad = SH.paper_sprite(int(w), int(h), seed=seed, tone=tone)
    f.c.save()
    f.c.translate(x, y)
    if rot:
        f.c.rotate(math.degrees(rot))
    f.c.scale(sc, sc)
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(clamp(alpha))
    f.c.drawImage(img, -w / 2 - pad, -h / 2 - pad, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    if shade > 0 and alpha > 0:
        sh = skia.GradientShader.MakeRadial((-w * 0.10, -h * 0.14), max(w, h) * 0.82,
                                            [C("#2A1608", 0), C("#2A1608", int(255 * shade * alpha * 0.30)), C("#1A0D04", int(255 * shade * alpha))], [0.0, 0.5, 1.0])
        f.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 + 4, -h / 2 + 4, w - 8, h - 8), 14, 14), skia.Paint(AntiAlias=True, Shader=sh))
    try:
        yield
    finally:
        f.c.restore()


INK = "#2A1A0C"


def reveal(f, text, x, y, prog, face="fell", size=40, color=INK, align="l", alpha=1.0, track=0.0, shadow=None):
    """Soldan sağa mürekkep gibi açılan metin."""
    if prog <= 0:
        return 0.0
    wt = sk.text_width(text, face, size, track)
    ox = x - (wt / 2 if align == "c" else wt if align == "r" else 0)
    f.c.save()
    f.c.clipRect(skia.Rect.MakeXYWH(ox - 10, y - size * 1.15, (wt + 20) * clamp(prog), size * 1.7))
    f.text(text, ox, y, face=face, size=size, color=color, align="l", track=track, alpha=alpha, shadow=shadow)
    f.c.restore()
    return wt


def scribbles(f, x, y, w, rows, prog=1.0, seed=1, line_h=30, color=INK, alpha=0.62, thick=5.5, row_dt=None, ragged=0.18, indent=0.0):
    """Okunmaz el yazısı satırları (kâğıt üstünde 'metin' izlenimi). prog 0..1 satır satır belirir."""
    rs = np.random.RandomState(seed)
    nshow = rows * clamp(prog)
    for r in range(rows):
        k = clamp(nshow - r)
        if k <= 0:
            break
        yy = y + r * line_h
        wr = w * (1.0 - ragged * rs.rand()) * (0.55 if (r == rows - 1 and rs.rand() > 0.4) else 1.0)
        xx = x + (indent if r == 0 else 0)
        x_end = x + wr
        cur = xx
        pts = []
        while cur < x_end:
            wl = 14 + rs.rand() * 70
            gap = 8 + rs.rand() * 14
            pts.append((cur, min(x_end, cur + wl)))
            cur += wl + gap
        xs_lim = x + (x_end - x) * k
        for (a, b) in pts:
            if a >= xs_lim:
                break
            b = min(b, xs_lim)
            ph = rs.rand() * 6
            p = skia.Path()
            p.moveTo(a, yy)
            n = max(2, int((b - a) / 9))
            for i in range(1, n + 1):
                px = a + (b - a) * i / n
                p.lineTo(px, yy + math.sin(px * 0.35 + ph) * 2.6 + (rs.rand() - 0.5) * 2.2)
            f.path(p, style="stroke", sw=thick * (0.7 + 0.5 * rs.rand()), color=color, alpha=alpha)


def strike(f, x0, y0, x1, y1, prog, color="#B02A2A", sw=9, alpha=0.95, jitter=2.0, seed=2):
    """Fırça gibi kırmızı çizgi (üstünü çizme)."""
    if prog <= 0:
        return
    k = ease_out(prog, 2)
    xe, ye = lerp(x0, x1, k), lerp(y0, y1, k)
    rs = np.random.RandomState(seed)
    for dy, a_, w_ in ((0, alpha, sw), (sw * 0.45, alpha * 0.55, sw * 0.5)):
        p = skia.Path()
        p.moveTo(x0, y0 + dy)
        n = 8
        for i in range(1, n + 1):
            u = i / n * k
            p.lineTo(lerp(x0, x1, u), lerp(y0, y1, u) + dy + (rs.rand() - 0.5) * jitter * 2)
        f.path(p, style="stroke", sw=w_, color=color, alpha=a_, cap="round")


def curve_arrow(f, p0, p1, bend=-120, prog=1.0, color="#F0D27A", sw=6, head=True, alpha=1.0, dash=None, shadow=True):
    """p0→p1 yay biçimli ok (bend: kontrol noktasının dik sapması)."""
    if prog <= 0:
        return
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1.0
    cxp, cyp = mx - dy / L * bend, my + dx / L * bend
    path = skia.Path()
    path.moveTo(*p0)
    path.quadTo(cxp, cyp, *p1)
    pm = skia.PathMeasure(path, False)
    ln = pm.getLength()
    part = skia.Path()
    pm.getSegment(0, ln * clamp(prog), part, True)
    if shadow:
        f.path(part, style="stroke", sw=sw + 4, color="#000000", alpha=0.45 * alpha)
    pa = f.paint(color, style="stroke", sw=sw, alpha=alpha)
    if dash:
        pa.setPathEffect(skia.DashPathEffect.Make(list(dash), 0))
    f.c.drawPath(part, pa)
    if head and prog > 0.04:
        pos, tan = pm.getPosTan(max(0.0, ln * clamp(prog) - 0.5))
        if pos is not None:
            ang = math.atan2(tan.y(), tan.x())
            ah = sw * 3.6
            tip = (pos.x(), pos.y())
            a1 = (tip[0] - ah * math.cos(ang - 0.45), tip[1] - ah * math.sin(ang - 0.45))
            a2 = (tip[0] - ah * math.cos(ang + 0.45), tip[1] - ah * math.sin(ang + 0.45))
            f.poly([tip, a1, a2], color=color, alpha=alpha)
            f.poly([tip, a1, a2], style="stroke", sw=1.6, color="#2A1A0C", alpha=0.8 * alpha)


# ───────────────────────────── damga / etiket ─────────────────────────────
def stamp2(f, text, x, y, rot=-0.10, size=62, color="#B02A2A", alpha=1.0, t=1.0, seed=5, sub=None, fill_bg=None):
    """Aşınmış kırmızı mühür damgası (çarpma animasyonlu). t: 0..1."""
    if t <= 0:
        return
    sc = 1.0 + (1 - back_out(t)) * 0.9 if t < 1 else 1.0
    a = alpha * min(1.0, t * 3)
    wd = sk.text_width(text, "title", size, 8) + 92
    hh = size * 1.5 + (size * 0.42 if sub else 0)
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(math.degrees(rot))
    f.c.scale(sc, sc)
    f.c.saveLayer(skia.Rect.MakeLTRB(-wd / 2 - 30, -hh, wd / 2 + 30, hh), None)
    if fill_bg:
        f.rrect(-wd / 2, -size * 0.85, wd, hh, 10, color=fill_bg, alpha=0.85 * a)
    f.rrect(-wd / 2, -size * 0.85, wd, hh, 10, style="stroke", sw=6, color=color, alpha=0.92 * a)
    f.rrect(-wd / 2 + 9, -size * 0.85 + 9, wd - 18, hh - 18, 6, style="stroke", sw=2.2, color=color, alpha=0.8 * a)
    f.text(text, 0, size * 0.28, face="title", size=size, color=color, align="c", track=8, alpha=0.95 * a)
    if sub:
        f.text(sub, 0, size * 0.28 + size * 0.62, face="cap_b", size=size * 0.36, color=color, align="c", track=5, alpha=0.9 * a)
    # aşınma: küçük delikler (DstOut)
    rs = np.random.RandomState(seed)
    er = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kDstOut, Color=C("#000000", 255))
    for _ in range(70):
        px, py = rs.uniform(-wd / 2, wd / 2), rs.uniform(-size * 0.85, hh - size * 0.85)
        er.setAlphaf(rs.uniform(0.25, 0.85))
        f.c.drawCircle(px, py, rs.uniform(0.8, 3.2), er)
    for _ in range(5):
        px, py = rs.uniform(-wd / 2, wd / 2), rs.uniform(-size * 0.85, hh - size * 0.85)
        er.setAlphaf(0.7)
        f.c.drawRect(skia.Rect.MakeXYWH(px, py, rs.uniform(10, 40), rs.uniform(1.2, 2.4)), er)
    f.c.restore()   # layer
    f.c.restore()


def tag(f, text, x, y, size=26, color="#E8D49A", edge="#C9962B", alpha=1.0, align="c", track=5, face="cap_b", pad=22, bg="#150D08", icon=None, icon_metal="gold"):
    """Küçük koyu etiket (anlatıya eşlik eden ince not: YAZILIR, ANLATILIR…)."""
    if alpha <= 0:
        return 0, 0
    wt = sk.text_width(text, face, size, track)
    iw = size * 1.5 if icon else 0
    w = wt + pad * 2 + iw
    h = size * 1.75
    x0 = x - (w / 2 if align == "c" else w if align == "r" else 0)
    f.rrect(x0 + 3, y - h * 0.68 + 5, w, h, 10, color="#000000", alpha=0.35 * alpha, blur=6)
    f.rrect(x0, y - h * 0.68, w, h, 10, color=bg, alpha=0.88 * alpha)
    f.rrect(x0, y - h * 0.68, w, h, 10, style="stroke", sw=2, color=edge, alpha=0.9 * alpha)
    if icon:
        icons.draw_icon(f, icon, x0 + pad + size * 0.55, y - size * 0.18, size=size * 1.25, metal=icon_metal, alpha=alpha, shadow=False)
    f.text(text, x0 + pad + iw, y, face=face, size=size, color=color, align="l", track=track, alpha=alpha)
    return w, h


def plate_text(f, text, x, y, size=34, alpha=1.0, color="#F3DE9A", sub=None, w=None, track=6):
    """İsim levhası (tek satır + isteğe bağlı alt satır) — özel çekimlerde."""
    wn = sk.text_width(text, "title_m", size, track)
    ww = max(wn + 90, 300) if w is None else w
    hh = size * 2.0 + (size * 0.9 if sub else 0)
    SH.plate(f, x - ww / 2, y - size * 1.25, ww, hh, alpha=alpha)
    f.text(text, x, y + size * 0.1, face="title_m", size=size, color=color, align="c", track=track, alpha=alpha, shadow=(2, 3, 3, "#000000"))
    if sub:
        f.text(sub, x, y + size * 0.1 + size * 0.95, face="cap_i", size=size * 0.78, color="#D9C795", align="c", alpha=alpha)


def big_gold(f, text, x, y, size=120, alpha=1.0, track=8, face="title", glow_a=0.0, scale=1.0):
    """Hızlı (önbelleksiz sayı için) altın yazı."""
    if glow_a > 0:
        f.text(text, x, y, face=face, size=size, color="#FFD27A", align="c", track=track, alpha=glow_a * alpha, shadow=(0, 0, 18, "#FFB347"))
    return SH.gold_flat(f, text, x, y, face=face, size=size, track=track, alpha=alpha)


# ───────────────────────────── küçük çizim ilkelleri ─────────────────────────────
def lens_flare(f, x, y, r=160, a=0.5):
    glow(f, x, y, r, "#FFE2A0", a)
    f.line(x - r * 1.4, y, x + r * 1.4, y, color="#FFE8B0", sw=2, alpha=0.35 * a, blur=2)


def flame(f, x, y, s=1.0, t=0.0, seed=0, a=1.0):
    """Küçük mum/meşale alevi (dinamik)."""
    fl = 0.85 + 0.15 * math.sin(t * 9 + seed * 1.7) + 0.05 * math.sin(t * 17 + seed)
    glow(f, x, y - 14 * s, 70 * s * fl, "#FFB347", 0.55 * a)
    f.oval(x, y - 10 * s, 6.5 * s * fl, 15 * s * fl, color="#FF9B3A", alpha=0.95 * a)
    f.oval(x, y - 6 * s, 3.4 * s * fl, 9 * s * fl, color="#FFF1C2", alpha=a)


def shadow_ellipse(f, x, y, rx, ry, a=0.5):
    f.oval(x, y, rx, ry, color="#000000", alpha=a, blur=ry * 0.5)


def book_box(f, x, y, w, h, d, color="#4A2A18", band="#C9962B", alpha=1.0, pages="#E9DDBB", rot=0.0, label=None, face_bright=1.0):
    """Yatay yatan kitap (ön yüzü=sırt, üstü=sayfalar). (x,y) = ön yüzün sol-alt köşesi. Hafif perspektif: d = derinlik."""
    f.c.save()
    f.c.translate(x, y)
    if rot:
        f.c.rotate(math.degrees(rot))
    sk_x, sk_y = d * 0.55, -d * 0.30       # derinlik yönü
    # üst yüz (sayfa bloğu)
    top = sk.poly_path([(0, -h), (w, -h), (w + sk_x, -h + sk_y), (sk_x, -h + sk_y)], True)
    f.path(top, shader=f.lin(0, -h + sk_y, 0, -h, [(mix(pages, "#FFFFFF", 0.25), 0.0), (mix(pages, "#7A5E30", 0.35), 1.0)]), alpha=alpha)
    for i in range(1, 5):
        u = i / 5
        f.line(sk_x * u, -h + sk_y * u, w + sk_x * u, -h + sk_y * u, color="#7A5E30", sw=1, alpha=0.30 * alpha)
    # sağ yan yüz
    side = sk.poly_path([(w, -h), (w + sk_x, -h + sk_y), (w + sk_x, sk_y), (w, 0)], True)
    f.path(side, shader=f.lin(w, 0, w + sk_x, 0, [(mix(color, "#000000", 0.25), 0.0), (mix(color, "#000000", 0.55), 1.0)]), alpha=alpha)
    # ön yüz (sırt)
    f.rect(0, -h, w, h, shader=f.lin(0, -h, 0, 0, [(mix(color, "#FFFFFF", 0.14 * face_bright), 0.0), (color, 0.5), (mix(color, "#000000", 0.4), 1.0)]), alpha=alpha)
    f.rect(0, -h, w, h, style="stroke", sw=2, color=mix(color, "#000000", 0.6), alpha=0.8 * alpha)
    for bx in (w * 0.16, w * 0.80):
        f.rect(bx, -h, w * 0.045, h, color=band, alpha=0.9 * alpha)
    f.rect(w * 0.28, -h * 0.74, w * 0.44, h * 0.48, style="stroke", sw=1.8, color=band, alpha=0.85 * alpha)
    f.c.restore()


def ellipse_pts(cx, cy, rx, ry, n, a0=-90.0, span=360.0, closed=True):
    out = []
    for i in range(n):
        a = math.radians(a0 + span * i / (n if closed else max(1, n - 1)))
        out.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    return out


# ───────────────────────────── kum saati (vektör, animasyonlu kum) ─────────────────────────────
def _hg_pt(px, py, s):
    return ((px - 256) * s, (py - 256) * s)


def draw_hourglass(f, x, y, h=360.0, fill_bottom=0.0, rot=0.0, alpha=1.0, glass_a=0.30, sand="#E3B54A"):
    """Kum saati: h = plakadan plakaya yükseklik. fill_bottom: nesne çerçevesinde alt hazne doluluğu (0..1); akış görünür.
    rot: radyan (çevirme animasyonu için)."""
    s = h / 360.0
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(math.degrees(rot))
    P = lambda a, b: _hg_pt(a, b, s)  # noqa: E731
    # cam gövde yolları (simgenin geometrisi)
    top_b = [P(140, 104), P(372, 104), P(290, 256), P(222, 256)]
    bot_b = [P(222, 256), P(290, 256), P(372, 408), P(140, 408)]
    full = sk.smooth_path([P(140, 104), P(372, 104), P(290, 256), P(372, 408), P(140, 408), P(222, 256)], True, 0.1)
    # cam dolgu (yarı saydam)
    f.path(full, shader=f.lin(-60 * s, 0, 60 * s, 0, [("#BFD6D0", 0.0, int(70 * glass_a * alpha * 3)), ("#FFFFFF", 0.4, int(40 * glass_a * alpha * 3)), ("#9FB8B2", 1.0, int(70 * glass_a * alpha * 3))]))
    # kum
    f.c.save()
    f.c.clipPath(full, skia.ClipOp.kIntersect, True)
    top_amt = 1.0 - fill_bottom
    ytop_level = P(0, 104)[1] + (1 - top_amt) * (P(0, 250)[1] - P(0, 104)[1]) * 1.0
    f.rect(-200 * s, ytop_level, 400 * s, (P(0, 256)[1] - ytop_level) + 2, color=sand, alpha=0.95 * alpha)
    ybot_level = P(0, 408)[1] - fill_bottom * (P(0, 408)[1] - P(0, 300)[1]) * 1.05
    # alt kum tepecik biçimi
    mound = skia.Path()
    mound.moveTo(*P(130, 410))
    mound.lineTo(*P(130, 410 - (408 - 300) * fill_bottom + 22 * min(1, fill_bottom * 3)))
    mound.lineTo(*P(256, 410 - (408 - 300) * fill_bottom - 18 * min(1, fill_bottom * 4)))
    mound.lineTo(*P(382, 410 - (408 - 300) * fill_bottom + 22 * min(1, fill_bottom * 3)))
    mound.lineTo(*P(382, 410))
    mound.close()
    if fill_bottom > 0.01:
        f.path(mound, color=sand, alpha=0.95 * alpha)
    if 0.02 < fill_bottom < 0.97:
        f.line(0, P(0, 256)[1], 0, ybot_level - 14 * s, color=sand, sw=max(2.0, 5 * s), alpha=0.9 * alpha)
    f.c.restore()
    f.path(full, style="stroke", sw=max(2.0, 4 * s), color="#F6E9C0", alpha=0.55 * alpha)
    # yansıma
    f.line(P(160, 130)[0], P(160, 130)[1], P(206, 232)[0], P(206, 232)[1], color="#FFFFFF", sw=max(2.0, 5 * s), alpha=0.35 * alpha)
    # plakalar ve direkler (altın)
    for yy in (76, 408):
        px0, py0 = P(120, yy)
        w_, h_ = 272 * s, 28 * s
        f.rrect(px0, py0, w_, h_, 8 * s, shader=f.lin(px0, py0, px0, py0 + h_, [("#F4DC8C", 0.0), ("#C9962B", 0.5), ("#6B4A12", 1.0)]), alpha=alpha)
        f.rrect(px0, py0, w_, h_, 8 * s, style="stroke", sw=2, color="#3A2610", alpha=0.7 * alpha)
    for sx in (-1, 1):
        px = sx * 120 * s
        f.rect(px - 7 * s, P(0, 104)[1], 14 * s, P(0, 408)[1] - P(0, 104)[1], shader=f.lin(px - 7 * s, 0, px + 7 * s, 0, [("#6B4A12", 0.0), ("#F4DC8C", 0.45), ("#7A5518", 1.0)]), alpha=alpha)
    f.c.restore()


def chain_links(f, p0, p1, bend=0.0, prog=1.0, color="#B58AD8", link=26, alpha=1.0, sw=5.0):
    """p0→p1 arası eğri boyunca zincir halkaları (dönüşümlü dik/yatay oval)."""
    if prog <= 0:
        return
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1.0
    path = skia.Path()
    path.moveTo(*p0)
    path.quadTo(mx - dy / L * bend, my + dx / L * bend, *p1)
    pm = skia.PathMeasure(path, False)
    ln = pm.getLength()
    n = max(2, int(ln / (link * 0.78)))
    for i in range(int(n * clamp(prog)) + 1):
        d = ln * i / n
        pos, tan = pm.getPosTan(min(d, ln))
        if pos is None:
            continue
        ang = math.degrees(math.atan2(tan.y(), tan.x()))
        f.c.save()
        f.c.translate(pos.x(), pos.y())
        f.c.rotate(ang)
        rw, rh = (link * 0.62, link * 0.36) if i % 2 == 0 else (link * 0.40, link * 0.22)
        f.oval(0, 0, rw, rh, style="stroke", sw=sw * (1.0 if i % 2 == 0 else 0.75), color="#000000", alpha=0.45 * alpha)
        f.oval(0, 0, rw, rh, style="stroke", sw=sw * 0.8, color=color, alpha=alpha)
        f.c.restore()


# ───────────────────────────── güvenli diorama sarmalayıcı ─────────────────────────────
@SH.kind("bw_theatre")
def k_bw_theatre(cx, **kw):
    """`theatre` çekimini çağırır; sahne kodu hata verirse (lab dosyaları yarım/bozuksa) tüm render çökmesin diye yer tutucu çizer ve uyarı basar."""
    f = cx.f
    n = f.c.getSaveCount()
    try:
        SH.KINDS["theatre"](cx, **kw)
    except Exception as e:  # noqa: BLE001
        import sys
        f.c.restoreToCount(n)
        print(f"[bw_theatre] '{kw.get('scene')}' sahnesi hata verdi: {type(e).__name__}: {e}", file=sys.stderr)
        f.rect(0, 0, W, H, shader=f.lin(0, 0, 0, H, [("#241509", 0.0), ("#0D0704", 1.0)]))
        f.text(f"[sahne: {kw.get('scene')} — hata]", W / 2, H / 2, face="cap_i", size=44, color="#8A7A55", align="c")
        f.vig(0.6)


# ───────────────────────────── hızlı madalya çizimi (önbellekli sprite + gölge) ─────────────────────────────
from functools import lru_cache  # noqa: E402

import medal as _medal  # noqa: E402


@lru_cache(maxsize=96)
def _mimg(key, metal, flip, inscr):
    return _medal.medal_image(key, metal, _medal.INSCR.get(key) if inscr else None, flip, size=720)


@lru_cache(maxsize=96)
def _mshadow(key, metal, flip, inscr):
    img = _mimg(key, metal, flip, inscr)
    pad = 60
    s = skia.Surface(720 + 2 * pad, 720 + 2 * pad)
    c = s.getCanvas()
    c.clear(skia.ColorTRANSPARENT)
    p = skia.Paint(AntiAlias=True)
    p.setImageFilter(skia.ImageFilters.Blur(18, 18))
    p.setColorFilter(skia.ColorFilters.Matrix([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.6, 0]))
    c.drawImage(img, pad, pad, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    return s.makeImageSnapshot(), pad


def draw_medal2(f, key, x, y, size, metal="gold", flip=False, alpha=1.0, tilt=0.0, glint=None, inscription=True, shadow=True):
    """SH.draw_medal ile aynı görünüm, ~2-3× hızlı (sprite ve gölge önbellekli)."""
    img = _mimg(key, metal, bool(flip), bool(inscription))
    s = size / 720.0
    cs = math.cos(tilt * 0.55)
    if shadow:
        sh, pad = _mshadow(key, metal, bool(flip), bool(inscription))
        f.c.save()
        f.c.translate(x + size * 0.03, y + size * 0.05)
        f.c.scale(s * cs, s)
        p = skia.Paint(AntiAlias=True)
        p.setAlphaf(clamp(alpha))
        f.c.drawImage(sh, -360 - pad, -360 - pad, skia.SamplingOptions(skia.FilterMode.kLinear), p)
        f.c.restore()
    f.c.save()
    f.c.translate(x, y)
    f.c.scale(s * cs, s)
    if glint is not None:
        f.c.saveLayer(skia.Rect.MakeLTRB(-380, -380, 380, 380), None)
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(clamp(alpha))
    f.c.drawImage(img, -360, -360, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    if glint is not None:
        gx = lerp(-520, 520, glint)
        shd = skia.GradientShader.MakeLinear([(gx - 110, -300), (gx + 110, 300)], [C("#FFFFFF", 0), C("#FFF4D0", int(170 * alpha)), C("#FFFFFF", 0)], [0, 0.5, 1])
        f.c.drawRect(skia.Rect.MakeLTRB(-380, -380, 380, 380), skia.Paint(Shader=shd, BlendMode=skia.BlendMode.kSrcATop))
        f.c.restore()
    f.c.restore()
