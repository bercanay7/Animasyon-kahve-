"""Bölüm yazarı D (c0, c9, c12, c13) ortak yardımcıları ve genel amaçlı çekim türleri ("wd_" öntekli).

* A(...)            : anlatı çapası; sözcük yoksa (metin yaması bekleyen cümleler) yedek sözcüklere / cümle başına düşer — KeyError vermez.
* icn(...)          : yeni simge henüz kayıtlı değilse yedek simge adı döndürür.
* tag/ kick_rule / shield_path / ingot ...: küçük çizim yardımcıları.
* wd_counter, wd_vs, wd_medal_swap: bölümler arası paylaşılan çekim türleri.
Ortak dosyalara dokunulmaz; her şey bu modülde.
"""
import math

import numpy as np
import skia

import icons
import medal
import shots as SH
import sk
from sk import W, H, C, back_out, clamp, ease_io, ease_out, lerp, mix, seg, smooth

# ───────────────────────────── çapalar ─────────────────────────────
HUD_R = (1500, 0, 420, 110)     # sağ üst HUD (ortak) — içerik koyma


def A(sid, key=None, off=0.0, nth=0, alt=()):
    """('sid', göreli_ofset) biçiminde çapa döndürür (cx.at / shot(a=) ikisi de kabul eder).
    key bulunamazsa alt sözcükleri dener; hiçbiri yoksa cümle başlangıcı + off kullanılır (metin yaması gelene dek güvenli)."""
    tl = SH.timeline()
    if sid not in tl.sent:
        raise KeyError(f"cümle yok: {sid}")
    t0 = tl.sent[sid]["t0"]
    if key is None:
        return (sid, float(off))
    for k in (key,) + tuple(alt):
        try:
            t = tl.word(sid, k, nth=nth)
            return (sid, float(t - t0 + off))
        except KeyError:
            continue
    return (sid, float(off))


def AE(sid, off=0.0):
    """Cümlenin SON anı (bitişi) + off, göreli çapa."""
    tl = SH.timeline()
    s = tl.sent[sid]
    return (sid, float(s["t1"] - s["t0"] + off))


def icn(name, fb="star"):
    """Simge adı kayıtlıysa döndür, değilse yedeği."""
    return name if name in icons._ICONS else fb


def has_scene(name):
    import scenes_lib as SL
    return name in SL.SCENES


# ───────────────────────────── küçük çizimler ─────────────────────────────
def glow_dot(f, x, y, r, color="#FFD58A", a=1.0):
    f.circle(x, y, r, shader=f.rad(x, y, r, [(color, 0.0, int(200 * a)), (color, 0.45, int(70 * a)), (color, 1.0, 0)]), blend=skia.BlendMode.kPlus)


def tag(f, text, x, y, k=1.0, size=30, sub=None, align="l", accent="#C9962B", face="title_m", track=5, color="#F3E2A8", min_w=0, fill_alpha=0.84):
    """Koyu levha + altın şerit + yazı (harita/diorama etiketi). (x,y): sol-üst (l) / sağ-üst (r) / orta-üst (c)."""
    if k <= 0:
        return (x, y, 0, 0)
    tw = sk.text_width(text, face, size, track)
    sw = sk.text_width(sub, "cap_i", size * 0.82) if sub else 0
    w = max(tw, sw, min_w) + 64
    h = size * 1.5 + 22 + (size * 0.92 if sub else 0)
    x0 = x if align == "l" else (x - w if align == "r" else x - w / 2)
    yy = y + (1 - smooth(k)) * 12
    f.rrect(x0 - 5, yy - 5, w + 10, h + 10, 14, color="#000000", alpha=0.32 * k, blur=9)
    f.rrect(x0, yy, w, h, 10, color="#120B06", alpha=fill_alpha * k)
    f.rrect(x0, yy, w, h, 10, style="stroke", sw=1.6, color=accent, alpha=0.7 * k)
    f.rrect(x0, yy, 7, h, 3, color=accent, alpha=0.95 * k)
    f.text(text, x0 + 34, yy + size * 1.12 + 6, face=face, size=size, color=color, align="l", track=track, alpha=k, shadow=(2, 2, 3, "#000000"))
    if sub:
        f.text(sub, x0 + 34, yy + size * 1.12 + 6 + size * 0.95, face="cap_i", size=size * 0.82, color="#C9B27A", align="l", alpha=k)
    return (x0, yy, w, h)


