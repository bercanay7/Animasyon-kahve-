"""Bölüm 11 (Adamın Kendisi) — özel çekim türleri. Hepsi `c11_` önekli.

Ton: yakın, sıcak, melankolik; mum ışığı. Büyük sahne yok; madalya yakın planları, sessiz notlar, ince etiketler.
"""
import math

import numpy as np
import skia

import icons
import shots as SH
import sk
from bw_lib import draw_icon2, dust2, glow_blit, gold2, static_backdrop  # noqa: E402
from bw_lib import (INK, big_gold, chain_links, curve_arrow, draw_medal2, fadeout, flame, glow, paper, push, reveal, scene_pt, scribbles, shift, spot,
                    stamp2, strike, tag)
from sk import C, H, W, back_out, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth

WARM = "#FFB347"


def warm_bg(cx, rays=0.22, glow_a=0.22, gx=W * 0.5, gy=H * 0.42, dust_n=45):
    """Mum ışığı zemini: koyu kehribar + hafifçe titreyen sıcak ışık havuzu."""
    f = cx.f
    static_backdrop(f, rays)
    fl = 0.9 + 0.1 * math.sin(cx.t * 7.3) * math.sin(cx.t * 3.1 + 1.0)
    glow_blit(f, gx, gy, 900, WARM, glow_a * fl)
    dust2(f, cx.t, n=dust_n, alpha=0.4)


def fit_plate(f, name, role, cx_, y, w=560, t=1.0):
    a = smooth(t)
    if a <= 0:
        return
    nsz = SH.fit_size(name, "title_m", 54, w - 90, 6)
    hh = 96 + (34 if role else 0)
    x0 = cx_ - w / 2
    yy = y + (1 - a) * 18
    SH.plate(f, x0, yy, w, hh, alpha=a)
    f.text(name, cx_, yy + 56, face="title_m", size=nsz, color="#F3DE9A", align="c", track=6, alpha=a, shadow=(2, 3, 3, "#000000"))
    if role:
        f.text(role, cx_, yy + 88, face="cap_i", size=28, color="#D9C795", align="c", alpha=a)


# ───────────────────────────── s1: devasa makine (beş cephe çarkları) + adam ─────────────────────────────
GEARS = [  # (x, y, boyut, yön, simge, hız)
    (470, 560, 880, 1, "coinbag", 1.0),
    (1260, 250, 620, -1, "monk", 1.42),
    (1400, 830, 700, -1, "crown", 1.26),
    (1830, 520, 420, 1, "crescent", 2.1),
    (120, 960, 460, -1, "family", 2.0),
]


@SH.kind("c11_machine")
def k_machine(cx, man_at=0.0, plate_at=2.2, q_at=2.6):
    f = cx.f
    warm_bg(cx, rays=0.18, glow_a=0.16)
    ga = cx.amt(0.0, 1.2)
    with push(cx, 1.0, 1.06):
        for (x, y, sz, d, ic, sp) in GEARS:
            rot = d * cx.t * 0.10 * sp
            draw_icon2(f, "b_gear", x, y, size=sz, metal="bronze", alpha=0.42 * ga, rot=rot, shadow=False)
            draw_icon2(f, ic, x, y, size=sz * 0.17, metal="gold", alpha=0.55 * ga, shadow=False)
        # adam: madalya
        a = cx.amt(man_at, 1.0)
        glow(f, W / 2, 500, 460, WARM, 0.22 * a)
        draw_medal2(f, "karl_olgun", W / 2, 500, 560 * (0.92 + 0.08 * ease_out(a)), "gold", False, alpha=a, tilt=0.14 * math.sin(cx.t * 0.5))
        fit_plate(f, "V. KARL", None, W / 2, 800, w=420, t=cx.amt(plate_at, 0.6))
        qa = cx.amt(q_at, 0.7)
        if qa > 0:
            draw_icon2(f, "question", 1320, 470, size=210 * (0.85 + 0.15 * back_out(qa)), metal="gold", alpha=0.9 * qa, glow=0.3)
    f.vig(0.62)


