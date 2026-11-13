"""Düz (flat) illüstrasyon parçaları: saat, saray, gemiler, maskot, zarf, fatura, efektler."""
import math

from engine import *  # noqa

D2R = math.pi / 180


# ═════════════════════════ SAAT ═════════════════════════
def _hand(ctx, cx, cy, ang, length, width, color, tail=0.0, alpha=1.0, decor=False):
    a = ang * D2R
    dx, dy = math.sin(a), -math.cos(a)
    nx, ny = -dy, dx
    def P(l, w):
        return (cx + dx * l + nx * w, cy + dy * l + ny * w)
    pts = [P(-tail, 0), P(0, width * 0.5), P(length * 0.18, width * 0.55), P(length * 0.62, width * 0.30),
           P(length, 0), P(length * 0.62, -width * 0.30), P(length * 0.18, -width * 0.55), P(0, -width * 0.5)]
    ctx.poly(pts, color, alpha)
    if decor:
        ctx.circ(*P(length * 0.55, 0), width * 0.55, color, alpha)


def clock(ctx, cx, cy, R, ha, ma, sa=None, ghost=0, ghost_step=14.0, numerals=True, glow_alpha=0.0, wedge=None):
    """Eski tip duvar saati. ha/ma/sa: derece (0=12, saat yönü)."""
    ctx.ell(cx + R * 0.05, cy + R * 0.08, R * 1.02, R * 1.02, (0, 0, 0), alpha=0.22)
    if glow_alpha > 0:
        ctx.glow(cx, cy, R * 1.5, C["gold"], glow_alpha)
    # gövde: koyu ahşap, ahşap vurgu, pirinç çerçeve
    ctx.circ(cx, cy, R, hexc("#4B2C1B"))
    ctx.circ(cx, cy, R * 0.965, hexc("#7A4A2B"))
    ctx.circ(cx, cy, R * 0.915, hexc("#E7B33F"))
    ctx.circ(cx, cy, R * 0.885, hexc("#B9811F"))
    ctx.circ(cx, cy, R * 0.86, hexc("#FFF4D6"))
    ctx.ring(cx, cy, R * 0.845, R * 0.012, hexc("#E4CFA0"))
    if wedge is not None:  # kırmızı geri sayım dilimi (derece aralığı, saat yönü)
        w0, w1, wal = wedge
        pts = [(cx, cy)] + [(cx + math.sin(math.radians(w0 + (w1 - w0) * k / 20)) * R * 0.84,
                             cy - math.cos(math.radians(w0 + (w1 - w0) * k / 20)) * R * 0.84) for k in range(21)]
        ctx.poly(pts, C["red"], wal)
    # dakika çizgileri
    n = 60
    for i in range(n):
        a = i * 6 * D2R
        major = i % 5 == 0
        r1 = R * (0.74 if major else 0.79)
        r2 = R * 0.83
        if R < 90 and not major:
            continue
        w = R * (0.026 if major else 0.010)
        ctx.line([(cx + math.sin(a) * r1, cy - math.cos(a) * r1), (cx + math.sin(a) * r2, cy - math.cos(a) * r2)],
                 max(w, 1.2), hexc("#2A1A12") if major else hexc("#7A5B3A"), cap=False)
    if numerals and R >= 140:
        for h in range(1, 13):
            a = h * 30 * D2R
            ctx.text(cx + math.sin(a) * R * 0.60, cy - math.cos(a) * R * 0.60 + R * 0.01, str(h), R * 0.17,
                     hexc("#3A2418"), path=FONT_LORA)
    # elde saat/dakika izleri (hızlı dönüşte)
    for g in range(ghost, 0, -1):
        al = 0.30 * (1 - g / (ghost + 1))
        _hand(ctx, cx, cy, ma - g * ghost_step, R * 0.76, R * 0.075, hexc("#1B2A41"), tail=R * 0.12, alpha=al)
    _hand(ctx, cx, cy, ha, R * 0.50, R * 0.095, hexc("#1B2A41"), tail=R * 0.10, decor=True)
    _hand(ctx, cx, cy, ma, R * 0.76, R * 0.075, hexc("#1B2A41"), tail=R * 0.12, decor=False)
    if sa is not None:
        _hand(ctx, cx, cy, sa, R * 0.80, R * 0.034, C["red"], tail=R * 0.20)
    ctx.circ(cx, cy, R * 0.055, hexc("#E7B33F"))
    ctx.circ(cx, cy, R * 0.025, C["red"] if sa is not None else hexc("#7A4A2B"))


# ═════════════════════════ ZARF ═════════════════════════
def wax_seal(ctx, X, x, y, r):
    ctx.circ(*X.p(x, y), X.len(r * 1.08), hexc("#8E1526"))
    ctx.circ(*X.p(x, y), X.len(r), hexc("#C8283B"))
    ctx.ring(*X.p(x, y), X.len(r * 0.72), X.len(r * 0.10), hexc("#E0505F"))
    ctx.circ(*X.p(x - r * 0.28, y - r * 0.30), X.len(r * 0.20), hexc("#F58A93"), alpha=0.7)


def envelope(ctx, cx, cy, s, rot=0.0, open_t=0.0, qmark=True, wob=0.0, glow=0.0, qs=1.0):
    X = Xf(cx, cy, s, rot=rot)
    if glow > 0:
        ctx.glow(cx, cy, 380 * s, C["gold"], glow)
    ctx.poly(X.pts([(-262, -166), (262, -166), (272, 188), (-252, 190)]), (0, 0, 0), 0.22)  # gölge
    body = [(-260, -170), (260, -170), (260, 170), (-260, 170)]
    ctx.poly(X.pts(body), hexc("#FFF1D3"))
    ctx.poly(X.pts([(-260, 170), (0, -20), (260, 170)]), hexc("#F2DBAA"))
    ctx.poly(X.pts([(-260, -170), (0, 40), (-260, 170)]), hexc("#F8E4B8"))
    ctx.poly(X.pts([(260, -170), (0, 40), (260, 170)]), hexc("#F5DFB0"))
    ctx.line(X.pts([(-260, 170), (0, -10), (260, 170)]), X.len(4), hexc("#D9BE83"), cap=False)
    apex = lerp(-18, -360, ease_out(open_t))
    inner = open_t > 0.45
    if inner:
        ctx.poly(X.pts([(-260, -170), (260, -170), (0, apex)]), hexc("#D9B26A"))
    else:
        ctx.poly(X.pts([(-260, -170), (260, -170), (0, apex)]), hexc("#EBCF98"))
        ctx.line(X.pts([(-260, -170), (0, apex), (260, -170)]), X.len(4), hexc("#CDAE72"), cap=False)
        if open_t < 0.2:
            wax_seal(ctx, X, 0, apex + 6, 44)
    ctx.line(X.pts([(-260, -170), (260, -170), (260, 170), (-260, 170), (-260, -170)]), X.len(5), hexc("#D9BE83"))
    if qmark:
        ctx.text(*X.p(0, 70), "?", 330 * s * qs, C["gold"], path=FONT_LORA, stroke=11 * s * qs, stroke_fill=C["navy"])


