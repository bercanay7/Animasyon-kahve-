"""c10 — Rahip ve Kral (1492–1498). Brif: brif/c10_brif.md. AĞIR/Zweig'ci. Mizah YALNIZ V6 (Botticelli miti: kaynak yokluğuna, 1–2 dokunuş). V1, V4, V7 MİZAH KAPALI.
Yıldız an: 9 Kasım 1494 (Pazar) — saat/ışık/ÇAN YOK. Zweig ironisi bölümde tek (V4 yansıma 1434→1494). İç dünya kalıbı tek (V4, Piero). "Beceriksiz" kesin kipte söylenmez.
Kapı: K1 (dramatik ironi; bölümün tek 'tanrısal kesinlik' hakkı) → c11. Söylenen sayı ≤6: 43 · 3 · 3.000 · 5 · 2 · 60."""
PRON = [
    (r"\bPico della Mirandola\b", "Piko della Mirandola"), (r"\bPico\b", "Piko"), (r"\bGirolamo\b", "Cirolamo"),
    (r"\bSavonarola\b", "Savonarola"), (r"\bBologna\b", "Bolonya"), (r"\bSarzana\b", "Sartsana"),
    (r"\bPisa\b", "Piza"), (r"\bLuca Corsini\b", "Luka Korsini"), (r"\bLanducci\b", "Landuççi"),
    (r"\bCapponi\b", "Kapponi"), (r"\bPonte Vecchio\b", "Ponte Vekkyo"), (r"\bPiagnoni\b", "Pyanyoni"),
    (r"\bCharles\b", "Şarl"), (r"\bBernardo del Nero\b", "Bernardo del Nero"),
]

