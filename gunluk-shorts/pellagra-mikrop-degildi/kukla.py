"""Kâğıt-kukla karakterleri (TESLİMAT #7): büstler (bel üstü), eklemli kollar, ifadeler.
Orijin = boyun tabanı. Birim ≈ ekran pikseli (s=1'de baş ≈ 170 px). Eller dünya koordinatı olarak döner (sahne nesne taşır)."""
import math

from guaj import *  # noqa

# ───────────────────────── görünüşler ─────────────────────────
LOOKS = {
    # Dr. Joseph Goldberger: bıyıklı, yuvarlak gözlüklü, melon şapkalı, koyu yelekli
    "goldberger": dict(skin=SKIN, hair=INK_L, hair_style="side", hat="bowler", hat_col=Hx("#3A2E27"), jacket=Hx("#4A4A58"),
                       shirt=CREAM, tie="bow", tie_col=BRICK, mustache=INK_L, glasses=True, nose=1.0, ears=True),
    "doc_a": dict(skin=SKIN, hair=Hx("#6B5A4A"), hair_style="bald_sides", hat=None, jacket=Hx("#5B4636"), shirt=CREAM, tie="long",
                  tie_col=RUST, mustache=Hx("#6B5A4A"), glasses=False, nose=1.15, ears=True, beard="goatee"),
    "doc_b": dict(skin=Hx("#E5AE82"), hair=Hx("#2E2A28"), hair_style="side", hat="straw", hat_col=Hx("#E3C27E"), jacket=Hx("#6E6A55"),
                  shirt=CREAM, tie="bow", tie_col=OLIVE_D, mustache=Hx("#2E2A28"), glasses=True, nose=0.95, ears=True),
    "doc_c": dict(skin=Hx("#F0C29A"), hair=Hx("#9C9A92"), hair_style="curly", hat=None, jacket=Hx("#3F4B5E"), shirt=CREAM,
                  tie="long", tie_col=OCHRE_D, mustache=Hx("#9C9A92"), glasses=False, nose=1.25, ears=True, beard="full"),
    "doc_d": dict(skin=Hx("#D9A173"), hair=Hx("#3A2A22"), hair_style="side", hat="bowler", hat_col=Hx("#5A4636"), jacket=Hx("#7A5A44"),
                  shirt=CREAM, tie="bow", tie_col=BRICK_D, mustache=Hx("#3A2A22"), glasses=False, nose=1.05, ears=True),
    # çocuklar: büyük kafa, kısa saç
    "kid_a": dict(skin=SKIN, hair=Hx("#5A3A22"), hair_style="kid", hat=None, jacket=Hx("#9C8A5E"), shirt=CREAM, tie=None, nose=0.55,
                  ears=True, kid=True),
    "kid_b": dict(skin=Hx("#E5AE82"), hair=Hx("#2E2A28"), hair_style="kid", hat="cap", hat_col=Hx("#6B7A4A"), jacket=Hx("#8A6A5A"),
                  shirt=CREAM, tie=None, nose=0.5, ears=True, kid=True),
    "kid_c": dict(skin=Hx("#D9A173"), hair=Hx("#3A2A22"), hair_style="kid_long", hat=None, jacket=Hx("#7C6F8A"), shirt=CREAM,
                  tie=None, nose=0.5, ears=True, kid=True),
    # çalışanlar
    "cook": dict(skin=Hx("#EDB98C"), hair=Hx("#8C5A3A"), hair_style="bun", hat="nurse", hat_col=CREAM, jacket=CREAM, shirt=CREAM,
                 tie=None, nose=0.9, ears=True, apron=Hx("#E9DDBE")),
    "nurse": dict(skin=Hx("#F0C29A"), hair=Hx("#4A3A2E"), hair_style="bun", hat="nurse", hat_col=CREAM, jacket=Hx("#7FA0A8"),
                  shirt=CREAM, tie=None, nose=0.8, ears=True, collar=CREAM),
    # mahkûmlar: çizgili üniforma
    "convict_a": dict(skin=Hx("#E5AE82"), hair=Hx("#3A2A22"), hair_style="short", hat=None, jacket=CREAM, stripe=INK, shirt=CREAM,
                      tie=None, nose=1.0, ears=True, stubble=True),
    "convict_b": dict(skin=Hx("#D9A173"), hair=Hx("#2E2A28"), hair_style="bald_sides", hat="cap", hat_col=CREAM, jacket=CREAM, stripe=INK,
                      shirt=CREAM, tie=None, nose=1.15, ears=True, stubble=True),
    "convict_c": dict(skin=Hx("#EDB98C"), hair=Hx("#6B5A4A"), hair_style="short", hat=None, jacket=CREAM, stripe=INK, shirt=CREAM,
                      tie=None, nose=0.9, ears=True, stubble=True),
    # yerli aşçı (Orta Amerika)
    "maya": dict(skin=Hx("#C98F5E"), hair=Hx("#1F1814"), hair_style="braid", hat=None, jacket=Hx("#C9503A"), shirt=CREAM, tie=None,
                 nose=0.9, ears=True, collar=OCHRE_L),
    # Avrupalı tüccar
    "euro": dict(skin=Hx("#F0C29A"), hair=Hx("#7A4A2E"), hair_style="side", hat="cap", hat_col=Hx("#3A4A66"), jacket=Hx("#4A5A78"),
                 shirt=CREAM, tie=None, nose=1.2, ears=True, beard="full"),
}

