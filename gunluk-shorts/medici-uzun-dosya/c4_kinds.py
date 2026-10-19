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


def draw_key(c, x, y, s=1.0, a=255, rot=0.0, col="#C79A3C"):
    """Büyük eski anahtar (halka + gövde + iki diş)."""
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(rot))
    c.scale(s, s)
    pa = skia.Paint(AntiAlias=True, Color=C(col, a))
    c.drawCircle(-46, 0, 26, pa)
    c.drawCircle(-46, 0, 11, P("#EFE3C2", a))
    c.drawRect(skia.Rect.MakeLTRB(-22, -7, 74, 7), pa)
    c.drawRect(skia.Rect.MakeLTRB(48, 7, 60, 30), pa)
    c.drawRect(skia.Rect.MakeLTRB(64, 7, 74, 22), pa)
    c.drawCircle(-46, 0, 26, S("#3A2616", 2.2, a))
    c.drawRect(skia.Rect.MakeLTRB(-22, -7, 74, 7), S("#3A2616", 1.8, a))
    c.restore()


def draw_drum(c, x, yb, w, h, open_top=True, shell=0.0, t=0.0):
    """Sekizgen tambur (üç yüz görünür): mermer bantlar, yuvarlak pencereler, açık üst (kubbesiz). shell>0: üstte kısmen örülmüş kabuk."""
    fw = [w * 0.26, w * 0.48, w * 0.26]
    cols = ["#CFC6AC", "#EFE5CC", "#BDB394"]
    xs = x - w / 2
    xa = [xs, xs + fw[0], xs + fw[0] + fw[1], xs + w]
    for i in range(3):
        GRAD_V(c, xa[i], yb - h, xa[i + 1], yb, [(cols[i], 0.0), (mix(cols[i], "#8A7A58", 0.35), 1.0)])
        for kb in range(1, 5):
            yy = yb - h + kb * h / 5.0
            R(c, xa[i], yy - 3, xa[i + 1], yy + 3, "#6E9878", 120 if kb % 2 else 70)
        INKR(c, xa[i], yb - h, xa[i + 1], yb, 1.8, 220)
    rr = [h * 0.10, h * 0.22, h * 0.10]
    for i in range(3):
        cxm = (xa[i] + xa[i + 1]) / 2
        cym = yb - h * 0.52
        c.drawCircle(cxm, cym, rr[i] + 6, P("#CDBB92"))
        c.drawCircle(cxm, cym, rr[i], P("#2A1C10"))
        c.drawCircle(cxm, cym, rr[i], S("#2A1A0C", 2.0, 230))
        c.drawCircle(cxm - rr[i] * 0.25, cym - rr[i] * 0.25, rr[i] * 0.35, P("#FFE9A0", 60))
    # saçak
    R(c, xs - 14, yb - h - 16, xs + w + 14, yb - h + 8, "#D6CBAE")
    INKR(c, xs - 14, yb - h - 16, xs + w + 14, yb - h + 8, 1.8, 220)
    R(c, xs - 20, yb - 6, xs + w + 20, yb + 8, "#B8A888")
    # açık üst: iç gölge halka
    if open_top:
        c.drawOval(skia.Rect.MakeLTRB(xs + 8, yb - h - 44, xs + w - 8, yb - h + 6), P("#3A2C1C"))
        c.drawOval(skia.Rect.MakeLTRB(xs + 8, yb - h - 44, xs + w - 8, yb - h + 6), S("#2A1A0C", 2.0, 230))
        c.drawOval(skia.Rect.MakeLTRB(xs + 40, yb - h - 30, xs + w - 40, yb - h - 4), P("#1E140A"))
    if shell > 0.01:
        hd = w * 0.46 * shell
        pts_l, pts_r = [], []
        for k in range(15):
            u = k / 14.0 * shell
            ex = (w / 2 - 6) * math.cos(u * math.pi / 2 * 0.97)
            ey = w * 0.46 * math.sin(u * math.pi / 2 * 0.97)
            pts_l.append((x - ex, yb - h - 8 - ey))
            pts_r.append((x + ex, yb - h - 8 - ey))
        poly = pts_l + pts_r[::-1]
        c.drawPath(sk.poly_path(poly), P("#C65B33"))
        INKP(c, sk.poly_path(poly), 1.8, 220)
    # küçük vinç: direk + kol + halat
    cxv = x - w * 0.28
    c.drawLine(cxv, yb - h - 10, cxv, yb - h - 120, S("#4A3018", 6.0, 240))
    c.drawLine(cxv - 16, yb - h - 120, cxv + 110, yb - h - 104, S("#4A3018", 5.0, 240))
    c.drawLine(cxv + 96, yb - h - 106, cxv + 96, yb - h - 56 + 8 * math.sin(t * 1.8), S("#2A1A0C", 2.0, 220))
    R(c, cxv + 86, yb - h - 56 + 8 * math.sin(t * 1.8), cxv + 106, yb - h - 36 + 8 * math.sin(t * 1.8), "#9A8A68")


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
    draw_drum(c, 1510, 760, 520, 250, t=t)
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
            draw_key(c, 1400, 505, s=1.0 * ease_out((kd - 0.9) * 10), rot=-0.5)
    kv = clamp((t - cx.at(("c4s2", "kumaştan", -0.2))) / 0.5)
    if kv > 0.003:
        draw_check(c, 520, 470, s=1.5, k=kv)
    kq = cx.amt(("c4s2", "kubbeden", -0.2), 0.5)
    if kq > 0.003:
        icons.draw_icon(f, "question", 1510, 340 + 10 * math.sin(t * 3.0), size=130 * (0.8 + 0.2 * ease_out(kq)), metal="gold", alpha=kq, shadow=True)
    kx = cx.amt(("c4s2", "değil,", -0.1), 0.5)
    if kx > 0.003:
        draw_cross(c, 1510, 590, 130, k=kx)
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


# ───────────────────────────── takvim sayfası ─────────────────────────────
def _calendar_img(w, h, head, n_days, start_col, tone=(236, 224, 192)):
    def draw(fr):
        c = fr.c
        pp = PP_sheet(w - 20, h - 20, seed=9, tone=tone)
        pp.draw(fr, w / 2, h / 2, rot=0.0, scale=1.0, alpha=1.0, shadow=0.0)
        c.drawRect(skia.Rect.MakeLTRB(14, 14, w - 14, 86), P("#A8321E"))
        INKR(c, 14, 14, w - 14, 86, 2.0, 230)
        CM.ink(fr, head, w / 2, 66, face="title", size=42, color="#F4E9CB", align="c", track=10, alpha=1.0, emboss=False)
        cw = (w - 56) / 7.0
        ch = (h - 140) / 6.0
        for d in range(n_days):
            col = (start_col + d) % 7
            row = (start_col + d) // 7
            CM.ink(fr, str(d + 1), 28 + cw * (col + 0.5), 124 + ch * (row + 0.62), face="title_m", size=int(min(30, ch * 0.5)), color="#2A1A0E", align="c", track=0, alpha=0.9, emboss=False)
        INKR(c, 10, 10, w - 10, h - 10, 2.4, 220)
    return bake(("cal", head, n_days, start_col, w, h), w, h, draw)


def draw_calendar(f, x, y, w, h, head, n_days=30, start_col=3, a=1.0, rot=0.0, mark=None, mark_k=0.0, flip=0.0):
    """Duvar takvimi yaprağı (x,y merkez). mark: işaretlenen gün (1-tabanlı) — kırmızı halka mark_k ile çizilir. flip>0: yaprak yukarı kıvrılıp gider."""
    c = f.c
    im = _calendar_img(int(w), int(h), head, n_days, start_col)
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(rot))
    if flip > 0:
        c.translate(0, -h * 0.5 * flip)
        c.scale(1.0, 1.0 - 0.9 * flip)
        c.translate(0, h * 0.5 * flip)
    SOFT(c, 8, 14, w * 0.55, h * 0.55, "#000000", 90 * a)
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(clamp(a))
    c.drawImage(im, -w / 2, -h / 2, L.LIN, p)
    if mark is not None and mark_k > 0.01:
        d = mark - 1
        cw = (w - 56) / 7.0
        chh = (h - 140) / 6.0
        col = (d + start_col) % 7
        row = (d + start_col) // 7
        cxm = -w / 2 + 28 + cw * (col + 0.5)
        cym = -h / 2 + 124 + chh * (row + 0.55)
        ring = skia.Path()
        ring.addOval(skia.Rect.MakeLTRB(cxm - cw * 0.46, cym - chh * 0.46, cxm + cw * 0.46, cym + chh * 0.46))
        pm = skia.PathMeasure(ring, False)
        seg = skia.Path()
        pm.getSegment(0, pm.getLength() * clamp(mark_k), seg, True)
        c.drawPath(seg, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5.0, Color=C("#8E2A1E", 240), StrokeCap=skia.Paint.kRound_Cap))
    c.restore()


# ═══════════════════════════ c4s3a: ilan çıkar (Ağustos 1418) ═══════════════════════════
def k_ilan4_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=4, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    bx, by, bw, bh = 1010.0, 540.0, 620.0, 700.0
    GRAD_V(c, bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2, [("#8A5A38", 0.0), ("#5E3A20", 1.0)])
    for k_ in range(9):
        c.drawLine(bx - bw / 2, by - bh / 2 + k_ * 80, bx + bw / 2, by - bh / 2 + k_ * 80 + 3, S("#2A1608", 1.3, 110))
    INKR(c, bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2, 3.0, 230)
    R(c, bx - 60, by + bh / 2, bx + 60, FY + 14, "#4A3018")
    INKR(c, bx - 60, by + bh / 2, bx + 60, FY + 14, 1.8, 220)
    t_in = cx.at(("c4s3", "ilan", -0.55))
    k = ease_out(clamp((t - t_in) / 0.55), 3)
    pw, ph = 440.0, 570.0
    yy = lerp(-420.0, by, k)
    rot = lerp(-0.25, 0.0, k) + 0.012 * math.sin(t * 2.2) * (1 - k)
    pp = PP_sheet(pw, ph, seed=33)
    if k > 0.003:
        pp.draw(f, bx, yy, rot=rot, scale=1.0, alpha=1.0, shadow=0.55)
        c.save()
        c.translate(bx, yy)
        c.rotate(math.degrees(rot))
        kh = cx.amt(("c4s3", "ilan", -0.1), 0.5)
        PP_hand(f, "İLAN", 0, -160, 92, "#2A1A0E", kh, seed=2)
        rs = _RS(3)
        for i in range(6):
            kl = clamp((t - (cx.at(("c4s3", "çıktı:", -0.3)) + 0.12 * i)) / 0.5)
            if kl > 0:
                ww = rs.uniform(240, 340) * kl
                c.drawLine(-170, -70 + i * 38, -170 + ww, -70 + i * 38 + rs.uniform(-3, 3), S("#3A2616", 2.6, 190))
        CM.wax_seal(f, 120, 220, 30, "#A52A1C", alpha=1.0, t=clamp((t - cx.at(("c4s3", "çıktı:", 0.1))) / 0.35), mono=None)
        c.restore()
    # çiviler: çekiç vuruşlarıyla
    for i, (nx, ny) in enumerate(((-190, -270), (190, -270), (-190, 270), (190, 270))):
        th = t_in + 0.55 + 0.32 * i
        if t >= th:
            c.drawCircle(bx + nx, by + ny, 8, P("#2A2620"))
            c.drawCircle(bx + nx - 2, by + ny - 2, 2.6, P("#9A9484"))
            kk = (t - th) / 0.25
            if kk < 1:
                c.drawCircle(bx + nx, by + ny, 10 + 40 * kk, S("#FFF2B0", 3.0, int(150 * (1 - kk))))
    # çekiçli usta (siluet)
    L.sil(f, "asker", 600, FY + 10, 350, t, action="work", dir=1, seed=7, color="#14100C", rim="#FFE2A0", rim_dir=1, prop="hammer")
    # okuyan kalabalık: sağdan yürüyüp durur
    for j, (kd, sd, xe, dy) in enumerate((("halk", 21, 1560, 40), ("soylu", 22, 1690, 90), ("tuccar", 23, 1800, 20))):
        tg = cx.at(("c4s3", "Ağustos", 0.0)) + 0.45 * j
        x = max(xe, xe + 420 - 230 * max(0.0, t - tg)) if t >= tg else xe + 420
        if t < tg:
            continue
        arrived = x <= xe + 0.5
        if arrived:
            L.sil(f, kd, xe, FY + dy - 10, 310, t, action="talk" if j != 1 else "point", dir=-1, seed=sd, color="#14100C", rim="#FFE2A0", rim_dir=-1)
        else:
            L.sil(f, kd, x, FY + dy - 10, 310, t, dir=-1, seed=sd, color="#14100C", rim="#FFE2A0", rim_dir=-1, walker=230.0)
    L.end(cx, cam, motes_n=14)
    L.engr(f, cx, "AĞUSTOS 1418", 960, 150, ("c4s3", "Ağustos", -0.1), size=76, track=14, dur=1.0, glow=0.15)


@CM.ckind("c4_ilan")
def k_ilan4(cx, **kw):
    k_ilan4_impl(cx, **kw)


# ═══════════════════════════ c4s3b: model için 200 altın florin ödül, teslim eylül sonuna kadar ═══════════════════════════
def k_odul_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=5, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    # model (kaide üstünde)
    km = ease_out(clamp((t - cx.at(("c4s3", "kullanılacak", -0.15))) / 0.9), 3)
    R(c, 780, 770, 1140, FY, "#6E4524")
    INKR(c, 780, 770, 1140, FY, 2.0, 220)
    R(c, 760, 750, 1160, 774, "#8A5A38")
    INKR(c, 760, 750, 1160, 774, 1.8, 220)
    if km > 0.003:
        draw_dome_model(c, 960, 750 + (1 - km) * 90, s=1.25, col="#CDA66A", glow=0.35 * km, t=t)
    # 200 florin: sağda sütun
    n_target = 200
    kc = ease_out(clamp((t - cx.at(("c4s3", "iki", -0.2))) / 1.4), 2.2)
    ncoin = int(36 * kc)
    L.coin_stack(c, 1560, FY - 8, ncoin, r=70, gap=11.0)
    if kc > 0.02:
        sp = CM.engraved(CM.fmt_int(n_target * kc), "title", 116, 8.0, TH.fg)
        CM.draw_spr(f, sp, 1560, 270, "c", alpha=smooth(kc * 5), shadow=0.0)
        CM.ink(f, "ALTIN FLORİN", 1560, 345, face="title_m", size=36, color=TH.fg2, align="c", track=6, alpha=smooth(kc * 5), emboss=False)
    # takvim (solda): eylül
    kt = ease_out(clamp((t - cx.at(("c4s3", "teslim", -0.4))) / 0.8), 3)
    if kt > 0.003:
        draw_calendar(f, 420, 470 + (1 - kt) * 60, 420, 520, "EYLÜL", n_days=30, start_col=3, a=kt, rot=-0.04, mark=30, mark_k=clamp((t - cx.at(("c4s3", "sonuna", -0.1))) / 0.6))
    ko = cx.amt(("c4s3", "sonuna", 0.0), 0.5)
    if ko > 0.003:
        icons.draw_icon(f, "hourglass", 420, 790 + 6 * math.sin(t * 2.0), size=96 * (0.8 + 0.2 * ko), metal="gold", alpha=ko, shadow=True)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "MODEL", 960, 250, at=("c4s3", "modele", -0.2), size=36, w=300)
    L.tag(f, cx, "EYLÜL SONU", 420, 150, at=("c4s3", "eylül", -0.1), size=34, w=420)


@CM.ckind("c4_odul")
def k_odul(cx, **kw):
    k_odul_impl(cx, **kw)


