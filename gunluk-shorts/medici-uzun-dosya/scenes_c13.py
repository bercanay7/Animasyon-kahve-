"""c13 — İki Kraliçe (1519–1642). PARÇA 6 KAPANIŞI (bitiş ekranı «SIRADAKİ PARÇA»; Parça 7: Roma Doğu Dilleri Matbaası / Galileo).
Yönetmen kartı: yonetmen_c13.md · notlar: notlar_c13.md. Tüm çekimler cümle/sözcük çapalı (mutlak saniye yok): gerçek ElevenLabs sesi gelince zamanlar çapalardan yeniden hizalanır.
Renk anahtarı: Perde III (MİRAS): Fransa zambak mavisi + altın (V1–V6, gün/alacakaranlık), 1572 gece (lacivert + kor pencere), Rubens galerisi sıcak ten/sinabar, Köln soğuk gri-lapis.
Sözleşme: RENK = belge/olgu · GRAVÜR (sepya, tek renk) = anekdot/efsane/rivayet. Damgalar (MİT/ANEKDOT/SÖYLENDİ) renkli çarpar. Yüz çizilmez (madalya/siluet). Rubens'ten KOPYA yok:
kodla üretilmiş küçük kompozisyonlar + Louvre başlıkları. İPLİK (Parklar): c12 kapısında başlar → Marsilya 1533 → Catherine'de kalınlaşır → Blois'da serbest kalır →
Marie'de yeniden başlar (Pitti) → Rubens'in ilk çerçevesinde parlar → Köln'de kopar.
İmza sekans: «Mit faturası» (c13s17–c13s21): beş kart tek hanede (gravür) → damgalar tok vuruşla → son kart BALET damgasız, altın GERÇEK mührü, renk patlar.
Mizah: YALNIZ fatura rayı (V5), mahsup/«en kibar yol» (V7), «yeniden yazdırmanın en pahalı yolu» (V9; sipariş sistemi). KAPALI: V1, 1559, 1572, Blois, V8, Köln.
"""
from shots import shot
import cilt_medici as CM
import p6_lib as L
import c13_kinds as K

look = L.look
ov = L.ov

D = dict(perde=3)