CH = dict(id="c10", n="X", title="Rahip ve Kral", years="1492 – 1498", mood="heavy", front="",
          paras=[[
              ("Nisan 1492'de Lorenzo, 43 yaşında, rahatlama umuduyla taşındığı Careggi villasında öldü.", None, "◐ M4c:A02,D47; \"43\" = M5 hesap (gün söylenmez: 8 ↔ 9 Nisan)"),
              ("Başucunda iki dostu vardı: şair Poliziano ve genç filozof Pico della Mirandola.", None, "◐ DBI (c. 73) M4c:C01"),
              ("Poliziano'nun mektubuna göre Lorenzo, Pico'ya, kütüphanesi bitmeden ölümün kendisini esirgemesini dilediğini söyledi.", None, "◐ iki özet; mektup metni GÖRÜLMEDİ M4c:C04,D49 (\"mektuba göre\"; 1494 el koyma söylenmez — ekranda boş raf)"),
              ("Savonarola da oradaydı; Poliziano'ya göre Lorenzo'nun günah çıkarmasını dinledi.", None, "◐ üç özet M4c:C02,D48 (opsiyonel; kutsama ayrıntısı söylenmez)"),
              ("Yıllar sonra rahibin yandaşları başka bir sahne anlattı: üç şart, ikisine evet, üçüncüde, Floransa'ya özgürlük verilmesinde, duvara dönmüş bir yüz.", None, "ANEKDOT ◐ Burlamacchi/G. F. Pico/Razzi M4c:C03,§5.1 (rivayet; birebir söz yok)"),
              ("Oysa Poliziano'nun mektubunun özetlerinde ne üç şart geçiyor ne de duvar.", None, "◐ üç özet; mektup görülmedi M4c:D48 (yayın öncesi teyit)"),
          ], [
              ("Girolamo Savonarola, 1475'te, genç yaşta, tıp öğrenimini bırakıp Bologna'da Dominiken tarikatına girdi; oraya yürüyerek gittiği yazılır.", None, "◐ M4c:A05,C07,D65"),
              ("1491'de manastırın başına geçti; 1494'e doğru kürsüde bir kılıçtan, bir kırbaçtan, bir tufandan söz ediyordu.", None, "◐ Britannica + Symonds M4c:A08,C06,D53 (\"yazılır\"; 1491'e koyma)"),
              ("Papa'nın ona kardinal şapkası önerdiği, onun da kırmızı yerine kandan bir şapka istediğini söylediği aktarılır.", None, "ANEKDOT ○ Britannica M4c:C08,D65,§5.6 (tırnaksız; birebir söylenmez)"),
          ], [
              ("Babasının yerine genç Piero geçti; konseyler onu itirazsız ama destek gösterisi olmadan onayladı.", None, "◐ M4c:A09,D54 (yaş 20 = M5)"),
              ("Babasının kurduğu denge çözülüyordu: 1493'te kurulan bir ittifakın dışında Floransa ve Napoli kalmıştı.", None, "◐ DBI Orsini + Cambridge M4c:A11,D54 (üyeler söylenmez)"),
              ("Piero görüşmeyi kendi eliyle yürütmek istedi; ekimin sonunda, Sarzana'daki Fransız kampında, şehrin kalelerini Signoria'ya sormadan krala bıraktı.", None, "◐ Treccani/Cambridge M4c:A13,D55 (kale sayısı, gün söylenmez; \"beceriksiz\" DENMEZ)"),
          ], [
              ("9 Kasım 1494, bir pazar.", None, "◐ Landucci ikincil + Cambridge M4c:A14,D56 (saat/çan YOK)"),
              ("Piero, Fransız kampından dönmüş, silahlı adamlarıyla Palazzo Vecchio'ya girmek istiyordu.", None, "◐ M4c:A14,A15"),
              ("Kapı yüzüne kapandı; kapıyı Signoria üyesi Luca Corsini'nin kapattığı anlatılır.", None, "○ tek özet M4c:A15,D56 (\"anlatılır\")"),
              ("Piero'ya bir saat içinde huzura çıkması emredildi.", None, "◐ Cambridge M4c:A15,A17"),
              ("Ne düşündüğünü bilmiyoruz; ama ne yaptığını biliyoruz: huzura çıkmadı, şehirden kaçtı; ilk durağının Bologna olduğu yazılır.", None, "kalıp (bölümün tek iç-dünya kalıbı); ○ Bologna yolu M4c:D56 (\"atına atlayıp\" ANEKDOT — söylenmez)"),
              ("Meydanda, yazıldığına göre, eski çağrı yükseldi: halk ve özgürlük.", None, "◐ Landucci'ye atfen ikincil M4c:A15,D56 (çeviri bize ait)"),
              ("Kardinal kardeşi Giovanni de, sade bir Fransisken rahibi kılığında şehirden çıktı.", None, "◐ DBI Leone X + Cambridge M4c:A18,D57 (gün/kapı çelişir → söylenmez; kılığa alay YOK)"),
              ("Altmış yıl önce, 1434'te, aile bir sürgünden zaferle dönmüştü. Şimdi gidiş sırası onlardaydı.", None, "◐ 1434 (c3) + hesap bize ait; YORUM yansıma (Zweig ironisi, bölümde tek)"),
          ], [
              ("Birkaç gün sonra, 17 Kasım'da, Charles Floransa'ya girdi; mızrağı yatay tutan bir fatih gibi, diye anlatılır.", None, "◐ gün / ○ mızrak M4c:A19,D58"),
              ("Şehrin müzakerecilerinden Piero Capponi, kralın şart taslağını önünde yırttı; karşılığında trompetlere çanlarla yanıt vereceklerini söylediği aktarılır.", None, "◐ yırtma Treccani; lafız ANEKDOT ○ M4c:A20,§5.5 (birebir söz yok)"),
              ("Aralıkta kurulan yeni düzenin merkezinde Venedik'ten esinlenen Büyük Konsey vardı; üç binden fazla yurttaşa açıktı.", None, "◐ Treccani ×2 + Oxford M4c:A24,D60 (\"açıktı\" = uygunluk)"),
              ("Yeni biçimin seçilmesinde Savonarola'nın payının belirleyici olduğu yazılır.", None, "◐ Treccani Savonarola maddesi + Britannica M4c:A25 (Pisa elçiliği / kralı yağmadan caydırdı: söylenmez)"),
          ], [
              ("7 Şubat 1497'de, Karnaval günlerinde, Signoria Meydanı'nda ilk ateş yakıldı.", None, "◐ M4c:A26,D61 (bir kaynak 8 Şubat)"),
              ("Ateşe ayna, peruk, kozmetik, iskambil, zar ve çalgılar atıldı; bir listede resim ve heykel de geçer.", None, "◐ Nardi + Yale seçkisi M4c:A26,C12,D61 (\"listeye göre\")"),
              ("Botticelli'nin kendi tablolarını bu ateşe attığı sık anlatılır; kimse hangi tabloyu yaktığını göstermiyor.", None, "◐ M3:#46–47,§5.12 + Britannica M4c:A28,§5.2,D61 (mizah a: kaynaksız mit)"),
              ("Hikâye ateşten çabuk yayıldı: bugün bile “Botticelli'lerin Ateşi” diye başlayan yazıların kaynakları geç ve zayıf.", None, "◐ M3:#47 M4c:§5.2 (mizah b + c, tek)"),
              ("Britannica'ya göre sanat ve kitap yıkımı önemsizdi.", None, "◐ M4c:D61 (\"Britannica'ya göre\")"),
              ("Aynı kürsüden hem yeni bir meclis hem de ilk ateş çıktı.", None, "YORUM Treccani (Konsey) + Nardi (ateş) M4c:A25–A26 (Savonarola portresinin adil kapanışı)"),
          ], [
              ("Ağustos 1497'de Medici'yi geri getirmeyi hedefleyen bir komplo ortaya çıktı; Bernardo del Nero dahil 5 kişi, Büyük Konsey'e başvuru hakkı tanınmadan idam edildi.", None, "◐ Treccani ×2; temyiz Johnson M4c:A30,A31,D63 (gün 21 ↔ 23 söylenmez)"),
              ("7 Nisan 1498'de Savonarola'nın sözlerini ateşle sınayacak bir gösteri planlandı; gösteri hiç yapılmadı.", None, "◐ Britannica M4c:A32,D64 (ayrıntı — Fransisken/Domenico, yağmur, pazarlık — anlatılmaz)"),
              ("Ertesi gün San Marco kuşatıldı ve Savonarola tutuklandı.", None, "◐ Britannica M4c:A33 (Palm Pazarı hesap)"),
              ("23 Mayıs 1498 şafağında Savonarola ve iki Dominiken arkadaşı ayine katıldı, komünyon aldı; sonra asıldılar, bedenleri meydanda yakıldı.", None, "◐ üç DBI maddesi M5:K29; M4c:A34,C14 (gün 22 ↔ 23 tek özet; şiddet gösterilmez)"),
              ("Külleri Ponte Vecchio'dan Arno'ya atıldı; gerekçenin, kimsenin yadigâr saklamaması olduğu yazılır.", None, "◐ DBI + Britannica M4c:A34 (gerekçe \"yazılır\")"),
          ], [
              ("Fransisken kılığında kaçan kardinal, bir gün aynı şehre bir ordunun arkasından dönecekti.", None, "◐ DBI Leone X M4:#3–#5; M4c:A18 (K1; \"on sekiz yıl\" c11'de; bölümün tek tanrısal kesinlik hakkı)"),
          ]])
