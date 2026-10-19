"""c15 — Son Medici'ler (1587–1737). AĞIR/YORGUN: kamera yavaş, ışık/toz/alev canlı; çekimler daha seyrek; geçişler candle/dip/yikama ağırlıklı.
Yönetmen kartı: yonetmen_c15.md · notlar: notlar_c15.md. Tüm çekimler cümle/sözcük çapalı.
Renk anahtarı: gece mum sarısı + lacivert (ölümler), gündüz soluk sıva (tartışma/şifre), yaldız yalnız taç/sikke; DNA katmanı mavi.
İmza sekans: «Soy ağacı solar» → mum mantığı: altı hükümdar mumu (s14'te yanık, s19'da tek tek söner), geriye tek ışık: bir kadın ve mühürlü sözleşme (kapı → c16).
Mizah (hafif, kaynağın kendi kuru dili): studiolo tarifi (yarı ofis… yarım daireler), iki haber başlığı, ruspanti (379 + sikke), yönetmeyen varis (1 KEZ).
KAPALI: Francesco/Bianca'nın ölümü (iki mum), Gian Gastone'nin yatağı/hastalığı/ölümü (HİÇ gösterilmez; boş taht odası), soyun bitişi. «Zehir çürütüldü» YOK: «BÜYÜK OLASILIKLA SITMA».
"""
from shots import shot
import cilt_medici as CM
import p7_lib as L
import c14_kinds as K14
import c15_kinds as K
look = L.look
ov = L.ov

HALF = [("OFİS", 172, ("c15s1", "ofis,", -0.1)), ("LABORATUVAR", 446, ("c15s1", "laboratuvar,", -0.1)), ("SAKLANMA YERİ", 874, ("c15s1", "saklanma", -0.1)), ("MERAK KABİNİ", 1346, ("c15s1", "merak", -0.1))]
LIV = (10.31, 43.55)
SID = (35.4, 33.8)
IST = (28.98, 41.01)
VIE = (16.3738, 48.2082)
FLO = (11.2558, 43.7696)

