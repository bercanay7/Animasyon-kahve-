# senaryo rev 2: (id, bölüm, tts, alt veya None, kaynak)
import json, re, sys
TTS2ALT = [('Prometeus', 'Prometheus'), ('Ayshilos', 'Aiskhylos'), ('Teogonia', 'Theogonia'), ('Gaya', 'Gaia'), ('Kaos', 'Khaos'),
           ('Rea', 'Rheia'), ('Hefaistos', 'Hephaistos'), ('Epimeteus', 'Epimetheus'), ('Klimene', 'Klymene'), ('Otris', 'Othrys'),
           ('Olimpos', 'Olympos'), ('Tetis', 'Thetis'), ('Göte', 'Goethe'), ('Meri Şeli', 'Mary Shelley'), ('Frankenştayn', 'Frankenstein'),
           ('Openhaymır', 'Oppenheimer'), ('İo', 'Io'), ('Mekoni', 'Mekone'), ('Afrodit', 'Aphrodite'), ('Olimposlu', 'Olympos'), ('Kafka', 'Kafka')]
def mkalt(t):
    a = re.sub(r'\[[^\]]*\]\s*', '', t)
    for x, y in TTS2ALT: a = a.replace(x, y)
    return a
S = []
def seg(i, b, tts, kaynak, alt=None): S.append({'id': i, 'bolum': b, 'tts': tts, 'alt': alt or mkalt(tts), 'kaynak': kaynak})
B = 'Açılış'
seg('A01', B, "[slowly] [deep voice] Tanrılardan ateşi çalıp insanlara veren bir Titan düşün.", "Th. 565–569; ZVP 7–8, 107–111")
seg('A02', B, "[ominous] Cezası: dünyanın ucunda, çıplak bir kayaya zincirlenmek.", "ZVP 1–5")
seg('A03', B, "[darkly] Her gün bir kartal iner, karaciğerini parçalar. Gece karaciğer yeniden büyür… [slowly] ve sabah, kartal yine gelir.", "Th. 523–525; ZVP 1021–1025")
seg('A04', B, "[mysterious] Adı… Prometeus.", "")
seg('A05', B, "[curious] Peki Zeus'u bu kadar öfkelendiren, gerçekten bir avuç ateş miydi?", "soru; cevabı D07–D10, E07–E11, K07")
seg('A06', B, "[thoughtfully] Bu oyunu Türkçeye çevirenlerden Azra Erhat, şaşırtıcı bir şey söyler. [mysterious] Ona göre o kayada asıl tutsak olan… Prometeus değildi.", "Erhat xiv2, xiv5 (cevabı J04–J06)")

B = 'Bir önsözün sorusu'
seg('B01', B, "[curious] Sahnede yalnızca tanrıların konuştuğu bir oyun, insanı anlatabilir mi?", "Erhat v4, xi2")
seg('B02', B, "Atinalı tragedya yazarı Ayshilos, Prometeus'u üç oyunda anlattı. Bize yalnızca biri ulaştı: Zincire Vurulmuş Prometeus.", "Erhat v2")
seg('B03', B, "Öbür ikisi kayıp; adları eski bir oyun listesinde duruyor. Kurtulmuş Prometeus… ve Ateş Taşıyan Prometeus.", "Erhat v2",
    "Öbür ikisi kayıp; adları eski bir oyun listesinde duruyor: Kurtulmuş Prometheus… ve Ateş Taşıyan Prometheus.")
seg('B04', B, "Kimi okurlar, bu oyunda yalnızca tanrıların rol aldığına dikkat çeker. [warmly] Ama oyunu Sabahattin Eyüboğlu'yla birlikte Türkçeye çeviren klasik filolog Azra Erhat'a göre, oyunun asıl konusu insandır.", "Erhat v4, xi2, xv4")
seg('B05', B, "Ona göre oynanan dram, insanlığın dramıdır. Prometeus da, Ayshilos'tan bu yana, insanı en iyi temsil eden kahramandır. Onun deyişiyle: insan dostu, tanrı düşmanı.", "Erhat v4, v5, xi2",
    "Ona göre oynanan dram, insanlığın dramıdır. Prometheus da, Aiskhylos'tan bu yana insanı en iyi temsil eden kahramandır. Onun deyişiyle: “insan dostu, tanrı düşmanı.”")
seg('B06', B, "[intrigued] Ve Erhat iki soru sorar. Prometeus, ne bakımdan insandır? Ve nasıl oldu da, İsa'dan önce beşinci yüzyılda yaşamış bir yazar, yirminci yüzyılın başkaldıran insanını yaratabildi?", "Erhat xi2, vi7",
    "Ve Erhat iki soru sorar: Prometheus ne bakımdan insandır? Ve nasıl oldu da İsa'dan önce V. yüzyılda yaşamış bir yazar, XX. yüzyılın başkaldıran insanını yaratabildi?")
seg('B07', B, "Erhat bu soruları, bin dokuz yüz altmış yedide yazdığı önsözde sorar. Ve cevabı ararken, önce çok daha geriye gider: tanrıların, taht için verdiği kavgaya.", "Erhat vi6, vi9, xvi2",
    "Erhat bu soruları 1967'de yazdığı önsözde sorar. Ve cevabı ararken önce çok daha geriye gider: tanrıların, taht için verdiği kavgaya.")

B = 'Gökteki darbeler'
seg('C01', B, "[curious] Tanrıların kralı Zeus, o tahta nasıl oturmuştu?", "")
seg('C02', B, "Erhat'a göre hem efsanenin, hem de oyunun merkezinde, bugün “hükümet darbesi” diyebileceğimiz bir olay vardır. Bir kuşak, kendinden öncekini devirir ve iktidarı ele geçirir.", "Erhat vi9",
    "Erhat'a göre hem efsanenin hem de oyunun merkezinde, bugün “hükümet darbesi” diyebileceğimiz bir olay vardır: Bir kuşak, kendinden öncekini devirir ve iktidarı ele geçirir.")
