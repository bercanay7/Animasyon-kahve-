"""c8_kinds — c8 «Aslanın İni» özel çekim türleri (Parça 4 sahne yazarı). `scenes_c8.py` içinde import edilir; `@CM.ckind` ile kaydolur.

Dünya koordinatı = nötr kamerada ekran koordinatı (1920×1080). Kamera: `cam=[(çapa, look(wx, wy, z)), …]` (p4_lib.look) ya da `cam=("push", …)`.
Kaynak disiplini: yüz yok (siluet/simge), şiddet yok (asılı beden, kan, ceset yok); ekrana yalnız script/brif sözcükleri yazılır.
Her tür `ovl=` (çapaya bağlı bindirme: etiket, damga, tarih plakası …) kabul eder; ovl ışıktan SONRA çizilir.
"""
import functools
import math

import cv2
import numpy as np
import skia

import cilt_kinds2 as K2
import cilt_medici as CM
import cilt_paper as PP
import icons
import medal
import p4_lib as L
import sk
from cilt_medici import TH
from p4_lib import INK, P, S, SOFT, look, ov
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth


# ═══════════════════════════ kurşun mühür (bulla) ═══════════════════════════
@functools.lru_cache(maxsize=4)
def bulla_image(size=420, text="SIXTVS · PP · IIII"):
    """Kurşun bulla: yükseklik haritası (boncuk halka, yazı halkası, haç) → kabartmalı kurşun metal. Dönüş: skia.Image (size²)."""
    S_ = size
    cxy = S_ / 2.0
    R_ = S_ * 0.47

    def gp(g, style="fill", w=1.0):
        p = skia.Paint(AntiAlias=True, Color=skia.Color(int(g), int(g), int(g), 255))
        if style == "stroke":
            p.setStyle(skia.Paint.kStroke_Style)
            p.setStrokeWidth(w)
            p.setStrokeCap(skia.Paint.kRound_Cap)
        return p
    sf = skia.Surface(S_, S_)
    c = sf.getCanvas()
    c.clear(skia.ColorBLACK)
    c.drawCircle(cxy, cxy, R_, gp(104))
    c.drawCircle(cxy, cxy, R_ - S_ * 0.012, gp(170, "stroke", S_ * 0.026))
    for i in range(52):                                        # boncuk halka
        a = i * 2 * math.pi / 52
        c.drawCircle(cxy + math.cos(a) * R_ * 0.90, cxy + math.sin(a) * R_ * 0.90, S_ * 0.0125, gp(205))
    c.drawCircle(cxy, cxy, R_ * 0.835, gp(190, "stroke", S_ * 0.010))
    c.drawCircle(cxy, cxy, R_ * 0.50, gp(190, "stroke", S_ * 0.012))
    n = len(text)
    fs = S_ * 0.076
    for i, ch in enumerate(text):                              # yazı halkası
        if ch == " ":
            continue
        a = -math.pi / 2 + (i + 0.5) * 2 * math.pi / n
        blob, wd = sk.text_blob("title_m", ch, fs, 0.0)
        c.save()
        c.translate(cxy + math.cos(a) * R_ * 0.675, cxy + math.sin(a) * R_ * 0.675)
        c.rotate(math.degrees(a + math.pi / 2))
        c.drawTextBlob(blob, -wd / 2, fs * 0.36, gp(235))
        c.restore()
    # merkez: haç (patée) + dört nokta
    arm, wd = R_ * 0.30, R_ * 0.075
    c.drawRect(skia.Rect.MakeLTRB(cxy - wd, cxy - arm, cxy + wd, cxy + arm), gp(225))
    c.drawRect(skia.Rect.MakeLTRB(cxy - arm, cxy - wd, cxy + arm, cxy + wd), gp(225))
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        c.drawCircle(cxy + dx * R_ * 0.20, cxy + dy * R_ * 0.20, R_ * 0.035, gp(215))
    hh = sf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)[..., 0].astype(np.float32) / 255.0
    sa = skia.Surface(S_, S_)
    ca = sa.getCanvas()
    ca.clear(skia.ColorTRANSPARENT)
    ca.drawCircle(cxy, cxy, R_, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    al = sa.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)[..., 3].astype(np.float32) / 255.0
    rgba = medal._relief_from_height(hh, al, "lead", strength=2.2)
    return sk.np_to_image(rgba)


