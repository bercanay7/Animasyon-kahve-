"""c15_kinds — c15 «Son Medici'ler» özel çekim türleri (Parça 7 sahne yazarı). `scenes_c15.py` içinde import edilir; `@CM.ckind` ile kaydolur.
Ruh hâli: AĞIR/YORGUN — kamera yavaş, ışık/toz/alev canlı; şiddet/ceset/hastalık/yatak YOK (mum, levha, simge, siluet). Zehir iddiası MİT/rivayet, DNA «büyük olasılıkla sıtma»
(ekranda «zehir çürütüldü» YOK). Ekrana yalnız script/brif sözcükleri yazılır; `mode`/`perde` ckind sarmalayıcısına aittir (tür parametresi olarak kullanma).
"""
import math

import numpy as np
import skia

import c14_kinds as K14
import cilt_anim as FA
import cilt_medici as CM
import cilt_oda as OD
import cilt_paper as PP
import icons
import p7_lib as L
import sk
from c14_kinds import A, palle_mark, script_line, seal_ring, wood_floor, scribble_line
from cilt_medici import TH
from p7_lib import P, S, SOFT, look, ov
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth


# ═══════════════════════════ ovl: yarım daire etiketler (studiolo: «yarı ofis, yarı laboratuvar…») ═══════════════════════════
def half_label(text, x, y, at, out=None, r=34, size=30, dur=0.6):
    """Yarısı dolu daire (altın) + etiket: «yarı …» ifadeleri için. (x,y) simge merkezi."""
    def fn(cx):
        k = L._kk(cx, at, dur, out, 0.5)
        if k <= 0.003:
            return
        f = cx.f
        c = f.c
        wd = sk.text_width(text, "title_m", size, 5) + 2 * r + 100
        CM.tablet(f, x - r - 34, y - r - 26, wd, 2 * r + 52, alpha=k, corner=12)
        rr = r * (0.7 + 0.3 * ease_out(k, 3))
        c.drawCircle(x, y, rr, S("#7A5C32", 3.4, A(255 * k)))
        pa = skia.Path()
        pa.moveTo(x, y)
        pa.arcTo(skia.Rect.MakeLTRB(x - rr, y - rr, x + rr, y + rr), 90, 180, False)
        pa.close()
        c.drawPath(pa, P("#D8A63A", A(255 * k)))
        CM.ink(f, text, x + r + 22, y + size * 0.36, face="title_m", size=size, color=TH.fg, align="l", track=5, alpha=k, emboss=False)
    return fn


# ═══════════════════════════ ovl: söylenti ipleri ═══════════════════════════
def whispers(at, pts, out=None, col="#E8D7A0", dur=1.6):
    """Pencereden pencereye geçen ince söylenti çizgisi (kesik çizgi, hareket eden boncuk). pts=[(x,y),…] ekran noktaları; `at`'ta yola çıkar."""
    def fn(cx):
        k = ease_io(clamp((cx.t - cx.at(at)) / dur))
        if k <= 0.003:
            return
        al = 1.0 - (cx.amt(out, 0.6) if out is not None else 0.0)
        if al <= 0.01:
            return
        c = cx.f.c
        pa = skia.Path()
        pa.moveTo(*pts[0])
        for i in range(1, len(pts)):
            xm, ym = (pts[i - 1][0] + pts[i][0]) / 2, min(pts[i - 1][1], pts[i][1]) - 90
            pa.quadTo(xm, ym, pts[i][0], pts[i][1])
        pm = skia.PathMeasure(pa, False)
        seg = skia.Path()
        pm.getSegment(0, pm.getLength() * k, seg, True)
        p = S(col, 4.0, A(220 * al))
        p.setPathEffect(skia.DashPathEffect.Make([10, 12], -cx.t * 26))
        c.drawPath(seg, p)
        pos, _ = pm.getPosTan(pm.getLength() * k)
        if pos is not None:
            c.drawCircle(pos.x(), pos.y(), 9, P("#FFF1B8", A(255 * al)))
            c.drawCircle(pos.x(), pos.y(), 22, P("#FFF1B8", A(60 * al)))
    return fn


def pie(c, x, y, r=60, a=255):
    """Turta (basit): kenar + kafes dilimler."""
    c.drawOval(skia.Rect.MakeLTRB(x - r, y - r * 0.55, x + r, y + r * 0.55), P("#C98F5A", a))
    c.drawOval(skia.Rect.MakeLTRB(x - r, y - r * 0.55, x + r, y + r * 0.55), S("#5A3418", 3.0, a))
    c.drawOval(skia.Rect.MakeLTRB(x - r * 0.78, y - r * 0.42, x + r * 0.78, y + r * 0.40), P("#E2B070", a))
    for i in range(-2, 3):
        c.drawLine(x + i * r * 0.28 - r * 0.2, y - r * 0.4, x + i * r * 0.28 + r * 0.2, y + r * 0.38, S("#8A5A2E", 3.0, a))
        c.drawLine(x - r * 0.7, y + i * r * 0.17 - r * 0.1, x + r * 0.7, y + i * r * 0.17 + r * 0.1, S("#8A5A2E", 3.0, a))