seg('C03', B, "Bu hikâyeyi Ayshilos'tan bir iki yüzyıl önce, şair Hesiodos, Teogonia adlı şiirinde anlatmıştı.", "Erhat vii1, vii3")
seg('C04', B, "Başlangıçta Kaos vardı. Ondan Toprak Ana, Gaya doğdu; Gaya da kendine bir eş yarattı: Gök, yani Uranos. [darkly] Ama Uranos, Gaya'dan doğan devlerden tiksindi ve her birini, doğar doğmaz, annelerinin karnına geri tıktı.", "Erhat vii3; Th. 116–160")
seg('C06', B, "Acılar içindeki Gaya, çelikten bir tırpan yapıp çocuklarına verdi. Hiçbiri babasına el kaldırmaya yanaşmadı… [slowly] en küçükleri Kronos hariç.", "Erhat vii4; Th. 160–172")
seg('C07', B, "[tense] Kronos gece pusuya yattı. Uranos, Gaya'nın üstüne eğildiği anda, tırpanı savurdu ve onu iğdiş etti.", "Erhat vii4; Th. 174–182")
seg('C08', B, "[wryly] Hesiodos bu noktada, deniz köpüğünden doğan Afrodit'in hikâyesine dalar gider. Erhat ise bu sahnede başka bir şey görür: tanrılar tarihinde bir devrim.", "Erhat vii5")
seg('C09', B, "[darkly] Ama bu devrim de, kendi çocuklarını yedi. Hem de kelimenin tam anlamıyla. Kronos, oğullarından birinin onu devireceğini biliyordu; çocuklarını doğar doğmaz yuttu.", "Erhat vii6, viii1; Th. 459–467",
    "Ama bu devrim de kendi çocuklarını yedi. Hem de kelimenin tam anlamıyla: Kronos, oğullarından birinin onu devireceğini biliyordu; çocuklarını doğar doğmaz yuttu.")
seg('C10', B, "Karısı Rea, son oğlunu Girit'e kaçırdı ve Kronos'a, kundağa sarılmış bir taş yutturdu. [slowly] O çocuk, Zeus'tu. Büyüdü, babasına kardeşlerini kusturdu ve onu tahttan indirdi.", "Erhat viii1; Th. 468–500")
seg('C12', B, "[thoughtfully] Erhat'a göre bu iki darbe aynı şey değildir. Birincisi, salt kaba kuvvetti. İkincisi ise, bir akıl ve hesap işiydi: Bu kez Zeus'a, kaba kuvvetin acısını tatmış Uranos ile Gaya kılavuzluk etmişti.", "Erhat viii2, viii3",
    "Erhat'a göre bu iki darbe aynı şey değildir. Birincisi salt kaba kuvvetti. İkincisi ise “bir akıl ve hesap işi”ydi: Bu kez Zeus'a, kaba kuvvetin acısını tatmış Uranos ile Gaia kılavuzluk etmişti.")
seg('C13', B, "Erhat'ın deyişiyle, birinci devrim kaba kuvvetin kendi kendine yenilmesiydi. İkincisi, kaba kuvvetin akılla yenilmesi.", "Erhat viii4",
    "Erhat'ın deyişiyle birinci devrim, kaba kuvvetin kendi kendine yenilmesiydi; ikincisi, “kaba kuvvetin akılla yenilmesi.”")
seg('C14', B, "[knowingly] Ve Erhat bir ayrıntıyı hatırlatır: Prometeus da işte bu devrimde rol oynamıştı. Nasıl mı? Ona birazdan geleceğiz.", "Erhat viii1")
seg('C15', B, "Sonra Titanlarla on yıl süren bir savaş geldi. Zeus, Gaya'nın öğüdüyle yerin altındaki yüz kollu devleri savaşa sürdü. [intense] Yer sarsıldı, denizler altüst oldu… ve Titanlar, Tartaros'a kapatıldı.", "Erhat viii6, ix1; Th. 617–735")
seg('C17', B, "Erhat'a göre Zeus artık aklı da, kol gücünü de kendi kişiliğinde birleştirmişti. Tahta oturdu ve dünyayı paylaştırmaya girişti.", "Erhat ix1, ix2")
seg('C18', B, "[ominous] [slowly] Bu paylaşmada karşısına dikilen tek engel… Prometeus'tu.", "Erhat ix2")

B = 'Aklın tekeli'
seg('D01', B, "[curious] Peki Zeus, bir Titan ailesine neden özel bir kin besliyordu?", "Erhat ix5")
seg('D02', B, "Prometeus, Titan İapetos ile, Okeanos'un kızı Klimene'nin oğluydu. Dört kardeştiler: Atlas, Menoitios, Prometeus ve Epimeteus.", "Erhat ix4; Th. 507–511")
seg('D03', B, "[darkly] Dördünün de sonu tüyler ürperticiydi. Zeus, Atlas'ı dünyanın ucuna dikip göğü omuzlarına yükledi. Menoitios'u yıldırımla çarpıp yerin dibine gömdü.", "Erhat ix4; Th. 514–520")
seg('D04', B, "Prometeus'u bir sütuna zincirleyip karaciğerini kartala yedirdi. Epimeteus'a ise bir “armağan” gönderdi. O armağana da geleceğiz.", "Erhat ix4; Th. 511–514, 521–525")
seg('D05', B, "Erhat sorar: Neden bu eşi görülmemiş cezalar? Titan oldukları için mi? [firmly] Hayır.", "Erhat ix5")
seg('D06', B, "Erhat'a göre bu kardeşlerin dördü de kafa gücünden pay almıştı. Akılca üstündüler. Bununla övünüyor, Zeus'a karşı gelmeye yelteniyorlardı.", "Erhat ix5",
    "Erhat'a göre bu kardeşlerin dördü de kafa gücünden pay almıştı. Akılca üstündüler; bununla övünüyor, Zeus'a karşı gelmeye yelteniyorlardı.")
