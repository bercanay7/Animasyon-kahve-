"""Bölüm 4 — Worms'ta Bir Keşiş (114 sn). Ton: yargı salonu — petrol (Protestan) ↔ kırmızı (Habsburg); gerilim.
Özel çekim türleri: kinds_c4.py (c4_ önekli). Ortak yardımcılar: bw_lib.py. Simgeler: icons_b.py."""
from shots import shot
import scenes_lib  # noqa: F401  (theatre şablonu + sahne aileleri)
import kinds_c4
import icons_b  # noqa: F401
from bw_lib import anc
from sk import W, H

F = ("fade", 0.7)
D = ("dip", 0.9)

SHOTS = [
    # s1 — Nisan 1521. Worms.
    shot("map", a=("c4s1", 0.0), tr=F, cams=[(0.0, (9.0, 48.8, 2.9)), (("c4s1", "Worms", 0.0), (9.2, 50.2, 3.9))],
         regions=[dict(name="almanya", color="#7A6A3A", at=0.2, alpha=0.30, hatch=True)],
         labels=[dict(text="ALMANYA", lon=10.4, lat=51.9, size=38, color="#E8D8A0", track=16, at=("c4s1", "1521", 0.3))],
         cities=[dict(lon=8.36, lat=49.63, name="WORMS", kind="seat", at=("c4s1", "Worms", -0.3), side="l", size=44)],
         extra=kinds_c4.make_worms_pulse(("c4s1", "Worms", -0.2)),
         date=("NİSAN 1521", ("c4s1", "Nisan", 0.0)), label="worms_harita"),
    # s2a — Reichstag salonu: imparator tahtta, karşısında küçük keşiş
    shot("bw_theatre", a=("c4s2", -0.4), tr=("fade", 0.4), scene="reichstag", dust_n=36, cams=[(0.0, (960, 600, 1.0)), (("c4s2", "bir", 1, 0.2), (960, 700, 1.45))],
         p=dict(monk=True, emperor=True, books=True, crowd=True, monk_z=1000), label="reichstag"),
    # s2b — Karl ↔ Luther
    shot("c4_duel", a=("c4s2", "bir", 1, -0.15), tr=("zoom", 0.6),
         left=dict(key="karl_genc", name="V. KARL", role="İmparator · 21 yaşında", at=0.2, metal="gold"),
         right=dict(key="luther", name="MARTİN LUTHER", role="Keşiş", at=("c4s2", "keşiş", -0.1), plate_at=("c4s2", "Martin", -0.15), metal="teal", flip=True),
         vs_at=("c4s2", "Martin", 0.0), label="karl_luther"),
    # s3a — 95 madde
    shot("c4_theses", a=("c4s3", -0.25), tr=F, at=0.0, year_at=0.5, against_at=("c4s3", "günah", -0.1), slash_at=("c4s3", "karşı", -0.1),
         count_at=("c4s3", "doksan", -0.1), write_at=("c4s3", "maddelik", -0.2), write_dur=2.4, label="95_madde"),
    # s3b — matbaa: Wittenberg'den Almanya'ya
    shot("map", a=("c4s3", "Matbaa", -0.2), tr=F, cams=[(0.0, (10.2, 50.8, 3.3)), (("c4s4", 0.0), (10.0, 50.6, 3.7))],
         regions=[dict(name="almanya", color="#7A6A3A", at=0.0, alpha=0.26, hatch=True)],
         cities=[dict(lon=12.65, lat=51.87, name="WİTTENBERG", kind="town", at=("c4s3", "Matbaa", -0.2), side="r", size=34)],
         extra=kinds_c4.make_spread(("c4s3", "Matbaa", 0.0), ("c4s3", "bu", -0.3)), approx=False, label="matbaa_yayildi"),
    # s4 — güvenli geçiş: yirmi bir gün
    shot("c4_safeconduct", a=("c4s4", -0.25), tr=F, at=0.0, seal_at=("c4s4", "sözü", 0.0), days_at=("c4s4", "yirmi", -0.12), days_dur=0.62, label="guvenli_gecis"),
    # s5 — kitaplar masada
    shot("c4_books", a=("c4s5", 0.0), tr=("fade", 0.4), drop_at=("c4s5", "kitaplarını", -0.15), drop_dt=0.2, q1_at=("c4s5", "senin", -0.1), q2_at=("c4s5", "Hepsinden", -0.1), label="kitaplar"),
    # s6 — bir gün süre; Almanca → Latince; vazgeçmiyor
    shot("c4_answer", a=("c4s6", -0.2), tr=F, day_at=("c4s6", "gün", -0.4), flip_at=("c4s6", "Ertesi", -0.1), de_at=("c4s6", "Almanca", -0.3), la_at=("c4s6", "Latince", -0.3), hold_at=("c4s6", "vazgeçmiyordu", -0.1), label="almanca_latince"),
    # s7 — Ben buradayım: RİVAYET / TUTANAKTA YOK / SONRADAN EKLENMİŞ
    shot("c4_protocol", a=("c4s7", -0.2), tr=F,
         words=[("Ben", ("c4s7", "Ben", -0.05)), ("buradayım,", ("c4s7", "buradayım", -0.05)), ("başka", ("c4s7", "başka", -0.05)), ("türlü", ("c4s7", "türlü", -0.05)), ("yapamam", ("c4s7", "yapamam", -0.05))],
         ghost_at=("c4s7", "büyük", -0.1), rumor_at=("c4s7", "ihtimalle", 0.0), swap_at=("c4s7", "Resmî", -0.35), gap_at=("c4s7", "tutanakta", -0.4),
         add_at=("c4s7", "sonradan", -0.2), stamp1_at=("c4s7", "tutanakta", 0.0), stamp2_at=("c4s7", "sonradan", 0.0), label="tutanakta_yok"),
    # s8 — ertesi sabah: bildiri okundu
    shot("c4_dawn_scroll", a=("c4s8", -0.2), tr=F, at=0.0, unroll_at=("c4s8", "imparatorun", -0.3), read_at=("c4s8", "yazılı", -0.2), seal_at=("c4s8", "okundu", 0.0), label="bildiri"),
    # s9 — atalar
    shot("c4_ancestors", a=("c4s9", -0.2), tr=F, ger_at=("c4s9", "Alman", -0.2), esp_at=("c4s9", "İspanya", -0.2), bur_at=("c4s9", "Burgonya", -0.2),
         keys_at=("c4s9", "Roma", -0.15), chain_at=("c4s9", "Kilisesi", -0.1), label="atalar"),
    # s10 — bin yıllık Hıristiyanlık, tek keşiş
    shot("bw_theatre", a=("c4s10", -0.2), tr=F, scene="c4_nave", cams=[(0.0, (960, 560, 1.0)), (("c4s10", "yanılıyor", 0.3), (960, 600, 1.34))], p=dict(), dust_n=60,
         overlay=lambda cx: kinds_c4.nave_overlay(cx, ("c4s10", "bin", -0.1), ("c4s10", "tek", -0.1), ("c4s10", "yanılıyor", -0.1)), label="bin_yil"),
    # s11 — krallıklar, dostlar, beden, kan, can, ruh
    shot("c4_pledge", a=("c4s11", -0.2), tr=F,
         items=[("KRALLIKLAR", "crown", "gold", ("c4s11", "krallıklarını", -0.25)), ("DOSTLAR", "b_friends", "silver", ("c4s11", "dostlarını", -0.25)),
                ("BEDEN", "b_body", "bronze", ("c4s11", "bedenini", -0.25)), ("KAN", "b_drop", "crimson", ("c4s11", "kanını", -0.25)),
                ("CAN", "b_heart", "crimson", ("c4s11", "canını", -0.25)), ("RUH", "b_flame", "gold", ("c4s11", "ruhunu", -0.25))],
         settle_at=("c4s11", "ortaya", -0.1), line_at=("c4s11", "yazdı", -0.4), label="alti_sey"),
    # s12 — Worms Fermanı: geriye dönük tarihli
    shot("c4_backdate", a=("c4s12", -0.2), tr=F, at=0.0, leave_at=("c4s12", "Luther", -0.1), sign_at=("c4s12", "imzalandı", -0.1), back_at=("c4s12", "ama", 0.0), stamp_at=("c4s12", "geriye", -0.1), label="ferman_geriye"),
    # s13 — kanun dışı
    shot("c4_banned", a=("c4s13", -0.2), tr=F, outlaw_at=("c4s13", "kanun", -0.1),
         rows=[("OKUMAK", "book", "ivory", ("c4s13", "okumak", 0.0)), ("BASMAK", "b_press", "gold", ("c4s13", "basmak", 0.0)), ("SATMAK", "coin", "gold", ("c4s13", "satmak", 0.0))], label="yasak"),
    # s14a — gece yolu
    shot("bw_theatre", a=("c4s14", -0.2), tr=D, scene="road_night", dust_n=36, cams=[(0.0, (960, 540, 1.0)), (("c4s14", "korumak", 0.0), (1000, 560, 1.3))], p=dict(riders=4, torches=4, rain=0.0, mountains=True, walk=16, fog=0.5), overlay=kinds_c4.road_overlay(("c4s14", "kaçırıldı", -0.15), 0), label="gece_yolu"),
    # s14b — Saksonya Seçmeni'nin adamları
    shot("bw_medal", a=("c4s14", "korumak", -0.35), tr=F, key="frederik_bilge", metal="teal", name="SAKSONYA SEÇMENİ", role="Frederik", pos="c", size=640, plate_at=("c4s14", "Saksonya", -0.2), label="seçmen"),
    # s15a — Wartburg: Şövalye Jörg
    shot("bw_theatre", a=("c4s15", -0.25), tr=D, scene="tower", dust_n=36, cams=[(0.0, (960, 560, 1.0)), (("c4s15", "Orada", 0.0), (960, 520, 1.35))], p=dict(variant="wartburg", night=True, figure="writer", candle=1.0), overlay=kinds_c4.wartburg_overlay(("c4s15", "Wartburg", -0.1), ("c4s15", "Şövalye", -0.15)), label="wartburg"),
    # s15b — Yeni Ahit Almancaya
    shot("c4_book", a=("c4s15", "Orada", -0.3), tr=F, head_at=("c4s15", "Yeni", -0.1), de_at=("c4s15", "Almancaya", -0.2), write_at=("c4s15", "Almancaya", 0.0), write_dur=1.5, label="yeni_ahit"),
    # s16 — fikri durduramadı
    shot("c4_finale", a=("c4s16", -0.25), tr=F, seal_at=("c4s16", "yazdırdı", 0.0), ignite_at=("c4s16", "ama", 0.0), label="fikir"),
]