SHOTS = [
    # ── 1. Palazzo Vecchio kulesi (dikey plan) ───────────────────────────────────────────────────
    shot("p7_sehir", ("c15s1", 0), scene="skyline_dikey", tod="day", mode="day", cam=("crane", "up", 130),
         ovl=ov(L.tag("I. FRANCESCO", 600, 170, ("c15s1", "Francesco", -0.1), size=36, w=460, out=("c15s1", "yaptırmıştı:", 0.0)),
                L.tag("PALAZZO VECCHIO", 1320, 170, ("c15s1", "Palazzo", -0.1), size=36, w=560, out=("c15s1", "yaptırmıştı:", 0.0))),
         label="Palazzo Vecchio kulesi (dikey plan)"),
    # ── 2. Studiolo: yarı ofis, yarı laboratuvar, yarı saklanma yeri, yarı merak kabini ───────────
    shot("p7_oda", ("c15s1", "kendine", 0.35), room="calisma", variant="studiolo", mode="night", figure="desk",
         zone_at=[("c15s1", "ofis,", -0.4), ("c15s1", "laboratuvar,", -0.4), ("c15s1", "saklanma", -0.4), ("c15s1", "merak", -0.4)], secret_at=("c15s1", "saklanma", 0.0),
         cams=[(("c15s1", "kendine", 0.35), (1050, 20, 1.0)), (("c15s1", "ofis,", -0.4), (1000, 40, 1.4)), (("c15s1", "laboratuvar,", -0.4), (1730, 40, 1.4)),
               (("c15s1", "saklanma", -0.4), (2250, 40, 1.4)), (("c15s1", "merak", -0.4), (2740, 40, 1.4)), (("c15s1", "kendisi", -0.1), (1900, 0, 0.95))],
         cam=("pan", "r", 160),
         ovl=ov(*[K.half_label(t_, x_, 170, a_, out=("c15s2", 0.0)) for (t_, x_, a_) in HALF]),
         tr=("zoomthru", 0.9, dict(at=(960, 260), at_b=(1050, 540))), link="scale", label="studiolo: dört bölge, tek siluet"),
    # ── 3. Bir gün arayla: iki mum ───────────────────────────────────────────────────────────────
    shot("c15_iki_mum", ("c15s2", -0.2), mode="night", a1=("c15s2", "Francesco,", -0.2), a2=("c15s2", "Bianca", -0.2), out1=("c15s2", "arayla", -0.1), out2=("c15s2", "arayla", 1.2), cam=("push", 0.07),
         ovl=ov(L.date_plate("EKİM 1587", ("c15s2", "Ekim", -0.1))),
         tr=("candle", 1.0, dict(at=(1000, 480), at_b=(700, 520))), link="light", label="iki mum: bir gün arayla"),
    # ── 4. Söylenti: pencereden pencereye (zehir hikâyesi: rivayet) ─────────────────────────────
    shot("p7_skyline", ("c15s3", -0.2), mode="night", seed=6, tod="dusk", pan=260, cam=("pan", "r", 200),
         ovl=ov(K.whispers(("c15s3", "dolaştığı", -0.5), [(300, 560), (640, 480), (1000, 540), (1360, 470), (1660, 540)], out=("c15s3", "turta", -0.3)),
                L.stamp("SÖYLENİR", 1500, 250, ("c15s3", "söylenir;", -0.1), size=52, rot=-0.07, out=("c15s3", "turta", 0.0)),
                K.pie_ov(960, 380, ("c15s3", "turta", -0.1)),
                L.stamp("ANEKDOT", 1260, 330, ("c15s3", "anlatılmıştır,", -0.2), size=52, rot=-0.06),
                K.whispers(("c15s3", "ilk", -0.1), [(930, 380), (700, 270), (460, 300), (240, 300)], col="#C9B27A", dur=2.2),
                L.icon("question", 190, 300, 120, ("c15s3", "gösteremiyoruz.", -0.5), glow=0.3, bob=4)),
         tr=("dip", 0.9), link="light", label="söylenti ipleri; turta anekdot; ilk anlatıcı yok"),
    # ── 5. Dört yüzyıllık ölçek: 1587 → 2006 · 2010 · 2026 ───────────────────────────────────────
    shot("c15_cetvel", ("c15s4", -0.1), mode="night", a0=("c15s4", -0.1), a_br=("c15s4", 0.2), a06=("c15s4", "2006'da", -0.15), a10=("c15s4", "2010'da", -0.1), a26=("c15s5", "2026'da", -0.1),
         cam=[(("c15s4", -0.1), look(720, 560, 1.0)), (("c15s4", "2006'da", -0.1), look(1000, 560, 1.12)), (("c15s5", "2026'da", -0.2), look(1230, 560, 1.28))],
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="1587 ····· dört yüzyıl ····· 2006 · 2010 · 2026"),
    # ── 6. 2026: üç numune, iki parazit DNA'sı ───────────────────────────────────────────────────
    shot("c15_dna", ("c15s5", "Francesco'nun", -0.2), mode="night", vials_at=("c15s5", "Francesco'nun", 0.0), three_at=("c15s5", "üç", -0.1), helix_at=("c15s5", "örneklerde", 0.0), two_at=("c15s5", "iki", -0.1),
         cam=("push", 0.07), tr=("zoomthru", 0.9, dict(at=(1726, 560), at_b=(1060, 540))), link="scale", label="DNA: üç numune, iki parazit"),
    # ── 7. İki haber başlığı, iki ayrı kesinlik ───────────────────────────────────────────────────
    shot("c15_baslik", ("c15s6", -0.15), mode="day", a1=("c15s6", "kitabı", -0.3), a2=("c15s6", "çözülmüş", -0.3), join_at=("c15s6", "aynı", 0.0), cam=("push", 0.07),
         tr=("sayfa", 0.9), link="material", label="“kitabı kapattı” ↔ “çözülmüş olabilir”"),
    # ── 8. Terazi: zehir hikâyesinin ağırlığı bugün sıtmanın tarafında ───────────────────────────
    shot("c15_terazi", ("c15s7", -0.1), mode="day", a_in=("c15s7", -0.1), a_dna=("c15s7", "enfeksiyonu", -0.2), a_cause=("c15s7", "nedenini", -0.2), a_tilt=("c15s7", "ağırlığı", -0.5),
         final_at=("c15s7", "bugün", 0.0), cam=("push", 0.07),
         ovl=ov(L.tag("BÜYÜK OLASILIKLA SITMA", 960, 150, ("c15s7", "sıtmanın", -0.2), size=42, w=860)),
         tr=("yikama", 0.9), link="material", label="terazi: sıtmaya yatar (zehir çürütüldü DEĞİL)"),
    # ── 9. Ferdinando: 13 yaşında kardinal, rahip olmadı, büyük dük ───────────────────────────────
    shot("c15_ferdinando", ("c15s8", -0.1), mode="day", hat_at=("c15s8", "Ferdinando,", -0.2), n_at=("c15s8", "13", -0.2), monk_at=("c15s8", "hiçbir", -0.3), x_at=("c15s8", "olmadı;", -0.4),
         crown_at=("c15s8", "büyük", -0.35), cam=("push", 0.07), ovl=ov(L.date_plate("19 EKİM 1587", ("c15s8", "19", -0.1))),
         tr=("carry", 0.9, dict(strip="ink", dir="r")), link="carry", label="kırmızı şapka ↔ taç"),
    # ── 10. Livorno'nun ticareti büyüdü ───────────────────────────────────────────────────────────
    shot("p7_liman", ("c15s9", -0.1), mode="day", variant="livorno", year=None, stamp=False, followers=4, crowd=10, t_dock=("c15s9", "büyüdü;", -0.6), cam=("push", 0.07),
         ovl=ov(L.date_plate("1593", ("c15s9", "1593'te", -0.15), out=("c15s9", "Livornina,", 0.0))),
         tr=("light", 0.9, dict(at=(960, 520))), link="light", label="Livorno limanı: ticaret büyür"),
    # ── 11. Livornina: üç vaat ────────────────────────────────────────────────────────────────────
    shot("c15_livornina", ("c15s9", "ilan", -0.4), mode="day", unroll_at=("c15s9", "ilan", -0.3), seal_at=("c15s9", "Livornina,", 0.0), d_at=("c15s9", "dinî", -0.2), af_at=("c15s9", "af", -0.2), v_at=("c15s9", "Toskana", -0.1),
         cam=("push", 0.07), tr=("sayfa", 0.9), link="material", label="1593 ilanı: dinî özgürlük · af · vatandaşlık"),
    # ── 12. Mustafa Ağa 1598 ──────────────────────────────────────────────────────────────────────
    shot("p7_liman", ("c15s10", -0.15), mode="day", variant="livorno", year=1598, delegation=dict(side="osmanli", n=5, t0=("c15s10", "elçisi", -0.2)), cam=("push", 0.07),
         ovl=ov(L.tag("SULTAN III. MEHMED'İN MEKTUPLARI", 960, 150, ("c15s10", "mektuplarını", -0.15), size=34, w=900, out=("c15s10", "Mustafa", 0.0)),
                L.tag("MUSTAFA AĞA", 1480, 330, ("c15s10", "Mustafa", -0.1), size=36, sub="OSMANLI ELÇİSİ", w=460),
                L.stamp("BAŞARISIZLIKLA BİTTİ", 1400, 820, ("c15s10", "başarısızlıkla", -0.2), size=44, rot=-0.06)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Mustafa Ağa'nın gelişi (saygılı)"),
    # ── 13. Fahreddin: 1608 antlaşması, sığınma güvencesi (yazılır) ───────────────────────────────
    shot("p7_map", ("c15s11", -0.1), mode="day", approx=False, cam=("push", 0.07),
         cams=[(("c15s11", -0.1), (33.5, 35.5, 4.2)), (("c15s11", "İstanbul", -0.5), (26.0, 39.0, 3.2)), (("c15s11", "Toskana'da", -0.4), (14.0, 41.2, 3.0))],
         cities=[dict(lon=SID[0], lat=SID[1], name="FAHREDDİN", kind="town", at=("c15s11", "Fahreddin'le", -0.5), size=36, side="l"),
                 dict(lon=IST[0], lat=IST[1], name="İSTANBUL", kind="capital", at=("c15s11", "İstanbul", -0.3), size=40, side="r"),
                 dict(lon=LIV[0], lat=LIV[1], name="LİVORNO", kind="capital", at=("c15s11", "Toskana'da", -0.4), size=38, side="r")],
         routes=[dict(pts=[IST, (31.5, 38.0), SID], at=("c15s11", "sıkıştırırsa", -0.2), dur=1.2, color="#A8321E", width=8.0),
                 dict(pts=[SID, (30.0, 34.5), (24.0, 35.4), (18.0, 37.5), (14.0, 40.3), (11.5, 42.6), LIV], at=("c15s11", "Toskana'da", -0.3), dur=2.4, color="#233C8C", width=8.0, dash=(18, 12))],
         icons_=[dict(kind="shield", lon=LIV[0] + 0.3, lat=LIV[1] + 0.5, size=100, at=("c15s11", "güvencesi", -0.3), metal="gold")],
         ovl=ov(L.date_plate("1608", ("c15s11", "1608'de", -0.1)), L.stamp("YAZILIR", 1500, 860, ("c15s11", "yazılır.", -0.3), size=44, rot=-0.06)),
         tr=("yikama", 0.9), link="material", label="1608: İstanbul sıkıştırırsa → Toskana (yazılır)"),
    # ── 14. 1613: Fahreddin gerçekten geldi ───────────────────────────────────────────────────────
    shot("p7_liman", ("c15s12", -0.1), mode="day", variant="livorno", year=1613, followers=2, cam=("push", 0.07),
         ovl=ov(L.tag("FAHREDDİN", 560, 150, ("c15s12", "Fahreddin", -0.1), size=38, w=440), L.tag("II. COSIMO DÖNEMİ", 1400, 150, ("c15s12", "II.", -0.2), size=34, w=560)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="1613: Livorno'ya yaklaşan gemiler"),
    # ── 15. Cosimo III: elli üç yıl; yün geriledi, ipek gelişti ──────────────────────────────────
    shot("c15_sektor", ("c15s13", -0.1), mode="day", years_at=("c15s13", "elli", -0.2), decl_at=("c15s13", "gerileme", -0.4), yun_at=("c15s13", "yün", -0.4), ipek_at=("c15s13", "ipek", -0.4), cam=("push", 0.07),
         ovl=ov(L.stamp("YAZILIR", 1500, 860, ("c15s13", "yazılır.", -0.3), size=44, rot=-0.06)),
         tr=("sayfa", 0.9), link="material", label="53 yıl: gerileme tek hat değil (yün ↓ ipek ↑)"),
    # ── 16. Hükümdar mumları: Gian Gastone 1723 ──────────────────────────────────────────────────
    shot("c15_hat", ("c15s14", -0.1), mode="night", lit_at=("c15s14", 0.0), out_at=999.0, woman_at=999.0, doc_at=999.0, cam=("pan", "r", 150),
         ovl=ov(L.tag("BÜYÜK DÜK GIAN GASTONE", 1380, 500, ("c15s14", "Gian", -0.1), size=34, w=660, out=("c15s14", "çevresindeki", 0.3))),
         tr=("light", 0.9, dict(at=(1000, 600))), link="light", label="hükümdar mumları (1723)"),
    # ── 17. 379 ruspanti ──────────────────────────────────────────────────────────────────────────
    shot("c15_ruspanti", ("c15s14", "çevresindeki", -0.4), mode="day", count_at=("c15s14", "379", -0.2), count_dur=1.6, coin_at=("c15s14", "altın", -0.3), cam=("push", 0.07),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="379 ruspanti: adını paradan alan çevre"),
    # ── 18. Treccani 1932 / 2010 ──────────────────────────────────────────────────────────────────
    shot("p7_doc", ("c15s15", -0.15), mode="day", title="TRECCANI · 1932", w=1200, h=700, size=54,
         lines=[("devlet işlerine kayıtsız;", ("c15s15", "kayıtsız", -0.3)), ("saltanatı: bir onarım", ("c15s15", "onarım", -0.3))],
         caption="çeviri bize ait", cam=("push", 0.07), tr=("sayfa", 0.9), link="material", label="Treccani 1932"),
    shot("p7_doc", ("c15s16", -0.15), mode="day", title="TRECCANI · 2010", w=1200, h=700, size=50,
         lines=[("tek reformu:", ("c15s16", "reformunun", -0.2)), ("üniversiteyi Aristotelesçilikten kurtarmak", ("c15s16", "üniversiteyi", -0.2))],
         caption="çeviri bize ait", cam=("push", 0.07), tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="Treccani 2010 (ayrışan hüküm)"),
    # ── 19. 9 Temmuz 1737: boş taht odası, yabancı birlikler (yatak/hastalık GÖSTERİLMEZ) ───────────
    shot("p7_oda", ("c15s17", -0.1), room="salon", variant="taht", path="taht_in", mode="night", tod="dusk",
         actors=[dict(kind="asker", x=2430, y=872, h=300, sil=True, prop="halberd", walk=(2080, 140), walk_at=("c15s17", "birlikleri", -0.9), seed=3),
                 dict(kind="asker", x=2560, y=884, h=300, sil=True, prop="halberd", walk=(2210, 140), walk_at=("c15s17", "birlikleri", -0.7), seed=5),
                 dict(kind="asker", x=980, y=872, h=300, sil=True, prop="halberd", walk=(1330, 140), walk_at=("c15s17", "birlikleri", -0.9), seed=7, dir=1),
                 dict(kind="asker", x=850, y=884, h=300, sil=True, prop="halberd", walk=(1200, 140), walk_at=("c15s17", "birlikleri", -0.7), seed=9, dir=1)],
         cam=("push", 0.07),
         ovl=ov(L.date_plate("9 TEMMUZ 1737", ("c15s17", "9", -0.1), out=("c15s17", "çünkü", 0.0)),
                L.tag("«non era già più sovrano del suo stato»", 960, 200, ("c15s17", "hükümdarı", -0.3), size=34, w=1160, sub="artık kendi devletinin hükümdarı değildi (çeviri bize ait)"),
                L.tag("LORRAINE DÜKÜ FRANCIS STEPHEN", 700, 860, ("c15s17", "Lorraine", -0.1), size=32, w=700)),
         tr=("candle", 1.0, dict(at=(960, 500), at_b=(1000, 560))), link="light", label="boş taht odası; yabancı birlikler girer"),
    # ── 20. Viyana'da karar; Floransa'ya yalnızca bir kez ─────────────────────────────────────────
    shot("p7_map", ("c15s18", -0.1), mode="day", approx=False, cam=("push", 0.07),
         cams=[(("c15s18", -0.1), (14.2, 45.8, 3.2)), (("c15s18", "Floransa'ya", -0.3), (13.8, 46.0, 3.3))],
         cities=[dict(lon=VIE[0], lat=VIE[1], name="VİYANA", kind="capital", at=("c15s18", "Viyana'da", -0.2), size=42, side="r"),
                 dict(lon=FLO[0], lat=FLO[1], name="FLORANSA", kind="capital", at=("c15s18", "Floransa'ya", -0.5), size=38, side="l")],
         routes=[dict(pts=[VIE, (14.4, 46.2), (12.8, 45.0), FLO], at=("c15s18", "kararlaştırılmıştı;", -0.1), dur=1.2, color="#7A5C32", width=5.0, dash=(10, 10), arrow=False),
                 dict(pts=[VIE, (14.4, 46.2), (12.8, 45.0), FLO], at=("c15s18", "Floransa'ya", 0.0), dur=2.8, color="#A8321E", width=9.0)],
         icons_=[dict(kind="scroll", lon=VIE[0] + 0.25, lat=VIE[1] + 0.45, size=96, at=("c15s18", "kararlaştırılmıştı;", -0.3), metal="gold"),
                 dict(kind="horse", route=[VIE, (14.4, 46.2), (12.8, 45.0), FLO], at=("c15s18", "Floransa'ya", 0.0), move_at=("c15s18", "Floransa'ya", 0.0), move_dur=2.8, size=84, metal="gold")],
         ovl=ov(L.tag("1 KEZ — 1739", 960, 150, ("c15s18", "yalnızca", 0.0), size=52, w=600)),
         tr=("yikama", 0.9), link="material", label="Viyana → Floransa: bir kez, 1739"),
    # ── 21. Erkek hat kapandı; geriye bir kadın ve imzalanacak sözleşme ────────────────────────────
    shot("c15_hat", ("c15s19", -0.1), mode="night", lit_at=("c15s19", -0.1), out_at=("c15s19", "kapanmıştı;", -0.5), out_dt=0.26, woman_at=("c15s19", "kadın", -0.3), doc_at=("c15s19", "sözleşme", -0.3),
         cam=("pan", "r", 140), tr=("candle", 1.0, dict(at=(1000, 520), at_b=(300, 700))), link="light", label="mumlar söner; tek ışık: kadın + sözleşme (kapı → c16)"),
]
YIL_AT = [(("c15s1", 0), 1587), (("c15s4", "2006'da", 0.0), 2006), (("c15s5", "2026'da", 0.0), 2026), (("c15s8", "19", 0.0), 1587), (("c15s9", "1593'te", 0.0), 1593), (("c15s10", 0), 1598),
          (("c15s11", "1608'de", 0.0), 1608), (("c15s12", "1613'te,", 0.0), 1613), (("c15s14", "1723'te", 0.0), 1723), (("c15s17", "9", 0.0), 1737), (("c15s18", "1739", 0.0), 1739)]
