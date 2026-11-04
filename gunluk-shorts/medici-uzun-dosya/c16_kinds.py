"""c16_kinds — c16 «Hesap» özel çekim türleri (Parça 7 sahne yazarı). `scenes_c16.py` içinde import edilir; `@CM.ckind` ile kaydolur.
Ruh hâli: AĞIR giriş + hafif-kuşkucu orta (tez sorgusu, sağlamlık haritası) + SESSİZ kapanış. Dünya koordinatı = nötr kamerada ekran koordinatı (1920×1080).
Olgu disiplini: yüz yok (siluet/simge/levha), şiddet/ceset yok; ekrana yalnız script/brif sözcükleri yazılır (metinler sahne dosyasından parametreyle gelir).
Sağlamlık haritası = akışın İÇİNDE: `saglam_band` (üst HUD, her iddia kendi çekiminde şeride uçar) + `c16_saglam` (üç büyük şerit → HUD'a küçülür).
`mode`/`perde`/`sahne`-benzeri adlar ckind'e aittir: tür parametresi olarak `view`/`sc` kullanılır. Her tür `ovl=` kabul eder (ışıktan sonra çizilir).
"""
import math

import numpy as np
import skia

import cilt_medici as CM
import cilt_oda as OD
import icons
import p7_lib as L
import sk
import c14_kinds as K14
import cilt_props as CP
from c14_kinds import A, palle_mark, wood_floor, book_closed, card_pane
from cilt_medici import TH
from p7_lib import INK, P, S, SOFT, look, ov
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth

GOLD = "#D9A532"
LAPIS = "#3C62B8"
LAPIS_L = "#7EA0EC"
RED = "#B03020"
RED_L = "#E0583F"
LANES = [("SAĞLAM", GOLD), ("NİTELİKLİ", LAPIS), ("MİT", RED)]
BAND_X0, BAND_Y, BAND_LW, BAND_H, BAND_GAP = 140.0, 46.0, 370.0, 72.0, 16.0


# ═══════════════════════════ ortak: kalkan levha, çizim parçaları ═══════════════════════════
def blur_paint(col, a, r=6.0):
    p = skia.Paint(AntiAlias=True, Color=C(col, A(a)))
    p.setImageFilter(skia.ImageFilters.Blur(r, r))
    return p


def dash_paint(col, a, w, on=16.0, off=14.0, cap=True):
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, A(a)))
    if cap:
        p.setStrokeCap(skia.Paint.kRound_Cap)
    p.setPathEffect(skia.DashPathEffect.Make([on, off], 0.0))
    return p


def shield_path(x, y, w, h):
    """Üstü düz, altı sivri 'maden kalkan' (x,y = üst orta)."""
    pa = skia.Path()
    pa.moveTo(x - w / 2, y)
    pa.lineTo(x + w / 2, y)
    pa.lineTo(x + w / 2, y + h * 0.52)
    pa.quadTo(x + w / 2, y + h * 0.86, x, y + h)
    pa.quadTo(x - w / 2, y + h * 0.86, x - w / 2, y + h * 0.52)
    pa.close()
    return pa


def plaque(f, x, y, w, h, a=1.0, glow=0.0, col="#EFE5CC", rim="#7A5C32", dark=False):
    """Kalkan levha (kâğıt/yaldız çerçeve). (x,y) üst orta. glow>0: altın hâle."""
    c = f.c
    if glow > 0.003:
        c.drawCircle(x, y + h * 0.5, max(w, h) * 0.78, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial(
            (x, y + h * 0.5), max(w, h) * 0.78, [C("#FFE9A0", A(150 * glow * a)), C("#FFE9A0", 0)], [0.0, 1.0])))
    pa = shield_path(x, y, w, h)
    c.save()
    c.translate(5, 9)
    c.drawPath(pa, blur_paint("#000000", 70 * a, 6.0))
    c.restore()
    top, bot = (mix(col, "#FFFFFF", 0.3), mix(col, "#000000", 0.22)) if not dark else ("#4A3A26", "#241A10")
    sh = skia.GradientShader.MakeLinear([(0, y), (0, y + h)], [C(top, A(255 * a)), C(bot, A(255 * a))], [0, 1])
    c.drawPath(pa, skia.Paint(AntiAlias=True, Shader=sh))
    c.drawPath(pa, S(rim, max(2.0, w * 0.018), A(240 * a)))
    inner = shield_path(x, y + w * 0.05, w * 0.86, h * 0.90)
    c.drawPath(inner, S("#D9A532", 1.8, A(150 * a)))