# ───────────────────────────── s2: Habsburg çenesi (saygılı yakın plan) ─────────────────────────────
@SH.kind("c11_chin")
def k_chin(cx, zoom_at=0.6, zoom_dur=2.2, label_at=0.3, tag_at=5.3, key="karl_olgun"):
    f = cx.f
    warm_bg(cx, rays=0.18, glow_a=0.2, gx=W * 0.55)
    # POI: çene (madalya içinde u=0.66, v=0.66)
    u, v = 0.66, 0.66
    k = ease_io(clamp((cx.t - cx.at(zoom_at)) / zoom_dur))
    size = lerp(640, 2100, k)
    # POI ekranda: başta madalya merkezinde → sonda (1180, 600)
    c0 = (W / 2 + (u - 0.5) * 640, 500 + (v - 0.5) * 640)
    c1 = (1130, 560)
    px, py = lerp(c0[0], c1[0], k), lerp(c0[1], c1[1], k)
    mx, my = px - (u - 0.5) * size, py - (v - 0.5) * size
    a = cx.amt(0.0, 0.8)
    drift = cx.u * 40
    draw_medal2(f, key, mx - drift, my, size, "gold", False, alpha=a, tilt=0.0, shadow=(k < 0.4))
    # ölçü yayı: çene hattı
    lk = cx.amt(label_at, 0.8, off=0.0)
    if lk > 0:
        cxp, cyp = px - drift, py
        r = lerp(150, 330, k)
        p = skia.Path()
        p.addArc(skia.Rect.MakeLTRB(cxp - r, cyp - r * 0.8, cxp + r, cyp + r * 0.8), 15, 110)
        pa = f.paint("#F0D27A", style="stroke", sw=3.2, alpha=0.9 * lk)
        pa.setPathEffect(skia.DashPathEffect.Make([14, 10], 0))
        f.c.drawPath(p, pa)
        # etiket: altta koyu şerit üstünde
        f.rect(0, H * 0.74, W, H * 0.26, shader=f.lin(0, H * 0.74, 0, H, [("#000000", 0.0, 0), ("#000000", 0.45, int(150 * lk)), ("#000000", 1.0, int(235 * lk))]))
        lx, ly = 140, 930
        f.text("HABSBURG ÇENESİ", lx, ly, face="title", size=60, color="#F4DD92", align="l", track=10, alpha=lk, shadow=(2, 3, 4, "#000000"))
        f.text("ağzı tam kapatamamak · çiğneme güçlüğü", lx + 4, ly + 54, face="cap_i", size=36, color="#D9C795", align="l", alpha=lk * cx.amt(label_at, 0.6, off=0.5))
    tk = cx.amt(tag_at, 0.5)
    if tk > 0:
        tag(f, "YAZILIR", 1500, 940, size=30, alpha=tk, track=14)
    f.vig(0.66)


# ───────────────────────────── s3: 2019 çalışması — küçük, kesin değil ─────────────────────────────
STUDY_KEYS = ["maksimilyan", "filip", "karl_olgun", "ferdinand", "felipe2", "juana"]