@functools.lru_cache(maxsize=4)
def bulla_shadow(size=420):
    S_ = size
    sa = skia.Surface(S_, S_)
    ca = sa.getCanvas()
    ca.clear(skia.ColorTRANSPARENT)
    ca.drawCircle(S_ / 2, S_ / 2, S_ * 0.47, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    al = sa.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)[..., 3]
    return CM.blur_sil(al, 12.0, (10, 8, 6))


@functools.lru_cache(maxsize=2)
def lump_image(size=240):
    """Basılmadan önceki kurşun topağı (yumru, mat)."""
    rgba = np.zeros((size, size, 4), np.uint8)
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    r = np.hypot((xx - size / 2) / 1.0, (yy - size / 2) / 0.78) / (size * 0.42)
    a = np.clip((1.0 - r) * 6, 0, 1)
    shade = np.clip(0.55 + 0.45 * (1 - r) - 0.12 * ((xx - size * 0.38) / size) ** 2 * 0 , 0, 1)
    ramp = sk._grad_ramp(sk.METAL["lead"])
    col = ramp[np.clip(shade * 255, 0, 255).astype(np.int32)]
    rgba[..., :3] = np.clip(col, 0, 255)
    rgba[..., 3] = (a * 255).astype(np.uint8)
    return sk.np_to_image(rgba)


def twisted_cord(c, x0, y0, x1, y1, w=7.0, col="#B79C6A", a=255, t=0.0):
    """Bükülü kenevir ip: iki sarmal şerit."""
    L_ = math.hypot(x1 - x0, y1 - y0)
    if L_ < 2:
        return
    ux, uy = (x1 - x0) / L_, (y1 - y0) / L_
    nx, ny = -uy, ux
    n = max(4, int(L_ / 9))
    for sgn, cc in ((1, mix(col, "#000000", 0.18)), (-1, col)):
        pts = []
        for i in range(n + 1):
            s = i / n
            off = math.sin(s * L_ / 7.0 * 1.0 + (0 if sgn > 0 else math.pi)) * w * 0.34
            pts.append((x0 + (x1 - x0) * s + nx * off, y0 + (y1 - y0) * s + ny * off))
        p = skia.Path()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        c.drawPath(p, S(cc, w * 0.62, a))
    c.drawLine(x0, y0, x1, y1, S("#2A1608", 1.0, int(70 * a / 255)))


def scribble(c, x0, x1, y, k, seed=0, col=INK, a=190, amp=4.2, words=True):
    """Okunmaz el yazısı satırı (kalem izleri): soldan sağa k oranında çizilir. Döner: uç noktası (x, y)."""
    if k <= 0.003:
        return x0, y
    rs = np.random.RandomState(seed)
    Lw = x1 - x0
    xs = x0
    pth = skia.Path()
    pth.moveTo(xs, y)
    end = (xs, y)
    xcur = xs
    while xcur < x0 + Lw * k:
        wl = rs.uniform(26, 96)
        gap = rs.uniform(12, 22)
        seg_end = min(xcur + wl, x0 + Lw * k)
        m = max(2, int((seg_end - xcur) / 8))
        for j in range(1, m + 1):
            px = xcur + (seg_end - xcur) * j / m
            py = y + (rs.uniform(-amp, amp) if j % 2 else rs.uniform(-amp * 0.3, amp * 0.3))
            pth.quadTo(px - (seg_end - xcur) / m * 0.5, y + rs.uniform(-amp, amp), px, py)
        end = (seg_end, y)
        xcur = seg_end + gap
        pth.moveTo(xcur, y)
        if xcur >= x0 + Lw:
            break
    c.drawPath(pth, S(col, 2.1, a))
    return end


def quill_at(f, x, y, a=1.0, ang=-56.0, bob=1.5, t=0.0):
    K2.draw_quill(f, x + 4, y + math.sin(t * 9.0) * bob, ang=ang, alpha=a, scale=0.9)


