"""Bölüm 6 — Kral, Esir, Düello (c6): Fransa ile savaş, Pavia, Madrid, Roma 1527, Hanımlar Barışı. Yazar: bölüm yazarı C."""
import math
from shots import shot
import scenes_lib  # noqa: F401  theatre şablonunu kaydeder
import icons       # noqa: F401
import sk
import stage_c678 as X
import stage_c6    # noqa: F401  özel çekim türleri + sahneler (c6_*)
from sk import H, W

A = X.W      # sözcük çapası (sözcük yoksa cümle ofsetine düşer)


def _pavia_ov():
    return X.ov_all(
        X.ov_date("24 ŞUBAT 1525", ("c6s3", "24", -0.1)),
        X.ov_kick("PAVIA", ("c6s3", "Pavia'da", -0.1), y=122, size=34),
        X.ov_stamp("BOZGUN", ("c6s3", "bozguna", -0.1), x=640, y=300, size=72, rot=-0.08),
        X.ov_medal("fransuva", ("c6s3", "François", -0.15), 1560, 440, size=320, metal="royal", flip=True, name="I. FRANÇOIS", role="Fransa Kralı", plate_y=610),
        X.ov_stamp("ESİR", ("c6s3", "esir", -0.1), x=1560, y=835, size=76, rot=-0.10),
    )


def _fleur_wait(cx):
    """François madalyası gelmeden önce: Fransa'yı simgeleyen zambak (fleur) belirir, madalya gelince söner."""
    k = cx.amt(("c6s1", "Fransa", -0.1), 0.8) * (1 - cx.amt(("c6s1", "François", -0.35), 0.5))
    if k > 0:
        cx.f.circle(W / 2 + 450, H * 0.45, 260, shader=cx.f.rad(W / 2 + 450, H * 0.45, 260, [("#27427A", 0.0, int(70 * k)), ("#27427A", 1.0, 0)]))
        X.ic(cx.f, "fleur", W / 2 + 450, H * 0.45, size=300 * (0.9 + 0.1 * k), metal="royal", alpha=k, glow=0.3 * k)


