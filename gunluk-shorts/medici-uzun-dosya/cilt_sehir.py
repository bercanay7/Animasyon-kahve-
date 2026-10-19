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
    glow(c, x, y - size * 0.20 * (0.4 + k), size * (0.8 + 1.3 * k), "#FF7A22", 0.22 * gl)
    glow(c, x, y - size * 0.34 * (0.4 + k), size * (0.5 + 0.7 * k), "#FFB347", 0.32 * gl)
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
    act = a.get("action", "walk" if sp > 1 else "idle")
    fl = a.get("flag")
    if act in ("walk", "idle"):
        FA.walker(f, a.get("kind", "halk"), x, y, h, t, speed=sp if act == "walk" else 0.0, dir=d, phase=a.get("phase", 0.0), seed=a.get("seed", 0), alpha=a.get("alpha", 1.0), cf=cf, prop=a.get("prop"), flag=fl)
    else:
        kw = {k: v for k, v in a.items() if k in ("t0", "dur", "depth", "target", "rise_at", "energy", "amount", "hop", "mode", "period", "high")}
        kw.pop("t0", None)
        FA.actor(f, a.get("kind", "halk"), x, y, h, tt, action=act, dir=d, seed=a.get("seed", 0), phase=a.get("phase", 0.0), alpha=a.get("alpha", 1.0), cf=cf, prop=a.get("prop"), **kw)


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
    def default_cams(self, act=None):
        if act == "ates":                                    # yığının etrafında yarım daire (paralaks) → yığın merkezinde SABİT (sonraki odun çekimi aynı noktadan başlar)
            return [(0.0, (PILE_X - 560, 30, 1.0)), (0.80, (PILE_X - 40, 30, 1.13)), (1.0, (PILE_X, 30, 1.15))]
        if act == "odun":
            return [(0.0, (PILE_X, 30, 1.15)), (1.0, (PILE_X + 20, 30, 1.19))]
        if act == "palle":
            return [(0.0, (2350, 40, 1.0)), (0.50, (1950, 30, 1.0)), (0.78, (950, 110, 1.12)), (1.0, (430, 110, 1.55))]
        if act == "pencere":                                 # ağır pull: cepheye yakın → geri
            return [(0.0, (PV_X0 + PV_W * 0.55, 150, 1.34)), (1.0, (PV_X0 + PV_W * 0.52, 80, 1.0))]
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

    def _items_state(self, ctx):
        p = ctx.p
        act = p["act"]
        return act

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
            hy = 836 + (i % 3) * 12 + sway * 0.3
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
        cf = lit_cf(ctx.tod)
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
        dk = dark_cf("#16121A")
        if back:
            # uzak siluet kalabalık (halka; yüz/ayrıntı yok)
            for m in self.ring:
                if m["row"] == 2:
                    continue
                if m["x"] < xa - 200 or m["x"] > xb + 200:
                    continue
                FA.walker(f, m["kind"], m["x"], m["y"], m["h"], t, speed=0.0, dir=m["face"], phase=m["phase"], seed=m["seed"], cf=dk)
            img, ox, oy, slots = self.pile_odun
            c.drawImage(img, PILE_X - ox, PILE_Y - oy, LIN)
            gallows_silhouette(c, PILE_X + 6, PILE_Y - 120, 430, "#0F0D0C", 252)
        else:
            for m in self.ring:
                if m["row"] != 2:
                    continue
                if m["x"] < xa - 200 or m["x"] > xb + 200:
                    continue
                FA.walker(f, m["kind"], m["x"], m["y"], m["h"], t, speed=0.0, dir=m["face"], phase=m["phase"], seed=m["seed"], cf=dk)

    # ── act: palle ──
    def _act_palle(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        T0 = ctx.p.get("t_meet", None)
        dur = max(ctx.cx.dur, 1e-3)
        # Medici kalkanı (yalnız bu act'te)
        medici_shield(c, MED_X0 + MED_W * 0.30, YG - 0.52 * MED_H, MED_H * 0.12, self.T)
        # Medici kalabalığı: Medici palazzosunun kapısından çıkıp SAĞA kabarır, sonra coşar
        for m in self._palle_crowd:
            tt = t - m["d"]
            u = clamp(tt / m["T"])
            x = m["x0"] + (m["x1"] - m["x0"]) * ease_out(u)
            v = (m["x1"] - m["x0"]) * (3 * (1 - u) ** 2) / m["T"] if 0 < u < 1 else 0.0
            if tt < 0 or x < xa - 200 or x > xb + 200:
                continue
            fl = ("medici", 0.62, 0.44, "#E0B84E", "#B33620") if m["flag"] else None
            if v > 18:
                FA.walker(f, m["kind"], x, m["y"], m["h"], t, speed=v, dir=1, phase=m["phase"], seed=m["seed"], prop=("pole" if m["flag"] else None), flag=fl)
            elif m["flag"]:
                FA.walker(f, m["kind"], x, m["y"], m["h"], t, speed=0.0, dir=1, phase=m["phase"], seed=m["seed"], prop="pole", flag=fl)
            else:
                amt = clamp((tt - m["T"]) / 1.2) * m["amt"]
                if amt > 0.05:
                    FA.actor(f, m["kind"], x, m["y"], m["h"], t, action="cheer", dir=1, seed=m["seed"], phase=m["phase"], amount=amt, hop=m["hop"])
                else:
                    FA.walker(f, m["kind"], x, m["y"], m["h"], t, speed=0.0, dir=1, phase=m["phase"], seed=m["seed"])
        # atlılar: sağdan sola gelir, yavaşlayıp DURUR (şiddet yok)
        for r_ in self._palle_riders:
            tt = t - r_["d"]
            if tt < -0.2:
                continue
            u = clamp(tt / r_["T"])
            x = r_["x0"] + (r_["x1"] - r_["x0"]) * ease_out(u)
            v = abs(r_["x1"] - r_["x0"]) * 3 * (1 - u) ** 2 / r_["T"] if u < 1 else 0.0
            if x < xa - 320 or x > xb + 320:
                continue
            g_ = "trot" if v > 130 else "walk"
            FA.rider(f, x, r_["y"], r_["h"], t, speed=v, gait=g_, dir=-1, seed=r_["seed"], phase=r_["phase"])
            if v > 60:
                for k in range(4):
                    ph = (t * 1.4 + k / 4.0) % 1.0
                    FA._puff(c, x + 130 + ph * 80, r_["y"] - 6 - ph * 30, 14 + 22 * ph, 0.30 * (1 - ph), "#CDB98E")

    def _prepare_palle(self, cx):
        dur = max(cx.dur, 1e-3)
        rs = _RS(14)
        self._palle_crowd = []
        n = 22
        for i in range(n):
            x1 = rs.uniform(1550, 2480)
            self._palle_crowd.append(dict(x0=MED_X0 + MED_W * 0.14 + rs.uniform(-60, 80), x1=x1, y=YG + rs.uniform(-12, 36), h=rs.uniform(158, 192), kind=["halk", "tuccar", "soylu", "soylu_f", "cocuk", "halk", "banker", "halk"][rs.randint(8)],
                                          seed=int(rs.randint(0, 40)), phase=rs.rand(), d=0.15 * dur * rs.rand() + 0.04 * dur * (i % 6), T=rs.uniform(0.34, 0.50) * dur, flag=(i % 4 == 1), amt=rs.uniform(0.6, 1.0), hop=rs.uniform(0.2, 0.7)))
        self._palle_crowd.sort(key=lambda m: m["y"])
        self._palle_riders = []
        for i in range(6):
            self._palle_riders.append(dict(x0=3900 + 170 * i, x1=2760 + 150 * i + rs.uniform(-40, 40), y=YG + 18 + (i % 3) * 14, h=262 + (i % 2) * 8, seed=3 + i, phase=rs.rand(), d=0.03 * dur * i, T=0.42 * dur))
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
                    fi = 0.86 + 0.14 * math.sin(t * 9.0 + tx * 0.01) + 0.06 * math.sin(t * 23 + tx)
                    glow(c, tx - 7, YG - 192, 74 * fi, "#FFB04A", 0.40)
                    bonfire(c, tx - 7, YG - 176, 34, t, seed=int(tx) % 50, k=0.55, glow_a=0.2, tod=ctx.tod)
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
        lit_bifora(c, w0[:4], a * flick, col="#FFC23D", core="#FFE79A")
        glow(c, w0[0], w0[1] - w0[3] * 0.5, w0[3] * 2.4, "#FFC23D", 0.34 * a * flick)
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
        elif act == "palle":
            if getattr(self, "_pd", None) != dur:
                self._prepare_palle(cx)
                self._pd = dur
            ctx.win_gold_t0 = _anchor(cx, p.get("gold_at"), 0.55 * dur)

    def grade(self, ctx):
        _grade_generic(self, ctx)


def _grade_generic(world, ctx):
    """Alacakaranlık/gece derecelendirmesi (ekran uzayı; bant içine): ışık kaynağı varsa ışık havuzu, yoksa düz örtü. day → CM.finish günışığı yapar."""
    f, c = ctx.f, ctx.c
    tod = ctx.tod
    if tod == "day":
        return
    by0, bh = ctx.band
    rect = (0, by0, W, by0 + bh)
    p = ctx.p
    act = p.get("act")
    dusk = (tod == "dusk")
    hue = (78, 46, 96) if dusk else (8, 12, 44)
    gain = 0.50 if dusk else 0.88
    if act == "pencere":                                                      # alacakaranlık → gece
        dur = max(ctx.cx.dur, 1e-3)
        nk = ease_io(ctx.t / dur)
        PN.tint_overlay(c, by0, bh, [("#5A3E78", 70), ("#E8905A", 26), ("#E8905A", 40)], [0.0, 0.55, 1.0])
        R(c, 0, by0, W, by0 + bh, "#0A1034", int(140 * nk))
        return
    L = world.lights(ctx) if hasattr(world, "lights") else []
    if L:
        wx, wy, r, kk = L[0]
        sx, sy = ctx.to_screen(1.0, wx, wy)
        R_ = r * ctx.z
        light_pool(f, sx, sy, R_, gain=gain, hue=hue, warm_a=0.0, edge=0.94 if not dusk else 0.80, rect=rect)
        glow(c, sx, sy, R_ * 1.1, "#FF8A2A", 0.16 * kk)
    else:
        if dusk:
            PN.tint_overlay(c, by0, bh, [("#5A3E78", 78), ("#E8905A", 28), ("#E8905A", 46)], [0.0, 0.55, 1.0])
        else:
            R(c, 0, by0, W, by0 + bh, "#0A1034", 150)
            light_pool(f, W / 2, by0 + bh * 0.5, 1100, gain=0.5, hue=hue, warm_a=0.04, edge=0.55, rect=rect)


# ═════════════════════════════ sahne kayıtları + `sehir` çekim türü ═════════════════════════════
_SW = {}
ACT_TOD = {("meydan", "ates"): "dusk", ("meydan", "odun"): "night", ("meydan", "palle"): "day", ("meydan", "pencere"): "dusk"}
DEFAULT_ACT = {"meydan": "ates", "sokak": None, "kale": "sur", "skyline_dikey": None}
CLASSES = {}   # (scene, act|None) → sınıf; alt bölümlerde doldurulur


def get_sworld(scene, act, tod):
    cls = CLASSES.get((scene, act)) or CLASSES.get((scene, None))
    if cls is None:
        raise ValueError(f"sehir: bilinmeyen sahne/act: {scene!r}/{act!r} (meydan: ates|odun|palle|pencere · sokak · kale: sur|castel|passetto · skyline_dikey)")
    key = (cls.name, tod)
    w = _SW.get(key)
    if w is None:
        w = _SW[key] = cls(tod)
    return w


CLASSES[("meydan", None)] = Meydan


@ckind("sehir")
def k_sehir(cx, scene="meydan", act=None, tod=None, cams=None, actors=None, stations=None, kick=None, caption=None, at=0.0, frame=True, seed=1, band=None,
            door=None, door_at=None, items_at=None, fire_at=None, **kw):
    """Dış mekân/şehir dünyası. scene: meydan | sokak | kale | skyline_dikey; act: (meydan) ates|odun|palle|pencere · (kale) sur|castel|passetto.
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
    pc = PN.PanoCam(cx, cams, world.default_cams(act), dur)
    t_cam = clamp(cx.t, 0.0, dur)
    camx, camy, z = pc.at(t_cam)
    if not cams:
        dx, dy, zm = _cam_mod(getattr(cx, "cam_spec", None), ease_io(t_cam / dur))
        camx, camy, z = camx + dx, camy + dy, z * zm
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
    ctx.p = dict(scene=scene, act=act, actors=actors, items_at=items_at, fire_at=fire_at, door=door, door_at=door_at, **{k: v for k, v in kw.items() if k not in ("cam",)})
    sts = stations if stations is not None else world.default_stations()
    ctx.stations = []
    for s_ in sts:
        s2 = dict(s_)
        s2["_at"] = float(s2["at_frac"]) * dur if ("at_frac" in s2 and "at" not in s2) else _anchor(cx, s2.get("at", 0.0))
        ctx.stations.append(s2)
    world.prepare(ctx)
    by0, bh = ctx.band
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, by0, W, by0 + bh))
    for item in world.stack(ctx):
        kind = item[0]
        if kind == "L":
            L = world.layers[item[1]]
            dy_ = item[2] if len(item) > 2 else 0.0
            ctx.xf(L.f, dy_)
            xa, xb = ctx.view(L.f)
            L.draw_view(c, xa, xb)
            ctx.end()
        elif kind == "D":
            fct = item[2]
            dy_ = item[3] if len(item) > 3 else 0.0
            ctx.xf(fct, dy_)
            xa, xb = ctx.view(fct)
            ctx.xa, ctx.xb = xa, xb
            getattr(world, item[1])(ctx)
            ctx.end()
    world.grade(ctx)
    if hasattr(world, "fx"):
        xa, xb = ctx.view(1.0)
        ctx.xa, ctx.xb = xa, xb
        world.fx(ctx)
    c.restore()
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
