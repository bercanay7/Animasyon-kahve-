# Senaryo rev 4: rev 3 (senaryo_rev3.py çıktısı) + doğrulama turunun (6 üye) kabul edilen düzeltmeleri. Kararlar: kurul/kararlar.md
import json, re, sys, collections, subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__))
tmp = '/tmp/claude-0/-home-user/c3662c9d-24be-574f-ac5d-de35ddf76b95/scratchpad/gen/_rev3.json'
subprocess.run([sys.executable, os.path.join(HERE, 'senaryo_rev3.py'), tmp], check=True, capture_output=True)
d = json.load(open(tmp)); S = d['segments']
import importlib.util
spec = importlib.util.spec_from_file_location('r3', os.path.join(HERE, 'senaryo_rev3.py'))
mkalt = None
TTS2ALT = [('Prometeus', 'Prometheus'), ('Ayshilos', 'Aiskhylos'), ('Teogonia', 'Theogonia'), ('Gaya', 'Gaia'), ('Kaos', 'Khaos'),
           ('Rea', 'Rheia'), ('Hefaistos', 'Hephaistos'), ('Epimeteus', 'Epimetheus'), ('Olimpos', 'Olympos'),
           ('Temis', 'Themis'), ('Göte', 'Goethe'), ('Meri Şeli', 'Mary Shelley'), ('Frankenştayn', 'Frankenstein'),
           ('Openhaymır', 'Oppenheimer'), ('İyo', 'İo'), ('Afrodit', 'Aphrodite'),
           ('bin dokuz yüz altmış yedide', "1967'de"), ('yirminci yüzyılın', 'XX. yüzyılın'), ('yirminci yüzyılda', 'XX. yüzyılda')]
def mk(t):
    a = re.sub(r'\[[^\]]*\]\s*', '', t)
    for x, y in TTS2ALT: a = a.replace(x, y)
    return a
idx = lambda i: next(k for k, s in enumerate(S) if s['id'] == i)
def set_(i, tts, alt=None, kaynak=None, bolum=None):
    s = S[idx(i)]; s['tts'] = tts; s['alt'] = alt or mk(tts)
    if kaynak is not None: s['kaynak'] = kaynak
    if bolum is not None: s['bolum'] = bolum
def ins_after(after, i, bolum, tts, kaynak, alt=None):
    S.insert(idx(after) + 1, {'id': i, 'bolum': bolum, 'tts': tts, 'alt': alt or mk(tts), 'kaynak': kaynak})
def move_after(i, after, bolum=None):
    s = S.pop(idx(i)); S.insert(idx(after) + 1, s)
    if bolum: s['bolum'] = bolum
def drop(i): S.pop(idx(i))

