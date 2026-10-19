"""c11 — Papa Oğulları (1512–1537). Brif: brif/c11_brif.md. AĞIR bölüm: mizah yalnız V2–V3'te (kurum/kibir); V1 ve V4–V8 KAPALI.
Yıldız anlar: 6 Mayıs 1527 (saat/hava/koku YOK), 5–6 Ocak 1537. Şarlken bağı TEK cümle (V4 başı)."""
PRON = [
    (r"\bSoderini\b", "Soderini"), (r"\bClemens\b", "Klemens"), (r"\bRaffaello\b", "Rafaello"), (r"\bAlbrecht\b", "Albreht"),
    (r"\bFugger\b", "Fugır"), (r"\bBourbon\b", "Burbon"), (r"\bOrange\b", "Oranj"), (r"\bPassetto di Borgo\b", "Passetto di Borgo"),
    (r"\bCastel Sant'Angelo\b", "Kastel Sant'Ancelo"), (r"\bCastel\b", "Kastel"),   # "Castel" tek başına: yukarıdaki satırdan SONRA
    (r"\bMainz\b", "Mayns"), (r"\bLuther\b", "Lüter"), (r"\bFabrizio\b", "Fabritsyo"), (r"\bd'Este\b", "deste"),
    (r"\bFerruccio\b", "Ferruçço"), (r"\bMaramaldo\b", "Maramaldo"),
    (r"\bLorenzino\b", "Lorentsino"), (r"\bBrutus\b", "Brütüs"), (r"\bSan Miniato\b", "San Minyato"), (r"\bGavinana\b", "Gavinana"),
    (r"\bAlessandro\b", "Alessandro"), (r"\bHanno\b", "Hanno"),
]

