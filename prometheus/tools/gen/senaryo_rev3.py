# Senaryo rev 3: 12 üyeli kurulun (2 tur) ve tek üyeli ilk kurulun önerileri tartılarak yazıldı. Kararlar: kurul/kararlar.md
import json, re, sys, collections
TTS2ALT = [('Prometeus', 'Prometheus'), ('Ayshilos', 'Aiskhylos'), ('Teogonia', 'Theogonia'), ('Gaya', 'Gaia'), ('Kaos', 'Khaos'),
           ('Rea', 'Rheia'), ('Hefaistos', 'Hephaistos'), ('Epimeteus', 'Epimetheus'), ('Otris', 'Othrys'), ('Olimpos', 'Olympos'),
           ('Tetis', 'Thetis'), ('Temis', 'Themis'), ('Göte', 'Goethe'), ('Meri Şeli', 'Mary Shelley'), ('Frankenştayn', 'Frankenstein'),
           ('Openhaymır', 'Oppenheimer'), ('İyo', 'İo'), ('Mekoni', 'Mekone'), ('Afrodit', 'Aphrodite'),
           ('bin dokuz yüz altmış yedide', "1967'de"), ('milattan önce beşinci yüzyılda', 'MÖ V. yüzyılda'), ('yirminci yüzyılın', 'XX. yüzyılın')]
def mkalt(t):
    a = re.sub(r'\[[^\]]*\]\s*', '', t)
    for x, y in TTS2ALT: a = a.replace(x, y)
    return a
S = []
def seg(i, b, tts, kaynak, alt=None): S.append({'id': i, 'bolum': b, 'tts': tts, 'alt': alt or mkalt(tts), 'kaynak': kaynak})

B = 'Açılış'
seg('A01', B, "[slowly] [deep voice] Tanrılardan ateşi, bile bile çalıp insanlara veren bir Titan düşün.", "Th. 565–569; ZVP 266 (bile bile); Erhat xi5")
seg('A02', B, "[mysterious] Şimdi de, onu dünyanın ucundaki bir kayaya zincirleyen tanrının… asıl tutsak olduğunu.", "Erhat xiv2, xiv5 (cevabı J04–J06)")
seg('A03', B, "[darkly] Her gün bir kartal iner, karaciğerini parçalar. Gece karaciğer yeniden büyür… [slowly] ve sabah, kartal yine gelir.", "Th. 523–525 (ödemesi I08b, L02)")
seg('A04', B, "[mysterious] Adı… Prometeus.", "")
seg('A06', B, "[thoughtfully] Bu tuhaf fikri, Azra Erhat yazar: efsaneyi anlatan antik bir oyunu Türkçeye çevirenlerden biri. Bin dokuz yüz altmış yedide yazdığı önsözde, bu eski hikâyeyi bambaşka bir gözle okur.", "Erhat xvi2, xv4")
seg('A05', B, "[curious] Peki bu nasıl olabilir? Ve Zeus'u bu kadar öfkelendiren, gerçekten bir avuç ateş miydi?", "sorular; cevapları E15–E16b ve J04–J06")

B = "Erhat'ın sorusu"
seg('B01', B, "[thoughtfully] Sahnede neredeyse yalnızca tanrıların konuştuğu bir oyun, insanı anlatabilir mi?", "Erhat v4 ('tanrıların ve tanrısal kişilerin'), xi2")
seg('B02', B, "Atinalı tragedya yazarı Ayshilos'un adıyla, bize tek bir Prometeus oyunu ulaştı: Zincire Vurulmuş Prometeus. Eski bir listenin saydığı öbür iki oyun ise kayıp.", "Erhat v2 (adları L02'de)")
seg('B04', B, "[warmly] Oyunu Sabahattin Eyüboğlu'yla birlikte çeviren Azra Erhat'a göre, anlatabilir: Oynanan dram, insanlığın dramıdır.", "Erhat v4, xv4")
seg('B05', B, "Onun deyişiyle insan dostu, tanrı düşmanı Prometeus, en çok da yirminci yüzyılda, insanı özüyle temsil eden bir kahraman olarak benimsenmiştir.", "Erhat v5 (kısa alıntı)",
    "Onun deyişiyle “insan dostu, tanrı düşmanı” Prometheus, en çok da XX. yüzyılda, insanı özüyle temsil eden bir kahraman olarak benimsenmiştir.")
seg('B06', B, "[intrigued] Ve Erhat can alıcı bir soru sorar: Nasıl oldu da, milattan önce beşinci yüzyılda yaşamış bir yazar, yirminci yüzyılın başkaldıran insanını yaratabildi?", "Erhat vi7 (cevabı K08a–K08b)")
seg('B07', B, "Cevabı ararken, önce çok daha geriye gider: tanrıların taht kavgasına.", "Erhat vi6, vi9")

B = 'Tanrıların taht kavgası'
seg('C01', B, "[wryly] Tanrıların kralı Zeus, o tahta nasıl oturmuştu? [softly] Kayadaki Titan, hepsini görmüştü.", "ZVP 956–959 (iki tiranın düşüşünü gördüm; ödemesi I06)")
seg('C02', B, "Erhat'a göre hem efsanenin, hem de oyunun merkezinde, bugün “hükümet darbesi” diyebileceğimiz bir olay vardır: Bir kuşak, kendinden öncekini devirir ve yönetim gücünü ele geçirir.", "Erhat vi9 (kısa alıntı)",
    "Erhat'a göre hem efsanenin hem de oyunun merkezinde, bugün “hükümet darbesi” diyebileceğimiz bir olay vardır: Bir kuşak, kendinden öncekini devirir ve yönetim gücünü ele geçirir.")
seg('C04', B, "Ayshilos'tan bir iki yüzyıl önce yaşamış Hesiodos'un Teogonia'sına göre, başlangıçta Kaos vardı. Sonra Toprak Ana, Gaya geldi ve kendine denk bir eş doğurdu: Gök, yani Uranos. [darkly] Ama Uranos, Gaya'dan doğan devlerden tiksindi; her birini doğar doğmaz, annelerinin karnına geri tıktı.", "Erhat vii1, vii3; Th. 116–160 (Gaia Khaos'tan 'sonra' gelir)")
seg('C06', B, "Acılar içindeki Gaya, çelikten bir tırpan yapıp çocuklarına verdi. Hiçbiri babasına el kaldırmaya yanaşmadı… [slowly] en küçükleri Kronos hariç.", "Erhat vii4; Th. 160–172")
seg('C07', B, "[tense] Kronos gece pusuya yattı. Uranos Gaya'nın üstüne eğildiği anda, oğlu tırpanı savurdu… ve babasını iğdiş etti.", "Erhat vii4; Th. 174–182")
seg('C08', B, "[wryly] Hesiodos burada, deniz köpüğünden doğan Afrodit'e dalıp gider. Erhat ise başka bir şey görür: tanrıların tarihinde bir devrim.", "Erhat vii5")
seg('C09', B, "[darkly] Ama bu devrim de, kendi çocuklarını yedi. Hem de kelimenin tam anlamıyla: Kronos, oğullarından birinin onu devireceğini biliyordu; çocuklarını doğar doğmaz yuttu.", "Erhat vii6, viii1; Th. 459–467")
seg('C10', B, "Karısı Rea, son oğlunu Girit'e kaçırdı ve Kronos'a kundağa sarılı bir taş yutturdu. [slowly] O çocuk Zeus'tu. Büyüyünce babasına kardeşlerini kusturdu ve onu tahttan indirdi.", "Erhat viii1; Th. 468–500")
seg('C12', B, "[thoughtfully] Erhat'a göre bu iki devrim aynı şey değildir. Birincisi, kaba kuvvetin kendi kendini yenmesiydi. İkincisi, kaba kuvvetin akılla yenilmesi: Bu kez Zeus'a, kaba kuvvetten ders almış Uranos ile Gaya yol göstermişti.", "Erhat viii2–viii4 (kısa alıntı)",
    "Erhat'a göre bu iki devrim aynı şey değildir. Birincisi, kaba kuvvetin kendi kendini yenmesiydi. İkincisi, “kaba kuvvetin akılla yenilmesi”: Bu kez Zeus'a, kaba kuvvetten ders almış Uranos ile Gaia yol göstermişti.")
seg('C14', B, "[knowingly] Ve Erhat bir ayrıntıyı hatırlatır: Prometeus da bu devrimde rol oynamıştı. Hangi rolü mü? Onu, zincirdeyken kendi ağzından duyacağız.", "Erhat viii1 (ödemesi G05)")
seg('C15', B, "Ardından Titanlarla on yıl süren bir savaş geldi. Zeus, Gaya'nın öğüdüyle, yerin altındaki yüz kollu devleri savaşa sürdü. [intense] Yer sarsıldı, denizler altüst oldu… ve Titanlar Tartaros'a kapatıldı.", "Erhat viii6, ix1; Th. 617–735")
seg('C17', B, "[thoughtfully] Ona göre Zeus, kaba kuvveti kendi hesabına çalıştırmıştı. Sonunda kaba güçler birbirini yok etti; dünyanın egemenliği yalnızca aklın gücüne dayandı. Yıldırım elinde, Zeus tahta oturdu ve dünyayı paylaştırmaya girişti.", "Erhat viii5, ix2; Th. 504–506, 881–885")
seg('C18', B, "[ominous] [slowly] Ve bu paylaşmada önüne tek bir engel çıktı… Prometeus.", "Erhat ix2")

