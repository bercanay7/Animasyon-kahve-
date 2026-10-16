"""Kâğıt kesme figürleri ve nesneler (silüetler, araçlar, belgeler). Hepsi telifli karakter/logo değil, genel çizimlerdir."""
import math
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw

from paper import *  # noqa


# ───────────────────────── insanlar ─────────────────────────
def kid(ctx, x, y, s=1.0, col=INK, point=1.0):
    """Pelerinli küçük çocuk silüeti (ayak y'de), göğe uzanan kol"""
    X = Xf(x, y, s)
    pshape(ctx, X.pts([(-24, 0), (-16, -58), (-9, -94), (9, -94), (16, -58), (24, 0)]), col, sh=(5 * s, 6 * s), sh_a=0.16, edge=0.24)
    pshape(ctx, X.pts(circ_poly(0, -110, 14, n=16)), col, sh=(3 * s, 4 * s), sh_a=0.12, edge=0.22)
    ctx.poly(X.pts([(-15, -105), (0, -136), (15, -105)]), col)
    ctx.line(X.pts([(10, -80), (10 + 30 * point, -80 - 22 * point)]), 6 * s, col, 1.0)


def hooded(ctx, x, y, s=1.0, col=INK, eye=None, mask=False, hgt=1.0, eye_r=4.0):
    """Kukuletalı çöl insanı; eye: göz parıltı rengi; mask: yüz bandı"""
    X = Xf(x, y, s)
    h = 150 * hgt
    pshape(ctx, X.pts([(-30, 0), (-22, -h * 0.45), (-12, -h * 0.82), (12, -h * 0.82), (22, -h * 0.45), (30, 0)]), col, sh=(6 * s, 7 * s), sh_a=0.16, edge=0.22)
    pshape(ctx, X.pts([(-18, -h * 0.78), (-12, -h * 0.98), (0, -h * 1.1), (12, -h * 0.98), (18, -h * 0.78)]), col, sh=(3 * s, 4 * s), sh_a=0.1, edge=0.2)
    fx, fy = X.p(0, -h * 0.92)
    if mask:
        ctx.poly(X.pts([(-13, -h * 0.86), (13, -h * 0.86), (11, -h * 0.78), (-11, -h * 0.78)]), tint(col, 0.14))
    if eye:
        for dx in (-6, 6):
            ex, ey = X.p(dx, -h * 0.93)
            ctx.glow(ex, ey, 14 * s, eye, 0.7)
            ctx.circ(ex, ey, eye_r * s, eye)


def author(ctx, x, y, s=1.0, col=INK):
    """Defterli yazar silüeti (şapka + defter)"""
    X = Xf(x, y, s)
    pshape(ctx, X.pts([(-26, 0), (-20, -70), (-12, -104), (12, -104), (20, -70), (26, 0)]), col, sh=(5 * s, 6 * s), sh_a=0.16, edge=0.22)
    pshape(ctx, X.pts(circ_poly(0, -122, 15, n=16)), col, sh=(3 * s, 4 * s), sh_a=0.12, edge=0.2)
    ctx.poly(X.pts([(-26, -130), (26, -130), (18, -136), (-18, -136)]), col)           # şapka kenarı
    ctx.poly(X.pts([(-14, -136), (-12, -154), (12, -154), (14, -136)]), col)
    prect(ctx, *X.p(14, -70), *X.p(40, -48), CREAM, sh=(3, 4), sh_a=0.2, edge=0.0)    # defter


def crowd_member(ctx, x, y, s, col):
    X = Xf(x, y, s)
    ctx.poly(X.pts([(-9, 0), (-6, -26), (6, -26), (9, 0)]), col)
    ctx.poly(X.pts(circ_poly(0, -34, 7, n=10)), col)


def throne(ctx, x, y, s=1.0, col=INK, glow=None):
    """Taht + kukuletalı figür (imparator)"""
    X = Xf(x, y, s)
    if glow:
        gx, gy = X.p(0, -190)
        ctx.glow(gx, gy, 210 * s, glow, 0.35)
    back = [(-64, 0), (-64, -250), (-44, -306), (-24, -254), (0, -340), (24, -254), (44, -306), (64, -250), (64, 0)]
    pshape(ctx, X.pts(back), col, sh=(8 * s, 10 * s), sh_a=0.25, edge=0.55)
    pshape(ctx, X.pts([(-82, 0), (-82, -56), (82, -56), (82, 0)]), tint(col, 0.08), sh=(6 * s, 8 * s), sh_a=0.2, edge=0.16)
    pshape(ctx, X.pts([(-28, -56), (-20, -150), (-10, -196), (10, -196), (20, -150), (28, -56)]), tint(col, -0.1), sh=(0, 0), sh_a=0.0, edge=0.18)
    pshape(ctx, X.pts([(-18, -180), (-12, -214), (0, -230), (12, -214), (18, -180)]), tint(col, -0.1), sh=(0, 0), sh_a=0.0, edge=0.18)


