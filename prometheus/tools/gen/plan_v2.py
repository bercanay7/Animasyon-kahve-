"""Plan listesi 2. sürüm: animatik kurulunun 1. tur raporlarına (6 üye) göre başkan kararları.
animatik/planlar_v1.json → animatik/planlar.json. Kararların gerekçesi kurul/kararlar.md'de."""
import json, os, re, copy
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
d = json.load(open(os.path.join(ROOT, 'animatik', 'planlar_v1.json')))
P = d['planlar']
ix = lambda pid: next(i for i, x in enumerate(P) if x['id'] == pid)
def up(pid, **kw):
    x = P[ix(pid)]
    for k, v in kw.items():
        if v is None: x.pop(k, None)
        else: x[k] = v
def drop(*pids):
    for pid in pids: P.pop(ix(pid))
def after(pid, new):
    P.insert(ix(pid) + 1, new)

# ---------- genel kurallar ----------
d['_not'] = ("Plan listesi 2. sürüm (animatik kurulu 1. tur sonrası). at: 'ID' cümle başı, 'ID@kelime' kelime, '#n' n. geçiş, "
  "'ID-1.8' kaydırma. k: S siyah figür (Hesiodos), K kırmızı figür (Aiskhylos), B beyaz zemin (Erhat). kit: üretim kiti. "
  "Kurallar: (1) Tek cümlelik Erhat yorumu = kenar şeridi (o anki katman yerinde kalır); tam sayfa beyaz zemin yalnız çok cümlelik öbeklerde. "
  "(2) Tam sayfa alıntı en çok 5: P181, P241, P263, P282, P288; öbür Erhat sözleri 2–4 kelimelik anahtar söz + 'ERHAT · s. x' köşe etiketi. "
  "(3) Telefon kuralı: yüz, ateş, gaga ve yazı y ≤ 700, x 96–1824; alt bant altyazıya ve oynatıcıya ayrılır. Alıntı ≥ 76 px, kaynak ≥ 40 px, okunacak dipinto cap ≥ 90 px. "
  "(4) Yazılar üst katmanda (over) çizilir: hareket bulanıklığı, sarsıntı ve dönüşe girmez. "
  "(5) Söz görünür: Prometheus'un sözü ağzından akan harfler (yalnız 8 anahtar dize Türkçe; öbürleri süs Yunan harf akışı), Güç'ün sözü kil levhaya kazınır, Hermes'in sözü mühür, sessizlikte harf yok. "
  "(6) Zeus kırmızı figür katmanında hiç görünmez: yalnız boş taht, gölge, buluttan uzanan soğuk beyaz kelepçeli bilek. Siyah figür (Hesiodos) katmanında ikonografik Zeus görünür. "
  "(7) Renk: altın = ateş ve akıl; soğuk beyaz (#E6ECFF) = Zeus ve yıldırım; karaciğer = kırmızı; umut = soluk, soğuk, küçük ışık. "
  "(8) Geçiş dilbilgisi: S'ye giriş kil, K'ye giriş sır akışı, B'ye giriş mürekkep; B'den hikâyeye dönüş sert ya da eşleşen kesme; bölüm kartı kil levha (sallanarak iner) ve sorudan 1,8 sn önce, sessizlikte; negatif geçiş yalnız kartal bağında (P006, P250). Yumuşak geçiş çapada BİTER (önceki sessizlikte oynar). "
  "(9) Her kitin taban hareketi otomatik eklenir (taban alanı); 'hareket' alanı olay katmanını yazar. Hiçbir kare donmaz. "
  "(10) Jest bilgi taşıyorsa figür kadraj boyunun ≥ %45'i; geniş planlarda bir katman büyük ölçekli olur (kamera ya da ışık). Flaşlar saniyede ≤ 3.")
d['setler'] = {
  'KAYA': "Kırmızı figür dikey dünya: Olympos tahtı (y≈−2200), bulut kuşağı (−1400…−700), İskit kayası ve zincirli Prometheus (0…1080), altında ova ve insanların ateşleri. Kameralar: GENİŞ, ORTA, YAKIN, ALT, ÜST, ZİNCİR, GÖZ→TONDO; alt kameralar OVA, MAĞARA, DENİZ, FIRTINA, OLYMPOS. Zincir P005, P158, P237, P240, P242'de aynı dünyada yalnız kamera konumudur. Kartal bu sette yaklaşan tehdittir (Hermes'in tehdidi). Bölüm saati: güneş V'te sabah, VII ikindi, VIII gün batımı, IX donma, X fırtına gecesi.",
  'TONDO': "kylix() tondosu S ya da K paletiyle: Lakonya kylixi (A03), madalyonlar (hatıra; Aiskhylos'un anlatısıysa K), iki tabak (F02), dünya diski, gözden dalılan görüntüler (GÖZ→TONDO: siyah göz bebeği tondonun siyah zeminine açılır).",
  'SAYFA': "Beyaz zemin yaşayan sayfa: bir Erhat öbeği tek ve uzun bir sayfadır, plan sınırları kameranın duraklarıdır (kesme yok). Türevleri: MASA (çevirmenlerin masası, lamba), GALERİ, BÖLÜNMÜŞ (levha içinde levha), kenar şeridi (tek cümlelik yorum).",
  'AMFORA': "Siyah figür dönen amfora frizi: soy ağacı ve devrimler (C), İapetos soyu (D), Herakles (L). Dönüş durak durak kelimelere bağlı; dönüşün kendisi geçiştir.",
  'METOP': "Siyah figür tek uzun metop frizi (Mekone, rezene, Pandora, küp): kamera pano pano kayar.",
  'TAHT': "Tek ve sabit nesne: üç taht x 560/960/1360, taban y 760, dipinto ΟΥΡΑΝΟΣ / ΚΡΟΝΟΣ / ΖΕΥΣ. Durum anlatıcıyı söyler: S'de Zeus'un tahtı sağlam; B'de E16'dan sonra kaidede ayakta bir insan; K'de çatlak ve titrek. Üçüncü taht filmde hiç devrilmez (yalnız I06'da soluk bir görüntü).",
  'ŞERİT': "Tek yatay friz, kamera kayar: uygarlık armağanları (G10b, her armağan bir pano), İo'nun soyu (H10), okçu, harita (sade vazo haritası), meşale koşusu (L).",
  'TİYATRO': "Dionysos tiyatrosu (akşam, gündüz, modern sahne): skene dekoru KAYA'nın kayası ve zincirli figür.",
  'BİTİŞ': "Bitiş ekranı: Sisifos çerçevesi (video öğesi x 150–870, y 180–585), abone alanı (x 1250–1650, y 230–630); son 20 sn.",
}
d['taban'] = {'KAYA': 'rüzgâr (saç, sakal, zincir), akan dalga kuşağı, ateş titremesi, ≥ 2–3 px/sn itme', 'SAYFA': 'kâğıt nefesi (±%0,4), 4 px/sn kayma, lamba ışığı titremesi, kalem ucu',
  'AMFORA': 'silindir dönüşü ve gövdede kayan parlama, toz zerreleri', 'METOP': '1–2 px/sn kamera sürünmesi, duman', 'TAHT': 'toz zerreleri, mürekkep sızması',
  'TONDO': 'kupa dönüşü', 'ŞERİT': 'kaydırma', 'TİYATRO': 'meşale titremesi, kalabalıkta kıpırtı', 'BİTİŞ': 'Sisifos döngüsü, alev'}
