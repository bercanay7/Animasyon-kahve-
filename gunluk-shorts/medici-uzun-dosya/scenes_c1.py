"""c1 — Florin Şehri (1252–1397). Parça 1, 2/3. 234 sn, gerçek ses. Yönetmen kartı: yonetmen_c1.md.

İmza sekans: "Florin yolculuğu" — dönen florin → iris → Floransa panoraması → florin makro → lanetli çiçek → darphane → ... → köşeye iğne → bankaya zoomthru.
KURUL TUR 1 (4 Kasım): yol haritası çipleri (PK2-K7: ALTIN · HESAP · VEBA · ÖFKE → ASIL HİKÂYE: MEDİCİ); zambak kırmızı/beyaz + etamin (SA2-K9);
abaküs yok → yazılı rakam + sayma bezi (KA1-V1/SA2-Ö3); Peruzzi sayım odası (iki figür + defter rafı) ve Villani = PERUZZİ ORTAĞI (teyit c1s10);
Peruzzi/Bardi çöküşü + III. Edward montajı (sert kesme); 1378 kalabalığında atlı yok, halk kadrosu, Medici sancağı yok (flag_ctx); KURAYLA (kese + isim fişi);
"ÇEKİLDİ" yok; Machiavelli iki figür + raf (çalışma odası); c1s23 kızıl yıkama yerine loncanın kaldırılması ve dışlanma; "MEDİCİ'NİN BU KOLU";
Vieri = GIOVANNI'NİN PATRONU; Orsanmichele levhası yalnız VIA PORTA ROSSA (teyit §3.5); son uzun plan bölündü; YIL_AT'a 1390 adımı.
Işık/zaman: kaynak saat/hava söylemez → gündüz nötr; veba/Ciompi'de renk solması yalnız anlatıma bağlı görsel dil (çan/şafak/gece iddiası yok).
Ağır sahneler (veba, Ciompi'nin ezilişi): mizah yok; beden/ceset/kan gösterilmez (siluet, toprak katmanı, pigment yıkama).
"""
import anim
from shots import shot
import cilt_medici as CM
import p1_ortak as P
import c1_kinds as K
import c2_kinds as K2

G = P.GIOVANNI
VILLANI = dict(kind="banker", seed=11)             # c1s5 darphane yöneticisi ile aynı figür
PERUZZI_A = dict(kind="banker", seed=21)
PERUZZI_B = dict(kind="banker", seed=23)
VIERI = dict(kind="banker", seed=71)
OFIS_P = dict(room="p1ofis", variant="peruzzi", tod="day", mode="day", perde=1, figure=None)
DAY = dict(tod="day", mode="day", perde=1)
TEMSILI = lambda at, out=None: P.tag("ARMALAR TEMSİLÎ", 300, 880, at, size=34, out=out)   # noqa: E731

