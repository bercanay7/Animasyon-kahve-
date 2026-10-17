"""Pellagra: Mikrop Değildi — 14 sahne grubu, guaj kukla stili. Her fonksiyon t için 1080x1920 RGB döndürür.
Statik arka planlar süreç başına bir kez çizilir (önbellek); hareketli her şey (kuklalar, parçacıklar, etiketler) üstüne çizilir."""
import math

import cues
from cues import st, wt, we, en, nw
from props import *  # noqa

LOOKS["farmer"] = dict(skin=Hx("#E0A878"), hair=Hx("#6B5A4A"), hair_style="short", hat="straw", hat_col=Hx("#E3C27E"), jacket=Hx("#5C7088"),
                       shirt=CREAM, tie=None, nose=1.2, ears=True, stubble=True)

_BG = {}


def cached(name, builder):
    if name not in _BG:
        c = Ctx()
        c.cam(W / 2, H / 2, 1.0)
        builder(c)
        _BG[name] = c.im
    return _BG[name]


def new(bgname=None, builder=None):
    ctx = Ctx()
    ctx.cam(W / 2, H / 2, 1.0)
    if bgname:
        ctx.im = cached(bgname, builder).copy()
        ctx.d = ImageDraw.Draw(ctx.im)
    return ctx


def fin(ctx, strength=1.0):
    return paint_post(ctx.finish(), strength)


def pop_k(t, t0, d=0.30, over=2.0):
    u = prog(t, t0, t0 + d)
    return 0.0 if u <= 0 else back_out(u, over)


def ease01(t, t0, d):
    return ease_out(prog(t, t0, t0 + d), 3)


# ═══════════════════════ A: kanca kartı (= kapak = son kare) ═══════════════════════
def _bg_card(c):
    c.vgrad(0, 0, W, H, [(0, Hx("#3E2616")), (0.55, Hx("#2C1A0E")), (1.0, Hx("#1F1209"))])
    c.glow(540, 700, 720, Hx("#8A5A2A"), 0.55)
    for i in range(34):                    # geniş boya darbeleri
        y = rng_hash(5, i, 1) * H
        x = rng_hash(5, i, 2) * W * 1.2 - 160
        c.line([(x, y), (x + 260 + 520 * rng_hash(5, i, 3), y + (rng_hash(5, i, 4) - 0.5) * 60)], 14 + 30 * rng_hash(5, i, 5),
               Hx("#6B4426") if i % 2 else Hx("#1A0E06"), 0.10 + 0.12 * rng_hash(5, i, 6), cap=True)


def scene_card(t, still=False):
    tt = 0.0 if still else t
    ctx = new("card", _bg_card)
    bob = 0.0 if still else 9 * math.sin(tt * 3.1)
    rot = -16 + (0.0 if still else 2.2 * math.sin(tt * 2.3))
    ctx.glow(540, 640 + bob, 460, Hx("#E8A04A"), 0.28)
    capsule_icon(ctx, 540, 640 + bob, 720, 250, rot=rot, c1=CREAM, c2=BRICK, ow=11, seed=3, t=tt)
    # sarkan parıltılar
    for i, (x, y, r) in enumerate(((190, 470, 22), (880, 520, 18), (820, 820, 16), (260, 800, 14))):
        sparkle(ctx, x, y + (0 if still else 6 * math.sin(tt * 2.5 + i)), r, LAMP, 0.9, 0.3 * i)
    k1 = 1.0 if still else 1.0 + 0.07 * math.exp(-max(0.0, tt - wt("A1", 0)) * 7) * (1 if tt >= wt("A1", 0) else 0)
    k2 = 1.0 if still else 1.0 + 0.07 * math.exp(-max(0.0, tt - wt("A2", 0)) * 7) * (1 if tt >= wt("A2", 0) else 0)
    for (y, s_, px, col, k) in ((1010, "DIŞKI YUTTULAR.", 124, CREAM, k1), (1160, "HASTALIK BULAŞMADI.", 100, Hx("#F6B73C"), k2)):
        fpx = fit_font(s_, FONT_SLAB, px, 940)
        ctx.text(540, y, s_, fpx * k, col, path=FONT_SLAB, stroke=9 * k, stroke_fill=Hx("#1A0E06"))
    return fin(ctx)


# ═══════════════════════ B1: güney manzarası ═══════════════════════
def _bg_south(c):
    sky_wash(c, [(0, Hx("#E8B677")), (0.40, Hx("#F3D095")), (0.74, Hx("#F6E0AE")), (1.0, Hx("#EEDB9E"))], seed=3)
    r0 = ridge(1030, 34, 0.0040, 0.6)
    hill(c, r0, Hx("#C79A4C"), light=Hx("#E5BF78"), seed=1, grass=Hx("#8A6A30"), grass_n=24)
    farmhouse(c, 700, 905, 1.02, seed=2)
    r1 = ridge(1250, 44, 0.0034, 2.2)
    hill(c, r1, Hx("#9D8B3F"), light=Hx("#C1B162"), seed=2, grass=Hx("#5C6A2A"), grass_n=40)
    r2 = ridge(1500, 38, 0.0030, 3.9)
    hill(c, r2, Hx("#6E6B2F"), light=Hx("#97915A"), seed=3, grass=Hx("#44521E"), grass_n=50)
    c.rect(0, 1680, W, H + 50, Hx("#5A4A28"))
    for yy, n_, sc_, off in ((1640, 5, 0.78, 20), (1760, 4, 1.0, 120), (1900, 3, 1.28, 40)):     # pamuk sıraları: toprak şeridi + bitkiler
        c.poly(blob(540, yy + 6, 640, 26 * sc_, 18, 0.05, int(yy)), Hx("#473A1E"), 0.8)
        for i in range(n_):
            cotton(c, off + i * (W - 2 * off) / max(1, n_ - 1 if n_ > 1 else 1) + (0 if n_ > 1 else 540), yy, sc_, 0.0, seed=yy + i)


def scene_south(t):
    ctx = new("south", _bg_south)
    sun(ctx, 770, 440, 120, t * 0.6, core=Hx("#F6C95C"), ring=Hx("#FBE6A8"), ray=Hx("#F2B94A"))
    for i, (x0, y, sc) in enumerate(((120, 330, 1.0), (520, 560, 0.7), (980, 250, 0.85))):
        cloud(ctx, ((x0 + t * (8 + 4 * i)) % (W + 500)) - 250, y, sc, CREAM, 3 + i)
    # afiş: ≈ 3 milyon vaka
    kb = pop_k(t, wt("B1", 8) - 0.15, 0.45)
    if kb > 0:
        for px_ in (118, 962):
            ctx.line([(px_, 1040), (px_, 690)], 16, INK, 1.0)
            ctx.line([(px_, 1040), (px_, 690)], 9, Hx("#8A6A44"), 1.0)
        P(ctx, [(118, 700), (962, 700), (962, 880), (118, 880)], CREAM, ow=8, seed=8, wob_amp=1.3, shade=(CREAM_D, 10, 0.5), dry=(CREAM_D, 14, 0.4))
        fpx = fit_font("≈ 3 MİLYON VAKA", FONT_SLAB, 92, 780)
        ctx.text(540, 770, "≈ 3 MİLYON VAKA", fpx * kb, INK, path=FONT_SLAB)
        ctx.text(540, 846, "1906–1940 · yaklaşık, tahmin", 36 * kb, INK_L, path=FONT_SOFT)
    return fin(ctx)


