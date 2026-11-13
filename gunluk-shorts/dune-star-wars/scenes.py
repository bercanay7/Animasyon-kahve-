"""Dune × Star Wars — 16 sahne grubu, kâğıt kesme diyorama stili. Her fonksiyon t için 1080x1920 RGB döndürür."""
import math

import cues
from cues import st, wt, we, en
from figs import *  # noqa

TWO_PI = 2 * math.pi


def new(t, z=1.0, cx=W / 2, cy=H / 2, shake=True):
    ctx = Ctx()
    sx, sy = cues.shake(t) if shake else (0.0, 0.0)
    ctx.cam(cx, cy, z, (sx, sy))
    return ctx


def fin(ctx, t, **kw):
    return paper_post(ctx.finish(), t, **kw)


def palmix(a, b, k):
    k = clamp(k)
    return dict(sky=[(p, mix(ca, cb, k)) for (p, ca), (_, cb) in zip(a["sky"], b["sky"])],
                ridges=[mix(x, y, k) for x, y in zip(a["ridges"], b["ridges"])],
                sun=mix(a["sun"], b["sun"], k), halo=mix(a["halo"], b["halo"], k), ink=mix(a["ink"], b["ink"], k),
                acc=b["acc"] if k > 0.5 else a["acc"])


def pop_k(t, t0, d=0.30, over=2.0):
    """0'dan 1'e taşarak (back_out) giriş; başlamadan önce tam 0"""
    u = prog(t, t0, t0 + d)
    return 0.0 if u <= 0 else back_out(u, over)


def slide_in(t, t0, d=0.45):
    return 1.0 - ease_out(prog(t, t0, t0 + d), 3)      # 1 → 0


# ═══════════════ kanca dünyası (iki dünyanın karışımı) ═══════════════
def hook_world(ctx, tt, kid_ring=0.0, throne_k=0.0, amp=1.0, ts=None):
    P = PAL["mash"]
    sky(ctx, P["sky"])
    stars(ctx, 70, 3, 0, 900, 0.9, tt)
    if throne_k > 0:
        throne(ctx, 800, 1040, 1.9, Hx("#241B3D"), glow=Hx("#FFB765"))
    sun(ctx, 300, 960 + 6 * math.sin(tt * 0.8), 120, P)
    sun(ctx, 640, 1010, 58, dict(P, sun=Hx("#FFD8A0"), halo=Hx("#FF9F5A")))
    dunes(ctx, P, tt, base=1000, spread=100, n=6, amp=26)
    worm_mouth(ctx, 800, 1130, 110, tt)
    kid(ctx, 250, 1090, 0.9)
    if kid_ring > 0:
        ctx.ring(250, 1020, 78 + 6 * math.sin(tt * 5), 5, GOLD, 0.85 * kid_ring)
    sand_streaks(ctx, ts if ts is not None else tt, (255, 226, 170), n=16, y0=1020, y1=1500, a=0.20 * amp)


def title_lines(ctx, dy=0.0):
    for (y, s, px, col) in ((430, "TATOOINE", 150, CREAM), (590, "ARRAKİS’TEN Mİ", 100, Hx("#8BE0FF")), (760, "GELDİ?", 170, CREAM)):
        ptext(ctx, 540, y + dy, s, px, col, FONT_TITLE, shadow=(5, 7, Hx("#1A0C08")))


