"""c11_kinds — c11 «Papa Oğulları» özel çekim türleri ve istasyonları (Parça 5 sahne yazarı). `scenes_c11.py` içinde import edilir; `@CM.ckind` ile kaydolur.

Dil: BEDEL perdesi — duman/kül tonu, ağır nefes, kısa vuruş; yüz çizilmez (siluet madalya / kâğıt-kukla profil), şiddet ve beden gösterilmez
(yağma = duman + bayrak, ölüm = madalya sönmesi/mürekkep çizgisi, Alessandro'nun ölümü = kapı + gölge). Ekrana yalnız script'te SESLENDİRİLEN ad/tarih/sayı yazılır;
saat/mum/şafak/çan iddiası yok. Tüm zamanlar cümle/sözcük çapalıdır (cx.at/cx.amt).

İçerik (özel türler)
  c11_prato    — s1: Prato (surlu şehir, duman sütunları, İspanyol bayrakları), kamera orduya kayar, kardinal Giovanni madalyası
  c11_leo      — s4: çocuk-kardinal madalyası → iki oylama → tiaralı X. Leo
  c11_seritler — s7: iki şerit: «MEDICI PAPASI» ↔ «MEDICI BANKASI — kayyumda»
  c11_borc     — s8: defter: alacaklılar (Bini, Gaddi, Salviati, Strozzi); Medici satırı boş
  c11_hanno    — s9–s10: fil Hanno (siluet), uzun mezar yazıtı, boş anma freski
  c11_akis     — s11: günah affı geliri: yarısı Roma, yarısı Fugger (akış diyagramı)
  c11_zincir   — s14: Leo → Clemens → Şarlken zinciri (Luther itirazı, ordu)
  c11_muhafiz  — s17: 189 → 147 → 42 İsviçre muhafızı ızgarası
  c11_madalya  — genel: zamanlı madalya sahnesi (s13, s16, s22, s23, s32…)
  istasyonlar  — st_papal_horse (s6), st_pulpit_clerk (s12)
"""
import math

import numpy as np
import skia

import c10_kinds as K10
import cilt_anim as FA
import cilt_cam as _CC
import cilt_medici as CM
import cilt_oda as OD
import cilt_pano as PN
import cilt_paper as PP
import cilt_sehir as SE
import icons
import p5_lib as L
import shots as _SH
import sk
from p5_lib import P, S
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth


# ═════════════════════════════ ortak: bayrak, siluet kalabalık ═════════════════════════════
def saltire_flag(c, x, y, w, h, t, seed=0, pole=True, col="#B3201A", cloth="#EFE4C6", wind=1.0):
    """İspanyol (Burgonya) çaprazı bayrağı: krem zemin, kızıl çapraz; dalgalı. x,y = direğin tepesi; sağa uzanır."""
    def pt(u, v):
        wv = math.sin(t * 4.2 * wind - u * 3.6 + seed) * 7.0 * u + math.sin(t * 2.3 + seed * 1.7 + v * 2.0) * 2.0 * u
        return x + u * w, y + v * h + wv
    n = 10
    top = [pt(i / n, 0.0) for i in range(n + 1)]
    bot = [pt(i / n, 1.0) for i in range(n + 1)]
    poly = sk.poly_path(top + bot[::-1])
    if pole:
        c.drawRect(skia.Rect.MakeLTRB(x - 4, y - 10, x + 4, y + h * 3.2), P("#4A3220"))
    c.drawPath(poly, P(cloth))
    for (u0, v0, u1, v1) in ((0, 0, 1, 1), (0, 1, 1, 0)):
        p = skia.Path()
        pts = [pt(u0 + (u1 - u0) * k / n, v0 + (v1 - v0) * k / n) for k in range(n + 1)]
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=h * 0.20, Color=C(col), StrokeJoin=skia.Paint.kRound_Join))
    c.drawPath(poly, S("#2A1608", 2.0, 200))


def _tent(c, x, y, s, col="#D8CCA8", stripe="#A8321E"):
    p = sk.poly_path([(x - s, y), (x, y - s * 0.95), (x + s, y)])
    c.drawPath(p, P(col))
    c.drawPath(p, S("#2A1608", 2.0, 210))
    c.drawPath(sk.poly_path([(x - s * 0.22, y), (x, y - s * 0.55), (x + s * 0.22, y)]), P("#2A1A10"))
    c.drawLine(x - s * 0.5, y - s * 0.47, x + s * 0.5, y - s * 0.47, S(stripe, 4.0, 220))