KIT = {'KAYA': 'KAYA', 'OVA': 'KAYA', 'MAĞARA': 'KAYA', 'OLYMPOS': 'KAYA', 'YAKIN': 'KAYA', 'LEVHA': 'KAYA', 'BAŞLIK': 'KAYA', 'DÜNYA DİSKİ': 'TONDO',
  'MADALYON': 'TONDO', 'İKİ TABAK': 'TONDO', 'KYLIX': 'TONDO', 'SOFRA': 'TONDO', 'SAYFA': 'SAYFA', 'MASA': 'SAYFA', 'GALERİ': 'SAYFA', 'BÖLÜNMÜŞ': 'SAYFA',
  'FRİZ': 'ŞERİT', 'HARİTA': 'ŞERİT', 'MEŞALE': 'ŞERİT', 'TİYATRO': 'TİYATRO', 'SAHNE': 'TİYATRO', 'ATÖLYE': 'METOP', 'METOP': 'METOP', 'AMFORA': 'AMFORA',
  'TAHT': 'TAHT', 'BİTİŞ': 'BİTİŞ'}

# ---------- açılış (A) ----------
up('P001', kare="KAPAK KARESİ, kararma yok. Gece; Prometheus profilden Olympos'tan iner, kaldırdığı rezene sapının ucunda alev (karenin tek parlak noktası). İlk ses: zincir şakırtısı.", gecis=None,
   hareket="A01@bile: koşarken baş omzun üstünden Olympos'a döner (gövde ileri, baş geri); A01@insanlara: kamera aşağıdaki ovaya iner, ocaklar sırayla yanar; A01@titan: kamera geri çıkar, ateşi kaldırmış Titan'ın yakın planı (tek sürekli plan, P001–P003).")
drop('P002', 'P003')
up('P004', at='A01+5.8', kare="ZİNCİR: çekiç kazığa iner, bilekteki halka kapanır (ilk vuruş A01 ile A02 arasındaki sessizlikte); kamera geri çekilir: kayaya mıhlı Prometheus. İkinci vuruş A02@mıhlatan'da.",
   hareket="çekiç, kıvılcım, toz, 0,15 sn beyaz çakma; ikinci vuruşta kamera bir kademe geri", gecis='kesme')
up('P005', kare="Kamera bilekten zinciri bulutlara kadar izler; A02@asıl'da zincir yukarıdan bir kez gerilir, bulutların arasında soğuk beyaz bir kelepçe pırıltısı (açılmaz; P237'nin kurulumu).", hareket="yukarı çevrinme; zincir gerilir, bulut akar, uzak şimşek")
for pid in ['P006', 'P007', 'P008', 'P009', 'P010']: up(pid, kit='TONDO')
up('P006', kare="Lakonya kylixi (siyah figür, Hesiodos): tek sürekli tondo planı. Sütuna bağlı Prometheus; güneş diski.", hareket="A03@kartal: kartal güneşten iner; @karaciğerini: göğse konar, kanatlarıyla örter; @gece: kupa döner, tondo kararır, böğürde altın ışık; @sabah: şafak, kartal yeniden; sonda kamera kartalın gözüne dalar.", gecis='negatif 0,8 sn')
drop('P007', 'P008', 'P009', 'P010')
up('P011', kare="Eşleşen kesme: kartal gözünün siyahı başlığın siyah sırrı olur. Vazo yazısı ΠΡΟΜΗΘΕΥΣ fırça çizgisiyle yazılır, Θ'nın içinden geri çekilme; harfler ateş alıp PROMETHEUS'a dönüşür; arkada zincirli siluet.")
up('P012', at='A06', kare="Beyaz zemin: kitap kapağı (Aiskhylos · Zincire Vurulmuş Prometheus), ortasında zincirli Prometheus'un küçük kırmızı figür levhası (vinyet; zincire asılmayı sürdürür).", yazi='AZRA ERHAT · 1967', gecis='mürekkep 0,5 sn (çapada biter)',
   hareket="A06@bin: kapağa 1967 damgası vurur; A06@oyunun: kapak açılır, ÖNSÖZ sayfası; vinyet sayfanın sol kenarında sürer")
drop('P013')
up('P014', kare="Sayfada vinyetin zinciri taşar, soru işaretine kıvrılır ve sayfanın üst kenarından çıkar: öbür ucu görünmez (taht yok).", yazi=None, hareket="zincir halka halka çizilir; soru işaretinin noktası kırmızı")
up('P015', at='A05@ve', kit='KAYA', set='KAYA/OVA', kare="Karanlıkta küçük bir alev; başında oturan bir ölümlü (siluet ölçeğinde, el yakın planı yok). Kamera yukarı kalkınca karanlıktan dev, boş bir taht belirir: öfkenin ölçüsüzlüğü.", hareket="A05@öfkelendiren: gökte soğuk şimşek titrer; A05@avuç: kamera aleve iner, alev nabız gibi atar; konuşma bitince kıvılcım yükselip bölüm levhasına dönüşür", gecis='mürekkepten dönüş: sert kesme')

# ---------- I (B) ----------
up('P016', at='B01-1.8', kare="Akşamüstü Dionysos tiyatrosu; skene dekoru KAYA'nın kayası ve zincirli figür, üstünde tanrı maskeleri. Bölüm levhası sessizlikte sallanarak iner.", hareket="eşleşen kesme: P015'in yükselen kıvılcımı tiyatronun üstündeki akşam yıldızı olur; vinç hareketi; B01@insanı: tanrı maskeleri arasında tek insan maskesi meşale ışığıyla yanar", gecis='kil levha')
up('P019', kit='SAYFA', hareket="tek sürekli sayfa (P019–P023): maske insan profiline döner; kamera durağa kayar")
up('P020', yazi='“İnsan dostu, tanrı düşmanı” · s. v', hareket="Prometheus insana doğru ~400 px yürür (jest büyük ölçekli)")
up('P023', yazi='NASIL?', hareket="harfler mürekkeple dolar; kalem daire çizer; kart sayfaya iğnelenir (P109, P157, P216 köşelerinde küçük olarak geri gelir)")
up('P024', gecis='kil 1,0 sn (çapada biter)')

