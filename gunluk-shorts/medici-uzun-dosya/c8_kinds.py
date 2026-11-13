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


# ═══════════════════════════ takvim yaprağı (bindirme) ═══════════════════════════
def calendar_flip(at, n0, n1, month="ARALIK", x=300.0, y=560.0, dt=0.23, out=None, size=210.0):
    """Yaprak takvim: `at` çapasından başlayıp her `dt` sn'de bir yaprak çevrilir (n0 → n1). Gün sayısı dev Cinzel; üstte ay."""
    def fn(cx):
        t0 = cx.at(at)
        k_in = clamp((cx.t - t0 + 0.4) / 0.4)
        if out is not None:
            k_in *= 1.0 - cx.amt(out, 0.5)
        if k_in <= 0.003:
            return
        f = cx.f
        c = f.c
        n_steps = n1 - n0
        u = (cx.t - t0) / dt
        idx = int(clamp(math.floor(u), 0, n_steps))
        frac = u - math.floor(u) if 0 <= u < n_steps else 1.0
        w, h = size * 1.0, size * 1.12
        c.save()
        c.translate(x, y)
        a = k_in
        f.rrect(-w / 2 + 6, -h / 2 + 12, w, h, 12, color="#000000", alpha=0.35 * a, blur=10)
        # alttaki (sonraki) yaprak
        def page(num, sy=1.0, top=True, al=1.0):
            c.save()
            c.translate(0, -h / 2 if top else 0)
            if top:
                c.scale(1.0, max(0.02, sy))
                c.translate(0, 0)
            f.rrect(-w / 2, 0 if top else -h / 2 + 0, w, h, 12, shader=f.lin(0, 0, 0, h, [("#F6EEDB", 0.0), ("#E6D8B6", 1.0)]), alpha=a * al)
            f.rrect(-w / 2, 0, w, 46, 12, color="#A8321E", alpha=a * al)
            CM.ink(f, month, 0, 33, face="title_m", size=26, color="#F6EEDB", align="c", track=8, alpha=a * al, emboss=False)
            CM.ink(f, str(num), 0, h * 0.74, face="title", size=96, color="#2A1A0C", align="c", track=2, alpha=a * al, emboss=False)
            c.restore()
        cur = n0 + idx
        nxt = min(n1, cur + 1)
        if idx < n_steps and 0 <= u < n_steps and 0.0 < frac < 1.0:
            page(nxt)                                   # altta sonraki gün
            # üstteki yaprak öne doğru yatıp kaybolur
            sy = max(0.02, 1.0 - ease_in(clamp(frac / 0.8), 2))
            page(cur, sy=sy, al=1.0 - ease_in(clamp((frac - 0.6) / 0.4), 2) * 0.0)
        else:
            page(min(n1, n0 + idx) if u >= 0 else n0)
        # halka (spiral) üst
        for i in range(5):
            xx = -w / 2 + 28 + i * (w - 56) / 4
            c.drawCircle(xx, -h / 2 - 2, 7.0, P("#2A2C32", int(255 * a)))
        c.restore()
    return fn


# ═══════════════════════════ date strip: Napoli şeridi (6 Aralık → 18 Aralık → 27 Şubat) ═══════════════════════════
def date_strip(at, marks, x0=330.0, x1=1590.0, y=830.0, fill_to=None, fill_dur=1.6, out=None, extra_marks=()):
    """Gün ölçekli şerit. marks=[(etiket, gün, çapa)]; fill_to=(gün, çapa) şerit bu güne kadar dolar. extra_marks=[(etiket, gün, çapa, renk)] sinabar damgalı iğne."""
    total = max(m[1] for m in marks)

    def X(d):
        return x0 + (x1 - x0) * d / total

    def fn(cx):
        k = cx.amt(at, 0.6)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.5)
        if k <= 0.003:
            return
        f = cx.f
        c = f.c
        col = TH.rule if TH.day else "#D8B25A"
        f.rrect(x0 - 40, y - 76, x1 - x0 + 80, 150, 14, color="#0A0C14" if not TH.day else "#EDE3C8", alpha=0.62 * k)
        c.drawLine(x0, y, x0 + (x1 - x0) * ease_out(k, 2), y, S(col, 5.0, int(240 * k)))
        if fill_to is not None:
            d_to, a_to = fill_to
            kf = ease_io(clamp((cx.t - cx.at(a_to)) / fill_dur))
            if kf > 0.002:
                f.rrect(x0, y - 9, (X(d_to) - x0) * kf, 18, 9, color=TH.acc if TH.day else "#C95A40", alpha=0.75 * k)
        for i_, (lab, d, an) in enumerate(marks):
            km = cx.amt(an, 0.45)
            if km <= 0.003:
                continue
            xx = X(d)
            c.drawLine(xx, y - 18 * km, xx, y + 18 * km, S(col, 3.0, int(250 * km)))
            f.circle(xx, y, 9 * km, color=TH.acc if TH.day else "#EDB968", alpha=km)
            up = (i_ % 2 == 0)
            CM.ink(f, lab, xx, y - 34 if up else y + 54, face="title_m", size=26, color=TH.fg, align="c" if 0 < i_ < len(marks) - 1 or True else "l", track=3, alpha=km, emboss=False)
        for lab, d, an, colr in extra_marks:
            km = cx.amt(an, 0.3)
            if km <= 0.003:
                continue
            xx = X(d)
            f.poly([(xx, y + 4), (xx - 11 * km, y + 34 * km), (xx + 11 * km, y + 34 * km)], color=colr, alpha=km)
            CM.ink(f, lab, xx, y + 66, face="title_m", size=28, color=colr, align="c", track=3, alpha=km, emboss=False)
    return fn


# ═══════════════════════════ c8_bargello: heyet gelir, takvim akar, pencere (beden YOK) ═══════════════════════════
BG_X0, BG_Y0 = 200.0, 300.0
BG_W, BG_H = 2320, 1500


