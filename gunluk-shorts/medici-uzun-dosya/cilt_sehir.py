"""cilt_sehir — DIŞ MEKÂN / ŞEHİR DÜNYASI (Lab-E): `sehir` çekim türü.

`shot("sehir", a, scene=…, act=…, tod=…, cams=[(çapa,(x,y,zoom)),…], actors=[…], stations=[…], kick=…, caption=…, …)`; `cam/link/longtake/montage` kabul edilir
(kendi kamera yolu vardır: `cams=`; `cam=("push"|"pull"|"pan"|"crane", …)` verilirse `cams` yokken varsayılan yolun üstüne uygulanır).

Sahneler (hepsi `cilt_pano` motoruyla aynı kalıpta: ≥3 paralaks derinliği, 1024 px kareaş önbelleği `out/_cache/world/sehir_*`, dinamik katmanlar çekimde):
  scene="meydan"  Signoria Meydanı (Palazzo Vecchio kule+mazgal, Loggia, kalabalık). act="ates" (Kibirlerin Yakılması) | "odun" (aynı kamera/yığın merkezi, közer→kül, siluet) |
                  "palle" (atlılar sağdan sola durur, Medici kalabalığı soldan sağa kabarır, sancaklar, Medici penceresi altın) | "pencere" (cephe, alacakaranlık→gece, pencereler tek tek kararır, ip çizgisi+gölge)
  scene="sokak"   dar sokak + palazzo cephesi + ağır kapı (`door="close"|"open"`, `door_at=çapa`: kapı TEK HAMLEDE kapanır), yürüyen figürler, ters yönde akan siluetler, kemerli eşik
  scene="kale"    act="sur" (Floransa surları, San Miniato çan kulesi yün balyalarıyla sarılı, ufukta çadır dizisi) | "castel" (Castel Sant'Angelo + Passetto) | "passetto" (örtülü koridor yan görünüm, tek plan)
  scene="skyline_dikey"  Palazzo Vecchio kulesine tek dikey plan (`crane up`): gövde → mazgal → çan odası → flama; yanlarda çatılar, kuşlar
Yeniden kullanılabilir işlevler: `palazzo_front`, `door_heavy`, `bonfire`, `tent_row` (+ `smoke_plume`, `ember_field`, `pyre`, `item_sprite`, `light_pool`).
Kısıt: şiddet/ceset/kan/asılı beden yok (siluet, işaret, gölge); ışık/saat iddiası yalnız görsel dil; ağır katmanlar tembel pişirilir; SrcOver (kPlus yavaş).
"""
import functools
import math
import os
import time
import zlib

import cv2
import numpy as np
import skia

import cilt_anim as FA
import cilt_city as CT
import cilt_medici as CM
import cilt_pano as PN
import cilt_scene as SC
import sk
from cilt_medici import TH, ckind
from sk import C, H, W, clamp, mix, smooth

HERE = PN.HERE
CACHE = PN.CACHE
def _src_ver():
    """Önbellek sürümü = bu dosyanın içerik özeti: çizim kodu değişince eski kareaşlar otomatik geçersiz olur."""
    try:
        with open(__file__, "rb") as fh_:
            return "s" + format(zlib.crc32(fh_.read()) & 0xFFFFFF, "x")
    except Exception:   # noqa: BLE001
        return "s1"


VER = _src_ver()
OV = PN.OV
INK = PN.INK
LIN = PN.LIN
YG = 846                        # ana düzlem ayak hizası (katman y)
R, RA, INKP, INKR, LINE, POLY, OVAL, GRAD_V = PN.R, PN.RA, PN.INKP, PN.INKR, PN.LINE, PN.POLY, PN.OVAL, PN.GRAD_V
_RS = PN._RS
glow = PN.glow

try:                            # `sehir` kendi kamera yolunu kullanır (pano gibi): qa_flow/cam uygulaması çift hareket üretmesin
    import cilt_cam as _CC
    _CC.OWN_CAMERA.add("sehir")
except Exception:               # noqa: BLE001
    pass


def _cv(f):
    return getattr(f, "c", f)


def _pt(col, a=255, aa=True, style=None, sw=1.0):
    p = skia.Paint(AntiAlias=aa, Color=C(col, a))
    if style == "stroke":
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(sw)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


# ═════════════════════════════ katman + dünya tabanı ═════════════════════════════
class SLayer(PN.Layer):
    """pano.Layer ile aynı; yalnız önbellek dosya adı bu modülün sürümünü taşır."""

    def _path(self, i):
        return os.path.join(CACHE, f"{self.world}_{self.tod}_{self.name}_{i}_{VER}.png")


class SWorld(PN.World):
    interior = False

    def layer(self, name, f, width, draw, **kw):
        L = SLayer(self.name, name, f, width, draw, tod=self.tod, **kw)
        self.layers[name] = L
        return L

    def default_stations(self):
        return []

    def prepare(self, ctx):
        ctx.fire_k, ctx.fire_t0, ctx.coal, ctx.items, ctx.win_off, ctx.win_gold_t0 = 0.0, None, 0.0, [], None, None

    def grade(self, ctx):
        _grade_generic(self, ctx)

    def lights(self, ctx):
        return []

    def fx(self, ctx):
        pass


# ═════════════════════════════ mimari yardımcılar ═════════════════════════════
def arch_path(xc, yb, w, h):
    """Yuvarlak kemerli açıklık yolu: xc orta, yb taban, w genişlik, h toplam yükseklik."""
    r = w / 2.0
    p = skia.Path()
    p.moveTo(xc - r, yb)
    p.lineTo(xc - r, yb - h + r)
    p.arcTo(skia.Rect.MakeLTRB(xc - r, yb - h, xc + r, yb - h + 2 * r), 180, 180, False)
    p.lineTo(xc + r, yb)
    p.close()
    return p


def stone_wall(c, x0, y0, x1, y1, col, T, depth=0.0, seed=1, ch=30.0, bw=(64.0, 110.0), rustic=True, joint_a=105, clip=None):
    """Taş blok duvar (bugnato/kesme): sıra yüksekliği ch, blok genişliği bw; üstte açık, altta koyu kenar; tek yol ile derz çizgileri.
    clip=(xa,xb): yalnız bu aralıktaki blokları çiz (rastgele dizi aynı kalır → kareaşlar arası süreklilik; uzun cepheler için)."""
    rs = _RS(seed)
    base = T(col, depth)
    cx0, cx1 = (x0, x1) if clip is None else (max(x0, clip[0] - 4), min(x1, clip[1] + 4))
    if cx1 <= cx0:
        return
    R(c, cx0, y0, cx1, y1, base)
    n = max(1, int(round((y1 - y0) / ch)))
    chh = (y1 - y0) / n
    jp = skia.Path()
    for r_ in range(n):
        yy = y0 + r_ * chh
        x = x0 - rs.uniform(0, bw[1] * 0.9)
        while x < x1:
            w_ = rs.uniform(*bw)
            k = rs.uniform(-0.075, 0.075)
            xa, xb = max(x, cx0), min(x + w_, cx1)
            if xb - xa > 3 and x + w_ > cx0 and x < cx1:
                R(c, xa, yy, xb, yy + chh, mix(base, "#FFF4DC" if k > 0 else "#2A1A0C", abs(k)))
                if rustic:
                    R(c, xa + 1, yy + 1, xb - 1, yy + 1 + min(3.4, chh * 0.12), "#FFFFFF", 44)
                    R(c, xa + 1, yy + chh - min(3.6, chh * 0.13), xb - 1, yy + chh - 1, "#2A1A0C", 52)
                jp.moveTo(xb, yy)
                jp.lineTo(xb, yy + chh)
            x += w_
        jp.moveTo(cx0, yy)
        jp.lineTo(cx1, yy)
    c.drawPath(jp, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#4A3A22", joint_a)))


def bifora_paths(x, yb, w, h):
    return [arch_path(x + s * w * 0.215, yb - h * 0.03, w * 0.36, h * 0.78) for s in (-1, 1)]


def bifora(c, x, yb, w, h, T, depth=0.0, frame="#D8C79E"):
    """Çift kemerli ortaçağ penceresi: taş çerçeve + iki koyu iç kemer + orta sütunçe. Dönüş: (x, yb, w, h)."""
    outer = arch_path(x, yb, w, h)
    c.drawPath(outer, _pt(T(frame, depth)))
    INKP(c, outer, 1.3, 175)
    for ip in bifora_paths(x, yb, w, h):
        c.drawPath(ip, _pt(T("#2A1E14", depth * 0.3)))
        INKP(c, ip, 1.0, 150)
    R(c, x - w * 0.028, yb - h * 0.80, x + w * 0.028, yb - h * 0.03, T("#E8D9B4", depth))
    R(c, x - w * 0.07, yb - h * 0.82, x + w * 0.07, yb - h * 0.79, T("#CDBB92", depth))
    R(c, x - w * 0.52, yb - 2, x + w * 0.52, yb + 3, T("#C9B88E", depth))      # denizlik
    INKR(c, x - w * 0.52, yb - 2, x + w * 0.52, yb + 3, 1.0, 140)
    return (x, yb, w, h)


def lit_bifora(c, box, a, col="#FFC862", core="#FFE9A8"):
    """Pencere ışığı (dinamik örtü): bifora iç kemerlerini sıcak ışıkla doldurur. a: 0..1."""
    if a <= 0.01:
        return
    x, yb, w, h = box
    for ip in bifora_paths(x, yb, w, h):
        c.drawPath(ip, _pt(col, int(235 * a)))
    sh = skia.GradientShader.MakeRadial((x, yb - h * 0.45), h * 0.55, [C(core, int(150 * a)), C(core, 0)], [0.0, 1.0])
    c.save()
    c.clipPath(skia.Path.Rect(skia.Rect.MakeLTRB(x - w * 0.5, yb - h, x + w * 0.5, yb)), skia.ClipOp.kIntersect, True)
    c.drawRect(skia.Rect.MakeLTRB(x - w * 0.6, yb - h, x + w * 0.6, yb), skia.Paint(Shader=sh))
    c.restore()
    glow(c, x, yb - h * 0.45, h * 0.95, "#FFB04A", 0.30 * a)


def crenel(c, x0, x1, ytop, mw, mh, gap, T, depth=0.0, col="#8A7452", kind="guelph"):
    """Mazgal dişleri (guelph: kare; ghibelline: kırlangıç kuyruğu); ytop = diş üst kenarı, mh yükseklik."""
    x = x0
    while x < x1 - mw * 0.4:
        w_ = min(mw, x1 - x)
        R(c, x, ytop, x + w_, ytop + mh, T(col, depth))
        R(c, x + w_ * 0.68, ytop, x + w_, ytop + mh, "#1A1008", 38)
        c.drawRect(skia.Rect.MakeLTRB(x, ytop, x + w_, ytop + mh), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.1, Color=C(INK, 150)))
        if kind == "ghibelline":
            c.drawPath(sk.poly_path([(x + w_ * 0.3, ytop), (x + w_ * 0.5, ytop + mh * 0.34), (x + w_ * 0.7, ytop)]), _pt("#1A1008", 150))
        else:
            R(c, x - 1.5, ytop - 3, x + w_ + 1.5, ytop + 1, T("#A28A62", depth))
        x += mw + gap


def machico(c, x0, x1, y, h, T, depth=0.0, unit=24.0, col="#8A7452"):
    """Konsol üstünde çıkma galeri (machicolation): y = galerinin alt kenarı, h yükseklik; kemerli aralıklar + alt konsollar."""
    R(c, x0 - 6, y - h, x1 + 6, y, T(col, depth))
    R(c, x0 - 8, y - h, x1 + 8, y - h + 4, T("#A28A62", depth))
    n = max(2, int((x1 - x0) / unit))
    st = (x1 - x0) / n
    for i in range(n):
        ax = x0 + (i + 0.5) * st
        c.drawPath(arch_path(ax, y - h * 0.05, st * 0.56, h * 0.74), _pt("#2A1E14", 215))
        c.drawPath(sk.poly_path([(ax - st * 0.5, y), (ax - st * 0.5 + st * 0.18, y + h * 0.38), (ax - st * 0.5 + st * 0.36, y)]), _pt(T(col, depth)))
        INKP(c, sk.poly_path([(ax - st * 0.5, y), (ax - st * 0.5 + st * 0.18, y + h * 0.38), (ax - st * 0.5 + st * 0.36, y)]), 0.9, 130)
    c.drawRect(skia.Rect.MakeLTRB(x0 - 6, y - h, x1 + 6, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 165)))


def tower_geom(cx, yb, tw, Hs, roof_h=None, gal_h=None):
    """vecchio_tower'ın çizimsiz geometrisi (önbellekten yüklenen kareaşlarda da bayrak/çan konumu bilinsin)."""
    gal_h = gal_h or tw * 0.34
    gy = yb - Hs
    bw_ = tw * 0.92
    bh_ = tw * 1.15
    b_y1 = gy - gal_h - 1
    b_y0 = b_y1 - bh_
    rh = roof_h or tw * 0.95
    top = b_y0 - rh
    return dict(flag=(cx, top - tw * 0.52), bell=(cx, b_y1 - bh_ * 0.06, bw_ * 0.80, bh_ * 0.74), top=top - tw * 0.55, gal=gy, b_y0=b_y0, b_y1=b_y1, tw=tw, cx=cx)


def vecchio_tower(c, cx, yb, tw, Hs, T, depth=0.0, seed=3, roof_h=None, gal_h=None):
    """Arnolfo kulesi (Palazzo Vecchio): cx orta, yb taban, tw gövde genişliği, Hs gövde yüksekliği. Üstte çıkma galeri + mazgal, çan odası (çan siluetli
    iki kemer), kiremit külah, küre + direk. Dönüş: dict(flag=(x,y), bell=(x,yb,w,h), top=y, gal=y)."""
    gal_h = gal_h or tw * 0.34
    stone_wall(c, cx - tw / 2, yb - Hs, cx + tw / 2, yb, "#BFA77F", T, depth, seed, ch=max(14.0, tw * 0.17), bw=(tw * 0.30, tw * 0.55), rustic=False)
    c.drawRect(skia.Rect.MakeLTRB(cx - tw / 2, yb - Hs, cx + tw / 2, yb), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 165)))
    for ry in (0.22, 0.52):                                   # dar ok yarıkları
        yy = yb - Hs * ry
        c.drawPath(arch_path(cx, yy, tw * 0.09, tw * 0.34), _pt("#241810", 225))
    # kule gövdesi sağ gölge
    R(c, cx + tw * 0.28, yb - Hs, cx + tw / 2, yb, "#1A1008", 34)
    gy = yb - Hs
    gx0, gx1 = cx - tw * 0.80, cx + tw * 0.80
    machico(c, gx0, gx1, gy, gal_h, T, depth, unit=tw * 0.21)
    m_top = gy - gal_h - tw * 0.22
    crenel(c, gx0, gx1, m_top, tw * 0.15, tw * 0.22, tw * 0.07, T, depth, kind="guelph")
    R(c, gx0 - 3, m_top + tw * 0.2, gx1 + 3, gy - gal_h + 2, T("#8A7452", depth))
    # çan odası
    bw_ = tw * 0.92
    bh_ = tw * 1.15
    b_y1 = gy - gal_h - 1
    b_y0 = b_y1 - bh_
    R(c, cx - bw_ / 2, b_y0, cx + bw_ / 2, b_y1, T("#C0A980", depth))
    stone_wall(c, cx - bw_ / 2, b_y0, cx + bw_ / 2, b_y1, "#C0A980", T, depth, seed + 5, ch=tw * 0.16, bw=(tw * 0.3, tw * 0.5), rustic=False, joint_a=70)
    c.drawRect(skia.Rect.MakeLTRB(cx - bw_ / 2, b_y0, cx + bw_ / 2, b_y1), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 160)))
    bell = None
    for sgn in (-1, 1):
        ax = cx + sgn * bw_ * 0.22
        c.drawPath(arch_path(ax, b_y1 - bh_ * 0.06, bw_ * 0.30, bh_ * 0.74), _pt("#22160D", 235))
        INKP(c, arch_path(ax, b_y1 - bh_ * 0.06, bw_ * 0.30, bh_ * 0.74), 1.0, 160)
    # çan siluetleri (bronz) — yalnız görsel, ses/olay iddiası yok
    for sgn in (-1, 1):
        ax = cx + sgn * bw_ * 0.22
        bp = skia.Path()
        by = b_y0 + bh_ * 0.34
        bp.moveTo(ax - bw_ * 0.085, by + bh_ * 0.30)
        bp.cubicTo(ax - bw_ * 0.085, by + bh_ * 0.10, ax - bw_ * 0.05, by, ax, by)
        bp.cubicTo(ax + bw_ * 0.05, by, ax + bw_ * 0.085, by + bh_ * 0.10, ax + bw_ * 0.085, by + bh_ * 0.30)
        bp.close()
        c.drawPath(bp, _pt(T("#9A6A2A", 0.0), 235))
    bell = (cx, b_y1 - bh_ * 0.06, bw_ * 0.80, bh_ * 0.74)
    # kiremit külah
    rh = roof_h or tw * 0.95
    roof = sk.poly_path([(cx - bw_ * 0.60, b_y0), (cx, b_y0 - rh), (cx + bw_ * 0.60, b_y0)])
    c.drawPath(roof, _pt(T("#B4552E", depth)))
    c.save()
    c.clipPath(roof, skia.ClipOp.kIntersect, True)
    for k in range(1, 9):
        c.drawLine(cx - bw_ * 0.62, b_y0 - rh * k / 9.0, cx + bw_ * 0.62, b_y0 - rh * k / 9.0, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#5A2412", 90)))
    R(c, cx + bw_ * 0.0, b_y0 - rh, cx + bw_ * 0.62, b_y0, "#1A1008", 30)
    c.restore()
    INKP(c, roof, 1.2, 175)
    top = b_y0 - rh
    c.drawCircle(cx, top - tw * 0.05, tw * 0.07, _pt(T("#D8A63A", 0.0)))
    c.drawLine(cx, top - tw * 0.05, cx, top - tw * 0.55, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(2.0, tw * 0.024), Color=C(INK, 215)))
    return dict(flag=(cx, top - tw * 0.52), bell=bell, top=top - tw * 0.55, gal=gy, b_y0=b_y0, b_y1=b_y1, tw=tw, cx=cx)


def palazzo_geom(kind, x, y, w, h, door=None, tower=True, tower_x=0.60):
    """Cephe geometrisi (çizimsiz): pencere kutuları [(xc,yb,w,h,satır)], kapı (xc,yb,w,h), kule (xc,yb,tw,Hs), galeri/çatı yüksekliği. x sol kenar, y zemin."""
    g = dict(kind=kind, x0=x, x1=x + w, y0=y, w=w, h=h, wins=[], door=None, tower=None)
    if kind == "vecchio":
        body = 0.78 * h
        g["yt"] = y - body
        wh = 0.22 * h
        ww = min(0.060 * w, wh * 0.74)
        n = max(3, int(round(w / (ww * 2.55))))
        for row, yb in ((1, y - 0.30 * h), (2, y - 0.60 * h)):
            for i in range(n):
                g["wins"].append(((x + (i + 0.5) * w / n), yb, ww, wh, row))
        if door is not None:
            dh = 0.40 * h
            g["door"] = (x + 0.28 * w, y, dh * 0.74, dh)
            g["wins"] = [q for q in g["wins"] if not (q[4] == 1 and abs(q[0] - g["door"][0]) < ww * 1.2)]
        if tower:
            tw = max(44.0, 0.072 * w)
            g["tower"] = (x + tower_x * w, y - 0.90 * h, tw, 0.50 * h)
            tg = tower_geom(g["tower"][0], g["tower"][1], tw, g["tower"][3], roof_h=tw * 0.80)
            g["flag"], g["bell"], g["top"] = tg["flag"], tg["bell"], tg["top"]
    elif kind == "medici":
        g["yt"] = y - 0.92 * h
        wh = 0.17 * h
        ww = min(0.056 * w, wh * 0.80)
        n = max(3, int(round(w / (ww * 2.7))))
        for row, yb in ((1, y - 0.445 * h), (2, y - 0.685 * h)):
            for i in range(n):
                g["wins"].append(((x + (i + 0.5) * w / n), yb, ww, wh, row))
        if door is not None:
            dh = 0.36 * h
            g["door"] = (x + 0.14 * w, y, dh * 0.78, dh)
    else:
        g["yt"] = y - 0.86 * h
        wh = 0.19 * h
        ww = min(0.05 * w, wh * 0.70)
        n = max(3, int(round(w / (ww * 2.9))))
        for row, yb in ((1, y - 0.30 * h), (2, y - 0.58 * h)):
            for i in range(n):
                g["wins"].append(((x + (i + 0.5) * w / n), yb, ww, wh, row))
        if door is not None:
            dh = 0.34 * h
            g["door"] = (x + 0.5 * w, y, dh * 0.74, dh)
            g["wins"] = [q for q in g["wins"] if not (q[4] == 1 and abs(q[0] - g["door"][0]) < ww * 1.3)]
    return g


def portal(c, xc, yb, dw, dh, T, depth=0.0, interior="#1A120A"):
    """Taş çerçeveli kemerli kapı açıklığı (kanatsız, koyu iç): kemer taşları + söve."""
    fr = dw * 0.20
    outer = arch_path(xc, yb, dw + 2 * fr, dh + fr)
    c.drawPath(outer, _pt(T("#D2C096", depth)))
    INKP(c, outer, 1.4, 180)
    n = 11
    rr = (dw + 2 * fr) / 2
    for i in range(n + 1):                                    # kemer taşları (ışınsal çizgiler)
        a = math.pi * (1 - i / n)
        cx_, cy_ = xc, yb - dh - fr + rr
        c.drawLine(cx_ + math.cos(a) * (rr - fr), cy_ - math.sin(a) * (rr - fr), cx_ + math.cos(a) * rr, cy_ - math.sin(a) * rr, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C(INK, 120)))
    inner = arch_path(xc, yb, dw, dh)
    c.drawPath(inner, _pt(T(interior, 0.0)))
    INKP(c, inner, 1.2, 170)
    R(c, xc - dw / 2 - fr, yb - 7, xc + dw / 2 + fr, yb, T("#BDAB82", depth))            # eşik taşı
    INKR(c, xc - dw / 2 - fr, yb - 7, xc + dw / 2 + fr, yb, 1.0, 130)


_WOOD = {}


def door_heavy(f, x, y, h, open_amount=0.0, w=None, alpha=1.0, glow_k=0.0, seed=1, swing=0.0):
    """Ağır ahşap kapı (iki kanat, demir kuşak + perçin + halka): x orta, y taban, h yükseklik. open_amount 0 = kapalı, 1 = iki kanat içe sonuna kadar açık
    (kanatlar eşik taşında menteşeli; açık kanat yatayda kısalır, serbest kenar perspektifle küçülür). glow_k: iç mekândan gelen sıcak ışık (0..1)."""
    c = _cv(f)
    w = w or h * 0.74
    r = w / 2.0
    th = clamp(open_amount) * 1.22                                           # rad (≈70°)
    ct, st = math.cos(th), math.sin(th)
    # iç boşluk (kanatların gerisinde)
    if open_amount > 0.01:
        inner = arch_path(x, y, w, h)
        sh = skia.GradientShader.MakeLinear([(0, y - h), (0, y)], [C("#0E0905", 255), C("#1E140B", 255), C(mix("#2A1A0C", "#C98A3A", 0.5 * glow_k), 255)], [0.0, 0.65, 1.0])
        c.drawPath(inner, skia.Paint(AntiAlias=True, Shader=sh))
        if glow_k > 0.01:
            c.drawRect(skia.Rect.MakeLTRB(x - w * 0.4, y - 10, x + w * 0.4, y), skia.Paint(Color=C("#FFC070", int(110 * glow_k))))
    wood, wood2 = "#5C3D22", "#3E2814"
    for sgn in (-1, 1):
        hx = x + sgn * r                                                       # menteşe kenarı (x)
        fx = hx - sgn * (w / 2.0) * ct                                         # serbest kenar
        sc_free = 1.0 - 0.13 * st                                              # serbest kenarda perspektif küçülme
        pts_top, pts_bot = [], []
        N = 8
        for i in range(N + 1):
            u = i / N
            xu = hx - sgn * (w / 2.0) * u                                      # kanat boyunca (düzlem içi) konum
            dx_c = xu - x
            ytop_flat = (y - h + r) - math.sqrt(max(0.0, r * r - dx_c * dx_c)) if abs(dx_c) < r else (y - h + r)
            sc = 1.0 - (1.0 - sc_free) * u
            X = hx - sgn * (w / 2.0) * ct * u
            pts_top.append((X, y - (y - ytop_flat) * sc))
            pts_bot.append((X, y - 0.0))
        poly = pts_top + pts_bot[::-1]
        path = sk.poly_path(poly)
        shade = 0.10 + 0.30 * st * (1 if sgn > 0 else 0.7)
        sh = skia.GradientShader.MakeLinear([(hx, 0), (fx, 0)], [C(mix(wood, "#1A1008", 0.0), int(255 * alpha)), C(mix(wood, "#1A1008", 0.18 + shade), int(255 * alpha))], [0.0, 1.0])
        c.drawPath(path, skia.Paint(AntiAlias=True, Shader=sh))
        c.save()
        c.clipPath(path, skia.ClipOp.kIntersect, True)
        npl = 5                                                                 # tahta araları + damar
        for i in range(1, npl):
            X = hx + (fx - hx) * i / npl
            c.drawLine(X, y - h, X, y, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(wood2, int(210 * alpha))))
        rs = _RS(seed + (3 if sgn > 0 else 0))
        for i in range(14):
            X = hx + (fx - hx) * rs.uniform(0.03, 0.97)
            y0_ = y - rs.uniform(0.1, 0.9) * h
            c.drawLine(X, y0_, X + rs.uniform(-1.5, 1.5), y0_ + rs.uniform(18, 60) * (h / 380.0), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#1A1008", 55)))
        # demir kuşaklar + perçinler
        for ry in (0.22, 0.52, 0.80):
            yy = y - h * ry
            ys_ = y - (y - yy) * (1.0 - (1.0 - sc_free) * 0.5)
            c.drawRect(skia.Rect.MakeLTRB(min(hx, fx), ys_ - h * 0.022, max(hx, fx), ys_ + h * 0.022), skia.Paint(Color=C("#262220", int(240 * alpha))))
            for i in range(6):
                X = hx + (fx - hx) * (0.08 + 0.17 * i)
                c.drawCircle(X, ys_, max(1.6, h * 0.0065), skia.Paint(AntiAlias=True, Color=C("#8E8070", int(235 * alpha))))
        c.restore()
        INKP(c, path, 1.4, int(190 * alpha))
        # halka (kapalıyken orta çizgiye yakın; açıkken serbest kenarda)
        rx = fx + sgn * (w * 0.06) * (1 if abs(ct) > 0.2 else 0) + swing * h * 0.02
        ry_ = y - h * 0.40
        rr_ = h * 0.036
        c.drawCircle(rx, ry_, rr_, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(2.0, h * 0.009), Color=C("#B8A27A", int(240 * alpha))))
        c.drawCircle(rx, ry_ - rr_ * 1.25, max(2.0, h * 0.012), skia.Paint(AntiAlias=True, Color=C("#4A4036", int(240 * alpha))))
    if open_amount < 0.02:                                                    # orta kilit sürgüsü
        R(c, x - 2, y - h * 0.58, x + 2, y - h * 0.22, "#1A1614", 200)


# ═════════════════════════════ palazzo cepheleri ═════════════════════════════
def palazzo_front(f, x, y, w, h, kind="vecchio", door=None, T=None, depth=0.0, seed=1, shield=False, tower=True, tower_x=0.60, leaves=True, wins_dark=True):
    """Palazzo cephesi çizer; döner: geometri sözlüğü (pencere kutuları, kapı, kule). x sol kenar, y zemin (ayak), w × h BLOK (kule hariç).
    kind: "vecchio" (bugnato blok + iki sıra bifora + konsollu mazgal galeri + Arnolfo kulesi) | "medici" (3 kat bugnato→sıva, bifora, güçlü saçak) | "generic".
    door: None = kapısız | 0..1 = ağır kapı (0 kapalı … 1 açık; `leaves=False` ise yalnız kemerli çerçeve, kanatlar dinamik `door_heavy`).
    shield: Medici kalkanı (altın zemin, altı kırmızı top). T: renk uyarlayıcı (cilt_city.Tint); None = gündüz."""
    c = _cv(f)
    T = T or CT.Tint("day")
    g = palazzo_geom(kind, x, y, w, h, door, tower, tower_x)
    x1 = x + w
    if kind == "vecchio":
        yt = g["yt"]
        if tower and g["tower"]:                                                  # kule bloğun ARKASINDA başlar (mazgal dişleri önde kalır)
            tcx, tyb, tw, Hs = g["tower"]
            tinfo = vecchio_tower(c, tcx, tyb, tw, Hs, T, depth, seed + 7, roof_h=tw * 0.80)
            g["flag"] = tinfo["flag"]
            g["bell"] = tinfo["bell"]
            g["top"] = tinfo["top"]
        stone_wall(c, x, yt, x1, y, "#BFA77F", T, depth, seed, ch=h * 0.088, bw=(w * 0.05, w * 0.085), rustic=True)
        for fy in (y - 0.17 * h, y - 0.45 * h, y - 0.74 * h):                   # kat silmeleri
            R(c, x - 3, fy - 4, x1 + 3, fy + 3, T("#D6C49C", depth))
            c.drawLine(x - 3, fy + 3, x1 + 3, fy + 3, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 150)))
        n0 = max(4, int(w / 150))
        for i in range(n0):                                                     # zemin kat dar pencereleri
            wx = x + (i + 0.5) * w / n0
            if g["door"] and abs(wx - g["door"][0]) < g["door"][2] * 1.15:
                continue
            c.drawPath(arch_path(wx, y - 0.07 * h, w * 0.024, h * 0.17), _pt("#241810", 220))
            R(c, wx - w * 0.012, y - 0.07 * h - h * 0.045, wx + w * 0.012, y - 0.07 * h - h * 0.04, "#3A2A18", 200)      # demir parmaklık
        for (xc, yb, ww, wh, row) in g["wins"]:
            bifora(c, xc, yb, ww, wh, T, depth)
        gy = g["yt"]
        machico(c, x - 4, x1 + 4, gy, 0.11 * h, T, depth, unit=h * 0.075)
        crenel(c, x - 4, x1 + 4, gy - 0.22 * h, h * 0.050, h * 0.10, h * 0.026, T, depth, kind="guelph")
        R(c, x - 6, gy - 0.12 * h, x1 + 6, gy - 0.11 * h + 2, T("#8A7452", depth))
        c.drawRect(skia.Rect.MakeLTRB(x, gy, x1, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 170)))
        R(c, x1 - w * 0.07, gy, x1, y, "#1A1008", 34)
    elif kind == "medici":
        yt = g["yt"]
        stone_wall(c, x, y - 0.36 * h, x1, y, "#C9B68C", T, depth, seed, ch=h * 0.10, bw=(w * 0.06, w * 0.10), rustic=True)
        stone_wall(c, x, y - 0.64 * h, x1, y - 0.36 * h, "#D2C096", T, depth, seed + 1, ch=h * 0.07, bw=(w * 0.05, w * 0.08), rustic=True, joint_a=80)
        R(c, x, yt + 0.10 * h * 0.0, x1, y - 0.64 * h, T("#E3D4AC", depth))
        R(c, x, yt, x1, y - 0.64 * h, T("#E3D4AC", depth))
        for fy in (y - 0.36 * h, y - 0.64 * h):
            R(c, x - 3, fy - 4, x1 + 3, fy + 3, T("#DCCCA2", depth))
            c.drawLine(x - 3, fy + 3, x1 + 3, fy + 3, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 150)))
        for (xc, yb, ww, wh, row) in g["wins"]:
            bifora(c, xc, yb, ww, wh, T, depth)
        n0 = max(3, int(w / 175))
        for i in range(n0):                                                     # zemin kat "diz çökmüş" pencereler
            wx = x + (i + 0.5) * w / n0 + (0.0 if g["door"] is None else w * 0.03)
            if g["door"] and abs(wx - g["door"][0]) < g["door"][2] * 1.3:
                continue
            c.drawPath(arch_path(wx, y - 0.09 * h, w * 0.040, h * 0.15), _pt(T("#2A1E14", 0.3)))
            R(c, wx - w * 0.028, y - 0.09 * h, wx + w * 0.028, y - 0.075 * h, T("#BDAB82", depth))
        # saçak (cornicione)
        R(c, x - 14, yt - 5, x1 + 14, yt + 0.06 * h, T("#C6B488", depth))
        R(c, x - 14, yt - 5, x1 + 14, yt, T("#DACA9E", depth))
        nbk = int(w / 26)
        for i in range(nbk):
            bx = x - 10 + i * (w + 20) / nbk
            c.drawPath(sk.poly_path([(bx, yt + 0.06 * h), (bx + (w + 20) / nbk * 0.8, yt + 0.06 * h), (bx + (w + 20) / nbk * 0.4, yt + 0.06 * h + 9)]), _pt(T("#9C8A64", depth)))
        c.drawRect(skia.Rect.MakeLTRB(x - 14, yt - 5, x1 + 14, yt + 0.06 * h), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 165)))
        R(c, x1 - w * 0.06, yt + 0.06 * h, x1, y, "#1A1008", 32)
        c.drawRect(skia.Rect.MakeLTRB(x, yt + 0.06 * h, x1, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 170)))
        # çatı kenarı (alçak, görünür kiremit şeridi)
        poly = [(x - 14, yt - 5), (x + 40, yt - 0.10 * h), (x1 - 40, yt - 0.10 * h), (x1 + 14, yt - 5)]
        c.drawPath(sk.poly_path(poly), _pt(T("#B4552E", depth)))
        INKP(c, sk.poly_path(poly), 1.2, 170)
        if shield:
            sx_, sy_ = x + w * 0.30, y - 0.52 * h
            medici_shield(c, sx_, sy_, h * 0.12, T)
    else:
        yt = g["yt"]
        R(c, x, yt, x1, y, T("#E1CFA6", depth))
        stone_wall(c, x, y - 0.14 * h, x1, y, "#CDB98E", T, depth, seed, ch=h * 0.07, bw=(w * 0.06, w * 0.10), rustic=True, joint_a=90)
        for qy in range(int((y - yt) / (h * 0.09)) + 1):                          # köşe taşları
            yy = yt + qy * h * 0.09
            R(c, x, yy, x + w * 0.02, yy + h * 0.085, T("#CDBB92" if qy % 2 else "#D8C8A0", depth))
            R(c, x1 - w * 0.02, yy, x1, yy + h * 0.085, T("#CDBB92" if qy % 2 else "#D8C8A0", depth))
        for fy in (y - 0.16 * h, y - 0.46 * h):
            R(c, x, fy - 3, x1, fy + 2, T("#CDBB92", depth))
        for (xc, yb, ww, wh, row) in g["wins"]:
            wp = arch_path(xc, yb, ww, wh)
            c.drawPath(wp, _pt(T("#2A1E14", depth * 0.3)))
            INKP(c, wp, 1.1, 160)
            R(c, xc - ww * 0.6, yb - 2, xc + ww * 0.6, yb + 3, T("#CDBB92", depth))
            R(c, xc - ww * 0.5, yb - wh * 0.40, xc - ww * 0.5 + ww * 0.34, yb, T("#4E6E4A", depth), 235)      # kepenk
        R(c, x - 10, yt - 2, x1 + 10, yt + 0.05 * h, T("#C6B488", depth))
        roof = sk.poly_path([(x - 14, yt - 2), (x + w * 0.10, yt - h * 0.16), (x1 - w * 0.10, yt - h * 0.16), (x1 + 14, yt - 2)])
        c.drawPath(roof, _pt(T("#B4552E", depth)))
        INKP(c, roof, 1.2, 170)
        R(c, x1 - w * 0.06, yt, x1, y, "#1A1008", 30)
        c.drawRect(skia.Rect.MakeLTRB(x, yt, x1, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 170)))
    if g["door"] is not None:
        xc, yb, dw, dh = g["door"]
        portal(c, xc, yb, dw, dh, T, depth)
        if leaves and door is not None:
            door_heavy(f, xc, yb, dh, float(door), w=dw)
    return g