# ---------- II (C) ----------
up('P025', at='C01-1.8', kit='TAHT', gecis='kil levha', kare="Olympos'un tepesinde boş, görkemli taht (siyah figür, TAHT nesnesi). Bölüm levhası sessizlikte.")
up('P026', kit='KAYA', set='KAYA/YAKIN', kare="Kayadaki Prometheus'un profil büstü; bakış çizgisi yönünde gökte tahtın soluk görüntüsü (göz makro yok).")
up('P027', k='S', kit='AMFORA', set='AMFORA', kare="Amforada bir figür tahtı ötekinin altından çeker (darbe). Kenar şeridi: “hükümet darbesi” · s. vi.", gecis='kil 0,6 sn', yazi='kenar şeridi: “hükümet darbesi” · s. vi')
up('P028', gecis=None, kare="Aynı amforada üç kuşak basamak basamak: her kuşak bir basamak yukarıda belirir, önceki geriye devrilir (temas yok).", hareket="C02@devirip: devrilme")
up('P029', kare="Amforada asalı bir rapsod: Hesiodos. Ağzından çıkan dipinto girdaba dönüşüp Khaos'a bağlanır.", yazi=None, hareket="C04@kaos: söz girdaba dönüşür; amfora döner")
up('P039', k='S', kit='AMFORA', set='AMFORA', kare="Amforada gök yerden kopmuş, Uranos'un tahtı devrik. Kenar şeridi: DEVRİM · s. vii (şeritte küçük taht devrilir).", gecis=None, yazi='kenar şeridi: DEVRİM · s. vii')
up('P040', gecis=None)
up('P044', at='C10@o#1', kare="Mağara ağzında parlayan kundak; iki kalkan diski çarpışır (Kuretler seste); keçi silueti.", hareket="kalkan çarpışması; kundağın ışıltısı")
up('P046', hareket="C12@birincisi: sol kefeye tırpan iner; C12@ikincisi: sağ kefeye kundak taşı; C12@akılla: terazi akla eğilir (tek sürekli sayfa P046–P048)", yazi='“kaba kuvvetin akılla yenilmesi” · s. viii')
up('P047', k='B', set='SAYFA', kit='SAYFA', kare="Sayfaya yapıştırılmış siyah figür madalyon: yaşlı Uranos ve Gaia genç Zeus'a öğüt verir.", gecis=None)
up('P048', yazi='ERHAT · s. viii', kare="Kenar frizinde Zeus'un arkasındaki kalabalıkta küçük bir figür; Erhat'ın kalemi onu daire içine alır; C14@prometeus'ta kamera figüre iter (figür ≥ %45 boy).", gecis=None)
up('P049', gecis='sert kesme', kare="Kayada Prometheus'un kapalı dudakları (profil büst); geri çekilme: 'kendi ağzından duyacağız'.")
up('P050', kare="Titanomakhia: karşılıklı iki kalkan sırası (aynı siluetin kopyaları, izosefali, faz kaydırmalı nefes).", hareket="C17@yüz: amforanın dibindeki ışın bandı kollara dönüşüp yükselir, kaya fırlatır; sarsıntı")
up('P052', k='S', kit='AMFORA', set='AMFORA', kare="Savaş alanı boşalır; kenar şeridi: 'geriye yalnız AKIL kaldı' · s. viii.", gecis=None, yazi='kenar şeridi: “geriye yalnız AKIL kaldı” · s. viii')
up('P055', at='C18@tek', hareket="C18@prometeus: yolun ortasında figür belirir, haritanın gölgesi ona çarpıp ikiye ayrılır")
up('P053', gecis=None, kare="Zeus elinde yıldırımla tahta oturur (siyah figür, ikonografik); C17@paylaştırmaya: dünya diski dilimlere ayrılır.")

# ---------- III (D) ----------
up('P056', at='D01-1.8', gecis='kil levha', kit='TONDO')
up('P057', kit='AMFORA', hareket="her ad söylendiğinde figür ve dipinto belirir (atlas, menoitios, prometeus, epimeteus); amfora döner")
for pid in ['P058', 'P059', 'P061']: up(pid, kit='TONDO')
up('P062', kare="Peçeli bir kadın silueti kucağında küçük bir küple Epimetheus'a doğru kayar; D04@armağan'da kurdele görünür, küpün kapağı titrer.", yazi=None)
up('P063', k='S', kit='AMFORA', set='AMFORA', kare="Amforada dört kardeş, başlarının üstünde kıvılcım; kenar şeridi: Erhat'ın sorusu 'Titan oldukları için mi?' · s. ix.", gecis=None, yazi=None)
up('P063b', k='S', kit='AMFORA', set='AMFORA', kare="D05@hayır: şeritte 'TİTAN' üstü çizilir, yerine 'ZEKÂ' yazılır; kıvılcımlar parlar.")
up('P064', k='S', kit='TAHT', set='TAHT', kare="Tahtta Zeus'un kapalı yumruğunda tek kıvılcım (tekel). Kenar şeridi: “Akıl gücüyse Zeus'un tekelindedir” · s. ix.", gecis=None, yazi='kenar şeridi')
up('P065', k='S', kit='TAHT', set='TAHT', kare="Başka bir yerde Prometheus'un başında ikinci kıvılcım; tahttaki siluetten koyu duman kaynar (dinmez öfke).", yazi=None)
up('P066', hareket="D08@geleceği: Prometheus'un gözünde bir kıvılcım yanar (P069'u önceden kurar); alttan çevrinme")
up('P067', kare="Tek METOP frizi, üç pano art arda tam kare (her birinde tek büyük eylem): D08@aldatır el çabukluğu (paylar yer değiştirir), D08@tedirgin Zeus omzunun üstünden bakar, D08@gülünç Zeus'un çelengi yan yatar, tanrı siluetlerinde omuz sarsıntısı; sonda kamera geri çekilip üç panoyu yan yana gösterir.")
up('P068', k='S', kit='AMFORA', set='AMFORA', kare="Amforadaki ΠΡΟΜΗΘΕΥΣ yazısı ΠΡΟ · ΜΗΘΕΥΣ diye ayrılır; altında 'önceden düşünen'.", gecis=None, yazi='PRO · METHEUS = önceden düşünen')
up('P069', kit='TONDO', set='GÖZ→TONDO', kare="Prometheus'un gözüne dalılır; göz bebeğinin siyahı bir tondoya açılır: düşen bir taht.")
up('P071', k='S', kit='TAHT', set='TAHT', kare="TAHT nesnesi: iki taht devrik, üçüncüsünde çatlak; kenar şeridi: “Üçüncü devrimin hazırlanması.” · s. x.", gecis=None, yazi='kenar şeridi')
up('P072', kare="TAHT nesnesi, tek kamera hareketi: devrik iki tahtın boyunca kayar.", hareket="D11@devrilmişti#0 ve #1'de toz savrulur; üçüncüde durur", gecis='sert kesme')
drop('P073')
up('P074', kare="Üçüncü taht (Zeus) devrilmez, titrer; kamera çok yavaş yaklaşır; üçüncü vuruş gelmez, sessizlik.")

