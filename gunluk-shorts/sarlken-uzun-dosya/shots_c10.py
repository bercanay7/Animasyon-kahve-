"""Bölüm 10 (Faturayı Kim Ödedi?) özel çekim türleri — c10_ önekli. Ton: soğuk gümüş-yeşil, defter."""
import math

import numpy as np
import skia

import icons
import kit_a as K
import shots as SH
import sk
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth, back_out

SILV = "#DCE8E6"
SILV_D = "#9FB8B4"
TEAL = "#5FA89A"


def _base(cx, rays=0.28, dust=45):
    f = cx.f
    K.bg(f, "cold")
    K.rays(f, "cold", rays)
    sk.dust(f, cx.t, n=dust, alpha=0.35, color="#CFE8E0")
    return f


def _silver_coins(f, t, n=14, alpha=0.22, seed=3):
    rs = np.random.RandomState(seed)
    for i in range(n):
        ph = (t * (0.05 + 0.04 * rs.rand()) + rs.rand()) % 1.0
        x = rs.rand() * W
        y = -40 + ph * (H + 80)
        K.coin(f, x, y, 14 + rs.rand() * 12, alpha=alpha * math.sin(math.pi * ph), rot=ph * 8, squash=abs(math.cos(ph * 14 + i)) * 0.7 + 0.3, col="#C8D2D6")


# ───────────────────────────── soru: savaşları kim ödedi? ─────────────────────────────
@SH.kind("c10_soru")
def k_c10_soru(cx, t_q=0.0):
    f = _base(cx, 0.3, 45)
    t = cx.t
    _silver_coins(f, t, 16)
    a = cx.amt(0.1, 0.8)
    qa = cx.amt(t_q, 0.6)
    K.glow_disc(f, 680, 520, 380, "#CFE8E0", 0.18 * a)
    icons.draw_icon(f, "swords", 680, 520 + math.sin(t * 1.2) * 6, size=420 * (0.9 + 0.1 * ease_out(a)), metal="silver", alpha=a, glow=0.25 * a)
    if qa > 0:
        K.glow_disc(f, 1280, 520, 420, "#F0D27A", 0.25 * qa)
        icons.draw_icon(f, "question", 1280, 520 + math.sin(t * 1.5) * 8, size=560 * (0.8 + 0.2 * back_out(qa)), metal="silver", alpha=qa, glow=0.45 * qa)
    f.vig(0.6)


# ───────────────────────────── gümüş sandık (üstü çizili) ─────────────────────────────
@SH.kind("c10_sandik")
def k_c10_sandik(cx, t_label=0.0, t_count=0.0, t_x=0.0):
    f = _base(cx, 0.3, 40)
    t = cx.t
    a = cx.amt(0.1, 0.8)
    cxw, cyw = 960, 480
    K.glow_disc(f, cxw, cyw, 360, "#CFE8E0", 0.2 * a)
    icons.draw_icon(f, "chest", cxw, cyw, size=480 * (0.92 + 0.08 * ease_out(a)), metal="silver", alpha=a, glow=0.2 * a)
    # sayma: kasaya düşen gümüş paralar
    t0 = cx.at(t_count)
    for i in range(26):
        u = clamp((t - t0 - i * 0.05) / 0.8)
        if 0 < u < 1:
            x = cxw + math.sin(i * 1.7) * 70
            y = lerp(-30, 360, u * u)
            K.coin(f, x, y, 17, alpha=1.0 if u < 0.9 else (1 - u) * 10, rot=u * 7 + i, squash=abs(math.cos(u * 10 + i)) * 0.75 + 0.25, col="#D6DFE2")
    la = cx.amt(t_label, 0.7)
    if la > 0:
        SH.gold_flat(f, "AMERİKA'NIN GÜMÜŞÜ", 960, 850 + 8 * (1 - la), face="title", size=int(64 * (0.92 + 0.08 * back_out(la))), track=12, alpha=la)
    K.x_mark(f, cxw, cyw, 250, clamp((t - cx.at(t_x)) / 0.5), sw=20, alpha=1.0)
    f.vig(0.6)