def wool_bale(c, x, y, s=1.0, a=255):
    """Yün balyası (bağlı): (x,y) merkez."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    sh = skia.GradientShader.MakeLinear([(0, -46), (0, 46)], [C("#F4EEDC", a), C("#D6CBAE", a), C("#A89A78", a)], [0, 0.55, 1])
    c.drawRoundRect(skia.Rect.MakeLTRB(-70, -46, 70, 46), 18, 18, skia.Paint(AntiAlias=True, Shader=sh))
    c.drawRoundRect(skia.Rect.MakeLTRB(-70, -46, 70, 46), 18, 18, S("#5A4326", 2.4, A(0.9 * a)))
    for dx in (-34, 0, 34):
        c.drawLine(dx, -46, dx, 46, S("#7A5C32", 4.0, A(0.85 * a)))
    rs = np.random.RandomState(4)
    for i in range(16):
        px, py = rs.uniform(-62, 62), rs.uniform(-38, 38)
        c.drawArc(skia.Rect.MakeXYWH(px, py, 16, 9), 200, 220, False, S("#B5A582", 1.5, A(0.6 * a)))
    c.restore()


def check_mark(c, x, y, s, col, a=255, w=None):
    w = w or s * 0.16
    pa = skia.Path()
    pa.moveTo(x - s * 0.42, y + s * 0.02)
    pa.lineTo(x - s * 0.10, y + s * 0.34)
    pa.lineTo(x + s * 0.46, y - s * 0.34)
    c.drawPath(pa, S(col, w, a))


def cross_mark(c, x, y, s, col, a=255, w=None, k=1.0):
    w = w or s * 0.16
    k = clamp(k)
    c.drawLine(x - s * 0.38, y - s * 0.38, x - s * 0.38 + s * 0.76 * min(1.0, k * 2.0), y - s * 0.38 + s * 0.76 * min(1.0, k * 2.0), S(col, w, a))
    if k > 0.5:
        kk = (k - 0.5) * 2.0
        c.drawLine(x + s * 0.38, y - s * 0.38, x + s * 0.38 - s * 0.76 * kk, y - s * 0.38 + s * 0.76 * kk, S(col, w, a))


def half_disc(c, x, y, r, col, a=255):
    c.drawCircle(x, y, r, S(col, max(2.5, r * 0.12), A(a)))
    pa = skia.Path()
    pa.moveTo(x, y)
    pa.arcTo(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), 90, 180, False)
    pa.close()
    c.drawPath(pa, P(col, A(a)))


def lane_icon(c, lane, x, y, r, a=255, light=True):
    col = (GOLD, LAPIS_L if light else LAPIS, RED_L if light else RED)[lane]
    if lane == 0:
        c.drawCircle(x, y, r, S(col, max(2.5, r * 0.12), A(a)))
        check_mark(c, x, y, r * 1.2, col, A(a), w=max(2.8, r * 0.2))
    elif lane == 1:
        half_disc(c, x, y, r, col, a)
    else:
        c.drawCircle(x, y, r, S(col, max(2.5, r * 0.12), A(a)))
        cross_mark(c, x, y, r * 1.2, col, A(a), w=max(2.8, r * 0.2))


# ═══════════════════════════ ovl: sağlamlık HUD şeridi (akışın içinde) ═══════════════════════════
def hud_rect(i, x0=BAND_X0, y=BAND_Y, lw=BAND_LW, h=BAND_H, gap=BAND_GAP):
    return (x0 + i * (lw + gap), y, lw, h)


def draw_lane_hud(f, i, rect, a=1.0, n_dots=0, new_dot=None, size=24):
    x, y, w, h = rect
    col = (GOLD, LAPIS_L, RED_L)[i]
    c = f.c
    CM.tablet(f, x, y, w, h, alpha=0.88 * a, corner=10)
    c.drawRoundRect(skia.Rect.MakeLTRB(x + 8, y + 10, x + 14, y + h - 10), 3, 3, P(col, A(255 * a)))
    CM.ink(f, LANES[i][0], x + 28, y + h * 0.62, face="title_m", size=size, color=col, align="l", track=4, alpha=a, emboss=False)
    dx0 = x + 28 + sk.text_width(LANES[i][0], "title_m", size, 4) + 30
    for j in range(n_dots):
        lane_icon(c, i, dx0 + j * 40, y + h / 2, 13, A(255 * a))


def saglam_band(tokens, band_at, out=None, dwell=1.0, fly=0.9, chip_size=28, base=(0, 0, 0)):
    """Üst HUD: üç şerit (SAĞLAM · NİTELİKLİ · MİT). tokens=[dict(lane, label, at, src=(x,y))]: iddia `src`'de çipiyle belirir, `dwell` sonra HUD'a uçar, şeritte simgeleşir.
    Şerit `band_at`'ta açılır (c16_saglam'ın küçülmüş hâlinden DEVRALIR: aynı geometri)."""
    def fn(cx):
        f = cx.f
        c = f.c
        kb = cx.amt(band_at, 0.5)
        if out is not None:
            kb *= 1.0 - cx.amt(out, 0.6)
        if kb <= 0.003:
            return
        t = cx.t
        counts = list(base)
        flights = []
        for tk in tokens:
            ta = cx.at(tk["at"])
            t_fly = ta + tk.get("dwell", dwell)
            t_end = t_fly + fly
            if t >= t_end:
                counts[tk["lane"]] += 1
            elif t >= ta:
                flights.append((tk, ta, t_fly, t_end))
        for i in range(3):
            draw_lane_hud(f, i, hud_rect(i), a=kb, n_dots=counts[i])
        for (tk, ta, t_fly, t_end) in flights:
            lane = tk["lane"]
            col = (GOLD, LAPIS_L, RED_L)[lane]
            sx, sy = tk["src"]
            hx, hy, hw, hh = hud_rect(lane)
            # varış noktası: sonraki nokta yuvası
            dx0 = hx + 28 + sk.text_width(LANES[lane][0], "title_m", 24, 4) + 30
            tx, ty = dx0 + counts[lane] * 40, hy + hh / 2
            u = clamp((t - t_fly) / fly)
            ku = ease_io(u, 2.0)
            k_in = ease_out(clamp((t - ta) / 0.35), 3)
            x = lerp(sx, tx, ku)
            y = lerp(sy, ty, ku) - math.sin(ku * math.pi) * 90
            sc = lerp(1.0, 0.0, ku)
            lab = tk["label"]
            wd = sk.text_width(lab, "title_m", chip_size, 4) + 56
            al = k_in * (1.0 - 0.0)
            if sc > 0.02:
                c.save()
                c.translate(x, y)
                c.scale(0.35 + 0.65 * sc, 0.35 + 0.65 * sc)
                CM.tablet(f, -wd / 2, -chip_size * 0.9, wd, chip_size * 1.9, alpha=al, corner=10)
                c.drawRoundRect(skia.Rect.MakeLTRB(-wd / 2, -chip_size * 0.9, wd / 2, chip_size * 1.0), 10, 10, S(col, 3.0, A(255 * al)))
                CM.ink(f, lab, 0, chip_size * 0.28, face="title_m", size=chip_size, color=TH.fg, align="c", track=4, alpha=al, emboss=False)
                lane_icon(c, lane, -wd / 2 + 4, -chip_size * 0.9, 17, A(255 * al))
                c.restore()
            if u > 0.82:                              # varış parıltısı
                rr = 34 * (u - 0.82) / 0.18
                c.drawCircle(tx, ty, rr, S(col, 3.0, A(200 * (1.0 - (u - 0.82) / 0.18))))
        # yeni nokta yerleşirken parlama (uçuş bitişi sonrası 0.4 sn)
        for tk in tokens:
            te = cx.at(tk["at"]) + tk.get("dwell", dwell) + fly
            if 0 <= t - te < 0.45:
                lane = tk["lane"]
                hx, hy, hw, hh = hud_rect(lane)
                dx0 = hx + 28 + sk.text_width(LANES[lane][0], "title_m", 24, 4) + 30
                idx = base[lane] + sum(1 for q in tokens if q["lane"] == lane and cx.at(q["at"]) + q.get("dwell", dwell) + fly <= te + 1e-6) - 1
                px, py = dx0 + idx * 40, hy + hh / 2
                k_ = (t - te) / 0.45
                c.drawCircle(px, py, 13 + 24 * k_, S((GOLD, LAPIS_L, RED_L)[lane], 3.0, A(190 * (1 - k_))))
    return fn


# ═══════════════════════════ c16_saglam: üç büyük şerit → HUD'a küçülür ═══════════════════════════
@CM.ckind("c16_saglam")
def k_saglam(cx, in_at=0.0, d_at=(0.4, 1.0, 1.6), shrink_at=2.4, seed=2, ovl=None, **_):
    """Şimdi anlattıklarımızı sağlamlığına göre ayıralım: üç boy boyu pigment şerit (altın SAĞLAM · lacivert NİTELİKLİ · kızıl MİT) kapak gibi iner; her birinin simgesi (✔ · ◐ · ✘)
    çarpar; sonra şeritler HUD konumuna KÜÇÜLÜR (sonraki çekimlerde `saglam_band` aynı geometriyi devralır)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.03, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    ks = cx.amt(shrink_at, 1.0)
    kk = ease_io(ks, 2.0)
    for i, (nm, col) in enumerate(LANES):
        ki = cx.amt(d_at[i], 0.7) if not isinstance(d_at[i], (int, float)) else clamp((t - cx.at(d_at[i])) / 0.7)
        if ki <= 0.003 and kk <= 0.003:
            continue
        ki = ease_out(ki, 3)
        bx, by, bw, bh = 150 + i * 580.0, 170.0, 540.0, 650.0
        hx, hy, hw, hh = hud_rect(i)
        x = lerp(bx, hx, kk)
        y = lerp(by - (1 - ki) * 520, hy, kk)
        w = lerp(bw, hw, kk)
        h = lerp(bh, hh, kk)
        # gövde: pigment (üstte açık, altta koyu) + fırça çizgileri
        sh = skia.GradientShader.MakeLinear([(0, y), (0, y + h)], [C(mix(col, "#FFFFFF", 0.20), 255), C(col, 255), C(mix(col, "#000000", 0.32), 255)], [0, 0.55, 1])
        c.save()
        c.translate(5, 9)
        c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), 14, 14, blur_paint("#000000", 80, 8.0))
        c.restore()
        c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), 14, 14, skia.Paint(AntiAlias=True, Shader=sh))
        if kk < 0.7:
            rs = np.random.RandomState(7 + i)
            for q in range(int(h / 14)):
                yy = y + 8 + q * 14 + rs.rand() * 5
                c.drawLine(x + 8, yy, x + w - 8, yy + rs.randn() * 1.4, S("#FFFFFF" if rs.rand() < 0.5 else "#000000", 1.2, A(24 * (1 - kk))))
        c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), 14, 14, S("#1E1008", 3.0, 230))
        # simge + başlık
        ic_r = lerp(110.0, 13.0, kk)
        icx, icy = lerp(x + w / 2, x + 28 + 6, kk), lerp(y + 250, y + h / 2, kk)
        kic = clamp((t - (cx.at(d_at[i]) + 0.35)) / 0.35) if kk < 0.01 else 1.0
        if kic > 0.003:
            sc = 1.0 + (1.0 - sk.back_out(kic)) * 0.6
            light = "#FFF4D0"
            c.save()
            c.translate(icx, icy)
            c.scale(sc, sc)
            c.translate(-icx, -icy)
            if i == 0:
                c.drawCircle(icx, icy, ic_r, S(light, max(3.0, ic_r * 0.10), 240))
                check_mark(c, icx, icy, ic_r * 1.2, light, 245, w=max(3.0, ic_r * 0.18))
            elif i == 1:
                half_disc(c, icx, icy, ic_r, light, 240)
            else:
                c.drawCircle(icx, icy, ic_r, S(light, max(3.0, ic_r * 0.10), 240))
                cross_mark(c, icx, icy, ic_r * 1.2, light, 245, w=max(3.0, ic_r * 0.18), k=clamp(kic * 1.3))
            c.restore()
        szt = lerp(70.0, 24.0, kk)
        tx = lerp(x + w / 2, x + 28, kk)
        ty = lerp(y + 440, y + h * 0.62, kk)
        al_t = clamp((t - (cx.at(d_at[i]) + 0.2)) / 0.4) if kk < 0.01 else 1.0
        CM.ink(f, nm, tx, ty, face="title", size=szt, color="#FFF4D0" if kk < 0.5 else (GOLD, LAPIS_L, RED_L)[i], align="c" if kk < 0.5 else "l", track=lerp(10.0, 4.0, kk), alpha=al_t, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=16, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c16_patron: kalkan levhalar (Rönesans'ı kim yarattı? / ölçek / zincir) ═══════════════════════════
ROW_X = [280.0, 620.0, 960.0, 1300.0, 1640.0]
ROW_NAMES = ["YÜN LONCASI", "STROZZI", "MEDİCİ", "RUCELLAI", "TORNABUONI"]


def _emblem(f, i, x, y, w, h, a=1.0, glow=0.0):
    c = f.c
    if i == 2:
        plaque(f, x, y, w, h, a, glow, col="#F2E2B8", rim="#8A6A2A")
        palle_mark(c, x, y + h * 0.43, w * 0.80, A(255 * a))
    elif i == 0:
        plaque(f, x, y, w, h, a, glow)
        wool_bale(c, x, y + h * 0.46, w / 230.0, A(255 * a))
    else:
        plaque(f, x, y, w, h, a, glow)
        CM.ink(f, "STR"[0] if i == 1 else ("R" if i == 3 else "T"), x, y + h * 0.60, face="title", size=w * 0.56, color="#5A4326", align="c", track=0, alpha=a, emboss=False)


@CM.ckind("c16_patron")
def k_patron(cx, view="siralama", seed=3, ovl=None, **p):
    """Kalkan levha dili (yüz/arma kopyası yok; düz baş harf + palle + yün balyası). view: siralama (s7–s8) | olcek (s12) | zincir (s17)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.04, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    if view == "siralama":
        _v_siralama(cx, f, c, t, **p)
    elif view == "olcek":
        _v_olcek(cx, f, c, t, **p)
    else:
        _v_zincir(cx, f, c, t, **p)
    cam.end(f)
    CM.finish(f, cx, motes_n=14, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)


def _v_siralama(cx, f, c, t, q_at=0.0, row_at=2.4, tek_at=3.0, deg_at=3.6, gor_at=4.4, **_):
    kq = cx.amt(q_at, 0.5)
    krow = ease_io(cx.amt(row_at, 1.0), 2.0)
    # tek büyük Medici kalkanı → sıraya iner
    bx, by, bw, bh = 960.0, 190.0, 380.0, 470.0
    rx, ry, rw, rh = ROW_X[2], 420.0, 230.0, 290.0
    x, y, w, h = lerp(bx, rx, krow), lerp(by, ry, krow), lerp(bw, rw, krow), lerp(bh, rh, krow)
    for i in (0, 1, 3, 4):
        ki = ease_out(clamp(cx.amt(row_at, 0.6, off=0.3 + 0.18 * (0 if i in (1, 3) else 1))), 3)
        if ki > 0.003:
            _emblem(f, i, ROW_X[i], ry + (1 - ki) * 60, rw, rh, a=ki)
            CM.ink(f, ROW_NAMES[i], ROW_X[i], ry + rh + 56, face="title_m", size=28, color=TH.fg2, align="c", track=4, alpha=ki, emboss=False)
    kg = cx.amt(gor_at, 0.7)
    if kq > 0.003:
        _emblem(f, 2, x, y, w, h, a=kq, glow=0.25 + 0.55 * kg)
    if krow > 0.5:
        CM.ink(f, "MEDİCİ", ROW_X[2], ry + rh + 56, face="title_m", size=lerp(28, 34, kg), color=TH.fg, align="c", track=4, alpha=ease_out((krow - 0.5) * 2), emboss=False)
    # büyük soru işareti
    kqq = cx.amt(q_at, 0.5) * (1.0 - cx.amt(row_at, 0.6))
    if kqq > 0.003:
        c.save()
        c.translate(1330, 360)
        c.scale(1.0 + 0.04 * math.sin(t * 2.2), 1.0 + 0.04 * math.sin(t * 2.2))
        c.translate(-1330, -360)
        icons.draw_icon(f, "question", 1330, 360, size=260 * (0.8 + 0.2 * ease_out(kqq, 3)), metal="gold", alpha=kqq, glow=0.3)
        c.restore()
    # TEK YARATICI (üstü çizilir)
    kt = cx.amt(tek_at, 0.45)
    if kt > 0.003:
        tx, ty = 960.0, 270.0
        wd = sk.text_width("TEK YARATICI", "title", 56, 8) + 80
        CM.tablet(f, tx - wd / 2, ty - 62, wd, 100, alpha=kt, corner=10)
        CM.ink(f, "TEK YARATICI", tx, ty + 6, face="title", size=56, color=TH.fg, align="c", track=8, alpha=kt, emboss=False)
        kd = cx.amt(deg_at, 0.4)
        if kd > 0.003:
            pl = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=8.0, Color=C(RED, 245), StrokeCap=skia.Paint.kRound_Cap)
            pl.setPathEffect(skia.DiscretePathEffect.Make(14.0, 1.4, 3))
            c.drawLine(tx - wd / 2 - 10, ty - 10, tx - wd / 2 - 10 + (wd + 20) * ease_io(kd, 1.6), ty - 18, pl)
    if kg > 0.003:
        s = "EN GÖRÜNÜR PATRONLARDAN BİRİ"
        wd = sk.text_width(s, "title_m", 40, 6) + 90
        CM.tablet(f, 960 - wd / 2, 800, wd, 96, alpha=kg, corner=12)
        CM.ink(f, s, 960, 862 + (1 - kg) * 8, face="title_m", size=40, color=TH.acc, align="c", track=6, alpha=kg, emboss=False)


def _v_olcek(cx, f, c, t, in_at=0.0, grow_at=0.8, spot_at=1.8, **_):
    ki = ease_out(cx.amt(in_at, 0.6), 3)
    kgrow = ease_io(cx.amt(grow_at, 1.0), 2.0)
    ks = ease_out(cx.amt(spot_at, 0.8), 2)
    ry = 400.0
    for i in range(5):
        xi = ROW_X[i]
        if i == 2:
            sc = lerp(1.0, 1.85, kgrow)
            w, h = 230 * sc, 290 * sc
            _emblem(f, 2, xi, ry + 290 - h + 40 * (1 - ki), w, h, a=ki, glow=0.3 * kgrow + 0.55 * ks)
        else:
            sc = lerp(1.0, 0.78, kgrow)
            w, h = 230 * sc, 290 * sc
            _emblem(f, i, xi, ry + 290 - h + 40 * (1 - ki), w, h, a=ki * lerp(1.0, 0.8, kgrow))
    # ölçek cetveli (sol): dikey boy çizgisi
    if kgrow > 0.003:
        xr = 130.0
        c.drawLine(xr, ry + 290, xr, ry + 290 - 290 * 1.85 * kgrow, S("#7A5C32", 4.0, A(220 * kgrow)))
        for q in range(0, 7):
            yy = ry + 290 - q * 90 * kgrow
            c.drawLine(xr - 12, yy, xr + 12, yy, S("#7A5C32", 3.0, A(200 * kgrow)))
    # siyasi görünürlük: tepeden spot huzmesi (Medici'ye)
    if ks > 0.003:
        x0, x1 = 960 - 90, 960 + 90
        pa = skia.Path()
        pa.moveTo(x0, 40)
        pa.lineTo(x1, 40)
        pa.lineTo(960 + 330 * ks, ry + 330)
        pa.lineTo(960 - 330 * ks, ry + 330)
        pa.close()
        sh = skia.GradientShader.MakeLinear([(0, 40), (0, ry + 330)], [C("#FFF1B8", A(120 * ks)), C("#FFF1B8", A(26 * ks))], [0, 1])
        c.drawPath(pa, skia.Paint(AntiAlias=True, Shader=sh))
    CM.ink(f, "MEDİCİ", ROW_X[2], ry + 380, face="title_m", size=36, color=TH.fg, align="c", track=5, alpha=ki, emboss=False)


def _v_zincir(cx, f, c, t, in_at=0.0, l1_at=1.4, l2_at=2.4, no_at=3.8, bn_at=3.2, **_):
    xs = [420.0, 960.0, 1500.0]
    y0, w, h = 330.0, 250.0, 310.0
    names = ["MEDİCİ", "FUGGER", "ROTHSCHILD"]
    ki = [ease_out(cx.amt(in_at, 0.6, off=0.25 * i), 3) for i in range(3)]
    for i, x in enumerate(xs):
        if ki[i] <= 0.003:
            continue
        if i == 0:
            _emblem(f, 2, x, y0 + (1 - ki[i]) * 50, w, h, a=ki[i], glow=0.2)
        else:
            plaque(f, x, y0 + (1 - ki[i]) * 50, w, h, ki[i])
            CM.ink(f, "F" if i == 1 else "R", x, y0 + h * 0.60 + (1 - ki[i]) * 50, face="title", size=w * 0.56, color="#5A4326", align="c", alpha=ki[i], emboss=False)
        CM.ink(f, names[i], x, y0 + h + 62, face="title_m", size=34, color=TH.fg, align="c", track=5, alpha=ki[i], emboss=False)
    # bağlantılar (kesik: benzetme) + ✘
    for j, (la, xa, xb) in enumerate(((l1_at, xs[0] + w / 2 + 14, xs[1] - w / 2 - 14), (l2_at, xs[1] + w / 2 + 14, xs[2] - w / 2 - 14))):
        k = cx.amt(la, 0.8)
        if k <= 0.003:
            continue
        yy = y0 + h * 0.46
        pl = dash_paint("#7A5C32", 230 * k, 5.0)
        c.drawLine(xa, yy, lerp(xa, xb, ease_out(k, 2)), yy, pl)
        kx = cx.amt(la, 0.4, off=0.9)
        if kx > 0.003:
            xm = (xa + xb) / 2
            c.drawCircle(xm, yy, 36, P("#F4E9CB", A(235 * kx)))
            c.drawCircle(xm, yy, 36, S("#7A5C32", 3.0, A(235 * kx)))
            cross_mark(c, xm, yy, 44, RED, A(255 * kx), w=7.0, k=kx)
    kb = cx.amt(bn_at, 0.4)
    if kb > 0.003:
        CM.stamp(f, "BENZETME", 960, 170, rot=-0.06, size=70, color=RED, alpha=1.0, t=kb)
    kn = cx.amt(no_at, 0.4)
    if kn > 0.003:
        CM.stamp(f, "SÜREKLİLİK YOK", 960, 800, rot=0.05, size=64, color=RED, alpha=1.0, t=kn)


# ═══════════════════════════ c16_tartisma: Gombrich ↔ Goldthwaite ═══════════════════════════
def _plinth(c, x, y, w, h, a=255, gilt=False):
    sh = skia.GradientShader.MakeLinear([(x - w / 2, 0), (x + w / 2, 0)], [C("#E8D9B4" if not gilt else "#F6DE8A", a), C("#B7A47A" if not gilt else "#C9962E", a), C("#8A7852" if not gilt else "#8A6420", a)], [0, 0.5, 1])
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, y, x + w / 2, y + h), skia.Paint(AntiAlias=True, Shader=sh))
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2, y, x + w / 2, y + h), S("#4A3A22", 2.2, A(0.9 * a)))
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2 - 10, y - 12, x + w / 2 + 10, y + 4), P("#D9CBA2" if not gilt else "#E6BE55", a))


def _bubble(f, x, y, w, h, a=1.0, tail=(0, 60)):
    c = f.c
    pa = skia.Path()
    pa.addRoundRect(skia.Rect.MakeLTRB(x - w / 2, y - h / 2, x + w / 2, y + h / 2), 22, 22)
    pa.moveTo(x - 20, y + h / 2 - 2)
    pa.lineTo(x + tail[0], y + h / 2 + tail[1])
    pa.lineTo(x + 26, y + h / 2 - 2)
    c.drawPath(pa, P("#F7EFD8", A(250 * a)))
    c.drawPath(pa, S("#5A4326", 3.0, A(240 * a)))


@CM.ckind("c16_tartisma")
def k_tartisma(cx, h_at=0.0, g_at=1.7, tip_at=2.6, itiraz_at=3.8, w_at=5.6, talep_at=6.8, city_at=8.0, coin_at=8.6, link_at=9.6, uniq_at=None, seed=4, ovl=None, **_):
    """İki yaka: SOL Gombrich (benzersiz konumdaki Medici sütunu; «TİPİK» balonu çizilir) · SAĞ Goldthwaite (şehirde biriken zenginlik → sanat talebi, zincir). Soyut: yüz yok."""
    f = cx.f
    cam = CM.Cam(cx, push=0.03, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    kg, kw = ease_out(cx.amt(g_at, 0.6), 3), ease_out(cx.amt(w_at, 0.6), 3)
    khh = cx.amt(h_at, 0.7)
    if khh > 0.003:
        CM.ink(f, "TARİHÇİLER TARTIŞIR", 960, 92 - 10 * (1 - khh), face="title", size=42, color=TH.fg, align="c", track=12, alpha=khh, emboss=False)
        CM.flourish_rule(f, 960, 118, 560, alpha=khh, grow=khh)
    c.drawLine(960, 150, 960, 900, S("#B8963E", 3.0, A(150 * max(kg, kw, khh * 0.6))))
    # --- sol: GOMBRICH ---
    if kg > 0.003:
        wd = sk.text_width("GOMBRICH", "title", 44, 7) + 70
        CM.tablet(f, 480 - wd / 2, 130, wd, 82, alpha=kg, corner=10)
        CM.ink(f, "GOMBRICH", 480, 190, face="title", size=44, color=TH.fg, align="c", track=7, alpha=kg, emboss=False)
        base = 780.0
        xs = [150.0, 300.0, 660.0, 810.0]
        for i, x in enumerate(xs):
            ki = ease_out(clamp((t - cx.at(g_at) - 0.25 - 0.12 * i) / 0.5), 3)
            if ki > 0.003:
                hh = 120.0
                _plinth(c, x, base - hh * ki, 110, hh * ki, 255 * ki)
                plaque(f, x, base - hh * ki - 120 * ki - 16, 84, 104, ki * 0.9)
        # Medici: yükselen yaldız sütun (benzersiz konum)
        kbz = ease_io(clamp((t - (cx.at(uniq_at) if uniq_at is not None else cx.at(g_at) + 0.8)) / 1.2), 2.0)
        hh = 120.0 + 150.0 * kbz
        km = ease_out(cx.amt(g_at, 0.6, off=0.7), 3)
        if km > 0.003:
            _plinth(c, 480, base - hh, 130, hh, 255 * km, gilt=True)
            _emblem(f, 2, 480, base - hh - 190, 140, 176, a=km, glow=0.3 + 0.5 * kbz)
        # «TİPİK» balonu → çizilir
        kt = cx.amt(tip_at, 0.45)
        if kt > 0.003:
            bx, by = 480, 290.0
            c.save()
            c.translate(bx, by)
            c.scale(0.8 + 0.2 * sk.back_out(kt), 0.8 + 0.2 * sk.back_out(kt))
            c.translate(-bx, -by)
            _bubble(f, bx, by, 300, 90, kt, tail=(0, 70))
            CM.ink(f, "“TİPİK”", bx, by + 18, face="title", size=48, color="#3A2616", align="c", track=5, alpha=kt, emboss=False)
            kd = cx.amt(itiraz_at, 0.45)
            if kd > 0.003:
                pl = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=9.0, Color=C(RED, 245), StrokeCap=skia.Paint.kRound_Cap)
                pl.setPathEffect(skia.DiscretePathEffect.Make(14.0, 1.4, 3))
                c.drawLine(bx - 170, by - 28, bx - 170 + 340 * ease_io(kd, 1.6), by + 30, pl)
            c.restore()
    # --- sağ: GOLDTHWAITE ---
    if kw > 0.003:
        wd = sk.text_width("GOLDTHWAITE", "title", 44, 7) + 70
        CM.tablet(f, 1440 - wd / 2, 130, wd, 82, alpha=kw, corner=10)
        CM.ink(f, "GOLDTHWAITE", 1440, 190, face="title", size=44, color=TH.fg, align="c", track=7, alpha=kw, emboss=False)
        # sanat talebi (çerçeve + yukarı oklar)
        kt = ease_out(cx.amt(talep_at, 0.6), 3)
        if kt > 0.003:
            fx, fy, fw, fh = 1130.0, 310.0, 250.0, 300.0
            f.rrect(fx + 6, fy + 10, fw, fh, 6, color="#000000", alpha=0.25 * kt, blur=8)
            f.rrect(fx, fy, fw, fh, 6, color="#C9962E", alpha=kt)
            f.rrect(fx + 16, fy + 16, fw - 32, fh - 32, 3, shader=f.lin(fx, fy, fx, fy + fh, [("#F3E6C4", 0.0), ("#D8C28E", 1.0)]), alpha=kt)
            c.drawCircle(fx + fw * 0.62, fy + fh * 0.36, 30 * kt, P("#B03020", A(220 * kt)))
            pth = skia.Path()
            pth.moveTo(fx + 30, fy + fh - 30)
            pth.lineTo(fx + fw * 0.4, fy + fh * 0.52)
            pth.lineTo(fx + fw * 0.64, fy + fh * 0.76)
            pth.lineTo(fx + fw - 30, fy + fh * 0.5)
            pth.lineTo(fx + fw - 30, fy + fh - 30)
            pth.close()
            c.drawPath(pth, P("#4F7A5A", A(210 * kt)))
            CM.ink(f, "SANAT TALEBİ", fx + fw / 2, fy + fh + 54, face="title_m", size=30, color=TH.fg, align="c", track=5, alpha=kt, emboss=False)
            for i in range(3):
                ph = (t * 0.9 + i / 3.0) % 1.0
                ay = fy - 10 - ph * 70
                c.drawLine(fx + fw + 36, ay + 20, fx + fw + 36, ay - 20, S(GOLD, 6.0, A(255 * kt * (1 - ph))))
                c.drawLine(fx + fw + 36, ay - 20, fx + fw + 22, ay - 4, S(GOLD, 6.0, A(255 * kt * (1 - ph))))
                c.drawLine(fx + fw + 36, ay - 20, fx + fw + 50, ay - 4, S(GOLD, 6.0, A(255 * kt * (1 - ph))))
        # şehir (ev siluetleri) + biriken sikke yığını
        kc = ease_out(cx.amt(city_at, 0.7), 3)
        if kc > 0.003:
            hx0 = 1470.0
            for i, (dx, hw_, hh_) in enumerate(((0, 90, 120), (100, 70, 90), (180, 100, 150), (290, 80, 100))):
                col = ("#C9B58A", "#B8A47A", "#D4C297", "#BFAA7E")[i]
                x0_ = hx0 + dx
                f.rect(x0_, 770 - hh_ * kc, hw_, hh_ * kc, color=col)
                f.rect(x0_, 770 - hh_ * kc, hw_, hh_ * kc, style="stroke", sw=2.0, color="#5A4326", alpha=0.8 * kc)
                f.poly([(x0_ - 6, 770 - hh_ * kc), (x0_ + hw_ / 2, 770 - hh_ * kc - 34 * kc), (x0_ + hw_ + 6, 770 - hh_ * kc)], color="#A8503A", alpha=kc)
            CM.ink(f, "ŞEHİR", hx0 + 190, 826, face="title_m", size=30, color=TH.fg, align="c", track=5, alpha=kc, emboss=False)
        kcn = cx.amt(coin_at, 1.4)
        if kcn > 0.003:
            nco = int(2 + 7 * kcn)
            for i in range(nco):
                L.coin_flat(c, 1560 + (i % 3) * 30 - 30, 700 - (i // 3) * 16, 26.0, 255)
            CM.ink(f, "BİRİKEN ZENGİNLİK", 1580, 886, face="title_m", size=28, color=TH.acc, align="c", track=4, alpha=min(1.0, kcn * 2), emboss=False)
        kl = cx.amt(link_at, 0.8)
        if kl > 0.003:
            pa = skia.Path()
            pa.moveTo(1560, 600)
            pa.quadTo(1470, 420 - 40 * kl, 1390, 470)
            pl = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7.0, Color=C(GOLD, A(255 * kl)), StrokeCap=skia.Paint.kRound_Cap)
            pl.setPathEffect(skia.DashPathEffect.Make([18, 12], -t * 30))
            c.drawPath(pa, pl)
    cam.end(f)
    CM.finish(f, cx, motes_n=14, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c16_sahne: opera ve piyano (Medici sarayında doğdu; icat onların değil) ═══════════════════════════
def _note(c, x, y, s, col, a):
    c.drawOval(skia.Rect.MakeLTRB(x - s * 0.34, y - s * 0.22, x + s * 0.34, y + s * 0.22), P(col, a))
    c.drawLine(x + s * 0.30, y - s * 0.02, x + s * 0.30, y - s * 1.0, S(col, s * 0.10, a))
    c.drawLine(x + s * 0.30, y - s * 1.0, x + s * 0.64, y - s * 0.72, S(col, s * 0.12, a))


@CM.ckind("c16_sahne")
def k_sahne(cx, op_at=0.0, pi_at=1.2, no_at=3.0, seed=5, ovl=None, **_):
    """Sol OPERA (perde açılır, notalar yükselir) · sağ PİYANO (tuşlar sırayla basılır); üstte tek palle: «MEDİCİ SARAYI»; sonunda «İCAT ONLARIN DEĞİL» damgası."""
    f = cx.f
    cam = CM.Cam(cx, push=0.05, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    ko = ease_out(cx.amt(op_at, 0.7), 3)
    kp = ease_out(cx.amt(pi_at, 0.7), 3)
    # palle (üst orta)
    kpal = ease_out(cx.amt(op_at, 0.8), 3)
    palle_mark(c, 960, 190, 150, A(255 * kpal))
    CM.ink(f, "MEDİCİ SARAYI", 960, 318, face="title_m", size=30, color=TH.fg2, align="c", track=7, alpha=kpal, emboss=False)
    # sol: opera
    if ko > 0.003:
        ox, oy, ow, oh = 160.0, 380.0, 620.0, 420.0
        f.rrect(ox - 14, oy - 14, ow + 28, oh + 28, 10, color="#C9962E", alpha=ko)
        f.rect(ox, oy, ow, oh, color="#2A1A12", alpha=ko)
        # sahne ışığı
        c.drawRect(skia.Rect.MakeLTRB(ox, oy, ox + ow, oy + oh), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((ox + ow / 2, oy + oh * 0.7), ow * 0.55, [C("#FFE2A0", A(150 * ko)), C("#FFE2A0", 0)], [0, 1])))
        kop = ease_io(clamp((t - cx.at(op_at) - 0.5) / 1.3), 2.0)
        for sg in (-1, 1):
            wcur = (ow / 2) * (1.0 - 0.78 * kop)
            x0 = ox if sg < 0 else ox + ow - wcur
            sh = skia.GradientShader.MakeLinear([(x0, 0), (x0 + wcur, 0)], [C("#7A1E16", A(255 * ko)), C("#B03020", A(255 * ko)), C("#7A1E16", A(255 * ko))], [0, 0.5, 1])
            c.drawRect(skia.Rect.MakeLTRB(x0, oy, x0 + wcur, oy + oh), skia.Paint(AntiAlias=True, Shader=sh))
            for q in range(1, 6):
                c.drawLine(x0 + wcur * q / 6, oy, x0 + wcur * q / 6, oy + oh, S("#4A0E0A", 2.0, A(110 * ko)))
        # notalar
        for i in range(5):
            ph = (t * 0.6 + i * 0.21) % 1.0
            if kop > 0.2:
                _note(c, ox + 180 + i * 62, oy + oh * 0.72 - ph * 190, 34, "#FFE9A8", A(255 * (1 - ph) * kop))
        CM.ink(f, "OPERA", ox + ow / 2, oy + oh + 70, face="title", size=56, color=TH.fg, align="c", track=10, alpha=ko, emboss=False)
    # sağ: piyano (tuşlar)
    if kp > 0.003:
        px0, py0, pw, ph_ = 1120.0, 560.0, 640.0, 200.0
        f.rrect(px0 - 12, py0 - 90, pw + 24, 100, 8, color="#2A1A12", alpha=kp)
        f.rrect(px0 - 12, py0 - 90, pw + 24, 100, 8, style="stroke", sw=3.0, color="#C9962E", alpha=0.9 * kp)
        nk = 12
        kw_ = pw / nk
        for i in range(nk):
            press = 0.0
            tk = cx.at(pi_at) + 0.7 + 0.22 * i
            if 0 <= t - tk < 0.5:
                press = math.sin((t - tk) / 0.5 * math.pi)
            x = px0 + i * kw_
            f.rect(x, py0 + press * 10, kw_ - 3, ph_ - press * 10, color=mix("#F4EEDC", "#C9BFA0", press), alpha=kp)
            f.rect(x, py0 + press * 10, kw_ - 3, ph_ - press * 10, style="stroke", sw=2.0, color="#3A2A18", alpha=0.85 * kp)
        for i in (0, 1, 3, 4, 5, 7, 8, 10):
            x = px0 + (i + 1) * kw_ - 15
            f.rect(x, py0, 26, ph_ * 0.6, color="#1C140E", alpha=kp)
        CM.ink(f, "PİYANO", px0 + pw / 2, py0 + ph_ + 76, face="title", size=56, color=TH.fg, align="c", track=10, alpha=kp, emboss=False)
    kn = cx.amt(no_at, 0.4)
    if kn > 0.003:
        CM.stamp(f, "İCAT ONLARIN DEĞİL", 1450, 290, rot=-0.05, size=60, color=RED, alpha=1.0, t=kn)
    cam.end(f)
    CM.finish(f, cx, motes_n=14, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c16_muze: Uffizi ↔ Capitoline (iki bina, iki yıl) ═══════════════════════════
import c0_kinds as K0  # noqa: E402


def draw_uffizi(f, x, gy, s, a=1.0, glow=0.0, w=520.0):
    """Revaklı Uffizi cephesi (c0_kuyruk'taki `_arcade`/`_portal`, ölçekli). (x,gy) = taban orta."""
    c = f.c
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(x - w * s, gy - 700 * s, x + w * s, gy + 6))
    c.translate(x, gy)
    c.scale(s, s)
    if a < 0.999:
        c.saveLayerAlpha(skia.Rect.MakeLTRB(-w - 40, -700, w + 40, 20), int(255 * a))
    K0._arcade(f, -w, w, 0.0, TH)
    K0._portal(f, 0.0, 0.0, glow)
    if a < 0.999:
        c.restore()
    c.restore()


def draw_capitoline(f, x, gy, s, a=1.0, glow=0.0):
    """Capitoline (stilize): ortada saçaklı palazzo, çift merdiven (cordonata), kule, iki yan kanat."""
    c = f.c
    c.save()
    c.translate(x, gy)
    c.scale(s, s)
    if a < 0.999:
        c.saveLayerAlpha(skia.Rect.MakeLTRB(-620, -700, 620, 40), int(255 * a))
    stone, shade = "#D6C59E", "#A8966F"
    for sg in (-1, 1):                                  # yan kanatlar
        x0 = 230 if sg > 0 else -430
        f.rect(x0, -250, 200, 250, color="#CDBB93")
        f.rect(x0, -250, 200, 250, style="stroke", sw=3, color="#7A6544")
        for k in range(3):
            f.rect(x0 + 30 + k * 56, -200, 34, 70, color="#5A4630")
        f.rect(x0 - 10, -262, 220, 16, color="#E3D3AC")
    f.rect(-70, -560, 140, 160, color=mix(stone, "#000000", 0.06))              # kule
    f.rect(-70, -560, 140, 160, style="stroke", sw=3, color="#7A6544")
    f.circle(0, -500, 34, color="#F4EAC8")
    f.circle(0, -500, 34, style="stroke", sw=3, color="#5A4326")
    f.poly([(-84, -560), (0, -640), (84, -560)], color="#A8503A")
    f.rect(-230, -400, 460, 400, color=stone)                                   # ana gövde
    f.rect(-230, -400, 460, 400, style="stroke", sw=4, color="#7A6544")
    f.poly([(-250, -400), (0, -480), (250, -400)], color="#E3D3AC")
    f.poly([(-250, -400), (0, -480), (250, -400)], style="stroke", sw=4, color="#7A6544")
    for k in range(5):                                                          # pilastrlar
        px = -190 + k * 95
        f.rect(px - 14, -390, 28, 360, color=mix(stone, "#FFFFFF", 0.3))
        f.rect(px - 14, -390, 28, 360, style="stroke", sw=2, color=shade)
    # kapı (ortada, sıcak ışık)
    arch = skia.Path()
    arch.moveTo(-60, -40)
    arch.lineTo(-60, -230)
    arch.arcTo(skia.Rect.MakeLTRB(-60, -290, 60, -170), 180, 180, False)
    arch.lineTo(60, -40)
    arch.close()
    c.drawPath(arch, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -290), (0, -40)], [C(mix("#3A2C20", "#FFE2A0", glow)), C(mix("#6E5A42", "#F0A850", glow))], [0, 1])))
    c.drawPath(arch, f.paint("#E3D3AC", style="stroke", sw=10))
    # çift merdiven
    for sg in (-1, 1):
        f.poly([(sg * 70, -40), (sg * 300, 0), (sg * 330, 0), (sg * 90, -40)], color="#C4B286")
    f.poly([(-70, -40), (70, -40), (110, 0), (-110, 0)], color="#B7A57A")
    for k in range(6):
        f.line(-100 + k * 8, -40 + k * 6.6, 100 - k * 8, -40 + k * 6.6, color="#8A7852", sw=2.0)
    if a < 0.999:
        c.restore()
    c.restore()


