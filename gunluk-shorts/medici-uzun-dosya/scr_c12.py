"""c12 — Dük (1537–1574). Brif: brif/c12_brif.md. Parça 3'ün soğuk açılışı (önceki parça özeti ilk cümleye gömülü). Soğukkanlı-otoriter; 1562 AĞIR.
Mizah YALNIZ V2 (üç ayrı 29), V4 (ofisler), V8 (ünvan zinciri: kuruma/sisteme). V1, V3, V5, V6, V7, Lepanto ve ölüm MİZAH KAPALI.
Yıldız an: Kasım–Aralık 1562 (V6; tek tarih tek cümle). Karakter cümlesi (YORUM) V7 sonunda. 'Cosimo oğlunu öldürdü' kesin kipte ASLA. Cosimo–Porte diplomasisi kaynakta YOK.
Kapı: K1 (eşzamanlılık, nötr) → c13. Kesilenler (sığmadı): Cosimo'nun maddeyi reddi (○), gizli danışma kurulu (○), San Miniato kalesi, Bronzino portresi, Eleonora'nın yolculuk günleri."""
PRON = [
    (r"\bEleonora di Toledo\b", "Eleonora di Toledo"), (r"\bGarzia\b", "Gartsiya"),
    (r"\bMontemurlo\b", "Montemurlo"), (r"\bSanto Stefano\b", "Santo Stefano"),
    (r"\bAccademia delle Arti del Disegno\b", "Akkademya delle Arti del Dizenyo"), (r"\bVilla di Castello\b", "Villa di Kastello"),
    (r"\bLepanto\b", "Lepanto"), (r"\bFelipe\b", "Felipe"), (r"\bPius\b", "Pius"),
]

