"""Sahne grupları. Her fonksiyon t (sn) için 1080x1920 RGB PIL görüntüsü döndürür (sahneye ait 1x katmanlar dahil)."""
import math

import events as E
import ui
from art import *  # noqa
from engine import *  # noqa

D2R = math.pi / 180
NAVY_DK = C["navy_dk"]
WALL_TOP, WALL_BOT = hexc("#FBEBC4"), hexc("#F0CE8A")
CLOCK_C = (540.0, 790.0)
CLOCK_R = 455.0
HUD_PT = (ui.HUD_ICON_X, ui.HUD_Y + 4)


def new_ctx(cam=None, shake=None):
    ctx = Ctx()
    cx, cy, z = cam if cam else (W / 2, H / 2, 1.0)
    ctx.cam(cx, cy, z, shake if shake else (0.0, 0.0))
    return ctx


# ═══════════════════ ortak arka planlar ═══════════════════
def wall_bg(ctx, t, alpha=1.0):
    """Sahne 1 duvarı: krem + dönen ışın + altın tozlar (ekran uzayı)"""
    par = ctx.par
    ctx.parallax(0)
    ctx.vgrad(0, 0, W, H, [(0, WALL_TOP), (1, WALL_BOT)], alpha=alpha)
    base = t * 2.4
    n = 14
    for i in range(n):
        a0 = (i * 360 / n + base) * D2R
        a1 = a0 + (180 / n) * D2R
        L = 2600
        ctx.poly([CLOCK_C, (CLOCK_C[0] + math.cos(a0) * L, CLOCK_C[1] + math.sin(a0) * L),
                  (CLOCK_C[0] + math.cos(a1) * L, CLOCK_C[1] + math.sin(a1) * L)], (255, 246, 214), 0.34 * alpha)
    for k in range(20):
        x = rng_hash(k, 1) * W
        y = (rng_hash(k, 2) * H - t * (18 + 30 * rng_hash(k, 3))) % H
        r = 3 + 6 * rng_hash(k, 4)
        ctx.circ(x, y, r, (255, 214, 120), 0.55 * alpha)
    ctx.parallax(par)


def teal_bg(ctx, t, alpha=1.0, dark=0.0, speed=1.0, red=0.0):
    par = ctx.par
    ctx.parallax(0)
    top = mix(mix(hexc("#118AA3"), NAVY_DK, dark), hexc("#7A1F2E"), red)
    bot = mix(mix(hexc("#094867"), NAVY_DK, dark), hexc("#3A0F1C"), red)
    ctx.vgrad(0, 0, W, H, [(0, top), (1, bot)], alpha=alpha)
    n = 16
    for i in range(n):
        a0 = (i * 360 / n + t * 7 * speed) * D2R
        a1 = a0 + (180 / n) * D2R
        L = 2600
        ctx.poly([(540, 820), (540 + math.cos(a0) * L, 820 + math.sin(a0) * L), (540 + math.cos(a1) * L, 820 + math.sin(a1) * L)],
                 (255, 214, 120), 0.11 * alpha)
    ctx.glow(540, 820, 700, (255, 196, 70), 0.30 * alpha)
    for k in range(16):
        x = rng_hash(k, 11) * W
        y = (rng_hash(k, 12) * H - t * (24 + 40 * rng_hash(k, 13)) * speed) % H
        ctx.circ(x, y, 3 + 5 * rng_hash(k, 14), (255, 230, 150), 0.5 * alpha)
    ctx.parallax(par)


# ═══════════════════ GRUP 1: sahne 1 + 2 (0–6 sn) ═══════════════════
def s1_clock_state(t):
    fr = t % 1.0
    pun = 0.02 * math.sin(math.pi * fr / 0.2) if fr < 0.2 else 0.0
    ma = 600.0 * t + 120.0 * t * t
    ha = ma / 12.0
    sa = 6.0 * math.floor(t) + 6.0 * back_out(prog(fr, 0, 0.12))
    return pun, ha, ma, sa


def scene_intro(t):
    t3 = min(t, 3.0)
    z = 1.0 + 0.012 * t3 + (0.06 * smooth(prog(t, 3.7, 6.2)))
    fr = t % 1.0
    tick_dy = 3.0 * math.sin(math.pi * clamp(fr / 0.12)) if t < 3.0 else 0.0
    sx, sy = E.shake(t)
    ctx = new_ctx((W / 2, H / 2 + (30 if t > 3.7 else 0) * prog(t, 3.7, 4.2), z), (sx, sy + tick_dy))
    wall_bg(ctx, t)
    # S2: teal arka plan'a geçiş
    k_bg = ease_io(prog(t, 3.0, 3.75))
    if k_bg > 0:
        teal_bg(ctx, t, alpha=k_bg)
    # Duvar saati (sahne 1) → küçülüp savaş saatine yerleşir
    pun, ha, ma, sa = s1_clock_state(t)
    p = ease_io(prog(t, 3.0, 3.72))
    if p < 1.0:
        cx = lerp(CLOCK_C[0], HUD_PT[0], p)
        cy = lerp(CLOCK_C[1], HUD_PT[1], p)
        R = lerp(CLOCK_R * (1 + pun), 27.0, p ** 0.85)
        par = ctx.par
        ctx.parallax(0)
        clock(ctx, cx, cy, R, ha, ma, sa, ghost=4 if p < 0.6 else 0, ghost_step=10.0, numerals=R > 160, glow_alpha=0.0)
        ctx.parallax(par)
    # Zarf (sahne 2)
    u = t - 3.70
    if u > 0:
        env_in = back_out(prog(u, 0, 0.42), 2.7)
        s = 0.98 * env_in
        amp = 1.8 + 3.2 * math.exp(-max(0, t - 5.0) / 0.2) * (1 if t >= 5.0 else 0)
        amp += 3.0 * math.exp(-u / 0.25)
        rot = amp * math.sin(u * 61) + 1.2 * math.sin(u * 23)
        jx, jy = 3.0 * math.sin(u * 47), 3.0 * math.cos(u * 53)
        qs = 1.0 + 0.30 * math.exp(-max(0, t - 4.55) / 0.14) * (1 if t >= 4.55 else 0) + 0.04 * math.sin(u * 9)
        glow = 0.35 + 0.15 * math.sin(u * 4)
        envelope(ctx, 540 + jx, 830 + jy + 12 * math.sin(u * 2.0), s, rot=rot, qs=qs, glow=glow)
        if 4.55 <= t < 4.9:  # "?" vurgusu: halka
            k = prog(t, 4.55, 4.9)
            ctx.ring(540, 830, 200 + 320 * k, 8 * (1 - k) + 1, (255, 228, 150), 0.7 * (1 - k))
    return ctx.finish()


