"""Dune × Star Wars — ikinci yarı sahneler: karşılaştırma sahnesi, belgeler, hüküm."""
import math

from PIL import Image

from scenes import *  # noqa
from scenes import hook_world, title_lines

# ═══════════════ D0–D5: iki panelli karşılaştırma sahnesi ═══════════════
PW, PH = 960, 410
PXL = 60
PYD, PYS = 330, 790
LABELS = {1: ("ARRAKİS", "TATOOINE"), 2: ("FREMEN · SPICE HARVESTER", "JAWA · SANDCRAWLER"), 3: ("KUM KURDU", "SARLACC"),
          4: ("SPICE (BAHARAT)", "“AURA SPICE” · İLK TASLAK"), 5: ("İMPARATOR · UZAY LONCASI", "İMPARATOR · TİCARET FED.")}


def _pop_time(k):
    idx = {1: 8, 2: 10, 3: 4, 4: 8, 5: 9}[k]
    return we(f"D{k}", idx)


def _reveals(k):
    """(a_dune, a_sw, b_extra) zamanları"""
    return {1: (wt("D1", 6), wt("D1", 8), wt("D1", 8)),
            2: (wt("D2", 3), wt("D2", 5), wt("D2", 8)),
            3: (wt("D3", 2), wt("D3", 3), wt("D3", 3)),
            4: (wt("D4", 1), wt("D4", 2), wt("D4", 6)),
            5: (wt("D5", 2), wt("D5", 4), wt("D5", 4))}[k]


def _item_of(t):
    k = 0
    for i in range(1, 6):
        if t >= st(f"D{i}") - 0.05:
            k = i
    return k


def panel_img(side, k, t, ua, ub):
    P = PAL["dune"] if side == "D" else PAL["sw"]
    p = Patch(PW, PH)
    p.vgrad(0, 0, PW, PH, P["sky"])
    if side == "S":
        stars(p, 36, 5 + k, 0, 200, 0.9, t)
    cols = (Hx("#E9A25B"), Hx("#D9803F"), Hx("#B9602E"), Hx("#E39A52"), Hx("#C46F36"))
    ground = 300
    # ---- gökyüzü nesneleri (kumullardan önce) ----
    if k == 1 and ua > 0:
        if side == "D":
            planet(p, 520, 140 - (1 - ua) * 260, 118, cols, ph=t * 0.03, halo=Hx("#FFC47A"))
            p.circ(790, 62 - (1 - ua) * 200, 16, Hx("#FFF3D6"))
            p.circ(835, 108 - (1 - ua) * 200, 10, Hx("#FFF3D6"))
        else:
            sun(p, 380, 180 + (1 - ua) * 240, 66, P)
            sun(p, 520, 214 + (1 - ua) * 240, 38, dict(P, sun=Hx("#FFE2A8"), halo=Hx("#FF9F5A")))
    if k == 4 and side == "D" and ua > 0:
        spice(p, 480, 185, 200 * ua, t, n=170)
    if k == 5:
        if side == "D" and ub > 0:
            guild_ship(p, 700 + (1 - ub) * 500, 120, 0.9)
        if side == "S" and ub > 0:
            fed_ship(p, 700 + (1 - ub) * 500, 120, 0.9)
    # ---- kumullar ----
    n = 3 if k == 3 else 4
    dunes(p, P, t, base=ground - 40, spread=44, n=n, amp=12, k0=0.0085, speed=0.25)
    # ---- zemin nesneleri ----
    if k == 2:
        if side == "D":
            if ua > 0:
                hooded(p, 210 - (1 - ua) * 300, 336, 1.3, INK, eye=SPICE, mask=True)
            if ub > 0:
                harvester(p, 690 + (1 - ub) * 520, 342, 0.74, t)
        else:
            if ua > 0:
                hooded(p, 210 - (1 - ua) * 300, 336, 0.98, Hx("#3A2A1A"), eye=Hx("#FFB02E"), hgt=0.9)
            if ub > 0:
                sandcrawler(p, 690 + (1 - ub) * 520, 344, 0.72, t)
    if k == 3:
        if side == "D" and ua > 0:
            worm_mouth(p, 480, 250 + (1 - ua) * 170, 125, t)
            layer(p, ridge_pts(312, 10, 0.0085, 2.3), P["ridges"][4])
            kid(p, 130, 316, 0.55, INK)
        if side == "S" and ua > 0:
            sarlacc(p, 480, 300 + (1 - ua) * 70, 205 * (0.4 + 0.6 * ua), t)
            hooded(p, 130, 330, 0.7, Hx("#3A2A1A"), eye=Hx("#FFB02E"), hgt=0.9)
    if k == 4 and side == "S" and ua > 0:
        X = Xf(480, 190 + (1 - ua) * 380, 1.0, rot=-2.5)
        pshape(p, X.pts([(-280, -150), (280, -150), (280, 150), (-280, 150)]), Hx("#F3E8C8"), sh=(8, 12), sh_a=0.32, edge=0.1)
        ptext(p, *X.p(0, -112), "THE STAR WARS — ilk taslak", 32, Hx("#3A2A1A"), FONT_TYPE)
        for i in range(5):
            ln = 470 - ((i * 53) % 130)
            p.line(X.pts([(-240, -62 + i * 34), (-240 + ln, -62 + i * 34)]), 9, (110, 96, 78), 0.5, cap=False)
        kh = ease_out(prog(t, _reveals(4)[2], _reveals(4)[2] + 0.5))
        by = -62 + 5 * 34
        p.poly(X.pts([(-250, by - 20), (-250 + 500 * kh, by - 20), (-250 + 500 * kh, by + 22), (-250, by + 22)]), Hx("#FFD84A"), 0.9)
        shown = "…200 pounds of aura spice…"[: int(26 * kh)]
        ptext(p, *X.p(0, by + 2), shown, 34, Hx("#2A160E"), FONT_TYPE)
    if k == 5:
        if side == "D" and ua > 0:
            throne(p, 230 - (1 - ua) * 360, 346, 0.82, Hx("#3A2412"), glow=Hx("#FFB765"))
        if side == "S" and ua > 0:
            throne(p, 230 - (1 - ua) * 360, 346, 0.82, Hx("#10162A"), glow=Hx("#7FB8FF"))
    # ---- etiketler ----
    tagchip(p, 26, 42, "DUNE · 1965" if side == "D" else "STAR WARS · 1977", 44, col=GOLD if side == "D" else SWYEL)
    if ua > 0.3:
        lab = LABELS[k][0 if side == "D" else 1]
        tagchip(p, 26, PH - 44, lab, 44)
    elif k:
        ptext(p, PW / 2, 150, "?", 150, (255, 255, 255), FONT_TITLE)
    return p.finish()