seg('D07', B, "[slowly] Oysa, Erhat'ın deyişiyle: Akıl gücüyse, Zeus'un tekelindedir. Zeus tahtı bu güçle kazanmıştı. Ve Erhat ekler: Bu gücü başkasında görmek, içinde dinmez bir öfke doğurur.", "Erhat ix5, x1 (kısa alıntılar)",
    "Oysa, Erhat'ın deyişiyle: “Akıl gücüyse Zeus'un tekelindedir.” Zeus tahtı bu güçle kazanmıştı. Ve Erhat ekler: Bu gücü başkasında görmek, içinde “dinmez bir öfke” doğurur.")
seg('D08', B, "Prometeus da bu öfkeyi durmadan körükler. Sivri aklını ve geleceği görme gücünü, Zeus'u aldatmak, kuşkulandırmak, küçük düşürmek için kullanır.", "Erhat x2")
seg('D09', B, "Adı bile bunu söyler: Prometeus, “önceden gören” demektir. O bir kâhindir. Gaya, Kronos'a devrileceğini nasıl haber verdiyse, Prometeus da Zeus'un bir gün tahtından düşeceğini bilir.", "Erhat x4")
seg('D10', B, "Erhat'a göre burada, Hesiodos'un pek üstünde durmadığı ama Ayshilos'un alabildiğine işlediği bir tema vardır: üçüncü devrimin hazırlanması.", "Erhat x3",
    "Erhat'a göre burada, Hesiodos'un pek üstünde durmadığı ama Aiskhylos'un alabildiğine işlediği bir tema vardır: “Üçüncü devrimin hazırlanması.”")
seg('D11', B, "[ominous] [slowly] Uranos devrilmişti. Kronos devrilmişti. Sıra kime gelecekti?", "anlatıcının köprüsü (Erhat x3–x4)")

B = "Mekone'deki hile"
seg('E01', B, "[curious] Eski Yunanlar kurban kestiğinde, neden eti kendileri yer, tanrılara yalnızca kemikleri yakardı?", "Th. 556–557")
seg('E03', B, "Cevap, Prometeus'tan uzun uzun söz eden ilk şair Hesiodos'ta. Ona göre bir gün tanrılar ve insanlar, Mekoni denen yerde paylarını belirlemek için bir araya geldi. Prometeus büyük bir öküz kesti ve ikiye ayırdı.", "Th. 535–538")
seg('E04', B, "Bir yanda, öküzün midesine gizlenmiş etler. Öbür yanda, parlak bir yağ tabakasına sarılmış… [slowly] çıplak kemikler.", "Th. 538–541")
seg('E05', B, "[wryly] “Hangisini istersen seç,” dedi Zeus'a. Zeus yağlı payı aldı ve altından beyaz kemikler çıktı. O günden beri insanlar etin kendine düşen payını yer, sunaklarda tanrılara kemik yakar.", "Th. 548–557",
    "“Hangisini istersen seç,” dedi Zeus'a. Zeus yağlı payı aldı ve altından beyaz kemikler çıktı. O günden beri insanlar etin kendine düşen payını yer, sunaklarda tanrılara kemik yakar.")
seg('E07', B, "[thoughtfully] Erhat'a göre bu, bir kurban geleneğinin nereden geldiğini açıklayan bir efsanedir. Ama asıl önemi başkadır: Prometeus, baştan beri insanlardan yanadır.", "Erhat x5")
seg('E08', B, "Onlara dayanarak Titanların öcünü almak, Olimpos tanrılarının yerine insanların egemenliğini getirmek ister. Erhat'ın deyişiyle: yeni bir devrimin hazırlayıcısıdır.", "Erhat x5 (kısa alıntı)",
    "Onlara dayanarak Titanların öcünü almak, Olympos tanrılarının yerine insanların egemenliğini getirmek ister. Erhat'ın deyişiyle: “Yeni bir devrimin hazırlayıcısıdır.”")
seg('E09', B, "[wryly] Zeus, bile bile aldanır; ama oldubittiyi önleyemez. [darkly] Bu onur yarasının öcünü almak için, ateşi insanlardan esirger.", "Erhat x5; Th. 550–552, 562–564")
seg('E10', B, "Prometeus onu bir kez daha aldatır. Ateşi, içi boş bir rezene sapına gizleyip insanlara götürür.", "Erhat x5; Th. 565–567; İG 50–52")
seg('E11', B, "[ominous] Erhat'a göre iki kez küçük düşürülen tanrıların kralı, artık kaba kuvvete başvurmak zorundaydı.", "Erhat x5")
seg('E12', B, "İlk ceza insanlara geldi. Hefaistos, topraktan bir kız biçimlendirdi. Bütün tanrılar ona birer armağan verdi; Hermes ise diline yalanı koydu. Adı, Pandora'ydı.", "İG 57–82; Th. 570–584")
seg('E13', B, "Prometeus kardeşini uyarmıştı: Zeus'tan asla armağan kabul etme. [wryly] Ama Epimeteus, yani “sonradan düşünen”, ancak iş işten geçince düşündü.", "İG 83–89")
seg('E14', B, "[ominous] Pandora büyük küpün kapağını kaldırdı. Hastalıklar, acılar, dertler dünyaya yayıldı. [softly] İçeride yalnızca bir şey kaldı: Umut.", "İG 90–99")
seg('E15', B, "Hesiodos hikâyeyi Zeus'tan yana anlatır: Zeus'un aklını aldatmak mümkün değildir. [knowingly] Ama Erhat satır aralarında başka bir şey okur: insanların gözünde aldatılmış, küçük düşmüş bir tanrı. Ona göre akıl gücü, artık tanrılardan insanlara geçmiştir.", "Th. 613–616; İG 105; Erhat x6, xi1")

