"""c3_kinds — c3 «Kule ve Sürgün» özel çekim türleri (Parça 2 sahne yazarı). `scenes_c3.py` içinde import edilir; `@CM.ckind` ile kaydolur.

Dünya koordinatı = nötr kamerada ekran koordinatı (1920×1080). Kamera: `cam=[(çapa, look(wx, wy, z)), …]` (look: dünya noktasını ekran merkezine alan anahtar kare).
Kaynak disiplini: yüz yok (siluet), şiddet yok; ekrana yalnız script sözcükleri (Alberghettino, Küçük Han, Guadagni, Albizzi …).
"""
import math

import numpy as np
import skia

import cilt_city as CT
import cilt_medici as CM
import cilt_sehir as SE
import icons
import p2_lib as L
import sk
from cilt_medici import TH
from p2_lib import (INK, P, S, GRAD_V, INKP, INKR, LINE, OVAL, POLY, R, RA, SOFT, FILLP, PT, STK, _RS, bake, blit, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth)
from sk import C, H, W


def look(wx, wy, z=1.0, rot=0.0):
    """Anahtar kare: dünya (wx,wy) noktası ekran merkezinde, zoom z."""
    return (z * (wx - W / 2), z * (wy - H / 2), z, rot)


# ═══════════════════════════ kule: Duomo'suz dikey şehir (1433'te kubbe tamamlanmamıştı) ═══════════════════════════
def draw_dome_wip(c, x, y, w, drum_h, T, depth=0.0, u=0.42):
    """Yapım hâlindeki kubbe: tambur + kısmen örülmüş kabuk (u: yükseklik oranı) + küçük vinç. (Fener/haç YOK.)"""
    marble = T("#EFE5CC", depth)
    green = T("#6E9878", depth)
    R(c, x - w * 0.47, y - drum_h, x + w * 0.47, y, marble)
    for k in range(4):
        R(c, x - w * 0.47, y - drum_h + drum_h * (0.22 + 0.22 * k), x + w * 0.47, y - drum_h + drum_h * (0.22 + 0.22 * k) + 2.4, green, 200)
    for dx in (-0.24, 0.0, 0.24):
        c.drawOval(skia.Rect.MakeXYWH(x + dx * w - w * 0.045, y - drum_h * 0.62, w * 0.09, drum_h * 0.34), skia.Paint(AntiAlias=True, Color=C(T("#3A2A1C", depth), 210)))
    c.drawRect(skia.Rect.MakeLTRB(x - w * 0.47, y - drum_h, x + w * 0.47, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#2A1A0C", 150)))
    yb = y - drum_h
    hd = w * 0.62
    ht = hd * u
    tile = T("#C65B33", depth)
    path = skia.Path()
    path.moveTo(x - w * 0.47, yb)
    # kabuğun yarım profili (u oranına kadar)
    n = 14
    pts_l, pts_r = [], []
    for k in range(n + 1):
        t = k / n * u
        ex = w * 0.47 * math.cos(t * math.pi / 2 * 0.95)
        ey = hd * math.sin(t * math.pi / 2 * 0.95) * 1.0
        pts_l.append((x - ex, yb - ey))
        pts_r.append((x + ex, yb - ey))
    poly = pts_l + pts_r[::-1]
    c.drawPath(sk.poly_path(poly), skia.Paint(AntiAlias=True, Color=C(tile)))
    c.drawPath(sk.poly_path(poly), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C("#2A1A0C", 170)))
    for k in range(1, 5):
        ty = yb - ht * k / 5.0
        c.drawLine(x - w * 0.4, ty, x + w * 0.4, ty, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#5A2412", 70)))
    # küçük vinç (direk + kol)
    ty = yb - ht
    cxr = x + w * 0.12
    c.drawLine(cxr, ty, cxr, ty - 96, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.0, Color=C("#4A3220")))
    c.drawLine(cxr - 8, ty - 94, cxr + 62, ty - 86, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6, Color=C("#4A3220")))
    c.drawLine(cxr + 60, ty - 86, cxr + 60, ty - 30, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#2A1A0C", 200)))


class DikeyP2(SE.SkylineDikey):
    """SkylineDikey'in Duomo'suz kopyası: yalnız `city` katmanı (kubbe yerine yapım hâlindeki tambur). Önbellek adı ayrı (`sehir_dikey_p2`)."""
    name = "sehir_dikey_p2"

    def _draw_city_v(self, fr, r0, r1):
        c = fr.c
        T = self.T
        LH = 900
        rr = SE._RS(5)
        wins = []
        x = -40
        while x < SE.VLW + 40:
            bw, bh = rr.uniform(44, 94), rr.uniform(34, 84)
            rs = SE._RS(int(rr.randint(1, 10 ** 6)))
            CT.draw_house(c, x, LH - 120 + (rs.rand() * 8 - 4), bw, bh, rs, T, 0.40, wins)
            x += bw + rr.uniform(-6, 8)
        base = LH - 124
        XD = 700
        c.save()
        c.translate(XD, base)
        c.scale(1.5, 1.5)
        c.translate(-XD, -base)
        CT.draw_nave(c, XD + 70, XD + 640, base + 4, 124, T, 0.26)
        draw_dome_wip(c, XD, base - 108, 214, 48, T, 0.22, u=0.38)
        CT.draw_campanile(c, XD + 205, base + 4, 54, 262, T, 0.22)
        c.restore()
        for tx, th in ((200, 210), (1500, 250), (1860, 180), (2150, 220)):
            CT.draw_tower(c, tx, base, 32, th, T, 0.32, spire=(tx == 1500))
        SE.GRAD_V(c, 0, LH - 124, SE.VLW, LH + 800, [(T("#B8A888", 0.35), 0.0), (T("#A89A78", 0.30), 1.0)])
        rs2 = SE._RS(61)
        for i in range(int(SE.VLW / 70)):
            hx = i * 70 + rs2.uniform(-10, 10)
            hy = LH - 110 + rs2.uniform(0, 600)
            bw_, bh_ = rs2.uniform(50, 100), rs2.uniform(30, 60)
            CT.draw_house(c, hx, hy, bw_, bh_, SE._RS(int(rs2.randint(1, 10 ** 6))), T, 0.34, wins)
        if self.tod != "day":
            SE.PN._lit_boxes(c, SE._RS(21), wins, True, 0.4 if self.tod == "night" else 0.16)


SE.CLASSES[("skyline_dikey_p2", None)] = DikeyP2
SE.DEFAULT_ACT["skyline_dikey_p2"] = None

# kule gövdesindeki yarıkların dünya yükseklikleri (SkylineDikey: base+260 + 380k) ve x'leri (VX ± 0,26·VTW)
SLIT_H = [740 + 380 * k for k in range(9)]
SLIT_X_R = SE.VX + SE.VTW * 0.26
SLIT_X_L = SE.VX - SE.VTW * 0.26


# ═══════════════════════════ hücre (Alberghettino): dar yarık, ışık huzmesi, oyma yazı ═══════════════════════════
SLIT = dict(x=1490.0, y0=330.0, y1=585.0, w=34.0)


def _cell_wall(fr, T):
    """Taş duvar + zemin (pişirilmiş katman 2900×1500; dünya x −500…2400, y −300…1200)."""
    c = fr.c
    c.translate(500, 300)
    xa, xb = -500, 2420
    R(c, xa, -300, xb, 810, T("#7D786E"))
    L.OD.ashlar(c, xa, xb, -300, 810, T, col="#7D786E", course=70.0, seed=5)
    # alt duvar kalınlığı: zemin çizgisi
    GRAD_V(c, xa, 700, xb, 812, [("#000000", 0.0, 0), ("#000000", 1.0, 70)])
    R(c, xa, 804, xb, 822, T("#5A564E"))
    c.drawLine(xa, 806, xb, 806, S("#1E1A14", 2.0, 190))
    # zemin: taş döşeme (derinlik)
    GRAD_V(c, xa, 822, xb, 1200, [("#6E6A60", 0.0), ("#4A463E", 1.0)])
    rs = _RS(9)
    y = 822.0
    row = 0
    hrow = 22.0
    while y < 1200:
        c.drawLine(xa, y, xb, y, S("#1E1A14", 1.2, 150))
        off = (row % 2) * 60
        x = xa - off
        wslab = 96 + row * 11
        while x < xb:
            c.drawLine(x, y, x - (x - 960) * 0.05 * (hrow / 22.0), y + hrow, S("#1E1A14", 1.0, 120))
            x += wslab
        # tek tek taş tonu
        for k in range(int((xb - xa) / wslab) + 2):
            if rs.rand() < 0.35:
                x0 = xa - off + k * wslab
                c.drawRect(skia.Rect.MakeLTRB(x0 + 3, y + 2, x0 + wslab - 3, y + hrow - 1), P("#FFFFFF" if rs.rand() < 0.5 else "#000000", 14))
        y += hrow
        hrow *= 1.14
        row += 1
    # duvar lekeleri/çatlak
    for i in range(14):
        x0, y0 = rs.uniform(xa, xb), rs.uniform(-200, 700)
        SOFT(c, x0, y0, rs.uniform(60, 190), rs.uniform(30, 90), "#2A261E", rs.uniform(14, 38))
    for i in range(5):
        x0, y0 = rs.uniform(200, 1800), rs.uniform(80, 560)
        pp = skia.Path()
        pp.moveTo(x0, y0)
        for k in range(1, 5):
            pp.lineTo(x0 + rs.uniform(-22, 22), y0 + k * rs.uniform(18, 34))
        c.drawPath(pp, S("#1E1A14", 1.3, 110))


def draw_slit(c, cx_t, x, y0, y1, w, open_k=1.0, glow=1.0, t=0.0):
    """Duvarda dar yarık: kalın duvar (içe doğru genişleyen eğik yüzler) + parlayan gökyüzü + ışıma. (x merkez, y0 üst, y1 alt, w yarık genişliği)."""
    sp = 62.0                                       # iç yüzde genişleme
    hh = y1 - y0
    # eğik yüzler (duvar kalınlığı): koyu
    left = [(x - w / 2, y0), (x - w / 2 - sp, y0 - 34), (x - w / 2 - sp, y1 + 34), (x - w / 2, y1)]
    right = [(x + w / 2, y0), (x + w / 2 + sp * 0.78, y0 - 34), (x + w / 2 + sp * 0.78, y1 + 34), (x + w / 2, y1)]
    top = [(x - w / 2, y0), (x + w / 2, y0), (x + w / 2 + sp * 0.78, y0 - 34), (x - w / 2 - sp, y0 - 34)]
    bot = [(x - w / 2, y1), (x + w / 2, y1), (x + w / 2 + sp * 0.78, y1 + 34), (x - w / 2 - sp, y1 + 34)]
    c.drawPath(sk.poly_path(left), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(x - w / 2 - sp, 0), (x - w / 2, 0)], [C("#4C483F"), C("#CFC8B0")], [0, 1])))
    c.drawPath(sk.poly_path(right), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(x + w / 2 + sp * 0.78, 0), (x + w / 2, 0)], [C("#2A2822"), C("#8A8470")], [0, 1])))
    c.drawPath(sk.poly_path(top), P("#34312B"))
    c.drawPath(sk.poly_path(bot), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, y1), (0, y1 + 34)], [C("#E8E0C4"), C("#6E6A58")], [0, 1])))
    for pts in (left, right, top, bot):
        INKP(c, sk.poly_path(pts), 1.6, 190)
    # yarığın kendisi: parlak gök
    sky = skia.GradientShader.MakeLinear([(0, y0), (0, y1)], [C("#CFE2F2"), C("#FFF6DC")], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, y0, x + w / 2, y1), skia.Paint(Shader=sky))
    # dışarıdan geçen kuş (silik)
    ph = (t * 0.12) % 1.0
    by = y0 + 30 + ph * (hh - 60)
    c.drawLine(x - 7, by, x + 7, by + math.sin(t * 9) * 3, S("#4A4034", 2.0, 170))
    # ışıma
    if glow > 0:
        SOFT(c, x, (y0 + y1) / 2, 150, hh * 0.78, "#FFF2C8", 95 * glow)


def draw_beam(c, x, ybot, floor_y, dx_floor, t, a=1.0, w_top=34.0, seed=3):
    """Yarıktan zemine eğik ışık huzmesi (toz zerreleriyle). (x, ybot) = yarığın alt orta noktası; huzme sola-aşağı iner."""
    k = 0.90 + 0.10 * math.sin(t * 0.4) + 0.04 * math.sin(t * 1.3 + 1)
    xf0, xf1 = x - dx_floor - 12, x - dx_floor + 118
    poly = [(x - w_top / 2, ybot), (x + w_top / 2, ybot), (xf1, floor_y), (xf0, floor_y)]
    sh = skia.GradientShader.MakeLinear([(x, ybot), ((xf0 + xf1) / 2, floor_y)], [C("#FFF3CE", int(150 * a * k)), C("#FFE8B0", int(70 * a * k)), C("#FFE8B0", int(30 * a * k))], [0.0, 0.55, 1.0])
    c.drawPath(sk.poly_path(poly), skia.Paint(AntiAlias=True, Shader=sh))
    # kenar çizgileri (ince, parlak)
    c.drawLine(x - w_top / 2, ybot, xf0, floor_y, S("#FFF8E0", 1.4, 60 * a))
    c.drawLine(x + w_top / 2, ybot, xf1, floor_y, S("#FFF8E0", 1.0, 40 * a))
    # zemin lekesi
    SOFT(c, (xf0 + xf1) / 2, floor_y + 12, (xf1 - xf0) * 0.78, 26, "#FFF0C0", 110 * a * k)
    # toz
    rs = _RS(seed)
    for i in range(30):
        ph = (t * (0.06 + 0.04 * rs.rand()) + rs.rand()) % 1.0
        u = ph
        px = lerp(x + rs.uniform(-w_top / 2, w_top / 2), lerp(xf0, xf1, rs.rand()), u) + math.sin(t * 0.8 + i) * 6
        py = lerp(ybot, floor_y, u) + math.cos(t * 0.6 + i * 1.7) * 5
        al = math.sin(math.pi * u) * (0.35 + 0.65 * abs(math.sin(t * 1.1 + i * 2.1)))
        c.drawCircle(px, py, 1.4 + 1.6 * rs.rand(), P("#FFF6D8", 200 * al * a))


def inn_sign(c, x, y, t, k=1.0, t_hit=0.0):
    """Duvara çakılı demir kol + sallanan han tabelası (yatak simgesi) — 'Küçük Han' adının tutukevi için fazla konuksever oluşu (mizah). x,y = kolun duvara bağlandığı nokta."""
    if k <= 0.003:
        return
    arm = 150.0
    # kol
    ap = skia.Path()
    ap.moveTo(x, y)
    ap.lineTo(x + arm, y)
    c.drawPath(ap, S("#1E1A14", 8, 255 * k))
    c.drawPath(ap, S("#4A4640", 4, 255 * k))
    c.drawCircle(x, y, 10, P("#2A2620", 255 * k))
    # sarkaç (damped)
    dt = max(0.0, t - t_hit)
    ang = math.sin(dt * 5.2) * math.exp(-dt * 0.9) * 0.34 * k
    sc = 0.2 + 0.8 * sk.back_out(clamp(dt / 0.35)) if dt < 0.35 else 1.0
    px, py = x + arm - 14, y
    c.save()
    c.translate(px, py)
    c.rotate(math.degrees(ang))
    c.scale(sc, sc)
    for cxo in (-34, 34):
        c.drawLine(cxo, 0, cxo, 40, S("#2A2620", 3.0, 255 * k))
    # levha
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-60, 40, 60, 132), 10, 10)
    c.drawRRect(rr, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 40), (0, 132)], [C("#E2C48A", int(255 * k)), C("#B48A4C", int(255 * k))], [0, 1])))
    c.drawRRect(rr, S("#3A2410", 3.0, 255 * k))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-52, 48, 52, 124), 6, 6), S("#6A4620", 1.4, 200 * k))
    c.restore()


def k_hucre_impl(cx, sil_at=0.0, name_at=("c3s2", "Alberghettino", 0.0), han_at=("c3s2", "Küçük", 0.0), sign_at=("c3s3", "konuksever", 0.0), seed=1, **_):
    f = cx.f
    c = f.c
    t = cx.t
    f.clear("#0B0A08")
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    T = L.OD.OTint("day")
    im = bake(("hucre_wall", 1), 2920, 1500, lambda fr: _cell_wall(fr, T))
    cam.begin(f)
    c.save()
    c.translate(-500, -300)
    c.drawImage(im, 0, 0, L.LIN)
    c.restore()
    # yarık + huzme
    draw_slit(c, t, SLIT["x"], SLIT["y0"], SLIT["y1"], SLIT["w"], t=t)
    draw_beam(c, SLIT["x"] - 8, SLIT["y1"], 830, 360, t)

    def carved(text, x, y, size, track, at, dur=1.2):
        k = cx.amt(at, dur)
        if k <= 0.003:
            return
        sp = CM.engraved(text, "title", int(size), float(track), "#1C1A16", 1.25)
        CM.draw_spr(f, sp, x, y, "c", alpha=min(1.0, k * 2), reveal=clamp(k * 1.1))
        if k < 1.0:                                              # keskinin ucundan taş kıvılcımı
            ex = x - sp.wid / 2 + sp.wid * clamp(k * 1.1)
            for j in range(6):
                ph = (t * 7.0 + j * 0.37) % 1.0
                c.drawCircle(ex + ph * 18 - 6, y - size * 0.4 + ph * 22 + j * 3, 1.6, P("#F0E2B4", 220 * (1 - ph)))
    carved("ALBERGHETTINO", 905, 372, 72, 12, name_at, 1.5)
    carved("KÜÇÜK HAN", 905, 480, 52, 16, han_at, 0.9)
    # han tabelası (mizah)
    ks = cx.amt(sign_at, 0.12)
    th = cx.at(sign_at)
    inn_sign(c, 1030, 170, t, k=ks, t_hit=th)
    if ks > 0.003:
        dt = max(0.0, t - th)
        sc = 0.2 + 0.8 * sk.back_out(clamp(dt / 0.35)) if dt < 0.35 else 1.0
        ang = math.sin(dt * 5.2) * math.exp(-dt * 0.9) * 0.34
        c.save()
        c.translate(1030 + 150 - 14, 170)
        c.rotate(math.degrees(ang))
        c.scale(sc, sc)
        icons.draw_icon(f, "bed", 0, 86, size=74, metal="bronze", alpha=ks, shadow=False)
        c.restore()
    # siluet (yarığa bakar)
    fa = cx.amt(sil_at, 0.6)
    L.sil(f, "soylu", 1370, 832, 372, t, action="idle", dir=1, seed=4, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=fa)
    cam.end(f)
    pool = (SLIT["x"] - 300, 620.0, 1250.0, 1.0)
    CM.finish(f, cx, motes_n=12, light=pool)


