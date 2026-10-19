"""c9_kinds — c9 «Defter Kapanıyor» özel çekim türleri (Parça 4 sahne yazarı). `scenes_c9.py` içinde import edilir; `@CM.ckind` ile kaydolur.

Dünya koordinatı = nötr kamerada ekran koordinatı (1920×1080). Kamera: `cam=[(çapa, look(...))]` ya da `cam=("push", …)`.
Kaynak disiplini: yüz yok (siluet/simge), şiddet yok; yağma sahnesinde figürler siluet; ekrana yalnız script/brif sözcükleri ve ekran kartı sayıları yazılır
(Londra 26.000+ £ ○, 51.533 FL ○, 15.445 FL ○; £10.500 SÖYLENMEZ/BASILMAZ).
Her tür `ovl=` (çapaya bağlı bindirme) kabul eder; ovl ışıktan SONRA çizilir.
"""
import functools
import math

import numpy as np
import skia

import cilt_medici as CM
import cilt_paper as PP
import icons
import p4_lib as L
import sk
from c8_kinds import quill_at, scribble
from cilt_medici import TH
from p4_lib import INK, P, S, SOFT, look, ov
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth



def _wood_table(f, seed=3, dark=False):
    """Üstten bakış ahşap masa: degrade + damar çizgileri + hafif vinyet (bir kez çiz)."""
    c = f.c
    base = ("#5A3A22", "#3E2814") if dark else ("#8A6240", "#6A4829")
    sh = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [C(base[0]), C(base[1])], [0, 1])
    c.drawRect(skia.Rect.MakeXYWH(-200, -200, W + 400, H + 400), skia.Paint(Shader=sh))
    rs = np.random.RandomState(seed)
    for i in range(70):
        y = rs.rand() * (H + 200) - 100
        a = 26 + rs.rand() * 34
        w = 1.0 + rs.rand() * 2.4
        col = "#2A180A" if rs.rand() < 0.65 else "#B88E5E"
        p = skia.Path()
        p.moveTo(-200, y)
        p.cubicTo(W * 0.3, y + rs.randn() * 16, W * 0.7, y + rs.randn() * 16, W + 200, y + rs.randn() * 10)
        c.drawPath(p, S(col, w, a))
    for xx in (W * 0.18, W * 0.83):          # tahta birleşimleri
        c.drawLine(xx, -50, xx + 6, H + 50, S("#241408", 3.0, 150))


# ═══════════════════════════ c9_defter: kalın defter incelir / kapanır ═══════════════════════════
def _ledger_page(c, x0, y0, w, h, side, seed, a=1.0):
    """Defter sayfası: krem zemin + cetvel çizgileri + okunmaz satırlar + kırmızı kenar çizgisi."""
    sh = skia.GradientShader.MakeLinear([(x0, 0), (x0 + w, 0)], [C("#E9DDBA" if side < 0 else "#F4EAD0"), C("#F4EAD0" if side < 0 else "#E6D9B4")], [0, 1])
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, w, h), skia.Paint(Shader=sh))
    # omurga gölgesi
    ex = x0 + w if side < 0 else x0
    sg = skia.GradientShader.MakeLinear([(ex - side * 70, 0), (ex, 0)], [C("#3A2810", 0), C("#3A2810", 80)], [0, 1])
    c.drawRect(skia.Rect.MakeXYWH(min(ex, ex - side * 70), y0, 70, h), skia.Paint(Shader=sg))
    rs = np.random.RandomState(seed)
    for i in range(14):
        yy = y0 + 70 + i * (h - 120) / 13.0
        c.drawLine(x0 + 30, yy, x0 + w - 30, yy, S("#A8B8C8", 1.1, 120))
        if rs.rand() < 0.85:
            scribble(c, x0 + 46, x0 + w - 130 - rs.rand() * 120, yy - 8, 1.0, seed=seed * 31 + i, a=150, amp=3.0)
    c.drawLine(x0 + w - 110, y0 + 40, x0 + w - 110, y0 + h - 40, S("#B8422E", 1.4, 150))
    c.drawLine(x0 + 90, y0 + 40, x0 + 90, y0 + h - 40, S("#B8422E", 1.2, 110))


@CM.ckind("c9_defter")
def k_defter(cx, phase="thin", thin_at=None, thin_dur=2.6, close_at=None, snuff_at=None, ovl=None, seed=5, **_):
    """Kalın defter (açık, iki sayfa + sayfa yığınları). phase='thin': sayfa yığınları incelir, yapraklar tek tek kalkıp toz olur ('sessizce incelmeye başlamıştı').
    phase='close': defter kapanır (sağ sayfa omurga etrafında çevrilir, tok çarpma + toz + sarsıntı); sol altta mum (snuff_at'ta söner)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    cam.begin(f)
    c = f.c
    _wood_table(f, seed, dark=not TH.day)
    t = cx.t
    tc = cx.at(close_at) if close_at is not None else 1e9
    sx_, sy_ = L_shake(t - tc - 0.42) if phase == "close" else (0.0, 0.0)
    cxs, top, bw, bh = 960.0, 190.0, 560.0, 690.0
    closing = ease_in(clamp((t - tc) / 0.34), 2.2) if phase == "close" else 0.0
    c.save()
    c.translate(sx_ + bw / 2 * (1.0 - math.cos(closing * math.pi)) / 2.0, sy_)
    # masa gölgesi
    SOFT(c, cxs, top + bh + 36, 760, 40, "#000000", 130)
    # kalınlık
    if phase == "thin":
        k = ease_io(clamp((t - (cx.at(thin_at) if thin_at is not None else 0.2)) / thin_dur), 1.4)
        T = lerp(124.0, 22.0, k)
    else:
        T = 52.0
    # kapak (deri) — alt kenarda görünen
    c.drawRoundRect(skia.Rect.MakeLTRB(cxs - bw - T - 26, top - 16, cxs + bw + T + 26, top + bh + 24), 14, 14, P("#4A2A18"))
    c.drawRoundRect(skia.Rect.MakeLTRB(cxs - bw - T - 26, top - 16, cxs + bw + T + 26, top + bh + 24), 14, 14, S("#1E1008", 3.0, 235))
    for sg in (-1, 1):
        # sayfa yığını (kenar çizgileri)
        xo = cxs + sg * bw
        n = 18
        for i in range(n):
            u = i / (n - 1)
            xx = xo + sg * (T * u)
            col = "#F2E8CC" if i % 2 == 0 else "#D9CBA2"
            c.drawRect(skia.Rect.MakeLTRB(min(xx, xx + sg * T / n), top + 6 + 8 * u, max(xx, xx + sg * T / n), top + bh - 6 - 6 * u), P(col))
        c.drawRect(skia.Rect.MakeLTRB(min(xo, xo + sg * T), top + 6, max(xo, xo + sg * T), top + bh - 6), S("#7A6840", 1.4, 160, cap=False))
    # sol sayfa
    _ledger_page(c, cxs - bw, top, bw, bh, -1, 5)
    # sağ sayfa: omurga etrafında x ölçeği 1 -> -1 (kapanış); kapanırken kitabın merkezi sahnede kalsın diye kayar
    sxp = math.cos(closing * math.pi)
    c.save()
    c.translate(cxs, 0)
    c.scale(sxp, 1.0)
    c.translate(-cxs, 0)
    if closing < 0.5:
        _ledger_page(c, cxs, top, bw, bh, 1, 8)
        if closing > 0.02:                                   # dönen sayfanın ucunda gölge
            c.drawRect(skia.Rect.MakeXYWH(cxs, top, bw, bh), P("#000000", int(70 * closing * 2)))
    else:
        c.drawRect(skia.Rect.MakeXYWH(cxs, top, bw, bh), P("#4A2A18"))
        c.drawRect(skia.Rect.MakeXYWH(cxs, top, bw, bh), S("#1E1008", 3.0, 235, cap=False))
        c.drawRect(skia.Rect.MakeXYWH(cxs + 22, top + 22, bw - 44, bh - 44), S("#C79A3C", 3.0, 220, cap=False))
        c.drawRect(skia.Rect.MakeXYWH(cxs + 38, top + 38, bw - 76, bh - 76), S("#C79A3C", 1.4, 170, cap=False))
    c.restore()
    if closing >= 0.5:
        import cilt_props as CP
        ccx = cxs + sxp * bw / 2
        CP.draw_arms(f, ccx, top + bh / 2, 300 * abs(sxp) ** 0.5 + 40, alpha=clamp((closing - 0.5) * 2.0), shadow=0.4, glow=0.0)
        for xx in (cxs + sxp * 60, cxs + sxp * (bw - 60)):
            for yy in (top + 60, top + bh - 60):
                c.drawCircle(xx, yy, 13, P("#C79A3C"))
    # yapraklar (incelme): sayfalar yığından kalkar, eğilir, toza karışır
    if phase == "thin":
        t00 = cx.at(thin_at) if thin_at is not None else 0.2
        for i in range(9):
            t0 = t00 + 0.10 + i * 0.34
            u = (t - t0) / 1.7
            if not (0 < u < 1):
                continue
            rr = np.random.RandomState(40 + i)
            lx = cxs + bw + T * 0.92
            y0 = top + 150 + rr.rand() * 330
            e = ease_in(u, 1.5)
            a_ = int(255 * (1.0 - clamp((u - 0.5) / 0.5)))
            c.save()
            c.translate(lx + 70 * e + 40 * math.sin(u * 5 + i), y0 - 300 * e)
            c.rotate(-lerp(4.0, 62.0, e) + 6 * math.sin(u * 7 + i))
            wl, hl = 300 * (1 - 0.30 * e), 380 * (1 - 0.10 * e)
            c.drawRect(skia.Rect.MakeXYWH(0, -hl / 2, wl, hl), P("#F4EAD0", a_))
            c.drawRect(skia.Rect.MakeXYWH(0, -hl / 2, wl, hl), S("#8A7848", 1.8, int(a_ * 0.8), cap=False))
            for j in range(7):
                yy_ = -hl / 2 + 44 + j * (hl - 80) / 6.0
                c.drawLine(18, yy_, wl - 18, yy_, S("#8E9AA8", 1.2, int(a_ * 0.45)))
                scribble(c, 24, wl - 60, yy_ - 6, 1.0, seed=100 + i * 9 + j, a=int(a_ * 0.55), amp=2.4)
            c.restore()
            # toz: yaprak solarken yukarı süzülür
            for j in range(7):
                ph = (u * 1.1 + j * 0.14) % 1.0
                SOFT(c, lx + 120 + j * 46 + 30 * math.sin(t * 2 + j), y0 - 200 - ph * 190, 12 + ph * 14, 12 + ph * 14, "#E8D8A8", 100 * clamp(u * 2.2) * (1 - ph))
    # mum
    if phase == "close" and snuff_at is not None:
        ts = cx.at(snuff_at)
        ks = 1.0 - ease_in(clamp((t - ts) / 0.35), 1.5)
        mx_, my_ = 300.0, 800.0
        c.drawRect(skia.Rect.MakeLTRB(mx_ - 16, my_ - 150, mx_ + 16, my_), P("#EDE2C2"))
        c.drawRect(skia.Rect.MakeLTRB(mx_ - 16, my_ - 150, mx_ + 16, my_), S("#8A7848", 1.6, 200, cap=False))
        c.drawOval(skia.Rect.MakeLTRB(mx_ - 54, my_ - 8, mx_ + 54, my_ + 18), P("#B08828"))
        L.flame(f, mx_, my_ - 152, 56, t, 3, k=ks)
        if t > ts:
            for j in range(5):
                ph = ((t - ts) * 0.5 + j * 0.2) % 1.0
                if t - ts < 2.4:
                    SOFT(c, mx_ + 8 * math.sin(t * 3 + j) + (j - 2) * 6, my_ - 160 - ph * 190, 12 + ph * 26, 16 + ph * 34, "#B9B2A4", 70 * (1 - ph) * (1 - clamp((t - ts) / 2.4)))
    # kapanış tozu
    uu = t - tc - 0.34
    if phase == "close" and 0 < uu < 1.0:
        for i in range(16):
            r3 = np.random.RandomState(900 + i)
            dd = (60 + 280 * r3.rand()) * ease_out(clamp(uu / 1.0), 2)
            sgn = 1 if i % 2 else -1
            SOFT(c, cxs + sgn * dd, top + bh - 6 - 24 * r3.rand(), 30 + 22 * uu, 20 + 12 * uu, "#CBB894", 90 * (1 - clamp(uu)))
    c.restore()
    cam.end(f)
    light = None
    if not TH.day:
        light = CM.candle_light(t, seed, base=(W * 0.5, H * 0.52), r=1500.0, sway=10.0)
    CM.finish(f, cx, motes_n=24, light=light)
    if ovl is not None:
        ovl(cx)


def L_shake(t_since, amp=9.0, tau=0.14, hz=26.0):
    if t_since < 0 or t_since > 1.0:
        return 0.0, 0.0
    e = math.exp(-t_since / tau)
    return amp * e * math.sin(t_since * hz * math.pi), amp * 0.6 * e * math.cos(t_since * hz * math.pi * 0.86)


# ═══════════════════════════ c9_sap: şap kristalleri ═══════════════════════════
@CM.ckind("c9_sap")
def k_sap(cx, ovl=None, seed=3, **_):
    """Şap (alüminyum sülfat): taş tezgâhta büyüyen saydam kristal kümesi; ışıltılar; kristaller sırayla uzar."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    # taş tezgâh
    GRAD = skia.GradientShader.MakeLinear([(0, 720), (0, 1000)], [C("#8E8A7C"), C("#5E5A4E")], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(-80, 720, W + 80, 1100), skia.Paint(Shader=GRAD))
    c.drawLine(-80, 720, W + 80, 720, S("#2A2418", 2.6, 230))
    SOFT(c, 960, 724, 620, 50, "#000000", 120)
    rs = np.random.RandomState(seed)
    items = []
    for i in range(15):
        ang = (rs.rand() - 0.5) * 120
        x = 960 + (rs.rand() - 0.5) * 720
        L_ = 190 + rs.rand() * 330 - abs(x - 960) * 0.18
        items.append((x, 722 + rs.rand() * 24, ang * (0.4 + abs(x - 960) / 600.0), max(120.0, L_), 52 + rs.rand() * 40, rs.rand()))
    items.sort(key=lambda q: q[1])
    for i, (x, y, ang, Ln, w, r_) in enumerate(items):
        u = ease_out(clamp((t - (0.15 + 0.17 * i)) / 0.9), 2)
        if u <= 0.003:
            continue
        L.crystal(c, x, y, ang, Ln * u, w * (0.4 + 0.6 * u), a=235, tint="#E4EEF0" if r_ > 0.3 else "#EFE0E4", seed=i)
    # ışıltılar
    for i in range(14):
        ph = (t * 0.7 + i * 0.37) % 1.0
        if ph < 0.35:
            r3 = np.random.RandomState(300 + i)
            gx, gy = 960 + (r3.rand() - 0.5) * 640, 400 + r3.rand() * 330
            a = math.sin(ph / 0.35 * math.pi)
            for ang in (0, 90):
                dx, dy = math.cos(math.radians(ang)) * 24 * a, math.sin(math.radians(ang)) * 24 * a
                c.drawLine(gx - dx, gy - dy, gx + dx, gy + dy, S("#FFFFFF", 2.6, int(230 * a)))
            f.circle(gx, gy, 12 * a, color="#FFFFFF", alpha=0.8 * a, blur=3)
    cam.end(f)
    CM.finish(f, cx, motes_n=26)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c9_hak: pazarlama hakkı belgesi (1466; grup mühürleri) ═══════════════════════════