POSE0 = dict(tilt=0.0, lean=0.0, bob=0.0, arm_l=(8.0, 6.0), arm_r=(8.0, 6.0), mouth="flat", eyes="open", brows=0.0, face=0.0,
             sick=0.0, flip=1, sweat=0.0, jaw=0.0, breathe=0.0, look=(0.0, 0.0), blush=0.0, rash=0.0)


def _rot(pts, ang, pivot):
    c, s = math.cos(ang), math.sin(ang)
    px, py = pivot
    return [(px + (x - px) * c - (y - py) * s, py + (x - px) * s + (y - py) * c) for x, y in pts]


def bust(ctx, x, y, s, look, pose=None, t=0.0, seed=0, ow=8.0):
    """Büst çizer. Dönüş: dict(handL, handR, head) dünya koordinatları (nesne taşımak için)."""
    L = LOOKS[look] if isinstance(look, str) else look
    P = dict(POSE0)
    if pose:
        P.update(pose)
    fl = P["flip"]
    kid = L.get("kid", False)
    tt = tq(t)
    br = 1.0 + 0.012 * math.sin(tt * 2.6 + seed) + P["breathe"]
    bob = P["bob"] + 2.0 * math.sin(tt * 2.2 + seed * 1.7)
    ox, oy = x + P["lean"] * s, y + bob * s

    def W_(px, py):      # yerel → dünya (yatay çevirme + ölçek)
        return (ox + px * s * fl, oy + py * s)

    def WP(pts):
        return [W_(a, b) for a, b in pts]

    sk = L["skin"]
    skd = shade(sk, -0.16)
    sick = clamp(P["sick"])
    if sick > 0:
        sk = mix(sk, SKIN_SICK, 0.75 * sick)
        skd = shade(sk, -0.16)
    sd = seed * 13 + 5
    owx = ow * s * (0.85 if kid else 1.0)
    scale_t = 0.92 if kid else 1.0

    # ── gövde ──
    tw = 118 * scale_t
    tor = [(-26, -10), (26, -10), (tw * 0.86, 2), (tw * 1.16, 34), (tw * 1.14, 110), (tw * 0.98, 250), (-tw * 0.98, 250),
           (-tw * 1.14, 110), (-tw * 1.16, 34), (-tw * 0.86, 2)]
    jac = L["jacket"]
    torP = shape(ctx, WP([(a * 1, b * br if b > 0 else b) for a, b in tor]), jac, ow=owx, seed=sd, t=tt, wob_amp=1.5, smooth=True,
                 shade=(shade(jac, -0.30), 14 * s, 0.55), hatch=(shade(jac, -0.22), 24 * s, 0.35))
    if L.get("stripe"):                     # mahkûm çizgileri
        c = Clip(ctx, torP)
        if c.ok:
            yy = -10.0
            while yy < 260:
                c.poly(WP([(-200, yy), (200, yy), (200, yy + 17), (-200, yy + 17)]), L["stripe"], 0.92)
                yy += 36
            c.done()
    if L.get("apron"):
        ap = WP([(-tw * 0.66, 70), (tw * 0.66, 70), (tw * 0.8, 250), (-tw * 0.8, 250)])
        shape(ctx, ap, L["apron"], ow=owx * 0.7, seed=sd + 1, t=tt, wob_amp=1.2, hatch=(shade(L["apron"], -0.15), 26 * s, 0.30))
    # gömlek V + yaka + kravat
    if L.get("shirt") is not None and not L.get("stripe") and not L.get("apron"):
        v = WP([(-30, -8), (30, -8), (0, 112)])
        shape(ctx, v, L["shirt"], ow=owx * 0.6, seed=sd + 2, t=tt, wob_amp=1.0)
        shape(ctx, WP([(-34, -10), (-6, 8), (-30, 26)]), shade(L["shirt"], -0.05), ow=owx * 0.5, seed=sd + 3, t=tt, wob_amp=0.8)
        shape(ctx, WP([(34, -10), (6, 8), (30, 26)]), shade(L["shirt"], -0.05), ow=owx * 0.5, seed=sd + 4, t=tt, wob_amp=0.8)
        if L.get("tie") == "bow":
            tc = L["tie_col"]
            shape(ctx, WP([(0, 14), (-34, 0), (-34, 30)]), tc, ow=owx * 0.55, seed=sd + 5, t=tt, wob_amp=0.8)
            shape(ctx, WP([(0, 14), (34, 0), (34, 30)]), tc, ow=owx * 0.55, seed=sd + 6, t=tt, wob_amp=0.8)
            shape(ctx, WP(ellipse_pts(0, 15, 9, 11, 12)), shade(tc, -0.2), ow=owx * 0.4, seed=sd + 7, t=tt, wob_amp=0.5)
        elif L.get("tie") == "long":
            tc = L["tie_col"]
            shape(ctx, WP([(-9, 10), (9, 10), (14, 100), (0, 118), (-14, 100)]), tc, ow=owx * 0.55, seed=sd + 5, t=tt, wob_amp=0.8,
                  hatch=(shade(tc, -0.25), 14 * s, 0.4))
    if L.get("collar"):
        shape(ctx, WP([(-36, -10), (0, 36), (-12, -6)]), L["collar"], ow=owx * 0.5, seed=sd + 8, t=tt, wob_amp=0.8)
        shape(ctx, WP([(36, -10), (0, 36), (12, -6)]), L["collar"], ow=owx * 0.5, seed=sd + 9, t=tt, wob_amp=0.8)

    # ── kollar ──
    hands = {}
    for side, key in ((-1, "arm_l"), (1, "arm_r")):
        a1, a2 = P[key]
        sh_x = side * tw * 0.96
        sh_y = 36.0
        upper, fore = 112.0 * scale_t, 104.0 * scale_t
        d1 = (math.sin(math.radians(a1)) * side, math.cos(math.radians(a1)))
        e = (sh_x + d1[0] * upper, sh_y + d1[1] * upper)
        d2 = (math.sin(math.radians(a1 + a2)) * side, math.cos(math.radians(a1 + a2)))
        h = (e[0] + d2[0] * fore, e[1] + d2[1] * fore)
        rU, rF = 27 * scale_t, 22 * scale_t
        shape(ctx, WP(capsule((sh_x, sh_y), e, rU, rF)), jac, ow=owx, seed=sd + 20 + side, t=tt, wob_amp=1.3,
              shade=(shade(jac, -0.30), 8 * s, 0.5))
        shape(ctx, WP(capsule(e, h, rF, rF * 0.92)), shade(jac, -0.06), ow=owx, seed=sd + 24 + side, t=tt, wob_amp=1.3,
              shade=(shade(jac, -0.30), 7 * s, 0.5))
        hp = (h[0] + d2[0] * 14, h[1] + d2[1] * 14)
        hsk = sk
        shape(ctx, WP(ellipse_pts(hp[0], hp[1], 25 * scale_t, 25 * scale_t, 16)), hsk, ow=owx * 0.85, seed=sd + 28 + side, t=tt, wob_amp=1.0,
              shade=(skd, 6 * s, 0.55))
        if P["rash"] > 0 or sick > 0.4:
            rr = max(P["rash"], sick * 0.8)
            for i in range(5):
                rx = hp[0] + (rng_hash(sd, i, side + 3) - 0.5) * 30
                ry = hp[1] + (rng_hash(sd, i, side + 9) - 0.5) * 30
                ctx.poly(blob(*W_(rx, ry), (5 + 3 * rng_hash(sd, i, 4)) * s, (4 + 3 * rng_hash(sd, i, 6)) * s, 8, 0.25, sd + i), BRICK, 0.85 * rr)
        hands[key] = W_(hp[0], hp[1])

    # ── boyun + kafa (kafa boyun tabanı çevresinde eğilir) ──
    shape(ctx, WP([(-20, -46), (20, -46), (24, 4), (-24, 4)]), skd, ow=owx * 0.8, seed=sd + 30, t=tt, wob_amp=1.0)
    hs = 0.86 if kid else 1.0
    hy = -122 * (0.9 if kid else 1.0)
    hr = 82.0                          # ölçekleme H_ içinde yapılır
    piv = (0, -30)
    ang = math.radians(P["tilt"])

    def H_(pts):
        q = [(px * hs, (py - hy) * hs + hy) for px, py in pts]
        return WP(_rot(q, ang, piv))

    fx = P["face"]
    ear_l = ellipse_pts(-hr * 0.98, hy + 6, 14, 22, 12)
    ear_r = ellipse_pts(hr * 0.98, hy + 6, 14, 22, 12)
    if L.get("ears", True):
        shape(ctx, H_(ear_l), sk, ow=owx * 0.7, seed=sd + 31, t=tt, wob_amp=0.8)
        shape(ctx, H_(ear_r), sk, ow=owx * 0.7, seed=sd + 32, t=tt, wob_amp=0.8)
    head = smooth_closed([(0, hy - 94), (62, hy - 74), (80, hy - 8), (62, hy + 56), (0, hy + 84), (-62, hy + 56), (-80, hy - 8), (-62, hy - 74)], 6)
    headP = shape(ctx, H_(head), sk, ow=owx * 1.05, seed=sd + 33, t=tt, wob_amp=1.4,
                  shade=(skd, 12 * s, 0.50), wash=(shade(sk, 0.08), shade(sk, -0.05), 0.40))
    # yanak kızarıklığı / döküntü
    if P["blush"] > 0 or sick > 0:
        bl = P["blush"]
        for sx_ in (-1, 1):
            ctx.poly(wob(H_(ellipse_pts(sx_ * 46 + fx * 8, hy + 34, 17, 12, 12)), 0.6, sd + 40 + sx_, tt), mix(sk, BRICK, 0.55), 0.55 * bl)
    if sick > 0.35 or P["rash"] > 0:
        rr = max(P["rash"], sick * 0.9)
        for i in range(7):
            rx = (rng_hash(sd, i, 21) - 0.5) * 100 + fx * 6
            ry = hy + 6 + rng_hash(sd, i, 22) * 70
            cx_, cy_ = H_([(rx, ry)])[0]
            ctx.poly(blob(cx_, cy_, (6 + 4 * rng_hash(sd, i, 4)) * s, (5 + 3 * rng_hash(sd, i, 6)) * s, 8, 0.25, sd + i), BRICK, 0.85 * rr)

    # ── burun, gözler, kaşlar, ağız ──
    nz = L.get("nose", 1.0)
    nose_c = (fx * 16, hy + 20)
    nP = shape(ctx, H_(ellipse_pts(nose_c[0], nose_c[1], 17 * nz, 22 * nz, 16)), mix(sk, BRICK, 0.10 + 0.25 * P["blush"]), ow=owx * 0.8,
               seed=sd + 50, t=tt, wob_amp=0.8, shade=(skd, 6 * s, 0.5))
    eye_y = hy - 14
    gx, gy = P["look"]
    for sx_ in (-1, 1):
        ex = sx_ * 32 + fx * 10
        e = P["eyes"]
        if e == "blink" or (e == "open" and (rng_hash(seed, int(tt * 3.0), 77) > 0.965)):
            pts = H_([(ex - 15, eye_y), (ex, eye_y + 6), (ex + 15, eye_y)])
            ink_line(ctx, pts, 6.5 * s, INK, sd + 60 + sx_, tt, 0.4, smooth=True)
        elif e == "wide":
            shape(ctx, H_(ellipse_pts(ex, eye_y, 18, 21, 14)), CREAM, ow=owx * 0.5, seed=sd + 61 + sx_, t=tt, wob_amp=0.5)
            ctx.poly(H_(ellipse_pts(ex + gx * 6, eye_y + gy * 6, 7, 7, 10)), INK)
        elif e == "squint":
            ink_line(ctx, H_([(ex - 15, eye_y + 3), (ex + 15, eye_y - 3 * sx_)]), 6.5 * s, INK, sd + 62 + sx_, tt, 0.4)
        elif e == "spiral":
            pts = []
            for k in range(26):
                a = k * 0.55
                r = 2.5 + k * 0.62
                pts.append((ex + r * math.cos(a), eye_y + r * math.sin(a)))
            ink_line(ctx, H_(pts), 4.2 * s, INK, sd + 63 + sx_, tt, 0.2)
        elif e == "sad":
            shape(ctx, H_(ellipse_pts(ex, eye_y + 3, 12, 14, 12)), CREAM, ow=owx * 0.4, seed=sd + 64 + sx_, t=tt, wob_amp=0.4)
            ctx.poly(H_(ellipse_pts(ex + gx * 4, eye_y + 5 + gy * 4, 6.5, 7.5, 10)), INK)
        else:
            ctx.poly(H_(ellipse_pts(ex + gx * 3, eye_y + gy * 3, 8.5, 10.5, 12)), INK)
            ctx.poly(H_(ellipse_pts(ex + gx * 3 - 3, eye_y + gy * 3 - 4, 2.8, 2.8, 8)), CREAM)
        # kaşlar: brows>0 kaldır, <0 çat/üzgün (iç uç yukarı)
        b = P["brows"]                      # >0 yukarı (şaşkın), <0 üzgün/endişeli (iç uçlar yukarı)
        by = eye_y - 30 - 9 * max(0.0, b)
        w_ = 10.0 * max(0.0, -b)
        k_ = 1 if sx_ == -1 else -1         # sol kaş: dış uç aşağı; sağ kaş: dış uç aşağı (iç uçlar yukarı)
        pa = (ex - 19, by + w_ * k_)
        pb = (ex + 19, by - w_ * k_)
        ink_line(ctx, H_([pa, ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2 - 5), pb]), 9 * s * (1.2 if not kid else 1.0), L["hair"] if L.get("hair") else INK,
                 sd + 66 + sx_, tt, 0.4, smooth=True)
    # gözlük
    if L.get("glasses"):
        for sx_ in (-1, 1):
            ex = sx_ * 32 + fx * 10
            ring = ellipse_pts(ex, eye_y, 27, 27, 22)
            ink_line(ctx, H_(ring + [ring[0]]), 6.5 * s, INK, sd + 70 + sx_, tt, 0.4)
        ink_line(ctx, H_([(-6 + fx * 10, eye_y), (6 + fx * 10, eye_y)]), 6 * s, INK, sd + 72, tt, 0.2)
    # ağız
    my = hy + 56
    mo = P["mouth"]
    mx = fx * 10
    jaw = P["jaw"]
    if mo == "open":
        mp = H_(ellipse_pts(mx, my + 4 + jaw * 6, 22, 12 + 16 * jaw, 14))
        shape(ctx, mp, Hx("#4A1F18"), ow=owx * 0.55, seed=sd + 80, t=tt, wob_amp=0.6)
        ctx.poly(H_(ellipse_pts(mx, my + 14 + jaw * 12, 12, 6, 10)), BRICK_D, 0.8)
    elif mo == "oh":
        shape(ctx, H_(ellipse_pts(mx, my + 6, 11, 14, 12)), Hx("#4A1F18"), ow=owx * 0.5, seed=sd + 80, t=tt, wob_amp=0.5)
    elif mo == "smile":
        ink_line(ctx, H_([(mx - 26, my - 2), (mx, my + 14), (mx + 26, my - 2)]), 6.5 * s, INK, sd + 81, tt, 0.4, smooth=True)
    elif mo == "worry":
        ink_line(ctx, H_([(mx - 24, my + 10), (mx, my - 3), (mx + 24, my + 10)]), 6.5 * s, INK, sd + 82, tt, 0.4, smooth=True)
    elif mo == "chew":
        k = math.sin(tt * 14.0)
        shape(ctx, H_(ellipse_pts(mx, my + 5, 20, 5 + 6 * (0.5 + 0.5 * k), 12)), Hx("#4A1F18"), ow=owx * 0.5, seed=sd + 83, t=tt, wob_amp=0.5)
    elif mo == "gulp":
        ink_line(ctx, H_([(mx - 20, my + 4), (mx, my + 8), (mx + 20, my + 4)]), 7 * s, INK, sd + 84, tt, 0.4, smooth=True)
        ctx.poly(H_(ellipse_pts(mx + 22, my - 6, 11, 11, 10)), skd, 0.55)
        ctx.poly(H_(ellipse_pts(mx - 22, my - 6, 11, 11, 10)), skd, 0.55)
    else:
        ink_line(ctx, H_([(mx - 20, my + 4), (mx + 20, my + 4)]), 6.5 * s, INK, sd + 85, tt, 0.4)
    # bıyık / sakal
    L_m = L.get("mustache")
    if L_m is not None and not kid:
        for sx_ in (-1, 1):
            pm = H_([(mx + sx_ * 2, my - 12), (mx + sx_ * 30, my - 18), (mx + sx_ * 52, my - 4), (mx + sx_ * 30, my - 6)])
            shape(ctx, pm, L_m, ow=owx * 0.35, seed=sd + 90 + sx_, t=tt, wob_amp=0.8, smooth=True)
    bd = L.get("beard")
    if bd == "goatee":
        shape(ctx, H_([(-20, my + 12), (20, my + 12), (14, my + 52), (-14, my + 52)]), L["hair"], ow=owx * 0.4, seed=sd + 95, t=tt, wob_amp=0.8, smooth=True)
    elif bd == "full":
        shape(ctx, H_([(-70, hy + 18), (-40, my + 4), (0, my + 22), (40, my + 4), (70, hy + 18), (58, hy + 76), (0, hy + 104), (-58, hy + 76)]),
              L["hair"], ow=owx * 0.5, seed=sd + 96, t=tt, wob_amp=1.0, smooth=True)
        # ağzı sakalın üstüne yeniden çiz
        ink_line(ctx, H_([(mx - 18, my + 8), (mx + 18, my + 8)]), 6 * s, CREAM if mo == "flat" else INK, sd + 97, tt, 0.3)
    if L.get("stubble"):
        for i in range(34):
            sx_ = (rng_hash(sd, i, 31) - 0.5) * 100
            sy_ = hy + 40 + rng_hash(sd, i, 32) * 44
            if abs(sx_) < 54:
                ctx.circ(*H_([(sx_, sy_)])[0], 2.4 * s, INK_L, 0.55)

    # ── saç / şapka ──
    hs_ = L.get("hair_style")
    hc = L["hair"]
    top = hy - 94
    if hs_ in ("side", "short", "kid", "kid_long", "curly", "bald_sides", "bun", "braid"):
        if hs_ == "side":
            hp_ = [(-82, hy - 8), (-70, hy - 70), (-20, top - 6), (50, top - 4), (80, hy - 40), (78, hy - 4), (60, hy - 50), (-4, hy - 56), (-56, hy - 40)]
        elif hs_ == "short":
            hp_ = [(-80, hy - 6), (-70, hy - 72), (-10, top - 4), (60, top + 2), (82, hy - 16), (66, hy - 54), (0, hy - 62), (-60, hy - 52)]
        elif hs_ == "kid":
            hp_ = [(-80, hy - 10), (-68, hy - 74), (-4, top - 8), (64, hy - 72), (82, hy - 10), (60, hy - 46), (4, hy - 58), (-58, hy - 46)]
        elif hs_ == "kid_long":
            hp_ = [(-84, hy + 40), (-80, hy - 40), (-64, hy - 78), (0, top - 10), (66, hy - 78), (82, hy - 40), (86, hy + 40), (66, hy - 34), (4, hy - 58), (-62, hy - 34)]
        elif hs_ == "curly":
            hp_ = [(-84, hy - 6), (-78, hy - 62), (-50, top - 10), (0, top - 22), (52, top - 10), (80, hy - 62), (86, hy - 6), (66, hy - 48), (0, hy - 60), (-66, hy - 48)]
        elif hs_ == "bald_sides":
            hp_ = [(-84, hy - 2), (-76, hy - 36), (-60, hy - 30), (-66, hy + 14), (-80, hy + 14)]
        elif hs_ == "bun":
            hp_ = [(-82, hy - 4), (-70, hy - 74), (-4, top - 8), (66, hy - 74), (82, hy - 4), (62, hy - 48), (0, hy - 60), (-60, hy - 48)]
            shape(ctx, H_(ellipse_pts(0, top - 22, 30, 26, 14)), hc, ow=owx * 0.8, seed=sd + 100, t=tt, wob_amp=0.8)
        else:  # braid
            hp_ = [(-82, hy - 4), (-70, hy - 74), (-4, top - 8), (66, hy - 74), (82, hy - 4), (62, hy - 48), (0, hy - 60), (-60, hy - 48)]
            shape(ctx, H_([(-72, hy + 10), (-92, hy + 70), (-76, hy + 160), (-58, hy + 150), (-66, hy + 70)]), hc, ow=owx * 0.8, seed=sd + 101, t=tt, wob_amp=1.0, smooth=True)
        shape(ctx, H_(hp_), hc, ow=owx * 0.9, seed=sd + 102, t=tt, wob_amp=1.2, smooth=True, shade=(shade(hc, -0.25), 7 * s, 0.4))
        if hs_ == "bald_sides" and L.get("hat") is None:      # tepe kel: ışık yansıması
            ctx.poly(wob(H_(ellipse_pts(-18, top + 12, 18, 9, 10, -0.5)), 0.4, sd, tt), CREAM, 0.30)
    hat = L.get("hat")
    hcol = L.get("hat_col", INK)
    if hat == "bowler":
        shape(ctx, H_(smooth_closed([(-70, hy - 70), (-60, hy - 130), (-26, hy - 158), (30, hy - 158), (62, hy - 130), (72, hy - 70)], 6)), hcol, ow=owx, seed=sd + 110, t=tt,
              wob_amp=1.2, shade=(shade(hcol, -0.3), 10 * s, 0.5), hatch=(shade(hcol, 0.12), 22 * s, 0.25))
        shape(ctx, H_(ellipse_pts(0, hy - 70, 104, 17, 22)), shade(hcol, -0.05), ow=owx, seed=sd + 111, t=tt, wob_amp=1.0, shade=(shade(hcol, -0.3), 6 * s, 0.5))
        shape(ctx, H_([(-68, hy - 82), (68, hy - 82), (66, hy - 96), (-66, hy - 96)]), INK_L, ow=owx * 0.3, seed=sd + 112, t=tt, wob_amp=0.6)
    elif hat == "straw":
        shape(ctx, H_(smooth_closed([(-56, hy - 74), (-48, hy - 128), (0, hy - 138), (48, hy - 128), (56, hy - 74)], 6)), hcol, ow=owx, seed=sd + 113, t=tt, wob_amp=1.2,
              hatch=(shade(hcol, -0.2), 16 * s, 0.35))
        shape(ctx, H_(ellipse_pts(0, hy - 72, 128, 22, 24)), shade(hcol, 0.04), ow=owx, seed=sd + 114, t=tt, wob_amp=1.0, hatch=(shade(hcol, -0.2), 16 * s, 0.30))
        shape(ctx, H_([(-54, hy - 84), (54, hy - 84), (53, hy - 98), (-53, hy - 98)]), BRICK, ow=owx * 0.3, seed=sd + 115, t=tt, wob_amp=0.6)
    elif hat == "cap":
        shape(ctx, H_(smooth_closed([(-74, hy - 62), (-60, hy - 116), (0, hy - 130), (62, hy - 116), (76, hy - 62)], 6)), hcol, ow=owx, seed=sd + 116, t=tt, wob_amp=1.1,
              shade=(shade(hcol, -0.3), 8 * s, 0.5), hatch=(shade(hcol, -0.2), 18 * s, 0.30))
        shape(ctx, H_([(-10, hy - 66), (96, hy - 60), (86, hy - 48), (-10, hy - 54)]), shade(hcol, -0.12), ow=owx * 0.7, seed=sd + 117, t=tt, wob_amp=0.8)
    elif hat == "nurse":
        shape(ctx, H_(smooth_closed([(-62, hy - 70), (-52, hy - 118), (0, hy - 130), (52, hy - 118), (62, hy - 70), (0, hy - 82)], 6)), hcol, ow=owx, seed=sd + 118, t=tt, wob_amp=1.0,
              shade=(shade(hcol, -0.12), 8 * s, 0.5))
        if L.get("collar") or L.get("apron"):
            shape(ctx, H_([(-6, hy - 118), (6, hy - 118), (6, hy - 100), (-6, hy - 100)]), BRICK, ow=owx * 0.2, seed=sd + 119, t=tt, wob_amp=0.3)

    # ter damlaları
    if P["sweat"] > 0:
        for i in range(3):
            u = (tt * 1.8 + i * 0.33) % 1.0
            sx_ = (-1 if i % 2 else 1) * (72 + 6 * i)
            sy_ = hy - 40 + u * 70
            dp = H_([(sx_, sy_ - 14), (sx_ + 8, sy_ + 2), (sx_, sy_ + 10), (sx_ - 8, sy_ + 2)])
            ctx.poly(smooth_closed(dp, 4), (150, 205, 235), 0.9 * P["sweat"] * (1 - u * 0.6))
    hx_, hy_ = W_(0, hy)
    return dict(handL=hands.get("arm_l"), handR=hands.get("arm_r"), head=(hx_, hy_), tor=P)