# — Açılış —
set_('A02', "[mysterious] Şimdi de, onu bir kayaya mıhlatan Zeus'un… asıl tutsak olduğunu.", kaynak="Erhat xiv2, xiv5 (cevabı J04–J06)")
set_('A03', "[darkly] Dünyanın ucunda, her gün bir kartal iner, karaciğerini parçalar. Gece karaciğer yeniden büyür… [slowly] ve sabah, kartal yine gelir.")
set_('A06', "[thoughtfully] Bu tuhaf fikir, Azra Erhat'ın. Bin dokuz yüz altmış yedide, Sabahattin Eyüboğlu'yla birlikte çevirdikleri antik bir oyuna yazdığı önsözde, bu eski hikâyeyi bambaşka bir gözle okur.", kaynak="Erhat xvi2, xv4")
set_('A05', "[curious] Peki zincirleyen, nasıl tutsak olabilir? Ve Zeus'u bu kadar öfkelendiren, gerçekten bir avuç ateş miydi?")
# — Erhat'ın sorusu —
set_('B04', "[warmly] Erhat'a göre, anlatabilir: Oynanan dram, insanlığın dramıdır.", kaynak="Erhat v4")
set_('B06', S[idx('B06')]['tts'], alt="Ve Erhat can alıcı bir soru sorar: Nasıl oldu da milattan önce beşinci yüzyılda yaşamış bir yazar, XX. yüzyılın başkaldıran insanını yaratabildi?")
# — Taht kavgası —
set_('C04', "Ayshilos'tan iki yüzyıl kadar önce yaşamış şair Hesiodos'un Teogonia'sına göre, önce Kaos vardı, sonra Toprak Ana, Gaya. Gaya kendine eş olarak Gök'ü, Uranos'u doğurdu. [darkly] Ama Uranos, Gaya'dan doğan devlerden tiksindi; her birini doğar doğmaz, annelerinin karnına geri tıktı.", kaynak="Erhat vii1, vii3; Th. 116–160")
set_('C12', "[thoughtfully] Erhat bu iki devrimi birbirinden ayırır. Birincisi, kaba kuvvetin kendi kendini yenmesiydi; ikincisi, kaba kuvvetin akılla yenilmesi. Bu kez Zeus'a, ders almışa benzeyen Uranos ile Gaya yol göstermişti.",
     alt="Erhat bu iki devrimi birbirinden ayırır. Birincisi, kaba kuvvetin kendi kendini yenmesiydi; ikincisi, “kaba kuvvetin akılla yenilmesi.” Bu kez Zeus'a, ders almışa benzeyen Uranos ile Gaia yol göstermişti.")
set_('C17', "Ardından Titanlarla on yıllık bir savaş geldi; Zeus, yerin altındaki yüz kollu devleri savaşa sürdü ve Titanlar Tartaros'a kapatıldı. [thoughtfully] Erhat'a göre kaba güçler birbirini yok etmişti; meydanda akıldan başka güç kalmamıştı. Yıldırım elinde, Zeus tahta oturdu ve Gaya'nın öğüdüyle, dünyayı kardeşleriyle çocukları arasında paylaştırmaya girişti.",
     kaynak="Erhat viii5, viii6, ix1, ix2; Th. 504–506, 617–735, 881–885")
# — Dinmez öfke —
set_('D08', "Prometeus ise bu öfkeyi körüklemekten çekinmez. Kehanet gücüyle Zeus'u hem aldatır, hem tedirgin eder, hem de gülünç düşürür.", kaynak="Erhat x2 (kendi cümlelerimiz)")
# — Mekone —
set_('E03', S[idx('E03')]['tts'].replace('Mekoni', 'Mekone'))
set_('E11', "[ominous] Erhat'ın okumasında, iki kez küçük düşen Zeus, artık kaba kuvvete başvurmak zorunda kalır.", kaynak="Erhat x5 (kendi cümlelerimiz)")
set_('E15', S[idx('E15')]['tts'], alt="Hesiodos Zeus'tan yana anlatır: Zeus'un aklı aşılamaz. Ama Erhat satır aralarında başka bir şey okur: insanların gözünde gülünç düşmüş bir tanrı. Çünkü “akıl gücü tanrılardan insanlara geçmiştir.”")
set_('E16', "[slowly] Ve Erhat, sıranın kime geldiğini söyler: Üçüncü ve son devrim olup bitmiştir. İnsan, kendi gücünün bilincine varmıştır.",
     alt="Ve Erhat, sıranın kime geldiğini söyler: “Üçüncü ve son devrim” olup bitmiştir. “İnsan kendi gücünün bilincine varmış”tır.", kaynak="Erhat xi1 (kısa alıntı; cümlenin devamı alınmadı) — D11'in cevabı")
