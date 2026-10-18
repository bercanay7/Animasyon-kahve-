"""Bölüm 8 — Akdeniz'de Barbaros (c8): Tunus 1534–35, Preveze 1538, Cezayir 1541. Yazar: bölüm yazarı C."""
import math
from shots import shot
import scenes_lib  # noqa: F401
import icons       # noqa: F401
import sk
import stage_c678 as X
import stage_c8    # noqa: F401  özel çekim türleri (c8_*)
import shots as SH
import stage as ST
from sk import H, W, clamp, ease_io, ease_out, back_out

A = X.W
CHAINS = "chains" if X.has_icon("chains") else "keys"


def _route_icon_ships(cx, cam, mv):
    pass


def _fleet_extras(*fns):
    def fn(cx, cam, mv):
        for g in fns:
            g(cx, cam, mv)
    return fn


def _ripples(center_ll, at, color="#5FA878", n=3, maxr=900, period=2.8):
    """Dönen/yayılan halkalar (Osmanlı deniz üstünlüğü dalgası)."""
    def fn(cx, cam, mv):
        k = cx.amt(at, 0.8)
        if k <= 0:
            return
        x, y = cam.ll(*center_ll)
        for i in range(n):
            u = ((cx.t - cx.at(at)) / period + i / n) % 1.0
            cx.f.circle(x, y, 40 + u * maxr, style="stroke", sw=5 * (1 - u) + 1.5, color=color, alpha=0.75 * (1 - u) * k)
            cx.f.circle(x, y, 40 + u * maxr, color=color, alpha=0.06 * (1 - u) * k)
    return fn


def _preveze_ov():
    def fn(cx):
        f = cx.f
        items = [("PAPALIK", "keys", "violet", ("c8s7", "papanın,", -0.1)), ("VENEDİK", "laurel", "teal", ("c8s7", "Venedik'in", -0.1)),
                 ("İMPARATOR", "imperial_crown", "gold", ("c8s7", "imparatorun", -0.1))]
        kgo = cx.amt(("c8s7", "geri", -0.1), 0.6)
        for i, (name, icon, metal, at) in enumerate(items):
            k = cx.amt(at, 0.5) * (1 - 0.45 * kgo)
            if k <= 0:
                continue
            x, y = 260, 330 + i * 120
            f.rrect(x - 190, y - 46, 390, 92, 14, color="#150D08", alpha=0.86 * k)
            f.rrect(x - 190, y - 46, 390, 92, 14, style="stroke", sw=2.5, color="#C9962B", alpha=0.95 * k)
            X.ic(f, icon, x - 130, y, size=72, metal=metal, alpha=k, shadow=False)
            f.text(name, x - 78, y + 14, face="title_m", size=34, color="#F4E6BC", align="l", track=5, alpha=k, shadow=(1, 2, 2, "#000000"))
        kb = cx.amt(("c8s7", "Barbaros'la", -0.15), 0.6)
        if kb > 0:
            x, y = 1660, 430
            f.rrect(x - 200, y - 46, 400, 92, 14, color="#0E1F16", alpha=0.88 * kb)
            f.rrect(x - 200, y - 46, 400, 92, 14, style="stroke", sw=2.5, color="#5FA878", alpha=0.95 * kb)
            X.ic(f, "crescent", x - 140, y, size=72, metal="forest", alpha=kb, shadow=False)
            f.text("BARBAROS", x - 88, y + 14, face="title_m", size=34, color="#D6F5E0", align="l", track=5, alpha=kb, shadow=(1, 2, 2, "#000000"))
        kc = cx.amt(("c8s7", "çekildi.", -0.35), 0.6)
        if kc > 0:
            X.chip(f, "GERİ ÇEKİLDİ", W / 2, 960, k=kc, size=40, edge="#B02A2A", color="#F8E2D8", padx=44, h=90)
    return fn


