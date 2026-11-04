"""cilt_city — Floransa silueti (fresk/diorama): Duomo kubbesi (sekiz beyaz damarlı kiremit kubbe + fener), Giotto çan kulesi (renkli mermer), Palazzo Vecchio kulesi
(Arnolfo: çıkma + mazgal + çan kafesi), Vaftizhane, San Lorenzo kubbesi, Santa Croce çan kulesi, ortaçağ kuleleri, çatı sıraları, Arno + Ponte Vecchio.

Katmanlar (kaydırma hızlarıyla paralaks): sky, hills, far (uzak şehir + anıtlar), near (nehir kıyısı evleri + köprü + nehir). Hepsi önbellekli görüntü; bayrak/kuş/pencere ışığı çekimde.
Zaman: 'day' | 'dusk' | 'night' (gece: lacivert gök, ay, yıldız, sarı pencere ışıkları). Kıyı: çatlak + boya kaybı (fresk) `cilt_scene._bake_texture`.
"""
import functools
import math

import numpy as np
import skia

import cilt_medici as CM
import cilt_scene as SC
import donem as DN
import cilt_wall as CW
import sk
from sk import C, Frame, clamp, mix

PW_EXTRA = 520          # panorama kaydırma payı (px)
PH = 700                # panorama yüksekliği (px)


class Tint:
    """Zaman/derinlik renk uyarlaması: day (olduğu gibi), dusk (sıcak), night (lacivert)."""

    def __init__(self, mode="day"):
        self.mode = mode

    def __call__(self, col, depth=0.0):
        """depth 0 = ön, 1 = uzak: atmosferik perspektif (soluk mavi-yeşile karışır)."""
        if self.mode == "night":
            c = mix(col, "#10204A", 0.58)
            return mix(c, "#2A3C74", depth * 0.30)
        if self.mode == "dusk":
            c = mix(col, "#E58A55", 0.20)
            return mix(c, "#B89AA0", depth * 0.36)
        return mix(col, "#B6C8C8", depth * 0.40)


def _R(c, x0, y0, x1, y1, col, alpha=255):
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.Paint(Color=C(col, alpha)))


def _ink(c, path, w=1.3, a=170, col="#2A1A0C"):
    c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, a), StrokeJoin=skia.Paint.kRound_Join))


def _lit_windows(c, rs, boxes, night, p=0.35):
    """Pencere ışıkları (gece/alacakaranlık): boxes=[(x,y,w,h)]. Dönüş: yanan pencerelerin kutuları."""
    lit = []
    for (x, y, w, h) in boxes:
        if rs.rand() < p:
            c.drawRect(skia.Rect.MakeXYWH(x - 2, y - 2, w + 4, h + 4), skia.Paint(AntiAlias=True, Color=C("#FFB04A", 60), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 3)))
            c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), skia.Paint(AntiAlias=True, Color=C("#FFD27A")))
            lit.append((x, y, w, h))
    return lit


# ───────────────────────────── anıtlar ─────────────────────────────
WOOD = "#6B4A2A"


def _scaffold(c, x0, x1, ytop, h, T, depth, n=None, a=210):
    """Ahşap iskele: dikmeler + yatay tablalar + çapraz bağ (inşaat sürüyor)."""
    col = C(T(WOOD, depth), a)
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=col, StrokeCap=skia.Paint.kRound_Cap)
    n = n or max(2, int((x1 - x0) / 16))
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
    for xx in xs:
        c.drawLine(xx, ytop + h, xx, ytop, p)
    for k in range(1, 4):
        yy = ytop + h * (1 - k / 3.4)
        c.drawLine(x0 - 2, yy, x1 + 2, yy, p)
    for i in range(len(xs) - 1):
        c.drawLine(xs[i], ytop + h * 0.70, xs[i + 1], ytop + h * 0.30, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C(T(WOOD, depth), int(a * 0.7))))


def _crane(c, x, ytop, h, T, depth, flip=1):
    """Basit yapı vinci (direk + kol + halat): kubbe/fener şantiyesi."""
    col = C(T("#5A3E22", depth), 220)
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.8, Color=col, StrokeCap=skia.Paint.kRound_Cap)
    c.drawLine(x, ytop, x, ytop - h, p)
    c.drawLine(x - flip * h * 0.10, ytop - h * 0.92, x + flip * h * 0.62, ytop - h * 0.78, p)
    c.drawLine(x + flip * h * 0.55, ytop - h * 0.80, x + flip * h * 0.55, ytop - h * 0.40, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=col))
    c.drawRect(skia.Rect.MakeXYWH(x + flip * h * 0.55 - 2.5, ytop - h * 0.40, 5, 4), skia.Paint(AntiAlias=True, Color=C(T("#A88A62", depth))))


def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def _dome_halfw(x, yb, w, hd, ycut):
    """Kubbe dış hattının (sağ yarı kübik) ycut yüksekliğindeki yarı genişliği."""
    P = [(x + w * 0.47, yb), (x + w * 0.47, yb - hd * 0.66), (x + w * 0.20, yb - hd * 0.97), (x, yb - hd)]
    lo, hi = 0.0, 1.0
    for _ in range(30):
        m = (lo + hi) / 2
        if _bez(*P, m)[1] > ycut:
            lo = m
        else:
            hi = m
    return _bez(*P, (lo + hi) / 2)[0] - x


def _crossing_stub(c, x, y, w, drum_h, T, depth, k):
    """1380–1410: kubbe yok, tambur yok — sekizgen geçişin tribün duvarları yükseliyor (iskeleli şantiye)."""
    marble = T("#EFE5CC", depth)
    h = drum_h * (0.35 + 0.9 * k)
    _R(c, x - w * 0.47, y - h * 0.15, x + w * 0.47, y + drum_h * 0.10, marble)
    for dx in (-0.47, -0.25, 0.25, 0.47):
        _R(c, x + dx * w - w * 0.035, y - h, x + dx * w + w * 0.035, y, marble)
    c.drawRect(skia.Rect.MakeLTRB(x - w * 0.47, y - h * 0.15, x + w * 0.47, y + drum_h * 0.10), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.1, Color=C("#2A1A0C", 140)))
    _scaffold(c, x - w * 0.50, x + w * 0.50, y - h - 10, h + 10, T, depth, n=7)