# ---------- IV (E) ----------
up('P075', at='E01-1.8', gecis='kil levha', hareket="levha kalkınca E01@neden'de kamera ziyafet frizinden sunağa kayar; E01@kemikleri'de kemik dumanı göğe, tanrıların burnuna yükselir")
up('P079', kare="İki pay yan yana: biri çirkin işkembe torbası, öbürü parlak yağa sarılı; siyah figür kazıması yağı kazır, altındaki kemik görünür (röntgen yok).")
up('P086', kare="Zeus'un pelerininin gölgesi (koyu bulut) insan köyünün üstünden geçer; ocaklar gölgenin kenarı değdikçe söner, sonuncusu E09@ateşi'de.")
up('P087', kare="Olympos'taki tanrı ocağında Prometheus rezene sapını közün üstüne indirir (E10@rezene); tırmanma yok.", hareket="köz parlar; sap tutuşur")
up('P088', k='S', kit='METOP', set='METOP', kare="KAPAK KARESİNİN SİYAH FİGÜR EŞİ: rezene sapıyla dağdan aşağı koşar; giriş ve çıkış sert kesme (P087 ile tek plan).", gecis='sert kesme')
up('P094', kare="Epimetheus kollarını açar (temas yok); 'iş işten geçince' başı geriye, arkasına döner: sonradan düşünen arkasına bakar.")
up('P097', kare="Kapak kapanır; küpün dibinde küçük, soluk, soğuk bir ışık: ELPİS (umut). Bu ışığın biçimi P165, P198, P286'da aynıdır.")
up('P098', k='S', kit='METOP', set='METOP', kare="Metopta iki kez aldatılmış Zeus; kenar şeridi: 'kaba kuvvet' · s. x (şeritte ağır bir yumruk simgesi).", gecis=None, yazi='kenar şeridi: kaba kuvvet')
up('P099', k='B', kit='SAYFA', set='SAYFA', kare="Beyaz zemin öbeği başlar (E15–E16): sayfada siyah figür bir iç kare: asalı rapsod Hesiodos Zeus'u över.", gecis='mürekkep 0,6 sn (çapada biter)')
up('P100', gecis=None)
up('P102', hareket="kıvılcım tanrıların katından insanların başlarına iner; alıntının bütün satırları aynı anda belirir ve P103'ün ilk saniyesine taşar")
up('P103', kare="TAHT nesnesi (B): taht devrilmez; E16@üçüncü'de tahtın önünde bir insan figürü doğrulur, E16@insan'da figürün gölgesi büyüyüp tahtı örter; taht yerinde ama içi boş.", gecis=None)
up('P104', k='B', kit='SAYFA', set='SAYFA', kare="Aynı sayfada insan figürü ateşin ışığında kendi ellerine bakar (büyük ölçek).", gecis=None)
up('P105', k='K', kit='KAYA', kare="P015'in alevi aynı kadrajda büyür; boş taht geride kararır; alevin içinde uygarlık frizinin (ŞERİT) maskeli önizlemesi döner.", gecis='sert kesme (eşleşen: P015)')
up('P106', kare="Eşleşen sert kesme: P105'teki alevden zincirin ilk halkasının parıltısına; zincir yukarı, kadraj dışına; bir tragedya maskesi belirir.", gecis='sert kesme')

# ---------- V (F) ----------
up('P107', at='F01-1.8', gecis='kil levha', kare="P106'daki maskeden geri çekilerek gündüz Atina tiyatrosu açılır (P016'nın ters hareketi). Bölüm levhası sessizlikte.")
up('P108', kit='TONDO', hareket="F02@büsbütün'de tabaktaki Prometheus figürlerine itme; figürler dönüşür")
up('P109', kare="Sayfanın sol üstünde P023'ün NASIL? kartı soluk ve iğneli durur; F03@öbür'de kamera kısa bir süre karta kayar, sonra sağda ikinci soru yazılır.", yazi='“Prometheus ne bakımdan insandır?” · s. xi')
up('P112', gecis='sert kesme (sır akışı olmadan; mahkeme şeridi iner)')
up('P114', hareket="şimşek titremesi; boş taht KAYA/EKSEN ön ayarında (taht 1160,170; sanık 760,820): bu eksen P158, P211, P217, P237'de aynen kullanılır")
up('P116', kare="Vazo alayı uylaşımı: üç figür soldan sağa profilden yürür; Prometheus ortada, zinciri iki uşağın elinden bileğine gergin; figürler birbirine değmez.")
up('P118', yazi='POLİS (mühür)')
up('P119', yazi=None, kare="Kratos parmağıyla gösterir; süs Yunan harf akışı (Türkçe cümle yok).")
up('P124', yazi=None, kare="Hephaistos'un sözü kil levhaya hafifçe kazınır gibi belirip söner (Türkçe metin yok); çekiç iner.")
up('P126', yazi="“Zeus'tan başka hiç kimse özgür değildir.” (kil levhaya kazınır, ≥ 60 px)", kare="Kratos'un soğuk profili alttan; sözü kil levhaya kazınır (Güç'ün sözü = taş).")
up('P127', set='KAYA/LEVHA', kit='KAYA')
up('P128', k='K', kit='KAYA', set='KAYA', kare="Kayada zincirli Prometheus; kenar şeridi: 'özgürlük · kölelik' · s. xiii (şeritte terazi; P046 ve P154 ile aynı çizim).", gecis=None, yazi='kenar şeridi: özgürlük · kölelik')
up('P129', gecis='mürekkep 0,6 sn (çapada biter)')
up('P130', gecis="eşleşen sert kesme: kölenin prangası → Prometheus'un kelepçesi", yazi=None, kare="Prometheus'un zincirli bilekleri; halkaya kazınmış ΔΕΣΜΩΤΗΣ yalnız doku.")
up('P132', k='K', kit='KAYA', set='KAYA', kare="Kayada önceki sahneyi geri saran küçük panolar kenar şeridinde: öbür figürlerin ağzından söz akar, Prometheus'un söz bandı boş; F10b@tek'te boşluk kırmızıyla daire içine alınır. Şerit: 'Dikkat ettin mi?' · s. xi.", gecis=None, yazi='kenar şeridi: Dikkat ettin mi?')
up('P133', kare="ZİNCİR: P004'ün birebir kompozisyonu; iki vuruş F10b@indi#0 ve F10b@indi#1'de (0,15 sn beyaz çakma), her vuruşta kamera bir kademe yaklaşır; ikincide kıvılcım ve toz büyür: izleyici açılıştaki anın bu an olduğunu anlar.", gecis='sert kesme')
drop('P134')
up('P136', hareket="çıkış yürüyüşleri; geri çekilme (geniş planda büyük ölçekli kamera hareketi), rüzgâr")
up('P138', kare="Tek sürekli panorama (P138–P142): F13@ey'de ağzından göğe kil renkli söz akar: EY KUTSAL GÖK.", hareket="F13@hızlı: rüzgâr çizgileri kanat biçimli yaylara dönüşüp bulutları sürer; F13@ırmakların: kayadan inen su çizgileri; F13@deniz: karenin kendi alt dalga bordürü pırıl pırıl 'güler'; F13@sen: kayanın dibi; F13@bakın: kayadan yüze çıkış")
drop('P139', 'P140', 'P141', 'P142')
up('P144', kare="İç ses kuralı başlar: F14@ama'da rüzgâr birden durur (filmin tek rüzgârsız ~19 sn'si); en yakın büst; arka plan sır siyahına koyulaşır; yalnız nefes.")
up('P145', set='KAYA/YAKIN', kare="Profilin arkasında, bakış çizgisi yönünde gökte soluk kırmızı figür siluetler geçer: kartal, fırtına, okçu (gözbebeği yok).")
up('P146', at='F14@bana#1', kare="ORTA'dan GENİŞ'e geri çekilme; başını eğer, kabullenir.", hareket="F14@zorunluluğun: zincirler gevşer")
up('P147', set='KAYA/ORTA', kare="Ağız animasyonu yok: F14@susabiliyorum'da ağızdan çıkan yazı yarım kalır, F14@konuşabiliyorum'da rüzgârsız havada dağılır; F14 bittikten ~1 sn sonra rüzgâr geri gelir.")