B = 'Duruşma'
seg('F01', B, "[curious] Peki aynı hikâyeyi, yüzyıllar sonra Atinalı bir şair anlatınca ne değişti?", "Erhat vii1")
seg('F02', B, "Erhat'a göre Hesiodos ile Ayshilos, buraya kadar aşağı yukarı aynı efsaneleri izler. Ama iş Prometeus'a gelince, iki şairin yorumu büsbütün değişir.", "Erhat ix3")
seg('F03', B, "Ve Erhat, oyunu okumak için ilginç bir yol önerir. Bugün bir yazar bu olayı sahneye koysa, bir duruşma kurardı: sanığı, tanıkları ve yargıçlarıyla. Ona göre bu oyunu, Kafka'nın Dava romanını okur gibi okumalıyız.", "Erhat xi4 (Erhat'ın andığı ad: Duruşma)")
seg('F05', B, "[slowly] Öyleyse duruşma başlasın. Sanık: Prometeus. Suçu: ateşi çalıp insanlara vermek, ve tanrıların kurduğu düzene karşı gelmek.", "Erhat xi3",
    "Öyleyse duruşma başlasın. Sanık: Prometheus. Suçu: ateşi çalıp insanlara vermek ve tanrıların kurduğu düzene karşı gelmek.")
seg('F06', B, "Sahne: dünyanın ucunda, İskit ülkesinin ıssız bir uçurumu. Zeus'un iki uşağı sanığı sürükleyerek getirir: Kratos ve Bia, yani Güç ve Zor. Erhat onlara, günümüzün diliyle, polis der.", "ZVP 1–87; Erhat xv3 (kısa alıntı)",
    "Sahne: dünyanın ucunda, İskit ülkesinin ıssız bir uçurumu. Zeus'un iki uşağı sanığı sürükleyerek getirir: Kratos ve Bia, yani Güç ve Zor. Erhat onlara “günümüzün diliyle” polis der.")
seg('F07', B, "Zincirleri vurmak, demirci tanrı Hefaistos'a düşer. Bu işi istemeyerek yapar; zincirlediği kendi akrabasıdır. Ama yine de vurur. [thoughtfully] Çünkü, onun deyişiyle: Yeni iktidara gelen her hükümdar serttir.", "ZVP 14–19, 35, 39 (kendi çevirimiz)",
    "Zincirleri vurmak, demirci tanrı Hephaistos'a düşer. Bu işi istemeyerek yapar; zincirlediği kendi akrabasıdır. Ama yine de vurur. Çünkü, onun deyişiyle: “Yeni iktidara gelen her hükümdar serttir.”")
seg('F08', B, "Güç ise, suçun adını koyar: insanseverlik. Bugünkü “filantropi” kelimesinin bilinen en eski kullanımlarından biri, bu oyundadır.", "ZVP 11, 28 (philanthrōpos tropos)")
seg('F09', B, "[coldly] Ve ekler: Tanrılar arasında, Zeus'tan başka hiç kimse özgür değildir.", "ZVP 49–50 (kendi çevirimiz); Erhat xiii5",
    "Ve ekler: “Tanrılar arasında Zeus'tan başka hiç kimse özgür değildir.”")
seg('F10', B, "[knowingly] Bu cümleyi aklında tut. Erhat'a göre dramın özü tam da budur: özgürlük ve kölelik.", "Erhat xiii1")
seg('F10b', B, "[slowly] Ve Erhat'ın dikkat çektiği bir ayrıntı: Bütün bu sahne boyunca Prometeus tek söz etmez. Kayaya çakılmaya, zincire, hakaretlere, sessizce katlanır.", "Erhat xv3; ZVP 1–87")
seg('F11', B, "[mocking] Giderken Güç alay eder: Sana boşuna “önceden gören” demişler. Asıl şimdi, bu zincirden kurtulmanın yolunu önceden görecek birine ihtiyacın var.", "ZVP 85–87 (kendi çevirimiz)",
    "Giderken Güç alay eder: “Sana boşuna ‘önceden gören’ demişler. Asıl şimdi, bu zincirden kurtulmanın yolunu önceden görecek birine ihtiyacın var.”")
seg('F13', B, "[softly] Sonra hepsi gider. Yapayalnız kalan Prometeus göğe seslenir: [reverently] Ey kutsal gök, ey hızlı kanatlı rüzgârlar, ırmakların kaynakları, deniz dalgalarının sayısız gülüşü… ve sen, herkesin anası Toprak. [pained] Bakın, bir tanrı, tanrılardan neler çekiyor.", "ZVP 88–92 (kendi çevirimiz)",
    "Sonra hepsi gider. Yapayalnız kalan Prometheus göğe seslenir: “Ey kutsal gök, ey hızlı kanatlı rüzgârlar, ırmakların kaynakları, deniz dalgalarının sayısız gülüşü… ve sen, herkesin anası Toprak: Bakın, bir tanrı tanrılardan neler çekiyor.”")

