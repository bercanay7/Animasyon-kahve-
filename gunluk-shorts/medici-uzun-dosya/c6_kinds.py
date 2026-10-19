"""c6_kinds — c6 «Lorenzo» özel çekim türleri (Parça 3 sahne yazarı). `scenes_c6.py` içinde import edilir; `@CM.ckind` ile kaydolur.

Dil: gündüz, sıcak sıva-kâğıt (perde ALTIN); anlatı sıcak ve hafif; Giostra'dan sonra ışık soğur (kapı: Giuliano).
Kaynak disiplini: yüz yok (stilize madalya/siluet), şiddet yok; ekrana yalnız script/brif sözcükleri yazılır. Ten rengi/ses/koku alayı YOK.
Tüm zamanlar cümle/sözcük çapalı (cx.at / cx.amt); mutlak saniye yok.
"""
import math

import numpy as np
import skia

import cilt_anim as FA
import cilt_cam
import cilt_kinds2 as K2
import cilt_medal as CMD
import cilt_medici as CM
import cilt_paper as PP
import icons
import p3_lib as L
import sk
from cilt_medici import TH
from p3_lib import INK, INKR, P, S, FILLP, GRAD_V, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth
from sk import C, H, W

INK_BROWN = "#2A180D"


def look(wx, wy, z=1.0, rot=0.0):
    """Anahtar kare: dünya (wx,wy) noktası ekran merkezinde, zoom z (cam=[(çapa, look(...)), …])."""
    return (z * (wx - W / 2), z * (wy - H / 2), z, rot)


def _glint(cx, at, period=1.0):
    k = clamp((cx.t - cx.at(at)) / period)
    return k if 0.0 < k < 1.0 else None


# ═════════════════════════════ c6s1–c6s2: Valori sayfası + Lorenzo madalyası ═════════════════════════════
@CM.ckind("c6_valori")
def k_valori(cx, a_page=0.0, a_med=0.0, l1=None, l2=None, l3=None, l4=None, a_gl=None, seed=3, **_):
    """Parşömen sayfa (sol) + Lorenzo madalyası (sağ). Sayfa: «NİCCOLÒ VALORİ — yakın dost», satırlar tüy kalemle yazılır; madalya mürekkep çizgisinden bronza dönüşür.
    l1..l4 = (metin, çapa): 1–2 → c6s1 (üvey ana / şefkatli ana), 3–4 → c6s2 (yüzü güzel sayılmazdı / vakarlıydı). a_med: madalyanın bronzlaştığı an; a_gl: yaldız parıltısı."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_page, 0.9)
    pw, ph = 860, 700
    pcx, pcy = 600, 520
    pp = PP.paper_image(pw, ph, seed, (238, 228, 198), "deckle", (), 44, 1.0)
    rot = -0.014 + 0.006 * math.sin(cx.t * 0.5)
    pp.draw(f, pcx, pcy, rot=rot, scale=0.97 + 0.03 * ease_out(a), alpha=a, shadow=0.6)
    c.save()
    c.translate(pcx, pcy)
    c.rotate(math.degrees(rot))
    # başlık: NİCCOLÒ VALORİ (oyma) + alt çizgi + "yakın dost"
    y = -ph / 2 + 112
    sp = CM.engraved("NİCCOLÒ VALORİ", "title_m", 50, 6.0, "#3A2616", 0.7)
    CM.draw_spr(f, sp, 0, y, "c", alpha=a * cx.amt(a_page, 0.7, off=0.3))
    CM.flourish_rule(f, 0, y + 30, 520, alpha=0.8 * a, color="#7A5A2E", grow=cx.amt(a_page, 0.8, off=0.5))
    CM.ink(f, "yakın dost", 0, y + 74, face="cap_i", size=34, color=TH.fg2, align="c", alpha=a * cx.amt(a_page, 0.6, off=0.7), emboss=False)
    ys = [y + 168, y + 244, y + 360, y + 436]
    lines = [l1, l2, l3, l4]
    quill = None
    for i, ln in enumerate(lines):
        if ln is None:
            continue
        txt, an = ln
        sz = 52 if i in (0, 2) else 50
        col = INK_BROWN
        res = K2.write_line(f, cx, txt, -ph * 0.5 + 76, ys[i], cx.at(an), "fell_i", sz, col, a, seed=60 + i, align="l")
        if res and 0.0 < res[0] < 1.0:
            quill = (res[1], res[2])
    # c6s2 ayracı: ince mürekkep çizgisi
    kk = cx.amt(l3[1], 0.5, off=-0.3) if l3 else 0.0
    if kk > 0:
        c.drawLine(-ph * 0.5 + 76, y + 300, -ph * 0.5 + 76 + 540 * kk, y + 300, S("#7A5A2E", 1.6, 150))
    c.restore()
    if quill is not None and quill[0] is not None:
        # kalem sayfa dönüşümünde; ekran koordinatına çevir
        ca, sa = math.cos(rot), math.sin(rot)
        qx = pcx + quill[0] * ca - quill[1] * sa
        qy = pcy + quill[0] * sa + quill[1] * ca
        K2.draw_quill(f, qx, qy, ang=-38.0, alpha=a)
    # madalya: önce mürekkep halka (çizim), sonra bronz
    mx, my, ms = 1440, 500, 600
    km = cx.amt(a_med, 1.1)
    ring_a = cx.amt(a_page, 0.9, off=0.6) * (1.0 - 0.85 * km)
    if ring_a > 0.01:
        pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.0, Color=C("#5A3E22", int(190 * ring_a)), StrokeCap=skia.Paint.kRound_Cap)
        pr.setPathEffect(skia.DashPathEffect.Make([18, 12], -cx.t * 22))
        c.drawCircle(mx, my, ms * 0.47, pr)
    if km > 0.01:
        gl = _glint(cx, a_gl, 1.3) if a_gl is not None else None
        CMD.draw_medal_b(f, "m_lorenzo", mx, my, ms * (0.93 + 0.07 * ease_out(km)), "bronze", alpha=km, tilt=0.16 * math.sin(cx.t * 0.55 + 0.4), glint=gl)
        CM.name_plate(f, "LORENZO DE' MEDİCİ", None, None, cx_=mx, y=my + ms * 0.54, t=cx.amt(a_med, 0.7, off=0.4), w=560)
    cam.end(f)
    CM.finish(f, cx, motes_n=24)


# ═════════════════════════════ c6s3–c6s4: ansiklopedi tarifi (ölçü çizgileri) + koku göstergesi ═════════════════════════════
@CM.ckind("c6_tarif")
def k_tarif(cx, a_head=0.0, a_nose=None, a_chin=None, a_eye=None, a_smell=None, a_attr=None, seed=5, **_):
    """Lorenzo madalyası + ince mürekkep ölçü çizgileri (Rönesans etüt sayfası): BASIK BURUN · ÖNE ÇIKIK ALT ÇENE · ZAYIF GÖRME (c6s3);
    ardından KOKU DUYUSU göstergesi (neredeyse boş) + «Valori'ye atfedilen tarif» (c6s4). Sakin, alaysız."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    mx, my, ms = 640, 530, 740
    ka = cx.amt(a_head, 0.9)
    s = ms / 640.0
    # madalya merkezine göre öznitelik noktaları (kalibre)
    P_nose = (mx + 156 * s, my + 16 * s)
    P_chin = (mx + 130 * s, my + 124 * s)
    P_eye = (mx + 80 * s, my - 50 * s)
    CMD.draw_medal_b(f, "m_lorenzo", mx, my, ms * (0.96 + 0.04 * ease_out(ka)), "bronze", alpha=ka, tilt=0.10 * math.sin(cx.t * 0.5), glint=None)
    # üst başlık
    hx = 1420
    kh = cx.amt(a_head, 0.7, off=0.4)
    if kh > 0.01:
        CM.ink(f, "ANSİKLOPEDİLERİN TARİFİ", hx, 238, face="title_m", size=34, color=TH.fg2, align="c", track=7, alpha=kh, emboss=False)
        CM.flourish_rule(f, hx, 262, 520, alpha=0.7 * kh, color="#7A5A2E", grow=kh)
    items = [("BASIK BURUN", P_nose, a_nose, 500), ("ÖNE ÇIKIK ALT ÇENE", P_chin, a_chin, 660), ("ZAYIF GÖRME", P_eye, a_eye, 340)]
    for name, pt, an, ly in items:
        if an is None:
            continue
        k = cx.amt(an, 0.7)
        if k <= 0.003:
            continue
        # kılavuz: özellikten etikete ince çizgi (çiziliyormuş gibi)
        lx = hx - 230
        kk_ = ease_io(k)
        ex = pt[0] + (lx - 14 - pt[0]) * kk_
        ey = pt[1] + (ly - pt[1]) * kk_
        c.drawLine(pt[0], pt[1], ex, ey, S("#4A3420", 2.0, 210))
        c.drawCircle(pt[0], pt[1], 7.5, P("#A8321E", 235 * k))
        c.drawCircle(pt[0], pt[1], 7.5, S(INK, 1.5, 210 * k))
        wd = sk.text_width(name, "cap_b", 40) + 64
        kk = cx.amt(an, 0.5, off=0.35)
        CM.tablet(f, lx, ly - 36 + (1 - kk) * 8, wd, 72, alpha=kk, corner=8)
        CM.ink(f, name, lx + wd / 2, ly + 12 + (1 - kk) * 8, face="cap_b", size=40, color=TH.fg, align="c", alpha=kk, emboss=False)
    # koku göstergesi
    if a_smell is not None:
        k = cx.amt(a_smell, 0.8)
        if k > 0.003:
            gx, gy, gw = hx - 250, 840, 500
            CM.ink(f, "Valori'ye atfedilen tarif", gx + gw / 2, gy - 98, face="cap_i", size=34, color=TH.fg3, align="c", alpha=0.95 * k, emboss=False)
            CM.ink(f, "KOKU DUYUSU", gx + gw / 2, gy - 44, face="title_m", size=36, color=TH.fg, align="c", track=7, alpha=k, emboss=False)
            c.save()
            c.translate(gx, gy)
            c.drawRoundRect(skia.Rect.MakeWH(gw, 26), 13, 13, P("#E8DCB8", 230 * k))
            c.drawRoundRect(skia.Rect.MakeWH(gw, 26), 13, 13, S("#4A3420", 2.0, 220 * k))
            fill = (0.045 + 0.012 * math.sin(cx.t * 1.7)) * ease_out(clamp((cx.t - cx.at(a_smell)) / 1.2))
            c.drawRoundRect(skia.Rect.MakeWH(max(8, gw * fill), 26), 13, 13, P("#A8321E", 235 * k))
            for i in range(1, 5):
                c.drawLine(gw * i / 5, 26, gw * i / 5, 36, S("#4A3420", 1.6, 160 * k))
            c.restore()
            CM.ink(f, "neredeyse yok", gx + gw / 2, gy + 82, face="cap_i", size=40, color=TH.fg2, align="c", alpha=cx.amt(a_smell, 0.6, off=0.6), emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c6s5: «Büyükbabası defter tutardı; torunu şiir yazdı.» ═════════════════════════════
@CM.ckind("c6_defter_siir")
def k_defter_siir(cx, a_open=0.0, a_led=None, a_move=None, a_verse=None, a_stamp=None, seed=7, **_):
    """Açık kitap: sol sayfa defter (satır satır sayılar yazılır; Cosimo madalyası), sağ sayfa şiir (kalem sağa geçer, mısralar açılır; Lorenzo madalyası).
    Yazılar okunmaz el yazısıdır (içerik uydurulmaz). a_stamp: «YORUM» damgası (hafif)."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_open, 0.5)
    pw, ph = 640, 790
    lx, rx, py = 690, 1290, 520
    ppL = PP.paper_image(pw, ph, seed, (238, 228, 198), "deckle", (), 44, 1.0)
    ppR = PP.paper_image(pw, ph, seed + 1, (241, 231, 201), "deckle", (), 44, 1.0)
    ppL.draw(f, lx, py, rot=-0.010, alpha=a, shadow=0.55)
    ppR.draw(f, rx, py, rot=0.008, alpha=a, shadow=0.55)
    # sırt gölgesi
    sx = (lx + rx) / 2 + 4
    sh = skia.GradientShader.MakeLinear([(sx - 70, 0), (sx + 70, 0)], [C("#2A1A0C", 0), C("#2A1A0C", int(120 * a)), C("#2A1A0C", 0)], [0, 0.5, 1])
    c.drawRect(skia.Rect.MakeLTRB(sx - 70, py - ph / 2 + 18, sx + 70, py + ph / 2 - 18), skia.Paint(Shader=sh))
    # madalyalar + adlar
    CMD.draw_medal_b(f, "m_cosimo", lx, 285, 150 * (0.9 + 0.1 * ease_out(a)), "bronze", alpha=a, shadow=0.4)
    CMD.draw_medal_b(f, "m_lorenzo", rx, 285, 150 * (0.9 + 0.1 * ease_out(a)), "bronze", alpha=a, shadow=0.4)
    CM.ink(f, "COSİMO", lx, 398, face="title_m", size=30, color=TH.fg2, align="c", track=7, alpha=a, emboss=False)
    CM.ink(f, "LORENZO", rx, 398, face="title_m", size=30, color=TH.fg2, align="c", track=7, alpha=a, emboss=False)
    tip = None
    # sol: defter satırları
    rows = 9
    t_led = cx.at(a_led) if a_led is not None else 1e9
    ys = [462 + 46 * i for i in range(rows)]
    for i, y in enumerate(ys):
        c.drawLine(lx - 270, y + 10, lx + 270, y + 10, S("#5A3E22", 1.3, int(70 * a)))
        k = clamp((cx.t - (t_led + 0.17 * i)) / 0.30)
        if k > 0:
            e = L.scribble(c, lx - 262, lx + 70, y, seed=11 + i, prog=k, a=205)
            if k > 0.55:
                kk = clamp((k - 0.55) / 0.45)
                for j in range(3):
                    xx = lx + 120 + j * 44
                    if kk > j / 3.0:
                        c.drawLine(xx, y - 14, xx + 3, y + 5, S("#3A2616", 2.4, 200))
                        c.drawLine(xx + 12, y - 12, xx + 14, y + 6, S("#3A2616", 2.0, 170))
            if 0 < k < 1:
                tip = (e, y)
    # kalem sağa geçer
    t_mv = cx.at(a_move) if a_move is not None else 1e9
    t_vs = cx.at(a_verse) if a_verse is not None else 1e9
    lens = [250, 300, 220, 280, 190, 300, 240, 170]
    for i, ln in enumerate(lens):
        y = 462 + 52 * i
        k = clamp((cx.t - (t_vs + 0.30 * i)) / 0.46)
        if k > 0:
            x0 = rx - ln / 2
            e = L.scribble(c, x0, x0 + ln, y, seed=70 + i, prog=k, a=205, amp=3.0)
            if 0 < k < 1:
                tip = (e, y)
        if i % 4 == 3 and k > 0:
            pass
    # kalem konumu: yazarken uçta; geçişte sol uçtan sağ ilk satıra süzülür
    qx = qy = None
    if tip is not None:
        qx, qy = tip
    elif cx.t >= t_mv and cx.t < t_vs + 0.2:
        kk = ease_io(clamp((cx.t - t_mv) / max(0.2, t_vs - t_mv + 0.1)))
        qx, qy = lerp(lx + 150, rx - 125, kk), lerp(ys[-1] + 4, 462 - 40, kk) - 60 * math.sin(kk * math.pi)
    if qx is not None:
        K2.draw_quill(f, qx, qy, ang=-38.0, alpha=a)
    if a_stamp is not None:
        L.stamp_at(f, cx, "YORUM", 1520, 800, a_stamp, rot=-0.09, size=40)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c6s6a: Piero öldü — ağırlık Lorenzo'ya geçer ═════════════════════════════
@CM.ckind("c6_aile")
def k_aile(cx, a_open=0.0, a_dead=None, a_date=None, a_thread=None, a_lor=None, a_age=None, seed=9, **_):
    """Cosimo → Piero → Lorenzo hattı: Piero'nun madalyası solar (gri, yas şeridi), tarih levhası, altın bir iplik ağırlığı Lorenzo'ya taşır, Lorenzo parlar."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_open, 0.8)
    px, lx, y = 560, 1360, 500
    ms = 430
    # Cosimo (üstte küçük) ve soy çizgisi
    CMD.draw_medal_b(f, "m_cosimo", 960, 255, 150, "bronze", alpha=0.55 * a, shadow=0.3)
    L.ink_line(c, [(900, 285), (760, 340), (610, 380)], col="#5A3E22", w=2.4, a=190 * a)
    L.ink_line(c, [(1020, 285), (1160, 340), (1310, 380)], col="#5A3E22", w=2.4, a=120 * a)
    dim = ease_io(cx.amt(a_dead, 1.6)) if a_dead is not None else 0.0
    # Piero
    c.save()
    if dim > 0.01:
        c.saveLayer(None, skia.Paint(ColorFilter=L.gray_filter(0.85 * dim)))
    CMD.draw_medal_b(f, "c6_piero", px, y, ms * (0.95 + 0.05 * ease_out(a)), "bronze", alpha=a * (1.0 - 0.18 * dim), tilt=0.12 * math.sin(cx.t * 0.5))
    if dim > 0.01:
        c.restore()
    if dim > 0.01:
        c.drawCircle(px, y, ms * 0.48, P("#1A1008", 120 * dim))
        # yas şeridi: köşeden köşeye siyah kurdele
        c.save()
        c.translate(px, y)
        c.rotate(-32)
        k = clamp(dim * 1.4)
        c.drawRect(skia.Rect.MakeLTRB(-ms * 0.50 * k, -16, ms * 0.50 * k, 16), P("#14100C", 235 * k))
        c.drawRect(skia.Rect.MakeLTRB(-ms * 0.50 * k, -16, ms * 0.50 * k, -12), P("#5A4A30", 200 * k))
        c.restore()
    c.restore()
    CM.ink(f, "PİERO", px, y + ms * 0.62, face="title_m", size=44, color=TH.fg, align="c", track=9, alpha=a * cx.amt(a_open, 0.6, off=0.4), emboss=False)
    # tarih levhası
    L.tag(f, cx, "2 ARALIK 1469", 960, 830, at=a_date if a_date is not None else 1e9, size=44, track=7, dur=0.5) if a_date is not None else None
    # altın iplik (Piero → Lorenzo)
    kt = ease_io(cx.amt(a_thread, 1.5)) if a_thread is not None else 0.0
    if kt > 0.003:
        x0, x1 = px + ms * 0.46, lx - ms * 0.46
        pts = [(x0, y), (lerp(x0, x1, 0.33), y - 70 + 14 * math.sin(cx.t * 1.3)), (lerp(x0, x1, 0.66), y + 60), (x1, y)]
        p = sk.smooth_path(pts, False, 0.5)
        pm = skia.PathMeasure(p, False)
        seg = skia.Path()
        pm.getSegment(0, pm.getLength() * kt, seg, True)
        c.drawPath(seg, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=11, Color=C("#E8C468", 90), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 7)))
        c.drawPath(seg, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.2, Color=C("#C79A3C", 235), StrokeCap=skia.Paint.kRound_Cap))
    # Lorenzo
    kl = ease_out(cx.amt(a_lor, 1.0)) if a_lor is not None else 0.0
    if kl > 0.01:
        L.PN.glow(c, lx, y, ms * 0.80 * (0.8 + 0.2 * kl), "#FFD27A", 0.30 * kl)
    CMD.draw_medal_b(f, "m_lorenzo", lx, y, ms * (0.93 + 0.07 * kl), "bronze", alpha=a * (0.58 + 0.42 * kl), tilt=-0.10 * math.sin(cx.t * 0.6), glint=(clamp((cx.t - cx.at(a_lor)) / 1.4) if a_lor is not None and 0 < (cx.t - cx.at(a_lor)) / 1.4 < 1 else None))
    CM.ink(f, "LORENZO", lx, y + ms * 0.62, face="title_m", size=44, color=TH.fg, align="c", track=9, alpha=a * cx.amt(a_open, 0.6, off=0.5), emboss=False)
    if a_age is not None:
        L.tag(f, cx, "20 YAŞ", lx, 830, at=a_age, size=44, track=8, dur=0.5)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c6s6b: «şehrin ve devletin yükü» — ölçek: madalya → şehir ═════════════════════════════
