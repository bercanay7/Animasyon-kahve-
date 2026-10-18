"""cilt_orn — Medici cildi süs kütüphanesi: boyalı bantlar (yuvarlak-palle, baklava, ip, asma), çerçeve, lapis-yıldız alanı, ince çizgi çerçeve.

Hepsi vektör (Skia) + hafif elle-çizim sapması (DiscretePathEffect). Pigment: oker, terra verde, sinabar, lapis, kireç beyazı; altın yalnız ince vurgu.
`frame_panel(f, x, y, w, h, ...)` bir dikdörtgenin çevresine bant çerçeve çizer (haritalar, belgeler, başlık levhası).
"""
import functools
import math

import cv2
import numpy as np
import skia

import cilt_medici as CM
import cilt_props as CP
import cilt_wall as CW
import sk
from sk import C, Frame, H, W, clamp, mix

PIG = CM.PIG


def _p(f, color, style="fill", sw=1.0, alpha=1.0, wob=None):
    p = f.paint(color, style=style, sw=sw, alpha=alpha)
    if wob:
        CM.wobble(p, wob[0], wob[1], wob[2] if len(wob) > 2 else 0)
    return p


# ───────────────────────────── bantlar (yatay; dikey için tuvali döndür) ─────────────────────────────
def band_roundels(f, x0, y, x1, h, ground=None, dot=None, rim=None, alpha=1.0, seed=0):
    """Palle sırası: zemin şeridi + yan yana yuvarlaklar (Medici motifi), ince çizgi kenarlı."""
    ground = ground or PIG["OCHRE_L"]
    dot = dot or PIG["CINNABAR"]
    rim = rim or PIG["INK_S"]
    c = f.c
    c.drawRect(skia.Rect.MakeLTRB(x0, y, x1, y + h), _p(f, ground, alpha=alpha))
    n = max(1, int((x1 - x0) / (h * 0.92)))
    step = (x1 - x0) / n
    r = h * 0.36
    for i in range(n):
        cx = x0 + step * (i + 0.5)
        cy = y + h / 2
        f.circle(cx + 1.2, cy + 2, r, color="#000000", alpha=0.18 * alpha, blur=1.6)
        f.circle(cx, cy, r, shader=f.rad(cx - r * 0.35, cy - r * 0.4, r * 1.6, [(mix(dot, "#FFFFFF", 0.38), 0.0), (dot, 0.5), (mix(dot, "#000000", 0.35), 1.0)]), alpha=alpha)
        p = _p(f, rim, "stroke", 1.4, 0.7 * alpha, (6, 0.5, i))
        c.drawCircle(cx, cy, r, p)
    for yy in (y, y + h):
        c.drawLine(x0, yy, x1, yy, _p(f, rim, "stroke", 1.6, 0.8 * alpha, (14, 0.7, 2)))


def band_lozenge(f, x0, y, x1, h, c1=None, c2=None, c3=None, rim=None, alpha=1.0, seed=0):
    """Baklava (harlequin/Cosmati) bandı: üç renkli dönüşümlü elmaslar."""
    c1 = c1 or PIG["CINNABAR"]
    c2 = c2 or PIG["OCHRE_L"]
    c3 = c3 or PIG["TERRA_D"]
    rim = rim or PIG["INK_S"]
    c = f.c
    c.drawRect(skia.Rect.MakeLTRB(x0, y, x1, y + h), _p(f, c2, alpha=alpha))
    w = h * 1.0
    n = int((x1 - x0) / w) + 2
    cols = [c1, c3]
    for i in range(n):
        cx = x0 + (i + 0.5) * w
        if cx - w * 0.5 > x1 or cx + w * 0.5 < x0:
            continue
        pts = [(cx, y + 2), (cx + w * 0.5, y + h / 2), (cx, y + h - 2), (cx - w * 0.5, y + h / 2)]
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(x0, y, x1, y + h))
        f.poly(pts, color=cols[i % 2], alpha=alpha)
        f.poly(pts, style="stroke", sw=1.3, color=rim, alpha=0.65 * alpha)
        f.circle(cx, y + h / 2, h * 0.07, color=PIG["LIME"], alpha=0.9 * alpha)
        c.restore()
    for yy in (y, y + h):
        c.drawLine(x0, yy, x1, yy, _p(f, rim, "stroke", 1.6, 0.8 * alpha, (14, 0.7, 4)))