B = "Zeus'un dinmez öfkesi"
seg('D01', B, "[darkly] Zeus, bir Titan ailesine neden özel bir kin besliyordu?", "Erhat ix5")
seg('D02', B, "Prometeus, Titan İapetos'un oğluydu. Dört kardeştiler: Atlas, Menoitios, Prometeus ve Epimeteus.", "Erhat ix4; Th. 507–511")
seg('D03', B, "Dördünün de sonu tüyler ürperticiydi. Zeus, Atlas'ı dünyanın ucuna dikip göğü omuzlarına yükledi; Menoitios'u yıldırımla çarpıp yerin dibine gömdü.", "Erhat ix4; Th. 514–520")
seg('D04', B, "Prometeus'u bir sütuna zincirleyip karaciğerini kartala yedirdi. Epimeteus'a ise bir “armağan” gönderdi. O armağana da geleceğiz.", "Erhat ix4; Th. 511–514, 521–525")
seg('D05', B, "Erhat sorar: Neden bu eşi görülmemiş cezalar? Titan oldukları için mi? [firmly] Hayır. Ona göre dördü de zekâlarıyla öne çıkıyordu; bununla övünüyor, Zeus'a kafa tutmaya kalkıyorlardı.", "Erhat ix5")
seg('D07', B, "[slowly] Oysa, Erhat'ın deyişiyle: Akıl gücüyse, Zeus'un tekelindedir. Ve bu gücü başkasında görmek, içinde dinmez bir öfke doğurur.", "Erhat ix5, x1 (kısa alıntılar)",
    "Oysa, Erhat'ın deyişiyle: “Akıl gücüyse Zeus'un tekelindedir.” Ve bu gücü başkasında görmek, içinde “dinmez bir öfke” doğurur.")
seg('D08', B, "Prometeus da bu öfkeyi kışkırtmaktan geri durmaz. Keskin zekâsını ve geleceği görme yeteneğini, Zeus'u kandırmaya, kuşkuya düşürmeye, gülünç duruma sokmaya harcar.", "Erhat x2")
seg('D09', B, "Adı bile bunu söyler: Prometeus, önceden düşünen demektir; Erhat'ın deyişiyle, önceden gören bir kâhin. Bir zamanlar Gaya, Kronos'u düşeceği konusunda uyarmıştı. Şimdi de Prometeus, Zeus'un bir gün düşeceğini bilir.", "Erhat x4")
seg('D10', B, "Erhat buna bir ad verir: üçüncü devrimin hazırlanması. Hesiodos'un pek üstünde durmadığı, Ayshilos'un ise alabildiğine işlediği bir tema.", "Erhat x3 (kısa alıntı)",
    "Erhat buna bir ad verir: “üçüncü devrimin hazırlanması.” Hesiodos'un pek üstünde durmadığı, Aiskhylos'un ise alabildiğine işlediği bir tema.")
seg('D11', B, "[ominous] [slowly] Uranos devrilmişti. Kronos devrilmişti. Sıra kime gelecekti?", "anlatıcının köprüsü (ödemesi E16, I03)")

B = "Mekone'deki hile"
seg('E01', B, "[intrigued] Eski Yunanlar kurban kestiğinde, neden eti kendileri yer, tanrılara yalnızca kemikleri yakardı?", "Th. 556–557")
seg('E03', B, "Cevap, Prometeus'tan uzun uzun söz eden ilk şair Hesiodos'ta. Ona göre bir gün tanrılar ve insanlar, Mekoni denen yerde paylarını belirlemek için bir araya geldi. Prometeus büyük bir öküz kesti ve ikiye ayırdı.", "Erhat vi5; Th. 535–538")
seg('E04', B, "Bir yanda, öküzün midesine gizlenmiş etler. Öbür yanda, parlak bir yağ tabakasına sarılmış… [slowly] çıplak kemikler.", "Th. 538–541")
seg('E05', B, "[wryly] “Hangisini istersen seç,” dedi Zeus'a. Zeus yağlı payı aldı ve altından beyaz kemikler çıktı. O günden beri insanlar etin kendine düşen payını yer, sunaklarda tanrılara kemik yakar.", "Th. 548–557")
seg('E07', B, "[thoughtfully] Erhat'a göre bu, bir kurban geleneğinin kökenini açıklayan bir efsanedir. Ama asıl önemi başkadır: Prometeus, baştan beri insanlardan yanadır.", "Erhat x5")
seg('E08', B, "Onlara dayanarak Titanların öcünü almak, Olimpos tanrılarının yerine insanların egemenliğini getirmek ister. Yani, yeni bir devrimin hazırlayıcısıdır.", "Erhat x5 (kısa alıntı)",
    "Onlara dayanarak Titanların öcünü almak, Olympos tanrılarının yerine insanların egemenliğini getirmek ister. Yani, “yeni bir devrimin hazırlayıcısıdır.”")
seg('E09', B, "[wryly] Zeus hileyi görür; bile bile aldanır, ama olan olmuştur. [darkly] Gururu yaralanan tanrı, öcünü insanlardan alır: Ateşi onlardan esirger.", "Erhat x5; Th. 550–552, 562–564")
seg('E10', B, "Prometeus onu bir kez daha aldatır. Ateşi, içi boş bir rezene sapına gizleyip insanlara götürür. [darkly] [slowly] Hesiodos'un deyişiyle, insanların arasında uzaktan parlayan o ışığı görmek, Zeus'u yüreğinin ta dibinden ısırır.", "Erhat x5; Th. 565–569; İG 50–52")
seg('E11', B, "[ominous] Erhat'a göre iki kez küçük düşürülen tanrıların kralı, artık kaba kuvvete başvurmak zorundaydı.", "Erhat x5")
seg('E12', B, "İlk ceza insanlara geldi. Hefaistos topraktan bir kız biçimlendirdi; bütün tanrılar ona birer armağan verdi, Hermes ise diline yalanı koydu. Adı, Pandora'ydı.", "İG 57–82; Th. 570–584")
seg('E13', B, "Prometeus kardeşini uyarmıştı: Zeus'tan asla armağan kabul etme. [wryly] Ama Epimeteus, yani “sonradan düşünen”, ancak iş işten geçince düşündü.", "İG 83–89")
seg('E14', B, "[ominous] Pandora büyük küpün kapağını kaldırdı. Hastalıklar, acılar, dertler dünyaya yayıldı. [softly] İçeride yalnızca bir şey kaldı: Umut.", "İG 90–99")
seg('E15', B, "Hesiodos hikâyeyi Zeus'tan yana anlatır: Zeus'u aldatmak da, aklını aşmak da mümkün değildir. [knowingly] Ama Erhat satır aralarında başka bir şey okur: insanların gözünde küçük düşmüş, gülünç olmuş bir tanrı. Çünkü akıl gücü, artık tanrılardan insanlara geçmiştir.", "Th. 613–616; İG 105; Erhat x6, xi1")
seg('E16', B, "[slowly] Ve Erhat, sıranın kime geldiğini söyler: Üçüncü ve son devrim olup bitmiştir. İnsan, kendi gücünün bilincine varmış… Olimpos'un tanrılarına karşı ayaklanmıştır.", "Erhat xi1 (Erhat'ta 'tanrıya karşı'; bağlam gereği Olympos tanrıları) — D11'in cevabı",
    "Ve Erhat, sıranın kime geldiğini söyler: “Üçüncü ve son devrim” olup bitmiştir. İnsan, kendi gücünün bilincine varmış… Olympos'un tanrılarına karşı ayaklanmıştır.")
seg('E16b', B, "[knowingly] Demek ki Zeus'u öfkelendiren, bir avuç ateşten fazlasıydı. [slowly] Ve Prometeus bunun bedelini, dünyanın ucunda ödeyecekti.", "anlatıcının sonucu (A05'in ara cevabı; Erhat x1, x5)")

B = 'Duruşma'
seg('F01', B, "[thoughtfully] Aynı Titan, yüzyıllar sonra Atina'da sahneye çıktığında, neden bambaşka birine dönüştü?", "Erhat vii1, ix3")
seg('F02', B, "Erhat'a göre tanrıların taht kavgasını anlatırken iki şair aşağı yukarı aynı efsaneleri izler. Ama iş Prometeus'a gelince, yorum büsbütün değişir. Ona göre bu fark, politika bilincinin nasıl geliştiğini gösterir.", "Erhat ix3, vii1")
seg('F03', B, "Ve önsözün öbür sorusu burada gelir: Prometeus, ne bakımdan insandır? Erhat cevap için bir yol önerir: Bugün bir yazar bu olayı sahneye koysa, bir duruşma kurardı; sanığı, tanıkları ve yargıçlarıyla.", "Erhat xi2, xi4 (cevabı G02)")
seg('F04', B, "Ona göre bu oyunu, örneğin Kafka'nın Dava romanını inceler gibi incelemeliyiz.", "Erhat xi4 (Erhat'ın andığı ad: Duruşma)")
seg('F05', B, "[slowly] Öyleyse duruşma başlasın. Sanık: Prometeus. Suçu: ateşi çalıp insanlara vermek, ve tanrıların kurduğu düzene karşı gelmek.", "Erhat xi3",
    "Öyleyse duruşma başlasın. Sanık: Prometheus. Suçu: ateşi çalıp insanlara vermek ve tanrıların kurduğu düzene karşı gelmek.")
