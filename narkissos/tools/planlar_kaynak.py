"""Plan listesi kaynağı (Narkissos; yönetmen: ana oturum). Çalıştır: python3 tools/planlar_kaynak.py
Çıktı: planlar.json ({id: {at, set, olcek, ne, eylem, tr, yazi, ...}}; film.js PA() yazımı), planlar.js (window.PLAN), planlar.md (insan için tablo).
Çapa yazımı film.js A() ile aynı: 'B02', 'B02@kelime', 'B02@kelime#1', '+0.4'. Kelime eşlemesi startsWith ile yapılır:
kısa öneklerde ('o', 've', 'bir', 'ses') önce gelen başka bir kelimeye takılır; doğrulayıcı bunu uyarı olarak yazar.
Seslendirme kesin (timeline.js, DUR 531,9 sn); bu dosya yalnız plan kararlarını tutar."""
import json, re, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# TL=yol: başka bir zaman çizelgesiyle yalnız doğrulama (çıktı dosyaları yazılmaz). Ör. TL=vo/oneri/timeline_oneri.js
TL = os.environ.get('TL')
tl = open(TL or os.path.join(ROOT, 'timeline.js'), encoding='utf-8').read()
CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', tl, re.S).group(1))
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', tl, re.S).group(1))
DUR = float(re.search(r'window\.DUR\s*=\s*([\d.]+)', tl).group(1))
BITIS = DUR - 20.0   # bitiş ekranı son 20 sn

SETLER = {
 'CAM': "Bugün: kararmış telefon camı ve bugünün genci (kapı planı A/E, `phoneScene`, PH3). Yansıma gerçek başın tam altında, birebir aynası, soluk; çapraz cam parlaması; nötr ekran ışığı camın üst kenarından",
 'HAVUZ': "Dokunulmamış pınar: kıyı kayası, kesik su ufku, karşı kıyıda nergisler, gümüş su. Narkissos (efeb başı, kısa khiton) yüzüstü uzanmış ya da kayaya yaslanmış; yansıma, analitik halka (`warpRings`), tanıma hamlesi (kapı D). Filmin ana mekânı",
 'NEHIR': "Nehir kıyısı (Narkissos'un annesi bir nehir perisidir; ad anılmaz): sazlar, akan su, periler. B01'de anne ve bebek",
 'DERE': "Köy kenarında sığ, çakıllı dere (P008'in nehri değil: saz yok, bir iki söğüt); arkada köye giden patika, P005/P054'teki patikanın biçiminde. F06'nın adsız çocuğu ve arkadaşları (mitte yok, temsilî)",
 'KEHANET': "Kör kâhin Tiresias'ın yeri: kayalık yamaç, tek zeytin ağacı; asalı, sakallı, gözleri kapalı kâhin (profil)",
 'DELFI': "Delfi, Apollon tapınağı: Dor sütunlu cephe, dağ yamacı; taşta ΓΝΩΘΙ ΣΑΥΤΟΝ yazıtı (dipinto harfleri). Tanrı figürü yok",
 'FRIZ': "Vazo frizi (kalabalık sahneleri vazo bandı gibi): hayranlar ve armağanlar, reddedilenler, beddua; sonda Sisifos (kanalın Sisifos videosunun silueti). Figürler dağınık gruplar hâlinde, sıra hâlinde eğilen dizi yok",
 'ORMAN': "Av ormanı ve açıklık: ağaç gövdeleri, yaprak perdeleri, geyik; Eko ile karşılaşma; ormanın üstündeki gök (C12'de ışık şeridi)",
 'YANKI': "Soyut vazo yüzeyi: siyah sır zemin, kırmızı figür ve dipinto yazılar (Eko'nun sesi). C02'de geçmiş (Juno yalnız ışık ve tavus kuşu simgesi), F04'te bugünün 'narsist' yankısı. Kişi yok ya da yalnız Eko",
 'DAG': "Dağlar ve mağara: Eko'nun saklandığı mağara ağzı, kayaya dönüşen beden, dağ yamaçlarında solan yankı yazıları",
 'YERALTI': "Styks: ölüler diyarının karanlık suyu. Figürsüz ve simgesel: yatay dalga çizgileri, uzakta soluk bir parıltı",
 'BELGE': "Gerçek görsel araları (Ran yöntemi), beyaz zemin lekythos çerçevesi içinde (`prometheus/lib/sayfa.js`, meander bordür); çerçevenin köşesinde her belgede aynı küçük sepya Narkissos (havuz başında uzanmış), her belgede ona bir şey olur (1646 ahlak satırı üstüne biner, 1898 kenar notu ve Ellis kırpması yanında, 1899 ad etiketi değişir, 1914 yanında soru): Met 401131 Tempesta 1606; Met 419135 Callot / 1646 levhası (yalnız resim + üst satır); Ellis 1898 cümle kırpması; Freud 1914 ilk sayfa. Lisans uretim_plani.md §5. Caravaggio, Pompeii, Hatay mozaiği, Waterhouse YOK",
 'YAZI': "Yazı levhası: dönen vazonun omzunda kırmızı figür yazı (A05 'narsisizm') ya da beyaz zemin sepya Narkissos'un ad etiketi (F03 'Narcismus'). F05'in sorusu ve F08'in ilk cümlesi artık sahnenin içinde (P085, P087)",
 'SON': "Bitiş ekranı (son 20 sn): siyah sır zemin, altta ince meander bandı ve küçük vazo figürü; orta-sağ ve üst bölge YouTube öğelerine (video kutusu, abone düğmesi) boş",
}
BOLUM = {'A': 'Cam', 'B': 'Kehanet', 'C': 'Yankı', 'D': 'Havuz', 'E': 'O benim', 'F': 'Ad'}
SAHIP = {'A': 'SAHİP-1', 'B': 'SAHİP-1', 'C': 'SAHİP-1', 'D': 'SAHİP-2', 'E': 'SAHİP-2', 'F': 'SAHİP-2'}

CUT = {'type': 'cut'}
def FADE(d=.6): return {'type': 'fade', 'dur': d, 'end': True}