def band_rope(f, x0, y, x1, h, c1=None, c2=None, ground=None, rim=None, alpha=1.0):
    """Çift iplik (guilloche): iki sinüs şerit, kesişimlerde dönüşümlü üst/alt."""
    c1 = c1 or PIG["LAPIS"]
    c2 = c2 or PIG["CINNABAR"]
    ground = ground or PIG["LIME"]
    rim = rim or PIG["INK_S"]
    c = f.c
    c.drawRect(skia.Rect.MakeLTRB(x0, y, x1, y + h), _p(f, ground, alpha=alpha))
    amp = h * 0.30
    per = h * 1.9
    sw = h * 0.20
    cy = y + h / 2

    def curve(ph, xa, xb):
        p = skia.Path()
        first = True
        x = xa
        while x <= xb + 2:
            yy = cy + math.sin((x - x0) / per * 2 * math.pi + ph) * amp
            if first:
                p.moveTo(x, yy); first = False
            else:
                p.lineTo(x, yy)
            x += 3
        return p
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(x0, y, x1, y + h))
    for col, ph in ((c1, 0.0), (c2, math.pi)):
        path = curve(ph, x0, x1)
        c.drawPath(path, _p(f, rim, "stroke", sw + 3.0, 0.8 * alpha))
        c.drawPath(path, _p(f, col, "stroke", sw, alpha))
    # üstte kalacak kesişim parçaları: A her ikinci kesişimde B'nin üstüne
    k = 0
    xcross = x0 + per / 2 * 0.0
    n = int((x1 - x0) / (per / 2)) + 2
    for i in range(n):
        xc = x0 + (i * 0.5) * per + per * 0.5 * 0.0
        xc = x0 + i * per / 2
        if i % 2 == 0:
            ph, col = 0.0, c1
        else:
            ph, col = math.pi, c2
        seg = curve(ph, xc - per * 0.09, xc + per * 0.09)
        c.drawPath(seg, _p(f, rim, "stroke", sw + 3.0, 0.8 * alpha))
        c.drawPath(seg, _p(f, col, "stroke", sw, alpha))
    c.restore()
    for yy in (y, y + h):
        c.drawLine(x0, yy, x1, yy, _p(f, rim, "stroke", 1.6, 0.8 * alpha, (14, 0.7, 6)))


def band_vine(f, x0, y, x1, h, ground=None, stem=None, leaf=None, berry=None, rim=None, alpha=1.0, seed=3):
    """Asma/akantus dalı: dalgalı gövde + sırayla yukarı/aşağı yapraklar + sinabar meyve (grottesche hissi)."""
    ground = ground or PIG["LIME"]
    stem = stem or PIG["TERRA_D"]
    leaf = leaf or PIG["TERRA"]
    berry = berry or PIG["CINNABAR"]
    rim = rim or PIG["INK_S"]
    c = f.c
    c.drawRect(skia.Rect.MakeLTRB(x0, y, x1, y + h), _p(f, ground, alpha=alpha))
    amp = h * 0.20
    per = h * 2.4
    cy = y + h / 2
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(x0, y, x1, y + h))
    p = skia.Path()
    x = x0 - 4
    p.moveTo(x, cy)
    while x <= x1 + 4:
        p.lineTo(x, cy + math.sin((x - x0) / per * 2 * math.pi) * amp)
        x += 3
    c.drawPath(p, _p(f, stem, "stroke", h * 0.07, alpha))
    n = int((x1 - x0) / (per / 2)) + 2
    for i in range(n):
        xc = x0 + i * per / 2 + per / 4
        yc = cy + math.sin((xc - x0) / per * 2 * math.pi) * amp
        up = -1 if i % 2 == 0 else 1
        lw, lh = h * 0.36, h * 0.17
        c.save(); c.translate(xc, yc); c.rotate(up * -38)
        lp = sk.smooth_path([(0, 0), (lw * 0.4, -lh * up), (lw, 0), (lw * 0.4, lh * up)], True, 0.6)
        c.drawPath(lp, _p(f, leaf, alpha=alpha))
        c.drawPath(lp, _p(f, rim, "stroke", 1.2, 0.7 * alpha))
        c.drawLine(0, 0, lw * 0.85, 0, _p(f, rim, "stroke", 1.0, 0.55 * alpha))
        c.restore()
        if i % 2 == 1:
            f.circle(xc + h * 0.07, yc + up * h * 0.20, h * 0.065, color=berry, alpha=alpha)
            f.circle(xc + h * 0.07, yc + up * h * 0.20, h * 0.065, color=rim, style="stroke", sw=1.0, alpha=0.6 * alpha)
    c.restore()
    for yy in (y, y + h):
        c.drawLine(x0, yy, x1, yy, _p(f, rim, "stroke", 1.6, 0.8 * alpha, (14, 0.7, 8)))


