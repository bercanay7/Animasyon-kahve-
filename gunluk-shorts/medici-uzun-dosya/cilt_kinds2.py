"""cilt_kinds2 — Medici cildi çekim türleri, ikinci grup: ledger (defter), letter (mühürlü mektup), doc, medal/medals (bronz portre madalyası).
`cilt_kinds` sonunda içe aktarılır."""
import functools
import math

import cv2
import numpy as np
import skia

import cilt_fx as FX
import cilt_medici as CM
import cilt_orn as ORN
import cilt_paper as PP
import cilt_props as CP
import sk
from sk import C, Frame, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, seg, smooth
from cilt_medici import PIG, TH, ckind

INK_BROWN = "#2A180D"


# ───────────────────────────── tüy kalem ─────────────────────────────
@functools.lru_cache(maxsize=2)
def quill_image():
    """Yatay tüy kalem sprite'ı: uç solda (0,0 → sprite içinde (14,70)), gövde +x'e uzanır. 480×140."""
    w, h = 480, 140
    fr = Frame(w, h)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    ox, oy = 14, 70
    # sapı (kalamus): ivory
    shaft = sk.smooth_path([(ox, oy), (ox + 90, oy - 3), (ox + 200, oy - 9), (ox + 330, oy - 16), (ox + 450, oy - 24)], False, 0.5)
    # vane (tüy): üst geniş, alt dar
    top = [(ox + 120, oy - 6), (ox + 170, oy - 30), (ox + 240, oy - 54), (ox + 320, oy - 62), (ox + 390, oy - 52), (ox + 440, oy - 38), (ox + 462, oy - 26)]
    bot = [(ox + 462, oy - 26), (ox + 430, oy - 16), (ox + 360, oy - 6), (ox + 280, oy + 8), (ox + 200, oy + 14), (ox + 140, oy + 8)]
    vane = sk.smooth_path(top + bot, True, 0.45)
    c.drawPath(vane, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, oy - 60), (0, oy + 16)], [C("#F6EFDC"), C("#D9CFB5")], [0, 1])))
    c.save()
    c.clipPath(vane, skia.ClipOp.kIntersect, True)
    rs = np.random.RandomState(2)
    for i in range(70):
        x = ox + 130 + i * 4.8
        t = (x - ox) / 460.0
        yc = oy - 3 - 20 * t
        a = math.radians(-62 if True else 62)
        for sgn, ln in ((-1, 52), (1, 22)):
            p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#8F8266", int(70 + 60 * rs.rand())))
            c.drawLine(x, yc, x + math.cos(math.radians(60)) * ln * 0.6, yc + sgn * ln * 0.9, p)
    c.restore()
    # çentik (tüy ucundan kesikler)
    c.drawPath(vane, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#7A6E52", 150)))
    c.drawPath(shaft, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6.0, Color=C("#EADFC0"), StrokeCap=skia.Paint.kRound_Cap))
    c.drawPath(shaft, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#8A7A58", 160)))
    # uç: koyu mürekkepli sivri
    nib = sk.poly_path([(ox - 6, oy + 2), (ox + 40, oy - 7), (ox + 62, oy - 3), (ox + 40, oy + 3)], True)
    c.drawPath(nib, skia.Paint(AntiAlias=True, Color=C("#3A2A16")))
    c.drawCircle(ox - 3, oy + 1.5, 2.6, skia.Paint(AntiAlias=True, Color=C("#1A0F06")))
    return fr.surf.makeImageSnapshot()


def draw_quill(f, x, y, ang=-38.0, alpha=1.0, scale=1.0):
    """Kalem ucu (x,y) noktasında; ang: derece."""
    img = quill_image()
    c = f.c
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    c.scale(scale, scale)
    # gölge
    sp = skia.Paint(AntiAlias=True)
    sp.setAlphaf(0.30 * alpha)
    sp.setImageFilter(skia.ImageFilters.Blur(5, 5))
    sp.setColorFilter(skia.ColorFilters.Matrix([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]))
    c.save(); c.translate(10, 22)
    c.drawImage(img, -14, -70, CM._LIN, sp)
    c.restore()
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(alpha)
    c.drawImage(img, -14, -70, CM._LIN, p)
    c.restore()


# ───────────────────────────── ledger ─────────────────────────────
def _row_xy(side, i, lay, pad=PP.LED_PAD):
    """Satır i taban çizgisi (yerel defter koordinatları, pad içeren görüntü uzayı DEĞİL; içerik uzayı)."""
    return PP.ROW0 + (i + 0.76) * PP.ROWH


@ckind("ledger")
def k_ledger(cx, left=(), right=(), head="", title_l="DEBITORI", title_r="CREDITORI", at=0.0, seed=5, total=None, rot=-0.010, size=44,
             focus=None, quill=True, cols=("f.", "s.", "d."), ink=INK_BROWN, tone=(236, 224, 192), scale=0.95, **_):
    """Açık defter: iki sayfa; satırlar tüy kalemle sırayla yazılır (mürekkep ıslak-koyu → kurur), silinen satırlar çizilir, vurgulu satır parlar.
    left/right = [dict(text, amt=(f,s,d) | str, at=çapa, strike=çapa, hl=çapa, dur)], total=dict(text, amt, at, row)
    focus=(x_yerel, y_yerel): çekim sonunda kamera bu noktaya doğru yaklaşır."""
    f = cx.f
    lay = PP.led_layout()
    pad = PP.LED_PAD
    cxs, cys = W / 2 - 24, H / 2 - 52
    # kamera: yerel nokta → ekran
    def to_screen(lx, ly):
        return cxs + (lx - PP.LED_W / 2) * scale, cys + (ly - PP.LED_H / 2) * scale
    pivot = to_screen(*focus) if focus else (W / 2, H / 2)
    cam = CM.Cam(cx, push=0.075 if focus else 0.05, drift=(7.0, 3.0), pivot=pivot)
    CM.bgfill(f, cx, seed=seed, cam=cam)
    cam.begin(f)
    c = f.c
    img, alpha = PP.ledger_spread(seed, tone, title_l, title_r, head, cols)
    c.save()
    c.translate(cxs, cys)
    c.rotate(math.degrees(rot))
    c.scale(scale, scale)
    c.translate(-PP.LED_W / 2, -PP.LED_H / 2)
    a = cx.amt(at, 0.8)
    # defter gölgesi + defter
    sh = CM.blur_sil(alpha, 16.0, (14, 8, 2)) if "led_sh" not in _CACHE else _CACHE["led_sh"]
    _CACHE["led_sh"] = sh
    sp = skia.Paint(AntiAlias=True); sp.setAlphaf(0.55 * a)
    c.drawImage(sh, -pad + 14, -pad + 24, CM._LIN, sp)
    ip = skia.Paint(AntiAlias=True); ip.setAlphaf(a)
    c.drawImage(img, -pad, -pad, CM._LIN, ip)
    # satırlar
    quill_pos = None
    last_active = (-1e9, None)
    for side, rows in (("L", left), ("R", right)):
        x0 = lay["L0"] if side == "L" else lay["R0"]
        x1 = lay["L1"] if side == "L" else lay["R1"]
        lab_x = x0 + (74 if side == "L" else 58)
        amt_x0, col_r, _rules = PP.amt_cols(x1)
        for i, r in enumerate(rows):
            ti = cx.at(r.get("at", at + 0.6 + 0.9 * i))
            txt = r["text"]
            dur1 = r.get("dur", min(1.5, 0.35 + 0.05 * len(txt)))
            p1 = clamp((cx.t - ti) / dur1)
            if p1 <= 0:
                continue
            y = _row_xy(side, i, lay)
            lsz = size
            maxw = amt_x0 - lab_x - 18
            tw = sk.text_width(txt, "fell_i", lsz)
            if tw > maxw:
                lsz = max(PP.LAB_MIN, lsz * maxw / tw)
                tw = sk.text_width(txt, "fell_i", lsz)
            e1 = ease_io(p1, 1.6)
            struck = r.get("strike") is not None
            sa = cx.amt(r["strike"], 0.45) if struck else 0.0
            col = ink
            alpha_row = a * (1.0 - 0.5 * sa)
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(lab_x - 8, y - size * 1.0, lab_x + tw * e1 + 10, y + size * 0.45))
            PP.hand(f, txt, lab_x, y, "fell_i", lsz, col, alpha_row, 1.1, seed=i * 7 + (0 if side == "L" else 3))
            # ıslak mürekkep: önde koyu
            if p1 < 1.0:
                c.restore(); c.save()
                c.clipRect(skia.Rect.MakeLTRB(lab_x + max(0.0, tw * e1 - 70), y - size, lab_x + tw * e1 + 10, y + size * 0.45))
                PP.hand(f, txt, lab_x, y, "fell_i", lsz, "#0E0804", 0.55, 1.1, seed=i * 7 + (0 if side == "L" else 3))
            c.restore()
            front = lab_x + tw * e1
            qy = y + 4
            # tutar
            amt = r.get("amt")
            if amt is not None:
                ta0 = ti + dur1 * 0.95
                pa = clamp((cx.t - ta0) / 0.55)
                if pa > 0:
                    if isinstance(amt, str):
                        amt = (amt,)
                    cols_i = [j for j in range(3) if j < len(amt) and amt[j] not in (None, "")]
                    for j in range(len(amt)):
                        if amt[j] in (None, ""):
                            continue
                        s_ = str(amt[j])
                        wj = sk.text_width(s_, "fell_i", size)
                        xr = col_r[j]
                        aj = clamp((cx.t - (ta0 + 0.16 * j)) / 0.4)
                        if aj > 0:
                            c.save()
                            c.clipRect(skia.Rect.MakeLTRB(xr - wj - 6, y - size, xr - wj + (wj + 12) * ease_io(aj, 1.6), y + size * 0.45))
                            PP.hand(f, s_, xr, y, "fell_i", size, col, alpha_row, 0.9, seed=i * 11 + j, align="r")
                            c.restore()
                            if aj < 1.0:
                                front = xr - wj + wj * ease_io(aj, 1.6)
                                qy = y + 4
                    if pa < 1.0 or p1 < 1.0:
                        pass
            active = (p1 < 1.0) or (amt is not None and clamp((cx.t - (ti + dur1 * 0.95)) / 0.9) < 1.0)
            if active:
                last_active = (ti, (front, qy))
            # silme çizgisi
            if struck and sa > 0:
                xe = (col_r[min(2, max(0, (len(amt) if amt is not None and not isinstance(amt, str) else 1) - 1))] if amt is not None else lab_x + tw) + 6
                xe = max(xe, lab_x + tw + 8) if amt is None else xe
                p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.2, Color=C("#6E2416", 235), StrokeCap=skia.Paint.kRound_Cap)
                p.setPathEffect(skia.DiscretePathEffect.Make(11.0, 1.4, i))
                c.drawLine(lab_x - 8, y - size * 0.26, lab_x - 8 + (xe - lab_x + 12) * ease_io(sa, 1.6), y - size * 0.30, p)
            # vurgu
            if r.get("hl") is not None:
                hk = cx.amt(r["hl"], 0.7)
                if hk > 0:
                    xw = (x1 - 40) - (lab_x - 20)
                    gp = skia.Paint(AntiAlias=True)
                    gp.setShader(skia.GradientShader.MakeLinear([(lab_x - 20, 0), (lab_x - 20 + xw, 0)], [C("#FFD060", int(120 * hk)), C("#FFD060", int(40 * hk)), C("#FFD060", 0)], [0, 0.7, 1]))
                    c.drawRect(skia.Rect.MakeLTRB(lab_x - 24, y - size * 0.95, lab_x - 24 + xw * hk, y + size * 0.38), gp)
                    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.0, Color=C("#A8321E", int(235 * hk)), StrokeCap=skia.Paint.kRound_Cap)
                    p.setPathEffect(skia.DiscretePathEffect.Make(14.0, 1.1, i + 4))
                    c.drawLine(lab_x - 14, y + size * 0.34, lab_x - 14 + (xw - 6) * hk, y + size * 0.34, p)
    # toplam
    if total:
        tr_ = total.get("row", 9)
        ti = cx.at(total.get("at", at + 0.6 + 0.9 * 9))
        y = _row_xy("R", tr_, lay)
        x1 = lay["R1"]
        amt_x0, col_r, _rules = PP.amt_cols(x1)
        kk = clamp((cx.t - ti) / 0.4)
        if kk > 0:
            for dyy in (-size * 1.0, -size * 1.0 + 6):
                p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2, Color=C("#3A2210", int(210 * kk)))
                p.setPathEffect(skia.DiscretePathEffect.Make(14.0, 0.8, 5))
                c.drawLine(amt_x0 + 8, y + dyy + 8, amt_x0 + 8 + (x1 - 44 - amt_x0) * kk, y + dyy + 8, p)
            lab_x = lay["R0"] + 58
            tw = sk.text_width(total["text"], "fell_i", size)
            pj = clamp((cx.t - ti - 0.2) / 0.8)
            if pj > 0:
                c.save()
                c.clipRect(skia.Rect.MakeLTRB(lab_x - 8, y - size, lab_x + tw * ease_io(pj, 1.6) + 10, y + size * 0.5))
                PP.hand(f, total["text"], lab_x, y, "fell_i", size, "#8E2A1A", a, 1.0, seed=99)
                c.restore()
                if pj < 1.0:
                    last_active = (ti, (lab_x + tw * ease_io(pj, 1.6), y + 4))
            amt = total.get("amt")
            if amt:
                ta0 = ti + 0.9
                for j, v in enumerate(amt):
                    if v in (None, ""):
                        continue
                    aj = clamp((cx.t - (ta0 + 0.15 * j)) / 0.45)
                    if aj > 0:
                        s_ = str(v)
                        wj = sk.text_width(s_, "fell_i", size)
                        c.save()
                        c.clipRect(skia.Rect.MakeLTRB(col_r[j] - wj - 6, y - size, col_r[j] - wj + (wj + 12) * ease_io(aj, 1.6), y + size * 0.5))
                        PP.hand(f, s_, col_r[j], y, "fell_i", size, "#8E2A1A", a, 0.9, seed=120 + j, align="r")
                        c.restore()
                        if aj < 1.0:
                            last_active = (ti + 1.0, (col_r[j] - wj + wj * ease_io(aj, 1.6), y + 4))
    # kalem
    if quill:
        if last_active[1] is not None and cx.t - last_active[0] < 6.0:
            qx, qy = last_active[1]
            active_now = True
        else:
            qx, qy = lay["R1"] - 120, PP.ROW0 + 10 * PP.ROWH - 10
            active_now = False
        tt = cx.t
        # kalem yumuşakça yeni noktaya süzülür (önceki konumu bilmeden: konuma göre hafif sarsıntı + hareket)
        bob = math.sin(tt * (9.0 if active_now else 1.2)) * (1.6 if active_now else 3.0)
        draw_quill(f, qx + 4, qy + bob, ang=-58.0 + (3 if active_now else 14), alpha=a, scale=0.92)
    c.restore()
    cam.end(f)
    CM.finish(f, cx, motes_n=26)


