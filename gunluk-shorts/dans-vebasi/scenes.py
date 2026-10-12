"""Dans Salgını (1518) — 12 sahne, kâğıt-kesme kolaj. Her fonksiyon t için 1080x1920 RGB döndürür."""
import math

import numpy as np

import cues
from art import *  # noqa
from cues import st, wt, we, en
from cutout import *  # noqa
from engine import *  # noqa

GROUND = 1000
PH0 = 0.9                 # 0. karedeki dansçı pozu
OMEGA = 2 * math.pi * 1.7  # dans hızı (rad/sn)
HERO = (540.0, 1195.0, 1.7)
T_END = cues.FINAL_T


def new_ctx(t, cam=(W / 2, H / 2, 1.0), tod=0.0, ang=70.0, shake=True, backdrop=True, cathedral=True):
    ctx = Ctx()
    sx, sy = cues.shake(t) if shake else (0.0, 0.0)
    ctx.cam(cam[0], cam[1], cam[2], (sx, sy))
    sky(ctx, tod, t)
    sun_moon(ctx, ang, t)
    if backdrop:
        town_backdrop(ctx, t, ground=GROUND, night=tod, with_cathedral=cathedral)
    return ctx


def tod_of(ang):
    s = math.sin(math.radians(ang))
    return clamp((0.25 - s) / 0.8)


def phase_at(t, off=0.0, speed=1.0):
    return PH0 + off + OMEGA * speed * tq(t)


def crowd_specs(n):
    out = []
    for i in range(n):
        d = (i * 0.6180339) % 1.0
        x = 70 + ((i * 0.3819 + 0.13 * (i % 3)) % 1.0) * 940
        y = lerp(1050, 1340, d)
        s = lerp(0.85, 1.55, d)
        out.append((y, x, s, i))
    out.sort()
    return out


def draw_crowd(ctx, t, n_show, droop=0.0, speed=1.0, hero=True, skip_hero_area=False, collapse=0.0, amp=1.0):
    specs = crowd_specs(max(1, n_show))
    for (y, x, s, i) in specs:
        if hero and i == 0:
            continue
        kind = i % 8
        g = "w" if i % 3 else "m"
        fl = 1 if i % 2 else -1
        dr = clamp(droop + 0.2 * rng_hash(i, 4))
        rot = 0.0
        yy = y
        if collapse > 0:
            ci = rng_hash(i, 77)
            kk = clamp((collapse - ci * 0.7) / 0.3)
            rot = 86 * ease_out(kk, 2) * (1 if i % 2 else -1)
            dr = max(dr, kk)
            yy = y + 40 * s * kk
        dancer(ctx, x, yy, s, t, phase_at(t, i * 1.3, speed * (0.9 + 0.2 * rng_hash(i, 5))), kind=kind, flip=fl, seed=100 + i * 7, droop=dr, gender=g,
               rot=rot, amp=amp)
    if hero:
        hx, hy, hs = HERO
        dancer(ctx, hx, hy, hs, t, phase_at(t, 0, speed), kind=0, gender="w", seed=1, droop=droop * 0.6, amp=amp)


def onlookers(ctx, t, k=1.0):
    """Meydan kenarında şaşkın izleyiciler (A ve L sahnesinde aynı)"""
    if k <= 0.02:
        return
    person(ctx, 120, 1330, 1.35 * k, t, "carpenter", seed=21, sway=0.4)
    person(ctx, 960, 1320, 1.3 * k, t, "council", flip=-1, seed=23, sway=0.4)


def spotlight(ctx, x, y, k=1.0):
    par = ctx.par
    ctx.poly([(x - 60, 120), (x + 60, 120), (x + 330, y + 40), (x - 330, y + 40)], (255, 244, 190), 0.16 * k)
    ctx.parallax(par)


