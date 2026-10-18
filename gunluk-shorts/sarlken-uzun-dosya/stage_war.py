"""Sahne-lab: gemi (karaka / kadırga / balıkçı), ahşap/taş yapılar — kâğıt-tiyatro siluet çizimleri.

Gemiler önbellekli sprite olarak pişirilir (ship_sprite); hareketli parçalar (bayrak, kürek, alev, duman) kare başına küçük çizimlerle eklenir.
Gemi koordinatı: baş (pruva) +x, su hattı y=0, yukarı −y; ölçü s=1 → karaka gövdesi ≈ 480 px.
"""
import math
from functools import lru_cache

import numpy as np
import skia

import props_war as PW
import sk
import stage as ST
from props_war import LIN, LINMIP, PLUS, RS, darken, lighten
from sk import C, H, W, clamp, lerp, mix, smooth


# ───────────────────────────── küçük çizim yardımcıları ─────────────────────────────
def cross_pattee(f, cx, cy, size, col, alpha=0.9):
    """Pattée haç (uçları genişleyen)."""
    a = size * 0.5
    b = size * 0.16
    c_ = size * 0.28
    pts = [(-b, -a), (b, -a), (b * 0.7, -c_), (c_, -b * 0.7), (a, -b), (a, b), (c_, b * 0.7), (b * 0.7, c_), (b, a), (-b, a), (-b * 0.7, c_), (-c_, b * 0.7), (-a, b), (-a, -b), (-c_, -b * 0.7), (-b * 0.7, -c_)]
    f.poly([(cx + x, cy + y) for x, y in pts], color=col, alpha=alpha)


def _sail_poly(cx, yt, yb, hw_t, hw_b, bulge, br=1.0, seed=0, torn=0.0, n=7):
    """Kare yelken kenar noktaları: rüzgâr kabarması. torn: yırtık (0..1)."""
    rs = RS(seed)
    pts = [(cx - hw_t, yt)]
    # üst kenar hafif sarkık
    for i in range(1, n):
        u = i / n
        pts.append((cx - hw_t + 2 * hw_t * u, yt + 3 * math.sin(math.pi * u) * 1.0))
    pts.append((cx + hw_t, yt))
    # sağ kenar: dışa şişkin
    for i in range(1, 4):
        u = i / 4
        xw = lerp(hw_t, hw_b, u) + bulge * 0.55 * math.sin(math.pi * u) * br
        pts.append((cx + xw, lerp(yt, yb, u)))
    pts.append((cx + hw_b, yb))
    # alt kenar: ortadan aşağı şişkin
    for i in range(1, n):
        u = i / n
        dy = bulge * 0.65 * math.sin(math.pi * u) * br
        if torn:
            dy += (rs.rand() * 2 - 0.3) * torn * 34 * (0.5 + math.sin(math.pi * u))
        pts.append((cx + hw_b - 2 * hw_b * u, yb + dy))
    pts.append((cx - hw_b, yb))
    for i in range(3, 0, -1):
        u = i / 4
        xw = lerp(hw_t, hw_b, u) + bulge * 0.55 * math.sin(math.pi * u) * br
        pts.append((cx - xw, lerp(yt, yb, u)))
    return pts