@functools.lru_cache(maxsize=2)
def _bargello_bake():
    import cilt_oda as OD
    fr = sk.Frame(BG_W, BG_H)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    c.translate(BG_X0, BG_Y0)
    T = OD.OTint("day")
    GY = 900.0
    # gökyüzü (soğuk, bulutsuz)
    sh = skia.GradientShader.MakeLinear([(0, -300), (0, GY)], [C("#AFC0CE"), C("#D8DFE0"), C("#E9E4D4")], [0, 0.6, 1])
    c.drawRect(skia.Rect.MakeLTRB(-BG_X0, -BG_Y0, BG_W, GY), skia.Paint(Shader=sh))
    # uzak çatılar
    rs = np.random.RandomState(7)
    x = -200
    while x < 2200:
        w = rs.uniform(80, 170)
        h = rs.uniform(40, 120)
        c.drawRect(skia.Rect.MakeLTRB(x, GY - 120 - h, x + w, GY), P("#9AA4A8", 200))
        c.drawPath(sk.poly_path([(x - 6, GY - 120 - h), (x + w / 2, GY - 120 - h - 34), (x + w + 6, GY - 120 - h)]), P("#9C6A56", 170))
        x += w + rs.uniform(-8, 14)
    # ana duvar
    wx0, wx1, wy0 = 300.0, 1700.0, 250.0
    c.drawRect(skia.Rect.MakeLTRB(wx0, wy0, wx1, GY), P("#A39A86"))
    OD.ashlar(c, wx0, wx1, wy0, GY, T, col="#A39A86", course=70.0, seed=4)
    c.drawRect(skia.Rect.MakeLTRB(wx0, wy0, wx1, GY), S("#2A2418", 3.0, 230, cap=False))
    # yapı kuşağı (string course)
    c.drawRect(skia.Rect.MakeLTRB(wx0 - 8, 566, wx1 + 8, 590), P("#B8AE98"))
    c.drawRect(skia.Rect.MakeLTRB(wx0 - 8, 566, wx1 + 8, 590), S("#2A2418", 1.8, 210, cap=False))
    # taçlandırma: konsol/mazgal bandı + mazgal dişleri
    c.drawRect(skia.Rect.MakeLTRB(wx0 - 14, wy0 - 38, wx1 + 14, wy0 + 6), P("#8E8670"))
    for xx in np.arange(wx0 - 4, wx1, 58):
        c.drawPath(sk.poly_path([(xx, wy0 - 38), (xx + 40, wy0 - 38), (xx + 30, wy0 + 6), (xx + 10, wy0 + 6)]), P("#7A7360"))
    for xx in np.arange(wx0 - 14, wx1 + 14, 52):
        c.drawRect(skia.Rect.MakeLTRB(xx, wy0 - 104, xx + 32, wy0 - 38), P("#A39A86"))
        c.drawRect(skia.Rect.MakeLTRB(xx, wy0 - 104, xx + 32, wy0 - 38), S("#2A2418", 1.6, 220, cap=False))
    c.drawRect(skia.Rect.MakeLTRB(wx0 - 14, wy0 - 38, wx1 + 14, wy0 + 6), S("#2A2418", 2.0, 220, cap=False))
    # kule (sağ-orta), kendi mazgalı ile
    tx0, tx1, ty0 = 1360.0, 1580.0, -230.0
    c.drawRect(skia.Rect.MakeLTRB(tx0, ty0, tx1, wy0), P("#9C937F"))
    OD.ashlar(c, tx0, tx1, ty0, wy0, T, col="#9C937F", course=64.0, seed=9)
    c.drawRect(skia.Rect.MakeLTRB(tx0, ty0, tx1, wy0), S("#2A2418", 3.0, 230, cap=False))
    c.drawRect(skia.Rect.MakeLTRB(tx0 - 26, ty0 - 44, tx1 + 26, ty0 + 4), P("#8E8670"))
    for xx in np.arange(tx0 - 22, tx1 + 22, 46):
        c.drawRect(skia.Rect.MakeLTRB(xx, ty0 - 108, xx + 28, ty0 - 44), P("#A39A86"))
        c.drawRect(skia.Rect.MakeLTRB(xx, ty0 - 108, xx + 28, ty0 - 44), S("#2A2418", 1.6, 220, cap=False))
    c.drawRect(skia.Rect.MakeLTRB(tx0 - 26, ty0 - 44, tx1 + 26, ty0 + 4), S("#2A2418", 2.0, 220, cap=False))
    for yy in (ty0 + 120, ty0 + 330):                    # kule yarıkları
        c.drawRect(skia.Rect.MakeLTRB((tx0 + tx1) / 2 - 9, yy, (tx0 + tx1) / 2 + 9, yy + 74), P("#14120E"))
    # pencereler (üst sıra) + alt sıra küçükler + kapı
    for xw in (480.0, 720.0, 960.0, 1200.0):
        OD.draw_window(c, T, xw, 330, 96, 180, night=False, arch=True, shutters=False, mullion=True, sill=True, stone=("#B8AE98", "#CFC6AE", "#C2B89F", "#9A9078"))
    for xw in (480.0, 720.0, 1200.0, 1440.0):
        OD.draw_window(c, T, xw, 650, 70, 110, night=False, arch=True, shutters=False, mullion=False, sill=True, stone=("#B8AE98", "#CFC6AE", "#C2B89F", "#9A9078"))
    # ana kapı (kemerli, derin söve)
    dx, dw, dh = 960.0, 210.0, 330.0
    pth = skia.Path()
    pth.moveTo(dx - dw / 2, GY)
    pth.lineTo(dx - dw / 2, GY - dh + dw / 2)
    pth.arcTo(skia.Rect.MakeLTRB(dx - dw / 2, GY - dh, dx + dw / 2, GY - dh + dw), 180, 180, False)
    pth.lineTo(dx + dw / 2, GY)
    pth.close()
    c.drawPath(pth, P("#2A1E12"))
    c.drawPath(pth, S("#6E6650", 12.0, 255, cap=False))
    c.drawPath(pth, S("#1A1408", 2.2, 230, cap=False))
    # zemin: kaldırım taşları (perspektif)
    sh2 = skia.GradientShader.MakeLinear([(0, GY), (0, GY + 400)], [C("#8E8A7C"), C("#6E6A5C")], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(-BG_X0, GY, BG_W, GY + 400), skia.Paint(Shader=sh2))
    c.drawLine(-BG_X0, GY, BG_W, GY, S("#2A2418", 2.4, 230))
    y, step = GY, 20.0
    while y < GY + 400:
        y += step
        step *= 1.2
        c.drawLine(-BG_X0, y, BG_W, y, S("#2A2418", 1.2, 80))
    for i in range(46):
        xx = -BG_X0 + i * 70.0
        c.drawLine(xx, GY, xx + (xx - 960) * 0.55, GY + 400, S("#2A2418", 1.0, 55))
    return fr.surf.makeImageSnapshot()


KEY_WIN = (1200.0, 330.0 + 90.0)      # önemli pencerenin merkezi (dünya)


def _textile(f, x, y, w, h, a=1.0, t=0.0):
    """Doğu kumaşı örnek şeridi (kaftan deseni): kırmızı zemin, altın ogival kafes, lapis/beyaz nar dolgusu."""
    c = f.c
    c.save()
    c.translate(x, y)
    f.rrect(-w / 2 + 6, -h / 2 + 12, w, h, 10, color="#000000", alpha=0.35 * a, blur=10)
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, h / 2), 10, 10)
    c.drawRRect(rr, P("#8E2A22", int(255 * a)))
    c.save()
    c.clipRRect(rr, skia.ClipOp.kIntersect, True)
    sp = 86.0
    for j in range(-3, 4):
        for i in range(-8, 9):
            px = i * sp + (sp / 2 if j % 2 else 0)
            py = j * sp * 0.62
            og = skia.Path()
            og.moveTo(px, py - 36)
            og.quadTo(px + 30, py - 8, px, py + 36)
            og.quadTo(px - 30, py - 8, px, py - 36)
            c.drawPath(og, S("#E0B84E", 3.0, int(255 * a)))
            c.drawCircle(px, py, 8.0, P("#233C8C", int(255 * a)))
            c.drawCircle(px, py - 20, 4.5, P("#F4E4B0", int(240 * a)))
    sh = skia.GradientShader.MakeLinear([(0, -h / 2), (0, h / 2)], [C("#FFFFFF", int(36 * a)), C("#000000", int(70 * a))], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, h / 2), skia.Paint(Shader=sh))
    c.restore()
    c.drawRRect(rr, S("#E0B84E", 5.0, int(255 * a)))
    c.drawRRect(rr, S("#2A1A0C", 1.6, int(220 * a)))
    c.restore()


