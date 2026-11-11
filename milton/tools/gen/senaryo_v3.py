"""Milton senaryosu, revizyon 3 → senaryo.json
Rev2 gövdesi (senaryo_v2.py) üzerine senaryo kurulu tur 2 kararlarını uygular; bkz. KURUL.md.
İşlemler: DEG (metni değiştir), SIL, EKLE (bir kimlikten sonra), SIRA (bölüm içi yeni sıra)."""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'senaryo_v2.py'), encoding='utf-8').read()
cut = src.index('# ───────────────────────── üretim')
ns = {'__file__': os.path.join(HERE, 'senaryo_v2.py')}
exec(compile(src[:cut], 'senaryo_v2_govde', 'exec'), ns)
S, OKUNUS, ROOT = ns['S'], ns['OKUNUS'], ns['ROOT']

DEG = {
 'A03': ("[curious] Birazdan cehennemden kaçacak. Ama cehennemden bir adım bile uzaklaşamayacak. Onu orada tutan ne?",
         "KC IV.18–23; merak sorusu. İlk cevap G02, asıl cevap L06–L08"),
 'B03': ("[sadly] İki küçük kızına, hiç bilmedikleri dilleri okumayı öğretmişti: İbranice, Yunanca, Latince. Kızlar, göremeyen babalarına, tek kelimesini anlamadıkları metinleri sesli okurdu. Bu saatler, yıllar içinde onlar için dayanılmaz oldu.", None),
 'B04': ("[darkly] Bu adam yalnızca bir şair değil, bir devrimciydi: Kralın idamını savunmuştu. Sonra devrim çöktü, krallık geri döndü. Londra'da cellat onun kitaplarını ateşe atarken, yazarı saklanıyordu. Alevleri göremezdi; sekiz yıldır kördü.",
         "Tenure of Kings, Eikonoklastes (1649); DNB s. 33 (16 Haziran 1660 kararı, cellat eliyle yakma, saklanma); 1652'de tam kör → 1660'ta sekiz yıl; '1660' ekran yazısı"),
 'B05': ("[calmly] Destana devrim henüz ayaktayken başlamıştı. Bu yenilginin içinde bitirdi.",
         "DNB s. 34 (yazım 1658'de başlar; Aubrey'e göre 1663'te biter)"),
 'D02': ("[calmly] Karşısına ilk çıkan, Abdiel olur. Kılıcını indirmeden önce ona şunu söyler: [firmly] “Asıl kölelik budur: akılsıza ya da kendinden üstüne başkaldırana hizmet etmek; seninkilerin şimdi sana ettiği gibi. Sen de özgür değilsin; kendi kendinin tutsağısın.”",
         "KC VI.171–181 (çevirimiz, kısaltılmış)"),
 'D03': ("[firmly] “Sen cehennemde hükümdar ol; bırak ben cennette hizmetkâr kalayım. Ama cehennemde krallık değil, zincir bekle.”",
         "KC VI.183–186 (çevirimiz). E07 (I.263) bu sözü tersine çevirir; ödemesi L07"),
 'D04': ("[calmly] Sonra kılıç iner. Şeytan on adım geriler; onuncu adımda dizinin üstüne çöker.", "KC VI.189–195"),
 'D08': ("[awed] Üçüncü gün, destanda Oğul ışıktan bir savaş arabasıyla gelir. Asiler cennetin kıyısına kadar sürülür ve kendilerini boşluğa atarlar.", None),
 'E04': ("[calmly] Şair bu sözlerin hemen ardından bir not düşer: Şeytan acı içinde böbürleniyordu; içi derin bir umutsuzlukla kıvranırken. [softly] Destan yayımlandığında, bu sözlerin şairi de bir savaşı kaybetmişti.",
         "KC I.125–126; yayım 1667, Restorasyon 1660"),
 'F03': ("[calmly] Şeytan gölgeyle dövüşmeye hazırlanırken kadın araya girer: [bitterly] “Beni unuttun mu? Cennette sen isyanı tasarlarken başının sol yanı yarıldı ve ben oradan doğdum. Sana benziyordum. Bana Günah dediler.”",
         "KC II.746–760 (çevirimiz, kısaltılmış; II.756 'likest to thee'). H11 ile ayna"),
 'G09b': ("[calmly] Cevabı yine kendisi verir: [coldly] “Bir yol kaldı: boyun eğmek. Ama o sözü bana gururum yasaklıyor.”", None),
 'G13': ("[bitterly] “Bunu beni cezalandıran da biliyor. Bu yüzden o barış vermekten ne kadar uzaksa, ben de dilemekten o kadar uzağım.”",
         "KC IV.103–104 (çevirimiz; 'therefore'). 'Bunu' = geri dönse yeniden düşeceğini (IV.93–102). Ödemesi L08"),
 'G16': ("[thoughtfully] Şeytan'ı burada, onu alkışlayan bir kalabalık olmadan görüyoruz. Maskesiz. Ona hak vermek zorunda değiliz. Yine de, belki ilk kez, ona acıyoruz.",
         "empati anı (S-Yon, S-Dram, H-Hassasiyet)"),
 'H10': ("[calmly] Uriel'in haber verdiği bekçi meleklerden biri, mızrağının ucuyla ona dokunur; Şeytan gerçek biçimine döner.",
         "KC IV.555–588 (Uriel'in uyarısı), IV.810–819; G15'in ödemesi"),
 'I04': ("[calmly] Uyuyan bir yılan bulur. İçine girmeden önce bir an durur: [disgusted] “Ne iğrenç bir alçalış! Bir zamanlar en yüce yer için yarışan ben, şimdi bir hayvanın bedenine hapsoluyorum.”",
         "KC IX.159–167 (çevirimiz, kısaltılmış); yılana giriş IX.187–190"),
 'I05': ("[calmly] Ve kendi geleceğini söyler: [bitterly] “Kim yükselmeye kalkarsa, yükseldiği kadar alçalmak zorundadır. İntikam önce tatlıdır; ama çok geçmeden acılaşır ve dönüp sahibini vurur.”",
         "KC IX.169–172 (çevirimiz). K12'de anılır"),
 'I06': ("[softly] Sabah, yılanın içinde, Havva'yı bahçede yalnız görür. Sonra destanın belki de en şaşırtıcı anı gelir: Havva'nın masumiyeti karşısında Şeytan, kendi kötülüğünden kopup dalgın durur. Nefreti, hilesi, kıskançlığı, intikamı; hepsi elinden düşer. Milton'ın deyişiyle, bir süre sersem bir iyilik içinde donakalır.", None),
 'J05': ("[softly] Ama her yandan, sayısız dilden yükselen tek bir ses duyar: kasvetli, ortak bir tıslama.", "KC X.506–509"),
 'J06': ("[calmly] Nifates Dağı'nda, bu kalabalığın önünde rezil olmaktan korktuğu için boyun eğememişti. Şimdi aynı kalabalıktan, alkış yerine tıslama yükseliyor.",
         "G10'un ödemesi; X.545–546 ('the applause they meant')"),
 'J09': ("[gravely] Milton'a göre Şeytan, günahı hangi kılıkta işlediyse cezasını da o kılıkta çeker. Alkışlar tıslamaya, zafer kendi ağızlarından kendi üstlerine yağan bir utanca dönüşür.",
         "KC X.516 (yalnız Şeytan), X.545–547"),
 'J11': ("[thoughtfully] Ve Şeytan destandan sessizce çekilir; son iki kitapta bir daha sahneye çıkmaz. Ama baştaki sorumuz hâlâ ortada: Onu orada tutan neydi? Cevabın bir parçası, destanın son sahnesinde saklı.",
         "KC XI–XII: Şeytan yalnız anılır; kanca (T-Tutma)"),
 'K03': ("[thoughtfully] Peki Şeytan da dileyebilir miydi? Milton'ın destanında bunun cevabı en başta verilir: İnsan aldatıldı; bu yüzden merhamet bulacak. Asi melekler kendi kendilerini ayarttı; onlar bulamayacak.",
         "KC III.129–132 (dolaylı anlatım; Tanrı'ya replik verilmez). Ödemesi L08"),
 'K05': ("[curious] Bu destanın kahramanı kim?", None),
 'K07': ("[thoughtfully] Ama yüz yıldan fazla sonra, şair ve ressam William Blake bambaşka bir şey ileri sürdü: Ona göre Milton, melekleri ve Tanrı'yı anlatırken zincirliydi; şeytanları ve cehennemi anlatırken özgür. Çünkü, der Blake, gerçek bir şairdi ve farkında olmadan Şeytan'ın tarafındaydı.", None),
 'K08': ("[softly] Şurası doğru: bu destandan akılda kalan sözlerin çoğu, Şeytan'ın sözleri.", "H-Hassasiyet (izleyiciye 'sen de' denmez)"),
 'K10': ("[calmly] Yirminci yüzyılda ise Narnia'nın yazarı C. S. Lewis, Kayıp Cennet'e Önsöz adlı kitabında tam tersini savundu.",
         "Lewis, A Preface to Paradise Lost (1942); ekranda özgün başlık ve yıl (H-Hukuk)"),
 'K11': ("[thoughtfully] Lewis'e göre bu, bir yükselişin değil, bir küçülmenin hikâyesiydi: “Kahramandan generale, generalden politikacıya, oradan casusa, yatak odası ya da banyo pencerelerinden içeri bakan bir şeye, sonra bir kurbağaya ve en sonunda bir yılana.”",
         "Lewis 1942, bölüm 13 (kısa alıntı, tam, çevirimiz; altyazıda tırnak içinde)"),
 'K12': ("[calmly] Şeytan da bunu, yılana girmeden önce kendi ağzıyla söylemişti.", "KC IX.169–170 (I05)"),
 'K14': ("[calmly] Milton son kitapta, yeryüzünün ilk zorbasını öğrenen Âdem'e şunu söyletir: Tanrı insanı, insanın efendisi yapmadı.",
         "KC XII.64–71 (konuşan Âdem; zorba adsız kalır)"),
 'K15': ("[calmly] Tarihteki başkaldırıların çoğu, elinden alınan hakları ve özgürlükleri geri istemek içindi. Ama bazıları özgürlük diye yola çıkıp yeni bir taht kurdu.",
         "kullanıcının görüşü (CLAUDE.md)"),
 'K16': ("[thoughtfully] Başta bir soru bırakmıştık: Asıl başkaldıran kim? Kalabalığı peşine takan mı, kalabalığa karşı tek başına duran mı? Abdiel'in cevabı belliydi: “Sen de özgür değilsin; kendi kendinin tutsağısın.” Başkaldırı her zaman özgürlük müdür?",
         "C12'nin ödemesi; KC VI.181"),
 'L05': ("[thoughtfully] O gözyaşı pişmanlık mıydı, gurur mu? Milton ikisini aynı yüzde, yan yana yazar. Destanın bir yerinde ağlıyor; başka bir yerinde, “boyun eğmek” sözünü kendine yasaklıyor.", None),
 'L06': ("[slowly] En başta sorduk: Cehennemden kaçan birini, orada tutan neydi? Bir cevabı duyduk: Cehennemi içinde taşıyordu. Peki içindeki o cehennemden bir çıkış var mıydı?",
         "A03'ün sorusu; G02; asıl soru (S-Yon)"),
 'L07': ("[calmly] Nifates Dağı'nda bir çıkış görmüştü: [coldly] “Bir yol kaldı: boyun eğmek. Ama o sözü bana gururum yasaklıyor.” [calmly] Abdiel onu uyarmıştı: Cehennemde krallık değil, zincir bekle. Krallığı buldu. Zincir ise kimsenin vurmadığı, kendi eliyle vurduğu bir zincirdi: gururu.",
         "KC IV.81–82, VI.186"),
 'L08': ("[thoughtfully] Ama destan öbür yarısını da söyler: Milton'ın destanında o kapı, kendi kendini ayartan asi meleklere açık değildir. Şeytan da bunu biliyordu: [quietly] “O barış vermekten ne kadar uzaksa, ben de dilemekten o kadar uzağım.” [thoughtfully] Onu orada tutan gururu muydu, yoksa Milton'ın ona hiç açmadığı bir kapı mı?",
         "KC III.129–132, IV.104 (iki okuma A03'ün sorusunda çarpışır; karar izleyicide)"),
 'L09': ("[thoughtfully] Kör şair bu hikâyeyi zifiri karanlıkta yazdırdı. Destanın bir yerinde tek bir şey diler: [reverently] “Öyleyse sen, göksel ışık, içime parla. Orada gözler aç ki, ölümlü gözün göremediğini göreyim ve anlatayım.” [thoughtfully] Belki de bu yüzden, insanın içinde de bir cehennem taşıyabileceğini en iyi o gördü.",
         "KC III.51–55 (çevirimiz); B01'in cevabı, çerçevenin kapanışı"),
 'L11': ("[warmly] Şair Shelley'ye göre Prometheus'a benzeyen tek hayalî karakter, Milton'ın Şeytan'ıydı; ama bir farkla: Prometheus hırstan, kıskançlıktan ve intikamdan arınmış olarak anlatılabilirdi. Ateşi kendisi için değil, insanlar için çalan o asinin hikâyesi ekranda. Bu hikâyeler hoşuna gidiyorsa, Zaman Kuryesi'ne abone olmayı unutma.",
         "Shelley, Prometheus Unbound önsözü (1820): 'The only imaginary being resembling in any degree Prometheus, is Satan… exempt from the taints of ambition, envy, revenge' (K-Uzman ve K-Denetim doğruladı); bitiş ekranı: Prometheus videosu + abone"),
}
SIL = {'B07', 'I03'}
EKLE = {  # kimden sonra: [(id, metin, kaynak)]
 'E07': [('E08', "[calmly] Bizim bildiğimiz hâliyle: cennette köle olacağıma, cehennemde kral olurum.", "I.263'ün yaygın Türkçe söylenişi (kullanıcının ifadesi)")],
 'K15': [('K15b', "[calmly] Milton'ın kendi devriminde de öyle oldu: Kralı deviren Cromwell kendisine sunulan tacı reddetti, ama ülkeyi taçsız bir kral gibi yönetti ve yerini oğluna bıraktı.",
          "Cromwell 1657'de tacı reddetti; Lord Protector 1653–1658; halefi oğlu Richard")],
 'L08': [('L08b', "[softly] Belki herkesin, söylemeyi kendine yasakladığı bir söz vardır.", "iksirin izleyiciye taşınması (S-Yon, S-Dram)")],
}

