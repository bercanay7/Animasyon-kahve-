"""Bölüm 5 — İmparator Hep Başka Yerde (104 sn). Ton: yol/kervan — toprak, duman; sonunda salon (c0'a dönüş).
Özel çekim türleri: kinds_c5.py (c5_ önekli). Ortak yardımcılar: bw_lib.py. Simgeler: icons_b.py. Atlı siluet: rider_b.py."""
from shots import shot
import scenes_lib  # noqa: F401  (theatre şablonu + sahne aileleri)
import kinds_c5
import icons_b  # noqa: F401
from bw_lib import anc, fadeout, tag
from sk import W, H

F = ("fade", 0.7)
D = ("dip", 0.9)
WH = ("whip", 0.6)


def _night_label(cx):
    f = cx.f
    k = cx.amt(("c5s12", "Innsbruck'tan", -0.1), 0.7)
    if k > 0:
        tag(f, "İNNSBRUCK  ·  GECE", 330, H - 120, size=30, alpha=k, track=10)


def _hall_out(cx):
    fadeout(cx, 1.0)


PEAS_P = dict(ground="plain", weather="dusk", smoke=0.8, fire=0.45,
              armies=[dict(side="#6A4A26", kind="peasants", x=0.40, row=0, n=20, dir=1, charge=0.5), dict(side="#6A4A26", kind="peasants", x=0.72, row=1, n=26, dir=-1, charge=0.35),
                      dict(side="#6A4A26", kind="peasants", x=0.2, row=2, n=30, dir=1, charge=0.3)])
FIELD_P = dict(ground="river", weather="fog", river=True, smoke=0.35,
               armies=[dict(side="#8E1F26", kind="cavalry", x=0.30, row=1, n=9, dir=1, charge=0.7, ford=True), dict(side="#8E1F26", kind="pike", x=0.52, row=1, n=22, dir=1, charge=0.5, ford=True),
                       dict(side="#1E5560", kind="pike", x=0.68, row=2, n=26, dir=-1, charge=0.2), dict(side="#1E5560", kind="arquebus", x=0.40, row=2, n=14, dir=-1, charge=0.1)])