def square_sail(f, cx, yt, yb, hw_t, hw_b, st, bulge=14, seed=0, torn=0.0, cross=None, cross_sz=0.5, detail=2, alpha=1.0, burn=0.0):
    pts = _sail_poly(cx, yt, yb, hw_t, hw_b, bulge, 1.0, seed, torn)
    path = sk.smooth_path(pts, True, 0.22)
    light, mid, shade = st["sail_l"], st["sail"], st["sail_d"]
    if burn > 0:
        light, mid, shade = mix(light, "#1A0F0A", burn * 0.7), mix(mid, "#1A0F0A", burn * 0.75), mix(shade, "#0A0604", burn * 0.7)
    dirx = st.get("light_dir", 1)
    x0, x1 = (cx - hw_b, cx + hw_b) if dirx > 0 else (cx + hw_b, cx - hw_b)
    f.path(path, shader=f.lin(x0, 0, x1, 0, [(light, 0.0), (mid, 0.45), (shade, 1.0)]), alpha=alpha)
    if detail >= 1:
        f.path(path, shader=f.lin(0, yt, 0, yb + bulge, [("#FFFFFF", 0.0, 22), ("#000000", 0.55, 0), ("#000000", 1.0, 70)]), alpha=alpha)
    f.c.save()
    f.c.clipPath(path, skia.ClipOp.kIntersect, True)
    if detail >= 2:
        for k in (-0.55, -0.18, 0.18, 0.55):                       # dikişler
            xx = cx + k * hw_b
            f.path(sk.smooth_path([(cx + k * hw_t, yt), (xx + bulge * 0.15 * k, (yt + yb) / 2), (xx, yb + bulge * 0.4)], False, 0.4), style="stroke", sw=1.1, color="#000000", alpha=0.20)
        for q in (0.32, 0.62):                                     # camadan (ıstralya) bantları
            yy = lerp(yt, yb, q)
            f.path(sk.smooth_path([(cx - hw_b * 1.1, yy), (cx, yy + bulge * 0.35), (cx + hw_b * 1.1, yy)], False, 0.4), style="stroke", sw=1.4, color="#000000", alpha=0.20)
        if cross:
            cross_pattee(f, cx, lerp(yt, yb, 0.5), min(hw_b * 2 * cross_sz, (yb - yt) * 0.85), cross, 0.78 * (1 - burn * 0.6))
    f.c.restore()
    f.path(path, style="stroke", sw=1.6, color=darken(shade, 0.55), alpha=0.7 * alpha)
    if burn > 0 and detail >= 1:                                   # yanık delikler
        rs = RS(seed + 4)
        for _ in range(4):
            hx, hy = cx + (rs.rand() - 0.5) * hw_b * 1.5, lerp(yt, yb, 0.3 + rs.rand() * 0.6)
            f.circle(hx, hy, 6 + rs.rand() * 12, color="#0A0604", alpha=0.8 * burn)
            f.circle(hx, hy, 9 + rs.rand() * 12, style="stroke", sw=2.0, color="#E8741C", alpha=0.7 * burn)


def yard(f, cx, y, hw, st, thick=6):
    f.line(cx - hw, y, cx + hw, y, color=st["hull"], sw=thick, cap="round")
    f.line(cx - hw, y - thick * 0.35, cx + hw, y - thick * 0.35, color=st["rim"], sw=1.2, alpha=0.7)


def _mast(f, x, y0, y1, st, w0=11, w1=6):
    f.poly([(x - w0 / 2, y0), (x + w0 / 2, y0), (x + w1 / 2, y1), (x - w1 / 2, y1)], color=st["hull"])
    f.line(x - w0 / 2 + 1, y0, x - w1 / 2 + 1, y1, color=st["rim"], sw=1.2, alpha=0.7)


def _top(f, x, y, w, st):
    """Gözetleme sepeti (crow's nest)."""
    f.poly([(x - w * 0.5, y), (x + w * 0.5, y), (x + w * 0.62, y - w * 0.42), (x - w * 0.62, y - w * 0.42)], color=st["hull"])
    f.line(x - w * 0.62, y - w * 0.42, x + w * 0.62, y - w * 0.42, color=st["rim"], sw=1.2, alpha=0.6)
    for k in range(-2, 3):
        f.line(x + k * w * 0.24, y - w * 0.42, x + k * w * 0.26, y - w * 0.72, color=st["hull"], sw=1.6)
    f.line(x - w * 0.6, y - w * 0.7, x + w * 0.6, y - w * 0.7, color=st["hull"], sw=1.6)


SHEER = ((-236, -128), (-150, -98), (-60, -82), (20, -80), (90, -88), (160, -112), (250, -128))


def _sheer_y(x):
    xs = [p[0] for p in SHEER]
    ys = [p[1] for p in SHEER]
    return float(np.interp(x, xs, ys))


