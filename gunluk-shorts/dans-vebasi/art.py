"""Kâğıt-kesme parçalar: dansçılar, müzisyenler, doktor, ev/katedral, sahne, araba, simgeler."""
import math

from cutout import *  # noqa
from engine import *  # noqa

D2R = math.pi / 180
DRESS = [RED, BLUE, GREEN, OCHRE, PURPLE, RED_LT, GREEN_DK, BROWN]


def _dir(theta, side):
    a = theta * D2R
    return side * math.sin(a), math.cos(a)


def _chain(p0, th1, L1, th2, L2, side):
    d1 = _dir(th1, side)
    p1 = (p0[0] + d1[0] * L1, p0[1] + d1[1] * L1)
    d2 = _dir(th2, side)
    p2 = (p1[0] + d2[0] * L2, p1[1] + d2[1] * L2)
    return p1, p2


def dancer(ctx, x, y, s, t, phase, kind=0, flip=1, seed=1, amp=1.0, droop=0.0, gender="w", rot=0.0, face=True, alpha=1.0):
    """Eklemli kâğıt kukla. y: yer çizgisi. phase: dans fazı (rad). droop: yorgunluk 0..1"""
    tqv = tq(t)
    am = amp * (1 - 0.65 * droop)
    sw, sw2, c = math.sin(phase), math.sin(phase + 1.7), math.cos(phase)
    hop = -18 * abs(sw) * am
    lean = 9 * math.sin(phase * 0.5 + 0.6) * am + 20 * droop
    X = Xf(x, y + hop * s, s, flip=flip, rot=rot + lean * 0.6)
    dress = DRESS[kind % len(DRESS)]
    cut = Cut(ctx, t)
    A = lambda pts, col, sd, **k: cut.add(X.pts(pts), col, sd, **k)
    hip = (0, -112)
    sh_l, sh_r = (-27, -188), (27, -188)
    # kollar
    thu_l = (70 + 85 * sw) * am + 18 * droop
    thl_l = thu_l + 45 * math.sin(phase + 0.7) * am
    thu_r = (70 + 85 * sw2) * am + 18 * droop
    thl_r = thu_r + 45 * math.sin(phase + 2.4) * am
    el_l, ha_l = _chain(sh_l, thu_l, 46, thl_l, 44, -1)
    el_r, ha_r = _chain(sh_r, thu_r, 46, thl_r, 44, 1)
    sleeve = dress if gender == "w" else mix(dress, (255, 255, 255), 0.0)
    # arka kol (sağ) + bacaklar
    A(limb(sh_r, el_r, 17), sleeve, seed + 1)
    A(limb(el_r, ha_r, 14), SKIN, seed + 2)
    for side, off in ((-1, 0.0), (1, math.pi)):
        ph = phase + off
        fi = 34 * math.sin(ph) * am * (1 - 0.4 * droop)
        bend = 55 * max(0.0, math.sin(ph + math.pi / 2)) * am
        h0 = (side * 13, -112)
        k, f = _chain(h0, fi * side * -1 if False else fi, 54, fi - bend, 56, 1)
        col = BROWN_DK if gender == "m" else (BROWN if side < 0 else BROWN_DK)
        A(limb(h0, k, 20), mix(dress, (0, 0, 0), 0.25) if gender == "m" else mix(PARCH_DK, BROWN, 0.5), seed + 3 + side)
        A(limb(k, f, 17), mix(dress, (0, 0, 0), 0.25) if gender == "m" else mix(PARCH_DK, BROWN, 0.5), seed + 5 + side)
        foot = [(f[0] - 12, f[1] - 4), (f[0] + 18, f[1] - 4), (f[0] + 22, f[1] + 8), (f[0] - 12, f[1] + 8)]
        A(foot, BROWN_DK, seed + 7 + side)
    # gövde
    if gender == "w":
        hs = 9 * math.sin(phase * 2) * am
        body = [(-28, -194), (28, -194), (22, -142), (56 + hs, -92), (-56 + hs, -92), (-22, -142)]
    else:
        body = [(-28, -194), (28, -194), (30, -112), (-30, -112)]
    A(body, dress, seed + 10)
    A([(-23, -146), (23, -146), (23, -134), (-23, -134)], GOLD, seed + 11, rim=False)
    A([(-14, -196), (14, -196), (0, -178)], PARCH_LT, seed + 12, rim=False)
    # ön kol (sol)
    A(limb(sh_l, el_l, 17), sleeve, seed + 13)
    A(limb(el_l, ha_l, 14), SKIN, seed + 14)
    # baş
    tilt = (9 * math.sin(phase * 2 + 0.4) * am + 24 * droop) * flip
    hc = (0, -226)
    head = circle(hc[0], hc[1], 29, 31, 14)
    head = rot_pts(head, tilt, (0, -196))
    A(head, SKIN, seed + 15)
    if gender == "w":
        wimple = [(-32, -222), (-27, -252), (0, -264), (27, -252), (32, -222), (24, -196), (-24, -196)]
        A(rot_pts(wimple, tilt, (0, -196)), PARCH_LT if kind % 3 else mix(PARCH_LT, ROSE, 0.4), seed + 16)
        A(rot_pts([(-20, -236), (20, -236), (16, -214), (-16, -214)], tilt, (0, -196)), SKIN, seed + 17, rim=False)
    else:
        cap = [(-32, -238), (-26, -262), (0, -274), (26, -262), (32, -238), (0, -244)]
        A(rot_pts(cap, tilt, (0, -196)), dress, seed + 16)
        A(rot_pts([(18, -262), (52, -290), (30, -254)], tilt, (0, -196)), GOLD, seed + 17, rim=False)
    cut.flush()
    # yüz
    if face:
        fp = lambda px, py: X.p(*rot_pts([(px, py)], tilt, (0, -196))[0])
        for ex in (-10, 10):
            a, b = fp(ex, -228)
            ctx.ell(a, b, 3.2 * s, 4.6 * s, INK)
        for cx_ in (-17, 17):
            a, b = fp(cx_, -216)
            ctx.circ(a, b, 5.5 * s, ROSE, 0.85)
        mo = fp(0, -211)
        open_ = 4 + 4 * abs(math.sin(phase * 2))
        ctx.ell(mo[0], mo[1], 6 * s, open_ * s, (120, 30, 34))


