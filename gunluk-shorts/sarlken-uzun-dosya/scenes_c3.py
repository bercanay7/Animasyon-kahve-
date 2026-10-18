"""Bölüm 3 — Şehirlerin İsyanı (1520–1522). Ton: kan kırmızısı, gri yağmur."""
import math

import icons
import kit_a as K
import scenes_lib  # theatre şablonunu kaydeder
import scenes_field as SF  # sahne-lab: savaş alanı (Villalar)
import scenes_siege as SG  # sahne-lab: kuşatma (Toledo)
import shots as SH
import shots_c3  # noqa: F401  (c3_bayram + c3_sokak sahnesi)
import sk
import stage as ST
from shots import shot
from sk import H, W, clamp, ease_out, lerp, smooth, back_out

AACHEN = (6.08, 50.78)
VILLALAR = (-5.10, 41.70)
VALENCIA = (-0.38, 39.47)
CASTILE_CITIES = [(-4.12, 40.95), (-4.70, 40.66), (-5.66, 40.97), (-4.72, 41.65), (-3.70, 42.34), (-5.57, 42.60), (-5.74, 41.50), (-4.53, 42.01),
                  (-2.47, 41.76), (-3.17, 40.63), (-4.02, 39.86), (-3.70, 40.42), (-2.13, 40.07), (-3.93, 38.98)]
THRONES = [("kastilya", (-4.5, 40.0)), ("aragon", (-0.5, 41.8)), ("burgonya", (4.6, 51.0)), ("avusturya", (14.0, 47.6))]
ROTA_DENIZ = [(-8.3, 43.45), (-7.0, 46.0), (-3.5, 49.0), (0.5, 50.8), (3.6, 51.7)]
ROTA_KARA = [(3.6, 51.7), (5.0, 51.2), AACHEN]


def _rain(cx, a=0.2):
    sk.rain(cx.f, cx.t, n=170, alpha=a, color="#B8C4CC")


# ───────────────────────────── harita kaplamaları ─────────────────────────────
def _ex_rota(cx, cm, mv):
    f = cx.f
    _rain(cx, 0.16)
    ba = cx.amt(("c3s1", "Tacı", -0.1), 0.7)
    x, y = cm.ll(*AACHEN)
    K.beacon(f, x, y, cx.t, amt=ba, color="#F0D27A", r=16)
    icons.draw_icon(f, "imperial_crown", x, y - 96, size=104, metal="gold", alpha=ba, glow=0.4 * ba)
    K.tag(f, "AACHEN", x + 40, y + 18, alpha=ba, size=38, align="l", pad=22)


def _card(f, x, y, w, h, a):
    SH.plate(f, x, y, w, h, alpha=0.92 * a, fill="#1A0B0B", edge="#C0392B", corner=18)


def _ex_tepki(cx, cm, mv):
    f = cx.f
    t = cx.t
    _rain(cx, 0.22)
    # öfke nedenleri: iki kart
    ya = cx.amt(("c3s2", "yabancı", -0.1), 0.6)
    if ya > 0:
        x, y, w, h = 40, 300 - 14 * (1 - ya), 360, 360
        _card(f, x, y, w, h, ya)
        for i, (kind, dx, hh) in enumerate((("noble", -92, 150), ("page", 0, 130), ("merchant", 92, 150))):
            K.fig(f, kind, x + w / 2 + dx, y + 200, hh, col="#0A0504", rim="#D9A05A", face=1 if i != 1 else -1, alpha=ya)
        K.txt(f, "YABANCI", x + w / 2, y + 262, face="title_m", size=34, color="#F3DE9A", track=8, alpha=ya)
        K.txt(f, "DANIŞMANLAR", x + w / 2, y + 308, face="title_m", size=34, color="#F3DE9A", track=8, alpha=ya)
    va = cx.amt(("c3s2", "vergilere", -0.1), 0.6)
    if va > 0:
        x, y, w, h = W - 400, 300 - 14 * (1 - va), 360, 360
        _card(f, x, y, w, h, va)
        icons.draw_icon(f, "coins", x + w / 2, y + 140, size=200 * (0.85 + 0.15 * back_out(va)), metal="gold", alpha=va, glow=0.25 * va)
        K.txt(f, "VERGİ", x + w / 2, y + 296, face="title", size=56, color="#F3DE9A", track=12, alpha=va)
    # şehirler kızarır (isimsiz)
    t0 = cx.at(("c3s2", "Kastilya", -0.1))
    for i, (lo, la) in enumerate(CASTILE_CITIES):
        a = smooth(clamp((t - t0 - i * 0.1) / 0.4))
        if a > 0:
            x, y = cm.ll(lo, la)
            K.beacon(f, x, y, t + i * 0.3, amt=a, color="#E0483A", r=11, rings=2, period=1.6)
    # tepki: yumruk + kızıl şok halkaları
    t1 = cx.at(("c3s2", "tepkiyle", -0.1))
    ka = smooth((t - t1) / 0.5)
    if ka > 0:
        x, y = cm.ll(-4.2, 40.9)
        for i in range(3):
            ph = clamp((t - t1 - i * 0.28) / 1.4)
            if 0 < ph < 1:
                f.circle(x, y, 60 + ph * 520, style="stroke", sw=5, color="#E0483A", alpha=(1 - ph) ** 1.4 * 0.75)
        K.glow_disc(f, x, y, 200, "#E0483A", 0.4 * ka)
        icons.draw_icon(f, "fist", x, y, size=230 * (0.8 + 0.2 * back_out(ka)), metal="crimson", alpha=ka, glow=0.4 * ka)