# ───────────────────────────── defter (kayıtlar) ─────────────────────────────
def _squiggle(f, x0, x1, y, rs, a, color="#1E2A2A", amp=5):
    pts = []
    n = max(3, int((x1 - x0) / 14))
    for i in range(n + 1):
        pts.append((lerp(x0, x1, i / n), y + math.sin(i * 1.9 + rs.rand() * 3) * amp * rs.rand()))
    f.path(sk.smooth_path(pts, False, 0.5), style="stroke", sw=3.2, color=color, alpha=a)


@SH.kind("c10_defter")
def k_c10_defter(cx, t_open=0.0, t_title=0.0):
    f = _base(cx, 0.25, 35)
    t = cx.t
    op = ease_out(clamp((t - cx.at(t_open)) / 0.7), 3)
    cxw, cyw, pw, ph = 960, 560, 640, 700
    rs = np.random.RandomState(7)
    for side in (-1, 1):
        w = pw * op
        x0 = cxw if side > 0 else cxw - w
        f.rrect(x0 + side * 8, cyw - ph / 2 + 12, w, ph, 10, color="#000000", alpha=0.45, blur=16)
        f.rrect(x0, cyw - ph / 2, w, ph, 8, shader=f.lin(x0 if side > 0 else x0 + w, 0, x0 + w if side > 0 else x0, 0, [("#6F8178", 0.0), ("#A9B8AA", 0.18), ("#97A698", 1.0)]))
        f.rrect(x0, cyw - ph / 2, w, ph, 8, style="stroke", sw=3, color="#3A4A44", alpha=0.8)
    if op > 0.3:
        for side in (-1, 1):
            xs, xe = (cxw + 40, cxw + pw - 40) if side > 0 else (cxw - pw + 40, cxw - 40)
            for r in range(13):
                y = cyw - ph / 2 + 80 + r * 46
                f.line(xs, y, xe, y, color="#4A5A52", sw=1.4, alpha=0.5 * op)
            f.line(lerp(xs, xe, 0.62), cyw - ph / 2 + 50, lerp(xs, xe, 0.62), cyw + ph / 2 - 40, color="#B04848", sw=1.6, alpha=0.5 * op)
        for side in (-1, 1):
            for r in range(13):
                ta = clamp((t - cx.at(t_open, off=0.5 + r * 0.075 + (0.0 if side < 0 else 0.04))) / 0.4)
                if ta <= 0:
                    continue
                xs = cxw + (40 if side > 0 else -pw + 40)
                y = cyw - ph / 2 + 80 + r * 46 - 8
                rs2 = np.random.RandomState(r * 7 + (3 if side > 0 else 1))
                w_ = (pw - 80) * 0.5 * ta
                _squiggle(f, xs, xs + w_, y, rs2, 0.8, amp=5)
                if ta > 0.7:
                    _squiggle(f, xs + (pw - 80) * 0.66, xs + (pw - 80) * 0.66 + 80 * (ta - 0.7) / 0.3, y, rs2, 0.9, amp=4)
    # sırt
    f.rect(cxw - 6, cyw - ph / 2, 12, ph, shader=f.lin(cxw - 6, 0, cxw + 6, 0, [("#1B2A27", 0.0), ("#5A6A62", 0.5), ("#1B2A27", 1.0)]), alpha=op)
    ta = cx.amt(t_title, 0.5)
    if ta > 0:
        K.txt(f, "KAYITLAR", 960, 130, face="title", size=58, color=SILV, track=18, alpha=ta)
    # kalem
    qx = lerp(cxw - 250, cxw + 250, clamp((t - cx.at(t_open, off=0.5)) / 1.2))
    qy = cyw + ph / 2 - 330 + math.sin(t * 8) * 6
    icons.draw_icon(f, "quill", qx + 90, qy - 40, size=170, metal="ivory", alpha=op, rot=0.5)
    f.vig(0.6)


_PILE = K.pile_spec(n=130, seed=11, width=520.0, height=170.0, rmin=15, rmax=21)