seg('F05b', B, "[knowingly] Yargıç ise hiç görünmeyecek: Zeus, oyun boyunca bir kez bile sahneye çıkmaz.", "ZVP (Zeus konuşan rol değildir; ödemesi J06)")
seg('F06', B, "Sahne: dünyanın ucunda, İskit ülkesinin ıssız bir uçurumu. Zeus'un iki uşağı, zincirli sanığı önlerine katıp getirir: Kratos ve Bia, yani Güç ve Zor. Erhat onlara, kendi çağının diliyle, polis der.", "ZVP 1–4; Erhat xv3")
seg('F08', B, "Güç, cezanın amacını açıkça söyler: Prometeus, Zeus'un tiranlığını sevmeyi öğrenecek… ve insanseverliğinden vazgeçecek. [knowingly] Bugünkü filantropi kelimesinin atası olan Yunanca insansever sözcüğünün bilinen en eski örneklerinden biri, bu oyundadır.", "ZVP 7–11, 28 (philanthrōpos)",
    "Güç, cezanın amacını açıkça söyler: Prometheus, Zeus'un tiranlığını sevmeyi öğrenecek… ve insanseverliğinden vazgeçecek. Bugünkü “filantropi” kelimesinin atası olan Yunanca “insansever” sözcüğünün bilinen en eski örneklerinden biri bu oyundadır.")
seg('F07', B, "Zincirleri vurmak, demirci tanrı Hefaistos'a düşer. Bu işi istemeyerek yapar; zincirlediği kendi akrabasıdır. Ama Zeus'un buyruğunu çiğneyemez. [thoughtfully] Kendi deyişiyle: Gücü yeni ele geçiren herkes serttir.", "ZVP 14–19, 35, 39 (kendi çevirimiz)",
    "Zincirleri vurmak, demirci tanrı Hephaistos'a düşer. Bu işi istemeyerek yapar; zincirlediği kendi akrabasıdır. Ama Zeus'un buyruğunu çiğneyemez. Kendi deyişiyle: “Gücü yeni ele geçiren herkes serttir.”")
seg('F09', B, "[bitterly] İş sürerken Hefaistos inler: Ah, nefret ettiğim zanaatım! [coldly] Güç'ün cevabı buz gibidir: Tanrılara hükmetmekten başka her iş bir yüktür. Zeus'tan başka hiç kimse özgür değildir.", "ZVP 45–50 (kendi çevirimiz); Erhat xiii5",
    "İş sürerken Hephaistos inler: “Ah, nefret ettiğim zanaatım!” Güç'ün cevabı buz gibidir: “Tanrılara hükmetmekten başka her iş bir yüktür. Zeus'tan başka hiç kimse özgür değildir.”")
seg('F10', B, "[knowingly] Bu cümleyi aklında tut. Erhat'a göre dramın özü, tam da budur: özgürlük ve kölelik.", "Erhat xiii1 (ödemesi J02–J04)")
seg('F10a', B, "[thoughtfully] Ona göre bunu anlamak için çağı düşünmek gerekir. Beşinci yüzyıl Atinası'nda kölelik, yasalara uygun, canlı bir kurumdu. Prometeus da herhangi bir köle gibi zincire vurulmuştur; oyunun Yunanca adındaki desmotes kelimesi, tam olarak budur. [slowly] Ama işkencesinin büyüklüğü zincirde değil, bir tanrının köle durumuna düşürülmesindedir.", "Erhat xiii2, v1",
    "Ona göre bunu anlamak için çağı düşünmek gerekir. V. yüzyıl Atinası'nda kölelik, yasalara uygun, canlı bir kurumdu. Prometheus da herhangi bir köle gibi zincire vurulmuştur; oyunun Yunanca adındaki “desmotes” kelimesi tam olarak budur. Ama işkencesinin büyüklüğü zincirde değil, bir tanrının köle durumuna düşürülmesindedir.")
seg('F11', B, "[mocking] Giderken Güç alay eder: Sana boşuna önceden düşünen demişler. Asıl şimdi, bu zincirden kurtulmanın yolunu önceden düşünecek birine ihtiyacın var.", "ZVP 85–87 (kendi çevirimiz)",
    "Giderken Güç alay eder: “Sana boşuna ‘önceden düşünen’ demişler. Asıl şimdi, bu zincirden kurtulmanın yolunu önceden düşünecek birine ihtiyacın var.”")
seg('F10b', B, "[slowly] Ve Erhat'ın dikkat çektiği bir ayrıntı: Bütün bu sahne boyunca Prometeus tek söz etmedi. Çekiç indi, bir daha indi; kayaya çakılmaya, zincire, hakaretlere, sessizce katlandı.", "Erhat xv3; ZVP 1–87")
seg('F13', B, "[softly] Ancak hepsi gidip yapayalnız kalınca konuşur. İlk sözleri göğedir: [reverently] Ey kutsal gök, ey hızlı kanatlı rüzgârlar, ırmakların kaynakları, deniz dalgalarının sayısız gülüşü… ve sen, herkesin anası Toprak; ve her şeyi gören güneş çemberi. [pained] Bakın bana: Bir tanrı, tanrılardan neler çekiyor.", "ZVP 88–92 (kendi çevirimiz)",
    "Ancak hepsi gidip yapayalnız kalınca konuşur. İlk sözleri göğedir: “Ey kutsal gök, ey hızlı kanatlı rüzgârlar, ırmakların kaynakları, deniz dalgalarının sayısız gülüşü… ve sen, herkesin anası Toprak; ve her şeyi gören güneş çemberi: Bakın bana, bir tanrı tanrılardan neler çekiyor.”")
seg('F14', B, "[whispers] Sonra birden kendi sözünü keser: Ama ne diyorum? Olacak her şeyi önceden, apaçık biliyorum; hiçbir acı bana habersiz gelmeyecek. [pained] [slowly] Yine de başıma gelenler üstüne… ne susabiliyorum, ne de konuşabiliyorum.", "ZVP 101–107 (kendi çevirimiz; Erhat s. xii'deki çeviri dizelerinden farklı)",
    "Sonra birden kendi sözünü keser: “Ama ne diyorum? Olacak her şeyi önceden, apaçık biliyorum; hiçbir acı bana habersiz gelmeyecek. Yine de başıma gelenler üstüne… ne susabiliyorum ne de konuşabiliyorum.”")

B = 'Savunma'
seg('G01', B, "[intrigued] Zincirdeki sanık, kendini nasıl savunur?", "Erhat xi5")
seg('G02', B, "Erhat'a göre savunması iki kavrama dayanır: bilinç ve özgürlük. Bunlar, uygar her toplumda benimsenmiş, insana özgü değişmez değerlerdir. [knowingly] Yani Prometeus'u insan yapan, bu ikisidir.", "Erhat xi5 (son cümle F03'ün cevabı: anlatıcı)")
seg('G03', B, "Çekiç seslerini duyan deniz perileri, Okeanos'un kızları, derinliklerden gelir. Prometeus onlara geçmişi anlatır. Titanlarla Zeus savaşırken, annesi ona geleceği söylemişti. Ayshilos'ta bu anne Toprak'tır; öbür adıyla Temis, yani Adalet.", "ZVP 128–135, 199–211; Erhat x4")
seg('G04', B, "Ve kehaneti açıktı: Zafer, gücün ve zorun değil… kurnazlığın olacaktı.", "ZVP 212–213")
seg('G05', B, "Titanlar bu öğüdü küçümsedi. Prometeus da Zeus'un yanına geçti; Kronos'u Tartaros'un karanlığına gömen, onun öğütleri oldu. [knowingly] Erhat'ın andığı o rolü, Ayshilos işte böyle anlatır.", "ZVP 214–221; Erhat viii1")
seg('G06', B, "[bitterly] Şimdi ise tahta çıkardığı tanrının zincirindeydi. Prometeus bunu tek cümleyle açıklar: Zorbalığın bir hastalığı vardır; dostlarına güvenmez.", "ZVP 221–225 (kendi çevirimiz)",
    "Şimdi ise tahta çıkardığı tanrının zincirindeydi. Prometheus bunu tek cümleyle açıklar: “Zorbalığın bir hastalığı vardır: dostlarına güvenmez.”")
seg('G07', B, "Zeus tahta oturur oturmaz tanrılara görevlerini dağıttı. Ama zavallı insanları hiç hesaba katmadı; onları yok edip yerine yeni bir soy yaratmak istiyordu. Buna karşı çıkan tek kişi, Prometeus oldu.", "ZVP 228–236")
seg('G07b', B, "[softly] Kendi sözleriyle: Ölümlülere acıdım. [pained] Ama bana acımayı… kimse layık görmedi.", "ZVP 239–241 (kendi çevirimiz)",
    "Kendi sözleriyle: “Ölümlülere acıdım. Ama bana acımayı… kimse layık görmedi.”")
seg('G08', B, "İnsanları kurtarmakla da kalmadı. Ölümlerini önceden görmelerini engelledi; içlerine kör umutlar yerleştirdi. [warmly] Sonra da ateşi verdi.", "ZVP 248–254")
seg('G09', B, "[intrigued] Erhat burada sorar: Ateşi tanrılardan çalıp insanlara vermek, ne demektir? Ona göre başkaları bunu bir efsane olarak bırakmıştı. Ayshilos ise ondan, uygarlığın tarihini çıkarır.", "Erhat xv2 (kısa alıntı)",
    "Erhat burada sorar: “Ateşi tanrılardan çalıp insanlara vermek ne demektir?” Ona göre başkaları bunu bir efsane olarak bırakmıştı. Aiskhylos ise ondan uygarlığın tarihini çıkarır.")
