"""c4 — Kubbe ve Kefaret (1418–1460'lar). Brif: brif/c4_brif.md. Orta-hafif, mizah serbest (kuruma/kibre/sistem). Soru: sipariş kefaret mi, yatırım mı? → açık bırakılır."""
PRON = [
    (r"\bBrunelleschi\b", "Brunelleski"), (r"\bGhiberti\b", "Giberti"), (r"\bArte della Lana\b", "Arte della Lana"),
    (r"\bIV\. Eugenius\b", "Dördüncü Evgenius"), (r"\bEugenius\b", "Evgenius"), (r"\bDufay\b", "Düfey"),
    (r"\bTerribilis est locus iste\b", "Terribilis est lokus iste"), (r"\bVespasiano da Bisticci\b", "Vespazyano da Bistiççi"),
    (r"\bVespasiano\b", "Vespazyano"), (r"\bFra Filippo Lippi\b", "Fra Filippo Lippi"), (r"\bVasari\b", "Vazari"),
    (r"\bBenzoni\b", "Bentsoni"), (r"\bKolomb\b", "Kolomb"), (r"\bGiovanni Rucellai\b", "Covanni Ruçellay"), (r"\bRucellai\b", "Ruçellay"),
    (r"\bDominiken\b", "Dominiken"), (r"\bSan Marco\b", "San Marko"), (r"\bSan Lorenzo\b", "San Lorentso"),
    (r"\bstrozziere\b", "strottsyere"), (r"\bPazzi\b", "Pattsi"), (r"\bMagi\b", "Maci"), (r"\bRicordi\b", "Rikordi"),
]