def big_label(ctx, cx, cy, text, px, col=RED, t=0.0, rot=-3.0, bg=PARCH_LT, k=1.0):
    from PIL import ImageFont
    f = font(FONT_LORA, px)
    wd = f.getlength(text)
    X = Xf(cx, cy, k, rot=rot)
    box = [(-wd / 2 - 34, -px * 0.74), (wd / 2 + 34, -px * 0.74), (wd / 2 + 34, px * 0.74), (-wd / 2 - 34, px * 0.74)]
    c = Cut(ctx, t)
    c.add(X.pts(box), bg, 5)
    c.flush()
    ctx.text(*X.p(0, 5), text, px * k, col, path=FONT_LORA)


# ═══════════ A: tek kadın dans ediyor ═══════════
def scene_A(t, still=False):
    tt_ = 0.0 if still else t
    a_end = st("B") + 0.1
    ang = 70.0 + 360.0 * ease_io(prog(tt_, wt("A", 6) - 0.15, a_end))
    tod = tod_of(ang)
    ctx = new_ctx(tt_, (W / 2, H / 2, 1.0 + 0.0 * tt_), tod=tod, ang=ang, shake=not still)
    spotlight(ctx, HERO[0], 1100, 1.0 - 0.8 * tod)
    onlookers(ctx, tt_)
    hx, hy, hs = HERO
    ph = PH0 if still else phase_at(tt_)
    dancer(ctx, hx, hy, hs, tt_, ph, kind=0, gender="w", seed=1)
    img = ctx.finish()
    return paper_post(img, 0.0 if still else tt_, still=still)


# ═══════════ B: yetkililer ve çözüm ═══════════
def scene_B(t):
    u = t - st("B")
    ctx = new_ctx(t, (W / 2, H / 2, 1.0 + 0.04 * prog(t, st("B"), en("B"))), tod=0.0, ang=70.0)
    # uzaktaki dansçı
    dancer(ctx, 860, 1060, 0.55, t, phase_at(t), kind=2, seed=5)
    # masa
    c = Cut(ctx, t)
    c.add([(150, 1240), (930, 1240), (930, 1286), (150, 1286)], BROWN)
    c.add([(190, 1286), (232, 1286), (232, 1420), (190, 1420)], BROWN_DK)
    c.add([(848, 1286), (890, 1286), (890, 1420), (848, 1420)], BROWN_DK)
    c.add([(420, 1226), (660, 1226), (660, 1240), (420, 1240)], PARCH_LT)
    c.flush()
    for i, (x, fl) in enumerate(((190, 1), (540, 1), (890, -1))):
        k = back_out(prog(u, 0.05 + 0.1 * i, 0.4 + 0.1 * i), 1.8)
        person(ctx, x, 1240 + (1 - k) * 400, 1.45, t, "council", flip=fl, seed=30 + i, sway=1.0, arm=10 * i)
    # ÇÖZÜM? bayrağı
    tb = wt("B", 3)
    if t >= tb - 0.05:
        k = back_out(prog(t, tb - 0.05, tb + 0.25), 2.0)
        banner(ctx, 540, 560, 560 * k, 120 * k, "ÇÖZÜM?", RED, PARCH_LT, int(80 * max(0.01, k)), t, rot=-2)
        qy = 700 + 14 * math.sin(t * 5)
        ctx.text(540, 760 + qy * 0 + 14 * math.sin(t * 5), "?", 280 * k, GOLD, path=FONT_LORA, stroke=8 * k, stroke_fill=INK)
    return paper_post(ctx.finish(), t)


