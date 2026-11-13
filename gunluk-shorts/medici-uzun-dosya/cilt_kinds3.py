"""cilt_kinds3 — Medici cildi çekim türleri, üçüncü grup: map (fresk/lapis harita), timeline, tree, bars, stacked, iconrow, network.
`cilt_kinds` sonunda içe aktarılır."""
import functools
import math
import zlib

import numpy as np
import skia

import cilt_medici as CM
import cilt_orn as ORN
import cilt_props as CP
import icons
import sk
from sk import C, Frame, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, seg, smooth
from cilt_medici import PIG, TH, ckind

# ek fraksiyon renkleri (Medici haritaları)
sk.FAC.update(dict(
    floransa=("#B33620", "#E8C25A"), toskana=("#B8603E", "#E8C25A"), cenova=("#C9A23A", "#3A2A10"), siena=("#8A6A9E", "#F0E8D0"),
    lucca=("#4F7A5A", "#F0E8D0"), ferrara=("#3E7A8A", "#F0E8D0"), mantova=("#7A8A3E", "#F0E8D0"),
))


def _h(s):
    """Süreçler arası kararlı sözcük özeti (hash() her çalıştırmada değişir)."""
    return zlib.crc32(str(s).encode("utf-8"))


def pig(name):
    """Pigment adı → hex (lapis, cinnabar, ochre, terra, umber, gold, lime, ink, rose, madder)."""
    m = dict(lapis=PIG["LAPIS"], cinnabar=PIG["CINNABAR"], vermilion=PIG["VERMILION"], ochre=PIG["OCHRE"], terra=PIG["TERRA"], umber=PIG["UMBER"],
             gold=PIG["GOLD"], lime=PIG["LIME"], ink=PIG["INK_S"], rose=PIG["ROSE"], madder=PIG["MADDER"], malachite=PIG["MALACHITE"], azurite=PIG["AZURITE"])
    if name in m:
        return m[name]
    if isinstance(name, str) and name in sk.FAC:
        return sk.FAC[name][0]
    return name


# ───────────────────────────── Medici bölgeleri ─────────────────────────────
_REG_DONE = [False]


def medici_regions(mv):
    """Floransa Cumhuriyeti (~1450) ve Toskana Büyük Dükalığı (~1570) YAKLAŞIK sınırları (kıyıya kırpılır)."""
    if _REG_DONE[0]:
        return
    prev = getattr(mv, "clip_to_land", False)
    mv.clip_to_land = True
    mv.add_region("floransa", [[(10.30, 43.55), (10.28, 43.95), (10.75, 44.10), (11.30, 44.16), (11.78, 44.08), (12.10, 43.78), (12.22, 43.35), (11.88, 43.22),
                                 (11.46, 43.42), (11.18, 43.50), (10.95, 43.30), (10.55, 43.30)]])
    mv.add_region("toskana", [[(9.95, 42.90), (10.20, 43.95), (10.60, 44.10), (11.30, 44.20), (11.85, 44.12), (12.25, 43.85), (12.30, 43.30), (11.95, 42.62), (11.30, 42.30),
                                (10.70, 42.35), (10.10, 42.60)]])
    mv.clip_to_land = prev
    _REG_DONE[0] = True


def _callout(f, text, x, y, k=1.0, w=560, size=34, sub=None, align="l"):
    lines = sk.wrap_text(text, "cap_b", size, w - 56)
    h = len(lines) * size * 1.22 + 40 + (size * 0.85 if sub else 0)
    xx = x if align == "l" else x - w
    CM.tablet(f, xx, y - 10 + (1 - k) * 10, w, h, alpha=k, corner=10)
    for i, ln in enumerate(lines):
        CM.ink(f, ln, xx + 30, y + 32 + i * size * 1.22 + (1 - k) * 10, face="cap_b", size=size, color=TH.fg, align="l", alpha=k, emboss=False)
    if sub:
        CM.ink(f, sub, xx + 30, y + 32 + len(lines) * size * 1.22 + 6, face="cap_i", size=size * 0.8, color=TH.fg2, align="l", alpha=k, emboss=False)


def _date_plate(f, txt, cx, t, at_=0.2):
    k = cx.amt(at_, 0.6)
    if k <= 0:
        return
    sz = 56
    wd = sk.text_width(txt, "title", sz, 6) + 80
    x, y = 90, H - 300
    CM.tablet(f, x, y - 66 * k, wd, 92, alpha=k, corner=10)
    CM.ink(f, txt, x + wd / 2, y - 4 * k, face="title", size=sz * 0.8, color=TH.fg, align="c", track=6, alpha=k, emboss=False)