@CM.ckind("c8_bargello")
def k_bargello(cx, arrive_at=None, flip_at=None, win_at=None, shade_at=None, cloth_at=None, ovl=None, seed=3, **_):
    """Bargello cephesi (soğuk gün): Floransa heyeti sağdan sola gelir (24 Aralık); takvim 24→29; pencere (içi kararır; BEDEN YOK); Doğu giysisi kumaş örneği."""
    import cilt_anim as FA
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    f.clear("#AFC0CE")
    cam.begin(f)
    c = f.c
    t = cx.t
    c.drawImage(_bargello_bake(), -BG_X0, -BG_Y0, CM._LIN)
    GY = 900.0
    # kuşlar / bayrak yok; duman: kulenin yanında ince baca dumanı yok (kaynaksız ayrıntı)
    ta = cx.at(arrive_at) if arrive_at is not None else 0.0
    # heyet: sağdan sola yürür, kapı önünde durur
    cast = [("soylu", 41, dict(robe="#7A2A22", robe2="#C79A3C", hat_col="#2A1A10"), None), ("banker", 42, dict(robe="#2F5A8A", robe2="#E0B84E", hat_col="#8A2A1E"), None),
            ("asker", 43, {}, "halberd"), ("tuccar", 44, dict(robe="#4A5A3A", robe2="#B08828"), None), ("asker", 45, {}, "halberd"), ("halk", 46, dict(robe="#6A4A2A"), None)]
    for i, (kd, sd, st, prop) in enumerate(cast):
        x_start = 1980.0 + i * 78.0
        x_stop = 1180.0 - i * 20.0 + (i % 2) * 40.0
        sp = 170.0
        tt = t - (ta - 0.15)
        x = max(x_stop, x_start - sp * max(0.0, tt + i * 0.0))
        moving = x > x_stop + 0.6
        y = GY + 46 + (i % 3) * 12
        hh = 178 - (i % 3) * 6
        try:
            if moving:
                FA.walker(f, kd, x, y, hh, t, speed=sp, dir=-1, phase=0.17 * i, seed=sd, prop=prop, **st)
            else:
                FA.actor(f, kd, x, y, hh, t, action="idle" if i % 2 else "talk", dir=-1, seed=sd, phase=0.17 * i, prop=prop, **st)
        except Exception:
            pass
    # pencere: iç kararır (BEDEN YOK) — kapanan panjur + soğuk gölge
    if win_at is not None:
        kw = cx.amt(win_at, 0.5)
        wx, wy = KEY_WIN
        if kw > 0.003:
            f.rrect(wx - 46, wy - 80, 92, 168, 40, color="#0C1018", alpha=0.0)
            # önemli pencereyi vurgulayan soğuk ışık halkası
            SOFT(c, wx, wy, 140 * kw, 190 * kw, "#9FB4D8", 70 * kw)
    if shade_at is not None:
        ks = ease_in(cx.amt(shade_at, 0.7), 2)
        wx, wy = KEY_WIN
        if ks > 0.003:
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(wx - 46, wy - 84, wx + 46, wy - 84 + 172 * ks))
            c.drawRect(skia.Rect.MakeLTRB(wx - 50, wy - 90, wx + 50, wy + 90), P("#10131C"))
            c.restore()
            # cephe boyunca ağır soğuk gölge (yukarıdan aşağı)
            sh = skia.GradientShader.MakeLinear([(wx, wy - 80), (wx + 300, wy + 520)], [C("#0A0E18", int(110 * ks)), C("#0A0E18", 0)], [0, 1])
            c.drawPath(sk.poly_path([(wx - 60, wy - 90), (wx + 60, wy - 90), (wx + 420, wy + 560), (wx + 160, wy + 560)]), skia.Paint(Shader=sh, AntiAlias=True))
    cam.end(f)
    f.rect(0, 0, W, H, color="#7C8EAE", alpha=0.07)
    CM.finish(f, cx, motes_n=16)
    if cloth_at is not None:
        kc = cx.amt(cloth_at, 0.7)
        if kc > 0.003:
            _textile(f, 1330, 790 + (1 - kc) * 120, 600, 180, a=kc, t=t)
            CM.tablet(f, 1330 - 210, 790 - 150 + (1 - kc) * 120, 420, 62, alpha=kc, corner=8)
            CM.ink(f, "DOĞU GİYSİLERİ", 1330, 790 - 150 + (1 - kc) * 120 + 43, face="title_m", size=30, color=TH.fg, align="c", track=7, alpha=kc, emboss=False)
    if ovl is not None:
        ovl(cx)


def late_scroll(at, x, y, size=150.0, out=None):
    """Yetki geç gelir: tomar yukarıdan düşer (sekme), mühür sonradan basılır (usul mizahı)."""
    def fn(cx):
        u = (cx.t - cx.at(at)) / 0.75
        if u <= 0:
            return
        f = cx.f
        e = clamp(u)
        drop = (1 - ease_out(e, 3)) * 420.0
        bounce = 14.0 * math.sin(clamp((u - 1.0) / 0.35) * math.pi) * (1 - clamp((u - 1.0) / 0.35)) if u > 1.0 else 0.0
        a = 1.0 - (cx.amt(out, 0.5) if out is not None else 0.0)
        icons.draw_icon(f, "scroll", x, y - drop - bounce, size=size, metal="gold", alpha=a * clamp(u * 4), glow=0.0, shadow=True, rot=-8.0 * (1 - e))
        if u > 1.15:
            CM.wax_seal(f, x + size * 0.30, y + size * 0.28 - bounce, 34, "#A52A1C", alpha=a, t=clamp((u - 1.15) / 0.35), palle=True)
    return fn


def question(at, x, y, size=260.0, out=None):
    """Büyük altın soru işareti (bilmiyoruz): belirir, hafif nefes alır."""
    def fn(cx):
        k = cx.amt(at, 0.5, ease=lambda u: sk.back_out(u))
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.5)
        if k <= 0.003:
            return
        icons.draw_icon(cx.f, "question", x, y + 6 * math.sin(cx.t * 2.2), size=size * (0.85 + 0.15 * min(1.0, k)) * (1 + 0.02 * math.sin(cx.t * 3)), metal="gold", alpha=clamp(k), glow=0.25 * k, shadow=True)
    return fn


# ═══════════════════════════ c8_leonardo: defter sayfası; giysi etüdü (beden YOK), satır satır not ═══════════════════════════
def _stroke_pts(pts, t=0.5):
    return sk.smooth_path(pts, False, t)


def _mirror(pts):
    return [(-x, y) for x, y in pts]


_GARMENT = [
    ("neck", [(-42, -236), (0, -214), (42, -236)]),
    ("shL", [(-42, -236), (-125, -222), (-172, -120), (-206, 30), (-230, 98)]),
    ("shR", _mirror([(-42, -236), (-125, -222), (-172, -120), (-206, 30), (-230, 98)])),
    ("cuffL", [(-230, 98), (-182, 112), (-150, 102)]),
    ("cuffR", _mirror([(-230, 98), (-182, 112), (-150, 102)])),
    ("inL", [(-150, 102), (-138, 12), (-112, -78), (-98, -132)]),
    ("inR", _mirror([(-150, 102), (-138, 12), (-112, -78), (-98, -132)])),
    ("bodyL", [(-98, -132), (-114, 40), (-142, 170), (-166, 264)]),
    ("bodyR", _mirror([(-98, -132), (-114, 40), (-142, 170), (-166, 264)])),
    ("hem", [(-166, 264), (-60, 280), (60, 280), (166, 264)]),
    ("front", [(-8, -216), (10, -100), (-4, 60), (12, 270)]),
    ("sash1", [(-106, -14), (0, 4), (106, -14)]),
    ("sash2", [(-104, 8), (0, 24), (104, 8)]),
    ("f1", [(-70, 30), (-76, 130), (-92, 258)]),
    ("f2", [(-34, 34), (-38, 140), (-42, 268)]),
    ("f3", [(40, 34), (46, 140), (52, 268)]),
    ("f4", [(78, 30), (88, 130), (104, 256)]),
    ("sl1", [(-196, 40), (-172, 70), (-168, 100)]),
    ("sl2", [(196, 40), (172, 70), (168, 100)]),
]


