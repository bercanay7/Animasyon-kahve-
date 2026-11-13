"""Bölüm 5 (İmparator Hep Başka Yerde) — özel çekim türleri. Hepsi `c5_` önekli.

Ton: yol/kervan — toprak, duman; sonunda salon (c0'a dönüş). Reform hattı petrol, Habsburg kırmızı, Fransa mavi, Osmanlı yeşil.
"""
import math

import numpy as np
import skia

import icons
import shots as SH
import sk
from bw_lib import (INK, backdrop, big_gold, chain_links, curve_arrow, duo_glow, fadeout, glow, paper, push, reveal, scribbles, shift,
                    spot, stamp2, strike, tag)
from bw_lib import draw_icon2, dust2, glow_blit, gold2, static_backdrop  # noqa: E402
from bw_lib import draw_medal2  # noqa: E402
from sk import C, H, W, back_out, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth

PETROL = "#1E5560"
PETROL_L = "#3F8C96"
CRIM = "#8E1F26"
ROYAL = "#27427A"
FOREST = "#2F6B4A"


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


# ───────────────────────────── s1: Almanya'dan ayrıldı, dokuz yıl dönemedi ─────────────────────────────
ROUTE_LEAVE = [(8.36, 49.63), (3.2, 48.4), (-1.6, 44.8), (-4.72, 41.65)]


def make_leave(go_at, year_at, block_at):
    def extra(cx, cam, mv):
        f = cx.f
        # imparatorun gidiş yolu
        k = ease_io(clamp((cx.t - cx.at(go_at)) / 2.4))
        if k > 0:
            mv.route(f, cam, ROUTE_LEAVE, prog=k, color="#F0D27A", width=6, arrow=True)
            (x, y), ang = mv.point_on(cam, ROUTE_LEAVE, k)
            draw_icon2(f, "crown", x, y - 36, size=64, metal="gold", alpha=min(1.0, k * 6), glow=0.4)
        # geri dönüş: kesikli kırmızı ok + yasak
        bk = clamp((cx.t - cx.at(block_at)) / 0.9)
        if bk > 0:
            mv.route(f, cam, [(-3.5, 42.5), (2.4, 46.4), (7.4, 49.2)], prog=bk, color="#C0392B", width=5, dash=(12, 10), arrow=True, alpha=0.95)
            mx, my = cam.ll(1.8, 46.1)
            draw_icon2(f, "b_forbid", mx, my, size=150 * (1.2 - 0.2 * ease_out(bk)), metal="crimson", alpha=bk, glow=0.25)
        # 9 YIL
        ya = cx.amt(year_at, 0.6)
        if ya > 0:
            px, py = 320, 430
            f.rrect(px - 215, py - 190, 430, 420, 24, color="#150D08", alpha=0.82 * ya)
            f.rrect(px - 215, py - 190, 430, 420, 24, style="stroke", sw=3, color="#C9962B", alpha=0.9 * ya)
            draw_icon2(f, "hourglass", px, py - 100, size=150, metal="gold", alpha=ya, shadow=False, glow=0.2)
            big_gold(f, "9", px, py + 100, size=190, alpha=ya, track=4)
            f.text("YIL", px, py + 170, face="title_m", size=50, color="#E0C682", align="c", track=18, alpha=ya)
    return extra


# ───────────────────────────── s2: üç cepheden baskı ─────────────────────────────
def make_pressure(es_at, fr_at, ot_at):
    center = (7.5, 47.2)

    def extra(cx, cam, mv):
        f = cx.f
        cxp, cyp = cam.ll(*center)
        # merkez: taç (imparator)
        ck = cx.amt(0.1, 0.8)
        glow(f, cxp, cyp, 120, "#FFD27A", 0.35 * ck)
        draw_icon2(f, "imperial_crown", cxp, cyp, size=110 * (0.85 + 0.15 * ck), metal="gold", alpha=ck, glow=0.35)
        specs = [(es_at, (-3.8, 40.2), "#C0392B", "İSPANYA", (-1.0, 38.4), 60),
                 (fr_at, (0.6, 46.6), "#4B6DB5", "FRANSA", (-0.5, 49.2), -50),
                 (ot_at, (26.0, 40.6), "#4FA57A", "OSMANLI", (23.0, 39.6), 70)]
        for (ta, src, col, lab, lpos, bend) in specs:
            k = clamp((cx.t - cx.at(ta)) / 1.0)
            if k <= 0:
                continue
            sx, sy = cam.ll(*src)
            # kuyruğu hafif geriden başlasın, ok merkeze 90 px kala bitsin
            dx, dy = cxp - sx, cyp - sy
            L = math.hypot(dx, dy)
            ex, ey = cxp - dx / L * 95, cyp - dy / L * 95
            curve_arrow(f, (sx, sy), (ex, ey), bend=bend, prog=ease_out(k, 2), color=col, sw=11, alpha=0.95)
            lx, ly = cam.ll(*lpos)
            f.text(lab, lx, ly, face="title", size=40, color="#F6ECCB", align="c", track=10, alpha=smooth(k * 2), shadow=(2, 3, 4, "#000000"))
    return extra