def scene_hook(t, still=False):
    tt = 0.0 if still else t
    zk = 0.0 if still else prog(tt, 1.0, en("A1"))
    ctx = new(tt, z=1.0 + 0.05 * zk, cx=W / 2, cy=lerp(H / 2, H * 0.62, zk), shake=not still)
    kr = ease_out(prog(tt, wt("A1", 7) - 0.1, wt("A1", 7) + 0.3)) * (1 - prog(tt, we("A1", 7) + 0.9, we("A1", 7) + 1.3))
    tk = ease_out(prog(tt, wt("A1", 11) - 0.1, wt("A1", 11) + 0.8))
    hook_world(ctx, tt if not still else 0.0, kid_ring=kr, throne_k=tk, amp=0.0 if still else prog(tt, 0.0, 0.5))
    if not still:
        if kr > 0:
            tagchip(ctx, 250, 930, "ÇOCUK", 46, a=kr)
        if tk > 0:
            tagchip(ctx, 700, 790, "İMPARATOR", 46, a=tk)
    fall = ease_in(prog(tt, 0.85, 1.30), 2.0)
    if tt < 1.35:
        title_lines(ctx, dy=-2300 * fall if not still else 0.0)
    return fin(ctx, tt)


# ═══════════════ A2: 1977 klaket → 12 yıl → 1965 kitap ═══════════════
def scene_timeline(t):
    ctx = new(t)
    desk(ctx, "warm", t)
    s0 = st("A2")
    # zaman şeridi
    ys = 990
    x77, x65 = 790, 300
    prect(ctx, 70, ys - 22, 1010, ys + 22, CREAM, sh=(6, 9), sh_a=0.3, edge=0.1)
    for yr in range(1965, 1978):
        x = lerp(x65, x77, (yr - 1965) / 12)
        ctx.line([(x, ys - 22), (x, ys + (12 if yr % 12 else 22))], 3, INK, 0.7, cap=False)
    # klaket (1977)
    kc = pop_k(t, wt("A2", 2) - 0.05, 0.4)
    if kc > 0:
        op = 26 * (1 - ease_out(prog(t, wt("A2", 2) + 0.1, wt("A2", 2) + 0.35)))
        clapper(ctx, x77, 640 + (1 - kc) * -420, 440, 300, "STAR WARS", "1977", open_deg=op)
    if kc > 0.5:
        ptext(ctx, x77, ys + 80, "1977", 70, SWYEL, FONT_TITLE, shadow=(3, 4, (0, 0, 0)))
    # 12 yıl köprüsü: sağdan sola uzar
    k12 = ease_io(prog(t, wt("A2", 5) - 0.05, wt("A2", 8) + 0.15))
    if k12 > 0.02:
        xe = lerp(x77, x65, k12)
        L = [(x77, ys - 60), (x77, ys - 100), (xe, ys - 100), (xe, ys - 60)]
        ctx.line(L, 6, GOLD, 1.0)
        cx_ = (x77 + xe) / 2
        yrn = int(round(lerp(1977, 1965, k12)))
        tagchip(ctx, cx_, ys - 150, "12 YIL", 58, col=GOLD, anchor="mm")
    # kitap (1965)
    kb = pop_k(t, wt("A2", 11) - 0.05, 0.45)
    if kb > 0:
        book(ctx, x65, 660 + (1 - kb) * -420, 290, 410, "DUNE", "FRANK HERBERT", t=t)
        ptext(ctx, x65, ys + 80, "1965", 70, Hx("#FFC47A"), FONT_TITLE, shadow=(3, 4, (0, 0, 0)))
    return fin(ctx, t, warm=0.02)