# ═══════════════════════════ c15_iki_mum: bir gün arayla ═══════════════════════════
@CM.ckind("c15_iki_mum")
def k_iki_mum(cx, a1=1.0, a2=2.6, out1=5.0, out2=6.2, names=("I. FRANCESCO", "BIANCA CAPPELLO"), seed=3, ovl=None, **_):
    """Karanlık oda; iki mum yan yana (adlarıyla); birincisi söner, aradaki bir günü gösteren ince güneş kadranı döner, ikincisi söner. Hiçbir şiddet/beden yok."""
    f = cx.f
    cam = CM.Cam(cx, push=0.04, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    wood_floor(c, 790, seed=seed)
    xs = (700.0, 1220.0)
    t1, t2 = cx.at(out1), cx.at(out2)
    for i, (xc, nm, an) in enumerate(zip(xs, names, (a1, a2))):
        k = cx.amt(an, 0.8)
        if k <= 0.003:
            continue
        to = (t1, t2)[i]
        lit = (1.0 - ease_in(clamp((t - to) / 0.9), 1.6)) * k
        OD.candle(f, xc, 790, 280, t, seed=3 + i * 5, lit=lit, holder=True)
        wd = sk.text_width(nm, "title_m", 34, 6) + 80
        CM.tablet(f, xc - wd / 2, 830, wd, 78, alpha=k * (0.55 + 0.45 * (1.0 if t < to else 0.0)), corner=8)
        CM.ink(f, nm, xc, 884, face="title_m", size=34, color=TH.fg, align="c", track=5, alpha=k, emboss=False)
    # gün kadranı (iki sönüş arasında bir tur)
    kd = clamp((t - t1) / max(0.1, t2 - t1))
    ka = cx.amt(out1, 0.6)
    if ka > 0.003:
        dx_, dy_, rr = 960.0, 560.0, 84.0
        c.drawCircle(dx_, dy_, rr, S("#C9A24A", 3.0, A(150 * ka)))
        for i in range(12):
            an = i * math.pi / 6
            c.drawLine(dx_ + math.cos(an) * rr * 0.86, dy_ + math.sin(an) * rr * 0.86, dx_ + math.cos(an) * rr, dy_ + math.sin(an) * rr, S("#C9A24A", 2.2, A(150 * ka)))
        an = -math.pi / 2 + kd * 2 * math.pi
        sx_, sy_ = dx_ + math.cos(an) * rr, dy_ + math.sin(an) * rr
        c.drawCircle(sx_, sy_, 24, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((sx_, sy_), 24, [C("#FFF3C4", A(255 * ka)), C("#FFD27A", 0)], [0, 1])))
        c.drawCircle(sx_, sy_, 9, P("#FFF8E0", A(255 * ka)))
    light = CM.candle_light(t, seed, base=(960, 560), r=840.0 + 200 * (1 - clamp((t - t2) / 1.5)), sway=6.0)
    cam.end(f)
    CM.finish(f, cx, motes_n=26, light=light, vig_s=0.6)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c15_dna: üç örnek, iki parazit DNA'sı ═══════════════════════════
def draw_vial(c, x, y, h=300, w=64, fill=0.7, col="#9AD0E8", a=255):
    c.drawRoundRect(skia.Rect.MakeLTRB(x - w / 2, y - h, x + w / 2, y), w / 2, w / 2, P("#E8F4FA", A(60 * a / 255)))
    lv = y - h * fill
    c.drawRoundRect(skia.Rect.MakeLTRB(x - w / 2 + 6, lv, x + w / 2 - 6, y - 6), w / 2 - 6, w / 2 - 6, P(col, A(0.8 * a)))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - w / 2, y - h, x + w / 2, y), w / 2, w / 2, S("#E8F4FA", 3.0, A(0.9 * a)))
    c.drawRect(skia.Rect.MakeLTRB(x - w / 2 - 6, y - h - 18, x + w / 2 + 6, y - h + 6), P("#7A5430", a))
    c.drawLine(x - w * 0.22, y - h + 20, x - w * 0.22, y - 24, S("#FFFFFF", 4, A(0.5 * a)))


