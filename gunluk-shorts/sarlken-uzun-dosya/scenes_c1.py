"""Bölüm 1 — Dört Tahtın Çocuğu (1500–1518). Ton: süslü hanedan altını → hüzün (Juana) → fırtına mavisi."""
import math

import icons
import kit_a as K
import scenes_lib  # theatre şablonunu kaydeder
import shots as SH
import shots_c1  # noqa: F401  (c1_* özel çekim türleri)
import sk
from shots import shot
from sk import H, W, clamp, ease_out, lerp, smooth

# ───────────────────────────── yardımcı kaplamalar ─────────────────────────────
GENT = (3.72, 51.05)
BURGOS = (-3.70, 42.34)
TORDESILLAS = (-5.00, 41.50)
MECHELEN = (4.48, 51.03)
SANTANDER = (-3.80, 43.46)
TAZONES = (-5.40, 43.54)
VALLADOLID = (-4.72, 41.65)


def _ex_gent(cx, cm, mv):
    K.place(cx.f, cm, GENT[0], GENT[1], "GENT", cx.t, amt=cx.amt(("c1s1", "Gent", -0.2), 0.6), side="r", size=42, r=17)


def _ex_burgos(cx, cm, mv):
    f = cx.f
    K.place(f, cm, BURGOS[0], BURGOS[1], "BURGOS", cx.t, amt=cx.amt(("c1s6", "Burgos'ta", -0.25), 0.6), side="r", size=42, r=17)
    a = cx.amt(("c1s6", "babası", -0.05), 1.0)
    if a > 0:
        # Filip: oniks madalya, sol tarafta; ölüm anında hafif kararır
        SH.draw_medal(f, K.mkey("filip", "ferdinand"), 470, 520, 430, "onyx", alpha=a, tilt=0.12 * math.sin(cx.t * 0.7), inscription=False)
        SH.name_plate(f, "FİLİP", None, None, cx_=470, y=H * 0.69, t=cx.amt(("c1s6", "babası", 0.25), 0.5), w=360)


def _ex_tordesillas(cx, cm, mv):
    K.place(cx.f, cm, TORDESILLAS[0], TORDESILLAS[1], "TORDESILLAS", cx.t, amt=cx.amt(("c1s7", "Tordesillas'ta", -0.25), 0.6), side="r", size=42, r=17)


def _ex_mechelen(cx, cm, mv):
    f = cx.f
    K.place(f, cm, MECHELEN[0], MECHELEN[1], "MECHELEN", cx.t, amt=cx.amt(("c1s10", "Mechelen'de", -0.15), 0.6), side="t", size=42, r=17)
    a = cx.amt(("c1s10", "Fransızcaydı", -0.15), 0.7)
    if a > 0:
        y = 860 - 12 * (1 - a)
        wd = 760
        SH.plate(f, W / 2 - wd / 2, y - 62, wd, 108, alpha=a, corner=18)
        icons.draw_icon(f, "fleur", W / 2 - wd / 2 + 76, y - 8, size=84, metal="gold", alpha=a, shadow=False)
        f.text("ANA DİLİ: FRANSIZCA", W / 2 + 40, y + 12, face="title_m", size=40, color="#F3DE9A", align="c", track=6, alpha=a, shadow=(2, 2, 3, "#000000"))


ROTA_ANA = [(3.4, 51.6), (0.8, 50.4), (-2.8, 49.5), (-5.3, 47.9), (-4.6, 45.9), (-3.9, 44.3), SANTANDER]
ROTA_GERCEK = [(-5.3, 47.9), (-7.1, 46.2), (-6.9, 44.5), (-5.6, 43.75), TAZONES]


def _ex_tazones(cx, cm, mv):
    f = cx.f
    a_s = cx.amt(("c1s14", "Santander'di", -0.15), 0.6)
    if a_s > 0:
        x, y = cm.ll(*SANTANDER)
        K.beacon(f, x, y, cx.t, amt=a_s, color="#9FB8C8", r=14)
        K.tag(f, "SANTANDER", x + 40, y + 16, alpha=a_s, size=36, align="l", pad=22, color="#C7D6E0", edge="#7C93A4", sub="hedef")
    a_t = cx.amt(("c1s14", "balıkçı", -0.15), 0.6)
    if a_t > 0:
        x, y = cm.ll(*TAZONES)
        K.beacon(f, x, y, cx.t, amt=a_t, color="#F0D27A", r=17)
        K.tag(f, "KÜÇÜK BALIKÇI KÖYÜ", x - 40, y + 70, alpha=a_t, size=36, align="r", pad=24)