@SH.kind("c11_study")
def k_study(cx, year_at=0.0, portrait_at=2.0, face_at=3.1, kin_at=5.2, link_at=6.4, small_at=8.0, sure_at=9.6):
    f = cx.f
    warm_bg(cx, rays=0.18, glow_a=0.16)
    a = cx.amt(0.0, 0.8)
    with push(cx, 1.0, 1.04):
        with paper(f, 960, 560, 1560, 800, rot=-0.008, alpha=a, seed=19, tone="#B79C68", shade=0.5):
            f.text("2019", -540, -400 + 112, face="title", size=96, color="#4A2E12", align="l", track=10, alpha=0.95 * cx.amt(year_at, 0.8))
            f.text("ÇALIŞMA", -250, -400 + 112, face="fell", size=52, color=INK, align="l", track=8, alpha=0.9 * cx.amt(year_at, 0.8, off=0.3))
            f.line(-710, -400 + 138, 710, -400 + 138, color=INK, sw=2.2, alpha=0.5 * a)
            # portre şeridi (hanedan portreleri)
            n = len(STUDY_KEYS)
            for i, key in enumerate(STUDY_KEYS):
                k = cx.amt(portrait_at, 0.5, off=0.18 * i)
                if k <= 0:
                    continue
                x = -600 + i * 240
                draw_medal2(f, key, x, -400 + 330, 200 * (0.85 + 0.15 * ease_out(k)), "gold", flip=(i % 2 == 1), alpha=k, shadow=True, inscription=False)
                # halka: ardışık portreler arası 'akraba evliliği' bağı
                if i < n - 1:
                    lk = cx.amt(kin_at, 0.4, off=0.12 * i)
                    if lk > 0:
                        draw_icon2(f, "ring", x + 120, -400 + 330, size=58, metal="bronze", alpha=lk, shadow=False)
            # iki kavram: yüz özellikleri ↔ akraba evlilikleri
            fk = cx.amt(face_at, 0.6)
            if fk > 0:
                f.text("YÜZ ÖZELLİKLERİ", -470, 118, face="title_m", size=38, color="#3A2610", align="c", track=6, alpha=fk)
            kk = cx.amt(kin_at, 0.6)
            if kk > 0:
                f.text("AKRABA EVLİLİKLERİ", 450, 118, face="title_m", size=38, color="#3A2610", align="c", track=6, alpha=kk)
            # bağ oku (ilişkilendirdi) → belirsizleşir
            lk = clamp((cx.t - cx.at(link_at)) / 0.9)
            unsure = cx.amt(small_at, 0.8)
            if lk > 0:
                col = mix("#8E6A1A", "#6B6B6B", unsure)
                curve_arrow(f, (-200, 104), (120, 104), bend=0, prog=ease_out(lk), color=col, sw=7, head=True, alpha=0.95, shadow=False, dash=((14, 10) if unsure > 0.5 else None))
            if unsure > 0.4:
                draw_icon2(f, "question", -40, 104, size=110 * unsure, metal="silver", alpha=unsure * 0.9, shadow=False)
    sa = cx.amt(small_at, 0.3)
    if sa > 0:
        stamp2(f, "ÇALIŞMA KÜÇÜK", 610, 850, rot=-0.05, size=56, t=sa, seed=6, fill_bg="#150D08")
    sb = cx.amt(sure_at, 0.3)
    if sb > 0:
        stamp2(f, "KESİN DEĞİL", 1370, 872, rot=0.05, size=52, t=sb, seed=17, fill_bg="#150D08", color="#B03030")
    f.vig(0.62)


# ───────────────────────────── s4: 26 yaşında Portekizli kuzeni İsabel'le evlendi ─────────────────────────────
@SH.kind("c11_wed")
def k_wed(cx, age_at=0.0, isabel_at=1.6, ring_at=3.2, size=500, y=H * 0.5):
    f = cx.f
    warm_bg(cx, rays=0.2, glow_a=0.22)
    gap = 640
    # üst: 26 YAŞINDA
    ak = cx.amt(age_at, 0.7)
    if ak > 0:
        v = int(round(26 * ease_out(clamp((cx.t - cx.at(age_at)) / 0.9), 2)))
        big_gold(f, str(max(1, v)), W / 2 - 150, 218, size=150, alpha=ak, track=6)
        f.text("YAŞINDA", W / 2 + 40, 218, face="title_m", size=48, color="#E0C682", align="l", track=14, alpha=cx.amt(age_at, 0.6, off=0.3))
    items = [("karl_genc", "V. KARL", None, "gold", False, 0.0), ("isabel", "İSABEL", "Portekizli kuzeni", "silver", True, isabel_at)]
    for i, (key, name, role, metal, flip, ta) in enumerate(items):
        x = W / 2 + (-gap / 2 if i == 0 else gap / 2)
        k = cx.amt(ta, 0.8)
        sl = (1 - ease_out(k)) * (-100 if i == 0 else 100)
        gl = (cx.t * 0.25 + 0.3 * i) % 2.0
        draw_medal2(f, key, x + sl, y + 40, size * (0.94 + 0.06 * ease_out(k)), metal if key != "karl_genc" else "gold", flip, alpha=k,
                    tilt=(0.16 if i == 0 else -0.16) * math.sin(cx.t * 0.5 + i) + (0.12 if i == 0 else -0.12), glint=(gl if gl < 1 else None))
        fit_plate(f, name, role, x, y + 40 + size * 0.53, w=520, t=cx.amt(ta, 0.6, off=0.4))
    rk = cx.amt(ring_at, 0.5)
    if rk > 0:
        glow(f, W / 2, y + 40, 220, "#FFE2A0", 0.5 * rk * (1 - 0.4 * cx.amt(ring_at, 1.0, off=0.5)))
        draw_icon2(f, "ring", W / 2, y + 40, size=170 * (0.6 + 0.4 * back_out(rk)), metal="gold", alpha=rk, glow=0.45)
    f.vig(0.62)