@CM.ckind("c15_dna")
def k_dna(cx, vials_at=0.4, three_at=1.4, helix_at=2.6, two_at=4.4, seed=4, ovl=None, **_):
    """Gece laboratuvar tezgâhı: üç numune tüpü (kaburga numuneleri; kemik gösterilmez), mavi DNA sarmalı döner (DNA katmanı mavi), iki parazit simgesi (halka+nokta) yanar.
    «3» ve «2» altın rakamlar kendi sözcüklerinde belirir."""
    f = cx.f
    cam = CM.Cam(cx, push=0.04, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    wood_floor(c, 790, seed=seed)
    for i in range(3):
        k = cx.amt(vials_at, 0.6, off=0.25 * i, ease=lambda u: ease_out(u, 3))
        if k > 0.003:
            draw_vial(c, 300 + i * 150, 790 + (1 - k) * 60, 280, 70, 0.55 + 0.1 * i, "#7FB6D8", A(255 * k))
    k3 = cx.amt(three_at, 0.45, ease=lambda u: ease_out(u, 3))
    if k3 > 0.003:
        sp = CM.gilt("3", "title", 150, 4.0)
        CM.draw_spr(f, sp, 450, 330, "c", alpha=k3, scale=1.0 + 0.2 * (1 - k3), glow=0.2)
    kh = cx.amt(helix_at, 0.9)
    if kh > 0.003:
        hx, hy, hh = 1060.0, 540.0, 520.0
        n = 22
        for s_ in (0, 1):
            pa = skia.Path()
            for i in range(n + 1):
                u = i / n
                ang = u * 4 * math.pi + t * 1.3 + s_ * math.pi
                x = hx + math.sin(ang) * 90
                y = hy - hh / 2 + hh * u
                pa.moveTo(x, y) if i == 0 else pa.lineTo(x, y)
            c.drawPath(pa, S("#3E6FD0" if s_ == 0 else "#7FA3E8", 12, A(235 * kh)))
        for i in range(n + 1):
            u = i / n
            ang = u * 4 * math.pi + t * 1.3
            x1, x2 = hx + math.sin(ang) * 90, hx - math.sin(ang) * 90
            y = hy - hh / 2 + hh * u
            c.drawLine(x1, y, x2, y, S("#C9DAF4", 4, A(150 * kh * (0.4 + 0.6 * abs(math.cos(ang))))))
        f.circle(hx, hy, 300, shader=f.rad(hx, hy, 300, [("#7FA3E8", 0.0, int(50 * kh)), ("#7FA3E8", 1.0, 0)]))
    k2 = cx.amt(two_at, 0.5, ease=lambda u: ease_out(u, 3))
    if k2 > 0.003:
        for j in range(2):
            px, py = 1560, 400 + j * 230
            c.drawCircle(px, py, 66, P("#E8C8C0", A(70 * k2)))
            c.drawCircle(px, py, 58, S("#A83A3A", 7, A(255 * k2)))
            c.drawCircle(px + 40, py - 20, 12, P("#A83A3A", A(255 * k2)))
            f.circle(px, py, 100, shader=f.rad(px, py, 100, [("#FFD27A", 0.0, int(90 * k2 * (0.6 + 0.4 * math.sin(t * 4 + j)))), ("#FFD27A", 1.0, 0)]))
        sp = CM.gilt("2", "title", 150, 4.0)
        CM.draw_spr(f, sp, 1760, 520, "c", alpha=k2, scale=1.0 + 0.2 * (1 - k2), glow=0.2)
    cam.end(f)
    CM.finish(f, cx, motes_n=24, light=CM.candle_light(t, seed, base=(1000, 520), r=1100.0, sway=8.0), vig_s=0.55)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c15_baslik: iki haber başlığı, iki ayrı kesinlik ═══════════════════════════
@CM.ckind("c15_baslik")
def k_baslik(cx, a1=0.4, a2=2.2, join_at=4.0, heads=("“KİTABI KAPATTI”", "“ÇÖZÜLMÜŞ OLABİLİR”"), seed=6, ovl=None, **_):
    """İki gazete kupürü yan yana: sol «KİTABI KAPATTI» (iri, sert damga ✓), sağ «ÇÖZÜLMÜŞ OLABİLİR» (soru işareti). Üstte «AYNI ÇALIŞMA» ayracı iki kupüre iner (kısa, kuru)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.045, drift=(3.0, 1.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    for i, (xc, an, hd) in enumerate(((520.0, a1, heads[0]), (1400.0, a2, heads[1]))):
        k = cx.amt(an, 0.7, ease=lambda u: ease_out(u, 3))
        if k <= 0.003:
            continue
        yc = 540 + (1 - k) * 50
        pp = PP.paper_image(720, 560, seed + i * 3, (234, 225, 198), "deckle", (), 44, 1.1)
        pp.draw(f, xc, yc, rot=(-0.02 if i == 0 else 0.015), scale=0.96 + 0.04 * k, alpha=k, shadow=0.6)
        c.save()
        c.translate(xc, yc)
        c.rotate(math.degrees(-0.02 if i == 0 else 0.015))
        lines = sk.wrap_text(hd, "title", 58, 600, 3.0)
        for j, ln in enumerate(lines):
            CM.ink(f, ln, 0, -110 + j * 84, face="title", size=58, color="#1A120A", align="c", track=3, alpha=k, emboss=False)
        for r in range(6):
            kk = cx.amt(an, 0.5, off=0.5 + 0.12 * r)
            c.drawLine(-290, 90 + r * 28, -290 + (560 - (r % 3) * 70) * kk, 90 + r * 28, S("#2A1A0E", 3.0, A(120 * kk)))
        c.restore()
        ks = cx.amt(an, 0.3, off=1.1)
        if ks > 0:
            if i == 0:
                CM.stamp(f, "KESİN", xc + 170, yc + 190, rot=-0.10, size=62, color="#2E6A46", alpha=1.0, t=ks)
            else:
                icons.draw_icon(f, "question", xc + 220, yc + 180, size=130 * (0.8 + 0.2 * ks), metal="gold", alpha=ks, glow=0.0)
    kj = cx.amt(join_at, 0.9, ease=lambda u: ease_out(u, 3))
    if kj > 0.003:
        pa = skia.Path()
        pa.moveTo(520, 190)
        pa.lineTo(520, 150)
        pa.lineTo(1400, 150)
        pa.lineTo(1400, 190)
        seg = skia.Path()
        pm = skia.PathMeasure(pa, False)
        pm.getSegment(0, pm.getLength() * kj, seg, True)
        c.drawPath(seg, S("#7A1E16", 5, A(240 * kj)))
        CM.ink(f, "AYNI ÇALIŞMA", 960, 134, face="title_m", size=34, color="#7A1E16", align="c", track=8, alpha=kj, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None, vig_s=0.5)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c15_terazi: zehir hikâyesinin ağırlığı sıtmanın tarafında ═══════════════════════════
def draw_balance(c, x, y, tilt, arm=330.0, a=255):
    """Terazi: (x,y) direk tepesi; tilt (rad, +: sağ kefe aşağı). Dönüş: (sol kefe merkezi, sağ kefe merkezi)."""
    c.drawRect(skia.Rect.MakeLTRB(x - 16, y, x + 16, y + 420), P("#8A6A2A", a))
    c.drawRect(skia.Rect.MakeLTRB(x - 16, y, x + 16, y + 420), S("#3A2A08", 2.4, A(0.9 * a), cap=False))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 150, y + 410, x + 150, y + 452), 10, 10, P("#8A6A2A", a))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - 150, y + 410, x + 150, y + 452), 10, 10, S("#3A2A08", 2.4, A(0.9 * a)))
    xl, yl = x - arm * math.cos(tilt), y - arm * math.sin(-tilt) * -1
    yl = y + arm * math.sin(-tilt)
    xr, yr = x + arm * math.cos(tilt), y + arm * math.sin(tilt)
    c.drawLine(xl, yl, xr, yr, S("#C9A24A", 14, a))
    c.drawLine(xl, yl, xr, yr, S("#F6E2A0", 4, A(0.8 * a)))
    c.drawCircle(x, y, 22, P("#D8B25A", a))
    c.drawCircle(x, y, 22, S("#3A2A08", 2.4, a))
    out = []
    for (xe, ye) in ((xl, yl), (xr, yr)):
        py = ye + 250
        c.drawLine(xe, ye, xe - 120, py, S("#8A6A2A", 3.0, A(0.9 * a)))
        c.drawLine(xe, ye, xe + 120, py, S("#8A6A2A", 3.0, A(0.9 * a)))
        pa = skia.Path()
        pa.moveTo(xe - 130, py)
        pa.quadTo(xe, py + 60, xe + 130, py)
        pa.close()
        c.drawPath(pa, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, py), (0, py + 56)], [C("#F6E2A0", a), C("#B88A3A", a)], [0, 1])))
        c.drawPath(pa, S("#3A2A08", 2.4, A(0.9 * a)))
        out.append((xe, py))
    return out


@CM.ckind("c15_terazi")
def k_terazi(cx, a_in=0.3, a_tilt=4.6, a_dna=1.8, a_cause=3.2, final_at=None, seed=5, ovl=None, **_):
    """Terazi: sol kefede dört yüzyıllık zehir hikâyesi (eski kitap/tomar yığını), sağ kefede sıtma (kehribar ağırlık). Önce ‘DNA: enfeksiyon ✓ / neden ?’ işaretleri,
    sonra terazi yavaşça sıtmaya yatar. «Zehir çürütüldü» YOK; kapanışta «BÜYÜK OLASILIKLA SITMA» levhası."""
    f = cx.f
    cam = CM.Cam(cx, push=0.04, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    k = cx.amt(a_in, 0.8)
    if k > 0.003:
        tilt = math.radians(10.0) * ease_io(clamp((t - cx.at(a_tilt)) / 2.4), 2.0) + math.radians(1.6) * math.sin(t * 1.1) * (1 - ease_io(clamp((t - cx.at(a_tilt)) / 2.4)))
        wood_floor(c, 880, seed=seed)
        (xl, yl), (xr, yr) = draw_balance(c, 960, 240, tilt, 330.0, A(255 * k))
        # sol kefe: eski kitap/tomar yığını
        for i in range(4):
            K14.book_closed(c, xl + (i % 2 - 0.5) * 20, yl - 8 - i * 46, w=200 - i * 14, h=44, col=("#6A2A1E", "#3A4A78", "#7A5A2A", "#4A3A5A")[i], a=A(255 * k), tilt=(i - 1.5) * 0.02)
        # sağ kefe: kehribar ağırlık
        c.drawPath(sk.poly_path([(xr - 70, yr - 6), (xr + 70, yr - 6), (xr + 54, yr - 110), (xr - 54, yr - 110)]), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(xr - 70, 0), (xr + 70, 0)], [C("#F2C46A", A(255 * k)), C("#C8892A", A(255 * k)), C("#8A5A1A", A(255 * k))], [0, 0.5, 1])))
        c.drawPath(sk.poly_path([(xr - 70, yr - 6), (xr + 70, yr - 6), (xr + 54, yr - 110), (xr - 54, yr - 110)]), S("#3A2208", 2.6, A(0.9 * k)))
        for (tx, tt, an_) in (("ZEHİR HİKÂYESİ", (xl, yl + 370), 0.8), ("SITMA", (xr, yr + 370), 0.8)):
            wd = sk.text_width(tx, "title_m", 32, 6) + 70
            CM.tablet(f, tt[0] - wd / 2, tt[1] - 36, wd, 70, alpha=k, corner=8)
            CM.ink(f, tx, tt[0], tt[1] + 10, face="title_m", size=32, color=TH.fg, align="c", track=6, alpha=k, emboss=False)
    kfin = (1.0 - cx.amt(final_at, 0.5)) if final_at is not None else 1.0
    kd = cx.amt(a_dna, 0.6) * kfin
    if kd > 0.003:
        CM.ink(f, "DNA: ENFEKSİYON", 960, 120, face="title_m", size=36, color="#2E6A46", align="c", track=6, alpha=kd, emboss=False)
        pa = skia.Path()
        pa.moveTo(640, 146)
        pa.lineTo(660, 168)
        pa.lineTo(700, 120)
        c.drawPath(pa, S("#2E6A46", 8, A(235 * kd)))
    kc = cx.amt(a_cause, 0.6) * kfin
    if kc > 0.003:
        CM.ink(f, "ÖLÜM NEDENİ: ?", 960, 186, face="title_m", size=36, color="#7A1E16", align="c", track=6, alpha=kc, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None, vig_s=0.5)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c15_ferdinando: 13 yaşında kardinal, rahip olmadı, büyük dük ═══════════════════════════
def draw_galero(c, x, y, s=1.0, a=255, sway=0.0):
    """Kardinal şapkası (galero): geniş kırmızı kenar + alçak tepe + sarkan püsküller (stilize)."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    for sgn in (-1, 1):                                              # püskül sıraları
        for row in range(5):
            for j in range(row + 1):
                tx = sgn * (150 + 10 * row) + (j - row / 2) * 26 + sway * (row + 1) * 1.5
                ty = 40 + row * 30
                c.drawLine(sgn * 150, 20, tx, ty, S("#5A1210", 1.6, A(0.9 * a)))
                c.drawCircle(tx, ty + 6, 8, P("#B3201A", a))
    c.drawOval(skia.Rect.MakeLTRB(-200, -30, 200, 40), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -30), (0, 40)], [C("#C9301F", a), C("#8A1A12", a)], [0, 1])))
    c.drawOval(skia.Rect.MakeLTRB(-200, -30, 200, 40), S("#3A0A06", 3.0, A(0.9 * a)))
    c.drawPath(sk.poly_path([(-90, -20), (-80, -90), (-40, -126), (40, -126), (80, -90), (90, -20)]), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -126), (0, -20)], [C("#D8402A", a), C("#A42218", a)], [0, 1])))
    c.drawPath(sk.poly_path([(-90, -20), (-80, -90), (-40, -126), (40, -126), (80, -90), (90, -20)]), S("#3A0A06", 3.0, A(0.9 * a)))
    c.drawOval(skia.Rect.MakeLTRB(-40, -140, 40, -112), P("#D8402A", a))
    c.restore()