# ───────────────────────────── map ─────────────────────────────
@ckind("map")
def k_map(cx, cam=(8, 47, 1.5), cams=None, style=None, regions=(), cities=(), routes=(), labels=(), icons_=(), notes=(), date=None,
          frame=True, compass=None, mountains=True, drift=None, tint=None, ripples=True, vig=0.5, extra=None, kick=None, approx=True, **_):
    """Fresk harita (gündüz: sıva-kâğıt zemin, ink kıyı, pigment bölgeler; gece: lapis deniz, altın kıyı). Parametreler Şarlken 'map' ile uyumludur.
    cams: [(an, (lon,lat,zoom)), …]; regions: [dict(name,color,at,alpha,hatch,glow)]; cities: [dict(lon,lat,name,kind,at,side,size)];
    routes: [dict(pts,at,dur,color,width,dash,label,arrow)]; labels: [dict(text,lon,lat,size,color,at,face,track,rot)]; icons_: [dict(kind,lon,lat,size,at,metal,rot,bob)]."""
    import mapsk
    import shots as SH
    f = cx.f
    mv = SH.mapview()
    medici_regions(mv)
    st = style or ("fresco" if TH.day else "lapis")
    if st == "paper":
        st = "fresco"
    if st == "night":
        st = "lapis"
    day = st == "fresco"
    if cams:
        ks = [(cx.at(a), v) for a, v in cams]
        c0 = ks[0][1]
        if cx.t <= ks[0][0]:
            cm = mapsk.Cam(*c0)
        elif cx.t >= ks[-1][0]:
            cm = mapsk.Cam(*ks[-1][1])
        else:
            cm = mapsk.Cam(*ks[-1][1])
            for (ta, va), (tb, vb) in zip(ks[:-1], ks[1:]):
                if ta <= cx.t <= tb:
                    cm = mapsk.cam_move(va, vb, (cx.t - ta) / max(1e-6, tb - ta))
                    break
    else:
        lon, lat, z = cam
        if drift:
            lon, lat, z = lon + drift[0] * cx.u, lat + drift[1] * cx.u, z * (1 + drift[2] * cx.u)
        else:
            z = z * (1.0 + 0.04 * cx.u)
        cm = mapsk.Cam(lon, lat, z)
    mv.base(f, cm, st, t=cx.t, mountains=mountains, ripples=ripples, tint=tint)
    txtc = TH.fg if day else "#F4E9CB"
    halo = (0, 0, 3.2, "#F3EAD2") if day else (2, 2, 3, "#000000")
    for r in regions:
        k = cx.amt(r.get("at", 0.0), r.get("dur", 0.8))
        if k > 0:
            mv.region(f, cm, r["name"], pig(r["color"]), alpha=r.get("alpha", 0.55 if day else 0.62), amt=k, hatch=r.get("hatch", False), glow=r.get("glow", True), style=st)
    for l in labels:
        k = cx.amt(l.get("at", 0.0), 0.7)
        if k > 0:
            mv.label(f, cm, l["text"], l["lon"], l["lat"], size=l.get("size", 34), color=l.get("color", "#2E2012" if day else "#E8D7A4"), face=l.get("face", "title_m"),
                     track=l.get("track", 10), alpha=k * l.get("alpha", 1.0), rot=l.get("rot", 0.0), shadow=day is False, scale_with_zoom=l.get("swz", 0.0))
    rcol = "#A8321E" if day else "#F0D27A"
    for r in routes:
        ta = r.get("at", 0.0)
        k = ease_io(clamp((cx.t - cx.at(ta)) / r.get("dur", 1.8)))
        if k > 0:
            end = mv.route(f, cm, r["pts"], prog=k, color=pig(r.get("color", rcol)), width=r.get("width", 6.0), dash=r.get("dash"), arrow=r.get("arrow", True),
                           alpha=r.get("alpha", 1.0), dash_phase=-cx.t * 30)
            if r.get("label") and end is not None and k > 0.5:
                CM.ink(f, r["label"], end[0] + 18, end[1] - 14, face="cap_b", size=r.get("lsize", 32), color=TH.fg if day else "#FFF1C4", align="l", alpha=cx.amt(ta, 0.4, off=r.get("dur", 1.8) * 0.5), emboss=day)
    for c_ in cities:
        mv.city(f, cm, c_["lon"], c_["lat"], c_.get("name"), kind=c_.get("kind", "town"), t=cx.t, color=pig(c_.get("color", "#B33620" if day else "#F0D27A")), size=c_.get("size", 32),
                name_side=c_.get("side", "r"), amt=cx.amt(c_.get("at", 0.0), 0.5), txt=txtc, shadow=halo)
    for ic in icons_:
        k = cx.amt(ic.get("at", 0.0), 0.5)
        if k <= 0:
            continue
        if "route" in ic:
            pr = ease_io(clamp((cx.t - cx.at(ic.get("move_at", ic.get("at", 0.0)))) / ic.get("move_dur", 3.0)))
            (x, y), ang = mv.point_on(cm, ic["route"], pr)
            rot = ic.get("rot", 0.0)
        else:
            x, y = cm.ll(ic["lon"], ic["lat"])
            rot = ic.get("rot", 0.0)
        bob = math.sin(cx.t * 2.0 + ic.get("lon", 0)) * ic.get("bob", 0.0)
        icons.draw_icon(f, ic["kind"], x, y + bob, size=ic.get("size", 70) * (0.8 + 0.2 * ease_out(k)), metal=ic.get("metal", "gold"), alpha=k, rot=rot, glow=ic.get("glow", 0.0), flip=ic.get("flip", False))
    if frame:
        ORN.frame_panel(f, 70, 70, W - 140, H - 140, band=26, kind="lozenge", alpha=0.96)
        cp = compass if compass else (W - 160, H - 270, 62)
        mv.compass(f, cp[0], cp[1], cp[2], alpha=0.9, style=st)
    if date:
        txt, at_ = (date, 0.2) if isinstance(date, str) else date
        _date_plate(f, txt, cx, cx.t, at_ if isinstance(at_, (int, float)) else 0.2)
    if approx and regions:
        CM.ink(f, "SINIRLAR YAKLAŞIKTIR", W / 2, H - 140, face="cap_i", size=28, color=TH.fg3 if day else "#C9BB8E", align="c", track=5, alpha=0.8 * cx.amt(0.8, 0.6), emboss=False)
    for n in notes:
        k = cx.amt(n.get("at", 0.0), 0.5)
        if k > 0:
            _callout(f, n["text"], n["x"], n["y"], k, w=n.get("w", 560), size=n.get("size", 34), sub=n.get("sub"), align=n.get("align", "l"))
    if kick:
        CM.kick(f, kick, W / 2, 130, alpha=cx.fade(0.5, 0.4), size=32, track=11)
    if extra:
        extra(cx, cm, mv)
    CM.finish(f, cx, motes_n=18, vig_s=0.42 if day else 0.62)