def draw_dome(c, x, y, w, hd, drum_h, lant_h, T, depth=0.0, outline=True, stage=None):
    """Brunelleschi kubbesi: (x, y=tambur tabanı). w taban genişliği.
    stage: None → eski (tam kubbe + fener + top/haç) | donem.DuomoStage → o yılın durumu (tribün/tambur/kubbe/fener/top-haç; şantiyede iskele + vinç)."""
    if stage is not None:
        return _draw_dome_stage(c, x, y, w, hd, drum_h, lant_h, T, depth, outline, stage)
    tile = T("#C65B33", depth)
    tile2 = T("#9C3F25", depth)
    marble = T("#EFE5CC", depth)
    green = T("#6E9878", depth)
    # tambur
    _R(c, x - w * 0.47, y - drum_h, x + w * 0.47, y, marble)
    for k in range(4):
        _R(c, x - w * 0.47, y - drum_h + drum_h * (0.22 + 0.22 * k), x + w * 0.47, y - drum_h + drum_h * (0.22 + 0.22 * k) + 2.4, green, 200)
    for dx in (-0.24, 0.0, 0.24):
        c.drawOval(skia.Rect.MakeXYWH(x + dx * w - w * 0.045, y - drum_h * 0.62, w * 0.09, drum_h * 0.34), skia.Paint(AntiAlias=True, Color=C(T("#3A2A1C", depth), 210)))
    if outline:
        c.drawRect(skia.Rect.MakeLTRB(x - w * 0.47, y - drum_h, x + w * 0.47, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#2A1A0C", 150)))
    yb = y - drum_h
    dome = skia.Path()
    dome.moveTo(x - w * 0.47, yb)
    dome.cubicTo(x - w * 0.47, yb - hd * 0.66, x - w * 0.20, yb - hd * 0.97, x, yb - hd)
    dome.cubicTo(x + w * 0.20, yb - hd * 0.97, x + w * 0.47, yb - hd * 0.66, x + w * 0.47, yb)
    dome.close()
    sh = skia.GradientShader.MakeLinear([(x - w * 0.5, 0), (x + w * 0.5, 0)], [C(mix(tile, "#FFFFFF", 0.14)), C(tile), C(tile2)], [0, 0.55, 1])
    c.drawPath(dome, skia.Paint(AntiAlias=True, Shader=sh))
    c.save()
    c.clipPath(dome, skia.ClipOp.kIntersect, True)
    # kiremit sıraları (kavisli)
    for k in range(1, 9):
        ty = yb - hd * k / 9.0
        c.drawLine(x - w * 0.5, ty, x + w * 0.5, ty + 5 * (1 if k % 2 else -1), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.1, Color=C("#5A2412", 70)))
    # beyaz damarlar
    for th in (-0.80, -0.50, -0.20, 0.20, 0.50, 0.80):
        pth = skia.Path()
        pth.moveTo(x + math.sin(th) * w * 0.46, yb)
        pth.quadTo(x + math.sin(th) * w * 0.40, yb - hd * 0.66, x + math.sin(th) * w * 0.03, yb - hd * 0.98)
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w * 0.026, Color=C(T("#F2EAD4", depth)), StrokeCap=skia.Paint.kRound_Cap))
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#6A5A40", 120)))
    c.restore()
    if outline:
        _ink(c, dome, 1.5, 190)
    # fener
    ly = yb - hd
    lw = w * 0.17
    _R(c, x - lw * 1.15, ly - 8, x + lw * 1.15, ly + 2, marble)
    _R(c, x - lw, ly - lant_h * 0.62, x + lw, ly - 8, marble)
    for dx in (-0.55, 0.0, 0.55):
        c.drawPath(sk.smooth_path([(x + dx * lw - lw * 0.22, ly - 12), (x + dx * lw - lw * 0.22, ly - lant_h * 0.46), (x + dx * lw, ly - lant_h * 0.52), (x + dx * lw + lw * 0.22, ly - lant_h * 0.46), (x + dx * lw + lw * 0.22, ly - 12)], True, 0.3),
                   skia.Paint(AntiAlias=True, Color=C(T("#4A3A28", depth), 200)))
    _R(c, x - lw * 1.1, ly - lant_h * 0.64, x + lw * 1.1, ly - lant_h * 0.60, marble)
    cone = sk.poly_path([(x - lw * 0.95, ly - lant_h * 0.64), (x, ly - lant_h * 0.96), (x + lw * 0.95, ly - lant_h * 0.64)])
    c.drawPath(cone, skia.Paint(AntiAlias=True, Color=C(T("#E3D8BA", depth))))
    c.drawCircle(x, ly - lant_h * 0.99, w * 0.022, skia.Paint(AntiAlias=True, Color=C(T("#D8A63A", depth))))
    c.drawLine(x, ly - lant_h * 1.0, x, ly - lant_h * 1.16, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.4, Color=C(T("#D8A63A", depth))))
    c.drawLine(x - 6, ly - lant_h * 1.10, x + 6, ly - lant_h * 1.10, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2, Color=C(T("#D8A63A", depth))))
    if outline:
        _ink(c, cone, 1.2, 170)
        c.drawRect(skia.Rect.MakeLTRB(x - lw, ly - lant_h * 0.62, x + lw, ly - 8), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.1, Color=C("#2A1A0C", 150)))


