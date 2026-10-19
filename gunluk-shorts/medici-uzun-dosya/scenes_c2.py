"""c2 — Defterin Sihri (1397–1429). Parça 1, 3/3 · PARÇA KAPANIŞI. 244 sn, gerçek ses. Yönetmen kartı: yonetmen_c2.md.

İmza sekans: "Defter dünyadır" — banka → kambiyo haritası (Brugge → Barselona, iki poliçe) → BORÇ ✗ FAİZ ✗ KUR FARKI ✓ → vicdan komitesi damgası → hediye paketi → Cossa mezarı (altın yaprak yazıt).
Mizah (c2): faiz yasağı ↔ kambiyo ↔ vicdan komitesi; "faiz değil hediye"; "eski papa"; çifte kayıt miti. KAPALI: Giovanni'nin ölümü, Cossa'nın esareti.
Kapı: "...bir hücreye kapatılacaktı." → Palazzo Vecchio kulesinde yavaş crane up, sessiz ve ağır (Parça 1 kanca kapanışı; bitiş ekranı Program'dan).
Kaynak sınıfı damgaları: ANEKDOT (rivayet/ölüm yatağı), MİT (çifte kayıt), "KLASİK BİR ÖRNEK" (model), "BİR HESABA GÖRE" (○).
"""
import functools

from shots import shot
import cilt_medici as CM
import p1_ortak as P
import c0_kinds as K0
import c1_kinds as K1
import c2_kinds as K

BANKA = dict(room="banka", tod="day", mode="day", perde=1)