@CM.ckind("c8_leonardo")
def k_leonardo(cx, draw_at=None, notes_at=None, ovl=None, seed=21, **_):
    """Defter sayfası (kâğıt sarısı): kalem kıyafet etüdünü çizgi çizgi çizer (omuz, kol, etek, kuşak, kıvrımlar); sağ kenarda `satır satır` not (okunmaz) + renk lekeleri. BEDEN YOK."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    PW, PH = 1000, 720
    pg = PP.paper_image(PW, PH, seed, (240, 226, 178), "deckle", (("v", 0.5),), 44, 1.0)
    cxp, cyp = 960.0, 540.0
    pg.draw(f, cxp, cyp, rot=-0.02, shadow=0.65)
    t0 = cx.at(draw_at) if draw_at is not None else 0.5
    t_notes = cx.at(notes_at) if notes_at is not None else t0 + 2.2
    c.save()
    c.translate(cxp - 40, cyp + 12)
    c.rotate(math.degrees(-0.02))
    ink = "#3A2412"
    # türban etüdü (sol üst; küçük): sarmal şeritler
    kt = clamp((t - (t0 - 0.2)) / 0.9)
    if kt > 0:
        px, py = -330.0, -170.0
        for i in range(6):
            u = clamp(kt * 1.4 - i * 0.12)
            if u <= 0:
                continue
            rr = 44 - i * 4
            pth = skia.Path()
            pth.addOval(skia.Rect.MakeLTRB(px - rr * 1.15, py - 52 + i * 12, px + rr * 1.15, py - 52 + i * 12 + rr * 0.9))
            pm = skia.PathMeasure(pth, False)
            seg = skia.Path()
            pm.getSegment(0, pm.getLength() * u, seg, True)
            c.drawPath(seg, S(ink, 2.0, 190))
    # kıyafet çizgileri
    tip = None
    dts = [0.0, 0.16, 0.16, 0.12, 0.12, 0.12, 0.12, 0.20, 0.20, 0.28, 0.26, 0.20, 0.20, 0.24, 0.24, 0.24, 0.24, 0.10, 0.10]
    tt = t0
    for i, (nm, pts) in enumerate(_GARMENT):
        du = 0.34 if nm not in ("hem", "front") else 0.5
        if nm.startswith("f") and nm[1:].isdigit():
            du = 0.4
        u = clamp((t - tt) / du)
        tt += du * 0.78
        if u <= 0:
            continue
        pth = _stroke_pts(pts)
        pm = skia.PathMeasure(pth, False)
        Lg = pm.getLength()
        seg = skia.Path()
        pm.getSegment(0, Lg * ease_io(u, 1.4), seg, True)
        w = 3.0 if nm in ("shL", "shR", "bodyL", "bodyR", "hem", "neck") else (2.2 if nm.startswith(("sash", "front", "cuff", "in")) else 1.7)
        c.drawPath(seg, S(ink, w, 235))
        if 0 < u < 1:
            pos, _ = pm.getPosTan(Lg * ease_io(u, 1.4))
            if pos is not None:
                tip = (pos.x(), pos.y())
    # tarama (gölge çizgileri): sol iç yüzeyde kısa çapraz çizgiler
    kh = clamp((t - (t0 + 2.4)) / 1.0)
    if kh > 0:
        for i in range(int(22 * kh)):
            y = -100 + i * 14
            xs0 = -92 - 8 * math.sin(i * 0.7)
            c.drawLine(xs0, y, xs0 + 34 + 8 * math.sin(i), y + 16, S(ink, 1.3, 140))
    # notlar: satır satır (okunmaz), satır başında renk lekesi
    cols = ["#A8321E", "#233C8C", "#C79A3C", "#3E7A5A", "#8E2A1E"]
    last_end = None
    for i in range(6):
        ti = t_notes + i * 0.42
        kk = clamp((t - ti) / 0.5)
        if kk <= 0:
            continue
        yy = -190 + i * 66
        f.circle(262, yy - 6, 9.0 * min(1.0, kk * 3), color=cols[i % len(cols)], alpha=0.9)
        e = scribble(c, 290, 470, yy, ease_io(kk, 1.3), seed=seed * 5 + i, a=200, amp=3.4)
        if 0 < kk < 1:
            last_end = e
    c.restore()
    # kalem: uç noktası (dünya → ekran)
    pen = None
    if last_end is not None:
        pen = (cxp - 40 + last_end[0], cyp + 12 + last_end[1])
    elif tip is not None:
        pen = (cxp - 40 + tip[0], cyp + 12 + tip[1])
    if pen is not None:
        quill_at(f, pen[0], pen[1], a=1.0, ang=-58.0, t=t)
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=CM.candle_light(t, seed, base=(W * 0.5, H * 0.50), r=1250.0, sway=14.0) if not TH.day else None)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c8_baris: barış maddeleri (üç madde, simgeli, mühürlü) ═══════════════════════════
@CM.ckind("c8_baris")
def k_baris(cx, ovl=None, seed=17, **_):
    """Barış belgesi: başlık yaldızı sönükleşir ('parlak değildi'); üç madde tüy kalemle yazılır, solunda simge: taç (kralın takdiri), sikke+kum saati (süreli ödeme), anahtar+zincir (Pazzi'ler salıverilir); sonda mühür."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    PWd, PHd = 1260, 800
    pg = PP.paper_image(PWd, PHd, seed, (238, 226, 192), "deckle", (("h", 0.5),), 44, 1.0)
    dx, dy = 960.0, 540.0
    ka = cx.amt(("c8s22", -0.2), 0.8)
    pg.draw(f, dx, dy, rot=-0.008, shadow=0.6, alpha=ka)
    # başlık: yaldız → kurşun/kül tonu ('parlak değildi')
    kt = cx.amt(("c8s22", "Barış", -0.1), 0.8)
    fade = ease_io(cx.amt(("c8s22", "değildi;", -0.1), 1.2))
    if kt > 0.003:
        sp_g = CM.gilt("BARIŞ ŞARTLARI", "title", 64, 10.0)
        sp_d = CM.engraved("BARIŞ ŞARTLARI", "title", 64, 10.0, "#5A4E40")
        CM.draw_spr(f, sp_g, dx, dy - PHd / 2 + 118, "c", alpha=kt * (1 - fade))
        CM.draw_spr(f, sp_d, dx, dy - PHd / 2 + 118, "c", alpha=kt * fade)
    CM.flourish_rule(f, dx, dy - PHd / 2 + 150, 560, alpha=0.7 * kt, color="#7A5A2E", grow=kt)
    rows = [
        (dict(kind="crown", metal="gold"), "Alınan yerlerin akıbeti: kralın takdiri", ("c8s22", "savaşta", -0.3), 2.9, 380.0),
        (dict(kind="coins", metal="gold"), "Alfonso'ya süreli ödeme", ("c8s22", "Alfonso'ya", -0.3), 2.0, 560.0),
        (dict(kind="keys", metal="silver"), "Volterra'daki Pazzi'ler: salıverilme", ("c8s22", "Volterra'da", -0.3), 2.8, 740.0),
    ]
    xs = dx - PWd / 2 + 270
    last = None
    for i, (ic, txt, an, du, yy) in enumerate(rows):
        t0 = cx.at(an)
        kk = clamp((t - t0 + 0.2) / 0.5)
        if kk > 0:
            R_ = 62.0
            f.circle(dx - PWd / 2 + 130, yy - 30, R_ * 1.0, shader=f.rad(dx - PWd / 2 + 130, yy - 30, R_, [("#F4EAD0", 0.0, int(230 * kk)), ("#D8C7A0", 1.0, int(230 * kk))]))
            f.circle(dx - PWd / 2 + 130, yy - 30, R_, style="stroke", sw=3.0, color="#7A5A2E", alpha=kk)
            icons.draw_icon(f, ic["kind"], dx - PWd / 2 + 130, yy - 30, size=104 * (0.8 + 0.2 * ease_out(kk)), metal=ic["metal"], alpha=kk, shadow=True)
            if i == 1 and kk > 0.5:                       # süreli: kum saati
                icons.draw_icon(f, "hourglass", dx - PWd / 2 + 218, yy - 30, size=52, metal="gold", alpha=kk * 0.9, shadow=False)
        p, qx, qy = K2.write_line(f, cx, txt, xs, yy, t0, face="fell_i", size=50, color="#2A180D", alpha=ka, dur=du, seed=30 + i)
        if 0 < p < 1:
            last = (qx, qy)
        if i == 2 and p >= 1:                              # zincir kırılır: salıverilme
            kb = clamp((t - (t0 + du + 0.1)) / 0.6)
            if kb > 0:
                icons.draw_icon(f, "chains", dx + PWd / 2 - 150 + 22 * kb * math.sin(kb * 40) * (1 - kb), yy - 30, size=96 * (1 - 0.0 * kb), metal="silver", alpha=0.95 * (1 - ease_in(clamp((kb - 0.4) / 0.6), 2)), shadow=False)
    if last is not None:
        quill_at(f, last[0], last[1], a=1.0, t=t)
    # mühür
    ks = clamp((t - cx.at(("c8s22", "sayılır.", -0.2))) / 0.45)
    if ks > 0:
        CM.wax_seal(f, dx + PWd / 2 - 150, dy + PHd / 2 - 110, 66, "#A52A1C", alpha=1.0, t=ks, palle=True)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c8_konsey: Yetmişler Konseyi (70 iskemle sayılır; beş yıllık, iki kez yenilenir) ═══════════════════════════
def _chair(c, x, y, s=1.0, a=1.0, tone="#6E4524", seat="#8E2A30"):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawRect(skia.Rect.MakeLTRB(-20, -62, 20, -6), P(tone, int(255 * a)))                 # arkalık
    c.drawRect(skia.Rect.MakeLTRB(-20, -62, 20, -6), S("#1E1008", 1.6, int(220 * a), cap=False))
    c.drawRect(skia.Rect.MakeLTRB(-13, -52, 13, -16), P(mix(tone, "#000000", 0.25), int(220 * a)))
    c.drawRoundRect(skia.Rect.MakeLTRB(-24, -8, 24, 8), 4, 4, P(seat, int(255 * a)))         # minder
    c.drawRoundRect(skia.Rect.MakeLTRB(-24, -8, 24, 8), 4, 4, S("#1E1008", 1.4, int(220 * a)))
    for xx in (-20, 20):
        c.drawRect(skia.Rect.MakeLTRB(xx - 3, 8, xx + 3, 30), P(tone, int(255 * a)))
    c.restore()


@CM.ckind("c8_konsey")
def k_konsey(cx, ovl=None, seed=5, **_):
    """Signoria salonu: 70 iskemle tek tek açılır (sayaç 1→70); altta yıl cetveli 1480: beş yıllık dilim çizilir, 1485 ve 1490'da `YENİLENDİ` damgasıyla uzar."""
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="top")
    cam.begin(f)
    c = f.c
    t = cx.t
    col = TH.rule if TH.day else "#D8B25A"
    # başlık levhası
    kt = cx.amt(("c8s23", "Yetmişler", -0.15), 0.6)
    if kt > 0.003:
        wd = sk.text_width("YETMİŞLER KONSEYİ", "title", 46, 8) + 90
        CM.tablet(f, 960 - wd / 2, 150 - 6 + (1 - kt) * 12, wd, 86, alpha=kt, corner=10)
        CM.ink(f, "YETMİŞLER KONSEYİ", 960, 150 + 56 + (1 - kt) * 12, face="title", size=40, color=TH.fg, align="c", track=8, alpha=kt, emboss=False)
    # giriş: Lorenzo madalyası (Nisan 1480) → iskemleler açılırken küçülüp kaybolur
    ka_ = cx.amt(("c8s23", "Nisanda", -0.2), 0.7) * (1.0 - cx.amt(("c8s23", "Yetmişler", 0.2), 0.8))
    if ka_ > 0.003:
        CMD.draw_medal_b(f, "m_lorenzo", 960 - 380 * ease_io(cx.amt(("c8s23", "Yetmişler", 0.0), 0.8)), 520, 460 * (0.94 + 0.06 * ka_), "bronze", False, alpha=ka_, tilt=0.18 * math.sin(t * 0.8), glint=((t * 0.3) % 2.0) if (t * 0.3) % 2.0 < 1 else None, inscription=False, shadow=0.6)
    # iskemleler (10 × 7)
    t_i0 = cx.at(("c8s23", "Yetmişler", 0.0))
    nshow = 0
    for r in range(7):
        for k in range(10):
            idx = r * 10 + k
            ti = t_i0 + idx * 0.022
            u = clamp((t - ti) / 0.28)
            if u <= 0:
                continue
            nshow += 1
            sc = 0.55 + 0.45 * sk.back_out(u)
            x = 960 + (k - 4.5) * 100 + (r % 2) * 18
            y = 262 + r * 74
            _chair(c, x, y + 30, s=sc * 0.78, a=u)
    # sayaç
    if nshow > 0:
        sp = CM.gilt(str(nshow), "title", 88, 6.0) if not TH.day else CM.engraved(str(nshow), "title", 88, 6.0, TH.fg)
        CM.draw_spr(f, sp, 1620, 330, "c", alpha=clamp(nshow / 3.0), shadow=0.4)
    # yıl cetveli
    x0, x1, yy = 360.0, 1560.0, 860.0
    kr = cx.amt(("c8s23", "kurdurdu", -0.6), 0.7)
    if kr > 0.003:
        def X(yr):
            return x0 + (x1 - x0) * (yr - 1480) / 15.0
        f.rrect(x0 - 70, yy - 118, x1 - x0 + 140, 210, 16, color="#0A0C14" if not TH.day else "#EDE3C8", alpha=0.55 * kr)
        c.drawLine(x0, yy, x0 + (x1 - x0) * kr, yy, S(col, 5.0, int(240 * kr)))
        for yr in (1480, 1485, 1490):
            xx = X(yr)
            c.drawLine(xx, yy - 16, xx, yy + 16, S(col, 3.0, int(250 * kr)))
            CM.ink(f, str(yr), xx, yy + 62, face="title", size=34, color=TH.fg, align="c", track=4, alpha=kr, emboss=False)
        # beş yıllık dilimler
        for (ya, yb, an, lab, stamp_an) in ((1480, 1485, ("c8s23", "yıllığına", -0.1), "5 YIL", None), (1485, 1490, ("c8s23", "1485'te", 0.0), "", ("c8s23", "1485'te", 0.9)),
                                             (1490, 1495, ("c8s23", "1490'da", 0.0), "", ("c8s23", "yenilendi.", -0.1))):
            kb = ease_out(clamp((t - cx.at(an)) / 0.9), 3)
            if kb <= 0.003:
                continue
            xa, xb = X(ya), X(yb)
            xb2 = xa + (xb - xa) * kb
            f.rrect(xa, yy - 12, xb2 - xa, 24, 12, color=TH.acc if TH.day else "#C95A40", alpha=0.78)
            if lab and kb > 0.7:
                CM.ink(f, lab, (xa + xb) / 2, yy - 32, face="title_m", size=30, color=TH.acc if TH.day else "#F0B8A0", align="c", track=6, alpha=clamp((kb - 0.7) / 0.3), emboss=False)
            if stamp_an is not None:
                ks_ = cx.amt(stamp_an, 0.3)
                if ks_ > 0.003:
                    CM.stamp(f, "YENİLENDİ", (xa + xb) / 2, yy - 86, rot=-0.07, size=40, alpha=1.0, t=ks_)
    cam.end(f)
    CM.finish(f, cx, motes_n=20)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ madalya yardımcıları: Mehmed (stilize profil), ters yüz ═══════════════════════════