B = 'Savunma'
seg('G01', B, "[curious] Peki sanık, kendini nasıl savunur?", "Erhat xi5")
seg('G02', B, "Erhat'a göre Prometeus'un savunması iki kavrama dayanır: bilinç ve özgürlük.", "Erhat xi5")
seg('G03', B, "Çekiç seslerini duyan Okeanos'un kızları, denizin derinliklerinden gelir. Prometeus onlara anlatır: Titanlarla Zeus savaşırken, annesi Toprak Ana ona geleceği söylemişti: Zafer, gücün ve zorun değil, kurnazlığın olacaktı.", "ZVP 128–135, 199–213; Erhat x4 (Aiskhylos'ta anası Gaia-Themis)")
seg('G05', B, "Titanlar bu öğüdü küçümsedi. Prometeus da Zeus'un yanına geçti. Kronos'u Tartaros'un karanlığına gömen, onun öğütleri oldu. [knowingly] Erhat'ın sözünü ettiği rol, işte buydu.", "ZVP 214–221; Erhat viii1")
seg('G06', B, "[bitterly] Şimdi ise tahta çıkardığı tanrının zincirindeydi. Prometeus bunu tek cümleyle açıklar: Tiranlığın bir hastalığı vardır; dostlarına güvenmez.", "ZVP 221–225 (kendi çevirimiz)",
    "Şimdi ise tahta çıkardığı tanrının zincirindeydi. Prometheus bunu tek cümleyle açıklar: “Tiranlığın bir hastalığı vardır: dostlarına güvenmez.”")
seg('G07', B, "Zeus tahta oturur oturmaz tanrılara görevlerini dağıttı. Ama zavallı insanları hiç hesaba katmadı; onları yok edip yerine yeni bir soy yaratmak istiyordu. Buna karşı çıkan tek kişi, Prometeus oldu.", "ZVP 228–236")
seg('G08', B, "İnsanları kurtarmakla da kalmadı. Ölümlerini önceden görmelerini engelledi; içlerine kör umutlar yerleştirdi. [warmly] Sonra da ateşi verdi.", "ZVP 248–254")
seg('G09', B, "[intrigued] Erhat burada sorar: Ateşi tanrılardan çalıp insanlara vermek, ne demektir? Ona göre başkaları bunu bir efsane olarak bırakmıştı. Ayshilos ise ondan, uygarlığın tarihini çıkarır.", "Erhat xv2 (kısa alıntı)",
    "Erhat burada sorar: “Ateşi tanrılardan çalıp insanlara vermek ne demektir?” Ona göre başkaları bunu bir efsane olarak bırakmıştı. Aiskhylos ise ondan uygarlığın tarihini çıkarır.")
seg('G10', B, "Ateşten önce insanlar, gözleri olup görmeyen, kulakları olup duymayan varlıklardı; mağaralarda karıncalar gibi yaşıyorlardı. Prometeus onlara yıldızları, sayıları, harfleri öğretti. Hayvanları evcilleştirmeyi, gemiyi, ilacı, madenleri… [proudly] Tek sözle: İnsanlardaki bütün sanatlar, Prometeus'tan gelir.", "ZVP 447–506 (kendi çevirimiz)",
    "Ateşten önce insanlar, gözleri olup görmeyen, kulakları olup duymayan varlıklardı; mağaralarda karıncalar gibi yaşıyorlardı. Prometheus onlara yıldızları, sayıları, harfleri öğretti. Hayvanları evcilleştirmeyi, gemiyi, ilacı, madenleri… “Tek sözle: İnsanlardaki bütün sanatlar Prometheus'tan gelir.”")
seg('G11', B, "[firmly] Ve sanık suçunu inkâr etmez. Erhat'ın dediği gibi, bugünkü bir sanığın söyleyeceğini söyler: Ne yaptımsa, bile bile yaptım.", "Erhat xi5 (kısa alıntı)",
    "Ve sanık suçunu inkâr etmez. Erhat'ın dediği gibi, bugünkü bir sanığın söyleyeceğini söyler: “Ne yaptımsa bile bile yaptım.”")
seg('G12', B, "Oyundaki sözleriyle: İsteyerek, isteyerek suç işledim; inkâr etmeyeceğim.", "ZVP 266 (kendi çevirimiz)",
    "Oyundaki sözleriyle: “İsteyerek, isteyerek suç işledim; inkâr etmeyeceğim.”")
seg('G13', B, "[thoughtfully] Erhat'a göre bu bilinç, onda hem bir gurur, hem de katlanma gücü doğurur. Başına gelecek her şeyi önceden biliyordu. Ve yine de yaptı.", "Erhat xii1; ZVP 101–105")

B = 'Tanıklar'
seg('H01', B, "[curious] Bu duruşmada tanıklık edenler kimlerdir?", "Erhat xi4, xiv1")
seg('H02', B, "Erhat'a göre oyunun evreni üç tür varlıkla doludur: Zeus'un kurbanları, uşakları ve dalkavukları.", "Erhat xiv1")
seg('H03', B, "Uşakları gördük: Güç, Zor ve Hefaistos. Sırada bir dalkavuk var: deniz tanrısı Okeanos.", "Erhat xiv1")
seg('H04', B, "Okeanos, Prometeus'a boyun eğmesini öğütler. “Kendini bil,” der. “Tanrıların başında yeni bir hükümdar var. Boşuna direnme.”", "ZVP 309–310, 322–323 (kendi çevirimiz)")
seg('H05', B, "Periler de onu anlamakta zorlanır: Sözünü hiç sakınmıyorsun, derler. [knowingly] Erhat'a göre Yunancadaki ifade, tam olarak “dilin fazla özgür” demektir.", "ZVP 180; Erhat xiii1")
seg('H06', B, "Sonra bir kurban gelir: boynuzlu, genç bir kız. Adı İo. Zeus'un gönlü ona düşünce, Hera'nın öfkesi de üstüne çökmüştü. Şimdi bir atsineği, onu durmadan dünyanın dört bir yanına kovalıyordu.", "ZVP 561–600, 640–686; Erhat xiv1 (Io: Zeus'un kurbanı)",
    "Sonra bir kurban gelir: boynuzlu, genç bir kız. Adı Io. Zeus'un gönlü ona düşünce, Hera'nın öfkesi de üstüne çökmüştü. Şimdi bir atsineği onu durmadan dünyanın dört bir yanına kovalıyordu.")