_CACHE = {}


# ───────────────────────────── yardımcı: el yazısı satırı açılımı ─────────────────────────────
def write_line(f, cx, text, x, y, t0, face="fell_i", size=44, color=INK_BROWN, alpha=1.0, dur=None, seed=0, align="l", jitter=1.1):
    """Tüy kalemle satır açılımı: soldan sağa kırpma + önde ıslak (koyu) uç. Döner: (ilerleme 0..1, uç x, uç y)."""
    tw = sk.text_width(text, face, size)
    dur = dur or min(2.2, 0.4 + 0.045 * len(text))
    p = clamp((cx.t - t0) / dur)
    if p <= 0:
        return 0.0, x, y
    e = ease_io(p, 1.5)
    xo = x - (tw / 2 if align == "c" else tw if align == "r" else 0)
    c = f.c
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(xo - 10, y - size * 1.05, xo + tw * e + 8, y + size * 0.5))
    PP.hand(f, text, x, y, face, size, color, alpha, jitter, seed, align)
    c.restore()
    if p < 1.0:
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(xo + max(0.0, tw * e - 70), y - size * 1.05, xo + tw * e + 8, y + size * 0.5))
        PP.hand(f, text, x, y, face, size, "#0E0804", 0.5 * alpha, jitter, seed, align)
        c.restore()
    return p, xo + tw * e, y