def _ex_villalar(cx, cm, mv):
    f = cx.f
    _rain(cx, 0.24)
    a = cx.amt(("c3s4", "Villalar'da,", -0.25), 0.6)
    if a > 0:
        x, y = cm.ll(*VILLALAR)
        K.beacon(f, x, y, cx.t, amt=a, color="#E0483A", r=17)
        K.tag(f, "VILLALAR", x + 42, y + 18, alpha=a, size=42, align="l", pad=24)


def _ex_valensiya(cx, cm, mv):
    f = cx.f
    _rain(cx, 0.2)
    a = cx.amt(("c3s7", "Valensiya'da", -0.15), 0.6)
    if a > 0:
        x, y = cm.ll(*VALENCIA)
        K.beacon(f, x, y, cx.t, amt=a, color="#E0483A", r=17)
        K.tag(f, "VALENSİYA", x + 42, y + 18, alpha=a, size=42, align="l", pad=24)
    ea = cx.amt(("c3s7", "esnaf", -0.1), 0.6)
    if ea > 0:
        K.tag(f, "ESNAF LONCALARI", W / 2, 985, alpha=ea, size=44, pad=36)
    ga = cx.amt(("c3s7", "Germanía", -0.15), 0.6)
    if ga > 0:
        f.rect(0, 720, W, 280, shader=f.lin(0, 720, 0, 1000, [("#000000", 0.0, 0), ("#000000", 1.0, int(150 * ga))]))
        SH.gold_flat(f, "GERMANÍA", W / 2, 905 + 8 * (1 - ga), face="title", size=int(110 * (0.9 + 0.1 * back_out(ga))), track=18, alpha=ga)


def _ex_cyl(cx, cm, mv):
    f = cx.f
    _rain(cx, 0.14)
    ba = cx.amt(("c3s8", "Bugün", -0.1), 0.6)
    K.tag(f, "BUGÜN", W / 2, 150, alpha=ba, size=44, pad=36)


def _ex_tahtlar(cx, cm, mv):
    f = cx.f
    t = cx.t
    _rain(cx, 0.14)
    t0 = cx.at(("c3s9", "aynı", -0.1))
    pos = {}
    for i, (nm, ll) in enumerate(THRONES):
        a = smooth(clamp((t - t0 - i * 0.28) / 0.5))
        x, y = cm.ll(*ll)
        pos[nm] = (x, y)
        if a <= 0:
            continue
        K.glow_disc(f, x, y, 96, "#F0D27A", 0.4 * a)
        icons.draw_icon(f, "crown", x, y, size=100 * (0.8 + 0.2 * back_out(a)), metal="gold", alpha=a, glow=0.3 * a)
    # Şarlken yalnız Kastilya'da
    ka = cx.amt(("c3s9", "başında", -0.15), 0.6)
    kx, ky = pos["kastilya"]
    t_x = cx.at(("c3s9", "duramazsın", -0.15))
    if ka > 0:
        SH.draw_medal(f, "karl_genc", kx - 120, ky + 22, 132, "gold", alpha=ka, inscription=False)
        f.circle(kx - 120, ky + 22, 74, style="stroke", sw=3.5, color="#F6DC8A", alpha=0.9 * ka)
    for j, nm in enumerate(("aragon", "burgonya", "avusturya")):
        k = smooth((t - t_x - j * 0.13) / 0.45)
        if k <= 0:
            continue
        x, y = pos[nm]
        sx, sy = kx - 120, ky + 22
        ex, ey = lerp(sx, x, 0.9 * k), lerp(sy, y, 0.9 * k)
        p = f.paint("#E0483A", style="stroke", sw=4, alpha=0.9 * k, cap="butt")
        import skia
        p.setPathEffect(skia.DashPathEffect.Make([12, 10], -t * 14))
        f.c.drawLine(sx, sy, ex, ey, p)
        K.x_mark(f, lerp(sx, x, 0.55), lerp(sy, y, 0.55), 15, clamp((k - 0.4) / 0.6), sw=6, alpha=k)