# ═══════════════════ GRUP 2: harita (6–11 sn) ═══════════════════
COAST = [(300, -600), (300, 0), (278, 300), (326, 520), (298, 700), (344, 880), (330, 1050), (372, 1250), (346, 1500), (382, 1800),
         (360, 2600)]
ZNZ = [(610, 830), (636, 850), (652, 915), (664, 1005), (658, 1098), (636, 1152), (606, 1132), (590, 1050), (594, 950), (600, 872)]
PEMBA = [(596, 600), (616, 614), (622, 668), (604, 690), (586, 650)]
MAFIA = [(640, 1420), (668, 1432), (672, 1480), (646, 1494), (628, 1460)]
PIN = (628, 862)


def map_cam(t):
    z0, cx0, cy0 = 0.92, 540.0, 960.0
    k = ease_io(prog(t, 6.45, 7.35))
    z = lerp(z0 + 0.02 * (t - 6.0), 3.0, k)
    cx, cy = lerp(cx0, 626.0, k), lerp(cy0, 985.0, k)
    if t > 7.35:
        z += 0.05 * (t - 7.35)
        cx += 4 * (t - 7.35)
    return cx, cy, z


def portrait(ctx, cx, cy, r, kind, grey=0.0, closed=0.0, t=0.0):
    """Yuvarlak kart içinde sade vektör portre (kişi benzerliği iddiası yok)."""
    def g(col):
        gray = int(0.3 * col[0] + 0.59 * col[1] + 0.11 * col[2])
        return mix(col, (gray, gray, gray), grey)
    ctx.circ(cx, cy, r + 14, g(C["gold"]))
    ctx.circ(cx, cy, r, g(hexc("#1E7C8F") if kind == "halid" else hexc("#5C6C7A")))
    # omuz / kaftan
    ctx.ell(cx, cy + r * 0.95, r * 0.78, r * 0.55, g(hexc("#23386B") if kind == "halid" else hexc("#4A4F63")))
    ctx.rect(cx - r * 0.10, cy + r * 0.34, cx + r * 0.10, cy + r * 0.60, g(hexc("#E0B58E")))
    # yüz
    ctx.ell(cx, cy + r * 0.02, r * 0.40, r * 0.46, g(hexc("#E8BE96")))
    # sakal
    beard = hexc("#2D2018") if kind == "halid" else hexc("#CFCFCF")
    ctx.poly([(cx - r * 0.38, cy + r * 0.05), (cx - r * 0.30, cy + r * 0.40), (cx, cy + r * 0.56), (cx + r * 0.30, cy + r * 0.40),
              (cx + r * 0.38, cy + r * 0.05), (cx + r * 0.26, cy + r * 0.22), (cx, cy + r * 0.26), (cx - r * 0.26, cy + r * 0.22)], g(beard))
    ctx.rrect(cx - r * 0.18, cy + r * 0.14, cx + r * 0.18, cy + r * 0.22, r * 0.04, g(beard))
    # gözler
    for sx in (-1, 1):
        ex = cx + sx * r * 0.16
        if closed > 0.5:
            ctx.line([(ex - r * 0.07, cy - r * 0.03), (ex + r * 0.07, cy - r * 0.03)], r * 0.035, (50, 40, 36))
        else:
            ctx.ell(ex, cy - r * 0.04, r * 0.045, r * 0.06, (30, 22, 18))
            ctx.circ(ex + r * 0.012, cy - r * 0.06, r * 0.014, (255, 255, 255))
        ctx.line([(ex - r * 0.09, cy - r * 0.14), (ex + r * 0.08, cy - r * (0.17 if kind == "halid" else 0.12))], r * 0.035, g(beard))
    # sarık
    turban = hexc("#C8283B") if kind == "halid" else hexc("#F2EEE4")
    ctx.ell(cx, cy - r * 0.40, r * 0.50, r * 0.30, g(turban))
    ctx.ell(cx - r * 0.08, cy - r * 0.50, r * 0.30, r * 0.16, g(shade(turban, 0.18)))
    ctx.line([(cx - r * 0.48, cy - r * 0.34), (cx + r * 0.48, cy - r * 0.34)], r * 0.06, g(C["gold"]), cap=False)