seg('H07', B, "[curious] Prometeus ona yolculuğunun haritasını çıkarır. Yolu bir boğazdan geçecek; o boğaz da onun adıyla anılacaktır: Bosporos. Yani, inek geçidi.", "ZVP 700–741 (özellikle 732–734)",
    "Prometheus ona yolculuğunun haritasını çıkarır. Yolu bir boğazdan geçecek; o boğaz da onun adıyla anılacaktır: Bosporos, yani “inek geçidi.”")
seg('H08', B, "Ayshilos'un sözünü ettiği, Kırım'daki bir boğazdır. Ama başka antik anlatılar, aynı adı İstanbul Boğazı'na verir: İo'nun yüzerek geçtiği yer.", "ZVP 729–734 (Kimmer Bosporosu); Apollodoros II.1.3")
seg('H09', B, "[softly] İo, acısına dayanamayıp ölmeyi diler. Prometeus'un cevabı ağırdır: Ben ölemem bile. İşkencem, Zeus tahtından düşmedikçe bitmeyecek.", "ZVP 747–756; Erhat xii3 (kendi çevirimiz)")
seg('H10', B, "Ve ekler: İo'nun soyundan, on üç kuşak sonra, onu bu zincirden kurtaracak bir okçu doğacak.", "ZVP 771–774, 871–873")

B = 'Sır'
seg('I01', B, "[curious] Zincirdeki bir sanık, yargıcını nasıl korkutabilir?", "")
seg('I02', B, "Prometeus bir sır biliyordu. Zeus bir gün bir evlilik yapacaktı. Ve o evlilikten, babasından daha güçlü bir oğul doğacaktı.", "ZVP 764–768, 907–912")
seg('I03', B, "[slowly] Tıpkı Uranos'un ve Kronos'un başına gelen gibi. Erhat'ın sözünü ettiği üçüncü devrim, işte buydu: Zeus'u sürekli kuşku içinde tutan bir bilgi.", "Erhat x3, x4; ZVP 910–914")
seg('I04', B, "Kiminle evlenmemesi gerektiğini, yalnızca Prometeus biliyordu. Ayshilos o adı vermez; başka anlatılar, onun deniz perisi Tetis olduğunu söyler.", "ZVP 913–925; Pindaros, İsthmia 8.26–47")
seg('I05', B, "Sonunda Zeus, habercisi Hermes'i gönderir. Erhat ona, sanığı gözdağıyla sorguya çeken bir polis müdürü der. Emir kısadır: Sırrı söyle.", "ZVP 944–952; Erhat xv3")
seg('I06', B, "[defiantly] Prometeus güler: Siz yeni tanrılar, kulelerinizde acı görmeyeceğinizi sanıyorsunuz. Ben oradan iki hükümdarın atıldığını gördüm. Üçüncüsünün düşüşünü de göreceğim.", "ZVP 953–959 (kendi çevirimiz)",
    "Prometheus güler: “Siz yeni tanrılar, kulelerinizde acı görmeyeceğinizi sanıyorsunuz. Ben oradan iki hükümdarın atıldığını gördüm. Üçüncüsünün düşüşünü de göreceğim.”")
seg('I07', B, "Hermes'in tehditlerine cevabı tek cümledir: Senin uşaklığınla, benim felaketimi değişmem.", "ZVP 966–967 (kendi çevirimiz)",
    "Hermes'in tehditlerine cevabı tek cümledir: “Senin uşaklığınla benim felaketimi değişmem.”")
seg('I08', B, "Hermes, Zeus'un “eyvah” demeyi bilmediğini söyler. [calmly] Prometeus'un cevabı: Yaşlanan zaman, her şeyi öğretir.", "ZVP 979–981 (kendi çevirimiz)",
    "Hermes, Zeus'un “eyvah” demeyi bilmediğini söyler. Prometheus'un cevabı: “Yaşlanan zaman her şeyi öğretir.”")
seg('I09', B, "Hermes, perilere oradan gitmelerini söyler. Ama periler kalır. İhanetten nefret etmeyi öğrendiklerini söyleyip, Prometeus'un yanında dururlar.", "ZVP 1058–1070",
    "Hermes, perilere oradan gitmelerini söyler. Ama periler kalır; ihanetten nefret etmeyi öğrendiklerini söyleyip Prometheus'un yanında dururlar.")
seg('I10', B, "[intense] Ve Zeus'un öfkesi iner. Yer sarsılır, gök gürler, şimşekler çakar. Rüzgârlar birbirine girer; gök, denize karışır.", "ZVP 1080–1090")
seg('I11', B, "[pained] [slowly] Prometeus'un son sözleri, göğe ve anasınadır: Görüyor musun, ne haksızlıklara uğruyorum.", "ZVP 1091–1093 (kendi çevirimiz)",
    "Prometheus'un son sözleri göğe ve anasınadır: “Görüyor musun, ne haksızlıklara uğruyorum.”")
seg('I12', B, "[firmly] Başta tek söz etmeyen Prometeus, dünya başına yıkılana dek konuşmayı sürdürmüştür. Son söz onundur. [slowly] Erhat'a göre Ayshilos'un söylemek istediği de budur: Kıyamet de kopsa, son söz özgür düşüncenindir.", "Erhat xv3 (kısa alıntı)",
    "Başta tek söz etmeyen Prometheus, dünya başına yıkılana dek konuşmayı sürdürmüştür. Son söz onundur. Erhat'a göre Aiskhylos'un söylemek istediği de budur: “Kıyamet de kopsa son söz özgür düşüncenindir.”")