# ───────────────────────────── s3a: Luther'in fikirleri yayıldı (uçuşan risaleler) ─────────────────────────────
@SH.kind("c5_ideas")
def k_ideas(cx, tag_at=0.9, n=34):
    f = cx.f
    static_backdrop(f, 0.22, (PETROL, "#6B3F1E", 0.30, H * 0.5))
    dust2(f, cx.t, n=50)
    rs = np.random.RandomState(12)
    # merkezde alev (fikir)
    fk = cx.amt(0.0, 0.7)
    glow(f, 560, 560, 380, "#FFB347", 0.28 * fk)
    draw_icon2(f, "b_flame", 560, 560 - 6 * math.sin(cx.t * 3), size=250 * (0.85 + 0.15 * fk), metal="gold", alpha=fk, glow=0.5)
    # uçuşan sayfalar: soldan sağa, derinlik katmanlı
    for i in range(n):
        t0 = 0.15 + rs.rand() * 1.9
        dur = 1.6 + rs.rand() * 1.2
        k = (cx.t - t0) / dur
        d = 0.45 + rs.rand() * 0.9                # derinlik (ölçek)
        y0 = 560 + rs.randn() * 40
        y1 = 170 + rs.rand() * 800
        x0, x1 = 600 + rs.rand() * 80, 760 + rs.rand() * 1050
        sd = rs.rand() * 6
        if k <= 0 or k >= 1.15:
            continue
        kk = clamp(k)
        u = ease_out(kk, 1.7)
        x = lerp(x0, x1, u)
        y = lerp(y0, y1, u) + math.sin(kk * 7 + sd) * 36 * d
        rot = math.sin(kk * 5 + sd) * 0.7 + (kk * 3.0 if i % 3 == 0 else 0)
        w, h = 120 * d, 160 * d
        a = smooth(kk * 6) * (1 - smooth((kk - 0.85) / 0.3))
        f.c.save()
        f.c.translate(x, y)
        f.c.rotate(math.degrees(rot))
        f.rrect(-w / 2, -h / 2, w, h, 6, shader=f.lin(0, -h / 2, 0, h / 2, [("#D9C79A", 0.0), ("#A8946A", 1.0)]), alpha=a * (0.50 + 0.40 * d / 1.35))
        for r in range(5):
            f.line(-w * 0.36, -h * 0.30 + r * h * 0.16, w * 0.36 - (w * 0.2 if r == 4 else 0), -h * 0.30 + r * h * 0.16, color="#3A2A18", sw=max(1.5, 3 * d), alpha=0.6 * a)
        f.c.restore()
    ta = cx.amt(tag_at, 0.6)
    if ta > 0:
        tag(f, "LUTHER'İN FİKİRLERİ", 560, 800, size=30, alpha=ta, track=8, icon=None)
    f.vig(0.6)


# ───────────────────────────── s3 üstü: Köylü Savaşı bindirmeleri (field sahnesi üzerine) ─────────────────────────────
def peasants_overlay(year_at, war_at, notl_at, num_at):
    def ov(cx):
        f = cx.f
        # alt şerit (okunurluk için koyu degrade)
        k1 = cx.amt(year_at, 0.7) if year_at is not None else 0.0
        if k1 > 0:
            f.rect(0, H * 0.70, W, H * 0.30, shader=f.lin(0, H * 0.70, 0, H, [("#000000", 0.0, 0), ("#000000", 1.0, int(215 * k1))]))
            gold2(f, "1524", 260, H * 0.90, face="title", size=118, track=10, alpha=k1, glow=0.3 * k1, align="c")
        k2 = cx.amt(war_at, 0.7) if war_at is not None else 0.0
        if k2 > 0:
            f.text("KÖYLÜ SAVAŞI", 560, H * 0.90 - 10, face="title_m", size=50, color="#F0DDA0", align="l", track=12, alpha=k2, shadow=(2, 3, 4, "#000000"))
        # Luther istememişti
        k3 = cx.amt(notl_at, 0.7) if notl_at is not None else 0.0
        if k3 > 0:
            draw_medal2(f, "luther", 1560, 330, 330 * (0.92 + 0.08 * ease_out(k3)), "teal", True, alpha=k3, tilt=0.1 * math.sin(cx.t * 0.7))
            draw_icon2(f, "b_forbid", 1560, 330, size=260 * (1.25 - 0.25 * ease_out(k3)), metal="crimson", alpha=0.92 * k3, glow=0.2)
            tag(f, "LUTHER İSTEMEMİŞTİ", 1560, 530, size=28, alpha=k3, track=6)
        # sayı
        k4 = cx.amt(num_at, 0.7) if num_at is not None else 0.0
        if k4 > 0:
            v = clamp((cx.t - cx.at(num_at)) / 1.3)
            lo, hi = int(round(70000 * ease_out(v, 2))), int(round(100000 * ease_out(v, 2)))
            s = f"{SH.fmt_int(lo)} – {SH.fmt_int(hi)}"
            f.rect(0, H * 0.62, W, H * 0.38, shader=f.lin(0, H * 0.62, 0, H, [("#000000", 0.0, 0), ("#000000", 0.6, int(230 * k4)), ("#000000", 1.0, int(240 * k4))]))
            big_gold(f, s, W / 2, H * 0.84, size=124, alpha=k4, track=4)
            f.text("KİŞİ ÖLDÜ", W / 2, H * 0.84 + 66, face="title_m", size=40, color="#E0C682", align="c", track=18, alpha=cx.amt(num_at, 0.5, off=0.4))
            tag(f, "TAHMİN", W - 330, H * 0.84 - 150, size=26, alpha=cx.amt(num_at, 0.5, off=0.6), track=8, color="#F3C9A0", edge="#B02A2A")
    return ov


# ───────────────────────────── s4: Speyer 1529 — Katolik çoğunluk, Worms Fermanı yeniden yürürlükte ─────────────────────────────
@SH.kind("c5_speyer")
def k_speyer(cx, year_at=0.0, city_at=1.5, maj_at=2.9, ferman_at=4.0, stamp_at=5.3):
    f = cx.f
    static_backdrop(f, 0.28, ("#7A5D1E", PETROL, 0.26))
    dust2(f, cx.t, n=50)
    with push(cx, 1.0, 1.05):
        # üst başlık: 1529 · SPEYER
        ya = cx.amt(year_at, 0.8)
        if ya > 0:
            gold2(f, "1529", 520, 215, face="title", size=130, track=14, alpha=ya, glow=0.3 * ya)
        ca = cx.amt(city_at, 0.7)
        if ca > 0:
            f.text("SPEYER", 520, 300, face="title_m", size=56, color="#F0DDA0", align="c", track=24, alpha=ca, shadow=(2, 3, 4, "#000000"))
        # oylama: jeton yığınları — Katolik çoğunluk (yüksek) ↔ azınlık (alçak)
        base_y = 880
        for (xc, nt, col, metal, lab, sub_) in ((330, 9, "#D4B64E", "gold", "KATOLİK", "ÇOĞUNLUK"), (700, 4, PETROL_L, "teal", "AZINLIK", None)):
            top_y = base_y - 36 - nt * 44
            for i in range(nt):
                ki = clamp((cx.t - cx.at(maj_at, off=0.11 * i)) / 0.30)
                if ki <= 0:
                    continue
                y = base_y - 36 - i * 44 - (1 - ease_out(ki)) * 140
                f.rrect(xc - 105, y - 6, 210, 44, 16, shader=f.lin(0, y, 0, y + 44, [(mix(col, "#FFFFFF", 0.22), 0.0), (col, 0.5), (mix(col, "#000000", 0.5), 1.0)]), alpha=ki)
                f.oval(xc, y - 6, 105, 19, color=mix(col, "#FFFFFF", 0.28), alpha=ki)
                f.oval(xc, y - 6, 105, 19, style="stroke", sw=2, color=mix(col, "#000000", 0.55), alpha=0.85 * ki)
            ka = cx.amt(maj_at, 0.6, off=0.11 * nt * 0.6)
            if ka > 0:
                draw_icon2(f, "cross", xc, top_y - 66, size=112, metal=metal, alpha=ka, shadow=False, glow=0.15)
                f.text(lab, xc, base_y + 60, face="title_m", size=34, color="#E7D5A0", align="c", track=8, alpha=ka)
                if sub_:
                    f.text(sub_, xc, base_y + 100, face="cap_i", size=34, color="#C9B27A", align="c", track=4, alpha=ka)
        # Worms Fermanı: sağda, yeniden canlanır
        fk = cx.amt(ferman_at, 0.8)
        if fk > 0:
            yy = 520 + (1 - ease_out(fk)) * 100
            with paper(f, 1370, yy, 620, 720, rot=0.035, alpha=fk, seed=71):
                f.text("WORMS FERMANI", 0, -360 + 100, face="fell", size=48, color=INK, align="c", track=2, alpha=fk)
                f.line(-200, -360 + 124, 200, -360 + 124, color=INK, sw=2, alpha=0.5 * fk)
                scribbles(f, -240, -360 + 190, 480, 9, prog=clamp((cx.t - cx.at(ferman_at, off=0.3)) / 1.2), seed=29, line_h=50, thick=6.4, alpha=0.62 * fk)
                SH.wax_seal(f, 150, 250, 58, color="#8E1F26", t=1.0, alpha=fk)
        sa = cx.amt(stamp_at, 0.3)
        if sa > 0:
            stamp2(f, "YENİDEN YÜRÜRLÜKTE", 1330, 860, rot=-0.09, size=48, t=sa, seed=14, fill_bg="#150D08")
    f.vig(0.6)