def draw_carrack(f, st, lod=2):
    hull, rim = st["hull"], st["rim"]
    sails = st.get("sails", "full")
    burn = st.get("burnt", 0.0)
    torn = 0.0 if sails != "torn" else 1.0
    # ── direkler (yelkenlerin arkasında)
    if lod >= 0:
        _mast(f, -5, -80, -452, st, 12, 6)
        _mast(f, 138, -126, -352, st, 10, 5)
        _mast(f, -160, -150, -318, st, 9, 5)
        f.line(228, -122, 372, -204, color=hull, sw=9)              # bukalemun: kesme (bowsprit)
        f.line(228, -127, 372, -208, color=rim, sw=1.2, alpha=0.7)
    # ── yelkenler
    if sails in ("full", "reef", "torn"):
        full = sails != "reef"
        if lod >= 1:
            yard(f, -5, -200, 128, st, 7)
            yard(f, 138, -238, 86, st, 6)
        square_sail(f, -5, -200, -106, 118, 134, st, 16, seed=1, torn=torn, cross=st["cross"], detail=lod, burn=burn)
        square_sail(f, 138, -238, -152, 78, 90, st, 12, seed=2, torn=torn, detail=lod, burn=burn)
        if full:
            yard(f, -5, -336, 92, st, 6) if lod >= 1 else None
            yard(f, 138, -324, 62, st, 5) if lod >= 1 else None
            yard(f, -5, -414, 54, st, 4) if lod >= 1 else None
            square_sail(f, -5, -336, -230, 86, 98, st, 12, seed=3, torn=torn, cross=st["cross"], cross_sz=0.42, detail=lod, burn=burn)
            square_sail(f, 138, -324, -256, 58, 66, st, 10, seed=4, torn=torn, detail=lod, burn=burn)
            square_sail(f, -5, -414, -344, 50, 60, st, 8, seed=5, torn=torn, detail=lod, burn=burn)
        # latin (mizzen) yelken
        yd = [(-262, -186), (-70, -322)]
        f.line(yd[0][0], yd[0][1], yd[1][0], yd[1][1], color=hull, sw=6)
        tri = skia.Path()
        tri.moveTo(*yd[0]); tri.lineTo(*yd[1]); tri.quadTo(-58, -236, -100, -176); tri.quadTo(-170, -156, yd[0][0], yd[0][1]); tri.close()
        f.path(tri, shader=f.lin(-262, 0, -70, 0, [(st["sail_d"], 0.0), (st["sail"], 0.55), (st["sail_l"], 1.0)] if st.get("light_dir", 1) < 0 else [(st["sail_l"], 0.0), (st["sail"], 0.5), (st["sail_d"], 1.0)]))
        f.path(tri, style="stroke", sw=1.4, color=darken(st["sail_d"], 0.5), alpha=0.65)
        # sprit yelkeni (bukalemun altı küçük)
        if lod >= 1 and full:
            square_sail(f, 322, -178, -128 - 0, 24, 30, st, 7, seed=6, torn=torn, detail=min(lod, 1), burn=burn)
    # ── gövde
    hp = skia.Path()
    hp.moveTo(-236, -128)
    hp.cubicTo(-200, -112, -150, -90, -60, -82)
    hp.cubicTo(20, -78, 90, -88, 160, -112)
    hp.lineTo(250, -128)
    hp.cubicTo(266, -100, 254, -62, 226, -28)
    hp.cubicTo(200, 6, 150, 30, 70, 36)
    hp.lineTo(-120, 36)
    hp.cubicTo(-192, 32, -230, 4, -242, -40)
    hp.cubicTo(-250, -80, -246, -106, -236, -128)
    hp.close()
    aft = sk.poly_path([(-238, -124), (-246, -176), (-234, -200), (-120, -200), (-120, -170), (-62, -170), (-62, -80), (-120, -84)], True)
    aft2 = sk.smooth_path([(-246, -172), (-238, -204), (-210, -214)], False, 0.3)
    fore = sk.poly_path([(112, -108), (112, -156), (238, -164), (262, -146), (256, -122), (170, -108)], True)
    sil = skia.Path()
    sil.addPath(hp)
    sil.addPath(aft)
    sil.addPath(fore)
    # kenar ışığı: gövde ana silüetinin hafif kaymış kopyası
    f.c.save()
    f.c.translate(-1.6, -1.8)
    f.path(sil, color=rim, alpha=0.85)
    f.c.restore()
    f.path(sil, shader=f.lin(0, -200, 0, 36, [(mix(hull, "#FFFFFF", 0.04), 0.0), (hull, 0.5), (darken(hull, 0.15), 1.0)]))
    if lod >= 1:
        # altın şerit (wale) ve ince şerit
        wl = [(x, _sheer_y(x) + 17) for x in range(-236, 252, 12)]
        f.path(sk.smooth_path(wl, False, 0.3), style="stroke", sw=7, color=st["gold"], alpha=0.70)
        wl2 = [(x, _sheer_y(x) + 31) for x in range(-226, 238, 12)]
        f.path(sk.smooth_path(wl2, False, 0.3), style="stroke", sw=2.4, color=st["gold"], alpha=0.5)
        if lod >= 2:
            for q in range(3):                                         # kaplama (tahta) çizgileri
                pl = [(x, _sheer_y(x) + 46 + q * 12 - (abs(x) / 480.0) * 14 * (q + 1) * 0.2) for x in range(-210, 220, 14)]
                f.path(sk.smooth_path(pl, False, 0.3), style="stroke", sw=1.2, color="#000000", alpha=0.35)
        # lomboz / top menfezleri
        for x in range(-112, 200, 34):
            y = _sheer_y(x) + 38
            on = st.get("lamp", False)
            f.rect(x - 7, y - 5, 14, 10, color=st["lamp_col"] if on else "#000000", alpha=0.9 if on else 0.5)
            if on and lod >= 2:
                PW.glow(f, x, y, 20, st["lamp_col"], 0.35)
        # kıç camları
        for k in range(3):
            xx = -226 + k * 24
            f.path(sk.smooth_path([(xx - 7, -150), (xx - 7, -166), (xx, -174), (xx + 7, -166), (xx + 7, -150)], True, 0.2), color=st["lamp_col"] if st.get("lamp") else "#000000", alpha=0.85 if st.get("lamp") else 0.45)
        # korkuluklar (balustrad)
        for x in range(-232, -122, 9):
            f.line(x, -200, x, -214, color=hull, sw=1.8)
        f.line(-234, -214, -122, -214, color=hull, sw=2)
        for x in range(-58, 112, 9):
            y = _sheer_y(x) - 3
            f.line(x, y, x, y - 15, color=hull, sw=1.6)
        f.line(-60, _sheer_y(-60) - 17, 112, _sheer_y(112) - 17, color=hull, sw=2)
        for x in range(122, 252, 9):
            f.line(x, -164, x, -178, color=hull, sw=1.8)
        f.line(120, -178, 250, -180, color=hull, sw=2)
        # arka direk fener direği
        f.line(-236, -204, -242, -236, color=hull, sw=3)
        f.rect(-250, -262, 16, 26, color=hull)
        f.poly([(-252, -262), (-232, -262), (-242, -276)], color=hull)
        if st.get("lamp"):
            f.rect(-247, -258, 10, 18, color=st["lamp_col"], alpha=0.95)
        # babalar
        f.line(-60, -166, 112, -166, color=hull, sw=1.0, alpha=0.0)
    # ── halat takımı
    if lod >= 1:
        rg = skia.Path()
        for sx in (-1, 1):                                              # ana direk çarmıhları
            for k in range(3):
                rg.moveTo(-5 + sx * 7, -222)
                rg.lineTo(-5 + sx * (86 + k * 12) + (0 if sx > 0 else 0), _sheer_y(-5 + sx * (86 + k * 12)) - 6)
            for k in range(3):
                rg.moveTo(138 + sx * 6, -250)
                rg.lineTo(138 + sx * (50 + k * 10), -152 if sx < 0 else -150)
        rg.moveTo(-5, -448)
        rg.lineTo(138, -352)
        rg.lineTo(366, -204)
        rg.moveTo(-5, -440)
        rg.lineTo(-232, -214)
        rg.moveTo(138, -350)
        rg.lineTo(240, -164)
        rg.moveTo(-160, -316)
        rg.lineTo(-236, -202)
        f.path(rg, style="stroke", sw=1.25, color=hull, alpha=0.8)
        if lod >= 2:                                                    # ratlines
            for sx in (-1, 1):
                for yy in range(-212, -102, 14):
                    t_ = (yy + 222) / 118.0
                    x_a = -5 + sx * (7 + (86 - 7) * t_)
                    x_b = -5 + sx * (7 + (110 - 7) * t_)
                    f.line(x_a, yy, x_b, yy, color=hull, sw=1.0, alpha=0.55)
            _top(f, -5, -222, 34, st)
            _top(f, 138, -250, 26, st)
    return