# ═════════════════════════════ s1 · Prato yağması (duman + bayrak; insan yok) ═════════════════════════════
@CM.ckind("c11_prato")
def k_prato(cx, seed=21, pan_at=0.0, pan_dur=7.0, med_at=0.0, ovl=None, **_):
    """Prato: surlu, kuleli şehir; üç duman sütunu yükselir; sağda İspanyol ordugâhı (çadır + çaprazlı bayraklar). Kamera şehirden orduya kayar (pan_at: başlangıç, pan_dur sn);
    med_at: ordunun yanında kardinal Giovanni siluet madalyası belirir. İnsan figürü, kan, ceset yok: yağma = duman, kıpkızıl pencereler ve yırtık flama."""
    f, c, cam = L.begin(cx, bg="wall", seed=seed, dress="both", push=0.03, drift=(0.0, 0.0))
    t = cx.t
    u = ease_io(clamp((t - cx.at(pan_at)) / pan_dur))
    pan = 760.0 * u
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, 150, W, 935))
    # gök (dumanlı alacakaranlık)
    c.drawRect(skia.Rect.MakeLTRB(0, 150, W, 640), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 150), (0, 640)], [C("#5E4E50"), C("#B87A56"), C("#E8B070")], [0.0, 0.62, 1.0])))
    # uzak tepeler (paralaks 0.25)
    c.save()
    c.translate(-pan * 0.25, 0)
    hp = skia.Path()
    hp.moveTo(-200, 640)
    for i in range(0, 14):
        hp.quadTo(-200 + i * 260 + 130, 520 - 38 * ((i * 7) % 4), -200 + (i + 1) * 260, 640)
    hp.lineTo(3600, 700)
    hp.lineTo(-200, 700)
    hp.close()
    c.drawPath(hp, P("#7A6858", 255))
    c.restore()
    # şehir (paralaks 0.72): sur, kuleler, evler, çan kulesi, kapı
    c.save()
    c.translate(-pan * 0.72, 0)
    rs = np.random.RandomState(5)
    wall_y0, wall_y1 = 520, 700
    for i in range(36):                                                       # evlerin çatıları (surun ardında)
        hx = 260 + i * 40 + rs.uniform(-6, 6)
        hh = rs.uniform(50, 120)
        hw = rs.uniform(46, 70)
        c.drawRect(skia.Rect.MakeLTRB(hx, wall_y0 - hh, hx + hw, wall_y0 + 10), P(mix("#A89070", "#8A7458", rs.rand())))
        c.drawPath(sk.poly_path([(hx - 4, wall_y0 - hh), (hx + hw / 2, wall_y0 - hh - 30), (hx + hw + 4, wall_y0 - hh)]), P(mix("#B0482E", "#8E3A26", rs.rand())))
    c.drawRect(skia.Rect.MakeLTRB(660, 250, 730, wall_y0), P("#B8A47C"))                  # çan kulesi
    c.drawRect(skia.Rect.MakeLTRB(660, 250, 730, wall_y0), S("#3A2A18", 2.0, 220))
    c.drawRect(skia.Rect.MakeLTRB(654, 230, 736, 262), P("#9A8660"))
    for k in range(3):
        c.drawPath(sk.poly_path([(662 + k * 24, 258), (668 + k * 24, 236), (674 + k * 24, 258)]), P("#2A1A10", 230))
    c.drawPath(sk.poly_path([(650, 230), (695, 168), (740, 230)]), P("#9A3A24"))
    c.drawRect(skia.Rect.MakeLTRB(150, wall_y0, 1760, wall_y1), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, wall_y0), (0, wall_y1)], [C("#C2AE82"), C("#8E7A56")], [0.0, 1.0])))
    for gx in range(150, 1760, 56):                                             # mazgallar
        c.drawRect(skia.Rect.MakeLTRB(gx, wall_y0 - 26, gx + 32, wall_y0), P("#C2AE82"))
        c.drawRect(skia.Rect.MakeLTRB(gx, wall_y0 - 26, gx + 32, wall_y0), S("#3A2A18", 1.6, 200))
    for tx in (150, 520, 1010, 1470, 1740):                                     # kuleler
        c.drawRect(skia.Rect.MakeLTRB(tx - 46, wall_y0 - 90, tx + 46, wall_y1), P("#B09A70"))
        c.drawRect(skia.Rect.MakeLTRB(tx - 46, wall_y0 - 90, tx + 46, wall_y1), S("#3A2A18", 2.2, 220))
        for gx in range(tx - 46, tx + 46, 24):
            c.drawRect(skia.Rect.MakeLTRB(gx, wall_y0 - 112, gx + 14, wall_y0 - 90), P("#B09A70"))
    c.drawRect(skia.Rect.MakeLTRB(150, wall_y0, 1760, wall_y1), S("#3A2A18", 3.0, 230))
    gp = skia.Path()                                                           # kapı (açık, karanlık)
    gp.moveTo(760, wall_y1)
    gp.lineTo(760, 620)
    gp.arcTo(skia.Rect.MakeLTRB(760, 560, 880, 680), 180, 180, False)
    gp.lineTo(880, wall_y1)
    gp.close()
    c.drawPath(gp, P("#150E0A"))
    # kıpkızıl pencereler (yağma = ışık/duman dili; insan yok)
    for k in range(7):
        wx = 270 + k * 190 + (k % 2) * 40
        kk = clamp(0.5 + 0.5 * math.sin(t * 3.0 + k * 1.9))
        PN.glow(c, wx, 600, 46, "#FF7A22", 0.36 + 0.3 * kk)
        c.drawRect(skia.Rect.MakeLTRB(wx - 7, 584, wx + 7, 616), P("#FFB347", int(180 + 70 * kk)))
    # duman sütunları
    for i, (sx, h_, w_) in enumerate(((420, 640, 120), (940, 760, 150), (1360, 600, 110), (1700, 520, 100))):
        SE.smoke_column(c, sx, 560, t, h=h_, w=w_, col="#2E2824", seed=i + 7, wind=90, a0=0.92, glow_a=0.45)
    c.restore()
    # zemin
    c.drawRect(skia.Rect.MakeLTRB(0, 700, W, 935), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 700), (0, 935)], [C("#8E7A52"), C("#5E5036")], [0.0, 1.0])))
    # ön plan (paralaks 1.0): tabela, yol, ordugâh
    c.save()
    c.translate(-pan, 0)
    rp = skia.Path()
    rp.moveTo(700 * 0.72 + 80, 705)
    rp.lineTo(700 * 0.72 + 200, 705)
    rp.lineTo(760, 935)
    rp.lineTo(120, 935)
    rp.close()
    c.drawPath(rp, P("#A89062", 150))
    # yol tabelası: PRATO (eğik, yırtık)
    sx_, sy_ = 360, 800
    c.drawRect(skia.Rect.MakeLTRB(sx_ - 7, sy_ - 210, sx_ + 7, sy_), P("#4A3220"))
    c.save()
    c.translate(sx_, sy_ - 190)
    c.rotate(-6)
    c.drawRect(skia.Rect.MakeLTRB(-120, -34, 120, 34), P("#8A6A3A"))
    c.drawRect(skia.Rect.MakeLTRB(-120, -34, 120, 34), S("#2A1608", 3.0, 230))
    c.restore()
    for i in range(7):                                                         # ordugâh: çadırlar
        _tent(c, 1780 + i * 190 + (i % 2) * 40, 880 - (i % 3) * 26, 92 - (i % 3) * 10)
    for i, bx in enumerate((1760, 1960, 2160, 2360, 2560)):                    # bayraklar
        saltire_flag(c, bx, 520 - 20 * (i % 2), 118, 76, t, seed=i * 1.3)
    c.restore()
    # Giovanni madalyası (ordunun yanında)
    km = cx.amt(med_at, 0.9)
    if km > 0.003:
        mx, my = 2180 - pan, 630
        L.sil_medal(f, mx, my + 4 * math.sin(t * 1.3), 150 * (0.88 + 0.12 * ease_out(km)), hat="galero", alpha=km, tilt=0.03 * math.sin(t * 0.8), nose=1.0)
    c.restore()
    cam.end(f)
    CM.finish(f, cx, motes_n=22)
    if ovl is not None:
        ovl(cx)