@CM.ckind("c9_hak")
def k_hak(cx, ovl=None, seed=12, **_):
    """Parşömen: okunmaz satırlar yazılır; altta dört mum mühür (üçü isimsiz, biri Medici) sırayla basılır: `bir gruba` verilen hak."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    PWd, PHd = 1160, 740
    pg = PP.paper_image(PWd, PHd, seed, (238, 226, 192), "deckle", (("h", 0.5),), 44, 1.0)
    dx, dy = 960.0, 500.0
    pg.draw(f, dx, dy, rot=-0.006, shadow=0.6)
    t0 = cx.at(("c9s4", -0.1))
    xl, xr = dx - PWd / 2 + 90, dx + PWd / 2 - 90
    last = None
    for i in range(8):
        yy = dy - PHd / 2 + 120 + i * 54
        kk = clamp((t - (t0 + 0.15 + i * 0.36)) / 0.7)
        e = scribble(c, xl, xr - (0 if i % 3 else 140), yy, ease_io(kk, 1.4), seed=70 + i, a=175)
        if 0 < kk < 1:
            last = e
    if last is not None:
        quill_at(f, last[0], last[1], t=t)
    CM.flourish_rule(f, dx, dy + PHd / 2 - 188, 520, alpha=0.7, color="#7A5A2E", grow=cx.amt(("c9s4", 0.4), 0.8))
    seals = [(dx - 390, "#2F5A8A", ("c9s4", "de'", 0.0), False), (dx - 130, "#A52A1C", ("c9s4", "Piero", -0.1), True), (dx + 130, "#3E7A5A", ("c9s4", "gruba", -0.35), False), (dx + 390, "#B08828", ("c9s4", "gruba", -0.05), False)]
    for (sx, colr, an, palle) in seals:
        ks = clamp((t - cx.at(an)) / 0.45)
        if ks > 0:
            CM.wax_seal(f, sx, dy + PHd / 2 - 112, 60, colr, alpha=1.0, t=ks, palle=palle)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c9_zaman: şube ömürleri aralık çubukları (Londra 1477–78 … 1494) ═══════════════════════════
@CM.ckind("c9_zaman")
def k_zaman(cx, axis=(1466, 1496), bars=(), marks=(), shade=None, title=None, y0=330.0, row=88.0, x0=420.0, x1=1740.0, ovl=None, seed=7, ticks=5, **_):
    """Yıl ekseni + şube çubukları. bars=[dict(name, a, b, at, col, dur, flame=True)]: çubuk `at`'ta soldan uzar; bittiği yerde şube mumu SÖNER (duman). marks=[dict(year, text, at, col)];
    shade=dict(a, b, at, label) = 'fiilî çözülme' dönemi gölgesi."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="top")
    cam.begin(f)
    c = f.c
    t = cx.t
    col = TH.rule if TH.day else "#D8B25A"
    a0, a1 = axis

    def X(yr):
        return x0 + (x1 - x0) * (yr - a0) / float(a1 - a0)
    yax = y0 + max(1, len(bars)) * row + 60
    f.rrect(x0 - 330, y0 - 90, x1 - x0 + 420, yax - y0 + 190, 16, color="#EDE3C8" if TH.day else "#0A0C14", alpha=0.5)
    if shade is not None:
        ks = cx.amt(shade["at"], 1.2)
        if ks > 0.003:
            xa, xb = X(shade["a"]), X(shade["b"])
            sh = skia.GradientShader.MakeLinear([(xa, 0), (xb, 0)], [C("#A8321E", int(70 * ks)), C("#A8321E", int(14 * ks))], [0, 1])
            c.drawRect(skia.Rect.MakeLTRB(xa, y0 - 40, xa + (xb - xa) * ks, yax), skia.Paint(Shader=sh))
            if shade.get("label"):
                CM.ink(f, shade["label"], (xa + xb) / 2, y0 - 50, face="title_m", size=30, color=TH.acc if TH.day else "#F0B8A0", align="c", track=7, alpha=ks, emboss=False)
    # eksen
    kx = ease_out(cx.amt(("c9s13", -0.1) if False else 0.0, 0.7), 2)
    c.drawLine(x0, yax, x1, yax, S(col, 4.0, 240))
    yr = a0 + (-a0 % ticks)
    while yr <= a1:
        xx = X(yr)
        c.drawLine(xx, yax - 12, xx, yax + 12, S(col, 2.4, 230))
        CM.ink(f, str(yr), xx, yax + 54, face="title_m", size=26, color=TH.fg, align="c", track=3, alpha=0.95, emboss=False)
        yr += ticks
    pal = ["#C95A40", "#3E7A5A", "#233C8C", "#B08828", "#8A6A9E", "#2F7A8A"]
    for i, b in enumerate(bars):
        yy = y0 + i * row + 30
        ta = cx.at(b["at"])
        kb = ease_io(clamp((t - ta) / b.get("dur", 1.1)))
        ka = clamp((t - ta + 0.25) / 0.4)
        if ka <= 0.003:
            continue
        colb = b.get("col", pal[i % len(pal)])
        CM.ink(f, b["name"], x0 - 28, yy + 12, face="title_m", size=30, color=TH.fg, align="r", track=4, alpha=ka, emboss=False)
        xa, xb = X(b["a"]), X(b["b"])
        f.rrect(x0, yy - 14, x1 - x0, 5, 2, color="#000000", alpha=0.08 * ka)
        wbar = max(2.0, (xb - xa) * kb) if b["b"] > b["a"] else 0
        if b["b"] > b["a"]:
            L._bar = None
            f.rrect(xa + 2, yy - 4, wbar, 36, 8, color="#000000", alpha=0.20 * ka, blur=3)
            f.rrect(xa, yy - 8, wbar, 36, 8, shader=f.lin(xa, yy - 8, xa, yy + 28, [(mix(colb, "#FFFFFF", 0.25), 0.0), (colb, 0.5), (mix(colb, "#000000", 0.30), 1.0)]), alpha=ka)
            f.rrect(xa, yy - 8, wbar, 36, 8, style="stroke", sw=2.0, color="#2A1A0C", alpha=0.8 * ka)
        else:
            f.circle(xa, yy + 10, 14 * kb, color=colb, alpha=ka)
        # şube mumu: çubuğun başında yanar, sonunda söner
        if b.get("flame", True):
            kf = 1.0 - ease_in(clamp((t - (ta + b.get("dur", 1.1) - 0.1)) / 0.4), 1.5)
            fx = xa - 18
            c.drawRect(skia.Rect.MakeLTRB(fx - 7, yy + 4, fx + 7, yy + 36), P("#EDE2C2"))
            c.drawRect(skia.Rect.MakeLTRB(fx - 7, yy + 4, fx + 7, yy + 36), S("#8A7848", 1.2, 200, cap=False))
            L.flame(f, fx, yy + 4, 32, t, i * 3 + 1, k=kf * ka)
            tt = t - (ta + b.get("dur", 1.1))
            if 0 < tt < 1.8:
                for j in range(3):
                    ph = (tt * 0.6 + j * 0.3) % 1.0
                    SOFT(c, fx + 4 * math.sin(t * 3 + j), yy - ph * 52, 8 + ph * 12, 10 + ph * 18, "#B9B2A4", 80 * (1 - ph) * (1 - clamp(tt / 1.8)))
        if b.get("label") and kb > 0.95:
            CM.ink(f, b["label"], xb + 16, yy + 20, face="title_m", size=26, color=TH.fg2, align="l", track=3, alpha=ka, emboss=False)
    for m in marks:
        km = cx.amt(m["at"], 0.5)
        if km <= 0.003:
            continue
        xx = X(m["year"])
        mc = m.get("col", "#A8321E")
        c.drawLine(xx, y0 - 30, xx, yax + 8, S(mc, 4.0, int(230 * km)))
        CM.stamp(f, m["text"], xx - 190, y0 - 70 if m.get("up", True) else yax + 100, rot=-0.06, size=m.get("size", 40), alpha=1.0, t=km)
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None if TH.day else CM.candle_light(t, seed, base=(960.0, 540.0), r=1850.0, sway=10.0))
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c9_londra: kredi (IV. Edward), yıl dilimi, sayaç ═══════════════════════════
@CM.ckind("c9_londra")
def k_londra(cx, ovl=None, seed=9, **_):
    """Sol: Londra şubesi (sandık) → sağ: Kral IV. Edward (taç). Sikkeler yay çizip krala akar; yıl dilimi 1466→1471; sayaç `26.000+ STERLİN` (£10.500 YOK)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    col = TH.rule if TH.day else "#D8B25A"
    # yıl dilimi (üstte)
    ky = cx.amt(("c9s11", "1466", -0.2), 0.6)
    if ky > 0.003:
        xa, xb, yy = 420.0, 1500.0, 245.0
        c.drawLine(xa, yy, xb, yy, S(col, 4.0, int(230 * ky)))
        kp = ease_io(clamp((t - cx.at(("c9s11", "1466", 0.0))) / max(0.4, cx.at(("c9s11", "1471", 0.2)) - cx.at(("c9s11", "1466", 0.0)))))
        f.rrect(xa, yy - 9, (xb - xa) * kp, 18, 9, color=TH.acc if TH.day else "#C95A40", alpha=0.8 * ky)
        for yr, xx in ((1466, xa), (1471, xb)):
            c.drawLine(xx, yy - 16, xx, yy + 16, S(col, 3.0, int(240 * ky)))
            CM.ink(f, str(yr), xx, yy + 58, face="title", size=40, color=TH.fg, align="c", track=4, alpha=ky, emboss=False)
    # Londra şubesi (sandık) — sol
    kl = cx.amt(("c9s11", "Londra", -0.2), 0.7)
    lx, ly = 500.0, 560.0
    if kl > 0.003:
        SOFT(c, lx, ly + 150, 190, 24, "#000000", 120 * kl)
        c.drawRect(skia.Rect.MakeLTRB(lx - 130, ly, lx + 130, ly + 150), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, ly), (0, ly + 150)], [C("#8A5A30", int(255 * kl)), C("#5A3418", int(255 * kl))], [0, 1])))
        c.drawRect(skia.Rect.MakeLTRB(lx - 130, ly, lx + 130, ly + 150), S("#1E1008", 2.6, int(235 * kl), cap=False))
        for xb in (lx - 100, lx + 100):
            c.drawRect(skia.Rect.MakeLTRB(xb - 12, ly, xb + 12, ly + 150), P("#3A3C44", int(255 * kl)))
        c.drawRoundRect(skia.Rect.MakeLTRB(lx - 28, ly + 38, lx + 28, ly + 98), 8, 8, P("#B08828", int(255 * kl)))
        c.drawPath(sk.poly_path([(lx - 130, ly), (lx - 110, ly - 40), (lx + 110, ly - 40), (lx + 130, ly)]), P("#6A4020", int(255 * kl)))
        c.drawPath(sk.poly_path([(lx - 130, ly), (lx - 110, ly - 40), (lx + 110, ly - 40), (lx + 130, ly)]), S("#1E1008", 2.2, int(235 * kl)))
        nstack = max(2, int(round(9 - 7 * clamp((t - cx.at(("c9s11", "1471", 0.0))) / 8.0))))
        for sx_ in (lx + 190, lx + 262):
            L.coin_stack(c, sx_, ly + 150, nstack, r=32.0, a=int(255 * kl), ph=sx_ * 0.01)
        CM.tablet(f, lx - 150, ly + 190, 300, 64, alpha=kl, corner=8)
        CM.ink(f, "LONDRA ŞUBESİ", lx, ly + 232, face="title_m", size=28, color=TH.fg, align="c", track=5, alpha=kl, emboss=False)
    # Kral IV. Edward (taç) — sağ
    kk = cx.amt(("c9s11", "Edward'a", -0.5), 0.7)
    rx, ry = 1420.0, 540.0
    if kk > 0.003:
        icons.draw_icon(f, "crown", rx, ry, size=240 * (0.9 + 0.1 * ease_out(kk)), metal="gold", alpha=kk, glow=0.22 * kk, shadow=True)
        CM.tablet(f, rx - 190, ry + 150, 380, 64, alpha=kk, corner=8)
        CM.ink(f, "KRAL IV. EDWARD", rx, ry + 192, face="title_m", size=28, color=TH.fg, align="c", track=5, alpha=kk, emboss=False)
    # sikke akışı
    ta = cx.at(("c9s11", "kredi", -3.0))
    tb = cx.at(("c9s11", "verdi.", 0.1))
    for i in range(34):
        t0 = cx.at(("c9s11", "1471", 0.0)) - 1.0 + i * 0.16
        u = (t - t0) / 1.3
        if not (0 < u < 1):
            continue
        x = lerp(lx + 140, rx - 130, u)
        y = ly + 40 - 190 * math.sin(math.pi * u)
        c.save()
        c.translate(x, y)
        c.scale(1.0, 0.45 + 0.55 * abs(math.cos(u * 9 + i)))
        L.coin_flat(c, 0, 0, r=25, a=int(255 * min(1.0, u * 5) * (1 - clamp((u - 0.9) / 0.1))))
        c.restore()
    # sayaç
    k0 = clamp((t - cx.at(("c9s11", "yirmi", -0.15))) / 1.5)
    if k0 > 0:
        v = 26000 * ease_out(k0, 3)
        txt = CM.fmt_int(v)
        sp = CM.gilt(txt, "title", 118, 6.0) if not TH.day else CM.engraved(txt, "title", 118, 6.0, TH.fg)
        CM.draw_spr(f, sp, 930, 900, "c", alpha=smooth(k0 * 5), shadow=0.5 if not TH.day else 0.0)
        kplus = cx.amt(("c9s11", "fazla", -0.1), 0.4)
        if kplus > 0.003:
            sp2 = CM.gilt("+", "title", 118, 4.0) if not TH.day else CM.engraved("+", "title", 118, 4.0, TH.fg)
            CM.draw_spr(f, sp2, 930 + sk.text_width(txt, "title", 118, 6.0) / 2 + 52, 900, "c", alpha=kplus)
        CM.ink(f, "STERLİN", 930, 960, face="title_m", size=38, color=TH.acc if TH.day else "#E8B070", align="c", track=14, alpha=smooth(k0 * 4), emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None if TH.day else CM.candle_light(t, seed, base=(960.0, 540.0), r=1850.0, sway=10.0))
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ madalya kayıtları: Portinari, Cesur Şarl (stilize; yüz iddiası YOK) ═══════════════════════════
import medal  # noqa: E402
import medal_extra as ME  # noqa: E402
import cilt_medal as CMD  # noqa: E402

if "m_portinari" not in medal.PEOPLE:
    ME.person("m_portinari", "THOMAS · PORTINARI ·", nose=20, hook=3, brow=3, lip=2, lip2=6, chin=9, jaw=1.0, fore=2, age=0.35, jowl=0.08, neck=1.0, hair="crop",
              hat="merchant_cap", beard=None, garment="fur_gown_merchant", eye="std", brow_style="raised", scale=1.06, dy=-8)
if "m_sarl" not in medal.PEOPLE:
    ME.person("m_sarl", "KAROLVS · DVX · BVRGVNDIAE ·", nose=22, hook=2, brow=4, lip=2, lip2=4, chin=14, jaw=1.15, fore=1, age=0.4, jowl=0.1, neck=1.1, hair="bowl",
              hat="burg_bonnet", garment="fur_jacket", eye="narrow", brow_style="stern", mouth="stern", scale=0.98, dy=-12)


def _plate(f, x, y, text, alpha=1.0, size=30, w=None, track=6.0):
    wd = w if w is not None else sk.text_width(text, "title_m", size, track) + 70
    CM.tablet(f, x - wd / 2, y - (size + 40) / 2, wd, size + 40, alpha=alpha, corner=8)
    CM.ink(f, text, x, y + size * 0.36, face="title_m", size=size, color=TH.fg, align="c", track=track, alpha=alpha, emboss=False)


def _glow_ring(f, x, y, r, k, col="#FFD27A"):
    f.circle(x, y, r * 1.5, shader=f.rad(x, y, r * 1.5, [(col, 0.55, int(120 * k)), (col, 1.0, 0)]))
    f.circle(x, y, r * 1.02, style="stroke", sw=5.0, color=col, alpha=0.8 * k)


# ═══════════════════════════ c9_iki: Portinari — devir / kredi / iki efendi ═══════════════════════════
@CM.ckind("c9_iki")
def k_iki(cx, phase="kredi", ovl=None, seed=11, **_):
    """Madalya sahnesi (stilize profiller). phase='devir': Cosimo'nun mumu söner (madalya kararır), Portinari parlar, MÜDÜR/ORTAK plakaları;
    'kredi': Portinari → Cesur Şarl sikke akışı + kesikli geri ok ✗; 'iki': Portinari'yi iki ip (Medici palle, dük tacı) sırayla çeker."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="top")
    cam.begin(f)
    c = f.c
    t = cx.t
    if phase == "devir":
        xc, xp, yy, sz = 520.0, 1380.0, 470.0, 470.0
        kd = cx.amt(("c9s7", "ölünce", -0.25), 0.55)
        CMD.draw_medal_b(f, "m_cosimo", xc, yy, sz, "bronze", False, alpha=1.0, tilt=0.12 * math.sin(t * 0.7), glint=None)
        if kd > 0.003:
            f.circle(xc, yy, sz * 0.5, color="#08070C", alpha=0.30 * kd)
        # mum (Cosimo'nun): ölünce söner
        mx_, my_ = xc, 835.0
        c.drawRect(skia.Rect.MakeLTRB(mx_ - 14, my_ - 100, mx_ + 14, my_), P("#EDE2C2"))
        c.drawRect(skia.Rect.MakeLTRB(mx_ - 14, my_ - 100, mx_ + 14, my_), S("#8A7848", 1.5, 200, cap=False))
        c.drawOval(skia.Rect.MakeLTRB(mx_ - 46, my_ - 6, mx_ + 46, my_ + 16), P("#B08828"))
        L.flame(f, mx_, my_ - 102, 46, t, 5, k=1.0 - ease_in(kd, 1.2))
        tt = t - cx.at(("c9s7", "ölünce", -0.25)) - 0.5
        if 0 < tt < 2.4:
            for j in range(5):
                ph = (tt * 0.5 + j * 0.2) % 1.0
                SOFT(c, mx_ + 8 * math.sin(t * 3 + j), my_ - 112 - ph * 170, 12 + ph * 22, 16 + ph * 30, "#B9B2A4", 70 * (1 - ph) * (1 - clamp(tt / 2.4)))
        kp = cx.amt(("c9s7", "Portinari", 1, -0.25), 0.7)
        dull = 0.35 * (1.0 - kp)
        kin = cx.amt(("c9s7", 0.0), 0.6)
        if kp > 0.003:
            _glow_ring(f, xp, yy, sz * 0.5, kp)
        CMD.draw_medal_b(f, "m_portinari", xp, yy, sz * (1.0 + 0.05 * kp), "bronze", False, alpha=0.9 * kin + 0.1, tilt=-0.10 * math.sin(t * 0.8), glint=((t * 0.3) % 2.0) if kp > 0.5 and (t * 0.3) % 2.0 < 1.0 else None)
        if dull > 0.003:
            f.circle(xp, yy, sz * 0.5, color="#08070C", alpha=dull)
        kn = cx.amt(("c9s7", "Cosimo", -0.1), 0.5)
        _plate(f, xc, 140, "COSIMO", alpha=kn * (1.0 - 0.35 * kd), size=32)
        kn2 = cx.amt(("c9s7", "Portinari", 1, -0.15), 0.5)
        _plate(f, xp, 140, "PORTINARI", alpha=kn2, size=32)
    elif phase == "kredi":
        xp, xs, yy, sz = 540.0, 1380.0, 470.0, 420.0
        kin = cx.amt(("c9s8", -0.1), 0.6)
        CMD.draw_medal_b(f, "m_portinari", xp, yy, sz, "bronze", False, alpha=kin, tilt=-0.10 * math.sin(t * 0.8))
        ks = cx.amt(("c9s8", "Burgonya", -0.15), 0.7)
        if ks > 0.003:
            CMD.draw_medal_b(f, "m_sarl", xs, yy, sz * (0.92 + 0.08 * ease_out(ks)), "bronze", False, alpha=ks, tilt=0.10 * math.sin(t * 0.7 + 1.0))
            icons.draw_icon(f, "crown", xs, yy - sz * 0.5 - 52, size=96, metal="gold", alpha=ks, shadow=True)
        _plate(f, xp, 140, "PORTINARI", alpha=kin, size=32)
        _plate(f, xs, 140, "CESUR ŞARL", alpha=ks, size=32)
        # sikke akışı (Portinari -> dük)
        t0 = cx.at(("c9s8", "krediler", -0.25))
        t1 = cx.at(("c9s8", "ödenmedi.", 0.4))
        for i in range(30):
            ti = t0 + i * 0.12
            if ti > t1:
                break
            u = (t - ti) / 1.25
            if not (0 < u < 1):
                continue
            x = lerp(xp + sz * 0.45, xs - sz * 0.45, u)
            y = yy + 40 - 240 * math.sin(math.pi * u)
            c.save()
            c.translate(x, y)
            c.scale(1.0, 0.45 + 0.55 * abs(math.cos(u * 8 + i)))
            L.coin_flat(c, 0, 0, r=19, a=int(255 * min(1.0, u * 5) * (1 - clamp((u - 0.92) / 0.08))))
            c.restore()
        kb = cx.amt(("c9s8", "krediler", -0.2), 0.5)
        if kb > 0.003:
            icons.draw_icon(f, "coinbag", (xp + xs) / 2, 250, size=130 * (0.9 + 0.1 * kb), metal="gold", alpha=kb, shadow=True)
        # kesikli geri ok + ✗ (geri ödenmedi)
        kr = ease_io(clamp((t - cx.at(("c9s8", "geri", -0.1))) / 0.9))
        if kr > 0.003:
            xa, xb = xs - sz * 0.5, lerp(xs - sz * 0.5, xp + sz * 0.5, 0.55 * kr)
            yb = yy + 250
            p = skia.Path()
            p.moveTo(xa, yb)
            p.quadTo((xa + xb) / 2, yb + 70, xb, yb)
            c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7, Color=C("#A8321E"), PathEffect=skia.DashPathEffect.Make([20, 14], -t * 30), StrokeCap=skia.Paint.kRound_Cap))
        kx = cx.amt(("c9s8", "ödenmedi.", -0.1), 0.3, ease=lambda u: sk.back_out(u))
        if kx > 0.003:
            xx_, yy_ = lerp(xs - sz * 0.5, xp + sz * 0.5, 0.55), yy + 250
            s_ = 46 * kx
            c.drawLine(xx_ - s_, yy_ - s_, xx_ + s_, yy_ + s_, S("#A8321E", 14, 245))
            c.drawLine(xx_ - s_, yy_ + s_, xx_ + s_, yy_ - s_, S("#A8321E", 14, 245))
    else:  # iki efendi
        xm, ym, sz = 960.0, 640.0, 430.0
        kin = cx.amt(("c9s9", -0.1), 0.6)
        ksw = clamp((t - cx.at(("c9s9", "iki", -0.2))) / 1.0)
        amp = 0.18 + 0.82 * ksw
        u = math.sin(t * 2.3) * amp
        mx_ = xm + 150 * u
        tilt = 0.30 * u
        kl = cx.amt(("c9s9", "Medici'nin", -0.15), 0.6)
        kr = cx.amt(("c9s9", "dükün", -0.2), 0.6)
        pal = (430.0, 200.0)
        crw = (1490.0, 200.0)
        # iplikler
        for (px, py, kk, sgn) in ((pal[0], pal[1] + 56, kl, -1), (crw[0], crw[1] + 56, kr, 1)):
            if kk <= 0.003:
                continue
            ex, ey = mx_ + sgn * sz * 0.40 * math.cos(tilt), ym - sz * 0.30
            e = ease_out(kk, 2.5)
            c.drawLine(px, py, lerp(px, ex, e), lerp(py, ey, e), S("#3A2A18", 3.0, int(235 * kk)))
            c.drawLine(px, py, lerp(px, ex, e), lerp(py, ey, e), S("#E8D8A8", 1.0, int(120 * kk)))
            if e > 0.97:
                c.drawCircle(ex, ey, 7, P("#3A2A18"))
        if kl > 0.003:
            CM.mini_palle(f, pal[0], pal[1], 160 * kl, mono=False, color="#8A2018", alpha=kl)
            c.drawLine(pal[0] - 70, pal[1] + 62, pal[0] + 70, pal[1] + 62, S("#3A2A18", 4.0, int(220 * kl)))
        if kr > 0.003:
            icons.draw_icon(f, "crown", crw[0], crw[1], size=150 * (0.9 + 0.1 * kr), metal="gold", alpha=kr, shadow=True)
            c.drawLine(crw[0] - 70, crw[1] + 62, crw[0] + 70, crw[1] + 62, S("#3A2A18", 4.0, int(220 * kr)))
        CMD.draw_medal_b(f, "m_portinari", mx_, ym, sz, "bronze", False, alpha=kin, tilt=tilt)
    cam.end(f)
    light = None
    if not TH.day:
        if phase == "devir":
            kd2 = ease_io(cx.amt(("c9s7", "ölünce", -0.1), 1.6))
            light = CM.candle_light(t, seed, base=(lerp(960.0, 1380.0, kd2), 470.0), r=lerp(1750.0, 1050.0, kd2), sway=12.0)
        elif phase == "kredi":
            light = CM.candle_light(t, seed, base=(960.0, 470.0), r=1700.0, sway=12.0)
        else:
            light = CM.candle_light(t, seed, base=(960.0, 560.0), r=1500.0, sway=12.0)
    CM.finish(f, cx, motes_n=22, light=light)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c9_gul: kısmen ödendi · güller · kaynaklar uzlaşmıyor ═══════════════════════════