# ───────────────────────────── kadırga ─────────────────────────────
GAL_OAR_X0, GAL_OAR_X1 = -150, 196
GAL_N_OARS = 22
GAL_OAR_Y = -30


def _lateen(f, st, ax, ay, bx, by, cx_, cy_, belly=16, seed=0, burn=0.0, detail=2):
    """Latin yelken: antenna (ax,ay)-(bx,by), kenar (cx_,cy_)."""
    path = skia.Path()
    path.moveTo(ax, ay)
    path.lineTo(bx, by)
    mx, my = (bx + cx_) / 2 + belly, (by + cy_) / 2
    path.quadTo(mx, my, cx_, cy_)
    path.quadTo((cx_ + ax) / 2 - belly * 0.2, max(cy_, ay) + belly * 0.8, ax, ay)
    path.close()
    sail, sd, sl = st["sail"], st["sail_d"], st["sail_l"]
    if burn > 0:
        sail, sd, sl = mix(sail, "#1A0F0A", burn * 0.7), mix(sd, "#0A0604", burn * 0.7), mix(sl, "#1A0F0A", burn * 0.7)
    x0, x1 = (ax, cx_) if st.get("light_dir", 1) > 0 else (cx_, ax)
    f.path(path, shader=f.lin(x0, 0, x1, 0, [(sl, 0.0), (sail, 0.5), (sd, 1.0)]))
    f.path(path, shader=f.lin(0, by, 0, cy_, [("#FFFFFF", 0.0, 20), ("#000000", 1.0, 60)]))
    if detail >= 2:
        f.c.save()
        f.c.clipPath(path, skia.ClipOp.kIntersect, True)
        for k in (0.22, 0.4, 0.58, 0.76):
            px, py = lerp(ax, bx, k), lerp(ay, by, k)
            f.line(px, py, lerp(px, cx_, 0.9) + 6 * k, lerp(py, cy_, 0.9), color="#000000", sw=1.0, alpha=0.2)
        f.c.restore()
    f.path(path, style="stroke", sw=1.4, color=darken(sd, 0.5), alpha=0.7)