BANDS = dict(roundels=band_roundels, lozenge=band_lozenge, rope=band_rope, vine=band_vine)


def frame_panel(f, x, y, w, h, band=34, kind="lozenge", alpha=1.0, gold=True, inner_line=True, **kw):
    """Dikdörtgenin DIŞINA bant çerçeve (köşelerde rozetli). (x,y,w,h) iç alanın dikdörtgeni."""
    fn = BANDS[kind]
    c = f.c
    b = band
    # dört bant: üst/alt yatay, sol/sağ dikey (tuval döndürülerek)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(x - b, y - b, x + w + b, y + h + b))
    fn(f, x, y - b, x + w, b, alpha=alpha, **kw)
    fn(f, x, y + h, x + w, b, alpha=alpha, **kw)
    for side in (-1, 1):
        c.save()
        cxp = x - b / 2 if side < 0 else x + w + b / 2
        c.translate(cxp, y + h / 2)
        c.rotate(90 if side > 0 else -90)
        fn(f, -h / 2, -b / 2, h / 2, b, alpha=alpha, **kw)
        c.restore()
    c.restore()
    # köşe rozetleri
    for (cx_, cy_) in ((x - b / 2, y - b / 2), (x + w + b / 2, y - b / 2), (x - b / 2, y + h + b / 2), (x + w + b / 2, y + h + b / 2)):
        f.circle(cx_, cy_, b * 0.62, color=PIG["LIME"], alpha=alpha)
        f.circle(cx_, cy_, b * 0.62, style="stroke", sw=1.6, color=PIG["INK_S"], alpha=0.8 * alpha)
        f.circle(cx_, cy_, b * 0.34, color=PIG["CINNABAR"], alpha=alpha)
        f.circle(cx_, cy_, b * 0.34, style="stroke", sw=1.2, color=PIG["INK_S"], alpha=0.7 * alpha)
    if gold:
        gc = CM.TH.gold
        for k, dd in ((0, 0), (1, b + 6)):
            p = f.paint(gc, style="stroke", sw=2.4 if k == 0 else 1.4, alpha=0.95 * alpha)
            CM.wobble(p, 18.0, 0.8, 9 + k)
            c.drawRect(skia.Rect.MakeLTRB(x - dd - (3 if k == 0 else 0), y - dd - (3 if k == 0 else 0), x + w + dd + (3 if k == 0 else 0), y + h + dd + (3 if k == 0 else 0)), p)
    if inner_line:
        p = f.paint(PIG["INK_S"], style="stroke", sw=1.4, alpha=0.7 * alpha)
        CM.wobble(p, 16.0, 0.8, 12)
        c.drawRect(skia.Rect.MakeLTRB(x, y, x + w, y + h), p)


def hairline_frame(f, x, y, w, h, alpha=1.0, color=None, gap=10, corner_dots=True):
    """İnce çift çizgi çerçeve (elle çizim sapmalı) — madalya/alıntı/belge kenarları için."""
    color = color or CM.TH.rule
    c = f.c
    for k, (ins, sw, aa) in enumerate(((0, 2.4, 0.9), (gap, 1.1, 0.7))):
        p = f.paint(color, style="stroke", sw=sw, alpha=aa * alpha)
        CM.wobble(p, 16.0, 0.9, 20 + k)
        c.drawRect(skia.Rect.MakeLTRB(x + ins, y + ins, x + w - ins, y + h - ins), p)
    if corner_dots:
        for (cx_, cy_) in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
            CM.diamond(f, cx_, cy_, 7, color, alpha)


# ───────────────────────────── yıldız ve lapis alan ─────────────────────────────
@functools.lru_cache(maxsize=4)
def star_sprite(n=8, size=128):
    m = CP.Mask(size)
    cx = cy = size / 2
    pts = []
    for i in range(n * 2):
        r = size * (0.46 if i % 2 == 0 else 0.20)
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    m.fill(sk.poly_path(pts))
    m.circle(cx, cy, size * 0.09, 0)
    mask = m.arr()
    mask = cv2.GaussianBlur(mask, (0, 0), 0.6)
    arr = sk.relief_sprite(mask, "leaf", bevel=2.6, strength=1.1, spec=0.9, tex=CM._crinkle((size, size), 3, 0.6))
    return sk.np_to_image(arr)