# ═════════════════════════════ s4 · çocuk-kardinal → iki oylama → X. Leo ═════════════════════════════
@CM.ckind("c11_leo")
def k_leo(cx, seed=22, child_at=0.0, red_at=0.0, grow_at=0.0, vote1_at=0.0, vote2_at=0.0, pope_at=0.0, ovl=None, **_):
    """Giovanni: küçük çıplak başlı madalya (çocuk) → kırmızı galero konur (kardinal) → merkeze büyür (grow_at: «mart 1513») → iki oy pusulası kutuya düşer (vote1_at/vote2_at)
    → tiara konur (pope_at: «papa seçildi»), altın patlama. Yüz yok."""
    f, c, cam = L.begin(cx, bg="wall", seed=seed, dress="both", push=0.045, drift=(6.0, 2.0))
    t = cx.t
    kc = cx.amt(child_at, 0.8)
    kg = ease_io(clamp((t - cx.at(grow_at)) / 1.3))
    x = lerp(560, 900, kg)
    y = lerp(620, 570, kg)
    R_ = lerp(96, 205, kg)
    kr = ease_out(clamp((t - cx.at(red_at)) / 0.55), 2.2)
    kp = ease_out(clamp((t - cx.at(pope_at)) / 0.7), 2.4)
    hat = "tiara" if kp > 0.02 else ("galero" if kr > 0.02 else "bare")
    hk = kp if hat == "tiara" else (kr if hat == "galero" else 1.0)
    if kp > 0.0:
        PN.glow(c, x, y, R_ * 2.2, "#FFD27A", 0.34 * kp * (1.0 - 0.4 * kp))
    L.sil_medal(f, x, y + 3 * math.sin(t * 1.3), R_ * (0.88 + 0.12 * ease_out(kc)), hat=hat, alpha=kc, hat_k=hk, tilt=0.03 * math.sin(t * 0.8), nose=1.0)
    if kr > 0.02 and kp < 0.5:                                                  # galero parlaması (sinabar)
        PN.glow(c, x, y - R_ * 0.8, R_ * 0.9, "#C8402A", 0.16 * kr)
    # oy kutusu + iki pusula
    bx, by = 1450, 760
    kb = cx.amt(vote1_at, 0.7, off=-0.9)
    if kb > 0.003:
        c.drawRect(skia.Rect.MakeLTRB(bx - 130, by, bx + 130, by + 140), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, by), (0, by + 140)], [C("#7A5632", int(255 * kb)), C("#4A3220", int(255 * kb))], [0.0, 1.0])))
        c.drawRect(skia.Rect.MakeLTRB(bx - 130, by, bx + 130, by + 140), S("#1A0F08", 3.0, int(240 * kb)))
        c.drawRect(skia.Rect.MakeLTRB(bx - 70, by - 6, bx + 70, by + 8), P("#1A0F08", int(255 * kb)))
        for i, anc in enumerate((vote1_at, vote2_at)):
            d = clamp((t - cx.at(anc)) / 0.9)
            if 0.0 < d < 1.0:
                py = lerp(by - 330, by - 14, ease_in(d, 1.8))
                icons.draw_icon(f, "ballot", bx - 40 + 80 * i + 6 * math.sin(d * 9.0), py, size=120, metal="gold", alpha=1.0, rot=0.3 * math.sin(d * 7.0))
            elif d >= 1.0:
                kt = ease_out(clamp((t - cx.at(anc) - 0.9) / 0.4), 2.0)
                tx_ = bx - 70 + 140 * i
                pa = f.paint("#2E7A3A", style="stroke", sw=9.0, alpha=0.95 * kt)
                c.drawLine(tx_ - 26, by + 76, tx_ - 8 + 4 * 0, by + 98, pa)
                c.drawLine(tx_ - 8, by + 98, tx_ + 34 * kt, by + 58 - 8 * kt, pa)
    cam.end(f)
    CM.finish(f, cx, motes_n=16, light=CM.candle_light(t, seed, base=(W * 0.5, 480), r=1500.0, sway=8.0))
    if ovl is not None:
        ovl(cx)