set_('E16b', "[knowingly] Demek ki Zeus'u öfkelendiren, bir avuç ateşten fazlasıydı. [slowly] Zincirin öbür ucunda kimin durduğunu ise, iki yüzyıl sonra bir Atina sahnesi gösterecekti.", kaynak="anlatıcının sonucu ve köprüsü (A05'in ara cevabı; A02'nin hatırlatılması)")
# — Duruşma —
set_('F02', "Erhat'a göre taht kavgasını iki şair de aşağı yukarı aynı anlatır; ama iş Prometeus'a gelince, yorumları büsbütün değişir.", kaynak="Erhat ix3")
set_('F08', "Güç, cezanın amacını söyler: Prometeus, Zeus'un zorbalığına razı olmayı öğrenecek… insanseverlikten vazgeçecek.", kaynak="ZVP 10–11 (στέργειν: razı olmak; kendi çevirimiz)")
set_('F10a', "[thoughtfully] Ona göre çağı düşünmek gerekir: Beşinci yüzyıl Atinası'nda kölelik, yasal bir kurumdu. Prometeus da bir köle gibi zincire vurulmuştu. [slowly] Ama işkencesini asıl büyüten, zincir değil; bir tanrının köle durumuna düşürülmesidir.",
     alt="Ona göre çağı düşünmek gerekir: V. yüzyıl Atinası'nda kölelik yasal bir kurumdu. Prometheus da bir köle gibi zincire vurulmuştu. Ama işkencesini asıl büyüten zincir değil, bir tanrının köle durumuna düşürülmesidir.")
set_('F10b', "[slowly] Erhat burada bir soru sorar: Dikkat ettin mi? Bütün bu sahne boyunca Prometeus tek söz etmedi. Çekiç indi, bir daha indi; zincire, hakaretlere, sessizce katlandı.", kaynak="Erhat xv3 ('Okuyucu dikkat etti mi ki…')")
set_('F13', "[softly] Ancak yapayalnız kalınca konuşur. İlk sözleri göğedir: [reverently] “Ey kutsal gök, hızlı kanatlı rüzgârlar, ırmakların kaynakları, deniz dalgalarının sayısız gülüşü… ve sen, herkesin anası Toprak. [pained] Bakın bana: Bir tanrıyım, ve tanrılardan neler çekiyorum.”",
     alt="Ancak yapayalnız kalınca konuşur. İlk sözleri göğedir: “Ey kutsal gök, hızlı kanatlı rüzgârlar, ırmakların kaynakları, deniz dalgalarının sayısız gülüşü… ve sen, herkesin anası Toprak: Bakın bana, bir tanrıyım ve tanrılardan neler çekiyorum.”", kaynak="ZVP 88–92 (birinci tekil; kendi çevirimiz) — I11 ile halka")
set_('F14', "[softly] Sonra birden kendi sözünü keser: [whispers] “Ama ne diyorum? Olacak her şeyi önceden, apaçık biliyorum; hiçbir acı bana habersiz gelmeyecek. Payıma düşeni olabildiğince kolay taşımalıyım; zorunluluğun gücüne karşı konmaz. [pained] [slowly] Yine de başıma gelenler üstüne… ne susabiliyorum, ne de konuşabiliyorum.”",
     alt="Sonra birden kendi sözünü keser: “Ama ne diyorum? Olacak her şeyi önceden, apaçık biliyorum; hiçbir acı bana habersiz gelmeyecek. Payıma düşeni olabildiğince kolay taşımalıyım; zorunluluğun gücüne karşı konmaz. Yine de başıma gelenler üstüne… ne susabiliyorum ne de konuşabiliyorum.”", kaynak="ZVP 101–107 (kendi çevirimiz; Erhat'ın s. xii'deki çeviri dizelerinden farklı)")
# — Savunma —
set_('G03', "Çekiç seslerini duyan deniz perileri, Okeanos'un kızları, derinliklerden gelir. Prometeus onlara geçmişi anlatır.", kaynak="ZVP 128–135, 197–198")
ins_after('G03', 'G03b', 'Savunma', "Ayshilos'ta annesi Toprak'tır; öbür adı Temis, yani Adalet. Titanlarla savaş sürerken, bu anne ona geleceği söylemişti: Zafer gücün değil… kurnazlığın olacaktı.", "ZVP 209–213; Erhat x4")
set_('G06', "[bitterly] Şimdi ise tahta çıkardığı tanrının zincirindeydi. Prometeus bunu tek cümleyle açıklar: “Zorbalığın bir hastalığı vardır: dostlarına güvenmez.”",
     alt="Şimdi ise tahta çıkardığı tanrının zincirindeydi. Prometheus bunu tek cümleyle açıklar: “Zorbalığın bir hastalığı vardır: dostlarına güvenmez.”")