# ───────────────────────────── 35 yıl / çoğu vergi ─────────────────────────────
@SH.kind("c10_sayac")
def k_c10_sayac(cx, t_num=0.0, t_label=0.0, t_tax=0.0):
    f = _base(cx, 0.3, 45)
    t = cx.t
    na = cx.amt(t_num, 0.5, off=-0.15)
    v = 35 * ease_out(clamp((t - cx.at(t_num)) / 0.9), 3)
    K.draw_pile(f, 960, 1040, ease_out(clamp(t / (cx.dur * 0.9)), 2), _PILE, alpha=0.5, scale=1.55, col="#C9B27A")
    K.glow_disc(f, 960, 450, 420, "#CFE8E0", 0.16 * na)
    if na > 0:
        SH.gold_flat(f, f"{int(round(v))}", 880, 560, face="title", size=300, track=10, alpha=na)
        SH.gold_flat(f, "YIL", 1210, 560, face="title", size=120, track=14, alpha=na, align="l")
    la = cx.amt(t_label, 0.6)
    if la > 0:
        K.txt(f, "olağanüstü gelirler", 960, 700, face="cap_i", size=64, color=SILV, alpha=la)
    ta = cx.amt(t_tax, 0.5)
    if ta > 0:
        yy = 860 + 8 * (1 - ta)
        wd = 700
        SH.plate(f, 960 - wd / 2, yy - 68, wd, 116, alpha=ta, corner=18, edge="#9FB8B4")
        icons.draw_icon(f, "coins", 960 - wd / 2 + 82, yy - 8, size=84, metal="silver", alpha=ta, shadow=False)
        f.text("ÇOĞU: VERGİ", 960 + 44, yy + 14, face="title_m", size=46, color=SILV, align="c", track=10, alpha=ta, shadow=(2, 2, 3, "#000000"))
    f.vig(0.6)


# ───────────────────────────── çubuklar: Alçak Ülkeler / Kastilya / Napoli ─────────────────────────────
@SH.kind("c10_bars")
def k_c10_bars(cx, items=(), t_unit=0.0, maxv=10.5):
    """items: [dict(label, value, color, t0, t1, text)] — t0: çubuk başlar, t1: değer yazısı."""
    f = _base(cx, 0.25, 40)
    t = cx.t
    x0, w, bh, gap = 600, 880, 96, 70
    n = len(items)
    y0 = 540 - (n * bh + (n - 1) * gap) / 2 + 20
    sc = 1.0 + 0.05 * cx.u
    f.c.save()
    f.c.translate(960, 540)
    f.c.scale(sc, sc)
    f.c.translate(-960, -540)
    ua = cx.amt(t_unit, 0.6)
    K.txt(f, "OLAĞANÜSTÜ GELİRLER · DÜKAT", 960, 150, face="title_m", size=34, color=SILV_D, track=10, alpha=smooth(t / 0.6) * (0.55 + 0.45 * ua))
    for i, it in enumerate(items):
        y = y0 + i * (bh + gap)
        a = cx.amt(it["t0"], 0.5)
        if a <= 0:
            continue
        k = ease_out(clamp((t - cx.at(it["t0"], off=0.1)) / 1.6), 3)
        col = it["color"]
        f.text(it["label"], x0 - 36, y + bh * 0.66, face="title_m", size=38, color=SILV, align="r", track=5, alpha=a, shadow=(2, 2, 3, "#000000"))
        f.rrect(x0, y, w, bh, 14, color="#000000", alpha=0.4 * a)
        bw = max(6.0, w * it["value"] / maxv * k)
        f.rrect(x0, y, bw, bh, 14, shader=f.lin(0, y, 0, y + bh, [(mix(col, "#FFFFFF", 0.3), 0.0), (col, 0.5), (mix(col, "#000000", 0.4), 1.0)]), alpha=a)
        f.rrect(x0, y, bw, bh, 14, style="stroke", sw=2.5, color=mix(col, "#FFFFFF", 0.55), alpha=0.8 * a)
        gx = x0 + ((t * 300 + i * 90) % (bw + 160)) - 80
        f.c.save()
        f.c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, y, bw, bh), 14, 14), skia.ClipOp.kIntersect, True)
        f.rect(gx - 30, y, 60, bh, shader=f.lin(gx - 30, 0, gx + 30, 0, [("#FFFFFF", 0.0, 0), ("#FFFFFF", 0.5, 70), ("#FFFFFF", 1.0, 0)]))
        f.c.restore()
        va = cx.amt(it["t1"], 0.5)
        if va > 0:
            f.text(it["text"], x0 + bw + 26, y + bh * 0.67, face="title_m", size=44, color="#F6E7B0", align="l", alpha=va, shadow=(2, 2, 3, "#000000"))
    f.c.restore()
    f.vig(0.6)