# ───────────────────────── gezegen / yaratık / araç ─────────────────────────
@lru_cache(maxsize=48)
def planet_sprite(r, cols, ph):
    """r: yarıçap (1x px); 2x çözünürlükte RGBA. cols: şerit renkleri"""
    n = int(2 * r * SS)
    base = Image.new("RGB", (n, n), cols[0])
    d = ImageDraw.Draw(base)
    nb = len(cols) - 1
    for j in range(1, len(cols)):
        pts = []
        for x in range(0, n + 1, 10):
            yy = n * (0.10 + 0.84 * (j - 1) / max(1, nb)) + 0.035 * n * math.sin(x / n * 6.283 * 1.4 + ph * 6.283 + j * 1.3)
            pts.append((x, yy))
        d.polygon(pts + [(n, n), (0, n)], fill=cols[j])
    a = np.asarray(base, dtype=np.float32)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    u, v = (xx / n - 0.5) * 2, (yy / n - 0.5) * 2
    lit = np.clip(1.08 - 0.62 * np.clip(u * 0.62 + v * 0.55 + 0.25, 0, 1.6), 0.45, 1.08)
    a = np.clip(a * lit[..., None], 0, 255).astype(np.uint8)
    out = Image.fromarray(a, "RGB").convert("RGBA")
    m = Image.new("L", (n, n), 0)
    ImageDraw.Draw(m).ellipse([0, 0, n - 1, n - 1], fill=255)
    out.putalpha(m)
    return out


def planet(ctx, cx, cy, r, cols, ph=0.0, halo=None, a=1.0):
    if halo is not None:
        ctx.glow(cx, cy, r * 1.7, halo, 0.45 * a)
    spr = planet_sprite(int(r), tuple(cols), round(ph % 1.0, 2))
    x, y = ctx.X(cx - r, cy - r)
    if a < 0.999:
        al = spr.getchannel("A").point(lambda v: int(v * a))
        ctx.im.paste(spr.convert("RGB"), (int(x), int(y)), al)
    else:
        ctx.im.paste(spr.convert("RGB"), (int(x), int(y)), spr.getchannel("A"))


def worm_mouth(ctx, cx, cy, R, t=0.0, body=Hx("#9C4B2A"), tooth=Hx("#F6E6C2"), throat=Hx("#150906"), glow=SPICE, n=26, open_k=1.0):
    """Kum kurdu ağzı (önden): pürüzlü halkalı dudak, kırmızı et, kıvrık ince kristal dişler, mavi parıltılı boğaz"""
    R = R * (0.97 + 0.03 * math.sin(t * 3.0))
    lip = []
    for i in range(56):
        a = i * 2 * math.pi / 56
        k = 1.0 + 0.05 * math.sin(a * 7 + 1.0)
        lip.append((cx + math.cos(a) * R * k, cy + math.sin(a) * R * k))
    pshape(ctx, lip, body, sh=(0, 10), sh_a=0.25, edge=0.22)
    ctx.circ(cx, cy, R * 0.90, tint(body, -0.22))
    ctx.circ(cx, cy, R * 0.82, Hx("#7D2C1E"))                       # et
    for r_ring, w_ring in ((0.70, 3.0), (0.58, 2.4)):
        ctx.ring(cx, cy, R * r_ring, w_ring, Hx("#5E1D14"), 0.7)
    th = R * 0.30 * (0.55 + 0.45 * open_k)
    ctx.circ(cx, cy, th * 1.5, Hx("#3B120C"))
    ctx.circ(cx, cy, th, throat)
    ctx.glow(cx, cy, R * 0.45, glow, 0.62 * open_k)
    rot = t * 0.18
    for i in range(n):
        a = rot + i * 2 * math.pi / n
        hw = math.pi / n * 0.40
        long_ = (i % 3 != 1)
        r_b = R * 0.84
        r_t = R * (0.34 if long_ else 0.50) * (1.0 + 0.5 * (1 - open_k))
        curl = 0.14 if long_ else -0.10
        base_l = (cx + math.cos(a - hw) * r_b, cy + math.sin(a - hw) * r_b)
        base_r = (cx + math.cos(a + hw) * r_b, cy + math.sin(a + hw) * r_b)
        mid_l = (cx + math.cos(a - hw * 0.6 + curl * 0.5) * (r_b + r_t) / 2, cy + math.sin(a - hw * 0.6 + curl * 0.5) * (r_b + r_t) / 2)
        mid_r = (cx + math.cos(a + hw * 0.6 + curl * 0.5) * (r_b + r_t) / 2, cy + math.sin(a + hw * 0.6 + curl * 0.5) * (r_b + r_t) / 2)
        tip = (cx + math.cos(a + curl) * r_t, cy + math.sin(a + curl) * r_t)
        poly = [base_l, mid_l, tip, mid_r, base_r]
        ctx.poly(poly, tooth)
        ctx.line(poly, 1.8, tint(tooth, -0.42), 0.8, cap=False)
    ctx.circ(cx, cy, R * 0.05, glow, 0.9 * open_k)