# ═════════════════════════ BULUT / DENİZ ═════════════════════════
def cloud(ctx, x, y, s, color=(255, 255, 255), alpha=0.95):
    for dx, dy, r in ((-60, 8, 38), (-18, -14, 50), (34, -4, 44), (74, 10, 32), (6, 14, 46)):
        ctx.circ(x + dx * s, y + dy * s, r * s, color, alpha)
    ctx.rect(x - 96 * s, y + 10 * s, x + 100 * s, y + 52 * s, color, alpha)


def waves(ctx, y0, y1, t, c0, c1, rows=7, amp=7, wl=150, x0=-200, x1=W + 200, speed=0.8, foam=True, clip_y=None):
    """Yatay dalga bantları: y0 üst, y1 alt; bantlar c0→c1 gradyanı"""
    if clip_y is None:
        ctx.vgrad(x0, y0 - 2, x1 + 30, y1 + 8, [(0, c0), (1, c1)])
    for i in range(rows):
        f = i / max(1, rows - 1)
        yt = lerp(y0, y1, f)
        yb = lerp(y0, y1, (i + 1) / rows) + amp * 2.2 + 6
        col = mix(c0, c1, f)
        if clip_y is not None:
            if yb < clip_y:
                continue
            yt = max(yt, clip_y)
        a = amp * (0.5 + f)
        w = wl * (0.7 + f * 0.8)
        pts = []
        x = x0
        while x <= x1 + 30:
            pts.append((x, yt + math.sin(x / w * 6.283 + t * speed * (1 + f) + i * 1.7) * a))
            x += 30
        pts += [(x1 + 30, yb), (x0, yb)]
        ctx.poly(pts, col)
        if foam and i % 2 == 1 and clip_y is None:
            for k in range(7):
                fx = x0 + ((k * 197 + i * 71 + t * 28 * (1 + f)) % (x1 - x0))
                fy = yt + math.sin(fx / w * 6.283 + t * speed * (1 + f) + i * 1.7) * a
                ctx.line([(fx - 24 * (0.6 + f), fy + 3), (fx + 24 * (0.6 + f), fy + 3)], 4 + 2 * f, C["foam"], 0.55)


def palm(ctx, x, y, s, t=0.0, lean=1, seed=0):
    X = Xf(x, y, s, flip=lean)
    sway = math.sin(t * 1.3 + seed) * 4
    trunk = [(0, 0), (10, -60), (22, -130), (24 + sway * 0.5, -200)]
    ctx.line(X.pts(trunk), X.len(18), hexc("#8A5A33"))
    ctx.line(X.pts([(5, -20), (15, -80)]), X.len(8), hexc("#A8754A"))
    top = (24 + sway * 0.5, -200)
    for i, (ang, ln) in enumerate(((-165, 120), (-130, 130), (-95, 105), (-55, 128), (-15, 122), (-190, 90), (20, 90))):
        a = (ang + sway * 1.5) * D2R
        ex, ey = top[0] + math.cos(a) * ln, top[1] + math.sin(a) * ln + 38
        mx, my = top[0] + math.cos(a) * ln * 0.5, top[1] + math.sin(a) * ln * 0.5 - 24
        nx, ny = -(ey - top[1]), (ex - top[0])
        nl = math.hypot(nx, ny) or 1
        nx, ny = nx / nl * 17, ny / nl * 17
        col = C["green"] if i % 2 else C["green_dk"]
        ctx.poly(X.pts([top, (mx + nx, my + ny), (ex, ey), (mx - nx, my - ny)]), col)
    ctx.circ(*X.p(top[0] - 6, top[1] + 8), X.len(9), hexc("#5C3B1E"))
    ctx.circ(*X.p(top[0] + 8, top[1] + 10), X.len(9), hexc("#5C3B1E"))


# ═════════════════════════ ALEV / DUMAN / PATLAMA ═════════════════════════
def flame(ctx, x, y, size, t, seed=0, alpha=1.0):
    f = 1 + 0.18 * math.sin(t * 17 + seed * 3.1) + 0.1 * math.sin(t * 29 + seed)
    w = size * 0.55
    ctx.poly([(x - w, y), (x - w * 0.5, y - size * 0.55 * f), (x - w * 0.1, y - size * 0.35),
              (x + w * 0.1, y - size * 1.0 * f), (x + w * 0.55, y - size * 0.45), (x + w, y)], C["fire"], alpha)
    ctx.poly([(x - w * 0.6, y), (x - w * 0.2, y - size * 0.45 * f), (x + w * 0.1, y - size * 0.7 * f),
              (x + w * 0.5, y)], C["orange"], alpha)
    ctx.poly([(x - w * 0.3, y), (x, y - size * 0.4 * f), (x + w * 0.3, y)], C["yellow"], alpha)


def smoke_puff(ctx, x, y, r, alpha=0.8, dark=0.0):
    base = mix(hexc("#E8E4E2"), C["smoke"], dark)
    ctx.circ(x, y, r, base, alpha)
    ctx.circ(x - r * 0.18, y - r * 0.22, r * 0.62, shade(base, 0.22), alpha)


def smoke_column(ctx, x, y, t, height=240, width=40, n=7, dark=0.5, seed=0, alpha=0.85, speed=0.45):
    for k in range(n):
        age = ((t * speed + k / n + rng_hash(seed, k) * 0.07) % 1.0)
        py = y - age * height
        px = x + math.sin(age * 5 + k * 1.9 + seed) * width * 0.6 + age * width * 0.5
        r = width * (0.5 + age * 1.1)
        smoke_puff(ctx, px, py, r, alpha * (1 - age) ** 0.7 * min(1, age * 6), dark)