def _draw_dome_stage(c, x, y, w, hd, drum_h, lant_h, T, depth, outline, st):
    tile = T("#C65B33", depth)
    tile2 = T("#9C3F25", depth)
    marble = T("#EFE5CC", depth)
    green = T("#6E9878", depth)
    if st.drum <= 0.0:
        if st.tribune > 0.0:
            _crossing_stub(c, x, y, w, drum_h, T, depth, st.tribune)
        return
    dh = drum_h * st.drum
    _R(c, x - w * 0.47, y - dh, x + w * 0.47, y, marble)
    for k in range(4):
        yy = y - drum_h + drum_h * (0.22 + 0.22 * k)
        if yy > y - dh:
            _R(c, x - w * 0.47, yy, x + w * 0.47, yy + 2.4, green, 200)
    if st.drum >= 1.0:
        for dx in (-0.24, 0.0, 0.24):
            c.drawOval(skia.Rect.MakeXYWH(x + dx * w - w * 0.045, y - drum_h * 0.62, w * 0.09, drum_h * 0.34), skia.Paint(AntiAlias=True, Color=C(T("#3A2A1C", depth), 210)))
    if outline:
        c.drawRect(skia.Rect.MakeLTRB(x - w * 0.47, y - dh, x + w * 0.47, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#2A1A0C", 150)))
    yb = y - drum_h
    if st.drum < 1.0:
        _scaffold(c, x - w * 0.50, x + w * 0.50, y - dh - 12, 14, T, depth, n=8)
        return
    if st.dome <= 0.0:                                       # 1415–1420: tambur açık (kubbe yok) — üstte iskele/vinç
        c.drawOval(skia.Rect.MakeLTRB(x - w * 0.47, yb - w * 0.035, x + w * 0.47, yb + w * 0.035), skia.Paint(AntiAlias=True, Color=C(T("#3A2A1C", depth), 200)))
        _scaffold(c, x - w * 0.48, x + w * 0.48, yb - 12, 12, T, depth, n=9, a=170)
        return
    dome = skia.Path()
    dome.moveTo(x - w * 0.47, yb)
    dome.cubicTo(x - w * 0.47, yb - hd * 0.66, x - w * 0.20, yb - hd * 0.97, x, yb - hd)
    dome.cubicTo(x + w * 0.20, yb - hd * 0.97, x + w * 0.47, yb - hd * 0.66, x + w * 0.47, yb)
    dome.close()
    built = min(1.0, st.dome)
    ycut = yb - hd * (built if built < 1.0 else 1.02)
    c.save()
    if built < 1.0:
        c.clipRect(skia.Rect.MakeLTRB(x - w, ycut, x + w, yb + 2))
    sh = skia.GradientShader.MakeLinear([(x - w * 0.5, 0), (x + w * 0.5, 0)], [C(mix(tile, "#FFFFFF", 0.14)), C(tile), C(tile2)], [0, 0.55, 1])
    c.drawPath(dome, skia.Paint(AntiAlias=True, Shader=sh))
    c.save()
    c.clipPath(dome, skia.ClipOp.kIntersect, True)
    for k in range(1, 9):
        ty = yb - hd * k / 9.0
        c.drawLine(x - w * 0.5, ty, x + w * 0.5, ty + 5 * (1 if k % 2 else -1), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.1, Color=C("#5A2412", 70)))
    for th in (-0.80, -0.50, -0.20, 0.20, 0.50, 0.80):
        pth = skia.Path()
        pth.moveTo(x + math.sin(th) * w * 0.46, yb)
        pth.quadTo(x + math.sin(th) * w * 0.40, yb - hd * 0.66, x + math.sin(th) * w * 0.03, yb - hd * 0.98)
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w * 0.026, Color=C(T("#F2EAD4", depth)), StrokeCap=skia.Paint.kRound_Cap))
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#6A5A40", 120)))
    c.restore()
    if outline:
        _ink(c, dome, 1.5, 190)
    c.restore()
    if built < 1.0:                                          # yarım kabuk: açık sekizgen ağız + iskele halkası + vinç
        hw = _dome_halfw(x, yb, w, hd, ycut)
        c.drawOval(skia.Rect.MakeLTRB(x - hw, ycut - max(2.0, hw * 0.10), x + hw, ycut + max(2.0, hw * 0.10)), skia.Paint(AntiAlias=True, Color=C(T("#2A1E14", depth), 230)))
        c.drawOval(skia.Rect.MakeLTRB(x - hw, ycut - max(2.0, hw * 0.10), x + hw, ycut + max(2.0, hw * 0.10)), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(marble, 230)))
        _scaffold(c, x - hw * 0.95, x + hw * 0.95, ycut - 13, 12, T, depth, n=max(3, int(hw / 9)), a=190)
        _crane(c, x + hw * 0.15, ycut - 4, max(16.0, hd * 0.30), T, depth, flip=-1)
        return
    ly = yb - hd
    lw = w * 0.17
    _R(c, x - lw * 1.15, ly - 8, x + lw * 1.15, ly + 2, marble)        # serraglio (fenerin oturduğu halka)
    if st.lantern <= 0.0:
        c.drawRect(skia.Rect.MakeLTRB(x - lw * 1.15, ly - 8, x + lw * 1.15, ly + 2), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#2A1A0C", 140)))
        return
    if st.lantern < 1.0:                                     # 1446–1461: fener yükseliyor (iskeleli gövde)
        top = ly - 8 - lant_h * 0.62 * st.lantern
        _R(c, x - lw, top, x + lw, ly - 8, marble)
        for dx in (-0.55, 0.0, 0.55):
            wy0 = max(top + 2, ly - lant_h * 0.46)
            if wy0 < ly - 14:
                c.drawRect(skia.Rect.MakeLTRB(x + dx * lw - lw * 0.22, wy0, x + dx * lw + lw * 0.22, ly - 12), skia.Paint(AntiAlias=True, Color=C(T("#4A3A28", depth), 200)))
        c.drawRect(skia.Rect.MakeLTRB(x - lw, top, x + lw, ly - 8), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.1, Color=C("#2A1A0C", 150)))
        _scaffold(c, x - lw * 1.35, x + lw * 1.35, top - 10, (ly - 8) - top + 10, T, depth, n=4, a=200)
        _crane(c, x, top - 6, max(14.0, lant_h * 0.45), T, depth)
        return
    _R(c, x - lw, ly - lant_h * 0.62, x + lw, ly - 8, marble)
    for dx in (-0.55, 0.0, 0.55):
        c.drawPath(sk.smooth_path([(x + dx * lw - lw * 0.22, ly - 12), (x + dx * lw - lw * 0.22, ly - lant_h * 0.46), (x + dx * lw, ly - lant_h * 0.52), (x + dx * lw + lw * 0.22, ly - lant_h * 0.46), (x + dx * lw + lw * 0.22, ly - 12)], True, 0.3),
                   skia.Paint(AntiAlias=True, Color=C(T("#4A3A28", depth), 200)))
    _R(c, x - lw * 1.1, ly - lant_h * 0.64, x + lw * 1.1, ly - lant_h * 0.60, marble)
    cone = sk.poly_path([(x - lw * 0.95, ly - lant_h * 0.64), (x, ly - lant_h * 0.96), (x + lw * 0.95, ly - lant_h * 0.64)])
    c.drawPath(cone, skia.Paint(AntiAlias=True, Color=C(T("#E3D8BA", depth))))
    if st.ball:                                               # ≥1471: Verrocchio'nun yaldızlı bakır topu + haç
        c.drawCircle(x, ly - lant_h * 0.99, w * 0.022, skia.Paint(AntiAlias=True, Color=C(T("#D8A63A", depth))))
        c.drawLine(x, ly - lant_h * 1.0, x, ly - lant_h * 1.16, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.4, Color=C(T("#D8A63A", depth))))
        c.drawLine(x - 6, ly - lant_h * 1.10, x + 6, ly - lant_h * 1.10, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2, Color=C(T("#D8A63A", depth))))
    if outline:
        _ink(c, cone, 1.2, 170)
        c.drawRect(skia.Rect.MakeLTRB(x - lw, ly - lant_h * 0.62, x + lw, ly - 8), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.1, Color=C("#2A1A0C", 150)))


def dome_top(x, y, w, hd, drum_h, lant_h, stage=None):
    """Kubbe grubunun o yılki en üst noktası (etiket çapası için): (x, y_üst)."""
    if stage is None or stage.full:
        return x, y - drum_h - hd - lant_h * 1.16
    if stage.drum <= 0:
        return x, y - (drum_h * (0.35 + 0.9 * stage.tribune) if stage.tribune > 0 else 0.0)
    if stage.dome <= 0:
        return x, y - drum_h * stage.drum
    if stage.dome < 1:
        return x, y - drum_h - hd * stage.dome
    if stage.lantern <= 0:
        return x, y - drum_h - hd - 8
    if stage.lantern < 1:
        return x, y - drum_h - hd - 8 - lant_h * 0.62 * stage.lantern
    return x, y - drum_h - hd - lant_h * 0.96


