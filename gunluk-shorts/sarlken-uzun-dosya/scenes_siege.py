"""Sahne ailesi: KUŞATMA (`siege`) — Roma 1527, Viyana 1529, Güns, Halkulvadi (La Goulette), Tenochtitlan, Toledo.
Kayıt: @SL.sc("siege"). Ayrıntılı API: SAHNE_KATALOGU_deniz_savas.md

Mimari (sea/field ile aynı): tek taban katman (gök + uzak tepe/dağ) + dyn içinde kırpılmış katman görüntüleri
(şehir/kale siluetleri, orta zemin, yakın zemin, ön plan) kendi paralaksıyla; ardından yangın/alev, top ateşi/duman,
merdiven + tırmanan askerler, sancaklar, savunucular, meşale ışıkları, yağmur/kar.
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

BASE_D, CITY_D, MID_D, NEAR_D, FG_D = 0.08, 0.42, 0.64, 0.92, 1.22
HZ = 540                                   # ufuk
CITY_BASE = 668                            # şehir/sur tabanı (şehir katmanı koordinatı)
MID_Y, NEAR_Y, FG_Y = 770, 905, 1026       # zemin kenarları (orta / yakın / ön plan)

TIMES = dict(
    day=dict(sky=[("#2F4C69", 0.0), ("#7A91A1", 0.48), ("#CBC4A2", 0.86), ("#E8D6A6", 1.0)], haze="#D6C7A0", sun=(0.76, 330, 40, "#FFF1CC", "#FFCF86"), moon=False, rim="#EBB571", lit=False, fire_vis=0.5, bright=1.0, cover=0.40,
             cloud_shadow="#56626E", cloud_light="#F6E0B2"),
    dusk=dict(sky=[("#171B36", 0.0), ("#4B3359", 0.30), ("#A24A55", 0.62), ("#E2733C", 0.86), ("#FFB257", 1.0)], haze="#EE9150", sun=(0.24, 512, 64, "#FFE2A0", "#FF8E3C"), moon=False, rim="#FF9A4E", lit=True, fire_vis=0.85, bright=0.95, cover=0.52,
              cloud_shadow="#3A2542", cloud_light="#FF9A55"),
    night=dict(sky=[("#04070E", 0.0), ("#0A1524", 0.40), ("#14283C", 0.78), ("#2A4660", 1.0)], haze="#33516B", sun=None, moon=True, rim="#8FB0CC", lit=True, fire_vis=1.0, bright=0.8, cover=0.34,
               cloud_shadow="#0A121C", cloud_light="#5E7894"),
)
CITIES = dict(
    roma=dict(stone="#7A5440", stone2="#5A3C2E", roof="#5A3026", ground="#6E5A3C", ground2="#2E2616", horizon_hills=True, att="imperial"),
    viyana=dict(stone="#8E8068", stone2="#645844", roof="#6E3C2E", ground="#5E6638", ground2="#252C16", horizon_hills=True, att="ottoman"),
    guns=dict(stone="#8A7C64", stone2="#605440", roof="#4A2E24", ground="#5A6A3A", ground2="#232C16", horizon_hills=True, att="ottoman"),
    halkulvadi=dict(stone="#AA9670", stone2="#7A6848", roof="#6A4A30", ground="#B09C6E", ground2="#4A3E26", horizon_hills=False, att="imperial"),
    tenochtitlan=dict(stone="#B9AC90", stone2="#8A7E66", roof="#A89878", ground="#4A5A3A", ground2="#1E2A1A", horizon_hills=True, att="spanish"),
    toledo=dict(stone="#8A7258", stone2="#5E4C3A", roof="#5A3226", ground="#7A6A40", ground2="#2C2616", horizon_hills=True, att="imperial"),
)


def _time(name, weather):
    T = dict(TIMES.get(name, TIMES["day"]))
    T["snow"] = (weather == "snow")
    T["time"] = name
    if weather == "rain":
        T["sky"] = [(mix(c, "#3A4348", 0.55), u) for c, u in T["sky"]]
        T["haze"] = mix(T["haze"], "#6E7A7A", 0.55)
        T["cover"] = 0.76
        T["bright"] *= 0.88
        T["cloud_shadow"] = mix(T["cloud_shadow"], "#0F1519", 0.5)
        T["cloud_light"] = mix(T["cloud_light"], "#6E8084", 0.6)
        T["sun"] = None
    elif weather == "snow":
        T["sky"] = [(mix(c, "#9AA3AA", 0.5), u) for c, u in T["sky"]]
        T["haze"] = mix(T["haze"], "#B8C0C4", 0.55)
        T["cover"] = 0.64
        T["sun"] = None
        T["cloud_light"] = mix(T["cloud_light"], "#DADFE0", 0.6)
    return T


def _stone(city, T, k=0.0, shade=0.0):
    C_ = CITIES[city]
    c = mix(C_["stone"], C_["stone2"], shade)
    return mix(c, T["haze"], k)


# ───────────────────────────── kamera yardımcıları ─────────────────────────────
def safe_cam(x, y, z, dmax=1.22):
    z = max(1.0, z)
    s = 1 + (z - 1) * dmax
    lx = (1180 - W / 2 / s) / dmax
    ly = (760 - H / 2 / s) / dmax
    return (W / 2 + max(-lx, min(lx, x - W / 2)), H / 2 + max(-ly, min(ly, y - H / 2)), z)


def cam_on_city(x=0.5, zoom=1.4, y=0.0):
    """Şehir/sur katmanında (x: 0..1, y: sahne y'si; 0 → sur tepesi civarı) bir noktaya odaklan."""
    X = x * W
    Y = (CITY_BASE - 170) if y == 0.0 else y
    cx = W / 2 + (X - W / 2) / CITY_D
    cy = H / 2 + (Y - H / 2) / CITY_D
    return safe_cam(cx, cy, zoom)


# ───────────────────────────── gök ─────────────────────────────
@lru_cache(maxsize=10)
def _cloud_s(time, weather, which):
    T = _time(time, weather)
    w2, h2 = (W + 2 * MARGIN) // 2, (HZ + MARGIN + 60) // 2
    yy = np.linspace(0, 1, h2, dtype=np.float32)
    if which == "mid":
        vf = np.clip(np.minimum(yy * 5, (1 - yy) * 3.0), 0, 1)
        a = PW.cloud_rgba(w2, h2, 61, cover=T["cover"], soft=0.36, scale=46, octaves=6, shadow=T["cloud_shadow"], light=T["cloud_light"], rim=None, vfade=vf, stretch=2.1,
                          periodic=True, gamma=1.15, thick_dark=0.4 if weather == "rain" else 0.2, sigma=5.0, reach=16, gain=1.35, light_dir=(0.55, -0.8))
        return PW.img_from_rgba(a, mip=False)
    vf = np.clip(np.minimum((yy - 0.45) * 4, (1.0 - yy) * 5), 0, 1)
    a = PW.cloud_rgba(w2, h2, 63, cover=T["cover"] * 0.85, soft=0.34, scale=30, octaves=5, shadow=mix(T["cloud_shadow"], T["haze"], 0.25), light=mix(T["cloud_light"], T["haze"], 0.35), rim=None,
                      vfade=vf, stretch=3.4, periodic=True, gamma=1.1, gain=1.3, sigma=2.5, reach=8, light_dir=(0.5, -0.7))
    r0, r1 = int(h2 * 0.50), int(h2 * 0.97)
    return PW.img_from_rgba(np.ascontiguousarray(a[r0:r1]), mip=False)


def _draw_img2(f, img, x, y, alpha=1.0):
    p = skia.Paint()
    if alpha < 1:
        p.setAlphaf(alpha)
    f.c.save()
    f.c.translate(x, y)
    f.c.scale(2.0, 2.0)
    f.c.drawImage(img, 0, 0, LIN, p)
    f.c.restore()


def _ridge(f, y, amp, col, seed, step=40, wl=0.0035, bottom=None):
    rs = RS(seed)
    ph = rs.rand() * 6.28
    pts = [(xx, y + math.sin(xx * wl + ph) * amp + math.sin(xx * wl * 2.7 + ph * 2) * amp * 0.4 + math.sin(xx * wl * 6.1 + ph) * amp * 0.12) for xx in range(-MARGIN, W + MARGIN + step, step)]
    pts += [(W + MARGIN, bottom or HZ + 160), (-MARGIN, bottom or HZ + 160)]
    f.path(sk.poly_path(pts, True), color=col)
    return pts


def bake_base(f, city, time, weather):
    T = _time(time, weather)
    C_ = CITIES[city]
    f.rect(-MARGIN, -MARGIN, W + 2 * MARGIN, HZ + MARGIN + 140, shader=f.lin(0, -MARGIN, 0, HZ, [(c, u) for c, u in T["sky"]]))
    if time == "night" or (T["moon"] and weather != "snow"):
        rs = RS(11)
        for i in range(380):
            x = rs.rand() * (W + 2 * MARGIN) - MARGIN
            y = (rs.rand() ** 1.7) * (HZ - 60) - MARGIN * 0.6
            f.circle(x, y, 0.6 + rs.rand() * 1.4, color="#DDE8FF", alpha=(0.25 + rs.rand() * 0.75) * (1 - clamp((y + 120) / 650) * 0.8) * (0.3 if weather == "rain" else 1.0))
        mx, my, mr = W * 0.30, 170, 50
        PW.glow_add(f, mx, my, 640, "#9FBBD6", 0.36 if weather != "rain" else 0.18, 140, 40, 0.3)
        f.circle(mx, my, mr, shader=f.rad(mx - 14, my - 16, mr * 1.5, [("#FBFDFF", 0.0), ("#DCE8F2", 0.6), ("#9FB4C8", 1.0)]), alpha=1.0 if weather != "rain" else 0.5)
    sun = T["sun"]
    if sun:
        sx, sy, sr, core, gc = sun
        sx *= W
        PW.glow_add(f, sx, sy, 760, gc, 0.30, 150, 46, 0.30)
        PW.glow_add(f, sx, sy, 300, gc, 0.42, 230, 90, 0.38)
        f.circle(sx, sy, sr, shader=f.rad(sx, sy, sr, [("#FFFFFF", 0.0), (core, 0.7), (core, 1.0)]))
        ST.god_rays(f, (sx, sy), -math.pi / 2, 2.6, 1500, n=9, alpha=0.05, color=mix(gc, "#FFFFFF", 0.3), seed=4, blur=26)
    _draw_img2(f, _cloud_s(time, weather, "mid"), -MARGIN, -MARGIN + 30, 0.95)
    hz_c = mix(mix(C_["ground2"], "#2A3A44", 0.5), T["haze"], 0.55)
    if city == "tenochtitlan":
        # Popocatépetl ve Iztaccíhuatl (kar tepeli volkanlar)
        for (vx, vh, vw) in ((W * 0.18, 230, 520), (W * 0.30, 170, 420)):
            pts = [(vx - vw, HZ + 40), (vx - vw * 0.5, HZ - vh * 0.55), (vx - vw * 0.12, HZ - vh * 0.92), (vx, HZ - vh), (vx + vw * 0.12, HZ - vh * 0.92), (vx + vw * 0.5, HZ - vh * 0.55), (vx + vw, HZ + 40)]
            f.path(sk.smooth_path(pts, True, 0.25), color=mix(hz_c, T["haze"], 0.35))
            f.path(sk.smooth_path([(vx - vw * 0.2, HZ - vh * 0.82), (vx - vw * 0.1, HZ - vh * 0.95), (vx, HZ - vh), (vx + vw * 0.1, HZ - vh * 0.95), (vx + vw * 0.2, HZ - vh * 0.82), (vx + vw * 0.08, HZ - vh * 0.78), (vx, HZ - vh * 0.84), (vx - vw * 0.08, HZ - vh * 0.76)], True, 0.3), color=mix("#EDEFF2", T["haze"], 0.35))
    if C_["horizon_hills"]:
        _ridge(f, HZ - 6, 30, mix(hz_c, T["haze"], 0.18), 3, wl=0.0030)
        _ridge(f, HZ + 12, 20, mix(hz_c, T["haze"], 0.0), 9, wl=0.0045)
    f.rect(-MARGIN, HZ - 150, W + 2 * MARGIN, 230, shader=f.lin(0, HZ - 150, 0, HZ + 70, [(T["haze"], 0.0, 0), (T["haze"], 0.7, int(255 * 0.35)), (T["haze"], 1.0, int(255 * 0.45))]))
    f.rect(-MARGIN, HZ + 70, W + 2 * MARGIN, 700, color=(_water_cols(T)[0] if city in ("tenochtitlan", "halkulvadi") else mix(C_["ground"], T["haze"], 0.55)))


# ───────────────────────────── yapı ilkelleri ─────────────────────────────
def _masonry(f, x0, y0, w, h, col, rs, course=15, blk=(36, 70), dark=0.20, light=0.10):
    """Taş/tuğla duvar dokusu: sıra çizgileri + kaydırmalı derzler + rastgele blok tonları."""
    n = int(h / course) + 1
    for r in range(n):
        y = y0 + r * course
        f.line(x0, y, x0 + w, y, color="#000000", sw=1.0, alpha=dark * 0.9)
        x = x0 + rs.rand() * blk[0] * (1 + 0.6 * (r % 2))
        while x < x0 + w:
            bw = blk[0] + rs.rand() * (blk[1] - blk[0])
            f.line(x, y, x, y + course, color="#000000", sw=1.0, alpha=dark * 0.7)
            if rs.rand() > 0.62:
                f.rect(x, y + 1, bw, course - 1, color=("#000000" if rs.rand() > 0.5 else "#FFFFFF"), alpha=0.05 + 0.05 * rs.rand())
            x += bw


def _merlons(f, x0, x1, ytop, col, mw=22, mh=17, gap=14, shade=None):
    x = x0
    while x < x1 - mw * 0.5:
        f.rect(x, ytop - mh, mw, mh + 2, color=col)
        if shade:
            f.rect(x + mw * 0.55, ytop - mh, mw * 0.45, mh + 2, color=shade, alpha=0.25)
        x += mw + gap


def wall(f, x0, x1, yb, h, T, city, lit_dir, rs, k=0.08, merlons=True, slits=True, tex=True, light=True):
    col = _stone(city, T, k)
    f.rect(x0, yb - h, x1 - x0, h, shader=f.lin(0, yb - h, 0, yb, [(lighten(col, 0.10), 0.0), (col, 0.30), (darken(col, 0.30), 1.0)]))
    if tex:
        _masonry(f, x0, yb - h, x1 - x0, h, col, rs)
    if merlons:
        _merlons(f, x0, x1, yb - h, col, shade="#000000")
    f.rect(x0, yb - h - 3, x1 - x0, 6, color=darken(col, 0.20))                    # sur üstü kornişi
    if slits:
        x = x0 + 30
        while x < x1 - 30:
            f.rect(x, yb - h * 0.62, 5, 18, color="#0A0705", alpha=0.8)
            x += 90 + rs.rand() * 80
    if light:
        f.line(x0, yb - h - 1, x1, yb - h - 1, color=T["rim"], sw=2.0, alpha=0.40)
    f.rect(x0, yb - 26, x1 - x0, 26, shader=f.lin(0, yb - 26, 0, yb, [("#000000", 0.0, 0), ("#000000", 1.0, 70)]))


def tower(f, x, yb, w, h, T, city, lit_dir, rs, kind="round", roof="cone", k=0.06, banner=None):
    col = _stone(city, T, k)
    x0, x1 = x - w / 2, x + w / 2
    ls = lit_dir
    if kind == "round":
        a, b = (x0, x1) if ls < 0 else (x1, x0)
        f.rect(x0, yb - h, w, h, shader=f.lin(a, 0, b, 0, [(lighten(col, 0.16), 0.0), (col, 0.45), (darken(col, 0.42), 1.0)]))
    else:
        f.rect(x0, yb - h, w, h, shader=f.lin(0, yb - h, 0, yb, [(lighten(col, 0.08), 0.0), (darken(col, 0.28), 1.0)]))
        fx = x0 if ls < 0 else x1 - w * 0.34
        f.rect(fx, yb - h, w * 0.34, h, color="#000000", alpha=0.0)
        sx = x1 - w * 0.36 if ls < 0 else x0
        f.rect(sx, yb - h, w * 0.36, h, color="#000000", alpha=0.28)
    _masonry(f, x0, yb - h, w, h, col, rs, course=14, blk=(26, 48))
    f.rect(x0 - 4, yb - h - 4, w + 8, 10, color=darken(col, 0.15))
    f.rect(x0, yb - 26, w, 26, shader=f.lin(0, yb - 26, 0, yb, [("#000000", 0.0, 0), ("#000000", 1.0, 70)]))
    rc = mix(CITIES[city]["roof"], T["haze"], 0.10)
    if T.get("snow"):
        rc = mix(rc, "#E6EAED", 0.72)
    ytop = yb - h - 4
    if roof == "cone":
        f.poly([(x0 - 8, ytop), (x, ytop - w * 0.95), (x1 + 8, ytop)], color=rc)
        f.poly([(x0 - 8, ytop), (x, ytop - w * 0.95), (x + (x1 - x0) * (-0.08 if ls < 0 else 0.08), ytop)], color=lighten(rc, 0.12), alpha=0.5)
        f.line(x, ytop - w * 0.95, x, ytop - w * 1.12, color="#0A0705", sw=2.4)
        if banner:
            meta_flag(banner, x, ytop - w * 1.1)
    elif roof == "flat":
        _merlons(f, x0 - 2, x1 + 2, ytop + 3, col, mw=18, mh=15, gap=10, shade="#000000")
    elif roof == "dome":
        f.oval(x, ytop, w * 0.56, w * 0.46, color=rc)
    f.line(x0 + 1, yb - h, x0 + 1, yb - 30, color=T["rim"], sw=1.6, alpha=0.30 if ls < 0 else 0.0)
    f.line(x1 - 1, yb - h, x1 - 1, yb - 30, color=T["rim"], sw=1.6, alpha=0.30 if ls > 0 else 0.0)


_META = {}


def meta_flag(spec, x, y):
    if _META.get("cur") is not None:
        _META["cur"]["flags"].append((x, y, spec))


def _meta_add(key, v):
    if _META.get("cur") is not None:
        _META["cur"][key].append(v)


def _house2(f, x, yb, w, h, rh, wall_c, roof_c, T, lit_dir, rs, lit=False, burn=0.0, win=True):
    f.rect(x - w / 2, yb - h, w, h, color=wall_c)
    side = x + (w * 0.2 if lit_dir < 0 else -w * 0.5)
    f.rect(side, yb - h, w * 0.3, h, color="#000000", alpha=0.26)
    if T.get("snow"):
        roof_c = mix(roof_c, "#E6EAED", 0.72)
    f.poly([(x - w / 2 - 4, yb - h), (x, yb - h - rh), (x + w / 2 + 4, yb - h)], color=roof_c)
    f.line(x - w / 2 - 4, yb - h, x, yb - h - rh, color=T["rim"], sw=1.2, alpha=0.35)
    if win:
        for q in range(1 if w < 46 else 2):
            wx = x + (q - (1 if w >= 46 else 0) * 0.5) * w * 0.4
            wy = yb - h * 0.55
            on = (lit and rs.rand() > 0.35) or burn > 0
            if on:
                col_ = "#FFB045" if burn > 0 else "#FFC770"
                f.rect(wx - 3.2, wy - 4.5, 6.4, 9, color=col_)
                PW.glow_add(f, wx, wy, 14, "#FF9A2E" if burn > 0 else "#FFB347", 0.7)
            else:
                f.rect(wx - 3.2, wy - 4.5, 6.4, 9, color="#0A0705", alpha=0.7)
    if burn > 0:
        _meta_add("fires", (x, yb - h - rh * 0.5, 0.55 + 0.5 * burn))


def _tent_ottoman(f, x, yb, s, col, trim, T, lit=False, door=True):
    """Osmanlı çadırı: silindir gövde + sivri konik çatı + altın alem (yarım ay)."""
    w, hb, hr = 120 * s, 48 * s, 84 * s
    f.rect(x - w / 2, yb - hb, w, hb, shader=f.lin(x - w / 2, 0, x + w / 2, 0, [(lighten(col, 0.10), 0.0), (col, 0.5), (darken(col, 0.38), 1.0)]))
    f.poly([(x - w / 2 - 6 * s, yb - hb), (x, yb - hb - hr), (x + w / 2 + 6 * s, yb - hb)], color=col)
    f.poly([(x - w / 2 - 6 * s, yb - hb), (x, yb - hb - hr), (x + w * 0.1, yb - hb)], color=lighten(col, 0.10), alpha=0.5)
    f.poly([(x + w * 0.1, yb - hb), (x, yb - hb - hr), (x + w / 2 + 6 * s, yb - hb)], color="#000000", alpha=0.25)
    f.rect(x - w / 2 - 6 * s, yb - hb - 3 * s, w + 12 * s, 7 * s, color=trim)
    f.rect(x - w / 2, yb - 7 * s, w, 7 * s, color=trim, alpha=0.9)
    for q in range(-2, 3):                                   # kumaş şeritleri
        f.line(x + q * w * 0.22, yb - hb - 2, x + q * w * 0.05, yb - hb - hr + 4, color="#000000", sw=1.2 * s, alpha=0.22)
    f.line(x, yb - hb - hr, x, yb - hb - hr - 22 * s, color="#C9962B", sw=2.4 * s)
    f.circle(x, yb - hb - hr - 24 * s, 4.2 * s, color="#E8C25A")
    f.path(PW.crescent_path(x, yb - hb - hr - 36 * s, 6.5 * s), color="#E8C25A")
    if door:
        f.poly([(x - 14 * s, yb), (x - 11 * s, yb - 30 * s), (x + 11 * s, yb - 30 * s), (x + 14 * s, yb)], color="#0A0705", alpha=0.9)
        if lit:
            f.poly([(x - 12 * s, yb), (x - 9 * s, yb - 27 * s), (x + 9 * s, yb - 27 * s), (x + 12 * s, yb)], color="#FFB045", alpha=0.85)
            PW.glow_add(f, x, yb - 14 * s, 40 * s, "#FF9A2E", 0.55)


def _tent_pavilion(f, x, yb, s, col, trim, T, lit=False):
    """Avrupa ordugâh çadırı: dikdörtgen gövde + beşik çatı + flama direği."""
    w, hb, hr = 110 * s, 40 * s, 52 * s
    f.rect(x - w / 2, yb - hb, w, hb, shader=f.lin(0, yb - hb, 0, yb, [(lighten(col, 0.08), 0.0), (darken(col, 0.32), 1.0)]))
    f.poly([(x - w / 2 - 8 * s, yb - hb), (x - w * 0.12, yb - hb - hr), (x + w * 0.12, yb - hb - hr), (x + w / 2 + 8 * s, yb - hb)], color=lighten(col, 0.04))
    f.rect(x - w / 2 - 8 * s, yb - hb - 3 * s, w + 16 * s, 6 * s, color=trim)
    f.poly([(x - 12 * s, yb), (x - 9 * s, yb - 28 * s), (x + 9 * s, yb - 28 * s), (x + 12 * s, yb)], color="#0A0705", alpha=0.9)
    if lit:
        f.poly([(x - 10 * s, yb), (x - 7 * s, yb - 25 * s), (x + 7 * s, yb - 25 * s), (x + 10 * s, yb)], color="#FFB045", alpha=0.8)
        PW.glow_add(f, x, yb - 12 * s, 36 * s, "#FF9A2E", 0.5)
    f.line(x, yb - hb - hr, x, yb - hb - hr - 34 * s, color="#0A0705", sw=2.0 * s)
    _meta_add("flags", (x, yb - hb - hr - 34 * s, trim))


def _tent_small(f, x, yb, s, col, T):
    w, hh = 64 * s, 46 * s
    f.poly([(x - w / 2, yb), (x, yb - hh), (x + w / 2, yb)], color=col)
    f.poly([(x, yb - hh), (x + w / 2, yb), (x + w * 0.1, yb)], color="#000000", alpha=0.26)
    f.poly([(x - 8 * s, yb), (x, yb - 22 * s), (x + 8 * s, yb)], color="#0A0705", alpha=0.85)


def _gabions(f, x0, x1, y, T, rs, col, h=26, w=22):
    """Hasır sepet (gabion) dizisi."""
    x = x0
    while x < x1:
        f.rect(x, y - h, w, h, color=col)
        f.rect(x + w * 0.62, y - h, w * 0.38, h, color="#000000", alpha=0.22)
        for q in range(4):
            f.line(x + 1, y - h + q * h / 4, x + w - 1, y - h + q * h / 4, color="#000000", sw=1.0, alpha=0.30)
        f.oval(x + w / 2, y - h, w / 2, 4, color=lighten(col, 0.1))
        x += w + 2


def _palisade(f, x0, x1, y, T, col, h=34):
    x = x0
    while x < x1:
        hh = h + (hash(int(x)) % 7)
        f.poly([(x, y), (x + 5, y - hh), (x + 10, y)], color=col)
        x += 9


@lru_cache(maxsize=24)
def cannon_sprite(ks, col, rim):
    """Büyük topçu (bombard) — gövde + tekerlek + kuyruk; namlu ucu sağda. (img, ox, oy, ks). Orijin: yer hizası, tekerlek ekseni civarı."""
    w, h = int(330 * ks) + 16, int(150 * ks) + 16
    ox, oy = int(170 * ks) + 8, int(120 * ks) + 8

    def fn(f):
        f.c.scale(ks, ks)
        rimc = rim
        # kuyruk
        f.poly([(-120, 0), (-100, -8), (-20, -42), (-10, -30)], color=col)
        # gövde (kundak)
        f.path(sk.poly_path([(-66, -30), (50, -40), (58, -62), (-60, -66)], True), color=col)
        # namlu (konik) + halkalar
        f.poly([(-52, -78), (-52, -52), (118, -58), (118, -70)], color=col)
        for q in range(5):
            xx = -30 + q * 34
            f.line(xx, -76 + q * 1.2, xx, -53 - q * 0.6, color=rimc, sw=1.4, alpha=0.55)
        f.poly([(112, -73), (130, -77), (130, -51), (112, -55)], color=col)
        f.oval(-52, -65, 12, 14, color=col)
        f.line(-50, -79, 120, -72, color=rimc, sw=1.5, alpha=0.8)
        # tekerlek
        for cx_ in (-8,):
            f.circle(cx_, -28, 31, color=col)
            f.circle(cx_, -28, 31, style="stroke", sw=2.0, color=rimc, alpha=0.65)
            f.circle(cx_, -28, 22, style="stroke", sw=1.4, color="#000000", alpha=0.5)
            for q in range(8):
                a = q * math.pi / 4
                f.line(cx_ + math.cos(a) * 5, -28 + math.sin(a) * 5, cx_ + math.cos(a) * 29, -28 + math.sin(a) * 29, color=rimc, sw=1.1, alpha=0.45)
            f.circle(cx_, -28, 6, color=rimc, alpha=0.7)
    im = PW.bake_sprite(fn, w, h, ox, oy)
    return im, ox, oy, ks


def _smoke_col_default(T):
    return "#9C9288" if T["bright"] > 0.9 else "#5C5C60"


# ───────────────────────────── şehir / kale siluetleri ─────────────────────────────
def _skyline(f, x0, x1, yb, hmin, hmax, T, city, lit_dir, rs, lit, fire, wall_k=0.18, dens=(34, 62), tall_every=0):
    """Şehir ev dizisi (arkadan öne iki sıra). fire: yangın olasılığı (0..1)."""
    C_ = CITIES[city]
    x = x0
    n = 0
    while x < x1:
        w = dens[0] + rs.rand() * (dens[1] - dens[0])
        h = hmin + rs.rand() * (hmax - hmin)
        rh = 14 + rs.rand() * 20
        burn = 1.0 if (rs.rand() < fire * 0.30) else 0.0
        wc = mix(_stone(city, T, wall_k, shade=rs.rand() * 0.5), "#000000", 0.0)
        rc = mix(C_["roof"], T["haze"], 0.10 + 0.1 * rs.rand())
        _house2(f, x + w / 2, yb, w, h, rh, wc, rc, T, lit_dir, rs, lit=lit, burn=burn)
        x += w * (0.80 + 0.3 * rs.rand())
        n += 1


def _arch_gate(f, x, yb, w, h, T, col):
    f.path(sk.smooth_path([(x - w / 2, yb), (x - w / 2, yb - h * 0.6), (x, yb - h), (x + w / 2, yb - h * 0.6), (x + w / 2, yb)], True, 0.5), color="#0A0705")
    for q in range(-3, 4):
        f.line(x + q * w * 0.13, yb, x + q * w * 0.13, yb - h * 0.8 + abs(q) * 3, color=lighten(col, 0.1), sw=1.4, alpha=0.5)
    f.line(x - w / 2, yb - h * 0.45, x + w / 2, yb - h * 0.45, color=lighten(col, 0.1), sw=1.4, alpha=0.5)


def _sant_angelo(f, x, yb, T, city, lit_dir, rs, lit):
    """Castel Sant'Angelo: kare kaide + büyük silindir + küçük silindir + melek heykeli."""
    col = _stone(city, T, 0.12)
    base_w, base_h = 330, 96
    f.rect(x - base_w / 2, yb - base_h, base_w, base_h, shader=f.lin(0, yb - base_h, 0, yb, [(lighten(col, 0.08), 0.0), (darken(col, 0.3), 1.0)]))
    _masonry(f, x - base_w / 2, yb - base_h, base_w, base_h, col, rs, course=14)
    _merlons(f, x - base_w / 2, x + base_w / 2, yb - base_h, col, shade="#000000")
    for tx in (-1, 1):
        tower(f, x + tx * (base_w / 2 - 10), yb, 70, base_h + 54, T, city, lit_dir, rs, kind="round", roof="flat")
    dw, dh = 240, 130
    a, b = (x - dw / 2, x + dw / 2) if lit_dir < 0 else (x + dw / 2, x - dw / 2)
    f.rect(x - dw / 2, yb - base_h - dh, dw, dh, shader=f.lin(a, 0, b, 0, [(lighten(col, 0.14), 0.0), (col, 0.45), (darken(col, 0.45), 1.0)]))
    _masonry(f, x - dw / 2, yb - base_h - dh, dw, dh, col, rs, course=16, blk=(30, 54))
    f.rect(x - dw / 2 - 5, yb - base_h - dh - 8, dw + 10, 12, color=darken(col, 0.12))
    for q in range(9):
        f.rect(x - dw / 2 + 8 + q * 26, yb - base_h - dh - 20, 14, 14, color=darken(col, 0.12))
    ty = yb - base_h - dh - 8
    tw, th = 120, 62
    f.rect(x - tw / 2, ty - th, tw, th, color=darken(col, 0.06))
    f.rect(x - tw / 2 - 4, ty - th - 6, tw + 8, 9, color=darken(col, 0.2))
    # melek: kanatlı siluet
    ay = ty - th - 6
    f.path(sk.smooth_path([(x - 5, ay), (x - 4, ay - 26), (x - 12, ay - 44), (x - 28, ay - 58), (x - 14, ay - 46), (x - 2, ay - 50), (x, ay - 62), (x + 2, ay - 50), (x + 14, ay - 46), (x + 28, ay - 58), (x + 12, ay - 44), (x + 4, ay - 26), (x + 5, ay)], True, 0.35), color="#0A0705")
    f.line(x + 6, ay - 52, x + 30, ay - 70, color="#0A0705", sw=2.0)
    if lit:
        for q in range(5):
            f.rect(x - 90 + q * 45, yb - base_h - dh * 0.55, 6, 14, color="#FFC770")
            PW.glow_add(f, x - 87 + q * 45, yb - base_h - dh * 0.55 + 6, 16, "#FFB347", 0.6)
    _meta_add("flags", (x, ay - 70, "#D4B64E"))


def _spire_stephan(f, x, yb, T, city, lit_dir, rs):
    """Stephansdom: sivri kule (süslü), yüksek mozaik çatılı nef."""
    col = _stone(city, T, 0.14, shade=0.2)
    # nef + mozaik çatı
    nw, nh = 330, 70
    f.rect(x - 380, yb - nh, nw + 120, nh, color=darken(col, 0.05))
    roof_c = mix("#3E4A4A", T["haze"], 0.12)
    f.poly([(x - 396, yb - nh), (x - 330, yb - nh - 150), (x - 80, yb - nh - 150), (x - 20, yb - nh)], color=roof_c)
    f.c.save()
    f.c.clipPath(sk.poly_path([(x - 396, yb - nh), (x - 330, yb - nh - 150), (x - 80, yb - nh - 150), (x - 20, yb - nh)], True), skia.ClipOp.kIntersect, True)
    for q in range(10):
        for r in range(8):
            pts = [(x - 396 + q * 40 + (r % 2) * 20, yb - nh - 6 - r * 19), (x - 376 + q * 40 + (r % 2) * 20, yb - nh - 16 - r * 19), (x - 356 + q * 40 + (r % 2) * 20, yb - nh - 6 - r * 19)]
            f.path(sk.poly_path(pts, False), style="stroke", sw=1.6, color=lighten(roof_c, 0.28), alpha=0.55)
    f.c.restore()
    # güney kule
    bw = 74
    f.rect(x - bw / 2, yb - 260, bw, 260, shader=f.lin(x - bw / 2, 0, x + bw / 2, 0, [(lighten(col, 0.1), 0.0), (col, 0.5), (darken(col, 0.4), 1.0)]))
    _masonry(f, x - bw / 2, yb - 260, bw, 260, col, rs, course=15, blk=(22, 36))
    for q in range(4):
        f.rect(x - bw / 2 + 12, yb - 120 - q * 48, 8, 26, color="#0A0705", alpha=0.7)
        f.rect(x + bw / 2 - 20, yb - 120 - q * 48, 8, 26, color="#0A0705", alpha=0.7)
    f.rect(x - bw / 2 - 5, yb - 262, bw + 10, 10, color=darken(col, 0.15))
    # sivri tepe (içbükey profil + kabarcıklar)
    pts_l = [(x - 34, yb - 262), (x - 30, yb - 330), (x - 22, yb - 390), (x - 12, yb - 450), (x - 4, yb - 500), (x, yb - 530)]
    pts_r = [(x + 34, yb - 262), (x + 30, yb - 330), (x + 22, yb - 390), (x + 12, yb - 450), (x + 4, yb - 500), (x, yb - 530)]
    f.path(sk.poly_path(pts_l + pts_r[::-1], True), shader=f.lin(x - 34, 0, x + 34, 0, [(lighten(col, 0.12), 0.0), (col, 0.5), (darken(col, 0.4), 1.0)]))
    for (px, py) in pts_l[1:-1]:
        f.poly([(px, py), (px - 7, py + 6), (px, py + 14)], color=col)
    for (px, py) in pts_r[1:-1]:
        f.poly([(px, py), (px + 7, py + 6), (px, py + 14)], color=col)
    f.line(x, yb - 530, x, yb - 566, color="#0A0705", sw=2.4)
    f.line(x - 6, yb - 556, x + 6, yb - 556, color="#0A0705", sw=2.4)
    _meta_add("flags", (x + 120, yb - 150, "#C9962B"))


def _pyramid(f, cx, yb, w, h, tiers, T, city, lit_dir, rs, temple=True):
    """Basamaklı piramit: kademeler + ortada çift merdiven + üstte iki tapınak (Templo Mayor)."""
    col = _stone(city, T, 0.10)
    th = h / tiers
    for i in range(tiers):
        ww = w * (1 - i * 0.14)
        y1 = yb - i * th
        f.rect(cx - ww / 2, y1 - th, ww, th, shader=f.lin(0, y1 - th, 0, y1, [(lighten(col, 0.10), 0.0), (darken(col, 0.18 + 0.05 * i), 1.0)]))
        f.rect(cx - ww / 2, y1 - th, ww, 3, color=lighten(col, 0.18), alpha=0.8)
        sx = cx + (ww / 2 - ww * 0.22) if lit_dir < 0 else cx - ww / 2
        f.rect(sx, y1 - th, ww * 0.22, th, color="#000000", alpha=0.22)
        for q in range(int(ww / 44)):
            f.line(cx - ww / 2 + 20 + q * 44, y1 - th + 6, cx - ww / 2 + 20 + q * 44, y1 - 6, color="#000000", sw=1.0, alpha=0.14)
    # ortadaki merdiven
    sw = w * 0.16
    f.poly([(cx - sw, yb), (cx - sw * 0.5, yb - h), (cx + sw * 0.5, yb - h), (cx + sw, yb)], color=lighten(col, 0.16))
    for q in range(int(h / 11)):
        yy = yb - q * 11 - 3
        wq = sw * (1 - 0.5 * (yb - yy) / h)
        f.line(cx - wq, yy, cx + wq, yy, color="#000000", sw=1.0, alpha=0.20)
    f.line(cx - sw, yb, cx - sw * 0.5, yb - h, color=darken(col, 0.3), sw=3.0)
    f.line(cx + sw, yb, cx + sw * 0.5, yb - h, color=darken(col, 0.3), sw=3.0)
    if temple:
        ty = yb - h
        tw = w * (1 - tiers * 0.14) * 0.9
        for sgn, tc in ((-1, "#B33A2C"), (1, "#3E78A8")):
            tx = cx + sgn * tw * 0.26
            f.rect(tx - tw * 0.17, ty - 70, tw * 0.34, 70, color=mix(col, "#000000", 0.05))
            f.rect(tx - tw * 0.17, ty - 70, tw * 0.34, 12, color=tc)
            f.rect(tx - tw * 0.2, ty - 82, tw * 0.4, 14, color=darken(col, 0.1))
            f.poly([(tx - tw * 0.2, ty - 82), (tx, ty - 104), (tx + tw * 0.2, ty - 82)], color=darken(col, 0.18))
            f.rect(tx - 7, ty - 54, 14, 54, color="#0A0705", alpha=0.85)
            _meta_add("flags", (tx, ty - 104, tc))
        _meta_add("fires", (cx, ty - 40, 0.5))


def _plain_house_cluster(f, x0, x1, yb, T, city, lit_dir, rs, lit, fire, rows=2, hmin=26, hmax=64):
    for r in range(rows):
        _skyline(f, x0 + r * 17, x1, yb - r * 18, hmin - r * 5, hmax - r * 8, T, city, lit_dir, rs, lit, fire if r == 0 else fire * 0.5, wall_k=0.22 + 0.1 * r)


# ───────────────────────────── şehir üreticileri ─────────────────────────────
def build_roma(f, T, lit_dir, rs, fire):
    city = "roma"
    lit = T["lit"]
    yb = CITY_BASE
    # tepeler/arka silüet
    _ridge(f, yb - 150, 40, mix("#3C3024", T["haze"], 0.45), 31, wl=0.003, bottom=yb + 30)
    # şehir evleri (surun arkası, surdan yüksek)
    _plain_house_cluster(f, -240, 2160, yb - 52, T, city, lit_dir, rs, lit, fire, rows=3, hmin=70, hmax=190)
    # Eski Aziz Petrus
    bx = 640
    col = _stone(city, T, 0.16, 0.15)
    f.rect(bx - 190, yb - 52 - 140, 380, 140, shader=f.lin(0, yb - 192, 0, yb - 52, [(lighten(col, 0.1), 0.0), (darken(col, 0.3), 1.0)]))
    f.poly([(bx - 205, yb - 192), (bx, yb - 292), (bx + 205, yb - 192)], color=mix("#3A2622", T["haze"], 0.12))
    for q in range(8):
        f.path(sk.smooth_path([(bx - 168 + q * 48, yb - 60), (bx - 168 + q * 48, yb - 120), (bx - 156 + q * 48, yb - 132), (bx - 144 + q * 48, yb - 120), (bx - 144 + q * 48, yb - 60)], True, 0.3), color="#0A0705", alpha=0.75)
    f.rect(bx + 215, yb - 52 - 270, 54, 270, shader=f.lin(bx + 215, 0, bx + 269, 0, [(lighten(col, 0.1), 0.0), (darken(col, 0.38), 1.0)]))
    f.poly([(bx + 209, yb - 322), (bx + 242, yb - 400), (bx + 275, yb - 322)], color=mix("#3A2622", T["haze"], 0.1))
    f.line(bx + 242, yb - 400, bx + 242, yb - 424, color="#0A0705", sw=2.4)
    f.line(bx + 233, yb - 414, bx + 251, yb - 414, color="#0A0705", sw=2.4)
    # Castel Sant'Angelo
    _sant_angelo(f, 1480, yb - 40, T, city, lit_dir, rs, lit)
    # Aurelius surları + kuleler + kapı
    wall(f, -260, 2180, yb, 150, T, city, lit_dir, rs, k=0.06)
    for tx, th in ((130, 215), (470, 205), (820, 220), (1500, 210), (1840, 212)):
        tower(f, tx, yb, 86, th, T, city, lit_dir, rs, kind="square", roof="flat")
    for tx in (1120, 1250):
        tower(f, tx, yb, 74, 200, T, city, lit_dir, rs, kind="round", roof="flat")
    _arch_gate(f, 1185, yb, 64, 98, T, _stone(city, T))
    # savunucular
    for q in range(16):
        x = -150 + q * 140 + rs.rand() * 60
        _meta_add("defenders", (x, yb - 150 - 3, 1 if rs.rand() > 0.5 else -1))
    for q in range(3):
        _meta_add("flags", (130 + q * 700, yb - 215 - 70, "#D4B64E"))


def build_viyana(f, T, lit_dir, rs, fire):
    city = "viyana"
    lit = T["lit"]
    yb = CITY_BASE
    _ridge(f, yb - 120, 34, mix("#2E3A26", T["haze"], 0.42), 41, wl=0.0034, bottom=yb + 30)
    # şehir (tepe üstünde, sağda uzanan yamaç)
    _plain_house_cluster(f, -120, 1720, yb - 40, T, city, lit_dir, rs, lit, fire, rows=3, hmin=60, hmax=150)
    _spire_stephan(f, 960, yb - 70, T, city, lit_dir, rs)
    # surlar: sol parça + bastiyonlar + kapı kulesi
    wall(f, -260, 1760, yb, 118, T, city, lit_dir, rs, k=0.07)
    for bxx in (260, 1060):
        col = _stone(city, T, 0.07)
        w1, w2, h = 180, 96, 138
        f.poly([(bxx - w1, yb), (bxx - w1 + 24, yb - h), (bxx + 14, yb - h), (bxx + 12, yb)], color=lighten(col, 0.08))       # aydınlık yüz
        f.poly([(bxx + 12, yb), (bxx + 14, yb - h), (bxx + 14 + w2, yb - h + 8), (bxx + w2 - 6, yb)], color=darken(col, 0.38))  # gölge yüz
        _masonry(f, bxx - w1 + 12, yb - h, w1 + w2 - 12, h, col, rs, course=14, blk=(28, 50), dark=0.16)
        _merlons(f, bxx - w1 + 24, bxx + 14 + w2, yb - h + 2, col, shade="#000000")
        f.rect(bxx - w1 + 24, yb - 26, w1 + w2, 26, shader=f.lin(0, yb - 26, 0, yb, [("#000000", 0.0, 0), ("#000000", 1.0, 70)]))
        for q in range(2):
            _meta_add("defenders", (bxx - 60 + q * 70, yb - h - 3, 1))
    tower(f, 1760, yb, 96, 210, T, city, lit_dir, rs, kind="square", roof="cone")
    for tx in (-60, 600, 1400):
        tower(f, tx, yb, 70, 175, T, city, lit_dir, rs, kind="round", roof="cone")
    _arch_gate(f, 600, yb, 56, 82, T, _stone(city, T))
    for q in range(14):
        x = -150 + q * 130 + rs.rand() * 60
        _meta_add("defenders", (x, yb - 118 - 3, 1 if rs.rand() > 0.5 else -1))
    _meta_add("flags", (260, yb - 138 - 70, "#B02A2A"))
    _meta_add("flags", (1060, yb - 138 - 70, "#B02A2A"))


def build_guns(f, T, lit_dir, rs, fire):
    city = "guns"
    lit = T["lit"]
    yb = CITY_BASE
    _ridge(f, yb - 100, 34, mix("#2A3622", T["haze"], 0.42), 51, wl=0.0030, bottom=yb + 30)
    # kaya/tepe
    hill = [(-300, yb + 10), (200, yb - 20), (520, yb - 70), (760, yb - 150), (900, yb - 250), (960, yb - 312), (1020, yb - 330), (1430, yb - 330), (1490, yb - 312), (1550, yb - 250), (1700, yb - 150), (1900, yb - 80), (2200, yb - 20), (2300, yb + 10)]
    f.path(sk.smooth_path(hill + [(2300, yb + 120), (-300, yb + 120)], True, 0.3), shader=f.lin(0, yb - 340, 0, yb + 24, [(mix(CITIES[city]["ground2"], T["haze"], 0.32), 0.0), (mix(CITIES[city]["ground"], T["haze"], 0.44), 0.85), (mix(CITIES[city]["ground"], T["haze"], 0.50), 1.0)]))
    hx = lambda x: float(np.interp(x, [p[0] for p in hill], [p[1] for p in hill]))
    for q in range(60):
        x = -240 + rs.rand() * 2400
        y = hx(x) + 6 + rs.rand() * 24
        hh = 26 + rs.rand() * 36
        for k in range(3):
            f.poly([(x - hh * 0.2 * (1 - k * 0.2), y - k * hh * 0.22), (x, y - hh * (k * 0.22 + 0.4)), (x + hh * 0.2 * (1 - k * 0.2), y - k * hh * 0.22)], color=mix("#101A0E", T["haze"], 0.12))
    # köy evleri yamaçta
    for q in range(26):
        x = 640 + q * 34 + rs.randn() * 10
        if 940 < x < 1460:
            continue
        y = hx(x) + 22 + rs.rand() * 18
        _house2(f, x, y, 28 + rs.rand() * 20, 22 + rs.rand() * 14, 14, _stone(city, T, 0.2), mix(CITIES[city]["roof"], T["haze"], 0.1), T, lit_dir, rs, lit=lit, burn=1.0 if rs.rand() < fire * 0.25 else 0.0)
    # kale: sur + iki kule + donjon + şapel
    ty = hx(1200) + 18
    # kaya şevleri: tepe omuzlarında tabakalı kaya çizgileri
    hp_ = sk.smooth_path(hill + [(2300, yb + 120), (-300, yb + 120)], True, 0.3)
    f.c.save()
    f.c.clipPath(hp_, skia.ClipOp.kIntersect, True)
    for q in range(34):
        x = 880 + q * 22 + rs.rand() * 10
        y = hx(x)
        f.line(x, y + 4, x + (rs.rand() - 0.5) * 18, y + 60 + rs.rand() * 60, color="#000000", sw=1.6, alpha=0.20)
    for q in range(6):
        f.line(860, yb - 300 + q * 26, 1560, yb - 296 + q * 26, color=mix(CITIES[city]["stone2"], "#000000", 0.4), sw=1.6, alpha=0.14)
    f.c.restore()
    wall(f, 950, 1450, ty + 10, 96, T, city, lit_dir, rs, k=0.07)
    tower(f, 960, ty + 10, 80, 170, T, city, lit_dir, rs, kind="round", roof="cone")
    tower(f, 1440, ty + 10, 80, 170, T, city, lit_dir, rs, kind="round", roof="cone")
    tower(f, 1200, ty - 40, 120, 190, T, city, lit_dir, rs, kind="square", roof="cone")
    f.rect(1052, ty - 120, 40, 120, color=_stone(city, T, 0.1))
    f.poly([(1046, ty - 120), (1072, ty - 188), (1098, ty - 120)], color=mix(CITIES[city]["roof"], T["haze"], 0.1))
    f.line(1072, ty - 188, 1072, ty - 206, color="#0A0705", sw=2.0)
    f.line(1066, ty - 198, 1078, ty - 198, color="#0A0705", sw=2.0)
    for q in range(8):
        _meta_add("defenders", (970 + q * 62, ty + 10 - 96 - 3, 1 if q % 2 else -1))
    _meta_add("flags", (1200, ty - 40 - 190 - 100, "#B02A2A"))
    if fire > 0.1:
        _meta_add("fires", (1200, ty - 120, 0.6 + 0.5 * fire))
        _meta_add("fires", (1380, ty - 40, 0.5))


def build_halkulvadi(f, T, lit_dir, rs, fire):
    city = "halkulvadi"
    lit = T["lit"]
    yb = CITY_BASE
    col = _stone(city, T, 0.14)
    # uzak kıyı + minareler (Tunus yönü, sisli)
    _ridge(f, yb - 70, 22, mix("#6A5A3C", T["haze"], 0.60), 61, wl=0.0034, bottom=yb + 30)
    for q, (mx, mh) in enumerate(((220, 120), (380, 90), (520, 140), (700, 100))):
        c2 = mix("#7A6A4A", T["haze"], 0.62)
        f.rect(mx - 5, yb - 70 - mh, 10, mh, color=c2)
        f.poly([(mx - 8, yb - 70 - mh), (mx, yb - 70 - mh - 30), (mx + 8, yb - 70 - mh)], color=c2)
        f.rect(mx - 38, yb - 100, 76, 36, color=c2)
        f.oval(mx, yb - 100, 30, 24, color=c2)
    # kumsal şeridi (kıyı)
    f.path(sk.smooth_path([(-300, yb + 18), (200, yb + 4), (700, yb - 4), (1100, yb - 8), (1400, yb - 6), (1900, yb - 2), (2300, yb + 6), (2300, yb + 80), (-300, yb + 80)], True, 0.4), color=mix(CITIES[city]["ground"], T["haze"], 0.30))
    # kale (kare, bastiyonlu, eğimli taban)
    fx0, fx1, fh = 1060, 1700, 150
    f.poly([(fx0 - 60, yb + 6), (fx0 - 20, yb - 30), (fx1 + 20, yb - 30), (fx1 + 60, yb + 6)], color=darken(col, 0.38))    # talus
    wall(f, fx0 - 20, fx1 + 20, yb - 26, fh, T, city, lit_dir, rs, k=0.08)
    for tx in (fx0, 1240, 1520, fx1):
        tower(f, tx, yb - 26, 100, fh + 62, T, city, lit_dir, rs, kind="square", roof="flat")
    tower(f, 1380, yb - 46, 120, fh + 100, T, city, lit_dir, rs, kind="square", roof="flat")
    _arch_gate(f, 1380, yb - 26, 54, 80, T, col)
    for q in range(10):
        x = fx0 + 40 + q * 62 + rs.rand() * 14
        _meta_add("defenders", (x, yb - 26 - fh - 3, 1 if q % 2 else -1))
    for tx in (fx0, fx1):
        _meta_add("flags", (tx, yb - 26 - fh - 62 - 4, "#2F6B4A"))
    _meta_add("flags", (1380, yb - 46 - fh - 100 - 4, "#2F6B4A"))
    # topluca mazgal topları
    if fire > 0.05:
        _meta_add("fires", (1240, yb - 26 - fh - 40, 0.55 + 0.5 * fire))
        _meta_add("fires", (1520, yb - 26 - fh - 20, 0.5 + 0.4 * fire))


def build_tenochtitlan(f, T, lit_dir, rs, fire):
    city = "tenochtitlan"
    lit = T["lit"]
    yb = CITY_BASE
    col = _stone(city, T, 0.12)
    # çevre kıyı (uzak, düşük) + dikilmiş ağaç kümeleri
    _ridge(f, yb - 40, 16, mix("#2E4026", T["haze"], 0.55), 71, wl=0.004, bottom=yb + 30)
    # ada: alçak taban
    f.path(sk.smooth_path([(180, yb + 14), (420, yb - 6), (900, yb - 12), (1500, yb - 10), (1820, yb - 4), (1900, yb + 14)], False, 0.4), style="stroke", sw=8, color=darken(col, 0.4))
    # düz çatılı beyaz evler (teraslar)
    for r in range(3):
        x = 250 + r * 22
        while x < 1760 - r * 18:
            w = 36 + rs.rand() * 44
            h = 22 + rs.rand() * 36 + (2 - r) * 6
            wc = mix(_stone(city, T, 0.14 + 0.08 * r, shade=rs.rand() * 0.4), "#000000", 0.0)
            yy = yb - 2 - r * 14
            f.rect(x, yy - h, w, h, color=wc)
            f.rect(x + w * 0.62, yy - h, w * 0.38, h, color="#000000", alpha=0.22)
            f.rect(x - 2, yy - h - 3, w + 4, 4, color=lighten(wc, 0.12))
            if rs.rand() > 0.6 and (lit or fire > 0):
                burn = rs.rand() < fire * 0.4
                f.rect(x + w * 0.4, yy - h * 0.6, 5, 8, color="#FFB045" if burn else "#FFC770")
                PW.glow_add(f, x + w * 0.4 + 2, yy - h * 0.6 + 4, 14, "#FF9A2E" if burn else "#FFB347", 0.6)
                if burn:
                    _meta_add("fires", (x + w * 0.5, yy - h - 4, 0.5 + 0.5 * fire))
            x += w * (0.85 + 0.25 * rs.rand())
    # piramitler
    _pyramid(f, 520, yb - 4, 250, 170, 4, T, city, lit_dir, rs, temple=False)
    _pyramid(f, 1530, yb - 4, 270, 200, 4, T, city, lit_dir, rs, temple=False)
    _pyramid(f, 1010, yb - 2, 520, 330, 5, T, city, lit_dir, rs, temple=True)
    # ağaç (ahuehuete) kümeleri
    for tx in (330, 760, 1260, 1700):
        for q in range(3):
            f.circle(tx + q * 20 - 20, yb - 30 - q % 2 * 8, 17 + q * 2, color=mix("#1E3220", T["haze"], 0.42))
    # savunucular piramit basamaklarında + sancaklar
    for q in range(10):
        _meta_add("defenders_small", (850 + q * 36 + rs.rand() * 10, yb - 2 - (q % 5) * 66 - 62, 1 if q % 2 else -1))
    # setyolları (uzun, düz toprak yollar): sol ve sağ kıyıya
    for x0_, x1_ in ((-300, 260), (1760, 2300)):
        f.rect(x0_, yb + 4, x1_ - x0_, 7, color=darken(col, 0.4))
        for q in range(int((x1_ - x0_) / 120)):
            f.rect(x0_ + 40 + q * 120, yb + 10, 14, 4, color="#000000", alpha=0.4)
    if fire > 0.05:
        _meta_add("fires", (1010, yb - 330 - 44, 0.6 * fire + 0.3))


def build_toledo(f, T, lit_dir, rs, fire):
    city = "toledo"
    lit = T["lit"]
    yb = CITY_BASE
    col = _stone(city, T, 0.12)
    _ridge(f, yb - 90, 30, mix("#4A3C28", T["haze"], 0.52), 81, wl=0.0030, bottom=yb + 30)
    hill = [(-300, yb + 20), (200, yb - 10), (500, yb - 70), (760, yb - 170), (940, yb - 290), (1100, yb - 360), (1260, yb - 330), (1420, yb - 240), (1600, yb - 130), (1900, yb - 40), (2300, yb + 20)]
    hy = lambda x: float(np.interp(x, [p[0] for p in hill], [p[1] for p in hill]))
    f.path(sk.smooth_path(hill + [(2300, yb + 120), (-300, yb + 120)], True, 0.35), shader=f.lin(0, yb - 360, 0, yb + 24, [(mix(CITIES[city]["ground2"], T["haze"], 0.3), 0.0), (mix(CITIES[city]["ground"], T["haze"], 0.44), 0.85), (mix(CITIES[city]["ground"], T["haze"], 0.50), 1.0)]))
    # yığılı şehir evleri
    for r in range(8):
        for q in range(110):
            x = -200 + rs.rand() * 2400
            yy = hy(x) + 6 + r * 18 + rs.rand() * 12
            if yy > yb + 12:
                continue
            w = 22 + rs.rand() * 36
            h = 18 + rs.rand() * 30
            _house2(f, x, yy, w, h, 8 + rs.rand() * 12, _stone(city, T, 0.18 + 0.05 * r, shade=rs.rand() * 0.5), mix(CITIES[city]["roof"], T["haze"], 0.1), T, lit_dir, rs, lit=lit, burn=1.0 if rs.rand() < fire * 0.12 else 0.0, win=(rs.rand() > 0.5))
    # Alcázar: büyük kare blok + dört köşe kulesi
    ax, ay = 1130, hy(1130) + 10
    f.rect(ax - 150, ay - 130, 300, 130, shader=f.lin(0, ay - 130, 0, ay, [(lighten(col, 0.1), 0.0), (darken(col, 0.3), 1.0)]))
    _masonry(f, ax - 150, ay - 130, 300, 130, col, rs, course=15)
    for sx in (-150, 150):
        tower(f, ax + sx, ay, 64, 210, T, city, lit_dir, rs, kind="square", roof="cone")
    for sx in (-60, 60):
        tower(f, ax + sx, ay, 50, 170, T, city, lit_dir, rs, kind="square", roof="cone")
    f.rect(ax - 142, ay - 142, 284, 14, color=darken(col, 0.14))
    for q in range(5):
        f.rect(ax - 100 + q * 50, ay - 100, 8, 22, color="#0A0705", alpha=0.7)
    _meta_add("flags", (ax - 150, ay - 210 - 64 * 0.95 - 20, "#8E1F26"))
    # katedral çan kulesi
    cx_ = 860
    cy_ = hy(cx_) + 12
    f.rect(cx_ - 26, cy_ - 220, 52, 220, shader=f.lin(cx_ - 26, 0, cx_ + 26, 0, [(lighten(col, 0.1), 0.0), (darken(col, 0.38), 1.0)]))
    _masonry(f, cx_ - 26, cy_ - 220, 52, 220, col, rs, course=14, blk=(18, 30))
    f.poly([(cx_ - 32, cy_ - 220), (cx_, cy_ - 320), (cx_ + 32, cy_ - 220)], color=mix(CITIES[city]["roof"], T["haze"], 0.1))
    f.line(cx_, cy_ - 320, cx_, cy_ - 346, color="#0A0705", sw=2.4)
    f.line(cx_ - 7, cy_ - 336, cx_ + 7, cy_ - 336, color="#0A0705", sw=2.4)
    # sur: yamaç boyunca basamaklı parçalar + uç kuleler
    for x0_ in range(300, 900, 52):
        wall(f, x0_, x0_ + 54, hy(x0_ + 27) + 16, 64, T, city, lit_dir, rs, k=0.1, slits=False, light=False)
    for x0_ in range(1480, 1990, 52):
        wall(f, x0_, x0_ + 54, hy(x0_ + 27) + 16, 64, T, city, lit_dir, rs, k=0.1, slits=False, light=False)
    tower(f, 1980, hy(1980) + 16, 70, 130, T, city, lit_dir, rs, kind="round", roof="cone")
    tower(f, 290, hy(290) + 16, 70, 130, T, city, lit_dir, rs, kind="round", roof="cone")
    for q in range(10):
        x = 330 + q * 54
        _meta_add("defenders_small", (x, hy(x + 20) + 16 - 66, 1))
    # yamaç sıraları (terasların çizgileri)
    for r in range(5):
        pts = [(x, hy(x) + 34 + r * 26) for x in range(-300, 2300, 80)]
        f.path(sk.smooth_path(pts, False, 0.4), style="stroke", sw=2.0, color=darken(col, 0.5), alpha=0.22)


BUILDERS = dict(roma=build_roma, viyana=build_viyana, guns=build_guns, halkulvadi=build_halkulvadi, tenochtitlan=build_tenochtitlan, toledo=build_toledo)


def _apron(f, city, T, rs):
    """Şehir tabanı ile orta zemin arasındaki boşluğu dolduran zemin/su önlüğü (şehir katmanı koordinatında)."""
    C_ = CITIES[city]
    y_a, y_b = CITY_BASE - 24, 1000
    if city in ("tenochtitlan", "halkulvadi"):
        c_top, c_bot = _water_cols(T)
        f.rect(-MARGIN, y_a, W + 2 * MARGIN, y_b - y_a, shader=f.lin(0, y_a, 0, y_b, [(mix(c_top, T["haze"], 0.22), 0.0), (c_bot, 1.0)]))
        # kentin suya yansıması (silik dikey çizgiler) + kıyı gölgesi
        r_ = RS(77)
        x_lo, x_hi = (200, 1860) if city == "tenochtitlan" else (1000, 1760)
        for q in range(70):
            x = x_lo + r_.rand() * (x_hi - x_lo)
            hh = 10 + r_.rand() * 46
            f.rect(x, CITY_BASE + 6, 3 + r_.rand() * 8, hh, color=mix(_stone(city, T, 0.1), T["haze"], 0.3), alpha=0.16 + 0.1 * r_.rand())
        f.rect(-MARGIN, CITY_BASE + 4, W + 2 * MARGIN, 34, shader=f.lin(0, CITY_BASE + 4, 0, CITY_BASE + 38, [("#000000", 0.0, 80), ("#000000", 1.0, 0)]))
        if city == "halkulvadi":
            col = mix(C_["ground2"], C_["ground"], 0.45)
            col = mix(col, T["haze"], 0.28)
            f.path(sk.smooth_path([(880, CITY_BASE - 40), (1000, CITY_BASE - 34), (1300, CITY_BASE - 30), (1740, CITY_BASE - 34), (1900, CITY_BASE - 14), (1980, CITY_BASE + 30), (1700, CITY_BASE + 70), (1200, CITY_BASE + 80), (900, CITY_BASE + 56), (830, CITY_BASE + 10)], True, 0.45), color=col)
            f.path(sk.smooth_path([(830, CITY_BASE + 10), (900, CITY_BASE + 56), (1200, CITY_BASE + 80), (1700, CITY_BASE + 70), (1980, CITY_BASE + 30)], False, 0.45), style="stroke", sw=4, color=T["haze"], alpha=0.5)
    else:
        a = mix(C_["ground"], T["haze"], 0.50)
        b = mix(C_["ground"], T["haze"], 0.30)
        f.rect(-MARGIN, y_a, W + 2 * MARGIN, y_b - y_a, shader=f.lin(0, y_a, 0, y_b, [(a, 0.0), (b, 1.0)]))
        tex = PW.streak_rgba(W + 2 * MARGIN, 300, 120, col="#000000", alpha=0.20, scale_x=360, scale_y=9, thr=0.56)
        f.c.drawImage(PW.img_from_rgba(tex), -MARGIN, y_a + 10, LIN, skia.Paint())
        # sur dibi hendeği (koyu çizgi) + toprak şev
        f.rect(-MARGIN, CITY_BASE - 2, W + 2 * MARGIN, 16, shader=f.lin(0, CITY_BASE - 2, 0, CITY_BASE + 14, [("#000000", 0.0, 90), ("#000000", 1.0, 0)]))
    f.rect(-MARGIN, y_a, W + 2 * MARGIN, 90, shader=f.lin(0, y_a, 0, y_a + 90, [(T["haze"], 0.0, 70), (T["haze"], 1.0, 0)]))


@lru_cache(maxsize=10)
def city_asset(city, time, weather, fire_q):
    """Şehir katmanı: (img, x, y, meta). fire_q: yangın (0..4, 0.25 adım)."""
    T = _time(time, weather)
    sun = T["sun"]
    lit_dir = -1 if (sun and sun[0] < 0.5) or (time == "night") else 1
    fire = fire_q / 4.0
    y0, hh = 90, 700
    meta = dict(fires=[], flags=[], defenders=[], defenders_small=[])
    _META["cur"] = meta
    rs = RS(1000 + len(city) * 31 + fire_q)

    def fn(f):
        BUILDERS[city](f, T, lit_dir, rs, fire)
    try:
        img = PW.bake_sprite(lambda f: (_apron(f, city, T, RS(5)), fn(f)), W + 2 * MARGIN, hh + 240, MARGIN, -y0, mip=False)
    finally:
        _META["cur"] = None
    return img, -MARGIN, y0, meta


# ───────────────────────────── zemin katmanları ─────────────────────────────
WATER_MID = ("halkulvadi", "tenochtitlan", "toledo")
WATER_NEAR = ("tenochtitlan",)
GUNS = dict(
    roma=dict(near=[430, 1010, 1520], mid=[260, 720, 1320, 1700]),
    viyana=dict(near=[380, 1000, 1560], mid=[210, 650, 1190, 1630]),
    guns=dict(near=[520, 1280], mid=[320, 820, 1500]),
    halkulvadi=dict(near=[300, 920, 1530], mid=[]),
    tenochtitlan=dict(near=[], mid=[]),
    toledo=dict(near=[420, 1020, 1530], mid=[260, 760, 1320, 1700]),
)
LADDERS = dict(roma=[(190, 215), (520, 545), (880, 905), (1560, 1585), (1890, 1915)], viyana=[(300, 325), (700, 722), (1120, 1145)], guns=[(1010, 1030), (1390, 1410)],
               halkulvadi=[(1100, 1120), (1300, 1320), (1620, 1640)], toledo=[(380, 400), (1600, 1620)], tenochtitlan=[])
ATT = dict(imperial=("landsknecht", "arquebusier", "halberdier", "pikeman"), ottoman=("janissary", "janissary", "janissary", "arquebusier"), spanish=("conquistador", "pikeman", "arquebusier", "halberdier"))


def _water_cols(T):
    return mix(T["haze"], "#3A5A6C", 0.64), mix("#0C1A24", T["haze"], 0.05)


def bake_ground(f, city, time, weather, k):
    T = _time(time, weather)
    C_ = CITIES[city]
    y_edge = MID_Y if k == 0 else NEAR_Y
    amp = 12 if k == 0 else 8
    rs = RS(2000 + k * 77 + len(city) * 13)
    xs = list(range(-MARGIN, W + MARGIN + 41, 40))
    edge = [(x, y_edge + amp * math.sin(x * 0.0021 + k) + amp * 0.5 * math.sin(x * 0.0067 + 2 * k)) for x in xs]
    ey = lambda x: y_edge + amp * math.sin(x * 0.0021 + k) + amp * 0.5 * math.sin(x * 0.0067 + 2 * k)
    water = (k == 0 and city in WATER_MID) or (k == 1 and city in WATER_NEAR)
    path = sk.smooth_path(edge + [(W + MARGIN, H + MARGIN + 100), (-MARGIN, H + MARGIN + 100)], True, 0.35)
    lit = T["lit"]
    if water:
        c_top, c_bot = _water_cols(T)
        if k == 1:
            c_top = mix(c_top, "#000000", 0.25)
        f.path(path, shader=f.lin(0, y_edge, 0, y_edge + 240, [(c_top, 0.0), (c_bot, 1.0)]))
        f.path(sk.smooth_path(edge, False, 0.35), style="stroke", sw=3, color=T["rim"], alpha=0.30)
        # kıyı kamışları
        if city in ("tenochtitlan", "toledo") and k == 1:
            for q in range(100):
                x = rs.rand() * (W + 2 * MARGIN) - MARGIN
                hh = 14 + rs.rand() * 36
                f.path(sk.smooth_path([(x, ey(x) + 4), (x + (rs.rand() - 0.5) * 8, ey(x) - hh * 0.5), (x + (rs.rand() - 0.5) * 16, ey(x) - hh)], False, 0.5), style="stroke", sw=1.5, color=mix("#0A100C", T["haze"], 0.1))
        sun = T["sun"]
        if sun and k == 0:
            PW.glow_add(f, sun[0] * W, y_edge + 50, 300, sun[4], 0.28, 200, 70, 0.3)
    else:
        col_a = mix(C_["ground"], T["haze"], 0.28 if k == 0 else 0.10)
        col_b = mix(C_["ground2"], T["haze"], 0.12 if k == 0 else 0.0)
        if weather == "rain":
            col_a, col_b = mix(col_a, "#1E2A24", 0.38), mix(col_b, "#0A100E", 0.3)
        if weather == "snow":
            col_a, col_b = mix(col_a, "#D4DADF", 0.7), mix(col_b, "#8896A2", 0.6)
        f.path(path, shader=f.lin(0, y_edge - 10, 0, y_edge + 240, [(col_a, 0.0), (col_b, 1.0)]))
        f.c.save()
        f.c.clipPath(path, skia.ClipOp.kIntersect, True)
        tex = PW.streak_rgba(W + 2 * MARGIN, 260, 90 + k, col="#000000", alpha=0.24, scale_x=340, scale_y=9, thr=0.55)
        f.c.drawImage(PW.img_from_rgba(tex), -MARGIN, y_edge - 20, LIN, skia.Paint())
        tex2 = PW.streak_rgba(W + 2 * MARGIN, 260, 95 + k, col=lighten(col_a, 0.4), alpha=0.14, scale_x=280, scale_y=7, thr=0.6)
        f.c.drawImage(PW.img_from_rgba(tex2), -MARGIN, y_edge - 10, LIN, skia.Paint())
        if weather == "rain":                                   # çamur birikintileri
            for q in range(16 + 8 * k):
                px = rs.rand() * (W + 2 * MARGIN) - MARGIN
                py = y_edge + 20 + rs.rand() * (60 + 60 * k)
                rx = 28 + rs.rand() * (50 + 30 * k)
                f.oval(px, py, rx, rx * 0.10, color=mix(T["haze"], "#1A2224", 0.4), alpha=0.6)
        f.c.restore()
        f.path(sk.smooth_path(edge, False, 0.35), style="stroke", sw=2.0 + k, color=T["rim"], alpha=0.30)
        dark = mix(col_b, "#000000", 0.4)
        att = C_["att"]
        if k == 0:
            # hendek: palisad + gabion sırası
            for seg in ((-200, 360), (560, 1010), (1130, 1520), (1640, 2150)):
                _palisade(f, seg[0], seg[1], ey(seg[0]) + 26, T, mix(dark, T["haze"], 0.08))
                _gabions(f, seg[0] + 10, seg[1] - 10, ey(seg[0]) + 54, T, rs, mix(dark, "#5A4A30", 0.3), h=22, w=19)
            # çadırlar
            xs_t = [90 + 210 * i + rs.randn() * 14 for i in range(9)]
            for i, x in enumerate(xs_t):
                if 640 < x < 1100 and city in ("viyana", "guns", "roma"):
                    continue
                yb = ey(x) + 66 + (i % 3) * 14
                if att == "ottoman":
                    colt = ("#2F6B4A", "#8E1F26", "#9A7A3A")[i % 3]
                    colt = mix(colt, T["haze"], 0.34)
                    _tent_ottoman(f, x, yb, 0.52 + 0.06 * (i % 2), mix(colt, "#000000", 0.0), "#C9962B", T, lit=lit)
                elif att == "imperial":
                    colt = ("#7A2A2A", "#B4A67E", "#5A4C34")[i % 3]
                    _tent_pavilion(f, x, yb, 0.5, mix(colt, T["haze"], 0.30), "#B88A3A", T, lit=lit)
                else:
                    _tent_small(f, x, yb, 0.9, mix("#8A7A5A", T["haze"], 0.2), T)
        else:
            for seg in ((-200, 330), (780, 1130), (1280, 1700)):
                _gabions(f, seg[0], seg[1], ey(seg[0]) + 46, T, rs, mix(dark, "#5A4A30", 0.3), h=34, w=28)
            for x in (180, 1790):
                yb = ey(x) + 110
                if att == "ottoman":
                    _tent_ottoman(f, x, yb, 1.05, mix("#2F6B4A" if x < 900 else "#8E1F26", T["haze"], 0.05), "#C9962B", T, lit=lit)
                elif att == "imperial":
                    _tent_pavilion(f, x, yb, 1.0, mix("#8E1F26" if x < 900 else "#C8BA8E", T["haze"], 0.05), "#C9962B", T, lit=lit)
                else:
                    _tent_small(f, x, yb, 1.5, mix("#8A7A5A", T["haze"], 0.1), T)
            for q in range(9):
                x = rs.rand() * (W + 2 * MARGIN) - MARGIN
                y = ey(x) + 30 + rs.rand() * 70
                kind = rs.rand()
                if kind < 0.4:
                    f.circle(x, y, 7 + 3 * rs.rand(), color=mix("#0A0705", T["haze"], 0.08))
                    f.circle(x + 12, y + 3, 7, color=mix("#0A0705", T["haze"], 0.08))
                elif kind < 0.7:
                    f.rect(x, y - 18, 26, 18, color=mix("#2A1C10", T["haze"], 0.1))
                    f.line(x, y - 9, x + 26, y - 9, color="#000000", sw=1.0, alpha=0.35)
                else:
                    ang = (rs.rand() - 0.5) * 0.6
                    f.line(x, y, x + math.sin(ang) * 70, y - math.cos(ang) * 70, color=mix("#0A0705", T["haze"], 0.08), sw=2.4)
    # derinlik buğusu
    fa = 0.22 if k == 0 else 0.08
    f.rect(-MARGIN, y_edge - 120, W + 2 * MARGIN, 190, shader=f.lin(0, y_edge - 120, 0, y_edge + 70, [(T["haze"], 0.0, 0), (T["haze"], 0.6, int(255 * fa)), (T["haze"], 1.0, 0)]))


@lru_cache(maxsize=12)
def ground_asset(city, time, weather, k):
    y0 = int((MID_Y if k == 0 else NEAR_Y) - 220)
    h = int(H + MARGIN + 100 - y0)

    def fn(f):
        bake_ground(f, city, time, weather, k)
    img = PW.bake_sprite(fn, W + 2 * MARGIN, h, MARGIN, -y0, mip=False)
    return img, -MARGIN, y0


@lru_cache(maxsize=5)
def fg_asset(city, time, weather):
    T = _time(time, weather)
    ytop = 880
    h = int(H + MARGIN + 100 - ytop)

    def fn(f):
        rs = RS(333)
        col = "#3A424A" if weather == "snow" else mix("#0A0F08", T["haze"], 0.05)
        y0 = H - 18
        f.rect(-MARGIN, y0 + 52, W + 2 * MARGIN, 500, color=col)
        for q in range(170):
            x = rs.rand() * (W + 2 * MARGIN) - MARGIN
            hh = 26 + rs.rand() * 84
            bx = x + (rs.rand() - 0.5) * 24
            f.path(sk.smooth_path([(x, y0 + 40), (x + (bx - x) * 0.5, y0 - hh * 0.5), (bx, y0 - hh)], False, 0.5), style="stroke", sw=1.6 + rs.rand() * 2.0, color=col)
        # saplanmış kazıklar / kırık mızraklar / gabion kenarları
        for q in range(7):
            x = rs.rand() * (W + 2 * MARGIN) - MARGIN
            hh = 90 + rs.rand() * 120
            ang = (rs.rand() - 0.5) * 0.5
            f.line(x, y0 + 40, x + math.sin(ang) * hh, y0 + 40 - math.cos(ang) * hh, color=col, sw=3.0 + rs.rand() * 2)
        for q in range(5):
            x = rs.rand() * (W + 2 * MARGIN) - MARGIN
            f.oval(x, y0 + 36, 36 + rs.rand() * 50, 12 + rs.rand() * 8, color=col)
    img = PW.bake_sprite(fn, W + 2 * MARGIN, h, MARGIN, -ytop, mip=False)
    return img, -MARGIN, ytop


# ───────────────────────────── dinamik: yangın, top, askerler, merdiven ─────────────────────────────
WALL_TOP = dict(roma=CITY_BASE - 150, viyana=CITY_BASE - 118, halkulvadi=CITY_BASE - 26 - 150)
LAD_BASE = dict(roma=CITY_BASE + 4, viyana=CITY_BASE + 4, halkulvadi=CITY_BASE - 22)
DEF_KINDS = dict(roma=("arquebusier", "halberdier"), viyana=("halberdier", "arquebusier"), guns=("halberdier", "arquebusier"), halkulvadi=("janissary", "arquebusier"),
                 toledo=("halberdier", "peasant"), tenochtitlan=("aztec_warrior",))
FIRE_PTS = {}


def _have(kind):
    return (kind in ST.FIGX) or (kind in ST.FIG)


def _fig(f, kind, x, y, h, col, rim, face=1, rot=0.0, shadow=0.0):
    if not _have(kind):
        kind = "pikeman"
    if shadow > 0:
        PW.shadow(f, x, y + 2, h * 0.30, h * 0.05, shadow)
    ST.figure(f, kind, x, y, float(int(h / 2) * 2), col=col, rim=rim, face=face, rot=rot)


def _fires(f, meta, t, fire, T, wind):
    pts = meta["fires"]
    if fire <= 0.02 or not pts:
        return
    n = int(math.ceil(len(pts) * min(1.0, fire * 0.75)))
    for i, (x, y, s) in enumerate(pts[:n]):
        sc = s * (0.45 + 0.5 * fire) * (0.8 + 0.4 * ((i * 7) % 5) / 4.0)
        PW.flame(f, x, y, sc, t, seed=i * 3 + 1, glow_a=0.9)
        if i % 2 == 0:
            PW.flame(f, x + 14 * sc, y + 3, sc * 0.7, t, seed=i * 3 + 2, glow_a=0.6)
        PW.glow(f, x, y - 30 * sc, 210 * sc, "#FF8A2E", 0.42 * T["fire_vis"])
    for i, (x, y, s) in enumerate(pts[:min(4, n)]):
        PW.smoke_column(f, x, y - 28 * s, t, n=9, h=340 * (0.6 + 0.7 * fire), w0=12, w1=52, col="#2A2018" if T["time"] != "day" else "#3A3028", a=0.40 * (0.5 + 0.5 * fire), rate=0.09, drift=-wind * 70, seed=i + 5, wobble=10)


def _defenders(f, meta, city, T, t):
    kinds = DEF_KINDS.get(city, ("halberdier",))
    col = mix("#0C0705", T["haze"], 0.30)
    rim = mix(T["rim"], T["haze"], 0.3)
    for i, (x, y, face) in enumerate(meta["defenders"]):
        _fig(f, kinds[i % len(kinds)], x, y + 2 - abs(math.sin(t * 0.9 + i)) * 1.0, 62, col, rim, face)
    for i, (x, y, face) in enumerate(meta["defenders_small"]):
        _fig(f, kinds[i % len(kinds)], x, y + 2, 46, col, rim, face)


def _flags_dyn(f, meta, T, t, wind, city=""):
    for i, (x, y, spec) in enumerate(meta["flags"]):
        col = spec if isinstance(spec, str) else "#8E1F26"
        emb = "crescent" if PW.is_green(col) else "cross"
        if city == "tenochtitlan":
            emb = "none"
            f.line(x, y + 4, x, y - 6, color="#0A0705", sw=2.2)
            PW.flag_cloth(f, x, y - 60, 52, 62, col, t, emblem="none", trim="#E8C25A", wind=-wind if wind else -1, seed=i, speed=3.0, cut="taper")
            for q in range(3):                       # tüy süsü (geometrik bant)
                yy = y - 56 + q * 18
                f.line(x + 6, yy, x + 44 * (1 if wind <= 0 else -1) * -1, yy + 2, color="#F0E2B8", sw=2.0, alpha=0.5)
            f.line(x, y - 62, x, y + 2, color="#0A0705", sw=2.4)
            continue
        f.line(x, y + 4, x, y - 6, color="#0A0705", sw=2.2)
        PW.flag_cloth(f, x, y - 54, 74, 44, col, t, emblem=emb, trim="#C9962B", wind=-wind if wind else -1, seed=i, speed=3.4, cut="swallow", emb="#F0E2B8")
        f.line(x, y - 56, x, y + 2, color="#0A0705", sw=2.4)


def _ladders(f, city, T, t, wind):
    if city not in WALL_TOP:
        return
    yt = WALL_TOP[city]
    yb = LAD_BASE[city]
    col = mix("#3A2614", T["haze"], 0.10)
    kind = ATT[CITIES[city]["att"]][0] if CITIES[city]["att"] in ATT else "landsknecht"
    if CITIES[city]["att"] == "ottoman":
        kind = "janissary"
    for li, (xb, xt) in enumerate(LADDERS.get(city, [])):
        f.line(xb - 6, yb, xt - 6, yt + 2, color=col, sw=3.0)
        f.line(xb + 6, yb, xt + 6, yt + 2, color=col, sw=3.0)
        nr = int((yb - yt) / 14)
        for q in range(nr):
            u = q / max(1, nr)
            f.line(xb + (xt - xb) * u - 6, yb - (yb - yt) * u, xb + (xt - xb) * u + 6, yb - (yb - yt) * u, color=col, sw=2.0)
        f.line(xb - 6, yb, xt - 6, yt + 2, color=T["rim"], sw=0.9, alpha=0.4)
        th = math.atan2(xt - xb, yb - yt) * 1.25
        for ci in range(3):
            u = (0.06 + (t * 0.03 + ci * 0.31 + li * 0.13) % 0.93)
            if u > 0.96:
                continue
            px = xb + (xt - xb) * u
            py = yb - (yb - yt) * u
            bob = -abs(math.sin(t * 3.0 + ci * 1.7 + li)) * 2.0
            _fig(f, kind, px, py + 4 + bob, 66, mix("#0C0705", T["haze"], 0.16), mix(T["rim"], T["haze"], 0.25), 1, rot=th)


def _gun(f, T, x, y, sc, face, t, rate, idx, wind, flash_list=None):
    ks = round(max(0.4, min(1.6, sc * 1.3)) * 8) / 8.0
    img, ox, oy, k = cannon_sprite(ks, mix("#0C0705", T["haze"], 0.1 + (0.2 if sc < 0.8 else 0.0)), mix(T["rim"], T["haze"], 0.2))
    if rate > 0.01:
        period = 5.2 / (0.25 + rate * 1.5)
        off = (idx * 1.37) % period
        age = (t - off) % period
        kk = int((t - off) // period)
    else:
        age, kk = 99.0, -1
    e = math.exp(-age * 7.0) if age < 1.0 else 0.0
    PW.shadow(f, x, y + 3, 120 * sc, 9 * sc, 0.40)
    f.c.save()
    f.c.translate(x - face * e * 16 * sc, y)
    f.c.scale(face * sc / k, sc / k)
    f.c.drawImage(img, -ox, -oy, LIN, skia.Paint())
    f.c.restore()
    mx, my = x + face * 128 * sc, y - 66 * sc
    if age < 0.14:
        ee = 1 - age / 0.14
        PW.glow(f, mx + face * 10 * sc, my, 110 * sc * (0.5 + ee), "#FFC66B", ee, 255, 140, 0.4)
        PW.glow(f, mx + face * 6 * sc, my, 40 * sc * (0.5 + ee), "#FFF1C4", ee)
    if 0 <= age < 6.0 and rate > 0.01:
        u = age / 6.0
        a = 0.62 * (1 - u) ** 1.2 * min(1.0, age * 3.5)
        col = _smoke_col_default(T)
        PW.puff(f, mx + face * (20 + age * 18) * sc + wind * age * 6, my - 12 * sc - age * 12 * sc, (22 + 100 * u ** 0.6) * sc, col, a, seed=kk + idx, rot=age * 0.2)
        PW.puff(f, mx + face * (6 + age * 10) * sc, my - 4 * sc - age * 8 * sc, (16 + 60 * u ** 0.6) * sc, col, a * 0.8, seed=kk + idx + 3, rot=-age * 0.25)
    if flash_list is not None and rate > 0.01 and kk >= 0:
        flash_list.append((idx, kk, off + kk * period))


def _impacts(f, city, T, t, events, wind):
    """Top mermisi isabetleri: sur üzerinde parlama + toz + moloz (şehir katmanı koordinatında)."""
    yt = WALL_TOP.get(city, CITY_BASE - 160)
    n = 0
    for (gi, kk, T0) in events:
        age = t - (T0 + 0.5)
        if age < 0 or age > 2.6 or n >= 7:
            continue
        n += 1
        rs = RS(gi * 131 + kk * 17 + 7)
        xi = 140 + rs.rand() * (W - 280)
        yi = yt + 14 + rs.rand() * (CITY_BASE - yt - 30)
        if age < 0.22:
            e = 1 - age / 0.22
            PW.glow(f, xi, yi, 80 * (0.6 + e), "#FFC66B", e)
            PW.glow(f, xi, yi, 26 * (0.6 + e), "#FFF1C4", e)
        u = age / 2.6
        PW.puff(f, xi + age * 4 * -wind, yi - age * 14, 30 + 90 * u ** 0.5, mix(_stone(city, T, 0.0), "#7A6A58", 0.4), 0.55 * (1 - u) ** 1.1, seed=gi + kk, rot=age)
        if age < 1.4:
            p_ = skia.Paint(AntiAlias=True, Color=C("#2A1C12", int(255 * (1 - age / 1.4))))
            for q in range(7):
                vx = (rs.rand() - 0.5) * 220
                vy = -90 - rs.rand() * 130
                f.c.drawRect(skia.Rect.MakeXYWH(xi + vx * age, yi + vy * age + 380 * age * age, 5, 4), p_)


def _wall_torches(f, meta, T, t, wind):
    """Sur üstü meşaleleri (dusk/night): periyodik sönüp yanar; sönünce ince duman izi bırakır."""
    if not T["lit"]:
        return
    pts = meta["defenders"][::2][:9] + meta["defenders_small"][::3][:4]
    for i, (x, y, face) in enumerate(pts):
        ph = t * 0.31 + i * 1.97
        cyc = math.sin(ph) + 0.55 * math.sin(ph * 2.3 + i)
        tx, ty = x + face * 13, y - 34
        f.line(tx, ty + 12, tx, ty - 2, color="#0A0705", sw=1.8)
        if cyc > -0.9:
            k = 1.0 if cyc > -0.55 else clamp((cyc + 0.9) / 0.35)
            PW.flame(f, tx, ty - 1, 0.30 * (0.8 + 0.2 * k), t, seed=i, glow_a=0.8 * k)
        else:
            PW.puff(f, tx + wind * 0.5, ty - 14 - (cyc + 1.4) * 10, 7, "#6A625A", 0.30, seed=i, rot=ph)


def _wall_fire(f, meta, T, t, rate, wind):
    """Savunucuların küçük ateşleri: sur tepesinde rastgele namlu parlaması + duman (cannon_fire > 0)."""
    pts = meta["defenders"]
    if not pts or rate <= 0.01:
        return
    n = len(pts)
    period = 2.4 / (0.3 + rate)
    for slot in range(4):
        off = slot * 0.61
        k = int((t - off) // period)
        for kk in (k - 1, k):
            if kk < 0:
                continue
            age = (t - off) - kk * period
            if age < 0 or age > 3.5:
                continue
            rs = RS(slot * 997 + kk * 31 + 3)
            x, y, face = pts[int(rs.rand() * n) % n]
            if age < 0.12:
                e = 1 - age / 0.12
                PW.glow(f, x + face * 14, y - 30, 34 * (0.6 + e), "#FFC66B", e)
            u = age / 3.5
            PW.puff(f, x + face * (14 + age * 6) + wind * age * 4, y - 30 - age * 8, 10 + 36 * u ** 0.6, _smoke_col_default(T), 0.5 * (1 - u) ** 1.2 * min(1.0, age * 4), seed=kk + slot, rot=age * 0.3)


def _campfires(f, pts, T, t, seed=0):
    day = T["bright"] > 0.99 and not T["lit"]
    for i, (x, y) in enumerate(pts):
        if day:
            PW.smoke_column(f, x, y - 4, t, n=4, h=120, w0=8, w1=34, col="#4A4038", a=0.35, rate=0.15, drift=24, seed=seed + i)
        else:
            PW.flame(f, x, y, 0.7, t, seed=seed + i * 2, glow_a=0.9)
            PW.sparks(f, x, y - 14, t, n=6, h=90, spread=24, seed=seed + i, size=1.6)


def _soldiers(f, city, T, t, layer, density, vis):
    att = ATT.get(CITIES[city]["att"], ATT["imperial"])
    col = mix("#0C0705", T["haze"], 0.0 if layer == "near" else 0.16)
    rim = mix(T["rim"], T["haze"], 0.0 if layer == "near" else 0.2)
    rs = RS(4040 + len(city) * 9 + (1 if layer == "near" else 0))
    if layer == "mid":
        n = int(16 * density)
        for i in range(n):
            x = 70 + (i + rs.rand() * 0.8) * (W - 140) / max(1, n)
            h = 120 + rs.rand() * 14
            y = MID_Y + 54 + rs.rand() * 26
            if vis and (x < vis[0] - 80 or x > vis[2] + 80):
                continue
            kind = att[int(rs.rand() * len(att)) % len(att)]
            face = 1 if rs.rand() > 0.45 else -1
            bob = -abs(math.sin(t * (2.2 + rs.rand()) + rs.rand() * 6)) * 1.6
            _fig(f, kind, x, y + bob, h, col, rim, face, shadow=0.35)
    else:
        xs = [250, 700, 1230, 1640, 980, 130]
        n = int(len(xs) * density)
        for i in range(n):
            x = xs[i] + rs.randn() * 20
            h = 215 + rs.rand() * 22
            y = NEAR_Y + 64 + (i % 2) * 22
            if vis and (x < vis[0] - 140 or x > vis[2] + 140):
                continue
            kind = att[i % len(att)]
            bob = -abs(math.sin(t * (1.8 + 0.3 * i) + i)) * 2.4
            _fig(f, kind, x, y + bob, h, col, rim, 1 if i % 2 else -1, shadow=0.42)


def _canoe(f, T, x, y, s, t, idx, face):
    col = mix("#0C0705", T["haze"], 0.12)
    rim = mix(T["rim"], T["haze"], 0.2)
    bob = math.sin(t * 1.1 + idx * 1.7) * 2.0
    f.c.save()
    f.c.translate(x, y + bob)
    f.c.scale(face * s, s)
    hull = sk.smooth_path([(-62, -10), (-46, 2), (0, 6), (46, 2), (64, -12), (46, -6), (0, -2), (-46, -6)], True, 0.35)
    f.path(hull, color=col)
    f.line(-60, -12, 62, -14, color=rim, sw=1.0, alpha=0.5)
    f.c.restore()
    for q, dx in enumerate((-30, 0, 30)):
        _fig(f, "aztec_warrior" if _have("aztec_warrior") else "native", x + face * dx * s, y + bob - 4 * s, 66 * s, col, rim, face)
    g = PW.glow_sprite(64, T["haze"], 200, 90, 0.5)
    pf = skia.Paint()
    pf.setAlphaf(0.30)
    f.c.save()
    f.c.translate(x, y + bob + 3)
    f.c.scale(70 * s / 64.0, 4.0 * s / 64.0 * 2)
    f.c.drawImage(g, -64, -64, LIN, pf)
    f.c.restore()


def _ship_at(f, T, tt, kind, x, yw, s, t, flag, idx, gun=0.0, heading=1, sails="full", burn=0.0):
    """Gemi: scenes_sea.draw_ship'i (row 0 y'sini geçici ayarlayarak) yeniden kullanır."""
    import scenes_sea as SSea
    mood = {"day": "calm", "dusk": "dusk", "night": "night"}.get(tt, "calm")
    M = SSea.MOODS[mood]
    sh = SSea._ship_defaults(M, mood, dict(kind=kind, x=x / W, row=0, s=s, flag=flag, heading=heading, rock=0.35, gun=gun, sails=sails, burn=burn, drift=0.0, clip=True))
    old = SSea.ROW_Y[0]
    SSea.ROW_Y[0] = yw
    try:
        SSea.draw_ship(f, M, mood, sh, t, -1, 0.0, 0.0, idx, None)
    finally:
        SSea.ROW_Y[0] = old


def _water_strips(f, T, t, y, k, wind, glint_x=None):
    c_top, c_bot = _water_cols(T)
    if k == 1:
        c_top = mix(c_top, "#000000", 0.25)
    a = PW.wave_strip(1180, 46, 8 + 4 * k, c_top, mix(T["haze"], c_top, 0.5), "#EEF2F0", 911 + k, sharp=1.9, glint=T["haze"], glint_amt=0.5, facets=2, shade="#06141C")
    b = PW.wave_strip(900, 34, 6 + 3 * k, c_top, mix(T["haze"], c_top, 0.45), "#EEF2F0", 921 + k, sharp=2.2, glint=T["haze"], glint_amt=0.7, facets=2, shade="#06141C", comps=((2, 1.0), (5, 0.5), (9, 0.25)))
    sp = 20.0 * (-wind) * (1 + 0.6 * k)
    for i, (dy, img, spd, al) in enumerate(((0, a, sp, 1.0), (44, b, sp * 1.4, 0.55), (84, a, sp * 1.8, 0.4))):
        PW.draw_strip(f, img, -MARGIN, W + MARGIN, y - 4 + dy + math.sin(t * 0.6 + i + k) * 1.5, t * spd + 250 * i, alpha=al)


def _fire_reflect(f, meta, fire, T, y_water):
    """Su üstünde yangın yansıması: dikey uzamış turuncu parıltı sütunları."""
    if fire <= 0.02:
        return
    g = PW.glow_sprite(128, "#FF8A2E", 200, 70, 0.45)
    pg = skia.Paint()
    pg.setAlphaf(0.30 * fire * T["fire_vis"])
    n = int(math.ceil(len(meta["fires"]) * min(1.0, fire * 0.75)))
    for (x, y, s) in meta["fires"][:n]:
        f.c.save()
        f.c.translate(x, y_water + 70)
        f.c.scale(46 * s / 128.0 * 2, 130 / 128.0)
        f.c.drawImage(g, -128, -128, LIN, pg)
        f.c.restore()


CAMPFIRES = dict(
    roma=dict(mid=[330, 880, 1450, 1820], near=[600, 1400]),
    viyana=dict(mid=[260, 770, 1330, 1760], near=[640, 1380]),
    guns=dict(mid=[400, 1000, 1600], near=[760]),
    halkulvadi=dict(mid=[], near=[500, 1200]),
    tenochtitlan=dict(mid=[], near=[]),
    toledo=dict(mid=[360, 1000, 1700], near=[700, 1500]),
)


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


@SL.sc("siege")
class Siege:
    """Kuşatma. p: city, time, fire, weather, cannon_fire, ladders (+ smoke, soldiers, wind). Bkz. SAHNE_KATALOGU_deniz_savas.md"""

    def __init__(self, p):
        self.p = p
        self.city = p.get("city", "roma")
        if self.city not in CITIES:
            self.city = "roma"
        self.time = p.get("time", "day")
        if self.time not in TIMES:
            self.time = "day"
        self.weather = p.get("weather", "clear")
        if self.weather not in ("clear", "rain", "snow"):
            self.weather = "clear"
        self.fire = float(clamp(float(p.get("fire", 0.0)) if not isinstance(p.get("fire"), bool) else (1.0 if p.get("fire") else 0.0)))
        cf = p.get("cannon_fire", 0.0)
        self.cf = clamp(1.0 if cf is True else (0.0 if cf is False else float(cf)))
        self.ladders = bool(p.get("ladders", False))
        sm = p.get("smoke", None)
        self.smoke = clamp(0.0 if sm is None else (1.0 if sm is True else float(sm)))
        self.density = clamp(float(p.get("soldiers", 1.0)))
        self.wind = 1 if p.get("wind", -1) >= 0 else -1
        self.T = _time(self.time, self.weather)
        self.fq = int(round(self.fire * 4))

    def layers(self):
        c, tm, w = self.city, self.time, self.weather

        def base(f):
            bake_base(f, c, tm, w)
        return [(BASE_D, base)]

    def dyn(self):
        T, city, tm, w = self.T, self.city, self.time, self.weather
        wind = self.wind
        fire, cf = self.fire, self.cf

        def master(f, t):
            cam = SW.cam_from_canvas(f, BASE_D)
            # gökte kayan alçak bulutlar
            c1 = _cloud_s(tm, w, "low")
            wpx = c1.width() * 2
            off = (t * (4.0 if w != "rain" else 10.0)) % wpx
            x_a = (-MARGIN - wpx + off) if wind > 0 else (-MARGIN - off)
            for dx in (0, wpx):
                _draw_img2(f, c1, x_a + dx, -MARGIN + 150 + (HZ + MARGIN + 60) * 0.50, 0.7)
            img, cx_, cy_, meta = city_asset(city, tm, w, self.fq)
            events = []
            # --- şehir katmanı
            SW.push_depth(f, cam, CITY_D)
            if fire > 0.05 and meta["fires"]:
                fx = sum(p[0] for p in meta["fires"]) / len(meta["fires"])
                PW.glow(f, fx, CITY_BASE - 190, 760, "#FF8A2E", 0.30 * fire * T["fire_vis"], 255, 110, 0.35)
            f.c.drawImage(img, cx_, cy_, LIN, skia.Paint())
            _defenders(f, meta, city, T, t)
            _wall_torches(f, meta, T, t, wind * 6)
            _flags_dyn(f, meta, T, t, wind, city)
            if self.ladders:
                _ladders(f, city, T, t, wind)
            _fires(f, meta, t, fire, T, wind)
            _wall_fire(f, meta, T, t, cf, wind * 6)
            f.c.restore()
            # --- orta zemin
            SW.push_depth(f, cam, MID_D)
            gimg, gx, gy = ground_asset(city, tm, w, 0)
            f.c.drawImage(gimg, gx, gy, LIN, skia.Paint())
            vis = _vis(f)
            if city in WATER_MID:
                _water_strips(f, T, t, MID_Y, 0, wind)
                _fire_reflect(f, meta, fire, T, MID_Y)
            self._boats(f, t, "mid")
            _soldiers(f, city, T, t, "mid", self.density, vis) if city not in WATER_MID or city == "toledo" else None
            for gi, x in enumerate(GUNS[city]["mid"]):
                _gun(f, T, x, MID_Y + 62, 0.52, 1 if gi % 2 == 0 else -1, t, cf, 10 + gi, wind * 6, events)
            _campfires(f, [(x, MID_Y + 70 + (i % 2) * 10) for i, x in enumerate(CAMPFIRES[city]["mid"])], T, t, seed=5)
            f.c.restore()
            # şehir katmanına isabetler (sur üzeri) — orta zemin sonrası çizilir ama şehir koordinatında
            if events and cf > 0.01:
                SW.push_depth(f, cam, CITY_D)
                _impacts(f, city, T, t, events, wind)
                f.c.restore()
            # --- yakın zemin
            SW.push_depth(f, cam, NEAR_D)
            gimg, gx, gy = ground_asset(city, tm, w, 1)
            f.c.drawImage(gimg, gx, gy, LIN, skia.Paint())
            vis = _vis(f)
            if city in WATER_NEAR:
                _water_strips(f, T, t, NEAR_Y, 1, wind)
                _fire_reflect(f, meta, fire, T, NEAR_Y)
            self._boats(f, t, "near")
            if city not in WATER_NEAR:
                _soldiers(f, city, T, t, "near", self.density, vis)
            ev2 = []
            for gi, x in enumerate(GUNS[city]["near"]):
                _gun(f, T, x, NEAR_Y + 108, 1.0, 1 if gi % 2 == 0 else -1, t, cf, gi, wind * 6, ev2)
            _campfires(f, [(x, NEAR_Y + 120) for x in CAMPFIRES[city]["near"]], T, t, seed=9)
            if self.smoke > 0.02 or cf > 0.3:
                self._smoke(f, t, max(self.smoke, cf * 0.5))
            f.c.restore()
            if ev2 and cf > 0.01:
                SW.push_depth(f, cam, CITY_D)
                _impacts(f, city, T, t, ev2, wind)
                f.c.restore()
            # --- ön plan
            SW.push_depth(f, cam, FG_D)
            fimg, fx_, fy_ = fg_asset(city, tm, w)
            f.c.drawImage(fimg, fx_, fy_, LIN, skia.Paint())
            f.c.restore()
            self._overlay(f, t)
        return {0: master}

    def _boats(self, f, t, layer):
        city, T, tm = self.city, self.T, self.time
        if city == "halkulvadi" and layer == "mid":
            for i, (kind, x, dy, s, flag, hd, gun) in enumerate((("galley", 330, 70, 0.60, "#8E1F26", 1, 0.9), ("galley", 860, 118, 0.70, "#8E1F26", 1, 1.0), ("carrack", 1230, 96, 0.50, "#8E1F26", -1, 0.7), ("galley", 90, 150, 0.74, "#8E1F26", 1, 0.8), ("galley", 1650, 130, 0.62, "#2F6B4A", -1, 0.8))):
                _ship_at(f, T, tm, kind, x, MID_Y + dy, s, t, flag, i, gun=gun * (1.0 if self.cf > 0.01 else 0.0), heading=hd)
        elif city == "tenochtitlan":
            if layer == "mid":
                for i in range(7):
                    x = (140 + i * 270 + (t * (8 + 3 * (i % 3)) * (1 if i % 2 else -1))) % (W + 400) - 200
                    _canoe(f, T, x, MID_Y + 40 + (i % 3) * 34, 0.72, t, i, 1 if i % 2 else -1)
                for i, (x, dy, s) in enumerate(((420, 96, 0.40), (1330, 120, 0.44))):
                    _ship_at(f, T, tm, "carrack", x, MID_Y + dy, s, t, "#8E1F26", 20 + i, gun=(0.9 if self.cf > 0.01 else 0.0), heading=1 if i == 0 else -1, sails="full")
            else:
                for i in range(4):
                    x = (320 + i * 520 + (t * (14 + 4 * (i % 2)) * (1 if i % 2 else -1))) % (W + 500) - 250
                    _canoe(f, T, x, NEAR_Y + 54 + (i % 2) * 46, 1.25, t, 30 + i, 1 if i % 2 else -1)

    def _smoke(self, f, t, sm):
        T = self.T
        rs = RS(900)
        col = _smoke_col_default(T)
        if self.time in ("dusk",):
            col = "#8C6A58"
        for i in range(int(2 + 2 * sm)):
            x = rs.rand() * W + math.sin(t * 0.13 + i) * 40 + t * 5 * -self.wind
            y = NEAR_Y - 20 - rs.rand() * 150
            r = 100 + rs.rand() * 80
            a = (0.20 + 0.34 * sm) * (0.6 + 0.4 * math.sin(t * 0.25 + i * 1.7))
            PW.puff(f, x, y, r, col, a, seed=i, rot=0.3 * i)

    def _overlay(self, f, t):
        c = f.c
        c.save()
        c.resetMatrix()
        if self.weather == "rain":
            PW.rain_lines(f, t, n=170, seed=8, angle=-0.22, length=20, alpha=0.22, color="#C9D6D8", speed=1100, sw=1.1, rect=(0, 0, W, H))
            PW.rain_lines(f, t, n=140, seed=18, angle=-0.22, length=34, alpha=0.28, color="#C9D6D8", speed=1500, sw=1.4, rect=(0, 0, W, H))
            PW.rain_lines(f, t, n=76, seed=28, angle=-0.22, length=58, alpha=0.30, color="#C9D6D8", speed=1950, sw=2.0, rect=(0, 0, W, H))
        elif self.weather == "snow":
            _snow(f, t, 220)
        c.restore()


def cam_on_gun(near=True, idx=0, zoom=1.6):
    """Yakın/orta topçu mevzisine kamera."""
    xs = GUNS["roma"]["near"] if near else GUNS["roma"]["mid"]
    return safe_cam(W / 2 + (xs[idx % len(xs)] - W / 2) / (NEAR_D if near else MID_D), H / 2 + ((NEAR_Y + 40 if near else MID_Y) - H / 2) / (NEAR_D if near else MID_D), zoom)