# ═══════════════════════════ BAŞKA KUKLALAR ═══════════════════════════
def person(ctx, x, y, s, t, kind="doctor", flip=1, seed=3, sway=0.0, arm=0.0):
    """Doktor / meclis üyesi / marangoz / müzisyen: sakin ayakta duran eklemli kukla"""
    X = Xf(x, y, s, flip=flip)
    cut = Cut(ctx, t)
    b = math.sin(t * 3 + seed) * 2 * sway
    if kind == "doctor":
        robe, hat = BLUE_DK, BLUE_DK
    elif kind == "council":
        robe, hat = RED, RED
    elif kind == "carpenter":
        robe, hat = BROWN, OCHRE
    else:
        robe, hat = GREEN, RED_LT
    cut.add(X.pts([(-26, -196 + b), (26, -196 + b), (46, 0), (-46, 0)]), robe, seed)
    cut.add(X.pts([(-26, -196 + b), (26, -196 + b), (8, -150), (-8, -150)]), PARCH_LT, seed + 1, rim=False)
    cut.add(X.pts([(-30, -150), (30, -150), (30, -138), (-30, -138)]), GOLD, seed + 2, rim=False)
    # kol (öne uzanır)
    shl = (22, -186 + b)
    ang = 120 + 30 * math.sin(t * 2.4 + seed) * sway + arm
    e1 = (shl[0] + math.sin(ang * D2R) * 44, shl[1] + math.cos(ang * D2R) * 44)
    h1 = (e1[0] + 36, e1[1] - 8)
    cut.add(X.pts(limb(shl, e1, 16)), robe, seed + 3)
    cut.add(X.pts(limb(e1, h1, 13)), SKIN, seed + 4)
    cut.add(X.pts(circle(0, -224 + b, 28, 30, 14)), SKIN, seed + 5)
    if kind == "doctor":
        cut.add(X.pts([(-28, -246 + b), (28, -246 + b), (24, -330 + b), (-24, -330 + b)]), hat, seed + 6)
        cut.add(X.pts([(-38, -246 + b), (38, -246 + b), (38, -238 + b), (-38, -238 + b)]), BLUE, seed + 7, rim=False)
        cut.add(X.pts([(-18, -214 + b), (18, -214 + b), (10, -168 + b), (-10, -168 + b)]), PARCH_LT, seed + 8, rim=False)  # sakal
    elif kind == "council":
        cut.add(X.pts([(-52, -246 + b), (52, -246 + b), (30, -306 + b), (-30, -306 + b)]), hat, seed + 6)
        cut.add(X.pts([(-56, -246 + b), (56, -246 + b), (56, -236 + b), (-56, -236 + b)]), PARCH_LT, seed + 7, rim=False)
    elif kind == "carpenter":
        cut.add(X.pts([(-30, -244 + b), (30, -244 + b), (22, -286 + b), (-22, -286 + b)]), hat, seed + 6)
    else:
        cut.add(X.pts([(-30, -244 + b), (30, -244 + b), (0, -292 + b)]), hat, seed + 6)
        cut.add(X.pts([(10, -278 + b), (46, -308 + b), (22, -270 + b)]), GOLD, seed + 7, rim=False)
    cut.flush()
    for ex in (-10, 10):
        px, py = X.p(ex, -228 + b)
        ctx.ell(px, py, 3 * s, 4.2 * s, INK)
    mx, my = X.p(0, -208 + b)
    ctx.ell(mx, my, 6 * s, 3.4 * s, (120, 30, 34))
    return X.p(*h1)


