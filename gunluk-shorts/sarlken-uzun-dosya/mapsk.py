"""Skia harita çizici: mapdata.py (Natural Earth 50m → dünya pikseli, tarihsel bölgeler) üzerinde.
Stiller: 'night' (kehribar-siyah zemin, altın kıyı ışıması) ve 'paper' (parşömen, mürekkep kıyı).
Kullanım:  mv = MapView(); cam = mv.cam(lon, lat, zoom); mv.base(f, cam, 'night'); mv.region(f, cam, 'ispanya', color)...
"""
import math

import numpy as np
import shapely
from shapely.geometry import Point
from shapely.prepared import prep

import mapdata
import skia
from sk import (C, Frame, H, P, W, clamp, ease_io, ease_out, lerp, mix, poly_path, smooth, smooth_path, text_width)

LEVELS = mapdata.LEVELS


class Cam:
    """Dünya pikseli ↔ ekran. (lon,lat) merkezde, zoom=1'de 32 px/derece; rot radyan (isteğe bağlı)."""

    def __init__(self, lon, lat, zoom, rot=0.0, cx=W / 2, cy=H / 2):
        self.lon, self.lat, self.zoom, self.rot = lon, lat, zoom, rot
        self.wx, self.wy = mapdata.to_world(lon, lat)
        self.cx, self.cy = cx, cy

    def w2s(self, x, y):
        dx, dy = (x - self.wx) * self.zoom, (y - self.wy) * self.zoom
        if self.rot:
            cr, sr = math.cos(self.rot), math.sin(self.rot)
            dx, dy = dx * cr - dy * sr, dx * sr + dy * cr
        return self.cx + dx, self.cy + dy

    def ll(self, lon, lat):
        return self.w2s(*mapdata.to_world(lon, lat))

    def apply(self, c):
        c.translate(self.cx, self.cy)
        if self.rot:
            c.rotate(math.degrees(self.rot))
        c.scale(self.zoom, self.zoom)
        c.translate(-self.wx, -self.wy)

    def visible(self, lon, lat, margin=80):
        x, y = self.ll(lon, lat)
        return -margin <= x <= W + margin and -margin <= y <= H + margin


def lerp_cam(a, b, t):
    """Kamera ara değeri: zoom logaritmik, merkez doğrusal (ekran-sabit his için zoom'a bağlı)."""
    z = math.exp(lerp(math.log(a.zoom), math.log(b.zoom), t))
    return Cam(lerp(a.lon, b.lon, t), lerp(a.lat, b.lat, t), z, lerp(a.rot, b.rot, t))


def cam_move(a, b, t, ease=ease_io):
    """a=(lon,lat,zoom) → b=(lon,lat,zoom); t 0..1. Büyük zoom değişiminde merkezi uzakta-yakında karıştırır (zoom-out-in)."""
    u = ease(clamp(t))
    z = math.exp(lerp(math.log(a[2]), math.log(b[2]), u))
    # merkez ekran-uzayında doğrusal olsun diye 1/zoom ağırlıklı karıştır
    ia, ib = 1.0 / a[2], 1.0 / b[2]
    iz = lerp(ia, ib, u)
    w = (iz - ia) / (ib - ia) if abs(ib - ia) > 1e-9 else u
    return Cam(lerp(a[0], b[0], w), lerp(a[1], b[1], w), z)