@CM.ckind("c15_ferdinando")
def k_ferdinando(cx, hat_at=0.3, n_at=1.2, monk_at=3.4, x_at=4.4, crown_at=6.6, seed=4, ovl=None, **_):
    """Kırmızı kardinal şapkası + altın «13»; sonra «rahip» (kukuletalı simge) kırmızı ✕ ile geçilir (hiçbir zaman rahip olmadı); sonunda şapka solar, altın taç gelir (büyük dük)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.05, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    kh = cx.amt(hat_at, 0.9, ease=lambda u: ease_out(u, 3))
    kc = cx.amt(crown_at, 0.8)
    if kh > 0.003 and kc < 0.999:
        draw_galero(c, 620, 560 + (1 - kh) * 80 - 40 * kc, 1.45 * (1 - 0.25 * kc), A(255 * kh * (1 - kc)), sway=math.sin(t * 1.4) * 2)
    kn = cx.amt(n_at, 0.5, ease=lambda u: ease_out(u, 3))
    if kn > 0.003:
        sp = CM.gilt("13", "title", 230, 6.0)
        CM.draw_spr(f, sp, 1200, 480, "c", alpha=kn * (1 - 0.7 * kc), scale=1.0 + 0.25 * (1 - kn), glow=0.3)
        CM.ink(f, "YAŞINDA", 1200, 580, face="title_m", size=44, color=TH.fg2, align="c", track=12, alpha=kn * (1 - 0.7 * kc), emboss=False)
    km = cx.amt(monk_at, 0.6, ease=lambda u: ease_out(u, 3))
    if km > 0.003:
        icons.draw_icon(f, "monk", 1560, 540, size=240 * (0.8 + 0.2 * km), metal="gold", alpha=km * (1 - kc), glow=0.0)
        kx = ease_out(clamp((t - cx.at(x_at)) / 0.4), 2)
        if kx > 0:
            c.drawLine(1440, 430, 1440 + 240 * kx, 430 + 240 * kx, S("#A8321E", 20, A(240 * (1 - kc))))
            c.drawLine(1680, 430, 1680 - 240 * kx, 430 + 240 * kx, S("#A8321E", 20, A(240 * (1 - kc))))
    if kc > 0.003:
        f.circle(960, 520, 420, shader=f.rad(960, 520, 420, [("#F7DF8E", 0.0, int(120 * kc)), ("#F7DF8E", 1.0, 0)]))
        icons.draw_icon(f, "crown", 960, 520 + (1 - kc) * 40, size=420 * (0.7 + 0.3 * ease_out(kc, 3)), metal="gold", alpha=kc, glow=0.35 * kc)
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None, vig_s=0.5)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c15_livornina: ilan + üç vaat ═══════════════════════════
@CM.ckind("c15_livornina")
def k_livornina(cx, unroll_at=0.2, seal_at=3.0, d_at=4.0, af_at=5.2, v_at=6.2, seed=6, ovl=None, **_):
    """1593 ilanı: tomar açılır (satırlar yazılır, metin okunmaz), palle mührü basılır; sağda üç vaat simgesi sırayla: dinî özgürlük (açık kitap), af (zincir kırılır), Toskana vatandaşlığı (kalkan+palle)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.05, drift=(2.0, 1.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    pw, ph = 700, 700
    pcx, pcy = 560.0, 520.0
    pp = PP.paper_image(pw, ph, seed, (236, 226, 196), "deckle", (("h", 0.5),), 44, 1.1)
    k_un = ease_out(clamp((t - cx.at(unroll_at)) / 1.2), 2.4)
    vis = max(8.0, ph * k_un)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, pcy - ph / 2 - 60, W, pcy - ph / 2 + vis))
    pp.draw(f, pcx, pcy, rot=-0.01, scale=1.0, alpha=1.0, shadow=0.6)
    for i in range(10):
        kk = clamp((t - cx.at(unroll_at) - 0.5 - i * 0.2) / 0.6)
        scribble_line(c, pcx - pw / 2 + 70, pcx + pw / 2 - 70, pcy - ph / 2 + 100 + i * 50, kk, seed=30 + i, a=210)
    c.restore()
    if k_un < 0.999:
        ey = pcy - ph / 2 + vis
        c.drawRoundRect(skia.Rect.MakeLTRB(pcx - pw / 2 - 10, ey - 8, pcx + pw / 2 + 10, ey + 40), 22, 22,
                        skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, ey - 8), (0, ey + 40)], [C("#B49A66"), C("#EADFC0"), C("#8A7344")], [0, 0.45, 1])))
    CM.wax_seal(f, pcx + 200, pcy + ph / 2 - 100, 66, "#A52A1C", alpha=1.0, t=clamp((t - cx.at(seal_at)) / 0.4), palle=True)
    # üç vaat
    items = [(1170.0, d_at, "book_open", "DİNÎ ÖZGÜRLÜK"), (1430.0, af_at, "chains", "AF"), (1690.0, v_at, "shield", "TOSKANA VATANDAŞLIĞI")]
    for i, (xx, an, ic, lab) in enumerate(items):
        k = cx.amt(an, 0.6, ease=lambda u: ease_out(u, 3))
        if k <= 0.003:
            continue
        yy = 470
        f.circle(xx, yy, 120, color="#000000", alpha=0.18 * k, blur=8)
        c.drawCircle(xx, yy, 104, P("#2A1A0E", A(150 * k)))
        c.drawCircle(xx, yy, 104, S("#C9A24A", 4.0, A(255 * k)))
        icons.draw_icon(f, ic, xx, yy, size=150 * (0.75 + 0.25 * k), metal="gold", alpha=k, glow=0.0)
        if ic == "shield":
            palle_mark(c, xx, yy + 4, 70, A(255 * k), "#B33620")
        if ic == "chains":
            kb = clamp((t - cx.at(an) - 0.5) / 0.4)
            if kb > 0:
                c.drawLine(xx - 40, yy + 40, xx + 40, yy - 40, S("#2A1A0E", 12 * kb, A(255 * kb)))
        wd = min(250, sk.text_width(lab, "title_m", 22, 3) + 40)
        CM.ink(f, lab, xx, yy + 150, face="title_m", size=22, color=TH.fg, align="c", track=3, alpha=k, emboss=False) if len(lab) < 16 else (
            CM.ink(f, "TOSKANA", xx, yy + 150, face="title_m", size=24, color=TH.fg, align="c", track=4, alpha=k, emboss=False),
            CM.ink(f, "VATANDAŞLIĞI", xx, yy + 182, face="title_m", size=24, color=TH.fg, align="c", track=4, alpha=k, emboss=False))
    cam.end(f)
    CM.finish(f, cx, motes_n=22, light=None, vig_s=0.5)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c15_ruspanti: 379 adam, adını paradan alan çevre ═══════════════════════════