@CM.ckind("c3_hucre")
def k_hucre(cx, **kw):
    k_hucre_impl(cx, **kw)


# ═══════════════════════════ dar yarıktan şehir (omuz üstü bakış) ═══════════════════════════
def _out_layers():
    """Yarığın ardındaki şehir: üç pişirilmiş katman (uzak gök+tepe · orta kuleler/katedral(kubbesiz) · yakın çatılar). Duomo 1433'te tamamlanmamıştı → yapım hâlinde tambur."""
    T = CT.Tint("day")
    WL = 3300

    def far(fr):
        c = fr.c
        sh = skia.GradientShader.MakeLinear([(0, 0), (0, 900)], [C("#7FA9D9"), C("#BFD6E4"), C("#F5E8C8")], [0.0, 0.62, 1.0])
        c.drawRect(skia.Rect.MakeLTRB(0, 0, WL, 1100), skia.Paint(Shader=sh))
        rs = _RS(11)
        for i in range(7):                                       # bulutlar
            x, y = rs.uniform(0, WL), rs.uniform(80, 420)
            for j in range(5):
                SOFT(c, x + j * 70 + rs.uniform(-20, 20), y + rs.uniform(-14, 14), rs.uniform(90, 170), rs.uniform(26, 46), "#FFFFFF", rs.uniform(110, 170))
        for (col, amp, sc, base, ph) in (("#A9BDB6", 40, 600, 700, 0.0), ("#93AFA5", 46, 420, 770, 2.1), ("#7F9E92", 52, 300, 840, 4.3)):
            cc = T(col, 0.2)
            pts = []
            x = -8
            while x <= WL + 8:
                pts.append((x, 1000 - L.PN.ridge_y(x, base - 700 + 400, amp, sc, ph)))
                x += 12
            poly = pts + [(pts[-1][0], 1200), (pts[0][0], 1200)]
            c.drawPath(sk.poly_path(poly), skia.Paint(AntiAlias=True, Color=C(cc)))
            c.drawPath(sk.poly_path(pts, False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, Color=C(mix(cc, "#1A2A22", 0.5), 150)))
            for gi in range(int(WL // 170) + 1):
                r_ = _RS(gi * 7 + int(ph * 10) + 1)
                if r_.rand() < 0.5:
                    x = gi * 170 + r_.uniform(0, 170)
                    L.PN.SC.cypress(c, x, 1000 - L.PN.ridge_y(x, base - 700 + 400, amp, sc, ph) + 3, r_.uniform(34, 60), T("#2E4A33", 0.3), T("#4F6E4A", 0.3)) if hasattr(L.PN, "SC") else None

    def mid(fr):
        c = fr.c
        rr = _RS(31)
        wins = []
        base = 900
        x = -40
        while x < WL + 40:                                       # uzak çatı sırası
            bw, bh = rr.uniform(70, 150), rr.uniform(60, 150)
            CT.draw_house(c, x, base + rr.uniform(-6, 6), bw, bh, _RS(int(rr.randint(1, 10 ** 6))), T, 0.38, wins)
            x += bw + rr.uniform(-8, 10)
        # katedral grubu (nef + kubbesiz tambur + çan kulesi) — x ≈ 1700
        XD = 1250
        c.save()
        c.translate(XD, base)
        c.scale(2.0, 2.0)
        c.translate(-XD, -base)
        CT.draw_nave(c, XD + 70, XD + 640, base + 4, 124, T, 0.22)
        draw_dome_wip(c, XD, base - 108, 214, 48, T, 0.20, u=0.38)
        CT.draw_campanile(c, XD + 205, base + 4, 54, 262, T, 0.20)
        c.restore()
        for tx, th in ((260, 520), (700, 380), (2650, 560), (3050, 430)):
            CT.draw_tower(c, tx, base + 4, 54, th, T, 0.28, spire=(tx in (260, 2650)))
        SE.GRAD_V(c, 0, base, WL, base + 400, [(T("#B8A888", 0.30), 0.0), (T("#A89A78", 0.25), 1.0)])

    def near(fr):
        c = fr.c
        rr = _RS(77)
        wins = []
        base = 1090
        x = -80
        while x < WL + 80:
            bw, bh = rr.uniform(150, 280), rr.uniform(110, 260)
            CT.draw_house(c, x, base, bw, bh, _RS(int(rr.randint(1, 10 ** 6))), T, 0.05, wins)
            # baca
            if rr.rand() < 0.5:
                cxh = x + bw * rr.uniform(0.2, 0.7)
                R(c, cxh, base - bh - 90, cxh + 26, base - bh - 20, T("#A8684A"))
            x += bw + rr.uniform(-14, 6)
    return (bake(("yarik_far",), WL, 1200, far), bake(("yarik_mid",), WL, 1200, mid), bake(("yarik_near",), WL, 1200, near))


def k_yarik_impl(cx, scan=(-1100.0, 1100.0), seed=1, **_):
    f = cx.f
    c = f.c
    t = cx.t
    f.clear("#16140F")
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    far, mid, near = _out_layers()
    cam.begin(f)
    # duvar (taş) — geniş
    T = L.OD.OTint("day")
    c.save()
    c.drawRect(skia.Rect.MakeLTRB(-1200, -800, 3100, 1900), P("#4A463E"))
    L.OD.ashlar(c, -1200, 3100, -800, 1900, T, col="#58544A", course=96.0, seed=4)
    c.restore()
    # içe doğru genişleyen yarık ağzı (splay): dış (ağız) ve iç (yarık) dikdörtgenleri
    Mx0, Mx1, My0, My1 = 330.0, 1590.0, -120.0, 1200.0
    Sx0, Sx1, Sy0, Sy1 = 840.0, 1080.0, 150.0, 940.0
    faces = {
        "L": [(Mx0, My0), (Sx0, Sy0), (Sx0, Sy1), (Mx0, My1)],
        "R": [(Mx1, My0), (Sx1, Sy0), (Sx1, Sy1), (Mx1, My1)],
        "T": [(Mx0, My0), (Mx1, My0), (Sx1, Sy0), (Sx0, Sy0)],
        "B": [(Mx0, My1), (Mx1, My1), (Sx1, Sy1), (Sx0, Sy1)],
    }
    cols = {"L": ("#7E786A", "#D8D0B0"), "R": ("#3C382F", "#948C74"), "T": ("#26231D", "#5E594C"), "B": ("#A8A088", "#F2EAC8")}
    for k_, pts in faces.items():
        p = sk.poly_path(pts)
        a0, a1 = (pts[0], pts[1]) if k_ in ("L", "R") else (pts[0], pts[3])
        sh = skia.GradientShader.MakeLinear([a0, a1], [C(cols[k_][0]), C(cols[k_][1])], [0, 1])
        c.drawPath(p, skia.Paint(AntiAlias=True, Shader=sh))
    # splay yüzlerinde taş sıraları (perspektifte yakınsayan çizgiler)
    for i in range(1, 9):
        u = i / 9.0
        yL0 = lerp(My0, My1, u)
        yS = lerp(Sy0, Sy1, u)
        c.drawLine(Mx0, yL0, Sx0, yS, S("#16120C", 1.4, 120))
        c.drawLine(Mx1, yL0, Sx1, yS, S("#16120C", 1.4, 120))
    for i in range(1, 7):
        u = i / 7.0
        c.drawLine(lerp(Mx0, Mx1, u), My1, lerp(Sx0, Sx1, u), Sy1, S("#16120C", 1.2, 90))
        c.drawLine(lerp(Mx0, Mx1, u), My0, lerp(Sx0, Sx1, u), Sy0, S("#16120C", 1.2, 90))
    # yarığın içi: şehir (kırpılmış, paralaks kaydırma)
    u = clamp(t / max(1.0, cx.dur))
    sc_x = lerp(scan[0], scan[1], ease_io(u, 2.0))
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(Sx0, Sy0, Sx1, Sy1))
    yb = Sy0 - 40
    blit(c, far, 960 - sc_x * 0.25, yb + far.height() / 2 - 120, ax=0.5, ay=0.5)
    blit(c, mid, 960 - sc_x * 0.55, yb + mid.height() / 2 - 130, ax=0.5, ay=0.5)
    blit(c, near, 960 - sc_x * 1.0, yb + near.height() / 2 - 120, ax=0.5, ay=0.5)
    # kuşlar
    for i in range(4):
        ph = (t * (0.10 + 0.03 * i) + i * 0.27) % 1.0
        bx = Sx0 - 40 + ph * (Sx1 - Sx0 + 80)
        by = Sy0 + 160 + i * 90 + math.sin(t * 1.3 + i) * 12
        fl = math.sin(t * 11 + i * 2.0) * 6
        pth = skia.Path()
        pth.moveTo(bx - 12, by + fl * 0.4)
        pth.quadTo(bx - 5, by - 6 - fl, bx, by)
        pth.quadTo(bx + 5, by - 6 - fl, bx + 12, by + fl * 0.4)
        c.drawPath(pth, S("#3A342C", 2.6, 220))
    c.restore()
    # yarığın ışıması + iç kenar çizgisi
    SOFT(c, 960, (Sy0 + Sy1) / 2, 240, 640, "#FFF2C8", 70)
    c.drawRect(skia.Rect.MakeLTRB(Sx0, Sy0, Sx1, Sy1), S("#16120C", 3.0, 230))
    # omuz üstü siluet (arkadan: yüz yok): baş + omuzlar, sağdan ışık kenarı
    br = 1.0 + 0.004 * math.sin(t * 1.6)
    pts = [(-160, 1240), (-90, 1010), (60, 905), (210, 862), (255, 800), (240, 720), (250, 640), (300, 575), (385, 548), (468, 578), (505, 650), (492, 735), (468, 790), (510, 850),
           (680, 905), (840, 990), (900, 1240)]
    body = sk.smooth_path([(x * 1.0, 540 + (y - 540) * br) for x, y in pts], True, 0.5)
    c.drawPath(body, P("#0F0B08"))
    rim = skia.Path()
    rim.addPath(body)
    c.save()
    c.clipPath(body, skia.ClipOp.kIntersect, True)
    c.translate(-5, 3)
    c.drawPath(body, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7, Color=C("#FFD890", 150)))
    c.restore()
    c.drawPath(body, P("#0F0B08"))
    # başlık: berrete (yumuşak, kenarsız) — yalnız silueti sertleştirir
    c.drawOval(skia.Rect.MakeLTRB(300, 520, 480, 585), P("#0F0B08"))
    cam.end(f)
    CM.finish(f, cx, motes_n=10, light=(960.0, 540.0, 1300.0, 1.0))


@CM.ckind("c3_yarik")
def k_yarik(cx, **kw):
    k_yarik_impl(cx, **kw)


# ═══════════════════════════ yardımcı: masa (ön görünüş, ters perspektif) ═══════════════════════════
def table_persp(c, x0, x1, yb, yf, apron=64, leg_to=None, col="#7A4A28", cloth=None, depth=0.10):
    """Masa: arka kenar yb, ön kenar yf (yf>yb); tabla trapez; ön apron + bacaklar. cloth=(ana, şerit) örtü."""
    ins = (x1 - x0) * depth
    top = [(x0 + ins, yb), (x1 - ins, yb), (x1, yf), (x0, yf)]
    tc = cloth[0] if cloth else col
    sh = skia.GradientShader.MakeLinear([(0, yb), (0, yf)], [C(mix(tc, "#FFFFFF", 0.12)), C(tc)], [0, 1])
    c.drawPath(sk.poly_path(top), skia.Paint(AntiAlias=True, Shader=sh))
    INKP(c, sk.poly_path(top), 1.8, 200)
    if cloth:
        c.drawLine(x0 + ins * 0.55, (yb + yf) / 2, x1 - ins * 0.55, (yb + yf) / 2, S(cloth[1], 3.0, 170))
    leg_to = leg_to or yf + apron + 110
    for lx in (x0 + 26, x1 - 26):
        c.drawRect(skia.Rect.MakeLTRB(lx - 14, yf, lx + 14, leg_to), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(lx - 14, 0), (lx + 14, 0)], [C(mix(col, "#FFFFFF", 0.1)), C(mix(col, "#000000", 0.35))], [0, 1])))
        INKR(c, lx - 14, yf, lx + 14, leg_to, 1.3, 180)
    ap = skia.Path()
    ap.addRect(skia.Rect.MakeLTRB(x0, yf, x1, yf + apron))
    c.drawPath(ap, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, yf), (0, yf + apron)], [C(mix(tc, "#000000", 0.18)), C(mix(tc, "#000000", 0.42))], [0, 1])))
    INKP(c, ap, 1.6, 190)
    rs = _RS(int(x0))
    for i in range(7):
        yy = rs.uniform(yf + 8, yf + apron - 8)
        c.drawLine(x0 + 6, yy, x1 - 6, yy + rs.uniform(-1.5, 1.5), S("#1E1208", 1.0, 70))


def dashed(c, x0, y0, x1, y1, col="#A8321E", w=3.0, a=220, dash=(16.0, 10.0), phase=0.0):
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, int(a)), StrokeCap=skia.Paint.kRound_Cap)
    p.setPathEffect(skia.DashPathEffect.Make(list(dash), phase))
    c.drawLine(x0, y0, x1, y1, p)


# ═══════════════════════════ c3s6: suçlama — yurttaşlar ve masadaki karar ═══════════════════════════
@CM.ckind("c3_suclama")
def k_suclama(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=2)
    t = cx.t
    GY = 820.0
    L.grid_floor(c, -500, 2420, GY, 1060)
    L.engr(f, cx, "SUÇLAMA", 960, 250, ("c3s6", -0.1), size=70, track=18, dur=0.8)
    kinds = ["halk", "tuccar", "banker", "soylu", "halk", "tuccar", "banker"]
    xs = [330 + i * 210 for i in range(7)]
    t_rise = cx.at(("c3s6", 0.15))
    k_pod = cx.amt(("c3s6", "üstüne", -0.1), 1.0)
    n_coin = 15
    pod_h = n_coin * 12.0 * ease_out(k_pod, 2)
    HH = 330.0
    for i, (kd, x) in enumerate(zip(kinds, xs)):
        k = clamp((t - (t_rise + 0.11 * i)) / 0.5)
        if k <= 0.003:
            continue
        up = (1.0 - ease_out(k, 3)) * 420
        y = GY + 6 + up
        if i == 3:
            L.coin_stack(c, x, GY + 4, int(n_coin * ease_out(k_pod, 2)), r=58, gap=12.0, ph=0.4)
            y = GY - pod_h + 4 + up
        stil = dict(robe="#2F5FB8", robe2="#E0B84E", hat_col="#B33620") if i == 3 else {}
        L.actor(f, kd, x, y, HH, t, action="idle", dir=1, seed=40 + i, phase=0.13 * i, **stil)
    kr = ease_io(cx.amt(("c3s6", "sıradan", 0.0), 0.9), 2)
    if kr > 0.003:
        x_a, x_b = 220.0, 220.0 + (1700.0 - 220.0) * kr
        dashed(c, x_a, GY - HH, x_b, GY - HH, col="#A8321E", w=3.4, a=210, phase=-t * 30)
    # masa + karar (kamera aşağı iner)
    table_persp(c, 380, 1540, 1170, 1330, apron=84, col="#7A4A28")
    for k_ in range(7):
        yy = 1170 + (k_ + 0.5) * (160 / 7)
        c.drawLine(380 + 120 * (1 - k_ / 7.0) * 0.3 + 10, yy, 1540 - 10, yy, S("#2A1608", 1.2, 60))
    GRAD_V(c, -500, 1460, 2420, 1800, [("#5A4A38", 0.0), ("#2E241A", 1.0)])
    ks = cx.amt(("c3s6", "masadaydı", -0.6), 0.55)
    if ks > 0.003:
        drop = (1.0 - ease_out(ks, 3)) * 300
        bounce = math.sin(max(0.0, ks - 0.8) * 40) * 4 * (1 - ks) if ks > 0.8 else 0.0
        pp = PP_sheet(620, 330, seed=14)
        yy = 1250 - drop + bounce
        pp.draw(f, 960, yy, rot=-0.03, scale=1.0, alpha=smooth(ks * 3), shadow=0.6)
        c.save()
        c.translate(960, yy)
        c.rotate(math.degrees(-0.03))
        PP_hand(f, "ÖLÜM CEZASI", 0, 16, 66, "#2A1A0E", smooth(ks * 3))
        kk = cx.amt(("c3s6", "ihtimali", 0.0), 1.4)
        if kk > 0.01:
            SOFT(c, -190 + 380 * kk, 50, 240, 90, "#8E2A1E", 125 * kk)
        c.restore()
        # mürekkep hokkası + kalem
        OD_inkwell(c, 1330, 1245)
    L.end(cx, cam, motes_n=20)


def OD_inkwell(c, x, y):
    c.drawOval(skia.Rect.MakeLTRB(x - 30, y - 12, x + 30, y + 12), P("#1A1208"))
    c.drawRect(skia.Rect.MakeLTRB(x - 24, y - 42, x + 24, y), P("#2A1E10"))
    c.drawOval(skia.Rect.MakeLTRB(x - 24, y - 52, x + 24, y - 32), P("#0E0A06"))
    INKR(c, x - 24, y - 42, x + 24, y, 1.4, 180)


def PP_sheet(w, h, seed=1, tone=(236, 224, 192)):
    return L.PP.paper_image(int(w), int(h), seed, tone, "deckle", (), 44, 1.0)


def PP_hand(f, text, x, y, size, color, alpha, seed=3, jitter=1.3):
    L.PP.hand(f, text, x, y, face="fell_i", size=size, color=color, alpha=alpha, jitter=jitter, seed=seed, align="c")


# ═══════════════════════════ c3s7: gravür — ekmek, zehir korkusu, bekçi (ANEKDOT) ═══════════════════════════
def cell_bg(c, T, slit_x=1180.0, slit_y0=120.0, slit_y1=400.0, beam_to=900.0, t=0.0, seed=3, beam_dx=330.0):
    """Hücre arka planı (pişirilmiş taş duvar + yarık + ışık huzmesi) — gravür sahnelerinde de kullanılır."""
    im = bake(("hucre_wall", 1), 2920, 1500, lambda fr: _cell_wall(fr, T))
    c.save()
    c.translate(-500, -300)
    c.drawImage(im, 0, 0, L.LIN)
    c.restore()
    draw_slit(c, t, slit_x, slit_y0, slit_y1, 34.0, t=t)
    draw_beam(c, slit_x - 8, slit_y1, beam_to, beam_dx, t, a=0.9)


