"""Sahne ailesi: SAVAŞ ALANI (`field`) — ova / bataklık / nehir / tepe; hava: açık, sis, yağmur, şafak, alacakaranlık, kar.
Ordular figür-lab siluetleriyle (pikeman, landsknecht, arquebusier, halberdier, peasant, cavalry_charge(_b), sipahi(_b), janissary…) çizilir.
Kayıt: @SL.sc("field"). Ayrıntılı API: SAHNE_KATALOGU_deniz_savas.md

Mimari (sea ile aynı): tek taban katman (gök + ufuk + uzak sırt + uzak kale) + dyn içinde kırpılmış zemin bantları (kendi paralaksıyla),
nehir bandı, ordular (figür sprite'ları), sancaklar, duman, sis, yağmur/kar.
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
from props_war import LIN, PLUS, RS, darken, lighten
from sk import C, H, W, clamp, lerp, mix, smooth
from stage import MARGIN

HZ = 500
EDGE_Y = (562, 702, 846, 1004)           # b0 uzak · b1 orta · b2 yakın · b3 ön plan zemin kenarı
BAND_D = (0.30, 0.52, 0.78, 1.06)
FG_D = 1.30
RIVER_Y, RIVER_D = 628, 0.41
BASE_D = 0.08
ROW_BAND = {2: 0, 1: 1, 0: 2}
ROW_S = {0: 1.0, 1: 0.66, 2: 0.43}
INF_H = 250.0                            # row 0 piyade boyu (px)
CAV_H = 262.0                            # row 0 atlı toplam boy (px)

WEATHER = dict(
    clear=dict(sky=[("#2A3C52", 0.0), ("#6F8392", 0.45), ("#D6C79C", 0.85), ("#F2DBA6", 1.0)], haze="#E1CF9E", sun=(0.26, 408, 44, "#FFF2D0", "#FFC983"), cloud_shadow="#56626E", cloud_light="#F6E0B2", cover=0.38,
               tint="#B49A5A", tint_k=0.22, rim="#E8A862", fog_a=0.20, bright=1.0, ridge="#8A8E72", sunlight=1.0),
    fog=dict(sky=[("#6F7678", 0.0), ("#9EA2A0", 0.5), ("#C6C6BA", 1.0)], haze="#C8C8BC", sun=(0.30, 470, 40, "#FFFFFF", "#E8E4D0"), cloud_shadow="#8C9296", cloud_light="#D8D8CC", cover=0.5,
             tint="#9AA08A", tint_k=0.35, rim="#CFC39E", fog_a=0.62, bright=1.0, ridge="#AEB1A2", sunlight=0.4),
    rain=dict(sky=[("#12181C", 0.0), ("#2A353A", 0.45), ("#566265", 1.0)], haze="#6C7878", sun=None, cloud_shadow="#0F1519", cloud_light="#6E8084", cover=0.74,
              tint="#4A5A48", tint_k=0.45, rim="#9AA9A6", fog_a=0.34, bright=0.9, ridge="#46544F", sunlight=0.2),
    dawn=dict(sky=[("#1D3047", 0.0), ("#4E5B7D", 0.28), ("#B0728C", 0.62), ("#F2A46C", 0.88), ("#FFD9A0", 1.0)], haze="#F2B98A", sun=(0.30, 494, 56, "#FFF0C8", "#FFA866"), cloud_shadow="#4A4468", cloud_light="#FFC890", cover=0.5,
              tint="#9A7A5E", tint_k=0.30, rim="#FFB26A", fog_a=0.32, bright=1.0, ridge="#8A6E78", sunlight=0.9),
    dusk=dict(sky=[("#171B36", 0.0), ("#4B3359", 0.30), ("#A24A55", 0.62), ("#E2733C", 0.86), ("#FFB257", 1.0)], haze="#EE9150", sun=(0.70, 498, 64, "#FFE2A0", "#FF8E3C"), cloud_shadow="#3A2542", cloud_light="#FF9A55", cover=0.52,
              tint="#7A5440", tint_k=0.32, rim="#FF9A4E", fog_a=0.24, bright=0.95, ridge="#6A4A50", sunlight=0.9),
    snow=dict(sky=[("#566069", 0.0), ("#98A1A7", 0.5), ("#CDD1D0", 1.0)], haze="#C9CFD0", sun=None, cloud_shadow="#838B93", cloud_light="#E0E4E4", cover=0.62,
              tint="#C8D0D6", tint_k=0.75, rim="#D8E0E8", fog_a=0.40, bright=1.0, ridge="#B4BCC2", sunlight=0.3),
)

GROUND = dict(
    plain=dict(far="#7C7642", near="#363E1E", amp=(24, 17, 11, 7), tree="poplar"),
    marsh=dict(far="#586A52", near="#1F2A1D", amp=(8, 6, 4, 3), tree="dead"),
    river=dict(far="#6E7844", near="#2E391F", amp=(18, 10, 7, 5), tree="poplar"),
    hills=dict(far="#606E3E", near="#27311A", amp=(62, 46, 26, 14), tree="pine"),
)


def _weather(name):
    return WEATHER.get(name, WEATHER["clear"])


def _ground(name):
    return GROUND.get(name, GROUND["plain"])


def _cols(ground, weather, k):
    """Bant k zemin rengi (uzak→yakın), hava rengiyle karışmış."""
    G, Wx = _ground(ground), _weather(weather)
    u = (0.0, 0.34, 0.68, 1.0)[k]
    c = mix(G["far"], G["near"], u ** 0.8)
    c = mix(c, Wx["tint"], Wx["tint_k"] * (0.55 + 0.45 * u))
    c = mix(c, Wx["haze"], (1 - u) * 0.34 * (1.6 if weather == "fog" else 1.0))
    if weather == "rain":
        c = mix(c, "#0A100E", 0.18)
    return c


@lru_cache(maxsize=32)
def _edge_params(ground, k):
    rs = RS(900 + k * 17 + len(ground))
    amp = _ground(ground)["amp"][k]
    comps = []
    for fq, a in ((0.0021, 1.0), (0.0057, 0.55), (0.0139, 0.22)):
        comps.append((amp * a * (0.7 + 0.6 * rs.rand()), fq * (0.8 + 0.4 * rs.rand()), rs.rand() * 6.283))
    return tuple(comps)


def edge_y(ground, k, x):
    """Bant k zemin üst kenarının x'teki y'si (katman koordinatı)."""
    y = EDGE_Y[k]
    for a, fq, ph in _edge_params(ground, k):
        y += a * math.sin(x * fq + ph)
    return y


# ───────────────────────────── kamera yardımcıları ─────────────────────────────
def safe_cam(x, y, z, dmax=1.30):
    """Kamerayı katman kenarlarında boşluk görünmeyecek aralığa sıkıştırır."""
    z = max(1.0, z)
    s = 1 + (z - 1) * dmax
    lx = (1180 - W / 2 / s) / dmax
    ly = (760 - H / 2 / s) / dmax
    return (W / 2 + max(-lx, min(lx, x - W / 2)), H / 2 + max(-ly, min(ly, y - H / 2)), z)


def cam_on(row=0, x=0.5, zoom=1.4, rise=0.4):
    """Verilen sıradaki (0 yakın..2 uzak) birliğin (x: 0..1) ekran ortasına gelmesi için güvenli kamera (x, y, zoom)."""
    k = ROW_BAND[int(row)]
    d = BAND_D[k]
    X = x * W
    Yc = EDGE_Y[k] + 34 * ROW_S[int(row)] - (INF_H * ROW_S[int(row)]) * (0.35 + 0.5 * rise)
    cx = W / 2 + (X - W / 2) / d
    cy = H / 2 + (Yc - H / 2) / d
    return safe_cam(cx, cy, zoom)


# ───────────────────────────── gök / uzak sırt / uzak kale ─────────────────────────────
@lru_cache(maxsize=24)
def _cloud_f(weather, which):
    Wx = _weather(weather)
    w2, h2 = (W + 2 * MARGIN) // 2, (HZ + MARGIN + 60) // 2
    yy = np.linspace(0, 1, h2, dtype=np.float32)
    st = weather in ("rain",)
    if which == "mid":
        vf = np.clip(np.minimum(yy * 5, (1 - yy) * 3.0), 0, 1)
        a = PW.cloud_rgba(w2, h2, 33, cover=Wx["cover"], soft=0.36, scale=46, octaves=6, shadow=Wx["cloud_shadow"], light=Wx["cloud_light"], rim=None, vfade=vf, stretch=2.1,
                          periodic=True, gamma=1.15, thick_dark=0.5 if st else 0.2, sigma=5.0, reach=16, gain=1.35, light_dir=(0.55, -0.8))
        return PW.img_from_rgba(a, mip=False)
    vf = np.clip(np.minimum((yy - 0.45) * 4, (1.0 - yy) * 5), 0, 1)
    a = PW.cloud_rgba(w2, h2, 35, cover=Wx["cover"] * 0.85, soft=0.34, scale=30, octaves=5, shadow=mix(Wx["cloud_shadow"], Wx["haze"], 0.25), light=mix(Wx["cloud_light"], Wx["haze"], 0.35), rim=None,
                      vfade=vf, stretch=3.4, periodic=True, gamma=1.1, gain=1.3, sigma=2.5, reach=8, light_dir=(0.5, -0.7))
    r0 = int(h2 * 0.44)
    return PW.img_from_rgba(np.ascontiguousarray(a[r0:]), mip=False)


def _draw_img2(f, img, x, y, alpha=1.0):
    p = skia.Paint()
    if alpha < 1:
        p.setAlphaf(alpha)
    f.c.save()
    f.c.translate(x, y)
    f.c.scale(2.0, 2.0)
    f.c.drawImage(img, 0, 0, LIN, p)
    f.c.restore()


def _ridge(f, y, amp, col, seed, step=40, wl=0.0035):
    rs = RS(seed)
    ph = rs.rand() * 6.28
    pts = [(xx, y + math.sin(xx * wl + ph) * amp + math.sin(xx * wl * 2.7 + ph * 2) * amp * 0.4 + math.sin(xx * wl * 6.1 + ph) * amp * 0.12) for xx in range(-MARGIN, W + MARGIN + step, step)]
    pts += [(W + MARGIN, HZ + 140), (-MARGIN, HZ + 140)]
    f.path(sk.poly_path(pts, True), color=col)
    return pts


def _castle_pavia(f, x, y, col, lit):
    """Pavia: Visconti kalesi — dört köşe kulesi, uzun cephe, merkez donjon, park surunun devamı."""
    w = 520
    f.rect(x - w / 2, y - 64, w, 64, color=col)
    for q in range(26):
        f.rect(x - w / 2 + q * 20, y - 74, 11, 12, color=col)
    for tx in (-w / 2 + 6, w / 2 - 6):
        f.rect(x + tx - 24, y - 112, 48, 112, color=col)
        for q in range(4):
            f.rect(x + tx - 24 + q * 13, y - 124, 8, 14, color=col)
    f.rect(x - 38, y - 140, 76, 90, color=col)
    f.poly([(x - 44, y - 140), (x, y - 190), (x + 44, y - 140)], color=col)
    for q in range(5):
        f.rect(x - 150 + q * 60, y - 108, 26, 44, color=col)
        f.poly([(x - 154 + q * 60, y - 108), (x - 137 + q * 60, y - 132), (x - 120 + q * 60, y - 108)], color=col)
    f.rect(x + w / 2, y - 34, 380, 34, color=col)
    f.rect(x - w / 2 - 380, y - 34, 380, 34, color=col)
    for k in range(10):
        tx = x - w / 2 - 340 + k * 66 + (k % 3) * 14
        f.oval(tx, y - 58 - (k % 4) * 6, 10, 38 + (k % 3) * 8, color=col)
    if lit:
        for q in range(6):
            f.rect(x - 160 + q * 64, y - 86, 5, 9, color="#FFC770")


def _castle_toledo(f, x, y, col, lit):
    """Toledo: tepe üstünde yığılmış şehir, Alcázar (dört köşe kuleli büyük blok), katedral çan kulesi."""
    hill = [(x - 420, y + 6), (x - 330, y - 34), (x - 220, y - 92), (x - 100, y - 142), (x + 20, y - 168), (x + 150, y - 148), (x + 260, y - 98), (x + 360, y - 40), (x + 440, y + 6)]
    f.path(sk.smooth_path(hill + [(x + 440, y + 40), (x - 420, y + 40)], True, 0.4), color=col)
    rs = RS(42)
    for i in range(46):
        hx = x - 360 + rs.rand() * 720
        top = float(np.interp(hx, [p[0] for p in hill], [p[1] for p in hill]))
        w = 18 + rs.rand() * 26
        h = 16 + rs.rand() * 26
        f.rect(hx - w / 2, top + 4 - h * 0.2, w, h, color=col)
        if rs.rand() > 0.5:
            f.poly([(hx - w / 2 - 2, top + 4 - h * 0.2), (hx, top - 10 - h * 0.2), (hx + w / 2 + 2, top + 4 - h * 0.2)], color=col)
    ax, ay = x + 40, y - 172
    f.rect(ax - 62, ay - 54, 124, 58, color=col)
    for tx in (-62, 62):
        f.rect(ax + tx - 16, ay - 84, 32, 90, color=col)
        f.poly([(ax + tx - 20, ay - 84), (ax + tx, ay - 112), (ax + tx + 20, ay - 84)], color=col)
    f.rect(ax - 40, ay - 74, 80, 24, color=col)
    f.rect(x - 150, y - 160, 22, 120, color=col)
    f.poly([(x - 154, y - 160), (x - 139, y - 212), (x - 124, y - 160)], color=col)
    f.rect(x - 4, y - 218, 8, 20, color=col)
    if lit:
        for q in range(7):
            f.rect(x - 220 + q * 60 + (q % 2) * 12, y - 88 - (q % 3) * 22, 4, 8, color="#FFC770")


def bake_base(f, ground, weather, castle):
    Wx = _weather(weather)
    f.rect(-MARGIN, -MARGIN, W + 2 * MARGIN, HZ + MARGIN + 100, shader=f.lin(0, -MARGIN, 0, HZ, [(c, u) for c, u in Wx["sky"]]))
    sun = Wx["sun"]
    if sun:
        sx, sy, sr, core, gc = sun
        sx *= W
        PW.glow_add(f, sx, sy, 720, gc, 0.34 if weather != "fog" else 0.5, 150, 46, 0.30)
        PW.glow_add(f, sx, sy, 280, gc, 0.45, 230, 90, 0.38)
        f.circle(sx, sy, sr, shader=f.rad(sx, sy, sr, [("#FFFFFF", 0.0), (core, 0.7), (core, 1.0)]), alpha=0.9 if weather != "fog" else 0.5)
        if weather in ("clear", "dawn", "dusk"):
            ST.god_rays(f, (sx, sy), -math.pi / 2, 2.6, 1500, n=9, alpha=0.05, color=mix(gc, "#FFFFFF", 0.3), seed=4, blur=26)
    _draw_img2(f, _cloud_f(weather, "mid"), -MARGIN, -MARGIN + 30, 0.95)
    ridge_c = Wx["ridge"]
    amp = 38 if ground == "hills" else 16
    _ridge(f, HZ - 8, amp, mix(ridge_c, Wx["haze"], 0.55), 3, wl=0.0030)
    _ridge(f, HZ + 6, amp * 0.7, mix(ridge_c, Wx["haze"], 0.35), 9, wl=0.0045)
    lit = weather in ("rain", "dusk", "dawn", "fog", "snow")
    if castle:
        cc = mix(mix(ridge_c, "#000000", 0.20), Wx["haze"], 0.40)
        cx = W * 0.70
        if castle == "pavia":
            _castle_pavia(f, cx, HZ + 14, cc, lit)
        elif castle == "toledo":
            _castle_toledo(f, cx, HZ + 20, cc, lit)
    f.rect(-MARGIN, HZ - 150, W + 2 * MARGIN, 230, shader=f.lin(0, HZ - 150, 0, HZ + 70, [(Wx["haze"], 0.0, 0), (Wx["haze"], 0.7, int(255 * (0.55 if weather == "fog" else 0.35))), (Wx["haze"], 1.0, int(255 * (0.7 if weather == "fog" else 0.45)))]))
    f.rect(-MARGIN, HZ + 40, W + 2 * MARGIN, 180, color=_cols(ground, weather, 0))


# ───────────────────────────── zemin bantları ─────────────────────────────
def _tree(f, kind, x, y, h, col, rs):
    if kind == "poplar":
        f.oval(x, y - h * 0.5, h * 0.11, h * 0.5, color=col)
        f.rect(x - 1.5, y - 6, 3, 8, color=col)
    elif kind == "pine":
        for q in range(5):
            w = h * 0.2 * (1 - q * 0.17)
            f.poly([(x - w, y - h * q * 0.19), (x, y - h * (q * 0.19 + 0.38)), (x + w, y - h * q * 0.19)], color=col)
        f.rect(x - 2, y - 4, 4, 8, color=col)
    elif kind == "dead":
        f.path(sk.smooth_path([(x, y), (x + rs.randn() * 3, y - h * 0.45), (x + rs.randn() * 4, y - h)], False, 0.5), style="stroke", sw=max(2.0, h * 0.04), color=col)
        for k in range(4):
            by = y - h * (0.35 + 0.17 * k)
            f.line(x, by, x + (rs.rand() - 0.5) * h * 0.5, by - h * 0.14, color=col, sw=max(1.2, h * 0.02))
    else:  # oak
        f.circle(x, y - h * 0.55, h * 0.36, color=col)
        f.circle(x - h * 0.22, y - h * 0.45, h * 0.26, color=col)
        f.circle(x + h * 0.22, y - h * 0.45, h * 0.26, color=col)
        f.rect(x - 3, y - h * 0.4, 6, h * 0.42, color=col)


def bake_band(f, ground, weather, k, river):
    Wx, G = _weather(weather), _ground(ground)
    col = _cols(ground, weather, k)
    far = _cols(ground, weather, min(3, k + 1))
    rs = RS(1200 + k * 31 + len(ground) * 7)
    xs = list(range(-MARGIN, W + MARGIN + 41, 40))
    edge = [(x, edge_y(ground, k, x)) for x in xs]
    path = sk.smooth_path(edge + [(W + MARGIN, H + MARGIN + 80), (-MARGIN, H + MARGIN + 80)], True, 0.35)
    y_top = EDGE_Y[k] - G["amp"][k] * 2.0
    f.path(path, shader=f.lin(0, y_top, 0, y_top + (EDGE_Y[min(3, k + 1)] - EDGE_Y[k]) + 120, [(mix(col, Wx["haze"], 0.10 if k < 3 else 0.0), 0.0), (mix(col, far, 0.7), 1.0)]))
    f.c.save()
    f.c.clipPath(path, skia.ClipOp.kIntersect, True)
    tex = PW.streak_rgba(W + 2 * MARGIN, 260, 60 + k, col="#000000", alpha=0.22, scale_x=380 - 40 * k, scale_y=8 + 4 * k, thr=0.55)
    f.c.drawImage(PW.img_from_rgba(tex), -MARGIN, EDGE_Y[k] - 20, LIN, skia.Paint())
    tex2 = PW.streak_rgba(W + 2 * MARGIN, 260, 80 + k, col=lighten(col, 0.5), alpha=0.16, scale_x=300 - 30 * k, scale_y=6 + 3 * k, thr=0.6)
    f.c.drawImage(PW.img_from_rgba(tex2), -MARGIN, EDGE_Y[k] - 10, LIN, skia.Paint())
    if weather == "snow":
        f.rect(-MARGIN, EDGE_Y[k] - 60, W + 2 * MARGIN, 80 + 26 * k, color="#E4EAF0", alpha=0.55)
    if ground == "marsh" and k >= 1:
        for q in range(9 + 4 * k):
            px = rs.rand() * (W + 2 * MARGIN) - MARGIN
            py = EDGE_Y[k] + 18 + rs.rand() * (60 + 40 * k)
            rx = 40 + rs.rand() * (60 + 30 * k)
            f.oval(px, py, rx, rx * 0.11, color=mix(Wx["haze"], "#202A2C", 0.45), alpha=0.7)
            f.oval(px, py - 1, rx * 0.8, rx * 0.04, color="#FFFFFF", alpha=0.18)
    if weather == "rain" and k >= 1:
        for q in range(14 + 6 * k):
            px = rs.rand() * (W + 2 * MARGIN) - MARGIN
            py = EDGE_Y[k] + 24 + rs.rand() * (60 + 40 * k)
            rx = 24 + rs.rand() * (50 + 20 * k)
            f.oval(px, py, rx, rx * 0.10, color=mix(Wx["haze"], "#1A2224", 0.4), alpha=0.55)
    f.c.restore()
    f.path(sk.smooth_path(edge, False, 0.35), style="stroke", sw=2.0 + k, color=Wx["rim"], alpha=0.30 * Wx["sunlight"] + 0.06)
    tint = mix(col, "#000000", 0.35)
    if river and k == 1:         # yakın kıyı kamışları + ıslak toprak şeridi
        f.path(sk.smooth_path([(x, y + 3) for x, y in edge], False, 0.35), style="stroke", sw=7, color=mix("#0A100C", Wx["haze"], 0.15), alpha=0.7)
        for q in range(110):
            x = rs.rand() * (W + 2 * MARGIN) - MARGIN
            y = edge_y(ground, 1, x) + 2
            hh = 12 + rs.rand() * 34
            f.path(sk.smooth_path([(x, y), (x + (rs.rand() - 0.5) * 8, y - hh * 0.55), (x + (rs.rand() - 0.5) * 14, y - hh)], False, 0.5), style="stroke", sw=1.4, color=mix(tint, "#000000", 0.3))
    for q in range(int(150 / (1 + 0.4 * k))):
        x = rs.rand() * (W + 2 * MARGIN) - MARGIN
        y = edge_y(ground, k, x) + 1 + rs.rand() * 6
        hh = (4 + rs.rand() * 10) * (0.7 + 0.4 * k)
        f.line(x, y, x + (rs.rand() - 0.5) * 5, y - hh, color=tint, sw=1.0 + 0.4 * k, alpha=0.7)
    tk = G["tree"]
    if k == 0:
        n = 36 if ground == "hills" else 12
        for q in range(n):
            x = rs.rand() * (W + 2 * MARGIN) - MARGIN
            y = edge_y(ground, 0, x) + 3
            hh = (46 + rs.rand() * 40) * (1.0 if ground == "hills" else 0.8)
            _tree(f, tk, x, y, hh, mix(tint, Wx["haze"], 0.12), rs)
    elif k == 1:
        n = 14 if ground == "hills" else 4
        for q in range(n):
            x = rs.rand() * (W + 2 * MARGIN) - MARGIN
            y = edge_y(ground, 1, x) + 4
            hh = 72 + rs.rand() * 52
            _tree(f, "oak" if tk == "poplar" else tk, x, y, hh, mix(tint, Wx["haze"], 0.08), rs)
    # çit/çalılık şeridi (uzak bantta ufuk çizgisini kırar)
    if k in (0, 1) and ground != "hills":
        hedge = []
        for x in range(-MARGIN, W + MARGIN + 31, 30):
            hedge.append((x, edge_y(ground, k, x) - 3 - (5 + 9 * abs(math.sin(x * 0.013 + k)) * (1.4 - 0.4 * k)) * (0.7 + 0.6 * rs.rand())))
        hp = sk.smooth_path(hedge + [(W + MARGIN, edge_y(ground, k, W + MARGIN) + 6), (-MARGIN, edge_y(ground, k, -MARGIN) + 6)], True, 0.5)
        f.path(hp, color=mix(tint, Wx["haze"], 0.10 + 0.05 * k))
    # yakın zemin: tekerlek izleri, saplanmış mızraklar, kalkanlar
    if k in (2, 3):
        for q in range(3):
            xs0 = rs.rand() * (W + 2 * MARGIN) - MARGIN
            ys0 = EDGE_Y[k] + 10
            xs1 = xs0 + (rs.rand() - 0.5) * 900
            wd = 7 + 5 * k
            f.poly([(xs0 - wd * 0.2, ys0), (xs0 + wd * 0.2, ys0), (xs1 + wd, ys0 + 190), (xs1 - wd, ys0 + 190)], color=mix(tint, "#000000", 0.35), alpha=0.28)
        for q in range(7 if k == 2 else 4):
            x = rs.rand() * (W + 2 * MARGIN) - MARGIN
            y = edge_y(ground, k, x) + 26 + rs.rand() * (50 if k == 2 else 40)
            sc = 0.9 + 0.5 * k
            kindp = rs.rand()
            if kindp < 0.45:     # saplanmış mızrak/ok
                ang = (rs.rand() - 0.5) * 0.7
                L = 70 * sc * (0.8 + 0.5 * rs.rand())
                f.line(x, y, x + math.sin(ang) * L, y - math.cos(ang) * L, color=mix("#0A0705", Wx["haze"], 0.08), sw=2.2 * sc)
                f.poly([(x + math.sin(ang) * L - 3 * sc, y - math.cos(ang) * L + 2), (x + math.sin(ang) * (L + 14 * sc), y - math.cos(ang) * (L + 14 * sc)), (x + math.sin(ang) * L + 3 * sc, y - math.cos(ang) * L + 2)], color="#0A0705")
            elif kindp < 0.75:   # yere düşmüş kalkan
                f.oval(x, y, 30 * sc, 7 * sc, color=mix("#0A0705", Wx["haze"], 0.1))
                f.oval(x, y - 2 * sc, 8 * sc, 2.4 * sc, color=Wx["rim"], alpha=0.45)
            else:                # çalı/taş
                f.oval(x, y, (16 + 14 * rs.rand()) * sc, (6 + 4 * rs.rand()) * sc, color=mix("#0A0705", Wx["haze"], 0.06))
    fa = Wx["fog_a"] * (1.0 - 0.28 * k) * (0.9 if k > 0 else 1.0)
    ycr = EDGE_Y[k]
    f.rect(-MARGIN, ycr - 150, W + 2 * MARGIN, 150 + 90, shader=f.lin(0, ycr - 150, 0, ycr + 90, [(Wx["haze"], 0.0, 0), (Wx["haze"], 0.62, int(255 * fa * 0.70)), (Wx["haze"], 1.0, 0)]))


@lru_cache(maxsize=40)
def band_image(ground, weather, k, river):
    y0 = int(EDGE_Y[k] - _ground(ground)["amp"][k] * 2.4 - 170)
    h = int(H + MARGIN + 90 - y0)

    def fn(f):
        bake_band(f, ground, weather, k, river)
    img = PW.bake_sprite(fn, W + 2 * MARGIN, h, MARGIN, -y0, mip=False)
    return img, -MARGIN, y0


def bake_river(f, ground, weather):
    Wx = _weather(weather)
    c_top = mix(Wx["haze"], "#36586C", 0.60)
    c_bot = mix(Wx["haze"], "#0E1E28", 0.84)
    y0 = RIVER_Y - 6
    f.rect(-MARGIN, y0, W + 2 * MARGIN, H + MARGIN + 80 - y0, shader=f.lin(0, y0, 0, y0 + 190, [(c_top, 0.0), (c_bot, 1.0)]))
    sun = Wx["sun"]
    if sun:
        PW.glow_add(f, sun[0] * W, RIVER_Y + 40, 260, sun[4], 0.25, 200, 70, 0.3)
    f.rect(-MARGIN, y0, W + 2 * MARGIN, 3, color=Wx["rim"], alpha=0.25)
    # uzak kıyı: ıslak toprak çizgisi + kamışlar
    rs = RS(555)
    f.rect(-MARGIN, y0 - 2, W + 2 * MARGIN, 7, color=mix("#0A100C", Wx["haze"], 0.18), alpha=0.8)
    tint = mix(_cols(ground, weather, 0), "#000000", 0.45)
    for q in range(120):
        x = rs.rand() * (W + 2 * MARGIN) - MARGIN
        hh = 8 + rs.rand() * 20
        f.line(x, y0 + 3, x + (rs.rand() - 0.5) * 6, y0 + 3 - hh, color=tint, sw=1.2)
    # parlama çizgileri (gökyüzü yansıması)
    for q in range(70):
        x = rs.rand() * (W + 2 * MARGIN) - MARGIN
        y = y0 + 8 + rs.rand() * 90
        f.line(x, y, x + 20 + rs.rand() * 70, y, color=mix(Wx["haze"], "#FFFFFF", 0.4), sw=1.0 + rs.rand() * 1.2, alpha=0.12 + 0.14 * rs.rand())


@lru_cache(maxsize=12)
def river_image(ground, weather):
    y0 = RIVER_Y - 70
    h = int(H + MARGIN + 90 - y0)

    def fn(f):
        bake_river(f, ground, weather)
    img = PW.bake_sprite(fn, W + 2 * MARGIN, h, MARGIN, -y0, mip=False)
    return img, -MARGIN, y0


@lru_cache(maxsize=8)
def fg_image(ground, weather):
    """Ön plan: koyu çimen/kamış siluetleri (alt kenar), kamerada hızlı paralaks."""
    Wx = _weather(weather)
    ytop = 800
    h = int(H + MARGIN + 90 - ytop)

    def fn(f):
        rs = RS(77)
        col = "#3A424A" if weather == "snow" else mix("#0A0F08", Wx["haze"], 0.04)
        y0 = H - 24
        f.rect(-MARGIN, y0 + 30, W + 2 * MARGIN, 400, color=col)
        for q in range(190):
            x = rs.rand() * (W + 2 * MARGIN) - MARGIN
            hh = 40 + rs.rand() * 120 * (1.0 if ground != "marsh" else 1.5)
            bx = x + (rs.rand() - 0.5) * 30
            f.path(sk.smooth_path([(x, y0 + 40), (x + (bx - x) * 0.5, y0 - hh * 0.5), (bx, y0 - hh)], False, 0.5), style="stroke", sw=1.6 + rs.rand() * 2.2, color=col)
        for q in range(8):
            x = rs.rand() * (W + 2 * MARGIN) - MARGIN
            f.oval(x, y0 + 14, 40 + rs.rand() * 60, 18 + rs.rand() * 14, color=col)
    img = PW.bake_sprite(fn, W + 2 * MARGIN, h, MARGIN, -ytop, mip=False)
    return img, -MARGIN, ytop


@lru_cache(maxsize=12)
def _fog_img(weather, haze):
    w2, h2 = (W + 2 * MARGIN) // 2, 140
    yy = np.linspace(0, 1, h2, dtype=np.float32)
    vf = np.clip(np.minimum(yy * 3.5, (1 - yy) * 2.6), 0, 1)
    a = PW.cloud_rgba(w2, h2, 51, cover=0.58, soft=0.5, scale=40, octaves=5, shadow=mix(haze, "#6A7078", 0.20), light=mix(haze, "#FFFFFF", 0.25), vfade=vf, stretch=3.2, periodic=True, gamma=1.1, gain=0.8, sigma=4, reach=6)
    return PW.img_from_rgba(a, mip=False)


# ───────────────────────────── figürler / ordular ─────────────────────────────
def _have(kind):
    return (kind in ST.FIGX) or (kind in ST.FIG)


_UNITS = dict(
    pike=("pikeman", "pikeman", "landsknecht", "halberdier", "pikeman"),
    arquebus=("arquebusier", "arquebusier", "arquebusier", "halberdier"),
    peasants=("peasant", "peasant", "peasant", "crowd_a", "crowd_c"),
    mixed=("pikeman", "arquebusier", "landsknecht", "halberdier", "pikeman", "arquebusier"),
)


def _is_green(hexc):
    c = hexc.lstrip("#")
    r_, g_, b_ = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return g_ > r_ * 1.05 and g_ >= b_


def _army_kind_pool(army):
    kind = army.get("kind", "pike")
    unit = army.get("unit")
    if unit:
        u = unit if isinstance(unit, (list, tuple)) else (unit,)
        return tuple(x if _have(x) else "pikeman" for x in u)
    if kind == "cavalry":
        if _is_green(army.get("side", "#8E1F26")) and _have("sipahi") and _have("sipahi_b"):
            return ("sipahi",)
        return ("cavalry_charge",) if _have("cavalry_charge") else ("horse_rider",)
    pool = _UNITS.get(kind, _UNITS["pike"])
    if army.get("side") and _is_green(army["side"]) and kind in ("pike", "mixed") and _have("janissary"):
        pool = ("janissary", "janissary", "janissary", "arquebusier") if kind == "mixed" else ("janissary",)
    return tuple(x if _have(x) else "pikeman" for x in pool)


def _gait_b(kind):
    return {"cavalry_charge": "cavalry_charge_b", "sipahi": "sipahi_b"}.get(kind)


def draw_army(f, M, ground, weather, army, ai, t, vis, fx_list):
    """Bir ordu: figür sprite'ları (arkadan öne), sancak, atış/duman. army: side, kind, x, row, n, dir, charge, unit, s, spread, banner, fire, ford."""
    kind = army.get("kind", "pike")
    row = int(clamp(army.get("row", 1), 0, 2))
    n = int(army.get("n", 24))
    dirn = 1 if army.get("dir", 1) >= 0 else -1
    charge = clamp(army.get("charge", 0.0))
    srow = ROW_S[row] * army.get("s", 1.0)
    side = army.get("side", "#8E1F26")
    ford = bool(army.get("ford", False))
    k = ROW_BAND[row]
    cav = (kind == "cavalry")
    h0 = (CAV_H if cav else INF_H) * srow
    pool = _army_kind_pool(army)
    rs = RS(ai * 7919 + n * 13 + row * 101 + int(army.get("x", 0.5) * 1000))
    ranks = 1 if (cav and n <= 9) else (2 if cav else int(clamp(round(math.sqrt(n / 2.2)), 2, 6)))
    cols = max(1, int(math.ceil(n / ranks)))
    spacing = (1.15 if cav else 0.36) * h0 * army.get("spread", 1.0)
    dy_rank = (0.34 if cav else 0.16) * h0
    speed = (170.0 if cav else (34.0 if kind != "peasants" else 48.0)) * charge * ROW_S[row]
    tint_k = {0: 0.0, 1: 0.14, 2: 0.30}[row] * (1.4 if weather == "fog" else 1.0)
    hz = M["haze"]
    col = mix(mix("#0C0705", side, 0.08), hz, tint_k)
    rim = mix(M["rim"], hz, tint_k * 0.6)
    x0c = army.get("x", 0.5) * W
    jit = rs.rand(n, 6)
    out = []
    for i in range(n):
        rk = min(i // cols, ranks - 1)
        cl = i % cols
        off = (cl - (cols - 1) / 2.0 + (jit[i, 0] - 0.5) * 0.7) * spacing + (rk % 2) * spacing * 0.35
        out.append((rk, x0c + off + dirn * speed * t, i, jit[i]))
    out.sort(key=lambda q: q[0], reverse=True)
    bannered = False
    fire = army.get("fire", 1.0 if kind == "arquebus" else 0.0)
    for rk, x, i, jv in out:
        if vis is not None and (x < vis[0] - 260 * srow - 100 or x > vis[2] + 260 * srow + 100):
            continue
        if ford:
            y_f = RIVER_Y + 44 - rk * dy_rank * 0.6 + 6 * jv[1]
        else:
            y_f = edge_y(ground, k, x) + 34 * srow - rk * dy_rank * 0.9 + (jv[1] - 0.5) * 6 * srow
        hh = float(int(h0 * (0.95 + 0.10 * jv[2]) * (0.97 ** rk) / 2) * 2)
        unit = pool[int(jv[3] * len(pool)) % len(pool)]
        ph = jv[4] * 6.283
        if cav:
            gs = 6.2 + 1.2 * jv[5]
            cf = 0.5 + 0.5 * charge
            gait = 0.5 + 0.5 * math.sin(t * gs * cf + ph)
            uk = _gait_b(unit)
            if uk and _have(uk) and gait > 0.5 and charge > 0.05:
                unit = uk
            bob = -math.sin(t * gs * cf + ph) * 0.012 * hh * (0.3 + 0.7 * charge)
        else:
            step = 3.2 + jv[5] * 0.8
            bob = -abs(math.sin(t * step + ph)) * 0.010 * hh * (0.25 + 0.75 * charge) - math.sin(t * 0.9 + ph) * 0.002 * hh
        f.c.save()
        wy = y_f - 0.20 * hh
        if ford:
            f.c.clipRect(skia.Rect.MakeLTRB(-4000, -4000, 6000, wy + math.sin(t * 2.3 + ph) * 2.0))
        ST.figure(f, unit, x, y_f + bob, hh, col=col, rim=rim, face=dirn)
        f.c.restore()
        if ford:
            g = PW.glow_sprite(64, M["haze"], 200, 90, 0.5)
            pf = skia.Paint()
            pf.setAlphaf(0.55)
            f.c.save()
            f.c.translate(x, wy + 2)
            f.c.scale(hh * 0.55 / 64.0, hh * 0.105 / 64.0)
            f.c.drawImage(g, -64, -64, LIN, pf)
            f.c.restore()
            for q in range(3):
                u = (t * 1.1 + jv[4] + q / 3.0) % 1.0
                f.c.drawCircle(x + (q - 1) * hh * 0.28 + dirn * u * 6, wy - u * hh * 0.22, 1.6 + 1.2 * (1 - u), skia.Paint(AntiAlias=True, Color=C(M["haze"], int(255 * (1 - u) * 0.8))))
        torch = army.get("torch", 0.0)
        if torch > 0 and jv[5] < torch and not cav:
            tx = x + dirn * 0.27 * hh
            ty = y_f + bob - 0.98 * hh
            f.line(tx, ty + 0.30 * hh, tx, ty - 0.05 * hh, color="#0C0705", sw=max(1.6, hh * 0.014))
            PW.flame(f, tx, ty - 0.03 * hh, hh / 330.0, t, seed=i, glow_a=0.9)
        if army.get("banner", True) and not bannered and M.get("_banners", True) and rk == 0 and abs(x - x0c) < spacing * 1.6 and not cav:
            bannered = True
            pole_h = hh * 2.15
            bx = x + dirn * hh * 0.10
            f.line(bx, y_f + bob, bx, y_f + bob - pole_h, color="#0C0705", sw=max(2.0, hh * 0.016))
            emb = "crescent" if _is_green(side) else ("saltire" if side.lower() in ("#8e1f26", "#9a2430", "#7b1e2b", "#a33a2e") else "cross")
            PW.flag_cloth(f, bx, y_f + bob - pole_h, hh * 0.78, hh * 0.46, side, t, emblem=emb, trim="#C9962B", wind=-dirn, seed=ai, speed=3.6, cut="swallow", emb="#F0E2B8")
        if fire > 0 and unit == "arquebusier":
            period = 4.6 / (0.3 + fire)
            tt = (t + jv[4] * period * 3.0) % period
            mx = x + dirn * hh * 0.62
            my = y_f + bob - hh * 1.17
            if tt < 0.16:
                e = 1 - tt / 0.16
                PW.glow(f, mx, my, hh * 0.32 * (0.5 + e), "#FFC66B", e, 255, 140, 0.4)
                PW.glow(f, mx, my, hh * 0.12 * (0.5 + e), "#FFF1C4", e)
            if tt < 5.0:
                fx_list.append((mx, my, tt, hh, jv[3], dirn))


def draw_fx_smoke(f, M, fx_list, wind):
    """Atış dumanı: her atıştan büyüyen/dağılan tek kabarcık (≤ 26)."""
    col = "#9C9288" if M["bright"] > 0.85 else "#5C5C60"
    for (mx, my, age, hh, jv, dirn) in fx_list[:26]:
        u = age / 5.0
        r = hh * (0.10 + 0.34 * u ** 0.6)
        a = 0.5 * (1 - u) ** 1.2 * min(1.0, age * 3)
        PW.puff(f, mx + dirn * hh * 0.12 * age + wind * age * 5, my - age * hh * 0.02 - 4, r, col, a, seed=int(jv * 9), rot=age * 0.2)


def _vis(f):
    try:
        b = f.c.getLocalClipBounds()
        return (b.left(), b.top(), b.right(), b.bottom())
    except Exception:
        return None


def _snow(f, t, n):
    rs = RS(19)
    for layer, (cnt, size, sp) in enumerate(((n // 2, 1.6, 38), (n // 3, 2.6, 62), (n // 6, 4.0, 90))):
        pl = []
        for i in range(cnt):
            px = (rs.rand() * W + math.sin(t * 0.8 + i * 1.7) * 26 * (layer + 1) + t * 12 * (layer + 1)) % W
            py = (rs.rand() * H + t * sp) % H
            pl.append(skia.Point(px, py))
        pp = skia.Paint(AntiAlias=True, Color=C("#FFFFFF", 200 - layer * 20), StrokeWidth=size, StrokeCap=skia.Paint.kRound_Cap)
        f.c.drawPoints(skia.Canvas.kPoints_PointMode, pl, pp)


# ───────────────────────────── sahne ─────────────────────────────
@SL.sc("field")
class Field:
    """Savaş alanı. p: ground, weather, armies, banners, smoke, river, castle_far, wind (bkz. SAHNE_KATALOGU_deniz_savas.md)."""

    def __init__(self, p):
        self.p = p
        self.ground = p.get("ground", "plain")
        if self.ground not in GROUND:
            self.ground = "plain"
        self.weather = p.get("weather", "clear")
        if self.weather not in WEATHER:
            self.weather = "clear"
        self.M = dict(_weather(self.weather))
        self.M["_banners"] = bool(p.get("banners", True))
        self.river = bool(p.get("river", self.ground == "river"))
        self.castle = p.get("castle_far")
        self.smoke = float(p.get("smoke", 0.0))
        self.wind = 1 if p.get("wind", -1) >= 0 else -1
        self.armies = list(p.get("armies") or [dict(side="#8E1F26", kind="pike", x=0.5, row=1, n=30, dir=1)])
        self.fire = float(p.get("fire", 0.0))
        self.rain = float(p.get("rain", 1.0 if self.weather == "rain" else 0.0))
        self.snow = float(p.get("snow", 1.0 if self.weather == "snow" else 0.0))

    def layers(self):
        g, w, c = self.ground, self.weather, self.castle

        def base(f):
            bake_base(f, g, w, c)
        return [(BASE_D, base)]

    def dyn(self):
        M, g, w = self.M, self.ground, self.weather
        river = self.river
        wind = self.wind

        def master(f, t):
            cam = SW.cam_from_canvas(f, BASE_D)
            c1 = _cloud_f(w, "low")
            wpx = c1.width() * 2
            off = (t * (3.5 if w != "rain" else 9.0)) % wpx
            x_a = (-MARGIN - wpx + off) if wind > 0 else (-MARGIN - off)
            for dx in (0, wpx):
                _draw_img2(f, c1, x_a + dx, -MARGIN + 150 + (HZ + MARGIN + 60) * 0.44, 0.7)
            fx_list = []
            rows_by_band = {0: [], 1: [], 2: []}
            fords = []
            for ai, a in enumerate(self.armies):
                if a.get("ford") and river:
                    fords.append((ai, a))
                else:
                    rows_by_band[ROW_BAND[int(clamp(a.get("row", 1), 0, 2))]].append((ai, a))
            for k in range(4):
                SW.push_depth(f, cam, BAND_D[k])
                bimg, bx, by = band_image(g, w, k, river)
                f.c.drawImage(bimg, bx, by, LIN, skia.Paint())
                vis = _vis(f)
                if k in rows_by_band:
                    for ai, a in rows_by_band[k]:
                        draw_army(f, M, g, w, a, ai, t, vis, fx_list)
                    if self.smoke > 0.02 and k in (0, 1):
                        self._smoke(f, t, k)
                    if self.fire > 0.02 and k == 0:
                        self._fires(f, t)
                if fx_list and k == 2:
                    draw_fx_smoke(f, M, fx_list, wind * 6)
                f.c.restore()
                if k == 0 and river:
                    SW.push_depth(f, cam, RIVER_D)
                    rimg, rx, ry = river_image(g, w)
                    f.c.drawImage(rimg, rx, ry, LIN, skia.Paint())
                    self._river_strips(f, t)
                    vis = _vis(f)
                    for ai, a in fords:
                        draw_army(f, M, g, w, a, ai, t, vis, fx_list)
                    f.c.restore()
                if k == 1 and (w in ("fog", "dawn", "rain", "snow") or g == "marsh"):
                    self._fog(f, cam, t, 0.42 if w == "fog" else 0.26)
            self._foreground(f, cam)
            self._overlay(f, t)
        return {0: master}

    # --- parçalar
    def _smoke(self, f, t, k):
        sm = self.smoke
        rs = RS(300 + k)
        col = "#8A7F76" if self.M["bright"] > 0.85 else "#4C5258"
        if self.weather in ("dusk", "dawn"):
            col = "#8C6A58"
        by = EDGE_Y[k]
        for i in range(int(2 + 4 * sm)):
            x = rs.rand() * W + math.sin(t * 0.13 + i) * 40 + t * 5 * -self.wind
            y = by - 20 - rs.rand() * 130
            r = 110 + rs.rand() * 100
            a = (0.16 + 0.34 * sm) * (0.6 + 0.4 * math.sin(t * 0.25 + i * 1.7))
            PW.puff(f, x, y, r, col, a, seed=i + k, rot=0.3 * i)

    def _fires(self, f, t):
        """Uzakta yanan köy/kale: ev siluetleri + alev + duman sütunu (fire=0..1: yangın sayısı/şiddeti)."""
        fr = self.fire
        n = 1 + int(2.2 * fr)
        for i in range(n):
            x = W * (0.16 + 0.31 * i + 0.07 * math.sin(i * 2.3))
            y = edge_y(self.ground, 0, x) + 3
            base = mix("#14100C", self.M["haze"], 0.25)
            for q in range(5):
                hx = x + (q - 2) * 26
                hh = 20 + 8 * ((q * 7 + i) % 4)
                f.rect(hx - 11, y - hh, 22, hh, color=base)
                f.poly([(hx - 14, y - hh), (hx, y - hh - 12), (hx + 14, y - hh)], color=base)
            for q in range(3):
                PW.flame(f, x + (q - 1) * 30, y - 12, 0.62 * (0.6 + 0.6 * fr), t, seed=i * 3 + q, glow_a=0.9)
            PW.glow(f, x, y - 30, 190 * (0.6 + 0.5 * fr), "#FF8A2E", 0.55)
            PW.smoke_column(f, x, y - 40, t, n=7, h=380 * (0.6 + 0.6 * fr), w0=18, w1=80, col="#17130F", a=0.55 * (0.5 + 0.5 * fr), rate=0.1, drift=-self.wind * 90, seed=i + 7)

    def _river_strips(self, f, t):
        M = self.M
        body = mix(M["haze"], "#26363E", 0.62)
        crest = mix(M["haze"], "#FFFFFF", 0.35)
        a = PW.wave_strip(1180, 46, 8, body, mix(crest, body, 0.45), "#EEF2F0", 811, sharp=1.9, foam_amt=0.0, glint=M["haze"], glint_amt=0.5, facets=2, shade="#06141C")
        b = PW.wave_strip(900, 34, 6, body, mix(crest, body, 0.4), "#EEF2F0", 812, sharp=2.2, foam_amt=0.0, glint=M["haze"], glint_amt=0.7, facets=2, shade="#06141C", comps=((2, 1.0), (5, 0.5), (9, 0.25)))
        sp = 22.0 * (-self.wind)
        for i, (y, img, spd, al) in enumerate(((RIVER_Y - 4, a, sp, 1.0), (RIVER_Y + 40, b, sp * 1.4, 0.55), (RIVER_Y + 70, a, sp * 1.8, 0.45))):
            PW.draw_strip(f, img, -MARGIN, W + MARGIN, y + math.sin(t * 0.6 + i) * 1.5, t * spd + 250 * i, alpha=al)

    def _fog(self, f, cam, t, alpha):
        SW.push_depth(f, cam, 0.66)
        img = _fog_img(self.weather, self.M["haze"])
        wpx = img.width() * 2
        off = (t * 7.0) % wpx
        x_a = (-MARGIN - wpx + off) if self.wind > 0 else (-MARGIN - off)
        for dx in (0, wpx):
            p_ = skia.Paint()
            p_.setAlphaf(alpha)
            f.c.save()
            f.c.translate(x_a + dx, 700)
            f.c.scale(2.0, 2.0)
            f.c.drawImage(img, 0, 0, LIN, p_)
            f.c.restore()
        f.c.restore()

    def _foreground(self, f, cam):
        SW.push_depth(f, cam, FG_D)
        img, x, y = fg_image(self.ground, self.weather)
        f.c.drawImage(img, x, y, LIN, skia.Paint())
        f.c.restore()

    def _overlay(self, f, t):
        c = f.c
        c.save()
        c.resetMatrix()
        if self.rain > 0.02:
            r = self.rain
            PW.rain_lines(f, t, n=int(60 + 120 * r), seed=8, angle=-0.22, length=20, alpha=0.18 * r + 0.05, color="#C9D6D8", speed=1100, sw=1.1, rect=(0, 0, W, H))
            PW.rain_lines(f, t, n=int(44 + 100 * r), seed=18, angle=-0.22, length=34, alpha=0.24 * r + 0.05, color="#C9D6D8", speed=1500, sw=1.4, rect=(0, 0, W, H))
            PW.rain_lines(f, t, n=int(20 + 56 * r), seed=28, angle=-0.22, length=58, alpha=0.28 * r + 0.04, color="#C9D6D8", speed=1950, sw=2.0, rect=(0, 0, W, H))
        if self.snow > 0.02:
            _snow(f, t, int(60 + 160 * self.snow))
        c.restore()