seg('G10', B, "Ateşten önce insanlar, gözleri olup görmeyen, kulakları olup duymayan varlıklardı; güneş görmeyen mağaralarda, karıncalar gibi yaşıyorlardı.", "ZVP 447–453")
seg('G10b', B, "Prometeus onlara yıldızları, sayıları, harfleri öğretti; hayvanları evcilleştirmeyi, gemiyi, ilacı, madenleri… [proudly] Tek sözle: İnsanlardaki bütün zanaatlar, Prometeus'tan gelir.", "ZVP 454–506 (kendi çevirimiz)",
    "Prometheus onlara yıldızları, sayıları, harfleri öğretti; hayvanları evcilleştirmeyi, gemiyi, ilacı, madenleri… “Tek sözle: İnsanlardaki bütün zanaatlar Prometheus'tan gelir.”")
seg('G11', B, "[firmly] Ve sanık suçunu inkâr etmez. Oyundaki sözleriyle: Bunların hepsini biliyordum. İsteyerek, isteyerek suç işledim. [thoughtfully] Erhat'a göre bu, bugünkü bir sanığın savunmasıdır: Ne yaptımsa, bile bile yaptım.", "ZVP 265–266 (kendi çevirimiz); Erhat xi5 (kısa alıntı)",
    "Ve sanık suçunu inkâr etmez. Oyundaki sözleriyle: “Bunların hepsini biliyordum. İsteyerek, isteyerek suç işledim.” Erhat'a göre bu, bugünkü bir sanığın savunmasıdır: “Ne yaptımsa bile bile yaptım.”")
seg('G12b', B, "[pained] [slowly] Ama hemen ardından şunu da itiraf eder: Böyle cezalarla, bu ıssız, yüksek kayada eriyip gideceğimi… düşünmemiştim.", "ZVP 268–270 (kendi çevirimiz)",
    "Ama hemen ardından şunu da itiraf eder: “Böyle cezalarla, bu ıssız, yüksek kayada eriyip gideceğimi… düşünmemiştim.”")
seg('G13', B, "[thoughtfully] Erhat'a göre bu bilinç, onda hem bir gurur, hem de bir katlanma duygusu doğurur. Biliyordu; ama bu kadarını beklemiyordu. [slowly] Ve yine de geri adım atmaz.", "Erhat xii1 (ikinci ve üçüncü cümle anlatıcının; ZVP 268–270)")

B = 'Tanıklar'
seg('H01', B, "[curious] Bu duruşmada kimler tanıklık eder? Ve içlerinden birinin hikâyesi, nasıl oldu da İstanbul Boğazı'nın adına karıştı?", "Erhat xiv1; Apollodoros II.1.3")
seg('H02', B, "Erhat'a göre oyunun evreni, Zeus'un kurbanları, uşakları ve dalkavuklarıyla doludur. Hepsi onun buyruğunu yerine getirir; kimi isteyerek, kimi istemeyerek. [firmly] Tek başkaldıran, Prometeus'tur.", "Erhat xiv1, xiii3")
seg('H03', B, "Uşakları gördük: Güç, Zor ve Hefaistos. Sırada bir dalkavuk var: yaşlı Titan Okeanos.", "Erhat xiv1")
seg('H04', B, "Okeanos iyi niyetlidir; Zeus'a gidip aracılık etmeyi bile önerir. Bir şartla: [softly] Kendini bil, der, huyunu değiştir; tanrıların başında yeni bir tiran var. Dilini de bu kadar azdırma. [coldly] Prometeus teklifi geri çevirir: Onu ikna edemezsin; kendi başını derde sokma.", "ZVP 307–331, 385 (kendi çevirimiz)")
seg('H05', B, "Periler bile ona, sözünü hiç sakınmıyorsun, der. [knowingly] Erhat'a göre Yunancadaki ifade, tam olarak dilin fazla özgür demektir. Başkaları, hiçbir umuda yer vermeden direnen bu bilinçli tutumu anlamaz; gurur, hatta kibir sanır. [slowly] Oysa Prometeus'a özgürlüğü sağlayan, bilincidir.", "ZVP 178–180; Erhat xii4, xiii1 (kısa alıntılar)",
    "Periler bile ona “sözünü hiç sakınmıyorsun” der. Erhat'a göre Yunancadaki ifade tam olarak “dilin fazla özgür” demektir. Başkaları, “hiçbir umuda yer vermeden” direnen bu bilinçli tutumu anlamaz; gurur, hatta kibir sanır. Oysa Prometheus'a özgürlüğü sağlayan bilincidir.")
seg('H05b', B, "[thoughtfully] Tuhaf olan şu: İnsanlara kör umutları veren de oydu. Kendine ise, hiçbir umut tanımadı.", "anlatıcının yan yana koyması (ZVP 250; Erhat xii4)")
seg('H06', B, "Sonra bir kurban gelir: boynuzlu, genç bir kız. Adı İyo. Zeus'un gönlü ona düşmüş, Hera'nın öfkesi de peşine takılmıştı: Bir atsineği onu durmadan dünyanın dört bir yanına kovalıyordu.", "ZVP 561–686; Erhat xiv1 (Io: Zeus'un kurbanı)")
seg('H07', B, "[intrigued] Prometeus ona yolculuğunun haritasını çıkarır. Yolu bir boğazdan geçecek; o boğaz da bu geçişten adını alacak: Bosporos. Yani, inek geçidi. [knowingly] Ayshilos'un sözünü ettiği, Kırım'ın doğusundaki Kerç Boğazı'dır; ama başka antik anlatılar, aynı adı İstanbul Boğazı'na verir.", "ZVP 729–735 (Kimmer Bosporosu); Apollodoros II.1.3",
    "Prometheus ona yolculuğunun haritasını çıkarır. Yolu bir boğazdan geçecek; o boğaz da bu geçişten adını alacak: Bosporos, yani “inek geçidi.” Aiskhylos'un sözünü ettiği, Kırım'ın doğusundaki Kerç Boğazı'dır; ama başka antik anlatılar aynı adı İstanbul Boğazı'na verir.")
seg('H09', B, "[softly] İyo, acısına dayanamayıp ölmeyi diler. Prometeus'un cevabı ağırdır: Ben ölemem bile. İşkencem, Zeus tiranlığından düşmedikçe bitmeyecek.", "ZVP 747–756 (kendi çevirimiz); Erhat xii3")
seg('H10', B, "Ve ekler: İyo'nun soyundan, on üç kuşak sonra, onu bu zincirden kurtaracak bir okçu doğacak.", "ZVP 771–774, 871–873 (ödemesi L01–L02)")

B = 'Tahtı sallayan sır'
seg('I01', B, "[intrigued] Zincirdeki bir sanık, yargıcını nasıl korkutabilir?", "")
seg('I02', B, "Prometeus bir sır biliyordu. Zeus bir gün bir evlilik yapacaktı. Ve o evlilikten, babasından daha güçlü bir oğul doğacaktı.", "ZVP 764–768, 907–912")
seg('I03', B, "[slowly] Tıpkı Uranos'un ve Kronos'un başına gelen gibi. Babasını deviren oğul, şimdi oğlundan korkan babaydı. [knowingly] Erhat'ın üçüncü devrimin hazırlanması dediği şey buydu: Zeus'u sürekli bir kuşkunun baskısı altında tutan bir bilgi.", "ZVP 910–914; Erhat x3, x4 (ikinci cümle anlatıcının)")
seg('I04', B, "Kiminle evlenmemesi gerektiğini yalnızca Prometeus biliyordu. Ayshilos o adı vermez; başka anlatılar, onun deniz perisi Tetis olduğunu söyler.", "ZVP 913–925; Pindaros, İsthmia 8.26–47")
seg('I05', B, "Sonunda Zeus, habercisi Hermes'i gönderir. Erhat ona, sanığı gözdağıyla sorguya çeken bir polis müdürü der. Emir kısadır: Sırrı söyle.", "ZVP 944–952; Erhat xv3")
seg('I06', B, "[defiantly] Prometeus alay eder: Siz yeni tanrılar, kalenizde hiç acı yüzü görmeyeceğinizi sanıyorsunuz. Ben oradan iki tiranın düştüğünü görmedim mi? Şimdi hüküm sürenin düşüşünü de göreceğim: en utanç verici biçimde, en çabuk.", "ZVP 953–959 (kendi çevirimiz)",
    "Prometheus alay eder: “Siz yeni tanrılar, kalenizde hiç acı yüzü görmeyeceğinizi sanıyorsunuz. Ben oradan iki tiranın düştüğünü görmedim mi? Şimdi hüküm sürenin düşüşünü de göreceğim: en utanç verici biçimde, en çabuk.”")
seg('I07', B, "Hermes'in tehditlerine cevabı tek cümledir: Bu felaketimi, senin uşaklığına değişmem.", "ZVP 966–967 (kendi çevirimiz)",
    "Hermes'in tehditlerine cevabı tek cümledir: “Bu felaketimi senin uşaklığına değişmem.”")
seg('I07b', B, "[defiantly] Ve zincirdeki adam, evrenin efendisine şart koşar: Bu aşağılayıcı zincirler çözülmeden, Zeus bu sırrı benden ne işkenceyle alabilir, ne de hileyle.", "ZVP 989–991 (kendi çevirimiz)",
    "Ve zincirdeki adam, evrenin efendisine şart koşar: “Bu aşağılayıcı zincirler çözülmeden, Zeus bu sırrı benden ne işkenceyle alabilir ne de hileyle.”")