# ───────────────────────────── letter ─────────────────────────────
@ckind("letter")
def k_letter(cx, addr=("Al Magnifico Signore", "Lorenzo de' Medici", "in Firenze"), lines=(), sig=None, date=None, at=0.0, open_at=None, seal_at=0.6,
             size=46, seed=9, tone=(238, 228, 198), seal_color="#A52A1C", stampt=None, quill=True, **_):
    """Mühürlü mektup: önce katlı paket (adres + balmumu mühür; mühür damlayıp basılır), open_at anında açılır → satır satır elyazısı.
    lines=[str | (str, çapa)]; sig=(imza, çapa); date=str."""
    f = cx.f
    cam = CM.Cam(cx, push=0.045, drift=(6.0, 3.0))
    CM.bgfill(f, cx, seed=seed, cam=cam)
    cam.begin(f)
    c = f.c
    oa = cx.at(open_at) if open_at is not None else 1e9
    k_open = smooth(clamp((cx.t - oa) / 0.8)) if open_at is not None else 0.0
    a = cx.amt(at, 0.7)
    # --- A: katlı paket
    if k_open < 1.0:
        pk = PP.paper_image(900, 560, seed, tone, "deckle", (("v", 0.5), ("h", 0.34), ("h", 0.67)), 44, 1.0)
        sc = (0.97 + 0.03 * ease_out(a)) * (1.0 + 0.10 * k_open)
        pk.draw(f, W / 2, H / 2 - 20, rot=-0.045, scale=sc, alpha=a * (1 - k_open), shadow=0.6)
        c.save(); c.translate(W / 2, H / 2 - 20); c.rotate(math.degrees(-0.045)); c.scale(sc, sc)
        ya = -70
        for i, ln in enumerate(addr):
            ai = a * (1 - k_open) * cx.amt(at + 0.3 + 0.25 * i, 0.5)
            PP.hand(f, ln, 40, ya + i * 62, "fell_i", 50 if i != 1 else 56, INK_BROWN, ai, 1.4, seed=i + 4, align="c")
        # mühür
        sk_ = clamp((cx.t - cx.at(seal_at)) / 0.45)
        if sk_ > 0:
            drop = 1.0 + (1 - sk.back_out(sk_)) * 0.7
            CM.wax_seal(f, -250, 150, 74, seal_color, alpha=a * (1 - k_open), t=sk_, palle=True)
        c.restore()
    # --- B: açık sayfa
    if k_open > 0:
        ow, oh = 1400, 780
        op = PP.paper_image(ow, oh, seed + 1, tone, "deckle", (("v", 0.5), ("h", 0.5)), 44, 1.1)
        sc = 0.92 + 0.08 * k_open
        op.draw(f, W / 2, H / 2 - 24, rot=-0.012, scale=sc, alpha=k_open, shadow=0.6)
        c.save(); c.translate(W / 2, H / 2 - 24); c.rotate(math.degrees(-0.012)); c.scale(sc, sc)
        x0, y0 = -ow / 2 + 110, -oh / 2 + 120
        last = None
        for i, ln in enumerate(lines):
            txt, an = (ln, None) if isinstance(ln, str) else ln
            t0 = cx.at(an) if an is not None else oa + 0.9 + 0.75 * i
            wsz = size if sk.text_width(txt, "fell_i", size) < ow - 260 else CM.fit_size(txt, "fell_i", size, ow - 260)
            p, qx, qy = write_line(f, cx, txt, x0, y0 + i * 68, t0, "fell_i", wsz, INK_BROWN, k_open, seed=20 + i)
            if 0 < p < 1:
                last = (qx, qy + 4)
        if date:
            PP.hand(f, date, ow / 2 - 120, -oh / 2 + 84, "fell_i", 40, "#5A3A22", k_open * cx.amt(oa + 0.6, 0.5), 1.0, seed=60, align="r")
        if sig:
            txt, an = sig
            t0 = cx.at(an)
            p, qx, qy = write_line(f, cx, txt, ow / 2 - 400, oh / 2 - 150, t0, "fell_i", size + 6, "#3A1E10", k_open, seed=70, align="c", dur=1.2)
            if 0 < p < 1:
                last = (qx, qy + 4)
            CM.wax_seal(f, ow / 2 - 110, oh / 2 - 60, 50, seal_color, alpha=k_open, t=clamp((cx.t - (cx.at(an) + 1.4)) / 0.4), palle=True)
        if quill and last is not None:
            draw_quill(f, last[0] + 4, last[1] + math.sin(cx.t * 9) * 1.5, ang=-56.0, alpha=k_open, scale=0.9)
        c.restore()
    if stampt:
        CM.stamp(f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 56)
    cam.end(f)
    CM.finish(f, cx, motes_n=28)