def medici_shield(c, x, y, s, T=None):
    """Medici kalkanı (stilize, altın zemin + altı kırmızı top; yazı yok): x,y merkez, s yarı genişlik."""
    sp = skia.Path()
    sp.moveTo(x - s, y - s * 1.05)
    sp.lineTo(x + s, y - s * 1.05)
    sp.lineTo(x + s, y + s * 0.2)
    sp.cubicTo(x + s, y + s * 0.9, x + s * 0.3, y + s * 1.25, x, y + s * 1.45)
    sp.cubicTo(x - s * 0.3, y + s * 1.25, x - s, y + s * 0.9, x - s, y + s * 0.2)
    sp.close()
    c.drawPath(sp, _pt("#E0B84E"))
    INKP(c, sp, 1.6, 200)
    for (px, py) in ((0.0, -0.62), (-0.46, -0.12), (0.46, -0.12), (-0.24, 0.40), (0.24, 0.40), (0.0, 0.82)):
        c.drawCircle(x + px * s, y + py * s, s * 0.21, _pt("#B33620"))
        c.drawCircle(x + px * s - s * 0.06, y + py * s - s * 0.07, s * 0.07, _pt("#FFFFFF", 90))


def loggia(c, x0, x1, y, h, T, depth=0.0, nb=3, seed=2):
    """Loggia dei Lanzi: üç geniş yuvarlak kemer, kalın ayaklar, üstte çeyrek-yonca yuvarlak frizli teras duvarı ve korkuluk."""
    top = y - h
    R(c, x0, top, x1, y, T("#D3C198", depth))
    step = (x1 - x0) / nb
    pier = step * 0.17
    R(c, x0, top - h * 0.30, x1, top + 4, T("#E2D3AB", depth))                                    # üst kat duvarı
    for i in range(nb):
        ax = x0 + (i + 0.5) * step
        arc_w = step - pier * 1.6
        c.drawPath(arch_path(ax, y, arc_w, h * 0.86), _pt(T("#3A2A1C", 0.0)))
        # iç gölge + derinlik
        c.drawPath(arch_path(ax, y, arc_w * 0.9, h * 0.80), _pt("#241810", 110))
    for i in range(nb + 1):
        px = x0 + i * step
        R(c, px - pier * 0.5, top, px + pier * 0.5, y, T("#C7B48A", depth))
        R(c, px + pier * 0.12, top, px + pier * 0.5, y, "#1A1008", 36)
        c.drawRect(skia.Rect.MakeLTRB(px - pier * 0.5, top, px + pier * 0.5, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 150)))
    for i in range(nb):                                                                              # kemer silmesi
        ax = x0 + (i + 0.5) * step
        ar = (step - pier * 1.6) / 2 + 6
        p = skia.Path()
        p.moveTo(ax - ar, y - h * 0.86 + (step - pier * 1.6) / 2)
        p.arcTo(skia.Rect.MakeLTRB(ax - ar, y - h * 0.86 - 6, ax + ar, y - h * 0.86 - 6 + 2 * ar), 180, 180, False)
        c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6.0, Color=C(T("#C9C6B4", 0.0))))
        INKP(c, p, 1.1, 140)
    fy0, fy1 = top - h * 0.24, top - 2
    R(c, x0 - 8, fy0, x1 + 8, fy1, T("#E9DDB8", depth))
    nq = int((x1 - x0) / (h * 0.30))
    for i in range(nq):
        qx = x0 + (i + 0.5) * (x1 - x0) / nq
        qr = (fy1 - fy0) * 0.36
        for a_ in range(4):
            ang = a_ * math.pi / 2 + math.pi / 4
            c.drawCircle(qx + math.cos(ang) * qr * 0.55, (fy0 + fy1) / 2 + math.sin(ang) * qr * 0.55, qr * 0.52, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=C("#8E7C58", 200)))
        c.drawCircle(qx, (fy0 + fy1) / 2, qr * 0.30, _pt(T("#6E8FB4", 0.0), 150))
    c.drawRect(skia.Rect.MakeLTRB(x0 - 8, fy0, x1 + 8, fy1), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 165)))
    R(c, x0 - 12, fy0 - 10, x1 + 12, fy0, T("#D6C8A0", depth))                                       # saçak
    c.drawLine(x0 - 12, fy0 - 10, x1 + 12, fy0 - 10, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 160)))
    # korkuluk
    nb2 = int((x1 - x0) / 34)
    for i in range(nb2):
        bx = x0 - 6 + i * (x1 - x0 + 12) / nb2
        R(c, bx, fy0 - 30, bx + 9, fy0 - 10, T("#D6C8A0", depth))
    R(c, x0 - 12, fy0 - 38, x1 + 12, fy0 - 30, T("#DCCFA8", depth))
    INKR(c, x0 - 12, fy0 - 38, x1 + 12, fy0 - 30, 1.1, 150)
    R(c, x0, y - 7, x1, y, T("#B8A67E", depth))


def narrow_house(c, x0, x1, y, h, T, seed=1, depth=0.22):
    """İki bina arasındaki dar araya sıkışmış gölgeli ev: kiremit beşik çatı, kemerli pencereler, alta doğru koyulaşma (sokak derinliği)."""
    rs = _RS(seed)
    w = x1 - x0
    wall = mix(T(CT.WALLS[rs.randint(len(CT.WALLS))], depth), "#2A1A0C", 0.26)
    R(c, x0 - 2, y - h, x1 + 2, y, wall)
    nx = max(1, int(w / 66))
    ny = max(2, int((h - 40) / 92))
    for iy in range(ny):
        for ix in range(nx):
            wx = x0 + (ix + 0.5) * w / nx
            wy = y - 46 - iy * (h - 90) / ny
            ww = min(34.0, w / nx * 0.52)
            wp = arch_path(wx, wy, ww, 58)
            c.drawPath(wp, _pt(T("#1E140C", 0.3)))
            INKP(c, wp, 1.0, 150)
            R(c, wx - ww * 0.6, wy - 2, wx + ww * 0.6, wy + 3, T("#B8A67E", depth))
    roof = sk.poly_path([(x0 - 7, y - h), (x0 + w * 0.5, y - h - w * 0.30), (x1 + 7, y - h)])
    c.drawPath(roof, _pt(mix(T("#B4552E", depth), "#2A1A0C", 0.18)))
    INKP(c, roof, 1.1, 165)
    for k in range(1, 6):
        yy = y - h - w * 0.30 * k / 6.0
        c.drawLine(x0 + w * 0.5 * k / 6.0 - 4, yy, x1 - w * 0.5 * k / 6.0 + 4, yy, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#3A160A", 80)))
    GRAD_V(c, x0 - 2, y - h, x1 + 2, y, [("#000000", 0.0, 20), ("#000000", 1.0, 125)])
    c.drawRect(skia.Rect.MakeLTRB(x0 - 2, y - h, x1 + 2, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 150)))


def torch_bracket(c, x, y, T=None):
    """Duvar meşale/fener demiri (konsol + halka): x,y = tutucu orta nokta."""
    col = "#2A2622"
    c.drawLine(x - 16, y + 4, x, y, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.4, Color=C(col, 245), StrokeCap=skia.Paint.kRound_Cap))
    c.drawCircle(x, y - 3, 7, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6, Color=C(col, 245)))
    c.drawLine(x - 3, y - 2, x - 7, y + 26, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.4, Color=C("#5A3C22", 245), StrokeCap=skia.Paint.kRound_Cap))


# ═════════════════════════════ ateş / duman / kıvılcım (önceden renklendirilmiş sprite'lar) ═════════════════════════════
_FIRE = {}
NFL = 16
FW, FH = 320, 520


def _flame_frames():
    """16 karelik alev döngüsü (320×520, taban alt-orta (160,508)): her dilim kendi dikey degradesiyle (taban sıcak sarı → turuncu → kızıl, uç saydam),
    dıştan içe 4 katman + sürüklenen kıvılcım dilleri; kenarlar hafif yumuşatılmış. Tam döngü (tam sayı frekans)."""
    if "fr" in _FIRE:
        return _FIRE["fr"]
    fr_list = []
    # (katman, dilim sayısı, yükseklik, taban genişliği, degrade durakları)
    layers = [
        (7, 1.00, 1.00, [("#F58A22", 255, 0.0), ("#E04A1A", 248, 0.42), ("#A8200F", 175, 0.84), ("#7A140C", 0, 1.0)]),
        (6, 0.84, 0.84, [("#FFC845", 255, 0.0), ("#F59A2A", 252, 0.50), ("#E8631F", 205, 0.90), ("#E8631F", 0, 1.0)]),
        (4, 0.62, 0.66, [("#FFF3B8", 255, 0.0), ("#FFD761", 252, 0.55), ("#FFB43A", 160, 0.92), ("#FFB43A", 0, 1.0)]),
        (2, 0.36, 0.50, [("#FFFCEA", 255, 0.0), ("#FFF3B8", 235, 0.60), ("#FFF3B8", 0, 1.0)]),
    ]
    blur = skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 1.5)
    for k in range(NFL):
        ph = 2 * math.pi * k / NFL
        fr = sk.Frame(FW, FH)
        fr.clear(skia.ColorTRANSPARENT)
        c = fr.c
        bx, by = FW / 2.0, FH - 12.0
        for li, (nt, hs, ws, stops) in enumerate(layers):
            rs = _RS(7 + li * 3)
            for i in range(nt):
                u = (i - (nt - 1) / 2.0) / max(1.0, (nt - 1) / 2.0)                    # -1..1
                r1, r2 = rs.uniform(0, 6.28), rs.uniform(0, 6.28)
                hh = (404 - 118 * abs(u) ** 1.2) * hs * (0.86 + 0.14 * math.sin(ph + r1)) * (0.94 + 0.06 * math.sin(2 * ph + r2)) * (0.96 + 0.04 * math.sin(3 * ph + i))
                bw = (58 - 13 * abs(u)) * ws
                xo = u * 70 * (1.0 - 0.28 * li / 3.0)
                sway = (22 + 8 * li) * math.sin(ph + r1 * 0.7 + i * 1.3) * 0.5 + u * 26 * (1 - 0.3 * li) + 9 * math.sin(2 * ph + r2)
                tipx, tipy = bx + xo + sway, by - hh
                midx = bx + xo + sway * 0.35 + 6 * math.sin(2 * ph + i)
                p = skia.Path()
                p.moveTo(bx + xo - bw, by)
                p.cubicTo(bx + xo - bw * 1.18, by - hh * 0.34, midx - bw * 0.62, by - hh * 0.66, tipx, tipy)
                p.cubicTo(midx + bw * 0.42, by - hh * 0.62, bx + xo + bw * 1.22, by - hh * 0.30, bx + xo + bw, by)
                p.close()
                sh = skia.GradientShader.MakeLinear([(0, by), (0, tipy)], [C(cc, aa) for cc, aa, _ in stops], [pp for _, _, pp in stops])
                c.drawPath(p, skia.Paint(AntiAlias=True, Shader=sh, MaskFilter=blur if li < 2 else None))
        # sürüklenen kıvılcım dilleri (yükselir, küçülür, solar)
        for j in range(4):
            u = (k / NFL + j / 4.0) % 1.0
            yy = by - FH * (0.50 + 0.46 * u)
            xx = bx + (j - 1.5) * 34 + 14 * math.sin(2 * math.pi * u * 1.5 + j * 2.0)
            hh = 54 * (1 - u) ** 0.8 + 6
            ww = 11 * (1 - 0.6 * u)
            lp = skia.Path()
            lp.moveTo(xx - ww, yy)
            lp.cubicTo(xx - ww, yy - hh * 0.5, xx - ww * 0.2, yy - hh * 0.8, xx, yy - hh)
            lp.cubicTo(xx + ww * 0.2, yy - hh * 0.8, xx + ww, yy - hh * 0.5, xx + ww, yy)
            lp.close()
            al = int(255 * math.sin(math.pi * u) ** 0.7)
            sh = skia.GradientShader.MakeLinear([(0, yy), (0, yy - hh)], [C("#FFD761", al), C("#F0742A", int(al * 0.5))], [0.0, 1.0])
            c.drawPath(lp, skia.Paint(AntiAlias=True, Shader=sh, MaskFilter=blur))
        fr_list.append(fr.surf.makeImageSnapshot())
    _FIRE["fr"] = fr_list
    return fr_list


def _soft_dot(col, n=48, power=1.6):
    key = ("dot", col, n)
    im = _FIRE.get(key)
    if im is None:
        yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
        r = np.hypot(xx - n / 2 + 0.5, yy - n / 2 + 0.5) / (n / 2)
        a = np.clip(1 - r, 0, 1) ** power
        rgb = sk.rgb(col) if hasattr(sk, "rgb") else (255, 255, 255)
        arr = np.dstack([np.full((n, n), rgb[0], np.uint8), np.full((n, n), rgb[1], np.uint8), np.full((n, n), rgb[2], np.uint8), (a * 255).astype(np.uint8)])
        im = _FIRE[key] = sk.np_to_image(arr)
    return im


_DP = skia.Paint()


def _blit_dot(c, im, x, y, r, a):
    _DP.setAlphaf(clamp(a))
    c.drawImageRect(im, skia.Rect.MakeWH(im.width(), im.height()), skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), LIN, _DP)


def smoke_plume(f, x, y, t, size=120.0, n=9, k=1.0, col="#5A544E", seed=3, rise=260.0, wind=40.0, a0=0.34, warm=None):
    """Yükselen duman: büyüyüp solan yumuşak topaklar (önceden renklendirilmiş sprite, SrcOver). y = çıkış noktası. warm: genç topaklar ateş ışığıyla ısınır."""
    c = _cv(f)
    im = _soft_dot(col, 56, 1.25)
    imw = _soft_dot(warm, 56, 1.25) if warm else None
    rs = _RS(seed)
    for i in range(n):
        per = 3.4 + 1.5 * rs.rand()
        ph = (t / per + i / n + rs.rand() * 0.05) % 1.0
        r = size * (0.22 + 0.9 * ph) * (0.7 + 0.5 * k)
        px = x + wind * ph * ph * 2.2 + math.sin(ph * 5.5 + i * 1.7) * size * 0.16 * ph + rs.uniform(-1, 1) * size * 0.1
        py = y - rise * (0.15 + ph) * (0.6 + 0.5 * k)
        a = a0 * k * math.sin(math.pi * min(1.0, ph * 1.15)) ** 1.4 * (1 - ph) ** 0.6
        wmix = (1.0 - smooth(clamp(ph / 0.42))) if imw is not None else 0.0
        _blit_dot(c, im, px, py, r, a * (1 - 0.7 * wmix))
        if wmix > 0.02:
            _blit_dot(c, imw, px, py, r * 0.9, a * 0.55 * wmix)


def torch_flame(c, x, y, t, size=36.0, seed=1):
    """Duvar meşalesi alevi (ucuz: 2 sprite + küçük parıltı + birkaç kıvılcım)."""
    fr = _flame_frames()
    fi = int(t * 14.0 + seed * 3) % NFL
    fl = 0.86 + 0.14 * math.sin(t * 9.0 + seed) + 0.06 * math.sin(t * 23 + seed * 2)
    glow(c, x, y - size * 0.7, size * 2.3 * fl, "#FFB04A", 0.42)
    for j, (dx, sc) in enumerate(((0.0, 1.0), (size * 0.12, 0.7))):
        ww = size * sc * 1.25
        hh = ww * (FH / FW) * (0.92 + 0.08 * math.sin(t * 8.0 + j + seed)) * fl
        _DP.setAlphaf(1.0)
        c.drawImageRect(fr[(fi + j * 5) % NFL], skia.Rect.MakeWH(FW, FH), skia.Rect.MakeXYWH(x + dx - ww / 2, y - hh * 0.985, ww, hh), LIN, _DP)
    ember_field(c, x, y - size * 0.8, t, n=7, spread=size * 0.35, h=size * 3.2, wind=30.0, k=1.0, seed=seed + 1, size=0.7)


def ember_field(f, x, y, t, n=40, spread=140.0, h=520.0, wind=60.0, k=1.0, seed=5, col="#FFB347", size=1.0):
    """Kıvılcım/kor uçuşu: yukarı süzülür, rüzgârla sağa sürüklenir, solar. x,y = çıkış."""
    c = _cv(f)
    im = _soft_dot(col, 24, 1.1)
    im2 = _soft_dot("#FFE9A0", 24, 1.3)
    rs = _RS(seed)
    for i in range(int(n * clamp(k, 0.0, 1.0)) if k < 1.0 else n):
        per = 1.7 + 2.2 * rs.rand()
        ph = (t / per + rs.rand()) % 1.0
        x0 = x + rs.uniform(-spread, spread) * (0.4 + 0.6 * (1 - ph))
        px = x0 + wind * ph * (0.6 + rs.rand()) + math.sin(t * 2.6 + i * 1.9) * 16 * ph
        py = y - h * ph ** 0.85 * (0.45 + 0.55 * rs.rand())
        fl = 0.55 + 0.45 * abs(math.sin(t * 11.0 + i * 3.1))
        rr = (2.6 + 3.4 * rs.rand()) * size * (1 - 0.6 * ph)
        a = (1 - ph) ** 1.1 * fl
        _blit_dot(c, im, px, py, rr * 2.4, a * 0.55)
        _blit_dot(c, im2, px, py, rr * 1.0, a * 0.9)


def ash_field(f, x, y, t, n=60, span=900.0, wind=90.0, k=1.0, seed=8):
    """Kül uçuşu: gri ince pullar sağa doğru sürüklenir (rüzgâr +x), yavaşça alçalır/dalgalanır."""
    c = _cv(f)
    rs = _RS(seed)
    p = skia.Paint(AntiAlias=True)
    for i in range(n):
        per = 5.0 + 5.0 * rs.rand()
        ph = (t / per + rs.rand()) % 1.0
        x0 = x + rs.uniform(-span * 0.15, span * 0.2)
        px = x0 + wind * ph * per * (0.35 + 0.65 * rs.rand())
        py = y - rs.uniform(60, 420) + 70 * ph + math.sin(t * 1.3 + i * 2.1) * 14
        a = math.sin(math.pi * ph) ** 0.8 * 0.75 * k
        p.setColor(C("#6A6660" if i % 3 else "#8E8A82", int(255 * clamp(a))))
        w_ = 3.0 + 4.0 * rs.rand()
        c.save()
        c.translate(px, py)
        c.rotate(math.degrees(t * (0.6 + rs.rand()) + i))
        c.drawOval(skia.Rect.MakeLTRB(-w_, -w_ * 0.35, w_, w_ * 0.35), p)
        c.restore()


# alev yerleşimi: (k eşiği, dx/size, dy/size, ölçek)  — küçük kıvılcımdan inferno'ya sprite sprite çoğalır
FIRE_LAYOUT = [(0.00, -0.20, 0.00, 0.62), (0.08, 0.18, 0.00, 0.66), (0.20, 0.00, 0.00, 0.92), (0.34, -0.36, 0.00, 0.62), (0.40, 0.38, 0.00, 0.66),
               (0.50, -0.12, -0.26, 0.80), (0.58, 0.16, -0.30, 0.74), (0.70, 0.02, -0.52, 0.78), (0.82, -0.24, -0.46, 0.55), (0.88, 0.30, -0.44, 0.58)]


def bonfire(f, x, y, size, t, seed=1, k=1.0, glow_a=1.0, tod="night", layout=None, smoke=True, embers=True):
    """Alev + kıvılcım + duman (önceden renklendirilmiş degrade sprite'lar, SrcOver; ≈4–8 ms). x,y = ateş tabanı (alt orta), size = taban genişliği (px),
    k = 0..1: kıvılcım → tek küçük alev → çok dilli ateş → inferno (sprite sayısı ve boyu büyür; dilimler bağımsız fazla titreşir). layout=[(k_eşik, dx, dy, ölçek)…] (size oranı).
    Dönüş: alevin tepe y'si."""
    c = _cv(f)
    k = clamp(k)
    if k <= 0.003:
        return y
    fr = _flame_frames()
    lay = layout or FIRE_LAYOUT
    gl = glow_a * (0.30 + 0.70 * k)
    glow(c, x, y - size * 0.20 * (0.4 + k), size * (0.60 + 0.80 * k), "#FF7A22", 0.26 * gl)          # (büyük SrcOver parıltılar pahalı: yarıçap kısa tutulur)
    glow(c, x, y - size * 0.34 * (0.4 + k), size * (0.38 + 0.50 * k), "#FFB347", 0.36 * gl)
    top = y
    pd = _DP
    items = []
    for i, (k0, dxf, dyf, sc0) in enumerate(lay):
        g = smooth(clamp((k - k0) / 0.24))
        if g < 0.02:
            continue
        items.append((dyf, i, dxf, sc0, g))
    items.sort(key=lambda q: (q[0], -abs(q[2])))                          # yüksek ve dışta olan önce, alt/orta ön
    for (dyf, i, dxf, sc0, g) in items:
        fi = int(t * 14.0 + i * 5 + seed * 3) % NFL
        wob = 1.0 + 0.05 * math.sin(t * 7.3 + i * 2.2 + seed) + 0.025 * math.sin(t * 13.1 + i)
        ww = size * 0.80 * sc0 * (0.22 + 0.78 * g) * (1.0 + 0.04 * math.sin(t * 5.1 + i))
        hh = ww * (FH / FW) * wob * (0.55 + 0.45 * g) * 1.22
        xx = x + dxf * size * min(1.0, 0.45 + 0.55 * k)
        yy = y + dyf * size
        pd.setAlphaf(clamp(0.35 + 0.9 * g))
        c.drawImageRect(fr[fi], skia.Rect.MakeWH(FW, FH), skia.Rect.MakeXYWH(xx - ww / 2, yy - hh * ((FH - 8.0) / FH), ww, hh), LIN, pd)
        top = min(top, yy - hh * 0.80)
    if embers:
        ember_field(f, x, y - size * 0.30, t, n=int(12 + 40 * k), spread=size * 0.34, h=size * (0.9 + 1.9 * k), wind=50 + 45 * k, k=1.0, seed=seed + 4, size=1.0 + 0.4 * k)
    if smoke:
        smoke_plume(f, x, top + size * 0.15, t, size=size * 0.36, n=int(5 + 7 * k), k=k, col={"day": "#6A645C", "dusk": "#4E4650", "night": "#2A2E40"}.get(tod, "#4E4650"),
                    seed=seed + 9, rise=size * 2.0, wind=30 + 34 * k, a0=0.46, warm="#D8743A")
    return top


_WASH = {}


def wash(c, y0, h, stops, pos, alpha=1.0):
    """Bant boyunca dikey degrade örtü (bir kez pişirilir; alfa ayarlanabilir). stops=[(renk, alfa)]."""
    key = (int(y0), int(h), tuple(stops), tuple(pos))
    img = _WASH.get(key)
    if img is None:
        fr = sk.Frame(W, int(h))
        fr.clear(skia.ColorTRANSPARENT)
        sh = skia.GradientShader.MakeLinear([(0, 0), (0, h)], [C(c_, a_) for c_, a_ in stops], list(pos))
        fr.c.drawRect(skia.Rect.MakeLTRB(0, 0, W, h), skia.Paint(Shader=sh))
        img = _WASH[key] = fr.surf.makeImageSnapshot()
    p = skia.Paint()
    p.setAlphaf(clamp(alpha))
    c.drawImage(img, 0, y0, skia.SamplingOptions(), p)


# ═════════════════════════════ ışık havuzu (alacakaranlık/gece: kaynağa göre karartma + sıcak ton) ═════════════════════════════
_POOLS = {}


def light_pool_img(hue, warm=(255, 150, 70), n=512, warm_a=0.20, edge=0.90):
    key = (tuple(hue), tuple(warm), n, round(warm_a, 3), round(edge, 3))
    im = _POOLS.get(key)
    if im is None:
        yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
        r = np.hypot(xx - n / 2 + 0.5, yy - n / 2 + 0.5) / (n / 2) * 1.3
        stops = [0.0, 0.10, 0.30, 0.60, 0.95, 1.30]
        al = np.interp(r, stops, [warm_a, warm_a * 0.8, edge * 0.40, edge * 0.74, edge * 0.97, edge]).astype(np.float32)
        t = np.clip((r - 0.04) / 0.55, 0, 1)
        t = t * t * (3 - 2 * t)
        col = np.array(warm, np.float32)[None, None, :] * (1 - t[..., None]) + np.array(hue, np.float32)[None, None, :] * t[..., None]
        rs = _RS(3)
        al = np.clip(al + rs.uniform(-0.004, 0.004, al.shape).astype(np.float32), 0, 1)
        im = _POOLS[key] = sk.np_to_image(np.dstack([col, al * 255]).astype(np.uint8))
    return im


def light_pool(f, x, y, r, gain=1.0, hue=(8, 12, 44), warm=(255, 150, 70), warm_a=0.20, edge=0.90, rect=None):
    """Işık havuzu örtüsü: (x,y) merkezde sıcak/şeffaf, dışa doğru `hue` renginde koyulaşır. r = 'aydınlık' yarıçap; gain = genel karartma (0..1).
    rect=(x0,y0,x1,y1): kenar dolgusu bu dikdörtgenle sınırlanır (bant içi)."""
    c = _cv(f)
    n = 512
    im = light_pool_img(hue, warm, n, warm_a, edge)
    D = 1.3 * r
    p = skia.Paint()
    p.setAlphaf(clamp(gain))
    c.drawImageRect(im, skia.Rect.MakeWH(n, n), skia.Rect.MakeLTRB(x - D, y - D, x + D, y + D), LIN, p)
    ex = skia.Paint(Color=skia.Color(hue[0], hue[1], hue[2], int(255 * edge * clamp(gain))))
    x0, y0, x1, y1 = rect if rect else (0, 0, W, H)
    L, T_, R_, B_ = x - D, y - D, x + D, y + D
    if L > x0:
        c.drawRect(skia.Rect.MakeLTRB(x0, y0, L, y1), ex)
    if R_ < x1:
        c.drawRect(skia.Rect.MakeLTRB(R_, y0, x1, y1), ex)
    if T_ > y0:
        c.drawRect(skia.Rect.MakeLTRB(max(x0, L), y0, min(x1, R_), T_), ex)
    if B_ < y1:
        c.drawRect(skia.Rect.MakeLTRB(max(x0, L), B_, min(x1, R_), y1), ex)


# ═════════════════════════════ Kibirler: eşya sprite'ları + odun yığını ═════════════════════════════
_ITEMS = {}
ITEM_KINDS = ["mirror", "cards", "dice", "wig", "lute"]