def lute(ctx, x, y, s, t, seed=5, ang=-35, flip=1):
    X = Xf(x, y, s, flip=flip, rot=ang)
    cut = Cut(ctx, t)
    cut.add(X.pts(circle(0, 0, 42, 56, 14)), OCHRE, seed)
    cut.add(X.pts(circle(0, 0, 13, 13, 10)), BROWN_DK, seed + 1, rim=False)
    cut.add(X.pts([(-9, -50), (9, -50), (9, -160), (-9, -160)]), BROWN, seed + 2)
    cut.add(X.pts([(-16, -160), (16, -160), (16, -190), (-16, -190)]), BROWN_DK, seed + 3)
    cut.flush()


def drum(ctx, x, y, s, t, seed=6, hit=0.0):
    X = Xf(x, y, s)
    cut = Cut(ctx, t)
    cut.add(X.pts([(-48, -40), (48, -40), (48, 40), (-48, 40)]), RED, seed)
    cut.add(X.pts(circle(0, -40, 48, 14, 14)), PARCH_LT, seed + 1)
    cut.add(X.pts([(-48, -4), (48, -4), (48, 8), (-48, 8)]), GOLD, seed + 2, rim=False)
    cut.flush()
    if hit > 0:
        ctx.ring(*X.p(0, -40), 60 * s * (1 + hit), 6 * s, GOLD, hit)


def horn(ctx, x, y, s, t, seed=7, flip=1):
    X = Xf(x, y, s, flip=flip, rot=-20)
    cut = Cut(ctx, t)
    cut.add(X.pts([(0, -8), (120, -40), (120, 40), (0, 8)]), GOLD, seed)
    cut.add(X.pts([(-30, -9), (4, -9), (4, 9), (-30, 9)]), BROWN, seed + 1)
    cut.flush()


def notes(ctx, x, y, t, n=5, spread=300, col=INK, scale=1.0, seed=1, speed=1.0, alpha=1.0):
    for i in range(n):
        ph = ((t * 0.55 * speed + i / n) % 1.0)
        nx = x + (rng_hash(seed, i) - 0.5) * spread + 30 * math.sin(ph * 6 + i)
        ny = y - ph * 340
        al = alpha * (1 - ph) ** 0.5 * min(1, ph * 8)
        sc = scale * (0.8 + 0.5 * rng_hash(seed, i, 3))
        ctx.ell(nx, ny, 15 * sc, 11 * sc, col, al)
        ctx.line([(nx + 13 * sc, ny - 2 * sc), (nx + 13 * sc, ny - 52 * sc)], 5 * sc, col, al)
        ctx.poly([(nx + 13 * sc, ny - 52 * sc), (nx + 36 * sc, ny - 38 * sc), (nx + 13 * sc, ny - 38 * sc)], col, al)


