"""Sahne ailesi: DENİZ (`sea`) — fırtına / sakin / şafak / alacakaranlık / gece; karaka, kadırga, balıkçı; kıyı köyü/liman.
Kayıt: @SL.sc("sea"). Ayrıntılı API: SAHNE_KATALOGU_deniz_savas.md

Katman düzeni (arkadan öne): gökyüzü(d.04) · uzak su/ufuk(.14) · bant0(.34) · bant1(.50) · [kıyı(.60)] · bant2(.68) · bant3(.90) · bant4(1.14)
Gemi sıraları: row3 = ufukta (gövde batık), row2 = bant0 ile bant1 arası, row1 = bant1–bant2, row0 = bant2–bant3 (en yakın).
"""
import math
from functools import lru_cache

import numpy as np
import skia

import props_war as PW
import scenes_lib as SL
import sk
import stage as ST
import stage_war as SW
from props_war import LIN, LINMIP, PLUS, RS, darken, lighten
from sk import C, H, W, clamp, lerp, mix, smooth
from stage import MARGIN

HZ = 500
BAND_Y = (566, 646, 752, 884, 1024)
BAND_D = (0.34, 0.50, 0.68, 0.90, 1.14)
ROW_Y = {3: HZ + 4, 2: BAND_Y[1] - 8, 1: BAND_Y[2] - 8, 0: BAND_Y[3] - 8}
ROW_S = {3: 0.22, 2: 0.42, 1: 0.68, 0: 1.0}
SKY_D, FAR_D, COAST_D = 0.04, 0.14, 0.60
BASE_D = 0.08

MOODS = dict(
    calm=dict(
        sky=[("#2D4256", 0.0), ("#5F7886", 0.42), ("#B9B39C", 0.78), ("#F0CE92", 1.0)], haze="#E9CC98", sun=(0.70, 376, 40, "#FFF3D2", "#FFC983", 1.0), moon=False,
        cloud_shadow="#52606C", cloud_light="#F8E1B4", cloud_rim="#FFEFC8", cover=0.42, stars=0.0,
        sea_top="#7C939B", sea_bot="#0E2431", crest="#F2DDB0", foam="#EFE6CF", glint="#FFE2A8", glint_amt=0.55, shade="#06141C",
        hull="#150D08", rim="#E9AC66", sail="#CDB78E", sail_l="#F3E0B6", sail_d="#7C6A4E", gold="#B58A2C", lamp=False, lamp_col="#FFC46A", light_dir=1,
        amp=1.0, speed=1.0, wave_spd=14, fog="#E6CC9A", fog_a=0.20, bright=1.0),
    dawn=dict(
        sky=[("#1D3047", 0.0), ("#4E5B7D", 0.30), ("#B0728C", 0.62), ("#F2A46C", 0.88), ("#FFD9A0", 1.0)], haze="#F6BE86", sun=(0.34, 492, 58, "#FFF0C8", "#FFA866", 1.15), moon=False,
        cloud_shadow="#4A4468", cloud_light="#FFC890", cloud_rim="#FFE2B0", cover=0.5, stars=0.0,
        sea_top="#6E5868", sea_bot="#0A121C", crest="#FFD2A0", foam="#FFE9CC", glint="#FFD08A", glint_amt=0.9, shade="#0A121E",
        hull="#120A08", rim="#FFB26A", sail="#D9B496", sail_l="#FFD9A8", sail_d="#7D5A56", gold="#C69A3A", lamp=False, lamp_col="#FFC46A", light_dir=-1,
        amp=0.9, speed=0.9, wave_spd=12, fog="#F2B98C", fog_a=0.28, bright=1.0),
    dusk=dict(
        sky=[("#171B36", 0.0), ("#4B3359", 0.30), ("#A24A55", 0.62), ("#E2733C", 0.86), ("#FFB257", 1.0)], haze="#F39A55", sun=(0.66, 500, 66, "#FFE2A0", "#FF8E3C", 1.3), moon=False,
        cloud_shadow="#3A2542", cloud_light="#FF9A55", cloud_rim="#FFCB78", cover=0.52, stars=0.12,
        sea_top="#62465A", sea_bot="#080E18", crest="#FFB070", foam="#FFD9B0", glint="#FFB65E", glint_amt=1.0, shade="#070E18",
        hull="#0F0807", rim="#FF9A4E", sail="#C79A7E", sail_l="#FFB77A", sail_d="#6A4650", gold="#C28A30", lamp=True, lamp_col="#FFC46A", light_dir=1,
        amp=0.95, speed=1.0, wave_spd=13, fog="#E7894F", fog_a=0.26, bright=0.95),
    night=dict(
        sky=[("#04070E", 0.0), ("#0A1524", 0.40), ("#14283C", 0.78), ("#2A4660", 1.0)], haze="#35536C", sun=None, moon=True,
        cloud_shadow="#0A121C", cloud_light="#5E7894", cloud_rim="#9FB8D0", cover=0.34, stars=1.0,
        sea_top="#27425A", sea_bot="#04090E", crest="#A9C2D8", foam="#C9DCEB", glint="#BFD6EA", glint_amt=0.8, shade="#02060A",
        hull="#07090C", rim="#8FB0CC", sail="#6D7C8E", sail_l="#A5B7C9", sail_d="#2E3946", gold="#7A6A3A", lamp=True, lamp_col="#FFC46A", light_dir=1,
        amp=0.9, speed=0.9, wave_spd=11, fog="#3A566E", fog_a=0.20, bright=0.8),
    storm=dict(
        sky=[("#0B1013", 0.0), ("#1B2429", 0.34), ("#364347", 0.68), ("#68787A", 0.95), ("#8FA096", 1.0)], haze="#6E7E7C", sun=None, moon=False,
        cloud_shadow="#0F1519", cloud_light="#6E8084", cloud_rim="#A9BDBA", cover=0.74, stars=0.0,
        sea_top="#3F5659", sea_bot="#050C0F", crest="#B4C9C6", foam="#E1ECEA", glint="#C9DBD8", glint_amt=0.15, shade="#02080A",
        hull="#07090A", rim="#9BB3B0", sail="#8F917F", sail_l="#C2C2AC", sail_d="#42443C", gold="#6E6030", lamp=False, lamp_col="#FFC46A", light_dir=1,
        amp=1.9, speed=1.7, wave_spd=34, fog="#5F706F", fog_a=0.34, bright=0.9),
)


# ───────────────────────────── kamera yardımcıları (bölüm yazarları için) ─────────────────────────────
def safe_cam(x, y, z, dmax=1.14):
    """Kamerayı, katman kenarlarında boşluk görünmeyecek aralığa sıkıştırır (MARGIN=220)."""
    z = max(1.0, z)
    s = 1 + (z - 1) * dmax
    lx = (1180 - W / 2 / s) / dmax
    ly = (760 - H / 2 / s) / dmax
    return (W / 2 + max(-lx, min(lx, x - W / 2)), H / 2 + max(-ly, min(ly, y - H / 2)), z)


def cam_on(row=0, x=0.5, zoom=1.4, rise=0.0, s=1.0):
    """Verilen sıradaki (row 0..3) geminin (x: 0..1) ekran ortasına gelmesi için kamera (x, y, zoom). rise: 0=gövde orta, 1=direk ucu."""
    d = {0: BAND_D[2], 1: BAND_D[1], 2: BAND_D[0], 3: FAR_D}[int(row)]
    X = x * W
    Yc = ROW_Y[int(row)] - (170 + 220 * rise) * ROW_S[int(row)] * s
    cx = W / 2 + (X - W / 2) / d
    cy = H / 2 + (Yc - H / 2) / d
    return safe_cam(cx, cy, zoom)


@lru_cache(maxsize=40)
def band_image(mood, k):
    """Bant k gövdesi: yalnız içerik yüksekliği kadar kırpılmış görüntü → (img, x, y) katman koordinatında."""
    M = _mood(mood)
    ytop = int(BAND_Y[k] - _amp(M, k) + STRIP_H[k] - 8)
    h = int(H + MARGIN + 70 - ytop)

    def fn(f):
        bake_band(f, M, k)
    img = PW.bake_sprite(fn, W + 2 * MARGIN, h, MARGIN, -ytop, mip=False)
    return img, -MARGIN, ytop


@lru_cache(maxsize=12)
def coast_image(coast, mood, side):
    M = _mood(mood)
    y0, y1 = 240, 870

    def fn(f):
        if coast == "tazones":
            bake_coast_tazones(f, M, mood, side)
        elif coast == "africa":
            bake_coast_africa(f, M, mood, side)
        else:
            bake_coast_harbor(f, M, mood, side)
        f.rect(-MARGIN, 480, W + 2 * MARGIN, 330, shader=f.lin(0, 480, 0, 790, [(M["fog"], 0.0, int(255 * M["fog_a"] * 0.55)), (M["fog"], 1.0, 0)]))
    img = PW.bake_sprite(fn, W + 2 * MARGIN, y1 - y0, MARGIN, -y0, mip=False)
    return img, -MARGIN, y0


def _mood(name):
    return MOODS.get(name, MOODS["calm"])