# ---------- VI (G) ----------
up('P148', at='G01-1.8', gecis='kil levha', set='KAYA/ALT')
up('P149', k='K', kit='KAYA', set='KAYA', kare="Kayada mahkeme şeridi; kenar şeridi: 'bilinç · özgürlük' · s. xi (şeritte iki sütun).", gecis=None, yazi='kenar şeridi: bilinç · özgürlük')
up('P150', k='K', kit='KAYA', set='KAYA', kare="Sanık başını kaldırır; iki kavram şeridin sütunlarında parlar.")
up('P151', kare="Okeanos'un kızları alttaki dalga kuşağından yükselir (x 160–620, y 360–690).", gecis='sert kesme')
up('P153', kit='TONDO', set='MADALYON (K)')
up('P155', k='K', kit='TONDO', set='MADALYON (K)', kare="Kırmızı figür hatıra tondosu: Titanlar sırtlarını döner; Prometheus Zeus'un yanına yürür (Zeus yüzsüz, sırtı dönük siluet).")
up('P156', k='K', kit='TONDO', set='MADALYON (K)', kare="Tondoda Kronos Tartaros'a batar; Prometheus fısıldar.")
up('P157', k='K', kit='TONDO', set='MADALYON (K)', kare="Tondodaki figürün çevresine kalemle daire (P048'in geri çağrısı); köşede küçük iğneli NASIL? kartı; kenar şeridi: 'o rol, işte buydu' · s. viii.", gecis=None)
up('P158', kare="Bileğinden yükselen zincir bulutlara girer; G06@zincirindeydi'de bulutlar kapanır, P005'teki soğuk pırıltı görünür; uç görünmez (taht yok).", gecis='sert kesme')
up('P159', yazi='“Zorbalığın bir hastalığı vardır: dostlarına güvenmez.”', kare="Boş tahtın çevresinde karanlıkta kısılan gözler (kuşku); Prometheus'un sözü ağzından akar.")
up('P160', k='K', kit='TONDO', set='MADALYON (K)', kare="Kırmızı figür tondo: küçük insanlar; G07@yok'ta vazo ressamının ıslak süngeri gibi bir mürekkep silme maskesi geçer, G07@yeni'de yeni kil figürler belirir (el yok).")
up('P161', k='K', kit='TONDO', set='MADALYON (K)')
up('P163', kare="Kamera geriye ve yukarıya, ÜST açıya (kartal bakışı) çekilir; periler kadrajdan çıkar: izleyici acımayı reddeden tanrının bakış yerine geçer.")
up('P164', kare="Her insanın arkasında küçük bir ölüm gölgesi; G08@ölümlerini'de ateşten bir ışık süpürmesi gölgeleri siler (el yok).")
up('P165', kare="Göğüslerine küçük, soluk, soğuk ışıklar yerleşir (ELPİS ışığıyla aynı biçim).")
up('P167', kare="Erhat'ın sorusu sayfada; rezene alevi kâğıdı yakar, yanık delikten P169'un uygarlık frizi görünür (bu, geçişin kendisidir).", yazi='“Ateşi tanrılardan çalıp insanlara vermek ne demektir?” · s. xi')
up('P169', gecis='yanık delikten geçiş')
up('P170', hareket="G10b@gözleri: tek bir başa ≥ 450 px kesme, boş göz; G10b@prometeus'ta mağaraya ışık girer, görmeyen gözler parlar")
# G10b: her armağan bir pano, tek ŞERİT, montaj bayrağı
gifts = [('P171', 'yıldızları', 'Takımyıldız çizgileri bağlanır (göz yıldızlara eşleşir).'), ('P171b', 'sayıları', 'Çakıl sayıları: •, ••, ••• (Attika rakamları Ι ΙΙ ΙΙΙ Π Δ yalnız doku).'),
         ('P173', 'harfleri', 'Balmumu tablete harfler kendiliğinden kazınır: Α Β Γ Δ (el yok).'), ('P174', 'hayvanları', 'Boyunduruklu öküz saban çeker (tek büyük siluet).'),
         ('P174b', 'gemiyi', 'Yelkenli dalgada (tek büyük siluet).'), ('P176', 'ilacı', 'Bir ot demeti ve şifalı yaprak (tek simge).'), ('P176b', 'madenleri', 'Örsün üstünde kıvılcım.')]
for pid, w, kare in gifts:
    if pid in [x['id'] for x in P]: up(pid, at=f'G10b@{w}', kare=kare, montaj=True, kit='ŞERİT', set='ŞERİT', yazi=None, hareket='kamera bir pano kayar; simge ≥ %50 boy, merkez (960,470)')
    else: after({'P171b': 'P171', 'P174b': 'P174', 'P176b': 'P176'}[pid], {'id': pid, 'at': f'G10b@{w}', 'k': 'K', 'set': 'ŞERİT', 'kit': 'ŞERİT', 'kare': kare, 'hareket': 'kamera bir pano kayar; simge ≥ %50 boy, merkez (960,470)', 'montaj': True})
up('P178', kare="Geri çekilme: yedi panonun tek bir frizin yan yana kareleri olduğu görülür; başında Prometheus'un ateşi.")
up('P179', gecis='sert kesme')
up('P180', yazi='“İsteyerek, isteyerek suç işledim.”')
up('P181', yazi="“Ne yaptımsa bile bile yaptım.” · s. xi (daktilo ≥ 64 px, G11@ne'ye kadar biter)", gecis='mürekkep 0,5 sn (çapada biter)')
up('P182', gecis='sert kesme', yazi=None)
up('P183b', hareket="figürün kil kenarları rüzgârda toz olup kopar (siluetten kil tozu parçacıkları); nefes")
up('P184', set='KAYA/YAKIN', kare="Bölünmüş kare yerine P145'in soluk görüntüleri bu kez dolu ve ağır geri gelir: bilmek soluk, yaşamak dolu.")
up('P185', at='G13b@yine', kare="Sessizlikte üslup karesinin gerilme döngüsü: ayak ileri basar, zincir gerilir, kazıktan toz dökülür ('geri adım atmaz').")