def item_sprite(kind):
    """Kibir eşyası (ayna, iskambil, zar, peruk, çalgı): 112×112 sprite (ortada), mürekkep dış hatlı. Dönüş: skia.Image."""
    im = _ITEMS.get(kind)
    if im is not None:
        return im
    fr = sk.Frame(112, 112)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    c.translate(56, 56)
    ink = lambda a=200, w=2.0: skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(INK, a), StrokeJoin=skia.Paint.kRound_Join)  # noqa: E731
    if kind == "mirror":
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-6, 22, 6, 52), 5, 5), _pt("#D8A63A"))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-6, 22, 6, 52), 5, 5), ink(190, 1.6))
        c.drawOval(skia.Rect.MakeLTRB(-28, -46, 28, 28), _pt("#D8A63A"))
        sh = skia.GradientShader.MakeLinear([(-24, -40), (24, 22)], [C("#F2FAFF"), C("#9CC4DC"), C("#6C98B8")], [0.0, 0.55, 1.0])
        c.drawOval(skia.Rect.MakeLTRB(-22, -40, 22, 22), skia.Paint(AntiAlias=True, Shader=sh))
        c.drawLine(-12, -28, 6, -6, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=C("#FFFFFF", 190), StrokeCap=skia.Paint.kRound_Cap))
        c.drawOval(skia.Rect.MakeLTRB(-28, -46, 28, 28), ink(210, 2.2))
        c.drawOval(skia.Rect.MakeLTRB(-22, -40, 22, 22), ink(130, 1.2))
    elif kind == "cards":
        for ang, off, col in ((-22, -16, "#F2EBD9"), (0, 0, "#F6EFDD"), (20, 16, "#F2EBD9")):
            c.save()
            c.translate(off, 14)
            c.rotate(ang)
            rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-19, -46, 19, 8), 4, 4)
            c.drawRRect(rr, _pt(col))
            c.drawRRect(rr, ink(200, 1.8))
            c.restore()
        # ön kart: sinabar kupa ve siyah maça
        c.save()
        c.translate(16, 14)
        c.rotate(20)
        c.drawCircle(-5, -26, 6.5, _pt("#B3361F"))
        c.drawCircle(5, -26, 6.5, _pt("#B3361F"))
        c.drawPath(sk.poly_path([(-11.5, -22), (11.5, -22), (0, -8)]), _pt("#B3361F"))
        c.restore()
    elif kind == "dice":
        for (ox, oy, rot_) in ((-12, 10, -12), (16, -6, 16)):
            c.save()
            c.translate(ox, oy)
            c.rotate(rot_)
            s_ = 25
            c.drawPath(sk.poly_path([(-s_, -s_ + 8), (-s_ + 9, -s_ - 5), (s_ + 9, -s_ - 5), (s_, -s_ + 8)]), _pt("#FFFFFF"))      # üst yüz
            c.drawPath(sk.poly_path([(s_, -s_ + 8), (s_ + 9, -s_ - 5), (s_ + 9, s_ - 5), (s_, s_)]), _pt("#CBC3AE"))               # yan yüz
            c.drawRect(skia.Rect.MakeLTRB(-s_, -s_ + 8, s_, s_), _pt("#F4EEDC"))
            INKR(c, -s_, -s_ + 8, s_, s_, 2.0, 210)
            INKP(c, sk.poly_path([(-s_, -s_ + 8), (-s_ + 9, -s_ - 5), (s_ + 9, -s_ - 5), (s_ + 9, s_ - 5), (s_, s_)], False), 2.0, 200)
            for (px, py) in ((-13, -3), (13, -3), (0, 12), (-13, 22 - 6), (13, 22 - 6)) if ox < 0 else ((-12, 0), (12, 0), (0, 12), (-12, 22 - 8), (12, 22 - 8)):
                c.drawCircle(px, py - 2, 3.6, _pt(INK, 235))
            c.restore()
    elif kind == "wig":
        rs = _RS(7)
        circles = []
        for i in range(22):
            a_ = rs.uniform(-math.pi, 0)
            rr = rs.uniform(18, 33)
            circles.append((math.cos(a_) * rs.uniform(16, 28) * 1.3, math.sin(a_) * 26 + 6, rr))
        circles += [(-30, 26, 16), (30, 26, 16), (-34, 40, 12), (34, 40, 12), (0, 8, 28)]
        for (cx_, cy_, rr) in circles:                                                                   # mürekkep altlık
            c.drawCircle(cx_, cy_, rr + 2.2, _pt(INK, 215))
        for i, (cx_, cy_, rr) in enumerate(circles):
            c.drawCircle(cx_, cy_, rr, _pt(mix("#6A4426", "#B88A58", (i % 5) / 6.0)))
            c.drawArc(skia.Rect.MakeLTRB(cx_ - rr * 0.6, cy_ - rr * 0.6, cx_ + rr * 0.6, cy_ + rr * 0.6), 200, 120, False, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, Color=C("#3A2410", 150)))
    else:                                                                                                  # lute
        c.save()
        c.rotate(-28)
        c.drawRect(skia.Rect.MakeLTRB(-4.5, -58, 4.5, -8), _pt("#4A2E18"))
        c.drawPath(sk.poly_path([(-6, -58), (-6, -70), (14, -76), (14, -64)]), _pt("#4A2E18"))
        body = skia.Path()
        body.moveTo(0, -12)
        body.cubicTo(-30, -12, -34, 30, 0, 44)
        body.cubicTo(34, 30, 30, -12, 0, -12)
        c.drawPath(body, _pt("#C58A44"))
        sh2 = skia.GradientShader.MakeLinear([(-30, 0), (30, 0)], [C("#FFFFFF", 70), C("#FFFFFF", 0), C("#1A1008", 60)], [0.0, 0.4, 1.0])
        c.drawPath(body, skia.Paint(AntiAlias=True, Shader=sh2))
        c.drawPath(body, ink(215, 2.3))
        c.drawCircle(0, 16, 8, _pt("#2A1A0C"))
        c.drawCircle(0, 16, 12, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0, Color=C("#6A4426", 230)))
        for sx_ in (-2.0, 0.0, 2.0):
            c.drawLine(sx_, -12, sx_ * 1.4, 36, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#EDE0B8", 210)))
        c.restore()
    im = _ITEMS[kind] = fr.surf.makeImageSnapshot()
    return im


def pyre(c, x, y, w, h, T=None, seed=1, tiers=6, loose=False, depth=0.0):
    """Odun yığını (basamaklı piramit; loose=True: dağınık odun/çalı yığını, çıkıntılı dallar). x orta, y zemin. Dönüş: eşya yuvaları [(x,y)] (alttan üste)."""
    T = T or CT.Tint("day")
    rs = _RS(seed)
    slots = []
    wood = ["#6A4A2C", "#7A5A36", "#58391F", "#8A6840"]
    th = h / tiers
    for ti in range(tiers):
        tw = w * (1.0 - ti * (0.88 / tiers)) * (0.97 + 0.03 * rs.rand())
        yb = y - ti * th
        nlog = max(2, int(tw / (th * 0.9)))
        for li in range(nlog + 1):
            lx = x - tw / 2 + (li + 0.5 * (ti % 2)) * tw / nlog
            if lx > x + tw / 2 + 2:
                continue
            col = wood[rs.randint(len(wood))]
            r_ = th * 0.52
            c.drawOval(skia.Rect.MakeLTRB(lx - r_ * 0.9, yb - th * 1.02, lx + r_ * 0.9, yb), _pt(T(col, depth)))
            c.drawOval(skia.Rect.MakeLTRB(lx - r_ * 0.9, yb - th * 1.02, lx + r_ * 0.9, yb), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 170)))
            c.drawOval(skia.Rect.MakeLTRB(lx - r_ * 0.45, yb - th * 0.78, lx + r_ * 0.45, yb - th * 0.26), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#3A2410", 120)))
        # üst yüzey boyunca eşya yuvaları
        for si in range(3 if ti > 0 else 4):
            sx_ = x + (si - (1 if ti > 0 else 1.5)) * tw * 0.26 + rs.uniform(-6, 6)
            slots.append((sx_, yb - th * 0.92 - 6))
    if loose:
        for i in range(int(w / 9)):
            ax = x + rs.uniform(-0.5, 0.5) * w * 0.9
            ay = y - rs.uniform(0.1, 0.95) * h
            ang = rs.uniform(-0.9, 0.9)
            L = rs.uniform(30, 90)
            c.drawLine(ax, ay, ax + math.sin(ang) * L, ay - math.cos(ang) * L * 0.6, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=rs.uniform(2.0, 4.5), Color=C(wood[i % 4], 245), StrokeCap=skia.Paint.kRound_Cap))
    # orta direk
    R(c, x - 6, y - h * 1.18, x + 6, y - h * 0.7, T("#5A3A20", depth))
    INKR(c, x - 6, y - h * 1.18, x + 6, y - h * 0.7, 1.2, 160)
    return slots


def gallows_silhouette(c, x, y, h, col="#12100E", a=250):
    """Darağacı SİLUETİ (yalnız ahşap çatı: dikme + yatay kiriş + payanda; beden/ip/ceset YOK)."""
    p = skia.Paint(AntiAlias=True, Color=C(col, a))
    w = h * 0.045
    c.drawRect(skia.Rect.MakeLTRB(x - w, y - h, x + w, y), p)                       # dikme
    c.drawRect(skia.Rect.MakeLTRB(x - w, y - h - w * 0.2, x + h * 0.42, y - h + w * 1.6), p)   # kiriş
    c.drawPath(sk.poly_path([(x + w, y - h * 0.72), (x + w + h * 0.20, y - h + w * 1.6), (x + w + h * 0.20 - w * 1.1, y - h + w * 1.6), (x + w, y - h * 0.72 + w * 1.6)]), p)   # payanda
    c.drawRect(skia.Rect.MakeLTRB(x - w * 2.6, y - h * 0.05, x + w * 2.6, y), p)    # kaide


# ═════════════════════════════ ortak: bayrak, figür sarmalayıcıları, kamera ═════════════════════════════
def flag_pennant(c, x, y, t, L=44.0, hgt=16.0, color="#B3301F", seed=0, wind=1.0):
    """Sallanan kırlangıç kuyruklu flama (x,y = direğe bağlandığı nokta, sağa doğru uzanır)."""
    pts_t, pts_b = [(x, y)], [(x, y + hgt)]
    n = 9
    for k in range(1, n + 1):
        u = k / n
        w = math.sin(t * 4.6 * wind - u * 3.4 + seed) * 4.8 * u
        pts_t.append((x + u * L, y + w))
        pts_b.append((x + u * L, y + hgt + w * 1.1))
    pts = pts_t + [(x + L * 0.80, y + hgt * 0.5 + math.sin(t * 4.6 * wind - 3.0 + seed) * 3)] + pts_b[::-1]
    path = sk.poly_path(pts)
    c.drawPath(path, _pt(color))
    c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 200)))
    c.drawCircle(x + L * 0.20, y + hgt * 0.5 + math.sin(t * 4.6 * wind - 0.7 + seed), 2.6, _pt("#F2E6C2", 235))


_DARK_CF = {}


def dark_cf(col="#14101A"):
    """Siluet rengi (figüre uygulanan renk filtresi): çizim kitine `cf=` olarak verilir."""
    cf = _DARK_CF.get(col)
    if cf is None:
        cf = _DARK_CF[col] = skia.ColorFilters.Blend(C(col), skia.BlendMode.kSrcATop)
    return cf


def ease_out(u):
    u = clamp(u)
    return 1 - (1 - u) ** 3


def ease_io(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


def _anchor(cx, a, default=0.0):
    """Zaman çapasını yerel saniyeye çevir (çözülemezse sayı ya da varsayılan)."""
    if a is None:
        return default
    if isinstance(a, (int, float)):
        return float(a)
    try:
        return float(cx.at(a))
    except Exception:   # noqa: BLE001
        return default


def _cam_mod(spec, u):
    """`cam=` ön ayarını varsayılan yolun üstüne uygula: (dx, dy, zoom çarpanı)."""
    if not spec or isinstance(spec, str):
        return 0.0, 0.0, 1.0
    try:
        k = spec[0]
        if k == "push":
            return 0.0, 0.0, 1.0 + float(spec[1]) * u
        if k == "pull":
            return 0.0, 0.0, 1.0 + float(spec[1]) * (1.0 - u)
        if k == "pan":
            sg = 1.0 if str(spec[1]).lower() in ("r", "right", "1") else -1.0
            return sg * float(spec[2]) * u, 0.0, 1.0
        if k == "crane":
            sg = -1.0 if str(spec[1]).lower() == "up" else 1.0
            return 0.0, sg * float(spec[2]) * u, 1.0
    except Exception:   # noqa: BLE001
        pass
    return 0.0, 0.0, 1.0


def draw_actor(ctx, a, ground=YG):
    """`actors=[dict(kind, x0|x, y, h, dir, speed, action, seed, prop, flag, phase, t0, t1, cf)]` öğesini çiz (dünya koordinatı; speed>0 → yürür)."""
    f, t = ctx.f, ctx.t
    t0 = a.get("t0", 0.0)
    tt = t - t0
    if tt < 0 and not a.get("early", False):
        return
    d = a.get("dir", 1)
    sp = a.get("speed", 0.0)
    x = a.get("x0", a.get("x", 0.0)) + d * sp * tt
    y = a.get("y", ground)
    h = a.get("h", 190)
    cf = a.get("cf")
    if isinstance(cf, str):
        cf = dark_cf(cf)
    alpha_g = a.get("alpha", 1.0)
    gt = a.get("gate")
    if gt:                                                          # geçide (androne) girer: derinleşir (küçülür, yukarı kayar) ve kararıp kaybolur
        u = clamp((x - (gt[0] - gt[1] / 2 + 60)) / (gt[1] * 0.80))
        if u > 0:
            h = h * (1.0 - 0.30 * u)
            y = y - 22 * u
            alpha_g = alpha_g * (1.0 - clamp((u - 0.45) / 0.55))
            if alpha_g <= 0.02:
                return
    act = a.get("action", "walk" if sp > 1 else "idle")
    fl = a.get("flag")
    stil = a.get("stil") or {}
    if act in ("walk", "idle"):
        FA.walker(f, a.get("kind", "halk"), x, y, h, t, speed=sp if act == "walk" else 0.0, dir=d, phase=a.get("phase", 0.0), seed=a.get("seed", 0), alpha=alpha_g, cf=cf, prop=a.get("prop"), flag=fl, **stil)
    else:
        kw = {k: v for k, v in a.items() if k in ("t0", "dur", "depth", "target", "rise_at", "energy", "amount", "hop", "mode", "period", "high")}
        kw.pop("t0", None)
        FA.actor(f, a.get("kind", "halk"), x, y, h, tt, action=act, dir=d, seed=a.get("seed", 0), phase=a.get("phase", 0.0), alpha=alpha_g, cf=cf, prop=a.get("prop"), **stil, **kw)


def silhouettize(img, col="#14101A", detail=0.30):
    """Sprite'ı tek renkli siluete çevir (alfa korunur; `detail`: parlaklığa bağlı çok hafif iç doku → kıvrım/kenar ipucu). FA'nın baş/ayakkabı sprite'ları cf'yi
    yok saydığı için renk filtresi yerine piksel düzeyinde yapılır (bir kez, pişirmede)."""
    arr = img.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kUnpremul_AlphaType).astype(np.float32)
    base = np.array(sk.rgb(col), np.float32)
    lum = arr[..., :3].mean(axis=2, keepdims=True) / 255.0
    arr[..., :3] = np.clip(base[None, None, :] + (lum - 0.35) * 70.0 * detail, 0, 255)
    return sk.np_to_image(np.ascontiguousarray(arr.astype(np.uint8)))


_SIL = {}


def sil_sprite(kind, seed, h, pose="stand", col="#14101A"):
    """Önceden pişirilmiş siluet figür (renk filtresi bir kez uygulanır; kare başına tek blit). Dönüş: (img, ox, oy, ölçek) — ayak (ox,oy)."""
    key = (kind, seed, int(h), pose, col)
    r = _SIL.get(key)
    if r is None:
        k = 1.3
        hh = h * k
        fr = sk.Frame(int(hh * 0.95) + 20, int(hh * 1.25) + 20)
        fr.clear(skia.ColorTRANSPARENT)
        ox, oy = fr.w / 2.0, fr.h - 10.0
        old_hint = FA.SCALE_HINT
        FA.set_scale_hint(1.0)
        if pose == "cheer":
            FA.actor(fr, kind, ox, oy, hh, 0.9, action="cheer", dir=1, seed=seed, phase=0.3, amount=1.0, hop=0.0)
        else:
            FA.walker(fr, kind, ox, oy, hh, 0.0, speed=0.0, dir=1, seed=seed)
        FA.set_scale_hint(old_hint)
        r = _SIL[key] = (silhouettize(fr.surf.makeImageSnapshot(), col), ox, oy, 1.0 / k)
    return r


def draw_sil(c, kind, seed, x, y, h, face, t, phase=0.0, pose="stand", col="#14101A", sway=1.0):
    """Siluet figürü çiz: ayak çevresinde hafif sallanma + nefes (cheer pozunda zıplama)."""
    img, ox, oy, s = sil_sprite(kind, seed, h, pose, col)
    c.save()
    hop = abs(math.sin(t * 3.2 + phase * 6.28)) * h * 0.04 if pose == "cheer" else 0.0
    c.translate(x, y - hop)
    c.rotate(math.sin(t * 0.7 + phase * 6.28) * 1.1 * sway)
    c.scale(face * s, s * (1.0 + 0.012 * math.sin(t * 1.6 + phase * 3.0)))
    c.drawImage(img, -ox, -oy, LIN)
    c.restore()


RING_ROWS = ((YG - 62, 126), (YG - 38, 139), (YG - 14, 152), (YG + 10, 166), (YG + 34, 182), (YG + 58, 198))


def ring_members(cx0, n, seed, side_rx=(240, 820), rows=RING_ROWS, behind=5, front=5):
    """Çevrede halka olan kalabalık üyeleri (deterministik): merkeze (cx0) bakar. Dönüş: y'ye göre sıralı liste; row: 0 arka … 5 ön."""
    rs = _RS(seed * 31 + 7)
    kinds = ["halk", "tuccar", "soylu", "soylu_f", "cocuk", "halk", "rahip", "banker", "kesis", "halk", "denizci", "halk"]
    out = []
    for i in range(n):
        if i < behind:
            side, dx, row = (1 if i % 2 else -1), rs.uniform(30, 180), rs.randint(0, 2)
        elif i < behind + front:
            side, dx, row = (1 if i % 2 else -1), rs.uniform(130, 320), 4 + (i % 2)
        else:
            side, dx, row = (1 if rs.rand() < 0.5 else -1), rs.uniform(*side_rx), rs.randint(0, 6)
        yb, hh = rows[row]
        k = kinds[rs.randint(len(kinds))]
        if k == "cocuk":
            hh *= 0.82
        out.append(dict(x=cx0 + side * dx, y=yb + rs.uniform(-5, 5), h=hh * rs.uniform(0.94, 1.06), kind=k, seed=int(rs.randint(0, 40)), phase=rs.rand(), face=-side, row=row,
                        act=("cheer" if rs.rand() < 0.40 else ("talk" if rs.rand() < 0.55 else "idle")), amt=rs.uniform(0.55, 1.0), hop=rs.uniform(0.2, 0.7), off=rs.uniform(-1.0, 1.0)))
    out.sort(key=lambda m: m["y"])
    return out


def draw_member(ctx, m, cheer_k=1.0, cf=None, alpha=1.0, x=None):
    """Tek halka üyesi: cheer (kollar havada, cheer_k oranında) | talk | bekleme."""
    f, t = ctx.f, ctx.t
    act = m["act"]
    if act == "cheer" and cheer_k < 0.18:
        act = "talk"
    xx = m["x"] if x is None else x
    if act == "cheer":
        FA.actor(f, m["kind"], xx, m["y"], m["h"], t, action="cheer", dir=m["face"], seed=m["seed"], phase=m["phase"], amount=m["amt"] * cheer_k, hop=m["hop"], cf=cf, alpha=alpha)
    elif act == "talk":
        FA.actor(f, m["kind"], xx, m["y"], m["h"], t, action="talk", dir=m["face"], seed=m["seed"], phase=m["phase"], energy=0.7, cf=cf, alpha=alpha)
    else:
        FA.walker(f, m["kind"], xx, m["y"], m["h"], t, speed=0.0, dir=m["face"], phase=m["phase"], seed=m["seed"], cf=cf, alpha=alpha)


def draw_ring(ctx, members, rows, cheer_k=1.0, t_gate=None, cf=None, xa=None, xb=None, alpha=1.0):
    """halka üyelerinin belirtilen sıralarını çiz (cheer_k: coşku düzeyi 0..1)."""
    for m in members:
        if m["row"] not in rows:
            continue
        if xa is not None and (m["x"] < xa - 160 or m["x"] > xb + 160):
            continue
        draw_member(ctx, m, cheer_k, cf, alpha)


_LIGHT_CF = {}


def lit_cf(tod):
    """Ateş ışığı altındaki ön figürler için sıcak/koyu çarpan (grade sonrası çizilen figürler arka planla uyumlu görünsün)."""
    cf = _LIGHT_CF.get(tod)
    if cf is None:
        col = {"day": "#FFFFFF", "dusk": "#E4C8B0", "night": "#D8B890"}[tod]
        cf = _LIGHT_CF[tod] = skia.ColorFilters.Blend(C(col), skia.BlendMode.kModulate)
    return cf


# ═════════════════════════════ MEYDAN (Piazza della Signoria) ═════════════════════════════
MED_X0, MED_W, MED_H = 60, 1000, 318            # sol: Medici tarzı palazzo (kalkan yalnız act="palle")
PV_X0, PV_W, PV_H = 1250, 1300, 336             # Palazzo Vecchio bloğu
LOG_X0, LOG_X1, LOG_H = 2650, 3910, 252         # Loggia
GEN_X0, GEN_W, GEN_H = 3990, 1120, 286          # sağ: genel palazzo
PILE_X = 1900                                   # yığın merkezi (Kibirler / odun) — V6→V7 eşleşmeli kesme için SABİT
PILE_Y = YG + 6


def _pile_sprite(kind="ates", seed=3):
    """Yığın sprite'ı (önbellekli): kind='ates' basamaklı piramit | 'odun' dağınık odun. Dönüş: (img, ox, oy, slots[(x,y) sprite uzayı])."""
    key = ("pile", kind, seed)
    r = _ITEMS.get(key)
    if r is None:
        w, h = (380, 250) if kind == "ates" else (420, 190)
        fr = sk.Frame(int(w + 160), int(h * 1.9 + 80))
        fr.clear(skia.ColorTRANSPARENT)
        ox, oy = fr.w / 2.0, fr.h - 30.0
        slots = pyre(fr.c, ox, oy, w, h, CT.Tint("day"), seed=seed, tiers=6, loose=(kind != "ates"))
        r = _ITEMS[key] = (fr.surf.makeImageSnapshot(), ox, oy, [(sx - ox, sy - oy) for sx, sy in slots])
    return r