# ───────────────────────────── gökyüzü ─────────────────────────────
@lru_cache(maxsize=24)
def _cloud_img(mood, seed, which):
    M = _mood(mood)
    w2, h2 = (W + 2 * MARGIN) // 2, (HZ + MARGIN + 60) // 2
    storm = mood == "storm"
    yy = np.linspace(0, 1, h2, dtype=np.float32)
    if which == "high":        # yüksek ince/geniş bulutlar
        vf = np.clip(1.0 - yy * 1.05, 0, 1) ** 0.6
        a = PW.cloud_rgba(w2, h2, seed, cover=0.40 if not storm else 0.62, soft=0.30, scale=60, octaves=5, shadow=M["cloud_shadow"], light=M["cloud_light"], rim=M["cloud_rim"],
                          vfade=vf, stretch=3.0, periodic=True, gamma=1.0, sigma=4.0, reach=10, gain=1.5, light_dir=(0.6 if M["light_dir"] > 0 else -0.6, -0.55))
    elif which == "mid":
        vf = np.clip(np.minimum(yy * 5, (1 - yy) * 3.0), 0, 1)
        a = PW.cloud_rgba(w2, h2, seed + 1, cover=M["cover"], soft=0.36, scale=46, octaves=6, gain=1.35, shadow=M["cloud_shadow"], light=M["cloud_light"], rim=M["cloud_rim"],
                          vfade=vf, stretch=2.1, periodic=True, gamma=1.15, thick_dark=0.55 if storm else 0.25, sigma=5.0, reach=16, light_dir=(0.55 if M["light_dir"] > 0 else -0.55, -0.8))
    else:                      # alçak, ufka yakın bulut şeritleri
        vf = np.clip(np.minimum((yy - 0.45) * 4, (1.0 - yy) * 5), 0, 1)
        a = PW.cloud_rgba(w2, h2, seed + 2, cover=M["cover"] * 0.85 + (0.1 if storm else 0), soft=0.34, scale=30, octaves=5, gain=1.3, shadow=mix(M["cloud_shadow"], M["haze"], 0.25), light=mix(M["cloud_light"], M["haze"], 0.35), rim=None,
                          vfade=vf, stretch=3.4, periodic=True, gamma=1.1, thick_dark=0.2, sigma=2.5, reach=8, light_dir=(0.5 if M["light_dir"] > 0 else -0.5, -0.7))
    if which == "low":
        r0 = int(h2 * 0.44)
        return PW.img_from_rgba(np.ascontiguousarray(a[r0:]), mip=False)
    return PW.img_from_rgba(a, mip=False)


def _draw_cloud(f, img, x, y, alpha=1.0, sc=2.0, plus=0.0):
    p = skia.Paint()
    if alpha < 1:
        p.setAlphaf(alpha)
    f.c.save()
    f.c.translate(x, y)
    f.c.scale(sc, sc)
    f.c.drawImage(img, 0, 0, LIN, p)
    f.c.restore()


def bake_sky(f, M, mood, p):
    f.rect(-MARGIN, -MARGIN, W + 2 * MARGIN, HZ + MARGIN + 80, shader=f.lin(0, -MARGIN, 0, HZ, [(c, u) for c, u in M["sky"]]))
    # yıldızlar
    if M["stars"] > 0:
        rs = RS(11)
        n = int(520 * M["stars"])
        for i in range(n):
            x = rs.rand() * (W + 2 * MARGIN) - MARGIN
            y = (rs.rand() ** 1.7) * (HZ - 20) - MARGIN * 0.6
            r = 0.6 + rs.rand() * 1.5
            a = (0.25 + rs.rand() * 0.75) * (1 - clamp((y + 120) / 650) * 0.8)
            f.circle(x, y, r, color="#DDE8FF", alpha=a)
            if r > 1.7:
                PW.glow_add(f, x, y, 9, "#BFD3FF", 0.4)
    # güneş / ay
    sun = M["sun"]
    if sun:
        sx, sy, sr, core, glow_c, k = sun
        sx = sx * W
        PW.glow_add(f, sx, sy, 760 * k, glow_c, 0.30, 150, 46, 0.30)
        PW.glow_add(f, sx, sy, 300 * k, glow_c, 0.42, 230, 90, 0.38)
        PW.glow_add(f, sx, sy, sr * 2.2, core, 0.55, 255, 150, 0.5)
        f.circle(sx, sy, sr, shader=f.rad(sx, sy, sr, [("#FFFFFF", 0.0), (core, 0.7), (core, 1.0)]))
        ST.god_rays(f, (sx, sy), -math.pi / 2, 2.6, 1500, n=11, alpha=0.06, color=mix(glow_c, "#FFFFFF", 0.3), seed=4, blur=26)
    if M["moon"] or p.get("moon"):
        mx, my, mr = W * 0.30, 170, 54
        PW.glow_add(f, mx, my, 700, "#9FBBD6", 0.38, 140, 40, 0.3)
        PW.glow_add(f, mx, my, 240, "#C7DAEA", 0.55, 220, 80, 0.4)
        f.circle(mx, my, mr, shader=f.rad(mx - 14, my - 16, mr * 1.5, [("#FBFDFF", 0.0), ("#DCE8F2", 0.6), ("#9FB4C8", 1.0)]))
        rs = RS(5)
        for q in range(9):
            a = rs.rand() * 6.283
            d = rs.rand() * mr * 0.7
            f.circle(mx + math.cos(a) * d, my + math.sin(a) * d, 4 + rs.rand() * 9, color="#7F93A8", alpha=0.20 + rs.rand() * 0.15)
    # bulutlar (yüksek + orta)
    seed = 7 if mood != "storm" else 21
    hi = _cloud_img(mood, seed, "high")
    _draw_cloud(f, hi, -MARGIN, -MARGIN, 0.85 if mood != "storm" else 0.7)
    mid = _cloud_img(mood, seed, "mid")
    _draw_cloud(f, mid, -MARGIN, -MARGIN + 30, 0.95)
    # ufuk sisi
    f.rect(-MARGIN, HZ - 140, W + 2 * MARGIN, 160, shader=f.lin(0, HZ - 140, 0, HZ + 20, [(M["haze"], 0.0, 0), (M["haze"], 1.0, int(255 * (0.45 if mood != "storm" else 0.6)))]))
    if mood == "storm":    # bulut yarığı: ufukta soluk ışık
        PW.glow_add(f, W * 0.42, HZ - 30, 620, "#9DB09F", 0.35, 120, 40, 0.3)
    if mood in ("dawn", "dusk") and sun:
        f.rect(-MARGIN, HZ - 26, W + 2 * MARGIN, 30, shader=f.lin(0, HZ - 26, 0, HZ + 4, [(sun[4], 0.0, 0), (sun[3], 1.0, 150)]))


# ───────────────────────────── su bantları ─────────────────────────────
def band_color(M, k):
    u = (0.0, 0.2, 0.46, 0.74, 1.0)[k]
    c = mix(M["sea_top"], M["sea_bot"], u ** 0.62)
    return mix(c, M["haze"], (1 - u) * 0.30 * (0.7 if M["fog_a"] > 0.3 else 1))


def bake_far(f, M, mood, p):
    """Ufuk çizgisi altı: uzak su + güneş/ay yolu + ufuk parlaması."""
    c0 = mix(M["sea_top"], M["haze"], 0.55)
    c1 = band_color(M, 0)
    f.rect(-MARGIN, HZ, W + 2 * MARGIN, 300, shader=f.lin(0, HZ, 0, HZ + 120, [(mix(c0, "#FFFFFF", 0.04), 0.0), (c1, 1.0)]))
    # ufuk çizgisi: ince parlak
    f.rect(-MARGIN, HZ - 2, W + 2 * MARGIN, 3.0, color=mix(M["haze"], "#FFFFFF", 0.25), alpha=0.65)
    # güneş yolu / ay yolu (yansıma): dikey parıltı sütunu
    sun = M["sun"]
    ref_x = None
    if sun:
        ref_x, col = sun[0] * W, sun[4]
    elif M["moon"] or p.get("moon"):
        ref_x, col = W * 0.30, "#BCD3E6"
    if ref_x is not None:
        PW.glow_add(f, ref_x, HZ + 14, 420, col, 0.30 if not M["moon"] else 0.22, 200, 70, 0.3)



def bake_band(f, M, k):
    """Bant k: opak su gövdesi (dalga şeridinin altında); renk bir sonraki bandın tepe rengine doğru kesintisiz akar."""
    y0 = BAND_Y[k] - int(_amp(M, k)) + STRIP_H[k] - 3
    c_top = band_color(M, k)
    if k < 4:
        y1 = BAND_Y[k + 1] - int(_amp(M, k + 1)) + 6
        c_nxt = band_color(M, k + 1)
        f.rect(-MARGIN, y0, W + 2 * MARGIN, H + MARGIN - y0 + 40, shader=f.lin(0, y0, 0, y1, [(c_top, 0.0), (c_nxt, 1.0)]))
        f.rect(-MARGIN, y1, W + 2 * MARGIN, H + MARGIN - y1 + 40, color=c_nxt)
    else:
        f.rect(-MARGIN, y0, W + 2 * MARGIN, H + MARGIN - y0 + 40, shader=f.lin(0, y0, 0, H + 80, [(c_top, 0.0), (mix(c_top, M["sea_bot"], 0.8), 1.0)]))
    # yatay ince parıltı dokusu
    tex = PW.streak_rgba(W + 2 * MARGIN, 160, 30 + k, col=M["crest"], alpha=0.06 + 0.02 * k, scale_x=420 - 40 * k, scale_y=5 + 2 * k, thr=0.66)
    im = PW.img_from_rgba(tex)
    f.c.drawImage(im, -MARGIN, y0 + 4, LIN, skia.Paint())


