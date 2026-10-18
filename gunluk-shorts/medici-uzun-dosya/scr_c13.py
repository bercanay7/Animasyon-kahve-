"""c13 — İki Kraliçe (1519/1533–1642). Brif: brif/c13_brif.md. İKİ YÜZ: mizah YALNIZ V5 (mit endüstrisi), V7 (çeyiz–borç mahsubu; hedef sistem), V9 (imge siyaseti; hedef kibir).
MİZAH KAPALI: V1, V4 (1572), V6, V8, V10 (Köln). Kurbana mizah YOK (Catherine'in bedeni/çocuksuzluğu/Diane, Marie'nin yoksulluğu, 1572 ölüleri). Cinsel/kaba gönderme YOK (kuşatma anekdotu çıplaklık/teslim ayrıntısı, düğün gecesi, 'kızı çırılçıplak aldım' girmez).
Yıldız an: 3 Temmuz 1642, Köln (V10) — oda betimi/son söz YOK. İkinci ağırlık 22–24 Ağustos 1572 (V4: saat/çan/şafak YOK; 'hepsini öldürün' YOK). Marie'nin doğum yılı söylenmez (1573 ↔ 1575). 'Rubens'in doğduğu evde' MİT — söylenmez.
Kapı: K3 uyarlaması (zıtlık) → c14. Söylenen sayı ≤6: 14 · 10 · 3.000 · 5 · 600.000 · 24."""
PRON = [
    (r"\bCatherine\b", "Katrin"), (r"\bMarie\b", "Mari"), (r"\bHenri Estienne\b", "Anri Estyen"), (r"\bHenri\b", "Anri"),
    (r"\bDiane de Poitiers\b", "Dyan dö Puatye"), (r"\bColigny\b", "Kolinyi"), (r"\bGuise\b", "Giz"),
    (r"\bBlois\b", "Blua"), (r"\bMarsilya\b", "Marsilya"), (r"\bConcini\b", "Konçini"), (r"\bRichelieu\b", "Rişölyö"),
    (r"\bLouvre\b", "Luvr"), (r"\bRubens\b", "Rubens"), (r"\bSiegen\b", "Zigen"), (r"\bKöln\b", "Köln"),
    (r"\bBalet comique\b", "Bale komik"), (r"\bKirke\b", "Kirke"), (r"\bLouis\b", "Lui"), (r"\bécu\b", "ekü"),
    (r"\bHuguenot\b", "Yugno"),
]