# ── tur 2: dil (A-Dil), ses (A-Ses) ve tempo kararları ──
DEG.update({
 'A01': ("[slowly] [softly] “Hangi yana kaçsam cehennem. Ben cehennemim.”", None),
 'A05': ("[thoughtfully] Bu hikâye bir şiirden: John Milton'ın destanından, Kayıp Cennet'ten. Buradaki Şeytan, bir şairin kaleminden çıkmış bir karakter; biz de bu hikâyeyi bir din anlatısı olarak değil, bir edebiyat eseri olarak okuyacağız.", None),
 'B02': ("[softly] Londra'da bir ev; gece. Bir adam uyuyamıyor; zihninde dizeler kuruyor. Anlatılanlara göre böyle gecelerde bazen kızını uyandırır, dizeleri ona yazdırırdı. Çoğu zaman da evde o sırada kim varsa, ona. Kırk dizeyi bir solukta söyler, sonra yirmiye indirirdi.", None),
 'B08': ("[thoughtfully] Işığını kaybetmiş bir şair, ışığını kaybetmiş bir meleği anlatacaktı.", "anlatıcının köprüsü; yenilgi koşutluğu E04'te"),
 'C03': ("[calmly] Milton onun cennetteki adını vermez: [gravely] “Eski adı artık cennette anılmıyor; ona bundan böyle Şeytan deyin.” [calmly] Yalnızca birkaç yerde, çekinerek, ona Lucifer adını yakıştırır: ışık taşıyan.",
         "KC V.658–659; Lucifer: V.760, VII.131–133, X.425 ('so call him')"),
 'C05': ("[darkly] O gece yarısı başmelek, yardımcısını gizlice uyandırır. Ordularına bir yalan söyletir: Kuzeydeki saraya, yeni kralı karşılamaya hazırlanmak için gidecekler.", None),
 'C09': ("[thoughtfully] Peki neden başkaldırdı? Ona sorsan: özgürlük için. Milton'a sorsan, iki kelime: kıskançlık ve gurur. Kendini küçük düşürülmüş saymıştı. Bu iki cevap, hikâyenin sonuna kadar yan yana yürüyecek.", None),
 'C11': ("[calmly] Abdiel ona karşı çıkar; sonra küçümseyen bakışların arasından, tek başına yürüyüp gider. Milton onu şöyle anlatır: binlerce hainin arasında sadık kalan tek kişi.", None),
 'E04': ("[calmly] Şair bu sözlerin hemen ardından bir not düşer: Şeytan acı içinde, yüksek sesle {böbürleniyordu; ama|böbürleniyordu. Ama} içi derin bir umutsuzlukla kıvranıyordu. [softly] Destan yayımlandığında, bu sözlerin şairi de bir savaşı kaybetmişti.",
         "KC I.125–126; yayım 1667, Restorasyon 1660"),
 'E05': ("[calmly] Sonra gölden kalkar. Milton'a göre bunu ancak göklerin izniyle yapabilir.", None),
 'E09': ("[in awe] Kalkanı omzunda ay gibi asılıdır. Mızrağı öyle büyüktür ki, en büyük geminin direği yanında değnek gibi kalır; o mızrağa yaslanarak yanan topraklarda yürür.", None),
 'E11': ("[softly] Ordusuna bakar: onun suçu yüzünden cennetten atılmış milyonlarca ruh. Yıldırım çarpmış bir ormanın ağaçları gibi yanık, ama hâlâ ayaktalar. Konuşmaya hazırlanır; boğazı düğümlenir. Üç kez dener; üç kez, ağlamayı gururuna yediremese de, gözlerinden yaşlar boşanır: meleklerin ağladığı gibi.", None),
 'E13': ("[darkly] Mecliste kimi yeni bir savaş ister, kimi sessizce katlanmayı. Sonunda Şeytan'ın planı kabul edilir: Tanrı'nın yeni yarattığı dünyaya, insana saldırmak.", None),
 'F02': ("[calmly] Dokuz katmanlı kapıda iki bekçi vardır: yarısı kadın, yarısı yılan bir {varlık; ve|varlık. Ve} biçimi olmayan bir gölge.", None),
 'F08': ("[calmly] Güneşe varır; genç bir melek kılığında, güneşin bekçisi Uriel'e yolu sorar. Uriel yolu gösterir.", "KC III.634–735"),
 'F09': ("[calmly] Şeytan aşağı süzülür ve bir dağın, Nifates'in tepesine konar.", "KC III.736–742"),
 'G07': ("[anguished] “Vay hâlime! Sonsuz gazaptan, sonsuz umutsuzluktan nereye kaçayım? [slowly] [softly] Hangi yana kaçsam cehennem. Ben cehennemim.”", None),
 'G13': ("[bitterly] “Beni cezalandıran da bunu biliyor. Bu yüzden, barışı bağışlamaktan o ne kadar uzaksa, dilemekten ben o kadar uzağım.”",
         "KC IV.103–104 (çevirimiz; 'therefore'). 'Bunu' = geri dönse yeniden düşeceğini (IV.93–102). Ödemesi L08"),
 'H05': ("[wistfully] “Onları hayranlıkla seyrediyorum. Onları sevebilirim bile. Bu savunmasız hâllerine acıyabilirim; bana acıyan olmasa da.”", None),
 'H06': ("[wistfully] “Masumiyetiniz karşısında yüreğim yumuşuyor.” [calmly] Ama hemen ekler: krallığının çıkarı, onuru ve intikamı onu buna mecbur bırakıyor.", None),
 'H11': ("[scornfully] “Beni tanımıyor musunuz?” [calmly] diye sorar, küçümseyerek. Meleklerden biri aynı küçümsemeyle karşılık verir: [firmly] “Parlaklığının hâlâ aynı olduğunu sanma. İyi olmaktan çıktığın gün, o ışık seni terk etti. Şimdi günahına benziyorsun.”",
         "KC IV.827–840 (çevirimiz, kısaltılmış; 'filled with scorn', karşılık veren Zephon); F03 ile ayna"),
 'I01': ("[darkly] İntikam, tatlı mıdır?", None),
 'I02': ("[calmly] Şeytan bahçeden kovulur. Yedi gece, karanlıkla birlikte dünyanın çevresinde döner; sekizinci gece, gizlice geri sızar.", None),
 'I06': ("[softly] Sabah, yılanın içinde, Havva'yı bahçede yalnız görür. Sonra destanın belki de en şaşırtıcı anı gelir: Havva'nın masumiyeti karşısında Şeytan, kendi kötülüğünden kopup dalgın durur. Nefreti, hilesi, kıskançlığı, {intikamı; hepsi|intikamı: hepsi} elinden düşer. Milton'ın deyişiyle, bir süre sersem bir iyilik içinde donakalır.", None),
 'J02': ("[calmly] Şeytan cehenneme döner. Sıradan bir asker kılığında saraya girer, tahtına çıkar ve birden eski parlaklığıyla belirir; Milton'ın deyişiyle, sahte bir parıltıyla. Cehennem onu sevinç haykırışlarıyla karşılar.", None),
 'J03': ("[triumphantly] “İnsanı yaratıcısından kopardım. Hem de bir elmayla! Gülmeye değmez mi?”", None),
 'J06': ("[thoughtfully] Nifates Dağı'nda, bu kalabalığın önünde rezil olmaktan korktuğu için boyun eğememişti. Şimdi aynı kalabalıktan, alkış yerine tıslama yükseliyor.",
         "G10'un ödemesi; X.545–546 ('the applause they meant')"),
 'K07': ("[calmly] Ama yüz yıldan fazla sonra, şair ve ressam William Blake bambaşka bir şey ileri sürdü: [passionately] Ona göre Milton, melekleri ve Tanrı'yı anlatırken zincirliydi; şeytanları ve cehennemi anlatırken özgür. Çünkü, der Blake, gerçek bir şairdi ve farkında olmadan Şeytan'ın tarafındaydı.", None),
 'K11': ("[calmly] Lewis'e göre bu, bir yükselişin değil, bir küçülmenin hikâyesiydi: [wryly] “Kahramandan generale. Generalden politikacıya. Oradan casusa; yatak odası ya da banyo pencerelerinden içeri bakan bir şeye. Sonra bir kurbağaya. Ve en sonunda, bir yılana.”",
         "Lewis 1942, bölüm 13 (kısa alıntı, tam, çevirimiz; altyazıda tırnak içinde)"),
 'K13': ("[thoughtfully] Peki ya Milton? Kralların devrilebileceğini savunan bir devrimci, Tanrı'nın tahtına başkaldıran bir meleği yazıyor. Ama o melek cehennemde ne yapıyor? Kendine, Hürmüz'ün ve Hindistan'ın hazinelerinden görkemli bir taht kuruyor.", None),
 'K16': ("[thoughtfully] Başta bir soru bırakmıştık: Asıl başkaldıran kim? Kalabalığı peşine takan mı, kalabalığa karşı tek başına duran mı? Abdiel'in cevabı belliydi: [firmly] “Sen de özgür değilsin; kendi kendinin tutsağısın.” [thoughtfully] Başkaldırı her zaman özgürlük müdür?",
         "C12'nin ödemesi; KC VI.181"),
 'L03': ("[softly] Kayalara uzanmış, kollarını yüzünün önünde kavuşturmuş bir melek. Kollarının arasından bize bakıyor. Gözleri {öfkeli; ve|öfkeli. Ve} dolu.", None),
 'L04': ("[calmly] Bu gözyaşının destanda bir karşılığı var: Milton'ın Şeytan'ı da yenik ordusunun karşısında ağlar; ağlamayı gururuna yediremese de, meleklerin ağladığı gibi.",
         "KC I.619–620. Cabanel'in Milton'dan aldığı iddia edilmez (K-Uzman)"),
 'L05': ("[thoughtfully] O gözyaşı pişmanlık mıydı, gurur mu? Milton ikisini aynı yüzde, yan yana yazar. Şeytan destanın bir yerinde ağlıyor; başka bir yerinde, “boyun eğmek” sözünü kendine yasaklıyor.", None),
 'L07': ("[calmly] Nifates Dağı'nda bir çıkış görmüştü: [coldly] “Bir yol kaldı: boyun eğmek. Ama o sözü bana gururum yasaklıyor.” [calmly] Abdiel onu uyarmıştı: [firmly] “Cehennemde krallık değil, zincir bekle.” [calmly] Krallığı buldu; zinciri de. Ama o zinciri ona kimse vurmadı. Kendi eliyle vurdu: gururu.",
         "KC IV.81–82, VI.186"),
 'L08': ("[thoughtfully] Ama destan öbür yarısını da söyler: Milton'ın destanında bağışlanma yolu, kendi kendini ayartan asi meleklere açık değildir. Şeytan bunu da biliyordu: [bitterly] “Barışı bağışlamaktan o ne kadar uzaksa, dilemekten ben o kadar uzağım.” [thoughtfully] Onu orada tutan gururu muydu, yoksa Milton'ın ona hiç açmadığı bir kapı mı?",
         "KC III.129–132, IV.104 (iki okuma A03'ün sorusunda çarpışır; karar izleyicide)"),
 'L11': ("[warmly] Şair Shelley'ye göre Prometheus'a benzeyen tek hayalî karakter, Milton'ın Şeytan'ıydı; ama Prometheus hırstan, kıskançlıktan ve intikamdan arınmış olarak anlatılabilirdi. Ateşi insanlar için çalan o asinin hikâyesi ekranda. Bu hikâyeler hoşuna gidiyorsa, Zaman Kuryesi'ne abone olmayı unutma.",
         "Shelley, Prometheus Unbound önsözü (1820): 'The only imaginary being resembling in any degree Prometheus, is Satan… exempt from the taints of ambition, envy, revenge' (K-Uzman ve K-Denetim doğruladı); bitiş ekranı: Prometheus videosu + abone"),
})