# ═══════════════ A3: ödünç? + reddedilmiş teklif ═══════════════
def scene_question(t):
    ctx = new(t)
    P = PAL["sw"]
    sky(ctx, [(0, Hx("#0E1730")), (1.0, Hx("#2B3F63"))])
    stars(ctx, 60, 8, 0, 1000, 0.9, t)
    # ödünç ok: kitap → klaket
    kb = pop_k(t, st("A3") + 0.2, 0.4)
    book(ctx, 240, 560 + (1 - kb) * 300, 170, 240, "DUNE", "", t=t)
    kc = pop_k(t, wt("A3", 1) - 0.1, 0.4)
    clapper(ctx, 830, 560 + (1 - kc) * 300, 260, 180, "STAR", "WARS", open_deg=12)
    ka = ease_out(prog(t, wt("A3", 6), wt("A3", 8)))
    if ka > 0.02:
        pts = [(340, 540), (440, 470), (640, 470), (720, 540)]
        ctx.line(cut_poly(pts, ka), 8, GOLD, 1.0)
        if ka > 0.95:
            ctx.poly([(720, 540), (690, 500), (700, 556)], GOLD)
    kq = pop_k(t, wt("A3", 8), 0.45, 2.5)
    if kq > 0 and t < wt("A3", 13) + 0.6:
        ptext(ctx, 540, 520, "?", 330 * kq, GOLD, FONT_TITLE, shadow=(6, 8, (20, 10, 4)))
    # zarf (reddedilmiş teklif)
    ke = ease_out(prog(t, wt("A3", 9) - 0.1, wt("A3", 9) + 0.55), 3)
    if ke > 0:
        envelope(ctx, 540, 1000 + (1 - ke) * 700, 640, 400, "TEKLİF", "?", flap=1.0, t=t)
    kst = pop_k(t, wt("A3", 13), 0.3, 1.6)
    if kst > 0:
        stamp(ctx, 600, 905, "GERİ ÇEVRİLDİ", 64, RED, -9.0, kst)
    return fin(ctx, t)


# ═══════════════ B1: Dune → Oregon kumulları → çöl gezegeni ═══════════════
def scene_oregon(t):
    ctx = new(t)
    k = ease_io(prog(t, wt("B1", 11) - 0.2, wt("B1", 13) + 0.2))
    P = palmix(PAL["oregon"], PAL["dune"], k)
    sky(ctx, P["sky"])
    # arka plan: okyanus şeridi (Oregon) — sıcaklaşırken solar
    ocean_a = 1 - k
    if ocean_a > 0.02:
        ctx.poly([(0, 900), (W, 900), (W, 1000), (0, 1000)], Hx("#5E87A0"), 0.9 * ocean_a)
        for i in range(5):
            ctx.line([(0, 912 + i * 16), (W, 912 + i * 16 + math.sin(t + i) * 4)], 2, Hx("#DCEBEF"), 0.4 * ocean_a, cap=False)
    # gezegen yükselir
    kp = ease_out(prog(t, wt("B1", 11) - 0.1, wt("B1", 13) + 0.4), 3)
    if kp > 0:
        planet(ctx, 540, 780 + (1 - kp) * 520, 250, (Hx("#E9A25B"), Hx("#D9803F"), Hx("#B9602E"), Hx("#E39A52"), Hx("#C46F36")), ph=t * 0.03, halo=Hx("#FFC47A"), a=1.0)
    # hareketli kum tepeleri (sağa doğru kayar)
    dunes(ctx, P, t, base=1010, spread=104, n=6, drift=t * 90, amp=30, speed=0.5)
    sand_streaks(ctx, t, (255, 240, 200), n=24, y0=950, y1=1500, a=0.26, speed=220)
    # çam ağaçları (Oregon)
    pa = 1 - k
    if pa > 0.05:
        for i, tx in enumerate((120, 190, 880, 960, 70)):
            ty = 1040 + 6 * i
            h = 130 + 40 * (i % 2)
            ctx.poly([(tx - 34, ty), (tx, ty - h), (tx + 34, ty)], mix(Hx("#2F4A2A"), P["ridges"][4], k), 0.95 * pa)
            ctx.poly([(tx - 26, ty - h * 0.45), (tx, ty - h * 1.05), (tx + 26, ty - h * 0.45)], mix(Hx("#385A31"), P["ridges"][4], k), 0.95 * pa)
    # yazar
    ka = pop_k(t, wt("B1", 3), 0.45)
    if ka > 0:
        author(ctx, 300, 1120 + (1 - ka) * 200, 1.25, INK)
    # başlıklar
    kd = pop_k(t, wt("B1", 2) - 0.05, 0.45, 2.2)
    if kd > 0 and t < wt("B1", 5) + 0.3:
        ptext(ctx, 540, 520, "DUNE", 250 * kd, CREAM, FONT_TITLE, shadow=(7, 9, Hx("#3A1C10")))
    if t >= wt("B1", 4) - 0.05:
        tagchip(ctx, 320, 1160, "FRANK HERBERT", 46, a=ease_out(prog(t, wt("B1", 4) - 0.05, wt("B1", 4) + 0.3)))
    if t >= wt("B1", 6) - 0.05 and k < 0.9:
        tagchip(ctx, 540, 420, "OREGON · 1950’LER", 52, anchor="mm", a=ease_out(prog(t, wt("B1", 6) - 0.05, wt("B1", 6) + 0.3)) * (1 - k))
    if kp > 0.4:
        tagchip(ctx, 540, 360, "ARRAKİS", 56, col=GOLD, anchor="mm", a=ease_out(prog(t, wt("B1", 12), wt("B1", 12) + 0.35)))
    return fin(ctx, t, warm=0.01)


