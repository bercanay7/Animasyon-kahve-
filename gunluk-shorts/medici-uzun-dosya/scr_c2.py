"""c2 — Defterin Sihri (1397–1429). Brif: brif/c2_brif.md. En mizahlı bölüm: faiz yasağı ↔ kambiyo, "eski papa", çifte kayıt miti. Giovanni'nin ölümü: mizah KAPALI."""
PRON = [
    (r"\bBaldassarre Cossa\b", "Baldassarre Kossa"), (r"\bCossa\b", "Kossa"),
    (r"\bXXIII\. Johannes\b", "Yirmi Üçüncü Yohannes"), (r"\bV\. Martinus\b", "Beşinci Martinus"),
    (r"\bKonstanz\b", "Konstanz"), (r"\bJohannes\b", "Yohannes"),
    (r"\bPalla Strozzi\b", "Palla Strottsi"), (r"\bStrozzi\b", "Strottsi"),
    (r"\bCavalcanti\b", "Kavalkanti"), (r"\bMachiavelli\b", "Makyavelli"),
    (r"\bPacioli\b", "Paçoli"), (r"\bcatasto\b", "katasto"),
    (r"\bdepositario\b", "depozitaryo"), (r"\b[Dd]e Roover\b", "de Rover"), (r"\bTracy Parks\b", "Treysi Parks"),
    (r"\bBrugge\b", "Brüge"),
]