def k_gravur_masa_impl(cx, **_):
    f = cx.f
    c = f.c
    t = cx.t
    L.mono_begin(f, 1.0)
    f.clear("#0B0A08")
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    cam.begin(f)
    T = L.OD.OTint("day")
    cell_bg(c, T, slit_x=1260.0, slit_y0=60.0, slit_y1=330.0, beam_to=850.0, t=t, beam_dx=420.0)
    t_fear = cx.at(("c3s7", "zehirlenmekten", 0.0))
    t_eat = cx.at(("c3s7", "yedi", -0.6))
    t_guard = cx.at(("c3s7", "bekçi", 0.0))
    t_each = cx.at(("c3s7", "getirilen", 0.0))
    t_taste = cx.at(("c3s7", "kendisi", 0.0))
    t_calm = cx.at(("c3s7", "rahatlattı", -0.2))
    X0, X1 = 600.0, 1760.0
    if t >= t_calm:
        act, t0a = "listen", 0.0
    elif t >= t_eat - 0.05:
        act, t0a = "eat", t_eat
    elif t >= t_fear:
        act, t0a = "fear", t_fear
    else:
        act, t0a = "listen", 0.0
    # kuru zemin gölgesi
    SOFT(c, 1100, 905, 760, 40, "#000000", 120)
    L.OD.seated(f, "soylu", X0 - 40, 846, 340, t, action=act, dir=1, seed=4, phase=0.2, t0=t0a, rim="#FFE2A0", rim_dir=1)
    table_persp(c, X0, X1, 702, 826, apron=70, col="#7A5232", depth=0.06)
    # kâseler: 'her yemek' ile sırayla gelir
    bowls = [(1030, 0.0), (1230, 0.55), (1430, 1.1)]
    t_b0 = cx.at(("c3s7", 0.0))
    push = cx.amt(("c3s7", "yalnız", 0.0), 0.8)
    for i, (bx, dly) in enumerate(bowls):
        tb = (t_b0 + 0.3) if i == 0 else (t_each + dly - 0.55)
        k = clamp((t - tb) / 0.35)
        if k <= 0.003:
            continue
        L.draw_bowl(c, bx + 90 * ease_out(push), 772 - (1 - ease_out(k, 3)) * 170, s=1.15, a=int(255 * min(1, k * 3)), fill="#6A4A2A", steam=0.17 * i, t=t)
    # ekmek
    t_bite = [t_eat + 0.55 + 1.3 * j for j in range(4)]
    bit = sum(0.26 * clamp((t - tb_) / 0.25) for tb_ in t_bite)
    gl = cx.amt(("c3s7", "ekmek", -0.1), 0.5) * (1 - cx.amt(("c3s7", "yedi", 0.0), 0.8) * 0.7)
    if gl > 0.01:
        SOFT(c, 800, 760, 180, 80, "#FFF0B8", 110 * gl)
    L.draw_loaf(c, 800, 782, s=1.12, bit=min(1.0, bit))
    sk_k = cx.amt(("c3s7", "zehirlenmekten", 0.0), 0.35) * (1.0 - cx.amt(("c3s7", "yalnız", 0.0), 0.5))
    if sk_k > 0.01:
        for bx in (1030, 1230):
            sy = 590 - 8 * math.sin(t * 5 + bx)
            icons.draw_icon(f, "skull", bx, sy, size=100 * (0.8 + 0.2 * sk_k), metal="bronze", alpha=sk_k, shadow=False)
    if t >= t_guard - 0.1:
        gx_end = 1850.0
        spd = 150.0
        gx0 = 2330.0
        x = max(gx_end, gx0 - spd * max(0.0, t - (t_guard - 0.1)))
        if x > gx_end + 0.5:
            L.walker(f, "asker", x, 850, 350, t, speed=spd, dir=-1, phase=0.0, seed=8, prop="basket", rim=None) if False else L.walker(f, "asker", x, 850, 350, t, speed=spd, dir=-1, phase=0.0, seed=8, prop="basket")
        else:
            L.actor(f, "asker", gx_end, 850, 350, t, action="taste", dir=-1, seed=8, phase=0.1, t0=t_taste - 0.1, period=2.2)
    cam.end(f)
    L.mono_end(f)
    CM.finish(f, cx, motes_n=14, light=(1100.0, 560.0, 1500.0, 1.0))
    L.tag(f, cx, "MACHIAVELLI", 1530, 250, at=("c3s7", "Machiavelli'ye", 0.0), size=34, w=420)
    L.stamp_at(f, cx, "ANEKDOT", 1530, 340, at=("c3s7", "Machiavelli'ye", 0.35), size=48)


@CM.ckind("c3_gravur_masa")
def k_gravur_masa(cx, **kw):
    k_gravur_masa_impl(cx, **kw)


# ═══════════════════════════ c3s8: küçük kâğıdın yolu (gravür, tek yatay plan) ═══════════════════════════
def loggia_front(c, x0, yg, w, h, T, n=5, seed=2):
    """Basit revaklı bina (hastane): sıva duvar, kemerli revak, üst kat pencereleri, kiremit saçak."""
    wall = T("#E3D3AE")
    R(c, x0, yg - h, x0 + w, yg, wall)
    GRAD_V(c, x0, yg - h, x0 + w, yg, [("#FFFFFF", 0.0, 24), ("#000000", 1.0, 40)])
    INKR(c, x0, yg - h, x0 + w, yg, 2.0, 200)
    # çatı saçağı
    R(c, x0 - 14, yg - h - 22, x0 + w + 14, yg - h + 6, T("#B9552F"))
    INKR(c, x0 - 14, yg - h - 22, x0 + w + 14, yg - h + 6, 1.6, 200)
    step = w / n
    for i in range(n):
        ax = x0 + i * step
        # sütun
        R(c, ax - 10, yg - h * 0.52, ax + 10, yg, T("#CBBE9C"))
        INKR(c, ax - 10, yg - h * 0.52, ax + 10, yg, 1.2, 170)
        # kemer içi
        p = skia.Path()
        p.moveTo(ax + 12, yg)
        p.lineTo(ax + 12, yg - h * 0.34)
        p.cubicTo(ax + 12, yg - h * 0.52, ax + step - 12, yg - h * 0.52, ax + step - 12, yg - h * 0.34)
        p.lineTo(ax + step - 12, yg)
        p.close()
        c.drawPath(p, P("#3A2A1C", 235))
        INKP(c, p, 1.6, 210)
        # üst kat penceresi
        wx = ax + step / 2
        wp = skia.Path()
        wp.addRoundRect(skia.Rect.MakeLTRB(wx - 15, yg - h * 0.86, wx + 15, yg - h * 0.62), 10, 10)
        c.drawPath(wp, P("#4A3A28", 230))
        INKP(c, wp, 1.2, 180)
    R(c, x0 + w - 10, yg - h * 0.52, x0 + w + 10, yg, T("#CBBE9C"))
    INKR(c, x0 + w - 10, yg - h * 0.52, x0 + w + 10, yg, 1.2, 170)


def coin_heap(c, x, y, n, spread=1.0, a=255, seed=1, t=0.0, r=15.0):
    """Altın sikke yığını (üstten bakışlı küçük daireler): n sikke."""
    rs = _RS(seed)
    for i in range(int(n)):
        ang = rs.uniform(0, 6.283)
        rad = rs.uniform(0, 1) ** 0.6 * 60 * spread
        h = rs.uniform(0, 1) * (28 * spread) * (1 - rad / (62 * spread))
        L.draw_coin_flat(c, x + math.cos(ang) * rad, y + math.sin(ang) * rad * 0.35 - h, r=r, a=a)


def k_kagit_yolu_impl(cx, **_):
    f = cx.f
    c = f.c
    t = cx.t
    L.mono_begin(f, 1.0)
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=2, cam=cam, dress=None)
    cam.begin(f)
    T = L.OD.OTint("day")
    GY = 860.0
    L.grid_floor(c, -500, 6000, GY, 1180, col1="#BDB090", col2="#8E8264")
    HH = 330.0
    # zamanlar
    t_give = cx.at(("c3s8", "aracısına", 0.0))
    t_slip = cx.at(("c3s8", "küçük", 0.0))
    t_run = cx.at(("c3s8", "verdi;", 0.35))
    t_arrive = cx.at(("c3s8", "hastanesinin", 0.0))
    t_1100 = cx.at(("c3s8", "bin", 0.0))
    t_dem = cx.at(("c3s8", "bini", 0.0))
    t_end = cx.at(("c3s8", "gitti.", 0.0))
    XA = 560.0
    # istasyon A: Cosimo (ver) → aracı (al)
    L.actor(f, "soylu", XA, GY, HH, t, action="give", dir=1, seed=4, phase=0.1, t0=t_give - 0.6, dur=0.7, hold=0.55, slip=True)
    # aracı
    XR = XA + 190.0
    HOSP = 1500.0
    DOOR_X = HOSP + 180.0
    spd = 330.0
    if t < t_run:
        L.actor(f, "tuccar", XR, GY + 4, HH, t, action="take", dir=-1, seed=7, phase=0.4, t0=t_give - 0.5, dur=0.6, hold=1.3, got_at=t_give + 0.35)
        ax = XR
    else:
        ax = min(DOOR_X - 160.0, XR + spd * (t - t_run))
        if ax < DOOR_X - 160.0 - 0.5:
            L.walker(f, "tuccar", ax, GY + 4, HH, t, speed=spd, dir=1, run=True, seed=7, phase=0.3, prop="scroll") if False else L.walker(f, "tuccar", ax, GY + 4, HH, t, speed=spd, dir=1, run=True, seed=7, phase=0.3)
    # hastane
    loggia_front(c, HOSP, GY, 720, 470, T, n=5)
    k_sign = cx.amt(("c3s8", "Santa", 0.0), 0.7)
    if k_sign > 0.003:
        L.engr(f, cx, "SANTA MARIA NUOVA", HOSP + 360, GY - 545, ("c3s8", "Santa", 0.0), size=44, track=8, dur=1.2)
    # başkan (rahip), kapıda alır
    L.actor(f, "rahip", DOOR_X + 180, GY + 2, HH, t, action="take", dir=-1, seed=12, phase=0.2, t0=t_arrive + 0.6, dur=0.7, hold=3.0, got_at=cx.at(("c3s8", "başkanından", 0.0)) + 0.2)
    if t >= t_arrive + 0.6 and ax >= DOOR_X - 160.5:
        L.actor(f, "tuccar", DOOR_X - 160.0, GY + 4, HH, t, action="give", dir=1, seed=7, phase=0.3, t0=t_arrive + 0.55, dur=0.6, hold=0.5, slip=(t < t_arrive + 1.9))
    # 1.100 duka: yığın + sayaç
    k_h = cx.amt(("c3s8", "bin", 0.0), 0.5)
    t_split = t_dem
    hx, hy = DOOR_X + 330.0, GY + 20
    if k_h > 0.003:
        n_big = int(26 * k_h)
        coin_heap(c, hx, hy, n_big, spread=1.35, a=int(255 * k_h), seed=5, r=17.0)
    # Guadagni
    GXG = HOSP + 1520.0
    kg = cx.amt(("c3s8", "gonfaloniere'ye", 0.0), 0.8)
    L.sil(f, "soylu", GXG, GY + 8, HH, t, action="idle", dir=-1, seed=23, color="#14100C", rim="#FFE2A0", rim_dir=-1, alpha=max(0.0, cx.amt(("c3s8", "bin", 0.0), 0.8)))
    # uçan 1.000 sikke (hx,hy) → Guadagni (GXG - 60, GY - 150)
    kf = clamp((t - t_dem) / 1.1)
    if 0 < kf <= 1.0:
        for i in range(18):
            u = clamp(kf * 1.25 - i * 0.03)
            if u <= 0 or u >= 1:
                continue
            px = lerp(hx, GXG - 70, u)
            py = lerp(hy - 20, GY - 150, u) - math.sin(math.pi * u) * 260
            L.draw_coin_flat(c, px, py, r=15.0, a=255)
    cam.end(f)
    L.mono_end(f)
    CM.finish(f, cx, motes_n=16)
    # kart: 1.000 + 100 DUKA (ekran kartı)
    kc = cx.amt(("c3s8", "bin", 0.0), 0.6)
    if kc > 0.003:
        L.tag(f, cx, "1.100 DUKA", 960, 240, at=("c3s8", "bin", 0.0), size=52, w=420, hold=("c3s8", "gitti.", 0.4))
    L.tag(f, cx, "1.000", 960 + 360, 400, at=("c3s8", "bini", 0.0), size=44, w=260, hold=("c3s8", "gitti.", 0.4), sub="GONFALONIERE'YE")
    L.stamp_at(f, cx, "ANEKDOT", 330, 270, at=("c3s8", "Yine", 0.0), size=46, rot=-0.08)


@CM.ckind("c3_kagit_yolu")
def k_kagit_yolu(cx, **kw):
    k_kagit_yolu_impl(cx, **kw)


# ═══════════════════════════ c3s9–c3s10: karar yaprağı — 'ölüm cezası' sürgüne döner; küçük kâğıt ═══════════════════════════
def k_karar_impl(cx, **_):
    from cilt_kinds2 import draw_quill
    f = cx.f
    c = f.c
    t = cx.t
    L.mono_begin(f, 1.0)
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=1, cam=cam, dress=None)
    cam.begin(f)
    # masa tahtası (alttan) + yaprak
    GRAD_V(c, -500, 700, 2420, 1400, [("#7A5232", 0.0), ("#4A2E18", 1.0)])
    for k_ in range(9):
        yy = 700 + k_ * 78
        c.drawLine(-500, yy, 2420, yy, S("#1E1208", 1.6, 110))
    c.drawRect(skia.Rect.MakeLTRB(-500, 690, 2420, 710), P("#2A1A0C", 120))
    pp = PP_sheet(1280, 640, seed=21)
    pp.draw(f, 960, 640, rot=-0.012, scale=1.0, alpha=1.0, shadow=0.7)
    c.save()
    c.translate(960, 640)
    c.rotate(math.degrees(-0.012))
    ka = cx.amt(("c3s9", -0.4), 0.5)
    txt1 = "ÖLÜM CEZASI"
    tw = sk.text_width(txt1, "fell_i", 120)
    PP_hand(f, txt1, 0, -20, 120, "#2A1A0E", ka, seed=5, jitter=1.2)
    # üstü çizme (kalem sürgüne gelince)
    t_s = cx.at(("c3s9", "sürgüne", 0.0))
    ks = clamp((t - (t_s - 0.35)) / 0.55)
    if ks > 0:
        e = ease_io(ks, 1.8)
        p_ = skia.Path()
        p_.moveTo(-tw / 2 - 20, -40)
        p_.lineTo(-tw / 2 - 20 + (tw + 40) * e, -52 + 18 * e)
        pp2 = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=9, Color=C("#7A1E12", 235), StrokeCap=skia.Paint.kRound_Cap)
        pp2.setPathEffect(skia.DiscretePathEffect.Make(11.0, 2.0, 3))
        c.drawPath(p_, pp2)
    # SÜRGÜN yazılır
    txt2 = "SÜRGÜN"
    tw2 = sk.text_width(txt2, "fell_i", 128)
    kw = clamp((t - (t_s + 0.1)) / 0.85)
    qx = qy = None
    if kw > 0:
        e2 = ease_io(kw, 1.5)
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(-tw2 / 2 - 14, 0, -tw2 / 2 - 14 + (tw2 + 40) * e2, 260))
        PP_hand(f, txt2, 0, 150, 128, "#1B2A66", 1.0, seed=8, jitter=1.0)
        c.restore()
        qx, qy = -tw2 / 2 - 14 + (tw2 + 40) * e2, 150
    c.restore()
    # kalem
    if ks > 0 and ks < 1:
        e = ease_io(ks, 1.8)
        qx_, qy_ = -tw / 2 - 20 + (tw + 40) * e, -52 + 18 * e
        draw_quill(f, 960 + qx_ + 4, 640 + qy_ + 8, ang=-58.0, alpha=1.0, scale=1.0)
    elif qx is not None and kw < 1.0:
        draw_quill(f, 960 + qx + 6, 640 + qy + 4, ang=-58.0, alpha=1.0, scale=1.0)
    # küçük kâğıt: iki karar arasına düşer (aradaki fark)
    ksl = cx.amt(("c3s10", 0.0), 0.5)
    if ksl > 0.003:
        drop = (1.0 - ease_out(ksl, 3)) * 380
        gl = cx.amt(("c3s10", "küçük", 0.0), 0.9)
        L.draw_slip(c, 1330, 880 - drop, w=190, h=124, rot=0.10, lines=3, seed=9, glow=gl)
    cam.end(f)
    L.mono_end(f)
    CM.finish(f, cx, motes_n=14)
    L.stamp_at(f, cx, "ANEKDOT", 1520, 220, at=("c3s9", 0.0), size=46, rot=-0.07, hold=("c3s10", 0.2))
    L.stamp_at(f, cx, "YORUM", 1520, 220, at=("c3s10", 0.3), size=46, rot=-0.07)


@CM.ckind("c3_karar")
def k_karar(cx, **kw):
    k_karar_impl(cx, **kw)