B = 'Zincirin öbür ucu'
seg('J01', B, "[slowly] Sorguyu burada bir an durduralım. [mysterious] Bu sahnede asıl tutsak olan kim?", "A02'nin sorusuna dönüş")
seg('J02', B, "Görünüşe bakılırsa cevap açık. Güç'ün ilk sahnedeki sözünü hatırla: Zeus'tan başka hiç kimse özgür değildir. Prometeus ise köledir: zincirde, ölümsüz olduğu için canına kıyma özgürlüğü bile yok. [intrigued] Erhat sorar: Ama bakalım, gerçekten de öyle mi?", "Erhat xiii4 (kısa alıntı); ZVP 50",
    "Görünüşe bakılırsa cevap açık. Güç'ün ilk sahnedeki sözünü hatırla: “Zeus'tan başka hiç kimse özgür değildir.” Prometheus ise köledir: zincirde, ölümsüz olduğu için canına kıyma özgürlüğü bile yok. Erhat sorar: “Ama bakalım gerçekten de öyle mi?”")
seg('J04', B, "[slowly] Ve cevap verir: Gerçekte Zeus köle… [firmly] Prometeus özgürdür.", "Erhat xiv2 (kısa alıntı)",
    "Ve cevap verir: “Gerçekte Zeus köle, Prometheus özgürdür.”")
seg('J05', B, "Bütün uşaklarına, dalkavuklarına rağmen Zeus, bir çocuk gibi zayıf ve çaresizdir. Onu yıkımdan kurtarabilecek tek kişi, aklın taşıyıcısı Prometeus'tur.", "Erhat xiv5")
seg('J06', B, "[knowingly] Erhat'ın deyişiyle: Zeus, tutukladığı düşmanının elinde tutukludur aslında. [slowly] Roller yer değiştirmiştir: Sanık özgür, görünmeyen yargıç tutsak.", "Erhat xiv5 (kısa alıntı); son cümle anlatıcının (F05b'nin ödemesi)",
    "Erhat'ın deyişiyle: “Zeus tutukladığı düşmanının elinde tutukludur aslında.” Roller yer değiştirmiştir: Sanık özgür, görünmeyen yargıç tutsak.")
seg('J08', B, "Erhat'a göre oyunun politika dersi de buradadır: Akılla tahta çıkan bir yönetim, akla ve özgür düşünceye sırt çevirdiğinde zayıflar… ve devrilme tehlikesiyle yüz yüze gelir.", "Erhat xiv4")
seg('J10', B, "Köleliği doğal sayan bir dünyada, hakkın köleden yana olduğunu söylemek… Ona göre bu, Ayshilos'un tek başına başardığı koca bir işti.", "Erhat xiii2")

B = 'Kartal, fırtına ve son söz'
seg('I08', B, "[pained] Sorgu sürer. Bir an, Prometeus'un ağzından tek bir inilti kaçar: Eyvah! [mocking] Hermes hemen yakalar: Zeus bu kelimeyi bilmez. [calmly] Prometeus'un cevabı: Yaşlanan zaman, her şeyi öğretir.", "ZVP 979–981 (kendi çevirimiz)",
    "Sorgu sürer. Bir an, Prometheus'un ağzından tek bir inilti kaçar: “Eyvah!” Hermes hemen yakalar: “Zeus bu kelimeyi bilmez.” Prometheus'un cevabı: “Yaşlanan zaman her şeyi öğretir.”")
seg('I08b', B, "[ominous] Hermes son tehdidini savurur: Kaya yıldırımla parçalanacak, sen içine gömüleceksin. Uzun zaman sonra ışığa döndüğünde, Zeus'un kanatlı köpeği, kanlı kartal gelecek. Çağrılmamış bir konuk gibi, bütün gün karaciğerinle ziyafet çekecek.", "ZVP 1016–1025 (kendi çevirimiz)")
seg('I08c', B, "[slowly] Açılıştaki kartal, Ayshilos'ta henüz gelmemiştir; o, hayır demenin bedelidir. [defiantly] Ama Prometeus, İyo'ya yakınarak söylediğini şimdi bir meydan okuma gibi söyler: Ne yaparsa yapsın… beni öldüremez.", "ZVP 1053 (kendi çevirimiz); ilk cümle anlatıcının")
seg('I09', B, "Hermes, perilere oradan gitmelerini söyler. Ama periler kalır: Hainlerden nefret etmeyi öğrendik, deyip Prometeus'un yanında dururlar.", "ZVP 1058–1070 (kendi çevirimiz)",
    "Hermes perilere oradan gitmelerini söyler. Ama periler kalır: “Hainlerden nefret etmeyi öğrendik” deyip Prometheus'un yanında dururlar.")
seg('I10', B, "[intense] Ve gök boşanır. Prometeus olanları kendi ağzıyla anlatır: Artık sözde değil, gerçekte! Yer sarsılıyor, gök gürlüyor, şimşekler çakıyor. Rüzgârlar birbirine saldırıyor… gök, denize karıştı.", "ZVP 1080–1090 (kendi çevirimiz); Erhat xv3 (diliyle canlandırır)")
seg('I11', B, "[pained] [slowly] İlk sözleri gibi, son sözleri de göğe ve anasınadır; adlarından biri Adalet olan anasına: Görüyor musun, ne haksızlıklara uğruyorum.", "ZVP 1091–1093 (kendi çevirimiz); F13 ve G03 ile halka",
    "İlk sözleri gibi son sözleri de göğe ve anasınadır, adlarından biri Adalet olan anasına: “Görüyor musun, ne haksızlıklara uğruyorum.”")
seg('I12', B, "[firmly] Başta tek söz etmeyen Prometeus, dünya başına yıkılıp yanında kalan perilerle birlikte gömülene dek, konuşmakta direnir. Son söz onundur. [slowly] Erhat'a göre Ayshilos'un söylemek istediği de budur: Kıyamet de kopsa, son söz özgür düşüncenindir.", "Erhat xv3 (kısa alıntı)",
    "Başta tek söz etmeyen Prometheus, dünya başına yıkılıp yanında kalan perilerle birlikte gömülene dek konuşmakta direnir. Son söz onundur. Erhat'a göre Aiskhylos'un söylemek istediği de budur: “Kıyamet de kopsa son söz özgür düşüncenindir.”")

B = 'Ateşin yolculuğu'
seg('L01', B, "[softly] Peki Prometeus'un haber verdiği o okçu, gerçekten geldi mi?", "H10'un ödemesi")
seg('L02', B, "Hesiodos'a göre geldi. Adı Herakles'ti; kartalı okuyla vurdu ve Prometeus'u acısından kurtardı. [wryly] Tabii Zeus'un izniyle: oğlunun ünü artsın diye. Ayshilos'un bu kurtuluşu anlattığı Kurtulmuş Prometeus ise kayıp; elimizde yalnızca birkaç parçası var.", "Th. 526–534; Erhat v2")
seg('L03', B, "[softly] Ama insanlık Prometeus'u, kurtulduğu anla değil, zincirdeki hâliyle hatırladı.", "anlatıcının yorumu")
seg('L04', B, "Erhat, onun izini Hesiodos'tan Alman şair Göte'ye kadar sürmeyi önerir. Göte'nin şiirinde Titan, Zeus'a meydan okur ve insanları kendi suretinde yoğurur. Erhat'a göre bu şiirden çıkan anlam şudur: Asıl yaratıcı, insanın kendisidir.", "Erhat vi6, xi1 (kısa alıntı); Goethe, 'Prometheus' (1774)",
    "Erhat, onun izini Hesiodos'tan Alman şair Goethe'ye kadar sürmeyi önerir. Goethe'nin şiirinde Titan, Zeus'a meydan okur ve insanları kendi suretinde yoğurur. Erhat'a göre bu şiirden çıkan anlam şudur: “Asıl yaratıcı, insanın kendisidir.”")
seg('L05', B, "Meri Şeli, Frankenştayn romanına Modern Prometeus alt başlığını koydu. Atom bombasının mimarı Openhaymır'ın biyografisinin adı da Amerikan Prometeus: Nolan'ın filmi bu kitaba dayanır.", "Shelley 1818; Bird & Sherwin 2005; Nolan 2023",
    "Mary Shelley, Frankenstein romanına “Modern Prometheus” alt başlığını koydu. Atom bombasının mimarı Oppenheimer'ın biyografisinin adı da “American Prometheus”: Nolan'ın filmi bu kitaba dayanır.")
seg('L06', B, "[softly] İnsan ne zaman kendisine yasaklanmış bir ateşe el uzatsa, o eski Titan'ın adı yeniden anılır.", "anlatıcının yorumu")

B = 'Başkaldıran yaratık'
seg('K01', B, "[thoughtfully] Erhat'ın önsözü de, tam bu soruyla açılır: İnsan nedir? Ne zaman insan olmaya başladı?", "Erhat v6")
seg('K02', B, "Erhat, kendi çağının düşünürlerinin sanki sözleşmiş gibi verdiği cevabı aktarır: İnsan, başkaldıran yaratıktır. Bu görüşe göre insanı insan yapan, doğaya ya da geleneğe boyun eğmeyi reddettiği andır; insan kalabilmek için de bu isyanı her seferinde yeniden başlatmak zorundadır.", "Erhat v6 (kısa alıntı + kendi cümlelerimiz)",
    "Erhat, kendi çağının düşünürlerinin sanki sözleşmiş gibi verdiği cevabı aktarır: “İnsan başkaldıran yaratıktır.” Bu görüşe göre insanı insan yapan, doğaya ya da geleneğe boyun eğmeyi reddettiği andır; insan kalabilmek için de bu isyanı her seferinde yeniden başlatmak zorundadır.")