CH = dict(id="c4", n="IV", title="Kubbe ve Kefaret", years="1418 – 1460'lar", mood="warm", front="",
          paras=[[
              ("Floransa'nın silüetine bugün de damgasını vuran kubbeyi Medici yaptırmadı.", None, "◐ M3:D1,§5.2"),
              ("Katedralin yapımı yün loncasının denetimindeydi; lonca kumaştan anlıyordu, kubbeden değil, o yüzden yarışma açtı.", None, "◐ M3:K1,K3,D1 (ilk yarı YORUM; mizah a)"),
              ("Ağustos 1418'de ilan çıktı: kullanılacak modele iki yüz altın florin ödül, teslim eylül sonuna kadar.", None, "◐ M3:K2,S1,S2"),
              ("1420 baharında Brunelleschi'nin tasarımı seçildi; Ghiberti'yle birlikte işin başına geçti.", None, "◐ M3:K4"),
          ], [
              ("Vasari'ye göre Brunelleschi, rakiplerine yumurtayı mermer üstünde dik durdurmalarını söylemiş; kimse başaramayınca tabanını kırıp dikmiş.", None, "ANEKDOT ○ M3:C8,§5.3 (\"Vasari'ye göre\")"),
              ("Rakipler “bunu biz de yapardık” deyince, planı görselerdi kubbeyi de yaparlarmış diye karşılık vermiş.", None, "ANEKDOT ○ M3:C8"),
              ("Aynı yumurta 1565'te Benzoni'nin kaleminde Kolomb'a bağlanır; kim kimden aldı, bilmiyoruz.", None, "○ M3b:b105,bm9 (mizah a)"),
          ], [
              ("25 Mart 1436, Floransa takvimine göre yılbaşı.", None, "◐ M3:K7"),
              ("Papa IV. Eugenius katedrali kutsadı.", None, "◐ M3:K7 (\"kubbe bitti\" DENMEZ: ayrı olay)"),
              ("Papa'nın özel korosu, Dufay'in bu tören için yazıldığı kabul edilen motetini söyledi.", None, "◐ M3:K7,C9 (\"kabul edilir\")"),
              ("Tenorlardan birinde kutsama ayininin ezgisi vardı: Terribilis est locus iste, yani “Ne heybetli bu yer.”", None, "◐ M3:C9 (çeviri bize ait)"),
              ("Kubbe yıllar süren bir işçilikle, ahşap kalıp kullanılmadan örülmüştü; kaynaklar böyle aktarır.", None, "◐ rehber/blog düzeyi M3:K6,S4,D2 (\"iskelesiz\" DENMEZ)"),
              ("Medici'nin belgeli Brunelleschi'si ise hemen yanındaki San Lorenzo'daydı: Eski Sakristi.", None, "◐ M3:D1,K5,§5.2"),
          ], [
              ("Cosimo'nun kitapçısı Vespasiano, ölümünden sonra şunu yazar: Cosimo'nun vicdanında hayli şey birikmişti, devlet yönetip başkalarının önüne geçmek isteyen çoğu adamın başına geldiği gibi.", None, "ANEKDOT ◐ M1:D26,M3:C1,C3 (Vespasiano ≈1495, övgücü; yazar sesi; mizah a)"),
              ("Bu yükü atmak için Papa'yla konuşmaya gitmiş.", None, "ANEKDOT ◐ M3:C1"),
              ("Papa ona San Marco'daki Dominiken manastırını yaptırmasını, on bin florin harcamasını önermiş.", None, "ANEKDOT ◐ M3:C2,M1:K43 (\"önermiş\")"),
              ("On bin yetmemiş; Cosimo işi bitirmek için kırk binden fazla florin harcamış.", None, "ANEKDOT ◐ M3:C2,S9"),
              ("“Kefaret” kelimesi ise sonradan, modern bir yazarın cümlesi; Papa'nın kendi sözü olarak kayıtlı değil.", None, "◐ M1:D31,K43,mit7"),
              ("Keşiş değildi ama bağışı sayesinde San Marco'da iki hücresi vardı: biri kendine, biri önemli konuklara.", None, "◐ M3:C5,K11 (mizah b)"),
              ("Evet, konuk odası o zaman da kıyakmış.", None, "YORUM"),
          ], [
              ("Medici tek değildi.", None, "—"),
              ("Giovanni Rucellai kendi defterine yazdı: elli yıl hep kazanıp harcamış, harcamayı kazanmaktan daha tatlı bulmuş.", None, "◐ M3:C10,D12 (Zibaldone; Cosimo'ya atfedilmez; çeviri bize ait)"),
              ("Palla Strozzi, ısmarladığı “Üç Kral’ın Tapınışı” tablosunda soyadını sanki imzalamış: maiyetin arasında bir şahinci var; strozziere, şahinci demek.", None, "◐ M3b:b83,bd21 (Gentile da Fabriano 1423; mizah b; \"sanki\": niyet iddia edilmez)"),
              ("Strozzi'ler 1489'da Medici sarayını aşacak bir saraya başladı; temel gününü bir astrolog seçti.", None, "◐ M3b:b87,b88"),
              ("Medici'nin rakibi Pazzi ailesi de Brunelleschi'ye atfedilen bir şapeli ısmarlamıştı; o adın 1478'de nasıl anılacağını biliyoruz, onlar bilmiyordu.", None, "◐ M3b:b85,b86 (\"atfedilir\"; yan yana koyuş YORUM)"),
          ], [
              ("Vasari'ye göre Cosimo, Fra Filippo Lippi'yi çalışsın diye evinde bir odaya kilitlemiş.", None, "ANEKDOT ◐ M3b:bd22,b106"),
              ("Lippi çarşafları makasla kesip ip yapmış, pencereden inmiş; Cosimo da pişman olup ona serbestlik tanımış.", None, "ANEKDOT ◐ M3b:bd22,b106 (\"anlatılır\"; mizah a: patron kibri)"),
          ], [
              ("Yıllar sonra genç Lorenzo ailenin defterini açtı: 1434'ten 1471'e sadaka, yapı ve vergi, altı yüz altmış üç bin florinden fazla.", None, "◐ M1b:bD3,b59,U1 (663.755; hane toplamı, \"sanat\" DEĞİL)"),
              ("Ricordi'ye göre toplam Lorenzo'ya akıl almaz göründü; üstelik başka harcamalar bunun dışındaydı.", None, "◐ M1b:bD3 (çeviri bize ait; \"inanılmaz\" yasak kalıp)"),
              ("Bu para kefaret miydi, yatırım mı?", None, "—"),
              ("Kaynaklarda üç iz var: vicdan, onur, ölümden sonra için bir yer.", None, "YORUM M3:§5.5,C1,C10,C15 (Eski Sakristi: Giovanni eşiyle gömülü)"),
          ], [
              ("Duvarlar dikilmişti.", None, "—"),
              ("Sıra, duvarların içine konacak şeye geldi: kitaplara.", None, "YORUM (c5 kapısı)"),
          ]])
