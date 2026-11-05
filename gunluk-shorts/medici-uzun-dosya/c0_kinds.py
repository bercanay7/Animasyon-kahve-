"""c0_kinds — c0 (KANCA) için özel çekim türleri. Tümü `c0_` önekli; ana motor dosyalarına dokunmaz.

c0_takvim  : takvim yaprakları hızla çevrilir, "114 GÜN" sayar (kardeşin ölümünden sözleşmeye).
c0_belge   : 31 Ekim 1737 belgesi — iki mühür, 13 madde (Romen rakamı), FRANSIZCA damgası, ITALIANO çizilir, III. madde vurgusu; kamera belge içinde gezer.
c0_kuyruk  : bugünün Uffizi kuyruğu (siluet) — yalnız siluet, yüz yok.
c0_sikke   : kılıçlar çizilir, altın sikke girer; geri sarma yıl sayacı 1737 → 1252.
Olgu disiplini: yalnız script'te geçen ad/sayı/tarih etiketleri; yüz yok.
"""
import math

import skia

import anim
import cilt_medici as CM
import cilt_oda as OD
import cilt_props as CP
import icons
import sk
from cilt_medici import TH, ckind
import cilt_cam
from sk import H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth


def _paper_stamp(*a, **k):
    """P1'de bütün damgalar tek dilde: kâğıt fişli, ≥4,5:1 mürekkep (anim.paper_stamp = CM.stamp imzası; kurul tur 2 TE2-Y5, ENG-C isteği)."""
    import anim as _AN
    return _AN.paper_stamp(*a, **k)


def _gilt_or_ink(txt, face, size, track, color=None):
    if TH.day:
        return CM.engraved(txt, face, int(size), track, color or TH.fg)
    return CM.gilt(txt, face, int(size), track)


# ─────────────────────────────────────────────────────────────────────────────
# c0_takvim
# ─────────────────────────────────────────────────────────────────────────────
def _leaf(f, x, y, w, h, tone, alpha=1.0, back=False, grid=True, seed=0):
    """Duvar takvimi yaprağı (üst kenarı bağda; (x,y) = sol-üst)."""
    c = f.c
    col = mix(tone, "#000000", 0.12) if back else tone
    f.rrect(x, y, w, h, 8, shader=f.lin(x, y, x, y + h, [(mix(col, "#FFFFFF", 0.10), 0.0), (col, 1.0)]), alpha=alpha)
    p = f.paint("#4A3420", style="stroke", sw=1.6, alpha=0.55 * alpha)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 8, 8), p)
    if grid and not back and h > 40:
        gp = f.paint("#6A5238", style="stroke", sw=1.2, alpha=0.28 * alpha)
        cols, rows = 7, 6
        gx0, gy0 = x + 34, y + 150
        gw, gh = w - 68, h - 200
        for i in range(cols + 1):
            c.drawLine(gx0 + gw * i / cols, gy0, gx0 + gw * i / cols, min(gy0 + gh, y + h - 6), gp)
        for j in range(rows + 1):
            yy = gy0 + gh * j / rows
            if yy < y + h - 6:
                c.drawLine(gx0, yy, gx0 + gw, yy, gp)


def _leaf_fly_pts(i, s, x0, y0, w, h):
    """k_takvim'deki i. savrulan yaprağın (s = uçuş ilerlemesi) dört köşesi + merkezi — çizimle aynı formül (deklanşör hız ipucu için)."""
    dxl = (-70 + 26 * math.sin(i * 1.7)) * s + 60 * math.sin(s * 5 + i) * (1 - s)
    lx = x0 + w * (0.30 + 0.35 * ((i * 37) % 10) / 10.0) + dxl
    ly = y0 + 40 + 700 * s * s + 80 * s
    ang = math.radians(math.sin(i) * 25 + 160 * s * (1 if i % 2 else -1))
    lw_, lh_ = w * 0.34, h * 0.30
    return anim.box_pts(lx, ly, -lw_ / 2, -lh_ / 2, lw_ / 2, lh_ / 2, rot=ang)


@ckind("c0_takvim")
def k_takvim(cx, start_at=("c0s6", "ölümünden", -0.3), end_at=("c0s6", "dört", 0.2), n=114, final=("31", "EKİM", "1737"), unit="GÜN", show_at=None, first=None, seed=2, **_):
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.05, drift=(5.0, 2.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="both")
    cam.begin(f)
    ta, tb = cx.at(start_at), cx.at(end_at)
    p = clamp((cx.t - ta) / max(1e-3, tb - ta))
    pe = ease_io(p, 2.0)
    appear = cx.amt(show_at if show_at is not None else start_at, 0.5, off=-0.6)
    # takvim gövdesi (asılı, hafif sallanır)
    x0, y0, w, h = 380, 205, 500, 640
    sway = math.radians(0.7) * math.sin(cx.t * 1.3) * (1.0 - 0.6 * smooth(p))
    c.save()
    c.translate(x0 + w / 2, y0 - 40)
    c.rotate(math.degrees(sway))
    c.translate(-(x0 + w / 2), -(y0 - 40))
    # ip + çivi
    f.line(x0 + w / 2 - 60, y0 - 12, x0 + w / 2, y0 - 90, color="#3A2616", sw=3.0, alpha=0.9 * appear)
    f.line(x0 + w / 2 + 60, y0 - 12, x0 + w / 2, y0 - 90, color="#3A2616", sw=3.0, alpha=0.9 * appear)
    f.circle(x0 + w / 2, y0 - 92, 9, color="#2A1A0C", alpha=appear)
    # arka levha + yığın kenarı
    f.rrect(x0 - 22 + 8, y0 - 18 + 14, w + 44, h + 70, 14, color="#000000", alpha=0.35 * appear, blur=10)
    f.rrect(x0 - 22, y0 - 18, w + 44, h + 70, 14, shader=f.lin(x0, y0, x0, y0 + h, [("#7A4E2A", 0.0), ("#4E2E16", 1.0)]), alpha=appear)
    f.rrect(x0 - 22, y0 - 18, w + 44, h + 70, 14, style="stroke", sw=2.4, color="#2A1A0C", alpha=0.8 * appear)
    for i in range(5):
        f.rrect(x0 + 3 * (4 - i) * 0.0, y0 + 10 + 3 * (4 - i), w, h, 8, color=mix("#E9DDBB", "#000000", 0.05 * i), alpha=appear)
    tone = "#EFE4C4"
    # sıradaki yaprak (altta görünen) ve çevrilen yaprak
    kf = pe * n
    frac = kf - math.floor(kf)
    spin = p > 0.0 and p < 1.0
    # taban yaprağı (sabit)
    _leaf(f, x0, y0, w, h, tone, alpha=appear, seed=1)
    # üst bant (bağ + delikler)
    f.rrect(x0, y0, w, 56, 8, shader=f.lin(x0, y0, x0, y0 + 56, [("#8E2A30", 0.0), ("#6A1A22", 1.0)]), alpha=appear)
    for i in range(4):
        f.circle(x0 + 80 + i * 113, y0 + 28, 8, color="#1A0F08", alpha=0.85 * appear)
        f.circle(x0 + 80 + i * 113, y0 + 28, 8, style="stroke", sw=2, color="#D8B25A", alpha=0.9 * appear)
    # çevrilen yapraklar: hayalet izli
    if spin:
        for g in range(3):
            fr = (frac - g * 0.33) % 1.0 if p < 0.985 else 0.0
            al = (1.0 if g == 0 else 0.34 / g) * appear
            th = math.pi * fr
            hh = h * abs(math.cos(th))
            if th < math.pi / 2:
                _leaf(f, x0, y0 + 56, w, max(1.0, hh - 56 * 0), tone, alpha=al * 0.95, grid=False)
            else:
                _leaf(f, x0, y0 + 56 - hh * 0.55, w, max(1.0, hh * 0.55), tone, alpha=al * 0.9, back=True, grid=False)
    # savrulan yapraklar (kopan yaprakların bir kısmı süzülerek düşer)
    nf = 26
    for i in range(nf):
        q = (i + 0.5) / nf
        ts = ta + (tb - ta) * q * 0.96
        s = (cx.t - ts) / 1.05
        if 0.0 < s < 1.0:
            dxl = (-70 + 26 * math.sin(i * 1.7)) * s + 60 * math.sin(s * 5 + i) * (1 - s)
            lx = x0 + w * (0.30 + 0.35 * ((i * 37) % 10) / 10.0) + dxl
            ly = y0 + 40 + 700 * s * s + 80 * s
            ang = (math.sin(i) * 25 + 160 * s * (1 if i % 2 else -1))
            al = (1.0 - smooth((s - 0.65) / 0.35)) * 0.85 * appear
            c.save()
            c.translate(lx, ly)
            c.rotate(ang)
            lw_, lh_ = w * 0.34, h * 0.30
            f.rrect(-lw_ / 2 + 4, -lh_ / 2 + 6, lw_, lh_, 6, color="#000000", alpha=0.25 * al, blur=6)
            f.rrect(-lw_ / 2, -lh_ / 2, lw_, lh_, 6, color=mix(tone, "#000000", 0.05 + 0.04 * (i % 3)), alpha=al)
            f.rrect(-lw_ / 2, -lh_ / 2, lw_, lh_, 6, style="stroke", sw=1.4, color="#4A3420", alpha=0.45 * al)
            c.restore()
            if al > 0.02:                                     # ENG-E (kurul tur 3 AN1-Y7): savrulan yaprağın gerçek hızı (konum + dönüş) → deklanşör
                anim.hint_pts(cx, *[_leaf_fly_pts(i, (tt - ts) / 1.05, x0, y0, w, h) for tt in (cx.t - anim.DT_HINT / 2, cx.t + anim.DT_HINT / 2)])
    # ilk yaprak (çevrilmeden önce): başlangıç tarihi — sayfa boş görünmesin (kurul AN2: durağan boş kâğıt)
    if first:
        kf0 = appear * (1.0 - smooth(p / 0.05))
        if kf0 > 0.01:
            CM.ink(f, first[1], x0 + w / 2, y0 + 38, face="title_m", size=34, color="#F4E3B2", align="c", track=12, alpha=kf0, emboss=False)
            sp0 = CM.painted(first[0], "title", 260, 6.0, "#3A2A1A", 1.3, 5)
            CM.draw_spr(f, sp0, x0 + w / 2, y0 + h * 0.60, "c", alpha=kf0)
            CM.ink(f, first[2], x0 + w / 2, y0 + h - 56, face="title_m", size=44, color="#4A3420", align="c", track=10, alpha=kf0, emboss=False)
    # son yaprak: tarih damgası
    kfin = cx.amt(end_at, 0.34)
    if kfin > 0:
        mon = sk.text_width(final[1], "title_m", 40, 12)
        CM.ink(f, final[1], x0 + w / 2, y0 + 38, face="title_m", size=34, color="#F4E3B2", align="c", track=12, alpha=kfin, emboss=False)
        sp = CM.painted(final[0], "title", 260, 6.0, "#A8321E", 1.3, 5)
        sc = 1.0 + (1 - sk.back_out(kfin)) * 0.9
        CM.draw_spr(f, sp, x0 + w / 2, y0 + h * 0.60, "c", alpha=kfin, scale=sc)
        CM.ink(f, final[2], x0 + w / 2, y0 + h - 56, face="title_m", size=44, color="#4A3420", align="c", track=10, alpha=kfin, emboss=False)
    c.restore()
    # sayaç
    xc = 1290
    tq = getattr(cx, "t_nom", cx.t)                          # ENG-E: sayaç karenin nominal saatinden — deklanşör alt örneklerinde rakam değişmez (hayalet rakam yok)
    val = int(round(n * ease_io(clamp((tq - ta) / max(1e-3, tb - ta)), 2.0)))
    a = cx.amt(start_at, 0.4, off=-0.2)
    txt = str(val)
    sz = 300
    sp = _gilt_or_ink(txt, "title", sz, 8.0)
    jit = (1.0 + 0.012 * math.sin(tq * 40)) if spin else 1.0
    CM.draw_spr(f, sp, xc, 640 + 20, "c", alpha=a, scale=jit, shadow=0.5 if not TH.day else 0.0, glow=0.20 * a if (not TH.day and p >= 1.0) else 0.0)
    CM.ink(f, unit, xc, 640 + 108, face="title_m", size=64, color=TH.acc if TH.day else "#F6D886", align="c", track=22, alpha=a * cx.amt(start_at, 0.6, off=0.1), emboss=False)
    # ilerleme çubuğu (çevrilen günler)
    bw = 520
    f.rrect(xc - bw / 2, 790, bw, 10, 5, color="#000000", alpha=0.35 * a)
    f.rrect(xc - bw / 2, 790, max(0.1, bw * pe), 10, 5, color=TH.acc if TH.day else "#E8C468", alpha=0.95 * a)
    cam.end(f)
    CM.finish(f, cx, motes_n=26)


