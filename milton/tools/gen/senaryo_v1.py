"""Milton senaryosu, revizyon 1 → senaryo.json
Yazım: metin bir kez yazılır; `alt` (altyazı) ve `tts` (seslendirme) buradan türetilir.
  {görünen|okunan}  : altyazıda soldaki, seslendirmede sağdaki (sayılar, okunuş)
  [etiket]          : yalnız seslendirmede (ElevenLabs v4 ses etiketi)
  OKUNUS sözlüğü    : özel adların seslendirme okunuşu
Kaynak kısaltmaları: KC = Kayıp Cennet (1674, 12 kitap), kitap.dize; çeviriler bizim.
DNB = Dictionary of National Biography (1894), 'Milton, John', s. 34–37."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

OKUNUS = [
    ('John Milton', 'Con Milton'), ('William Blake', 'Vilyım Bleyk'), ('Blake', 'Bleyk'),
    ('C. S. Lewis', 'Si Es Luis'), ('Lewis', 'Luis'), ('Shelley', 'Şeli'), ('Narnia', 'Narniya'),
    ('Lucifer', 'Lusifer'), ('Beelzebub', 'Belzebub'), ('Pandemonium', 'Pandemonyum'),
    ('Abdiel', 'Abdiyel'), ('Uriel', 'Uriyel'), ('Cromwell', 'Kromvel'),
    ('Gustave Doré', 'Güstav Dore'), ('Doré', 'Dore'), ('Alexandre Cabanel', 'Aleksandr Kabanel'),
    ('Cabanel', 'Kabanel'), ('Villa Medici', 'Villa Mediçi'), ('Charles', 'Çarls'),
    ('Prometheus', 'Prometeus'),
]

S = []
def s(id_, bolum, metin, kaynak=''):
    S.append((id_, bolum, metin, kaynak))

# ───────────────────────── A. Kanca ─────────────────────────
b = 'Alev gölü'
s('A01', b, "[slowly] [deep voice] “Hangi yana kaçsam cehennem… cehennem benim.” [pause] Bunu söyleyen, bir zamanlar cennetin en parlak meleğiydi.",
  "KC IV.75; parlaklık: I.84–87, VII.131–133")
s('A02', b, "[darkly] Şimdi yanan bir gölün ortasında gözlerini açıyor. Dokuz gün boyunca düşmüştü. Etrafında alev var ama ışık yok; Milton'ın deyişiyle, görünür bir karanlık.",
  "KC I.56–58 (gözler), VI.871 (dokuz gün düştüler), I.62–63 (darkness visible)")
s('A03', b, "Elmas zincirlerle bu göle bağlı. Birazdan zincirlerinden kurtulacak, cehennemin kapısından çıkıp Kaos'u aşacak. Ama nereye giderse gitsin, cehennem de onunla gelecek.",
  "KC I.48, I.209–213 (zincir ve göl), II.871–1055 (kapı, Kaos), IV.18–23 (cehennemi içinde taşır)")
s('A04', b, "[curious] Peki zincirleri çözülen birini, cehennemde tutan neydi?",
  "merak sorusu; cevabı G09, L09")
s('A05', b, "[thoughtfully] Bu hikâye bir kutsal kitaptan değil, bir şiirden: John Milton'ın {1667|bin altı yüz altmış yedi}'de yayımlanan destanı, Kayıp Cennet'ten. Buradaki Şeytan, bir şairin yarattığı bir karakter.",
  "ilk baskı Ağustos 1667 (10 kitap), ikinci baskı 1674 (12 kitap); kullanıcı kararı: yalnız edebi okuma")
s('A06', b, "[softly] Ve onu yaratan şair, bu dizeleri söylerken hiçbir şey göremiyordu.",
  "körlük: 1652'den itibaren tam kör (Leonard 2000; DNB)")

# ───────────────────────── B. Şair ─────────────────────────
b = 'Karanlıkta yazdıran şair'
s('B01', b, "[thoughtfully] Londra, on yedinci yüzyıl. John Milton, kırk üç yaşına geldiğinde gözleri tamamen kararmıştı.",
  "Milton d. 9 Aralık 1608; 1652'de tam kör (43 yaşında)")
s('B02', b, "Ama Milton yalnızca bir şair değildi. Kral Birinci Charles'ın yargılanıp idam edilmesini savunmuş, kralı deviren devrimin hükümetinde çalışmıştı.",
  "The Tenure of Kings and Magistrates (1649), Eikonoklastes (1649); Yabancı Diller Sekreteri 1649–1660")
s('B03', b, "[darkly] Sonra devrim çöktü. {1660|Bin altı yüz altmış}'ta krallık geri döndü. Milton saklandı; kitapları cellat eliyle yakıldı; kendisi yakalanıp hapse atıldı.",
  "Restorasyon Mayıs 1660; Avam Kamarası 16 Haziran 1660 kararı, yakma Ağustos 1660; kısa süreli hapis, Aralık 1660'ta salıverildi (DNB s. 33–34)")
s('B04', b, "Dostlarının araya girmesiyle kurtuldu. Ama artık kör, yoksul ve yenilmiş bir adamdı.",
  "Marvell vb. (Wikipedia 'John Milton', DNB s. 34); maddi kayıplar DNB s. 34")
s('B05', b, "[softly] Ve tam o yıllarda, bir destanı yazdırmaya koyuldu.",
  "yazım 1658–1663/64 (Aubrey; DNB s. 34)")
s('B06', b, "Dizeleri çoğu zaman geceleri, uykusuzken kafasında kuruyordu. Bazen kızlarından birini uyandırıp yazdırır, kırk dizeyi bir solukta söyleyip sonra yirmiye indirirdi.",
  "DNB s. 37 (uykusuz gecelerde kızına yazdırır; 40 dize → 20)")
s('B07', b, "Sabahları da evde kim varsa ona yazdırırdı: yeğenine, dostlarına, tuttuğu yardımcılara.",
  "DNB s. 37 (10–30 dizeyi evde bulunan herkese); yeğen Edward Phillips; 'a series of aides in his employ'")
s('B08', b, "[sadly] İki küçük kızına, anlamını bilmedikleri dillerde okumayı öğretmişti: İbranice, Yunanca, Latince. Kızlar, anlamadıkları sözcükleri göremeyen babalarına okurdu.",
  "DNB s. 36 (Phillips: iki küçük kız, İbranice, belki Süryanice, Yunanca, Latince, anlamını bilmeden)")
s('B09', b, "Babalarıyla araları iyi değildi; bu okuma saatleri, yıllar içinde onlar için dayanılmaz bir hâl almıştı.",
  "DNB s. 36 (Phillips: 'almost beyond endurance'; ilişkiler 'unfortunate')")
s('B10', b, "[thoughtfully] Destanın üçüncü kitabında Milton kendi körlüğünü anlatır: “Mevsimler döner; ama bana gün dönmez. Ne sabah ne akşam, ne bahar çiçeği ne yaz gülü… ne de bir insan yüzü.”",
  "KC III.40–44 (çevirimiz, kısaltılmış)")
s('B11', b, "[softly] “Öyleyse sen, göksel ışık, içime parla. Orada gözler aç ki, ölümlü gözün göremediğini göreyim ve anlatayım.”",
  "KC III.51–55 (çevirimiz)")
s('B12', b, "Işığını kaybetmiş bir şair, ışığını kaybetmiş bir meleği anlatacaktı.",
  "anlatıcının köprüsü")
s('B13', b, "[mysterious] Yeğeninin anlattığına göre, Milton bu hikâyenin ilk dizelerini yıllar önce yazmıştı. Ve o dizeler bir zafer şarkısı değildi: Şeytan'ın, güneşe yaptığı bir itiraftı. Oraya geleceğiz.",
  "DNB s. 34: Phillips, tasarlanan tragedyanın açılışının (~1642) şimdi IV. kitabın başındaki Şeytan konuşması olduğunu bildirir (KC IV.32 vd.); ödemesi G03, G15")
s('B14', b, "Ama önce, o meleğin düşmeden önceki hâline bakalım.", "")

# ───────────────────────── C. Cennet ─────────────────────────
b = 'Işık taşıyan'
s('C01', b, "[curious] Her şeye sahip olan biri, neden başkaldırır?", "bölüm sorusu; cevabı C06")
s('C02', b, "[warmly] Milton'ın cenneti, ışıktan bir dünyadır. Ve o dünyanın en parlak varlıklarından biri, başmeleklerin ilki; ilki değilse bile, en büyüklerinden biridir.",
  "KC V.659–661 ('of the first, if not the first Arch-Angel')")
s('C03', b, "Milton ona bir yerde Lucifer der: ışık taşıyan. Yüzü, yıldızların arasındaki sabah yıldızı gibi parlıyormuş.",
  "KC VII.131–133 (Lucifer); V.708–709 (sabah yıldızı gibi yüzü); Lucifer: Lat. 'ışık taşıyan'")
s('C04', b, "Asıl adını ise hiç söylemez. “Eski adı artık cennette anılmıyor,” der. “Ona bundan böyle Şeytan deyin.”",
  "KC V.658–659 (çevirimiz)")
s('C05', b, "[slowly] Bir gün, Milton'ın anlattığına göre, Tanrı bütün melekleri toplar ve Oğul'u onların başına geçirir. Bundan sonra herkes onun önünde diz çökecek; ona karşı gelen, Tanrı'ya karşı gelmiş sayılacaktır.",
  "KC V.600–615; Tanrı ve Oğul figürle değil ışıkla gösterilir (kullanıcı kararı)")
s('C06', b, "Başmelek bu manzaraya dayanamaz. Milton sebebini iki kelimeyle söyler: kıskançlık ve gurur. Kendini küçültülmüş sayar.",
  "KC V.662–665 ('fraught with envy… through pride… thought himself impaired')")
s('C07', b, "[darkly] Gece yarısı, emrindeki melekleri uyandırır ve onları kuzeye, kendi sarayına götürür.",
  "KC V.667–689")
s('C08', b, "Ve orada, isyanların en eski kelimesiyle konuşur: özgürlük.", "KC V.787–802 (giriş)")
s('C09', b, "[firmly] “Boynunuzu eğip dizinizi mi bükeceksiniz? Biz cennetin yerlisiyiz. Hepimiz eşit değilsek de, hepimiz özgürüz. Yasasız da yanılmayanlara kim yasa koyabilir?”",
  "KC V.787–799 (çevirimiz, kısaltılmış)")
s('C10', b, "Cennetin ordularının üçte biri, onun peşinden gider.", "KC V.709–710")
s('C11', b, "[softly] Ama bir melek ayağa kalkar. Adı Abdiel'dir.", "KC V.803–808")
s('C12', b, "Abdiel ona karşı çıkar; sonra binlerce küçümseyen bakışın arasından, tek başına yürüyüp gider. Milton onu şöyle anlatır: sadakatsizlerin arasında sadık kalan tek kişi.",
  "KC V.896–907 ('faithful found among the faithless, faithful only he… though single')")
s('C13', b, "[thoughtfully] Peki burada asıl başkaldıran kim: kalabalığı peşine takan mı, kalabalığa karşı tek başına duran mı? Bu soruyu aklında tut.",
  "kurulum; ödemesi K12")

# ───────────────────────── D. Savaş ve düşüş ─────────────────────────
b = 'Dokuz gün'
s('D01', b, "[curious] Ölümsüz bir varlık, acıyı ilk kez nasıl tanır?", "bölüm sorusu; cevabı D04")
s('D02', b, "Cennette savaş başlar. İlk darbeyi Abdiel vurur. Kılıcı Şeytan'ın miğferine iner; Şeytan on adım geriler ve onuncu adımda dizinin üstüne çöker.",
  "KC VI.189–195")
s('D03', b, "Abdiel darbeden önce ona şunu söylemişti: “Asıl kölelik, akılsıza hizmet etmektir. Seninkiler şimdi sana hizmet ediyor. Ama sen özgür değilsin; kendi kendinin tutsağısın.”",
  "KC VI.178–181 (çevirimiz, kısaltılmış)")
s('D04', b, "[darkly] Savaşın ortasında bir başmeleğin kılıcı, Şeytan'ın sağ yanını yarar. Ve Milton yazar: Şeytan acıyı ilk kez o an tanıdı.",
  "KC VI.320–327 ('Then Satan first knew pain')")
s('D05', b, "Yarası çabucak kapanır. Ama bir zamanlar parlayan zırhı artık lekelidir.", "KC VI.330–334")
s('D06', b, "Asiler barutu ve topu icat eder. Sadık melekler de dağları kökünden söküp üzerlerine atar.",
  "KC VI.482–520, VI.584–594 (barut, top); VI.639–666 (dağlar)")
s('D07', b, "[awed] Üçüncü gün, Oğul ışıktan bir arabayla gelir. Asiler cennetin kıyısına kadar sürülür ve kendilerini boşluğa atarlar.",
  "KC VI.699, VI.748–866")
s('D08', b, "[slowly] Dokuz gün düştüler. Kaos kükredi. Sonunda cehennem ağzını açıp onları yuttu ve üzerlerine kapandı.",
  "KC VI.871–875")
s('D09', b, "Ve hikâye, en başta gördüğümüz yere döner: yanan göle.", "")

# ───────────────────────── E. Cehennem ─────────────────────────
b = 'Cehennemde kral'
s('E01', b, "[curious] Her şeyini kaybeden biri, ilk olarak ne söyler?", "bölüm sorusu")
s('E02', b, "Şeytan yanında yatan yardımcısı Beelzebub'u görür. İlk sözleri bir şaşkınlıktır: “Sen o musun? Ah, ne kadar düşmüş, ne kadar değişmişsin! Bir zamanlar ışık diyarında, binlerce parlak varlığı gölgede bırakırdın.”",
  "KC I.79–87 (çevirimiz, kısaltılmış)")
s('E03', b, "[firmly] Ama hemen toparlanır: “Savaş alanını kaybettik; ne olmuş? Her şey kaybedilmedi. Yenilmez irade, intikam, ölümsüz nefret ve asla boyun eğmeyen cesaret, hâlâ bizde.”",
  "KC I.105–109 (çevirimiz, kısaltılmış)")
s('E04', b, "Milton bu sözlerin hemen ardından küçük bir not düşer: Şeytan, acı içinde böbürleniyordu; içi derin bir umutsuzlukla kıvranırken.",
  "KC I.125–126")
s('E05', b, "Gölden kalkar. Kalkanı omzunda, ay gibi asılıdır. Bir geminin direği kadar uzun mızrağına yaslanarak, yanan topraklarda yürür.",
  "KC I.283–296")
s('E06', b, "Yüzünde yıldırımların açtığı derin izler var. Ama hâlâ, yıkılmış bir başmelek kadar görkemli.",
  "KC I.591–601")
s('E07', b, "[softly] Yenik ordusunun karşısına geçip konuşmaya başladığında, sesi düğümlenir. Üç kez dener; üç kez, kendi küçümsemesine rağmen, gözlerinden yaşlar boşanır. Milton'ın deyişiyle: meleklerin ağladığı gibi.",
  "KC I.604–621 ('Tears, such as Angels weep'); kurulum, ödemesi L05")
s('E08', b, "[thoughtfully] Sonra cehennemi selamlar: “Elveda mutlu topraklar; merhaba dehşet. Zihin kendi yeridir. Kendi içinde cehennemi cennet, cenneti cehennem yapabilir.”",
  "KC I.249–255 (çevirimiz, kısaltılmış)")
s('E09', b, "[slowly] [firmly] Ve destanın en ünlü dizesini söyler: “Cehennemde hüküm sürmek, cennette hizmet etmekten iyidir.”",
  "KC I.263 (çevirimiz)")
s('E10', b, "[pause] Yani: cennette köle olacağıma, cehennemde kral olurum.", "I.263'ün anlatıcı açımlaması")
s('E11', b, "Şeytanlar cehennemin toprağından altın kazar. Bir saatten kısa sürede, yerden devasa bir saray yükselir: Pandemonium, bütün şeytanların meclisi.",
  "KC I.670–730, I.697 ('in an hour'), I.756 (Pandæmonium)")
s('E12', b, "Mecliste kimi yeni bir savaş ister, kimi sessizce katlanmayı, kimi cehennemde kendi krallıklarını kurmayı. Sonunda Şeytan'ın planı kabul edilir: Tanrı'nın yeni yarattığı dünyaya, insana saldırmak.",
  "KC II.51–378 (Moloch, Belial, Mammon, Beelzebub; plan Şeytan'ındır: II.379–380)")
s('E13', b, "[darkly] Kimsenin gitmeye cesaret edemediği bu yolculuğa, yalnızca o gönüllü olur.",
  "KC II.417–466")
s('E14', b, "[slowly] Ayağa kalktığında bütün cehennem önünde eğilir; onu Tanrı'ya denk sayıp yüceltirler. Diz çökmeyi reddeden melek, şimdi önünde diz çökülen bir kraldır.",
  "KC II.476–479; taht: II.1–6")

# ───────────────────────── F. Kapı ve Kaos ─────────────────────────
b = 'Kapıdaki kız'
s('F01', b, "[curious] Kendi aklından doğmuş bir şeyle yüz yüze gelsen, onu tanır mıydın?", "bölüm sorusu; cevabı F04")
s('F02', b, "Cehennemin dokuz katlı kapısında iki bekçi vardır: yarısı kadın, yarısı yılan bir varlık… ve biçimi olmayan bir gölge.",
  "KC II.645–673")
s('F03', b, "Şeytan gölgeyle dövüşmeye hazırlanırken kadın araya girer: “Beni unuttun mu? Cennette sen isyanı tasarlarken, başından ben doğmuştum. Bana Günah dediler.”",
  "KC II.746–760 (çevirimiz, kısaltılmış)")
s('F04', b, "[darkly] Şeytan onu tanımaz. Kendi aklından doğan şeyi tanımaz. Ve o gölgenin, Günah'tan doğan Ölüm olduğunu öğrenir.",
  "KC II.737–745, II.781–789")
s('F05', b, "Kapı açılır. Önünde ne başı ne sonu olan karanlık bir okyanus vardır: Kaos.", "KC II.871–916")
s('F06', b, "Kanatlarını açıp uçar; sonra boşluğa düşer, binlerce kulaç aşağı. Bir rüzgâr onu yeniden yukarı fırlatmasa, hâlâ düşüyor olurdu.",
  "KC II.927–938")
s('F07', b, "Sonunda uzakta bir şey görür: cennete altın bir zincirle asılı, ayın yanındaki en küçük yıldız kadar bir dünya.",
  "KC II.1051–1053")
s('F08', b, "Güneşe varır. Genç bir melek kılığına girip güneşin bekçisi Uriel'e yolu sorar. Milton'a göre ne insan ne melek, ikiyüzlülüğü göremez.",
  "KC III.634–684")
s('F09', b, "Uriel yolu gösterir. Şeytan aşağı süzülür ve bir dağın, Nifates'in tepesine konar.",
  "KC III.724–742")

# ───────────────────────── G. Nifates ─────────────────────────
b = 'Güneşe itiraf'
s('G01', b, "[curious] Kimse duymadığını sanırken, Şeytan kendine ne söyler?", "bölüm sorusu")
s('G02', b, "Cehennemden kaçmıştır. Ama Milton uyarır: cehennemi yanında getirmişti. Kendinden kaçamadığı gibi, cehennemden de bir adım uzaklaşamazdı.",
  "KC IV.18–23")
s('G03', b, "[slowly] Güneşe bakar ve konuşmaya başlar: “Ey ihtişamla taçlanmış güneş… sana dostça seslenmiyorum. Işınlarından nefret ettiğimi söylemek için adını anıyorum; çünkü bana hangi yücelikten düştüğümü hatırlatıyorlar.”",
  "KC IV.32–39 (çevirimiz, kısaltılmış); Phillips'e göre ilk yazılan dizeler (DNB s. 34)")
s('G04', b, "[softly] Sonra, hiç beklemediğimiz bir şey söyler: “O, benden bu karşılığı hak etmemişti. Beni yaratmıştı; iyiliğini başa kakmazdı. Hizmeti de ağır değildi.”",
  "KC IV.42–45 (çevirimiz)")
s('G05', b, "“Keşke beni sıradan bir melek yaratsaydı. O zaman mutlu kalırdım.”", "KC IV.58–61 (çevirimiz, kısaltılmış)")
s('G06', b, "[thoughtfully] Ve kendine bir soru sorar: “Senin de onlar gibi özgür iraden var mıydı? Vardı. O hâlde kimi suçlayacaksın?”",
  "KC IV.63–68 (çevirimiz, kısaltılmış)")
s('G07', b, "[sadly] [slowly] “Vay zavallı bana! Sonsuz öfkeden, sonsuz umutsuzluktan nereye kaçayım? Hangi yana kaçsam cehennem. Cehennem benim.”",
  "KC IV.73–75 (çevirimiz)")
s('G08', b, "“En derin dipte, beni yutmak için ağzını açan daha derin bir dip var. Onun yanında, çektiğim cehennem cennet gibi kalıyor.”",
  "KC IV.76–78 (çevirimiz)")
s('G09', b, "[softly] Bir an yumuşar: “Pişmanlığa hiç yer kalmadı mı? Bağışlanmaya?” [pause] Cevabı yine kendisi verir: “Bir yol kaldı: boyun eğmek. Ama o kelimeyi, gururum yasaklıyor.”",
  "KC IV.79–82 (çevirimiz); A04 sorusunun cevabı burada saklı, L09'da açılır")
s('G10', b, "Gururu… ve cehennemde bıraktığı ordunun önünde rezil olma korkusu. Onlara boyun eğmeyi değil, Tanrı'yı yenmeyi vaat etmişti.",
  "KC IV.82–86")
s('G11', b, "[bitterly] “Onlar beni cehennemin tahtında yüceltirken, içimde nasıl inlediğimi bilmiyorlar. Tacım ve asam ne kadar yükselirse, ben o kadar aşağı düşüyorum.”",
  "KC IV.86–92 (çevirimiz, kısaltılmış)")
s('G12', b, "[thoughtfully] Ve en dürüst cümlesini kurar: “Diyelim ki pişman oldum ve eski yerime döndüm. Ne kadar sürer? Yükseklik, eski düşüncelerimi geri getirir. Acı içinde verdiğim sözleri, rahata erince geri alırım.”",
  "KC IV.93–97 (çevirimiz, kısaltılmış)")
s('G13', b, "[slowly] Sonunda kararını verir: “Elveda umut. Umutla birlikte elveda korku; elveda pişmanlık. Kötülük… sen benim iyiliğim ol.”",
  "KC IV.108–110 (çevirimiz)")
s('G14', b, "[softly] Bu sözleri söylerken yüzü üç kez değişir: öfkeyle, kıskançlıkla, umutsuzlukla. Kimsenin görmediğini sanır; ama güneşin bekçisi Uriel, hepsini görmüştür.",
  "KC IV.114–130")
s('G15', b, "[thoughtfully] İşte Milton'ın bu hikâye için yazdığı ilk dizeler bunlardı. Şeytan'ı ilk kez alkışlayan bir kalabalık olmadan görüyoruz. [pause] Ve ilk kez, ona acıyoruz.",
  "DNB s. 34 (Phillips); empati anı")

# ───────────────────────── H. Aden ─────────────────────────
b = "Aden'de bir yabancı"
s('H01', b, "[curious] Yok etmeye geldiğin bir şeyi, sevebilir misin?", "bölüm sorusu")
s('H02', b, "Şeytan Aden bahçesine varır. Doğudaki tek kapıyı küçümser; tek sıçrayışta duvarın üstünden atlar.",
  "KC IV.178–183")
s('H03', b, "Bahçenin en yüksek ağacına, hayat ağacına tüner: bir karabatak gibi.", "KC IV.194–196")
s('H04', b, "[softly] Ve ilk kez onları görür: Âdem ile Havva'yı.", "KC IV.288 vd.")
s('H05', b, "[softly] “Düşüncelerim onları hayranlıkla izliyor,” der. “Onları sevebilirdim. Kimsesiz hâllerine acıyabilirim; bana acıyan olmasa da.”",
  "KC IV.358–375 (çevirimiz, kısaltılmış)")
s('H06', b, "“Masumiyetiniz karşısında eriyorum,” der. Ama hemen ekler: krallığının çıkarı, onur ve intikam, onu bunu yapmaya zorlamaktadır.",
  "KC IV.388–392")
s('H07', b, "[firmly] Milton burada araya girer: “Böyle konuştu iblis; ve zorunluluğu, o zorbaların bahanesini, şeytanca işlerine kılıf yaptı.”",
  "KC IV.393–394 (çevirimiz: 'necessity, the tyrant's plea')")
s('H08', b, "Sonra iki insanın birbirine sarılışını izler: “Nefret dolu manzara! İşkence dolu manzara! Bu ikisi birbirinin kollarında cennetteler. Bense ne sevincin ne sevginin olduğu bir cehenneme itilmişim.”",
  "KC IV.505–511 (çevirimiz, kısaltılmış)")
s('H09', b, "[darkly] Gece olunca, Havva'nın kulağının dibine çömelir: bir kurbağa gibi. Ona rüyalar fısıldar.",
  "KC IV.799–809")
s('H10', b, "Bekçi meleklerden biri mızrağının ucuyla ona dokununca, gerçek biçimine döner.", "KC IV.810–819")
s('H11', b, "“Beni tanımıyor musunuz?” diye kükrer. Melekler cevap verir: “Parlaklığının hâlâ aynı olduğunu sanma. İyi olmaktan çıktığın gün, o ışık seni terk etti.”",
  "KC IV.827–840 (çevirimiz, kısaltılmış)")
s('H12', b, "[slowly] Şeytan utanç içinde kalakalır. İyiliğin ne kadar heybetli olduğunu hisseder ve kaybettiğine yanar; en çok da, ışığının gözle görülür biçimde söndüğünü fark edince.",
  "KC IV.846–850")

# ───────────────────────── I. Yılan ─────────────────────────
b = 'Yılanın içinde'
s('I01', b, "[curious] İntikam, insanı rahatlatır mı?", "bölüm sorusu; cevabı I05")
s('I02', b, "Şeytan bahçeden kovulur. Yedi gece boyunca karanlıkla birlikte dünyanın çevresinde döner. Sekizinci gece, gizlice geri sızar.",
  "KC IV.1013–1015; IX.53–69")
s('I03', b, "[sadly] Dünyaya bakar ve yine itiraf eder: “Bir şeyden sevinç duyabilseydim, seni nasıl da dolaşırdım! Ama etrafımda ne kadar güzellik görürsem, içimde o kadar işkence duyuyorum.”",
  "KC IX.114–122 (çevirimiz, kısaltılmış)")
s('I04', b, "Uyuyan bir yılan bulur ve ağzından içine girer. “Ne iğrenç bir iniş!” der. “Bir zamanlar tanrılarla en yüksek yer için yarışan ben, şimdi bir hayvanın içine sıkışıyorum.”",
  "KC IX.159–167, IX.182–190 (çevirimiz, kısaltılmış)")
s('I05', b, "[thoughtfully] Ve kendi geleceğini söyler: “İntikam önce tatlıdır; ama çok geçmeden acılaşır ve dönüp sahibini vurur.”",
  "KC IX.171–172 (çevirimiz)")
s('I06', b, "[softly] Sabah, Havva'yı bahçede yalnız görür. Ve destanın belki de en tuhaf anı gelir: Şeytan bir süre kendi kötülüğünden ayrı durur. Nefreti, hilesi, kıskançlığı, intikamı… hepsi elinden düşer. Milton'ın deyişiyle, bir süre sersemlemiş gibi iyi kalır.",
  "KC IX.455–466 ('stupidly good': 17. yy'da 'sersemlemiş, donakalmış')")
s('I07', b, "[darkly] Ama içinde hep yanan o cehennem, cennetin ortasında bile, bu sevinci çabucak bitirir.",
  "KC IX.467–470")
s('I08', b, "Yılanın diliyle konuşur, Havva'yı ikna eder. Havva meyveyi koparır ve yer.", "KC IX.532–781")
s('I09', b, "[slowly] Dünya yarasını hisseder; doğa iç çeker. Ve suçlu yılan, sessizce çalılığa sıvışır.",
  "KC IX.782–785")
s('I10', b, "Kazanmıştır. Peki bu zafer, neye benzeyecek?", "")

# ───────────────────────── J. Alkış ─────────────────────────
b = 'Alkış'
s('J01', b, "[curious] Zafer anında, insan ne duymayı bekler?", "bölüm sorusu")
s('J02', b, "Şeytan cehenneme döner. Sıradan bir asker kılığında saraya girer, tahtına çıkar ve birden eski parlaklığıyla belirir. Cehennem çığlıklarla onu karşılar.",
  "KC X.441–457")
s('J03', b, "[firmly] “İnsanı yaratıcısından kopardım,” der. “Hem de bir elmayla! Gülmeye değmez mi?”",
  "KC X.485–488 (çevirimiz, kısaltılmış)")
s('J04', b, "Ve susar. O büyük alkışı bekler.", "KC X.504–506")
s('J05', b, "[darkly] [slowly] Ama her yandan, sayısız dilden yükselen tek bir ses duyar: kasvetli, ortak bir tıslama. Herkesin aşağılaması.",
  "KC X.506–509")
s('J06', b, "Şaşırır; ama şaşırmaya bile vakti kalmaz. Yüzünün sivrildiğini hisseder. Kolları kaburgalarına yapışır, bacakları birbirine dolanır ve yüzüstü yere yığılır: devasa bir yılan.",
  "KC X.509–514")
s('J07', b, "Konuşmak ister; ağzından yalnızca tıslama çıkar. Bütün şeytanlar yılana dönüşmüştür.", "KC X.517–521")
s('J08', b, "[slowly] Günah işlediği biçimde cezalandırılmıştır. Alkışları ıslığa, zaferleri kendi ağızlarından kendi üstlerine yağan bir utanca dönüşür.",
  "KC X.516, X.545–547")
s('J09', b, "Önlerinde meyveyle dolu ağaçlar belirir. Açlıkla saldırırlar; meyveler ağızlarında acı küle döner.",
  "KC X.547–570")
s('J10', b, "[thoughtfully] Ve Şeytan destandan sessizce çekilir. Son iki kitapta bir daha sahneye çıkmaz.",
  "KC XI–XII: Şeytan yalnız anılır, görünmez")

# ───────────────────────── K. İki okuma ─────────────────────────
b = 'İki okuma'
s('K01', b, "[curious] Peki bu hikâyenin kahramanı kim?", "bölüm sorusu")
s('K02', b, "Milton destanın en başında amacını açıkça söyler: Tanrı'nın yollarını insanlara haklı göstermek.",
  "KC I.26 (çevirimiz)")
s('K03', b, "Ama yüz yıldan fazla sonra, şair ve ressam William Blake başka bir şey görür.",
  "Blake, The Marriage of Heaven and Hell (1790–93)")
s('K04', b, "[firmly] Blake'e göre Milton, melekleri ve Tanrı'yı anlatırken zincirliydi; şeytanları ve cehennemi anlatırken özgür. Çünkü gerçek bir şairdi ve farkında olmadan Şeytan'ın tarafındaydı.",
  "Blake, MHH lv. 5–6, 'The Voice of the Devil' notu (çevirimiz)")
s('K05', b, "Romantik şairler de Şeytan'da bir isyan kahramanı gördü. Shelley'ye göre, Kayıp Cennet'teki Şeytan'ın enerjisini ve görkemini hiçbir şey aşamazdı.",
  "Shelley, A Defence of Poetry (1821; yay. 1840) (çevirimiz)")
s('K06', b, "Yirminci yüzyılda ise, Narnia'nın yazarı C. S. Lewis tam tersini savundu.",
  "Lewis, A Preface to Paradise Lost (1942), bölüm 13")
s('K07', b, "[thoughtfully] Lewis'e göre bu, bir kahramanın değil, bir küçülmenin hikâyesiydi: Kahramandan generale, generalden politikacıya, oradan casusa, yatak odası penceresinden içeri bakan bir şeye, sonra bir kurbağaya… ve en sonunda bir yılana.",
  "Lewis 1942, bölüm 13 (kısa alıntı, çevirimiz; telifli eser: yalnız kısa alıntı)")
s('K08', b, "Gerçekten de destan boyunca Şeytan'ın ışığı söner, biçimi bozulur: başmelekten karabataka, kurbağaya, yılana.",
  "KC I.591–601, IV.196, IV.800, IX.182–190, X.511–514")
s('K09', b, "[thoughtfully] Peki ya Milton? Kralların devrilebileceğini savunan bir devrimci, Tanrı'nın tahtına başkaldıran bir meleği yazıyor. Ama o melek cehennemde ne yapıyor? Kendi tahtını kuruyor.",
  "Tenure of Kings (1649); KC II.1–6")
s('K10', b, "Milton o tahtı, doğunun en zengin krallarının hazinelerinden bile görkemli anlatır. Cenneti zorbalıkla suçlayan Şeytan, onun yerine kendi tahtını kurar.",
  "KC II.1–6; I.124 ('the tyranny of Heaven')")
s('K11', b, "Tarihteki başkaldırıların çoğu, elinden alınan hakları ve özgürlükleri geri istemek içindi. Ama bazıları özgürlük diye yola çıkıp yeni bir taht kurdu. Milton'ın kendi devriminde bile, kralı deviren Cromwell, Lord Koruyucu unvanıyla ülkeyi tek başına yönetti ve yerini oğluna bıraktı.",
  "kullanıcının görüşü (CLAUDE.md); Cromwell Lord Koruyucu 1653–1658, halefi oğlu Richard (1658)")
s('K12', b, "[slowly] Abdiel'in sözünü hatırla: “Sen özgür değilsin; kendi kendinin tutsağısın.” [pause] Başkaldırı her zaman özgürlük müdür?",
  "KC VI.181; C13'ün ödemesi")

# ───────────────────────── L. Gözyaşı ─────────────────────────
b = 'Bir damla yaş'
s('L01', b, "[curious] Peki ya o gözyaşları?", "bölüm sorusu; E07'nin ödemesi")
s('L02', b, "Milton'dan sonra ressamlar Şeytan'ı yeniden ve yeniden çizdi. {1866|Bin sekiz yüz altmış altı}'da Gustave Doré'nin gravürlerinde, karanlığa düşen kanatlı bir siluet oldu. Bu videodaki çizimler de onun izinden gidiyor.",
  "Doré, Paradise Lost, Cassell 1866, 50 levha")
s('L03', b, "Ondan yirmi yıl önce, Roma'daki Villa Medici'de genç bir Fransız ressam, Alexandre Cabanel, Düşmüş Melek'i yaptı.",
  "Cabanel, L'Ange déchu, 1847, Villa Médicis'ten ikinci envoi; Musée Fabre, Montpellier")
s('L04', b, "[softly] Kayalara uzanmış, kollarını yüzünün önünde kavuşturmuş bir melek. Kollarının arasından bize bakıyor. Gözleri öfkeli… ve dolu.",
  "tablonun betimi (Musée Fabre; Wikipedia 'The Fallen Angel')")
s('L05', b, "Bu gözyaşı, ressamın uydurması değildi. Milton, Şeytan'ı yenik ordusunun karşısında ağlatmıştı: kendi küçümsemesine rağmen, meleklerin ağladığı gibi.",
  "KC I.619–620")
s('L06', b, "[thoughtfully] O gözyaşı pişmanlık mıydı, gurur mu? Belki ikisi birden. Destanda bir yerde ağlıyor; bir yerde, “boyun eğmek” kelimesini söyleyemiyor.",
  "I.620 ve IV.81–82")
s('L07', b, "[slowly] Ve destan, Şeytan'la bitmez. Son sahnede iki insan, Âdem ile Havva, cennetten çıkar. Milton yazar: “Birkaç damla gözyaşı döktüler; ama çabuk sildiler. Dünya, bütün genişliğiyle önlerindeydi.”",
  "KC XII.645–647 (çevirimiz)")
s('L08', b, "Onlar, Şeytan'ın yapamadığını yapmıştı: suçlarını kabul edip af dilemişlerdi.",
  "KC X.1097–1104")
s('L09', b, "[slowly] En başta sorduk: Zincirleri çözülen birini, cehennemde tutan neydi? Milton'ın cevabı belki de Nifates Dağı'nda söylenemeyen o tek kelimede saklı. [pause] Kimsenin takmadığı, insanın kendi eliyle taktığı bir zincir.",
  "A04'ün cevabı; G09; VI.181")
s('L10', b, "[thoughtfully] Kör şair bu hikâyeyi zifiri karanlıkta yazdırdı. Ama belki de cehennemin en çok insanın içinde olduğunu, en iyi o gördü.",
  "çerçevenin kapanışı (B10–B12)")
s('L11', b, "[curious] Peki sen ne düşünüyorsun? Blake mi haklıydı, Lewis mi? O gözyaşı pişmanlık mı, gurur mu? Ve başkaldırı ne zaman özgürlüktür, ne zaman insanın kendi cehennemi? Yorumlarda yaz.",
  "izleyiciye soru")
s('L12', b, "[warmly] Tanrılara kafa tutan bir başka asinin, Prometheus'un hikâyesi ekranda. Bu hikâyeler hoşuna gidiyorsa, kanala abone olmayı unutma.",
  "bitiş ekranı: Prometheus videosu + abone")

# ───────────────────────── üretim ─────────────────────────
def alt_of(m):
    m = re.sub(r'\[[^\]]*\]\s*', '', m)
    m = re.sub(r'\{([^|}]*)\|[^}]*\}', r'\1', m)
    return re.sub(r'\s+', ' ', m).strip()

def tts_of(m):
    m = re.sub(r'\{[^|}]*\|([^}]*)\}', r'\1', m)
    for a, o in OKUNUS:
        m = re.sub(r'(?<![\wçğıöşüÇĞİÖŞÜ])' + re.escape(a) + r'(?![a-zçğıöşü])', o, m)
    m = m.replace('[pause]', '…')
    return re.sub(r'\s+', ' ', m).strip()

segs = [{'id': i, 'bolum': bo, 'tts': tts_of(m), 'alt': alt_of(m), 'kaynak': k} for i, bo, m, k in S]
ids = [x['id'] for x in segs]; assert len(ids) == len(set(ids)), 'yinelenen id'
out = {
    'voice': 'Emrullah (voice_id seslendirme öncesi creative_list_voices ile bulunur)',
    'revizyon': 1,
    'not': "tts: seslendirme metni (ses etiketleri, özel adlar okunuşa göre, sayılar yazıyla). alt: altyazı metni. kaynak: iddianın dayanağı. KC = Kayıp Cennet, 1674 baskısı, kitap.dize (kaynak/kayip_cennet_1674_dizeler.json). Bütün dize çevirileri bizim (özgün metin kamu malı). DNB = Dictionary of National Biography, cilt 38 (1894), 'Milton, John'.",
    'segments': segs,
}
json.dump(out, open(os.path.join(ROOT, 'senaryo.json'), 'w'), ensure_ascii=False, indent=1)
ch = sum(len(x['alt']) for x in segs)
print(len(segs), 'cümle;', ch, 'karakter (altyazı); tahmini süre', round(ch / 13.0 / 60, 1), 'dk')
from collections import OrderedDict
c = OrderedDict()
for x in segs: c[x['bolum']] = c.get(x['bolum'], 0) + len(x['alt'])
for k, v in c.items(): print(f'  {k:28s} {v:5d} kr  ~{v/13/60:4.1f} dk')
