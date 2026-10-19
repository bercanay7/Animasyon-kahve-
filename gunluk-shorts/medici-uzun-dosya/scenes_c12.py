"""c12 — Dük (1537–1574). PARÇA 6 AÇILIŞI (bölüm kartsız; Program ilk çekime «MEDİCİ — PARÇA VI — DÜK VE İKİ KRALİÇE» bindirmesini 1,2–4,8 sn ekler: ilk çekimin orta bandında YAZI yok).
Yönetmen kartı: yonetmen_c12.md · notlar: notlar_c12.md. Tüm çekimler cümle/sözcük çapalı (mutlak saniye yok): gerçek ElevenLabs sesi gelince zamanlar çapalardan yeniden hizalanır.
Renk anahtarı: devlet soğuğu — kül/umber duvar + soluk altın + devlet kızılı (mühür); 1562 gece (kor mum + şarap/lacivert); Lepanto lacivert-altın.
İmza sekans: «Dük makinesi» (c12s11–c12s15): 13 makam iğnesi dağınıktır → tek çatıya toplanır (plan) → Uffizi kendini kurar (build) → Vasari Koridoru'nda kesintisiz kayma (plan → pano corridor).
Sözleşme: rivayet/anekdot = gravür (c12s23); belge/olgu = renk. 1562: yalnız tarih, mum ve sessizlik (şiddet/ceset/iskelet yok; ceket yalnız bir giysi).
Mizah: YALNIZ üç ayrı 29 (takvim), «ofisler» (Uffizi), ünvan zinciri (fatura). KAPALI: Lorenzino, Siena, 1562, Michelangelo'nun cenazesi, Lepanto, ölüm.
"""
from shots import shot
import cilt_medici as CM
import p6_lib as L
import c12_kinds as K

look = L.look
ov = L.ov

# ── ortak parametre kısayolları
D = dict(perde=3)

