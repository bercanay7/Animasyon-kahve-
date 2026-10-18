"""c6 — Lorenzo (1449–1478). Brif: brif/c6_brif.md. Sıcak, hafif; sonda gölge (Giuliano). Giostra ve ölüm: mizah KAPALI. Görünüş/koku/ses alayı YOK."""
PRON = [
    (r"\bNiccolò Valori\b", "Nikkolo Valori"), (r"\bLucrezia Tornabuoni\b", "Lukretsya Tornabuvoni"), (r"\bPulci\b", "Pulçi"),
    (r"\bMorgante\b", "Morgante"), (r"\bPoliziano\b", "Politsyano"), (r"\bGiostra\b", "Costra"), (r"\bSanta Croce\b", "Santa Kroçe"),
    (r"\bMarco Vespucci\b", "Marko Vespuççi"), (r"\bBotticelli\b", "Botiçelli"), (r"\bVerrocchio\b", "Verrokyo"),
    (r"\bPerugino\b", "Peruçino"), (r"\bMagnifico\b", "Manyifiko"), (r"\bCondivi\b", "Kondivi"),
    (r"\bMichelangelo\b", "Mikelancelo"), (r"\bVita nova\b", "Vita nova"), (r"\bSimonetta\b", "Simonetta"),
]

CH = dict(id="c6", n="VI", title="Lorenzo", years="1449 – 1478", mood="warm", front="",
          paras=[[
              ("Lorenzo'yu en iyi dostu Niccolò Valori anlatır: doğa, görünüşü konusunda ona üvey ana gibi davranmış; ama zihne gelince şefkatli bir ana olmuş.", None, "◐ M5:K16; M3:C26 (özgün görülmedi → \"Valori'ye atfedilir\")"),
              ("Valori'ye göre yüzü güzel sayılmazdı, ama saygı uyandıracak kadar vakarlıydı.", None, "◐ M5:K16"),
              ("Ansiklopedilerin tarifi daha çıplak: basık burun, öne çıkık alt çene, zayıf görme.", None, "◐ M5:K15 (EI 1934; ten rengi ve ses söylenmez)"),
              ("Valori'ye göre koku bile alamıyordu.", None, "◐ zayıf M5:K19; M3:C27 (yayın öncesi teyit)"),
              ("Büyükbabası defter tutardı; torunu şiir yazdı.", None, "YORUM (Plutarkhos paraleli)"),
          ], [
              ("2 Aralık 1469'da babası Piero öldü; günler içinde yirmi yaşındaki Lorenzo şehrin ve devletin yükünü üstlendi.", None, "◐ ölüm / ○ \"günler içinde\" M5:P4,P6,K21"),
              ("Bunu hatıra defterinde, Ricordi'sinde, şöyle gerekçelendirir: dostlarını ve servetini korumak için; çünkü Floransa'da devletsiz zengin yaşamak zordu.", None, "◐ M5:K21 (\"Ricordi'ye göre\"; çeviri bize ait; PARA→İKTİDAR halkasının Lorenzo'dan teyidi)"),
              ("İsteksiz davrandığını, yaşını ve tehlikeyi gerekçe gösterdiğini de yazar; ama bunu anlatan yine kendisi.", None, "◐/○ M5:K21 (kendi imajı uyarısı)"),
          ], [
              ("Annesi Lucrezia Tornabuoni bir şairdi: dua şarkıları ve beş manzum anlatı yazdı, Pulci'nin dostuydu, Morgante'ye ilham verdi.", None, "◐ M5:K10,K11"),
              ("Oğluna eş seçmeyi de kendisi üstlendi: 1467 baharında Roma'da Clarice'yi görüp Piero'ya üç mektup yazdı.", None, "◐ M5:K13,P5"),
              ("28 Mart tarihli ilk mektupta kızın uzun boylu, narin, açık tenli ve bol saçlı olduğunu, yüzünün çok güzel olmasa da hoş olduğunu yazar.", None, "◐ \"aktarılır\" M5:K13; M2:C6.1 (Salvadori edisyonu; çeviri bize ait)"),
              ("Lorenzo evliliği defterine şöyle geçirir, diye aktarılır: Clarice'yi aldım ya da bana verildi.", None, "○ M5:K27 (mizah b; hedef evlilik pazarı, Clarice değil)"),
              ("Roma'da vekâletle nikâh kıyıldıktan sonra düğün şenlikleri 4 Haziran 1469'da Floransa'da başladı.", None, "◐/○ M5:P6,P8"),
              ("Clarice, 1479'da çocuklarının hocası Poliziano'yu evden çıkarttı; ona uygun bir eğitmen olmadığına ikna olmuştu.", None, "◐ M5:K25 (iki Treccani maddesi)"),
          ], [
              ("Lorenzo'nun çevresinde okul yoktu, atölyeler vardı: Verrocchio'nun atölyesinden Leonardo, Perugino ve Botticelli geçtiği söylenir.", None, "◐ atıflar zor M3:K40,Y10 (\"Medici sanat okulu\" DENMEZ)"),
              ("1476 ile 1477 arasında Lorenzo ve Poliziano, Napoli'nin isteğiyle bir Toskana şiir derlemesi hazırladı; içinde Dante'nin Vita nova'sı da vardı.", None, "◐ M3:K43,C43"),
              ("“Muhteşem”, yani Magnifico, bir saygı sözcüğüydü; Machiavelli Prens'i Lorenzo'nun önce oğluna, sonra torununa ithaf etti ve ikisine de “Muhteşem” diye seslendi.", None, "◐ kullanım M3b:bd13,b52,bm6; HAFIZA-D unvan genelliği → \"kullanılırdı\" (mizah a: unvan enflasyonu)"),
          ], [
              ("Michelangelo'nun biyografisini yazan Condivi'ye göre Lorenzo, genç sanatçının yonttuğu yaşlı faunun başına şaka yapmış: yaşlıların dişleri tam olmaz.", None, "ANEKDOT ◐ M3:C31,b102,bd23 (Condivi 1553; \"sarayında büyüdü\" DENMEZ)"),
              ("Michelangelo bir dişi kırıp diş etini oymuş; Lorenzo da onu eve almış: oda, sofra, ayda beş dukat.", None, "ANEKDOT ◐ M3b:b101,bd24 (\"anlatılır\")"),
          ], [
              ("29 Ocak 1475'te Santa Croce Meydanı'nda, Venedik ve Milano'yla ittifakı kutlamak için büyük bir turnuva yapıldı: Giostra.", None, "◐ M5:K23; M3:K41"),
              ("Kazanan Lorenzo değil, kardeşi Giuliano'ydu; seçtiği kadın, Marco Vespucci'nin eşi Simonetta'ydı.", None, "◐ M5:K23,P7; M3:D11"),
              ("Botticelli sancağa Simonetta'yı miğferli bir Pallas olarak resmetmişti; asıl sancak kayıp.", None, "◐ olay / ○ görünüş M3:C36 (\"anlatılır\")"),
              ("Poliziano bu günü bir şiire döktü; şiir, kahramanı ölünce yarım kaldı.", None, "◐ M5:K23 (Stanze per la giostra)"),
              ("Simonetta, 1476 Nisanında yirmi üç yaşında veremden öldü; Giuliano'yla sevgili olup olmadıklarını bilmiyoruz.", None, "◐ M5:K23; M3:K42 (\"bilmiyoruz\" kalıbı)"),
              ("Lorenzo yıllar sonra bir karnaval şarkısına şunu yazacaktı: ne güzel şey gençlik, ama kaçıp gidiyor.", None, "◐ tarih/biçim M3:K52,C42 (1490; çeviri bize ait; sahneye bağlama YORUM)"),
          ], [
              ("Giostra'dan 26 Nisan 1478'e, bir Pazar sabahına, üç yıl üç ay vardı.", None, "◐ M2:K45; hesap bize ait (\"Paskalya\" DEĞİL, Pazar ayini)"),
              ("Giuliano yirmi dört yaşında ölecekti.", None, "◐ M5:P7,D24 (Zweig: izleyici bilir, kahraman bilmez; bölümde tek kullanım)"),
          ]])