set_('G07b', "[softly] Kendi sözleriyle: [pained] “Ölümlülere acıdım. Ama kendim… acınmaya layık görülmedim.”", alt="Kendi sözleriyle: “Ölümlülere acıdım. Ama kendim… acınmaya layık görülmedim.”", kaynak="ZVP 239–241 (edilgen yapı korunarak; kendi çevirimiz)")
set_('G11', "[firmly] Ve sanık suçunu inkâr etmez. Oyundaki sözleriyle: “Bunların hepsini biliyordum. İsteyerek, isteyerek suç işledim.” [thoughtfully] Erhat'a göre bu, bugünkü bir sanığın savunmasıdır: Ne yaptımsa, bile bile yaptım.",
     alt="Ve sanık suçunu inkâr etmez. Oyundaki sözleriyle: “Bunların hepsini biliyordum. İsteyerek, isteyerek suç işledim.” Erhat'a göre bu, bugünkü bir sanığın savunmasıdır: “Ne yaptımsa bile bile yaptım.”")
set_('G13', "[thoughtfully] Erhat'ın deyişiyle bu bilinç, onda hem gurur, hem de bir katlanma duygusu doğurur.", alt="Erhat'ın deyişiyle bu bilinç, onda hem gurur hem de bir “katlanma duygusu” doğurur.", kaynak="Erhat xii1 (kısa alıntı)")
move_after('G13', 'G11')
ins_after('G12b', 'G13b', 'Savunma', "[softly] Yani biliyordu; ama bilmek, yaşamak değildi. [slowly] Yine de geri adım atmaz.", "anlatıcının yorumu (ZVP 268–270'e dayanır)")
# — Tanıklar —
set_('H04', "Yaşlı Titan Okeanos, iyi niyetle aracılık önerir: [softly] “Kendini bil; tanrıların başında yeni bir zorba var. Diline sahip ol.” [coldly] Prometeus'un cevabı buz gibidir: “Suçumdan pay almadığın için seni kıskanıyorum. Kendi başını derde sokma.”",
     kaynak="ZVP 307–334 (kendi çevirimiz)")
set_('H05', "Periler ona, sözünü sakınmıyorsun, der. [knowingly] Erhat, bu çevirinin ardındaki Yunanca ifadenin tam anlamını verir: Dilin fazla özgür. Başkaları, hiçbir umuda yer vermeden direnen bu tutumu gurur ya da kibir sanır. [slowly] Oysa ona özgürlüğü sağlayan, bilincidir.",
     alt="Periler ona “sözünü sakınmıyorsun” der. Erhat, bu çevirinin ardındaki Yunanca ifadenin tam anlamını verir: “dilin fazla özgür.” Başkaları, “hiçbir umuda yer vermeden” direnen bu tutumu “gurur ya da kibir” sanır. Oysa ona özgürlüğü sağlayan bilincidir.",
     kaynak="ZVP 178–180; Erhat xii4, xiii1 (Eyüboğlu-Erhat çevirisinden iki kelime, kaynak gösterilerek)")
set_('H09', "[softly] İyo, acısına dayanamayıp ölmeyi diler. Prometeus'un cevabı ağırdır: “Ben ölemem bile. İşkencem, Zeus'un zorbalığı yıkılmadıkça bitmeyecek.”",
     alt="İo, acısına dayanamayıp ölmeyi diler. Prometheus'un cevabı ağırdır: “Ben ölemem bile. İşkencem, Zeus'un zorbalığı yıkılmadıkça bitmeyecek.”", kaynak="ZVP 747–756 (kendi çevirimiz)")