# ── tur 3 sonrası rötuşlar (üyelerin "düşük/orta" önerileri; onaydan sonra, yapı değişmez) ──
DEG.update({
 'B05': ("[calmly] Destanına, devrim henüz ayaktayken başlamıştı. Bu yenilginin içinde bitirdi.", None),
 'D08': ("[awed] Destanda üçüncü gün, Oğul ışıktan bir savaş arabasıyla gelir. Asiler cennetin kıyısına kadar sürülür ve kendilerini boşluğa atarlar.", None),
 'E12': ("[awed] Şeytanlar cehennemin toprağından altın kazar. Bir saat içinde, yerden devasa bir saray yükselir: Pandemonium, bütün şeytanların meclisi.", None),
 'E09': ("[awed] Kalkanı omzunda ay gibi asılıdır. Mızrağı öyle büyüktür ki, en büyük geminin direği yanında değnek gibi kalır; o mızrağa yaslanarak yanan topraklarda yürür.", None),
 'I04': ("[calmly] Saklanmak için uyuyan bir yılan arar; ararken kendinden iğrenir: [disgusted] “Ne iğrenç bir alçalış! Bir zamanlar en yüce yer için yarışan ben, şimdi bir hayvanın bedenine hapsoluyorum.”",
         "KC IX.159–167 (çevirimiz, kısaltılmış; sözler yılanı ararken söylenir)"),
 'I05': ("[calmly] Ve kendi geleceğini söyler: [bitterly] “Kim yükselmeye kalkarsa, yükseldiği kadar alçalmak zorundadır. İntikam önce tatlıdır; ama çok geçmeden acılaşır ve dönüp sahibini vurur.” [calmly] Sonra yılanı bulur ve ağzından içine girer.",
         "KC IX.169–172 (çevirimiz); yılana giriş IX.182–190. K12'de anılır"),
 'J02': ("[calmly] Şeytan cehenneme döner. Sıradan bir asker kılığında saraya girer, tahtına çıkar ve birden belirir: düşüşten ona kalan ışıkla ya da, Milton'ın deyişiyle, sahte bir parıltıyla. Cehennem onu sevinç haykırışlarıyla karşılar.", None),
 'J09': ("[gravely] Milton'a göre Şeytan, günahı hangi kılıkta işlediyse cezasını da o kılıkta çeker. Zafer, kendi ağızlarından kendi üstlerine yağan bir utanca dönüşür.", None),
 'K03': ("[thoughtfully] Peki Şeytan da dileyebilir miydi? Milton'ın destanında bunun cevabı daha üçüncü kitapta verilir: İnsan aldatıldı; bu yüzden merhamet bulacak. Asi melekler kendi kendilerini ayarttı; onlar bulamayacak.", None),
 'K07': ("[calmly] Ama yüz yıldan fazla sonra, şair ve ressam William Blake bambaşka bir şey ileri sürdü: [passionately] Ona göre Milton, melekleri ve Tanrı'yı anlatırken zincirliydi; şeytanları ve cehennemi anlatırken özgür. Blake'in gerekçesi şuydu: Milton gerçek bir şairdi ve farkında olmadan Şeytan'ın tarafındaydı.", None),
 'K11': ("[calmly] Lewis'e göre bu, bir yükselişin değil, bir küçülmenin hikâyesiydi: [wryly] “Kahramandan generale. Generalden politikacıya. Oradan casusa. Yatak odası ya da banyo pencerelerinden içeri bakan bir şeye. Sonra bir kurbağaya. Ve en sonunda, bir yılana.”", None),
 'K12': ("[calmly] Şeytan da bunu, yılana girmeden önce kendi ağzıyla söylemişti: yükselmeye kalkan, yükseldiği kadar alçalır.", "KC IX.169–170 (I05)"),
 'K14': ("[calmly] Milton son kitapta Âdem'e şunu söyletir: Tanrı insanı, insanın efendisi yapmadı.", "KC XII.64–71 (konuşan Âdem)"),
 'L07': ("[calmly] Nifates Dağı'nda bir çıkış görmüştü: [coldly] “Bir yol kaldı: boyun eğmek. Ama o sözü bana gururum yasaklıyor.” [calmly] Abdiel onu uyarmıştı: [firmly] “Cehennemde krallık değil, zincir bekle.” [calmly] Krallığı buldu; zinciri de. Gölün zincirleri çözülmüştü; bu zinciri ise ona kimse vurmadı. Kendi eliyle vurdu: gururu.",
         "KC IV.81–82, VI.186; gölün zincirleri I.48, I.210"),
 'L08': ("[thoughtfully] Ama destan bir şey daha söyler: bağışlanma yolu, kendi kendini ayartan asi meleklere açık değildir. Şeytan bunu da biliyordu: [bitterly] “Barışı bağışlamaktan o ne kadar uzaksa, dilemekten ben o kadar uzağım.” [thoughtfully] Onu orada tutan gururu muydu, yoksa Milton'ın ona hiç açmadığı bir kapı mı?",
         "KC III.129–132, IV.104 (iki okuma A03'ün sorusunda çarpışır; karar izleyicide)"),
 'L09': ("[thoughtfully] Kör şair bu hikâyeyi zifiri karanlıkta yazdırdı. Destanın bir yerinde tek bir şey diler: [reverently] “Sen, göksel ışık, içime parla. Orada gözler aç ki, ölümlü gözün göremediğini göreyim ve anlatayım.” [thoughtfully] Belki de bu yüzden, insanın kendi içinde bir cehennem taşıyabileceğini en iyi o gördü.",
         "KC III.51–55 (çevirimiz); B01'in cevabı, çerçevenin kapanışı"),
 'L11': ("[warmly] Ateşi insanlar için çalan bir başka asinin, Prometheus'un hikâyesi ekranda. Romantik şair Shelley'ye göre Prometheus'a benzeyen tek hayalî karakter, Milton'ın Şeytan'ıydı; ama Prometheus hırstan, kıskançlıktan ve intikamdan arınmış olarak anlatılabilirdi. Bu hikâyeler hoşuna gidiyorsa, Zaman Kuryesi'ne abone olmayı unutma.",
         "Shelley, Prometheus Unbound önsözü (1820): 'The only imaginary being resembling in any degree Prometheus, is Satan… exempt from the taints of ambition, envy, revenge' (K-Uzman ve K-Denetim doğruladı); bitiş ekranı: Prometheus videosu + abone"),
})
# ── ABT taraması (kurul/senaryo_tur3/ABT-tarama.md): "ve sonra" kuyruklarını kıran köprüler; başkan 8/10 maddeyi aldı ──
DEG.update({
 'B04': ("[darkly] Bu adam yalnızca bir şair değil, bir devrimciydi: Kralın idamını savunmuştu. Devrim çöküp krallık geri dönünce, Londra'da cellat onun kitaplarını ateşe atarken yazarı saklanıyordu. Alevleri göremezdi; sekiz yıldır kördü.", None),
 'D08': ("[awed] Kimse üstün gelemez. Destanda üçüncü gün, Oğul ışıktan bir savaş arabasıyla gelir. Asiler cennetin kıyısına kadar sürülür ve kendilerini boşluğa atarlar.",
         "KC VI.693–694 (savaş sonuçsuz), VI.699, VI.748–866"),
 'E09': ("[awed] Kalkanı omzunda ay gibi asılıdır. Mızrağı öyle büyüktür ki, en büyük geminin direği yanında değnek gibi kalır.", None),
 'E12': ("[awed] Sonunda konuşur; ordu işe koyulur. Şeytanlar cehennemin toprağından altın kazar. Bir saat içinde, yerden devasa bir saray yükselir: Pandemonium, bütün şeytanların meclisi.",
         "KC I.663 ('He spake'), I.670–730 (I.697 'in an hour'), I.756; görsel: Dor sütunlu, altın tavanlı tapınak (I.713–717)"),
 'F05': ("[darkly] Günah kapıyı açar. Şeytan'ın önünde ne başı ne sonu olan bir okyanus vardır: Kaos.", "KC II.871–884 (kapıyı Günah açar), II.890–916"),
 'J10': ("[darkly] Ceza bitmez: önlerinde meyveyle dolu ağaçlar belirir. Açlıkla saldırırlar; meyveler ağızlarında acı küle döner.", None),
 'K13': ("[thoughtfully] Blake mi haklı, Lewis mi? Peki ya Milton? Kralların devrilebileceğini savunan bir devrimci, Tanrı'nın tahtına başkaldıran bir meleği yazıyor. Ama o melek cehennemde ne yapıyor? Kendine, Hürmüz'ün ve Hindistan'ın hazinelerinden görkemli bir taht kuruyor.", None),
 'K14': ("[calmly] Üstelik Milton son kitapta Âdem'e şunu söyletir: Tanrı insanı, insanın efendisi yapmadı.", "KC XII.64–71 (konuşan Âdem)"),
})
SIL |= {'K09'}
# ilk etiketi değiştir ([calmly] dozu; A-Ses)
ETIKET = {'D07': 'tense', 'E10': 'gravely', 'E12': 'awed', 'F05': 'darkly', 'F06': 'tense', 'H02': 'wryly', 'H03': 'darkly',
          'I08': 'gravely', 'I10': 'quietly', 'J08': 'tense', 'J10': 'darkly', 'J07': 'tense', 'G08': 'trembling voice'}