def crown(ctx, cx, cy, s, rot=0.0):
    X = Xf(cx, cy, s, rot=rot)
    ctx.poly(X.pts([(-60, 30), (-70, -30), (-34, 0), (0, -52), (34, 0), (70, -30), (60, 30)]), C["gold"])
    ctx.rect(*X.p(-62, 18), *X.p(62, 40), C["gold_dk"])
    for x in (-70, 0, 70):
        ctx.circ(*X.p(x, -34 if x else -56), X.len(9), C["red"])
    ctx.circ(*X.p(0, 28), X.len(8), hexc("#2BB3A8"))


def draw_map_world(ctx, t):
    ctx.vgrad(-4000, -4000, 5000, 6000, [(0, hexc("#2BC9C4")), (1, hexc("#139AB0"))])
    # dalga çizgileri (dünya)
    for i in range(40):
        for j in range(8):
            x = 380 + ((i * 211 + j * 97 + t * 14) % 1100)
            y = -300 + i * 70 + (j % 3) * 9
            ctx.line([(x, y), (x + 36, y)], 4, (230, 255, 250), 0.35, cap=True)
    # sığ su
    ctx.poly([(x + 70, y) for x, y in COAST] + [(-2000, 2600), (-2000, -600)], hexc("#69DDD3"), 0.75)
    ctx.poly([(x + 30, y) for x, y in COAST] + [(-2000, 2600), (-2000, -600)], hexc("#8FEBDD"), 0.65)
    # kara
    ctx.poly(COAST + [(-2000, 2600), (-2000, -600)], C["sand"])
    ctx.poly([(x - 90, y) for x, y in COAST] + [(-2000, 2600), (-2000, -600)], hexc("#A9D27E"))
    ctx.poly([(x - 230, y) for x, y in COAST] + [(-2000, 2600), (-2000, -600)], hexc("#7FBC63"))
    for k in range(10):
        ctx.poly([(60 + k * 31, 300 + k * 160), (130 + k * 31, 250 + k * 160), (200 + k * 31, 300 + k * 160)], hexc("#69A653"))
    ctx.line(COAST[1:-1], 6, (255, 255, 255), 0.7)
    # adalar
    for poly_ in (PEMBA, MAFIA):
        ctx.poly([(x + 22, y) for x, y in poly_], hexc("#69DDD3"), 0.7)
        ctx.poly(poly_, C["sand"])
    ctx.poly([(x + 36, y) for x, y in ZNZ], hexc("#69DDD3"), 0.8)
    ctx.poly([(x + 18, y) for x, y in ZNZ], hexc("#8FEBDD"), 0.7)
    ctx.poly(ZNZ, C["sand"])
    ctx.poly([(x * 0.88 + 628 * 0.12, y * 0.93 + 990 * 0.07) for x, y in ZNZ], hexc("#7FBC63"))
    ctx.line(ZNZ + [ZNZ[0]], 5, (255, 255, 255), 0.75)
    # tek tük palmiye
    for (px, py) in ((620, 960), (640, 1040), (612, 1080)):
        palm(ctx, px, py, 0.16, t, seed=px)
    palace(ctx, 628, 925, 0.16, t=t, flag=1.0)