# ─────────────────────────────────────────────────────────────────────────────
# c0_belge
# ─────────────────────────────────────────────────────────────────────────────
DOC_FILL = (1986.944, 161.505, 5.705882)         # oda1743: belge ekranı doldurur (cams anahtarı)
DOC_ROT = -0.012
# FRANSIZCA damgasının belge düzlemindeki merkezi. Kurul tur 3 TE2-G4 (ENG-E): eski (150, −40) #8'in 2,1–2,24× yakın planında harfleri x≈1880–1940'a,
# kırmızı çerçeveyi ve fişi ekran dışına itiyordu → 85 belge px sola: #8 boyunca harfler ≤ ≈1750, çerçeve ≤ ≈1830, fiş ≤ ≈1880; #7'de ("Fransızca")
# damga kadrajın ortasına iner (≈x 940). Aynı belge düzlemi: #7, #8 ve #10'da aynı yer (süreklilik).
FR_XY = (65.0, -40.0)
ROMAN =["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII"]
LINE_Y = [-380 + 150 + 35.0 * i for i in range(13)]       # doc_sheet satır tabanları (belge merkezi = 0,0)


def _cr(vals, t):
    """Catmull-Rom (uç teğetleri 0) — vals: [(t_i, v_i)]; v_i tuple."""
    n = len(vals)
    if t <= vals[0][0]:
        return vals[0][1]
    if t >= vals[-1][0]:
        return vals[-1][1]
    i = 0
    while i < n - 2 and t > vals[i + 1][0]:
        i += 1
    t0, v0 = vals[i]
    t1, v1 = vals[i + 1]
    u = (t - t0) / max(1e-6, t1 - t0)
    u = u * u * (3 - 2 * u)
    return tuple(a + (b - a) * u for a, b in zip(v0, v1))


def _cam_keys(cx, cams):
    ks = [(cx.at(a), v) for a, v in cams]
    ks.sort(key=lambda q: q[0])
    return ks


def _cr_cut(vals, t, e0=0.0, e1=0.0, tau=0.6):
    """_cr ile aynı (anahtarlar arası smoothstep, iç anahtarlarda hız 0), ama UÇLARDA eğim: e0/e1 = ilk/son aralığın ortalama hızının katı.
    e > 0 iken uç aralık Hermite'tir (dış uçta e, iç uçta 0; e ≤ 3 için tekdüze, aşma yok) ve anahtarın ötesinde kamera durmaz: o hızla sürer, tau sn'de
    sönümlenir (cilt_pano.pchip ile aynı uzatma: en çok e·v·tau yol). e0 = e1 = 0 → _cr ile bit-birebir aynı (geçişli uçlar ve P7'nin girişi değişmez)."""
    n = len(vals)
    if n < 2 or (e0 <= 0.0 and e1 <= 0.0):
        return _cr(vals, t)
    if t <= vals[0][0]:
        (ta, va), (tb, vb) = vals[0], vals[1]
        if e0 <= 0.0:
            return va
        k = tau * (1.0 - math.exp(-(ta - t) / tau))
        return tuple(a - e0 * (b - a) / max(1e-6, tb - ta) * k for a, b in zip(va, vb))
    if t >= vals[-1][0]:
        (ta, va), (tb, vb) = vals[-2], vals[-1]
        if e1 <= 0.0:
            return vb
        k = tau * (1.0 - math.exp(-(t - tb) / tau))
        return tuple(b + e1 * (b - a) / max(1e-6, tb - ta) * k for a, b in zip(va, vb))
    i = 0
    while i < n - 2 and t > vals[i + 1][0]:
        i += 1
    (ta, va), (tb, vb) = vals[i], vals[i + 1]
    u = clamp((t - ta) / max(1e-6, tb - ta))
    s0 = e0 if i == 0 else 0.0
    s1 = e1 if i == n - 2 else 0.0
    g = (u ** 3 - 2 * u * u + u) * s0 + (3 * u * u - 2 * u ** 3) + (u ** 3 - u * u) * s1
    return tuple(a + (b - a) * g for a, b in zip(va, vb))


def _doc_cam(cx, ks):
    """c0_belge kamerası (k_belge ve belge_sayac AYNI işlevi kullanır → sayaç belgeye bağlı kalır). Kurul tur 3 AN1-Y-N3 (ENG-E): SERT KESMEYLE birleşen
    uçta eğim cilt_cam.CUT_SLOPE ("hareket üstünde kesme"; cilt_cam/cilt_pano ile aynı kural): 43,9 sn'de #8 kesmeden hızsız başlıyordu (ilk adım ≈0),
    #7 son anahtarından sonra kesmeye dek duruyordu. Geçişli uçlara (zoomthru/carry) dokunulmaz: e = 0, eski smoothstep."""
    e0 = cilt_cam._end_factor(False, bool(getattr(cx, "cut_in", False)))
    e1 = cilt_cam._end_factor(False, bool(getattr(cx, "cut_out", False)))
    return _cr_cut(ks, cx.t, e0, e1)


def _hand(f, text, x, y, size, color, alpha=1.0, seed=0, align="l"):
    import cilt_paper as PP
    PP.hand(f, text, x, y, "fell_i", size, color, alpha, 1.0, seed=seed, align=align)


cilt_cam.OWN_CAMERA.add("c0_belge")      # kendi kamera anahtarları (cams=) var