set_('H10', "Ve bir şey daha söyler: İyo'nun soyundan, on üç kuşak sonra, onu bu zincirden kurtaracak bir okçu doğacak.", kaynak="ZVP 771–774, 871–873 (ödemesi L01–L02)")
# — Sır ve sorgu —
set_('I05', "Sonunda Zeus, habercisi Hermes'i gönderir; Erhat'ın deyişiyle, sanığı gözdağıyla sorguya çeken bir polis müdürü. Emir kısadır: Sırrı söyle.",
     alt="Sonunda Zeus, habercisi Hermes'i gönderir; Erhat'ın deyişiyle “sanığı gözdağıyla sorguya çeken” bir polis müdürü. Emir kısadır: Sırrı söyle.")
set_('I06', "[defiantly] Prometeus alay eder: “Siz yeni tanrılar, kalenizde hiç acı yüzü görmeyeceğinizi sanıyorsunuz. Ben oradan iki zorbanın düştüğünü görmedim mi? Üçüncüsünün, şimdi hüküm sürenin düşüşünü de göreceğim: en utanç verici biçimde, en çabuk.”",
     kaynak="ZVP 953–959 (κοιρανοῦντα: üçüncüsü; kendi çevirimiz) — D11 ile bağ")
set_('I08', "[mocking] Hermes'in tehditleri sürerken, Prometeus'un ağzından bir an tek bir inilti kaçar: [pained] “Eyvah!” [mocking] Hermes hemen yakalar: “Zeus bu kelimeyi bilmez.” [calmly] Prometeus'un cevabı: “Yaşlanan zaman, her şeyi öğretir.”",
     alt="Hermes'in tehditleri sürerken, Prometheus'un ağzından bir an tek bir inilti kaçar: “Eyvah!” Hermes hemen yakalar: “Zeus bu kelimeyi bilmez.” Prometheus'un cevabı: “Yaşlanan zaman her şeyi öğretir.”", bolum='Tahtı sallayan sır')
move_after('I08', 'I07')
set_('I07b', "[defiantly] Ve zincirdeki adam, evrenin efendisine şart koşar: “Bu aşağılayıcı zincirler çözülmeden, Zeus bu sırrı benden ne işkenceyle alabilir, ne de hileyle.”")
# — Zincirin öbür ucu —
set_('J05', "Ona göre Zeus, bütün uşaklarına, dalkavuklarına rağmen, bir çocuk gibi zayıf ve çaresizdir: Onu yıkımdan kurtarabilecek tek kişi, zincire vurduğu Prometeus'tur.",
     alt="Ona göre Zeus, bütün uşaklarına, dalkavuklarına rağmen, “bir çocuk gibi zayıf ve çaresizdir”: Onu yıkımdan kurtarabilecek tek kişi, zincire vurduğu Prometheus'tur.", kaynak="Erhat xiv5 (kısa alıntı + kendi cümlemiz)")
set_('J06', "[knowingly] Erhat'ın deyişiyle: Zeus, tutukladığı düşmanının elinde tutukludur aslında. [slowly] Yani roller yer değiştirmiştir: Sanık özgür, görünmeyen yargıç tutsak.",
     alt="Erhat'ın deyişiyle: “Zeus tutukladığı düşmanının elinde tutukludur aslında.” Yani roller yer değiştirmiştir: Sanık özgür, görünmeyen yargıç tutsak.")
# — Kartal, fırtına —
ins_after('J10', 'I08a', 'Kartal, fırtına ve son söz', "[darkly] Zorba, susturamadığı birine ne yapar?", "bölüm sorusu")
set_('I08b', "[ominous] Sorguya dönelim. Hermes son tehdidini savurur: “Kaya yıldırımla parçalanacak, sen içine gömüleceksin. Uzun zaman sonra ışığa döndüğünde, Zeus'un kanatlı köpeği, kanlı kartal gelecek. Çağrılmamış bir konuk gibi, bütün gün karaciğerinle ziyafet çekecek.”",
     alt="Sorguya dönelim. Hermes son tehdidini savurur: “Kaya yıldırımla parçalanacak, sen içine gömüleceksin. Uzun zaman sonra ışığa döndüğünde, Zeus'un kanatlı köpeği, kanlı kartal gelecek. Çağrılmamış bir konuk gibi bütün gün karaciğerinle ziyafet çekecek.”")