# ═══════════ C: 1518, Strazburg ═══════════
def scene_C(t):
    u = t - st("C")
    zin = ease_out(prog(t, st("C"), en("C")), 2)
    ctx = new_ctx(t, (W / 2, lerp(1100, 800, zin), lerp(1.0, 1.12, zin)), tod=0.0, ang=70.0)
    # katedral yakın plan
    ctx.parallax(0.6)
    cathedral(ctx, 760, 1180, 1.25, t)
    ctx.parallax(1.0)
    k = back_out(prog(t, wt("C", 1) - 0.05, wt("C", 1) + 0.25), 2.0)
    ctx.parallax(0)
    X = Xf(540, 760, 1.0, rot=-3)
    c = Cut(ctx, t)
    c.add(X.pts([(-420, -230), (420, -240), (440, 230), (-430, 240)]), PARCH_LT, 7)
    c.add(X.pts([(-440, -250), (-380, -250), (-380, 250), (-440, 250)]), PARCH_DK, 8)
    c.add(X.pts([(380, -250), (440, -250), (440, 250), (380, 250)]), PARCH_DK, 9)
    c.flush()
    if k > 0.02:
        ctx.text(540, 700, "1518", 270 * k, RED, path=FONT_LORA, stroke=0)
        ctx.text(540, 880, "STRAZBURG", 96 * k, INK, path=FONT_LORA)
    ctx.parallax(1.0)
    dancer(ctx, 300, 1260, 1.3, t, phase_at(t, 1.0), kind=1, gender="m", seed=44)
    dancer(ctx, 820, 1280, 1.4, t, phase_at(t, 2.2), kind=3, gender="w", seed=45, flip=-1)
    return paper_post(ctx.finish(), t)


# ═══════════ D: kalabalık büyüyor 1 → 34 → 400 ═══════════
def scene_D(t):
    n = cues.dancers(t)
    shown = 1 + int(n / 34.0 * 14) if n <= 34 else 15 + int((n - 34) / 366.0 * 30)
    z = lerp(1.0, 0.8, ease_io(prog(t, st("D"), en("D"))))
    ctx = new_ctx(t, (W / 2, 1010, z), tod=0.0, ang=70.0)
    draw_crowd(ctx, t, shown, speed=1.15)
    ctx.parallax(0)
    for key, label, tq_ in (("34", "34", wt("D", 2)), ("400", "400", wt("D", 7))):
        if t >= tq_ - 0.03 and (key == "400" or t < wt("D", 7)):
            k = back_out(prog(t, tq_ - 0.03, tq_ + 0.25), 2.2)
            big_label(ctx, 540, 520, label, 220, RED, t, rot=-3 if key == "34" else 3, k=max(0.01, k))
    ctx.parallax(1.0)
    return paper_post(ctx.finish(), t)


# ═══════════ E: yemek yok, uyku yok, yığılanlar ═══════════
def scene_E(t):
    u = t - st("E")
    ang = 70 + 360 * prog(t, st("E"), en("E")) * 1.0
    tod = tod_of(ang)
    ctx = new_ctx(t, (W / 2, 1010, 0.92), tod=tod, ang=ang)
    col = clamp((t - wt("E", 5)) / 1.4)
    draw_crowd(ctx, t, 38, droop=clamp(0.3 + 0.7 * prog(t, st("E"), wt("E", 5))), speed=0.85, collapse=col, amp=1.0)
    ctx.parallax(0)
    tb, tbed = wt("E", 1), wt("E", 3)
    kb = back_out(prog(t, st("E") + 0.05, st("E") + 0.4), 2.0)
    if kb > 0.02:
        bread(ctx, 270, 540, 1.7 * kb, t)
        if t >= tb:
            big_x(ctx, 270, 540, 1.0, t, RED, ease_out(prog(t, tb, tb + 0.2)))
    ke = back_out(prog(t, wt("E", 2) - 0.05, wt("E", 2) + 0.3), 2.0)
    if ke > 0.02:
        bed(ctx, 810, 560, 1.5 * ke, t)
        if t >= tbed:
            big_x(ctx, 810, 540, 1.0, t, RED, ease_out(prog(t, tbed, tbed + 0.2)))
    ctx.parallax(1.0)
    # yığılanların etrafında dönen yıldızlar
    if t >= wt("E", 5):
        for i in range(7):
            a = t * 4 + i
            x, y = 200 + (i * 140) % 700, 1090 + 40 * math.sin(a)
            ctx.poly([(x, y - 18), (x + 5, y - 5), (x + 18, y), (x + 5, y + 5), (x, y + 18), (x - 5, y + 5), (x - 18, y), (x - 5, y - 5)], GOLD, clamp((t - wt("E", 5)) * 3))
    return paper_post(ctx.finish(), t)