SHOTS = [
    # ── 1. florin makro (c0'ın son sikkesinin devamı) ─────────────────────────
    shot("p1_coin", ("c1s1", 0), n=1, size=520, mode="day", perde=1,
         ovl=P.ov(P.label("1252", 960, 168, ("c1s1", "1252'de", 0.0), size=104, face="title", track=14, rise=22),
                  P.glint(960, 508, ("c1s1", "1252'de", 0.4), r=160)),
         cam=("push", 0.07), tr=("iris", 0.9, dict(obj="palle", at=(960, 358), r=114)), link="shape", label="florin, 1252"),
    # ── 2. Floransa panoraması (iris içinden; soldan sağa) ──────────────────
    shot("p1_pano", ("c1s1", "altınını", -0.3), pano="florence", **DAY,
         cams=[(("c1s1", "altınını", -0.3), (960, 0, 1.0)), (("c1s1", "şehrin", 0.0), (1900, 0, 1.02)), (("c1s2", -0.2), (3100, 0, 1.06))],
         ovl=P.tag("FLORANSA", 960, 252, ("c1s1", "Floransa", 0.4), size=52),
         cam=("pan", "r"), tr=("iris", 0.35, dict(obj="florin", at=(960, 508), r=245)), link="shape", label="Floransa kendi altınını basıyor"),
    # ── 3. florin makro: 3,5 g · 2 cm · neredeyse saf altın ──────────────────
    shot("p1_coin", ("c1s2", -0.1), n=1, size=520, mode="day", perde=1,
         ovl=P.ov(P.count_up(400, 520, ("c1s2", "üç", -0.2), 3.5, dur=1.2, unit="GRAM", size=150, fmt=lambda v: f"{v:.1f}".replace(".", ",")),
                  P.dimline(708, 1212, 830, ("c1s2", "buçuk", 0.0), "2 CM"),
                  P.label("NEREDEYSE", 1500, 500, ("c1s2", "neredeyse", -0.1), size=48, track=10),
                  P.label("SAF ALTIN", 1500, 570, ("c1s2", "saf", -0.15), size=56, face="title", track=12),
                  P.glint(960, 508, ("c1s2", "saf", 0.1), r=190)),
         cam=("pull",), tr=("zoomthru", 0.9, dict(at=(1000, 560), at_b=(960, 508))), link="scale", label="3,5 g · 2 cm"),
    # ── 4. Dante: lanetli çiçek (Floransa zambağı: altın → lanette kızıl; beyaz komün zemini; etamin) — HUD gizli (kurul tur 2 SA2-Y3/KA2-D2:
    #       "lanetli çiçek" dizesi ≈1320'lerin, HUD 1252 olayı yanlış tarihliyordu) ──
    shot("c1_cicek", ("c1s3", -0.1), mode="day", perde=1, hud=False,
         plate=("DANTE", ("c1s3", "Dante", -0.1), 381, 150),
         florin_at=("c1s3", -0.1), bloom_at=("c1s3", "lanetli", -0.45), curse_at=("c1s3", "lanetli", 0.0), shep_at=("c1s3", "dedi", -0.5),
         morph_at=("c1s3", "kurda", 0.0), flee_at=("c1s3", "çeviren", -0.4), quote_at=("c1s3", "lanetli", 0.0),
         cam=("push",), tr=("iris", 1.1, dict(obj="florin", at=(960, 508), r=240)), link="shape", label="lanetli çiçek"),
    # ── 5. darphane — TEK ÇEKİM (kurul tur 2 AN2-Ö1 #23: eski 5a→5b aynı kadrajda sert kesmeydi, ×0,99 + 80 px, işçinin pozu sıçrıyordu):
    #       "Floransa, yine de"de sert kesme → çekiç/örs yakın; "Kronikçi Giovanni Villani"de kamera uçan sikkeleri izleyerek sağa kayar → yığın ve
    #       masasında sayan Villani (soldurma yok: baştan orada, kadraj dışında). Işık patlaması kalktı (c0+c1'de yalnız iki ifşa anı). ──
    shot("c1_darphane", ("c1s4", -0.1), mode="day", perde=1, master_at=("c1s4", -1.0),
         cam=[(("c1s4", -0.1), (-470, 30, 1.40, 0)), (("c1s4", "devam", 0.0), (-400, 30, 1.38, 0)), (("c1s5", "Villani", -0.3), (120, 10, 1.12, 0)),
              (("c1s5", "darphane", 0.0), (230, 0, 1.22, 0)), (("c1s5", "bilirdi", 0.0), (330, 20, 1.42, 0))],
         ovl=P.plate("GİOVANNİ VİLLANİ", 1120, 170, ("c1s5", "Villani", -0.05), role="KRONİKÇİ · ESKİ DARPHANE YÖNETİCİSİ", w=760),
         tr="cut", link="audio", label="darphane: basmaya devam → Villani sayar"),
    # ── 6. 1338: kenti de saydı (≈90.000 — Villani'nin tahmini) ──────────────
    shot("p1_sehir", ("c1s6", -0.15), scene="meydan", act="kalabalik", dir="r", flags="lily", riders=0, flag_ctx="kalabalik", **DAY,
         ovl=P.ov(P.tag("1338", 400, 200, ("c1s6", "1338'de", -0.1), size=60),
                  P.count_up(960, 430, ("c1s6", "yaklaşık", -0.45), 90000, dur=1.4, unit="KİŞİ", size=190, bg=True, prefix="≈"),
                  # kurul tur 2 (KA1-K4/TE2-Y5): damga sayaç kartının üstüne biniyordu → kartın ÜSTÜNDE, gök zemininde, kartla arası boş
                  anim.stamp_ovl("VİLLANİ'YE GÖRE · TAHMİN", 1030, 196, ("c1s6", "göre", 0.1), "ink", rot=-0.04, size=44, out=("c1s6", "çocuklar", -0.4))),
         cam=("pan", "r"), tr=("slide", 0.7, dict(dir="r")), link="dir", label="1338: ≈90.000 kişi (tahmin)"),
    # ── 7. hesap okulları: yazılı rakamlar + sayma bezi (abaküs yok); defterlerin şehri ──
    shot("c1_okul", ("c1s6", "çocuklar", -0.4), mode="day", perde=1, kids_at=("c1s6", "çocuklar", -0.3), board_at=("c1s6", "hesap", -0.5), plate_at=("c1s6", "okullarına", -0.2),
         ovl=P.tag("DEFTERLERİN ŞEHRİ", 960, 880, ("c1s7", "Defterlerin", -0.1), size=48),
         cam=("push",), tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="hesap okulları: defterlerin şehri"),
    # ── 8. çok şubeli banka: Medici'nin icadı değil ──────────────────────────
    shot("c1_agi", ("c1s8", -0.15), mode="day", perde=1, hubs=[], keep_intro=True,
         intro_at=("c1s8", "şubeli", -0.1), medici_at=("c1s8", "Medici'nin", -0.15), medici_no_at=("c1s8", "değildi", -0.1),
         cam=("pull",), tr=("slide", 0.3, dict(dir="r")), link="dir", label="çok şubeli banka: Medici'nin icadı değil"),
    # ── 9. Peruzzi sayım odası (1330'lar): iki ortak + defter rafı; 15 şube (bir kaynağa göre) ──
    shot("p1_oda", ("c1s8", "bir", -0.3), **OFIS_P,
         actors=[dict(PERUZZI_A, x=560, y=880, h=450, action="count", dir=1, layer="front"),
                 dict(PERUZZI_B, x=1240, y=880, h=450, action="talk", at=("c1s8", "Peruzzi", -0.3), dir=-1, layer="front")],
         cams=[(("c1s8", "bir", -0.3), (880, 40, 1.20)), (("c1s9", -0.2), (980, 56, 1.30))],
         ovl=P.ov(P.tag("PERUZZİ BANKASI · 1330'LAR", 700, 190, ("c1s8", "1330'larda", -0.2), size=46),
                  P.count_up(1440, 470, ("c1s8", "on", -0.35), 15, dur=0.8, unit="ŞUBE", size=190, bg=True, min_w=330, unit_size=44),
                  anim.stamp_ovl("BİR KAYNAĞA GÖRE", 1440, 290, ("c1s8", "kaynağa", 0.1), "ink", rot=-0.05, size=40)),
         cam=("push",), tr="cut", link="audio", label="Peruzzi sayım odası: 15 şube"),
    # ── 10a. MONTAJ: Peruzzi de Bardi de 1340'larda battı (sert kesmeler) ─────
    shot("c1_agi", ("c1s9", -0.15), mode="day", perde=1, montage=True,
         hubs=[dict(label="PERUZZİ", x=620, y=540, rx=360, ry=210, n=15, build=(("c1s8", -0.2), ("c1s8", -0.1)), label_at=("c1s8", -0.2),
                    die=(("c1s9", "battı", -0.3), ("c1s9", "battı", 0.9))),
               dict(label="BARDİ", x=1400, y=540, rx=330, ry=200, n=15, col="#8E2A30", build=(("c1s8", -0.2), ("c1s8", -0.1)), label_at=("c1s8", -0.2),
                    die=(("c1s9", "battı", -0.1), ("c1s9", "battı", 1.0)), ang0=-0.4)],
         ovl=P.ov(P.tag("1340'LAR", 960, 200, ("c1s9", "1340'larda", -0.2), size=56),
                  P.tag("ŞUBE SAYILARI TEMSİLÎ", 1500, 880, ("c1s9", -0.15), size=34)),
         cam=("push", 0.07, dict(shake=[(("c1s9", "battı", 0.0), 4)])), tr="cut", link="audio", label="Peruzzi ve Bardi batar"),
    # ── 10b. MONTAJ: III. Edward'ın ödemediği borçlar ────────────────────────
    shot("c1_edward", ("c1s9", "sebep", -0.2), mode="day", perde=1, montage=True,
         plate_at=("c1s9", "İngiltere", -0.2), flow_at=("c1s9", "III.", -0.1), stop_at=("c1s9", "ödemediği", -0.2), stamp_at=("c1s9", "borçlar", 0.0),
         cam=("truck", "r"), tr="cut", link="audio", label="Edward'ın ödemediği borç"),
    # ── 11. kronikçi Villani de Peruzzi'nin ortağıydı (aynı sayım odası: geri çağırma); kaybedenlerin içinden ──
    shot("p1_oda", ("c1s10", -0.15), **OFIS_P,
         actors=[dict(VILLANI, x=946, y=823, h=280, action="write", seated=True, dir=1),
                 dict(PERUZZI_A, x=560, y=880, h=450, action="count", dir=1, layer="front"),
                 dict(PERUZZI_B, x=1420, y=880, h=450, action="idle", dir=-1, layer="front")],
         cams=[(("c1s10", -0.15), (1060, 40, 1.16)), (("c1s10", "Peruzzi'nin", -0.2), (1000, 60, 1.34)), (("c1s10", "kaybedenlerin", 0.0), (980, 66, 1.42))],
         # kurul tur 2 (SA2-Y5/KA1-Ö2/KA2-D4; başkan DBI "Villani, Giovanni" ile doğruladı): 1341'de batan Peruzzi değil, Villani'nin yönettiği Buonaccorsi
         ovl=P.ov(P.plate("GİOVANNİ VİLLANİ", 1260, 180, ("c1s10", "Villani", -0.3), role="1300'DE PERUZZİ ORTAĞI · YÖNETTİĞİ BUONACCORSİ 1341'DE BATTI", w=1030),
                  P.desat(("c1s10", "kaybedenlerin", -0.2), ("c1s10", "içindendi", 0.6), k_max=0.7, dark=0.25, tint="#6E7480", tint_a=0.12)),
         cam=("push",), tr=("zoomthru", 0.7, dict(at=(960, 560), at_b=(960, 520))), link="scale", label="Villani: Peruzzi ortağı; kaybedenlerin içinden"),
    # ── 12. VEBA: Floransa'nın rengi solar ───────────────────────────────────
    shot("p1_skyline", ("c1s11", -0.15), seed=3, **DAY, pan=240,
         ovl=P.ov(P.desat(("c1s11", "1348", -0.2), ("c1s11", "bırakmadı", 0.1), k_max=0.93, dark=0.55, tint="#59607A", tint_a=0.18),
                  P.tag("MART 1348 · YAZ BOYUNCA", 960, 215, ("c1s11", "Mart'ında", -0.2), size=48)),
         cam=("pan", "r", 240), tr=("yikama", 2.0), link="color", label="veba: renk solar"),
    # ── 13a. Boccaccio anlatır: sağlıklılar hastadan kaçar ───────────────────
    shot("c1_sokak", ("c1s12", -0.15), mode="day", perde=1,
         people=[dict(kind="halk", x0=1560, dir=-1, speed=300, h=232, seed=3, at=("c1s12", "sağlıklılar", -0.2), stil=dict(run=True)),
                 dict(kind="soylu_f", x0=1500, dir=-1, speed=280, h=226, seed=6, at=("c1s12", "sağlıklılar", 0.2), stil=dict(run=True)),
                 dict(kind="tuccar", x0=1620, dir=-1, speed=320, h=236, seed=9, at=("c1s12", "hastadan", -0.2), stil=dict(run=True)),
                 dict(kind="halk", x0=1700, dir=1, speed=0, h=226, seed=14, at=("c1s12", -0.3), action="idle", cf="#2A2018")],
         ovl=P.ov(P.desat(("c1s12", -0.2), ("c1s12", "sağlıklılar", 0.0), k_max=0.93, dark=0.55, tint="#59607A", tint_a=0.18, k_start=0.95),
                  P.plate("BOCCACCİO", 340, 205, ("c1s12", "Boccaccio", -0.1), role="ANLATIR")),
         cam=("truck", "r"), tr=("zoomthru", 0.6, dict(at=(1100, 460), at_b=(960, 520))), link="scale", label="Boccaccio: sağlıklılar kaçar"),
    # ── 13b. hasta yalnız: boş oda, pencere ışığı solar (beden yok) ──────────
    shot("p1_oda", ("c1s12", "hasta", -0.3), room="bos", variant="koln", path="in", **DAY, fade_at=("c1s12", "hasta", -0.1), fade_dur=3.4,
         actors=[dict(kind="halk", x=1020, y=806, h=270, action="idle", sil="#0E0806", seed=5, dir=1, rim_dir=1, hat="coif")], cam=("push",),   # SA2-K7: geniş kenarlı şapka yok
         ovl=P.desat(("c1s12", "hasta", -0.3), ("c1s12", "hasta", -0.2), k_max=0.93, dark=0.45, tint="#59607A", tint_a=0.18, k_start=0.95),
         tr=("candle", 0.8, dict(at=(960, 640), at_b=(1200, 560))), link="light", label="hasta yalnız"),
    # ── 13c. kapılar kapanır; sokak boş (aynı sokak → sert kesme) ─────────────
    shot("c1_sokak", ("c1s12", "evlerde", -0.4), mode="day", perde=1, door_at=("c1s12", "evlerde", -0.1), people=[],
         ovl=P.desat(("c1s12", "evlerde", -0.4), ("c1s12", "evlerde", -0.3), k_max=0.95, dark=0.7, tint="#59607A", tint_a=0.2, k_start=0.97),
         cam=("pan", "r"), tr="cut", link="audio", label="kapılar kapanır, sokak boş"),
    # ── 14a. Stefani, 12 yaşında ─────────────────────────────────────────────
    shot("c1_sokak", ("c1s13", -0.1), mode="day", perde=1,
         people=[dict(kind="cocuk", x0=1180, dir=1, speed=0, h=180, seed=5, at=("c1s13", -0.2), action="idle"),
                 dict(kind="halk", x0=1560, dir=-1, speed=70, h=226, seed=8, at=("c1s13", -0.2), cf="#2A2018")],
         ovl=P.ov(P.desat(("c1s13", -0.2), ("c1s13", 0.0), k_max=0.93, dark=0.5, tint="#59607A", tint_a=0.18, k_start=0.95),
                  P.plate("MARCHİONNE Dİ COPPO STEFANİ", 960, 205, ("c1s13", "Stefani", -0.1)),
                  P.count_up(1500, 520, ("c1s13", "on", -0.2), 12, dur=0.6, unit="YAŞINDA", size=170, bg=True, min_w=300, unit_size=40)),
         cam=("pull",), tr=("slide", 0.35, dict(dir="r")), link="dir", label="Stefani: on iki yaşında"),
    # ── 14b. yıllar sonra: kronik yazılır (hücre; oturan yazar) ──────────────
    shot("p1_oda", ("c1s13", "yıllar", -0.3), room="calisma", variant="hucre", **DAY, figure=None, lamp_day=0.6,
         actors=[dict(kind="tuccar", seed=19, x=946, y=823, h=280, action="write", seated=True, dir=1)],
         cams=[(("c1s13", "yıllar", -0.3), (1060, 30, 1.25)), (("c1s13", "ölülerin", -0.3), (1020, 60, 1.40))],
         ovl=P.tag("YILLAR SONRA", 960, 200, ("c1s13", "yıllar", -0.2), size=56),
         cam=("push",), tr=("candle", 0.6, dict(at=(960, 640), at_b=(1200, 560))), link="light", label="yıllar sonra: kronik"),
    # ── 14c. toplu çukurlar, katman katman toprak (beden yok; ilk karede okunur) ──
    shot("c1_toprak", ("c1s13", "ölülerin", -0.3), mode="day", perde=1, pit_at=("c1s13", "çukurlara", -0.25), layers_at=("c1s13", "üstlerinin", -0.15), layers_to=("c1s13", "örtüldüğünü", 0.3),
         ovl=P.tag("KATMAN KATMAN", 960, 200, ("c1s13", "katman", -0.1), size=54),
         cam=("tilt", "down", 140), tr=("yikama", 0.8), link="color", label="çukur, katman katman toprak"),
    # ── 15. ne düşündüğünü bilmiyoruz; ne gördüğünü yazdığını biliyoruz (nakarat = anlatım) ──
    shot("c1_yazi", ("c1s14", -0.1), mode="night", perde=1, q_at=("c1s14", "düşündüğünü", -0.3), q_out=("c1s14", "ne", 1, 0.3), w_at=("c1s14", "gördüğünü", -0.2), w_to=("c1s14", "biliyoruz", 0.4),
         # ENG-D "beyan ↔ gerçekleşen" kapısı (kurul tur 2): itme ölçülen hareketin yarısına ulaşmıyordu (içerik merkezde) → açılan geri çekiliş ("biliyoruz")
         cam=("pull",), tr=("slide", 0.6, dict(dir="u")), link="dir", label="bilmiyoruz → yazdığını biliyoruz"),
    # ── 16. 1378: bu kez öfke sokaktaydı (halk kadrosu; atlı yok; Medici sancağı yok) ──
    shot("p1_procession", ("c1s15", -0.1), dir="l", density=1.6, seed=4, speed=150.0, flag_ctx="ciompi",
         mix=dict(common=0.55, banner=0.2, guard=0.1, elder=0.15, rider=0.0, noble=0.0, page=0.0, cleric=0.0), mode="day", perde=1,
         ovl=P.tag("1378", 960, 200, ("c1s15", "1378'de", -0.1), size=64),
         cam=("truck", "r"), tr=("slide", 0.8, dict(dir="r")), link="dir", label="1378: öfke sokakta (halk)"),
    # ── 17. KURAYLA: Signoria'da isim kesesinden fiş çekilir — SALVESTRO gonfaloniere ──
    shot("p1_oda", ("c1s16", -0.15), room="salon", variant="signoria", **DAY, path="default",
         actors=[dict(kind="soylu", seed=24, x=1180, y=880, h=430, action="idle", dir=1, layer="front"),
                 dict(kind="soylu", seed=26, x=1560, y=880, h=430, action="point", at=("c1s16", "kurayla", -0.4), dir=-1, layer="front")],
         cams=[(("c1s16", -0.15), (1320, 40, 1.18)), (("c1s16", "kurayla", -0.3), (1360, 56, 1.30))],
         ovl=P.ov(P.tag("MAYIS 1378", 480, 200, ("c1s16", "Mayıs'ında", -0.2), size=52, out=("c1s16", "Salvestro", -0.5)),
                  P.plate("SALVESTRO DE' MEDİCİ", 600, 150, ("c1s16", "Salvestro", -0.3), role="MEDİCİ AİLESİNİN BAŞKA BİR KOLU", w=800),
                  K.kura(1000, 700, ("c1s16", -0.1), ("c1s16", "kurayla", -0.2), name="SALVESTRO", rise=210.0),
                  P.tag("KURAYLA", 1440, 300, ("c1s16", "kurayla", 0.2), size=56, dur=0.25),
                  P.tag("GONFALONİERE · ŞEHRİN BAŞI", 1100, 880, ("c1s16", "gonfaloniere", -0.2), size=44)),
         cam=("push",), tr="cut", link="audio", label="kurayla gonfaloniere: Salvestro"),
    # ── 18. yün işçilerinin loncası yoktu (21 kalkan TEMSİLÎ) ─────────────────
    shot("c1_lonca", ("c1s17", -0.1), mode="day", perde=1, rows_at=("c1s17", "Ama", 0.0), carder_at=("c1s17", "yün", -0.2), empty_at=("c1s17", "loncası", -0.15), mute_at=("c1s17", "sesi", -0.2),
         ovl=TEMSILI(("c1s17", "Floransa'yı", 0.0)),
         cam=("pan", "r"), tr=("carry", 0.95, dict(strip="banner", dir="r")), link="carry", label="21 lonca; yün işçisinin yeri boş"),
    # ── 19a. 22 Temmuz: Ciompi Palazzo Vecchio'yu alır (Komün zambağı/popolo haçı; atlı yok) ──
    shot("p1_sehir", ("c1s18", -0.1), scene="meydan", act="kalabalik", dir="l", flags="cross", riders=0, flag_ctx="ciompi", **DAY,
         ovl=P.ov(P.tag("22 TEMMUZ 1378", 470, 200, ("c1s18", "Temmuz'da", -0.1), size=56, out=("c1s18", "Palazzo", 0.9)),
                  anim.stamp_ovl("CİOMPİ", 1470, 420, ("c1s18", "Ciompi", 0.1), "squash", rot=-0.07, size=72, out=("c1s18", "ele", 0.2))),
         cam=("truck", "r"), tr=("slide", 0.7, dict(dir="r")), link="dir", label="Ciompi Palazzo Vecchio'yu ele geçirir"),
    # ── 19b. kule: bir yün tarayıcısı, Michele di Lando, gonfaloniere (ÇEKİLDİ yok) ──
    shot("p1_sehir", ("c1s18", "bir", -0.2), scene="skyline_dikey", **DAY, cam=("crane", "up", 300),
         ovl=P.plate("MİCHELE Dİ LANDO", 560, 640, ("c1s18", "Michele", -0.3), role="YÜN TARAYICISI → GONFALONİERE", w=820),
         tr=("zoomthru", 0.8, dict(at=(1000, 420), at_b=(960, 520))), link="scale", label="kule: Michele di Lando gonfaloniere"),
    # ── 20a. talepler OKUNUR — Signoria salonu (kurul tur 2 AN2-K3: 8,3 sn'lik, %60'ı boş belge kartı bölündü): Ciompi temsilcisi okur, başkanlık
    #        (Signoria) masanın ardında dinler; konuşma tomarında ilk talep GERÇEK HARFLERLE yazılır (dalgalı çizgi değil); kamera tomara iter.
    #        Aynı salon = Mayıs'taki kura sahnesi (aynı saray). Figür başlıkları dönem (kurul SA2-K7: geniş kenarlı "17. yy" şapkası yok). ──
    shot("p1_oda", ("c1s19", -0.1), room="salon", variant="signoria", **DAY, path="default",
         actors=[dict(kind="soylu", seed=24, x=1640, y=690, h=262, action="idle", dir=-1, layer="behind"),
                 dict(kind="soylu", seed=26, x=1900, y=690, h=262, action="idle", dir=-1, layer="behind", phase=0.4, hat="mazzocchio"),
                 dict(kind="halk", seed=35, x=900, y=880, h=415, action="idle", dir=1, layer="front", hat="coif"),
                 dict(kind="halk", seed=31, x=1150, y=880, h=430, action="talk", at=("c1s19", "Talepleri", -0.1), dir=1, layer="front", hat="woolcap")],
         cams=[(("c1s19", -0.1), (1380, 40, 1.16)), (("c1s19", "işçilere", -0.1), (1440, 72, 1.36))],
         ovl=P.ov(K.oda_bagli([(("c1s19", -0.1), (1380, 40, 1.16)), (("c1s19", "işçilere", -0.1), (1440, 72, 1.36))], (1380, 40, 1.16),
                              K.dilekce_tomar(770, 470, ("c1s19", "yazıldığına", -0.2), ("c1s19", "vergide", 0.1), "Vergide adalet", ("c1s19", "vergide", -0.1), w=600, size=46)),
                  P.tag("YAZILDIĞINA GÖRE", 1500, 880, ("c1s19", "yazıldığına", -0.1), size=40)),
         cam=("push",), tr=("zoomthru", 0.6, dict(at=(960, 150), at_b=(960, 520))), link="scale", label="talepler Signoria'da okunur"),
    # ── 20b. talepler belgesi ≈4 sn (yakın; kâğıt kesmede hazır, boş alan yok): ilk satır yazılmış, ikinci ve üçüncü sözcüğünde yazılır ──
    shot("p1_doc", ("c1s19", "işçilere", -0.06), title="CİOMPİ'NİN TALEPLERİ", w=1040, h=500, mode="day", perde=1, size=66, at=-1.0,
         lines=[("Vergide adalet", ("c1s19", "vergide", -0.2)), ("İşçilere lonca hakkı", ("c1s19", "işçilere", 0.0)), ("Kamu borcunun azaltılması", ("c1s19", "kamu", -0.2))],
         ovl=P.tag("YAZILDIĞINA GÖRE", 1500, 880, ("c1s19", "yazıldığına", -0.1), size=40),
         cam=("push",), tr="cut", link="audio", label="Ciompi'nin talepleri (belge)"),
    # ── 21a. bir buçuk asır sonra: Machiavelli (çalışma odası, raf; Medici siparişi) — HUD gizli (kurul tur 2 KA2-D2: 1378 değil, ≈1520);
    #        malzeme geçişi: tarih kitabının sayfası çevrilir, cümleler arası nefeste (place=after); ışık patlaması kalktı ──
    shot("p1_oda", ("c1s20", -0.8), room="calisma", variant="kutuphane", **DAY, figure=None, hud=False,
         actors=[dict(P.MACHIAVELLI, x=1366, y=823, h=280, action="write", seated=True, dir=1),
                 dict(kind="halk", seed=8, x=2500, y=880, h=430, sil="#241A14", dir=-1, rim_dir=-1, walk=(1940, 260), walk_at=("c1s20", "Machiavelli", 0.2), layer="front", hat="coif")],
         cams=[(("c1s20", -0.8), (1300, 20, 1.12)), (("c1s20", "Machiavelli", -0.2), (1500, 40, 1.22))],
         ovl=P.plate("MACHİAVELLİ", 760, 170, ("c1s20", "Machiavelli", -0.3), role="MEDİCİ SİPARİŞİYLE TARİH YAZAR", w=760),
         cam=("pan", "r"), tr=("sayfa", 0.8, dict(place="after")), link="material", label="Machiavelli: Medici siparişiyle tarih"),
    # ── 21b. adı belli olmayan isyancının ağzına koca bir konuşma: KURGU — KESMEDE İSYANCIYA YAKIN PLAN (kurul tur 2 AN2-Ö1 #46: eski ×1,15 sıçrama →
    #        ×1,64 ve konu değişir), "koydu"da geri çekilip yazan tarihçiyi açar (konuşmanın sahibi). Soru işareti ve tomar odaya bağlı (oda_bagli). HUD gizli. ──
    shot("p1_oda", ("c1s20", "adı", -0.2), room="calisma", variant="kutuphane", **DAY, figure=None, hud=False,
         actors=[dict(P.MACHIAVELLI, x=1366, y=823, h=280, action="write", seated=True, dir=1),
                 dict(kind="halk", seed=8, x=1940, y=880, h=430, action="talk", at=("c1s20", "konuşma", 0.0), sil="#241A14", dir=-1, rim_dir=-1, layer="front", hat="coif")],
         cams=[(("c1s20", "adı", -0.2), (1940, 70, 2.0)), (("c1s20", "ağzına", -0.3), (1925, 72, 2.06)), (("c1s20", "koydu", 0.2), (1650, 60, 1.40)),
               (("c1s21", "isyancının", 0.0), (1690, 70, 1.48))],
         ovl=P.ov(K.oda_bagli([(("c1s20", "adı", -0.2), (1940, 70, 2.0)), (("c1s20", "ağzına", -0.3), (1925, 72, 2.06)), (("c1s20", "koydu", 0.2), (1650, 60, 1.40)),
                               (("c1s21", "isyancının", 0.0), (1690, 70, 1.48))], (1650, 60, 1.40),
                              P.icon_at("question", 1370, 300, ("c1s20", "belli", -0.2), size=120, bob=5, out=("c1s20", "konuşma", 0.0)),
                              K2.tomar(950, 380, ("c1s20", "ağzına", -0.2), ("c1s20", "koydu", 0.3), w=390, dirn=1, lines=4)),
                  P.tag("KURGU · KONUŞMA TARİHÇİNİN", 960, 200, ("c1s21", "tarihçinin", 0.0), size=50, dur=0.3)),
         cam=("push",), tr="cut", link="cam", label="isyancının ağzına konuşma (kurgu)"),
    # ── 22. Ağustos sonu: loncaların milisleri isyanı ezdi (ağır; beden yok) ──
    shot("p1_procession", ("c1s22", -0.1), dir="l", density=1.3, seed=9, speed=150.0, flag_ctx="lonca",
         mix=dict(guard=0.6, banner=0.25, common=0.15, rider=0.0, noble=0.0, page=0.0), mode="day", perde=1,
         ovl=P.ov(P.dim(("c1s22", "milisleri", 0.0), ("c1s23", -0.0), alpha=0.5),
                  P.tag("AĞUSTOS SONU", 960, 200, ("c1s22", "Ağustos", -0.1), size=56, out=("c1s23", -0.1))),
         cam=("truck", "r", 170), tr=("yikama", 1.6), link="color", label="loncaların milisleri"),
    # ── 23. kısa ömürlü lonca kaldırıldı; yönetimden de dışlandılar (c1s17 armaları geri döner) ──
    shot("c1_lonca", ("c1s23", -0.15), mode="day", perde=1, rows_at=("c1s22", -0.6), carder_at=("c1s22", -0.6), new_at=("c1s22", -0.6), new_label="CİOMPİ LONCASI",
         remove_at=("c1s23", "kaldırıldı", -0.1), empty_at=("c1s23", "kaldırıldı", 1.0), out_at=("c1s23", "yönetimden", 0.0),
         ovl=P.ov(P.tag("KISA ÖMÜRLÜ LONCA KALDIRILDI", 960, 200, ("c1s23", "kaldırıldı", 0.2), size=48, out=("c1s23", "yönetimden", -0.2)),
                  P.tag("YÖNETİMDEN DE DIŞLANDILAR", 960, 200, ("c1s23", "yönetimden", 0.0), size=48),
                  TEMSILI(("c1s23", -0.15))),
         cam=("pull",), tr=("carry", 0.7, dict(strip="banner", dir="r")), link="carry", label="lonca kaldırıldı; dışlandılar"),
    # ── 24. Medici'nin bu kolu bir kademe altta; kır gelirleri ───────────────
    shot("c1_kademe", ("c1s24", -0.1), mode="day", perde=1, elite_at=("c1s24", "seçkinlerinin", -0.35), medici_at=("c1s24", "Medici'nin", -0.1), field_at=("c1s24", "kır", -0.6), income_at=("c1s24", "gelirleriyle", -0.3),
         ovl=TEMSILI(("c1s24", "seçkinlerinin", 0.0)),
         cam=("pan", "r"), tr=("slide", 0.35, dict(dir="r")), link="dir", label="bir kademe altta; kır gelirleri"),
    # ── 25. Giovanni di Bicci: babasının mütevazı mirasından küçük bir pay (ev; iki kardeş, sandık) ──
    shot("p1_oda", ("c1s25", -0.15), room="p1ofis", variant="ev", **DAY, figure=None,
         actors=[dict(G, x=760, y=880, h=460, action="idle", dir=1, layer="front"),
                 dict(kind="tuccar", seed=12, x=300, y=880, h=460, action="count", dir=1, layer="front")],
         cams=[(("c1s25", -0.15), (760, 40, 1.22)), (("c1s25", "mirasından", -0.3), (700, 56, 1.32))],
         ovl=P.ov(P.plate("GİOVANNİ Dİ BİCCİ", 1340, 180, ("c1s25", "Giovanni", -0.2), role="MEDİCİ'NİN BU KOLUNDAN", w=700),
                  P.coin_arc((560, 760), (900, 640), ("c1s25", "küçük", -0.3), n=3, lift=110, size=60),
                  P.tag("KÜÇÜK BİR PAY", 1340, 880, ("c1s25", "küçük", -0.1), size=46)),
         # ışık geçişi c0+c1'de yalnız iki ifşa anında (kurul tur 2 AN1-Y8): biri bu — "ASIL HİKÂYE: MEDİCİ", insan çapası Giovanni ilk kez görünür
         cam=("push",), tr=("light", 0.7, dict(at=(760, 560))), link="light", label="Giovanni di Bicci: küçük pay"),
    # ── 26a. Roma ────────────────────────────────────────────────────────────
    shot("p1_map", ("c1s26", -0.1), mode="day", perde=1, approx=False,
         # kurul tur 2 (SA2-K14 sınıfı): son karede "FLORANSA" etiketi üst çerçevede kesiliyordu → iniş daha az derin, iki şehir kadrajda kalır
         cams=[(("c1s26", -0.1), (11.9, 43.0, 3.3)), (("c1s26", "bankasında", 0.0), (12.15, 42.55, 4.3))],
         cities=[dict(lon=11.25, lat=43.77, name="FLORANSA", kind="capital", at=("c1s26", -0.0), size=32), dict(lon=12.50, lat=41.89, name="ROMA", kind="capital", at=("c1s26", "Roma'da", -0.2), size=36)],
         routes=[dict(pts=[(11.25, 43.77), (11.8, 42.9), (12.50, 41.89)], at=("c1s26", "Roma'da", -0.3), dur=1.6, width=7)],
         cam=("push", 0.07), tr=("zoomthru", 0.7, dict(at=(960, 500), at_b=(960, 520))), link="scale", label="Roma"),
    # ── 26b. Vieri di Cambio'nun bankası (Roma): Vieri çekilir, alacak ve borçlar Giovanni'ye geçer ──
    shot("p1_oda", ("c1s26", "çalıştı", -0.3), room="salon", variant="roma", **DAY, path="default",
         actors=[dict(G, x=1240, y=880, h=440, action="write", dir=1, layer="front"),
                 dict(VIERI, x=1560, y=880, h=450, action="talk", dir=-1, layer="front", walk=(2300, 160), walk_at=("c1s26", "çekilince", -0.1))],
         cams=[(("c1s26", "çalıştı", -0.3), (1380, 40, 1.22)), (("c1s26", "devraldı", -0.4), (1300, 56, 1.34))],
         ovl=P.ov(P.plate("VİERİ Dİ CAMBİO", 1280, 170, ("c1s26", "çalıştı", 0.0), role="GİOVANNİ'NİN PATRONU", w=640, out=("c1s26", "1390'ların", -0.3)),
                  P.tag("1390'LARIN BAŞI", 520, 200, ("c1s26", "1390'ların", -0.2), size=48),
                  P.tag("ALACAK + BORÇ", 960, 880, ("c1s26", "alacak", -0.1), size=46),
                  P.prop_arc("book", (1500, 640), (1150, 600), ("c1s26", "devraldı", -0.4), dur=0.8, size=130, lift=120, show_from=("c1s26", "alacak", -0.3)),
                  P.tag("DEVRALDI", 1460, 330, ("c1s26", "devraldı", 0.1), size=56, dur=0.25)),
         cam=("truck", "r"), tr="cut", link="audio", label="Vieri'nin bankası: devir"),
    # ── 27a. Piccarda Bueri'nin çeyizi: 1.500 florin — sikke KESMEDE tam görünür, dönerek (kurul tur 2 AN1-Y5/Y6: boş parşömende 0,9 sn'de
    #        sıfırdan solan "ölü açılış" yoktu; at=−1 → kesme anında tam boy, tam opak) ──
    shot("p1_coin", ("c1s27", -0.1), n=1, size=420, pos=(520, 560), mode="day", perde=1, cam=("push",), at=-1.0,
         ovl=P.ov(P.count_up(1290, 540, ("c1s27", "bin", -0.25), 1500, dur=1.1, unit="FLORİN", size=200),
                  P.icon_at("ring", 1630, 330, ("c1s27", "Piccarda", -0.1), size=170, glow=True, bob=6),
                  # "EVLİLİK ÇEYİZİ" etiketi kaldırıldı: "1.500"ün sıfırlarına biniyor ve güvenli alanı aşıyordu (kurul tur 2, SA1-Y2); üst levha aynı bilgiyi verir
                  P.tag("PİCCARDA BUERİ'NİN ÇEYİZİ", 960, 200, ("c1s27", "Piccarda", -0.15), size=50)),
         tr="cut", link="audio", label="1.500 florinlik çeyiz"),
    # ── 27b. ilk sermaye = bir evlilik sözleşmesi — HUD 1385 (YIL_AT; başkan kararı: DBI/de Roover, evlilik 1385). "İLK SERMAYE" damgası başlığın
    #        ("EVLİLİK SÖZLEŞMESİ") üstüne biniyordu → kâğıdın boş alt-sağına (yazı × yazı çakışması yok) ──
    shot("p1_doc", ("c1s27", "hanedanın", -0.3), title="EVLİLİK SÖZLEŞMESİ", lines=[("Piccarda Bueri", ("c1s27", "hanedanın", 0.0)), ("çeyiz · 1.500 florin", ("c1s27", "ilk", 0.0))], seal=True, seal_at=("c1s27", "sözleşmesiydi", -0.2), w=1000, h=640, mode="day", perde=1,
         ovl=P.ov(P.icon_at("ring", 880, 655, ("c1s27", "evlilik", -0.15), size=190, glow=True, bob=5),
                  anim.stamp_ovl("İLK SERMAYE", 1250, 545, ("c1s27", "sermayesi", 0.1), "bounce", rot=-0.08, size=62)),
         cam=("tilt", "down", 140), tr=("slide", 0.5, dict(dir="r")), link="dir", label="hanedanın ilk sermayesi: evlilik sözleşmesi"),
    # ── 28a. 1397: iş Roma'dan Floransa'ya taşınır ───────────────────────────
    shot("p1_map", ("c1s28", -0.1), mode="day", perde=1, approx=False,
         cams=[(("c1s28", -0.1), (12.0, 42.8, 4.0)), (("c1s28", "Floransa'ya", 0.0), (11.7, 43.2, 5.4))],
         cities=[dict(lon=12.50, lat=41.89, name="ROMA", kind="capital", at=("c1s28", -0.0), size=34), dict(lon=11.25, lat=43.77, name="FLORANSA", kind="capital", at=("c1s28", "Floransa'ya", -0.2), size=34)],
         routes=[dict(pts=[(12.50, 41.89), (11.8, 42.9), (11.25, 43.77)], at=("c1s28", "Roma'dan", -0.25), dur=2.0, width=8)],
         ovl=P.tag("1397", 960, 200, ("c1s28", "1397'de", -0.1), size=72),
         # ENG-D "beyan ↔ gerçekleşen" kapısı (kurul tur 2): harita kendi anahtar karelerinde Floransa'ya YAKLAŞIYOR (zum 4,0 → 5,4); "pull" beyanı TERS idi → push
         cam=("push",), tr=("yikama", 0.9), link="material", label="1397: Roma'dan Floransa'ya taşınma"),
    # ── 28b. Orsanmichele köşesi: levhada yalnız VIA PORTA ROSSA (teyit §3.5); köşeye iğne. Kurul tur 2: Orsanmichele kübik Gotik simge (SA2-K3);
    #        "sessiz cep" (AN1-Y4) → ikinci sürekli hareket: kese Via Porta Rossa boyunca köşeye yürür ("taşıdı … köşeye"), yayalar, ışık süpürmesi;
    #        kamera itmesi ≈%1,5/sn ──
    shot("c1_kose", ("c1s28", "Orsanmichele", -0.5), mode="day", perde=1, orsa_at=("c1s28", "Orsanmichele", -0.3), street1_at=("c1s28", "Porta", -0.2), street2_at=None,
         move_at=("c1s28", "Via", -0.2), pin_at=("c1s28", "köşeye", -0.35),
         cam=("push", 0.10), tr=("zoomthru", 0.8, dict(at=(1500, 300), at_b=(960, 600))), link="scale", label="Orsanmichele köşesi: iğne"),
    # ── 29–31. köşedeki banka: sermaye 10.000 florin → bir masa ve bir defter (geniş → yakın) ──
    shot("p1_oda", ("c1s29", -0.15), room="p1banka", **DAY,
         cams=[(("c1s29", -0.15), (1500, 20, 1.05)), (("c1s30", -0.1), (900, 40, 1.15)), (("c1s30", "masa", 0.0), (640, 70, 1.5)), (("c1s31", "belliydi", 0.0), (600, 80, 1.58))],
         ovl=P.ov(P.count_up(960, 400, ("c1s29", "on", -0.15), 10000, dur=1.1, unit="FLORİN", size=190, out=("c1s30", -0.0), bg=True),
                  P.tag("BİR MASA VE BİR DEFTER", 960, 200, ("c1s30", "masa", -0.2), size=52, out=("c1s31", 0.4)),
                  P.coin_arc((330, 780), (1000, 620), ("c1s31", "kazanmanın", -0.3), n=5, lift=140, size=64),
                  P.glint(960, 640, ("c1s31", "Para", -0.1), r=260, dur=1.0)),
         cam=("push",), tr=("zoomthru", 0.6, dict(at=(960, 520), at_b=(960, 520))), link="scale", label="köşede bir masa, bir defter"),
    # ── 32. Zor olan: Kilise'nin "faiz günahtır" dediği çağda huzurla kazanmak — KESMEDE MASAYA YAKIN PLAN (defter + florin; kurul tur 2 AN2-Ö1 #58:
    #       eski kesme ×1,01, −156 px "kamera atlıyor"du → ×1,55 ve konu nesne), sonra geri çekilip salonu, levhayı ve haçı açar ──
    shot("p1_oda", ("c1s32", -0.15), room="p1banka", **DAY,
         cams=[(("c1s32", -0.15), (470, 190, 2.45)), (("c1s32", "olan", 0.3), (485, 182, 2.36)), (("c1s32", "faiz", -0.3), (720, 110, 1.62)),
               (("c1s32", "kazanmaktı", 0.6), (1000, 30, 1.12))],
         ovl=P.ov(P.tablet_text("“FAİZ GÜNAHTIR”", 960, 270, ("c1s32", "faiz", -0.25), size=66, face="title_m", pad=60),
                  P.icon_at("cross", 1560, 420, ("c1s32", "Kilise'nin", -0.1), size=220, glow=True, bob=5),
                  P.glint(700, 700, ("c1s32", "huzurla", 0.0), r=220, dur=1.2),
                  P.coin_arc((330, 760), (900, 600), ("c1s32", "huzurla", 0.0), n=6, lift=160, size=70)),
         cam=("pull",), tr="cut", link="cam", label="faiz günahtır: huzurla kazanmak"),
]

