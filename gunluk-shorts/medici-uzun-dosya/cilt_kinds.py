"""cilt_kinds — Medici cildi çekim türleri (@ckind). `shots.py` sonunda içe aktarılır; eski türlerin ÜZERİNE yazar, yeni türleri ekler.

Ortak parametreler (her tür): mode='day'|'night', perde=1|2|3 (yoksa bölümden), seed=int (duvar varyantı).
Türler: title, fresco_title, chapter_card, quote, counter, emblem, palle, coin, black, (devam: ledger, letter, doc, medal, medals, map, timeline, tree,
bars, stacked, iconrow, network, frieze, skyline …) — bkz. STIL_REHBERI.md.
"""
import math

import numpy as np
import skia

import cilt_fx as FX
import cilt_medici as CM
import cilt_orn as ORN
import cilt_props as CP
import icons
import sk
from sk import C, Frame, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, seg, smooth
from cilt_medici import PIG, TH, ckind

CREAM = "#F4E9CB"
GOLD_T = "#EBC76E"


# ───────────────────────────── yardımcılar ─────────────────────────────
def wrap_lines(text, face, size, max_w, track=0.0, max_lines=3):
    """Kelime sarma; çok uzunsa en çok max_lines satır."""
    lines = sk.wrap_text(text, face, size, max_w, track)
    return lines[:max_lines] if len(lines) > max_lines else lines


def _title_style(style=None):
    return style or ("engraved" if TH.day else "gilt")


def title_spr(text, size, track, style=None, color=None):
    st = _title_style(style)
    if st == "gilt":
        return CM.gilt(text, "title", int(size), float(track))
    if st == "painted":
        return CM.painted(text, "title", int(size), float(track), color or TH.acc)
    return CM.engraved(text, "title", int(size), float(track), color or TH.fg)


# ───────────────────────────── title ─────────────────────────────
@ckind("title")
def k_title(cx, text="MEDİCİ", sub=None, kick=None, at=0.0, size=170, style=None, color=None, face="title", sub_at=None, kick_at=None, y=0.50,
            seed=0, rule=True, glow=True, **_):
    """Büyük başlık kartı (tarih/yıl kartları, bölüm içi başlıklar). gündüz: oyma mürekkep; gece: yaldız."""
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed)
    cam.begin(f)
    k = cx.amt(at, 1.1)
    size = CM.fit_size(text, "title", size, 1560, size * 0.14)
    sp = title_spr(text, size, size * 0.14, style, color)
    yb = H * y + size * 0.34
    glint = ((cx.t - cx.at(at) - 0.6) * 0.30) % 2.2 if cx.t > cx.at(at) + 0.6 else None
    if glint is not None and glint > 1:
        glint = None
    CM.draw_spr(f, sp, W / 2, yb, "c", alpha=k, reveal=clamp(k * 1.15), glow=0.35 * k if (glow and not TH.day) else 0.0, shadow=0.5 if not TH.day else 0.0,
                glint=glint if _title_style(style) == "gilt" else None)
    if kick:
        a = cx.amt(kick_at if kick_at is not None else at + 0.3, 0.8)
        CM.kick(f, kick, W / 2, yb - size * 0.95, alpha=a, size=34, track=14)
    if rule:
        CM.flourish_rule(f, W / 2, yb + size * 0.20, min(900, sp.wid * 0.9), alpha=cx.amt(at + 0.7, 0.8), grow=cx.amt(at + 0.7, 1.0))
    if sub:
        a = cx.amt(sub_at if sub_at is not None else at + 0.9, 0.9)
        sz = CM.fit_size(sub, "cap_i", 60, 1500)
        CM.ink(f, sub, W / 2, yb + size * 0.20 + 82, face="cap_i", size=sz, color=TH.fg2, align="c", alpha=a)
    cam.end(f)
    CM.finish(f, cx)


# ───────────────────────────── fresco_title ─────────────────────────────
_PANEL = {}


def panel_image(w, h, b, tone, mode, perde, seed):
    key = (w, h, b, tone, mode, perde, seed)
    if key not in _PANEL:
        fr = Frame(w + 2 * b, h + 2 * b)
        fr.clear(skia.ColorTRANSPARENT)
        fr.c.drawImage(ORN.lapis_field(w, h, seed, True, 0.5, tone), b, b)
        ORN.frame_panel(fr, b, b, w, h, band=b, kind="lozenge")
        _PANEL[key] = fr.surf.makeImageSnapshot()
    return _PANEL[key]