SHOTS = [
    # s1 — iki rakip
    shot("c678_medals", a=("c6s1", -0.2), items=[
        dict(key="karl_olgun", name="V. KARL", role="İmparator", at=("c6s1", "Şarlken'in", -0.1), metal="gold"),
        dict(key="fransuva", name="I. FRANÇOIS", role="Fransa Kralı", at=("c6s1", "François", -0.3), metal="royal", flip=True)],
        size=540, y=H * 0.45, gap=900, vs=("c6s1", "François", 0.35), extra=_fleur_wait, label="karl_fransuva"),

    # s2 — Fransa kuşatılmış: Habsburg toprakları sırayla, kuşatma okları
    shot("map", a=("c6s2", -0.35), tr=("fade", 0.9),
         cams=[(0.0, (4.4, 47.1, 1.34)), (("c6s2", "Napoli.", 0.9), (4.9, 46.7, 1.40))], compass=(150, 930, 58),
         regions=[dict(name="fransa", color="fransa", at=("c6s2", "Fransa,", -0.1), alpha=0.72),
                  dict(name="ispanya", color="ispanya", at=("c6s2", "İspanya,", -0.2)),
                  dict(name="hollanda", color="burgonya", at=("c6s2", "kuzeyde", 0.0)),
                  dict(name="franche_comte", color="avusturya", at=("c6s2", "doğuda", 0.0), hatch=True),
                  dict(name="napoli_kara", color="ispanya", at=("c6s2", "İtalya'da", -0.15))],
         routes=[dict(pts=[(-3.8, 40.4), (-1.6, 42.9), (1.4, 44.2)], at=("c6s2", "güneyde", 0.0), dur=1.5, color="#E8C25A", width=7),
                 dict(pts=[(5.0, 52.0), (3.8, 50.2), (2.6, 48.4)], at=("c6s2", "kuzeyde", 0.15), dur=1.5, color="#E8C25A", width=7),
                 dict(pts=[(7.6, 46.4), (5.6, 46.5), (3.8, 46.6)], at=("c6s2", "doğuda", 0.2), dur=1.3, color="#E8C25A", width=7),
                 dict(pts=[(15.2, 40.6), (11.8, 43.6), (8.2, 45.0)], at=("c6s2", "İtalya'da", 0.0), dur=1.6, color="#E8C25A", width=7)],
         labels=[dict(text="FRANSA", lon=0.8, lat=46.4, size=52, color="#C4D4F8", at=("c6s2", "Fransa,", 0.1), track=14),
                 dict(text="İSPANYA", lon=-3.4, lat=39.6, size=38, at=("c6s2", "İspanya,", 0.0)),
                 dict(text="HOLLANDA", lon=5.2, lat=52.7, size=30, at=("c6s2", "Hollanda,", -0.4), track=8),
                 dict(text="BURGONYA", lon=8.9, lat=47.4, size=28, at=("c6s2", "Burgonya", -0.1), track=6),
                 dict(text="NAPOLİ", lon=12.4, lat=39.3, size=30, color="#F0C8BE", at=("c6s2", "Napoli.", -0.3), track=8)],
         cities=[dict(lon=2.35, lat=48.86, name="PARİS", kind="capital", at=("c6s2", "Fransa,", 0.3), color="#9CB8E8", side="l")],
         label="fransa_kusatma"),

    # s3 — Pavia: bozgun, kral esir
    shot("c678_sahne", a=("c6s3", -0.3), tr=("whip", 0.5), scene="field",
         cams=[(0.0, X.fcam(0, .60, 1.08)), (("c6s3", "bozguna", 0.0), X.fcam(0, .46, 1.22)), (("c6s3", "düştü", 1.0), X.fcam(0, .30, 1.45))],
         p=dict(tag="c6_pavia", ground="plain", weather="fog", castle_far="pavia", smoke=0.7,
                armies=[dict(side="#27427A", kind="pike", x=0.14, row=1, n=12, dir=-1, charge=0.4),
                        dict(side="#27427A", kind="cavalry", x=0.40, row=0, n=7, dir=-1, charge=0.5),
                        dict(side="#9A2430", kind="cavalry", x=0.70, row=0, n=7, dir=-1, charge=0.55),
                        dict(side="#9A2430", kind="arquebus", x=0.76, row=1, n=12, dir=-1, fire=1.0),
                        dict(side="#9A2430", kind="pike", x=0.90, row=2, n=14, dir=-1, charge=0.4)]),
         overlay=_pavia_ov(), label="pavia"),

    # s4 — annesine mektup (aktarılan söz) + sonradan yaygınlaşan slogan
    shot("c6_mektup", a=("c6s4", -0.4), tr=("fade", 0.8), at_a=("c6s4", "bana", 0.0), at_b=("c6s4", "kaldı", 0.0), at_hedge=("c6s4", "aktarıldığına", -0.1),
         at_seal=("c6s4", "diyordu", -0.2), at_slip=("c6s4", "Meşhur", -0.25), at_stamp=("c6s4", "sonradan", -0.1), label="mektup"),

    # s5 — Madrid: hücre; esir kral + antlaşma (İtalya, Flandre; mühür)
    shot("c678_sahne", a=("c6s5", -0.3), tr=("fade", 0.8), scene="tower",
         cams=[(0.0, (970, 520, 1.0)), (("c6s5", "İtalya", -0.2), (1000, 440, 1.3))],
         p=dict(tag="c6_madrid_cell", variant="cell", night=True, figure="man", candle=1.0),
         overlay=X.ov_all(X.ov_kick("MADRİD", ("c6s5", "Madrid'de", -0.1), y=122, size=38), X.ov_chip("ESİR", ("c6s5", "esirken", -0.1), x=W / 2, y=H * 0.88, size=40, edge="#B02A2A", color="#F8E2D8", padx=44)),
         label="madrid_hucre"),
    shot("c6_antlasma", a=("c6s5", "İtalya", -0.08), tr=("fade", 0.5), at_medal=0.0, at_title=0.1, at_chip=0.4,
         at_l1=("c6s5", "İtalya", -0.15), at_l2=("c6s5", "Flandre", -0.15), at_strike=("c6s5", "vazgeçen", -0.05), at_seal=("c6s5", "imzaladı", -0.1), label="madrid_antlasma"),
    shot("c6_rehin", a=("c6s5", "İki", -0.2), tr=("dip", 0.6), at=0.0, at_stamp=("c6s5", "rehin", -0.1), label="rehin"),

    # s6 — esirin sözü geçersiz: belge yırtılır
    shot("c6_yirt", a=("c6s6", -0.3), tr=("fade", 0.7), at_flare=("c6s6", "Özgürlüğüne", 0.0), at_tear=("c6s6", "reddetti", 0.0),
         at_stamp=("c6s6", "geçersizdi", -0.15), at_note=("c6s6", "esirin", -0.1), label="antlasma_yirt"),

    # s7 — Roma 1527
    shot("c678_sahne", a=("c6s7", -0.3), tr=("whip", 0.6), scene="siege",
         cams=[(0.0, (960, 560, 1.0)), (("c6s7", "maaşını", 0.0), (1000, 600, 1.3))],
         p=dict(tag="c6_roma1", city="roma", time="dusk", fire=0.6, ladders=True, weather="clear"),
         overlay=X.ov_all(X.ov_embers(40, seed=5), X.ov_date("6 MAYIS 1527", ("c6s7", "6", -0.1)), X.ov_kick("ROMA", ("c6s7", "1527'de", -0.15), y=122, size=36)), label="roma_kusatma"),
    shot("c6_maas", a=("c6s7", "maaşını", -0.15), tr=("fade", 0.4), at=0.0, at_strike=("c6s7", "alamayan", -0.15), at_men=("c6s7", "imparatorluk", -0.15), label="maas_yok"),
    shot("c678_sahne", a=("c6s7", "Roma'ya", -0.5), tr=("whip", 0.3), scene="siege",
         cams=[(0.0, (900, 600, 1.1)), (("c6s8", 0.0), (1000, 560, 1.5))],
         p=dict(tag="c6_roma2", city="roma", time="night", fire=1.0, ladders=True, cannon_fire=True, weather="clear"),
         overlay=X.ov_embers(70, seed=7), label="roma_giris"),

    # s8 — Papa sığınır; muhafızlar
    shot("c678_sahne", a=("c6s8", -0.2), tr=("fade", 0.7), scene="c6_santangelo",
         cams=[(0.0, (900, 560, 1.0)), (("c6s8", "189", -0.2), (1100, 580, 1.4))], p=dict(tag="c6_sant", fire=1.0, bx=1180),
         overlay=X.ov_all(X.ov_medal("klemens", ("c6s8", "Papa,", -0.15), 340, 470, size=330, metal="violet", name="KLEMENS VII", role="Papa", plate_y=640),
                          X.ov_kick("CASTEL SANT'ANGELO", ("c6s8", "Castel", -0.1), y=122, size=34, x=720)), label="sant_angelo"),
    shot("c6_muhafiz", a=("c6s8", "189", -0.15), tr=("fade", 0.6), at_total=("c6s8", "189", -0.1), at_dead=("c6s8", "147'si", -0.05), dead_dur=1.5, label="muhafiz_189_147"),

    # s9 — emir yok; aylarca
    shot("c6_emir", a=("c6s9", -0.3), tr=("fade", 0.7), at_medal=("c6s9", "İmparator", -0.1), at_paper=("c6s9", "emir", -0.25), at_stamp=("c6s9", "vermemişti", -0.15), label="emir_yok"),
    shot("c6_aylar", a=("c6s9", "Ama", -0.25), tr=("fade", 0.6), at=0.0, at_start=("c6s9", "aylarca", -0.35), at_end=("c6s9", "kaldı", 0.45),
         at_word=("c6s9", "aylarca", -0.1), at_stamp=("c6s9", "kaldı", 0.2), label="papa_aylarca"),

    # s10 — uzak sonuç: Roma → İngiltere; zincir
    shot("map", a=("c6s10", -0.2), tr=("fade", 0.8), cams=[(0.0, (4.7, 47.4, 1.34)), (("c6s10", "papa,", -0.3), (4.3, 47.5, 1.42))],
         regions=[dict(name="papalik", color="papalik", at=("c6s10", "Sıkça", 0.0), alpha=0.7),
                  dict(name="britanya", color="ingiliz", at=("c6s10", "İngiltere'de", -0.3))],
         routes=[dict(pts=[(12.5, 41.9), (8.0, 45.4), (2.0, 49.4), (-0.12, 51.4)], at=("c6s10", "uzak", -0.1), dur=2.2, color="#E26A5A", width=7, dash=(16, 10))],
         cities=[dict(lon=12.5, lat=41.9, name="ROMA", kind="battle", at=("c6s10", "Sıkça", 0.0), side="b"),
                 dict(lon=-0.12, lat=51.5, name="LONDRA", kind="capital", at=("c6s10", "İngiltere'de", -0.2), color="#E26A5A", side="l")],
         labels=[dict(text="İNGİLTERE", lon=-2.4, lat=53.2, size=36, color="#F0C8BE", at=("c6s10", "İngiltere'de", -0.3))],
         extra=lambda cx, cam, mv: X.ov_stamp("SIKÇA ANLATILIR", ("c6s10", "Sıkça", 0.0), x=1500, y=300, size=54, rot=-0.05)(cx),
         label="roma_ingiltere"),
    shot("c6_zincir", a=("c6s10", "papa,", -0.25), tr=("fade", 0.7), at_n1=0.0, at_n2=("c6s10", "papa,", -0.1), at_n3=("c6s10", "Aragonlu", -0.15), at_n4=("c6s10", "Henry,", -0.1),
         at_teyze=("c6s10", "teyzesi", -0.05), at_x=("c6s10", "onaylayamadı", -0.25), at_break=("c6s10", "koptu", -0.45), at_stamp=0.15, label="zincir_catherine_henry"),

    # s11 — 1528: yalancı! düello yapılmadı
    shot("c6_duello", a=("c6s11", -0.3), tr=("dip", 0.8), at_year=("c6s11", "1528'de", -0.1), at_names=("c6s11", "hükümdar", -0.15), at_b1=("c6s11", "yalancı", -0.1), at_b2=("c6s11", "yalancı", 0.3),
         at_swords=("c6s11", "düelloya", -0.1), at_gone=("c6s11", "Düello", 1, -0.1), at_stamp=("c6s11", "yapılmadı", -0.25), label="duello"),

    # s12 — Cambrai 1529; iki kadın
    shot("map", a=("c6s12", -0.3), tr=("fade", 0.8), cams=[(0.0, (3.2, 49.7, 3.8)), (("c6s12", "iki", 0.0), (3.5, 50.0, 4.6))],
         regions=[dict(name="fransa", color="fransa", at=0.0, alpha=0.7), dict(name="hollanda", color="burgonya", at=0.0, alpha=0.7)],
         labels=[dict(text="FRANSA", lon=1.2, lat=48.5, size=44, color="#C4D4F8", at=0.6, track=14), dict(text="HABSBURG TOPRAKLARI", lon=5.6, lat=51.1, size=26, color="#F0C8BE", at=0.9, track=8)],
         cities=[dict(lon=3.236, lat=50.176, name="CAMBRAI", kind="siege", at=("c6s12", "Cambrai'de", -0.3), size=34, side="r"),
                 dict(lon=2.35, lat=48.86, name="PARİS", kind="capital", at=0.5, color="#9CB8E8", side="l"),
                 dict(lon=4.35, lat=50.85, name="BRÜKSEL", kind="capital", at=0.7, color="#E8A89E", side="r")],
         date=("1529", ("c6s12", "1529'da", -0.1)), label="cambrai_harita"),
    shot("c6_hanimlar", a=("c6s12", "iki", -0.25), tr=("fade", 0.7), at_two=("c6s12", "kadın", -0.4), at_l=("c6s12", "annesi", -0.5), at_r=("c6s12", "halası", -0.6),
         at_title=("c6s12", "Hanımlar", -0.1), label="hanimlar_baris"),

    # s13 — 2 milyon altın ecü
    shot("c6_fidye", a=("c6s13", -0.1), tr=("fade", 0.7), at=("c6s13", "iki", -0.2), at_boys=0.25, label="iki_milyon_ecu"),

    # s14 — kalıcı olmadı: kesintili savaş, 1558
    shot("c6_savas", a=("c6s14", -0.3), tr=("fade", 0.8), at_axis=("c6s14", "Barış", -0.15), at_peace=("c6s14", "Barış", 0.0), at_war=("c6s14", "olmadı", 0.25),
         at_gap=("c6s14", "kesintilerle", -0.1), at_end=("c6s14", "ömrünün", -0.2), label="savas_kronoloji"),
]
