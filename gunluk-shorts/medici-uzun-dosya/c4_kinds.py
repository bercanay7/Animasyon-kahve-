"""c4_kinds — c4 «Kubbe ve Kefaret» özel çekim türleri (Parça 2 sahne yazarı). `scenes_c4.py` içinde import edilir; `@CM.ckind` ile kaydolur.

Dünya koordinatı = nötr kamerada ekran koordinatı (1920×1080). Kamera: `cam=[(çapa, look(wx, wy, z)), …]`.
Kaynak disiplini: yüz yok (siluet), şiddet yok; ekrana yalnız script sözcükleri/brif kartları. Rivayet (ANEKDOT) sahneleri gravür sepyası.
Ortak yardımcılar `p2_lib` (L) ve `c3_kinds` (K3) içindedir.
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
import c3_kinds as K3
from cilt_medici import TH
from p2_lib import (INK, P, S, GRAD_V, INKP, INKR, LINE, OVAL, POLY, R, RA, SOFT, FILLP, PT, STK, _RS, bake, blit, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth)
from c3_kinds import look, table_persp, dashed, arm_to, draw_palle_badge, PP_sheet, PP_hand, draw_dome_wip
from sk import C, H, W


# ───────────────────────────── ortak küçük çizimler ─────────────────────────────
def draw_bolt(c, x, y, w, h, col, a=255):
    """Kumaş topu (yatay silindir) — (x,y) merkez."""
    GRAD_V(c, x - w / 2, y - h / 2, x + w / 2, y + h / 2, [(mix(col, "#FFFFFF", 0.38), 0.0), (col, 0.45), (mix(col, "#000000", 0.45), 1.0)])
    for k in range(1, 6):
        c.drawLine(x - w / 2 + k * w / 6, y - h / 2, x - w / 2 + k * w / 6, y + h / 2, S(mix(col, "#000000", 0.5), 1.2, 90))
    c.drawOval(skia.Rect.MakeLTRB(x + w / 2 - h * 0.18, y - h / 2, x + w / 2 + h * 0.18, y + h / 2), P(mix(col, "#FFFFFF", 0.22)))
    c.drawOval(skia.Rect.MakeLTRB(x + w / 2 - h * 0.18, y - h / 2, x + w / 2 + h * 0.18, y + h / 2), S("#2A1A0C", 1.4, 190))
    INKR(c, x - w / 2, y - h / 2, x + w / 2, y + h / 2, 1.6, 210)


def draw_drape(c, x, ytop, w, hlen, col, t, seed=1, a=255):
    """Askıdan sarkan kumaş: dalgalı alt kenar, hafif sallanma."""
    p = skia.Path()
    p.moveTo(x - w / 2, ytop)
    p.lineTo(x + w / 2, ytop)
    n = 8
    for i in range(n + 1):
        px = x + w / 2 - w * i / n
        py = ytop + hlen + 12 * math.sin(i * 1.7 + seed + t * 1.6) + (10 if i % 2 else 0)
        p.lineTo(px, py)
    p.close()
    sh = skia.GradientShader.MakeLinear([(x - w / 2, 0), (x + w / 2, 0)], [C(mix(col, "#000000", 0.28)), C(mix(col, "#FFFFFF", 0.18)), C(mix(col, "#000000", 0.30))], [0.0, 0.5, 1.0])
    c.drawPath(p, skia.Paint(AntiAlias=True, Shader=sh))
    for k in range(1, 5):
        c.drawLine(x - w / 2 + k * w / 5, ytop, x - w / 2 + k * w / 5 + 4 * math.sin(t + k), ytop + hlen, S(mix(col, "#000000", 0.5), 1.0, 70))
    INKP(c, p, 1.6, 200)


def draw_check(c, x, y, s=1.0, col="#2E7A3E", k=1.0, w=9.0):
    p = skia.Path()
    p.moveTo(x - 34 * s, y)
    p.lineTo(x - 10 * s, y + 28 * s)
    p.lineTo(x + 40 * s, y - 36 * s)
    pm = skia.PathMeasure(p, False)
    seg = skia.Path()
    pm.getSegment(0, pm.getLength() * k, seg, True)
    c.drawPath(seg, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w * s, Color=C(col, 240), StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join))


def draw_cross(c, x, y, r, k=1.0, col="#8E2A1E", w=11.0):
    pp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, 235), StrokeCap=skia.Paint.kRound_Cap)
    pp.setPathEffect(skia.DiscretePathEffect.Make(9.0, 1.6, 4))
    c.drawLine(x - r, y - r, lerp(x - r, x + r, min(1.0, k * 2)), lerp(y - r, y + r, min(1.0, k * 2)), pp)
    if k > 0.5:
        kk = (k - 0.5) * 2
        c.drawLine(x + r, y - r, lerp(x + r, x - r, kk), lerp(y - r, y + r, kk), pp)


def draw_dome_model(c, x, yb, s=1.0, col="#CDA66A", glow=0.0, t=0.0):
    """Ahşap kubbe maketi: sekizgen kaide + tambur + kaburga çizgili kabuk (yeniden çizim; belge görseli değil)."""
    w, dh, hd = 300 * s, 70 * s, 190 * s
    R(c, x - w * 0.62, yb - 22 * s, x + w * 0.62, yb, mix(col, "#000000", 0.35))
    INKR(c, x - w * 0.62, yb - 22 * s, x + w * 0.62, yb, 1.6, 220)
    R(c, x - w / 2, yb - 22 * s - dh, x + w / 2, yb - 22 * s, col)
    INKR(c, x - w / 2, yb - 22 * s - dh, x + w / 2, yb - 22 * s, 1.8, 220)
    for k in range(5):
        c.drawLine(x - w / 2 + (k + 0.5) * w / 5, yb - 22 * s - dh, x - w / 2 + (k + 0.5) * w / 5, yb - 22 * s, S("#2A1A0C", 1.2, 120))
    base = yb - 22 * s - dh
    pts_l, pts_r = [], []
    n = 16
    for k in range(n + 1):
        u = k / n
        ex = (w / 2) * math.cos(u * math.pi / 2 * 0.97)
        ey = hd * math.sin(u * math.pi / 2 * 0.97)
        pts_l.append((x - ex, base - ey))
        pts_r.append((x + ex, base - ey))
    poly = pts_l + pts_r[::-1]
    sh = skia.GradientShader.MakeLinear([(x - w / 2, 0), (x + w / 2, 0)], [C(mix(col, "#000000", 0.30)), C(mix(col, "#FFFFFF", 0.22)), C(mix(col, "#000000", 0.38))], [0.0, 0.42, 1.0])
    c.drawPath(sk.poly_path(poly), skia.Paint(AntiAlias=True, Shader=sh))
    for k in range(1, 6):
        u = k / 6.0
        pa = skia.Path()
        for j in range(0, n + 1):
            uu = j / n
            ex = (w / 2) * math.cos(uu * math.pi / 2 * 0.97) * math.sin(u * math.pi * 0.5 + 0.35)
            ey = hd * math.sin(uu * math.pi / 2 * 0.97)
            px = x + (ex if k > 2 else -ex) * (1 if k != 3 else 0.0)
            if j == 0:
                pa.moveTo(px, base - ey)
            else:
                pa.lineTo(px, base - ey)
        c.drawPath(pa, S("#2A1A0C", 1.1, 110))
    INKP(c, sk.poly_path(poly), 1.8, 220)
    if glow > 0.01:
        SOFT(c, x, base - hd * 0.5, w * 0.9, hd * 0.9, "#FFE9A0", 120 * glow)


# ═══════════════════════════ c4s2: yün loncası katedralin yapımını denetler; kumaştan anlar, kubbeden değil; yarışma açar ═══════════════════════════
def k_lonca_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=2, dress=None)
    t = cx.t
    T = L.OD.OTint("day")
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    # ── sol: kumaş tezgâhı ──
    for i, (dx, col) in enumerate(((330, "#A8321E"), (560, "#233C8C"), (790, "#C79A3C"))):
        draw_drape(c, dx, 250, 150, 300, col, t, seed=i + 1)
    c.drawLine(210, 250, 880, 250, S("#3A2616", 8.0, 235))
    table_persp(c, 150, 930, 700, 830, apron=74, col="#7A4A28", depth=0.07)
    for (bx, by, bw, bh, col) in ((290, 650, 220, 64, "#A8321E"), (500, 648, 220, 62, "#233C8C"), (710, 651, 220, 64, "#3A7A52"), (380, 590, 210, 58, "#C79A3C"), (610, 590, 210, 58, "#7A4A8A")):
        draw_bolt(c, bx, by, bw, bh, col)
    # kumaş açılır: tezgâhın önünde ölçülür
    kc = ease_out(clamp((t - cx.at(("c4s2", "lonca", -0.3))) / 1.2), 2)
    if kc > 0.003:
        xs = 300 + 560 * kc
        c.drawRect(skia.Rect.MakeLTRB(300, 712, xs, 744), P("#A8321E", 235))
        INKR(c, 300, 712, xs, 744, 1.4, 200)
        for m in range(int((xs - 300) / 40) + 1):
            c.drawLine(300 + m * 40, 712, 300 + m * 40, 724, S("#F4E9CB", 2.0, 220))
    # tüccar siluet (ölçer)
    L.sil(f, "tuccar", 1010, FY + 6, 330, t, action="work", dir=-1, seed=14, color="#14100C", rim="#FFE2A0", rim_dir=-1, prop="staff")
    # ── sağ: yapım hâlindeki katedral (kubbesiz tambur) kemer pencerede ──
    wx0, wx1, wy0, wy1 = 1170.0, 1850.0, 190.0, 840.0
    c.save()
    pth = skia.Path()
    pth.moveTo(wx0, wy1)
    pth.lineTo(wx0, wy0 + 230)
    pth.cubicTo(wx0, wy0 - 40, wx1, wy0 - 40, wx1, wy0 + 230)
    pth.lineTo(wx1, wy1)
    pth.close()
    c.clipPath(pth, skia.ClipOp.kIntersect, True)
    sh = skia.GradientShader.MakeLinear([(0, wy0), (0, wy1)], [C("#9CBBDC"), C("#E8E4D0")], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(wx0, wy0 - 60, wx1, wy1), skia.Paint(Shader=sh))
    for hx, hy, hw, col in ((1300, 620, 520, "#93AFA5"), (1640, 650, 560, "#7F9E92")):
        c.drawOval(skia.Rect.MakeLTRB(hx - hw / 2, hy - 90, hx + hw / 2, hy + 220), P(col))
    R(c, wx0, 760, wx1, wy1, "#B8A888")
    CT_T = CT.Tint("day")
    draw_dome_wip(c, 1510, 760, 560, 250, CT_T, 0.06, u=0.0)
    c.restore()
    INKP(c, pth, 3.4, 235)
    # ── anlatı olayları ──
    # denetim: loncanın direğinden katedrale uzanan altın ip, ucunda anahtar
    kd = ease_io(clamp((t - cx.at(("c4s2", "denetimindeydi;", -0.5))) / 1.1), 2)
    if kd > 0.003:
        pa = skia.Path()
        pa.moveTo(880, 262)
        pa.cubicTo(1000, 120, 1250, 180, 1400, 470)
        pm = skia.PathMeasure(pa, False)
        seg = skia.Path()
        pm.getSegment(0, pm.getLength() * kd, seg, True)
        c.drawPath(seg, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7.0, Color=C("#C79A3C", 245), StrokeCap=skia.Paint.kRound_Cap))
        c.drawPath(seg, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0, Color=C("#FFF0B0", 220), StrokeCap=skia.Paint.kRound_Cap))
        if kd > 0.9:
            icons.draw_icon(f, "keys", 1420, 500, size=110 * ease_out((kd - 0.9) * 10), metal="gold", alpha=1.0)
    kv = clamp((t - cx.at(("c4s2", "kumaştan", -0.2))) / 0.5)
    if kv > 0.003:
        draw_check(c, 520, 470, s=1.5, k=kv)
    kq = cx.amt(("c4s2", "kubbeden", -0.2), 0.5)
    if kq > 0.003:
        icons.draw_icon(f, "question", 1510, 380 + 10 * math.sin(t * 3.0), size=130 * (0.8 + 0.2 * ease_out(kq)), metal="gold", alpha=kq, shadow=True)
    kx = cx.amt(("c4s2", "değil,", -0.1), 0.5)
    if kx > 0.003:
        draw_cross(c, 1510, 600, 120, k=kx)
    # yarışma ilanı: direğe çivilenmiş tomar açılır
    c.drawRect(skia.Rect.MakeLTRB(1096, 330, 1118, FY + 16), P("#6A4426"))
    INKR(c, 1096, 330, 1118, FY + 16, 1.6, 220)
    kn = ease_out(clamp((t - cx.at(("c4s2", "yarışma", -0.2))) / 0.9), 2.4)
    if kn > 0.003:
        hh = 300 * kn
        pp = PP_sheet(220, 300, seed=41)
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(980, 370, 1240, 370 + hh))
        pp.draw(f, 1107, 520, rot=0.03, scale=1.0, alpha=1.0, shadow=0.45)
        c.restore()
        c.drawRect(skia.Rect.MakeLTRB(988, 366 + hh, 1226, 378 + hh), P("#5E3A20"))
        if kn > 0.7:
            CM.wax_seal(f, 1107, 540, 28, "#A52A1C", alpha=1.0, t=clamp((kn - 0.7) * 3.3), mono=None)
            PP_hand(f, "YARIŞMA", 1107, 462, 40, "#2A1A0E", clamp((kn - 0.7) * 3.3), seed=5)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "YÜN LONCASI", 560, 150, at=("c4s2", "yün", -0.15), size=36, w=440)
    L.tag(f, cx, "KATEDRALİN YAPIMI", 1510, 120, at=("c4s2", "Katedralin", 0.0), size=30, w=520, hold=("c4s2", "yarışma", 0.1))


@CM.ckind("c4_lonca")
def k_lonca(cx, **kw):
    k_lonca_impl(cx, **kw)