class Meydan(SWorld):
    name = "sehir_meydan"
    PW = 5200
    _draw_sky = PN.Florence._draw_sky
    _draw_hills = PN.Florence._draw_hills
    dyn_sky = PN.Florence.dyn_sky

    def build(self):
        PW = self.PW
        cam_span = PW - W

        def Lw(f):
            return int(W + cam_span * f + 500)
        self.cloud_seed = 4
        self.G_PV = palazzo_geom("vecchio", PV_X0, YG, PV_W, PV_H, door=0.0, tower_x=0.60)
        self.G_MED = palazzo_geom("medici", MED_X0, YG, MED_W, MED_H, door=0.0)
        self.G_GEN = palazzo_geom("generic", GEN_X0, YG, GEN_W, GEN_H, door=0.0)
        rr = _RS(5)
        self.city_houses = []
        x = -40
        while x < Lw(0.30) + 60:
            bw, bh = rr.uniform(34, 74), rr.uniform(30, 70)
            self.city_houses.append((x, bw, bh, int(rr.randint(1, 10 ** 6)), 0.46, 0))
            x += bw + rr.uniform(-4, 8)
        x = 20
        while x < Lw(0.30) + 60:
            bw, bh = rr.uniform(40, 80), rr.uniform(34, 76)
            self.city_houses.append((x, bw, bh, int(rr.randint(1, 10 ** 6)), 0.26, 20))
            x += bw + rr.uniform(-6, 6)
        self.mid_houses = []
        x = -60
        rr = _RS(17)
        while x < Lw(0.62) + 60:
            bw, bh = rr.uniform(110, 190), rr.uniform(230, 360)
            self.mid_houses.append((x, bw, bh, int(rr.randint(1, 10 ** 6))))
            x += bw + rr.uniform(-10, 14)
        self.layer("sky", 0.05, Lw(0.05), self._draw_sky, opaque=True, scale=0.5, wear=3, loss=0.5, yr=(0, 700))
        self.layer("hills", 0.14, Lw(0.14), self._draw_hills, scale=0.5, wear=2, yr=(330, 800))
        self.layer("city", 0.30, Lw(0.30), self._draw_city, wear=2, yr=(60, 620))
        self.layer("mid", 0.62, Lw(0.62), self._draw_mid, wear=2, yr=(160, 860))
        self.layer("main", 1.0, PW, self._draw_main, wear=4)
        self.ring = ring_members(PILE_X, 30, 4)
        self.pile = _pile_sprite("ates")
        self.pile_odun = _pile_sprite("odun", 5)
        self.fgs = [(-560, 1.0), (-300, 0.85), (-110, 1.05), (210, 0.95), (440, 1.1), (640, 0.9)]
        self.win_order = list(_RS(9).permutation(len(self.G_PV["wins"])))

    # ── kamera yolları (act'e göre) ──
    def default_cams(self, act=None, p=None):
        if act == "ates":                                    # yığının etrafında yarım daire (paralaks) → yığın merkezinde SABİT (sonraki odun çekimi aynı noktadan başlar)
            return [(0.0, (PILE_X - 560, 30, 1.0)), (0.80, (PILE_X - 40, 30, 1.13)), (1.0, (PILE_X, 30, 1.15))]
        if act == "odun":
            return [(0.0, (PILE_X, 30, 1.15)), (1.0, (PILE_X + 20, 30, 1.19))]
        if act == "palle":
            return [(0.0, (2200, 40, 1.0)), (0.42, (1800, 36, 1.0)), (0.72, (1150, 96, 1.14)), (1.0, (640, 104, 1.40))]
        if act == "pencere":                                 # ağır pull: cepheye yakın → geri
            return [(0.0, (PV_X0 + PV_W * 0.55, 150, 1.34)), (1.0, (PV_X0 + PV_W * 0.52, 80, 1.0))]
        if act == "kalabalik":                               # kalabalığın içinde yavaş itme (kabaran halk)
            return [(0.0, (PV_X0 + PV_W * 0.50, 70, 1.0)), (1.0, (PV_X0 + PV_W * 0.50 + (60 if (p or {}).get("dir", "l") in ("r", 1) else -60), 50, 1.10))]
        return [(0.0, (1400, 0, 1.0)), (1.0, (2600, 0, 1.0))]

    def stack(self, ctx):
        return [("L", "sky"), ("D", "dyn_sky", 0.05), ("L", "hills"), ("L", "city"), ("D", "dyn_city", 0.30), ("L", "mid"), ("D", "dyn_mid", 0.62), ("L", "main"), ("D", "dyn_main", 1.0), ("D", "dyn_front", 1.38)]

    # ── katman boyaları ──
    def _draw_city(self, fr, xa, xb):
        c = fr.c
        T = self.T
        night = self.tod == "night"
        wins = []
        for (x, bw, bh, sd, dep, dy) in self.city_houses:
            if x + bw < xa - 60 or x > xb + 60:
                continue
            rs = _RS(sd)
            CT.draw_house(c, x, PN.Y_FAR + dy + (rs.rand() * 8 - 4), bw, bh, rs, T, dep, wins)
        base = PN.Y_FAR
        XD = 880                                                                 # Duomo grubu (sol-uzak)
        if xa - 900 < XD < xb + 900:
            c.save()
            c.translate(XD, base)
            c.scale(1.18, 1.18)
            c.translate(-XD, -base)
            CT.draw_nave(c, XD + 60, XD + 560, base + 4, 118, T, 0.16)
            CT.draw_dome(c, XD, base - 100, 200, 124, 44, 70, T, 0.12)
            CT.draw_campanile(c, XD + 196, base + 4, 50, 244, T, 0.12)
            c.restore()
            for tx, th in ((XD - 760, 150), (XD + 1020, 142), (XD + 1500, 176), (XD + 2100, 134), (XD + 2700, 160)):
                CT.draw_tower(c, tx, base, 30, th, T, 0.35, spire=(tx == XD + 1500))
        if night or self.tod == "dusk":
            PN._lit_boxes(c, _RS(int(xa) % 997 + 1), [b for b in wins], True, 0.38 if night else 0.18)

    def _draw_mid(self, fr, xa, xb):
        c = fr.c
        T = self.T
        wins = []
        for (x, bw, bh, sd) in self.mid_houses:
            if x + bw < xa - 40 or x > xb + 40:
                continue
            rs = _RS(sd)
            CT.draw_house(c, x, YG - 60, bw, bh, rs, T, 0.20, wins)
            if rs.rand() < 0.45:                                                  # baca
                cxh = x + bw * rs.uniform(0.2, 0.75)
                R(c, cxh, YG - 60 - bh - bw * 0.40 - 22, cxh + 12, YG - 60 - bh - bw * 0.20, T("#9C6A4A", 0.2))
        if self.tod != "day":
            PN._lit_boxes(c, _RS(int(xa) % 991 + 5), wins, True, 0.42 if self.tod == "night" else 0.22)

    def _draw_main(self, fr, xa, xb):
        c = fr.c
        T = self.T
        PN.draw_pavement(c, xa, xb, YG - 8, 960, T, seed=int(xa) // 1024)
        # sokak aralıkları: bina araları (gölgeli duvar)
        for (g0, g1) in ((MED_X0 + MED_W - 4, PV_X0 + 4), (PV_X0 + PV_W - 4, LOG_X0 + 4), (LOG_X1 - 4, GEN_X0 + 4)):
            if g1 < xa - 40 or g0 > xb + 40:
                continue
            narrow_house(c, g0, g1, YG - 8, 330 + (int(g0) % 5) * 12, T, seed=int(g0) % 97)
        if xa < MED_X0 + MED_W + 80 and xb > MED_X0 - 80:
            palazzo_front(c, MED_X0, YG, MED_W, MED_H, "medici", door=0.0, T=T, seed=21)
        if xa < PV_X0 + PV_W + 80 and xb > PV_X0 - 80 or (xb > self.G_PV["tower"][0] - 200 and xa < self.G_PV["tower"][0] + 200):
            palazzo_front(c, PV_X0, YG, PV_W, PV_H, "vecchio", door=0.0, T=T, seed=31)
        if xa < LOG_X1 + 80 and xb > LOG_X0 - 80:
            loggia(c, LOG_X0, LOG_X1, YG - 6, LOG_H, T)
        if xa < GEN_X0 + GEN_W + 80 and xb > GEN_X0 - 80:
            palazzo_front(c, GEN_X0, YG, GEN_W, GEN_H, "generic", door=0.0, T=T, seed=41)
        # meşale demirleri (cephe)
        for tx in (self.G_PV["door"][0] - 120, self.G_PV["door"][0] + 120, PV_X0 + PV_W * 0.62, PV_X0 + PV_W * 0.86):
            if xa - 40 < tx < xb + 40:
                torch_bracket(c, tx, YG - 170, T)
        # kaldırım izleri / taş sıraları ve ufak eşya (varil, çuval)
        rs = _RS(77)
        for i in range(34):
            x = rs.uniform(0, self.PW)
            if not (xa - 30 < x < xb + 30):
                continue
            y = YG + rs.uniform(40, 100)
            OVAL(c, x, y, rs.uniform(10, 26), rs.uniform(2, 5), "#7A6A48", 90)
        for bx in (MED_X0 + MED_W + 40, PV_X0 - 60, GEN_X0 - 50, LOG_X1 + 30):
            if xa - 60 < bx < xb + 60:
                for j in range(2):
                    px, py = bx + j * 42, YG - 2
                    OVAL(c, px, py - 26, 20, 28, T("#7A5230", 0.0), 255)
                    c.drawOval(skia.Rect.MakeLTRB(px - 20, py - 54, px + 20, py + 2), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 170)))
                    for hy in (-38, -14):
                        c.drawLine(px - 19, py + hy, px + 19, py + hy, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=C("#2A2622", 200)))

    # ── dinamik ──
    def dyn_city(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        FA.atmo_birds(c, t, 9, 1.0, xa, xb, 200, 380, speed=22.0, night=ctx.night, seed=3, size=0.8)
        rs = _RS(31)
        for i in range(10):
            x = 300 + i * 330 + rs.uniform(-60, 60)
            if x < xa - 60 or x > xb + 60:
                continue
            for k in range(5):
                ph = (t * 0.16 + k / 5.0 + i * 0.37) % 1.0
                FA._puff(c, x + math.sin(ph * 6 + i) * 8 * ph, PN.Y_FAR - 56 - ph * 90, 5 + 14 * ph, 0.26 * (1 - ph), "#C8C0B4" if not ctx.night else "#6A7A9A")

    def dyn_mid(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        rs = _RS(61)
        for i in range(16):                                                       # bacalardan ince duman
            x = -40 + i * 300 + rs.uniform(-60, 60)
            if x < xa - 60 or x > xb + 60:
                continue
            for k in range(4):
                ph = (t * 0.18 + k / 4.0 + i * 0.29) % 1.0
                FA._puff(c, x + math.sin(ph * 5 + i) * 6 * ph, YG - 60 - 400 - ph * 80, 4 + 9 * ph, 0.2 * (1 - ph), "#C8C0B4" if not ctx.night else "#6A7A9A")

    def _banners(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        # Loggia terasından sarkan kırmızı-krem bayraklar; Palazzo Vecchio kulesi flaması
        top = YG - 6 - LOG_H - LOG_H * 0.24 - 10
        for i, lx in enumerate((LOG_X0 + 120, LOG_X0 + 640, LOG_X1 - 160)):
            if lx < xa - 120 or lx > xb + 60:
                continue
            PN.draw_cloth(c, lx, top, "#B3361F", "#EDE4CC", 64, 150, t, ph=i * 1.7, wind=1.0, kind="tente", seed=70 + i)
            LINE(c, lx - 4, top, lx + 72, top, "#4A3220", 2.6)
        fl = self.G_PV.get("flag")
        if fl is not None and xa - 80 < fl[0] < xb + 80:
            flag_pennant(c, fl[0] + 1.0, fl[1] + 3, t, 48.0, 17.0, "#B3301F")

    def dyn_main(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        p = ctx.p
        act = p.get("act")
        self._banners(ctx)
        if act == "ates":
            self._act_ates(ctx, back=True)
        elif act == "odun":
            self._act_odun(ctx, back=True)
        elif act == "palle":
            self._act_palle(ctx)
        elif act == "kalabalik":
            self._act_crowd(ctx)
        # kullanıcı figürleri / istasyonlar
        for a_ in (p.get("actors") or []):
            draw_actor(ctx, a_)
        for st in ctx.stations:
            fn = st.get("fn")
            if fn is None:
                continue
            x = st.get("x", 0)
            if x < xa - 700 or x > xb + 700:
                continue
            ctx.st = st
            fn(ctx, st)
        if act == "ates":
            self._act_ates(ctx, back=False)
        elif act == "odun":
            self._act_odun(ctx, back=False)

    def dyn_front(self, ctx):
        """Ön plan (paralaks 1,38): ateş başında arkadan görünen siluet başlar/omuzlar (kukuleta, bere, çıplak baş) — derinlik + çerçeve; ateşe bakan kenarda sıcak ışık."""
        act = ctx.p.get("act")
        if act not in ("ates", "odun"):
            return
        c, t = ctx.c, ctx.t
        kf = ctx.fire_k if act == "ates" else ctx.coal * 0.8
        base = W / 2 + (PILE_X - W / 2) * 1.38
        for i, (dx, sc) in enumerate(self.fgs):
            x = base + dx * 1.25
            if x < ctx.xa - 150 or x > ctx.xb + 150:
                continue
            sway = math.sin(t * 0.6 + i * 1.9) * 2.5
            r_ = 27 * sc
            hy = 806 + (i % 3) * 12 + sway * 0.3
            col = "#0C0A0E"
            kind = i % 3
            sh = skia.Path()                                            # omuzlar (boyun daralır, omuz eğimi)
            sh.moveTo(x - r_ * 2.5, 1000)
            sh.cubicTo(x - r_ * 2.6, hy + r_ * 2.1, x - r_ * 1.6, hy + r_ * 1.15, x - r_ * 0.55, hy + r_ * 0.95)
            sh.lineTo(x - r_ * 0.45, hy + r_ * 0.30)
            sh.lineTo(x + r_ * 0.45, hy + r_ * 0.30)
            sh.lineTo(x + r_ * 0.55, hy + r_ * 0.95)
            sh.cubicTo(x + r_ * 1.6, hy + r_ * 1.15, x + r_ * 2.6, hy + r_ * 2.1, x + r_ * 2.5, 1000)
            sh.close()
            c.drawPath(sh, _pt(col, 255))
            c.drawOval(skia.Rect.MakeLTRB(x - r_ * 0.86 + sway, hy - r_ * 1.0, x + r_ * 0.86 + sway, hy + r_ * 0.72), _pt(col, 255))
            if kind == 0:                                               # kukuleta
                c.drawPath(sk.poly_path([(x - r_ * 1.15 + sway, hy + r_ * 0.55), (x - r_ * 0.35 + sway, hy - r_ * 1.35), (x + r_ * 0.35 + sway, hy - r_ * 1.35), (x + r_ * 1.15 + sway, hy + r_ * 0.55)]), _pt(col, 255))
            elif kind == 1:                                             # bere
                c.drawOval(skia.Rect.MakeLTRB(x - r_ * 1.15 + sway, hy - r_ * 1.35, x + r_ * 1.05 + sway, hy - r_ * 0.45), _pt(col, 255))
            if kf > 0.05:                                               # ateşe bakan kenarda sıcak ışık
                side = 1 if dx < 0 else -1
                c.drawArc(skia.Rect.MakeLTRB(x - r_ * 0.95 + sway, hy - r_ * 1.05, x + r_ * 0.95 + sway, hy + r_ * 0.75), (-70 if side > 0 else 130), 70, False,
                          skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6, Color=C("#FF9A3A", int(190 * min(1.0, kf)))))
        return

    # ── act: ates (Kibirlerin Yakılması) ──
    def _carriers(self, ctx):
        """Her eşya için bir taşıyıcı: sepet/çuvalla yığına yürür, durur, eşyayı fırlatır; sonra halkaya katılıp coşar. Dönüş: [(y, çizici)] ve eşya kaynakları."""
        t = ctx.t
        out = []
        n = len(ctx.items)
        for i, (t_land, kind, _src) in enumerate(ctx.items):
            side = 1 if i % 2 else -1
            xs = PILE_X + side * (215 + 36 * (i % 4) + 14 * (i % 3))
            y = YG + 10 + (i % 3) * 22 - (i % 5) * 4
            h = 164 + (i % 3) * 9
            v = 112.0 + 8 * (i % 3)
            t_throw = t_land - 0.95
            t_arr = t_throw - 0.40
            x = xs + side * v * max(0.0, t_arr - t)
            ctx.items[i] = (t_land, kind, (xs - side * 4, y - h * 0.66))
            out.append((y, i, x, xs, y, h, v, t_arr, t_throw, side))
        return out

    def _draw_carrier(self, ctx, q, kf):
        f, t = ctx.f, ctx.t
        (y, i, x, xs, _y, h, v, t_arr, t_throw, side) = q
        if x < ctx.xa - 200 or x > ctx.xb + 200:
            return
        kind = ["halk", "tuccar", "soylu", "soylu_f", "halk", "cocuk", "banker", "halk"][i % 8]
        sd = 3 + i * 5
        if t < t_arr:
            FA.walker(f, kind, x, y, h, t, speed=v, dir=-side, phase=(i * 0.173) % 1.0, seed=sd, prop=("basket" if i % 2 else "sack"))
        elif t < t_throw + 0.35:
            FA.walker(f, kind, x, y, h, t, speed=0.0, dir=-side, phase=(i * 0.173) % 1.0, seed=sd, prop=("basket" if i % 2 else "sack"))
        elif kf > 0.2 and i % 2 == 0:
            FA.actor(f, kind, x, y, h, t, action="cheer", dir=-side, seed=sd, phase=(i * 0.173) % 1.0, amount=0.5 + 0.5 * kf, hop=0.4)
        else:
            FA.actor(f, kind, x, y, h, t, action="talk", dir=-side, seed=sd, phase=(i * 0.173) % 1.0, energy=0.8)

    def _act_ates(self, ctx, back=True):
        f, c, t = ctx.f, ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        kf = ctx.fire_k
        ck = 0.35 + 0.65 * kf
        thr = YG + 12
        if back:
            car = self._carriers(ctx)
            figs = [(m["y"], 0, m) for m in self.ring if m["y"] <= thr] + [(q[0], 1, q) for q in car if q[0] <= thr]
            figs.sort(key=lambda q: q[0])
            for (_, kd, o) in figs:
                if kd == 0:
                    if xa - 160 < o["x"] < xb + 160:
                        draw_member(ctx, o, ck)
                else:
                    self._draw_carrier(ctx, o, kf)
            img, ox, oy, slots = self.pile
            c.drawImage(img, PILE_X - ox, PILE_Y - oy, LIN)
            self._items(ctx, slots)
            ctx._car_front = [q for q in car if q[0] > thr]
        # ön sıra (y > eşik) → fx aşamasında, ateşten SONRA çizilir (ateşin önünde durur)

    def _act_ates_front(self, ctx):
        xa, xb = ctx.xa, ctx.xb
        kf = ctx.fire_k
        ck = 0.35 + 0.65 * kf
        cf = None
        thr = YG + 12
        figs = [(m["y"], 0, m) for m in self.ring if m["y"] > thr] + [(q[0], 1, q) for q in getattr(ctx, "_car_front", [])]
        figs.sort(key=lambda q: q[0])
        for (_, kd, o) in figs:
            if kd == 0:
                if xa - 160 < o["x"] < xb + 160:
                    draw_member(ctx, o, ck, cf=cf)
            else:
                self._draw_carrier(ctx, o, kf)

    def _items(self, ctx, slots):
        c, t = ctx.c, ctx.t
        items = ctx.items
        n = len(items)
        burn = clamp((t - ctx.fire_t0 - 0.6) / 4.0) if ctx.fire_t0 is not None else 0.0
        for i, (t_land, kind, src) in enumerate(items):
            sl = slots[min(len(slots) - 1, int(i * len(slots) / max(1, n)))]
            dst = (PILE_X + sl[0], PILE_Y + sl[1] - 14)
            fl = 0.95
            u = (t - (t_land - fl)) / fl
            if u < 0:
                continue
            if u < 1.0:
                e = ease_io(u)
                x = src[0] + (dst[0] - src[0]) * e
                y = src[1] + (dst[1] - src[1]) * e - 240 * 4 * u * (1 - u)
                ang = (i * 57 % 90 - 45) * u + 480 * u * (1 if i % 2 else -1) * (1 - 0.15 * u)
            else:
                x, y = dst
                ang = (i * 57 % 90 - 45) + 480 * (1 if i % 2 else -1)
                y += 3 * math.exp(-(t - t_land) * 7) * math.sin((t - t_land) * 22)
            sc = 0.60 if i % 5 != 4 else 0.68
            c.save()
            c.translate(x, y)
            c.rotate(ang)
            c.scale(sc, sc)
            pt = skia.Paint()
            pt.setAlphaf(1.0 - 0.9 * burn if u >= 1.0 else 1.0)
            c.drawImage(item_sprite(kind), -56, -56, LIN, pt)
            c.restore()

    # ── act: odun (aynı kamera/yığın merkezi; közer→kül; yalnız siluet) ──
    def _act_odun(self, ctx, back=True):
        f, c, t = ctx.f, ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        ck = ctx.coal
        if back:
            for m in self.ring:                                                  # uzak siluet kalabalık (yüz/ayrıntı yok): sallanır, bir kısmı kolunu kaldırır
                if m["row"] >= 4 or m["x"] < xa - 200 or m["x"] > xb + 200:
                    continue
                pose = "cheer" if (m["act"] == "cheer" and math.sin(t * 0.8 + m["phase"] * 6.28) > 0.55) else "stand"
                draw_sil(c, m["kind"], m["seed"], m["x"], m["y"], m["h"], m["face"], t, m["phase"], pose)
            img, ox, oy, slots = self.pile_odun
            c.drawImage(img, PILE_X - ox, PILE_Y - oy, LIN)
            gallows_silhouette(c, PILE_X + 6, PILE_Y - 120, 430, "#0F0D0C", 252)
        else:
            for m in self.ring:
                if m["row"] < 4 or m["x"] < xa - 200 or m["x"] > xb + 200:
                    continue
                draw_sil(c, m["kind"], m["seed"], m["x"], m["y"], m["h"], m["face"], t, m["phase"], "stand")

    # ── act: palle ──
    def _act_palle(self, ctx):
        """act="palle": Medici kalkanı + soldan sağa kabaran Medici kalabalığı (PALLE sancakları) + sağdan sola gelip duran atlılar."""
        c = ctx.c
        medici_shield(c, MED_X0 + MED_W * 0.30, YG - 0.52 * MED_H, MED_H * 0.12, self.T)
        self._act_crowd(ctx)

    def _act_crowd(self, ctx):
        """Kabaran kalabalık (act="palle" ve act="kalabalik"): yürüyüş → durma → coşku; sancaktarlar; (varsa) atlılar sağdan sola yavaşlayıp durur."""
        f, c, t = ctx.f, ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        sg = self._cdir
        dev = self._cdev
        for m in self._palle_crowd:
            tt = t - m["d"]
            if tt < 0:
                continue
            dist = m["x1"] - m["x0"]
            u = clamp(tt / m["T"])
            x = m["x0"] + dist * u * u * (3 - 2 * u)
            v = abs(dist) / m["T"] * 6 * u * (1 - u) if 0 < u < 1 else 0.0
            if x < xa - 200 or x > xb + 200:
                continue
            fl = (dev[0], 0.62, 0.44, dev[1], dev[2]) if (m["flag"] and dev) else None
            if v > 14:
                FA.walker(f, m["kind"], x, m["y"], m["h"], t, speed=v, dir=sg, phase=m["phase"], seed=m["seed"], prop=("pole" if fl else None), flag=fl)
            elif fl:
                FA.walker(f, m["kind"], x, m["y"], m["h"], t, speed=0.0, dir=sg, phase=m["phase"], seed=m["seed"], prop="pole", flag=fl)
            else:
                amt = clamp((tt - m["T"]) / 0.9) * m["amt"]
                if amt > 0.05:
                    FA.actor(f, m["kind"], x, m["y"], m["h"], t, action="cheer", dir=sg, seed=m["seed"], phase=m["phase"], amount=amt, hop=m["hop"])
                else:
                    FA.walker(f, m["kind"], x, m["y"], m["h"], t, speed=0.0, dir=sg, phase=m["phase"], seed=m["seed"])
        # atlılar: sağdan sola dörtnaldan tırısa, yürüyüşe yavaşlar ve DURUR (şiddet yok); toz izi
        for r_ in self._palle_riders:
            tt = t - r_["d"]
            if tt < -0.2:
                continue
            u = clamp(tt / r_["T"])
            dist = r_["x1"] - r_["x0"]
            x = r_["x0"] + dist * (1 - (1 - u) ** 2)
            v = abs(dist) * 2 * (1 - u) / r_["T"] if u < 1 else 0.0
            if x < xa - 320 or x > xb + 320:
                continue
            g_ = "gallop" if v > 300 else ("trot" if v > 120 else "walk")
            FA.rider(f, x, r_["y"], r_["h"], t, speed=v, gait=g_, dir=-1, seed=r_["seed"], phase=r_["phase"])
            if v > 50:
                for k in range(5):
                    ph = (t * 1.3 + k / 5.0 + r_["phase"]) % 1.0
                    _blit_dot(c, _soft_dot("#CDB98E", 40, 1.2), x + 120 + ph * (60 + 0.25 * v), r_["y"] - 8 - ph * 36, 14 + 26 * ph, 0.34 * (1 - ph) * min(1.0, v / 200))

    def _prepare_crowd(self, cx, act, p):
        dur = max(cx.dur, 1e-3)
        pal = (act == "palle")
        rs = _RS(14 if pal else 15)
        d = p.get("dir", "r" if pal else "l")
        sg = 1 if d in ("r", 1, "R") else -1
        self._cdir = sg
        fk = p.get("flags", "medici" if pal else "lily")
        self._cdev = {"medici": ("medici", "#E0B84E", "#B33620"), "lily": ("lily", "#F4EEDC", "#B33620"), "stripes": ("stripes", "#233C8C", "#E0B84E"), "cross": ("cross", "#F4EEDC", "#B33620")}.get(fk) if fk else None
        n = int(p.get("n", 24))
        kinds = ["halk", "tuccar", "soylu", "soylu_f", "cocuk", "halk", "banker", "halk"]
        self._palle_crowd = []
        for i in range(n):
            if pal:
                x1 = rs.uniform(700, 1350) if rs.rand() < 0.62 else rs.uniform(1350, 1750)
                x0 = rs.uniform(-300, 380)
            elif sg > 0:
                x1 = rs.uniform(PV_X0 + 250, PV_X0 + 1050)
                x0 = rs.uniform(PV_X0 - 1250, PV_X0 - 100)
            else:
                x1 = rs.uniform(PV_X0 + 250, PV_X0 + 1050)
                x0 = rs.uniform(PV_X0 + PV_W + 100, PV_X0 + PV_W + 1250)
            if sg * (x1 - x0) < 120:
                x0 = x1 - sg * rs.uniform(250, 700)
            self._palle_crowd.append(dict(x0=x0, x1=x1, y=YG + rs.uniform(-18, 40), h=rs.uniform(156, 192), kind=kinds[rs.randint(8)], seed=int(rs.randint(0, 40)), phase=rs.rand(),
                                          d=0.05 * dur * rs.rand() + 0.012 * dur * (i % 8), T=0.0, flag=(i % 4 == 1), amt=rs.uniform(0.6, 1.0), hop=rs.uniform(0.2, 0.7)))
        for m in self._palle_crowd:
            m["T"] = abs(m["x1"] - m["x0"]) / rs.uniform(112, 150)
        self._palle_crowd.sort(key=lambda m: m["y"])
        self._palle_riders = []
        nr = int(p.get("riders", 5 if pal else 0))
        for i in range(nr):
            self._palle_riders.append(dict(x0=(3950 if pal else PV_X0 + PV_W + 1500) + 190 * i, x1=(2200 if pal else PV_X0 + PV_W + 300) + 150 * i + rs.uniform(-40, 40), y=YG + 18 + (i % 3) * 14, h=262 + (i % 2) * 8,
                                           seed=3 + i, phase=rs.rand(), d=0.012 * dur * i, T=0.46 * dur))
        self._palle_riders.sort(key=lambda r: r["y"])

    # ── fx: grade sonrası (ateş, parıltı, yanan pencereler) ──
    def win_alpha(self, ctx, i, kind="pv"):
        act = ctx.p.get("act")
        t = ctx.t
        if act == "pencere":
            tn = ctx.win_off[i % len(ctx.win_off)] if ctx.win_off else 1e9
            a = 1.0 - ease_io((t - tn) / 0.55)
            return a * (0.88 + 0.12 * math.sin(t * 7.0 + i * 2.1))
        if act in ("ates", "odun"):
            h = (i * 7919 + 13) % 10
            if h > 3:
                return 0.0
            return (0.55 + 0.25 * math.sin(t * 3.0 + i)) * (1.0 if ctx.tod != "day" else 0.0)
        return 0.0

    def fx(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        p = ctx.p
        act = p.get("act")
        night = ctx.tod != "day"
        ctx.xf(1.0)
        xa, xb = ctx.xa, ctx.xb
        if night:
            for i, box in enumerate(self.G_PV["wins"]):
                if xa - 60 < box[0] < xb + 60:
                    lit_bifora(c, box[:4], self.win_alpha(ctx, i))
            if act in ("pencere", "ates", "odun"):
                fl = self.G_PV.get("bell")
                if fl and act == "pencere":
                    a_ = 0.9 * (1 - ease_io((t - ctx.win_off[-1]) / 0.8)) if ctx.win_off else 0.0
                    lit_bifora(c, (fl[0], fl[1], fl[2] * 0.7, fl[3]), a_ * 0.6)
            # meşaleler
            for tx in (self.G_PV["door"][0] - 120, self.G_PV["door"][0] + 120, PV_X0 + PV_W * 0.62, PV_X0 + PV_W * 0.86):
                if xa - 60 < tx < xb + 60:
                    torch_flame(c, tx - 7, YG - 176, t, seed=int(tx) % 50)
        if act == "palle":
            self._palle_fx(ctx)
        if act == "pencere":
            self._pencere_fx(ctx)
        if act in ("ates", "odun"):
            kf = ctx.fire_k
            if act == "ates":
                bonfire(c, PILE_X, PILE_Y - 20, 330, t, seed=2, k=kf, glow_a=1.0, tod=ctx.tod)
                self._act_ates_front(ctx)
            else:
                kodun = kf
                coal = ctx.coal
                # közer yatağı: yığın tabanında parlayan kor + titreyen ışık
                rs = _RS(19)
                for i in range(26):
                    px = PILE_X + rs.uniform(-0.5, 0.5) * 380
                    py = PILE_Y - rs.uniform(0.0, 0.5) * 70 - 4
                    fl = 0.5 + 0.5 * math.sin(t * (2.0 + rs.rand() * 3) + i * 1.7)
                    r_ = rs.uniform(10, 26)
                    _blit_dot(c, _soft_dot("#FF5A1E", 48, 1.1), px, py, r_ * 1.6, coal * (0.35 + 0.5 * fl))
                    _blit_dot(c, _soft_dot("#FFB347", 24, 1.2), px, py, r_ * 0.7, coal * (0.2 + 0.45 * fl))
                glow(c, PILE_X, PILE_Y - 40, 360 * (0.4 + 0.6 * coal), "#FF7A2A", 0.40 * coal)
                bonfire(c, PILE_X, PILE_Y - 22, 300, t, seed=6, k=kodun, glow_a=0.8, tod=ctx.tod)
                ash_field(c, PILE_X, PILE_Y - 100, t, n=70, wind=110, k=1.0, seed=8)
                smoke_plume(c, PILE_X + 30, PILE_Y - 120, t, size=130, n=8, k=0.5 + 0.5 * coal, col="#2C3042" if ctx.tod == "night" else "#4E4850", seed=12, rise=420, wind=90, a0=0.26)
        ctx.end()

    def _palle_fx(self, ctx):
        """Medici Sarayı penceresinde altın ışık (+ Lorenzo SİLUETİ yok; yalnız ışık); sancak parıltıları."""
        c, t = ctx.c, ctx.t
        dur = max(ctx.cx.dur, 1e-3)
        a = ease_io((t - ctx.win_gold_t0) / 1.2) if ctx.win_gold_t0 is not None else ease_io((t / dur - 0.55) / 0.2)
        wins = [w for w in self.G_MED["wins"] if w[4] == 2]
        wins.sort(key=lambda w: abs(w[0] - 470))
        w0 = wins[0]
        flick = 0.92 + 0.08 * math.sin(t * 6.1) + 0.04 * math.sin(t * 17.0)
        glow(c, w0[0], w0[1] - w0[3] * 0.5, w0[3] * 3.2, "#FFB020", 0.40 * a * flick)
        lit_bifora(c, w0[:4], a * flick, col="#FFC23D", core="#FFE79A")
        glow(c, w0[0], w0[1] - w0[3] * 0.5, w0[3] * 1.3, "#FFE08A", 0.45 * a * flick)
        for w_ in wins[1:3]:
            lit_bifora(c, w_[:4], a * 0.35 * flick, col="#E8A83A")

    def _pencere_fx(self, ctx):
        """İp çizgisi + gölge (asılı beden YOK): pencere denizliğinden sarkan ince ip, duvara düşen yumuşak gölge. Alacakaranlık→gece: lacivert örtü."""
        c, t = ctx.c, ctx.t
        wins = [w for w in self.G_PV["wins"] if w[4] == 2]
        wins.sort(key=lambda w: w[0])
        for sel in (wins[2], wins[5] if len(wins) > 5 else wins[-1]):
            x, yb = sel[0], sel[1]
            sway = math.sin(t * 1.1 + x * 0.01) * 2.4
            top_y = yb + 3
            L = 175
            pth = skia.Path()
            pth.moveTo(x + 2, top_y)
            pth.quadTo(x + 2 + sway * 0.5, top_y + L * 0.5, x + 3 + sway, top_y + L)
            c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6, Color=C("#2A1A0C", 235), StrokeCap=skia.Paint.kRound_Cap))
            c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#8A6A3A", 160)))
            # ucu: püskül (düğüm değil; ceset/beden/ilmik yok)
            c.drawCircle(x + 3 + sway, top_y + L + 4, 4.2, _pt("#2A1A0C", 235))
            # duvara düşen gölge (yumuşak, sağa eğik, uzun)
            sp = skia.Path()
            sp.moveTo(x + 14, top_y)
            sp.lineTo(x + 40 + sway, top_y + L + 30)
            sp.lineTo(x + 52 + sway, top_y + L + 30)
            sp.lineTo(x + 20, top_y)
            sp.close()
            c.drawPath(sp, skia.Paint(AntiAlias=True, Color=C("#10141E", 70), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 4)))

    # ── ışık/örtü (screen space) ──
    def lights(self, ctx):
        """Işık kaynakları: [(dünya x, dünya y, 'aydınlık' yarıçap, güç)]."""
        act = ctx.p.get("act")
        if act in ("ates", "odun"):
            kf = ctx.fire_k
            if act == "ates":
                return [(PILE_X, PILE_Y - 160 * kf - 40, 300 + 780 * kf, kf)]
            return [(PILE_X, PILE_Y - 130 * ctx.coal - 50, 260 + 520 * ctx.coal, ctx.coal)]
        return []

    def prepare(self, ctx):
        cx, p, t = ctx.cx, ctx.p, ctx.t
        dur = max(cx.dur, 1e-3)
        act = p.get("act")
        ctx.fire_k, ctx.fire_t0, ctx.coal, ctx.items, ctx.win_off, ctx.win_gold_t0 = 0.0, None, 0.0, [], None, None
        if act == "ates":
            items_at = p.get("items_at")
            n = len(items_at) if items_at else 14
            times = [_anchor(cx, a, 0.0) for a in items_at] if items_at else [0.06 * dur + (0.50 * dur - 0.06 * dur) * i / max(1, n - 1) for i in range(n)]
            rs = _RS(33)
            for i, tl in enumerate(times):
                side = 1 if i % 2 else -1
                src = (PILE_X + side * rs.uniform(360, 700), YG - rs.uniform(120, 190))
                ctx.items.append((tl, ITEM_KINDS[i % len(ITEM_KINDS)] if i % 7 != 6 else ITEM_KINDS[(i * 3) % 5], src))
            f0 = _anchor(cx, p.get("fire_at"), 0.58 * dur)
            ctx.fire_t0 = f0
            ramp = float(p.get("fire_dur", max(2.5, 0.40 * dur)))
            ctx.fire_k = smooth(clamp((t - f0) / ramp)) ** 0.9
        elif act == "odun":
            p_ = clamp(t / dur)
            k0 = float(p.get("fire0", 0.72))
            ctx.fire_k = k0 * (1 - p_) ** 1.8 * (1.0 if p_ < 0.9 else clamp((1 - p_) / 0.1))
            ctx.coal = 0.95 - 0.55 * p_
        elif act == "pencere":
            n = len(self.G_PV["wins"])
            order = self.win_order
            rank = {int(w): r for r, w in enumerate(order)}
            ctx.win_off = [0.10 * dur + 0.74 * dur * (rank[i] / max(1, n - 1)) for i in range(n)] + [0.90 * dur]
        elif act in ("palle", "kalabalik"):
            key_ = (dur, act, p.get("dir"), p.get("n"), p.get("flags"), p.get("riders"))
            if getattr(self, "_pd", None) != key_:
                self._prepare_crowd(cx, act, p)
                self._pd = key_
            ctx.win_gold_t0 = _anchor(cx, p.get("gold_at"), 0.55 * dur)

    def grade(self, ctx):
        _grade_generic(self, ctx)


def _grade_generic(world, ctx):
    """Alacakaranlık/gece derecelendirmesi (ekran uzayı; bant içine): ışık kaynağı varsa ışık havuzu, yoksa düz örtü. day → CM.finish günışığı yapar."""
    f, c = ctx.f, ctx.c
    tod = ctx.tod
    by0, bh = ctx.band
    rect = (0, by0, W, by0 + bh)
    p = ctx.p
    act = p.get("act")
    if act == "palle":                                                           # gün → sıcak akşam rengi (yalnız görsel dil): pencere ışığı öne çıkar
        dur = max(ctx.cx.dur, 1e-3)
        nk = ease_io((ctx.t / dur - 0.38) / 0.5)
        if nk > 0.01:
            wash(c, by0, bh, [("#6A3E78", 120), ("#E8803A", 70), ("#E8803A", 130)], [0.0, 0.55, 1.0], 0.95 * nk)
    if tod == "day":
        return
    dusk = (tod == "dusk")
    hue = (78, 46, 96) if dusk else (8, 12, 44)
    gain = 0.50 if dusk else 0.88
    if act == "pencere":                                                      # alacakaranlık → gece
        dur = max(ctx.cx.dur, 1e-3)
        nk = ease_io(ctx.t / dur)
        wash(c, by0, bh, [("#5A3E78", 70), ("#E8905A", 26), ("#E8905A", 40)], [0.0, 0.55, 1.0], 1.0 - 0.6 * nk)
        R(c, 0, by0, W, by0 + bh, "#0A1034", int(150 * nk))
        return
    L = world.lights(ctx) if hasattr(world, "lights") else []
    if L:
        wx, wy, r, kk = L[0]
        sx, sy = ctx.to_screen(1.0, wx, wy)
        R_ = r * ctx.z
        light_pool(f, sx, sy, R_, gain=gain, hue=hue, warm_a=round(0.20 * clamp(kk) / 0.04) * 0.04, edge=0.94 if not dusk else 0.80, rect=rect)
    else:
        if dusk:
            wash(c, by0, bh, [("#5A3E78", 78), ("#E8905A", 28), ("#E8905A", 46)], [0.0, 0.55, 1.0])
        else:
            R(c, 0, by0, W, by0 + bh, "#0A1034", 150)
            light_pool(f, W / 2, by0 + bh * 0.5, 1100, gain=0.5, hue=hue, warm_a=0.04, edge=0.55, rect=rect)


# ═════════════════════════════ SOKAK (dar sokak + palazzo cephesi + ağır kapı) ═════════════════════════════
DOOR_X = 3600
ARCH_X = 1850
DOOR_W, DOOR_H = 270, 372
FAC_H = 556                     # cephe yüksekliği (zemin → saçak)

_WALKSIL = {}


def walk_sil_set(kind, seed, h=300, col="#120F14", n=12):
    """Siluet yürüme döngüsü (n kare, önceden pişirilmiş): [(img…), ox, oy, f_cyc (döngü/sn), v_px (pişirme zemin hızı)]. Kare başına tek blit."""
    key = (kind, seed, h, col, n)
    r = _WALKSIL.get(key)
    if r is None:
        old = FA.SCALE_HINT
        FA.set_scale_hint(1.0)
        kit, bh = FA.kit_for(kind, seed, h)
        s_ = h / bh
        hb = kit.B["hb"]
        v_px = 0.80 * h
        vh = (v_px / s_) / hb
        s_len = hb * clamp(0.43 * (max(vh, 1e-3) / 0.8) ** 0.4 * kit.d.get("stride", 1.0), 0.09, 0.52)
        f_cyc = ((v_px / s_) / s_len) / 2.0
        frames = []
        ox = oy = 0.0
        for k in range(n):
            fr = sk.Frame(int(h * 1.0) + 40, int(h * 1.2) + 20)
            fr.clear(skia.ColorTRANSPARENT)
            ox, oy = fr.w / 2.0, fr.h - 10.0
            FA.walker(fr, kind, ox, oy, h, k / (n * f_cyc), speed=v_px, dir=1, seed=seed)
            frames.append(silhouettize(fr.surf.makeImageSnapshot(), col))
        FA.set_scale_hint(old)
        r = _WALKSIL[key] = (frames, ox, oy, f_cyc, v_px)
    return r


def draw_walk_sil(c, st, x, y, scale, face, t, v_ground, phase=0.0):
    """Siluet yürüyüşü: oynatma hızı zemin hızına oranlanır (paralaks silüetlerinde ayak kayması gözetilmez)."""
    frames, ox, oy, f_cyc, v_px = st
    rate = abs(v_ground) / v_px
    n = len(frames)
    idx = int(((t * f_cyc * rate + phase) % 1.0) * n) % n
    c.save()
    c.translate(x, y)
    c.scale(face * scale, scale)
    c.drawImage(frames[idx], -ox, -oy, LIN)
    c.restore()


def tunnel_arch(c, xc, yb, w, h, T, depth=0.0, warm=0.0):
    """Androne (geçit): taş çerçeveli kemer + içte küçülen iç içe tonozlar; uçta ışık (gün ışığı/lamba). warm: uç ışığın sıcaklığı."""
    portal(c, xc, yb, w, h, T, depth, interior="#120C07")
    for i in range(1, 7):
        sc = 1.0 - i * 0.135
        col = mix("#1A120A", "#6A4A2A" if warm < 0.5 else "#B8803A", (i / 7.0) ** 2)
        c.drawPath(arch_path(xc, yb - 4 * i, w * sc, h * sc - 6 * i), _pt(col, 235))
    c.drawPath(arch_path(xc, yb - 26, w * 0.16, h * 0.36), _pt("#F4E2B0" if warm < 0.5 else "#FFD27A", 245))
    for k in range(5):                                                        # zemin perspektif çizgileri
        yy = yb - 3 - k * 3
        c.drawLine(xc - w * 0.5 * (1 - k * 0.17), yy, xc + w * 0.5 * (1 - k * 0.17), yy, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#000000", 70)))


def window_grille(c, xc, yb, w, h, T, depth=0.0):
    """Zemin kat pencere: taş söveli, demir parmaklıklı (yatay-dikey kafes) küçük pencere + konsol."""
    R(c, xc - w * 0.62, yb - h - 8, xc + w * 0.62, yb + 6, T("#D2C096", depth))
    INKR(c, xc - w * 0.62, yb - h - 8, xc + w * 0.62, yb + 6, 1.2, 160)
    R(c, xc - w / 2, yb - h, xc + w / 2, yb, T("#1E140C", 0.2))
    for k in range(1, 5):
        c.drawLine(xc - w / 2 + k * w / 5, yb - h, xc - w / 2 + k * w / 5, yb, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2, Color=C("#6A6258", 235)))
    for k in range(1, 4):
        c.drawLine(xc - w / 2, yb - k * h / 4, xc + w / 2, yb - k * h / 4, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.8, Color=C("#6A6258", 225)))
    R(c, xc - w * 0.7, yb + 2, xc + w * 0.7, yb + 10, T("#BDAB82", depth))