def _storm_ov(cx):
    f = cx.f
    # barut ıslandı
    kb = cx.amt(("c8s10", "barutu", -0.2), 0.6) * (1 - cx.amt(("c8s10", "yaklaşık", -0.2), 0.5))
    if kb > 0:
        X.ic(f, "cannon", 300, 430, size=240, metal="silver", alpha=kb, glow=0.15 * kb)
        for i in range(14):
            xx = 210 + (i * 37) % 200
            yy = 280 + ((cx.t * 260 + i * 53) % 260)
            f.line(xx, yy, xx - 6, yy + 24, color="#9CC4D8", sw=3, alpha=0.8 * kb)
        X.chip(f, "BARUT ISLANDI", 300, 640, k=kb, size=34, edge="#5E8FA8", color="#DCEEF8", padx=36)
    # yaklaşık yüz elli gemi
    kn = cx.amt(("c8s10", "yaklaşık", -0.15), 0.5)
    if kn > 0:
        v = ease_out(clamp((cx.t - cx.at(("c8s10", "yüz", -0.15))) / 1.0), 3)
        SH.gold_flat(f, f"≈ {int(round(150 * v))}", W / 2, 520, face="title", size=200, track=8, alpha=kn)
        f.text("GEMİ BATTI", W / 2, 610, face="title_m", size=56, color="#E0C682", align="c", track=16, alpha=cx.amt(("c8s10", "yüz", -0.15), 0.5, off=0.3))
        SH.stamp(f, "YAKLAŞIK", W / 2 + 430, 400, rot=-0.07, size=40, t=cx.amt(("c8s10", "yaklaşık", -0.1), 0.3), color="#9A7A38")