# ═══════════════════════════ c4s4: 1420 baharı — Brunelleschi'nin tasarımı seçilir; Ghiberti'yle birlikte işin başına geçer ═══════════════════════════
def k_secim_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=6, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    # iki siluet (el sıkışır) — masanın arkasında
    t_hs = cx.at(("c4s4", "birlikte", -0.35))
    h_ = 470.0
    xm = 960.0
    for (xx, dr, kd, sd) in ((xm - 0.30 * h_, 1, "soylu", 12), (xm + 0.30 * h_, -1, "banker", 13)):
        L.sil(f, kd, xx, FY + 4, h_, t, action="handshake", dir=dr, seed=sd, color="#14100C", rim="#FFE2A0", rim_dir=dr, t0=t_hs)
    table_persp(c, 440, 1480, 770, 880, apron=70, col="#7A4A28", depth=0.07)
    # iki maket: sol elenen (soluk), sağ seçilen (altın)
    kk = cx.amt(("c4s4", "tasarımı", -0.3), 0.7)
    ks = ease_out(clamp((t - cx.at(("c4s4", "seçildi;", -0.3))) / 0.8), 3)
    draw_dome_model(c, 690, 790, s=0.80, col=mix("#B8B0A0", "#8A8070", 0.2 * ks), glow=0.0, t=t)
    draw_dome_model(c, 1240, 790, s=0.80, col="#CDA66A", glow=0.5 * ks, t=t)
    if ks > 0.003:
        CM.wax_seal(f, 1240, 740, 36, "#A52A1C", alpha=1.0, t=clamp(ks * 1.4), mono=None)
        draw_check(c, 1240, 580 - 30 * (1 - ks), s=1.3, k=clamp(ks * 1.6))
    # bahar dalı (pencere yok; sade çiçekli dal sağ üst)
    kb = cx.amt(("c4s4", "baharında", -0.2), 0.8)
    if kb > 0.003:
        pth = skia.Path()
        pth.moveTo(1920, 120)
        pth.cubicTo(1700, 150, 1560, 230, 1430, 190)
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7.0, Color=C("#5A3C22", int(235 * kb)), StrokeCap=skia.Paint.kRound_Cap))
        rs = _RS(11)
        for i in range(14):
            fx = lerp(1920, 1430, i / 13.0) + rs.uniform(-14, 14)
            fy = 120 + (190 - 120) * (i / 13.0) * 0.8 + rs.uniform(-22, 40) + 30 * math.sin(i)
            kf = clamp((kb * 14 - i) / 1.5)
            if kf > 0:
                for pet in range(5):
                    a_ = pet * 1.2566 + 0.3
                    c.drawCircle(fx + math.cos(a_) * 11 * kf, fy + math.sin(a_) * 11 * kf, 8 * kf, P("#F6D4DC", 235))
                c.drawCircle(fx, fy, 5 * kf, P("#E8C25A"))
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "BRUNELLESCHI", 740, 330, at=("c4s4", "Brunelleschi'nin", -0.1), size=32, w=400)
    L.tag(f, cx, "GHIBERTI", 1180, 330, at=("c4s4", "Ghiberti'yle", -0.1), size=32, w=300)
    L.date_plate(f, cx, "1420 · BAHAR", ("c4s4", "1420", -0.1), x=96, y=860, size=46)


@CM.ckind("c4_secim")
def k_secim(cx, **kw):
    k_secim_impl(cx, **kw)


# ───────────────────────────── konuşma balonu ─────────────────────────────
def draw_bubble(f, x, y, w, h, lines, k, tail=(0.0, 60.0), size=34, tone="#F6F0DC", seed=3):
    """Konuşma balonu: (x,y) merkez; tail=(dx,dy) kuyruk ucu göreli konum; lines: el yazısı satırları (k: 0..1 açılış)."""
    if k <= 0.003:
        return
    c = f.c
    c.save()
    c.translate(x, y)
    sc = 0.7 + 0.3 * ease_out(k)
    c.scale(sc, sc)
    rr = skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, h / 2)
    tp = skia.Path()
    tp.moveTo(-w * 0.10, h / 2 - 2)
    tp.lineTo(tail[0], tail[1])
    tp.lineTo(w * 0.10, h / 2 - 2)
    tp.close()
    SOFT(c, 6, 10, w * 0.52, h * 0.58, "#000000", 70 * k)
    c.drawRoundRect(rr, 24, 24, skia.Paint(AntiAlias=True, Color=C(tone, int(250 * k))))
    c.drawPath(tp, skia.Paint(AntiAlias=True, Color=C(tone, int(250 * k))))
    c.drawRoundRect(rr, 24, 24, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.4, Color=C("#2A1A0C", int(220 * k))))
    c.drawLine(-w * 0.10, h / 2, tail[0], tail[1], S("#2A1A0C", 2.4, 220 * k))
    c.drawLine(w * 0.10, h / 2, tail[0], tail[1], S("#2A1A0C", 2.4, 220 * k))
    n = len(lines)
    for i, ln in enumerate(lines):
        PP_hand(f, ln, 0, -h / 2 + (i + 0.78) * h / max(1, n) - (4 if n > 1 else 0), size, "#2A1A0E", k, seed=seed + i)
    c.restore()


def draw_plan_scroll(f, x, y, w, h, k, seed=2):
    """Açılan plan tomarı: dome kesit kroki çizgileri (kaburga/balıksırtı). k: açılma 0..1."""
    if k <= 0.003:
        return
    c = f.c
    hh = h * ease_out(k)
    pp = PP_sheet(w, h, seed=seed)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(x - w / 2 - 10, y - h / 2 - 12, x + w / 2 + 10, y - h / 2 + hh))
    pp.draw(f, x, y, rot=0.0, scale=1.0, alpha=1.0, shadow=0.5)
    # kubbe kesit krokisi
    pa = skia.Path()
    pa.moveTo(x - w * 0.32, y + h * 0.22)
    pa.cubicTo(x - w * 0.32, y - h * 0.34, x + w * 0.32, y - h * 0.34, x + w * 0.32, y + h * 0.22)
    c.drawPath(pa, S("#3A2616", 2.6, 220))
    pb = skia.Path()
    pb.moveTo(x - w * 0.22, y + h * 0.22)
    pb.cubicTo(x - w * 0.22, y - h * 0.18, x + w * 0.22, y - h * 0.18, x + w * 0.22, y + h * 0.22)
    c.drawPath(pb, S("#3A2616", 2.0, 190))
    c.drawLine(x - w * 0.36, y + h * 0.22, x + w * 0.36, y + h * 0.22, S("#3A2616", 2.6, 220))
    for i in range(1, 5):
        xx = x - w * 0.32 + i * w * 0.64 / 5
        c.drawLine(xx, y + h * 0.22, xx * 0.6 + x * 0.4, y - h * 0.18 - 10, S("#3A2616", 1.2, 150))
    c.restore()
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2 - 8, y - h / 2 + hh - 8, x + w / 2 + 8, y - h / 2 + hh + 8), P("#5E3A20"))
    INKR(c, x - w / 2 - 8, y - h / 2 + hh - 8, x + w / 2 + 8, y - h / 2 + hh + 8, 1.6, 220)


# ═══════════════════════════ c4s5–s6: yumurta (Vasari'ye göre) — gravür ═══════════════════════════
def k_yumurta_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=7, dress=None, mono=1.0)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    # mermer tezgâh
    table_persp(c, 640, 1420, 740, 840, apron=60, col="#7A4A28", depth=0.06)
    slab = [(700, 748), (1360, 748), (1400, 828), (660, 828)]
    c.drawPath(sk.poly_path(slab), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 748), (0, 828)], [C("#F2EFE8"), C("#C9C4B6")], [0, 1])))
    INKP(c, sk.poly_path(slab), 2.0, 220)
    for i in range(6):
        c.drawLine(740 + i * 110, 752, 730 + i * 116 + 26, 824, S("#8A8474", 1.0, 80))
    # siluetler
    t_say = cx.at(("c4s5", "yumurtayı", -0.4))
    act_b = "point" if t_say - 0.2 <= t < cx.at(("c4s5", "tabanını", -0.6)) else "idle"
    L.sil(f, "soylu", 470, FY + 2, 410, t, action=act_b, dir=1, seed=12, color="#14100C", rim="#FFE2A0", rim_dir=1, t0=t_say)
    for j, (xx, sd, kd) in enumerate(((1560, 31, "tuccar"), (1700, 32, "banker"), (1840, 33, "halk"))):
        act = "talk" if (cx.at(("c4s6", "Rakipler", -0.1)) <= t < cx.at(("c4s6", "planı", 0.0)) or cx.at(("c4s5", "kimse", 0.3)) <= t < cx.at(("c4s5", "tabanını", -0.3))) else "idle"
        L.sil(f, kd, xx, FY + 8 + 10 * j, 380, t, action=act, dir=-1, seed=sd, color="#14100C", rim="#FFE2A0", rim_dir=-1, energy=1.2)
    # rakiplerin yumurtaları: sırayla devrilir
    t_a0 = cx.at(("c4s5", "söylemiş;", -0.3))
    for i, xe in enumerate((1010, 1140, 1270)):
        ta = t_a0 + 0.55 * i
        if t < ta:
            continue
        u = t - ta
        wob = (0.04 + 0.10 * clamp(u / 0.9)) * math.sin(u * 13.0)
        if u < 0.9:
            L.draw_egg(c, xe, 742, s=1.9, tilt=wob)
        else:
            kf = ease_in(clamp((u - 0.9) / 0.35), 2)
            sgn = 1 if i != 1 else -1
            L.draw_egg(c, xe + sgn * 34 * kf, 742 + 6 * kf, s=1.9, tilt=sgn * (0.30 + 1.25 * kf))
    kxm = cx.amt(("c4s5", "başaramayınca", -0.1), 0.5)
    if kxm > 0.003:
        for i, xe in enumerate((1010, 1140, 1270)):
            draw_cross(c, xe, 640, 34, k=clamp(kxm * 1.2 - i * 0.12), w=7.0)
    # Brunelleschi'nin yumurtası: dokunup tabanını kırar, dik durur
    t_k = cx.at(("c4s5", "tabanını", -0.4))
    if t >= t_k - 0.5:
        uu = t - t_k
        if uu < 0:
            yy = 742 - 120 * ease_out(clamp((uu + 0.5) / 0.5), 2)
            L.draw_egg(c, 830, yy, s=1.9, tilt=0.2)
        elif uu < 0.8:
            tap = abs(math.sin(uu / 0.8 * math.pi * 2.0))
            L.draw_egg(c, 830, 742 - 120 + 120 * clamp(tap) * 0.9, s=1.9, tilt=0.2 * (1 - clamp(uu / 0.8)), crack=clamp(uu / 0.8))
        else:
            L.draw_egg(c, 830, 742, s=1.9, tilt=0.0, crack=1.0)
            kg = clamp((uu - 0.8) / 0.6)
            SOFT(c, 830, 700, 110, 110, "#FFE9A0", 150 * (1 - 0.3 * kg) * min(1.0, kg * 3))
            if kg < 1:
                c.drawCircle(830, 700, 50 + 120 * kg, S("#FFF2B0", 3.0, int(170 * (1 - kg))))
        if 0.15 < uu < 1.2:                                       # kırık kabuk parçaları
            ks_ = (uu - 0.15) / 1.05
            for q in range(6):
                ang = -2.6 + q * 0.42
                px = 830 + math.cos(ang) * 120 * ks_
                py = 742 + math.sin(ang) * 120 * ks_ + 260 * ks_ * ks_
                c.save()
                c.translate(px, py)
                c.rotate(math.degrees(ks_ * 9 + q))
                c.drawPath(sk.poly_path([(-7, -5), (8, -3), (3, 7)]), P("#F4EAD2", int(255 * (1 - ks_))))
                c.restore()
    # konuşma balonları
    kb = cx.amt(("c4s6", "bunu", -0.2), 0.4) * (1.0 - cx.amt(("c4s6", "planı", -0.3), 0.4))
    draw_bubble(f, 1640, 300, 470, 130, ["BUNU BİZ DE", "YAPARDIK"], kb, tail=(-10, 100), size=40)
    # plan tomarı + karşılık balonu
    kp = clamp((t - cx.at(("c4s6", "planı", -0.2))) / 0.8)
    draw_plan_scroll(f, 250, 520, 230, 300, kp)
    if kp > 0.05:
        for pxx in (150, 350):
            c.drawCircle(pxx, 352, 7, P("#2A2620"))
    kd = cx.amt(("c4s6", "kubbeyi", 0.0), 0.5)
    if kd > 0.003:
        draw_bubble(f, 560, 250, 340, 200, [], kd, tail=(-30, 130))
        draw_dome_model(c, 560, 310, s=0.45 * (0.7 + 0.3 * ease_out(kd)), col="#CDA66A", glow=0.3 * kd, t=t)
    L.end(cx, cam, mono=1.0, motes_n=14, light=(1000.0, 560.0, 1500.0, 0.9))
    L.tag(f, cx, "VASARI", 1500, 110, at=("c4s5", "Vasari'ye", -0.1), size=36, w=300, hold=("c4s6", "Rakipler", -0.3))
    L.stamp_at(f, cx, "ANEKDOT", 1500, 200, at=("c4s5", "göre", 0.0), size=48, rot=-0.07, hold=("c4s6", "Rakipler", -0.3))
    L.tag(f, cx, "BRUNELLESCHI", 470, 160, at=("c4s5", "Brunelleschi,", -0.1), size=30, w=380, hold=("c4s6", "Rakipler", -0.3))
    L.tag(f, cx, "RAKİPLERİ", 1640, 330, at=("c4s5", "rakiplerine", -0.1), size=30, w=320, hold=("c4s5", "yumurtayı", 0.3))


@CM.ckind("c4_yumurta")
def k_yumurta(cx, **kw):
    k_yumurta_impl(cx, **kw)


# ═══════════════════════════ c4s7: aynı yumurta 1565'te Benzoni'nin kaleminde Kolomb'a bağlanır ═══════════════════════════
def k_kolomb_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=8, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    XL, XR = 520.0, 1400.0
    kl = cx.amt(("c4s7", -0.1), 0.6)
    L.sil(f, "soylu", XL, FY + 6, 420, t, action="idle", dir=1, seed=12, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kl)
    kr = ease_out(cx.amt(("c4s7", "Kolomb'a", -0.5), 0.8), 2)
    if kr > 0.003:
        L.sil(f, "denizci", XR + (1 - kr) * 260, FY + 6, 420, t, action="idle" if kr > 0.99 else "idle", dir=-1, seed=15, color="#14100C", rim="#FFE2A0", rim_dir=-1, alpha=kr)
    # gemi simgesi (Kolomb tarafı)
    ks = cx.amt(("c4s7", "Kolomb'a", -0.2), 0.7)
    if ks > 0.003:
        icons.draw_icon(f, "ship", XR + 20, 250 + 8 * math.sin(t * 1.6), size=170 * (0.8 + 0.2 * ease_out(ks)), metal="gold", alpha=ks, shadow=True)
    # kitap + kalem (Benzoni'nin 1565'i)
    kb = cx.amt(("c4s7", "Benzoni'nin", -0.3), 0.7)
    if kb > 0.003:
        icons.draw_icon(f, "book", 960, 250 + 6 * math.sin(t * 1.4), size=150 * (0.8 + 0.2 * ease_out(kb)), metal="gold", alpha=kb, shadow=True)
        icons.draw_icon(f, "quill", 1060, 230 + 6 * math.sin(t * 1.9), size=110 * (0.8 + 0.2 * ease_out(kb)), metal="gold", alpha=kb, shadow=True)
    # yumurta: Brunelleschi'nin elinde → yay → Kolomb'a; sonra 'kim kimden' için ileri geri
    t_fly = cx.at(("c4s7", "bağlanır;", -0.5))
    t_pp = cx.at(("c4s7", "kimden", -0.3))
    ex0, ey0 = XL + 120, FY - 210
    ex1, ey1 = XR - 120, FY - 210
    if t < t_fly:
        L.draw_egg(c, ex0, ey0 + 4 * math.sin(t * 2.0), s=1.5, tilt=0.15)
    else:
        u = t - t_fly
        if t < t_pp:
            k = clamp(u / 0.9)
            ex = lerp(ex0, ex1, ease_io(k, 1.6))
            ey = lerp(ey0, ey1, k) - 260 * math.sin(math.pi * k)
            L.draw_egg(c, ex, ey, s=1.5, tilt=0.3 + 5.0 * k)
        else:
            v = (t - t_pp) / 0.9
            ph = v % 2.0
            k = ph if ph < 1.0 else 2.0 - ph
            ex = lerp(ex1, ex0, ease_io(k, 1.6)) if False else lerp(ex1, ex0, k)
            ey = ey0 - 220 * math.sin(math.pi * (ph % 1.0))
            L.draw_egg(c, ex, ey, s=1.5, tilt=0.3 + 4.0 * v)
    kq = cx.amt(("c4s7", "kimden", -0.3), 0.5)
    if kq > 0.003:
        icons.draw_icon(f, "question", 960, 420 + 10 * math.sin(t * 3.0), size=190 * (0.8 + 0.2 * ease_out(kq)), metal="gold", alpha=kq, shadow=True)
        dashed(c, XL + 200, 520, XR - 200, 520, col="#8A7A62", w=3.0, a=int(200 * kq), dash=(10.0, 12.0), phase=-t * 30)
    L.end(cx, cam, motes_n=14)
    L.engr(f, cx, "1565", 960, 160, ("c4s7", "1565'te", -0.1), size=84, track=16, dur=0.9, glow=0.15)
    L.tag(f, cx, "BENZONI", 1010, 360, at=("c4s7", "Benzoni'nin", -0.1), size=34, w=340)
    L.stamp_src(f, cx, "TEK KAYNAK", 1530, 130, at=("c4s7", "bağlanır;", -0.2), size=40, rot=-0.07)


@CM.ckind("c4_kolomb")
def k_kolomb(cx, **kw):
    k_kolomb_impl(cx, **kw)