seg('K04', B, "Erhat, kendi kuşağının bu görüşü öylesine benimsediğini yazar ki, gelenek süslerini üstlerinden atmışlardır. Ve ekler: Umuda karşı da ayaklandık. Bugün, bu dünyada yaşamak istiyorlardı.", "Erhat vi1, vi2 (kısa alıntı)",
    "Erhat, kendi kuşağının bu görüşü öylesine benimsediğini yazar ki, gelenek süslerini üstlerinden atmışlardır. Ve ekler: “Umuda karşı da ayaklandık.” Bugün, bu dünyada yaşamak istiyorlardı.")
seg('K08a', B, "[firmly] Erhat'ın en baştaki sorusunun cevabı da önsözün içinde. Efsane Prometeus'a kâhin der. Erhat'ın yirminci yüzyılı kâhine inanmaz; ama aklıyla geleceği gören düşünürü tanır, onun kör iktidarların baskısına uğradığını da bilir.", "Erhat xiv6, xv1 (kısa alıntı); B06'nın cevabı",
    "Erhat'ın en baştaki sorusunun cevabı da önsözün içinde. Efsane Prometheus'a kâhin der. Erhat'ın XX. yüzyılı kâhine inanmaz; ama aklıyla geleceği gören düşünürü tanır, onun “kör iktidarların baskısına” uğradığını da bilir.")
seg('K08b', B, "Ona göre Ayshilos, insan toplumunun değişmez bir yasasını sezmişti: Kaba güç gelip geçer, düşünce kalır. [slowly] Bu yasa değişmediği için, yirmi beş yüzyıl önceki bu sanık, hâlâ insana benziyor.", "Erhat xiv3 (ilk cümle Erhat'ın özeti; ikinci cümle anlatıcının)")
seg('K06', B, "Erhat'a göre bu kuşağın tek ülküsü, insan olmaktı; bu uğurda katlanılmayacak cefa yoktu. [slowly] [reverently] Ve önsöz, bu ülkünün ilk temsilcisini tek cümleyle adlandırır: Bu ülkünün ilk temsilcisi… Prometeus'tur.", "Erhat vi3, vi4 (kısa alıntı)",
    "Erhat'a göre bu kuşağın tek ülküsü insan olmaktı; bu uğurda katlanılmayacak cefa yoktu. Ve önsöz, bu ülkünün ilk temsilcisini tek cümleyle adlandırır: “Bu ülkünün ilk temsilcisi Prometheus'tur.”")

B = 'Kapanış'
seg('M00', B, "[warmly] Erhat ile Eyüboğlu, çeviriye başlarken bu oyunun çevrilemeyeceğini, hatta sahnelenemeyeceğini düşünüyormuş. Çevirdikçe yanıldıklarını anlamışlar… ve coşmuşlar. Dilekleri, Prometeus'u bir gün bir Türk tiyatrosunda görmekti.", "Erhat xv4, xvi1")
seg('M02', B, "[curious] Peki sen olsan? Bedelini bile bile, o ateşi yine de verir miydin? Yorumlarda yaz.", "")
seg('M03', B, "[warmly] Tanrılara kafa tutan bir başka isyankârın, Sisifos'un hikâyesi ekranda. Bu hikâyeler hoşuna gidiyorsa, kanala abone olmayı unutma.", "bitiş ekranı: Sisifos videosu + abone")


