"""c2 — Defterin Sihri (1397–1429). Brif: brif/c2_brif.md. En mizahlı bölüm: faiz yasağı ↔ kambiyo, "eski papa", çifte kayıt miti. Giovanni'nin ölümü: mizah KAPALI."""
PRON = [
    (r"\bBaldassarre Cossa\b", "Baldassarre Kossa"), (r"\bCossa\b", "Kossa"),
    (r"\bXXIII\. Johannes\b", "Yirmi Üçüncü Yohannes"), (r"\bV\. Martinus\b", "Beşinci Martinus"),
    (r"\bKonstanz\b", "Konstanz"), (r"\bJohannes\b", "Yohannes"),
    (r"\bPalla Strozzi\b", "Palla Strottsi"), (r"\bStrozzi\b", "Strottsi"),
    (r"\bCavalcanti\b", "Kavalkanti"), (r"\bMachiavelli\b", "Makyavelli"),
    (r"\bPacioli\b", "Paçoli"), (r"\bcatasto\b", "katasto"),
    (r"\bdepositario\b", "depozitaryo"), (r"\b[Dd]e Roover\b", "de Rover"),
    (r"\bBrugge\b", "Brüge"),
]

CH = dict(id="c2", n="II", title="Defterin Sihri", years="1397 – 1429", mood="dry", front="",
          paras=[[
              ("Çözüm, kambiyodaydı.", None, "YORUM (c1 kapısına yanıt)"),
              ("Kilise her türlü faizi tefecilik sayıp yasaklamıştı; bankacılar da bir yol buldular.", None, "● teyit_P1 (birincil metin okundu) · ◐ M1:§5B,D35"),
              ("Klasik bir örnekte işleyiş şöyleydi: Brugge'de bir tüccara parayı peşin verirsin, karşılığında Barselona'ya çekilmiş bir poliçe alırsın.", None, "◐ model M1:§5A (Medici'ye özgü belge yok; tutar yok)"),
              ("Vadesi gelince poliçe tahsil edilir, ikinci bir poliçeyle de para geri döner; kazanç, kur farkıdır.", None, "◐ model M1:§5A"),
              ("Ortada borç yok, faiz yok; yalnızca kur farkı var.", None, "● teyit_P1 (birincil metin okundu) · ◐ gerekçe M1:§5B"),
              ("Orta Çağ'ın en yaratıcı departmanı muhtemelen buydu: vicdan komitesi.", None, "YORUM (mizah a; USLUP §5-B)"),
              ("Tim Parks'ın aktardığına göre mevduata gelince, faiz sözleşmeye yazılmaz; banker bunu kendi takdiriyle, bir lütuf olarak öderdi.", None, "○ M1:§5B (Tim Parks, Medici Money 2005 özeti; \"aktardığına göre\") — kurul KA1-K1/KA2-E1: ad düzeltildi"),
              ("Faiz değil, hediye.", None, "● teyit_P1 (birincil metin okundu) · ○ M1:§5B (mizah a)"),
          ], [
              ("Üstelik bu işin müşterilerinden biri, faizi yasaklayan Kilise'nin ta kendisiydi.", None, "● teyit_P1 (birincil metin okundu) · ○ M1:D19 (de Roover)"),
              ("De Roover'a göre Roma şubesi zamanla sermayesiz çalışır hale geldi; kasayı Kilise'nin yatırdığı para dolduruyordu.", None, "● de Roover 1963: Roma şubesinin sermayesi 1402'de 4.000, 1420'de 6.000 fl; 'the capital had already been withdrawn in 1426', 1429 sözleşmesinde 'no corpo'; papalık mevduatı ana kaynak — kurul tur 2 KA2-Y1 (eski cümle Averardo'nun ayrı bankasına ait cümleyi Giovanni'ye bağlıyordu)"),
              ("25 Mart 1402'de Venedik şubesi açıldı; Floransa'da o gün yılbaşıydı.", None, "● teyit_P1 (birincil metin okundu) · ◐ M1:#28,D18 (kasıt söylenmez)"),
          ], [
              ("Çifte kaydı Medici'ler icat etti derler.", None, "● teyit_P1 (birincil metin okundu) · MİT M1:mit1"),
              ("Etmediler: Cenova'nın 1340 tarihli hesapları bunun bilinen en eski tam örneklerinden biridir.", None, "◐ M1:#71,#76"),
              ("Medici'nin farkı defterde değil, yapıdaydı: her şubenin kendi ortaklığı, kendi defteri vardı.", None, "● teyit_P1 (birincil metin okundu) · ◐ M1:§5C"),
          ], [
              ("Giovanni, Baldassarre Cossa adlı bir kilise adamına borç verdi; adam sonra XXIII. Johannes adıyla papa oldu.", None, "◐ M1b:b28,bD13 (yalnız \"borç\")"),
              ("1415'te Konstanz Konsili onu papalıktan indirdi.", None, "● teyit_P1 (birincil metin okundu) · ◐ M1b:U4,b29"),
              ("İndirilen Cossa'yı Giovanni'nin kefaletle ya da fidyeyle kurtardığı yazılır; kaynaklar bu konuda ayrışıyor.", None, "◐/○ M1:D16,M1b:b30,bD14,U6 (tutar söylenmez)"),
              ("Cossa Floransa'da öldü, Vaftizhane'ye gömüldü; mezarına yazılan söz şuydu: “eski papa”.", None, "● teyit_P1 (birincil metin okundu) · ◐ M1:#33,#36,D15"),
              ("Papa V. Martinus itiraz etti. Yazıt kaldı.", None, "◐ M1:#36,D15 (mizah a: kurum/kibir)"),
              ("De Roover'ın andığı belgelere göre Martinus, Cossa'nın bir borca karşılık bıraktığı mitrayı geri almak için Giovanni'yi aforozla tehdit etmek zorunda kalmıştı.", None, "● de Roover 1963, n. 45 (Camerani Marri 1951, s. 32, belge 48–49): 'Martin V had to threaten Giovanni di Bicci with excommunication… restore the pledge'; DBI: Giovanni Kilise rehni iki mitrayı saklıyordu — kurul: atıf Treccani→de Roover, 'rivayet' değil belgeli"),
              ("Papalığın resmî kasa memurluğu da 1422'den sonra yirmi iki yıl kesintisiz, ardından on sekiz yıl aralıklarla Medici'de kaldı.", None, "● DBI 'Medici, Giovanni di Bicci': 'per 22 anni consecutivi e per altri 18 a intermittenza' (1422 Bartolomeo Bardi depositario) — kurul teyit_P1 ✗→düzeltildi"),
          ], [
              ("1427'de Floransa hanelerin servetini tek tek yazdırdı; bu sayıma catasto denir.", None, "● teyit_P1 (birincil metin okundu) · ◐ M1:#39"),
              ("Bir hesaba göre yüz otuz yedi hane, kayıtlı servetin yaklaşık yüzde otuzunu tutuyordu; en zengini Palla Strozzi'ydi.", None, "● Online Catasto of 1427 (Herlihy–Klapisch-Zuber–Litchfield–Molho, Brown Üniv.): 137 hane = kayıtlı servetin %29,8'i; en zengini Palla Strozzi — kurul tur 2 KA1 · önceki: ◐ Strozzi / ○ %29,8 M1:#39,§4B (\"bir hesaba göre\")"),
              ("Giovanni bu sayımın yürürlüğe girmesini destekledi.", None, "● teyit_P1 (birincil metin okundu) · ◐ M1:#38 (yıl 1426/27 çelişkili)"),
          ], [
              ("Giovanni 1420'de bankanın yönetimini oğullarına bırakmıştı; 1397'den o yıla kadar defterler yüz elli bini aşkın florin kâr gösterir.", None, "● teyit_P1 (birincil metin okundu) · ◐ M1b:U5,b33; ◐ toplam M1:#35 (\"gösterir\")"),
              ("20 Şubat 1429'da öldü; Floransa takvimine göre hâlâ 1428'di.", None, "● teyit_P1 (birincil metin okundu) · ◐ M1:#40; M5:P1"),
              ("İleride Muhteşem diye anılacak torununun oğlu Lorenzo'nun kaydına göre, bıraktığı servet yüz seksen bin florin dolayındaydı.", None, "● teyit_P1 (birincil metin okundu) · ○ DBI/M5:D32 (\"Lorenzo'nun kaydına göre\"; DBI 'bisnipote' = torunun oğlu — kurul KA1-V6/KA2-Ö7)"),
              ("Son sözlerini ise iki kalemden, iki ayrı biçimde okuyoruz.", None, "● teyit_P1 (birincil metin okundu) · ANEKDOT M1:D11–D14"),
              ("Machiavelli, bir asra yakın sonra, onun ağzından oğullarına bir konuşma yazar: huzurla gidiyordur ve kıskançlık, insana verilenden değil, istediğinden doğar.", None, "ANEKDOT ◐ M1:D11,M5:K01 (\"Machiavelli'ye göre\"; kurgu payı)"),
              ("Cavalcanti ise 1430'larda, hapisteyken, olaya daha yakın bir kalemle başka bir şey yazar: kimse dünyevi tasaları sonsuz huzurla değiş tokuş ettiği için kederlenmemeli.", None, "● Cavalcanti, Istorie fiorentine IV (Polidori 1838); DBI 'Cavalcanti, Giovanni': Stinche'de ≈10 yıl, 'In prigione egli attese alla stesura delle Istorie fiorentine' — kurul tur 2 KA2-Y2"),
              ("Hangisi gerçekten söylendi, bilmiyoruz.", None, "YORUM"),
              ("Machiavelli onu, yoksulun ihtiyacını kimse istemeden de sık sık gideren biri olarak çizer.", None, "● teyit_P1 (birincil metin okundu) · ANEKDOT ◐ M1:D14"),
              ("Ama o kalem, Medici'nin siparişiyle çalışıyordu.", None, "◐ M1:D07,D11 (kaynak eleştirisi)"),
          ], [
              ("Giovanni öldüğünde oğlu Cosimo kırk yaşına yaklaşıyordu.", None, "● teyit_P1 (birincil metin okundu) · ◐ M5:P2 (1389 doğumlu)"),
              ("Birkaç yıl sonra aynı Cosimo, şehrin en yüksek kulesinde bir hücreye kapatılacaktı.", None, "◐ M2:K06 (Eylül 1433)"),
          ]])