SHOTS = [
    # s1 — Almanya'dan ayrıldı, dokuz yıl dönemedi
    shot("map", a=("c5s1", 0.0), tr=F, cams=[(0.0, (6.5, 47.2, 1.7)), (("c5s1", "ayrıldı", 0.0), (4.6, 46.0, 2.0))],
         regions=[dict(name="almanya", color="#7A6A3A", at=0.2, alpha=0.30, hatch=True), dict(name="ispanya", color="ispanya", at=("c5s1", "ayrıldı", 1.2), alpha=0.45)],
         labels=[dict(text="ALMANYA", lon=10.3, lat=49.0, size=36, track=14, at=0.6)],
         cities=[dict(lon=8.36, lat=49.63, name="WORMS", kind="seat", at=0.3, side="r", size=34)],
         extra=kinds_c5.make_leave(("c5s1", "ayrıldı", -0.1), ("c5s1", "Dokuz", -0.05), ("c5s1", "dönemedi", -0.1)), label="almanyadan_ayrildi"),
    # s2 — İspanya karışık, Fransa saldırıyor, Akdeniz'de Osmanlı: üç ok
    shot("map", a=("c5s2", -0.3), tr=F, cams=[(0.0, (13.0, 44.5, 1.38)), (("c5s2", "vardı", 0.0), (13.0, 44.7, 1.4))],
         regions=[dict(name="ispanya", color="ispanya", at=("c5s2", "İspanya", -0.1), alpha=0.5), dict(name="fransa", color="fransa", at=("c5s2", "Fransa", -0.1), alpha=0.5),
                  dict(name="osmanli_1520", color="osmanli", at=("c5s2", "Osmanlı", -0.1), alpha=0.5)],
         extra=kinds_c5.make_pressure(("c5s2", "İspanya", 0.0), ("c5s2", "Fransa", 0.0), ("c5s2", "Akdeniz'de", 0.0)), label="uc_cephe"),
    # s3a — Luther'in fikirleri yayıldı
    shot("c5_ideas", a=("c5s3", -0.2), tr=F, tag_at=("c5s3", "Luther'in", 0.0), label="fikirler_yayildi"),
    # s3b — 1524, Köylü Savaşı
    shot("bw_theatre", a=("c5s3", "1524'te", -0.4), tr=WH, scene="field", cams=[(0.0, (960, 560, 1.0)), (("c5s3", "Luther", 1, -0.2), (900, 600, 1.25))],
         p=PEAS_P,
         overlay=kinds_c5.peasants_overlay(("c5s3", "1524'te", 0.0), ("c5s3", "Köylü", -0.1), None, None), label="koylu_savasi"),
    # s3c — Luther istememişti; 70–100 bin
    shot("bw_theatre", a=("c5s3", "Luther", 1, -0.3), tr=F, scene="field", cams=[(0.0, (900, 600, 1.25)), (("c5s3", "öldü", 0.0), (860, 620, 1.4))],
         p=PEAS_P,
         overlay=kinds_c5.peasants_overlay(None, None, ("c5s3", "Luther", 1, -0.1), ("c5s3", "yetmiş", -0.15)), label="luther_istememisti"),
    # s4 — Speyer 1529: Worms Fermanı yeniden yürürlükte
    shot("c5_speyer", a=("c5s4", -0.3), tr=F, year_at=("c5s4", "1529'da", -0.1), city_at=("c5s4", "Speyer'de", -0.1), maj_at=("c5s4", "çoğunluk", -0.6),
         ferman_at=("c5s4", "Worms", -0.3), stamp_at=("c5s4", "yeniden", -0.05), label="speyer"),
    # s5 — itiraz → protesto → Protestan
    shot("c5_protest", a=("c5s5", -0.25), tr=F, prince_at=("c5s5", "Birkaç", -0.1), city_at=("c5s5", "on", -0.15), objection_at=("c5s5", "itiraz", -0.15),
         protesto_at=("c5s5", "protesto", -0.25), protestan_at=("c5s5", "Protestan", -0.1), label="protestan"),
    # s6a — 1530 Augsburg: inanç beyanı imparatora sunuldu
    shot("c5_confession", a=("c5s6", -0.25), tr=F, year_at=("c5s6", "1530'da", -0.1), city_at=("c5s6", "Augsburg'da", -0.2), seal_at=("c5s6", "Protestanlar", 0.0),
         write_at=("c5s6", "inançlarını", 0.0), offer_at=("c5s6", "imparatora", -0.15), label="augsburg_itirafi"),
    # s6b — ana yazar: Melanchthon
    shot("c5_authors", a=("c5s6", "Metnin", -0.3), tr=F, at=0.0, luther_at=("c5s6", "Luther", -0.1), mel_at=("c5s6", "Melanchthon'du", -0.3), label="ana_yazar"),
    # s7a — dinledi ama kabul etmedi
    shot("c5_refuse", a=("c5s7", -0.25), tr=F, at=0.0, listen_at=("c5s7", "dinledi", -0.1), no_at=("c5s7", "ama", -0.05), stamp_at=("c5s7", "kabul", 0.0), label="kabul_etmedi"),
    # s7b — Şmalkalden Birliği
    shot("c5_league", a=("c5s7", "Prensler", -0.3), tr=F, shield_at=("c5s7", "Prensler", -0.15), name_at=("c5s7", "Şmalkalden", -0.1),
         close_at=("c5s7", "Birliği'ni", -0.2), flash_at=("c5s7", "kurdu", -0.05), label="smalkalden"),
    # s8 — ancak cepheler yatışınca, 1546'da savaş
    shot("c5_wait", a=("c5s8", -0.3), tr=F, at=0.0, fr_at=("c5s8", "Fransa", -0.2), ot_at=("c5s8", "Osmanlı", -0.2), calm_at=("c5s8", "yatışınca", -0.2), war_at=("c5s8", "1546'da", -0.1), label="yatisinca_1546"),
    # s9a — Mühlberg, 24 Nisan 1547; sisli sabah; Elbe geçişi (parşömen savaş planı)
    shot("c5_plan", a=("c5s9", -0.3), tr=F, at=0.0, date_at=("c5s9", "Nisan", -0.4), river_at=("c5s9", "1547'de", 0.0), city_at=("c5s9", "Mühlberg'de", -0.15),
         army_at=("c5s9", "Mühlberg'de", 0.5), fog_at=("c5s9", "sisli", -0.3), cross_at=("c5s9", "Elbe", -0.25), label="muhlberg_plan"),
    # s9b — Protestan ordusu dağıldı
    shot("bw_theatre", a=("c5s9", "geçti", 0.15), tr=F, scene="field", cams=[(0.0, (960, 560, 1.0)), (("c5s9", "dağıttı", 0.0), (1000, 580, 1.3))],
         p=FIELD_P, label="sis_elbe"),
    # s9c — Saksonya Seçmeni esir düştü
    shot("medal", a=("c5s9", "Saksonya", -0.35), tr=D, key="johann_friedrich", metal="teal", name="SAKSONYA SEÇMENİ", role="Johann Friedrich", pos="c", size=640,
         plate_at=("c5s9", "Saksonya", -0.1), stampt=("ESİR", 1330, 330, ("c5s9", "esir", -0.1), 84), label="secmen_esir"),
    # s10 — Tiziano, bir yıl sonra: altın çerçevede atlı imparator
    shot("c5_titian", a=("c5s10", -0.3), tr=F, at=0.0, year_at=("c5s10", "bir", -0.1), frame_at=("c5s10", "imparatoru", -0.6), symbol_at=("c5s10", "zaferin", -0.1),
         paint_at=("c5s10", "resmetti", -0.1), armor_at=("c5s10", "zırhlı", -0.05), alone_at=("c5s10", "tek", -0.1), label="tiziano_cerceve"),
    # s11 — zafer kısa sürdü; 1552 Moritz
    shot("c5_moritz", a=("c5s11", -0.2), tr=D, short_at=("c5s11", "Zafer", -0.05), year_at=("c5s11", "1552'de", -0.1), ally_at=("c5s11", "müttefiki", -0.3), snap_at=("c5s11", "karşı", -0.2), label="moritz"),
    # s12 — Innsbruck, gece kaçış (sedye yok: meşaleli atlı kafile)
    shot("bw_theatre", a=("c5s12", -0.2), tr=D, scene="road_night", cams=[(0.0, (960, 560, 1.0)), (("c5s12", "kaldı", 0.0), (1000, 560, 1.28))],
         p=dict(riders=5, torches=5, rain=0.45, mountains=True, litter=False, walk=11, fog=0.6, dir=-1), overlay=_night_label, label="innsbruck_gece"),
    # s13 — Augsburg Barışı, Eylül 1555
    shot("c5_peace", a=("c5s13", -0.2), tr=D, at=0.0, date_at=("c5s13", "Eylül", -0.1), title_at=("c5s13", "Augsburg", -0.1), seal_at=("c5s13", "imzalandı", -0.1),
         luther_at=("c5s13", "Lutherciliğe", -0.2), open_at=("c5s13", "yer", -0.25), label="augsburg_barisi"),
    # s14 — Barışı o yapmadı; kardeşi Ferdinand yürüttü
    shot("medal", a=("c5s14", -0.25), tr=F, key="ferdinand", name="FERDİNAND", role="Kardeşi · yürüten", pos="c", size=640, plate_at=("c5s14", "Ferdinand", -0.35), label="ferdinand"),
    # s15 — Tam bir ay sonra, o büyük salonda (c0 ile aynı sahne): siyaha çözülür
    shot("bw_theatre", a=("c5s15", -0.3), tr=F, scene="hall", cams=[(0.0, (960, 540, 1.0)), (("c5s15", "duruyordu", 0.6), (975, 600, 1.16))], p=dict(),
         overlay=_hall_out, label="salon_son"),
]