# ───────────────────────────── s5: itiraz → protesto → Protestan ─────────────────────────────
@SH.kind("c5_protest")
def k_protest(cx, prince_at=0.0, city_at=1.1, objection_at=2.0, protesto_at=3.3, protestan_at=5.1):
    f = cx.f
    static_backdrop(f, 0.28, (PETROL, "#6B3F1E", 0.26))
    dust2(f, cx.t, n=50)
    with push(cx, 1.0, 1.05):
        # sol: birkaç prens (kalkanlar)
        pk = cx.amt(prince_at, 0.4)
        for i in range(4):
            k = cx.amt(prince_at, 0.5, off=0.14 * i)
            if k <= 0:
                continue
            x = 250 + i * 150
            y = 360 + (30 if i % 2 else 0)
            draw_icon2(f, "shield", x, y - (1 - ease_out(k)) * 40, size=150, metal=["gold", "silver", "bronze", "gold"][i], alpha=k, glow=0.12)
        if pk > 0:
            f.text("BİRKAÇ PRENS", 400, 510, face="title_m", size=34, color="#E7D5A0", align="c", track=8, alpha=pk)
        # sağ: 14 şehir
        ck = cx.amt(city_at, 0.6)
        if ck > 0:
            v = int(round(14 * ease_out(clamp((cx.t - cx.at(city_at)) / 0.9), 2)))
            draw_icon2(f, "tower", 1160, 360, size=170, metal="bronze", alpha=ck, glow=0.1)
            big_gold(f, str(max(1, v)), 1430, 400, size=190, alpha=ck, track=4)
            f.text("ŞEHİR", 1430, 470, face="title_m", size=44, color="#E0C682", align="c", track=18, alpha=ck)
        # itiraz: ünlem / ok
        ok = cx.amt(objection_at, 0.5)
        if ok > 0:
            tag(f, "İTİRAZ", 960, 620, size=34, alpha=ok, track=14, color="#F3C9A0", edge="#C0392B")
        # PROTESTO → PROTESTAN (kök korunur, ek değişir)
        y = 800
        size = 134
        track = 10
        stem = "PROTEST"
        w_stem = sk.text_width(stem, "title", size, track)
        w_o = sk.text_width("O", "title", size, track)
        w_an = sk.text_width("AN", "title", size, track)
        wt = w_stem + track + max(w_o, w_an)
        x_stem = W / 2 - wt / 2 + w_stem / 2
        pa = cx.amt(protesto_at, 0.7)
        if pa > 0:
            swap = cx.amt(protestan_at, 0.55)
            gold2(f, stem, x_stem, y, face="title", size=size, track=track, alpha=pa, glow=0.3 * pa)
            xo = W / 2 - wt / 2 + w_stem + track + (w_o / 2 if swap < 1 else 0)
            if swap < 1:
                gold2(f, "O", W / 2 - wt / 2 + w_stem + track + w_o / 2, y, face="title", size=size, track=track, alpha=pa * (1 - swap))
            if swap > 0:
                gold2(f, "AN", W / 2 - wt / 2 + w_stem + track + w_an / 2, y, face="title", size=size, track=track, alpha=swap, glow=0.5 * swap, scale=1.0 + (1 - swap) * 0.25)
        la = cx.amt(protesto_at, 0.5, off=0.15)
        if la > 0 and cx.amt(protestan_at, 0.4) < 1:
            f.text("PROTESTO ETTİ", 960, 905, face="cap_i", size=36, color="#B9A674", align="c", track=6, alpha=la * (1 - cx.amt(protestan_at, 0.4)))
    f.vig(0.6)