@CM.ckind("c6_yuk")
def k_yuk(cx, a_move=0.0, a_city=None, a_state=None, a_age=None, seed=3, **_):
    """Floransa silueti (skyline) üzerinde Lorenzo madalyası: önce ortada (yük omzunda), sonra küçülüp köşeye çekilir; ŞEHİR / DEVLET levhaları iğnelenir."""
    import shots as SH
    f = cx.f
    c = f.c
    labels = []
    if a_city is not None:
        labels.append(dict(on="duomo", name="ŞEHİR", at=cx.at(a_city)))
    if a_state is not None:
        labels.append(dict(on="pv", name="DEVLET", at=cx.at(a_state)))
    SH.KINDS["skyline"](cx, seed=seed, tod="day", pan=180.0, labels=labels)
    k = ease_io(cx.amt(a_move, 1.3))
    mx, my, ms = lerp(960, 330, k), lerp(500, 330, k), lerp(430, 230, k)
    L.PN.glow(c, mx, my, ms * 0.8, "#FFD27A", 0.20)
    CMD.draw_medal_b(f, "m_lorenzo", mx, my, ms, "bronze", alpha=1.0, tilt=0.10 * math.sin(cx.t * 0.6))
    if a_age is not None:
        L.tag(f, cx, "20 YAŞ", mx, my + ms * 0.62, at=a_age, size=40, track=8, dur=0.5)


def _row_tag(f, cx, icon, text, x, y, at, size=36, icons_n=1, metal="bronze", w=None, hold=None):
    """Tablet satırı: solda kabartma simge (icons_n adet küçük simge yan yana), sağda Cinzel metin. (x,y) tablet sol-orta."""
    k = cx.amt(at, 0.55)
    if hold is not None:
        k *= 1.0 - cx.amt(hold, 0.4)
    if k <= 0.003:
        return
    iw = 70 if icons_n == 1 else 44 * icons_n + 30
    tw = sk.text_width(text, "cap_b", size) + 56
    wd = w or (iw + tw + 30)
    hh = 86
    CM.tablet(f, x, y - hh / 2 + (1 - k) * 10, wd, hh, alpha=k, corner=8)
    for i in range(icons_n):
        ik = clamp((k - 0.15 * i) / (1 - 0.15 * i)) if icons_n > 1 else k
        icons.draw_icon(f, icon, x + 52 + i * (44 if icons_n > 1 else 0), y + (1 - k) * 10, size=62 if icons_n == 1 else 46, metal=metal, alpha=ik, shadow=False)
    CM.ink(f, text, x + iw + 10 + tw / 2 - 16, y + 13 + (1 - k) * 10, face="cap_b", size=size, color=TH.fg, align="c", alpha=k, emboss=False)


# ═════════════════════════════ c6s9: Lucrezia Tornabuoni, şair ═════════════════════════════
@CM.ckind("c6_lucrezia")
def k_lucrezia(cx, a_open=0.0, a_dua=None, a_bes=None, a_pulci=None, a_morg=None, seed=11, **_):
    """Lucrezia madalyası (sol) + sağda satır satır: DUA ŞARKILARI · BEŞ MANZUM ANLATI · PULCİ'NİN DOSTU · MORGANTE'YE İLHAM. Madalyadan mısra çizgileri yükselir."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_open, 0.8)
    mx, my, ms = 520, 520, 560
    gl = (cx.t * 0.30 + 0.2) % 2.2
    CMD.draw_medal_b(f, "m_lucrezia", mx, my, ms * (0.95 + 0.05 * ease_out(a)), "bronze", alpha=a, tilt=0.14 * math.sin(cx.t * 0.5), glint=gl if gl < 1 else None)
    CM.name_plate(f, "LUCREZİA TORNABUONİ", "şair", None, cx_=mx, y=my + ms * 0.54, t=cx.amt(a_open, 0.7, off=0.3), w=640)
    # mısra çizgileri: madalyadan yukarı süzülen ince dizeler
    for i in range(5):
        ph = (cx.t * 0.18 + i * 0.2) % 1.0
        yy = my - 120 - ph * 260
        xx = mx + 120 + i * 22 + 20 * math.sin(ph * 6 + i)
        al = math.sin(ph * math.pi) * 0.5 * a
        L.scribble(c, xx, xx + 80 + 20 * i, yy, seed=3 + i, a=170 * al, amp=2.2, w=1.8)
    x0 = 1010
    _row_tag(f, cx, "scroll", "DUA ŞARKILARI", x0, 300, a_dua if a_dua is not None else 1e9)
    _row_tag(f, cx, "scroll", "BEŞ MANZUM ANLATI", x0, 430, a_bes if a_bes is not None else 1e9, icons_n=5)
    _row_tag(f, cx, "quill", "PULCİ'NİN DOSTU", x0, 560, a_pulci if a_pulci is not None else 1e9)
    _row_tag(f, cx, "book", "MORGANTE'YE İLHAM", x0, 690, a_morg if a_morg is not None else 1e9)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c6s11: 28 Mart tarihli ilk mektup ═════════════════════════════
@CM.ckind("c6_mektup")
def k_mektup(cx, a_open=0.0, a_unfold=None, a_lines=None, tags=(), date="28 Mart 1467", seed=13, **_):
    """Üç katlı mektup yığını: ilki ortaya gelir, açılır (dikey katlanma), okunmaz satırlar yazılır; kenar notları (tags=[(metin, çapa)]) iğnelenir.
    Metin YAZILMAZ (mektup görülmedi): yalnız tarih + anlatıdaki sözcükler etiket olarak."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_open, 0.6)
    pw, ph = 760, 640
    # arkada iki kapalı mektup (üç mektup)
    for k_, (dx, dy, rt) in enumerate(((-24, -30, -0.07), (-8, 26, 0.045))):
        pp = PP.paper_image(pw - 60, ph - 140, seed + 2 + k_, (232, 220, 188), "deckle", (), 44, 1.0)
        pp.draw(f, 640 + dx, 540 + dy, rot=rt, scale=0.9, alpha=0.9 * a, shadow=0.45)
        CM.wax_seal(f, 640 + dx + 10, 540 + dy + 20, 30, "#A52A1C", alpha=0.8 * a, t=1.0, palle=True)
    # ana mektup: açılma
    ku = ease_io(cx.amt(a_unfold, 0.9)) if a_unfold is not None else 1.0
    pp = PP.paper_image(pw, ph, seed, (240, 230, 200), "deckle", (), 44, 1.0)
    sy = 0.16 + 0.84 * ku
    cxl, cyl = 700, 530
    c.save()
    c.translate(cxl, cyl)
    c.rotate(math.degrees(-0.012))
    c.scale(1.0, sy)
    pp.draw(f, 0, 0, rot=0.0, scale=1.0, alpha=a, shadow=0.55)
    c.restore()
    if ku > 0.35:
        k2 = clamp((ku - 0.35) / 0.65)
        c.save()
        c.translate(cxl, cyl)
        c.rotate(math.degrees(-0.012))
        # tarih (el yazısı) + satırlar
        PP.hand(f, date, -pw / 2 + 80, -ph / 2 + 100, "fell_i", 42, "#4A2E18", a * k2, 1.0, seed=7, align="l")
        t_l = cx.at(a_lines) if a_lines is not None else 1e9
        for i in range(8):
            kk = clamp((cx.t - (t_l + 0.30 * i)) / 0.5)
            if kk > 0:
                ln = 560 - (i % 3) * 60 - (i == 7) * 160
                L.scribble(c, -pw / 2 + 80, -pw / 2 + 80 + ln, -ph / 2 + 190 + 52 * i, seed=100 + i, prog=kk, a=200 * k2)
        c.restore()
    # kenar notları
    for i, (txt, an) in enumerate(tags):
        L.tag(f, cx, txt, 1370, 300 + i * 112, at=an, size=34, track=6, dur=0.5)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c6s7b: «devletsiz zengin yaşamak zordu» — servet kefesi ═════════════════════════════