# ═════════════════════════════ s6 · beyaz at, yedekten yürüten Alfonso d'Este (pano istasyonu) ═════════════════════════════
def st_papal_horse(ctx, st):
    """Pano `florence` istasyonu: beyaz atlı Papa (beyaz cübbe) soldan sağa yavaş yürür (yükseliş yönü); atın yedeğini aforozlu Alfonso d'Este yürüyerek çeker (önde, kısa ip).
    st: x (t=0 konumu), speed. İki figür de kâğıt-kukla profil (yüz iddiası yok)."""
    f, c, t = ctx.f, ctx.c, ctx.t
    sp = st.get("speed", 80.0)
    x = st["x"] + sp * t
    yg = 846
    # Alfonso: atın önünde, yedekte
    FA.walker(f, "soylu", x + 330, yg - 4, 232, t, speed=sp, dir=1, seed=33, robe="#2A2230", robe2="#8A6A3A", hat_col="#1A1008")
    FA.rider(f, x, yg, 330, t, speed=sp, gait="walk", dir=1, seed=9, coat="#F0E8D4", cloth="#EFE8DA", cl_pat=("fleur", "#E8C25A"), robe="#F2EDE0", robe2="#E0B84E", hat="mazzocchio", hat_col="#E8C25A")
    c.drawLine(x + 214, yg - 190, x + 304, yg - 140, f.paint("#3A2616", style="stroke", sw=3.0, alpha=0.9))