def explosion(ctx, x, y, age, size=1.0, seed=0, debris=True):
    """age: saniye (0'dan)"""
    if age < 0:
        return
    a = age
    if a < 0.5:
        ctx.glow(x, y, 330 * size, C["orange"], 0.9 * (1 - a / 0.5) ** 1.5)
    if a < 0.18:
        ctx.glow(x, y, 220 * size * (0.5 + a * 4), (255, 245, 200), 1 - a / 0.18)
    # ateş topu
    if a < 0.9:
        k = ease_out(a / 0.9, 2)
        for i in range(6):
            ang = i * 1.05 + seed
            ox, oy = math.cos(ang) * 55 * size * k, math.sin(ang) * 40 * size * k - 25 * size * k
            r = (46 + 18 * (i % 3)) * size * (0.4 + k * 0.7)
            col = mix(C["yellow"], C["fire"], clamp(a / 0.5))
            ctx.circ(x + ox, y + oy, r, col, clamp(1 - a / 0.9) ** 0.8)
    # şok halkası
    if a < 0.5:
        ctx.ring(x, y, 260 * size * ease_out(a / 0.5), 14 * size * (1 - a / 0.5) + 2, (255, 240, 210), 0.6 * (1 - a / 0.5))
    # toz / duman (kısa ömürlü, hafif)
    for i in range(6):
        ang = -math.pi / 2 + (rng_hash(seed, i) - 0.5) * 2.2
        life = 1.3 + rng_hash(seed, i, 9) * 0.9
        if a > life:
            continue
        k = ease_out(a / life, 2)
        dist = (60 + 120 * rng_hash(seed, i, 3)) * size * k
        px = x + math.cos(ang) * dist
        py = y + math.sin(ang) * dist * 0.9 - 30 * size * k * 1.5
        r = (26 + 30 * rng_hash(seed, i, 5)) * size * (0.5 + k * 0.8)
        col = mix(C["dust"], C["smoke"], clamp(a / 1.2) * 0.7)
        ctx.circ(px, py, r, col, 0.55 * (1 - a / life) ** 0.9 * min(1, a * 8))
    if debris and a < 1.1:
        for i in range(12):
            ang = -math.pi / 2 + (rng_hash(seed, i, 11) - 0.5) * 3.0
            v = 300 + 380 * rng_hash(seed, i, 12)
            px = x + math.cos(ang) * v * a * size
            py = y + math.sin(ang) * v * a * size + 700 * a * a * size
            c = (C["white"], C["white_sh"], C["brown"], C["dust"])[i % 4]
            sz = (8 + 12 * rng_hash(seed, i, 13)) * size
            ctx.poly([(px - sz, py - sz * 0.6), (px + sz * 0.9, py - sz * 0.8), (px + sz, py + sz * 0.7), (px - sz * 0.7, py + sz)],
                     c, clamp(1.3 - a / 1.1))


def cannonball(ctx, x, y, r=9):
    ctx.circ(x, y, r, hexc("#1B1B1F"))
    ctx.circ(x - r * 0.3, y - r * 0.3, r * 0.35, hexc("#6C6C78"))


# ═════════════════════════ SARAY ═════════════════════════
def _wavy_flag(ctx, X, px, py, w, h, t, color, amp=6):
    n = 10
    top = [(px + w * i / n, py + math.sin(i * 0.9 - t * 8) * amp * (i / n)) for i in range(n + 1)]
    bot = [(px + w * i / n, py + h + math.sin(i * 0.9 - t * 8) * amp * (i / n)) for i in range(n, -1, -1)]
    ctx.poly(X.pts(top + bot), color)
    ctx.poly(X.pts([(x, y + (h * 0.42 if False else 0)) for x, y in top[:1]] + [top[0], (px, py + h)]), shade(color, -0.2))