def street_windows(xa, xb, y, h, door_x=DOOR_X, arch_x=ARCH_X):
    """Sokak cephesi pencere geometrisi (çizimsiz): [(tür 'grille'|'bifora'|'arch', xc, yb, w, h, kat)]; [xa,xb] aralığı."""
    out = []
    i0 = max(0, int((xa - 260) // 215) - 1)
    for i in range(i0, int((xb - 260) // 215) + 2):
        xc = 260 + i * 215
        if xc < xa - 60 or xc > xb + 60:
            continue
        near_door = abs(xc - door_x) < 330
        near_arch = abs(xc - arch_x) < 440
        if not near_door and not near_arch:
            out.append(("grille", xc, y - 0.13 * h, 78, 96, 0))
        if not near_arch and not (near_door and abs(xc - door_x) < 120):
            out.append(("bifora", xc, y - 0.405 * h, 84, 150, 1))
        if not (near_door and abs(xc - door_x) < 120):
            out.append(("arch", xc, y - 0.77 * h, 62, 112, 2))
    return out


def street_facade(c, xa, xb, X0, X1, y, h, T, seed=5, door_x=DOOR_X, arch_x=ARCH_X):
    """Uzun sokak cephesi (X0..X1; yalnız [xa,xb] aralığı çizilir): bugnato zemin → ince bugnato → sıva üst kat, taş bank, pencere sıraları, saçak + çatı + bacalar.
    Dönüş: pencere kutuları [(xc,yb,w,h,kat)]."""
    wins = []
    cl = (xa, xb)
    stone_wall(c, X0, y - 0.31 * h, X1, y, "#C2AC82", T, 0.0, seed, ch=h * 0.062, bw=(86, 150), rustic=True, clip=cl)
    stone_wall(c, X0, y - 0.64 * h, X1, y - 0.31 * h, "#CDB98E", T, 0.0, seed + 1, ch=h * 0.048, bw=(70, 120), rustic=True, joint_a=84, clip=cl)
    cx0, cx1 = max(X0, xa - 4), min(X1, xb + 4)
    R(c, cx0, y - h, cx1, y - 0.64 * h, T("#E0CFA6", 0.0))
    # üst kat sıva: ince derz izleri + leke
    rs = _RS(seed + 9)
    for i in range(int((cx1 - cx0) / 90)):
        px = rs.uniform(cx0, cx1)
        py = rs.uniform(y - h + 20, y - 0.66 * h)
        OVAL(c, px, py, rs.uniform(20, 70), rs.uniform(6, 22), "#B8A47A", 26)
    for fy in (y - 0.31 * h, y - 0.64 * h):
        R(c, cx0, fy - 5, cx1, fy + 4, T("#D8C79E", 0.0))
        c.drawLine(cx0, fy + 4, cx1, fy + 4, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 150)))
    # taş bank (panchina)
    R(c, cx0, y - 54, cx1, y, T("#B9A57C", 0.0))
    R(c, cx0, y - 62, cx1, y - 52, T("#D9C9A0", 0.0))
    c.drawLine(cx0, y - 62, cx1, y - 62, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 160)))
    c.drawLine(cx0, y - 52, cx1, y - 52, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C(INK, 120)))
    gx = int(cx0 // 150) * 150
    pj = skia.Path()
    while gx < cx1:
        pj.moveTo(gx, y - 52)
        pj.lineTo(gx, y)
        gx += 150
    c.drawPath(pj, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#4A3A22", 90)))
    # pencereler (küresel ızgara)
    for (kind, xc, yb, ww, wh, kat) in street_windows(max(X0, xa - 300), min(X1, xb + 300), y, h, door_x, arch_x):
        if xc < cx0 - 60 or xc > cx1 + 60:
            continue
        if kind == "grille":
            window_grille(c, xc, yb, ww, wh, T)
        elif kind == "bifora":
            bifora(c, xc, yb, ww, wh, T)
            wins.append((xc, yb, ww, wh, kat))
        else:
            wp = arch_path(xc, yb, ww, wh)
            c.drawPath(wp, _pt(T("#241810", 0.2)))
            INKP(c, wp, 1.1, 160)
            R(c, xc - 40, yb - 2, xc + 40, yb + 4, T("#CDBB92", 0.0))
            R(c, xc - 31, yb - 56, xc, yb, T("#5A7650", 0.0), 235)                  # yarı açık kepenk
            wins.append((xc, yb, ww, wh, kat))
    # kapı üstü balkon penceresi + stemma
    if cx0 - 200 < door_x < cx1 + 200:
        bifora(c, door_x, y - 0.56 * h, 120, 190, T)
        R(c, door_x - 96, y - 0.56 * h + 4, door_x + 96, y - 0.56 * h + 20, T("#C6B488", 0.0))
        INKR(c, door_x - 96, y - 0.56 * h + 4, door_x + 96, y - 0.56 * h + 20, 1.2, 160)
        for k in range(7):
            R(c, door_x - 90 + k * 30, y - 0.56 * h + 20, door_x - 78 + k * 30, y - 0.56 * h + 34, T("#B4A07A", 0.0))
        sx_, sy_ = door_x, y - DOOR_H - 96
        sp = skia.Path()
        sp.moveTo(sx_ - 36, sy_ - 34)
        sp.lineTo(sx_ + 36, sy_ - 34)
        sp.lineTo(sx_ + 36, sy_ + 10)
        sp.cubicTo(sx_ + 36, sy_ + 40, sx_ + 12, sy_ + 54, sx_, sy_ + 64)
        sp.cubicTo(sx_ - 12, sy_ + 54, sx_ - 36, sy_ + 40, sx_ - 36, sy_ + 10)
        sp.close()
        c.drawPath(sp, _pt(T("#D6C8A0", 0.0)))
        INKP(c, sp, 1.6, 190)
        c.drawLine(sx_ - 36, sy_ - 6, sx_ + 36, sy_ - 6, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=9, Color=C("#9C8A64", 200)))
    # saçak + çatı
    R(c, cx0, y - h - 22, cx1, y - h, T("#CDBB92", 0.0))
    nb = int((cx1 - cx0) / 36) + 2
    bx0 = int(cx0 // 36) * 36
    for i in range(nb):
        bx = bx0 + i * 36
        c.drawPath(sk.poly_path([(bx, y - h), (bx + 24, y - h), (bx + 12, y - h + 20)]), _pt(T("#9C8A64", 0.0)))
    c.drawLine(cx0, y - h - 22, cx1, y - h - 22, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 165)))
    R(c, cx0, y - h - 62, cx1, y - h - 22, T("#B4552E", 0.0))
    for k in range(1, 5):
        c.drawLine(cx0, y - h - 22 - k * 8, cx1, y - h - 22 - k * 8, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#5A2412", 90)))
    tj = skia.Path()
    gx = int(cx0 // 22) * 22
    while gx < cx1:
        tj.moveTo(gx, y - h - 62)
        tj.lineTo(gx, y - h - 22)
        gx += 22
    c.drawPath(tj, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#5A2412", 55)))
    c.drawLine(cx0, y - h - 62, cx1, y - h - 62, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 150)))
    for bxc in (620, 1480, 2250, 3380, 4040, 5250, 6000):                      # bacalar
        if cx0 - 60 < bxc < cx1 + 60:
            R(c, bxc, y - h - 130, bxc + 36, y - h - 62, T("#A8684A", 0.0))
            R(c, bxc - 5, y - h - 140, bxc + 41, y - h - 128, T("#8A5236", 0.0))
            INKR(c, bxc, y - h - 130, bxc + 36, y - h - 62, 1.1, 150)
    return wins


class Sokak(SWorld):
    name = "sehir_sokak"
    PW = 6400
    _draw_sky = PN.Florence._draw_sky
    _draw_hills = PN.Florence._draw_hills
    dyn_sky = PN.Florence.dyn_sky
    _draw_city = Meydan._draw_city

    def build(self):
        PW = self.PW
        cam_span = PW - W

        def Lw(f):
            return int(W + cam_span * f + 500)
        self.cloud_seed = 7
        rr = _RS(6)
        self.city_houses = []
        x = -40
        while x < Lw(0.30) + 60:
            bw, bh = rr.uniform(34, 74), rr.uniform(30, 70)
            self.city_houses.append((x, bw, bh, int(rr.randint(1, 10 ** 6)), 0.46, 0))
            x += bw + rr.uniform(-4, 8)
        x = 20
        while x < Lw(0.30) + 60:
            bw, bh = rr.uniform(40, 80), rr.uniform(34, 76)
            self.city_houses.append((x, bw, bh, int(rr.randint(1, 10 ** 6)), 0.26, 20))
            x += bw + rr.uniform(-6, 6)
        self.mid_houses = []
        x = -60
        rr = _RS(23)
        while x < Lw(0.60) + 60:
            bw, bh = rr.uniform(120, 200), rr.uniform(500, 650)
            self.mid_houses.append((x, bw, bh, int(rr.randint(1, 10 ** 6))))
            x += bw + rr.uniform(-10, 10)
        self.layer("sky", 0.05, Lw(0.05), self._draw_sky, opaque=True, scale=0.5, wear=3, loss=0.5, yr=(0, 700))
        self.layer("hills", 0.14, Lw(0.14), self._draw_hills, scale=0.5, wear=2, yr=(330, 800))
        self.layer("city", 0.30, Lw(0.30), self._draw_city, wear=2, yr=(60, 620))
        self.layer("mid", 0.60, Lw(0.60), self._draw_mid, wear=2, yr=(60, 860))
        self.layer("main", 1.0, PW, self._draw_main, wear=4)
        self.walk_wins = []
        self.sil_kinds = [("halk", 3), ("tuccar", 5), ("kesis", 2), ("soylu_f", 4), ("halk", 9), ("rahip", 6), ("soylu", 8), ("banker", 11), ("cocuk", 4), ("halk", 14), ("tuccar", 17), ("soylu_f", 21)]
        rs = _RS(41)
        self.fg_sils = []
        x = 400.0
        for i in range(16):
            k, sd = self.sil_kinds[i % len(self.sil_kinds)]
            self.fg_sils.append(dict(kind=k, seed=sd, x0=x, v=-rs.uniform(120, 190), h=rs.uniform(0.85, 1.15), ph=rs.rand()))
            x += rs.uniform(750, 1250)
        self.amb = []
        rs = _RS(77)
        for i in range(9):
            self.amb.append(dict(kind=["halk", "tuccar", "soylu_f", "cocuk", "banker", "kesis", "denizci", "halk", "rahip"][i % 9], x0=rs.uniform(300, 6000), dir=1 if rs.rand() < 0.5 else -1, v=rs.uniform(38, 70),
                                 seed=int(rs.randint(0, 40)), h=rs.uniform(150, 178), y=YG - 28 + rs.uniform(-6, 8), phase=rs.rand(), prop=(["sack", "basket", "staff", None][rs.randint(4)])))
        self.talk = [dict(kind="tuccar", x=1180, seed=3, face=1), dict(kind="banker", x=1262, seed=5, face=-1), dict(kind="halk", x=3560, seed=9, face=1), dict(kind="soylu_f", x=3650, seed=12, face=-1)]

    def default_cams(self, act=None, p=None):
        p = p or {}
        d = p.get("door")
        if d:                                                 # kapıya itiş: sokak seviyesinde yaklaşır
            return [(0.0, (DOOR_X - 620, 70, 1.0)), (0.55, (DOOR_X - 200, 80, 1.10)), (1.0, (DOOR_X + 30, 96, 1.30))]
        return [(0.0, (900, 40, 1.0)), (0.66, (1480, 40, 1.05)), (1.0, (ARCH_X - 50, 44, 1.20))]       # yürüyen figürleri izler, sonunda kemerli eşiğe oturur

    def stack(self, ctx):
        return [("L", "sky"), ("D", "dyn_sky", 0.05), ("L", "hills"), ("L", "city"), ("D", "dyn_city", 0.30), ("L", "mid"), ("D", "dyn_mid", 0.60), ("L", "main"), ("D", "dyn_main", 1.0), ("D", "dyn_front", 1.45)]

    def _draw_mid(self, fr, xa, xb):
        c = fr.c
        T = self.T
        wins = []
        for (x, bw, bh, sd) in self.mid_houses:
            if x + bw < xa - 40 or x > xb + 40:
                continue
            rs = _RS(sd)
            CT.draw_house(c, x, YG - 40, bw, bh, rs, T, 0.26, wins)
            if rs.rand() < 0.5:
                cxh = x + bw * rs.uniform(0.2, 0.75)
                R(c, cxh, YG - 40 - bh - bw * 0.40 - 26, cxh + 12, YG - 40 - bh - bw * 0.20, T("#9C6A4A", 0.26))
        if self.tod != "day":
            PN._lit_boxes(c, _RS(int(xa) % 991 + 5), wins, True, 0.42 if self.tod == "night" else 0.2)

    def _draw_main(self, fr, xa, xb):
        c = fr.c
        T = self.T
        PN.draw_pavement(c, xa, xb, YG - 8, 960, T, seed=int(xa) // 1024)
        street_facade(c, xa, xb, 0, self.PW, YG, FAC_H, T, seed=5)
        if xa < DOOR_X + 400 and xb > DOOR_X - 400:
            portal(c, DOOR_X, YG, DOOR_W, DOOR_H, T)
        if xa < ARCH_X + 500 and xb > ARCH_X - 500:
            tunnel_arch(c, ARCH_X, YG, 400, 400, T, warm=0.0 if self.tod == "day" else 1.0)
        # meşale/fener demirleri
        for tx in (DOOR_X - 230, DOOR_X + 230, ARCH_X - 300, ARCH_X + 300, 1500, 3950):
            if xa - 40 < tx < xb + 40:
                torch_bracket(c, tx, YG - 300, T)
        # kaldırım taşları, varil, çuval
        rs = _RS(77)
        for i in range(60):
            x = rs.uniform(0, self.PW)
            if not (xa - 30 < x < xb + 30):
                continue
            OVAL(c, x, YG + rs.uniform(40, 100), rs.uniform(10, 28), rs.uniform(2, 5), "#7A6A48", 90)
        for bx in (700, 1900, 3300, 4300, 5600):
            if xa - 60 < bx < xb + 60:
                OVAL(c, bx, YG - 26, 22, 30, T("#7A5230", 0.0))
                c.drawOval(skia.Rect.MakeLTRB(bx - 22, YG - 56, bx + 22, YG + 4), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 170)))
                for hy in (-40, -14):
                    c.drawLine(bx - 21, YG + hy, bx + 21, YG + hy, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=C("#2A2622", 200)))

    # ── hazırlık: kapı hareketi ──
    def prepare(self, ctx):
        cx, p, t = ctx.cx, ctx.p, ctx.t
        dur = max(cx.dur, 1e-3)
        d = p.get("door")
        dat = _anchor(cx, p.get("door_at"), 0.60 * dur)
        op, slam, glow_k = 0.0, -1.0, 0.0
        if d == "close":
            if t < dat:
                op = 0.92 + 0.035 * math.sin(t * 1.4)
            else:
                u = (t - dat) / 0.20
                if u < 1.0:
                    op = 0.92 * (1.0 - u * u)                    # hızlanarak TEK HAMLEDE kapanır
                else:
                    slam = t - dat - 0.20
                    op = 0.05 * math.exp(-slam * 11) * abs(math.sin(slam * 24))
            glow_k = 0.85 if ctx.tod != "day" else 0.25
        elif d == "open":
            if p.get("door_at") is None:
                op = 0.9
            else:
                u = (t - dat) / 0.9
                op = 0.92 * ease_out(u) + (0.03 * math.sin(max(0.0, t - dat - 0.9) * 5) * math.exp(-max(0.0, t - dat - 0.9) * 3) if u > 1 else 0.0)
            glow_k = 0.85 if ctx.tod != "day" else 0.25
        ctx.door_open, ctx.slam_t, ctx.door_glow, ctx.door_at = op, slam, glow_k, dat
        if slam >= 0.0 and slam < 0.9:                           # çarpma sarsıntısı (kamera ofseti)
            amp = 10.0 * math.exp(-slam * 7.5)
            ctx.camx += math.sin(slam * 71.0) * amp * 0.55
            ctx.camy += math.cos(slam * 87.0) * amp
        ctx.fire_k = 0.0

    def lights(self, ctx):
        if ctx.tod == "day":
            return []
        return [(DOOR_X, YG - 200, 1100, 0.55)]

    def grade(self, ctx):
        _grade_generic(self, ctx)

    # ── dinamik ──
    def dyn_city(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        FA.atmo_birds(c, t, 7, 1.0, xa, xb, 190, 350, speed=24.0, night=ctx.night, seed=5, size=0.8)

    def dyn_mid(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        rs = _RS(61)
        for i in range(14):
            x = -40 + i * 330 + rs.uniform(-60, 60)
            if x < xa - 60 or x > xb + 60:
                continue
            for k in range(4):
                ph = (t * 0.18 + k / 4.0 + i * 0.29) % 1.0
                _blit_dot(c, _soft_dot("#C8C0B4" if not ctx.night else "#6A7A9A", 40, 1.2), x + math.sin(ph * 5 + i) * 6 * ph, YG - 40 - 640 - ph * 90, 5 + 11 * ph, 0.22 * (1 - ph))

    def dyn_main(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        p = ctx.p
        # çatıdan bacalar: duman
        for bxc in (620, 1480, 2250, 3380, 4040, 5250, 6000):
            if xa - 80 < bxc < xb + 80:
                smoke_plume(c, bxc + 18, YG - FAC_H - 140, t, size=26, n=5, k=0.8, col="#B8B0A4" if not ctx.night else "#566080", seed=bxc % 17, rise=130, wind=26, a0=0.34)
        # asılı kumaş (üst kat pencerelerinden) + kırlangıçlar
        for i, bx in enumerate((900, 2050, 3500, 5100)):
            if xa - 100 < bx < xb + 60:
                LINE(c, bx - 6, YG - 0.78 * FAC_H - 60, bx + 90, YG - 0.78 * FAC_H - 60, "#4A3220", 3.0)
                PN.draw_cloth(c, bx, YG - 0.78 * FAC_H - 60, ["#B3361F", "#233C8C", "#C79A3C", "#2E6A4F"][i % 4], "#EDE4CC", 74, 150, t, ph=i * 1.4, wind=1.0, kind="tente", seed=90 + i)
        # banktaki konuşanlar
        for m in self.talk:
            if xa - 120 < m["x"] < xb + 120:
                FA.actor(f, m["kind"], m["x"], YG - 6, 168, t, action="talk", dir=m["face"], seed=m["seed"], phase=(m["x"] * 0.013) % 1.0, energy=0.9)
        # ortam yürüyenleri (iki yönlü)
        vis = []
        for a_ in self.amb:
            x = a_["x0"] + a_["dir"] * a_["v"] * t
            if xa - 160 < x < xb + 160:
                vis.append((a_["y"], a_, x))
        vis.sort(key=lambda q: q[0])
        for (_, a_, x) in vis:
            FA.walker(f, a_["kind"], x, a_["y"], a_["h"], t, speed=a_["v"], dir=a_["dir"], phase=a_["phase"], seed=a_["seed"], prop=a_["prop"])
        # kapı
        if p.get("door") and xa - 300 < DOOR_X < xb + 300:
            door_heavy(f, DOOR_X, YG, DOOR_H, ctx.door_open, w=DOOR_W, glow_k=ctx.door_glow, seed=3, swing=(math.sin(max(0.0, ctx.slam_t) * 30) * math.exp(-max(0.0, ctx.slam_t) * 5) if ctx.slam_t >= 0 else 0.0) * 6)
            if ctx.slam_t >= 0.0 and ctx.slam_t < 1.6:
                st_ = ctx.slam_t
                for k in range(10):                                  # çarpma tozu (tabandan yayılır)
                    ph_ = clamp(st_ / 1.3)
                    dx_ = (k - 4.5) * 34 * (0.35 + ph_)
                    _blit_dot(c, _soft_dot("#D8C69C", 40, 1.0), DOOR_X + dx_, YG - 12 - ph_ * (30 + (k % 3) * 22), 22 + 46 * ph_, 0.72 * (1 - ph_) ** 1.1)
                for k in range(14):                                  # lento'dan dökülen toz taneleri
                    ph_ = clamp((st_ - 0.02 * k) / 0.9)
                    if 0 < ph_ < 1:
                        _blit_dot(c, _soft_dot("#B8A47A", 20, 1.0), DOOR_X + (k - 6.5) * 18, YG - DOOR_H - 16 + ph_ * 130 + (k % 4) * 6, 3.0, 0.7 * (1 - ph_))
        # kullanıcı/varsayılan figürler (yürüyüş)
        acts = p.get("actors")
        if acts is None:
            dur_ = max(ctx.cx.dur, 1e-3)
            vw = clamp(1060.0 / (0.76 * dur_), 70.0, 150.0)
            gate = (ARCH_X, 400)
            acts = [dict(kind="soylu", x0=640, dir=1, speed=vw, h=214, seed=2, phase=0.0, y=YG - 8, gate=gate, stil=dict(robe="#2F5FB8", robe2="#E0B84E", hat_col="#B33620")),
                    dict(kind="tuccar", x0=478, dir=1, speed=vw, h=206, seed=7, phase=0.35, y=YG - 2, gate=gate, stil=dict(robe="#9C3A2A", robe2="#D8B070")),
                    dict(kind="banker", x0=330, dir=1, speed=vw, h=208, seed=11, phase=0.66, y=YG - 12, gate=gate, stil=dict(robe="#2E6A4F", robe2="#C79A3C"))]
        for a_ in sorted(acts, key=lambda q: q.get("y", YG)):
            draw_actor(ctx, a_)
        for st in ctx.stations:
            fn = st.get("fn")
            if fn is None:
                continue
            if abs(st.get("x", 0) - (xa + xb) / 2) > 1400:
                continue
            ctx.st = st
            fn(ctx, st)

    def dyn_front(self, ctx):
        """Ön plan (paralaks 1,45): ters yönde (sağdan sola) akan SİLUET kalabalık; yürüme döngüsü önceden pişirilmiş (kare başına tek blit)."""
        c, t = ctx.c, ctx.t
        for m in self.fg_sils:
            x = m["x0"] + m["v"] * t
            if x < ctx.xa - 300 or x > ctx.xb + 300:
                continue
            st = walk_sil_set(m["kind"], m["seed"], 300, {"day": "#2B2118", "dusk": "#1E1620", "night": "#08080F"}[ctx.tod])
            draw_walk_sil(c, st, x, 930 + (m["seed"] % 3) * 14, m["h"], -1, t, abs(m["v"]) * 1.0, m["ph"])

    # ── fx: ateş/ışık ──
    def fx(self, ctx):
        c, t = ctx.c, ctx.t
        if ctx.tod == "day":
            return
        ctx.xf(1.0)
        xa, xb = ctx.xa, ctx.xb
        for tx in (DOOR_X - 230, DOOR_X + 230, ARCH_X - 300, ARCH_X + 300, 1500, 3950):
            if xa - 60 < tx < xb + 60:
                torch_flame(c, tx - 7, YG - 284, t, size=54.0, seed=int(tx) % 50)
        # yanan pencereler: yarısı sıcak ışık (üst katlar), sakin titreme; geçit ucundaki ışık
        for (kind, xc, yb, ww, wh, kat) in street_windows(xa - 100, xb + 100, YG, FAC_H):
            if kind == "grille":
                continue
            hsh = (int(xc) * 7919 + kat * 31) % 11
            if hsh > 5:
                continue
            a_ = (0.70 + 0.2 * math.sin(t * 2.3 + xc * 0.07)) * (1.0 if hsh % 2 == 0 else 0.55)
            if kind == "bifora":
                lit_bifora(c, (xc, yb, ww, wh), a_)
            else:
                c.drawPath(arch_path(xc, yb, ww, wh), _pt("#FFC862", int(215 * a_)))
                glow(c, xc, yb - wh * 0.5, wh * 0.85, "#FFB04A", 0.30 * a_)
        if xa - 500 < ARCH_X < xb + 500:
            fl = 0.9 + 0.1 * math.sin(t * 6.0)
            glow(c, ARCH_X, YG - 120, 240 * fl, "#FFC070", 0.40)
        if ctx.p.get("door") and xa - 300 < DOOR_X < xb + 300 and ctx.door_open > 0.05:
            glow(c, DOOR_X, YG - 130, 300 * (0.5 + 0.5 * ctx.door_open), "#FFB04A", 0.38 * ctx.door_open)
        ctx.end()


# ═════════════════════════════ KALE (surlar, kuşatma, Castel Sant'Angelo, Passetto) ═════════════════════════════
def _lerp(a, b, u):
    return a + (b - a) * u


def wool_bale(c, x, y, w, h, seed=1, col=None):
    """Yün balyası: yuvarlak köşeli bej bohça, iple bağlı (dikey şeritler + düğüm), yün kılları dokusu; (x,y) sol-üst."""
    rs = _RS(seed)
    base = col or mix("#EADFC4", "#CDBE9A", rs.rand() * 0.55)
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), h * 0.30, h * 0.30)
    sh = skia.GradientShader.MakeLinear([(0, y), (0, y + h)], [C(mix(base, "#FFFFFF", 0.22)), C(base), C(mix(base, "#5A4630", 0.30))], [0.0, 0.5, 1.0])
    c.drawRRect(rr, skia.Paint(AntiAlias=True, Shader=sh))
    c.save()
    c.clipRRect(rr, skia.ClipOp.kIntersect, True)
    for i in range(int(w * h / 190)):
        px, py = x + rs.uniform(3, w - 3), y + rs.uniform(3, h - 3)
        L = rs.uniform(5, 13)
        ang = rs.uniform(-0.7, 0.7)
        c.drawLine(px, py, px + L * math.cos(ang), py + L * math.sin(ang), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C("#FFFBEA" if rs.rand() < 0.55 else "#9C8A66", 110 if rs.rand() < 0.55 else 80), StrokeCap=skia.Paint.kRound_Cap))
    for fx in (0.27, 0.73):
        c.drawLine(x + w * fx, y, x + w * fx, y + h, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6, Color=C("#5A4630", 225)))
        c.drawCircle(x + w * fx, y + h * 0.5, 2.6, _pt("#3A2A18", 235))
    c.drawLine(x, y + h * 0.5, x + w, y + h * 0.5, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C("#5A4630", 150)))
    c.restore()
    c.drawRRect(rr, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 185)))


def cannon(c, x, y, s=1.0, dirn=1, col="#2A2420", metal="#7A6648"):
    """Top siluet (tekerlekli kızak + hafif yukarı bakan namlu): x,y = kızağın zemin noktası; dirn namlu yönü; renkler koyu (duman/ateş/insan yok)."""
    c.save()
    c.translate(x, y)
    c.scale(dirn * s, s)
    c.drawPath(sk.poly_path([(-30, 0), (24, 0), (32, -16), (-22, -34)]), _pt(col))
    c.save()
    c.translate(-4, -33)
    c.rotate(-11)
    bp = skia.Path()
    bp.moveTo(-14, -10)
    bp.lineTo(70, -8)
    bp.lineTo(88, -9)
    bp.lineTo(88, 9)
    bp.lineTo(70, 8)
    bp.lineTo(-14, 11)
    bp.close()
    c.drawPath(bp, _pt(metal))
    for rx in (6, 34, 68):
        c.drawRect(skia.Rect.MakeLTRB(rx, -11, rx + 5, 12), _pt(col, 235))
    c.drawRect(skia.Rect.MakeLTRB(84, -12, 93, 12), _pt(col, 240))
    INKP(c, bp, 1.3, 200)
    c.restore()
    for wx in (-14, 16):
        c.drawCircle(wx, -7, 11, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.0, Color=C(col, 255)))
        c.drawCircle(wx, -7, 2.6, _pt(col))
        for k in range(4):
            a = k * math.pi / 4
            c.drawLine(wx - math.cos(a) * 10, -7 - math.sin(a) * 10, wx + math.cos(a) * 10, -7 + math.sin(a) * 10, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.8, Color=C(col, 255)))
    c.restore()


def gabion(c, x, y, w, h, T, seed=1):
    """Toprak dolu hasır sepet (cesto): kahverengi örgü, üstte toprak yığını; (x,y) sol-alt."""
    R(c, x, y - h, x + w, y, T("#7A5A34", 0.0))
    for i in range(1, 6):
        c.drawLine(x + i * w / 6, y - h, x + i * w / 6, y, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#3A2410", 150)))
    for i in range(1, 4):
        c.drawLine(x, y - i * h / 4, x + w, y - i * h / 4, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0, Color=C("#4A3018", 130)))
    c.drawOval(skia.Rect.MakeLTRB(x - 2, y - h - h * 0.22, x + w + 2, y - h + h * 0.22), _pt(T("#8A6E48", 0.0)))
    INKR(c, x, y - h, x + w, y, 1.1, 170)


def tent_layout(x0, x1, y, size, seed=0, jitter=0.35):
    """Çadır dizisi yerleşimi (çizimsiz; önbellekten yüklenen kareaşlarda da bayrak konumları bilinsin): [dict(x, y, w, h, kind, flag)]."""
    rs = _RS(seed)
    out = []
    x = x0
    while x < x1:
        w = size * rs.uniform(0.85, 1.35)
        h = w * rs.uniform(0.70, 0.95)
        kind = ("pavilion" if rs.rand() < 0.62 else "long")
        out.append(dict(x=x + w / 2, y=y + rs.uniform(-1, 1) * size * 0.12, w=w, h=h, kind=kind, flag=(rs.rand() < 0.55), fk=int(rs.randint(0, 3)), pole=h * rs.uniform(0.55, 0.9)))
        x += w * rs.uniform(1.05, 1.0 + jitter + 0.6)
    return out