STRIP_H = (34, 46, 62, 84, 112)
STRIP_AMP = (8, 13, 22, 36, 56)
STRIP_P = (900, 1020, 1160, 1320, 1540)


def _amp(M, k):
    return STRIP_AMP[k] * M["amp"] * (1.0 if M["amp"] < 1.5 else 1.15)


def _strip_set(M, mood, k, which):
    """(ana, ikincil) dalga şeridi görüntüleri."""
    a = _amp(M, k)
    storm = mood == "storm"
    body = band_color(M, k)
    crest = M["crest"]
    foam_amt = (0.9 if storm else 0.12) * (0.35 + 0.17 * k) if mood != "night" else 0.12
    if which == 0:
        return PW.wave_strip(STRIP_P[k], STRIP_H[k], int(a), body, mix(crest, body, 0.74 - 0.13 * k), M["foam"], 100 + k * 7, sharp=2.0 + (0.8 if storm else 0.0), foam_amt=foam_amt,
                             glint=M["glint"], glint_amt=M["glint_amt"] * (0.5 if k < 2 else 0.3), facets=3, shade=M["shade"])
    # ikincil: daha ince, yarı saydam, farklı periyot (kayma/paralaks hissi)
    h2 = int(STRIP_H[k] * 0.78)
    return PW.wave_strip(int(STRIP_P[k] * 0.77) // 2 * 2, h2, int(a * 0.8), body, mix(crest, body, 0.45), M["foam"], 200 + k * 5, sharp=2.4, foam_amt=foam_amt * 1.4,
                         glint=M["glint"], glint_amt=M["glint_amt"] * 0.8, facets=2, shade=M["shade"], comps=((2, 1.0), (4, 0.5), (7, 0.25)))