def sarlacc(ctx, cx, cy, w, t=0.0, sand=Hx("#7A6A44"), pit=Hx("#2A1E14"), tooth=Hx("#EAD9AE"), n=26):
    """Sarlacc çukuru (üstten, eğik): kum halka, dişli ağız, dalgalanan dokunaçlar"""
    ry = w * 0.46
    pshape(ctx, circ_poly(cx, cy, w, ry, 44), sand, sh=(0, 8), sh_a=0.25, edge=0.2)
    ctx.poly(circ_poly(cx, cy + 3, w * 0.74, ry * 0.72, 40), tint(sand, -0.22))
    ctx.poly(circ_poly(cx, cy + 6, w * 0.6, ry * 0.58, 40), pit)
    for i in range(n):
        a = i * 2 * math.pi / n
        a2 = a + 2 * math.pi / n * 0.8
        px0, py0 = cx + math.cos(a) * w * 0.6, cy + 6 + math.sin(a) * ry * 0.58
        px1, py1 = cx + math.cos(a2) * w * 0.6, cy + 6 + math.sin(a2) * ry * 0.58
        am = (a + a2) / 2
        tx, ty = cx + math.cos(am) * w * 0.34, cy + 6 + math.sin(am) * ry * 0.32
        ctx.poly([(px0, py0), (px1, py1), (tx, ty)], tooth)
    ctx.circ(cx, cy + 8, w * 0.16, Hx("#0B0605"))
    for k in range(5):
        ang = -2.5 + k * 0.62
        pts = []
        for j in range(12):
            u = j / 11
            wob = math.sin(t * 2.4 + k * 1.3 + u * 5.0) * 14 * u
            pts.append((cx + math.cos(ang) * w * 0.5 * u + wob, cy + 4 - u * w * (0.5 + 0.18 * (k % 2))))
        ctx.line(pts, 11 - 6 * 0.0, Hx("#6C4A33"), 1.0)
        ctx.circ(pts[-1][0], pts[-1][1], 9, Hx("#8A6446"))


def harvester(ctx, x, y, s=1.0, t=0.0, body=Hx("#C06A2F"), dark=Hx("#3A1E14"), flip=1):
    """Baharat toplayıcısı: devasa paletli makine (yandan)"""
    X = Xf(x, y, s, flip=flip)
    # toz
    for i in range(7):
        u = (t * 0.9 + i / 7) % 1.0
        px, py = X.p(-190 - u * 140, -20 - u * 50)
        ctx.circ(px, py, 18 * s * (0.6 + u), (230, 190, 130), 0.28 * (1 - u))
    pshape(ctx, X.pts([(-170, 0), (160, 0), (160, 40), (-170, 40)]), dark, sh=(6 * s, 9 * s), sh_a=0.25)
    for wx in (-135, -68, 0, 68, 128):
        ctx.circ(*X.p(wx, 20), 17 * s, tint(dark, 0.18))
    pshape(ctx, X.pts([(-160, 0), (-160, -84), (-60, -112), (60, -112), (124, -62), (160, -62), (160, 0)]), body, sh=(6 * s, 8 * s), sh_a=0.22)
    pshape(ctx, X.pts([(160, -62), (222, -98), (222, -8), (160, -22)]), tint(body, -0.12), sh=(4 * s, 6 * s), sh_a=0.2)
    pshape(ctx, X.pts([(-24, -112), (64, -112), (64, -152), (-24, -152)]), tint(body, -0.05), sh=(3 * s, 5 * s), sh_a=0.2)
    ctx.poly(X.pts([(-12, -122), (52, -122), (52, -144), (-12, -144)]), Hx("#FFE3A8"))
    ctx.poly(X.pts([(-132, -84), (-112, -84), (-112, -150), (-132, -150)]), tint(dark, 0.1))
    for vx in (-120, -80, -40, 0):
        ctx.line(X.pts([(vx, -50), (vx + 22, -50)]), 3 * s, tint(body, -0.3), 0.8)