medal.PEOPLE.setdefault("m_mehmed", dict(nose=24, hook=4, brow=4, lip=2, lip2=3, chin=3, jaw=1.0, fore=1, age=0.5, jowl=0.1, neck=1.0,
                                          hair="none", hat="turban_big", beard="mustache", garment="kaftan", mouth_open=0.0, scale=0.98, dy=120))
import cilt_medal as CMD  # noqa: E402


def _icon_alpha(name, size):
    a = icons.icon_array(name, "bronze")[..., 3].astype(np.float32) / 255.0
    return cv2.resize(a, (size, size), interpolation=cv2.INTER_AREA)


@functools.lru_cache(maxsize=2)
def reverse_image(size=720):
    """Madalyanın ters yüzü (stilize): zafer arabası + iki at + araba üstünde oturan (yüzsüz) figür; altta alevli sandalye amblemi (Napoli krallarının). Dökme bronz + patina."""
    S_ = 1000
    Hh = np.zeros((S_, S_), np.float32)
    al = np.zeros((S_, S_), np.float32)
    sf = skia.Surface(S_, S_)
    c = sf.getCanvas()
    c.clear(skia.ColorBLACK)

    def gp(g, style="fill", w=1.0):
        p = skia.Paint(AntiAlias=True, Color=skia.Color(int(g), int(g), int(g), 255))
        if style == "stroke":
            p.setStyle(skia.Paint.kStroke_Style)
            p.setStrokeWidth(w)
            p.setStrokeCap(skia.Paint.kRound_Cap)
        return p
    cx_, R_ = S_ / 2, S_ * 0.47
    c.drawCircle(cx_, cx_, R_, gp(96))
    c.drawCircle(cx_, cx_, R_ - 14, gp(185, "stroke", 26))
    c.drawCircle(cx_, cx_, R_ * 0.90, gp(150, "stroke", 8))
    # araba: tekerlek (halka + kollar)
    c.save()
    c.translate(640, 520)
    c.scale(1.28, 1.28)
    c.translate(-640, -520)
    wx, wy, wr = 640, 590, 105
    c.drawCircle(wx, wy, wr, gp(215, "stroke", 20))
    c.drawCircle(wx, wy, 24, gp(240))
    for i in range(8):
        a_ = i * math.pi / 4
        c.drawLine(wx, wy, wx + math.cos(a_) * wr, wy + math.sin(a_) * wr, gp(210, "stroke", 9))
    # araba kasası
    body = skia.Path()
    body.moveTo(510, 520); body.lineTo(800, 520); body.cubicTo(830, 520, 840, 470, 820, 440); body.lineTo(780, 440); body.lineTo(780, 500); body.lineTo(540, 500); body.close()
    c.drawPath(body, gp(205))
    c.drawLine(510, 520, 470, 566, gp(195, "stroke", 14))                      # oka bağlanan
    # oturan figür (yüzsüz): sarık + gövde
    c.drawCircle(700, 355, 42, gp(230))
    c.drawOval(skia.Rect.MakeLTRB(656, 316, 746, 360), gp(240))
    tor = skia.Path()
    tor.moveTo(660, 500); tor.cubicTo(652, 430, 670, 392, 700, 392); tor.cubicTo(732, 392, 752, 430, 748, 500); tor.close()
    c.drawPath(tor, gp(222))
    # sancak
    c.drawLine(760, 500, 770, 290, gp(215, "stroke", 9))
    pen = skia.Path()
    pen.moveTo(770, 294); pen.lineTo(876, 314); pen.lineTo(770, 344); pen.close()
    c.drawPath(pen, gp(210))
    c.restore()
    arr = sf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)[..., 0].astype(np.float32) / 255.0
    Hh = arr
    # atlar (ikon alfasından): iki at, biri biraz geride
    ha = _icon_alpha("horse", 460)
    for (hx, hy, g) in ((250, 470, 0.92), (160, 520, 0.70)):
        y0, x0 = hy - 230, hx - 230
        ys, xs = max(0, y0), max(0, x0)
        ye, xe = min(S_, y0 + 460), min(S_, x0 + 460)
        sub = ha[ys - y0:ye - y0, xs - x0:xe - x0]
        Hh[ys:ye, xs:xe] = np.maximum(Hh[ys:ye, xs:xe], sub * g)
    # alevli sandalye amblemi (alt orta)
    sf2 = skia.Surface(S_, S_)
    c2 = sf2.getCanvas()
    c2.clear(skia.ColorTRANSPARENT)
    def wp(g, style="fill", w=1.0):
        p = skia.Paint(AntiAlias=True, Color=skia.Color(int(g), int(g), int(g), 255))
        if style == "stroke":
            p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(w); p.setStrokeCap(skia.Paint.kRound_Cap)
        return p
    ex, ey = 520, 790
    c2.drawRect(skia.Rect.MakeLTRB(ex - 54, ey - 50, ex + 54, ey - 26), wp(255))             # oturak
    c2.drawRect(skia.Rect.MakeLTRB(ex - 54, ey - 130, ex - 34, ey - 26), wp(255))            # arkalık direği
    c2.drawRect(skia.Rect.MakeLTRB(ex - 54, ey - 134, ex + 30, ey - 112), wp(255))
    for xx in (-46, 44):
        c2.drawRect(skia.Rect.MakeLTRB(ex + xx - 6, ey - 26, ex + xx + 6, ey + 24), wp(255))
    em = sf2.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)[..., 3].astype(np.float32) / 255.0
    Hh = np.maximum(Hh, em * 0.95)
    fl = _icon_alpha("b_flame", 230)
    y0, x0 = ey - 330, ex - 115
    Hh[y0:y0 + 230, x0:x0 + 230] = np.maximum(Hh[y0:y0 + 230, x0:x0 + 230], fl * 1.0)
    # dairesel alfa
    yy_, xx_ = np.mgrid[0:S_, 0:S_].astype(np.float32)
    alpha = np.clip((R_ - np.hypot(xx_ - cx_, yy_ - cx_)) * 0.9, 0, 1)
    Hh = Hh * alpha
    rgba = medal._relief_from_height(Hh, alpha, "bronze")
    rgb = rgba[..., :3].astype(np.float32)
    lum = rgb.mean(-1) / 255.0
    rs = np.random.RandomState(7)
    pat = np.clip((0.40 - lum) / 0.26, 0, 1)
    rgb = rgb * (1 - 0.34 * pat[..., None]) + np.array([62, 96, 82], np.float32) * 0.34 * pat[..., None]
    rgba[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    rgba = cv2.resize(rgba, (size, size), interpolation=cv2.INTER_AREA)
    return sk.np_to_image(rgba)


@functools.lru_cache(maxsize=2)
def reverse_shadow(size=720):
    sa = skia.Surface(size, size)
    ca = sa.getCanvas()
    ca.clear(skia.ColorTRANSPARENT)
    ca.drawCircle(size / 2, size / 2, size * 0.47, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    al = sa.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)[..., 3]
    return CM.blur_sil(al, 16.0, (14, 8, 2))


def draw_bow(f, x, y, s=1.0, a=1.0, sway=0.0):
    """Hediye fiyongu (kırmızı saten): iki kulak + düğüm + iki kuyruk."""
    c = f.c
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(sway))
    c.scale(s, s)
    col, dk = "#B3301F", "#6A160E"
    for sg in (-1, 1):
        p = skia.Path()
        p.moveTo(0, 0)
        p.cubicTo(sg * 40, -70, sg * 120, -80, sg * 118, -22)
        p.cubicTo(sg * 114, 22, sg * 40, 20, 0, 0)
        c.drawPath(p, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -70), (0, 20)], [C(mix(col, "#FFFFFF", 0.22), int(255 * a)), C(col, int(255 * a))], [0, 1])))
        c.drawPath(p, S(dk, 2.4, int(230 * a)))
        q = skia.Path()
        q.moveTo(0, 6)
        q.quadTo(sg * 46, 80, sg * 90, 142)
        q.lineTo(sg * 56, 152)
        q.quadTo(sg * 24, 90, 0, 22)
        c.drawPath(q, P(col, int(255 * a)))
        c.drawPath(q, S(dk, 2.2, int(230 * a)))
    c.drawOval(skia.Rect.MakeLTRB(-22, -16, 22, 22), P(mix(col, "#FFFFFF", 0.1), int(255 * a)))
    c.drawOval(skia.Rect.MakeLTRB(-22, -16, 22, 22), S(dk, 2.2, int(230 * a)))
    c.restore()