# ───────────────────────────── kıyılar ─────────────────────────────
def _ridge(x0, x1, pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return lambda x: float(np.interp(x, xs, ys))


def _house(f, x, y, w, h, roof_h, wall, roof, lit, rs, win=True, gable=True):
    """Küçük taş/badanalı ev (ön cephe + beşik çatı)."""
    f.rect(x - w / 2, y - h, w, h, color=wall)
    f.rect(x - w / 2, y - h, w, h, shader=f.lin(x - w / 2, 0, x + w / 2, 0, [("#000000", 0.0, 60), ("#000000", 0.55, 0), ("#000000", 1.0, 90)]))
    if gable:
        f.poly([(x - w / 2 - 4, y - h), (x, y - h - roof_h), (x + w / 2 + 4, y - h)], color=roof)
        f.line(x - w / 2 - 4, y - h, x, y - h - roof_h, color=lighten(roof, 0.25), sw=1.2, alpha=0.5)
    if win:
        nwin = 1 if w < 46 else 2
        for q in range(nwin):
            wx = x + (q - (nwin - 1) / 2) * w * 0.4
            wy = y - h * 0.58
            if lit and rs.rand() > 0.35:
                f.rect(wx - 3.2, wy - 4.5, 6.4, 9, color="#FFC770")
                PW.glow_add(f, wx, wy, 15, "#FFB347", 0.7)
            else:
                f.rect(wx - 3.2, wy - 4.5, 6.4, 9, color="#0A0705", alpha=0.7)


def _tree_clump(f, x, y, r, col, rs):
    pts = []
    n = 9
    for i in range(n):
        a = math.pi * (1 + i / (n - 1))
        pts.append((x + math.cos(a) * r * (0.85 + rs.rand() * 0.3), y + math.sin(a) * r * (0.7 + rs.rand() * 0.45)))
    pts.append((x + r, y + 4))
    pts.append((x - r, y + 4))
    f.path(sk.smooth_path(pts, True, 0.5), color=col)


def bake_coast_tazones(f, M, mood, side):
    """Asturias kıyısı: dik yeşil burun, taş evli balıkçı köyü, kilise, mendirek. side: 'r' | 'l'."""
    sgn = 1 if side == "r" else -1
    xo = lambda x: x if sgn > 0 else W - x
    storm = mood == "storm"
    dark_land = mix("#0E1B14", M["haze"], 0.14 + (0.1 if not storm else 0.04))
    mid_land = mix("#17301F", M["haze"], 0.2)
    rim = M["rim"]
    ridge_pts = [(1040, 770), (1110, 735), (1190, 690), (1290, 612), (1400, 540), (1520, 478), (1650, 420), (1790, 372), (1960, 338), (2140, 322), (2240, 320)]
    ridge = _ridge(0, 0, ridge_pts)
    # arka sırt (daha açık, sisli)
    back = [(1160, 760), (1250, 668), (1370, 588), (1520, 520), (1680, 470), (1850, 440), (2020, 420), (2260, 410)]
    bp = [(xo(x), y) for x, y in back] + [(xo(2260), 800), (xo(1160), 800)]
    f.path(sk.smooth_path(bp, True, 0.4), color=mix(mid_land, M["haze"], 0.35))
    # ana burun
    pts = [(xo(x), y) for x, y in ridge_pts] + [(xo(2260), 820), (xo(1040), 820)]
    land = sk.smooth_path(pts, True, 0.38)
    f.path(land, shader=f.lin(0, 320, 0, 780, [(mix(mid_land, "#000000", 0.0), 0.0), (dark_land, 0.55), (mix(dark_land, "#000000", 0.4), 1.0)]))
    f.path(sk.smooth_path([(xo(x), y) for x, y in ridge_pts], False, 0.38), style="stroke", sw=2.2, color=rim, alpha=0.55)
    f.c.save()
    f.c.clipPath(land, skia.ClipOp.kIntersect, True)
    # çalılık/ağaç öbekleri
    rs = RS(31)
    for i in range(46):
        x = 1140 + rs.rand() * 1100
        y = ridge(x) + 12 + rs.rand() * 120
        _tree_clump(f, xo(x), y, 16 + rs.rand() * 26, mix("#0B1A10", M["haze"], 0.08 + rs.rand() * 0.1), rs)
    # çayır çizgileri (yamaç)
    for i in range(30):
        x = 1100 + rs.rand() * 1100
        y = ridge(x) + 30 + rs.rand() * 160
        f.line(xo(x), y, xo(x + 90 + rs.rand() * 120), y + 12 + rs.rand() * 20, color=mix("#274A2C", M["haze"], 0.25), sw=3, alpha=0.18)
    f.c.restore()
    # köy: yamaçtan kıyıya inen evler
    rs = RS(77)
    wall0 = mix("#D9CDB0", M["haze"], 0.42 + (0.05 if storm else 0))
    roof0 = mix("#4A2A1E", M["haze"], 0.12)
    lit = mood in ("storm", "dusk", "night", "dawn")
    xs_ = np.linspace(1115, 1560, 20)
    houses = []
    for i, x in enumerate(xs_):
        x += rs.randn() * 12
        base = ridge(x) + 46 + rs.rand() * 34 + (i % 3) * 26
        base = min(base, 758 - (i % 2) * 7)
        w = 40 + rs.rand() * 34
        houses.append((x, base, w, 26 + rs.rand() * 22, 16 + rs.rand() * 12))
    houses.sort(key=lambda h_: h_[1])
    for x, base, w, h, rh in houses:
        _house(f, xo(x), base, w, h, rh, mix(wall0, "#000000", 0.18 * (1 - (base - 600) / 200.0 if base > 600 else 0)), roof0, lit, rs)
    # kilise (çan kulesi + sundurma) — tepe konumunda
    cx = 1330
    cy = ridge(cx) + 70
    f.rect(xo(cx) - 24, cy - 70, 48, 70, color=mix(wall0, "#000000", 0.2))
    f.poly([(xo(cx) - 28, cy - 70), (xo(cx), cy - 100), (xo(cx) + 28, cy - 70)], color=roof0)
    tw = 20
    f.rect(xo(cx + 44) - tw / 2, cy - 108, tw, 108, color=mix(wall0, "#000000", 0.25))
    f.poly([(xo(cx + 44) - tw / 2 - 3, cy - 108), (xo(cx + 44), cy - 142), (xo(cx + 44) + tw / 2 + 3, cy - 108)], color=roof0)
    f.path(sk.smooth_path([(xo(cx + 44) - 5, cy - 88), (xo(cx + 44) - 5, cy - 98), (xo(cx + 44), cy - 104), (xo(cx + 44) + 5, cy - 98), (xo(cx + 44) + 5, cy - 88)], True, 0.2), color="#0A0705")
    f.line(xo(cx + 44), cy - 142, xo(cx + 44), cy - 158, color="#0A0705", sw=2)
    f.line(xo(cx + 44) - 6, cy - 151, xo(cx + 44) + 6, cy - 151, color="#0A0705", sw=2)
    if lit:
        f.rect(xo(cx) - 4, cy - 40, 8, 16, color="#FFC770")
        PW.glow_add(f, xo(cx), cy - 32, 34, "#FFB347", 0.7)
    # mendirek (taş dalgakıran) + fener
    mx0, mx1 = 1000, 1300
    f.path(sk.poly_path([(xo(mx0), 764), (xo(mx0 + 30), 748), (xo(mx1), 746), (xo(mx1 + 20), 758), (xo(mx1), 770), (xo(mx0), 776)], True), color=mix("#18130E", M["haze"], 0.08))
    f.rect(xo(mx1 - 3) - 5, 726, 10, 22, color="#120D09")
    f.poly([(xo(mx1 - 3) - 8, 726), (xo(mx1 - 3), 716), (xo(mx1 - 3) + 8, 726)], color="#120D09")
    PW.glow_add(f, xo(mx1 - 3), 734, 60, "#FFC770", 0.75)
    f.circle(xo(mx1 - 3), 735, 3.2, color="#FFEBB0")
    # sahilde kayalar / kıyı kenarı karanlığı
    for i in range(14):
        x = 1030 + i * 38 + rs.rand() * 20
        f.oval(xo(x), 762 + rs.rand() * 8, 22 + rs.rand() * 24, 8 + rs.rand() * 6, color="#0C0A08")


def bake_coast_africa(f, M, mood, side):
    """Kuzey Afrika limanı: alçak kum sırtı, teraslı beyaz şehir, minareler, kubbeler, kale/sur, palmiye."""
    sgn = -1 if side == "l" else 1
    xo = lambda x: x if sgn > 0 else W - x
    wall0 = mix("#E8D8B6", M["haze"], 0.55)
    wall_d = mix("#BFA77A", M["haze"], 0.6)
    land = mix("#5A4630", M["haze"], 0.55)
    ridge_pts = [(900, 752), (1000, 714), (1120, 660), (1260, 612), (1400, 590), (1540, 574), (1700, 570), (1900, 560), (2240, 556)]
    ridge = _ridge(0, 0, ridge_pts)
    pts = [(xo(x), y) for x, y in ridge_pts] + [(xo(2260), 820), (xo(900), 820)]
    f.path(sk.smooth_path(pts, True, 0.3), shader=f.lin(0, 560, 0, 780, [(mix(land, M["haze"], 0.2), 0.0), (mix(land, "#000000", 0.25), 1.0)]))
    rs = RS(55)
    lit = mood in ("dusk", "night", "storm", "dawn")
    # terasları ev blokları: tepeden denize
    cols = []
    for row in range(5):
        yb = 745 - row * 26
        x = 940 + row * 60
        while x < 1780 - row * 40:
            w = 36 + rs.rand() * 44
            h = 22 + rs.rand() * 30 + row * 4
            top = yb - h
            if top < ridge(x) - 8:
                top = ridge(x) - 8
                h = yb - top
            col = mix(wall0, wall_d, rs.rand() * 0.5 + row * 0.08)
            f.rect(xo(x) - (w / 2 if sgn > 0 else w / 2), top, w, h, color=col)
            f.rect(xo(x) - w / 2, top, w, 4, color=lighten(col, 0.2), alpha=0.5)
            f.rect(xo(x) - w / 2, top, w, h, shader=f.lin(xo(x) - w / 2, 0, xo(x) + w / 2, 0, [("#000000", 0.0, 70), ("#000000", 0.5, 0), ("#000000", 1.0, 100)]))
            if rs.rand() > 0.5:
                wx = xo(x) + (rs.rand() - 0.5) * w * 0.5
                wy = top + h * (0.35 + rs.rand() * 0.3)
                if lit and rs.rand() > 0.4:
                    f.rect(wx - 2.5, wy - 4, 5, 8, color="#FFC770")
                    PW.glow_add(f, wx, wy, 13, "#FFB347", 0.6)
                else:
                    f.rect(wx - 2.5, wy - 4, 5, 8, color="#1A120B", alpha=0.75)
            x += w * (0.9 + rs.rand() * 0.25)
    # kubbeler + minareler
    for (mx, mh, kind) in ((1180, 150, "min"), (1330, 120, "dome"), (1480, 170, "min"), (1630, 110, "dome"), (1010, 100, "min")):
        base = ridge(mx) + 62
        c_ = mix(wall0, "#000000", 0.08)
        if kind == "min":
            f.rect(xo(mx) - 5, base - mh, 10, mh, color=c_)
            f.rect(xo(mx) - 9, base - mh * 0.72, 18, 6, color=mix(c_, "#000000", 0.25))
            f.poly([(xo(mx) - 7, base - mh), (xo(mx), base - mh - 34), (xo(mx) + 7, base - mh)], color=mix(c_, "#000000", 0.2))
            f.circle(xo(mx), base - mh - 36, 2.5, color=mix(c_, "#000000", 0.2))
            if lit:
                f.circle(xo(mx), base - mh * 0.72 - 6, 2.6, color="#FFC770")
                PW.glow_add(f, xo(mx), base - mh * 0.72 - 6, 18, "#FFB347", 0.7)
        else:
            f.rect(xo(mx) - 34, base - mh * 0.5, 68, mh * 0.5, color=mix(c_, "#000000", 0.06))
            f.rect(xo(mx) - 30, base - mh * 0.5 - 9, 60, 10, color=mix(c_, "#000000", 0.2))
            f.path(sk.smooth_path([(xo(mx) - 30, base - mh * 0.5 - 8), (xo(mx) - 28, base - mh * 0.5 - 30), (xo(mx), base - mh * 0.5 - 42), (xo(mx) + 28, base - mh * 0.5 - 30), (xo(mx) + 30, base - mh * 0.5 - 8)], True, 0.5), color=mix(c_, "#000000", 0.32))
            f.line(xo(mx), base - mh * 0.5 - 42, xo(mx), base - mh * 0.5 - 58, color=mix(c_, "#000000", 0.4), sw=2)
    # sur ve kule (denize bakan)
    wy = 744
    f.path(sk.poly_path([(xo(860), wy + 14), (xo(860), wy - 30), (xo(1900), wy - 34), (xo(1900), wy + 14)], True), color=mix(wall_d, "#000000", 0.2))
    for x in range(860, 1900, 22):
        f.rect(xo(x) - 5, wy - 42, 10, 10, color=mix(wall_d, "#000000", 0.2))
    for tx in (900, 1220, 1620, 1880):
        f.rect(xo(tx) - 20, wy - 76, 40, 86, color=mix(wall_d, "#000000", 0.28))
        for q in range(4):
            f.rect(xo(tx) - 20 + q * 11, wy - 86, 7, 11, color=mix(wall_d, "#000000", 0.28))
        if lit:
            f.rect(xo(tx) - 2, wy - 56, 4, 12, color="#FFC770")
    # fener kulesi
    lx = 880
    f.rect(xo(lx) - 11, wy - 140, 22, 150, color=mix(wall_d, "#000000", 0.35))
    f.rect(xo(lx) - 15, wy - 150, 30, 12, color=mix("#000000", wall_d, 0.2))
    PW.glow_add(f, xo(lx), wy - 158, 90, "#FFC770", 0.7 if lit else 0.25)
    f.rect(xo(lx) - 6, wy - 168, 12, 18, color="#FFEBB0", alpha=0.85 if lit else 0.3)
    # palmiyeler
    for pi, x in enumerate((1090, 1150, 1760, 1810, 1700)):
        px = xo(x)
        base = ridge(x) + 60
        hgt = 96 + (pi % 3) * 14
        lean = (-1) ** pi * 8
        f.path(sk.smooth_path([(px, base), (px + lean * 0.4, base - hgt * 0.4), (px + lean * 0.9, base - hgt * 0.8), (px + lean, base - hgt)], False, 0.5), style="stroke", sw=4.2, color="#17120C", cap="round")
        tx, ty = px + lean, base - hgt
        for k in range(9):
            a_ = -math.pi + (k + 0.5) * math.pi / 9 + (0.0 if k != 4 else 0.0)
            ln = 34 + (k % 3) * 8
            ex, ey = tx + math.cos(a_) * ln, ty + math.sin(a_) * ln * 0.55 + ln * 0.35
            mx, my = tx + math.cos(a_) * ln * 0.55, ty + math.sin(a_) * ln * 0.85 - 4
            fr = skia.Path()
            fr.moveTo(tx, ty)
            fr.quadTo(mx, my - 4, ex, ey)
            fr.quadTo(mx, my + 5, tx, ty + 2)
            f.path(fr, color="#17120C")
    # ışık yansıması rim
    f.path(sk.smooth_path([(xo(x), y) for x, y in ridge_pts], False, 0.3), style="stroke", sw=2, color=M["rim"], alpha=0.35)


def bake_coast_harbor(f, M, mood, side):
    """Liman: taş rıhtım, fener kulesi, ambarlar, çan kulesi, bağlı gemi direkleri."""
    sgn = 1 if side == "r" else -1
    xo = lambda x: x if sgn > 0 else W - x
    wall0 = mix("#CDBF9E", M["haze"], 0.5)
    roof0 = mix("#3C241A", M["haze"], 0.2)
    lit = mood in ("dusk", "night", "storm", "dawn")
    rs = RS(66)
    # kara şeridi ve arkada tepeler
    ridge_pts = [(980, 760), (1100, 700), (1250, 650), (1450, 620), (1700, 600), (2000, 590), (2260, 586)]
    ridge = _ridge(0, 0, ridge_pts)
    pts = [(xo(x), y) for x, y in ridge_pts] + [(xo(2260), 820), (xo(980), 820)]
    f.path(sk.smooth_path(pts, True, 0.35), color=mix("#1E2418", M["haze"], 0.35))
    # şehir
    for i in range(30):
        x = 1020 + i * 38 + rs.randn() * 8
        base = 740 - (i % 4) * 14
        w = 34 + rs.rand() * 30
        h = 30 + rs.rand() * 40
        _house(f, xo(x), base, w, h, 14 + rs.rand() * 16, mix(wall0, "#000000", 0.1 + 0.1 * (i % 3)), roof0, lit, rs)
    # çan kuleleri / kule
    for (tx, th) in ((1210, 150), (1530, 120)):
        f.rect(xo(tx) - 14, 740 - th, 28, th, color=mix(wall0, "#000000", 0.25))
        f.poly([(xo(tx) - 18, 740 - th), (xo(tx), 740 - th - 46), (xo(tx) + 18, 740 - th)], color=roof0)
        if lit:
            f.rect(xo(tx) - 3, 740 - th * 0.7, 6, 12, color="#FFC770")
            PW.glow_add(f, xo(tx), 740 - th * 0.7, 20, "#FFB347", 0.7)
    # rıhtım
    f.path(sk.poly_path([(xo(900), 760), (xo(980), 742), (xo(1760), 742), (xo(1790), 760), (xo(1760), 776), (xo(900), 780)], True), color="#14100B")
    for x in range(920, 1760, 46):
        f.rect(xo(x) - 3, 742, 6, 14, color="#0C0907", alpha=0.7)
    # fener
    lx = 1790
    f.rect(xo(lx) - 12, 628, 24, 118, color="#17110C")
    f.rect(xo(lx) - 18, 616, 36, 14, color="#17110C")
    f.poly([(xo(lx) - 18, 616), (xo(lx), 592), (xo(lx) + 18, 616)], color="#17110C")
    f.rect(xo(lx) - 7, 598, 14, 20, color="#FFEBB0")
    PW.glow_add(f, xo(lx), 608, 130, "#FFC770", 0.9)
    # rıhtım meşaleleri
    for x in range(1000, 1740, 130):
        PW.glow_add(f, xo(x), 732, 36, "#FFB347", 0.8)
        f.circle(xo(x), 733, 2.4, color="#FFE7A6")
    f.path(sk.smooth_path([(xo(x), y) for x, y in ridge_pts], False, 0.35), style="stroke", sw=2, color=M["rim"], alpha=0.35)


# ───────────────────────────── gemi çizimi (dyn) ─────────────────────────────
def _vis(f):
    """Geçerli dönüşümde görünür dikdörtgen (katman koordinatı): (l, t, r, b)."""
    try:
        b = f.c.getLocalClipBounds()
        return (b.left(), b.top(), b.right(), b.bottom())
    except Exception:
        return None


def _flash_env(t, seed, amount):
    """Şimşek parlaması zarfı ve olayı: (env, olay_id, olay_t)."""
    if amount <= 0:
        return 0.0, -1, 0.0
    per = 3.4 / (0.35 + amount)
    best = (0.0, -1, 0.0)
    k0 = int(t / per) - 1
    for k in range(k0, k0 + 3):
        if k < 0:
            continue
        rs = RS(seed * 131 + k)
        T = k * per + rs.rand() * per * 0.55
        age = t - T
        if age < 0 or age > 0.9:
            continue
        e = math.exp(-age / 0.075) * (1.0 if age < 0.35 else 0.0) + 0.65 * math.exp(-max(0.0, age - 0.17) / 0.07) * (1.0 if age >= 0.17 else 0.0)
        e *= (0.6 + 0.4 * rs.rand())
        if e > best[0]:
            best = (e, k, age)
    return best


def _ship_defaults(M, mood, sh):
    d = dict(kind="carrack", x=0.5, row=0, s=1.0, flag="#8E1F26", heading=1, rock=None, sink=0.0, burn=0.0, gun=0.0, sails=None, emblem="auto", lamp=None, drift=None)
    d.update(sh)
    d["row"] = int(clamp(d["row"], 0, 3))
    if d["rock"] is None:
        d["rock"] = 1.0 if mood == "storm" else 0.28
    if d["sails"] is None:
        d["sails"] = "reef" if mood == "storm" and d["kind"] == "carrack" else "full"
    if d["emblem"] == "auto":
        c = d["flag"].lstrip("#")
        r_, g_, b_ = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
        d["emblem"] = "crescent" if (g_ > r_ * 1.05 and g_ >= b_) else "cross"
    return d


def _wave_h(t, ph, A, w):
    return A * (math.sin(w * t + ph) + 0.45 * math.sin(w * 1.63 * t + ph * 2.1 + 1.3))


def draw_ship(f, M, mood, sh, t, wind, flash, fire_flash, idx, vis=None):
    """Tek gemi: sprite + hareketli parçalar (bayrak, kürek, alev, duman, köpük)."""
    kind = sh["kind"]
    row = sh["row"]
    srow = ROW_S[row] * sh["s"]
    yw = ROW_Y[row]
    head = 1 if sh["heading"] >= 0 else -1
    ph = idx * 1.93 + 0.7
    w1 = (0.62 + 0.55 * (M["speed"] - 0.9)) * (1.0)
    rock = sh["rock"]
    sink = clamp(sh["sink"])
    burn = clamp(sh["burn"])
    drift = sh["drift"] if sh["drift"] is not None else (7.0 * ROW_S[row] * (1.0 if sink <= 0 else 0.0))
    x = sh["x"] * W + head * drift * t
    A = (2.2 + 11.0 * rock) * srow ** 0.8
    heave = _wave_h(t, ph, A, w1) * 0.8
    roll_amp = 0.012 + 0.085 * rock
    roll = roll_amp * (math.sin(w1 * t + ph + 0.9) + 0.5 * math.sin(w1 * 1.63 * t + ph * 1.3)) * head
    tilt_sink = sink * 0.46 * head * (-1 if idx % 2 else 1)
    dy_sink = sink * 175 * srow
    lod = 2 if srow >= 0.6 else 1 if srow >= 0.32 else 0
    ks = round(max(0.25, min(2.0, srow * 1.3)) * 8) / 8.0
    cross = sh["flag"] if sh["emblem"] == "cross" else ""
    lamp = sh["lamp"] if sh["lamp"] is not None else M["lamp"]
    hk = {0: 0.0, 1: 0.10, 2: 0.24, 3: 0.36}[row] * (1.0 if mood != "storm" else 1.25)
    hz = M["haze"]
    sprite = SW.ship_sprite(kind, ks, mix(M["hull"], hz, hk * 0.8), mix(M["rim"], hz, hk * 0.5), mix(M["sail"], hz, hk), mix(M["sail_l"], hz, hk), mix(M["sail_d"], hz, hk), mix(M["gold"], hz, hk), cross, bool(lamp), M["lamp_col"], sh["sails"], round(burn, 1), M["light_dir"], sh["flag"], lod)
    img, ox, oy, k = sprite
    cs = f.c
    if vis is not None:
        bw = 330 * srow + 40
        if x + bw < vis[0] or x - bw > vis[2] or yw - 540 * srow - 60 > vis[3] or yw + 120 < vis[1]:
            return
    SAMP = LIN if srow / k >= 0.72 else LINMIP
    cs.save()
    if sink > 0 or row == 3:
        cs.clipRect(skia.Rect.MakeLTRB(-3000, -3000, 6000, yw - 1 + (0 if row == 3 else 9) + heave * 0.2))
    cs.translate(x, yw + heave + dy_sink)
    # yansıma (sakin sularda): ters, soluk, düşük çözünürlük — dönmeden (hızlı yol)
    if mood in ("calm", "dawn", "dusk", "night") and row <= 2 and sink < 0.3 and kind != "fishing":
        rimg, rox, roy, rk = SW.ship_reflect(kind, ks, M["hull"], M["sail"], M["sail_d"], M["haze"])
        pr = skia.Paint()
        pr.setAlphaf(0.30 if mood != "night" else 0.22)
        cs.save()
        cs.scale(srow * head / rk, srow / rk)
        cs.drawImage(rimg, -rox, 6 - roy, LIN, pr)
        cs.restore()
    theta = roll + tilt_sink
    cs.save()
    if abs(theta) < 0.16 and sink <= 0:
        # küçük açı: dikey dilimlerle hızlı "dönme" (gerçek döndürme çok yavaş)
        cs.scale(srow * head / k, srow / k)
        PW.draw_rolled(cs, img, ox, oy, theta * head, SAMP, None, 7.0, srow / k)
    else:
        cs.rotate(math.degrees(theta))
        cs.scale(srow * head / k, srow / k)
        cs.drawImage(img, -ox, -oy, SAMP, skia.Paint())
    cs.restore()
    cs.rotate(math.degrees(theta))
    cs.scale(srow * head, srow)
    # ── bayraklar
    fl = sh["flag"]
    emb = sh["emblem"]
    wf = -1  # kıç yönü (yerel x)
    sp = 4.2 * (0.8 + 0.5 * M["speed"])
    if kind == "carrack" and sh["sails"] != "bare":
        PW.flag_cloth(f, -5, -452, 92, 30, fl, t, emblem="none", trim=None, wind=wf, seed=idx, speed=sp, cut="swallow")
        PW.flag_cloth(f, 138, -352, 70, 24, fl, t, emblem="none", wind=wf, seed=idx + 1, speed=sp, cut="swallow")
        PW.flag_cloth(f, -160, -318, 60, 20, fl, t, emblem="none", wind=wf, seed=idx + 2, speed=sp, cut="swallow")
        f.line(-208, -204, -214, -268, color=M["hull"], sw=3.0)
        PW.flag_cloth(f, -214, -268, 110, 64, fl, t, emblem=emb, trim=M["gold"], wind=wf, seed=idx + 3, speed=sp, cut=None, emb="#F3E6C0")
    elif kind == "galley":
        PW.flag_cloth(f, 58, -318, 78, 24, fl, t, emblem="none", wind=wf, seed=idx, speed=sp, cut="swallow")
        PW.flag_cloth(f, 198, -238, 60, 18, fl, t, emblem="none", wind=wf, seed=idx + 1, speed=sp, cut="swallow")
        f.line(-246, -176, -248, -226, color=M["hull"], sw=3.0)
        PW.flag_cloth(f, -248, -226, 96, 52, fl, t, emblem=emb, trim=M["gold"], wind=wf, seed=idx + 3, speed=sp, cut=None, emb="#F3E6C0")
    elif kind == "fishing" and sh["sails"] != "bare":
        PW.flag_cloth(f, 14, -206, 34, 12, fl, t, emblem="none", wind=wf, seed=idx, speed=sp, cut="swallow")
    # ── kürekler
    if kind == "galley":
        _oars(f, M, t, idx, rock, sink)
    # ── fener parıltısı
    if lamp and kind != "fishing":
        fk = 0.8 + 0.2 * math.sin(t * 7.3 + idx * 2.0) * math.sin(t * 3.1 + idx)
        if kind == "carrack":
            PW.glow(f, -242, -250, 120, M["lamp_col"], 0.9 * fk)
        else:
            for (lx, lh) in ((-252, 72), (-240, 108), (-228, 144)):
                PW.glow(f, lx, -128 - lh - 12, 56, M["lamp_col"], 0.7 * fk)
    elif lamp and kind == "fishing":
        PW.glow(f, 104, -56, 40, M["lamp_col"], 0.8 * (0.85 + 0.15 * math.sin(t * 6 + idx)))
    # ── köpük (su hattı)
    foam = PW.glow_sprite  # ucuz: elips parıltı olarak
    pf = skia.Paint()
    pf.setAlphaf(0.40 if mood == "storm" else 0.22)
    L = {"carrack": 250, "galley": 270, "fishing": 100}[kind]
    for q, (fx, fw, fa) in enumerate(((0.0, 1.0, 1.0), (L * 0.86, 0.42, 1.2))):
        g = PW.glow_sprite(64, M["foam"], 190, 80, 0.5)
        cs.save()
        cs.translate(fx * (1 if q else 0), 6)
        cs.scale(L * fw / 64.0 * 1.15, 0.2 * L * fw / 64.0 * 0.5)
        cs.drawImage(g, -64, -64, LIN, pf)
        cs.restore()
    # ── ateş / yanma
    if burn > 0.05:
        fxs = {"carrack": (-170, -90, -20, 40, 100, 160), "galley": (-70, -20, 30, 80, 130, 180), "fishing": (-30, 0, 30)}[kind]
        fy = {"carrack": -88, "galley": -50, "fishing": -26}[kind]
        base = {"carrack": 1.25, "galley": 0.8, "fishing": 0.6}[kind]
        for q, fx in enumerate(fxs):
            sz = base * (0.45 + 0.75 * burn) * (0.75 + 0.5 * ((q * 7 + idx) % 5) / 4.0)
            PW.flame(f, fx, fy - (q % 2) * 6, sz, t, seed=idx * 5 + q, glow_a=0.7 * burn)
        PW.glow(f, 0, -80, 240 * burn + 60, "#FF8A2E", 0.5 * burn)
    # ── namlu alevi + duman
    if sh["gun"] > 0:
        _guns(f, M, t, idx, kind, sh["gun"], wind=wf)
    cs.restore()
    if burn > 0.05:
        # kuru duman sütunu (dünya ekseninde, gemiyle birlikte kayar)
        cs.save()
        cs.translate(x, yw + heave + dy_sink)
        PW.smoke_column(f, 0, -120 * srow, t, n=int(6 + 8 * burn), h=520 * srow ** 0.7 + 120, w0=14 * srow + 8, w1=70 * srow + 40, col="#15110E", a=0.55 * (0.6 + 0.4 * burn), rate=0.12, drift=-wind * 90, seed=idx + 3)
        cs.restore()
        # su üstü yansıma
        PW.glow(f, x, yw + 40 * srow, 220 * srow * (0.6 + burn), "#FF7A28", 0.35 * burn)
    if sink > 0.02:
        _sink_fx(f, M, t, x, yw, srow, sink, idx, mood)


class SimpleF:
    def __init__(self, f):
        self.f = f


def _oars(f, M, t, idx, rock, sink):
    """Kürekler: tek Path (kare başına 1 çizim)."""
    sp = 2.6 + 0.8 * M["speed"] * 0.5
    path = skia.Path()
    blade = skia.Path()
    n = SW.GAL_N_OARS
    for k in range(n):
        xx = SW.GAL_OAR_X0 + (SW.GAL_OAR_X1 - SW.GAL_OAR_X0) * k / (n - 1)
        ph = t * sp - k * 0.035 + idx * 0.9
        cphi = math.cos(ph)
        sphi = math.sin(ph)
        x_tip = xx + 40 * cphi - 26
        y_tip = SW.GAL_OAR_Y + 66 + 22 * sphi + (1.0 - sink) * 0 + 10
        path.moveTo(xx, SW.GAL_OAR_Y - 8)
        path.lineTo(x_tip, y_tip)
        ux, uy = x_tip - xx, y_tip - (SW.GAL_OAR_Y - 8)
        L = math.hypot(ux, uy)
        ux, uy = ux / L, uy / L
        bl = 24
        nx, ny = -uy, ux
        blade.moveTo(x_tip - ux * bl + nx * 3.4, y_tip - uy * bl + ny * 3.4)
        blade.lineTo(x_tip + nx * 4.0, y_tip + ny * 4.0)
        blade.lineTo(x_tip - nx * 4.0, y_tip - ny * 4.0)
        blade.lineTo(x_tip - ux * bl - nx * 3.4, y_tip - uy * bl - ny * 3.4)
        blade.close()
    f.c.drawPath(path, skia.Paint(AntiAlias=True, Color=C(M["hull"]), Style=skia.Paint.kStroke_Style, StrokeWidth=3.0, StrokeCap=skia.Paint.kRound_Cap))
    f.c.drawPath(blade, skia.Paint(AntiAlias=True, Color=C(M["hull"])))
    f.c.drawPath(path, skia.Paint(AntiAlias=True, Color=C(M["rim"], 90), Style=skia.Paint.kStroke_Style, StrokeWidth=0.9))


def _guns(f, M, t, idx, kind, amount, wind=-1):
    """Top atışları: periyodik namlu alevi + büyüyen/dağılan duman."""
    period = 3.6 / (0.25 + amount)
    nguns = 3
    for g in range(nguns):
        off = (g * 1.37 + idx * 0.83) % period
        k = int((t - off) // period)
        for kk in (k - 1, k):
            T = kk * period + off
            age = t - T
            if age < 0 or age > 7.5 or kk < 0:
                continue
            rs = RS(idx * 977 + g * 31 + kk)
            gx = lerp(-70, 170, rs.rand())
            gy = {"carrack": -42, "galley": -64}.get(kind, -40)
            if kind == "carrack":
                gy = -34 - rs.rand() * 10
            if age < 0.16:
                e = 1 - age / 0.16
                PW.glow(f, gx + 10, gy, 120 * (0.5 + e), "#FFC66B", 1.0 * e, 255, 140, 0.4)
                PW.glow(f, gx + 10, gy, 44 * (0.5 + e), "#FFF1C4", 1.0 * e)
            # duman
            u = age / 7.5
            r = 26 + 120 * u ** 0.6
            a = 0.62 * (1 - u) ** 1.2 * min(1.0, age * 3)
            px = gx + wind * (age * 16 + 6) * (1.0 if wind else 0) - 6
            py = gy - 14 - age * 11
            PW.puff(f, px, py, r, "#9C9288" if M["bright"] > 0.85 else "#5C5C60", a, seed=kk + g, rot=age * 0.2)
            PW.puff(f, px + wind * r * 0.45, py - r * 0.2, r * 0.7, "#8A8078" if M["bright"] > 0.85 else "#505458", a * 0.8, seed=kk + g + 2, rot=-age * 0.3)


def _sink_fx(f, M, t, x, yw, srow, sink, idx, mood):
    """Batan gemi: köpük halkası, kabarcık/sıçrama, enkaz."""
    rs = RS(idx + 99)
    pf = skia.Paint()
    g = PW.glow_sprite(64, M["foam"], 220, 110, 0.5)
    for q in range(3):
        u = (t * 0.5 + q / 3.0) % 1.0
        pf.setAlphaf(0.5 * (1 - u) * min(1.0, sink * 3))
        f.c.save()
        f.c.translate(x + (q - 1) * 30 * srow, yw + 6 + u * 4)
        f.c.scale((130 + 150 * u) * srow / 64.0, (12 + 14 * u) * srow / 64.0)
        f.c.drawImage(g, -64, -64, LIN, pf)
        f.c.restore()
    for i in range(14):
        u = (t * 0.8 + rs.rand()) % 1.0
        px = x + (rs.rand() - 0.5) * 240 * srow * (0.4 + u)
        py = yw - u * 70 * srow * (0.6 + rs.rand()) + 6
        f.c.drawCircle(px, py, (1.2 + 2.4 * rs.rand()) * (1 - u * 0.5), skia.Paint(AntiAlias=True, Color=C(M["foam"], int(255 * (1 - u) * 0.8))))
    for i in range(6):          # enkaz (tahta parçaları)
        ex = x + (rs.rand() - 0.5) * 520 * srow + math.sin(t * 0.9 + i) * 8
        ey = yw + 2 + math.sin(t * 1.3 + i * 2) * 3
        a = (rs.rand() - 0.5) * 0.6 + math.sin(t + i) * 0.1
        f.c.save()
        f.c.translate(ex, ey)
        f.c.rotate(math.degrees(a))
        f.c.drawRect(skia.Rect.MakeXYWH(-14 * srow - 4, -2, 28 * srow + 8, 3.4), skia.Paint(Color=C(M["hull"])))
        f.c.restore()


# ───────────────────────────── sahne ─────────────────────────────
@SL.sc("sea")
class Sea:
    """Deniz sahnesi. p: mood, ships, coast, coast_side, lightning, rain, moon, smoke, wind (bkz. SAHNE_KATALOGU_deniz_savas.md)."""

    def __init__(self, p):
        self.p = p
        self.mood = p.get("mood", "calm")
        if self.mood not in MOODS:
            self.mood = "calm"
        self.M = MOODS[self.mood]
        st = self.mood == "storm"
        self.rain = float(p.get("rain", 0.85 if st else 0.0))
        self.lightning = float(p.get("lightning", 0.7 if st else 0.0))
        self.coast = p.get("coast")
        self.side = p.get("coast_side", "l" if self.coast == "africa" else "r")
        self.smoke = float(p.get("smoke", 0.0))
        self.mist = float(p.get("mist", 0.0))
        self.wind = 1 if p.get("wind", -1) >= 0 else -1
        ships = p.get("ships")
        if ships is None:
            ships = [dict(kind="carrack", x=0.5, row=0)]
        self.ships = [_ship_defaults(self.M, self.mood, s) for s in ships]
        self.mi = self.mood
        self._extra = []
        sun = self.M["sun"]
        if sun:
            self._ref = (sun[0] * W, sun[4], 0.9)
        elif self.M["moon"] or p.get("moon"):
            self._ref = (W * 0.30, "#CFE0F0", 0.6)
        else:
            self._ref = None
        self._ref_sx = None

    # --- statik: tek taban katman (gök + ufuk + uzak su). Bantlar/gemiler/kıyı dyn içinde, kırpılmış görüntülerle ve kendi paralaksıyla çizilir
    # (tam boy katman görüntüsü kamera yakınlaştırınca ~10 ms/katman; kırpılmış bant görüntüsü çok daha ucuz).
    def layers(self):
        M, mood, p = self.M, self.mood, self.p

        def base(f):
            bake_sky(f, M, mood, p)
            bake_far(f, M, mood, p)
        return [(BASE_D, base)]

    # --- dinamik
    def dyn(self):
        M, mood = self.M, self.mood
        coast = self.coast
        t_cache = {}

        def flash_at(t):
            if t not in t_cache:
                t_cache[t] = _flash_env(t, 3, self.lightning)
            return t_cache[t]

        wspd = M["wave_spd"]
        wind = self.wind

        def D_sky(f, t):
            if self._ref is not None:
                try:
                    self._ref_sx = f.c.getTotalMatrix().mapXY(self._ref[0], HZ).x()
                except Exception:
                    self._ref_sx = None
            sp = 3.0 + 0.9 * wspd * 0.5 * (1.8 if mood == "storm" else 1.0)
            c1 = _cloud_img(mood, 7 if mood != "storm" else 21, "low")
            wpx = c1.width() * 2
            off = (t * sp) % wpx
            x_a = (-MARGIN - wpx + off) if wind > 0 else (-MARGIN - off)
            for dx in (0, wpx):
                _draw_cloud(f, c1, x_a + dx, -MARGIN + 150 + (HZ + MARGIN + 60) * 0.44, 0.7 if mood != "storm" else 0.9)
            e, ev, age = flash_at(t)
            if mood == "night" or M["stars"] > 0.5:
                rs = RS(9)
                for i in range(9):
                    x = rs.rand() * (W + 2 * MARGIN) - MARGIN
                    y = rs.rand() * 380 - 120
                    a = 0.5 + 0.5 * math.sin(t * (1.0 + rs.rand() * 2) + i * 3)
                    PW.glow(f, x, y, 12 + 6 * a, "#CFE0FF", 0.55 * a)
            if e > 0.02:
                rs = RS(3 * 131 + ev)
                bx = 160 + rs.rand() * (W - 320)
                PW.glow(f, bx, 90, 1100, "#B7C9FF", 0.62 * e, 255, 110, 0.35)
                if e > 0.25:
                    bs = PW.bolt_sprite(1 + (ev % 4) * 2 + 1, int(300 + rs.rand() * 120))
                    p_ = skia.Paint()
                    p_.setAlphaf(clamp(e * 1.3))
                    f.c.save()
                    f.c.translate(bx - bs.width() / 2, 60)
                    f.c.drawImage(bs, 0, 0, LIN, p_)
                    f.c.restore()

        def master(f, t):
            cam = SW.cam_from_canvas(f, BASE_D)
            D_sky(f, t)
            e, ev, age = flash_at(t)
            vis = _vis(f)
            for i, sh in enumerate(self.ships):
                if sh["row"] == 3:
                    draw_ship(f, M, mood, sh, t, wind, e, 0.0, i, vis)
            self._glitter(f, t)
            rowmap = {0: 2, 1: 1, 2: 0}
            for k in range(5):
                SW.push_depth(f, cam, BAND_D[k])
                bimg, bx, by = band_image(mood, k)
                f.c.drawImage(bimg, bx, by, LIN, skia.Paint())
                self._strips(f, t, k)
                if k in rowmap:
                    vis = _vis(f)
                    for i, sh in enumerate(self.ships):
                        if sh["row"] == rowmap[k]:
                            draw_ship(f, M, mood, sh, t, wind, e, 0.0, i, vis)
                if k == 0:
                    self._battle_smoke(f, t, 0, False)
                if k in (0, 1, 3):
                    self._mist(f, t, k)
                if k == 2:
                    self._battle_smoke(f, t, 2, True)
                f.c.restore()
                if k == 1 and coast:
                    SW.push_depth(f, cam, COAST_D)
                    cimg, cx_, cy_ = coast_image(coast, mood, self.side)
                    f.c.drawImage(cimg, cx_, cy_, LIN, skia.Paint())
                    self._coast_dyn(f, t)
                    f.c.restore()
            self._overlay(f, t, e)
        return {0: master}

    # --- yardımcılar
    def _glitter(self, f, t):
        M = self.M
        sun = M["sun"]
        if sun:
            rx, col = sun[0] * W, sun[4]
        elif M["moon"] or self.p.get("moon"):
            rx, col = W * 0.30, "#CFE0F0"
        else:
            return
        rs = RS(17)
        p_ = skia.Paint(AntiAlias=True)
        p_.setBlendMode(PLUS)
        for i in range(34):
            u = rs.rand() ** 1.5
            y = HZ + 8 + u * 330
            sp = 0.5 + rs.rand() * 1.2
            a = 0.5 + 0.5 * math.sin(t * sp * 3 + i * 5.1)
            if a < 0.35:
                continue
            x = rx + (rs.rand() - 0.5) * (30 + u * 340) + math.sin(t * 0.7 + i) * 6
            wdt = 4 + u * 26 * rs.rand() + 3
            p_.setColor(C(col, int(255 * 0.55 * a * (1 - u * 0.4))))
            f.c.drawRect(skia.Rect.MakeXYWH(x - wdt / 2, y, wdt, 1.4 + u * 1.6), p_)

    def _strips(self, f, t, k):
        M, mood = self.M, self.mood
        A = _amp(M, k)
        y0 = BAND_Y[k] - int(A) - 1
        sp = M["wave_spd"] * (0.35 + 0.5 * k)
        a = _strip_set(M, mood, k, 0)
        b = _strip_set(M, mood, k, 1)
        bob = math.sin(t * (0.5 + 0.12 * k) + k) * (1.5 + 1.2 * k) * (M["amp"] if mood == "storm" else 0.6)
        PW.draw_strip(f, b, -MARGIN, W + MARGIN, y0 + 3 + bob * 0.5 - 6 - 2 * k, -self.wind * t * sp * 1.45 + 300 * k, alpha=0.55)
        PW.draw_strip(f, a, -MARGIN, W + MARGIN, y0 + bob, -self.wind * t * sp)
        self._reflect(f, t, k, y0)
        if mood == "storm" and k >= 2:
            self._spray(f, t, k, y0 + bob)

    def _reflect(self, f, t, k, y0):
        """Güneş/ay yolu: ekran uzayında sabit sütun, her bantta kıpırdayan parıltılar (kamera paralaksından bağımsız)."""
        if self._ref is None or self._ref_sx is None:
            return
        _, col, strength = self._ref
        inv = skia.Matrix()
        if not f.c.getTotalMatrix().invert(inv):
            return
        xl = inv.mapXY(self._ref_sx, 0).x()
        ytop = BAND_Y[k] - _amp(self.M, k)
        ybot = (BAND_Y[k + 1] - _amp(self.M, k + 1)) if k < 4 else H + 140
        u_mid = clamp(((ytop + ybot) / 2 - HZ) / (H - HZ))
        wd = 60 + 420 * u_mid
        g = PW.glow_sprite(128, col, 160, 60, 0.45)
        pg = skia.Paint()
        pg.setAlphaf(0.28 * strength)
        f.c.save()
        f.c.translate(xl, (ytop + ybot) / 2 + 10)
        f.c.scale(wd / 128.0, (ybot - ytop) * 0.75 / 128.0)
        f.c.drawImage(g, -128, -128, LIN, pg)
        f.c.restore()
        rs = RS(300 + k)
        p_ = skia.Paint(AntiAlias=True)
        p_.setBlendMode(PLUS)
        n = 14 + 8 * k
        for i in range(n):
            y = ytop + 4 + rs.rand() * (ybot - ytop - 6)
            u = clamp((y - HZ) / (H - HZ))
            wc = 40 + 340 * u
            x = xl + rs.randn() * wc * 0.30 + math.sin(t * 0.7 + i * 1.3) * 6
            a = 0.5 + 0.5 * math.sin(t * (1.0 + rs.rand() * 2.2) * 2 + i * 3.1)
            if a < 0.3:
                continue
            fall = 1.0 - clamp(abs(x - xl) / wc) ** 1.3
            w_ = 5 + 34 * u * rs.rand() + 3
            p_.setColor(C(col, int(255 * clamp(0.75 * strength * a * fall * (1 - 0.3 * u)))))
            f.c.drawRect(skia.Rect.MakeXYWH(x - w_ / 2, y, w_, 1.3 + 2.2 * u), p_)

    def _mist(self, f, t, k):
        """Deniz sisi (mist=0..1): ufka yakın geniş, çok saydam buğu kabarcıkları."""
        ms = self.mist
        if ms <= 0.02:
            return
        rs = RS(700 + k)
        col = self.M["haze"]
        n = int(5 + 9 * ms)
        by = BAND_Y[k]
        for i in range(n):
            x = ((rs.rand() * (W + 1200) - 600) + t * (4 + 6 * rs.rand()) * -self.wind) % (W + 1200) - 600
            y = by - 30 - rs.rand() * 90
            r = 190 + rs.rand() * 260
            a = (0.10 + 0.34 * ms) * (0.6 + 0.4 * math.sin(t * 0.2 + i * 2.1))
            PW.puff(f, x, y, r, col, a, seed=i + k, rot=0.4 * i)

    def _battle_smoke(self, f, t, k, front):
        """Barut dumanı: yavaş sürüklenen büyük saydam kabarcıklar (smoke=0..1)."""
        sm = self.smoke
        if sm <= 0.02:
            return
        M = self.M
        rs = RS(500 + k * 7 + (1 if front else 0))
        col = "#8A7F76" if M["bright"] > 0.85 else "#4C5258"
        if self.mood in ("dusk", "dawn"):
            col = "#8C6A58"
        n = int(6 + 12 * sm)
        by = BAND_Y[k]
        for i in range(n):
            ph = rs.rand()
            x = ((rs.rand() * (W + 900) - 450) + t * (6 + 10 * rs.rand()) * -self.wind) % (W + 900) - 450
            y = (by + 10 - rs.rand() * 190) if front else (by - 40 - rs.rand() * 150)
            r = 110 + rs.rand() * 170
            a = (0.14 + 0.36 * sm) * (0.55 + 0.45 * math.sin(t * 0.25 + i * 1.7)) * (1.0 if front else 0.85)
            PW.puff(f, x, y, r, col, a, seed=i + k, rot=0.3 * i)

    def _spray(self, f, t, k, y0):
        rs = RS(40 + k)
        n = 12 + 6 * k
        p_ = skia.Paint(AntiAlias=True)
        for i in range(n):
            ph = (t * (0.35 + rs.rand() * 0.5) + rs.rand()) % 1.0
            x = (rs.rand() * (W + 2 * MARGIN) - MARGIN + t * 30 * (-self.wind) * (0.4 + k * 0.2)) % (W + 2 * MARGIN) - MARGIN
            y = y0 + 8 - ph * (26 + 20 * k) * (0.5 + rs.rand())
            r = (1.0 + 1.7 * rs.rand()) * (0.7 + 0.3 * k)
            p_.setColor(C(self.M["foam"], int(255 * (1 - ph) * 0.7)))
            f.c.drawCircle(x, y, r, p_)

    def _coast_dyn(self, f, t):
        M, mood = self.M, self.mood
        side = self.side
        sgn = 1 if side == "r" else -1
        xo = lambda x: x if sgn > 0 else W - x
        e, ev, age = _flash_env(t, 3, self.lightning)
        if self.coast == "tazones":
            # küçük balıkçı tekneleri: mendirek önünde demirli
            for q, (bx, s_) in enumerate(((1130, 0.55), (1215, 0.45), (1340, 0.5))):
                sh = dict(kind="fishing", x=xo(bx) / W, row=1, s=s_ / ROW_S[1] * 0.0 + s_, flag="#7A2A24", heading=1 if sgn > 0 else -1, rock=0.5, sails="bare", drift=0.0)
                sh = _ship_defaults(M, self.mood, sh)
                sh["drift"] = 0.0
                self._boat(f, M, sh, t, 760 + (q % 2) * 6, e, q + 20)
            # kıyı köpüğü
            g = PW.glow_sprite(64, M["foam"], 200, 90, 0.5)
            pf = skia.Paint()
            for q in range(18):
                ph = (t * 0.35 + q * 0.37) % 1.0
                x = xo(1030 + q * 52 + math.sin(t * 0.8 + q) * 10)
                pf.setAlphaf((0.5 * math.sin(math.pi * ph)) * (0.9 if self.mood == "storm" else 0.45))
                f.c.save()
                f.c.translate(x, 764 + (1 - ph) * 5)
                f.c.scale((34 + 24 * ph) / 64.0, (6 + 4 * ph) / 64.0)
                f.c.drawImage(g, -64, -64, LIN, pf)
                f.c.restore()
        elif self.coast == "harbor":
            for q, (bx, s_) in enumerate(((1100, 0.75), (1330, 0.7), (1560, 0.78))):
                sh = _ship_defaults(M, self.mood, dict(kind="carrack", x=xo(bx) / W, row=1, s=s_ / ROW_S[1] * ROW_S[1], flag="#2D5A8E", heading=1 if sgn > 0 else -1, rock=0.2, sails="bare", drift=0.0))
                sh["drift"] = 0.0
                self._boat(f, M, sh, t, 774 + (q % 2) * 5, e, q + 30)

    def _boat(self, f, M, sh, t, yw, flash, idx):
        """Kıyı katmanında bağlı tekne (satır ölçeği dışı: s doğrudan ölçek)."""
        kind = sh["kind"]
        srow = sh["s"]
        head = 1 if sh["heading"] >= 0 else -1
        ph = idx * 1.7
        rock = sh["rock"]
        heave = _wave_h(t, ph, 2.0 + 5 * rock, 0.8) * srow
        roll = (0.015 + 0.06 * rock) * math.sin(0.9 * t + ph) * head
        ks = round(max(0.25, min(2.0, srow * 1.7)) * 8) / 8.0
        lamp = M["lamp"] or self.mood in ("storm", "dusk", "night")
        img, ox, oy, k = SW.ship_sprite(kind, ks, M["hull"], M["rim"], M["sail"], M["sail_l"], M["sail_d"], M["gold"], "", bool(lamp), M["lamp_col"], sh["sails"], 0.0, M["light_dir"], sh["flag"], 1)
        f.c.save()
        f.c.translate(sh["x"] * W, yw + heave)
        f.c.rotate(math.degrees(roll))
        f.c.scale(srow * head / k, srow / k)
        f.c.drawImage(img, -ox, -oy, LINMIP, skia.Paint())
        if flash > 0.05:
            pf = skia.Paint()
            pf.setAlphaf(clamp(flash * 0.3))
            pf.setBlendMode(PLUS)
            f.c.drawImage(img, -ox, -oy, LINMIP, pf)
        f.c.restore()
        if lamp and kind == "fishing":
            PW.glow(f, sh["x"] * W + head * 104 * srow, yw + heave - 56 * srow, 38 * srow * 2.2, M["lamp_col"], 0.75 * (0.85 + 0.15 * math.sin(6 * t + idx)))

    def _overlay(self, f, t, e):
        """Ekran uzayı: yağmur, şimşek aydınlığı, barut buğusu, vinyet ışıltısı."""
        M, mood = self.M, self.mood
        c = f.c
        c.save()
        c.resetMatrix()
        if self.rain > 0.02:
            r = self.rain
            ang = -0.30 if mood == "storm" else -0.08
            PW.rain_lines(f, t, n=int(70 + 150 * r), seed=8, angle=ang, length=20, alpha=0.20 * r + 0.06, color=M["foam"], speed=1100, sw=1.1, rect=(0, 0, W, H))
            PW.rain_lines(f, t, n=int(50 + 120 * r), seed=18, angle=ang, length=34, alpha=0.26 * r + 0.06, color=M["foam"], speed=1500, sw=1.4, rect=(0, 0, W, H))
            PW.rain_lines(f, t, n=int(24 + 70 * r), seed=28, angle=ang, length=60, alpha=0.30 * r + 0.05, color=M["foam"], speed=1950, sw=2.0, rect=(0, 0, W, H))
        if e > 0.02:
            p_ = skia.Paint()
            p_.setBlendMode(PLUS)
            p_.setColor(C("#8CA0D0", int(255 * clamp(e * 0.20))))
            c.drawRect(skia.Rect.MakeWH(W, H), p_)
        c.restore()