SHOTS = [
    # ══ V1 · MARSİLYA 1533 (s1–s4) ═══════════════════════════════════════════════════════════
    # 1 · yetim: doğum + ebeveyn tarihleri; iplik soldan (c12 kapısından) gelir, Catherine'e bağlanır, ebeveyn çizgileri solarken yalnız iplik sürer
    shot("c13_yetim", ("c13s1", 0), a_c=("c13s1", "Catherine'di.", -0.5), a_l=("c13s1", "babası,", -0.25), a_m=("c13s1", "annesi", -0.25),
         a_el=("c13s1", "babası,", 0.0), a_em=("c13s1", "annesi", 0.0), d_m=("c13s1", "haftalarda", -0.35), d_l=("c13s1", "öldü.", -0.6), a_die=("c13s1", "öldü.", 0.5),
         mode="day", cam=("push", 0.06), **D,
         ovl=ov(L.tag("FLORANSA", 960, 100, ("c13s1", "Floransa'da", -0.1), size=44, w=480),
                L.thread([(-60, 930), (360, 850), (680, 730), (800, 660)], ("c13s1", 0), dur=1.9, w=3.0, w_end=5.0),
                L.thread([(1120, 700), (1440, 800), (1720, 880), (2020, 930)], ("c13s1", "öldü.", 0.5), dur=1.6, w=5.0, w_end=7.0)),
         label="Catherine: yetim (soy çizgisi, iplik)"),
    # 2 · ANEKDOT (gravür): kuşatma altındaki şehir, bazı sesler çocuğu surlara çıkarıp düşmanın önüne koymayı önerir (kim önerdi bilinmez; ayrıntı yok)
    shot("p6_sehir", ("c13s2", -0.35), scene="kale", act="sur", tod="day", mode="day", mono=1.0, cam=("pull", 0.06), **D,
         actors=[dict(kind="cocuk", x=1480, y=700, h=120, dir=-1, action="idle", seed=4)],
         ovl=ov(L.tag("KUŞATMA", 480, 230, ("c13s2", "kuşatma", -0.1), size=46, w=420, out=("c13s2", "anlatılır.", 0.4)),
                K.voice_arcs(120, 600, ("c13s2", "seslerin", -0.15), out=("c13s2", "koymayı", 0.3)),
                L.tag("BAZI SESLER", 360, 820, ("c13s2", "seslerin", -0.1), size=38, w=440, out=("c13s2", "koymayı", 0.3)),
                L.stamp("ANEKDOT", 1450, 300, ("c13s2", "anlatılır.", -0.4), size=62, rot=-0.08)),
         tr=("yikama", 0.9), link="material", label="kuşatma anekdotu (gravür)"),
    # 3 · 1533: Clemens → Catherine ↔ Henri (üç madalya; iplik üstten geçer)
    shot("p6_medals", ("c13s3", -0.2), items=[dict(key="klemens", name="VII. CLEMENS", role="MEDICI PAPASI", at=("c13s3", "Clemens", -0.45)),
                                              dict(key="m_catherine", name="CATHERINE", at=("c13s3", "onu", -0.3)),
                                              dict(key="m_henri2", name="HENRI", role="FRANSA KRALI'NIN OĞLU", at=("c13s3", "Henri", -0.4))],
         size=400, mode="day", cam=("push", 0.07), **D,
         ovl=ov(L.date_plate("28 EKİM 1533 (27)", ("c13s3", "1533'te", 0.2)),
                L.thread([(450, 300), (700, 235), (960, 300), (1190, 230), (1450, 300)], ("c13s3", "papası", 0.0), dur=2.4, w=4.0, w_end=6.0),
                L.icon_at("ring", 1184, 150, ("c13s3", "evlendirdi.", -0.6), size=150, glow=True, bob=5)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Clemens → Catherine, Henri (1533)"),
    # 4 · Marsilya 1533 (V7 ile AYNI kadraj): kadırga yanaşır, iplik denizde çizilir; gelin 14 yaşında
    shot("p6_liman", ("c13s3", "evlendirdi.", -0.35), variant="marsilya", year=1533, thread=True, t_dock=("c13s4", "yaşındaydı.", -1.0), mode="day", **D,
         ovl=ov(L.tag("MARSİLYA", 960, 215, ("c13s4", "Marsilya'daydı;", -0.1), size=52, w=560, out=("c13s4", "gelin", 0.6)),
                L.count_up(1560, 300, ("c13s4", "14", -0.1), 14, dur=0.9, unit="YAŞINDA", size=150),
                L.tag("ÇEYİZ ≈100.000 ALTIN", 1560, 520, ("c13s4", "yaşındaydı.", -0.2), size=34, w=520)),
         tr=("zoomthru", 0.9, dict(at=(1184, 160), at_b=(960, 540))), link="scale", label="Marsilya 1533 (ilk kadraj)"),

    # ══ V2 · ON YIL (s5–s6) ═════════════════════════════════════════════════════════════════
    # 5 · çocuksuz on yıl: Henri–Diane önde, pencerede küçük Catherine; yıl sayacı 1533 → 1543; 10 yuvarlak; «çok»: yuvarlak ızgara
    shot("p6_oda", ("c13s5", -0.3), room="bos", variant="blois", path="default", figure=False, candle_lit=True, tod="dusk", mode="day", cam=("push", 0.04), **D,
         actors=[dict(kind="soylu", x=1180, y=806, h=268, action="idle", sil="#120A06", seed=5, dir=-1, rim_dir=-1),
                 dict(kind="soylu_f", x=1380, y=806, h=268, action="idle", sil="#120A06", seed=9, dir=1, rim_dir=1)],
         ovl=ov(K.year_run(1560, 190, ("c13s5", "on", -0.1), 1533, 1543, dur=3.2, size=130, unit="YIL", out=("c13s6", "Sonra", 0.2)),
                L.dots_row(700, 880, 10, ("c13s5", "on", 0.0), step=0.3, r=22, gap=64, out=("c13s6", "Sonra", 0.3)),
                L.tag("DIANE DE POITIERS", 1480, 240, ("c13s5", "Diane", -0.15), size=34, w=520, out=("c13s6", "Sonra", 0.2)),
                K.dot_grid(660, 820, 11, 3, ("c13s6", "çocukları", -0.2), step=0.06, r=17, gx=54, gy=50)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="on yıl (oda, yıl sayacı, yuvarlaklar)"),

    # ══ V3 · DUL KRALİÇE (s7–s10) ═══════════════════════════════════════════════════════════
    # 6 · 10 Temmuz 1559: turnuva alanı; iki atlı birbirine koşar (çarpışma GÖSTERİLMEZ — kararma)
    shot("c13_turnuva", ("c13s7", -0.6), t_meet=("c13s7", "isabet", 0.5), mode="day", **D,
         cam=[(("c13s7", -0.6), look(640, 560, 1.0)), (("c13s7", "turnuvada", 0.0), look(900, 570, 1.08)), (("c13s7", "isabet", 0.4), look(1080, 580, 1.2)), (("c13s7", "öldü.", 0.0), look(1130, 580, 1.26))],
         ovl=ov(L.date_plate("10 TEMMUZ 1559", ("c13s7", "Temmuz", -0.2)), L.tag("TURNUVA", 960, 215, ("c13s7", "turnuvada", -0.1), size=50, w=460)),
         tr=("giornata", 0.9), link="material", label="turnuva: iki atlı (çarpışma yok)"),
    # 7 · siyahtan siyah giysili madalya yükselir
    shot("p6_medal", ("c13s7", "öldü.", -0.4), key="m_catherine_dul", metal="bronze", pos="l", size=600, name="CATHERINE", role="DUL KRALİÇE", mode="day", cam=("push", 0.06), **D,
         ovl=ov(L.tag("SİYAH", 1400, 330, ("c13s8", "siyah", -0.1), size=60, w=560),
                L.stamp("YAZILIR", 1400, 640, ("c13s8", "yazılır.", -0.1), size=56, rot=-0.07),
                L.thread([(1100, 880), (1400, 830), (1700, 900), (2000, 860)], ("c13s8", "Catherine'in", 0.0), dur=2.2, w=5.0, w_end=7.0)),
         tr=("dip", 1.0), link="color", label="siyah giysili madalya (1559 sonrası)"),
    # 8 · 1560 sonunda küçük IX. Charles tahta çıkınca devleti fiilen Catherine yönetti
    shot("p6_oda", ("c13s9", -0.35), room="salon", variant="taht", path="taht", tod="dusk", mode="day", cam=("push", 0.04), **D,
         actors=[dict(kind="cocuk", x=1040, y=700, h=118, action="idle", sil="#120A06", seed=5, dir=-1, rim_dir=-1),
                 dict(kind="soylu_f", x=1250, y=806, h=290, action="idle", sil="#0A0604", seed=9, dir=-1, rim_dir=-1)],
         ovl=ov(L.date_plate("1560 SONU", ("c13s9", "1560", 0.0)),
                L.tag("IX. CHARLES", 640, 230, ("c13s9", "Charles", -0.1), size=48, w=520),
                L.tag("CATHERINE", 1380, 230, ("c13s9", "Catherine", -0.2), size=48, w=520),
                L.stamp("FİİLEN", 1380, 380, ("c13s9", "fiilen", -0.1), size=56, rot=-0.07)),
         tr=("light", 0.9, dict(at=(520, 540))), link="light", label="küçük kral, fiilen Catherine"),
    # 9 · din savaşını uzlaşmayla durdurmak istedi: iki sancak arasında el sıkışma
    shot("c13_uzlasma", ("c13s9", "yönetti.", -0.15), t_shake=("c13s10", "uzlaşmayla", 0.2), mode="day", cam=("push", 0.05), **D,
         ovl=ov(L.tag("DİN SAVAŞI", 440, 210, ("c13s10", "savaşını", -0.15), size=46, w=440), L.tag("UZLAŞMA", 1480, 210, ("c13s10", "uzlaşmayla", -0.2), size=46, w=440)),
         tr=("carry", 0.9, dict(strip="banner", dir="r")), link="carry", label="uzlaşma: el sıkışma"),
    # 10 · Ocak 1562 fermanı (belge): Protestanlara kent surlarının dışında ibadet izni
    shot("p6_doc", ("c13s10", "Ocak", -0.35), title="FERMAN", date="OCAK 1562", w=1180, h=640, seal=True, seal_at=("c13s10", "verdi.", -1.7), caption="Britannica · çeviri bize ait",
         lines=[("Fransız Protestanlarına", ("c13s10", "Fransız", -0.1)), ("kent surlarının dışında", ("c13s10", "surlarının", -0.2))],
         mode="day", cam=("push", 0.07), **D,
         ovl=ov(L.icon_at("castle", 1560, 330, ("c13s10", "kent", -0.2), size=190, glow=True, bob=4),
                L.stamp("SURLARIN DIŞINDA", 1560, 520, ("c13s10", "dışında,", -0.5), size=44, rot=-0.06)),
         tr=("sayfa", 0.9), link="material", label="Ocak 1562 fermanı"),
    # 11 · silahsız ibadet: surun dışında dua eden küçük topluluk
    shot("p6_sehir", ("c13s10", "silahsız", -0.3), scene="kale", act="sur", tod="day", mode="day", cam=("push", 0.05), **D,
         actors=[dict(kind="halk", x=1050, y=760, h=130, dir=1, action="idle", seed=3), dict(kind="halk", x=1130, y=770, h=124, dir=1, action="pray", seed=4),
                 dict(kind="halk", x=1210, y=762, h=128, dir=1, action="pray", seed=5), dict(kind="halk", x=1290, y=772, h=122, dir=1, action="pray", seed=6)],
         ovl=ov(L.tag("SİLAHSIZ İBADET", 960, 215, ("c13s10", "silahsız", -0.1), size=48, w=600)),
         tr=("iris", 0.9, dict(obj="seal", at=(1280, 440), r=110)), link="shape", label="surun dışında silahsız ibadet"),

    # ══ V4 · 1572 (s11–s14; AĞIR; mizah KAPALI; şiddet/çan/saat yok) ═════════════════════════
    # 12 · kamera sabit hızda üç karttan geçer; her kartta pencereler söner; ≈3.000 kartı sessiz belirir; tek mum küçülür
    shot("c13_1572", ("c13s11", -0.3), mode="night", longtake=True, **D,
         cards=[dict(x=1208, big="22 AĞUSTOS 1572", sub="AMİRAL COLIGNY: SUİKAST GİRİŞİMİ", at=("c13s11", "22", -0.15), dark=[("c13s11", "oldu;", 0.1), ("c13s11", "oldu;", 0.45), ("c13s11", "ertesi", 0.0)]),
                dict(x=2016, big="23 AĞUSTOS", sub="KONSEY: LİDERLERİN ÖLDÜRÜLMESİ", at=("c13s11", "ertesi", -0.1), dark=[("c13s11", "karar", -0.2), ("c13s11", "karar", 0.2), ("c13s11", "verdi.", 0.3)]),
                dict(x=2841, big="24 AĞUSTOS", sub="PARİS'TE KATLİAM BAŞLADI", at=("c13s12", "24", -0.1), dark=[("c13s12", "yayıldı;", -0.4), ("c13s12", "yayıldı;", 0.1), ("c13s12", "yayıldı;", 0.6)])],
         toll=dict(x=2841, at=("c13s12", "üç", -0.2), text="≈3.000 (PARİS, TAHMİN)"),
         candle=dict(x=3280, y=860, at=("c13s12", "yalnız", -0.5), out=("c13s12", "ölü", -0.6)),
         cam=[(("c13s11", -0.3), look(960, 560, 1.0)), (("c13s11", "1572'de", 0.0), look(1208, 560, 1.0)), (("c13s11", "konsey,", 0.0), look(2016, 560, 1.0)), (("c13s12", "Ağustos'ta", 0.0), look(2841, 560, 1.0)),
              (("c13s12", "yalnız", 0.0), look(3030, 580, 1.05)), (("c13s13", -0.1), look(3080, 590, 1.08))],
         tr=("yikama", 0.9), link="color", label="1572: üç tarih kartı, pencereler söner (sessiz)"),
    # 13 · Britannica: liderlerin öldürülmesi onaylanmıştı; katliam büyük olasılıkla değil; tarihçiler ayrılır
    shot("c13_onay", ("c13s13", -0.2), a_med=("c13s13", "Britannica'ya", 0.0), a_th1=("c13s13", "liderlerin", -0.3), a_tick=("c13s13", "onaylamıştı;", -0.2), a_th2=("c13s13", "katliamı", -0.3),
         a_q=("c13s13", "olasılıkla", 0.1), a_fork=("c13s14", "ayrılır.", -1.4), mode="day", cam=("push", 0.05), **D,
         ovl=ov(L.tag("BRITANNICA'YA GÖRE", 420, 230, ("c13s13", "Britannica'ya", -0.1), size=34, w=560),
                L.stamp("TARİHÇİLER AYRILIR", 960, 960, ("c13s14", "ayrılır.", -1.0), size=46, rot=0.02)),
         tr=("candle", 1.0, dict(at=(1220, 780), at_b=(960, 540))), link="light", label="onay: liderler ✓ / katliam ? (çatal)"),

    # ══ V5 · EFSANE VE FATURA (s15–s21) ═════════════════════════════════════════════════════
    # 14 · TON KIRILMAZ: çıplak fade (bölümün tek çıplak fade'i) → soluk gün ışığı, yazı masası/kütüphane
    shot("p6_oda", ("c13s15", -0.3), room="calisma", variant="kutuphane", path="scribe", figure="desk", tod="day", mode="day", cam=("push", 0.04), **D,
         ovl=ov(L.engr("KÖTÜ İTALYAN KRALİÇE", 960, 190, ("c13s15", "kötü", -0.2), size=70, track=10, dur=1.4, style="engraved"),
                L.stamp("EFSANE", 1500, 340, ("c13s15", "efsane", -0.1), size=62, rot=-0.07)),
         tr=("fade", 1.0), link=None, label="soluk gün ışığı: kütüphane (efsane doğar)"),
    # 15 · 1573: Protestan broşürdeki şiir (gravür)
    shot("p6_doc", ("c13s16", -0.2), title="BROŞÜR", date="1573", w=1100, h=640, mono=1.0, lines=[("Protestan bir broşür", ("c13s16", "Protestan", -0.1)), ("içinde bir şiir", ("c13s16", "şiirdi;", -0.4))],
         mode="day", cam=("push", 0.07), **D,
         ovl=ov(L.tag("İLK SALDIRILARDAN BİRİ", 960, 190, ("c13s16", "saldırılardan", -0.2), size=40, w=760)),
         tr=("sayfa", 0.9), link="material", label="1573 broşür şiiri (gravür)"),
    # 16 · 1575: adsız kitapçık → sonradan Henri Estienne'e atfedildi (gravür)
    shot("p6_doc", ("c13s16", "1575'te", -0.4), title="KİTAPÇIK", date="1575", w=1100, h=640, mono=1.0, lines=[("adsız bir kitapçık", ("c13s16", "adsız", -0.1))],
         mode="day", cam=("push", 0.07), **D,
         ovl=ov(L.stamp("ADSIZ", 1380, 330, ("c13s16", "adsız", 0.0), size=72, rot=-0.08, out=("c13s16", "atfedildi.", -0.2)),
                L.stamp("ATFEDİLDİ: HENRI ESTIENNE", 960, 800, ("c13s16", "Estienne'e", 0.0), size=44, rot=0.03)),
         tr=("sayfa", 0.9), link="material", label="1575 kitapçık: ADSIZ → atfedildi"),
    # 17 · İMZA (1/4): her şey onun hanesine — beş kart (gravür): çatal · dondurma · topuk · parfüm · zehir
    shot("c13_fatura", ("c13s17", -0.25), a_head=("c13s17", "hanesine", -0.3), mono=1.0, montage=True, mode="day", **D,
         items=[dict(label="ÇATAL", icon="fork", at=("c13s17", "çatalı", -0.1)), dict(label="DONDURMA", icon="ice", at=("c13s17", "dondurmayı", -0.1)), dict(label="TOPUK", icon="heel", at=("c13s17", "topuklu", -0.1)),
                dict(label="PARFÜM", icon="perfume", at=("c13s17", "parfümü", -0.1)), dict(label="ZEHİR", icon="vial", at=("c13s17", "zehri.", -0.1))],
         cam=[(("c13s17", -0.25), look(960, 540, 1.0)), (("c13s17", "çatalı", 0.0), look(520, 580, 1.35)), (("c13s17", "dondurmayı", 0.0), look(800, 580, 1.35)), (("c13s17", "topuklu", 0.0), look(1000, 580, 1.35)),
              (("c13s17", "parfümü", 0.0), look(1280, 580, 1.35)), (("c13s17", "zehri.", 0.2), look(1560, 580, 1.4)), (("c13s17", "zehri.", 1.4), look(1180, 560, 1.0))],
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="mit faturası: beş kart"),
    # 18 · İMZA (2/4): çatal Catherine'den önce İtalya'daydı (damga); bir anlatı onu Venedik'e gelen Bizans prensesine bağlar
    shot("c13_fatura", ("c13s18", -0.25), a_head=("c13s17", "hanesine", -0.3), mono=1.0, montage=True, mode="day", **D,
         items=[dict(label="ÇATAL", icon="fork", at=("c13s17", "çatalı", -0.1)), dict(label="DONDURMA", icon="ice", at=("c13s17", "dondurmayı", -0.1)), dict(label="TOPUK", icon="heel", at=("c13s17", "topuklu", -0.1)),
                dict(label="PARFÜM", icon="perfume", at=("c13s17", "parfümü", -0.1)), dict(label="ZEHİR", icon="vial", at=("c13s17", "zehri.", -0.1))],
         stamps=[("CATHERINE'DEN ÖNCE", 0, ("c13s18", "önce", -0.1), -0.07, 44, (0, 470))],
         cam=[(("c13s18", -0.25), look(1180, 560, 1.0)), (("c13s18", "Catherine'den", 0.0), look(520, 600, 1.5)), (("c13s18", "bağlar.", 0.0), look(500, 620, 1.62))],
         ovl=ov(L.tag("BİR ANLATI: BİZANS PRENSESİ", 1280, 230, ("c13s18", "anlatı", -0.1), size=38, w=720), L.tag("VENEDİK", 1280, 330, ("c13s18", "Venedik'e", -0.1), size=34, w=360),
                L.stamp("ANEKDOT", 1520, 460, ("c13s18", "prensesine", 0.0), size=50, rot=0.07)),
         tr=None, link="cam", label="çatal: CATHERINE'DEN ÖNCE (damga)"),
    # 19 · İMZA (3/4): dondurma 19. yüzyıl hikâyesi (damga)
    shot("c13_fatura", ("c13s19", -0.2), a_head=("c13s17", "hanesine", -0.3), mono=1.0, montage=True, mode="day", **D,
         items=[dict(label="ÇATAL", icon="fork", at=("c13s17", "çatalı", -0.1)), dict(label="DONDURMA", icon="ice", at=("c13s17", "dondurmayı", -0.1)), dict(label="TOPUK", icon="heel", at=("c13s17", "topuklu", -0.1)),
                dict(label="PARFÜM", icon="perfume", at=("c13s17", "parfümü", -0.1)), dict(label="ZEHİR", icon="vial", at=("c13s17", "zehri.", -0.1))],
         stamps=[("CATHERINE'DEN ÖNCE", 0, ("c13s18", "önce", -0.1), -0.07, 44, (0, 470)), ("19. YY HİKÂYESİ", 1, ("c13s19", "19.", -0.15), 0.06, 44, (0, 470))],
         cam=[(("c13s19", -0.2), look(520, 600, 1.45)), (("c13s19", "Dondurma", 0.0), look(800, 600, 1.5)), (("c13s19", "çıkıyor.", 0.0), look(780, 610, 1.62))],
         tr=None, link="cam", label="dondurma: 19. YY HİKÂYESİ (damga)"),
    # 20 · İMZA (4/4): topuk, parfüm, zehir damgaları (≈1 sn aralık) — «tek bir yabancıya yazmış; pratik bir düzen»
    shot("c13_fatura", ("c13s20", -0.2), a_head=("c13s17", "hanesine", -0.3), mono=1.0, montage=True, mode="day", **D,
         items=[dict(label="ÇATAL", icon="fork", at=("c13s17", "çatalı", -0.1)), dict(label="DONDURMA", icon="ice", at=("c13s17", "dondurmayı", -0.1)), dict(label="TOPUK", icon="heel", at=("c13s17", "topuklu", -0.1)),
                dict(label="PARFÜM", icon="perfume", at=("c13s17", "parfümü", -0.1)), dict(label="ZEHİR", icon="vial", at=("c13s17", "zehri.", -0.1))],
         stamps=[("CATHERINE'DEN ÖNCE", 0, ("c13s18", "önce", -0.1), -0.07, 44, (0, 470)), ("19. YY HİKÂYESİ", 1, ("c13s19", "19.", -0.15), 0.06, 44, (0, 470)),
                 ("BİNİCİ AYAKKABISI", 2, ("c13s20", "inceliğini", -0.1), -0.05, 40, (0, 470)), ("KANIT YOK", 3, ("c13s20", "günahını", 0.3), 0.07, 52, (0, 470)), ("EDEBÎ KALIP", 4, ("c13s20", "yabancıya", -0.1), -0.06, 44, (0, 470))],
         cam=[(("c13s20", -0.2), look(780, 600, 1.45)), (("c13s20", "inceliğini", 0.0), look(1000, 600, 1.35)), (("c13s20", "yabancıya", 0.0), look(1200, 590, 1.2)), (("c13s20", "düzen.", 0.2), look(1100, 560, 1.0))],
         ovl=ov(L.label("TEK BİR YABANCI", 960, 200, ("c13s20", "tek", -0.1), size=60, face="title", track=14)),
         tr=None, link="cam", label="topuk · parfüm · zehir damgaları; pratik bir düzen"),
    # 21 · Gerçek olan bir gösteriydi: Balet comique (RENK); altın GERÇEK mührü, damgasız
    shot("c13_balet", ("c13s21", -0.3), form_at=("c13s21", "Kirke", 0.0), mode="night", **D,
         cam=[(("c13s21", -0.3), look(700, 540, 1.1)), (("c13s21", "sahnelenen", 0.0), look(1000, 540, 1.04)), (("c13s21", "saray", 0.0), look(1240, 540, 1.0)), (("c13s21", "balesiydi.", 0.4), look(1180, 540, 1.06))],
         ovl=ov(L.engr("GERÇEK", 960, 150, ("c13s21", "Gerçek", -0.1), size=120, track=18, style="gilt", dur=1.2, glow=0.7),
                L.date_plate("15 EKİM 1581", ("c13s21", "15", -0.1)),
                L.tag("BALET COMIQUE", 560, 330, ("c13s21", "Balet", -0.1), size=42, w=560),
                L.tag("KİRKE EFSANESİ", 560, 410, ("c13s21", "Kirke", -0.1), size=34, w=500),
                L.count_up(1560, 330, ("c13s21", "beş", -0.1), 5, dur=0.9, unit="SAATİ AŞAN", size=150),
                L.icon_at("book", 1560, 600, ("c13s21", "basılı", -0.2), size=170, glow=True, bob=4)),
         tr=("iris", 0.9, dict(obj="seal", at=(1560, 560), r=120)), link="shape", label="Balet comique: GERÇEK (altın mühür)"),

    # ══ V6 · BLOIS (s22; AĞIR; mizah KAPALI) ═══════════════════════════════════════════════
    # 22 · Catherine 5 Ocak 1589'da Blois'da öldü; Guise Dükü aynı şatoda önceki yılın son günlerinde (iplik ucu serbest kalır; mum söner)
    shot("p6_oda", ("c13s22", -0.3), room="bos", variant="blois", path="default", figure=False, candle_lit=True, snuff_at=("c13s22", "öldü;", 0.5), tod="night", mode="night", cam=("push", 0.03), **D,
         ovl=ov(K.medal_ovl("m_catherine", 1330, 420, 330, ("c13s22", "Catherine,", -0.2), out=("c13s22", "öldü;", 0.0), out_dur=2.2, name="CATHERINE", dates="5 OCAK 1589"),
                L.thread([(-40, 830), (420, 770), (800, 640), (1130, 520)], ("c13s22", 0), dur=2.0, w=5.0, w_end=7.0, free_at=("c13s22", "öldü;", 0.2), free_dur=3.0),
                L.tag("BLOIS", 600, 215, ("c13s22", "Blois'da", -0.1), size=52, w=420),
                K.span13(560, 1360, 840, ("c13s22", "Guise", 0.0), "23 ARALIK 1588", "5 OCAK 1589", at1=("c13s22", "Ocak", -0.1), dur=2.2)),
         tr=("dip", 1.0), link="shape", label="Blois: Catherine'in ölümü, iplik ucu serbest"),

    # ══ V7 · MARIE VE ÇEYİZ (s23–s27) ═══════════════════════════════════════════════════════
    # 23 · yeni iplik: Pitti'den Marie'ye
    shot("p6_medal", ("c13s23", -0.3), key="m_marie", metal="bronze", pos="l", size=600, name="MARIE", role="MEDICI KIZI", mode="day", cam=("push", 0.06), **D,
         ovl=ov(L.tag("PİTTİ", 1400, 330, ("c13s23", "Medici", -0.1), size=60, w=420),
                L.thread([(1800, 480), (1500, 540), (1150, 450), (950, 400)], ("c13s23", "Marie,", -0.2), dur=2.0, w=3.0, w_end=5.0),
                L.tag("FRANSA'YA GELİN", 1400, 660, ("c13s23", "gelin", -0.2), size=42, w=620)),
         tr=("sayfa", 0.9), link="material", label="Marie: yeni iplik (Pitti)"),
    # 24 · 5 Ekim 1600: vekâleten (nefte sunak; kral orada değildi: BOŞ YER)
    shot("p6_pano", ("c13s24", -0.3), pano="nave", tod="dusk", mode="day", cam=("push", 0.04), **D,
         stations=[dict(x=3300, at_frac=0.0, fn=K.st_vekalet)],
         cams=[(("c13s24", -0.3), (2700, 0, 1.0)), (("c13s24", "kıyıldı;", 0.0), (3250, 0, 1.12)), (("c13s24", "değildi.", 0.5), (3150, 0, 1.2))],
         ovl=ov(L.date_plate("5 EKİM 1600", ("c13s24", "1600'de", -0.1)), L.tag("VEKÂLETEN", 960, 215, ("c13s24", "vekâleten", -0.15), size=52, w=480),
                L.tag("KRAL ORADA DEĞİLDİ", 960, 880, ("c13s24", "kral", -0.1), size=40, w=640)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="vekâleten kıyılan nikâh (boş yer)"),
    # 25 · çeyiz 600.000 écu (sikke)
    shot("p6_coin", ("c13s25", -0.25), at=("c13s25", "Çeyiz", -0.1), size=520, n=1, mode="day", cam=("push", 0.06), **D,
         ovl=ov(L.count_up(960, 200, ("c13s25", "600.000", -0.15), 600000, dur=1.3, unit="ÉCU · ÇEYİZ", size=130)),
         tr=("iris", 0.9, dict(obj="florin", at=(960, 520), r=130)), link="shape", label="çeyiz: 600.000 écu"),
    # 26 · defter: Fransa'nın borcundan düşüldü; gelinin parası damadın borcuna mahsup edildi; en kibar yol
    shot("p6_ledger", ("c13s25", "ve", -0.1), title_l="FRANSA'NIN BORCU", title_r="ÇEYİZ", cols=("ÉCU", "", ""),
         left=[dict(text="Toskana Büyük Dükü'ne", at=("c13s25", "Fransa'nın", -0.1), strike=("c13s25", "mahsup", 0.1))],
         right=[dict(text="Gelinin parası", amt=("600.000",), at=("c13s25", "gelinin", -0.2), hl=("c13s25", "mahsup", -0.2))],
         focus=(700, 640), mode="day", **D,
         ovl=ov(L.stamp("MAHSUP", 960, 880, ("c13s25", "mahsup", 0.0), size=64, rot=-0.06),
                L.icon_move("ring", (1500, 520), (620, 520), ("c13s26", "evlenmek.", -0.9), dur=1.6, size=150, arc=100)),
         tr=("sayfa", 0.9), link="material", label="defter: çeyiz ↔ borç (mahsup)"),
    # 27 · Marsilya 1600 (V1 ile AYNI kadraj): Marie 3 Kasım 1600'de indi
    shot("p6_liman", ("c13s26", "evlenmek.", -0.3), variant="marsilya", year="3 KASIM 1600", t_dock=("c13s27", "indi.", -0.8), mode="day", **D,
         ovl=ov(L.tag("MARSİLYA", 960, 215, ("c13s27", "Marsilya'ya", -0.2), size=52, w=560)),
         tr=("yikama", 0.9), link="color", label="Marsilya 1600 (AYNI kadraj)"),

    # ══ V8 · NAİPLİK, KAÇIŞ, SÜRGÜN (s28–s31; mizah KAPALI) ═══════════════════════════════
    # 28 · tek uzun plan: zaman çizgisi + altı vinyet; iplik sağ kenardan çıkar, kamera boş kalır
    shot("c13_zaman", ("c13s28", -0.3), longtake=True, tail_at=("c13s31", "dönmedi.", 0.0), mode="day", **D,
         events=[dict(x=900, date="13 MAYIS 1610", sub="TAÇ", at=("c13s28", "13", -0.1), kind="crown"),
                 dict(x=2400, date="14 MAYIS 1610", sub="HENRI IV · MARIE NAİP", at=("c13s28", "ertesi", -0.1), kind="crowd"),
                 dict(x=3900, date="1617", sub="BLOIS ŞATOSU", at=("c13s29", "Favorisi", -0.1), kind="castle"),
                 dict(x=5400, date="21–22 ŞUBAT 1619", sub="GECE KAÇIŞ", at=("c13s29", "1619'da", -0.2), kind="window", out=("c13s29", "kaçtı.", 0.0)),
                 dict(x=6900, date="10–11 KASIM 1630", sub="ALDATILANLAR GÜNÜ", at=("c13s30", "1630'daki", -0.2), kind="door"),
                 dict(x=8400, date="TEMMUZ 1631", sub="FRANSA'DAN ÇIKTI", at=("c13s31", "1631'de", -0.2), kind="border")],
         cam=[(("c13s28", -0.3), look(900, 560, 1.0)), (("c13s28", "taç", 0.4), look(950, 560, 1.0)), (("c13s28", "ertesi", -0.2), look(2400, 560, 1.0)), (("c13s28", "oldu.", 0.2), look(2450, 560, 1.0)),
              (("c13s29", "Favorisi", -0.2), look(3900, 560, 1.0)), (("c13s29", "gönderildi;", 0.3), look(3950, 560, 1.0)), (("c13s29", "bir", -0.1), look(5400, 560, 1.0)), (("c13s29", "kaçtı.", 0.8), look(5450, 560, 1.0)),
              (("c13s30", "1630'daki", -0.2), look(6900, 560, 1.0)), (("c13s30", "değil.", 0.3), look(6950, 560, 1.0)), (("c13s31", "1631'de", -0.2), look(8400, 560, 1.0)), (("c13s31", "dönmedi.", 0.0), look(8450, 560, 1.0)),
              (("c13s31", "dönmedi.", 1.2), look(9400, 560, 1.0)), (("c13s32", -0.5), look(9450, 560, 1.0))],
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="zaman çizgisi: altı vinyet, iplik çıkar"),

    # ══ V9 · RUBENS'İN YİRMİ DÖRT TABLOSU (s32–s34) ═══════════════════════════════════════
    # 29 · galeriye giriş: girişten uzun dolly; 24 çerçeve
    shot("c13_galeri", ("c13s32", -0.3), cams=[(("c13s32", -0.3), (-600, 0, 1.0)), (("c13s32", "ısmarladı:", 0.0), (900, 0, 1.0)), (("c13s33", -0.4), (1500, 0, 1.0))], mode="day", longtake=True, **D,
         ovl=ov(L.date_plate("26 ŞUBAT 1622", ("c13s32", "1622'de", 0.0)),
                L.count_up(1560, 220, ("c13s32", "yirmi", -0.1), 24, dur=1.0, unit="DEV TABLO", size=130),
                K.frames24(("c13s32", "yirmi", 0.0), x=1560, y=420)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Galerie Médicis: dolly, 24 çerçeve"),
    # 30 · Louvre'a göre: kendi anlatısını sunma fırsatı; ressam kralı gücendirmemeliydi
    shot("p6_quote", ("c13s33", -0.3), text="Marie'ye kendi anlatısını sunma fırsatı", who="LOUVRE", src="çeviri bize ait", mark=False, size=70, wrap=1250, at=("c13s33", "Louvre'a", -0.1),
         mode="day", cam=("push", 0.06), **D,
         ovl=ov(L.tag("RESSAM KRALI GÜCENDİRMEMELİYDİ", 960, 840, ("c13s33", "ressam", -0.1), size=38, w=960), L.icon_at("scales", 1620, 330, ("c13s33", "gücendirmemeye", -0.2), size=170, glow=True, bob=4)),
         tr=("sayfa", 0.9), link="material", label="Louvre: kendi anlatısını sunma"),
    # 31 · Parklar çerçevesinde iplik parlar; Blois çerçevesinde kısa zum; dolly büyük çerçevede durur
    shot("c13_galeri", ("c13s34", -0.3), a_spark=("c13s34", "ipliğini", -0.3),
         cams=[(("c13s34", -0.3), (-90, -190, 1.5)), (("c13s34", "eğirir;", 0.2), (30, -170, 1.45)), (("c13s34", "Blois'dan", -0.2), (1000, 120, 1.15)), (("c13s34", "kahramanca", 0.0), (1300, 190, 1.55)),
               (("c13s35", -0.5), (2900, 0, 1.0))], mode="day", **D,
         ovl=ov(L.tag("LES PARQUES FILANT LE DESTIN", 600, 215, ("c13s34", "Kader", -0.1), size=32, w=700, out=("c13s34", "Blois'dan", -0.2)),
                L.tag("LA REINE S'ENFUIT DU CHÂTEAU DE BLOIS", 1260, 215, ("c13s34", "Blois'dan", -0.1), size=32, w=860)),
         tr=("zoomthru", 0.9, dict(at=(960, 540), at_b=(960, 540))), link="scale", label="Parklar çerçevesi: iplik parlar"),

    # ══ V10 · KÖLN 1642 (s35–s37) ══════════════════════════════════════════════════════════
    # 32 · Paris → Köln çizgisi (iplik biter)
    shot("p6_map", ("c13s35", -0.4), mode="day", cam=("push", 0.03), **D,
         cams=[(("c13s35", -0.4), (4.4, 49.8, 5.2)), (("c13s35", "Köln'de,", -0.6), (5.6, 50.4, 6.6))],
         cities=[dict(lon=2.3522, lat=48.8566, name="PARİS", kind="capital", at=("c13s35", -0.3), size=34, color="#233C8C", side="l"),
                 dict(lon=6.9603, lat=50.9375, name="KÖLN", kind="capital", at=("c13s35", "Köln'de,", -0.9), size=38, color="#B33620", side="r")],
         routes=[dict(pts=[(2.3522, 48.8566), (3.6, 49.5), (5.0, 50.2), (6.9603, 50.9375)], at=("c13s35", -0.2), dur=2.4, color="#8E3342", width=5.0, arrow=False)],
         ovl=L.date_plate("3 TEMMUZ 1642", ("c13s35", "Temmuz", -0.2)),
         tr=("zoomthru", 0.9, dict(at=(960, 470), at_b=(960, 540))), link="scale", label="altın çerçeve → harita (Paris → Köln)"),
    # 33 · Köln: boş oda, pencere ışığı solar, iplik kopar; «Rubens ailesinin evi»; söylendi (sepya), Siegen
    shot("p6_oda", ("c13s35", "Köln'de,", -0.3), room="bos", variant="koln", path="in", fade_at=("c13s35", "yoksul", -0.2), fade_dur=9.0, thread_at=("c13s35", "öldü.", 0.1), tod="day", mode="day", longtake=True, **D,
         ovl=ov(L.desat(("c13s36", "söylendi,", -0.5), ("c13s36", "oysa", 0.0), k_max=0.9, dark=0.0, tint="#B8A078", tint_a=0.18),
                L.tag("RUBENS AİLESİNİN EVİ", 960, 215, ("c13s36", "Rubens", -0.15), size=44, w=760, out=("c13s36", "sonradan", 0.0)),
                L.stamp("SÖYLENDİ", 1500, 360, ("c13s36", "söylendi,", -0.1), size=60, rot=-0.07, out=("c13s36", "oysa", 0.2)),
                L.tag("SIEGEN", 960, 215, ("c13s36", "Siegen'di.", -0.2), size=56, w=420)),
         tr=("zoomthru", 0.9, dict(at=(1100, 560), at_b=(960, 540))), link="scale", label="harita → boş oda (iplik kopar)"),
    # 34 · Tablolar Paris'te kaldı: karanlıkta 24 çerçeve, uzak galeri
    shot("c13_galeri", ("c13s37", -0.3), dark_at=("c13s37", -0.3), cams=[(("c13s37", -0.3), (600, 0, 1.0)), (("c13s37", "galerideler.", 0.0), (-300, 0, 1.0))], mode="night", **D,
         ovl=ov(L.tag("LOUVRE", 960, 215, ("c13s37", "Louvre'da,", -0.2), size=56, w=420), L.tag("AYRI BİR GALERİ", 960, 880, ("c13s37", "ayrı", -0.1), size=40, w=540)),
         tr=("dip", 1.0), link="light", label="karanlıkta 24 çerçeve (Louvre)"),

    # ══ KAPI (s38) — c14'ün üç vuruşu: Arapça harf · opera · gökyüzü ═════════════════════
    # 35 · iki kraliçe imgesini savunurken (madalyalar sönük)
    shot("p6_medals", ("c13s38", -0.2), items=[dict(key="m_catherine_dul", name="CATHERINE", at=("c13s38", "kraliçe", -0.3)), dict(key="m_marie", name="MARIE", at=("c13s38", "kraliçe", -0.1))],
         size=420, mode="night", cam=("push", 0.06), **D,
         ovl=ov(L.dim(("c13s38", -0.2), ("c13s38", "ailenin", -0.3), alpha=0.35, dur=0.6),
                L.tag("İMGE", 960, 215, ("c13s38", "imgesini", -0.15), size=56, w=360, out=("c13s38", "ailenin", -0.2)),
                L.icon_at("shield", 960, 470, ("c13s38", "savunurken,", -0.4), size=170, glow=True, bob=4, out=("c13s38", "ailenin", -0.2))),
         tr=("light", 0.9, dict(at=(960, 540))), link="light", label="iki kraliçe: imge"),
    # 36 · Floransa'daki kol: Arapça harf kestirmek
    shot("c13_harf", ("c13s38", "ailenin", -0.35), a_start=("c13s38", "Arapça", -0.2), step=0.22, letters="ابتثجح", mode="day", cam=("push", 0.05), **D,
         ovl=ov(L.tag("FLORANSA'DAKİ KOL", 960, 215, ("c13s38", "Floransa'daki", -0.15), size=46, w=640, out=("c13s38", "kestirip,", 0.0))),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Arapça harf kestirmek"),
    # 37 · opera sahnelettirip: perde açılır
    shot("p6_oda", ("c13s38", "kestirip,", 0.25), room="perde", path="in", open_at=("c13s38", "kestirip,", 0.3), open_dur=1.4, tod="night", mode="night", cam=("push", 0.04), **D,
         tr=("yikama", 0.8), link="color", label="opera: perde açılır"),
    # 38 · gökyüzüne de adını yazdırıyordu (kapı; ağırlık merkezli kapanış)
    shot("c13_gok", ("c13s38", "gökyüzüne", -0.45), a_moons=("c13s38", "gökyüzüne", -0.3), a_name=("c13s38", "adını", -0.2), mode="night", cam=("push", 0.05), **D,
         tr=("light", 0.9, dict(at=(960, 540))), link="light", label="gökyüzüne MEDİCİ yazılır (kapı)"),
]

YIL_AT = [(("c13s1", "1519'da", -0.2), 1519), (("c13s3", "1533'te", -0.1), 1533), (("c13s7", "1559'da", -0.1), 1559), (("c13s10", "1562", -0.1), 1562), (("c13s11", "1572'de", -0.1), 1572),
          (("c13s16", "1573'te", -0.1), 1573), (("c13s16", "1575'te", -0.1), 1575), (("c13s21", "1581'de", -0.1), 1581), (("c13s22", "1589'da", -0.1), 1589), (("c13s24", "1600'de", -0.1), 1600),
          (("c13s28", "1610'da", -0.1), 1610), (("c13s30", "1630'daki", -0.1), 1630), (("c13s32", "1622'de", -0.1), 1622), (("c13s35", "1642'de", -0.1), 1642)]

OUTRO_TR = ("iris", 1.0, dict(obj="lens", at=(700, 460), r=125))