def kick_rule(f, text, x, y, k=1.0, size=28, track=12, color="#D9C48A", face="title_m", span=130):
    """— YAZI — : ince altın çizgilerle çevrili küçük başlık."""
    if k <= 0:
        return
    wd = sk.text_width(text, face, size, track)
    f.text(text, x, y, face=face, size=size, color=color, align="c", track=track, alpha=k, shadow=(2, 2, 3, "#000000"))
    for sgn in (-1, 1):
        x0 = x + sgn * (wd / 2 + 26)
        f.line(x0, y - size * 0.3, x0 + sgn * span * k, y - size * 0.3, color="#C9962B", sw=1.6, alpha=0.75 * k)
        f.circle(x0, y - size * 0.3, 3, color="#C9962B", alpha=k)


def shield_path(cx, cy, w, h):
    p = skia.Path()
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    p.moveTo(x0, y0 + h * 0.04)
    p.cubicTo(x0 + w * 0.2, y0 - h * 0.02, x1 - w * 0.2, y0 - h * 0.02, x1, y0 + h * 0.04)
    p.lineTo(x1, cy + h * 0.06)
    p.cubicTo(x1, cy + h * 0.30, cx + w * 0.30, cy + h * 0.44, cx, y1)
    p.cubicTo(cx - w * 0.30, cy + h * 0.44, x0, cy + h * 0.30, x0, cy + h * 0.06)
    p.close()
    return p


def ingot(f, x, y, w=220, h=104, metal="gold", alpha=1.0, lit=0.0):
    """Altın külçe (yamuk, bevel). (x,y) = alt-orta."""
    top = w * 0.74
    pts = [(x - w / 2, y), (x + w / 2, y), (x + top / 2, y - h), (x - top / 2, y - h)]
    base = {"gold": ("#F4DC8C", "#C9962B", "#7A5518"), "bronze": ("#D9A56A", "#9A6A3A", "#4A2C14"), "crimson": ("#E26A5A", "#8E1F26", "#3A0D12"),
            "silver": ("#F0F4F8", "#A8AFB8", "#4A4F56")}[metal]
    path = sk.poly_path(pts, True)
    f.path(path, shader=f.lin(x, y - h, x, y, [(base[0], 0.0), (base[1], 0.45), (base[2], 1.0)]), alpha=alpha)
    f.path(path, style="stroke", sw=2.4, color=mix(base[2], "#000000", 0.4), alpha=0.9 * alpha)
    f.poly([(x - top / 2 + 6, y - h + 5), (x + top / 2 - 6, y - h + 5), (x + top / 2 - 14, y - h + 22), (x - top / 2 + 14, y - h + 22)], color="#FFF3C8", alpha=0.35 * alpha)
    f.line(x - w * 0.18, y - h * 0.18, x + w * 0.08, y - h * 0.18, color="#FFF3C8", sw=3, alpha=0.25 * alpha)
    if lit > 0:
        glow_dot(f, x, y - h / 2, w * 0.8, "#FFD58A", lit * alpha)


def reveal_text(f, text, x, y, k, face="title", size=60, color="#F0D27A", track=8, align="c", shadow=True, soft=40):
    """Soldan sağa açılan yazı (k 0..1)."""
    if k <= 0:
        return
    wd = sk.text_width(text, face, size, track)
    x0 = x - wd / 2 if align == "c" else (x if align == "l" else x - wd)
    f.c.save()
    f.c.clipRect(skia.Rect.MakeLTRB(x0 - 10, y - size * 1.2, x0 + (wd + 20) * clamp(k), y + size * 0.6))
    f.text(text, x, y, face=face, size=size, color=color, align=align, track=track, shadow=(2, 3, 4, "#000000") if shadow else None)
    f.c.restore()