# — sıkılaştırma (21 dk hedefi): kısaltılan cümleler ve çıkarılanlar —
DROP = {'C08', 'F04', 'G04', 'H03', 'F11', 'J08', 'C15', 'E13', 'G10'}
OVR = {
 'C02': ("Erhat'a göre efsanenin de, oyunun da merkezinde, bugün “hükümet darbesi” diyebileceğimiz bir olay var: Bir kuşak, öncekini devirip yönetimi ele geçirir.",
         "Erhat'a göre efsanenin de oyunun da merkezinde, bugün “hükümet darbesi” diyebileceğimiz bir olay var: Bir kuşak, öncekini devirip yönetimi ele geçirir."),
 'C04': ("Hesiodos'un Teogonia'sına göre önce Kaos vardı, sonra Toprak Ana, Gaya. Gaya kendine eş olarak Gök'ü, Uranos'u doğurdu. [darkly] Ama Uranos, Gaya'dan doğan devlerden tiksindi; her birini doğar doğmaz, annelerinin karnına geri tıktı.", None),
 'C07': ("[tense] Kronos gece pusuya yattı. Uranos Gaya'nın üstüne eğildiği anda, oğlu tırpanı savurdu… ve babasını iğdiş etti. [knowingly] Erhat burada, tanrıların tarihinde bir devrim görür.", None),
 'C09': ("[darkly] Ama bu devrim de, kendi çocuklarını yedi. Hem de kelimenin tam anlamıyla: Oğullarından birinin onu devireceğini bilen Kronos, çocuklarını doğar doğmaz yuttu.", None),
 'C12': ("[thoughtfully] Erhat'a göre bu iki devrim aynı değildir. Birincisi kaba kuvvetin kendi kendini yenmesiydi; ikincisi, kaba kuvvetin akılla yenilmesi. Bu kez Zeus'a, ders almış Uranos ile Gaya yol göstermişti.",
         "Erhat'a göre bu iki devrim aynı değildir. Birincisi kaba kuvvetin kendi kendini yenmesiydi; ikincisi, “kaba kuvvetin akılla yenilmesi.” Bu kez Zeus'a, ders almış Uranos ile Gaia yol göstermişti."),
 'C15': ("Ardından Titanlarla on yıllık bir savaş geldi. Zeus, Gaya'nın öğüdüyle yerin altındaki yüz kollu devleri savaşa sürdü. [intense] Yer sarsıldı, denizler altüst oldu… ve Titanlar Tartaros'a kapatıldı.", None),
 'C17': ("[thoughtfully] Ona göre kaba güçler birbirini yok etmişti; meydanda akıldan başka güç kalmamıştı. Yıldırım elinde, Zeus tahta oturdu ve dünyayı paylaştırmaya girişti.", None),
 'D03': ("Dördünün de sonu tüyler ürperticiydi. Atlas, dünyanın ucunda göğü omuzlarında taşımaya mahkûm edildi; Menoitios, yıldırımla yerin dibine gömüldü.", None),
 'D04': ("Prometeus bir sütuna zincirlendi, karaciğeri kartala yem oldu. Epimeteus'a ise bir “armağan” gönderildi. Ona da geleceğiz.", None),
 'D05': ("Erhat sorar: Neden bu eşi görülmemiş cezalar? Titan oldukları için mi? [firmly] Hayır. Dördü de zekâlarıyla öne çıkıyor, Zeus'a kafa tutmaya kalkıyordu.", None),
 'D08': ("Prometeus da bu öfkeyi kışkırtmaktan geri durmaz. Keskin zekâsını ve geleceği görme gücünü, Zeus'u kandırmak, kuşkuya düşürmek, gülünç etmek için kullanır.", None),
 'D09': ("Adı da bunu söyler: Prometeus, önceden düşünen demektir; Erhat'ın deyişiyle bir kâhin. Gaya nasıl Kronos'u uyarmışsa, Prometeus da Zeus'un bir gün düşeceğini bilir.", None),
 'D10': ("Erhat buna bir ad verir: üçüncü devrimin hazırlanması.", "Erhat buna bir ad verir: “üçüncü devrimin hazırlanması.”"),
 'E03': ("Cevap, Hesiodos'ta. Bir gün tanrılar ve insanlar, Mekoni'de paylarını belirlemek için toplanır. Prometeus büyük bir öküz keser ve ikiye ayırır.", None),
 'E04': ("Bir yanda, öküzün midesine gizlenmiş etler. Öbür yanda, parlak bir yağa sarılmış… [slowly] çıplak kemikler.", None),
 'E05': ("[wryly] “Hangisini istersen seç,” der Zeus'a. Zeus yağlı payı alır; altından beyaz kemikler çıkar. O günden beri insanlar eti kendileri yer, tanrılara kemik yakar.", None),
 'E07': ("[thoughtfully] Erhat'a göre bu efsanenin asıl önemi başkadır: Prometeus, baştan beri insanlardan yanadır.", None),
 'E08': ("Onlara dayanarak, Olimpos tanrılarının yerine insanların egemenliğini getirmek ister. Yani, yeni bir devrimin hazırlayıcısıdır.",
         "Onlara dayanarak, Olympos tanrılarının yerine insanların egemenliğini getirmek ister. Yani, “yeni bir devrimin hazırlayıcısıdır.”"),
 'E09': ("[wryly] Zeus hileyi görür; bile bile aldanır, ama olan olmuştur. [darkly] Gururu yaralanan tanrı, öcünü insanlardan alır: Ateşi esirger.", None),
 'E10': ("Prometeus onu bir kez daha aldatır: Ateşi içi boş bir rezene sapına gizleyip insanlara götürür. [darkly] [slowly] Hesiodos'un deyişiyle, uzaktan parlayan o ışığı görmek, Zeus'u yüreğinin ta dibinden ısırır.", None),
 'E11': ("[ominous] Erhat'a göre iki kez küçük düşen tanrıların kralı, artık kaba kuvvete başvurmak zorundaydı.", None),
 'E12': ("İlk ceza insanlara gelir: Hefaistos topraktan bir kız yoğurur, tanrılar onu armağanlarla süsler; Hermes de diline yalanı koyar. Adı, Pandora'dır.", None),
 'E13': ("Prometeus kardeşini uyarmıştı: Zeus'tan armağan alma. [wryly] Ama Epimeteus, yani “sonradan düşünen”, ancak iş işten geçince düşünür.", None),
 'E14': ("[ominous] Pandora büyük küpün kapağını kaldırır; hastalıklar, acılar, dertler dünyaya yayılır. [softly] İçeride yalnızca bir şey kalır: Umut.", None),
 'E15': ("Hesiodos Zeus'tan yana anlatır: Zeus'un aklı aşılamaz. [knowingly] Ama Erhat satır aralarında başka bir şey okur: insanların gözünde gülünç düşmüş bir tanrı. Çünkü akıl gücü, artık tanrılardan insanlara geçmiştir.", None),
 'E16b': ("[knowingly] Demek ki Zeus'u öfkelendiren, bir avuç ateşten fazlasıydı. [slowly] Ve Prometeus bunun bedelini, dünyanın ucunda ödeyecekti.", None),
 'F02': ("Erhat'a göre taht kavgasını iki şair de aşağı yukarı aynı anlatır. Ama iş Prometeus'a gelince, yorum büsbütün değişir; bu da politika bilincinin nasıl geliştiğini gösterir.", None),
 'F03': ("Ve önsözün öbür sorusu burada gelir: Prometeus, ne bakımdan insandır? Erhat bir yol önerir: Bugün bu olayı sahneye koyan bir yazar, bir duruşma kurardı. Oyunu, Kafka'nın Dava'sını okur gibi okumalıyız.", None),
 'F05': ("[slowly] Öyleyse duruşma başlasın. Sanık: Prometeus. Suçu: ateşi çalıp insanlara vermek, ve tanrıların düzenine karşı gelmek.",
         "Öyleyse duruşma başlasın. Sanık: Prometheus. Suçu: ateşi çalıp insanlara vermek ve tanrıların düzenine karşı gelmek."),
 'F05b': ("[knowingly] Yargıç ise hiç görünmeyecek: Zeus, oyun boyunca sahneye bir kez bile çıkmaz.", None),
 'F06': ("Sahne, İskit ülkesinin ıssız bir uçurumu. Zeus'un iki uşağı, sanığı önlerine katıp getirir: Kratos ve Bia, yani Güç ve Zor. Erhat onlara, kendi çağının diliyle, polis der.", None),
 'F08': ("Güç, cezanın amacını söyler: Prometeus, Zeus'un tiranlığına boyun eğmeyi öğrenecek, insanseverlikten vazgeçecek. [knowingly] Filantropi kelimesinin atası, bilinen en eski örneklerinden biriyle, bu oyundadır.",
         "Güç, cezanın amacını söyler: Prometheus, Zeus'un tiranlığına boyun eğmeyi öğrenecek, insanseverlikten vazgeçecek. “Filantropi” kelimesinin atası, bilinen en eski örneklerinden biriyle bu oyundadır."),
 'F07': ("Zincirleri, demirci tanrı Hefaistos vurur. İstemeyerek; zincirlediği kendi akrabasıdır. Ama Zeus'un buyruğunu çiğneyemez. [thoughtfully] Kendi deyişiyle: Gücü yeni ele geçiren herkes serttir.",
         "Zincirleri, demirci tanrı Hephaistos vurur. İstemeyerek; zincirlediği kendi akrabasıdır. Ama Zeus'un buyruğunu çiğneyemez. Kendi deyişiyle: “Gücü yeni ele geçiren herkes serttir.”"),
 'F10a': ("[thoughtfully] Ona göre çağı düşünmek gerekir: Beşinci yüzyıl Atinası'nda kölelik, yasal bir kurumdu. Prometeus da bir köle gibi zincire vurulmuştu. [slowly] Ama asıl işkence zincir değil, bir tanrının köle durumuna düşürülmesidir.",
          "Ona göre çağı düşünmek gerekir: V. yüzyıl Atinası'nda kölelik yasal bir kurumdu. Prometheus da bir köle gibi zincire vurulmuştu. Ama asıl işkence zincir değil, bir tanrının köle durumuna düşürülmesidir."),
 'F11': ("[mocking] Giderken Güç alay eder: Sana boşuna önceden düşünen demişler. Asıl şimdi, seni kurtaracak bir önceden düşünene ihtiyacın var.",
         "Giderken Güç alay eder: “Sana boşuna ‘önceden düşünen’ demişler. Asıl şimdi, seni kurtaracak bir önceden düşünene ihtiyacın var.”"),
 'F10b': ("[slowly] Ve Erhat'ın dikkat çektiği bir ayrıntı: Bütün bu sahne boyunca Prometeus tek söz etmedi. Çekiç indi, bir daha indi; zincire, hakaretlere, sessizce katlandı.", None),
 'F13': ("[softly] Ancak yapayalnız kalınca konuşur. İlk sözleri göğedir: [reverently] Ey kutsal gök, hızlı kanatlı rüzgârlar, ırmakların kaynakları, deniz dalgalarının sayısız gülüşü… ve sen, herkesin anası Toprak. [pained] Bakın bana: Bir tanrı, tanrılardan neler çekiyor.",
         "Ancak yapayalnız kalınca konuşur. İlk sözleri göğedir: “Ey kutsal gök, hızlı kanatlı rüzgârlar, ırmakların kaynakları, deniz dalgalarının sayısız gülüşü… ve sen, herkesin anası Toprak: Bakın bana, bir tanrı tanrılardan neler çekiyor.”"),
 'G02': ("Erhat'a göre savunması iki kavrama dayanır: bilinç ve özgürlük. İnsana özgü, değişmez iki değer. [knowingly] Yani Prometeus'u insan yapan, bu ikisidir.", None),
 'G03': ("Çekiç seslerini duyan Okeanos'un kızları gelir. Prometeus onlara anlatır: Titanların savaşında annesi, Ayshilos'ta Toprak, öbür adıyla Temis, yani Adalet, ona geleceği söylemişti: Zafer gücün değil… kurnazlığın olacaktı.", None),
 'G05': ("Titanlar bu öğüdü küçümsedi; Prometeus Zeus'un yanına geçti. Kronos'u Tartaros'a gömen, onun öğütleri oldu. [knowingly] Erhat'ın andığı o rol, işte buydu.", None),
 'G07': ("Zeus tahta oturunca insanları hiç hesaba katmadı; onları yok edip yerine yeni bir soy yaratmak istiyordu. Buna karşı çıkan tek kişi, Prometeus oldu.", None),
 'G10': ("Ateşten önce insanlar, gözleri olup görmeyen, kulakları olup duymayan varlıklardı; mağaralarda karıncalar gibi yaşıyorlardı.", None),
 'G10b': ("Prometeus onlara yıldızları, sayıları, harfleri öğretti; hayvanları, gemiyi, ilacı, madenleri… [proudly] Tek sözle: İnsanlardaki bütün zanaatlar, Prometeus'tan gelir.",
          "Prometheus onlara yıldızları, sayıları, harfleri öğretti; hayvanları, gemiyi, ilacı, madenleri… “Tek sözle: İnsanlardaki bütün zanaatlar Prometheus'tan gelir.”"),
 'G13': ("[thoughtfully] Erhat'a göre bu bilinç, onda hem gurur, hem de bir katlanma duygusu doğurur. Biliyordu; ama bu kadarını beklemiyordu. [slowly] Yine de geri adım atmaz.", None),
 'H02': ("Erhat'a göre oyunun evreni, Zeus'un kurbanları, uşakları ve dalkavuklarıyla doludur. Hepsi buyruğunu yerine getirir; kimi isteyerek, kimi istemeyerek. [firmly] Tek başkaldıran, Prometeus'tur. Uşakları gördük; sırada bir dalkavuk var.", None),
 'H04': ("Yaşlı Titan Okeanos, iyi niyetle aracılık önerir: [softly] Kendini bil, der; tanrıların başında yeni bir tiran var. Dilini bu kadar azdırma. [coldly] Prometeus geri çevirir: Kendi başını derde sokma.", None),
 'H05': ("Periler bile ona, sözünü hiç sakınmıyorsun, der. [knowingly] Erhat'a göre Yunancadaki ifade, tam olarak dilin fazla özgür demektir. Başkaları, hiçbir umuda yer vermeden direnen bu tutumu gurur, hatta kibir sanır. [slowly] Oysa ona özgürlüğü sağlayan, bilincidir.",
         "Periler bile ona “sözünü hiç sakınmıyorsun” der. Erhat'a göre Yunancadaki ifade tam olarak “dilin fazla özgür” demektir. Başkaları, “hiçbir umuda yer vermeden” direnen bu tutumu gurur, hatta kibir sanır. Oysa ona özgürlüğü sağlayan bilincidir."),
 'H06': ("Sonra bir kurban gelir: boynuzlu, genç bir kız. Adı İyo. Zeus'un gönlü ona düşmüş, Hera'nın öfkesi peşine takılmıştı: Bir atsineği onu dünyanın dört bir yanına kovalıyordu.", None),
 'H07': ("[intrigued] Prometeus ona yolculuğunu anlatır: Bir boğazdan geçecek ve boğaz, bu geçişten adını alacak: Bosporos, yani inek geçidi. [knowingly] Ayshilos'un kastettiği Kırım'daki Kerç Boğazı'dır; ama başka anlatılar, aynı adı İstanbul Boğazı'na verir.",
         "Prometheus ona yolculuğunu anlatır: Bir boğazdan geçecek ve boğaz bu geçişten adını alacak: Bosporos, yani “inek geçidi.” Aiskhylos'un kastettiği Kırım'daki Kerç Boğazı'dır; ama başka anlatılar aynı adı İstanbul Boğazı'na verir."),
 'I05': ("Sonunda Zeus, habercisi Hermes'i gönderir; Erhat'ın deyişiyle, sanığı gözdağıyla sorguya çeken bir polis müdürü. Emir kısadır: Sırrı söyle.", None),
 'J02': ("Görünüşe bakılırsa cevap açık. Güç'ün sözünü hatırla: Zeus'tan başka kimse özgür değildir. Prometeus ise zincirde; ölümsüz olduğu için, canına kıyma özgürlüğü bile yok. [intrigued] Erhat sorar: Ama bakalım, gerçekten de öyle mi?",
         "Görünüşe bakılırsa cevap açık. Güç'ün sözünü hatırla: “Zeus'tan başka kimse özgür değildir.” Prometheus ise zincirde; ölümsüz olduğu için canına kıyma özgürlüğü bile yok. Erhat sorar: “Ama bakalım gerçekten de öyle mi?”"),
 'L02': ("Hesiodos'a göre geldi: Adı Herakles'ti. Kartalı okuyla vurdu ve Prometeus'u acısından kurtardı. [wryly] Tabii Zeus'un izniyle; oğlunun ünü artsın diye. Ayshilos'un Kurtulmuş Prometeus'u ise kayıp.", None),
 'L04': ("Erhat, onun izini Alman şair Göte'ye kadar sürmeyi önerir. Göte'nin şiirinde Titan, Zeus'a meydan okur ve insanları kendi suretinde yoğurur. Erhat'a göre bu şiirin anlamı şudur: Asıl yaratıcı, insanın kendisidir.",
         "Erhat, onun izini Alman şair Goethe'ye kadar sürmeyi önerir. Goethe'nin şiirinde Titan, Zeus'a meydan okur ve insanları kendi suretinde yoğurur. Erhat'a göre bu şiirin anlamı şudur: “Asıl yaratıcı, insanın kendisidir.”"),
 'K02': ("Ve kendi çağının düşünürlerinin, sanki sözleşmiş gibi verdiği cevabı aktarır: İnsan, başkaldıran yaratıktır. Doğaya ya da geleneğe boyun eğmeyi reddettiği an insan olmuştur; insan kalmak için de bu isyanı her gün yeniden başlatmalıdır.",
         "Ve kendi çağının düşünürlerinin sanki sözleşmiş gibi verdiği cevabı aktarır: “İnsan başkaldıran yaratıktır.” Doğaya ya da geleneğe boyun eğmeyi reddettiği an insan olmuştur; insan kalmak için de bu isyanı her gün yeniden başlatmalıdır."),
 'K04': ("Erhat'ın kuşağı bu görüşü öylesine benimser ki, gelenek süslerini üstünden atar. Ve ekler: Umuda karşı da ayaklandık; bugün, bu dünyada yaşamak istiyoruz.",
         "Erhat'ın kuşağı bu görüşü öylesine benimser ki, gelenek süslerini üstünden atar. Ve ekler: “Umuda karşı da ayaklandık”; bugün, bu dünyada yaşamak istiyoruz."),
 'K08a': ("[firmly] Erhat'ın en baştaki sorusunun cevabı da önsözde. Efsane Prometeus'a kâhin der. Erhat'ın yirminci yüzyılı kâhine inanmaz; ama aklıyla geleceği gören düşünürü tanır, onun kör iktidarların baskısına uğradığını da bilir.",
          "Erhat'ın en baştaki sorusunun cevabı da önsözde. Efsane Prometheus'a kâhin der. Erhat'ın XX. yüzyılı kâhine inanmaz; ama aklıyla geleceği gören düşünürü tanır, onun “kör iktidarların baskısına” uğradığını da bilir."),
 'K06': ("Erhat'a göre bu kuşağın tek ülküsü, insan olmaktı. [slowly] [reverently] Ve önsöz, bu ülkünün ilk temsilcisini tek cümleyle adlandırır: Bu ülkünün ilk temsilcisi… Prometeus'tur.",
         "Erhat'a göre bu kuşağın tek ülküsü insan olmaktı. Ve önsöz, bu ülkünün ilk temsilcisini tek cümleyle adlandırır: “Bu ülkünün ilk temsilcisi Prometheus'tur.”"),
 'M00': ("[warmly] Erhat ile Eyüboğlu, başta bu oyunun çevrilemeyeceğini, sahnelenemeyeceğini düşünüyormuş. Çevirdikçe yanıldıklarını anlamışlar… ve coşmuşlar. Dilekleri, Prometeus'u bir Türk tiyatrosunda görmekti.", None),
}