# ═════════════════════════════ s7 · iki şerit: Medici papası ↔ Medici bankası (kayyumda) ═════════════════════════════
@CM.ckind("c11_seritler")
def k_seritler(cx, seed=23, pope_at=0.0, bank_at=0.0, lock_at=0.0, key_at=0.0, ovl=None, **_):
    """Ekran ikiye bölünür: ÜST şerit sıcak/altın — tiaralı Papa madalyası (pope_at); ALT şerit soğuk/kurşun — kapalı banka (bank_at): sandık + zincir (lock_at), anahtar kayyuma geçer (key_at)."""
    f, c, cam = L.begin(cx, bg="wall", seed=seed, dress="both", push=0.04, drift=(6.0, 0.0))
    t = cx.t
    kp = ease_out(clamp((t - cx.at(pope_at)) / 0.9), 2.2)
    kb = ease_out(clamp((t - cx.at(bank_at)) / 0.9), 2.2)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, 150, W, 540))
    c.translate(0, -(1 - kp) * 400)
    c.drawRect(skia.Rect.MakeLTRB(0, 150, W, 540), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 150), (0, 540)], [C("#F2D898"), C("#D8A850")], [0.0, 1.0])))
    for i in range(14):                                                           # ışın demetleri
        a_ = -1.25 + i * 0.19
        c.drawPath(sk.poly_path([(960, 330), (960 + 1600 * math.sin(a_ - 0.04), 330 - 1600 * math.cos(a_ - 0.04)), (960 + 1600 * math.sin(a_ + 0.04), 330 - 1600 * math.cos(a_ + 0.04))]), P("#FFF1B8", 46))
    PN.glow(c, 960, 340, 330, "#FFF1B8", 0.5)
    L.sil_medal(f, 960, 340, 150, hat="tiara", alpha=1.0, tilt=0.025 * math.sin(t * 0.8), nose=1.0)
    c.restore()
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, 540, W, 935))
    c.translate(0, (1 - kb) * 400)
    c.drawRect(skia.Rect.MakeLTRB(0, 540, W, 935), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 540), (0, 935)], [C("#6E7684"), C("#3E4452")], [0.0, 1.0])))
    for xx in range(0, W, 120):                                                   # sönük defter rafı çizgileri
        c.drawLine(xx, 560, xx, 935, S("#2A3040", 2.0, 110))
    c.drawRect(skia.Rect.MakeLTRB(280, 800, 1640, 840), P("#2E3442"))               # banka tezgâhı
    c.drawRect(skia.Rect.MakeLTRB(280, 800, 1640, 806), P("#8A92A4"))
    kl = ease_out(clamp((t - cx.at(lock_at)) / 0.55), 2.0)
    icons.draw_icon(f, "chest", 760, 700, size=280, metal="lead", alpha=1.0)
    if kl > 0.003:
        icons.draw_icon(f, "chains", 760, 690 - (1 - kl) * 200, size=330, metal="lead", alpha=kl)
    kk = clamp((t - cx.at(key_at)) / 1.4)
    kay = cx.amt(key_at, 0.6)
    if kay > 0.003:                                                               # kayyum: berretto madalyası; anahtar ona geçer
        L.sil_medal(f, 1340, 700, 100, hat="berretto", alpha=kay, tilt=0.03 * math.sin(t * 0.9), flip=True, nose=1.0)
        ux = lerp(850, 1260, ease_io(kk))
        uy = 640 - 130 * math.sin(math.pi * ease_io(kk))
        icons.draw_icon(f, "keys", ux, uy, size=120, metal="bronze", alpha=1.0 - 0.6 * smooth(clamp((kk - 0.85) / 0.15)), rot=0.4 * math.sin(kk * 8.0))
    c.restore()
    c.drawRect(skia.Rect.MakeLTRB(0, 536, W, 546), P("#C79A3C"))
    cam.end(f)
    CM.finish(f, cx, motes_n=14)
    if ovl is not None:
        ovl(cx)