def ring_pulse(f, x, y, t0, t, r0=20, r1=260, dur=1.4, color="#F0D27A", sw=3, a=0.8):
    k = (t - t0) / dur
    if 0 < k < 1:
        f.circle(x, y, lerp(r0, r1, ease_out(k)), style="stroke", sw=sw * (1 - 0.6 * k), color=color, alpha=a * (1 - k))


def draw_medal_plain(f, key, x, y, size, metal="gold", flip=False, alpha=1.0, t=0.0, i=0, glint=True, shadow=True):
    gl = (t * 0.25 + 0.2 * i) % 2.0
    SH.draw_medal(f, key, x, y, size, metal, flip, alpha=alpha, tilt=0.15 * math.sin(t * 0.5 + i), glint=(gl if (glint and gl < 1) else None), shadow=shadow)


def cameo(f, cx, key, x, y, size, at, metal="bronze", name=None, role=None, flip=False, plate_dy=None, plate_w=None, i=0, dur=0.7):
    """Çekim içine küçük madalya + isteğe bağlı isim levhası yerleştirir; at: çapa. Dönüş: görünürlük 0..1."""
    k = cx.amt(at, dur)
    if k <= 0:
        return 0.0
    sc = 0.9 + 0.1 * ease_out(k)
    draw_medal_plain(f, key, x, y, size * sc, metal, flip, alpha=k, t=cx.t, i=i)
    if name:
        SH.name_plate(f, name, role, None, cx_=x, y=y + (plate_dy if plate_dy is not None else size * 0.52), t=cx.amt(at, 0.6, off=0.35), w=plate_w)
    return k


def vignette_dark(f, a):
    """Çekimi (0..1) siyaha doğru karartır."""
    if a > 0:
        f.rect(0, 0, W, H, color="#000000", alpha=clamp(a))


def smoke_puff(f, x, y, t, n=7, w=90, h=260, color="#2A1D14", alpha=0.35, seed=3):
    sk.smoke(f, x, y, t, w=w, h=h, n=n, seed=seed, color=color, alpha=alpha)