# ═══════════════════════════ c8_aforoz: aforoz belgesi + kurşun mühür ═══════════════════════════
DOC_W, DOC_H = 1060, 640
DOC_C = (960.0, 400.0)
BULLA_PIV = (960.0, DOC_C[1] + DOC_H / 2 - 4)          # ipin belgeden çıktığı nokta
CORD_L = 128.0
BULLA_R = 96.0
BULLA_REST = (BULLA_PIV[0], BULLA_PIV[1] + CORD_L + BULLA_R * 0.92)   # sakin konum (merkez)
LAT_PHRASE = "iniquitatis filius et perditionis alumnus"


def _swing(t_since, A=0.22, w=5.4, tau=1.5):
    if t_since < 0:
        return 0.0
    return A * math.exp(-t_since / tau) * math.cos(w * t_since)


def _shake(t_since, amp=9.0, tau=0.13, hz=26.0):
    if t_since < 0 or t_since > 1.0:
        return 0.0, 0.0
    e = math.exp(-t_since / tau)
    return amp * e * math.sin(t_since * hz * 2 * math.pi * 0.5), amp * 0.6 * e * math.cos(t_since * hz * 2 * math.pi * 0.43)


def draw_bulla(f, cx, t_imp, rest=None, drop_t=None, spin=0.0, alpha=1.0, flat_k=1.0):
    """Asılı bulla: belgeden iki ip; t_imp anında basılır (çene → topak yassılır), sonra sarkaç gibi sallanır. drop_t: ip kopar, bulla düşer (yerçekimi)."""
    c = f.c
    t = cx.t
    px, py = BULLA_PIV
    if drop_t is None or t < drop_t:
        th = _swing(t - t_imp) if t >= t_imp else 0.012 * math.sin(t * 1.3)
        bx, by = px + math.sin(th) * (CORD_L + BULLA_R * 0.9), py + math.cos(th) * (CORD_L + BULLA_R * 0.9)
        rot = th
        # ipler (iki paralel, bulla üstünde birleşir)
        for dx0 in (-26.0, 26.0):
            twisted_cord(c, px + dx0, py - 3, bx + math.sin(th) * -BULLA_R * 0.0 + dx0 * 0.25, by - BULLA_R * 0.92, w=6.5, a=int(255 * alpha), t=t)
    else:
        u = t - drop_t
        g = 2400.0
        bx0 = px + math.sin(_swing(drop_t - t_imp)) * (CORD_L + BULLA_R * 0.9)
        by0 = py + math.cos(_swing(drop_t - t_imp)) * (CORD_L + BULLA_R * 0.9)
        bx, by = bx0 + 70.0 * u, by0 + 0.5 * g * u * u - 120.0 * u
        rot = 4.0 * u
        # kopmuş ip uçları: belge kenarında kısa sarkan ipler
        for dx0, dd in ((-26.0, 0.6), (26.0, -0.4)):
            sw = math.sin(t * 2.2 + dx0) * 0.12 * math.exp(-u * 0.9)
            twisted_cord(c, px + dx0, py - 3, px + dx0 + math.sin(sw) * 54 * (1 + dd * 0.2), py + 54, w=6.0, a=int(255 * alpha))
        if by > H + 200:
            return
    k = ease_out(clamp((t - (t_imp - 0.55)) / 0.5), 2) if t_imp is not None else 1.0
    c.save()
    c.translate(bx, by)
    c.rotate(math.degrees(rot))
    if t < t_imp:
        # topak (basılmadan önce) + iki çene yaklaşır
        sc = 0.62 + 0.0
        img = lump_image(240)
        c.scale(sc, sc)
        c.drawImage(img, -120, -120, CM._LIN, skia.Paint(AntiAlias=True))
    else:
        fl = clamp((t - t_imp) / 0.16)                       # yassılma
        sx = lerp(0.62, 1.0, ease_out(fl, 3))
        sy = lerp(0.50, 1.0, ease_out(fl, 3))
        img = bulla_image(420)
        c.scale(BULLA_R * 2 / 420.0 * sx * 1.0, BULLA_R * 2 / 420.0 * sy * 1.0)
        # gölge
        sp = skia.Paint(AntiAlias=True)
        sp.setAlphaf(0.55 * alpha)
        c.drawImage(bulla_shadow(420), -210 + 16, -210 + 26, CM._LIN, sp)
        pp = skia.Paint(AntiAlias=True)
        pp.setAlphaf(alpha)
        c.drawImage(img, -210, -210, CM._LIN, pp)
        # parıltı süpürmesi
        gl = (t - t_imp - 0.2) * 0.9
        if 0.0 <= gl <= 1.0:
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(-210, -210, 210, 210))
            gx = -260 + 520 * gl
            sh = skia.GradientShader.MakeLinear([(gx - 70, -200), (gx + 70, 200)], [C("#FFFFFF", 0), C("#DCE6FF", 120), C("#FFFFFF", 0)], [0, 0.5, 1])
            c.drawRect(skia.Rect.MakeLTRB(-210, -210, 210, 210), skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kSrcATop if False else skia.BlendMode.kSrcOver))
            c.restore()
    c.restore()
    return bx, by