def scene_map(t):
    cx, cy, z = map_cam(t)
    sx, sy = E.shake(t)
    ctx = new_ctx((cx, cy, z), (sx, sy))
    draw_map_world(ctx, t)
    # iğne
    u = t - 6.95
    if u > 0:
        drop = (1 - ease_out(prog(u, 0, 0.28), 3)) * 160
        pc = (PIN[0], PIN[1] - drop)
        ctx.circ(PIN[0], PIN[1] + 2, 9 * (1 - drop / 160 * 0.5), (0, 0, 0), 0.25)
        ctx.poly([(pc[0] - 11, pc[1] - 26), (pc[0] + 11, pc[1] - 26), (pc[0], pc[1])], C["red_dk"])
        ctx.circ(pc[0], pc[1] - 36, 15, C["red"])
        ctx.circ(pc[0] - 4, pc[1] - 40, 5, (255, 190, 190))
        if u > 0.25:
            k = ((u - 0.25) * 1.2) % 1.0
            ctx.ring(PIN[0], PIN[1], 18 + 56 * k, 3, C["red"], 0.8 * (1 - k))
    # ── ekran uzayı: kartlar (8.0–11.0)
    uc = t - 8.0
    if uc > -0.05:
        ctx.parallax(0)
        dim = 0.62 * ease_out(prog(uc, 0, 0.4))
        ctx.overlay_rgb((8, 40, 60), dim)
        slide = (1 - ease_out(prog(uc, 0, 0.45), 3)) * 700
        grey = smooth(prog(t, 8.7, 9.5))
        closed = 1.0 if t > 8.9 else 0.0
        yy = 760
        pL = 8.0 + 0.0
        portrait(ctx, 300 - slide, yy, 150, "sultan", grey=grey, closed=closed, t=t)
        # yas bandı
        if t > 9.0:
            k = ease_out(prog(t, 9.0, 9.4))
            ctx.poly([(300 + 70 - slide, yy - 150 + 6), (300 + 150 - slide, yy - 150 + 6 + 70 * k), (300 + 120 - slide, yy - 150 + 6 + 100 * k), (300 + 40 - slide, yy - 150 + 6 + 30 * k)],
                     (20, 20, 24))
        ph = back_out(prog(uc, 0.6, 1.1), 2.0)
        portrait(ctx, 780 + (1 - ph) * 700, yy, 150 * max(0.01, 1.0 + 0.08 * math.exp(-max(0, t - 10.0) / 0.2) * (1 if t >= 10.0 else 0)),
                 "halid", t=t)
        # ok
        if t > 9.2:
            k = ease_out(prog(t, 9.2, 9.7))
            for i in range(3):
                ax = 540 - 50 + i * 40
                ctx.poly([(ax - 14, yy - 44), (ax + 14, yy), (ax - 14, yy + 44), (ax - 4, yy)], C["gold"], clamp(k * 3 - i * 0.6))
        # taç uçuşu
        if t > 9.3:
            k = ease_io(prog(t, 9.3, 10.1))
            x = lerp(300, 780, k)
            y = lerp(yy - 190, yy - 180, k) - math.sin(k * math.pi) * 150
            if k < 1.0:
                crown(ctx, x, y, 1.0, rot=lerp(-20, 20, k))
            else:
                crown(ctx, 780, yy - 178 + 4 * math.sin((t - 10.1) * 6), 1.0, rot=0)
        if t > 10.1:  # parıltı
            k = prog(t, 10.1, 10.7)
            for i in range(8):
                a = i * math.pi / 4 + 0.4
                d = 130 * ease_out(k)
                ctx.circ(780 + math.cos(a) * (d + 80), yy - 180 + math.sin(a) * (d + 30), 7 * (1 - k) + 1, C["gold"], 1 - k)
        ctx.parallax(1)
    img = ctx.finish()
    # ── 1x katmanlar
    d = ImageDraw.Draw(img)
    zfade = 1 - prog(z, 1.0, 1.45)
    if zfade > 0.02 and t < 7.0:
        for txt, wx, wy, px, col, sf in (("AFRİKA", 120, 1100, 64, hexc("#5A3A1E"), hexc("#FFF2CF")),
                                         ("HİNT", 830, 700, 46, (255, 255, 255), hexc("#0B6E86")),
                                         ("OKYANUSU", 830, 760, 46, (255, 255, 255), hexc("#0B6E86"))):
            X0, Y0 = ctx.X(wx, wy)
            spr = word_sprite(txt, col, px, stroke=4, stroke_fill=sf, shadow=False)
            blit(img, spr, X0 / SS, Y0 / SS, 1.0, zfade)
    if 7.45 <= t < 8.0 + 0.3:
        X0, Y0 = ctx.X(PIN[0], PIN[1] + 40)
        X0 += 340 * SS
        k = ease_out(prog(t, 7.45, 7.7))
        blit(img, word_sprite("ZANZİBAR", (255, 255, 255), 50, stroke=5, stroke_fill=hexc("#0B6E86")), X0 / SS, Y0 / SS, 1.0,
             k * (1 - prog(t, 8.0, 8.3)))
    if t >= 8.5:
        for txt, cxl, t0l in (("SULTAN", 300, 8.6), ("HALİD", 780, 10.2)):
            if t >= t0l:
                spr = word_sprite(txt, (255, 255, 255) if txt == "HALİD" else (200, 205, 210), 52, stroke=5)
                u_ = (t - t0l) / 0.25
                blit(img, spr, cxl, 985, max(0.02, back_out(u_, 2.5)), clamp(u_ * 4))
    # tarih damgası
    if t >= 7.30:
        fade = 1 - prog(t, 8.1, 8.4)
        if fade > 0:
            ui.draw_stamp_pop(img, ui.date_stamp_sprite(), 540, 470, t - 7.30, -5.0, end_scale=1.0, start_scale=2.4)
            if t - 7.30 < 0.0:
                pass
    return img


# ═══════════════════ GRUP 3: liman — sahne 4-7 (11–32 sn) ═══════════════════
def harbor_cam(t):
    wide = (540.0, 960.0, 1.0)
    if t < 16.0:
        k = prog(t, 11.0, 16.0)
        return lerp(540, 500, k), lerp(960, 930, k), 1.0 + 0.06 * k
    if t < 20.0:
        k = ease_io(prog(t, 16.0, 20.0))
        return lerp(500, 345, k), lerp(930, 700, k), lerp(1.06, 1.32, k)
    if t < 22.3:
        return 540.0, 960.0, 1.0 + 0.05 * prog(t, 20.0, 22.3)
    if t < 23.8:
        k = ease_io(prog(t, 22.3, 23.3))
        return lerp(540, 600, k), lerp(960, 790, k), lerp(1.05, 1.5, k)
    if t < 24.7:
        k = ease_io(prog(t, 23.8, 24.7))
        return lerp(600, 880, k), lerp(790, 1140, k), lerp(1.5, 1.8, k)
    if t < 27.0:
        k = prog(t, 24.7, 27.0)
        return lerp(880, 890, k), lerp(1140, 1175, k), lerp(1.8, 1.7, k)
    if t < 27.8:
        k = ease_io(prog(t, 27.0, 27.8))
        return lerp(890, 540, k), lerp(1175, 900, k), lerp(1.7, 1.05, k)
    if t < 28.4:
        k = ease_io(prog(t, 27.8, 28.35))
        return lerp(540, 509, k), lerp(900, 570, k), lerp(1.05, 2.3, k)
    k = prog(t, 28.4, 32.0)
    return 509 + 14 * k, 570 + 30 * k, 2.3 - 0.4 * k


def draw_ultimatum(ctx, t):
    k = ease_out(prog(t, 12.0, 13.4), 2.5)
    if k <= 0 or t >= 20.0:
        return
    x0, y, w, h = 640.0, 345.0, 400.0, 170.0
    wo = parchment_h(ctx, x0, y, w, h, k)
    if k > 0.97:
        ctx.text(x0 + w / 2 - 14, y + 52, "ÜLTİMATOM", 52, C["ink"], path=FONT_LORA)
        for i, ww in enumerate((300, 240)):
            ctx.rrect(x0 + 34, y + 96 + i * 28, x0 + 34 + ww, y + 106 + i * 28, 5, hexc("#9B7B4A"))
        ctx.circ(x0 + w - 46, y + h - 36, 24, hexc("#C8283B"))
        ctx.ring(x0 + w - 46, y + h - 36, 15, 3, hexc("#E0505F"))