# ═══════════════ B2+B3: reddedilen mektuplar → Nebula ═══════════════
def scene_book(t):
    ctx = new(t)
    desk(ctx, "warm", t)
    # reddedilen mektup yığını: sağdan girip sola uçar
    t0, t1 = st("B2") + 0.1, en("B2") + 0.5
    n = 9
    for i in range(n):
        ts = t0 + i * (t1 - t0) / n * 0.9
        u = prog(t, ts, ts + 0.9)
        if u <= 0 or u >= 1:
            continue
        x = lerp(1150, -250, ease_in(u, 1.6) * 0.6 + u * 0.4)
        y = 700 + 130 * math.sin(i * 1.7) + 40 * math.sin(u * 6)
        X = Xf(x, y, 1.0, rot=-14 + 9 * ((i * 5) % 7) / 3 + u * 40)
        sh = [(-110, -145), (110, -145), (110, 145), (-110, 145)]
        pshape(ctx, X.pts(sh), CREAM, sh=(6, 9), sh_a=0.3, edge=0.1)
        for j in range(6):
            ctx.line(X.pts([(-80, -90 + j * 26), (80 - (j % 3) * 30, -90 + j * 26)]), 6, (130, 112, 90), 0.45, cap=False)
        stamp(ctx, *X.p(0, 60), "RET", 56, RED, -12 + (i % 3) * 6, 1.0)
    # sayaç
    cnt = int(clamp((t - st("B2")) / max(0.1, en("B2") - st("B2") + 0.2), 0, 1) * 20)
    if t >= st("B2") and t < st("B3") + 0.25:
        ptext(ctx, 540, 425, f"{cnt}+" if cnt < 20 else "20+", 170, CREAM, FONT_TITLE, shadow=(5, 7, (20, 10, 4)))
        ptext(ctx, 540, 565, "YAYINCI REDDETTİ", 54, Hx("#F0B070"), FONT_BOLD)
    # kitap (ortada) — B3'te yükselir
    kb = ease_out(prog(t, wt("B2", 5) + 0.2, wt("B2", 5) + 0.8), 3)
    kz = 1 + 0.06 * math.sin(t * 2.2)
    if kb > 0:
        book(ctx, 540, 830 + (1 - kb) * 700, 340, 470, "DUNE", "FRANK HERBERT", t=t)
    kn = pop_k(t, wt("B3", 2), 0.5, 2.0)
    if kn > 0:
        gx, gy = 835, 600
        ctx.glow(gx, gy, 230 * kn, GOLD, 0.6)
        star = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5 + t * 0.4
            r = (130 if i % 2 == 0 else 62) * kn
            star.append((gx + math.cos(a) * r, gy + math.sin(a) * r))
        pshape(ctx, star, GOLD, sh=(6, 9), sh_a=0.3)
        ptext(ctx, gx, gy, "NEBULA", 38 * max(0.2, kn), INK, FONT_TITLE)
        ptext(ctx, gx, gy + 170, "1965", 60, GOLD, FONT_TITLE, shadow=(3, 4, (20, 10, 4)))
    return fin(ctx, t, warm=0.02)