@CM.ckind("c6_terazi")
def k_terazi(cx, a_open=0.0, a_gold=None, a_state=None, a_shake=None, seed=15, **_):
    """Büyük terazi: sol kefe SERVET (florin yığını büyür, kefe ağırlaşır), sağ kefe DEVLET (boş; kesikli palle izi). Ağırlık eğimi; son cümlede tedirgin sallanma.
    PARA → İKTİDAR halkasının Lorenzo'dan teyidi (anlatıdaki cümle; yeni olgu yok)."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_open, 0.7)
    px, py = 960, 330
    Lb = 380
    kg = ease_io(cx.amt(a_gold, 1.2)) if a_gold is not None else 0.0
    ks = cx.amt(a_state, 0.7) if a_state is not None else 0.0
    ksh = cx.amt(a_shake, 2.0) if a_shake is not None else 0.0
    ang = math.radians(-13.0 * kg + (2.2 * math.sin(cx.t * 5.5) * math.exp(-0.5 * max(0.0, cx.t - cx.at(a_shake))) if a_shake is not None and cx.t > cx.at(a_shake) else 0.0) + 1.0 * math.sin(cx.t * 0.9))
    # direk + ayak
    c.drawRect(skia.Rect.MakeLTRB(px - 9, py, px + 9, 880), P("#7A5A22", 255 * a))
    c.drawRect(skia.Rect.MakeLTRB(px - 9, py, px + 9, 880), S(INK, 1.6, 180 * a))
    c.drawOval(skia.Rect.MakeLTRB(px - 120, 860, px + 120, 905), P("#5A4018", 255 * a))
    c.drawOval(skia.Rect.MakeLTRB(px - 120, 860, px + 120, 905), S(INK, 1.6, 180 * a))
    # kiriş
    ex1, ey1 = px - Lb * math.cos(ang), py - Lb * math.sin(ang)
    ex2, ey2 = px + Lb * math.cos(ang), py + Lb * math.sin(ang)
    c.drawLine(ex1, ey1, ex2, ey2, S("#C4A04A", 12, 255 * a))
    c.drawLine(ex1, ey1, ex2, ey2, S(INK, 2.0, 170 * a))
    c.drawCircle(px, py, 18, P("#E8C25A", 255 * a))
    c.drawCircle(px, py, 18, S(INK, 2.0, 190 * a))
    for side, (ex, ey) in (("l", (ex1, ey1)), ("r", (ex2, ey2))):
        drop = 250
        c.drawLine(ex, ey, ex - 130, ey + drop, S("#8A6A30", 2.4, 230 * a))
        c.drawLine(ex, ey, ex + 130, ey + drop, S("#8A6A30", 2.4, 230 * a))
        p = skia.Path()
        p.moveTo(ex - 150, ey + drop)
        p.quadTo(ex, ey + drop + 70, ex + 150, ey + drop)
        p.close()
        FILLP(c, p, "#C4A04A", 255 * a, 2.0, 200)
        if side == "l" and kg > 0.01:
            n = max(1, int(round(25 * kg)))
            OD_ = L.OD
            OD_.draw_coins(c, ex, ey + drop - 4, n, s=2.0, t=cx.t, seed=3, glint=True)
        if side == "r":
            # DEVLET: kesikli palle izi (boş kefe)
            if ks > 0.01:
                pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.4, Color=C("#7A2018", int(190 * ks)), StrokeCap=skia.Paint.kRound_Cap)
                pr.setPathEffect(skia.DashPathEffect.Make([10, 9], -cx.t * 18))
                for (ox, oy) in ((-34, -42), (0, -42), (34, -42), (-17, -84), (17, -84), (0, -126)):
                    c.drawCircle(ex + ox, ey + drop + oy + 10, 15, pr)
    # etiketler (kefelerin üstünde, kiriş ucuna asılı)
    L.tag(f, cx, "SERVET", ex1, ey1 - 74, at=a_gold if a_gold is not None else 1e9, size=40, track=9, dur=0.5)
    L.tag(f, cx, "DEVLET", ex2, ey2 - 74, at=a_state if a_state is not None else 1e9, size=40, track=9, dur=0.5)
    cam.end(f)
    CM.finish(f, cx, motes_n=20)


# ═════════════════════════════ c6s8: «ama bunu anlatan yine kendisi» — aynadaki imaj ═════════════════════════════
@CM.ckind("c6_ayna")
def k_ayna(cx, a_open=0.0, a_reluct=None, a_age=None, a_danger=None, a_self=None, seed=17, **_):
    """Solda üç gerekçe levhası (İSTEKSİZ · YAŞ · TEHLİKE) sırayla yazılır; sağda bronz el aynası: içinde ters çevrilmiş Lorenzo madalyası (kendi imajı);
    «yine kendisi» anında ayna parlar, KENDİ ANLATIMI levhası + tüy kalem."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_open, 0.7)
    items = [("İSTEKSİZ", a_reluct, "scroll"), ("YAŞ", a_age, "hourglass"), ("TEHLİKE", a_danger, "swords")]
    for i, (txt, an, ic) in enumerate(items):
        if an is None:
            continue
        k = cx.amt(an, 0.5)
        if k <= 0.003:
            continue
        y = 330 + i * 150
        wd = 430
        CM.tablet(f, 250, y - 44 + (1 - k) * 12, wd, 88, alpha=k, corner=8)
        icons.draw_icon(f, ic if ic != "swords" else "sword", 306, y + (1 - k) * 12, size=56, metal="bronze", alpha=k, shadow=False)
        CM.ink(f, txt, 250 + wd / 2 + 26, y + 14 + (1 - k) * 12, face="title_m", size=40, color=TH.fg, align="c", track=7, alpha=k, emboss=False)
    # bronz el aynası
    mx, my = 1330, 480
    rx, ry = 270, 340
    ks = cx.amt(a_self, 0.9) if a_self is not None else 0.0
    sc = 0.95 + 0.05 * ease_out(a)
    c.save()
    c.translate(mx, my)
    c.rotate(math.degrees(0.05 * math.sin(cx.t * 0.7)))
    c.scale(sc, sc)
    # sap
    hp = skia.Path()
    hp.moveTo(-26, ry - 10); hp.lineTo(26, ry - 10); hp.lineTo(18, ry + 210); hp.quadTo(0, ry + 240, -18, ry + 210); hp.close()
    c.drawPath(hp, P("#8A5C30", 255 * a))
    c.drawPath(hp, S(INK, 2.2, 200 * a))
    # çerçeve
    c.drawOval(skia.Rect.MakeLTRB(-rx - 34, -ry - 34, rx + 34, ry + 34), P("#8A5C30", 255 * a))
    c.drawOval(skia.Rect.MakeLTRB(-rx - 34, -ry - 34, rx + 34, ry + 34), S(INK, 2.4, 210 * a))
    c.drawOval(skia.Rect.MakeLTRB(-rx - 22, -ry - 22, rx + 22, ry + 22), S("#E8C468", 4.0, 220 * a))
    for kx in range(24):
        ang = kx / 24 * 6.283
        c.drawCircle((rx + 28) * math.cos(ang), (ry + 28) * math.sin(ang), 5.0, P("#EBC587", 235 * a))
    # cam yüzey
    gl = skia.GradientShader.MakeLinear([(-rx, -ry), (rx, ry)], [C("#EEF2E6", int(235 * a)), C("#C9D6D4", int(235 * a)), C("#E6EBDD", int(235 * a))], [0, 0.55, 1])
    c.save()
    clip = skia.Path()
    clip.addOval(skia.Rect.MakeLTRB(-rx, -ry, rx, ry))
    c.clipPath(clip, skia.ClipOp.kIntersect, True)
    c.drawRect(skia.Rect.MakeLTRB(-rx, -ry, rx, ry), skia.Paint(Shader=gl))
    CMD.draw_medal_b(f, "m_lorenzo", 0, -10, 400, "bronze", flip=True, alpha=0.95 * a, tilt=0.0, shadow=0.0)
    # parıltı: çapraz bant
    gk = (ease_io(ks) * 1.6 - 0.3) if ks > 0 else -1
    if gk > -0.3 and ks < 1.0:
        gx = -rx + (2 * rx) * gk
        sh = skia.GradientShader.MakeLinear([(gx - 90, -ry), (gx + 90, ry)], [C("#FFFFFF", 0), C("#FFFFFF", int(160 * a)), C("#FFFFFF", 0)], [0, 0.5, 1])
        c.drawRect(skia.Rect.MakeLTRB(-rx, -ry, rx, ry), skia.Paint(Shader=sh))
    c.restore()
    c.restore()
    L.tag(f, cx, "KENDİ ANLATIMI", mx, 880, at=a_self if a_self is not None else 1e9, size=40, track=8, dur=0.5)
    cam.end(f)
    CM.finish(f, cx, motes_n=20)


# ═════════════════════════════ c6s12: defter kaydı (mizah: evlilik pazarı) ═════════════════════════════
@CM.ckind("c6_ledger")
def k_c6_ledger(cx, stampt=None, **kw):
    """Standart `ledger` + kaynak damgası (○ TEK KAYNAK). Defter satırı: «Clarice'yi aldım» silinir → «ya da bana verildi»."""
    import shots as SH
    SH.KINDS["ledger"](cx, **kw)
    if stampt:
        L.stamp_at(cx.f, cx, stampt[0], stampt[1], stampt[2], stampt[3], rot=-0.09, size=stampt[4] if len(stampt) > 4 else 40)


# ═════════════════════════════ c6s15: atölye (oda dünyasına eklenen yeni oda: "c6_atolye") ═════════════════════════════
import cilt_oda as OD  # noqa: E402
import cilt_pano as PN  # noqa: E402
from cilt_oda import OV, Y_FL, LH, F_WALL, F_FG, PT, STK, SOFT, FILLP, BOX, WOOD  # noqa: E402


class Atolye(OD.Room):
    """Bir Rönesans atölyesi (bottega): ham sıva duvar, sokağa açılan geniş kemer, tezgâh + aletler, heykeltıraş kaidesi (kil büst: yüzsüz), şövale (boş panel), taş blok, duvarda asılı çizim kâğıtları.
    Yüz/kişi ayrıntısı yok; figürler `actors` ile (siluet). Kaynaksız ayrıntı yok: yalnız genel atölye düzeni."""
    name = "c6_atolye"
    PW = 3000

    def build(self):
        self.layer("wall", F_WALL, self.Lw(F_WALL), self._draw_wall, wear=3)
        self.layer("main", 1.0, self.PW, self._draw_main, scale=1.2)
        self.layer("fg", F_FG, self.Lw(F_FG), self._draw_fg)

    def paths(self):
        return {"default": [(0.0, (1100, 0, 1.0)), (1.0, (1900, 0, 1.05))],
                "sweep_r": [(0.0, (1000, 0, 1.0)), (1.0, (2000, 0, 1.0))],
                "wide": [(0.0, (1500, 20, 0.9)), (1.0, (1500, 0, 1.05))]}

    def default_actors(self, ctx=None):
        return [dict(kind="halk", x=1950, y=806, h=268, action="work", mode="strike", prop="hammer", sil="#120A06", seed=5, dir=-1, rim_dir=1),
                dict(kind="cocuk", x=2400, y=806, h=232, action="work", mode="lay", prop="trowel", sil="#120A06", seed=8, dir=-1)]

    # ── statik ───────────────────────────────────────────────────────────
    def _draw_wall(self, fr, xa, xb):
        c, T = fr.c, self.T
        wx = self.wx
        OD.plaster(c, xa, xb, OV - 40, Y_FL + 30, T, "#DCCBA2", "#C8B58A", amp=0.06)
        OD.cornice(c, xa, xb, 72, T, col="#7A5A3A", plaster="#CDB98F", gold=False)
        OD.wainscot(c, xa, xb, Y_FL - 108, Y_FL + 18, T, "#8A5A38", seed=7)
        # sokağa açılan geniş kemer (parlak): taş çerçeve + içeride açık gök ve uzak evler
        ax = wx(1500)
        if xa - 500 < ax < xb + 500:
            w_, h_ = 420, 500
            path = OD.doorway_stone(c, T, ax, Y_FL + 10, w_, h_, "#B4AE9A")
            c.save()
            c.clipPath(path, skia.ClipOp.kIntersect, True)
            GRAD_V(c, ax - w_, Y_FL - h_, ax + w_, Y_FL + 12, [("#BFD8E4", 0.0), ("#EAE2C8", 0.75), ("#CDBE98", 1.0)])
            rs = _RSX(4)
            xx = ax - w_ / 2
            while xx < ax + w_ / 2:
                bw, bh = rs.uniform(46, 90), rs.uniform(70, 150)
                R_(c, xx, Y_FL - 20 - bh, xx + bw, Y_FL - 20, "#C9B58C", 230)
                R_(c, xx, Y_FL - 20 - bh, xx + bw, Y_FL - 20 - bh + 10, "#B5513A", 230)
                for k in range(2):
                    R_(c, xx + 10 + k * 24, Y_FL - 20 - bh + 34, xx + 20 + k * 24, Y_FL - 20 - bh + 54, "#5A4A34", 200)
                xx += bw + rs.uniform(2, 10)
            c.restore()
        # yan pencere
        for x in (620, 2380):
            if xa - 300 < wx(x) < xb + 300:
                OD.draw_window(c, T, wx(x), 226, 150, 300, night=False, shutters=True)
        # duvarda asılı çizim kâğıtları (okunmaz karalama; kaynaksız içerik yok)
        rs = _RSX(9)
        for x, y, w_, h_, rt in ((900, 250, 120, 160, -0.05), (1080, 300, 100, 130, 0.04), (1860, 260, 140, 170, 0.03), (2060, 240, 100, 150, -0.04), (2620, 300, 120, 150, 0.05)):
            X = wx(x)
            if xa - 200 < X < xb + 200:
                c.save()
                c.translate(X, y)
                c.rotate(math.degrees(rt))
                SOFT(c, 4, 8, w_ * 0.55, h_ * 0.52, "#000000", 55)
                R_(c, -w_ / 2, -h_ / 2, w_ / 2, h_ / 2, "#EFE5C8")
                INKR(c, -w_ / 2, -h_ / 2, w_ / 2, h_ / 2, 1.0, 150)
                for j in range(5):
                    yy = -h_ / 2 + 22 + j * (h_ - 36) / 5
                    c.drawLine(-w_ / 2 + 12, yy, -w_ / 2 + 12 + w_ * rs.uniform(0.4, 0.74), yy + rs.uniform(-3, 3), STK("#3A2616", 1.4, 150))
                c.restore()
        sh = OD.LGP((0, Y_FL - 30), (0, Y_FL + 30), [("#1A0F06", 0.0, 0), ("#1A0F06", 1.0, 80)])
        c.drawRect(skia.Rect.MakeLTRB(xa, Y_FL - 30, xb, Y_FL + 30), sh)

    def _draw_main(self, fr, xa, xb):
        c, T = fr.c, self.T
        OD.floor_planks(c, xa, xb, Y_FL, LH, T, "#9A7248", seed=3, w0=230.0, rowh=14.0, grow=1.16)
        # tezgâh (x≈900–1280): ahşap tabla + bacaklar + aletler (keski, çekiç, kâğıt)
        if xa - 400 < 1100 < xb + 400:
            WOOD(c, 900, 690, 1300, 718, T, "#7A4E2A", seed=2)
            for lx in (930, 1270):
                WOOD(c, lx - 14, 718, lx + 14, 818, T, "#6A4220", seed=lx, vertical=True)
            SOFT(c, 1100, 822, 230, 12, "#000000", 85)
            for i, (tx, tl) in enumerate(((960, 46), (1010, 40), (1060, 52))):
                c.drawLine(tx, 688, tx + tl, 680, STK("#3A3A3A", 4.2, 240))
                c.drawLine(tx, 688, tx - 12, 690, STK("#6A4220", 7.5, 255))
            R_(c, 1130, 674, 1270, 690, "#EFE5C8")
            INKR(c, 1130, 674, 1270, 690, 1.0, 150)
        # taş blok (kemer önü)
        if xa - 300 < 1560 < xb + 300:
            BOX(c, 1470, 722, 1660, 822, "#C9C1AE", T, hl=0.20, sh=0.24, ink=1.6)
            for k in range(6):
                c.drawLine(1480 + k * 28, 730 + (k % 2) * 6, 1496 + k * 28, 752 + (k % 3) * 8, STK("#7A7466", 1.3, 160))
            SOFT(c, 1565, 826, 120, 10, "#000000", 90)
        # kaide + kil büst (yüzsüz, iri hatlı)
        if xa - 300 < 1950 < xb + 300:
            BOX(c, 1900, 640, 2000, 822, "#B4AE9A", T, hl=0.18, sh=0.22, ink=1.6)
            BOX(c, 1886, 622, 2014, 646, "#C9C1AE", T, hl=0.18, sh=0.20, ink=1.5)
            bp = skia.Path()
            bp.moveTo(1915, 622)
            bp.quadTo(1900, 560, 1932, 520)
            bp.quadTo(1950, 486, 1976, 520)
            bp.quadTo(2008, 560, 1988, 622)
            bp.close()
            FILLP(c, bp, "#B58A6A", 255, 1.6, 200, shader=skia.GradientShader.MakeLinear([(1900, 520), (2000, 620)], [C("#D8B08A"), C("#A07A58"), C("#7E5A40")], [0, 0.55, 1]))
            SOFT(c, 1955, 826, 120, 10, "#000000", 90)
        # şövale + boş panel
        if xa - 300 < 2400 < xb + 300:
            for lx, rt in ((2330, 6), (2470, -6)):
                c.drawLine(lx, 560, lx + rt * 8, 822, STK("#6A4220", 9, 255))
            c.drawLine(2400, 560, 2400, 822, STK("#6A4220", 9, 255))
            BOX(c, 2310, 430, 2490, 640, "#E4D8B8", T, hl=0.10, sh=0.14, ink=2.0)
            BOX(c, 2300, 420, 2500, 436, "#7A4E2A", T, hl=0.10, sh=0.2, ink=1.3)
            c.drawLine(2330, 520, 2470, 520, STK("#4A3420", 1.2, 90))
            SOFT(c, 2400, 826, 130, 10, "#000000", 80)
        # küçük fıçı/vazo (süs)
        for x in (700, 2750):
            if xa - 200 < x < xb + 200:
                BOX(c, x - 34, 746, x + 34, 822, "#7A5230", T, hl=0.16, sh=0.26, ink=1.4)
                for yy in (762, 800):
                    c.drawLine(x - 34, yy, x + 34, yy, STK("#2A1A0C", 2.0, 200))

    def _draw_fg(self, fr, xa, xb):
        c, T = fr.c, self.T
        fx = lambda x: W / 2 + (x - W / 2) * F_FG
        for x in (260, 2780):
            if xa - 120 < fx(x) < xb + 120:
                xx = fx(x)
                R_(c, xx - 30, OV - 40, xx + 30, 900, "#3A342A", 255)
                OD.HGRAD(c, xx - 30, OV - 40, xx + 30, 900, [("#FFFFFF", 0.0, 34), ("#000000", 0.45, 0), ("#000000", 1.0, 100)])
                INKR_(c, xx - 30, OV - 40, xx + 30, 900, 1.5, 200)

    def dyn_main(self, ctx):
        c, t = ctx.c, ctx.t
        # keski tozu: kaidenin çevresinde süzülen taneler
        rs = _RSX(21)
        for k in range(14):
            ph = (t * 0.35 + rs.rand()) % 1.0
            x = 1955 + (rs.rand() - 0.5) * 140 + ph * 40
            y = 600 - ph * 120 + rs.rand() * 30
            c.drawCircle(x, y, 1.6 + 2.2 * rs.rand(), skia.Paint(AntiAlias=True, Color=C("#EFE5C8", int(150 * (1 - ph)))))
        OD.draw_extra(ctx, "back")

    def dyn_front(self, ctx):
        OD.draw_extra(ctx, "front")