@ckind("fresco_title")
def k_fresco_title(cx, text="MEDİCİ", sub="BANKA ÖLDÜ, GÜZELLİK KALDI", kick="ZAMAN KURYESİ", at=2.6, panel_at=0.3, tone="lapis", arms=True,
                   seed=1, sub_face="cap_i", size=216, **_):
    """Ana başlık: duvarda giornata giornata açılan lapis fresk levhası + altın yıldızlar + yaldız harfli başlık + palle arması.
    Zaman: panel_at'ten itibaren ~3 sn'de yamalar açılır; at'te başlık yaldızı belirir."""
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed, cam=CM.Cam(cx, push=0.05, drift=(6.0, 2.5)))
    cam.begin(f)
    c = f.c
    pw, ph, b = 1480, 740, 36
    px, py = (W - pw) / 2 - b, 118 - b + 6
    img = panel_image(pw, ph, b, tone, TH.mode, TH.perde, seed)
    paths, order = FX.giornata_paths(seed + 20, pw + 2 * b, ph + 2 * b)
    kk = clamp((cx.t - cx.at(panel_at)) / 3.4)
    c.save(); c.translate(px, py)

    def dr(al):
        p = skia.Paint(AntiAlias=True)
        p.setAlphaf(clamp(al))
        c.drawImage(img, 0, 0, CM._LIN, p)
    FX.giornata_reveal(c, paths, order, kk, dr, span=0.74, soft=0.28)
    c.restore()
    # içerik
    gcol = "#E9C770"
    ka = cx.amt(at - 1.2, 0.9)
    CM.ink(f, kick, W / 2, 196, face="title_m", size=32, color=gcol, align="c", track=16, alpha=ka)
    if arms:
        aa = cx.amt(at - 1.6, 1.0)
        yy = 358 - (1 - aa) * 14
        CP.draw_arms(f, W / 2, yy, 228 * (0.94 + 0.06 * aa), alpha=aa, shadow=0.6, glow=0.20 * aa, glint=((cx.t * 0.16) % 2.2) if (cx.t * 0.16) % 2.2 < 1 else None)
    size = CM.fit_size(text, "title", size, 1320, size * 0.12)
    sp = CM.gilt(text, "title", int(size), float(size * 0.12))
    ta = cx.amt(at, 1.3)
    gl = ((cx.t - cx.at(at) - 1.2) * 0.26) % 2.4 if cx.t > cx.at(at) + 1.2 else None
    if gl is not None and gl > 1:
        gl = None
    CM.draw_spr(f, sp, W / 2, 646, "c", alpha=ta, reveal=clamp(ta * 1.2), glow=0.30 * ta, shadow=0.6, glint=gl)
    CM.flourish_rule(f, W / 2, 696, 820, alpha=cx.amt(at + 0.9, 0.8), color=gcol, grow=cx.amt(at + 0.9, 1.1))
    if sub:
        sa = cx.amt(at + 1.3, 1.0)
        szs = CM.fit_size(sub, sub_face, 56, 1240)
        CM.ink(f, sub, W / 2, 772, face=sub_face, size=szs, color=CREAM, align="c", alpha=sa, track=0)
    cam.end(f)
    CM.finish(f, cx, motes_n=40, light=CM.candle_light(cx.t, 1, base=(W * 0.5, H * 0.47), r=900))