# ═══════════════ C1–C3: 1977 → Lucas'ın ilhamları → Dune yok ═══════════════
def scene_influences(t):
    ctx = new(t)
    desk(ctx, "cool", t)
    kc = ease_out(prog(t, st("C1"), st("C1") + 0.5), 3)
    ky = ease_io(prog(t, st("C2") - 0.1, st("C2") + 0.5))
    my = lerp(640, 445, ky)
    ms = lerp(1.0, 0.5, ky)
    if kc > 0:
        marquee(ctx, 540, my + (1 - kc) * -500, 820 * ms, 330 * ms, "STAR WARS", "1977", t)
    cards = [("JOSEPH CAMPBELL", "Bin Yüzlü Kahraman (kitap)", Hx("#B3473E"), icon_book, wt("C2", 5)),
             ("KUROSAWA", "Gizli Kale (film, 1958)", Hx("#3F6EA8"), icon_hat, wt("C2", 9)),
             ("FLASH GORDON", "eski film dizileri", Hx("#C28A2E"), icon_rocket, wt("C2", 13))]
    for i, (hd, sb, col, ic, ts) in enumerate(cards):
        sl = slide_in(t, ts - 0.05, 0.5)
        if sl >= 0.999:
            continue
        y0 = 548 + i * 158
        info_card(ctx, 90 + sl * 1000, y0, 990 + sl * 1000, y0 + 140, hd, sb, col, ic)
    # 4. kart: Dune yok
    y0 = 1022
    ks = ease_out(prog(t, st("C3"), st("C3") + 0.4))
    if ks > 0:
        x0, x1 = 90, 600
        xm = (x0 + x1) / 2
        ctx.line([(x0, y0), (x1, y0), (x1, y0 + 140), (x0, y0 + 140), (x0, y0)], 4, CREAM, 0.6 * ks, cap=False)
        ptext(ctx, xm, y0 + 70, "?", 100, CREAM, FONT_TITLE) if t < wt("C3", 1) else None
        kd = pop_k(t, wt("C3", 1), 0.35)
        if kd > 0:
            ptext(ctx, xm, y0 + 70, "DUNE", 96 * kd, Hx("#FFC47A"), FONT_TITLE, shadow=(3, 4, (0, 0, 0)))
        kx = ease_out(prog(t, wt("C3", 2), wt("C3", 2) + 0.3))
        if kx > 0:
            ctx.line([(x0 + 40, y0 + 18), (lerp(x0 + 40, x1 - 40, kx), lerp(y0 + 18, y0 + 122, kx))], 10, RED, 1.0)
            ctx.line([(x1 - 40, y0 + 18), (lerp(x1 - 40, x0 + 40, kx), lerp(y0 + 18, y0 + 122, kx))], 10, RED, 1.0)
    kst = pop_k(t, wt("C3", 8), 0.3, 1.6)
    if kst > 0:
        stamp(ctx, 800, 1022 + 70, "AÇIKÇA\nKABUL ETMEDİ", 38, RED, -7.0, kst)
    return fin(ctx, t)


def _funcs():
    from scenes2 import (scene_stage, scene_news, scene_tally, scene_lucas, scene_tree, scene_warn, scene_door, scene_chart, scene_quote, scene_verdict)
    return [scene_hook, scene_timeline, scene_question, scene_oregon, scene_book, scene_influences, scene_stage, scene_news, scene_tally,
            scene_lucas, scene_tree, scene_warn, scene_door, scene_chart, scene_quote, scene_verdict]


_F = None


def render_group(g, t):
    global _F
    if _F is None:
        _F = _funcs()
    return _F[g](t)