def _sokak_overlay(cx):
    f = cx.f
    t = cx.t
    a1 = smooth((t - cx.at(("c3s3", "1520'de", -0.1))) / 0.5)
    a2 = smooth((t - cx.at(("c3s3", "Komünero", -0.1))) / 0.5)
    if a1 <= 0:
        return
    f.rect(0, 560, W, 520, shader=f.lin(0, 560, 0, H, [("#000000", 0.0, 0), ("#000000", 1.0, int(205 * a1))]))
    SH.gold_flat(f, "1520", W / 2, 800 + 6 * (1 - a1), face="title", size=108, track=16, alpha=a1)
    if a2 > 0:
        SH.gold_flat(f, "KOMÜNERO İSYANI", W / 2, 950 + 8 * (1 - a2), face="title", size=int(92 * (0.92 + 0.08 * back_out(a2))), track=14, alpha=a2)


def _toledo_overlay(cx):
    f = cx.f
    t = cx.t
    K.tag(f, "TOLEDO", 120, 150, alpha=smooth((t - cx.at(("c3s6", "Toledo'da", -0.1))) / 0.5), size=46, align="l", pad=28)
    ma = smooth((t - cx.at(("c3s6", "María", -0.25))) / 0.8)
    if ma > 0:
        SH.draw_medal(f, "maria_pacheco", 360, 560, 440 * (0.94 + 0.06 * ease_out(ma)), "silver", alpha=ma, inscription=False, tilt=0.1 * math.sin(t * 0.6))
        SH.name_plate(f, "MARÍA PACHECO", "Padilla'nın dul eşi", None, cx_=360, y=H * 0.77, t=smooth((t - cx.at(("c3s6", "María", 0.0))) / 0.5), w=600)
    la = smooth((t - cx.at(("c3s6", "aylarca", -0.1))) / 0.5)
    if la > 0:
        f.rect(1200, 380, 720, 420, shader=f.rad(1560, 580, 360, [("#000000", 0.0, int(120 * la)), ("#000000", 1.0, 0)]))
        icons.draw_icon(f, "hourglass", 1560, 520, size=200 * (0.85 + 0.15 * back_out(la)), metal="gold", alpha=la, glow=0.3 * la)
        K.txt(f, "AYLARCA", 1560, 700, face="title", size=56, color="#F6DC8A", track=12, alpha=la)