def pictogram(c, x, y, s=1.0, col="#2A1A0E", a=255):
    c.drawCircle(x, y - 17 * s, 6.5 * s, P(col, a))
    c.drawPath(sk.poly_path([(x - 4 * s, y - 9 * s), (x + 4 * s, y - 9 * s), (x + 9 * s, y + 13 * s), (x - 9 * s, y + 13 * s)]), P(col, a))


@CM.ckind("c15_ruspanti")
def k_ruspanti(cx, count_at=0.6, count_dur=2.4, coin_at=5.6, n=379, cols=21, seed=3, ovl=None, **_):
    """Küçük insan piktogramlarından ızgara: 0→379 dolar (sayaç), sonra her figürün başında altın sikke belirir (adlarını altın sikkeden = «ruspi»). Sağda altın sayaç + «RUSPANTİ»."""
    f = cx.f
    cam = CM.Cam(cx, push=0.05, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    kc = ease_out(clamp((t - cx.at(count_at)) / count_dur), 2.2)
    shown = int(round(n * kc))
    gx, gy, dx, dy = 140.0, 190.0, 38.0, 44.0
    rows = int(math.ceil(n / cols))
    tc = cx.at(coin_at)
    for i in range(n):
        if i >= shown:
            break
        r_, c_ = divmod(i, cols)
        x = gx + c_ * dx + (dx / 2 if r_ % 2 else 0)
        y = gy + r_ * dy
        pop = clamp((kc * n - i) / 6.0)
        pictogram(c, x, y, 0.9 + 0.1 * pop, "#2A1A0E", A(255 * min(1.0, pop * 2)))
        ti = tc + i * 0.0045
        kk = clamp((t - ti) / 0.25)
        if kk > 0:
            yy = y - 36 - (1 - ease_out(kk, 3)) * 18
            c.drawCircle(x, yy, 6.4, P("#E0B040", A(255 * kk)))
            c.drawCircle(x, yy, 6.4, S("#6A4A12", 1.2, A(220 * kk)))
    if shown > 0:
        sp = CM.gilt(str(shown), "title", 230, 6.0)
        CM.draw_spr(f, sp, 1480, 470, "c", alpha=1.0, glow=0.25)
        CM.ink(f, "RUSPANTİ", 1480, 590, face="title_m", size=50, color=TH.acc, align="c", track=14, alpha=cx.amt(count_at, 0.5, off=0.8), emboss=False)
    kk = cx.amt(coin_at, 0.6)
    if kk > 0.003:
        L.coin_flat(c, 1250, 760, r=30)
        CM.ink(f, "RUSPİ = ALTIN SİKKE", 1530, 774, face="title_m", size=30, color=TH.fg, align="c", track=5, alpha=kk, emboss=False)
    cam.end(f)
    CM.finish(f, cx, motes_n=20, light=None, vig_s=0.5)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c15_sektor: yün geriledi, ipek gelişti ═══════════════════════════
def wool_bale(c, x, y, w=150, h=96, a=255):
    c.drawRoundRect(skia.Rect.MakeLTRB(x - w / 2, y - h, x + w / 2, y), 14, 14, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, y - h), (0, y)], [C("#F0E6CC", a), C("#C9B88E", a)], [0, 1])))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - w / 2, y - h, x + w / 2, y), 14, 14, S("#5A4A2A", 2.4, A(0.9 * a)))
    for fx in (-w * 0.2, w * 0.2):
        c.drawLine(x + fx, y - h, x + fx, y, S("#6A4A22", 4, A(0.9 * a)))
    c.drawLine(x - w / 2, y - h * 0.5, x + w / 2, y - h * 0.5, S("#6A4A22", 4, A(0.9 * a)))