# Satır: (çapa, set, ölçek, ekranda ne olur, [(çapa, sözcüğe bağlı eylem)], geçiş, ekran yazısı, kamera, hassasiyet notu, levha mı)
# Ölçekler: geniş · orta · orta-yakın · yakın · ayrıntı · ters açı (ardışık iki plan aynı ölçekte olmaz)
P = [
 # ───────────── A · Cam (kanca; kapak A "O BENİM" ilk 5 sn'de) ─────────────
 ('A01-0.7', 'CAM', 'orta-yakın',
  "Kanca, kapak A'nın ekseni: bugünün genci kararmış telefon camına bakar; camda yüzünün birebir, soluk aynası tam altında. Akış kartları kayar ve söner, camda yalnız yüz ve yansıması kalır. 'baktın'dan sonraki sessizlikte (≈3,1–4,5 sn) telefonun kenarları kıyıya açılır, cam havuza döner (kapı A); 'iki bin yıl' derken havuz kurulmuştur. Sessiz okuma testi: 3,0 sn karesi kör okura verilir",
  [('A01-0.4', "başparmak akışı yukarı kaydırır (1. kaydırma)"), ('A01@camda', "2. kaydırma; akış kartları sönmeye başlar"), ('A01@baktın', "kartlar söndü: camda yalnız yüz ve yansıma; yansıyan göz bir an parlar (tek odak)"),
   ('A01@baktın+0.55', "anlatım sustu: cam → havuz biçim dönüşümü başlar (`morphPts`, kısa); yansıma soluk ve halkayla dağınık kalır, gövdeden ≥ 60 px açık, kol kesmez, halka yansımanın üstünden geçer (FABLE tur 3, madde 1)"), ('A02@iki-0.2', "dönüşüm biter: cam havuz olmuştur; kesme 'iki'de antik yüze")],
  CUT, "", "'baktın'a kadar z .82→.86 çok yavaş yaklaşma; dönüşümde suya iniş (kapı A)",
  "Beğeni sayacı, marka, logo yok. Çene altında sıcak parıltı yok (hale); ışık soğuk/nötr ve camın kenarından. Yansıyan saç 'uzun tutam' okunmasın (tur 3, madde 2)", False),
 ('A02@iki', 'HAVUZ', 'orta',
  "Aynı eksenden antik pınar, 'iki bin yıl'da (≈4,5 sn; kapak A'nın vaadi ilk 5 sn'de): efeb başlı genç (kısa khiton) kıyıda yüzüstü uzanmış, suya bakıyor; yansıması suda, soluk (kapı C). Vazo ressamlarının âdetiyle figürün yanına adı yazılır",
  [('A02@genç', "su durulur; yansıma netleşir"), ('A02@baktı',"genç başını suya biraz daha eğer; yansıma toparlanır"), ('A02@narkissos', "figürün yanında dipinto ΝΑΡΚΙΣΣΟΣ fırçayla yazılır; altında Türkçe etiket")],
  CUT, "etiket: NARKİSSOS (dipinto ΝΑΡΚΙΣΣΟΣ, figürün yanında; y < 880)", "yatay kaydırma sağa",
  "Dört ayak üstünde eğilme ya da diz çökme yok; bacaklar düz ve yerde, khiton uyluk ortasında", False),
 ('A03', 'HAVUZ', 'geniş',
  "Bilinen resim: orman kenarında pınar, kıyıda küçük, uzanmış genç. Herkesin bildiği hikâyenin kartpostalı",
  [('A03@herkes', "kıyıdaki nergisler rüzgârla aynı yöne eğilir"), ('A03@unutulan', "rüzgâr durur, su aynalaşır; kamera gence doğru kayar")],
  CUT, "", "yavaş yaklaşma (≤ %10) ve yatay kayma", "", False),
 ('A03@sudaki', 'HAVUZ', 'yakın',
  "Yüz ve yansıması (kapı D yakın planı; öpüşme ekseni değil, burunlar ≥ 300 px). Kapak A'nın sözü: kendini gördü. P053'ten ayrım: el kayada kalır, parmak ve su teması yok, yansıma soluk ve 9 kare gecikmeli kalır (kilitlenme yok)",
  [('A03@anladı', "yansıyan göz karenin en parlak noktası olur"), ('A03@benim', "genç hafifçe irkilir (küçük; yansıma irkilmeyi 9 kare geç izler; tam tanıma hamlesi E04'e saklı)")],
  CUT, "alıntı: “O benim.” küçük ve soluk sepya (‘benim’den sonra, üst yarıda; P053'teki büyük kırmızı yazının ön sesi) · künye: Ovidius, Dönüşümler III 463", "çok yavaş yaklaşma",
  "Dudak teması yok. Halka baştan ≥ 60 px uzak", False),
 ('A04', 'HAVUZ', 'ters açı',
  "Arkadan ve yukarıdan: genç kıyıda; arkasında ormana açılan boş patika. Gitmek mümkün, ama gitmiyor",
  [('A04@neden', "patikaya güneş düşer"), ('A04@kalkıp', "rüzgâr yaprakları patikadan uzağa sürükler; genç kıpırdamaz")],
  CUT, "", "yatay kaydırma patikaya doğru", "", False),
 ('A05', 'YAZI', 'ayrıntı',
  "Dönen bir vazonun omzunda kırmızı figür yazı: ΝΑΡΚΙΣΣΟΣ. 'narsisizm'de harfler yeniden dizilir: NARSİSİZM",
  [('A05@kelimede', "vazo döner, ΝΑΡΚΙΣΣΟΣ yazısı ön yüze gelir"), ('A05@narsisizm', "harfler kıvrılıp yeniden dizilir: NARSİSİZM (kapı kelimesi)")],
  CUT, "yazı: ΝΑΡΚΙΣΣΟΣ → NARSİSİZM (vazo yüzeyinde, y 300–700)", "vazo yavaş döner (yatay kayma)", "", True),
 ('A05@peki', 'HAVUZ', 'yakın',
  "Su yüzü ve yansıma; başlığın sorusu. Damla ve halka yok (gözyaşı halkası yalnız P062'de): bir esinti suyu ürpertir, yansıma titrer",
  [('A05@kendini', "esinti suyu ürpertir; ince yatay kırışıklar yansımanın üstünden geçer"), ('A05@döner', "yansıma titreyip yerine oturur, yüz bölünmez; kenarda bir yaprak kıyıya sürüklenir")],
  CUT, "", "çok yavaş uzaklaşma (z 1,0 → ,94)", "", False),

 # ───────────── B · Kehanet ─────────────
 ('B01', 'NEHIR', 'geniş',
  "Nehir kıyısı, vazo frizi gibi: nehir perisi anne bebeği kucağında; iki üç peri bebeğe bakıyor",
  [('B01@perilerin', "periler bebeğe doğru eğilir (ayakta, baş eğme)"), ('B01@güzeldir', "bir peri bebeğe bir nergis değil bir sarmaşık dalı uzatır")],
  FADE(.7), "bölüm kartı: KEHANET (ilk 3 sn, üst yarı)", "yatay kaydırma",
  "Anne ve bebek profilden; önden simetrik 'anne-çocuk' ikonu yok, ışık halkası yok (Meryem ikonografisi okunmasın). Peri giysileri uzun khiton", False),
 ('B01@annesi', 'KEHANET', 'orta',
  "Kayalık yamaçta kör kâhin Tiresias (asalı, sakallı, gözleri kapalı); anne bebekle karşısında",
  [('B01@kör', "Tiresias başını kaldırır, gözleri kapalı kalır"), ('B01@oğlum', "anne bebeği kâhine doğru uzatır")],
  CUT, "etiket: TİRESİAS (dipinto ΤΕΙΡΕΣΙΑΣ yanında)", "yatay kaydırma kâhine doğru", "Kâhin önden simetrik değil, profil", False),
 ('B02', 'KEHANET', 'yakın',
  "Tiresias'ın profili yakın: ağzından vazo geleneğindeki gibi fırça yazısı çıkar (dipinto). Konuşma dipintosu Türkçe; Latince yalnız künyede",
  [('B02@kendini', "ağızdan dipinto KENDİNİ TANIMAZSA akmaya başlar"), ('B02@tanımazsa', "son harf yerine oturur; kenarda annenin eli bebeği göğsüne çeker")],
  CUT, "dipinto: KENDİNİ TANIMAZSA (ağızdan, alıntı yazısı ayrıca yok) · künye: Ovidius, Dönüşümler III 348 · si se non noverit", "dipinto akarken kamera yazıyla birlikte sağa kayar", "", True),
 ('B03', 'DELFI', 'geniş',
  "Delfi: dağ yamacında Dor sütunlu Apollon tapınağı; girişteki taş. Kısa bağlam planı (kancadan sonra bilinen bağlam: Kafka/İkaros dersi); ağırlık P012'de. Eşleme kesmesi: P010'daki dipintonun yatay çizgisi taş yazıtın satır çizgisine oturur",
  [('B03@yazılı', "kamera tapınak girişindeki taşa kayar; taşta harfler henüz boş çizgi")],
  CUT, "künye: Delfi, Apollon tapınağı", "yatay kaydırma",
  "Tanrı figürü yok; sunak ya da tapınma hâlindeki kalabalık yok", False),
 ('B03@kendini', 'DELFI', 'ayrıntı',
  "Yazıtın yakını; yazıtın altında bir su birikintisi. Taşta ΓΝΩΘΙ ΣΑΥΤΟΝ, altında Türkçe KENDİNİ TANI; Türkçe satır suda ters döner (P061'deki KENDİNİ TANIMAZSA → TANIDI'nın karşılığı)",
  [('B03@kendini', "taşta ΓΝΩΘΙ ΣΑΥΤΟΝ harf harf belirir, altında Türkçe KENDİNİ TANI"), ('B03@tersine', "Türkçe satır suda ters (ayna) görünür; harfler tek tek döner"), ('B03@ölüm', "ters yazı halkalarla dağılır (Delfi birikintisi; gözyaşı halkası değil)")],
  CUT, "yazıt: ΓΝΩΘΙ ΣΑΥΤΟΝ (taşta, Yunanca) · KENDİNİ TANI (Türkçe, taşın altında) · künye: Delfi, Apollon tapınağı", "yavaş aşağı kayma (taştan suya)", "", True),
 ('B04', 'ORMAN', 'orta',
  "On altı yaşında Narkissos: avcı (kısa khiton, mızrak), orman kenarında yürür. Bebekten gence zaman sıçraması",
  [('B04@narkissos', "genç kadraja yürür (`yuruyusYolu`, ayak kaymaz)"), ('B04@on', "durur, mızrağı omzuna alır, başını çevirir")],
  FADE(.7), "", "figürü izleyen yatay kaydırma", "", False),
 ('B04@delikanlılar', 'FRIZ', 'geniş',
  "Vazo frizi: delikanlılar ve kızlar küçük, dağınık gruplar hâlinde ona armağan uzatır (çelenk, çiçek, tavşan: vazo resmindeki kur armağanları)",
  [('B04@kızlar', "kızlar grubu çelenk uzatır"), ('B04@gönül', "bütün başlar ona döner")],
  CUT, "", "yatay kaydırma frizi boydan boya tarar",
  "Sıra hâlinde eğilen dizi yok (namaz safı okuması); gruplar düzensiz, ayakta. Çıplaklık yok", False),
 ('B05', 'FRIZ', 'yakın',
  "Narkissos'un profili: çene yukarı, başını çevirir; önüne uzatılan çelenk",
  [('B05@gururludur', "başını çevirir"), ('B05@kazanamaz', "çelenk elden kayar, yere düşer")],
  CUT, "", "yavaş yukarı kayma (düşen çelenkten yüze)", "", False),
 ('B06', 'ORMAN', 'geniş',
  "Orman: geyik ağaçların arasından fırlar, Narkissos mızrakla peşinde koşar",
  [('B06@geyik', "geyik kadrajı soldan sağa geçer"), ('B06@biri', "ön planda yaprakların arasında biri durur: yüzü yaprak gölgesinde, yalnız gözü seçilir (Eko)")],
  CUT, "", "koşuyu izleyen yatay kaydırma (`araclar/hareket` koşu)", "", False),

 # ───────────── C · Yankı (Eko karşı kutup; kapak B'nin karşıtlığı) ─────────────
 ('C01', 'ORMAN', 'orta',
  "Eko ağacın arkasından çıkar: dağ perisi, uzun khiton ve himation, saçı toplu, yüzü açık. Vazo âdetiyle adı yanına yazılır",
  [('C01@eko', "dipinto ΗΧΩ yanında belirir; altında Türkçe etiket"), ('C01@susmayı', "ağzı aralanır, kapanır"), ('C01@konuşmayı', "eli dudağına gider, bekler")],
  CUT, "bölüm kartı: YANKI (ilk 3 sn) · etiket: EKO (dipinto ΗΧΩ)", "paralaks: ön plandaki ağaç gövdesi kayar, Eko onun arkasından çıkar",
  "Eko baştan ayağa örtülü değil (yüz açık, kollar görünür); çıplaklık yok", False),
 ('C02', 'YANKI', 'geniş',
  "Geçmiş, siyah sır zemin üstünde: Eko konuşur, ağzından uzun, kıvrılan bir dipinto şeridi akar. Juno figürle çizilmez: sağdan tavus kuşu kuyruğu ve ışık",
  [('C02@konuşurdu', "şerit uzar, kıvrılır"), ('C02@junoyu', "sağdan tavus kuşu kuyruğu açılır, sıcak ışık"), ('C02@kandırdığı', "şerit tavus kuşunun gözleri arasında dolanır"), ('C02@cezalandırıldı', "ışık kesilir; şerit kopar, harfler yere dökülür")],
  FADE(.6), "", "yatay kaydırma şeridi izler",
  "Juno ve hiçbir tanrıça figür olarak çizilmez; ışık ve kuş simgesi. Tavus kuşu gözleri 'nazar' gibi değil, kuyruk biçimiyle okunsun", False),
 ('C02@günden-0.65', 'YANKI', 'yakın',
  "Eko'nun profili yakın: başka bir ağızdan gelen söz ona doğru akar; yalnız son öbek onda yanar ve geri döner. Yazı yok: harfsiz söz (P020/P052 dili, okunmayan fırça kıvrımları)",
  [('C02@son', "gelen sözün yalnız son öbeği kırmızı yanar"), ('C02@verebilir', "Eko o öbeği iki kez küçülerek geri verir; solarak uzaklaşır")],
  CUT, "", "yazıyı izleyen yatay kayma", "Kaynakta olmayan söz yazılmaz: okunur harf yok", False),
 ('C03', 'ORMAN', 'ters açı',
  "Eko'nun omzunun üstünden: açıklıkta uzakta Narkissos. Eko'nun söyleyemediği söz",
  [('C03@aşık', "Eko yaprak dalını aralar"), ('C03@söylemek', "ağzından içi boş bir yazı şeridi çıkar (harfsiz)"), ('C03@söyleyemez', "şerit söner"), ('C03@başkasının', "Eko geri çekilir, bekler")],
  FADE(.6), "", "yatay kayma omuz üstünden", "", False),
 ('C04', 'ORMAN', 'geniş',
  "Orman: arkadaşları ağaçların ardında kaybolur, Narkissos yalnız kalır ve seslenir",
  [('C04@ayrı', "arkadaş siluetleri kadrajdan çıkar"), ('C04@seslenir', "Narkissos elini ağzına götürür"), ('C04@kim', "ağzından dipinto KİM VAR BURADA? ağaçlara doğru akar")],
  CUT, "", "yatay kaydırma", "", False),
 ('C04@bir', 'ORMAN', 'yakın',
  "Eko'nun yüzü yaprakların arasında: gelen yazının yalnız son kelimesi ondan geri çıkar",
  [('C04@cevap', "gelen yazı Eko'ya ulaşır; 'KİM VAR' söner"), ('C04@burada#1', "BURADA! Eko'dan çıkar, soluk kırmızı, solarak tekrar eder (yankı dili)")],
  CUT, "", "paralaks: ön plandaki yapraklar kayar, yüz sabit", "", False),
 ('C05', 'ORMAN', 'orta',
  "Narkissos döner, ağaçlara seslenir; yankı başka yönden gelir",
  [('C05@gel', "GEL! yazısı ondan çıkar"), ('C05@gel#1', "GEL! başka yönden, ağaçların arasından geri gelir; Narkissos başını çevirir"), ('C06@burada', "BURADA BULUŞALIM! yazısı")],
  CUT, "", "yatay kaydırma", "", False),
 ('C06@eko', 'ORMAN', 'yakın',
  "Eko'nun yüzü: sevinç (kaşlar kalkar, gülümseme). En canlı yankı",
  [('C06@sevinçle', "gülümser"), ('C06@buluşalım#1', "BULUŞALIM! en büyük ve en parlak yankı olarak Eko'dan çıkar")],
  CUT, "", "çok yavaş uzaklaşma (yankı büyürken)", "", False),
 ('C06@ormandan', 'ORMAN', 'geniş',
  "Eko ağaçların arasından çıkıp kollarını açarak ona koşar",
  [('C06@kollarını', "kollar açılır"), ('C06@boynuna', "Eko ona neredeyse ulaşır")],
  CUT, "", "koşuyu izleyen yatay kaydırma (`yuruyusYolu` koşu, `yayIzi` himation)",
  "Sarılma gösterilmez: kollar ulaşmadan plan kesilir", False),
 ('C07', 'ORMAN', 'orta',
  "Narkissos geri çekilir, elini kaldırıp iter ve kaçar; reddi yazıyla",
  [('C07@çek', "eliyle iter"), ('C07@ancak', "ağzından dipinto ANCAK BEN ÖLÜNCE BANA SAHİP OLURSUN"), ('C07@olursun', "döner, kaçar")],
  CUT, "", "hafif yatay kayma", "", False),
 ('C08', 'ORMAN', 'yakın',
  "Eko kollarını indirir; aynı yazının yalnız son yarısı ondan geri döner",
  [('C08@son', "'ANCAK BEN ÖLÜNCE' söner"), ('C08@bana', "BANA SAHİP OLURSUN Eko'dan çıkar, kırmızı vurgu")],
  CUT, "künye: Ovidius, Dönüşümler III 391–392", "çok yavaş uzaklaşma (Eko küçülür)", "", False),
 ('C09', 'ORMAN', 'ayrıntı',
  "Havada asılı kalan yazı: BANA SAHİP OLURSUN. Kelimeler ormanın içine, uzaktaki pınara doğru sürüklenir (L3'ün sözü)",
  [('C09@tut', "yazı havada durur, harfler hafifçe parlar"), ('C09@sahibine', "yazı ağaçların arasından uzaklaşır"), ('C09@dönecek', "son harf uzakta bir su yüzüne düşer ve yansır")],
  CUT, "", "yazıyı izleyen yatay kaydırma", "", True),
 ('C10', 'DAG', 'orta',
  "Reddedilen Eko: yüzünü bir yaprak dalıyla örter (III 393–394) ve mağaraya çekilir",
  [('C10@yapraklarla', "eli yapraklı dalı yüzüne çeker; yalnız yüz örtülür"), ('C10@mağaralarda', "kamera mağara ağzına kayar, Eko girişte oturur"), ('C10@büyür', "mağara ağzındaki gölge büyür")],
  FADE(.7), "", "yatay kaydırma mağaraya",
  "Örtü yalnız yaprak; başörtüsü, çarşaf ya da baştan ayağa örtü yok", False),
 ('C11', 'DAG', 'yakın',
  "Eko'nun bedeni erir: kil rengi solar, beden kaya rengine karışır ve kayanın biçimini alır. Ses kalır",
  [('C11@eritir', "figürün rengi solmaya başlar"), ('C11@kemikleri', "figürün yerinde kaya biçimi belirir"), ('C11@taşa', "kaya tamamlanır; kayanın yüzünde soluk bir profil çizgisi kalır")],
  CUT, "", "figürden kayanın dibine yavaş aşağı kayma",
  "Zayıflamış beden, kaburga, iskelet ya da kemik çizimi yok: erime renk ve biçim değişimiyle", False),
 ('C11@ise-0.25', 'DAG', 'geniş',
  "Dağ sırası, kimse yok: yamaçlarda dipinto yazılar solarak belirip söner. Ses yaşar",
  [('C11@görünmez', "kamera boş vadide kayar"), ('C11@herkes', "yazılar yamaçtan yamaca sırayla yankılanır"), ('C11@duyar', "son yazı söner")],
  CUT, "", "yatay kaydırma", "", False),
 ('C12', 'FRIZ', 'orta',
  "Vazo frizi: geri çevrilen başkaları, dağınık, başları öne düşük",
  [('C12@değildi', "figürler bir bir başını kaldırır"), ('C12@küçümsenenlerden', "biri öne çıkar")],
  CUT, "", "yatay kaydırma",
  "Sıra hâlinde eğilen dizi yok; figürler ayakta ve düzensiz", False),
 ('C12@ellerini', 'FRIZ', 'ters açı',
  "Arkadan siluet: öne çıkan genç tek kolunu göğe uzatır (el yarı açık); beddua yazısı göğe yükselir",
  [('C12@kaldırır', "uzak kol dirsek bükük kalkar, neredeyse dik göğe uzanır, el yarı açık (arkadan; yüzü örtmez)"), ('C12@sevsin', "ağzından dipinto O DA BÖYLE SEVSİN göğe yükselir"), ('C12@kavuşamasın', "yazı bulutlara ulaşır")],
  CUT, "", "aşağıdan göğe yavaş kayma",
  "Arkadan siluet; tek kol göğe, el yarı açık. Yumruk, 45° öne uzanan düz kol (selam), iki avucu göğe açık dua pozu, diz çökme, secde yok", False),
 ('C12@haklı', 'ORMAN', 'geniş',
  "Ormanın üstünde bulutlu gök: bulutlar aralanır, tek ince ışık şeridi iner. Öç tanrıçası figürle çizilmez",
  [('C12@tanrıçası', "bulutlar aralanır, tek ışık şeridi"), ('C12@kabul', "ışık şeridi ormanın içindeki pınara iner")],
  CUT, "", "ışığı izleyen aşağı kayma",
  "Tanrıça figürü, yüz, hale, haç biçimli ışın yok: tek dikey şerit", False),

 # ───────────── D · Havuz ─────────────
 ('D01', 'HAVUZ', 'orta',
  "Işık şeridi pınara değer: orman içinde dokunulmamış, gümüş gibi parlak bir kaynak",
  [('D01@karşılık', "ışık su yüzüne değer, yayılır"), ('D01@gümüş', "su yüzü gümüş parlar")],
  CUT, "bölüm kartı: HAVUZ (ilk 3 sn)", "yavaş yaklaşma (≤ %10)", "Işık suyun üstünde halka ya da hale biçimi almaz", False),
 ('D01@ona', 'HAVUZ', 'ayrıntı',
  "Kıyının yakını: hiçbir şey suya değmez",
  [('D01@çoban', "kıyıda bir çobanın ve keçinin gölgesi geçer, suya değmez"), ('D01@hayvan', "bir kuş suyun üstünden uçar, inmez"), ('D01@dal', "dal sallanır ama düşmez; su kıpırdamaz")],
  CUT, "", "yatay kaydırma kıyı boyunca", "", False),
 ('D02', 'HAVUZ', 'orta',
  "Yorgun Narkissos gelir, mızrağını bırakır, kıyıya uzanır ve suya eğilir (kapı C pozu)",
  [('D02@yorulan', "mızrak yere bırakılır"), ('D02@uzanır', "yüzüstü uzanır"), ('D02@susuzluğunu', "eli suya iner"), ('D02@başka', "su durulur, yansıma belirir")],
  CUT, "", "yatay kaydırma figürle",
  "Uzanma; dört ayak üstü eğilme, diz çökme, alnı suya değme yok", False),
 ('D03', 'HAVUZ', 'yakın',
  "Yüz ve yansıması: âşık oluş. Yansıma gecikmesi buradan başlar: yansıma gerçeği 9 kare (0,3 sn) geç izler; hafif, ama her kıpırtıda var",
  [('D03@aşık', "gözler açılır, durur; yansımanın gözleri 9 kare sonra açılır"), ('D03@oysa', "esinti yansımayı ürpertir: yalnızca su")],
  CUT, "", "yüzden yansımaya yavaş aşağı kayma", "Dudak teması yok", False),
 ('D04', 'HAVUZ', 'orta',
  "Mermer heykel gibi: figür kıpırdamaz, rengi kil kırmızısından beyaz zemin mermerine döner; çevresinde yalnız doğa kıpırdar",
  [('D04@heykel', "figür beyaz zemine (lekythos beyazı) döner"), ('D04@kıpırdamadan', "yapraklar ve su kıpırdar, figür sabit")],
  CUT, "", "yatay kaydırma", "Beden açık değil; khiton görünür", False),
 ('D04@yıldız', 'HAVUZ', 'ayrıntı',
  "Onun gözünden yansıma: kamera yansımanın üstünde gezinir",
  [('D04@göze', "yansıyan gözler parlar"), ('D04@buklelere', "kamera bukleler boyunca kayar"), ('D04@boyna', "kamera boyna iner")],
  CUT, "", "yansıma üstünde yavaş kayma",
  "Sensüel değil: kıpırdamayan şaşkın bakış; beden yakın planı yok, boyunda durur", False),
 ('D05', 'HAVUZ', 'ters açı',
  "Tam tepeden: su çizgisi dikey eksende, kıyının taşı solda; iki yüz yan yana (solda gerçek baş tepeden, sağda suyun içinde yansıyan yüz). Seven de o, sevilen de: kompozisyon D'nin profil + altta yansıma düzeninden ayrılır",
  [('D05@seven', "soldaki baş ışıklanır"), ('D05@sevilen', "sağdaki yansıma ışıklanır, 9 kare geç")],
  CUT, "", "tepeden; su çizgisi boyunca yavaş dikey kayma", "", False),
 ('D06', 'HAVUZ', 'orta',
  "Suya eğilip yaklaşır, kollarını daldırır; yansıma halkalarla kırılır",
  [('D06@yaklaşır', "yüz suya yaklaşır, değmeden durur"), ('D06@kollarını', "kollar suya dalar, yansıma halkayla kırılır"), ('D06@yakalayamaz', "eller boş çıkar, damlalar düşer")],
  CUT, "", "hafif yatay kayma", "Dudak teması yok (III 427 yaklaşma, öpüş gösterilmez)", False),
 ('D07', 'HAVUZ', 'yakın',
  "Yansıma toparlanır; bölümün küçük sorusu",
  [('D07@bilmez', "yansıma toparlanır"), ('D07@bilse', "kamera yansımadan gerçek yüze çıkar")],
  CUT, "soru: Bilse, kalkıp gider miydi? (üst yarı, alıntı yazısı)", "yukarı kayma", "", False),
 ('D08', 'HAVUZ', 'geniş',
  "Kıyının kenarında, hikâyenin dışından gelen biri: togalı şair silueti (Ovidius, vazo dilinde dönem silueti, portre değil)",
  [('D08@ovidius', "şair kadraja girer; etiket"), ('D08@durur', "şair durur; yaprakların kıpırtısı yavaşlar"), ('D08@seslenir', "şair elini gence doğru uzatır")],
  CUT, "etiket: OVİDİUS · Dönüşümler, MS 8", "yatay kaydırma",
  "Gerçek kişi: gerçekçi portre yok, vazo silueti", False),
 ('D09', 'HAVUZ', 'ters açı',
  "Şairin omzunun üstünden genç: yine suya uzanır",
  [('D09@kaçan', "genç elini suya uzatır"), ('D09@yakalamaya', "eli suda boşa kapanır")],
  CUT, "künye: Ovidius, Dönüşümler III 432–434", "omuz üstü sabit eksen, yavaş yaklaşma", "", False),
 ('D09@gördüğün', 'HAVUZ', 'ayrıntı',
  "Yansıma 'gölge'ye döner: suyun içindeki suret kırmızı figürden siyah figüre (vazo dilinde gölge) geçer",
  [('D09@yansıyan', "yansıma koyulaşmaya başlar"), ('D09@gölgesi', "yansıma tam siyah figür olur")],
  CUT, "", "çok yavaş uzaklaşma", "", False),
 ('D10', 'HAVUZ', 'orta',
  "Konuşan şair (P044–P045'in mekân mantığı): togalı Ovidius silueti solda önde, omzunun yanından kıyıda genç ve suda yansıması. 'Seninle' her sözde yansıma onu bir an sonra (9 kare) izler: kıpırtılar görünür, gecikme fark edilir",
  [('D10@gelir', "şair elini gence doğru açar; genç başını eğer, yansıma bir an sonra"), ('D10@kalır', "ikisi durur"), ('D10@gider', "genç kalkmaya davranır, yansıma geç gelir"), ('D10@gidebilirsen', "baş geri iner: gidemez; şairin eli iner")],
  CUT, "", "şairin omzundan gence doğru yatay kayma", "Gerçek kişi: gerçekçi portre yok, vazo silueti", False),
 ('D11', 'HAVUZ', 'geniş',
  "Zaman geçer, o aynı yerde: gün batar, gece olur, şafak söker",
  [('D11@gidemez', "güneş batar"), ('D11@açlık', "yanındaki dokunulmamış ekmek ve meyve"), ('D11@uyku', "gece: yıldızlar nokta"), ('D11@koparabilir', "şafak; o hâlâ kıyıda")],
  CUT, "", "çok yavaş yatay kayma; ışık değişir (zaman plan içinde)",
  "Yıldızlar nokta; altı köşeli ya da haç biçimli yıldız yok. Hilal ay ve yıldız birlikte konmaz", False),

 # ───────────── E · O benim (dönüş) ─────────────
 ('E01', 'HAVUZ', 'ayrıntı',
  "Yansımanın gözü: bir şey dikkatini çeker",
  [('E01@dikkatini', "gerçek göz kısılır; yansımanın gözü 9 kare sonra")],
  CUT, "bölüm kartı: O BENİM (2,5 sn)", "paralaks: ön plandaki sazlar kayar, göz sabit", "", False),
 ('E02', 'HAVUZ', 'orta',
  "Tanıma hamlesinin hazırlığı (kapı D düzeni), orta ölçek: kol, kıyı kayası ve su birlikte kadrajda; gerçek el ve yansımanın eli aynı karede, 'yansımanın eli geç gelir' iki el birlikte görünürken okunur",
  [('E02@uzatınca', "el kayadan kalkar"), ('E02@uzatır', "yansımanın eli 9 kare (0,3 sn) gecikmeyle gelir")],
  CUT, "", "hafif yatay kayma (kol boyunca)", "", False),
 ('E02@gülümseyince', 'HAVUZ', 'yakın',
  "Yüz ve yansıma: gülümser, ağlar; yansıma 9 kare geç izler",
  [('E02@gülümser', "yansıma 9 kare geç gülümser"), ('E02@ağlayınca', "gözde yaş"), ('E02@yaş', "yansımanın gözünde de yaş")],
  CUT, "", "yansımadan gerçek yüze yavaş yukarı kayma", "", False),
 ('E02@sudaki#1', 'HAVUZ', 'ayrıntı',
  "Yansımanın dudakları kıpırdar: ağzından çıkan yazı suyun içinde kalır, yüzeyi geçemez (Eko'nun tersi: beden var, ses yok)",
  [('E02@kıpırdar', "su altındaki ağızdan soluk dipinto çıkar"), ('E02@ulaşmaz', "yazı su yüzeyine çarpıp dağılır")],
  CUT, "", "çok yavaş yaklaşma", "", False),
 ('E03', 'HAVUZ', 'yakın',
  "Tanıma hamlesi (kapı D_benim): işaret parmağı suya değer, yansımanın parmağı 'benim'de aynı karede buluşur, D03'ten beri süren 9 karelik gecikme sıfırlanır (kilitlenme: filmin bu andaki tek görsel olayı), yansıma soluktan kile döner; genç irkilir. E04 bitişi ile E05 arasındaki ≈1,8 sn sessizlik bu planın içinde: yeni eylem yok, kilitli yansıma durur",
  [('E03@anlar', "işaret parmağı suya değer (küçük halka)"), ('E04@benim', "iki parmak buluşur, gecikme sıfırlanır; irkilme (baş geri, kaş kalkar, ağız aralanır); ekrana yalnız “O benim.” gelir"), ('E04@anladım', "el suda kalır"), ('E04@aldatmıyor', "el çekilir; yansıma birebir kilitli ve sabit (sessizlik boyunca)")],
  CUT, "alıntı: yalnız “O benim.” (‘benim’de, üst yarı, büyük kırmızı; kapak sözü) · künye küçük: Ovidius, Dönüşümler III 463 · iste ego sum. ‘Anladım. Suretim beni aldatmıyor.’ yalnız altyazıda", "çok yavaş yaklaşma; irkilme anında kamera hızlanmaz ya da sarsılmaz",
  "Âdem'in Yaratılışı çağrışımı: buluşma suyun yüzeyinde, kendi yansımasıyla; animatikte kör okura verilir. Halka baştan ≥ 60 px", False),
 ('E05', 'HAVUZ', 'geniş',
  "Geri çekilmiş manzara: o hâlâ kıyıda. Arkasındaki patika ışıkla açılır ve söner",
  [('E05@artık', "kamera geri kayar"), ('E05@ama', "arkadaki patikaya ışık düşer: gitmek mümkün"), ('E05@gidemiyor', "ışık söner, figür kıpırdamaz")],
  CUT, "", "yatay kayma (zoom yerine)", "", False),
 ('E06', 'HAVUZ', 'ters açı',
  "Sırttan: genç kıyıda, kamera omzunun arkasında; yüzünü yalnız suyun yansımasında görürüz. Su yüzündeki güneş parıltısı yükselir ve gerçek yüzün kenarını (yanak, kulak) sıcak ışıkla çizer. D'nin profil + altta yansıma karesinden ayrılır",
  [('E06@yanıyorum', "su yüzündeki güneş parıltısı yükselir, yüzün kenarına sıcak ışık"), ('E06@yapayım', "başını iki elinin arasına alır (sırttan: dirsekler açılır)")],
  CUT, "künye küçük: Ovidius, Dönüşümler III 464 (alıntı altyazıda; ekranda alıntı yazısı yok)", "omuz arkasından yavaş yaklaşma",
  "Göğüste alev ya da önden simetrik göğüs ışığı yok (Kutsal Kalp); ışık yalnız yüzün kenarında, aşağıdan sudan", False),
 ('E07', 'HAVUZ', 'orta',
  "Kollarıyla kıyıyı kavramış; eli yansımanın yüzüne çok yakın, değmez. Alıntı yazısı 'SAHİP' kelimesi üst yarının ortasında olacak biçimde dizilir (P057'ye eşleme kesmesi)",
  [('E07@istediğim', "eli yansımaya yaklaşır"), ('E07@sahip', "durur; yazıda 'SAHİP' kırmızı yanar"), ('E07@yoksul', "el boş kapanır")],
  CUT, "alıntı: “Sahip olduğum şey beni yoksul etti.” · künye: III 466 · inopem me copia fecit", "yatay kayma", "", False),
 ('E08', 'ORMAN', 'geniş',
  "Hatıra, beyaz zeminde (lekythos beyazı, solgun sepya çizgi; sessizde de 'geçmiş' okunur): C07'nin kompozisyonu (orman, iten el); aynı dipinto ağzından çıkar. Giriş eşleme kesmesiyle: P056'daki 'SAHİP' kelimesi aynı ekran yerinde kalır, çevresi hatıraya döner",
  [('E08@ancak', "dipinto ANCAK BEN ÖLÜNCE BANA SAHİP OLURSUN ('SAHİP' önceki planın yerinde)"), ('E08@olursun', "yazı ormandan pınara doğru uçar")],
  CUT, "", "C07 çizimi (P026) daha geniş kadrajla, beyaz zemin paletiyle yeniden kullanılır (SAHİP-1'in işlevi); hafif yatay kayma", "", False),
 ('E08@söz', 'HAVUZ', 'ayrıntı',
  "Uçan yazı suya düşer: 'SAHİP' kelimesi yansımanın ağzına oturur. Söz geri döndü",
  [('E08@döndü', "kelime suya değer, yansımanın dudaklarında durur")],
  CUT, "yazı: SAHİP (suda) · künye: copia · III 391 / 466 (üst yarı)", "çok yavaş yaklaşma", "", True),
 ('E09', 'HAVUZ', 'ters açı',
  "Tepeden: figür ve yansıması. 'Keşke bedenimden ayrılabilsem'",
  [('E09@ayrılabilsem', "akıntı yansımayı hafifçe uzaklaştırır, figür ona uzanır"), ('E09@dilek', "suya bir yaprak düşer"), ('E09@uzak', "yansıma geri gelir, figür elini çeker")],
  CUT, "künye küçük: Ovidius, Dönüşümler III 467 (alıntı altyazıda; ekranda alıntı yazısı yok)", "tepeden bakış; yavaş yatay kayma (dönme yok)",
  "Bedenden ayrılan hayalet/ruh figürü yok", False),
 ('E10', 'KEHANET', 'yakın',
  "Hatıra, beyaz zeminde (lekythos beyazı, solgun sepya; P057 ile aynı hatıra dili): B02'nin kompozisyonu, Tiresias'ın profili; aynı Türkçe dipinto",
  [('E10@kendini', "dipinto KENDİNİ TANIMAZSA yeniden belirir")],
  FADE(.6), "dipinto: KENDİNİ TANIMAZSA (alıntı yazısı ayrıca yok)", "B02 çizimi (P010) beyaz zemin paletiyle yeniden kullanılır; çok yavaş uzaklaşma", "", False),
 ('E10@şimdi', 'HAVUZ', 'orta',
  "Aynı Türkçe yazı havuzun yüzünde yansır (P012'deki ters dönen KENDİNİ TANI'nın karşılığı): KENDİNİ TANIMAZSA → TANIDI. Halka yok (gözyaşı halkası P062'ye saklı)",
  [('E10@tanıdı', "yazı suda ters döner; TANIMAZSA'nın sonu düşer: TANIDI"), ('E10@kurtarmadı', "yazı halkasız batar ve suyun içinde söner")],
  CUT, "yazı: KENDİNİ TANIMAZSA → TANIDI (suda)", "yavaş aşağı kayma", "", True),
 ('E11', 'HAVUZ', 'yakın',
  "Gözyaşı halkası (kapı D_halka): filmde damla + halka + yüzün dağılması yalnız burada. Damla düşer, halka yansımayı dağıtır, yüz koyu lekeye dağılır",
  [('E11@gözyaşları', "gözyaşı düşer"), ('E11@suyu', "halka doğar"), ('E11@dağılır', "yansıma yatay dalga kaydırmasıyla koyu lekeye dağılır")],
  CUT, "", "gözden suya, damlayı izleyen aşağı kayma",
  "İlk halka baştan ≥ 60 px uzak (hale); bloklu kırılma 'dijital bozulma' okunursa yatay dalgaya dön (tur 3, madde 5)", False),
 ('E12', 'HAVUZ', 'ters açı',
  "Suyun içinden yukarı (elin altından): dağılmış yansımanın yerinden yüzeye bakarız; yüzeyin üstünde açık avuç, onun ötesinde soluk gök ve genç. P062'nin yakın planından eksen ve ölçek değişir",
  [('E12@kal', "el yüzeyin hemen üstünde durur, dokunmaz; parmak uçlarının gölgesi suya düşer"), ('E12@bakayım', "yüzey durulur; el ve yüz yukarıda toparlanır")],
  CUT, "", "sudan yukarı, çok yavaş yükselme", "", False),
 ('E13', 'HAVUZ', 'ayrıntı',
  "Kıyıdaki ot yaprağında kırağı: güneş vurur, kırağı erir (benzetme sahnede)",
  [('E13@bakar', "güneş ışığı yaprağa ulaşır"), ('E13@kırağı', "kırağı parlar, erimeye başlar"), ('E13@erirse', "damla suya düşer")],
  CUT, "", "yaprak boyunca yatay kayma", "", False),
 ('E13@o', 'HAVUZ', 'orta',
  "İncelme (kayboluş değil): kahramanın dönüşümü 'o da aşkla'dan başlar. Beden yerinde kalır; kil kırmızısı solar, kenarlar yumuşar ve çevresinde polen gibi ışık noktaları belirir. P067 (ah), P068 (son söz) ve P070 (baş otlara) aynı, incelmiş bedeni gösterir; kayboluş P073–P074'te",
  [('E13@aşkla', "renk solmaya başlar"), ('E13@incelir', "kenarlar yumuşar, çevresinde ışık noktaları"), ('E13@erir#1', "beden soluk ve ince, ama yerinde; ışık noktaları havada kalır")],
  CUT, "", "çok yavaş uzaklaşma",
  "Zayıflamış beden estetiği yok (kaburga, çökük yüz, iskelet); incelme ışık ve renkle", False),
 ('E14', 'DAG', 'ters açı',
  "Eko'nun bakışı: kayaların arasından uzaktaki kıyı. Eko görünmez (bedeni yok, yalnız ses)",
  [('E14@böyle', "kayaların arasından kıyıya bakış"), ('E14@kırgınlığını', "kayanın yüzünde soluk kırmızı profil çizgisi"), ('E14@üzülür', "kayadan küçük bir taş düşer")],
  CUT, "", "yavaş yatay kayma (bakış)", "", False),
 ('E14@narkissos', 'HAVUZ', 'orta',
  "Kıyıdaki son ışık: incelmiş, soluk Narkissos (P065'teki beden) 'ah' der, kayalardan yankı döner",
  [('E14@ah', "dipinto AH ağzından"), ('E14@ah#1', "AH kayalardan soluk kırmızı geri döner")],
  CUT, "", "hafif yatay kayma", "", False),
 ('E15', 'HAVUZ', 'yakın',
  "Son bakış: incelmiş, soluk beden (P065'ten beri) suya son sözü söyler",
  [('E15@ah', "dipinto AH, BOŞUNA SEVİLEN ÇOCUK! yansımaya doğru"), ('E15@elveda', "ELVEDA, yazı suya iner")],
  CUT, "", "yüzden suya yavaş aşağı kayma (yazıyı izler)", "", False),
 ('E15@eko', 'DAG', 'geniş',
  "Dağlar: ELVEDA yankısı yamaçtan yamaca, her tekrarda solarak (ELVEDA · elveda · eda)",
  [('E15@elveda#1', "ELVEDA dağlardan döner, üç kez solarak tekrar eder")],
  CUT, "", "yatay kaydırma", "", False),
 ('E16', 'HAVUZ', 'orta',
  "İncelmiş beden başını yeşil otların üstüne bırakır; ışık söner. Beden hâlâ yerinde (kayboluş P073'te). Sakin, korkutucu değil",
  [('E16@bırakır', "baş otlara iner"), ('E16@ölüm', "ışık söner, su kararır")],
  CUT, "", "çok yavaş yaklaşma", "Ceset, ölü yüz yakın planı yok; baş otlarda, uzaktan", False),
 ('E16@ölüler', 'YERALTI', 'geniş',
  "Styks: karanlık su, figürsüz. Suyun yüzünde soluk bir yüz parıltısı",
  [('E16@stiks', "etiket; yatay dalga çizgileri kıpırdar"), ('E16@kendine', "karanlık suda soluk oval bir parıltı (yüz)"), ('E16@eder', "parıltı kaybolmaz, yerinde titrer")],
  CUT, "etiket: STYKS", "yatay kaydırma",
  "Ölüler diyarı figürsüz ve simgesel; kayıkçı, kafatası, iblis yok", False),
 ('E17', 'HAVUZ', 'orta',
  "Kıyıda periler ağıt yakar (ayakta, elleri başlarında: Yunan ağıt jesti); dağlardan yankı",
  [('E17@ağıt', "periler ellerini başlarına götürür"), ('E17@yankısıyla', "yamaçlardan soluk dipinto yankı")],
  CUT, "", "yatay kaydırma",
  "Periler dağınık; sıra hâlinde eğilen dizi yok. Saç yolma, yüz tırmalama yok", False),
 ('E17@bedeni', 'HAVUZ', 'yakın',
  "Kayboluş burada: başın bırakıldığı ot yatağında yalnız P065'teki ışık noktaları kalmıştır; peri otları aralarken son noktalar havalanır ve söner. Beden yok",
  [('E17@aradıklarında', "bir peri otları aralar; ışık noktaları havalanır"), ('E17@yoktur', "son nokta söner; eli boş yere değer")],
  CUT, "", "hafif yatay kayma", "", False),
 ('E17@yerinde', 'HAVUZ', 'ayrıntı',
  "Bedenin yerinde, son ışık noktasının söndüğü yerde nergis açar: beyaz, oval, düzensiz taç yapraklar; safran göbek. Çiçek suya eğilir ve yansır",
  [('E17@safran', "göbek safran sarısına döner"), ('E17@beyaz', "beyaz yapraklar açılır"), ('E17@çiçek', "çiçek suya eğilir, yansıması belirir")],
  CUT, "", "çok yavaş yaklaşma",
  "Yandan ya da ¾ açı: önden simetrik altı köşeli yıldız okunmasın; yapraklar düzensiz ve üst üste", False),

 # ───────────── F · Ad (birleştirme; ders anlatısı değil) ─────────────
 ('F01', 'HAVUZ', 'yakın',
  "Nergis kıyıda; vazo ressamının yazdığı ad şimdi çiçeğin yanında (A02'deki ΝΑΡΚΙΣΣΟΣ etiketinin karşılığı). Ekranda aynı anda tek ad: Yunanca ad aynı yerde Latince botanik ada döner",
  [('F01@nergisin', "bölüm kartı söndükten sonra dipinto ΝΑΡΚΙΣΣΟΣ çiçeğin yanında belirir"), ('F01@narkissus', "harfler aynı yerde Latince botanik ada döner: Narcissus (italik)")],
  CUT, "bölüm kartı: AD (ilk 2 sn, tek başına) · etiket: dipinto ΝΑΡΚΙΣΣΟΣ → Narcissus (tek ad, aynı yerde)", "çok yavaş yaklaşma", "", False),
 ('F01@peki', 'HAVUZ', 'orta',
  "Kamera nergisten geri çekilir: kıyıda nergis ve suda yansıması. Bölümün sorusu üst yarıda; ad harfleri gevşer ve suya dökülür, akıntı onları kadraj dışına (belgelere) taşır",
  [('F01@gencin', "ΝΑΡΚΙΣΣΟΣ harfleri gevşer"), ('F01@kelimeye', "harfler suya dökülür, akıntıyla sağa uzaklaşır")],
  CUT, "soru: Bir gencin adı nasıl bir kelimeye dönüştü? (üst yarı)", "yavaş uzaklaşma", "", False),
 ('F02', 'BELGE', 'geniş',
  "Tempesta 1606 (Met 401131, CC0), beyaz zemin lekythos çerçevesi içinde. Çerçevenin sağ alt köşesinde küçük sepya Narkissos (beyaz zemin vazo çizgisi, havuz başında uzanmış): F02–F05'in bütün belge planlarında aynı köşede kalır ve her belgede ona bir şey olur",
  [('F02@ahlak', "bordür kendini çizer; kamera yaklaşır; köşedeki sepya Narkissos suya eğilir"), ('F02@bin', "çerçevenin köşesinde yıl")],
  FADE(.6), "künye: Antonio Tempesta, 1606 · The Met, CC0", "yavaş yaklaşma (≤ %10)", "", False),
 ('F02@basılan', 'BELGE', 'orta',
  "Callot / 1646 levhası (Met 419135; yalnız resim + üst satır kırpılır) aynı çerçevede; köşede sepya Narkissos. 1646'da ona olan: levhanın ahlak satırı kalkar ve onun bedeninin üstüne biner",
  [('F02@kitabında', "levha çerçeveye oturur"), ('F02@gravürünün', "üst satır levhadan kalkar, köşedeki sepya Narkissos'un gövdesinin üstüne bir etiket gibi çapraz iner ve orada kalır")],
  CUT, "künye: Jacques Callot, Lux Claustri · 1646 baskısı · The Met, CC0", "yukarı kayma",
  "Levhadaki diz üstü eğilen figür hassasiyet bakışından geçer; secde okunursa kırpılır, yalnız üst satır kalır. Satır başın üstünde yatay şerit olarak durmaz (hale okunmasın), gövdeye çapraz", False),
 ('F02@aşırı', 'BELGE', 'ayrıntı',
  "Üst satırın yakını: L'excez de l'Amour propre est cause de sa perte; satırın altında sepya Narkissos'un gövdesi (yazı onun üstünde, çapraz)",
  [('F02@kendi', "satırın altı vazo kırmızısıyla çizilir"), ('F02@sebebidir', "Türkçe çeviri belirir")],
  CUT, "alıntı: “Aşırı öz-sevgi, kendi yıkımının sebebidir.” (çevirimiz)", "satır boyunca yatay kayma", "", True),
 ('F03', 'BELGE', 'orta',
  "Beyaz zemin lekythos: sepya Narkissos havuz başında (köşeden çerçevenin ortasına büyür); 1646'nın ahlak satırı üstünden silinir. Mit bir vaka notuna döner: 1898'de kenar notu ve Ellis kırpması ayrı levha olmadan figürün yanında belirir (Fable 5.2 numarasıyla P080 bu plana bindirildi)",
  [('F03@sonunda', "ahlak satırı figürün üstünden silinir"), ('F03@tıbbın', "figürün yanına el yazısı bir kenar notu çizilir (okunmaz çizgiler)"), ('F03@ingiliz', "Ellis 1898 cümle kırpması kenar notunun yerine, figürün yanına oturur: “This Narcissus-like tendency … self-admiration” (makale başlığı yok)"), ('F03@narkissos', "“Narcissus-like” kırmızı halkayla çizilir"), ('F03@eğilim', "halka kapanır; sepya Narkissos hiç kıpırdamadan suya bakar")],
  CUT, "yazı: Ellis kırpması (figürün yanında) · künye: Havelock Ellis · 1898", "yavaş yatay kayma, sonra kırpmaya doğru yavaş yaklaşma",
  "Ellis'in 'kadınlarda ayna' çerçevesi kırpmada yok", False),
 ('F03@bir#2', 'YAZI', 'yakın',
  "1899'da ona olan: F03'teki sepya Narkissos'un yanında ad etiketi değişir: dipinto ΝΑΡΚΙΣΣΟΣ → Narcismus → narsisizm",
  [('F03@alman', "ΝΑΡΚΙΣΣΟΣ'un yanına el yazısıyla Narcismus"), ('F03@narsisizm', "Narcismus → narsisizm (Türkçe)")],
  CUT, "künye: Paul Näcke · 1899 · yazı: Narcismus → narsisizm", "çok yavaş yaklaşma", "", True),
 ('F04', 'YANKI', 'geniş',
  "Bugün: siyah sır zemin; 'narsist' kelimesi Eko'nun yankısı gibi her yönden, farklı boylarda belirip solar. Kişi yok",
  [('F04@narsist', "ilk yazı belirir"), ('F04@kelimesini', "yazılar çoğalır"), ('F04@duyuyoruz', "yazılar her yönden, üst üste")],
  FADE(.6), "yazı: narsist (yankı yazıları, y < 880)", "hafif yatay kayma",
  "Parmakla gösterme, yüz, alay yok; kelime kimseye yapışmaz", True),
 ('F04@ama', 'HAVUZ', 'orta',
  "Çekinceyi görüntü söyler: P082'nin 'narsist' yazıları alacakaranlıktaki pınarın üstüne yağar; hiçbir şeye ve kimseye yapışmadan suya düşer ve söner. Figür yok",
  [('F04@ama', "yazılar yukarıdan, kesmenin içinden düşmeye devam eder"), ('F04@uzmanın', "ilk yazılar suya değer ve iz bırakmadan söner (halka yok)"), ('F04@tanıdır', "son yazı söner; su boş")],
  CUT, "", "çok yavaş yatay kayma", "Hasta, doktor, ilaç, beyin görseli yok", False),
 ('F04@bu#1', 'HAVUZ', 'ayrıntı',
  "Kıyıdaki nergis; su durulur. Bu hikâye kimseye teşhis koymaz",
  [('F04@kimseye', "nergisin yansıması netleşir"), ('F04@koymaz', "nergis hafifçe suya eğilir")],
  CUT, "", "çok yavaş yaklaşma", "", False),
 ('F05', 'BELGE', 'yakın',
  "Freud 1914 ilk sayfa (Jahrbuch VI, archive.org, kamu malı) beyaz zemin çerçevede; köşede sepya Narkissos (artık adı narsisizm). Başlığın sorusu bu planın sonunda eylem olarak gelir (Fable 5.2 numarasıyla P085 levhası kaldırıldı)",
  [('F05@froyd', "başlık 'Zur Einführung des Narzißmus' kırmızıyla çizilir"), ('F05@başta', "kamera sayfadan geri kayar"), ('F05@soruya', "sayfanın kenarında, sepya Narkissos'un yanında başlığın sorusu kırmızı fırçayla yazılır"), ('F05@cevabını', "sorunun altında boş bir şerit açılır (cevap yeri)")],
  FADE(.6), "künye: Sigmund Freud · Narsisizm Üzerine, 1914 · yazı: Kendini sevmek ne zaman narsisizme döner?", "yavaş yaklaşma, 'başta'dan sonra geri kayma", "Freud portresi yok", False),
 ('F06', 'DERE', 'orta',
  "Adsız bir çocuk (vazo dilinde; mitte yok, temsilî görsel): köy kenarında sığ dereye eğilir, yansımasına güler, kalkıp patikadaki arkadaşlarına koşar. Olağan: bakar ve gider. Genç Narkissos sanılmaz: 7–8 yaş oranı (baş büyük, boy onun yarısı), kısa düz saç, alında bant yok, kemerli kısa tunik (khiton değil), elinde çember (trokhos: vazo resminde çocuk oyuncağı). Arkadaki patika P005 ve P054'teki patikanın biçiminde: 'gitmek' motifi üçüncü kez ve cevabıyla",
  [('F06@birincil', "çocuk suya eğilir, yansımasını görür"), ('F06@kendini', "yansımasına güler"), ('F06@hastalık', "kalkar, çemberini alır, patikaya koşmaya başlar"), ('F06@olağan', "kadrajdan çıkmıştır: uzakta patikada arkadaşlarının yanında; kıyıda yalnız dalgalanan su")],
  FADE(.6), "", "koşuyu izleyen yatay kaydırma, 'olağan'da patikada durur",
  "Çocuk giyinik; tek başına gösterilmez, arkadaşları baştan sona kadrajda (patikada). Mitte yok: temsilî görsel", False),
 ('F07', 'HAVUZ', 'orta-yakın',
  "Kapalı pınar: kıyı ve su yüzü. Akıntısı yok; su yükselir, dışarı akmaya çalışır ama akamaz, kendi içinde döner. Freud'un ilk cümlesi beyaz kartta değil, yükselen suyun üstünde belirir (Fable 5.2 numarasıyla P088 kaldırıldı)",
  [('F07@ölçüyü', "su seviyesi kıyıya kadar yükselir"), ('F07@dışarıya', "kıyıda bir oluk açılmaya çalışır"), ('F07@akamadığında', "su dışarı akmaz, halkalar içe döner"), ('F08@güçlü', "suyun yüzeyinde ilk cümle sepya fırçayla satır satır belirir"), ('F08@korur', "künye belirir; su seviyesi durur")],
  FADE(.6), "alıntı: “Güçlü bir benlik sevgisi insanı hastalığa karşı korur.” (suyun üstünde) · künye: Freud, 1914 · s. 11 (çevirimiz)", "yavaş yatay kayma", "", False),
 ('F08@ama', 'HAVUZ', 'geniş',
  "Aynı pınar, geniş: kıyıdaki oluk açılır, su dışarı, ormana doğru akar; akıntı ağaçların arasına ulaşır",
  [('F08@sevmeye', "oluk açılır, su akmaya başlar"), ('F08@gerekir', "akıntı ormana ulaşır")],
  CUT, "alıntı: “Ama sonunda, hastalanmamak için sevmeye başlamak gerekir.”", "akıntıyı izleyen yatay kayma", "", False),
 ('F08@engellendiği', 'HAVUZ', 'yakın',
  "Akıntı bir taşa takılır; su geri döner, yüzey kapanır, yalnız yansıma kalır",
  [('F08@sevemeyen', "su taşa çarpar, geri döner"), ('F08@hastalanır', "yüzey kapanır")],
  CUT, "künye küçük: Freud, 1914 (üçüncü cümle yalnız altyazıda; görüntü söyler: akıntı taşa takılır, yüzey kapanır)", "çok yavaş yaklaşma", "", False),
 ('F09', 'HAVUZ', 'geniş',
  "Karşıtlık (kapak B): solda ışıkta suya bakan Narkissos, sağda karanlıkta kayaya karışmış Eko",
  [('F09@bağı', "kamera ikisini birlikte alacak biçimde kayar"), ('F09@bilgi', "Narkissos'un yüzündeki ışık sabit, Eko'nun kayası gölgede")],
  CUT, "", "yatay kaydırma", "", False),
 ('F09@onu', 'DAG', 'orta',
  "Eko'nun kayası yakından: dipinto yankılar kayadan Narkissos'a doğru akar",
  [('F09@ses', "kayadan soluk kırmızı AH yazısı çıkar"), ('F09@ahına', "yankılar kıyıya doğru akar")],
  CUT, "", "yatay kayma kayadan kıyıya", "", False),
 ('F09@oysa', 'HAVUZ', 'yakın',
  "Narkissos'un gözü suda; arkasında yankı yazıları söner",
  [('F09@ayıramadı', "yankılar söner, göz sudan ayrılmaz")],
  CUT, "", "paralaks: arkadaki yankı yazıları kayar, göz sabit", "", False),
 ('F10', 'HAVUZ', 'ters açı',
  "Tepeden: figür ve yansıması kapalı bir halka gibi; sevgi sudan dışarı çıkamaz",
  [('F10@kendini', "figür ve yansıma tek halka biçimi kurar"), ('F10@sevgisi', "havuzun kenarı içe kapanır"), ('F10@çıkamadı', "halka kapanır")],
  CUT, "", "tepeden yavaş yatay kayma", "Halka bir figürün başının çevresinde değil, iki bedenin çevresinde (hale okunmasın)", False),
 ('F10@ovidius', 'HAVUZ', 'orta',
  "D08'in togalı şairi kıyının kenarında; sözünü tekrar eder ve uzaklaşır. Genç kalır",
  [('F10@seninle', "şair elini gence uzatır"), ('F10@gidebilirsen', "şair döner ve gider; genç kıpırdamaz")],
  CUT, "alıntı: “Seninle gider; eğer sen gidebilirsen.” · künye: Ovidius, III 436", "yatay kayma", "", False),
 ('F11', 'CAM', 'orta-yakın',
  "Çerçeve kapanır: havuzun kıyısı telefonun kenarına döner (kapı E), camda bugünün genci ve yansıması, P001'le aynı eksen. Çapalar F11'in yeniden hizalanmış kelime zamanlarına göre (vo/oneri; eski hizalamada F11 4,9 sn'ye sıkışmıştı)",
  [('F11@camda', "havuz → cam biçim dönüşümü başlar"), ('F11@biliyorsun', "dönüşüm biter: camda genç ve birebir yansıması"), ('F11@yeter', "genç durur; gözü camda"), ('F11@yorumlara', "ekran ışığı kararmaya başlar")],
  CUT, "", "kapı E: havuz yakınından telefon kadrajına açılır, sonra çok yavaş yaklaşma",
  "Telefon bölümünde ahlak dersi yok: el telefonu bırakmaz ya da fırlatmaz; soru açık kalır. Beğeni sayacı, logo yok", False),
 ('F12', 'HAVUZ', 'ayrıntı',
  "Kıyıdaki nergis suya eğik (E17'nin karşılığı): bilmek yetmedi",
  [('F12@yetmedi', "nergis suya biraz daha eğilir")],
  CUT, "", "nergis boyunca yavaş aşağı kayma", "", False),
 ('F12@sisifosa', 'FRIZ', 'orta',
  "Vazo frizinde Sisifos taşı yokuşa iter (kanalın Sisifos videosunun silueti, aynı vazo dili). 'Ekranda' denmeden Sisifos silueti bitiş ekranındaki yerine oturur: P099'a kesme görünmez, yalnız zemin kararır",
  [('F12@yetti', "taş tepeye yaklaşır"), ('F12@mi', "friz küçülerek sol alta kaymaya başlar"), ('F12@hikayesi', "Sisifos silueti bitiş ekranındaki yerine oturmuştur; sağ ve üst boş")],
  CUT, "", "yatay kaydırma", "", False),
 ('F12@ekranda-0.22', 'SON', 'geniş',
  "Bitiş ekranı (son 20 sn): siyah sır zemin; solda küçük Sisifos frizi ağır ağır döner, altta ince meander bandı; orta-sağ ve üst boş (video kutusu, abone düğmesi)",
  [('F12@ekranda', "Sisifos frizinin altından çıkan kırmızı nokta video kutusunun alt kenarına koşar ve orada durur: önerilen video orada"), ('F12@geçmişten', "nokta, arkasında meander bandı bırakarak video kutusunun altında soldan sağa çizer"), ('F12@devam', "bant video kutusunun sağ kenarını geçer"), ('F12@abone', "bant abone düğmesinin altına ulaşır; nokta bir kez nabız atar"), ('F12@ol+4', "friz döner: Sisifos'un taşı tepeye ulaşır"), ('F12@ol+8.5', "taş geri yuvarlanmaya başlar (döngü; anlatım bitti, sessiz döngü bitiş ekranı için)")],
  CUT, "", "vazo frizi çok yavaş döner (19 sn, kesmesiz)",
  "Yazı ve figür YouTube öğelerinin altına düşmez; ekran yazısı yok", False),
]