@ckind("c0_belge")
def k_belge(cx, cams=None, seals=None, num_at=None, num_dur=1.1, fr_at=None, it_at=None, it_strike_at=None, hl_at=None, hl_out=None,
            names_at=None, third_at=None, scrim_at=None, seed=3, pen_at=None, names_out=None, names_hide=(), script_alpha=1.0, **_):
    """Belge (1100×760 kâğıt; oda belgesiyle aynı). cams=[(çapa, (doc_x, doc_y, ölçek))] — belge koordinatında (0,0 = merkez) ekran merkezine gelen nokta + ölçek.
    seals=(sol_çapa, sağ_çapa); names_at=(sol,sağ) mühür altı etiketleri; num_at: 13 Romen rakamı sırayla; fr_at: FRANSIZCA damgası;
    it_at/it_strike_at: ITALIANO yazılır / çizilir; hl_at: III. madde vurgusu (hl_out'ta söner)."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    ks = _cam_keys(cx, cams or [(0.0, (0.0, 0.0, 0.97))])
    dxc, dyc, s = _doc_cam(cx, ks)
    px, py = 960 - dxc * s, 520 - dyc * s
    OD.doc_sheet(f, px, py, s, cx.t, n=13, shown=None, seed=seed, rot=DOC_ROT, seal=False, shadow=0.6, script_alpha=script_alpha)   # v3.2: #8 yakında gövde yazısı ≈%70
    c.save()
    c.translate(px, py)
    c.rotate(math.degrees(DOC_ROT))
    c.scale(s, s)
    ink = "#3A2616"
    # III. madde vurgusu (altın leke + sinabar alt çizgi)
    if hl_at is not None:
        k = cx.amt(hl_at, 0.6)
        if hl_out is not None:
            k *= 1.0 - cx.amt(hl_out, 0.5)
        if k > 0.003:
            y = LINE_Y[2]
            gp = skia.Paint(AntiAlias=True)
            gp.setShader(skia.GradientShader.MakeLinear([(-470, 0), (500, 0)], [sk.C("#FFD060", int(150 * k)), sk.C("#FFD060", int(46 * k))], [0, 1]))
            c.drawRect(skia.Rect.MakeLTRB(-470, y - 26, -470 + 970 * smooth(k), y + 12), gp)
            pl = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.0, Color=sk.C("#A8321E", int(235 * k)), StrokeCap=skia.Paint.kRound_Cap)
            pl.setPathEffect(skia.DiscretePathEffect.Make(14.0, 1.1, 3))
            c.drawLine(-455, y + 12, -455 + 940 * smooth(k), y + 12, pl)
    # Romen rakamları (sol kenar boşluğu)
    if num_at is not None:
        t0n = cx.at(num_at)
        for i, r in enumerate(ROMAN):
            ti = t0n + num_dur * i / 13.0
            k = clamp((cx.t - ti) / 0.28)
            if k <= 0:
                continue
            y = LINE_Y[i]
            sc = 1.0 + (1.0 - sk.back_out(k)) * 0.5
            c.save()
            c.translate(-505, y + 6)
            c.scale(sc, sc)
            col = "#A8321E" if i == 2 else "#6A3A22"
            CM.ink(f, r, 0, 0, face="title_m", size=26, color=col, align="l" if False else "c", track=2, alpha=k, emboss=False)
            c.restore()
    # mühürler
    if seals:
        la, ra = seals
        CM.wax_seal(f, -330, 262, 58, "#A52A1C", alpha=1.0, t=cx.amt(la, 0.45), palle=True)
        _SEAL_BOX = (-58 * 1.15, -58 * 1.15, 58 * 1.15, 58 * 1.15)
        anim.hint_pop(cx, -330, 262, _SEAL_BOX, la, 0.45, anim.cm_seal_scale)      # ENG-E (AN1-Y7): mühür "çarpması"nın gerçek hızı → deklanşör
        kr = cx.amt(ra, 0.45)
        if kr > 0:
            CM.wax_seal(f, 330, 262, 58, "#233C8C", alpha=1.0, t=kr, palle=False)
            anim.hint_pop(cx, 330, 262, _SEAL_BOX, ra, 0.45, anim.cm_seal_scale)
            ring_a = smooth(kr)
            f.circle(330, 262, 22, style="stroke", sw=3.0, color="#E8D49A", alpha=0.85 * ring_a)
            f.circle(330, 262, 9, color="#E8D49A", alpha=0.7 * ring_a)
    if names_at:
        for ni, (txt, x, an) in enumerate(((names_at[0], -330, names_at[2]), (names_at[1], 330, names_at[3]))):
            k = cx.amt(an, 0.5)
            for (hi, h_out, h_in) in names_hide:            # (ad sırası, sönme çapası, dönüş çapası): kamera öbür tarafa geçince
                if hi == ni:                                # kenarda yarım kalan ad söner, tam görünüme dönünce geri gelir
                    k *= clamp(1.0 - cx.amt(h_out, 0.35) + (cx.amt(h_in, 0.35) if h_in is not None else 0.0))
            if names_out is not None:                      # kamera mühürlerden ayrılınca adlar söner: alt kenarda yarım ad kalmasın
                k *= 1.0 - cx.amt(names_out, 0.4)          # (başkan, kurul tur 3 TE2-G1 ilkesi; qa_yerlesim yarım yazı: 43,1 sn %71)
            if k > 0.003:
                CM.ink(f, txt, x, 262 + 94 + (1 - k) * 8, face="title_m", size=26, color="#4A2A16", align="c", track=5, alpha=k, emboss=False)
    # kalem (imza anı)
    if pen_at is not None:
        k = cx.amt(pen_at, 0.4)
        if k > 0.003:
            qx = -330 + 90 * (1.0 - k) + 12 * math.sin(cx.t * 9)
            OD.quill(c, qx, 262 + 4, -58.0, 0.9, alpha=k * (1 - cx.amt(pen_at, 1.0, off=1.4)))
    # FRANSIZCA damgası (konum FR_XY: kurul tur 3 TE2-G4 — #8 yakın planında sağ kenara taşıyordu)
    if fr_at is not None:
        k = cx.amt(fr_at, 0.3)
        if k > 0:
            _paper_stamp(f, "FRANSIZCA", FR_XY[0], FR_XY[1], rot=-0.12, size=86, color="#A8321E", alpha=1.0, t=k)
            anim.hint_pop(cx, FR_XY[0], FR_XY[1], anim.cm_stamp_box("FRANSIZCA", 86), fr_at, 0.3, anim.cm_stamp_scale, rot=-0.12)   # ENG-E (AN1-Y7)
    # ITALIANO (elle yazılır) + sinabar çizgi
    if it_at is not None:
        k = clamp((cx.t - cx.at(it_at)) / 0.55)
        if k > 0:
            txt = "ITALIANO"
            tw = sk.text_width(txt, "fell_i", 78)
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(-tw / 2 - 10, -260, -tw / 2 + tw * ease_io(k, 1.6) + 8, -120))
            _hand(f, txt, 0, -170, 78, ink, 1.0, seed=11, align="c")
            c.restore()
            if it_strike_at is not None:
                sa = cx.amt(it_strike_at, 0.5)
                if sa > 0:
                    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7.0, Color=sk.C("#A8321E", 245), StrokeCap=skia.Paint.kRound_Cap)
                    p.setPathEffect(skia.DiscretePathEffect.Make(12.0, 1.6, 2))
                    c.drawLine(-tw / 2 - 22, -198, -tw / 2 - 22 + (tw + 44) * ease_io(sa, 1.6), -190, p)
    c.restore()
    # çevre karartma (III. madde vurgusunda): ekranın kalanı kararır
    if scrim_at is not None:
        k = cx.amt(scrim_at, 0.7)
        if hl_out is not None:
            k *= 1.0 - cx.amt(hl_out, 0.5)
        if k > 0.003:
            yb = py + LINE_Y[2] * s
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(0, yb - 40 * s, W, yb + 24 * s), skia.ClipOp.kDifference)
            f.rect(0, 0, W, H, color="#0C0806", alpha=0.62 * k)
            c.restore()
    cam.end(f) if False else None
    CM.finish(f, cx, motes_n=14, light=CM.candle_light(cx.t, 3, base=(W * 0.5, H * 0.5), r=1250.0, sway=4.0))


# ─────────────────────────────────────────────────────────────────────────────
# c0_kuyruk — bugünün Uffizi kuyruğu (siluet)
# ─────────────────────────────────────────────────────────────────────────────
import cilt_anim as FA  # noqa: E402

_Q = dict(by0=150, bh=800)


def _sil_person(f, x, yg, h, phase, walk, kind, alpha=1.0, col="#2A1E15", rim="#E8B070"):
    """Yandan (sağa bakan) düz koyu siluet; yürüme: bacak/kol salınımı. kind: plain | pack | phone | hat | child | long."""
    c = f.c
    w = walk
    hh = h * (0.72 if kind == "child" else 1.0)
    sw = math.sin(phase) * w
    sw2 = -sw
    pa = skia.Paint(AntiAlias=True, Color=sk.C(col, int(255 * alpha)))
    leg = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=hh * 0.072, Color=sk.C(col, int(255 * alpha)), StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    arm = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=hh * 0.050, Color=sk.C(col, int(255 * alpha)), StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    hipy = yg - hh * 0.50
    # bacaklar (arka önce)
    for s_ in (sw2, sw):
        kx = x + s_ * hh * 0.07
        ky = yg - hh * 0.26
        fx = x + s_ * hh * 0.12
        fy = yg - hh * 0.018 - max(0.0, math.sin(phase + (0 if s_ == sw else math.pi))) * hh * 0.035 * w
        pth = skia.Path()
        pth.moveTo(x, hipy + hh * 0.02)
        pth.lineTo(kx, ky)
        pth.lineTo(fx, fy)
        c.drawPath(pth, leg)
        c.drawOval(skia.Rect.MakeLTRB(fx - hh * 0.035, fy - hh * 0.012, fx + hh * 0.085, fy + hh * 0.02), pa)
    # gövde (omuz → kalça; ceket ya da uzun palto)
    ext = 0.14 if kind == "long" else 0.0
    tor = skia.Path()
    tor.moveTo(x - hh * 0.085, yg - hh * 0.80)
    tor.cubicTo(x - hh * 0.02, yg - hh * 0.84, x + hh * 0.07, yg - hh * 0.83, x + hh * 0.095, yg - hh * 0.78)
    tor.cubicTo(x + hh * 0.105, yg - hh * 0.66, x + hh * 0.085, yg - hh * 0.56, x + hh * 0.082, yg - hh * (0.45 - ext))
    tor.lineTo(x - hh * 0.082, yg - hh * (0.45 - ext))
    tor.cubicTo(x - hh * 0.085, yg - hh * 0.56, x - hh * 0.10, yg - hh * 0.68, x - hh * 0.085, yg - hh * 0.80)
    tor.close()
    c.drawPath(tor, pa)
    if kind == "pack":
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - hh * 0.175, yg - hh * 0.78, x - hh * 0.06, yg - hh * 0.50), hh * 0.04, hh * 0.04), pa)
    # kollar
    shx, shy = x + hh * 0.005, yg - hh * 0.775
    if kind == "phone":
        hx, hy = x + hh * 0.19, yg - hh * 0.94
        pth = skia.Path(); pth.moveTo(shx, shy); pth.lineTo(x + hh * 0.13, yg - hh * 0.72); pth.lineTo(hx, hy)
        c.drawPath(pth, arm)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(hx - hh * 0.014, hy - hh * 0.085, hx + hh * 0.034, hy + hh * 0.006), 2, 2), pa)
        c.drawRect(skia.Rect.MakeLTRB(hx + hh * 0.010, hy - hh * 0.072, hx + hh * 0.027, hy - hh * 0.008), skia.Paint(Color=sk.C("#F2C27A", int(215 * alpha))))
    else:
        for s_ in (sw2, sw):
            hx = shx + s_ * hh * 0.11 + hh * 0.02
            hy = yg - hh * 0.50
            pth = skia.Path(); pth.moveTo(shx, shy); pth.lineTo(shx + s_ * hh * 0.05, yg - hh * 0.64); pth.lineTo(hx, hy)
            c.drawPath(pth, arm)
    # baş + boyun
    hr = hh * 0.068
    hx, hy = x + hh * 0.018, yg - hh * 0.905
    c.drawRect(skia.Rect.MakeLTRB(hx - hh * 0.028, hy + hr * 0.4, hx + hh * 0.030, yg - hh * 0.79), pa)
    c.drawOval(skia.Rect.MakeLTRB(hx - hr * 1.05, hy - hr, hx + hr * 1.12, hy + hr * 1.05), pa)
    if kind == "hat":
        c.drawOval(skia.Rect.MakeLTRB(hx - hr * 2.0, hy - hr * 0.95, hx + hr * 2.1, hy - hr * 0.35), pa)
        c.drawOval(skia.Rect.MakeLTRB(hx - hr * 1.0, hy - hr * 1.65, hx + hr * 1.0, hy - hr * 0.5), pa)
    rp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.8, Color=sk.C(rim, int(130 * alpha)))
    c.drawArc(skia.Rect.MakeLTRB(hx - hr, hy - hr, hx + hr, hy + hr), -70, 110, False, rp)


def _arcade(f, x0, x1, gy, T):
    """Revaklı cephe (Uffizi revağı, stilize): taş sütunlar + kemerler + üst pencere katı + silme. Dünya koordinatında yatay tekrar."""
    c = f.c
    stone, stone_d, shade = "#CDBB93", "#A8966F", "#4B3C2E"
    mod = 380.0
    i0, i1 = int(x0 // mod) - 1, int(x1 // mod) + 2
    # üst duvar
    f.rect(x0 - 40, gy - 630, x1 - x0 + 80, 150, color="#D6C59E")
    for i in range(i0, i1):
        xa = i * mod
        # pencere (üst kat)
        wx = xa + mod / 2
        f.rect(wx - 44, gy - 612, 88, 104, color="#5A4630")
        f.rect(wx - 44, gy - 612, 88, 104, style="stroke", sw=4, color="#E8DABA")
        f.rect(wx - 56, gy - 626, 112, 14, color="#E8DABA")
        c.drawLine(wx, gy - 612, wx, gy - 508, f.paint("#E8DABA", style="stroke", sw=3))
    # silme
    f.rect(x0 - 40, gy - 480, x1 - x0 + 80, 26, color="#E3D3AC")
    f.rect(x0 - 40, gy - 454, x1 - x0 + 80, 10, color="#9A8860")
    f.rect(x0 - 40, gy - 650, x1 - x0 + 80, 22, color="#E3D3AC")
    # revak: derin gölgeli kemer boşlukları
    f.rect(x0 - 40, gy - 444, x1 - x0 + 80, 444, color="#6A5640")
    for i in range(i0, i1):
        xa = i * mod
        cxm = xa + mod / 2
        aw = mod - 96
        arch = skia.Path()                       # düz arşitravlı açıklık (Uffizi revağı: kemer yok — kurul SA2-K1)
        arch.moveTo(cxm - aw / 2, gy)
        arch.lineTo(cxm - aw / 2, gy - 360)
        arch.lineTo(cxm + aw / 2, gy - 360)
        arch.lineTo(cxm + aw / 2, gy)
        arch.close()
        c.drawPath(arch, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, gy - 440), (0, gy)], [sk.C("#2A2018"), sk.C("#6E5A42")], [0, 1])))
        c.drawPath(arch, f.paint("#E3D3AC", style="stroke", sw=9))
        # iç kemer (derinlik)
        c.drawPath(arch, f.paint("#3A2C20", style="stroke", sw=2, alpha=0.8))
        # sütun
        f.rect(xa - 24, gy - 444, 48, 444, color=stone)
        f.rect(xa - 24, gy - 444, 12, 444, color=mix(stone, "#FFFFFF", 0.35))
        f.rect(xa + 12, gy - 444, 12, 444, color=mix(stone, "#000000", 0.22))
        f.rect(xa - 32, gy - 24, 64, 24, color=stone_d)
        f.rect(xa - 32, gy - 452, 64, 18, color="#E3D3AC")


def _portal(f, x, gy, glow):
    """Büyük giriş kapısı: kemerli, içeriden sıcak ışık."""
    c = f.c
    w, h = 330, 440
    arch = skia.Path()                           # dikdörtgen kapı (düz lento)
    arch.moveTo(x - w / 2, gy)
    arch.lineTo(x - w / 2, gy - h + 40)
    arch.lineTo(x + w / 2, gy - h + 40)
    arch.lineTo(x + w / 2, gy)
    arch.close()
    c.drawPath(arch, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, gy - h), (0, gy)], [sk.C("#FFE2A0"), sk.C("#F0A850")], [0, 1])))
    f.circle(x, gy - 160, 280, shader=f.rad(x, gy - 160, 280, [("#FFD58A", 0.0, int(120 * glow)), ("#FFD58A", 1.0, 0)]))
    c.drawPath(arch, f.paint("#E8D9B4", style="stroke", sw=22))
    c.drawPath(arch, f.paint("#7A6544", style="stroke", sw=3))


@ckind("c0_kuyruk")
def k_kuyruk(cx, scroll=(1180.0, 2020.0), sign_at=None, kick_at=None, kick="BUGÜN", coin_at=None, seed=5, walk_hz=1.0 / 2.6, n=19, **_):
    f = cx.f
    c = f.c
    by0, bh = _Q["by0"], _Q["bh"]
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    u = clamp(cx.t / max(1e-6, cx.dur))
    cam_st = getattr(cx, "cam_state", None)
    kin, kout = bool(getattr(cx, "cut_in", False)), bool(getattr(cx, "cut_out", False))
    if kin or kout:                  # ENG-E (kurul tur 3 AN1-Y-N3 taraması): kendi kaydırması sert kesmeyle birleşen uçta durmasın (cilt_cam.CUT_SLOPE; #14 77,97 sn)
        s0, s1 = (cilt_cam.CUT_SLOPE if kin else 0.0), (cilt_cam.CUT_SLOPE if kout else 0.0)
        scr = lerp(scroll[0], scroll[1], cilt_cam.hermite(u, s0, s1))
    else:
        scr = lerp(scroll[0], scroll[1], ease_io(u, 2.0))
    zoom = (cam_st.s if cam_st is not None else 1.0)
    gy = 860.0
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, by0, W, by0 + bh))
    # zum (kamera cam=push): içerik merkezden büyür
    c.translate(W / 2, by0 + bh * 0.55)
    c.scale(zoom, zoom)
    c.translate(-W / 2, -(by0 + bh * 0.55))
    # gökyüzü
    sky = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, by0), (0, gy - 450)], [sk.C("#F3E7C8"), sk.C("#E9D3A4")], [0, 1]))
    c.drawRect(skia.Rect.MakeLTRB(0, by0, W, gy - 440), sky)
    # uzak: Palazzo Vecchio kulesi (siluet, hafif sisli)
    tx = 2860 - scr * 0.35
    tcol = "#B3A28A"
    f.rect(tx - 54, gy - 1000, 108, 380, color=tcol)
    f.rect(tx - 90, gy - 1030, 180, 52, color=mix(tcol, "#000000", 0.08))
    for k in range(6):
        f.rect(tx - 90 + k * 31, gy - 1056, 18, 26, color=mix(tcol, "#000000", 0.08))
    f.rect(tx - 40, gy - 1160, 80, 130, color=tcol)
    f.poly([(tx - 52, gy - 1160), (tx, gy - 1250), (tx + 52, gy - 1160)], color=mix(tcol, "#000000", 0.1))
    f.rect(tx - 120, gy - 700, 300, 90, color=mix(tcol, "#FFFFFF", 0.12))
    # cephe (yakın)
    c.save()
    c.translate(-scr, 0)
    _arcade(f, scr - 60, scr + W + 60, gy, TH)
    pxw = 3140.0
    glow = 0.8 + 0.2 * math.sin(cx.t * 2.1)
    _portal(f, pxw, gy, glow)
    # tabela (script'te geçen ad: Uffizi)
    if sign_at is not None:
        k = cx.amt(sign_at, 0.7)
        if k > 0.003:
            sp = CM.gilt("UFFİZİ", "title", 56, 14.0)          # kanal kuralı: ekran yazısı sk.tr_upper (kurul tur 2 TE2-Ö12)
            CM.draw_spr(f, sp, pxw, gy - 470, "c", alpha=k, glow=0.25 * k, shadow=0.4)
    # zemin
    f.rect(scr - 80, gy, W + 160, 120, color="#B9A682")
    f.rect(scr - 80, gy, W + 160, 6, color="#8A7650")
    for i in range(int((scr - 80) // 150) - 1, int((scr + W + 80) // 150) + 2):
        c.drawLine(i * 150, gy, i * 150 - 60, gy + 120, f.paint("#8A7650", style="stroke", sw=2, alpha=0.5))
    # kuyruk: iki sıra, adım adım ilerler
    import random
    rs = random.Random(seed)
    kinds = ["plain", "pack", "phone", "hat", "plain", "long", "pack", "child", "phone", "plain", "hat", "pack", "plain", "long", "phone", "plain", "pack", "hat", "plain", "child"]
    step_len = 74.0
    T0 = cx.t * walk_hz
    nstep = math.floor(T0)
    fr = T0 - nstep
    mv = smooth(clamp(fr / 0.55))
    people = []
    for i in range(n):
        row = i % 2
        base = pxw - 120 - i * 66 - row * 20 + rs.uniform(-8, 8)
        xw = base + step_len * (nstep + mv)
        walkamp = 1.0 if (0.0 < fr < 0.6) else 0.0
        hh = 300 if row == 0 else 262
        yg = gy + (46 if row == 0 else 14)
        al = 1.0
        door_in = clamp((xw - (pxw - 120)) / 120.0)
        if door_in > 0:
            al = 1.0 - door_in
            if al <= 0.01:
                continue
        people.append((yg, xw, hh, i, row, al, walkamp, kinds[i % len(kinds)]))
    people.sort()
    for (yg, xw, hh, i, row, al, wa, kd) in people:
        # yer gölgesi
        f.oval(xw + 10, yg + 2, hh * 0.22, hh * 0.026, color="#000000", alpha=0.25 * al)
        _sil_person(f, xw, yg, hh, cx.t * 6.2 + i * 1.3, 0.55 if wa > 0 else 0.0, kd, alpha=al, col="#2A1E15" if row == 0 else "#3A2C20")
    # sikke (müşteri): kuyruğun başından sırayla
    if coin_at is not None:
        t0c = cx.at(coin_at)
        for j, (yg, xw, hh, i, row, al, wa, kd) in enumerate(sorted(people, key=lambda q: -q[1])[:11]):
            ph = clamp((cx.t - (t0c + 0.11 * j)) / 0.95)
            if 0 < ph < 1:
                cyc = yg - hh * 1.06 - 120 * ph
                a_ = math.sin(ph * math.pi)
                rx = 15 * abs(math.cos(ph * 9 + j))
                f.circle(xw, cyc, 20, shader=f.rad(xw, cyc, 24, [("#FFF0B0", 0.0, int(170 * a_)), ("#F0C050", 1.0, 0)]))
                f.oval(xw, cyc, max(3.0, rx), 15, color="#E8B840", alpha=0.95 * a_)
                f.oval(xw, cyc, max(3.0, rx), 15, style="stroke", sw=1.6, color="#7A5A1E", alpha=0.9 * a_)
    c.restore()
    # kuşlar
    for b in range(5):
        bx = (b * 410 + cx.t * (60 + 14 * b)) % (W + 200) - 100
        by = by0 + 70 + (b * 37) % 90 + math.sin(cx.t * 0.9 + b) * 14
        fl = math.sin(cx.t * 9 + b * 2.0) * 5
        pth = skia.Path(); pth.moveTo(bx - 9, by + fl * 0.4); pth.quadTo(bx - 4, by - 4 - fl, bx, by); pth.quadTo(bx + 4, by - 4 - fl, bx + 9, by + fl * 0.4)
        c.drawPath(pth, f.paint("#3A2A1A", style="stroke", sw=2.2, alpha=0.55))
    c.restore()
    # çerçeve bantları
    for yy in (by0 - 40, by0 + bh):
        FA.vine_band(f, yy, 1.0)
        c.drawLine(-40, yy + (40 if yy < by0 else 0), W + 40, yy + (40 if yy < by0 else 0), f.paint(TH.gold, style="stroke", sw=2.6, alpha=0.9))
    CM.finish(f, cx, motes_n=22)
    if kick_at is not None:                      # kurul SA1-Ö1/TE2: kicker okunur levha (ekran uzayı, ≥46 px, koyu zemin, kenardan içeride)
        k = cx.amt(kick_at, 0.6)
        if k > 0.003:
            sz = 48
            wd = sk.text_width(kick, "title_m", sz, 16) + 64
            yk = 196 + (1 - k) * 14
            f.rrect(W / 2 - wd / 2, yk - 52, wd, 74, 12, color="#120C08", alpha=0.80 * k)
            f.rrect(W / 2 - wd / 2, yk - 52, wd, 74, 12, style="stroke", sw=2.0, color="#C9A45A", alpha=0.85 * k)
            CM.ink(f, kick, W / 2, yk, face="title_m", size=sz, color="#FFF4D6", align="c", track=16, alpha=k, emboss=False)


# ─────────────────────────────────────────────────────────────────────────────
# c0_sikke — kılıçlar değil, altın sikke; geri sarma yıl sayacı
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c0_sikke")
def k_sikke(cx, sw_at=None, no_at=None, coin_at=None, cd_a=None, cd_b=None, y_from=1737, y_to=1252, seed=2, **_):
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.04, drift=(4.0, 1.5))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    cam.begin(f)
    cxm, cym = W / 2, 440
    # açılış: önceki çekimin soru işareti (cevap aranıyor) → kılıçlarla yer değiştirir
    if sw_at is not None:
        kq = 1.0 - cx.amt(sw_at, 0.3, off=-0.05)
        if kq > 0.003:
            f.circle(cxm, cym, 260, shader=f.rad(cxm, cym, 260, [("#F0D27A", 0.0, int(80 * kq)), ("#F0D27A", 1.0, 0)]))
            icons.draw_icon(f, "question", cxm, cym, size=330 * (0.9 + 0.1 * kq), metal="gold", alpha=kq, rot=0.08 * math.sin(cx.t * 3.0), glow=0.0)
    # kılıçlar
    ks = cx.amt(sw_at, 0.35) if sw_at is not None else 0.0
    kc = cx.amt(coin_at, 0.9) if coin_at is not None else 0.0
    if ks > 0.003:
        out = smooth(clamp((cx.t - cx.at(coin_at)) / 0.9)) if coin_at is not None else 0.0
        sc = 0.8 + 0.2 * sk.back_out(ks)
        shake = 6.0 * math.sin(cx.t * 60) * max(0.0, 1.0 - (cx.t - cx.at(sw_at)) / 0.35) if cx.t > cx.at(sw_at) else 0.0
        sx = cxm - 520 * out + shake
        icons.draw_icon(f, "swords", sx, cym, size=470 * sc, metal="silver", alpha=ks * (1 - 0.9 * out), glow=0.0)
        if no_at is not None:
            kn = cx.amt(no_at, 0.32)
            if kn > 0:
                L = 330
                for sgn in (1, -1):
                    p = f.paint("#B33620", style="stroke", sw=22, alpha=0.95 * (1 - out), cap="round")
                    CM.wobble(p, 14.0, 2.0, 3 + sgn)
                    c.drawLine(sx - sgn * L * kn * 0.5 + 0, cym - L * 0.5 * kn * 1, sx + sgn * L * kn * 0.5, cym + L * 0.5 * kn, p)
    # sikke: sağdan yuvarlanarak girer, sonra dönerek durur
    if kc > 0.003:
        e = ease_out(clamp((cx.t - cx.at(coin_at)) / 1.0), 3)
        x = lerp(W + 380, cxm, e)
        spin = cx.t * 0.9 + 0.35 + (1 - e) * 14.0
        size = 470 * (0.92 + 0.08 * e)
        gl = (cx.t * 0.42 + 0.2) % 2.0
        for g in (3, 2, 1):
            if e < 0.97:
                CP.draw_coin(f, x + g * 46 * (1 - e) * 2.0, cym + math.sin(cx.t * 1.2) * 6, size, spin=spin - g * 0.5, alpha=0.18 * kc, shadow=0.0)
        CP.draw_coin(f, x, cym + math.sin(cx.t * 1.2) * 6, size, spin=spin, alpha=kc, shadow=0.55, glow=0.22 * kc, glint=gl if gl < 1 else None)
        if e < 1.0:                                           # ENG-E (kurul tur 3 AN1-Y7): yuvarlanan sikkenin gerçek hızı (≈110–170 px/kare; akış ≈20 ölçüyordu) → deklanşör
            tc_ = cx.at(coin_at)

            def _coin_pts(tt):
                e_ = ease_out(clamp((tt - tc_) / 1.0), 3)
                x_, y_ = lerp(W + 380, cxm, e_), cym + math.sin(tt * 1.2) * 6
                sz_ = 470 * (0.92 + 0.08 * e_)
                hw_ = 0.5 * sz_ * max(0.012, abs(math.cos(tt * 0.9 + 0.35 + (1 - e_) * 14.0)))
                return [(x_ - hw_, y_), (x_ + hw_, y_), (x_, y_ - sz_ / 2), (x_, y_ + sz_ / 2), (x_, y_)]
            anim.hint_pts(cx, _coin_pts(cx.t - anim.DT_HINT / 2), _coin_pts(cx.t + anim.DT_HINT / 2))
    # geri sarma halkası + yıl sayacı
    if cd_a is not None and cd_b is not None:
        ta, tb = cx.at(cd_a), cx.at(cd_b)
        p = clamp((cx.t - ta) / max(1e-3, tb - ta))
        pe = ease_io(p, 2.4)
        a0 = cx.amt(cd_a, 0.5)
        if a0 > 0.003:
            R = 372.0
            ang0 = -pe * 900.0
            f.circle(cxm, cym, R - 6, style="stroke", sw=2.2, color="#F0D27A", alpha=0.35 * a0)
            for i in range(72):
                a = math.radians(ang0 + i * 5.0)
                big = (i % 6 == 0)
                r0, r1 = R, R + (38 if big else 18)
                col = "#F6DC90" if not TH.day else "#8A6422"
                c.drawLine(cxm + math.cos(a) * r0, cym + math.sin(a) * r0, cxm + math.cos(a) * r1, cym + math.sin(a) * r1,
                           f.paint(col, style="stroke", sw=5.0 if big else 2.8, alpha=min(1.0, (1.0 if big else 0.7) * a0)))
            # geri dönen ok ucu (saat yönünün tersi)
            ta_ = math.radians(ang0 - 20)
            f.circle(cxm + math.cos(ta_) * (R + 62), cym + math.sin(ta_) * (R + 62), 7, color="#F0D27A", alpha=0.9 * a0)
        v = int(round(lerp(y_from, y_to, pe)))
        txt = str(v)
        sp = _gilt_or_ink(txt, "title", 175, 10.0)
        landed = clamp((cx.t - tb) / 0.4)
        sc = 1.0 + 0.10 * (1 - sk.back_out(clamp(landed))) * (1 if p >= 1 else 0)
        CM.draw_spr(f, sp, cxm, 884, "c", alpha=a0, scale=sc, shadow=0.55 if not TH.day else 0.0, glow=(0.16 + 0.22 * landed) if not TH.day else 0.0)
    cam.end(f)
    CM.finish(f, cx, motes_n=34)


# ─────────────────────────────────────────────────────────────────────────────
# c0_sinir — "Floransa'dan ve Büyük Dukalık'tan çıkarılamayacaktı": harita + sınır + zincir + özet kartı
# (map türünün extra= kancası; Büyük Dukalık çokgeni medici_regions'taki YAKLAŞIK toskana çokgenidir)
# ─────────────────────────────────────────────────────────────────────────────
TOSKANA = [(9.95, 42.90), (10.20, 43.95), (10.60, 44.10), (11.30, 44.20), (11.85, 44.12), (12.25, 43.85), (12.30, 43.30), (11.95, 42.62), (11.30, 42.30), (10.70, 42.35), (10.10, 42.60)]
FLO = (11.25, 43.77)


def sinir_extra(cx, cm, mv, border_at=None, label_at=None, items_at=None, lock_at=None, quote_at=None, quote_out=None):
    """Harita üstü: hazine simgeleri Floransa'da → sınır çizilir → simgeler dışarı yönelir, zincir kilitlenir → özet kartı."""
    f = cx.f
    c = f.c
    # sınır: map türünün kendi bölge dolgusu (kıyıya kırpılır; YAKLAŞIK sınır) — çokgen çizgisi çizilmez
    fx, fy = cm.ll(*FLO)
    # hazine simgeleri: Floransa çevresinde süzülür; kilit anında sınıra doğru yönelir ve geri sekir
    if items_at is not None:
        kinds_ = [("chest", -200, -60), ("scroll", -105, -140), ("crown", 0, -175), ("book_open", 105, -140), ("ring", 200, -60)]
        tl = cx.at(lock_at) if lock_at is not None else 1e9
        for i, (ic, ox, oy) in enumerate(kinds_):
            k = cx.amt(items_at, 0.5, off=0.12 * i)
            if k <= 0.003:
                continue
            bob = math.sin(cx.t * 2.0 + i * 1.4) * 6
            # çıkış denemesi: sağa (doğuya) uzanır, sınırda durur
            dt = clamp((cx.t - (tl + 0.05 * i)) / 0.40)
            reach = math.sin(dt * math.pi) * (210 + 20 * i) if dt < 1.0 else 0.0
            x = fx + ox + reach
            y = fy + oy + bob
            f.circle(x, y + 36, 30, color="#000000", alpha=0.18 * k, blur=6)
            icons.draw_icon(f, ic, x, y, size=104 * (0.8 + 0.2 * sk.back_out(k)), metal="gold", alpha=k, glow=0.0)
    # ZİNCİR + ASMA KİLİT (kapak K1 motifi; kurul C-c0 / PK2-K5): "çıkarılamayacaktı"da iki zincir hazine kümesini sarar, kilit iner ve kulp kapanır
    if lock_at is not None:
        import kapak_medici as KP
        import anim
        tl = cx.at(lock_at)
        kl = clamp((cx.t - (tl - 0.55)) / 0.55)
        if kl > 0.003:
            ky = fy + 40
            B = 150
            R = B * 0.30
            leg_y = ky - B * 0.10
            e = ease_out(kl, 2.2)
            pl = (fx - R - B * 0.02, leg_y)
            pr = (fx + R + B * 0.02, leg_y)
            a0 = (lerp(pl[0] - 900, pl[0], e), lerp(leg_y + 60, leg_y, e))
            a1 = (lerp(pr[0] + 900, pr[0], e), lerp(leg_y + 60, leg_y, e))
            KP.draw_chain(f, (fx - 980, fy + 120), a0, sag=50, L=B * 0.40)
            KP.draw_chain(f, a1, (fx + 980, fy + 130), sag=50, L=B * 0.40)
            yy = ky - 260 * (1.0 - anim.settle(cx.t, tl - 0.25, 0.35, 0.10))
            t_cl = clamp((cx.t - tl) / 0.22)
            drop = (1.0 - sk.back_out(t_cl)) * B * 0.12
            f.circle(fx, yy + B * 0.4, B * 1.4, shader=f.rad(fx, yy + B * 0.4, B * 1.4, [("#FFB454", 0.0, int(70 * kl)), ("#FFB454", 1.0, 0)]))
            KP.draw_padlock(f, fx, yy, B, drop=drop)
            fl = clamp((cx.t - tl) / 0.40)
            if 0 < fl < 1:
                f.circle(fx, yy + 40, 300 * fl, shader=f.rad(fx, yy + 40, 300 * fl + 1, [("#FFF1B8", 0.0, int(160 * (1 - fl))), ("#FFF1B8", 1.0, 0)]))
            dx, dy = anim.shake(cx.t, tl, 0.25, 4.0, seed=3)
            if dx or dy:
                anim.jolt(f, dx, dy)
    # 3. MADDE · ÖZET kartı — ALINTI DEĞİL (tırnak yok; kurul KA2-Ö5): anlatımla aynı yüklem
    if quote_at is not None:
        k = cx.amt(quote_at, 0.6)
        if quote_out is not None:
            k *= 1.0 - cx.amt(quote_out, 0.6)
        if k > 0.003:
            head = "3. MADDE · ÖZET"
            l1, l2 = "Koleksiyonlar Floransa'dan ve", "Büyük Dukalık'tan çıkarılamaz."
            sz = 56
            wd = max(sk.text_width(l1, "cap_b", sz), sk.text_width(l2, "cap_b", sz)) + 160
            x0, y0, hh = W / 2 - wd / 2, 600 + (1 - k) * 24, 300
            f.rrect(x0 + 6, y0 + 10, wd, hh, 14, color="#000000", alpha=0.35 * k, blur=10)
            f.rrect(x0, y0, wd, hh, 14, color="#120C08", alpha=0.92 * k)
            f.rrect(x0, y0, wd, hh, 14, style="stroke", sw=2.4, color="#C9A45A", alpha=0.9 * k)
            CM.ink(f, head, W / 2, y0 + 62, face="title_m", size=42, color="#F6D886", align="c", track=12, alpha=k, emboss=False)
            CM.flourish_rule(f, W / 2, y0 + 88, 380, alpha=k, grow=k)
            CM.ink(f, l1, W / 2, y0 + 168, face="cap_b", size=sz, color="#FFF4D6", align="c", alpha=k, emboss=False)
            CM.ink(f, l2, W / 2, y0 + 236, face="cap_b", size=sz, color="#FFF4D6", align="c", alpha=k, emboss=False)
    # SINIR YAKLAŞIKTIR (kurul KA2-Ö5 / SA2-Ö5): temsilî sınır uyarısı (kalıcı, küçük)
    # (uyarı levhası artık ekran uzayında: sahne dosyasında P.tag("SINIR YAKLAŞIKTIR", …) — kamera kaydırmasıyla kenarda kırpılmasın)
    if label_at is not None:
        k = cx.amt(label_at, 0.7)
        if k > 0.003:
            a0 = cm.ll(10.10, 44.28)
            CM.ink(f, "BÜYÜK DUKALIK", W / 2 + 40, 200, face="title", size=54, color="#2E2012" if TH.day else "#F4E9CB", align="c", track=16, alpha=k)


