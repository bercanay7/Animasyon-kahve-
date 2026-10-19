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
VER = "s1"                      # kareaş önbelleği sürümü (çizim kodu değişince artır)
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

    # ana ajanın tembel pişirme/ısıtma çağrısı için
    def default_stations(self):
        return []


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


def stone_wall(c, x0, y0, x1, y1, col, T, depth=0.0, seed=1, ch=30.0, bw=(64.0, 110.0), rustic=True, joint_a=105):
    """Taş blok duvar (bugnato/kesme): sıra yüksekliği ch, blok genişliği bw; üstte açık, altta koyu kenar; tek yol ile derz çizgileri."""
    rs = _RS(seed)
    base = T(col, depth)
    R(c, x0, y0, x1, y1, base)
    n = max(1, int(round((y1 - y0) / ch)))
    chh = (y1 - y0) / n
    jp = skia.Path()
    for r_ in range(n):
        yy = y0 + r_ * chh
        x = x0 - rs.uniform(0, bw[1] * 0.9)
        while x < x1:
            w_ = rs.uniform(*bw)
            xa, xb = max(x, x0), min(x + w_, x1)
            if xb - xa > 3:
                k = rs.uniform(-0.075, 0.075)
                R(c, xa, yy, xb, yy + chh, mix(base, "#FFF4DC" if k > 0 else "#2A1A0C", abs(k)))
                if rustic:
                    R(c, xa + 1, yy + 1, xb - 1, yy + 1 + min(3.4, chh * 0.12), "#FFFFFF", 44)
                    R(c, xa + 1, yy + chh - min(3.6, chh * 0.13), xb - 1, yy + chh - 1, "#2A1A0C", 52)
                jp.moveTo(xb, yy)
                jp.lineTo(xb, yy + chh)
            x += w_
        jp.moveTo(x0, yy)
        jp.lineTo(x1, yy)
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


def door_heavy(f, x, y, h, open_amount=0.0, w=None, alpha=1.0, glow_k=0.0, seed=1):
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
        rx = fx + sgn * (w * 0.06) * (1 if abs(ct) > 0.2 else 0)
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


def torch_bracket(c, x, y, T=None):
    """Duvar meşale/fener demiri (konsol + halka): x,y = tutucu orta nokta."""
    col = "#2A2622"
    c.drawLine(x - 16, y + 4, x, y, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.4, Color=C(col, 245), StrokeCap=skia.Paint.kRound_Cap))
    c.drawCircle(x, y - 3, 7, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6, Color=C(col, 245)))
    c.drawLine(x - 3, y - 2, x - 7, y + 26, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.4, Color=C("#5A3C22", 245), StrokeCap=skia.Paint.kRound_Cap))


# ═════════════════════════════ ateş / duman / kıvılcım (önceden renklendirilmiş sprite'lar) ═════════════════════════════
_FIRE = {}
NFL = 12


def _flame_frames():
    """12 karelik alev döngüsü: 256×420, taban alt-orta (128, 410). Kuyruklu dilimler; dıştan içe kızıl→turuncu→sarı→krem. Tam döngü (tam sayı frekans)."""
    if "fr" in _FIRE:
        return _FIRE["fr"]
    fr_list = []
    layers = [("#B3321A", 1.0, 1.0), ("#E5601E", 0.88, 0.93), ("#F59A2A", 0.70, 0.84), ("#FFD157", 0.50, 0.76), ("#FFF1B4", 0.30, 0.68)]
    for k in range(NFL):
        ph = 2 * math.pi * k / NFL
        fr = sk.Frame(256, 420)
        fr.clear(skia.ColorTRANSPARENT)
        c = fr.c
        bx, by = 128.0, 410.0
        for li, (col, sc, wsc) in enumerate(layers):
            rs = _RS(11)                                                                 # her katmanda aynı dilim düzeni
            nt = 5
            for i in range(nt):
                u = (i - (nt - 1) / 2.0) / ((nt - 1) / 2.0)                              # -1..1
                hh = (330 - 62 * abs(u)) * sc * (0.84 + 0.16 * math.sin(ph + i * 1.9 + rs.uniform(0, 1))) * (0.92 + 0.08 * math.sin(2 * ph + i * 2.7))
                bw = (62 - 14 * abs(u)) * wsc * sc ** 0.4
                xo = u * 62 * (0.9 - 0.3 * sc)
                sway = (20 + 10 * sc) * math.sin(ph + i * 2.3) * 0.5 + u * 18 * (1 - sc) + 9 * math.sin(2 * ph + i * 1.3)
                tipx = bx + xo + sway
                tipy = by - hh
                p = skia.Path()
                p.moveTo(bx + xo - bw, by)
                p.cubicTo(bx + xo - bw * 1.25, by - hh * 0.42, tipx - bw * 0.35 - sway * 0.2, by - hh * 0.72, tipx, tipy)
                p.cubicTo(tipx + bw * 0.30 + sway * 0.1, by - hh * 0.68, bx + xo + bw * 1.25, by - hh * 0.38, bx + xo + bw, by)
                p.close()
                c.drawPath(p, skia.Paint(AntiAlias=True, Color=C(col, 255)))
                if li == 0:
                    c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2, Color=C("#6A1A0C", 95)))
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


