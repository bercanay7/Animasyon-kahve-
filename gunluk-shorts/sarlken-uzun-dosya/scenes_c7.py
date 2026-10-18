"""Bölüm 7 — Sultan: Hiç Karşılaşmadılar (c7): Süleyman ve Şarlken, Mohaç, Viyana 1529, Güns 1532, 1547 ateşkesi. Yazar: bölüm yazarı C."""
import math
from shots import shot
import scenes_lib  # noqa: F401
import icons       # noqa: F401
import sk
import stage_c678 as X
import stage_c6    # noqa: F401  (Paper ortak)
import stage_c7    # noqa: F401  özel çekim türleri (c7_*)
import shots as SH
import stage as ST
from sk import H, W, clamp, ease_io, ease_out, back_out

A = X.W


# ───────────── harita kaplamaları ─────────────
def _dist_extra(cx, cam, mv):
    """İstanbul ↔ Brüksel: iki madalya uçlarda, aralarında uzun kesikli çizgi ve HİÇ KARŞILAŞMADILAR."""
    f = cx.f
    xi, yi = cam.ll(28.98, 41.01)
    xb, yb = cam.ll(4.35, 50.85)
    kl = ease_io(clamp((cx.t - cx.at(("c7s2", "Bildiğimiz", 0.2))) / 1.4))
    if kl > 0:
        xe, ye = xi + (xb - xi) * kl, yi + (yb - yi) * kl
        p = f.paint("#F0D27A", style="stroke", sw=5, alpha=0.9)
        p.setPathEffect(__import__("skia").DashPathEffect.Make([16, 14], -cx.t * 30))
        f.c.drawLine(xi, yi, xe, ye, p)
    for (x, y, key, metal, flip, at_, name) in ((xi, yi, "suleyman", "forest", True, ("c7s2", "Bildiğimiz", 0.0), "SÜLEYMAN"), (xb, yb, "karl_olgun", "gold", False, ("c7s2", "Bildiğimiz", 0.15), "ŞARLKEN")):
        k = cx.amt(at_, 0.7)
        if k > 0:
            f.circle(x, y - 150, 150, shader=f.rad(x, y - 150, 150, [("#000000", 0.0, int(140 * k)), ("#000000", 1.0, 0)]))
            SH.draw_medal(f, key, x, y - 150 + (1 - k) * 20, 250 * (0.9 + 0.1 * ease_out(k)), metal, flip, alpha=k, tilt=0.1 * math.sin(cx.t * 0.6))
            f.text(name, x, y + 52, face="title_m", size=28, color="#F0DDA0", align="c", track=6, alpha=k, shadow=(2, 2, 3, "#000000"))
    kh = cx.amt(("c7s2", "Bildiğimiz", -0.1), 0.6)
    if kh > 0:
        f.text("BİLDİĞİMİZ KADARIYLA", W / 2, 118, face="cap_i", size=36, color="#C9B27A", align="c", track=10, alpha=kh, shadow=(2, 2, 3, "#000000"))
    km = cx.amt(("c7s2", "hiç", -0.1), 0.6)
    if km > 0:
        X.chip(f, "HİÇ KARŞILAŞMADILAR", (xi + xb) / 2, (yi + yb) / 2 - 110, k=km, size=40, edge="#F0D27A", color="#F4DD92", padx=40, h=92)
        X.ic(f, "question", (xi + xb) / 2, (yi + yb) / 2 + 20, size=110, metal="silver", alpha=0.85 * km)