def R_(c, x0, y0, x1, y1, col, a=255):
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.Paint(Color=C(col, int(a))))


def INKR_(c, x0, y0, x1, y1, w=1.2, a=170):
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C("#2A1A0C", int(a))))


def _RSX(n):
    return np.random.RandomState(int(n))


OD.ROOMS["c6_atolye"] = Atolye


@CM.ckind("c6_atolye")
def k_c6_atolye(cx, figs=(), names=True, cams=None, labels=(), **kw):
    """Atölye (oda dünyası): siluet figürler atölyeden geçer; her figürün üstünde adı (script sözcüğü) levha olarak onu izler.
    figs=[dict(name, at, x0, x1, speed, y, h, kind, seed)] ; at = yürüyüş başlangıç çapası."""
    import shots as SH
    actors = [dict(kind="halk", x=1950, y=806, h=268, action="work", mode="strike", prop="hammer", sil="#120A06", seed=5, dir=-1, rim_dir=1),
              dict(kind="cocuk", x=2400, y=806, h=232, action="work", mode="lay", prop="trowel", sil="#120A06", seed=8, dir=-1)]
    for i, d in enumerate(figs):
        actors.append(dict(kind=d.get("kind", "soylu"), x=d["x0"], y=d.get("y", 808), h=d.get("h", 262), action="idle", sil="#120A06", walk=(d["x1"], d.get("speed", 150.0)), walk_at=d["at"],
                           fade_x=d.get("fade_x"), seed=d.get("seed", 3 + i), dir=1, layer="front", prop=d.get("prop")))
        if d.get("fade_x") is None:
            actors[-1].pop("fade_x")
    SH.KINDS["oda"](cx, room="c6_atolye", actors=actors, cams=cams, tod="day", frame=True, **kw)
    # sabit levhalar: (metin, giriş çapası, çıkış çapası|None, üstü çizilme çapası|None, x, y)
    for (txt, a_in, a_out, a_strike, lx, ly) in labels:
        k = cx.amt(a_in, 0.5)
        if a_out is not None:
            k *= 1.0 - cx.amt(a_out, 0.5)
        if k <= 0.01:
            continue
        wd = sk.text_width(txt, "title_m", 44, 8) + 76
        CM.tablet(cx.f, lx - wd / 2, ly - 44 + (1 - k) * 10, wd, 88, alpha=k, corner=8)
        CM.ink(cx.f, txt, lx, ly + 14 + (1 - k) * 10, face="title_m", size=44, color=TH.fg, align="c", track=8, alpha=k, emboss=False)
        if a_strike is not None:
            ks = ease_io(cx.amt(a_strike, 0.4))
            if ks > 0.01:
                pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5.0, Color=C("#8E2A1A", int(235 * k)), StrokeCap=skia.Paint.kRound_Cap)
                pr.setPathEffect(skia.DiscretePathEffect.Make(12.0, 1.3, 2))
                cx.f.c.drawLine(lx - wd / 2 + 18, ly - 2, lx - wd / 2 + 18 + (wd - 36) * ks, ly - 6, pr)
    if names and cams:
        camx, camy, z = L.cam_probe(cx, cams, None)
        for i_, d in enumerate(figs):
            t0 = cx.at(d["at"])
            sp = d.get("speed", 150.0)
            dist = d["x1"] - d["x0"]
            u = clamp((cx.t - t0) * sp / max(1.0, abs(dist)))
            x = d["x0"] + dist * u
            sx, sy = L.world_to_screen(camx, camy, z, x, d.get("y", 808) - d.get("h", 262) - 30)
            sy -= 60 * i_
            al = clamp((cx.t - (cx.at(d.get("name_at", d["at"])) - 0.2)) / 0.4) * (1.0 if u < 0.97 else clamp((1.0 - u) / 0.03))
            if al > 0.01 and 120 < sx < W - 120:
                wd = sk.text_width(d["name"], "title_m", 34, 6) + 52
                CM.tablet(cx.f, sx - wd / 2, sy - 34, wd, 64, alpha=al, corner=8)
                CM.ink(cx.f, d["name"], sx, sy + 12, face="title_m", size=34, color=TH.fg, align="c", track=6, alpha=al, emboss=False)


# ═════════════════════════════ c6s16a: Lorenzo ve Poliziano — derleme (yazma yığını) ═════════════════════════════
@CM.ckind("c6_derleme")
def k_derleme(cx, a_open=0.0, a_y1=None, a_y2=None, a_lor=None, a_pol=None, a_stack=None, seed=19, **_):
    """İki madalya (Lorenzo · Poliziano) arasında yazma yaprakları teker teker gelip yığılır (derleme); üstte 1476 — 1477 şeridi. Metin yazılmaz (okunmaz satırlar)."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_open, 0.7)
    # yıllar şeridi
    k1 = cx.amt(a_y1, 0.6) if a_y1 is not None else 0.0
    k2 = cx.amt(a_y2, 0.6) if a_y2 is not None else 0.0
    if k1 > 0.01 or k2 > 0.01:
        c.drawLine(560, 262, 560 + 800 * ease_io(k2), 262, S("#5A3E22", 3.0, 210))
        L.tag(f, cx, "1476", 560, 262, at=a_y1, size=40, track=8, dur=0.5) if a_y1 is not None else None
        L.tag(f, cx, "1477", 1360, 262, at=a_y2, size=40, track=8, dur=0.5) if a_y2 is not None else None
    # madalyalar
    for key, x, an, nm in (("m_lorenzo", 430, a_lor, "LORENZO"), ("c6_poliziano", 1490, a_pol, "POLİZİANO")):
        k = ease_out(cx.amt(an, 0.8)) if an is not None else 0.0
        if k > 0.01:
            CMD.draw_medal_b(f, key, x, 540, 330 * (0.92 + 0.08 * k), "bronze", alpha=k, tilt=0.12 * math.sin(cx.t * 0.6 + x))
            CM.ink(f, nm, x, 540 + 205, face="title_m", size=38, color=TH.fg, align="c", track=8, alpha=k, emboss=False)
    # yığılan yaprak sayfaları (soldan ve sağdan sırayla)
    t0 = cx.at(a_stack) if a_stack is not None else 1e9
    pp = PP.paper_image(380, 520, seed, (240, 230, 200), "deckle", (), 44, 1.0)
    for i in range(7):
        ti = t0 + 0.55 * i
        k = ease_out(clamp((cx.t - ti) / 0.7))
        if k <= 0:
            continue
        side = -1 if i % 2 == 0 else 1
        sx = 960 + side * (760 - 760 * k)
        sy = 560 - i * 6 + 40 * (1 - k)
        rt = (0.06 * ((i * 37) % 7 - 3) / 3.0) + side * 0.5 * (1 - k)
        pp.draw(f, sx, sy, rot=rt, scale=0.78, alpha=min(1.0, k * 1.5), shadow=0.45)
        if k > 0.95:
            for j in range(5):
                L.scribble(c, sx - 110, sx + 110 - (j % 3) * 30, sy - 140 + j * 52, seed=300 + i * 7 + j, a=130, amp=2.6, w=1.7)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c6s17b: Prens'in ithafı — «Muhteşem» damgaları (unvan enflasyonu) ═════════════════════════════
@CM.ckind("c6_magnifico")
def k_magnifico(cx, a_open=0.0, a_mach=None, a_son=None, a_grand=None, a_ithaf=None, a_st1=None, a_st2=None, seed=23, **_):
    """Deri ciltli PRENS kitabı; Machiavelli adı iğnelenir; ithaf çizgisi iki levhaya akar (OĞLU · TORUNU); «Muhteşem» damgası art arda iki kez VURUR (kuru mizah: unvan enflasyonu)."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_open, 0.6)
    bx, by, bw, bh = 520, 520, 360, 500
    sc = 0.94 + 0.06 * ease_out(a)
    c.save()
    c.translate(bx, by)
    c.rotate(math.degrees(-0.035))
    c.scale(sc, sc)
    SOFT(c, 12, bh / 2 + 16, bw * 0.62, 18, "#000000", 90 * a)
    # sayfa bloğu (yan)
    c.drawRect(skia.Rect.MakeLTRB(-bw / 2 + 14, -bh / 2 + 10, bw / 2 + 12, bh / 2 + 8), P("#EFE4C6", 255 * a))
    for i in range(10):
        c.drawLine(bw / 2 + 4, -bh / 2 + 20 + i * 48, bw / 2 + 12, -bh / 2 + 24 + i * 48, S("#9A8A66", 1.2, 160 * a))
    # kapak
    cover = skia.Path()
    cover.addRoundRect(skia.Rect.MakeLTRB(-bw / 2, -bh / 2, bw / 2, bh / 2), 10, 10)
    c.drawPath(cover, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-bw / 2, -bh / 2), (bw / 2, bh / 2)], [C("#8A3A2C", int(255 * a)), C("#6A2A20", int(255 * a)), C("#4A1C14", int(255 * a))], [0, 0.5, 1])))
    c.drawPath(cover, S(INK, 3.0, 220 * a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-bw / 2 + 24, -bh / 2 + 24, bw / 2 - 24, bh / 2 - 24), 6, 6, S("#E8C468", 3.0, 235 * a))
    c.drawRoundRect(skia.Rect.MakeLTRB(-bw / 2 + 36, -bh / 2 + 36, bw / 2 - 36, bh / 2 - 36), 4, 4, S("#E8C468", 1.4, 170 * a))
    sp = CM.gilt("PRENS", "title", 70, 10.0)
    CM.draw_spr(f, sp, 0, -20, "c", alpha=a, glow=0.1)
    for dx in (-100, 100):
        c.drawCircle(dx, 90, 7, P("#E8C468", 230 * a))
    c.drawLine(-110, 50, 110, 50, S("#E8C468", 2.0, 220 * a))
    c.restore()
    L.tag(f, cx, "MACHİAVELLİ", bx, 840, at=a_mach if a_mach is not None else 1e9, size=40, track=8, dur=0.5)
    # ithaf çizgileri → iki levha
    plates = [("LORENZO'NUN OĞLU", a_son, 1130, 400, a_st1), ("LORENZO'NUN TORUNU", a_grand, 1130, 640, a_st2)]
    ki = cx.amt(a_ithaf, 1.0) if a_ithaf is not None else 0.0
    for i, (txt, an, px, py, ast) in enumerate(plates):
        k = cx.amt(an, 0.55) if an is not None else 0.0
        if k <= 0.003:
            continue
        wd = 600
        CM.tablet(f, px - wd / 2, py - 56 + (1 - k) * 12, wd, 112, alpha=k, corner=10)
        CM.ink(f, txt, px, py + 12 + (1 - k) * 12, face="title_m", size=34, color=TH.fg, align="c", track=5, alpha=k, emboss=False)
        # ithaf çizgisi (kitaptan levhaya mürekkep ip)
        kk = ease_io(clamp((ki - 0.45 * i) / 0.55))
        if kk > 0.003:
            pts = [(bx + bw * 0.5 + 20, by - 40 + i * 90), (760, py - 60 + 90 * i), (px - wd / 2 - 20, py)]
            p = sk.smooth_path(pts, False, 0.5)
            pm = skia.PathMeasure(p, False)
            seg = skia.Path()
            pm.getSegment(0, pm.getLength() * kk, seg, True)
            pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.2, Color=C("#4A3420", 215), StrokeCap=skia.Paint.kRound_Cap)
            pr.setPathEffect(skia.DashPathEffect.Make([16, 10], -cx.t * 30))
            c.drawPath(seg, pr)
        # damga
        if ast is not None:
            ks = cx.amt(ast, 0.3)
            if ks > 0.003:
                CM.stamp(f, "MUHTEŞEM", px + 450, py + 6, rot=-0.10 + 0.04 * i, size=50, alpha=1.0, t=ks)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c6s18–19: Faun anekdotu (gravür) ═════════════════════════════