# ═══════════════════════════ c3s12: sürgünün süresi — kaynaklar anlaşamıyor ═══════════════════════════
def k_sure_impl(cx, **_):
    from cilt_kinds3 import _bar_fill
    f, c, cam = L.begin(cx, bg="wall", seed=0, dress="both")
    t = cx.t
    X0, PX = 380.0, 54.0                            # sıfır yıl noktası ve yıl başına px
    rows = [(1, 405), (5, 515), (10, 625), (20, 735)]
    k_book = [cx.amt(("c3s12", "Kaynaklar", 0.0), 0.4, off=0.17 * i) for i in range(4)]
    t_dim = cx.at(("c3s12", "çoğu", 0.0))
    kd = cx.amt(("c3s12", "çoğu", 0.0), 0.6)
    # eksen
    ka = cx.amt(("c3s12", 0.0), 0.7)
    L.engr(f, cx, "SÜRGÜNÜN SÜRESİ", 960, 262, ("c3s12", 0.1), size=56, track=16, dur=1.0)
    c.drawLine(X0, 810, X0 + 20 * PX, 810, S(TH.rule, 3.0, 230 * ka))
    for y_ in range(0, 21):
        major = y_ in (0, 1, 10, 20)
        c.drawLine(X0 + y_ * PX, 810, X0 + y_ * PX, 810 + (20 if major else 10), S(TH.rule, 2.0, 200 * ka))
    for y_ in (1, 10, 20):
        CM.ink(f, str(y_), X0 + y_ * PX, 868, face="title_m", size=30, color=TH.fg2, align="c", alpha=ka, emboss=False, track=3)
    CM.ink(f, "YIL", X0 + 20 * PX + 70, 868, face="title_m", size=26, color=TH.fg3, align="l", alpha=ka, track=6, emboss=False)
    # çubuklar
    starts = {1: ("c3s12", "bir", 0.0, 0.5), 20: ("c3s12", "yirmi", 0.0, 1.3), 5: ("c3s12", "yirmi", 0.55, 0.9), 10: ("c3s12", "yirmi", 0.9, 0.9)}
    cols = {1: "#7A5A38", 5: "#7A5A38", 10: "#233C8C", 20: "#7A5A38"}
    labels = {1: "BİR YIL", 20: "YİRMİ YIL", 10: "ON YIL"}
    for i, (yrs, yy) in enumerate(rows):
        sid, kw_, off, dur = starts[yrs]
        k = ease_out(clamp((t - (cx.at((sid, kw_, 0.0)) + (off if kw_ == "yirmi" else 0.0))) / dur), 3)
        # kitap simgesi (kaynak)
        kb = k_book[i]
        dimk = kd if yrs != 10 else 0.0
        if kb > 0.003:
            icons.draw_icon(f, "book", 270, yy + 30, size=84 * (0.8 + 0.2 * sk.back_out(kb)), metal="bronze", alpha=kb * (1 - 0.55 * dimk), shadow=False)
        if k > 0.003:
            w = max(6.0, yrs * PX * k)
            hl = (yrs == 10) and kd > 0.01
            col = "#C79A3C" if hl else cols[yrs]
            _bar_fill(f, X0, yy, w, 62, col, alpha=(1 - 0.6 * dimk) if yrs != 10 else 1.0)
            if yrs in labels and k > 0.9:
                al = cx.amt(("c3s12", "yirmi" if yrs == 20 else ("bir" if yrs == 1 else "on"), 0.0), 0.4, off=(1.1 if yrs == 20 else 0.0)) if yrs != 10 else cx.amt(("c3s12", "on", 0.0), 0.4)
                CM.ink(f, labels[yrs], X0 + yrs * PX + 24, yy + 44, face="title_m", size=36 if yrs != 10 else 46, color=TH.fg if yrs != 10 else TH.acc, align="l", track=5, alpha=al * (1 - 0.5 * dimk if yrs != 10 else 1.0), emboss=False)
    # çoğu anlatıda: altın parantez
    kb = cx.amt(("c3s12", "anlatıda", 0.0), 0.6)
    if kb > 0.003:
        x1 = X0 + 10 * PX
        pth = skia.Path()
        pth.moveTo(x1 + 4, 585)
        pth.quadTo(x1 + 30, 656, x1 + 4, 696)
        c.drawPath(pth, S("#C79A3C", 5.0, 235 * kb))
        L.tag(f, cx, "ÇOĞU ANLATIDA", x1 + 330, 660 + 70, at=("c3s12", "anlatıda", 0.0), size=30, w=360)
    L.end(cx, cam, motes_n=18)


@CM.ckind("c3_sure")
def k_sure(cx, **kw):
    k_sure_impl(cx, **kw)


# ═══════════════════════════ c3s14: yanında mimar Michelozzo ═══════════════════════════
def k_michelozzo_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=1, dress=None)
    t = cx.t
    GY = 800.0
    L.grid_floor(c, -800, 3200, GY, 1100)
    # yol çizgisi: kesikli rota
    dashed(c, -500, GY + 56, 2800, GY + 56, col="#233C8C", w=5.0, a=190, dash=(26.0, 16.0), phase=-t * 55)
    sp = 108.0
    x0 = 120 + sp * t
    L.walker(f, "soylu", x0 + 380, GY, 330, t, speed=sp, dir=1, phase=0.0, seed=4, stil=None) if False else L.walker(f, "soylu", x0 + 380, GY, 330, t, speed=sp, dir=1, phase=0.0, seed=4)
    L.walker(f, "banker", x0 + 210, GY + 8, 318, t, speed=sp, dir=1, phase=0.45, seed=9, prop="scroll") if False else L.walker(f, "banker", x0 + 210, GY + 8, 318, t, speed=sp, dir=1, phase=0.45, seed=9)
    # Michelozzo'nun üstünde çizilen kemer (mürekkep çizgisi) + pergel
    kk = ease_io(cx.amt(("c3s14", "mimar", 0.0), 1.2), 2)
    mx = x0 + 210
    if kk > 0.003:
        pth = skia.Path()
        by = GY - 470
        for i in range(3):
            ax = mx - 160 + i * 160
            pth.moveTo(ax, by + 100)
            pth.lineTo(ax, by + 36)
            pth.cubicTo(ax, by - 30, ax + 120, by - 30, ax + 120, by + 36)
            pth.lineTo(ax + 120, by + 100)
        pm = skia.PathMeasure(pth, False)
        part = skia.Path()
        pm.getSegment(0, pm.getLength() * kk, part, True)
        c.drawPath(part, S("#2A1A0C", 3.4, 235))
        c.drawLine(mx - 170, by + 100, mx + 190, by + 100, S("#2A1A0C", 3.0, 235 * min(1.0, kk * 3)))
        # pergel
        px, py = mx + 235, by + 18
        ang = 0.30 + 0.12 * math.sin(t * 2.4)
        for sg in (-1, 1):
            c.drawLine(px, py, px + sg * 56 * math.sin(ang) * 1.0, py + 140 * math.cos(ang), S("#2A2620", 7.0, 235 * min(1, kk * 2)))
            c.drawLine(px, py, px + sg * 56 * math.sin(ang), py + 140 * math.cos(ang), S("#8A8272", 3.0, 235 * min(1, kk * 2)))
        c.drawCircle(px, py, 11, P("#C4A04A", 255 * min(1, kk * 2)))
    L.end(cx, cam, motes_n=18)
    L.tag(f, cx, "MICHELOZZO", 1420, 250, at=("c3s14", "Michelozzo", 0.0), size=40, sub="MİMAR", w=480)


@CM.ckind("c3_michelozzo")
def k_michelozzo(cx, **kw):
    k_michelozzo_impl(cx, **kw)


# ═══════════════════════════ c3s15: Floransa'da rüzgâr değişiyordu ═══════════════════════════
def k_ruzgar_impl(cx, **_):
    f = cx.f
    c = f.c
    t = cx.t
    T = CT.Tint("day")
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    f.clear("#9CBBDC")
    cam.begin(f)
    t_flip = cx.at(("c3s15", "değişiyordu", -0.35))
    kf = smooth(clamp((t - t_flip) / 0.8))              # 0: rüzgâr sola, 1: rüzgâr sağa
    wind = -1.0 + 2.0 * kf
    # gök
    sh = skia.GradientShader.MakeLinear([(0, -400), (0, 900)], [C("#6F9ED6"), C("#BDD0DC"), C("#F4E8C8")], [0.0, 0.62, 1.0])
    c.drawRect(skia.Rect.MakeLTRB(-600, -500, 2520, 1000), skia.Paint(Shader=sh))
    # bulutlar: rüzgârla akar
    for i in range(7):
        base = _RS(i + 4).uniform(-300, 2200)
        spd = 26.0 * (0.6 + 0.2 * (i % 3))
        # hız yönü rüzgârla yumuşakça döner
        posx = base + spd * (-t * 1.0 + 2.2 * (t - t_flip) * smooth(clamp((t - t_flip) / 1.2)) * 0.0)
        # sürekli konum: ∫wind dt
        w_int = -t + 2.0 * max(0.0, (t - t_flip) - 0.4) * (1 if t > t_flip else 0) * 0.5
        px = base + spd * w_int
        py = 160 + 80 * (i % 4)
        for j in range(5):
            SOFT(c, px + j * 74, py + math.sin(j + i) * 14, 120 + 22 * j % 40, 34, "#FFFFFF", 150)
    # uzak tepeler
    for (col, amp, sc, base, ph) in (("#A9BDB6", 40, 600, 640, 0.0), ("#8FAEA2", 46, 420, 700, 2.1)):
        pts = []
        x = -600
        while x <= 2520:
            pts.append((x, 1000 - L.PN.ridge_y(x, base - 300, amp, sc, ph)))
            x += 14
        c.drawPath(sk.poly_path(pts + [(2520, 1100), (-600, 1100)]), P(T(col, 0.2)))
    # çatılar
    rr = _RS(31)
    wins = []
    x = -600
    while x < 2520:
        bw, bh = rr.uniform(120, 220), rr.uniform(110, 230)
        CT.draw_house(c, x, 900, bw, bh, _RS(int(rr.randint(1, 10 ** 6))), T, 0.18, wins)
        x += bw + rr.uniform(-10, 8)
    GRAD_V(c, -600, 900, 2520, 1200, [(T("#B8A888", 0.2), 0.0), (T("#A89A78", 0.1), 1.0)])
    # kule + sancak
    TX = 960.0
    TW, TH_ = 150.0, 330.0
    gd = SE.vecchio_tower(c, TX, 940, TW, TH_, T, 0.0, 77, roof_h=TW * 0.95)
    pole_top = gd["flag"][1]
    TX = gd["flag"][0]
    # sancak: ana eksende dönen kırlangıç kuyruklu flama
    fl = 120.0
    ang = math.pi * (1.0 - kf)                     # π: sola, 0: sağa
    sx = math.cos(ang)
    c.save()
    c.translate(TX, pole_top + 8)
    c.scale(0.8, 0.8)
    pts_t, pts_b = [(0, 0)], [(0, 46)]
    n = 12
    for k in range(1, n + 1):
        u = k / n
        wv = math.sin(t * 6.2 - u * 3.6) * 9 * u * (0.4 + 0.6 * abs(sx))
        pts_t.append((u * fl * sx, wv))
        pts_b.append((u * fl * sx, 46 + wv * 1.1))
    pts = pts_t + [(fl * 0.8 * sx, 23 + math.sin(t * 6.2 - 3.2) * 5)] + pts_b[::-1]
    c.drawPath(sk.poly_path(pts), P("#B3301F"))
    c.drawPath(sk.poly_path(pts), S("#2A1A0C", 2.2, 220))
    c.restore()
    # bacalar ve duman: rüzgâra yatar
    for i, bx in enumerate((300, 620, 1300, 1560, 1800)):
        by = 900 - 210 - (i % 3) * 20
        R(c, bx, by - 70, bx + 34, by + 4, T("#A8684A"))
        INKR(c, bx, by - 70, bx + 34, by + 4, 1.2, 180)
        for k in range(8):
            ph = (t * 0.5 + k / 8.0 + i * 0.13) % 1.0
            sx_ = bx + 17 + wind * (ph * 120) + math.sin(ph * 6 + i) * 8
            sy_ = by - 80 - ph * 140
            SOFT(c, sx_, sy_, 16 + 34 * ph, 14 + 26 * ph, "#C8C0B4", 120 * (1 - ph))
    # kuşlar rüzgârla
    for i in range(5):
        ph = (t * (0.07 + 0.01 * i) + i * 0.2) % 1.0
        bx = (900 + wind * 0 + (ph - 0.5) * 1700) if wind < 0 else (900 - (ph - 0.5) * 1700)
        by = 250 + i * 55 + math.sin(t * 1.4 + i) * 14
        flp = math.sin(t * 10 + i * 2) * 6
        pth = skia.Path()
        pth.moveTo(bx - 12, by + flp * 0.4)
        pth.quadTo(bx - 5, by - 7 - flp, bx, by)
        pth.quadTo(bx + 5, by - 7 - flp, bx + 12, by + flp * 0.4)
        c.drawPath(pth, S("#3A342C", 2.6, 200))
    cam.end(f)
    CM.finish(f, cx, motes_n=14)


@CM.ckind("c3_ruzgar")
def k_ruzgar(cx, **kw):
    k_ruzgar_impl(cx, **kw)


# ═══════════════════════════ c3s16: kura (torbalar) → Rinaldo'nun kurul girişimi ═══════════════════════════
def arm_to(c, shoulder, target, s=1.0, col="#7A5A3A", sleeve="#4A3422", open_=0.0, a=255):
    dx, dy = target[0] - shoulder[0], target[1] - shoulder[1]
    ang = math.degrees(math.atan2(dy, dx))
    reach = max(40.0, math.hypot(dx, dy) - 34 * s * 0.95)
    return L.hand_arm(c, shoulder[0], shoulder[1], ang, reach, s=s, col=col, sleeve=sleeve, open_=open_, a=a)


def draw_palle_badge(c, x, y, s=1.0, a=255):
    """Küçük Medici işareti (altı top): kâğıt/torba üstü damga."""
    for (dx, dy, rr) in CM.PALLE_POS:
        px, py = x + (dx - 0.5) * 34 * s, y + (dy - 0.52) * 34 * s
        c.drawCircle(px, py, rr * 34 * s * 0.5, P("#A8321E", a))
        c.drawCircle(px, py, rr * 34 * s * 0.5, S("#3A1008", 0.8, 160 * a / 255))


def k_kura_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=3, dress=None)
    t = cx.t
    GY = 880.0
    # ── sağ: torba panosu (tahta pano + mandallar) ──
    BX0, BX1, BY0, BY1 = 1230.0, 2000.0, 190.0, 560.0
    GRAD_V(c, BX0, BY0, BX1, BY1, [("#8A5A38", 0.0), ("#5E3A20", 1.0)])
    for k_ in range(6):
        c.drawLine(BX0, BY0 + k_ * 62, BX1, BY0 + k_ * 62 + 3, S("#2A1608", 1.3, 110))
    INKR(c, BX0, BY0, BX1, BY1, 2.4, 220)
    bag_x = [1310 + i * 120 for i in range(6)]
    rs = _RS(11)
    for i, bx in enumerate(bag_x):
        # mandal + sallanan torba
        c.drawCircle(bx, BY0 + 40, 7, P("#2A1A0C"))
        sw = 3.0 * math.sin(t * 1.3 + i * 1.1) + 1.2 * math.sin(t * 2.7 + i)
        L.draw_bag(c, bx, BY0 + 150 + (i % 2) * 18, s=1.18, seed=i + 2, sway=sw, slips=2)
    # ── masa + sıralanan kâğıtlar ──
    table_persp(c, 1150, 2060, 760, 880, apron=70, col="#7A4A28", depth=0.07)
    t_draw0 = cx.at(("c3s16", "kura", -0.2))
    nslot = 5
    per = 0.62
    slot_x = [1360 + i * 125 for i in range(nslot)]
    hand_pos = None
    for i in range(nslot):
        tp = t_draw0 + i * per
        u = (t - tp) / per
        bi = (i * 2 + 1) % 6
        bagp = (bag_x[bi], BY0 + 150 + (bi % 2) * 18 - 70)
        slot = (slot_x[i], 800)
        if u < -0.05 or (u > 1.0 and False):
            continue
        if u < 0:
            continue
        if u >= 1.0:
            # yerleşmiş kâğıt (palle damgalı)
            L.draw_slip(c, slot[0], slot[1], w=96, h=66, rot=0.05 * ((-1) ** i), lines=1, seed=i + 3)
            draw_palle_badge(c, slot[0] + 0, slot[1] + 6, s=0.9)
            continue
        rest = (bagp[0] + 150, bagp[1] - 170)
        if u < 0.28:
            k = ease_io(u / 0.28, 2)
            tgt = (lerp(rest[0], bagp[0], k), lerp(rest[1], bagp[1], k))
            slip_p = None
        elif u < 0.45:
            k = ease_out((u - 0.28) / 0.17, 2)
            tgt = (bagp[0], bagp[1] - 60 * k)
            slip_p = (bagp[0], bagp[1] - 60 * k + 20)
        elif u < 0.88:
            k = ease_io((u - 0.45) / 0.43, 2)
            tgt = (lerp(bagp[0], slot[0], k), lerp(bagp[1] - 60, slot[1] - 90, k) - math.sin(math.pi * k) * 70)
            slip_p = (tgt[0], tgt[1] + 24)
        else:
            k = (u - 0.88) / 0.12
            tgt = (slot[0] + 80 * k, slot[1] - 90 - 120 * k)
            slip_p = (slot[0], slot[1] - (1 - k) * 66)
        arm_to(c, (tgt[0] + 300, -140), tgt, s=2.4, sleeve="#4A3422")
        if slip_p is not None:
            L.draw_slip(c, slip_p[0], slip_p[1], w=96, h=66, rot=0.2 * (u - 0.5), lines=1, seed=i + 3)
            if u > 0.45:
                draw_palle_badge(c, slip_p[0], slip_p[1] + 6, s=0.9)
    # ── sol: Rinaldo ve kurul girişimi ──
    sx0 = 200.0
    # zemin
    L.grid_floor(c, -400, 1180, GY, 1200)
    # yazı masası + yazıcı + mühür
    table_persp(c, 330, 950, 770, 880, apron=62, col="#6A4426", depth=0.07)
    k_sheet = cx.amt(("c3s16", "olağanüstü", -0.3), 0.6)
    if k_sheet > 0.003:
        pp = PP_sheet(250, 170, seed=18)
        pp.draw(f, 640, 820, rot=-0.03, scale=0.9, alpha=k_sheet, shadow=0.55)
        # satır çizgileri (yazılıyor)
        kw_ = clamp((t - cx.at(("c3s16", "olağanüstü", -0.2))) / 1.4)
        for j in range(4):
            wj = 150 * clamp(kw_ * 4 - j)
            c.drawLine(550, 790 + j * 18, 550 + wj, 790 + j * 18 + math.sin(j) * 2, S("#3A2616", 2.0, 210))
        CM.wax_seal(f, 730, 835, 30, "#A52A1C", alpha=1.0, t=cx.amt(("c3s16", "kurul", 0.0), 0.35), palle=False, mono="A")
    ka = cx.amt(("c3s16", "Rinaldo", -0.2), 0.7)
    L.sil(f, "soylu", sx0, 872, 372, t, action="point" if t >= cx.at(("c3s16", "karşı", -0.2)) else "talk", dir=1, seed=23, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=ka,
          t0=cx.at(("c3s16", "karşı", -0.2)), dur=2.5, target=(1.0, -0.2))
    L.sil(f, "banker", 700, 878, 330, t, action="write", dir=-1, seed=9, color="#1A1410", rim="#FFE2A0", rim_dir=-1, alpha=ka) if False else None
    # haberciler (sola koşar: tehdit yönü)
    tm = cx.at(("c3s16", "toplatmaya", -0.1))
    for j in range(3):
        u = (t - (tm + 0.28 * j))
        if u < 0:
            continue
        x = 980 - 330 * u
        L.walker(f, ["tuccar", "halk", "banker"][j], x, GY + 96 + 18 * j, 340, t, speed=330, dir=-1, run=True, seed=30 + j, phase=0.3 * j)
    cam.end(f)
    CM.finish(f, cx, motes_n=18)
    L.tag(f, cx, "SIGNORIA", 1560, 960 - 40, at=("c3s16", "Signoria", 0.0), size=36, w=300, hold=("c3s16", "Rinaldo", -0.2))
    L.tag(f, cx, "AĞUSTOS SONU", 1560, 150, at=("c3s16", "Ağustos", 0.0), size=34, w=400, hold=("c3s16", "Cosimo", 0.5)) if False else None