# ═══════════════════════════ ARKA PLAN ═══════════════════════════
def sky(ctx, tod=0.0, t=0.0):
    """Gökyüzü: tod 0=gündüz, 1=gece (ekran uzayı)"""
    par = ctx.par
    ctx.parallax(0)
    day_top, day_bot = (236, 214, 160), (248, 232, 190)
    ng_top, ng_bot = (28, 36, 72), (62, 72, 112)
    ctx.vgrad(0, 0, W, H, [(0, mix(day_top, ng_top, tod)), (1, mix(day_bot, ng_bot, tod))])
    if tod > 0.4:
        for i in range(26):
            x = rng_hash(i, 1) * W
            y = rng_hash(i, 2) * 900 + 300
            r = 3 + 4 * rng_hash(i, 3)
            tw = 0.6 + 0.4 * math.sin(t * 3 + i)
            ctx.poly([(x, y - r * 2), (x + r * 0.6, y - r * 0.6), (x + r * 2, y), (x + r * 0.6, y + r * 0.6), (x, y + r * 2), (x - r * 0.6, y + r * 0.6),
                      (x - r * 2, y), (x - r * 0.6, y - r * 0.6)], GOLD, (tod - 0.4) / 0.6 * tw)
    ctx.parallax(par)


def sun_moon(ctx, ang, t=0.0):
    """ang: 0..360 (0=gün doğumu sol, 90=öğle, 180=batım, 270=gece yarısı). Dönen tekerlek"""
    par = ctx.par
    ctx.parallax(0)
    cx, cy, R = 540, 1180, 760
    for k, (col, rr, base) in enumerate(((GOLD, 78, 0), ((236, 236, 222), 64, 180))):
        a = (ang + base) * D2R
        x, y = cx - math.cos(a) * R, cy - math.sin(a) * R * 0.9
        if y < cy + 60:
            cut = Cut(ctx, t, shadow=(6, 8), shadow_a=0.22)
            if k == 0:
                for j in range(12):
                    aa = j * 30 * D2R
                    cut.add([(x + math.cos(aa - 0.13) * rr * 1.1, y + math.sin(aa - 0.13) * rr * 1.1), (x + math.cos(aa) * rr * 1.7, y + math.sin(aa) * rr * 1.7),
                             (x + math.cos(aa + 0.13) * rr * 1.1, y + math.sin(aa + 0.13) * rr * 1.1)], OCHRE, j, rim=False)
            cut.add(circle(x, y, rr, rr, 16), col, k)
            if k == 1:
                cut.add(circle(x + 22, y - 6, rr * 0.82, rr * 0.82, 14), (36, 46, 82), 9, rim=False)
            cut.flush()
    ctx.parallax(par)


def house(ctx, x, y, w, h, body, roof, seed=0, t=0.0, lit=0.0, flip=1):
    """Yarı ahşap ev. (x,y): zemin merkezi"""
    cut = Cut(ctx, t, shadow=(5, 7), shadow_a=0.25)
    cut.add([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y - h), (x - w / 2, y - h)], body, seed)
    cut.add([(x - w / 2 - 14, y - h), (x + w / 2 + 14, y - h), (x + flip * w * 0.12, y - h - w * 0.55)], roof, seed + 1)
    cut.flush()
    cut = Cut(ctx, t, shadow=(0, 0), shadow_a=0.0, rim=0.0)
    tw = 8
    for i in range(0, 4):
        px = x - w / 2 + i * w / 3
        cut.add([(px - tw / 2, y), (px + tw / 2, y), (px + tw / 2, y - h), (px - tw / 2, y - h)], BROWN_DK, seed + 10 + i, rim=False)
    cut.add([(x - w / 2, y - h * 0.5 - tw / 2), (x + w / 2, y - h * 0.5 - tw / 2), (x + w / 2, y - h * 0.5 + tw / 2), (x - w / 2, y - h * 0.5 + tw / 2)], BROWN_DK, seed + 20, rim=False)
    cut.add(limb((x - w / 2, y - h * 0.5), (x - w / 6, y - h), tw), BROWN_DK, seed + 21, rim=False)
    cut.add(limb((x + w / 2, y - h * 0.5), (x + w / 6, y - h), tw), BROWN_DK, seed + 22, rim=False)
    for j, (wx, wy) in enumerate(((-w / 3, -h * 0.28), (w / 3, -h * 0.28), (-w / 3, -h * 0.74), (w / 3, -h * 0.74))):
        col = mix((150, 170, 190), GOLD, lit)
        cut.add([(x + wx - 16, y + wy - 20), (x + wx + 16, y + wy - 20), (x + wx + 16, y + wy + 20), (x + wx - 16, y + wy + 20)], col, seed + 30 + j, rim=False)
    cut.flush()