def draw_nave(c, x0, x1, y, h, T, depth=0.0):
    """Katedral nefi (kubbenin batısında = görüntüde sağda; uzun alçak kiremit çatı + yan koridor)."""
    wall = T("#EFE5CC", depth)
    roof = T("#C0522E", depth)
    _R(c, x0, y - h * 0.55, x1, y, wall)
    for k in range(int((x1 - x0) / 22)):
        xx = x0 + 10 + k * 22
        c.drawPath(sk.smooth_path([(xx, y - h * 0.12), (xx, y - h * 0.34), (xx + 5, y - h * 0.40), (xx + 10, y - h * 0.34), (xx + 10, y - h * 0.12)], True, 0.3), skia.Paint(AntiAlias=True, Color=C(T("#4A3A28", depth), 170)))
    for kk in range(3):
        _R(c, x0, y - h * (0.50 - 0.16 * kk), x1, y - h * (0.50 - 0.16 * kk) + 2.2, T("#6E9878", depth), 190)
    nave_roof = sk.poly_path([(x0, y - h * 0.55), (x0, y - h), (x1 - (x1 - x0) * 0.04, y - h), (x1, y - h * 0.55)])
    c.drawPath(nave_roof, skia.Paint(AntiAlias=True, Color=C(roof)))
    for k in range(12):
        c.drawLine(x0, y - h + (k + 1) * h * 0.04, x1 - (x1 - x0) * 0.03, y - h + (k + 1) * h * 0.04, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#5A2412", 70)))
    _ink(c, nave_roof, 1.3, 170)
    c.drawRect(skia.Rect.MakeLTRB(x0, y - h * 0.55, x1, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#2A1A0C", 150)))


def draw_campanile(c, x, y, w, h, T, depth=0.0, stage=None):
    """Giotto çan kulesi: renkli mermer (beyaz/pembe/yeşil), alt panel/çıkıntılar, orta çift ışıklı pencereler, üstte üç ışıklı büyük pencere + saçak.
    stage: None → eski (tam) | 0..1 → o yılın yüksekliği (donem.campanile_stage; yarımken üst kenar iskeleli)."""
    if stage is not None and stage < 1.0:
        if stage <= 0.0:
            return
        hb = h * stage
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(x - w, y - hb, x + w, y + 4))
        draw_campanile(c, x, y, w, h, T, depth, None)
        c.restore()
        c.drawLine(x - w / 2, y - hb, x + w / 2, y - hb, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C("#2A1A0C", 160)))
        _scaffold(c, x - w / 2 - 3, x + w / 2 + 3, y - hb - 16, 18, T, depth, n=4)
        return
    cream = T("#EFE6D0", depth)
    pink = T("#D9A3A0", depth)
    green = T("#7CA286", depth)
    x0, x1 = x - w / 2, x + w / 2
    _R(c, x0, y - h, x1, y, cream)
    # panel ızgarası
    rows = 13
    for r in range(rows):
        ty = y - h * (r + 1) / rows
        for k in range(3):
            tx = x0 + 4 + k * (w - 8) / 3
            col = pink if (r + k) % 2 == 0 else green
            if r < 4:
                c.drawRect(skia.Rect.MakeXYWH(tx + 1.5, ty + 2, (w - 8) / 3 - 3, h / rows - 4), skia.Paint(AntiAlias=True, Color=C(col, 190)))
            elif r in (9, 10):
                pass
    # pencereler
    for (r, big) in ((5, False), (6, False), (7, False), (8, False)):
        ty = y - h * (r + 1) / rows
        for k in range(2):
            tx = x0 + w * (0.22 + 0.34 * k)
            c.drawPath(sk.smooth_path([(tx, ty + h / rows * 0.9), (tx, ty + h / rows * 0.30), (tx + w * 0.10, ty + h / rows * 0.12), (tx + w * 0.20, ty + h / rows * 0.30), (tx + w * 0.20, ty + h / rows * 0.9)], True, 0.3),
                       skia.Paint(AntiAlias=True, Color=C(T("#3A2A1C", depth), 215)))
    ty = y - h * 11 / rows
    for k in range(3):
        tx = x0 + w * (0.10 + 0.27 * k)
        c.drawPath(sk.smooth_path([(tx, ty + h / rows * 1.9), (tx, ty + h / rows * 0.6), (tx + w * 0.08, ty + h / rows * 0.3), (tx + w * 0.16, ty + h / rows * 0.6), (tx + w * 0.16, ty + h / rows * 1.9)], True, 0.3),
                   skia.Paint(AntiAlias=True, Color=C(T("#3A2A1C", depth), 215)))
    # saçak
    _R(c, x0 - 5, y - h - 8, x1 + 5, y - h + 6, T("#E6DCBF", depth))
    for k in range(7):
        _R(c, x0 - 3 + k * (w + 6) / 7, y - h + 6, x0 - 3 + k * (w + 6) / 7 + (w + 6) / 14, y - h + 14, T("#CBBE9C", depth))
    c.drawRect(skia.Rect.MakeLTRB(x0, y - h, x1, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C("#2A1A0C", 160)))
    c.drawRect(skia.Rect.MakeLTRB(x0 - 5, y - h - 8, x1 + 5, y - h + 14), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#2A1A0C", 150)))


def draw_pv(c, x, y, s, T, depth=0.0, flag=None, stage=None):
    """Palazzo Vecchio: taş sıralı blok + mazgal/çıkma + Arnolfo kulesi (çıkmalı, çan kafesi, kiremit külah, bayrak direği). Döner: bayrak direği ucu (x,y).
    stage: None → eski (tam) | 0 → yapı yok (1299 öncesi; dönüş None) | 0..1 → yükseliyor (iskeleli)."""
    if stage is not None and stage < 1.0:
        if stage <= 0.0:
            return None
        bh_full = 120 * s + 14 * s + 190 * s + 124 * s
        hb = bh_full * stage
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(x - 400 * s, y - hb, x + 400 * s, y + 4))
        draw_pv(c, x, y, s, T, depth, flag, None)
        c.restore()
        bx0 = x - 190 * s * 0.62
        _scaffold(c, bx0, bx0 + 190 * s, y - min(hb, 120 * s) - 14, 16, T, depth, n=8)
        return None
    stone = T("#BFA77F", depth)
    stone2 = T("#A28A62", depth)
    bw, bh = 190 * s, 120 * s
    bx0 = x - bw * 0.62
    _R(c, bx0, y - bh, bx0 + bw, y, stone)
    for r in range(8):
        _R(c, bx0, y - bh + r * bh / 8, bx0 + bw, y - bh + r * bh / 8 + 1.4, stone2, 160)
    for r, ry in enumerate((0.20, 0.52)):
        for k in range(5):
            wx = bx0 + bw * (0.10 + 0.19 * k)
            c.drawPath(sk.smooth_path([(wx, y - bh * (1 - ry) + bh * 0.22), (wx, y - bh * (1 - ry) + bh * 0.06), (wx + bw * 0.035, y - bh * (1 - ry)), (wx + bw * 0.07, y - bh * (1 - ry) + bh * 0.06), (wx + bw * 0.07, y - bh * (1 - ry) + bh * 0.22)], True, 0.3),
                       skia.Paint(AntiAlias=True, Color=C(T("#3A2A1C", depth), 200)))
    # çıkma + mazgal
    _R(c, bx0 - 6 * s, y - bh - 14 * s, bx0 + bw + 6 * s, y - bh + 2, T("#8A7452", depth))
    for k in range(int(bw / (14 * s)) + 1):
        c.drawPath(sk.poly_path([(bx0 - 6 * s + k * 14 * s, y - bh + 2), (bx0 - 6 * s + k * 14 * s + 7 * s, y - bh + 14 * s), (bx0 - 6 * s + k * 14 * s + 14 * s, y - bh + 2)]), skia.Paint(AntiAlias=True, Color=C("#3A2A1C", 190)))
    for k in range(int((bw + 12 * s) / (16 * s))):
        _R(c, bx0 - 6 * s + k * 16 * s, y - bh - 28 * s, bx0 - 6 * s + k * 16 * s + 9 * s, y - bh - 14 * s, T("#8A7452", depth))
    c.drawRect(skia.Rect.MakeLTRB(bx0, y - bh, bx0 + bw, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C("#2A1A0C", 160)))
    # kule
    tx = bx0 + bw * 0.28
    tw = 40 * s
    th = 190 * s
    y_top = y - bh - 14 * s
    _R(c, tx - tw / 2, y_top - th, tx + tw / 2, y_top, stone)
    for r in range(10):
        _R(c, tx - tw / 2, y_top - th + r * th / 10, tx + tw / 2, y_top - th + r * th / 10 + 1.2, stone2, 150)
    for ry in (0.20, 0.50):
        c.drawPath(sk.smooth_path([(tx - 5 * s, y_top - th * (1 - ry) + 18 * s), (tx - 5 * s, y_top - th * (1 - ry) + 4 * s), (tx, y_top - th * (1 - ry)), (tx + 5 * s, y_top - th * (1 - ry) + 4 * s), (tx + 5 * s, y_top - th * (1 - ry) + 18 * s)], True, 0.3), skia.Paint(AntiAlias=True, Color=C("#3A2A1C", 200)))
    gy = y_top - th
    _R(c, tx - tw * 0.80, gy - 16 * s, tx + tw * 0.80, gy + 2, T("#8A7452", depth))
    for k in range(7):
        c.drawPath(sk.poly_path([(tx - tw * 0.80 + k * tw * 1.6 / 7, gy + 2), (tx - tw * 0.80 + (k + 0.5) * tw * 1.6 / 7, gy + 12 * s), (tx - tw * 0.80 + (k + 1) * tw * 1.6 / 7, gy + 2)]), skia.Paint(AntiAlias=True, Color=C("#3A2A1C", 190)))
    for k in range(6):
        _R(c, tx - tw * 0.80 + k * tw * 1.6 / 6, gy - 30 * s, tx - tw * 0.80 + k * tw * 1.6 / 6 + tw * 1.6 / 12, gy - 16 * s, T("#8A7452", depth))
    _R(c, tx - tw * 0.55, gy - 66 * s, tx + tw * 0.55, gy - 30 * s, stone)
    for k in (-0.3, 0.3):
        c.drawPath(sk.smooth_path([(tx + k * tw - 4 * s, gy - 34 * s), (tx + k * tw - 4 * s, gy - 56 * s), (tx + k * tw, gy - 62 * s), (tx + k * tw + 4 * s, gy - 56 * s), (tx + k * tw + 4 * s, gy - 34 * s)], True, 0.3), skia.Paint(AntiAlias=True, Color=C("#3A2A1C", 210)))
    roof = sk.poly_path([(tx - tw * 0.66, gy - 66 * s), (tx, gy - 104 * s), (tx + tw * 0.66, gy - 66 * s)])
    c.drawPath(roof, skia.Paint(AntiAlias=True, Color=C(T("#B4552E", depth))))
    _ink(c, roof, 1.2, 170)
    c.drawRect(skia.Rect.MakeLTRB(tx - tw / 2, y_top - th, tx + tw / 2, y_top), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C("#2A1A0C", 160)))
    c.drawLine(tx, gy - 104 * s, tx, gy - 124 * s, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0, Color=C("#2A1A0C", 200)))
    c.drawCircle(tx, gy - 104 * s, 3.6 * s, skia.Paint(AntiAlias=True, Color=C(T("#D8A63A", depth))))
    return (tx, gy - 124 * s)