# ───────────────────────────── gümüş akışı eğrisi + Potosí ─────────────────────────────
def _sig(x):
    return 1 / (1 + math.exp(-x))


def _flow(yr):
    """ŞEMATİK gümüş akışı (veri değildir): hükümdarlık boyunca düşük, sonra sert yükselir."""
    return 0.035 + 0.07 * _sig((yr - 1542) / 9) + 0.9 * _sig((yr - 1578) / 10) ** 1.6


@SH.kind("c10_egri")
def k_c10_egri(cx, t_flow=0.0, t_boom=0.0, t_after=0.0, t_potosi=0.0, t_year=0.0):
    f = _base(cx, 0.25, 40)
    t = cx.t
    ax0, ax1, ay = 230, 1700, 820
    ph = 560

    def X(yr):
        return lerp(ax0, ax1, (yr - 1500) / 100.0)

    def Y(v):
        return ay - v * ph

    a = smooth(t / 0.6)
    # Şarlken dönemi bandı
    f.rect(X(1519), ay - ph - 40, X(1556) - X(1519), ph + 40, color="#C9962B", alpha=0.12 * a)
    f.line(X(1519), ay - ph - 40, X(1519), ay, color="#C9962B", sw=2, alpha=0.5 * a)
    f.line(X(1556), ay - ph - 40, X(1556), ay, color="#C9962B", sw=2, alpha=0.5 * a)
    K.txt(f, "ŞARLKEN DÖNEMİ", (X(1519) + X(1556)) / 2, ay - ph + 10, face="title_m", size=28, color="#E0C682", track=8, alpha=a)
    for yr in (1519, 1556):
        K.txt(f, str(yr), X(yr), ay + 52, face="title_m", size=30, color="#CDBB86", track=3, alpha=a)
    f.line(ax0, ay, ax1 + 40, ay, color="#9FB8B4", sw=3, alpha=0.8 * a)
    f.line(ax0, ay, ax0, ay - ph - 40, color="#9FB8B4", sw=3, alpha=0.5 * a)
    # eğri (ilerleme: 1500→1556 yavaş; sonrası patlama)
    p1 = ease_out(clamp((t - cx.at(t_flow)) / 1.5), 2)
    p2 = ease_in(clamp((t - cx.at(t_boom)) / 1.5), 2)
    yr_end = 1500 + p1 * 56 + p2 * 44
    n = 90
    pts = []
    for i in range(n + 1):
        yr = 1500 + i * (yr_end - 1500) / n
        pts.append((X(yr), Y(_flow(yr))))
    if len(pts) > 2 and yr_end > 1501:
        path = sk.smooth_path(pts, False, 0.3)
        fill = skia.Path(path)
        fill.lineTo(pts[-1][0], ay)
        fill.lineTo(pts[0][0], ay)
        fill.close()
        f.path(fill, shader=f.lin(0, ay - ph, 0, ay, [("#CFE8E0", 0.0, 90), ("#CFE8E0", 1.0, 5)]))
        f.path(path, style="stroke", sw=14, color="#CFE8E0", alpha=0.2, blur=8)
        f.path(path, style="stroke", sw=6, color="#EAF3F1")
        hx, hy = pts[-1]
        K.glow_disc(f, hx, hy, 46, "#FFFFFF", 0.7)
    la = cx.amt(t_flow, 0.6, off=-0.2)
    K.txt(f, "GÜMÜŞ AKIŞI", ax0 + 20, ay - ph - 62, face="title_m", size=36, color=SILV, align="l", track=8, alpha=la)
    ba = cx.amt(t_after, 0.6)
    if ba > 0:
        K.tag(f, "ASIL PATLAMA: SONRA", X(1583), Y(0.62) - 40 * (1 - ba), alpha=ba, size=36, align="c", pad=26, edge="#9FB8B4")
    # Potosí
    pa = cx.amt(t_potosi, 0.7)
    if pa > 0:
        mx, my = X(1545), Y(_flow(1545)) - 120
        f.line(mx, my + 60, mx, ay, color="#F0D27A", sw=2.5, alpha=0.8 * pa)
        K.glow_disc(f, mx, my, 150, "#CFE8E0", 0.25 * pa)
        icons.draw_icon(f, "c10_dag", mx, my, size=190 * (0.85 + 0.15 * back_out(pa)), metal="silver", alpha=pa, glow=0.3 * pa)
        K.tag(f, "POTOSÍ", mx, my - 118, alpha=pa, size=36, align="c", pad=24, edge="#9FB8B4")
    ya = cx.amt(t_year, 0.5)
    if ya > 0:
        mx = X(1545)
        SH.gold_flat(f, "1545", mx, ay + 130, face="title", size=int(62 * (0.9 + 0.1 * back_out(ya))), track=8, alpha=ya)
    K.txt(f, "ŞEMATİK ÇİZİM", ax1 + 40, ay + 118, face="cap_i", size=26, color=SILV_D, align="r", alpha=0.7 * a)
    f.vig(0.6)