# ═══════════════════════════ c4s8: 25 Mart 1436, Floransa takvimine göre yılbaşı ═══════════════════════════
def k_takvim_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=9, dress=None)
    t = cx.t
    k = ease_out(cx.amt(("c4s8", -0.1), 0.8), 3)
    mk = clamp((t - cx.at(("c4s8", "25", 0.0))) / 0.7)
    draw_calendar(f, 960, 560 + (1 - k) * 80, 640, 720, "MART", n_days=31, start_col=2, a=k, rot=-0.02, mark=25, mark_k=mk)
    # büyük 25
    kn = cx.amt(("c4s8", "25", -0.05), 0.5)
    if kn > 0.003:
        CM.draw_spr(f, CM.engraved("25", "title", 150, 8.0, TH.fg), 480, 540, "c", alpha=kn, shadow=0.0)
    # yılbaşı kurdelesi + zambak
    ky = ease_out(clamp((t - cx.at(("c4s8", "yılbaşı.", -0.9))) / 0.9), 2.5)
    if ky > 0.003:
        w = 560 * ky
        rb = skia.Path()
        rb.moveTo(1240 - 0, 470)
        rb.lineTo(1240 + w, 470)
        rb.lineTo(1240 + w - 30, 520)
        rb.lineTo(1240 + w, 570)
        rb.lineTo(1240, 570)
        rb.close()
        c.drawPath(rb, P("#A8321E"))
        INKP(c, rb, 2.0, 220)
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(1240, 460, 1240 + w, 580))
        CM.ink(f, "YILBAŞI", 1240 + 270, 538, face="title", size=56, color="#F4E9CB", align="c", track=10, alpha=1.0, emboss=False)
        c.restore()
        if ky > 0.6:
            icons.draw_icon(f, "fleur", 1500, 340 + 8 * math.sin(t * 2.0), size=150 * smooth((ky - 0.6) * 2.5), metal="gold", alpha=1.0, shadow=True)
    L.end(cx, cam, motes_n=18)
    L.engr(f, cx, "1436", 960, 150, ("c4s8", "1436,", -0.1), size=88, track=16, dur=0.9, glow=0.15)
    L.tag(f, cx, "FLORANSA TAKVİMİ", 1500, 700, at=("c4s8", "Floransa", -0.1), size=32, w=470)


@CM.ckind("c4_takvim")
def k_takvim(cx, **kw):
    k_takvim_impl(cx, **kw)


# ═══════════════════════════ c4s9–10: Papa IV. Eugenius katedrali kutsar; özel koro Dufay'in motetini söyler ═══════════════════════════
def draw_note(c, x, y, s=1.0, a=255, rot=0.0):
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(rot))
    c.drawOval(skia.Rect.MakeLTRB(-11 * s, -8 * s, 11 * s, 8 * s), P("#2A1A0E", a))
    c.drawLine(10 * s, 0, 10 * s, -52 * s, S("#2A1A0E", 3.0 * s, a))
    p = skia.Path()
    p.moveTo(10 * s, -52 * s)
    p.cubicTo(24 * s, -44 * s, 28 * s, -30 * s, 18 * s, -22 * s)
    c.drawPath(p, S("#2A1A0E", 3.0 * s, a))
    c.restore()


def k_kutsama_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=10, dress=None)
    t = cx.t
    FY = 820.0
    T = L.OD.OTint("day")
    L.grid_floor(c, -500, 2500, FY, 1300, col1="#D6C9A6", col2="#B8A67C")
    # arka duvar: üç uzun kemerli pencere + saçak
    for i, xx in enumerate((560, 960, 1360)):
        pth = skia.Path()
        pth.moveTo(xx - 90, 520)
        pth.lineTo(xx - 90, 250)
        pth.cubicTo(xx - 90, 100, xx + 90, 100, xx + 90, 250)
        pth.lineTo(xx + 90, 520)
        pth.close()
        c.drawPath(pth, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 100), (0, 520)], [C("#9CBBDC"), C("#E8E4D0")], [0, 1])))
        INKP(c, pth, 3.0, 230)
        c.drawLine(xx, 160, xx, 520, S("#2A1A0C", 2.0, 170))
    R(c, -300, 560, 2300, 600, "#CDBB92")
    INKR(c, -300, 560, 2300, 600, 2.0, 200)
    # iki büyük sütun
    for xx in (190, 1730):
        GRAD_V(c, xx - 60, 80, xx + 60, FY, [("#CFC6AC", 0.0), ("#9C927A", 1.0)])
        R(c, xx - 80, 60, xx + 80, 110, "#B8AE94")
        R(c, xx - 80, FY - 30, xx + 80, FY, "#B8AE94")
        INKR(c, xx - 60, 80, xx + 60, FY, 2.0, 220)
    # sunak basamakları + sunak
    for i in range(3):
        R(c, 640 - i * 40, FY - 24 * (i + 1) + 24 - 24 + 24, 1280 + i * 40, FY - 24 * i, mix("#C8B88E", "#8A7A58", 0.15 * i))
        INKR(c, 640 - i * 40, FY - 24 * (i + 1), 1280 + i * 40, FY - 24 * i, 1.6, 200)
    R(c, 840, FY - 140, 1080, FY - 72, "#F0EAD8")
    INKR(c, 840, FY - 140, 1080, FY - 72, 2.0, 220)
    # papa: kutsama el hareketi; yanlarda iki yardımcı
    t_b = cx.at(("c4s9", "katedrali", -0.1))
    kp = ease_out(cx.amt(("c4s9", -0.1), 0.6), 2)
    L.sil(f, "papa", 960, FY - 70, 430, t, action="point" if t >= t_b else "idle", dir=1, seed=3, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kp, t0=t_b)
    for (xx, kd, sd, dr) in ((760, "kardinal", 6, 1), (1160, "rahip", 7, -1)):
        L.sil(f, kd, xx, FY - 40, 360, t, action="idle", dir=dr, seed=sd, color="#14100C", rim="#FFE2A0", rim_dir=dr, alpha=kp)
    kb = cx.amt(("c4s9", "kutsadı.", -0.2), 0.5)
    if kb > 0.003:
        for q in range(12):
            a_ = q * 0.5236
            c.drawLine(1010 + math.cos(a_) * 80, 520 + math.sin(a_) * 80, 1010 + math.cos(a_) * (130 + 40 * math.sin(t * 5 + q)), 520 + math.sin(a_) * (130 + 40 * math.sin(t * 5 + q)), S("#FFD060", 3.0, int(190 * kb)))
        SOFT(c, 1010, 520, 130, 130, "#FFE9A0", 120 * kb)
    # koro (sağda, yarım daire sıra): önce susar, 'korosu'yla başlar, nota yükselir
    t_ch = cx.at(("c4s10", "korosu,", -0.8))
    kch = ease_out(clamp((t - t_ch) / 0.8), 2)
    for j in range(5):
        xx = 1450 + j * 96
        if kch > 0.003:
            L.sil(f, "kesis", xx + (1 - kch) * 340, FY + 40 + (j % 2) * 14, 340, t, action="talk" if kch > 0.99 else "idle", dir=-1, seed=40 + j, color="#14100C", rim="#FFE2A0", rim_dir=-1, alpha=kch, energy=0.6)
    ksing = cx.amt(("c4s10", "korosu,", 0.0), 0.5)
    if ksing > 0.003:
        for q in range(14):
            ph = ((t - t_ch) * 0.28 + q * 0.0714) % 1.0
            nx = 1450 + (q * 53) % 480 + 18 * math.sin(ph * 9 + q)
            ny = 560 - ph * 460
            draw_note(c, nx, ny, s=0.9 + 0.3 * ((q * 7) % 3) / 3.0, a=int(235 * ksing * math.sin(math.pi * ph)), rot=0.2 * math.sin(ph * 6 + q))
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "PAPA IV. EUGENIUS", 960, 140, at=("c4s9", "IV.", -0.1), size=38, w=600, hold=("c4s10", "Papa'nın", 0.3))
    L.tag(f, cx, "DUFAY · MOTET", 1600, 230, at=("c4s10", "Dufay'in", -0.2), size=36, sub="YAZILDIĞI KABUL EDİLİR", w=520)


@CM.ckind("c4_kutsama")
def k_kutsama(cx, **kw):
    k_kutsama_impl(cx, **kw)


# ═══════════════════════════ c4s11: Tenor partisi — kutsama ayini ezgisi; Terribilis est locus iste — «Ne heybetli bu yer.» ═══════════════════════════
def draw_square_note(c, x, y, a=255, glow=0.0):
    if glow > 0.02:
        SOFT(c, x, y, 34, 26, "#FFD060", 170 * glow)
    c.drawRect(skia.Rect.MakeLTRB(x - 12, y - 11, x + 12, y + 11), P(mix("#2A1A0E", "#C79A3C", glow * 0.5), a))
    c.drawRect(skia.Rect.MakeLTRB(x - 12, y - 11, x + 12, y + 11), S("#1A0E06", 1.4, a))


def draw_c_clef(c, x, y, a=255):
    pa = skia.Paint(AntiAlias=True, Color=C("#2A1A0E", a))
    c.drawRect(skia.Rect.MakeLTRB(x - 14, y - 46, x - 4, y + 46), pa)
    c.drawRect(skia.Rect.MakeLTRB(x + 4, y - 40, x + 14, y - 4), pa)
    c.drawRect(skia.Rect.MakeLTRB(x + 4, y + 4, x + 14, y + 40), pa)


def k_nota_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=11, dress=None)
    t = cx.t
    kp = ease_out(cx.amt(("c4s11", -0.1), 0.8), 3)
    pw, ph = 1480.0, 760.0
    pp = PP_sheet(pw, ph, seed=51)
    pp.draw(f, 960, 540 + (1 - kp) * 60, rot=-0.008, scale=1.0, alpha=kp, shadow=0.6)
    SY = 440.0
    X0, X1 = 330.0, 1590.0
    # dört çizgili kızıl portre
    for i in range(4):
        yy = SY + i * 34
        c.drawLine(X0, yy, lerp(X0, X1, ease_out(clamp((t - cx.at(("c4s11", "Tenorlardan", -0.2))) / 0.9), 2)), yy, S("#8E2A1E", 2.6, int(235 * kp)))
    kc = cx.amt(("c4s11", "Tenorlardan", 0.0), 0.5)
    draw_c_clef(c, X0 + 40, SY + 51, a=int(240 * kc))
    # notalar (kare nota): sırayla gelir; 'ezgisi' ile bir bölümü altın yanar
    pitch = [0, 1, 0, -1, 1, 2, 1, 0, 1, -1, 0, 1, 0, -1]
    t_n0 = cx.at(("c4s11", "birinde", -0.1))
    kz = cx.amt(("c4s11", "ezgisi", -0.1), 0.6)
    for i, pv in enumerate(pitch):
        nx = X0 + 150 + i * 80
        ny = SY + 51 - pv * 17
        kn = ease_out(clamp((t - (t_n0 + 0.17 * i)) / 0.3), 3)
        if kn > 0.003:
            gl = kz * (1.0 if 3 <= i <= 11 else 0.0) * (0.6 + 0.4 * math.sin(t * 4 + i))
            draw_square_note(c, nx, ny - (1 - kn) * 30, a=int(255 * kn), glow=gl)
    # Latince heceler: söylendiği anda yazılır
    for (txt, xx, an) in (("Terribilis", 560.0, ("c4s11", "Terribilis", -0.1)), ("est", 880.0, ("c4s11", "est", -0.1)), ("locus", 1030.0, ("c4s11", "locus", -0.1)), ("iste", 1300.0, ("c4s11", "iste,", -0.1))):
        k = clamp((t - cx.at(an)) / 0.5)
        if k > 0.003:
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(xx - 200, SY + 120, xx - 200 + 400 * k, SY + 220))
            PP_hand(f, txt, xx, SY + 190, 64, "#2A1A0E", 1.0, seed=hash(txt) % 50 + 1)
            c.restore()
    # çeviri
    kt = cx.amt(("c4s11", "“Ne", -0.2), 0.8)
    if kt > 0.003:
        sp = CM.gilt("“NE HEYBETLİ BU YER.”", "title", 70, 8.0)
        CM.draw_spr(f, sp, 960, 740, "c", alpha=kt, shadow=0.4)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "TENOR", 440, 150, at=("c4s11", "Tenorlardan", -0.1), size=36, w=300)
    L.tag(f, cx, "KUTSAMA AYİNİ EZGİSİ", 1340, 150, at=("c4s11", "kutsama", -0.1), size=32, w=640)


@CM.ckind("c4_nota")
def k_nota(cx, **kw):
    k_nota_impl(cx, **kw)


# ═══════════════════════════ c4s13: Medici'nin belgeli Brunelleschi'si — yanındaki San Lorenzo, Eski Sakristi ═══════════════════════════
def draw_umbrella_dome_elev(c, x, yb, w, h, a=255, k=1.0, t=0.0):
    """Eski Sakristi kesiti (yeniden çizim): kübik oda, gri taş pilastrlar, şemsiye kubbe (12 kaburga) ve oculus."""
    R(c, x - w / 2, yb - h, x + w / 2, yb, "#EDE5D0")
    INKR(c, x - w / 2, yb - h, x + w / 2, yb, 2.4, 230)
    # pilastrlar + arklar (gri taş: pietra serena)
    for sg in (-1, 1):
        R(c, x + sg * (w / 2 - 44) - 14, yb - h * 0.62, x + sg * (w / 2 - 44) + 14, yb, "#8C9096")
    R(c, x - w / 2, yb - h * 0.62 - 12, x + w / 2, yb - h * 0.62 + 6, "#8C9096")
    # kubbe: yarım daire, kaburgalar
    cy = yb - h * 0.62 - 12
    r = w / 2
    pth = skia.Path()
    pth.moveTo(x - r, cy)
    pth.arcTo(skia.Rect.MakeLTRB(x - r, cy - r, x + r, cy + r), 180.0, 180.0, False)
    pth.close()
    c.drawPath(pth, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((x, cy - r * 0.2), r * 1.2, [C("#FFF8E4"), C("#E4DABE")], [0.0, 1.0])))
    for i in range(13):
        ang = math.pi + i * math.pi / 12.0
        c.drawLine(x + math.cos(ang) * r * 0.16, cy + math.sin(ang) * r * 0.16, x + math.cos(ang) * r, cy + math.sin(ang) * r, S("#8C9096", 4.0, 235))
    for rr in (0.55,):
        c.drawArc(skia.Rect.MakeLTRB(x - r * rr, cy - r * rr, x + r * rr, cy + r * rr), 180.0, 180.0, False, S("#8C9096", 3.0, 200))
    c.drawCircle(x, cy - r * 0.1, r * 0.12, P("#9CBBDC"))
    c.drawCircle(x, cy - r * 0.1, r * 0.12, S("#8C9096", 4.0, 240))
    INKP(c, pth, 2.2, 230)
    # sunak nişi (apsis): küçük kemerli oda + sunak
    ap = skia.Path()
    ap.moveTo(x - 70, yb)
    ap.lineTo(x - 70, yb - h * 0.20)
    ap.cubicTo(x - 70, yb - h * 0.36, x + 70, yb - h * 0.36, x + 70, yb - h * 0.20)
    ap.lineTo(x + 70, yb)
    ap.close()
    c.drawPath(ap, P("#4A3A28", 235))
    INKP(c, ap, 2.4, 230)
    R(c, x - 40, yb - 38, x + 40, yb - 18, "#F0EAD8")
    INKR(c, x - 40, yb - 38, x + 40, yb - 18, 1.4, 220)
    for i in range(6):
        c.drawLine(x - w / 2 + 14, yb - 8 + i * 0.0, x + w / 2 - 14, yb - 8, S("#8A7A58", 1.0, 60))