# seslendirme parçaları: uzun bölümler bu kimliklerde yeni çekime bölünür (bolum alanı değişmez)
PARCA = {'B06', 'C06', 'D05', 'E06', 'E12', 'F05', 'G07', 'G11', 'H07', 'I06', 'J05', 'K10', 'K13', 'L06', 'L09'}
SIRA = {'Alkış': ['J01', 'J02', 'J03', 'J04', 'J05', 'J07', 'J08', 'J06', 'J09', 'J10', 'J11']}
BOLUM = {'Cehennem benim': 'Ben cehennemim'}

T = []
for i, bo, m, k in S:
    if i in SIL: continue
    if i in DEG: m, k = DEG[i][0], (DEG[i][1] if DEG[i][1] is not None else k)
    if i in ETIKET: m = re.sub(r'^\[[^\]]*\]', '[' + ETIKET[i] + ']', m)
    bo = BOLUM.get(bo, bo)
    T.append((i, bo, m, k))
    for j, m2, k2 in EKLE.get(i, []): T.append((j, bo, m2, k2))
assert not (set(DEG) | SIL | set(EKLE)) - {i for i, *_ in S}, (set(DEG) | SIL | set(EKLE)) - {i for i, *_ in S}
for bo, order in SIRA.items():
    idx = [n for n, x in enumerate(T) if x[1] == bo]; by = {T[n][0]: T[n] for n in idx}
    assert set(order) == set(by), (set(order) ^ set(by))
    for n, i in zip(idx, order): T[n] = by[i]