set_('I08c', "[slowly] Açılıştaki kartal, Ayshilos'ta bir tehdittir: hayır demenin bedeli. [defiantly] Prometeus'un cevabı: “Bu haberleri zaten biliyordum. Ne yaparsa yapsın… beni öldüremez.”",
     alt="Açılıştaki kartal, Aiskhylos'ta bir tehdittir: hayır demenin bedeli. Prometheus'un cevabı: “Bu haberleri zaten biliyordum. Ne yaparsa yapsın… beni öldüremez.”", kaynak="ZVP 1040–1041, 1053 (kendi çevirimiz); ilk cümle anlatıcının")
set_('I09', "Hermes perilere oradan gitmelerini söyler. Ama periler kalır: “Hainlerden nefret etmeyi öğrendik,” deyip Prometeus'un yanında dururlar.",
     alt="Hermes perilere oradan gitmelerini söyler. Ama periler kalır: “Hainlerden nefret etmeyi öğrendik” deyip Prometheus'un yanında dururlar.")
set_('I10', "[intense] Sözle yenemediği sanığa, Zeus sonunda kaba kuvvetle cevap verir. Prometeus olanları kendi ağzıyla anlatır: “Artık sözde değil, gerçekte! Yer sarsılıyor, gök gürlüyor, şimşekler çakıyor. Rüzgârlar birbirine saldırıyor… gök, denize karıştı.”",
     alt="Sözle yenemediği sanığa, Zeus sonunda kaba kuvvetle cevap verir. Prometheus olanları kendi ağzıyla anlatır: “Artık sözde değil, gerçekte! Yer sarsılıyor, gök gürlüyor, şimşekler çakıyor. Rüzgârlar birbirine saldırıyor… gök denize karıştı.”", kaynak="ZVP 1080–1090 (kendi çevirimiz); Erhat xv3; E11'in ödemesi")
set_('I11', "[slowly] İlk sözleri gibi, son sözleri de göğe ve anasınadır; adlarından biri Adalet olan anasına: [pained] “Görüyor musun, haksız yere neler çekiyorum.”",
     alt="İlk sözleri gibi son sözleri de göğe ve anasınadır, adlarından biri Adalet olan anasına: “Görüyor musun, haksız yere neler çekiyorum.”", kaynak="ZVP 1091–1093 (ἔκδικα πάσχω; kendi çevirimiz) — F13 ve G03b ile halka")
set_('I12', "[firmly] Erhat'ın dikkat çektiği gibi, başta tek söz etmeyen Prometeus, dünya başına yıkılıp perilerle birlikte gömülene dek konuşmakta direnir. Son söz onundur. [slowly] Ona göre Ayshilos'un söylemek istediği de budur: Kıyamet de kopsa, son söz özgür düşüncenindir.",
     alt="Erhat'ın dikkat çektiği gibi, başta tek söz etmeyen Prometheus, dünya başına yıkılıp perilerle birlikte gömülene dek konuşmakta direnir. Son söz onundur. Ona göre Aiskhylos'un söylemek istediği de budur: “Kıyamet de kopsa son söz özgür düşüncenindir.”")