def draw_bapt(c, x, y, w, h, T, depth=0.0):
    """Vaftizhane: sekizgen beyaz-yeşil mermer blok + alçak piramit çatı + küçük fener."""
    cream, green = T("#EFE5CC", depth), T("#6E9878", depth)
    _R(c, x - w / 2, y - h, x + w / 2, y, cream)
    for k in range(3):
        _R(c, x - w / 2, y - h * (0.18 + 0.30 * k), x + w / 2, y - h * (0.18 + 0.30 * k) + 2.4, green, 210)
    for k in range(5):
        xx = x - w / 2 + 8 + k * (w - 16) / 5
        c.drawPath(sk.smooth_path([(xx, y - h * 0.50), (xx, y - h * 0.72), (xx + 6, y - h * 0.80), (xx + 12, y - h * 0.72), (xx + 12, y - h * 0.50)], True, 0.3), skia.Paint(AntiAlias=True, Color=C(T("#4A3A28", depth), 170)))
    roof = sk.poly_path([(x - w * 0.52, y - h), (x - w * 0.14, y - h - h * 0.42), (x + w * 0.14, y - h - h * 0.42), (x + w * 0.52, y - h)])
    c.drawPath(roof, skia.Paint(AntiAlias=True, Color=C(T("#8E8878", depth))))
    c.drawRect(skia.Rect.MakeLTRB(x - w * 0.07, y - h - h * 0.62, x + w * 0.07, y - h - h * 0.42), skia.Paint(AntiAlias=True, Color=C(cream)))
    c.drawPath(sk.poly_path([(x - w * 0.09, y - h - h * 0.62), (x, y - h - h * 0.80), (x + w * 0.09, y - h - h * 0.62)]), skia.Paint(AntiAlias=True, Color=C(T("#E3D8BA", depth))))
    _ink(c, roof, 1.2, 160)
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, y - h, x + w / 2, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#2A1A0C", 150)))


def draw_tower(c, x, y, w, h, T, depth=0.0, spire=False):
    stone = T("#B8A07A", depth)
    _R(c, x - w / 2, y - h, x + w / 2, y, stone)
    for r in range(int(h / 14)):
        _R(c, x - w / 2, y - h + r * 14, x + w / 2, y - h + r * 14 + 1.0, T("#9C855F", depth), 150)
    if spire:
        c.drawPath(sk.poly_path([(x - w * 0.62, y - h), (x, y - h - w * 2.6), (x + w * 0.62, y - h)]), skia.Paint(AntiAlias=True, Color=C(T("#9A8E7A", depth))))
    else:
        for k in range(3):
            _R(c, x - w / 2 - 2 + k * (w + 4) / 3 * 1.0, y - h - 11, x - w / 2 - 2 + k * (w + 4) / 3 + (w + 4) / 6, y - h, stone)
        _R(c, x - w / 2 - 3, y - h, x + w / 2 + 3, y - h + 6, T("#8A7452", depth))
    for ry in (0.30, 0.62):
        c.drawPath(sk.smooth_path([(x - 3, y - h * (1 - ry) + 14), (x - 3, y - h * (1 - ry) + 3), (x, y - h * (1 - ry)), (x + 3, y - h * (1 - ry) + 3), (x + 3, y - h * (1 - ry) + 14)], True, 0.3), skia.Paint(AntiAlias=True, Color=C(T("#3A2A1C", depth), 200)))
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, y - h, x + w / 2, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#2A1A0C", 150)))