# ───────────────────────────── s6: Augsburg'da yazılı inanç beyanı imparatora sunulur ─────────────────────────────
@SH.kind("c5_confession")
def k_confession(cx, year_at=0.0, city_at=1.4, seal_at=2.7, write_at=3.4, offer_at=5.0):
    f = cx.f
    static_backdrop(f, 0.28, (PETROL, CRIM, 0.26))
    dust2(f, cx.t, n=50)
    with push(cx, 1.0, 1.04, pan=(-14, 0)):
        # sağda: taç ve taht
        ok = cx.amt(offer_at, 0.9)
        glow(f, 1610, 560, 380, "#FFB347", 0.18 + 0.12 * ok)
        draw_icon2(f, "imperial_crown", 1610, 470, size=300, metal="gold", alpha=0.92, glow=0.3 + 0.2 * ok)
        f.rrect(1470, 668, 280, 36, 8, color="#5A141A")
        f.rrect(1470, 668, 280, 36, 8, style="stroke", sw=2, color="#C9962B", alpha=0.8)
        f.rrect(1430, 704, 360, 30, 8, color="#3A0E12")
        # solda: yıl + şehir + etiket
        ya = cx.amt(year_at, 0.8)
        if ya > 0:
            gold2(f, "1530", 330, 470, face="title", size=170, track=12, alpha=ya, glow=0.3 * ya)
        ca = cx.amt(city_at, 0.7)
        if ca > 0:
            f.text("AUGSBURG", 330, 570, face="title_m", size=58, color="#F0DDA0", align="c", track=18, alpha=ca, shadow=(2, 3, 4, "#000000"))
        ta = cx.amt(seal_at, 0.6, off=-0.2)
        if ta > 0:
            tag(f, "PROTESTANLAR", 330, 700, size=30, alpha=ta, track=10, color="#9ED3DA", edge="#3F8C96", icon="b_flame", icon_metal="teal")
        # belge: ortadan tahta doğru sunulur
        a = cx.amt(year_at, 0.8)
        slide = ease_io(clamp((cx.t - cx.at(offer_at)) / 1.0))
        px = lerp(960, 1170, slide)
        py = 540 + (1 - ease_out(a)) * 120 - 50 * math.sin(math.pi * slide)
        sc_ = 1.0 - 0.22 * slide
        with paper(f, px, py, 700, 820, rot=-0.03 + 0.05 * slide, sc=sc_, alpha=a, seed=83):
            reveal(f, "AUGSBURG İTİRAFI", 0, -410 + 108, clamp((cx.t - cx.at(city_at)) / 1.0), face="fell", size=54, align="c", alpha=a)
            f.line(-230, -410 + 132, 230, -410 + 132, color=INK, sw=2, alpha=0.5 * a)
            scribbles(f, -280, -410 + 200, 560, 11, prog=clamp((cx.t - cx.at(write_at)) / 1.5), seed=33, line_h=52, thick=6.6, alpha=0.62 * a)
            SH.wax_seal(f, 200, 300, 64, color="#1E5560", t=cx.amt(seal_at, 0.35), alpha=a, mono="P")
    f.vig(0.6)


# ───────────────────────────── s6b: ana yazar Luther değil, Melanchthon ─────────────────────────────
@SH.kind("c5_authors")
def k_authors(cx, at=0.0, luther_at=1.4, mel_at=2.4, size=540, y=H * 0.46):
    f = cx.f
    static_backdrop(f, 0.28, (PETROL, "#6B4A12", 0.28, y))
    dust2(f, cx.t, n=55)
    a = cx.amt(at, 0.8)
    lk = cx.amt(luther_at, 0.6)
    mk = cx.amt(mel_at, 0.7)
    gap = 680
    for i, (key, name, role) in enumerate((("luther", "LUTHER", None), ("melanchthon", "MELANCHTHON", None))):
        x = W / 2 + (-gap / 2 if i == 0 else gap / 2)
        sl = (1 - ease_out(a)) * (-120 if i == 0 else 120)
        dim = (1 - 0.62 * lk) if i == 0 else (0.62 + 0.38 * mk)
        sc = (0.94 + 0.06 * ease_out(a)) * (1.0 + (0.05 * mk if i == 1 else -0.03 * lk))
        gl = (cx.t * 0.25 + 0.3 * i) % 2.0
        draw_medal2(f, key, x + sl, y, size * sc, "teal", flip=(i == 0), alpha=a * dim, tilt=(0.18 if i == 0 else -0.18) * math.sin(cx.t * 0.5 + i) + (0.12 if i == 0 else -0.12),
                      glint=(gl if (gl < 1 and i == 1 and mk > 0.5) else None))
        fit_plate(f, name, role, x, y + size * 0.53, w=620, t=cx.amt(at, 0.6, off=0.3) * (dim if i == 0 else 1.0))
    # Luther: üstü çizilir
    if lk > 0:
        draw_icon2(f, "b_forbid", W / 2 - gap / 2, y, size=300 * (1.2 - 0.2 * ease_out(lk)), metal="crimson", alpha=0.9 * lk, glow=0.2)
    # Melanchthon: ana yazar etiketi + kalem
    if mk > 0:
        glow(f, W / 2 + gap / 2, y - 60, 330, "#FFD27A", 0.20 * mk)
        draw_icon2(f, "quill", W / 2 + gap / 2 + 220, y - 230, size=190, metal="gold", alpha=mk, rot=0.3, glow=0.3)
        tag(f, "ANA YAZAR", W / 2 + gap / 2, y - size * 0.62, size=32, alpha=mk, track=12, color="#F4DD92")
    f.vig(0.58)


# ───────────────────────────── s7a: dinledi ama kabul etmedi ─────────────────────────────
@SH.kind("c5_refuse")
def k_refuse(cx, at=0.0, listen_at=0.6, no_at=1.4, stamp_at=1.6, key="karl_olgun"):
    f = cx.f
    static_backdrop(f, 0.28, (CRIM, PETROL, 0.28))
    dust2(f, cx.t, n=50)
    a = cx.amt(at, 0.8)
    with push(cx, 1.0, 1.04):
        # Karl: sonunda arkasını döner (yatay ölçek 1 → −1)
        k = clamp((cx.t - cx.at(no_at)) / 0.7)
        sx = math.cos(math.pi * ease_io(k))
        mx, my, ms = 560, 470, 540
        f.c.save()
        f.c.translate(mx, my)
        f.c.scale(sx if abs(sx) > 0.03 else 0.03, 1.0)
        f.c.translate(-mx, -my)
        draw_medal2(f, key, mx, my, ms * (0.94 + 0.06 * ease_out(a)), "gold", False, alpha=a, tilt=0.0)
        f.c.restore()
        fit_plate(f, "V. KARL", None, mx, my + ms * 0.53, w=420, t=cx.amt(at, 0.6, off=0.3))
        # belge (sağda) ve ses halkaları
        yy = 470 + (1 - ease_out(a)) * 100
        with paper(f, 1370, yy, 560, 720, rot=0.03, alpha=a, seed=83):
            f.text("AUGSBURG İTİRAFI", 0, -360 + 96, face="fell", size=44, color=INK, align="c", alpha=a)
            f.line(-190, -360 + 118, 190, -360 + 118, color=INK, sw=2, alpha=0.5 * a)
            scribbles(f, -220, -360 + 180, 440, 10, prog=clamp(a * 1.4), seed=33, line_h=52, thick=6.4, alpha=0.6 * a)
            SH.wax_seal(f, 150, 270, 56, color="#1E5560", t=1.0, alpha=a, mono="P")
        la = cx.amt(listen_at, 0.5)
        if la > 0:
            for i in range(3):
                ph = clamp((cx.t - cx.at(listen_at) - i * 0.22) / 0.9)
                if ph <= 0 or ph >= 1:
                    continue
                r = 70 + 70 * i + 60 * ph
                p = skia.Path()
                p.addArc(skia.Rect.MakeLTRB(1080 - r, 470 - r, 1080 + r, 470 + r), 150, 60)
                f.path(p, style="stroke", sw=5, color="#F0D27A", alpha=0.8 * (1 - ph))
            tag(f, "DİNLEDİ", 960, 830, size=30, alpha=la * (1 - cx.amt(no_at, 0.4)), track=12)
    sa = cx.amt(stamp_at, 0.3)
    if sa > 0:
        stamp2(f, "KABUL EDİLMEDİ", 1360, 560, rot=-0.13, size=52, t=sa, seed=19, fill_bg="#150D08")
    f.vig(0.6)