def k_sakristi_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=12, dress=None)
    t = cx.t
    kp = ease_out(cx.amt(("c4s13", -0.1), 0.8), 3)
    pw, ph = 1560.0, 800.0
    PP_sheet(pw, ph, seed=61).draw(f, 960, 540 + (1 - kp) * 60, rot=0.006, scale=1.0, alpha=kp, shadow=0.6)
    # beat 1: palle + pergel
    k1 = cx.amt(("c4s13", "Medici'nin", -0.1), 0.6)
    if k1 > 0.003:
        import cilt_props as CP
        CP.draw_arms(f, 330, 360, 150, alpha=k1, shadow=0.5, glow=0.0, glint=None)
        kd_ = ease_out(cx.amt(("c4s13", "belgeli", -0.2), 0.6), 3)
        if kd_ > 0.003:
            pp_ = PP_sheet(210, 270, seed=62)
            pp_.draw(f, 330, 640 + (1 - kd_) * 40, rot=-0.05, scale=1.0, alpha=kd_, shadow=0.5)
            for i in range(6):
                c.drawLine(250, 560 + i * 26, 410 - (i % 3) * 22, 560 + i * 26, S("#3A2616", 2.2, int(190 * kd_)))
            CM.wax_seal(f, 372, 720, 26, "#A52A1C", alpha=1.0, t=clamp((kd_ - 0.5) * 2.0), mono=None)
    # beat 2: plan (Duomo sekizgeni + San Lorenzo haçı), aralarında kısa mesafe
    k2 = cx.amt(("c4s13", "hemen", -0.2), 0.7)
    if k2 > 0.003:
        a2 = int(255 * k2)
        # Duomo
        nave = skia.Rect.MakeLTRB(1020, 430, 1250, 560)
        c.drawRect(nave, P("#D8CBA6", a2))
        INKR(c, 1020, 430, 1250, 560, 2.4, a2)
        oc = skia.Path()
        for i in range(8):
            ang = math.pi / 8 + i * math.pi / 4
            px, py = 1350 + math.cos(ang) * 118, 495 + math.sin(ang) * 118
            (oc.moveTo if i == 0 else oc.lineTo)(px, py)
        oc.close()
        c.drawPath(oc, P("#D8CBA6", a2))
        INKP(c, oc, 2.6, a2)
        c.drawCircle(1350, 495, 62, S("#8A7A58", 2.0, int(200 * k2)))
        # San Lorenzo (Latin haçı)
        R(c, 520, 466, 820, 524, "#D8CBA6", a2)
        INKR(c, 520, 466, 820, 524, 2.4, a2)
        R(c, 620, 400, 690, 590, "#D8CBA6", a2)
        INKR(c, 620, 400, 690, 590, 2.4, a2)
        # mesafe işareti
        dashed(c, 830, 495, 1010, 495, col="#8E2A1E", w=4.0, a=int(235 * k2), dash=(10.0, 8.0), phase=-t * 20)
        for xx in (830, 1010):
            c.drawLine(xx, 478, xx, 512, S("#8E2A1E", 3.0, int(235 * k2)))
    # beat 3: Eski Sakristi vurgusu (kare oda) + kesit
    k3 = cx.amt(("c4s13", "Eski", -0.3), 0.7)
    if k3 > 0.003:
        R(c, 520, 524, 600, 604, "#F2E8C8", int(255 * k3))
        INKR(c, 520, 524, 600, 604, 3.0, 255 * k3)
        SOFT(c, 560, 564, 80, 80, "#FFD060", 150 * k3 * (0.7 + 0.3 * math.sin(t * 4)))
        c.drawCircle(560, 564, 70 + 12 * math.sin(t * 3), S("#C79A3C", 3.0, int(230 * k3)))
        kk = ease_out(clamp((t - cx.at(("c4s13", "Eski", 0.3))) / 0.9), 3)
        if kk > 0.003:
            c.save()
            c.translate(0, (1 - kk) * 120)
            SOFT(c, 1240, 600, 330, 40, "#000000", 90 * kk)
            draw_umbrella_dome_elev(c, 1240, 790, 520, 520, a=int(255 * kk), k=kk, t=t)
            c.restore()
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "BRUNELLESCHI", 330, 180, at=("c4s13", "Brunelleschi'si", -0.3), size=32, w=400, hold=("c4s13", "yanındaki", 0.0))
    L.tag(f, cx, "SAN LORENZO", 700, 330, at=("c4s13", "San", -0.1), size=32, w=380)
    L.tag(f, cx, "KATEDRAL", 1350, 330, at=("c4s13", "hemen", 0.0), size=32, w=300, hold=("c4s13", "Eski", -0.3))
    L.tag(f, cx, "ESKİ SAKRİSTİ", 1240, 160, at=("c4s13", "Eski", 0.0), size=36, w=460)


@CM.ckind("c4_sakristi")
def k_sakristi(cx, **kw):
    k_sakristi_impl(cx, **kw)


# ═══════════════════════════ ortak: raf, merdiven, manastır ═══════════════════════════
def draw_shelf(c, x0, y0, w, h, rows=3, seed=1, a=255):
    """Kitap rafı: ahşap çerçeve, sıralı renkli kitap sırtları."""
    R(c, x0, y0, x0 + w, y0 + h, "#4A3018")
    INKR(c, x0, y0, x0 + w, y0 + h, 2.4, 230)
    rs = _RS(seed)
    rh = h / rows
    cols = ["#8E2A1E", "#233C8C", "#3A7A52", "#C79A3C", "#6A4A8A", "#7A4A28", "#A8321E"]
    for r in range(rows):
        yb = y0 + (r + 1) * rh - 8
        R(c, x0 + 6, yb, x0 + w - 6, yb + 8, "#6A4426")
        x = x0 + 14
        while x < x0 + w - 30:
            bw = rs.uniform(16, 34)
            bh = rs.uniform(rh * 0.55, rh * 0.86)
            col = cols[int(rs.randint(0, len(cols)))]
            R(c, x, yb - bh, x + bw, yb, col)
            INKR(c, x, yb - bh, x + bw, yb, 1.0, 200)
            c.drawLine(x + 3, yb - bh + 10, x + bw - 3, yb - bh + 10, S("#F4E9CB", 1.2, 140))
            x += bw + rs.uniform(1, 5)


def draw_monastery(c, x, yb, s=1.0, a=255, t=0.0, build=1.0):
    """San Marco tipi manastır: revaklı avlu bloğu + küçük kilise + çan kulesi (genel temsil)."""
    w, h = 520 * s, 170 * s
    k = clamp(build)
    hh = h * k
    R(c, x - w / 2, yb - hh, x + w / 2, yb, "#E3D3AE", a)
    INKR(c, x - w / 2, yb - hh, x + w / 2, yb, 2.2, 220)
    if k > 0.3:
        for i in range(7):
            ax = x - w / 2 + 30 * s + i * 70 * s
            p = skia.Path()
            p.moveTo(ax - 22 * s, yb)
            p.lineTo(ax - 22 * s, yb - 56 * s)
            p.cubicTo(ax - 22 * s, yb - 82 * s, ax + 22 * s, yb - 82 * s, ax + 22 * s, yb - 56 * s)
            p.lineTo(ax + 22 * s, yb)
            p.close()
            c.drawPath(p, P("#4A3A28", int(235 * min(1.0, (k - 0.3) * 3))))
            INKP(c, p, 1.4, 190)
    # çatı
    R(c, x - w / 2 - 10 * s, yb - hh - 16 * s, x + w / 2 + 10 * s, yb - hh + 4 * s, "#B9552F", a)
    INKR(c, x - w / 2 - 10 * s, yb - hh - 16 * s, x + w / 2 + 10 * s, yb - hh + 4 * s, 1.6, 210)
    # kilise + çan kulesi
    if k > 0.5:
        ka = clamp((k - 0.5) * 2.0)
        ch = 150 * s * ka
        R(c, x + w * 0.18, yb - hh - ch, x + w * 0.46, yb - hh, "#EFE5CC", int(255 * ka))
        INKR(c, x + w * 0.18, yb - hh - ch, x + w * 0.46, yb - hh, 2.0, int(220 * ka))
        tw = 230 * s * ka
        R(c, x - w * 0.42, yb - hh - tw, x - w * 0.32, yb - hh, "#EFE5CC", int(255 * ka))
        INKR(c, x - w * 0.42, yb - hh - tw, x - w * 0.32, yb - hh, 2.0, int(220 * ka))
        if ka > 0.8:
            tp = skia.Path()
            tp.moveTo(x - w * 0.43, yb - hh - tw)
            tp.lineTo(x - w * 0.37, yb - hh - tw - 40 * s)
            tp.lineTo(x - w * 0.31, yb - hh - tw)
            tp.close()
            c.drawPath(tp, P("#B9552F", a))
            INKP(c, tp, 1.6, 210)


def draw_stairs(c, x0, y0, x1, y1, n=9, col="#B49C70"):
    """Soldan sağa yükselen basamaklar: (x0,y0) alt sol, (x1,y1) üst sağ (yb tabanı)."""
    sw = (x1 - x0) / n
    sh = (y0 - y1) / n
    for i in range(n):
        xa = x0 + i * sw
        yt = y0 - (i + 1) * sh
        R(c, xa, yt, xa + sw + 1, 1040, mix(col, "#7A6A48", 0.10 * (i % 2) + 0.05 * (n - i) / n))
        R(c, xa, yt, xa + sw + 1, yt + 14, mix(col, "#FFFFFF", 0.22))
        c.drawLine(xa, yt, xa + sw, yt, S("#2A1A0C", 2.6, 220))
        c.drawLine(xa, yt, xa, yt + sh, S("#2A1A0C", 2.0, 190))


def stair_pos(x0, y0, x1, y1, n, u):
    """Merdiven üstünde u∈[0,1] konumu (ayak noktası)."""
    sw = (x1 - x0) / n
    sh = (y0 - y1) / n
    i = min(n - 1, int(u * n))
    return x0 + u * (x1 - x0), y0 - (i + 1) * sh


# ═══════════════════════════ c4s14a: kitapçı Vespasiano yazar ═══════════════════════════
def k_vespasiano_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=13, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    L.OD.draw_window(c, L.OD.OTint("day"), 795, 190, 330, 520, night=False)
    draw_shelf(c, 140, 160, 520, 560, rows=4, seed=3)
    draw_shelf(c, 1240, 160, 520, 560, rows=4, seed=7)
    # kitapçı tezgâhı (ortada) + yazı masası
    table_persp(c, 600, 1380, 760, 860, apron=70, col="#7A4A28", depth=0.07)
    # yazan figür: masa arkasında oturan siluet (yazar)
    kw = cx.amt(("c4s14", "yazar:", -0.8), 0.5)
    L.OD.seated(f, "banker", 880, 800, 360, t, action="write", dir=1, seed=9, sil="#14100C", rim="#FFE2A0", rim_dir=1, t0=cx.at(("c4s14", "kitapçısı", 0.0)), alpha=1.0)
    # masa üstü: kâğıt + mürekkep; yazı satırları 'yazar:' ile açılır
    pp = PP_sheet(260, 180, seed=71)
    pp.draw(f, 1100, 752, rot=-0.02, scale=1.0, alpha=1.0, shadow=0.4)
    rs = _RS(5)
    t_l = cx.at(("c4s14", "yazar:", -0.3))
    for i in range(5):
        kl = clamp((t - (t_l + 0.28 * i)) / 0.45)
        if kl > 0:
            c.drawLine(1010, 706 + i * 22, 1010 + rs.uniform(140, 200) * kl, 706 + i * 22 + rs.uniform(-2, 2), S("#3A2616", 2.4, 200))
    K3.OD_inkwell(c, 1270, 790)
    # tezgâhta kodekslerden yığın
    for i, (bx, col) in enumerate(((700, "#8E2A1E"), (730, "#233C8C"), (710, "#3A7A52"))):
        R(c, bx - 60, 745 - i * 22, bx + 60, 767 - i * 22, col)
        INKR(c, bx - 60, 745 - i * 22, bx + 60, 767 - i * 22, 1.4, 210)
    L.end(cx, cam, motes_n=16, light=(1000.0, 540.0, 1500.0, 0.9))
    L.tag(f, cx, "VESPASIANO", 960, 120, at=("c4s14", "Vespasiano", -0.1), size=40, sub="KİTAPÇI", w=520)
    L.tag(f, cx, "COSİMO'NUN ÖLÜMÜNDEN SONRA", 960, 250, at=("c4s14", "ölümünden", -0.2), size=32, w=760, hold=("c4s14", "şunu", 0.2))
    L.stamp_at(f, cx, "ANEKDOT", 1560, 150, at=("c4s14", "yazar:", -0.2), size=46, rot=-0.07)


@CM.ckind("c4_vespasiano")
def k_vespasiano(cx, **kw):
    k_vespasiano_impl(cx, **kw)


# ═══════════════════════════ c4s14b: vicdanda biriken yük; yönetip başkalarının önüne geçmek isteyen çoğu adam ═══════════════════════════
def k_vicdan_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=14, dress=None)
    t = cx.t
    T = L.OD.OTint("day")
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    # sol: VİCDAN çuvalı — kâğıtlar düşerek birikir, şişer
    t_b = cx.at(("c4s14", "vicdanında", -0.2))
    kb = ease_out(clamp((t - t_b) / 0.7), 3)
    n_in = clamp((t - cx.at(("c4s14", "hayli", -0.1))) / 1.8)
    swell = 1.0 + 0.30 * n_in
    if kb > 0.003:
        L.draw_bag(c, 430, 680 + (1 - kb) * 160, s=2.5 * swell * kb, seed=5, sway=1.4 * math.sin(t * 1.7), slips=min(6, 1 + int(n_in * 6)))
    for i in range(9):
        tp = cx.at(("c4s14", "hayli", -0.15)) + 0.2 * i
        u = (t - tp) / 0.9
        if 0 < u < 1:
            L.draw_slip(c, 430 + 50 * math.sin(i * 2.1), lerp(60, 330, u * u), w=70, h=48, rot=1.8 * u + i, lines=1, seed=i + 2, a=int(255 * (1 - clamp((u - 0.8) * 5))))
    # sağ: merdiven + boş koltuk; tırmananlar çuval taşır
    SX0, SY0, SX1, SY1, N = 900.0, 870.0, 1700.0, 470.0, 8
    draw_stairs(c, SX0, SY0, SX1, SY1, n=N)
    R(c, 1700, SY1, 1900, SY1 + 24, "#8A5A38")
    INKR(c, 1700, SY1, 1900, SY1 + 24, 2.0, 230)
    L.OD.draw_chair(c, T, 1800, SY1, back_h=330, seat_h=90, w=130, facing=-1, col="#6E4524", cushion="#8E2A30")
    SOFT(c, 1800, SY1 - 180, 160, 220, "#FFE9A0", 70)
    ts = cx.at(("c4s14", "devlet", -0.2))
    t_sack = cx.at(("c4s14", "geldiği", -0.6))
    t_pass = cx.at(("c4s14", "başkalarının", 0.0))
    for j, (kd, sd, du, u0, spd) in enumerate((("soylu", 31, 0.0, 0.0, 0.085), ("banker", 32, 0.5, -0.12, 0.085), ("tuccar", 33, 0.9, -0.22, 0.07), ("halk", 34, 1.4, -0.34, 0.07))):
        u = u0 + spd * max(0.0, t - ts - du)
        if j == 1 and t > t_pass:                                 # ikinci figür öne geçer
            u += 0.11 * clamp((t - t_pass) / 1.2)
        if u < 0.0 or u > 1.02:
            continue
        uu = clamp(u)
        fx, fy = stair_pos(SX0, SY0, SX1, SY1, N, uu)
        prop = "sack" if t >= t_sack + 0.2 * j else None
        L.sil(f, kd, fx - 40, fy + 8, 300, t, dir=1, seed=sd, color="#14100C", rim="#FFE2A0", rim_dir=1, walker=70.0 if uu < 0.98 else 0.0, prop=prop)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "VİCDAN", 430, 230, at=("c4s14", "vicdanında", -0.2), size=40, w=330)
    L.tag(f, cx, "ÇOĞU ADAM", 1300, 170, at=("c4s14", "çoğu", -0.1), size=34, w=380)


@CM.ckind("c4_vicdan")
def k_vicdan(cx, **kw):
    k_vicdan_impl(cx, **kw)


# ═══════════════════════════ c4s15–16: Papa'yla konuşmaya gider; San Marco'yu yaptırmasını, on bin florin harcamasını önerir ═══════════════════════════
def k_papa_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=15, dress=None)
    t = cx.t
    T = L.OD.OTint("day")
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300, col1="#D6C9A6", col2="#B8A67C")
    # taht (sağda) + papa
    R(c, 1380, FY - 60, 1860, FY, "#8E2A1E")
    INKR(c, 1380, FY - 60, 1860, FY, 2.0, 220)
    L.OD.draw_chair(c, T, 1640, FY - 60, back_h=420, seat_h=100, w=150, facing=-1, col="#6E4524", cushion="#8E2A30")
    t_talk = cx.at(("c4s16", "Papa", -0.1))
    L.sil(f, "papa", 1640, FY - 62, 400, t, action="talk" if t >= t_talk else "idle", dir=-1, seed=3, color="#14100C", rim="#FFE2A0", rim_dir=-1, energy=1.1, t0=t_talk)
    # Cosimo: omzunda ağır çuval, soldan yürür
    t_w = cx.at(("c4s15", -0.2))
    u = clamp((t - t_w) / max(1.0, (cx.at(("c4s16", -0.1)) - t_w)))
    x = lerp(180.0, 880.0, ease_io(u, 1.3))
    walking = u < 0.98
    L.sil(f, "soylu", x, FY + 8, 400, t, dir=1, seed=4, color="#14100C", rim="#FFE2A0", rim_dir=1, walker=88.0 if walking else 0.0, prop="sack")
    # manastır maketi masa üstünde (ortada)
    table_persp(c, 920, 1320, 760, 860, apron=60, col="#7A4A28", depth=0.07)
    kmo = ease_out(clamp((t - cx.at(("c4s16", "yaptırmasını,", -0.9))) / 1.6), 2)
    if kmo > 0.003:
        draw_monastery(c, 1120, 756, s=0.72, a=255, t=t, build=kmo)
    # on bin florin
    k10 = cx.amt(("c4s16", "on", -0.2), 0.6)
    if k10 > 0.003:
        L.coin_stack(c, 1000, 756, int(8 * k10), r=44, gap=9.0)
        sp = CM.engraved("10.000", "title", 96, 8.0, TH.fg)
        CM.draw_spr(f, sp, 640, 340, "c", alpha=k10, shadow=0.0)
        CM.ink(f, "FLORİN", 640, 410, face="title_m", size=36, color=TH.fg2, align="c", track=6, alpha=k10, emboss=False)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "PAPA", 1640, 170, at=("c4s15", "Papa'yla", -0.1), size=38, w=300)
    L.tag(f, cx, "SAN MARCO", 1120, 400, at=("c4s16", "Marco'daki", -0.1), size=32, sub="DOMİNİKEN MANASTIRI", w=470)
    L.stamp_at(f, cx, "ANEKDOT", 220, 110, at=("c4s15", "Bu", -0.1), size=46, rot=-0.07)


@CM.ckind("c4_papa")
def k_papa(cx, **kw):
    k_papa_impl(cx, **kw)