# ── çapa çözümü (film.js A() / Wd() ile aynı) ──
norm = lambda w: re.sub(r'[^\wçğıöşü]', '', w.lower().replace('â', 'a').replace('î', 'i').replace('û', 'u'))
UYARI = []
def A(at, kim=''):
    m = re.match(r'^([A-Z]\d+[a-z]?)(?:@([^#+-]+)(?:#(\d+))?)?([+-][\d.]+)?$', at)
    if not m: raise SystemExit(f'çapa yazımı bozuk: {at} ({kim})')
    sid, w, n, off = m.group(1), m.group(2), int(m.group(3) or 0), float(m.group(4) or 0)
    if sid not in CUES: raise SystemExit(f'cümle yok: {at} ({kim})')
    t = CUES[sid]['s']
    if w:
        nw = norm(w); hits = [x for x in WORDS if x['id'] == sid and x['w'].startswith(nw)]
        if len(hits) <= n: raise SystemExit(f'kelime bulunamadı: {at} ({kim})')
        if hits[n]['w'] != nw: UYARI.append(f'{kim} {at}: "{nw}" önek olarak "{hits[n]["w"]}" kelimesine takıldı')
        t = hits[n]['s']
    return round(t + off, 2)

planlar, rows = {}, []
for i, (at, st, ol, ne, ey, tr, yazi, kam, has, lev) in enumerate(P):
    pid = f'P{i + 1:03d}'; harf = at[0]
    assert st in SETLER, st
    planlar[pid] = {'at': at, 'set': st, 'olcek': ol, 'ne': ne, 'eylem': [{'at': a, 'ne': e} for a, e in ey], 'tr': tr, 'yazi': yazi,
                    'kamera': kam, 'hassasiyet': has, 'levha': lev, 'bolum': BOLUM[harf], 'sahip': SAHIP[harf]}
    rows.append((pid, A(at, pid)))