# ───────────────────────────── doc ─────────────────────────────
@ckind("doc")
def k_doc(cx, title="", lines=(), w=1100, h=760, at=0.0, line_dt=0.5, seal=None, seal_at=None, tone=(238, 228, 198), rot=-0.012, hl=None, hl_at=None,
          size=44, head_size=54, caption=None, stampt=None, date=None, align="l", seed=3, edge="deckle", pan=(0, 0), zoom=0.05, **_):
    """Belge (antlaşma/kararname/bono): kâğıt, başlık (oyma Cinzel), satır satır elyazısı, vurgulu ifade (altın + sinabar), balmumu mühür (palle).
    lines=[str | (str, çapa)]. seal=True|renk; hl=(x,y,w) yerel koordinat (belge merkezi 0,0) + hl_at."""
    f = cx.f
    cam = CM.Cam(cx, push=zoom, drift=(5.0, 2.5))
    CM.bgfill(f, cx, seed=seed, cam=cam)
    cam.begin(f)
    c = f.c
    a = cx.amt(at, 0.8)
    pp = PP.paper_image(int(w), int(h), seed, tone, edge, (), 44, 1.0)
    sc = 0.96 + 0.04 * ease_out(a)
    cxp, cyp = W / 2 + pan[0] * cx.u, H / 2 - 20 + pan[1] * cx.u
    pp.draw(f, cxp, cyp, rot=rot * (1 - 0.4 * cx.u), scale=sc, alpha=a, shadow=0.6)
    c.save(); c.translate(cxp, cyp); c.rotate(math.degrees(rot * (1 - 0.4 * cx.u))); c.scale(sc, sc)
    y = -h / 2 + 100
    if title:
        tsz = CM.fit_size(title, "title_m", head_size, w - 200, 4)
        sp = CM.engraved(title, "title_m", int(tsz), 4.0, "#3A2616", 0.7)
        CM.draw_spr(f, sp, 0, y, "c", alpha=a * cx.amt(at + 0.25, 0.6))
        CM.flourish_rule(f, 0, y + 28, w * 0.5, alpha=0.8 * a, color="#7A5A2E", grow=cx.amt(at + 0.45, 0.7))
        y += 104
    xs = -w / 2 + 90
    last = None
    for i, ln in enumerate(lines):
        txt, an = (ln, None) if isinstance(ln, str) else ln
        t0 = cx.at(an) if an is not None else cx.at(at, off=0.5 + i * line_dt)
        wsz = size if sk.text_width(txt, "fell_i", size) < w - 180 else CM.fit_size(txt, "fell_i", size, w - 180)
        p, qx, qy = write_line(f, cx, txt, xs if align == "l" else 0, y, t0, "fell_i", wsz, INK_BROWN, a, seed=40 + i, align="l" if align == "l" else "c")
        y += size * 1.45
    if hl and hl_at is not None:
        k = clamp((cx.t - cx.at(hl_at)) / 0.6)
        hx, hy, hw = hl
        gp = skia.Paint(AntiAlias=True)
        gp.setShader(skia.GradientShader.MakeLinear([(hx, 0), (hx + hw, 0)], [C("#FFD060", int(115 * a)), C("#FFD060", int(30 * a))], [0, 1]))
        c.drawRect(skia.Rect.MakeLTRB(hx - 6, hy - size * 0.95, hx - 6 + (hw + 12) * k, hy + size * 0.40), gp)
        pl = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.2, Color=C("#A8321E", int(235 * a)), StrokeCap=skia.Paint.kRound_Cap)
        pl.setPathEffect(skia.DiscretePathEffect.Make(14.0, 1.1, 3))
        c.drawLine(hx, hy + size * 0.36, hx + hw * k, hy + size * 0.36, pl)
    if date:
        PP.hand(f, date, -w / 2 + 90, h / 2 - 78, "fell_i", 40, "#5A3A22", a * 0.95, 1.0, seed=7, align="l")
    if seal:
        CM.wax_seal(f, w / 2 - 130, h / 2 - 104, 62, seal if isinstance(seal, str) else "#A52A1C", alpha=a, t=cx.amt(seal_at if seal_at is not None else at + 1.6, 0.4), palle=True)
    c.restore()
    if caption:
        CM.ink(f, caption, W / 2, H - 150, face="cap_i", size=40, color=TH.fg2, align="c", alpha=cx.amt(at + 0.6, 0.6))
    if stampt:
        CM.stamp(f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 56)
    cam.end(f)
    CM.finish(f, cx, motes_n=28)


