"""c8 — Aslanın İni (1478–1481). PARÇA 4 AÇILIŞI (bölüm kartsız; ilk çekimin orta bandı boş: Program başlık bindirmesi 1,2–4,8 sn). Yönetmen kartı: yonetmen_c8.md.
Renk anahtarı: deniz lacivert + altın (diplomasi) + Doğu turuncu/kızılı (yalnız donanma, mimari, alev) + kâğıt sarısı (Bandini/Leonardo çizgisi) + kurşun grisi (aforoz).
Tüm çekimler cümle/sözcük çapalı (mutlak saniye yok). Mizah: kuruma/usule (bulla üslubu, yetki sonradan, Yetmişler, madalya); KAPALI: Bandini/Leonardo, Otranto.
"""
from shots import shot
import cilt_medici as CM
import p4_lib as L
import c8_kinds as K
look = L.look

SHOTS = [
    # ── 1. Floransa silueti (bağlam; Pazzi şiddeti tekrar gösterilmez) ─────────────────────────
    shot("p4_skyline", ("c8s1", 0), seed=3, tod="dusk", mode="night", perde=2, cam=("pan", "r", 380), label="Floransa silueti, alacakaranlık"),
    # ── 2. Aforoz belgesi: tomar açılır, satırlar yazılır, kurşun mühür basılır ───────────────
    shot("c8_aforoz", ("c8s1", "Haziran", -0.35), phase="giris", mode="night", perde=2, unroll_at=("c8s1", "Haziran", -0.3), imp_at=("c8s1", "aforoz", 0.05),
         cam=[(("c8s1", "Haziran", -0.35), look(960, 330, 1.22)), (("c8s1", "Sixtus", 0.0), look(960, 420, 1.02)), (("c8s1", "aforoz", -0.2), look(960, 560, 1.12)), (("c8s1", "geçmeden", 0.0), look(960, 540, 1.0))],
         ovl=L.ov(L.date_plate("HAZİRAN 1478", ("c8s1", "Haziran", 0.0), out=("c8s1", "geçmeden", 0.3)),
                  L.tag("PAPA IV. SIXTUS", 1700, 470, ("c8s1", "IV.", 0.0), size=32, w=420, out=("c8s1", "aforoz", 0.9)),
                  L.stamp("AFOROZ", 1330, 640, ("c8s1", "etti;", -0.1), size=66, rot=-0.10, out=("c8s1", "yasak,", 0.2))),
         tr=("carry", 0.9, dict(strip="paper", dir="l")), link="carry", label="aforoz belgesi, kurşun mühür"),
    # ── 3. Interdikt: mühür şehri örter (yasak) ─────────────────────────────────────────────
    shot("p4_skyline", ("c8s1", "Floransa'ya", -0.1), seed=5, tod="dusk", mode="night", perde=2, dir=-1, cam=("pan", "l", 300),
         ovl=L.ov(K.interdikt(("c8s1", "yasak,", -0.9), ("c8s1", "interdikt", -0.15)), L.dim(("c8s1", "yani", 0.0), alpha=0.28, dur=1.2)),
         tr=("iris", 0.9, dict(obj="seal", at=K.BULLA_REST, r=K.BULLA_R + 6)), link="shape", label="interdikt: şehir sessizleşir"),
    # ── 4. Latince satır: kötülüğün oğlu ve yıkımın evladı ─────────────────────────────────
    shot("c8_aforoz", ("c8s2", -0.2), phase="satir", mode="night", perde=2, imp_at=None, line_at=("c8s2", "alışılmış", -0.3), tr_at=("c8s2", "kötülüğün", -0.1),
         cam=[(("c8s2", -0.2), look(960, 420, 1.35)), (("c8s2", "üslupla,", 0.0), look(900, 430, 1.75)), (("c8s2", "evladı”", 0.0), look(960, 500, 1.55))],
         ovl=L.ov(L.stamp("○ TEK KAYNAK", 1500, 250, ("c8s2", "Aktarıldığına", 0.2), size=44, rot=-0.08)),
         tr=("zoomthru", 0.9, dict(at=(960, 560), at_b=(960, 420))), link="scale", label="Latince satır ve çeviri"),
    # ── 5. Napoli Kralı Ferrante Papa'nın yanında savaşa girdi (harita: oklar Toskana'ya, sağdan sola/yukarı) ──
    shot("p4_map", ("c8s3", -0.2), mode="day", perde=2, cam=("push", 0.05), approx=False,
         cams=[(("c8s3", -0.2), (13.9, 41.7, 4.3)), (("c8s3", "savaşa", 0.2), (12.9, 42.6, 5.0)), (("c8s3", "ordunun", 0.0), (12.2, 43.1, 5.6))],
         cities=[dict(lon=14.2681, lat=40.8518, name="NAPOLİ", kind="capital", at=("c8s3", "Napoli", -0.1), size=34), dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c8s3", "ordunun", -0.5), size=34, side="l")],
         icons_=[dict(kind="crown", lon=14.27, lat=41.28, size=84, at=("c8s3", "Kralı", 0.0), metal="gold"), dict(kind="keys", lon=12.4964, lat=41.9028, size=88, at=("c8s3", "Papa'nın", 0.0), metal="gold")],
         routes=[dict(pts=[(14.2681, 40.9), (13.35, 41.5), (12.55, 42.25), (11.95, 42.95), (11.45, 43.45)], at=("c8s3", "savaşa", -0.2), dur=1.8, color="#A8321E", width=9.0),
                 dict(pts=[(12.64, 43.73), (12.15, 43.62), (11.75, 43.50), (11.45, 43.45)], at=("c8s3", "ordunun", 0.2), dur=1.3, color="#A8321E", width=7.0)],
         tr=("carry", 0.9, dict(strip="ink", dir="l")), link="carry", label="harita: Napoli ve Papalık Toskana'ya"),
    # ── 6. Ordunun başında Alfonso, generali Federico (alay sağdan sola) ───────────────────────
    shot("p4_procession", ("c8s3", "ordunun", -0.1), dir="l", density=1.25, speed=150.0, seed=6, mode="day", perde=2, cam=("pan", "l", 520),
         mix=dict(rider=0.32, noble=0.10, page=0.0, banner=0.26, guard=0.28, elder=0.0, cleric=0.0, common=0.04),
         ovl=L.ov(L.tag("ALFONSO", 1320, 810, ("c8s3", "Alfonso,", -0.15), size=36, w=420, sub="FERRANTE'NİN OĞLU", out=("c8s3", "generali", 0.2)),
                  L.tag("FEDERICO DA MONTEFELTRO", 640, 810, ("c8s3", "Federico", -0.2), size=34, w=700, sub="URBINO'DAN · GENERAL")),
         tr=("slide", 0.8, dict(dir="l")), link="dir", label="ordu yürür (Alfonso, Federico)"),
    # ── 7. Siena geçişe izin verdi; Chianti'de kaleler alındı ───────────────────────────────────
    shot("p4_map", ("c8s4", -0.15), mode="day", perde=2, cam=("push", 0.06), approx=False,
         cams=[(("c8s4", -0.15), (11.42, 43.28, 12.0)), (("c8s4", "Alfonso", 0.0), (11.30, 43.45, 14.5)), (("c8s4", "aldı.", 0.0), (11.25, 43.5, 15.5))],
         cities=[dict(lon=11.3308, lat=43.3188, name="SIENA", kind="town", at=("c8s4", "Siena", -0.1), size=32, color="#8A6A9E"), dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c8s4", "Siena", 0.0), size=32, side="l")],
         labels=[dict(text="CHIANTI", lon=11.30, lat=43.52, size=44, track=16, at=("c8s4", "Chianti'ye", -0.2), color="#5A3E1E", face="title_m")],
         routes=[dict(pts=[(11.55, 43.05), (11.40, 43.22), (11.33, 43.32), (11.30, 43.42), (11.27, 43.55)], at=("c8s4", "izin", -0.3), dur=1.9, color="#A8321E", width=9.0)],
         icons_=[dict(kind="castle", lon=11.37, lat=43.49, size=62, at=("c8s4", "kaleleri", -0.1), metal="gold"), dict(kind="castle", lon=11.29, lat=43.47, size=62, at=("c8s4", "kaleleri", 0.25), metal="gold"),
                 dict(kind="castle", lon=11.22, lat=43.53, size=62, at=("c8s4", "aldı.", -0.2), metal="gold")],
         tr=("slide", 0.8, dict(dir="l")), link="dir", label="Siena geçit verir, Chianti kaleleri"),
    # ── 8. Poggio Imperiale yenilgisi, Colle'nin düşüşü ──────────────────────────────────────
    shot("p4_map", ("c8s5", -0.15), mode="day", perde=2, cam=("push", 0.05), approx=False,
         cams=[(("c8s5", -0.15), (11.2, 43.55, 13.0)), (("c8s5", "Floransa", 0.0), (11.17, 43.60, 15.0)), (("c8s5", "Colle", 0.0), (11.14, 43.47, 17.0)), (("c8s5", "düştü.", 0.0), (11.14, 43.45, 17.5))],
         cities=[dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c8s5", "sonbaharında", 0.0), size=32, side="r"),
                 dict(lon=11.1469, lat=43.4684, name="POGGIO IMPERIALE", kind="battle", at=("c8s5", "Poggio", -0.2), size=30, side="l"),
                 dict(lon=11.1177, lat=43.4233, name="COLLE VAL D'ELSA", kind="siege", at=("c8s5", "Colle", -0.2), size=30, side="l")],
         routes=[dict(pts=[(11.255, 43.74), (11.20, 43.62), (11.16, 43.52), (11.147, 43.47)], at=("c8s5", "Floransa", 0.0), dur=1.2, color="#233C8C", width=8.0)],
         extra=L.mx(L.mimpact(11.1469, 43.4684, ("c8s5", "yenildi;", -0.4)), L.marrow([(11.147, 43.47), (11.18, 43.58), (11.23, 43.68)], ("c8s5", "yenildi;", 0.0), dur=1.0, color="#233C8C", width=6.0, dash=(14, 10)),
                    L.mimpact(11.1177, 43.4233, ("c8s5", "ardından", -0.1), color="#8E2A1E", n=2)),
         date=("SONBAHAR 1479", ("c8s5", "1479", 0.0)),
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="Poggio Imperiale, Colle"),
    # ── 9. Savaş masrafı hazineyi boşaltıyordu ───────────────────────────────────────────────
    shot("c8_kasa", ("c8s6", -0.1), mode="night", perde=2, cam=("push", 0.07), close_at=("c8s6", "boşaltıyordu.", 0.45),
         tr=("light", 0.8, dict(at=(960, 760))), link="light", label="hazine boşalır, kapak çarpar"),
    shot("black", ("c8s7", 0), text="[devam]", label="yer tutucu"),
]
YIL_AT = [(("c8s1", 0), 1478)]
