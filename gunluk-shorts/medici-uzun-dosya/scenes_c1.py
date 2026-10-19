"""c1 — Florin Şehri (1252–1397). Parça 1, 2/3. 240 sn, gerçek ses. Yönetmen kartı: yonetmen_c1.md.

İmza sekans: "Florin yolculuğu" — dönen florin → iris → Floransa panoraması (soldan sağa) → florin makro → lanetli çiçek → darphane (her vuruşta florin) → ... → köşeye iğne → bankaya zoomthru.
Işık/zaman: kaynak saat/hava söylemez → gündüz nötr; veba/Ciompi'de renk solması/kızıl yıkama yalnız anlatıma bağlı görsel dil (çan/şafak/gece iddiası yok).
Ağır sahneler (veba, Ciompi'nin ezilişi): mizah yok; beden/ceset/kan gösterilmez (siluet, toprak katmanı, pigment yıkama).
"""
import functools

from shots import shot
import cilt_medici as CM
import p1_ortak as P
import c1_kinds as K

S = "c1s"

SHOTS = [
    # ── 1. florin makro (c0'ın son sikkesinin devamı) ─────────────────────────
    shot("p1_coin", ("c1s1", 0), n=1, size=520, mode="day", perde=1,
         ovl=P.ov(P.label("1252", 960, 168, ("c1s1", "1252'de", 0.0), size=104, face="title", track=14, rise=22),
                  P.glint(960, 508, ("c1s1", "1252'de", 0.4), r=160)),
         cam=("push", 0.08), tr=("iris", 0.9, dict(obj="palle", at=(960, 358), r=114)), link="shape", label="florin, 1252"),
    # ── 2. Floransa panoraması (iris içinden açılır; soldan sağa kayma) ───────
    shot("p1_pano", ("c1s1", "altınını", -0.3), pano="florence", tod="day", mode="day", perde=1, cam=("push", 0.08),
         cams=[(("c1s1", "altınını", -0.3), (960, 0, 1.0)), (("c1s1", "şehrin", 0.0), (1900, 0, 1.02)), (("c1s2", -0.2), (3100, 0, 1.06))],
         ovl=P.label("FLORANSA", 960, 252, ("c1s1", "Floransa", 0.4), size=62, face="title", track=16, color="#F6E7B6"),
         tr=("iris", 0.9, dict(obj="florin", at=(960, 508), r=245)), link="shape", label="Floransa kendi altınını basıyor"),
    # ── 3. florin makro: 3,5 g · 2 cm · neredeyse saf altın ──────────────────
    shot("p1_coin", ("c1s2", -0.1), n=1, size=520, mode="day", perde=1,
         ovl=P.ov(P.count_up(400, 520, ("c1s2", "üç", -0.2), 3.5, dur=1.2, unit="GRAM", size=150, fmt=lambda v: f"{v:.1f}".replace(".", ",")),
                  P.dimline(708, 1212, 830, ("c1s2", "buçuk", 0.0), "2 CM"),
                  P.label("NEREDEYSE", 1500, 500, ("c1s2", "neredeyse", -0.1), size=48, track=10),
                  P.label("SAF ALTIN", 1500, 570, ("c1s2", "saf", -0.15), size=56, face="title", track=12),
                  P.glint(960, 508, ("c1s2", "saf", 0.1), r=190)),
         cam=("push", 0.07), tr=("zoomthru", 0.9, dict(at=(1000, 560), at_b=(960, 508))), link="scale", label="3,5 g · 2 cm"),
    # ── 4. Dante: lanetli çiçek ───────────────────────────────────────────────
    shot("c1_cicek", ("c1s3", -0.1), mode="day", perde=1,
         plate=("DANTE", ("c1s3", "Dante", -0.1), 330, 150),
         florin_at=("c1s3", -0.1), bloom_at=("c1s3", "lanetli", -0.45), curse_at=("c1s3", "lanetli", 0.0), shep_at=("c1s3", "dedi", -0.5),
         morph_at=("c1s3", "kurda", 0.0), flee_at=("c1s3", "çeviren", -0.4), quote_at=("c1s3", "lanetli", 0.0),
         cam=("push", 0.06), tr=("iris", 0.9, dict(obj="florin", at=(960, 508), r=240)), link="shape", label="lanetli çiçek"),
    # ── 5a. darphane: yine de basmaya devam ──────────────────────────────────
    shot("c1_darphane", ("c1s4", -0.1), mode="day", perde=1, cam=("push", 0.08),
         tr=("light", 0.9, dict(at=(205, 800))), link="light", label="darphane: basmaya devam"),
    # ── 5b. Villani: eski darphane yöneticisi, sayı saymayı bilir (kadraj masaya kayar) ──
    shot("c1_darphane", ("c1s5", "Kronikçi", -0.2), mode="day", perde=1, master_at=("c1s5", "Villani", -0.4), toff=4.4,
         cam=[(("c1s5", "Kronikçi", -0.2), (0, 0, 1.0, 0)), (("c1s5", "darphane", 0.0), (200, 0, 1.28, 0)), (("c1s5", "bilirdi", 0.0), (330, 20, 1.42, 0))],
         ovl=P.plate("GIOVANNI VILLANI", 1150, 150, ("c1s5", "Villani", -0.05), role="KRONİKÇİ · ESKİ DARPHANE YÖNETİCİSİ", w=740),
         tr=None, link="cam", label="Villani: sayı saymayı bilirdi"),
    # ── 6. 1338: kenti de saydı (90.000) ─────────────────────────────────────
    shot("p1_sehir", ("c1s6", -0.15), scene="meydan", act="kalabalik", dir="r", flags="lily", mode="day", perde=1, cam=("push", 0.07),
         ovl=P.ov(P.label("1338", 960, 215, ("c1s6", "1338'de", -0.1), size=84, face="title", track=14),
                  P.count_up(960, 430, ("c1s6", "doksan", -0.2), 90000, dur=1.5, unit="KİŞİ", size=190, bg=True),
                  P.stamp("VILLANI'YE GÖRE", 1470, 700, ("c1s6", "göre", 0.0), rot=-0.07, size=46, out=("c1s6", "çocuklar", -0.4))),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="1338: 90.000 kişi"),
    # ── 7. hesap okulları ─────────────────────────────────────────────────────
    shot("c1_okul", ("c1s6", "çocuklar", -0.4), mode="day", perde=1, kids_at=("c1s6", "çocuklar", -0.3), board_at=("c1s6", "hesap", -0.3), plate_at=("c1s6", "okullarına", -0.2),
         cam=("push", 0.07), tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="hesap okulları: defterlerin şehri"),
    # ── 8. Peruzzi: on beş şube (Medici icadı değil) + Bardi, ikisi de batar ─
    shot("c1_agi", ("c1s8", -0.15), mode="day", perde=1, longtake=True,
         hubs=[dict(label="PERUZZİ", x=620, y=540, rx=360, ry=210, n=15, build=(("c1s8", "Peruzzi", -0.0), ("c1s8", "vardı", -0.1)),
                    label_at=("c1s8", "Peruzzi", -0.2), die=(("c1s9", "battı", -0.3), ("c1s9", "battı", 1.4))),
               dict(label="BARDİ", x=1450, y=540, rx=300, ry=190, n=11, col="#8E2A30", build=(("c1s9", "Bardi", -0.3), ("c1s9", "Bardi", 0.8)),
                    label_at=("c1s9", "Bardi", -0.2), die=(("c1s9", "battı", -0.1), ("c1s9", "battı", 1.5)), ang0=-0.4)],
         intro_at=("c1s8", "şubeli", -0.1), count=dict(at=("c1s8", "Peruzzi", -0.1), to=("c1s8", "vardı", -0.1), n=15, x=960, y=185, label="ŞUBE"),
         medici_at=("c1s8", "Medici'nin", -0.15), medici_no_at=("c1s8", "değildi", -0.1),
         ovl=P.ov(P.stamp("BİR KAYNAĞA GÖRE", 1480, 330, ("c1s8", "kaynağa", 0.0), rot=-0.06, size=40, out=("c1s8", "Peruzzi", -0.4)),
                  P.label("1330'LAR", 1480, 250, ("c1s8", "1330'larda", -0.1), size=52, face="title", track=14, out=("c1s9", -0.2)),
                  P.label("1340'LAR", 1480, 250, ("c1s9", "1340'larda", -0.1), size=52, face="title", track=14)),
         cam=("push", 0.06), tr=("sayfa", 0.9), link="material", label="Peruzzi'nin 15 şubesi; Bardi; çöküş"),
    # ── 9. III. Edward'ın ödemediği borçlar ──────────────────────────────────
    shot("c1_edward", ("c1s9", "sebep", -0.2), mode="day", perde=1,
         plate_at=("c1s9", "İngiltere", -0.2), flow_at=("c1s9", "III.", -0.1), stop_at=("c1s9", "ödemediği", -0.2), stamp_at=("c1s9", "borçlar", 0.0),
         cam=("push", 0.07), tr=("carry", 0.9, dict(strip="ink", dir="r")), link="carry", label="Edward'ın ödemediği borç"),
    # ── 10a. kronikçi Villani (sol) ──────────────────────────────────────────
    shot("c1_kardes", ("c1s10", -0.1), mode="day", perde=1, chron_at=("c1s10", "kronikçi", -0.4), brother_at=("c1s10", "kardeşi", -0.4),
         link_at=("c1s10", "Peruzzi", -0.2), owner_at=("c1s10", "kaybedenlerin", -0.1),
         cam=[(("c1s10", -0.1), (-300, 0, 1.4, 0)), (("c1s10", "kardeşi", -0.3), (-300, 0, 1.5, 0))],
         tr=("slide", 0.9, dict(dir="l")), link="dir", label="kronikçi Villani"),
    # ── 10b. kardeşi Peruzzi'de çalışıyordu: kadraj sağa kayar, ip bağlanır ──
    shot("c1_kardes", ("c1s10", "kardeşi", -0.3), mode="day", perde=1, chron_at=("c1s10", "kronikçi", -0.4), brother_at=("c1s10", "kardeşi", -0.4),
         link_at=("c1s10", "Peruzzi", -0.2), owner_at=("c1s10", "kaybedenlerin", -0.1), toff=5.0,
         cam=[(("c1s10", "kardeşi", -0.3), (0, 0, 1.0, 0)), (("c1s10", "ailesindendi", 0.5), (0, 0, 1.16, 0))],
         tr=None, link="cam", label="sayıyı veren adam, kaybedenlerin ailesinden"),
    # ── 11. VEBA: Floransa'nın rengi solar ───────────────────────────────────
    shot("p1_skyline", ("c1s11", -0.15), seed=3, tod="day", mode="day", perde=1, pan=240,
         ovl=P.ov(P.desat(("c1s11", "1348", -0.2), ("c1s11", "kaldı", 0.1), k_max=0.93, dark=0.55, tint="#59607A", tint_a=0.18),
                  P.tablet_text("MART – TEMMUZ 1348", 960, 215, ("c1s11", "Mart'ında", -0.2), size=42, face="title_m", pad=44)),
         cam=("pan", "r", 240), tr=("yikama", 0.9), link="color", label="veba: renk solar"),
    # ── 12a. Boccaccio anlatır: sağlıklılar hastadan kaçar ───────────────────
    shot("c1_sokak", ("c1s12", -0.15), mode="day", perde=1,
         people=[dict(kind="halk", x0=1560, dir=-1, speed=300, h=232, seed=3, at=("c1s12", "sağlıklılar", -0.2), stil=dict(run=True)),
                 dict(kind="soylu_f", x0=1500, dir=-1, speed=280, h=226, seed=6, at=("c1s12", "sağlıklılar", 0.2), stil=dict(run=True)),
                 dict(kind="tuccar", x0=1620, dir=-1, speed=320, h=236, seed=9, at=("c1s12", "hastadan", -0.2), stil=dict(run=True)),
                 dict(kind="halk", x0=1700, dir=1, speed=0, h=226, seed=14, at=("c1s12", -0.3), action="idle", cf="#2A2018")],
         ovl=P.ov(P.desat(("c1s12", -0.2), ("c1s12", "sağlıklılar", 0.0), k_max=0.93, dark=0.55, tint="#59607A", tint_a=0.18, k_start=0.95),
                  P.plate("BOCCACCIO", 340, 205, ("c1s12", "Boccaccio", -0.1), role="ANLATIR")),
         cam=("push", 0.06), tr=("zoomthru", 0.9, dict(at=(1100, 460), at_b=(960, 520))), link="scale", label="Boccaccio: sağlıklılar kaçar"),
    # ── 12b. hasta yalnız: boş oda, pencere ışığı solar (beden yok) ──────────
    shot("p1_oda", ("c1s12", "hasta", -0.3), room="bos", variant="koln", path="in", tod="day", mode="day", perde=1, fade_at=("c1s12", "hasta", -0.1), fade_dur=3.4,
         actors=[dict(kind="halk", x=1020, y=806, h=270, action="idle", sil="#0E0806", seed=5, dir=1, rim_dir=1)], cam=("push", 0.08),
         ovl=P.desat(("c1s12", "hasta", -0.3), ("c1s12", "hasta", -0.2), k_max=0.93, dark=0.45, tint="#59607A", tint_a=0.18, k_start=0.95),
         tr=("candle", 1.0, dict(at=(960, 640), at_b=(1200, 560))), link="light", label="hasta yalnız"),
    # ── 12c. kapılar kapanır; sokak boş ──────────────────────────────────────
    shot("c1_sokak", ("c1s12", "evlerde", -0.4), mode="day", perde=1, door_at=("c1s12", "evlerde", -0.1), people=[],
         ovl=P.desat(("c1s12", "evlerde", -0.4), ("c1s12", "evlerde", -0.3), k_max=0.95, dark=0.7, tint="#59607A", tint_a=0.2, k_start=0.97),
         cam=("push", 0.06), tr=("slide", 0.9, dict(dir="l")), link="dir", label="kapılar kapanır, sokak boş"),
    # ── 13a. Stefani, 12 yaşında ─────────────────────────────────────────────
    shot("c1_sokak", ("c1s13", -0.1), mode="day", perde=1,
         people=[dict(kind="cocuk", x0=1180, dir=1, speed=0, h=180, seed=5, at=("c1s13", -0.2), action="idle"),
                 dict(kind="halk", x0=1560, dir=-1, speed=70, h=226, seed=8, at=("c1s13", -0.2), cf="#2A2018")],
         ovl=P.ov(P.desat(("c1s13", -0.2), ("c1s13", 0.0), k_max=0.93, dark=0.5, tint="#59607A", tint_a=0.18, k_start=0.95),
                  P.plate("MARCHIONNE DI COPPO STEFANI", 960, 205, ("c1s13", "Stefani", -0.1), w=900),
                  P.count_up(1500, 520, ("c1s13", "iki", -0.2), 12, dur=0.9, unit="YAŞINDA", size=170)),
         cam=("pull", 0.08), tr=("slide", 0.9, dict(dir="r")), link="dir", label="Stefani: on iki yaşında"),
    # ── 13b. yıllar sonra: kronik yazılır ────────────────────────────────────
    shot("p1_oda", ("c1s13", "yıllar", -0.4), room="calisma", variant="kutuphane", figure="desk", tod="day", mode="day", perde=1,
         path="scribe", cam=("push", 0.08), ovl=P.label("YILLAR SONRA", 960, 205, ("c1s13", "yıllar", -0.2), size=58, face="title", track=16),
         tr=("candle", 1.0, dict(at=(960, 640), at_b=(1200, 560))), link="light", label="yıllar sonra: kronik"),
    # ── 13c. toplu çukurlar, katman katman toprak (beden yok) ───────────────
    shot("c1_toprak", ("c1s13", "ölülerin", -0.25), mode="night", perde=1, pit_at=("c1s13", "çukurlara", -0.25), layers_at=("c1s13", "üstlerinin", -0.15), layers_to=("c1s13", "örtüldüğünü", 0.3),
         ovl=P.label("KATMAN KATMAN", 960, 215, ("c1s13", "katman", -0.1), size=52, face="title_m", track=16, color="#E8D49A"),
         cam=("push", 0.07), tr=("dip", 0.9), link="color", label="çukur, katman katman toprak"),
    # ── 14. ne düşündüğünü bilmiyoruz; ne gördüğünü yazdığını biliyoruz ─────
    shot("c1_yazi", ("c1s14", -0.1), mode="night", perde=1, q_at=("c1s14", "düşündüğünü", -0.3), q_out=("c1s14", "ne", 0.7), w_at=("c1s14", "gördüğünü", -0.2), w_to=("c1s14", "biliyoruz", 0.4),
         cam=("push", 0.06), tr=("slide", 0.9, dict(dir="u")), link="dir", label="bilmiyoruz → yazdığını biliyoruz"),
    # ── 15. 1378: bu kez öfke sokaktaydı ─────────────────────────────────────
    shot("p1_procession", ("c1s15", -0.1), dir="l", density=1.6, seed=4, speed=150.0, mode="day", perde=1,
         ovl=P.label("1378", 960, 215, ("c1s15", "1378'de", -0.1), size=88, face="title", track=14),
         cam=("push", 0.08), tr=("yikama", 0.9), link="color", label="1378: öfke sokakta (sağdan sola kabarır)"),
    # ── 16a. Medici ailesinin başka bir kolundan Salvestro ───────────────────
    shot("p1_tree", ("c1s16", -0.1), title="MEDİCİ AİLESİ", mode="day", perde=1, cam=("push", 0.07),
         nodes=[dict(id="r", icon="shield", name="MEDİCİ AİLESİ", x=0.5, y=0.30, at=("c1s16", "Medici", -0.2), size=170, nsize=34),
                dict(id="s", icon="flag", name="SALVESTRO", x=0.30, y=0.66, at=("c1s16", "Salvestro", -0.25), size=170, nsize=34),
                dict(id="g", icon="family", name="BAŞKA BİR KOL", x=0.70, y=0.66, at=("c1s16", "başka", -0.3), size=170, nsize=34)],
         edges=[("r", "s", ("c1s16", "kolundan", -0.1)), ("r", "g", ("c1s16", "başka", 0.0))],
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Medici ailesinin başka bir kolu: Salvestro"),
    # ── 16b. halkın alkışıyla gonfaloniere ───────────────────────────────────
    shot("p1_sehir", ("c1s16", "halkın", -0.3), scene="meydan", act="kalabalik", dir="r", flags="medici", mode="day", perde=1, cam=("push", 0.07),
         ovl=P.ov(P.plate("SALVESTRO DE' MEDİCİ", 400, 215, ("c1s16", "halkın", 0.2), role="GONFALONIERE SEÇİLDİ", w=760),
                  P.icon_at("flag", 1400, 330, ("c1s16", "gonfaloniere", -0.15), size=210, glow=True, bob=6),
                  P.stamp("AKTARILIR", 1390, 660, ("c1s16", "gonfaloniere", 0.4), rot=-0.07, size=44)),
         tr=("zoomthru", 0.9, dict(at=(960, 560), at_b=(960, 520))), link="scale", label="halkın alkışıyla gonfaloniere"),
    # ── 17. yün işçilerinin loncası yoktu ────────────────────────────────────
    shot("c1_lonca", ("c1s17", -0.1), mode="day", perde=1, rows_at=("c1s17", "Ama", 0.0), carder_at=("c1s17", "yün", -0.2), empty_at=("c1s17", "loncası", -0.15), mute_at=("c1s17", "sesi", -0.2),
         cam=("push", 0.07), tr=("carry", 0.95, dict(strip="banner", dir="r")), link="carry", label="21 lonca; yün işçisinin yeri boş"),
    # ── 18a. 22 Temmuz: Ciompi Palazzo Vecchio'yu alır ───────────────────────
    shot("p1_sehir", ("c1s18", -0.1), scene="meydan", act="kalabalik", dir="l", flags="stripes", riders=0, mode="day", perde=1, cam=("push", 0.07),
         ovl=P.ov(P.label("22 TEMMUZ 1378", 960, 215, ("c1s18", "Temmuz'da", -0.1), size=72, face="title", track=14, out=("c1s18", "Palazzo", 0.9)),
                  P.stamp("CIOMPI", 1470, 380, ("c1s18", "Ciompi", 0.0), rot=-0.07, size=64, out=("c1s18", "ele", 0.0))),
         tr=("slide", 0.9, dict(dir="l")), link="dir", label="Ciompi Palazzo Vecchio'yu ele geçirir"),
    # ── 18b. kule: yün tarayıcısı gonfaloniere; Salvestro çekilir ────────────
    shot("p1_sehir", ("c1s18", "bir", -0.2), scene="skyline_dikey", tod="day", mode="day", perde=1, cam=("crane", "up", 300),
         ovl=P.ov(P.plate("MICHELE DI LANDO", 460, 760, ("c1s18", "Michele", -0.3), role="YÜN TARAYICISI → GONFALONIERE", w=800, out=("c1s18", "Salvestro", 0.5)),
                  P.plate("SALVESTRO", 1500, 760, ("c1s18", "Salvestro", -0.1), role="ÇEKİLDİ", w=560)),
         tr=("zoomthru", 0.9, dict(at=(1000, 420), at_b=(960, 520))), link="scale", label="kule: Michele di Lando gonfaloniere"),
    # ── 19. talepler (yazıldığına göre) ──────────────────────────────────────
    shot("p1_oda", ("c1s19", -0.1), room="salon", variant="signoria", tod="day", mode="day", perde=1, path="default", cam=("push", 0.06),
         ovl=P.ov(P.tablet_icon("scales", "VERGİDE ADALET", 540, 250, ("c1s19", "vergide", -0.15)),
                  P.tablet_icon("shield", "İŞÇİLERE LONCA HAKKI", 560, 390, ("c1s19", "lonca", -0.15)),
                  P.tablet_icon("coins", "KAMU BORCUNUN AZALTILMASI", 640, 530, ("c1s19", "borcunun", -0.2), w=780),
                  P.stamp("YAZILDIĞINA GÖRE", 1500, 300, ("c1s19", "yazıldığına", 0.0), rot=-0.06, size=40)),
         tr=("zoomthru", 0.9, dict(at=(960, 150), at_b=(960, 520))), link="scale", label="Ciompi'nin talepleri"),
    # ── 20–21. Machiavelli isyancının ağzına konuşma koyar (KURGU) ──────────
    shot("c1_machiavelli", ("c1s20", -0.1), mode="day", perde=1, longtake=True, plate_at=("c1s20", "Machiavelli", -0.2), order_at=("c1s20", "siparişiyle", -0.2),
         rebel_at=("c1s20", "adı", -0.5), nameless_at=("c1s20", "belli", -0.25), scroll_at=("c1s20", "isyancının", -0.1), scroll_to=("c1s21", "isyancının", 0.0), stamp_at=("c1s21", "isyancının", -0.25),
         cam=("push", 0.06), tr=("sayfa", 0.9), link="material", label="Machiavelli: isyancının ağzına konuşma (kurgu)"),
    # ── 22. loncaların milisleri isyanı ezdi (ağır; beden yok) ────────────────
    shot("p1_procession", ("c1s22", -0.1), dir="l", density=1.3, seed=9, speed=150.0, mix=dict(guard=0.65, banner=0.2, common=0.1, noble=0.05), mode="day", perde=1,
         ovl=P.ov(P.dim(("c1s22", "milisleri", 0.0), ("c1s23", -0.0), alpha=0.5),
                  P.label("AĞUSTOS SONU", 960, 215, ("c1s22", "Ağustos", -0.1), size=60, face="title", track=14, color="#F6E7B6", out=("c1s23", -0.1))),
         cam=("push", 0.08), tr=("slide", 0.9, dict(dir="l")), link="dir", label="loncaların milisleri"),
    # ── 23. en kanlı günlerden biri: Floransa'nın üstüne kızıl pigment yıkama ──
    shot("p1_skyline", ("c1s23", -0.15), seed=5, tod="day", mode="day", perde=1, pan=220,
         ovl=P.ov(P.desat(("c1s23", -0.1), ("c1s23", "tarihinin", 0.2), k_max=0.8, dark=0.45),
                  P.red_bleed(("c1s23", "tarihinin", -0.3), dur=2.4, alpha=0.62)),
         cam=("pan", "l", 220), tr=("yikama", 0.9), link="color", label="Floransa tarihinin en kanlı günlerinden biri (yıkama)"),
    # ── 24. Medici adı bir kademe altta; kır gelirleri ───────────────────────
    shot("c1_kademe", ("c1s24", -0.1), mode="day", perde=1, elite_at=("c1s24", "seçkinlerin", -0.35), medici_at=("c1s24", "Medici", -0.1), field_at=("c1s24", "kır", -0.6), income_at=("c1s24", "gelirleriyle", -0.3),
         cam=("push", 0.07), tr=("yikama", 0.9), link="color", label="bir kademe altta; kır gelirleri"),
    # ── 25. Giovanni di Bicci: küçük bir pay ─────────────────────────────────
    shot("p1_medal", ("c1s25", -0.1), key="m_giovanni", metal="bronze", pos="l", size=620, at=0.0, mode="day", perde=1,
         ovl=P.ov(P.plate("GIOVANNI DI BICCI", 1380, 380, ("c1s25", "Giovanni", -0.1), role="MEDİCİ AİLESİNDEN", w=720),
                  P.icon_at("coinbag", 1380, 640, ("c1s25", "mütevazı", -0.2), size=130, glow=True, bob=5),
                  P.label("KÜÇÜK BİR PAY", 1380, 790, ("c1s25", "küçük", -0.15), size=46, face="title_m", track=12)),
         cam=("push", 0.07), tr=("iris", 0.9, dict(obj="palle", at=(915, 750), r=95)), link="shape", label="Giovanni di Bicci: küçük pay"),
    # ── 26a. Roma: Vieri di Cambio'nun bankası ───────────────────────────────
    shot("p1_map", ("c1s26", -0.1), mode="day", perde=1, approx=False, cam=("push", 0.08),
         cams=[(("c1s26", -0.1), (11.9, 43.0, 3.3)), (("c1s26", "Vieri", 0.3), (12.3, 42.2, 5.4))],
         cities=[dict(lon=11.25, lat=43.77, name="FLORANSA", kind="capital", at=("c1s26", -0.0), size=32), dict(lon=12.50, lat=41.89, name="ROMA", kind="capital", at=("c1s26", "Roma'da", -0.2), size=36)],
         routes=[dict(pts=[(11.25, 43.77), (11.8, 42.9), (12.50, 41.89)], at=("c1s26", "Roma'da", -0.3), dur=2.0, width=7)],
         ovl=P.plate("VIERI DI CAMBIO'NUN BANKASI", 1380, 250, ("c1s26", "Cambio'nun", -0.1), w=880),
         tr=("zoomthru", 0.9, dict(at=(960, 500), at_b=(960, 520))), link="scale", label="Roma: Vieri di Cambio'nun bankası"),
    # ── 26b. alacak ve borçlar devredilir ────────────────────────────────────
    shot("p1_ledger", ("c1s26", "Vieri", 1, -0.2), head="ROMA", title_l="ALACAK", title_r="BORÇ",
         left=[dict(text="Roma işinin alacakları", at=("c1s26", "alacak", -0.1), hl=("c1s26", "devraldı", -0.2))],
         right=[dict(text="Roma işinin borçları", at=("c1s26", "borçlarını", -0.1), hl=("c1s26", "devraldı", -0.2))],
         mode="day", perde=1, seed=7, focus=(600, 380),
         ovl=P.ov(P.tablet_text("1390'LARIN BAŞI", 960, 880, ("c1s26", "1390'ların", -0.2), size=44, face="title_m", pad=50),
                  P.stamp("DEVRALDI", 1450, 880 - 70, ("c1s26", "devraldı", -0.1), rot=-0.08, size=64)),
         cam=("push", 0.07), tr=("sayfa", 0.9), link="material", label="alacak ve borçlar devralınır"),
    # ── 27a. Piccarda Bueri'nin çeyizi: 1.500 florin ─────────────────────────
    shot("p1_coin", ("c1s27", -0.1), n=1, size=420, pos=(520, 560), mode="day", perde=1, cam=("push", 0.07),
         ovl=P.ov(P.count_up(1290, 540, ("c1s27", "bin", -0.25), 1500, dur=1.5, unit="FLORİN", size=200),
                  P.icon_at("ring", 1630, 330, ("c1s27", "Piccarda", -0.1), size=170, glow=True, bob=6),
                  P.label("EVLİLİK ÇEYİZİ", 1630, 450, ("c1s27", "çeyiziyle", -0.15), size=38, face="title_m", track=10),
                  P.label("PICCARDA BUERI'NİN ÇEYİZİ", 960, 215, ("c1s27", "Piccarda", -0.15), size=54, face="title", track=12)),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="1.500 florinlik çeyiz"),
    # ── 27b. ilk sermaye = bir evlilik sözleşmesi ────────────────────────────
    shot("p1_doc", ("c1s27", "hanedanın", -0.3), title="EVLİLİK SÖZLEŞMESİ", lines=[], seal=True, seal_at=("c1s27", "sözleşmesiydi", -0.2), w=1000, h=640, mode="day", perde=1, cam=("push", 0.07),
         ovl=P.ov(P.icon_at("ring", 960, 560, ("c1s27", "evlilik", -0.15), size=210, glow=True, bob=5),
                  P.stamp("İLK SERMAYE", 1380, 330, ("c1s27", "sermayesi", -0.15), rot=-0.08, size=60)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="hanedanın ilk sermayesi: evlilik sözleşmesi"),
    # ── 28a. 1397: iş Roma'dan Floransa'ya taşınır ───────────────────────────
    shot("p1_map", ("c1s28", -0.1), mode="day", perde=1, approx=False, cam=("push", 0.08),
         cams=[(("c1s28", -0.1), (12.0, 42.8, 4.0)), (("c1s28", "Floransa'ya", 0.0), (11.7, 43.2, 5.4))],
         cities=[dict(lon=12.50, lat=41.89, name="ROMA", kind="capital", at=("c1s28", -0.0), size=34), dict(lon=11.25, lat=43.77, name="FLORANSA", kind="capital", at=("c1s28", "Floransa'ya", -0.2), size=34)],
         routes=[dict(pts=[(12.50, 41.89), (11.8, 42.9), (11.25, 43.77)], at=("c1s28", "Roma'dan", -0.25), dur=2.0, width=8)],
         ovl=P.label("1397", 960, 215, ("c1s28", "1397'de", -0.1), size=88, face="title", track=14),
         tr=("yikama", 0.9), link="material", label="1397: Roma'dan Floransa'ya taşınma"),
    # ── 28b. Orsanmichele köşesi: iki sokağın kesiştiği yer ──────────────────
    shot("c1_kose", ("c1s28", "Orsanmichele", -0.5), mode="day", perde=1, orsa_at=("c1s28", "Orsanmichele", -0.3), street1_at=("c1s28", "Porta", -0.2), street2_at=("c1s28", "Calimala", -0.2), pin_at=("c1s28", "köşeye", -0.35),
         cam=("push", 0.07), tr=("zoomthru", 0.9, dict(at=(1500, 300), at_b=(960, 520))), link="scale", label="Orsanmichele köşesi: iğne"),
    # ── 29–32. köşede bir masa ve bir defter; sermaye on bin florin; faiz günahtır (uzun plan) ──
    shot("p1_oda", ("c1s29", -0.1), room="banka", tod="day", mode="day", perde=1, longtake=True,
         cams=[(("c1s29", -0.1), (1500, 20, 1.05)), (("c1s30", -0.1), (900, 40, 1.15)), (("c1s30", "masa", 0.0), (640, 70, 1.5)), (("c1s32", "faiz", 0.0), (560, 80, 1.62))],
         ovl=P.ov(P.count_up(960, 400, ("c1s29", "on", -0.15), 10000, dur=1.1, unit="FLORİN", size=190, out=("c1s30", -0.0), bg=True),
                  P.label("BİR MASA VE BİR DEFTER", 960, 215, ("c1s30", "masa", -0.2), size=58, face="title", track=14, out=("c1s31", 0.0)),
                  P.tablet_text("“FAİZ GÜNAHTIR”", 960, 270, ("c1s32", "faiz", -0.25), size=66, face="title_m", pad=60),
                  P.icon_at("cross", 1560, 400, ("c1s32", "Kilise'nin", -0.1), size=230, glow=True, bob=5),
                  P.glint(700, 700, ("c1s32", "huzurla", 0.0), r=220, dur=1.2)),
         cam=("push", 0.06), tr=("zoomthru", 0.9, dict(at=(960, 520), at_b=(960, 520))), link="scale", label="köşede bir masa, bir defter; faiz günahtır"),
]
YIL_AT = [(("c1s6", "1338'de", -0.1), 1338), (("c1s11", "Veba", -0.1), 1348), (("c1s15", "1378'de", -0.1), 1378), (("c1s28", "1397'de", -0.1), 1397)]