# ═══════════════════════ B2: belirtiler ═══════════════════════
def _bg_porch(c):
    plank_wall(c, 0, H, Hx("#C28A4A"), seed=4, gap=132)
    c.glow(540, 760, 700, Hx("#F2C27A"), 0.42)
    c.rect(0, 1400, W, H + 40, Hx("#7B4E2C"))
    for i in range(14):
        c.line([(0, 1420 + i * 38), (W, 1420 + i * 38 + (rng_hash(3, i, 1) - 0.5) * 8)], 4, Hx("#4E3018"), 0.5, cap=False)


def scene_symptoms(t):
    t0 = cues.gstart(2)
    ctx = new("porch", _bg_porch)
    sick_k = ease01(t, t0, 0.5)
    spiral = t > wt("B2", 3) - 0.1
    b = bust(ctx, 540, 1090, 1.42, "farmer", dict(sick=1.0, mouth="worry", eyes="spiral" if spiral else "sad", brows=-1.0, sweat=1.0, rash=1.0,
                                                   arm_l=(14, 28), arm_r=(14, 28), tilt=4 * math.sin(tq(t) * 1.8) + (6 if spiral else 0), bob=3), t=t, seed=7)
    # etiketler (kelime zamanlarında pop)
    items = [("DÖKÜNTÜ", 0, 250, 560, -5), ("İSHAL", 2, 830, 690, 4), ("BUNAMA", 3, 200, 960, 3), ("ÖLÜM", 4, 860, 1010, -4)]
    for text, wi, x, y, rot in items:
        k = pop_k(t, wt("B2", wi) - 0.05, 0.30)
        if k > 0:
            tag(ctx, x, y, text, 54, k=k, rot=rot, seed=wi * 5 + 3, path=FONT_SLAB, col=CREAM, fill_text=BRICK_D if text == "ÖLÜM" else INK)
            if text == "DÖKÜNTÜ":
                for i in range(5):
                    ctx.poly(blob(x - 80 + i * 40, y + 62 + (i % 2) * 8, 11 * k, 9 * k, 8, 0.2, i), BRICK)
            elif text == "İSHAL":
                for i in range(3):
                    ctx.poly(smooth_closed([(x - 50 + i * 50, y + 52 * k), (x - 40 + i * 50, y + 72 * k), (x - 50 + i * 50, y + 86 * k), (x - 60 + i * 50, y + 72 * k)], 4), Hx("#7DB7DA"))
            elif text == "BUNAMA":
                pts = [(x + (2.5 + j * 0.9) * math.cos(j * 0.55), y + 64 + (2.5 + j * 0.9) * math.sin(j * 0.55)) for j in range(30)]
                ctx.line(pts, 6, INK, 1.0)
            else:
                P(ctx, smooth_closed([(x - 28, y + 100), (x - 28, y + 60), (x, y + 44), (x + 28, y + 60), (x + 28, y + 100)], 5), Hx("#B9B2A4"), ow=5, seed=2, wob_amp=0.8)
                ctx.line([(x, y + 62), (x, y + 90)], 6, INK, 1.0)
                ctx.line([(x - 12, y + 72), (x + 12, y + 72)], 6, INK, 1.0)
    return fin(ctx)


# ═══════════════════════ B3: mikrop arayan doktorlar ═══════════════════════
def _bg_office(c):
    plank_wall(c, 0, 1160, Hx("#6F8A6A"), seed=9, gap=150)
    c.glow(300, 600, 600, Hx("#CFE3C2"), 0.30)
    window(c, 620, 470, 330, 420, sky=Hx("#CFE3E8"), frame=Hx("#4A3A2A"), seed=3)
    # raf + kavanozlar
    P(c, [(60, 470), (560, 470), (560, 500), (60, 500)], Hx("#8A6A3A"), ow=6, seed=4, wob_amp=0.8)
    for i, col in enumerate((OCHRE, BRICK, OLIVE_L, OCHRE_L, Hx("#9CC4D4"))):
        P(c, rrect_pts(80 + i * 96, 390, 150 + i * 96, 470, 12), col, ow=5.5, seed=10 + i, wob_amp=0.8, shade=(shade(col, -0.25), 6, 0.5))


def scene_doctors(t):
    ctx = new("office", _bg_office)
    peer = 12 * math.sin(tq(t) * 2.0)
    bust(ctx, 175, 1060, 0.92, "doc_a", dict(mouth="flat", brows=-0.3, face=0.5, tilt=-4, eyes="open", look=(0.7, 0.2), arm_l=(12, 20), arm_r=(36, 70)), t=t, seed=3)
    bust(ctx, 905, 1060, 0.92, "doc_c", dict(mouth="worry", brows=-0.4, face=-0.5, tilt=4, eyes="open", look=(-0.7, 0.2), arm_l=(36, 70), arm_r=(12, 20)), t=t, seed=5)
    bust(ctx, 520, 1090 + peer, 0.98, "doc_d", dict(mouth="oh", brows=0.8, face=0.4, tilt=-12 + peer * 0.4, eyes="wide", look=(0.5, 0.8), arm_l=(30, 60), arm_r=(30, 60), lean=-8), t=t, seed=7)
    table(ctx, -60, W + 60, 1190, col=Hx("#7A5232"), seed=3)
    microscope(ctx, 560, 1010, 0.62, seed=2)
    k = pop_k(t, wt("B3", 4) - 0.05, 0.40, 2.2)
    if k > 0:
        bubble(ctx, 820, 600, 380, 270, (700, 800), thought=True, seed=4, t=t, k=k)
        germ(ctx, 820, 600, 84 * k, t, seed=4)
    return fin(ctx)


# ═══════════════════════ yardımcı: plan içi mini-whip ═══════════════════════
from fx import whip  # noqa: E402


def sub_whip(t, tb, fa, fb, dur=0.24, axis=0):
    h = dur / 2
    if t < tb - h:
        return fa(t)
    if t > tb + h:
        return fb(t)
    return whip(fa(t), fb(t), (t - (tb - h)) / dur, axis)