@CM.ckind("c3_kura")
def k_kura(cx, **kw):
    k_kura_impl(cx, **kw)


# ═══════════════════════════ c3s17: sürgün kararı kalktı (ilan rüzgârla uçar) ═══════════════════════════
def k_ilan_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=1, dress=None)
    t = cx.t
    # pano
    bx, by, bw, bh = 960.0, 560.0, 560.0, 760.0
    GRAD_V(c, bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2, [("#8A5A38", 0.0), ("#5E3A20", 1.0)])
    for k_ in range(10):
        c.drawLine(bx - bw / 2, by - bh / 2 + k_ * 76, bx + bw / 2, by - bh / 2 + k_ * 76 + 3, S("#2A1608", 1.3, 110))
    INKR(c, bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2, 3.0, 230)
    t_up = cx.at(("c3s17", "kalktı;", -0.5))
    k = clamp((t - t_up) / 1.0)
    nails = [(-120, -230), (120, -230), (-120, 210), (120, 210)]
    for i, (nx, ny) in enumerate(nails):
        hop = 0.0
        if k > 0 and i < 2:
            hop = -26 * min(1, k * 4)
        c.drawCircle(bx + nx, by + ny + hop, 7, P("#2A2620"))
        c.drawCircle(bx + nx - 2, by + ny + hop - 2, 2.4, P("#9A9484"))
    # ilan
    if k < 1.0:
        e = ease_in(k, 2.2)
        x = bx + 280 * e + math.sin(k * 14) * 18 * k
        y = by - 1000 * e + math.sin(k * 9 + 1) * 24 * k
        rot = -0.02 + 0.9 * e * math.sin(k * 7)
        sc = 1.0 - 0.35 * e
        pp = PP_sheet(380, 520, seed=33)
        pp.draw(f, x, y, rot=rot, scale=sc, alpha=1.0, shadow=0.55)
        c.save()
        c.translate(x, y)
        c.rotate(math.degrees(rot))
        c.scale(sc, sc)
        PP_hand(f, "SÜRGÜN", 0, -40, 62, "#2A1A0E", 1.0, seed=2)
        PP_hand(f, "KARARI", 0, 40, 50, "#2A1A0E", 1.0, seed=3)
        c.drawLine(-130, 120, 130, 120, S("#3A2616", 2.0, 180))
        c.drawLine(-110, 150, 90, 150, S("#3A2616", 2.0, 150))
        CM.wax_seal(f, 90, 190, 26, "#A52A1C", alpha=1.0, t=1.0, mono="S")
        c.restore()
    # rüzgâr çizgileri (sağa, yukarı): yön değişti
    kw_ = cx.amt(("c3s17", "sürgün", 0.0), 0.6)
    for i in range(7):
        ph = (t * 0.8 + i * 0.173) % 1.0
        x0 = -100 + ph * 2100
        y0 = 700 - i * 70 - ph * 160
        pth = skia.Path()
        pth.moveTo(x0, y0)
        pth.cubicTo(x0 + 80, y0 - 26, x0 + 150, y0 + 22, x0 + 230, y0 - 8)
        c.drawPath(pth, S("#6A5A44", 2.4, 100 * kw_ * math.sin(math.pi * ph)))
    cam.end(f)
    CM.finish(f, cx, motes_n=16)
    L.tag(f, cx, "EYLÜL SONU", 1500, 200, at=("c3s17", "Eylül", 0.0), size=34, w=380, hold=("c3s17", "kalktı;", 0.2))


@CM.ckind("c3_ilan")
def k_ilan(cx, **kw):
    k_ilan_impl(cx, **kw)


# ═══════════════════════════ c3s17b: 6 Ekim 1434 — yalnız yolcu surlara yürür ═══════════════════════════
def k_donus_impl(cx, **_):
    f = cx.f
    c = f.c
    t = cx.t
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    far, mid, near = _out_layers()
    cam.begin(f)
    c.drawRect(skia.Rect.MakeLTRB(-800, -600, 2800, 1500), P("#9CBBDC"))
    ox = 0.0
    blit(c, far, 960, 520, ax=0.5, ay=0.5, sx=1.15)
    blit(c, mid, 960 + 60, 520 + 54, ax=0.5, ay=0.5, sx=1.15)
    # önde: yol + sur + kapı kulesi (sağda)
    T = CT.Tint("day")
    GY = 900.0
    GRAD_V(c, -800, GY - 30, 2800, 1300, [("#BFB08A", 0.0), ("#8E7E5C", 1.0)])
    c.drawLine(-800, GY - 30, 2800, GY - 30, S("#2A1A0C", 2.0, 160))
    # yol (perspektifte daralan şerit)
    road = [(-400, 1200), (400, GY - 28), (1500, GY - 28), (2300, 1200)]
    c.drawPath(sk.poly_path(road), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, GY), (0, 1200)], [C("#D8C99C"), C("#B8A878")], [0, 1])))
    # sur
    WX0 = 1400.0
    SE.stone_wall(c, WX0, GY - 360, 2800, GY - 20, "#B4A27C", T, 0.0, 5, ch=30.0, bw=(80, 130), rustic=False)
    for k_ in range(14):                                           # mazgallar
        R(c, WX0 + k_ * 100, GY - 400, WX0 + k_ * 100 + 56, GY - 360, T("#A8966E"))
        INKR(c, WX0 + k_ * 100, GY - 400, WX0 + k_ * 100 + 56, GY - 360, 1.2, 170)
    INKR(c, WX0, GY - 360, 2800, GY - 20, 2.0, 190)
    # kapı kulesi
    KX = 1760.0
    SE.stone_wall(c, KX - 170, GY - 560, KX + 170, GY - 20, "#BBA880", T, 0.0, 9, ch=30.0, bw=(80, 130), rustic=False)
    INKR(c, KX - 170, GY - 560, KX + 170, GY - 20, 2.2, 200)
    for k_ in range(4):
        R(c, KX - 170 + k_ * 96, GY - 604, KX - 170 + k_ * 96 + 54, GY - 560, T("#A8966E"))
        INKR(c, KX - 170 + k_ * 96, GY - 604, KX - 170 + k_ * 96 + 54, GY - 560, 1.2, 170)
    gp = skia.Path()
    gp.moveTo(KX - 78, GY - 20)
    gp.lineTo(KX - 78, GY - 230)
    gp.cubicTo(KX - 78, GY - 330, KX + 78, GY - 330, KX + 78, GY - 230)
    gp.lineTo(KX + 78, GY - 20)
    gp.close()
    c.drawPath(gp, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, GY - 330), (0, GY - 20)], [C("#1A100A"), C("#6A4A2A")], [0, 1])))
    INKP(c, gp, 2.4, 230)
    SOFT(c, KX, GY - 100, 160, 120, "#FFE2A0", 70 + 20 * math.sin(t * 1.5))
    # yalnız yolcu: soldan yürür
    u = clamp(t / max(1.0, cx.dur))
    px = 300 + 1180 * ease_io(u, 1.4)
    L.walker(f, "soylu", px, GY + 76 - 0.06 * (px - 300), 250, t, speed=150, dir=1, seed=4, phase=0.0, stil=None) if False else L.walker(f, "soylu", px, GY + 78 - 0.05 * (px - 300), 250 - 0.03 * (px - 300), t, speed=150 if u < 0.97 else 0, dir=1, seed=4, phase=0.0)
    cam.end(f)
    CM.finish(f, cx, motes_n=14)
    L.engr(f, cx, "6 EKİM 1434", 960, 250, ("c3s17", "Ekim", -0.1), size=84, track=14, dur=1.2, glow=0.15)


@CM.ckind("c3_donus")
def k_donus(cx, **kw):
    k_donus_impl(cx, **kw)


# ═══════════════════════════ c3s18: Albizzi'lerin ıssız konakları ═══════════════════════════
def _issiz_strip(fr):
    c = fr.c
    T = CT.Tint("day")
    GYs = 960.0
    sh = skia.GradientShader.MakeLinear([(0, 0), (0, 560)], [C("#9CBBDC"), C("#E8E4D0")], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(0, 0, 4200, 700), skia.Paint(Shader=sh))
    # arkada çatı sırası
    rr = _RS(5)
    wins0 = []
    x = -40
    while x < 4300:
        bw, bh = rr.uniform(120, 220), rr.uniform(220, 360)
        CT.draw_house(c, x, 560, bw, bh, _RS(int(rr.randint(1, 10 ** 6))), T, 0.40, wins0)
        x += bw + rr.uniform(-8, 10)
    R(c, 0, 556, 4200, 700, T("#B8A888", 0.3))
    wins = SE.street_facade(c, 0, 4200, 0, 4200, GYs, 700, T, seed=8, door_x=-99999, arch_x=-99999)
    for (xc, yb, w, h, kat) in wins:                       # kepenkler kapalı (konaklar ıssız)
        x0, x1 = xc - w / 2, xc + w / 2
        c.drawRect(skia.Rect.MakeLTRB(x0, yb - h, x1, yb), P("#5A3C22"))
        for k_ in range(5):
            c.drawLine(x0, yb - h + (k_ + 0.5) * h / 5, x1, yb - h + (k_ + 0.5) * h / 5, S("#2A1608", 1.3, 190))
        c.drawLine((x0 + x1) / 2, yb - h, (x0 + x1) / 2, yb, S("#2A1608", 1.6, 200))
        INKR(c, x0, yb - h, x1, yb, 1.6, 220)
    # kapalı ağır kapılar
    for dx in (700, 1900, 3100):
        SE.portal(c, dx, GYs, 190, 340, T)
        c.drawRect(skia.Rect.MakeLTRB(dx - 70, GYs - 300, dx + 70, GYs), P("#3E2A16"))
        for k_ in range(4):
            c.drawLine(dx - 70, GYs - 300 + k_ * 75, dx + 70, GYs - 300 + k_ * 75, S("#1A1008", 5.0, 230))
        c.drawCircle(dx, GYs - 150, 11, S("#2A2620", 3.0, 240))
        INKR(c, dx - 70, GYs - 300, dx + 70, GYs, 2.0, 230)
    L.PN.draw_pavement(c, 0, 4200, GYs - 6, 1220, T, seed=3)


def k_issiz_impl(cx, **_):
    f = cx.f
    c = f.c
    t = cx.t
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    im = bake(("issiz_strip", 2), 4200, 1300, _issiz_strip)
    cam.begin(f)
    c.drawRect(skia.Rect.MakeLTRB(-600, -800, 5000, 1900), P("#9CBBDC"))
    c.save()
    c.translate(-1100, -20)
    c.drawImage(im, 0, 0, L.LIN)
    c.restore()
    GY = 960.0 - 20
    # gevşek kepenk (rüzgârda sallanır): ıssızlık
    sx0 = 1300.0
    sw = math.sin(t * 1.7) * 0.5 + math.sin(t * 3.1) * 0.2
    c.save()
    c.translate(sx0, 480)
    c.rotate(math.degrees(0.20 * sw))
    c.drawRect(skia.Rect.MakeLTRB(0, 0, 54, 150), P("#6A4426"))
    INKR(c, 0, 0, 54, 150, 1.6, 220)
    for k_ in range(5):
        c.drawLine(0, 15 + k_ * 30, 54, 15 + k_ * 30, S("#2A1608", 1.2, 170))
    c.restore()
    # yalnız yürüyüş: kapıların önünden
    u = clamp(t / max(1.0, cx.dur))
    px = 130 + 1500 * ease_io(u, 1.3)
    L.walker(f, "soylu", px, GY - 12, 300, t, speed=96 if u < 0.97 else 0.0, dir=1, seed=4, phase=0.0)
    # uçuşan kâğıt/yaprak
    for i in range(5):
        ph = (t * 0.15 + i * 0.21) % 1.0
        x = -200 + ph * 2400
        y = GY - 40 - 90 * abs(math.sin(ph * 9 + i)) - 20 * i
        c.save()
        c.translate(x, y)
        c.rotate(math.degrees(ph * 14 + i))
        c.drawRect(skia.Rect.MakeLTRB(-9, -6, 9, 6), P("#C8B88A", 200))
        c.restore()
    cam.end(f)
    CM.finish(f, cx, motes_n=16)
    L.stamp_src(f, cx, "TEK KAYNAK", 1530, 220, at=("c3s18", "anlatılır", -0.3), size=40, rot=-0.07)


@CM.ckind("c3_issiz")
def k_issiz(cx, **kw):
    k_issiz_impl(cx, **kw)


# ═══════════════════════════ c3s19: Rinaldo ve Strozzi sürgüne yürür (sağdan sola) ═══════════════════════════
def draw_city_gate(c, T, GY, KX, t, walls=True):
    GRAD_V(c, -800, GY - 30, 3200, 1500, [("#BFB08A", 0.0), ("#8E7E5C", 1.0)])
    c.drawLine(-800, GY - 30, 3200, GY - 30, S("#2A1A0C", 2.0, 160))
    road = [(-600, 1300), (300, GY - 28), (2200, GY - 28), (3100, 1300)]
    c.drawPath(sk.poly_path(road), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, GY), (0, 1300)], [C("#D8C99C"), C("#B8A878")], [0, 1])))
    if walls:
        SE.stone_wall(c, KX - 1500, GY - 360, KX + 1500, GY - 20, "#B4A27C", T, 0.0, 5, ch=30.0, bw=(80, 130), rustic=False)
        for k_ in range(30):
            R(c, KX - 1500 + k_ * 100, GY - 400, KX - 1500 + k_ * 100 + 56, GY - 360, T("#A8966E"))
            INKR(c, KX - 1500 + k_ * 100, GY - 400, KX - 1500 + k_ * 100 + 56, GY - 360, 1.2, 170)
        INKR(c, KX - 1500, GY - 360, KX + 1500, GY - 20, 2.0, 190)
    SE.stone_wall(c, KX - 190, GY - 580, KX + 190, GY - 20, "#BBA880", T, 0.0, 9, ch=30.0, bw=(80, 130), rustic=False)
    INKR(c, KX - 190, GY - 580, KX + 190, GY - 20, 2.2, 200)
    for k_ in range(4):
        R(c, KX - 190 + k_ * 107, GY - 626, KX - 190 + k_ * 107 + 60, GY - 580, T("#A8966E"))
        INKR(c, KX - 190 + k_ * 107, GY - 626, KX - 190 + k_ * 107 + 60, GY - 580, 1.2, 170)
    gp = skia.Path()
    gp.moveTo(KX - 88, GY - 20)
    gp.lineTo(KX - 88, GY - 240)
    gp.cubicTo(KX - 88, GY - 350, KX + 88, GY - 350, KX + 88, GY - 240)
    gp.lineTo(KX + 88, GY - 20)
    gp.close()
    c.drawPath(gp, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, GY - 350), (0, GY - 20)], [C("#1A100A"), C("#6A4A2A")], [0, 1])))
    INKP(c, gp, 2.4, 230)
    SOFT(c, KX, GY - 100, 170, 120, "#FFE2A0", 60 + 15 * math.sin(t * 1.5))


def k_surgun_kapi_impl(cx, **_):
    f = cx.f
    c = f.c
    t = cx.t
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    far, mid, near = _out_layers()
    cam.begin(f)
    c.drawRect(skia.Rect.MakeLTRB(-1200, -800, 3600, 1600), P("#9CBBDC"))
    blit(c, far, 960, 480, ax=0.5, ay=0.5, sx=1.2)
    T = CT.Tint("day")
    GY = 900.0
    KX = 1500.0
    draw_city_gate(c, T, GY, KX, t)
    t0 = cx.at(("c3s19", 0.0))
    for j, (kd, sd, dy, ph, col) in enumerate((("soylu", 23, 74, 0.0, dict(robe="#7A2A22", robe2="#C79A3C", hat_col="#2A1A10")), ("banker", 44, 108, 0.5, dict(robe="#2F5A8A", robe2="#E0B84E", hat_col="#8A2A1E")))):
        u = t - (t0 + 0.7 + 0.45 * j)
        if u < 0:
            continue
        x = KX - 40 - 112 * u
        L.walker(f, kd, x, GY + dy, 300 - dy * 0.1, t, speed=112, dir=-1, seed=sd, phase=ph, prop="sack", **col)
    cam.end(f)
    CM.finish(f, cx, motes_n=12)
    L.tag(f, cx, "RINALDO DEGLI ALBIZZI", 520, 230, at=("c3s19", "Rinaldo", 0.0), size=34, w=520, hold=("c3s19", "ile,", 0.7))
    L.tag(f, cx, "PALLA STROZZI", 1400, 230, at=("c3s19", "Strozzi", -0.1), size=36, sub="1427 · EN ZENGİN SAYILAN", w=520)
    L.stamp_at(f, cx, "SÜRGÜN", 1560, 420, at=("c3s19", "sürgüne", 0.0), size=64, rot=-0.08)


@CM.ckind("c3_surgun_kapi")
def k_surgun_kapi(cx, **kw):
    k_surgun_kapi_impl(cx, **kw)