CH = dict(id="c13", n="XIII", title="İki Kraliçe", years="1519 – 1642", mood="duo", front="",
          paras=[[
              ("Onun adı Catherine'di. 1519'da Floransa'da doğdu; annesi ve babası, doğumundan sonraki haftalarda öldü.", None, "◐ Britannica + Treccani EI + PUF; M4c:B01–B03 (gün kartı ekranda: 13 Nisan → 28 Nisan → 4 Mayıs)"),
              ("Çocukken, doğduğu şehir kuşatma altındayken, bazı seslerin onu surlara çıkarıp düşmanın önüne koymayı önerdiği anlatılır.", None, "ANEKDOT ◐; ilk yazan bulunamadı; çıplaklık/teslim ayrıntısı bilinçle söylenmez; kim önerdi söylenmez M4c:B05,C16"),
              ("1533'te Medici papası VII. Clemens onu Fransa Kralı'nın oğlu Henri ile evlendirdi.", None, "◐ Britannica M4c:B06,D83 (\"amcası\" DENMEZ — uzak akraba; 28 Ekim ↔ 27 ekranda)"),
              ("Marsilya, 14 yaşında bir gelin.", None, "◐ 14 = hesap bize ait (çeyiz \"yüz bin altın\" ekran kartı)"),
          ], [
              ("Evlilikten sonraki on yıl çocuk olmadı; Henri'nin gönlü Diane de Poitiers'deydi.", None, "◐ Britannica \"10 anxious years\" + Diane M4c:B07,D79 (tıbbi/cinsel ayrıntı GİRMEZ)"),
              ("Sonra çocukları oldu, hem de çok.", None, "◐ Britannica \"ten children\" (sayı kartta) M4c:B07"),
          ], [
              ("10 Temmuz 1559'da Henri, bir turnuvada başına isabet eden mızrak yüzünden öldü.", None, "◐ Britannica + Guizot + Thompson M4c:B08,D80 (29 ↔ 30 Haziran söylenmez; çarpışma gösterilmez)"),
              ("Catherine'in bundan sonra uzun yıllar siyah giydiği yazılır.", None, "○ bir çalışma M4c:C20,D80 (opsiyonel; \"yazılır\")"),
              ("1560 sonunda küçük IX. Charles tahta çıkınca devleti fiilen Catherine yönetti.", None, "◐ Guizot + Thompson M4c:B09,D73 (\"naip\" unvanı verilmedi → \"fiilen\")"),
              ("Din savaşını uzlaşmayla durdurmak istedi; Ocak 1562 fermanı Fransız Protestanlarına kent surlarının dışında, silahsız ibadet izni verdi.", None, "◐ Britannica + dokumen.pub M4c:B10,D74 (adil portre; iki yorum söylenmez)"),
          ], [
              ("22 Ağustos 1572'de Amiral Coligny'ye suikast girişimi oldu; ertesi gün konsey, Protestan liderlerin öldürülmesine karar verdi.", None, "◐ Britannica; azmettirici ○ M4c:B11; M4b:b32–b33 (saat/çan/şafak YOK)"),
              ("24 Ağustos'ta Paris'te başlayan katliam başka şehirlere yayıldı; yalnız Paris'te üç bin kadar ölü olduğu tahmin edilir.", None, "◐ Britannica (tahmin); ülke rakamı H M4c:B11,D75"),
              ("Britannica'ya göre Catherine, liderlerin öldürülmesini onaylamıştı; ardından gelen katliamı büyük olasılıkla onaylamamıştı.", None, "◐ Britannica M4b:bM7; M4c:D75 (\"Britannica'ya göre\")"),
              ("Tarihçiler tam bu noktada ayrılır.", None, "◐ Mariéjol \"tuzak\", Jouanna \"konsey\", Knecht M4c:§5.14 (tek tarihçi kesin tutum olarak verilmez)"),
          ], [
              ("Katliamdan sonra Catherine'in çevresinde bir efsane büyüdü: kötü İtalyan kraliçe.", None, "◐ Britannica M4c:C21,B12 (geçiş cümlesi: düz; mizah 1572'den hemen sonra başlamaz)"),
              ("İlk saldırılardan biri 1573'te Protestan bir broşürdeki şiirdi; 1575'te adsız bir kitapçık çıktı, sonradan Henri Estienne'e atfedildi.", None, "◐ McIlvenna + IA + EB 1911 M4c:B12,D76 (\"atfedildi\")"),
              ("Sonra faturalar kesilmeye başladı: çatalı o getirmiş, dondurmayı o getirmiş, topuklu ayakkabıyı da, parfümü de… ve tabii zehri.", None, "◐ M4b:bM9 + M4c:D77 (hepsi \"anlatılır\" düzeyi; mizah a+c)"),
              ("Oysa çatal Catherine'den çok önce İtalya'daydı; bir anlatı onu Venedik'e gelen bir Bizans prensesine bağlar.", None, "◐ \"Catherine'den önce İtalya'da\" (California Academy + NatGeo + The Florentine); ANEKDOT ○ prenses M4c:D77,§5.8 (1071 söylenmez)"),
              ("Dondurma hikâyesinin izi ise 19. yüzyıla çıkıyor.", None, "◐ Liddell–Weir + Colonial Williamsburg + Cooks Info M4b:bM9"),
              ("Bir ülke inceliğini de günahını da tek bir yabancıya yazmış; pratik bir düzen.", None, "YORUM (mizah b; hedef mit düzeni, kadın değil; opsiyonel)"),
              ("Gerçek olan bir gösteriydi: 15 Ekim 1581'de sahnelenen Balet comique, Kirke efsanesini anlatan, beş saati aşan, basılı metni olan bir saray balesiydi.", None, "◐ M4b:b38 (Britannica, Wikipedia, EBSCO); \"ilk\" denmez; mekân çelişir M4c:B13,§5.13"),
          ], [
              ("Catherine, 5 Ocak 1589'da Blois'da öldü; Guise Dükü aynı şatoda, bir önceki yılın son günlerinde öldürülmüştü.", None, "◐ Britannica (Catherine + Blois) M4c:B14–B15,D78 (plörezi söylenmez)"),
          ], [
              ("Bir başka Medici kızı, Marie, Fransa'ya gelin gitti.", None, "◐ Britannica M4c:B16–B18 (doğum yılı SÖYLENMEZ: 1573 ↔ 1575)"),
              ("Evlilik 1600'de Floransa'da vekâleten kıyıldı; kral orada değildi.", None, "◐ M4b:b40 (5 Ekim; vekilin kimliği söylenmez) M4c:B18"),
              ("Çeyiz 600.000 écu'ydu ve Fransa'nın Toskana Büyük Dükü'ne olan borcundan düşüldüğü yazılır: gelinin parası, damadın borcuna mahsup edildi.", None, "◐ herodote.net + sept.info + Britannica + Gutenberg M4b:b41; M4c:B17,D72 (borç miktarı ○ söylenmez; mizah a)"),
              ("Borcu ödemenin en kibar yolu, borç verenin kızıyla evlenmek.", None, "YORUM (mizah b; hedef kraliyet maliyesi) M4c:D72"),
              ("Marie, 3 Kasım 1600'de Marsilya'ya indi.", None, "◐ Louvre başlığı M4c:C22 (aynı liman — V1 ile eşleşir)"),
          ], [
              ("13 Mayıs 1610'da taç giydi; ertesi gün Henri IV öldürüldü, Marie naip oldu.", None, "◐ Gutenberg Pardoe + Louvre başlıkları M4c:B19–B20"),
              ("Favorisi Concini 1617'de öldürülünce Blois Şatosu'na gönderildi. Ne düşündüğünü bilmiyoruz; ama ne yaptığını biliyoruz: 1619'da bir gece kaçtı.", None, "◐ yıllar; Louvre başlığı \"nuit du 21 au 22 février 1619\" M4c:B21–B23 (iç-dünya kalıbı, bölümde tek; ip/merdiven H söylenmez)"),
              ("1630'daki Aldatılanlar Günü'nde oğlu Kral Louis, Richelieu'yu seçti, annesini değil.", None, "◐ Versailles + Britannica M4c:B26,D81 (10–11 Kasım ekranda)"),
              ("Marie 1631'de Fransa'dan çıktı ve bir daha dönmedi.", None, "◐ Versailles + Osborne M4c:B27"),
          ], [
              ("1622'de Marie, Rubens'e yaşamını anlatan yirmi dört dev tablo ısmarladı: hayatını yeniden yazdırmanın en pahalı yolu.", None, "◐ Louvre (1622, 24 tablo) M4c:B25,D70; ikinci yarı YORUM (mizah: kibir; Marie'nin yoksulluğuna değil)"),
              ("Louvre'a göre bu seri Marie'ye kendi anlatısını sunma fırsatı verdi; ressam kralı gücendirmemeye de dikkat etmek zorundaydı.", None, "◐ Louvre sayfası (çeviri bize ait) M4c:C23 (\"Louvre'a göre\")"),
              ("Kader tanrıçaları Marie'nin yaşam ipliğini eğirir; Blois'dan gece kaçış bile kahramanca bir sahne olarak yer alır.", None, "◐ Louvre başlıkları (Les Parques filant le destin…, La Reine s'enfuit du château de Blois…) M4c:C22"),
          ], [
              ("Marie, 3 Temmuz 1642'de Köln'de, yoksul öldü.", None, "◐ Britannica + Osborne + Pardoe M4c:B28 (oda betimi, son söz, tanık YOK)"),
              ("Ev, Rubens ailesinin yıllarca oturduğu evdi; sonradan Rubens'in orada doğduğu söylendi, oysa doğduğu yer Siegen'di.", None, "◐ Britannica (Siegen) + M4b:b48 + Köln levhaları M4c:D69,§5.16 (efsane \"söylendi\")"),
              ("Tablolar ise Paris'te kaldı; bugün Louvre'da, ayrı bir galerideler.", None, "◐ M4b:b44 (Luxembourg 1625, Louvre 1816, Galerie Médicis 1993) M4c:B29 (restorasyon güncelliği söylenmez)"),
              ("İki kraliçe Fransa'da imgesini savunurken, ailenin Floransa'daki kolu adını gökyüzüne yazdırıyordu.", None, "YORUM + ◐ c14 (K3 uyarlaması; Galileo 1610 — \"Floransa'da\" yanlış; Medici adı = uydular)"),
          ]])