def draw_dies(f, cx, t_imp, bx, by):
    """Basma çeneleri: bullatorium — iki demir çene yandan yaklaşıp kapanır, geri çekilir."""
    c = f.c
    u = cx.t - (t_imp - 0.5)
    if u < -0.2 or u > 1.4:
        return
    if u < 0.5:
        k = ease_in(clamp((u + 0.2) / 0.7), 2)           # yaklaşır
    elif u < 0.62:
        k = 1.0
    else:
        k = 1.0 - ease_out(clamp((u - 0.62) / 0.6), 2)   # çekilir
    gap = lerp(330.0, 112.0, k)
    for sgn in (-1, 1):
        x = bx + sgn * gap
        c.save()
        c.translate(x, by)
        c.scale(sgn, 1.0)
        # çene: kalın koyu demir blok + tutaç
        jaw = skia.Path()
        jaw.moveTo(-26, -60); jaw.lineTo(26, -50); jaw.lineTo(26, 50); jaw.lineTo(-26, 60); jaw.close()
        c.drawPath(jaw, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-26, 0), (26, 0)], [C("#6A6E76"), C("#2A2C32")], [0, 1])))
        c.drawPath(jaw, S("#0E0F12", 2.2, 220))
        c.drawRect(skia.Rect.MakeLTRB(26, -14, 260, 14), P("#3A2A1C"))                # sap (dışa)
        c.drawRect(skia.Rect.MakeLTRB(26, -14, 260, 14), S("#16100A", 1.6, 200))
        c.restore()


def draw_scroll_roll(f, x0, x1, y, r=26.0, a=1.0):
    """Parşömen tomarı (silindir): alt kenarı yuvarlanmış kâğıt."""
    c = f.c
    rr = skia.Rect.MakeLTRB(x0 - 12, y - r, x1 + 12, y + r)
    sh = skia.GradientShader.MakeLinear([(0, y - r), (0, y + r)], [C("#F6EBD0", int(255 * a)), C("#D8C79E", int(255 * a)), C("#8E7448", int(255 * a))], [0.0, 0.55, 1.0])
    c.drawRoundRect(rr, r, r, skia.Paint(AntiAlias=True, Shader=sh))
    c.drawRoundRect(rr, r, r, S("#4A3418", 1.8, int(200 * a)))
    for xe in (x0 - 12, x1 + 12):
        c.drawOval(skia.Rect.MakeLTRB(xe - r * 0.45, y - r, xe + r * 0.45, y + r), P("#D8C79E", int(255 * a)))
        c.drawOval(skia.Rect.MakeLTRB(xe - r * 0.45, y - r, xe + r * 0.45, y + r), S("#4A3418", 1.6, int(200 * a)))
        c.drawOval(skia.Rect.MakeLTRB(xe - r * 0.2, y - r * 0.55, xe + r * 0.2, y + r * 0.55), S("#7A5A30", 1.4, int(160 * a)))