# ───────────────────────────── s5a: İsabel öldü — madalya altından onikse döner ─────────────────────────────
@SH.kind("c11_loss")
def k_loss(cx, year_at=0.0, age_at=2.4, death_at=3.3, size=560, y=H * 0.48):
    f = cx.f
    warm_bg(cx, rays=0.14, glow_a=0.12)
    a = cx.amt(0.0, 0.8)
    dk = cx.amt(death_at, 1.2)
    with push(cx, 1.0, 1.05):
        draw_medal2(f, "isabel", W / 2, y, size, "silver", True, alpha=a * (1 - dk), tilt=0.1 * math.sin(cx.t * 0.5))
        draw_medal2(f, "isabel", W / 2, y, size, "onyx", True, alpha=a * dk, tilt=0.1 * math.sin(cx.t * 0.5), shadow=False)
        fit_plate(f, "İSABEL", None, W / 2, y + size * 0.53, w=420, t=cx.amt(0.3, 0.6))
    yk = cx.amt(year_at, 0.8)
    if yk > 0:
        gold2(f, "1539", 420, 260, face="title", size=120, track=12, alpha=yk, glow=0.3 * yk)
    ak = cx.amt(age_at, 0.6)
    if ak > 0:
        tag(f, "35 YAŞINDA", 1500, 330, size=34, alpha=ak, track=12)
    f.vig(0.66)


# ───────────────────────────── s5b: manastıra çekildi (üzerine bindirme: sahne üstünde) ─────────────────────────────
def cloister_overlay(approx_at, two_at, never_at):
    def ov(cx):
        f = cx.f
        k = cx.amt(approx_at, 0.6)
        if k > 0:
            f.rect(0, H * 0.70, W, H * 0.30, shader=f.lin(0, H * 0.70, 0, H, [("#000000", 0.0, 0), ("#000000", 1.0, int(205 * k))]))
            w1 = sk.text_width("YAKLAŞIK", "title_m", 48, 14)
            w2 = sk.text_width("İKİ AY", "title", 104, 12)
            tot = w1 + 46 + w2
            x0 = W / 2 - tot / 2 - 130
            f.text("YAKLAŞIK", x0, H * 0.905, face="title_m", size=48, color="#C9B27A", align="l", track=14, alpha=k, shadow=(2, 3, 4, "#000000"))
            k2 = cx.amt(two_at, 0.6)
            if k2 > 0:
                gold2(f, "İKİ AY", x0 + w1 + 46, H * 0.905 + 4, face="title", size=104, track=12, alpha=k2, glow=0.25 * k2, align="l")
                tag(f, "MANASTIR", x0 + tot + 130, H * 0.905 - 6, size=32, alpha=cx.amt(two_at, 0.5, off=0.3), track=14, align="l")
        k3 = cx.amt(never_at, 0.6)
        if k3 > 0:
            draw_icon2(f, "ring", 1700, 260, size=170, metal="gold", alpha=k3 * (1 - 0.5 * cx.amt(never_at, 0.7, off=0.2)), glow=0.2)
            sl = clamp((cx.t - cx.at(never_at, off=0.35)) / 0.4)
            if sl > 0:
                draw_icon2(f, "b_forbid", 1700, 260, size=240 * (1.2 - 0.2 * ease_out(sl)), metal="crimson", alpha=0.95 * sl, glow=0.2)
    return ov


# ───────────────────────────── s6: ömrünün sonuna kadar siyah ─────────────────────────────
@SH.kind("c11_black")
def k_black(cx, black_at=1.3, tag_at=2.0, size=600):
    f = cx.f
    warm_bg(cx, rays=0.12, glow_a=0.12)
    a = cx.amt(0.0, 0.8)
    bk = cx.amt(black_at, 1.0)
    with push(cx, 1.0, 1.05):
        draw_medal2(f, "karl_yasli", W / 2, 500, size, "gold", False, alpha=a * (1 - bk), tilt=0.08 * math.sin(cx.t * 0.5))
        draw_medal2(f, "karl_yasli", W / 2, 500, size, "onyx", False, alpha=a * bk, tilt=0.08 * math.sin(cx.t * 0.5), shadow=(bk < 0.5))
    # kenarlardan inen siyah örtü
    if bk > 0:
        veil = sk.baked("c11_black_veil", lambda g: g.rect(0, 0, W, H, shader=g.rad(W / 2, 500, 900, [("#000000", 0.0, 0), ("#000000", 0.55, 60), ("#000000", 1.0, 190)])))
        vp = skia.Paint()
        vp.setAlphaf(clamp(bk))
        f.c.drawImage(veil, 0, 0, skia.SamplingOptions(), vp)
    tk = cx.amt(tag_at, 0.5)
    if tk > 0:
        tag(f, "ANLATILIR", W / 2, 920, size=32, alpha=tk, track=16)
    f.vig(0.7)


