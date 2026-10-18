"""cilt_kinds4 — Medici cildi çekim türleri, dördüncü grup: frieze (Gozzoli tarzı alay frizi), skyline (Floransa silueti).
`cilt_kinds` sonunda içe aktarılır."""
import functools
import math

import numpy as np
import skia

import cilt_figs as FG
import cilt_medici as CM
import cilt_orn as ORN
import cilt_scene as SC
import sk
from sk import C, Frame, H, W, clamp, ease_io, ease_out, lerp, mix, smooth
from cilt_medici import PIG, TH, ckind

BAND_H = 680
BAND_Y = 172


@functools.lru_cache(maxsize=6)
def _cast(seed, travel):
    return SC.make_cast(seed, travel)


@ckind("frieze")
def k_frieze(cx, seed=1, speed=34.0, x0=0.0, kick=None, caption=None, at=0.0, **_):
    """Boyalı alay frizi (Magi Alayı tarzı): duvarda yatay bir fresk bandı; kamera bant boyunca yavaşça kayar (hafif paralaks: gökyüzü/tepe/ön plan/figürler).
    Figürler: atlılar (brokar kapariş), yaya soylular/uşaklar; manzara: tepeler, selvi, portakal, şato, çiçekli çayır; boya kaybı + çatlak ağı.
    seed: farklı alay/manzara; speed: px/sn; x0: başlangıç kayması."""
    f = cx.f
    night = not TH.day
    cam = CM.Cam(cx, push=0.02, drift=(0.0, 2.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    travel = int(speed * 20 + 120)
    mode = "night" if night else "day"
    sky = SC.sky_layer(W + int(0.45 * travel) + 40, BAND_H, seed, mode)
    mid = SC.mid_layer(W + int(0.85 * travel) + 40, BAND_H, seed + 1, mode)
    cast = _cast(seed, travel)
    scroll = x0 + speed * clamp(cx.t, 0, cx.dur + 4)
    a = cx.amt(at, 0.8)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, BAND_Y, W, BAND_Y + BAND_H))
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(a)
    c.drawImage(sky, -scroll * 0.45, BAND_Y, CM._LIN, p)
    c.drawImage(mid, -scroll * 0.85, BAND_Y, CM._LIN, p)
    rowspd = {0: 0.88, 1: 0.94, 2: 1.0}
    for d in cast:
        sx = d["x"] - scroll * rowspd[d["depth"]]
        if sx < -420 or sx > W + 420:
            continue
        key = FG.rider_sprite if d["kind"] == "rider" else FG.walker_sprite
        img, ox, oy = key(int(d["h"]), d["spec"])
        bob = (math.sin(cx.t * 2.3 + d["phase"]) * 2.4) if d["kind"] == "rider" else abs(math.sin(cx.t * 3.1 + d["phase"])) * -3.2
        sway = math.sin(cx.t * 1.1 + d["phase"]) * 0.004
        c.save()
        c.translate(sx, BAND_Y + d["y"] + bob)
        c.rotate(math.degrees(sway))
        pp = skia.Paint(AntiAlias=True)
        pp.setAlphaf(a)
        c.drawImage(img, -ox, -oy, CM._LIN, pp)
        c.restore()
    c.restore()
    # bant çerçevesi (üst/alt): asma + altın filet
    for yy in (BAND_Y - 40, BAND_Y + BAND_H):
        ORN.band_vine(f, -40, yy, W + 40, 40, alpha=a)
        c.drawLine(-40, yy + (40 if yy < BAND_Y else 0), W + 40, yy + (40 if yy < BAND_Y else 0), f.paint(TH.gold, style="stroke", sw=2.6, alpha=0.9 * a))
    if kick:
        CM.kick(f, kick, W / 2, 104, alpha=cx.amt(at + 0.4, 0.8), size=34, track=14)
    if caption:
        wd = sk.text_width(caption, "cap_i", 40) + 90
        CM.tablet(f, 90, BAND_Y + BAND_H + 54 - 4, wd, 66, alpha=cx.amt(at + 0.8, 0.7), corner=8)
        CM.ink(f, caption, 90 + wd / 2, BAND_Y + BAND_H + 54 + 44, face="cap_i", size=40, color=TH.fg, align="c", alpha=cx.amt(at + 0.8, 0.7), emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=30)


# ───────────────────────────── skyline: Floransa silueti ─────────────────────────────
import cilt_city as CT

SKY_Y = 168                      # bant üstü (dekor asma bandı 128–168)
LABEL_DEF = {                    # anıt etiketi: (dx, dy) plaka merkezi, çapaya göre
    "duomo": (0, -118), "campanile": (215, -96), "pv": (-235, -34), "ponte": (0, 262), "bapt": (0, -112), "santacroce": (-110, -96),
}
LABEL_NAMES = {"duomo": "DUOMO", "campanile": "CAMPANILE", "pv": "PALAZZO VECCHIO", "ponte": "PONTE VECCHIO", "bapt": "VAFTİZHANE", "santacroce": "SANTA CROCE"}