SHOTS = [
    # ── 1a. Çözüm kambiyodaydı; Kilise her türlü faizi tefecilik sayıp yasaklamıştı (c1'in banka köşesinden devam) ──
    shot("p1_oda", ("c2s1", -0.1), **BANKA, cam=("push", 0.06),
         cams=[(("c2s1", -0.1), (900, 40, 1.15)), (("c2s2", "Kilise", 0.0), (1300, 30, 1.2)), (("c2s2", "tefecilik", 0.0), (1700, 20, 1.28))],
         ovl=P.ov(P.pop_label("KAMBİYO", 960, 215, ("c2s1", "kambiyodaydı", -0.25), size=118, track=16),
                  P.glint(960, 205, ("c2s1", "kambiyodaydı", 0.1), r=190),
                  P.tablet_icon("cross", "KİLİSE: FAİZ = TEFECİLİK", 640, 420, ("c2s2", "Kilise", -0.1), w=760, size=34),
                  P.stamp("YASAK", 1520, 400, ("c2s2", "yasaklamıştı", -0.25), rot=-0.08, size=84)),
         link="scale", label="banka: kambiyo; Kilise faizi yasakladı"),
    # ── 1b. bankacılar da bir yol buldular ───────────────────────────────────
    shot("p1_oda", ("c2s2", "bankacılar", -0.2), **BANKA, path="count", cam=("push", 0.08),
         ovl=P.ov(P.icon_at("compass", 960, 400, ("c2s2", "yol", -0.2), size=300, glow=True, bob=8),
                  P.label("BİR YOL", 960, 640, ("c2s2", "buldular", -0.4), size=64, face="title", track=18),
                  P.coin_arc((520, 760), (1400, 760), ("c2s2", "buldular", -0.3), n=5, lift=140)),
         tr=("light", 0.9, dict(at=(960, 400))), link="light", label="bankacılar bir yol buldu"),
    # ── 2. Klasik örnek: Brugge → Barselona poliçe ───────────────────────────
    shot("p1_map", ("c2s3", -0.1), mode="day", perde=1, approx=False,
         cams=[(("c2s3", -0.1), (2.8, 46.4, 1.8)), (("c2s3", "Barselona'ya", 0.0), (2.8, 46.3, 1.9)), (("c2s3", "karşılığında", 0.0), (2.8, 46.3, 2.0))],
         cities=[dict(lon=3.22, lat=51.21, name="BRUGGE", kind="capital", at=("c2s3", "Brugge'de", -0.2), size=34),
                 dict(lon=2.17, lat=41.39, name="BARSELONA", kind="capital", at=("c2s3", "Barselona'ya", -0.25), size=34)],
         routes=[dict(pts=[(3.22, 51.21), (0.9, 46.3), (2.17, 41.39)], at=("c2s3", "Barselona'ya", -0.25), dur=1.6, width=7, color="#A8321E")],
         icons_=[dict(kind="coinbag", lon=3.22, lat=51.21, size=96, at=("c2s3", "parayı", -0.1), bob=4),
                 dict(kind="scroll", lon=3.22, lat=51.21, size=84, at=("c2s3", "Barselona'ya", -0.2), route=[(3.22, 51.21), (0.9, 46.3), (2.17, 41.39)], move_at=("c2s3", "Barselona'ya", -0.1), move_dur=1.4, glow=0.0)],
         ovl=P.ov(P.stamp("KLASİK BİR ÖRNEK", 1500, 190, ("c2s3", "Klasik", -0.1), rot=-0.06, size=46),
                  P.tablet_icon("coins", "PARAYI PEŞİN VERİRSİN", 560, 255, ("c2s3", "peşin", -0.2), w=700, size=32)),
         cam=("push", 0.06), tr=("zoomthru", 0.9, dict(at=(960, 560), at_b=(960, 520))), link="scale", label="kambiyo: Brugge → Barselona"),
    # ── 2b. karşılığında Barselona'ya çekilmiş bir poliçe alırsın (belge yakın plan) ──
    shot("p1_doc", ("c2s3", "karşılığında", -0.2), title="POLİÇE", lines=[("Brugge'de verilen", ("c2s3", "çekilmiş", 0.0)), ("Barselona'da ödenir", ("c2s3", "poliçe", 0.0))], seal=True, seal_at=("c2s3", "alırsın", -0.2),
         w=980, h=640, mode="day", perde=1, cam=("push", 0.08),
         ovl=P.ov(P.stamp("KLASİK BİR ÖRNEK", 1500, 250, ("c2s3", "Klasik", 0.0), rot=-0.06, size=42, out=("c2s3", "karşılığında", -0.3)),
                  P.coin_arc((330, 700), (1100, 520), ("c2s3", "alırsın", -0.5), n=4, lift=120)),
         tr=("sayfa", 0.9), link="material", label="poliçe: Barselona'ya çekilmiş"),
    # ── 3. vadesi gelince: poliçe tahsil, ikinci poliçeyle para geri döner; kazanç kur farkı ──
    shot("p1_map", ("c2s4", -0.1), mode="day", perde=1, approx=False,
         cams=[(("c2s4", -0.1), (2.8, 46.3, 2.0)), (("c2s4", "kazanç", -0.3), (2.8, 46.4, 1.75))],
         cities=[dict(lon=3.22, lat=51.21, name="BRUGGE", kind="capital", at=-0.5, size=34), dict(lon=2.17, lat=41.39, name="BARSELONA", kind="capital", at=-0.5, size=34)],
         routes=[dict(pts=[(3.22, 51.21), (0.9, 46.3), (2.17, 41.39)], at=-0.3, dur=0.2, width=6, color="#A8321E"),
                 dict(pts=[(2.17, 41.39), (5.1, 46.0), (3.22, 51.21)], at=("c2s4", "ikinci", -0.3), dur=1.8, width=7, color="#233C8C", label="2. POLİÇE")],
         icons_=[dict(kind="coins", lon=2.17, lat=41.39, size=100, at=("c2s4", "tahsil", -0.3), bob=4),
                 dict(kind="scroll", lon=2.17, lat=41.39, size=84, at=("c2s4", "ikinci", -0.2), route=[(2.17, 41.39), (5.1, 46.0), (3.22, 51.21)], move_at=("c2s4", "poliçeyle", -0.3), move_dur=1.6, glow=0.0),
                 dict(kind="coinbag", lon=3.22, lat=51.21, size=100, at=("c2s4", "geri", -0.1), bob=4)],
         ovl=P.ov(P.tablet_icon("scroll", "VADESİ GELİNCE TAHSİL", 560, 255, ("c2s4", "Vadesi", -0.1), w=700, size=32, out=("c2s4", "kazanç", -0.3)),
                  P.pop_label("KUR FARKI", 1500, 255, ("c2s4", "kur", -0.1), size=84, track=10)),
         cam=("pull", 0.07), tr=("slide", 0.9, dict(dir="r")), link="dir", label="tahsil, ikinci poliçe, kazanç = kur farkı"),
    # ── 4. Ortada borç yok, faiz yok; yalnızca kur farkı var ─────────────────
    shot("c2_nolist", ("c2s5", -0.1), mode="day", perde=1, borc_at=("c2s5", "borç", -0.25), borc_x=("c2s5", "yok", -0.15), faiz_at=("c2s5", "faiz", -0.25), faiz_x=("c2s5", "yok", 1, -0.15), kur_at=("c2s5", "yalnızca", -0.2),
         cam=("push", 0.07), tr=("carry", 0.9, dict(strip="ink", dir="r")), link="carry", label="BORÇ ✗ FAİZ ✗ KUR FARKI ✓"),
    # ── 5. vicdan komitesi (mizah vuruşu) ────────────────────────────────────
    shot("p1_oda", ("c2s6", -0.1), room="salon", variant="medici", sil=True, tod="day", mode="day", perde=1, path="table",
         ovl=P.ov(P.stamp("VİCDAN KOMİTESİ", 960, 300, ("c2s6", "vicdan", -0.15), rot=-0.05, size=92),
                  P.icon_at("scales", 1560, 400, ("c2s6", "departmanı", -0.1), size=190, glow=True, bob=6),
                  P.label("EN YARATICI DEPARTMAN", 1560, 520, ("c2s6", "yaratıcı", -0.2), size=32, face="title_m", track=8)),
         cam=("push", 0.07), tr=("slide", 0.9, dict(dir="r")), link="dir", label="vicdan komitesi"),
    # ── 6. mevduat: faiz sözleşmeye yazılmaz (Parks) ─────────────────────────
    shot("p1_doc", ("c2s7", -0.1), title="MEVDUAT SÖZLEŞMESİ", lines=[("Mevduat: kabul edildi", ("c2s7", "mevduata", 0.0)), ("Faiz: —", ("c2s7", "faiz", 0.0))], seal=True, seal_at=("c2s7", "yazılmaz", 0.0),
         w=980, h=700, pan=(190, 30), mode="day", perde=1, cam=("push", 0.07),
         ovl=P.ov(P.plate("TRACY PARKS", 320, 330, ("c2s7", "Parks'ın", -0.2), role="AKTARDIĞINA GÖRE", w=520),
                  P.crossout(965, 512, 54, ("c2s7", "yazılmaz", -0.15), sw=12)),
         tr=("sayfa", 0.9), link="material", label="mevduat sözleşmesi: faiz yazılmaz"),
    # ── 7. banker lütuf olarak öder; faiz değil, hediye ───────────────────────
    shot("c2_hediye", ("c2s7", "banker", -0.2), mode="day", perde=1, tag_at=("c2s7", "kendi", -0.1), open_at=("c2s7", "lütuf", -0.4), strike_at=("c2s8", "değil", -0.15), gift_at=("c2s8", "hediye", -0.1),
         cam=("push", 0.08), tr=("zoomthru", 0.9, dict(at=(960, 560), at_b=(960, 520))), link="scale", label="faiz değil, hediye"),
    # ── 8. Üstelik müşterilerinden biri Kilise'nin ta kendisi ─────────────────
    shot("p1_oda", ("c2s9", -0.1), **BANKA, path="corner",
         actors=[dict(kind="tuccar", x=1010 + 380, y=830, h=262, action="talk", dir=-1, seed=40, layer="back"),
                 dict(kind="kardinal", x=2300, y=820, h=290, walk=(1500, 120), walk_at=("c2s9", "müşterilerinden", -0.6), seed=9, layer="front")],
         ovl=P.ov(P.tablet_icon("cross", "MÜŞTERİ: KİLİSE", 640, 270, ("c2s9", "Kilise'nin", -0.3), w=640, size=34),
                  P.glint(1010, 600, ("c2s9", "kendisiydi", -0.1), r=180)),
         cam=("push", 0.07), tr=("slide", 0.9, dict(dir="r")), link="dir", label="müşteri: Kilise'nin ta kendisi"),
    # ── 9. Roma şubesi: ayrı sermaye yok, kasayı Kilise doldurdu ─────────────
    shot("c2_kasa", ("c2s10", -0.1), mode="day", perde=1, branch_at=("c2s10", "Roma", -0.2), nocap_at=("c2s10", "ayrı", -0.2), church_at=("c2s10", "Kilise'nin", -0.3), fill_at=("c2s10", "kasayı", -0.1), fill_to=("c2s10", "doldurdu", 0.3),
         ovl=P.stamp("DE ROOVER'A GÖRE", 1520, 860, ("c2s10", "Roover'a", -0.1), rot=-0.06, size=42),
         cam=("push", 0.08), tr=("zoomthru", 0.9, dict(at=(1100, 560), at_b=(960, 520))), link="scale", label="Roma şubesi: kasayı Kilise doldurdu"),
    # ── 10. 25 Mart 1402: Venedik şubesi; Floransa'da o gün yılbaşı ──────────
    shot("p1_map", ("c2s11", -0.1), mode="day", perde=1, approx=False,
         cams=[(("c2s11", -0.1), (11.9, 44.7, 3.6)), (("c2s11", "Venedik", 0.0), (12.0, 44.9, 4.6)), (("c2s11", "yılbaşıydı", 0.0), (11.8, 44.6, 4.0))],
         cities=[dict(lon=11.25, lat=43.77, name="FLORANSA", kind="capital", at=("c2s11", -0.0), size=34), dict(lon=12.34, lat=45.44, name="VENEDİK", kind="capital", at=("c2s11", "Venedik", -0.25), size=36)],
         routes=[dict(pts=[(11.25, 43.77), (11.9, 44.7), (12.34, 45.44)], at=("c2s11", "Venedik", -0.3), dur=1.4, width=7)],
         ovl=P.ov(P.tablet_text("25 MART 1402", 470, 240, ("c2s11", "Mart", -0.3), size=52, face="title_m", pad=54),
                  P.stamp("YILBAŞI", 1480, 400, ("c2s11", "yılbaşıydı", -0.2), rot=-0.07, size=70),
                  P.icon_at("hourglass", 440, 480, ("c2s11", "Floransa'da", -0.1), size=170, glow=True, bob=5)),
         cam=("push", 0.07), tr=("yikama", 0.9), link="material", label="25 Mart 1402: Venedik şubesi; yılbaşı"),
    # ── 11. çifte kaydı Medici icat etti derler (MİT) ────────────────────────
    shot("p1_ledger", ("c2s12", -0.1), head="DEFTER", title_l="DEBITORI", title_r="CREDITORI",
         left=[dict(text="Giriş", at=("c2s12", "Çifte", -0.1), amt=("12",)), dict(text="Çıkış", at=("c2s12", "Medici'ler", -0.2), amt=("7",))],
         right=[dict(text="Çıkış", at=("c2s12", "Çifte", 0.1), amt=("12",)), dict(text="Giriş", at=("c2s12", "Medici'ler", 0.0), amt=("7",))],
         mode="day", perde=1, seed=5, focus=(500, 380),
         ovl=P.ov(P.icon_at("shield", 960, 175, ("c2s12", "Medici'ler", -0.15), size=150, glow=True),
                  P.stamp("MİT", 1500, 300, ("c2s12", "icat", -0.1), rot=-0.1, size=110)),
         cam=("push", 0.07), tr=("sayfa", 0.9), link="material", label="çifte kayıt: Medici icadı mı? MİT"),
    # ── 12. Etmediler: Cenova 1340 … ─────────────────────────────────────────
    shot("p1_timeline", ("c2s13", -0.1), a0=1320, a1=1520, step=20, mode="day", perde=1, title="ÇİFTE KAYDIN İZİ",
         events=[(1340, "CENOVA", ("c2s13", "Cenova'nın", -0.1)), (1407, "VENEDİK", ("c2s13", "tam", 0.0)), (1494, "PACIOLI", ("c2s13", "biridir", -0.2))],
         hl=None, cam=("push", 0.06),
         ovl=P.ov(P.stamp("ETMEDİLER", 960, 800, ("c2s13", "Etmediler", 0.0), rot=-0.04, size=84, out=("c2s13", "tarihli", 0.0)),
                  P.icon_at("shield", 1660, 440, ("c2s13", "eski", -0.3), size=150, bob=5, glow=False),
                  P.crossout(1660, 440, 76, ("c2s13", "eski", 0.0), sw=12)),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="çifte kayıt: Cenova 1340 → …"),
    # ── 13. Medici'nin farkı yapıdaydı: her şubenin kendi ortaklığı, defteri ─
    shot("p1_network", ("c2s14", -0.1), mode="day", perde=1, title="MEDİCİ'NİN FARKI: YAPI", legend=False, size=170,
         nodes=[dict(id="f", name="FLORANSA", icon="coinbag", x=0.50, y=0.42, at=("c2s14", "yapıdaydı", -0.2), size=190),
                dict(id="r", name="ROMA", icon="book", x=0.20, y=0.58, at=("c2s14", "şubenin", -0.1), size=160),
                dict(id="v", name="VENEDİK", icon="book", x=0.80, y=0.58, at=("c2s14", "kendi", -0.1), size=160)],
         edges=[("f", "r", "ortaklik", ("c2s14", "ortaklığı", -0.2)), ("f", "v", "ortaklik", ("c2s14", "ortaklığı", 0.1))],
         ovl=P.ov(P.label("KENDİ ORTAKLIĞI", 480, 880, ("c2s14", "ortaklığı", -0.1), size=34, face="title_m", track=8),
                  P.label("KENDİ DEFTERİ", 1440, 880, ("c2s14", "defteri", -0.15), size=34, face="title_m", track=8)),
         cam=("push", 0.07), tr=("light", 0.9, dict(at=(960, 480))), link="light", label="her şubenin kendi ortaklığı ve defteri"),
    # ── 14. Giovanni Cossa'ya borç verdi; papa oldu; Konstanz'da indirildi ───
    shot("c2_borc", ("c2s15", -0.1), mode="day", perde=1, longtake=True,
         names_at=(("c2s15", "Giovanni", -0.3), ("c2s15", "Baldassarre", -0.3), 1),
         give_at=("c2s15", "borç", -0.25), pope_at=("c2s15", "papa", -0.35), fall_at=("c2s16", "indirdi", -0.45), council_at=("c2s16", "1415'te", -0.2),
         cam=("push", 0.06), tr=("zoomthru", 0.9, dict(at=(960, 560), at_b=(960, 520))), link="scale", label="Giovanni → Cossa: borç, papalık, Konstanz"),
    # ── 15. kefalet mi fidye mi: kaynaklar ayrışıyor ─────────────────────────
    shot("c2_ayrim", ("c2s17", -0.1), mode="day", perde=1, walk_at=("c2s17", "İndirilen", -0.1), fork_at=("c2s17", "Giovanni'nin", -0.3), left_at=("c2s17", "kefaletle", -0.25), right_at=("c2s17", "fidyeyle", -0.25), stamp_at=("c2s17", "ayrışıyor", -0.3),
         cam=("push", 0.07), tr=("slide", 0.9, dict(dir="r")), link="dir", label="kefalet mi fidye mi: yol ayrımı"),
    # ── 16. Vaftizhane mezarı: "eski papa"; Martinus itiraz; yazıt kaldı ─────
    shot("c2_mezar", ("c2s18", -0.1), mode="day", perde=1, longtake=True, place_at=("c2s18", "Vaftizhane'ye", -0.3), carve_at=("c2s18", "eski", -0.5), carve_to=("c2s18", "papa", 0.35), protest_at=("c2s19", "itiraz", -0.25), stay_at=("c2s19", "Yazıt", -0.1),
         cam=("push", 0.07), tr=("light", 0.9, dict(at=(960, 760))), link="light", label="Cossa'nın mezarı: ESKİ PAPA"),
    # ── 17. rivayet: mitra, borç karşılığı, aforoz tehdidi ───────────────────
    shot("c2_rivayet", ("c2s20", -0.1), mode="day", perde=1, longtake=True, src_at=("c2s20", "Treccani'nin", -0.2), med_at=("c2s20", "Giovanni", -0.3), pawn_at=("c2s20", "mitrayı", -0.45), ask_at=("c2s20", "Martinus", -0.2), threat_at=("c2s20", "aforozla", -0.7),
         cam=("push", 0.06), tr=("sayfa", 0.9), link="material", label="rivayet: mitra, aforoz tehdidi (ANEKDOT)"),
    # ── 18a. papalığın resmî kasa memurluğu (anahtarlar) ──────────────────────
    shot("p1_emblem", ("c2s21", -0.1), icon="keys", metal="gold", size=480, pos=(960, 540), mode="day", perde=1, cam=("push", 0.08),
         ovl=P.ov(P.label("PAPALIĞIN RESMÎ KASA MEMURLUĞU", 960, 205, ("c2s21", "kasa", -0.4), size=46, face="title_m", track=8),
                  P.label("1420'LERİN BAŞINDAN İTİBAREN", 960, 860, ("c2s21", "1420'lerin", -0.2), size=44, face="title_m", track=10),
                  P.glint(960, 540, ("c2s21", "memurluğu", -0.2), r=240)),
         tr=("light", 0.9, dict(at=(960, 540))), link="light", label="papalığın resmî kasa memurluğu"),
    # ── 18b. kesintilerle, yirmi iki yıl kadar Medici'de ─────────────────────
    shot("p1_counter", ("c2s21", "kesintilerle", -0.3), value=22, unit="yıl", at=0.3, dur=1.2, size=330, mode="day", perde=1, cam=("push", 0.08),
         ovl=P.ov(P.label("KESİNTİLERLE", 960, 215, ("c2s21", "kesintilerle", -0.2), size=56, face="title_m", track=12),
                  P.icon_at("keys", 330, 560, ("c2s21", "yirmi", -0.3), size=200, glow=True, bob=6),
                  P.icon_at("shield", 1590, 560, ("c2s21", "Medici'de", -0.3), size=200, glow=True, bob=6)),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="22 yıl Medici'de"),
    # ── 19. catasto: 1427, hane hane ──────────────────────────────────────────
    shot("c2_katasto", ("c2s22", -0.1), mode="day", perde=1, write_at=("c2s22", "tek", -0.3), write_to=("c2s22", "denir", 0.25), title_at=("c2s22", "catasto", -0.7),
         cam=("push", 0.07), tr=("sayfa", 0.9), link="material", label="catasto: hanelerin servetini tek tek"),
    # ── 20a. 137 hane servetin ~%30'unu tutuyordu ────────────────────────────
    shot("p1_stacked", ("c2s23", -0.1), parts=[("137 HANE", 29.8, "gold", ("c2s23", "yüz", -0.1)), ("GERİ KALAN HANELER", 70.2, "umber", ("c2s23", "kayıtlı", -0.1))], total=100, unit="%", title="KAYITLI SERVET", total_label="%29,8",
         mode="day", perde=1, dur=1.4, cam=("push", 0.07),
         ovl=P.ov(P.stamp("BİR HESABA GÖRE", 1500, 250, ("c2s23", "hesaba", -0.1), rot=-0.06, size=44),
                  P.icon_at("chest", 960, 800, ("c2s23", "tutuyordu", -0.3), size=170, glow=True, bob=5)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="137 hane ≈ %30"),
    # ── 20b. en zengini Palla Strozzi ────────────────────────────────────────
    shot("p1_emblem", ("c2s23", "en", -0.15), icon="chest", metal="gold", size=420, pos=(1100, 560), mode="day", perde=1, cam=("push", 0.08),
         ovl=P.ov(P.plate("PALLA STROZZI", 520, 300, ("c2s23", "Palla", -0.5), role="EN ZENGİNİ", w=700),
                  P.count_up(520, 640, ("c2s23", "zengini", -0.05), 162925, dur=0.8, unit="FLORİN · BRÜT", size=150, bg=True, min_w=500, unit_size=34)),
         tr=("zoomthru", 0.9, dict(at=(1100, 560), at_b=(960, 520))), link="scale", label="en zengini Palla Strozzi"),
    # ── 21. Giovanni sayımın yürürlüğe girmesini destekledi ───────────────────
    shot("p1_medal", ("c2s24", -0.1), key="m_giovanni", metal="bronze", pos="l", size=620, at=0.0, mode="day", perde=1, cam=("push", 0.07),
         ovl=P.ov(P.plate("GIOVANNI", 1380, 380, ("c2s24", "Giovanni", -0.1), role="CATASTO'YU DESTEKLEDİ", w=720),
                  P.icon_at("ballot", 1380, 650, ("c2s24", "destekledi", -0.35), size=200, glow=True, bob=5),
                  P.stamp("DESTEKLEDİ", 1380, 840, ("c2s24", "destekledi", -0.05), rot=-0.06, size=60)),
         tr=("iris", 0.9, dict(obj="seal", at=(500, 500), r=300)), link="shape", label="Giovanni catasto'yu destekledi"),
    # ── 22a. 1420: yönetimi oğullarına bırakmıştı ─────────────────────────────
    shot("p1_tree", ("c2s25", -0.1), title="1420", mode="day", perde=1, cam=("push", 0.07),
         nodes=[dict(id="g", key="m_giovanni", name="GIOVANNI", x=0.5, y=0.30, at=("c2s25", "Giovanni", -0.2), size=210, nsize=34),
                dict(id="a", icon="family", name="OĞULLARI", x=0.5, y=0.72, at=("c2s25", "oğullarına", -0.3), size=190, nsize=34)],
         edges=[("g", "a", ("c2s25", "bırakmıştı", -0.3))],
         ovl=P.label("1420 · BANKANIN YÖNETİMİ", 960, 190, ("c2s25", "1420'de", -0.1), size=48, face="title", track=10),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="1420: yönetim oğullarına"),
    # ── 22b. 1397'den o yıla kadar defterler 152.820 florin kâr gösterir ──────
    shot("p1_ledger", ("c2s25", "1397'den", -0.3), head="1397 – 1420", title_l="DEBITORI", title_r="CREDITORI",
         left=[dict(text="Banka defterleri", at=("c2s25", "defterler", -0.3), hl=("c2s25", "kâr", -0.2))], right=[dict(text="Kâr", at=("c2s25", "florin", -0.4))],
         total=dict(text="1397–1420 KÂR", amt=("152.820 fl.",), at=("c2s25", "yüz", -0.1), row=7),
         mode="day", perde=1, seed=7, focus=(780, 560),
         ovl=P.ov(P.count_up(960, 215, ("c2s25", "yüz", -0.2), 152820, dur=1.5, unit="FLORİN KÂR", size=150, bg=True),
                  P.stamp("DEFTERLER GÖSTERİR", 1500, 880, ("c2s25", "gösterir", -0.2), rot=-0.05, size=38)),
         cam=("push", 0.07), tr=("sayfa", 0.9), link="material", label="defterler: 152.820 florin kâr"),
    # ── 23. 20 Şubat 1429 — Floransa takvimine göre hâlâ 1428 ────────────────
    shot("c2_yil", ("c2s26", -0.1), mode="night", perde=1, date_at=("c2s26", "20", -0.3), snuff_at=("c2s26", "öldü", -0.2), roll_at=("c2s26", "hâlâ", -0.2), cal_at=("c2s26", "Floransa", -0.1),
         cam=("push", 0.06), tr=("candle", 1.0, dict(at=(420, 640), at_b=(960, 560))), link="light", label="20 Şubat 1429; takvimde hâlâ 1428"),
    # ── 24. büyük torunu Lorenzo'nun kaydına göre 180 bin florin ──────────────
    shot("p1_medal", ("c2s27", -0.1), key="m_lorenzo", metal="bronze", pos="l", size=620, at=0.0, mode="day", perde=1, cam=("push", 0.07),
         ovl=P.ov(P.plate("LORENZO", 1380, 330, ("c2s27", "torunu", -0.3), role="İLERİDE MUHTEŞEM DİYE ANILACAK", w=800),
                  P.count_up(1380, 640, ("c2s27", "servet", 0.15), 180000, dur=1.2, unit="FLORİN", size=170, bg=True),
                  P.stamp("LORENZO'NUN KAYDINA GÖRE", 1400, 880, ("c2s27", "kaydına", -0.1), rot=-0.04, size=36)),
         tr=("zoomthru", 0.9, dict(at=(500, 500), at_b=(960, 520))), link="scale", label="Lorenzo'nun kaydına göre 180 bin florin"),
    # ── 25. son sözleri iki kalemden, iki ayrı biçimde okuyoruz ───────────────
    shot("c2_kalemler", ("c2s28", -0.1), mode="day", perde=1, left_at=("c2s28", "kalemden", -0.4), right_at=("c2s28", "iki", 1, -0.1), cam=("push", 0.07),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="iki kalem, iki biçim"),
    # ── 26. Machiavelli, onun ağzından oğullarına bir konuşma yazar ───────────
    shot("c1_machiavelli", ("c2s29", -0.1), mode="day", perde=1, longtake=True, plate_at=("c2s29", "Machiavelli", -0.2), plate_text="MACHIAVELLİ", rebel_who="old", rebel_at=("c2s29", "onun", -0.3),
         scroll_at=("c2s29", "konuşma", -0.4), scroll_to=("c2s29", "doğar", 0.2), stamp_at=("c2s29", "doğar", -0.6), stamp_text="ANEKDOT",
         cam=("push", 0.06), tr=("sayfa", 0.9), link="material", label="Machiavelli yazar (ANEKDOT)"),
    # ── 27. Cavalcanti, olaya daha yakın kalemle başka bir şey yazar ──────────
    shot("c2_kalemler", ("c2s30", -0.1), mode="day", perde=1, longtake=True, left_at=("c2s30", -0.5), right_at=("c2s30", -0.5), write_a=("c2s30", -0.5), write_b=("c2s30", "başka", -0.3), stamp_at=("c2s30", "yazar", 0.2),
         cam=[(("c2s30", -0.1), (-200, 0, 1.0, 0)), (("c2s30", "olaya", 0.0), (200, 10, 1.25, 0)), (("c2s30", "kimse", 0.0), (330, 10, 1.4, 0))],
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="Cavalcanti yazar (ANEKDOT)"),
    # ── 28. hangisi gerçekten söylendi, bilmiyoruz ────────────────────────────
    shot("c2_kalemler", ("c2s31", -0.1), mode="day", perde=1, left_at=("c2s31", -0.5), right_at=("c2s31", -0.5), write_a=("c2s29", -0.5), write_b=("c2s30", "başka", -0.3), q_at=("c2s31", "bilmiyoruz", -0.6),
         cam=[(("c2s31", -0.1), (330, 10, 1.4, 0)), (("c2s31", "söylendi", 0.0), (0, 0, 1.0, 0))],
         tr=("slide", 0.9, dict(dir="r")), link="cam", label="hangisi söylendi: bilmiyoruz"),
    # ── 29. Machiavelli onu yoksulun ihtiyacını kimse istemeden gideren biri çizer ──
    shot("c2_sadaka", ("c2s32", -0.1), mode="day", perde=1, who_at=("c2s32", "Machiavelli", -0.2), give_at=("c2s32", "yoksulun", -0.35), stamp_at=("c2s32", "çizer", -0.5),
         cam=("push", 0.07), tr=("slide", 0.9, dict(dir="l")), link="dir", label="yoksulun ihtiyacını kimse istemeden"),
    # ── 30. Ama o kalem Medici'nin siparişiyle çalışıyordu ────────────────────
    shot("c1_machiavelli", ("c2s33", -0.1), mode="day", perde=1, plate_at=("c2s33", "kalem", -0.3), order_big=("c2s33", "siparişiyle", -0.35),
         cam=("pull", 0.08), tr=("zoomthru", 0.9, dict(at=(1180, 520), at_b=(960, 520))), link="scale", label="o kalem Medici'nin siparişiyle çalışıyordu"),
    # ── 31. Giovanni öldüğünde oğlu Cosimo kırk yaşına yaklaşıyordu ───────────
    shot("p1_medal", ("c2s34", -0.1), key="m_cosimo", metal="bronze", pos="l", size=640, at=0.0, mode="night", perde=1, cam=("push", 0.07),
         ovl=P.ov(P.plate("COSIMO", 1380, 360, ("c2s34", "Cosimo", -0.15), role="GIOVANNI'NİN OĞLU", w=700),
                  P.count_up(1380, 650, ("c2s34", "Cosimo", 0.1), 39, dur=1.0, unit="YAŞINDAYDI", size=190, bg=True, unit_size=40),
                  P.label("1389 DOĞUMLU · HESAPLA", 1380, 850, ("c2s34", "kırk", -0.4), size=30, face="title_m", track=8)),
         tr=("iris", 0.9, dict(obj="seal", at=(500, 500), r=320)), link="shape", label="Cosimo: kırk yaşına yaklaşıyordu"),
    # ── 32. KAPI: şehrin en yüksek kulesinde bir hücre — sessiz, ağır ─────────
    shot("p1_sehir", ("c2s35", -0.1), scene="skyline_dikey", tod="day", mode="day", perde=1,
         cams=[(("c2s35", -0.1), (1120, 2900, 1.08)), (("c2s35", "kulesinde", 0.0), (1120, 3700, 1.02)), (("c2s35", "kapatılacaktı", 0.4), (1120, 4160, 1.0))],
         ovl=P.ov(P.desat(("c2s35", "şehrin", -0.1), ("c2s35", "kapatılacaktı", 0.3), k_max=0.75, dark=0.62, tint="#4A5068", tint_a=0.14),
                  P.glint(960, 520, ("c2s35", "hücreye", 0.0), r=70, dur=2.0, alpha=0.5)),
         cam=("crane", "up", 300), tr=("light", 0.9, dict(at=(960, 520))), link="light", label="kapı: şehrin en yüksek kulesi"),
]
YIL_AT = [(("c2s11", "1402'de", -0.1), 1402), (("c2s16", "1415'te", -0.1), 1415), (("c2s22", "1427'de", -0.1), 1427), (("c2s26", "1429'da", -0.1), 1429)]