def draw_galley(f, st, lod=2):
    hull, rim = st["hull"], st["rim"]
    sails = st.get("sails", "full")
    burn = st.get("burnt", 0.0)
    rig = ((26, -40, 58, -316, (-132, -108), (226, -318), (150, -58), 1.0), (176, -50, 198, -236, (96, -112), (258, -240), (214, -66), 0.62))
    for (bx0, by0, bx1, by1, ya, yb, yc, sc) in rig:
        f.line(bx0, by0, bx1, by1, color=hull, sw=8.5 * sc + 2)
        f.line(bx0 - 3, by0, bx1 - 3, by1, color=rim, sw=1.0, alpha=0.6)
        if sails in ("full", "torn"):
            _lateen(f, st, ya[0], ya[1], yb[0], yb[1], yc[0], yc[1], belly=18 * sc, seed=1, burn=burn, detail=lod)
        elif sails == "reef":   # toplanmış yelken: antenna boyunca sarı
            f.line(ya[0], ya[1], yb[0], yb[1], color=hull, sw=6.5 * sc + 1)
            f.line(lerp(ya[0], yb[0], 0.12), lerp(ya[1], yb[1], 0.12) + 8, lerp(ya[0], yb[0], 0.88), lerp(ya[1], yb[1], 0.88) + 8, color=mix(st["sail"], "#000000", 0.35), sw=10 * sc + 2)
        f.line(ya[0], ya[1], yb[0], yb[1], color=hull, sw=6.0 * sc + 1.2)
        f.line(ya[0], ya[1] - 2, yb[0], yb[1] - 2, color=rim, sw=1.0, alpha=0.65)
    # gövde
    hp = skia.Path()
    hp.moveTo(-240, -134)
    hp.cubicTo(-254, -100, -248, -66, -226, -50)
    hp.cubicTo(-150, -42, -60, -40, 30, -40)
    hp.cubicTo(118, -40, 196, -46, 236, -66)
    hp.lineTo(270, -88)
    hp.lineTo(282, -62)
    hp.lineTo(350, -40)
    hp.lineTo(268, -10)
    hp.cubicTo(220, 12, 150, 26, 60, 28)
    hp.lineTo(-110, 28)
    hp.cubicTo(-190, 24, -234, 8, -250, -34)
    hp.cubicTo(-256, -70, -252, -104, -240, -134)
    hp.close()
    sil = skia.Path()
    sil.addPath(hp)
    # kıç tente (çatı) — direk ve kenarlarla
    awn = skia.Path()
    awn.moveTo(-246, -124)
    awn.quadTo(-240, -170, -196, -176)
    awn.quadTo(-142, -178, -108, -134)
    awn.lineTo(-106, -92)
    awn.lineTo(-246, -92)
    awn.close()
    sil.addPath(sk.poly_path([(196, -78), (270, -96), (272, -66), (196, -56)], True))     # pruva platformu
    f.c.save()
    f.c.translate(-1.6, -1.8)
    f.path(sil, color=rim, alpha=0.85)
    f.c.restore()
    f.path(sil, shader=f.lin(0, -176, 0, 28, [(mix(hull, "#FFFFFF", 0.05), 0.0), (hull, 0.55), (darken(hull, 0.15), 1.0)]))
    # kıç direkleri (tente altı)
    for xx in (-232, -190, -148, -112):
        f.line(xx, -92, xx, -92 - 30 - 20 * (1 - abs(xx + 170) / 70.0), color=hull, sw=2.4)
    f.path(awn, shader=f.lin(0, -178, 0, -92, [(mix(st["awn"], "#FFFFFF", 0.05), 0.0), (darken(st["awn"], 0.45), 1.0)]), alpha=0.95)
    f.path(awn, style="stroke", sw=2.2, color=st["gold"], alpha=0.6)
    f.c.save()
    f.c.clipPath(awn, skia.ClipOp.kIntersect, True)
    for k in range(7):
        xx = -240 + k * 20
        f.line(xx, -180, xx + 8, -92, color="#000000", sw=2.2, alpha=0.22)
    f.c.restore()
    if lod >= 1:
        # fener direkleri
        for i, (lx, lh) in enumerate(((-252, 72), (-240, 108), (-228, 144))):
            if i == 2 and lod < 2:
                continue
            f.line(lx, -128, lx - 2, -128 - lh, color=hull, sw=3)
            f.rect(lx - 8, -128 - lh - 22, 16, 22, color=hull)
            f.poly([(lx - 10, -128 - lh - 22), (lx + 10, -128 - lh - 22), (lx, -128 - lh - 36)], color=hull)
            if st.get("lamp"):
                f.rect(lx - 5, -128 - lh - 19, 10, 15, color=st["lamp_col"], alpha=0.95)
        # kürek dayanağı (apostis) + altın çizgi
        f.line(-172, -47, 204, -49, color=lighten(hull, 0.12), sw=4.5, alpha=0.95)
        f.line(-172, -53, 204, -55, color=st["gold"], sw=1.6, alpha=0.5)
        # kürek lumbozları
        for k in range(GAL_N_OARS):
            xx = GAL_OAR_X0 + (GAL_OAR_X1 - GAL_OAR_X0) * k / (GAL_N_OARS - 1)
            f.circle(xx, GAL_OAR_Y - 6, 2.6, color="#000000", alpha=0.0)
        # kürekçi başları (güverte kenarında)
        for x in range(-150, 200, 13):
            f.oval(x, -44 - 3, 4.8, 5.8, color=hull)
        # pruva topu
        f.line(206, -100, 296, -110, color=hull, sw=8.5, cap="round")
        f.circle(204, -99, 8.5, color=hull)
        f.line(294, -110, 300, -111, color=rim, sw=2.5, alpha=0.8)
        f.line(282, -62, 350, -42, color=rim, sw=1.2, alpha=0.7)
        if st.get("lamp") and lod >= 2:
            for x in range(-100, 170, 52):
                f.rect(x - 4, -58, 8, 6, color=st["lamp_col"], alpha=0.85)
                PW.glow(f, x, -55, 16, st["lamp_col"], 0.3)
        # halat
        rg = skia.Path()
        rg.moveTo(58, -316); rg.lineTo(270, -92)
        rg.moveTo(58, -312); rg.lineTo(-240, -128)
        rg.moveTo(198, -236); rg.lineTo(270, -92)
        rg.moveTo(40, -240); rg.lineTo(-6, -46)
        rg.moveTo(40, -240); rg.lineTo(96, -46)
        f.path(rg, style="stroke", sw=1.1, color=hull, alpha=0.7)