# ───────────────────────────── timeline ─────────────────────────────
@ckind("timeline")
def k_timeline(cx, a0=1400, a1=1500, events=(), at=0.0, title=None, hl=None, y=H * 0.52, step=10, w=1560, seed=0, **_):
    """Yıl cetveli: boyalı çizgi + çentikler; olaylar sinabar palle işaretleri (yıl: Cinzel, etiket: Cormorant); hl=(y0,y1,etiket[,çapa]) vurgulu aralık."""
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed, cam=CM.Cam(cx, push=0.035, drift=(6.0, 2.0)), dress="both")
    cam.begin(f)
    c = f.c
    x0 = W / 2 - w / 2

    def X(yr):
        return x0 + (yr - a0) / (a1 - a0) * w
    a = cx.amt(at, 0.6)
    if title:
        CM.kick(f, title, W / 2, 168, alpha=a, size=34, track=11)
    prog = ease_out(clamp((cx.t - cx.at(at)) / 1.0))
    p = f.paint(TH.rule if TH.day else "#D8B25A", style="stroke", sw=5.0, alpha=0.95)
    CM.wobble(p, 16.0, 1.0, 3)
    c.drawLine(x0, y, x0 + w * prog, y, p)
    yr = a0
    while yr <= a1:
        xx = X(yr)
        if xx <= x0 + w * prog + 1:
            major = (yr % (step * 2) == 0)
            L = 22 if major else 12
            f.line(xx, y - L, xx, y + L, color=TH.rule if TH.day else "#D8B25A", sw=2.4, alpha=0.9)
            if major:
                CM.ink(f, str(yr), xx, y + 70, face="title_m", size=28, color=TH.fg3 if TH.day else "#BFB287", align="c", track=3, alpha=0.95, emboss=False)
        yr += step
    if hl:
        y0_, y1_, lab = hl[0], hl[1], hl[2]
        ta = hl[3] if len(hl) > 3 else at + 2.0
        k = cx.amt(ta, 0.8)
        xa, xb = X(y0_), X(y1_)
        f.rrect(xa, y - 11, (xb - xa) * k, 22, 11, color=TH.acc if TH.day else "#C95A40", alpha=0.62)
        CM.ink(f, lab, (xa + xb) / 2, y - 70, face="title", size=56, color=TH.acc if TH.day else CM.CREAM if hasattr(CM, "CREAM") else "#F4E9CB", align="c", track=6, alpha=k)
    for i, ev in enumerate(events):
        yr_, lab = ev[0], ev[1]
        ta = ev[2] if len(ev) > 2 and ev[2] is not None else at + 0.5 + 0.4 * i
        col = pig(ev[3]) if len(ev) > 3 and ev[3] else (TH.acc if TH.day else "#EDB968")
        k = cx.amt(ta, 0.5)
        if k <= 0:
            continue
        xx = X(yr_)
        up = -1 if i % 2 == 0 else 1
        L = (150 if up > 0 else 112) * k
        c.drawLine(xx, y, xx, y + up * L, f.paint(TH.rule if TH.day else "#D8B25A", style="stroke", sw=3.0, alpha=0.9 * k))
        r_ = 14 * k
        f.circle(xx + 1.5, y + 3, r_, color="#000000", alpha=0.3 * k, blur=2)
        f.circle(xx, y, r_, shader=f.rad(xx - r_ * 0.35, y - r_ * 0.4, r_ * 1.7, [(mix(col, "#FFFFFF", 0.42), 0.0), (col, 0.5), (mix(col, "#000000", 0.4), 1.0)]), alpha=k)
        f.circle(xx, y, r_, style="stroke", sw=1.4, color=PIG["INK_S"], alpha=0.7 * k)
        ty = y + up * (196 if up > 0 else 128)
        CM.ink(f, str(yr_), xx, ty - 42, face="title", size=46, color=TH.acc if TH.day else "#EDB968", align="c", track=3, alpha=k)
        CM.ink(f, lab, xx, ty + 8, face="cap_b", size=36, color=TH.fg, align="c", alpha=k)
    cam.end(f)
    CM.finish(f, cx)