# ═══════════════════════ C: yetimhane — gözlem ve çıkarım ═══════════════════════
def _bg_orphan(c):
    plank_wall(c, 0, 1080, Hx("#E3CFA0"), seed=12, gap=170)
    c.rect(0, 770, W, 1090, Hx("#7E8F55"))                      # lambri
    for i in range(0, 9):
        c.line([(i * 140 + 20, 770), (i * 140 + 20, 1090)], 5, Hx("#5C6B3A"), 0.55, cap=False)
    c.line([(-20, 770), (W + 20, 770)], 22, INK, 1.0)
    c.line([(-20, 770), (W + 20, 770)], 14, Hx("#8A6A44"), 1.0)
    c.poly([(0, 1090), (W, 1090), (W, H + 40), (0, H + 40)], Hx("#8E6038"))   # zemin
    for i in range(0, 16):
        y = 1090 + i * 64
        c.line([(0, y), (W, y + (rng_hash(5, i, 1) - 0.5) * 6)], 5, Hx("#5A3A20"), 0.6, cap=False)
    window(c, 90, 250, 300, 420, sky=Hx("#CFE3E8"), frame=Hx("#6B4A2E"), seed=2)
    window(c, 690, 250, 300, 420, sky=Hx("#CFE3E8"), frame=Hx("#6B4A2E"), seed=5)
    light_shaft(c, 90, 250, 300, 420, 140, 1180, a=0.14)
    light_shaft(c, 690, 250, 300, 420, 740, 1180, a=0.14)
    c.line([(540, -20), (540, 120)], 8, INK, 1.0)
    lamp(c, 540, 220, 0.9, 0.0, glow=0.6)


def _kid_looks(sick, t):
    return dict(sick=sick, mouth="worry" if sick > 0.5 else "smile", eyes="sad" if sick > 0.5 else "open", brows=-1.0 * sick,
                sweat=1.0 if sick > 0.6 else 0.0, rash=sick, blush=1.0 - sick, bob=3 * sick)


def _orph_intro(t):
    ctx = new("orphan", _bg_orphan)
    t0 = cues.gstart(4)
    look = math.sin(tq(t) * 1.4)
    b = bust(ctx, 600, 1180, 1.35, "goldberger", dict(mouth="oh" if t < wt("C1", 5) else "flat", brows=0.7, face=0.35 * look, tilt=5 * look, eyes="open", look=(0.8 * look, 0.2),
                                                          arm_l=(30, 60), arm_r=(20, 40), lean=-10 * look), t=t, seed=1)
    if b["handL"]:                                     # defter
        hx, hy = b["handL"]
        P(ctx, [(hx - 50, hy - 40), (hx + 36, hy - 52), (hx + 46, hy + 36), (hx - 40, hy + 48)], CREAM, ow=5, seed=3, wob_amp=0.8, shade=(CREAM_D, 6, 0.5))
        for i in range(4):
            ctx.line([(hx - 32, hy - 20 + i * 16), (hx + 28, hy - 28 + i * 16)], 3, INK_L, 0.7, cap=False)
    k = pop_k(t, wt("C1", 0) - 0.05, 0.35)
    stamp(ctx, 330, 560, "1914", 150, BRICK, -7, k)
    return fin(ctx)


def _orph_kids(t):
    ctx = new("orphan", _bg_orphan)
    t0 = wt("C1", 8) - 0.15
    sk = ease01(t, t0, 0.4)
    for i, (x, look) in enumerate(((190, "kid_a"), (540, "kid_b"), (890, "kid_c"))):
        bust(ctx, x, 1075 + 4 * math.sin(tq(t) * 2 + i), 1.05, look, dict(_kid_looks(sk, t), face=(-0.3, 0.0, 0.3)[i], tilt=3 * math.sin(tq(t) * 1.6 + i), arm_l=(10, 50), arm_r=(10, 50)), t=t, seed=10 + i)
    table(ctx, -60, W + 60, 1190, col=Hx("#7A5232"), seed=6)
    for x in (190, 540, 890):
        plate(ctx, x, 1160, 120, 34, seed=x)
        mush(ctx, x, 1150, 64, 20, seed=x)
    k = pop_k(t, wt("C1", 8) - 0.05, 0.35)
    tag(ctx, 540, 560, "ÇOCUKLAR", 70, k=k, rot=-3, seed=3, path=FONT_SLAB, col=CREAM, fill_text=BRICK_D)
    return fin(ctx)


def _orph_staff(t):
    ctx = new("orphan", _bg_orphan)
    for x, look, fc in ((290, "cook", 0.3), (800, "nurse", -0.3)):
        bust(ctx, x, 1090, 1.28, look, dict(mouth="smile", brows=0.3, blush=1.0, face=fc, tilt=3 * math.sin(tq(t) * 1.3 + x), arm_l=(14, 36), arm_r=(14, 36)), t=t, seed=int(x))
    table(ctx, -60, W + 60, 1200, col=Hx("#8A6038"), seed=7)
    P(ctx, rrect_pts(380, 1090, 700, 1200, 20), Hx("#6A6A60"), ow=7, seed=2, wob_amp=1.0, shade=(Hx("#46463E"), 8, 0.5))     # kazan
    P(ctx, ellipse_pts(540, 1090, 160, 22, 24), Hx("#46463E"), ow=6, seed=3, wob_amp=0.8)
    steam(ctx, 540, 1070, t, n=4, h=220, a=0.45)
    k = pop_k(t, wt("C1", 10) - 0.05, 0.35)
    tag(ctx, 540, 560, "ÇALIŞANLAR", 70, k=k, rot=3, seed=4, path=FONT_SLAB, col=CREAM, fill_text=OLIVE_D)
    return fin(ctx)


def _orph_think(t):
    ctx = new("orphan", _bg_orphan)
    t0 = cues.st("C2")
    up = ease01(t, wt("C2", 2), 0.3)
    bust(ctx, 600, 1130, 1.25, "goldberger", dict(mouth="flat", brows=0.6, face=-0.4, tilt=-5, eyes="open", look=(-0.7, -0.6), arm_l=(10, 30), arm_r=(150 * up + 12 * (1 - up), 10), lean=14), t=t, seed=1)
    k = pop_k(t, t0 + 0.05, 0.4)
    if k > 0:
        bubble(ctx, 330, 600, 560, 520, (480, 860), thought=True, seed=6, t=t, k=k)
        # balonun içi: hemşire + mikrop; mikrop değince hemşire hastalanır
        land = prog(t, wt("C2", 0) + 0.25, wt("C2", 2))
        sick = ease_out(prog(t, wt("C2", 3), wt("C2", 4) + 0.3))
        bust(ctx, 330, 700, 0.5, "nurse", dict(_kid_looks(sick, t), mouth="worry" if sick > 0.5 else "smile"), t=t, seed=4)
        gx = lerp(110, 300, ease_out(land))
        gy = lerp(470, 520, land) + 8 * math.sin(tq(t) * 5)
        if sick < 0.9:
            germ(ctx, gx, gy, 40, t, seed=2, ow=6)
        xk = ease_out(prog(t, wt("C2", 4) + 0.2, wt("C2", 4) + 0.6))
        cross(ctx, 330, 600, 1.7, xk)
    return fin(ctx)


def scene_orphanage(t):
    tA, tB, tC = wt("C1", 8) - 0.12, wt("C1", 10) - 0.12, cues.st("C2") - 0.08
    return sub_whip(t, tA, _orph_intro, lambda tt: sub_whip(tt, tB, _orph_kids, lambda t3: sub_whip(t3, tC, _orph_staff, _orph_think, 0.22, 1), 0.24), 0.24)