def sandcrawler(ctx, x, y, s=1.0, t=0.0, body=Hx("#8C7A5B"), dark=Hx("#2E2518"), flip=1):
    """Jawa kum aracı: eğimli gövde, aydınlık pencereler"""
    X = Xf(x, y, s, flip=flip)
    for i in range(6):
        u = (t * 0.8 + i / 6) % 1.0
        px, py = X.p(-190 - u * 120, -15 - u * 40)
        ctx.circ(px, py, 16 * s * (0.6 + u), (225, 195, 140), 0.26 * (1 - u))
    pshape(ctx, X.pts([(-176, 0), (176, 0), (176, 52), (-176, 52)]), dark, sh=(6 * s, 9 * s), sh_a=0.25)
    for wx in (-130, -62, 8, 78, 146):
        ctx.circ(*X.p(wx, 26), 24 * s, tint(dark, 0.14))
        ctx.circ(*X.p(wx, 26), 10 * s, tint(dark, -0.1))
    pshape(ctx, X.pts([(-182, 0), (-170, -76), (170, -76), (182, 0)]), body, sh=(5 * s, 7 * s), sh_a=0.22)
    pshape(ctx, X.pts([(-150, -76), (-106, -156), (96, -156), (146, -76)]), tint(body, -0.1), sh=(4 * s, 6 * s), sh_a=0.2)
    for i in range(6):
        wx = -80 + i * 34
        ctx.poly(X.pts([(wx, -118), (wx + 18, -118), (wx + 18, -132), (wx, -132)]), Hx("#FFC24A"))
    ctx.poly(X.pts([(176, -4), (232, 14), (176, 14)]), tint(body, -0.25))
    ctx.line(X.pts([(0, -156), (0, -200)]), 4 * s, dark, 1.0)


def spice(ctx, cx, cy, r, t=0.0, n=110, core=SPICE):
    """Baharat: mavi-altın tozdan dönen bulut"""
    ctx.glow(cx, cy, r * 1.35, core, 0.40)
    for i in range(n):
        u = i / n
        ang = i * 0.42 + t * (0.9 + 0.4 * u)
        rad = r * (u ** 0.75) * (0.8 + 0.2 * math.sin(t * 2 + i))
        x, y = cx + math.cos(ang) * rad, cy + math.sin(ang) * rad * 0.62
        c = mix(core, Hx("#FFD58A"), clamp(u * 1.3))
        ctx.circ(x, y, 2.0 + 3.6 * (1 - u) ** 0.6, c, 0.55 + 0.4 * (1 - u))


def guild_ship(ctx, x, y, s=1.0, col=Hx("#B9824A"), dark=INK):
    """Dev yük gemisi (uzun gövde, pencere sıraları)"""
    X = Xf(x, y, s)
    pshape(ctx, X.pts([(-200, -34), (180, -34), (214, 0), (180, 34), (-200, 34)]), col, sh=(6 * s, 9 * s), sh_a=0.25)
    for i in range(14):
        wx = -176 + i * 26
        ctx.poly(X.pts([(wx, -10), (wx + 12, -10), (wx + 12, 2), (wx, 2)]), Hx("#FFE3A8"))
    ctx.line(X.pts([(-200, 20), (190, 20)]), 3 * s, dark, 0.55)
    for ex in (-206, -206):
        ctx.glow(*X.p(ex, 0), 40 * s, SPICE, 0.5)


def fed_ship(ctx, x, y, s=1.0, col=Hx("#8FA6B2"), dark=Hx("#10202C")):
    """Disk gövdeli ticaret gemisi (halka + kubbeler)"""
    X = Xf(x, y, s)
    pshape(ctx, X.pts(circ_poly(0, 0, 118, 52, 40)), col, sh=(6 * s, 9 * s), sh_a=0.25)
    ctx.poly(X.pts(circ_poly(0, -8, 88, 34, 36)), tint(col, -0.12))
    for dx in (-60, 0, 60):
        pshape(ctx, X.pts(circ_poly(dx, -30, 20, 14, 18)), tint(col, 0.1), sh=(2, 3), sh_a=0.15)
    for dx in (-96, 96):
        ctx.glow(*X.p(dx, 6), 26 * s, SWYEL, 0.5)
        ctx.circ(*X.p(dx, 6), 5 * s, SWYEL)