def _draw_faun(c, x, y, s=1.0, tooth_out=0.0, gum_cut=0.0, laugh=0.0, a=255):
    """Yaşlı faun başı (taş; yandan değil önden; gravür çizgili). (x,y) = baş merkezi; s ölçek. tooth_out: sol-üst dişin düştüğü (0..1) ; gum_cut: diş eti oyulma çizgisi (0..1)."""
    ink = "#2A1A0C"
    st = "#BDB4A0"
    st2 = "#8E8672"
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    # kaide
    c.drawRect(skia.Rect.MakeLTRB(-150, 205, 150, 330), P("#A8A08C", a))
    c.drawRect(skia.Rect.MakeLTRB(-150, 205, 150, 330), S(ink, 3.0, 210))
    c.drawRect(skia.Rect.MakeLTRB(-170, 192, 170, 214), P("#C5BDA9", a))
    c.drawRect(skia.Rect.MakeLTRB(-170, 192, 170, 214), S(ink, 2.6, 210))
    for k in range(5):
        c.drawLine(-140 + k * 70, 220 + (k % 2) * 14, -120 + k * 70, 290 + (k % 3) * 12, S("#6E6652", 1.4, 110))
    # boyun
    c.drawRect(skia.Rect.MakeLTRB(-60, 150, 60, 200), P(st2, a))
    # boynuzlar
    for sx in (-1, 1):
        hp = skia.Path()
        hp.moveTo(sx * 70, -150)
        hp.quadTo(sx * 118, -230, sx * 92, -272)
        hp.quadTo(sx * 128, -226, sx * 120, -150)
        hp.close()
        c.drawPath(hp, P("#A89F8A", a))
        c.drawPath(hp, S(ink, 2.6, 215))
    # kulaklar (sivri)
    for sx in (-1, 1):
        ep = skia.Path()
        ep.moveTo(sx * 138, -30)
        ep.lineTo(sx * 214, -92)
        ep.lineTo(sx * 160, 28)
        ep.close()
        c.drawPath(ep, P(st2, a))
        c.drawPath(ep, S(ink, 2.6, 215))
    # kafa
    hd = skia.Path()
    hd.moveTo(-132, -90)
    hd.quadTo(-146, -190, 0, -196)
    hd.quadTo(146, -190, 132, -90)
    hd.quadTo(150, 40, 100, 120)
    hd.quadTo(60, 190, 0, 196)
    hd.quadTo(-60, 190, -100, 120)
    hd.quadTo(-150, 40, -132, -90)
    hd.close()
    c.drawPath(hd, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-140, -190), (140, 190)], [C("#D2C9B2", a), C(st, a), C("#8A826E", a)], [0, 0.5, 1])))
    c.drawPath(hd, S(ink, 3.2, 225))
    # saç bukleleri (üstte)
    for i in range(7):
        cx_ = -108 + i * 36
        c.drawCircle(cx_, -176 + 8 * math.sin(i * 1.7), 22, P("#B2A994", a))
        c.drawCircle(cx_, -176 + 8 * math.sin(i * 1.7), 22, S(ink, 2.0, 200))
    # alın kırışıkları
    for k, (yy, w_) in enumerate(((-120, 80), (-100, 96), (-80, 70))):
        c.drawPath(sk.smooth_path([(-w_, yy + 6), (0, yy - 8), (w_, yy + 6)], False, 0.5), S(ink, 2.0, 170))
    # kaşlar + gözler (taş: oyuk göz)
    for sx in (-1, 1):
        c.drawPath(sk.smooth_path([(sx * 30, -64), (sx * 64, -80), (sx * 100, -58)], False, 0.5), S(ink, 5.0, 225))
        c.drawOval(skia.Rect.MakeLTRB(sx * 62 - 22, -54, sx * 62 + 22, -34), P("#5A5242", a))
        c.drawOval(skia.Rect.MakeLTRB(sx * 62 - 22, -54, sx * 62 + 22, -34), S(ink, 2.4, 220))
        c.drawCircle(sx * 62, -44, 6, P("#1A1208", a))
    # burun (geniş)
    np_ = skia.Path()
    np_.moveTo(-10, -40); np_.quadTo(-24, 20, -42, 36); np_.quadTo(0, 56, 42, 36); np_.quadTo(24, 20, 10, -40)
    c.drawPath(np_, P("#A89F8A", a * 0.8))
    c.drawPath(np_, S(ink, 2.4, 200))
    for sx in (-1, 1):
        c.drawOval(skia.Rect.MakeLTRB(sx * 20 - 9, 34, sx * 20 + 9, 46), P("#3A3224", a))
    # yanak çizgileri
    for sx in (-1, 1):
        c.drawPath(sk.smooth_path([(sx * 58, 18), (sx * 86, 54), (sx * 78, 96)], False, 0.5), S(ink, 2.0, 170))
    # sakal + ağız (gülen, dişli)
    mo = skia.Path()
    mo.moveTo(-76, 74)
    mo.quadTo(0, 112 + 14 * laugh, 76, 74)
    mo.quadTo(0, 96 + 16 * laugh, -76, 74)
    mo.close()
    c.drawPath(mo, P("#2A1A12", a))
    c.drawPath(mo, S(ink, 2.6, 225))
    # üst dişler
    n = 6
    for i in range(n):
        tx = -58 + i * 23
        tp = skia.Rect.MakeLTRB(tx, 78 + 3 * abs(i - 2.5), tx + 19, 98 + 3 * abs(i - 2.5))
        if i == 1 and tooth_out > 0.01:
            continue
        c.drawRoundRect(tp, 3, 3, P("#EFE8D4", a))
        c.drawRoundRect(tp, 3, 3, S(ink, 1.5, 200))
    if tooth_out > 0.01:
        # diş boşluğu + oyulmuş diş eti
        c.drawRoundRect(skia.Rect.MakeLTRB(-35, 78 + 3 * 1.5, -16, 98 + 3 * 1.5), 3, 3, P("#4A2A20", a))
        if gum_cut > 0.01:
            pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.4, Color=C("#7A1E18", int(220 * gum_cut)), StrokeCap=skia.Paint.kRound_Cap)
            c.drawPath(sk.smooth_path([(-40, 82), (-32, 70 - 4 * gum_cut), (-14, 80)], False, 0.5), pr)
    # sakal buklesi
    for i in range(9):
        bx_ = -66 + i * 16.5
        c.drawPath(sk.smooth_path([(bx_, 108), (bx_ + 4, 134 + 10 * math.sin(i * 1.3)), (bx_ - 2, 168)], False, 0.5), S(ink, 2.4, 190))
    c.restore()