# bayat çapraz göndermeleri düzelt
FIX = [('cevabı C06', 'cevabı C09'), ('ödemesi D04', 'ödemesi D05'), ('uyarısı D04', 'uyarısı D03'), ('L09–L09c', 'L06–L08'), ('L09b', 'L07'), ('L09c', 'L08'), ('ödemesi L05', 'ödemesi L04'), ('ödemesi K12', 'ödemesi K16'), ('ödemesi L10', 'ödemesi L09')]
S = []
for i, bo, m, k in T:
    for a, b in FIX: k = k.replace(a, b)
    S.append((i, bo, m, k))

def alt_of(m):
    m = re.sub(r'\[[^\]]*\]\s*', '', m)
    m = re.sub(r'\{([^|}]*)\|[^}]*\}', r'\1', m)
    return re.sub(r'\s+', ' ', m).strip()

def tts_of(m):
    m = re.sub(r'\{[^|}]*\|([^}]*)\}', r'\1', m)
    m = re.sub(r'…(\s*)(?=[a-zçğıöşü])', r',\1', m); m = m.replace('…', '.')
    for a, o in OKUNUS:
        m = re.sub(r'(?<![\wçğıöşüÇĞİÖŞÜ])' + re.escape(a) + r'(?![a-zçğıöşü])', o, m)
    m = m.replace("Milton'ın", "Milton'un")  # ünlü uyumu: ad 'o' ile okunur (A-Dil); altyazıda 'Milton'ın' kalır
    return re.sub(r'\s+', ' ', m).strip()