def _pennant(f, x, y, t, a=1.0, L=40.0, hgt=15.0, color="#B3301F"):
    """Palazzo Vecchio kulesi bayrağı: sallanan kırlangıç kuyruklu flama."""
    c = f.c
    top = [(x, y)]
    bot = [(x, y + hgt)]
    n = 9
    for k in range(1, n + 1):
        u = k / n
        w = math.sin(t * 4.6 - u * 3.4) * 4.5 * u
        top.append((x + u * L, y + w))
        bot.append((x + u * L, y + hgt * (1 - 0.0 * u) + w * 1.1))
    pts = top + [(x + L * 0.80, y + hgt * 0.5 + math.sin(t * 4.6 - 3.0) * 3)] + bot[::-1]
    path = sk.poly_path(pts)
    pp = skia.Paint(AntiAlias=True, Color=C(color, int(255 * a)))
    c.drawPath(path, pp)
    c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#2A1A0C", int(200 * a))))
    c.drawCircle(x + L * 0.20, y + hgt * 0.5 + math.sin(t * 4.6 - 0.7) * 1.0, 2.6, skia.Paint(AntiAlias=True, Color=C("#F2E6C2", int(235 * a))))


def _birds(f, t, n, a, night):
    if night:
        return
    c = f.c
    for i in range(n):
        sp = 22 + (i * 7) % 17
        bx = (i * 331 + t * sp) % (W + 360) - 180
        by = SKY_Y + 90 + (i % 4) * 46 + math.sin(t * 0.7 + i * 1.9) * 16
        fl = math.sin(t * 10.0 + i * 2.3) * 5.5
        s = 0.8 + (i % 3) * 0.22
        pth = skia.Path()
        pth.moveTo(bx - 9 * s, by + fl * s * 0.4)
        pth.quadTo(bx - 4 * s, by - 4 * s - fl * s, bx, by)
        pth.quadTo(bx + 4 * s, by - 4 * s - fl * s, bx + 9 * s, by + fl * s * 0.4)
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0 * s, Color=C("#2A1A0C", int(190 * a)), StrokeCap=skia.Paint.kRound_Cap))


def _river_glints(f, t, a, night, y0, y1):
    c = f.c
    col = "#FFF4D0" if night else "#FFFFFF"
    for i in range(40):
        yy = y0 + ((i * 37) % 100) / 100.0 * (y1 - y0)
        k = (yy - y0) / max(1.0, (y1 - y0))
        L = 16 + 46 * k
        xx = ((i * 211 + t * (7 + 14 * k)) % (W + 120)) - 60
        al = (0.20 + 0.22 * math.sin(t * 1.7 + i * 1.3) ** 2) * a * (0.55 if night else 1.0)
        c.drawLine(xx, yy, xx + L, yy, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4 + 1.3 * k, Color=C(col, int(255 * al)), StrokeCap=skia.Paint.kRound_Cap))