@CM.ckind("c6_faun")
def k_faun(cx, phase=1, a_open=0.0, a_cond=None, a_faun=None, a_lor=None, a_joke=None, a_stamp=None, a_hit=None, a_gum=None, a_house=None, a_room=None, a_table=None, a_duk=None, seed=29, **_):
    """GRAVÜR dilinde (rivayet): taş faun başı, genç heykeltıraş (siluet, çekiç), Lorenzo (siluet).
    phase=1 (c6s18): şaka — «yaşlıların dişleri tam olmaz». phase=2 (c6s19): diş kırılır, diş eti oyulur; Lorenzo onu eve alır: ODA · SOFRA · AYDA 5 DUKAT."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    L.mono_begin(f, 1.0)
    cam.begin(f)
    a = cx.amt(a_open, 0.6)
    fx, fy, fs = 760, 450, 1.25 if phase == 1 else 1.4
    t_hit = cx.at(a_hit) if a_hit is not None else 1e9
    tooth_out = clamp((cx.t - t_hit - 0.25) / 0.2) if a_hit is not None else 0.0
    gum = ease_io(cx.amt(a_gum, 1.4)) if a_gum is not None else 0.0
    _draw_faun(c, fx, fy, fs, tooth_out=tooth_out, gum_cut=gum, laugh=0.4 + 0.3 * math.sin(cx.t * 2.0), a=255 * a)
    # düşen diş
    if a_hit is not None and cx.t > t_hit + 0.2:
        u = cx.t - (t_hit + 0.2)
        tx = fx - 26 * fs + 90 * u
        ty = fy + 84 * fs - 220 * u + 560 * u * u
        if ty < fy + 330 * fs:
            c.save()
            c.translate(tx, ty)
            c.rotate(300 * u)
            c.drawRoundRect(skia.Rect.MakeLTRB(-11, -15, 11, 15), 3, 3, P("#EFE8D4", 255))
            c.drawRoundRect(skia.Rect.MakeLTRB(-11, -15, 11, 15), 3, 3, S(INK, 2.0, 220))
            c.restore()
    # heykeltıraş (siluet, çekiç vurur)
    sx_ = 1190 if phase == 1 else 1150
    swing = a_hit if phase == 2 else None
    OD.sil_actor(f, "halk", sx_, 810, 300, cx.t, action="work", dir=-1, seed=5, color="#120A06", rim="#B8A888", rim_dir=1, mode="strike", prop="hammer", period=1.5)
    # Lorenzo (siluet)
    lx_ = 1560
    kl = cx.amt(a_lor, 0.7) if a_lor is not None else 1.0
    if phase == 1:
        OD.sil_actor(f, "soylu", lx_, 812, 330, cx.t, action="point", dir=-1, seed=9, color="#120A06", rim="#B8A888", rim_dir=1, alpha=kl, t0=cx.at(a_joke) - 0.6 if a_joke is not None else 0.5, target=(-1.0, 0.0))
    else:
        # c6s19: eve alma — Lorenzo ev kapısına doğru işaret eder
        OD.sil_actor(f, "soylu", lx_, 812, 330, cx.t, action="point", dir=1, seed=9, color="#120A06", rim="#B8A888", rim_dir=1, alpha=kl, t0=cx.at(a_house) - 0.4 if a_house is not None else 0.5, target=(1.0, -0.1))
    cam.end(f)
    L.mono_end(f)
    # yazılar (renkli kalır: belge/etiket; gravür yalnız resim)
    if phase == 1:
        L.tag(f, cx, "CONDİVİ", 300, 250, at=a_cond if a_cond is not None else 1e9, size=40, track=8, dur=0.5)
        L.tag(f, cx, "LORENZO", lx_, 440, at=a_lor if a_lor is not None else 1e9, size=40, track=8, dur=0.5)
        if a_joke is not None:
            k = cx.amt(a_joke, 0.6)
            if k > 0.01:
                wd = 640
                CM.tablet(f, 980 - wd / 2 + 150, 150 + (1 - k) * 8, wd, 96, alpha=k, corner=12)
                CM.ink(f, "yaşlıların dişleri tam olmaz", 980 + 150, 150 + 62 + (1 - k) * 8, face="cap_i", size=48, color=TH.fg, align="c", alpha=k, emboss=False)
        L.stamp_at(f, cx, "ANEKDOT", 1560, 270, a_stamp if a_stamp is not None else 1e9, rot=-0.08, size=44)
    else:
        if a_gum is not None:
            pass
        L.stamp_at(f, cx, "ANEKDOT", 250, 190, a_stamp if a_stamp is not None else 1e9, rot=-0.08, size=40)
        # oda · sofra · ayda beş dukat
        rows = [("ODA", a_room, "bed"), ("SOFRA", a_table, "chest"), ("AYDA 5 DUKAT", a_duk, "coins")]
        for i, (txt, an, ic) in enumerate(rows):
            k = cx.amt(an, 0.5) if an is not None else 0.0
            if k <= 0.003:
                continue
            x0, y = 1330, 330 + i * 140
            wd = sk.text_width(txt, "title_m", 42, 7) + 150
            CM.tablet(f, x0, y - 48 + (1 - k) * 12, wd, 96, alpha=k, corner=8)
            icons.draw_icon(f, ic, x0 + 60, y + (1 - k) * 12, size=64, metal="bronze", alpha=k, shadow=False)
            CM.ink(f, txt, x0 + 100 + (wd - 100) / 2, y + 14 + (1 - k) * 12, face="title_m", size=42, color=TH.fg, align="c", track=7, alpha=k, emboss=False)
    CM.finish(f, cx, motes_n=18)


# ═════════════════════════════ GIOSTRA DÜNYASI (pano dünyası "c6_giostra") ═════════════════════════════
import cilt_city as CT  # noqa: E402
import cilt_scene as SC  # noqa: E402

YG_G = 846                       # ana düzlem ayak hizası
FENCE_Y = 826                    # çit tabanı
PEN = [("#B33620", "#F4E8C8"), ("#233C8C", "#E0B84E"), ("#2F7A5A", "#F4E8C8"), ("#E0B84E", "#B33620"), ("#F4E8C8", "#233C8C")]


def pennant(c, x, y, Lg, hh, t, ph, c1, c2):
    """Direğin ucundan sağa akan kırlangıç kuyruklu flama (dalgalı); iki renkli (kısmen)."""
    n = 12
    top, bot = [], []
    for i in range(n + 1):
        u = i / n
        amp = hh * 0.40 * u
        yy = y + math.sin(t * 5.2 - u * 5.8 + ph) * amp
        w_ = hh * (1.0 - 0.55 * u)
        top.append((x + u * Lg, yy - w_ / 2))
        bot.append((x + u * Lg, yy + w_ / 2))
    for (a, b, col) in ((0, 7, c1), (7, 12, c2)):
        poly = top[a:b + 1] + bot[a:b + 1][::-1]
        pa = sk.poly_path(poly)
        c.drawPath(pa, skia.Paint(AntiAlias=True, Color=C(col)))
        c.drawPath(pa, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#2A1A0C", 170)))
    # kuyruk çatalı
    ex, ey = top[-1][0], (top[-1][1] + bot[-1][1]) / 2
    c.drawPath(sk.poly_path([top[-1], (ex - hh * 0.30, ey), bot[-1]]), skia.Paint(AntiAlias=True, Color=C("#EFE5C8", 120)))


def _palazzo(c, x, yb, w, h, rs, T):
    wall = T(["#E4D5AE", "#D9C79A", "#EBDFC0", "#CDBB8E"][rs.randint(4)], 0.2)
    c.drawRect(skia.Rect.MakeLTRB(x, yb - h, x + w, yb), P(wall))
    c.drawRect(skia.Rect.MakeLTRB(x + w * 0.74, yb - h, x + w, yb), P("#2A1A0C", 34))
    L.INKR(c, x, yb - h, x + w, yb, 1.4, 160)
    # saçak + çatı
    c.drawRect(skia.Rect.MakeLTRB(x - 8, yb - h - 12, x + w + 8, yb - h), P(T("#9A5A34", 0.2)))
    c.drawPath(sk.poly_path([(x - 8, yb - h - 12), (x + 22, yb - h - 56), (x + w - 22, yb - h - 56), (x + w + 8, yb - h - 12)]), P(T("#B5552E", 0.2)))
    nx = max(2, int(w / 74))
    rows = max(2, int((h - 40) / 90))
    for iy in range(rows):
        for ix in range(nx):
            wx_ = x + (ix + 0.5) * w / nx
            wy_ = yb - h + 26 + iy * ((h - 60) / rows)
            ww_, wh_ = 30, 52
            p = skia.Path()
            p.moveTo(wx_ - ww_ / 2, wy_ + wh_)
            p.lineTo(wx_ - ww_ / 2, wy_ + ww_ / 2)
            p.arcTo(skia.Rect.MakeLTRB(wx_ - ww_ / 2, wy_, wx_ + ww_ / 2, wy_ + ww_), 180, 180, False)
            p.lineTo(wx_ + ww_ / 2, wy_ + wh_)
            p.close()
            c.drawPath(p, P("#3A2A1C", 215))
            c.drawPath(p, S("#2A1A0C", 1.2, 180))
            # sarkık kumaş (festival): bazı pencerelerin altında
            if (ix + iy + int(x)) % 3 == 0:
                col = (("#B33620", "#F4E8C8"), ("#233C8C", "#E0B84E"), ("#F4E8C8", "#B33620"))[(ix + iy * 2 + int(x // 100)) % 3]
                c.drawRect(skia.Rect.MakeLTRB(wx_ - 24, wy_ + wh_ - 6, wx_ + 24, wy_ + wh_ + 54), P(col[0]))
                c.drawRect(skia.Rect.MakeLTRB(wx_ - 24, wy_ + wh_ - 6, wx_ + 24, wy_ + wh_ + 2), P(col[1]))
                for k in range(3):
                    c.drawLine(wx_ - 16 + k * 16, wy_ + wh_ + 2, wx_ - 16 + k * 16, wy_ + wh_ + 54, S("#000000", 1.2, 50))
                L.INKR(c, wx_ - 24, wy_ + wh_ - 6, wx_ + 24, wy_ + wh_ + 54, 1.0, 150)


def _church(c, x, yb, w, h, T):
    """Genel bir Toskana kilisesi cephesi (düz, bantlı taş; gabled; gül pencere; üç portal). Santa Croce için stilize temsil: ayrıntı iddiası yok."""
    stone = T("#E2D5B4", 0.15)
    band = T("#CBBD96", 0.15)
    x0, x1 = x - w / 2, x + w / 2
    c.drawRect(skia.Rect.MakeLTRB(x0, yb - h * 0.66, x1, yb), P(stone))
    for k in range(7):
        yy = yb - h * 0.66 + k * (h * 0.66 / 7)
        c.drawRect(skia.Rect.MakeLTRB(x0, yy, x1, yy + h * 0.66 / 14), P(band, 150))
    # yan nef çatıları + ortada yüksek gable
    gb = sk.poly_path([(x - w * 0.34, yb - h * 0.66), (x, yb - h), (x + w * 0.34, yb - h * 0.66)])
    c.drawPath(gb, P(stone))
    c.drawPath(gb, S("#2A1A0C", 1.8, 190))
    for sx in (-1, 1):
        sp = sk.poly_path([(x + sx * w * 0.34, yb - h * 0.66), (x + sx * w * 0.5, yb - h * 0.52), (x + sx * w * 0.5, yb - h * 0.66)])
        c.drawPath(sp, P(stone))
        c.drawPath(sp, S("#2A1A0C", 1.4, 170))
    L.INKR(c, x0, yb - h * 0.66, x1, yb, 1.8, 190)
    # gül pencere
    rx, ry = x, yb - h * 0.80
    c.drawCircle(rx, ry, h * 0.10, P("#7A8A9A", 235))
    c.drawCircle(rx, ry, h * 0.10, S("#2A1A0C", 2.2, 210))
    for k in range(8):
        a = k * math.pi / 4
        c.drawLine(rx, ry, rx + math.cos(a) * h * 0.10, ry + math.sin(a) * h * 0.10, S("#2A1A0C", 1.6, 200))
    c.drawCircle(rx, ry, h * 0.035, P("#E8C468", 230))
    # portaller
    for dx, pw_, ph_ in ((-w * 0.30, w * 0.13, h * 0.30), (0, w * 0.17, h * 0.38), (w * 0.30, w * 0.13, h * 0.30)):
        PN.draw_arch_opening(c, x + dx, yb, pw_, ph_, T, inner="#3A2A1C")
    # çan kulesi (yan)
    CT.draw_campanile(c, x1 + w * 0.10, yb, w * 0.10, h * 1.15, T, 0.15)


class Giostra(PN.World):
    """Santa Croce Meydanı'nı TEMSİL eden stilize piyasa: uzak tepeler/şehir, çevre palazzolar + kilise cephesi (genel), ahşap çit, sahanlıklı seyirci sıraları, flamalı direkler, kum zemin.
    Kaynaksız ayrıntı (jüri, ödül, hava, atların sayısı) YOK; at/atlı/kalabalık `FA` kitinden; atlılar `stations` ile gelir."""
    name = "c6_giostra"
    PW = 7600
    interior = False

    def build(self):
        PW = self.PW
        span = PW - W

        def Lw(f):
            return int(W + span * f + 500)
        self.layer("sky", 0.05, Lw(0.05), self._draw_sky, opaque=True, scale=0.5, wear=3, loss=0.5, yr=(0, 700))
        self.layer("hills", 0.14, Lw(0.14), self._draw_hills, scale=0.5, wear=2, yr=(330, 800))
        self.city_houses = []
        x = -40
        rr = PN._RS(5)
        while x < Lw(0.30) + 60:
            bw, bh = rr.uniform(34, 74), rr.uniform(30, 70)
            self.city_houses.append((x, bw, bh, int(rr.randint(1, 10 ** 6)), 0.46, 0))
            x += bw + rr.uniform(-4, 8)
        x = 20
        while x < Lw(0.30) + 60:
            bw, bh = rr.uniform(40, 80), rr.uniform(34, 76)
            self.city_houses.append((x, bw, bh, int(rr.randint(1, 10 ** 6)), 0.26, 20))
            x += bw + rr.uniform(-6, 6)
        self.XD = 2700
        self.layer("city", 0.30, Lw(0.30), self._draw_city, wear=2, yr=(60, 620))
        self.XC = int(960 + (3400 - 960) * 0.62)             # kilise x'i (arka katmanda; kamera x≈3400'de ortada)
        self.layer("back", 0.62, Lw(0.62), self._draw_back, wear=3, yr=(180, 812))
        self.layer("main", 1.0, PW, self._draw_main, wear=4)
        self.cheer = 0.55

    def default_cams(self):
        return [(0.0, (1300, 0, 1.0)), (1.0, (2500, 0, 1.08))]

    def default_stations(self):
        return []

    def stack(self, ctx):
        return [("L", "sky"), ("L", "hills"), ("L", "city"), ("D", "dyn_city", 0.30), ("L", "back"), ("D", "dyn_back", 0.62), ("L", "main"), ("D", "dyn_main", 1.0)]

    # ── statik katmanlar ────────────────────────────────────────────────────
    def _draw_sky(self, fr, xa, xb):
        c = fr.c
        GRAD_V(c, xa, 0, xb, 760, [("#6F9ED6", 0.0), ("#BDD0DC", 0.55), ("#F4E8C8", 1.0)])
        L.R(c, xa, 759, xb, 960, "#F4E8C8")
        rs = PN._RS(int(xa) // 7 + 3)
        for i in range(int((xb - xa) / 380) + 1):
            x = xa + rs.uniform(0, 380) + i * 380
            y = rs.uniform(OV + 40, 420)
            for k in range(3):
                c.drawOval(skia.Rect.MakeLTRB(x + k * 70, y - 8, x + k * 70 + 210, y + 12), skia.Paint(AntiAlias=True, Color=C("#FFFFFF", 42), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8)))

    def _draw_hills(self, fr, xa, xb):
        c = fr.c
        T = self.T
        for (col, amp, sc, base, ph) in (("#A9BDB6", 40, 600, 392, 0.0), ("#93AFA5", 46, 420, 440, 2.1), ("#7F9E92", 52, 300, 486, 4.3)):
            cc = T(col, 0.2)
            pts = []
            x = xa - 8
            while x <= xb + 8:
                pts.append((x, PN.ridge_y(x, base, amp, sc, ph)))
                x += 8
            poly = pts + [(pts[-1][0], 960), (pts[0][0], 960)]
            c.drawPath(sk.poly_path(poly), skia.Paint(AntiAlias=True, Color=C(cc)))
            c.drawPath(sk.poly_path(pts, False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, Color=C(mix(cc, "#1A2A22", 0.5), 150)))
            gx0 = int(xa // 150) - 1
            for gi in range(gx0, int(xb // 150) + 2):
                r_ = PN._RS(gi * 7 + int(ph * 10))
                if r_.rand() < 0.55:
                    x = gi * 150 + r_.uniform(0, 150)
                    y = PN.ridge_y(x, base, amp, sc, ph)
                    SC.cypress(c, x, y + 3, r_.uniform(28, 52), T("#2E4A33", 0.3), T("#4F6E4A", 0.3))

    def _draw_city(self, fr, xa, xb):
        c = fr.c
        T = self.T
        wins = []
        base = 548
        for (x, bw, bh, sd, dep, dy) in self.city_houses:
            if x + bw < xa - 60 or x > xb + 60:
                continue
            rs = PN._RS(sd)
            CT.draw_house(c, x, base + dy + (rs.rand() * 8 - 4), bw, bh, rs, T, dep, wins)
        XD = self.XD
        if xb > XD - 900 and xa < XD + 900:
            c.save()
            c.translate(XD, base)
            c.scale(1.25, 1.25)
            c.translate(-XD, -base)
            CT.draw_nave(c, XD + 70, XD + 640, base + 4, 124, T, 0.16)
            CT.draw_dome(c, XD, base - 108, 214, 132, 48, 74, T, 0.12)
            CT.draw_campanile(c, XD + 205, base + 4, 54, 262, T, 0.12)
            c.restore()
            CT.draw_tower(c, XD - 700, base, 32, 190, T, 0.30, spire=False)

    def _draw_back(self, fr, xa, xb):
        c = fr.c
        T = self.T
        yb = 790
        # zemin şeridi (arka düzlem kum/taş)
        GRAD_V(c, xa, yb - 6, xb, 830, [(T("#C9B88E", 0.3), 0.0), (T("#B8A67A", 0.2), 1.0)])
        rs = PN._RS(3)
        x = -400
        while x < xb + 400:
            w_ = rs.uniform(170, 300)
            h_ = rs.uniform(220, 330)
            if abs((x + w_ / 2) - self.XC) < 760:
                x += w_ + 6
                continue
            if x + w_ > xa - 200 and x < xb + 200:
                _palazzo(c, x, yb, w_, h_, PN._RS(int(x) % 9973 + 7), T)
            x += w_ + rs.uniform(2, 10)
        if xb > self.XC - 900 and xa < self.XC + 900:
            _church(c, self.XC, yb, 1040, 560, T)

    def _draw_main(self, fr, xa, xb):
        c = fr.c
        T = self.T
        PW = self.PW
        # kum zemin
        GRAD_V(c, xa, 800, xb, 940, [("#D8C28E", 0.0), ("#CDB482", 0.4), ("#BFA470", 1.0)])
        rs = PN._RS(int(xa) // 11 + 5)
        for i in range(int((xb - xa) / 14)):
            xx = rs.uniform(xa, xb)
            yy = rs.uniform(806, 930)
            c.drawCircle(xx, yy, rs.uniform(0.8, 2.2), skia.Paint(Color=C("#8A6E40", 70)))
        for k in range(3):
            yy = 852 + k * 26
            c.drawLine(xa, yy, xb, yy + 2, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#8A6E40", 60)))
        # seyirci sahanlıkları: ahşap platform + önü örtü (festoon)
        x0 = int(xa // 120) * 120 - 120
        # arka sahanlık (üst sıra)
        L.R(c, xa, 696, xb, 708, "#7A5030")
        L.INKR(c, xa, 696, xb, 708, 1.2, 170)
        for xx in range(x0, int(xb) + 120, 120):
            L.R(c, xx - 5, 708, xx + 5, 770, "#6A4220")
        # ön sahanlık
        L.R(c, xa, 770, xb, 790, "#8A5A34")
        L.INKR(c, xa, 770, xb, 790, 1.4, 190)
        L.R(c, xa, 790, xb, 826, "#6A4220")
        for xx in range(x0, int(xb) + 120, 60):
            c.drawLine(xx, 790, xx, 826, S("#2A1A0C", 1.2, 130))
        # festoon örtüler (çit önünde asılı kumaş)
        for i, xx in enumerate(range(x0, int(xb) + 240, 240)):
            col = PEN[i % len(PEN)]
            p = skia.Path()
            p.moveTo(xx, 792)
            p.quadTo(xx + 120, 850, xx + 240, 792)
            p.lineTo(xx + 240, 800)
            p.quadTo(xx + 120, 860, xx, 800)
            p.close()
            c.drawPath(p, P(col[0]))
            c.drawPath(p, S("#2A1A0C", 1.2, 170))
        # çit (iki ray + direkler)
        for xx in range(x0, int(xb) + 120, 110):
            L.R(c, xx - 4, FENCE_Y - 66, xx + 4, FENCE_Y + 6, "#8A5A34")
            L.INKR(c, xx - 4, FENCE_Y - 66, xx + 4, FENCE_Y + 6, 1.0, 150)
        for yy in (FENCE_Y - 50, FENCE_Y - 24):
            L.R(c, xa, yy - 5, xb, yy + 5, "#A0683A")
            c.drawLine(xa, yy - 5, xb, yy - 5, S("#2A1A0C", 1.0, 150))
            c.drawLine(xa, yy + 5, xb, yy + 5, S("#2A1A0C", 1.0, 150))
        # bayrak direkleri (dinamik flamalar için)
        for xx in range(560, PW, 640):
            if xa - 60 < xx < xb + 60:
                PN.draw_pole(c, xx, FENCE_Y - 66, 396, w=10, col="#6A4A2C")
                c.drawCircle(xx, 392, 7, P("#E0B84E"))

    # ── canlı katmanlar ─────────────────────────────────────────────────────
    def dyn_city(self, ctx):
        FA.atmo_birds(ctx.c, ctx.t, 6, 1.0, ctx.xa, ctx.xb, 120, 340, speed=22.0, night=False, seed=3, size=0.8)

    def dyn_back(self, ctx):
        pass

    def dyn_main(self, ctx):
        f, c, t = ctx.f, ctx.c, ctx.t
        xa, xb = ctx.xa, ctx.xb
        cheer = ctx.cx.__dict__.get("g_cheer", self.cheer)
        for (y0, y1, hh, n, sd) in ((706, 770, (150, 176), 34, 31), (770, 800, (160, 190), 26, 32)):
            if cheer < 0:
                break
            n_ = max(8, int(n * (self.PW) / 7600))
            FA.crowd(f, t, (160, y0, self.PW - 160, y1), n_ * 6, seed=sd, wave=0.6, mode="cheer" if cheer > 0.5 else "stand", h=hh, view=(xa, xb), cull=160, wave_speed=0.8)
        # flamalar
        for i, xx in enumerate(range(560, self.PW, 640)):
            if xa - 360 < xx < xb + 60:
                c1, c2 = PEN[i % len(PEN)]
                pennant(c, xx + 2, 408, 150, 54, t, i * 1.3, c1, c2)
        # istasyonlar (atlılar)
        for st in ctx.stations:
            fn = st.get("fn")
            if fn is None:
                continue
            ctx.st = st
            fn(ctx, st)


PN.WORLDS["c6_giostra"] = Giostra


def _lance(T, u_scale=1.0, tilt=-6.0):
    def prop(c, hk):
        u = hk.u
        hand = (0.31 * u, -0.27 * u)
        c.save()
        c.translate(hand[0], hand[1])
        c.rotate(tilt)
        Lg = u * 3.6
        c.drawLine(-u * 0.9, 0, Lg, 0, S("#5A3C20", 7.0, 255))
        c.drawLine(-u * 0.9, 0, Lg, 0, S("#C79A3C", 1.8, 230))
        c.drawPath(sk.poly_path([(Lg, -7), (Lg + 34, 0), (Lg, 7)]), P("#8A8A90"))
        # flama (şerit)
        for k in range(3):
            c.drawLine(Lg - 70, -4 + 0, Lg - 160 - 14 * math.sin(T * 9 + k), 12 + 8 * k + 5 * math.sin(T * 8 + k * 1.7), S("#B33620" if k % 2 == 0 else "#F4E8C8", 6.0, 235))
        c.restore()
    return prop


def st_rider(ctx, st):
    """Atlı istasyonu: st = dict(x0, v, y, h, gait, seed, lance=True, dirn=1, hide_before=True). `_at` anından itibaren v px/sn ile sağa (dirn=1) dörtnala gider."""
    t = ctx.t - st["_at"]
    v = st.get("v", 760.0)
    dirn = st.get("dirn", 1)
    if t < 0 and st.get("hide_before", True):
        return
    u = max(0.0, t)
    x = st["x0"] + dirn * v * u
    vv = v if t >= 0 else float(st.get("v0", 0.0))
    prop = _lance(ctx.t, tilt=-5.0) if st.get("lance", True) else None
    FA.rider(ctx.f, x, st.get("y", 866), st.get("h", 290), ctx.t, speed=vv, gait=st.get("gait", "gallop") if t >= 0 else st.get("gait0", "walk"), dir=dirn, seed=st.get("seed", 3), prop=prop)
    if t >= 0 and vv > 300:
        # toz: arka toynak hizasında süzülen tozlar
        for k in range(8):
            age = (k * 0.09 + (ctx.t * 3.0) % 0.72)
            px = x - dirn * (90 + 55 * age * 4.0)
            py = st.get("y", 866) - 6 - 40 * age
            FA._puff(ctx.c, px, py, 26 + 46 * age, 0.30 * (1 - age / 0.8) if age < 0.8 else 0.0)


def st_walkers(ctx, st):
    """Arka planda yavaş yürüyen sancaklı atlılar (alay). st = dict(x0, n, gap, dirn, seed, speed)."""
    f = ctx.f
    t = ctx.t
    for i in range(st.get("n", 2)):
        x = st["x0"] + st.get("dirn", 1) * st.get("speed", 70.0) * t + i * st.get("gap", 320)
        FA.rider(f, x, st.get("y", 872), st.get("h", 272), t, speed=st.get("speed", 70.0), gait="walk", dir=st.get("dirn", 1), seed=st.get("seed", 5) + i, prop=_lance(t, tilt=-80.0))


@CM.ckind("c6_giostra")
def k_giostra(cx, title=None, ally=None, date=None, cool_at=None, shadow_at=None, cheer=0.6, **kw):
    """Santa Croce Meydanı (temsil): `pano` dünyası c6_giostra + üst katman: VENEDİK ◦ MİLANO ittifak levhaları, tarih levhası, ışık soğuması (cool_at) ve uzun gölge (shadow_at).
    kw → pano (cams, stations, kick, caption, tod…)."""
    import shots as SH
    cx.g_cheer = cheer
    SH.KINDS["pano"](cx, pano="c6_giostra", **kw)
    f = cx.f
    c = f.c
    if ally is not None:
        a_v, a_m, a_r = ally
        k1 = cx.amt(a_v, 0.55)
        k2 = cx.amt(a_m, 0.55)
        kr = cx.amt(a_r, 0.6)
        for txt, k, x in (("VENEDİK", k1, 640), ("MİLANO", k2, 1280)):
            if k > 0.01:
                wd = 520
                CM.tablet(f, x - wd / 2, 226 - 44 + (1 - k) * 12, wd, 88, alpha=k, corner=8)
                CM.ink(f, txt, x, 226 + 14 + (1 - k) * 12, face="title_m", size=46, color=TH.fg, align="c", track=9, alpha=k, emboss=False)
        if kr > 0.01:
            icons.draw_icon(f, "ring", 960, 226, size=96, metal="gold", alpha=kr, shadow=True, glow=0.2)
            c.drawLine(900, 226, 760, 226, S("#C79A3C", 3.0, 220 * kr))
            c.drawLine(1020, 226, 1160, 226, S("#C79A3C", 3.0, 220 * kr))
    if title is not None:
        kt = cx.amt(title[1], 0.9)
        if kt > 0.003:
            sp = CM.gilt(title[0], "title", 150, 20.0)
            CM.draw_spr(f, sp, W / 2, 330, "c", alpha=min(1.0, kt * 1.6), reveal=clamp(kt * 1.2), glow=0.25 * kt, shadow=0.8)
    if date is not None:
        L.date_plate(f, cx, date[0], date[1], x=96, y=330, size=48)
    if cool_at is not None:
        k = ease_io(cx.amt(cool_at, 2.4))
        if k > 0.003:
            sh = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [C("#22305E", int(150 * k)), C("#1B2750", int(120 * k)), C("#101A3C", int(170 * k))], [0, 0.55, 1])
            c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), skia.Paint(Shader=sh))
    if shadow_at is not None:
        k = ease_out(cx.amt(shadow_at, 2.2))
        if k > 0.003:
            # uzun gölge (yüzsüz siluet gölgesi): sağdan sola doğru zemine uzanır
            x0, y0 = 1560, 880
            Ls = 1100 * k
            pts = [(0, 0), (-18, -0.1), (-30, -0.34), (-22, -0.55), (-14, -0.74), (0, -0.92), (14, -0.74), (22, -0.55), (30, -0.34), (18, -0.1), (0, 0)]
            q = [(x0 - Ls * (-py) * 1.0 + px * (1 + 1.6 * (-py)), y0 + 70 * (-py) * k - 6 * px * 0.05) for px, py in pts]
            p = sk.smooth_path(q, True, 0.4)
            c.drawPath(p, skia.Paint(AntiAlias=True, Color=C("#0A0A18", int(150 * k)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6)))


# ═════════════════════════════ c6s21: kazanan Giuliano; seçtiği kadın Simonetta ═════════════════════════════
@CM.ckind("c6_madalyalar")
def k_madalyalar(cx, a_open=0.0, a_lor=None, a_not=None, a_giu=None, a_chose=None, a_sim=None, a_husb=None, seed=31, **_):
    """Üç madalya soldan sağa: Lorenzo (silikleşir, «KAZANAN DEĞİL») → Giuliano («KAZANAN») → ince mürekkep ipi «SEÇTİĞİ KADIN» → Simonetta («Marco Vespucci'nin eşi»)."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    ms = 380
    xs = (400, 960, 1520)
    y = 500
    kl = ease_out(cx.amt(a_lor, 0.8)) if a_lor is not None else 0.0
    kn = ease_io(cx.amt(a_not, 0.9)) if a_not is not None else 0.0
    kg = ease_out(cx.amt(a_giu, 0.8)) if a_giu is not None else 0.0
    ks = ease_out(cx.amt(a_sim, 0.8)) if a_sim is not None else 0.0
    if kl > 0.01:
        c.save()
        if kn > 0.01:
            c.saveLayer(None, skia.Paint(ColorFilter=L.gray_filter(0.8 * kn)))
        CMD.draw_medal_b(f, "m_lorenzo", xs[0], y, ms * (0.93 + 0.07 * kl), "bronze", alpha=kl * (1 - 0.35 * kn), tilt=0.1 * math.sin(cx.t * 0.6))
        if kn > 0.01:
            c.restore()
        c.restore()
        CM.ink(f, "LORENZO", xs[0], y + ms * 0.62, face="title_m", size=40, color=TH.fg, align="c", track=8, alpha=kl * (1 - 0.4 * kn), emboss=False)
        if kn > 0.01:
            # kesikli halka: «değil»
            pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.0, Color=C("#8E2A1A", int(220 * kn)), StrokeCap=skia.Paint.kRound_Cap)
            pr.setPathEffect(skia.DashPathEffect.Make([16, 14], -cx.t * 18))
            c.drawCircle(xs[0], y, ms * 0.52, pr)
            L.tag(f, cx, "DEĞİL", xs[0], y + ms * 0.62 + 84, at=a_not, size=36, track=9, dur=0.4)
    if kg > 0.01:
        L.PN.glow(c, xs[1], y, ms * 0.85 * (0.8 + 0.2 * kg), "#FFD27A", 0.28 * kg)
        gl = (cx.t - cx.at(a_giu)) / 1.4
        CMD.draw_medal_b(f, "c6_giuliano", xs[1], y, ms * (0.93 + 0.07 * kg), "bronze", alpha=kg, tilt=-0.1 * math.sin(cx.t * 0.7), glint=gl if 0 < gl < 1 else None)
        CM.ink(f, "GİULİANO", xs[1], y + ms * 0.62, face="title_m", size=44, color=TH.fg, align="c", track=9, alpha=kg, emboss=False)
        L.tag(f, cx, "KAZANAN", xs[1], y + ms * 0.62 + 84, at=a_giu, size=36, track=9, dur=0.4)
    # seçtiği kadın: ip
    kc = ease_io(cx.amt(a_chose, 1.1)) if a_chose is not None else 0.0
    if kc > 0.01:
        x0, x1 = xs[1] + ms * 0.52, xs[2] - ms * 0.52
        pts = [(x0, y - 20), (lerp(x0, x1, 0.5), y - 130), (x1, y - 20)]
        p = sk.smooth_path(pts, False, 0.5)
        pm = skia.PathMeasure(p, False)
        seg = skia.Path()
        pm.getSegment(0, pm.getLength() * kc, seg, True)
        pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.6, Color=C("#5A3E22", 225), StrokeCap=skia.Paint.kRound_Cap)
        pr.setPathEffect(skia.DashPathEffect.Make([14, 9], -cx.t * 26))
        c.drawPath(seg, pr)
        L.tag(f, cx, "SEÇTİĞİ KADIN", lerp(x0, x1, 0.5), y - 176, at=a_chose, size=34, track=7, dur=0.5)
    if ks > 0.01:
        CMD.draw_medal_b(f, "c6_simonetta", xs[2], y, ms * (0.93 + 0.07 * ks), "bronze", alpha=ks, tilt=0.1 * math.sin(cx.t * 0.55 + 1.0))
        CM.ink(f, "SİMONETTA", xs[2], y + ms * 0.62, face="title_m", size=44, color=TH.fg, align="c", track=9, alpha=ks, emboss=False)
        L.tag(f, cx, "Marco Vespucci'nin eşi", xs[2], y + ms * 0.62 + 84, at=a_husb if a_husb is not None else a_sim, size=30, face="cap_i", track=2, dur=0.5)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c6s22: Botticelli'nin sancağı — temsil; asıl sancak kayıp ═════════════════════════════