# ───────────────────────────── medal / medals ─────────────────────────────
import cilt_medal as CMD  # noqa: E402


@ckind("medal")
def k_medal(cx, key="m_cosimo", metal="bronze", name=None, role=None, dates=None, pos="c", size=640, flip=False, at=0.0, plate_at=0.6, stampt=None,
            note=None, seed=0, extra=None, **_):
    """Tek bronz portre madalyası + isim levhası. pos: 'c' (altta levha) | 'l' | 'r' (yanda levha)."""
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed, cam=CM.Cam(cx, push=0.04, drift=(6.0, 2.5)), dress="top")
    cam.begin(f)
    xc = {"c": W / 2, "l": W * 0.34, "r": W * 0.66}[pos]
    yc = H * 0.44 if name else H * 0.46
    a = cx.amt(at, 0.8)
    sc = 0.95 + 0.05 * ease_out(a)
    tl = 0.20 * math.sin(cx.t * 0.55 + 0.4)
    gl = (cx.t * 0.26 + 0.2) % 1.8
    CMD.draw_medal_b(f, key, xc, yc, size * sc, metal, flip, alpha=a, tilt=tl, glint=gl if gl < 1 else None)
    if name:
        if pos == "c":
            CM.name_plate(f, name, role, dates, cx_=W / 2, y=H * 0.775, t=cx.amt(plate_at, 0.6))
        else:
            tx = W * 0.78 if pos == "l" else W * 0.22
            CM.name_plate(f, name, role, dates, cx_=tx, y=H * 0.42, t=cx.amt(plate_at, 0.6), w=540)
    if note:
        CM.ink(f, note, W / 2, H * 0.90, face="cap_i", size=40, color=TH.fg2, align="c", alpha=cx.amt(plate_at + 0.5, 0.6))
    if extra:
        extra(cx)
    if stampt:
        CM.stamp(f, stampt[0], stampt[1], stampt[2], t=cx.amt(stampt[3], 0.3), size=stampt[4] if len(stampt) > 4 else 56)
    cam.end(f)
    CM.finish(f, cx)