# ═══════════ F: doktorlar "sıcak kan" — çözüm: daha fazla dans ═══════════
def scene_F(t):
    u = t - st("F")
    ctx = new_ctx(t, (W / 2, 1010, 1.0), tod=0.0, ang=70.0)
    k_dr = back_out(prog(u, 0.0, 0.4), 1.8)
    # doktor + şişe
    dancers_bg = 8 if t >= wt("F", 6) else 3
    draw_crowd(ctx, t, 10 if t >= wt("F", 6) else 4, speed=1.0 if t < wt("F", 6) else 1.5, hero=False, amp=1.0 if t < wt("F", 6) else 1.25)
    person(ctx, 210, 1300 + (1 - k_dr) * 500, 1.7, t, "doctor", seed=61, sway=1.0, arm=-20)
    kf = back_out(prog(t, wt("F", 1) - 0.05, wt("F", 1) + 0.3), 2.0)
    if kf > 0.02:
        flask(ctx, 820, 1050 + (1 - kf) * 200, 1.6 * kf, t)
    if t >= wt("F", 1):
        ctx.parallax(0)
        big_label(ctx, 540, 500, "SICAK KAN", 110, RED, t, rot=-2, k=ease_out(prog(t, wt("F", 1), wt("F", 1) + 0.25), 2))
        ctx.parallax(1.0)
    if t >= wt("F", 4):
        ctx.parallax(0)
        k = back_out(prog(t, wt("F", 4), wt("F", 4) + 0.3), 2.0)
        ctx.overlay_rgb(PARCH, 0.0)
        ctx.parallax(1.0)
    if t >= wt("F", 6) - 0.05:
        ctx.parallax(0)
        k = back_out(prog(t, wt("F", 6) - 0.05, wt("F", 6) + 0.25), 2.2)
        banner(ctx, 540, 700, 720 * k, 130 * k, "DAHA FAZLA DANS!", RED, PARCH_LT, int(70 * max(0.01, k)), t, rot=-3)
        ctx.parallax(1.0)
    return paper_post(ctx.finish(), t)


# ═══════════ G: sahne kuruluyor, müzisyenler ═══════════
def scene_G(t):
    u = t - st("G")
    ctx = new_ctx(t, (W / 2, 1010, 0.95), tod=0.0, ang=70.0)
    draw_crowd(ctx, t, 26, speed=1.35, hero=False, amp=1.2)
    build = ease_out(prog(t, st("G"), wt("G", 2)), 1.5)
    stage(ctx, 540, 1180, 760, 190, build, t)
    # marangozlar
    for i, x in enumerate((130, 950)):
        k = back_out(prog(u, 0.0, 0.35), 1.8)
        person(ctx, x, 1340 + (1 - k) * 400, 1.4, t, "carpenter", flip=1 if i == 0 else -1, seed=71 + i, sway=1.5, arm=40 * math.sin(t * 14 + i))
    tm = wt("G", 2)
    if t >= tm - 0.05:
        k = back_out(prog(t, tm - 0.05, tm + 0.3), 2.0)
        yoff = (1 - k) * -300
        bobv = 6 * math.sin(t * 9)
        lute(ctx, 380, 990 + yoff + bobv, 0.8, t, ang=-25)
        drum(ctx, 560, 1080 + yoff, 0.9, t, hit=0.5 * (0.5 + 0.5 * math.sin(t * 8)))
        horn(ctx, 640, 940 + yoff + bobv, 0.8, t, 6)
        notes(ctx, 540, 900, t, n=8, spread=500, alpha=k, scale=1.3, seed=3)
    return paper_post(ctx.finish(), t)


