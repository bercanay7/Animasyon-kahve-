"""Milton senaryosu, revizyon 2 (senaryo kurulu tur 1 kararlarıyla; bkz. kurul/senaryo_tur1/KARAR.md) → senaryo.json
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
    ('Lucifer', 'Lüsifer'), ('Beelzebub', 'Belzebub'), ('Pandemonium', 'Pandemonyum'),
    ('Abdiel', 'Abdiyel'), ('Uriel', 'Uriyel'), ('Cromwell', 'Kromvel'),
    ('Gustave Doré', 'Güstav Dore'), ('Doré', 'Dore'), ('Alexandre Cabanel', 'Aleksandr Kabanel'),
    ('Cabanel', 'Kabanel'), ('Villa Medici', 'Villa Mediçi'), ('Charles', 'Çarls'),
    ('Prometheus', 'Prometeus'), ('Hürmüz', 'Hürmüz'), ('Zaman Kuryesi', 'Zaman Kuryesi'),
]

S = []
def s(id_, bolum, metin, kaynak=''):
    S.append((id_, bolum, metin, kaynak))

# Etiket kuralı (A-Ses): her segment açık bir etiketle başlar; anlatıcıya dönüş [calmly];
# karakter sözünün etiketi açılış tırnağının hemen önünde. Duraklar seste değil vo/plan.json'da kurulur.

# ───────────────────────── A. Kanca ─────────────────────────
b = 'Cehennem benim'
s('A01', b, "[slowly] “Hangi yana kaçsam cehennem. Ben cehennemim.”",
  "KC IV.75 (çevirimiz). Ses: G07'nin seçilen çekiminden kesilebilir (A-Ses). Ekranda künye: John Milton · Kayıp Cennet · IV.75")
s('A02', b, "[calmly] Bunu söyleyen, bir zamanlar cennetin en parlak meleğiydi.",
  "KC V.659–661, V.708–709, VII.131–133")
s('A03', b, "[curious] Birazdan cehennemden kaçacak. Ama cehennemden bir adım bile uzaklaşamayacak. Neden?",
  "KC IV.18–23 ('nor from Hell one step… can fly'); merak sorusu, cevabı L09–L09c")
s('A04', b, "[darkly] Hikâye, onun gözlerini açtığı yerde başlar: yanan bir gölün ortasında. Dokuz gün düşmüştü. Etrafında alev var ama ışık yok; yalnızca görünür bir karanlık. Kırılmaz zincirlerle bu göle bağlı.",
  "KC I.56–58, VI.871, I.62–63, I.48, I.210")
s('A05', b, "[thoughtfully] Bu hikâye bir şiirden: John Milton'ın destanı, Kayıp Cennet'ten. Buradaki Şeytan, Milton'ın kaleminden çıkmış bir karakter; biz de onu bir din anlatısı olarak değil, bir edebiyat eseri olarak okuyacağız.",
  "kullanıcı kararı (yalnız edebi okuma); H-Hassasiyet + H-Hukuk ortak metni; 1667 yılı ekran yazısı")
s('A06', b, "[softly] Ve bu destanı yazdıran şair, hiçbir şey göremiyordu.",
  "1652'den itibaren tam kör (Wikipedia 'John Milton', Leonard 2000)")

# ───────────────────────── B. Kör şair ─────────────────────────
b = 'Kör şair'
s('B01', b, "[curious] Hiçbir şey göremeyen bir adam, cehennemi nasıl bu kadar iyi gördü?",
  "bölüm sorusu; ödemesi L10")
s('B02', b, "[softly] Londra'da bir ev; gece. Gözleri görmeyen bir adam uyuyamıyor. Anlatılanlara göre bazen dizeleri uykusuz gecelerde zihninde kurar, kızını uyandırıp ona yazdırırdı: kırk dizeyi bir solukta söyler, sonra yirmiye indirirdi. Çoğu zaman da evde kim varsa, ona.",
  "DNB s. 37 (uykusuz gecelerde kızına; 40 → 20 dize; evde bulunan herkese 10–30 dize); 'Londra, 1660'lar' ekran yazısı")
s('B03', b, "[sadly] İki küçük kızına, hiç bilmedikleri dilleri okumayı öğretmişti: İbranice, Yunanca, Latince. Kızlar, göremeyen babalarına, tek kelimesini anlamadıkları metinleri sesli okurdu. Bu saatler, yıllar içinde onlar için dayanılmaz bir hâl aldı.",
  "DNB s. 36 (Phillips; 'almost beyond endurance')")
s('B04', b, "[thoughtfully] Milton kırk üç yaşında tamamen kör olmuştu. Ama yalnızca bir şair değil, bir devrimciydi: Kralın idamını savunmuş, kralı deviren devrimin hükümetinde çalışmıştı.",
  "d. 9 Aralık 1608, 1652'de tam kör; Tenure of Kings, Eikonoklastes (1649); Yabancı Diller Sekreteri 1649–1660")
s('B05', b, "[darkly] Sonra devrim çöktü; krallık geri döndü. Kitapları cellat eliyle yakıldı, kendisi bir süre hapse atıldı. Destana devrim henüz ayaktayken başlamıştı; büyük kısmını bu yenilginin içinde yazdırdı.",
  "DNB s. 33 (16 Haziran 1660 kararı, yakma; yazın tutuklanma, harç ödeyince salıverilme); DNB s. 34 (yazım 1658'de başlar, Aubrey'e göre 1663'te biter); '1660' ekran yazısı")
s('B06', b, "[calmly] Destanın üçüncü kitabında kendi körlüğünü anlatır: [tenderly] “Mevsimler döner; ama bana gün dönmez. Ne sabah ne akşam, ne bahar çiçeği ne yaz gülü. Ne de bir insan yüzü.”",
  "KC III.40–44 (çevirimiz, kısaltılmış)")
s('B07', b, "[reverently] “Öyleyse sen, göksel ışık, içime parla. Orada gözler aç ki, ölümlü gözün göremediğini göreyim ve anlatayım.”",
  "KC III.51–55 (çevirimiz)")
s('B08', b, "[thoughtfully] Işığını ve devrimini kaybetmiş bir şair, ışığını ve savaşını kaybetmiş bir meleği anlatacaktı.",
  "anlatıcının köprüsü")
s('B09', b, "[mysterious] Yeğeninin anlattığına göre, bu hikâyenin ilk dizeleri çok daha önce, Milton'ın gözleri henüz görürken, bir tiyatro oyununun açılışı olarak yazılmıştı. Ve o dizeler bir zafer şarkısı değildi: Şeytan'ın güneşe yaptığı bir itiraftı. Oraya geleceğiz.",
  "DNB s. 34: Phillips, tasarlanan tragedyanın açılışının (~1642) bugün IV. kitabın başındaki Şeytan konuşması olduğunu bildirir; yorumcular IV.32–41 olarak belirler. Ödemesi G02b")
s('B10', b, "[calmly] Ama önce, o meleğin düşmeden önceki hâline bakalım.", "")

# ───────────────────────── C. Cennet ─────────────────────────
b = 'Işık taşıyan'
s('C01', b, "[curious] Her şeye sahip olan biri, neden başkaldırır?", "bölüm sorusu; iki cevabı C06")
s('C02', b, "[calmly] Milton'ın cenneti ışıktan bir dünyadır. O dünyanın en parlak varlıklarından biri bir başmelektir: başmeleklerin en büyüklerinden biri, belki de en büyüğü.",
  "KC V.659–661 ('of the first, if not the first Arch-Angel')")
s('C03', b, "[calmly] Milton onun cennetteki adını vermez: [gravely] “Eski adı artık cennette anılmıyor; ona bundan böyle Şeytan deyin.” [calmly] Yalnızca birkaç yerde, “öyle diyelim” diyerek ona Lucifer der, yani ışık taşıyan. Bir zamanlar meleklerin arasında, yıldızların arasındaki sabah yıldızından bile parlakmış.",
  "KC V.658–659; Lucifer: V.760, VII.131–133, X.425 ('so call him'); sabah yıldızı: V.708–709, VII.132–133")
s('C04', b, "[gravely] Bir gün, Milton'ın anlattığına göre, Tanrı bütün melekleri toplar ve Oğul'u onların başına geçirir. Bundan sonra herkes onun önünde diz çökecek; ona karşı gelen, Tanrı'ya karşı gelmiş sayılacak ve dönüşü olmayan bir karanlığa düşecektir.",
  "KC V.600–615; Tanrı ve Oğul figürle değil, ışıkla gösterilir (kullanıcı kararı)")
s('C05', b, "[darkly] Gece yarısı, yardımcısını gizlice uyandırır. Ordulara bir yalan söylenir: Kuzeydeki saraya, yeni kralı karşılamaya hazırlanmak için gidecekler.",
  "KC V.667–693")
s('C06', b, "[calmly] Ve orada konuşur. Sözlerindeki kelime, isyanların en eski kelimesidir: özgürlük.", "KC V.772–802")
s('C07', b, "[defiantly] “Boyun eğip diz mi bükeceksiniz? Biz cennetin öz evlatlarıyız. Hepimiz eşit değiliz belki, ama hepimiz eşit ölçüde özgürüz. Yasa olmadan da yoldan çıkmayan bizlere, kim yasa koyabilir?”",
  "KC V.787–799 (çevirimiz, kısaltılmış). 'Boyun eğmek' ile G09b aynı sözcük ve jest")
s('C08', b, "[calmly] Sabah yıldızı gibi yüzü ve yalanlarıyla, cennetin ordularının üçte birini peşinden sürükler.",
  "KC V.708–710 ('allured them, and with lies drew after him the third part')")
s('C09', b, "[thoughtfully] Neden? Kendisine sorsanız: özgürlük için. Milton'a sorsanız, iki kelime: kıskançlık ve gurur. Kendini küçük düşürülmüş saymıştı. Bu iki cevap, hikâyenin sonuna kadar yan yana yürüyecek.",
  "KC V.662–665 ('fraught with envy… through pride… thought himself impaired')")
s('C10', b, "[softly] Ama bir melek ayağa kalkar. Adı Abdiel'dir.", "KC V.803–808")
s('C11', b, "[calmly] Abdiel ona karşı çıkar; sonra binlerce küçümseyen bakışın arasından, tek başına yürüyüp gider. Milton onu şöyle anlatır: binlerce hainin arasında sadık kalan tek kişi.",
  "KC V.896–907")
s('C12', b, "[thoughtfully] Peki burada asıl başkaldıran kim: kalabalığı peşine takan mı, kalabalığa karşı tek başına duran mı? Bu soruyu aklında tut.",
  "kurulum; ödemesi K12")

# ───────────────────────── D. Savaş ve düşüş ─────────────────────────
b = 'Dokuz gün'
s('D01', b, "[darkly] Cennette ilk kez kılıçlar çekilir. Ve ölümsüz bir varlık, birazdan acının ne olduğunu öğrenecek.", "bölüm vaadi; ödemesi D04")
s('D02', b, "[calmly] İlk darbeyi Abdiel vurur. Kılıcı Şeytan'ın miğferine iner; Şeytan on adım geriler, onuncu adımda dizinin üstüne çöker.",
  "KC VI.189–195")
s('D03', b, "[calmly] Abdiel darbeden önce ona şunu söylemişti: [firmly] “Asıl kölelik budur: akılsıza ya da kendinden üstüne başkaldırana hizmet etmek; seninkilerin şimdi sana ettiği gibi. Sen de özgür değilsin; kendi kendinin tutsağısın.”",
  "KC VI.178–181 (çevirimiz, kısaltılmış)")
s('D04', b, "[calmly] Ve eklemişti: [firmly] “Sen cehennemde, kendi krallığında hüküm sür; bırak ben cennette hizmet edeyim. Ama cehennemde krallık değil, zincir bekle.”",
  "KC VI.183–186 (çevirimiz). I.263'ün habercisi; ödemesi L09b")
s('D05', b, "[darkly] Savaşın ortasında bir başmeleğin kılıcı, Şeytan'ın sağ yanını yarar. Milton yazar: Şeytan acıyı ilk kez o an tanıdı.",
  "KC VI.320–327 ('Then Satan first knew pain')")
s('D06', b, "[calmly] Yarası çabucak kapanır. Ama bir zamanlar parlayan zırhı artık lekelidir.", "KC VI.330–334")
s('D07', b, "[calmly] Asiler barutu ve topu icat eder. Sadık melekler de dağları kökünden söküp üzerlerine atar.",
  "KC VI.482–520, VI.584–594; VI.639–666")
s('D08', b, "[awed] Üçüncü gün, Oğul ışıktan bir savaş arabasıyla gelir. Asiler cennetin kıyısına kadar sürülür ve kendilerini boşluğa atarlar.",
  "KC VI.699, VI.748–866")
s('D09', b, "[gravely] Dokuz gün düştüler. Kaos kükredi. Sonunda cehennem ağzını açıp onları yuttu ve üzerlerine kapandı.",
  "KC VI.871–875")
s('D10', b, "[calmly] Ve hikâye, en başta gördüğümüz yere döner: yanan göle.", "")

# ───────────────────────── E. Cehennem ─────────────────────────
b = 'Cehennemde kral'
s('E01', b, "[curious] Her şeyini kaybeden biri, ilk olarak ne söyler?", "bölüm sorusu")
s('E02', b, "[calmly] Şeytan, yanında yatan yardımcısı Beelzebub'u görür. İlk sözleri bir şaşkınlıktır: [sadly] “Sen o musun? Ah, ne kadar düşmüş, ne kadar değişmişsin! Bir zamanlar ışık diyarında, binlerce parlak varlığı gölgede bırakırdın.”",
  "KC I.79–87 (çevirimiz, kısaltılmış)")
s('E03', b, "[calmly] Ama hemen toparlanır: [defiantly] “Meydanı kaybettik; ne çıkar? Her şey kaybedilmiş değil: yenilmez irade, intikam hırsı, ölümsüz nefret ve asla boyun eğmeyen yüreklilik hâlâ bizde.”",
  "KC I.105–109 (çevirimiz, kısaltılmış)")
s('E04', b, "[calmly] Şair bu sözlerin hemen ardından bir not düşer: Şeytan acı içinde böbürleniyordu; içi derin bir umutsuzlukla kıvranırken. [softly] Bu sözleri yazdıran adam da, bir savaşı kaybetmişti.",
  "KC I.125–126; Milton'ın yenilgisi B04–B05")
s('E05', b, "[calmly] Sonra gölden kalkar. Milton'a göre bunu ancak cennet izin verdiği için yapabilir.",
  "KC I.209–213 ('but that the will and high permission of all-ruling Heaven left him at large')")
s('E06', b, "[calmly] Yanan kıyıya çıkınca cehennemi selamlar: [proudly] “Elveda, mutlu ovalar; selam size, dehşetler! Ve sen, en derin cehennem, yeni sahibini karşıla. Zihin kendi dünyasıdır; kendi içinde cehennemi cennet, cenneti cehennem yapabilir.”",
  "KC I.249–255 (çevirimiz, kısaltılmış; 'thy new possessor' I.252)")
s('E07', b, "[calmly] Sonra destanın en ünlü dizesini söyler: [proudly] “Cehennemde hükümdar olmak, cennette hizmetkâr olmaktan yeğdir.”",
  "KC I.263 (çevirimiz). Menteşe; Abdiel'in uyarısı D04")
s('E09', b, "[calmly] Kalkanı omzunda ay gibi asılıdır. Mızrağının yanında en büyük geminin direği bir değnek gibi kalırdı; ona yaslanarak yanan topraklarda yürür.",
  "KC I.283–296")
s('E10', b, "[calmly] Yüzünde yıldırımların açtığı derin izler var; ama hâlâ yıkılmış bir başmelek kadar görkemli. Milton o yüzü anlatırken iki şeyi yan yana yazar: kaşlarının altında gurur, gözlerinde pişmanlık.",
  "KC I.591–605 ('considerate pride… cast signs of remorse and passion')")
s('E11', b, "[softly] Ordusuna bakar: kendi suçu yüzünden cennetten atılmış milyonlarca ruh. Yıldırım çarpmış bir ormanın ağaçları gibi yanık, ama hâlâ ayaktalar. Konuşmaya hazırlanır; boğazı düğümlenir. Üç kez dener; üç kez, ağlamayı gururuna yediremese de, gözlerinden yaşlar boşanır: meleklerin ağladığı gibi.",
  "KC I.605–621 ('Tears, such as Angels weep'); ödemesi L05")
s('E12', b, "[calmly] Şeytanlar cehennemin toprağından altın kazar. Bir saatten kısa sürede, yerden devasa bir saray yükselir: Pandemonium, bütün şeytanların meclisi.",
  "KC I.670–730 (I.697 'in an hour'), I.756; görsel: Dor sütunlu, altın tavanlı tapınak (I.713–717)")
s('E13', b, "[calmly] Mecliste kimi yeni bir savaş ister, kimi sessizce katlanmayı, kimi cehennemde kendi krallıklarını kurmayı. Sonunda Şeytan'ın planı kabul edilir: Tanrı'nın yeni yarattığı dünyaya, insana saldırmak.",
  "KC II.51–378 (Moloch, Belial, Mammon, Beelzebub; plan Şeytan'ın: II.379–380)")
s('E14', b, "[darkly] Kimsenin gitmeye cesaret edemediği bu yolculuğa, yalnızca o gönüllü olur.", "KC II.417–466")
s('E15', b, "[wryly] Ayağa kalktığında bütün cehennem önünde eğilir; onu Tanrı'ya denk sayıp yüceltirler. Diz çökmeyi reddeden melek, şimdi önünde diz çökülen bir kraldır.",
  "KC II.476–479; taht II.1–6")

# ───────────────────────── F. Kapı ve Kaos ─────────────────────────
b = 'Kapıdaki bekçiler'
s('F01', b, "[curious] Cehennemin kapısında, onu çok iyi tanıyan biri bekliyordu. Peki Şeytan onu neden tanımadı?", "bölüm sorusu; cevabı F04")
s('F02', b, "[calmly] Dokuz katmanlı kapıda iki bekçi vardır: yarısı kadın, yarısı yılan bir varlık; ve biçimi olmayan bir gölge.",
  "KC II.645–673")
s('F03', b, "[calmly] Şeytan gölgeyle dövüşmeye hazırlanırken kadın araya girer: [bitterly] “Beni unuttun mu? Cennette sen isyanı tasarlarken başının sol yanı yarıldı ve ben oradan doğdum. Bana Günah dediler.”",
  "KC II.746–760 (çevirimiz, kısaltılmış)")
s('F04', b, "[darkly] Şeytan onu tanımaz; kendi aklından doğan şeyi tanımaz. Ve dövüşmek üzere olduğu o gölgenin kim olduğunu öğrenir: Ölüm. Kendi oğlu.",
  "KC II.737–745, II.781–787 ('Thine own begotten')")
s('F05', b, "[calmly] Kapı açılır. Önünde ne başı ne sonu olan karanlık bir okyanus vardır: Kaos.", "KC II.871–916")
s('F06', b, "[calmly] Kanatlarını açıp uçar; sonra boşluğa düşer, binlerce kulaç aşağı. Bir rüzgâr onu yeniden yukarı fırlatmasa, hâlâ düşüyor olurdu.",
  "KC II.927–938")
s('F07', b, "[awed] Sonunda uzakta bir şey görür: cennete altın bir zincirle asılı, ayın yanındaki en küçük yıldız kadar bir dünya.",
  "KC II.1051–1053")
s('F08', b, "[calmly] Güneşe varır. Genç bir melek kılığına girip güneşin bekçisi Uriel'e yolu sorar. Milton'a göre ne insan ne melek, ikiyüzlülüğü göremez.",
  "KC III.634–684")
s('F09', b, "[calmly] Uriel yolu gösterir. Şeytan aşağı süzülür ve bir dağın, Nifates'in tepesine konar.", "KC III.724–742")

# ───────────────────────── G. Nifates ─────────────────────────
b = 'Güneşe itiraf'
s('G01', b, "[curious] Kimsenin duymadığını sanırken, Şeytan kendine ne söyler?", "bölüm sorusu")
s('G02', b, "[calmly] Cehennemden kurtulmuştur. Ama şair uyarır: Cehennemi içinde taşıyor. Kendinden nasıl kaçamıyorsa, cehennemden de bir adım uzaklaşamaz.",
  "KC IV.18–23; A03 sorusunun ilk kısmi cevabı")
s('G02b', b, "[softly] Ve şimdi, Milton'ın yıllar önce, gözleri henüz görürken yazdığı o ilk dizeler.",
  "DNB s. 34 (Phillips); IV.32–41. Ödeme: B09")
s('G03', b, "[calmly] Güneşe bakar: [bitterly] “Ey ihtişamla taçlanmış güneş… Sana dostça seslenmiyorum. Işınlarından nefret ettiğimi söylemek için adını anıyorum; çünkü bana hangi yücelikten düştüğümü hatırlatıyorlar.”",
  "KC IV.32–39 (çevirimiz, kısaltılmış)")
s('G04', b, "[softly] Sonra hiç beklemediğimiz bir şey söyler, hem de Tanrı için: [quietly] “Benden böyle bir karşılığı hak etmemişti. Beni yaratmıştı; iyiliğini kimsenin başına kakmazdı. Ona hizmet etmek de ağır değildi.”",
  "KC IV.42–45 (çevirimiz)")
s('G05', b, "[sadly] “Keşke beni sıradan bir melek yaratsaydı. O zaman mutlu kalırdım.”", "KC IV.58–61 (çevirimiz, kısaltılmış)")
s('G06', b, "[thoughtfully] Sonra kendine bir soru sorar: [quietly] “Sadık kalanlar gibi senin de özgür iraden, ayakta kalma gücün yok muydu? Vardı. O hâlde kimi suçlayacaksın?”",
  "KC IV.63–68 (çevirimiz, kısaltılmış)")
s('G07', b, "[slowly] [anguished] “Vay hâlime! Sonsuz gazaptan, sonsuz umutsuzluktan nereye kaçayım? Hangi yana kaçsam cehennem. Ben cehennemim.”",
  "KC IV.73–75 (çevirimiz). A01 ile aynı kompozisyon ve ekran yazısı")
s('G08', b, "[anguished] “En derin dipte, beni yutmak için ağzını açan daha derin bir dip var. Onun yanında, çektiğim cehennem cennet gibi kalıyor.”",
  "KC IV.76–78 (çevirimiz)")
s('G09', b, "[calmly] Bir an yumuşar: [trembling] “Pişmanlığa hiç yer kalmadı mı? Bağışlanmaya?”",
  "KC IV.79–80 (çevirimiz). Ardından filmin tek tam sessizliği (plan.json gap 2,0)")
s('G09b', b, "[calmly] Cevabı yine kendisi verir: [coldly] “Bir yol kaldı: boyun eğmek. Ama o sözü ağzıma almayı, gururum yasaklıyor.”",
  "KC IV.81–82 (çevirimiz); C07 'boyun eğmek' ile aynı sözcük; L09b")
s('G10', b, "[calmly] Gururu, ve cehennemde bıraktığı ordunun önünde rezil olma korkusu. Onlara vaat ettiği şey boyun eğmek değil, Tanrı'yı yenmekti.",
  "KC IV.82–86; ödemesi J06")
s('G11', b, "[bitterly] “Onlar beni cehennemin tahtında yüceltirken, içimde nasıl inlediğimi bilmiyorlar. Tacım ve asam ne kadar yükselirse, ben o kadar aşağı düşüyorum.”",
  "KC IV.86–92 (çevirimiz, kısaltılmış)")
s('G12', b, "[calmly] Belki de en dürüst sözünü söyler: [quietly] “Diyelim ki pişman oldum ve eski yerime döndüm. Ne kadar sürer? Yükselince, yükseklik yine başımı döndürür. Acı içinde verdiğim sözleri, rahata erince geri alırım.”",
  "KC IV.93–97 (çevirimiz, kısaltılmış)")
s('G13', b, "[bitterly] “Bunu beni cezalandıran da biliyor. O barış vermekten ne kadar uzaksa, ben de dilemekten o kadar uzağım.”",
  "KC IV.103–104 (çevirimiz). İkinci okuma için kurulum; ödemesi L09c")
s('G14', b, "[calmly] Sonunda kararını verir: [coldly] “Elveda umut. Umutla birlikte, elveda korku. Elveda pişmanlık.” [quietly] “Kötülük: sen benim iyiliğim ol.”",
  "KC IV.108–110 (çevirimiz). Shorts bu cümleyle bitmez (H-Hassasiyet)")
s('G15', b, "[softly] Bu sözleri söylerken yüzü üç kez değişir: öfkeyle, kıskançlıkla, umutsuzlukla. Kimsenin görmediğini sanır; ama güneşin bekçisi Uriel, hepsini görmüştür.",
  "KC IV.114–130")
s('G16', b, "[thoughtfully] Şeytan'ı burada, onu alkışlayan bir kalabalık olmadan görüyoruz. Maskesiz. Acımak, hak vermek değildir. Ama ilk kez, ona acıyoruz.",
  "empati anı; S-Dram + H-Hassasiyet ortak metni")

# ───────────────────────── H. Aden ─────────────────────────
b = "Aden'de bir yabancı"
s('H01', b, "[curious] Yok etmeye geldiğin bir şeyi, sevebilir misin?", "bölüm sorusu")
s('H02', b, "[calmly] Şeytan Aden bahçesine varır. Doğudaki tek kapıyı küçümser; tek sıçrayışta duvarın üstünden atlar.", "KC IV.178–183")
s('H03', b, "[calmly] Bahçenin en yüksek ağacına, hayat ağacına tüner: bir karabatak gibi.", "KC IV.194–196")
s('H04', b, "[softly] Ve ilk kez onları görür: Âdem ile Havva'yı.", "KC IV.288 vd. Görsel: uzak, örtülü siluet (H-Hukuk, H-Hassasiyet)")
s('H05', b, "[wistfully] “Onları hayranlıkla seyrediyorum,” der. “Onları sevebilirim bile. Bu savunmasız hâllerine acıyabilirim; bana acıyan olmasa da.”",
  "KC IV.358–375 (çevirimiz, kısaltılmış)")
s('H06', b, "[calmly] “Masumiyetiniz karşısında yüreğim yumuşuyor,” der. Ama hemen ekler: krallığının çıkarı, onuru ve intikamı onu buna mecbur bırakıyor.",
  "KC IV.388–392")
s('H07', b, "[gravely] Şair burada araya girer: “Böyle konuştu Şeytan; zorbaların hep sığındığı bahaneyle, zorunlulukla, şeytanca işlerine kılıf uydurdu.”",
  "KC IV.393–394 (çevirimiz: 'the Fiend… necessity, the tyrant's plea')")
s('H08', b, "[calmly] Sonra iki insanı yan yana görür: [bitterly] “Nefret edilesi manzara! İşkence veren manzara! Bu ikisi birbirinin kollarında cennetteler. Bense, sevincin de sevginin de olmadığı bir cehenneme itildim.”",
  "KC IV.505–511 (çevirimiz, kısaltılmış; 'Imparadised in one another's arms' görselde yalnız yan yana iki siluet)")
s('H09', b, "[darkly] Gece olunca, Havva'nın kulağının dibine çömelir: bir kurbağa gibi. Ona rüyalar fısıldar.", "KC IV.799–809")
s('H10', b, "[calmly] Bekçi meleklerden biri mızrağının ucuyla ona dokununca, gerçek biçimine döner.", "KC IV.810–819")
s('H11', b, "[defiantly] “Beni tanımıyor musunuz?” diye kükrer. [calmly] Melekler cevap verir: [firmly] “Parlaklığının hâlâ aynı olduğunu sanma. İyi olmaktan çıktığın gün, o ışık seni terk etti. Şimdi günahına benziyorsun.”",
  "KC IV.827–840 (çevirimiz, kısaltılmış); F04 ile ayna")
s('H12', b, "[softly] Şeytan utanç içinde kalakalır. İyiliğin ne kadar heybetli olduğunu hisseder ve kaybettiğine yanar; en çok da sönükleşen ışığının başkalarının gözünden kaçmadığını görünce.",
  "KC IV.846–850; C09 'küçültülmüş' ile ayna")

# ───────────────────────── I. Yılan ─────────────────────────
b = 'Yılanın içinde'
s('I01', b, "[whispers] İntikam, tatlı mıdır?", "bölüm sorusu; cevabı I05")
s('I02', b, "[calmly] Şeytan bahçeden kovulur. Yedi gece boyunca karanlıkla birlikte dünyanın çevresinde döner. Sekizinci gece, gizlice geri sızar.",
  "KC IV.1013–1015; IX.53–69")
s('I03', b, "[calmly] Dünyaya bakar ve yine itiraf eder: [sadly] “Bir şeyden sevinç duyabilseydim, seni nasıl da dolaşırdım! Ama etrafımda ne kadar güzellik görürsem, içimde o kadar işkence duyuyorum.”",
  "KC IX.114–122 (çevirimiz, kısaltılmış)")
s('I04', b, "[calmly] Uyuyan bir yılan bulur ve ağzından içine girer: [disgusted] “Ne iğrenç bir alçalış! Bir zamanlar en yüce yer için yarışan ben, şimdi bir hayvanın bedenine hapsoluyorum.”",
  "KC IX.159–167, IX.182–190 (çevirimiz, kısaltılmış)")
s('I05', b, "[calmly] Ve kendi geleceğini söyler: [bitterly] “İntikam önce tatlıdır; ama çok geçmeden acılaşır ve dönüp sahibini vurur.”",
  "KC IX.171–172 (çevirimiz)")
s('I06', b, "[softly] Sabah, Havva'yı bahçede yalnız görür. Sonra destanın belki de en şaşırtıcı anı gelir: Havva'nın masumiyeti karşısında Şeytan, kendi kötülüğünden kopup dalgın durur. Nefreti, hilesi, kıskançlığı, intikamı; hepsi elinden düşer. Milton'ın deyişiyle, bir süre sersem bir iyilik içinde donakalır.",
  "KC IX.455–466 ('stupidly good': 17. yy'da 'sersemlemiş, donakalmış')")
s('I07', b, "[darkly] Ama içinde hep yanan o cehennem, cennetin ortasında bile, bu sevinci çabucak bitirir.", "KC IX.467–470")
s('I08', b, "[calmly] Yılanın diliyle konuşur, Havva'yı ikna eder. Havva meyveyi koparır ve yer; sonra Âdem de.", "KC IX.532–781, IX.996–999")
s('I09', b, "[softly] Dünya yarayı hisseder; doğa iç çeker ve her şeyin kaybedildiğini haber verir. Suçlu yılan, sessizce çalılığa süzülür.", "KC IX.782–785")
s('I10', b, "[calmly] Kazanmıştır.", "")

# ───────────────────────── J. Alkış ─────────────────────────
b = 'Alkış'
s('J01', b, "[curious] Zafer anında, insan ne duymayı bekler?", "bölüm sorusu")
s('J02', b, "[calmly] Şeytan cehenneme döner. Sıradan bir asker kılığında saraya girer, tahtına çıkar ve birden eski parlaklığıyla belirir; Milton'ın deyişiyle, sahte bir parıltıyla. Cehennem çığlıklarla onu karşılar.",
  "KC X.441–457 (X.451–452 'false glitter')")
s('J03', b, "[triumphantly] “İnsanı yaratıcısından kopardım,” der. “Hem de bir elmayla! Gülmeye değmez mi?”", "KC X.485–488 (çevirimiz, kısaltılmış)")
s('J04', b, "[softly] Ve susar. O büyük alkışı bekler.", "KC X.504–506. Ardından gap 2,0 (müzik de susar)")
s('J05', b, "[softly] Ama her yandan, sayısız dilden yükselen tek bir ses duyar: kasvetli, ortak bir tıslama. Herkesin aşağılaması.", "KC X.506–509")
s('J06', b, "[calmly] Nifates Dağı'nda, bu kalabalığın önünde rezil olmaktan korktuğu için boyun eğememişti. Şimdi aynı kalabalık ona tıslıyor.",
  "G10'un ödemesi (S-Dram)")
s('J07', b, "[darkly] Şaşırır; ama çok geçmeden asıl kendi hâline şaşırır. Yüzünün sivrildiğini hisseder. Kolları kaburgalarına yapışır, bacakları birbirine dolanır ve yüzüstü yere yığılır: devasa bir yılan. Önünde diz çökülen kral, şimdi karnının üstünde.",
  "KC X.509–514; E15'in ödemesi")
s('J08', b, "[calmly] Konuşmak ister; ağzından yalnızca tıslama çıkar. Bütün şeytanlar yılana dönüşmüştür.", "KC X.517–521")
s('J09', b, "[gravely] Günahı hangi kılıkta işlediyseler, cezasını da o kılıkta çekerler. Alkışları tıslamaya, zaferleri kendi ağızlarından kendi üstlerine yağan bir utanca dönüşür.",
  "KC X.516, X.545–547")
s('J10', b, "[calmly] Önlerinde meyveyle dolu ağaçlar belirir. Açlıkla saldırırlar; meyveler ağızlarında acı küle döner.", "KC X.547–570")
s('J11', b, "[thoughtfully] Ve Şeytan destandan sessizce çekilir. Son iki kitapta bir daha sahneye çıkmaz.", "KC XI–XII: Şeytan yalnız anılır")

# ───────────────────────── K0. Destanın sonu ─────────────────────────
b = 'Dünya önlerindeydi'
s('K01', b, "[softly] Destan, Şeytan'la bitmez. Son sahnede Âdem ile Havva, kaybettikleri cennetten, Aden'den çıkar. Milton yazar: [tenderly] “İnsanca birkaç damla gözyaşı döktüler; ama çabucak sildiler. Bütün dünya önlerindeydi.”",
  "KC XII.645–647 (çevirimiz). Görsel: arkadan, uzak, el ele iki siluet")
s('K02', b, "[calmly] Onlar, Şeytan'ın yapmadığını yapmışlardı: kusurlarını kabul edip bağışlanma dilemişlerdi.", "KC X.1097–1104 ('faults')")
s('K03', b, "[thoughtfully] Ama Milton'ın Tanrı'sı bunu destanın başında söylemişti: İnsan aldatıldı; bu yüzden merhamet bulacak. İsyancı melekler kendi kendilerini ayarttı; onlar bulamayacak.",
  "KC III.129–132; ikinci okuma için kurulum (K-Uzman); L09c")
s('K04', b, "[calmly] Şeytan hakkındaki asıl kavga ise, Milton öldükten sonra başladı.", "köprü; Milton ö. 8 Kasım 1674")

# ───────────────────────── K. İki okuma ─────────────────────────
b = 'İki okuma'
s('K05', b, "[curious] Bu hikâyenin kahramanı kim?", "bölüm sorusu")
s('K06', b, "[calmly] Milton destanın en başında amacını açıkça söyler: Tanrı'nın insanlara karşı yollarının adil olduğunu göstermek.", "KC I.26 (çevirimiz)")
s('K07', b, "[thoughtfully] Ama yüz yıldan fazla sonra, şair ve ressam William Blake başka bir şey gördü: Milton, melekleri ve Tanrı'yı anlatırken zincirliydi; şeytanları ve cehennemi anlatırken özgür. Çünkü gerçek bir şairdi ve farkında olmadan Şeytan'ın tarafındaydı.",
  "Blake, The Marriage of Heaven and Hell (1790–93), 'The Voice of the Devil' notu (çevirimiz)")
s('K08', b, "[softly] Kendine sor: bu hikâyeden aklında kalan sözler, kimin sözleri?", "S-Dram")
s('K09', b, "[calmly] Romantik şairler de Şeytan'da bir isyan kahramanı gördü.", "Byron, Shelley, Hazlitt (Wikipedia 'Paradise Lost')")
s('K10', b, "[calmly] Yirminci yüzyılda ise Narnia'nın yazarı C. S. Lewis, Kayıp Cennet'e Önsöz adlı kitabında tam tersini savundu.",
  "Lewis, A Preface to Paradise Lost (1942); ekranda künye (H-Hukuk)")
s('K11', b, "[thoughtfully] Lewis'e göre bu, bir yükselişin değil, bir küçülmenin hikâyesiydi: “Kahramandan generale, generalden politikacıya, oradan casusa, yatak odası penceresinden içeri bakan bir şeye, sonra bir kurbağaya ve en sonunda bir yılana.”",
  "Lewis 1942, bölüm 13 (kısa alıntı, çevirimiz; altyazıda tırnak içinde)")
s('K12', b, "[calmly] Şeytan bunu kendisi de söylemişti, yılanın içine girmeden önce: [bitterly] “Kim yükselmeye kalkarsa, yükseldiği kadar alçalmak zorundadır.”",
  "KC IX.169–170 (çevirimiz)")
s('K13', b, "[thoughtfully] Peki ya Milton? Kralların devrilebileceğini savunan bir devrimci, Tanrı'nın tahtına başkaldıran bir meleği yazıyor. Ama o melek cehennemde ne yapıyor? Hürmüz'ün ve Hindistan'ın krallarının hazinelerinden bile görkemli bir taht kuruyor.",
  "Tenure of Kings (1649); KC II.1–6")
s('K14', b, "[calmly] Milton'ın kendi cevabı Abdiel'in ağzındadır: Asıl kölelik, akılsıza hizmet etmektir. Son kitapta da yeryüzünün ilk zorbası için şunu yazar: Tanrı insanı, insanın efendisi yapmadı.",
  "KC VI.178–181; XII.64–71 ('man over men he made not lord')")
s('K15', b, "[calmly] Tarihteki başkaldırıların çoğu, elinden alınan hakları ve özgürlükleri geri istemek içindi. Ama bazıları özgürlük diye yola çıkıp yeni bir taht kurdu. Milton'ın kendi devriminde bile kralı deviren Cromwell, kendisine sunulan tacı reddetti; ama Lord Koruyucu olarak taçsız bir kral gibi yönetti ve yerini oğluna bıraktı.",
  "kullanıcının görüşü (CLAUDE.md); Cromwell: 1657'de tacı reddetti, Lord Protector 1653–1658, halefi Richard Cromwell")
s('K16', b, "[thoughtfully] Kalabalığı peşine takan mı, kalabalığa karşı tek başına duran mı? Abdiel'in sözünü hatırla: “Sen özgür değilsin; kendi kendinin tutsağısın.” Başkaldırı her zaman özgürlük müdür?",
  "C12'nin ödemesi; KC VI.181")

# ───────────────────────── L. Gözyaşı ─────────────────────────
b = 'Bir damla yaş'
s('L01', b, "[curious] Peki ya o gözyaşları?", "bölüm sorusu; E11'in ödemesi")
s('L02', b, "[softly] {1847|Bin sekiz yüz kırk yedi} yılında genç bir Fransız ressam, Alexandre Cabanel, düşmüş bir meleği şöyle resmetti:",
  "Cabanel, L'Ange déchu, 1847; Musée Fabre, Montpellier. Videoda tek renkli kare olabilir (S-Yon)")
s('L03', b, "[softly] Kayalara uzanmış, kollarını yüzünün önünde kavuşturmuş bir melek. Kollarının arasından bize bakıyor. Gözleri öfkeli; ve dolu.",
  "tablonun betimi (Musée Fabre; Wikipedia 'The Fallen Angel')")
s('L04', b, "[calmly] Bu gözyaşının Milton'da bir karşılığı var: Milton da Şeytan'ı yenik ordusunun karşısında ağlatmıştı; ağlamayı gururuna yediremese de, meleklerin ağladığı gibi.",
  "KC I.619–620. Cabanel'in Milton'dan aldığı iddia edilmez (K-Uzman)")
s('L05', b, "[thoughtfully] O gözyaşı pişmanlık mıydı, gurur mu? Milton ikisini aynı yüzde, yan yana yazar. Destanın bir yerinde ağlıyor; başka bir yerinde, “boyun eğmek” sözünü ağzına alamıyor.",
  "KC I.603–605, IV.81–82")
s('L06', b, "[slowly] En başta sorduk: Cehennemden kaçan biri, neden cehennemden bir adım bile uzaklaşamadı?", "A03'ün sorusu")
s('L07', b, "[calmly] Cevabın yarısını Nifates Dağı'nda, kendi ağzından duyduk: [coldly] “Bir yol kaldı: boyun eğmek. Ama o sözü ağzıma almayı, gururum yasaklıyor.” [calmly] Abdiel onu uyarmıştı: Cehennemde krallık değil, zincir bekle. Krallığı buldu. Zincir ise kimsenin vurmadığı, kendi eliyle vurduğu bir zincirdi: gururu.",
  "KC IV.81–82, VI.186")
s('L08', b, "[thoughtfully] Ama destan öbür yarısını da söyler: O kapı ona açık değildi. Şeytan da biliyordu: [quietly] “Bunu beni cezalandıran da biliyor.” [thoughtfully] Peki onu orada tutan gururu muydu, yoksa hiç açılmamış bir kapı mı? Cevap, hangi okumayı seçtiğine bağlı.",
  "KC III.129–132, IV.103 (K-Uzman: iki okuma A03'ün sorusunda çarpışır, karar izleyiciye)")
s('L09', b, "[thoughtfully] Kör şair bu hikâyeyi zifiri karanlıkta yazdırdı. Ama belki de, insanın içinde de bir cehennem taşıyabileceğini en iyi o gördü.",
  "B01'in ödemesi; çerçevenin kapanışı")
s('L10', b, "[curious] Peki sen ne düşünüyorsun? O gözyaşı pişmanlık mıydı, gurur mu? Ve başkaldırı ne zaman özgürlüktür, ne zaman insanın kendi cehennemi? Yorumlarda yaz.",
  "izleyiciye soru")
s('L11', b, "[warmly] Shelley, Şeytan'a benzeyen tek kahramanın Prometheus olduğunu yazar; ama bir farkla: Prometheus'ta hırs, kıskançlık ve intikam yoktu. Ateşi kendisi için değil, insanlar için çalan o asinin hikâyesi ekranda. Bu hikâyeler hoşuna gidiyorsa, Zaman Kuryesi'ne abone olmayı unutma.",
  "Shelley, Prometheus Unbound önsözü (1820; kamu malı) — kaynak denetçisi doğrulayacak; bitiş ekranı: Prometheus videosu + abone")
# ───────────────────────── üretim ─────────────────────────
def alt_of(m):
    m = re.sub(r'\[[^\]]*\]\s*', '', m)
    m = re.sub(r'\{([^|}]*)\|[^}]*\}', r'\1', m)
    return re.sub(r'\s+', ' ', m).strip()

def tts_of(m):
    m = re.sub(r'\{[^|}]*\|([^}]*)\}', r'\1', m)
    m = re.sub(r'…(\s*)(?=[a-zçğıöşü])', r',\1', m); m = m.replace('…', '.')
    for a, o in OKUNUS:
        m = re.sub(r'(?<![\wçğıöşüÇĞİÖŞÜ])' + re.escape(a) + r'(?![a-zçğıöşü])', o, m)
    m = m.replace('[pause]', '.')
    return re.sub(r'\s+', ' ', m).strip()

segs = [{'id': i, 'bolum': bo, 'tts': tts_of(m), 'alt': alt_of(m), 'kaynak': k} for i, bo, m, k in S]
ids = [x['id'] for x in segs]; assert len(ids) == len(set(ids)), 'yinelenen id'
out = {
    'voice': 'Emrullah (voice_id seslendirme öncesi creative_list_voices ile bulunur)',
    'revizyon': 2,
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