def harbor_clock(ctx, t):
    if t < 11.0 - 0.001 or t >= 20.0:
        return
    tot = E.world_time(t)
    hh = (tot / 3600.0) % 12
    sec_total = tot % 3600
    mi = sec_total / 60.0
    se = tot % 60.0
    if t < 16.0:
        fr = se % 1.0
        sa = 6.0 * math.floor(se) + 6.0 * back_out(prog(fr, 0, 0.12))
    else:
        sa = 6.0 * se
    # dakika ibresi: saniyeler içinde sıçrayarak ilerler
    mi_i = math.floor(mi) + (back_out(prog(se, 0, 0.15)) if t < 16.0 else 0.0) * 0 + (se / 60.0 if t >= 16.0 else 0.0)
    ma = mi_i * 6.0
    ha = (hh + mi_i / 60.0) * 30.0 - 0.0
    ha = ((tot / 3600.0) % 12) * 30.0
    pop = 1.0
    if t >= 16.0:
        pop = 1 + 0.28 * ease_out(prog(t, 16.0, 16.35), 2)
    appear = back_out(prog(t, 11.0, 11.5), 2.2)
    tickp = 1 + 0.035 * math.sin(math.pi * (t % 1.0) / 0.2) if (t % 1.0) < 0.2 and t < 16.0 else 1.0
    R = 135.0 * pop * appear * tickp
    cx, cy = 235.0 + 30 * (pop - 1), 520.0 + 40 * (pop - 1)
    if R > 3:
        wedge = None
        if t < 16.0:
            wedge = (sa % 360 if sa % 360 > 0 else 360, 360.0, 0.45)
        clock(ctx, cx, cy, R, ha, ma, sa, ghost=0, numerals=True, wedge=wedge)
        if t >= 16.0:
            lag = 1 - prog(t, 16.0, 16.5)
            ctx.ring(cx, cy, R * (1.05 + 0.4 * (1 - lag)), 8 * lag + 1, (255, 255, 255), 0.7 * lag)