OVR.update({
 'C17': ("Ardından Titanlarla on yıllık bir savaş geldi; Zeus, yerin altındaki yüz kollu devleri savaşa sürdü ve Titanlar Tartaros'a kapatıldı. [thoughtfully] Erhat'a göre kaba güçler birbirini yok etmişti; meydanda akıldan başka güç kalmamıştı. Yıldırım elinde, Zeus tahta oturdu.", None),
 'E12': ("İlk ceza insanlara gelir: Hefaistos topraktan bir kız yoğurur, tanrılar onu armağanlarla süsler. Adı, Pandora'dır. Prometeus kardeşini uyarmıştı: Zeus'tan armağan alma. [wryly] Ama Epimeteus, yani “sonradan düşünen”, ancak iş işten geçince düşünür.", None),
 'G10b': ("Ateşten önce insanlar, gözleri olup görmeyen varlıklardı; mağaralarda karıncalar gibi yaşıyorlardı. Prometeus onlara yıldızları, sayıları, harfleri öğretti; hayvanları, gemiyi, ilacı, madenleri… [proudly] Tek sözle: İnsanlardaki bütün zanaatlar, Prometeus'tan gelir.",
          "Ateşten önce insanlar, gözleri olup görmeyen varlıklardı; mağaralarda karıncalar gibi yaşıyorlardı. Prometheus onlara yıldızları, sayıları, harfleri öğretti; hayvanları, gemiyi, ilacı, madenleri… “Tek sözle: İnsanlardaki bütün zanaatlar Prometheus'tan gelir.”"),
 'F08': ("Güç, cezanın amacını söyler: Prometeus, Zeus'un tiranlığına boyun eğmeyi öğrenecek… insanseverlikten vazgeçecek.", None),
 'I04': ("Kiminle evlenmemesi gerektiğini ise, yalnızca Prometeus biliyordu.", None),
 'K08b': ("[slowly] Belki de bu yüzden, yirmi beş yüzyıl önceki bu sanık, hâlâ insana benziyor.", None),
})
S = [x for x in S if x['id'] not in DROP]
for x in S:
    if x['id'] in OVR:
        t, a = OVR[x['id']]; x['tts'] = t; x['alt'] = a or mkalt(t)

# atıf kalıplarını çeşitlendir ("Erhat'a göre" ≤ 12)
VAR = {'C12': ("Erhat'a göre bu iki devrim", "Erhat bu iki devrimi ayırır: Bu iki devrim"),
       'E11': ("Erhat'a göre iki kez", "Erhat'ın okumasında, iki kez"),
       'F10': ("Erhat'a göre dramın özü", "Erhat'ın gözünde dramın özü"),
       'G13': ("Erhat'a göre bu bilinç", "Erhat'ın deyişiyle bu bilinç"),
       'H05': ("Erhat'a göre Yunancadaki", "Erhat'ın açıklamasıyla, Yunancadaki"),
       'K06': ("Erhat'a göre bu kuşağın", "Önsöze göre bu kuşağın")}
for x in S:
    if x['id'] in VAR:
        a, b = VAR[x['id']]
        for k in ('tts', 'alt'):
            assert a in x[k], (x['id'], k); x[k] = x[k].replace(a, b)
out = {'voice': 'Emrullah (DpEiQMnL9WxMsymCsjPY), eleven_v4', 'revizyon': 3,
       'not': "tts: seslendirme metni (ses etiketleri, Yunanca adlar okunuşa göre). alt: altyazı ve ekran metni (Erhat'ın yazımı). kaynak: iddianın dayanağı. Erhat = kaynak/onsoz_notlar.md maddeleri (s. v–xvi); Th. = Hesiodos, Theogonia; İG = Hesiodos, İşler ve Günler; ZVP = Aiskhylos, Zincire Vurulmuş Prometheus (dize numaraları Yunanca metne göre). Ekranda her Erhat iddiasında 'ERHAT · s. …' etiketi görünür (animatikte işlenir).",
       'segments': S}
json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
ids = [s['id'] for s in S]; assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
# süre: Sisifos'ta ölçülen hızla (karakter 13,91/sn saf konuşma; cümle arası ~1,0 sn; bölüm arası +2,2 sn)
c = collections.OrderedDict(); ch = 0
for s in S:
    t = re.sub(r'\[[^\]]*\]', '', s['tts']); n = len(re.sub(r'\s+', ' ', t).strip())
    c.setdefault(s['bolum'], [0, 0]); c[s['bolum']][0] += 1; c[s['bolum']][1] += n; ch += n
tot = 0
for k, (n, cc) in c.items():
    d = cc / 13.91 + n * 1.0 + 2.2; tot += d; print(f'{k:28s} {n:3d} cümle {d:6.0f} sn')
print(len(S), 'cümle; tahmini', f'{int(tot // 60)}:{tot % 60:04.1f}', '(+ son 15 sn bitiş ekranı)')
print('Erhat geçişi:', sum(s['tts'].count('Erhat') for s in S), " 'Erhat'a göre':", sum(s['tts'].count("Erhat'a göre") for s in S), " 'Peki':", sum(s['tts'].count('Peki') for s in S), ' [curious]:', sum(s['tts'].count('[curious]') for s in S))