# sıra, süre, eylem pencereleri
hata = []
T = [t for _, t in rows]
for k in range(1, len(T)):
    if T[k] <= T[k - 1]: hata.append(f'sıra bozuk: {rows[k - 1][0]} {T[k - 1]} → {rows[k][0]} {T[k]}')
sure = {}
for k, (pid, t) in enumerate(rows):
    end = T[k + 1] if k + 1 < len(T) else DUR
    sure[pid] = (t, round(end - t, 2))
    for e in planlar[pid]['eylem']:
        te = A(e['at'], pid)
        e['_t'] = te
        if not (t - 1e-6 <= te < end): hata.append(f'{pid} eylemi plan dışında: {e["at"]} = {te} (plan {t}–{end})')
# ardışık ölçek
for k in range(1, len(rows)):
    a, b = planlar[rows[k - 1][0]]['olcek'], planlar[rows[k][0]]['olcek']
    if a == b: hata.append(f'ardışık aynı ölçek: {rows[k - 1][0]} ve {rows[k][0]} ({a})')
# yenilik aralıkları: kesme ya da sözcüğe bağlı eylem olmadan geçen süre
isaret = sorted(set([t for _, t in rows] + [e['_t'] for p in planlar.values() for e in p['eylem']] + [DUR]))
bosluk = []
for a, b in zip([0.0] + isaret, isaret):
    if b - a > 5.0:
        pid = max((p for p, t in rows if t <= a + 1e-6), key=lambda p: sure[p][0], default=rows[0][0])
        bosluk.append((round(a, 2), round(b, 2), round(b - a, 2), pid))