# ───────────────────────────── bars / stacked ─────────────────────────────
@functools.lru_cache(maxsize=16)
def _gouache(w, h, seed=3):
    """Guaj doku maskesi (bar yüzeyi için: hafif fırça + pigment yoğunluğu)."""
    import cilt_wall as CW
    rs = np.random.RandomState(seed)
    st = rs.standard_normal((h // 2 + 2, w // 2 + 2)).astype(np.float32)
    st = np.clip(1 + 0.08 * (np.array(__import__("cv2").resize(__import__("cv2").GaussianBlur(st, (0, 0), sigmaX=30, sigmaY=1.6), (w, h))) / 0.15), 0.8, 1.2)
    return st


def _bar_fill(f, x, y, w, h, col, alpha=1.0, r=8):
    """Pigment çubuk: dikey ışık, hafif doku çizgileri, el çizimi mürekkep kenar."""
    c = f.c
    f.rrect(x + 3, y + 5, w, h, r, color="#000000", alpha=0.26 * alpha, blur=5)
    f.rrect(x, y, w, h, r, shader=f.lin(x, y, x, y + h, [(mix(col, "#FFFFFF", 0.22), 0.0), (col, 0.5), (mix(col, "#000000", 0.30), 1.0)]), alpha=alpha)
    # fırça çizgileri
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), skia.ClipOp.kIntersect, True)
    rs = np.random.RandomState(int(x + w) % 97)
    for i in range(int(h / 7)):
        yy = y + 4 + i * 7 + rs.rand() * 3
        c.drawLine(x, yy, x + w, yy + rs.randn() * 1.2, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.1, Color=C("#FFFFFF" if rs.rand() < 0.5 else "#000000", int(26 * alpha))))
    c.restore()
    p = f.paint(PIG["INK_S"], style="stroke", sw=2.2, alpha=0.85 * alpha)
    CM.wobble(p, 12.0, 1.0, 5)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), p)