@CM.ckind("c9_gul")
def k_gul(cx, ovl=None, seed=13, **_):
    """c9s12: taç → sandık: birkaç sikke geri döner (kısmen); kalan sikkeler kesikli kontur; kırmızı/beyaz güller (GÜLLER SAVAŞI); iki 'KAYNAK' levhası arasında ≠."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    col = TH.rule if TH.day else "#D8B25A"
    # sol: taç ve sandık (sikke geri akışı)
    crw, chest = (420.0, 430.0), (420.0, 720.0)
    k0 = cx.amt(("c9s12", -0.2), 0.6)
    if k0 > 0.003:
        icons.draw_icon(f, "crown", crw[0], crw[1], size=190 * (0.9 + 0.1 * k0), metal="gold", alpha=k0, shadow=True, glow=0.15 * k0)
        icons.draw_icon(f, "chest", chest[0], chest[1], size=170, metal="gold", alpha=k0, shadow=True)
        CM.ink(f, "IV. EDWARD", crw[0], crw[1] - 130, face="title_m", size=28, color=TH.fg, align="c", track=6, alpha=k0, emboss=False)
    t0 = cx.at(("c9s12", "kısmı", -0.1))
    for i in range(5):
        u = (t - (t0 + i * 0.22)) / 1.0
        if not (0 < u < 1):
            continue
        x = lerp(crw[0] + 20, chest[0] + 10, u) + 30 * math.sin(math.pi * u) * (1 if i % 2 else -1)
        y = lerp(crw[1] + 70, chest[1] - 40, u) - 60 * math.sin(math.pi * u)
        c.save()
        c.translate(x, y)
        c.scale(1.0, 0.5 + 0.5 * abs(math.cos(u * 7 + i)))
        L.coin_flat(c, 0, 0, r=19, a=int(255 * min(1.0, u * 6) * (1 - clamp((u - 0.9) / 0.1))))
        c.restore()
    kok = cx.amt(("c9s12", "ödendi;", -0.1), 0.4, ease=lambda u: sk.back_out(u))
    if kok > 0.003:
        icons.draw_icon(f, "scroll", chest[0] + 150, chest[1] - 40, size=70, metal="gold", alpha=kok)
        c.drawLine(chest[0] + 118, chest[1] - 40, chest[0] + 140, chest[1] - 18, S("#3E7A5A", 10 * kok, 245))
        c.drawLine(chest[0] + 140, chest[1] - 18, chest[0] + 186, chest[1] - 72, S("#3E7A5A", 10 * kok, 245))
    # kalan: kesikli kontur sikkeler
    kr = cx.amt(("c9s12", "kalanı", -0.1), 0.6)
    for i in range(7):
        if kr <= 0.003:
            break
        xx = 280 + (i % 4) * 78
        yy = 880 - (i // 4) * 40
        pth = skia.Path()
        pth.addCircle(xx, yy, 24)
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.0, Color=C("#6A3C28", int(200 * kr)), PathEffect=skia.DashPathEffect.Make([6, 6], 0)))
    # güller
    kg = cx.amt(("c9s12", "Güller", -0.15), 0.7)
    if kg > 0.003:
        sway = math.sin(t * 1.4)
        L.rose(c, 1130 - 12 * sway, 400 + 8 * sway, 96 * (0.8 + 0.2 * kg), col="#B3301F", edge="#4A0E08", a=int(255 * kg))
        L.rose(c, 1470 + 12 * sway, 400 - 8 * sway, 96 * (0.8 + 0.2 * kg), col="#F2EBDD", edge="#8A7C66", a=int(255 * kg))
        c.drawLine(1230, 400, 1370, 400, S(col, 3.0, int(200 * kg)))
    # kalan sikke → güller oku (suçlanır)
    ka = ease_io(clamp((t - cx.at(("c9s12", "suçlanır,", -0.3))) / 1.1))
    if ka > 0.003:
        p = skia.Path()
        p.moveTo(520, 860)
        p.quadTo(800, 760, lerp(520, 1100, ka), lerp(860, 520, ka))
        c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=C("#A8321E", 230), PathEffect=skia.DashPathEffect.Make([16, 12], -t * 30), StrokeCap=skia.Paint.kRound_Cap))
        icons.draw_icon(f, "question", 800, 700, size=70 * ka, metal="gold", alpha=ka)
    # iki kaynak levhası ve ≠
    kt = cx.amt(("c9s12", "rakamlar", -0.2), 0.6)
    if kt > 0.003:
        yb = 700.0
        for xx, nm in ((1130.0, "KAYNAK"), (1480.0, "KAYNAK")):
            CM.tablet(f, xx - 130, yb - 60, 260, 120, alpha=kt, corner=10)
            icons.draw_icon(f, "book", xx, yb - 12, size=64, metal="bronze", alpha=kt)
            CM.ink(f, nm, xx, yb + 44, face="title_m", size=24, color=TH.fg, align="c", track=6, alpha=kt, emboss=False)
        kne = cx.amt(("c9s12", "kaynağa", -0.2), 0.4, ease=lambda u: sk.back_out(u))
        if kne > 0.003:
            xm = 1305.0
            s_ = 44 * kne
            c.drawLine(xm - s_, yb - 14, xm + s_, yb - 14, S("#A8321E", 11, 245))
            c.drawLine(xm - s_, yb + 18, xm + s_, yb + 18, S("#A8321E", 11, 245))
            c.drawLine(xm + s_ * 0.55, yb - 48 * kne, xm - s_ * 0.55, yb + 52 * kne, S("#A8321E", 11, 245))
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None if TH.day else CM.candle_light(t, seed, base=(960.0, 540.0), r=1850.0, sway=10.0))
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c9_cark: 'suçlu kimdi?' suçlama çarkı ═══════════════════════════
_CARK_SEG = [("AJANLAR", "#3E7A5A"), ("SASSETTİ", "#233C8C"), ("LORENZO", "#B08828"), ("PRENSLER", "#A8321E")]


def _sector(cxh, cyh, r0, r1, a0, a1):
    p = skia.Path()
    n = 18
    pts = []
    for i in range(n + 1):
        a = math.radians(lerp(a0, a1, i / n) - 90)
        pts.append((cxh + r1 * math.cos(a), cyh + r1 * math.sin(a)))
    for i in range(n, -1, -1):
        a = math.radians(lerp(a0, a1, i / n) - 90)
        pts.append((cxh + r0 * math.cos(a), cyh + r0 * math.sin(a)))
    return sk.poly_path(pts)


@CM.ckind("c9_cark")
def k_cark(cx, phase="spin", land_at=None, land_dur=2.6, ovl=None, seed=17, hub="?", agents_at=None, **_):
    """Suçlama çarkı (4 dilim: AJANLAR · SASSETTİ · LORENZO · PRENSLER). phase='spin': hızla döner (bulanık, ortada ?); 'land': yavaşlayıp AJANLAR'ın üstünde durur
    (iğneler ibreyi tıkırdatır); 'spin2': yavaşlar ama hiçbir dilimde oturmaz (kime sorduğunuza bağlı)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    hx, hy, R = 960.0, 480.0, 330.0
    if phase == "spin":
        th = 620.0 * t
        sp = 1.0
    elif phase == "land":
        tl = cx.at(land_at) if land_at is not None else cx.dur
        u = clamp(t / max(0.3, tl))
        th = -45.0 + 1260.0 * (1.0 - ease_out(u, 3.0))
        sp = 1.0 - ease_out(u, 2.0) * 0.9
    else:
        tl = cx.dur
        u = clamp(t / max(0.3, tl))
        th = -8.0 + 900.0 * (1.0 - ease_out(u, 2.2)) + 14.0 * t
        sp = 0.18 + 0.8 * (1.0 - ease_out(u, 2.2))
    # ayak / direk
    SOFT(c, hx, 905, 330, 34, "#000000", 120)
    c.drawRect(skia.Rect.MakeLTRB(hx - 26, hy, hx + 26, 890), P("#6A4A2A"))
    c.drawRect(skia.Rect.MakeLTRB(hx - 26, hy, hx + 26, 890), S("#2A1A0C", 2.6, 235, cap=False))
    c.drawPath(sk.poly_path([(hx - 190, 900), (hx - 120, 870), (hx + 120, 870), (hx + 190, 900)]), P("#5A3A1E"))
    c.drawPath(sk.poly_path([(hx - 190, 900), (hx - 120, 870), (hx + 120, 870), (hx + 190, 900)]), S("#2A1A0C", 2.6, 235))
    # dış halka
    f.circle(hx, hy, R + 38, color="#3A2410")
    f.circle(hx, hy, R + 38, style="stroke", sw=4.0, color="#1A0E06")
    f.circle(hx, hy, R + 16, color="#8A6A32")
    # dilimler
    seg_k = None
    for k, (nm, colr) in enumerate(_CARK_SEG):
        a0 = th + k * 90.0
        c.drawPath(_sector(hx, hy, 70, R, a0, a0 + 90.0), P(colr))
        c.drawPath(_sector(hx, hy, 70, R, a0, a0 + 90.0), S("#1A0E06", 3.0, 230))
        mid = a0 + 45.0
        # üstte duran dilim
        dm = ((mid + 180.0) % 360.0) - 180.0
        if abs(dm) < 45.0 and sp < 0.5:
            seg_k = k
        c.save()
        c.translate(hx, hy)
        c.rotate(mid - 90.0 + 90.0)
        c.translate(0, -R * 0.62)
        al = 1.0 if sp < 0.5 else max(0.25, 1.0 - sp * 0.75)
        sc = 1.0
        CM.ink(f, nm, 0, 12, face="title_m", size=34 if len(nm) < 8 else 30, color="#F6EAD0", align="c", track=5, alpha=al, emboss=False)
        c.restore()
    # parlama (düşen dilim)
    if phase == "land" and seg_k is not None:
        kk = clamp((t - (cx.at(land_at) if land_at is not None else cx.dur) + 0.1) / 0.5)
        if kk > 0:
            c.drawPath(_sector(hx, hy, 70, R, th + seg_k * 90.0, th + seg_k * 90.0 + 90.0), P("#FFF2C8", int(110 * kk * (0.6 + 0.4 * math.sin(t * 6)))))
    # hareket izi
    if sp > 0.35:
        for i in range(16):
            a = math.radians(i * 22.5 + th * 1.0 - 90)
            rr = R * (0.55 + 0.4 * ((i * 0.37) % 1.0))
            pth = skia.Path()
            pth.addArc(skia.Rect.MakeLTRB(hx - rr, hy - rr, hx + rr, hy + rr), math.degrees(a), -26.0 * sp)
            c.drawPath(pth, S("#FFFFFF", 3.5, int(85 * sp)))
    # iğneler (çevrede) + ibre
    npg = 24
    for i in range(npg):
        a = math.radians(i * 360.0 / npg + th - 90)
        c.drawCircle(hx + (R + 27) * math.cos(a), hy + (R + 27) * math.sin(a), 6.0, P("#E8C25A"))
        c.drawCircle(hx + (R + 27) * math.cos(a), hy + (R + 27) * math.sin(a), 6.0, S("#2A1A0C", 1.5, 220))
    ph = (th / (360.0 / npg)) % 1.0
    dev = 16.0 * (1.0 - clamp(ph / 0.45)) if sp > 0.03 else 0.0
    c.save()
    c.translate(hx, hy - R - 70)
    c.rotate(dev)
    c.drawPath(sk.poly_path([(-26, -12), (26, -12), (0, 78)]), P("#D8B25A"))
    c.drawPath(sk.poly_path([(-26, -12), (26, -12), (0, 78)]), S("#2A1A0C", 3.0, 235))
    c.drawCircle(0, -4, 8, P("#2A1A0C"))
    c.restore()
    # ajanlar (bankacı figürleri): çark AJANLAR'da dururken sağda belirir
    if agents_at is not None:
        ka_ = cx.amt(agents_at, 0.6)
        if ka_ > 0.003:
            import cilt_anim as FA
            for k_, (axx, act, pr_) in enumerate(((1450.0, "talk", None), (1630.0, "count", None), (1800.0, "idle", "sack"))):
                try:
                    if act == "idle":
                        FA.walker(f, "banker", axx, 900.0, 330.0, t, speed=0.0, dir=-1, seed=40 + k_, alpha=ka_, prop=pr_)
                    else:
                        FA.actor(f, "banker", axx, 900.0, 330.0, t - 0.2 * k_, action=act, dir=-1, seed=40 + k_, alpha=ka_)
                except Exception:
                    pass
    # göbek
    f.circle(hx, hy, 74, color="#C79A3C")
    f.circle(hx, hy, 74, style="stroke", sw=4.0, color="#2A1A0C")
    f.circle(hx, hy, 52, color="#8A6A32")
    kh = cx.amt(0.0, 0.5)
    if hub == "?":
        icons.draw_icon(f, "question", hx, hy, size=86, metal="gold", alpha=kh, shadow=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=20, light=None if TH.day else CM.candle_light(t, seed, base=(1100.0, 520.0), r=1800.0, sway=10.0))
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c9_kriz: 'genel kriz yok' (Goldthwaite) ═══════════════════════════
@CM.ckind("c9_kriz")
def k_kriz(cx, ovl=None, seed=19, **_):
    """1400–1500 ekseninde sakin dalgalı çizgi (Floransa bankacılığı); sağ uçta hayalet (kesikli) çöküş konturu 'KRİZ?'; 'görmez' anında çizgi içinden geçip ✗ konur."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="top")
    cam.begin(f)
    c = f.c
    t = cx.t
    col = TH.rule if TH.day else "#D8B25A"
    x0, x1, yax, yl = 360.0, 1560.0, 700.0, 470.0

    def X(yr):
        return x0 + (x1 - x0) * (yr - 1400) / 100.0
    f.rrect(x0 - 80, 260, x1 - x0 + 160, 520, 16, color="#EDE3C8" if TH.day else "#0A0C14", alpha=0.5)
    ka = cx.amt(("c9s18", "Goldthwaite", -0.3), 0.6)
    c.drawLine(x0, yax, x1, yax, S(col, 4.0, int(240 * ka)))
    for yr in (1400, 1425, 1450, 1475, 1500):
        xx = X(yr)
        c.drawLine(xx, yax - 12, xx, yax + 12, S(col, 2.4, int(230 * ka)))
        CM.ink(f, str(yr), xx, yax + 54, face="title_m", size=28, color=TH.fg, align="c", track=3, alpha=ka * (1.0 if yr == 1500 else 0.8), emboss=False)
    kl = ease_io(clamp((t - cx.at(("c9s18", "Goldthwaite", -0.1))) / max(0.5, cx.at(("c9s18", "Floransa'da", 0.0)) - cx.at(("c9s18", "Goldthwaite", -0.1)))), 1.2)
    # sakin çizgi
    pts = []
    n = 120
    xe = lerp(x0, x1, kl)
    for i in range(n + 1):
        x = lerp(x0, x1, i / n)
        if x > xe:
            break
        y = yl + 16 * math.sin(i * 0.31) + 9 * math.sin(i * 0.77 + 1.0)
        pts.append((x, y))
    if len(pts) > 1:
        p = skia.Path()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        c.drawPath(p, S("#2F5A8A", 7.0, 240))
        c.drawCircle(pts[-1][0], pts[-1][1], 10, P("#2F5A8A"))
    # hayalet çöküş konturu
    kg = cx.amt(("c9s18", "krizi", -0.35), 0.5)
    if kg > 0.003:
        gx = X(1488)
        gp = skia.Path()
        gp.moveTo(gx - 120, yl)
        gp.lineTo(gx - 30, yl + 12)
        gp.lineTo(gx + 20, yax - 50)
        gp.lineTo(gx + 80, yl + 110)
        gp.lineTo(gx + 170, yl + 40)
        c.drawPath(gp, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=C("#A8321E", int(200 * kg)), PathEffect=skia.DashPathEffect.Make([14, 12], -t * 28), StrokeCap=skia.Paint.kRound_Cap))
        CM.ink(f, "KRİZ?", gx + 20, yax - 70, face="title_m", size=34, color="#A8321E", align="c", track=8, alpha=kg, emboss=False)
        kx = cx.amt(("c9s18", "görmez.", -0.3), 0.35, ease=lambda u: sk.back_out(u))
        if kx > 0.003:
            s_ = 70 * kx
            c.drawLine(gx + 20 - s_, yl + 90 - s_, gx + 20 + s_, yl + 90 + s_, S("#A8321E", 15, 245))
            c.drawLine(gx + 20 - s_, yl + 90 + s_, gx + 20 + s_, yl + 90 - s_, S("#A8321E", 15, 245))
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None if TH.day else CM.candle_light(t, seed, base=(960.0, 540.0), r=1850.0, sway=10.0))
    if ovl is not None:
        ovl(cx)



# ═══════════════════════════ marionet bindirmesi: iki efendi (palle ve taç) ═══════════════════════════
def marionet(a_pal, a_crw, a_pull, attach=((698.0, 292.0), (1222.0, 292.0)), pal=(430.0, 170.0), crw=(1490.0, 170.0)):
    """Kukla iplikleri: solda Medici palle, sağda dük tacı; ipler madalyanın üst kenarına bağlı; sırayla çekerler (çekilen ip gergin, öteki sarkık)."""
    def fn(cx):
        f = cx.f
        c = f.c
        t = cx.t
        kl = cx.amt(a_pal, 0.6)
        kr = cx.amt(a_crw, 0.6)
        ksw = clamp((t - cx.at(a_pull)) / 1.0)
        u = math.sin(t * 2.3) * (0.30 + 0.70 * ksw)
        for (pp, kk, sgn, at_pt) in ((pal, kl, -1, attach[0]), (crw, kr, 1, attach[1])):
            if kk <= 0.003:
                continue
            pull = max(0.0, -u * sgn)                      # bu efendinin çektiği an
            px, py = pp[0], pp[1] - 34.0 * pull
            ex, ey = at_pt
            e = ease_out(kk, 2.5)
            sag = 70.0 * (1.0 - pull)
            qx, qy = (px + ex) / 2, (py + ey) / 2 + sag
            p = skia.Path()
            p.moveTo(px, py + 60)
            p.quadTo(lerp(px, qx, e), lerp(py + 60, qy, e), lerp(px, ex, e), lerp(py + 60, ey, e))
            sc_ = "#3A2A18" if TH.day else "#E8D8A8"
            c.drawPath(p, S("#000000", 5.0, int(90 * kk)))
            c.drawPath(p, S(sc_, 3.0, int(235 * kk)))
            if e > 0.97:
                c.drawCircle(ex, ey, 8, P(sc_))
            c.drawLine(px - 74, py + 62, px + 74, py + 62, S(sc_, 5.0, int(230 * kk)))
            if sgn < 0:
                CM.mini_palle(f, px, py, 160 * kk, mono=False, color="#8A2018", alpha=kk)
            else:
                icons.draw_icon(f, "crown", px, py, size=150 * (0.9 + 0.1 * kk), metal="gold", alpha=kk, shadow=True)
    return fn


# ═══════════════════════════ bronz heykel siluetleri (David, Judith: stilize; şiddet yok) ═══════════════════════════
def bronze_fig(c, x, y, h, kind="david", a=255, lit=1.0, t=0.0):
    """Ayakları (x,y) olan stilize bronz figür: gövde/uzuv çokgenleri + bronz degrade + sıcak kenar ışığı. lit: 0 soğuk-koyu … 1 sıcak-altın."""
    lo, hi = mix("#3A2A1A", "#7A5A2C", lit), mix("#5A4020", "#E2B25A", lit)
    edge = mix("#10161E", "#2A1608", lit)
    sh = skia.GradientShader.MakeLinear([(x - h * 0.2, y - h), (x + h * 0.2, y)], [C(hi, a), C(lo, a)], [0, 1])
    pt = skia.Paint(AntiAlias=True, Shader=sh)

    def poly(pts):
        c.drawPath(sk.poly_path([(x + px * h, y + py * h) for px, py in pts]), pt)
        c.drawPath(sk.poly_path([(x + px * h, y + py * h) for px, py in pts]), S(edge, max(1.6, h * 0.012), int(a * 0.9)))

    def limb(p0, p1, wd):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L_ = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L_ * wd / 2, dx / L_ * wd / 2
        poly([(p0[0] + nx, p0[1] + ny), (p1[0] + nx, p1[1] + ny), (p1[0] - nx, p1[1] - ny), (p0[0] - nx, p0[1] - ny)])
    if kind == "david":
        limb((-0.05, -0.46), (-0.07, 0.0), 0.075)
        limb((0.05, -0.46), (0.075, 0.0), 0.075)
        poly([(-0.10, -0.46), (0.10, -0.46), (0.078, -0.80), (-0.078, -0.80)])
        limb((-0.075, -0.78), (-0.20, -0.62), 0.04)         # kalçada el
        limb((-0.20, -0.62), (-0.095, -0.50), 0.04)
        limb((0.078, -0.78), (0.125, -0.52), 0.04)
        c.drawCircle(x, y - 0.87 * h, 0.062 * h, pt)
        c.drawCircle(x, y - 0.87 * h, 0.062 * h, S(edge, max(1.6, h * 0.012), int(a * 0.9)))
        poly([(-0.135, -0.915), (0.135, -0.915), (0.07, -0.935), (-0.07, -0.935)])       # geniş şapka kenarı
        poly([(-0.05, -0.935), (0.05, -0.935), (0.03, -0.985), (-0.03, -0.985)])
    else:
        poly([(-0.15, 0.0), (0.15, 0.0), (0.095, -0.62), (-0.095, -0.62)])
        poly([(-0.095, -0.62), (0.095, -0.62), (0.075, -0.80), (-0.075, -0.80)])
        limb((0.075, -0.78), (0.03, -0.64), 0.04)
        limb((-0.075, -0.78), (-0.03, -0.66), 0.04)
        c.drawCircle(x, y - 0.87 * h, 0.058 * h, pt)
        c.drawCircle(x, y - 0.87 * h, 0.058 * h, S(edge, max(1.6, h * 0.012), int(a * 0.9)))
        poly([(-0.07, -0.90), (0.07, -0.90), (0.10, -0.78), (-0.10, -0.78)])               # örtü
    # kenar parıltısı
    if lit > 0.2:
        c.drawLine(x - h * 0.04, y - 0.80 * h, x - h * 0.05, y - 0.50 * h, S("#FFF0C0", max(1.5, h * 0.012), int(a * 0.55 * lit)))


# ═══════════════════════════ c9_saray: Palazzo Medici (el koyma), bronzlar şehirden geçer, Palazzo Vecchio salonu ═══════════════════════════
def _sky(f, y1=900.0, top="#C8D4E0", bot="#F2D8A8", x0=-2600.0, x1=5200.0):
    sh = skia.GradientShader.MakeLinear([(0, 0), (0, y1)], [C(top), C(bot)], [0, 1])
    f.c.drawRect(skia.Rect.MakeLTRB(x0, -900, x1, y1), skia.Paint(Shader=sh))


def _ground(f, y=868.0, x0=-2600.0, x1=5200.0):
    c = f.c
    sh = skia.GradientShader.MakeLinear([(0, y), (0, y + 260)], [C("#8E7C62"), C("#5A4C3A")], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(x0, y, x1, y + 400), skia.Paint(Shader=sh))
    c.drawLine(x0, y, x1, y, S("#2A1A0C", 3.0, 220))
    rs = np.random.RandomState(4)
    for i in range(int((x1 - x0) / 46)):
        xx = x0 + i * 46 + rs.rand() * 20
        c.drawLine(xx, y + 10 + rs.rand() * 120, xx + 26 + rs.rand() * 22, y + 10 + rs.rand() * 120, S("#3A2A1A", 1.6, 70))


def _seal_band(c, x0, y0, x1, y1, k, wax=True, seed=0):
    """Kapının/penceresinin üstüne çapraz kâğıt mühür bandı + balmumu mührü (el koyma)."""
    if k <= 0.003:
        return
    xe, ye = lerp(x0, x1, k), lerp(y0, y1, k)
    c.drawLine(x0, y0, xe, ye, S("#000000", 18, int(70 * k)))
    c.drawLine(x0, y0, xe, ye, S("#EFE3C0", 16, 255))
    c.drawLine(x0, y0, xe, ye, S("#8A7848", 2.0, 220))
    if wax and k > 0.9:
        mxp, myp = (x0 + x1) / 2, (y0 + y1) / 2
        c.drawCircle(mxp, myp, 24, P("#A52A1C"))
        c.drawCircle(mxp, myp, 24, S("#4A0E08", 2.0, 230))
        c.drawCircle(mxp, myp, 12, S("#E8B0A0", 1.6, 160))


@CM.ckind("c9_saray")
def k_saray(cx, phase="el", ovl=None, seed=21, **_):
    """phase='el': Palazzo Medici cephesi — Cumhuriyet flaması iner, kapıya ve yan konutlara mühür bandı vurulur, 'EL KONDU' damgası (yağma yok);
    'tas': bronz heykeller (David, Judith) arabayla şehirden Palazzo Vecchio'ya taşınır (kamera arabayı izler: dünya x 0..3300);
    'vecchio': Palazzo Vecchio salonu — soğuk karanlık → bronzlara altın ışık (güzellik kaldı)."""
    import cilt_city as CT
    import cilt_sehir as SE
    import cilt_anim as FA
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    c = f.c
    t = cx.t
    if phase == "vecchio":
        CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
        cam.begin(f)
        # arka duvar + kemerler
        kw = cx.amt(("c9s26", "bronzları", -0.3), 1.6)
        T = CT.Tint("day")
        SE.stone_wall(c, -200, 120, 2120, 860, "#B8A27A", T, 0.0, seed, ch=62.0, bw=(110.0, 190.0), rustic=True)
        for xc_ in (360.0, 960.0, 1560.0):
            pth = SE.arch_path(xc_, 860.0, 380.0, 560.0)
            c.drawPath(pth, P("#2A2218"))
            c.drawPath(pth, S("#1A120A", 5.0, 240))
            c.drawPath(SE.arch_path(xc_, 860.0, 340.0, 520.0), P("#3E3226", 255))
        # zemin (karo)
        sh = skia.GradientShader.MakeLinear([(0, 860), (0, 1100)], [C("#6A5A44"), C("#3A2E20")], [0, 1])
        c.drawRect(skia.Rect.MakeLTRB(-200, 860, 2120, 1100), skia.Paint(Shader=sh))
        for i in range(-6, 14):
            c.drawLine(960 + i * 150, 860, 960 + i * 420, 1100, S("#2A1E12", 2.0, 90))
        c.drawLine(-200, 905, 2120, 905, S("#2A1E12", 2.0, 80))
        # kaideler + heykeller
        for xc_, kind in ((690.0, "david"), (1230.0, "judith")):
            c.drawRect(skia.Rect.MakeLTRB(xc_ - 90, 700, xc_ + 90, 868), P("#8A7860"))
            c.drawRect(skia.Rect.MakeLTRB(xc_ - 90, 700, xc_ + 90, 868), S("#2A1E12", 3.0, 235, cap=False))
            c.drawRect(skia.Rect.MakeLTRB(xc_ - 110, 684, xc_ + 110, 704), P("#A89478"))
            bronze_fig(c, xc_, 684, 430, kind, 255, lit=kw, t=t)
        # ışık huzmeleri (sıcak altın) heykellerin üstüne
        if kw > 0.003:
            for xc_ in (690.0, 1230.0):
                sh = skia.GradientShader.MakeLinear([(xc_, -50), (xc_, 700)], [C("#FFE6A0", int(150 * kw)), C("#FFE6A0", int(14 * kw))], [0, 1])
                c.drawPath(sk.poly_path([(xc_ - 60, -50), (xc_ + 60, -50), (xc_ + 190, 700), (xc_ - 190, 700)]), skia.Paint(AntiAlias=True, Shader=sh))
            for i in range(26):
                rs = np.random.RandomState(500 + i)
                xx = 690 + (i % 2) * 540 + (rs.rand() - 0.5) * 300
                yy = ((rs.rand() * 700 + t * 18 * (0.5 + rs.rand())) % 700)
                f.circle(xx, yy, 2.4 + rs.rand() * 2, color="#FFF0C0", alpha=0.55 * kw * (0.4 + 0.6 * math.sin(t * 2 + i) ** 2))
        cam.end(f)
        light = None
        if not TH.day:
            light = CM.candle_light(t, seed, base=(lerp(1700.0, 960.0, kw), 520.0), r=lerp(900.0, 1700.0, kw), sway=10.0)
        CM.finish(f, cx, motes_n=18, light=light)
        # sönük (kapanan) banka için soğuk örtü: kw küçükken ekran hafif lacivert
        if ovl is not None:
            ovl(cx)
        return
    T = CT.Tint("dusk")
    cam.begin(f)
    _sky(f, 868.0, top="#9EB0C8", bot="#F0CFA0")
    # uzak şehir silueti
    rs0 = np.random.RandomState(3)
    for i in range(34):
        xx = -2500 + i * 240 + rs0.rand() * 60
        hh = 120 + rs0.rand() * 190
        c.drawRect(skia.Rect.MakeXYWH(xx, 868 - hh - 40, 150 + rs0.rand() * 60, hh), P("#A09084", 255))
    _ground(f)
    if phase == "el":
        g = SE.palazzo_front(f, 380.0, 868.0, 1160.0, 680.0, kind="medici", door=0.0, T=T, seed=seed, shield=True, tower=False)
        SE.palazzo_front(f, -560.0, 868.0, 880.0, 560.0, kind="generic", T=T, seed=seed + 2, tower=False)
        SE.palazzo_front(f, 1600.0, 868.0, 900.0, 580.0, kind="generic", T=T, seed=seed + 3, tower=False)
        # Cumhuriyet flaması (zambak) iner
        kb = ease_out(cx.amt(("c9s22", "Cumhuriyet", -0.1), 1.0), 2.4)
        if kb > 0.003:
            bx, by0 = 1230.0, -260.0 + 540.0 * kb
            sway = math.sin(t * 2.0) * 6
            pth = sk.poly_path([(bx - 70, by0), (bx + 70, by0), (bx + 70, by0 + 330), (bx + sway, by0 + 290), (bx - 70, by0 + 330)])
            c.drawPath(pth, P("#E6DCC2"))
            c.drawPath(pth, S("#2A1A0C", 3.0, 235))
            icons.draw_icon(f, "fleur", bx, by0 + 140, size=108, metal="gold", alpha=1.0, shadow=False)
            c.drawLine(bx - 90, by0 - 6, bx + 90, by0 - 6, S("#3A2410", 8.0, 255))
        # mühür bantları: ana kapı, yan konutlar
        dr = g.get("door")
        if dr:
            dx, dyb, dw, dh = dr
            kd = ease_out(cx.amt(("c9s22", "Medici'ye", -0.1), 0.5), 2.0)
            _seal_band(c, dx - dw * 0.55, dyb - dh * 0.15, dx + dw * 0.55, dyb - dh * 0.85, kd)
            _seal_band(c, dx - dw * 0.55, dyb - dh * 0.85, dx + dw * 0.55, dyb - dh * 0.15, ease_out(cx.amt(("c9s22", "Medici'ye", 0.3), 0.5), 2.0), wax=False)
        for (xs_, an) in ((-120.0, ("c9s22", "konutlarına", -0.1)), (2050.0, ("c9s22", "konutlarına", 0.25))):
            kk = ease_out(cx.amt(an, 0.5), 2.0)
            _seal_band(c, xs_ - 80, 868 - 60, xs_ + 80, 868 - 290, kk)
        for xf, an in ((300.0, 0.0), (1480.0, 0.7)):
            SE.flag_pennant(c, xf, 220, t, L=70.0, hgt=24.0, color="#B3301F", seed=int(xf))
    else:  # tas
        T2 = CT.Tint("day")
        SE.palazzo_front(f, 40.0, 868.0, 760.0, 600.0, kind="medici", door=0.0, T=T, seed=seed, shield=True, tower=False)
        SE.palazzo_front(f, 860.0, 868.0, 640.0, 520.0, kind="generic", T=T, seed=seed + 4, tower=False)
        SE.palazzo_front(f, 1580.0, 868.0, 600.0, 560.0, kind="generic", T=T, seed=seed + 5, tower=False)
        SE.palazzo_front(f, 2300.0, 868.0, 1100.0, 640.0, kind="vecchio", T=T, seed=seed + 6, tower=True, tower_x=0.62)
        # arabanın konumu: Donatello'nun'dan taşındı'ya
        ta, tb = cx.at(("c9s22", "Donatello'nun", -0.2)), cx.at(("c9s22", "taşındı.", 0.2))
        u = ease_io(clamp((t - ta) / max(0.5, tb - ta)), 1.3)
        carx = lerp(420.0, 2380.0, u)
        gy = 868.0
        # araba: kasa, tekerlekler, yük
        for sgn, kind in ((-1, "david"), (1, "judith")):
            bronze_fig(c, carx + sgn * 62, gy - 118, 230, kind, 255, lit=0.45, t=t)
        c.drawRect(skia.Rect.MakeLTRB(carx - 150, gy - 124, carx + 150, gy - 92), P("#6A4A2A"))
        c.drawRect(skia.Rect.MakeLTRB(carx - 150, gy - 124, carx + 150, gy - 92), S("#2A1A0C", 3.0, 240, cap=False))
        for wx_ in (carx - 90, carx + 90):
            rot = (carx / 40.0) * 57.3
            c.save()
            c.translate(wx_, gy - 46)
            c.rotate(rot)
            c.drawCircle(0, 0, 50, P("#8A6A3E"))
            c.drawCircle(0, 0, 50, S("#2A1A0C", 5.0, 245))
            for k in range(6):
                a_ = k * math.pi / 3
                c.drawLine(0, 0, 46 * math.cos(a_), 46 * math.sin(a_), S("#2A1A0C", 4.0, 235))
            c.drawCircle(0, 0, 9, P("#2A1A0C"))
            c.restore()
        c.drawLine(carx - 160, gy - 108, carx - 220, gy - 90, S("#3A2410", 7.0, 245))
        spd = max(0.0, (carx - lerp(420.0, 2380.0, ease_io(clamp((t - 0.05 - ta) / max(0.5, tb - ta)), 1.3))) * -1 + 500.0)
        for k, off in enumerate((-250.0, -330.0)):
            FA.walker(f, "halk", carx + off, gy + 6 + k * 14, 214.0 - k * 8, t, speed=470.0 * (1.0 if 0.02 < u < 0.98 else 0.1), dir=1, phase=0.3 * k, seed=11 + k, prop="pole" if False else None)
        # toz
        for j in range(8):
            ph = (t * 0.9 + j * 0.13) % 1.0
            SOFT(c, carx - 110 - ph * 160, gy - 6 - ph * 28, 20 + ph * 28, 10 + ph * 12, "#C8B898", 90 * (1 - ph) * (1.0 if 0.02 < u < 0.98 else 0.0))
    cam.end(f)
    CM.finish(f, cx, motes_n=16)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c9_kesit: Palazzo Medici kesiti (alt kat kalabalık, üst kat ışıklı ve boş) ═══════════════════════════
@CM.ckind("c9_kesit")
def k_kesit(cx, ovl=None, seed=23, **_):
    """c9s23: kesit görünümü: sol-orta bina (üst kat ışıklı, boş), alt kat kemerli galeri; kalabalık siluetleri bahçe kapısından sağdaki bahçeye dolar (yağma ayrıntısı YOK)."""
    import cilt_sehir as SE
    import cilt_anim as FA
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    cam.begin(f)
    c = f.c
    t = cx.t
    _sky(f, 868.0, top="#7E8FAE", bot="#D8B890")
    gy = 868.0
    bx0, bx1, yf, yt = 200.0, 1320.0, 570.0, 250.0
    # çatı
    c.drawPath(sk.poly_path([(bx0 - 30, yt), (bx1 + 30, yt), (bx1 + 10, yt - 46), (bx0 - 10, yt - 46)]), P("#8A4A2C"))
    c.drawPath(sk.poly_path([(bx0 - 30, yt), (bx1 + 30, yt), (bx1 + 10, yt - 46), (bx0 - 10, yt - 46)]), S("#2A1A0C", 3.0, 240))
    # üst kat (ışıklı, boş)
    c.drawRect(skia.Rect.MakeLTRB(bx0, yt, bx1, yf), P("#EAD5A4"))
    sh = skia.GradientShader.MakeRadial((760, 400), 520, [C("#FFE9B0", 200), C("#FFE9B0", 0)], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(bx0, yt, bx1, yf), skia.Paint(Shader=sh))
    for wx_ in (340.0, 560.0, 780.0, 1000.0, 1200.0):
        c.drawPath(SE.arch_path(wx_, yf - 70, 90.0, 150.0), P("#FFEBB8"))
        c.drawPath(SE.arch_path(wx_, yf - 70, 90.0, 150.0), S("#6A4A2A", 3.0, 235))
    # boş mobilya
    c.drawRect(skia.Rect.MakeLTRB(540, yf - 96, 900, yf - 76), P("#6A4A2A"))
    c.drawRect(skia.Rect.MakeLTRB(560, yf - 76, 576, yf), P("#4A321A"))
    c.drawRect(skia.Rect.MakeLTRB(864, yf - 76, 880, yf), P("#4A321A"))
    for chx in (470.0, 960.0, 1090.0):
        c.drawRect(skia.Rect.MakeLTRB(chx - 28, yf - 70, chx + 28, yf - 56), P("#5A3A1E"))
        c.drawRect(skia.Rect.MakeLTRB(chx - 28, yf - 130, chx - 18, yf - 56), P("#5A3A1E"))
        c.drawRect(skia.Rect.MakeLTRB(chx + 18, yf - 56, chx + 28, yf), P("#5A3A1E"))
        c.drawRect(skia.Rect.MakeLTRB(chx - 28, yf - 56, chx - 18, yf), P("#5A3A1E"))
    # avize (mumlar) — ışık
    c.drawLine(760, yt, 760, yt + 70, S("#2A1A0C", 3.0, 240))
    c.drawOval(skia.Rect.MakeLTRB(710, yt + 66, 810, yt + 88), P("#B08828"))
    for ci in (722, 760, 798):
        c.drawRect(skia.Rect.MakeLTRB(ci - 3, yt + 40, ci + 3, yt + 68), P("#EDE2C2"))
        L.flame(f, ci, yt + 40, 14, t, ci, k=1.0)
    # ara kat
    c.drawRect(skia.Rect.MakeLTRB(bx0 - 14, yf, bx1 + 14, yf + 26), P("#6A5A44"))
    c.drawRect(skia.Rect.MakeLTRB(bx0 - 14, yf, bx1 + 14, yf + 26), S("#2A1A0C", 3.0, 240, cap=False))
    # alt kat (loş galeri)
    c.drawRect(skia.Rect.MakeLTRB(bx0, yf + 26, bx1, gy), P("#4A3C2C"))
    for ax_ in (330.0, 560.0, 790.0, 1020.0, 1230.0):
        c.drawPath(SE.arch_path(ax_, gy, 170.0, 220.0), P("#2A2016"))
        c.drawPath(SE.arch_path(ax_, gy, 170.0, 220.0), S("#1A120A", 3.0, 240))
    # bahçe kapısı + bahçe
    c.drawRect(skia.Rect.MakeLTRB(bx1, yf + 60, 2100, gy), P("#9AA878"))
    c.drawRect(skia.Rect.MakeLTRB(bx1 + 40, 420, 2100, gy - 30), P("#7C9A6A"))
    for tx_, th_ in ((1480.0, 360.0), (1700.0, 420.0), (1900.0, 380.0)):
        c.drawRect(skia.Rect.MakeLTRB(tx_ - 12, gy - 40 - th_ * 0.45, tx_ + 12, gy - 40), P("#5A3A1E"))
        c.drawCircle(tx_, gy - 40 - th_ * 0.6, th_ * 0.34, P("#3E6A3E"))
        c.drawCircle(tx_, gy - 40 - th_ * 0.6, th_ * 0.34, S("#1A3A1A", 3.0, 230))
    c.drawOval(skia.Rect.MakeLTRB(1600, gy - 70, 1800, gy - 40), P("#8EA8B8"))
    c.drawRect(skia.Rect.MakeLTRB(1692, gy - 150, 1708, gy - 56), P("#8A7A62"))
    _ground(f, y=gy)
    # kalabalık: alt kattan bahçeye (siluet)
    cf = SE.dark_cf("#1A1410")
    t0 = cx.at(("c9s23", "Kalabalık", -0.2))
    k = clamp((t - t0) / 1.0)
    if k > 0.003:
        FA.crowd(f, t, (260, 800, 1980, 870), 26, seed=7, mode="march", dir=1, h=(150, 205), speed=150.0, cf=cf, alpha=k, wave=0.4)
    # pencerelerden dışarı sızan sıcak ışık (üst kat boş)
    cam.end(f)
    CM.finish(f, cx, motes_n=16)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c9_sapel: Santa Trinita — Sassetti'nin şapeli (giornata: sıva parçaları sırayla) ═══════════════════════════
@CM.ckind("c9_sapel")
def k_sapel(cx, ovl=None, seed=25, **_):
    """c9s20: şapel nişi; iskelede ressam sıva sürer (giornata: dokuz sıva parçası sırayla boyanır); köşede incelen defter + kısalan mum (ironi: YORUM)."""
    import cilt_sehir as SE
    import cilt_anim as FA
    import cilt_city as CT
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    T = CT.Tint("day")
    gy = 872.0
    # yan duvar taş
    SE.stone_wall(c, -300, 60, 2220, gy, "#B6A482", T, 0.0, seed, ch=58.0, bw=(100.0, 180.0), rustic=True)
    # niş: yuvarlak kemerli girinti
    ax, aw, ah = 1010.0, 820.0, 800.0
    arch = SE.arch_path(ax, gy - 80, aw, ah)
    c.drawPath(arch, P("#D9CBA6"))
    c.drawPath(arch, S("#2A1A0C", 7.0, 245))
    # giornata parçaları (nişin içi)
    x0, x1, y0, y1 = ax - aw / 2, ax + aw / 2, gy - 80 - ah, gy - 80
    cols_w = [(x1 - x0) / 3.0] * 3
    rows_h = [(y1 - y0) * 0.30, (y1 - y0) * 0.36, (y1 - y0) * 0.34]
    pigm = ["#2F5A8A", "#B89A44", "#2F5A8A", "#A8503A", "#D9B060", "#3E7A5A", "#7A5A9E", "#C79A3C", "#A8503A"]
    tstart = cx.at(("c9s20", "Sassetti", -0.35))
    c.save()
    c.clipPath(arch)
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), P("#CDBF98"))                      # arriccio (çıplak)
    n = 0
    yy = y0
    for r_, hh in enumerate(rows_h):
        xx = x0
        for c_, ww in enumerate(cols_w):
            ts = tstart + n * 0.62
            kp = clamp((t - ts) / 0.45)                                              # sıva
            kc = clamp((t - ts - 0.5) / 0.9)                                         # pigment
            if kp > 0:
                jit = 8 * math.sin(n * 2.3)
                pr = skia.Rect.MakeLTRB(xx + 2 + jit * 0.2, yy + 2, xx + ww * kp - 2, yy + hh - 2)
                c.drawRect(pr, P("#EBDDBA"))
                if kc > 0:
                    col = pigm[n % len(pigm)]
                    g2 = skia.GradientShader.MakeLinear([(xx, yy), (xx, yy + hh)], [C(mix(col, "#FFFFFF", 0.25), int(235 * kc)), C(col, int(235 * kc))], [0, 1])
                    c.drawRect(pr, skia.Paint(Shader=g2))
                    # sade fresk çizgileri: kemer, hale, yıldız
                    cxx, cyy = xx + ww / 2, yy + hh / 2
                    if n % 3 == 0:
                        c.drawCircle(cxx, cyy, min(ww, hh) * 0.20, S("#F2D78A", 5.0, int(230 * kc)))
                    elif n % 3 == 1:
                        c.drawPath(SE.arch_path(cxx, yy + hh - 14, ww * 0.5, hh * 0.62), S("#2A1A0C", 4.0, int(200 * kc)))
                    else:
                        for kk in range(5):
                            a_ = kk * 2 * math.pi / 5 - math.pi / 2
                            c.drawLine(cxx, cyy, cxx + math.cos(a_) * ww * 0.18, cyy + math.sin(a_) * ww * 0.18, S("#F2D78A", 4.0, int(220 * kc)))
                c.drawRect(pr, S("#8A7A5A", 2.0, int(200 * kp), cap=False))
            xx += ww
            n += 1
        yy += hh
    c.restore()
    c.drawPath(arch, S("#2A1A0C", 7.0, 245))
    # sunak masası
    c.drawRect(skia.Rect.MakeLTRB(ax - 360, gy - 96, ax + 360, gy - 60), P("#8A6A3E"))
    c.drawRect(skia.Rect.MakeLTRB(ax - 360, gy - 96, ax + 360, gy - 60), S("#2A1A0C", 3.0, 240, cap=False))
    c.drawRect(skia.Rect.MakeLTRB(ax - 330, gy - 60, ax + 330, gy), P("#6A4A2A"))
    # zemin
    sh = skia.GradientShader.MakeLinear([(0, gy), (0, 1100)], [C("#7A6A52"), C("#3E3222")], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(-300, gy, 2220, 1100), skia.Paint(Shader=sh))
    c.drawLine(-300, gy, 2220, gy, S("#2A1A0C", 3.0, 230))
    # iskele
    for px_ in (330.0, 620.0):
        c.drawRect(skia.Rect.MakeLTRB(px_ - 9, 180, px_ + 9, gy + 40), P("#6A4A2A"))
        c.drawRect(skia.Rect.MakeLTRB(px_ - 9, 180, px_ + 9, gy + 40), S("#2A1A0C", 2.0, 235, cap=False))
    for yb_ in (640.0, 360.0):
        c.drawRect(skia.Rect.MakeLTRB(280, yb_, 700, yb_ + 20), P("#8A6A3E"))
        c.drawRect(skia.Rect.MakeLTRB(280, yb_, 700, yb_ + 20), S("#2A1A0C", 2.4, 235, cap=False))
    c.drawLine(330, 640, 620, 360, S("#4A321A", 7.0, 230))
    c.drawLine(330, 360, 620, 640, S("#4A321A", 7.0, 230))
    # ressam (iskelede sıva sürer)
    FA.actor(f, "halk", 520.0, 640.0, 250.0, t, action="work", dir=1, seed=5, mode="lay", prop="trowel")
    # köşede: incelen defter + kısalan mum (ironi)
    kb = cx.amt(("c9s20", "Genel", -0.1), 0.6)
    if kb > 0.003:
        lx, ly = 1620.0, 800.0
        T_ = lerp(46.0, 14.0, ease_io(clamp((t - tstart) / 6.5), 1.2))
        c.drawRoundRect(skia.Rect.MakeLTRB(lx - 120, ly - 60 - T_, lx + 120, ly + 10), 6, 6, P("#4A2A18", int(255 * kb)))
        c.drawRoundRect(skia.Rect.MakeLTRB(lx - 112, ly - 56 - T_, lx + 112, ly + 4), 4, 4, P("#EDE0BA", int(255 * kb)))
        c.drawLine(lx, ly - 56 - T_, lx, ly + 4, S("#8A7848", 2.0, int(200 * kb)))
        hh = lerp(130.0, 46.0, clamp((t - tstart) / 7.0))
        c.drawRect(skia.Rect.MakeLTRB(lx + 150, gy - hh, lx + 178, gy), P("#EDE2C2", int(255 * kb)))
        c.drawRect(skia.Rect.MakeLTRB(lx + 150, gy - hh, lx + 178, gy), S("#8A7848", 1.4, int(200 * kb), cap=False))
        L.flame(f, lx + 164, gy - hh - 2, 36, t, 9, k=kb)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ bindirme yardımcıları ═══════════════════════════
def seal_pop(x, y, at, r=60, color="#A52A1C", palle=True, out=None):
    """Çapada balmumu mührü basılır (palle izi)."""
    def fn(cx):
        k = clamp((cx.t - cx.at(at)) / 0.45)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k > 0.003:
            CM.wax_seal(cx.f, x, y, r, color, alpha=1.0, t=k, palle=palle)
    return fn


def check_cross(x, y, at, ok=True, size=70, out=None):
    """Çapada ✓ (yeşil) ya da ✗ (kızıl) çarpar."""
    def fn(cx):
        k = cx.amt(at, 0.32, ease=lambda u: sk.back_out(u))
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k <= 0.003:
            return
        c = cx.f.c
        s_ = size * k
        if ok:
            c.drawLine(x - s_ * 0.7, y, x - s_ * 0.15, y + s_ * 0.6, S("#3E7A5A", 16, 245))
            c.drawLine(x - s_ * 0.15, y + s_ * 0.6, x + s_ * 0.85, y - s_ * 0.7, S("#3E7A5A", 16, 245))
        else:
            c.drawLine(x - s_ * 0.7, y - s_ * 0.7, x + s_ * 0.7, y + s_ * 0.7, S("#A8321E", 16, 245))
            c.drawLine(x - s_ * 0.7, y + s_ * 0.7, x + s_ * 0.7, y - s_ * 0.7, S("#A8321E", 16, 245))
    return fn


def icon_at(name, x, y, at, size=150, metal="gold", out=None, glow=0.0):
    def fn(cx):
        k = cx.amt(at, 0.5)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k > 0.003:
            icons.draw_icon(cx.f, name, x, y, size=size * (0.85 + 0.15 * ease_out(k)), metal=metal, alpha=k, shadow=True, glow=glow * k)
    return fn