# ═══════════════════════════ c3s20: boş koltuk, gölge, takılmayan taç, otuz yıl ═══════════════════════════
def k_koltuk_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=2, dress=None)
    t = cx.t
    T = L.OD.OTint("day")
    FY = 880.0
    # zemin (tahta) + süpürgelik
    L.OD.floor_planks(c, -600, 2520, FY, 1300, T, col="#8A6038", seed=5)
    R(c, -600, FY - 36, 2520, FY, T("#6E4524"))
    c.drawLine(-600, FY, 2520, FY, S("#1E1208", 2.0, 200))
    # pencere + gün ışığı lekesi
    L.OD.draw_window(c, T, 360, 180, 230, 460, night=False)
    pts = [(300, FY + 14), (560, FY + 14), (1120, FY + 140), (700, FY + 140)]
    c.drawPath(sk.poly_path(pts), P("#FFF0C0", 70))
    c.drawPath(sk.poly_path([(250, 640), (470, 640), (1020, FY + 10), (640, FY + 10)]), P("#FFF4D0", 36))
    # dev gölge (duvarda): 'bu adam'
    ks = cx.amt(("c3s20", "adam,", 0.0), 1.0)
    sh = 0.30 * ks
    L.sil(f, "soylu", 1430, FY + 20, 1000, t, action="idle", dir=-1, seed=4, color="#000000", rim=None, rim_dir=1, alpha=sh)
    # boş koltuk
    L.OD.draw_chair(c, T, 960, FY, back_h=320, seat_h=86, w=120, facing=1, col="#6E4524", cushion="#8E2A30")
    SOFT(c, 960, FY + 8, 190, 22, "#000000", 90)
    # taç: iner, koltuğa konmaz, kalkar
    t_c = cx.at(("c3s20", "taç", 0.0))
    t_k = cx.at(("c3s20", "takmadan", 0.0))
    kd = ease_out(clamp((t - (t_c - 0.9)) / 0.9), 3)
    ku = ease_in(clamp((t - (t_k + 0.15)) / 0.8), 2)
    if kd > 0.003 and ku < 1.0:
        cy = lerp(-160, 520, kd) - 700 * ku + 12 * math.sin(t * 3.1) * kd
        al = 1.0 - ku
        SOFT(c, 960, cy + 40, 200, 90, "#FFE9A0", 120 * al * kd)
        icons.draw_icon(f, "crown", 960, cy, size=220, metal="gold", alpha=al, glow=0.25 * al, shadow=False)
        if kd > 0.99 and ku < 0.02:                       # koltuğa değmeden asılı kalır: kısa titreşim
            c.drawLine(900, cy + 130, 1020, cy + 130, S("#C79A3C", 2.0, 120))
    # otuz yıl cetveli (duvarda)
    kk = ease_io(cx.amt(("c3s20", "otuz", 0.0), 0.9), 2)
    if kk > 0.003:
        x0, x1, yy = 340.0, 1580.0, 250.0
        c.drawLine(x0, yy, x0 + (x1 - x0) * kk, yy, S(TH.rule, 4.0, 235))
        n = 30
        for i in range(n + 1):
            if i / n <= kk:
                big = i in (0, 30)
                c.drawLine(x0 + (x1 - x0) * i / n, yy - (16 if big else 8), x0 + (x1 - x0) * i / n, yy + (16 if big else 8), S(TH.rule, 2.0, 220))
        CM.ink(f, "1434", x0, yy + 56, face="title_m", size=30, color=TH.fg2, align="c", alpha=kk, track=4, emboss=False)
        if kk > 0.97:
            CM.ink(f, "1464", x1, yy + 56, face="title_m", size=30, color=TH.fg2, align="c", alpha=1.0, track=4, emboss=False)
        L.engr(f, cx, "30 YIL", 960, 180, ("c3s20", "otuz", 0.1), size=74, track=16, style="gilt", dur=0.8, glow=0.2)
    L.end(cx, cam, motes_n=18)


@CM.ckind("c3_koltuk")
def k_koltuk(cx, **kw):
    k_koltuk_impl(cx, **kw)


# ═══════════════════════════ c3s21: Papa II. Pius'a göre: adı ve statüsü dışında bir kral ═══════════════════════════
def k_kral_impl(cx, **_):
    import cilt_props as CP
    f, c, cam = L.begin(cx, bg="wall", seed=1, dress="both")
    t = cx.t
    # üst etiket + Papa anahtarları
    k0 = cx.amt(("c3s21", "Pius'a", 0.0), 0.6)
    if k0 > 0.003:
        icons.draw_icon(f, "keys", 720, 100, size=84, metal="gold", alpha=k0, shadow=False)
        L.tag(f, cx, "II. PIUS'A GÖRE", 1010, 100, at=("c3s21", "Pius'a", 0.0), size=36, w=520)
    # palle kalkanı
    ks = cx.amt(("c3s21", "Papa", 0.0), 0.7)
    if ks > 0.003:
        CP.draw_arms(f, 960, 700, 380 * (0.92 + 0.08 * ease_out(ks)), alpha=ks, shadow=0.6, glow=0.0, glint=((t * 0.3) % 2.0) if (t * 0.3) % 2.0 < 1 else None)
    # hayalet taç (kesikli) → 'bir kraldı' ile altın dolar
    kg = cx.amt(("c3s21", "kraldı.", -0.15), 0.7)
    kcr = cx.amt(("c3s21", "Cosimo,", 0.3), 0.8)
    if kcr > 0.003:
        cy = 330 + 6 * math.sin(t * 2.0)
        icons.draw_icon(f, "crown", 960, cy, size=250, metal="gold", alpha=(0.22 + 0.78 * kg) * kcr, glow=0.30 * kg, shadow=False)
        halo = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.0, Color=C("#C79A3C", int(220 * kcr)))
        halo.setPathEffect(skia.DashPathEffect.Make([18.0, 12.0], -t * 40))
        c.drawOval(skia.Rect.MakeLTRB(960 - 190, cy - 112, 960 + 190, cy + 124), halo)
        if kg > 0.4:
            for i in range(8):
                a_ = i * 0.785 + t * 0.6
                SOFT(c, 960 + math.cos(a_) * 170, cy + math.sin(a_) * 100, 16, 16, "#FFF2B0", 150 * kg)
    # 'adı' ve 'hukuki statüsü' levhaları → dışında: karalanır
    for (txt, x, an, off) in (("ADI", 420.0, ("c3s21", "adı", -0.1), 0.0), ("HUKUKİ STATÜSÜ", 1500.0, ("c3s21", "hukuki", -0.1), 0.0)):
        kp = cx.amt(an, 0.45)
        if kp <= 0.003:
            continue
        wd = sk.text_width(txt, "title_m", 34, 6) + 80
        CM.tablet(f, x - wd / 2, 560 - 40 + (1 - kp) * 14, wd, 84, alpha=kp * (1 - 0.35 * cx.amt(("c3s21", "dışında", 0.0), 0.5)), corner=8)
        CM.ink(f, txt, x, 560 + 14, face="title_m", size=34, color=TH.fg, align="c", track=6, alpha=kp, emboss=False)
        kx = ease_io(cx.amt(("c3s21", "dışında", 0.0), 0.5), 2)
        if kx > 0.003:
            p_ = skia.Path()
            p_.moveTo(x - wd / 2 + 8, 560 + 4)
            p_.lineTo(x - wd / 2 + 8 + (wd - 16) * kx, 560 - 10)
            pp2 = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7, Color=C("#8E2A1E", 235), StrokeCap=skia.Paint.kRound_Cap)
            pp2.setPathEffect(skia.DiscretePathEffect.Make(9.0, 1.6, 4))
            c.drawPath(p_, pp2)
    L.end(cx, cam, motes_n=22)


@CM.ckind("c3_kral")
def k_kral(cx, **kw):
    k_kral_impl(cx, **kw)


# ═══════════════════════════ c3s22: düzenin sırrı — dolabın açılışı, torbalar, kurayla çekilen Signoria ═══════════════════════════
def draw_cabinet(c, x, yb, w, h, open_k, T=None, t=0.0, bags=True, seed=1, key_k=0.0):
    """Çift kanatlı ahşap dolap (ön görünüş). open_k 0..1: kanatlar yana açılır (perspektifle daralır); içinde 3 sıra torba."""
    x0, x1 = x - w / 2, x + w / 2
    # gövde (arka)
    GRAD_V(c, x0, yb - h, x1, yb, [("#3A2412", 0.0), ("#1E1208", 1.0)])
    if bags:
        rs = _RS(seed)
        for row in range(3):
            yy = yb - h + 40 + row * (h - 60) / 3
            c.drawLine(x0 + 12, yy + (h - 60) / 3 - 22, x1 - 12, yy + (h - 60) / 3 - 22, S("#8A5A38", 8.0, 230))
            for k_ in range(3):
                bx = x0 + w * (0.20 + 0.30 * k_)
                sw = 2.2 * math.sin(t * 1.4 + row + k_)
                L.draw_bag(c, bx, yy + 70, s=0.82, seed=seed + row * 3 + k_, sway=sw, slips=1)
    INKR(c, x0, yb - h, x1, yb, 3.0, 230)
    # kanatlar
    for sgn in (-1, 1):
        wd = (w / 2) * (1.0 - 0.86 * ease_io(open_k, 2))
        hx = x + sgn * w / 2                      # menteşe dışta
        xa, xb = (hx - wd, hx) if sgn < 0 else (hx, hx + wd)
        if sgn < 0:
            xa, xb = x0, x0 + wd
        else:
            xa, xb = x1 - wd, x1
        GRAD_V(c, xa, yb - h, xb, yb, [("#8A5A38", 0.0), ("#5E3A20", 1.0)])
        INKR(c, xa, yb - h, xb, yb, 2.4, 230)
        if wd > 60:
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(xa + wd * 0.14, yb - h + 40, xb - wd * 0.14, yb - 40), 8, 8)
            c.drawRRect(rr, S("#2A1608", 3.0, 190))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(xa + wd * 0.22, yb - h + 60, xb - wd * 0.22, yb - 60), 6, 6), S("#B07838", 1.4, 130))
    # kilit
    if open_k < 0.4:
        lx, ly = x, yb - h * 0.52
        c.drawCircle(lx, ly, 26, P("#C4A04A", 255 * (1 - open_k / 0.4)))
        c.drawCircle(lx, ly, 26, S("#3A2610", 2.4, 230 * (1 - open_k / 0.4)))
        c.drawCircle(lx, ly - 4, 5, P("#1A1008", 255 * (1 - open_k / 0.4)))
        c.drawRect(skia.Rect.MakeLTRB(lx - 2.5, ly, lx + 2.5, ly + 16), P("#1A1008", 255 * (1 - open_k / 0.4)))


def k_dolap_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=3, dress=None)
    t = cx.t
    T = L.OD.OTint("day")
    GY = 900.0
    L.grid_floor(c, -500, 2420, GY, 1180)
    CX_, CW_, CH_ = 600.0, 600.0, 700.0
    t_key = cx.at(("c3s22", "sırrı", -0.2))
    t_open = t_key + 0.9
    ok = clamp((t - t_open) / 0.9)
    draw_cabinet(c, CX_, GY, CW_, CH_, ok, T=T, t=t, seed=3)
    # anahtar: gelir, döner
    kk = clamp((t - t_key) / 0.9)
    if kk > 0 and ok < 0.3:
        kx = lerp(CX_ + 340, CX_ + 10, ease_out(min(1, kk * 1.6), 3))
        ky = GY - CH_ * 0.52 - 4
        rot = (kk - 0.55) * 160 * clamp((kk - 0.55) * 4) if kk > 0.55 else 0
        c.save()
        c.translate(kx, ky)
        c.rotate(rot)
        icons.draw_icon(f, "keys", 0, 0, size=120, metal="gold", alpha=1.0 - clamp((ok) / 0.3), shadow=False)
        c.restore()
    # sağda sıra: Signoria üyeleri (kurayla belirir)
    BX0, BX1 = 1180.0, 1900.0
    c.drawRect(skia.Rect.MakeLTRB(BX0, GY - 70, BX1, GY - 40), P("#6A4426"))
    INKR(c, BX0, GY - 70, BX1, GY - 40, 2.0, 220)
    for lx_ in (BX0 + 30, BX1 - 50):
        c.drawRect(skia.Rect.MakeLTRB(lx_, GY - 40, lx_ + 20, GY), P("#4A2E18"))
    t_draw = cx.at(("c3s22", "çekilirdi.", -2.1))
    nfig = 5
    for i in range(nfig):
        tp = t_draw + 0.42 * i
        u = (t - tp) / 0.8
        if u <= 0:
            continue
        fx = BX0 + 70 + i * 140
        # kâğıt dolaptan bankın üstüne uçar, sonra siluete dönüşür
        if u < 0.55:
            k = ease_io(u / 0.55, 2)
            bag = (CX_ + CW_ * (0.20 + 0.30 * (i % 3)), GY - CH_ + 160 + (i % 3) * 200)
            px = lerp(bag[0], fx, k)
            py = lerp(bag[1], GY - 300, k) - math.sin(math.pi * k) * 160
            L.draw_slip(c, px, py, w=84, h=58, rot=0.3 * math.sin(k * 6), lines=1, seed=i + 2, glow=0.5)
        else:
            k = ease_out((u - 0.55) / 0.45, 3)
            L.sil(f, "soylu" if i % 2 == 0 else "banker", fx, GY - 36 + (1 - k) * 90, 330, t, action="idle", dir=-1, seed=50 + i, color="#1A1008", rim="#E8A860", rim_dir=-1, alpha=k, phase=0.17 * i)
    # sağlayan el: dolaptan çeker
    for i in range(nfig):
        tp = t_draw + 0.42 * i
        u = (t - tp) / 0.8
        if 0 < u < 0.45:
            bag = (CX_ + CW_ * (0.20 + 0.30 * (i % 3)), GY - CH_ + 160 + (i % 3) * 200)
            arm_to(c, (bag[0] - 420, 40), (bag[0] + 6, bag[1] + 20 - 70 * ease_out(u / 0.45)), s=2.2, sleeve="#2F5A8A")
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "SIGNORIA", 1540, 250, at=("c3s22", "Signoria", 0.0), size=36, w=300)


@CM.ckind("c3_dolap")
def k_dolap(cx, **kw):
    k_dolap_impl(cx, **kw)


# ═══════════════════════════ c3s23: Cosimo torbaları doldurur (yıllarca) ═══════════════════════════
def draw_hourglass_anim(c, x, y, s, t, t_flip, a=255):
    """Kum saati: t_flip anında yarım dönüş (180°); içindeki kum akar."""
    k = clamp((t - t_flip) / 0.9)
    ang = 180.0 * ease_io(k, 2) if t >= t_flip else 0.0
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    w, h = 60 * s, 96 * s
    top = [(-w, -h), (w, -h), (w * 0.12, 0), (-w * 0.12, 0)]
    bot = [(-w * 0.12, 0), (w * 0.12, 0), (w, h), (-w, h)]
    for pts in (top, bot):
        p = sk.poly_path(pts)
        c.drawPath(p, P("#E8DDB8", 120 * a / 255))
        INKP(c, p, 2.4, 230)
    fill_top = max(0.0, 1.0 - clamp((t - t_flip) / 5.0)) if t >= t_flip else 0.0
    sand = "#C79A3C"
    ht = h * 0.9 * fill_top
    c.save()
    c.clipPath(sk.poly_path(top), skia.ClipOp.kIntersect, True)
    c.drawRect(skia.Rect.MakeLTRB(-w, -h * 0.05 - ht, w, -h * 0.05), P(sand, a))
    c.restore()
    c.save()
    c.clipPath(sk.poly_path(bot), skia.ClipOp.kIntersect, True)
    c.drawRect(skia.Rect.MakeLTRB(-w, h - h * 0.9 * (1 - fill_top), w, h), P(sand, a))
    c.restore()
    c.drawLine(0, 0, 0, h * 0.85, S(sand, 2.4, a))
    c.drawRect(skia.Rect.MakeLTRB(-w - 12, -h - 14, w + 12, -h), P("#5E3A20", a))
    c.drawRect(skia.Rect.MakeLTRB(-w - 12, h, w + 12, h + 14), P("#5E3A20", a))
    c.restore()