def _pallas_art(c, w=400, h=620, prog=1.0):
    """Miğferli Pallas (yüzsüz, profil siluet çizgisi + düz boya yıkama): kodla yeniden çizilmiş TEMSİL. prog: yukarıdan aşağı açılma (0..1)."""
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(-20, -20, w + 20, h * clamp(prog) + 4))
    ink = "#2A1A0C"
    # peplos (uzun giysi): omuzdan yere dökülen
    robe = skia.Path()
    robe.moveTo(150, 190)
    robe.quadTo(120, 330, 96, 600)
    robe.lineTo(310, 600)
    robe.quadTo(290, 340, 254, 190)
    robe.close()
    c.drawPath(robe, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(100, 190), (300, 600)], [C("#E8DCC0"), C("#C9B88E"), C("#A8946A")], [0, 0.5, 1])))
    c.drawPath(robe, S(ink, 3.0, 230))
    for k in range(7):
        x = 126 + k * 26
        c.drawPath(sk.smooth_path([(x, 250), (x - 6 + k * 3, 420), (x - 16 + k * 5, 598)], False, 0.5), S(ink, 1.6, 150))
    # boyun + göğüs
    c.drawPath(sk.poly_path([(176, 150), (214, 150), (230, 200), (160, 200)]), P("#D9B48A"))
    c.drawPath(sk.poly_path([(176, 150), (214, 150), (230, 200), (160, 200)]), S(ink, 2.4, 220))
    # miğfer (kubbe + yanak siperi + sorguç); yüz ayrıntısı YOK (siper kapalı)
    hp = skia.Path()
    hp.moveTo(140, 150)
    hp.quadTo(130, 40, 200, 34)
    hp.quadTo(272, 40, 262, 150)
    hp.quadTo(246, 168, 200, 168)
    hp.quadTo(160, 168, 140, 150)
    hp.close()
    c.drawPath(hp, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(140, 30), (262, 170)], [C("#E8D08A"), C("#B8923C"), C("#7A5A1C")], [0, 0.5, 1])))
    c.drawPath(hp, S(ink, 3.2, 235))
    c.drawPath(sk.smooth_path([(176, 90), (200, 110), (244, 100)], False, 0.5), S(ink, 2.2, 200))
    # sorguç (at kılı) geriye akar
    c.drawPath(sk.smooth_path([(196, 36), (160, -6), (96, -2), (60, 40), (66, 96)], False, 0.5), S("#8E2A1A", 14.0, 235))
    c.drawPath(sk.smooth_path([(196, 36), (160, -6), (96, -2), (60, 40), (66, 96)], False, 0.5), S(ink, 2.0, 200))
    # mızrak (sağ elde) ve kalkan (sol)
    c.drawLine(300, 80, 300, 604, S("#6A4A2C", 8.0, 255))
    c.drawPath(sk.poly_path([(300, 40), (314, 90), (286, 90)]), P("#8A8A90"))
    c.drawPath(sk.poly_path([(300, 40), (314, 90), (286, 90)]), S(ink, 2.0, 220))
    c.drawCircle(130, 360, 84, P("#B8923C"))
    c.drawCircle(130, 360, 84, S(ink, 3.0, 230))
    c.drawCircle(130, 360, 58, S("#E8D08A", 3.0, 220))
    c.drawCircle(130, 360, 18, P("#7A5A1C"))
    c.restore()


_BAN = {}


def _banner_imgs(w=520, h=700):
    key = (w, h)
    if key in _BAN:
        return _BAN[key]
    Q = 2.0
    fr = sk.Frame(int(w * Q), int(h * Q))
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    c.scale(Q, Q)
    # bez + çerçeve kenarı
    cloth = skia.Path()
    cloth.addRect(skia.Rect.MakeLTRB(6, 6, w - 6, h - 6))
    c.drawPath(cloth, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 0), (w, h)], [C("#F1E6C8"), C("#E4D3A8"), C("#D6C292")], [0, 0.5, 1])))
    c.drawPath(cloth, S("#2A1A0C", 3.0, 235))
    c.drawRect(skia.Rect.MakeLTRB(20, 20, w - 20, h - 20), S("#B33620", 6.0, 230))
    c.drawRect(skia.Rect.MakeLTRB(32, 32, w - 32, h - 32), S("#C79A3C", 2.0, 220))
    base = fr.surf.makeImageSnapshot()
    fr2 = sk.Frame(int(w * Q), int(h * Q))
    fr2.clear(skia.ColorTRANSPARENT)
    fr2.c.scale(Q, Q)
    fr2.c.save()
    fr2.c.translate(60, 40)
    _pallas_art(fr2.c, 400, 620, 1.0)
    fr2.c.restore()
    art = fr2.surf.makeImageSnapshot()
    _BAN[key] = (base, art)
    return _BAN[key]