SHOTS = [
    # ══ V1 · KENTİN BAŞI (s1–s4) ═══════════════════════════════════════════════════════════
    # 1 · Floransa alacakaranlıkta (parça açılışı: orta bant boş); «öldürmüş» anında ışık kısılır (cinayet gösterilmez)
    shot("p6_skyline", ("c12s1", 0), seed=3, tod="dusk", mode="day", pan=300, cam=("pan", "r", 300), **D,
         ovl=ov(L.dim(("c12s1", "öldürmüş,", -0.2), ("c12s1", "yerine", 0.0), alpha=0.42, dur=0.9),
                L.date_plate("OCAK 1537", ("c12s1", "Ocak", 0.15)),
                L.tag("SENATO", 1420, 200, ("c12s1", "Senato", -0.05), out=("c12s1", "Medici'nin", 0.0))),
         label="Floransa alacakaranlık (parça açılışı)"),
    # 2 · Medici'nin yan kolundan 17 yaşındaki Cosimo: ağaç — ana gövde (kalkan), yan kol uzar, ucunda madalya açılır
    shot("c12_dal", ("c12s1", "yerine", 0.0), grow_at=("c12s1", "yerine", 0.0), shield_at=("c12s1", "Medici'nin", -0.2), branch_at=("c12s1", "yan", -0.25), bud_at=("c12s1", "kolundan", 0.1), medal_at=("c12s1", "Cosimo'yu", -0.4),
         mode="day", cam=("push", 0.05), **D,
         ovl=ov(L.tag("MEDİCİ", 620, 880, ("c12s1", "Medici'nin", -0.1), size=44, w=380), L.tag("YAN KOL", 1010, 800, ("c12s1", "yan", -0.1), size=40, w=380),
                L.count_up(1630, 260, ("c12s1", "17", -0.1), 17, dur=0.9, unit="YAŞINDA", size=150)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Medici ağacı: yan kol → Cosimo (17)"),
    # 3 · Senato koşulu yazıya geçirdi: belge
    shot("p6_doc", ("c12s2", -0.2), title="SENATO KARARI", date="10 OCAK 1537", w=1180, h=620, seal=True, seal_at=("c12s2", "geçirdi:", 0.1), caption="Treccani (DBI) · çeviri bize ait",
         lines=[("non avesse il titolo di duca,", ("c12s2", "Ertesi", 0.15)), ("ma solo «capo e primario della città»", ("c12s2", "Senato", 0.0))],
         mode="day", cam=("push", 0.07), **D,
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="Senato kararı (IT özgün)"),
    # 4 · dük olmayacak; yalnızca «kentin başı ve birincisi»
    shot("c12_unvan", ("c12s2", "dük", -0.4), mode="day", **D,
         plates=[dict(x=520, main="DÜK", at=("c12s2", "dük", -0.1), strike=("c12s2", "olmayacak,", -0.1), w=400),
                 dict(x=1370, main="KENTİN BAŞI VE BİRİNCİSİ", sub="capo e primario della città", at=("c12s2", "yalnızca", 0.0), w=980)],
         cam=[(("c12s2", "dük", -0.4), look(860, 430, 1.12)), (("c12s2", "yalnızca", 0.2), look(1180, 430, 1.0)), (("c12s3", -0.4), look(1320, 440, 1.16))],
         ovl=L.date_plate("10 OCAK 1537", ("c12s2", "dük", 0.0)),
         tr=("carry", 0.9, dict(strip="ink", dir="r")), link="carry", label="DÜK ✗ → kentin başı ve birincisi"),
    # 5 · çağıran soylular: yönetilebilir biri (kukla ipleri = YORUM)
    shot("p6_oda", ("c12s3", -0.2), room="salon", variant="medici", path="sweep_r", tod="dusk", mode="day", cam=("push", 0.04), **D,
         ovl=ov(L.tag("SOYLULAR", 520, 210, ("c12s3", "soylular", 0.0), out=("c12s3", "istemişti;", 0.2)),
                L.strings_down([760, 1010, 1260, 1510], -40, (1330, 690), ("c12s3", "yönetilebilir", -0.15), out=("c12s3", "Cosimo", -0.1)),
                L.stamp("MUHTEMELEN", 1500, 330, ("c12s3", "muhtemelen", 0.1), size=46, rot=-0.07, out=("c12s3", "Cosimo", -0.1)),
                L.label("YÖNETİLEBİLİR", 1330, 850, ("c12s3", "yönetilebilir", -0.1), size=44, face="cap_i", out=("c12s3", "Cosimo", -0.1))),
         tr=("light", 0.9, dict(at=(1330, 690))), link="light", label="soylular ve kukla ipleri (YORUM)"),
    # 6 · Mugello'da yetişmiş, şehirde tanınmayan çocuk: kalabalık onu görmeden akar
    shot("p6_sehir", ("c12s3", "Cosimo", -0.25), scene="sokak", tod="day", mode="day", cam=("push", 0.05), **D, actors=[dict(kind="cocuk", x0=760, y=822, h=210, dir=1, speed=64, seed=5)],
         cams=[(("c12s3", "Cosimo", -0.25), (900, 40, 1.0)), (("c12s4", -0.3), (1480, 44, 1.12))],
         ovl=ov(L.tag("MUGELLO", 440, 230, ("c12s3", "Mugello'da", -0.1), size=40, out=("c12s3", "şehirde", 0.4)),
                L.tag("ŞEHİRDE TANINMAYAN", 1300, 230, ("c12s3", "tanınmayan", -0.5), size=36, w=640)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Mugello'dan gelen çocuk, kalabalık görmez"),
    # 7 · Montemurlo: aceleyle toplanmış sürgün ordusu yenilir (alay; şiddet yok)
    shot("p6_procession", ("c12s4", -0.15), dir="r", density=1.25, mix=dict(guard=0.30, banner=0.25, rider=0.25, common=0.12, page=0.08), speed=120.0, tod="day", mode="day", cam=("pan", "r", 260), **D,
         ovl=ov(L.date_plate("AĞUSTOS 1537", ("c12s4", "Ağustos", 0.0)), L.tag("MONTEMURLO", 1450, 215, ("c12s4", "Montemurlo'da,", -0.1), size=48, w=620),
                L.tag("SÜRGÜN ORDUSU", 480, 215, ("c12s4", "sürgün", -0.1), size=40, w=560, out=("c12s4", "yendi;", 0.3)),
                L.stamp("YENDİ", 1000, 790, ("c12s4", "yendi;", 0.0), size=64, rot=-0.07, out=("c12s4", "Treccani", 0.0))),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Montemurlo: sürgün ordusu yenilir"),
    # 8 · Treccani bu zaferi cumhuriyetçi restorasyon tehdidinin sonu sayar
    shot("p6_quote", ("c12s4", "İtalyan", -0.25), text="Cumhuriyetçi restorasyon tehdidinin sonu", who="TRECCANI", src="İtalyan Ansiklopedisi", mark=False, size=74, wrap=1250, at=("c12s4", "İtalyan", -0.1),
         mode="day", cam=("push", 0.06), **D, ovl=L.stamp("SON", 1560, 330, ("c12s4", "sonu", -0.1), size=72, rot=-0.10),
         tr=("yikama", 0.9), link="material", label="Treccani: tehdidin sonu"),

    # ══ V2 · ELEONORA, ÜÇ AYRI 29 (s5–s8) ═══════════════════════════════════════════════════
    # 9 · 1539: Cosimo ve Eleonora
    shot("p6_medals", ("c12s5", -0.15), items=[dict(key="m_cosimo1", name="COSIMO", at=("c12s5", "Cosimo,", -0.2)), dict(key="m_eleonora", name="ELEONORA", role="DI TOLEDO · İSPANYOL SOYLUSU", at=("c12s5", "Eleonora", -0.3))],
         size=470, mode="day", cam=("push", 0.07), **D,
         ovl=ov(L.date_plate("1539", ("c12s5", "1539'da", 0.0)), L.icon_at("ring", 960, 470, ("c12s5", "evlendi.", -0.1), size=190, glow=True, bob=5)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Cosimo ve Eleonora (1539)"),
    # 10 · 29 MART: Napoli'de sözleşme, vekâleten
    shot("c12_takvim", ("c12s6", -0.15), mode="day", **D,
         leaves=[dict(month="MART", tag="NAPOLİ", sub="sözleşme · vekâleten", at=("c12s6", "29", -0.1), x=560, y=470, rot=-0.05)],
         cam=[(("c12s6", -0.15), look(700, 520, 1.12)), (("c12s6", "vekâleten", 0.0), look(620, 520, 1.25))],
         tr=("sayfa", 0.9), link="material", label="29 Mart: Napoli, vekâleten"),
    # 11 · 29 Haziran: Eleonora Floransa'ya girer (harita: Napoli → Floransa)
    shot("p6_map", ("c12s6", "Eleonora", -0.2), view=(12.0, 42.6, 5.6), mode="day", cam=("push", 0.07), **D,
         cities=[dict(lon=14.2681, lat=40.8518, name="NAPOLİ", kind="capital", at=("c12s6", "Eleonora", -0.15), size=34, color="#B33620", side="r"),
                 dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c12s6", "Haziran'da", 0.0), size=34, color="#233C8C", side="l")],
         routes=[dict(pts=[(14.2681, 40.8518), (12.7, 41.9), (10.6, 42.9), (10.4, 43.55), (11.2558, 43.7696)], at=("c12s6", "Eleonora", -0.1), dur=2.4, color="#A8321E", width=7.0, dash=(18, 12))],
         icons_=[dict(kind="galley", route=[(14.2681, 40.8518), (12.7, 41.9), (10.6, 42.9), (10.4, 43.55), (11.2558, 43.7696)], at=("c12s6", "Eleonora", -0.1), move_at=("c12s6", "Eleonora", -0.1), move_dur=2.4, size=80, metal="gold")],
         ovl=L.date_plate("29 HAZİRAN", ("c12s6", "Haziran'da", 0.0)),
         tr=("zoomthru", 0.9, dict(at=(960, 540), at_b=(960, 540))), link="scale", label="29 Haziran: Napoli → Floransa"),
    # 12 · 29 Temmuz: resmî düğün (takvimde üç yaprak)
    shot("c12_takvim", ("c12s6", "resmî", -0.3), mode="day", **D,
         leaves=[dict(month="MART", tag="NAPOLİ", sub="sözleşme · vekâleten", at=("c12s6", "29", -0.1), x=560, y=470, rot=-0.05),
                 dict(month="HAZİRAN", tag="FLORANSA", sub="girişi", at=("c12s6", "29", 1, -0.1), x=960, y=470, rot=0.03),
                 dict(month="TEMMUZ", tag="RESMÎ DÜĞÜN", at=("c12s6", "29", 2, -0.1), x=1360, y=470, rot=-0.025)],
         cam=[(("c12s6", "resmî", -0.3), look(1150, 520, 1.25)), (("c12s6", "yapıldı.", 0.2), look(1100, 520, 1.1))],
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="29 Temmuz: resmî düğün"),
    # 13 · mizah: üç ayrı 29'a ihtiyaç duymuştu (yapraklar sırayla zıplar; sahne geri çekilir, Cosimo siluet)
    shot("c12_takvim", ("c12s7", -0.1), mode="day", **D,
         leaves=[dict(month="MART", tag="NAPOLİ", sub="sözleşme · vekâleten", at=("c12s6", "29", -0.1), x=560, y=470, rot=-0.05),
                 dict(month="HAZİRAN", tag="FLORANSA", sub="girişi", at=("c12s6", "29", 1, -0.1), x=960, y=470, rot=0.03),
                 dict(month="TEMMUZ", tag="RESMÎ DÜĞÜN", at=("c12s6", "29", 2, -0.1), x=1360, y=470, rot=-0.025)],
         jumps=[("c12s7", "üç", 0.0), ("c12s7", "ayrı", 0.0), ("c12s7", "29'a", 0.0)],
         actor=dict(kind="tuccar", x=1700, y=720, h=430, at=("c12s7", "Cosimo", -0.2), action="point", seed=8, p=dict(target=(-260, -80))),
         cam=[(("c12s7", -0.1), look(1100, 520, 1.1)), (("c12s7", "29'a", 0.2), look(1020, 520, 0.9)), (("c12s8", -0.3), look(1000, 520, 0.84))],
         ovl=L.stamp("ÜÇ AYRI 29", 960, 140, ("c12s7", "29'a", 0.1), size=62, rot=-0.04),
         tr=None, link="cam", label="üç ayrı 29 (mizah)"),
    # 14 · Pitti Sarayı'nı Eleonora satın aldı
    shot("p6_oda", ("c12s8", -0.15), room="salon", variant="pitti", path="sweep_r", tod="dusk", mode="day", cam=("push", 0.04), **D,
         ovl=ov(L.tag("PİTTİ SARAYI", 960, 215, ("c12s8", "Pitti", -0.1), size=52, w=820),
                L.tag("ELEONORA", 560, 800, ("c12s8", "Eleonora", -0.1), size=42, w=520),
                L.icon_move("coinbag", (700, 760), (1320, 700), ("c12s8", "satın", -0.1), dur=0.9, size=150, arc=70)),
         tr=("light", 0.9, dict(at=(960, 540))), link="light", label="Pitti Sarayı: Eleonora satın aldı"),

    # ══ V3 · DEVLET VE SAVAŞ (s9–s10; mizah KAPALI) ═════════════════════════════════════════
    # 15 · Venedik'te Lorenzino pusuya düşürülüp öldürülür (şiddet gösterilmez: ışık kısılır, pigment yıkama)
    shot("p6_liman", ("c12s9", -0.15), variant="generic", name="VENEDİK", year=None, tod="dusk", mode="day", cam=("pan", "r", 160), **D,
         ovl=ov(L.date_plate("26 ŞUBAT 1548", ("c12s9", "Şubat", -0.2)),
                L.dim(("c12s9", "pusuya", -0.1), None, alpha=0.5, dur=1.2),
                L.ink_wash(("c12s9", "öldürüldü;", -0.1), dur=1.8, alpha=0.30, out=("c12s9", "emri", 0.0))),
         tr=("dip", 0.9), link="color", label="Venedik 1548 (ağır; şiddet yok)"),
    # 16 · emri Cosimo'nun verdiği uzun süre kabul edildi; yeni bir çalışma kuşku düşürüyor
    shot("p6_doc", ("c12s9", "emri", -0.2), title="LORENZİNO · 1548", w=1160, h=640, mode="day", cam=("push", 0.06), **D,
         lines=[("emri Cosimo'nun verdiği", ("c12s9", "emri", -0.1)), ("uzun süre kabul edildi", ("c12s9", "uzun", -0.1))],
         ovl=ov(L.stamp("KABUL EDİLDİ", 1350, 300, ("c12s9", "kabul", -0.05), size=54, rot=-0.07),
                L.stamp("YENİ BİR ÇALIŞMA: KUŞKU", 960, 840, ("c12s9", "kuşku", -0.1), size=48, rot=0.03),
                L.icon_at("question", 1560, 620, ("c12s9", "kuşku", 0.0), size=210, glow=True)),
         tr=("sayfa", 0.9), link="material", label="emri verdiği kabul; yeni çalışma: kuşku"),
    # 17 · Siena on beş ay direndi, açlıktan teslim oldu
    shot("p6_map", ("c12s10", -0.15), view=(11.28, 43.42, 11.0), mode="day", cam=("push", 0.07), **D,
         cities=[dict(lon=11.3308, lat=43.3188, name="SİYENA", kind="town", at=("c12s10", 0.0), size=36, color="#B33620", side="r"),
                 dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c12s10", 0.0), size=30, color="#233C8C", side="r")],
         ovl=ov(L.count_up(1500, 330, ("c12s10", "on", -0.1), 15, dur=1.2, unit="AY", size=170),
                L.desat(("c12s10", "açlıktan", -0.2), ("c12s10", "oldu;", 0.4), k_max=0.8, dark=0.35)),
         tr=("zoomthru", 0.9, dict(at=(960, 540), at_b=(960, 540))), link="scale", label="Siena: on beş ay"),
    # 18 · 1557: II. Felipe şehri Cosimo'ya bıraktı (anahtar uçar)
    shot("p6_medals", ("c12s10", "1557'de", -0.25), items=[dict(key="felipe2", name="II. FELİPE", at=("c12s10", "II.", -0.3)), dict(key="m_cosimo1_o", name="COSIMO", at=("c12s10", "Cosimo'ya", -0.35))],
         size=470, mode="day", cam=("push", 0.07), **D,
         ovl=ov(L.date_plate("1557", ("c12s10", "1557'de", 0.0)),
                L.icon_move("keys", (620, 520), (1300, 520), ("c12s10", "şehri", 0.0), dur=1.3, size=170, arc=90)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="II. Felipe → Cosimo: şehrin anahtarı"),

    # ══ V4 · UFFIZI — «DÜK MAKİNESİ» (s11–s15) ═══════════════════════════════════════════════
    # 19 · 13 makam dağınık → tek çatı (plan)
    shot("c12_plan", ("c12s11", -0.2), pins_at=("c12s11", "Floransa'ya", 0.0), pins_dt=0.11, fly_at=("c12s11", "tek", -0.1), u_fill_at=("c12s11", "altında", -0.2),
         tabela_at=("c12s11", "toplayacaktı.", -0.5), lab_pv=("c12s11", "Cosimo,", 0.0), lab_uf=("c12s11", "toplayacaktı.", -0.3), mode="day", **D,
         cam=[(("c12s11", -0.2), look(690, 500, 1.55)), (("c12s11", "Floransa'ya", 0.0), look(960, 540, 1.0)), (("c12s11", "tek", 0.0), look(960, 520, 1.1)), (("c12s12", -0.3), look(960, 590, 1.5))],
         ovl=ov(L.tag("VASARI", 1560, 210, ("c12s11", "Vasari'den", 0.0), size=44, w=420, out=("c12s11", "Floransa'ya", 0.3)),
                L.count_up(1560, 320, ("c12s11", "13", -0.12), 13, dur=0.9, unit="İDARİ MAKAM", size=130, out=("c12s11", "toplayacaktı.", 0.0))),
         tr=("light", 0.9, dict(at=(960, 540))), link="light", label="13 makam: dağınık → tek çatı (plan)"),
    # 20 · Uffizi kendini kurar (uzun plan): «yani ofisler»; doğduğunda bir memur binası
    shot("p6_build", ("c12s12", -0.2), build="uffizi", p=(("c12s12", -0.2), ("c12s13", "ünlü", 0.0)), tod="day", mode="day", longtake=True, cam=("push", 0.05), **D,
         ovl=ov(L.tag("UFFIZI", 560, 235, ("c12s12", "Uffizi,", -0.1), size=60, w=520),
                L.tag("= OFİSLER", 1360, 235, ("c12s12", "ofisler", -0.15), size=52, w=620),
                L.silhouette_queue(-60, 905, 8, ("c12s13", "galerilerinden", -0.2), speed=90.0, h=130, dir=1, step=170.0, seed=3),
                L.stamp("MEMUR BİNASI", 1430, 430, ("c12s13", "memur", -0.1), size=64, rot=-0.07)),
         tr=("zoomthru", 1.0, dict(at=(960, 560), at_b=(960, 560))), link="scale", label="Uffizi kendini kurar (imza)"),
    # 21 · 1565: koridor çizgisi (plan): Uffizi → Palazzo Vecchio → Arno → Pitti
    shot("c12_plan", ("c12s14", -0.15), built=True, corr_at=("c12s14", "1565'te", 0.6), corr_dur=4.4, lab_pv=("c12s14", "Palazzo", -0.1), lab_pitti=("c12s14", "Pitti", -0.1), lab_arno=("c12s14", "Arno'yu", -0.1),
         lab_uf=("c12s14", "Uffizi'nin", -0.3), lab_ponte=("c12s14", "Arno'yu", 0.3), mode="day", **D,
         cam=[(("c12s14", -0.15), look(960, 540, 1.0)), (("c12s14", "Palazzo", 0.0), look(840, 560, 1.12)), (("c12s14", "Arno'yu", -0.2), look(1100, 620, 1.12)), (("c12s14", "aşan", 0.5), look(1380, 700, 1.3))],
         ovl=L.date_plate("1565", ("c12s14", "1565'te", 0.0)),
         tr=("light", 0.9, dict(at=(960, 540))), link="light", label="1565: koridor çizgisi (plan)"),
    # 22 · Vasari Koridoru'nda kesintisiz kayma (Arno üstünde)
    shot("p6_pano", ("c12s14", "Arno'yu", 0.35), pano="corridor", tod="dusk", mode="day", longtake=True, cam=("push", 0.05), **D,
         cams=[(("c12s14", "Arno'yu", 0.35), (1000, 0, 1.0)), (("c12s14", "iktidarın", 0.0), (2300, 0, 1.0)), (("c12s14", "evine", 0.0), (3500, 0, 1.0)), (("c12s15", "çok", 0.0), (4700, 0, 1.0))],
         ovl=ov(L.tag("ARNO", 960, 215, ("c12s14", "aşan", -0.1), size=48, w=360, out=("c12s14", "iktidarın", 0.0)),
                L.tag("İKTİDARIN OFİSİNDEN EVİNE", 960, 215, ("c12s14", "iktidarın", -0.1), size=44, w=1020, out=("c12s15", "Müze", 0.1)),
                L.tag("KAPALI BİR YOL", 960, 820, ("c12s14", "kapalı", -0.1), size=40, w=560, out=("c12s15", "Müze", 0.1))),
         tr=("zoomthru", 1.0, dict(at=(1380, 700), at_b=(960, 540))), link="scale", label="Vasari Koridoru'nda kayma (imza)"),
    # 23 · Müze olması çok sonra: 1769'da halka açıldı (kapı açılır, kuyruk girer)
    shot("p6_sehir", ("c12s15", "Müze", -0.2), scene="sokak", door="open", door_at=("c12s15", "açıldı.", -0.5), tod="day", mode="day", cam=("push", 0.05), **D, actors=[],
         ovl=ov(L.timeline_span(300, 1620, 270, ("c12s15", "olması", -0.1), dur=2.6, l0="1560", l1="1769", at1=("c12s15", "1769'da", -0.1)),
                L.silhouette_queue(-80, 880, 6, ("c12s15", "bina", 0.0), speed=70.0, h=150, dir=1, step=190.0, seed=5)),
         tr=("carry", 0.9, dict(strip="banner", dir="r")), link="carry", label="1769: halka açıldı"),

    # ══ V5 · SANTO STEFANO (s16–s18) ═══════════════════════════════════════════════════════
    # 24 · kendi şövalye tarikatı: sancak direğe çekilir
    shot("c12_sancak", ("c12s16", -0.15), rise_at=("c12s16", "kendi", -0.2), rise_dur=2.6, mode="day", cam=("push", 0.05), **D,
         ovl=ov(L.label("ŞÖVALYE TARİKATI", 1240, 150, ("c12s16", "şövalye", -0.1), size=52, face="title_m", track=12),
                L.tag("SANTO STEFANO", 1240, 880, ("c12s16", "Santo", -0.1), size=58, w=860)),
         tr=("iris", 0.9, dict(obj="seal", at=(960, 520), r=210)), link="shape", label="Santo Stefano sancağı yükselir"),
    # 25 · Papa 1561'de onayladı (belge + kurşun/mum mühür)
    shot("p6_doc", ("c12s17", -0.15), title="PAPA ONAYI", date="1 EKİM 1561", w=1160, h=640, seal=True, seal_at=("c12s17", "onayladı;", -0.2), mode="day", cam=("push", 0.06), **D,
         lines=[("Santo Stefano Tarikatı", ("c12s17", "Papa", 0.0))],
         tr=("sayfa", 0.9), link="material", label="Papa onayı (1 Ekim 1561)"),
    # 26 · 1562'de Pisa'da Cosimo büyük usta olarak giydirildi
    shot("p6_medal", ("c12s17", "1562'de", -0.2), key="m_cosimo1_o", metal="bronze", pos="l", size=620, mode="day", cam=("push", 0.06), **D,
         ovl=ov(L.mantle(("c12s17", "giydirildi.", -0.9), cx_=653, y_=610, w=520),
                L.tag("BÜYÜK USTA", 1400, 400, ("c12s17", "büyük", -0.1), size=56, w=700),
                L.date_plate("15 MART 1562 · PİSA", ("c12s17", "Pisa'da", -0.1), x=1050, y=640)),
         tr=("light", 0.9, dict(at=(520, 540))), link="light", label="1562 Pisa: büyük usta (manto)"),
    # 27 · amaç: Osmanlı/korsan gemileriyle savaşmak, Hristiyan esirleri kurtarmak
    shot("p6_deniz", ("c12s18", -0.15), scene="acik", tod="day", mode="day", cam=("pan", "r", 200), **D,
         ships=[dict(kind="kadirga", flag="toskana", x0=300, x1=1180, y=680, scale=1.0, t0=0.0, t1=("c12s18", "kurtarmaktı;", 0.0), highlight=True),
                dict(kind="kadirga", flag="osmanli", x0=1850, x1=1500, y=560, scale=0.7, t0=0.0, t1=("c12s18", "kurtarmaktı;", 0.0))],
         ovl=ov(L.stamp("KAYNAKLARA GÖRE", 1450, 270, ("c12s18", "Kaynaklara", 0.0), size=44, rot=-0.06, out=("c12s18", "amaç,", 0.9)),
                L.chain_break(1420, 760, ("c12s18", "esirleri", -0.2), ("c12s18", "kurtarmaktı;", -0.4), size=240, out=("c12s18", "ganimet", -0.2))),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Santo Stefano kadırgaları (pan r)"),
    # 28 · ganimet satışının Livorno'yu zenginleştirdiği yazılır (○)
    shot("p6_liman", ("c12s18", "ganimet", -0.25), variant="livorno", year=None, tod="day", mode="day", cam=("push", 0.07), **D,
         ovl=ov(L.tag("LİVORNO", 960, 215, ("c12s18", "Livorno'yu", -0.15), size=52, w=520),
                L.icon_at("coins", 1500, 760, ("c12s18", "zenginleştirdiği", -0.2), size=210, glow=True, bob=5),
                L.stamp("YAZILIR", 1500, 360, ("c12s18", "yazılır.", -0.1), size=52, rot=-0.07)),
         tr=("yikama", 0.9), link="color", label="Livorno: ganimet (yazılır ○)"),

    # ══ V6 · KASIM–ARALIK 1562 (s19–s25; yıldız an; AĞIR) ═══════════════════════════════════
    # 29 · aile kıyıda geziye çıktı ve sıtmaya yakalandı (renk solar)
    shot("p6_deniz", ("c12s19", -0.15), scene="acik", tod="dusk", mode="day", cam=("pan", "r", 150), **D,
         ships=[dict(kind="tekne", flag="toskana", x0=300, x1=1450, y=640, scale=0.9, t0=0.0, t1=("c12s19", "yakalandı.", 0.3), crew=True)],
         ovl=ov(L.date_plate("KASIM 1562", ("c12s19", "Kasım", 0.0)),
                L.desat(("c12s19", "sıtmaya", -0.3), ("c12s19", "yakalandı.", 0.6), k_max=0.92, dark=0.55, tint="#59607A", tint_a=0.18)),
         tr=("dip", 0.9), link="color", label="Kasım 1562: kıyıda gezi, renk solar"),
    # 30 · üç tarih kartı, üç mum (tek uzun plan; sessizlik)
    shot("c12_1562", ("c12s20", -0.2), mode="night", longtake=True, **D,
         stations=[dict(x=960, big="20 KASIM", name="GIOVANNI", sub="KARDİNAL · 19 YAŞINDA", at=("c12s20", "20", -0.1), snuff_at=("c12s20", "öldü;", 0.0)),
                   dict(x=2360, big="", double=("6", "12", "ARALIK"), name="GARZIA", sub="15 YA DA 16 YAŞINDA", at=("c12s21", "Aralığın", -0.1), snuff_at=("c12s21", "gitti;", 0.0)),
                   dict(x=3760, big="17 ARALIK", name="ELEONORA", at=("c12s22", "17", -0.1), snuff_at=("c12s22", "öldü:", 0.0))],
         span=dict(at=("c12s22", "dört", -0.1), x0=960, x1=3760, label="DÖRT HAFTA"),
         cam=[(("c12s20", -0.2), look(1000, 560, 1.12)), (("c12s20", "öldü;", 0.6), look(1060, 560, 1.08)), (("c12s21", -0.1), look(2320, 560, 1.1)), (("c12s21", "gitti;", 0.8), look(2400, 560, 1.06)),
              (("c12s22", -0.1), look(3700, 560, 1.1)), (("c12s22", "öldü:", 0.0), look(3720, 560, 1.06)), (("c12s22", "haftada", 0.0), look(3700, 540, 1.0)),
              (("c12s22", "ölüm.", 0.5), look(2360, 520, 0.52)), (("c12s23", -0.15), look(2360, 520, 0.5))],
         tr=("candle", 1.0, dict(at=(960, 640), at_b=(960, 640))), link="light", label="üç tarih, üç mum (uzun plan)"),
    # 31 · RİVAYET (gravür): Garzia kardeşini, Cosimo da Garzia'yı öldürmüş; çok sonra ortaya çıkan, ilk yazanı bilinmeyen hikâye
    shot("c12_rivayet", ("c12s23", -0.15), a_nodes=("c12s23", "hikâye", -0.2), a1=("c12s23", "kardeşini,", -0.3), a2=("c12s23", "Garzia'yı", -0.4), a_axis=("c12s23", "Rivayet", -0.2),
         a_slip=("c12s23", "ortaya", -0.5), a_q=("c12s23", "yazanını", -0.1), mode="day", **D,
         cam=[(("c12s23", -0.15), look(1040, 520, 1.0)), (("c12s23", "Rivayet", -0.2), look(1040, 620, 0.95)), (("c12s23", "ortaya", 0.0), look(2300, 640, 1.0)), (("c12s23", "gösteremiyoruz.", 0.3), look(3100, 640, 1.1))],
         ovl=ov(L.stamp("RİVAYET", 1500, 250, ("c12s23", "Rivayet", -0.1), size=72, rot=-0.08, out=("c12s23", "ölümlerden", 0.4)),
                L.stamp("BELGE YOK", 1100, 250, ("c12s23", "gösteremiyoruz.", -0.5), size=52, rot=0.05)),
         tr=("yikama", 1.0), link="color", label="rivayet: gravür diyagram, çok sonra"),
    # 32 · 1857: mezar açılır; kırmızı atlas ceket; şiddet izi yok; sıtmayla uyumlu bulgular
    shot("c12_ceket", ("c12s24", -0.15), open_at=("c12s24", "mezar", -0.95), reveal_at=("c12s24", "açıldığında", 0.0), glint_at=("c12s24", "atlas", -0.2), mode="night", **D,
         cam=[(("c12s24", -0.15), look(960, 560, 1.18)), (("c12s24", "kırmızı", -0.3), look(960, 560, 1.05)), (("c12s24", "şiddet", 0.0), look(980, 620, 1.2)), (("c12s24", "verdi.", 0.0), look(960, 560, 1.0))],
         ovl=ov(L.engr("1857", 960, 160, ("c12s24", "1857'de", -0.1), size=92, style="gilt", track=14, out=("c12s24", "izi", 0.6)),
                L.tag("ŞİDDET İZİ GÖRÜLMEDİ", 960, 900, ("c12s24", "şiddet", -0.1), size=44, w=860, out=("c12s24", "sonraki", 0.2)),
                L.tag("KEMİK İNCELEMELERİ: SITMAYLA UYUMLU", 960, 900, ("c12s24", "sonraki", 0.1), size=40, w=1180)),
         tr=("dip", 1.0), link="light", label="1857: mezar, kırmızı atlas ceket"),
    # 33 · Cosimo'nun o haftalarda ne düşündüğünü bilmiyoruz (karanlıkta madalya)
    shot("p6_medal", ("c12s25", -0.15), key="m_cosimo1_o", metal="bronze", pos="c", size=600, mode="night", cam=("pull", 0.07), **D,
         ovl=ov(L.dim(("c12s25", "haftalarda", -0.1), None, alpha=0.45, dur=1.6),
                L.engr("?", 1500, 650, ("c12s25", "bilmiyoruz.", -0.5), size=240, style="gilt", track=2, dur=1.4)),
         tr=("candle", 1.0, dict(at=(960, 640), at_b=(960, 640))), link="light", label="ne düşündüğünü bilmiyoruz"),

    # ══ V7 · AKADEMİ VE MICHELANGELO (s26–s28) ═══════════════════════════════════════════
    # 34 · 13 Ocak 1563: Sanatlar Akademisi (belge)
    shot("p6_doc", ("c12s26", -0.15), title="SANATLAR AKADEMİSİ", date="13 OCAK 1563", w=1180, h=660, seal=True, seal_at=("c12s26", "kuruldu:", -0.3), mode="day", cam=("push", 0.06), **D,
         lines=[("Cosimo'nun desteğiyle", ("c12s26", "desteğiyle,", -0.3)), ("Vasari'nin yönetiminde", ("c12s26", "yönetiminde", -0.3))],
         tr=("sayfa", 0.9), link="material", label="Sanatlar Akademisi (13 Ocak 1563)"),
    # 35 · yarı lonca, yarı akademi
    shot("p6_iconrow", ("c12s26", "yarı", -0.3), items=[dict(icon="shield", label="LONCA", at=("c12s26", "lonca,", -0.2)), dict(icon="laurel", label="AKADEMİ", at=("c12s26", "akademi,", -0.2))],
         size=360, mode="day", cam=("push", 0.07), **D,
         ovl=ov(L.stamp("YARI", 700, 330, ("c12s26", "yarı", -0.05), size=46, rot=-0.06, out=("c12s26", "akademi,", 0.0)), L.stamp("YARI", 1220, 330, ("c12s26", "yarı", 1, -0.05), size=46, rot=0.05)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="yarı lonca, yarı akademi"),
    # 36 · Medici devletindeki sanat üretimini denetleyen kurul
    shot("p6_oda", ("c12s26", "Medici", -0.2), room="salon", variant="signoria", path="sweep_r", tod="dusk", mode="day", cam=("push", 0.04), **D,
         ovl=ov(L.tag("KURUL", 960, 215, ("c12s26", "kurul.", -0.9), size=54, w=420), L.icon_at("scales", 1500, 330, ("c12s26", "denetleyen", -0.1), size=190, glow=True, bob=4)),
         tr=("light", 0.9, dict(at=(960, 540))), link="light", label="denetleyen kurul"),
    # 37 · Michelangelo kurumun başındaki adlardan biri
    shot("p6_medal", ("c12s27", -0.15), key="m_michelangelo", metal="bronze", pos="l", size=560, mode="day", cam=("push", 0.06), **D,
         ovl=ov(L.tag("MICHELANGELO", 1380, 380, ("c12s27", "Michelangelo", -0.05), size=60, w=860),
                L.label("KURUMUN BAŞINDAKİ ADLARDAN BİRİ", 1380, 520, ("c12s27", "kurumun", 0.0), size=34, face="cap_i")),
         tr=("light", 0.9, dict(at=(520, 540))), link="light", label="Michelangelo (Akademi)"),
    # 38 · 1564'te ölünce cenazesini Akademi düzenledi (alay; ağır)
    shot("p6_procession", ("c12s27", "1564'te", -0.25), dir="r", density=1.1, mix=dict(cleric=0.30, elder=0.25, page=0.15, banner=0.2, common=0.1), speed=75.0, tod="dusk", mode="day", cam=("pan", "r", 150), **D,
         ovl=ov(L.date_plate("14 TEMMUZ 1564 · SAN LORENZO", ("c12s27", "1564'te", 0.1), x=96, y=800), L.tag("AKADEMİ", 1460, 215, ("c12s27", "Akademi", -0.1), size=50, w=520)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="cenaze alayı (Akademi düzenledi)"),
    # 39 · güzelliği de bir devlet dairesi gibi örgütledi
    shot("c12_daire", ("c12s28", -0.15), belt_at=("c12s28", -0.15), sign_at=("c12s28", "devlet", -0.2), mode="day", cam=("push", 0.05), **D,
         tr=("carry", 0.9, dict(strip="ribbon", dir="r")), link="carry", label="güzellik, devlet dairesi (mühür)"),

    # ══ V8 · BÜYÜK DÜK, LEPANTO, ÖLÜM (s29–s35) ═════════════════════════════════════════
    # 40 · 1564: yönetimi Francesco'ya bıraktı ama dük unvanını korudu
    shot("p6_medals", ("c12s29", -0.15), items=[dict(key="m_cosimo1_o", name="COSIMO", at=("c12s29", "Cosimo", -0.2)), dict(key="m_francesco", name="FRANCESCO", at=("c12s29", "Francesco'ya", -0.3))],
         size=470, mode="day", cam=("push", 0.07), **D,
         ovl=ov(L.date_plate("1564", ("c12s29", "1564'te", 0.0)),
                L.icon_move("keys", (620, 520), (1320, 520), ("c12s29", "günlük", 0.0), dur=1.4, size=160, arc=80),
                L.icon_at("crown", 697, 150, ("c12s29", "korudu.", -0.7), size=190, glow=True, bob=4),
                L.tag("DÜK UNVANI", 697, 880, ("c12s29", "dük", -0.1), size=40, w=520)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="yönetim Francesco'ya, unvan Cosimo'da"),
    # 41 · 1569 Büyük Dük, 1570 taç (ünvan rayı)
    shot("c12_unvan", ("c12s30", -0.15), mode="day", **D,
         plates=[dict(x=560, main="BÜYÜK DÜK", sub="27 AĞUSTOS 1569 · V. PIUS", at=("c12s30", "1569'da", -0.1), stamp=[("ROMA", ("c12s30", "Büyük", -0.1), 430, 80, -0.14)], w=700),
                 dict(x=1480, main="TAÇ", sub="5 MART 1570 · ROMA", at=("c12s30", "1570'te", -0.1), stamp=[("ROMA", ("c12s30", "taç", -0.1), 330, 80, 0.12)], w=700)],
         crown=dict(x=1480, y=200, at=("c12s30", "taç", -0.1), size=200),
         cam=[(("c12s30", -0.15), look(900, 430, 1.1)), (("c12s30", "1570'te", 0.0), look(1180, 430, 1.0)), (("c12s31", -0.3), look(1380, 430, 1.1))],
         tr=("light", 0.9, dict(at=(1480, 420))), link="light", label="Büyük Dük → taç (ünvan rayı)"),
    # 42 · İmparatorun onayı: kentin birincisi → dük → Roma tacı → Viyana faturası (mizah: sistem)
    shot("c12_unvan", ("c12s31", -0.2), mode="day", **D,
         plates=[dict(x=900, main="KENTİN BİRİNCİSİ", at=("c12s31", "kentin", -0.1), w=520),
                 dict(x=1560, main="DÜK", at=("c12s31", "dük", -0.1), w=360),
                 dict(x=2200, main="TAÇ", sub="ROMA", at=("c12s31", "Roma", -0.1), w=380),
                 dict(x=2860, main="VİYANA", sub="FATURA", at=("c12s31", "Viyana", -0.1), w=440)],
         crown=dict(x=560, y=190, at=("c12s31", "İmparatorun", -0.1), size=210, out=("c12s31", "kentin", 0.2)),
         coins=dict(x=560, y=640, at=("c12s31", "para", -0.1), size=170),
         invoice=dict(at=("c12s31", "fatura", -0.35), x=2860, y=700, stamp=("VİYANA", ("c12s31", "kesti.", -0.1))),
         cam=[(("c12s31", -0.2), look(760, 430, 1.1)), (("c12s31", "kentin", 0.0), look(1000, 430, 1.0)), (("c12s31", "dük", 0.2), look(1560, 450, 1.0)), (("c12s31", "Roma", 0.2), look(2200, 460, 1.0)),
              (("c12s31", "Viyana", 0.0), look(2780, 520, 1.0)), (("c12s31", "kesti.", 0.3), look(2860, 540, 1.1))],
         ovl=L.stamp("ANLATILIR", 1500, 160, ("c12s31", "anlatılır:", -0.3), size=52, rot=-0.06, out=("c12s31", "kentin", 0.4)),
         tr=None, link="cam", label="ünvan zinciri → fatura (mizah)"),
    # 43 · Lepanto/İnebahtı (harita)
    shot("p6_map", ("c12s32", -0.15), view=(21.6, 38.6, 6.4), mode="day", cam=("push", 0.07), **D,
         cities=[dict(lon=21.8, lat=38.37, name="LEPANTO", kind="town", at=("c12s32", "Lepanto'da,", -0.4), size=34, color="#233C8C", side="l"),
                 dict(lon=21.8, lat=38.37, name="İNEBAHTI", kind="town", at=("c12s32", "İnebahtı'da,", -0.5), size=34, color="#B33620", side="r")],
         icons_=[dict(kind="galley", lon=20.3, lat=38.1, at=("c12s32", "Lepanto'da,", 0.0), size=64, metal="gold"), dict(kind="galley", lon=22.4, lat=38.0, at=("c12s32", "İnebahtı'da,", 0.0), size=64, metal="gold", flip=True)],
         ovl=L.date_plate("7 EKİM 1571", ("c12s32", "Ekim", -0.1)),
         tr=("zoomthru", 0.9, dict(at=(960, 540), at_b=(960, 540))), link="scale", label="Lepanto / İnebahtı: harita"),
    # 44 · iki filo: yaklaşık iki yüz kadırga; Toskana'dan on iki (kadırga çubuğu); Osmanlı donanması ağır bir yenilgi aldı
    shot("p6_deniz_filo", ("c12s32", "Hristiyan", -0.4), n=24, highlight=12, gap=(1700, 420), horizon=292, smoke_at=("c12s33", "yenilgi", -0.4), smoke_dur=3.2, dim=0.5, tod="day", mode="day",
         longtake=True, cam=("push", 0.04), **D,
         ovl=ov(L.fleet_bar(("c12s32", "yaklaşık", -0.2), n_hi=12, n_all=200, hi_at=("c12s32", "on", -0.1), out=("c12s33", "donanması", 0.0)),
                L.tag("OSMANLI DONANMASI", 1440, 860, ("c12s33", "Osmanlı", -0.1), size=40, w=700)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="iki filo; 12 / ≈200; duman"),
    # 45 · Nisan 1574: Villa di Castello'da öldü (mum söner)
    shot("p6_medal", ("c12s34", -0.15), key="m_cosimo1_o", metal="bronze", pos="l", size=600, mode="night", cam=("pull", 0.06), **D,
         ovl=ov(L.tag("COSIMO", 1380, 360, ("c12s34", "Cosimo,", -0.1), size=56, w=520),
                L.date_plate("NİSAN 1574", ("c12s34", "Nisan", -0.05), x=96, y=800),
                L.tag("VILLA DI CASTELLO", 1380, 520, ("c12s34", "Villa", -0.1), size=40, w=700),
                L.dim(("c12s34", "öldü.", -0.2), None, alpha=0.72, dur=1.2)),
         tr=("candle", 1.0, dict(at=(520, 640), at_b=(960, 640))), link="light", label="Cosimo'nun ölümü (ışık söner)"),
    # 46 · Cosimo Floransa'da bir devlet kurarken (Floransa silueti, soldan sağa)
    shot("p6_skyline", ("c12s35", -0.1), seed=5, tod="dusk", mode="day", pan=300, cam=("pan", "r", 300), **D,
         ovl=L.label("FLORANSA", 960, 215, ("c12s35", "Floransa'da", -0.1), size=62, face="title", track=16, out=("c12s35", "Paris'te,", -0.2)),
         tr=("light", 0.9, dict(at=(960, 520))), link="light", label="Floransa'da devlet"),
    # 47 · aynı yıllarda Paris'te: iplik Floransa'dan Paris'e uzanır (c13'ün motifi); 24 Ağustos 1572
    shot("p6_map", ("c12s35", "Paris'te,", -0.55), mode="day", cam=("push", 0.03), **D,
         cams=[(("c12s35", "Paris'te,", -0.55), (11.2558, 43.7696, 5.2)), (("c12s35", "kızı,", 0.0), (6.5, 46.3, 4.2)), (("c12s35", "ortasındaydı.", -0.2), (2.6, 48.8, 6.4))],
         cities=[dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c12s35", "Floransa'da", 0.0), size=34, color="#B33620", side="r"),
                 dict(lon=2.3522, lat=48.8566, name="PARİS", kind="capital", at=("c12s35", "Paris'te,", -0.1), size=38, color="#233C8C", side="r")],
         routes=[dict(pts=[(11.2558, 43.7696), (9.0, 45.0), (6.0, 46.6), (4.0, 47.9), (2.3522, 48.8566)], at=("c12s35", "doğumlu", -0.4), dur=3.2, color="#8E3342", width=5.0, arrow=False)],
         ovl=ov(L.date_plate("24 AĞUSTOS 1572", ("c12s35", "24", -0.1)),
                L.desat(("c12s35", "krizin", -0.3), ("c12s35", "ortasındaydı.", 0.2), k_max=0.6, dark=0.5)),
         tr=("zoomthru", 0.9, dict(at=(1100, 560), at_b=(960, 540))), link="scale", label="iplik Floransa → Paris (kapı)"),
]

YIL_AT = [(("c12s1", "1537'de", -0.2), 1537), (("c12s5", "1539'da", -0.1), 1539), (("c12s9", "1548'de", -0.1), 1548), (("c12s10", "1557'de", -0.1), 1557), (("c12s11", "1560'ta", -0.1), 1560),
          (("c12s14", "1565'te", -0.1), 1565), (("c12s19", "1562'de", -0.1), 1562), (("c12s26", "1563'te,", -0.1), 1563), (("c12s27", "1564'te", -0.1), 1564), (("c12s30", "1569'da", -0.1), 1569),
          (("c12s32", "1571'de", -0.1), 1571), (("c12s34", "1574'te", -0.1), 1574)]