def k_doldur_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=2, dress=None)
    t = cx.t
    GY = 900.0
    L.grid_floor(c, -500, 2420, GY, 1200)
    # masa
    table_persp(c, 760, 1760, 730, 860, apron=70, col="#7A4A28", depth=0.07)
    # Cosimo siluet (gözetler)
    ka = cx.amt(("c3s23", "Cosimo", 0.0), 0.7)
    L.sil(f, "soylu", 470, GY + 8, 360, t, action="talk", dir=1, seed=4, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=ka, energy=0.9)
    # kum saati
    kh = cx.amt(("c3s23", "yıllarca,", -0.2), 0.5)
    if kh > 0.003:
        draw_hourglass_anim(c, 470, 230, 1.35, t, cx.at(("c3s23", "yıllarca,", 0.0)), a=int(255 * kh))
    # torba (tahtanın üstünde, şişer)
    t_bag = cx.at(("c3s23", "torbaların", -0.2))
    kb = ease_out(clamp((t - t_bag) / 0.5), 3)
    t_fill0 = cx.at(("c3s23", "bir", 0.0))
    nfill = int(clamp((t - t_fill0) / 2.8) * 14)
    swell = 1.0 + 0.22 * clamp((t - t_fill0) / 3.4)
    BXc, BYc = 1450.0, 690.0
    if kb > 0.003:
        L.draw_bag(c, BXc, BYc - 30 + (1 - kb) * 120, s=2.9 * swell * kb, seed=7, sway=1.2 * math.sin(t * 2.0), slips=min(6, 2 + nfill // 2), a=255)
    # soldaki sepet: işaretli ve işaretsiz kâğıtlar
    c.drawRoundRect(skia.Rect.MakeLTRB(830, 690, 1100, 760), 14, 14, P("#8A5A38")) if hasattr(c, "drawRoundRect") else c.drawRect(skia.Rect.MakeLTRB(830, 690, 1100, 760), P("#8A5A38"))
    INKR(c, 830, 690, 1100, 760, 2.0, 220)
    for i in range(7):
        L.draw_slip(c, 870 + i * 34, 676 - (i % 2) * 8, w=68, h=46, rot=0.15 * ((-1) ** i), lines=1, seed=i, a=255)
        if i % 2 == 0:
            draw_palle_badge(c, 870 + i * 34, 682 - (i % 2) * 8, s=0.62)
    # el: işaretli kâğıtları torbaya tıkar (hızlı)
    if nfill > 0 and t < cx.at(("c3s23", "uğraştı.", 0.2)):
        per = 0.28
        u = ((t - t_fill0) % per) / per
        src = (1010, 640)
        dst = (BXc, BYc - 230)
        if u < 0.5:
            k = ease_io(u / 0.5, 2)
            tgt = (lerp(src[0], dst[0], k), lerp(src[1], dst[1], k) - math.sin(math.pi * k) * 90)
            slip_p = (tgt[0], tgt[1] + 24)
        else:
            k = (u - 0.5) / 0.5
            tgt = (lerp(dst[0], src[0], ease_io(k, 2)), lerp(dst[1], src[1], ease_io(k, 2)) - math.sin(math.pi * k) * 60)
            slip_p = None
        arm_to(c, (tgt[0] + 40, -240), tgt, s=2.3, sleeve="#2F5A8A")
        if slip_p is not None:
            L.draw_slip(c, slip_p[0], slip_p[1], w=68, h=46, rot=0.4 * u, lines=1, seed=3)
            draw_palle_badge(c, slip_p[0], slip_p[1] + 4, s=0.62)
    # işaretsiz kâğıtlar kenara düşer (kutu dışı)
    for i in range(4):
        tp = t_fill0 + 0.5 + i * 0.6
        u = clamp((t - tp) / 0.9)
        if 0 < u < 1:
            x = 1110 + 160 * u + i * 12
            y = 760 + 260 * u * u
            L.draw_slip(c, x, y, w=60, h=40, rot=2.6 * u + i, lines=1, seed=20 + i, a=int(255 * (1 - u * 0.7)))
    L.end(cx, cam, motes_n=14)
    L.stamp_at(f, cx, "YORUM", 1560, 230, at=("c3s23", "çıkarmaması", 0.0), size=46, rot=-0.07)


@CM.ckind("c3_doldur")
def k_doldur(cx, **kw):
    k_doldur_impl(cx, **kw)


# ═══════════════════════════ c3s24: kura vardı; torbaya kimin gireceğine kura karar vermiyordu (kapıdaki bekçi) ═══════════════════════════
def k_bekci_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=1, dress=None)
    t = cx.t
    GY = 900.0
    L.grid_floor(c, -500, 2420, GY, 1180)
    BXc, BYc = 1480.0, 600.0
    L.draw_bag(c, BXc, BYc, s=3.6, seed=4, sway=1.5 * math.sin(t * 1.6), slips=0)
    # bekçi (kapıdaki): çantanın önünde, sola bakar
    t_g = cx.at(("c3s24", "torbaya", -0.3))
    kg = cx.amt(("c3s24", "torbaya", -0.3), 0.5)
    L.sil(f, "asker", 1110, GY + 10, 360, t, action="point", dir=-1, seed=8, color="#14100C", rim="#FFE2A0", rim_dir=-1, alpha=kg, prop="halberd")
    # konveyör çizgisi
    c.drawLine(-300, 830, 1050, 830, S("#5A3C22", 6.0, 200))
    t_q = cx.at(("c3s24", 0.0))
    # önce 'kura vardı': kâğıt çeken el (bir kez)
    kk = cx.amt(("c3s24", "vardı;", -0.6), 0.4)
    # sıra: kâğıtlar soldan gelir (her 0.55 sn), işaretli olanlar torbaya girer, öbürleri elenir
    t_s0 = cx.at(("c3s24", "gireceğine", -0.9))
    for i in range(7):
        tp = t_s0 + 0.55 * i
        u = (t - tp) / 2.4
        if u < 0:
            continue
        marked = (i % 2 == 0)
        x = lerp(-120, 940, ease_io(clamp(u / 0.62), 1.6))
        y = 800
        rot = 0.0
        a = 255
        if u > 0.62:
            k = (u - 0.62) / 0.38
            if marked:
                # torbanın ağzına çıkar ve içeri girer
                x = lerp(940, BXc - 20, ease_io(k, 2))
                y = lerp(800, BYc - 320, ease_io(k, 2)) - math.sin(math.pi * k) * 120
                a = int(255 * (1 - clamp((k - 0.8) / 0.2)))
            else:
                # elenir: aşağı düşer, döner
                x = 940 + 160 * k
                y = 800 + 300 * k * k
                rot = 3.0 * k
                a = int(255 * (1 - k * 0.8))
        if a > 4:
            L.draw_slip(c, x, y, w=104, h=70, rot=rot, lines=1, seed=i + 1, a=a)
            if marked:
                draw_palle_badge(c, x, y + 6, s=0.95, a=a)
    L.end(cx, cam, motes_n=12)
    L.tag(f, cx, "KURA", 520, 250, at=("c3s24", "Kura", 0.0), size=46, w=260, hold=("c3s24", "torbaya", -0.2))
    L.stamp_at(f, cx, "YORUM", 1560, 230, at=("c3s24", "vermiyordu.", -0.3), size=46, rot=-0.07)


@CM.ckind("c3_bekci")
def k_bekci(cx, **kw):
    k_bekci_impl(cx, **kw)


# ═══════════════════════════ c3s25: Padgett–Ansell ağı (kümeler yalnız Medici üzerinden bağlanır) ═══════════════════════════
_AG = {}
HUB = (960.0, 525.0)


def _ag_layout():
    if "L" in _AG:
        return _AG["L"]
    spec = [((420.0, 540.0), 8, "#233C8C", 2), ((1480.0, 290.0), 7, "#8A6A2A", 5), ((1480.0, 760.0), 7, "#3A7A52", 9)]
    out = []
    for (cc, n, col, sd) in spec:
        pts = []
        for i in range(n):
            ang = i * 2.39996 + sd
            rr = 34 + 40 * math.sqrt(i)
            pts.append((cc[0] + rr * math.cos(ang) * 1.3, cc[1] + rr * math.sin(ang) * 0.95))
        edges = []
        for i in range(1, n):
            ds = sorted(range(i), key=lambda j: (pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2)
            for j in ds[:(1 if i == 1 else 2)]:
                edges.append((i, j))
        gate = min(range(n), key=lambda i: (pts[i][0] - HUB[0]) ** 2 + (pts[i][1] - HUB[1]) ** 2)
        out.append(dict(c=cc, pts=pts, edges=edges, gate=gate, col=col))
    _AG["L"] = out
    return out


def k_ag_impl(cx, **_):
    import cilt_props as CP
    f, c, cam = L.begin(cx, bg="wall", seed=4, dress=None)
    t = cx.t
    lay = _ag_layout()
    t_n0 = cx.at(("c3s25", "Padgett", -0.3))
    t_hub = cx.at(("c3s25", "Medici", 0.0))
    kb = cx.amt(("c3s25", "bağlı", -0.1), 0.9)
    kh = cx.amt(("c3s25", "yalnız", 0.0), 0.7)
    kdim = 1.0 - 0.55 * cx.amt(("c3s25", "Medici", 0.0), 0.8)
    # kümeler: yarı saydam bölge + kesikli çerçeve
    for d in lay:
        if kb > 0.003:
            cxx, cyy = d["c"]
            rc = skia.Rect.MakeLTRB(cxx - 270, cyy - 180, cxx + 270, cyy + 180)
            c.drawOval(rc, P(d["col"], 34 * kb))
            dp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.0, Color=C(d["col"], int(150 * kb)))
            dp.setPathEffect(skia.DashPathEffect.Make([14.0, 10.0], -t * 14))
            c.drawOval(rc, dp)
    # kümeler arası kopukluk: çarpı işaretleri
    kg = cx.amt(("c3s25", "olmayan", 0.0), 0.7)
    if kg > 0.003:
        for (xa, ya, xb, yb) in ((690, 470, 835, 420), (690, 610, 835, 650), (1480, 485, 1480, 565)):
            dashed(c, xa, ya, xb, yb, col="#8A7A62", w=3.0, a=int(210 * kg * kdim), dash=(10.0, 12.0))
            mx, my = (xa + xb) / 2, (ya + yb) / 2
            xs = 16 * (0.6 + 0.4 * ease_out(kg))
            c.drawLine(mx - xs, my - xs, mx + xs, my + xs, S("#A8321E", 5.0, int(235 * kg * kdim)))
            c.drawLine(mx - xs, my + xs, mx + xs, my - xs, S("#A8321E", 5.0, int(235 * kg * kdim)))
    # küme içi bağlar + düğümler
    for k, d in enumerate(lay):
        pts = d["pts"]
        tn = [t_n0 + 0.8 * k + 0.14 * i for i in range(len(pts))]
        for (i, j) in d["edges"]:
            pe = clamp((t - max(tn[i], tn[j]) - 0.05) / 0.28)
            if pe > 0:
                (x0, y0), (x1, y1) = pts[j], pts[i]
                c.drawLine(x0, y0, lerp(x0, x1, pe), lerp(y0, y1, pe), S(mix(d["col"], "#2A1A0C", 0.35), 3.0, 200))
    # Medici bağları (altın)
    for k, d in enumerate(lay):
        gx, gy = d["pts"][d["gate"]]
        pe = ease_io(clamp((t - (t_hub + 0.45 * k)) / 0.75), 2)
        if pe > 0:
            ex, ey = lerp(HUB[0], gx, pe), lerp(HUB[1], gy, pe)
            c.drawLine(HUB[0], HUB[1], ex, ey, S("#FFD060", 18.0, 60))
            c.drawLine(HUB[0], HUB[1], ex, ey, S("#C79A3C", 7.0, 245))
            c.drawLine(HUB[0], HUB[1], ex, ey, S("#FFF0B0", 2.0, 220))
            if pe > 0.99:                                          # akış: ışık noktaları
                for q in range(2):
                    ph = ((t * 0.55 + q * 0.5 + k * 0.23) % 1.0)
                    px_, py_ = lerp(HUB[0], gx, ph), lerp(HUB[1], gy, ph)
                    SOFT(c, px_, py_, 14, 14, "#FFF2B0", 200)
    for k, d in enumerate(lay):
        pts = d["pts"]
        for i, (x, y) in enumerate(pts):
            tn = t_n0 + 0.8 * k + 0.14 * i
            kk = ease_out(clamp((t - tn) / 0.3), 3)
            if kk <= 0.003:
                continue
            gate = (i == d["gate"])
            rr = (19 if gate else 14) * kk
            sh = skia.GradientShader.MakeRadial((x - rr * 0.3, y - rr * 0.35), rr * 1.6, [C(mix(d["col"], "#FFFFFF", 0.45)), C(d["col"]), C(mix(d["col"], "#000000", 0.45))], [0.0, 0.5, 1.0])
            c.drawCircle(x, y + 3, rr, P("#000000", 70))
            c.drawCircle(x, y, rr, skia.Paint(AntiAlias=True, Shader=sh))
            c.drawCircle(x, y, rr, S("#1A100A", 1.6, 220))
            if gate and kh > 0.5:
                c.drawCircle(x, y, rr + 6, S("#FFD060", 3.0, int(230 * (kh - 0.5) * 2)))
    # merkez: Medici arması
    if kh > 0.003:
        SOFT(c, HUB[0], HUB[1], 200, 200, "#FFD060", 70 * kh)
        CP.draw_arms(f, HUB[0], HUB[1], 190 * (0.9 + 0.1 * ease_out(kh)), alpha=kh, shadow=0.6, glow=0.35 * kh, glint=((t * 0.3) % 2.0) if (t * 0.3) % 2.0 < 1 else None)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "PADGETT · ANSELL", 960, 100, at=("c3s25", "Padgett", -0.1), size=36, sub="SOSYOLOGLAR", w=640)
    L.tag(f, cx, "AİLE GRUPLARI", 420, 322, at=("c3s25", "aile", 0.0), size=30, w=400)
    L.tag(f, cx, "MEDICI", 960, 700, at=("c3s25", "Medici", 0.0), size=36, w=300)


@CM.ckind("c3_ag")
def k_ag(cx, **kw):
    k_ag_impl(cx, **kw)


# ═══════════════════════════ c3s27: şube kutuları (harita bindirmesi; p2_map extra=) ═══════════════════════════
BRANCHES = [
    ("ROMA", 12.4964, 41.9028, (210, -45)),
    ("VENEDİK", 12.3155, 45.4408, (215, -35)),
    ("MİLANO", 9.19, 45.4642, (-30, -125)),
    ("CENEVRE", 6.1432, 46.2044, (-215, -35)),
    ("AVİGNON", 4.8055, 43.9493, (-215, 40)),
    ("BRUGGE", 3.2247, 51.2093, (175, -20)),
    ("LONDRA", -0.1276, 51.5072, (-215, 25)),
]


def branch_extra(cx, cm, mv):
    f = cx.f
    c = f.c
    t = cx.t
    t0 = cx.at(("c3s27", "Şube", -0.2))
    t_cap = cx.at(("c3s27", "sermayeden", 0.0))
    t_pro = cx.at(("c3s27", "kârdan", 0.0))
    t_lock = cx.at(("c3s27", "kendi", -0.3))
    fx, fy = cm.ll(11.2558, 43.7696)
    kf = cx.amt(("c3s27", "Şube", -0.4), 0.5)
    if kf > 0.003:
        c.drawCircle(fx, fy, 15 * kf, P("#B33620", 255 * kf))
        c.drawCircle(fx, fy, 15 * kf, S("#2A1A0C", 2.0, 220 * kf))
        CM.ink(f, "FLORANSA", fx + 24, fy + 10, face="title_m", size=26, color=TH.fg, align="l", track=4, alpha=kf, emboss=False)
    for i, (name, lon, lat, (dx, dy)) in enumerate(BRANCHES):
        x, y = cm.ll(lon, lat)
        k = ease_out(clamp((t - (t0 + 0.30 * i)) / 0.45), 3)
        if k <= 0.003:
            continue
        bx, by = x + dx, y + dy
        c.drawLine(x, y, bx, by, S("#2A1A0C", 2.0, int(200 * k)))
        c.drawCircle(x, y, 8 * k, P("#A8321E", 255 * k))
        c.drawCircle(x, y, 8 * k, S("#2A1A0C", 1.6, 230 * k))
        w_, h_ = 236, 104
        CM.tablet(f, bx - w_ / 2, by - h_ / 2 + (1 - k) * 16, w_, h_, alpha=k, corner=8)
        CM.ink(f, name, bx, by - 12, face="title_m", size=27, color=TH.fg, align="c", track=4, alpha=k, emboss=False)
        x0b = bx - 100
        kc = ease_out(clamp((t - (t_cap - 0.1 + 0.07 * i)) / 0.5), 3)
        kp = ease_out(clamp((t - (t_pro - 0.1 + 0.10 * i)) / 0.7), 3)
        if kc > 0.003:
            R(c, x0b, by + 10, x0b + 30 * kc, by + 22, "#3A5A9A")
            INKR(c, x0b, by + 10, x0b + 30 * kc, by + 22, 1.2, 200)
        if kp > 0.003:
            R(c, x0b, by + 28, x0b + 188 * kp, by + 40, "#C79A3C")
            INKR(c, x0b, by + 28, x0b + 188 * kp, by + 40, 1.2, 200)
        kl = ease_out(clamp((t - (t_lock + 0.22 * i)) / 0.4), 3)
        if kl > 0.003:
            c.drawRect(skia.Rect.MakeLTRB(bx - w_ / 2 - 4, by - h_ / 2 - 4, bx + w_ / 2 + 4, by + h_ / 2 + 4), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.0, Color=C("#8E2A1E", int(230 * kl))))
            icons.draw_icon(f, "keys", bx + w_ / 2 - 12, by - h_ / 2 - 6, size=56 * (0.7 + 0.3 * kl), metal="gold", alpha=kl, shadow=True)
    kl_ = cx.amt(("c3s27", "sermayeden", -0.2), 0.5)
    if kl_ > 0.003:
        for (lx, col, txt) in ((330, "#3A5A9A", "SERMAYE PAYI"), (700, "#C79A3C", "KÂR PAYI")):
            R(c, lx, 900, lx + 44, 920, col, 255 * kl_)
            INKR(c, lx, 900, lx + 44, 920, 1.4, 220 * kl_)
            CM.ink(f, txt, lx + 60, 918, face="cap_b", size=28, color=TH.fg, align="l", track=3, alpha=kl_, emboss=False)


# ═══════════════════════════ c3s28: kâr kartı (186.382 → 290.791 FL; yarıdan fazlası Roma) ═══════════════════════════
def k_kar_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=5, dress=None)
    t = cx.t
    GY = 800.0
    SC_ = 1.7
    # yıl cetveli 1435 → 1450 (önce büyük, çubuklar gelirken küçülüp yukarı çıkar)
    t_a = cx.at(("c3s28", "1435'ten", 0.0))
    t_b = cx.at(("c3s28", "1450'ye", 0.0))
    kr = cx.amt(("c3s28", "1435'ten", -0.2), 0.6)
    ek = ease_io(cx.amt(("c3s28", "kadar", 0.3), 1.0), 2)
    if kr > 0.003:
        x0, x1 = lerp(420.0, 500.0, ek), lerp(1500.0, 1420.0, ek)
        yy = lerp(400.0, 150.0, ek)
        al = kr * (1.0 - 0.45 * ek)
        u = clamp((t - t_a) / max(0.3, t_b - t_a))
        c.drawLine(x0, yy, x1, yy, S(TH.rule, 3.0, int(150 * al)))
        for i in range(16):
            xx = lerp(x0, x1, i / 15.0)
            big = i in (0, 15)
            c.drawLine(xx, yy - (lerp(26, 14, ek) if big else lerp(13, 7, ek)), xx, yy + (lerp(26, 14, ek) if big else lerp(13, 7, ek)), S(TH.rule, 2.0, int(200 * al)))
        xe = lerp(x0, x1, ease_io(u, 1.6))
        c.drawRect(skia.Rect.MakeLTRB(x0, yy - lerp(14, 8, ek), xe, yy + lerp(14, 8, ek)), P("#C79A3C", 235 * al))
        INKR(c, x0, yy - lerp(14, 8, ek), max(x0 + 2, xe), yy + lerp(14, 8, ek), 1.4, 200 * al)
        lsz = lerp(76, 34, ek)
        CM.draw_spr(f, CM.engraved("1435", "title", int(lsz), 4.0, TH.fg), x0, yy + lsz * 1.25, "c", alpha=al, shadow=0.0)
        if u > 0.85:
            CM.draw_spr(f, CM.engraved("1450", "title", int(lsz), 4.0, TH.fg), x1, yy + lsz * 1.25, "c", alpha=al * clamp((u - 0.85) * 8), shadow=0.0)
    # çubuklar
    c.drawLine(420, GY, 1300, GY, S(TH.rule, 4.0, 230))
    t_l = cx.at(("c3s28", "kadar", 0.0))
    kl = ease_out(clamp((t - t_l) / 0.9), 3)
    HL = 186.382 * SC_ * kl
    if kl > 0.003:
        GRAD_V(c, 480, GY - HL, 700, GY, [("#8A9AC0", 0.0), ("#4A5A86", 1.0)])
        c.drawRect(skia.Rect.MakeLTRB(490, GY - HL, 514, GY), P("#FFFFFF", 46))
        INKR(c, 480, GY - HL, 700, GY, 2.4, 230)
        CM.ink(f, "1420–35", 590, GY + 56, face="title_m", size=32, color=TH.fg2, align="c", track=4, alpha=kl, emboss=False)
        txt = CM.fmt_int(186382 * kl) + " FL"
        CM.draw_spr(f, CM.engraved(txt, "title", 44, 4.0, TH.fg2), 590, GY - HL - 44, "c", alpha=kl, shadow=0.0)
    t_r = cx.at(("c3s28", "iki", -0.1))
    kg = ease_out(clamp((t - t_r) / 2.4), 2.6)
    HR = 290.791 * SC_ * kg
    xr0, xr1 = 940.0, 1180.0
    if kg > 0.003:
        GRAD_V(c, xr0, GY - HR, xr1, GY, [("#EBC65A", 0.0), ("#A8761E", 1.0)])
        # Roma bölümü (alttan, yarıyı geçer)
        kro = ease_io(clamp((t - cx.at(("c3s28", "fazlası", -0.5))) / 1.1), 2)
        HRo = HR * 0.54 * kro
        if kro > 0.003:
            GRAD_V(c, xr0, GY - HRo, xr1, GY, [("#C8452E", 0.0), ("#7E2216", 1.0)])
            c.drawLine(xr0, GY - HRo, xr1, GY - HRo, S("#2A1008", 2.4, 230))
        c.drawRect(skia.Rect.MakeLTRB(xr0 + 12, GY - HR, xr0 + 38, GY), P("#FFFFFF", 50))
        INKR(c, xr0, GY - HR, xr1, GY, 2.6, 235)
        CM.ink(f, "1435–50", (xr0 + xr1) / 2, GY + 56, face="title_m", size=32, color=TH.fg, align="c", track=4, alpha=kg, emboss=False)
        txt = CM.fmt_int(290791 * kg) + " FL"
        CM.draw_spr(f, CM.engraved(txt, "title", 60, 4.0, TH.fg), (xr0 + xr1) / 2, GY - HR - 54, "c", alpha=smooth(kg * 5), shadow=0.0)
        if kg > 0.2:
            icons.draw_icon(f, "coins", (xr0 + xr1) / 2 + 150, GY - HR - 20 + 6 * math.sin(t * 2.2), size=104 * smooth((kg - 0.2) * 3), metal="gold", alpha=1.0)
        # yarı çizgisi
        kh = ease_io(cx.amt(("c3s28", "yarıdan", -0.1), 0.7), 2)
        if kh > 0.003:
            yh = GY - 0.5 * HR
            dashed(c, xr0 - 70, yh, xr0 - 70 + (xr1 - xr0 + 140) * kh, yh, col="#2A1A0C", w=3.0, a=235, dash=(14.0, 9.0))
            CM.ink(f, "YARISI", xr0 - 86, yh + 9, face="cap_b", size=28, color=TH.fg, align="r", track=3, alpha=kh, emboss=False)
        if kro > 0.5:
            ka = clamp((kro - 0.5) * 2)
            CM.ink(f, "ROMA", (xr0 + xr1) / 2, GY - HRo / 2 + 12, face="title", size=44, color="#F4E9CB", align="c", track=8, alpha=ka, emboss=False)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "19.386 FL / YIL", 1530, 560, at=("c3s28", "yazdı;", -0.4), size=40, sub="ORTALAMA · HESAPLANMIŞ", w=500)
    L.stamp_src(f, cx, "TEK KAYNAK", 1560, 300, at=("c3s28", "Roma'dan", -0.1), size=40, rot=-0.07)