@CM.ckind("c6_sancak")
def k_sancak(cx, a_open=0.0, a_bot=None, a_sim=None, a_paint=None, a_paint_dur=1.8, a_stamp=None, a_lost=None, seed=37, **_):
    """Direğe asılı sancak: dalgalanan bez (dikey dilimler). «miğferli Pallas» yukarıdan aşağı çizilir (kodla yeniden çizilmiş temsil, yüzsüz);
    «asıl sancak kayıp»ta boya silinir, bez çözülür, yalnız kesikli çerçeve + boş direk + levha kalır."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_open, 0.7)
    base, art = _banner_imgs()
    bw, bh = 520, 700
    px = 560                                           # direk x
    top = 150
    # direk + enine çubuk
    c.drawRect(skia.Rect.MakeLTRB(px - 9, top - 60, px + 9, 900), P("#6A4A2C", 255 * a))
    c.drawRect(skia.Rect.MakeLTRB(px - 9, top - 60, px + 9, 900), S(INK, 1.8, 190 * a))
    c.drawCircle(px, top - 64, 14, P("#E0B84E", 255 * a))
    c.drawRect(skia.Rect.MakeLTRB(px - 8, top - 8, px + bw + 40, top + 12), P("#6A4A2C", 255 * a))
    c.drawRect(skia.Rect.MakeLTRB(px - 8, top - 8, px + bw + 40, top + 12), S(INK, 1.6, 190 * a))
    lost = ease_io(cx.amt(a_lost, 1.6)) if a_lost is not None else 0.0
    kp = clamp((cx.t - cx.at(a_paint)) / a_paint_dur) if a_paint is not None else 0.0
    art_alpha = (1.0 - lost) if kp > 0 else 0.0
    cl_alpha = a * (1.0 - 0.92 * lost)
    # dalgalanan bez
    n = 22
    wv = lambda i: (math.sin(cx.t * 2.4 - i * 0.42) * 22 + math.sin(cx.t * 4.1 - i * 0.8) * 7) * (i / n) ** 1.1
    x0 = px + 12
    sw = bw / n
    pb = skia.Paint(AntiAlias=True)
    pb.setAlphaf(clamp(cl_alpha))
    pa = skia.Paint(AntiAlias=True)
    pa.setAlphaf(clamp(a * art_alpha))
    # sürüklenen kenar (çözülme): sağ uçtan başlayarak şeritler kısalır
    for i in range(n):
        dy = wv(i)
        # çözülme: lost ilerledikçe sağdaki dilimler solar
        fade = 1.0 - clamp((lost * 1.4 - (1.0 - i / n) * 0.0) - 0.0)
        src = skia.Rect.MakeLTRB(i * sw * 2, 0, (i + 1) * sw * 2, bh * 2)
        dst = skia.Rect.MakeLTRB(x0 + i * sw, top + dy, x0 + (i + 1) * sw + 0.8, top + dy + bh)
        c.drawImageRect(base, src, dst, CM._LIN, pb)
        if kp > 0 and art_alpha > 0.01:
            clip_h = bh * kp
            src2 = skia.Rect.MakeLTRB(i * sw * 2, 0, (i + 1) * sw * 2, bh * 2)
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(x0 + i * sw - 1, top + dy - 2, x0 + (i + 1) * sw + 1, top + dy + clip_h))
            c.drawImageRect(art, src2, dst, CM._LIN, pa)
            c.restore()
    # kesikli iz (kayıp sancağın çerçevesi)
    if lost > 0.05:
        pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.4, Color=C("#5A3E22", int(220 * lost)), StrokeCap=skia.Paint.kRound_Cap)
        pr.setPathEffect(skia.DashPathEffect.Make([16, 12], -cx.t * 14))
        c.drawRect(skia.Rect.MakeLTRB(x0 + 6, top + 6, x0 + bw - 6, top + bh - 6), pr)
    # etiketler
    L.tag(f, cx, "BOTTİCELLİ", 1370, 300, at=a_bot if a_bot is not None else 1e9, size=40, track=8, dur=0.5)
    L.tag(f, cx, "SİMONETTA", 1370, 420, at=a_sim if a_sim is not None else 1e9, size=40, track=8, dur=0.5)
    if a_paint is not None:
        L.tag(f, cx, "MİĞFERLİ PALLAS", 1370, 540, at=a_paint, size=38, track=7, dur=0.5)
    L.stamp_at(f, cx, "○ TEK KAYNAK", 1500, 700, a_stamp if a_stamp is not None else 1e9, rot=-0.08, size=40)
    kl = cx.amt(a_lost, 0.8) if a_lost is not None else 0.0
    if kl > 0.01:
        CM.ink(f, "asıl sancak kayıp", 1370, 820, face="cap_i", size=60, color=TH.fg, align="c", alpha=kl, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c6s23: yarım kalan şiir ═════════════════════════════
@CM.ckind("c6_siir")
def k_siir(cx, a_open=0.0, a_write=None, a_stop=None, a_drop=None, seed=41, **_):
    """Poliziano'nun şiir sayfası: mısralar (okunmaz) tüy kalemle sırayla yazılır; son mısra ortada KESİLİR, kalem düşer, alt satırlar BOŞ kalır (şiir yarım).
    Metin yazılmaz (Stanze metni görülmedi)."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_open, 0.6)
    pw, ph = 660, 800
    pcx, pcy = 960, 530
    pp = PP.paper_image(pw, ph, seed, (240, 230, 200), "deckle", (), 44, 1.0)
    rot = -0.01
    pp.draw(f, pcx, pcy, rot=rot, scale=0.97 + 0.03 * ease_out(a), alpha=a, shadow=0.6)
    c.save()
    c.translate(pcx, pcy)
    c.rotate(math.degrees(rot))
    sp = CM.engraved("POLİZİANO", "title_m", 44, 7.0, "#3A2616", 0.7)
    CM.draw_spr(f, sp, 0, -ph / 2 + 92, "c", alpha=a)
    CM.flourish_rule(f, 0, -ph / 2 + 122, 380, alpha=0.8 * a, color="#7A5A2E", grow=a)
    t0 = cx.at(a_write) if a_write is not None else 1e9
    t_stop = cx.at(a_stop) if a_stop is not None else 1e9
    rows = 12
    tip = None
    for i in range(rows):
        y = -ph / 2 + 190 + i * 46
        ln = 480 - (i % 4) * 36 - (60 if i % 8 == 7 else 0)
        c.drawLine(-pw / 2 + 80, y + 12, pw / 2 - 80, y + 12, S("#5A3E22", 1.1, int(55 * a)))
        ti = t0 + 0.20 * i
        k = clamp((cx.t - ti) / 0.38)
        last = i == rows - 3
        if last:
            k = min(k, 0.46 * clamp((cx.t - ti) / 0.38))
            # son satır yalnızca belirli ilerlemeye kadar
        if i > rows - 3:
            continue                         # son iki satır BOŞ
        if k > 0:
            e = L.scribble(c, -ln / 2, -ln / 2 + ln, y, seed=500 + i, prog=k, a=205)
            if 0 < k < 1 and cx.t < t_stop:
                tip = (e, y)
            if last:
                tip = (e, y)
    # son satır: kesik mürekkep lekesi
    if cx.t > t_stop:
        yy = -ph / 2 + 190 + (rows - 3) * 46
        c.drawCircle(-240 + 0.46 * 480 - 240 + 240, yy + 4, 3.2, P("#1A0F06", 210))
    c.restore()
    # kalem: yazarken uçta; durunca sallanır; düşer
    if tip is not None and cx.t < t_stop + 0.2:
        ca, sa = math.cos(rot), math.sin(rot)
        qx = pcx + tip[0] * ca - tip[1] * sa
        qy = pcy + tip[0] * sa + tip[1] * ca
        K2.draw_quill(f, qx, qy, ang=-38.0 + 4 * math.sin(cx.t * 3.0), alpha=a)
    elif a_drop is not None and cx.t >= cx.at(a_drop):
        u = cx.t - cx.at(a_drop)
        yy = -ph / 2 + 190 + (rows - 3) * 46
        qx0 = pcx + (-240 + 0.46 * 480 - 240 + 240) - 0
        qy0 = pcy + yy
        qx = qx0 + 40 * u
        qy = qy0 - 20 * u + 900 * u * u
        K2.draw_quill(f, qx, qy, ang=-38.0 + 260 * u, alpha=a * clamp(1 - u / 1.4))
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c6s24: Simonetta (1476) ve Giuliano — «bilmiyoruz» ═════════════════════════════
@CM.ckind("c6_iki_madalya")
def k_iki_madalya(cx, a_open=0.0, a_date=None, a_age=None, a_dead=None, a_giu=None, a_link=None, a_unk=None, seed=43, **_):
    """Simonetta madalyası (NİSAN 1476 · 23 YAŞ): solar (gri, yas); sonra Giuliano madalyası ve aralarında kesikli ip + soru işareti: «BİLMİYORUZ»."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_open, 0.8)
    sx, gx, y, ms = 600, 1320, 480, 440
    dim = ease_io(cx.amt(a_dead, 1.6)) if a_dead is not None else 0.0
    c.save()
    if dim > 0.01:
        c.saveLayer(None, skia.Paint(ColorFilter=L.gray_filter(0.85 * dim)))
    CMD.draw_medal_b(f, "c6_simonetta", sx, y, ms * (0.95 + 0.05 * ease_out(a)), "bronze", alpha=a * (1 - 0.25 * dim), tilt=0.1 * math.sin(cx.t * 0.5))
    if dim > 0.01:
        c.restore()
        c.drawCircle(sx, y, ms * 0.485, P("#1A1008", 110 * dim))
    c.restore()
    CM.ink(f, "SİMONETTA", sx, y + ms * 0.62, face="title_m", size=44, color=TH.fg, align="c", track=9, alpha=a, emboss=False)
    if a_date is not None:
        L.tag(f, cx, "NİSAN 1476", sx - 150, 850, at=a_date, size=40, track=7, dur=0.5)
    if a_age is not None:
        L.tag(f, cx, "23 YAŞ", sx + 250, 850, at=a_age, size=40, track=7, dur=0.5)
    # Giuliano
    kg = ease_out(cx.amt(a_giu, 0.9)) if a_giu is not None else 0.0
    if kg > 0.01:
        CMD.draw_medal_b(f, "c6_giuliano", gx, y, ms * (0.93 + 0.07 * kg), "bronze", alpha=kg, tilt=-0.1 * math.sin(cx.t * 0.6))
        CM.ink(f, "GİULİANO", gx, y + ms * 0.62, face="title_m", size=44, color=TH.fg, align="c", track=9, alpha=kg, emboss=False)
    kl = ease_io(cx.amt(a_link, 1.0)) if a_link is not None else 0.0
    if kl > 0.01:
        x0, x1 = sx + ms * 0.52, gx - ms * 0.52
        pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.0, Color=C("#5A3E22", int(225 * kl)), StrokeCap=skia.Paint.kRound_Cap)
        pr.setPathEffect(skia.DashPathEffect.Make([14, 12], -cx.t * 20))
        c.drawLine(x0, y, x0 + (x1 - x0) * kl, y, pr)
        if kl > 0.7:
            bob = 6 * math.sin(cx.t * 2.6)
            icons.draw_icon(f, "question", (x0 + x1) / 2, y - 6 + bob, size=130, metal="bronze", alpha=clamp((kl - 0.7) / 0.3), shadow=True)
    L.tag(f, cx, "BİLMİYORUZ", (sx + gx) / 2, y - 200, at=a_unk if a_unk is not None else 1e9, size=46, track=9, dur=0.5)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c6s25: «Ne güzel şey gençlik, ama kaçıp gidiyor» — kayan yazı ═════════════════════════════
@CM.ckind("c6_canzona")
def k_canzona(cx, a_open=0.0, a_year=None, words1=(), words2=(), a_note=None, seed=47, **_):
    """Karnaval flamaları altında kayan tipografi: «ne güzel şey gençlik,» yazılır; «ama kaçıp gidiyor» sözcükleri sağa kayıp kaçar.
    words1/words2 = [(sözcük, çapa)]; çeviri bize ait notu; tarih «1490»."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_open, 0.7)
    # karnaval flama dizisi (bunting): iki ip + renkli üçgenler
    for ly, amp in ((190, 40), (250, 26)):
        pts = [(0 + i * 120, ly + amp * math.sin(i * 0.55 + cx.t * 0.6) * 0.3 + amp * (1 - math.cos(i / 16 * 2 * math.pi)) * 0.5) for i in range(17)]
        c.drawPath(sk.smooth_path(pts, False, 0.5), S("#5A3E22", 2.4, 230 * a))
        for i in range(16):
            px, py = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
            col = PEN[(i + int(ly)) % len(PEN)][0]
            sw_ = 5 * math.sin(cx.t * 2.0 + i)
            c.drawPath(sk.poly_path([(px - 26, py), (px + 26, py), (px + sw_, py + 66)]), P(col, 235 * a))
            c.drawPath(sk.poly_path([(px - 26, py), (px + 26, py), (px + sw_, py + 66)]), S(INK, 1.4, 190 * a))
    if a_year is not None:
        L.tag(f, cx, "1490", 960, 380, at=a_year, size=46, track=10, dur=0.5)
    # sözcük sözcük yazı
    def place(words, y, size, col, runaway=False):
        x_total = sum(sk.text_width(w, "fell_i", size) + 28 for w, _ in words) - 28
        x = 960 - x_total / 2
        for i, (w, an) in enumerate(words):
            ww = sk.text_width(w, "fell_i", size)
            t0 = cx.at(an)
            k = clamp((cx.t - t0) / 0.45)
            if k <= 0:
                x += ww + 28
                continue
            dx = 0.0
            al = k
            rot = 0.0
            dy = 0.0
            if runaway:
                u = cx.t - (t0 + 0.55)
                if u > 0:
                    dx = 760 * u ** 1.8 + 24 * u
                    dy = -260 * u ** 1.6 * (0.7 + 0.3 * i)
                    rot = 10 * u
                    al = clamp(1 - u / 1.6)
            if al > 0.01:
                c.save()
                c.translate(x + dx + ww / 2, y + dy + 6 * math.sin(cx.t * 1.5 + i))
                c.rotate(rot)
                if runaway:
                    f.text(w, 0, 0, face="fell_i", size=size, color=col, align="c", alpha=al * a)
                else:
                    c.save()
                    c.clipRect(skia.Rect.MakeLTRB(-ww / 2 - 6, -size, -ww / 2 + (ww + 12) * ease_io(k), size * 0.5))
                    f.text(w, 0, 0, face="fell_i", size=size, color=col, align="c", alpha=al * a)
                    c.restore()
                c.restore()
            x += ww + 28
    place(words1, 560, 104, "#2A180D")
    place(words2, 740, 104, "#8E2A1A", runaway=True)
    if a_note is not None:
        CM.ink(f, "çeviri bize ait", 960, 880, face="cap_i", size=34, color=TH.fg3, align="c", alpha=0.95 * cx.amt(a_note, 0.6), emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=24)


# ═════════════════════════════ c6s26: Giostra'dan 26 Nisan 1478'e — zaman şeridi ═════════════════════════════
@CM.ckind("c6_zaman")
def k_zaman(cx, a_open=0.0, a_start=None, a_draw=None, a_draw_dur=3.2, a_end=None, a_sunday=None, a_span=None, seed=53, **_):
    """Uzun ay cetveli (39 çentik): sol uç «29 OCAK 1475» (Giostra), sağ uç «26 NİSAN 1478» (+ PAZAR işareti). Çizgi soldan sağa çizilir, florin boncuğu yuvarlanır;
    sonunda aralığa kıvrık ayraç ve «3 YIL 3 AY» levhası. Kamera boncuğu izler."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress="top")
    cam.begin(f)
    a = cx.amt(a_open, 0.6)
    x0, x1, y = 260, 3500, 520                          # geniş (kamera ile gezilir)
    n = 39
    kd = ease_io(clamp((cx.t - cx.at(a_draw)) / a_draw_dur)) if a_draw is not None else 0.0
    c.drawLine(x0, y, x0 + (x1 - x0) * kd, y, S("#4A3420", 5.0, 235 * a))
    for i in range(n + 1):
        xi = x0 + (x1 - x0) * i / n
        if (xi - x0) / (x1 - x0) > kd:
            break
        big = (i % 12 == 0) or i == n
        c.drawLine(xi, y - (34 if big else 16), xi, y + (34 if big else 16), S("#4A3420", 3.0 if big else 2.0, 225 * a))
    # sol uç: Giostra
    ks = cx.amt(a_start, 0.6) if a_start is not None else 0.0
    if ks > 0.01:
        L.tag(f, cx, "29 OCAK 1475", x0, y - 150, at=a_start, size=44, track=7, dur=0.5)
        c.drawLine(x0, y - 110, x0, y - 38, S("#7A5A2E", 2.2, 200 * ks))
        icons.draw_icon(f, "horse", x0, y + 120, size=110, metal="bronze", alpha=ks, shadow=True)
        CM.ink(f, "GİOSTRA", x0, y + 220, face="title_m", size=38, color=TH.fg2, align="c", track=9, alpha=ks, emboss=False)
    # sağ uç: 26 Nisan 1478 + Pazar
    ke = cx.amt(a_end, 0.6) if a_end is not None else 0.0
    if ke > 0.01:
        L.tag(f, cx, "26 NİSAN 1478", x1, y - 150, at=a_end, size=44, track=7, dur=0.5)
        c.drawLine(x1, y - 110, x1, y - 38, S("#7A5A2E", 2.2, 200 * ke))
    kp = cx.amt(a_sunday, 0.6) if a_sunday is not None else 0.0
    if kp > 0.01:
        L.tag(f, cx, "PAZAR", x1, y + 150, at=a_sunday, size=40, track=10, dur=0.5)
        c.drawLine(x1, y + 40, x1, y + 112, S("#7A5A2E", 2.2, 200 * kp))
    # florin boncuğu
    if kd > 0:
        bx = x0 + (x1 - x0) * kd
        spin = abs(math.cos(cx.t * 5.0))
        icons.draw_icon(f, "coin", bx, y - 4, size=84, metal="gold", alpha=a, shadow=True, rot=0.0, glow=0.2)
    # üç yıl üç ay: ayraç
    kb = ease_io(cx.amt(a_span, 1.0)) if a_span is not None else 0.0
    if kb > 0.01:
        xa_, xb_ = x0, x0 + (x1 - x0) * kb
        yb_ = y + 270
        c.drawPath(sk.smooth_path([(xa_, yb_ - 40), (xa_, yb_), ((xa_ + xb_) / 2, yb_ + 20), (xb_, yb_), (xb_, yb_ - 40)], False, 0.5), S("#8E2A1A", 10.0, 235 * kb))
        L.tag(f, cx, "3 YIL 3 AY", (x0 + x1) / 2, y + 400, at=a_span, size=110, track=10, dur=0.5)
    cam.end(f)
    CM.finish(f, cx, motes_n=22)


# kendi kamera yolu olan türler (qa_flow: yerleşik kamera sayılır)
for _k in ("oda", "c6_giostra", "c6_atolye"):
    cilt_cam.OWN_CAMERA.add(_k)