# ───────────────────────────── balıkçı teknesi ─────────────────────────────
def draw_fishing(f, st, lod=2):
    hull, rim = st["hull"], st["rim"]
    sail_c = mix(st["sail"], "#8A5A32", 0.45)
    sail_l = mix(st["sail_l"], "#B07840", 0.35)
    sail_d = mix(st["sail_d"], "#3A220F", 0.5)
    burn = st.get("burnt", 0.0)
    if st.get("sails", "full") != "bare":
        f.line(6, -22, 12, -200, color=hull, sw=6)
        pts = [(-70, -30), (-24, -118), (14, -204), (28, -150), (22, -32), (-20, -28)]
        path = sk.smooth_path(pts, True, 0.16)
        f.path(path, shader=f.lin(-70, 0, 28, 0, [(sail_l, 0.0), (sail_c, 0.5), (sail_d, 1.0)] if st.get("light_dir", 1) > 0 else [(sail_d, 0.0), (sail_c, 0.5), (sail_l, 1.0)]))
        f.path(path, style="stroke", sw=1.3, color=darken(sail_d, 0.5), alpha=0.7)
        f.line(-72, -30, 16, -210, color=hull, sw=4)
        if lod >= 1:
            f.path(sk.smooth_path([(-52, -46), (-6, -90), (16, -140)], False, 0.4), style="stroke", sw=1.0, color="#000000", alpha=0.2)
            f.path(sk.smooth_path([(-40, -64), (4, -66), (22, -70)], False, 0.4), style="stroke", sw=1.0, color="#000000", alpha=0.2)
    hp = skia.Path()
    hp.moveTo(-84, -44)
    hp.cubicTo(-74, -22, -42, 6, 8, 14)
    hp.cubicTo(52, 14, 92, -4, 112, -52)
    hp.lineTo(104, -52)
    hp.cubicTo(82, -26, 40, -22, -8, -24)
    hp.cubicTo(-40, -24, -64, -30, -76, -44)
    hp.close()
    f.c.save(); f.c.translate(-1.2, -1.4)
    f.path(hp, color=rim, alpha=0.8)
    f.c.restore()
    f.path(hp, shader=f.lin(0, -52, 0, 14, [(mix(hull, "#FFFFFF", 0.05), 0.0), (hull, 1.0)]))
    f.path(sk.smooth_path([(x, -26 + (abs(x - 14) / 100) ** 2 * 22) for x in range(-78, 110, 14)], False, 0.3), style="stroke", sw=2.0, color=st["gold"], alpha=0.35)
    if lod >= 1:
        # balıkçılar (iki küçük silüet) ve sepet
        for fx, fh in ((-40, 34), (28, 30)):
            f.oval(fx, -24 - fh * 0.75, 4.4, 5.2, color=hull)
            f.poly([(fx - 6, -24), (fx + 6, -24), (fx + 4.5, -24 - fh * 0.7), (fx - 4.5, -24 - fh * 0.7)], color=hull)
        f.path(sk.smooth_path([(52, -25), (66, -25), (68, -33), (50, -33)], True, 0.2), color=hull)
        if st.get("lamp"):
            f.circle(104, -56, 3.0, color=st["lamp_col"])
            PW.glow(f, 104, -56, 22, st["lamp_col"], 0.55)