def palace(ctx, ox, oy, s, dmg=0.0, t=0.0, flag=1.0, flag_show=True, flame_t=None, tilt=0.0):
    """Beyaz, kuleli saray. Orijinal taban merkezinde (ox,oy). dmg 0..1 hasar."""
    X = Xf(ox, oy, s)
    ctx.ell(*X.p(20, 4), 300 * s, 20 * s, hexc("#B98B4E"), 0.45)
    # kule (arkada)
    ctx.poly(X.pts([(118, -190), (118, -350), (192, -350), (192, -190)]), C["white"])
    ctx.poly(X.pts([(168, -190), (168, -350), (192, -350), (192, -190)]), C["white_sh"])
    ctx.rect(*X.p(108, -362), *X.p(202, -346), hexc("#B9A57C"))
    # ana gövde
    ctx.rect(*X.p(-262, -24), *X.p(262, 0), C["white_dk"])
    ctx.rect(*X.p(-240, -196), *X.p(240, -24), C["white"])
    ctx.rect(*X.p(150, -196), *X.p(240, -24), C["white_sh"])
    ctx.rect(*X.p(-248, -212), *X.p(248, -194), C["white_dk"])
    # korkuluk / mazgal
    for i in range(-12, 12):
        x = i * 20 + 4
        if dmg > 0.5 and rng_hash(i, 77) < dmg * 0.55:
            continue
        ctx.rect(*X.p(x, -230), *X.p(x + 12, -212), C["white_sh"] if x > 150 else C["white"])
    # orta köşk + kiremit çatı
    ctx.rect(*X.p(-100, -262), *X.p(100, -212), C["white"])
    ctx.rect(*X.p(40, -262), *X.p(100, -212), C["white_sh"])
    ctx.poly(X.pts([(-118, -262), (-72, -312), (72, -312), (118, -262)]), hexc("#D2653A"))
    ctx.poly(X.pts([(60, -312), (72, -312), (118, -262), (96, -262)]), hexc("#B24E2A"))
    ctx.rect(*X.p(-120, -270), *X.p(120, -258), hexc("#E88B5B"))
    # alt kemerli galeri
    for i in range(-4, 5):
        cx = i * 52
        dark = hexc("#1E6C7A") if i != 0 else hexc("#14515E")
        ctx.rect(*X.p(cx - 19, -90), *X.p(cx + 19, -24), dark)
        ctx.ell(*X.p(cx, -90), X.len(19), X.len(19), dark)
        ctx.rect(*X.p(cx - 13, -86), *X.p(cx + 13, -24), shade(dark, 0.18))
        ctx.ell(*X.p(cx, -86), X.len(13), X.len(13), shade(dark, 0.18))
    ctx.rect(*X.p(-1, -26), *X.p(1, -24), hexc("#000000"), 0)
    # balkon
    ctx.rect(*X.p(-244, -108), *X.p(244, -98), hexc("#8B5A2B"))
    for i in range(-23, 24):
        ctx.rect(*X.p(i * 10.5 - 1.5, -124), *X.p(i * 10.5 + 1.5, -108), hexc("#8B5A2B"))
    ctx.rect(*X.p(-244, -128), *X.p(244, -122), hexc("#8B5A2B"))
    # üst kat pencereleri
    for i in range(-4, 5):
        cx = i * 52
        if i == 0:
            continue
        ctx.rect(*X.p(cx - 16, -178), *X.p(cx + 16, -138), hexc("#2A8C7E"))
        ctx.ell(*X.p(cx, -178), X.len(16), X.len(16), hexc("#2A8C7E"))
        ctx.rect(*X.p(cx - 3, -190), *X.p(cx + 3, -138), hexc("#E8F3EA"))
    # merkezi altın kapı
    ctx.rect(*X.p(-24, -190), *X.p(24, -130), hexc("#C9962E"))
    ctx.ell(*X.p(0, -190), X.len(24), X.len(24), hexc("#C9962E"))
    ctx.rect(*X.p(-16, -184), *X.p(16, -130), hexc("#FFD76A"))
    ctx.ell(*X.p(0, -184), X.len(16), X.len(16), hexc("#FFD76A"))
    # kule detayları
    ctx.rect(*X.p(138, -330), *X.p(150, -300), hexc("#2A8C7E"))
    ctx.rect(*X.p(160, -330), *X.p(172, -300), hexc("#2A8C7E"))
    broken = dmg > 0.7
    if not broken:
        ctx.ell(*X.p(155, -362), X.len(52), X.len(40), hexc("#2A9D8F"))
        ctx.rect(*X.p(100, -362), *X.p(210, -346), hexc("#B9A57C"))
        ctx.rect(*X.p(153, -430), *X.p(157, -396), hexc("#C9962E"))
        ctx.circ(*X.p(155, -432), X.len(7), C["gold"])
    else:
        ctx.poly(X.pts([(118, -350), (130, -372), (142, -352), (158, -384), (172, -354), (186, -368), (192, -350)]), C["white"])
    # saat (kule yüzü)
    ctx.circ(*X.p(155, -278), X.len(24), hexc("#CDBE9F"))
    ctx.circ(*X.p(155, -278), X.len(19), C["paper"])
    ctx.line([X.p(155, -278), X.p(155, -292)], X.len(3.5), hexc("#222222"))
    ctx.line([X.p(155, -278), X.p(165, -272)], X.len(3.5), hexc("#222222"))
    # hasar
    if dmg > 0.05:
        k = clamp(dmg)
        scorches = [(-150, -150, 70, 50), (80, -120, 80, 55), (-30, -240, 60, 30), (170, -160, 50, 60), (-210, -100, 40, 40), (10, -60, 70, 36)]
        for i, (sx, sy, rw, rh) in enumerate(scorches):
            if k * 6 > i + 0.2:
                ctx.ell(*X.p(sx, sy), X.len(rw), X.len(rh), hexc("#2B2223"), 0.55)
        holes = [(-160, -158, 38), (100, -132, 44), (-20, -246, 34), (180, -140, 30)]
        for i, (hx, hy, hs) in enumerate(holes):
            if k * 4.2 > i + 0.3:
                g = clamp(k * 4.2 - i)
                ctx.poly(X.pts([(hx - hs, hy + hs * 0.6), (hx - hs * 0.5, hy - hs * 0.9), (hx + hs * 0.1, hy - hs * 0.5),
                                (hx + hs * 0.8, hy - hs * 0.8), (hx + hs, hy + hs * 0.5), (hx, hy + hs * 0.9)]), hexc("#3A2A2A"), g)
                if flame_t is not None and k > 0.3:
                    ctx.glow(*X.p(hx, hy), X.len(hs * 2.2), C["orange"], 0.45 * g)
        # çatlaklar
        for i, pts in enumerate((((-60, -190), (-48, -160), (-62, -140), (-50, -110)), ((60, -196), (72, -170), (58, -150), (66, -120)),
                                  ((-210, -190), (-198, -160), (-208, -135)))):
            if k * 5 > i + 0.5:
                ctx.line(X.pts(pts), X.len(4), hexc("#6B5B45"), cap=False)
        if flame_t is not None and k > 0.25:
            for i, (fx, fy, fs) in enumerate(((-160, -214, 50), (100, -190, 56), (-20, -300, 44), (178, -350, 40))):
                if k * 4.2 > i + 0.5:
                    gx, gy = X.p(fx, fy)
                    flame(ctx, gx, gy, fs * s * 1.3, flame_t, seed=i + 1)
    # direk + bayrak
    pole_top = -470
    ctx.line(X.pts([(-60, -312), (-60, pole_top)]), X.len(5), hexc("#6B5B45"))
    ctx.circ(*X.p(-60, pole_top), X.len(6), C["gold"])
    if flag_show:
        fy = lerp(-330, -450, clamp(flag))
        _wavy_flag(ctx, X, -57, fy, 92, 56, t, C["red"], amp=7 * (0.4 + 0.6 * clamp(flag)))
    if dmg > 0.4:
        pass


# ═════════════════════════ GEMİ ═════════════════════════
def union_jack(ctx, X, x, y, w, h):
    ctx.rect(*X.p(x, y), *X.p(x + w, y + h), hexc("#1B3A8C"))
    ctx.line([X.p(x, y), X.p(x + w, y + h)], X.len(h * 0.28), (255, 255, 255), cap=False)
    ctx.line([X.p(x, y + h), X.p(x + w, y)], X.len(h * 0.28), (255, 255, 255), cap=False)
    ctx.line([X.p(x + w / 2, y), X.p(x + w / 2, y + h)], X.len(h * 0.42), (255, 255, 255), cap=False)
    ctx.line([X.p(x, y + h / 2), X.p(x + w, y + h / 2)], X.len(h * 0.42), (255, 255, 255), cap=False)
    ctx.line([X.p(x + w / 2, y), X.p(x + w / 2, y + h)], X.len(h * 0.2), hexc("#D7263D"), cap=False)
    ctx.line([X.p(x, y + h / 2), X.p(x + w, y + h / 2)], X.len(h * 0.2), hexc("#D7263D"), cap=False)


def ship_gun_tips(ox, oy, s, rot=0.0, angs=(-16, -16), recoil=(0, 0)):
    X = Xf(ox, oy, s, rot=rot)
    out = []
    for (tx, ty), a, rc in zip(((138, -62), (-150, -62)), angs, recoil):
        L = 76 - 14 * rc
        out.append(X.p(tx + math.cos(a * D2R) * L, ty + math.sin(a * D2R) * L))
    return out