def _ex_valladolid(cx, cm, mv):
    K.place(cx.f, cm, VALLADOLID[0], VALLADOLID[1], "VALLADOLID", cx.t, amt=cx.amt(("c1s16", "Valladolid", 0.0), 0.6), side="r", size=42, r=17)


def _tower_overlay(cx):
    """46 YIL: 1509 → 1555 ilerleme çubuğu (kule dioramasının üstünde)."""
    f = cx.f
    t0 = cx.at(("c1s8", "kırk", -0.1))
    t_end = cx.at(("c1s8", "kapatmayı", 0.0))
    a = smooth((cx.t - t0) / 0.5) * (1 - smooth((cx.t - t_end) / 0.6))
    if a <= 0:
        return
    k = ease_out(clamp((cx.t - t0 - 0.05) / 1.15), 2)
    f.rect(0, 690, W, 390, shader=f.lin(0, 690, 0, H, [("#000000", 0.0, 0), ("#000000", 1.0, int(215 * a))]))
    x0, x1, y = 330, 1590, 912
    f.line(x0, y, x1, y, color="#C9962B", sw=4, alpha=0.6 * a)
    f.line(x0, y, lerp(x0, x1, k), y, color="#F6DC8A", sw=8, alpha=a)
    for xx, lab in ((x0, "1509"), (x1, "1555")):
        f.circle(xx, y, 10, color="#F0D27A", alpha=a)
        f.text(lab, xx, y + 60, face="title_m", size=36, color="#E3CF98", align="c", track=4, alpha=a, shadow=(2, 2, 3, "#000000"))
    mx = lerp(x0, x1, k)
    K.glow_disc(f, mx, y, 40, "#FFE9A8", 0.8 * a)
    SH.gold_flat(f, f"{int(round(46 * k))} YIL", W / 2, 835, face="title", size=100, track=8, alpha=a)


def _tazones_overlay(cx):
    a = cx.amt(("c1s14", "Tazones'a", -0.1), 0.6)
    K.tag(cx.f, "TAZONES", 330, 190, alpha=a, size=48, align="l", pad=30)


def _storm_date(cx):
    SH._date_stamp(cx.f, ("EYLÜL 1517", ("c1s14", "Eylül", -0.1)), cx)


