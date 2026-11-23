# Senaryo kaynağı: senaryo.json bundan üretilir (python3 tools/senaryo_kaynak.py). Satır biçimi:
#   KİMLİK | bölüm | tts (ses etiketli) | alt (altyazı; boşsa tts'den etiketler atılır) | kaynak notu
# Kaynak kısaltmaları: SB = Standart Babil sürümü (tablet, satır: George 2003 numaralaması; olgu kaynağı, metni alınmaz),
# OB P / OB Y / OB S = Eski Babil Pennsylvania, Yale, Sippar (Meissner) tabletleri (Jastrow ve Clay 1920 çevirisi, kamu malı),
# Th = Thompson 1928 (kamu malı). Alıntıların Türkçesi bizim; aslıyla karşılaştırma kaynak/DOGRULAMA.md.
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SATIR = r'''
A01|Kanca|[calmly] Dört bin yıllık bir destanda bir kral, ölüme karşı aradığını buldu, eline aldı… ve bir yılana kaptırdı.||Kanca, kapak A'nın vaadi ilk saniyede: bitki elde, yılan. SB XI 305-307. "Dört bin yıllık": en eski Sümerce Gılgamış şiirleri ~MÖ 2100, Eski Babil destanı ~MÖ 1800
A02|Kanca|[softly] Onu bu yola düşüren bir ölümdü: en yakın dostunun ölümü. Altı gün yedi gece başından kalkmamış, onu gömdürmemişti.||Kapak B'nin vaadi ilk 10 sn'de. SB X 58-60; OB S ii. L2 açılır (D11-D13 kapatır)
A03|Kanca|[calmly] Kral eve eli boş döndü. Ve yanındaki yabancıya ilk sözü şu oldu: “Çık şu surların üstüne. Tuğlalarına bak.”||SB XI 322-324. Yabancı: kayıkçı Urşanabi; rolü (kayıkçı) ve görüntüsü kancada ekilir, adı E09'da
A04|Kanca|[curious] Her şeyini kaybetmiş bir adam neden övünür?||L1 (yönün sorusu) açılır; cevap olay: H01-H09
A05|Kanca|[thoughtful] Sen de bir gün öleceğini biliyorsun. Bunu bile bile nasıl yaşanır? Gılgamış bu sorudan kaçarak dünyanın ucuna kadar gitti.||Başlığın sorusu. Ad kancanın içinde (kimlik); sonraki cümle hikâye (köprü yok)
B01|Yabani adam|[calmly] Gılgamış, Uruk şehrinin kralıydı: üçte ikisi tanrı, üçte biri insan.||SB I 48; IX 51
B02|Yabani adam|[calmly] Gücüne denk kimse yoktu ve bedelini şehir ödüyordu: kral, babasına oğul, annesine kız bırakmıyordu.||SB I 67-76 (olgu)
B03|Yabani adam|[calmly] Halk tanrılara yakardı. Ana tanrıça bir parça kil kopardı, bozkıra attı. Kilden, krala denk biri doğdu: Enkidu.||SB I 101-104 (Aruru kili koparıp bozkıra atar). Kil üslubun kendisi
B04|Yabani adam|[calmly] Enkidu bozkırda ceylanlarla otluyor, hayvanlarla aynı sudan içiyordu. Bedeni baştan ayağa tüylüydü; insan nedir bilmiyordu.||SB I 105-112; OB P iii ("with the cattle to drink water")
B05|Yabani adam|[calmly] Onu insanların arasına bir kadın getirdi: Şamhat.||SB I 145-190. Şamhat ilk perdede adı ve görüntüsüyle (D03-D05'i taşıyacak)
B06|Yabani adam|[softly] Enkidu altı gün yedi gece onunla kaldı. Sonra ceylanlarının yanına döndü; ama ceylanlar ondan kaçtı.||OB P ii 4-6 ("six days and seven nights"); SB I 194-199. Cinsellik yalnız imayla. "Altı gün yedi gece" kalıbı üç kez döner (B06, D12, F06); anlatılmaz
B07|Yabani adam|[softly] Artık onlardan biri değildi.||SB I 200-202
B08|Yabani adam|[warmly] Şamhat kendi giysisini ikiye bölüp onu giydirdi. Ona ekmek verdi; Enkidu ekmek yemeyi bilmiyordu. Bira verdi; yedi testi içti, yüzü parladı.||OB P ii 27-iii 25 (Jastrow "wine"; şikarum bugün "bira" okunur). Giysi: OB P ii 27-30 ("She stripped off a garment, clothed him with one")
B09|Yabani adam|[thoughtful] Ekmek, bira, bir giysi. Küçük şeyler. Ölüm döşeğinde bunlar ona hatırlatılacaktı.||Ekme: D04 ödenir. L3 açılır
B10|Yabani adam|[firmly] Enkidu Uruk'a geldi ve kapıyı ayağıyla tutup kralın yolunu kesti. İki boğa gibi boğuştular; eşiği yıktılar, duvarı sarstılar.||OB P vi ("Enkidu blocked the gate with his foot… like oxen they fought, the threshold they demolished, the wall they impaired")
B11|Yabani adam|[warmly] Sonunda Gılgamış'ın öfkesi dindi. O günden sonra iki düşman, iki dost oldu.||OB P vi ("his wrath was appeased"); SB II
C01|Ormanın bekçisi|[calmly] Bir gün Gılgamış dostuna bir yolculuk önerdi: uzaktaki Sedir Ormanı'na gidip bekçisi Humbaba'yı öldürmek.||OB Y iii; SB II. Humbaba ilk perdede
C02|Ormanın bekçisi|[firmly] Enkidu ormanı biliyordu. “Humbaba'nın kükremesi tufandır,” dedi. “Ağzı ateştir, nefesi ölümdür.”||OB Y iii ("whose roar is a flood, whose mouth is fire, whose breath is death"), Jastrow ve Clay 1920
C03|Ormanın bekçisi|[firmly] Gılgamış'ın cevabı hazırdı: “İnsanın günleri sayılıdır; ne yapsa yeldir. Sen şimdiden ölümden mi korkuyorsun? Ben önden giderim. Düşersem adımı bırakmış olurum.”||OB Y iv 140-148. Akadca (Jastrow ve Clay 1920 harf çevirisi): a-we-lu-tum ma-nu-ú ú-tam-mu-ša / mi-im-ma ša i-te-ni-pu-šu ša-ru-ma / at-ta an-na-nu-um-ma ta-dar mu-tam … lu-ul-li-ik-ma i-na pa-ni-ka … šu-mi lu-uš-tak-na. Jastrow 1920 'ba-ba-nu' okuyup 'kapılarda' çevirmiş; bugünkü okuma 'günleri sayılıdır… yeldir' (Fable senaryo okuması, 23 Kasım; başkan Akadca satırda doğruladı)
C04|Ormanın bekçisi|[thoughtful] Gılgamış'ın ölüme ilk cevabı buydu: geride bir ad bırakmak.||Tek soyut cümle, olaydan (C03) hemen sonra
C05|Ormanın bekçisi|[calmly] Ormana vardılar. Maymunlar bağırıyor, ağustosböcekleri ötüyor, kuşlar şakıyordu. Bu sesleri iki bin on birde ortaya çıkan kırık bir tabletten biliyoruz.|Ormana vardılar. Maymunlar bağırıyor, ağustosböcekleri ötüyor, kuşlar şakıyordu. Bu sesleri 2011'de ortaya çıkan kırık bir tabletten biliyoruz.|SB V; Süleymaniye Müzesi tableti, 2011 (Al-Rawi ve George 2014, JCS 66). Tablet bilgisi sahnenin içinde, tek cümle (Fable önerisi 16). C06 kimliği boş bırakıldı (numara kayması dersi)
C07|Ormanın bekçisi|[firmly] Humbaba yenildi ve aman diledi. Enkidu, “Dinleme onu,” dedi. Öldürdüler.||SB V (Humbaba yalvarır, Enkidu öldürmesini söyler)
C08|Ormanın bekçisi|[calmly] Sonra ormanın en yüksek sedirini kestiler. Enkidu ondan tanrıların tapınağına dev bir kapı yaptı.||SB V 293-302 (Nippur'daki Enlil tapınağına kapı). Ekme: D02
C09|Ormanın bekçisi|[calmly] Eve döndüklerinde, tanrıların gökten saldığı bir boğayı da öldürdüler.||SB VI (Gök Boğası; İştar adı anılmaz, ad yükü)
C10|Ormanın bekçisi|[slowly] Tanrılar toplandı. Ormanın bekçisini ve göğün boğasını öldüren iki dosttan biri ölmeliydi.||SB VII; Hitit sürümü (Th VII i: "These who the heavenly Bull have kill'd and Humbaba have smitten… Enkidu shall die")
C11|Ormanın bekçisi|[slowly] Seçtikleri Enkidu oldu.||Th VII i (Hititçe parça)
D01|Yatağın başı|[softly] Enkidu kararı rüyasında duydu ve yatağa düştü.||SB VII 1-
D02|Yatağın başı|[firmly] İlk öfkesi kendi elleriyle yaptığı kapıyaydı: “Bunu bilseydim, baltamı alır, seni paramparça ederdim.”||SB VII 37-64 (George 2003; olgu, çeviri bizim). Th'de yok (1928'de bilinmiyordu)
D03|Yatağın başı|[firmly] Sonra Şamhat'ı lanetledi: onu insanların arasına getiren kadını.||SB VII 100-131; Th VII ii özet
D04|Yatağın başı|[slowly] Güneş tanrısı gökten seslendi: “Enkidu, neden lanet ediyorsun? Sana tanrılara layık ekmek yediren, krallara layık içki içiren, sırtına giysi geçiren o değil mi? Sana Gılgamış gibi bir dost veren o değil mi?”||Th VII iii 34-40 ("She 'twas who made thee eat bread, for divinity proper… wine… a generous mantle… and for comrade did give to thee Gilgamish"). B08-B09'un ödemesi
D05|Yatağın başı|[softly] Enkidu'nun öfkesi dindi. Lanetini geri aldı ve Şamhat'ı kutsadı.||Th VII iii 49-iv ("his wrath was appeased… relenting, regrets his curse, and blesses the Hetaera")
D06|Yatağın başı|[thoughtful] Ekmek, bira, bir giysi, bir dost. Ölümle ödenen bir hayat. Ölmek üzere olan adam, o hayatı kutsadı.||Yorum, tek; olaydan (D05) hemen sonra. L3 kapanır; L2'ye ilk cevap (olayla)
D07|Yatağın başı|[softly] On iki gün yattı; her gün biraz daha kötüledi.||SB VII 252-255 (on iki gün)
D08|Yatağın başı|[slowly] Gılgamış elini dostunun göğsüne koydu. Kalbi atmıyordu.||Th VIII ii 15-17 ("his heart… made no beat"); SB VIII 57-58
D09|Yatağın başı|[slowly] Dostunun yüzünü, bir gelinin yüzü gibi örttü.||Th VIII ii 17 ("Then he veil'd (his) friend like a bride"); SB VIII 59
D10|Yatağın başı|[sad] Sonra yavrusu elinden alınmış bir dişi aslan gibi ölünün önünde bir ileri bir geri yürüdü. Saçlarını yoldu, üstündeki süsleri söküp attı.||Th VIII ii 18-21 ("Roar'd like a lioness robb'd of her whelps… Paced he backwards and forwards, tearing and casting his ringlets"); SB VIII 60-64
D11|Yatağın başı|[softly] Onu gömdürmedi.||SB X 58; OB S ii 4 ("unto the tomb I have not consign'd him")
D12|Yatağın başı|[sad] Sonradan kendisi anlatacaktı: “Altı gün yedi gece başında ağladım. Gömülmesine izin vermedim. Dostum çığlığıma kalkar diye.”||SB X 56-59; OB S ii (George okuması "My friend will surely rise at my cry"). Alıntı Siduri'ye anlatılır (E05); burada öne alındı
D13|Yatağın başı|[whispers] “Ta ki burnundan bir kurt düşene kadar.”||SB X 60; OB S ii ("until a maggot fell from his nostril"; Th 1928 bunu "like a worm hath lain on his face" okur, eski okuma). L2 kapanır. Sonra 1,5 sn sessizlik
D14|Yatağın başı|[slowly] Sonra bozkıra çıktı ve kendi kendine sordu: “Ben de ölmeyecek miyim? Enkidu gibi olmayacak mıyım? İçime bir dert girdi. Ölümden korkuyorum; bozkırlarda dolaşıyorum.”||Th IX i 3-5 ("I, too—shall I not die like Enkidu also? Sorrow hath enter'd my heart; I fear death as I range o'er the desert"); SB IX 3-5
D15|Yatağın başı|[calmly] Bir aslan postuna büründü ve kaçmaya başladı.||Th VII iii 43 / VIII iii 7 ("will put on the skin of a lion, and range o'er the desert"); SB IX
E01|Dünyanın ucu|[curious] Bir tek insanın ölümsüz olduğunu biliyordu: tufandan kurtulan Utnapiştim. Dünyanın ucunda yaşıyordu.||Th IX i 6-7; SB IX 6-7. Utnapiştim filmin ilk yarısında
E02|Dünyanın ucu|[calmly] Güneşin doğup battığı ikiz dağa vardı. Kapıyı bekleyen akrep insanlar onu uyardı; dinlemedi.||SB IX ii-iii (Maşu dağı, akrep insanlar). Canavar tek cümle
E03|Dünyanın ucu|[slowly] Güneşin geceleri geçtiği yola girdi. Karanlık o kadar koyuydu ki ne önünü görüyordu ne arkasını. Öyle yürüdü.||SB IX iv-v ("dense was the darkness, there was no light, he could see nothing ahead or behind"); Th IX
E04|Dünyanın ucu|[calmly] Karanlığın sonunda, ağaçlarında taş mücevherler yetişen bir bahçe vardı. Gılgamış durmadı.||SB IX v-vi; Th IX notu ("numerous minerals and stones")
E05|Dünyanın ucu|[calmly] Deniz kıyısında bir meyhane buldu. Meyhaneci Siduri onu görünce kapısını sürgüledi: karşısında yüzü yanmış, aslan postlu bir yabancı vardı.||SB X 1-20; Th X ii ("Barr'd she her postern"). Gılgamış da bir yabancı (H09'un yankısı)
E06|Dünyanın ucu|[warmly] Siduri ona şöyle dedi: “Gılgamış, nereye koşuyorsun? Aradığın hayatı bulamayacaksın. Tanrılar insanı yarattığında ona ölümü verdiler; hayatı kendi ellerinde tuttular.”||OB S iii 1-5 (Jastrow ve Clay 1920: "Why, O Gish, does thou run about? The life that thou seekest, thou wilt not find. When the gods created mankind, Death they imposed on mankind; Life they kept in their power.")
E07|Dünyanın ucu|[warmly] “Sen karnını doyur. Gece gündüz sevin. Giysilerin temiz olsun, başını yıka. Elini tutan çocuğa bak. Karın koynunda sevinsin.”||OB S iii 6-13 ("Thou, O Gish, fill thy belly, Day and night do thou rejoice… Let thy clothes be clean, Wash thy head… Care for the little one who takes hold of thy hand! Let the wife rejoice in thy bosom!"). Yalnız Eski Babil sürümünde (ekran künyesi, anlatılmaz)
E08|Dünyanın ucu|[calmly] Gılgamış dinlemedi. Utnapiştim'in yolunu sordu.||Th X ii 16 ("which is the way unto Uta-Napishtim?")
E09|Dünyanın ucu|[calmly] Siduri onu kayıkçı Urşanabi'ye gönderdi: ölüm sularını geçebilen tek kişiye.||SB X 80-90. Urşanabi adı ve görüntüsüyle ilk yarıda ekilir (H'yi taşır)
E10|Dünyanın ucu|[calmly] Ölüm sularına eli değen ölürdü. Gılgamış ormandan uzun sırıklar kesti; her birini suya bir kez daldırıp bıraktılar.||Th X iii 40-iv 9; SB X 160-180. Sayı (120/300) kaynaklarda ayrışıyor, söylenmez
E11|Dünyanın ucu|[calmly] Sırıklar bitince Gılgamış giysisini çıkarıp yelken diye kaldırdı.||SB X 181-183; Th X iv 9-10
F01|Tufandan kurtulan adam|[calmly] Kıyıda Utnapiştim bekliyordu. Gılgamış ona baktı: kendisinden hiçbir farkı olmayan bir adamdı.||SB XI 2-6
F02|Tufandan kurtulan adam|[curious] “Sen nasıl ölümsüz oldun?”||SB XI 7
F03|Tufandan kurtulan adam|[calmly] Utnapiştim anlattı. Bir zamanlar tanrılar insanlığı bir tufanla silmeye karar vermişti. Bir tanrı ona fısıldadı: “Evini yık, bir gemi yap.”||SB XI 14-31 (Ea uyarır). Dinî karşılaştırma yapılmaz
F04|Tufandan kurtulan adam|[slowly] Altı gün yedi gece fırtına esti. Dindiğinde bütün insanlık kile dönmüştü.||SB XI 128-135 ("all the people had turned to clay"). Kil: B03'ün yankısı
F05|Tufandan kurtulan adam|[calmly] Ölümsüzlüğü tanrılar ona bir kez vermişti; yalnız ona.||SB XI 203-206
F06|Tufandan kurtulan adam|[firmly] “Peki senin için tanrıları kim toplayacak?” dedi Utnapiştim. “Haydi: altı gün yedi gece uyumadan dur.”||Th XI 197-199 ("Who will assemble the gods for thy (need)… Come, fall not asleep for six days, aye, a se'nnight!")
F07|Tufandan kurtulan adam|[softly] Gılgamış oturdu ve uyku hemen bir sis gibi üstüne çöktü.||Th XI 200-201 ("a sleep like a breeze breathed upon him"; George "like a mist")
F08|Tufandan kurtulan adam|[calmly] Utnapiştim karısına döndü: “İnsan aldatıcıdır; seni de aldatır. Her gün bir ekmek pişir, başucuna koy. Geçen günleri duvara çiz.”||SB XI 209-214; Th XI ("on the house-wall do thou mark it")
F09|Tufandan kurtulan adam|[calmly] Gılgamış uyandığında, “Gözüm daha yeni kapanmıştı,” dedi.||SB XI 219-222; Th XI
F10|Tufandan kurtulan adam|[slowly] Utnapiştim ekmekleri gösterdi. Birincisi taş gibi kurumuştu, ikincisi kösele gibiydi, üçüncüsü nemlenmiş, dördüncüsü beyazlamış, beşincisi küflenmiş, altıncısı tazeydi. Yedincisi hâlâ közdeydi.||SB XI 225-230 (George okuması; Th 1928 eski okuma: "unu toplandı, elendi…"). Somut kanıt
F11|Tufandan kurtulan adam|[thoughtful] Ölümü yenmeye gelen adam, bir uykuyu yenememişti.||Yorum, tek
F12|Tufandan kurtulan adam|[sad] “Ne yapayım Utnapiştim? Nereye gideyim? Yatak odamda ölüm oturuyor. Nereye ayak bassam, ölüm orada.”||Th XI 243-246 ("O, how shall I act, (or) where shall I hie me… Death in my bed-chamber broodeth, and Death is wherever I listen"); SB XI 244-246
G01|Yılan|[calmly] Utnapiştim onu yıkanmaya gönderdi. Gılgamış başını yıkadı, temiz giysiler giydi; tıpkı meyhanecinin öğüdündeki gibi.||Th XI 250-270 ("Lead him to where he may bathe… garb himself in a mantle"); E07'nin yankısı (anlatıcının gözlemi)
G02|Yılan|[curious] Tam yola çıkarken Utnapiştim bir sır verdi: denizin dibinde dikenli bir bitki vardı. Onu yiyen gençliğine dönerdi.||Th XI 266-270 ("a plant like a thorn… deep down in the ocean"); SB XI 278-286
G03|Yılan|[firmly] Gılgamış ayaklarına taş bağlayıp dibe daldı. Bitkiyi kopardı; dikenler elini kanattı. Taşları kesti, deniz onu kıyıya attı.||Th XI 271-278 ("Bound heavy stones on his feet… its prickles did scratch him… Cut he the heavy stones from his feet")
G04|Yılan|[warmly] Bitkiye bir ad verdi: “Yaşlı adam gençleşir.”||Th XI 283 ("'Greybeard-who-turneth-to-man-in-his-prime' is its name"); SB XI 298
G05|Yılan|[calmly] Hemen yemedi. “Uruk'a götüreceğim,” dedi kayıkçıya. “Önce bir yaşlıya deneyeceğim, sonra ben yiyeceğim.”||Th XI 280-284; SB XI 296-299
G06|Yılan|[calmly] Yolda serin sulu bir gölet gördü ve yıkanmak için içine indi.||Th XI 286-288 ("a pool of cool water, (and) therein descending Bathed")
G07|Yılan|[slowly] Bir yılan bitkinin kokusunu aldı. Sessizce çıktı, bitkiyi aldı götürdü. Giderken derisini geride bıraktı.||SB XI 305-307 (George: "as it went back it sloughed its skin"); Th 1928 eski okuma. L ana (A01) cevabı
G08|Yılan|[sad] Gılgamış oturdu ve ağladı. Gözyaşları yanaklarından aktı.||Th XI 290-291 ("Then Gilgamish sate him, (and) burst into weeping. Over his cheeks flow'd his tears")
G09|Yılan|[sad] “Urşanabi, kimin için yoruldu bu kollar? Kimin için tükendi yüreğimin kanı? Kendime hiçbir iyilik yapamadım. Bir yılana yaptım.”||Th XI 292-295 ("for whom have toiléd mine arms, O Ur-Shanabi… for whom hath my heart's blood been spent?… 'tis for an earth-lion (only)"); "toprak aslanı" = yılan (SB XI 311-314)
G10|Yılan|[slowly] Ve eve eli boş döndü.||A03'ün yankısı
H01|Surlar|[calmly] Uruk'a vardıklarında Gılgamış kayıkçıya döndü.||Th XI 303-305 ("to the middle of Erech, the high-wall'd, arrivéd. Gilgamish spake… to the boatman Ur-Shanabi")
H02|Surlar|[warmly] “Çık Urşanabi, Uruk'un surlarına, yürü. Temeline bak, tuğlalarını yokla. Tuğlaları fırında pişmemiş mi? Temelini yedi bilge atmamış mı?”||Th XI 306-308 ("go up and walk on the ramparts of Erech, Look on its base, and take heed of its bricks, if its bricks be not kiln-burnt"); SB XI 323-326 (yedi bilge)
H03|Surlar|[warmly] “Bir parça şehir, bir parça hurma bahçesi, bir parça kil çukuru. Hepsi Uruk.”||SB XI 327-328; Th XI 309-310 ("One shar the city, (and) one shar the gardens…")
H04|Surlar|[softly] Surun içinde ekmek pişiren fırınlar, hurma bahçeleri, birbirinin elini tutan insanlar vardı.||Görüntü E07 ve D04'ün yankısı (fırın, çocuk eli). Metin değil, anlatıcının görüntüsü
H05|Surlar|[warmly] Destan bu sözleri iki kez söyler: sonda kayıkçıya, ilk tablette de okuyana. “Çık Uruk'un surlarına, yürü, tuğlalarına bak.”||Halka yapı: SB I 18-21 = XI 323-326 (Fable önerisi 10: 'burada biter' çıkış işareti vermesin). H06 kimliği boş
H07|Surlar|[warmly] Ve: “Sedir sandığı bul. Tunç kilidini aç. Lacivert taştan tableti çıkar ve oku: Gılgamış'ın bütün çektiklerini.”||SB I 24-28 (George 2003; olgu, çeviri bizim). Th I 10 ("Graved on a table of stone all the travail")
H08|Surlar|[calmly] Bu hikâye kâtipten kâtibe, dilden dile geçti. Üç bin yıldan da önce, Hitit başkenti Hattuşa'da, bugün Çorum'un Boğazkale'sinde, üç ayrı dilde kopyaları yazıldı.||Hattuşa (Boğazköy): Akadca, Hurrice, Hititçe parçalar, MÖ 14.-13. yy (Beckman 2019). Türkiye kapısı, tek cümle
H09|Surlar|[slowly] Onu her okuyan, o yabancının yerine geçti. Bugün o yabancı sensin.||L1'in cevabı: yabancı = sonra gelen herkes
H10|Surlar|[thoughtful] Gılgamış aradığını bir yılana kaptırdı. Sen de öleceğini biliyorsun. Bir gün bir yabancıya hangi suru göstereceksin? Cevabını yorumlara yaz.||Başlığın sorusuna izleyicinin kendi cevabı; iksir
H11|Surlar|[warmly] Geçmişten bir tablet daha getirmemiz için Zaman Kuryesi'ne abone ol. Ölümün karşısında gülümseyen bir başka adam, Sisifos, ekranda.||Abone çağrısı son sahnenin içinde; bitiş ekranı (son 20 sn) "ekranda" sözcüğünü içerir
'''
def temiz(t): return re.sub(r'\s+', ' ', re.sub(r'\[[^\]]*\]', '', t)).strip()
seg = []
for ln in SATIR.strip().split('\n'):
    if not ln.strip(): continue
    p = ln.split('|')
    assert len(p) == 5, ln
    sid, bol, tts, alt, kay = [x.strip() for x in p]
    seg.append({'id': sid, 'bolum': bol, 'tts': tts, 'alt': alt or temiz(tts), 'kaynak': kay})
ids = [s['id'] for s in seg]; assert len(ids) == len(set(ids))
out = {'voice': 'Emrullah (ElevenLabs; voice_id creative_list_voices ile bulunur)',
       'revizyon': 'rev1 (23 Kasım 2026): Fable senaryo okuması uygulandı (uretim_plani.md §8)',
       'not': 'Kaynak: Gılgamış destanı. Kamu malı çeviriler kaynak/ altında (Jastrow ve Clay 1920; Thompson 1928). Standart sürümün satır numaraları George 2003 (olgu kaynağı). Çeviriler bizim. İskelet: Harmon çemberi (uretim_plani.md §5).',
       'segments': seg}
json.dump(out, open(os.path.join(ROOT, 'senaryo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
n = sum(len(s['tts']) for s in seg); w = sum(len(temiz(s['tts']).split()) for s in seg)
print(len(seg), 'cümle', n, 'karakter (tts, etiketli)', w, 'kelime; tahmini süre', round(w / 108, 1), 'dk')