def _R(ctx, X, x0, y0, x1, y1, color, alpha=1.0):
    ctx.poly(X.pts([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]), color, alpha)


def ship(ctx, ox, oy, s, t, rot=0.0, angs=(-16, -16), recoil=(0.0, 0.0), smoke=1.0, seed=0, sultan=False, dmg=0.0):
    """Sağa bakan savaş gemisi. (ox,oy) su çizgisinin merkezi. sultan=True: sultanın beyaz yatı."""
    X = Xf(ox, oy, s, rot=rot)
    if not sultan:
        hull_c, super_c, fun_c = hexc("#27323F"), hexc("#EFE2C2"), hexc("#E5B96B")
        hull = [(-232, -40), (212, -40), (252, -64), (238, -12), (204, 22), (-204, 22), (-238, -8)]
        ctx.poly(X.pts(hull), hull_c)
        ctx.poly(X.pts([(-236, -14), (240, -16), (238, -8), (-238, -6)]), hexc("#DAD3BF"))
        ctx.poly(X.pts([(-236, -6), (238, -8), (204, 22), (-204, 22), (-238, -8)]), hexc("#8C2B2F"))
        ctx.line(X.pts([(-225, -34), (205, -34)]), X.len(3), hexc("#3A4858"), cap=False)
        # güverte yapıları
        _R(ctx, X, -72, -98, 76, -40, super_c)
        _R(ctx, X, 40, -98, 76, -40, shade(super_c, -0.12))
        for i in range(5):
            _R(ctx, X, -60 + i * 28, -84, -44 + i * 28, -66, hexc("#2B4A5C"))
        _R(ctx, X, -82, -108, 86, -98, hexc("#6E4B2C"))
        _R(ctx, X, -34, -134, 34, -108, super_c)
        _R(ctx, X, -24, -126, 24, -116, hexc("#2B4A5C"))
        # bacalar
        for fx in (-118, 40):
            _R(ctx, X, fx, -176, fx + 36, -98, fun_c)
            _R(ctx, X, fx + 22, -176, fx + 36, -98, shade(fun_c, -0.15))
            _R(ctx, X, fx - 3, -176, fx + 39, -156, hexc("#1C1C1E"))
        # direkler
        ctx.line(X.pts([(176, -64), (176, -214)]), X.len(6), hexc("#4A2E1A"))
        ctx.line(X.pts([(-196, -56), (-196, -190)]), X.len(6), hexc("#4A2E1A"))
        ctx.line(X.pts([(150, -170), (202, -170)]), X.len(4), hexc("#4A2E1A"), cap=False)
        ctx.line(X.pts([(-218, -150), (-174, -150)]), X.len(4), hexc("#4A2E1A"), cap=False)
        _R(ctx, X, 168, -190, 184, -176, hexc("#4A2E1A"))
        for a, b in (((176, -214), (252, -66)), ((176, -214), (118, -42)), ((-196, -190), (-232, -42)), ((-196, -190), (-140, -42))):
            ctx.line(X.pts([a, b]), X.len(2), hexc("#2A2A2A"), 0.55, cap=False)
        # flama
        wv = math.sin(t * 6 + seed) * 5
        ctx.poly(X.pts([(176, -214), (232, -208 + wv), (176, -198)]), C["red"])
        ctx.line(X.pts([(-232, -42), (-232, -100)]), X.len(3.5), hexc("#4A2E1A"))
        union_jack(ctx, X, -230, -104 + wv * 0.15, 54, 32)
        # toplar
        for (tx, ty), a, rc in zip(((138, -62), (-150, -62)), angs, recoil):
            L = 76 - 14 * rc
            ex, ey = tx + math.cos(a * D2R) * L, ty + math.sin(a * D2R) * L
            ctx.line(X.pts([(tx, ty), (ex, ey)]), X.len(15), hexc("#1E252E"))
            ctx.circ(*X.p(ex, ey), X.len(9.5), hexc("#11161C"))
            ctx.ell(*X.p(tx, ty + 2), X.len(26), X.len(20), hexc("#1E252E"))
            ctx.ell(*X.p(tx - 5, ty - 4), X.len(10), X.len(6), hexc("#47525F"))
        smoke_x = (-100, 58)
    else:
        hull = [(-200, -34), (178, -34), (222, -50), (205, -8), (175, 20), (-170, 20), (-205, -8)]
        ctx.poly(X.pts(hull), hexc("#F6EEDB"))
        ctx.poly(X.pts([(-205, -14), (205, -14), (200, -6), (-203, -6)]), C["gold"])
        ctx.poly(X.pts([(-203, -6), (200, -6), (175, 20), (-170, 20)]), hexc("#8C2B2F"))
        _R(ctx, X, -100, -84, 90, -34, hexc("#FFF8EC"))
        _R(ctx, X, 50, -84, 90, -34, C["white_sh"])
        for i in range(6):
            ctx.ell(*X.p(-84 + i * 28, -62), X.len(8), X.len(10), hexc("#2B4A5C"))
        _R(ctx, X, -110, -96, 100, -84, C["gold"])
        ctx.poly(X.pts([(-60, -150), (-60, -96), (-100, -96)]), hexc("#FFF8EC"))
        ctx.poly(X.pts([(-60, -150), (-60, -96), (80, -96), (50, -142)]), hexc("#FFE9B8"))
        ctx.line(X.pts([(-60, -96), (-60, -176)]), X.len(5), hexc("#4A2E1A"))
        wv = math.sin(t * 6 + seed) * 5
        ctx.poly(X.pts([(-58, -176), (-8, -170 + wv), (-58, -150)]), C["red"])
        _R(ctx, X, 110, -130, 142, -84, hexc("#C13B2E"))
        _R(ctx, X, 110, -130, 142, -112, hexc("#1C1C1E"))
        ctx.line(X.pts([(-200, -34), (-200, -92)]), X.len(3.5), hexc("#4A2E1A"))
        ctx.poly(X.pts([(-198, -92), (-160, -88 + wv * 0.3), (-198, -66)]), C["red"])
        smoke_x = (126,)
    # funda: duman
    if smoke > 0:
        for sx in smoke_x:
            gx, gy = X.p(sx, -180 if not sultan else -138)
            smoke_column(ctx, gx - 6 * s, gy, t + seed, height=170 * s * smoke, width=18 * s, n=5, dark=0.6, seed=seed + sx,
                         alpha=0.8, speed=0.5)