def silk_bolt(c, x, y, w=170, h=52, col="#A8321E", a=255):
    c.drawRoundRect(skia.Rect.MakeLTRB(x - w / 2, y - h, x + w / 2, y), h / 2, h / 2, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, y - h), (0, y)], [C(mix(col, "#FFFFFF", 0.4), a), C(col, a), C(mix(col, "#000000", 0.4), a)], [0, 0.5, 1])))
    c.drawRoundRect(skia.Rect.MakeLTRB(x - w / 2, y - h, x + w / 2, y), h / 2, h / 2, S("#2A1A0E", 2.0, A(0.9 * a)))
    c.drawCircle(x + w / 2 - h / 2, y - h / 2, h * 0.28, S(mix(col, "#000000", 0.5), 2.0, A(0.8 * a)))


@CM.ckind("c15_sektor")
def k_sektor(cx, years_at=0.2, decl_at=2.6, yun_at=6.8, ipek_at=8.4, seed=4, ovl=None, **_):
    """Üstte «53 YIL»; büyük gri «gerileme» oku iner; sonra iki sütun: YÜN (denk yığını azalır, ok aşağı) ve İPEK (top kumaş yığını artar, ok yukarı). Sektörel nüans (tek hat değil)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.05, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress="both")
    cam.begin(f)
    c = f.c
    t = cx.t
    ky = cx.amt(years_at, 0.7)
    if ky > 0.003:
        sp = CM.gilt("53 YIL", "title", 130, 8.0)
        CM.draw_spr(f, sp, 960, 210, "c", alpha=ky, glow=0.2)
    kd = ease_out(clamp((t - cx.at(decl_at)) / 1.4), 2.0)
    split = cx.amt(yun_at, 0.8)
    if kd > 0.003:
        al = 1.0 - 0.8 * split
        x0, x1 = 460, 1460
        y0, y1 = 330, 330 + 150 * kd
        pa = skia.Path()
        pa.moveTo(x0, y0)
        pa.lineTo(x0 + (x1 - x0) * kd, y0 + (y1 - y0))
        c.drawPath(pa, S("#6A6A72", 22, A(220 * al)))
        if kd > 0.8:
            c.drawPath(sk.poly_path([(x1 - 40, y1 + 40), (x1 + 40, y1 + 40), (x1, y1 + 90)]), P("#6A6A72", A(220 * al)))
        CM.ink(f, "GERİLEME", 960, 296, face="title_m", size=40, color="#4A4A52", align="c", track=12, alpha=kd * al, emboss=False)
    base = 860
    c.drawRect(skia.Rect.MakeLTRB(160, base, 1760, base + 14), P("#4A2E16", 220))
    c.drawLine(960, 380, 960, base, S("#7A5C32", 2.0, A(150 * split)))
    # YÜN: azalan yığın
    ky_ = cx.amt(yun_at, 0.6)
    if ky_ > 0.003:
        nw = int(round(lerp(6.0, 2.0, ease_io(clamp((t - cx.at(yun_at) - 0.4) / 1.4), 2.0))))
        for i in range(nw):
            wool_bale(c, 560 + (i % 2 - 0.5) * 30, base - i * 100, 190, 94, A(255 * ky_))
        CM.ink(f, "YÜN", 560, base + 70, face="title_m", size=44, color=TH.fg, align="c", track=12, alpha=ky_, emboss=False)
        ka = ease_out(clamp((t - cx.at(yun_at) - 0.3) / 0.7), 2)
        if ka > 0:
            c.drawLine(380, 420, 380, 420 + 160 * ka, S("#A8321E", 18, A(235 * ka)))
            c.drawPath(sk.poly_path([(340, 580 * 1), (420, 580), (380, 640)]) if False else sk.poly_path([(340, 420 + 150 * ka), (420, 420 + 150 * ka), (380, 420 + 200 * ka)]), P("#A8321E", A(235 * ka)))
    # İPEK: artan yığın
    kp = cx.amt(ipek_at, 0.6)
    if kp > 0.003:
        ns = int(round(lerp(2.0, 7.0, ease_io(clamp((t - cx.at(ipek_at) - 0.4) / 1.6), 2.0))))
        cols_ = ("#A8321E", "#233C8C", "#C79A3C", "#2E6A46", "#8E3342", "#2F6A93", "#B33620")
        for i in range(ns):
            silk_bolt(c, 1360 + (i % 2 - 0.5) * 24, base - i * 62, 230, 56, cols_[i % len(cols_)], A(255 * kp))
        CM.ink(f, "İPEK", 1360, base + 70, face="title_m", size=44, color=TH.fg, align="c", track=12, alpha=kp, emboss=False)
        ka = ease_out(clamp((t - cx.at(ipek_at) - 0.3) / 0.7), 2)
        if ka > 0:
            c.drawLine(1620, 580, 1620, 580 - 160 * ka, S("#2E6A46", 18, A(235 * ka)))
            c.drawPath(sk.poly_path([(1580, 580 - 150 * ka), (1660, 580 - 150 * ka), (1620, 580 - 200 * ka)]), P("#2E6A46", A(235 * ka)))
    cam.end(f)
    CM.finish(f, cx, motes_n=20, light=None, vig_s=0.5)
    if ovl is not None:
        ovl(cx)


# ═══════════════════════════ c15_hat: erkek hat kapandı; bir kadın ve imzalanacak bir sözleşme ═══════════════════════════
@CM.ckind("c15_hat")
def k_hat(cx, lit_at=0.0, out_at=1.6, out_dt=0.34, woman_at=3.4, doc_at=4.6, names=("I. FRANCESCO", "I. FERDINANDO", "II. COSIMO", "II. FERDINANDO", "III. COSIMO", "GIAN GASTONE"), seed=3, ovl=None, **_):
    """Toskana'yı yöneten hat: altı isim, her birinin üstünde bir mum. Mumlar tek tek söner (erkek hat kapandı). Sağda tek bir ışık: kadın silueti (yüz yok) ve mühürlü sözleşme tomarı."""
    f = cx.f
    cam = CM.Cam(cx, push=0.04, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    wood_floor(c, 800, seed=seed)
    n = len(names)
    to = cx.at(out_at)
    base_x, step = 300.0, 232.0
    for i, nm in enumerate(names):
        xi = base_x + i * step
        kl = cx.amt(lit_at, 0.8, off=0.1 * i)
        if kl <= 0.003:
            continue
        ti = to + i * out_dt
        lit = (1.0 - ease_in(clamp((t - ti) / 0.8), 1.6)) * kl
        OD.candle(f, xi, 800, 230, t, seed=3 + i * 3, lit=lit, holder=True)
        wd = sk.text_width(nm, "title_m", 19, 1) + 30
        al = kl * (0.45 + 0.55 * (1.0 if t < ti + 0.3 else 0.0))
        CM.tablet(f, xi - wd / 2, 830, wd, 52, alpha=al, corner=8)
        CM.ink(f, nm, xi, 864, face="title_m", size=19, color=TH.fg, align="c", track=1, alpha=al, emboss=False)
    kw = cx.amt(woman_at, 1.0)
    kd = cx.amt(doc_at, 0.8)
    xw = 1750.0
    if kw > 0.003:
        OD.candle(f, xw - 120, 800, 260, t, seed=11, lit=kw, holder=True)
        OD.sil_actor(f, "soylu_f", xw, 800, 400, t, "idle", dir=-1, seed=4, alpha=kw)
    if kd > 0.003:
        c.save()
        c.translate(xw - 280, 640)
        c.drawRoundRect(skia.Rect.MakeLTRB(-60, -90, 60, 90), 12, 12, P("#EFE5CC", A(255 * kd)))
        c.drawRoundRect(skia.Rect.MakeLTRB(-60, -90, 60, 90), 12, 12, S("#5A3E1E", 2.4, A(240 * kd)))
        for r in range(5):
            c.drawLine(-40, -60 + r * 28, 40 - (r % 2) * 14, -60 + r * 28, S("#2A1A0E", 2.2, A(150 * kd)))
        c.restore()
        CM.wax_seal(f, xw - 280, 700, 28, "#A52A1C", alpha=1.0, t=kd, palle=True)
    light = CM.candle_light(t, seed, base=(1000 - 520 * clamp((t - to) / (out_dt * n + 0.8)) + 520 * 0, 560), r=1250.0 - 560 * clamp((t - to) / (out_dt * n + 0.8)), sway=6.0)
    if kw > 0.003:
        light = CM.candle_light(t, seed, base=(1000 + 600 * clamp((t - cx.at(woman_at)) / 1.5), 560), r=760.0, sway=6.0)
    cam.end(f)
    CM.finish(f, cx, motes_n=24, light=light, vig_s=0.6)
    if ovl is not None:
        ovl(cx)



# ═══════════════════════════ c15_cetvel: kırık eksen — 1587 ·····(dört yüzyıl)····· 2006 · 2010 · 2026 ═══════════════════════════
@CM.ckind("c15_cetvel")
def k_cetvel(cx, a0=0.0, a_br=1.0, a06=1.6, a10=3.2, a26=5.4, seed=5, ovl=None, **_):
    """Gece cetveli. Sol uçta 1587 (mum sarısı), ortada KOPUK eksen (dört yüzyıllık boşluk, üstünde ayraç), sağ uçta 2006 · 2010 · 2026 yıl başına 20 px ile açılır.
    Etiketler yalnız script sözcükleri: EKİM 1587, ARSENİK, SITMA ANTİJENİ, SITMA DNA'sı, DÖRT YÜZYIL. DNA katmanı mavi (lapis)."""
    f = cx.f
    cam = CM.Cam(cx, push=0.03, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed % 3, cam=cam, dress=None)
    cam.begin(f)
    c = f.c
    t = cx.t
    y = 580.0
    gold = "#D8B25A"
    k0 = cx.amt(a0, 0.8)

    def X06(yr):
        return 1240.0 + (yr - 2006) * 20.0
    # eksen parçaları
    gl = P(gold, A(255 * k0))
    pl = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5.0, Color=C(gold, A(235 * k0)))
    c.drawLine(160, y, 560, y, pl)
    kb = cx.amt(a_br, 1.2)
    # kopuş işaretleri
    for xb_ in (590.0, 1110.0):
        for dx_ in (-9, 9):
            c.drawLine(xb_ + dx_ - 8, y + 26, xb_ + dx_ + 8, y - 26, S(gold, 3.0, A(220 * k0)))
    dash = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.0, Color=C(gold, A(120 * kb)),
                      PathEffect=skia.DashPathEffect.Make([4, 16], 0.0))
    if kb > 0.003:
        c.drawLine(630, y, 630 + 440 * ease_out(kb), y, dash)
    k6 = cx.amt(a06, 0.8)
    xr1 = 1180.0 + 640.0 * ease_out(clamp((t - cx.at(a06)) / 1.6))
    if k6 > 0.003:
        c.drawLine(1140, y, xr1, y, pl)
        for yr in range(2006, 2031, 5):
            xx = X06(yr)
            if xx <= xr1:
                c.drawLine(xx, y - 11, xx, y + 11, S(gold, 2.4, A(200 * k6)))
    # 1587 işareti (mum sarısı)

    def marker(x, col, k, up, lab, yr, lab_col, stem=130.0):
        if k <= 0.003:
            return
        L_ = stem * ease_out(k)
        c.drawLine(x, y, x, y + up * L_, S(gold, 3.0, A(230 * k)))
        c.drawCircle(x, y, 40 * k, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((x, y), 40 * k + 1, [C(col, A(170 * k)), C(col, 0)], [0, 1])))
        c.drawCircle(x, y, 15 * k, P(col, A(255 * k)))
        c.drawCircle(x, y, 15 * k, S("#2A1A0E", 2.0, A(200 * k)))
        if up > 0:
            ty_y, ty_l = y + stem + 52, y + stem + 106
        else:
            ty_y, ty_l = y - stem - 28, y - stem - 82
        CM.ink(f, str(yr), x, ty_y, face="title", size=50, color=col, align="c", track=4, alpha=k)
        CM.ink(f, lab, x, ty_l, face="cap_b", size=38, color=lab_col, align="c", alpha=k)
    marker(360.0, "#FFD27A", cx.amt(a0, 0.7), 1, "EKİM 1587", 1587, "#F4E9CB")
    ochre, lapis = "#E0A83A", "#78A4F0"
    marker(X06(2006), ochre, cx.amt(a06, 0.6), 1, "ARSENİK", 2006, "#F4E9CB")
    marker(X06(2010), ochre, cx.amt(a10, 0.6), -1, "SITMA ANTİJENİ", 2010, "#F4E9CB")
    marker(X06(2026), lapis, cx.amt(a26, 0.6), 1, "SITMA DNA'sı", 2026, "#F4E9CB")
    # üst ayraç: DÖRT YÜZYIL (1587 → 2006)
    kbr = cx.amt(a06, 1.4)
    if kbr > 0.003:
        xa, xb = 360.0, X06(2006)
        xe = xa + (xb - xa) * ease_out(kbr)
        yb = y - 150.0
        pb = S(gold, 3.2, A(235 * kbr))
        c.drawLine(xa, yb, xe, yb, pb)
        c.drawLine(xa, yb, xa, yb + 34, pb)
        if kbr > 0.97:
            c.drawLine(xb, yb, xb, yb + 34, pb)
        ka2 = clamp((kbr - 0.35) / 0.5)
        CM.ink(f, "DÖRT YÜZYIL", (xa + xb) / 2, yb - 40, face="title", size=64, color="#EDB968", align="c", track=10, alpha=ka2)
    light = CM.candle_light(t, seed, base=(900, 620), r=1100.0, sway=5.0)
    cam.end(f)
    CM.finish(f, cx, motes_n=20, light=light, vig_s=0.55)
    if ovl is not None:
        ovl(cx)


def pie_ov(x, y, at, out=None):
    def fn(cx):
        k = L._kk(cx, at, 0.6, out, 0.5)
        if k > 0.003:
            pie(cx.f.c, x, y - (1 - k) * 20, r=70 * (0.8 + 0.2 * k), a=A(255 * k))
    return fn