@ckind("medals")
def k_medals(cx, items=(), size=500, y=H * 0.43, gap=None, title=None, vs=None, plates=True, seed=0, **_):
    """Yan yana bronz madalyalar. items=[dict(key, name, role, dates, at, metal, flip)]. vs=çapa → ortada kılıç simgesi."""
    import icons
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed, cam=CM.Cam(cx, push=0.035, drift=(5.0, 2.0)), dress="top")
    cam.begin(f)
    n = len(items)
    gap = gap or min(size * 1.12, (W - 240) / max(1, n))
    x0 = W / 2 - gap * (n - 1) / 2
    for i, it in enumerate(items):
        ta = it.get("at", 0.2 + 0.35 * i)
        a = cx.amt(ta, 0.7)
        x = x0 + i * gap
        sc = (0.93 + 0.07 * ease_out(a)) * (1.0 + 0.02 * cx.u)
        g = (cx.t * 0.24 + 0.2 * i) % 2.0
        CMD.draw_medal_b(f, it["key"], x, y, size * sc, it.get("metal", "bronze"), it.get("flip", False), alpha=a, tilt=0.14 * math.sin(cx.t * 0.5 + i), glint=g if g < 1 else None)
        if plates and it.get("name"):
            CM.name_plate(f, it["name"], it.get("role"), it.get("dates"), cx_=x, y=y + size * 0.52, t=cx.amt(ta + 0.4, 0.5), w=min(gap - 24, 560))
    if vs:
        icons.draw_icon(f, "swords", W / 2, y, size=130, metal="silver", alpha=cx.amt(vs, 0.4))
    if title:
        CM.kick(f, title, W / 2, 150, alpha=cx.fade(0.6, 0.4), size=34, track=12)
    cam.end(f)
    CM.finish(f, cx)