def tent_row(f, x0, x1, y, size, T=None, seed=0, depth=0.5, jitter=0.35):
    """İmparatorluk ordusu çadır dizisi (ufukta; insan yok): koni/uzun çadırlar, iki tonlu paneller, direk; döner: bayrak noktaları [(x, y, tür)]. Bayraklar dinamik (`tent_flags`)."""
    c = _cv(f)
    T = T or CT.Tint("day")
    pts = []
    for tt in tent_layout(x0, x1, y, size, seed, jitter):
        x, yb, w, h = tt["x"], tt["y"], tt["w"], tt["h"]
        wall = T("#EFE6D0", depth)
        stripe = T("#B8452C" if tt["fk"] != 1 else "#2E4F8A", depth)
        if tt["kind"] == "pavilion":
            body = sk.poly_path([(x - w / 2, yb), (x - w * 0.10, yb - h), (x + w * 0.10, yb - h), (x + w / 2, yb)])
            c.drawPath(body, _pt(wall))
            c.save()
            c.clipPath(body, skia.ClipOp.kIntersect, True)
            n = 5
            for k in range(n):
                if k % 2 == 0:
                    c.drawPath(sk.poly_path([(x - w / 2 + k * w / n, yb), (x - w * 0.10 + k * w * 0.2 / n, yb - h), (x - w * 0.10 + (k + 1) * w * 0.2 / n, yb - h), (x - w / 2 + (k + 1) * w / n, yb)]), _pt(stripe))
            c.restore()
            INKP(c, body, 1.0, 165)
            c.drawPath(sk.poly_path([(x - w * 0.09, yb), (x, yb - h * 0.46), (x + w * 0.09, yb)]), _pt(T("#3A2A1C", depth), 235))
        else:
            body = sk.poly_path([(x - w / 2, yb), (x - w / 2, yb - h * 0.40), (x, yb - h), (x + w / 2, yb - h * 0.40), (x + w / 2, yb)])
            c.drawPath(body, _pt(wall))
            c.drawPath(sk.poly_path([(x - w / 2, yb - h * 0.40), (x, yb - h), (x + w / 2, yb - h * 0.40), (x + w / 2, yb - h * 0.52), (x, yb - h * 1.10), (x - w / 2, yb - h * 0.52)]), _pt(stripe, 190))
            INKP(c, body, 1.0, 165)
            c.drawPath(sk.poly_path([(x - w * 0.07, yb), (x - w * 0.07, yb - h * 0.34), (x + w * 0.07, yb - h * 0.34), (x + w * 0.07, yb)]), _pt(T("#3A2A1C", depth), 235))
        if tt["flag"]:
            R(c, x + w * 0.02, yb - h, x + w * 0.02 + 1.6, yb - h - tt["pole"], INK, 235)
        R(c, x + w / 2 - w * 0.07, yb - 2, x + w / 2 + w * 0.06, yb, "#3A2A1C", 120)
        if tt["flag"]:
            pts.append((x + w * 0.02 + 0.8, yb - h - tt["pole"], tt["fk"], size))
    return pts


def tent_flags(c, pts, t, scale=1.0):
    """Çadır bayrakları: kızıl çapraz (Burgonya) / altın zeminde kara kartal / lacivert; rüzgârda dalgalanır."""
    for i, (x, y, fk, size) in enumerate(pts):
        w, h = size * 0.62 * scale, size * 0.34 * scale
        top, bot = [], []
        n = 6
        for k in range(n + 1):
            u = k / n
            wv = math.sin(t * 5.2 - u * 3.6 + i) * h * 0.16 * u
            top.append((x + u * w, y + wv))
            bot.append((x + u * w, y + h + wv))
        path = sk.poly_path(top + bot[::-1])
        col = ("#F2EBD9", "#E0B84E", "#2E4F8A")[fk % 3]
        c.drawPath(path, _pt(col))
        c.save()
        c.clipPath(path, skia.ClipOp.kIntersect, True)
        if fk % 3 == 0:                                                         # kızıl çapraz (sade X)
            c.drawLine(x, y, x + w, y + h, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.4, h * 0.20), Color=C("#B3301F", 235)))
            c.drawLine(x, y + h, x + w, y, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.4, h * 0.20), Color=C("#B3301F", 235)))
        elif fk % 3 == 1:                                                       # kartal: kara gövde + iki kanat (stilize)
            cxp, cyp = x + w * 0.5, y + h * 0.55
            c.drawOval(skia.Rect.MakeLTRB(cxp - w * 0.07, cyp - h * 0.30, cxp + w * 0.07, cyp + h * 0.32), _pt("#1A1008", 240))
            c.drawPath(sk.poly_path([(cxp, cyp - h * 0.1), (cxp - w * 0.32, cyp - h * 0.40), (cxp - w * 0.22, cyp + h * 0.08)]), _pt("#1A1008", 240))
            c.drawPath(sk.poly_path([(cxp, cyp - h * 0.1), (cxp + w * 0.32, cyp - h * 0.40), (cxp + w * 0.22, cyp + h * 0.08)]), _pt("#1A1008", 240))
        c.restore()
        c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C(INK, 190)))


def circling_birds(c, cx, cy, rx, ry, t, n=6, seed=1, size=1.0, col="#2A1A0C"):
    """Kule çevresinde dönen kuşlar (elips yörünge; kanat çırpar; önde/arkada ölçek değişir)."""
    rs = _RS(seed)
    for i in range(n):
        w = (0.30 + 0.12 * rs.rand()) * (1 if i % 2 else -1)
        ph = rs.uniform(0, 6.28)
        a = t * w + ph
        bx = cx + math.cos(a) * rx * (0.7 + 0.3 * rs.rand())
        by = cy + math.sin(a) * ry + math.sin(t * 0.8 + i) * 8
        near = 0.5 + 0.5 * math.sin(a)
        s_ = (0.7 + 0.5 * near) * size
        fl = math.sin(t * 9.0 + i * 2.3) * 5.5
        pth = skia.Path()
        pth.moveTo(bx - 9 * s_, by + fl * s_ * 0.4)
        pth.quadTo(bx - 4 * s_, by - 4 * s_ - fl * s_, bx, by)
        pth.quadTo(bx + 4 * s_, by - 4 * s_ - fl * s_, bx + 9 * s_, by + fl * s_ * 0.4)
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0 * s_, Color=C(col, 200), StrokeCap=skia.Paint.kRound_Cap))


def smoke_column(c, x, y, t, h=500.0, w=90.0, col="#5A5048", seed=1, wind=60.0, a0=0.5, glow_col="#E8803A", glow_a=0.35, n=30):
    """Uzakta yükselen kalın duman sütunu (stilize): tabanında sıcak parıltı, yükseldikçe genişler/eğilir/solar. Ceset/kan/yağma ayrıntısı yok."""
    im = _soft_dot(col, 64, 1.15)
    rs = _RS(seed)
    if glow_a > 0:
        glow(c, x, y, w * 1.5, glow_col, glow_a)
    for i in range(n):
        per = 7.0 + 3.0 * rs.rand()
        ph = (t / per + i / n + rs.rand() * 0.04) % 1.0
        r = w * (0.36 + 1.15 * ph)
        px = x + wind * ph ** 1.4 * (h / 400.0) + math.sin(ph * 6.0 + i * 1.3) * w * 0.20 * ph
        py = y - h * ph
        a = a0 * math.sin(math.pi * min(1.0, ph * 1.25)) ** 0.8 * (1 - ph) ** 0.30
        _blit_dot(c, im, px, py, r, a)
        _blit_dot(c, im, px + w * 0.10, py + r * 0.15, r * 0.7, a * 0.7)


def bale_tower(c, cx, yb, tw, Hs, T, seed=3, depth=0.0):
    """Çan kulesi yün balyalarıyla sarılı: çekirdek tuğla gövde + sıra sıra balyalar (kaydırmalı), üstte taş galeri (top platformu) ve çan odası. Dönüş: dict(top, deck=(x,y,w), flag)."""
    brick = T("#B4704A", depth)
    R(c, cx - tw / 2, yb - Hs, cx + tw / 2, yb, brick)
    rs = _RS(seed)
    bh = tw * 0.30
    bw0 = tw * 0.52
    rows = int(Hs / (bh * 0.94)) + 1
    for r_ in range(rows):
        yy = yb - (r_ + 1) * bh * 0.94
        if yy < yb - Hs - bh * 0.3:
            break
        off = (r_ % 2) * bw0 * 0.5
        x = cx - tw / 2 - 10 - off
        while x < cx + tw / 2 + 10:
            wv = bw0 * rs.uniform(0.92, 1.08)
            wool_bale(c, x, yy, wv, bh, seed=int(rs.randint(0, 10 ** 6)), col=T(mix("#EADFC4", "#CDBE9A", rs.rand() * 0.5), depth))
            x += wv - 2
    # kule kenarlarını taşan balyaları düzeltmek için yan gölge
    R(c, cx + tw * 0.34, yb - Hs, cx + tw / 2 + 12, yb, "#1A1008", 26)
    # üst galeri (taş platform + korkuluk)
    gy = yb - Hs
    R(c, cx - tw * 0.80, gy - 14, cx + tw * 0.80, gy + 4, T("#8A7452", depth))
    for k in range(7):
        c.drawPath(sk.poly_path([(cx - tw * 0.80 + k * tw * 1.6 / 7, gy + 4), (cx - tw * 0.80 + (k + 0.5) * tw * 1.6 / 7, gy + 16), (cx - tw * 0.80 + (k + 1) * tw * 1.6 / 7, gy + 4)]), _pt("#3A2A1C", 190))
    INKR(c, cx - tw * 0.80, gy - 14, cx + tw * 0.80, gy + 4, 1.2, 170)
    for k in range(6):                                                         # korkuluk dişleri (balya çuvalı ile örtülü)
        R(c, cx - tw * 0.80 + k * tw * 1.6 / 6, gy - 34, cx - tw * 0.80 + k * tw * 1.6 / 6 + tw * 1.6 / 12, gy - 14, T("#8A7452", depth))
    # çan odası
    bw_ = tw * 0.92
    bh_ = tw * 0.95
    R(c, cx - bw_ / 2, gy - 14 - bh_, cx + bw_ / 2, gy - 14, T("#CFA882", depth))
    for sgn in (-1, 1):
        c.drawPath(arch_path(cx + sgn * bw_ * 0.22, gy - 24, bw_ * 0.28, bh_ * 0.72), _pt("#22160D", 235))
    c.drawRect(skia.Rect.MakeLTRB(cx - bw_ / 2, gy - 14 - bh_, cx + bw_ / 2, gy - 14), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 170)))
    roof = sk.poly_path([(cx - bw_ * 0.58, gy - 14 - bh_), (cx, gy - 14 - bh_ - tw * 0.62), (cx + bw_ * 0.58, gy - 14 - bh_)])
    c.drawPath(roof, _pt(T("#B4552E", depth)))
    INKP(c, roof, 1.2, 175)
    top = gy - 14 - bh_ - tw * 0.62
    c.drawLine(cx, top, cx, top - tw * 0.45, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.4, Color=C(INK, 220)))
    return dict(top=top - tw * 0.45, flag=(cx, top - tw * 0.45), deck=(cx, gy - 14, tw * 1.6))


def san_miniato_front(c, x0, y, w, h, T, depth=0.0):
    """San Miniato al Monte cephesi (stilize): beyaz-yeşil mermer panelli alt arkad, üstte alınlık + mozaik, arkada alçak nef gövdesi ve çatısı. x0 sol, y zemin."""
    x1 = x0 + w
    nave_w = w * 0.95
    R(c, x1 - 4, y - h * 0.58, x1 + nave_w, y, T("#E3DAC2", depth))                                # nef gövdesi (arkada, sağa)
    c.drawPath(sk.poly_path([(x1 - 6, y - h * 0.58), (x1 + 20, y - h * 0.82), (x1 + nave_w - 10, y - h * 0.82), (x1 + nave_w + 8, y - h * 0.58)]), _pt(T("#A8502C", depth)))
    for k in range(1, 5):
        c.drawLine(x1 + 14 - k * 2, y - h * 0.58 - k * h * 0.06, x1 + nave_w - 4 + k * 0, y - h * 0.58 - k * h * 0.06, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#5A2412", 80)))
    for k in range(5):
        c.drawPath(arch_path(x1 + 40 + k * nave_w / 5.2, y - h * 0.18, 18, 46), _pt("#2A2018", 200))
    c.drawRect(skia.Rect.MakeLTRB(x1 - 4, y - h * 0.58, x1 + nave_w, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 160)))
    R(c, x0, y - h * 0.66, x1, y, T("#EFE9D8", depth))
    n = 5
    for i in range(n):                                                                             # alt arkad: 5 kemer
        ax = x0 + (i + 0.5) * w / n
        c.drawPath(arch_path(ax, y, w / n * 0.66, h * 0.50), _pt("#2A2018", 235))
        INKP(c, arch_path(ax, y, w / n * 0.66, h * 0.50), 1.0, 160)
    for i in range(n + 1):
        R(c, x0 + i * w / n - 7, y - h * 0.50, x0 + i * w / n + 7, y, T("#C7D0BE", depth))
    R(c, x0, y - h * 0.58, x1, y - h * 0.50, T("#4A6E5A", depth))
    for k in range(int(w / 22)):
        R(c, x0 + k * 22 + 4, y - h * 0.575, x0 + k * 22 + 14, y - h * 0.505, T("#EFE9D8", depth))
    R(c, x0 + w * 0.03, y - h * 0.66, x1 - w * 0.03, y - h * 0.58, T("#D8C48A", depth))
    R(c, x0 + w * 0.12, y - h * 1.0, x1 - w * 0.12, y - h * 0.66, T("#EFE9D8", depth))
    for k in range(3):
        c.drawPath(arch_path(x0 + w * (0.30 + 0.20 * k), y - h * 0.70, w * 0.06, h * 0.12), _pt("#3A2A1C", 215))
    pedi = sk.poly_path([(x0 + w * 0.10, y - h * 1.0), (x0 + w * 0.5, y - h * 1.30), (x1 - w * 0.10, y - h * 1.0)])
    c.drawPath(pedi, _pt(T("#EFE9D8", depth)))
    mos = sk.poly_path([(x0 + w * 0.22, y - h * 1.04), (x0 + w * 0.5, y - h * 1.22), (x1 - w * 0.22, y - h * 1.04)])
    c.drawPath(mos, _pt(T("#2E4F8A", depth)))
    c.drawCircle(x0 + w * 0.5, y - h * 1.09, w * 0.05, _pt(T("#E0B84E", depth)))
    for rr_ in (pedi, mos):
        INKP(c, rr_, 1.2, 170)
    c.drawRect(skia.Rect.MakeLTRB(x0, y - h * 0.66, x1, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 165)))
    c.drawRect(skia.Rect.MakeLTRB(x0 + w * 0.12, y - h * 1.0, x1 - w * 0.12, y - h * 0.66), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 165)))


def castel_sant_angelo(c, x, yb, s, T, depth=0.0, col="#B09A72"):
    """Castel Sant'Angelo (silindirik kale): mazgallı kare taban + dört yuvarlak köşe burcu (yan görünümde iki uç), kalın silindir gövde (kör kemer şeridi),
    üstte daha küçük silindir kule + mazgal; x orta, yb zemin; s ölçek (gövde genişliği ≈ 400·s)."""
    stone = T(col, depth)
    stone2 = T(mix(col, "#2A1A0C", 0.30), depth)
    # taban blok + yan burçlar
    bw, bh = 640 * s, 120 * s
    R(c, x - bw / 2, yb - bh, x + bw / 2, yb, stone)
    for r_ in range(4):
        R(c, x - bw / 2, yb - bh + r_ * bh / 4, x + bw / 2, yb - bh + r_ * bh / 4 + 1.5, stone2, 150)
    for sgn in (-1, 1):
        bx = x + sgn * (bw / 2)
        c.drawOval(skia.Rect.MakeLTRB(bx - 66 * s, yb - bh * 1.12, bx + 66 * s, yb - bh * 0.1), _pt(stone))
        R(c, bx - 66 * s, yb - bh * 0.62, bx + 66 * s, yb, stone)
        c.drawPath(arch_path(bx, yb - bh * 0.1, 14 * s, 42 * s), _pt("#241810", 225))
        crenel(c, bx - 60 * s, bx + 60 * s, yb - bh * 1.18, 15 * s, 18 * s, 9 * s, T, depth, col="#8A7452")
        INKR(c, bx - 66 * s, yb - bh * 0.62, bx + 66 * s, yb, 1.3, 160)
    crenel(c, x - bw / 2 + 60 * s, x + bw / 2 - 60 * s, yb - bh - 18 * s, 20 * s, 18 * s, 12 * s, T, depth, col="#8A7452")
    c.drawRect(skia.Rect.MakeLTRB(x - bw / 2, yb - bh, x + bw / 2, yb), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 170)))
    # silindir gövde
    dw, dh = 430 * s, 190 * s
    y0 = yb - bh
    sh = skia.GradientShader.MakeLinear([(x - dw / 2, 0), (x + dw / 2, 0)], [C(mix(stone, "#FFF4DC", 0.20)), C(stone), C(mix(stone, "#2A1A0C", 0.38))], [0.0, 0.45, 1.0])
    c.drawRect(skia.Rect.MakeLTRB(x - dw / 2, y0 - dh, x + dw / 2, y0), skia.Paint(Shader=sh))
    for r_ in range(1, 7):                                                       # taş sıraları (hafif eğri)
        yy = y0 - r_ * dh / 7
        c.drawLine(x - dw / 2, yy, x + dw / 2, yy + 3, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#4A3A22", 80)))
    na = 9                                                                       # kör kemer şeridi
    for i in range(na):
        ax = x - dw / 2 + (i + 0.5) * dw / na
        c.drawPath(arch_path(ax, y0 - dh * 0.58, dw / na * 0.46, dh * 0.34), _pt("#2A1E14", 140 + int(55 * (1 - abs(i - na / 2) / (na / 2)))))
    R(c, x - dw / 2 - 6 * s, y0 - dh - 18 * s, x + dw / 2 + 6 * s, y0 - dh + 4, T("#8A7452", depth))
    crenel(c, x - dw / 2 - 4 * s, x + dw / 2 + 4 * s, y0 - dh - 40 * s, 22 * s, 22 * s, 12 * s, T, depth, col="#8A7452")
    c.drawRect(skia.Rect.MakeLTRB(x - dw / 2, y0 - dh, x + dw / 2, y0), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 170)))
    # üst küçük kule + bayrak direği
    uw, uh = 200 * s, 96 * s
    yt = y0 - dh - 18 * s
    R(c, x - uw / 2, yt - uh, x + uw / 2, yt, T("#B8A47C", depth))
    for k in range(3):
        c.drawPath(arch_path(x - uw * 0.30 + k * uw * 0.30, yt - 8 * s, 28 * s, 56 * s), _pt("#241810", 220))
    crenel(c, x - uw / 2 - 4 * s, x + uw / 2 + 4 * s, yt - uh - 20 * s, 16 * s, 20 * s, 10 * s, T, depth, col="#8A7452")
    c.drawRect(skia.Rect.MakeLTRB(x - uw / 2, yt - uh, x + uw / 2, yt), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 170)))
    c.drawLine(x, yt - uh - 20 * s, x, yt - uh - 100 * s, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(2.4, 3.2 * s), Color=C(INK, 225)))
    return dict(flag=(x, yt - uh - 98 * s), top=yt - uh - 100 * s, left=x - bw / 2, right=x + bw / 2)


KS_PLAT = 690                    # plato (San Miniato tepesi) ana düzlem y
KS_TX, KS_TW, KS_THS = 1100, 140, 268          # balyalı çan kulesi: x, genişlik, balyalı gövde yüksekliği
KS_CHX = 1440                    # kilise cephesi sol x
KS_W0, KS_W1 = 1980, 3250        # sur duvarı aralığı


def bale_tower_geom(cx, yb, tw, Hs):
    """bale_tower'ın çizimsiz geometrisi: bayrak noktası, top güvertesi."""
    gy = yb - Hs
    top = gy - 14 - tw * 0.95 - tw * 0.62
    return dict(flag=(cx, top - tw * 0.45), deck=(cx, gy - 14, tw * 1.6), top=top - tw * 0.45)


def ks_ground(x):
    """San Miniato tepesi zemin profili (ana düzlem y): plato → iniş → vadi → karşı yamaç."""
    if x < 1900:
        return KS_PLAT + 6 * math.sin(x / 190.0)
    if x < 2800:
        u = (x - 1900) / 900.0
        return _lerp(KS_PLAT, 792, u * u * (3 - 2 * u))
    if x < 3250:
        return 792 + 4 * math.sin(x / 90.0)
    u = min(1.0, (x - 3250) / 700.0)
    return _lerp(792, 735, u * u * (3 - 2 * u))