# — Ateşin yolculuğu —
set_('L02', "Hesiodos'a göre geldi: Adı Herakles'ti. Kartalı öldürdü ve Prometeus'u acısından kurtardı. [wryly] Tabii Zeus'un izniyle; oğlunun ünü artsın diye. Ayshilos'un Kurtulmuş Prometeus'u ise kayıp.", kaynak="Th. 526–534; Erhat v2 ('okçu' ZVP 871–873'ten)")
set_('L05', "Meri Şeli, Frankenştayn romanına Modern Prometeus alt başlığını koydu. Atom bombasının babası diye anılan Openhaymır'ın biyografisinin adı da Amerikan Prometeus: Nolan'ın filmi bu kitaba dayanır.",
     alt="Mary Shelley, Frankenstein romanına “Modern Prometheus” alt başlığını koydu. Atom bombasının babası diye anılan Oppenheimer'ın biyografisinin adı da “American Prometheus”: Nolan'ın filmi bu kitaba dayanır.")
# — Başkaldıran yaratık —
set_('K01', "[thoughtfully] Erhat'ın önsözü, daha ilk sayfasında şu soruyu anar: İnsan nedir? Ne zaman insan olmaya başladı?", kaynak="Erhat v6")
set_('K02', "Ve kendi çağının düşünürlerinin, sanki sözleşmiş gibi verdiği cevabı aktarır: İnsan, başkaldıran yaratıktır. Doğaya ya da geleneğe boyun eğmeyi reddettiği an insan olmuştur; insan kalması da, bu başkaldırıyı yeniden ve yeniden sürdürmesine bağlıdır.",
     alt="Ve kendi çağının düşünürlerinin sanki sözleşmiş gibi verdiği cevabı aktarır: “İnsan başkaldıran yaratıktır.” Doğaya ya da geleneğe boyun eğmeyi reddettiği an insan olmuştur; insan kalması da, bu başkaldırıyı yeniden ve yeniden sürdürmesine bağlıdır.")
set_('K04', "Erhat, kendi kuşağının bu görüşü öylesine benimsediğini yazar ki, gelenek süslerini üstünden atmıştır. Ve onun adına ekler: Umuda karşı da ayaklandık; bugün ve bu dünyada yaşamak istiyoruz.",
     alt="Erhat, kendi kuşağının bu görüşü öylesine benimsediğini yazar ki, gelenek süslerini üstünden atmıştır. Ve onun adına ekler: “Umuda karşı da ayaklandık: Bugün ve bu dünyada yaşamak istiyoruz.”", kaynak="Erhat vi1, vi2 (kısa alıntı, tırnakta)")
set_('K08a', "[firmly] Peki, Erhat'ın en baştaki sorusu? Milattan önce beşinci yüzyılın bir yazarı, yirminci yüzyılın başkaldıran insanını nasıl yaratabildi? Erhat'ın kendi cevabı şudur: Prometeus efsanede de politik bir kişiydi; ama onun dramını modern anlamda politik bir dram olarak canlandırmak, Atina'nın politik görüşü en köklü tragedya yazarı Ayshilos'un başarısıydı.",
     alt="Peki, Erhat'ın en baştaki sorusu? Milattan önce beşinci yüzyılın bir yazarı, XX. yüzyılın başkaldıran insanını nasıl yaratabildi? Erhat'ın kendi cevabı şudur: Prometheus efsanede de politik bir kişiydi; ama onun dramını modern anlamda politik bir dram olarak canlandırmak, Atina'nın politik görüşü en köklü tragedya yazarı Aiskhylos'un başarısıydı.",
     kaynak="Erhat vi7–vi8 (B06'nın sorusu yeniden soruluyor ve Erhat'ın cevabı)")
set_('K08b', "[thoughtfully] Önsözün sonuna doğru bir ipucu daha verir: Efsane Prometeus'a kâhin der. Erhat'ın çağı kâhine inanmaz; ama aklıyla geleceği gören düşünürü tanır, onun bu hizmeti yüzünden cezalandırıldığını da bilir.", kaynak="Erhat xiv6, xv1 (kendi cümlelerimiz)")
ins_after('K08a', 'K08c', 'Başkaldıran yaratık', "Ve ona göre Ayshilos'un bize dek ulaşan bildirisi şudur: Akıl gücü, kaba güçten üstündür; düşünceye gem vurulamaz. [slowly] Belki de bu yüzden, yirmi beş yüzyıl önceki bu sanık, hâlâ insana benziyor.",
     "Erhat xiv3 (kısa alıntı; 'iktidar sahipleri' cümlesi alınmadı); son cümle anlatıcının",
     alt="Ve ona göre Aiskhylos'un bize dek ulaşan bildirisi şudur: “Akıl gücü kaba güçten üstündür, düşünceye gem vurulamaz.” Belki de bu yüzden, yirmi beş yüzyıl önceki bu sanık hâlâ insana benziyor.")