# ---------- VII (H) ----------
up('P186', at='H01-1.8', gecis='kil levha')
up('P187', yazi='kurbanlar · uşaklar · dalkavuk')
up('P189', yazi="“Tek başkaldıran Prometheus'tur.” · s. xiii (≥ 4 sn, H02@sırada'ya kadar)")
up('P190', kare="Mahkeme şeridine TANIKLAR listesi iner: KRATOS ✓ · BİA ✓ · HEPHAİSTOS ✓ · OKEANOS · PERİLER · İO (İo'nun yanında soru işaretli boynuz simgesi); tanıklar sırayla işaretlenir (P191, P195, P200).")
up('P191', kare="Okeanos balık kuyruklu, yaşlı bir deniz tanrısıdır (Sophilos deinosu): alttaki dalga kuşağından H04@okeanos'ta yükselir.", gecis='sert kesme')
up('P192', yazi=None)
up('P194', kare="Okeanos rahatlamış, dalgaya geri batar (H04@kendi#1).")
up('P195', yazi='agan eleutherostomeis · “dilin fazla özgür” · s. xiii')
up('P196', k='K', kit='KAYA', set='KAYA', kare="Kayada figürün çevresinde 'GURUR? KİBİR?' etiketleri kenar şeridinde belirir, üstleri çizilir.", gecis=None, yazi='kenar şeridi: “hiçbir umuda yer vermeden” · s. xii')
up('P197', k='K', kit='KAYA', set='KAYA', kare="Şeritte BİLİNÇ parlar; ağzından çıkan söz zinciri çözülür.")
up('P198', gecis='sert kesme', kare="Ovada göğüslerinde ELPİS biçiminde soluk umut ışıklarıyla insanlar.")
up('P199', kare="Göğsünde ışık olmayan tek figür: Prometheus; onu yalnız ovadaki ateşlerin yansıması aydınlatır; gözleri açık, geleceği görüyor.")
up('P201', kit='TONDO', set='MADALYON (K)', kare="Madalyon kadraj boyunun ≥ %80'i: gözlü bir bulut (Zeus'un arzusu) ve Hera'nın tavus gözleri.")
up('P202', kit='TONDO', set='DÜNYA DİSKİ', kare="Atsineği İo'yu kupanın kenarında, dünya diskinin çevresinde kovalar; atsineği parlak bir iz çizgisiyle görünür.")
up('P203', kit='ŞERİT', kare="Sade vazo haritası: iki büyük deniz lekesi ve iki boğaz yarığı; İo'nun yolu ≥ 10 px parlak çizgi, ucunda İo'nun başı ilerler.", yazi=None)
up('P204', kit='ŞERİT', kare="İnek (≥ %25 boy) boğazı yüzerek geçer; ad bölünür: BOS · POROS.", yazi='BOS · POROS = inek geçidi (y ≤ 300, ≥ 64 px)')
up('P205', kit='ŞERİT', kare="Kerç'e sıkı kadraj (boğaz genişliğin ≥ %30'u).", yazi='Kerç Boğazı')
up('P206', kit='ŞERİT', kare="Kesme (kaydırma değil): İstanbul'a ayrı sıkı kadraj ve kendi ineği.", yazi='İstanbul Boğazı')
up('P208', kare="Söz: 'Ben ölemem bile.' H09@işkencem'de kartal gölgesi yok: yukarıda boş tahtın ilk çatlağı (H09@yıkılmadıkça).", yazi='“Ben ölemem bile.”')
up('P209', kit='ŞERİT', gecis='eşleşen kesme: zincir halkaları → 13 kuşağın koştuğu meander şeridi')
up('P210', kit='ŞERİT', kare="On üçüncü figür: aslan postlu okçu yayını gerer; kare donmaz: yay gerili kalır, kiriş titrer, post dalgalanır, kamera ok ucuna yaklaşır.")

# ---------- VIII (I) ----------
up('P211', at='I01-1.8', gecis='kil levha', set='KAYA/ÜST')
up('P212', kare="Prometheus'un dudakları kapalı, profil büst; önlerinde soğuk beyaz bir mühür parlar.")
up('P215', kare="TAHT nesnesi (S): Uranos'un ve Kronos'un tahtları devrik; Zeus'un gölgesi bir beşiğin üstüne düşer.")
up('P216', k='S', kit='TAHT', set='TAHT', kare="Aynı kompozisyonda katman içi teknik değişimi (kil → kâğıt); kenar şeridi: 'üçüncü devrimin hazırlanması' · s. x; köşede küçük NASIL? kartı.", gecis=None)
up('P217', gecis='sert kesme')
up('P218', kit='TONDO', set='GÖZ→TONDO', kare="Prometheus'un gözüne dalılır; tondoda mühürlü bir ad (okunmaz).")
up('P220', yazi="POLİS MÜDÜRÜ (mühür, I05@polis'te; P118 ile kafiye)")
up('P221', yazi='SIRRI SÖYLE. (mühür)')
up('P222', yazi=None, kare="Prometheus alay eder: plan / karşı plan; süs Yunan harf akışı.")
up('P224', kare="Üçüncü tahtın düşüşü yalnız bir görüntü olarak, soluk (filmde üçüncü tahtın tek düşüşü).")
up('P226', kare="Prometheus'un zincirli elleri ↔ Hermes'in bileğinden tahta giden ince soğuk beyaz tasma ipi (uşaklık); I07@bu'da ip gerilir.", yazi='“Bu felaketimi senin uşaklığına değişmem.”')
up('P228', kare="EYVAH: 0,7 sn rüzgâr kesilir, figürün kenarından toz kopar, tek bir zincir halkası sarsılır, 0,1 sn beyaz çakma (kartal gölgesi yok).", yazi='“Eyvah!”')
up('P229', yazi=None)
up('P230', yazi=None)
up('P231', yazi='şart: “Bu aşağılayıcı zincirler çözülmeden…”')
up('P232', kare="Hermes geri çekilir, çizmelerindeki kanatlar durur; yukarıda boş tahtın gözleri kısılır (simge yok).")