def _slide_pair(side, k, t):
    ra = _reveals(k)
    r_a = ra[0] if side == "D" else ra[1]
    ua = ease_out(prog(t, r_a, r_a + 0.55), 3)
    ub = ease_out(prog(t, ra[2], ra[2] + 0.6), 3)
    cur = panel_img(side, k, t, ua, ub)
    tin = st(f"D{k}")
    e = prog(t, tin - 0.10, tin + 0.35)
    if k > 1 and 0 < e < 1:
        old = panel_img(side, k - 1, t, 1.0, 1.0)
        out = Image.new("RGB", (PW, PH))
        eo = ease_io(e)
        out.paste(old, (int(-PW * eo), 0))
        out.paste(cur, (int(PW * (1 - eo)), 0))
        return out
    return cur


def scene_stage(t):
    ctx = new(t)
    desk(ctx, "ink", t)
    k0 = _item_of(t)
    # D0 giriş: 5 benzerlik
    if k0 == 0:
        ki = ease_out(prog(t, st("D0"), st("D0") + 0.5), 3)
        tagchip(ctx, 540, 520, "YORUMCULARIN SAYDIĞI", 52, anchor="mm", a=ki)
        ptext(ctx, 540, 720, "5", 420 * max(0.1, ki), GOLD, FONT_TITLE, shadow=(8, 10, (20, 10, 4)))
        ptext(ctx, 540, 960, "BENZERLİK", 130, CREAM, FONT_TITLE, shadow=(5, 7, (20, 10, 4)))
        for i in range(5):
            ts = wt("D0", 2) + 0.1 * i
            kk = pop_k(t, ts, 0.3)
            if kk > 0:
                pcirc(ctx, 140 + i * 200, 1130, 52 * kk, CREAM)
                ptext(ctx, 140 + i * 200, 1132, str(i + 1), 62 * kk, INK, FONT_TITLE)
    img = ctx.finish()
    if k0 >= 1:
        a_in = ease_out(prog(t, st("D1") - 0.2, st("D1") + 0.35), 3)
        pd = _slide_pair("D", k0, t)
        ps = _slide_pair("S", k0, t)
        paste_panel(img, pd, PXL - (1 - a_in) * 1100, PYD, 28)
        paste_panel(img, ps, PXL + (1 - a_in) * 1100, PYS, 28)
        # "=" rozeti
        pk = pop_k(t, _pop_time(k0), 0.35, 2.4)
        if pk > 0:
            b = Patch(120, 120, bg=CREAM)
            b.text(60, 62, "=", 110, INK, path=FONT_TITLE)
            b.circ(60, 60, 54, CREAM)
            b.text(60, 62, "=", 100, RED, path=FONT_TITLE)
            bi = b.finish()
            sz = int(120 * pk)
            if sz > 10:
                paste_panel(img, bi.resize((sz, sz), Image.LANCZOS), 540 - sz // 2, 765 - sz // 2, r=sz // 2, shadow=True)
    return paper_post(img, t)


# ═══════════════ E1: gazete kupürü — Herbert 1977 ═══════════════
QUOTE_LINES = ["“Dava açmamak için", "elimden geleni", "yapacağım.”"]


def _typed_lines(lines, k):
    tot = sum(len(s) for s in lines)
    n = int(tot * clamp(k))
    out = []
    for s in lines:
        out.append(s[:max(0, n)])
        n -= len(s)
    return out


def scene_news(t):
    ctx = new(t)
    desk(ctx, "warm", t)
    sl = slide_in(t, st("E1"), 0.5)
    k = prog(t, wt("E1", 9), we("E1", 14))
    cx, cy, w, h = 540, 790 + sl * 900, 880, 840
    X = Xf(cx, cy, 1.0, rot=-1.5)
    hw, hh = w / 2, h / 2
    pshape(ctx, X.pts([(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]), Hx("#EFE3C0"), sh=(12, 16), sh_a=0.34, edge=0.1)
    ptext(ctx, *X.p(0, -hh + 56), "GAZETE · 1977", 56, INK, FONT_SERIF)
    ctx.line(X.pts([(-hw + 30, -hh + 98), (hw - 30, -hh + 98)]), 4, INK, 0.8)
    ctx.line(X.pts([(-hw + 30, -hh + 108), (hw - 30, -hh + 108)]), 1.6, INK, 0.7)
    ptext(ctx, *X.p(0, -hh + 160), "Dune yazarı Frank Herbert", 46, Hx("#4A3626"), FONT_SERIF)
    for col in range(2):
        x0 = -hw + 34 + col * (w / 2 - 6)
        for i in range(6):
            yy = -hh + 218 + i * 34
            ln = (w / 2 - 70) * (0.62 + 0.38 * rng_hash(i, col, 5))
            ctx.line(X.pts([(x0, yy), (x0 + ln, yy)]), 8, (120, 104, 84), 0.45, cap=False)
    by0, by1 = hh - 480, hh - 140
    kb = ease_out(prog(t, wt("E1", 8), wt("E1", 9)))
    ctx.poly(X.pts([(-hw + 24, by0), (-hw + 24 + (w - 48) * kb, by0), (-hw + 24 + (w - 48) * kb, by1), (-hw + 24, by1)]), Hx("#FFD84A"), 0.88)
    lines = _typed_lines(QUOTE_LINES, k)
    for i, ln in enumerate(lines):
        ptext(ctx, *X.p(0, (by0 + by1) / 2 + (i - 1) * 76), ln, 58, INK, FONT_SERIF)
    ptext(ctx, *X.p(0, hh - 62), "1977 · aktarılan söz", 44, Hx("#6A4E36"), FONT_BOLD)
    kc = pop_k(t, wt("E1", 4), 0.3, 1.8)
    if kc > 0:
        stamp(ctx, 690, 690, "ANLATILDIĞINA GÖRE", 40, Hx("#8A5A1E"), -6.0, kc)
    return fin(ctx, t, warm=0.02)


# ═══════════════ E2: tahta — 16 özdeşlik noktası ═══════════════
def _tally16(ctx, x, y, k, sp=30, size=112):
    shown = int(16 * clamp(k))
    for g in range(4):
        gx = x + (g % 2) * (4 * sp + 96)
        gy = y + (g // 2) * (size + 54)
        cnt = min(5, shown - g * 5)
        for i in range(max(0, min(4, cnt))):
            wob = (rng_hash(g, i, 2) - 0.5) * 4
            ctx.line([(gx + i * sp + wob, gy), (gx + i * sp - wob, gy + size)], 8, (246, 242, 226), 0.95)
        if cnt >= 5:
            ctx.line([(gx - 16, gy + size * 0.82), (gx + 3 * sp + 16, gy + size * 0.18)], 8, (246, 242, 226), 0.95)


def scene_tally(t):
    ctx = new(t)
    desk(ctx, "warm", t)
    kb = ease_out(prog(t, st("E2"), st("E2") + 0.5), 3)
    cx, cy = 540, 740 - (1 - kb) * 900
    chalkboard(ctx, cx, cy, 860, 560)
    CH, BOARD = (246, 242, 226), Hx("#1F3B33")
    # başlık: yıl söylenirken tebeşirle yazılır
    ttl = "UCLA · 1985"
    nT = int(round(len(ttl) * ease_out(prog(t, st("E2") + 0.55, wt("E2", 1) - 0.25), 1.2)))
    if nT > 0:
        x0 = cx - font(FONT_TITLE, 66).getlength(ttl) / 2
        ptext(ctx, x0, cy - 214, ttl[:nT], 66, CH, FONT_TITLE, anchor="lm")
    # "iki eser" karalaması: DUNE ⟷ STAR WARS (sayım başlamadan tahtadan silinir)
    fo = 1 - ease_out(prog(t, wt("E2", 5) - 0.5, wt("E2", 5) - 0.08))
    if fo > 0.01:
        cc = mix(BOARD, CH, fo)
        yy = cy - 30
        k1 = pop_k(t, wt("E2", 2) - 0.05, 0.35, 1.8)
        k2 = pop_k(t, wt("E2", 3) - 0.05, 0.35, 1.8)
        if k1 > 0:
            ptext(ctx, cx - 300, yy, "DUNE", 60 * min(1.15, k1), cc, FONT_TITLE)
        if k2 > 0:
            ptext(ctx, cx + 240, yy, "STAR WARS", 60 * min(1.15, k2), cc, FONT_TITLE)
        ka = ease_out(prog(t, wt("E2", 4) - 0.05, wt("E2", 4) + 0.4), 2)
        if ka > 0.02:
            ax0, ax1 = cx - 185, cx + 20
            xe = lerp(ax0, ax1, ka)
            ctx.line([(ax0, yy), (xe, yy)], 7, cc, 1.0)
            if ka > 0.15:
                ctx.line([(ax0 + 26, yy - 22), (ax0, yy), (ax0 + 26, yy + 22)], 7, cc, 1.0)
            if ka > 0.92:
                ctx.line([(ax1 - 26, yy - 22), (ax1, yy), (ax1 - 26, yy + 22)], 7, cc, 1.0)
    k = ease_out(prog(t, wt("E2", 5) - 0.05, we("E2", 8)), 1.0)
    _tally16(ctx, cx - 360, cy - 150, k)
    k16 = pop_k(t, we("E2", 8) - 0.1, 0.4, 2.2)
    if k16 > 0:
        ptext(ctx, cx + 250, cy + 20, "16", 230 * k16, GOLD, FONT_TITLE, shadow=(5, 7, (10, 20, 16)))
    kq = pop_k(t, wt("E2", 11) - 0.05, 0.4, 1.8)
    if kq > 0:
        by = 1135
        prect(ctx, 80, by - 62, 1000, by + 62, CREAM, sh=(8, 12), sh_a=0.3, edge=0.1)
        ptext(ctx, 540, by, "“Kopyaladılar demiyorum.”", 56 * min(1.0, kq), INK, FONT_SERIF)
    return fin(ctx, t, warm=0.02)


# ═══════════════ E3: Lucas'ın cevabı — ikisinde de çöl ═══════════════
def scene_lucas(t):
    ctx = new(t)
    desk(ctx, "cool", t)
    tagchip(ctx, 540, 400, "LUCAS · 1977 (AKTARILAN SÖZ)", 48, anchor="mm", a=ease_out(prog(t, st("E3"), st("E3") + 0.4)))
    # yönetmen sandalyesi
    kc = ease_out(prog(t, st("E3") + 0.1, st("E3") + 0.6), 3)
    if kc > 0:
        director_chair(ctx, 215, 1130 + (1 - kc) * 500, 1.15)
        ptext(ctx, 215, 1160 + (1 - kc) * 500, "LUCAS", 44, CREAM, FONT_BOLD)
    # konuşma balonu
    kb = pop_k(t, wt("E3", 3) - 0.1, 0.4, 1.8)
    if kb > 0:
        bx, by = 600, 650
        pshape(ctx, [(bx - 400, by - 170), (bx + 400, by - 170), (bx + 400, by + 170), (bx - 400, by + 170)], CREAM, sh=(10, 14), sh_a=0.32)
        pshape(ctx, [(bx - 360, by + 160), (bx - 300, by + 160), (bx - 400, by + 250)], CREAM, sh=(6, 10), sh_a=0.0, edge=0.0)
        k = prog(t, wt("E3", 4), we("E3", 10))
        lines = _typed_lines(["“Tek ortak nokta:", "ikisinde de çöl.”"], k)
        for i, ln in enumerate(lines):
            ptext(ctx, bx, by - 40 + i * 92, ln, 66, INK, FONT_SERIF)
    # kitap + klaket + ÇÖL
    kk = pop_k(t, wt("E3", 7) - 0.05, 0.45)
    if kk > 0:
        book(ctx, 520, 1010 + (1 - kk) * 400, 130, 185, "DUNE", "", t=t)
        clapper(ctx, 800, 1010 + (1 - kk) * 400, 220, 150, "STAR WARS", "", open_deg=10)
    kd = pop_k(t, wt("E3", 9) - 0.05, 0.5, 2.0)
    if kd > 0:
        ptext(ctx, 660, 1190, "= ÇÖL", 120 * min(1.0, kd), GOLD, FONT_TITLE, shadow=(5, 7, (8, 14, 24)))
    return fin(ctx, t)


# ═══════════════ F1: ortak atalar ağacı ═══════════════
def scene_tree(t):
    ctx = new(t)
    P = PAL["oregon"]
    sky(ctx, [(0, Hx("#7FA3B8")), (0.6, Hx("#D8E4DC")), (1.0, Hx("#F3E8C8"))])
    kt = ease_io(prog(t, wt("F1", 4) - 0.1, wt("F1", 7) + 0.3))
    layer(ctx, ridge_pts(1160, 20, 0.006, 0.5), Hx("#CDB985"))
    layer(ctx, ridge_pts(1230, 16, 0.007, 2.0), Hx("#A79256"))
    kq = 1 - ease_out(prog(t, wt("F1", 4) - 0.1, wt("F1", 4) + 0.3))
    if kq > 0.02 and t > st("F1"):
        ptext(ctx, 540, 520, "KOPYA MI?", 170 * (0.6 + 0.4 * kq), INK, FONT_TITLE, shadow=(5, 7, Hx("#E9DDB8")))
    if kt > 0.02:
        tree(ctx, 540, 1070, t, kt)
        # yapraklar
        for sgn in (-1, 1):
            tx, ty = 540 + sgn * (14 + 300 * kt * 1.0), 1070 - 570 * kt
            for i in range(9):
                a = i * 0.7 + sgn
                lx, ly = tx + math.cos(a) * 70 * kt, ty + math.sin(a) * 46 * kt - 20
                pcirc(ctx, lx, ly, 34 * kt, mix(Hx("#6E9A52"), Hx("#C8A640"), (i % 3) / 3.0), sh=(4, 6), sh_a=0.2)
        # tabelalar
        ks = pop_k(t, wt("F1", 4) + 0.2, 0.4)
        if ks > 0:
            X0, Y0 = 540 - 314 * kt, 1070 - 570 * kt
            prect(ctx, X0 - 130, Y0 - 140 * ks, X0 + 130, Y0 - 140 * ks + 84, Hx("#C98A3A"), sh=(6, 9), sh_a=0.3)
            ptext(ctx, X0, Y0 - 140 * ks + 44, "DUNE", 58, CREAM, FONT_TITLE)
            X1 = 540 + 314 * kt - 34
            wsw = font(FONT_TITLE, 52).getlength("STAR WARS")
            prect(ctx, X1 - wsw / 2 - 28, Y0 - 140 * ks, X1 + wsw / 2 + 28, Y0 - 140 * ks + 84, Hx("#1E3558"), sh=(6, 9), sh_a=0.3)
            ptext(ctx, X1, Y0 - 140 * ks + 44, "STAR WARS", 52, SWYEL, FONT_TITLE)
    # kökler (karolar)
    k1 = pop_k(t, wt("F1", 8) - 0.05, 0.4)
    k2 = pop_k(t, wt("F1", 11) - 0.05, 0.4)
    for kk, x, l1, l2 in ((k1, 290, "ARABİSTANLI", "LAWRENCE"), (k2, 790, "KAHRAMAN", "MİTLERİ")):
        if kk > 0:
            ctx.line([(540, 1070), (540 + (x - 540) * 0.55, 1082), (x, 1078)], 14, Hx("#6A4328"), 1.0)
            wd = font(FONT_BOLD, 46).getlength(l1)
            prect(ctx, x - wd / 2 - 24, 1078 - 40 * kk, x + wd / 2 + 24, 1078 + 120 * kk, CREAM, sh=(5, 8), sh_a=0.3)
            ptext(ctx, x, 1078 + 20 * kk, l1, 46 * min(1, kk), INK, FONT_BOLD)
            ptext(ctx, x, 1078 + 78 * kk, l2, 46 * min(1, kk), INK, FONT_BOLD)
    return fin(ctx, t, warm=0.015)


# ═══════════════ F2: uyarı — kahramanın hatası herkesi sürükler ═══════════════
def scene_warn(t):
    ctx = new(t)
    P = PAL["dune"]
    sky(ctx, P["sky"])
    sun(ctx, 760, 700, 90, P)
    layer(ctx, ridge_pts(900, 22, 0.0052, 0.8), P["ridges"][1])
    # uçurum: sağda zemin biter
    edge_x = 830
    crack = prog(t, wt("F2", 12) - 0.1, wt("F2", 13) + 0.4)
    ground = [(-60, 1010), (edge_x - 60 * crack * 0.0, 1010), (edge_x + 10 + 14 * crack, 1040), (edge_x - 6, 1100), (edge_x - 40, 1300), (-60, 1300)]
    for gi, gcol in enumerate((Hx("#4A2415"), Hx("#33180E"), Hx("#22100A"), Hx("#150A06"))):                   # boşluk: açıktan koyuya kâğıt katmanları
        gx_l, gy_b = edge_x - 20 + gi * 58, 1500 - gi * 120
        jag = [(gx_l + 9 * math.sin(j * 2.3 + gi * 1.7), 1010 + j * (gy_b - 1010) / 7) for j in range(8)]
        ctx.poly([(gx_l, 1010), (W + 60, 1010), (W + 60, gy_b)] + jag[::-1], gcol)
        if gi:
            ctx.line(jag, 3, (0, 0, 0), 0.35, cap=False)
    pshape(ctx, ground, P["ridges"][3], sh=(0, -10), sh_a=0.25, edge=0.2)
    ctx.poly([(-60, 1110), (edge_x - 50, 1110), (edge_x - 40, 1300), (-60, 1300)], P["ridges"][4])
    # çatlaklar
    if crack > 0:
        for i, (a, b) in enumerate((((700, 1010), (760, 1060)), ((760, 1060), (740, 1100)), ((780, 1010), (815, 1070)))):
            fr_ = clamp(crack * 1.4 - i * 0.2)
            if fr_ > 0.02:
                ctx.line(cut_poly([a, b], fr_), 5, INK, 0.9)
        for i in range(6):
            u = clamp((crack - i * 0.08) * 1.6)
            if 0 < u < 1:
                ctx.circ(790 + i * 12, 1040 + u * 260, 8, P["ridges"][3])
    # kalabalık (soldan sağa uçuruma doğru) + lider
    crowd(ctx, 330, 1032, 4, 7, 1.05, INK, t, spread=66)
    kl = pop_k(t, st("F2") + 0.15, 0.5)
    hooded(ctx, 215, 1080 + (1 - kl) * 300, 2.0, INK, eye=SPICE, hgt=1.15)
    ctx.line([(277, 900), (277, 690)], 7, INK, 1.0)
    pshape(ctx, [(277, 690), (417, 710), (377, 750), (417, 790), (277, 770)], RED, sh=(4, 6), sh_a=0.25)
    # uyarı üçgeni
    kw = pop_k(t, wt("F2", 4), 0.4, 2.2)
    if kw > 0:
        cx, cy = 790, 640
        tri = [(cx, cy - 86 * kw), (cx + 80 * kw, cy + 52 * kw), (cx - 80 * kw, cy + 52 * kw)]
        pshape(ctx, tri, GOLD, sh=(5, 8), sh_a=0.3)
        ptext(ctx, cx, cy + 10, "!", 90 * kw, INK, FONT_TITLE)
        tagchip(ctx, cx, cy + 110, "UYARI", 50, col=RED, ink=CREAM, anchor="mm")
    return fin(ctx, t, warm=0.01)


# ═══════════════ G1+G2: kapı → teklif → ret → klaket (Dune 1984) ═══════════════
def scene_door(t):
    ctx = new(t)
    desk(ctx, "warm", t)
    t_clap = wt("G2", 5)
    dslide = ease_io(prog(t, t_clap - 0.5, t_clap - 0.1))
    knock = prog(t, wt("G1", 9) - 0.05, we("G1", 10) + 0.35)
    if dslide < 0.99:
        door(ctx, 540 - dslide * 1100, 770, 400, 620, "D. LYNCH", knock=knock, t=t)
    ke = ease_out(prog(t, wt("G1", 5) - 0.1, wt("G1", 5) + 0.55), 3)
    if ke > 0 and dslide < 0.99:
        envelope(ctx, 540 - dslide * 1100, 1035 + (1 - ke) * 600, 560, 330, "TEKLİF", "!", flap=1.0)
        tagchip(ctx, 540 - dslide * 1100, 1205, "JEDI’IN DÖNÜŞÜ", 44, anchor="mm", a=ke)
    kr = pop_k(t, wt("G2", 2), 0.3, 1.7)
    if kr > 0 and dslide < 0.99:
        stamp(ctx, 560 - dslide * 1100, 930, "GERİ ÇEVRİLDİ", 54, RED, -8.0, kr)
    # klaket: yukarıdan iner, çarpar
    kc = ease_out(prog(t, t_clap - 0.55, t_clap - 0.05), 3)
    if kc > 0:
        op = 28 * (1 - ease_in(prog(t, t_clap - 0.1, t_clap + 0.04), 2))
        clapper(ctx, 540, 760 - (1 - kc) * 900, 560, 380, "DUNE", "1984", open_deg=op)
        if t > t_clap:
            ptext(ctx, 540, 1060, "YÖN: DAVID LYNCH", 56, CREAM, FONT_TITLE, shadow=(4, 5, (10, 4, 2)))
    return fin(ctx, t, warm=0.02)


# ═══════════════ G3: gişe — yatırımını bile çıkaramadı ═══════════════
def scene_chart(t):
    ctx = new(t)
    desk(ctx, "warm", t)
    ptext(ctx, 540, 420, "DUNE · 1984", 90, CREAM, FONT_TITLE, shadow=(4, 6, (10, 4, 2)))
    k1 = ease_out(prog(t, wt("G3", 1) - 0.1, wt("G3", 1) + 0.7), 3)
    k2 = ease_out(prog(t, wt("G3", 2), wt("G3", 3) + 0.4), 3)
    x0 = 90
    for (y, lab, val, frac, col, k) in ((640, "BÜTÇE", "≈ 40 MİLYON $", 1.0, Hx("#C98A3A"), k1), (900, "HASILAT", "≈ 31 MİLYON $", 0.76, Hx("#B03A2E"), k2)):
        ptext(ctx, x0, y - 66, lab, 56, Hx("#F0B070"), FONT_BOLD, anchor="lm")
        prect(ctx, x0, y - 40, x0 + 880 * frac * k, y + 70, col, sh=(6, 9), sh_a=0.3, edge=0.18)
        if k > 0.6:
            ptext(ctx, x0 + 24, y + 15, val, 62, CREAM, FONT_TITLE, anchor="lm")
    kz = pop_k(t, wt("G3", 3), 0.35, 1.8)
    if kz > 0:
        stamp(ctx, 780, 1040, "ZARAR", 96, RED, -8.0, kz)
    tagchip(ctx, 540, 1170, "kaynaklara göre yaklaşık", 44, anchor="mm", a=ease_out(prog(t, st("G3") + 0.3, st("G3") + 0.7)))
    return fin(ctx, t, warm=0.02)


# ═══════════════ G4: Villeneuve alıntısı ═══════════════
def scene_quote(t):
    ctx = new(t)
    desk(ctx, "cool", t)
    kn = pop_k(t, wt("G4", 2) - 0.05, 0.4)
    if kn > 0:
        tagchip(ctx, 540, 400, "DENIS VILLENEUVE", 62, col=CREAM, anchor="mm")
    kc = pop_k(t, wt("G4", 5) - 0.05, 0.45)
    if kc > 0:
        clapper(ctx, 540, 610 + (1 - kc) * -400, 330, 225, "DUNE", "yeni film", open_deg=10)
    ks = ease_out(prog(t, wt("G4", 10) - 0.1, wt("G4", 10) + 0.5), 3)
    if ks > 0:
        qy = 960 + (1 - ks) * 700
        pshape(ctx, [(70, qy - 220), (1010, qy - 220), (1010, qy + 220), (70, qy + 220)], CREAM, sh=(12, 16), sh_a=0.34)
        ptext(ctx, 140, qy - 160, "“", 200, GOLD, FONT_SERIF)
        k = prog(t, wt("G4", 10), we("G4", 16))
        lines = _typed_lines(["Star Wars’ın ana fikirlerinin", "çoğu Dune’dan geliyor.”"], k)
        for i, ln in enumerate(lines):
            ptext(ctx, 540, qy - 30 + i * 76, ln, 58, INK, FONT_SERIF)
        ptext(ctx, 540, qy + 150, "— yönetmen, bir röportajda", 44, Hx("#6A4E36"), FONT_BOLD)
    return fin(ctx, t)


# ═══════════════ H1+H2: hüküm → kart (başa dönüş) ═══════════════
def scene_verdict(t):
    ctx = new(t)
    P = PAL["mash"]
    card_t = wt("H2", 5) - 0.15
    k_in = ease_out(prog(t, card_t, card_t + 0.6), 3)
    sky(ctx, P["sky"])
    stars(ctx, 60, 4, 0, 900, 0.9, t)
    planet(ctx, 230, 520, 128, (Hx("#E9A25B"), Hx("#D9803F"), Hx("#B9602E"), Hx("#E39A52"), Hx("#C46F36")), ph=t * 0.02, halo=Hx("#FFC47A"))
    planet(ctx, 850, 500, 102, (Hx("#E8D9A0"), Hx("#CDBB85"), Hx("#A99A63"), Hx("#E0CF98"), Hx("#BFAE78")), ph=t * 0.02, halo=Hx("#FFE9A8"))
    dunes(ctx, P, t, base=1000, spread=100, n=6, amp=26)
    # ayak izleri: Arrakis'ten Tatooine'e
    ki = prog(t, wt("H1", 6), we("H1", 8) + 0.6)
    n = int(26 * ki)
    for i in range(n):
        u = i / 25
        x = lerp(120, 960, u)
        y = 1215 + 26 * math.sin(u * 7) - 30 * u
        o = (i % 2) * 22 - 11
        ctx.ell(x, y + o, 15, 8, (255, 232, 176), 0.9)
        ctx.ell(x, y + o, 8, 4, SPICE, 0.8)
    k1 = pop_k(t, wt("H1", 5) - 0.1, 0.35, 1.8)
    if k1 > 0:
        stamp(ctx, 540, 690, "KOPYA KANITI: YOK", 60, RED, -5.0, k1)
    k2 = pop_k(t, wt("H1", 8) - 0.1, 0.35, 1.8)
    if k2 > 0:
        stamp(ctx, 540, 815, "İZLER: ÇOK", 74, Hx("#2F8FC0"), 4.0, k2)
    # H2: üç olasılık
    for i, (lab, wi) in enumerate((("TESADÜF", 1), ("İLHAM", 3), ("ORTAK KAYNAK", 6))):
        kk = pop_k(t, wt("H2", wi) - 0.05, 0.35)
        if kk > 0 and k_in < 0.5:
            tagchip(ctx, 540, 985 + i * 88, lab, 52 * kk, col=CREAM, anchor="mm")
    if k_in > 0.001:
        dy = -2300 * (1 - k_in)
        amp = prog(t, card_t + 0.6, card_t + 1.1) * (1 - prog(t, cues.FINAL_T - 0.8, cues.FINAL_T))
        c2 = Ctx()
        c2.cam(W / 2, H / 2, 1.0, (0.0, 0.0))
        hook_world(c2, 0.0, amp=amp, ts=t)
        title_lines(c2, dy=0.0)
        out = ctx.finish()
        out.paste(c2.finish(), (0, int(dy)))
        return paper_post(out, 0.0)
    return fin(ctx, t)