# yol haritası çipleri (kurul PK2-K7): sol üst, sessiz — ALTIN · HESAP · VEBA · ÖFKE → ASIL HİKÂYE: MEDİCİ
P.with_ovl(SHOTS, P.roadmap([(("c1s1", 0.4), 0), (("c1s6", "hesap", -0.2), 1), (("c1s11", -0.1), 2), (("c1s15", -0.1), 3), (("c1s25", -0.1), 4)]))

# Kurul tur 2 (başkan kararları; KA1/KA2/SA2): 1338 artık c1s5 BAŞINDA (Villani levhası "ESKİ darphane yöneticisi" 1338 rakamıyla tutarlı; c1s6'daki
# ayrı 1338 adımı gereksizdi, birleşti) · evlilik sözleşmesi belgesi (27b, "hanedanın") 1385 (DBI: Piccarda Bueri ile evlilik 1385; de Roover: Ekim 1385),
# ardından c1s28'de 1397. Dante (c1s3) ve Machiavelli (c1s20–21) çekimlerinde HUD gizli (shot(hud=False)).
YIL_AT = [(("c1s5", -0.2), 1338), (("c1s11", "Veba", -0.1), 1348), (("c1s15", "1378'de", -0.1), 1378), (("c1s26", "1390'ların", -0.1), 1390),
          (("c1s27", "hanedanın", -0.3), 1385), (("c1s28", "1397'de", -0.1), 1397)]