# ───────────────────────────── s7b: Şmalkalden Birliği ─────────────────────────────
@SH.kind("c5_league")
def k_league(cx, shield_at=0.0, name_at=1.0, close_at=1.9, flash_at=2.5, n=8):
    f = cx.f
    static_backdrop(f, 0.28, (PETROL, "#6B3F1E", 0.30))
    dust2(f, cx.t, n=50)
    cxm, cym = W / 2, 520
    rx, ry = 560, 300
    with push(cx, 1.0, 1.05):
        pts = []
        for i in range(n):
            ang = math.radians(-90 + 360 * i / n + 22.5)
            pts.append((cxm + rx * math.cos(ang), cym + ry * math.sin(ang)))
        ck = clamp((cx.t - cx.at(close_at)) / 0.9)
        # zincir: ardışık kalkanlar arası
        for i in range(n):
            p0, p1 = pts[i], pts[(i + 1) % n]
            seg = clamp(ck * n - i)
            if seg > 0:
                mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
                bend = 0.0
                chain_links(f, p0, p1, bend=bend, prog=seg, color="#8FD0D8", link=34, alpha=0.95, sw=6)
        for i, (x, y) in enumerate(pts):
            k = cx.amt(shield_at, 0.5, off=0.1 * i)
            if k <= 0:
                continue
            glow(f, x, y, 120, PETROL_L, 0.22 * k)
            draw_icon2(f, "shield", x, y - (1 - ease_out(k)) * 40, size=170 * (0.8 + 0.2 * back_out(k)), metal="teal", alpha=k, glow=0.2)
        na = cx.amt(name_at, 0.8)
        if na > 0:
            gold2(f, "ŞMALKALDEN", cxm, cym - 10, face="title", size=96, track=14, alpha=na, glow=0.3 * na, scale=1.0 + (1 - na) * 0.05)
            gold2(f, "BİRLİĞİ", cxm, cym + 100, face="title", size=96, track=18, alpha=cx.amt(name_at, 0.8, off=0.35), glow=0.3)
    fl = cx.amt(flash_at, 0.3) * (1 - cx.amt(flash_at, 0.8, off=0.3))
    if fl > 0:
        glow(f, cxm, cym, 900, "#9FE0E8", 0.45 * fl)
    f.vig(0.6)


# ───────────────────────────── s8: ancak cepheler yatışınca, 1546'da savaş ─────────────────────────────
@SH.kind("c5_wait")
def k_wait(cx, at=0.0, fr_at=1.0, ot_at=1.4, calm_at=2.8, war_at=3.95, a0=1520, a1=1548):
    f = cx.f
    static_backdrop(f, 0.25, ("#6B3F1E", CRIM, 0.2))
    dust2(f, cx.t, n=45)
    x0, x1, y = 170, 1750, 640
    def X(yr):
        return x0 + (yr - a0) / (a1 - a0) * (x1 - x0)
    k = ease_out(clamp((cx.t - cx.at(at)) / 1.2))
    f.line(x0, y, x0 + (x1 - x0) * k, y, color="#C9962B", sw=5, alpha=0.9)
    for yr in range(a0, a1 + 1):
        xx = X(yr)
        if xx > x0 + (x1 - x0) * k:
            break
        L = 22 if yr % 10 == 0 else (14 if yr % 5 == 0 else 8)
        f.line(xx, y - L, xx, y + L, color="#C9962B", sw=2.2, alpha=0.75)
    evs = [(1521, "WORMS", 0.4, -1), (1529, "SPEYER", 0.7, 1), (1530, "AUGSBURG", 1.0, -1)]
    for (yr, lab, ta, up) in evs:
        kk = cx.amt(at, 0.5, off=ta)
        if kk <= 0:
            continue
        xx = X(yr)
        f.line(xx, y, xx, y + up * 96 * kk, color="#B9A674", sw=2.5, alpha=0.9 * kk)
        f.circle(xx, y, 10 * kk, color="#F0D27A", alpha=kk)
        f.text(str(yr), xx, y + up * 176 + (0 if up < 0 else 30), face="title", size=34, color="#CDBB86", align="c", track=3, alpha=kk)
        f.text(lab, xx, y + up * 120 + (0 if up < 0 else 28), face="cap_b", size=28, color="#E7D5A0", align="c", alpha=kk, track=4)
    # cepheler: Fransa ve Osmanlı (önce kızgın, 'yatışınca' soluk)
    calm = cx.amt(calm_at, 0.9)
    for (ic, metal, lab, ta, xyr) in (("fleur", "royal", "FRANSA", fr_at, 1535), ("crescent", "forest", "OSMANLI", ot_at, 1541)):
        kk = cx.amt(ta, 0.6)
        if kk <= 0:
            continue
        xx = X(xyr)
        hot = (1 - calm)
        glow(f, xx, 400, 150, "#C0392B", 0.35 * hot * kk)
        draw_icon2(f, ic, xx, 400 - 6 * math.sin(cx.t * 3 + xyr) * hot, size=170, metal=metal, alpha=kk * (0.4 + 0.6 * hot), glow=0.25 * hot)
        f.text(lab, xx, 525, face="title_m", size=30, color="#E7D5A0", align="c", track=8, alpha=kk * (0.5 + 0.5 * hot))
    if calm > 0:
        tag(f, "YATIŞTI", (X(1535) + X(1541)) / 2, 330, size=32, alpha=calm, track=14, color="#B7D8C4", edge="#4FA57A")
    # 1546: savaş
    wk = cx.amt(war_at, 0.5)
    if wk > 0:
        xx = X(1546)
        glow(f, xx, y, 200, "#FF8A2A", 0.45 * wk)
        f.line(xx, y, xx, y - 150 * wk, color="#C0392B", sw=4, alpha=wk)
        draw_icon2(f, "swords", xx, y - 220, size=210 * (0.7 + 0.3 * back_out(wk)), metal="crimson", alpha=wk, glow=0.35)
        gold2(f, "1546", xx, y + 120, face="title", size=84, track=8, alpha=wk, glow=0.35)
        f.text("SAVAŞ", xx, y + 176, face="title_m", size=40, color="#F0DDA0", align="c", track=16, alpha=cx.amt(war_at, 0.5, off=0.25))
    f.vig(0.6)