_TOSK_DONE = [False]


def ensure_toskana(mv):
    """map türünün `clip_to_land` kırpması projeksiyon uyumsuzluğundan boş çıkıyor (notlar_c0.md: motordan istek). Burada çokgeni lon/lat'ta İtalya karasına kırpıp
    `mv.D['regions']['c0_toskana']` olarak ekliyoruz (YAKLAŞIK sınır)."""
    if _TOSK_DONE[0]:
        return
    import mapdata
    from shapely.geometry import Polygon
    land = mapdata._countries()["Italy"]
    g = Polygon(TOSKANA).buffer(0).intersection(land)
    mv.D["regions"]["c0_toskana"] = mapdata._levels(mapdata._project(g))
    for k in [k for k in mv._paths if isinstance(k, tuple) and k[0] == "c0_toskana"]:
        del mv._paths[k]
    _TOSK_DONE[0] = True


@ckind("c0_harita")
def k_harita(cx, **kw):
    import shots as SH
    ensure_toskana(SH.mapview())
    SH.KINDS["map"](cx, **kw)


# ─────────────────────────────────────────────────────────────────────────────
# galeri üstü: 3. maddenin sıraladığı beş kalem (ÇEVİRİ damgalı) — p1_pano ovl'u
# ─────────────────────────────────────────────────────────────────────────────
def hazine_ovl(items, stamp_at=None, y_icon=760, y_lab=888, size=118, gap=330):
    """items=[(simge, etiket, çapa)] — çapada simge yaldız-kabartma olarak belirir, altına Cinzel etiket yazılır; satır tamamlanınca parlar."""
    def fn(cx):
        f = cx.f
        n = len(items)
        x0 = W / 2 - gap * (n - 1) / 2
        # yarı saydam şerit (okunurluk)
        ks = [cx.amt(a, 0.5) for (_, _, a) in items]
        band = max(ks) if ks else 0.0
        if band > 0.003:
            f.rect(0, y_icon - 110, W, 310, shader=f.lin(0, y_icon - 110, 0, y_icon + 200, [("#120C06", 0.0, 0), ("#120C06", 0.24, int(185 * band)), ("#120C06", 0.80, int(185 * band)), ("#120C06", 1.0, 0)]))
        for i, (ic, lab, a) in enumerate(items):
            k = cx.amt(a, 0.45)
            if k <= 0.003:
                continue
            x = x0 + i * gap
            sc = 0.7 + 0.3 * sk.back_out(k)
            f.circle(x, y_icon, size * 0.78, shader=f.rad(x, y_icon, size * 0.78, [("#F0D27A", 0.0, int(70 * k)), ("#F0D27A", 1.0, 0)]))
            icons.draw_icon(f, ic, x, y_icon - 8 * (1 - k), size=size * sc, metal="gold", alpha=k, glow=0.0)
            for j, ln in enumerate(lab.split("\n")):
                szl = CM.fit_size(ln, "title_m", 30, gap - 26, 5)
                CM.ink(f, ln, x, y_lab + j * 30 - (15 if "\n" in lab else 0), face="title_m", size=szl, color="#F6E7B6", align="c", track=5, alpha=k, emboss=False)
    return fn