def muzzle_flash(ctx, x, y, age, s=1.0, ang=-16):
    if age < 0 or age > 0.5:
        return
    k = age / 0.5
    ctx.glow(x, y, 190 * s * (1 + k * 0.4), C["orange"], 0.95 * (1 - k) ** 1.2)
    if age < 0.14:
        a = ang * D2R
        L = 120 * s * (1 - age / 0.14 * 0.4)
        tip = (x + math.cos(a) * L, y + math.sin(a) * L)
        n = (-math.sin(a) * 22 * s, math.cos(a) * 22 * s)
        ctx.poly([(x + n[0], y + n[1]), tip, (x - n[0], y - n[1]), (x - math.cos(a) * 18 * s, y - math.sin(a) * 18 * s)], C["yellow"])
        ctx.poly([(x + n[0] * 0.5, y + n[1] * 0.5), (x + (tip[0] - x) * 0.6, y + (tip[1] - y) * 0.6), (x - n[0] * 0.5, y - n[1] * 0.5)],
                 (255, 250, 230))
    # barut dumanı
    for i in range(4):
        r = (26 + i * 12) * s * (0.6 + k)
        smoke_puff(ctx, x + (i * 26 + 28 * k * 3) * s, y - (6 + i * 5 + 40 * k) * s, r, 0.85 * (1 - k) ** 0.8, 0.25)


# ═════════════════════════ MASKOT: ZAMAN KURYESİ + AT ═════════════════════════
def _leg(ctx, X, hx, hy, ang_up, bend, col, hoof, up=64, lo=72, w=32):
    a1 = ang_up * D2R
    kx, ky = hx + math.sin(a1) * up, hy + math.cos(a1) * up
    a2 = (ang_up - bend) * D2R
    fx, fy = kx + math.sin(a2) * lo, ky + math.cos(a2) * lo
    ctx.line(X.pts([(hx, hy), (kx, ky)]), X.len(w), col)
    ctx.circ(*X.p(kx, ky), X.len(w * 0.5), col)
    ctx.line(X.pts([(kx, ky), (fx, fy - 8)]), X.len(w * 0.68), col)
    ctx.ell(*X.p(fx + 4, fy - 3), X.len(14), X.len(10), hoof)
    return fx, fy


