"""c8 — Aslanın İni (1478–1481). PARÇA 4 AÇILIŞI (bölüm kartsız; ilk çekimin orta bandı boş: Program başlık bindirmesi 1,2–4,8 sn). Yönetmen kartı: yonetmen_c8.md.
Renk anahtarı: deniz lacivert + altın (diplomasi) + Doğu turuncu/kızılı (yalnız donanma, mimari, alev) + kâğıt sarısı (Bandini/Leonardo çizgisi) + kurşun grisi (aforoz).
Tüm çekimler cümle/sözcük çapalı (mutlak saniye yok). Mizah: kuruma/usule (bulla üslubu, yetki sonradan, Yetmişler, madalya); KAPALI: Bandini/Leonardo, Otranto.
"""
from shots import shot
import cilt_medici as CM
import p4_lib as L
import c8_kinds as K
look = L.look

ROTA_FN = [(11.2558, 43.7696), (11.9, 42.95), (12.75, 41.95), (13.5, 41.2), (14.2681, 40.87)]

SHOTS = [
    # ── 1. Floransa silueti (bağlam; Pazzi şiddeti tekrar gösterilmez) ─────────────────────────
    shot("p4_skyline", ("c8s1", 0), seed=3, tod="dusk", mode="night", perde=2, cam=("pan", "r", 380), label="Floransa silueti, alacakaranlık"),
    # ── 2. Aforoz belgesi: tomar açılır, satırlar yazılır, kurşun mühür basılır ───────────────
    shot("c8_aforoz", ("c8s1", "Haziran", -0.35), phase="giris", mode="night", perde=2, unroll_at=("c8s1", "Haziran", -0.3), imp_at=("c8s1", "aforoz", 0.05),
         cam=[(("c8s1", "Haziran", -0.35), look(960, 330, 1.22)), (("c8s1", "Sixtus", 0.0), look(960, 420, 1.02)), (("c8s1", "aforoz", -0.2), look(960, 560, 1.12)), (("c8s1", "geçmeden", 0.0), look(960, 540, 1.0))],
         ovl=L.ov(L.date_plate("HAZİRAN 1478", ("c8s1", "Haziran", 0.0), out=("c8s1", "geçmeden", 0.3)),
                  L.tag("PAPA IV. SIXTUS", 1700, 470, ("c8s1", "IV.", 0.0), size=32, w=420, out=("c8s1", "aforoz", 0.9)),
                  L.stamp("AFOROZ", 1330, 640, ("c8s1", "etti;", -0.1), size=66, rot=-0.10, out=("c8s1", "yasak,", 0.2))),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="aforoz belgesi, kurşun mühür"),
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
         tr=("zoomthru", 0.9, dict(at=(960, 700), at_b=(960, 540))), link="scale", label="Siena geçit verir, Chianti kaleleri"),
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
    # ── 10. 6 Aralık 1479: Lorenzo Floransa'dan düşman kralın yanına (harita; rozet yürür) ─────────
    shot("p4_map", ("c8s7", -0.1), mode="day", perde=2, cam=("push", 0.05), approx=False,
         cams=[(("c8s7", -0.1), (11.9, 43.2, 6.6)), (("c8s7", "ayrılıp", 0.0), (12.5, 42.5, 5.4)), (("c8s7", "Napoli'ye", 0.0), (13.4, 41.9, 4.7))],
         cities=[dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c8s7", 0.3), size=34, side="l"), dict(lon=14.2681, lat=40.8518, name="NAPOLİ", kind="capital", at=("c8s7", "kralın", -0.2), size=34)],
         icons_=[dict(kind="crown", lon=14.27, lat=41.28, size=84, at=("c8s7", "kralın", 0.0), metal="gold")],
         routes=[dict(pts=ROTA_FN, at=("c8s7", "ayrılıp", -0.3), dur=2.5, color="#233C8C", width=9.0, dash=(22, 12))],
         extra=L.mbadge(ROTA_FN, ("c8s7", "ayrılıp", -0.3), dur=2.5), date=("6 ARALIK 1479", ("c8s7", 0.1)),
         tr=("sayfa", 0.8), link="material", label="harita: Floransa → Napoli (6 Aralık 1479)"),
    # ── 11. Pisa mektubu: yazıp bildirdi; Signoria elçilik ve tam yetki verdi (anlatılır) ──────────
    shot("p4_letter", ("c8s8", -0.1), addr=("Signoria'ya",), lines=(), seal_at=("c8s8", "yazıp", -0.1), mode="day", perde=2, cam=("push", 0.08),
         ovl=L.ov(L.tag("PİSA · ARALIK 1479", 960, 190, ("c8s8", 0.0), size=40, w=640, out=("c8s8", "elçilik", 0.4)),
                  L.tag("ELÇİLİK", 560, 830, ("c8s8", "elçilik", -0.1), size=40, w=360), L.tag("TAM YETKİ", 1360, 830, ("c8s8", "tam", -0.1), size=40, w=420),
                  L.stamp("○ TEK KAYNAK", 1500, 300, ("c8s8", "anlatılır.", -0.3), size=44, rot=-0.08)),
         tr=("zoomthru", 0.9, dict(at=(1080, 760), at_b=(960, 540))), link="scale", label="Pisa mektubu, Signoria'nın yetkisi"),
    # ── 12. Önce yola çıktı, yetkiyi sonra aldı (usul mizahı: yetki geriden geç gelir) ───────────
    shot("p4_deniz_rota", ("c8s9", -0.1), tod="day", ship_kind="kadirga", flag="toskana", scale=0.9, thread=True, mode="day", perde=2,
         route=[(240, 664), (900, 620), (1700, 590), (2500, 560)], labels=[dict(name="PİSA", at_xy=(300.0, 300.0), f=0.40, t=("c8s9", -0.1), dy=-90)],
         ovl=L.ov(L.tag("1 · YOLA ÇIKTI", 1420, 250, ("c8s9", "yola", -0.1), size=38, w=520, out=("c8s9", "diplomasi", 0.3)), K.late_scroll(("c8s9", "sonra", -0.25), 330, 520),
                  L.tag("2 · YETKİ", 330, 700, ("c8s9", "yetkiyi", 0.0), size=36, w=380, out=("c8s9", "diplomasi", 0.3)), L.stamp("YORUM", 1500, 800, ("c8s9", "diplomasi", 0.0), size=46, rot=-0.07)),
         tr=("slide", 0.8, dict(dir="r")), link="dir", cam=("push", 0.05), label="yola çıktı, yetki sonra geldi"),
    # ── 13. Napoli'ye 18 Aralık'ta vardı ─────────────────────────────────────────────────────
    shot("p4_liman", ("c8s10", -0.1), variant="napoli", year="18 ARALIK 1479", ship=dict(mode="arrive", kind="kadirga", flag="toskana"), t_dock=("c8s10", "vardı.", 0.0), followers=0,
         mode="day", perde=2, tr=("slide", 0.8, dict(dir="r")), link="dir", cam=("push", 0.05), label="Napoli limanı (18 Aralık)"),
    # ── 14. Konuk muydu, rehine mi? (Napoli salonu; iki siluet; odak kayar) ─────────────────────
    shot("p4_oda", ("c8s11", -0.2), room="salon", variant="napoli", path="table", mode="night", perde=2,
         cam=("rack", (330, 560), (1560, 560), dict(at=("c8s11", "rehine", -0.1), dur=1.6, r=420)),
         ovl=K.date_strip(("c8s11", "şubat", -0.8), [("6 ARALIK 1479", 0, ("c8s11", "şubat", -0.8)), ("18 ARALIK", 12, ("c8s11", "şubat", -0.5)), ("27 ŞUBAT 1480", 83, ("c8s11", "şubat", 0.2))],
                          fill_to=(83, ("c8s11", "şubat", -0.2)), fill_dur=1.5),
         tr=("light", 0.9, dict(at=(960, 640))), link="light", label="Napoli salonu: konuk mu, rehine mi?"),
    # ── 15. Aynı haftalarda doğudan bir yolculuk sona eriyordu (harita doğuya kayar) ─────────────
    shot("p4_map", ("c8s12", -0.1), mode="day", perde=2, cam=("push", 0.05), approx=False,
         cams=[(("c8s12", -0.1), (21.6, 41.9, 2.6)), (("c8s12", "gelen", 0.0), (20.6, 42.2, 2.7))],
         cities=[dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c8s12", -0.1), size=32, side="b"), dict(lon=28.9784, lat=41.0082, name="İSTANBUL", kind="capital", at=("c8s12", "doğudan", -0.2), size=32, side="b")],
         routes=[dict(pts=[(28.9, 41.1), (26.0, 40.2), (23.0, 39.3), (19.5, 39.7), (15.5, 41.0), (12.4, 43.0), (11.3, 43.75)], at=("c8s12", "doğudan", -0.2), dur=3.2, color="#A8321E", width=8.0, dash=(20, 12))],
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="harita: doğudan Floransa'ya yolculuk"),
    # ── 16. Bandini kiliseden kaçıp İstanbul'a ulaşmıştı; orada akrabaları vardı (Pera rıhtımı) ──────────────
    shot("p4_liman", ("c8s13", -0.1), variant="pera", year=None, name="İSTANBUL", ship=dict(mode="arrive", kind="tekne", flag="genel", dir=1, scale=1.0), t_dock=("c8s13", "ulaşmıştı;", -0.3), crowd=10,
         cams=[(("c8s13", -0.1), (940, 4, 1.0)), (("c8s13", "akrabaları", 0.0), (1120, -6, 1.14))],
         mode="day", perde=2, tr=("slide", 0.9, dict(dir="r")), link="dir", cam=("push", 0.05), label="Pera: İstanbul'a ulaşmıştı"),
    # ── 17. 8 Mayıs 1479: temsilcinin mektubu Floransa'ya yol alır; Sultan katili tutuklatmıştı ──────────────
    shot("p4_map", ("c8s14", -0.1), mode="day", perde=2, cam=("push", 0.05), approx=False,
         cams=[(("c8s14", -0.1), (28.5, 41.2, 8.0)), (("c8s14", "yazdığına", 0.0), (28.3, 41.2, 7.0)), (("c8s14", "Sultan", -0.4), (20.8, 42.0, 2.7)), (("c8s14", "katili", -0.7), (21.0, 41.8, 2.8)), (("c8s14", "tutuklatmıştı.", -0.2), (28.8, 41.2, 7.5))],
         cities=[dict(lon=28.9784, lat=41.0082, name="PERA", kind="capital", at=("c8s14", "Pera'daki", -0.5), size=32, side="b"), dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c8s14", "Sultan", -0.5), size=32, side="b")],
         icons_=[dict(kind="scroll", route=[(28.9, 41.1), (26.3, 40.3), (23.0, 39.4), (19.5, 39.8), (15.5, 41.1), (12.4, 43.0), (11.3, 43.72)], at=("c8s14", "yazdığına", -0.2), move_at=("c8s14", "yazdığına", 0.0), move_dur=3.6, size=84, metal="gold"),
                 dict(kind="chains", lon=29.25, lat=41.42, size=92, at=("c8s14", "tutuklatmıştı.", -0.7), metal="silver")],
         routes=[dict(pts=[(28.9, 41.1), (26.3, 40.3), (23.0, 39.4), (19.5, 39.8), (15.5, 41.1), (12.4, 43.0), (11.3, 43.72)], at=("c8s14", "yazdığına", -0.2), dur=3.6, color="#A8321E", width=5.0, dash=(14, 10))],
         date=("8 MAYIS 1479", ("c8s14", 0.0)),
         ovl=L.ov(L.tag("PERA'DAKİ FLORANSALI TEMSİLCİ", 760, 170, ("c8s14", "Pera'daki", -0.1), size=32, w=760, out=("c8s14", "Sultan", 0.2)), L.tag("FATİH SULTAN MEHMED", 1280, 170, ("c8s14", "Fatih", -0.1), size=34, w=560)),
         tr=("zoomthru", 0.9, dict(at=(1500, 640), at_b=(960, 540))), link="scale", label="mektup yolda: temsilci yazdı, Sultan tutuklattı"),
    # ── 18. Floransa Antonio de' Medici'yi seçti; 14 Temmuz'da aceleyle yola çıkardı ─────────────────────────
    shot("p4_deniz_rota", ("c8s15", -0.1), tod="day", ship_kind="kadirga", flag="toskana", scale=0.92, thread=True, mode="day", perde=2,
         route=[(240, 664), (1000, 620), (2000, 580), (3000, 560), (3900, 600)],
         labels=[dict(name="FLORANSA", at_xy=(300.0, 300.0), f=0.40, t=("c8s15", -0.1), dy=-90), dict(name="İSTANBUL", at_xy=(4200.0, 300.0), f=0.40, t=("c8s15", "ortasından", 0.0), dy=-90)],
         ovl=L.ov(L.tag("ANTONIO DE' MEDICI", 960, 190, ("c8s15", "Antonio", -0.1), size=38, w=620, sub="ELÇİ", out=("c8s15", "yola", 0.4)),
                  L.date_plate("14 TEMMUZ", ("c8s15", "Temmuz'da", -0.1), x=96, y=860),
                  K.date_strip(("c8s15", "çünkü", -0.1), [("14 TEMMUZ", 0, ("c8s15", "çünkü", 0.0)), ("AĞUSTOS ORTASI", 32, ("c8s15", "Ağustos", 0.0))], x0=1060.0, x1=1760.0, y=860.0, fill_to=(32, ("c8s15", "Ağustos", 0.1)), fill_dur=2.2)),
         tr=("zoomthru", 0.9, dict(at=(960, 560), at_b=(960, 560))), link="scale", cam=("push", 0.05), label="Antonio'nun aceleyle yolculuğu"),
    # ── 19. Sultan'ın nedenini bilmiyoruz; Floransa'nın ticaret ayrıcalıkları vardı (Pera rıhtımı, yük) ────────
    shot("p4_liman", ("c8s16", -0.1), variant="pera", year=None, crowd=14, ship=dict(mode="depart", dir=-1, kind="nao", flag="toskana", t_leave=("c8s16", "ayrıcalıkları", -0.2)),
         cams=[(("c8s16", -0.1), (1240, 0, 1.12)), (("c8s16", "ticaret", 0.0), (1100, 6, 1.2)), (("c8s16", "vardı.", 0.0), (960, 0, 1.0))],
         ovl=L.ov(K.question(("c8s16", "bilmiyoruz;", -0.2), 960, 470, out=("c8s16", "Floransa'nın", 0.0)), L.tag("TİCARET AYRICALIKLARI", 960, 860, ("c8s16", "ayrıcalıkları", -0.3), size=36, w=700)),
         mode="day", perde=2, tr=("carry", 0.9, dict(strip="ribbon", dir="r")), link="carry", cam=("push", 0.05), label="Pera: neden bilmiyoruz; ticaret ayrıcalıkları"),
    # ── 20. Heyet 24 Aralık'ta vardı; beş gün sonra 29 Aralık: Bargello'nun penceresi (beden YOK) ───────────────
    shot("c8_bargello", ("c8s17", -0.1), arrive_at=("c8s17", -0.1), win_at=("c8s18", "penceresinden", -0.4), shade_at=("c8s18", "asıldı;", -0.25), cloth_at=("c8s18", "giysileri", -0.5),
         mode="day", perde=2,
         cam=[(("c8s17", -0.1), look(1280, 600, 1.0)), (("c8s17", "vardı.", -0.4), look(1130, 610, 1.05)), (("c8s18", -0.1), look(980, 540, 1.0)), (("c8s18", "Bargello'nun", -0.2), look(1130, 470, 1.15)),
              (("c8s18", "penceresinden", 0.0), look(1200, 440, 1.8)), (("c8s18", "hâlâ", -0.3), look(1200, 470, 1.6)), (("c8s18", "vardı.", 0.0), look(1330, 600, 1.1))],
         ovl=L.ov(L.date_plate("24 ARALIK", ("c8s17", "Aralık'ta", -0.3), out=("c8s18", "beş", -0.3)), K.calendar_flip(("c8s18", "beş", -0.2), 24, 29, dt=0.22, out=("c8s18", "Bargello'nun", -0.3)),
                  L.date_plate("29 ARALIK 1479", ("c8s18", "Aralık'ta,", -0.1))),
         tr=("slide", 0.9, dict(dir="r")), link="dir", longtake=True, label="Bargello: heyet (24 Aralık), 29 Aralık"),
    # ── 21. O sırada Lorenzo Napoli'deydi (aynı tarih, iki şehir: şerit üstünde 29 Aralık) ──────────────────
    shot("p4_oda", ("c8s19", -0.15), room="salon", variant="napoli", path="table", mode="night", perde=2, cam=("push", 0.07),
         ovl=K.date_strip(("c8s19", -0.1), [("18 ARALIK", 0, ("c8s19", -0.1)), ("27 ŞUBAT 1480", 71, ("c8s19", "Napoli'deydi.", -0.3))], fill_to=(71, ("c8s19", "Lorenzo", -0.4)), fill_dur=1.3,
                          extra_marks=[("29 ARALIK 1479", 11, ("c8s19", "sırada", -0.2), "#E8715A")]),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Napoli: aynı gün, iki şehir (eşzamanlılık)"),
    # ── 22. Leonardo asılı adamı çizdi; giysisini satır satır not etti (kıyafet etüdü; beden YOK) ──────────────
    shot("c8_leonardo", ("c8s20", -0.15), mode="night", perde=2, draw_at=("c8s20", "çizdi,", -0.2), notes_at=("c8s20", "satır", -0.2),
         cam=[(("c8s20", -0.15), look(900, 520, 1.12)), (("c8s20", "giysisini", 0.0), look(900, 560, 1.28)), (("c8s20", "not", 0.0), look(1090, 560, 1.4)), (("c8s20", "etti.", 0.3), look(980, 540, 1.1))],
         ovl=L.tag("LEONARDO", 360, 860, ("c8s20", -0.05), size=36, w=420, out=("c8s20", "etti.", 0.4)),
         tr=("sayfa", 0.9), link="material", label="Leonardo'nun sayfası: giysi etüdü ve notlar"),
    # ── 23. Ferrante Papa'nın safından ayrıldı; Lorenzo mart ortasında Floransa'ya barışla döndü (dönüş YUKARI) ───
    shot("p4_map", ("c8s21", -0.15), mode="day", perde=2, cam=("push", 0.05), approx=False,
         cams=[(("c8s21", -0.15), (12.9, 42.3, 4.9)), (("c8s21", "Lorenzo", -0.2), (12.9, 42.0, 4.9)), (("c8s21", "döndü.", 0.0), (12.5, 42.9, 5.4))],
         cities=[dict(lon=14.2681, lat=40.8518, name="NAPOLİ", kind="capital", at=-3.0, size=34), dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=-3.0, size=34, side="l")],
         icons_=[dict(kind="crown", lon=14.27, lat=41.28, size=84, at=-3.0, metal="gold"), dict(kind="keys", lon=12.4964, lat=41.9028, size=88, at=-3.0, metal="gold")],
         extra=L.mx(L.marrow([(14.2681, 40.9), (13.35, 41.5), (12.55, 42.25), (11.95, 42.95), (11.45, 43.45)], -3.0, dur=0.4, color="#A8321E", width=9.0, out=("c8s21", "ayrıldı;", 0.0)),
                    L.marrow(ROTA_FN[::-1], ("c8s21", "Lorenzo", 0.0), dur=2.6, color="#233C8C", width=9.0, dash=(22, 12)), L.mbadge(ROTA_FN[::-1], ("c8s21", "Lorenzo", 0.0), dur=2.6)),
         date=("MART ORTASI", ("c8s21", "mart", -0.1)),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="harita: Ferrante ayrıldı, Lorenzo yukarı döndü"),
    # ── 24. Barış parlak değildi: üç madde, mühür ──────────────────────────────────────────────────────
    shot("c8_baris", ("c8s22", -0.15), mode="day", perde=2, longtake=True,
         cam=[(("c8s22", -0.15), look(960, 540, 1.0)), (("c8s22", "savaşta", -0.4), look(900, 420, 1.35)), (("c8s22", "Alfonso'ya", -0.5), look(950, 550, 1.35)), (("c8s22", "Volterra'da", -0.5), look(980, 690, 1.35)), (("c8s22", "sayılır.", -0.2), look(960, 540, 1.0))],
         tr=("sayfa", 0.9), link="material", label="barış maddeleri ve mühür"),
    # ── 25. Yetmişler Konseyi: 70 iskemle sayılır; beş yıllık, iki kez yenilenir ─────────────────────────
    shot("c8_konsey", ("c8s23", -0.15), mode="day", perde=2, cam=("push", 0.06), ovl=L.date_plate("NİSAN 1480", ("c8s23", "Nisanda", -0.1), out=("c8s23", "Yetmişler", 0.3)), tr=("giornata", 0.9), link="material", label="Yetmişler Konseyi (70 iskemle, 1480-85-90)"),
    # ── 26. Sonra denizden bir haber geldi (ufukta Osmanlı kadırgası, sağdan sola/aşağı) ──────────────────
    shot("p4_deniz", ("c8s24", -0.1), scene="acik", tod="dusk", birds=7, mode="day", perde=2, cam=("push", 0.05),
         ships=[dict(kind="kadirga", flag="osmanli", route=[(1330, 352), (1220, 430), (1040, 560), (860, 690)], t0=0.0, t1=("c8s25", -0.1), ease="io", scale=0.95),
                dict(kind="kadirga", flag="osmanli", x0=1700, x1=1250, y=470, scale=0.7, t0=0.0, t1=("c8s25", -0.1), ease="lin")],
         cams=[(("c8s24", -0.1), (960, 6, 1.0)), (("c8s25", -0.1), (940, -10, 1.12))],
         tr=("dip", 0.8), link="light", label="denizden haber: Osmanlı donanması ufukta"),
    # ── 27. 28 Temmuz 1480: Gedik Ahmed Paşa'nın donanması Otranto'da; şehir ağustosta düştü (alev, duman; insan yok) ──
    shot("p4_deniz_kiyi", ("c8s25", -0.1), tod="fire", n=16, fire_at=("c8s25", "ağustosta", -0.9), mode="day", perde=2, cam=("push", 0.05),
         cams=[(("c8s25", -0.1), (1050, 20, 1.0)), (("c8s25", "düştü.", 0.0), (940, -8, 1.2))],
         ovl=L.ov(L.date_plate("28 TEMMUZ 1480", ("c8s25", "28", -0.15), out=("c8s25", "ağustosta", -0.3)), L.date_plate("AĞUSTOS 1480", ("c8s25", "ağustosta", -0.2)),
                  L.tag("GEDİK AHMED PAŞA", 700, 170, ("c8s25", "Gedik", -0.1), size=34, w=560, sub="DONANMA"), L.tag("OTRANTO", 1380, 170, ("c8s25", "Otranto", -0.25), size=34, w=360)),
         tr=("dip", 0.8), link="light", label="Otranto: donanma çıkar, şehir düşer"),
    # ── 28. Ferrante Alfonso'yu ve ordusunu Toskana'dan geri çağırdı (oklar ters yöne; kamera devamı) ────
    shot("p4_map", ("c8s26", -0.15), mode="day", perde=2, cam=("push", 0.05), approx=False,
         cams=[(("c8s26", -0.15), (14.6, 41.6, 4.5)), (("c8s26", "ordusunu", 0.0), (13.0, 42.3, 4.8))],
         cities=[dict(lon=14.2681, lat=40.8518, name="NAPOLİ", kind="capital", at=-3.0, size=34), dict(lon=18.4896, lat=40.1459, name="OTRANTO", kind="siege", at=-3.0, size=32, side="b")],
         labels=[dict(text="TOSKANA", lon=11.1, lat=43.35, size=44, track=18, at=-3.0, color="#5A3E1E", face="title_m")],
         icons_=[dict(kind="crown", lon=14.27, lat=41.28, size=84, at=-3.0, metal="gold"), dict(kind="b_flame", lon=18.49, lat=40.65, size=100, at=-3.0, metal="gold", bob=3.0)],
         routes=[dict(pts=[(11.45, 43.45), (11.95, 42.95), (12.55, 42.25), (13.35, 41.5), (14.2681, 40.95)], at=("c8s26", "çağırdı.", -1.9), dur=2.2, color="#A8321E", width=9.0)],
         tr=("light", 0.9, dict(at=(1480, 520))), link="light", label="harita: ordu Toskana'dan geri çağrılır"),
    # ── 29. Papa'nın öfkesi geri plana düştü; Aralık 1480'de elçiler affedildi (bulla düşer, mum mühür basılır) ──
    shot("c8_aforoz", ("c8s27", -0.15), phase="af", mode="night", perde=2, drop_at=("c8s27", "plana", -0.35), seal_at=("c8s27", "affedildi.", -0.45),
         cam=[(("c8s27", -0.15), look(960, 560, 1.0)), (("c8s27", "geri", -0.4), look(960, 620, 1.15)), (("c8s27", "Aralık", -0.2), look(1200, 480, 1.25)), (("c8s27", "affedildi.", 0.3), look(1100, 470, 1.35))],
         ovl=L.ov(K.icon_pop("b_flame", 1640, 230, ("c8s27", "Osmanlı", -0.1), out=("c8s27", "geri", 0.2), size=170, glow=0.45), L.date_plate("ARALIK 1480", ("c8s27", "Aralık", -0.2)), L.tag("FLORANSA'NIN ELÇİLERİ", 1500, 860, ("c8s27", "elçileri", -0.2), size=32, w=620)),
         tr=("light", 0.9, dict(at=(960, 700))), link="light", label="bulla düşer, affedildiler (Aralık 1480)"),
    # ── 30. Bertoldo atölyesi: Fatih Sultan Mehmed'in profili bronza dökülür ───────────────────────────
    shot("c8_dokum", ("c8s28", -0.15), mode="night", perde=2, pour_at=("c8s28", "heykeltıraşı", 0.0), open_at=("c8s28", "profilini", -0.5), cam=("push", 0.06),
         ovl=L.ov(L.tag("BERTOLDO DI GIOVANNI", 960, 170, ("c8s28", "Bertoldo", -0.1), size=36, w=640, sub="LORENZO'NUN HEYKELTIRAŞI", out=("c8s28", "profilini", -0.3)),
                  L.tag("FATİH SULTAN MEHMED", 960, 170, ("c8s28", "profilini", -0.3), size=36, w=640)),
         tr=("carry", 0.9, dict(strip="ribbon", dir="r")), link="carry", label="döküm: bronz akar, kalıp açılır"),
    # ── 31. Madalya (ön yüz): sipariş 'olabilir'; kesin belge yok ────────────────────────────────────────
    shot("p4_medal", ("c8s29", -0.15), key="m_mehmed", metal="bronze", name="FATİH SULTAN MEHMED", role="stilize profil", cam=("orbit", 10), mode="night", perde=2,
         ovl=L.ov(K.icon_pop("question", 1500, 330, ("c8s29", "olabilir;", -0.5), out=("c8s29", "kesin", 0.0), size=200), L.stamp("KESİN BELGE YOK", 1420, 700, ("c8s29", "belge", -0.25), size=46, rot=-0.07)),
         tr=("zoomthru", 0.9, dict(at=(960, 470), at_b=(960, 470), depth=3.0)), link="scale", label="madalya: ısmarlanmış olabilir"),
    # ── 32. Ters yüz: zafer arabası, alevli sandalye amblemi ─────────────────────────────────────────────
    shot("c8_madalya", ("c8s30", -0.2), flip_at=("c8s30", "Arka", -0.1), mode="night", perde=2, cam=("push", 0.06),
         ovl=L.ov(L.tag("ZAFER ARABASI", 1460, 280, ("c8s30", "zafer", -0.1), size=36, w=500, out=("c8s30", "alevli", 0.0)), L.tag("ALEVLİ SANDALYE · NAPOLİ KRALLARI", 1330, 280, ("c8s30", "alevli", -0.1), size=30)),
         tr=("zoomthru", 0.8, dict(at=(960, 470), at_b=(960, 470), depth=2.5)), link="scale", label="madalyanın ters yüzü"),
    # ── 33. Napoli'ye olası saldırıya imâ; tuhaf hediye (fiyong) · Mehmed 3 Mayıs 1481'de öldü ───────────────
    shot("c8_madalya", ("c8s31", -0.15), show="rev", castle_at=("c8s31", "Napoli'ye", -0.35), bow_at=("c8s31", "tuhaf", -0.4), flip_back_at=("c8s32", "öldü;", -0.35), dim_at=("c8s32", "öldü;", -0.2),
         mode="night", perde=2, longtake=True, cam=[(("c8s31", -0.15), look(960, 540, 1.0)), (("c8s31", "tuhaf", 0.0), look(900, 520, 1.12)), (("c8s32", -0.1), look(960, 540, 1.0))],
         ovl=L.ov(L.stamp("YORUM", 1560, 280, ("c8s31", "tuhaf", 0.3), size=46, rot=-0.07, out=("c8s32", "Mehmed", 0.0)), L.date_plate("3 MAYIS 1481", ("c8s32", "3", -0.15))),
         tr=("slide", 0.9, dict(dir="l")), link="dir", label="olası saldırıya imâ; tuhaf hediye; ölüm"),
    # ── 34. Otranto aynı yılın eylülünde Napoli'ye döndü (bayrak değişir) ───────────────────────────────────
    shot("p4_map", ("c8s32", "Otranto", -0.4), mode="day", perde=2, cam=("push", 0.05), approx=False,
         cams=[(("c8s32", "Otranto", -0.4), (17.0, 40.4, 8.0)), (("c8s32", "döndü.", 0.0), (16.8, 40.5, 8.8))],
         cities=[dict(lon=18.4896, lat=40.1459, name="OTRANTO", kind="siege", at=-3.0, size=34, side="b"), dict(lon=14.2681, lat=40.8518, name="NAPOLİ", kind="capital", at=-3.0, size=34)],
         extra=L.mx(L.mflag(18.4896, 40.1459, -3.0, color="#B33620", emblem="crescent", h=95.0, out=("c8s32", "Napoli'ye", -0.5)), L.mflag(18.4896, 40.1459, ("c8s32", "Napoli'ye", -0.3), color="#233C8C", emblem="plain", h=95.0),
                    L.marrow([(14.2681, 40.9), (15.8, 40.6), (17.2, 40.3), (18.3, 40.17)], ("c8s32", "eylülünde", -0.4), dur=1.8, color="#233C8C", width=8.0)),
         date=("EYLÜL 1481", ("c8s32", "eylülünde", -0.4)),
         tr=("dip", 0.8), link="light", label="Otranto Napoli'ye döner (Eylül 1481)"),
    # ── 35. Lorenzo bir savaşı barışa çevirmişti (kılıçlar defne olur) ──────────────────────────────────────
    shot("p4_palle", ("c8s33", -0.1), size=520, mode="day", perde=2, cam=("pull", 0.07), ovl=K.swords_to_laurel(("c8s33", "barışa", -0.5)),
         tr=("carry", 0.9, dict(strip="banner", dir="r")), link="carry", label="savaş barışa çevrildi (Medici arması, defne)"),
    # ── 36. KAPI: bankanın şubelerinde ışıklar birer birer sönüyordu (c9'a) ───────────────────────────────
    shot("p4_map", ("c8s34", -0.15), mode="day", perde=2, style="lapis", cam=("push", 0.05), approx=False, frame=True, compass=(1760, 860, 58),
         cams=[(("c8s34", -0.15), (5.5, 47.7, 2.25)), (("c8s34", "sönüyordu.", 0.0), (5.5, 47.6, 2.45))],
         cities=[dict(lon=-0.1276, lat=51.5074, name="LONDRA", kind="town", at=("c8s34", "Londra'dan", -0.6), size=30, side="r", color="#FFD27A"), dict(lon=9.19, lat=45.4642, name="MİLANO", kind="town", at=("c8s34", "Milano'ya,", -0.6), size=30, side="b", color="#FFD27A")],
         extra=L.mx(*[L.mglow(lo, la, ("c8s34", "Ama", 0.0 + 0.1 * i), out=an, r=30.0) for i, (lo, la, an) in enumerate([
             (-0.1276, 51.5074, ("c8s34", "Londra'dan", 0.1)), (9.19, 45.4642, ("c8s34", "Milano'ya,", 0.1)), (3.2247, 51.2093, ("c8s34", "ışıklar", 0.0)), (4.8055, 43.9493, ("c8s34", "birer", 0.0)),
             (4.8357, 45.764, ("c8s34", "birer", 0.45)), (12.3155, 45.4408, ("c8s34", "sönüyordu.", -0.1))])]),
         ovl=L.dim(("c8s34", "birer", 0.55), alpha=0.72, dur=2.2),
         tr=("candle", 1.0, dict(at=(960, 540), at_b=(1500, 600))), link="light", label="KAPI: şube ışıkları birer birer söner"),
]
YIL_AT = [(("c8s1", 0), 1478), (("c8s5", "1479", -0.1), 1479), (("c8s21", "mart", -0.2), 1480), (("c8s32", "1481'de", -0.1), 1481)]