# ═══════════════════════════ c4s17: on bin yetmemiş; işi bitirmek için kırk binden fazla florin ═══════════════════════════
def k_kirkbin_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=16, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    # sol: manastır inşaatı
    kb = clamp((t - cx.at(("c4s17", "yetmemiş;", -0.1))) / max(0.5, cx.at(("c4s17", "harcamış.", -0.2)) - cx.at(("c4s17", "yetmemiş;", -0.1))))
    build = 0.38 + 0.62 * ease_io(kb, 1.4)
    draw_monastery(c, 700, FY - 6, s=1.15, a=255, t=t, build=build)
    if build < 0.99:                                           # iskele çizgileri
        for i in range(6):
            xx = 700 - 300 + i * 120
            c.drawLine(xx, FY - 6, xx, FY - 6 - 210 * 1.15 * 0.8, S("#6A4426", 3.0, 200))
        for j in range(3):
            yy = FY - 6 - 70 * (j + 1)
            c.drawLine(700 - 320, yy, 700 + 320, yy, S("#6A4426", 3.0, 200))
    # sağ: florin sütunu — 10.000 sınırı kırmızı kesik çizgi
    ka = ease_out(cx.amt(("c4s17", -0.1), 0.6), 2)
    kgrow = ease_io(clamp((t - cx.at(("c4s17", "yetmemiş;", 0.0))) / (cx.at(("c4s17", "harcamış.", -0.2)) - cx.at(("c4s17", "yetmemiş;", 0.0)))), 1.6)
    ncoin = int(10 * ka + 30 * kgrow)
    CX_ = 1460.0
    L.coin_stack(c, CX_, FY - 6, ncoin, r=80, gap=11.0)
    ylim = FY - 6 - 10 * 11.0
    dashed(c, CX_ - 190, ylim, CX_ + 190, ylim, col="#A8321E", w=4.0, a=int(235 * ka), dash=(14.0, 9.0), phase=-t * 30)
    # sayaç: 10.000 → çizilir; 40.000+ sayar
    k10 = cx.amt(("c4s17", "On", -0.05), 0.5) * (1.0 - 0.0)
    kx = cx.amt(("c4s17", "yetmemiş;", 0.0), 0.4)
    k40 = ease_out(clamp((t - cx.at(("c4s17", "kırk", -0.2))) / 1.5), 2.5)
    if k40 < 0.02:
        sp = CM.engraved("10.000", "title", 100, 8.0, TH.fg)
        CM.draw_spr(f, sp, 1060, 260, "c", alpha=smooth(k10 * 3), shadow=0.0)
        if kx > 0.003:
            c.drawLine(900, 262, 900 + 320 * kx, 250, S("#8E2A1E", 9.0, 235))
    else:
        sp = CM.engraved(CM.fmt_int(40000 * k40) + ("+" if k40 > 0.97 else ""), "title", 108, 8.0, TH.fg)
        CM.draw_spr(f, sp, 1060, 260, "c", alpha=1.0, shadow=0.0)
        CM.ink(f, "FLORİN", 1060, 330, face="title_m", size=36, color=TH.fg2, align="c", track=6, alpha=smooth(k40 * 4), emboss=False)
    # taşan florinler
    if kgrow > 0.8:
        for q in range(5):
            ph = ((t * 1.3 + q * 0.2) % 1.0)
            L.draw_coin_flat(c, CX_ + (q - 2) * 64 + 40 * ph, FY - 6 - 40 * 11.0 - 30 + 300 * ph * ph, r=22, a=int(255 * (1 - ph)))
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "SAN MARCO", 420, 200, at=("c4s17", "bitirmek", -0.3), size=34, w=360)
    L.stamp_at(f, cx, "ANEKDOT", 1560, 200, at=("c4s17", "yetmemiş;", -0.2), size=44, rot=-0.07)


@CM.ckind("c4_kirkbin")
def k_kirkbin(cx, **kw):
    k_kirkbin_impl(cx, **kw)


# ═══════════════════════════ c4s18: «Kefaret» kelimesi sonradan, modern bir yazarın cümlesi; Papa'nın sözü olarak kayıtlı değil ═══════════════════════════
def k_kefaret_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=17, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    # Papa (solda) ve söz satırları (belge)
    kp = ease_out(cx.amt(("c4s18", -0.1), 0.6), 2)
    L.sil(f, "papa", 360, FY + 4, 440, t, action="talk", dir=1, seed=3, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kp, energy=0.8)
    pw, ph = 900.0, 560.0
    PP_sheet(pw, ph, seed=81).draw(f, 1090, 520, rot=-0.01, scale=1.0, alpha=kp, shadow=0.55)
    rs = _RS(6)
    for i in range(8):
        kl = clamp((t - (cx.at(("c4s18", -0.1)) + 0.12 * i)) / 0.5)
        if kl > 0:
            ww = rs.uniform(520, 700) * kl
            c.drawLine(740, 330 + i * 46, 740 + ww, 330 + i * 46 + rs.uniform(-2, 2), S("#3A2616", 2.6, 190))
    # KEFARET etiketi: 'sonradan' yapışır; 'kayıtlı değil'de soyulup gider
    t_hit = cx.at(("c4s18", "Kefaret", 0.2)) if False else cx.at(("c4s18", "kelimesi", -0.1))
    t_pl = cx.at(("c4s18", "kayıtlı", -0.2))
    kfall = ease_in(clamp((t - (t_hit - 0.5)) / 0.5), 2)
    sx, sy = 1090.0, 520.0
    if t < t_hit:
        px_, py_ = lerp(1500.0, sx, kfall), lerp(120.0, sy, kfall)
        sc, rot, a, peel = lerp(1.5, 1.0, kfall), lerp(-0.25, -0.04, kfall), clamp((t - (t_hit - 0.55)) / 0.2), 0.0
    else:
        kp_ = clamp((t - t_pl) / 0.9)
        px_, py_, sc, rot = sx, sy, 1.0, -0.04
        peel = kp_
        a = 1.0 - clamp((kp_ - 0.5) / 0.5)
    if a > 0.003:
        L.draw_sticker(f, px_, py_, 560, 180, "“KEFARET”", a=a, rot=rot, scale=sc, peel=peel, size=68, track=6.0)
    if t >= t_hit and t < t_hit + 0.45:
        kk = (t - t_hit) / 0.45
        c.drawCircle(sx, sy, 150 + 190 * kk, S("#FFF2B0", 4.0, int(160 * (1 - kk))))
    # soyulunca altta yalnız boş çizgiler kalır + KAYITLI DEĞİL
    L.end(cx, cam, motes_n=14)
    L.stamp_at(f, cx, "SONRADAN", 1090, 250, at=("c4s18", "sonradan,", -0.1), size=52, rot=-0.07, hold=("c4s18", "kayıtlı", -0.3))
    L.tag(f, cx, "MODERN BİR YAZAR", 1500, 160, at=("c4s18", "modern", -0.1), size=34, w=520, hold=("c4s18", "kayıtlı", -0.3))
    L.tag(f, cx, "PAPA", 360, 190, at=("c4s18", "Papa'nın", -0.2), size=36, w=280)
    L.stamp_at(f, cx, "KAYITLI DEĞİL", 1090, 800, at=("c4s18", "değil.", -0.5), size=62, rot=-0.06)


@CM.ckind("c4_kefaret")
def k_kefaret(cx, **kw):
    k_kefaret_impl(cx, **kw)


# ═══════════════════════════ c4s19–20: San Marco'da iki hücre — biri kendine, biri konuklara; konuk odası kıyak ═══════════════════════════
def draw_goblet(c, x, y, s=1.0, a=255):
    p = skia.Path()
    p.moveTo(x - 22 * s, y - 40 * s)
    p.lineTo(x + 22 * s, y - 40 * s)
    p.cubicTo(x + 22 * s, y - 8 * s, x + 6 * s, y - 4 * s, x + 4 * s, y + 4 * s)
    p.lineTo(x + 4 * s, y + 24 * s)
    p.lineTo(x + 20 * s, y + 30 * s)
    p.lineTo(x - 20 * s, y + 30 * s)
    p.lineTo(x - 4 * s, y + 24 * s)
    p.lineTo(x - 4 * s, y + 4 * s)
    p.cubicTo(x - 6 * s, y - 4 * s, x - 22 * s, y - 8 * s, x - 22 * s, y - 40 * s)
    p.close()
    c.drawPath(p, P("#E0B84E", a))
    INKP(c, p, 1.8, a)
    c.drawRect(skia.Rect.MakeLTRB(x - 18 * s, y - 38 * s, x + 18 * s, y - 28 * s), P("#8E2A1E", a))


def k_hucreler_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=18, dress=None)
    t = cx.t
    # plan zemini: levha (parşömen)
    kp = ease_out(cx.amt(("c4s19", -0.1), 0.7), 3)
    PP_sheet(1640, 840, seed=91).draw(f, 960, 540, rot=0.0, scale=1.0, alpha=kp, shadow=0.55)
    # koridor
    R(c, 260, 540, 1660, 620, "#DCCFA8")
    INKR(c, 260, 540, 1660, 620, 2.4, 220)
    for i in range(14):
        c.drawLine(260 + i * 100, 540, 260 + i * 100, 620, S("#8A7A58", 1.0, 100))
    widths = [220, 220, 220, 360, 220]
    x = 300.0
    cells = []
    for i, wd in enumerate(widths):
        kc = ease_out(clamp((t - (cx.at(("c4s19", "San", -0.2)) + 0.12 * i)) / 0.5), 3)
        cells.append((x, wd))
        if kc > 0.003:
            R(c, x, 280, x + wd, 540, "#EFE5CC", int(255 * kc))
            INKR(c, x, 280, x + wd, 540, 2.6, int(235 * kc))
            R(c, x + wd / 2 - 24, 534, x + wd / 2 + 24, 546, "#F4E9CB")           # kapı boşluğu
            c.drawLine(x + wd / 2 - 24, 540, x + wd / 2 + 24, 540, S("#8A7A58", 2.0, 220))
        x += wd + 28
    # hücre A (kendine): ikinci hücre; hücre B (konuklara): dördüncü
    ax, aw = cells[1]
    bx, bw = cells[3]
    # basit hücre (A): dar yatak, tabure, dar pencere
    R(c, ax + 36, 400, ax + aw - 36, 470, "#B8A888")
    INKR(c, ax + 36, 400, ax + aw - 36, 470, 1.8, 220)
    R(c, ax + 36, 400, ax + 80, 470, "#F4E9CB")
    c.drawCircle(ax + aw - 56, 506, 14, P("#8A5A38"))
    R(c, ax + aw / 2 - 8, 296, ax + aw / 2 + 8, 340, "#5A4A34")
    # konuk hücresi (B): bordürlü halı, direkli büyük yatak, yastıklar, yan masa, kadeh, meyve
    R(c, bx + 18, 296, bx + bw - 18, 524, "#8E2A1E", 190)
    INKR(c, bx + 18, 296, bx + bw - 18, 524, 2.0, 220)
    for q in range(6):
        c.drawLine(bx + 30 + q * (bw - 60) / 5, 304, bx + 30 + q * (bw - 60) / 5, 516, S("#E0B84E", 2.0, 150))
    R(c, bx + 44, 330, bx + bw - 44, 456, "#C79A3C")
    INKR(c, bx + 44, 330, bx + bw - 44, 456, 2.0, 230)
    R(c, bx + 52, 338, bx + 118, 392, "#F4E9CB")
    R(c, bx + 52, 396, bx + 118, 450, "#F4E9CB")
    for (px_, py_) in ((bx + 44, 330), (bx + bw - 44, 330), (bx + 44, 456), (bx + bw - 44, 456)):
        c.drawCircle(px_, py_, 9, P("#5A3C22"))
    R(c, bx + bw - 120, 470, bx + bw - 30, 520, "#6E4524")
    INKR(c, bx + bw - 120, 470, bx + bw - 30, 520, 1.6, 220)
    draw_goblet(c, bx + bw - 92, 486, s=0.55)
    for q in range(3):
        c.drawCircle(bx + bw - 58 + q * 12, 492 - (q % 2) * 6, 7, P("#B8321E"))
    # keşiş simgesi: 'değildi' ile çarpı
    km = cx.amt(("c4s19", "Keşiş", -0.1), 0.5) * (1.0 - cx.amt(("c4s19", "bağışı", -0.3), 0.4))
    if km > 0.003:
        icons.draw_icon(f, "monk", 960, 180, size=170 * (0.8 + 0.2 * ease_out(km)), metal="bronze", alpha=km, shadow=True)
        kx_ = cx.amt(("c4s19", "değildi", -0.1), 0.4)
        if kx_ > 0.003:
            draw_cross(c, 960, 180, 70, k=kx_, w=9.0)
    # bağış: florinler manastıra akar
    kb = clamp((t - cx.at(("c4s19", "bağışı", -0.2))) / 1.2)
    for q in range(6):
        ph = clamp(kb * 1.4 - q * 0.12)
        if 0 < ph < 1:
            L.draw_coin_flat(c, lerp(300, 960, ph), lerp(120, 330, ph) - 60 * math.sin(math.pi * ph), r=22, a=int(255 * (1 - ph * 0.3)))
    # iki hücreye vurgu
    kh = cx.amt(("c4s19", "iki", -0.1), 0.5)
    for (xx, ww, lab) in ((ax, aw, "1"), (bx, bw, "2")):
        if kh > 0.003:
            c.drawRect(skia.Rect.MakeLTRB(xx - 6, 274, xx + ww + 6, 546), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5.0, Color=C("#C79A3C", int(240 * kh))))
            CM.ink(f, lab, xx + ww / 2, 250, face="title", size=56, color=TH.acc, align="c", track=0, alpha=kh, emboss=False)
    # Cosimo işareti (kendine) ve konuk işareti
    k1 = cx.amt(("c4s19", "kendine,", -0.3), 0.5)
    if k1 > 0.003:
        import cilt_props as CP
        CP.draw_arms(f, ax + aw / 2, 660, 90, alpha=k1, shadow=0.4, glow=0.0, glint=None)
    k2 = cx.amt(("c4s19", "konuklara.", -0.5), 0.5)
    if k2 > 0.003:
        icons.draw_icon(f, "star", bx + bw / 2, 660, size=96 * (0.8 + 0.2 * ease_out(k2)), metal="gold", alpha=k2, shadow=True)
    # c4s20: VIP etiketi konuk odasının kapısına yapışır
    t_v = cx.at(("c4s20", "kıyakmış.", -0.7))
    kv = ease_in(clamp((t - (t_v - 0.5)) / 0.5), 2)
    if t >= t_v - 0.5:
        L.draw_sticker(f, lerp(bx + bw / 2 + 400, bx + bw / 2, kv), lerp(180.0, 590.0, kv), 220, 96, "VIP", a=clamp((t - (t_v - 0.55)) / 0.2), rot=lerp(-0.3, -0.06, kv), scale=lerp(1.5, 1.0, kv), size=56, track=10.0)
        if t >= t_v and t < t_v + 0.45:
            kk = (t - t_v) / 0.45
            c.drawCircle(bx + bw / 2, 590, 90 + 130 * kk, S("#FFF2B0", 4.0, int(170 * (1 - kk))))
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "SAN MARCO", 960, 120, at=("c4s19", "Marco'da", -0.2), size=40, w=420, hold=("c4s19", "iki", 0.0))
    L.tag(f, cx, "COSİMO İÇİN", ax + aw / 2, 750, at=("c4s19", "biri", -0.1), size=30, w=330, hold=("c4s20", "Evet,", -0.3))
    L.tag(f, cx, "KONUKLAR İÇİN", bx + bw / 2, 750, at=("c4s19", "önemli", -0.2), size=30, w=380, hold=("c4s20", "Evet,", -0.3))
    L.stamp_at(f, cx, "YORUM", 1500, 200, at=("c4s20", "Evet,", 0.0), size=46, rot=-0.07)


@CM.ckind("c4_hucreler")
def k_hucreler(cx, **kw):
    k_hucreler_impl(cx, **kw)


# ═══════════════════════════ palazzo cepheleri (genel temsil; belge görseli değil) ═══════════════════════════
_PAL = dict(
    medici=dict(low="#C9A872", mid="#E3CFA0", up="#EAD9B0", cor="#8A6A3A", rus=2, pil=False, nw=5),
    rucellai=dict(low="#E0D4B2", mid="#E8DDBE", up="#EFE5CC", cor="#A8986E", rus=0, pil=True, nw=5),
    strozzi=dict(low="#B4A486", mid="#BDAE90", up="#C6B898", cor="#7A6C54", rus=3, pil=False, nw=6),
)