CH = dict(id="c12", n="XII", title="Dük", years="1537 – 1574", mood="cold", front="",
          paras=[[
              ("Ocak 1537'de bir dükü kuzeni öldürmüş, Senato da yerine 17 yaşında Cosimo'yu seçmişti.", None, "◐ M4b:b5 (Parça 3 özeti; c11 sonu)"),
              ("Ertesi gün Senato koşulu yazıya geçirdi: Cosimo dük olmayacak, yalnızca “kentin başı ve birincisi” diye anılacaktı.", None, "◐ M4b:b5,bD3,D14 (Treccani DBI; çeviri bize ait)"),
              ("Onu çağıran soylular muhtemelen yönetilebilir birini istemişti; Cosimo Mugello'da yetişmiş, şehirde pek tanınmayan bir çocuktu.", None, "◐ iskelet; \"yönetilebilir\" YORUM M4b:bD4,b6 (\"muhtemelen\" + gerekçe)"),
              ("Ağustos başında, Montemurlo'da, aceleyle toplanmış sürgün ordusunu yendi; Treccani bu zaferi cumhuriyetçi restorasyon tehdidinin sonu sayar.", None, "◐ olgu, ○ gün (31 Tem–2 Ağu) M4b:b8 (\"ağustos başı\")"),
          ], [
              ("1539'da Cosimo, İspanyol soylusu Eleonora di Toledo ile evlendi.", None, "◐ M4b:b10 (\"Pedro de Toledo\" HAFIZA, söylenmez)"),
              ("Sözleşme 29 Mart'ta Napoli'de imzalandı ve evlilik vekâleten kutlandı; Eleonora 29 Haziran'da Floransa'ya girdi, resmî düğün ise 29 Temmuz'da yapıldı.", None, "◐ M4b:b10,b11,b12,D9 (M4 #52 \"29 Haziran evlendi\" YANLIŞ)"),
              ("Yani Cosimo evlenmek için üç ayrı 29'a ihtiyaç duymuştu.", None, "◐ M4b:b10–b12 (mizah b: takvim/protokol)"),
              ("Yüzyılın ortasında Pitti Sarayı'nı Eleonora satın aldı.", None, "◐ M4b:b16; M3b:b80 (1549 ↔ 1550 → \"yüzyılın ortasında\")"),
          ], [
              ("26 Şubat 1548'de Venedik'te Lorenzino pusuya düşürülüp öldürüldü; emri Cosimo'nun verdiği uzun süre kabul edildi, yeni bir çalışma buna kuşku düşürüyor.", None, "◐ olgu / ○ yorum M4b:b15,bM3 (Dall'Aglio; kesin kip YOK)"),
              ("Siena yaklaşık on beş ay direndi ve açlıktan teslim oldu; 1557'de II. Felipe şehri Cosimo'ya bıraktı.", None, "◐ M4b:b18,b20 (\"nisan 1555\" gün ○)"),
          ], [
              ("1560'ta Cosimo, Vasari'den bir bina istedi: Floransa'ya dağılmış 13 idari makamı tek çatı altında toplayacaktı.", None, "◐ M3:#56,cd49"),
              ("Binanın adı da bunu söylüyordu: Uffizi, yani ofisler.", None, "◐ M3:cd49 (mizah a)"),
              ("Dünyanın en ünlü galerilerinden biri, doğduğunda bir memur binasıydı.", None, "YORUM (mizah a; c0 geri çağrısı)"),
              ("Üst galerisi 1565'te Palazzo Vecchio'yu Pitti Sarayı'na bağlayan koridora dönüştü: iktidarın ofisinden evine kapalı bir yol.", None, "◐ koridor; \"iktidarın ofisinden evine\" YORUM M3:cd50 (\"5 ay\", \"düğün için\" H)"),
              ("Müze olması çok sonra: bina halka ancak 1769'da açıldı.", None, "◐ M3:#64,#72; M3b:b76,b78 (\"ilk modern müze\" DENMEZ; Francesco/Tribuna ≈1581 söylenmez)"),
          ], [
              ("Cosimo bir de kendi şövalye tarikatını kurdu: Santo Stefano.", None, "◐ M4b:b21"),
              ("Papa 1561'de onayladı; 1562'de Pisa'da Cosimo, tarikatın büyük ustası olarak giydirildi.", None, "◐ M4b:b21 (1 Ekim 1561 / 15 Mart 1562 — günler ekranda)"),
              ("Kaynaklara göre amaç, Osmanlı ve korsan gemileriyle savaşmak ve Hristiyan esirleri kurtarmaktı; ganimet satışının Livorno'yu zenginleştirdiği yazılır.", None, "◐ amaç M4b:b21,b22 / ○ ganimet bM6 (esire mizah YOK; bagno ÇIKMADI)"),
          ], [
              ("Kasım 1562'de aile kıyıda bir geziye çıktı ve sıtmaya yakalandı.", None, "◐ M4b:b23,bM1 (tek tarih tek cümle; Zweig yavaşlatması)"),
              ("20 Kasım'da Cosimo'nun kardinal oğlu Giovanni öldü; on dokuz yaşındaydı.", None, "◐ M4b:b23"),
              ("Aralığın ilk yarısında kardeşi Garzia gitti; on beş ya da on altı yaşındaydı.", None, "◐ (6 ↔ 12 Aralık çelişir) M4b:b23,§5.1"),
              ("17 Aralık'ta Eleonora öldü: dört haftada üç ölüm.", None, "◐ M4b:b23 (\"27 gün\" hesap bize ait)"),
              ("Sonra bir hikâye doğdu: Garzia kardeşini, Cosimo da Garzia'yı öldürmüş. Rivayetin ilk yazanı bilinmiyor; ölümlerden çok sonra ortaya çıktı.", None, "ANEKDOT/◐ mit M4b:bM1 (\"rivayete göre\"; belge yok)"),
              ("1857'de mezar açıldığında Garzia'nın iskeletinde kırmızı atlas bir ceket vardı, şiddet izi yoktu; ölümlerin sıtmadan olduğu sonucuna varıldı.", None, "◐ M4b:b24,bD8,bM1 (2026 DNA çalışması GİRMEZ — D16)"),
              ("Cosimo'nun o haftalarda ne düşündüğünü bilmiyoruz.", None, "kalıp (bölümde 1; mektup yok)"),
          ], [
              ("13 Ocak 1563'te, Cosimo'nun desteğiyle, Vasari'nin yönetiminde Sanatlar Akademisi kuruldu: yarı lonca, yarı akademi, Medici devletindeki sanat üretimini denetleyen bir kurul.", None, "◐ M3:#57,cd51; M3b:b71 (Accademia delle Arti del Disegno; \"ilk\" DENMEZ)"),
              ("Michelangelo da kurumun başındaki adlardan biriydi; 1564'te ölünce cenazesini Akademi düzenledi.", None, "◐ M3:cd51,#60 (14 Temmuz San Lorenzo ekranda; \"mal gibi\" ANEKDOT söylenmez)"),
              ("Cosimo güzelliği de bir devlet dairesi gibi örgütledi.", None, "YORUM (karakter cümlesi)"),
          ], [
              ("1564'te Cosimo günlük yönetimi oğlu Francesco'ya bıraktı ama dük unvanını korudu.", None, "◐ M4b:b25"),
              ("1569'da V. Pius ona Büyük Dük unvanını verdi, 1570'te de Roma'da taç giydi.", None, "◐ M4b:b26,b27 (27 Ağustos 1569 / 5 Mart 1570 — ekranda; taç: bir kaynak Ocak 1570)"),
              ("İmparatorun onayı ancak yıllar sonra, para karşılığı geldi, diye anlatılır: kentin birincisi dük oldu, Roma ona taç verdi, Viyana fatura kesti.", None, "○ M4b:b27,bM5 (100.000 duka SÖYLENMEZ; mizah a: ünvan zinciri)"),
              ("7 Ekim 1571'de Lepanto'da, Türkçedeki adıyla İnebahtı'da, Hristiyan devletlerin yaklaşık iki yüz kadırgalık donanmasında, kaynaklara göre, Toskana'dan on iki gemi vardı.", None, "◐ 12 ↔ papalık hizmetinde/kiralanmış (iki anlatım) M4b:b28,T17 (şövalye ○ söylenmez; komutan H)"),
              ("Osmanlı donanması o gün ağır bir yenilgi aldı.", None, "HAFIZA-Y M4:T7 (yayın öncesi Türkçe/Osmanlı kaynakla teyit; kayıp rakamı verilmez; nötr ve saygılı)"),
              ("Cosimo, Nisan 1574'te Villa di Castello'da öldü.", None, "◐ yıl+yer; gün H M4b:b29"),
              ("Cosimo Floransa'da bir devlet kuruyordu. Aynı yıllarda Paris'te, Floransa doğumlu bir Medici kızı, adı 24 Ağustos 1572 ile anılacak bir krizin ortasındaydı.", None, "◐ tarih; sorumluluk tartışmalı → c13 M4b:b32–b35,bM7 (K1)"),
          ]])