@CM.ckind("c8_madalya")
def k_madalya(cx, flip_at=None, flip_back_at=None, bow_at=None, castle_at=None, dim_at=None, tilt0=0.0, ovl=None, size=640, seed=2, show="obv", **_):
    """Mehmed madalyası: ön yüz (stilize profil, yüz iddiası yok) → döner → ters yüz (zafer arabası, alevli sandalye); fiyong + Napoli kalesi (olası saldırıya imâ); sonda söner ve ön yüze döner."""
    f = cx.f
    cam = CM.bgfill(f, cx, seed=seed % 3, cam=CM.Cam(cx, push=0.0, drift=(0.0, 0.0)), dress="top")
    cam.begin(f)
    c = f.c
    t = cx.t
    xc, yc = 960.0, 470.0
    # dönme açısı (0 = ön, π = ters)
    th = 0.0 if show == "obv" else math.pi
    if flip_at is not None:
        th = math.pi * ease_io(clamp((t - cx.at(flip_at)) / 1.1), 2) if show == "obv" else th
    if flip_back_at is not None:
        kb = ease_io(clamp((t - cx.at(flip_back_at)) / 1.1), 2)
        th = math.pi * (1.0 - kb) if (flip_at is not None or show != "obv") and kb > 0 else th
    cs = math.cos(th)
    front = cs >= 0
    sx = max(0.04, abs(cs))
    bob = math.sin(t * 1.3) * 5.0
    if castle_at is not None:
        kc0 = cx.amt(castle_at, 0.8)
        xc = lerp(960.0, 700.0, ease_io(kc0))
    c.save()
    c.translate(xc, yc + bob)
    c.scale(sx * (size / 720.0), size / 720.0)
    sp = skia.Paint(AntiAlias=True)
    sp.setAlphaf(0.6)
    if front:
        c.drawImage(CMD.medal_shadow("m_mehmed", "bronze", None, False, 720), -360 + 24, -360 + 38, CM._LIN, sp)
        c.drawImage(CMD.medal_img("m_mehmed", "bronze", None, False, 720), -360, -360, CM._LIN, skia.Paint(AntiAlias=True))
        img_for_gl = None
    else:
        c.drawImage(reverse_shadow(720), -360 + 24, -360 + 38, CM._LIN, sp)
        c.drawImage(reverse_image(720), -360, -360, CM._LIN, skia.Paint(AntiAlias=True))
    # parıltı
    gl = (t * 0.28 + 0.2) % 2.0
    if gl < 1.0 and sx > 0.5:
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(-340, -340, 340, 340))
        gx = -440 + 880 * gl
        shd = skia.GradientShader.MakeLinear([(gx - 90, -300), (gx + 90, 300)], [C("#FFFFFF", 0), C("#FFE6B0", 70), C("#FFFFFF", 0)], [0, 0.5, 1])
        c.drawCircle(0, 0, 330, skia.Paint(Shader=shd, AntiAlias=True))
        c.restore()
    c.restore()
    # fiyong ve etiket (ters yüz görünürken)
    if bow_at is not None and not front:
        kb = cx.amt(bow_at, 0.55, ease=lambda u: sk.back_out(u))
        if kb > 0.003:
            draw_bow(f, xc + 150 * sx, yc - 292 + bob, s=0.95 * min(1.0, kb), a=clamp(kb), sway=0.06 * math.sin(t * 2.4))
    # Napoli kalesi + kesikli ok (olası saldırıya imâ)
    if castle_at is not None:
        kc = cx.amt(castle_at, 0.8)
        if kc > 0.003:
            cxx, cyy = 1450.0, 640.0
            icons.draw_icon(f, "castle", cxx, cyy, size=250 * (0.85 + 0.15 * ease_out(kc)), metal="gold", alpha=kc, shadow=True)
            CM.tablet(f, cxx - 130, cyy + 150, 260, 66, alpha=kc, corner=8)
            CM.ink(f, "NAPOLİ", cxx, cyy + 196, face="title_m", size=34, color=TH.fg, align="c", track=8, alpha=kc, emboss=False)
            ka = clamp((t - cx.at(castle_at) - 0.4) / 1.0)
            if ka > 0:
                x_a, y_a = xc + 170, yc + 200
                x_b, y_b = cxx - 150, cyy - 20
                n = 26
                for i in range(int(n * ease_io(ka))):
                    u = i / n
                    if i % 2:
                        continue
                    px = lerp(x_a, x_b, u)
                    py = lerp(y_a, y_b, u) - 80 * math.sin(math.pi * u)
                    qx = lerp(x_a, x_b, (i + 1) / n)
                    qy = lerp(y_a, y_b, (i + 1) / n) - 80 * math.sin(math.pi * (i + 1) / n)
                    c.drawLine(px, py, qx, qy, S("#A8321E", 5.0, 230))
                if ka > 0.97:
                    f.poly([(x_b, y_b), (x_b - 26, y_b - 14), (x_b - 20, y_b + 16)], color="#A8321E", alpha=0.95)
    # karartma (öldü)
    if dim_at is not None:
        kd = cx.amt(dim_at, 1.4)
        if kd > 0.003:
            sh = skia.GradientShader.MakeRadial((xc, yc), 700, [C("#05060C", int(40 * kd)), C("#05060C", int(215 * kd))], [0.0, 1.0])
            c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=sh))
    cam.end(f)
    CM.finish(f, cx, motes_n=22)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c8_dokum: Bertoldo'nun atölyesi — bronz dökülür, kalıp açılır, profil belirir ═══════════════════════════