# ───────────────────────── nesneler ─────────────────────────
def book(ctx, cx, cy, w=300, h=420, title="DUNE", sub="FRANK HERBERT", col=Hx("#C98A3A"), t=0.0, tilt=0.0):
    X = Xf(cx, cy, 1.0, rot=tilt)
    hw, hh = w / 2, h / 2
    pshape(ctx, X.pts([(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]), tint(col, -0.28), sh=(12, 16), sh_a=0.32, edge=0.1)   # arka kapak
    ctx.poly(X.pts([(hw - 2, -hh + 8), (hw + 14, -hh + 14), (hw + 14, hh - 4), (hw - 2, hh - 10)]), CREAM)               # sayfa kenarı
    for i in range(1, 9):
        yy = -hh + 14 + i * (h - 24) / 9
        ctx.line(X.pts([(hw, yy), (hw + 13, yy + 4)]), 1.5, CREAM_SH, 0.9, cap=False)
    pshape(ctx, X.pts([(-hw, -hh), (hw - 4, -hh), (hw - 4, hh), (-hw, hh)]), col, sh=(0, 0), sh_a=0.0, edge=0.18)
    ctx.poly(X.pts([(-hw, -hh), (-hw + 20, -hh), (-hw + 20, hh), (-hw, hh)]), tint(col, -0.22))
    # kapak resmi: kum tepesi + küçük figür
    ctx.poly(X.pts([(-hw + 20, 40), (-90, 10), (-20, 46), (60, 6), (hw - 4, 36), (hw - 4, hh), (-hw + 20, hh)]), tint(col, -0.34))
    ctx.poly(X.pts([(-hw + 20, 90), (-50, 62), (30, 96), (110, 58), (hw - 4, 84), (hw - 4, hh), (-hw + 20, hh)]), tint(col, -0.5))
    ctx.circ(*X.p(70, -30), 30, Hx("#FFF0C8"))
    ctx.poly(X.pts([(-30, 8), (-26, -14), (-22, 8)]), INK)
    tp = min(92, w * 0.30)
    ptext(ctx, *X.p(10, -hh + tp * 0.7), title, tp, Hx("#FFF4DA"), FONT_TITLE, shadow=(3, 4, tint(col, -0.55)))
    if sub:
        ptext(ctx, *X.p(10, -hh + tp * 0.7 + tp * 0.62), sub, max(14, w * 0.085), Hx("#FFE6B0"), FONT_BOLD)


def clapper(ctx, cx, cy, w=360, h=250, line1="STAR WARS", line2="1977", open_deg=24.0, col=INK):
    """Klaket: üst çubuk menteşeden açılır; open_deg=0 → kapalı"""
    pshape(ctx, [(cx - w / 2, cy - h / 2 + 34), (cx + w / 2, cy - h / 2 + 34), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], Hx("#242424"), sh=(10, 14), sh_a=0.32, edge=0.2)
    for i in range(1, 6):
        yy = cy - h / 2 + 34 + i * (h - 34) / 6
        ctx.line([(cx - w / 2 + 16, yy), (cx + w / 2 - 16, yy)], 2, (80, 80, 80), 0.7, cap=False)
    p1 = min(56, w * 0.145)
    ptext(ctx, cx, cy + h * 0.04, line1, p1, CREAM, FONT_TITLE)
    if line2:
        ptext(ctx, cx, cy + h * 0.04 + p1 * 1.15, line2, p1 * 0.82, SWYEL, FONT_BOLD)
    X = Xf(cx - w / 2, cy - h / 2 + 34, 1.0, rot=-open_deg)
    stick = [(0, 0), (w, 0), (w, -34), (0, -34)]
    pshape(ctx, X.pts(stick), Hx("#1A1A1A"), sh=(6, 8), sh_a=0.25, edge=0.2)
    for i in range(7):
        x0 = i * w / 7
        ctx.poly(X.pts([(x0, 0), (x0 + w / 14, 0), (x0 + w / 14 + 18, -34), (x0 + 18, -34)]), CREAM)


def marquee(ctx, cx, cy, w, h, line1, line2, t=0.0):
    """Sinema tabelası: ampuller yanıp söner"""
    pshape(ctx, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], Hx("#17192B"), sh=(10, 14), sh_a=0.32, edge=0.16)
    n = int(w // 40)
    for i in range(n + 1):
        x = cx - w / 2 + 14 + i * (w - 28) / n
        for yy in (cy - h / 2 + 12, cy + h / 2 - 12):
            on = (int(t * 4) + i) % 2 == 0
            ctx.glow(x, yy, 14, GOLD, 0.5 if on else 0.15)
            ctx.circ(x, yy, 5, GOLD if on else Hx("#7A6A3A"))
    ptext(ctx, cx, cy - 8, line1, h * 0.46, SWYEL, FONT_TITLE, shadow=(4, 5, (0, 0, 0)))
    ptext(ctx, cx, cy + h * 0.30, line2, h * 0.2, CREAM, FONT_BOLD)


def envelope(ctx, cx, cy, w=520, h=340, label="TEKLİF", seal="?", flap=1.0, t=0.0):
    X = Xf(cx, cy, 1.0)
    hw, hh = w / 2, h / 2
    pshape(ctx, X.pts([(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]), CREAM, sh=(12, 16), sh_a=0.32, edge=0.12)
    ctx.poly(X.pts([(-hw, hh), (0, 6), (hw, hh)]), CREAM_SH)
    ctx.line(X.pts([(-hw, hh), (0, 6), (hw, hh)]), 2.5, tint(CREAM_SH, -0.25), 0.8, cap=False)
    fl = [(-hw, -hh), (0, -hh + (hh + 8) * flap * 1.0 - (1 - flap) * 0), (hw, -hh)]
    ctx.poly(X.pts(fl), tint(CREAM, -0.06))
    ctx.line(X.pts(fl), 2.5, tint(CREAM_SH, -0.25), 0.8, cap=False)
    sx, sy = X.p(0, -hh + (hh + 8) * flap * 0.95)
    pcirc(ctx, sx, sy, 38, RED, sh=(3, 5), sh_a=0.3, edge=0.18)
    ptext(ctx, sx, sy + 2, seal, 48, Hx("#FFE0DC"), FONT_TITLE)
    ptext(ctx, cx, cy + hh * 0.42, label, 52, INK, FONT_BOLD)


def info_card(ctx, x0, y0, x1, y1, head, sub, col, icon=None, t=0.0, alpha=1.0):
    """Yatay bilgi kartı: solda simge kutusu, sağda başlık/alt başlık"""
    pshape(ctx, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], CREAM, sh=(8, 12), sh_a=0.30 * alpha)
    ctx.poly([(x0, y0), (x0 + (y1 - y0), y0), (x0 + (y1 - y0), y1), (x0, y1)], col)
    if icon:
        icon(ctx, x0 + (y1 - y0) / 2, (y0 + y1) / 2, (y1 - y0))
    ptext(ctx, x0 + (y1 - y0) + 26, (y0 + y1) / 2 - 26, head, 50, INK, FONT_TITLE, anchor="lm")
    ptext(ctx, x0 + (y1 - y0) + 26, (y0 + y1) / 2 + 32, sub, 44, Hx("#6A4E36"), FONT_BOLD, anchor="lm")


def icon_book(ctx, cx, cy, sz):
    s = sz / 170
    pshape(ctx, [(cx - 44 * s, cy - 56 * s), (cx + 44 * s, cy - 56 * s), (cx + 44 * s, cy + 56 * s), (cx - 44 * s, cy + 56 * s)], CREAM, sh=(4, 6), sh_a=0.25, edge=0.0)
    ctx.poly(circ_poly(cx, cy - 8 * s, 16 * s, n=14), INK)
    ctx.poly([(cx - 22 * s, cy + 40 * s), (cx - 14 * s, cy + 8 * s), (cx + 14 * s, cy + 8 * s), (cx + 22 * s, cy + 40 * s)], INK)


def icon_hat(ctx, cx, cy, sz):
    s = sz / 170
    ctx.poly([(cx - 54 * s, cy + 18 * s), (cx, cy - 40 * s), (cx + 54 * s, cy + 18 * s)], CREAM)
    ctx.line([(cx - 40 * s, cy + 48 * s), (cx + 48 * s, cy - 50 * s)], 6 * s, Hx("#E8E8E8"), 1.0)
    ctx.line([(cx - 52 * s, cy + 56 * s), (cx - 34 * s, cy + 40 * s)], 8 * s, INK, 1.0)


def icon_rocket(ctx, cx, cy, sz):
    s = sz / 170
    ctx.poly([(cx - 18 * s, cy + 46 * s), (cx - 18 * s, cy - 20 * s), (cx, cy - 58 * s), (cx + 18 * s, cy - 20 * s), (cx + 18 * s, cy + 46 * s)], CREAM)
    ctx.poly([(cx - 18 * s, cy + 14 * s), (cx - 44 * s, cy + 52 * s), (cx - 18 * s, cy + 42 * s)], RED)
    ctx.poly([(cx + 18 * s, cy + 14 * s), (cx + 44 * s, cy + 52 * s), (cx + 18 * s, cy + 42 * s)], RED)
    ctx.circ(cx, cy - 8 * s, 8 * s, Hx("#4AA8E0"))


def newspaper(ctx, cx, cy, w, h, head, hl_text, tag, t=0.0, hl_k=1.0, rot=-1.5):
    X = Xf(cx, cy, 1.0, rot=rot)
    hw, hh = w / 2, h / 2
    pshape(ctx, X.pts([(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]), Hx("#EFE3C0"), sh=(12, 16), sh_a=0.34, edge=0.1)
    ptext(ctx, *X.p(0, -hh + 56), head, 52, INK, FONT_SERIF)
    ctx.line(X.pts([(-hw + 30, -hh + 94), (hw - 30, -hh + 94)]), 4, INK, 0.8)
    ctx.line(X.pts([(-hw + 30, -hh + 104), (hw - 30, -hh + 104)]), 1.6, INK, 0.7)
    # gri metin satırları
    for col in range(2):
        x0 = -hw + 34 + col * (w / 2 - 6)
        for i in range(9):
            yy = -hh + 140 + i * 30
            ln = (w / 2 - 70) * (0.62 + 0.38 * rng_hash(i, col, 5))
            ctx.line(X.pts([(x0, yy), (x0 + ln, yy)]), 7, (120, 104, 84), 0.45, cap=False)
    # alıntı bandı
    by0, by1 = hh - 440, hh - 150
    k = clamp(hl_k)
    ctx.poly(X.pts([(-hw + 24, by0), (-hw + 24 + (w - 48) * k, by0), (-hw + 24 + (w - 48) * k, by1), (-hw + 24, by1)]), Hx("#FFD84A"), 0.85)
    if k > 0.35:
        ptext(ctx, *X.p(0, (by0 + by1) / 2), hl_text, 38, INK, FONT_SERIF, anchor="mm")
    ptext(ctx, *X.p(0, hh - 60), tag, 34, Hx("#6A4E36"), FONT_BOLD)


def chalkboard(ctx, cx, cy, w, h):
    pshape(ctx, [(cx - w / 2 - 22, cy - h / 2 - 22), (cx + w / 2 + 22, cy - h / 2 - 22), (cx + w / 2 + 22, cy + h / 2 + 22), (cx - w / 2 - 22, cy + h / 2 + 22)], Hx("#7B4E2B"), sh=(12, 16), sh_a=0.34)
    ctx.poly([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], Hx("#1F3B33"))
    for i in range(14):
        yy = cy - h / 2 + 30 + i * (h - 40) / 14
        ctx.line([(cx - w / 2 + 10, yy), (cx + w / 2 - 10, yy + (rng_hash(i, 3, 1) - 0.5) * 4)], 9, (255, 255, 255), 0.018, cap=False)


def tally(ctx, x, y, n, col=(244, 240, 224), gap=62, rowlen=4, size=76, k=1.0):
    """Çentik sayacı: her 5'te çapraz çizgi (4 dikey + 1 çapraz)"""
    groups = (n + 4) // 5
    shown = int(n * k)
    for g in range(groups):
        gx = x + (g % 4) * (rowlen * 24 + 64)
        gy = y + (g // 4) * (size + 36)
        cnt = min(5, shown - g * 5)
        for i in range(min(4, max(0, cnt))):
            wob = (rng_hash(g, i, 2) - 0.5) * 3
            ctx.line([(gx + i * 24 + wob, gy), (gx + i * 24 - wob, gy + size)], 6, col, 0.95)
        if cnt >= 5:
            ctx.line([(gx - 14, gy + size * 0.8), (gx + 3 * 24 + 14, gy + size * 0.2)], 6, col, 0.95)


def door(ctx, cx, cy, w=380, h=640, plate="D. LYNCH", knock=0.0, t=0.0):
    pshape(ctx, [(cx - w / 2 - 26, cy - h / 2 - 26), (cx + w / 2 + 26, cy - h / 2 - 26), (cx + w / 2 + 26, cy + h / 2), (cx - w / 2 - 26, cy + h / 2)], Hx("#4B3A2A"), sh=(10, 14), sh_a=0.3)
    pshape(ctx, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], Hx("#8A5A34"), sh=(0, 0), sh_a=0.0, edge=0.16)
    for (a, b, c, d) in ((-0.40, -0.44, -0.04, -0.06), (0.04, -0.44, 0.40, -0.06), (-0.40, 0.02, -0.04, 0.40), (0.04, 0.02, 0.40, 0.40)):
        x0, y0, x1, y1 = cx + w * a, cy + h * b, cx + w * c, cy + h * d
        ctx.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], tint(Hx("#8A5A34"), -0.16))
        ctx.line([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], 3, tint(Hx("#8A5A34"), 0.2), 0.8, cap=False)
    pcirc(ctx, cx + w * 0.34, cy + h * 0.06, 14, Hx("#E7C15A"))
    prect(ctx, cx - 74, cy - h / 2 + 26, cx + 74, cy - h / 2 + 76, Hx("#E7C15A"), sh=(3, 4), sh_a=0.25, edge=0.1)
    ptext(ctx, cx, cy - h / 2 + 52, plate, 30, INK, FONT_BOLD)
    if knock > 0:
        for j in range(3):
            u = clamp(knock * 3 - j)
            if 0 < u < 1:
                ctx.ring(cx + w * 0.1, cy - h * 0.02, 30 + 90 * u, 5, GOLD, 0.8 * (1 - u))