def draw_palazzo(c, x, yb, w, h, style="medici", a=255, build=1.0, glow=0.0, dim=0.0):
    """Üç kat: bosajlı zemin, pencere sıraları, çıkıntılı saçak. build<1: aşağıdan yukarı yükselir (kısmi yükseklik)."""
    S_ = _PAL[style]
    k = clamp(build)
    if k <= 0.003:
        return
    hh = h * k
    x0, x1 = x - w / 2, x + w / 2
    f1, f2 = 0.36, 0.64
    cl = lambda col: mix(col, "#6A5A44", dim * 0.5)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(x0 - 30, yb - hh - 60, x1 + 30, yb + 4))
    # katlar
    y_top = yb - h
    R(c, x0, y_top + h * f2, x1, yb, cl(S_["low"]), a)
    R(c, x0, y_top + h * f1, x1, y_top + h * f2, cl(S_["mid"]), a)
    R(c, x0, y_top, x1, y_top + h * f1, cl(S_["up"]), a)
    # bosaj
    if S_["rus"]:
        rows = 6 + 2 * S_["rus"]
        for r in range(rows):
            yy = yb - r * (h * (f1 if S_["rus"] >= 3 else 0.36) / 5.5)
            if S_["rus"] >= 3 or yy > y_top + h * f2 - 4:
                c.drawLine(x0, yy, x1, yy, S("#2A1A0C", 1.4, 130))
                off = 0 if r % 2 else 60
                for xv in range(int(x0 + off), int(x1), 120):
                    c.drawLine(xv, yy, xv, yy - h * 0.065, S("#2A1A0C", 1.0, 90))
    if S_["pil"]:
        for i in range(int(S_["nw"]) + 1):
            xp = x0 + w * i / S_["nw"]
            R(c, xp - 9, y_top + 10, xp + 9, yb, cl("#CDBE98"), a)
            INKR(c, xp - 9, y_top + 10, xp + 9, yb, 1.0, 130)
        for yy in (y_top + h * f1, y_top + h * f2):
            R(c, x0, yy - 7, x1, yy + 7, cl("#B8A87E"), a)
            INKR(c, x0, yy - 7, x1, yy + 7, 1.0, 140)
    # pencereler (kemerli)
    nw = S_["nw"]
    for fl, (ya, yb2) in enumerate(((y_top + h * 0.06, y_top + h * 0.28), (y_top + h * f1 + h * 0.05, y_top + h * f1 + h * 0.24))):
        for i in range(nw):
            wx = x0 + w * (i + 0.5) / nw
            ww = w / nw * 0.30
            p = skia.Path()
            p.moveTo(wx - ww, yb2)
            p.lineTo(wx - ww, ya + ww * 1.1)
            p.cubicTo(wx - ww, ya - ww * 0.3, wx + ww, ya - ww * 0.3, wx + ww, ya + ww * 1.1)
            p.lineTo(wx + ww, yb2)
            p.close()
            c.drawPath(p, P("#3A2A1C", 235))
            INKP(c, p, 1.4, 190)
            c.drawLine(wx, ya + ww * 0.5, wx, yb2, S("#CDBE98", 2.0, 200))
    # zemin kat: kapı kemeri + küçük pencereler
    dw = w * 0.07
    dp = skia.Path()
    dp.moveTo(x - dw, yb)
    dp.lineTo(x - dw, yb - h * 0.20)
    dp.cubicTo(x - dw, yb - h * 0.30, x + dw, yb - h * 0.30, x + dw, yb - h * 0.20)
    dp.lineTo(x + dw, yb)
    dp.close()
    c.drawPath(dp, P("#2A1C10", 240))
    INKP(c, dp, 2.0, 220)
    for i in range(nw):
        wx = x0 + w * (i + 0.5) / nw
        if abs(wx - x) < w * 0.12:
            continue
        R(c, wx - 18, yb - h * 0.20, wx + 18, yb - h * 0.08, "#2A1C10", 235)
        INKR(c, wx - 18, yb - h * 0.20, wx + 18, yb - h * 0.08, 1.2, 200)
    # saçak
    R(c, x0 - 18, y_top - 22, x1 + 18, y_top + 10, cl(S_["cor"]), a)
    INKR(c, x0 - 18, y_top - 22, x1 + 18, y_top + 10, 1.8, 220)
    R(c, x0 - 8, y_top + 10, x1 + 8, y_top + 22, cl(mix(S_["cor"], "#000000", 0.2)), a)
    INKR(c, x0, yb - h, x1, yb, 2.4, 230)
    c.restore()
    if glow > 0.01:
        SOFT(c, x, yb - h * 0.5, w * 0.7, h * 0.7, "#FFE9A0", 110 * glow)


# ═══════════════════════════ c4s21–22a: Medici tek değildi; Giovanni Rucellai kendi defterine yazdı ═══════════════════════════
def k_saraylar_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=19, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    specs = (("medici", 440, 440, 500, ("c4s21", -0.05), "MEDICI"), ("rucellai", 960, 440, 470, ("c4s21", "tek", 0.0), "RUCELLAI"), ("strozzi", 1480, 460, 540, ("c4s21", "değildi.", -0.25), "STROZZI"))
    kr = cx.amt(("c4s22", "Rucellai", -0.2), 0.7)
    for (st, x, w, h, an, name) in specs:
        kb = ease_out(cx.amt(an, 0.9), 2.4)
        dim = 0.0
        glow = 0.0
        if st != "rucellai":
            dim = 0.55 * kr
        else:
            glow = 0.7 * kr
        draw_palazzo(c, x, FY, w, h, style=st, build=kb, glow=glow, dim=dim)
        if kb > 0.4:
            ka = clamp((kb - 0.4) * 1.7)
            CM.tablet(f, x - 150, FY - h - 110, 300, 64, alpha=ka * (1 - 0.4 * dim), corner=8)
            CM.ink(f, name, x, FY - h - 66, face="title_m", size=30, color=TH.fg, align="c", track=6, alpha=ka, emboss=False)
    # Medici işareti ilk cephede
    km = cx.amt(("c4s21", "Medici", 0.1), 0.5)
    if km > 0.003:
        import cilt_props as CP
        CP.draw_arms(f, 440, FY - 640, 100, alpha=km * (1 - 0.55 * kr), shadow=0.4, glow=0.0, glint=None)
    # Rucellai: defter açılır, satırlar yazılır
    kb2 = ease_out(cx.amt(("c4s22", "defterine", -0.4), 0.8), 3)
    if kb2 > 0.003:
        icons.draw_icon(f, "book_open", 960, 250 + 8 * math.sin(t * 1.6), size=190 * (0.8 + 0.2 * kb2), metal="gold", alpha=kb2, shadow=True)
        icons.draw_icon(f, "quill", 1090, 230 + 6 * math.sin(t * 2.0), size=120 * (0.8 + 0.2 * kb2), metal="gold", alpha=kb2, shadow=True)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "GIOVANNI RUCELLAI", 960, 120, at=("c4s22", "Giovanni", -0.1), size=36, w=620)
    L.tag(f, cx, "ZİBALDONE", 1220, 240, at=("c4s22", "defterine", -0.1), size=34, w=360)


@CM.ckind("c4_saraylar")
def k_saraylar(cx, **kw):
    k_saraylar_impl(cx, **kw)


# ═══════════════════════════ c4s22b: elli yıl hep kazanıp harcamış; harcamayı kazanmaktan daha tatlı bulmuş ═══════════════════════════
def draw_honey_jar(c, x, y, s=1.0, a=255, drip=0.0, glow=0.0, t=0.0):
    SOFT(c, x, y - 60 * s, 160 * s, 150 * s, "#FFD060", 90 * glow)
    p = skia.Path()
    p.moveTo(x - 70 * s, y - 20 * s)
    p.cubicTo(x - 100 * s, y - 100 * s, x - 90 * s, y - 150 * s, x - 56 * s, y - 160 * s)
    p.lineTo(x + 56 * s, y - 160 * s)
    p.cubicTo(x + 90 * s, y - 150 * s, x + 100 * s, y - 100 * s, x + 70 * s, y - 20 * s)
    p.cubicTo(x + 60 * s, y + 4 * s, x - 60 * s, y + 4 * s, x - 70 * s, y - 20 * s)
    p.close()
    c.drawPath(p, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((x - 30 * s, y - 100 * s), 130 * s, [C("#FFE590", a), C("#E0A030", a), C("#8A5A18", a)], [0.0, 0.5, 1.0])))
    INKP(c, p, 2.0, a)
    R(c, x - 62 * s, y - 182 * s, x + 62 * s, y - 158 * s, "#6A4426", a)
    INKR(c, x - 62 * s, y - 182 * s, x + 62 * s, y - 158 * s, 1.6, 220)
    if drip > 0.01:
        dl = 70 * s * drip
        dp = skia.Path()
        dp.moveTo(x + 24 * s, y - 158 * s)
        dp.lineTo(x + 24 * s, y - 158 * s + dl)
        c.drawPath(dp, S("#E0A030", 12 * s, a))
        c.drawCircle(x + 24 * s, y - 158 * s + dl, 9 * s, P("#E0A030", a))


def k_kazan_harca_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=20, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    # sol: kazanmak — kasa dolar
    kk = cx.amt(("c4s22", "kazanıp", -0.5), 0.6)
    n_in = clamp((t - cx.at(("c4s22", "hep", -0.1))) / 1.7)
    if kk > 0.003:
        icons.draw_icon(f, "chest", 500, FY - 150, size=330 * (0.8 + 0.2 * ease_out(kk)), metal="bronze", alpha=kk, shadow=True)
        L.coin_stack(c, 500, FY - 12, int(14 * n_in * kk), r=70, gap=9.0, a=int(255 * kk)) if False else None
        for i in range(8):
            ph = (t * 0.8 + i * 0.125) % 1.0
            if n_in > 0.02:
                L.draw_coin_flat(c, 500 + 30 * math.sin(i * 2.0), lerp(120, FY - 280, ph), r=24, a=int(255 * n_in * (1 - clamp((ph - 0.85) * 6.0))))
    # sağ: harcamak — bal kavanozu (tatlı): kese açılır, florinler dışarı
    t_h = cx.at(("c4s22", "harcamış,", -0.3))
    kh = ease_out(clamp((t - t_h) / 0.8), 3)
    ks = cx.amt(("c4s22", "tatlı", -0.3), 0.8)
    if kh > 0.003:
        L.draw_bag(c, 1180, 560 + (1 - kh) * 100, s=1.3 * kh, seed=6, sway=2.0 * math.sin(t * 2.0), slips=0)
        for i in range(8):
            ph = ((t - t_h) * 0.7 + i * 0.125) % 1.0
            L.draw_coin_flat(c, 1180 + 60 * math.sin(i * 1.7) + 120 * ph, 560 + 360 * ph * ph, r=22, a=int(255 * kh * (1 - clamp((ph - 0.8) * 5))))
        draw_honey_jar(c, 1560, FY - 6, s=1.6 * (0.7 + 0.3 * ks), a=int(255 * ks), drip=ks, glow=ks, t=t)
    # elli yıl tutanağı (beşli demetler)
    t_y = cx.at(("c4s22", "elli", -0.1))
    ky = clamp((t - t_y) / 1.4)
    if ky > 0.003:
        n = int(50 * ky)
        for g in range(10):
            gx = 520 + g * 90
            for j in range(5):
                idx = g * 5 + j
                if idx >= n:
                    break
                if j < 4:
                    c.drawLine(gx + j * 12, 240, gx + j * 12, 296, S("#8E2A1E", 4.0, 235))
                else:
                    c.drawLine(gx - 6, 288, gx + 52, 246, S("#8E2A1E", 4.0, 235))
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "50 YIL", 960, 140, at=("c4s22", "elli", -0.1), size=64, w=380, track=12)
    L.tag(f, cx, "KAZANMAK", 330, 520, at=("c4s22", "kazanıp", -0.3), size=34, w=340)
    L.tag(f, cx, "HARCAMAK", 1560, 470, at=("c4s22", "harcamış,", -0.3), size=34, w=340)


@CM.ckind("c4_kazan_harca")
def k_kazan_harca(cx, **kw):
    k_kazan_harca_impl(cx, **kw)


# ═══════════════════════════ c4s23: Palla Strozzi'nin «Üç Kral'ın Tapınışı» tablosu — maiyette bir şahinci (strozziere) ═══════════════════════════
def k_uckral_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=21, dress=None)
    t = cx.t
    # altın çerçeveli sunak panosu (sivri kemerli), yeniden çizim
    fx0, fx1, fy0, fy1 = 360.0, 1560.0, 230.0, 850.0
    kf = ease_out(cx.amt(("c4s23", -0.1), 0.8), 3)
    c.save()
    c.translate(0, (1 - kf) * 60)
    pth = skia.Path()
    pth.moveTo(fx0, fy1)
    pth.lineTo(fx0, fy0 + 90)
    pth.cubicTo(fx0, fy0 + 20, fx0 + 160, fy0 - 10, 960, fy0 - 70)
    pth.cubicTo(fx1 - 160, fy0 - 10, fx1, fy0 + 20, fx1, fy0 + 90)
    pth.lineTo(fx1, fy1)
    pth.close()
    SOFT(c, 960, fy1 + 10, 700, 40, "#000000", 100)
    c.drawPath(pth, P("#C79A3C"))
    c.save()
    c.clipPath(pth, skia.ClipOp.kIntersect, True)
    # iç: gök yaldızı + tepe + yol
    GRAD_V(c, fx0, fy0 - 80, fx1, fy1, [("#E8C25A", 0.0), ("#F2D88A", 0.45), ("#7FA878", 0.46), ("#4F7A58", 1.0)])
    for q in range(40):
        c.drawCircle(fx0 + 40 + (q * 97) % (fx1 - fx0 - 80), fy0 + 20 + (q * 53) % 300, 3.0, P("#FFF0B0", 160))
    # yıldız (üstte)
    sx_, sy_ = 960, fy0 + 40
    for i in range(8):
        a_ = i * 0.7854
        c.drawLine(sx_, sy_, sx_ + math.cos(a_) * (46 if i % 2 == 0 else 28), sy_ + math.sin(a_) * (46 if i % 2 == 0 else 28), S("#FFFFFF", 5.0, 230))
    c.drawCircle(sx_, sy_, 12, P("#FFFFFF"))
    # maiyet: renkli, ufak figürler yavaşça yürür (resmin içinde)
    GYp = fy1 - 60
    cast = (("tuccar", 21, 0), ("soylu", 22, 1), ("halk", 23, 2), ("banker", 24, 3), ("soylu_f", 25, 4), ("asker", 26, 5), ("tuccar", 27, 6), ("halk", 28, 7), ("soylu", 29, 8))
    for (kd, sd, j) in cast:
        xx = (fx1 + 100) - ((t * 22.0 + j * 150.0) % (fx1 - fx0 + 300))
        L.walker(f, kd, xx, GYp + 10 * (j % 3), 230 + 6 * (j % 3), t, speed=22.0, dir=-1, seed=sd, phase=j * 0.37)
    c.restore()
    c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=26, Color=C("#B8862E")))
    c.drawPath(pth, S("#4A3410", 3.0, 230))
    c.restore()
    # şahinci vurgusu: halka + şahin simgesi (zoom anıyla)
    ksh = cx.amt(("c4s23", "şahinci", -0.3), 0.6)
    fx_, fy_ = 1180.0, GYp - 120
    if ksh > 0.003:
        c.drawCircle(fx_, fy_, 120 + 8 * math.sin(t * 3), S("#8E2A1E", 6.0, int(240 * ksh)))
        icons.draw_icon(f, "eagle", fx_ - 40, fy_ - 160, size=110 * (0.8 + 0.2 * ease_out(ksh)), metal="bronze", alpha=ksh, shadow=True)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "PALLA STROZZI", 960, 130, at=("c4s23", "Strozzi,", -0.2), size=38, w=520, hold=("c4s23", "soyadını", 0.0))
    L.tag(f, cx, "ÜÇ KRAL'IN TAPINIŞI", 960, 130, at=("c4s23", "Tapınışı”", -0.7), size=36, sub="GENTILE DA FABRIANO · 1423 · YENİDEN ÇİZİM", w=700, hold=("c4s23", "soyadını", 0.0))
    # strozziere = STROZZI + ERE
    k2 = cx.amt(("c4s23", "strozziere,", -0.2), 0.6)
    if k2 > 0.003:
        sp1 = CM.gilt("STROZZI", "title", 96, 10.0)
        sp2 = CM.engraved("ERE", "title", 96, 10.0, TH.fg)
        wA = sk.text_width("STROZZI", "title", 96, 10.0)
        wB = sk.text_width("ERE", "title", 96, 10.0)
        x0 = 960 - (wA + wB) / 2
        CM.draw_spr(f, sp1, x0, 850, "l", alpha=k2, shadow=0.4)
        CM.draw_spr(f, sp2, x0 + wA, 850, "l", alpha=k2, shadow=0.0)
    L.tag(f, cx, "ŞAHİNCİ", 1500, 330, at=("c4s23", "şahinci", -0.2), size=40, w=360) if False else None
    k3 = cx.amt(("c4s23", "demek.", -0.9), 0.6)
    if k3 > 0.003:
        L.tag(f, cx, "= ŞAHİNCİ", 1560, 420, at=("c4s23", "demek.", -0.9), size=48, w=440)


@CM.ckind("c4_uckral")
def k_uckral(cx, **kw):
    k_uckral_impl(cx, **kw)