SHOTS = [
    # s1 — Akdeniz'de karşısında sultanın amirali
    shot("c678_sahne", a=("c8s1", -0.2), scene="sea", cams=[(0.0, (960, 560, 1.0)), (("c8s1", "Barbaros", -0.1), (1040, 580, 1.25))],
         p=dict(tag="c8_deniz1", mood="dawn", coast=None, ships=[dict(kind="galley", x=0.22, row=1, s=1.0, flag="#2F6B4A", heading=1), dict(kind="galley", x=0.5, row=2, s=1.25, flag="#2F6B4A", heading=1),
                                                              dict(kind="galley", x=0.8, row=1, s=1.05, flag="#2F6B4A", heading=1)]),
         overlay=X.ov_kick("AKDENİZ", ("c8s1", "Akdeniz'de", -0.1), y=122, size=38), label="akdeniz_kadirgalar"),
    shot("medal", a=("c8s1", "Barbaros", -0.15), tr=("fade", 0.7), key="barbaros", metal="forest", name="BARBAROS HAYREDDİN PAŞA", role="Osmanlı Amirali", pos="c", size=700, bgk="sea",
         at=("c8s1", "Barbaros", -0.1), plate_at=("c8s1", "Hayreddin", -0.15), extra=lambda cx: X.kick(cx, "1534", ("c8s2", "1534'te", -0.1), y=132, size=46), label="barbaros"),

    # s2 — 1534: kaptan-ı derya; Tunus
    shot("map", a=("c8s2", "Barbaros", -0.15), tr=("fade", 0.7), cams=[(0.0, (19.4, 38.8, 1.7)), (("c8s3", -0.3), (17.0, 38.2, 1.9))],
         regions=[dict(name="osmanli_1520", color="osmanli", at=0.0, alpha=0.55), dict(name="tunus", color="osmanli", at=("c8s2", "Tunus'u", -0.1), alpha=0.7),
                  dict(name="sicilya", color="ispanya", at=0.2, alpha=0.5), dict(name="napoli_kara", color="ispanya", at=0.2, alpha=0.5)],
         routes=[dict(pts=[(28.98, 41.01), (26.4, 38.8), (23.0, 36.6), (17.0, 36.2), (11.0, 37.0), (10.3, 36.8)], at=("c8s2", "kaptan-ı", -0.1), dur=3.0, color="#5FA878", width=9)],
         cities=[dict(lon=28.98, lat=41.01, name="İSTANBUL", kind="capital", at=0.0, color="#9FE0B4", side="b", size=28),
                 dict(lon=10.18, lat=36.8, name="TUNUS", kind="siege", at=("c8s2", "Tunus'u", -0.1), side="t", size=32)],
         notes=[dict(text="KAPTAN-I DERYA", x=210, y=250, at=("c8s2", "kaptan-ı", -0.1), w=520, size=40)],
         icons_=[dict(kind="ship", lon=26.4, lat=38.8, size=84, at=("c8s2", "kaptan-ı", 0.0), metal="forest", route=[(28.98, 41.01), (26.4, 38.8), (23.0, 36.6), (17.0, 36.2), (11.0, 37.0), (10.3, 36.8)],
                      move_at=("c8s2", "kaptan-ı", -0.1), move_dur=3.0, bob=3)],
         date=("1534", ("c8s2", "1534'te", -0.1)), label="istanbul_tunus"),

    # s3 — Ertesi yıl: Şarlken + Doria, bizzat Tunus'a
    shot("c678_medals", a=("c8s3", -0.2), tr=("fade", 0.7), bgk="sea", size=520, y=H * 0.45, gap=900, title="TUNUS SEFERİ · 1535",
         items=[dict(key="karl_olgun", name="V. KARL", role="İmparator", at=("c8s3", "Şarlken,", -0.1), metal="gold"),
                dict(key="doria", name="ANDREA DORIA", role="Filo komutanı", at=("c8s3", "Andrea", -0.1), metal="silver", flip=True)],
         extra=lambda cx: X.chip(cx.f, "BİZZAT", 510, 150 + 0, k=cx.amt(("c8s3", "bizzat", -0.1), 0.5), size=36, edge="#E3B54A", color="#F4DD92", padx=40) if False else
         X.chip(cx.f, "BİZZAT", 510, 840 + 120, k=cx.amt(("c8s3", "bizzat", -0.1), 0.5), size=34, edge="#E3B54A", color="#F4DD92", padx=40), label="karl_doria"),

    # s4 — Halkulvadi düştü; yirmi bin esir
    shot("c678_sahne", a=("c8s4", -0.3), tr=("whip", 0.5), scene="siege", cams=[(0.0, (960, 560, 1.0)), (("c8s4", "Yaklaşık", -0.3), (1000, 580, 1.3))],
         p=dict(tag="c8_halk", city="halkulvadi", time="day", weather="clear", cannon_fire=True, fire=0.4),
         overlay=X.ov_all(X.ov_date("TEMMUZ 1535", ("c8s4", "Temmuz", -0.1)), X.ov_kick("HALKULVADİ", ("c8s4", "Halkulvadi", -0.2), y=122, size=38),
                          X.ov_stamp("TUNUS ALINDI", ("c8s4", "Tunus", -0.15), x=W / 2, y=900, size=56, rot=-0.05)), label="halkulvadi"),
    shot("c678_cift", a=("c8s4", "Yaklaşık", -0.2), tr=("fade", 0.5), bgk="sea", title="HALKULVADİ · TUNUS", y=H * 0.5, size=190, ykick=150,
         items=[dict(value=20000, unit="esir", label="SERBEST KALDI", icon=CHAINS, metal="gold", at=("c8s4", "yirmi", -0.15), dur=1.3)],
         stampt=("YAKLAŞIK", 1330, 330, ("c8s4", "Yaklaşık", -0.1), 44, -0.07), label="20bin_esir"),

    # s5 — Habsburg çevresinde zafer kutlaması
    shot("c8_zafer", a=("c8s5", -0.2), tr=("zoom", 0.6), at_kick=("c8s5", "Habsburg", -0.1), at_laurel=("c8s5", "Habsburg", 0.0), at_word=("c8s5", "zafer", -0.15), label="zafer_kutlama"),

    # s6 — deniz uzundu; Barbaros hâlâ ortadaydı
    shot("c678_sahne", a=("c8s6", -0.2), tr=("dip", 0.7), scene="sea", cams=[(0.0, (960, 540, 1.0)), (("c8s7", -0.4), (1000, 560, 1.2))],
         p=dict(tag="c8_gece", mood="night", moon=True, coast=None, ships=[dict(kind="galley", x=0.55, row=0, s=0.55, flag="#2F6B4A", heading=-1), dict(kind="galley", x=0.68, row=0, s=0.5, flag="#2F6B4A", heading=-1),
                                                                     dict(kind="galley", x=0.8, row=0, s=0.45, flag="#2F6B4A", heading=-1)]),
         overlay=X.ov_medal("barbaros", ("c8s6", "Barbaros", -0.15), 1560, 410, size=320, metal="forest"), label="gece_deniz_filo"),

    # s7 — Preveze: harita + deniz savaşı
    shot("map", a=("c8s7", -0.3), tr=("fade", 0.7), cams=[(0.0, (20.2, 38.6, 3.0)), (("c8s7", "papanın,", -0.3), (20.7, 38.95, 4.4))],
         regions=[dict(name="osmanli_1520", color="osmanli", at=0.0, alpha=0.55), dict(name="venedik", color="venedik", at=0.2, alpha=0.6)],
         cities=[dict(lon=20.75, lat=38.95, name="PREVEZE", kind="battle", at=("c8s7", "Preveze'de,", -0.6), side="r", size=36)],
         date=("28 EYLÜL 1538", ("c8s7", "28", -0.1)), label="preveze_harita"),
    shot("c678_sahne", a=("c8s7", "papanın,", -0.25), tr=("whip", 0.5), scene="sea", cams=[(0.0, (900, 560, 1.0)), (("c8s7", "geri", -0.2), (1000, 580, 1.3))],
         p=dict(tag="c8_preveze", mood="calm", coast="harbor", smoke=True, ships=[dict(kind="galley", x=0.2, row=1, s=1.0, flag="#D4B64E", heading=1), dict(kind="galley", x=0.32, row=2, s=1.2, flag="#2F7A8A", heading=1),
                                                                               dict(kind="carrack", x=0.45, row=1, s=1.0, flag="#8E1F26", heading=1),
                                                                               dict(kind="galley", x=0.78, row=1, s=1.1, flag="#2F6B4A", heading=-1), dict(kind="galley", x=0.9, row=2, s=1.25, flag="#2F6B4A", heading=-1)]),
         overlay=_preveze_ov(), label="preveze_savas"),

    # s8 — Sonraki yıllarda doğu Akdeniz'de Osmanlı üstün
    shot("map", a=("c8s8", -0.2), tr=("fade", 0.7), cams=[(0.0, (23.0, 38.2, 2.5)), (("c8s9", -0.4), (22.0, 37.8, 2.7))],
         regions=[dict(name="osmanli_1550", color="osmanli", at=("c8s8", "Osmanlı", -0.5), alpha=0.6, dur=1.4)],
         labels=[dict(text="AKDENİZ'İN DOĞUSU", lon=27.0, lat=34.2, size=40, color="#BFE9D0", at=("c8s8", "Akdeniz'in", -0.1), track=12),
                 dict(text="OSMANLI DONANMASI", lon=21.0, lat=36.2, size=34, color="#9FE0B4", at=("c8s8", "donanması", -0.3), track=10)],
         icons_=[dict(kind="ship", lon=26.0, lat=36.5, size=86, at=("c8s8", "Osmanlı", -0.2), metal="forest", route=[(28.5, 36.2), (25.0, 36.0), (21.0, 36.8)], move_at=("c8s8", "Osmanlı", -0.2), move_dur=3.6, bob=3),
                 dict(kind="ship", lon=24.0, lat=38.0, size=86, at=("c8s8", "Osmanlı", 0.0), metal="forest", route=[(26.0, 39.0), (23.0, 37.6), (19.8, 37.8)], move_at=("c8s8", "Osmanlı", 0.0), move_dur=3.6, bob=3),
                 dict(kind="ship", lon=23.0, lat=35.0, size=86, at=("c8s8", "Osmanlı", 0.3), metal="forest", route=[(27.0, 35.0), (23.5, 34.8), (19.5, 35.4)], move_at=("c8s8", "Osmanlı", 0.3), move_dur=3.6, bob=3)],
         extra=_ripples((20.75, 38.95), ("c8s8", "Sonraki", 0.0)), label="dogu_akdeniz_ustunluk"),

    # s9 — 1541: Cezayir; 500 yelkenli, 24 bin asker
    shot("map", a=("c8s9", -0.2), tr=("fade", 0.7), cams=[(0.0, (3.4, 38.9, 2.6)), (("c8s9", "beş", -0.3), (3.1, 37.6, 3.6))],
         regions=[dict(name="cezayir", color="osmanli", at=("c8s9", "Cezayir'e", -0.3), alpha=0.5), dict(name="ispanya", color="ispanya", at=0.0, alpha=0.55)],
         routes=[dict(pts=[(2.8, 41.2), (3.0, 39.4), (3.05, 37.3)], at=("c8s9", "Cezayir'e", -0.2), dur=2.0, color="#E8C25A", width=8)],
         cities=[dict(lon=3.06, lat=36.75, name="CEZAYİR", kind="siege", at=("c8s9", "Cezayir'e", -0.3), side="r", size=34)],
         date=("1541", ("c8s9", "1541'de", -0.1)), label="cezayir_harita"),
    shot("c678_cift", a=("c8s9", "beş", -0.15), tr=("fade", 0.5), bgk="sea", title="CEZAYİR · 1541", y=H * 0.5, size=150, ykick=140,
         items=[dict(value=500, prefix="≈ ", unit="yelkenli", icon="ship", metal="gold", at=("c8s9", "beş", -0.1), dur=1.3),
                dict(value=24000, prefix="≈ ", unit="asker", icon="swords", metal="gold", at=("c8s9", "yaklaşık", -0.15), dur=1.5)], label="500_24bin"),

    # s10 — fırtına: barut ıslandı, ≈150 gemi battı
    shot("c678_sahne", a=("c8s10", -0.2), tr=("whip", 0.5), scene="sea", cams=[(0.0, (960, 560, 1.0)), (("c8s10", "yaklaşık", -0.3), (980, 580, 1.25))],
         p=dict(tag="c8_firtina", mood="storm", rain=True, lightning=True, coast="africa",
                ships=[dict(kind="carrack", x=0.2, row=1, s=1.0, flag="#8E1F26", heading=1, rock=0.8), dict(kind="carrack", x=0.45, row=2, s=1.2, flag="#8E1F26", heading=1, rock=1.0, sink=0.5),
                       dict(kind="galley", x=0.68, row=1, s=1.0, flag="#8E1F26", heading=1, rock=0.9, sink=0.8), dict(kind="carrack", x=0.85, row=2, s=1.1, flag="#8E1F26", heading=1, rock=1.0, sink=0.3)]),
         overlay=_storm_ov, label="cezayir_firtina"),

    # s11 — Cortés oradaydı; konseye çağrılmadığı anlatılır
    shot("c8_konsey", a=("c8s11", -0.3), tr=("dip", 0.7), at_scene=0.0, at_kort=("c8s11", "Hernán", -0.2), at_kick=("c8s11", "savaş", -0.15), at_chip=("c8s11", "çağrılmadığı", -0.2),
         at_stamp=("c8s11", "anlatılır.", -0.2), label="cortes_konsey"),
]
