"""Bölüm 8 (Akdeniz'de Barbaros) özel çekim türleri. Ad önteki: c8_*"""
import math

import numpy as np
import skia

import icons
import shots as SH
import sk
import stage as ST
import stage_c678 as X
from sk import C, H, back_out, clamp, ease_in, ease_io, ease_out, lerp, mix, seg, smooth
from sk import W as SW

CX = SW / 2
SEA_L = "#27455C"
TURQ = "#2F7A8A"


# ───────────────────────────── c8_zafer: Habsburg çevresinde kutlama ─────────────────────────────
_SUN = {}


def _sunburst():
    if "img" not in _SUN:
        S = 2800
        s = skia.Surface(S, S)
        c = s.getCanvas()
        c.clear(skia.ColorTRANSPARENT)
        n = 22
        for i in range(n):
            a0 = 2 * math.pi * i / n
            a1 = a0 + math.pi / n * 0.9
            p = skia.Path()
            p.moveTo(S / 2, S / 2)
            p.lineTo(S / 2 + math.cos(a0) * S, S / 2 + math.sin(a0) * S)
            p.lineTo(S / 2 + math.cos(a1) * S, S / 2 + math.sin(a1) * S)
            p.close()
            sh = skia.GradientShader.MakeRadial((S / 2, S / 2), S * 0.5, [C("#FFE2A0", 120), C("#FFE2A0", 0)], [0.05, 1.0])
            c.drawPath(p, skia.Paint(AntiAlias=True, Shader=sh))
        _SUN["img"] = s.makeImageSnapshot()
    return _SUN["img"]