# ───────────────────────────── çekim listesi ─────────────────────────────
SHOTS = [
    # s1 — 24 Şubat 1500, Gent: Avrupa → Flandre
    shot("a_map", a=0.0, tr=("fade", 0.8), need=("c1_flandre",),
         cams=[(0.0, (8.0, 47.8, 1.45)), (("c1s1", "Şubat", 0.1), (7.2, 48.8, 1.7)), (("c1s1", "Gent", -0.2), (3.75, 51.05, 7.2))],
         regions=[dict(name="c1_flandre", color="burgonya", at=("c1s1", "Flandre'daki", -0.3), alpha=0.5)],
         labels=[dict(text="FLANDRE", lon=3.2, lat=51.5, size=64, track=30, color="#F2D78A", at=("c1s1", "Flandre'daki", -0.1))],
         date=("24 ŞUBAT 1500", ("c1s1", "24", -0.1)), extra=_ex_gent, label="gent_harita"),
    # s2 — Juana & Filip
    shot("c1_evli", a=("c1s2", -0.25), tr=("fade", 0.8), a_j=("c1s2", "Kastilya", -0.1), a_f=("c1s2", "Burgonyalı", -0.1), a_ring=("c1s2", "Filip", 0.15), label="juana_filip"),
    # s3 — dört büyükanne-büyükbaba (soy ağacı)
    shot("tree", a=("c1s3", -0.1), at=("c1s3", "Dört", -0.1),
         nodes=[dict(id="mb", key=K.mkey("maria_burgonya", "margareta"), name="MARİA", dates="Burgonyalı", x=0.17, y=0.2, at=("c1s3", "büyükanne", -0.1), size=215, nsize=26),
                dict(id="mx", key="maksimilyan", name="MAKSİMİLYAN", x=0.39, y=0.2, at=("c1s3", "ve", 0.0), size=215, nsize=26),
                dict(id="fe", key=K.mkey("fernando", "ferdinand"), name="FERNANDO", x=0.61, y=0.2, at=("c1s3", "büyükbabasının", -0.1), size=215, nsize=26),
                dict(id="ik", key=K.mkey("isabel_kastilya", "juana"), name="İSABEL", x=0.83, y=0.2, at=("c1s3", "büyükbabasının", 0.3), size=215, nsize=26),
                dict(id="fi", key=K.mkey("filip", "ferdinand"), name="FİLİP", x=0.3, y=0.5, at=("c1s3", "her", -0.1), size=235, nsize=28),
                dict(id="ju", key="juana", name="JUANA", x=0.7, y=0.5, at=("c1s3", "biri", -0.1), size=235, nsize=28),
                dict(id="ka", key=K.mkey("karl_cocuk", "karl_genc"), name="ŞARLKEN", x=0.5, y=0.795, at=("c1s3", "ona", -0.1), size=205, nsize=28)],
         edges=[("mb", "fi", ("c1s3", "her", 0.1)), ("mx", "fi", ("c1s3", "her", 0.3)), ("fe", "ju", ("c1s3", "biri", 0.1)), ("ik", "ju", ("c1s3", "biri", 0.3)),
                ("fi", "ka", ("c1s3", "ona", 0.1)), ("ju", "ka", ("c1s3", "ona", 0.3))],
         label="soy_agaci"),
    # s3b — dört ülke sırayla yanar
    shot("a_map", a=("c1s3", "Burgonya'yı", -0.8), tr=("fade", 0.8), need=("c1_aragon", "c1_kastilya"),
         cams=[(0.0, (3.5, 44.8, 1.26)), (("c1s3", "Kastilya'yı", 0.3), (3.5, 44.8, 1.33))],
         regions=[dict(name="hollanda", color="burgonya", at=("c1s3", "Burgonya'yı", -0.1)), dict(name="franche_comte", color="burgonya", at=("c1s3", "Burgonya'yı", 0.1)),
                  dict(name="avusturya", color="avusturya", at=("c1s3", "Avusturya'yı", -0.1)),
                  dict(name="c1_aragon", color="#C28A22", at=("c1s3", "Aragon'u", -0.1)), dict(name="napoli", color="#C28A22", at=("c1s3", "Aragon'u", 0.1)),
                  dict(name="sicilya", color="#C28A22", at=("c1s3", "Aragon'u", 0.2)), dict(name="sardunya", color="#C28A22", at=("c1s3", "Aragon'u", 0.3)),
                  dict(name="c1_kastilya", color="ispanya", at=("c1s3", "Kastilya'yı", -0.1))],
         labels=[dict(text="BURGONYA", lon=4.8, lat=51.9, size=34, at=("c1s3", "Burgonya'yı", -0.05)), dict(text="AVUSTURYA", lon=14.3, lat=48.1, size=34, at=("c1s3", "Avusturya'yı", -0.05)),
                 dict(text="ARAGON", lon=0.6, lat=41.6, size=32, at=("c1s3", "Aragon'u", -0.05)), dict(text="KASTİLYA", lon=-5.6, lat=38.5, size=32, at=("c1s3", "Kastilya'yı", -0.05))],
         label="dort_ulke"),
    # s4 — miras yolu: taç çok uzakta; beş ay sonra bir ölüm ve yol açılır
    shot("c1_yol", a=("c1s4", -0.2), tr=("fade", 0.8), t_far=("c1s4", "çok", 0.0), t_name=("c1s4", "İspanya", -0.1), t_five=("c1s4", "Beş", -0.1),
         t_cousin=("c1s4", "henüz", -0.15), t_age=("c1s4", "iki", -0.1), t_die=("c1s4", "öldü", 0.0), t_open=("c1s4", "yol", -0.1), label="miras_yolu"),
    # s5 — evlilikle ve ölümle
    shot("c1_cift", a=("c1s5", -0.2), tr=("fade", 0.7), t_crowns=("c1s5", "tahtları", -0.2), t_ring=("c1s5", "evlilikle", -0.1), t_skull=("c1s5", "ölümle", -0.1), label="evlilik_olum"),
    # s6 — Burgos: baba ölür
    shot("a_map", a=("c1s6", -0.2), tr=("dip", 0.8),
         cams=[(0.0, (-3.0, 41.0, 2.6)), (("c1s6", "Burgos'ta", 0.15), (-3.7, 42.34, 8.0))],
         regions=[dict(name="c1_kastilya", color="ispanya", at=0.3, alpha=0.17)], need=("c1_kastilya",),
         date=("6 YAŞINDA", ("c1s6", "Altı", -0.1)), extra=_ex_burgos, label="burgos"),
    # s7 — 1509, Tordesillas
    shot("a_map", a=("c1s7", -0.2), tr=("fade", 0.8),
         cams=[(0.0, (-4.0, 40.6, 2.6)), (("c1s7", "Tordesillas'ta", 0.0), (-5.0, 41.5, 7.5))],
         regions=[dict(name="c1_kastilya", color="ispanya", at=0.3, alpha=0.17)], need=("c1_kastilya",),
         date=("1509", ("c1s7", "1509'dan", -0.1)), extra=_ex_tordesillas, label="tordesillas_harita"),
    # s7–s8 — kule: Juana, 46 yıl
    shot("a_theatre", a=("c1s7", "bir", -0.2), tr=("fade", 0.9), scene="tower", p=dict(variant="tordesillas", night=True, figure="woman", candle=True),
         cams=[(0.0, (960, 540, 1.0)), (("c1s8", "Orada", 0.0), (960, 500, 1.3)), (("c1s8", "Oğlu", 0.0), (990, 450, 1.7)), (("c1s9", -0.4), (1000, 430, 2.0))],
         overlay=_tower_overlay, label="kule_juana"),
    # s9 — delilik mi, siyaset mi
    shot("c1_delilik", a=("c1s9", -0.2), tr=("fade", 0.8), t_l=("c1s9", "deliliğe", -0.15), t_r=("c1s9", "siyasete", -0.15), t_q=("c1s9", "bağlı", -0.1), t_stamp=("c1s9", "tartışıyor", -0.1), label="delilik_siyaset"),
    # s10 — Margareta, Mechelen
    shot("a_medals", a=("c1s10", -0.2), tr=("fade", 0.8), size=500, y=H * 0.44, gap=680,
         items=[dict(key=K.mkey("karl_cocuk", "karl_genc"), name="KÜÇÜK ŞARLKEN", at=("c1s10", "Küçük", -0.1), pw=640),
                dict(key="margareta", name="MARGARETA", role="Hala", at=("c1s10", "halası", -0.1), pw=640)], label="karl_margareta"),
    shot("a_map", a=("c1s10", "Mechelen'de", -0.35), tr=("fade", 0.8),
         cams=[(0.0, (3.0, 49.5, 3.0)), (("c1s10", "büyüdü", 0.0), (4.48, 51.03, 8.0))],
         regions=[dict(name="hollanda", color="burgonya", at=0.3, alpha=0.2)], extra=_ex_mechelen, label="mechelen"),
    # s11 — dört dil sözü (rivayet)
    shot("c1_dort_dil", a=("c1s11", -0.2), tr=("fade", 0.8), t_stamp=("c1s11", "Rivayete", -0.05),
         items=[dict(icon="cross", who="TANRI", lang="ESPAÑOL", t_who=("c1s11", "Tanrı'yla", -0.1), t_lang=("c1s11", "İspanyolca", -0.1)),
                dict(icon="c1_gul", metal="crimson", who="KADINLAR", lang="ITALIANO", t_who=("c1s11", "kadınlarla", -0.1), t_lang=("c1s11", "İtalyanca", -0.1)),
                dict(icon="sword", metal="silver", who="ERKEKLER", lang="FRANÇAIS", t_who=("c1s11", "erkeklerle", -0.1), t_lang=("c1s11", "Fransızca", -0.1)),
                dict(icon="c1_at", who="ATI", lang="DEUTSCH", t_who=("c1s11", "atıyla", -0.1), t_lang=("c1s11", "Almanca", -0.1))], label="dort_dil"),
    # s12 — söz: ölümünden ~43 yıl sonra yazıya geçti, belge bilinmiyor
    shot("quote", a=("c1s12", -0.2), tr=("fade", 0.8), size=60, wrap=1500, at=0.2, who="ŞARLKEN'E ATFEDİLEN SÖZ",
         text="Tanrı'yla İspanyolca, kadınlarla İtalyanca, erkeklerle Fransızca, atıyla Almanca konuşurdu.", label="soz_alinti"),
    shot("a_timeline_s", a=("c1s12", "ölümünden", -0.25), tr=("fade", 0.7), a0=1550, a1=1610, step=10, at=0.0,
         events=[(1558, "ÖLÜM", ("c1s12", "ölümünden", -0.1)), (1601, "İLK YAZILI KAYIT", ("c1s12", "yazıya", -0.15))],
         hl=(1558, 1601, "YAKLAŞIK 43 YIL", ("c1s12", "kırk", -0.2)),
         stampt=("BELGE BİLİNMİYOR", 960, 880, ("c1s12", "belge", 0.2), 70), label="43_yil"),
    # s13 — Fernando ölür; Şarlken anneyle birlikte kral
    shot("medal", a=("c1s13", -0.2), tr=("dip", 0.9), key=K.mkey("fernando", "ferdinand"), metal="onyx", name="FERNANDO", role="Aragonlu · Şarlken'in dedesi", dates="† 1516",
         pos="c", size=640, plate_at=("c1s13", "Fernando", 0.0), at=0.0, label="fernando_oldu"),
    shot("c1_ortak_kral", a=("c1s13", "Şarlken,", -0.2), tr=("fade", 0.8), a_karl=0.0, a_juana=("c1s13", "tutsak", -0.15), a_bars=("c1s13", "tutsak", 0.05), a_link=("c1s13", "birlikte", -0.15),
         a_k=("c1s13", "Kastilya", -0.1), a_a=("c1s13", "Aragon'un", -0.1), a_crown=("c1s13", "kralı", -0.15), label="ortak_kral"),
    # s14 — Eylül 1517 fırtınası; Santander yerine Tazones
    shot("a_theatre", a=("c1s14", -0.2), tr=("whip", 0.6), scene="sea",
         p=dict(mood="storm", lightning=0.85, rain=0.9,
                ships=[dict(kind="carrack", x=0.30, row=0, rock=1.0, flag="#8E1F26"), dict(kind="carrack", x=0.62, row=1, heading=-1, rock=1.0, flag="#8E1F26"),
                       dict(kind="carrack", x=0.50, row=2, rock=1.0, sails="torn", flag="#8E1F26"), dict(kind="carrack", x=0.12, row=2, rock=1.0, flag="#8E1F26"),
                       dict(kind="carrack", x=0.84, row=0, s=0.85, heading=-1, sails="torn", flag="#8E1F26")]),
         cams=[(0.0, (960, 540, 1.0)), (("c1s14", "yoldan", 0.0), (1010, 556, 1.2))], overlay=_storm_date, label="firtina"),
    shot("a_map", a=("c1s14", "Hedefleri", -0.3), tr=("fade", 0.8),
         cams=[(0.0, (-2.5, 47.0, 3.2)), (("c1s14", "küçük", -0.4), (-4.7, 44.2, 7.6))],
         routes=[dict(pts=ROTA_ANA, at=("c1s14", "Hedefleri", -0.1), dur=2.0, color="#9FB8C8", width=5, dash=(14, 12), arrow=False),
                 dict(pts=ROTA_GERCEK, at=("c1s14", "küçük", -0.1), dur=1.5, color="#F0D27A", width=7)],
         icons_=[dict(kind="ship", lon=-5.3, lat=47.9, size=84, at=("c1s14", "küçük", -0.1), route=ROTA_GERCEK, move_at=("c1s14", "küçük", -0.1), move_dur=1.5, metal="gold")],
         extra=_ex_tazones, label="tazones_rota"),
    shot("a_theatre", a=("c1s14", "Tazones'a", -0.2), tr=("fade", 0.7), scene="sea",
         p=dict(mood="dusk", coast="tazones", rain=0.25, ships=[dict(kind="carrack", x=0.30, row=0, rock=0.5, flag="#8E1F26"), dict(kind="carrack", x=0.52, row=1, rock=0.5, sails="reef", flag="#8E1F26")]),
         cams=[(0.0, (1000, 560, 1.0)), (("c1s15", "On", -0.3), (1180, 600, 1.4))], overlay=_tazones_overlay, label="tazones_koyu"),
    # s15 — 17 yaşında kral, yeni halkının dilini konuşamıyor
    shot("c1_halk", a=("c1s15", -0.2), tr=("fade", 0.8), a_q=(("c1s15", "halkının", 0.0), ("c1s15", "dilini", 0.0), ("c1s15", "iyi", -0.1)), label="yeni_halk"),
    # s16 — Valladolid Kortesi 1518
    shot("a_map", a=("c1s16", -0.2), tr=("fade", 0.8),
         cams=[(0.0, (-3.5, 41.0, 3.2)), (("c1s16", "1518'de", 0.0), (-4.72, 41.65, 8.0))],
         regions=[dict(name="c1_kastilya", color="ispanya", at=0.3, alpha=0.17)], need=("c1_kastilya",),
         date=("1518", ("c1s16", "1518'de", -0.1)), extra=_ex_valladolid, label="valladolid_harita"),
    shot("doc", a=("c1s16", "talebini", -0.3), tr=("fade", 0.8), title="VALLADOLID KORTESİ · 1518", w=1200, h=350, size=64, head_size=56, at=0.0, align="c", tone="#D2BE8E",
         lines=[("Kastilyacayı öğren.", ("c1s16", "Kastilyacayı", -0.1)), ("Yabancı danışmanlarını gönder.", ("c1s16", "yabancı", -0.1))],
         hl=(-sk.text_width("Kastilyacayı öğren.", "fell", 64, 0) / 2, -4, sk.text_width("Kastilyacayı öğren.", "fell", 64, 0)), hl_at=("c1s16", "öğren", -0.1), label="kortes_talebi"),
]