def illuminated_cap(c, x, y, s=120.0, a=1.0, t=0.0):
    """Süslü baş harf kutusu (harf yok: altın sarmal + lapis zemin)."""
    c.drawRect(skia.Rect.MakeXYWH(x, y, s, s), P("#233C8C", int(255 * a)))
    c.drawRect(skia.Rect.MakeXYWH(x, y, s, s), S("#C79A3C", 4.0, int(255 * a), cap=False))
    c.drawRect(skia.Rect.MakeXYWH(x + 8, y + 8, s - 16, s - 16), S("#C79A3C", 1.6, int(200 * a), cap=False))
    cx0, cy0 = x + s / 2, y + s / 2
    p = skia.Path()
    for i in range(64):
        u = i / 63.0
        ang = u * 5.6
        rr = s * (0.06 + 0.30 * u)
        px, py = cx0 + math.cos(ang) * rr, cy0 + math.sin(ang) * rr
        p.moveTo(px, py) if i == 0 else p.lineTo(px, py)
    c.drawPath(p, S("#E8C25A", 3.4, int(255 * a)))
    for i in range(5):
        ang = 0.6 + i * 1.25
        c.drawCircle(cx0 + math.cos(ang) * s * 0.36, cy0 + math.sin(ang) * s * 0.36, 4.5, P("#E8C25A", int(255 * a)))