# ───────────────────────────── s10: Tiziano — altın çerçevede atlı imparator ─────────────────────────────
def _frame_gold(f, x, y, w, h, alpha=1.0):
    """Süslü altın tablo çerçevesi (x,y = merkez)."""
    t = 36
    for k_, (inset, col) in enumerate(((0, "#4A3210"), (6, "#C9962B"), (14, "#F4DC8C"), (24, "#B88A3A"), (32, "#6B4A12"))):
        f.rrect(x - w / 2 + inset, y - h / 2 + inset, w - 2 * inset, h - 2 * inset, 8, style="stroke", sw=max(2, t - 2 * inset if k_ == 0 else 5), color=col, alpha=alpha)
    f.rrect(x - w / 2 - 4, y - h / 2 - 4, w + 8, h + 8, 10, style="stroke", sw=3, color="#2A1A0C", alpha=0.8 * alpha)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx_, cy_ = x + sx * (w / 2 - 6), y + sy * (h / 2 - 6)
            f.circle(cx_, cy_, 26, shader=f.rad(cx_ - 6, cy_ - 8, 34, [("#FBE9A6", 0.0), ("#C9962B", 0.6), ("#5A3E12", 1.0)]), alpha=alpha)
            for a_ in range(8):
                ang = a_ * math.pi / 4
                f.line(cx_ + math.cos(ang) * 14, cy_ + math.sin(ang) * 14, cx_ + math.cos(ang) * 40, cy_ + math.sin(ang) * 40, color="#F4DC8C", sw=3, alpha=0.7 * alpha)
    f.rect(x - w / 2 + 36, y - h / 2 + 36, w - 72, h - 72, style="stroke", sw=2, color="#000000", alpha=0.6 * alpha)


@SH.kind("c5_titian")
def k_titian(cx, at=0.0, year_at=1.0, frame_at=2.2, symbol_at=3.0, paint_at=4.3, armor_at=5.5, alone_at=7.6):
    from rider_b import draw_rider
    f = cx.f
    static_backdrop(f, 0.25, ("#6B3F1E", "#4A1E10", 0.24))
    dust2(f, cx.t, n=50)
    a = cx.amt(at, 0.8)
    with push(cx, 1.0, 1.06, pan=(-18, 0)):
        # sol: Tiziano madalyası + etiket
        sl = (1 - ease_out(a)) * -120
        draw_medal2(f, "tiziano", 470 + sl, 440, 470 * (0.94 + 0.06 * ease_out(a)), "ivory", False, alpha=a, tilt=0.2 * math.sin(cx.t * 0.5) + 0.1)
        fit_plate(f, "TİZİANO", None, 470, 700, w=460, t=cx.amt(at, 0.6, off=0.35))
        yk = cx.amt(year_at, 0.7)
        if yk > 0:
            tag(f, "BİR YIL SONRA", 470, 860, size=34, alpha=yk, track=14, color="#F4DD92")
        # sağ: altın çerçeve
        fk = cx.amt(frame_at, 0.9)
        fx_, fy_, fw, fh = 1250, 575, 620, 780
        if fk > 0:
            glow(f, fx_, fy_, 560, "#FFB347", 0.18 * fk)
            # tuval: alacakaranlık gökyüzü + uzak ağaçlar
            f.c.save()
            f.c.clipRect(skia.Rect.MakeXYWH(fx_ - fw / 2 + 18, fy_ - fh / 2 + 18, fw - 36, fh - 36))
            f.rect(fx_ - fw / 2, fy_ - fh / 2, fw, fh, shader=f.lin(0, fy_ - fh / 2, 0, fy_ + fh / 2, [("#2A3A4A", 0.0, int(255 * fk)), ("#C0602A", 0.55, int(255 * fk)), ("#F0A858", 0.78, int(255 * fk)), ("#3A2418", 0.80, int(255 * fk)), ("#1A100A", 1.0, int(255 * fk))]))
            glow(f, fx_ - 120, fy_ + 70, 360, "#FFD9A0", 0.35 * fk)
            ST_ = __import__("stage")
            ST_.hills(f, fy_ + 170, 24, "#2A1A10", seed=3, step=60)
            ST_.pines(f, fx_ - fw / 2, fx_ + fw / 2, fy_ + 190, 120, "#150C07", seed=5, dens=60)
            # atlı: soldan fırça gibi açılır
            pk = clamp((cx.t - cx.at(paint_at)) / 2.2)
            if pk > 0:
                f.c.saveLayer(skia.Rect.MakeXYWH(fx_ - fw / 2, fy_ - fh / 2, fw, fh), None)
                draw_rider(f, fx_ - 20, fy_ + 280, 1.06, alpha=1.0)
                edge = fx_ - fw / 2 + (fw + 200) * ease_out(pk, 1.4) - 100
                sh = skia.GradientShader.MakeLinear([(edge - 140, 0), (edge, 0)], [C("#000000", 255), C("#000000", 0)], [0, 1])
                f.c.drawRect(skia.Rect.MakeXYWH(fx_ - fw / 2 - 20, fy_ - fh / 2 - 20, fw + 40, fh + 40), skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kDstIn))
                f.c.restore()
            f.c.restore()
            _frame_gold(f, fx_, fy_, fw, fh, alpha=fk)
            # 'zafer simgesi': defne
            sk_ = cx.amt(symbol_at, 0.7)
            if sk_ > 0:
                draw_icon2(f, "laurel", fx_ - fw / 2 - 95, fy_ - 150, size=140, metal="gold", alpha=sk_, glow=0.35)
            # zırh parıltısı
            ak = cx.amt(armor_at, 0.6) * (1 - cx.amt(armor_at, 0.9, off=1.2))
            if ak > 0:
                glow(f, fx_ + 8, fy_ + 20, 150, "#FFE2A0", 0.35 * ak)
    ak2 = cx.amt(alone_at, 0.9)
    if ak2 > 0:
        # sağdaki tek figür dışında her şey kısılır
        f.rect(0, 0, 900, H, shader=f.lin(0, 0, 900, 0, [("#000000", 0.0, int(120 * ak2)), ("#000000", 1.0, 0)]))
    f.vig(0.62)