# ───────────────────────────── sayaç (paylaşılan) ─────────────────────────────
@SH.kind("wd_counter")
def k_wd_counter(cx, value=100000, unit="FLORİN", label=None, sub=None, at=0.0, dur=1.8, prefix="", suffix="", size=200, pos=(W / 2, H * 0.5),
                 icon=None, icon_metal="gold", medal_=None, stamps=(), bgk="night", kick=None, kick_at=None, decimals=0, extra=None, bg_icons=(), unit_at=None, label_at=None, sub_at=None,
                 zoom=0.04):
    """Sayan büyük sayı + damgalar + isteğe bağlı madalya/simge.
    medal_=dict(key, metal, size, x, y, at, name, role, flip); stamps=[(metin, x, y, çapa[, boyut[, rot]])]; bg_icons=[dict(icon,x,y,size,at,metal,alpha,rot)]"""
    f = cx.f
    f.bg(bgk)
    f.rays(alpha=0.32)
    sk.dust(f, cx.t, n=50)
    for bi in bg_icons:
        kk = cx.amt(bi.get("at", 0.0), 0.8)
        if kk > 0:
            icons.draw_icon(f, icn(bi["icon"], "coin"), bi["x"], bi["y"], size=bi.get("size", 300), metal=bi.get("metal", "bronze"), alpha=bi.get("alpha", 0.16) * kk, rot=bi.get("rot", 0.0), shadow=False)
    if medal_:
        m = medal_
        kk = cx.amt(m.get("at", 0.0), 0.8)
        if kk > 0:
            sc = (0.92 + 0.08 * ease_out(kk)) * (1.0 + zoom * cx.u)
            draw_medal_plain(f, m["key"], m.get("x", W * 0.28), m.get("y", H * 0.48), m.get("size", 560) * sc, m.get("metal", "gold"), m.get("flip", False), alpha=kk, t=cx.t)
            if m.get("name"):
                SH.name_plate(f, m["name"], m.get("role"), None, cx_=m.get("x", W * 0.28), y=m.get("y", H * 0.48) + m.get("size", 560) * 0.52, t=cx.amt(m.get("at", 0.0) + 0.5, 0.6), w=m.get("plate_w"))
    k = ease_out(clamp((cx.t - cx.at(at)) / dur), 3)
    v = value * k
    s = f"{v:.{decimals}f}".replace(".", ",") if decimals else SH.fmt_int(v)
    a = cx.amt(at, 0.4)
    px, py = pos
    if icon:
        icons.draw_icon(f, icn(icon, "coin"), px, py - size * 0.95, size=size * 0.8, metal=icon_metal, alpha=a, glow=0.3)
    sc = 1.0 + zoom * 0.5 * cx.u
    f.c.save(); f.c.translate(px, py); f.c.scale(sc, sc); f.c.translate(-px, -py)
    SH.gold_flat(f, prefix + s + suffix, px, py + size * 0.3, face="title", size=size, track=6, alpha=a)
    f.c.restore()
    if unit:
        f.text(unit.upper(), px, py + size * 0.3 + 78, face="title_m", size=48, color="#E0C682", align="c", track=14, alpha=cx.amt(unit_at if unit_at is not None else at + 0.3, 0.5))
    if label:
        f.text(label, px, py + size * 0.3 + 142, face="cap_i", size=40, color="#C9B27A", align="c", alpha=cx.amt(label_at if label_at is not None else at + 0.6, 0.6))
    if sub:
        f.text(sub, px, py + size * 0.3 + 192, face="cap", size=28, color="#A89868", align="c", alpha=cx.amt(sub_at if sub_at is not None else at + 0.9, 0.6), track=3)
    if kick:
        SH.kicker(f, kick, W / 2, 150, alpha=cx.amt(kick_at if kick_at is not None else at, 0.7), size=30, track=12, face="title_m", color="#E0C682")
    for st in stamps:
        SH.stamp(f, st[0], st[1], st[2], rot=(st[5] if len(st) > 5 else -0.12), t=cx.amt(st[3], 0.3), size=(st[4] if len(st) > 4 else 64))
    if extra:
        extra(cx)
    f.vig(0.6)