@SH.kind("c8_zafer")
def k_zafer(cx, at_kick=0.0, at_word=0.0, at_laurel=0.0):
    """Tunus zaferi: dönen güneş ışınları, defne, sallanan Habsburg sancakları, kıvılcımlar."""
    f = cx.f
    f.bg("night")
    X.tone(f, "#C9962B", 0.16, cy=0.5)
    a = cx.amt(at_laurel, 0.8)
    img = _sunburst()
    f.c.save()
    f.c.translate(CX, 520)
    f.c.rotate(cx.t * 3.0)
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(0.55 * a)
    p.setBlendMode(skia.BlendMode.kPlus)
    f.c.drawImage(img, -1400, -1400, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    f.c.restore()
    # sancaklar (sol/sağ), üstten sallanır
    for i, (bx, col, ic_) in enumerate(((330, "#7B1B22", "eagle"), (1590, "#7B1B22", "eagle"), (130, "#6B1D24", "castle"), (1790, "#6B1D24", "castle"))):
        k = cx.amt(at_kick, 0.8, off=0.15 * i)
        if k <= 0:
            continue
        f.c.save()
        f.c.translate(bx, -40)
        f.c.rotate(math.sin(cx.t * 1.6 + i * 1.3) * 2.2)
        f.c.translate(-bx, 40)
        ST.banner(f, bx, -40 - (1 - ease_out(k)) * 420, 150, 520, color=col, icon=ic_, wave=math.sin(cx.t * 2 + i) * 2)
        f.c.restore()
    # çanlar (tepeden sallanır)
    if X.has_icon("bell"):
        kb = cx.amt(at_kick, 0.8, off=0.3)
        for i, bx in enumerate((470, 1450)):
            if kb <= 0:
                continue
            f.c.save()
            f.c.translate(bx, 40)
            f.c.rotate(math.sin(cx.t * 3.2 + i * 1.7) * 11)
            f.line(0, 0, 0, 90, color="#7A5518", sw=5, alpha=kb)
            X.ic(f, "bell", 0, 170, size=190 * kb, metal="gold", alpha=kb, glow=0.25 * kb)
            f.c.restore()
    X.ic(f, "laurel", CX, 470 + math.sin(cx.t * 1.1) * 6, size=430 * (0.85 + 0.15 * back_out(a)), metal="gold", alpha=a, glow=0.45 * a)
    kw = cx.amt(at_word, 0.6)
    if kw > 0:
        SH.gold_flat(f, "ZAFER", CX, 830, face="title", size=130, track=18, alpha=kw)
    kk = cx.amt(at_kick, 0.7)
    if kk > 0:
        SH.kicker(f, "HABSBURG ÇEVRESİNDE", CX, 170, alpha=kk, size=34, track=14, face="title_m", color="#E0C682")
    sk.embers(f, cx.t, n=70, seed=3, color="#FFD27A")
    sk.dust(f, cx.t, n=60, alpha=0.6)
    f.vig(0.58)


# ───────────────────────────── c8_konsey: boş sandalyeli savaş konseyi ─────────────────────────────
def _chair(f, x, y, w=130, h=330, col="#2B1A0F", trim="#8A6338"):
    """Yüksek arkalıklı sandalye (arka duvara karşı)."""
    top = y - h
    f.path(ST.pointed_arch_path(x, y, w, h), shader=f.lin(x - w / 2, top, x + w / 2, y, [(mix(col, "#FFFFFF", 0.10), 0.0), (col, 0.6), (mix(col, "#000000", 0.4), 1.0)]))
    f.path(ST.pointed_arch_path(x, y, w, h), style="stroke", sw=3, color=trim, alpha=0.8)
    f.path(ST.pointed_arch_path(x, y, w * 0.62, h * 0.8), style="stroke", sw=2, color=trim, alpha=0.4)


def _council_back(f):
    # duvar + zemin
    f.rect(0, 0, SW, H, shader=f.lin(0, 0, 0, H, [("#2E1D12", 0.0), ("#150D08", 0.7), ("#0B0705", 1.0)]))
    for r in range(8):
        f.line(0, 40 + r * 90, SW, 40 + r * 90, color="#000000", sw=1.6, alpha=0.25)
    # arka duvarda büyük harita levhası (gravür)
    f.rrect(560, 90, 800, 360, 10, color="#C9B27A", alpha=0.20)
    f.rrect(560, 90, 800, 360, 10, style="stroke", sw=4, color="#8A6338", alpha=0.7)
    rs = np.random.RandomState(4)
    for i in range(26):
        x = 600 + rs.rand() * 720
        y = 120 + rs.rand() * 300
        f.line(x, y, x + 20 + rs.rand() * 80, y + (rs.rand() - 0.5) * 30, color="#5A3E1E", sw=1.4, alpha=0.35)
    # sandalyeler + oturanlar
    xs = [830, 1010, 1190, 1370, 1550]
    kinds = ["noble", "cardinal", "merchant", "noble", "scribe"]
    for i, x in enumerate(xs):
        _chair(f, x, 700, 160, 400)
    for i, (x, kd) in enumerate(zip(xs, kinds)):
        ST.figure(f, kd, x, 760, 540, col="#0B0705", rim="#C58A44", face=1 if x < 1190 else -1)
    # boş sandalye (sol uç)
    _chair(f, 590, 740, 170, 440, col="#33200F", trim="#B88A3A")
    # masa
    f.path(sk.poly_path([(430, 690), (1820, 690), (1930, 790), (330, 790)]), shader=f.lin(0, 690, 0, 790, [("#5A3A22", 0.0), ("#3A2415", 1.0)]))
    f.rect(330, 790, 1600, 78, shader=f.lin(0, 790, 0, 868, [("#2C1A0F", 0.0), ("#120A06", 1.0)]))
    f.line(330, 790, 1930, 790, color="#C9962B", sw=3, alpha=0.7)
    f.line(430, 690, 1820, 690, color="#E3B54A", sw=2, alpha=0.35)
    # masa üstünde harita
    f.path(sk.poly_path([(900, 708), (1480, 708), (1540, 772), (840, 772)]), shader=f.lin(0, 708, 0, 772, [("#DCCB9E", 0.0), ("#B9A474", 1.0)]))
    f.line(960, 726, 1420, 726, color="#5A3E1E", sw=1.5, alpha=0.5)
    f.line(930, 742, 1450, 742, color="#5A3E1E", sw=1.5, alpha=0.5)
    f.circle(1230, 744, 6, color="#B02A2A")
    # mumluklar
    for x in (740, 1640):
        f.rect(x - 6, 650, 12, 52, color="#EADCB5")
        f.rect(x - 16, 700, 32, 8, color="#8A6338")
    # sıcak ışık
    f.circle(1190, 640, 760, shader=f.rad(1190, 640, 760, [("#FFB347", 0.0, 70), ("#FF8A33", 0.5, 26), ("#FF8A33", 1.0, 0)]), blend=skia.BlendMode.kPlus)
    # sol: boş sandalyeye ışık huzmesi
    f.path(sk.poly_path([(540, 0), (640, 0), (800, 790), (400, 790)]), shader=f.lin(0, 0, 0, 790, [("#FFE2A0", 0.0, 8), ("#FFE2A0", 1.0, 52)]), blend=skia.BlendMode.kPlus)


@SH.kind("c8_konsey")
@X.pushy(0.03)
def k_konsey(cx, at_scene=0.0, at_kort=0.0, at_kick=0.0, at_chip=0.0, at_stamp=0.0, key="kortes"):
    """Savaş konseyi masası: oturanlar, BOŞ sandalye, kapıda Cortés; ANLATILIR damgası."""
    f = cx.f
    f.c.drawImage(sk.baked(("c8_council",), _council_back), 0, 0)
    a = cx.amt(at_scene, 0.8)
    if a < 1:
        f.rect(0, 0, SW, H, color="#000000", alpha=1 - a)
    # mum alevleri
    for i, x in enumerate((740, 1640)):
        fl = 0.8 + 0.2 * math.sin(cx.t * 9 + i * 2.1)
        f.circle(x, 636, 42 * fl, shader=f.rad(x, 636, 42 * fl, [("#FFD58A", 0.0, 150), ("#FFB347", 0.4, 60), ("#FFB347", 1.0, 0)]), blend=skia.BlendMode.kPlus)
        f.oval(x, 636, 4.5 * fl, 11 * fl, color="#FFF1C2")
    # Cortés (kapıda, ışık dışında)
    km = cx.amt(at_kort, 0.9)
    if km > 0:
        mx, my = 290, 540
        f.circle(mx, my, 250, shader=f.rad(mx, my, 250, [("#000000", 0.0, int(150 * km)), ("#000000", 1.0, 0)]))
        SH.draw_medal(f, key, mx, my + (1 - km) * 26, 360 * (0.92 + 0.08 * ease_out(km)), "bronze", False, alpha=km * 0.95, tilt=0.14 * math.sin(cx.t * 0.55))
        X.name_plate2(f, "HERNÁN CORTÉS", "Meksika'nın fatihi", mx + 30, H * 0.80, size=40, t=cx.amt(at_kort, 0.6, off=0.3), minw=460)
        # kesikli çizgi: medalden boş sandalyeye
        ka = ease_out(clamp((cx.t - cx.at(at_chip)) / 1.0))
        if ka > 0:
            p = f.paint("#E3B54A", style="stroke", sw=4, alpha=0.8 * ka)
            p.setPathEffect(skia.DashPathEffect.Make([12, 12], -cx.t * 24))
            f.c.drawLine(mx + 190, my - 20, lerp(mx + 190, 560, ka), lerp(my - 20, 560, ka), p)
    kk = cx.amt(at_kick, 0.7)
    if kk > 0:
        SH.kicker(f, "SAVAŞ KONSEYİ", CX + 150, 150, alpha=kk, size=34, track=14, face="title_m", color="#E0C682")
    kc = cx.amt(at_chip, 0.5)
    if kc > 0:
        X.chip(f, "KONSEYE ÇAĞRILMADI", 1190, 900, k=kc, size=36, edge="#B02A2A", color="#F8E2D8", padx=40, h=90)
    t = cx.amt(at_stamp, 0.3)
    if t > 0:
        SH.stamp(f, "ANLATILIR", 1500, 960, rot=-0.07, size=62, t=t)
    f.vig(0.62)