def smoke_plume(f, x, y, t, size=120.0, n=9, k=1.0, col="#5A544E", seed=3, rise=260.0, wind=40.0, a0=0.34):
    """Yükselen duman: büyüyüp solan yumuşak topaklar (önceden renklendirilmiş sprite, SrcOver). y = çıkış noktası."""
    c = _cv(f)
    im = _soft_dot(col, 56, 1.25)
    rs = _RS(seed)
    for i in range(n):
        per = 3.4 + 1.5 * rs.rand()
        ph = (t / per + i / n + rs.rand() * 0.05) % 1.0
        r = size * (0.22 + 0.9 * ph) * (0.7 + 0.5 * k)
        px = x + wind * ph * ph * 2.2 + math.sin(ph * 5.5 + i * 1.7) * size * 0.16 * ph + rs.uniform(-1, 1) * size * 0.1
        py = y - rise * (0.15 + ph) * (0.6 + 0.5 * k)
        a = a0 * k * math.sin(math.pi * min(1.0, ph * 1.15)) ** 1.4 * (1 - ph) ** 0.6
        _blit_dot(c, im, px, py, r, a)


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


def bonfire(f, x, y, size, t, seed=1, k=1.0, glow_a=1.0, tod="night"):
    """Alev + kıvılcım + duman (önceden renklendirilmiş sprite; ≈3–6 ms). x,y = ateş tabanı (alt orta), size = taban genişliği (px), k = 0..1 (kıvılcım→inferno).
    k<0.15 tek küçük alev; k büyüdükçe dilim sayısı/boyu artar. Dönüş: alevin tepe y'si."""
    c = _cv(f)
    k = clamp(k)
    if k <= 0.003:
        return y
    fr = _flame_frames()
    rs = _RS(seed)
    nfl = 1 + int(round(5 * smooth(clamp(k * 1.25))))
    tops = []
    gl = glow_a * (0.35 + 0.65 * k)
    # zemin parıltısı
    glow(c, x, y - size * 0.18 * k, size * (0.9 + 1.1 * k), "#FF8A2A", 0.26 * gl)
    glow(c, x, y - size * 0.30 * k, size * (0.55 + 0.65 * k), "#FFC25A", 0.34 * gl)
    order = sorted(range(nfl), key=lambda i: abs(i - (nfl - 1) / 2.0), reverse=True)
    pd = _DP
    for i in order:
        u = (i - (nfl - 1) / 2.0) / max(1.0, (nfl - 1) / 2.0)
        sc = size / 190.0 * (0.50 + 0.65 * (1 - 0.35 * abs(u))) * (0.30 + 0.70 * smooth(clamp(k * 1.15)))
        fi = int(t * 13.0 + i * 5 + seed * 3) % NFL
        wob = 1.0 + 0.045 * math.sin(t * 7.3 + i * 2.2 + seed)
        xx = x + u * size * 0.34 * min(1.0, 0.4 + k)
        hh = 410 * sc * wob
        ww = 256 * sc * (1.0 + 0.04 * math.sin(t * 5.1 + i))
        pd.setAlphaf(1.0)
        c.drawImageRect(fr[fi], skia.Rect.MakeWH(256, 420), skia.Rect.MakeXYWH(xx - ww / 2, y - hh * (410.0 / 420.0), ww, hh), LIN, pd)
        tops.append(y - hh * 0.84)
    top = min(tops)
    # kıvılcım + duman
    ember_field(f, x, y - size * 0.25, t, n=int(10 + 34 * k), spread=size * 0.30, h=size * (1.0 + 1.8 * k), wind=50 + 40 * k, k=1.0, seed=seed + 4, size=1.0)
    smoke_plume(f, x, top + size * 0.12, t, size=size * 0.34, n=int(4 + 6 * k), k=k, col={"day": "#6A645C", "dusk": "#4E4850", "night": "#2C3042"}.get(tod, "#4E4850"), seed=seed + 9, rise=size * 1.5, wind=30 + 30 * k, a0=0.30)
    return top


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