@ckind("bars")
def k_bars(cx, items=(), unit="", at=0.0, title=None, maxv=None, dur=1.4, x0=520, bar_h=64, gap=34, w=1000, y0=None, valfmt=None, seed=0, **_):
    """Yatay pigment çubuklar. items=[(etiket, değer, pigment|hex, çapa?)]."""
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed, cam=CM.Cam(cx, push=0.03, drift=(5.0, 2.0)), dress="both")
    cam.begin(f)
    n = len(items)
    maxv = maxv or max(i[1] for i in items)
    tot_h = n * bar_h + (n - 1) * gap
    y = (y0 if y0 is not None else H / 2 - tot_h / 2 + 10)
    if title:
        CM.kick(f, title, W / 2, y - 80, alpha=cx.amt(at, 0.6), size=36, track=10)
    for i, it in enumerate(items):
        lab, val, col = it[0], it[1], pig(it[2])
        ta = it[3] if len(it) > 3 else at + 0.3 * i
        k = ease_out(clamp((cx.t - cx.at(ta)) / dur), 3)
        a = cx.amt(ta, 0.4)
        yy = y + i * (bar_h + gap)
        CM.ink(f, lab, x0 - 30, yy + bar_h * 0.68, face="title_m", size=32, color=TH.fg, align="r", track=3, alpha=a)
        f.rrect(x0, yy, w, bar_h, 8, color="#000000", alpha=0.10 * a)
        bw = max(0.1, w * val / maxv * k)
        _bar_fill(f, x0, yy, bw, bar_h, col, a)
        vs = (valfmt(val * k) if valfmt else CM.fmt_int(val * k)) + (" " + unit if unit else "")
        CM.ink(f, vs, x0 + bw + 22, yy + bar_h * 0.70, face="title_m", size=38, color=TH.fg, align="l", alpha=a)
    cam.end(f)
    CM.finish(f, cx)


@ckind("stacked")
def k_stacked(cx, parts=(), total_label=None, total=None, unit="florin", at=0.0, dur=1.6, title=None, y=H * 0.5, w=1500, h=124, seed=0, **_):
    """Parçalı tek çubuk. parts=[(etiket, değer, pigment, çapa?)]; toplam üstte."""
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed, cam=CM.Cam(cx, push=0.03, drift=(5.0, 2.0)), dress="both")
    cam.begin(f)
    tot = total or sum(p[1] for p in parts)
    x0 = W / 2 - w / 2
    if title:
        CM.kick(f, title, W / 2, y - 190, alpha=cx.amt(at, 0.6), size=36, track=10)
    ORN.hairline_frame(f, x0 - 18, y - 18, w + 36, h + 36, alpha=0.9 * cx.amt(at, 0.5), gap=8, corner_dots=False)
    x = x0
    for i, p_ in enumerate(parts):
        lab, val, col = p_[0], p_[1], pig(p_[2])
        ta = p_[3] if len(p_) > 3 else at + 0.5 * i
        k = ease_out(clamp((cx.t - cx.at(ta)) / dur), 3)
        a = cx.amt(ta, 0.4)
        pw = w * val / tot * k
        if pw > 1:
            _bar_fill(f, x, y, pw, h, col, a, r=4)
        if k > 0.55 and pw > 80:
            CM.ink(f, CM.fmt_int(val * k), x + pw / 2, y + h * 0.64, face="title_m", size=min(46, max(30, pw * 0.2)), color="#FFF3D2", align="c", alpha=a, emboss=False)
            CM.ink(f, lab, x + pw / 2, y + h + 62, face="title_m", size=30, color=TH.fg, align="c", track=3, alpha=a)
        x += pw
    if total_label:
        a = cx.amt(at + 0.1, 0.6)
        sp = CM.engraved(total_label, "title", 62, 6.0, TH.fg) if TH.day else CM.gilt(total_label, "title", 62, 6.0)
        CM.draw_spr(f, sp, W / 2, y - 66, "c", alpha=a)
    cam.end(f)
    CM.finish(f, cx)