# ───────────────────────────── s7: gut, perhiz, bol yemek (sahne üstü etiketler) ─────────────────────────────
FOOT = (985, 738)      # bedroom sahnesi: hasta bacağın dayandığı minder (props katmanı, derinlik 1.0)
PLATE = (1190, 700)    # komodin: tabak + ekmek


def gout_overlay(cams, gut_at, still_at, diet_at, feast_at, tag_at):
    """Bedroom üstü: gut = bacakta kırmızı zonklama (üç atak), PERHİZ = tabağın üstünde yasak halkası, BOL YEMEK = halka erir, yemek ısınır.
    Altta ince etiket sırası; YAZILIR rozeti sağ üstte. Efektler sahne nesnesine kilitli (bw_lib.scene_pt)."""
    def ov(cx):
        f = cx.f
        # --- gut atakları: üç zonklama halkası + sürekli ince kızıl ışık
        tg = cx.t - cx.at(gut_at, off=-0.1)
        if tg > -0.2:
            fx, fy, s = scene_pt(cx, cams, *FOOT)
            base = 0.20 + 0.10 * math.sin(cx.t * 3.2)
            k_in = clamp(tg / 0.5)
            glow(f, fx, fy, 120 * s, "#E0392B", base * k_in)
            for i in range(3):
                ti = tg - i * 0.62
                if 0 < ti < 1.15:
                    u = ti / 1.15
                    r = (34 + 150 * ease_out(u)) * s
                    f.circle(fx, fy, r, style="stroke", sw=max(1.5, 6 * (1 - u)) * s, color="#E8493A", alpha=0.85 * (1 - u) ** 1.2)
                    glow(f, fx, fy, r * 0.9, "#E0392B", 0.35 * (1 - u))
        # --- perhiz: yasak halkası tabağın üstünde; bol yemekte erir
        td = cx.amt(diet_at, 0.45)
        tf = cx.amt(feast_at, 0.7)
        if td > 0:
            px, py, s = scene_pt(cx, cams, *PLATE)
            ring = td * (1.0 - tf)
            if ring > 0.01:
                draw_icon2(f, "b_forbid", px, py - 10 * s, size=210 * s * (1.2 - 0.2 * ease_out(td)) * (1 + 0.25 * tf), metal="crimson", alpha=0.92 * ring, glow=0.2)
            if tf > 0:
                glow(f, px + 10 * s, py - 8 * s, 150 * s, "#FFC060", 0.42 * tf * (0.9 + 0.1 * math.sin(cx.t * 5.0)))
        # --- alt karartma + etiketler
        f.rect(0, H * 0.74, W, H * 0.26, shader=f.lin(0, H * 0.74, 0, H, [("#000000", 0.0, 0), ("#000000", 1.0, int(205 * cx.amt(gut_at, 0.6)))]))
        for (lab, ta, x) in (("GUT ATAKLARI", gut_at, 402), ("HAREKETSİZ", still_at, 865), ("PERHİZ", diet_at, 1222), ("BOL YEMEK", feast_at, 1565)):
            k = cx.amt(ta, 0.5)
            if k > 0:
                f.text(lab, x, H * 0.90, face="title_m", size=40, color="#F0DDA0", align="c", track=10, alpha=k, shadow=(2, 3, 4, "#000000"))
                hw = sk.text_width(lab, "title_m", 40, 10) / 2
                f.line(x - hw, H * 0.90 + 18, x + hw, H * 0.90 + 18, color="#C9962B", sw=2, alpha=0.8 * k)
        tk = cx.amt(tag_at, 0.5)
        if tk > 0:
            tag(f, "YAZILIR", W - 330, 170, size=30, alpha=tk, track=14)
    return ov


# ───────────────────────────── s8/s9: dolaşarak yönetti — gezi ağı ─────────────────────────────
STOPS = [("ALMANYA", (10.0, 50.3)), ("İTALYA", (12.0, 43.4)), ("İSPANYA", (-3.8, 40.3)), ("HOLLANDA", (5.0, 52.0)),
         ("FRANSA", (2.3, 47.0)), ("TUNUS", (10.0, 36.8)), ("CEZAYİR", (3.0, 36.7))]