# ───────────────────────────── iki taraflı karşılaştırma ─────────────────────────────
@SH.kind("wd_vs")
def k_wd_vs(cx, left=None, right=None, center=None, size=500, y=H * 0.44, gap=640, title=None, title_at=0.0, stamps=(), bgk="night", ring_at=0.0, extra=None, plate_dy=None):
    """İki yan yana yuva (madalya veya simge). Yuva dict: key|icon, metal, name, role, at, flip, label. center=dict(icon,size,at,sway).
    Yuvalar `ring_at`ten itibaren kesikli halka olarak görünür; içerik `at`te dolar."""
    f = cx.f
    f.bg(bgk)
    f.rays(alpha=0.3)
    sk.dust(f, cx.t, n=50)
    cxm = W / 2
    kr = cx.amt(ring_at, 0.8)
    for si, (slot, sx) in enumerate(((left, cxm - gap / 2), (right, cxm + gap / 2))):
        if not slot:
            continue
        ka = cx.amt(slot.get("at", 0.0), 0.8)
        rr = size * 0.5
        if kr > 0 and ka < 1:
            f.circle(sx, y, rr * (0.9 + 0.1 * kr), style="stroke", sw=3, color="#C9962B", alpha=0.6 * kr * (1 - ka))
            f.circle(sx, y, rr * (0.9 + 0.1 * kr) - 16, style="stroke", sw=1.2, color="#C9962B", alpha=0.3 * kr * (1 - ka))
        if ka > 0:
            sc = (0.92 + 0.08 * ease_out(ka)) * (1.0 + 0.03 * cx.u)
            if slot.get("key"):
                draw_medal_plain(f, slot["key"], sx, y, size * sc, slot.get("metal", "gold"), slot.get("flip", False), alpha=ka, t=cx.t, i=si)
            elif slot.get("icon"):
                glow_dot(f, sx, y, size * 0.7, "#E3B54A", 0.35 * ka)
                icons.draw_icon(f, icn(slot["icon"], "star"), sx, y, size=size * 0.78 * sc, metal=slot.get("metal", "gold"), alpha=ka, glow=0.3)
            if slot.get("name"):
                SH.name_plate(f, slot["name"], slot.get("role"), None, cx_=sx, y=y + (plate_dy if plate_dy is not None else size * 0.54), t=cx.amt(slot.get("at", 0.0) + 0.35, 0.6), w=min(gap - 40, 560))
    if center:
        kc = cx.amt(center.get("at", 0.0), 0.6)
        if kc > 0:
            sz = center.get("size", 150)
            ang = (math.sin(cx.t * 1.1) * 0.10) if center.get("sway") else 0.0
            icons.draw_icon(f, icn(center["icon"], "swords"), cxm, y + center.get("dy", 0), size=sz * (0.8 + 0.2 * back_out(kc)), metal=center.get("metal", "silver"), alpha=kc, rot=ang, glow=0.2)
    if title:
        SH.kicker(f, title, W / 2, 150, alpha=cx.amt(title_at, 0.7), size=30, track=12, face="title_m", color="#E0C682")
    for st in stamps:
        SH.stamp(f, st[0], st[1], st[2], rot=(st[5] if len(st) > 5 else -0.1), t=cx.amt(st[3], 0.3), size=(st[4] if len(st) > 4 else 64))
    if extra:
        extra(cx)
    f.vig(0.58)


# ───────────────────────────── madalya + metal değişimi / kararma ─────────────────────────────
@SH.kind("wd_medal_swap")
def k_wd_medal_swap(cx, key="karl_yasli", metal_a="bronze", metal_b="onyx", swap_at=1.0, swap_dur=0.9, name=None, role=None, pos="c", size=640, at=0.0, plate_at=0.6,
                    dark_at=None, dark_dur=1.4, dark_to=0.85, stamps=(), bgk="night", extra=None, y=None, glow_end=True, fade_out=0.0):
    """Madalya yavaşça `metal_a`dan `metal_b`ya geçer (ölüm/yas); isteğe bağlı karartma."""
    f = cx.f
    f.bg(bgk)
    xc = {"c": W / 2, "l": W * 0.34, "r": W * 0.66}[pos]
    yc = y if y is not None else (H * 0.46 if name else H * 0.5)
    ks = cx.amt(swap_at, swap_dur)
    f.rays(alpha=(0.35 + 0.1 * math.sin(cx.t * 0.7)) * (1 - 0.7 * ks))
    a = cx.amt(at, 0.8)
    sc = (1.0 + 0.05 * cx.u) * (0.94 + 0.06 * ease_out(a))
    if ks < 1:
        draw_medal_plain(f, key, xc, yc, size * sc, metal_a, False, alpha=a * (1 - ks), t=cx.t)
    if ks > 0:
        draw_medal_plain(f, key, xc, yc, size * sc, metal_b, False, alpha=a * ks, t=cx.t, glint=False)
    sk.dust(f, cx.t, n=50, alpha=0.4 * (1 - 0.6 * ks))
    if name:
        if pos == "c":
            SH.name_plate(f, name, role, None, cx_=W / 2, y=H * 0.80, t=cx.amt(plate_at, 0.6))
        else:
            SH.name_plate(f, name, role, None, cx_=(W * 0.78 if pos == "l" else W * 0.22), y=H * 0.44, t=cx.amt(plate_at, 0.6), w=560)
    for st in stamps:
        SH.stamp(f, st[0], st[1], st[2], rot=(st[5] if len(st) > 5 else -0.1), t=cx.amt(st[3], 0.3), size=(st[4] if len(st) > 4 else 64))
    if extra:
        extra(cx)
    f.vig(0.55 + 0.25 * ks)
    if dark_at is not None:
        vignette_dark(f, dark_to * cx.amt(dark_at, dark_dur))
    if fade_out > 0:
        vignette_dark(f, smooth((cx.t - (cx.dur - fade_out)) / fade_out))


