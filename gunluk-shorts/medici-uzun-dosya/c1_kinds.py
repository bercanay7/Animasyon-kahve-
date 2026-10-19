"""c1_kinds — c1 (Florin Şehri) için özel çekim türleri. Tümü `c1_` önekli; ana motor dosyalarına dokunmaz.

c1_darphane : darphane — işçi anvile çekiçle vurur, her vuruşta florin yığına uçar; yanda sayan yönetici (Villani).
c1_cicek    : Dante'nin "lanetli çiçeği" — florin zambağı çiçeğe dönüşür, çoban kurda döner (siluet).
c1_agi      : şube ağı — merkez + şubeler (kurulur, sönenler); Peruzzi/Bardi.
c1_edward   : krala giden florinler geri dönmez (borç) — sembolik, siluetsiz.
c1_toprak   : toprak katmanları (veba çukurları — yalnız katman çizgileri; ceset/beden yok).
c1_lonca    : lonca armaları sırası; yün işçisinin yeri boş (kesikli çerçeve).
c1_machiavelli : tarihçi yazar, isyancının ağzına koca bir konuşma ruloşu çıkar (kurgu).
c1_kademe   : seçkinler bir kademe yukarıda; Medici bir kademe aşağıda, kır gelirleri.
c1_kose     : Orsanmichele köşesi — iki sokağın kesiştiği yer (şehir planı), köşeye iğne.
Olgu disiplini: yalnız script'te geçen ad/sayı/tarihler; yüz yok; ölüm/şiddet gösterilmez.
"""
import math

import skia

import cilt_anim as FA
import cilt_cam
import cilt_medici as CM
import cilt_oda as OD
import cilt_props as CP
import icons
import sk
from cilt_medici import TH, ckind
from sk import H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth


sk.METAL["c1_curse"] = [("#0A0612", 0.0), ("#2A1640", 0.30), ("#6A3A8A", 0.56), ("#2A1640", 0.80), ("#0A0612", 1.0)]


def _gilt_or_ink(txt, face, size, track, color=None):
    if TH.day:
        return CM.engraved(txt, face, int(size), track, color or TH.fg)
    return CM.gilt(txt, face, int(size), track)


# ─────────────────────────────────────────────────────────────────────────────
# c1_darphane
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c1_darphane")
def k_darphane(cx, period=0.62, phase=0.0, master_at=None, seed=3, pile0=6, gy=808, toff=0.0, **_):
    T = cx.t + toff
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    cam.begin(f)
    # ocak parıltısı (arka)
    f.circle(1000, gy - 330, 520, shader=f.rad(1000, gy - 330, 520, [("#FFC866", 0.0, 120), ("#FFC866", 1.0, 0)]))
    # ocak (sol arka): tuğla gövde + ağız + alev
    import cilt_sehir as SE
    f.rrect(40, gy - 470, 330, 470, 14, shader=f.lin(40, 0, 370, 0, [("#9A5A3A", 0.0), ("#B0704A", 0.5), ("#7A4430", 1.0)]))
    f.rrect(40, gy - 470, 330, 470, 14, style="stroke", sw=3, color="#3A1E10", alpha=0.8)
    fa_ = skia.Path(); fa_.moveTo(110, gy); fa_.lineTo(110, gy - 190); fa_.arcTo(skia.Rect.MakeLTRB(110, gy - 190 - 90, 300, gy - 190 + 90), 180, 180, False); fa_.lineTo(300, gy); fa_.close()
    c.drawPath(fa_, f.paint("#2A1208"))
    f.circle(205, gy - 120, 150, shader=f.rad(205, gy - 120, 150, [("#FFB040", 0.0, 220), ("#FF7020", 0.6, 120), ("#FF7020", 1.0, 0)]))
    SE.bonfire(f, 205, gy - 8, 120, T, 5, k=1.0, glow_a=0.4, tod="day", smoke=False, embers=True)
    # zemin/tezgâh
    f.rect(-200, gy, W + 400, 500, shader=f.lin(0, gy, 0, gy + 300, [("#7A5430", 0.0), ("#4E3218", 1.0)]))
    for i in range(-2, 16):
        c.drawLine(i * 150 - 30, gy, i * 150 - 150, gy + 280, f.paint("#2E1C0C", style="stroke", sw=2.5, alpha=0.5))
    f.rect(-200, gy - 4, W + 400, 8, color="#2E1C0C", alpha=0.6)
    wx = 560.0
    hh = 560.0
    hx, hy = wx + 0.42 * hh, gy - 0.635 * hh
    # anvil kütüğü + anvil
    f.rrect(hx - 78, hy + 26, 156, gy - hy - 26, 10, shader=f.lin(hx - 78, 0, hx + 78, 0, [("#5A3C1E", 0.0), ("#8A6034", 0.5), ("#4A3018", 1.0)]))
    anv = skia.Path()
    anv.moveTo(hx - 130, hy + 2)
    anv.lineTo(hx + 118, hy + 2)
    anv.lineTo(hx + 190, hy + 16)
    anv.lineTo(hx + 110, hy + 38)
    anv.lineTo(hx + 56, hy + 52)
    anv.lineTo(hx + 70, hy + 92)
    anv.lineTo(hx - 70, hy + 92)
    anv.lineTo(hx - 56, hy + 52)
    anv.lineTo(hx - 126, hy + 36)
    anv.close()
    c.drawPath(anv, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, hy), (0, hy + 92)], [sk.C("#8A8A94"), sk.C("#2E2E36")], [0, 1])))
    c.drawPath(anv, f.paint("#14141A", style="stroke", sw=3, alpha=0.9))
    f.rect(hx - 130, hy - 2, 248, 8, color="#C8C8D4", alpha=0.7)
    # çalışan
    FA.actor(f, "tuccar", wx, gy + 18, hh, T, action="work", mode="strike", period=period, phase=phase, seed=seed)
    # vuruşlar: u = 0.70 anında çekiç iner
    t0 = (0.70 - phase) * period
    k0 = max(0, int(math.floor((T - t0) / period)) - 3)
    px, py0 = 1290.0, gy - 6
    landed = 0
    k_hits = int(math.floor((T - t0) / period)) + 1
    for k in range(max(0, k_hits)):
        tk = t0 + k * period
        a = T - tk
        if a < 0:
            continue
        if a >= 0.62:
            landed += 1
    nn = pile0 + landed
    if nn > 0:
        OD.draw_coins(c, px, py0, min(nn, 45), 3.3, T, seed=1, glint=True)
    for k in range(max(0, k_hits - 5), k_hits + 1):
        tk = t0 + k * period
        a = T - tk
        if a < -0.02 or a > 0.7:
            continue
        if a >= 0:
            # çakma: parıltı + kıvılcımlar
            g = max(0.0, 1.0 - a / 0.22)
            if g > 0:
                f.circle(hx + 20, hy - 6, 120 * (0.5 + 0.7 * (1 - g)), shader=f.rad(hx + 20, hy - 6, 130, [("#FFF4C0", 0.0, int(230 * g)), ("#FFB040", 0.5, int(120 * g)), ("#FFB040", 1.0, 0)]))
                for s_ in range(9):
                    ang = math.radians(-160 + s_ * 18 + 6 * math.sin(k * 3 + s_))
                    r0, r1 = 30 + 160 * (1 - g), 60 + 230 * (1 - g)
                    c.drawLine(hx + 20 + math.cos(ang) * r0, hy - 6 + math.sin(ang) * r0, hx + 20 + math.cos(ang) * r1, hy - 6 + math.sin(ang) * r1,
                               f.paint("#FFE08A", style="stroke", sw=3.0, alpha=0.9 * g))
            # sikke uçuşu
            u = a / 0.62
            if u < 1.0:
                ax, ay = hx + 20, hy - 30
                xx = lerp(ax, px - 40 + 25 * math.sin(k * 2.0), ease_out(u, 1.4))
                yy = lerp(ay, py0 - 55, u * u) - 170 * math.sin(math.pi * min(1, u * 0.95))
                CP.draw_coin(f, xx, yy, 96, spin=a * 22 + k, alpha=1.0, shadow=0.3)
    # yönetici (sayan)
    if master_at is not None:
        km = cx.amt(master_at, 0.6)
        if km > 0.003:
            FA.actor(f, "banker", 1690, gy + 14, 520, T, action="count", dir=-1, seed=11, alpha=km)
    cam.end(f)
    CM.finish(f, cx, motes_n=26)