def draw_harbor(ctx, t):
    dmg = E.palace_dmg(t)
    P = E.PAL
    bomb = prog(t, 20.0, 27.5)
    # gökyüzü
    ctx.rect(-2000, -2000, 3200, 0, C["sky_hi"])
    ctx.vgrad(-2000, 0, 3200, 770, [(0, C["sky_hi"]), (0.75, mix(C["sky_hi"], C["sky_lo"], 0.55)), (1, C["sky_lo"])])
    ctx.glow(150, 380, 420, (255, 244, 190), 0.55)
    ctx.parallax(0.35)
    for i, (cx_, cy_, s_) in enumerate(((880, 470, 1.1), (160, 650, 0.9), (560, 330, 0.8), (1250, 360, 1.0), (-200, 400, 1.0))):
        cloud(ctx, cx_ + 14 * math.sin(t * 0.25 + i), cy_, s_, alpha=0.9)
    ctx.parallax(1.0)
    # uzak tepeler
    ctx.poly([(-300, 770), (-100, 730), (60, 745), (160, 770)], hexc("#8CCFB0"))
    ctx.poly([(620, 770), (760, 722), (880, 740), (1010, 706), (1200, 760), (1300, 770)], hexc("#8CCFB0"))
    waves(ctx, 770, 930, t, C["sea_hi"], C["sea"], rows=4, amp=4, wl=160, x0=-600, x1=W + 600, foam=False)
    # sahil şeridi
    ctx.poly([(-600, 932), (1700, 924), (1700, 996), (-600, 1006)], C["sand"])
    ctx.poly([(-600, 932), (1700, 924), (1700, 942), (-600, 950)], C["sand_hi"])
    ctx.poly([(-600, 996), (1700, 988), (1700, 1000), (-600, 1010)], hexc("#B98B4E"), 0.5)
    palm(ctx, 250, 975, 0.6, t, lean=1, seed=1)
    palm(ctx, 900, 978, 0.55, t, lean=-1, seed=2)
    palace(ctx, P["ox"], P["oy"], P["s"], dmg=dmg, t=t, flag=1.0 - ease_io(prog(t, 28.5, 29.8)), flame_t=t if dmg > 0.2 else None)
    # önde deniz
    waves(ctx, 1010, 1900, t, C["sea"], C["sea_deep"], rows=12, amp=7, wl=170, x0=-700, x1=W + 700)
    # gökteki saat ve parşömen (sahne 4/5)
    ctx.parallax(0.8)
    harbor_clock(ctx, t)
    draw_ultimatum(ctx, t)
    ctx.parallax(0.5)
    if 13.4 <= t < 20.0:
        for j in range(4):
            gx = 1300 - ((t - 13.4) * (150 + 40 * j) + j * 260) % 1700
            gull(ctx, gx, 450 + j * 60 + 14 * math.sin(t * 1.3 + j), 1.9 - 0.15 * j, t, seed=j)
    ctx.parallax(1.0)

    # gemiler (uzaktan yakına)
    recoils = {}
    for s in E.SHOTS:
        age = t - s["t"]
        if 0 <= age < 0.6:
            recoils[(s["ship"], s["gun"])] = max(recoils.get((s["ship"], s["gun"]), 0), math.exp(-age / 0.14))
    draws = [("s", i) for i in range(5)] + [("sultan", 0)]
    draws.sort(key=lambda d: (E.SHIPS[d[1]][1] if d[0] == "s" else E.SULTAN[1]))
    for kind, i in draws:
        if kind == "s":
            x, y, s, rot = E.ship_pose(i, t)
            if x < -600:
                continue
            rc = (recoils.get((i, 0), 0.0), recoils.get((i, 1), 0.0))
            # top namlusu hedefe doğru yükselsin
            ship(ctx, x, y, s, t, rot=rot - 1.5 * max(rc), angs=(-24, -24), recoil=rc, seed=i * 3, smoke=1.0 if x > 0 else 0.2)
            waves(ctx, 1010, 1900, t, C["sea"], C["sea_deep"], rows=12, amp=7, wl=170, x0=x - 270 * s, x1=x + 270 * s, clip_y=y, foam=False)
            # pruva köpüğü
            ctx.line([(x + 250 * s, y + 4), (x + 205 * s, y + 8)], 6 * s, C["foam"], 0.8)
            ctx.line([(x - 240 * s, y + 6), (x - 330 * s, y + 8)], 5 * s, C["foam"], 0.5)
            if E.ship_x_off(i, t) < -20:
                ctx.poly([(x - 240 * s, y + 2), (x - 520 * s, y + 6), (x - 240 * s, y + 14)], C["foam"], 0.5)
        else:
            sx_, sy_, ss_ = E.SULTAN
            sink = E.sultan_sink(t)
            bob = math.sin(t * 1.5) * 4
            ang = 46.0 * sink + (3.0 * math.sin(t * 7) * sink)
            y = sy_ + bob + 150 * ss_ * sink
            ship(ctx, sx_ + 30 * sink, y, ss_, t, rot=ang, sultan=True, smoke=1.0 - sink)
            waves(ctx, 1010, 1900, t, C["sea"], C["sea_deep"], rows=12, amp=7, wl=170, x0=sx_ - 300, x1=sx_ + 340, clip_y=sy_ + bob, foam=False)
            if 0.02 < sink < 0.98:  # köpük + kabarcık
                for j in range(6):
                    a = (t * 0.7 + j / 6) % 1.0
                    ctx.circ(sx_ + (j - 3) * 34 + 20 * sink, sy_ + 12 - a * 70, 6 + 8 * a, C["foam"], 0.7 * (1 - a))
    # namlu ağzı + mermiler
    for s in E.SHOTS:
        age = t - s["t"]
        mx, my = E.muzzle(s["ship"], s["gun"], s["t"], recoil=0.0)
        if 0 <= age < 0.5:
            x, y, sc, rot = E.ship_pose(s["ship"], t)
            tips = ship_gun_tips(x, y, sc, rot=rot, angs=(-24, -24), recoil=(0.8, 0.8))
            muzzle_flash(ctx, tips[s["gun"]][0], tips[s["gun"]][1], age, sc * 1.3, ang=-24)
        u = age / s["flight"]
        if 0 < u < 1:
            tx, ty = s["target"]
            bx, by = lerp(mx, tx, u), lerp(my, ty, u) - 4 * 170 * u * (1 - u)
            for j in range(1, 5):
                uu = max(0.0, u - j * 0.022)
                ctx.circ(lerp(mx, tx, uu), lerp(my, ty, uu) - 4 * 170 * uu * (1 - uu), 9 - j, (235, 230, 225), 0.55 - j * 0.1)
            cannonball(ctx, bx, by, 9)
    # patlamalar
    for i, im in enumerate(E.IMPACTS):
        age = t - im["t"]
        if 0 <= age < 3.8:
            explosion(ctx, im["x"], im["y"], age, size=im["size"], seed=i * 1.7)
    # saray yangın dumanı
    if dmg > 0.3:
        for i, (lx, ly) in enumerate(((-160, -214), (100, -190), (-20, -300), (178, -350))):
            gx, gy = E.palace_pt(lx, ly)
            if dmg * 4.2 > i + 0.5:
                smoke_column(ctx, gx, gy, t, height=250, width=24, n=4, dark=0.75, seed=i, alpha=0.42, speed=0.3)
    # ışık tonu
    if bomb > 0:
        ctx.overlay_rgb((255, 96, 30), 0.20 * ease_out(prog(t, 20.0, 25.0)))
        ctx.overlay_rgb((40, 24, 30), 0.12 * prog(t, 23.0, 28.5))
    if t < 20.0:
        # S5: ekran kararır
        ctx.overlay_rgb((6, 12, 28), 0.34 * ease_out(prog(t, 16.0, 16.5)) + 0.22 * prog(t, 19.0, 19.9))
        # kırmızı vinyet nabzı
        if t > 16.4:
            pulse = 0.5 + 0.5 * math.sin((t - 16.4) * 4.8)
            ctx.overlay_rgb((120, 10, 20), 0.10 * pulse * prog(t, 16.4, 17.5))
    else:
        pass


def scene_harbor(t):
    cx, cy, z = harbor_cam(t)
    sx, sy = E.shake(t)
    ctx = new_ctx((cx, cy, z), (sx, sy))
    draw_harbor(ctx, t)
    if t > 28.0:  # S7: köz parçacıkları
        for k in range(26):
            life = 2.6
            ph = ((t * 0.55 + rng_hash(k, 5)) % 1.0)
            x = 509 + (rng_hash(k, 6) - 0.5) * 520 + math.sin(ph * 6 + k) * 30
            y = 760 - ph * 520
            ctx.circ(x, y, 3 + 3 * rng_hash(k, 7), C["orange"] if k % 3 else C["yellow"], 0.9 * (1 - ph))
    img = ctx.finish()
    # S7 1x katmanlar: mühür + not
    if t >= 30.12:
        ui.draw_stamp_pop(img, ui.seal_sprite(), 540, 790, t - 30.12, -9.0, end_scale=0.80, start_scale=2.4)
    if t >= 30.6:
        k = ease_out(prog(t, 30.6, 30.85))
        blit(img, ui.note_sprite("kaynaklara göre 38-45 dk", 42), 540, 1208, 1.0, k)
    return img