B = 'Asıl tutsak'
seg('J01', B, "[curious] Peki bu duruşmada, gerçekten tutsak olan kimdi?", "Erhat xiii4")
seg('J02', B, "Görünüşe bakılırsa cevap açık. Zeus evrenin efendisidir. Prometeus ise zincirde: ölümsüz olduğu için, canına kıyma özgürlüğü bile yok.", "Erhat xiii4")
seg('J03', B, "[curious] Erhat sorar: Ama bakalım, gerçekten öyle mi?", "Erhat xiii4 (kısa alıntı)",
    "Erhat sorar: “Ama bakalım gerçekten de öyle mi?”")
seg('J04', B, "[slowly] [reverently] Ve cevap verir: Gerçekte Zeus köle, Prometeus özgürdür.", "Erhat xiv2 (kısa alıntı)",
    "Ve cevap verir: “Gerçekte Zeus köle, Prometheus özgürdür.”")
seg('J05', B, "Çünkü Zeus'u yıkımdan kurtarabilecek tek kişi, aklın taşıyıcısı Prometeus'tur. Bütün uşaklarına, dalkavuklarına rağmen Zeus, bir çocuk gibi zayıf ve çaresizdir.", "Erhat xiv5")
seg('J06', B, "[knowingly] Erhat'ın deyişiyle: Zeus, tutukladığı düşmanının elinde tutukludur aslında.", "Erhat xiv5 (kısa alıntı)",
    "Erhat'ın deyişiyle: “Zeus tutukladığı düşmanının elinde tutukludur aslında.”")
seg('J07', B, "Erhat'a göre Ayshilos'un asıl dersi şudur: Akıl gücü, kaba güçten üstündür. Özgür düşünce tutuklanamaz, susturulamaz.", "Erhat xiv3")
seg('J08', B, "Ve akılla kurulan bir yönetim, akla ve özgür düşünceye sırt çevirdiğinde, zayıflar ve devrilme tehlikesiyle yüz yüze gelir.", "Erhat xiv4")
seg('J08b', B, "Efsane Prometeus'a kâhin der. Erhat'a göre bizim çağımız kâhine inanmaz; ama aklıyla geleceği gören düşünürü tanır. Ve bu hizmetinin karşılığında, kör iktidarların baskısına uğradığını da bilir.", "Erhat xiv6, xv1 (kısa alıntı)",
    "Efsane Prometheus'a kâhin der. Erhat'a göre bizim çağımız kâhine inanmaz; ama aklıyla geleceği gören düşünürü tanır. Ve bu hizmetinin karşılığında “kör iktidarların baskısına” uğradığını da bilir.")
seg('J09', B, "[thoughtfully] Erhat'a göre bunu söylemek, beşinci yüzyıl Atinası'nda kolay değildi. Kölelik de zorbalık da yasalara uygun kurumlardı. Prometeus da, herhangi bir köle gibi zincire vurulmuştu.", "Erhat xiii2",
    "Erhat'a göre bunu söylemek V. yüzyıl Atinası'nda kolay değildi. Kölelik de zorbalık da yasalara uygun kurumlardı. Prometheus da herhangi bir köle gibi zincire vurulmuştu.")
seg('J10', B, "Köleliği doğal sayan bir dünyada, hakkın köleden yana olduğunu söylemek… Erhat'a göre bu, Ayshilos'un tek başına başardığı koca bir işti.", "Erhat xiii2")

B = 'Başkaldıran yaratık'
seg('K01', B, "[curious] Peki insan, ne zaman insan olmaya başladı?", "Erhat v6")
seg('K02', B, "Erhat, önsözün başında bu soruya günümüz düşünürlerinin, sanki sözleşmiş gibi verdiği cevabı aktarır: İnsan, başkaldıran yaratıktır.", "Erhat v6 (kısa alıntı)",
    "Erhat, önsözün başında bu soruya günümüz düşünürlerinin sanki sözleşmiş gibi verdiği cevabı aktarır: “İnsan başkaldıran yaratıktır.”")
seg('K03', B, "Bu görüşe göre insan, doğanın ya da geleneğin kurulu düzenine karşı ayaklandığı an insan olmuştur. İnsanlığını da ancak yeniden ve yeniden başkaldırarak sürdürebilir.", "Erhat v6")
seg('K04', B, "Erhat, kendi kuşağı adına konuşur: Gelenek süslerini üstümüzden atıyoruz, der. İster tanrıdan, ister insandan gelsin, avutucu ninnilere kulak vermiyoruz. Umuda karşı da ayaklandık; bugün, bu dünyada yaşamak istiyoruz.", "Erhat vi1, vi2 (kısa alıntılar)",
    "Erhat kendi kuşağı adına konuşur: Gelenek süslerini üstümüzden atıyoruz, der; ister tanrıdan ister insandan gelsin, “avutucu ninnilere” kulak vermiyoruz. “Umuda karşı da ayaklandık”: bugün, bu dünyada yaşamak istiyoruz.")
seg('K05', B, "[thoughtfully] Prometeus da öyledir. Erhat'a göre o, hiçbir umuda yer vermeden direnir. Hesiodos'ta umut, küpün dibinde kalmıştı. Ayshilos'ta Prometeus, insanlara kör umutlar vermişti. Kendisi ise umuda değil, bilincine tutunur.", "Erhat xii4; İG 96–99; ZVP 250; son cümle anlatıcının")
seg('K06', B, "Erhat'a göre bu kuşağın tek ülküsü, insan olmaktı. [slowly] [reverently] Ve önsöz, bu ülkünün nereden geldiğini tek cümleyle söyler: Bu ülkünün ilk temsilcisi… Prometeus'tur.", "Erhat vi3, vi4 (kısa alıntı)",
    "Erhat'a göre bu kuşağın tek ülküsü insan olmaktı. Ve önsöz, bu ülkünün nereden geldiğini tek cümleyle söyler: “Bu ülkünün ilk temsilcisi Prometheus'tur.”")