# ═══════════════════════ D0: şüpheciler + kararlı Goldberger ═══════════════════════
def _bg_study(c):
    c.vgrad(0, 0, W, H, [(0, Hx("#6A5A7A")), (1.0, Hx("#2A2034"))])
    plank_wall(c, 0, 1260, Hx("#7A6A8A"), seed=14, gap=150)     # akşam mor duvar
    c.glow(540, 700, 700, Hx("#C9A8D8"), 0.28)
    P(c, [(60, 330), (500, 330), (500, 700), (60, 700)], Hx("#5E4A6E"), ow=7, seed=2, wob_amp=1.0)
    for i in range(4):
        for j in range(3):
            P(c, rrect_pts(90 + i * 100, 360 + j * 112, 170 + i * 100, 440 + j * 112, 6), (OCHRE, BRICK, OLIVE, CREAM)[(i + j) % 4], ow=4.5, seed=20 + i * 3 + j, wob_amp=0.6)
    window(c, 640, 330, 300, 380, sky=Hx("#6A5A8A"), frame=Hx("#3A2A4A"), seed=3)


def scene_skeptics(t):
    ctx = new("study", _bg_study)
    t0 = cues.gstart(5)
    xs = (135, 405, 675, 945)
    looks = ("doc_a", "doc_b", "doc_c", "doc_d")
    for i, (x, lk) in enumerate(zip(xs, looks)):
        sh = math.sin(tq(t) * 5.2 + i * 1.7)
        bust(ctx, x, 1070, 0.74, lk, dict(mouth="worry", brows=-0.5, tilt=6 * sh, face=0.5 * sh, eyes="open", arm_l=(10, 240), arm_r=(10, 240), look=(0.5 * sh, 0)), t=t, seed=20 + i)
    kb = pop_k(t, wt("D0", 1) - 0.05, 0.4)
    if kb > 0:
        bubble(ctx, 540, 560, 640, 170, (410, 700), seed=3, t=t, k=kb)
        ctx.text(540, 558, "BULAŞICIDIR!", 78 * kb, BRICK_D, path=FONT_SLAB)
    # Goldberger yan taraftan girer
    e = ease_out(prog(t, wt("D1", 0) - 0.2, wt("D1", 0) + 0.5), 3)
    gx = lerp(1350, 560, e)
    hold = ease01(t, wt("D1", 3), 0.4)
    b = bust(ctx, gx, 1215, 1.05, "goldberger", dict(mouth="flat", brows=0.2, face=-0.3, tilt=-3, eyes="open", arm_l=(10, 30), arm_r=(120 * hold + 8 * (1 - hold), 50 * hold + 10 * (1 - hold)), lean=0), t=t, seed=1)
    if hold > 0.3 and b["handR"]:
        hx, hy = b["handR"]
        pill(ctx, hx, hy - 38, 26 * hold, 0.0, CREAM, seed=3, t=t)
        sparkle(ctx, hx + 36, hy - 70, 16 * hold, LAMP, 0.9, 0.3)
    table(ctx, -60, W + 60, 1400, col=Hx("#5A3A24"), seed=9, depth=70, edge=40)
    return fin(ctx)


# ═══════════════════════ D2: kirli parti ═══════════════════════
def _bg_party(c):
    c.vgrad(0, 0, W, H, [(0, Hx("#241B33")), (0.55, Hx("#33264A")), (1.0, Hx("#1A1224"))])
    plank_wall(c, 0, 1150, Hx("#3A2C4E"), seed=16, gap=160)
    c.glow(540, 760, 800, Hx("#FFC070"), 0.40)
    # buluşma bayrakları (alaycı "parti")
    pts = [(-20, 420), (270, 520), (540, 560), (810, 520), (1100, 420)]
    sm = smooth_open(pts, 12)
    c.line(sm, 7, INK, 1.0)
    cols = (BRICK, OCHRE, OLIVE_L, CREAM, BRICK, OCHRE, OLIVE_L, CREAM, BRICK)
    for i, k in enumerate(range(8, len(sm) - 6, 14)):
        x, y = sm[k]
        P(c, [(x - 30, y), (x + 30, y), (x, y + 70)], cols[i % len(cols)], ow=5, seed=30 + i, wob_amp=0.6)


