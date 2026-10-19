"""c6 — Lorenzo (1449–1478). Parça 3 AÇILIŞI (bölüm kartsız; Program ilk çekime «MEDİCİ — PARÇA III» bindirmesi ekler: ilk çekimin orta bandı boş).
Yönetmen kartı: yonetmen_c6.md · notlar: notlar_c6.md. Tüm çekimler cümle/sözcük çapalı (mutlak saniye yok).
İmza sekans: GIOSTRA (c6s20–c6s27): meydan → mızrak koşusu (hızlı yatay kayma) → madalyalar → sancak (temsil; asıl sancak kayıp) → yarım şiir → zaman şeridi → ışık soğur.
"""
from shots import shot
import cilt_medici as CM
import c6_kinds as K

L_ = K.look

SHOTS = [
    # ── V1: Valori'nin tarifi ─────────────────────────────────────────────────
    shot("skyline", ("c6s1", 0), seed=3, tod="day", cam=("pan", "r", 300), pan=300, kick="FLORANSA", label="Floransa (parça açılışı)"),
    shot("c6_valori", ("c6s1", "anlatır", 0.5), a_page=("c6s1", "anlatır", 0.5), a_med=("c6s2", "yüzü", 0.2), a_gl=("c6s2", "vakarlıydı", -0.3),
         l1=("Doğa, görünüşte ona üvey ana;", ("c6s1", "doğa,", 0.3)), l2=("zihinde şefkatli bir ana.", ("c6s1", "zihne", -0.1)),
         l3=("Yüzü güzel sayılmazdı,", ("c6s2", "yüzü", 0.0)), l4=("ama saygı uyandıracak kadar vakarlıydı.", ("c6s2", "ama", -0.1)),
         cam=[(("c6s1", "anlatır", 0.5), L_(780, 520, 1.08)), (("c6s1", "zihne", 0.0), L_(800, 520, 1.1)), (("c6s2", "yüzü", 0.0), L_(990, 520, 1.0)),
              (("c6s2", "ama", 0.0), L_(1100, 520, 1.03)), (("c6s2", "vakarlıydı", 0.3), L_(1200, 500, 1.1)), (("c6s3", -0.2), L_(1340, 500, 1.18))],
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", longtake=True, label="Valori sayfası, Lorenzo madalyası"),
    shot("c6_tarif", ("c6s3", -0.15), a_head=("c6s3", -0.1), a_nose=("c6s3", "basık", -0.1), a_chin=("c6s3", "öne", -0.1), a_eye=("c6s3", "zayıf", -0.1), a_smell=("c6s4", "koku", -0.3),
         cam=[(("c6s3", -0.15), L_(900, 540, 1.0)), (("c6s3", "zayıf", -0.2), L_(1000, 480, 1.1)), (("c6s4", -0.2), L_(1060, 560, 1.0)), (("c6s5", -0.4), L_(1120, 560, 1.07))],
         tr=("slide", 0.9, dict(dir="r")), link="dir", longtake=True, label="ansiklopedi tarifi; koku göstergesi"),
    # ── V1 sonu: defter / şiir ────────────────────────────────────────────────
    shot("c6_defter_siir", ("c6s5", -0.1), a_open=("c6s5", -0.1), a_led=("c6s5", "defter", -0.15), a_move=("c6s5", "torunu", -0.35), a_verse=("c6s5", "şiir", -0.3), a_stamp=("c6s5", "yazdı", 0.15),
         cam=[(("c6s5", -0.1), L_(700, 520, 1.16)), (("c6s5", "tutardı", 0.2), L_(760, 520, 1.16)), (("c6s5", "torunu", -0.3), L_(1000, 520, 1.1)), (("c6s6", -0.3), L_(1230, 520, 1.12))],
         tr=("sayfa", 0.8), link="material", label="defter → şiir (büyükbaba/torun)"),
    # ── V2: Aralık 1469 ───────────────────────────────────────────────────────
    shot("c6_aile", ("c6s6", -0.1), a_open=("c6s6", -0.1), a_date=("c6s6", "2", -0.1), a_dead=("c6s6", "öldü;", -0.3), a_thread=("c6s6", "günler", -0.1), a_lor=("c6s6", "yirmi", -0.2), a_age=("c6s6", "yirmi", 0.0),
         cam=[(("c6s6", -0.1), L_(960, 520, 1.0)), (("c6s6", "öldü;", 0.0), L_(740, 520, 1.12)), (("c6s6", "yirmi", -0.3), L_(1180, 520, 1.1)), (("c6s6", "şehrin", -0.4), L_(1300, 520, 1.14))],
         tr=("sayfa", 0.8), link="material", label="Piero öldü; ağırlık Lorenzo'ya"),
    shot("c6_yuk", ("c6s6", "şehrin", -0.4), a_move=("c6s6", "şehrin", -0.2), a_city=("c6s6", "şehrin", 0.0), a_state=("c6s6", "devletin", 0.0),
         cam=("crane", "up", 90), tr=("slide", 0.8, dict(dir="r")), link="dir", label="şehrin ve devletin yükü (ölçek: madalya → şehir)"),
    # ── V2 devam: Ricordi gerekçesi ───────────────────────────────────────────
    shot("doc", ("c6s7", -0.15), title="RİCORDİ", lines=[("dostlarını ve servetini korumak için", ("c6s7", "dostlarını", -0.15))], w=1180, h=700,
         caption="Ricordi'ye göre · çeviri bize ait", hl=(-420, 20, 640), hl_at=("c6s7", "korumak", 0.0),
         cam=("push", 0.07), tr=("light", 0.9, dict(at=(960, 600))), link="light", label="hatıra defteri: Ricordi (çeviri bize ait)"),
    shot("c6_terazi", ("c6s7", "çünkü", -0.3), a_open=("c6s7", "çünkü", -0.3), a_gold=("c6s7", "çünkü", 0.0), a_state=("c6s7", "devletsiz", -0.1), a_shake=("c6s7", "yaşamak", 0.0),
         cam=("push", 0.06), tr=("zoomthru", 0.8, dict(at=(960, 520), at_b=(960, 520))), link="scale", label="servet kefesi; devletsiz zengin"),
    shot("c6_ayna", ("c6s8", -0.1), a_open=("c6s8", -0.1), a_reluct=("c6s8", "İsteksiz", 0.0), a_age=("c6s8", "yaşını", -0.1), a_danger=("c6s8", "tehlikeyi", -0.1), a_self=("c6s8", "yine", -0.1),
         cam=[(("c6s8", -0.1), L_(900, 520, 1.0)), (("c6s8", "ama", -0.2), L_(1000, 520, 1.05)), (("c6s9", -0.4), L_(1180, 520, 1.12))],
         tr=("sayfa", 0.8), link="material", label="gerekçe; ama anlatan yine kendisi (ayna)"),
    # ── V3: ailenin kadınları ─────────────────────────────────────────────────
    shot("c6_lucrezia", ("c6s9", -0.1), a_open=("c6s9", -0.1), a_dua=("c6s9", "dua", -0.1), a_bes=("c6s9", "beş", -0.1), a_pulci=("c6s9", "Pulci'nin", -0.1), a_morg=("c6s9", "Morgante'ye", -0.1),
         cam=[(("c6s9", -0.1), L_(960, 520, 1.0)), (("c6s9", "beş", 0.0), L_(1000, 520, 1.06)), (("c6s9", "Morgante'ye", 0.0), L_(980, 520, 1.1))],
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Lucrezia Tornabuoni, şair"),
    shot("map", ("c6s10", -0.1), view=(11.9, 42.9, 5.2), kick="1467 BAHARI", date=("1467", ("c6s10", "1467", 0.0)),
         cities=[dict(lon=12.4964, lat=41.9028, name="ROMA", kind="capital", at=("c6s10", "Roma'da", -0.2), size=40, color="#B33620", side="r"),
                 dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c6s10", "Piero'ya", -0.6), size=40, color="#233C8C", side="l")],
         routes=[dict(pts=[(12.4964, 41.9028), (12.1, 42.6), (11.7, 43.3), (11.2558, 43.7696)], at=("c6s10", "üç", -0.2), dur=2.2, color="#A8321E", width=7.0, dash=(18, 12))],
         icons_=[dict(kind="scroll", route=[(12.4964, 41.9028), (12.1, 42.6), (11.7, 43.3), (11.2558, 43.7696)], at=("c6s10", "üç", -0.3), move_at=("c6s10", "üç", -0.2), move_dur=2.0, size=76, metal="gold"),
                 dict(kind="scroll", route=[(12.4964, 41.9028), (12.1, 42.6), (11.7, 43.3), (11.2558, 43.7696)], at=("c6s10", "mektup", -0.3), move_at=("c6s10", "mektup", -0.2), move_dur=2.0, size=76, metal="gold"),
                 dict(kind="scroll", route=[(12.4964, 41.9028), (12.1, 42.6), (11.7, 43.3), (11.2558, 43.7696)], at=("c6s10", "yazdı.", -0.3), move_at=("c6s10", "yazdı.", -0.2), move_dur=2.0, size=76, metal="gold")],
         cam=("push", 0.05), tr=("zoomthru", 0.9, dict(at=(960, 540), at_b=(960, 540))), link="scale", label="1467: Roma → Piero'ya üç mektup"),
    shot("c6_mektup", ("c6s11", -0.1), a_open=("c6s11", -0.1), a_unfold=("c6s11", "28", -0.1), a_lines=("c6s11", "mektupta", 0.0),
         tags=[("UZUN BOYLU", ("c6s11", "uzun", -0.1)), ("NARİN", ("c6s11", "narin,", -0.1)), ("AÇIK TENLİ", ("c6s11", "açık", -0.1)), ("BOL SAÇLI", ("c6s11", "bol", -0.1)), ("YÜZÜ HOŞ", ("c6s11", "hoş", -0.2))],
         cam=[(("c6s11", -0.1), L_(960, 540, 1.0)), (("c6s11", "mektupta", 0.0), L_(1000, 520, 1.06)), (("c6s12", -0.4), L_(1060, 520, 1.1))],
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="28 Mart tarihli ilk mektup"),
    shot("c6_ledger", ("c6s12", -0.1), title_l="RİCORDİ", title_r="EVLİLİK", head="",
         left=[dict(text="Clarice'yi aldım", at=("c6s12", "Clarice'yi", -0.1), strike=("c6s12", "ya", -0.1)), dict(text="ya da bana verildi", at=("c6s12", "ya", 0.0), hl=("c6s12", "verildi.", 0.2))],
         stampt=("○ TEK KAYNAK", 1500, 190, ("c6s12", "aktarılır:", 0.0), 38), focus=(500, 330),
         cam=("push", 0.07), tr=("sayfa", 0.8), link="material", label="defter kaydı: aldım ya da bana verildi (mizah: evlilik pazarı)"),
    shot("procession", ("c6s13", -0.1), dir="r", density=1.15, mix=dict(rider=0.22, noble=0.22, page=0.16, banner=0.22, guard=0.04, elder=0.06, cleric=0.04, common=0.04), pan=("r", 760), speed=110.0, seed=5,
         kick="4 HAZİRAN 1469", caption="düğün şenlikleri", cam=("pan", "r", 160), tr=("slide", 0.9, dict(dir="r")), link="dir", label="düğün şenlikleri (alay soldan sağa)"),
    shot("oda", ("c6s14", -0.1), room="salon", variant="medici", tod="day", kick="1479",
         actors=[dict(kind="soylu_f", x=1430, y=806, h=272, action="point", sil=True, layer="front", at=("c6s14", "evden", -0.4), seed=4, dir=1),
                 dict(kind="banker", x=1690, y=812, h=270, action="idle", sil=True, layer="front", walk=(2480, 85), walk_at=("c6s14", "evden", 0.0), fade_x=(2150, 2420), prop="book", seed=6, dir=1),
                 dict(kind="cocuk", x=1160, y=806, h=186, action="idle", sil=True, layer="front", seed=8, dir=1),
                 dict(kind="cocuk", x=1250, y=812, h=176, action="idle", sil=True, layer="front", seed=9, dir=1)],
         cams=[(("c6s14", -0.1), (1250, 0, 1.0)), (("c6s14", "evden", -0.2), (1560, 10, 1.25)), (("c6s14", "ikna", 0.0), (1900, 20, 1.2))],
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Clarice, Poliziano'yu evden çıkarır (siluet)"),
    shot("black", ("c6s15", -0.1), text="son", cam=("push", 0.05), label="x"),
]