def _route_medal(key, metal, pts, at, dur, size=210, flip=False, tag=None):
    """Rota üzerinde ilerleyen madalya. tag=(metin,): varışta madalyanın yanına (sağ) kent adı yazılır (madalya kent etiketini örtmesin)."""
    def fn(cx, cam, mv):
        pr = ease_io(clamp((cx.t - cx.at(at)) / dur))
        if pr <= 0:
            return
        (x, y), ang = mv.point_on(cam, pts, pr)
        cx.f.circle(x, y, size * 0.7, shader=cx.f.rad(x, y, size * 0.7, [("#000000", 0.0, 110), ("#000000", 1.0, 0)]))
        SH.draw_medal(cx.f, key, x, y, size * (0.9 + 0.1 * ease_out(clamp(pr * 6))), metal, flip, alpha=clamp(pr * 8), tilt=0.1)
        if tag and pr > 0.82:
            ka = clamp((pr - 0.82) / 0.18)
            cx.f.text(tag[0], x + size * 0.56, y + 10, face="title_m", size=30, color="#F6E6B8", align="l", track=5, alpha=ka, shadow=(2, 2, 3, "#000000"))
    return fn


def _extras(*fns):
    def fn(cx, cam, mv):
        for g in fns:
            g(cx, cam, mv)
    return fn


def _mohac_water(cx):
    """Lajos madalyası: kaçarken derede boğuldu — alttan yükselen karanlık su + halkalar."""
    f = cx.f
    k = cx.amt(("c7s3", "kaçarken", -0.1), 1.8)
    if k <= 0:
        return
    k2 = cx.amt(("c7s3", "derede", -0.2), 0.8)
    ytop = H - k * 0.30 * H
    pts = [(x, ytop + math.sin(x * 0.012 + cx.t * 2.0) * 9 + math.sin(x * 0.031 - cx.t * 3.1) * 4) for x in range(-20, W + 60, 40)]
    pts += [(W + 20, H + 20), (-20, H + 20)]
    f.path(sk.poly_path(pts), shader=f.lin(0, ytop, 0, H, [("#1B4256", 0.0, 175), ("#071018", 1.0, 240)]))
    f.path(sk.poly_path(pts[:-2], False), style="stroke", sw=3, color="#9CC4D8", alpha=0.55)
    if k2 > 0:
        for i in range(3):
            u = ((cx.t - cx.at(("c7s3", "derede", -0.2))) * 0.6 + i / 3) % 1.0
            f.oval(W * 0.34, ytop + 6, 40 + u * 260, 8 + u * 46, style="stroke", sw=3, color="#BFE0F0", alpha=0.6 * (1 - u) * k2)


def _viyana_weather(cx):
    """Yağmur (sahnenin kendisi) → çamur (zemin kararır) → erken kar (zemin ağarır, taneler artar) → geri çekilme oku."""
    f = cx.f
    km = cx.amt(("c7s8", "çamur", -0.15), 1.0)
    ks = cx.amt(("c7s8", "erken", -0.1), 1.4)
    if km > 0:
        f.rect(0, 640, W, H - 640, shader=f.lin(0, 640, 0, H, [("#2A1C10", 0.0, 0), ("#2A1C10", 1.0, int(120 * km))]))
    if ks > 0:
        f.rect(0, 560, W, H - 560, shader=f.lin(0, 560, 0, H, [("#F2F6F8", 0.0, 0), ("#F2F6F8", 1.0, int(78 * ks))]))
        sk.snow(f, cx.t, n=int(30 + 120 * ks), alpha=0.85 * ks)
    k = cx.amt(("c7s8", "Ekim", -0.1), 0.7)
    if k > 0:
        X.scrim(f, W / 2, 112, w=900, h=150, a=0.36 * k)
        SH.kicker(f, "EKİM ORTASI", W / 2, 122, alpha=k, size=36, track=14, face="title_m", color="#E8CF8A")
    kg = cx.amt(("c7s8", "geri", -0.15), 0.6)
    if kg > 0:
        X.chip(f, "GERİ ÇEKİLME", W / 2, 205, k=kg, size=40, edge="#B02A2A", color="#F8E2D8", padx=40, h=88)
        pr = ease_out(clamp((cx.t - cx.at(("c7s8", "geri", -0.1))) / 1.5))
        X.arrow(f, (640, 905), (1560, 905), pr, color="#6FBF8A", width=10, bend=-60, alpha=0.9)