@CM.ckind("c3_kar")
def k_kar(cx, **kw):
    k_kar_impl(cx, **kw)


# ═══════════════════════════ c3s29: «holding» sonradan eklenen etiket; o günlerde compagnia ═══════════════════════════
def k_holding_impl(cx, **_):
    import cilt_props as CP
    f, c, cam = L.begin(cx, bg="wall", seed=6, dress=None)
    t = cx.t
    # eski defter kapağı / levha
    pk = cx.amt(("c3s29", -0.2), 0.7)
    PX, PY, PW, PH = 960.0, 540.0, 1180.0, 430.0
    CM.tablet(f, PX - PW / 2, PY - PH / 2 + (1 - pk) * 20, PW, PH, alpha=pk, corner=14)
    CP.draw_arms(f, PX - 400, PY, 200, alpha=pk, shadow=0.6, glow=0.0, glint=None)
    c.drawLine(PX - 230, PY + 78, PX + 480, PY + 78, S("#5A3C22", 2.4, int(200 * pk)))
    # compagnia: yazılır
    t_w = cx.at(("c3s29", "compagnia", -0.1))
    kw_ = clamp((t - t_w) / 0.95)
    if kw_ > 0.003:
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(PX - 250, PY - 120, PX - 250 + 760 * ease_io(kw_, 1.4), PY + 120))
        PP_hand(f, "compagnia", PX + 130, PY + 48, 150, "#2A1608", 1.0, seed=7, jitter=1.6)
        c.restore()
    # HOLDING etiketi: havadan gelir, yapışır; 'o günlerde' ile soyulup savrulur
    t_in = cx.at(("c3s29", "Holding", -0.2))
    t_hit = cx.at(("c3s29", "eklendi;", -0.1))
    t_pl = cx.at(("c3s29", "günlerde", -0.1))
    kin = ease_out(clamp((t - t_in) / 0.6), 3)
    kfall = ease_in(clamp((t - (t_hit - 0.55)) / 0.55), 2)
    sx, sy = PX + 130, PY + 8
    if t < t_hit:
        px_ = lerp(PX + 520, sx, kfall)
        py_ = lerp(130.0, sy, kfall) - 12 * math.sin(t * 2.4) * (1 - kfall)
        sc = lerp(1.45, 1.0, kfall)
        rot = lerp(-0.22, -0.035, kfall)
        a = kin
        peel = 0.0
    else:
        px_, py_, sc, rot = sx, sy, 1.0, -0.035
        a = 1.0
        kp_ = clamp((t - t_pl) / 0.85)
        peel = kp_
        a = 1.0 - clamp((kp_ - 0.55) / 0.45)
        sc = 1.0 + 0.04 * (1 - clamp((t - t_hit) / 0.2)) 
    if a > 0.003:
        L.draw_sticker(f, px_, py_, 560, 190, "“HOLDING”", a=a, rot=rot, scale=sc, peel=peel, size=70, track=6.0)
    if t >= t_hit and t < t_hit + 0.45:                        # yapışma halkası
        kk = (t - t_hit) / 0.45
        c.drawCircle(sx, sy, 150 + 190 * kk, S("#FFF2B0", 4.0, int(160 * (1 - kk))))
    L.end(cx, cam, motes_n=14)
    L.stamp_at(f, cx, "SONRADAN", 520, 250, at=("c3s29", "sonradan", -0.1), size=52, rot=-0.08, hold=("c3s29", "günlerde", 0.3))
    L.tag(f, cx, "O GÜNLERDE", 1450, 250, at=("c3s29", "günlerde", -0.1), size=34, w=420)


@CM.ckind("c3_holding")
def k_holding(cx, **kw):
    k_holding_impl(cx, **kw)


# ═══════════════════════════ c3s30: Careggi villası, 1 Ağustos 1464 ═══════════════════════════
def draw_villa(c, T, x, yb, t=0.0):
    """Careggi tipi taş villa (genel temsil; ön görünüş): terasta istinat duvarı, iki kat, üç kemerli revak, kapalı kepenkler."""
    # teras duvarı
    L.stone_wall(c, x - 560, x + 560, yb, yb + 130, T, col="#B4A27C", course=44, seed=4)
    INKR(c, x - 560, yb, x + 560, yb + 130, 2.0, 200)
    R(c, x - 575, yb - 8, x + 575, yb + 6, T("#CDBB92"))
    INKR(c, x - 575, yb - 8, x + 575, yb + 6, 1.4, 200)
    # gövde
    GRAD_V(c, x - 330, yb - 260, x + 330, yb, [(T("#EADCB6"), 0.0), (T("#CDBB92"), 1.0)])
    INKR(c, x - 330, yb - 260, x + 330, yb, 2.4, 230)
    c.drawLine(x - 330, yb - 130, x + 330, yb - 130, S("#2A1A0C", 1.6, 150))
    # çatı (kırma) + saçak
    roof = [(x - 372, yb - 260), (x + 372, yb - 260), (x + 290, yb - 350), (x - 290, yb - 350)]
    c.drawPath(sk.poly_path(roof), P(T("#C0603A")))
    for k_ in range(1, 6):
        yy = yb - 260 - k_ * 15
        c.drawLine(x - 372 + k_ * 16, yy, x + 372 - k_ * 16, yy, S("#5A2412", 1.0, 120))
    INKP(c, sk.poly_path(roof), 2.2, 220)
    R(c, x + 150, yb - 410, x + 190, yb - 340, T("#B8A47C"))
    INKR(c, x + 150, yb - 410, x + 190, yb - 340, 1.6, 200)
    # üst kat pencereleri (kapalı kepenk)
    for k_ in range(5):
        wx = x - 250 + k_ * 125
        if abs(wx - x) < 40:
            wx = x
        R(c, wx - 24, yb - 238, wx + 24, yb - 150, "#5A3C22")
        for j in range(5):
            c.drawLine(wx - 24, yb - 238 + j * 17.6 + 8, wx + 24, yb - 238 + j * 17.6 + 8, S("#2A1608", 1.0, 170))
        INKR(c, wx - 24, yb - 238, wx + 24, yb - 150, 1.6, 220)
    # revak (3 kemer)
    for k_ in range(3):
        ax = x - 120 + k_ * 120
        pth = skia.Path()
        pth.moveTo(ax - 44, yb)
        pth.lineTo(ax - 44, yb - 74)
        pth.cubicTo(ax - 44, yb - 124, ax + 44, yb - 124, ax + 44, yb - 74)
        pth.lineTo(ax + 44, yb)
        pth.close()
        c.drawPath(pth, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, yb - 124), (0, yb)], [C("#2A1C10"), C("#6A4A2A")], [0, 1])))
        INKP(c, pth, 2.0, 230)
    for k_ in range(4):
        px = x - 180 + k_ * 120
        R(c, px - 7, yb - 80, px + 7, yb, T("#E0D2AC"))
        INKR(c, px - 7, yb - 80, px + 7, yb, 1.2, 200)
    # yan kapalı pencereler (zemin kat)
    for sg in (-1, 1):
        for k_ in range(2):
            wx = x + sg * (250 + k_ * 62)
            R(c, wx - 20, yb - 110, wx + 20, yb - 40, "#5A3C22")
            INKR(c, wx - 20, yb - 110, wx + 20, yb - 40, 1.4, 210)


def k_careggi_impl(cx, **_):
    f = cx.f
    c = f.c
    t = cx.t
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    cam.begin(f)
    T = CT.Tint("day")
    sh = skia.GradientShader.MakeLinear([(0, -500), (0, 780)], [C("#9CBBDC"), C("#EFE6C8")], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(-1200, -1000, 3200, 800), skia.Paint(Shader=sh))
    # yavaş bulutlar
    for i in range(6):
        cxx = ((i * 520 + t * (6 + i * 1.5)) % 2800) - 400
        cyy = 60 + (i * 97) % 340
        SOFT(c, cxx, cyy, 220 + 20 * i, 36, "#FFFFFF", 150)
        SOFT(c, cxx + 110, cyy - 18, 150, 30, "#FFFFFF", 120)
    LH = 900.0
    for (col, amp, scl, base, ph, al) in (("#A9BDB6", 40, 600, 420, 0.0, 0.0), ("#93AFA5", 46, 420, 340, 2.1, 0.0), ("#7F9E92", 52, 300, 270, 4.3, 0.0)):
        cc = T(col, 0.2)
        pts = []
        x = -1200
        while x <= 3200:
            pts.append((x, LH - L.PN.ridge_y(x, base, amp, scl, ph)))
            x += 10
        poly = pts + [(pts[-1][0], LH + 900), (pts[0][0], LH + 900)]
        c.drawPath(sk.poly_path(poly), skia.Paint(AntiAlias=True, Color=C(cc)))
        c.drawPath(sk.poly_path(pts, False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=C(mix(cc, "#1A2A22", 0.5), 150)))
    # ön tepe (villanın oturduğu yamaç)
    pts = []
    x = -1200
    while x <= 3200:
        pts.append((x, 760 - 40 * math.sin(x * 0.0021 + 0.6) - 24 * math.sin(x * 0.0057)))
        x += 12
    poly = pts + [(pts[-1][0], 1500), (pts[0][0], 1500)]
    c.drawPath(sk.poly_path(poly), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 700), (0, 1200)], [C("#8FA070"), C("#5E7A48")], [0, 1])))
    c.drawPath(sk.poly_path(pts, False), S("#2A3A20", 2.0, 200))
    VX_ = 1000.0
    draw_villa(c, T, VX_, 790.0, t)
    for (cxx, hh) in ((300, 300), (410, 250), (1620, 290), (1710, 240), (1830, 280), (190, 230)):
        SE.SC.cypress(c, cxx, 800 + (cxx % 7) * 4, hh, T("#2E4A33", 0.1), T("#4F6E4A", 0.1))
    # rüzgârda kıpırdayan yapraklar / kuş değil; sade: uçuşan yapraklar
    for i in range(6):
        ph = (t * 0.10 + i * 0.17) % 1.0
        x = -100 + ph * 2200
        y = 640 + 140 * abs(math.sin(ph * 7 + i)) + 18 * i
        c.save()
        c.translate(x, y)
        c.rotate(math.degrees(ph * 12 + i))
        c.drawOval(skia.Rect.MakeLTRB(-8, -4, 8, 4), P("#7A8A4A", 190))
        c.restore()
    cam.end(f)
    CM.finish(f, cx, motes_n=12)
    L.date_plate(f, cx, "1 AĞUSTOS 1464", ("c3s30", "Ağustos", -0.2), x=96, y=860, size=48)
    L.tag(f, cx, "CAREGGİ", 1180, 250, at=("c3s30", "Careggi'deki", -0.1), size=38, w=420)
    L.stamp_src(f, cx, "TEK KAYNAK", 1580, 360, at=("c3s30", "yazılır", -0.3), size=40, rot=-0.07)


@CM.ckind("c3_careggi")
def k_careggi(cx, **kw):
    k_careggi_impl(cx, **kw)


# ═══════════════════════════ c3s31–32: şehrin mizacı (gravür, ANEKDOT): elli yıl, sürgün, binalar kalır ═══════════════════════════
def _sokak_strip(fr):
    c = fr.c
    T = CT.Tint("day")
    GYs = 960.0
    sh = skia.GradientShader.MakeLinear([(0, 0), (0, 560)], [C("#9CBBDC"), C("#E8E4D0")], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(0, 0, 4200, 700), skia.Paint(Shader=sh))
    rr = _RS(5)
    wins0 = []
    x = -40
    while x < 4300:
        bw, bh = rr.uniform(120, 220), rr.uniform(220, 360)
        CT.draw_house(c, x, 560, bw, bh, _RS(int(rr.randint(1, 10 ** 6))), T, 0.40, wins0)
        x += bw + rr.uniform(-8, 10)
    R(c, 0, 556, 4200, 700, T("#B8A888", 0.3))
    SE.street_facade(c, 0, 4200, 0, 4200, GYs, 700, T, seed=8, door_x=-99999, arch_x=-99999)
    for dx in (700, 1900, 3100):
        SE.portal(c, dx, GYs, 190, 340, T)
    L.PN.draw_pavement(c, 0, 4200, GYs - 6, 1220, T, seed=3)


_KALIR = [("soylu", 31, 180, 70, 305, 1, "talk"), ("banker", 32, 300, 100, 312, -1, "talk"), ("tuccar", 33, 440, 40, 296, 1, "idle"), ("halk", 34, 560, 96, 292, -1, "talk"),
          ("soylu", 35, 690, 64, 306, 1, "idle"), ("banker", 36, 800, 22, 300, -1, "point"), ("tuccar", 37, 920, 92, 296, 1, "talk"), ("soylu_f", 38, 1030, 50, 296, -1, "idle"),
          ("halk", 39, 380, 14, 290, 1, "idle"), ("soylu", 40, 1110, 20, 300, -1, "idle")]


def k_sehir_kalir_impl(cx, **_):
    f = cx.f
    c = f.c
    t = cx.t
    kcol = cx.amt(("c3s31", "binaları", -0.3), 1.4)
    L.mono_begin(f, 1.0 - 0.7 * kcol)
    f.clear("#0B0A08")
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    im = bake(("sokak_strip", 1), 4200, 1300, _sokak_strip)
    cam.begin(f)
    c.drawRect(skia.Rect.MakeLTRB(-600, -800, 5000, 1900), P("#9CBBDC"))
    c.save()
    c.translate(-700, -20)
    c.drawImage(im, 0, 0, L.LIN)
    c.restore()
    GY = 940.0
    t_leave = cx.at(("c3s31", "hepsi", -0.1))
    for i, (kd, sd, x0, dy, hh, dr, act) in enumerate(_KALIR):
        td = t_leave + 0.11 * i + (0.3 if i % 3 == 1 else 0.0)
        if t < td:
            L.sil(f, kd, x0, GY + dy - 20, hh, t, action=act, dir=dr, seed=sd, color="#14100C", rim="#FFE2A0", rim_dir=dr, energy=1.0)
        else:
            x = x0 - 240.0 * (t - td)
            if x > -260:
                L.sil(f, kd, x, GY + dy - 20, hh, t, dir=-1, seed=sd, color="#14100C", rim="#FFE2A0", rim_dir=-1, walker=240.0, prop="sack")
    cam.end(f)
    L.mono_end(f)
    # binalar kalır: sıcak ışık süpürmesi (renk geri gelir)
    ks = cx.amt(("c3s31", "binaları", -0.2), 1.8)
    if ks > 0.003:
        a0, a1, a2 = clamp(ks - 0.45), clamp(ks), clamp(ks + 0.45)
        sh = skia.GradientShader.MakeLinear([(0, 0), (W, 0)], [C("#FFD890", 0), C("#FFD890", int(130 * ks)), C("#FFD890", 0)], [a0, a1, max(a2, a1 + 1e-4)])
        c.drawRect(skia.Rect.MakeLTRB(0, 300, W, 900), skia.Paint(Shader=sh))
    CM.finish(f, cx, motes_n=12, light=(960.0, 520.0, 1500.0, 0.9))
    # elli yıl: tutanak çizgileri (beşli demetler)
    t_y = cx.at(("c3s31", "elli", -0.1))
    ky = clamp((t - t_y) / 1.5)
    if ky > 0.003:
        n = int(50 * ky)
        for g in range(10):
            gx = 360 + g * 120
            for j in range(5):
                idx = g * 5 + j
                if idx >= n:
                    break
                if j < 4:
                    c.drawLine(gx + j * 15, 330, gx + j * 15, 400, S("#8E2A1E", 5.0, 235))
                else:
                    c.drawLine(gx - 8, 392, gx + 66, 338, S("#8E2A1E", 5.0, 235))
        L.tag(f, cx, "50 YIL", 960, 235, at=("c3s31", "elli", -0.1), size=72, w=420, track=12)
    L.tag(f, cx, "COSİMO'YA ATFEDİLEN", 560, 180, at=("c3s31", "atfedilen", -0.3), size=34, w=620, hold=("c3s31", "elli", -0.1))
    L.stamp_at(f, cx, "ANEKDOT", 1480, 200, at=("c3s31", "atfedilen", 0.0), size=50, rot=-0.07)
    L.stamp_at(f, cx, "KAYNAĞI BELİRSİZ", 960, 520, at=("c3s32", "Kaynağı", -0.1), size=84, rot=-0.06)


@CM.ckind("c3_sehir_kalir")
def k_sehir_kalir(cx, **kw):
    k_sehir_kalir_impl(cx, **kw)
