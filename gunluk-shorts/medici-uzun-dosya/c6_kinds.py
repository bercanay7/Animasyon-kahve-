"""c6_kinds — c6 «Lorenzo» özel çekim türleri (Parça 3 sahne yazarı). `scenes_c6.py` içinde import edilir; `@CM.ckind` ile kaydolur.

Dil: gündüz, sıcak sıva-kâğıt (perde ALTIN); anlatı sıcak ve hafif; Giostra'dan sonra ışık soğur (kapı: Giuliano).
Kaynak disiplini: yüz yok (stilize madalya/siluet), şiddet yok; ekrana yalnız script/brif sözcükleri yazılır. Ten rengi/ses/koku alayı YOK.
Tüm zamanlar cümle/sözcük çapalı (cx.at / cx.amt); mutlak saniye yok.
"""
import math

import numpy as np
import skia

import cilt_anim as FA
import cilt_kinds2 as K2
import cilt_medal as CMD
import cilt_medici as CM
import cilt_paper as PP
import icons
import p3_lib as L
import sk
from cilt_medici import TH
from p3_lib import INK, P, S, FILLP, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth
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
            gx, gy, gw = hx - 250, 800, 500
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