@CM.ckind("c8_dokum")
def k_dokum(cx, pour_at=None, open_at=None, ovl=None, seed=4, **_):
    """Atölye (gece, ocak ışığı): yan duran dökümcü siluet (çekiçle), kepçe eğilir, erimiş bronz akışı kalıbın hunisine; kalıp turuncudan soğur; kalıp ikiye açılınca Mehmed profilli madalya belirir."""
    import cilt_oda as OD
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    tp = cx.at(pour_at) if pour_at is not None else 1.0
    to = cx.at(open_at) if open_at is not None else tp + 3.0
    mx_, my_ = 1040.0, 600.0                         # kalıp merkezi
    R0 = 205.0
    # ocak (sol): kor yatağı + alev
    SOFT(c, 330, 840, 420, 200, "#FF8A2A", 120)
    SOFT(c, 330, 860, 250, 90, "#FFD27A", 130)
    for i in range(3):
        icons.draw_icon(f, "b_flame", 330 + (i - 1) * 90 + 8 * math.sin(t * 5 + i), 790 - 10 * math.sin(t * 6 + i * 2), size=150 + 22 * math.sin(t * 7 + i), metal="gold", alpha=0.95, glow=0.5, shadow=False)
    # tezgâh
    bench = skia.Rect.MakeLTRB(120, 800, 1820, 880)
    c.drawRect(bench, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 800), (0, 880)], [C("#7A4C26"), C("#4E2E14")], [0, 1])))
    c.drawRect(bench, S("#1E1008", 2.4, 230, cap=False))
    for xx in (220, 700, 1180, 1660):
        c.drawLine(xx, 880, xx - 8, 1010, S("#2A1608", 18, 255, cap=False))
    SOFT(c, mx_, 806, 300, 24, "#000000", 120)
    # dökümcü siluet (sol): çekiç
    OD.sil_actor(f, "tuccar", 560, 806, 330, t, action="work", dir=1, seed=3, color="#14100C", rim="#FF9A4A", rim_dir=-1, mode="strike", prop="hammer")
    # kalıp: kil ikili disk + huni
    kc = clamp((t - (tp + 1.0)) / 3.5)                # soğuma
    kfill = ease_io(clamp((t - tp) / 1.7), 1.5)       # dolum
    open_k = ease_io(clamp((t - to) / 0.9), 2)
    clay = "#6E4A32"
    hot = mix("#FF8A2A", "#7A2A10", ease_out(kc, 2))
    # madalya (kalıbın arkasında, açılınca görünür)
    if open_k > 0.002:
        sz = 0.62
        c.save()
        c.translate(mx_, my_)
        c.scale(sz, sz)
        p0 = skia.Paint(AntiAlias=True)
        p0.setAlphaf(clamp(open_k * 1.4))
        sp = skia.Paint(AntiAlias=True)
        sp.setAlphaf(0.5 * clamp(open_k * 1.4))
        c.drawImage(CMD.medal_shadow("m_mehmed", "bronze", None, False, 720), -360 + 26, -360 + 40, CM._LIN, sp)
        c.drawImage(CMD.medal_img("m_mehmed", "bronze", None, False, 720), -360, -360, CM._LIN, p0)
        # sıcak parlama (soğur)
        hot_a = clamp(0.55 * (1 - clamp((t - to) / 2.2)) * open_k)
        if hot_a > 0.01:
            c.drawCircle(0, 0, 330, P("#FF9A3A", int(255 * hot_a)))
        c.restore()
    for sgn in (-1, 1):
        sh = open_k * 280.0 * sgn
        c.save()
        c.translate(mx_ + sh, my_)
        clip = skia.Path()
        clip.addRect(skia.Rect.MakeLTRB(0 if sgn > 0 else -R0 - 40, -R0 - 40, R0 + 40 if sgn > 0 else 0, R0 + 40))
        c.clipPath(clip, skia.ClipOp.kIntersect, True)
        c.drawCircle(0, 0, R0, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((-60, -80), R0 * 1.4, [C(mix(clay, "#FFFFFF", 0.22)), C(clay), C(mix(clay, "#000000", 0.45))], [0, 0.55, 1])))
        c.drawCircle(0, 0, R0, S("#1E1008", 3.0, 235))
        c.drawCircle(0, 0, R0 * 0.82, S("#2A1608", 2.0, 120))
        # dolum parıltısı (alttan yükselen)
        if kfill > 0.01:
            c.save()
            c.clipPath(skia.Path.Circle(0, 0, R0 - 6), skia.ClipOp.kIntersect, True)
            lvl = R0 - 2 * R0 * kfill
            c.drawRect(skia.Rect.MakeLTRB(-R0, lvl, R0, R0), P(hot, int(150 * (1 - 0.65 * ease_out(kc, 2)))))
            c.drawCircle(0, 0, R0, P(hot, int(70 * (1 - ease_out(kc, 2)))))
            c.restore()
        c.restore()
    if open_k < 0.5:
        # huni (sprue)
        fun = sk.poly_path([(mx_ - 56, my_ - R0 - 78), (mx_ + 56, my_ - R0 - 78), (mx_ + 24, my_ - R0 + 4), (mx_ - 24, my_ - R0 + 4)])
        c.drawPath(fun, P(clay, int(255 * (1 - open_k * 2))))
        c.drawPath(fun, S("#1E1008", 2.6, int(235 * (1 - open_k * 2))))
        if kfill > 0.01:
            c.drawOval(skia.Rect.MakeLTRB(mx_ - 44, my_ - R0 - 92, mx_ + 44, my_ - R0 - 66), P(hot, int(240 * (1 - open_k * 2))))
    # kepçe + akış
    kt = ease_io(clamp((t - (tp - 0.8)) / 0.9), 2)
    ang = 38.0 * kt * (1 - ease_io(clamp((t - (tp + 1.9)) / 0.7), 2))
    px_, py_ = mx_ + 190.0, my_ - R0 - 330.0 + 60.0 * (1 - kt)
    if kt > 0.003 and open_k < 0.6:
        c.save()
        c.translate(px_, py_)
        c.rotate(-ang * 0.0)
        c.rotate(ang)
        c.drawLine(40, -10, 360, -230, S("#3A2A1C", 20, 255))                         # sap
        bowl = skia.Path()
        bowl.moveTo(-110, -20); bowl.cubicTo(-110, 52, -46, 76, 14, 76); bowl.cubicTo(70, 76, 108, 40, 108, -10); bowl.close()
        c.drawPath(bowl, P("#3A3C44"))
        c.drawPath(bowl, S("#0E0F12", 3.0, 235))
        c.drawOval(skia.Rect.MakeLTRB(-110, -34, 108, 6), P(mix("#FF8A2A", "#FFD27A", 0.4)))
        c.restore()
    # akış (huniye)
    if tp <= t <= tp + 2.0:
        ks = clamp((t - tp) / 0.25) * (1 - clamp((t - (tp + 1.6)) / 0.4))
        lipx, lipy = px_ - 100 * math.cos(math.radians(ang)) + 10, py_ + 50 * math.sin(math.radians(ang)) - 6
        top = (lipx, lipy)
        bot = (mx_, my_ - R0 - 78)
        pth = skia.Path()
        pth.moveTo(*top)
        n = 12
        for i in range(1, n + 1):
            u = i / n
            pth.lineTo(lerp(top[0], bot[0], u) + 5 * math.sin(t * 20 + u * 9) * (1 - u * 0.3), lerp(top[1], bot[1], u))
        c.drawPath(pth, S("#FF6A10", 16, int(255 * ks)))
        c.drawPath(pth, S("#FFD27A", 8, int(255 * ks)))
        c.drawPath(pth, S("#FFF4D0", 3, int(255 * ks)))
        CM.sparks(f, t, mx_, my_ - R0 - 80, n=14, seed=4, h=170, alpha=0.9 * ks)
    # duman (soğurken)
    if t > tp + 1.2 and open_k < 0.9:
        for i in range(5):
            ph = ((t - tp) * 0.35 + i * 0.2) % 1.0
            SOFT(c, mx_ + (i - 2) * 38 + 14 * math.sin(t + i), my_ - R0 - 60 - ph * 250, 34 + ph * 40, 40 + ph * 50, "#C9C0B0", 60 * (1 - ph))
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=CM.candle_light(t, seed, base=(W * 0.52, H * 0.55), r=1500.0, sway=10.0) if not TH.day else None)
    if ovl is not None:
        ovl(cx)