@CM.ckind("c8_aforoz")
def k_aforoz(cx, phase="giris", imp_at=None, drop_at=None, seal_at=None, unroll_at=0.0, unroll_dur=1.2, line_at=None, tr_at=None, date=None, ovl=None, seed=11, **_):
    """Aforoz belgesi (kurşun mühürlü). phase: 'giris' (tomar açılır, satırlar yazılır, bulla basılır: imp_at) · 'satir' (yakın plan: Latince satır yazılır, altında TR çeviri: line_at/tr_at)
    · 'af' (bulla düşer: drop_at; mum mühür basılır: seal_at). Kamera: cam=[(çapa, look(...))] ya da push."""
    f = cx.f
    night = not TH.day
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    t_imp = cx.at(imp_at) if imp_at is not None else (-9.0 if phase != "giris" else 1e9)
    # sarsıntı (basma anı)
    sx_, sy_ = _shake(t - t_imp) if phase == "giris" else (0.0, 0.0)
    c.save()
    c.translate(sx_, sy_)
    ku = ease_io(clamp((t - cx.at(unroll_at)) / unroll_dur), 2) if phase == "giris" else 1.0
    pp = PP.paper_image(DOC_W, DOC_H, seed, (236, 224, 192), "deckle", (("h", 0.5),), 44, 1.0)
    dx, dy = DOC_C
    vis_h = DOC_H * (0.04 + 0.96 * ku)
    # belge: üstten açılıyor (üst kenara hizalı kırpma)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, 0, W, dy - DOC_H / 2 + vis_h))
    pp.draw(f, dx, dy, shadow=0.6)
    # baş harf + satırlar
    ix, iy = dx - DOC_W / 2 + 74, dy - DOC_H / 2 + 74
    illuminated_cap(c, ix, iy, 118.0, a=0.95)
    # papalık anahtarları (altın) belgenin üst ortasında küçük
    rows = []
    y0 = dy - DOC_H / 2 + 110
    xl = dx - DOC_W / 2 + 74
    xr = dx + DOC_W / 2 - 74
    for i in range(9):
        yy = y0 + i * 52
        xa = (ix + 118 + 28) if i < 2 else xl
        rows.append((xa, xr - (0 if i % 4 != 3 else 90 + 30 * (i % 3)), yy))
    tlines = cx.at(("c8s1", "Haziran", -0.3)) if phase == "giris" else -100.0
    last_end = None
    for i, (xa, xb, yy) in enumerate(rows):
        if phase == "satir" and 340 <= yy <= 560:
            continue
        t_i = (tlines if phase == "giris" else -100) + 0.12 + i * 0.30
        kk = clamp((t - t_i) / 0.62) if phase == "giris" else 1.0
        if phase == "satir":
            kk = 1.0
        e = scribble(c, xa, xb, yy, ease_io(kk, 1.4), seed=seed * 7 + i, a=int(185 - 25 * (i % 3)))
        if 0 < kk < 1:
            last_end = e
    # ağır çizgi: belge altı süs
    CM.flourish_rule(f, dx, dy + DOC_H / 2 - 72, DOC_W * 0.46, alpha=0.65, color="#7A5A2E", grow=ku)
    c.restore()
    # tomar silindiri (açılırken)
    if phase == "giris" and ku < 0.999:
        draw_scroll_roll(f, dx - DOC_W / 2 + 6, dx + DOC_W / 2 - 6, dy - DOC_H / 2 + vis_h, r=24.0)
    # kalem
    if phase == "giris" and last_end is not None and ku > 0.5 and t < t_imp:
        quill_at(f, last_end[0], last_end[1], a=1.0, t=t)
    # papalık anahtarları + tarih
    if phase == "giris":
        kk = cx.amt(("c8s1", "Papa", -0.1), 0.6)
        if kk > 0.003:
            icons.draw_icon(f, "keys", dx + DOC_W / 2 - 150, dy - DOC_H / 2 + 120, size=150 * (0.85 + 0.15 * ease_out(kk)), metal="gold", alpha=kk, glow=0.18 * kk, shadow=True)
    # Latince satır (yakın plan)
    if phase == "satir":
        ya = dy + 6
        t_l = cx.at(line_at) if line_at is not None else 0.4
        xs = dx - 470
        K2.write_line(f, cx, LAT_PHRASE, xs, ya, t_l, face="fell_i", size=62, color="#2A180D", alpha=1.0, dur=1.9, seed=71)
        # vurgu çizgisi (sinabar) — 'üslupla'
        kh = clamp((t - (t_l + 2.0)) / 0.7)
        if kh > 0:
            wl = sk.text_width(LAT_PHRASE, "fell_i", 62)
            pl = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.4, Color=C("#A8321E", int(235 * kh)), StrokeCap=skia.Paint.kRound_Cap)
            pl.setPathEffect(skia.DiscretePathEffect.Make(14.0, 1.1, 5))
            c.drawLine(xs, ya + 16, xs + wl * ease_io(kh, 1.6), ya + 16, pl)
        if tr_at is not None:
            kt = cx.amt(tr_at, 0.7)
            if kt > 0:
                CM.ink(f, "kötülüğün oğlu ve yıkımın evladı", dx, ya + 112, face="cap_i", size=50, color="#6A1E14", align="c", alpha=kt, emboss=False)
    # mum mührü (af)
    if phase == "af" and seal_at is not None:
        ks = clamp((t - cx.at(seal_at)) / 0.45)
        CM.wax_seal(f, dx + DOC_W / 2 - 150, dy + DOC_H / 2 - 120, 70, "#A52A1C", alpha=1.0, t=ks, palle=True)
    # bulla
    t_drop = cx.at(drop_at) if drop_at is not None else None
    if phase == "giris":
        bx, by = draw_bulla(f, cx, t_imp)
        draw_dies(f, cx, t_imp, BULLA_REST[0], BULLA_REST[1] - 8)
    else:
        r_ = draw_bulla(f, cx, -9.0, drop_t=t_drop)
    c.restore()
    cam.end(f)
    L_ = None
    if night:
        CM.finish(f, cx, motes_n=26, light=CM.candle_light(t, seed, base=(W * 0.5, H * 0.46), r=1250.0, sway=14.0))
    else:
        CM.finish(f, cx, motes_n=22)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ interdikt bindirmesi: kurşun mühür şehri örter ═══════════════════════════