class KaleSur(SWorld):
    name = "sehir_kale_sur"
    PW = 3800
    _draw_sky = PN.Florence._draw_sky
    _draw_hills = PN.Florence._draw_hills
    dyn_sky = PN.Florence.dyn_sky
    CAMP = (100, 2300)
    TENT_Y = (534, 545, 557)
    TENT_SZ = (26, 31, 37)

    def build(self):
        PW = self.PW
        cam_span = PW - W

        def Lw(f):
            return int(W + cam_span * f + 500)
        self.cloud_seed = 11
        rr = _RS(8)
        self.city_houses = []
        x = -40
        while x < Lw(0.46) + 60:
            bw, bh = rr.uniform(44, 90), rr.uniform(34, 80)
            self.city_houses.append((x, bw, bh, int(rr.randint(1, 10 ** 6)), 0.32, 0))
            x += bw + rr.uniform(-6, 8)
        self.layer("sky", 0.05, Lw(0.05), self._draw_sky, opaque=True, scale=0.5, wear=3, loss=0.5, yr=(0, 700))
        self.layer("hills", 0.12, Lw(0.12), self._draw_hills, scale=0.5, wear=2, yr=(330, 800))
        self.layer("camp", 0.22, Lw(0.22), self._draw_camp, wear=2, yr=(380, 760))
        self.layer("city", 0.46, Lw(0.46), self._draw_city2, wear=2, yr=(260, 760))
        self.layer("main", 1.0, PW, self._draw_main, wear=4)
        self.tg = bale_tower_geom(KS_TX, KS_PLAT, KS_TW, KS_THS)

    def default_cams(self, act=None, p=None):                       # yavaş pull: balyalı kuleye yakından başlar, geri açılıp surları ve ufuktaki çadırları gösterir
        return [(0.0, (1180, -150, 1.46)), (0.55, (1460, -40, 1.16)), (1.0, (1860, 36, 1.0))]

    def stack(self, ctx):
        return [("L", "sky"), ("D", "dyn_sky", 0.05), ("L", "hills"), ("L", "camp"), ("D", "dyn_camp", 0.22), ("L", "city"), ("D", "dyn_city", 0.46), ("L", "main"), ("D", "dyn_main", 1.0), ("D", "dyn_front", 1.30)]

    def _draw_camp(self, fr, xa, xb):
        c = fr.c
        T = self.T
        GRAD_V(c, xa, 520, xb, 760, [(T("#CDBC90", 0.55), 0.0), (T("#BCA974", 0.45), 0.5), (T("#A89A62", 0.3), 1.0)])
        for i, (yy, sz) in enumerate(zip(self.TENT_Y, self.TENT_SZ)):
            tent_row(c, max(xa - 80, self.CAMP[0]), min(xb + 80, self.CAMP[1]), yy, sz, T, seed=11 + i, depth=0.55 - 0.05 * i)
        GRAD_V(c, xa, 500, xb, 590, [("#E8D6A8", 0.0, 0), ("#E8D6A8", 0.55, 80), ("#E8D6A8", 1.0, 0)])          # ufuk tozu

    def _draw_city2(self, fr, xa, xb):
        c = fr.c
        T = self.T
        wins = []
        for (x, bw, bh, sd, dep, dy) in self.city_houses:
            if x + bw < xa - 60 or x > xb + 60:
                continue
            rs = _RS(sd)
            CT.draw_house(c, x, 640 + (rs.rand() * 8 - 4), bw, bh, rs, T, dep, wins)
        base = 646
        XD = 1500
        if xa - 900 < XD < xb + 900:
            CT.draw_nave(c, XD + 60, XD + 480, base + 4, 100, T, 0.24)
            CT.draw_dome(c, XD, base - 88, 176, 108, 40, 60, T, 0.22)
            CT.draw_campanile(c, XD + 178, base + 4, 44, 210, T, 0.22)
            CT.draw_pv(c, XD + 800, base + 4, 0.80, T, 0.28)
        GRAD_V(c, xa, 636, xb, 760, [(T("#97A468", 0.3), 0.0), (T("#8C9A5A", 0.2), 1.0)])

    def _draw_main(self, fr, xa, xb):
        c = fr.c
        T = self.T
        PW = self.PW
        pts = [(xa - 8, ks_ground(xa - 8))]
        x = xa - 8
        while x <= xb + 8:
            pts.append((x, ks_ground(x)))
            x += 12
        poly = pts + [(pts[-1][0], 960), (pts[0][0], 960)]
        sh = skia.GradientShader.MakeLinear([(0, 660), (0, 960)], [C(T("#A8B067", 0.0)), C(T("#8C9A55", 0.0)), C(T("#6E7A42", 0.0))], [0.0, 0.5, 1.0])
        c.drawPath(sk.poly_path(poly), skia.Paint(AntiAlias=True, Shader=sh))
        c.drawPath(sk.poly_path(pts, False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.8, Color=C(INK, 140)))
        rs = _RS(int(xa) // 7 + 5)
        for i in range(int((xb - xa) / 9)):                                       # çimen çizgileri + koyu/açık yama
            gx = rs.uniform(xa, xb)
            gy = ks_ground(gx) + rs.uniform(6, 170)
            c.drawLine(gx, gy, gx + rs.uniform(-3, 3), gy - rs.uniform(5, 14), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#4E5A2A" if rs.rand() < 0.6 else "#B8C078", 130)))
        for i in range(int((xb - xa) / 120)):
            gx = rs.uniform(xa, xb)
            OVAL(c, gx, ks_ground(gx) + rs.uniform(30, 150), rs.uniform(40, 120), rs.uniform(8, 20), "#5A6A30", 40)
        # toprak yol: platodan yamaçtan iner
        pj = []
        for gx in range(1250, 3000, 20):
            pj.append((gx, ks_ground(gx) + 46 + 9 * math.sin(gx / 60.0)))
        if not (pj[-1][0] < xa - 40 or pj[0][0] > xb + 40):
            c.drawPath(sk.poly_path([(p_[0], p_[1] - 8) for p_ in pj] + [(p_[0], p_[1] + 11) for p_ in pj[::-1]]), _pt(T("#CDBB8C", 0.0), 190))
        # San Miniato + balyalı çan kulesi (plato)
        if xa < KS_CHX + 1000 and xb > 400:
            san_miniato_front(c, KS_CHX, KS_PLAT, 400, 214, T)
            bale_tower(c, KS_TX, KS_PLAT, KS_TW, KS_THS, T, seed=3)
            rs2 = _RS(55)
            for (bx0, rows_) in ((820, 3), (1280, 2), (1900, 3)):                  # yerde balya yığınları
                for r_ in range(rows_):
                    for k in range(rows_ - r_):
                        wool_bale(c, bx0 + k * 70 + r_ * 35, KS_PLAT - (r_ + 1) * 40 + 10, 68, 42, seed=int(rs2.randint(0, 10 ** 6)))
            dx_, dy_, dw_ = self.tg["deck"]
            cannon(c, dx_ - dw_ * 0.36, dy_ - 14, 0.66, -1)                          # tepede iki top siluet (namlular dışa)
            cannon(c, dx_ + dw_ * 0.36, dy_ - 14, 0.66, 1)
        # Floransa surları: yamacı izleyen duvar
        if xb > KS_W0 - 60 and xa < KS_W1 + 60:
            xs = list(range(max(KS_W0, int(xa) - 30), min(KS_W1, int(xb) + 30), 10))
            if len(xs) > 1:
                top = [(x_, ks_ground(x_) - 20 - 96) for x_ in xs]
                bot = [(x_, ks_ground(x_) + 6) for x_ in xs]
                wall = sk.poly_path(top + bot[::-1])
                shw = skia.GradientShader.MakeLinear([(0, 560), (0, 900)], [C(T("#C4AE84", 0.0)), C(T("#A8926A", 0.0))], [0.0, 1.0])
                c.drawPath(wall, skia.Paint(AntiAlias=True, Shader=shw))
                c.save()
                c.clipPath(wall, skia.ClipOp.kIntersect, True)
                jp = skia.Path()
                for r_ in range(6):
                    for x_ in xs[::5]:
                        jy = ks_ground(x_) - 20 - 96 + r_ * 18
                        jp.moveTo(x_, jy)
                        jp.lineTo(x_ + 50, jy + 0.5)
                        jp.moveTo(x_ + (r_ % 2) * 25, jy)
                        jp.lineTo(x_ + (r_ % 2) * 25, jy + 18)
                c.drawPath(jp, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#4A3A22", 95)))
                c.restore()
                c.drawPath(sk.poly_path(top, False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=C(INK, 175)))
                for x_ in range(int(max(KS_W0, xa - 30)) // 34 * 34, int(min(KS_W1, xb + 30)), 34):
                    yy = ks_ground(x_) - 20 - 96
                    R(c, x_, yy - 20, x_ + 18, yy + 2, T("#A8926A", 0.0))
                    c.drawRect(skia.Rect.MakeLTRB(x_, yy - 20, x_ + 18, yy + 2), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C(INK, 150)))
                    c.drawPath(arch_path(x_ + 9, yy + 44, 6, 24), _pt("#241810", 160))
                for tx in (2290, 2740, 3150):                                          # kuleler
                    if xa - 90 < tx < xb + 90:
                        gy = ks_ground(tx)
                        R(c, tx - 44, gy - 168, tx + 44, gy + 4, T("#B9A37A", 0.0))
                        crenel(c, tx - 50, tx + 50, gy - 190, 18, 22, 10, T, 0.0, col="#8A7452")
                        for ry in (0.38, 0.66):
                            c.drawPath(arch_path(tx, gy - 168 * (1 - ry) - 20, 8, 28), _pt("#241810", 225))
                        c.drawRect(skia.Rect.MakeLTRB(tx - 44, gy - 168, tx + 44, gy + 4), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 175)))
                        R(c, tx + 28, gy - 168, tx + 44, gy + 4, "#1A1008", 36)
                gx_ = 3000                                                              # kapı kulesi
                if xa - 110 < gx_ < xb + 110:
                    gy = ks_ground(gx_)
                    R(c, gx_ - 70, gy - 186, gx_ + 70, gy + 4, T("#B09A72", 0.0))
                    crenel(c, gx_ - 76, gx_ + 76, gy - 210, 20, 24, 10, T, 0.0, col="#8A7452")
                    c.drawPath(arch_path(gx_, gy + 2, 62, 110), _pt("#1E140C", 245))
                    INKP(c, arch_path(gx_, gy + 2, 62, 110), 1.4, 190)
                    c.drawRect(skia.Rect.MakeLTRB(gx_ - 70, gy - 186, gx_ + 70, gy + 4), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, Color=C(INK, 180)))
                for gx2 in range(2000, 2900, 70):                                      # hasır sepetler (cesto)
                    if xa - 60 < gx2 < xb + 60:
                        gabion(c, gx2, ks_ground(gx2) - 116, 40, 42, T, seed=gx2)
        # servi ağaçları + ön taşlar
        rs3 = _RS(66)
        for i in range(40):
            tx = rs3.uniform(0, PW)
            if not (xa - 40 < tx < xb + 40):
                continue
            if KS_W0 - 40 < tx < KS_W1 + 70 or KS_CHX - 40 < tx < KS_CHX + 520 or abs(tx - KS_TX) < 150:
                continue
            SC.cypress(c, tx, ks_ground(tx) + 5, rs3.uniform(96, 170), T("#2E4A33", 0.0), T("#4F6E4A", 0.0))
        for i in range(40):
            tx = rs3.uniform(0, PW)
            if xa - 20 < tx < xb + 20:
                OVAL(c, tx, ks_ground(tx) + rs3.uniform(50, 160), rs3.uniform(8, 22), rs3.uniform(3, 8), "#7A6A48", 80)

    # ── dinamik ──
    def dyn_camp(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        for i, (yy, sz) in enumerate(zip(self.TENT_Y, self.TENT_SZ)):
            pts = []
            for tt in tent_layout(max(xa - 80, self.CAMP[0]), min(xb + 80, self.CAMP[1]), yy, sz, 11 + i):
                if tt["flag"]:
                    pts.append((tt["x"] + tt["w"] * 0.02 + 0.8, tt["y"] - tt["h"] - tt["pole"], tt["fk"], sz))
            tent_flags(c, pts, t, 1.0)
        rs = _RS(81)
        for i in range(18):                                                       # ocak dumanları (ince)
            x = 150 + i * 118 + rs.uniform(-30, 30)
            if x < xa - 40 or x > xb + 40:
                continue
            smoke_plume(c, x, 545 + (i % 3) * 8, t, size=13, n=4, k=0.9, col="#B8A88A", seed=i, rise=90, wind=30, a0=0.40)
        dust = _soft_dot("#D8C69C", 64, 1.1)
        for i in range(10):                                                       # sürüklenen toz bulutları
            ph = (t * 0.05 + i * 0.131) % 1.0
            _blit_dot(c, dust, 120 + i * 210 + ph * 320, 552 + (i % 3) * 10, 70 + 26 * math.sin(i * 1.7), 0.22 * math.sin(math.pi * ph))
        FA.atmo_birds(c, t, 4, 1.0, xa, xb, 380, 500, speed=18.0, night=ctx.night, seed=21, size=0.6)

    def dyn_city(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        rs = _RS(33)
        for i in range(14):
            x = 120 + i * 230 + rs.uniform(-40, 40)
            if x < xa - 40 or x > xb + 40:
                continue
            smoke_plume(c, x, 586, t, size=20, n=5, k=0.8, col="#B8B0A4", seed=i + 3, rise=130, wind=26, a0=0.34)

    def dyn_main(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        fx_, fy_ = self.tg["flag"]
        flag_pennant(c, fx_ + 1, fy_ + 2, t, 54.0, 19.0, "#B3301F", seed=1)
        circling_birds(c, fx_ + 20, fy_ + 170, 200, 70, t, 6, seed=4)
        for i, tx in enumerate((2290, 2740, 3150, 3000)):
            if xa - 90 < tx < xb + 90:
                gy = ks_ground(tx)
                top = gy - (232 if tx == 3000 else 190) - 6
                c.drawLine(tx, top, tx, top - 70, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.4, Color=C(INK, 225)))
                flag_pennant(c, tx + 1, top - 68, t, 40.0, 15.0, "#E0B84E" if i % 2 else "#B3301F", seed=i * 2 + 1)
        fluff = _soft_dot("#F6EEDB", 24, 1.2)                                     # rüzgârda uçuşan yün tutamları
        for i in range(12):
            ph = (t * 0.10 + i * 0.121) % 1.0
            px = KS_TX - 90 + ph * 560 + math.sin(t * 1.3 + i * 2.1) * 12
            py = KS_PLAT - 60 - i * 20 - ph * 100 + math.sin(t * 2.0 + i) * 8
            _blit_dot(c, fluff, px, py, 4.0 + (i % 3), 0.8 * math.sin(math.pi * ph))

    def dyn_front(self, ctx):
        """Ön plan (1,30): rüzgârda salınan uzun otlar."""
        c, t = ctx.c, ctx.t
        rs = _RS(91)
        p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2, Color=C("#4E5A2A", 210), StrokeCap=skia.Paint.kRound_Cap)
        for i in range(80):
            gx = ctx.xa + rs.uniform(0, 1) * (ctx.xb - ctx.xa)
            gy = 846 + rs.uniform(0, 40)
            hh = rs.uniform(30, 70)
            sw = math.sin(t * 2.0 + gx * 0.02 + i) * 8 + math.sin(t * 3.4 + i * 1.7) * 3
            pth = skia.Path()
            pth.moveTo(gx, gy)
            pth.quadTo(gx + sw * 0.4, gy - hh * 0.6, gx + sw, gy - hh)
            p.setColor(C("#4E5A2A" if i % 3 else "#8E9A4E", 215))
            c.drawPath(pth, p)


# ─────────── Roma 1527: Castel Sant'Angelo + Passetto ───────────
def _draw_sky_smoky(self, fr, xa, xb):
    """Dumanlı gök (gün: gri-mavi → kül-ocher → turuncu ufuk; yumuşak duman bantları); dusk/night: Florence gökleri."""
    if self.tod != "day":
        return PN.Florence._draw_sky(self, fr, xa, xb)
    c = fr.c
    GRAD_V(c, xa, 0, xb, 760, [("#76828E", 0.0), ("#B9AE9C", 0.50), ("#E6C18F", 0.86), ("#F2CB92", 1.0)])
    R(c, xa, 759, xb, 960, "#F2CB92")
    rs = _RS(int(xa) // 7 + 17)
    for i in range(int((xb - xa) / 300) + 1):
        x = xa + rs.uniform(0, 300) + i * 300
        y = rs.uniform(OV + 60, 470)
        for k in range(3):
            c.drawOval(skia.Rect.MakeLTRB(x + k * 80, y - 10, x + k * 80 + 260, y + 14), skia.Paint(AntiAlias=True, Color=C("#6A625C", 46), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10)))
    GRAD_V(c, xa, 480, xb, 700, [("#E8803A", 0.0, 0), ("#E8803A", 0.7, 52), ("#E8803A", 1.0, 70)])           # ufukta ateş ışığının sıcak yansıması


def _rome_far(self, fr, xa, xb):
    """Uzak Roma silueti (0,34): çatılar, kuleler, şemsiye çamları, eski San Pietro cephesi (stilize); gün/dusk/night Tint."""
    c = fr.c
    T = self.T
    wins = []
    for (x, bw, bh, sd, dep, dy) in self.city_houses:
        if x + bw < xa - 60 or x > xb + 60:
            continue
        rs = _RS(sd)
        CT.draw_house(c, x, 700 + dy + (rs.rand() * 8 - 4), bw, bh, rs, T, dep, wins)
    for tx, th in ((300, 210), (880, 170), (1650, 232), (2300, 186), (2980, 214), (3500, 176)):
        if xa - 80 < tx < xb + 80:
            CT.draw_tower(c, tx, 700, 30, th, T, 0.34, spire=(tx % 3 == 0))
    XP = 1230                                                                              # eski San Pietro (cephe + nef + çan kulesi)
    if xa - 600 < XP < xb + 600:
        R(c, XP - 210, 700 - 150, XP + 210, 700, T("#E6D6B0", 0.30))
        c.drawPath(sk.poly_path([(XP - 190, 700 - 150), (XP, 700 - 262), (XP + 190, 700 - 150)]), _pt(T("#C9B890", 0.30)))
        INKP(c, sk.poly_path([(XP - 190, 700 - 150), (XP, 700 - 262), (XP + 190, 700 - 150)]), 1.2, 150)
        for k in range(7):
            c.drawPath(arch_path(XP - 156 + k * 52, 700, 26, 72), _pt(T("#3A2A1C", 0.3), 190))
        R(c, XP + 214, 700 - 220, XP + 252, 700, T("#C4AE88", 0.30))
        c.drawPath(sk.poly_path([(XP + 210, 700 - 220), (XP + 233, 700 - 262), (XP + 256, 700 - 220)]), _pt(T("#A8502C", 0.30)))
        INKR(c, XP - 210, 700 - 150, XP + 210, 700, 1.2, 140)
    rs = _RS(int(xa) // 11 + 3)
    for i in range(int((xb - xa) / 180) + 1):                                              # şemsiye çamları
        x = xa + i * 180 + rs.uniform(0, 140)
        SC.umbrella_pine(c, x, 706, rs.uniform(86, 130), T("#3C5A38", 0.34))
    if self.tod != "day":
        PN._lit_boxes(c, _RS(int(xa) % 997 + 1), wins, True, 0.34 if self.tod == "night" else 0.14)


class KaleCastel(SWorld):
    name = "sehir_kale_castel"
    PW = 4200
    _draw_sky = _draw_sky_smoky
    _draw_hills = PN.Florence._draw_hills
    dyn_sky = PN.Florence.dyn_sky
    _draw_city = _rome_far
    CX = 2420                                  # kale merkezi
    BASE = 790                                 # kale/duvar zemin hizası (ana düzlem)
    CS = 1.22                                  # kale ölçeği

    def build(self):
        PW = self.PW
        cam_span = PW - W

        def Lw(f):
            return int(W + cam_span * f + 500)
        self.cloud_seed = 13
        rr = _RS(12)
        self.city_houses = []
        x = -40
        while x < Lw(0.34) + 60:
            bw, bh = rr.uniform(40, 86), rr.uniform(34, 76)
            self.city_houses.append((x, bw, bh, int(rr.randint(1, 10 ** 6)), 0.42, 0))
            x += bw + rr.uniform(-6, 8)
        self.layer("sky", 0.05, Lw(0.05), self._draw_sky, opaque=True, scale=0.5, wear=3, loss=0.5, yr=(0, 700))
        self.layer("hills", 0.12, Lw(0.12), self._draw_hills, scale=0.5, wear=2, yr=(330, 800))
        self.layer("city", 0.34, Lw(0.34), self._draw_city, wear=2, yr=(260, 760))
        self.layer("main", 1.0, PW, self._draw_main, wear=4)
        self.layer("river", 0.9, Lw(0.9), self._draw_river, yr=(600, 900))
        self.tgeo = None

    def default_cams(self, act=None, p=None):
        return [(0.0, (1650, 60, 1.0)), (1.0, (2330, 40, 1.16))]                    # yavaş itme: Passetto duvarından kaleye

    def stack(self, ctx):
        return [("L", "sky"), ("D", "dyn_sky", 0.05), ("L", "hills"), ("L", "city"), ("D", "dyn_city", 0.34), ("L", "main"), ("D", "dyn_main", 1.0), ("L", "river"), ("D", "dyn_river", 0.9), ("D", "dyn_front", 1.3)]

    def _draw_river(self, fr, xa, xb):
        c = fr.c
        T = self.T
        GRAD_V(c, xa, self.BASE + 4, xb, 900, [(T("#7FA0A0", 0.1), 0.0), (T("#4E7C86", 0.0), 0.5), (T("#2E566A", 0.0), 1.0)])
        rs = _RS(int(xa) // 3 + 5)
        for i in range(int((xb - xa) / 12)):
            yy = rs.uniform(self.BASE + 14, 880)
            x = rs.uniform(xa, xb)
            L = rs.uniform(14, 56)
            c.drawLine(x, yy, x + L, yy, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4 + (yy - self.BASE) * 0.012, Color=C("#FFFFFF" if rs.rand() < 0.55 else "#1E3A4A", int(rs.uniform(26, 72))), StrokeCap=skia.Paint.kRound_Cap))
        if self.tod == "dusk":                                                                # gökyüzü yansıması (turuncu → mor)
            GRAD_V(c, xa, self.BASE + 4, xb, 900, [("#FF9A4A", 0.0, 120), ("#C0607A", 0.5, 90), ("#4A3A7A", 1.0, 70)])
        elif self.tod == "day":
            GRAD_V(c, xa, self.BASE + 4, xb, 900, [("#E8A060", 0.0, 70), ("#6A8CA0", 1.0, 20)])
        R(c, xa, self.BASE - 2, xb, self.BASE + 8, T("#7C6C4E", 0.0))                      # rıhtım kenarı
        c.drawLine(xa, self.BASE + 8, xb, self.BASE + 8, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=C(INK, 150)))

    def _draw_main(self, fr, xa, xb):
        c = fr.c
        T = self.T
        B = self.BASE
        PW = self.PW
        # Passetto: kalın taş duvar + kör kemer sırası + üstte örtülü koridor (ok yarıkları, kiremit çatı, mazgal dişleri)
        W0, W1 = -200, self.CX - 520 * self.CS / 1.22
        if xb > W0 and xa < W1 + 60:
            x0, x1 = max(W0, xa - 10), min(W1, xb + 10)
            stone_wall(c, W0, B - 200, W1, B, "#C6B18A", T, 0.0, 41, ch=34, bw=(80, 140), rustic=False, joint_a=90, clip=(xa, xb))
            nar = int((W1 - W0) / 190)
            for i in range(nar):                                                              # kör kemerler
                ax = W0 + (i + 0.5) * (W1 - W0) / nar
                if ax < xa - 100 or ax > xb + 100:
                    continue
                c.drawPath(arch_path(ax, B, (W1 - W0) / nar * 0.62, 150), _pt(T("#6A5A40", 0.0), 215))
                INKP(c, arch_path(ax, B, (W1 - W0) / nar * 0.62, 150), 1.1, 150)
            R(c, x0, B - 214, x1, B - 196, T("#CDBB92", 0.0))
            c.drawLine(x0, B - 196, x1, B - 196, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 160)))
            # üstte koridor gövdesi
            R(c, x0, B - 314, x1, B - 214, T("#D3BF98", 0.0))
            stone_wall(c, W0, B - 314, W1, B - 214, "#D3BF98", T, 0.0, 43, ch=24, bw=(60, 100), rustic=False, joint_a=70, clip=(xa, xb))
            gx = int(x0 // 86) * 86
            while gx < x1 + 86:                                                              # ok yarıkları
                c.drawPath(arch_path(gx + 43, B - 232, 12, 52), _pt("#1E140C", 235))
                gx += 86
            R(c, x0, B - 336, x1, B - 312, T("#A8502C", 0.0))                                # çatı saçağı
            c.drawLine(x0, B - 336, x1, B - 336, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C(INK, 160)))
            for k in range(1, 4):
                c.drawLine(x0, B - 336 + k * 6, x1, B - 336 + k * 6, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#5A2412", 90)))
            crenel(c, W0, W1, B - 360, 22, 24, 14, T, 0.0, col="#8A7452")
            R(c, x1 - 28, B - 360, x1, B, "#1A1008", 32)
        # Castel Sant'Angelo
        if xa - 600 < self.CX < xb + 600:
            castel_sant_angelo(c, self.CX, B, self.CS, T, col="#B27C58")
            c.drawPath(arch_path(self.CX, B, 78 * self.CS, 104 * self.CS), _pt("#1E140C", 245))                  # giriş kapısı (kapı + kemer)
            INKP(c, arch_path(self.CX, B, 78 * self.CS, 104 * self.CS), 1.4, 190)
        # sağ: rıhtım duvarı + alçak Borgo evleri + torrione
        RX0 = self.CX + 420
        if xb > RX0 - 40:
            stone_wall(c, RX0, B - 130, PW + 100, B, "#B09A72", T, 0.0, 47, ch=30, bw=(80, 130), rustic=False, joint_a=88, clip=(xa, xb))
            crenel(c, RX0, PW + 100, B - 152, 20, 22, 12, T, 0.0, col="#8A7452")
            for tx in (self.CX + 940, self.CX + 1540):
                if xa - 80 < tx < xb + 80:
                    R(c, tx - 40, B - 220, tx + 40, B, T("#B9A37A", 0.0))
                    crenel(c, tx - 46, tx + 46, B - 244, 17, 22, 10, T, 0.0, col="#8A7452")
                    c.drawPath(arch_path(tx, B - 100, 8, 30), _pt("#241810", 225))
                    INKR(c, tx - 40, B - 220, tx + 40, B, 1.3, 170)
        # servi/çam
        rs = _RS(77)
        for i in range(26):
            tx = rs.uniform(0, PW)
            if xa - 40 < tx < xb + 40 and not (self.CX - 520 < tx < self.CX + 520) and tx > W1:
                SC.umbrella_pine(c, tx, B - 130 + 6, rs.uniform(90, 140), T("#3C5A38", 0.0))

    def dyn_city(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        # uzaktaki Roma'dan yükselen duman sütunları (stilize; olay yok)
        for i, (sx, h, w_) in enumerate(((520, 560, 86), (980, 470, 72), (1380, 640, 100), (1760, 500, 78), (2150, 600, 96), (2530, 470, 74), (2900, 590, 90), (3300, 460, 70))):
            if xa - 200 < sx < xb + 200:
                smoke_column(c, sx, 700, t, h=h, w=w_, col="#322A28" if ctx.tod == "day" else "#2A2634", seed=i + 1, wind=80, a0=0.85, glow_a=0.45 if ctx.tod != "day" else 0.30)
        FA.atmo_birds(c, t, 6, 1.0, xa, xb, 250, 480, speed=20.0, night=ctx.night, seed=9, size=0.8)

    def dyn_main(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        B = self.BASE
        s_ = self.CS
        fx_, fy_ = self.CX, B - 522 * s_
        if xa - 100 < fx_ < xb + 100:
            flag_pennant(c, fx_ + 1, fy_ + 2, t, 70.0, 26.0, "#E0B84E", seed=2)
            circling_birds(c, fx_, fy_ + 190 * s_, 380 * s_, 100, t, 8, seed=8)
        for sgn in (-1, 1):                                                            # burç direkleri: flama
            bx = self.CX + sgn * 320 * s_
            if xa - 80 < bx < xb + 80:
                top = B - 120 * s_ * 1.18 - 18 * s_
                c.drawLine(bx, top, bx, top - 96, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.4, Color=C(INK, 225)))
                flag_pennant(c, bx + 1, top - 94, t, 38.0, 15.0, "#B3301F", seed=3 + sgn)
        # Passetto üstünde direkler/flamalar
        for px in range(100, int(self.CX - 600), 560):
            if xa - 60 < px < xb + 60:
                c.drawLine(px, B - 360, px, B - 430, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2, Color=C(INK, 220)))
                flag_pennant(c, px + 1, B - 428, t, 32.0, 12.0, "#B3301F" if (px // 560) % 2 else "#E0B84E", seed=px % 7)
        # küller (havada uçuşan, çok seyrek): ash_field
        ash_field(c, (xa + xb) / 2, 560, t, n=26, span=1400, wind=70, k=0.55, seed=3)

    def dyn_river(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        rs = _RS(14)
        col = "#FFF4D0" if ctx.night else "#FFFFFF"
        for i in range(34):
            yy = self.BASE + 16 + rs.uniform(0, 74)
            k = (yy - self.BASE) / 90.0
            L = 16 + 40 * k
            span = (xb - xa) + 200
            xx = xa - 100 + (rs.uniform(0, span) + t * (6 + 12 * k)) % span
            al = (0.22 + 0.22 * math.sin(t * 1.7 + i * 1.3) ** 2) * (0.6 if ctx.night else 1.0)
            c.drawLine(xx, yy, xx + L, yy, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4 + 1.2 * k, Color=C(col, int(255 * al)), StrokeCap=skia.Paint.kRound_Cap))

    def dyn_front(self, ctx):
        pass

    def grade(self, ctx):
        _grade_generic(self, ctx)


# Passetto (örtülü koridor) — yan görünüm tek plan
YF = 700            # koridor zemin arka kenarı
YFOOT = 744         # figür ayak hizası
YCE = 334           # tavan alt hizası
BAYW = 420          # sütun aralığı


def passetto_slits(xa, xb):
    """Ok yarığı konumları (her bayın ortası)."""
    i0 = max(0, int(xa // BAYW) - 1)
    return [(i + 0.5) * BAYW for i in range(i0, int(xb // BAYW) + 2) if xa - 40 <= (i + 0.5) * BAYW <= xb + 40]


class KalePassetto(SWorld):
    name = "sehir_kale_passetto"
    PW = 5600
    _draw_sky = _draw_sky_smoky
    _draw_hills = PN.Florence._draw_hills
    dyn_sky = PN.Florence.dyn_sky
    _draw_city = _rome_far

    def build(self):
        PW = self.PW
        cam_span = PW - W

        def Lw(f):
            return int(W + cam_span * f + 500)
        self.cloud_seed = 15
        rr = _RS(18)
        self.city_houses = []
        x = -40
        while x < Lw(0.30) + 60:
            bw, bh = rr.uniform(44, 96), rr.uniform(60, 150)
            self.city_houses.append((x, bw, bh, int(rr.randint(1, 10 ** 6)), 0.40, 0))
            x += bw + rr.uniform(-6, 8)
        self.layer("sky", 0.05, Lw(0.05), self._draw_sky, opaque=True, scale=0.5, wear=3, loss=0.5, yr=(0, 700))
        self.layer("hills", 0.12, Lw(0.12), self._draw_hills, scale=0.5, wear=2, yr=(330, 800))
        self.layer("city", 0.30, Lw(0.30), self._draw_city, wear=2, yr=(260, 760))
        self.layer("main", 1.0, PW, self._draw_main, wear=4)
        self.cast = []                                                                           # heyet: (tür, seed, dx(ekranda), boy, prop)
        self.cast = [("asker", 4, 360, 250, "halberd"), ("asker", 9, 300, 252, "halberd"), ("asker", 13, 214, 248, "halberd"),
                     ("kardinal", 3, 120, 236, None), ("papa", 2, 24, 240, None), ("kardinal", 5, -70, 234, None),
                     ("rahip", 7, -150, 230, None), ("asker", 17, -222, 250, "halberd"), ("asker", 21, -296, 248, "halberd"), ("asker", 25, -366, 250, "halberd")]

    def default_cams(self, act=None, p=None):
        dur = (p or {}).get("_dur", 14.0)
        v = 168.0
        keys = [(f_, (900 + v * dur * f_, 0, 1.0)) for f_ in (0.0, 0.25, 0.5, 0.75, 1.0)]
        return keys

    def stack(self, ctx):
        return [("L", "sky"), ("D", "dyn_sky", 0.05), ("L", "hills"), ("L", "city"), ("D", "dyn_city", 0.30), ("L", "main"), ("D", "dyn_main", 1.0), ("D", "dyn_front", 1.32)]

    def _draw_main(self, fr, xa, xb):
        c = fr.c
        T0 = self.T
        T = lambda col, d=0.0: mix(T0(col, d), "#1A1008", 0.34)                    # koridor içi loş: figürler/meşale ışığı öne çıkar  # noqa: E731
        PW = self.PW
        cl = (xa, xb)
        # çatı kenarı + kiremit (koridorun dışı: üstte)
        R(c, xa, YCE - 58, xb, YCE - 6, T0("#A8502C", 0.0))
        for k in range(1, 5):
            c.drawLine(xa, YCE - 58 + k * 10, xb, YCE - 58 + k * 10, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#5A2412", 90)))
        tj = skia.Path()
        gx = int(xa // 24) * 24
        while gx < xb + 24:
            tj.moveTo(gx, YCE - 58)
            tj.lineTo(gx, YCE - 6)
            gx += 24
        c.drawPath(tj, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#5A2412", 55)))
        c.drawLine(xa, YCE - 58, xb, YCE - 58, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 165)))
        for mx in range(int(xa // 40) * 40, int(xb) + 40, 40):                                       # çatı sırtında mazgal dişleri (örtülü koridor çatısı)
            R(c, mx, YCE - 76, mx + 22, YCE - 58, T0("#8A7452", 0.0))
            c.drawRect(skia.Rect.MakeLTRB(mx, YCE - 76, mx + 22, YCE - 58), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C(INK, 150)))
        R(c, xa, YCE - 8, xb, YCE + 6, T("#CDBB92", 0.0))                                          # saçak taşı
        # geri duvar (sıva + taş izi)
        GRAD_V(c, xa, YCE + 6, xb, YF, [(T("#CDB78C", 0.0), 0.0), (T("#D8C59C", 0.0), 0.55), (T("#BFA980", 0.0), 1.0)])
        stone_wall(c, 0, YCE + 6, PW, YF, "#D2BE94", T, 0.0, 51, ch=36, bw=(90, 150), rustic=False, joint_a=40, clip=cl)
        # tavan kirişleri (koyu tonoz bandı) + pilastr/kemer sırası
        GRAD_V(c, xa, YCE + 6, xb, YCE + 60, [("#1A120A", 0.0, 235), ("#1A120A", 1.0, 0)])
        i0 = max(0, int(xa // BAYW) - 1)
        for i in range(i0, int(xb // BAYW) + 3):
            px = i * BAYW
            if px < xa - 80 or px > xb + 80:
                continue
            R(c, px - 22, YCE + 6, px + 22, YF, T("#B9A57C", 0.0))                                   # pilastr
            R(c, px + 8, YCE + 6, px + 22, YF, "#1A1008", 40)
            R(c, px - 30, YCE + 6, px + 30, YCE + 26, T("#CDBB92", 0.0))                              # başlık
            R(c, px - 28, YF - 22, px + 28, YF, T("#A8946C", 0.0))                                    # kaide
            INKR(c, px - 22, YCE + 26, px + 22, YF - 22, 1.1, 130)
            # kemer (sığ)
            cxp = px + BAYW / 2
            p = skia.Path()
            p.moveTo(px + 22, YCE + 70)
            p.cubicTo(px + 90, YCE + 20, px + BAYW - 90, YCE + 20, px + BAYW - 22, YCE + 70)
            c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=14, Color=C(T("#C0AC84", 0.0))))
            c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 140)))
        # ok yarıkları: geri duvarda dar delikler (arkadaki gökyüzü/şehir/duman görünür) + ışık huzmesi
        for sx in passetto_slits(xa, xb):
            hole = arch_path(sx, 590, 24, 128)
            splay = sk.poly_path([(sx - 34, 596), (sx - 12, 590), (sx - 12, 462), (sx - 34, 456)])
            splay2 = sk.poly_path([(sx + 34, 596), (sx + 12, 590), (sx + 12, 462), (sx + 34, 456)])
            c.drawPath(splay, _pt("#8C7A58", 190))
            c.drawPath(splay2, _pt("#7A6A4A", 190))
            c.drawPath(hole, skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kClear))
            INKP(c, hole, 1.3, 190)
            sh = skia.GradientShader.MakeLinear([(0, 470), (0, YFOOT + 20)], [C("#FFC278", 70), C("#FFC278", 26), C("#FFC278", 4)], [0.0, 0.7, 1.0])
            shaft = sk.poly_path([(sx - 12, 470), (sx + 12, 470), (sx + 150, YFOOT + 14), (sx + 52, YFOOT + 14)])
            c.drawPath(shaft, skia.Paint(AntiAlias=True, Shader=sh))
        # zemin: taş döşeme (arkadan öne) + alt kalın duvar (kesit)
        GRAD_V(c, xa, YF, xb, YFOOT + 34, [(T("#8E7C58", 0.0), 0.0), (T("#B09C74", 0.0), 0.6), (T("#9C8862", 0.0), 1.0)])
        c.drawLine(xa, YF, xb, YF, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 150)))
        pj = skia.Path()
        gx = int(xa // 70) * 70
        while gx < xb + 70:
            pj.moveTo(gx, YF)
            pj.lineTo(gx - 26, YFOOT + 34)
            gx += 70
        for k in range(1, 5):
            pj.moveTo(xa, YF + k * 10)
            pj.lineTo(xb, YF + k * 10)
        c.drawPath(pj, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#4A3A22", 90)))
        stone_wall(c, 0, YFOOT + 34, PW, 900, "#A8926A", T, 0.0, 53, ch=34, bw=(80, 140), rustic=False, joint_a=95, clip=cl)
        for i in range(int(xa // 300) - 1, int(xb // 300) + 2):                                   # alt kör kemerler
            ax = (i + 0.5) * 300
            c.drawPath(arch_path(ax, 900, 180, 108), _pt(T("#5E4E36", 0.0), 215))
        R(c, xa, YFOOT + 30, xb, YFOOT + 40, T("#C6B488", 0.0))
        c.drawLine(xa, YFOOT + 40, xb, YFOOT + 40, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 160)))

    def dyn_city(self, ctx):
        c, t = ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        for i, (sx, h, w_) in enumerate(((300, 560, 74), (760, 470, 62), (1250, 640, 86), (1730, 520, 70), (2200, 600, 80), (2700, 480, 64), (3200, 620, 84))):
            if xa - 200 < sx < xb + 200:
                smoke_column(c, sx, 700, t, h=h, w=w_, col="#2E2824" if ctx.tod == "day" else "#2E2C3A", seed=i + 5, wind=80, a0=0.92, glow_a=0.45)
        FA.atmo_birds(c, t, 5, 1.0, xa, xb, 200, 330, speed=22.0, night=ctx.night, seed=19, size=0.8)

    def dyn_main(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        # meşale/fener: yarıkların arasında duvar konsolları
        for sx in passetto_slits(xa - 400, xb + 400):
            tx = sx + BAYW * 0.5
            if xa - 60 < tx < xb + 60:
                torch_bracket(c, tx, 560)
                torch_flame(c, tx - 7, 544, t, size=46.0, seed=int(tx) % 40)
            glow(c, sx, 530, 130 * (0.9 + 0.1 * math.sin(t * 2.1 + sx)), "#FFB04A", 0.22)
            glow(c, sx + BAYW * 0.5, 540, 190 * (0.92 + 0.08 * math.sin(t * 7.3 + sx)), "#FF9A3A", 0.30)                # meşale ışık havuzu
        # ışık huzmelerinde süzülen toz
        dot = _soft_dot("#FFE2A8", 24, 1.2)
        for sx in passetto_slits(xa - 100, xb + 100):
            for k in range(6):
                ph = (t * (0.12 + 0.03 * k) + k * 0.17 + sx * 0.003) % 1.0
                px = sx - 10 + ph * (150 + 40 * k % 3) * 0.9 + math.sin(t * 1.4 + k) * 6
                py = 480 + ph * (YFOOT - 470)
                _blit_dot(c, dot, px, py, 2.6 + (k % 3), 0.7 * math.sin(math.pi * ph))
        # heyet: kamera hızına eşit zemin hızıyla hızla yürür (ayak kaymaz); Papa'yı muhafızlar ve kardinaller sarmalar
        v = max(0.0, ctx.cam_vx)
        base = ctx.camx
        jost = math.sin(t * 3.0)
        order = []
        for (kind, sd, dx, hh, prop) in self.cast:
            x = base + dx - 40 + 10 * math.sin(t * 2.2 + dx * 0.02) + 6 * jost
            y = YFOOT + (6 if kind in ("papa",) else 0) - (8 if kind == "asker" and dx > 0 else 0) + 4 * math.sin(dx)
            order.append((y, kind, sd, x, hh, prop, dx))
        order.sort(key=lambda q: q[0])
        for (y, kind, sd, x, hh, prop, dx) in order:
            if x < xa - 200 or x > xb + 200:
                continue
            stil = dict(robe="#F2EDE0", robe2="#E0B84E") if kind == "papa" else {}
            FA.walker(f, kind, x, y, hh, t, speed=max(v, 1.0), dir=1, phase=((dx * 0.0031) % 1.0), seed=sd, prop=prop, **stil)

    def dyn_front(self, ctx):
        """Ön plan (1,32): koridorun önündeki kalın taş payandalar (figürler arkalarından geçer)."""
        c = ctx.c
        for i in range(0, 14):
            px = 700 + i * 1180
            if px < ctx.xa - 80 or px > ctx.xb + 80:
                continue
            R(c, px - 32, 60, px + 32, 900, "#4A3C2E", 255)
            R(c, px - 32, 60, px - 18, 900, "#6A5844", 255)
            R(c, px + 16, 60, px + 32, 900, "#22180F", 255)
            R(c, px - 46, 60, px + 46, 92, "#5A4A38", 255)
            R(c, px - 44, 846, px + 44, 900, "#5A4A38", 255)
            c.drawLine(px - 32, 92, px - 32, 846, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 180)))
            c.drawLine(px + 32, 92, px + 32, 846, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 180)))

    def prepare(self, ctx):
        super().prepare(ctx)
        pc = ctx.pc
        dt = 0.05
        ctx.cam_vx = (pc.at(clamp(ctx.t + dt, 0, ctx.cx.dur))[0] - pc.at(clamp(ctx.t - dt, 0, ctx.cx.dur))[0]) / (2 * dt)

    def grade(self, ctx):
        _grade_generic(self, ctx)



# ═════════════════════════════ SKYLINE DİKEY (Palazzo Vecchio kulesine tek dikey plan: crane up) ═════════════════════════════
class VLayer:
    """Dikey kareaşlı paralaks katmanı: genişlik LW, yükseklik LH; kareaşlar yukarıdan aşağı 1024 satırlık dilimler; disk önbelleği `sehir_*`.
    draw(fr, r0, r1): katman tuval koordinatında (y aşağı; satır 0 = katmanın tepesi; zemin = LH) [r0,r1] satırlarını çizer."""
    TH = 1024

    def __init__(self, world, name, fy, width, ground, pad, draw, tod="day", fx=0.0):
        self.world, self.name, self.fy, self.fx = world, name, fy, fx
        self.ground, self.pad = int(ground), int(pad)
        self.width, self.height, self.draw, self.tod = int(width), int(ground + pad), draw, tod
        self.tiles = {}

    def n_tiles(self):
        return int(math.ceil(self.height / self.TH))

    def _path(self, i):
        return os.path.join(CACHE, f"{self.world}_{self.tod}_{self.name}_{i}_{VER}.png")

    def tile(self, i):
        t = self.tiles.get(i)
        if t is None:
            t = self.tiles[i] = self._bake(i)
        return t

    def _bake(self, i):
        path = self._path(i)
        try:
            if os.path.exists(path):
                a = cv2.imread(path, cv2.IMREAD_UNCHANGED)
                if a is not None and a.shape[2] == 4:
                    return sk.np_to_image(cv2.cvtColor(a, cv2.COLOR_BGRA2RGBA))
        except Exception:   # noqa: BLE001
            pass
        r0 = i * self.TH
        r1 = min(self.height, r0 + self.TH)
        fr = sk.Frame(self.width, int(r1 - r0))
        fr.clear(skia.ColorTRANSPARENT)
        c = fr.c
        c.translate(0, -r0)
        c.clipRect(skia.Rect.MakeLTRB(0, r0, self.width, r1))
        self.draw(fr, r0, r1)
        img = fr.surf.makeImageSnapshot()
        try:
            os.makedirs(CACHE, exist_ok=True)
            arr = img.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kUnpremul_AlphaType)
            cv2.imwrite(path, cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA), [cv2.IMWRITE_PNG_COMPRESSION, 1])
        except Exception:   # noqa: BLE001
            pass
        return img

    def draw_view(self, c, hcam, camx, z, cyb):
        """Ekranda görünen kareaşları çiz. hcam: kamera yüksekliği (px, zeminden), cyb: bant merkezinin ekran y'si."""
        hl = hcam * self.fy                                             # katmanın ekran merkezindeki yüksekliği
        half = 420.0 / z + 40
        hlo, hhi = hl - half, hl + half
        cxl = W / 2 + (camx - W / 2) * (1.0 if self.fx else 1.0)
        for i in range(self.n_tiles()):
            top_h = self.ground - i * self.TH
            bot_h = top_h - min(self.TH, self.height - i * self.TH)
            if bot_h > hhi or top_h < hlo:
                continue
            img = self.tile(i)
            sy = cyb - (top_h - hl) * z
            sx = W / 2 - cxl * z
            c.save()
            c.translate(sx, sy)
            c.scale(z, z)
            c.drawImage(img, 0, 0, LIN)
            c.restore()


VH = 5200            # ana katman yüksekliği
VX = 1120            # kule ekseni (dünya x)
VTW = 290            # kule gövde genişliği
VHS = 3560           # kule gövdesi yüksekliği (taban 480'den)
VLW = 2300


def vt_geom():
    """Dikey sahnede kulenin yükseklik (zeminden) geometrisi: [gövde başı, galeri, çan odası, külah, direk üstü]."""
    tw = VTW
    base = 480
    gy = base + VHS
    gal_h = tw * 0.34
    b1 = gy + gal_h + 1
    b0 = b1 + tw * 1.15
    rh = tw * 0.95
    top = b0 + rh + tw * 0.55
    return dict(base=base, gal=gy, bell0=b1, bell1=b0, roof=b0 + rh, top=top, flag=top - 4)


class SkylineDikey(SWorld):
    name = "sehir_dikey"
    PW = VLW
    CAM_Y_SIGN = -1                      # cam=("crane","up",px): kamera yüksekliği artar (camy = zeminden yükseklik)

    def build(self):
        self.vl = {}
        self.vl["far"] = VLayer(self.name, "far", 0.10, VLW, 700, 760, self._draw_far, self.tod)
        self.vl["city"] = VLayer(self.name, "city", 0.22, VLW, 900, 760, self._draw_city_v, self.tod)
        self.vl["mid"] = VLayer(self.name, "mid", 0.50, VLW, 2000, 760, self._draw_mid_v, self.tod)
        self.vl["main"] = VLayer(self.name, "main", 1.0, VLW, VH, 760, self._draw_main_v, self.tod)
        self.vl["near"] = VLayer(self.name, "near", 1.45, VLW, 760, 0, self._draw_near_v, self.tod)
        self.layers = {k: v for k, v in self.vl.items()}
        self.G = vt_geom()
        rs = _RS(7)
        self.clouds = [(rs.uniform(-200, VLW), rs.uniform(250, 4600), rs.uniform(300, 760), rs.uniform(4, 14), rs.uniform(0.55, 0.95)) for _ in range(34)]

    def bake_all(self, cam_x_range=None):
        n = 0
        for L in self.vl.values():
            for i in range(L.n_tiles()):
                L.tile(i)
                n += 1
        return n

    def default_cams(self, act=None, p=None):
        g = self.G
        return [(0.0, (VX, 300, 1.14)), (0.30, (VX - 30, 1500, 1.06)), (0.70, (VX + 20, 3500, 1.02)), (0.90, (VX, g["top"] - 250, 1.0)), (1.0, (VX, g["top"] - 250, 1.0))]

    # ── katman boyaları (satır = LH - yükseklik) ──
    def _draw_far(self, fr, r0, r1):
        c = fr.c
        T = self.T
        LH = 700
        for (col, amp, sc, base, ph) in (("#A9BDB6", 40, 600, 330, 0.0), ("#93AFA5", 46, 420, 250, 2.1), ("#7F9E92", 52, 300, 170, 4.3)):
            cc = T(col, 0.2)
            pts = []
            x = -8
            while x <= VLW + 8:
                pts.append((x, LH - PN.ridge_y(x, base, amp, sc, ph)))
                x += 10
            poly = pts + [(pts[-1][0], LH + 800), (pts[0][0], LH + 800)]
            c.drawPath(sk.poly_path(poly), skia.Paint(AntiAlias=True, Color=C(cc)))
            c.drawPath(sk.poly_path(pts, False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, Color=C(mix(cc, "#1A2A22", 0.5), 150)))
            for gi in range(int(VLW // 150) + 1):
                r_ = _RS(gi * 7 + int(ph * 10) + 1)
                if r_.rand() < 0.55:
                    x = gi * 150 + r_.uniform(0, 150)
                    SC.cypress(c, x, LH - PN.ridge_y(x, base, amp, sc, ph) + 3, r_.uniform(30, 54), T("#2E4A33", 0.3), T("#4F6E4A", 0.3))
                if r_.rand() < 0.10:
                    SC.castle(c, gi * 150 + 70, LH - PN.ridge_y(gi * 150 + 70, base, amp, sc, ph) + 3, r_.uniform(26, 38), T("#E6D9B8", 0.3), T("#B4552E", 0.3))

    def _draw_city_v(self, fr, r0, r1):
        c = fr.c
        T = self.T
        LH = 900
        rr = _RS(5)
        wins = []
        x = -40
        while x < VLW + 40:
            bw, bh = rr.uniform(44, 94), rr.uniform(34, 84)
            rs = _RS(int(rr.randint(1, 10 ** 6)))
            CT.draw_house(c, x, LH - 120 + (rs.rand() * 8 - 4), bw, bh, rs, T, 0.40, wins)
            x += bw + rr.uniform(-6, 8)
        base = LH - 124
        XD = 700
        c.save()
        c.translate(XD, base)
        c.scale(1.5, 1.5)
        c.translate(-XD, -base)
        CT.draw_nave(c, XD + 70, XD + 640, base + 4, 124, T, 0.26)
        CT.draw_dome(c, XD, base - 108, 214, 132, 48, 74, T, 0.22)
        CT.draw_campanile(c, XD + 205, base + 4, 54, 262, T, 0.22)
        c.restore()
        for tx, th in ((200, 210), (1500, 250), (1860, 180), (2150, 220)):
            CT.draw_tower(c, tx, base, 32, th, T, 0.32, spire=(tx == 1500))
        GRAD_V(c, 0, LH - 124, VLW, LH + 800, [(T("#B8A888", 0.35), 0.0), (T("#A89A78", 0.30), 1.0)])
        rs2 = _RS(61)
        for i in range(int(VLW / 70)):                                                      # alt çatı sıraları: ufuk altı yoğun kiremit dokusu
            hx = i * 70 + rs2.uniform(-10, 10)
            hy = LH - 110 + rs2.uniform(0, 600)
            bw_, bh_ = rs2.uniform(50, 100), rs2.uniform(30, 60)
            CT.draw_house(c, hx, hy, bw_, bh_, _RS(int(rs2.randint(1, 10 ** 6))), T, 0.34, wins)
        if self.tod != "day":
            PN._lit_boxes(c, _RS(21), wins, True, 0.4 if self.tod == "night" else 0.16)

    def _draw_mid_v(self, fr, r0, r1):
        c = fr.c
        T = self.T
        LH = 2000
        DEP = 0.52                                                                   # uzak kuleler: sisli (atmosferik perspektif)

        def slender(x, w, h, spire):
            yb = LH - 20
            col = "#D8C8A4" if spire else "#C8B48C"
            stone_wall(c, x - w / 2, yb - h, x + w / 2, yb, col, T, DEP, 90 + int(x) % 50, ch=40, bw=(w * 0.4, w * 0.7), rustic=False, joint_a=45)
            c.drawRect(skia.Rect.MakeLTRB(x - w / 2, yb - h, x + w / 2, yb), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 110)))
            for k in range(int(h / 300)):
                c.drawPath(arch_path(x, yb - 140 - k * 300, w * 0.11, 50), _pt("#2A2018", 170))
            if spire:
                c.drawPath(sk.poly_path([(x - w * 0.62, yb - h), (x, yb - h - w * 2.6), (x + w * 0.62, yb - h)]), _pt(T("#8E8878", DEP)))
                R(c, x - w * 0.56, yb - h - 56, x + w * 0.56, yb - h + 2, T("#E6DCBF", DEP))
                for k in range(2):
                    c.drawPath(arch_path(x - w * 0.18 + k * w * 0.36, yb - h - 4, w * 0.20, 48), _pt("#2A1E14", 190))
            else:
                machico(c, x - w * 0.78, x + w * 0.78, yb - h, w * 0.30, T, DEP, unit=w * 0.22)
                crenel(c, x - w * 0.78, x + w * 0.78, yb - h - w * 0.52, w * 0.15, w * 0.22, w * 0.07, T, DEP)
        slender(250, 96, 1460, True)          # Badia (iğne külahlı)
        slender(1980, 104, 1240, False)       # Bargello (mazgallı)
        slender(2220, 84, 1700, True)
        slender(640, 80, 860, False)
        rs = _RS(29)
        wins = []
        x = -60
        while x < VLW + 60:                                                          # çatı sırası (ufka yakın, alçak) + zemin dolgusu
            bw, bh = rs.uniform(120, 220), rs.uniform(100, 250)
            CT.draw_house(c, x, LH - 4, bw, bh, _RS(int(rs.randint(1, 10 ** 6))), T, 0.40, wins)
            x += bw + rs.uniform(-8, 10)
        GRAD_V(c, 0, LH - 6, VLW, LH + 800, [(T("#C4B08A", 0.40), 0.0), (T("#B0A07A", 0.35), 1.0)])
        for i in range(int(VLW / 110)):
            hx = i * 110 + rs.uniform(-20, 20)
            CT.draw_house(c, hx, LH + 20 + rs.uniform(0, 640), rs.uniform(100, 170), rs.uniform(70, 150), _RS(int(rs.randint(1, 10 ** 6))), T, 0.36, wins)
        if self.tod != "day":
            PN._lit_boxes(c, _RS(33), wins, True, 0.4 if self.tod == "night" else 0.16)

    def _draw_main_v(self, fr, r0, r1):
        c = fr.c
        T = self.T
        LH = VH
        g = self.G
        yb = LH - g["base"]
        vecchio_tower(c, VX, yb, VTW, VHS, T, 0.0, 77, roof_h=VTW * 0.95)
        # kule gövdesine ince detay: kuşak silmeleri + küçük pencereler (yarıklar zaten çizildi)
        for hh in range(g["base"] + 520, g["base"] + VHS - 120, 520):
            R(c, VX - VTW / 2 - 4, LH - hh - 6, VX + VTW / 2 + 4, LH - hh + 4, T("#D6C49C", 0.0))
            c.drawLine(VX - VTW / 2 - 4, LH - hh + 4, VX + VTW / 2 + 4, LH - hh + 4, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 150)))
        for hh in range(g["base"] + 260, g["base"] + VHS - 200, 380):
            for sgn in (-1, 1):
                c.drawPath(arch_path(VX + sgn * VTW * 0.26, LH - hh, 12, 44), _pt("#241810", 225))
        # palazzo gövdesi (zemin: LH) + kaldırım dolgusu (zemin altı)
        PN.draw_pavement(c, 0, VLW, LH - 2, LH + 800, T, seed=3)
        palazzo_front(c, VX - 800, LH, 1600, 600, "vecchio", door=0.0, T=T, seed=31, tower=False)

    def _draw_near_v(self, fr, r0, r1):
        """Çok yakın çatılar (yalnız tırmanışın başında, ekran kenarlarında geçer): iri kiremit çatı + baca."""
        c = fr.c
        T = self.T
        LH = 760
        for (x0, x1, h) in ((-80, 360, 190), (1840, 2380, 150)):
            poly = [(x0, LH), (x0, LH - h), ((x0 + x1) / 2, LH - h - 90), (x1, LH - h), (x1, LH)]
            c.drawPath(sk.poly_path(poly), _pt(T("#B4552E", 0.0)))
            INKP(c, sk.poly_path(poly), 1.6, 190)
            for k in range(1, 8):
                c.drawLine(x0 + k * 6, LH - h - 90 * (1 - k / 8.0) + 30 * 0 + k * 10 - 10 * 0, x1 - k * 6, LH - h - 90 * (1 - k / 8.0) + k * 10, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#5A2412", 90)))
            R(c, x0 + 80, LH - h - 140, x0 + 130, LH - h - 40, T("#A8684A", 0.0))
            R(c, x0 + 72, LH - h - 154, x0 + 138, LH - h - 138, T("#8A5236", 0.0))

    # ── render ──
    def render(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        by0, bh = ctx.band
        h = ctx.camy                                      # kamera yüksekliği (zeminden px)
        z = ctx.z
        cyb = by0 + bh / 2
        g = self.G
        k = clamp(h / g["top"])
        tod = ctx.tod
        # gökyüzü degradesi (yüksekliğe göre derinleşir)
        if tod == "night":
            stops = [("#04081C", 0.0), ("#0C1A4A", 0.5), ("#3A5088", 1.0)]
        elif tod == "dusk":
            stops = [(mix("#4E5E9E", "#262A6A", k), 0.0), (mix("#E8A07A", "#B87898", k), 0.58), (mix("#F8D9A0", "#E6A878", k * 0.5), 1.0)]
        else:
            stops = [(mix("#6F9ED6", "#2E5CAA", k), 0.0), (mix("#BDD0DC", "#7EA4D4", k), 0.55), (mix("#F4E8C8", "#E4E4DC", k), 1.0)]
        sh = skia.GradientShader.MakeLinear([(0, by0), (0, by0 + bh)], [C(s_[0]) for s_ in stops], [s_[1] for s_ in stops])
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(0, by0, W, by0 + bh))
        c.drawRect(skia.Rect.MakeLTRB(0, by0, W, by0 + bh), skia.Paint(Shader=sh))
        if tod == "night":
            rs = _RS(3)
            for i in range(120):
                c.drawCircle(rs.uniform(0, W), by0 + rs.uniform(0, bh * 0.8), rs.uniform(0.8, 2.0), skia.Paint(AntiAlias=True, Color=C("#FFF2C4", int(rs.uniform(90, 230)))))
        # bulutlar (iki derinlik: 0,30 ve 0,70) + uzak katmanlar
        cl = PN.cloud_sprite()
        pt = skia.Paint()
        for (cx0, hc, L, sp, a_) in self.clouds:
            fyc = 0.30 if hc < 2400 else 0.62
            sy = cyb - (hc - h * fyc) * z
            if sy < by0 - 120 or sy > by0 + bh + 120:
                continue
            x = (cx0 + t * sp) % (VLW + 600) - 300
            sx = W / 2 + (x - (W / 2 + (ctx.camx - W / 2) * 0.1)) * z + W / 2 * 0
            pt.setAlphaf(a_ * (0.7 if tod != "day" else 1.0))
            c.drawImageRect(cl, skia.Rect.MakeWH(cl.width(), cl.height()), skia.Rect.MakeXYWH(sx - L * z * 0.5, sy - L * z * 0.11, L * z, L * z * 0.22), LIN, pt)
        for nm in ("far", "city", "mid"):
            self.vl[nm].draw_view(c, h, ctx.camx, z, cyb)
        # orta katman: kuş sürüleri (kulelerin çevresinde)
        # ana katman
        self.vl["main"].draw_view(c, h, ctx.camx, z, cyb)
        # ana düzlem dinamikleri (y: yükseklik → ekran)
        def sy_(hh):
            return cyb - (hh - h) * z

        def sx_(xx):
            return W / 2 + (xx - ctx.camx) * z
        c.save()
        c.translate(W / 2, cyb)
        c.scale(z, z)
        c.translate(-ctx.camx, h)                                  # artık (x, -yükseklik) koordinatı: yükseklik hh → y = -hh
        FA.set_scale_hint(z)
        # kule tepesi flaması + çan odası (sakin) + kuş halkaları
        flag_pennant(c, VX + 1, -(g["flag"]), t, 140.0, 48.0, "#B3301F", seed=2)
        circling_birds(c, VX + 30, -(g["flag"] - 260), 330, 120, t, 9, seed=3, size=1.6)
        for hh, nb, sd in ((1500, 6, 11), (2600, 7, 12), (3500, 6, 13)):
            if abs(hh - h) < 700:
                circling_birds(c, VX, -hh, 360, 90, t, nb, seed=sd, size=1.5)
        # kule yanlarından sarkan demir kollarda flamalar (yükselirken akan hareket) + yarıklardan havalanan güvercinler
        for i, hh in enumerate((860, 1480, 2100, 2720, 3340)):
            if abs(hh - h) > 640:
                continue
            side = 1 if i % 2 else -1
            bx = VX + side * VTW / 2
            c.drawLine(bx, -hh, bx + side * 44, -hh - 8, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.0, Color=C("#2A2622", 245), StrokeCap=skia.Paint.kRound_Cap))
            c.save()
            c.translate(bx + side * 44, -hh - 10)
            c.scale(side, 1)
            flag_pennant(c, 0, 0, t, 70.0, 26.0, ("#B3301F", "#E0B84E", "#233C8C")[i % 3], seed=i + 4, wind=1.0)
            c.restore()
        for kk, hh in enumerate(range(g["base"] + 260, g["base"] + VHS - 200, 380)):
            if abs(hh - h) > 640:
                continue
            for sgn in (-1, 1):
                per = 7.0 + (kk % 3) * 1.3 + (0.7 if sgn > 0 else 0.0)
                ph = (t / per + kk * 0.37 + (0.5 if sgn > 0 else 0.0)) % 1.0
                if ph > 0.38:
                    continue
                u = ph / 0.38
                bx = VX + sgn * VTW * 0.26 + sgn * u * 300
                by = -(hh + 20) - u * 120 + 60 * math.sin(math.pi * u) * 0.0
                fl = math.sin(t * 13.0 + kk + sgn) * 7
                pth = skia.Path()
                pth.moveTo(bx - 14, by + fl * 0.4)
                pth.quadTo(bx - 6, by - 7 - fl, bx, by)
                pth.quadTo(bx + 6, by - 7 - fl, bx + 14, by + fl * 0.4)
                c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.2, Color=C("#3A3430", int(255 * (1 - u ** 3))), StrokeCap=skia.Paint.kRound_Cap))
        # mazgallı galeri/dam kuşları: tepeden uçarak geçen sürü
        FA.atmo_birds(c, t, 8, 1.0, VX - 900, VX + 900, -(g["bell1"] - 200), -(g["bell1"] + 500), speed=30.0, night=(tod == "night"), seed=17, size=1.6)
        FA.atmo_birds(c, t, 6, 1.0, VX - 900, VX + 900, -(1400), -(2100), speed=24.0, night=(tod == "night"), seed=18, size=1.4)
        FA.set_scale_hint(1.0)
        c.restore()
        # ön yakın çatılar
        self.vl["near"].draw_view(c, h, ctx.camx, z, cyb)
        if tod != "night":                                                                      # tırmandıkça güneş parıltısı
            glow(c, W * 0.22, by0 + 130, 760, "#FFF1C0" if tod == "day" else "#FFC890", 0.10 + 0.22 * k)
        c.restore()
        # derecelendirme: alacakaranlık/gece
        if tod == "dusk":
            wash(c, by0, bh, [("#5A3E78", 56), ("#E8905A", 20), ("#E8905A", 40)], [0.0, 0.55, 1.0], 1.0)
        elif tod == "night":
            R(c, 0, by0, W, by0 + bh, "#0A1034", 70)