# ───────────────────────────── iconrow ─────────────────────────────
@ckind("iconrow")
def k_iconrow(cx, items=(), at=0.0, y=H * 0.46, size=190, gap=None, title=None, hl=None, metal="gold", seed=0, **_):
    """items=[dict(icon, label, sub, at, metal)] yan yana kabartma simgeler (yaldız/bronz/lapis…), altlarında Cinzel etiket."""
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed, cam=CM.Cam(cx, push=0.035, drift=(5.0, 2.0)), dress="both")
    cam.begin(f)
    n = len(items)
    gap = gap or min(size * 1.7, (W - 300) / max(1, n - 1 if n > 1 else 1))
    x0 = W / 2 - gap * (n - 1) / 2
    if title:
        CM.kick(f, title, W / 2, 170, alpha=cx.amt(at, 0.6), size=34, track=11)
    for i, it in enumerate(items):
        ta = it.get("at", at + 0.4 * i)
        k = cx.amt(ta, 0.55)
        x = x0 + i * gap
        sc = 0.8 + 0.2 * sk.back_out(k)
        if hl is not None and hl == i:
            f.circle(x, y, size * 0.9, shader=f.rad(x, y, size * 0.9, [("#F0D27A", 0.0, int(100 + 36 * math.sin(cx.t * 4))), ("#F0D27A", 1.0, 0)]))
        icons.draw_icon(f, it["icon"], x, y - 10 * (1 - k), size=size * sc, metal=it.get("metal", metal), alpha=k, glow=0.0)
        if it.get("label"):
            CM.ink(f, it["label"], x, y + size * 0.80, face="title_m", size=32, color=TH.fg, align="c", track=5, alpha=k)
        if it.get("sub"):
            CM.ink(f, it["sub"], x, y + size * 0.80 + 44, face="cap_i", size=32, color=TH.fg2, align="c", alpha=k)
    cam.end(f)
    CM.finish(f, cx)


# ───────────────────────────── tree ─────────────────────────────
def _edge_path(xa, ya, xb, yb, bow=0.0):
    ym = (ya + yb) / 2
    p = skia.Path()
    p.moveTo(xa, ya)
    p.cubicTo(xa + bow, ym, xb + bow, ym, xb, yb)
    return p


@ckind("tree")
def k_tree(cx, nodes=(), edges=(), at=0.0, title=None, size=200, seed=0, **_):
    """Soy ağacı: bronz madalya/simge düğümleri, mürekkep ip bağlar. nodes=[dict(id,key|icon,name,dates,x,y (0..1),at,metal,size,tag)]; edges=[(a,b,çapa[,renk])]."""
    import cilt_medal as CMD
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed, cam=CM.Cam(cx, push=0.03, drift=(5.0, 2.0)), dress="top")
    cam.begin(f)
    pos = {n["id"]: (n["x"] * W, n["y"] * H) for n in nodes}
    pos_off = {n["id"]: n.get("size", size) / 2 + (104 if (n.get("name") or n.get("dates")) else 24) for n in nodes}
    if title:
        CM.kick(f, title, W / 2, 160, alpha=cx.amt(at, 0.6), size=32, track=10)
    for e in edges:
        a_, b_ = e[0], e[1]
        ta = e[2] if len(e) > 2 else at
        col = pig(e[3]) if len(e) > 3 else (TH.rule if TH.day else "#D8B25A")
        k = ease_out(clamp((cx.t - cx.at(ta)) / 0.8), 2)
        if k <= 0:
            continue
        (xa, ya), (xb, yb) = pos[a_], pos[b_]
        path = _edge_path(xa, ya + pos_off.get(a_, 24), xb, yb - 30)
        pm = skia.PathMeasure(path, False)
        part = skia.Path()
        pm.getSegment(0, pm.getLength() * k, part, True)
        f.path(part, style="stroke", sw=10, color="#000000", alpha=0.20, blur=2.0)
        p1 = f.paint(col, style="stroke", sw=4.5, alpha=0.95)
        CM.wobble(p1, 18.0, 0.9, 2)
        f.c.drawPath(part, p1)
    for n in nodes:
        ta = n.get("at", at)
        k = cx.amt(ta, 0.6)
        if k <= 0:
            continue
        x, y = pos[n["id"]]
        s = n.get("size", size) * (0.88 + 0.12 * ease_out(k))
        if n.get("key"):
            CMD.draw_medal_b(f, n["key"], x, y, s, n.get("metal", "bronze"), n.get("flip", False), alpha=k, inscription=n.get("ins", False), shadow=0.5)
        elif n.get("icon"):
            icons.draw_icon(f, n["icon"], x, y, size=s * 0.8, metal=n.get("metal", "gold"), alpha=k, glow=0.0)
        if n.get("name"):
            CM.ink(f, n["name"], x, y + s / 2 + 42, face="title_m", size=n.get("nsize", 30), color=TH.fg, align="c", track=3, alpha=k)
        if n.get("dates"):
            CM.ink(f, n["dates"], x, y + s / 2 + 78, face="cap_i", size=28, color=TH.fg2, align="c", alpha=k * 0.95)
        if n.get("tag"):
            CM.ink(f, n["tag"], x, y - s / 2 - 16, face="cap_b", size=28, color=TH.acc, align="c", track=4, alpha=k)
    cam.end(f)
    CM.finish(f, cx)