def cathedral(ctx, x, y, s, t=0.0, seed=2):
    """Strazburg katedrali benzeri: geniş cephe + tek yüksek kule/sivri çatı"""
    X = Xf(x, y, s)
    cut = Cut(ctx, t, shadow=(8, 10), shadow_a=0.28)
    cut.add(X.pts([(-210, 0), (210, 0), (210, -430), (-210, -430)]), STONE, seed)
    cut.add(X.pts([(-210, -430), (210, -430), (130, -520), (-130, -520)]), STONE_DK, seed + 1)
    cut.add(X.pts([(-140, -520), (-60, -520), (-40, -1000), (-100, -1000)]), STONE, seed + 2)   # kule
    cut.add(X.pts([(-110, -1000), (-30, -1000), (-70, -1360)]), STONE_DK, seed + 3)             # sivri çatı
    cut.add(X.pts([(-150, -520), (-50, -520), (-50, -560), (-150, -560)]), STONE_DK, seed + 4, rim=False)
    cut.flush()
    cut = Cut(ctx, t, shadow=(0, 0), shadow_a=0.0, rim=0.0)
    cut.add(X.pts(circle(0, -320, 70, 70, 16)), PARCH_LT, seed + 5, rim=False)
    cut.add(X.pts(circle(0, -320, 52, 52, 16)), RED, seed + 6, rim=False)
    cut.add(X.pts(circle(0, -320, 22, 22, 12)), GOLD, seed + 7, rim=False)
    for k, px in enumerate((-130, 0, 130)):
        cut.add(X.pts([(px - 34, 0), (px + 34, 0), (px + 34, -150), (px, -190), (px - 34, -150)]), BROWN_DK, seed + 8 + k, rim=False)
    for yy in (-700, -820, -920):
        cut.add(X.pts([(-92, yy), (-68, yy), (-68, yy - 60), (-92, yy - 60)]), BROWN_DK, seed + 20, rim=False)
    cut.flush()


def cobbles(ctx, y, t=0.0, x0=-1400, x1=2500, depth=2800):
    ctx.rect(x0, y, x1, y + depth, (178, 138, 88))
    ctx.poly([(x0, y), (x1, y), (x1, y + 26), (x0, y + 26)], (150, 112, 68))
    for r in range(9):
        for i in range(-12, 28):
            cx = x0 + 60 + i * 110 + (r % 2) * 55 + (rng_hash(i, r) - 0.5) * 16
            cy = y + 60 + r * 74 + (rng_hash(r, i, 2) - 0.5) * 8
            ctx.ell(cx, cy, 44 + 6 * rng_hash(i, r, 3), 24 + 3 * rng_hash(i, r, 4), mix((178, 138, 88), (130, 96, 60), 0.25 + 0.3 * rng_hash(i, r, 5)))