set_('K06', "Erhat'ın kuşağının tek ülküsü, insan olmaktı; bu uğurda göze alamayacakları çaba, katlanamayacakları cefa yoktu. [slowly] [reverently] Ve önsöz, bu ülküyü tek bir ada bağlar: Bu ülkünün ilk temsilcisi… Prometeus'tur.",
     alt="Erhat'ın kuşağının tek ülküsü insan olmaktı; bu uğurda göze alamayacakları çaba, katlanamayacakları cefa yoktu. Ve önsöz bu ülküyü tek bir ada bağlar: “Bu ülkünün ilk temsilcisi Prometheus'tur.”", kaynak="Erhat vi3, vi4 (kısa alıntı)")
drop('K08b')
set_('K08a', "[firmly] Peki ya Erhat'ın en baştaki sorusu? İki bin beş yüz yıl önceki bir yazar, yirminci yüzyılın başkaldıran insanını nasıl yaratabildi? Erhat'ın cevabı: Prometeus efsanede de politikti; ama onu modern anlamda politik bir drama dönüştüren, Atina'nın politik görüşü en köklü tragedya yazarı Ayshilos'tu.",
     alt="Peki ya Erhat'ın en baştaki sorusu? İki bin beş yüz yıl önceki bir yazar, XX. yüzyılın başkaldıran insanını nasıl yaratabildi? Erhat'ın cevabı: Prometheus efsanede de politikti; ama onu modern anlamda politik bir drama dönüştüren, Atina'nın politik görüşü en köklü tragedya yazarı Aiskhylos'tu.",
     kaynak="Erhat vi7–vi8 (B06'nın sorusu yeniden soruluyor; Erhat'ın cevabı)")
# K bloğu sırası: K01, K02, K04, K08a, K08b, K08c, K06 (zaten bu sırada); kuyruk M00, M02, M03
# — bölüm adları (YouTube bölümleri) —
REN = {'Açılış': 'Ateşi bile bile çalan Titan', 'Savunma': 'Savunma: “Bile bile yaptım”', 'Tanıklar': 'Tanıklar ve “inek geçidi”',
       'Ateşin yolculuğu': "Herakles'ten Oppenheimer'a", 'Kapanış': 'Çevirmenlerin dileği'}
for s in S: s['bolum'] = REN.get(s['bolum'], s['bolum'])
d['revizyon'] = 4; d['segments'] = S
ids = [s['id'] for s in S]; assert len(ids) == len(set(ids))
json.dump(d, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
c = collections.OrderedDict(); tot = 0
for s in S:
    t = re.sub(r'\[[^\]]*\]', '', s['tts']).replace('“', '').replace('”', ''); n = len(re.sub(r'\s+', ' ', t).strip())
    c.setdefault(s['bolum'], [0, 0]); c[s['bolum']][0] += 1; c[s['bolum']][1] += n
for k, (n, cc) in c.items():
    dd = cc / 13.91 + n * 1.0 + 2.2; tot += dd; print(f'{k:32s} {n:3d} cümle {dd:6.0f} sn')
print(len(S), 'cümle; tahmini', f'{int(tot // 60)}:{tot % 60:04.1f}')
print("'Erhat'a göre':", sum(s['tts'].count("Erhat'a göre") for s in S), " 'Peki':", sum(s['tts'].count('Peki') for s in S), ' [curious]:', sum(s['tts'].count('[curious]') for s in S))