SHOTS = [
    # s1 — Doğuda başka bir imparator
    shot("medal", a=("c7s1", -0.2), key="suleyman", metal="forest", name="KANUNİ SULTAN SÜLEYMAN", role="Osmanlı Sultanı", pos="c", size=700,
         at=("c7s1", "Doğuda", -0.1), plate_at=("c7s1", "Kanuni", -0.3), extra=lambda cx: X.tone(cx.f, "#2F6B4A", 0.16), label="suleyman"),

    # s2 — aynı yıllarda hüküm sürdüler
    shot("c7_hukum", a=("c7s2", -0.2), tr=("fade", 0.7), at_axis=("c7s2", "İkisi", -0.1), at_bars=("c7s2", "aynı", -0.1), at_overlap=("c7s2", "hüküm", 0.0), label="ayni_yillar"),

    # s2b — hiç yüz yüze gelmediler: uzaklık
    shot("map", a=("c7s2", "kadarıyla", 0.1), tr=("fade", 0.7), cams=[(0.0, (16.8, 47.6, 1.18)), (("c7s3", -0.3), (16.8, 47.4, 1.26))],
         regions=[dict(name="osmanli_1520", color="osmanli", at=0.0, alpha=0.55), dict(name="ispanya", color="ispanya", at=0.2, alpha=0.6),
                  dict(name="hollanda", color="burgonya", at=0.3, alpha=0.6), dict(name="avusturya", color="avusturya", at=0.4, alpha=0.6)],
         cities=[dict(lon=28.98, lat=41.01, name=None, kind="capital", at=0.2, color="#9FE0B4"),
                 dict(lon=4.35, lat=50.85, name=None, kind="capital", at=0.3, color="#F0C080")],
         extra=_dist_extra, label="uzaklik"),

    # s3 — Mohaç: Macar ordusu yenildi
    shot("c678_sahne", a=("c7s3", -0.3), tr=("whip", 0.55), scene="field",
         cams=[(0.0, X.fcam(0, .32, 1.12)), (("c7s3", "yenildi.", -0.3), X.fcam(0, .50, 1.45))],
         p=dict(tag="c7_mohac", ground="marsh", weather="dusk", river=True, smoke=0.6,
                armies=[dict(side="#B5483A", kind="cavalry", x=0.22, row=0, n=8, dir=1, charge=0.5),
                        dict(side="#B5483A", kind="pike", x=0.12, row=1, n=12, dir=1, charge=0.4),
                        dict(side="#2F6B4A", kind="mixed", x=0.74, row=1, n=16, dir=-1, charge=0.3),
                        dict(side="#2F6B4A", kind="arquebus", x=0.86, row=2, n=12, dir=-1, fire=1.0),
                        dict(side="#2F6B4A", kind="cavalry", x=0.68, row=0, n=6, dir=-1, charge=0.45)]),
         overlay=X.ov_all(X.ov_haze(n=8, y0=560, y1=800, col="#6A4A30", a=0.30, seed=11, rmin=160, rmax=260, speed=26),
                          X.ov_date("29 AĞUSTOS 1526", ("c7s3", "29", -0.1)), X.ov_kick("MOHAÇ", ("c7s3", "Mohaç'ta,", -0.2), y=122, size=38)), label="mohac"),
    shot("medal", a=("c7s3", "Kral", -0.2), tr=("dip", 0.6), key="lajos2", metal="onyx", name="II. LAJOS", role="Macaristan Kralı", pos="l", size=700,
         at=("c7s3", "Kral", -0.1), plate_at=("c7s3", "Lajos,", -0.1), extra=_mohac_water, label="lajos"),

    # s4 — çocuğu yoktu; Ferdinand öne çıktı; soylular ikiye bölündü
    shot("c7_taht", a=("c7s4", -0.1), tr=("fade", 0.7), at_crown=("c7s4", "Çocuğu", -0.1), at_title=("c7s4", "Macaristan", -0.15), at_ferd=("c7s4", "Ferdinand", -0.45),
         at_plate=("c7s4", "Ferdinand", 0.0), label="bos_taht_ferdinand"),
    shot("map", a=("c7s4", "Macar", 1, -0.25), tr=("fade", 0.7), cams=[(0.0, (20.0, 47.2, 3.1)), (("c7s5", -0.3), (20.4, 47.0, 3.4))],
         regions=[dict(name="macar_habsburg", color="avusturya", at=0.0, alpha=0.65), dict(name="macar_osmanli", color="macar", at=("c7s4", "ikiye", -0.2), alpha=0.65),
                  dict(name="erdel", color="macar", at=("c7s4", "ikiye", -0.1), alpha=0.65)],
         labels=[dict(text="FERDİNAND", lon=17.4, lat=48.7, size=40, color="#F4C7A8", at=("c7s4", "Macar", 1, 0.1), track=10),
                 dict(text="ZAPOLYA", lon=22.6, lat=46.9, size=40, color="#E3E8B0", at=("c7s4", "ikiye", 0.0), track=10)],
         cities=[dict(lon=18.68, lat=45.99, name="MOHAÇ", kind="battle", at=0.2, side="b")],
         icons_=[dict(kind="swords", lon=19.6, lat=47.6, size=96, at=("c7s4", "bölündü", -0.2), metal="silver")], label="macar_bolunme"),

    # s5 — Zapolya Osmanlı vasalı
    shot("c7_vasal", a=("c7s5", -0.2), tr=("fade", 0.7), at_medal=("c7s5", "Rakip", -0.1), at_ott=("c7s5", "Osmanlı", -0.25), at_link=("c7s5", "Osmanlı", 0.2),
         at_chip=("c7s5", "vasalı", -0.1), label="zapolya_vasal"),

    # s6 — 1529: Viyana önünde
    shot("map", a=("c7s6", -0.2), tr=("fade", 0.5), cams=[(0.0, (23.2, 44.8, 1.55)), (("c7s6", "Kuşatma", 0.0), (21.0, 46.2, 1.85))],
         regions=[dict(name="osmanli_1520", color="osmanli", at=0.0, alpha=0.5), dict(name="avusturya", color="avusturya", at=("c7s6", "Viyana", -0.3), alpha=0.6),
                  dict(name="macar_habsburg", color="avusturya", at=("c7s6", "Viyana", -0.3), alpha=0.5)],
         routes=[dict(pts=[(28.98, 41.01), (26.56, 41.67), (23.3, 42.7), (20.46, 44.82), (19.04, 47.5), (16.37, 48.21)], at=("c7s6", "Süleyman,", -0.2), dur=2.6, color="#5FA878", width=9)],
         cities=[dict(lon=28.98, lat=41.01, name="İSTANBUL", kind="capital", at=0.0, color="#9FE0B4", side="b", size=28),
                 dict(lon=16.37, lat=48.21, name="VİYANA", kind="siege", at=("c7s6", "Viyana", -0.3), side="t", size=36)],
         date=("1529", ("c7s6", "1529'da", -0.1)),
         extra=_route_medal("suleyman", "forest", [(28.98, 41.01), (26.56, 41.67), (23.3, 42.7), (20.46, 44.82), (19.04, 47.5), (16.37, 48.21)], ("c7s6", "Süleyman,", -0.2), 2.6, size=200, flip=True),
         label="viyana_yolu"),
    shot("c678_sahne", a=("c7s6", "Kuşatma", -0.15), tr=("whip", 0.5), scene="siege",
         cams=[(0.0, (960, 560, 1.0)), (("c7s7", 0.0), (1000, 580, 1.3))],
         p=dict(tag="c7_viyana1", city="viyana", time="day", weather="clear", cannon_fire=True, fire=0.3),
         overlay=X.ov_all(X.ov_date("27 EYLÜL 1529", ("c7s6", "27", -0.1)), X.ov_kick("VİYANA", ("c7s6", "Kuşatma", -0.1), y=122, size=38, x=620)), label="viyana_kusatma"),

    # s7 — ordu büyüklüğü (modern tahmin)
    shot("c678_cift", a=("c7s7", -0.2), tr=("fade", 0.6), title="OSMANLI ORDUSU · VİYANA 1529", tone_col="#2F6B4A", y=H * 0.46, size=140, ykick=140,
         items=[dict(value=(75000, 100000), unit="asker", icon="crescent", metal="forest", at=("c7s7", "Osmanlı", -0.1), count_at=("c7s7", "yetmiş", -0.15), hide0=True, dur=1.7)],
         band=("janissary", 46, ("c7s7", "Osmanlı", 0.0)), stampt=("MODERN TAHMİN", 960, 800, ("c7s7", "modern", -0.1), 54), label="ordu_75_100bin"),

    # s8 — yağmur, çamur, erken kar → geri çekilme
    shot("c678_sahne", a=("c7s8", -0.2), tr=("whip", 0.5), scene="siege",
         cams=[(0.0, (1020, 590, 1.22)), (("c7s9", -0.4), (1240, 560, 1.0))],
         p=dict(tag="c7_viyana2", city="viyana", time="day", weather="rain", fire=0.0),
         overlay=_viyana_weather, label="yagmur_kar_cekilme"),

    # s9 — Şarlken o hafta İtalya'da
    shot("map", a=("c7s9", -0.2), tr=("wipe", 0.8), cams=[(0.0, (9.6, 45.4, 1.8)), (("c7s10", -0.4), (11.0, 45.8, 2.1))],
         regions=[dict(name="ispanya", color="ispanya", at=0.0, alpha=0.6), dict(name="papalik", color="papalik", at=("c7s9", "papadan", -0.2), alpha=0.7),
                  dict(name="avusturya", color="avusturya", at=0.0, alpha=0.5)],
         routes=[dict(pts=[(2.17, 41.39), (5.2, 42.9), (8.93, 44.41), (11.34, 44.49)], at=("c7s9", "İtalya'daydı;", -0.4), dur=2.6, color="#E8C25A", width=8)],
         cities=[dict(lon=2.17, lat=41.39, name="BARSELONA", kind="town", at=0.0, side="b", size=26),
                 dict(lon=8.93, lat=44.41, name="CENOVA", kind="town", at=("c7s9", "İtalya'daydı;", 0.3), side="b", size=26),
                 dict(lon=11.34, lat=44.49, name=None, kind="capital", at=("c7s9", "papadan", -0.3), side="r", size=30),
                 dict(lon=16.37, lat=48.21, name="VİYANA · KUŞATMA", kind="siege", at=("c7s9", "hafta", -0.2), side="t", size=28)],
         icons_=[dict(kind="imperial_crown", lon=11.34, lat=46.2, size=110, at=("c7s9", "tacını", -0.2), metal="gold", bob=5)],
         extra=_route_medal("karl_olgun", "gold", [(2.17, 41.39), (5.2, 42.9), (8.93, 44.41), (11.34, 44.49)], ("c7s9", "İtalya'daydı;", -0.4), 2.6, size=210, tag=("BOLOGNA",)),
         label="karl_italya"),

    # s10 — 1532: doğrudan imparatora; sefer günlüğü
    shot("map", a=("c7s10", -0.2), tr=("fade", 0.7), cams=[(0.0, (22.0, 45.2, 1.8)), (("c7s10", "Osmanlı", -0.2), (20.0, 46.4, 2.0))],
         regions=[dict(name="osmanli_1550", color="osmanli", at=0.0, alpha=0.5), dict(name="avusturya", color="avusturya", at=0.2, alpha=0.55),
                  dict(name="almanya", color="#7A6A3A", at=0.4, alpha=0.35, hatch=True)],
         routes=[dict(pts=[(28.98, 41.01), (23.3, 42.7), (20.46, 44.82), (19.04, 47.5), (16.54, 47.4)], at=("c7s10", "doğrudan", -0.5), dur=2.6, color="#5FA878", width=9)],
         cities=[dict(lon=28.98, lat=41.01, name="İSTANBUL", kind="capital", at=0.0, color="#9FE0B4", side="b", size=28)],
         icons_=[dict(kind="imperial_crown", lon=13.4, lat=48.6, size=120, at=("c7s10", "imparatora", -0.15), metal="gold", bob=5)],
         notes=[dict(text="HEDEF: İMPARATOR", x=210, y=120, at=("c7s10", "imparatora", -0.1), w=560, size=40)],
         date=("1532", ("c7s10", "1532'de", -0.1)), label="1532_sefer"),
    shot("c7_gunluk", a=("c7s10", "Osmanlı", -0.15), tr=("fade", 0.7), at=0.0, at_quote=("c7s10", "İspanya", -0.15), at_hl=("c7s10", "kralı”.", -0.2), label="sefer_gunlugu"),

    # s11 — Güns: küçük kale, garnizon, 25 gün
    shot("c678_sahne", a=("c7s11", -0.2), tr=("whip", 0.5), scene="siege",
         cams=[(0.0, (960, 500, 1.0)), (("c7s11", "yedi", 0.0), (1010, 305, 1.14))],
         p=dict(tag="c7_guns", city="guns", time="day", weather="clear", cannon_fire=True, fire=0.15),
         overlay=X.ov_kick("GÜNS", ("c7s11", "Güns,", -0.2), y=122, size=40, x=560), label="guns_kale"),
    shot("c678_cift", a=("c7s11", "yedi", -0.15), tr=("fade", 0.5), title="GÜNS · 1532", tone_col="#6A7A38", y=H * 0.5, size=140, ykick=140,
         items=[dict(value=(700, 800), unit="kişi", label="GARNİZON", icon="castle", metal="gold", at=("c7s11", "yedi", -0.1), dur=1.5),
                dict(value=25, unit="gün", label="ORDUYU OYALADI", icon="hourglass", metal="gold", at=("c7s11", "yirmi", -0.15), dur=1.2)], label="guns_700_800_25"),

    # s12 — iki ordu hiç karşılaşmadı
    shot("map", a=("c7s12", -0.2), tr=("fade", 0.6), cams=[(0.0, (17.2, 48.2, 3.3)), (("c7s13", -0.3), (17.2, 48.1, 3.5))],
         regions=[dict(name="avusturya", color="avusturya", at=0.0, alpha=0.30), dict(name="macar_habsburg", color="avusturya", at=0.0, alpha=0.24),
                  dict(name="macar_osmanli", color="osmanli", at=0.0, alpha=0.34)],
         cities=[dict(lon=16.37, lat=48.21, name="VİYANA", kind="town", at=0.0, side="t", size=30),
                 dict(lon=16.54, lat=47.38, name="GÜNS", kind="siege", at=0.0, side="l", size=28)],
         extra=lambda cx, cam, mv: _ordular(cx, cam, mv), label="ordular_karsilasmadi"),

    # s13 — unvan: İmparator yalnızca sultan
    shot("c7_unvan", a=("c7s13", -0.2), tr=("zoom", 0.7), at_doc=("c7s13", "Osmanlı", -0.1), at_gen=("c7s13", "genellikle", -0.1), at_karl=("c7s13", "ona", -0.25), at_imp=("c7s13", "imparator", -0.2), at_strike=("c7s13", "demedi", -0.1),
         at_king=("c7s13", "İspanya", -0.1), at_sultan=("c7s13", "yalnızca", -0.3), at_crown=("c7s13", "sultandı", -0.35), label="unvan_imparator_sultan"),

    # s14 — 1547 ateşkesi; 30.000 altın
    shot("c7_ates", a=("c7s14", -0.2), tr=("fade", 0.7), at=0.0, at_len=("c7s14", "beş", -0.1), at_seal=("c7s14", "imzalandı.", -0.2), label="ates_kes_1547"),
    shot("c678_cift", a=("c7s14", "Ferdinand,", -0.2), tr=("fade", 0.5), title="FERDİNAND ÖDEYECEKTİ", kick_at=("c7s14", "Ferdinand,", -0.1), tone_col="#C9962B", y=H * 0.5, size=170, ykick=170,
         items=[dict(value=30000, unit="altın", label="HER YIL", icon="coins", metal="gold", at=("c7s14", "Ferdinand,", 0.1), count_at=("c7s14", "otuz", -0.2), dur=1.4)], label="30bin_altin"),

    # s15 — Viyana tutuldu, Macaristan kayıp; yükü kardeşi taşıdı
    shot("map", a=("c7s15", -0.2), tr=("fade", 0.7), cams=[(0.0, (20.0, 47.2, 3.0)), (("c7s15", "Yükün", -0.3), (19.6, 47.2, 3.2))],
         regions=[dict(name="macar_habsburg", color="avusturya", at=("c7s15", "Habsburg,", -0.1), alpha=0.65),
                  dict(name="macar_osmanli", color="osmanli", at=("c7s15", "kaybetti.", -0.9), alpha=0.7), dict(name="erdel", color="osmanli", at=("c7s15", "kaybetti.", -0.7), alpha=0.6)],
         cities=[dict(lon=16.37, lat=48.21, name="VİYANA", kind="capital", at=("c7s15", "Viyana'yı", -0.2), side="t", size=34, color="#F4C7A8")],
         labels=[dict(text="TUTULDU", lon=16.0, lat=49.1, size=34, color="#F4C7A8", at=("c7s15", "tuttu;", -0.2), track=10),
                 dict(text="KAYIP", lon=20.6, lat=46.7, size=64, color="#C6F0D4", at=("c7s15", "bölümünü", -0.1), track=14)],
         label="macaristan_kayip"),
    shot("c7_yuk", a=("c7s15", "Yükün", -0.15), tr=("fade", 0.7), at_title=("c7s15", "Yükün", -0.1), at_karl=("c7s15", "çoğunu", -0.1), at_not=("c7s15", "değil,", -0.55),
         at_ferd=("c7s15", "kardeşi", -0.35), label="yuku_kardesi_tasidi"),
]