def courier(ctx, ox, oy, s, phase, flip=1, env=True, env_spin=0.0, expression=0):
    """At üstünde Zaman Kuryesi. (ox,oy): atın ayak hizası/gövde ortası altı. phase: dörtnala fazı (radyan)."""
    X = Xf(ox, oy, s, flip=flip)
    brown, brown_d, brown_l = hexc("#8B5A2B"), hexc("#5E3A1B"), hexc("#A97444")
    hoof = hexc("#2B1A10")
    bob = -9 * abs(math.sin(phase * 0.5 + 0.4)) - 4
    # gölge
    ctx.ell(*X.p(0, 8), X.len(190), X.len(16), (0, 0, 0), 0.22)
    # uzak bacaklar (koyu)
    legs = [
        # (hx, off, far)
        (-112, math.pi * 0.0 + 0.5, True), (80, math.pi * 0.0 + 1.2, True),
    ]
    sw = lambda o: math.sin(phase + o)
    lf = lambda o: max(0.0, math.cos(phase + o))
    for hx, o, _ in legs:
        _leg(ctx, X, hx, -138 + bob, 36 * sw(o) + 6, 10 + 70 * lf(o), brown_d, hoof)
    # kuyruk
    wv = math.sin(phase * 1.0)
    tp = [(-128, -208 + bob), (-186, -208 + bob + wv * 5), (-244, -184 + bob + wv * 16), (-282, -138 + bob + wv * 26)]
    ctx.line(X.pts(tp), X.len(36), brown_d)
    ctx.line(X.pts(tp[1:]), X.len(24), hexc("#2E1B0E"))
    ctx.line(X.pts([tp[2], tp[3], (-292, -112 + bob + wv * 30)]), X.len(12), hexc("#2E1B0E"))
    # gövde
    ctx.ell(*X.p(0, -188 + bob), X.len(142), X.len(64), brown)
    ctx.ell(*X.p(4, -168 + bob), X.len(122), X.len(38), brown_l)
    ctx.ell(*X.p(0, -208 + bob), X.len(128), X.len(36), brown, 0.0)
    # boyun + baş
    ctx.poly(X.pts([(62, -236 + bob), (152, -322 + bob), (212, -282 + bob), (136, -150 + bob)]), brown)
    ctx.poly(X.pts([(112, -176 + bob), (176, -268 + bob), (212, -282 + bob), (136, -150 + bob)]), brown_l, 0.55)
    ctx.poly(X.pts([(152, -326 + bob), (206, -322 + bob), (272, -262 + bob), (266, -238 + bob), (226, -244 + bob), (186, -262 + bob)]), brown)
    ctx.ell(*X.p(262, -250 + bob), X.len(20), X.len(15), hexc("#D1A173"))
    ctx.circ(*X.p(268, -254 + bob), X.len(3.5), hexc("#3A2412"))
    ctx.circ(*X.p(200, -300 + bob), X.len(7), (20, 14, 10))
    ctx.circ(*X.p(202, -302 + bob), X.len(2.5), (255, 255, 255))
    ctx.poly(X.pts([(158, -322 + bob), (166, -358 + bob), (186, -324 + bob)]), brown_d)
    # yele
    fl = math.sin(phase + 1.2)
    mane = hexc("#2E1B0E")
    ctx.poly(X.pts([(58, -240 + bob), (150, -330 + bob), (160, -326 + bob), (140, -316 + bob), (70, -226 + bob)]), mane)
    for i in range(5):
        px, py = lerp(70, 150, i / 4), lerp(-236, -324, i / 4)
        ctx.poly(X.pts([(px, py + bob), (px - 28 - fl * 8, py - 10 + bob + fl * 6), (px - 8, py + 14 + bob)]), mane)
    # eyer örtüsü
    ctx.rrect(*X.p(-40, -250 + bob), *X.p(70, -176 + bob), X.len(10), C["red"]) if False else None
    ctx.poly(X.pts([(-42, -246 + bob), (66, -246 + bob), (74, -176 + bob), (-48, -176 + bob)]), C["red"])
    ctx.line(X.pts([(-46, -182 + bob), (72, -182 + bob)]), X.len(7), C["gold"], cap=False)
    # ── Kurye: gövde ──
    # kaftan eteği (arkaya savrulan)
    sk = math.sin(phase * 1.0 + 0.7)
    ctx.poly(X.pts([(-32, -248 + bob), (-96, -236 + bob + sk * 8), (-120, -196 + bob + sk * 14), (-70, -200 + bob), (-24, -214 + bob)]),
             hexc("#1B2A5A"))
    # bacak/bot
    ctx.line(X.pts([(-2, -238 + bob), (44, -204 + bob)]), X.len(34), hexc("#1B2850"))
    ctx.line(X.pts([(44, -204 + bob), (32, -150 + bob)]), X.len(28), hexc("#3B2418"))
    ctx.ell(*X.p(34, -144 + bob), X.len(24), X.len(10), hexc("#2A170C"))
    # yakın bacaklar (at) - önde
    for hx, o in ((-98, math.pi + 0.2), (96, math.pi + 0.9)):
        _leg(ctx, X, hx, -138 + bob, 36 * sw(o) + 6, 10 + 70 * lf(o), brown, hoof)
    # gövde (kaftan)
    ctx.poly(X.pts([(-34, -242 + bob), (30, -242 + bob), (58, -338 + bob), (-6, -354 + bob)]), hexc("#23386B"))
    ctx.poly(X.pts([(-34, -242 + bob), (-6, -354 + bob), (14, -350 + bob), (-6, -242 + bob)]), hexc("#1B2A5A"))
    ctx.line(X.pts([(30, -242 + bob), (58, -338 + bob)]), X.len(6), C["gold"], cap=False)
    ctx.poly(X.pts([(-34, -270 + bob), (35, -270 + bob), (39, -252 + bob), (-36, -252 + bob)]), C["gold"])
    ctx.rect(*X.p(-4, -272 + bob), *X.p(10, -250 + bob), hexc("#B9811F"))
    # kol + dizgin
    sh = (26, -332 + bob)
    el = (62, -296 + bob + math.sin(phase) * 4)
    hd = (112, -306 + bob + math.sin(phase + 0.5) * 5)
    ctx.line(X.pts([sh, el]), X.len(26), hexc("#23386B"))
    ctx.line(X.pts([el, hd]), X.len(22), hexc("#2B4382"))
    ctx.circ(*X.p(*hd), X.len(13), hexc("#F4C7A1"))
    ctx.line(X.pts([hd, (268, -256 + bob)]), X.len(3.5), hexc("#2A170C"), cap=False)
    if env:
        ex, ey = hd[0] + 20, hd[1] - 30
        E = Xf(*X.p(ex, ey), s * 0.42, flip=flip, rot=-14 + env_spin)
        ctx.poly(E.pts([(-70, -46), (70, -46), (70, 46), (-70, 46)]), hexc("#FFF1D3"))
        ctx.poly(E.pts([(-70, -46), (70, -46), (0, 8)]), hexc("#EBCF98"))
        ctx.circ(*E.p(0, 8), E.len(13), hexc("#C8283B"))
    # ── Baş ──
    hc = (34, -402 + bob + 2 * math.sin(phase + 0.8))
    # örgüler
    for k, (oy_, col) in enumerate(((0, hexc("#16161A")), (22, hexc("#202026")))):
        pts = []
        for i in range(7):
            pts.append((hc[0] - 40 - i * 17, hc[1] + 8 + oy_ + math.sin(phase * 1.0 + i * 0.9 + k) * (4 + i * 2.2)))
        ctx.line(X.pts(pts), X.len(15), col)
        ex, ey = pts[-1]
        ctx.circ(*X.p(ex, ey), X.len(8), C["red"])
    ctx.circ(*X.p(*hc), X.len(54), hexc("#F4C7A1"))
    ctx.ell(*X.p(hc[0] - 6, hc[1] + 10), X.len(46), X.len(40), hexc("#F8D3B0"), 0.0)
    ctx.circ(*X.p(hc[0] - 52, hc[1] + 4), X.len(10), hexc("#E8AE86"))  # kulak
    # yanaklar
    ctx.circ(*X.p(hc[0] + 31, hc[1] + 18), X.len(13), hexc("#FF8FA3"), 0.85)
    ctx.circ(*X.p(hc[0] - 22, hc[1] + 20), X.len(11), hexc("#FF8FA3"), 0.8)
    # gözler
    blink = 1.0
    for ex, er in ((hc[0] + 24, 1.0), (hc[0] - 6, 0.85)):
        ctx.ell(*X.p(ex, hc[1] - 2), X.len(6.5 * er), X.len(9 * er * blink), (24, 16, 12))
        ctx.circ(*X.p(ex + 2, hc[1] - 5), X.len(2.6 * er), (255, 255, 255))
    ctx.line(X.pts([(hc[0] + 14, hc[1] - 18), (hc[0] + 34, hc[1] - 16)]), X.len(3.5), (30, 20, 14), cap=True)
    ctx.line(X.pts([(hc[0] - 16, hc[1] - 16), (hc[0] + 2, hc[1] - 18)]), X.len(3), (30, 20, 14), cap=True)
    ctx.poly(X.pts([(hc[0] + 40, hc[1] + 2), (hc[0] + 48, hc[1] + 10), (hc[0] + 38, hc[1] + 11)]), hexc("#E8A87F"))
    # gülümseme
    ctx.arc(*X.p(hc[0] + 18, hc[1] + 20), X.len(15), 20 if flip == 1 else 20, 160, X.len(3.5), (150, 50, 50)) if False else None
    mpts = [(hc[0] + 4 + i * 4.2, hc[1] + 24 + math.sin(i / 7 * math.pi) * 8) for i in range(8)]
    ctx.line(X.pts(mpts), X.len(3.6), hexc("#A33A3A"))
    # ── Şapka ──
    hb = 3 * math.sin(phase + 0.3)
    brim_y = hc[1] - 42 + hb
    crown = [(hc[0] - 52, brim_y)]
    for i in range(0, 19):
        a = math.pi + math.pi * i / 18
        crown.append((hc[0] + math.cos(a) * 56, brim_y + math.sin(a) * 74))
    ctx.poly(X.pts(crown), hexc("#B3261E"))
    ctx.poly(X.pts([(hc[0] + 10, brim_y - 70), (hc[0] + 56, brim_y), (hc[0] + 30, brim_y)]), hexc("#8E1B15"), 0.6)
    ctx.line(X.pts([(hc[0] - 44, brim_y - 22), (hc[0] + 44, brim_y - 22)]), X.len(5), C["gold"], cap=False)
    ctx.rrect(*X.p(hc[0] - 66, brim_y - 16), *X.p(hc[0] + 66, brim_y + 18), X.len(16), hexc("#6B3E26"))
    for i in range(8):
        fx = hc[0] - 56 + i * 16
        ctx.ell(*X.p(fx, brim_y + (i % 2) * 8 - 3), X.len(7), X.len(4), hexc("#8A5733"))
    ctx.line(X.pts([(hc[0], brim_y - 74), (hc[0], brim_y - 86)]), X.len(5), C["gold_dk"])
    ctx.circ(*X.p(hc[0], brim_y - 96), X.len(14), C["gold"])
    ctx.circ(*X.p(hc[0] - 4, brim_y - 100), X.len(5), (255, 241, 168))
    return X.p(hd[0] + 20, hd[1] - 30)