WALLS = ["#E1CFA6", "#D8B88A", "#E5C7A4", "#CFB080", "#E7D9B4", "#D6A98A"]
ROOFS = ["#B9552F", "#C46A3A", "#A84B2A", "#B65E36"]


def draw_house(c, x, y, w, h, rs, T, depth=0.0, win_boxes=None, hip=None, rec=None):
    wall = T(WALLS[rs.randint(len(WALLS))], depth)
    roof = T(ROOFS[rs.randint(len(ROOFS))], depth)
    if rec is not None:
        rec.append((x, w, wall, roof))
    _R(c, x, y - h, x + w, y, wall)
    c.drawRect(skia.Rect.MakeLTRB(x + w * 0.72, y - h, x + w, y), skia.Paint(Color=C("#2A1A0C", 36)))
    rh = min(h * 0.45, w * 0.40) * (0.7 + 0.5 * rs.rand())
    if hip is None:
        hip = rs.rand() < 0.5
    if hip:
        path = sk.poly_path([(x - 3, y - h), (x + w * 0.18, y - h - rh), (x + w * 0.82, y - h - rh), (x + w + 3, y - h)])
    else:
        path = sk.poly_path([(x - 3, y - h), (x + w * 0.5, y - h - rh * 1.25), (x + w + 3, y - h)])
    c.drawPath(path, skia.Paint(AntiAlias=True, Color=C(roof)))
    _ink(c, path, 1.0, 150)
    nwx = max(1, int(w / 24))
    nwy = max(1, int((h - 10) / 30))
    for ix in range(nwx):
        for iy in range(nwy):
            wx = x + (ix + 0.5) * w / nwx - 3.5
            wy = y - h + 8 + iy * (h - 14) / nwy
            c.drawRect(skia.Rect.MakeXYWH(wx, wy, 7, 11), skia.Paint(Color=C(T("#3A2A1C", depth), 190)))
            if win_boxes is not None:
                win_boxes.append((wx, wy, 7, 11))
    c.drawRect(skia.Rect.MakeLTRB(x, y - h, x + w, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#2A1A0C", 140)))


def draw_bridge(c, x, y, w, T, rs, win_boxes=None):
    """Ponte Vecchio: üç segmental kemer + ayak başlarında üçgen kesme + üstte çıkmalı (konsollu) dükkânlar; ortada açıklık."""
    stone = T("#9C8A68", 0.0)
    stone2 = T("#7E6E50", 0.0)
    deck = y
    ph = 66
    n = 3
    aw = w / n
    # gövde + kemerler
    _R(c, x - w / 2, deck, x + w / 2, deck + ph, stone)
    for r in range(5):
        _R(c, x - w / 2, deck + 6 + r * 12, x + w / 2, deck + 7.2 + r * 12, stone2, 120)
    for k in range(n):
        ax = x - w / 2 + (k + 0.5) * aw
        p = skia.Path()
        p.moveTo(ax - aw * 0.36, deck + ph)
        p.quadTo(ax, deck + ph - ph * 1.30, ax + aw * 0.36, deck + ph)
        p.close()
        c.drawPath(p, skia.Paint(AntiAlias=True, Color=C(T("#1B3340", 0.0), 245)))
        _ink(c, p, 1.4, 190)
    for k in range(n + 1):                                  # ayak başları (üçgen kesme)
        px = x - w / 2 + k * aw
        c.drawPath(sk.poly_path([(px - aw * 0.04, deck + ph), (px, deck + ph - 16), (px + aw * 0.04, deck + ph)]), skia.Paint(AntiAlias=True, Color=C(stone2)))
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, deck, x + w / 2, deck + ph), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C("#2A1A0C", 170)))
    # dükkânlar: iki blok, ortada açıklık; çıkma konsolları köprü kenarlarına taşar
    pal = ["#C9772F", "#D8B070", "#BE5A35", "#E0C9A0", "#A8683A"]
    for (x0, x1) in ((x - w / 2 - 6, x - w * 0.115), (x + w * 0.115, x + w / 2 + 6)):
        cur = x0
        while cur < x1 - 14:
            bw_ = min(x1 - cur, rs.uniform(36, 58))
            bh = rs.uniform(62, 84)
            col = T(pal[rs.randint(len(pal))], 0.0)
            oh = rs.uniform(5, 10)
            yb = deck + rs.uniform(-2, 2)
            _R(c, cur - oh, yb - bh, cur + bw_ + oh * 0.5, yb - bh + 16, T("#6C4C2C", 0.0))          # çıkma (ahşap)
            for kk in range(3):                                                                       # konsollar
                bx = cur - oh + kk * (bw_ + oh * 1.5) / 3
                c.drawLine(bx, yb - bh + 16, bx + 4, yb - bh + 28, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2, Color=C(T("#4A3420", 0.0), 220)))
            _R(c, cur, yb - bh + 16, cur + bw_, yb, col)
            c.drawRect(skia.Rect.MakeLTRB(cur + bw_ * 0.74, yb - bh + 16, cur + bw_, yb), skia.Paint(Color=C("#2A1A0C", 38)))
            roof = sk.poly_path([(cur - oh - 2, yb - bh), (cur + bw_ * 0.5, yb - bh - 18), (cur + bw_ + oh * 0.5 + 2, yb - bh)])
            c.drawPath(roof, skia.Paint(AntiAlias=True, Color=C(T("#A8472A", 0.0))))
            _ink(c, roof, 1.0, 160)
            wx = cur + bw_ * 0.5 - 5
            c.drawRect(skia.Rect.MakeXYWH(wx, yb - bh + 28, 10, 15), skia.Paint(Color=C(T("#3A2A1C", 0.0), 215)))
            c.drawLine(wx, yb - bh + 35.5, wx + 10, yb - bh + 35.5, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#C9A860", 120)))
            if win_boxes is not None:
                win_boxes.append((wx, yb - bh + 28, 10, 15))
            c.drawRect(skia.Rect.MakeLTRB(cur, yb - bh + 16, cur + bw_, yb), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#2A1A0C", 150)))
            cur += bw_ + rs.uniform(1, 4)


# ───────────────────────────── katmanlar ─────────────────────────────
def _arr(fr):
    return fr.surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kUnpremul_AlphaType)


_AUTO = object()


def era_key(y=_AUTO):
    """Dönem anahtarı (önbellek + çizim): (DuomoStage, çan kulesi oranı, Palazzo Vecchio oranı, San Lorenzo kubbesi) ya da None (yıl yok → eski çizim)."""
    y = DN.year() if y is _AUTO else y
    if y is None:
        return None
    return (DN.duomo_stage(y), DN.campanile_stage(y), DN.pv_stage(y), DN.sanlorenzo_dome(y))


def era_tag(era):
    """Önbellek dosya adı eki: '' (eski) ya da '_e<…>'."""
    if era is None:
        return ""
    d, cp, pv, sl = era
    return f"_e{d.tag()}c{int(round(cp * 1000))}p{int(round(pv * 1000))}{'s' if sl else 'n'}"


def note_era(where, era, **extra):
    """Dönem kaydı (qa_donem): bu karede çizilen Duomo/çan kulesi durumu."""
    if not DN.LOG_ON:
        return
    if era is None:
        DN.note_once_per_frame("duomo", where=where, era=None, **extra)
        return
    d, cp, pv, sl = era
    DN.note_once_per_frame("duomo", where=where, nave=d.nave, tribune=d.tribune, drum=d.drum, dome=d.dome, lantern=d.lantern, ball=d.ball, **extra)
    DN.note_once_per_frame("campanile", where=where, h=cp, **extra)
    DN.note_once_per_frame("pv", where=where, h=pv, **extra)
    DN.note_once_per_frame("sanlorenzo", where=where, dome=bool(sl), **extra)


def draw_duomo_group(c, cx_dome, base, T, era, nave=(70, 640, 4, 124), bapt=(700, 6, 96, 64), dome=(-108, 214, 132, 48, 74), camp=(205, 4, 54, 262),
                     depth=(0.16, 0.12, 0.12, 0.12)):
    """Duomo grubu (nef + Vaftizhane + kubbe + çan kulesi) — dönem anahtarına göre (era None → eski tam hâl). Koordinatlar cx_dome'a göre."""
    d = cp = None
    if era is not None:
        d, cp = era[0], era[1]
    n0, n1, ny, nh = nave
    if d is None or d.nave >= 1.0:
        draw_nave(c, cx_dome + n0, cx_dome + n1, base + ny, nh, T, depth[0])
    elif d.nave > 0.0:                                   # 1296–1380: nef inşa hâlinde (çatı yok/iskele)
        draw_nave(c, cx_dome + n0, cx_dome + n1, base + ny, nh * (0.55 + 0.45 * d.nave), T, depth[0])
        _scaffold(c, cx_dome + n0, cx_dome + n0 + (n1 - n0) * 0.45, base + ny - nh * (0.55 + 0.45 * d.nave) - 14, 16, T, depth[0], n=9, a=180)
    else:                                               # 1296 öncesi: eski Santa Reparata (alçak bazilika)
        draw_nave(c, cx_dome + n0 + (n1 - n0) * 0.25, cx_dome + n1, base + ny, nh * 0.62, T, depth[0])
    bx, by, bw, bh = bapt
    draw_bapt(c, cx_dome + bx, base + by, bw, bh, T, depth[1])
    if d is None or d.nave > 0.0:
        dy, dw, dhd, ddr, dl = dome
        draw_dome(c, cx_dome, base + dy, dw, dhd, ddr, dl, T, depth[2], stage=d)
    cxo, cyo, cw, chh = camp
    draw_campanile(c, cx_dome + cxo, base + cyo, cw, chh, T, depth[3], stage=cp)


def city_layers(PH=700, seed=1, mode="day", corner=True, era=_AUTO):
    """Dönüş: dict(sky, hills, far, near, W_sky, W_hills, W_far, W_near, flag=(x,y) in far, windows) — her biri skia.Image.
    era: dönem anahtarı (varsayılan: o an çizilen çekimin yılı, donem.year(); yıl yoksa eski tam Floransa)."""
    if era is _AUTO:
        era = era_key()
    L = _city_layers(PH, seed, mode, corner, era)
    note_era("skyline", era)
    return L


@functools.lru_cache(maxsize=6)
def _city_layers(PH=700, seed=1, mode="day", corner=True, era=None):
    T = Tint(mode)
    rs = np.random.RandomState(seed)
    night = mode == "night"
    out = {}
    base_far = int(PH * 0.745)          # uzak şehir tabanı
    base_near = int(PH * 0.80)          # kıyı evleri tabanı
    river_y0 = int(PH * 0.80)
    # ---- gökyüzü
    w_sky = 1920 + int(PW_EXTRA * 0.12) + 40
    fr = Frame(w_sky, PH)
    c = fr.c
    if mode == "day":
        SC.sky_gradient(c, w_sky, PH * 0.85, "#78A0D4", "#BED0DC", "#F2E6C8")
        SC.clouds(c, w_sky, PH * 0.6, rs, 6)
    elif mode == "dusk":
        SC.sky_gradient(c, w_sky, PH * 0.85, "#5A6FA8", "#E8A07A", "#F8D9A0")
        SC.clouds(c, w_sky, PH * 0.6, rs, 5)
    else:
        SC.sky_gradient(c, w_sky, PH * 0.85, "#080F30", "#17286A", "#5A6EAA")
        for i in range(int(w_sky / 12)):
            c.drawCircle(rs.uniform(0, w_sky), rs.uniform(0, PH * 0.5), rs.uniform(0.7, 1.9), skia.Paint(AntiAlias=True, Color=C("#FFF2C4", int(rs.uniform(80, 230)))))
        mx, my = w_sky * 0.78, PH * 0.20
        c.drawCircle(mx, my, 70, skia.Paint(AntiAlias=True, Color=C("#FFF1C0", 38), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30)))
        disc = skia.Path()
        disc.addCircle(mx, my, 34)
        cut = skia.Path()
        cut.addCircle(mx - 14, my - 8, 29)
        try:
            cres = skia.Op(disc, cut, skia.PathOp.kDifference_PathOp)
        except Exception:
            cres = disc
        c.drawPath(cres or disc, skia.Paint(AntiAlias=True, Color=C("#FFF3CE")))                     # hilal
    out["sky"] = fr.surf.makeImageSnapshot()
    # ---- tepeler (Fiesole)
    w_h = 1920 + int(PW_EXTRA * 0.30) + 40
    fr = Frame(w_h, PH)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    hor = PH * 0.50
    for col, amp, sc, off in (("#A9BDB6", 40, 600, 0), ("#93AFA5", 46, 420, 34), ("#7F9E92", 52, 300, 70)):
        xs, ys = SC._ridge(rs, w_h, hor + off, amp, sc)
        cc = T(col, 0.2)
        c.drawPath(SC._poly_from_ridge(xs, ys, PH), skia.Paint(AntiAlias=True, Color=C(cc)))
        c.drawPath(sk.poly_path([(float(x), float(y)) for x, y in zip(xs, ys)], False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, Color=C(mix(cc, "#1A2A22", 0.5), 150)))
        for j in range(w_h // 120):
            i = rs.randint(2, len(xs) - 2)
            SC.cypress(c, float(xs[i]), float(ys[i]) + 3, rs.uniform(26, 44), T("#2E4A33", 0.3), T("#4F6E4A", 0.3))
    for j in range(max(2, w_h // 800)):
        i = rs.randint(8, len(xs) - 8)
        SC.castle(c, float(xs[i]), float(ys[i]) + 3, rs.uniform(26, 36), T("#E6D9B8", 0.3), T("#B4552E", 0.3))
    out["hills"] = fr.surf.makeImageSnapshot()
    # ---- uzak şehir + anıtlar
    w_far = 1920 + int(PW_EXTRA * 0.62) + 40
    fr = Frame(w_far, PH)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    wins_far = []
    x = -30
    while x < w_far + 30:                    # uzak çatılar
        bw = rs.uniform(30, 64)
        bh = rs.uniform(26, 62)
        draw_house(c, x, base_far + rs.uniform(-4, 6), bw, bh, rs, T, 0.45, wins_far)
        x += bw + rs.uniform(-4, 8)
    S = 1.0
    ox = w_far * 0.0
    px = 760
    cx_dome = 1210
    # Santa Croce çan kulesi, torri
    draw_tower(c, 330, base_far, 30, 170, T, 0.30, spire=True)
    for tx, th in ((560, 120), (940, 138), (1620, 150), (1960, 118)):
        draw_tower(c, tx, base_far, 28, th, T, 0.35)
    flag = draw_pv(c, px, base_far + 4, 1.0, T, 0.18, stage=None if era is None else era[2])
    if flag is None:                                                     # Palazzo Vecchio henüz yok/yarım: flama ortaçağ kulesinde
        flag = (940, base_far - 149)
    if era is None or era[3]:
        draw_dome(c, 2150, base_far - 18, 120, 82, 32, 44, T, 0.28)      # San Lorenzo (uzak, batıda; büyük kubbe 1604 sonrası)
    draw_duomo_group(c, cx_dome, base_far, T, era)
    x = 80
    while x < w_far:                          # önde ikinci sıra evler
        bw = rs.uniform(36, 70)
        bh = rs.uniform(30, 70)
        draw_house(c, x, base_far + 18 + rs.uniform(-3, 5), bw, bh, rs, T, 0.25, wins_far)
        x += bw + rs.uniform(-6, 6)
    out["far"] = fr.surf.makeImageSnapshot()
    out["flag"] = flag
    # ---- yakın: kıyı evleri + köprü + nehir + sur
    w_near = 1920 + int(PW_EXTRA * 0.92) + 40
    fr = Frame(w_near, PH)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    wins_near = []
    rec_near = []
    bridge_x = 880
    x = -20
    while x < w_near + 20:
        bw = rs.uniform(48, 92)
        bh = rs.uniform(56, 116)
        if abs((x + bw / 2) - bridge_x) < 230:
            x += bw
            continue
        draw_house(c, x, base_near + rs.uniform(-4, 2), bw, bh, rs, T, 0.0, wins_near, rec=rec_near)
        x += bw + rs.uniform(-8, 6)
    # nehir
    sh = skia.GradientShader.MakeLinear([(0, river_y0 - 2), (0, PH)], [C(T("#8FB0B0", 0.1)), C(T("#4E7C86", 0.0)), C(T("#2E566A", 0.0))], [0, 0.45, 1])
    c.drawRect(skia.Rect.MakeLTRB(0, river_y0 - 2, w_near, PH), skia.Paint(Shader=sh))
    for i in range(int(w_near / 14)):
        yy = rs.uniform(river_y0 + 8, PH - 8)
        xx = rs.uniform(0, w_near)
        c.drawLine(xx, yy, xx + rs.uniform(14, 52), yy, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C("#FFFFFF" if rs.rand() < 0.6 else "#1E3A4A", int(rs.uniform(36, 90)))))
    # evlerin nehirdeki yansıması (dalgalı kısa şeritler)
    for (hx, hw, wcol, rcol) in rec_near:
        for j in range(6):
            yy = river_y0 + 10 + j * 15 + rs.uniform(-2, 2)
            ww = hw * (0.92 - 0.09 * j)
            xx = hx + (hw - ww) / 2 + math.sin(j * 1.7 + hx) * 4
            col = rcol if j == 0 else wcol
            _R(c, xx, yy, xx + ww, yy + 4.2, col, int(112 - j * 17))
    # kıyı seti (ev diplerinde taş duvar)
    _R(c, 0, base_near - 2, w_near, river_y0 + 6, T("#9C8B6C", 0.0))
    for k in range(int(w_near / 36)):
        _R(c, k * 36, base_near + 2, k * 36 + 2, river_y0 + 4, T("#6E5E44", 0.0), 120)
    c.drawLine(0, river_y0 + 6, w_near, river_y0 + 6, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0, Color=C("#2A1A0C", 160)))
    draw_bridge(c, bridge_x, river_y0 - 40, 430, T, rs, wins_near)
    # köprü kemerleri altı: koyu su yansıması
    # ön sur / ağaçlar
    for tx in (60, w_near - 90, 1500):
        SC.cypress(c, tx, PH - 4, rs.uniform(150, 210), T("#2E4A33", 0.0), T("#4F6E4A", 0.0))
    out["lit_near"] = []
    out["lit_far"] = []
    if night or mode == "dusk":
        out["lit_near"] = _lit_windows(c, rs, wins_near, night, 0.55 if night else 0.25)
    out["near"] = fr.surf.makeImageSnapshot()
    if night or mode == "dusk":
        # uzak pencere ışıkları far katmanına: yeniden çiz
        fr2 = Frame(w_far, PH)
        fr2.clear(skia.ColorTRANSPARENT)
        fr2.c.drawImage(out["far"], 0, 0)
        out["lit_far"] = _lit_windows(fr2.c, rs, wins_far, night, 0.5 if night else 0.2)
        out["far"] = fr2.surf.makeImageSnapshot()
    # ---- fresk dokusu: yalnız kenar kaybı + çatlak (alfa delikleri: sky, hills hariç tutulabilir)
    for key in ("sky", "far", "near"):
        im = out[key]
        arr = im.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kUnpremul_AlphaType)
        if key == "sky":
            arr[..., 3] = 255
        out[key] = sk.np_to_image(SC._bake_texture(arr, rs, {"sky": -1.5, "far": -1.1, "near": -1.4}[key], 0.55))
    out["w"] = dict(sky=w_sky, hills=w_h, far=w_far, near=w_near)
    return out


SPEEDS = dict(sky=0.12, hills=0.30, far=0.62, near=0.92)


def anchors(PH=700, era=_AUTO):
    """Anıt çapaları: ad → (katman, x, y) katman uzayında (üst uç). Dönem modunda Duomo/çan kulesi çapası o yılki yapının üstüne iner."""
    bf = int(PH * 0.745)
    rv = int(PH * 0.80)
    if era is _AUTO:
        era = era_key()
    duo_y, camp_y = bf - 374, bf - 274
    if era is not None:
        duo_y = int(dome_top(1210, bf - 108, 214, 132, 48, 74, era[0])[1])
        if era[1] < 1.0:
            camp_y = int(bf + 4 - 262 * era[1] - 18)
    return dict(
        duomo=("far", 1210, duo_y), campanile=("far", 1415, camp_y), pv=("far", 695, bf - 444),
        bapt=("far", 1910, bf - 112), santacroce=("far", 330, bf - 250), ponte=("near", 880, rv - 40 - 112),
        arno=("near", 1300, rv + 70),
    )