# ---------- IX (J): doruk ----------
up('P233', at='J01-1.8', kare="Bölüm levhası; J01@durduralım'da sahne DONAR: solgun kil renkleri, toz ve kıvılcımlar havada asılı, kamera asılı parçacıkların arasında paralaksla ilerler; yalnız ateş renkli kalır. J01@asıl'da kamera bilekteki zincire itmeye başlar.", gecis='kil levha (donmuş karede)')
up('P234', kare="Donmuş karede P127'nin kil levhası belirir: “Zeus'tan başka hiç kimse özgür değildir.”", yazi='kil levha (P127)')
up('P235', hareket="zincir; donmuş karede yalnız nefes")
up('P236', k='K', kit='KAYA', set='KAYA', at='J02@ama', kare="Donmuş KAYA'nın üstünde kenar şeridi: “Ama bakalım, gerçekten de öyle mi?” · s. xiii; şeritteki soru işareti P014'ün zincir-soru işaretidir; J02@ama'da soru işareti düzelip zincire dönüşür ve kamera zincir boyunca yukarı kaymaya başlar.", gecis=None, yazi='kenar şeridi')
up('P237', kare="AÇILIM (≈ 6 sn, tek kesintisiz plan, çözülme yok): kamera dikey dünyada zinciri bulutlardan yukarı izler; J04@gerçekte'de bulutlar açılır; J04@zeus'ta tahtın kolu görünür; J04@köle'de zincir buluttan uzanan tek bir bilekte, soğuk beyaz kelepçede biter, kelepçe parlar (P005'in pırıltısı): yüz ve gövde yok. Etiket: ZEUS · KÖLE (y≈220).", gecis=None, yazi='ZEUS · KÖLE')
up('P238', gecis='sert kesme (J04@prometeus)', yazi='PROMETHEUS · ÖZGÜR (y≈420); köşede ERHAT · s. xiv', kare="Aşağı kesme: Prometheus; zincir boyunca altın ışık akar, duruşu özgür. İki etiket P239'a taşar, J05@uşaklarına'da söner.")
up('P239', kare="Tahtın içinde yüzsüz bir gölge; J05@çocuk'ta çocuk boyuna küçülür; koltuğun koluna yapışmış küçük bir el; eğilen uşaklar P188'deki domino sırasının kırmızı figür kopyası (boş tahta eğilirler).")
up('P240', kare="Dikey dünyada zincir: altın ışık Prometheus'un ucundan Zeus'un soğuk beyaz ucuna akar (Zeus'un Prometheus'a bağımlılığı renkle okunur).")
up('P241', k='B', kare="Tam sayfa alıntı (5'ten biri): “Zeus tutukladığı düşmanının elinde tutukludur aslında.” Sayfada iki figür arasındaki zincirin kilidi Zeus tarafına geçer.", yazi='“Zeus tutukladığı düşmanının elinde tutukludur aslında.” · s. xiv')
up('P242', kare="Dikey eksen bir tahterevalliye dönüşür (çapraz, pivot 960,430; uçlar 420,640 ve 1500,220); figürler dik kalır; terazi P046 ve P154'teki Themis terazisiyle aynı çizim.", hareket="J06@roller ile J06@sanık arasında dönüş biter; J06@sanık: kaya ucu yükselir, 'SANIK: özgür'; J06@yargıç: taht ucu iner, 'YARGIÇ: tutsak' (etiketler dik)", yazi='SANIK: özgür · YARGIÇ: tutsak', gecis='mürekkepten dönüş: sert kesme')
up('P243', k='K', kit='KAYA', set='KAYA', kare="KAYA'da köle frizi kenar şeridinde; kölelerden biri başını kaldırır; terazi köleden yana eğilir; şerit: 'hakkın köleden yana olduğu' · s. xiii.", gecis=None)
up('P244', at='J10@ayshilosun', gecis='sert kesme')

# ---------- X (I08a–I12) ----------
up('P245', at='I08a-1.8', gecis='kil levha (donmuş plakada)', kare="Donmuş karede bölüm levhası; renk önce gökteki bulutlara gelir.", set='KAYA/GENİŞ')
up('P246', kare="I08b@sorguya'da parçacıklar düşmeye devam eder, renk tümüyle geri gelir; Hermes'in tehdidi: yıldırımın kayayı yarması bir görüntü olarak.")
up('P249', set='KAYA/ÜST', kit='KAYA', kare="KAYA'nın ÜST kamerası (kartal bakışı): kamera gökten küçük zincirli figüre doğru sarmal çizerek iner; I08b@çağrılmamış'ta kısa bir pençe silueti; I08b@ziyafet'te kartalın gölgesi gövdeyi tümüyle örter (yeni set yok).")
up('P250', kare="Açılışın eşi: kylixteki siyah figür kartal (P006) negatif geçişle kırmızı figür göğüne döner; yalnız gölgesi kayar ve I08c@bedeli'de Prometheus'un göğsünde durur: 'hayır demenin bedeli'.")
up('P251', yazi='“Ne yaparsa yapsın… beni öldüremez.”')
up('P253', yazi='“Hainlerden nefret etmeyi öğrendik.”')
up('P255', kare="P142'nin (F13'ün toprak kadrajı) yıkılmış hâli: I10@gerçekte'de ilk şimşek (2 kare), I10@yer'de sarsıntı, toprak yarılır.", at='I10@artık')
up('P256', kare="P138'in (gök) yıkılmış hâli: gök gürlemesi planın başında, şimşek I10@şimşekler'de (saniyede ≤ 3 flaş).")
up('P257', kare="P139'un yıkılmış hâli: rüzgâr çizgilerinden iki karşıt sarmal I10@rüzgarlar'da çarpışır, girdaba döner; Prometheus'un ağzından akan yazı rüzgârda parçalanır ama akmaya devam eder.", at='I10@rüzgarlar')
up('P258', kare="P141'in yıkılmış hâli: deniz kuşağı yükselir, gök kuşağı iner, kadrajın kuşakları birbirine karışır.")
up('P259', hareket="fırtınanın gözünde iç ses kuralı: rüzgâr sesi düşer, yalnız nefes; I11@adalet'te fırtına bulutlarında P153'teki ΘΕΜΙΣ madalyonu soluk belirir, terazisi bir an dengelenir")
up('P260', yazi='“Görüyor musun, haksız yere neler çekiyorum.”')
up('P261', k='K', kit='KAYA', set='KAYA/FIRTINA', kare="Kayada: I12@yıkılana'da kaya yarılır, I12@gömülene'de Prometheus ve perilerle birlikte kapanır, I12@konuşmakta'da yazı çatlaktan parlar; susan → konuşan panoları yalnız kenar şeridinde (x 1500–1880, y 60–300).", gecis=None)
up('P262', gecis=None, kare="I12@son: kare sır siyahına döner; ekranda yalnız son sözün ateş renkli harfleri havada kalır (y 380–520).")
up('P263', gecis="mürekkep 0,8 sn (I12@erhatın#1'de biter)", kare="Havadaki harfler sayfadaki alıntıya dönüşür (tam sayfa alıntı); I12@özgür'de 'özgür' kelimesi ateş rengiyle parlar; konuşma bitince harfler kıvılcım olup sayfadan fırlar.")