# ═════════════════════════════ s8 · defter: alacaklılar (Medici satırı boş) ═════════════════════════════
@CM.ckind("c11_borc")
def k_borc(cx, seed=24, head_at=0.0, rows_at=(), none_at=0.0, strike_at=0.0, ovl=None, **_):
    """Defter sayfası: başlık «BORÇ»; alacaklılar satır satır yazılır (rows_at: [(ad, çapa)]); beşinci satır Medici bankası için KESİKLİ boş yuva, `strike_at`'ta üstü çizilir.
    Solda Leo (tiaralı madalya) `head_at`'ta belirir ve söner."""
    f, c, cam = L.begin(cx, bg="wall", seed=seed, dress="both", push=0.04, drift=(-5.0, 0.0))
    t = cx.t
    k0 = cx.amt(head_at, 0.8)
    px, py, pw, ph = 1060, 560, 1040, 700
    pp = PP.paper_image(pw, ph, 12, (226, 212, 180), "deckle", (("h", 0.5),), 44, 1.0)
    pp.draw(f, px, py + (1 - ease_out(k0)) * 80, rot=-0.01, scale=1.0, alpha=k0, shadow=0.6)
    c.save()
    c.translate(px - pw / 2, py - ph / 2 + (1 - ease_out(k0)) * 80)
    ink = "#2A180D"
    c.drawRect(skia.Rect.MakeLTRB(60, 120, pw - 60, 124), P(ink, int(170 * k0)))
    for i in range(6):
        yy = 190 + i * 98
        c.drawLine(60, yy + 46, pw - 60, yy + 46, S("#8A6A3A", 1.6, int(110 * k0)))
    rs = [(nm, a) for nm, a in rows_at]
    for i, (nm, anc) in enumerate(rs):
        k = cx.amt(anc, 0.5)
        if k <= 0.003:
            continue
        yy = 190 + i * 98
        CM.ink(f, nm, 90, yy + 36, face="fell_i", size=54, color="#2A180D", align="l", alpha=k, emboss=False)
        L.scribble(c, 520, 520 + 120 + 80 * ((i * 5) % 4), yy + 20, seed=40 + i, col="#2A180D", a=int(200 * k), amp=3.0, prog=ease_out(k), w=2.4)
    kn = cx.amt(none_at, 0.6)
    if kn > 0.003:                                                                # Medici: boş, kesikli yuva
        yy = 190 + 4 * 98
        pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.4, Color=C("#8A6A3A", int(220 * kn)))
        pr.setPathEffect(skia.DashPathEffect.Make([14, 10], -t * 18))
        c.drawRect(skia.Rect.MakeLTRB(70, yy + 6, pw - 70, yy + 76), pr)
        CM.ink(f, "MEDİCİ BANKASI", 90, yy + 54, face="fell_i", size=46, color="#8A7A5A", align="l", alpha=0.55 * kn, emboss=False)
        ks = ease_out(clamp((t - cx.at(strike_at)) / 0.5), 2.0)
        if ks > 0.01:
            pa = f.paint("#A8321E", style="stroke", sw=9.0, alpha=0.95)
            CM.wobble(pa, 7.0, 1.4, 4)
            c.drawLine(70, yy + 44, 70 + (pw - 140) * ks, yy + 40, pa)
    c.restore()
    cam.end(f)
    CM.finish(f, cx, motes_n=14, light=CM.candle_light(t, seed, base=(W * 0.6, 520), r=1500.0, sway=8.0))
    if ovl is not None:
        ovl(cx)