def soru_ovl(at, x=1480, y=470, size=330, out=None):
    """Büyük yaldız soru işareti (bir kez 'pop' yapar, sallanır)."""
    def fn(cx):
        k = cx.amt(at, 0.4)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k <= 0.003:
            return
        f = cx.f
        sc = 0.6 + 0.4 * sk.back_out(k)
        rot = 0.08 * math.sin(cx.t * 3.0)
        f.circle(x, y, size * 0.7, shader=f.rad(x, y, size * 0.7, [("#F0D27A", 0.0, int(90 * k)), ("#F0D27A", 1.0, 0)]))
        icons.draw_icon(f, "question", x, y, size=size * sc, metal="gold", alpha=k, rot=rot, glow=0.0)
    return fn


# ─────────────────────────────────────────────────────────────────────────────
# özel simgeler (icons._ICONS'a kayıt; mevcut simgeler değişmez)
# ─────────────────────────────────────────────────────────────────────────────
def _pth(pts, close=True):
    return sk.poly_path(pts, close)


@icons.icon("c0_galeri")
def _i_galeri(m):
    m.rect(52, 84, 408, 34, r=8)
    m.rect(70, 112, 372, 52, r=6)
    m.rect(70, 160, 372, 262)
    m.rect(52, 420, 408, 44, r=8)
    for bx in (92, 208, 326):
        p = skia.Path()
        p.moveTo(bx, 420)
        p.lineTo(bx, 300)
        p.arcTo(skia.Rect.MakeLTRB(bx, 300 - 48, bx + 94, 300 + 48), 180, 180, False)
        p.lineTo(bx + 94, 420)
        p.close()
        m.cut(p)
        m.cut(_pth([(bx - 6, 164), (bx + 100, 164)], False), 6)
    for x in (80, 196, 314, 432):
        m.cut(_pth([(x, 172), (x, 414)], False), 3)