# levha
lev = [(p, sure[p][1]) for p in planlar if planlar[p]['levha']]
lev_top = sum(d for _, d in lev)
for p, d in lev:
    if d > 8.0: hata.append(f'yazı levhası 8 sn üstünde: {p} {d}')
# yazı yoğun: levha, ya da alıntı/soru/yazı katmanı, ya da iki ve daha çok yazı kalemi (dipinto dahil). Altyazı açık izleyicide (≈%38) üçlü yazı yükü
for pid, t in rows:
    p = planlar[pid]
    kalem = len(re.findall(r'(alıntı|soru|yazı|yazıt|dipinto|etiket)\s*:', p['yazi']))   # bölüm kartı sayılmaz: plan başında 2–3 sn tek başına durur, öbür yazılar ondan sonra gelir
    dip = any('dipinto' in e['ne'] for e in p['eylem']) and 'dipinto' not in p['yazi']
    p['yazi_yogun'] = bool(p['levha'] or re.search(r'(alıntı|soru|yazı|yazıt)\s*:', p['yazi']) or kalem + dip >= 2)
yy_ard = [(rows[k - 1][0], rows[k][0]) for k in range(1, len(rows)) if planlar[rows[k - 1][0]]['yazi_yogun'] and planlar[rows[k][0]]['yazi_yogun']]
yazili = [pid for pid, _ in rows if planlar[pid]['yazi'] or any('dipinto' in e['ne'] for e in planlar[pid]['eylem'])]
# fiilen aynı boy: yakın ↔ orta-yakın komşuluğu aynı sette (doğrulayıcı uyarısı; Fable 5.2)
yakin_ard = [(rows[k - 1][0], rows[k][0]) for k in range(1, len(rows))
             if {planlar[rows[k - 1][0]]['olcek'], planlar[rows[k][0]]['olcek']} == {'yakın', 'orta-yakın'} and planlar[rows[k - 1][0]]['set'] == planlar[rows[k][0]]['set']]