# ═══════════════════ GRUP 4: zarf geri geliyor (32–35 sn) ═══════════════════
def scene_env2(t):
    u = t - 32.0
    z = 1.0 + 0.22 * ease_in(prog(t, 32.0, 35.0), 1.6)
    sx, sy = E.shake(t)
    vio = prog(t, 33.9, 34.9)
    jx = 10 * math.sin(t * 91) * (0.3 + vio)
    jy = 8 * math.cos(t * 87) * (0.3 + vio)
    ctx = new_ctx((540, 830, z), (sx, sy))
    teal_bg(ctx, t, dark=0.55, speed=2.4, red=0.18 + 0.2 * vio)
    s = 1.22 * back_out(prog(u, 0, 0.35), 2.2)
    beats = (32.6, 33.3, 34.0, 34.55)
    qs = 1.0 + 0.04 * math.sin(t * 11)
    for b in beats:
        if t >= b:
            qs += 0.35 * math.exp(-(t - b) / 0.12)
    rot = (3.4 + 5 * vio) * math.sin(t * 85) + 2.0 * math.sin(t * 31)
    envelope(ctx, 540 + jx, 830 + jy + 10 * math.sin(t * 3.2), s, rot=rot, qs=qs, glow=0.55 + 0.25 * math.sin(t * 9))
    for b in beats:  # şok halkaları
        if b <= t < b + 0.4:
            k = (t - b) / 0.4
            ctx.ring(540, 830, 220 + 380 * k, 9 * (1 - k) + 1, (255, 214, 120), 0.8 * (1 - k))
    # kıvılcımlar
    for k in range(16):
        a = rng_hash(k, 21) * 6.283
        ph = (t * (0.9 + 0.5 * vio) + rng_hash(k, 22)) % 1.0
        d = 280 + ph * 340
        ctx.circ(540 + math.cos(a) * d, 830 + math.sin(a) * d * 0.8, 5 * (1 - ph) + 1, C["yellow"], 1 - ph)
    return ctx.finish()


# ═══════════════════ GRUP 5: sahil + final (35–42 sn) ═══════════════════
GROUND_Y = 1205.0
CS = 0.95  # kurye ölçeği
LAND = (800.0, 1185.0)
PAL_B = (690.0, 945.0, 0.8)


def courier_x(t):
    if t < 36.6:
        return lerp(-440.0, 650.0, prog(t, 35.0, 36.6))
    return lerp(650.0, 1600.0, ease_in(prog(t, 36.6, 37.6), 1.3))


def courier_phase(t):
    return t * 2 * math.pi * 2.5


def beach_cam(t):
    if t < 37.4:
        k = ease_out(prog(t, 35.0, 37.4), 2)
        return lerp(430, 540, k), lerp(1000, 960, k), lerp(1.14, 1.0, k)
    if t < 40.0:
        return 540.0, 960.0, 1.0
    k = ease_io(prog(t, 40.0, 40.95))
    return 540.0, lerp(960, 800, k), lerp(1.0, 0.5, k)


def draw_beach(ctx, t):
    ctx.rect(-2000, -2000, 3200, 0, C["sky_hi"])
    ctx.vgrad(-2000, 0, 3200, 790, [(0, C["sky_hi"]), (1, C["sky_lo"])])
    ctx.glow(900, 420, 380, (255, 244, 190), 0.5)
    ctx.parallax(0.4)
    for i, (cx_, cy_, s_) in enumerate(((220, 520, 1.1), (820, 400, 0.9), (560, 640, 0.7))):
        cloud(ctx, cx_ + 20 * math.sin(t * 0.3 + i), cy_, s_)
    ctx.parallax(1.0)
    waves(ctx, 790, 940, t, C["sea_hi"], C["sea"], rows=5, amp=5, wl=170, x0=-2500, x1=W + 2500, foam=True)
    ctx.vgrad(-2500, 925, 3500, 4200, [(0, C["sand_hi"]), (0.08, C["sand"]), (1, C["sand_lo"])])
    ctx.poly([(-900, 925), (2000, 925), (2000, 945), (-900, 950)], hexc("#B9F2E8"), 0.8)
    pal = PAL_B
    palace(ctx, pal[0], pal[1] + 20, pal[2], dmg=0.55, t=t, flag=0.0, flame_t=None)
    for i, (lx, ly) in enumerate(((-160, -214), (100, -190))):
        gx, gy = pal[0] + lx * pal[2], pal[1] + 20 + ly * pal[2]
        smoke_column(ctx, gx, gy, t, height=240, width=30, n=5, dark=0.6, seed=i + 7, alpha=0.5, speed=0.25)
    palm(ctx, 120, 1000, 0.8, t, lean=1, seed=3)
    palm(ctx, 985, 1010, 0.7, t, lean=-1, seed=4)
    # zemin işaretleri
    for k in range(10):
        ctx.ell(60 + k * 118 + rng_hash(k, 3) * 40, 1290 + (k % 3) * 60, 40, 8, hexc("#D9B472"), 0.6)