def interdikt(at, stamp_at, dur=1.2, cxy=(960.0, 560.0), r1=620.0):
    """Skyline üstüne: büyük kurşun mühür gölgesi şehri örter (halka + haç), şehir kararır; `İNTERDİKT` damgası vurur."""
    def fn(cx):
        k = cx.amt(at, dur, ease=lambda u: ease_out(u, 3))
        if k <= 0.003:
            return
        f = cx.f
        c = f.c
        x, y = cxy
        r = lerp(r1 * 0.35, r1, k)
        sh = skia.GradientShader.MakeRadial((x, y), r, [C("#3A3E48", int(70 * k)), C("#3A3E48", int(120 * k)), C("#1E2026", int(200 * k)), C("#1E2026", 0)], [0.0, 0.6, 0.92, 1.0])
        c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Shader=sh))
        for rr, ww, aa in ((r * 0.96, 10, 0.55), (r * 0.80, 4, 0.40), (r * 0.52, 3, 0.35)):
            c.drawCircle(x, y, rr, S("#B8BCC6", ww, int(255 * aa * k)))
        arm = r * 0.17
        for dx, dy in ((1, 0), (0, 1)):
            c.drawLine(x - dx * arm, y - dy * arm, x + dx * arm, y + dy * arm, S("#B8BCC6", 12, int(150 * k)))
        # yasak: üstte dönen kesik halka (sessizlik)
        ph = cx.t * 0.25
        pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.0, Color=C("#C8CCD6", int(110 * k)))
        pa.setPathEffect(skia.DashPathEffect.Make([16.0, 20.0], -cx.t * 18))
        c.drawCircle(x, y, r * 0.66, pa)
        ks = cx.amt(stamp_at, 0.3)
        if ks > 0.003:
            CM.stamp(f, "İNTERDİKT", x, y + r * 0.14, rot=-0.07, size=78, color="#C9D2E6" if not TH.day else None, alpha=1.0, t=ks)
    return fn