class MapView:
    def __init__(self):
        self.D = mapdata.data()
        self._paths = {}
        land = self.D["regions"]["__kara__"][1.0]
        polys = []
        from shapely.geometry import Polygon
        for ext, holes in land:
            try:
                polys.append(Polygon(ext, holes))
            except Exception:
                pass
        self._landprep = prep(shapely.union_all([p.buffer(0) for p in polys]))
        m = self.D["mount"]
        keep = [i for i in range(len(m)) if self._landprep.contains(Point(float(m[i][0]), float(m[i][1])))]
        self.mount = m[keep]
        self._rip = None

    # ---- yol önbelleği
    def level(self, zoom):
        lv = LEVELS[0]
        for z in LEVELS:
            if z <= zoom * 1.25:
                lv = z
        return lv

    def path(self, name, zoom):
        lv = self.level(zoom)
        key = (name, lv)
        if key not in self._paths:
            p = skia.Path()
            p.setFillType(skia.PathFillType.kEvenOdd)
            for ext, holes in self.D["regions"][name][lv]:
                p.addPoly([tuple(map(float, q)) for q in ext], True)
                for h in holes:
                    p.addPoly([tuple(map(float, q)) for q in h], True)
            self._paths[key] = p
        return self._paths[key]

    def ripple_paths(self):
        if self._rip is None:
            self._rip = []
            for d, rings in self.D["ripples"]:
                p = skia.Path()
                for r in rings:
                    p.addPoly([tuple(map(float, q)) for q in r], True)
                self._rip.append((d, p))
        return self._rip

    def cam(self, lon, lat, zoom, rot=0.0):
        return Cam(lon, lat, zoom, rot)

    # ---- zemin
    def base(self, f, cam, style="night", t=0.0, mountains=True, ripples=True, tint=None):
        c = f.c
        night = style == "night"
        if night:
            f.rect(0, 0, W, H, shader=f.lin(0, 0, 0, H, [("#16293A", 0.0), ("#0D1822", 1.0)]))
        else:
            f.rect(0, 0, W, H, shader=f.rad(W / 2, H / 2, H * 1.0, [("#EBDDB8", 0.0), ("#D9C697", 1.0)]))
        c.save()
        cam.apply(c)
        z = cam.zoom
        land = self.path("__kara__", z)
        sw = 1.0 / z
        # kıyı dalgaları
        if ripples:
            for i, (d, p) in enumerate(self.ripple_paths()):
                a = [0.34, 0.20, 0.11][i] * (1.0 if z > 0.45 else clamp(z / 0.45))
                col = "#6FA3B8" if night else "#7A5F36"
                lw = (1.4 if night else 1.2) * sw
                c.drawPath(p, f.paint(col, style="stroke", sw=lw, alpha=a))
        # kara dolgusu
        if night:
            c.drawPath(land, f.paint(shader=skia.GradientShader.MakeLinear([(0, 0), (0, H)], [C("#4A3524"), C("#33241A")], None) if False else None, color="#3C2B1D"))
        else:
            c.drawPath(land, f.paint("#E7D3A4"))
        if tint:
            c.drawPath(land, f.paint(tint[0], alpha=tint[1]))
        # dağlar
        if mountains and z > 1.6:
            mp = skia.Path()
            for x, y, s, sd in self.mount:
                ss = s * 0.9
                mp.moveTo(x - ss, y + ss * 0.5)
                mp.lineTo(x, y - ss * 0.7)
                mp.lineTo(x + ss, y + ss * 0.5)
                mp.moveTo(x, y - ss * 0.7)
                mp.lineTo(x + ss * 0.25, y + ss * 0.5)
            c.drawPath(mp, f.paint("#8A6A44" if night else "#8C6B3E", style="stroke", sw=1.3 * sw, alpha=0.55 if night else 0.7))
        # kıyı çizgisi: dış ışıma + keskin hat
        if night:
            c.drawPath(land, f.paint("#E3B54A", style="stroke", sw=7 * sw, alpha=0.16, blur=3.5 * sw))
            c.drawPath(land, f.paint("#E3B54A", style="stroke", sw=1.6 * sw, alpha=0.85))
        else:
            c.drawPath(land, f.paint("#4E3419", style="stroke", sw=1.5 * sw, alpha=0.9))
        c.restore()

    # ---- bölge
    def region(self, f, cam, name, color, alpha=0.62, edge=None, glow=True, amt=1.0, hatch=False, style="night"):
        if amt <= 0:
            return
        c = f.c
        c.save()
        cam.apply(c)
        z = cam.zoom
        p = self.path(name, z)
        sw = 1.0 / z
        a = alpha * amt
        c.drawPath(p, f.paint(color, alpha=a))
        if hatch:
            c.save()
            c.clipPath(p, skia.ClipOp.kIntersect, True)
            hp = skia.Path()
            step = 9 / z
            x0, y0 = cam.wx - W / 2 / z - 40 / z, cam.wy - H / 2 / z - 40 / z
            n = int((W + H) / 9) + 8
            for i in range(n):
                hp.moveTo(x0 + i * step, y0)
                hp.lineTo(x0 + i * step - H / z, y0 + H / z + 80 / z)
            c.drawPath(hp, f.paint(mix(color, "#FFFFFF", 0.35), style="stroke", sw=1.2 * sw, alpha=0.30 * amt))
            c.restore()
        ec = edge or mix(color, "#FFFFFF", 0.45)
        if glow:
            c.save()
            c.clipPath(p, skia.ClipOp.kIntersect, True)
            c.drawPath(p, f.paint(ec, style="stroke", sw=22 * sw, alpha=0.38 * amt, blur=7 * sw))
            c.restore()
        c.drawPath(p, f.paint(ec, style="stroke", sw=1.8 * sw, alpha=0.95 * amt))
        c.restore()

    # ---- ekran uzayı çizimleri (kamera sonrası)
    def label(self, f, cam, text, lon, lat, size=34, color="#E8D7A4", face="title_m", track=8.0, alpha=1.0, rot=0.0, shadow=True, dy=0.0, scale_with_zoom=0.0):
        x, y = cam.ll(lon, lat)
        s = size * (cam.zoom ** scale_with_zoom if scale_with_zoom else 1.0)
        f.c.save()
        f.c.translate(x, y + dy)
        if rot:
            f.c.rotate(math.degrees(rot))
        f.text(text, 0, 0, face=face, size=s, color=color, align="c", track=track * s / 34.0, alpha=alpha,
               shadow=(2, 2, 3, "#000000") if shadow else None)
        f.c.restore()

    def city(self, f, cam, lon, lat, name=None, kind="town", t=0.0, alpha=1.0, color="#F0D27A", size=26, dx=14, dy=-10, name_side="r", amt=1.0):
        x, y = cam.ll(lon, lat)
        a = alpha * amt
        if a <= 0:
            return
        r = 6.5 * (0.6 + 0.4 * amt)
        if kind in ("capital", "seat"):
            f.circle(x, y, r * 2.4, color=color, alpha=0.18 * a, blur=6)
            star = [(x + (r * 1.9 if i % 2 == 0 else r * 0.8) * math.cos(math.pi * i / 4 - math.pi / 2), y + (r * 1.9 if i % 2 == 0 else r * 0.8) * math.sin(math.pi * i / 4 - math.pi / 2)) for i in range(8)]
            f.poly(star, color=color, alpha=a)
            f.poly(star, style="stroke", sw=1.4, color="#2A1A0C", alpha=a)
        elif kind == "battle":
            f.circle(x, y, r * 3.0, color="#C0392B", alpha=0.22 * a, blur=6)
            for sgn in (-1, 1):
                f.line(x - sgn * r * 1.6, y - r * 1.6, x + sgn * r * 1.6, y + r * 1.6, color="#F4E4B0", sw=3.2, alpha=a)
                f.line(x - sgn * r * 1.6, y - r * 1.6, x + sgn * r * 1.6, y + r * 1.6, color="#2A1A0C", sw=1.2, alpha=a)
        elif kind == "siege":
            f.rect(x - r * 1.2, y - r * 0.9, r * 2.4, r * 1.9, color="#E8D8A8", alpha=a)
            for k in (-1, 0, 1):
                f.rect(x + k * r * 0.85 - r * 0.28, y - r * 1.5, r * 0.56, r * 0.7, color="#E8D8A8", alpha=a)
            f.rect(x - r * 1.2, y - r * 0.9, r * 2.4, r * 1.9, style="stroke", sw=1.3, color="#2A1A0C", alpha=a)
        else:
            f.circle(x, y, r * 1.9, color=color, alpha=0.16 * a, blur=5)
            f.circle(x, y, r, color=color, alpha=a)
            f.circle(x, y, r, color="#2A1A0C", style="stroke", sw=1.6, alpha=a)
        if name:
            if name_side == "r":
                f.text(name, x + dx, y + dy + size * 0.3, face="cap_b", size=size, color="#F6ECCB", align="l", alpha=a, shadow=(2, 2, 3, "#000000"))
            elif name_side == "l":
                f.text(name, x - dx, y + dy + size * 0.3, face="cap_b", size=size, color="#F6ECCB", align="r", alpha=a, shadow=(2, 2, 3, "#000000"))
            elif name_side == "t":
                f.text(name, x, y - 20 - size * 0.2, face="cap_b", size=size, color="#F6ECCB", align="c", alpha=a, shadow=(2, 2, 3, "#000000"))
            else:
                f.text(name, x, y + 22 + size * 0.8, face="cap_b", size=size, color="#F6ECCB", align="c", alpha=a, shadow=(2, 2, 3, "#000000"))

    def route(self, f, cam, pts, prog=1.0, color="#F0D27A", width=5.0, dash=None, arrow=True, glow=True, alpha=1.0, dash_phase=0.0, smooth_t=0.5, taper=False):
        """pts: [(lon,lat)...]; prog 0..1 kısmen çizer. Yumuşak eğri + ok başı."""
        if prog <= 0:
            return None
        sp = [cam.ll(*q) for q in pts]
        path = smooth_path(sp, close=False, tension=smooth_t) if len(sp) > 2 else poly_path(sp, close=False)
        pm = skia.PathMeasure(path, False)
        L = pm.getLength()
        part = skia.Path()
        pm.getSegment(0, L * clamp(prog), part, True)
        c = f.c
        if glow:
            c.drawPath(part, f.paint(color, style="stroke", sw=width * 3.2, alpha=0.20 * alpha, blur=width * 1.4))
        p = f.paint(color, style="stroke", sw=width, alpha=alpha)
        if dash:
            p.setPathEffect(skia.DashPathEffect.Make([dash[0], dash[1]], dash_phase))
        c.drawPath(part, f.paint("#2A1A0C", style="stroke", sw=width + 3.0, alpha=0.55 * alpha, cap="round") if not dash else f.paint("#2A1A0C", style="stroke", sw=0, alpha=0))
        c.drawPath(part, p)
        end = None
        if prog > 0.02:
            d = L * clamp(prog)
            pos, tan = pm.getPosTan(max(0.0, d - 0.5))
            if pos is not None and arrow and prog > 0.02:
                ang = math.atan2(tan.y(), tan.x())
                ah = width * 3.4
                tip = (pos.x() + math.cos(ang) * 1.0, pos.y() + math.sin(ang) * 1.0)
                a1 = (tip[0] - ah * math.cos(ang - 0.45), tip[1] - ah * math.sin(ang - 0.45))
                a2 = (tip[0] - ah * math.cos(ang + 0.45), tip[1] - ah * math.sin(ang + 0.45))
                f.poly([tip, a1, a2], color=color, alpha=alpha)
                f.poly([tip, a1, a2], style="stroke", sw=1.6, color="#2A1A0C", alpha=0.8 * alpha)
            end = (pos.x(), pos.y()) if pos is not None else None
        return end

    def point_on(self, cam, pts, prog, smooth_t=0.5):
        sp = [cam.ll(*q) for q in pts]
        path = smooth_path(sp, close=False, tension=smooth_t) if len(sp) > 2 else poly_path(sp, close=False)
        pm = skia.PathMeasure(path, False)
        pos, tan = pm.getPosTan(pm.getLength() * clamp(prog))
        return (pos.x(), pos.y()), math.atan2(tan.y(), tan.x())

    # ---- süs: harita çerçevesi
    def frame(self, f, style="night", alpha=1.0, inset=34):
        col = "#C9962B" if style == "night" else "#5A3E1E"
        a = alpha
        x0, y0, x1, y1 = inset, inset, W - inset, H - inset
        f.rect(x0, y0, x1 - x0, y1 - y0, style="stroke", sw=3, color=col, alpha=0.9 * a)
        f.rect(x0 + 10, y0 + 10, x1 - x0 - 20, y1 - y0 - 20, style="stroke", sw=1.2, color=col, alpha=0.7 * a)
        # kenar çentikleri
        for i in range(0, int((x1 - x0) / 24) + 1):
            x = x0 + i * 24
            L = 8 if i % 5 else 14
            f.line(x, y0, x, y0 + L, color=col, sw=1.2, alpha=0.7 * a)
            f.line(x, y1, x, y1 - L, color=col, sw=1.2, alpha=0.7 * a)
        for i in range(0, int((y1 - y0) / 24) + 1):
            y = y0 + i * 24
            L = 8 if i % 5 else 14
            f.line(x0, y, x0 + L, y, color=col, sw=1.2, alpha=0.7 * a)
            f.line(x1, y, x1 - L, y, color=col, sw=1.2, alpha=0.7 * a)
        for (cx, cy) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
            f.circle(cx, cy, 9, color=col, alpha=0.9 * a)
            f.circle(cx, cy, 4, color="#2A1A0C", alpha=0.9 * a)

    def compass(self, f, x, y, r=70, rot=0.0, alpha=0.9, style="night"):
        col = "#E3B54A" if style == "night" else "#4E3419"
        c = f.c
        c.save(); c.translate(x, y); c.rotate(math.degrees(rot))
        f.circle(0, 0, r * 0.98, style="stroke", sw=1.5, color=col, alpha=0.8 * alpha)
        f.circle(0, 0, r * 0.62, style="stroke", sw=1.0, color=col, alpha=0.6 * alpha)
        for i in range(16):
            a = math.pi * 2 * i / 16
            L = 1.0 if i % 4 == 0 else (0.82 if i % 2 == 0 else 0.7)
            tip = (math.cos(a) * r * L, math.sin(a) * r * L)
            side = r * (0.085 if i % 4 == 0 else 0.055)
            b1 = (math.cos(a + math.pi / 2) * side, math.sin(a + math.pi / 2) * side)
            b2 = (-b1[0], -b1[1])
            f.poly([tip, b1, b2], color=col, alpha=(0.95 if i % 4 == 0 else 0.7) * alpha)
        # kuzey oku
        f.poly([(0, -r * 1.22), (r * 0.12, -r * 0.88), (-r * 0.12, -r * 0.88)], color="#C0392B" if style == "night" else "#8E1F26", alpha=alpha)
        c.restore()
        f.text("K", x, y - r * 1.3 - 8, face="title", size=22, color=col, align="c", alpha=alpha)