@CM.ckind("c16_muze")
def k_muze(cx, view="iki", u_at=0.0, ilk_at=1.6, c_at=2.6, ac_at=4.0, oysa_at=3.4, seed=6, ovl=None, **_):
    """İki bina yan yana: SOL Uffizi (revak; «İLK MODERN MÜZE» levhası çizilir) · SAĞ Roma'daki Capitoline (kapı açılır, 1734). view='iki' (c16s16)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.05, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    gy = 800.0
    f.rect(-200, gy, W + 400, 400, color="#B9A77C", alpha=0.55)
    f.line(-200, gy, W + 400, gy, color="#6A5640", sw=3.0)
    ku = ease_out(cx.amt(u_at, 0.8), 3)
    kc = ease_out(cx.amt(c_at, 0.8), 3)
    if ku > 0.003:
        draw_uffizi(f, 520.0, gy, 0.60, a=ku, glow=0.3, w=420.0)
        CM.ink(f, "UFFIZI", 520, gy + 62, face="title", size=50, color=TH.fg, align="c", track=10, alpha=ku, emboss=False)
    if kc > 0.003:
        kg_ = cx.amt(ac_at, 0.8)
        draw_capitoline(f, 1400.0, gy, 0.80, a=kc, glow=0.2 + 0.8 * kg_)
        CM.ink(f, "CAPITOLINE · ROMA", 1400, gy + 62, face="title", size=44, color=TH.fg, align="c", track=7, alpha=kc, emboss=False)
        if kg_ > 0.003:
            CM.tablet(f, 1400 - 100, 170 - 20 * (1 - kg_), 200, 96, alpha=kg_, corner=10)
            CM.ink(f, "1734", 1400, 240 - 20 * (1 - kg_), face="title", size=64, color=TH.acc, align="c", track=6, alpha=kg_, emboss=False)
    # «İLK MODERN MÜZE» levhası (Uffizi üstünde) → üstü çizilir
    ki = cx.amt(ilk_at, 0.6)
    if ki > 0.003:
        s_ = "İLK MODERN MÜZE"
        wd = sk.text_width(s_, "title", 44, 6) + 80
        CM.tablet(f, 520 - wd / 2, 130 - 16 * (1 - ki), wd, 100, alpha=ki, corner=10)
        CM.ink(f, s_, 520, 196 - 16 * (1 - ki), face="title", size=44, color=TH.fg, align="c", track=6, alpha=ki, emboss=False)
        ko_ = cx.amt(oysa_at, 0.45)
        if ko_ > 0.003:
            pl = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=9.0, Color=C(RED, 245), StrokeCap=skia.Paint.kRound_Cap)
            pl.setPathEffect(skia.DiscretePathEffect.Make(14.0, 1.4, 3))
            c.drawLine(520 - wd / 2 - 10, 180, 520 - wd / 2 - 10 + (wd + 20) * ease_io(ko_, 1.6), 170, pl)
            kq = cx.amt(oysa_at, 0.3, off=0.2)
            if kq > 0.003:
                CM.stamp(f, "İLK DEĞİL", 520, 330, rot=-0.07, size=60, color=RED, alpha=1.0, t=kq)
    # zaman oku: Capitoline → Uffizi («ÖNCE»)
    ka = cx.amt(ac_at, 0.9, off=0.6)
    if ka > 0.003:
        pa = skia.Path()
        pa.moveTo(1250, 400)
        pa.quadTo(960, 300 - 40 * ka, 700 + (1 - ka) * 540, 400)
        pl = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6.0, Color=C(GOLD, A(255 * ka)), StrokeCap=skia.Paint.kRound_Cap)
        pl.setPathEffect(skia.DashPathEffect.Make([16, 12], -t * 24))
        c.drawPath(pa, pl)
        CM.ink(f, "ÖNCE", 980, 296, face="title_m", size=36, color=TH.acc, align="c", track=8, alpha=ka, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=14, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c16_kurum: banka öldü; kurumlar kaldı ═══════════════════════════
_PET = ["#2B4EA8", "#2E8B57", "#B03020", "#1E1C1A", "#E0A83A"]


def draw_inlay(f, x, y, k_list, a=1.0, r=96.0):
    """Sert taş (pietre dure) çiçek: koyu levha üzerinde beş taş yaprak ve orta kehribar; k_list: her parçanın yerine oturma 0..1."""
    c = f.c
    f.rrect(x - r * 1.5, y - r * 1.5, r * 3.0, r * 3.0, 14, color="#1C1814", alpha=a)
    f.rrect(x - r * 1.5, y - r * 1.5, r * 3.0, r * 3.0, 14, style="stroke", sw=4.0, color="#C9962E", alpha=a)
    for i in range(5):
        k = clamp(k_list[i]) if i < len(k_list) else 0.0
        if k <= 0.003:
            continue
        ang = -math.pi / 2 + i * 2 * math.pi / 5
        dist = lerp(r * 2.2, r * 0.62, ease_out(k, 3))
        px, py = x + math.cos(ang) * dist, y + math.sin(ang) * dist
        c.save()
        c.translate(px, py)
        c.rotate(math.degrees(ang) + 90)
        pa = skia.Path()
        pa.moveTo(0, r * 0.52)
        pa.quadTo(r * 0.52, 0, 0, -r * 0.52)
        pa.quadTo(-r * 0.52, 0, 0, r * 0.52)
        sh = skia.GradientShader.MakeLinear([(0, -r * 0.5), (0, r * 0.5)], [C(mix(_PET[i], "#FFFFFF", 0.32), A(255 * a)), C(_PET[i], A(255 * a)), C(mix(_PET[i], "#000000", 0.3), A(255 * a))], [0, 0.5, 1])
        c.drawPath(pa, skia.Paint(AntiAlias=True, Shader=sh))
        c.drawPath(pa, S("#0E0A06", 2.0, A(220 * a)))
        c.restore()
    kc = clamp(k_list[5]) if len(k_list) > 5 else 0.0
    if kc > 0.003:
        f.circle(x, y, r * 0.30 * sk.back_out(kc), color=_PET[4], alpha=a)
        f.circle(x, y, r * 0.30 * sk.back_out(kc), style="stroke", sw=2.5, color="#0E0A06", alpha=0.85 * a)


@CM.ckind("c16_kurum")
def k_kurum(cx, ledger_at=0.0, kurum_at=1.2, opif_at=2.2, work_at=3.4, uffizi_at=4.8, yil_at=6.0, bugun_at=None, acik_at=None, seed=3, ovl=None, **_):
    """Üç sütun: SOL kapanan defter (BANKA, ✘) · ORTA Opificio levhası (taşlar yerine oturur) · SAĞ Uffizi (kapı yanar, 1769). Üstte «KURUMLAR KALDI»."""
    f = cx.f
    cam = CM.Cam(cx, push=0.05, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    gy = 800.0
    f.line(-200, gy, W + 400, gy, color="#6A5640", sw=3.0)
    kl = ease_out(cx.amt(ledger_at, 0.7), 3)
    kdead = ease_io(cx.amt(ledger_at, 0.9, off=0.7), 2.0)
    if kl > 0.003:
        a_ = kl * lerp(1.0, 0.55, kdead)
        book_closed(c, 330, gy - 60, 380, 116, col=mix("#8A2E1E", "#5A5A5A", kdead), a=A(255 * a_), band="#D8B25A")
        book_closed(c, 330, gy - 176, 350, 104, col=mix("#2F4F8A", "#5A5A5A", kdead), a=A(255 * a_), band="#D8B25A", tilt=-0.03)
        CM.ink(f, "BANKA", 330, gy + 66, face="title", size=48, color=TH.fg, align="c", track=10, alpha=kl, emboss=False)
        if kdead > 0.003:
            cross_mark(c, 330, gy - 150, 190, RED, A(240 * kdead), w=16.0, k=kdead)
    kk = cx.amt(kurum_at, 0.6)
    if kk > 0.003:
        s_ = "KURUMLAR KALDI"
        wd = sk.text_width(s_, "title", 54, 8) + 90
        CM.tablet(f, 960 - wd / 2, 150 - 14 * (1 - kk), wd, 104, alpha=kk, corner=12)
        CM.ink(f, s_, 960, 222 - 14 * (1 - kk), face="title", size=54, color=TH.acc, align="c", track=8, alpha=kk, emboss=False)
    ko = ease_out(cx.amt(opif_at, 0.6), 3)
    if ko > 0.003:
        ks = [ease_out(clamp((t - cx.at(work_at) - 0.34 * i) / 0.55), 3) for i in range(6)]
        draw_inlay(f, 960, gy - 250, ks, a=ko, r=118.0)
        for q in range(8):
            ph = (t * 0.5 + q * 0.13) % 1.0
            if ks[0] > 0.3:
                c.drawCircle(960 + math.cos(q * 2.4) * 190, gy - 250 + math.sin(q * 2.4) * 190 - ph * 30, 3, P("#FFF1B8", A(180 * (1 - ph) * min(1.0, ks[5] + 0.3))))
        CM.ink(f, "OPIFICIO DELLE PIETRE DURE", 960, gy + 66, face="title_m", size=34, color=TH.fg, align="c", track=5, alpha=ko, emboss=False)
        kw = cx.amt(bugun_at if bugun_at is not None else work_at, 0.6, off=0.0 if bugun_at is not None else 1.8)
        if kw > 0.003:
            CM.ink(f, "BUGÜN DE ÇALIŞIYOR", 960, gy + 116, face="cap_i", size=34, color=TH.acc, align="c", alpha=kw, emboss=False)
    ku = ease_out(cx.amt(uffizi_at, 0.7), 3)
    if ku > 0.003:
        draw_uffizi(f, 1560.0, gy, 0.62, a=ku, glow=0.35 + 0.65 * cx.amt(yil_at, 0.8), w=330.0)
        CM.ink(f, "UFFIZI", 1560, gy + 66, face="title", size=48, color=TH.fg, align="c", track=10, alpha=ku, emboss=False)
        ky = cx.amt(yil_at, 0.6)
        if ky > 0.003:
            CM.tablet(f, 1560 - 100, 300 - 18 * (1 - ky), 200, 96, alpha=ky, corner=10)
            CM.ink(f, "1769", 1560, 370 - 18 * (1 - ky), face="title", size=64, color=TH.acc, align="c", track=6, alpha=ky, emboss=False)
            kac = cx.amt(acik_at if acik_at is not None else yil_at, 0.6, off=0.0 if acik_at is not None else 1.0)
            CM.ink(f, "HALKA AÇIK", 1560, gy + 116, face="cap_i", size=34, color=TH.acc, align="c", alpha=kac, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=14, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c16_mit_tablo: yol boyunca düzelttiğimiz hikâyeler ═══════════════════════════
ROWS = [
    ("ÇİFTE KAYDI MEDİCİ İCAT ETTİ", "CENOVA 1340'TA", 2),
    ("BOTTICELLI TABLOLARINI YAKTI", "HANGİ TABLO? GÖSTEREN YOK", 2),
    ("KOZİMO OĞLUNU ÖLDÜRDÜ", "SITMAYLA UYUMLU", 2),
    ("ZEHİRLİ TURTA (FRANCESCO I)", "BÜYÜK OLASILIKLA SITMA", 1),
    ("KATRİN'İN ÇATALI, DONDURMASI", "ÇATAL ÇOK ÖNCE İTALYA'DA", 2),
    ("UFFIZI İLK MODERN MÜZE", "CAPITOLINE 1734", 2),
    ("MEDİCİ'DEN ROTHSCHILD'E ZİNCİR", "BENZETME, BAĞ YOK", 2),
    ("SÖZLEŞME BİR BAĞIŞTI", "DEVİR KOŞULU (BİR YORUM)", 1),
    ("MEDİCİ RÖNESANS'I YARATTI", "EN GÖRÜNÜR PATRONLARDAN BİRİ", 2),
    ("SAVONAROLA LORENZO'NUN BAŞUCUNDA", "YANDAŞLARIN ANLATTIĞI SAHNE", 1),
]


@CM.ckind("c16_mit_tablo")
def k_mit_tablo(cx, start_at=0.0, dt=0.40, head_at=None, rows=ROWS, seed=3, ovl=None, **_):
    """Düzeltilen hikâyelerin bir arada kapanış tablosu: iki sütun × beş satır. Her satır kendi anında kayar; iddia üstü çizilir, düzeltme altına yazılır; ✘ (kızıl) ya da ◐ (lacivert: nitelikli)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.03, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    kh = cx.amt(head_at if head_at is not None else start_at, 0.6)
    if kh > 0.003:
        CM.ink(f, "DÜZELTTİĞİMİZ HİKÂYELER", 960, 150, face="title", size=46, color=TH.fg, align="c", track=10, alpha=kh, emboss=False)
        CM.flourish_rule(f, 960, 180, 520, alpha=kh, grow=kh)
    for i, (claim, fix, lane) in enumerate(rows):
        col, row = divmod(i, 5)
        ta = cx.at(start_at) + 0.35 + dt * i
        k = ease_out(clamp((t - ta) / 0.45), 3)
        if k <= 0.003:
            continue
        x0 = 70.0 + col * 900.0
        y0 = 215.0 + row * 138.0 + (1 - k) * 16
        w, h = 880.0, 118.0
        CM.tablet(f, x0, y0, w, h, alpha=k, corner=12)
        lc = (GOLD, LAPIS, RED)[lane]
        lcl = (GOLD, LAPIS_L, RED_L)[lane]
        ic = clamp((t - ta - 0.15) / 0.35)
        c.save()
        c.translate(x0 + 58, y0 + h / 2)
        sc = 1.0 + (1 - sk.back_out(ic)) * 0.6 if ic < 1 else 1.0
        c.scale(sc, sc)
        c.drawCircle(0, 0, 36, P("#F7EFD8", A(240 * k)))
        c.drawCircle(0, 0, 36, S(lc, 4.0, A(255 * k)))
        if lane == 2:
            cross_mark(c, 0, 0, 44, lc, A(255 * ic), w=7.0, k=ic)
        else:
            half_disc(c, 0, 0, 22, lc, A(255 * ic))
        c.restore()
        szc = CM.fit_size(claim, "title_m", 28, w - 150, 3)
        CM.ink(f, claim, x0 + 112, y0 + 46, face="title_m", size=szc, color=TH.fg2, align="l", track=3, alpha=k, emboss=False)
        ks = clamp((t - ta - 0.35) / 0.4)
        if ks > 0.003:
            tw = sk.text_width(claim, "title_m", szc, 3)
            pl = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5.0, Color=C(lc if lane == 2 else "#7A5C32", A(235 * k)), StrokeCap=skia.Paint.kRound_Cap)
            pl.setPathEffect(skia.DiscretePathEffect.Make(12.0, 1.2, 3))
            c.drawLine(x0 + 106, y0 + 38, x0 + 106 + (tw + 12) * ease_io(ks, 1.6), y0 + 34, pl)
        szf = CM.fit_size(fix, "title", 34, w - 150, 3)
        CM.ink(f, fix, x0 + 112, y0 + 94, face="title", size=szf, color=TH.fg if lane == 1 else TH.acc, align="l", track=3, alpha=clamp((t - ta - 0.4) / 0.3) * k, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=12, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c16_mezar: mezar yakın zamanda açıldı; iç organlar ayrı bir kapta; ölüm nedeni belirsiz ═══════════════════════════
@CM.ckind("c16_mezar")
def k_mezar(cx, open_at=0.6, kap_at=2.4, date_at=1.2, bel_at=4.2, seed=5, ovl=None, **_):
    """Medici Şapelleri kriptası (sessiz, ağır): taş lahit, kapağı hafif aralanır (altın ışık çizgisi — içi GÖSTERİLMEZ); sağda ayrı bir kap (küp) ışır; sonunda «?». Ceset/organ görüntüsü YOK."""
    f = cx.f
    cam = CM.Cam(cx, push=0.05, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    # kemerli duvar nişi
    f.rect(-100, 0, W + 200, H, color="#241A14", alpha=0.0)
    for q in range(-2, 5):
        xq = 160 + q * 520
        arch = skia.Path()
        arch.moveTo(xq - 150, 880)
        arch.lineTo(xq - 150, 460)
        arch.arcTo(skia.Rect.MakeLTRB(xq - 150, 310, xq + 150, 610), 180, 180, False)
        arch.lineTo(xq + 150, 880)
        arch.close()
        c.drawPath(arch, P("#171210", 200))
        c.drawPath(arch, S("#6A5640", 5.0, 150))
    f.rect(-100, 800, W + 200, 400, color="#2C2219")
    f.line(-100, 800, W + 100, 800, color="#8A7852", sw=3.0, alpha=0.8)
    # lahit
    lx, ly, lw, lh = 700.0, 600.0, 640.0, 210.0
    f.rect(lx - 10, ly + 8, lw + 20, lh, color="#000000", alpha=0.4)
    sh = skia.GradientShader.MakeLinear([(0, ly), (0, ly + lh)], [C("#B9AD92"), C("#8D8168"), C("#5E5340")], [0, 0.5, 1])
    c.drawRect(skia.Rect.MakeLTRB(lx, ly, lx + lw, ly + lh), skia.Paint(AntiAlias=True, Shader=sh))
    c.drawRect(skia.Rect.MakeLTRB(lx, ly, lx + lw, ly + lh), S("#2A2018", 3.0, 230))
    for q in range(3):
        c.drawLine(lx + 40, ly + 70 + q * 40, lx + lw - 40, ly + 70 + q * 40, S("#4A3E2E", 2.0, 90))
    ko = ease_io(cx.amt(open_at, 1.6), 2.0)
    lid_dx = 70.0 * ko
    sh2 = skia.GradientShader.MakeLinear([(0, ly - 56), (0, ly + 4)], [C("#D2C7AC"), C("#A39777")], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(lx - 18 + lid_dx, ly - 56, lx + lw + 18 + lid_dx, ly + 4), skia.Paint(AntiAlias=True, Shader=sh2))
    c.drawRect(skia.Rect.MakeLTRB(lx - 18 + lid_dx, ly - 56, lx + lw + 18 + lid_dx, ly + 4), S("#2A2018", 3.0, 230))
    palle_mark(c, lx + lw / 2 + lid_dx, ly - 28, 56, 150, col="#6A5640")
    if ko > 0.02:                                                            # kapak aralığından ince altın ışık
        c.drawRect(skia.Rect.MakeLTRB(lx + lw + 18 - 4, ly - 6, lx + lw + 18 + lid_dx + 2, ly + 8), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(lx + lw, 0), (lx + lw + lid_dx, 0)], [C("#FFE2A0", A(220 * ko)), C("#FFE2A0", A(40 * ko))], [0, 1])))
    # ayrı kap (küp) — sağ raf
    kk = ease_out(cx.amt(kap_at, 0.8), 3)
    if kk > 0.003:
        ux, uy = 1560.0, 760.0
        f.rect(ux - 140, uy + 6, 280, 26, color="#4A3A28", alpha=kk)
        f.circle(ux, uy - 60, 150 * kk, shader=f.rad(ux, uy - 60, 150 * kk + 1, [("#FFE2A0", 0.0, int(110 * kk)), ("#FFE2A0", 1.0, 0)]))
        pa = skia.Path()
        pa.moveTo(ux - 38, uy)
        pa.cubicTo(ux - 92, uy - 40, ux - 84, uy - 128, ux - 40, uy - 150)
        pa.lineTo(ux + 40, uy - 150)
        pa.cubicTo(ux + 84, uy - 128, ux + 92, uy - 40, ux + 38, uy)
        pa.close()
        sh3 = skia.GradientShader.MakeLinear([(ux - 90, 0), (ux + 90, 0)], [C("#E0B07A", A(255 * kk)), C("#B07A44", A(255 * kk)), C("#6A4424", A(255 * kk))], [0, 0.5, 1])
        c.drawPath(pa, skia.Paint(AntiAlias=True, Shader=sh3))
        c.drawPath(pa, S("#2A1608", 3.0, A(240 * kk)))
        c.drawRect(skia.Rect.MakeLTRB(ux - 46, uy - 168, ux + 46, uy - 146), P("#8A5A2E", A(255 * kk)))
        c.drawRect(skia.Rect.MakeLTRB(ux - 46, uy - 168, ux + 46, uy - 146), S("#2A1608", 2.5, A(240 * kk)))
        CM.tablet(f, ux - 150, 836, 300, 70, alpha=kk, corner=10)
        CM.ink(f, "AYRI BİR KAP", ux, 884, face="title_m", size=32, color=TH.fg, align="c", track=5, alpha=kk, emboss=False)
    kd = cx.amt(date_at, 0.6)
    if kd > 0.003:
        s_ = "ARALIK 2012 – ŞUBAT 2013"
        wd = sk.text_width(s_, "title", 38, 6) + 76
        CM.tablet(f, 120, 170 - 12 * (1 - kd), wd, 86, alpha=kd, corner=10)
        CM.ink(f, s_, 120 + wd / 2, 226 - 12 * (1 - kd), face="title", size=38, color=TH.fg, align="c", track=6, alpha=kd, emboss=False)
    kb = cx.amt(bel_at, 0.6)
    if kb > 0.003:
        icons.draw_icon(f, "question", 1000, 250, size=190 * (0.8 + 0.2 * ease_out(kb, 3)), metal="silver", alpha=kb, glow=0.2)
        CM.tablet(f, 760, 380 - 10 * (1 - kb), 480, 84, alpha=kb, corner=10)
        CM.ink(f, "ÖLÜM NEDENİ: BELİRSİZ", 1000, 434 - 10 * (1 - kb), face="title_m", size=34, color=TH.fg, align="c", track=5, alpha=kb, emboss=False)
    light = CM.candle_light(t, seed, base=(1000, 640), r=1000.0, sway=4.0)
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=light, vig_s=0.62)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c16_para: «Para gitti, banka gitti.» ═══════════════════════════
@CM.ckind("c16_para")
def k_para(cx, gone_at=0.9, ledger_at=1.1, gone2_at=1.5, seed=4, ovl=None, **_):
    """Karanlık zeminde tek florin: «gitti» sözcüğünde yaldız tozuna dağılır; yanında kapalı defter belirir ve o da söner. Bitiş: tam karanlık (sonraki çekime ağır geçiş)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.04, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    kg = ease_in(cx.amt(gone_at, 0.9), 1.6)
    ks = 1.0 - kg
    # florin (yaldız disk, orta)
    if ks > 0.01:
        f.circle(700, 540, 150, shader=f.rad(700, 540, 150, [("#FFD27A", 0.0, int(120 * ks)), ("#FFD27A", 1.0, 0)]))
        CP.draw_coin(f, 700, 540 + math.sin(t * 1.2) * 6, 330, spin=t * 0.9 + 0.35 + kg * 6.0, alpha=ks, shadow=0.55, glow=0.22 * ks)
    rs = np.random.RandomState(9)
    for q in range(26):                                             # dağılan yaldız tozu
        ang = rs.uniform(0, 2 * math.pi)
        sp = rs.uniform(40, 220)
        u = clamp((t - cx.at(gone_at)) / 1.6)
        if u > 0:
            px, py = 700 + math.cos(ang) * sp * u, 540 + math.sin(ang) * sp * u - 60 * u * u * 3
            c.drawCircle(px, py, 3.2, P("#FFD27A", A(230 * (1 - u))))
    kl = ease_out(cx.amt(ledger_at, 0.5), 3) * (1.0 - ease_in(cx.amt(gone2_at, 0.9), 1.6))
    if kl > 0.01:
        book_closed(c, 1220, 590, 420, 130, col="#8A2E1E", a=A(255 * kl), band="#D8B25A")
        book_closed(c, 1220, 462, 400, 118, col="#2F4F8A", a=A(255 * kl), band="#D8B25A", tilt=-0.03)
    light = CM.candle_light(t, seed, base=(960, 540), r=900.0 * (0.6 + 0.4 * ks), sway=4.0)
    cam.end(f)
    CM.finish(f, cx, motes_n=16, light=light, vig_s=0.6)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ ovl: fener alayı (her 18 Şubat; silüet, yüz yok) ═══════════════════════════
def lantern_walk(at, y=880.0, n=11, x_from=-120.0, x_to=2040.0, dur=9.0, h=96.0, out=None, spacing=118.0, col="#2A1E15", seed=3):
    """Yürüyen fener alayı: n siluet (yandan), her biri elinde fener; `at`'tan itibaren `dur` sn'de x_from→x_to. Altyazı bölgesinin (y≥938) üstünde yürür."""
    import c0_kinds as K0_

    def fn(cx):
        f = cx.f
        c = f.c
        t = cx.t
        ta = cx.at(at)
        if t < ta - 0.1:
            return
        u = clamp((t - ta) / dur)
        al = 1.0 - (cx.amt(out, 0.8) if out is not None else 0.0)
        if al <= 0.01:
            return
        rs = np.random.RandomState(seed)
        for i in range(n):
            xi = lerp(x_from - i * spacing, x_to - i * spacing, u)
            if xi < -80 or xi > W + 80:
                continue
            ph = t * 4.6 + i * 1.7
            yj = y + (i % 3) * 4
            hh = h * (0.92 + 0.1 * rs.rand())
            K0_._sil_person(f, xi, yj, hh, ph, 1.0, "plain", alpha=al, col=col)
            lx, ly = xi + hh * 0.20, yj - hh * 0.50 + math.sin(ph) * 3
            c.drawCircle(lx, ly, hh * 0.9, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((lx, ly), hh * 0.9, [C("#FFD58A", A(150 * al)), C("#FFD58A", 0)], [0, 1])))
            c.drawRect(skia.Rect.MakeLTRB(lx - hh * 0.03, ly - hh * 0.05, lx + hh * 0.03, ly + hh * 0.06), P("#FFF3C8", A(255 * al)))
    return fn


# ═══════════════════════════ ovl'lar: yün balyası, yaldız yazı çizgisi, pencere ışığı, fener noktaları, kapanış karartması ═══════════════════════════
def bale_ov(x, y, at, out=None, s=1.4):
    def fn(cx):
        k = L._kk(cx, at, 0.55, out, 0.5)
        if k > 0.003:
            wool_bale(cx.f.c, x, y - (1 - k) * 14, s * (0.8 + 0.2 * ease_out(k, 3)), A(255 * k))
    return fn


def gold_script(at, y=250.0, x0=300.0, x1=1700.0, dur=2.2, col="#F4D890", size=34, seed=5, out=None):
    """Gökyüzünde yaldız yazı çizgisi (stilize, OKUNMAZ): «bir kadının da imzaladığı bir cümle» — soldan sağa yazılır, ince hâle."""
    def fn(cx):
        k = clamp((cx.t - cx.at(at)) / dur)
        if k <= 0.003:
            return
        al = 1.0 - (cx.amt(out, 0.8) if out is not None else 0.0)
        c = cx.f.c
        c.saveLayerAlpha(skia.Rect.MakeLTRB(0, y - 80, W, y + 80), int(255 * al))
        K14.script_line(c, x0, x1, y, ease_io(k, 1.6), size=size, seed=seed, col=col, a=235)
        c.restore()
        xe = x0 + (x1 - x0) * ease_io(k, 1.6)
        cx.f.circle(xe, y, 46, shader=cx.f.rad(xe, y, 46, [("#FFF1B8", 0.0, int(170 * al * (1 - 0.5 * k))), ("#FFF1B8", 1.0, 0)]))
    return fn


def window_glow(x, y, at, r=130.0, out=None, col="#FFD58A", pulse=0.12):
    def fn(cx):
        k = L._kk(cx, at, 1.2, out, 0.8)
        if k <= 0.003:
            return
        pr = 1.0 + pulse * math.sin(cx.t * 2.3)
        cx.f.circle(x, y, r * pr, shader=cx.f.rad(x, y, r * pr, [(col, 0.0, int(190 * k)), (col, 1.0, 0)]))
        cx.f.circle(x, y, 7 * (0.6 + 0.4 * k), color="#FFF3C8", alpha=k)
    return fn


def lantern_dots(at, y=786.0, n=14, dur=7.0, x_from=-80.0, x_to=1960.0, spacing=96.0, seed=3, out=None):
    """Kıyıda yürüyen fener noktaları (uzaktan; figür çizilmez): n sıcak ışık, `dur` sn'de soldan sağa."""
    def fn(cx):
        t = cx.t
        ta = cx.at(at)
        if t < ta - 0.1:
            return
        u = clamp((t - ta) / dur)
        al = 1.0 - (cx.amt(out, 0.8) if out is not None else 0.0)
        rs = np.random.RandomState(seed)
        for i in range(n):
            xi = lerp(x_from - i * spacing, x_to - i * spacing, u)
            if xi < -40 or xi > W + 40:
                continue
            ki = clamp((xi + 40) / 220.0) * al
            yi = y + 6 * math.sin(t * 3.1 + i) * 0.4 + (i % 3) * 3
            cx.f.circle(xi, yi, 30, shader=cx.f.rad(xi, yi, 30, [("#FFD58A", 0.0, int(170 * ki)), ("#FFD58A", 1.0, 0)]))
            cx.f.circle(xi, yi, 4.2, color="#FFF3C8", alpha=ki)
    return fn