def tree(ctx, cx, base_y, t=0.0, grow=1.0):
    """Aile ağacı: ortak kök ve iki dal"""
    trunk = [(cx - 54, base_y), (cx - 34, base_y - 250 * grow), (cx + 34, base_y - 250 * grow), (cx + 54, base_y)]
    pshape(ctx, trunk, Hx("#6A4328"), sh=(6, 8), sh_a=0.25)
    for sgn in (-1, 1):
        x0, y0 = cx + sgn * 14, base_y - 240 * grow
        pts = []
        for j in range(14):
            u = j / 13
            pts.append((x0 + sgn * (40 + 260 * u * grow) * (0.8 + 0.2 * u), y0 - (330 * u ** 0.9) * grow))
        ctx.line(pts, 46, Hx("#6A4328"), 1.0)
        ctx.line([(x + 4, y - 4) for x, y in pts], 4, Hx("#8B5E3C"), 0.8, cap=False)
        for j in (4, 8):                                           # küçük dallar
            px, py = pts[j]
            ctx.line([(px, py), (px + sgn * 70 * grow, py - 40 * grow)], 22, Hx("#6A4328"), 1.0)


def crowd(ctx, x0, y0, rows, cols, s, col, t=0.0, spread=70):
    for r in range(rows):
        for c in range(cols):
            if rng_hash(r, c, 9) < 0.12:
                continue
            x = x0 + c * spread * s + (r % 2) * spread * s * 0.5 + (rng_hash(r, c, 1) - 0.5) * 12
            y = y0 + r * 38 * s + math.sin(t * 5 + c * 0.9 + r) * 1.5
            crowd_member(ctx, x, y, s * (0.8 + 0.12 * r), col)