# ───────────────────────────── network (aile ağı) ─────────────────────────────
EDGE_KINDS = dict(
    evlilik=dict(color="#D8A63A", width=6.5, dash=None, label="EVLİLİK"),
    ortaklik=dict(color="#3E5FB8", width=5.5, dash=None, label="ORTAKLIK"),
    akrabalik=dict(color="#6A4A2A", width=4.0, dash=None, label="AKRABALIK"),
    rakip=dict(color="#B33620", width=4.5, dash=(14, 10), label="REKABET"),
    ittifak=dict(color="#4C7A56", width=5.0, dash=(2, 10), label="İTTİFAK"),
)


def auto_layout(nodes, edges, iters=260, seed=3):
    """Eksik x,y değerleri için deterministik yay-itme yerleşimi (0..1 uzayı; kenar boşlukları korunur)."""
    ids = [n["id"] for n in nodes]
    rs = np.random.RandomState(seed)
    P = {i: np.array([0.5 + 0.35 * math.cos(2 * math.pi * k / len(ids)), 0.5 + 0.3 * math.sin(2 * math.pi * k / len(ids))]) + rs.randn(2) * 0.01 for k, i in enumerate(ids)}
    for it in range(iters):
        F = {i: np.zeros(2) for i in ids}
        for a in ids:
            for b in ids:
                if a >= b:
                    continue
                d = P[a] - P[b]
                r = max(0.03, float(np.hypot(*d)))
                fr = 0.0016 / (r * r)
                F[a] += d / r * fr
                F[b] -= d / r * fr
        for e in edges:
            a, b = e[0], e[1]
            d = P[b] - P[a]
            r = float(np.hypot(*d))
            fs = (r - 0.22) * 0.05
            F[a] += d / max(r, 1e-6) * fs
            F[b] -= d / max(r, 1e-6) * fs
        for i in ids:
            F[i] += (np.array([0.5, 0.5]) - P[i]) * 0.01
            P[i] = P[i] + np.clip(F[i], -0.02, 0.02)
    xs = np.array([P[i][0] for i in ids]); ys = np.array([P[i][1] for i in ids])
    xs = (xs - xs.min()) / max(1e-6, np.ptp(xs)); ys = (ys - ys.min()) / max(1e-6, np.ptp(ys))
    return {i: (0.12 + 0.76 * xs[k], 0.20 + 0.52 * ys[k]) for k, i in enumerate(ids)}


