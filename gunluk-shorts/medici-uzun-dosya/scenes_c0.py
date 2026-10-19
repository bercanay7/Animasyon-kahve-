"""c0 — Hiçbir Şey Buradan Çıkmayacak (1737–1743). KANCA, 101 sn, gerçek ses. Yönetmen kartı: yonetmen_c0.md.

Işık/zaman: kaynakta saat/hava YOK → oda `tod="dusk"` (alacakaranlık + mum havuzu; pencere nötr soluk cam, AY/YILDIZ YOK, "gece" iddiası yok).
İmza sekans: "Aile Antlaşması, tek plan" — skyline → oda (zoomthru) → belge (zoomthru) → 3. madde → galeri (zoomthru) → harita/sınır → bugünün kuyruğu → geri sarma.
Tüm çekimler cümle/sözcük çapalı (mutlak saniye yok).
"""
import functools

from shots import shot
import cilt_medici as CM
import p1_ortak as P
import c0_kinds as K

DOC = K.DOC_FILL          # oda1743: belge ekranı doldurur (cams anahtarı)

ODA_DUSK = dict(tod="dusk", mode="night", perde=1)

SHOTS = [
    # ── 1. Floransa, alacakaranlık (ölçek: şehir) ──────────────────────────
    shot("skyline", ("c0s1", 0), seed=2, tod="dusk", mode="night", perde=1, pan=300, kick="18 ŞUBAT 1743 · FLORANSA", at=-0.4,
         cam=("pan", "r", 300), label="Floransa, alacakaranlık"),
    # ── 2. 1743 odası: yatak (silüet), isim levhası; kamera sağa kayar → duvardaki Medici arması ──
    shot("p1_oda", ("c0s2", -0.1), room="oda1743", figure="lying", **ODA_DUSK,
         cams=[(("c0s2", -0.1), (1000, 30, 1.12)), (("c0s2", "Luisa", 0.0), (985, 30, 1.2)), (("c0s3", 0.0), (1150, 20, 1.15)), (("c0s4", -0.3), (1740, 30, 1.25))],
         ovl=P.plate("ANNA MARIA LUISA", 1400, 790, ("c0s2", "Anna", -0.1), out=("c0s3", "Medici", 0.9)),
         tr=("zoomthru", 0.9, dict(at=(1000, 560))), link="scale", label="1743 odası: yatak, arma"),
    # ── 3. Boş taht, yabancı birlik siluetleri girer ───────────────────────
    shot("p1_oda", ("c0s4", -0.1), room="salon", variant="taht", path="taht_in", **ODA_DUSK,
         actors=[dict(kind="asker", x=2430, y=872, h=300, sil=True, prop="halberd", walk=(2080, 140), walk_at=("c0s4", "yabancı", -0.7), seed=3),
                 dict(kind="asker", x=2560, y=884, h=300, sil=True, prop="halberd", walk=(2210, 140), walk_at=("c0s4", "yabancı", -0.5), seed=5),
                 dict(kind="asker", x=980, y=872, h=300, sil=True, prop="halberd", walk=(1330, 140), walk_at=("c0s4", "yabancı", -0.7), seed=7, dir=1),
                 dict(kind="asker", x=850, y=884, h=300, sil=True, prop="halberd", walk=(1200, 140), walk_at=("c0s4", "yabancı", -0.5), seed=9, dir=1)],
         ovl=P.tablet_text("5 YIL 7 AY ÖNCE", 560, 860, ("c0s4", "beş", -0.1), size=38, out=("c0s4", "ölmüştü", 0.9)),
         tr=("iris", 0.9, dict(obj="palle", at=(1410, 290), r=95)), link="shape", label="boş taht, yabancı birlik"),
    # ── 4. Medici salonu: palle frizi; tek siluet "hâlâ o duruyordu" ──────
    shot("oda", ("c0s5", -0.1), room="salon", variant="medici", **ODA_DUSK,
         cams=[(("c0s5", -0.1), (1100, 0, 1.0)), (("c0s5", "yüzyıllarca", 0.0), (1450, 20, 1.1)), (("c0s5", "hâlâ", 0.0), (1760, 50, 1.45))],
         actors=[dict(kind="soylu_f", x=1900, y=858, h=300, action="idle", sil=True, layer="front", seed=4)],
         cam=("push", 0.06), tr=("slide", 0.9, dict(dir="r")), link="dir", label="Medici salonu, tek siluet"),
    # ── 5. 31 Ekim 1737: imza masası (mum, zaman sıçraması) ────────────────
    shot("oda", ("c0s6", -0.15), room="oda1743", figure="seated", **ODA_DUSK, kick="31 EKİM 1737",
         cams=[(("c0s6", -0.15), (1700, 40, 1.3)), (("c0s6", "Gian", 0.0), (1760, 50, 1.45))],
         cam=("push", 0.06), tr=("candle", 1.0, dict(at=(960, 640), at_b=(1500, 540))), link="light", label="imza masası 1737"),
    # ── 6. 114 GÜN: takvim yaprakları ──────────────────────────────────────
    shot("c0_takvim", ("c0s6", "ölümünden", -0.4), mode="night", perde=1, cam=("push", 0.06),
         start_at=("c0s6", "ölümünden", -0.3), end_at=("c0s6", "dört", 0.2),
         tr=("sayfa", 0.9), link="material", label="114 GÜN takvim"),
    # ── 7. İmza: kalem + mühür; kamera belgeye iner ───────────────────────
    shot("oda", ("c0s6", "sözleşme", -0.5), room="oda1743", figure="seated", seal_at=("c0s6", "imzalandı", -0.1), **ODA_DUSK,
         cams=[(("c0s6", "sözleşme", -0.5), (1820, 50, 1.5)), (("c0s6", "imzalandı", 0.0), (1900, 80, 2.4)), (("c0s7", -0.1), DOC)],
         cam=("push", 0.06), tr=("zoomthru", 0.9, dict(at=(630, 560))), link="scale", label="imza, mühür, belgeye iniş"),
    # ── 8. Belge: iki yan, 13 madde, FRANSIZCA, ITALIANO çizilir (tek kesintisiz belge planı) ──
    shot("c0_belge", ("c0s7", -0.1), mode="night", perde=1,
         cams=[(("c0s7", -0.1), (0, 0, 0.97)), (("c0s7", "Luisa", 0.0), (-300, 150, 1.5)), (("c0s7", "Lorraine", 0.2), (300, 150, 1.5)),
               (("c0s8", -0.1), (0, 0, 1.0)), (("c0s8", "on", 0.0), (-420, 20, 1.8)), (("c0s8", "ve", 0.0), (-150, -40, 1.25)), (("c0s8", "Fransızca", 0.2), (80, -90, 1.2)),
               (("c0s9", 0.0), (0, -140, 1.45)), (("c0s9", "bile", 0.0), (0, -120, 1.7)), (("c0s10", -0.4), (0, 0, 1.0))],
         seals=(("c0s7", "Anna", 0.0), ("c0s7", "Lorraine", 0.3)),
         names_at=("ANNA MARIA LUISA", "LORRAINE TARAFI", ("c0s7", "Luisa", 0.15), ("c0s7", "tarafı", -0.3)),
         pen_at=("c0s7", "Bir", 0.0),
         num_at=("c0s8", "on", 0.0), num_dur=1.2, fr_at=("c0s8", "Fransızca", 0.0),
         it_at=("c0s9", "diliyle", 0.0), it_strike_at=("c0s9", "yazılmamıştı", -0.2),
         tr=("zoomthru", 0.9, dict(at=(960, 520), at_b=(960, 520))), link="scale", label="belge: iki mühür, 13 madde, FRANSIZCA"),
    # ── 9. Masa başı siluet: odak (bilmiyoruz → biliyoruz) ─────────────────
    shot("p1_oda", ("c0s10", -0.1), room="oda1743", figure="seated", **ODA_DUSK,
         cams=[(("c0s10", -0.1), DOC), (("c0s10", "düşündüğünü", 0.0), (1850, 70, 1.6)), (("c0s11", 0.0), (1880, 60, 1.75))],
         ovl=P.ov(K.soru_ovl(("c0s10", "bilmiyoruz", -0.2), x=905, y=480, size=230, out=("c0s10", "ama", -0.1)),
                  P.glint(1180, 690, ("c0s10", "biliyoruz", -0.6), r=190, dur=1.4)),
         cam=("pull", 0.08), tr=("carry", 0.95, dict(strip="paper", dir="r")), link="carry", label="masa başı: bilmiyoruz → biliyoruz"),
    # ── 10. III. madde vurgulanır ──────────────────────────────────────────
    shot("c0_belge", ("c0s11", -0.1), mode="night", perde=1,
         cams=[(("c0s11", -0.1), (0, 0, 1.0)), (("c0s11", "üçüncü", 0.0), (0, -60, 1.7)), (("c0s12", "İtalyanca", 0.3), (0, -160, 2.5))],
         seals=(("c0s7", 0.0), ("c0s7", 0.0)), num_at=("c0s8", "on", 0.0), num_dur=0.01, fr_at=("c0s8", 0.0), hl_at=("c0s11", "üçüncü", -0.2), scrim_at=("c0s11", "üçüncü", -0.2),
         tr=("zoomthru", 0.9, dict(at=(960, 560), at_b=(960, 520))), link="scale", label="III. madde"),
    # ── 11. Galeri: zoomthru ile açılan Vasari koridoru; beş kalem sıralanır ──
    shot("p1_pano", ("c0s12", -0.1), pano="corridor", tod="day", mode="day", perde=1, stations=[],
         cams=[(("c0s12", -0.1), (2300, 0, 1.08)), (("c0s12", "kütüphaneler", 0.0), (3300, 10, 1.12)), (("c0s12", "Floransa", -0.3), (4300, 0, 1.2))],
         ovl=P.ov(K.hazine_ovl([("c0_galeri", "GALERİLER", ("c0s12", "galeriler", -0.15)), ("c0_tablo", "TABLOLAR", ("c0s12", "tablolar", -0.15)), ("c0_heykel", "HEYKELLER", ("c0s12", "heykeller", -0.15)),
                                ("book_open", "KÜTÜPHANELER", ("c0s12", "kütüphaneler", -0.15)), ("c0_mucevher", "MÜCEVHERLER", ("c0s12", "mücevherler", -0.15)),
                                ("chest", "ÖTEKİ\nKIYMETLİ ŞEYLER", ("c0s12", "öteki", -0.1))], gap=310, size=100),
                  P.stamp("ÇEVİRİ", 1480, 250, ("c0s12", "İtalyanca", 0.3), rot=-0.08, size=50)),
         tr=("zoomthru", 0.9, dict(at=(960, 230), at_b=(960, 520))), link="scale", label="galeri: Vasari koridoru, 5 kalem"),
    # ── 12. Harita: Büyük Dukalık sınırı, zincir, 3. maddenin özeti ────────
    shot("c0_harita", ("c0s12", "Floransa", -0.4), mode="day", perde=1, approx=False,
         cams=[(("c0s12", "Floransa", -0.4), (11.1, 43.4, 5.0)), (("c0s12", "çıkarılamayacaktı", 0.6), (11.12, 43.4, 6.3))],
         regions=[dict(name="c0_toskana", color="ochre", at=("c0s12", "Büyük", -0.2), alpha=0.6, dur=1.2)],
         cities=[dict(lon=11.25, lat=43.77, name="FLORANSA", kind="capital", at=("c0s12", "Floransa", -0.2), size=34)],
         cam=("push", 0.06),
         extra=functools.partial(K.sinir_extra, label_at=("c0s12", "Dukalık", -0.2), items_at=("c0s12", "Floransa", 0.0), lock_at=("c0s12", "çıkarılamayacaktı", -0.1),
                                 quote_at=("c0s12", "çıkarılamayacaktı", 0.55), quote_out=("c0s13", "devletin", -0.6)),
         tr=("slide", 0.9, dict(dir="u")), link="dir", label="harita: Büyük Dukalık, zincir"),
    # ── 13. Gerekçe: üç kalem ──────────────────────────────────────────────
    shot("c0_gerekce", ("c0s13", -0.1), mode="day", perde=1, cam=("push", 0.08),
         draw_at=("c0s13", "Gerekçesi", -0.1), stamp=("c0s13", "aktarılır", -0.1),
         items=[dict(icon="crown", label="DEVLETİN SÜSÜ", at=("c0s13", "devletin", -0.1)), dict(icon="scales", label="HALKIN YARARI", at=("c0s13", "halkın", -0.1)),
                dict(icon="globe", label="YABANCILARIN MERAKI", at=("c0s13", "yabancıların", -0.1))],
         tr=("light", 0.9, dict(at=(1470, 780))), link="light", label="gerekçe: süs, yarar, merak"),
    # ── 14–15. Bugünün kuyruğu: "Yabancıların merakı." (sert kesme) ────────
    shot("c0_kuyruk", ("c0s14", 0), mode="day", perde=1, cam=("push", 0.07),
         sign_at=("c0s15", "Uffizi", 0.0), kick_at=("c0s15", "Bugün", -0.1), coin_at=("c0s15", "müşterisi", 0.0),
         link="audio", label="Uffizi kuyruğu (bugün)"),
    # ── 16. Bankacı ailesi: geriye kayma, soru işareti ─────────────────────
    shot("p1_oda", ("c0s16", -0.1), room="banka", path="corner", **ODA_DUSK,
         ovl=P.ov(K.soru_ovl(("c0s16", "geldi", -0.15), out=("c0s17", 0.0))),
         tr=("slide", 0.9, dict(dir="l")), link="dir", label="banka köşesi: nasıl geldi?"),
    # ── 17–18. Kılıçlar değil, altın sikke; geri sarma: 1252 ───────────────
    shot("c0_sikke", ("c0s17", -0.05), mode="night", perde=1, cam=("push", 0.07),
         sw_at=("c0s17", "kılıçlarda", -0.1), no_at=("c0s17", "değil", -0.1), coin_at=("c0s17", "altın", -0.2),
         cd_a=("c0s18", "Saati", 0.1), cd_b=("c0s18", "1252", 0.15),
         tr=("yikama", 0.9), link="material", label="kılıç değil sikke; 1252"),
]
YIL_AT = [(("c0s6", "1737", -0.2), 1737), (("c0s18", "geri", -0.1), 1252)]