def _ordular(cx, cam, mv):
    import skia
    f = cx.f
    xa, ya = cam.ll(15.7, 48.6)       # imparatorluk ordusu (Viyana yakını)
    xo, yo = cam.ll(18.0, 46.9)       # Osmanlı ordusu (Güns yönü)
    ka = cx.amt(("c7s12", "İmparatorluk", -0.1), 0.8)
    ko = cx.amt(("c7s12", "İmparatorluk", 0.3), 0.8)
    for (x, y, k, col, rim, face) in ((xa, ya, ka, "#B02A3A", "#F6D98A", 1), (xo, yo, ko, "#2F8A5A", "#C6F0D4", -1)):
        if k <= 0:
            continue
        f.circle(x, y - 40, 150, shader=f.rad(x, y - 40, 150, [("#000000", 0.0, int(120 * k)), ("#000000", 1.0, 0)]))
        for i in range(9):
            ST.figure(f, "pikeman", x + (i - 4) * 24, y + (i % 3) * 12, 112, col=col, rim=rim, face=face, alpha=k)
    kb = cx.amt(("c7s12", "bekledi.", -0.4), 0.6)
    if kb > 0:
        X.ic(f, "hourglass", xa - 110, ya - 150, size=96, metal="gold", alpha=kb)
        X.chip(f, "BEKLEDİ", xa - 110, ya - 230, k=kb, size=30, edge="#E3B54A", color="#F4DD92")
    kg = cx.amt(("c7s12", "karşılaşmadı.", -0.5), 0.7)
    if kg > 0:
        xm, ym = (xa + xo) / 2, (ya + yo) / 2
        p = f.paint("#F0D27A", style="stroke", sw=5, alpha=0.95 * kg)
        p.setPathEffect(skia.DashPathEffect.Make([12, 12], -cx.t * 22))
        f.c.drawLine(xa + 40, ya + 20, xo - 40, yo - 10, p)
        X.ic(f, "question", xm, ym - 4, size=96, metal="silver", alpha=0.9 * kg)
        X.chip(f, "İKİ ORDU HİÇ KARŞILAŞMADI", W / 2 + 270, 205, k=kg, size=38, edge="#B02A2A", color="#F8E2D8", padx=40, h=90)