def town_backdrop(ctx, t, cx=540, ground=900, night=0.0, with_cathedral=True, zoom_par=True):
    """Paralaks katmanlı kasaba: gökyüzü, katedral, evler, kaldırım"""
    ctx.parallax(0.18)
    for i, (cx_, cy_, sc_) in enumerate(((140, 440, 1.3), (620, 560, 1.0), (980, 380, 1.2), (-260, 520, 1.1), (1300, 520, 1.0))):
        xx = cx_ + 22 * math.sin(t * 0.25 + i)
        cc = Cut(ctx, t, shadow=(6, 8), shadow_a=0.16, rim=2.0)
        cc.add([(xx - 120 * sc_, cy_ + 34 * sc_), (xx - 90 * sc_, cy_ - 10 * sc_), (xx - 40 * sc_, cy_ - 40 * sc_), (xx + 20 * sc_, cy_ - 48 * sc_),
                (xx + 80 * sc_, cy_ - 20 * sc_), (xx + 130 * sc_, cy_ + 6 * sc_), (xx + 120 * sc_, cy_ + 34 * sc_)], (250, 244, 226), 60 + i)
        cc.flush()
    ctx.parallax(0.35)
    if with_cathedral:
        cathedral(ctx, 250, ground - 20, 1.0, t)
    for i, (hx, hw, hh, bc, rc) in enumerate(((640, 190, 190, PARCH_LT, RED), (860, 210, 230, mix(PARCH, STONE, 0.3), BLUE), (1060, 190, 170, PARCH_LT, BROWN))):
        house(ctx, hx, ground - 20, hw, hh, bc, rc, seed=i * 5, t=t, lit=night * 0.9)
    ctx.parallax(0.7)
    for i, (hx, hw, hh, bc, rc) in enumerate(((-30, 230, 270, PARCH, RED), (190, 200, 210, mix(PARCH, OCHRE, 0.25), GREEN_DK), (1010, 220, 300, PARCH_LT, BLUE), (1230, 210, 240, PARCH, RED))):
        house(ctx, hx, ground + 40, hw, hh, bc, rc, seed=40 + i * 5, t=t, lit=night * 0.9, flip=-1 if i % 2 else 1)
    ctx.parallax(1.0)
    cobbles(ctx, ground, t)


# ═══════════════════════════ SAHNE ÖĞELERİ ═══════════════════════════
def banner(ctx, cx, cy, w, h, text, col=RED, tcol=PARCH_LT, px=72, t=0.0, rot=0.0, seed=3):
    X = Xf(cx, cy, 1.0, rot=rot)
    cut = Cut(ctx, t)
    cut.add(X.pts([(-w / 2 - 46, -h / 2 + 18), (-w / 2 + 10, -h / 2 + 18), (-w / 2 + 10, h / 2 + 18), (-w / 2 - 46, h / 2 + 18), (-w / 2 - 20, 18)]), mix(col, (0, 0, 0), 0.25), seed)
    cut.add(X.pts([(w / 2 + 46, -h / 2 + 18), (w / 2 - 10, -h / 2 + 18), (w / 2 - 10, h / 2 + 18), (w / 2 + 46, h / 2 + 18), (w / 2 + 20, 18)]), mix(col, (0, 0, 0), 0.25), seed + 1)
    cut.add(X.pts([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]), col, seed + 2)
    cut.flush()
    ctx.text(*X.p(0, 3), text, px, tcol, path=FONT_LORA)


def stage(ctx, x, y, w, h, build=1.0, t=0.0):
    cut = Cut(ctx, t)
    n = 6
    for i in range(n):
        k = ease_out(clamp(build * (n + 1) - i), 3)
        if k <= 0.01:
            continue
        yy = y - h + i * h / n - (1 - k) * 600
        cut.add([(x - w / 2, yy), (x + w / 2, yy), (x + w / 2, yy + h / n - 4), (x - w / 2, yy + h / n - 4)], mix(BROWN, OCHRE, 0.25 * (i % 2)), 70 + i)
    for px in (-w / 2 + 20, w / 2 - 20):
        k = ease_out(clamp(build * 3 - 1.4), 3)
        cut.add([(x + px - 14, y), (x + px + 14, y), (x + px + 14, y - h * k), (x + px - 14, y - h * k)], BROWN_DK, 80 + int(px))
    cut.flush()


def cart(ctx, x, y, s, t, wheel=0.0, seed=9):
    X = Xf(x, y, s)
    cut = Cut(ctx, t)
    cut.add(X.pts([(-170, -110), (170, -110), (170, -50), (-170, -50)]), BROWN, seed)
    for k in range(7):
        cut.add(X.pts([(-170 + k * 50, -110), (-160 + k * 50, -110), (-160 + k * 50, -190), (-170 + k * 50, -190)]), BROWN_DK, seed + 1 + k, rim=False)
    cut.add(X.pts([(170, -92), (270, -80), (270, -70), (170, -70)]), BROWN_DK, seed + 10)  # oj
    cut.flush()
    for wx in (-110, 110):
        cut = Cut(ctx, t)
        cut.add(X.pts(circle(wx, -38, 44, 44, 14)), BROWN_DK, seed + 20)
        cut.add(X.pts(circle(wx, -38, 30, 30, 12)), OCHRE, seed + 21, rim=False)
        for kk in range(4):
            a = wheel + kk * math.pi / 4
            cut.add(X.pts(limb((wx - math.cos(a) * 40, -38 - math.sin(a) * 40), (wx + math.cos(a) * 40, -38 + math.sin(a) * 40), 7)), BROWN_DK, seed + 30 + kk, rim=False)
        cut.flush()
    return X