# ═════════════════════════ FATURA (PARŞÖMEN) ═════════════════════════
def parchment_h(ctx, x0, y, w, h, open_t):
    """Yatay açılan ültimatom parşömeni: x0 sol, genişlik w, yükseklik h"""
    wo = max(10.0, w * open_t)
    ctx.ell(x0 + wo / 2 + 6, y + h / 2 + 10, wo / 2 + 12, h / 2 + 4, (0, 0, 0), 0.0)
    ctx.rect(x0 + 6, y + 8, x0 + wo + 6, y + h + 8, (0, 0, 0), 0.18)
    ctx.rect(x0, y, x0 + wo, y + h, C["paper"])
    ctx.rect(x0, y, x0 + wo, y + 8, C["paper_dk"])
    ctx.rect(x0, y + h - 8, x0 + wo, y + h, C["paper_dk"])
    # sol makara
    ctx.rrect(x0 - 14, y - 12, x0 + 14, y + h + 12, 14, hexc("#B9915A"))
    ctx.rrect(x0 - 6, y - 12, x0 + 4, y + h + 12, 5, hexc("#D8B67C"))
    ctx.circ(x0, y - 12, 12, hexc("#8E6A3A"))
    ctx.circ(x0, y + h + 12, 12, hexc("#8E6A3A"))
    # sağ makara
    rx = x0 + wo
    ctx.rrect(rx - 14, y - 12, rx + 14, y + h + 12, 14, hexc("#B9915A"))
    ctx.rrect(rx - 6, y - 12, rx + 4, y + h + 12, 5, hexc("#D8B67C"))
    return wo


def invoice(ctx, cx, top, w, length, t, rows_shown=99, stamp=0.0):
    """Aşağı doğru açılan fatura. top: üst makara merkez y. length: açılan kağıt boyu."""
    x0, x1 = cx - w / 2, cx + w / 2
    # kağıt
    if length > 4:
        ctx.rect(x0 + 8, top + 14, x1 + 8, top + length + 12, (0, 0, 0), 0.18)
        ctx.rect(x0, top, x1, top + length, C["paper"])
        ctx.rect(x0, top, x0 + 14, top + length, C["paper_dk"])
        ctx.rect(x1 - 14, top, x1, top + length, C["paper_dk"])
        # içerik
        y = top + 78
        if length > 130:
            ctx.text(cx, y, "FATURA", 96, C["ink"], path=FONT_LORA)
        y += 70
        if length > 190:
            ctx.line([(x0 + 50, y - 38), (x1 - 50, y - 38)], 4, C["paper_sh"], cap=False)
            ctx.text(cx, y, "Kullanılan top mermileri", 46, hexc("#7A5232"))
        y += 80
        rows = 5
        for i in range(rows):
            ry = y + i * 92
            if ry + 40 > top + length - 18 or i >= rows_shown:
                break
            cannonball(ctx, x0 + 84, ry, 24)
            for k in range(11):
                ctx.circ(x0 + 140 + k * 22, ry + 12, 3.2, hexc("#9B7B4A"))
            ctx.circ(x1 - 84, ry, 28, C["gold"])
            ctx.circ(x1 - 84, ry, 20, C["gold_dk"])
            ctx.text(x1 - 84, ry + 1, "₺" if False else "$", 28, C["gold"], path=FONT_POP) if False else None
            ctx.ring(x1 - 84, ry, 20, 3, hexc("#FFE08A"))
        if stamp > 0 and length > 600:
            sx, sy = cx + 20, top + length - 120
            k = ease_out(stamp, 3)
            Xs = Xf(sx, sy, 1.6 - 0.6 * k, rot=-9)
            if stamp < 1:
                pass
            ctx.poly(Xs.pts([(-190, -52), (190, -52), (190, 52), (-190, 52)]), C["red"], 0.0)
            ctx.line(Xs.pts([(-190, -52), (190, -52), (190, 52), (-190, 52), (-190, -52)]), Xs.len(8), C["red"], 0.9 * k)
            ctx.text(*Xs.p(0, 2), "ÖDENECEK", 64 * Xs.s, C["red"], path=FONT_LORA)
    # alt makara (kıvrım) — açılan ucu
    yb = top + length
    ctx.rrect(x0 - 16, yb - 4, x1 + 16, yb + 38, 20, hexc("#B9915A"))
    ctx.rrect(x0 - 10, yb + 2, x1 + 10, yb + 12, 5, hexc("#D8B67C"))
    ctx.circ(x0 - 16, yb + 17, 20, hexc("#8E6A3A"))
    ctx.circ(x1 + 16, yb + 17, 20, hexc("#8E6A3A"))
    # üst makara
    ctx.rrect(x0 - 16, top - 34, x1 + 16, top + 6, 20, hexc("#B9915A"))
    ctx.rrect(x0 - 10, top - 28, x1 + 10, top - 18, 5, hexc("#D8B67C"))
    ctx.circ(x0 - 16, top - 14, 20, hexc("#8E6A3A"))
    ctx.circ(x1 + 16, top - 14, 20, hexc("#8E6A3A"))


def courier_hand(ox, oy, s, phase, flip=1):
    """Kuryenin zarfı tuttuğu elin dünya konumu (courier() ile aynı formül)."""
    X = Xf(ox, oy, s, flip=flip)
    bob = -9 * abs(math.sin(phase * 0.5 + 0.4)) - 4
    hd = (112, -306 + bob + math.sin(phase + 0.5) * 5)
    return X.p(hd[0] + 20, hd[1] - 30)


def gull(ctx, x, y, s, t, seed=0):
    f = math.sin(t * 9 + seed) * 0.6
    L = 34 * s
    ctx.line([(x - L, y - 6 * s - f * 14 * s), (x - L * 0.5, y - 14 * s * (1 - f) - 6 * s), (x, y)], 5 * s, (255, 255, 255))
    ctx.line([(x, y), (x + L * 0.5, y - 14 * s * (1 - f) - 6 * s), (x + L, y - 6 * s - f * 14 * s)], 5 * s, (255, 255, 255))