# ───────────────────────────── sprite pişirici ─────────────────────────────
BBOX = dict(carrack=(-290, -520, 400, 80), galley=(-290, -420, 370, 60), fishing=(-110, -230, 130, 36))
DRAW = dict(carrack=draw_carrack, galley=draw_galley, fishing=draw_fishing)


@lru_cache(maxsize=96)
def ship_sprite(kind, ks, hull, rim, sail, sail_l, sail_d, gold, cross, lamp, lamp_col, sails, burnt, light_dir, awn, lod):
    """kind → (Image, ox, oy, ks): orijin (ox,oy) = su hattı ortası; ks: sprite çözünürlük çarpanı."""
    x0, y0, x1, y1 = BBOX[kind]
    pad = 6
    w = int((x1 - x0) * ks) + 2 * pad
    h = int((y1 - y0) * ks) + 2 * pad
    ox = int(-x0 * ks) + pad
    oy = int(-y0 * ks) + pad
    st = dict(hull=hull, rim=rim, sail=sail, sail_l=sail_l, sail_d=sail_d, gold=gold, cross=cross, lamp=lamp, lamp_col=lamp_col, sails=sails, burnt=burnt, light_dir=light_dir, awn=awn)

    def fn(f):
        f.c.scale(ks, ks)
        DRAW[kind](f, st, lod)
    im = PW.bake_sprite(fn, w, h, ox, oy)
    return im, ox, oy, ks


def ship_style(M, flag, kind):
    """Ruh halinden (mood) gemi renkleri."""
    return dict(hull=M["hull"], rim=M["rim"], sail=M["sail"], sail_l=M["sail_l"], sail_d=M["sail_d"], gold=M["gold"], cross=flag, lamp=M["lamp"], lamp_col=M["lamp_col"], light_dir=M["light_dir"], awn=flag)