# ─────────────────────────────────────────────────────────────────────────────
# yardımcı: koyun, kurt (siluet çizimleri)
# ─────────────────────────────────────────────────────────────────────────────
def _sheep(f, x, yg, s, t, ph, alpha=1.0, dirn=1):
    c = f.c
    c.save()
    c.translate(x, yg)
    c.scale(dirn * s, s)
    pa = skia.Paint(AntiAlias=True, Color=sk.C("#F2EBD8", int(255 * alpha)))
    pk = skia.Paint(AntiAlias=True, Color=sk.C("#2A2018", int(255 * alpha)))
    st = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=sk.C("#2A2018", int(255 * alpha)), StrokeCap=skia.Paint.kRound_Cap)
    sw = math.sin(t * 7 + ph) * 8
    for lx, sg in ((-26, 1), (-10, -1), (14, 1), (30, -1)):
        c.drawLine(lx, -26, lx + sw * sg * 0.6, 0, st)
    for (cx_, cy_, r) in ((-26, -52, 22), (-4, -60, 26), (20, -54, 24), (-14, -40, 22), (10, -38, 22), (34, -46, 17)):
        c.drawCircle(cx_, cy_, r, pa)
    c.drawOval(skia.Rect.MakeLTRB(40, -64, 66, -42), pk)          # kafa
    c.drawLine(46, -62, 40, -72, st)
    c.restore()


def _wolf(f, x, yg, s, t, alpha=1.0, dirn=1, col="#1A1418"):
    c = f.c
    c.save()
    c.translate(x, yg)
    c.scale(dirn * s, s)
    pa = skia.Paint(AntiAlias=True, Color=sk.C(col, int(255 * alpha)))
    st = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=11, Color=sk.C(col, int(255 * alpha)), StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    sw = math.sin(t * 9) * 16
    body = skia.Path()
    body.moveTo(-90, -96)
    body.cubicTo(-60, -140, 40, -138, 86, -112)
    body.cubicTo(100, -100, 100, -70, 80, -64)
    body.cubicTo(30, -50, -50, -50, -92, -66)
    body.close()
    c.drawPath(body, pa)
    for lx, sg in ((-76, 1), (-44, -1), (46, -1), (72, 1)):
        pth = skia.Path(); pth.moveTo(lx, -66); pth.lineTo(lx + sw * sg * 0.5, -36); pth.lineTo(lx + sw * sg, 0)
        c.drawPath(pth, st)
    tail = skia.Path(); tail.moveTo(-90, -98); tail.cubicTo(-130, -110, -150, -80, -150, -52)
    c.drawPath(tail, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=18, Color=sk.C(col, int(255 * alpha)), StrokeCap=skia.Paint.kRound_Cap))
    head = skia.Path()
    head.moveTo(70, -126); head.lineTo(112, -140); head.lineTo(150, -112); head.lineTo(176, -108); head.lineTo(172, -96); head.lineTo(136, -86); head.lineTo(100, -78); head.lineTo(78, -90); head.close()
    c.drawPath(head, pa)
    c.drawPath(sk.poly_path([(96, -132), (104, -168), (122, -138)]), pa)
    # parlayan göz
    c.drawCircle(134, -112, 5.5, skia.Paint(AntiAlias=True, Color=sk.C("#FFD060", int(255 * alpha))))
    c.restore()


@ckind("c1_cicek")
def k_cicek(cx, plate=None, florin_at=None, bloom_at=None, curse_at=None, shep_at=None, morph_at=None, flee_at=None, quote_at=None, quote="lanetli çiçek", seed=2, **_):
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="both")
    cam.begin(f)
    gy = 770
    # tepeler (çoban sahnesi)
    for i, (col, y0, amp) in enumerate((("#B9C79A", 640, 40), ("#9DB27E", 700, 34), ("#7E9A62", 760, 26))):
        pth = skia.Path()
        pth.moveTo(-50, H)
        for xi in range(-50, W + 100, 60):
            pth.lineTo(xi, y0 + amp * math.sin(xi * 0.004 + i * 1.7) + 12 * math.sin(xi * 0.011 + i))
        pth.lineTo(W + 50, H)
        pth.close()
        c.drawPath(pth, f.paint(col, alpha=0.9))
    for xi, hh in ((220, 150), (1650, 190), (1760, 130), (1480, 110)):
        c.drawOval(skia.Rect.MakeLTRB(xi - 20, gy - hh - 40, xi + 20, gy - 20), f.paint("#3E5A3A"))
        c.drawLine(xi, gy - 30, xi, gy - 4, f.paint("#2A1A0C", style="stroke", sw=4))
    # florin (başlangıç): çiçeğe dönüşür
    kf = cx.amt(florin_at, 0.5) if florin_at is not None else 0.0
    kb = ease_out(clamp((cx.t - cx.at(bloom_at)) / 1.0), 3) if bloom_at is not None else 0.0
    kc = smooth(clamp((cx.t - cx.at(curse_at)) / 0.9)) if curse_at is not None else 0.0
    fx, fy = 1010.0, 470.0
    if kf > 0.003 and kb < 1.0:
        CP.draw_coin(f, fx, fy, 380 * (1.0 - 0.45 * kb), spin=cx.t * 1.0 + 0.4, alpha=kf * (1 - kb), shadow=0.5)
    if kb > 0.003:
        sway = 0.04 * math.sin(cx.t * 1.6)
        # sap
        stem = skia.Path(); stem.moveTo(fx, gy + 20); stem.quadTo(fx + 40 * math.sin(cx.t * 1.1), gy - 160, fx + 4, fy + 110 * kb)
        c.drawPath(stem, f.paint(mix("#4E7A3C", "#241A2C", kc), style="stroke", sw=14, alpha=kb))
        f.circle(fx, fy, 330 * kb, shader=f.rad(fx, fy, 330 * kb, [(mix("#F0D27A", "#6A2A8A", kc), 0.0, int(110 * kb)), ("#F0D27A", 1.0, 0)]))
        icons.draw_icon(f, "fleur", fx, fy, size=470 * kb * (1.0 + 0.02 * math.sin(cx.t * 2.2)), metal="gold", alpha=kb * (1 - kc), rot=sway, glow=0.0)
        if kc > 0.003:
            icons.draw_icon(f, "fleur", fx, fy, size=470 * kb * (1.0 + 0.02 * math.sin(cx.t * 2.2)), metal="c1_curse", alpha=kb * kc, rot=sway, glow=0.0)
            # mor sis
            for q in range(9):
                ph = (cx.t * 0.35 + q / 9.0) % 1.0
                f.circle(fx + 120 * math.sin(q * 2.3 + cx.t * 0.6), fy + 90 - 260 * ph, 26 + 40 * ph, color="#5A2A7A", alpha=0.20 * kc * (1 - ph), blur=8)
    # çoban + koyunlar
    ks = clamp((cx.t - cx.at(shep_at)) / 3.4) if shep_at is not None else 0.0
    tm = cx.at(morph_at) if morph_at is not None else 1e9
    tf = cx.at(flee_at) if flee_at is not None else 1e9
    if ks > 0:
        xs = lerp(-160, 650, ease_io(ks, 1.5))
        walking = 1.0 if ks < 1.0 else 0.0
        morph = smooth(clamp((cx.t - tm) / 0.55))
        if morph < 1.0:
            _SHEP = skia.Path()
            # çoban: siluet + asa
            import c0_kinds as K0
            K0._sil_person(f, xs, gy + 14, 340, cx.t * 6.0, 0.55 * walking, "plain", alpha=1 - morph, col="#2A1E15")
            f.line(xs + 62, gy + 14, xs + 82, gy - 330, color="#4A3420", sw=7, alpha=1 - morph)
            f.circle(xs + 80, gy - 336, 16, style="stroke", sw=6, color="#4A3420", alpha=1 - morph)
        if morph > 0.0:
            wsc = 1.05 + 0.15 * math.sin(morph * math.pi)
            _wolf(f, xs + 20 + 40 * clamp((cx.t - tm) / 1.5), gy + 14, wsc, cx.t, alpha=morph, dirn=1)
            f.circle(xs + 40, gy - 150, 240, shader=f.rad(xs + 40, gy - 150, 240, [("#8A3AB0", 0.0, int(120 * math.sin(morph * math.pi))), ("#8A3AB0", 1.0, 0)]))
        # koyunlar (çeviren: kaçışır)
        for j, (dx, sc_) in enumerate(((-150, 0.85), (-250, 0.7), (-340, 0.8))):
            fl = clamp((cx.t - (tf + 0.12 * j)) / 1.2)
            xx = xs + dx - 700 * ease_in(fl, 2.0) if tf < 1e8 else xs + dx
            _sheep(f, xx, gy + 12, sc_ * 1.3, cx.t * (1 + 1.8 * fl), j, alpha=1.0)
    if plate is not None:
        CM.name_plate(f, plate[0], None, None, cx_=plate[2] if len(plate) > 2 else 560, y=plate[3] if len(plate) > 3 else 170, t=cx.amt(plate[1], 0.6))
    # alıntı
    if quote_at is not None:
        kq = cx.amt(quote_at, 0.6)
        if kq > 0.003:
            wd = sk.text_width(f"“{quote}”", "cap_i", 70) + 120
            CM.tablet(f, W / 2 - wd / 2, 130 + (1 - kq) * 12, wd, 120, alpha=kq, corner=12)
            CM.ink(f, f"“{quote}”", W / 2, 212 + (1 - kq) * 12, face="cap_i", size=70, color=TH.fg, align="c", alpha=kq, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# yardımcı: kalkan (lonca/aile armaları — stilize, olgu iddiası yok)
# ─────────────────────────────────────────────────────────────────────────────
def _shield_path(w, h):
    p = skia.Path()
    p.moveTo(-w / 2, -h / 2)
    p.lineTo(w / 2, -h / 2)
    p.lineTo(w / 2, h * 0.08)
    p.cubicTo(w / 2, h * 0.34, w * 0.18, h * 0.46, 0, h / 2)
    p.cubicTo(-w * 0.18, h * 0.46, -w / 2, h * 0.34, -w / 2, h * 0.08)
    p.close()
    return p


def _shield(f, x, y, w, h, c1, c2, charge="cross", alpha=1.0, scale=1.0, rot=0.0):
    c = f.c
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    if rot:
        c.rotate(rot)
    sp = _shield_path(w, h)
    f.path(sp, color="#000000", alpha=0.25 * alpha, blur=6)
    c.drawPath(sp, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -h / 2), (0, h / 2)], [sk.C(mix(c1, "#FFFFFF", 0.18), int(255 * alpha)), sk.C(c1, int(255 * alpha))], [0, 1])))
    c.save()
    c.clipPath(sp, skia.ClipOp.kIntersect, True)
    pc = f.paint(c2, alpha=alpha)
    if charge == "cross":
        c.drawRect(skia.Rect.MakeLTRB(-w * 0.09, -h / 2, w * 0.09, h / 2), pc)
        c.drawRect(skia.Rect.MakeLTRB(-w / 2, -h * 0.16, w / 2, h * 0.02), pc)
    elif charge == "bend":
        pp = skia.Path(); pp.moveTo(-w / 2, -h / 2); pp.lineTo(-w * 0.2, -h / 2); pp.lineTo(w / 2, h * 0.3); pp.lineTo(w / 2, h * 0.02); pp.close()
        c.drawPath(pp, pc)
    elif charge == "bars":
        for k in range(3):
            c.drawRect(skia.Rect.MakeLTRB(-w / 2, -h * 0.32 + k * h * 0.26, w / 2, -h * 0.32 + k * h * 0.26 + h * 0.12), pc)
    elif charge == "chief":
        c.drawRect(skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, -h * 0.16), pc)
        c.drawCircle(0, h * 0.14, w * 0.2, pc)
    elif charge == "circle":
        c.drawCircle(0, -h * 0.04, w * 0.26, pc)
        c.drawCircle(0, -h * 0.04, w * 0.13, f.paint(c1, alpha=alpha))
    elif charge == "star":
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            r = w * (0.30 if k % 2 == 0 else 0.13)
            pts.append((r * math.cos(a), -h * 0.04 + r * math.sin(a)))
        c.drawPath(sk.poly_path(pts), pc)
    elif charge == "lily":
        c.drawPath(sk.poly_path([(0, -h * 0.34), (w * 0.16, -h * 0.04), (0, h * 0.2), (-w * 0.16, -h * 0.04)]), pc)
        c.drawCircle(-w * 0.2, -h * 0.02, w * 0.1, pc)
        c.drawCircle(w * 0.2, -h * 0.02, w * 0.1, pc)
    c.restore()
    c.drawPath(sp, f.paint("#2A1A0C", style="stroke", sw=3.2, alpha=0.9 * alpha))
    c.drawPath(sp, f.paint("#D8B25A", style="stroke", sw=1.2, alpha=0.7 * alpha))
    c.restore()