CH = dict(id="c2", n="II", title="Defterin Sihri", years="1397 – 1429", mood="dry", front="",
          paras=[[
              ("Çözüm, kambiyodaydı.", None, "YORUM (c1 kapısına yanıt)"),
              ("Kilise her türlü faizi tefecilik sayıp yasaklamıştı; bankacılar da bir yol buldular.", None, "◐ M1:§5B,D35"),
              ("Klasik bir örnekte işleyiş şöyleydi: Brugge'de bir tüccara parayı peşin verirsin, karşılığında Barselona'ya çekilmiş bir poliçe alırsın.", None, "◐ model M1:§5A (Medici'ye özgü belge yok; tutar yok)"),
              ("Vadesi gelince poliçe tahsil edilir, ikinci bir poliçeyle de para geri döner; kazanç, kur farkıdır.", None, "◐ model M1:§5A"),
              ("Ortada borç yok, faiz yok; yalnızca kur farkı var.", None, "◐ gerekçe M1:§5B"),
              ("Orta Çağ'ın en yaratıcı departmanı muhtemelen buydu: vicdan komitesi.", None, "YORUM (mizah a; USLUP §5-B)"),
              ("Tracy Parks'ın aktardığına göre mevduata gelince, faiz sözleşmeye yazılmaz; banker bunu kendi takdiriyle, bir lütuf olarak öderdi.", None, "○ M1:§5B (Parks özeti; \"aktardığına göre\")"),
              ("Faiz değil, hediye.", None, "○ M1:§5B (mizah a)"),
          ], [
              ("Üstelik bu işin müşterilerinden biri, faizi yasaklayan Kilise'nin ta kendisiydi.", None, "○ M1:D19 (de Roover)"),
              ("De Roover'a göre Roma şubesine ayrı sermaye verilmedi; kasayı Kilise'nin yatırdığı para doldurdu.", None, "○ M1:#27,D19 (\"de Roover'a göre\")"),
              ("25 Mart 1402'de Venedik şubesi açıldı; Floransa'da o gün yılbaşıydı.", None, "◐ M1:#28,D18 (kasıt söylenmez)"),
          ], [
              ("Çifte kaydı Medici'ler icat etti derler.", None, "MİT M1:mit1"),
              ("Etmediler: Cenova'nın 1340 tarihli hesapları bunun bilinen en eski tam örneklerinden biridir.", None, "◐ M1:#71,#76"),
              ("Medici'nin farkı defterde değil, yapıdaydı: her şubenin kendi ortaklığı, kendi defteri vardı.", None, "◐ M1:§5C"),
          ], [
              ("Giovanni, Baldassarre Cossa adlı bir kilise adamına borç verdi; adam sonra XXIII. Johannes adıyla papa oldu.", None, "◐ M1b:b28,bD13 (yalnız \"borç\")"),
              ("1415'te Konstanz Konsili onu papalıktan indirdi.", None, "◐ M1b:U4,b29"),
              ("İndirilen Cossa'yı Giovanni'nin kefaletle ya da fidyeyle kurtardığı yazılır; kaynaklar bu konuda ayrışıyor.", None, "◐/○ M1:D16,M1b:b30,bD14,U6 (tutar söylenmez)"),
              ("Cossa Floransa'da öldü, Vaftizhane'ye gömüldü; mezarına yazılan söz şuydu: “eski papa”.", None, "◐ M1:#33,#36,D15"),
              ("Papa V. Martinus itiraz etti. Yazıt kaldı.", None, "◐ M1:#36,D15 (mizah a: kurum/kibir)"),
              ("Treccani'nin Giovanni maddesinde bir de şu rivayet geçer: Martinus, Cossa'nın bir borca karşılık bıraktığı mitrayı geri almak için Giovanni'yi aforozla tehdit etmiş.", None, "ANEKDOT ○ M1b:b34,bD1 (\"rivayet\"; DBI özeti)"),
              ("Papalığın resmî kasa memurluğu da 1420'lerin başından itibaren, kesintilerle, yirmi iki yıl kadar Medici'de kaldı.", None, "◐ M1b:b32,U2"),
          ], [
              ("1427'de Floransa hanelerin servetini tek tek yazdırdı; bu sayıma catasto denir.", None, "◐ M1:#39"),
              ("Bir hesaba göre yüz otuz yedi hane, kayıtlı servetin yaklaşık yüzde otuzunu tutuyordu; en zengini Palla Strozzi'ydi.", None, "◐ Strozzi / ○ %29,8 M1:#39,§4B (\"bir hesaba göre\")"),
              ("Giovanni bu sayımın yürürlüğe girmesini destekledi.", None, "◐ M1:#38 (yıl 1426/27 çelişkili)"),
          ], [
              ("Giovanni 1420'de bankanın yönetimini oğullarına bırakmıştı; 1397'den o yıla kadar defterler yüz elli bini aşkın florin kâr gösterir.", None, "◐ M1b:U5,b33; ◐ toplam M1:#35 (\"gösterir\")"),
              ("20 Şubat 1429'da öldü; Floransa takvimine göre hâlâ 1428'di.", None, "◐ M1:#40; M5:P1"),
              ("Büyük torunu Lorenzo'nun kaydına göre, bıraktığı servet yüz seksen bin florin dolayındaydı.", None, "○ DBI/M5:D32 (\"Lorenzo'nun kaydına göre\")"),
              ("Son sözlerini ise iki kalemden, iki ayrı biçimde okuyoruz.", None, "ANEKDOT M1:D11–D14"),
              ("Machiavelli, bir asra yakın sonra, ona oğullarına bir konuşma yaptırır: huzurla gidiyordur ve kıskançlık, insana verilenden değil, istediğinden doğar.", None, "ANEKDOT ◐ M1:D11,M5:K01 (\"Machiavelli'ye göre\"; kurgu payı)"),
              ("Cavalcanti ise 1440'larda, olaya daha yakın bir kalemle, başka bir şey yazar: kimse dünyevi tasaları sonsuz huzurla değiş tokuş ettiği için kederlenmemeli.", None, "ANEKDOT ○ M1:D12 (İngilizce çeviriden dolaylı; birebir söz yok)"),
              ("Hangisi gerçekten söylendi, bilmiyoruz.", None, "YORUM"),
              ("Machiavelli onu, yoksulun ihtiyacını kimse istemeden de sık sık gideren biri olarak çizer.", None, "ANEKDOT ◐ M1:D14"),
              ("Ama o kalem, Medici'nin siparişiyle çalışıyordu.", None, "◐ M1:D07,D11 (kaynak eleştirisi)"),
          ], [
              ("Giovanni öldüğünde oğlu Cosimo kırk yaşına yaklaşıyordu.", None, "◐ M5:P2 (1389 doğumlu)"),
              ("Birkaç yıl sonra aynı Cosimo, şehrin en yüksek kulesinde bir hücreye kapatılacaktı.", None, "◐ M2:K06 (Eylül 1433)"),
          ]])