# ═════════════════════════════ sahne kayıtları + `sehir` çekim türü ═════════════════════════════
_SW = {}
TIMES = {}      # son karenin bölüm süreleri (ms): katman/dinamik/grade/fx — preview_sehir --ms dökümü için
ACT_TOD = {("meydan", "ates"): "dusk", ("meydan", "odun"): "night", ("meydan", "palle"): "day", ("meydan", "pencere"): "dusk", ("meydan", "kalabalik"): "day", ("kale", "castel"): "dusk"}
DEFAULT_ACT = {"meydan": "ates", "sokak": None, "kale": "sur", "skyline_dikey": None}
CLASSES = {}   # (scene, act|None) → sınıf; alt bölümlerde doldurulur


_CLEANED = []


def _clean_stale():
    """Eski sürümlerin kareaşlarını sil (yalnız bu modülün `sehir_*` dosyaları)."""
    if _CLEANED:
        return
    _CLEANED.append(1)
    try:
        for fn in os.listdir(CACHE):
            if fn.startswith("sehir_") and not fn.endswith(f"_{VER}.png"):
                try:
                    os.remove(os.path.join(CACHE, fn))
                except OSError:
                    pass
    except OSError:
        pass


def get_sworld(scene, act, tod):
    _clean_stale()
    cls = CLASSES.get((scene, act)) or CLASSES.get((scene, None))
    if cls is None:
        raise ValueError(f"sehir: bilinmeyen sahne/act: {scene!r}/{act!r} (meydan: ates|odun|palle|pencere · sokak · kale: sur|castel|passetto · skyline_dikey)")
    key = (cls.name, tod)
    w = _SW.get(key)
    if w is None:
        w = _SW[key] = cls(tod)
    return w


CLASSES[("meydan", None)] = Meydan
CLASSES[("sokak", None)] = Sokak
CLASSES[("kale", "sur")] = KaleSur
CLASSES[("skyline_dikey", None)] = SkylineDikey
CLASSES[("kale", "castel")] = KaleCastel
CLASSES[("kale", "passetto")] = KalePassetto


@ckind("sehir")
def k_sehir(cx, scene="meydan", act=None, tod=None, cams=None, actors=None, stations=None, kick=None, caption=None, at=0.0, frame=True, seed=1, band=None,
            door=None, door_at=None, items_at=None, fire_at=None, **kw):
    """Dış mekân/şehir dünyası. scene: meydan | sokak | kale | skyline_dikey; act: (meydan) ates|odun|palle|pencere|kalabalik · (kale) sur|castel|passetto.
    tod: day|dusk|night (yoksa act'e göre varsayılan). cams=[(çapa,(x,y,zoom)),…] (x: ana düzlemde ekran merkezi; y: + aşağı; skyline_dikey'de (x, yükseklik_px, zoom)).
    actors=[dict(kind, x0, y, h, dir, speed, action, seed, prop, flag, t0, cf)] ek figürler; stations=[dict(x, fn)] pano ile aynı. door="close"|"open", door_at=çapa (sokak).
    items_at=[çapa…] eşyaların yığına düştüğü anlar, fire_at=çapa ilk kıvılcım (meydan/ates). cam=("push"|"pull"|"pan"|"crane",…) `cams` yokken varsayılan yolun üstüne uygulanır."""
    f = cx.f
    c = f.c
    act = act or DEFAULT_ACT.get(scene)
    night_theme = not TH.day
    tod = tod or ACT_TOD.get((scene, act)) or ("night" if night_theme else "day")
    world = get_sworld(scene, act, tod)
    if band is None:
        band = (150, 800) if frame else (0, 800)
    a = cx.amt(at, 0.9) if at else 1.0
    dur = max(cx.dur, 1e-3)
    pdict = dict(scene=scene, act=act, actors=actors, items_at=items_at, fire_at=fire_at, door=door, door_at=door_at, _dur=dur, **{k: v for k, v in kw.items() if k not in ("cam",)})
    pc = PN.PanoCam(cx, cams, world.default_cams(act, pdict), dur)
    t_cam = clamp(cx.t, 0.0, dur)
    camx, camy, z = pc.at(t_cam)
    if not cams:
        dx, dy, zm = _cam_mod(getattr(cx, "cam_spec", None), ease_io(t_cam / dur))
        camx, camy, z = camx + dx, camy + dy * getattr(world, "CAM_Y_SIGN", 1), z * zm
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    mb0, mbh = band
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, 0, W, mb0 + 2))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    c.restore()
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, mb0 + mbh - 2, W, H))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    c.restore()
    ctx = PN.Ctx(f, cx, world, camx, camy, z, band if frame else (0, 800), tod, a)
    ctx.band = (band[0], band[1]) if frame else (140, 800)
    ctx.p = pdict
    ctx.pc = pc
    sts = stations if stations is not None else world.default_stations()
    ctx.stations = []
    for s_ in sts:
        s2 = dict(s_)
        s2["_at"] = float(s2["at_frac"]) * dur if ("at_frac" in s2 and "at" not in s2) else _anchor(cx, s2.get("at", 0.0))
        ctx.stations.append(s2)
    world.prepare(ctx)
    by0, bh = ctx.band
    if hasattr(world, "render"):                                  # kendi çizim akışı olan dünya (skyline_dikey)
        TIMES.clear()
        t0_ = time.perf_counter()
        world.render(ctx)
        TIMES["_toplam_sahne"] = (time.perf_counter() - t0_) * 1000
        c.save()
        c.restore()
        return _sehir_finish(f, cx, c, ctx, world, tod, frame, by0, bh, a, kick, caption, at)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, by0, W, by0 + bh))
    tm = TIMES
    tm.clear()
    pc0 = time.perf_counter()
    for item in world.stack(ctx):
        kind = item[0]
        t0_ = time.perf_counter()
        if kind == "L":
            L = world.layers[item[1]]
            dy_ = item[2] if len(item) > 2 else 0.0
            ctx.xf(L.f, dy_)
            xa, xb = ctx.view(L.f)
            L.draw_view(c, xa, xb)
            ctx.end()
            key = "L:" + item[1]
        elif kind == "D":
            fct = item[2]
            dy_ = item[3] if len(item) > 3 else 0.0
            ctx.xf(fct, dy_)
            xa, xb = ctx.view(fct)
            ctx.xa, ctx.xb = xa, xb
            getattr(world, item[1])(ctx)
            ctx.end()
            key = item[1]
        tm[key] = tm.get(key, 0.0) + (time.perf_counter() - t0_) * 1000
    t0_ = time.perf_counter()
    world.grade(ctx)
    tm["grade"] = (time.perf_counter() - t0_) * 1000
    if hasattr(world, "fx"):
        t0_ = time.perf_counter()
        xa, xb = ctx.view(1.0)
        ctx.xa, ctx.xb = xa, xb
        world.fx(ctx)
        tm["fx"] = (time.perf_counter() - t0_) * 1000
    c.restore()
    tm["_toplam_sahne"] = (time.perf_counter() - pc0) * 1000
    return _sehir_finish(f, cx, c, ctx, world, tod, frame, by0, bh, a, kick, caption, at)


def _sehir_finish(f, cx, c, ctx, world, tod, frame, by0, bh, a, kick, caption, at):
    """Bant süsleri + metin + günışığı/toz/vinyet (tüm sahneler için ortak son)."""
    if frame:
        for yy in (by0 - 40, by0 + bh):
            FA.vine_band(f, yy, a)
            c.drawLine(-40, yy + (40 if yy < by0 else 0), W + 40, yy + (40 if yy < by0 else 0), f.paint(TH.gold, style="stroke", sw=2.6, alpha=0.9 * a))
    if kick:
        CM.kick(f, kick, W / 2, 104, alpha=cx.amt(at + 0.4, 0.8), size=34, track=14)
    if caption:
        wd = sk.text_width(caption, "cap_i", 44) + 100
        cyy = by0 + bh - 70
        CM.tablet(f, W / 2 - wd / 2, cyy - 36, wd, 76, alpha=cx.amt(at + 0.8, 0.7), corner=10)
        CM.ink(f, caption, W / 2, cyy + 14, face="cap_i", size=44, color=TH.fg, align="c", alpha=cx.amt(at + 0.8, 0.7), emboss=False)
    # son: günışığı (yalnız gündüz) + toz + vinyet
    if tod == "day" and TH.mode == "day":
        CM.relight(f, cx)
    CM.motes(f, cx.t, n=22 if tod != "day" else 26, seed=2)
    CM.vig(f, 0.78 if tod == "night" else None)


def olaylar(scene="meydan", act=None, dur=10.0, **p):
    """Müzik/SFX ajanı için çekim-içi OLAY ZAMANLARI (yerel saniye; çapalar sayı olarak verilmişse): [(t, ad)]. Küresel zaman = Shot.origin + t.
    ates: ilk_kivilcim, esya_dustu×n, alev_tam · sokak: kapi_hamlesi (kapanma/açılma başlar), kapi_carpar (yalnız close) · palle: atlilar_gelir/atlilar_durur, kalabalik_coser · pencere: pencere_kararir×n."""
    act = act or DEFAULT_ACT.get(scene)
    ev = []

    def num(a, d_):
        return float(a) if isinstance(a, (int, float)) else d_
    if scene == "meydan" and act == "ates":
        ia = p.get("items_at")
        n = len(ia) if ia else 14
        times = [num(a, 0.0) for a in ia] if ia else [0.06 * dur + (0.50 * dur - 0.06 * dur) * i / max(1, n - 1) for i in range(n)]
        ev += [(t_, "esya_dustu") for t_ in times]
        f0 = num(p.get("fire_at"), 0.58 * dur)
        ev += [(f0, "ilk_kivilcim"), (f0 + float(p.get("fire_dur", max(2.5, 0.40 * dur))), "alev_tam")]
    elif scene == "sokak" and p.get("door"):
        dat = num(p.get("door_at"), 0.60 * dur)
        ev.append((dat, "kapi_hamlesi"))
        if p.get("door") == "close":
            ev.append((dat + 0.20, "kapi_carpar"))
    elif scene == "meydan" and act in ("palle", "kalabalik"):
        ev += [(0.06 * dur, "kalabalik_kabarir"), (0.46 * dur, "atlilar_durur"), (0.62 * dur, "kalabalik_coser")]
    elif scene == "meydan" and act == "pencere":
        ev += [(0.10 * dur + 0.74 * dur * i / 13.0, "pencere_kararir") for i in range(14)]
    return sorted(ev)