# ═══════════ H: dans yayılıyor ═══════════
def scene_H(t):
    u = t - st("H")
    z = lerp(1.0, 0.62, ease_io(prog(t, st("H"), en("H"))))
    ctx = new_ctx(t, (W / 2, 1000, z), tod=0.0, ang=70.0)
    stage(ctx, 540, 1180, 760, 190, 1.0, t)
    # sahne etrafında dönen halkalar
    nring = 34
    for r_i, (rx, ry, sc, sp) in enumerate(((560, 150, 1.1, 1.0), (760, 210, 1.3, -0.8))):
        for k in range(nring // 2):
            a = k * 2 * math.pi / (nring // 2) + t * 0.5 * sp
            x = 540 + math.cos(a) * rx
            y = 1180 + math.sin(a) * ry + 120
            if math.sin(a) > 0.0 or r_i == 0:
                dancer(ctx, x, y, sc * (0.8 + 0.4 * math.sin(a) * 0.5 + 0.2), t, phase_at(t, k * 0.9, 1.4), kind=(k + r_i) % 8, seed=200 + k, flip=1 if k % 2 else -1,
                       gender="w" if k % 3 else "m")
    musicians = [(380, 990), (560, 1080), (700, 940)]
    lute(ctx, 380, 990, 0.8, t, ang=-25)
    drum(ctx, 560, 1080, 0.9, t, hit=0.5 * (0.5 + 0.5 * math.sin(t * 8)))
    horn(ctx, 640, 940, 0.8, t, 6)
    notes(ctx, 540, 900, t, n=10, spread=700, scale=1.4, seed=5, speed=1.6)
    return paper_post(ctx.finish(), t)


# ═══════════ I: müzik yasak, dansçılar türbeye ═══════════
def scene_I(t):
    u = t - st("I")
    pan = ease_io(prog(t, wt("I", 3), en("I") + 0.3))
    ctx = new_ctx(t, (lerp(540, 1000, pan), 1000, 1.0), tod=0.0, ang=70.0)
    # sahne (yasak)
    stage(ctx, 540, 1180, 760, 190, 1.0, t)
    tb = wt("I", 2)
    lute(ctx, 380, 990, 0.8, t, ang=-25)
    drum(ctx, 560, 1080, 0.9, t)
    horn(ctx, 640, 940, 0.8, t, 6)
    if t >= wt("I", 1):
        big_x(ctx, 540, 1010, 3.2, t, RED, ease_out(prog(t, wt("I", 1), wt("I", 1) + 0.25)))
    # YASAK damgası
    if t >= tb:
        ctx.parallax(0)
        k = ease_out(prog(t, tb, tb + 0.12), 3)
        if t < wt("I", 3) + 0.3:
            stamp_text(ctx, 540, 560, "YASAK", int(150 * (2.0 - 1.0 * k)), RED, -8.0, t)
        ctx.parallax(1.0)
    # yol + türbe + araba
    tc = wt("I", 4)
    if t >= tc - 0.4:
        ctx.parallax(1.0)
        chapel(ctx, 1380, 1050, 1.15, t)
        cx = lerp(-300, 1150, ease_io(prog(t, tc - 0.1, en("I") + 0.4)))
        X = cart(ctx, cx, 1330, 1.8, t, wheel=t * 6)
        for j in range(4):
            dancer(ctx, cx - 170 + j * 110, 1330 - 100 * 1.8 / 1.8 * 1.25, 0.9, t, phase_at(t, j * 1.4, 0.8), kind=(j * 2) % 8, seed=300 + j, droop=0.5, flip=1)
    return paper_post(ctx.finish(), t)


# ═══════════ J: ergot mu, histeri mi? ═══════════
def scene_J(t):
    u = t - st("J")
    ctx = new_ctx(t, (W / 2, 1010, 1.0), tod=0.0, ang=70.0, backdrop=False)
    ctx.parallax(0)
    ctx.vgrad(0, 0, W, H, [(0, (62, 48, 86)), (1, (36, 28, 60))])
    for i in range(14):
        x = rng_hash(i, 1) * W
        y = (rng_hash(i, 2) * H - t * 30) % H
        ctx.circ(x, y, 4, GOLD, 0.35)
    ctx.parallax(1.0)
    tilt = 12 * math.sin(t * 1.5) if t < wt("J", 10) else 0
    pl, pr = balance(ctx, 540, 1180, 1.5, t, tilt)
    ctx.line([pl, (pl[0], pl[1] + 150)], 6, PARCH_LT)
    ctx.line([pr, (pr[0], pr[1] + 150)], 6, PARCH_LT)
    # kefeler
    for (p, lbl) in ((pl, "L"), (pr, "R")):
        c = Cut(ctx, t)
        c.add([(p[0] - 120, p[1] + 150), (p[0] + 120, p[1] + 150), (p[0] + 80, p[1] + 190), (p[0] - 80, p[1] + 190)], BROWN, 91 + len(lbl))
        c.flush()
    kl = back_out(prog(t, wt("J", 5) - 0.05, wt("J", 5) + 0.3), 2.0)
    if kl > 0.02:
        rye(ctx, pl[0], pl[1] + 150, 0.9 * kl, t)
        big_label(ctx, 270, 560, "ERGOT", 96, RED, t, rot=-4, k=kl)
    kr = back_out(prog(t, wt("J", 8) - 0.05, wt("J", 8) + 0.3), 2.0)
    if kr > 0.02:
        head_swirl(ctx, pr[0], pr[1] + 80, 0.9 * kr, t)
        big_label(ctx, 800, 560, "HİSTERİ", 96, PURPLE, t, rot=4, k=kr)
    # soru işareti
    kq = back_out(prog(t, wt("J", 10), wt("J", 10) + 0.3), 2.0)
    if kq > 0.02:
        ctx.text(540, 760 + 10 * math.sin(t * 6), "?", 380 * kq, GOLD, path=FONT_LORA, stroke=9 * kq, stroke_fill=INK)
    return paper_post(ctx.finish(), t)


# ═══════════ K: müzik susuyor, dans duruyor ═══════════
def scene_K(t):
    u = t - st("K")
    ts = wt("K", 3)
    z = lerp(1.0, 1.1, prog(t, st("K"), en("K") + 0.5))
    ctx = new_ctx(t, (W / 2, 1010, z), tod=0.0, ang=70.0)
    slow = 1.0 - ease_io(prog(t, wt("K", 1), ts + 0.1))
    col = clamp((t - ts) / 1.6)
    draw_crowd(ctx, t, 38, droop=clamp(0.3 + 0.7 * prog(t, wt("K", 1), ts)), speed=max(0.0, slow * 1.2), collapse=col)
    # kaybolan notalar
    notes(ctx, 540, 900, t, n=8, spread=700, alpha=clamp(1 - prog(t, wt("K", 1), ts)), scale=1.3, seed=5)
    desat = 0.85 * prog(t, wt("K", 1), ts + 0.8)
    return paper_post(ctx.finish(), t, desat=desat)


# ═══════════ L: sessizlik… ve dans yeniden başlıyor ═══════════
def scene_L(t):
    u = t - st("L")
    tr = wt("L", 2)   # "sessizliktir" — dansçı geri gelir
    ctx = new_ctx(t, (W / 2, H / 2, 1.0), tod=0.0, ang=70.0)
    desat = 0.85 * (1 - ease_io(prog(t, st("L") + 0.1, tr + 0.05)))
    k = back_out(prog(t, tr, tr + 0.28), 1.8)
    # boş meydan: yerde düşmüş kuklalar (birkaçı)
    if t < tr + 0.4:
        for i, (x, y, s_) in enumerate(((180, 1250, 1.2), (480, 1300, 1.4), (800, 1270, 1.3), (330, 1340, 1.5), (900, 1360, 1.5))):
            dancer(ctx, x, y + 38, s_, t, 0.0, kind=i * 2 % 8, seed=400 + i, droop=1.0, rot=86 * (1 if i % 2 else -1), amp=0.0)
    if k > 0.02:
        spotlight(ctx, HERO[0], 1100, ease_out(prog(t, tr, tr + 0.4)))
        onlookers(ctx, t, k)
        hx, hy, hs = HERO
        tau = tq(t) - T_END
        ph = PH0 + OMEGA * min(0.0, tau)
        dancer(ctx, hx, hy, hs * k, t, ph, kind=0, gender="w", seed=1)
    return paper_post(ctx.finish(), t, desat=desat)


def _scene_funcs():
    return [scene_A, scene_B, scene_C, scene_D, scene_E, scene_F, scene_G, scene_H, scene_I, scene_J, scene_K, scene_L]


def render_group(g, t):
    return _scene_funcs()[g](t)