# ───────────────────────────── chapter_card ─────────────────────────────
def _slab(f, x, y, w, h, alpha=1.0, seed=2):
    """Sıva levha: kenarı hafif kırık-düzensiz, bevel, iç gölge, sıva tanesi."""
    c = f.c
    rs = np.random.RandomState(seed)
    pts = []
    n = 60
    for i in range(n):
        pts.append((x + w * i / n, y + rs.randn() * 1.6))
    for i in range(n // 2):
        pts.append((x + w + rs.randn() * 1.6, y + h * i / (n // 2)))
    for i in range(n):
        pts.append((x + w - w * i / n, y + h + rs.randn() * 1.6))
    for i in range(n // 2):
        pts.append((x + rs.randn() * 1.6, y + h - h * i / (n // 2)))
    path = sk.smooth_path(pts, True, 0.25)
    c.drawPath(path, f.paint("#000000", alpha=0.55 * alpha, blur=16))
    c.save(); c.translate(0, 0)
    sh = skia.GradientShader.MakeLinear([(x, y), (x + w * 0.7, y + h)], [C("#F1E8D0"), C("#DCD0B0")], [0, 1])
    c.drawPath(path, skia.Paint(AntiAlias=True, Shader=sh, Alpha=int(255 * alpha)))
    c.restore()
    c.save()
    c.clipPath(path, skia.ClipOp.kIntersect, True)
    # bevel: üst-sol açık, alt-sağ koyu
    c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=14, Color=C("#FFFFFF", int(120 * alpha)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 5)))
    c.save(); c.translate(7, 8)
    c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=16, Color=C("#6A5230", int(150 * alpha)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 7)))
    c.restore()
    c.restore()


@ckind("chapter_card")
def k_chapter_card(cx, n="I", title="", years="", perde_label=None, seed=0, **_):
    """Bölüm kartı (3 sn): koyu duvarda sıva levha; oyma Cinzel başlık + roma rakamı + palle arması. perde_label: 'PERDE II — GÜZELLİK' (yeni perdede)."""
    f = cx.f
    CM.use("night", cx.perde if hasattr(cx, "perde") and cx.perde else 2)
    cx.f.cilt_mode = "night"
    cam = CM.bgfill(f, cx, seed=seed + 1, cam=CM.Cam(cx, push=0.03, drift=(5.0, 2.0)))
    cam.begin(f)
    a = cx.fade(0.30, 0.35)
    sx, sy, sw, sh = 190, 168, 1540, 720
    # sıva levha içeriği ışık altında olsun → gündüz teması ile çiz
    CM.use("day", TH.perde)
    slide = (1 - smooth(cx.t / 0.55)) * 24
    _slab(f, sx, sy + slide * 0.0, sw, sh, alpha=a)
    ORN.hairline_frame(f, sx + 34, sy + 34, sw - 68, sh - 68, alpha=0.9 * a, color="#8A6A36", gap=9)
    # sol: arma
    ak = cx.amt(0.15, 0.7)
    CP.draw_arms(f, sx + 310, sy + sh / 2 + 6, 330 * (0.95 + 0.05 * ak), alpha=a * ak, shadow=0.45, glow=0.0, glint=((cx.t * 0.55) % 2.0) if (cx.t * 0.55) % 2.0 < 1 else None)
    # sağ: BÖLÜM + rakam + başlık + yıllar
    xr = sx + 310 + 330 / 2 + 150
    xc = (xr + sx + sw - 60) / 2
    CM.ink(f, "BÖLÜM", xc, sy + 150, face="title_m", size=34, color=TH.fg2, align="c", track=16, alpha=a * cx.amt(0.2, 0.5))
    if perde_label:
        CM.ink(f, perde_label, xc, sy + 112, face="title_m", size=28, color=TH.acc, align="c", track=10, alpha=a * cx.amt(0.1, 0.5))
    nsp = CM.painted(str(n), "title", 190, 12.0, TH.acc, 1.2, 5)
    kn = cx.amt(0.35, 0.55)
    CM.draw_spr(f, nsp, xc, sy + 330, "c", alpha=a * kn, reveal=clamp(kn * 1.2))
    CM.flourish_rule(f, xc, sy + 372, 560, alpha=a * cx.amt(0.8, 0.6), grow=cx.amt(0.8, 0.8))
    tt = sk.tr_upper(title)
    size = 62
    lines = wrap_lines(tt, "title", size, sw - (xr - sx) - 150, 5.0, 3)
    while len(lines) > 2 and size > 46:
        size -= 4
        lines = wrap_lines(tt, "title", size, sw - (xr - sx) - 150, 5.0, 3)
    y0 = sy + 460 - (len(lines) - 1) * size * 0.5
    for i, ln in enumerate(lines):
        sp = CM.engraved(ln, "title", int(size), 5.0, TH.fg, 1.0)
        kt = cx.amt(0.9 + 0.15 * i, 0.8)
        CM.draw_spr(f, sp, xc, y0 + i * size * 1.28, "c", alpha=a * kt, reveal=clamp(kt * 1.2))
    if years:
        CM.ink(f, years, xc, sy + sh - 120, face="cap_i", size=44, color=TH.fg2, align="c", alpha=a * cx.amt(1.5, 0.7))
    cam.end(f)
    CM.use("night", TH.perde)
    CM.finish(f, cx, motes_n=26, light=CM.candle_light(cx.t, 2, base=(W * 0.5, H * 0.5), r=1150))


# ───────────────────────────── quote ─────────────────────────────
@ckind("quote")
def k_quote(cx, text="", who=None, src=None, at=0.0, size=64, stampt=None, face="cap_i", wrap=1380, y0=None, mark=True, seed=0, **_):
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed)
    cam.begin(f)
    lines = sk.wrap_text(text, face, size, wrap)
    a = cx.amt(at, 0.9)
    lh = size * 1.30
    total = len(lines) * lh
    y = (y0 if y0 is not None else H * 0.47 - total / 2 + size * 0.7)
    ORN.hairline_frame(f, 150, 120, W - 300, 740, alpha=0.9 * a, gap=10)
    if mark:
        CM.draw_spr(f, CM.painted("“", "title", 230, 0.0, TH.acc if TH.day else "#D9A95A", 1.3, 9), W / 2 - wrap / 2 - 60, y + 40, "l", alpha=0.85 * a)
    for i, ln in enumerate(lines):
        ai = cx.amt(at + 0.16 * i, 0.75)
        CM.ink(f, ln, W / 2, y + i * lh, face=face, size=size, color=TH.fg, align="c", alpha=ai)
    yy = y + len(lines) * lh + 10
    if who:
        CM.flourish_rule(f, W / 2, yy + 8, 360, alpha=cx.amt(at + 0.5 + 0.16 * len(lines), 0.6), grow=cx.amt(at + 0.5 + 0.16 * len(lines), 0.7))
        CM.ink(f, who, W / 2, yy + 66, face="title_m", size=34, color=TH.acc if TH.day else GOLD_T, align="c", track=8, alpha=cx.amt(at + 0.6 + 0.16 * len(lines), 0.6))
    if src:
        CM.ink(f, src, W / 2, yy + 116, face="cap_i", size=30, color=TH.fg2, align="c", alpha=cx.amt(at + 0.8 + 0.16 * len(lines), 0.6))
    if stampt:
        CM.stamp(f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 56)
    cam.end(f)
    CM.finish(f, cx)


# ───────────────────────────── counter ─────────────────────────────
@ckind("counter")
def k_counter(cx, value=850000, unit="florin", label="", at=0.0, dur=1.7, coin=False, sub=None, size=200, prefix="", suffix="", decimals=0,
              seed=0, color=None, **_):
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed)
    cam.begin(f)
    k = ease_out(clamp((cx.t - cx.at(at)) / dur), 3)
    v = value * k
    s = (f"{v:.{decimals}f}".replace(".", ",") if decimals else CM.fmt_int(v))
    txt = prefix + s + suffix
    a = cx.amt(at, 0.4)
    size = CM.fit_size(txt, "title", size, 1300 if not coin else 1000, 6)
    wd = sk.text_width(txt, "title", size, 6)
    xc = W / 2 + (130 if coin else 0)
    if coin:
        CP.draw_coin(f, xc - wd / 2 - 150, H * 0.47, 240, spin=cx.t * 1.4, alpha=a, shadow=0.55, glint=((cx.t * 0.5) % 2.0) if (cx.t * 0.5) % 2.0 < 1 else None)
    sp = CM.engraved(txt, "title", int(size), 6.0, color or (TH.fg if TH.day else GOLD_T)) if TH.day else CM.gilt(txt, "title", int(size), 6.0)
    CM.draw_spr(f, sp, xc, H * 0.47 + size * 0.34, "c", alpha=a, shadow=0.5 if not TH.day else 0.0)
    y = H * 0.47 + size * 0.34
    if unit:
        CM.ink(f, sk.tr_upper(unit), xc, y + 82, face="title_m", size=50, color=TH.acc if TH.day else GOLD_T, align="c", track=14, alpha=cx.amt(at + 0.3, 0.5))
    if label:
        CM.ink(f, label, xc, y + 150, face="cap_i", size=46, color=TH.fg2, align="c", alpha=cx.amt(at + 0.6, 0.6))
    if sub:
        CM.ink(f, sub, xc, y + 204, face="cap", size=32, color=TH.fg3, align="c", track=3, alpha=cx.amt(at + 0.9, 0.6))
    cam.end(f)
    CM.finish(f, cx)


# ───────────────────────────── palle ─────────────────────────────
@ckind("palle")
def k_palle(cx, at=0.0, size=520, kick=None, caption=None, sub=None, stampt=None, field="gold", seed=0, pos=(W / 2, H * 0.47), **_):
    """Altı top (palle) Medici arması: yaldızlı sivri-tane zemin, kırmızı mine toplar, lapis top üstünde 3 zambak. Parıltı taranır."""
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed)
    cam.begin(f)
    a = cx.amt(at, 0.9)
    sc = (0.92 + 0.08 * ease_out(a)) * (1.0 + 0.02 * cx.u)
    gl = (cx.t * 0.30 + 0.1) % 2.0
    CP.draw_arms(f, pos[0], pos[1] + math.sin(cx.t * 1.1) * 5, size * sc, alpha=a, shadow=0.6, glow=0.22 * a if not TH.day else 0.08 * a, glint=gl if gl < 1 else None, field=field)
    if kick:
        CM.kick(f, kick, W / 2, 128, alpha=cx.amt(at + 0.3, 0.7), size=34, track=14)
    if caption:
        CM.ink(f, caption, W / 2, H * 0.865, face="cap_i", size=48, color=TH.fg2, align="c", alpha=cx.amt(at + 0.8, 0.7))
    if sub:
        sp = title_spr(sub, 50, 10.0)
        CM.draw_spr(f, sp, W / 2, H * 0.80, "c", alpha=cx.amt(at + 0.5, 0.8))
    if stampt:
        CM.stamp(f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 56)
    cam.end(f)
    CM.finish(f, cx)


# ───────────────────────────── coin ─────────────────────────────
@ckind("coin")
def k_coin(cx, at=0.0, size=520, kick=None, caption=None, sub=None, spin_rate=0.9, stampt=None, n=1, seed=0, pos=(W / 2, H * 0.47), **_):
    """Florin: dönen sikke (bir yüzünde zambak, diğerinde Vaftizci Yahya). n>1: arkada yan yana soluk sikkeler (yığın hissi)."""
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed)
    cam.begin(f)
    a = cx.amt(at, 0.9)
    gl = (cx.t * 0.42 + 0.2) % 2.0
    if n > 1:
        rs = np.random.RandomState(7)
        for i in range(n - 1):
            ang = 2 * math.pi * i / (n - 1) + 0.6
            rx, ry = size * 0.78, size * 0.30
            CP.draw_coin(f, pos[0] + math.cos(ang) * rx, pos[1] + 30 + math.sin(ang) * ry, size * 0.52, spin=cx.t * (0.7 + 0.2 * (i % 3)) + i, alpha=0.9 * a, shadow=0.5)
    CP.draw_coin(f, pos[0], pos[1] + math.sin(cx.t * 1.2) * 6, size * (0.93 + 0.07 * ease_out(a)), spin=cx.t * spin_rate + 0.35, alpha=a, shadow=0.55,
                 glow=0.20 * a if not TH.day else 0.06 * a, glint=gl if gl < 1 else None)
    if kick:
        CM.kick(f, kick, W / 2, 128, alpha=cx.amt(at + 0.3, 0.7), size=34, track=14)
    if sub:
        sp = title_spr(sk.tr_upper(sub), 56, 12.0)
        CM.draw_spr(f, sp, W / 2, H * 0.80, "c", alpha=cx.amt(at + 0.5, 0.8))
    if caption:
        CM.ink(f, caption, W / 2, H * 0.865, face="cap_i", size=46, color=TH.fg2, align="c", alpha=cx.amt(at + 0.8, 0.7))
    if stampt:
        CM.stamp(f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 56)
    cam.end(f)
    CM.finish(f, cx)