# ───────────────────────────── çekim listesi ─────────────────────────────
SHOTS = [
    # s1 — taç için İspanya'dan ayrılış
    shot("a_map", a=0.0, tr=("fade", 0.8), cams=[(0.0, (0.5, 47.2, 1.62)), (("c3s1", "gerekti", 0.3), (1.0, 47.4, 1.72))], tint=("#5A1A1A", 0.22),
         regions=[dict(name="ispanya", color="ispanya", at=("c3s1", "İspanya'dan", -0.15), alpha=0.5)],
         routes=[dict(pts=ROTA_DENIZ, at=("c3s1", "ayrılması", -0.2), dur=1.3, color="#F0D27A", width=7), dict(pts=ROTA_KARA, at=("c3s1", "gerekti", -0.1), dur=0.7, color="#F0D27A", width=7, dash=(12, 9))],
         icons_=[dict(kind="ship", lon=-8.3, lat=43.45, size=80, at=("c3s1", "ayrılması", -0.2), route=ROTA_DENIZ, move_at=("c3s1", "ayrılması", -0.2), move_dur=1.3, metal="gold")],
         extra=_ex_rota, approx=False, label="ispanyadan_ayrilis"),
    # s2 — yabancı danışmanlar + vergi → Kastilya şehirlerinde tepki
    shot("a_map", a=("c3s2", -0.2), tr=("fade", 0.8), need=("c1_kastilya",), cams=[(0.0, (-4.0, 40.7, 2.7)), (("c3s2", "karşılandı", 0.3), (-4.0, 40.8, 2.85))], tint=("#5A1A1A", 0.3),
         regions=[dict(name="c1_kastilya", color="#8E1F26", at=("c3s2", "Kastilya", -0.1), alpha=0.5)], extra=_ex_tepki, approx=False, label="sehirlerde_tepki"),
    # s3 — 1520: Komünero İsyanı patlar
    shot("a_theatre", a=("c3s3", -0.2), tr=("whip", 0.5), scene="c3_sokak", cams=[(0.0, (960, 590, 1.0)), (("c3s3", "patladı", 0.3), (960, 560, 1.32))], dust_n=0, vig=0.62,
         overlay=_sokak_overlay, label="komunero_isyani"),
    # s4 — 23 Nisan 1521, Villalar
    shot("a_map", a=("c3s4", -0.2), tr=("fade", 0.7), need=("c1_kastilya",), cams=[(0.0, (-4.0, 41.0, 3.4)), (("c3s4", "Villalar'da,", 0.0), (-5.1, 41.7, 7.5))], tint=("#5A1A1A", 0.25),
         date=("23 NİSAN 1521", ("c3s4", "23", -0.1)), extra=_ex_villalar, approx=False, label="villalar_harita"),
    shot("a_theatre", a=("c3s4", "kraliyet", -0.35), tr=("whip", 0.4), scene="field",
         p=dict(ground="plain", weather="rain", armies=[dict(side="#8E1F26", kind="cavalry", x=0.26, row=0, n=10, dir=1, charge=1.0), dict(side="#5A3A8A", kind="peasants", x=0.74, row=1, n=34, dir=-1, charge=0.0)]),
         cams=[(0.0, SF.cam_on(0, 0.30, 1.2)), (("c3s4", "dağıttı", 0.3), SF.cam_on(0, 0.56, 1.5))], label="villalar_savas"),
    # s5 — ertesi gün üç önder idam edildi
    shot("a_medals", a=("c3s5", -0.2), tr=("dip", 0.9), size=430, y=H * 0.46, gap=500, bgname="blood", date=("ERTESİ GÜN", ("c3s5", "Ertesi", -0.1)),
         stampt=("İDAM", 960, 190, ("c3s5", "idam", -0.1), 78),
         items=[dict(key="padilla", name="PADILLA", role="Komünero önderi", metal="onyx", at=("c3s5", "Padilla,", -0.1), pw=460),
                dict(key="bravo", name="BRAVO", role="Komünero önderi", metal="onyx", at=("c3s5", "Bravo", -0.1), pw=460),
                dict(key="maldonado", name="MALDONADO", role="Komünero önderi", metal="onyx", at=("c3s5", "Maldonado", -0.1), pw=460)], label="uc_onder"),
    # s6 — Toledo: María Pacheco aylarca direndi
    shot("a_theatre", a=("c3s6", -0.2), tr=("fade", 0.8), scene="siege", p=dict(city="toledo", time="dusk", weather="rain", fire=0.3, cannon_fire=0.4),
         cams=[(0.0, (960, 540, 1.0)), (("c3s6", "direndi", 0.3), SG.cam_on_city(0.58, 1.4, y=340))], overlay=_toledo_overlay, label="toledo_pacheco"),
    # s7 — Valensiya'da Germanía
    shot("a_map", a=("c3s7", -0.2), tr=("fade", 0.8), need=("c3_valensiya",), cams=[(0.0, (-1.5, 40.2, 3.0)), (("c3s7", "Valensiya'da", -0.1), (-0.38, 39.5, 6.5))], tint=("#5A1A1A", 0.25),
         regions=[dict(name="c3_valensiya", color="#8E1F26", at=("c3s7", "Valensiya'da", -0.1), alpha=0.5)], extra=_ex_valensiya, approx=False, label="valensiya_germania"),
    # s8 — Kastilya-León bugün Villalar yıldönümünü bayram sayıyor
    shot("a_map", a=("c3s8", -0.2), tr=("fade", 0.8), need=("c3_castilla_leon",), cams=[(0.0, (-3.6, 41.6, 3.1)), (("c3s8", "bölgesi,", 0.3), (-4.5, 41.7, 3.9))], tint=("#4A1A1A", 0.18),
         regions=[dict(name="c3_castilla_leon", color="#9A2430", at=("c3s8", "Kastilya-León", -0.15), alpha=0.58)],
         labels=[dict(text="KASTİLYA-LEÓN", lon=-4.5, lat=41.7, size=62, track=20, color="#F8EBC0", at=("c3s8", "Kastilya-León", -0.1))], extra=_ex_cyl, approx=False, label="kastilya_leon"),
    shot("c3_bayram", a=("c3s8", "Villalar'ın", -0.25), tr=("fade", 0.8), t_flag=("c3s8", "Villalar'ın", -0.1), t_date=("c3s8", "yıldönümünü", -0.1), t_label=("c3s8", "bayramı", -0.1), label="bayram"),
    # s9 — ilk ders: aynı anda bütün tahtların başında duramazsın
    shot("a_map", a=("c3s9", -0.2), tr=("fade", 0.8), cams=[(0.0, (4.5, 45.4, 1.22)), (("c3s9", "duramazsın", 0.4), (4.5, 45.4, 1.28))], tint=("#4A1A1A", 0.15),
         regions=[dict(name="karl_kendi", color="#6A2A2A", at=0.4, alpha=0.18), dict(name="ferdinand", color="#6A2A2A", at=0.6, alpha=0.18)],
         extra=_ex_tahtlar, stampt=("İLK DERS", 470, 235, ("c3s9", "İlk", -0.05), 92), approx=False, label="ilk_ders"),
]