# ---------- XI (L) ----------
up('P264', at='L01-1.8', gecis='eşleşen kesme: harflerin kıvılcımı → okçunun ok ucundaki parıltı; kil levha', kare="P210'un aynı karesinden açılır: okçu oku bırakır.")
up('P265', k='S', kit='TONDO', set='KYLIX', kare="Açılıştaki Lakonya kylixinin tondosu: Herakles her gün gelen kartalı aynı kupada vurur (L02@öldürdü'de saplanır).", gecis='kil 0,6 sn')
up('P267', k='K', kit='TİYATRO', set='TİYATRO', kare="P018'in üç papirüsü aynı kompozisyonda: 'Kurtulmuş Prometheus' toza döner.")
up('P268', kare="Aynı zincirli duruş (promChained aynı poz) çağ çağ: siyah figür, kırmızı figür, beyaz zemin, gravür tarama deseni, modern yalnız kontur; galeri kayması.")
up('P269', k='B')
up('P270', k='B', kit='SAYFA', set='SAYFA', kare="Krem sayfada tek kil renkli figür: Titan kilden küçük bir insan biçimlendirir.", gecis=None)
up('P272', yazi='FRANKENSTEIN / THE MODERN PROMETHEUS / 1818 (L05@modern)', kare="Yalnız başlık sayfası; üstünde şimşek; kil figürün eli kıpırdar.")
up('P273', kare="Kitap ön kapağı: AMERICAN PROMETHEUS (L05@amerikan); L05@nolanın'da gerçek bir kesme: kitap → meşale; beyaz parlama L05@kitaba'ya kayar (film görüntüsü yok).", yazi='Nolan · Oppenheimer (2023)')
up('P274', kare="Tek koşucu silueti hep aynı; zemin bordürü çağ çağ değişir; son koşucu modern; L06@el'de el alevin önünde durur.")

# ---------- XII (K) ----------
up('P275', at='K08a-1.8', gecis='kil levha', kare="Bölüm levhası; NASIL? kartı karttan ayrı, P276'da K08a@nasıl'da yazılır.")
up('P276', kare="B06'nın bölünmüş karesi değiştirilerek: sağdaki XX. yüzyıl figürü baştan ayakta; K08a@yaratabildi'de dönüp Aiskhylos'a bakar; çizgi bu kez sağdan sola akar.", yazi='NASIL? (K08a@nasıl)')
up('P277', k='B', kit='SAYFA', set='BÖLÜNMÜŞ', kare="Bölünmüş karenin sol yarısında kanıt panosu: taht kavgası frizinin ortasında duran Prometheus (siyasi bir kişi).", gecis=None)
up('P278', k='B', kit='SAYFA', set='BÖLÜNMÜŞ', kare="Kanıt panosu: Aiskhylos yazar, tiyatroda Atinalı yurttaşlar.", gecis=None, yazi='“politik görüşü en köklü” · s. vi')
up('P280', k='B', kit='SAYFA', set='SAYFA', kare="Sanık sırasındaki zincirli figürün silueti aynı duruşta modern bir insan siluetine dönüşür (kâğıtta).")
up('P281', hareket="K01@ilk'te sayfa çevrilir; tek uzun sayfa yolculuğu başlar (P281–P287): aynı küçük figür bütün durakları geçer")
up('P281b', at='K01@insan#1', kare="'İnsan nedir?' bir anda yazılır, ikinci satır K01@ne'de; figür dört ayak üstünde kalıp yukarı bakar (soru).", yazi='İnsan nedir? / Ne zaman insan olmaya başladı?')
up('P282', kare="K02 başında figür ayağa kalkar (cevap); K02@insan'da tam sayfa alıntı belirir.", yazi='“İnsan başkaldıran yaratıktır.” · s. v')
up('P283', kare="Tek kesintisiz plan (P283–P284): kamera iç içe çerçevelerden geri çekilir; K02@doğaya'da figür siyah figür meander çerçevesinden çıkar; K02@insan#1'de kırmızı figür çerçevesinden; K02@her'de sayfanın kendi kenarından çıkıp ateşin altın ışığına basar.")
drop('P284')
up('P285', kare="Figür gelenek süslerini (çelenk, takı) üstünden atar; süsler çizgi olarak düşer.")
up('P286', kare="K04@umuda'da P095–P097'nin pithos levhası gelir, kapalı ELPİS küpü; K04@bugün'de figür küpten döner, elinde ateşle güneşe yürür (umut soluk, ateş altın).", yazi='“Umuda karşı da ayaklandık.” · s. vi')
up('P287', yazi='İNSAN OLMAK · s. vi', kare="Çaba ve cefa: taşıyan, kuran figürlerden bir friz; küçük figür elindeki ateşi taşımayı sürdürür.")
up('P288', k='K', kit='KAYA', set='BAŞLIK', kare="Küçük figürün ateşi kapanan kitabın kapağına değer; ateşli PROMETHEUS harfleri onun ateşiyle tutuşur; K06@prometeustur'da P011'in kompozisyonuna kesme (harfler + zincirli siluet): açılış başlığının halkası. Kapak karesine kesilmez; sessizlikte harflerden tek kıvılcım süzülür.", yazi="“Bu ülkünün ilk temsilcisi Prometheus'tur.” · s. vi")

# ---------- XIII (M) ----------
up('P289', at='M00', gecis="eşleşen kesme: P288'in alevi → lambanın alevi", kare="Çevirmenlerin masası (portre yok): iki fincan, iki kalem, müsvedde, lamba. XIII bölüm levhası ekrandan kalkar (açıklamada bölüm damgası olarak kalır).",
   hareket="M00@çevrilemeyeceğini: müsveddedeki satırların üstü çizilir; M00@sahnelenemeyeceğini: kenardaki küçük sahne çizimi silinir; iki kalem sırayla kendiliğinden yazar; lamba titrer, buhar yükselir", yazi=None)
up('P291', kit='TİYATRO', set='TİYATRO', kare="P016'nın tiyatrosu modern sahne olarak: perde yerine bir ışık dairesi açılır; ışıkta kırmızı figür Prometheus; seyirci tek sıra siluet.")
up('P292', at='M02', gecis="eşleşen kesme: sahnedeki Prometheus'un ateşi → izleyiciye uzanan alev", kare="KAPAK KARESİNİN SON KULLANIMI: rezene sapındaki alev izleyiciye uzatılır; M02@ateşi'de alev kadrajın altından giren izleyicinin avucuna konur (öznel plan).", yazi='Peki sen olsan?')
up('P293', kare="Bitiş ekranı (son 20 sn): solda Sisifos çerçevesi (video öğesi x 150–870, y 180–585), sağda abone alanı (x 1250–1650, y 230–630); alev sürer.")

# kit ataması ve çekim (render birimi) numarası
for x in P:
    if 'kit' not in x:
        base = x['set'].split('/')[0].split(' ')[0]
        x['kit'] = KIT.get(base, KIT.get(x['set'], 'KAYA'))
    x['taban'] = d['taban'].get(x['kit'], '')
cek, prev = 0, None
for x in P:
    key = (x['kit'], x['k'])
    if prev is None or key != prev or (x.get('gecis') and 'levha' in x['gecis']): cek += 1
    x['cekim'] = f'Ç{cek:03d}'; prev = key
d['planlar'] = P
json.dump(d, open(os.path.join(ROOT, 'animatik', 'planlar.json'), 'w'), ensure_ascii=False, indent=1)
print(len(P), 'plan,', cek, 'çekim')