def icon_pop(kind, x, y, at, out=None, size=150.0, metal="gold", glow=0.2, rot=0.0, hold_bob=0.0):
    """Çapada beliren simge (geri-çıkış hareketi); out çapasında söner."""
    def fn(cx):
        k = cx.amt(at, 0.5, ease=lambda u: sk.back_out(u))
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.5)
        if k <= 0.003:
            return
        icons.draw_icon(cx.f, kind, x, y + hold_bob * math.sin(cx.t * 2.0), size=size * (0.7 + 0.3 * min(1.2, k)), metal=metal, alpha=clamp(k), glow=glow * clamp(k), rot=rot, shadow=True)
    return fn


def swords_to_laurel(at, x=960.0, y=470.0, size=520.0):
    """Kılıçlar (gümüş) solar, defne çelengi Medici armasını sarar (savaş → barış)."""
    def fn(cx):
        k = ease_io(clamp((cx.t - cx.at(at)) / 1.5))
        a_s = 1.0 - clamp(k * 1.6)
        if a_s > 0.01:
            icons.draw_icon(cx.f, "swords", x, y - 30 * k, size=size * (0.9 + 0.2 * k), metal="silver", alpha=a_s, glow=0.0, shadow=True)
        if k > 0.15:
            ka = clamp((k - 0.15) / 0.85)
            icons.draw_icon(cx.f, "laurel", x, y + 10, size=size * 1.18 * (0.85 + 0.15 * ka), metal="gold", alpha=ka, glow=0.25 * ka, shadow=True)
    return fn