# ───────────────────────────── altın küre (procedural) ─────────────────────────────
def draw_globe(f, x, y, r, rot=0.0, alpha=1.0, glow=0.0, tilt_deg=-20.0, ring=True):
    """Altın küre: meridyen/paralel kazıma çizgileri; rot (rad) döner. alpha 0..1."""
    a255 = int(255 * clamp(alpha))
    if a255 <= 0:
        return
    if glow > 0:
        glow_dot(f, x, y, r * 1.9, "#FFD58A", glow * alpha)
    f.circle(x + r * 0.06, y + r * 0.10, r * 1.02, color="#000000", alpha=0.35 * alpha, blur=r * 0.09)
    sh = skia.GradientShader.MakeRadial((x - r * 0.38, y - r * 0.42), r * 1.55, [C("#FFF0B8", a255), C("#E0B04A", a255), C("#9A6B1A", a255), C("#4A3210", a255)], [0.0, 0.42, 0.78, 1.0])
    f.circle(x, y, r, shader=sh)
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(tilt_deg)
    clip = skia.Path(); clip.addCircle(0, 0, r)
    f.c.clipPath(clip, skia.ClipOp.kIntersect, True)
    ink = "#4A3210"
    for i in range(8):                        # meridyenler (yalnız ön yarı)
        lam = rot + i * math.pi / 8 * 2
        pts, run = [], []
        for k in range(-18, 19):
            ph = math.radians(k * 5)
            xx = r * math.cos(ph) * math.sin(lam)
            zz = math.cos(ph) * math.cos(lam)
            yy = -r * math.sin(ph)
            if zz > 0:
                run.append((xx, yy))
            else:
                if len(run) > 1:
                    pts.append(run)
                run = []
        if len(run) > 1:
            pts.append(run)
        for seg_ in pts:
            f.path(sk.poly_path(seg_, False), style="stroke", sw=max(1.4, r * 0.012), color=ink, alpha=0.55 * alpha)
    for ph_d in (-60, -30, 0, 30, 60):        # paraleller
        ph = math.radians(ph_d)
        wx = r * math.cos(ph)
        yy = -r * math.sin(ph)
        f.line(-wx, yy, wx, yy, color=ink, sw=max(1.6, r * (0.02 if ph_d == 0 else 0.011)), alpha=(0.7 if ph_d == 0 else 0.5) * alpha)
    f.circle(-r * 0.3, -r * 0.35, r * 0.5, shader=f.rad(-r * 0.3, -r * 0.35, r * 0.5, [("#FFFFFF", 0.0, int(80 * alpha)), ("#FFFFFF", 1.0, 0)]))
    f.c.restore()
    f.circle(x, y, r, style="stroke", sw=max(2.0, r * 0.03), color="#6B4A12", alpha=0.9 * alpha)
    if ring:                                  # meridyen halkası + ayak
        f.c.save(); f.c.translate(x, y); f.c.rotate(tilt_deg)
        f.oval(0, 0, r * 1.12, r * 1.12, style="stroke", sw=max(3.0, r * 0.045), color="#C9962B", alpha=0.95 * alpha)
        f.oval(0, 0, r * 1.12, r * 1.12, style="stroke", sw=max(1.0, r * 0.012), color="#FFF0B8", alpha=0.6 * alpha)
        f.c.restore()