# ───────────────────────────── emblem (genel simge) ─────────────────────────────
@ckind("emblem")
def k_emblem(cx, icon="coin", metal="gold", size=460, at=0.0, kick=None, sub=None, caption=None, stampt=None, pos=(W / 2, H * 0.46), glow=0.3,
             extra=None, seed=0, **_):
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed)
    cam.begin(f)
    a = cx.amt(at, 0.8)
    sc = (0.9 + 0.1 * sk.back_out(a)) * (1.0 + 0.03 * cx.u)
    icons.draw_icon(f, icon, pos[0], pos[1] + math.sin(cx.t * 1.3) * 5, size=size * sc, metal=metal, alpha=a, glow=glow * a if not TH.day else 0.08 * a)
    if kick:
        CM.kick(f, kick, W / 2, 128, alpha=cx.amt(at + 0.3, 0.6), size=34, track=14)
    if sub:
        sp = title_spr(sub, 50, 10.0)
        CM.draw_spr(f, sp, W / 2, H * 0.82, "c", alpha=cx.amt(at + 0.5, 0.8))
    if caption:
        CM.ink(f, caption, W / 2, H * 0.89, face="cap_i", size=44, color=TH.fg2, align="c", alpha=cx.amt(at + 0.8, 0.6))
    if stampt:
        CM.stamp(f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 56)
    if extra:
        extra(cx)
    cam.end(f)
    CM.finish(f, cx)


# ───────────────────────────── black ─────────────────────────────
@ckind("black")
def k_black(cx, text=None, at=0.0, size=60, **_):
    f = cx.f
    f.clear("#06070C" if not TH.day else "#1A140C")
    if text:
        CM.ink(f, text, W / 2, H / 2, face="cap_i", size=size, color="#D9C795", align="c", alpha=cx.amt(at, 0.8), emboss=False)