BENDS = [90, -110, 100, -60, 70, -90]


def make_travel(times, dur=1.0, all_done=False):
    """times: her durak için çapa (7 adet; ilki yalnızca belirir). Gezi yolu duraktan durağa çizilir, taç ilerler."""
    def extra(cx, cam, mv):
        f = cx.f
        pts = [cam.ll(*p) for (_, p) in STOPS]
        head = None
        for i in range(len(STOPS) - 1):
            k = 1.0 if all_done else clamp((cx.t - cx.at(times[i + 1], off=-0.15)) / dur)
            if k <= 0:
                continue
            curve_arrow(f, pts[i], pts[i + 1], bend=BENDS[i], prog=ease_io(k), color="#F0D27A", sw=6, head=(k < 1 or True), alpha=0.95)
            if k < 1:
                mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
                dx, dy = pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]
                L = math.hypot(dx, dy) or 1
                qx, qy = mx - dy / L * BENDS[i], my + dx / L * BENDS[i]
                t_ = ease_io(k)
                hx = (1 - t_) ** 2 * pts[i][0] + 2 * (1 - t_) * t_ * qx + t_ ** 2 * pts[i + 1][0]
                hy = (1 - t_) ** 2 * pts[i][1] + 2 * (1 - t_) * t_ * qy + t_ ** 2 * pts[i + 1][1]
                head = (hx, hy)
        # duraklar: nokta + ad
        for i, (name, ll) in enumerate(STOPS):
            k = 1.0 if all_done else (cx.amt(times[i], 0.5, off=-0.1))
            if k <= 0:
                continue
            x, y = pts[i]
            f.circle(x, y, 22 * (1.0 + 0.5 * (1 - k)), color="#F0D27A", alpha=0.2 * k, blur=6)
            f.circle(x, y, 9, color="#F0D27A", alpha=k)
            f.circle(x, y, 9, style="stroke", sw=2, color="#2A1A0C", alpha=k)
            dy_ = -30 if name not in ("TUNUS", "CEZAYİR") else 44
            f.text(name, x, y + dy_, face="title_m", size=34, color="#F6ECCB", align="c", track=8, alpha=k, shadow=(2, 2, 4, "#000000"))
        if head is not None:
            glow(f, head[0], head[1], 70, "#FFD27A", 0.5)
            draw_icon2(f, "imperial_crown", head[0], head[1] - 28, size=70, metal="gold", alpha=1.0, glow=0.4)
        nk = 1.0 if all_done else cx.amt(times[1], 0.8, off=-0.2)
        if nk > 0:      # güzergâh tarihsel bir rota değil, durakları bağlayan şematik çizgi
            f.text("güzergâh şematiktir", 110, 1004, face="cap_i", size=28, color="#CDBB88", align="l", alpha=0.72 * nk)
    return extra


def road_overlay(desk_at, road_at):
    """Son çekim: 'masada değil, yollarda' — masa (yazı takımı) silinir, yol parlar. Sol Atlantik boşluğuna yerleşir."""
    def ov(cx):
        f = cx.f
        k = cx.amt(desk_at, 0.5)
        if k > 0:
            f.rrect(90, 250, 560, 190, 18, color="#150D08", alpha=0.84 * k)
            f.rrect(90, 250, 560, 190, 18, style="stroke", sw=2.5, color="#7A5518", alpha=0.9 * k)
            draw_icon2(f, "scroll", 200, 345, size=120, metal="ivory", alpha=k, shadow=False)
            draw_icon2(f, "quill", 350, 335, size=120, metal="gold", alpha=k, shadow=False)
            f.text("MASA", 540, 372, face="title_m", size=44, color="#E7D5A0", align="c", track=12, alpha=k)
            sl = clamp((cx.t - cx.at(desk_at, off=0.35)) / 0.45)
            if sl > 0:
                strike(f, 110, 360, 630, 338, sl, sw=11, seed=4)
        rk = cx.amt(road_at, 0.6)
        if rk > 0:
            f.rect(0, 470, 760, 200, shader=f.lin(0, 470, 0, 670, [("#000000", 0.0, 0), ("#000000", 0.5, int(190 * rk)), ("#000000", 1.0, 0)]))
            gold2(f, "YOLLARDA", 380, 600, face="title", size=96, track=18, alpha=rk, glow=0.4 * rk)
    return ov