def chapel(ctx, x, y, s, t=0.0):
    X = Xf(x, y, s)
    cut = Cut(ctx, t, shadow=(7, 9))
    cut.add(X.pts([(-420, 0), (420, 0), (240, -150), (-240, -150)]), GREEN, 1)
    cut.add(X.pts([(-110, -150), (110, -150), (110, -300), (-110, -300)]), STONE, 2)
    cut.add(X.pts([(-130, -300), (130, -300), (0, -400)]), RED, 3)
    cut.add(X.pts([(-26, -150), (26, -150), (26, -230), (0, -250), (-26, -230)]), BROWN_DK, 4, rim=False)
    cut.add(X.pts([(-5, -400), (5, -400), (5, -470), (-5, -470)]), GOLD, 5, rim=False)
    cut.add(X.pts([(-26, -440), (26, -440), (26, -430), (-26, -430)]), GOLD, 6, rim=False)
    cut.flush()


def bread(ctx, x, y, s, t=0.0):
    cut = Cut(ctx, t)
    cut.add([(x + px * s, y + py * s) for px, py in circle(0, 0, 70, 44, 14)], OCHRE, 3)
    cut.add([(x + px * s, y + py * s) for px, py in circle(0, -8, 56, 30, 12)], mix(OCHRE, (255, 255, 255), 0.25), 4, rim=False)
    cut.flush()
    for k in (-26, 0, 26):
        ctx.line([(x + k * s - 10 * s, y - 20 * s), (x + k * s + 10 * s, y + 6 * s)], 6 * s, BROWN, 0.9)


def bed(ctx, x, y, s, t=0.0):
    cut = Cut(ctx, t)
    cut.add([(x - 110 * s, y - 20 * s), (x + 110 * s, y - 20 * s), (x + 110 * s, y + 30 * s), (x - 110 * s, y + 30 * s)], BLUE, 5)
    cut.add([(x - 110 * s, y - 20 * s), (x + 110 * s, y - 20 * s), (x + 110 * s, y - 2 * s), (x - 110 * s, y - 2 * s)], PARCH_LT, 6, rim=False)
    cut.add([(x - 104 * s, y - 56 * s), (x - 52 * s, y - 56 * s), (x - 52 * s, y - 20 * s), (x - 104 * s, y - 20 * s)], PARCH_LT, 7)
    cut.add([(x - 124 * s, y - 100 * s), (x - 106 * s, y - 100 * s), (x - 106 * s, y + 60 * s), (x - 124 * s, y + 60 * s)], BROWN_DK, 8)
    cut.add([(x + 106 * s, y - 40 * s), (x + 124 * s, y - 40 * s), (x + 124 * s, y + 60 * s), (x + 106 * s, y + 60 * s)], BROWN_DK, 9)
    cut.flush()


def big_x(ctx, x, y, s, t, col=RED, k=1.0):
    for a, b in (((-1, -1), (1, 1)), ((1, -1), (-1, 1))):
        p0 = (x + a[0] * 90 * s, y + a[1] * 90 * s)
        p1 = (x + (a[0] + (b[0] - a[0]) * k) * 90 * s, y + (a[1] + (b[1] - a[1]) * k) * 90 * s)
        c = Cut(ctx, t, shadow=(5, 6))
        c.add(limb(p0, p1, 26 * s), col, 11)
        c.flush()