for e in planlar.values():
    for x in e['eylem']: x.pop('_t', None)

if TL:   # yalnız doğrulama
    print('TL doğrulama:', TL, '| plan', len(planlar), '| levha', round(lev_top, 1), f'%{100 * lev_top / DUR:.1f}', '| en uzun levha', max(d for _, d in lev))
    print('boşluklar:', bosluk); print('art arda yazı yoğun:', yy_ard); print('yakın↔orta-yakın aynı set:', yakin_ard)
    print('uyarı:', UYARI); print('HATA:', hata if hata else 'yok'); raise SystemExit(1 if hata else 0)
kok = ROOT
json.dump(planlar, open(os.path.join(kok, 'planlar.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(os.path.join(kok, 'planlar.js'), 'w', encoding='utf-8').write('// tools/planlar_kaynak.py tarafından üretildi\nwindow.PLAN = ' + json.dumps({k: {'id': k, **v} for k, v in planlar.items()}, ensure_ascii=False) + ';\n')

# ── planlar.md ──
def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'.replace('.', ',')
def vf(x, n=1): return f'{x:.{n}f}'.replace('.', ',')
def trs(tr): return 'kesme' if tr['type'] == 'cut' else f"{tr['type']} {vf(tr['dur'])} sn (sessizlikte biter)" if tr.get('end') else f"{tr['type']} {vf(tr['dur'])} sn"
def esc(s): return str(s).replace('|', '/').replace('\n', ' ')
L = []
L.append('# Narkissos: plan listesi\n')
L.append(f'Üretici: `tools/planlar_kaynak.py` (bu dosyayı elle düzeltme; kaynağı düzeltip yeniden çalıştır). Çıktılar: `planlar.json` (film.js `PA()` yazımı), `planlar.js` (`window.PLAN`), bu tablo. Zamanlar `timeline.js`ten (DUR {vf(DUR)} sn = {mmss(DUR)}); süre bir sonraki planın çapasına kadardır.\n')
L.append('## Özet\n')
olc = Counter(p['olcek'] for p in planlar.values())
ortalama = DUR / len(planlar)
L.append(f'- **{len(planlar)} plan**, ortalama {vf(ortalama)} sn; en kısa {vf(min(d for _, d in sure.values()))} sn ({min(sure, key=lambda p: sure[p][1])}), en uzun {vf(max(d for _, d in sure.values()))} sn ({max(sure, key=lambda p: sure[p][1])}).')
L.append(f'- Ekran yazısı ya da dipinto olan plan: {len(yazili)}; yazı yoğun (yy): {sum(1 for p in planlar.values() if p["yazi_yogun"])} plan, art arda iki yy: {len(yy_ard)} çift (aşağıda gerekçeleriyle).')
L.append('- Ölçekler: ' + ', '.join(f'{k} {v}' for k, v in olc.most_common()) + '. Ardışık iki plan aynı ölçekte değil (doğrulayıcı denetler).')
L.append(f'- Yazı levhası (yazının ana içerik olduğu plan; Fable 5.2\'nin "fiilen yazı planı" saydıkları dahil): {len(lev)} plan ({", ".join(p for p, _ in lev)}), toplam {vf(lev_top)} sn = %{vf(100 * lev_top / DUR)} (sınır %20); en uzunu {vf(max(d for _, d in lev))} sn (sınır 8 sn). Boş kâğıt planı yok.')
L.append(f'- Bitiş ekranı {mmss(BITIS)}–{mmss(DUR)} ({vf(BITIS)}–{vf(DUR)} sn); "ekranda" {mmss(A("F12@ekranda"))}. Görev metnindeki "8:11,9–8:31,9" DUR 531,9 ile uyuşmuyor; doğrusu 8:31,9–8:51,9.')
L.append('- Sahipler: SAHİP-1 A–C (Cam, Kehanet, Yankı), SAHİP-2 D–F (Havuz, O benim, Ad).')
for s in ('SAHİP-1', 'SAHİP-2'):
    ps = [p for p in planlar if planlar[p]['sahip'] == s]
    L.append(f'  - {s}: {len(ps)} plan ({ps[0]}–{ps[-1]}), {vf(sum(sure[p][1] for p in ps), 0)} sn; setler: ' + ', '.join(f'{k} {v}' for k, v in Counter(planlar[p]["set"] for p in ps).most_common()))
L.append('- **Set kodu sahipliği:** HAVUZ ve CAM kapıdaki `kapi/vazo/nark.js`ten (`phoneScene`, `dScene`, `mirror`, `warpRings`, `proneFig`) gelir ve iki sahip de kullanır (SAHİP-1 A bölümünde 5 HAVUZ ve 1 CAM planı çizer). Öneri: başkan bunları dağıtımdan önce ortak `lib/sahne/havuz.js` ve `cam.js`e taşır; sahipler yalnız kendi plan dosyalarına yazar. Hatıra planları (E08 → P026, E10 → P010, F10@ovidius → P044) özgün planın çizim işlevini çağırır.')
L.append('- **İş yükü:** bölüm sınırıyla bölüşüm dengesiz (yukarıdaki saniyeler). İstenirse dengeleme: F bölümünün düz 2B planları (BELGE, YAZI, YANKI F04) SAHİP-1\'e verilir; HAVUZ\'un ve sepya Narkissos\'un sürekliliği SAHİP-2\'de kalır.')
L.append('- **Engelleyici: hizalama (F11 ve fazlası).** Fable 5.2: F11 19 kelime 4,9 sn\'de. Dalga biçiminden yeniden ölçüldü (`tools/hizala_cumle.py`, cümle düzeyinde): sorun yalnız F11 değil. `hizala.py` yalnız senaryo kimliği sınırlarını sessizliğe oturtuyordu; kimlik içindeki cümleler sayılmadığı için sınırlar bir iki cümle kaydı (s08\'de F05 F06\'nın ilk cümlesini, F10 F11\'in ilk iki cümlesini taşıyordu). Yeni hizalamada bütün alt cümleler 0,055–0,095 sn/harf bandında ya da yanında (eskisinde 18 kimlik bandın dışındaydı). Öneri dosyaları `vo/oneri/` (çekim başına `*.words.json` ve `timeline_oneri.js`); `timeline.js`e dokunulmadı (görev kuralı). Uygulama başkanda: `cp vo/oneri/s0*.words.json vo/ && python3 tools/build_vo.py && python3 tools/planlar_kaynak.py && python3 tools/srt.py`. Ses örnekleri yerinde kalır, DUR değişmez (531,9); yalnız cümle sınırları ve plan.json boşluklarının yeri değişir. Plan listesi iki zaman çizelgesiyle de hatasız doğrulandı (`TL=vo/oneri/timeline_oneri.js python3 tools/planlar_kaynak.py`). Bu tablodaki zamanlar şimdiki `timeline.js`ten; değişen cümlelerin yeni zamanları aşağıda, "Hizalama önerisi" bölümünde.')
L.append('- **Araç uyumu:** `tools/plan_zaman.py` `animatik/planlar.json`daki eski liste biçimini okur; bu dosya kimlik → plan sözlüğüdür (`P = [dict(id=k, **v) for k, v in json.load(...).items()]`).')
L.append('\n## Genel kurallar (her plan)\n')
L.append('- **Donuk plan yok:** her plan ilk kareden hareketlidir: varsayılan çok yavaş yaklaşma (≤ %10, ≥ 6 sn) ya da yatay kayma (ikisi birden değil) + aşağıdaki sözcüğe bağlı eylemler. Kamera sütunu yönü verir.')
L.append('- **Çapa yazımı** `film.js` `A()` ile aynı; kelime eşlemesi önekle (`startsWith`) yapılır. Kısa önekler (o, ve, bir, ses) önceki kelimeye takılır: kodda olay saati `Wd()`/`A()` ile alınır, sabit saniye yazılmaz.')
L.append('- **Geçiş:** aynı mekânda kesme; yumuşak geçiş (`fade`, ≤ 0,7 sn, sessizlikte biter) yalnız mekân ya da zaman sıçramasında. İki levha saydamlıkla karışmaz. Cam ↔ havuz geçişi plan içi biçim dönüşümüdür (P001, ' + [k for k, v in planlar.items() if v['at'] == 'F11'][0] + '), kesme değil.')
L.append('- **Yazılar** `over` katmanında; x 120–1800, y 90–880 (y > 880 altyazının). Alıntı ≥ 64 px, etiket ≥ 40 px. Bölüm kartı yalnız başlık, sahnenin üstünde 2–3 sn, tek başına (F01\'in sorusu kartta değil, P076\'da sahnenin üstünde).')
L.append('- **Dipinto (yankı dili):** vazo geleneğinde ağızdan çıkan fırça yazısı; Eko\'nun yankısı yalnız son sözleri, her tekrarda solarak. `prometheus/lib/dipinto.js` yalnız Yunan harfi çiziyor: Latin ve Türkçe harfler (Ç Ğ İ Ö Ş Ü dahil) ortak dosyaya başkan tarafından eklenir (motordan istek).')
L.append('- **Dipinto dili:** konuşma dipintosu her zaman Türkçe (KENDİNİ TANIMAZSA, KİM VAR BURADA?, BANA SAHİP OLURSUN); Latince yalnız künyede (si se non noverit, iste ego sum, inopem me copia fecit), Yunanca yalnız ad etiketlerinde (ΝΑΡΚΙΣΣΟΣ, ΗΧΩ, ΤΕΙΡΕΣΙΑΣ) ve Delfi taşında. Türkçe çift: P012 taşın altındaki KENDİNİ TANI suda ters döner ↔ P061 KENDİNİ TANIMAZSA → TANIDI.')
L.append('- **Yansıma gecikmesi (tek kural):** D03\'ten (P038) E04 \'benim\'e (P053) kadar yansıma gerçeği 9 kare (0,3 sn) geç izler; hafif ama her kıpırtıda var, görünür olduğu yerler P047 (konuşan şair, orta), P050 (iki el aynı karede), P051. A bölümündeki havuz planları da aynı kurala uyar (tanınmadan önce). \'Benim\'de gecikme sıfırlanır ve yansıma kilitlenir: tanıma anının tek görsel olayı. Kilitten sonra yansıma birebirdir.')
L.append('- **Gözyaşı halkası:** damla + halka + yüzün dağılması filmde yalnız P062\'de (E11). Başka yerde damla düşmez; P007\'de esinti, P061\'de yazı halkasız batar. Delfi birikintisindeki halka (P012) ve kolların suya dalması (P042) ayrı imge olarak kalır.')
L.append('- **Hatıra dili:** hatıra planları (P057 Eko\'nun reddi, P060 Tiresias) beyaz zemin lekythos paletiyle (solgun sepya çizgi) çizilir; sessizde de \'geçmiş\' okunur. P057\'ye giriş eşleme kesmesiyle (SAHİP kelimesi yerinde kalır).')
L.append('- **Beden sürekliliği:** P065\'te (E13 \'o da aşkla\') beden yalnız incelir: renk solar, kenar yumuşar, çevresinde ışık noktaları. P067, P068, P070 aynı incelmiş bedeni gösterir. Kayboluş P073\'te (ot yatağında son ışık noktaları söner), nergis P074\'te o yerde açar.')
L.append('- **Yazı yoğun:** levha ya da alıntı/soru/yazı katmanı olan ya da iki ve daha çok yazı kalemi (dipinto dahil) taşıyan plan; tabloda (yy). Altyazı açık izleyicide (≈%38) üç katman olur. Art arda iki yazı yoğun plan doğrulayıcıda uyarı verir (aşağıda). Bölüm kartı sayılmaz: plan başında 2–3 sn tek başına durur.')
L.append('- **Hassasiyet (bütün planlar):** secde, dört ayak üstü eğilme, diz çökme yok; hale, haç, altı köşeli yıldız yok; çıplaklık yok (khiton uyluk ortasında); Eko baştan ayağa örtülü değil (yüzünü yaprakla örter); ruh sağlığıyla alay yok; telefon bölümünde ahlak dersi yok; Juno ve öç tanrıçası figürle çizilmez (ışık/simge).')
L.append('- **Belirlenimcilik:** `Math.random`/`Date.now` yok; tohum kare numarasından (`rng(seed)`, `hash`, `noise`).')
L.append('\n## Setler\n')
L.append('| Set | Ne | Planlar |')
L.append('|---|---|---|')
for k, v in SETLER.items():
    ps = [p for p in planlar if planlar[p]['set'] == k]
    L.append(f'| {k} | {esc(v)} | {len(ps)}: {", ".join(ps)} |')
L.append('\n## Plan tablosu\n')
cur = None
for pid, t in rows:
    p = planlar[pid]
    if p['bolum'] != cur:
        cur = p['bolum']; L.append(f'\n### {cur} ({p["sahip"]})\n')
        L.append('| Plan | Çapa | Başlangıç | Süre | Ölçek | Set | Ekranda ne olur | Sözcüğe bağlı eylemler | Geçiş | Ekran yazısı / künye | Kamera | Hassasiyet |')
        L.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
    ey = '<br>'.join(f'`{e["at"]}` {esc(e["ne"])}' for e in p['eylem'])
    L.append(f'| **{pid}**{" (levha)" if p["levha"] else ""}{" (yy)" if p["yazi_yogun"] and not p["levha"] else ""} | `{p["at"]}` | {mmss(t)} | {vf(sure[pid][1])} | {p["olcek"]} | {p["set"]} | {esc(p["ne"])} | {ey} | {trs(p["tr"])} | {esc(p["yazi"]) or "—"} | {esc(p["kamera"])} | {esc(p["hassasiyet"]) or "—"} |')
L.append('\n## Yenilik boşlukları (kesme ya da sözcüğe bağlı eylem olmadan > 5 sn)\n')
if bosluk:
    for a, b, d, pid in bosluk: L.append(f'- {mmss(a)}–{mmss(b)} ({vf(d)} sn), {pid}' + (' (bitiş ekranı: kesmesiz, vazo frizi yavaş döner; bilinçli)' if a >= BITIS - 1 else ''))
else: L.append('- yok')
if UYARI:
    L.append('\n## Önek uyarıları (denetlendi)\n')
    for u in UYARI: L.append(f'- {u}')
L.append('\n## Art arda yazı yoğun planlar (uyarı) ve karar\n')
YY_NOT = {
 'F02@aşırı>F03': "kabul: F03'ün ilk ≈4 sn'si yalnız sepya figür ve okunmaz kenar notu; Ellis kırpması 'İngiliz'de, planın ortasında gelir",
 'F03>F03@bir#2': "kabul: Ad bölümünün konusu kelimenin kendisi; iki planda da aynı sepya figür kadrajda (ders değil, bir adın başına gelenler)",
 'F03@bir#2>F04': "kabul: araya fade (zaman sıçraması); F04'ün yazıları tek kelime (narsist), okunacak cümle yok",
 'F07>F08@ama': "kabul (Fable 5.2'nin isteği): Freud'un iki cümlesi pınar benzetmesinin üstünde kesintisiz okunur; üçüncü cümle ekrandan kaldırıldı (P089 yalnız künye)",
}
for x, y in yy_ard:
    k = planlar[x]['at'] + '>' + planlar[y]['at']
    L.append(f'- {x} → {y} (`{planlar[x]["at"]}` → `{planlar[y]["at"]}`): ' + YY_NOT.get(k, 'GEREKÇESİZ: başkana'))
if yakin_ard: L.append('- yakın ↔ orta-yakın aynı sette (fiilen aynı boy): ' + ', '.join(f'{a}–{b}' for a, b in yakin_ard))
else: L.append('- yakın ↔ orta-yakın komşuluğu aynı sette: yok')
# hizalama önerisi: vo/oneri/timeline_oneri.js varsa değişen cümleler
ON = os.path.join(ROOT, 'vo', 'oneri', 'timeline_oneri.js')
if os.path.exists(ON):
    C2 = json.loads(re.search(r'window\.CUES = (\{.*?\});', open(ON, encoding='utf-8').read(), re.S).group(1))
    L.append('\n## Hizalama önerisi (engelleyici; başkan uygular)\n')
    L.append('`tools/hizala_cumle.py` ile cümle düzeyinde yeniden ölçüldü; aşağıdaki cümlelerin sınırı ≥ 0,25 sn değişiyor. Plan çapaları kelimeye bağlı olduğu için kendiliğinden kayar; doğrulayıcı yeni zaman çizelgesiyle de hatasız.\n')
    L.append('| Cümle | Şimdi (timeline.js) | Öneri | Süre şimdi → öneri |')
    L.append('|---|---|---|---|')
    for k in CUES:
        a_, b_ = CUES[k], C2[k]
        if abs(a_['s'] - b_['s']) > .25 or abs(a_['e'] - b_['e']) > .25:
            L.append(f"| {k} | {mmss(a_['s'])}–{mmss(a_['e'])} | {mmss(b_['s'])}–{mmss(b_['e'])} | {vf(a_['e'] - a_['s'])} → {vf(b_['e'] - b_['s'])} sn |")
L.append('\n## Fable 5.2 denetimi (puan 7,5): yapılanlar\n')
L.append('Numara değişikliği: Fable 5.2\'deki P080 (Ellis levhası), P085 (soru levhası) ve P088 (Freud kartı) kalktı; F01@peki ve F04@bu iki yeni plan. P001–P075 aynı numarada; sonrası: eski P076–P079 → P077–P080, eski P081–P083 → aynı, eski P084 → P085, eski P086–P087 → aynı, eski P089–P099 → P088–P098.\n')
for x in [
 "**P065 süreklilik (engelleyici):** çapa `E13@o` ('o da aşkla'); beden yalnız incelir (renk solar, kenar yumuşar, ışık noktaları), kaybolmaz. P067, P068, P070 aynı incelmiş bedeni gösterir; kayboluş P073'te, nergis P074'te o yerde. Genel kural 'Beden sürekliliği'.",
 "**F11 zamanları (engelleyici):** yukarıda 'Engelleyici: hizalama' ve 'Hizalama önerisi'. Yalnız F10–F12 değil, s02, s04, s05, s06, s07, s08 çekimlerinde 27 cümlenin sınırı kaymıştı; F11 öneride 9,6 sn. P095'in (F11) dört eylemi ve cam dönüşümü yeni zamanlarla da plan içinde.",
 "**P083 bölündü:** `F04@ama` (P083, orta): 'narsist' yazıları kimseye yapışmadan suya düşer ve iz bırakmadan söner (çekinceyi görüntü söyler). `F04@bu#1` (P084, ayrıntı): kıyıdaki nergis, su durulur.",
 "**F02–F05 (ders riski):** sepya Narkissos bütün belge planlarının köşesinde; her belgede ona bir şey olur (1606 suya eğilir, 1646 ahlak satırı gövdesinin üstüne biner, 1898 kenar notu ve Ellis kırpması yanında, 1899 ad etiketi değişir, 1914 yanında soru). Ellis levhası F03'e bindirildi, soru levhası Freud planının sonuna eylem oldu. Kalan karakter yokluğu: F04 (yankı, bilinçli: kişi yok) ve F04@ama/@bu (çekince, ≈9 sn; 'narsist' yazılarının sönmesi ve nergis olay taşıyor).",
 "**P088–P090 (yeni P087–P089):** Freud kartı kalktı; ilk cümle P087'nin yükselen suyunda. P088 geniş (akıntı ormana), P089 yakın; ölçek dizisi orta (çocuk) → orta-yakın → geniş → yakın. Üçüncü cümle ekrandan kaldırıldı (altyazıda; görüntü söylüyor).",
 "**Gözyaşı halkası:** P007'de esinti (damla ve halka yok); P061'de yazı halkasız batıp söner. Damla + halka + yüz yalnız P062'de.",
 "**P062 → P063:** P063 ters açı (suyun içinden yukarı, elin altından). **P050** orta: kol, kıyı ve iki el aynı karede.",
 "**Yansıma gecikmesi:** tek kural (genel kurallarda): D03'ten 9 kare, 'benim'de kilit. P038, P047, P049–P051, P053 buna göre yazıldı; P004'te kilitlenme yok.",
 "**P053:** 'benim'de ekranda yalnız “O benim.” (büyük kırmızı); öbür iki cümle altyazıda, künye küçük. E04 ile E05 arasındaki ≈1,8 sn sessizlikte yeni eylem yok, kilitli yansıma durur. **P004:** parmak ve su teması yok, yansıma soluk ve gecikmeli, yazı küçük sepya.",
 "**P055–P060:** P055 ve P059'da alıntı yazısı yok (yalnız küçük künye). Yazı P056 'SAHİP' → P058 'SAHİP / copia' ödemesinde. P057 ve P060 beyaz zemin hatıra paleti; P057'ye fade yerine eşleme kesmesi (SAHİP kelimesi yerinde kalır).",
 "**Dipinto dili:** konuşma dipintosu Türkçe (P010 KENDİNİ TANIMAZSA; Latince yalnız künyede). P012'de taşın altındaki Türkçe KENDİNİ TANI suda ters döner; P061'de KENDİNİ TANIMAZSA → TANIDI.",
 "**P001:** cam → havuz dönüşümü 'baktın'dan sonraki sessizlikte (≈3,1–4,5 sn), kısa; P002 'iki'de (≈4,5 sn) antik yüz ve soluk yansıma: kapak A'nın vaadi ilk 5 sn'de. 3,0 sn karesi sessiz okuma testine.",
 "**D bölümü:** P041 tam tepeden (su çizgisi dikey, iki yüz yan yana), P047 şairin omzundan orta plan, P055 sırttan (parıltı yüzün kenarında). Kamera varsayılanı çeşitlendi: 'çok yavaş yaklaşma' ≈35 plandan 12'ye; yerine uzaklaşma, dikey kayma, paralaks, omuz arkası, sudan yükselme.",
 "**B bölümü:** P011'in fade'i kalktı (P010'un dipinto çizgisinden taş yazıta eşleme kesmesi); P011 kısa (≈3–4 sn), ağırlık P012'de (`B03@kendini`'den). B'de iki fade kaldı (P008 bölüm başı, P013 zaman sıçraması).",
 "**P086 (F06):** yeni set DERE (P008'in nehri değil); çocuk 7–8 yaş oranı, kısa düz saç, kemerli tunik, elinde çember (trokhos); arkadaşları baştan patikada. 'hastalık'ta kalkar, 'olağan'da kadrajdan çıkmış. Patika P005/P054'ün biçiminde.",
 "**Levha sayımı:** fiilen yazı planları levha sayıldı (P010, P028, P058, P061, P082; P011 ve P075 değişiklikten sonra yazı planı değil); 'yazı yoğun' (yy) etiketi ve art arda yy uyarısı üreticide.",
 "**P097–P098 (eski P098–P099):** Sisifos silueti 'hikâyesi'nde, 'ekranda'dan önce bitiş ekranındaki yerine oturur; P098'de kırmızı nokta 'ekranda'da video kutusunun altına koşar ve orada durur. P096 (nergis) kısa kalır.",
]: L.append('- ' + x)
L.append('\n## Sessiz okuma testi adayları (animatik)\n')
L.append('- P001 3,0 sn karesi (soru sormadan); P049–P053 (gecikme ve kilit görünüyor mu, parmak buluşması Âdem\'in Yaratılışı okunuyor mu); P065 (beden kayboldu mu sanılıyor?); P083–P084; P086 (çocuk Narkissos sanılıyor mu?); P093 (F10 tepeden halka).')
L.append('\n## Reddedilenler\n')
L.append('- **Yok (bütün maddeler uygulandı).** Kısmen uygulananlar ve gerekçeleri:')
L.append('  - *F11 hizalaması `timeline.js`e uygulanmadı:* görev kuralı (seslendirme kesin, DEĞİŞTİRME). Hizalama önerisi ve aracı hazır; uygulamak başkanın kararı (yukarıdaki tek satır). Plan listesi iki zaman çizelgesinde de geçerli.')
L.append('  - *Ad bölümündeki art arda yazı yoğun zincir (P079–P082) tamamen kırılmadı:* bölümün konusu kelimenin kendisi; zincirin her halkasında aynı sepya figür kadrajda ve her biri ona bir şey yapıyor (Fable\'ın önerdiği çözüm). Daha fazla kırmak için ad değişimini (P081) F03\'e eylem olarak bindirmek gerekir, bu da ≈15 sn\'lik tek plan yapar; donukluk riski yazı yükünden büyük.')
L.append('  - *P060\'ın fade\'i kaldı:* havuzdan Tiresias\'a hem mekân hem zaman sıçraması; Fable eşleme kesmesini yalnız P057 için istedi. Hatıra beyaz zemin paletiyle ayrıca belli.')
open(os.path.join(kok, 'planlar.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

print(len(planlar), 'plan; ort', round(ortalama, 2), 'sn;', dict(Counter(p['set'] for p in planlar.values())))
print('ölçek:', dict(olc))
print('levha:', lev, 'toplam', round(lev_top, 1), f'%{100 * lev_top / DUR:.1f}')
ids = {s['id'] for s in json.load(open(os.path.join(kok, 'senaryo.json'), encoding='utf-8'))['segments']}
kapsanan = {rows[k][0] for k in range(len(rows))}
cumle_plan = {}
for pid, t in rows: pass
print('boşluklar:', bosluk)
_g=sorted(((round(b-a,2),round(a,2)) for a,b in zip([0.0]+isaret,isaret)),reverse=True)[:8]; print('en uzun aralıklar:', _g)
print('uyarı:', UYARI)
print('HATA:', hata if hata else 'yok')