def end_dim(at, alpha=0.7, dur=2.4):
    """Kapanış: ekran yavaşça kararır (son çekim; Program bitiş ekranına devreder)."""
    def fn(cx):
        k = ease_io(clamp((cx.t - cx.at(at)) / dur), 1.6)
        if k > 0.003:
            cx.f.rect(0, 0, W, H, color="#05060C", alpha=alpha * k)
    return fn


# ═══════════════════════════ c16_yuruyus: Palazzo Vecchio'dan Medici Şapelleri'ne alay + ücretsiz müzeler (plan görünümü) ═══════════════════════════
@CM.ckind("c16_yuruyus")
def k_yuruyus(cx, pv_at=0.0, route_at=0.2, walk_at=0.2, walk_dur=3.6, ch_at=2.0, ticket_at=5.0, free_at=5.8, seed=2, ovl=None, **_):
    """Kuş bakışı şema (kâğıt): Arno şeridi, SOL Palazzo Vecchio kulesi, SAĞ Medici Şapelleri kubbesi; kesik çizgi yol; fener taşıyan siluetler yolu yürür. Sonda bilet + «ÜCRETSİZ»."""
    f = cx.f
    cam = CM.Cam(cx, push=0.05, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    # Arno şeridi
    rp = skia.Path()
    rp.moveTo(-100, 640)
    rp.cubicTo(500, 560, 900, 760, 1400, 650)
    rp.cubicTo(1700, 590, 1900, 640, 2050, 620)
    c.drawPath(rp, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=70, Color=C("#9DB7C4", 190), StrokeCap=skia.Paint.kRound_Cap))
    c.drawPath(rp, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=70, Color=C("#6E8C9C", 90), StrokeCap=skia.Paint.kRound_Cap))
    pts = [(470, 440), (700, 470), (900, 420), (1120, 380), (1330, 330)]
    # yol (kesik)
    kr = ease_out(clamp((t - cx.at(route_at)) / 3.0), 1.4)
    if kr > 0.003:
        pa = skia.Path()
        pa.moveTo(*pts[0])
        for i in range(1, len(pts)):
            pa.quadTo((pts[i - 1][0] + pts[i][0]) / 2, min(pts[i - 1][1], pts[i][1]) - 20, *pts[i])
        pm = skia.PathMeasure(pa, False)
        L_ = pm.getLength()
        seg = skia.Path()
        pm.getSegment(0, L_ * kr, seg, True)
        c.drawPath(seg, dash_paint("#7A5C32", 235, 5.0, 14.0, 12.0))
    # Palazzo Vecchio (kule simgesi)
    kp = ease_out(cx.amt(pv_at, 0.7), 3)
    if kp > 0.003:
        icons.draw_icon(f, "tower", 470, 400, size=210 * (0.85 + 0.15 * kp), metal="gold", alpha=kp)
        CM.tablet(f, 470 - 175, 520, 350, 70, alpha=kp, corner=10)
        CM.ink(f, "PALAZZO VECCHIO", 470, 568, face="title_m", size=32, color=TH.fg, align="c", track=5, alpha=kp, emboss=False)
    # Medici Şapelleri (kubbe)
    kc = ease_out(cx.amt(ch_at, 0.7), 3)
    if kc > 0.003:
        x, y = 1330.0, 330.0
        f.rect(x - 110, y - 20 + 40 * (1 - kc), 220, 90, color="#CDBB93", alpha=kc)
        f.rect(x - 110, y - 20 + 40 * (1 - kc), 220, 90, style="stroke", sw=3.0, color="#7A6544", alpha=kc)
        dm = skia.Path()
        dm.moveTo(x - 90, y - 20 + 40 * (1 - kc))
        dm.arcTo(skia.Rect.MakeLTRB(x - 90, y - 110 + 40 * (1 - kc), x + 90, y + 70 + 40 * (1 - kc)), 180, 180, False)
        dm.close()
        c.drawPath(dm, P("#B24A32", A(255 * kc)))
        c.drawPath(dm, S("#5A2A1A", 3.0, A(255 * kc)))
        c.drawLine(x, y - 110 + 40 * (1 - kc), x, y - 140 + 40 * (1 - kc), S("#7A6544", 4.0, A(255 * kc)))
        CM.tablet(f, x - 215, 450, 430, 70, alpha=kc, corner=10)
        CM.ink(f, "MEDİCİ ŞAPELLERİ", x, 498, face="title_m", size=32, color=TH.fg, align="c", track=5, alpha=kc, emboss=False)
    # yürüyen siluetler (fener)
    uw = clamp((t - cx.at(walk_at)) / walk_dur)
    if uw > 0.003:
        pa = skia.Path()
        pa.moveTo(*pts[0])
        for i in range(1, len(pts)):
            pa.quadTo((pts[i - 1][0] + pts[i][0]) / 2, min(pts[i - 1][1], pts[i][1]) - 20, *pts[i])
        pm = skia.PathMeasure(pa, False)
        L_ = pm.getLength()
        for i in range(9):
            ui = uw * 1.12 - i * 0.07
            if ui <= 0 or ui >= 1.0:
                continue
            p_ = pm.getPosTan(L_ * ui)
            px, py = p_[0].x(), p_[0].y()
            ph = t * 5.0 + i * 1.3
            K0._sil_person(f, px, py + 8, 58, ph, 1.0, "plain", alpha=1.0, col="#2A1E15")
            f.circle(px + 12, py - 26, 20, shader=f.rad(px + 12, py - 26, 20, [("#FFD58A", 0.0, 170), ("#FFD58A", 1.0, 0)]))
            f.circle(px + 12, py - 26, 3.4, color="#FFF3C8")
    # bilet + ÜCRETSİZ
    kt = ease_out(cx.amt(ticket_at, 0.7), 3)
    if kt > 0.003:
        tx, ty, tw, th_ = 700.0, 780.0, 480.0, 130.0
        c.save()
        c.translate(tx, ty + (1 - kt) * 30)
        c.rotate(-3)
        f.rrect(-tw / 2 + 5, -th_ / 2 + 8, tw, th_, 12, color="#000000", alpha=0.25 * kt, blur=8)
        f.rrect(-tw / 2, -th_ / 2, tw, th_, 12, color="#F3E6C4", alpha=kt)
        f.rrect(-tw / 2, -th_ / 2, tw, th_, 12, style="stroke", sw=3.0, color="#7A5C32", alpha=kt)
        c.drawLine(tw / 2 - 110, -th_ / 2 + 8, tw / 2 - 110, th_ / 2 - 8, dash_paint("#7A5C32", 200 * kt, 3.0, 8.0, 8.0))
        CM.ink(f, "BELEDİYE MÜZELERİ", -50, 10, face="title_m", size=32, color=TH.fg, align="c", track=4, alpha=kt, emboss=False)
        c.restore()
    kf = cx.amt(free_at, 0.35)
    if kf > 0.003:
        CM.stamp(f, "ÜCRETSİZ", 1230, 770, rot=-0.08, size=80, color=RED, alpha=1.0, t=kf)
    cam.end(f)
    CM.finish(f, cx, motes_n=12, light=None, vig_s=0.45)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c16_harita: c0_harita + ovl (c0'ın Büyük Dukalık haritasına dönüş) ═══════════════════════════
@CM.ckind("c16_harita")
def k_harita16(cx, ovl=None, **kw):
    import shots as SH
    K0.ensure_toskana(SH.mapview())
    SH.KINDS["map"](cx, **kw)
    if ovl is not None:
        ovl(cx)