CH = dict(id="c11", n="XI", title="Papa Oğulları", years="1512 – 1537", mood="heavy", front="",
          paras=[[
              ("29 Ağustos 1512'de İspanyol ordusu Prato'yu alıp yağmaladı; ordunun yanında, papalık elçisi sıfatıyla, Medici'den bir kardinal vardı: Lorenzo'nun oğlu Giovanni.", None, "◐ M4:#3 (mizah KAPALI)"),
              ("Günler sonra Papa'ya yazdığı mektupta olanları “başkalarına örnek ve dehşet” diye anlattığı aktarılır.", None, "○ M4:3B#1 (İngilizce ikincil aktarım; çeviri bize ait; ölü sayısı söylenmez)"),
              ("Cumhuriyetin başındaki Soderini'nin yönetimi düştü ve Medici, sürgüne gönderilişinden yaklaşık on sekiz yıl sonra, eylülde Floransa'ya döndü.", None, "◐ M4:#4,#5 (\"on sekiz yıl\" hesap bize ait)"),
          ], [
              ("Giovanni daha çocukken, yazıldığına göre on üç yaşında, kardinal yapılmıştı; mart 1513'te, otuz yedi yaşında, yalnızca iki oylamada papa seçildi: X. Leo.", None, "○ 13 yaş M4:#2 (\"yazıldığına göre\") / ◐ 37 yaş, 2 oylama M4:#7,#9"),
              ("11 Nisan 1513'te Lateran'a giden alay, Giovanni'nin bir yıl önce Ravenna'da esir düştüğü günün yıldönümüne denk geliyordu.", None, "○ M4:#11,3B#3 (\"anlatılır\")"),
              ("Papa'nın beyaz atını, aforozlu Alfonso d'Este'nin yedekten yürüttüğü anlatılır.", None, "○ Schaff→Pastor IV (tek eski ikincil); M4:3B#3 (cümle artık \"anlatılır\" kipinde; maliyet söylenmez; mizah a)"),
          ], [
              ("Medici'nin artık papası vardı ama bankası yoktu; ailenin mülkü 1494'te kayyumlara devredilmişti.", None, "◐ M1b:b67,U33; M4:D3"),
              ("Leo borçlu öldü; alacaklıları arasında Bini, Gaddi, Salviati ve Strozzi adları geçer, Medici bankasının adı geçmez.", None, "○ M4:3B#6,D3 (Pastor; \"geçer\")"),
              ("1514'te Portekiz Kralı Papa'ya Hanno adında bir fil gönderdi.", None, "◐ M4:#12,3B#4"),
              ("Fil iki yıl sonra ölünce Leo ona uzun bir mezar yazıtı yazdı ve Raffaello'dan anma freski istedi; evet, fil için.", None, "◐ M4:3B#4 (mizah a+b; altınlı müshil rivayeti söylenmez)"),
              ("Mainz Başpiskoposu Albrecht, başpiskoposluk için Fugger'den borç almıştı; çözüm basitti: günah affı gelirinin yarısı Roma'ya, yarısı Fugger'e gidecekti.", None, "◐ M4:#14,3B#5 (kredi tutarı söylenmez; mizah a)"),
              ("Vaizin yanında, payını toplamak için bir Fugger memuru dururdu; bugünkü adıyla komisyoncu.", None, "◐ M4:3B#5 (mizah c, tek)"),
              ("Leo 1 Aralık 1521'de öldü; zehir söylentisinin kanıtı yok, hastalığın olasılıkla sıtma olduğu düşünülür.", None, "◐ ölüm / ○ söylenti M4:#19,§5.3"),
          ], [
              ("X. Leo'nun papalığında Luther itiraz etmişti; Giuliano'nun ölümünden bir ay sonra doğan oğlu Giulio'nun, yani VII. Clemens'in papalığında ise Roma'ya Şarlken'in, yani V. Karl'ın ordusu girdi.", None, "◐+◐ M4:#16,#25; M5:K24,P12 (c7s45 sonucu: Giulio = Clemens; ŞARLKEN CÜMLESİ, tek)"),
              ("6 Mayıs 1527'de Roma'ya giren ordu imparatorundu ama maaşını alamıyordu; Britannica'ya göre saldırı, imparatorun emriyle değil, ödenmeyen askerlerin inisiyatifiyle gelmişti.", None, "◐ M4:#25 (kaynak adıyla)"),
              ("Komutan Bourbon Dükü, saldırının başında ölümcül yaralandı.", None, "◐ M4:#25 (kimin vurduğu söylenmez)"),
              ("Papa'yı koruyan İsviçre Muhafızı'nın yüz seksen dokuz kişisinden yüz kırk yedisi öldü.", None, "◐ M4:#25,3B#8 (ekran: 189 → 147 → 42)"),
              ("Sağ kalan kırk iki kişi, Papa'yı Passetto di Borgo geçidinden Castel Sant'Angelo'ya götürdü.", None, "◐ M4:#25"),
              ("Kaçarken beyaz cüppesi düşman arkebüzcülerinin gözüne çarpmasın diye üstüne bir pelerin atıldığı anlatılır.", None, "○ ANEKDOT M4:3B#9,§5.6 (kim attı/renk söylenmez)"),
              ("Yağma aylarca sürdü; ölü sayısı için verilen rakamlar çok geniş bir aralıkta değişir.", None, "○ M4:#29; ◐ aralık M4:§4 (rakam söylenmez)"),
          ], [
              ("1527'de Floransa Medici'yi bir kez daha kovup cumhuriyeti yeniden kurdu; Castel'de teslim olan Papa ise fidye ödenene dek orada kaldı.", None, "◐ M4:#26,#27"),
              ("Papa aralıkta kılık değiştirip kaçtı; kılığı bir kaynakta seyyar satıcı, bir başkasında tüccar olarak anlatılır.", None, "◐ M4:#28,3B#13 (\"Ne düşündüğünü…\" kalıbı c8/c10'da kaldı; üçüncü tekrar düz anlatıma çevrildi)"),
              ("Esaretten sakalıyla çıktı ve onu ömür boyu taşıdı; bazıları bunu bir yas sakalı sayar.", None, "○ M4:3B#12,§5.7 (\"yazılır\"; \"yas\"=YORUM; \"ilk sakallı papa\" DENMEZ)"),
          ], [
              ("Clemens, imparatorun ordusunun yardımıyla ailesini Floransa'ya geri getirmeye hazırlanıyordu; 24 Ekim 1529'da ordu, Orange Prensi komutasında şehri kuşattı.", None, "◐ M3b:b40; M4:#33"),
              ("Cumhuriyet surların başına bir heykeltıraş koymuştu: Michelangelo istihkâmların genel sorumlusuydu, üstelik Medici'nin mezar şapelini de üstlenmiş olan aynı adamdı.", None, "◐ M4:#30,#17; M3b:b40,b32 (Zweig ironisi)"),
              ("Michelangelo San Miniato çan kulesinin dışını yün balyalarıyla sardırdı ve tepeye iki top çıkarıldı.", None, "◐ M4:3B#14 (\"anlatılır\"; San Niccolò ≠ San Miniato)"),
              ("Eylülde, kuşatma başlamadan, Venedik'e kaçtı; Floransa onu haydut ilan edip mallarına el koydu; kasımda döndüğü anlatılır.", None, "◐ kaçış / ○ ilan, dönüş M3b:b41; M4:#32"),
          ], [
              ("3 Ağustos 1530'da Gavinana'da Orange Prensi göğsüne iki kurşun yiyerek öldü; Floransa'nın komutanı Francesco Ferruccio ise yaralı yakalandı ve Fabrizio Maramaldo tarafından öldürüldü.", None, "◐ M4:#37"),
              ("Ferruccio'nun son sözleri üç ayrı biçimde aktarılır; Maramaldo'nun adı ise İtalyancada güçsüze saldıran alçak anlamında bir sözcüğe dönüştü.", None, "◐ M4:§5.9 (\"aktarılır\"; tırnak yok)"),
              ("Cumhuriyet teslim olunca Michelangelo bir süre saklandı; saklandığı yerin Yeni Sakristi'nin altındaki bir oda olduğu da söylenir. Papa onu bağışladı, ama bir şartla: Yeni Sakristi'ye dönecekti.", None, "◐ M3b:b42,b43,bm8 (iki gelenek: Yeni Sakristi altı ↔ San Niccolò; \"söylenir\"; cumhuriyetin teslimi eklendi)"),
              ("1975'te, Yeni Sakristi'nin altındaki iki kat sıva kalkınca, duvarları kömür çizimlerle dolu bir oda çıktı ortaya; çizimleri Michelangelo'ya bağlamak tartışmalıdır.", None, "◐ M3b:b44,bd18 (restoratör iki kat sıva; atıf tartışmalı; Zweig yavaşlatması)"),
          ], [
              ("Alessandro, V. Karl'ın desteğiyle 1532'de kalıtsal dük oldu ve 1536'da imparatorun kızıyla evlendi.", None, "○ destek M4:#40; ◐ M4:#43,#47 (kökeni girilmez)"),
              ("5 Ocak 1537 gecesi kuzeni Lorenzino ona kendi dairesinde bir buluşma vaat etti; Alessandro adamlarını göndermiş, odada uyuyakalmıştı.", None, "◐ M4b:b1 (saat/mum/şafak YOK; \"bir kadın\" ayrıntısı girilmez)"),
              ("Lorenzino hizmetkârıyla döndü; kılıç ve hançerle öldürdüler, Alessandro şiddetle direndi.", None, "◐ M4b:b1 (parmak ısırma ANEKDOT: söylenmez; şiddet gösterilmez)"),
              ("Lorenzino Venedik'e kaçtı ve kendini Brutus'a benzetti; İtalyan Ansiklopedisi Treccani buna siyaset değil, özel intikam der.", None, "◐ M4b:b4 (parçada ilk Treccani → kısa tanım)"),
              ("9 Ocak'ta Kırk Sekizler Senatosu, on yedi yaşındaki Cosimo'yu seçti.", None, "◐ M4b:b5 (c11'in son olgu cümlesi)"),
              ("Floransa'da pek tanınmayan bu çocuk, otuz yedi yıl hüküm sürecekti.", None, "◐ M4b:§5.1 (37 yıl hesap bize ait; K3 → c12 kapısı = Parça 2 kancası)"),
              ("Nasıl?", None, "—"),
          ]])