def scene_party(t):
    ctx = new("party", _bg_party)
    xs = (108, 324, 540, 756, 972)
    looks = ("doc_a", "doc_b", "goldberger", "doc_c", "doc_d")
    tg = wt("D2", 11)                                    # "yuttu"
    swallow = prog(t, tg - 0.1, tg + 0.5)
    result = t >= cues.st("D3")
    scared = t >= wt("D4", 0) - 0.05
    lamp(ctx, 540, 890, 0.8, t, glow=0.9)
    hands = []
    for i, (x, lk) in enumerate(zip(xs, looks)):
        raise_ = ease01(t, wt("D2", 1) + 0.15 * i, 0.5) * (1 - ease_out(swallow))
        pose = dict(tilt=-14 * ease_out(swallow) * (1 if i % 2 == 0 else -1) * 0.8,
                    mouth="gulp" if 0.15 < swallow < 0.95 else ("smile" if result and not scared else ("oh" if scared else "flat")),
                    eyes="blink" if 0.15 < swallow < 0.9 else ("wide" if scared else "open"),
                    brows=0.5 if scared else 0.0, sweat=1.0 if (swallow > 0.2 and not result) else 0.0,
                    arm_l=(12, 30), arm_r=(10 + 120 * raise_, 40 + 20 * raise_), blush=0.7 if result else 0.0, face=(-0.3, -0.1, 0.0, 0.1, 0.3)[i])
        b = bust(ctx, x, 1080 + 6 * math.sin(tq(t) * 3 + i), 0.76, lk, pose, t=t, seed=40 + i)
        hands.append((b["handR"], raise_, i))
    table(ctx, -60, W + 60, 1170, col=Hx("#4E3A2A"), seed=11, depth=84, edge=50)
    for hnd, rk, i in hands:                             # el elde hap
        if hnd and rk > 0.05 and swallow < 0.5:
            pill(ctx, hnd[0], hnd[1] - 24, 17, 0.3 * i, seed=i, t=t, ow=4)
    P(ctx, ellipse_pts(540, 1160, 250, 38, 30), Hx("#8A8A8E"), ow=7, seed=4, wob_amp=0.9, shade=(Hx("#5E5E64"), 8, 0.5))
    n_p = 9 if swallow < 0.3 else max(0, int(9 * (1 - (swallow - 0.3) / 0.7)))
    for i in range(n_p):
        pill(ctx, 440 + (i % 5) * 44 + 16 * (i // 5), 1148 + 12 * (i // 5), 17, i, seed=i, t=0)
    jar(ctx, 175, 1122, 0.8, "KABUK", liquid=Hx("#B88A5A"), seed=2, t=t)
    jar(ctx, 905, 1122, 0.8, "İDRAR", liquid=Hx("#E8D060"), seed=3, t=t)
    jar(ctx, 1012, 1132, 0.7, "DIŞKI", liquid=Hx("#7A5A32"), seed=5, t=t)
    # damgalar ve onaylar (uyarı gelince yıl damgası ve onaylar söner)
    fade_w = 1.0 - prog(t, cues.STAMP_WARN - 0.25, cues.STAMP_WARN - 0.02)
    k1 = pop_k(t, cues.STAMP_YEAR, 0.28, 2.4)
    if k1 > 0 and fade_w > 0.02:
        stamp(ctx, 330, 600, "1916", 150, BRICK, -7, min(1.0, k1)) if fade_w > 0.98 else None
        if fade_w <= 0.98:
            stamp(ctx, 330, 600 - 30 * (1 - fade_w), "1916", 150 * (0.7 + 0.3 * fade_w), mix(BRICK, Hx("#241B33"), 1 - fade_w), -7, 1.0)
    if result and fade_w > 0.02:
        for i, x in enumerate(xs):
            ck = prog(t, cues.st("D3") + 0.18 * i, cues.st("D3") + 0.18 * i + 0.35)
            check(ctx, x, 790, 1.15 * (0.6 + 0.4 * fade_w), ck * fade_w)
    k2 = prog(t, cues.STAMP_WARN, cues.STAMP_WARN + 0.18)
    if k2 > 0:
        stamp(ctx, 540, 740, "SAKIN\nDENEMEYİN", 124, BRICK, -6, k2)
    return fin(ctx)


# ═══════════════════════ E0: boş tabak ═══════════════════════
def _bg_tabletop(c):
    c.vgrad(0, 0, W, H, [(0, Hx("#5A3A22")), (1.0, Hx("#2E1C10"))])
    for i in range(40):
        y = rng_hash(8, i, 1) * H
        c.line([(-20, y), (W + 20, y + (rng_hash(8, i, 2) - 0.5) * 24)], 6 + 10 * rng_hash(8, i, 3), Hx("#3A2414") if i % 2 else Hx("#7A5232"), 0.22, cap=True)
    c.glow(540, 800, 760, Hx("#E8A04A"), 0.28)


def scene_plate(t):
    ctx = new("tabletop", _bg_tabletop)
    t_ans = wt("E0b", 1)
    pulse = 1.0 + 0.07 * math.exp(-max(0.0, t - t_ans) * 6) * (1 if t >= t_ans else 0)
    ready = ease01(t, cues.gstart(7) - 0.05, 0.5)
    # çatal / kaşık
    P(ctx, rrect_pts(150, 560, 190, 1160, 16), Hx("#BFC0C4"), ow=7, seed=2, wob_amp=0.9, shade=(Hx("#8A8B90"), 7, 0.5))
    for i in range(3):
        P(ctx, rrect_pts(124 + i * 24, 430, 142 + i * 24, 600, 8), Hx("#BFC0C4"), ow=5, seed=3 + i, wob_amp=0.6)
    P(ctx, rrect_pts(890, 640, 930, 1160, 16), Hx("#BFC0C4"), ow=7, seed=5, wob_amp=0.9, shade=(Hx("#8A8B90"), 7, 0.5))
    P(ctx, ellipse_pts(910, 560, 56, 96, 20), Hx("#BFC0C4"), ow=7, seed=6, wob_amp=0.9)
    if t >= t_ans:
        ctx.glow(540, 820, 520 * (0.8 + 0.4 * ease_out(prog(t, t_ans, t_ans + 0.5))), Hx("#FFD27A"), 0.55)
    plate(ctx, 540, 820, 380 * pulse * (0.4 + 0.6 * ready), 380 * pulse * (0.4 + 0.6 * ready), seed=3)
    # soru işaretleri
    for i, (x, y, rot) in enumerate(((190, 420, -14), (850, 460, 12), (540, 360, -4), (300, 1020, 10), (800, 1000, -9))):
        wi = min(i, 3)
        k = pop_k(t, wt("E0", wi) - 0.05, 0.32, 2.4)
        gone = ease_in(prog(t, t_ans - 0.05, t_ans + 0.25), 2)
        if k > 0 and gone < 1:
            ctx.text(x + 6, y + 8, "?", 250 * k * (1 - gone), INK, path=FONT_SLAB)
            ctx.text(x, y, "?", 250 * k * (1 - gone), Hx("#F6B73C"), path=FONT_SLAB, stroke=7, stroke_fill=INK)
    if t >= t_ans:
        for i in range(8):
            a = i * math.pi / 4 + 0.4
            u = ease_out(prog(t, t_ans, t_ans + 0.6))
            sparkle(ctx, 540 + math.cos(a) * (420 + 40 * math.sin(i)) * u, 820 + math.sin(a) * (420 + 40 * math.cos(i)) * u, 24 * (1 - 0.4 * u), LAMP, 0.9 * (1 - 0.5 * u), a)
    return fin(ctx)


# ═══════════════════════ E1: diyet testi (yetimhane) ═══════════════════════
def scene_diet(t):
    ctx = new("orphan", _bg_orphan)
    cure = ease01(t, wt("E2b", 0) + 0.1, 0.8)
    sk = 1.0 - cure
    tg = wt("E2", 0)
    for i, (x, look) in enumerate(((250, "kid_a"), (830, "kid_c"))):
        pose = dict(_kid_looks(sk, t), face=(-0.3, 0.3)[i], tilt=3 * math.sin(tq(t) * 1.6 + i) * (1 if sk > 0.5 else 0.3), arm_l=(10, 50), arm_r=(10, 50))
        if cure > 0.5:
            pose.update(mouth="smile", eyes="open", sweat=0.0, brows=0.4, blush=1.0)
        bust(ctx, x, 1075 + 4 * math.sin(tq(t) * 2 + i), 1.05, look, pose, t=t, seed=10 + i)
    ge = ease_out(prog(t, tg - 0.15, tg + 0.45), 3)
    gp = dict(mouth="smile", brows=0.4, face=0.0, tilt=3 * math.sin(tq(t) * 2), arm_l=(30 + 30 * math.sin(tq(t) * 3), 40), arm_r=(25 + 35 * math.sin(tq(t) * 3 + 1), 40))
    if ge > 0:
        bust(ctx, lerp(540, 540, ge), lerp(1500, 1110, ge), 0.9, "goldberger", gp, t=t, seed=1)
    table(ctx, -60, W + 60, 1190, col=Hx("#7A5232"), seed=6)
    plate(ctx, 250, 1160, 150, 40, seed=1)
    mush(ctx, 250, 1148, 78, 24, seed=2)
    molasses(ctx, 320, 1156, 36, 12, seed=3)
    plate(ctx, 830, 1160, 150, 40, seed=2)
    jug(ctx, 540, 1130, 0.5, None, seed=2)
    # Goldberger menüye ekler: süt, yumurta, et
    for (wi, kind) in ((3, "milk"), (4, "egg"), (6, "meat")):
        k = pop_k(t, wt("E2", wi) - 0.05, 0.34, 2.2)
        if k > 0:
            if kind == "milk":
                milk(ctx, 905, 1100 - 30 * (1 - min(1, k)), 0.62 * k)
            elif kind == "egg":
                for j in range(3):
                    egg(ctx, 770 + j * 36, 1146 - 6 * (1 - min(1, k)), 22 * k, seed=j)
            else:
                meat(ctx, 830, 1150, 0.62 * k, seed=3)
    # etiket: soldaki / sağdaki tabak
    k1 = pop_k(t, wt("E1", 2) - 0.1, 0.35)
    tag(ctx, 285, 640, "MISIR + PEKMEZ", 36, k=k1, rot=-3, seed=3, path=FONT_SLAB, fill_text=OCHRE_D)
    k2 = pop_k(t, wt("E2", 2) - 0.05, 0.35)
    tag(ctx, 790, 640, "SÜT · YUMURTA · ET", 34, k=k2, rot=3, seed=4, path=FONT_SLAB, fill_text=OLIVE_D)
    if cure > 0.4:
        for i in range(6):
            a = i * math.pi / 3 + t
            u = ease_out(prog(t, wt("E2b", 2) - 0.1, wt("E2b", 2) + 0.7))
            for x in (250, 830):
                sparkle(ctx, x + math.cos(a) * 190 * u, 820 + math.sin(a) * 150 * u, 22 * (1 - 0.5 * u), LAMP, 0.9 * (1 - 0.6 * u), a)
    return fin(ctx)


# ═══════════════════════ E3: hapishane çiftliği ═══════════════════════
def _bg_prison(c):
    sky_wash(c, [(0, Hx("#D9B27A")), (0.45, Hx("#EBD0A0")), (1.0, Hx("#F1E2BE"))], seed=21)
    r0 = ridge(1000, 30, 0.0038, 1.0)
    hill(c, r0, Hx("#B88B4A"), light=Hx("#D8B070"), seed=1, grass=Hx("#7A5C2A"), grass_n=24)
    # gözetleme kulesi
    for dx in (-40, 40):
        c.line([(840 + dx, 1000), (840 + dx * 0.6, 640)], 14, INK, 1.0)
        c.line([(840 + dx, 1000), (840 + dx * 0.6, 640)], 8, Hx("#6A4A2E"), 1.0)
    P(c, [(770, 640), (910, 640), (930, 560), (750, 560)], Hx("#6A4A2E"), ow=7, seed=3, wob_amp=1.0)
    P(c, [(740, 560), (840, 500), (940, 560)], Hx("#4E3A28"), ow=7, seed=4, wob_amp=0.8)
    r1 = ridge(1200, 36, 0.0032, 2.9)
    hill(c, r1, Hx("#9B8A44"), light=Hx("#BDAE6A"), seed=2, grass=Hx("#5C6A2A"), grass_n=34)
    fence(c, -10, W + 30, 920, 1.0, seed=3)
    for i in range(0, 12):                                        # dikenli tel
        x = i * 100
        c.line([(x, 960), (x + 50, 940), (x + 100, 960)], 3, INK, 0.9, cap=False)


def scene_prison(t):
    ctx = new("prison", _bg_prison)
    ps = 0.62
    xs = (100, 270, 440, 610, 780, 950)
    looks = ("convict_a", "convict_b", "convict_c", "convict_a", "convict_b", "convict_c")
    sick_idx = (1, 3, 5)
    for i, (x, lk) in enumerate(zip(xs, looks)):
        sk = 0.0
        if i in sick_idx:
            sk = ease01(t, wt("E4", 1) + 0.1 * sick_idx.index(i), 0.5)
        eat = t < wt("E4", 0) and t > wt("E3", 5)
        pose = dict(_kid_looks(sk, t), mouth=("worry" if sk > 0.5 else ("chew" if eat else "flat")), eyes="sad" if sk > 0.5 else "open",
                    brows=-1.0 * sk, blush=0.0, face=(-0.2, 0.1, 0.0, -0.1, 0.2, 0.0)[i], arm_l=(12, 36), arm_r=(12, 36 + 8 * math.sin(tq(t) * 6 + i)))
        bust(ctx, x, 1085 + 4 * math.sin(tq(t) * 2.2 + i), ps, lk, pose, t=t, seed=60 + i)
    table(ctx, -60, W + 60, 1170, col=Hx("#6A4A2E"), seed=8, depth=80, edge=48)
    for x in xs:
        cornbread(ctx, x, 1180, 96, 36, seed=int(x))
    jug(ctx, 540, 1130, 0.45, None, seed=3)
    # af kâğıdı
    k = pop_k(t, wt("E3", 1) - 0.1, 0.4)
    if k > 0:
        bob = 8 * math.sin(tq(t) * 3)
        P(ctx, [(430, 500 + bob), (650, 500 + bob), (650, 640 + bob), (430, 640 + bob)], CREAM, ow=7 * k, seed=5, wob_amp=1.2, shade=(CREAM_D, 8, 0.5))
        ctx.line([(430, 520 + bob), (650, 520 + bob)], 6, CREAM_D, 1.0, cap=False)
        ctx.text(540, 570 + bob, "AF", 82 * k, BRICK, path=FONT_SLAB)
        ctx.poly(ellipse_pts(540, 622 + bob, 20 * k, 20 * k, 14), BRICK)
        for dx in (-1, 1):
            ctx.line([(540, 622 + bob), (540 + dx * 24, 668 + bob)], 9, BRICK_D, 1.0)
    ky = pop_k(t, wt("E4", 0) - 0.05, 0.4)
    tag(ctx, 540, 770, "YAKLAŞIK YARISI", 66, k=ky, rot=-2, seed=6, path=FONT_SLAB, fill_text=BRICK_D)
    return fin(ctx)


# ═══════════════════════ F1: niasin ═══════════════════════
def _bg_lab(c):
    c.vgrad(0, 0, W, H, [(0, Hx("#4A7774")), (1.0, Hx("#2E4A4A"))])
    plank_wall(c, 0, 1180, Hx("#4F7F7A"), seed=18, gap=180)
    for r, y in enumerate((420, 640)):
        P(c, [(40, y), (400, y), (400, y + 28), (40, y + 28)], Hx("#8A6A3A"), ow=6, seed=5 + r, wob_amp=0.8)
        for i, col in enumerate((OCHRE, BRICK, OLIVE_L, CREAM, Hx("#9CC4D4"))):
            P(c, rrect_pts(60 + i * 66, y - 66, 108 + i * 66, y, 10), col, ow=5, seed=30 + r * 7 + i, wob_amp=0.6)
    c.glow(540, 800, 700, Hx("#FFE9A8"), 0.28)


def scene_niacin(t):
    ctx = new("lab", _bg_lab)
    mv = ease_in_out = ease_io(prog(t, cues.st("F2") - 0.1, cues.st("F2") + 0.5))
    bx = lerp(540, 750, mv)
    sc = lerp(1.45, 1.05, mv)
    kb = pop_k(t, cues.gstart(10), 0.5, 1.8)
    for i in range(16):                                   # dönen ışınlar
        a = i * math.pi / 8 + t * 0.4
        ctx.line([(bx + math.cos(a) * 260 * sc, 860 + math.sin(a) * 260 * sc), (bx + math.cos(a) * 480 * sc, 860 + math.sin(a) * 480 * sc)], 18, Hx("#FFE08A"), 0.25, cap=True)
    bottle(ctx, bx, 880, 1.0 * sc * min(1, kb), "NİASİN", seed=3)
    if t >= wt("F1", 1):
        for i in range(10):
            u = ((t - wt("F1", 1)) * 0.6 + i / 10) % 1.0
            sparkle(ctx, bx + 190 * math.sin(i * 2.1) * sc, 1120 - u * 560, 22 * (1 - u * 0.5), LAMP, 0.9 * (1 - u), i)
    # 1937 damgası ve mezar taşı
    k37 = pop_k(t, wt("F2", 2) - 0.05, 0.32, 2.2)
    if k37 > 0:
        stamp(ctx, 760, 560, "1937", 150, BRICK, 6, min(1.0, k37))
    kt = ease_out(prog(t, wt("F2", 3) - 0.1, wt("F2", 3) + 0.6), 3)
    if kt > 0:
        tx = lerp(-260, 230, kt)
        ctx.glow(tx, 1000, 360, Hx("#FFD7A0"), 0.34 * kt)
        tombstone(ctx, tx, 1170, 1.05, "J. GOLDBERGER", "1929", seed=2)
        fl = 1 + 0.12 * math.sin(tq(t) * 11)
        P(ctx, rrect_pts(tx + 108, 1140, tx + 138, 1178, 6), CREAM, ow=4, seed=3, wob_amp=0.5)
        ctx.poly(smooth_closed([(tx + 123, 1100 - 14 * fl), (tx + 132, 1124), (tx + 123, 1142), (tx + 114, 1124)], 4), LAMP)
    return fin(ctx)


# ═══════════════════════ F3: mısır suçlu değildi (kireç) ═══════════════════════
def _bg_gold(c):
    c.vgrad(0, 0, W, H, [(0, Hx("#E6A25A")), (0.5, Hx("#F2C27F")), (1.0, Hx("#C9803E"))])
    c.glow(540, 760, 820, Hx("#FFF0B8"), 0.45)
    for i in range(30):
        y = rng_hash(9, i, 1) * H
        c.line([(-20, y), (W + 20, y + (rng_hash(9, i, 2) - 0.5) * 20)], 8 + 12 * rng_hash(9, i, 3), Hx("#FFE0A0"), 0.07, cap=True)


def _corn_innocent(t):
    ctx = new("gold", _bg_gold)
    k = pop_k(t, cues.gstart(11), 0.5, 1.8)
    up = ease01(t, wt("F3", 4) - 0.2, 0.4)
    wig = 3 * math.sin(tq(t) * 3)
    for i in range(14):
        a = i * 2 * math.pi / 14 + t * 0.3
        ctx.line([(540 + math.cos(a) * 330, 800 + math.sin(a) * 330), (540 + math.cos(a) * 500, 800 + math.sin(a) * 500)], 14, Hx("#FFF0B8"), 0.35, cap=True)
    corn_cob(ctx, 540, 860, 2.0 * min(1, k), rot=wig, seed=3, face=True, t=t, arms=up)
    ks = pop_k(t, wt("F3", 5) - 0.1, 0.4)
    tag(ctx, 540, 470, "SUÇSUZ", 92, k=ks, rot=-3, seed=5, path=FONT_SLAB, fill_text=OLIVE_D)
    return fin(ctx)


def _bg_village(c):
    c.vgrad(0, 0, W, H, [(0, Hx("#E88A52")), (0.38, Hx("#F6C486")), (0.7, Hx("#F8DDA4")), (1.0, Hx("#D9A05A"))])
    c.glow(300, 520, 520, Hx("#FFF2C0"), 0.50)
    r0 = ridge(980, 40, 0.0036, 1.4)
    hill(c, r0, Hx("#B5693A"), light=Hx("#D88A52"), seed=3, grass=Hx("#7A4A2A"), grass_n=18)
    # kerpiç kulübe
    P(c, [(660, 1010), (660, 760), (800, 700), (960, 740), (1010, 1010)], Hx("#D9A56A"), ow=8, seed=5, wob_amp=1.2, shade=(Hx("#A8713E"), 12, 0.5), dry=(Hx("#B88650"), 14, 0.35))
    P(c, [(640, 770), (820, 676), (1040, 744), (1020, 790), (820, 740), (660, 806)], Hx("#C9A24A"), ow=7, seed=6, wob_amp=1.0, hatch=(Hx("#9A7A30"), 14, 0.4))
    P(c, smooth_closed([(790, 1010), (790, 880), (830, 840), (870, 880), (870, 1010)], 5), Hx("#4A2E1A"), ow=6, seed=7, wob_amp=0.8)
    for x, sc in ((90, 1.0), (240, 0.8)):                         # agav
        for j in range(7):
            ang = -1.35 + j * 0.45
            P(c, [(x, 1020), (x + math.cos(ang) * 150 * sc - 14, 1020 + math.sin(ang) * 150 * sc), (x + math.cos(ang) * 190 * sc, 1020 + math.sin(ang) * 190 * sc), (x + math.cos(ang) * 150 * sc + 14, 1020 + math.sin(ang) * 150 * sc)],
              OLIVE if j % 2 else OLIVE_D, ow=5, seed=40 + j, wob_amp=0.6)
    r1 = ridge(1260, 36, 0.0032, 3.0)
    hill(c, r1, Hx("#8A5A30"), light=Hx("#B07A44"), seed=4, grass=Hx("#5A3A20"), grass_n=24)
    c.rect(0, 1480, W, H + 40, Hx("#6A4224"))


def _village(t):
    ctx = new("village", _bg_village)
    tl = wt("F4", 5)                                     # "kireç"
    pour = prog(t, tl - 0.15, tl + 0.9)
    milky = ease_out(prog(t, tl + 0.1, tl + 1.2))
    stir = math.sin(tq(t) * 6.0)
    bust(ctx, 480, 1100, 1.2, "maya", dict(mouth="smile", brows=0.3, face=0.2, tilt=3 * stir, arm_l=(36, 70), arm_r=(60 + 20 * stir, 50), blush=0.5), t=t, seed=9)
    # kavanoz kireç
    jx, jy = 900, 1010
    tilt = -50 * ease_in_out_(pour) if pour < 1 else -50 * (1 - prog(t, tl + 0.9, tl + 1.3))
    ctx.glow(jx, jy - 40, 260, Hx("#FFF2C0"), 0.25)
    jar(ctx, jx, jy, 0.95, "KİREÇ", liquid=Hx("#F7F2E6"), seed=4, t=t)
    if 0.05 < pour < 1.0:
        for i in range(22):
            u = ((t - (tl - 0.1)) * 1.8 + i / 22) % 1.0
            px = lerp(jx - 60, 600, u) + 10 * math.sin(i * 3)
            py = lerp(jy - 140, 1160, u ** 1.6)
            ctx.circ(px, py, 5 + 4 * rng_hash(2, i, 1), Hx("#FFFFFF"), 0.9 * (1 - u * 0.4))
    # kazan
    X = Xf(540, 1235, 1.0)
    P(ctx, X.pts(smooth_closed([(-120, -80), (120, -80), (160, 10), (130, 100), (60, 140), (-60, 140), (-130, 100), (-160, 10)], 5)), Hx("#B8683E"), ow=9, seed=1, wob_amp=1.3, shade=(Hx("#7E4326"), 14, 0.5), hatch=(Hx("#9C5532"), 22, 0.30))
    P(ctx, X.pts(ellipse_pts(0, -80, 124, 26, 28)), Hx("#7E4326"), ow=8, seed=2, wob_amp=0.9)
    water = mix(Hx("#8DA48A"), Hx("#F2E7CF"), milky)
    ctx.poly(X.pts(ellipse_pts(0, -80, 108, 19, 26)), water)
    for i in range(9):
        ctx.poly(blob(*X.p(-84 + i * 21 + 5 * math.sin(i + t * 2), -82 + 3 * math.cos(i * 2)), 11, 8, 7, 0.2, i), OCHRE_L)
    steam(ctx, 690, 1140, t, n=4, h=240, a=0.45)
    if t >= wt("F4b", 2) - 0.1:                          # niasin serbest kalır
        for i in range(14):
            u = ((t - wt("F4b", 2)) * 0.55 + i / 14) % 1.0
            sparkle(ctx, 540 + 150 * math.sin(i * 1.9 + t) * (0.4 + u), 1150 - u * 640, 24 * (1 - u * 0.5), LAMP, 0.95 * (1 - u), i)
        kk = pop_k(t, wt("F4b", 2) - 0.05, 0.4)
        tag(ctx, 540, 610, "NİASİN", 90, k=kk, rot=-3, seed=8, path=FONT_SLAB, fill_text=OCHRE_D)
    return fin(ctx)


def ease_in_out_(x):
    return ease_io(x)


def scene_corn(t):
    tb = cues.st("F4") - 0.08
    return sub_whip(t, tb, _corn_innocent, _village, 0.24)


# ═══════════════════════ F5: fırtınalı gemi (kireç iskelede kaldı) ═══════════════════════
def _bg_storm(c):
    c.vgrad(0, 0, W, H, [(0, Hx("#1E2540")), (0.45, Hx("#3A4668")), (0.8, Hx("#5F7494")), (1.0, Hx("#7C90AC"))])
    for i in range(40):                                               # yağmur çizgileri
        x = rng_hash(3, i, 1) * (W + 300) - 150
        y = rng_hash(3, i, 2) * 1100
        c.line([(x, y), (x - 40, y + 130)], 5, Hx("#A9B8D0"), 0.14 + 0.1 * rng_hash(3, i, 3), cap=True)
    for i, (x, y, sc) in enumerate(((160, 280, 1.3), (760, 200, 1.6), (500, 460, 1.1))):
        cloud(c, x, y, sc, Hx("#46557A"), 20 + i)


def scene_ship(t):
    ctx = new("storm", _bg_storm)
    t0 = cues.gstart(12)
    u = ease_out(prog(t, t0, t0 + 3.6), 1.6)
    lightning = max(0.0, 1 - abs(t - (wt("F5", 3) + 0.05)) / 0.12)
    if lightning > 0:
        ctx.poly([(780, 0), (840, 0), (800, 330), (900, 330), (700, 700), (760, 380), (680, 380)], Hx("#FFF4C0"), 0.9 * lightning)
    waves(ctx, 1190, t, [Hx("#2F4A6E"), Hx("#27405F"), Hx("#1F3450"), Hx("#18283F")], amp=28, seed=2, speed=1.1, n=4)
    # iskele + unutulan kireç
    P(ctx, [(-30, 1130), (250, 1130), (250, 1190), (-30, 1190)], Hx("#6A4A2E"), ow=7, seed=3, wob_amp=1.0, dry=(Hx("#3E2A18"), 8, 0.4))
    for x in (30, 200):
        P(ctx, [(x - 12, 1130), (x + 12, 1130), (x + 12, 1320), (x - 12, 1320)], Hx("#4E3A28"), ow=6, seed=4 + x, wob_amp=0.8)
    wave_ = 8 * math.sin(tq(t) * 7)
    jar(ctx, 130, 1050, 0.9, "KİREÇ", liquid=Hx("#F7F2E6"), seed=2, t=t)
    for sx in (-1, 1):
        ctx.poly(ellipse_pts(130 + sx * 18, 996, 6, 8, 8), INK)
    ink_line(ctx, [(112, 1026), (130, 1014), (148, 1026)], 5, INK, 3, t, 0.2, smooth=True)
    ink_line(ctx, [(176, 990), (206 + wave_, 950)], 8, INK, 5, t, 0.2)
    ship(ctx, lerp(520, 780, u), 1130 + 10 * math.sin(tq(t) * 3.4), 1.05, t, seed=2, rock=3.2 * math.sin(tq(t) * 2.4))
    waves(ctx, 1300, t * 1.1 + 1.0, [Hx("#1F3450"), Hx("#18283F"), Hx("#101C2E")], amp=24, seed=5, speed=1.3, n=3)
    return fin(ctx)


# ═══════════════════════ G: mikrop çarpı ═══════════════════════
def _bg_end(c):
    c.vgrad(0, 0, W, H, [(0, Hx("#E8C98A")), (1.0, Hx("#D9A85A"))])
    c.glow(540, 820, 760, Hx("#FFF0C0"), 0.55)
    for i in range(26):
        y = rng_hash(11, i, 1) * H
        c.line([(-20, y), (W + 20, y + (rng_hash(11, i, 2) - 0.5) * 20)], 10 + 14 * rng_hash(11, i, 3), Hx("#FFF4D0"), 0.09, cap=True)


def scene_end(t):
    ctx = new("end", _bg_end)
    tx = cues.GERM_X
    dead = ease_out(prog(t, tx, tx + 0.45), 2)
    k = pop_k(t, cues.gstart(13), 0.4, 1.6)
    r = 250 * min(1, k) * (1 - 0.18 * dead)
    col = mix(OLIVE, Hx("#8A8F72"), dead)
    germ(ctx, 540, 830, r, t * (1 - 0.8 * dead), col=col, seed=7, mood="mean" if dead < 0.5 else "sad", ow=11)
    cross(ctx, 540, 830, 3.9, prog(t, tx, tx + 0.35))
    if dead > 0.3:
        for i in range(10):
            a = i * 2 * math.pi / 10
            u = ease_out(prog(t, tx + 0.1, tx + 0.8))
            sparkle(ctx, 540 + math.cos(a) * 420 * u, 830 + math.sin(a) * 420 * u, 24 * (1 - u * 0.5), LAMP, 0.9 * (1 - u * 0.6), a)
    return fin(ctx)


def render_group(g, t):
    return GROUP_FN[g](t)


GROUP_FN = {
    0: lambda t: scene_card(t),
    1: scene_south,
    2: scene_symptoms,
    3: scene_doctors,
    4: scene_orphanage,
    5: scene_skeptics,
    6: scene_party,
    7: scene_plate,
    8: scene_diet,
    9: scene_prison,
    10: scene_niacin,
    11: scene_corn,
    12: scene_ship,
    13: scene_end,
}