@ckind("network")
def k_network(cx, nodes=(), edges=(), at=0.0, title=None, legend=True, size=150, seed=0, **_):
    """Aile/ortaklık ağı: düğümler (bronz portre madalyası, simge ya da baş harf yuvarlağı) + türlü ipler.
    nodes=[dict(id, name, key|icon|initials, x, y (0..1; yoksa otomatik), at, group, size)]; edges=[(a, b, tür, çapa)] tür ∈ evlilik|ortaklik|akrabalik|rakip|ittifak."""
    import cilt_medal as CMD
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed, cam=CM.Cam(cx, push=0.03, drift=(5.0, 2.0)), dress="top")
    cam.begin(f)
    c = f.c
    lay = None
    if any(("x" not in n or "y" not in n) for n in nodes):
        lay = auto_layout(nodes, edges)
    pos = {}
    for n in nodes:
        x, y = (n["x"], n["y"]) if "x" in n and "y" in n else lay[n["id"]]
        pos[n["id"]] = (x * W + math.sin(cx.t * 0.5 + _h(n["id"]) % 7) * 5, y * H + math.cos(cx.t * 0.42 + _h(n["id"]) % 5) * 4)
    if title:
        CM.kick(f, title, W / 2, 150, alpha=cx.amt(at, 0.6), size=32, track=10)
    used = []
    for e in edges:
        a_, b_, kind = e[0], e[1], e[2] if len(e) > 2 else "akrabalik"
        ta = e[3] if len(e) > 3 else at + 0.6
        k = ease_out(clamp((cx.t - cx.at(ta)) / 1.0), 2)
        if k <= 0:
            continue
        if kind not in used:
            used.append(kind)
        st = EDGE_KINDS.get(kind, EDGE_KINDS["akrabalik"])
        (xa, ya), (xb, yb) = pos[a_], pos[b_]
        mx, my = (xa + xb) / 2, (ya + yb) / 2
        nx, ny = -(yb - ya), (xb - xa)
        nl = math.hypot(nx, ny) or 1.0
        bow = 38 * (1 if (_h(a_ + b_) % 2) else -1)
        path = skia.Path()
        path.moveTo(xa, ya)
        path.quadTo(mx + nx / nl * bow, my + ny / nl * bow, xb, yb)
        pm = skia.PathMeasure(path, False)
        part = skia.Path()
        pm.getSegment(0, pm.getLength() * k, part, True)
        f.path(part, style="stroke", sw=st["width"] + 5, color="#000000", alpha=0.20, blur=2.0)
        pa = f.paint(st["color"], style="stroke", sw=st["width"], alpha=0.96)
        if st["dash"]:
            pa.setPathEffect(skia.DashPathEffect.Make(list(st["dash"]), -cx.t * 18))
        c.drawPath(part, pa)
        f.path(part, style="stroke", sw=max(1.2, st["width"] * 0.28), color="#FFFFFF", alpha=0.28)
        if k >= 1.0:       # yolculuk eden boncuk
            ph = (cx.t * 0.16 + (_h(a_ + b_) % 100) / 100.0) % 1.0
            pos_, _ = pm.getPosTan(pm.getLength() * ph)
            if pos_ is not None:
                f.circle(pos_.x(), pos_.y(), st["width"] * 0.95, color=mix(st["color"], "#FFFFFF", 0.5), alpha=0.9)
    for n in nodes:
        ta = n.get("at", at)
        k = cx.amt(ta, 0.6)
        if k <= 0:
            continue
        x, y = pos[n["id"]]
        s = n.get("size", size) * (0.85 + 0.15 * ease_out(k))
        if n.get("key"):
            CMD.draw_medal_b(f, n["key"], x, y, s, "bronze", n.get("flip", False), alpha=k, inscription=False, shadow=0.55)
        elif n.get("icon"):
            f.circle(x, y, s * 0.5, color="#000000", alpha=0.18 * k, blur=6)
            f.circle(x, y, s * 0.5, shader=f.lin(x, y - s / 2, x, y + s / 2, [(TH.plate[0], 0.0), (TH.plate[1], 1.0)]), alpha=k)
            f.circle(x, y, s * 0.5, style="stroke", sw=3, color=TH.plate_edge, alpha=k)
            icons.draw_icon(f, n["icon"], x, y, size=s * 0.62, metal=n.get("metal", "gold"), alpha=k, glow=0.0)
        else:
            ini = n.get("initials") or "".join(w_[0] for w_ in n["name"].split()[:2]).upper()
            f.circle(x + 2, y + 5, s * 0.5, color="#000000", alpha=0.30 * k, blur=6)
            f.circle(x, y, s * 0.5, shader=f.rad(x - s * 0.15, y - s * 0.2, s * 0.8, [(mix(pig(n.get("color", "lapis")), "#FFFFFF", 0.3), 0.0), (pig(n.get("color", "lapis")), 0.6), (mix(pig(n.get("color", "lapis")), "#000000", 0.4), 1.0)]), alpha=k)
            f.circle(x, y, s * 0.5, style="stroke", sw=3.4, color="#D8B25A", alpha=0.95 * k)
            CM.ink(f, ini, x, y + s * 0.16, face="title", size=s * 0.42, color="#F6E7B6", align="c", alpha=k, emboss=False)
        if n.get("name"):
            nsz = n.get("nsize", 30)
            wn = sk.text_width(n["name"], "title_m", nsz, 3) + 36
            CM.tablet(f, x - wn / 2, y + s / 2 + 8, wn, nsz + 26, alpha=k, corner=8, shadow=True)
            CM.ink(f, n["name"], x, y + s / 2 + 8 + nsz + 8, face="title_m", size=nsz, color=TH.fg, align="c", track=3, alpha=k, emboss=False)
    if legend and used:
        lx, ly = 100, H - 330
        for i, kind in enumerate(used):
            st = EDGE_KINDS.get(kind, EDGE_KINDS["akrabalik"])
            yy = ly + i * 42
            pa = f.paint(st["color"], style="stroke", sw=st["width"], alpha=0.95)
            if st["dash"]:
                pa.setPathEffect(skia.DashPathEffect.Make(list(st["dash"]), 0))
            c.drawLine(lx, yy, lx + 74, yy, pa)
            CM.ink(f, st["label"], lx + 92, yy + 9, face="title_m", size=26, color=TH.fg2, align="l", track=4, alpha=0.95, emboss=False)
    cam.end(f)
    CM.finish(f, cx)
