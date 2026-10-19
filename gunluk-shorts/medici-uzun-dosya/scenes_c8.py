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
                  L.tag("PAPA IV. SIXTUS", 1400, 150, ("c8s1", "IV.", 0.0), size=38, w=520, out=("c8s1", "aforoz", 0.6)),
                  L.stamp("AFOROZ", 1330, 640, ("c8s1", "etti;", -0.1), size=66, rot=-0.10, out=("c8s1", "yasak,", 0.2))),
         tr=("carry", 0.9, dict(strip="paper", dir="l")), link="carry", label="aforoz belgesi, kurşun mühür"),
    # ── 3. Interdikt: mühür şehri örter (yasak) ─────────────────────────────────────────────
    shot("p4_skyline", ("c8s1", "Floransa'ya", -0.1), seed=5, tod="dusk", mode="night", perde=2, dir=-1, cam=("pan", "l", 300),
         tr=("iris", 0.9, dict(obj="seal", at=K.BULLA_REST, r=K.BULLA_R + 6)), link="shape", label="interdikt: şehir sessizleşir"),
    # ── 4. Latince satır: kötülüğün oğlu ve yıkımın evladı ─────────────────────────────────
    shot("c8_aforoz", ("c8s2", -0.2), phase="satir", mode="night", perde=2, imp_at=None, line_at=("c8s2", "alışılmış", -0.3), tr_at=("c8s2", "kötülüğün", -0.1),
         cam=[(("c8s2", -0.2), look(960, 420, 1.35)), (("c8s2", "üslupla,", 0.0), look(900, 430, 1.75)), (("c8s2", "evladı”", 0.0), look(960, 500, 1.55))],
         ovl=L.ov(L.stamp("○ TEK KAYNAK", 1500, 250, ("c8s2", "Aktarıldığına", 0.2), size=44, rot=-0.08)),
         tr=("zoomthru", 0.9, dict(at=(960, 560), at_b=(960, 420))), link="scale", label="Latince satır ve çeviri"),
    shot("black", ("c8s3", 0), text="[devam]", label="yer tutucu"),
]
YIL_AT = [(("c8s1", 0), 1478)]