# ───────────────────────────── s11: Zafer kısa sürdü — Moritz, eski müttefik ─────────────────────────────
@SH.kind("c5_moritz")
def k_moritz(cx, short_at=0.0, year_at=2.0, ally_at=3.5, snap_at=6.4):
    f = cx.f
    static_backdrop(f, 0.28, (PETROL, CRIM, 0.26))
    dust2(f, cx.t, n=55)
    # Faz A: defne solar
    la = cx.amt(short_at, 0.6) * (1 - cx.amt(year_at, 0.8, off=-0.4))
    if la > 0:
        fade = 1.0 - 0.7 * cx.amt(short_at, 1.6, off=0.7)
        glow(f, W / 2, 500, 420, "#FFD27A", 0.3 * la * fade)
        draw_icon2(f, "laurel", W / 2, 500, size=420, metal="gold" if fade > 0.55 else "bronze", alpha=la * (0.45 + 0.55 * fade), glow=0.3 * fade)
        f.text("ZAFER", W / 2, 840, face="title", size=64, color="#E7D5A0", align="c", track=22, alpha=la * fade)
    # Faz B: iki madalya, ortada kopan zincir
    mk = cx.amt(year_at, 0.8)
    if mk > 0:
        gap = 780
        sk_ = clamp((cx.t - cx.at(snap_at)) / 0.5)
        for i, (key, name, role, metal, flip) in enumerate((("moritz", "SAKSONYALI MORİTZ", "Eski müttefik", "teal", False), ("karl_olgun", "V. KARL", None, "gold", True))):
            x = W / 2 + (-gap / 2 if i == 0 else gap / 2)
            slide = (1 - ease_out(mk)) * (-140 if i == 0 else 140)
            shake = (math.sin(cx.t * 60) * 5 * (1 - ease_out(sk_ * 2)) * (1 if sk_ > 0 else 0))
            draw_medal2(f, key, x + slide + shake, 440, 470 * (0.94 + 0.06 * ease_out(mk)), metal, flip, alpha=mk, tilt=(0.16 if i == 0 else -0.16) * math.sin(cx.t * 0.5 + i))
            fit_plate(f, name, role, x, 700, w=560, t=cx.amt(year_at, 0.6, off=0.4))
        # zincir ortada (müttefiklik)
        ak = cx.amt(ally_at, 0.6)
        if ak > 0:
            sp = 1.0 + 0.0
            if sk_ <= 0:
                chain_links(f, (W / 2 - 150, 440), (W / 2 + 150, 440), bend=0, prog=ak, color="#F0D27A", link=36, alpha=ak, sw=7)
                glow(f, W / 2, 440, 130, "#FFD27A", 0.25 * ak)
            else:
                off = 70 * ease_out(sk_)
                chain_links(f, (W / 2 - 150 - off, 440 + 20 * sk_), (W / 2 - 22 - off, 440 + 50 * sk_), bend=0, prog=1.0, color="#F0D27A", link=36, alpha=1 - 0.4 * sk_, sw=7)
                chain_links(f, (W / 2 + 22 + off, 440 + 50 * sk_), (W / 2 + 150 + off, 440 + 20 * sk_), bend=0, prog=1.0, color="#F0D27A", link=36, alpha=1 - 0.4 * sk_, sw=7)
                glow(f, W / 2, 440, 380 * (1 - sk_) + 60, "#FF5A3A", 0.5 * (1 - sk_))
        yk = cx.amt(year_at, 0.8, off=0.1)
        if yk > 0:
            gold2(f, "1552", W / 2, 190, face="title", size=110, track=14, alpha=yk, glow=0.3 * yk)
        tg = cx.amt(ally_at, 0.6)
        if tg > 0 and sk_ <= 0:
            tag(f, "ESKİ MÜTTEFİK", W / 2, 560, size=30, alpha=tg, track=12)
        if sk_ > 0:
            draw_icon2(f, "swords", W / 2, 440, size=190 * ease_out(sk_), metal="crimson", alpha=sk_, glow=0.3)
    f.vig(0.6)


# ───────────────────────────── s13: Augsburg Barışı — Lutherciliğe yer açıldı ─────────────────────────────
@SH.kind("c5_peace")
def k_peace(cx, at=0.0, date_at=0.9, title_at=2.8, seal_at=3.8, luther_at=5.2, open_at=6.2):
    f = cx.f
    static_backdrop(f, 0.28, (PETROL, "#7A5D1E", 0.26))
    dust2(f, cx.t, n=50)
    a = cx.amt(at, 0.8)
    with push(cx, 1.0, 1.05):
        yy = 540 + (1 - ease_out(a)) * 140
        with paper(f, 960, yy, 1260, 800, rot=-0.012, alpha=a, seed=91, tone="#D9C48F"):
            reveal(f, "AUGSBURG BARIŞI", 0, -400 + 108, clamp((cx.t - cx.at(title_at)) / 1.1), face="fell", size=72, align="c", alpha=a)
            f.line(-330, -400 + 134, 330, -400 + 134, color=INK, sw=2.4, alpha=0.55 * a)
            dk = cx.amt(date_at, 0.7)
            if dk > 0:
                f.text("EYLÜL 1555", 0, -400 + 186, face="fell_i", size=44, color="#5A3A18", align="c", alpha=0.9 * dk, track=3)
            # iki niş: Katolik (dolu) ↔ Lutherci (açılacak yer)
            ny = 40
            for (nx, ic, metal, lab, ta) in ((-250, "cross", "violet", "KATOLİK", shift(date_at, 0.6)), (250, "cross", "teal", "LUTHERCİLİK", luther_at)):
                k = cx.amt(ta, 0.6)
                # niş çerçevesi
                path = skia.Path()
                path.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(nx - 170, ny - 190, 340, 400), 170, 170))
                if nx > 0:
                    ok = cx.amt(open_at, 0.7)
                    dash = skia.DashPathEffect.Make([14, 10], 0)
                    pa = f.paint(mix("#7A5518", "#C9962B", ok), style="stroke", sw=4, alpha=0.9)
                    if ok < 1:
                        pa.setPathEffect(dash)
                    f.c.drawPath(path, pa)
                    if ok > 0:
                        f.c.drawPath(path, f.paint("#F0D27A", style="stroke", sw=7, alpha=0.55 * ok, blur=6))
                else:
                    f.c.drawPath(path, f.paint("#7A5518", style="stroke", sw=4, alpha=0.9))
                if k > 0:
                    draw_icon2(f, ic, nx, ny + 10 - (1 - ease_out(k)) * 30, size=230 * (0.85 + 0.15 * back_out(k)), metal=metal, alpha=k, glow=0.12)
                    f.text(lab, nx, ny + 260, face="fell", size=40, color=INK, align="c", track=4, alpha=0.9 * k)
            SH.wax_seal(f, 500, -210, 62, color="#8E1F26", t=cx.amt(seal_at, 0.35), alpha=a, mono="A")
    f.vig(0.6)