segs = [dict({'id': i, 'bolum': bo, 'tts': tts_of(m), 'alt': alt_of(m), 'kaynak': k}, **({'vo_parca': 1} if i in PARCA else {})) for i, bo, m, k in S]
ids = [x['id'] for x in segs]; assert len(ids) == len(set(ids)), 'yinelenen id'
for x in segs: assert x['tts'].startswith('['), ('etiketsiz segment', x['id'])
out = {
    'voice': 'Emrullah (voice_id seslendirme öncesi creative_list_voices ile bulunur)',
    'revizyon': 3,
    'not': "tts: seslendirme metni (ses etiketleri, özel adlar okunuşa göre, sayılar yazıyla). alt: altyazı metni. kaynak: iddianın dayanağı. KC = Kayıp Cennet, 1674 baskısı, kitap.dize (kaynak/kayip_cennet_1674_dizeler.json). Bütün dize çevirileri bizim (özgün metin kamu malı). DNB = Dictionary of National Biography, cilt 38 (1894), 'Milton, John'.",
    'segments': segs,
}
json.dump(out, open(os.path.join(ROOT, 'senaryo.json'), 'w'), ensure_ascii=False, indent=1)
ch = sum(len(x['alt']) for x in segs); kel = sum(len(x['alt'].split()) for x in segs)
print(len(segs), 'cümle;', ch, 'karakter;', kel, 'kelime; tahmini süre', round(ch / 13.0 / 60, 1), 'dk (13 kr/sn)')
c = {}
for x in segs: c[x['bolum']] = c.get(x['bolum'], 0) + len(x['alt'])
for k, v in c.items(): print(f'  {k:28s} {v:5d} kr  ~{v/13/60:4.1f} dk')