# ───────────────────────────── Fugger'in mektubu ─────────────────────────────
@SH.kind("c10_mektup")
def k_c10_mektup(cx, lines=(), t_summary=0.0, t_seal=None, w=1180, h=620):
    f = _base(cx, 0.22, 35)
    t = cx.t
    img, pad = SH.paper_sprite(w, h, seed=29, tone="#CDBB90")
    a = cx.amt(0.0, 0.7)
    sc = (1.0 + 0.05 * cx.u) * (0.96 + 0.04 * ease_out(a))
    f.c.save()
    f.c.translate(W / 2, H * 0.5)
    f.c.rotate(math.degrees(-0.012 * (1 - 0.4 * cx.u)))
    f.c.scale(sc, sc)
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(a)
    f.c.drawImage(img, -w / 2 - pad, -h / 2 - pad, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    ink = "#1E2A2A"
    f.text("FUGGER'İN MEKTUBU · 1523", 0, -h / 2 + 92, face="fell", size=52, color=ink, align="c", track=2, alpha=a * cx.amt(0.3, 0.5))
    f.line(-w * 0.34, -h / 2 + 112, w * 0.34, -h / 2 + 112, color=ink, sw=1.6, alpha=0.6 * a)
    y = -h / 2 + 200
    for i, (txt, anc) in enumerate(lines):
        ti = cx.at(anc)
        prog = clamp((t - ti) / 0.6)
        if prog > 0:
            wt = sk.text_width(txt, "fell", 48, 0)
            f.c.save()
            f.c.clipRect(skia.Rect.MakeXYWH(-w / 2 + 80, y - 56, (wt + 24) * prog, 90))
            f.text(txt, -w / 2 + 90, y, face="fell", size=48, color=ink, align="l", alpha=a)
            f.c.restore()
        y += 96
    # özet etiketi
    sa = cx.amt(t_summary, 0.4)
    if sa > 0:
        f.rrect(w / 2 - 190, -h / 2 + 38, 150, 58, 10, style="stroke", sw=3, color="#8E1F26", alpha=0.85 * sa)
        f.text("ÖZET", w / 2 - 115, -h / 2 + 78, face="title", size=32, color="#8E1F26", align="c", track=8, alpha=0.9 * sa)
        f.text("kelimesi kelimesine değil", w / 2 - 50, -h / 2 + 158, face="fell_i", size=28, color=ink, align="r", alpha=0.8 * sa)
    if t_seal is not None:
        SH.wax_seal(f, w / 2 - 150, h / 2 - 96, 58, color="#2F5232", t=cx.amt(t_seal, 0.35), alpha=a, mono="F")
    f.c.restore()
    f.vig(0.55)


# ───────────────────────────── uçurum: devletin borcu ─────────────────────────────
@SH.kind("c10_ucurum")
def k_c10_ucurum(cx, t_year=0.0, t_crown=0.0, t_debt=0.0, t_edge=0.0):
    f = _base(cx, 0.22, 35)
    t = cx.t
    ya = cx.amt(t_year, 0.6)
    edge_x, top_y = 1180, 650
    # boşluk (uçurum): koyu degrade + düşen paralar
    f.rect(edge_x, 0, W - edge_x, H, shader=f.lin(0, 0, 0, H, [("#04090A", 0.0), ("#0A1616", 1.0)]))
    for i in range(10):
        ph = (t * (0.18 + 0.05 * (i % 3)) + i * 0.13) % 1.0
        K.coin(f, edge_x + 80 + (i * 61) % 560, 300 + ph * 820, 14 + (i % 3) * 3, alpha=0.5 * (1 - ph) * smooth((t - cx.at(t_edge, off=-0.2)) / 0.5), rot=ph * 9 + i, squash=abs(math.cos(ph * 12 + i)) * 0.7 + 0.3, col="#C8D2D6")
    f.circle(edge_x + 330, H + 40, 520, shader=f.rad(edge_x + 330, H + 40, 520, [("#B02A2A", 0.0, int(70 * smooth((t - cx.at(t_edge, off=-0.3)) / 0.8))), ("#B02A2A", 1.0, 0)]), blend=skia.BlendMode.kPlus)
    # zemin (plato) ve kaya yüzü
    f.rect(0, top_y, edge_x, H - top_y, shader=f.lin(0, top_y, 0, H, [("#1A2A28", 0.0), ("#0A1413", 1.0)]))
    f.line(0, top_y, edge_x, top_y, color="#9FB8B4", sw=3, alpha=0.5)
    f.path(sk.poly_path([(edge_x, top_y), (edge_x + 40, top_y + 160), (edge_x - 10, top_y + 360), (edge_x + 30, H + 20), (edge_x - 120, H + 20), (edge_x - 120, top_y)], True), color="#0C1716")
    f.line(edge_x, top_y, edge_x + 40, top_y + 160, color="#9FB8B4", sw=2, alpha=0.4)
    # borç sütunları (defter yığınları): soldan sağa yükselen, kırmızıya dönen
    n = 8
    da = cx.amt(t_debt, 0.5, off=-0.6)
    for i in range(n):
        k = ease_out(clamp((t - cx.at(t_debt, off=-0.5 + i * 0.12)) / 0.9), 3)
        if k <= 0:
            continue
        hgt = (40 + i ** 1.7 * 8) * k
        bx = 150 + i * 118
        col = mix("#7FA8A0", "#B02A2A", i / (n - 1))
        f.rect(bx, top_y - hgt, 86, hgt, shader=f.lin(bx, 0, bx + 86, 0, [(mix(col, "#000000", 0.4), 0.0), (mix(col, "#FFFFFF", 0.15), 0.4), (mix(col, "#000000", 0.45), 1.0)]), alpha=0.95)
        f.rect(bx, top_y - hgt, 86, hgt, style="stroke", sw=2, color=mix(col, "#FFFFFF", 0.4), alpha=0.7)
        for r in range(int(hgt / 38)):
            f.line(bx + 8, top_y - 22 - r * 38, bx + 78, top_y - 22 - r * 38, color="#000000", sw=1.4, alpha=0.3)
    if da > 0:
        K.txt(f, "DEVLETİN BORCU", 560, top_y + 120, face="title_m", size=42, color="#E7D5A0", track=10, alpha=da)
    # taç: kenarda, uçuruma doğru eğilir
    ca = cx.amt(t_crown, 0.7)
    if ca > 0:
        tilt = 0.14 * smooth((t - cx.at(t_edge)) / 1.2) + 0.012 * math.sin(t * 3)
        cxw = 150 + 7 * 118 + 60
        cyw = top_y - (40 + 7 ** 1.7 * 8) - 130 - 20 * (1 - ca)
        K.glow_disc(f, cxw, cyw, 230, "#F0D27A", 0.35 * ca)
        icons.draw_icon(f, "imperial_crown", cxw, cyw, size=300, metal="gold", alpha=ca, rot=tilt, glow=0.4 * ca)
    if ya > 0:
        SH.gold_flat(f, "1556", 330, 190, face="title", size=96, track=14, alpha=ya)
    f.vig(0.6)


# ───────────────────────────── kapanış: altınla değil, borçla ayakta ─────────────────────────────
@SH.kind("c10_kapanis")
def k_c10_kapanis(cx, t_gold=0.0, t_not=0.0, t_debt=0.0):
    f = _base(cx, 0.28, 40)
    t = cx.t
    ga = cx.amt(t_gold, 0.7)
    fade_gold = 1 - smooth((t - cx.at(t_not, off=-0.05)) / 0.9)       # altın sütunu söner
    dk = ease_out(clamp((t - cx.at(t_debt, off=-0.1)) / 0.9), 3)       # borç sütunu (defter yığını) belirir
    bx, base = 960, 930
    n_coin = 20
    cstep = 22
    top_y = base - n_coin * cstep
    # altın para sütunu
    if ga * fade_gold > 0.01:
        for i in range(n_coin):
            kk = smooth(clamp((t - cx.at(t_gold, off=i * 0.03)) / 0.4))
            tarn = smooth((t - cx.at(t_not)) / 0.8)
            K.coin(f, bx, base - i * cstep, 150, alpha=kk * fade_gold, squash=0.26, col=mix("#E3B54A", "#7A8680", tarn))
    # defter yığını
    if dk > 0:
        books = 9
        bh_ = (base - top_y) / books
        for i in range(books):
            kk = ease_out(clamp(dk * 1.4 - i * 0.07))
            if kk <= 0:
                continue
            wdt = 300 - (i % 3) * 14
            yy = base - (i + 1) * bh_ + bh_ * (1 - kk) * 40
            col = mix("#B02A2A", "#6F1A1A", (i % 3) / 3.0)
            xo = ((i * 37) % 31) - 15
            f.rrect(bx - wdt / 2 + xo, yy, wdt, bh_ - 3, 5, shader=f.lin(0, yy, 0, yy + bh_, [(mix(col, "#FFFFFF", 0.18), 0.0), (col, 0.5), (mix(col, "#000000", 0.4), 1.0)]), alpha=kk)
            f.rrect(bx - wdt / 2 + xo, yy, wdt, bh_ - 3, 5, style="stroke", sw=2, color="#E3B54A", alpha=0.6 * kk)
            f.rect(bx - wdt / 2 + xo + 22, yy + 7, 14, bh_ - 17, color="#E3B54A", alpha=0.5 * kk)
    # taç
    cy_ = top_y - 130 + math.sin(t * 2.2) * 4
    sway = 0.03 * math.sin(t * 2.7) * (0.4 + 0.6 * dk)
    K.glow_disc(f, bx, cy_, 260, "#F0D27A", 0.35)
    icons.draw_icon(f, "imperial_crown", bx, cy_, size=340, metal="gold", alpha=1.0, rot=sway, glow=0.4)
    # üstü çizili altın ve BORÇ damgası
    sa = cx.amt(t_not, 0.5)
    if sa > 0 and dk < 0.5:
        K.x_mark(f, bx, base - 170, 220, clamp((t - cx.at(t_not)) / 0.5), sw=18, alpha=sa * (1 - dk * 2))
    SH.stamp(f, "BORÇ", 1420, 560, rot=-0.1, size=130, t=cx.amt(t_debt, 0.3, off=-0.05))
    f.vig(0.62)