# ───────────────────────────── Mühlberg: Elbe geçişi — savaş planı (parşömen üzerinde) ─────────────────────────────
INK_M = "#2A1A0C"


def unit_block(f, x, y, w, h, col, kind="inf", alpha=1.0, rot=0.0):
    """Savaş planı birlik kutusu (piyade: çapraz; süvari: çizgi)."""
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(math.degrees(rot))
    f.rect(-w / 2 + 3, -h / 2 + 4, w, h, color="#000000", alpha=0.25 * alpha, blur=4)
    f.rect(-w / 2, -h / 2, w, h, color=col, alpha=0.92 * alpha)
    f.rect(-w / 2, -h / 2, w, h, style="stroke", sw=3, color=INK_M, alpha=0.95 * alpha)
    if kind == "inf":
        f.line(-w / 2, -h / 2, w / 2, h / 2, color=INK_M, sw=2.2, alpha=0.7 * alpha)
        f.line(-w / 2, h / 2, w / 2, -h / 2, color=INK_M, sw=2.2, alpha=0.7 * alpha)
    else:
        f.line(-w / 2, h / 2, w / 2, -h / 2, color=INK_M, sw=3, alpha=0.8 * alpha)
    f.c.restore()


@SH.kind("c5_plan")
def k_plan(cx, at=0.0, date_at=0.0, river_at=0.8, city_at=1.4, army_at=1.9, fog_at=3.4, cross_at=4.9):
    """Mühlberg: parşömen savaş planı — Elbe, iki yakada birlikler, sis, geçiş oku."""
    f = cx.f
    static_backdrop(f, 0.26, ("#4A2A18", PETROL, 0.2))
    dust2(f, cx.t, n=45)
    a = cx.amt(at, 0.8)
    with push(cx, 1.0, 1.05, pan=(-10, 0)):
        yy = 560 + (1 - ease_out(a)) * 120
        with paper(f, 960, yy, 1520, 820, rot=-0.01, alpha=a, seed=57, tone="#BCA270"):
            # tarih (sol üst)
            dk = cx.amt(date_at, 0.8)
            f.text("24 NİSAN 1547", -690, -410 + 112, face="fell", size=60, color=INK, align="l", track=4, alpha=0.95 * dk)
            f.line(-700, -410 + 138, 700, -410 + 138, color=INK, sw=2, alpha=0.5 * a)
            # nehir: mürekkep fırçası
            rk = ease_out(clamp((cx.t - cx.at(river_at)) / 1.5), 2)
            if rk > 0:
                pts = [(-150, -350), (-90, -240), (10, -120), (110, 0), (230, 110), (350, 225), (470, 330)]
                path = sk.smooth_path(pts, False, 0.5)
                pm = skia.PathMeasure(path, False)
                part = skia.Path()
                pm.getSegment(0, pm.getLength() * rk, part, True)
                f.path(part, style="stroke", sw=30, color="#2F6F9A", alpha=0.20 * a)
                f.path(part, style="stroke", sw=18, color="#3F7FA8", alpha=0.95 * a)
                f.path(part, style="stroke", sw=4, color="#1F4A66", alpha=0.6 * a)
                f.text("ELBE", 340, 120, face="fell_i", size=46, color="#1F4A66", align="c", alpha=0.95 * rk)
            # Mühlberg işareti
            ck = cx.amt(city_at, 0.7)
            if ck > 0:
                f.circle(112, 2, 13, color="#8E1F26", alpha=ck)
                f.circle(112, 2, 13, style="stroke", sw=3, color=INK_M, alpha=ck)
                f.text("MÜHLBERG", 84, 38, face="title_m", size=46, color=INK_M, align="r", track=8, alpha=ck)
            # birlikler
            ak = cx.amt(army_at, 0.7)
            if ak > 0:
                for i, (x, y) in enumerate(((-260, 170), (-170, 230), (-80, 160), (-330, 270), (-210, 330))):
                    unit_block(f, x, y + (1 - ease_out(ak)) * 14, 74, 40, "#B4423A", "inf" if i % 2 == 0 else "cav", ak, rot=-0.5)
                for i, (x, y) in enumerate(((190, -170), (290, -250), (370, -110), (110, -270))):
                    unit_block(f, x, y + (1 - ease_out(ak)) * 14, 74, 40, "#2E7A86", "inf" if i % 2 == 0 else "cav", ak, rot=-0.5)
            if ak > 0:
                f.text("şematik çizim", 700, 382, face="fell_i", size=30, color=INK_M, align="r", alpha=0.62 * ak)
            # geçiş oku
            xk = clamp((cx.t - cx.at(cross_at)) / 1.5)
            if xk > 0:
                curve_arrow(f, (-110, 215), (300, -170), bend=-120, prog=ease_io(xk), color="#8E1F26", sw=12, alpha=0.95, shadow=False)
            # sis
            fk = cx.amt(fog_at, 1.6)
            if fk > 0:
                f.c.save()
                f.c.clipRect(skia.Rect.MakeXYWH(-740, -400, 1480, 800))
                for i in range(14):
                    x = (((i * 211 + cx.t * (16 + 3 * (i % 4))) % 1900) - 950)
                    y = -330 + (i * 137) % 700
                    r = 230 + (i % 5) * 45
                    f.circle(x, y, r, shader=f.rad(x, y, r, [("#8FA2AC", 0.0, int(105 * fk)), ("#8FA2AC", 0.6, int(52 * fk)), ("#8FA2AC", 1.0, 0)]))
                f.c.restore()
    f.vig(0.62)