@icons.icon("c0_tablo")
def _i_tablo(m):
    m.rect(70, 100, 372, 312, r=14)
    inner = skia.Path()
    inner.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(116, 146, 396, 366), 6, 6))
    m.cut(inner)
    m.circle(318, 212, 32)
    m.poly([(116, 366), (206, 262), (268, 330), (338, 270), (396, 322), (396, 366)])
    m.cut(_pth([(150, 366), (206, 300), (240, 340)], False), 5)
    m.line(256, 100, 256, 62, 8)
    m.circle(256, 56, 12)
    for (x, y) in ((92, 122), (420, 122), (92, 390), (420, 390)):
        m.circle(x, y, 13)
        m.cut(_pth([(x - 6, y), (x + 6, y)], False), 3)


@icons.icon("c0_heykel")
def _i_heykel(m):
    m.rect(138, 428, 236, 44, r=8)
    m.rect(168, 396, 176, 38, r=6)
    m.circle(256, 118, 36)
    m.rect(240, 140, 32, 30)
    m.smooth([(200, 176), (312, 176), (330, 292), (306, 396), (206, 396), (182, 292)], close=True, t=0.35)
    m.line(310, 190, 368, 112, 30)
    m.circle(374, 104, 17)
    for (x0, y0, x1, y1) in ((226, 214, 214, 380), (256, 222, 256, 386), (286, 214, 296, 380)):
        m.cut(_pth([(x0, y0), (x1, y1)], False), 5)
    m.cut(_pth([(204, 262), (306, 292)], False), 5)