seg('K07', B, "Şimdi başta sorduğumuz soruya dönebiliriz. Zeus'u öfkelendiren yalnızca bir avuç ateş miydi? Erhat'ın okumasında ateş, iki kez küçük düşürülen bir tanrının son damlasıdır. Asıl mesele akıldır.", "Erhat x1, x5, ix5")
seg('K08', B, "[firmly] Ve Erhat'ın sorusunun cevabı da buradadır. Ayshilos tanrıları anlatırken, aslında iktidarı ve özgürlüğü anlatıyordu. Bu sorular eskimediği için, Prometeus hâlâ bugünün insanına benziyor.", "Erhat vi8, xi2, xiii1 ile uyumlu anlatıcı sonucu")

B = 'Ateşin yolculuğu'
seg('L01', B, "[curious] Peki Prometeus, sonunda kurtuldu mu?", "")
seg('L02', B, "Ayshilos'un cevabını bilmiyoruz; Kurtulmuş Prometeus kayıp. Hesiodos'a göreyse bir gün Herakles gelir, kartalı okuyla vurur ve Prometeus'u acısından kurtarır. [wryly] Tabii, Zeus'un izniyle.", "Erhat v2; Th. 526–534")
seg('L04', B, "Erhat onun izini Hesiodos'tan Göte'ye kadar sürer. Göte'nin şiirinde Prometeus, Zeus'a meydan okur ve insanları kendi suretinde yoğurur. Erhat'a göre bu şiirin anlamı açıktır: Asıl yaratıcı, insanın kendisidir.", "Erhat vi6, xi1; Goethe, 'Prometheus' (1774)")
seg('L05', B, "Meri Şeli, Frankenştayn romanına, “Modern Prometeus” alt başlığını koydu. Atom bombasının mimarı Openhaymır'ın biyografisinin adı ise, “Amerikan Prometeus”tur.", "Shelley 1818; Bird & Sherwin 2005",
    "Mary Shelley, Frankenstein romanına “Modern Prometheus” alt başlığını koydu. Atom bombasının mimarı Oppenheimer'ın biyografisinin adı ise “American Prometheus”tur.")
seg('L06', B, "[softly] İnsan ne zaman kendisine yasaklanmış bir ateşe el uzatsa, o eski Titan'ın adı yeniden anılır.", "anlatıcının yorumu")

B = 'Kapanış'
seg('M00', B, "[warmly] Erhat ile Eyüboğlu, çeviriye başlamadan önce bu oyunun çevrilemeyeceğini, hatta sahnelenemeyeceğini düşünüyormuş. Çevirdikçe yanıldıklarını anlamışlar. Dilekleri, Prometeus'u bir gün bir Türk tiyatrosunda oynanırken görmekti.", "Erhat xv4, xvi1")
seg('M01', B, "[warmly] Bir önsöz, bir efsaneyi bambaşka bir gözle okumayı öğretebilir. Azra Erhat'ınki, zincirdeki bu Titan'da insanın kendisini görmeyi öğretiyor. Ve onun dileğiyle: Bu bildiri, bugün de kulaklarımızda çınlasın.", "Erhat v5, vi4, xv3 (kısa alıntı)",
    "Bir önsöz, bir efsaneyi bambaşka bir gözle okumayı öğretebilir. Azra Erhat'ınki, zincirdeki bu Titan'da insanın kendisini görmeyi öğretiyor. Ve onun dileğiyle: “Bildirisi bugün de kulaklarımızda çınlasın!”")
seg('M02', B, "[curious] Peki sen ne düşünüyorsun? O kayada asıl tutsak kimdi: Prometeus mu, Zeus mu? Yorumlarda yaz.", "")
seg('M03', B, "[warmly] Geçmişten bugüne soru taşıyan bu hikâyeler hoşuna gidiyorsa, kanala abone olmayı unutma. Bir sonraki hikâyede görüşmek üzere.", "",
    "Geçmişten bugüne soru taşıyan bu hikâyeler hoşuna gidiyorsa kanala abone olmayı unutma. Bir sonraki hikâyede görüşmek üzere.")
out = {'voice': 'Emrullah (DpEiQMnL9WxMsymCsjPY), eleven_v4', 'revizyon': 2,
       'not': "tts: seslendirme metni (ses etiketleri, Yunanca adlar okunuşa göre). alt: altyazı ve ekran metni (Erhat'ın yazımı). kaynak: iddianın dayanağı. Erhat = kaynak/onsoz_notlar.md maddeleri (s. v–xvi); Th. = Hesiodos, Theogonia; İG = Hesiodos, İşler ve Günler; ZVP = Aiskhylos, Zincire Vurulmuş Prometheus (dize numaraları Yunanca metne göre).",
       'segments': S}
json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
import collections
c = collections.OrderedDict(); tot = 0
for s in S:
    w = len(re.sub(r'\[[^\]]*\]', ' ', s['tts']).split()); tot += w
    c.setdefault(s['bolum'], [0, 0]); c[s['bolum']][0] += 1; c[s['bolum']][1] += w
for k, v in c.items(): print(f'{k:22s} {v[0]:3d} cümle {v[1]:4d} kelime ~{v[1]/2.0+v[0]*0.6:5.0f} sn')
print(len(S), 'cümle', tot, 'kelime', 'tahmini', round((tot / 2.0 + len(S) * .6 + 12 * 2.5) / 60, 1), 'dk')
ids = [s['id'] for s in S]; assert len(ids) == len(set(ids))