def draw_courier_part(ctx, t):
    x = courier_x(t)
    ph = courier_phase(t)
    # toz bulutları
    if 35.0 <= t < 38.0:
        for k in range(0, 40):
            tk = 35.0 + k * 0.07
            age = t - tk
            if 0 <= age < 0.8 and tk < 37.6:
                xk = courier_x(tk) - 100
                r = 18 + 40 * ease_out(age / 0.8)
                ctx.circ(xk, GROUND_Y - 8 - 40 * ease_out(age / 0.8), r, C["dust"], 0.7 * (1 - age / 0.8))
    # hız çizgileri
    if t < 37.5:
        for k in range(7):
            ph2 = (t * 5 + k * 0.37) % 1.0
            ly = 1010 + k * 54
            lx = x - 140 - ph2 * 420
            ctx.line([(lx, ly), (lx - 120, ly)], 5, (255, 255, 255), 0.5 * (1 - ph2))
    has_env = t < 36.55
    if x < 1700:
        courier(ctx, x, GROUND_Y, CS, ph, env=has_env)


def draw_envelope_fx(ctx, t):
    if 36.55 <= t < 37.05:
        k = (t - 36.55) / 0.5
        hx, hy = courier_hand(courier_x(36.55), GROUND_Y, CS, courier_phase(36.55))
        x = lerp(hx, LAND[0], ease_out(k, 1.6))
        y = lerp(hy, LAND[1], k) - 4 * 160 * k * (1 - k)
        envelope(ctx, x, y, lerp(0.17, 0.28, k), rot=k * 900 - 14, qmark=False)
    elif t >= 37.05:
        land = prog(t, 37.05, 37.25)
        bounce = 14 * math.exp(-(t - 37.05) / 0.08) * abs(math.sin((t - 37.05) * 30))
        if t < 37.62:
            open_t = prog(t, 37.2, 37.62)
            ctx.glow(LAND[0], LAND[1] - 40, 160 + 220 * open_t, C["gold"], 0.2 + 0.5 * open_t)
            envelope(ctx, LAND[0], LAND[1] - bounce, 0.28, rot=0, open_t=open_t, qmark=False)
            if t < 37.35:  # iniş tozu
                k = (t - 37.05) / 0.3
                for j in range(5):
                    ctx.circ(LAND[0] + (j - 2) * 38 * (0.4 + k), LAND[1] + 22 - 30 * k, 16 + 20 * k, C["dust"], 0.6 * (1 - k))


def draw_invoice_part(ctx, t):
    if t < 37.55:
        return
    rise = ease_out(prog(t, 37.55, 38.25), 2.5)
    top = lerp(1060.0, 440.0, rise)
    w = lerp(80.0, 620.0, ease_out(prog(t, 37.55, 38.2), 2))
    length = 700.0 * ease_out(prog(t, 38.25, 39.3), 2.2)
    stamp = prog(t, 39.32, 39.7)
    cx = lerp(LAND[0], 540.0, rise)
    if w > 100:
        invoice(ctx, cx, top, w, length, t, stamp=stamp)
    else:
        ctx.rrect(cx - w / 2, top - 20, cx + w / 2, top + 30, 20, hexc("#B9915A"))


def scene_beach(t):
    cx, cy, z = beach_cam(t)
    sx, sy = E.shake(t)
    ctx = new_ctx((cx, cy, z), (sx, sy))
    draw_beach(ctx, t)
    if t < 40.5:
        draw_courier_part(ctx, t)
        draw_envelope_fx(ctx, t)
        if t > 37.4:
            ctx.parallax(0)
            ctx.overlay_rgb((8, 20, 40), 0.40 * ease_out(prog(t, 37.4, 38.1)))
            ctx.parallax(1)
        draw_invoice_part(ctx, t)
    else:
        ctx.parallax(0)
        ctx.overlay_rgb((8, 20, 40), 0.40)
        ctx.parallax(1)
        draw_invoice_part(ctx, t)
    # ── final: duvar saatine dönüş (ekran uzayı)
    if t >= 40.45:
        ctx.parallax(0)
        k_bg = ease_io(prog(t, 40.55, 41.15))
        wall_bg(ctx, 0.0, alpha=k_bg)
        p = prog(t, 40.45, 41.35)
        e = ease_io(p)
        R = lerp(27.0, CLOCK_R, back_out(p, 1.1))
        cxx = lerp(HUD_PT[0], CLOCK_C[0], e)
        cyy = lerp(HUD_PT[1], CLOCK_C[1], e)
        ma = 1080.0 * (1 - ease_out(p, 3))
        clock(ctx, cxx, cyy, R, ma / 12.0, ma, ma * 6.0 if p < 1 else 0.0, ghost=4 if (p < 0.7 or p >= 1.0) else 0, ghost_step=14.0 if p < 1.0 else 10.0, numerals=R > 160)
        ctx.parallax(1)
    img = ctx.finish()
    return img


def final_sparkle(img, t):
    """41.4–41.78: saat yerine oturunca parıltı (ding)"""
    if not (41.38 <= t < 41.78):
        return
    k = prog(t, 41.38, 41.78)
    d = ImageDraw.Draw(img)
    cx, cy = CLOCK_C
    for i in range(10):
        a = i * math.pi / 5 + 0.3
        r0 = CLOCK_R * (1.02 + 0.10 * k)
        x, y = cx + math.cos(a) * r0, cy + math.sin(a) * r0
        s = 18 * (1 - k)
        d.polygon([(x, y - s), (x + s * 0.3, y - s * 0.3), (x + s, y), (x + s * 0.3, y + s * 0.3), (x, y + s), (x - s * 0.3, y + s * 0.3),
                   (x - s, y), (x - s * 0.3, y - s * 0.3)], fill=C["gold"])