# ─────────────────────────────────────────────────────────────────────────────
# c1_agi — şube ağı (Peruzzi / Bardi)
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c1_agi")
def k_agi(cx, hubs=(), count=None, medici_at=None, medici_no_at=None, label_at=None, intro_at=None, seed=1, **_):
    """hubs=[dict(label, x, y, rx, ry, n, build=(a0,a1), die=(a0,a1), ang0, col)]; count=dict(at, to, x, y, label) → büyük sayaç (şube sayısı)."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="both")
    cam.begin(f)
    for hi, h in enumerate(hubs):
        hx, hy, rx, ry, n = h["x"], h["y"], h["rx"], h["ry"], h["n"]
        b0, b1 = (cx.at(h["build"][0]), cx.at(h["build"][1])) if h.get("build") else (0.0, 0.0)
        kh = clamp((cx.t - (b0 - 0.5)) / 0.5) if h.get("build") else 1.0
        d0, d1 = (cx.at(h["die"][0]), cx.at(h["die"][1])) if h.get("die") else (1e9, 1e9 + 1)
        dk = clamp((cx.t - d0) / max(1e-3, d1 - d0))
        col = h.get("col", "#233C8C")
        ang0 = h.get("ang0", -math.pi / 2 + 0.2)
        pts = []
        for i in range(n):
            a = ang0 + 2 * math.pi * i / n
            pts.append((hx + rx * math.cos(a), hy + ry * math.sin(a)))
        # kenarlar + düğümler
        for i, (px, py) in enumerate(pts):
            ti = lerp(b0, b1, i / max(1, n - 1))
            k = clamp((cx.t - ti) / 0.4)
            if k <= 0:
                continue
            death = clamp(dk * (n + 3) - ((i * 7) % n) * 0.9)           # düğümler karışık sırada söner
            dead = smooth(clamp(death))
            lc = mix("#6A4A2A", "#8A8A92", dead)
            # hat (büyür)
            ex, ey = lerp(hx, px, ease_out(k, 2)), lerp(hy, py, ease_out(k, 2))
            pl = f.paint(lc, style="stroke", sw=4.0, alpha=0.9 * (1 - 0.6 * dead))
            if dead > 0.3:
                pl.setPathEffect(skia.DashPathEffect.Make([10, 12], 0))
            c.drawLine(hx, hy, ex, ey, pl)
            # akan florin (canlıyken)
            if k >= 1.0 and dead < 0.5:
                ph = (cx.t * 0.5 + i * 0.173) % 1.0
                f.circle(lerp(hx, px, ph), lerp(hy, py, ph), 6, color="#F0C040", alpha=0.95 * (1 - dead))
            s_ = 26 * ease_out(k, 3) * (1 - 0.15 * dead)
            f.circle(px + 2, py + 6, s_, color="#000000", alpha=0.25 * k, blur=4)
            f.circle(px, py, s_, shader=f.rad(px - s_ * 0.3, py - s_ * 0.35, s_ * 1.5, [(mix(mix(col, "#FFFFFF", 0.35), "#9A9AA2", dead), 0.0), (mix(col, "#8A8A92", dead), 1.0)]), alpha=k)
            f.circle(px, py, s_, style="stroke", sw=3.0, color=mix("#D8B25A", "#777780", dead), alpha=k)
            f.circle(px, py, s_ * 0.34, color=mix("#F6DC90", "#A0A0A8", dead), alpha=k)
        # merkez
        hs = 64 * ease_out(kh, 3)
        hd = smooth(clamp(dk * (n + 3) - n * 0.95))
        if hs > 1:
            f.circle(hx + 3, hy + 8, hs, color="#000000", alpha=0.3 * kh, blur=8)
            f.circle(hx, hy, hs, shader=f.rad(hx - hs * 0.3, hy - hs * 0.35, hs * 1.6, [(mix("#6A8AD8", "#9A9AA2", hd), 0.0), (mix(col, "#7A7A82", hd), 1.0)]), alpha=kh)
            f.circle(hx, hy, hs, style="stroke", sw=5, color=mix("#E8C468", "#8A8A90", hd), alpha=kh)
            icons.draw_icon(f, "coinbag", hx, hy, size=hs * 1.2, metal="gold" if hd < 0.5 else "silver", alpha=kh * (1 - 0.3 * hd), glow=0.0)
            if hd > 0.4:
                for sg in (1, -1):
                    f.line(hx - 46, hy - 46 * sg, hx + 46, hy + 46 * sg, color="#6A2A2A", sw=6, alpha=0.9 * hd)
        if h.get("label"):
            kl = cx.amt(h.get("label_at", h["build"][0] if h.get("build") else 0.0), 0.6, off=-0.2)
            lab = h["label"]
            wd = sk.text_width(lab, "title_m", 36, 6) + 70
            yy = hy + ry + 76
            CM.tablet(f, hx - wd / 2, yy - 38, wd, 66, alpha=kl * (1 - 0.25 * hd), corner=8)
            CM.ink(f, lab, hx, yy + 8, face="title_m", size=36, color=TH.fg if hd < 0.5 else TH.fg3, align="c", track=6, alpha=kl, emboss=False)
    if intro_at is not None and medici_at is not None:
        # genel "çok şubeli banka" şeması: ortada merkez, etrafında şubeler tek tek kurulur; Medici arması gelince solar
        ti = cx.at(intro_at)
        fade = 1.0 - cx.amt(medici_at, 0.5, off=0.1)
        if fade > 0.003:
            gx, gy2 = 960.0, 560.0
            for q in range(8):
                kq = clamp((cx.t - (ti + 0.16 * q)) / 0.4)
                if kq <= 0:
                    continue
                a = math.radians(q * 45 + 12)
                px, py = gx + 330 * math.cos(a), gy2 + 190 * math.sin(a)
                ex, ey = lerp(gx, px, ease_out(kq, 2)), lerp(gy2, py, ease_out(kq, 2))
                c.drawLine(gx, gy2, ex, ey, f.paint("#6A4A2A", style="stroke", sw=4, alpha=0.8 * fade))
                f.circle(px, py, 22 * ease_out(kq, 3), shader=f.rad(px - 6, py - 6, 30, [("#9AB0E0", 0.0), ("#4A64B0", 1.0)]), alpha=fade)
                f.circle(px, py, 22 * ease_out(kq, 3), style="stroke", sw=3, color="#D8B25A", alpha=fade)
            f.circle(gx, gy2, 52, shader=f.rad(gx - 14, gy2 - 14, 70, [("#7A94D8", 0.0), ("#2A4090", 1.0)]), alpha=fade)
            f.circle(gx, gy2, 52, style="stroke", sw=5, color="#E8C468", alpha=fade)
            icons.draw_icon(f, "coinbag", gx, gy2, size=62, metal="gold", alpha=fade, glow=0.0, shadow=False)
            CM.ink(f, "ÇOK ŞUBELİ BANKA", gx, 330, face="title_m", size=46, color=TH.fg, align="c", track=12, alpha=fade * cx.amt(intro_at, 0.5), emboss=False)
    if medici_at is not None:
        km = cx.amt(medici_at, 0.5)
        if km > 0.003:
            mx_, my_ = 250.0, 300.0
            f.circle(mx_, my_, 170, shader=f.rad(mx_, my_, 170, [("#C03020", 0.0, int(60 * km)), ("#C03020", 1.0, 0)]))
            CP.draw_arms(f, mx_, my_, 210 * (0.85 + 0.15 * sk.back_out(km)), alpha=km, shadow=0.5)
            if medici_no_at is not None:
                kn = cx.amt(medici_no_at, 0.32)
                if kn > 0.003:
                    for sg in (1, -1):
                        f.line(mx_ - 130 * kn, my_ - 130 * sg * kn, mx_ + 130 * kn, my_ + 130 * sg * kn, color="#A8201A", sw=16, alpha=0.95 * kn)
    if count is not None:
        ta = cx.at(count["at"])
        tb = cx.at(count["to"]) if count.get("to") is not None else ta + 1.5
        v = int(round(count["n"] * ease_out(clamp((cx.t - ta) / max(0.2, tb - ta)), 2)))
        ka = cx.amt(count["at"], 0.4)
        if ka > 0.003:
            sp = _gilt_or_ink(str(v), "title", 180, 8.0)
            CM.draw_spr(f, sp, count["x"], count["y"], "c", alpha=ka, shadow=0.0)
            CM.ink(f, count.get("label", ""), count["x"], count["y"] + 70, face="title_m", size=46, color=TH.acc, align="c", track=16, alpha=ka * cx.amt(count["at"], 0.8, off=0.2), emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# c1_edward — florinler krala gider, geri dönmez
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c1_edward")
def k_edward(cx, flow_at=None, stop_at=None, plate_at=None, stamp_at=None, seed=2, **_):
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="both")
    cam.begin(f)
    ax, bx, yy = 520.0, 1500.0, 520.0
    tf = cx.at(flow_at) if flow_at is not None else 0.0
    ts = cx.at(stop_at) if stop_at is not None else 1e9
    # sol: florin yığını (şehir bankaları) — azalır
    left = max(6, 40 - int(max(0.0, (cx.t - tf)) * 5))
    f.circle(ax, yy + 150, 260, shader=f.rad(ax, yy + 150, 260, [("#F0D27A", 0.0, 80), ("#F0D27A", 1.0, 0)]))
    OD.draw_coins(c, ax, yy + 150, left, 3.2, cx.t, seed=2, glint=True)
    icons.draw_icon(f, "coinbag", ax, yy - 20, size=230, metal="gold", alpha=1.0, glow=0.0)
    # sağ: taç
    kp = cx.amt(plate_at, 0.6) if plate_at is not None else 1.0
    f.circle(bx, yy, 280, shader=f.rad(bx, yy, 280, [("#C03020", 0.0, int(70 * kp)), ("#C03020", 1.0, 0)]))
    icons.draw_icon(f, "crown", bx, yy - 10, size=300 * (0.8 + 0.2 * sk.back_out(kp)), metal="gold", alpha=kp, glow=0.0)
    if plate_at is not None:
        CM.name_plate(f, "III. EDWARD", "İNGİLTERE KRALI", None, cx_=bx, y=yy + 190, t=cx.amt(plate_at, 0.6))
    # ok yolu
    pth = skia.Path(); pth.moveTo(ax + 150, yy + 40); pth.quadTo((ax + bx) / 2, yy - 260, bx - 170, yy + 20)
    kk = cx.amt(flow_at, 0.5) if flow_at is not None else 1.0
    c.drawPath(pth, f.paint("#C9A24A", style="stroke", sw=5, alpha=0.5 * kk))
    pm = skia.PathMeasure(pth, False)
    L = pm.getLength()
    if flow_at is not None and cx.t > tf:
        n = 14
        for i in range(n):
            ph = ((cx.t - tf) * 0.55 + i / n) % 1.0
            pos, _ = pm.getPosTan(L * ph)
            if pos is None:
                continue
            f.circle(pos.x(), pos.y(), 17, shader=f.rad(pos.x() - 5, pos.y() - 5, 24, [("#FFF0B0", 0.0), ("#E0A830", 1.0)]), alpha=min(1.0, (cx.t - tf) * 2) * (0.9 if cx.t < ts else 0.9))
    # geri dönüş (yol boş): kesikli gri ok, sonra çarpı
    back = skia.Path(); back.moveTo(bx - 170, yy + 120); back.quadTo((ax + bx) / 2, yy + 360, ax + 150, yy + 130)
    kb = cx.amt(stop_at, 0.6, off=-0.4) if stop_at is not None else 0.0
    if kb > 0.003:
        pb = f.paint("#8A8A92", style="stroke", sw=6, alpha=0.8 * kb)
        pb.setPathEffect(skia.DashPathEffect.Make([16, 14], -cx.t * 30))
        c.drawPath(back, pb)
        mx, my = (ax + bx) / 2, yy + 250
        kx = cx.amt(stop_at, 0.3)
        for sg in (1, -1):
            f.line(mx - 62 * kx, my - 62 * sg * kx, mx + 62 * kx, my + 62 * sg * kx, color="#A8201A", sw=18, alpha=0.95 * kx)
    if stamp_at is not None:
        CM.stamp(f, "ÖDENMEDİ", 960, 800, rot=-0.07, size=70, t=cx.amt(stamp_at, 0.3))
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# c1_toprak — toprak katmanları (çukur kesiti; ceset/beden yok)
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c1_toprak")
def k_toprak(cx, pit_at=None, layers_at=None, layers_to=None, n=8, seed=3, **_):
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    cam.begin(f)
    c.drawRect(skia.Rect.MakeLTRB(-50, -50, W + 50, H + 50), f.paint("#14100E"))
    gy, x0, x1, ybot = 330.0, 460.0, 1460.0, 800.0
    # toprak gövdesi (kesit)
    f.rect(-50, gy, W + 100, H, shader=f.lin(0, gy, 0, H, [("#4A3420", 0.0), ("#2A1C10", 1.0)]))
    rs = [(37 * i) % 11 for i in range(80)]
    for i in range(70):
        xx = (i * 71) % W
        yy = gy + 30 + (i * 53) % (H - gy)
        f.circle(xx, yy, 3 + rs[i % 80] * 0.3, color="#6A4A2E", alpha=0.35)
    # yüzey çizgisi + otlar
    c.drawLine(-50, gy, W + 50, gy, f.paint("#6E8A4A", style="stroke", sw=10, alpha=0.95))
    for i in range(0, W, 26):
        c.drawLine(i, gy, i + 4 * math.sin(i + cx.t), gy - 12 - (i % 3) * 5, f.paint("#7E9A56", style="stroke", sw=3, alpha=0.9))
    # çukur (açılır)
    kp = ease_out(clamp((cx.t - cx.at(pit_at)) / 1.1), 2) if pit_at is not None else 0.0
    if kp > 0.003:
        depth = (ybot - gy) * kp
        pit = skia.Path(); pit.moveTo(x0, gy - 2); pit.lineTo(x1, gy - 2); pit.lineTo(x1 - 30, gy + depth); pit.lineTo(x0 + 30, gy + depth); pit.close()
        c.drawPath(pit, f.paint("#080604"))
        c.drawPath(pit, f.paint("#2A1C10", style="stroke", sw=4, alpha=0.9))
    # katmanlar: alttan yukarı
    if layers_at is not None:
        ta = cx.at(layers_at)
        tb = cx.at(layers_to) if layers_to is not None else ta + 2.5
        cols = ["#6A4A2A", "#8A6A3E", "#5A3E22", "#A07C48", "#4A3220", "#8A6A3E", "#6A4A2A", "#9A7A46"]
        lh = (ybot - gy - 10) / n
        for i in range(n):
            ti = lerp(ta, tb, i / n)
            k = ease_out(clamp((cx.t - ti) / 0.5), 2)
            if k <= 0:
                continue
            yb = ybot - i * lh
            ht = lh * k
            top = yb - ht
            wl = x0 + 30 - (x0 + 30 - x0) * (ybot - yb) / (ybot - gy)
            wr = x1 - 30 + 30 * (ybot - yb) / (ybot - gy)
            pth = skia.Path(); pth.moveTo(wl, yb)
            for xi in range(int(wl), int(wr) + 1, 40):
                pth.lineTo(xi, top + 5 * math.sin(xi * 0.03 + i))
            pth.lineTo(wr, yb); pth.close()
            c.drawPath(pth, f.paint(cols[i % len(cols)], alpha=0.98))
            c.drawPath(pth, f.paint("#1E140A", style="stroke", sw=2.2, alpha=0.8))
            for q in range(14):
                f.circle(wl + (wr - wl) * ((q * 37 + i * 11) % 100) / 100.0, top + ht * ((q * 53) % 100) / 100.0, 2.4, color="#2A1C10", alpha=0.5 * k)
    cam.end(f)
    CM.finish(f, cx, motes_n=16, light=CM.candle_light(cx.t, 3, base=(W * 0.5, H * 0.52), r=1100.0, sway=3.0))


# ─────────────────────────────────────────────────────────────────────────────
# c1_lonca — lonca armaları; yün işçilerinin yeri boş
# ─────────────────────────────────────────────────────────────────────────────
_CHG = ["cross", "bend", "bars", "chief", "circle", "star", "lily"]
_COL = [("#8E2A30", "#F0E6CC"), ("#233C8C", "#F0D27A"), ("#F0E6CC", "#8E2A30"), ("#3E7A5A", "#F0E6CC"), ("#D2A33E", "#233C8C"), ("#5A3E7A", "#F0D27A"), ("#B33620", "#F0E6CC")]


@ckind("c1_lonca")
def k_lonca(cx, rows_at=None, carder_at=None, empty_at=None, mute_at=None, seed=2, **_):
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="both")
    cam.begin(f)
    t0 = cx.at(rows_at) if rows_at is not None else 0.0
    # 21 arma: 3 sıra × 7
    sx0, sy0, dx, dy = 960 - 3 * 190, 270, 190, 190
    for r in range(3):
        for k in range(7):
            i = r * 7 + k
            ti = t0 + 0.07 * i
            kk = clamp((cx.t - ti) / 0.35)
            if kk <= 0:
                continue
            ch = _CHG[(i * 3 + r) % len(_CHG)]
            c1_, c2_ = _COL[(i * 5 + r * 2) % len(_COL)]
            _shield(f, sx0 + k * dx, sy0 + r * dy + 10 * math.sin(cx.t * 1.5 + i), 112, 138, c1_, c2_, ch, alpha=kk, scale=0.85 + 0.15 * sk.back_out(kk))
    # yün tarayıcısı siluet (boş yer) — alt orta
    kcr = cx.amt(carder_at, 0.6) if carder_at is not None else 0.0
    gy = 960
    if kcr > 0.003:
        OD.sil_actor(f, "halk", 880, gy, 400, cx.t, action="work", dir=1, seed=6, color="#2A1E15", rim="#E8B070", rim_dir=1, alpha=kcr) if False else OD.sil_actor(f, "halk", 880, gy, 400, cx.t, action="idle", dir=1, seed=6, color="#2A1E15", rim="#E8B070", rim_dir=1)
        # yün tarağı + yün lifleri
        f.line(880 + 70, gy - 170, 880 + 190, gy - 210, color="#4A3420", sw=8, alpha=kcr)
        for q in range(6):
            f.line(880 + 170 + q * 9, gy - 224, 880 + 176 + q * 9, gy - 185, color="#4A3420", sw=3, alpha=kcr)
        for q in range(7):
            ph = (cx.t * 0.7 + q / 7.0) % 1.0
            f.circle(880 + 230 + 30 * math.sin(q * 2 + cx.t), gy - 200 - 120 * ph, 10 + 8 * ph, color="#F2EBD8", alpha=0.7 * kcr * (1 - ph))
    # boş (kesikli) kalkan + çarpı
    ke = cx.amt(empty_at, 0.5) if empty_at is not None else 0.0
    if ke > 0.003:
        sp = _shield_path(150, 186)
        c.save(); c.translate(1290, gy - 150); c.scale(1.0, 1.0)
        pd = f.paint("#6A4A2A", style="stroke", sw=6, alpha=0.9 * ke)
        pd.setPathEffect(skia.DashPathEffect.Make([16, 12], -cx.t * 14))
        c.drawPath(sp, pd)
        c.restore()
        kx = cx.amt(empty_at, 0.4, off=0.35)
        for sg in (1, -1):
            f.line(1290 - 52 * kx, gy - 150 - 52 * sg * kx, 1290 + 52 * kx, gy - 150 + 52 * sg * kx, color="#A8201A", sw=10, alpha=0.9 * kx)
    # susturulmuş konuşma balonu
    km = clamp((cx.t - cx.at(mute_at)) / 1.6) if mute_at is not None else 0.0
    if km > 0:
        a = math.sin(min(1, km) * math.pi) * (1 - 0.4 * max(0, km - 1))
        bx, by = 1060, gy - 500
        f.oval(bx, by, 110, 62, color="#F6EFD8", alpha=0.95 * a)
        f.oval(bx, by, 110, 62, style="stroke", sw=3, color="#4A3420", alpha=a)
        f.poly([(bx - 40, by + 52), (bx - 66, by + 98), (bx - 4, by + 58)], color="#F6EFD8", alpha=0.95 * a)
        for q in range(3):
            f.circle(bx - 36 + q * 36, by, 8, color="#4A3420", alpha=a * (0.4 + 0.6 * ((cx.t * 2 + q) % 3 < 1.5)))
        # silik çizgi
        f.line(bx - 100, by - 46, bx + 100, by + 46, color="#A8201A", sw=7, alpha=0.8 * a * clamp(km * 1.4))
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# c1_machiavelli — tarihçi, isyancının ağzına koca bir konuşma koyar (KURGU)
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c1_machiavelli")
def k_machiavelli(cx, plate_at=None, order_at=None, rebel_at=None, scroll_at=None, scroll_to=None, nameless_at=None, stamp_at=None, seed=2, **_):
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="both")
    cam.begin(f)
    gy = 900
    f.rect(-100, gy, W + 200, 300, shader=f.lin(0, gy, 0, gy + 200, [("#7A5430", 0.0), ("#4E3218", 1.0)]))
    # yazar (sol) — masa başında yazan
    wx = 470
    FA.actor(f, "banker", wx, gy, 560, cx.t, action="write", seed=4)
    kp = cx.amt(plate_at, 0.6) if plate_at is not None else 0.0
    if kp > 0.003:
        CM.name_plate(f, "MACHIAVELLİ", None, None, cx_=wx + 60, y=gy - 840, t=kp)
    # Medici siparişi: masa köşesinde palle mührü
    ko = cx.amt(order_at, 0.5) if order_at is not None else 0.0
    if ko > 0.003:
        CM.wax_seal(f, wx + 300, gy - 130, 40, "#A52A1C", alpha=ko, t=ko, palle=True)
    # isyancı (sağ) — adsız siluet
    rx = 1500
    kr = cx.amt(rebel_at, 0.6) if rebel_at is not None else 0.0
    if kr > 0.003:
        OD.sil_actor(f, "halk", rx, gy + 6, 560, cx.t, action="idle", dir=-1, seed=8, color="#241A14", rim="#E8B070", rim_dir=-1)
        hx_, hy_ = rx + 0.02 * 560, gy - 0.905 * 560
        kn = cx.amt(nameless_at, 0.5) if nameless_at is not None else 0.0
        if kn > 0.003:
            f.circle(hx_ + 6, hy_ - 120, 52, shader=f.rad(hx_, hy_ - 130, 62, [("#F6EFD8", 0.0, 255), ("#F6EFD8", 1.0, 255)]), alpha=0.95 * kn)
            f.circle(hx_ + 6, hy_ - 120, 52, style="stroke", sw=4, color="#4A3420", alpha=kn)
            icons.draw_icon(f, "question", hx_ + 6, hy_ - 120, size=82, metal="bronze", alpha=kn, glow=0.0, shadow=False)
    # konuşma rulosu: yazarın masasından isyancının ağzına doğru uzar; üzerine satırlar yazılır
    if scroll_at is not None:
        ta = cx.at(scroll_at)
        tb = cx.at(scroll_to) if scroll_to is not None else ta + 4.0
        p = ease_io(clamp((cx.t - ta) / max(0.3, tb - ta)), 1.6)
        if p > 0.003:
            sx, sy = wx + 190, gy - 270
            ex, ey = rx + 24, gy - 0.905 * 560 + 10
            pts = []
            n = 40
            for i in range(n + 1):
                u = i / n
                x = lerp(sx, ex, u)
                y = lerp(sy, ey, u) - 330 * math.sin(math.pi * u) + 24 * math.sin(u * 22 + cx.t * 2)
                pts.append((x, y))
            m = max(2, int(n * p))
            band = 78
            top, bot = [], []
            for i in range(m + 1):
                (x, y) = pts[i]
                (x2, y2) = pts[min(n, i + 1)]
                ang = math.atan2(y2 - y, x2 - x)
                nx, ny = -math.sin(ang), math.cos(ang)
                wv = band * (0.55 + 0.45 * min(1.0, i / 6.0))
                top.append((x + nx * wv * 0.5, y + ny * wv * 0.5))
                bot.append((x - nx * wv * 0.5, y - ny * wv * 0.5))
            poly = sk.poly_path(top + bot[::-1])
            c.drawPath(poly, f.paint("#F1E6C4", alpha=0.98))
            c.drawPath(poly, f.paint("#4A3420", style="stroke", sw=2.6, alpha=0.9))
            for i in range(0, m, 2):
                (x, y) = pts[i]
                (x2, y2) = pts[min(n, i + 1)]
                f.line(x, y - 9, x2, y2 - 9, color="#3A2616", sw=3.2, alpha=0.65)
                f.line(x, y + 11, x2, y2 + 11, color="#3A2616", sw=3.2, alpha=0.65)
            # kalem ucu: rulonun yazıldığı yerde
            ex_, ey_ = pts[m]
            OD.quill(c, ex_ + 6, ey_ + 8, -58.0, 0.9)
    if stamp_at is not None:
        CM.stamp(f, "KURGU", 960, 340, rot=-0.08, size=96, t=cx.amt(stamp_at, 0.3))
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# c1_kademe — seçkinler bir kademe yukarıda; Medici bir kademe aşağıda; kır gelirleri
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c1_kademe")
def k_kademe(cx, elite_at=None, medici_at=None, field_at=None, income_at=None, seed=2, **_):
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="both")
    cam.begin(f)
    gy = 880
    # basamaklar (sol yarı): üst = seçkinler, bir alt = Medici
    steps = [(150, gy - 260, 540), (690, gy - 130, 450), (1140, gy, 300)]
    for i, (x, y, w) in enumerate(steps):
        f.rect(x, y, w, gy - y + 60, shader=f.lin(x, y, x, gy + 60, [("#D8C9A4", 0.0), ("#A8946A", 1.0)]))
        f.rect(x, y, w, 12, color="#F0E4C2")
        f.rect(x, y, w, gy - y + 60, style="stroke", sw=3, color="#5A3E22", alpha=0.7)
    ke = cx.amt(elite_at, 0.6) if elite_at is not None else 0.0
    if ke > 0.003:
        for i in range(4):
            _shield(f, 250 + i * 125, steps[0][1] - 96, 100, 124, *_COL[(i * 2 + 1) % len(_COL)], _CHG[(i * 2) % len(_CHG)], alpha=ke * clamp(ke * 1.4 - i * 0.15), scale=1.0)
        CM.ink(f, "SEÇKİNLER", 150 + 270, steps[0][1] + 110, face="title_m", size=42, color="#4A2A12", align="c", track=12, alpha=ke, emboss=False)
    km = cx.amt(medici_at, 0.6) if medici_at is not None else 0.0
    if km > 0.003:
        CP.draw_arms(f, 915, steps[1][1] - 130, 190 * (0.85 + 0.15 * sk.back_out(km)), alpha=km, shadow=0.5)
        CM.ink(f, "MEDİCİ", 915, steps[1][1] + 90, face="title_m", size=42, color="#4A2A12", align="c", track=12, alpha=km, emboss=False)
        # bir kademe: ok
        ka = smooth(clamp((km - 0.2) / 0.8))
        f.line(716, steps[0][1] - 4, 716, steps[1][1] - 56, color="#A8201A", sw=7, alpha=0.9 * ka)
        f.poly([(716, steps[1][1] - 36), (700, steps[1][1] - 62), (732, steps[1][1] - 62)], color="#A8201A", alpha=0.9 * ka)
    # kır: sağda tarla sıraları + selvi + çiftlik
    kf = cx.amt(field_at, 0.8) if field_at is not None else 0.0
    if kf > 0.003:
        fx0, fx1 = 1470, 1800
        poly = sk.poly_path([(fx0, gy + 40), (fx1 + 40, gy + 40), (fx1 + 40, gy - 150), (fx0 + 80, gy - 150)])
        c.drawPath(poly, f.paint("#9DB27E", alpha=kf))
        for r in range(6):
            yy = gy - 130 + r * 28
            c.drawLine(fx0 + 80 - r * 12, yy, fx1 + 40, yy, f.paint("#6E8A4A", style="stroke", sw=5, alpha=kf))
        c.drawOval(skia.Rect.MakeLTRB(1640 - 18, gy - 330, 1640 + 18, gy - 100), f.paint("#3E5A3A", alpha=kf))
        f.rect(1690, gy - 220, 100, 80, color="#C9B58A", alpha=kf)
        f.poly([(1680, gy - 220), (1740, gy - 280), (1800, gy - 220)], color="#B33620", alpha=kf)
    # gelir: tarladan Medici'ye altın tanecikleri
    ki = clamp((cx.t - cx.at(income_at)) / 3.0) if income_at is not None else 0.0
    if ki > 0:
        pth = skia.Path(); pth.moveTo(1520, gy - 120); pth.quadTo(1230, gy - 420, 990, steps[1][1] - 70)
        pm = skia.PathMeasure(pth, False)
        for i in range(10):
            ph = ((cx.t - cx.at(income_at)) * 0.5 + i / 10.0) % 1.0
            pos, _ = pm.getPosTan(pm.getLength() * ph)
            if pos is not None:
                f.circle(pos.x(), pos.y(), 12, shader=f.rad(pos.x() - 3, pos.y() - 3, 16, [("#FFF0B0", 0.0), ("#E0A830", 1.0)]), alpha=min(1.0, ki * 3))
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# c1_kose — şehir planı: Orsanmichele; Via Porta Rossa × Via Calimala; köşeye iğne
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c1_kose")
def k_kose(cx, orsa_at=None, street1_at=None, street2_at=None, pin_at=None, seed=2, **_):
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="both")
    cam.begin(f)
    ox, oy = 960.0, 520.0
    # şehir blokları (üstten): iki sokak X biçiminde keser
    rs = [(41 * i) % 17 for i in range(60)]
    blocks = [(-100, -80, 560, 340), (-100, 380, 560, 420), (720, -80, 460, 340), (720, 480, 460, 380), (1000, -80, 420, 320), (1060, 640, 380, 280)]
    # dört büyük blok (köşeler) + Orsanmichele bloğu (köşede)
    c.save()
    c.translate(ox, oy)
    c.rotate(-12)
    for (bx, by, bw, bh) in ((-1100, -700, 960, 560), (150, -700, 1100, 560), (-1100, 150, 960, 620), (150, 150, 1100, 620)):
        c.drawRect(skia.Rect.MakeXYWH(bx, by, bw, bh), f.paint("#C9B58A"))
        c.drawRect(skia.Rect.MakeXYWH(bx, by, bw, bh), f.paint("#5A3E22", style="stroke", sw=3, alpha=0.7))
        for q in range(14):
            qx = bx + 40 + (q * 137) % int(bw - 120)
            qy = by + 40 + (q * 89) % int(bh - 120)
            c.drawRect(skia.Rect.MakeXYWH(qx, qy, 90 + rs[q] * 5, 60 + rs[q + 3] * 3), f.paint("#B33620", alpha=0.85))
            c.drawRect(skia.Rect.MakeXYWH(qx, qy, 90 + rs[q] * 5, 60 + rs[q + 3] * 3), f.paint("#3A1E10", style="stroke", sw=2, alpha=0.6))
    # sokaklar (açık zemin) etiketleri
    c.restore()
    # Orsanmichele: köşe bloğu (yüksek, kemerli)
    ko = cx.amt(orsa_at, 0.7) if orsa_at is not None else 0.0
    if ko > 0.003:
        c.save(); c.translate(ox + 190, oy - 190); c.rotate(-12); c.scale(0.9 + 0.1 * ko, 0.9 + 0.1 * ko)
        f.rect(-130, -110, 260, 220, color="#E6D8B4", alpha=ko)
        f.rect(-130, -110, 260, 220, style="stroke", sw=4, color="#3A2210", alpha=ko)
        for q in range(4):
            f.rect(-100 + q * 54, -80, 40, 120, color="#8A7048", alpha=ko)
        f.poly([(-150, -110), (0, -170), (150, -110)], color="#B33620", alpha=ko)
        c.restore()
        CM.ink(f, "ORSANMICHELE", ox + 190, oy - 400, face="title_m", size=34, color=TH.fg, align="c", track=8, alpha=ko, emboss=False)
    # sokak etiketleri
    k1 = cx.amt(street1_at, 0.6) if street1_at is not None else 0.0
    k2 = cx.amt(street2_at, 0.6) if street2_at is not None else 0.0
    for (kk, txt, ang, px, py) in ((k1, "VIA PORTA ROSSA", -12, 520, 560), (k2, "VIA CALIMALA", 78, 1210, 600)):
        if kk > 0.003:
            c.save(); c.translate(px, py); c.rotate(ang)
            CM.ink(f, txt, 0, 0, face="title_m", size=40, color="#5A1A12", align="c", track=10, alpha=kk, emboss=False)
            c.restore()
    # iğne: kesişim
    kp = cx.amt(pin_at, 0.5) if pin_at is not None else 0.0
    if kp > 0.003:
        drop = (1 - ease_out(kp, 3)) * 160
        f.circle(ox + 14, oy + 16, 22 * kp, color="#000000", alpha=0.3 * kp, blur=6)
        f.circle(ox, oy - drop - 90, 62 * kp, shader=f.rad(ox - 16, oy - 16 - drop - 90, 80, [("#FF8A70", 0.0), ("#A8201A", 1.0)]), alpha=kp)
        f.line(ox, oy - drop - 28, ox, oy, color="#2A1A0C", sw=7, alpha=kp)
        icons.draw_icon(f, "coinbag", ox, oy - drop - 90, size=70 * kp, metal="gold", alpha=kp, glow=0.0, shadow=False)
        if kp >= 1.0:
            ph = (cx.t * 0.8) % 1.0
            f.circle(ox, oy, 40 + 120 * ph, style="stroke", sw=4, color="#A8201A", alpha=0.6 * (1 - ph))
    cam.end(f)
    CM.finish(f, cx, motes_n=18)


# ─────────────────────────────────────────────────────────────────────────────
# c1_okul — hesap okulu: çocuklar yazar/sayar, hoca hesap tahtasında boncuk kaydırır
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c1_okul")
def k_okul(cx, kids_at=None, board_at=None, plate_at=None, seed=4, **_):
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="both")
    cam.begin(f)
    gy = 900
    f.rect(-100, gy, W + 200, 300, shader=f.lin(0, gy, 0, gy + 200, [("#8A6038", 0.0), ("#563820", 1.0)]))
    for i in range(-2, 16):
        c.drawLine(i * 140, gy, i * 140 - 70, gy + 200, f.paint("#3A2410", style="stroke", sw=2.5, alpha=0.5))
    # hesap tahtası (sağ): çerçeveli tahta + 5 sıra boncuk
    bx, by, bw, bh = 1120, 250, 640, 430
    kb = cx.amt(board_at, 0.7) if board_at is not None else 1.0
    f.rrect(bx + 8, by + 12, bw, bh, 12, color="#000000", alpha=0.3 * kb, blur=10)
    f.rrect(bx, by, bw, bh, 12, shader=f.lin(bx, by, bx, by + bh, [("#6A4222", 0.0), ("#4A2C14", 1.0)]), alpha=kb)
    f.rrect(bx + 22, by + 22, bw - 44, bh - 44, 6, shader=f.lin(bx, by, bx, by + bh, [("#2E3A2E", 0.0), ("#1E2820", 1.0)]), alpha=kb)
    tb = cx.at(board_at) if board_at is not None else 0.0
    for r in range(5):
        yy = by + 78 + r * 70
        c.drawLine(bx + 44, yy, bx + bw - 44, yy, f.paint("#D8C9A4", style="stroke", sw=3, alpha=0.8 * kb))
        for q in range(9):
            slide = 0.5 + 0.5 * math.sin((cx.t - tb) * (0.9 + 0.17 * r) + r * 1.7 + q * 0.31)
            xx = bx + 70 + q * 52 + slide * (46 if q < 4 + (r % 3) else 0) * smooth(clamp((cx.t - tb) / 1.0))
            f.circle(xx, yy, 19, shader=f.rad(xx - 6, yy - 6, 26, [("#F0D27A", 0.0), ("#B08A34", 1.0)]), alpha=kb)
            f.circle(xx, yy, 19, style="stroke", sw=1.8, color="#3A2610", alpha=0.7 * kb)
    # çocuklar (üç sıra masa) + hoca
    kk = cx.amt(kids_at, 0.5) if kids_at is not None else 1.0
    xs = (260, 520, 780)
    kinds = [("cocuk", "write"), ("cocuk", "count"), ("cocuk", "write")]
    for i, x in enumerate(xs):
        if kk * 1.4 - i * 0.2 <= 0.01:
            continue
        FA.actor(f, "cocuk", x, gy + 36 - i * 8, 360, cx.t, action=kinds[i][1], seed=21 + i * 3, phase=0.31 * i, alpha=clamp(kk * 1.4 - i * 0.2))
    FA.actor(f, "rahip" if False else "banker", 1010, gy + 24, 560, cx.t, action="point", dir=1, seed=33, t0=0.0, target=(160, -250), alpha=kk)
    if plate_at is not None:
        CM.name_plate(f, "HESAP OKULLARI", None, None, cx_=bx + bw / 2, y=by + bh + 40, t=cx.amt(plate_at, 0.6))
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# c1_kardes — kronikçi Villani (yazar) ve kardeşi (Peruzzi'de sayar): ip bağlanır
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c1_kardes")
def k_kardes(cx, chron_at=None, brother_at=None, link_at=None, owner_at=None, seed=5, toff=0.0, **_):
    T = cx.t + toff
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="both")
    cam.begin(f)
    gy = 900
    f.rect(-100, gy, W + 200, 300, shader=f.lin(0, gy, 0, gy + 200, [("#8A6038", 0.0), ("#563820", 1.0)]))
    for i in range(-2, 16):
        c.drawLine(i * 140, gy, i * 140 - 70, gy + 200, f.paint("#3A2410", style="stroke", sw=2.5, alpha=0.5))
    # iki masa (iki ayrı alan): sol: kronik; sağ: Peruzzi kasası
    k1 = cx.amt(chron_at, 0.6) if chron_at is not None else 1.0
    k2 = cx.amt(brother_at, 0.6) if brother_at is not None else 1.0
    if k1 > 0.003:
        FA.actor(f, "banker", 480, gy + 20, 500, T, action="write", seed=4, alpha=k1)
        CM.name_plate(f, "GIOVANNI VILLANI", "KRONİKÇİ", None, cx_=520, y=gy - 790, t=k1)
        # kronik defteri: açık kitap + yanında "borç" satırı
        OD.draw_book(c, 760, gy - 150, 150, 26, "#6A2E24", True) if False else None
    if k2 > 0.003:
        FA.actor(f, "banker", 1440, gy + 20, 500, T, action="count", dir=-1, seed=9, alpha=k2)
        # Peruzzi kalkanı: kasa üstünde asılı
        _shield(f, 1440, 350, 130, 162, "#3E5FB8", "#F0E6CC", "bars", alpha=k2, scale=1.0)
        CM.name_plate(f, "VILLANI'NİN KARDEŞİ", "PERUZZİ'DE ÇALIŞIYORDU", None, cx_=1400, y=gy - 790, t=k2, w=660)
    # ip: kronikçi → kardeş (aile bağı), üzerinde "kaybedenlerin ailesi"
    kl = cx.amt(link_at, 0.8) if link_at is not None else 0.0
    if kl > 0.003:
        a, b = (600, gy - 440), (1330, gy - 440)
        pth = skia.Path(); pth.moveTo(*a); pth.quadTo(960, gy - 700, *b)
        pm = skia.PathMeasure(pth, False)
        part = skia.Path(); pm.getSegment(0, pm.getLength() * ease_io(kl, 2.0), part, True)
        c.drawPath(part, f.paint("#A8201A", style="stroke", sw=7, alpha=0.9))
        pa = f.paint("#E8C468", style="stroke", sw=2.5, alpha=0.9)
        pa.setPathEffect(skia.DashPathEffect.Make([10, 12], -cx.t * 18))
        c.drawPath(part, pa)
    ko = cx.amt(owner_at, 0.5) if owner_at is not None else 0.0
    if ko > 0.003:
        CM.stamp(f, "KAYBEDENLERİN AİLESİNDEN", 780, 400, rot=-0.04, size=44, t=ko)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ─────────────────────────────────────────────────────────────────────────────
# c1_sokak — `sehir/sokak` sarmalayıcısı: figürlerin başlama anları çapa (at=) ile verilir
# ─────────────────────────────────────────────────────────────────────────────
cilt_cam.OWN_CAMERA.add("c1_sokak")


@ckind("c1_sokak")
def k_c1_sokak(cx, people=(), door_at=None, **kw):
    import shots as SH
    acts = []
    for d in people:
        d = dict(d)
        an = d.pop("at", None)
        d["t0"] = cx.at(an) if an is not None else d.get("t0", 0.0)
        acts.append(d)
    if door_at is not None:
        kw["door"] = "close"
        kw["door_at"] = door_at
    SH.KINDS["sehir"](cx, scene="sokak", actors=acts, **kw)


# ─────────────────────────────────────────────────────────────────────────────
# c1_yazi — "ne düşündüğünü bilmiyoruz; ne gördüğünü yazdığını biliyoruz": soru işareti söner, kalem satır yazar
# ─────────────────────────────────────────────────────────────────────────────
def _scribble(x0, x1, y, n, seed=3):
    """El yazısını andıran dalgalı iz (döngüler + eğim); noktalar listesi."""
    pts = []
    for i in range(n + 1):
        u = i / n
        x = lerp(x0, x1, u) + 18 * math.sin(u * 95 + seed) 
        yy = y + 22 * math.sin(u * 61 + seed * 2) * (0.6 + 0.4 * math.sin(u * 9)) - 10 * math.cos(u * 95 + seed)
        pts.append((x, yy))
    return pts


@ckind("c1_yazi")
def k_yazi(cx, q_at=None, q_out=None, w_at=None, w_to=None, top="NE DÜŞÜNDÜĞÜNÜ BİLMİYORUZ", bottom="NE GÖRDÜĞÜNÜ, NE YAZDIĞINI BİLİYORUZ", seed=2, **_):
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="both")
    cam.begin(f)
    col = TH.fg if TH.day else "#F0E2B8"
    # soru işareti
    kq = cx.amt(q_at, 0.5) if q_at is not None else 0.0
    if q_out is not None:
        kq *= 1.0 - cx.amt(q_out, 0.6)
    if kq > 0.003:
        f.circle(960, 400, 300, shader=f.rad(960, 400, 300, [("#F0D27A", 0.0, int(80 * kq)), ("#F0D27A", 1.0, 0)]))
        icons.draw_icon(f, "question", 960, 400, size=360 * (0.85 + 0.15 * sk.back_out(kq)), metal="gold", alpha=kq, rot=0.06 * math.sin(cx.t * 3.0), glow=0.0)
        CM.ink(f, top, 960, 650, face="title_m", size=CM.fit_size(top, "title_m", 44, 1500, 8), color=col, align="c", track=8, alpha=kq, emboss=False)
    # yazı: kalem satırı çizer
    ta = cx.at(w_at) if w_at is not None else 1e9
    tb = cx.at(w_to) if w_to is not None else ta + 2.4
    p = ease_io(clamp((cx.t - ta) / max(0.4, tb - ta)), 1.4)
    if p > 0.003:
        pts = _scribble(300, 1620, 540, 160, seed)
        m = max(2, int(len(pts) * p))
        pth = skia.Path()
        pth.moveTo(*pts[0])
        for q in pts[1:m + 1]:
            pth.lineTo(*q)
        pp = f.paint("#1E1208" if TH.day else "#E8D8A8", style="stroke", sw=5.0, alpha=0.95)
        c.drawPath(pth, pp)
        qx, qy = pts[m]
        OD.quill(c, qx + 4, qy + 6, -58.0, 1.0)
        kb = cx.amt(w_at, 0.7, off=0.3) if w_at is not None else 0.0
        CM.ink(f, bottom, 960, 740, face="title_m", size=CM.fit_size(bottom, "title_m", 42, 1560, 8), color=col, align="c", track=8, alpha=kb, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=20, light=CM.candle_light(cx.t, 2, base=(W * 0.5, H * 0.52), r=1500.0, sway=4.0))


import p1_ortak as _P  # noqa: E402
_P.add_ovl(['c1_yazi', 'c1_sokak', 'c1_okul', 'c1_kardes', 'c1_darphane', 'c1_cicek', 'c1_agi', 'c1_edward', 'c1_toprak', 'c1_lonca', 'c1_machiavelli', 'c1_kademe', 'c1_kose'])