@ckind("skyline")
def k_skyline(cx, seed=1, tod=None, pan=340.0, x0=0.0, dir=1, kick=None, caption=None, labels=None, at=0.0, birds=7, **_):
    """Floransa silueti (fresk panorama): Duomo kubbesi + Giotto çan kulesi + Palazzo Vecchio + Vaftizhane + Santa Croce + Arno üstünde Ponte Vecchio; kamera yatay kayar (4 katman paralaks),
    sallanan bayrak, kuşlar (gündüz), nehir parıltısı, gece pencere ışığı titremesi.
    tod: 'day'|'dusk'|'night' (yoksa moda göre); pan: toplam kayma px (0–520); x0: başlangıç; dir: ±1; kick: üst başlık; caption: nehir üstünde kartuş yazı;
    labels: [dict(on='duomo'|'campanile'|'pv'|'ponte'|'bapt'|'santacroce', name=..., at=sn, dx=, dy=)]."""
    f = cx.f
    night = not TH.day
    tod = tod or ("night" if night else "day")
    cam = CM.Cam(cx, push=0.03, drift=(0.0, 1.6))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    PH = CT.PH
    L = CT.city_layers(PH, seed, tod)
    u = clamp(cx.t / max(1e-6, cx.dur), 0.0, 1.0)
    scroll = clamp(x0 + dir * pan * u, 0.0, float(CT.PW_EXTRA))
    a = cx.amt(at, 1.0)
    SP = CT.SPEEDS
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, SKY_Y, W, SKY_Y + PH))
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(a)
    for key in ("sky", "hills", "far", "near"):
        c.drawImage(L[key], -scroll * SP[key], SKY_Y, CM._LIN, p)
        if key == "far":
            fx, fy = L["flag"]
            _pennant(f, fx - scroll * SP["far"] + 1.0, SKY_Y + fy + 3, cx.t, a)
            if tod != "day":                                    # pencere titremesi (mum)
                for k, (wx, wy, ww, wh) in enumerate(L["lit_far"][:18]):
                    fl = clamp(0.5 + 0.9 * math.sin(cx.t * (2.4 + 0.37 * k) + k * 2.1) * math.sin(cx.t * 0.9 + k), 0.0, 1.0)
                    if fl < 0.98:
                        c.drawRect(skia.Rect.MakeXYWH(wx - scroll * SP["far"], SKY_Y + wy, ww, wh), skia.Paint(Color=C("#2A2234", int(190 * (1 - fl) * a))))
    # yakın katman pencereleri titremesi
    if tod != "day":
        for k, (wx, wy, ww, wh) in enumerate(L["lit_near"][:22]):
            fl = clamp(0.5 + 0.9 * math.sin(cx.t * (1.9 + 0.31 * k) + k * 1.3) * math.sin(cx.t * 0.7 + k * 0.6), 0.0, 1.0)
            if fl < 0.98:
                c.drawRect(skia.Rect.MakeXYWH(wx - scroll * SP["near"], SKY_Y + wy, ww, wh), skia.Paint(Color=C("#2A2234", int(200 * (1 - fl) * a))))
    _river_glints(f, cx.t, a, night or tod == "night", SKY_Y + PH * 0.80 + 14, SKY_Y + PH - 14)
    _birds(f, cx.t, birds, a, night or tod == "night")
    c.restore()
    # bant çerçevesi
    for yy in (SKY_Y - 40, SKY_Y + PH):
        ORN.band_vine(f, -40, yy, W + 40, 40, alpha=a)
        c.drawLine(-40, yy + (40 if yy < SKY_Y else 0), W + 40, yy + (40 if yy < SKY_Y else 0), f.paint(TH.gold, style="stroke", sw=2.6, alpha=0.9 * a))
    A = CT.anchors(PH)
    for lb in (labels or []):
        on = lb.get("on", "duomo")
        layer, lx, ly = A[on]
        ax = lx - scroll * SP[layer]
        ay = SKY_Y + ly
        dx, dy = lb.get("dx"), lb.get("dy")
        ddx, ddy = LABEL_DEF.get(on, (0, -100))
        dx = ddx if dx is None else dx
        dy = ddy if dy is None else dy
        k = cx.amt(lb.get("at", 1.0), 0.7)
        if k <= 0.001:
            continue
        name = lb.get("name") or LABEL_NAMES.get(on, on.upper())
        size = lb.get("size", 34)
        wd = sk.text_width(name, "cap_b", size) + 60
        px_, py_ = clamp(ax + dx, 90 + wd / 2, W - 90 - wd / 2), ay + dy
        # kılavuz çizgi
        ex = px_
        ey = py_ + (30 if dy < 0 else -30)
        c.drawLine(ax, ay, ex, ey, f.paint(TH.fg, style="stroke", sw=2.0, alpha=0.75 * k))
        c.drawCircle(ax, ay, 5.5, f.paint(TH.acc, alpha=k))
        c.drawCircle(ax, ay, 5.5, f.paint(TH.fg, style="stroke", sw=1.2, alpha=0.8 * k))
        CM.tablet(f, px_ - wd / 2, py_ - 32 + (1 - k) * 8, wd, 64, alpha=k, corner=8)
        CM.ink(f, name, px_, py_ + 12 + (1 - k) * 8, face="cap_b", size=size, color=TH.fg, align="c", alpha=k, emboss=False)
    if kick:
        CM.kick(f, kick, W / 2, 104, alpha=cx.amt(at + 0.4, 0.8), size=34, track=14)
    if caption:
        wd = sk.text_width(caption, "cap_i", 44) + 100
        cyy = SKY_Y + PH - 92
        CM.tablet(f, W / 2 - wd / 2, cyy - 36, wd, 76, alpha=cx.amt(at + 0.8, 0.7), corner=10)
        CM.ink(f, caption, W / 2, cyy + 14, face="cap_i", size=44, color=TH.fg, align="c", alpha=cx.amt(at + 0.8, 0.7), emboss=False)
    cam.end(f)
    if night:
        CM.finish(f, cx, motes_n=22, light=CM.candle_light(cx.t, seed, base=(W * 0.5, H * 0.46), r=1500.0, sway=12.0))
    else:
        CM.finish(f, cx, motes_n=26)


# ───────────────────────────── dünya ve figür animasyonu (hareketli figür kiti, pano, yapım, alay) ─────────────────────────────
import cilt_anim, cilt_pano, cilt_build  # noqa: E402,F401