# ═══════════════════════════ c4s24: Strozzi'ler 1489'da Medici sarayını aşacak bir saraya başladı; temel gününü astrolog seçti ═══════════════════════════
def draw_star_disc(c, x, y, r, rot=0.0, k=1.0, a=255):
    """Gök diski (astrolab benzeri): iç içe halkalar, takımyıldız noktaları, dönen kol."""
    c.drawCircle(x, y, r, P("#E8DDBE", a))
    c.drawCircle(x, y, r, S("#2A1A0C", 3.0, a))
    c.drawCircle(x, y, r * 0.72, S("#8A6A3A", 2.0, int(a * 0.8)))
    c.drawCircle(x, y, r * 0.38, S("#8A6A3A", 2.0, int(a * 0.8)))
    rs = _RS(7)
    for i in range(28):
        ang = rs.uniform(0, 6.283) + rot * 0.2
        rad = rs.uniform(0.15, 0.95) * r
        c.drawCircle(x + math.cos(ang) * rad, y + math.sin(ang) * rad, 3.2, P("#2A1A0C", a))
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(rot))
    c.drawLine(-r, 0, r, 0, S("#8E2A1E", 4.0, a))
    c.drawCircle(r * 0.62, 0, 10, S("#C79A3C", 4.0, a))
    c.restore()


def k_strozzi_saray_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=22, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    # sol: Medici sarayı (küçük)
    km = ease_out(cx.amt(("c4s24", "Medici", -0.2), 0.8), 2.4)
    draw_palazzo(c, 380, FY, 400, 400, style="medici", build=km, dim=0.0)
    # sağ: Strozzi sarayı — önce taslak (hayalet), Medici'yi aşar; 'başladı'da yalnız temel atılır
    kg = ease_out(cx.amt(("c4s24", "Strozzi'ler", 0.2), 1.0), 2.4)
    _gp = skia.Paint()
    _gp.setAlphaf(0.26)
    c.saveLayer(None, _gp)
    draw_palazzo(c, 1480, FY, 560, 640, style="strozzi", build=kg, dim=0.3)
    c.restore()
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(1180, FY - 640 * kg - 40, 1780, FY + 4))
    c.drawRect(skia.Rect.MakeLTRB(1200, FY - 640, 1760, FY), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.0, Color=C("#8A7A58", 220)))
    for i in range(1, 6):
        dashed(c, 1200, FY - 640 + i * 106, 1760, FY - 640 + i * 106, col="#8A7A58", w=1.6, a=130, dash=(10.0, 10.0))
    c.restore()
    kb = ease_out(clamp((t - cx.at(("c4s24", "başladı;", -0.2))) / 1.0), 2.0)
    draw_palazzo(c, 1480, FY, 560, 640, style="strozzi", build=0.12 * kb)
    # seviye çizgisi: Medici'nin yüksekliği → Strozzi taslağı aşar
    kl = cx.amt(("c4s24", "aşacak", -0.4), 0.5)
    if kl > 0.003:
        dashed(c, 280, FY - 400, 1800, FY - 400, col="#8E2A1E", w=3.0, a=int(220 * kl), dash=(14.0, 10.0), phase=-t * 30)
    # temel taşı: 'başladı'da iner
    ks = ease_in(clamp((t - cx.at(("c4s24", "başladı;", -0.5))) / 0.5), 2)
    if ks > 0.003:
        R(c, 1380, FY - 70 - (1 - ks) * 300, 1580, FY - 34 - (1 - ks) * 300, "#9A9484")
        INKR(c, 1380, FY - 70 - (1 - ks) * 300, 1580, FY - 34 - (1 - ks) * 300, 2.0, 230)
    # astrolog (orta): gök diski; 'seçti'de halka belirir
    ka = ease_out(cx.amt(("c4s24", "astrolog", -0.9), 0.8), 2)
    if ka > 0.003:
        L.sil(f, "kesis", 900, FY + 4, 400, t, action="point", dir=1, seed=51, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=ka, t0=cx.at(("c4s24", "astrolog", -0.5)))
        draw_star_disc(c, 960, 300, 150 * (0.7 + 0.3 * ka), rot=t * 0.35, a=int(255 * ka))
        kc = cx.amt(("c4s24", "seçti.", -0.4), 0.6)
        if kc > 0.003:
            c.drawCircle(960, 300, 170 + 10 * math.sin(t * 4), S("#C79A3C", 7.0, int(240 * kc)))
            SOFT(c, 960, 300, 200, 200, "#FFE9A0", 110 * kc)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "STROZZI", 1480, 130, at=("c4s24", "Strozzi'ler", -0.1), size=38, w=340)
    L.tag(f, cx, "MEDICI SARAYI", 380, 330, at=("c4s24", "Medici", -0.2), size=30, w=380)
    L.engr(f, cx, "1489", 960, 160, ("c4s24", "1489'da", -0.1), size=88, track=16, dur=0.9, glow=0.15)


@CM.ckind("c4_strozzi_saray")
def k_strozzi_saray(cx, **kw):
    k_strozzi_saray_impl(cx, **kw)


# ═══════════════════════════ c4s25: Pazzi ailesi de Brunelleschi'ye atfedilen bir şapel ısmarlamıştı; 1478 adı ═══════════════════════════
def draw_chapel(c, x, yb, s=1.0, a=255):
    """Pazzi Şapeli tipi: altı ince sütunlu revak + ortada kemerli giriş + mermer çatı + küçük kubbe/fener (yeniden çizim)."""
    w, h = 640 * s, 230 * s
    R(c, x - w / 2, yb - h, x + w / 2, yb, "#EDE5D0", a)
    INKR(c, x - w / 2, yb - h, x + w / 2, yb, 2.2, 230)
    # kubbe (arkada)
    dcx, dcy = x, yb - h - 20 * s
    dp = skia.Path()
    dp.moveTo(dcx - 130 * s, dcy)
    dp.cubicTo(dcx - 130 * s, dcy - 150 * s, dcx + 130 * s, dcy - 150 * s, dcx + 130 * s, dcy)
    dp.close()
    c.drawPath(dp, P("#C65B33", a))
    INKP(c, dp, 2.0, 220)
    for i in range(1, 6):
        c.drawLine(dcx - 130 * s + i * 43 * s, dcy, dcx + (i - 3) * 8 * s, dcy - 128 * s, S("#5A2412", 1.2, 110))
    R(c, dcx - 18 * s, dcy - 190 * s, dcx + 18 * s, dcy - 128 * s, "#EDE5D0", a)
    INKR(c, dcx - 18 * s, dcy - 190 * s, dcx + 18 * s, dcy - 128 * s, 1.6, 220)
    # saçak + attik
    R(c, x - w / 2 - 10 * s, yb - h - 20 * s, x + w / 2 + 10 * s, yb - h + 8 * s, "#B8AE94", a)
    INKR(c, x - w / 2 - 10 * s, yb - h - 20 * s, x + w / 2 + 10 * s, yb - h + 8 * s, 1.8, 220)
    # sütunlar
    for i in range(7):
        cxm = x - w / 2 + 40 * s + i * (w - 80 * s) / 6
        R(c, cxm - 9 * s, yb - h + 12 * s, cxm + 9 * s, yb, "#C9C0A6", a)
        INKR(c, cxm - 9 * s, yb - h + 12 * s, cxm + 9 * s, yb, 1.2, 190)
    # kemerli giriş
    ap = skia.Path()
    ap.moveTo(x - 70 * s, yb)
    ap.lineTo(x - 70 * s, yb - 110 * s)
    ap.cubicTo(x - 70 * s, yb - 190 * s, x + 70 * s, yb - 190 * s, x + 70 * s, yb - 110 * s)
    ap.lineTo(x + 70 * s, yb)
    ap.close()
    c.drawPath(ap, P("#2A1C10", 240))
    INKP(c, ap, 2.2, 230)


def k_pazzi_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=23, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    kc = ease_out(cx.amt(("c4s25", "Pazzi", -0.4), 0.9), 2.4)
    c.save()
    c.translate(0, (1 - kc) * 120)
    draw_chapel(c, 1000, FY, s=1.45, a=int(255 * kc))
    c.restore()
    # Medici işareti (sol altta küçük): rakip
    km = cx.amt(("c4s25", "Medici'nin", -0.1), 0.6)
    if km > 0.003:
        import cilt_props as CP
        CP.draw_arms(f, 250, 640, 130, alpha=km, shadow=0.4, glow=0.0, glint=None)
    # PAZZI levhası: kapının üstünde; 1478 koyu mürekkep sızar
    kp = cx.amt(("c4s25", "Pazzi", -0.1), 0.6)
    if kp > 0.003:
        CM.tablet(f, 840, 300, 320, 78, alpha=kp, corner=8)
        CM.ink(f, "PAZZI", 1000, 350, face="title", size=46, color=TH.fg, align="c", track=10, alpha=kp, emboss=False)
    kd = ease_in(clamp((t - cx.at(("c4s25", "1478'de", -0.3))) / 1.2), 1.6)
    if kd > 0.003:
        # gölge: sağ üstten çöken koyu leke (şiddet yok)
        sh = skia.GradientShader.MakeRadial((1960, -40), 1900 * kd, [C("#1A0E08", int(150 * kd)), C("#1A0E08", 0)], [0.0, 1.0])
        c.drawRect(skia.Rect.MakeLTRB(0, 0, 1920, 1080), skia.Paint(Shader=sh))
        sp = CM.engraved("1478", "title", 130, 14.0, "#1A0E08")
        CM.draw_spr(f, sp, 1000, 200, "c", alpha=smooth(kd * 3), shadow=0.0)
    # onlar bilmiyordu: üç siluet şapele bakar (rahat)
    kb = ease_out(cx.amt(("c4s25", "onlar", -0.3), 0.8), 2)
    for j, (kd_, sd, xx) in enumerate((("soylu", 61, 560), ("soylu_f", 62, 660), ("banker", 63, 1430))):
        if kb > 0.003:
            L.sil(f, kd_, xx, FY + 8 + 8 * j, 330, t, action="talk" if j != 2 else "idle", dir=1 if xx < 1000 else -1, seed=sd, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kb, energy=0.7)
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "PAZZI ŞAPELİ", 1000, 130, at=("c4s25", "şapeli", -0.2), size=38, w=520, hold=("c4s25", "1478'de", -0.1))
    L.tag(f, cx, "ATFEDİLEN: BRUNELLESCHI", 1500, 380, at=("c4s25", "atfedilen", -0.2), size=30, w=560, hold=("c4s25", "1478'de", -0.1))


@CM.ckind("c4_pazzi")
def k_pazzi(cx, **kw):
    k_pazzi_impl(cx, **kw)


# ═══════════════════════════ c4s26–27: Fra Filippo Lippi odaya kilitlenir; çarşaflarla pencereden iner; serbestlik (Vasari'ye göre, gravür) ═══════════════════════════
def draw_scissors(c, x, y, s=1.0, open_=0.5, rot=0.0, a=255):
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(rot))
    c.scale(s, s)
    ang = 0.12 + 0.30 * open_
    for sg in (-1, 1):
        c.save()
        c.rotate(math.degrees(sg * ang))
        c.drawLine(0, 0, 70, 0, S("#9A9484", 8.0, a))
        c.drawLine(0, 0, 70, 0, S("#2A2620", 1.4, a))
        c.restore()
    for sg in (-1, 1):
        c.save()
        c.rotate(math.degrees(-sg * ang * 0.6))
        c.drawCircle(-30, sg * 14, 13, S("#6A4426", 6.0, a))
        c.restore()
    c.drawCircle(0, 0, 5, P("#2A2620", a))
    c.restore()


def k_lippi_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=24, dress=None, mono=1.0)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    # oda (kesit): sol duvar kapı, sağ duvar pencere; dışarısı sağda
    RX0, RX1, RY0 = 300.0, 1080.0, 250.0
    R(c, RX0, RY0, RX1, FY, "#EDE3C8")
    INKR(c, RX0, RY0, RX1, FY, 3.0, 235)
    R(c, RX0 - 24, RY0 - 26, RX1 + 24, RY0, "#B9A27C")
    INKR(c, RX0 - 24, RY0 - 26, RX1 + 24, RY0, 2.0, 220)
    # pencere (sağ duvarda, açık)
    R(c, RX1 - 46, 360, RX1, 600, "#9CBBDC")
    INKR(c, RX1 - 46, 360, RX1, 600, 3.0, 240)
    c.drawLine(RX1 - 23, 360, RX1 - 23, 600, S("#2A1A0C", 2.0, 200))
    R(c, RX1 - 54, 600, RX1 + 56, 624, "#9A8A68")
    INKR(c, RX1 - 54, 600, RX1 + 56, 624, 2.2, 230)
    # kapı (sol duvar): kilitli → açık
    t_lock = cx.at(("c4s26", "kilitlemiş.", -0.5))
    t_open = cx.at(("c4s27", "serbestlik", -0.3))
    kopen = ease_out(clamp((t - t_open) / 0.9), 2)
    R(c, RX0 - 4, 560, RX0 + 14, FY, "#5A3C22")
    INKR(c, RX0 - 4, 560, RX0 + 14, FY, 2.0, 230)
    if kopen > 0.003:
        c.save()
        c.translate(RX0 - 4, 0)
        c.scale(1.0 + 3.0 * kopen, 1.0)
        R(c, 0, 560, 14, FY, "#8A5A38")
        c.restore()
    # şövale + tuval + palet
    R(c, 480, 470, 600, 700, "#E6DCBE")
    INKR(c, 480, 470, 600, 700, 2.4, 230)
    c.drawLine(470, 700, 430, FY, S("#5A3C22", 8.0, 235))
    c.drawLine(610, 700, 650, FY, S("#5A3C22", 8.0, 235))
    c.drawLine(540, 470, 540, 440, S("#5A3C22", 8.0, 235))
    for i, col in enumerate(("#A8321E", "#233C8C", "#C79A3C")):
        c.drawCircle(500 + 40 * i, 560 + 30 * math.sin(i), 16 + 6 * (i % 2), P(col, 230))
    # yatak (çarşaflar)
    ksh = cx.amt(("c4s27", "çarşafları", -0.3), 0.5)
    kcut = clamp((t - cx.at(("c4s27", "kesip", -0.1))) / 0.8)
    R(c, 760, 740, 1040, 800, "#8A5A38")
    INKR(c, 760, 740, 1040, 800, 2.0, 230)
    R(c, 764, 700, 1036, 748, "#F6F0DC")
    INKR(c, 764, 700, 1036, 748, 2.0, 230)
    for i in range(5):
        c.drawLine(790 + i * 55, 704, 790 + i * 55, 746, S("#2A1A0C", 1.0, 70))
    # makas: çarşafı keser
    if ksh > 0.003 and kcut < 1.0:
        draw_scissors(c, 900 + 90 * kcut, 690 - 10 * math.sin(t * 22), s=1.3, open_=0.5 + 0.5 * math.sin(t * 24), rot=-0.2, a=int(255 * ksh))
    # ip: pencere eşiğinden yere (ip yapmış), uzar
    kr = ease_out(clamp((t - cx.at(("c4s27", "ip", -0.2))) / 0.9), 2)
    if kr > 0.003:
        x0, y0 = RX1 + 6, 610
        yy = lerp(y0, FY - 8, kr)
        c.drawLine(x0, y0, x0 + 80 * kr, yy, S("#2A1A0C", 14.0, 200))
        c.drawLine(x0, y0, x0 + 80 * kr, yy, S("#F4EAD2", 10.0, 250))
        for q in range(1, 9):
            fq = q / 9.0
            if fq <= kr:
                c.drawCircle(x0 + 80 * fq * kr / max(kr, 1e-3) * (kr), lerp(y0, yy, fq), 6, P("#F4EAD2", 240)) if False else c.drawCircle(lerp(x0, x0 + 80 * kr, fq), lerp(y0, yy, fq), 6, P("#F4EAD2", 240))
    # Lippi (rahip siluet): odada çalışır → pencereden iner → özgürce yürür
    t_win = cx.at(("c4s27", "pencereden", -0.2))
    t_down = cx.at(("c4s27", "inmiş;", -0.2))
    if t < t_win:
        L.sil(f, "kesis", 560, FY + 4, 380, t, action="work", dir=1, seed=33, color="#14100C", rim="#FFE2A0", rim_dir=1)
    else:
        ud = clamp((t - t_win) / max(0.5, t_down - t_win + 0.4))
        px_ = lerp(RX1 - 60, RX1 + 60, ease_io(ud, 1.5))
        py_ = lerp(FY - 180, FY - 0, ease_io(ud, 1.5))
        if ud < 0.98:
            L.sil(f, "kesis", px_, py_ + 0, 300, t, action="idle", dir=-1, seed=33, color="#14100C", rim="#FFE2A0", rim_dir=-1)
        else:
            kw = clamp((t - cx.at(("c4s27", "pişman", 0.0))) / 1.2)
            L.sil(f, "kesis", lerp(RX1 + 60, RX0 - 120 - 0, ease_io(kw, 1.3)) if t > t_open else RX1 + 60, FY + 4, 340, t, dir=-1, seed=33, color="#14100C", rim="#FFE2A0", rim_dir=-1, walker=96.0 if (t > t_open and kw < 0.99) else 0.0)
    # Cosimo (soldaki, dışarıda): anahtarı çevirir; pişman olur
    L.sil(f, "soylu", 160, FY + 4, 380, t, action="talk" if (cx.at(("c4s27", "pişman", -0.1)) <= t < t_open) else "idle", dir=1, seed=4, color="#14100C", rim="#FFE2A0", rim_dir=1, energy=0.6)
    kkey = cx.amt(("c4s26", "kilitlemiş.", -0.5), 0.4)
    if kkey > 0.003 and t < t_open:
        draw_key(c, RX0 - 56, 640, s=0.8 * kkey, rot=0.0 + 0.8 * clamp((t - t_lock) / 0.4))
    L.end(cx, cam, mono=1.0, motes_n=14, light=(1000.0, 560.0, 1500.0, 0.9))
    L.tag(f, cx, "VASARI", 1500, 110, at=("c4s26", "Vasari'ye", -0.1), size=36, w=300)
    L.stamp_at(f, cx, "ANEKDOT", 1500, 200, at=("c4s26", "göre", 0.0), size=48, rot=-0.07)
    L.tag(f, cx, "FRA FILIPPO LIPPI", 960, 130, at=("c4s26", "Lippi'yi", -0.3), size=36, w=560, hold=("c4s27", "çarşafları", -0.3))