def tagchip(ctx, x, y, text, px=34, col=CREAM, ink=INK, anchor="lm", pad=16, a=1.0):
    """Kâğıt etiket (rozet)"""
    if a <= 0.05:
        return x
    f = font(FONT_BOLD, px)
    wd = f.getlength(text)
    x0 = x if anchor == "lm" else x - wd / 2 - pad
    if anchor == "lm":
        x0 = x - pad
    x1 = x0 + wd + pad * 2
    pshape(ctx, [(x0, y - px * 0.8), (x1, y - px * 0.8), (x1, y + px * 0.8), (x0, y + px * 0.8)], col, sh=(4, 6), sh_a=0.28 * a, edge=0.0)
    ctx.text((x0 + x1) / 2, y + 2, text, px, ink, path=FONT_BOLD)
    return x1


def quote_card(ctx, cx, cy, w, h, lines, who, sub="", ink=INK, k=1.0):
    pshape(ctx, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], CREAM, sh=(12, 16), sh_a=0.34)
    ptext(ctx, cx - w / 2 + 70, cy - h / 2 + 90, "“", 190, GOLD, FONT_SERIF)
    n = len(lines)
    for i, ln in enumerate(lines):
        ptext(ctx, cx, cy - 40 + (i - (n - 1) / 2) * 62, ln, 46, ink, FONT_SERIF)
    ptext(ctx, cx, cy + h / 2 - 96, who, 40, RED, FONT_TITLE)
    if sub:
        ptext(ctx, cx, cy + h / 2 - 50, sub, 30, Hx("#6A4E36"), FONT_BOLD)


def director_chair(ctx, cx, cy, s=1.0, col=Hx("#2B3A55"), frame=Hx("#8A6A44")):
    """Yönetmen sandalyesi (ayak y = cy)"""
    X = Xf(cx, cy, s)
    for sgn in (-1, 1):                                    # çapraz ayaklar
        ctx.line(X.pts([(sgn * 80, 0), (-sgn * 80, -150)]), 12 * s, frame, 1.0)
    ctx.line(X.pts([(-92, -150), (92, -150)]), 12 * s, frame, 1.0)                       # oturak çıtası
    pshape(ctx, X.pts([(-88, -158), (88, -158), (88, -176), (-88, -176)]), col, sh=(4, 6), sh_a=0.25)   # koltuk
    pshape(ctx, X.pts([(-82, -190), (82, -190), (82, -300), (-82, -300)]), col, sh=(4, 6), sh_a=0.25)   # arkalık
    ctx.line(X.pts([(-92, -150), (-92, -312)]), 12 * s, frame, 1.0)
    ctx.line(X.pts([(92, -150), (92, -312)]), 12 * s, frame, 1.0)
    ctx.line(X.pts([(-110, -230), (110, -230)]), 12 * s, frame, 1.0)                     # kolçak