@functools.lru_cache(maxsize=6)
def lapis_field(w, h, seed=1, stars=True, loss=0.35, tone="lapis"):
    """Lapis lazuli fresk alanı (RGBA skia.Image): fırça izli pigment, kenarda birikmiş koyu, kırılgan çatlak ağı, kenar kayıpları
    (sıva görünür), altın 8 köşeli yıldızlar. tone: 'lapis' | 'oxblood' (Perde III)."""
    rs = np.random.RandomState(seed)
    base = {"lapis": (26, 44, 120), "oxblood": (96, 22, 24), "terra": (70, 90, 60)}[tone]
    # fırça izleri: yatay uzamış gürültü
    st = rs.standard_normal((h // 2 + 2, w // 2 + 2)).astype(np.float32)
    st = cv2.GaussianBlur(st, (0, 0), sigmaX=40, sigmaY=2.2)
    st = cv2.resize(st / (st.std() + 1e-6), (w, h))
    mf = CW.lf(rs, h, w, 90)
    hf = CW.lf(rs, h, w, 20)
    gr = CW.gn(rs, h, w, 1.0)
    dens = 1 + 0.07 * st + 0.09 * mf + 0.035 * hf + 0.02 * gr
    # kenarlarda pigment birikimi (koyu) + merkezde hafif açık
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ed = np.minimum(np.minimum(xx, w - 1 - xx) / (w * 0.5), np.minimum(yy, h - 1 - yy) / (h * 0.5))
    dens *= 0.80 + 0.30 * np.clip(ed * 2.2, 0, 1) ** 0.6
    col = np.empty((h, w, 3), np.float32)
    col[:] = base
    col *= dens[..., None]
    # çatlak ağı (açık çizgiler: sıva çatlaktan görünür)
    cr = CW.micro_craquelure(rs, h, w, ncell=420, warp=7.0)
    cr2 = CW.long_cracks(rs, h, w, n=6)
    cm = np.clip(cr * 0.5 + cr2, 0, 1)
    plast = np.array([196, 186, 160], np.float32)
    col = col * (1 - cm[..., None] * 0.55) + plast * cm[..., None] * 0.55
    # kayıp (lacuna): kenara yakın gürültü eşiği → alfa düşer, sıva rengi görünür
    ln = CW.lf(rs, h, w, 26) * 0.7 + CW.lf(rs, h, w, 7) * 0.5
    edge_w = np.clip(1.0 - ed * 3.0, 0, 1)
    cen = np.exp(-(((xx - w / 2) / (w * 0.30)) ** 2 + ((yy - h / 2) / (h * 0.36)) ** 2))
    lossm = CW.sstep(1.50 - 0.20 * loss, 1.90 - 0.20 * loss, ln + edge_w * 1.0 - cen * 0.75)
    alpha = np.clip(1.0 - lossm, 0, 1)
    # kayıp kenarında açık çizgi
    edge = np.clip(cv2.GaussianBlur(lossm, (0, 0), 1.6) - lossm * 0.7, 0, 1)
    col = col * (1 - edge[..., None] * 0.5) + plast * edge[..., None] * 0.5
    arr = np.dstack([np.clip(col, 0, 255), alpha * 255]).astype(np.uint8)
    fr = Frame(w, h)
    fr.clear(skia.ColorTRANSPARENT)
    fr.c.drawImage(sk.np_to_image(arr), 0, 0)
    if stars:
        star = star_sprite(8, 128)
        for i in range(34):
            sx, sy = rs.uniform(0.04, 0.96) * w, rs.uniform(0.05, 0.95) * h
            sz = rs.choice([30, 36, 44, 56]) * (w / 1500.0) ** 0.5
            fr.c.save(); fr.c.translate(sx, sy); fr.c.rotate(rs.uniform(0, 45)); fr.c.scale(sz / 128, sz / 128)
            fr.c.drawImage(star, -64, -64, CM._LIN)
            fr.c.restore()
    return fr.surf.makeImageSnapshot()


# ───────────────────────────── duvar giydirmesi: korniş + sövme (zoccolo) ─────────────────────────────
@functools.lru_cache(maxsize=6)
def plinth_image(perde=2, w=W + 260, h=124):
    """Sövme (alt şerit): sahte mermer; Perde I umber-bej damarlı, II terra verde, III porfir kırmızısı. Üst kenarda kabartma silme."""
    rs = np.random.RandomState(8 + perde)
    base = {1: (96, 80, 62), 2: (78, 96, 66), 3: (112, 44, 40)}[perde]
    mf = CW.lf(rs, h, w, 70) * 0.10 + CW.lf(rs, h, w, 24) * 0.05
    col = np.empty((h, w, 3), np.float32)
    col[:] = base
    col *= (1 + mf)[..., None]
    veins = np.zeros((h, w), np.uint8)
    for i in range(16):
        x = rs.uniform(0, w)
        y = rs.uniform(10, h)
        pts = []
        ang = rs.uniform(-0.5, 0.5)
        for k in range(22):
            ang += rs.normal(0, 0.18)
            x += math.cos(ang) * 22
            y += math.sin(ang) * 9
            pts.append((int(x), int(y)))
        cv2.polylines(veins, [np.array(pts, np.int32).reshape(-1, 1, 2)], False, int(rs.uniform(120, 255)), 1 if rs.rand() < 0.7 else 2, cv2.LINE_AA)
    veins = cv2.GaussianBlur(veins.astype(np.float32) / 255.0, (0, 0), 0.9)
    vcol = np.array({1: (205, 192, 160), 2: (206, 214, 188), 3: (232, 190, 170)}[perde], np.float32)
    col = col * (1 - veins[..., None] * 0.45) + vcol * veins[..., None] * 0.45
    # silme (üstte): açık çizgi + alt gölge
    col[0:7] = col[0:7] * 0.3 + np.array([226, 214, 184], np.float32) * 0.7
    col[7:9] *= 0.55
    shade = np.linspace(1.0, 0.82, h)[:, None, None]
    col *= shade
    a = np.full((h, w), 255, np.uint8)
    return sk.np_to_image(np.dstack([np.clip(col, 0, 255), a]).astype(np.uint8))


@functools.lru_cache(maxsize=4)
def cornice_image(day=True, w=W + 260, h=76):
    """Korniş şeridi (üst): ocre zemin + palle yuvarlakları + altın filet + alt gölge (önbellekli)."""
    fr = Frame(w, h)
    fr.clear(skia.ColorTRANSPARENT)
    base = mix(PIG["PLASTER_D"], PIG["OCHRE"], 0.45) if day else mix(PIG["PLASTER_D"], PIG["OCHRE_D"], 0.5)
    fr.c.translate(130, 0)
    fr.rect(-130, 0, w, 46, shader=fr.lin(0, 0, 0, 46, [(mix(base, "#FFFFFF", 0.18), 0.0), (base, 1.0)]))
    band_roundels(fr, -130, 2, w, 38, ground=mix(base, "#FFFFFF", 0.10), dot=PIG["CINNABAR"], alpha=0.95)
    fr.c.drawLine(-130, 46, w, 46, fr.paint(CM.TH.gold, style="stroke", sw=2.4, alpha=0.9))
    fr.rect(-130, 47, w, 16, shader=fr.lin(0, 47, 0, 63, [("#2A1C0E", 0.0, 80), ("#2A1C0E", 1.0, 0)]))
    return fr.surf.makeImageSnapshot()


def dress(f, cam, top=True, bottom=True, alpha=1.0, perde=None):
    """Duvar giydirmesi (duvarla birlikte paralaks): üstte palle'li korniş şeridi, altta mermer sövme. relight() ile aynı ışığı alır."""
    perde = perde or CM.TH.perde
    c = f.c
    c.save()
    CM.cam_xf(c, cam.ws * 1.015, cam.wdx, cam.wdy)
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(alpha)
    if top:
        c.drawImage(cornice_image(CM.TH.day), -130, -20, CM._LIN, p)
    if bottom:
        c.drawImage(plinth_image(perde), -130, H - 100, CM._LIN, p)
        f.rect(-130, H - 112, W + 260, 12, shader=f.lin(0, H - 112, 0, H - 100, [("#2A1C0E", 0.0, 0), ("#2A1C0E", 1.0, 70)]))
    c.restore()