def flask(ctx, x, y, s, t, boil=1.0):
    X = Xf(x, y, s)
    cut = Cut(ctx, t)
    cut.add(X.pts([(-24, -190), (24, -190), (24, -110), (90, 0), (-90, 0), (-24, -110)]), (190, 220, 230), 21)
    cut.add(X.pts([(-66, -34), (66, -34), (90, 0), (-90, 0)]), RED_LT, 22, rim=False)
    cut.add(X.pts([(-40, -190), (40, -190), (40, -210), (-40, -210)]), BROWN, 23)
    cut.flush()
    for k in range(5):
        ph = (t * 1.6 * boil + k * 0.2) % 1.0
        ctx.circ(*X.p(-40 + k * 20 + 6 * math.sin(ph * 9), -40 - ph * 120), 7 * s * (1 - 0.4 * ph), (255, 255, 255), 0.85 * (1 - ph))
    # kaynama buharı
    for k in range(3):
        ph = (t * 0.9 + k * 0.33) % 1.0
        ctx.circ(*X.p(-10 + 12 * k + 10 * math.sin(ph * 6), -220 - ph * 140), 22 * s * (0.6 + ph), (255, 255, 255), 0.6 * (1 - ph))


def rye(ctx, x, y, s, t):
    cut = Cut(ctx, t)
    cut.add(limb((x, y), (x, y - 260 * s), 10 * s), GREEN, 31)
    for k in range(7):
        yy = y - 280 * s - k * 34 * s
        for sgn in (-1, 1):
            cut.add([(x + sgn * 4 * s, yy + 8 * s), (x + sgn * 28 * s, yy - 14 * s), (x + sgn * 10 * s, yy + 24 * s)], OCHRE if k % 3 else BROWN_DK, 32 + k + (sgn > 0) * 7, rim=False)
    cut.flush()


def head_swirl(ctx, x, y, s, t):
    X = Xf(x, y, s)
    cut = Cut(ctx, t)
    cut.add(X.pts([(-50, 100), (-60, 20), (-40, -60), (10, -90), (60, -60), (70, 0), (50, 40), (80, 60), (40, 70), (30, 100)]), SKIN, 41)
    cut.flush()
    pts = []
    for i in range(60):
        a = i * 0.32 + t * 3
        r = 6 + i * 0.9
        pts.append((x + (0 + math.cos(a) * r) * s * 1.0, y + (-20 + math.sin(a) * r) * s))
    ctx.line(pts, 6 * s, PURPLE)


def balance(ctx, x, y, s, t, tilt):
    X = Xf(x, y, s)
    cut = Cut(ctx, t)
    cut.add(X.pts([(-12, 0), (12, 0), (8, -260), (-8, -260)]), BROWN_DK, 51)
    cut.add(X.pts([(-70, 0), (70, 0), (70, 18), (-70, 18)]), BROWN_DK, 52)
    cut.flush()
    top = X.p(0, -260)
    L = 230 * s
    a = tilt * D2R
    pl, pr = (top[0] - math.cos(a) * L, top[1] - math.sin(a) * L), (top[0] + math.cos(a) * L, top[1] + math.sin(a) * L)
    cut = Cut(ctx, t)
    cut.add(limb(pl, pr, 14 * s), BROWN, 53)
    cut.flush()
    return pl, pr


def stamp_text(ctx, cx, cy, text, px, col=RED, rot=-8.0, t=0.0, pad=26):
    X = Xf(cx, cy, 1.0, rot=rot)
    from PIL import ImageFont
    f = font(FONT_LORA, px)
    wd = f.getlength(text)
    box = [(-wd / 2 - pad, -px * 0.72), (wd / 2 + pad, -px * 0.72), (wd / 2 + pad, px * 0.72), (-wd / 2 - pad, px * 0.72)]
    pts = X.pts(box)
    ctx.poly(pts, PARCH_LT, 0.92)
    c = Cut(ctx, t, shadow=(0, 0), shadow_a=0.0, rim=0.0)
    inner = [(box[0][0] + 8, box[0][1] + 8), (box[1][0] - 8, box[1][1] + 8), (box[2][0] - 8, box[2][1] - 8), (box[3][0] + 8, box[3][1] - 8)]
    ctx.line(X.pts(box + [box[0]]), 8, col)
    ctx.line(X.pts(inner + [inner[0]]), 3, col)
    ctx.text(*X.p(0, 4), text, px, col, path=FONT_LORA)