@CM.ckind("c4_lippi")
def k_lippi(cx, **kw):
    k_lippi_impl(cx, **kw)


# ═══════════════════════════ c4s29: Ricordi'ye göre toplam Lorenzo'ya akıl almaz göründü; başka harcamalar bunun dışındaydı ═══════════════════════════
def k_akil_almaz_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=25, dress=None)
    t = cx.t
    FY = 880.0
    L.grid_floor(c, -400, 2400, FY, 1300)
    # dev toplam: duvarda, 'altı yüz …' ile sayar
    t_a = cx.at(("c4s28", "altı", -0.1))
    t_b = cx.at(("c4s28", "fazla", 0.1))
    kcount = ease_out(clamp((t - t_a) / max(0.5, t_b - t_a)), 2.2)
    kn = clamp((t - (t_a - 0.1)) / 0.4)
    k_shock = cx.amt(("c4s29", "akıl", -0.1), 0.5)
    pulse = 1.0 + 0.10 * k_shock * (0.6 + 0.4 * math.sin(t * 9.0))
    shake = 5.0 * k_shock * math.sin(t * 31.0) if k_shock < 0.99 else 0.0
    txt = CM.fmt_int(663755 * kcount)
    sp = CM.engraved(txt, "title", int(190 * pulse), 12.0, TH.fg)
    CM.draw_spr(f, sp, 1000 + shake, 360, "c", alpha=smooth(kn * 3), shadow=0.0)
    CM.ink(f, "FLORİN", 1000, 470, face="title_m", size=44, color=TH.fg2, align="c", track=10, alpha=smooth(kn * 3), emboss=False)
    # Lorenzo (siluet): sayıdan geri çekilir
    kl = cx.amt(("c4s29", -0.15), 0.7)
    kb = cx.amt(("c4s29", "akıl", -0.1), 0.8)
    lx = lerp(520.0, 380.0, ease_out(kb, 2))
    if kl > 0.003:
        L.sil(f, "soylu", lx, FY + 6, 400, t, action="idle", dir=1, seed=4, color="#14100C", rim="#FFE2A0", rim_dir=1, alpha=kl)
    kq = cx.amt(("c4s29", "almaz", -0.1), 0.5)
    if kq > 0.003:
        for q in range(3):
            icons.draw_icon(f, "question", lx - 10 + q * 60, 330 - 40 * q + 8 * math.sin(t * 3.0 + q), size=90 * (0.8 + 0.2 * ease_out(kq)), metal="gold", alpha=kq, shadow=True)
    # toplamın dışı: kesikli kutu + dışına taşan kâğıtlar/florinler
    kd = cx.amt(("c4s29", "başka", -0.2), 0.6)
    if kd > 0.003:
        pp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5.0, Color=C("#8E2A1E", int(235 * kd)), StrokeCap=skia.Paint.kRound_Cap)
        pp.setPathEffect(skia.DashPathEffect.Make([18.0, 12.0], -t * 40))
        c.drawRect(skia.Rect.MakeLTRB(560, 220, 1440, 540), pp)
        t_o = cx.at(("c4s29", "harcamalar", -0.2))
        for i in range(10):
            ph = ((t - t_o) * 0.55 + i * 0.1) % 1.0
            if t < t_o:
                continue
            x = 1440 + 90 * ph + 40 * (i % 3)
            y = 380 + 40 * math.sin(i * 1.7) + 380 * ph * ph
            if i % 2:
                L.draw_slip(c, x, y, w=76, h=52, rot=3.0 * ph + i, lines=1, seed=i, a=int(255 * (1 - ph * 0.6)))
            else:
                L.draw_coin_flat(c, x, y, r=24, a=int(255 * (1 - ph * 0.6)))
    L.end(cx, cam, motes_n=14)
    L.tag(f, cx, "RICORDI", 480, 150, at=("c4s29", "Ricordi'ye", -0.1), size=38, sub="LORENZO", w=380, hold=("c4s29", "başka", 0.0))
    L.tag(f, cx, "TOPLAMIN DIŞINDA", 1500, 640, at=("c4s29", "dışındaydı.", -0.8), size=34, w=520)


@CM.ckind("c4_akil_almaz")
def k_akil_almaz(cx, **kw):
    k_akil_almaz_impl(cx, **kw)


# ═══════════════════════════ c4s30–31: kefaret mi yatırım mı? — terazi; kaynaklarda üç iz: vicdan, onur, ölümden sonra için bir yer ═══════════════════════════
def draw_balance(f, x, y, tilt, s=1.0, a=255, lab_l=None, lab_r=None, hl_l=0.0, hl_r=0.0, t=0.0):
    """Terazi: gövde + dönen kol + iki kefe (zincirle asılı, yatay kalır). tilt radyan (+: sağ kefe aşağı)."""
    c = f.c
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    # ayak
    p = skia.Path()
    p.moveTo(-90, 420)
    p.lineTo(90, 420)
    p.lineTo(18, 60)
    p.lineTo(-18, 60)
    p.close()
    c.drawPath(p, P("#6E4524", a))
    INKP(c, p, 2.4, a)
    c.drawCircle(0, 40, 30, P("#C79A3C", a))
    c.drawCircle(0, 40, 30, S("#4A3410", 2.4, a))
    # kol
    c.save()
    c.translate(0, 40)
    c.rotate(math.degrees(tilt))
    c.drawRect(skia.Rect.MakeLTRB(-380, -10, 380, 10), P("#8A5A38", a))
    INKR(c, -380, -10, 380, 10, 2.0, a)
    c.restore()
    for sg, lab, hl in ((-1, lab_l, hl_l), (1, lab_r, hl_r)):
        ex = sg * 380 * math.cos(tilt)
        ey = 40 + sg * 380 * math.sin(tilt)
        c.drawLine(ex, ey, ex - 90, ey + 190, S("#4A3410", 3.0, a))
        c.drawLine(ex, ey, ex + 90, ey + 190, S("#4A3410", 3.0, a))
        pw = 200
        if hl > 0.01:
            SOFT(c, ex, ey + 215, pw * 0.8, 60, "#FFD060", 150 * hl)
        pan = skia.Path()
        pan.moveTo(ex - pw / 2, ey + 190)
        pan.cubicTo(ex - pw / 2, ey + 250, ex + pw / 2, ey + 250, ex + pw / 2, ey + 190)
        pan.close()
        c.drawPath(pan, P("#C79A3C", a))
        INKP(c, pan, 2.4, a)
        if lab:
            CM.tablet(f, ex - 150, ey + 270, 300, 66, alpha=a / 255.0, corner=8)
            CM.ink(f, lab, ex, ey + 316, face="title_m", size=34, color=TH.fg, align="c", track=6, alpha=a / 255.0, emboss=False)
    c.restore()


def draw_footprints(c, x0, y0, x1, y1, k, n=9, a=255):
    for i in range(n):
        if i / n > k:
            break
        fx = lerp(x0, x1, i / (n - 1.0))
        fy = lerp(y0, y1, i / (n - 1.0)) + (14 if i % 2 else -14)
        c.save()
        c.translate(fx, fy)
        c.rotate(math.degrees(math.atan2(y1 - y0, x1 - x0)))
        c.drawOval(skia.Rect.MakeLTRB(-16, -8, 14, 8), P("#5A3C22", int(a * 0.8)))
        c.drawOval(skia.Rect.MakeLTRB(12, -6, 24, 6), P("#5A3C22", int(a * 0.8)))
        c.restore()


def k_terazi_iz_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=26, dress=None)
    t = cx.t
    ks = ease_out(cx.amt(("c4s30", -0.1), 0.7), 3)
    t_k = cx.at(("c4s30", "kefaret", -0.1))
    t_y = cx.at(("c4s30", "yatırım", -0.1))
    t_m = cx.at(("c4s30", "mı?", -0.2))
    t_i = cx.at(("c4s31", "Kaynaklarda", -0.1))
    if t < t_k:
        tilt = 0.0
    elif t < t_y:
        tilt = -0.14 * ease_out(clamp((t - t_k) / 0.5), 2)
    elif t < t_m:
        tilt = lerp(-0.14, 0.14, ease_io(clamp((t - t_y) / 0.55), 1.5))
    else:
        tilt = 0.14 * math.cos(clamp(t - t_m, 0, 6) * 3.4) * math.exp(-0.5 * clamp(t - t_m, 0, 6))
    kmove = ease_io(clamp((t - t_i) / 1.0), 1.6)
    sc = lerp(1.0, 0.62, kmove)
    bx = lerp(960.0, 360.0, kmove)
    by = lerp(180.0, 330.0, kmove)
    draw_balance(f, bx, by, tilt, s=sc * ks, a=int(255 * ks), lab_l="KEFARET", lab_r="YATIRIM", hl_l=max(0.0, -tilt / 0.14), hl_r=max(0.0, tilt / 0.14), t=t)
    kq = cx.amt(("c4s30", "mı?", -0.3), 0.5) * (1.0 - kmove)
    if kq > 0.003:
        icons.draw_icon(f, "question", 960, 110 + 8 * math.sin(t * 3.0), size=150 * (0.8 + 0.2 * ease_out(kq)), metal="gold", alpha=kq, shadow=True)
    # üç iz: ayak izleri + levhalar
    plates = (("VİCDAN", "heart", 250.0, ("c4s31", "vicdan,", -0.1), ("c4s31", "üç", 0.0)),
              ("ONUR", "laurel", 500.0, ("c4s31", "onur,", -0.1), ("c4s31", "vicdan,", 0.2)),
              ("ÖLÜMDEN SONRA İÇİN BİR YER", "cross", 750.0, ("c4s31", "ölümden", -0.1), ("c4s31", "onur,", 0.2)))
    for (txt, ic, yy, an, at0) in plates:
        kt = clamp((cx.at(an) - cx.at(at0) + 0.6))
        kf = clamp((t - cx.at(at0)) / max(0.4, cx.at(an) - cx.at(at0) + 0.2))
        if kf > 0.0:
            draw_footprints(c, 640, 560 + (yy - 500) * 0.2, 1080, yy, kf, n=9, a=235)
        kp = ease_out(cx.amt(an, 0.6), 3)
        if kp > 0.003:
            CM.tablet(f, 1100 + (1 - kp) * 100, yy - 56, 760, 112, alpha=kp, corner=10)
            CM.ink(f, txt, 1100 + 330 + (1 - kp) * 100, yy + 14, face="title_m", size=40 if len(txt) < 12 else 32, color=TH.fg, align="c", track=6, alpha=kp, emboss=False)
            icons.draw_icon(f, ic, 1100 + 700 + (1 - kp) * 100, yy, size=84, metal="gold", alpha=kp, shadow=True)
    L.end(cx, cam, motes_n=14)
    L.stamp_at(f, cx, "YORUM", 300, 150, at=("c4s31", "Kaynaklarda", 0.0), size=44, rot=-0.07)


@CM.ckind("c4_terazi_iz")
def k_terazi_iz(cx, **kw):
    k_terazi_iz_impl(cx, **kw)


# ═══════════════════════════ c4s32–33: duvarlar dikilmişti; sıra duvarların içine konacak şeye geldi: kitaplara (kitap kulesi, dikey çıkış) ═══════════════════════════
def draw_book_block(c, x, y, w, h, col, a=255, tilt=0.0):
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(tilt))
    GRAD_V(c, -w / 2, -h, w / 2, 0, [(mix(col, "#FFFFFF", 0.25), 0.0), (col, 0.5), (mix(col, "#000000", 0.4), 1.0)])
    R(c, w / 2 - 14, -h, w / 2, 0, "#F4EAD2")
    for k in range(1, 3):
        c.drawLine(w / 2 - 14, -h + k * h / 3, w / 2, -h + k * h / 3, S("#8A7A58", 1.0, 160))
    R(c, -w / 2, -h * 0.82, -w / 2 + 10, -h * 0.18, "#E0B84E")
    INKR(c, -w / 2, -h, w / 2, 0, 1.6, 220)
    c.restore()


def k_kitap_kule_impl(cx, **_):
    f, c, cam = L.begin(cx, bg="wall", seed=27, dress=None)
    t = cx.t
    T = L.OD.OTint("day")
    FY = 880.0
    # dikey zemin: yukarı doğru gökyüzü
    sh = skia.GradientShader.MakeLinear([(0, -2400), (0, 600)], [C("#F6E7B8"), C("#C79A3C")], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(-600, -2600, 2600, 0), skia.Paint(Shader=sh))
    # kütüphane salonu: kemerli duvarlar, boş raflar, okuma sehpaları
    L.grid_floor(c, -400, 2400, FY, 1300, col1="#D6C9A6", col2="#B8A67C")
    kw_ = ease_out(clamp((t - cx.at(("c4s32", -0.1))) / 1.1), 2.2)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(-400, FY - (FY - 240) * kw_ - 10, 2400, FY))
    c.translate(0, (1 - kw_) * (FY - 240))
    wall = "#EDE3C8"
    R(c, -400, 0, 2400, FY, wall)
    for i in range(7):
        ax = 150 + i * 270
        p = skia.Path()
        p.moveTo(ax - 90, FY)
        p.lineTo(ax - 90, 420)
        p.cubicTo(ax - 90, 250, ax + 90, 250, ax + 90, 420)
        p.lineTo(ax + 90, FY)
        p.close()
        c.drawPath(p, P("#CFC4A2", 255))
        INKP(c, p, 2.4, 230)
        draw_shelf(c, ax - 70, 440, 140, 400, rows=4, seed=i + 3) if False else None
        # boş raf (tahta çubuklar)
        for r in range(4):
            c.drawLine(ax - 76, 470 + r * 100, ax + 76, 470 + r * 100, S("#6A4426", 6.0, 235))
        R(c, ax - 105, 430, ax - 90, FY, "#B8AE94")
        INKR(c, ax - 105, 430, ax - 90, FY, 1.4, 190)
    R(c, -400, 380, 2400, 420, "#B8AE94")
    INKR(c, -400, 380, 2400, 420, 2.0, 220)
    c.restore()
    # sehpalar
    for xx in (420, 960, 1500):
        R(c, xx - 80, FY - 180, xx + 80, FY - 150, "#6E4524")
        c.drawLine(xx - 60, FY - 150, xx - 80, FY, S("#5A3C22", 8.0, 235))
        c.drawLine(xx + 60, FY - 150, xx + 80, FY, S("#5A3C22", 8.0, 235))
        INKR(c, xx - 80, FY - 180, xx + 80, FY - 150, 1.6, 220)
    # kitap kulesi: 'kitaplara' ile yükselir
    t0 = cx.at(("c4s33", "Sıra,", -0.2))
    t1 = cx.at(("c4s33", "kitaplara.", 0.5))
    n = int(44 * ease_io(clamp((t - t0) / max(0.5, t1 - t0)), 1.4))
    cols = ["#8E2A1E", "#233C8C", "#3A7A52", "#C79A3C", "#6A4A8A", "#7A4A28", "#A8321E"]
    rs = _RS(9)
    ybk = FY - 180
    for i in range(n):
        wb = 200 + 60 * math.sin(i * 1.3) + (i % 3) * 14
        hb = 38 + (i % 4) * 4
        ybk -= hb
        draw_book_block(c, 960 + 18 * math.sin(i * 2.1), ybk + hb, wb, hb, cols[i % len(cols)], tilt=0.02 * math.sin(i * 1.9))
    if n > 0 and n < 44:
        # en üstteki uçan kitap
        ph = (t * 3.0) % 1.0
        draw_book_block(c, 960 - 400 + 400 * ph, ybk - 160 + 160 * ph * ph - 120 * math.sin(math.pi * ph), 190, 40, cols[n % len(cols)], tilt=0.2 * math.sin(ph * 6.0))
    # işaret: tepede açık kitap parlar
    kt = cx.amt(("c4s33", "kitaplara.", -0.2), 0.7)
    if kt > 0.003 and n > 0:
        SOFT(c, 960, ybk - 60, 260, 120, "#FFE9A0", 140 * kt)
        icons.draw_icon(f, "book_open", 960, ybk - 120, size=220 * (0.8 + 0.2 * kt), metal="gold", alpha=kt, shadow=True)
    L.end(cx, cam, motes_n=18)
    L.tag(f, cx, "KİTAP", 1560, 220, at=("c4s33", "kitaplara.", -0.3), size=52, w=320, track=14)


@CM.ckind("c4_kitap_kule")
def k_kitap_kule(cx, **kw):
    k_kitap_kule_impl(cx, **kw)