# ═══════════════════════════ c8_kasa: hazine boşalıyor ═══════════════════════════
@CM.ckind("c8_kasa")
def k_kasa(cx, close_at=None, ovl=None, seed=3, **_):
    """Demir bantlı sandık: sikke yığını erir, sikkeler yay çizerek dışarı (sola) uçar; sonunda kapak çarpar (toz + sarsıntı)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    tc = cx.at(close_at) if close_at is not None else cx.dur - 0.5
    sx_, sy_ = _shake(t - tc, amp=10.0)
    c.save()
    c.translate(sx_, sy_)
    bx0, bx1, by0, by1 = 730.0, 1190.0, 650.0, 880.0
    hy_ = 612.0                                                  # menteşe
    # zemin gölgesi
    SOFT(c, 960, by1 + 14, 330, 34, "#000000", 120)
    # arka duvar parıltısı (sikke ışığı)
    h_lvl = clamp(1.0 - ease_io(clamp((t - 0.15) / max(0.5, tc - 0.15 - 0.3)), 1.4) * 0.97)
    SOFT(c, 960, by0 - 40, 520, 260, "#FFD27A", 70 * (0.3 + 0.7 * h_lvl))
    # kapak (açık): arkada
    k_lid = ease_in(clamp((t - tc) / 0.28), 2.4)
    yf = lerp(402.0, by0 - 6.0, k_lid)
    xf0, xf1 = lerp(762.0, 722.0, k_lid), lerp(1158.0, 1198.0, k_lid)
    lid = sk.poly_path([(bx0 + 36, hy_), (bx1 - 36, hy_), (xf1, yf), (xf0, yf)])
    c.drawPath(lid, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, yf), (0, hy_)], [C("#7A4C26"), C("#5A3418")], [0, 1])))
    c.drawPath(lid, S("#1E1008", 2.4, 230))
    if k_lid < 0.9:
        for xb in (860, 1060):
            c.drawLine(xb + (xf0 - 762) * 0.2, yf + 6, xb, hy_ - 4, S("#2A2C32", 12, 230, cap=False))
    # gövde içi (karanlık ağız)
    c.drawOval(skia.Rect.MakeLTRB(bx0 + 14, by0 - 36, bx1 - 14, by0 + 36), P("#120B06"))
    # sikke yığını (gövde ağzında yükselen tepecik)
    rs = np.random.RandomState(seed)
    n = 170
    coins = sorted(((rs.rand(), rs.rand(), rs.rand()) for _ in range(n)), key=lambda q: q[1])
    for (a_, b_, thr) in coins:
        if thr > h_lvl:
            continue
        w_ = (bx1 - bx0 - 80) * 0.5 * (1.0 - b_ ** 1.5 * 0.0)
        px = 960 + (a_ - 0.5) * 2 * w_ * (1.0 - 0.75 * (1 - b_) ** 1.0 * (1 - h_lvl * 0.2))
        py = by0 - 6 - (1 - b_) * 150 * h_lvl * (1 - abs(a_ - 0.5) * 1.35) - 6
        L.coin_flat(c, px, py, r=15 + 3 * b_)
    # gövde ön yüz
    body = skia.Rect.MakeLTRB(bx0, by0, bx1, by1)
    c.drawRect(body, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, by0), (0, by1)], [C("#8A5A30"), C("#5A3418")], [0, 1])))
    for i in range(6):
        yy = by0 + 10 + i * 36
        c.drawLine(bx0, yy, bx1, yy + rs.uniform(-1.5, 1.5), S("#2A1608", 1.4, 90))
    c.drawRect(body, S("#1E1008", 2.6, 235, cap=False))
    for xb in (bx0 + 38, bx1 - 38):
        c.drawRect(skia.Rect.MakeLTRB(xb - 15, by0, xb + 15, by1), P("#3A3C44"))
        c.drawRect(skia.Rect.MakeLTRB(xb - 15, by0, xb + 15, by1), S("#0E0F12", 1.6, 220, cap=False))
        for yb in (by0 + 30, by0 + 110, by1 - 26):
            c.drawCircle(xb, yb, 4.0, P("#9AA0AA"))
    c.drawRect(skia.Rect.MakeLTRB(bx0, by0 + 22, bx1, by0 + 46), P("#3A3C44"))
    c.drawRect(skia.Rect.MakeLTRB(bx0, by0 + 22, bx1, by0 + 46), S("#0E0F12", 1.4, 200, cap=False))
    # kilit plakası
    c.drawRoundRect(skia.Rect.MakeLTRB(930, by0 + 14, 990, by0 + 94), 8, 8, P("#B08828"))
    c.drawRoundRect(skia.Rect.MakeLTRB(930, by0 + 14, 990, by0 + 94), 8, 8, S("#3A2A08", 2.0, 230))
    c.drawCircle(960, by0 + 50, 8.0, P("#1A1208"))
    # uçan sikkeler (sola yay)
    nf = 30
    for i in range(nf):
        t0 = 0.10 + i * (max(0.8, tc - 0.45) / nf) * 0.92
        u = t - t0
        if u < 0 or u > 1.5:
            continue
        r2 = np.random.RandomState(100 + i)
        vx = -(260 + r2.rand() * 380)
        vy = -(520 + r2.rand() * 340)
        xx = 960 + (r2.rand() - 0.5) * 200 + vx * u
        yy = by0 - 40 + vy * u + 0.5 * 1500 * u * u
        a_ = clamp(1.0 - max(0.0, u - 1.0) / 0.5)
        sq = abs(math.cos(u * (7 + r2.rand() * 4)))
        c.save()
        c.translate(xx, yy)
        c.scale(1.0, 0.35 + 0.65 * sq)
        L.coin_flat(c, 0, 0, r=16, a=int(255 * a_))
        c.restore()
    # çarpma tozu
    uu = t - tc - 0.26
    if 0 < uu < 0.9:
        for i in range(14):
            r3 = np.random.RandomState(500 + i)
            ang = r3.rand() * math.pi
            dd = (50 + 160 * r3.rand()) * ease_out(clamp(uu / 0.9), 2)
            SOFT(c, 960 + math.cos(ang) * dd * (1 if i % 2 else -1), by0 - 14 - math.sin(ang) * dd * 0.35, 30 + 20 * uu, 22 + 12 * uu, "#CBB894", 90 * (1 - clamp(uu / 0.9)))
    c.restore()
    cam.end(f)
    CM.finish(f, cx, motes_n=20, light=CM.candle_light(t, seed, base=(960, 640), r=1300.0, sway=12.0) if not TH.day else None)
    if ovl is not None:
        ovl(cx)