@icons.icon("c0_mucevher")
def _i_mucevher(m):
    m.poly([(176, 128), (336, 128), (432, 232), (256, 438), (80, 232)])
    for pts in ([(80, 232), (432, 232)], [(176, 128), (206, 232), (256, 438)], [(336, 128), (306, 232), (256, 438)], [(176, 128), (256, 232), (336, 128)], [(206, 232), (256, 150), (306, 232)]):
        m.cut(_pth(pts, False), 7)
    m.poly([(404, 96), (416, 124), (444, 136), (416, 148), (404, 176), (392, 148), (364, 136), (392, 124)])


# ─────────────────────────────────────────────────────────────────────────────
# c0_gerekce — üç madalyon: devletin süsü · halkın yararı · yabancıların merakı
# ─────────────────────────────────────────────────────────────────────────────
@ckind("c0_gerekce")
def k_gerekce(cx, title="GEREKÇE", items=(), draw_at=None, stamp=None, seed=1, **_):
    """items=[dict(icon, label, at)]. Madalyon halkaları `draw_at`'tan itibaren kendini çizer (boş çerçeve → simge), `at` anında simge yaldız kabartma olarak girer."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.05, drift=(4.0, 2.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="both")
    cam.begin(f)
    n = len(items)
    R = 148.0
    gap = 540.0
    x0 = W / 2 - gap * (n - 1) / 2
    yc = 520.0
    d0 = cx.at(draw_at) if draw_at is not None else 0.0
    # başlık
    kt = cx.amt(draw_at, 0.8) if draw_at is not None else 1.0
    sp = CM.engraved(title, "title", 78, 18.0, TH.fg) if TH.day else CM.gilt(title, "title", 78, 18.0)
    CM.draw_spr(f, sp, W / 2, 232, "c", alpha=kt, shadow=0.0)
    CM.flourish_rule(f, W / 2, 268, 700, alpha=kt, grow=kt)
    if stamp is not None:
        _paper_stamp(f, "ÇEVİRİ", 1500, 300, rot=-0.08, size=46, t=cx.amt(stamp, 0.3))
    import anim
    for i, it in enumerate(items):
        x = x0 + i * gap
        kd = clamp((cx.t - (d0 + 0.16 * i)) / 0.9)
        e = ease_io(kd, 2.0)
        ka = cx.amt(it["at"], 0.5)
        # hareket (kurul C-c0 "gerekçe madalyonu hareketi"): madalyon aşağıdan oturarak gelir, simge girince sallanır, ardından yavaş salınır
        ent = anim.settle(cx.t, d0 + 0.16 * i - 0.2, 0.7, 0.12)
        yc = 520.0 + 260.0 * (1.0 - ent) + 8.0 * math.sin(cx.t * 1.1 + i * 2.1)
        t_ic = cx.at(it["at"])
        rot_ic = 0.10 * anim.wobble(cx.t, t_ic + 0.2, amp=1.0, freq=2.6, decay=3.5)
        # arkada dönen ışın tacı (simge geldikten sonra)
        if ka > 0.003:
            for r_ in range(28):
                ang = math.radians(r_ * (360 / 28) + cx.t * 12 * (1 if i % 2 == 0 else -1))
                r0, r1 = R + 24, R + 24 + (46 if r_ % 2 == 0 else 24) * ka
                c.drawLine(x + math.cos(ang) * r0, yc + math.sin(ang) * r0, x + math.cos(ang) * r1, yc + math.sin(ang) * r1,
                           f.paint("#C9A24A" if TH.day else "#F0D27A", style="stroke", sw=3.0, alpha=0.65 * ka))
        # madalyon gövdesi
        f.circle(x + 6, yc + 12, R, color="#000000", alpha=0.28 * e, blur=10)
        f.circle(x, yc, R, shader=f.rad(x - R * 0.3, yc - R * 0.35, R * 1.5, [(mix(TH.plate[0], "#FFFFFF", 0.25), 0.0), (TH.plate[1], 1.0)]), alpha=e)
        # halka çizilir
        oval = skia.Rect.MakeLTRB(x - R, yc - R, x + R, yc + R)
        p1 = f.paint("#B08A34" if TH.day else "#E8C468", style="stroke", sw=12, alpha=0.95)
        c.drawArc(oval, -90, 360 * e, False, p1)
        p2 = f.paint("#5A3E1A" if TH.day else "#7A5A1E", style="stroke", sw=2.4, alpha=0.9)
        c.drawArc(skia.Rect.MakeLTRB(x - R + 14, yc - R + 14, x + R - 14, yc + R - 14), -90, 360 * e, False, p2)
        # simge
        if ka > 0.003:
            sc = 0.7 + 0.3 * sk.back_out(ka)
            pulse = 1.0 + 0.04 * math.sin(cx.t * 3 + i) * ka
            icons.draw_icon(f, it["icon"], x, yc - 6, size=210 * sc * pulse, metal="gold", alpha=ka, glow=0.0, rot=rot_ic)
            # parıltı süpürmesi (simge girişinde)
            gs = clamp((cx.t - t_ic - 0.15) / 0.7)
            if 0 < gs < 1:
                gx = x - R + 2 * R * gs
                f.circle(gx, yc - 20, 60, shader=f.rad(gx, yc - 20, 60, [("#FFF4C0", 0.0, int(150 * math.sin(gs * math.pi))), ("#FFF4C0", 1.0, 0)]))
            lsz = max(34.0, CM.fit_size(it["label"], "title_m", 40, gap - 90, 3))
            lw_ = sk.text_width(it["label"], "title_m", lsz, 3) + 56
            f.rrect(x - lw_ / 2, yc + R + 34 + (1 - ka) * 10, lw_, lsz + 34, 10, color="#120C08", alpha=0.80 * ka)
            CM.ink(f, it["label"], x, yc + R + 34 + lsz + 8 + (1 - ka) * 10, face="title_m", size=lsz, color="#FFF4D6", align="c", track=3, alpha=ka, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=24)


import p1_ortak as _P  # noqa: E402
_P.add_ovl(['c0_takvim', 'c0_belge', 'c0_kuyruk', 'c0_sikke', 'c0_harita', 'c0_gerekce'])


# ─────────────────────────────────────────────────────────────────────────────
# kurul tur 2 (SCN-1): iki satırlı koyu etiket · belgeyle kayan sayaç
# ─────────────────────────────────────────────────────────────────────────────
def tag_lines(lines, x, y, at, size=52, face="title_m", out=None, dur=0.45, track=6.0, pad=26, gap=0.20, x_min=None):
    """P.tag ile aynı görünüm (koyu yarı saydam zemin, altın kontur, krem yazı ≥7:1), ama ÇOK SATIRLI tek kutu: uzun etiket (KA2-D3 "MEDİCİ
    HANEDANININ SON ÜYESİ") yanındaki armaya taşmasın diye iki satıra bölünür. Kutu güvenli alana ve altyazı bandının üstüne kıstırılır;
    x_min: kutunun sol kenarı bundan sola geçmez (komşu öğeden kaçınma)."""
    def fn(cx):
        k = cx.amt(at, dur)
        if out is not None:
            k *= 1.0 - cx.amt(out, 0.4)
        if k <= 0.003:
            return
        f = cx.f
        sx0, sx1 = _P.SAFE_X0, _P.SAFE_X1
        sz = min(CM.fit_size(ln, face, size, sx1 - sx0 - 2 * pad, track) for ln in lines)
        wd = max(sk.text_width(ln, face, sz, track) for ln in lines) + 2 * pad
        lh = sz * 1.05
        hh = lh * len(lines) + gap * sz * (len(lines) - 1) + 2 * pad * 0.62
        x0 = max(sx0, min(sx1 - wd, x - wd / 2))
        if x_min is not None:
            x0 = max(x0, min(x_min, sx1 - wd))
        yy = min(y, _P.SUB_Y0 - hh / 2 - 6)
        top = yy - hh / 2 + (1 - k) * 8
        f.rrect(x0, top, wd, hh, 12, color="#120C08", alpha=0.74 * k)
        f.rrect(x0, top, wd, hh, 12, style="stroke", sw=2.0, color="#C9A45A", alpha=0.75 * k)
        for i, ln in enumerate(lines):
            by = top + pad * 0.62 + i * (lh + gap * sz) + lh * 0.5 + sz * 0.36
            CM.ink(f, ln, x0 + wd / 2, by, face=face, size=sz, color="#FFF4D6", align="c", track=track, alpha=k, emboss=False)
    return fn


def belge_sayac(cams, doc_xy, at, value, out=None, **kw):
    """c0_belge kamerasına BAĞLI sayaç (kurul tur 2 C1: "13 MADDE" kutusu Romen rakamlarını örtüyordu, qa_yerlesim çakışması 43,1 sn).
    Kutu belge düzleminde kâğıdın DIŞINDA, masa üstünde durur (doc_xy belge koordinatı; kâğıt x∈[−550, 550]); kamera belgeye kayarken kutu
    da kâğıtla birlikte kadrajdan çıkar (kayan nesne) ve rakamlar asla kutunun altına girmez. Boyut ekran uzayında sabit (okunurluk)."""
    def fn(cx):
        ks = _cam_keys(cx, cams)
        dxc, dyc, s = _doc_cam(cx, ks)                         # k_belge ile aynı kamera (kesme ucu eğimi dâhil)
        px, py = 960 - dxc * s, 520 - dyc * s
        _P.count_up(px + doc_xy[0] * s, py + doc_xy[1] * s, at, value, out=out, **kw)(cx)
    return fn
