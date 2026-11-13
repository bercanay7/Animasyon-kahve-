# SA2 · Tur 2 · Sanat ve üslup · Mercek: DÖNEM / GELENEK UZMANI (dönem doğruluğu, katman ve okunurluk)
Medici Parça 1 v2 (`out_p1/medici_P1.mp4`, 598,5 sn, 14.365 kare) · 5 Kasım 2026

## 1. Karar
**RED, 8,5/10** (tur 1: 5,0; eşik ≥9). Bu turda engelleyici bulgu yok.

- **Kapananlar:** Tur 1'deki dört engelleyicinin dördü de kapandı. Kapanış tek tek yamayla değil, sistemle oldu: `donem.py` ile `qa_donem` kuruldu. Katman kapalıyken 95 ihlal çıkıyor, açıkken 0. qa_flow v2 satırı: "Dönem (ENG-A) GEÇTİ · 318 kare · İHLAL 0". Sekiz önemli maddenin altısı kapandı.
- **Puanı 9'un altında tutanlar:** dört yeni "önemli" bulgu var, hepsinin düzeltmesi ucuz:
  - **Y1:** figür belirirken başı gövdesinden önce geliyor.
  - **Y2:** 1338 meydanında Loggia dei Lanzi var; yapı 1376–82'de inşa edildi.
  - **Y3:** Dante ve Villani çekimlerinde HUD 1252'de kalıyor.
  - **Y4:** dönem katmanı, 1520 tarihli bir Medici mührünü 1429 armasıyla çiziyor. Bu, katmanın kendisinin getirdiği bir gerileme.
- Ö4 (1252 kıyafeti) hâlâ açık.
- **Yol:** Y1–Y4 ile kapaktaki arma (§5) düzelirse puan 9,5 olur. Ö4 açık kalırsa 9,0. Gerileme kontrolünü tek üye olarak ben yaparım. Toplam yeniden render 6 çekim, yaklaşık 40 saniyelik görüntü.

**Sınır:** Videoyu oynatamadım, sesi dinleyemedim. v1 videosu silindiği için tur 1 kıyasını kendi tur 1 notlarımla ve kodla yaptım.

**Dayanaklar:**
- **Kareler:** v2'nin 106 çekiminin her birinin ortasından birer kare (960 px) ve 60'tan fazla tam çözünürlüklü kare.
- **Yoğun şeritler:**
  - 130,6–132,1 sn ve 143,0–146,0 sn, saniyede 8 kare;
  - 486,4–493,6 sn, saniyede 3 kare;
  - 187,1–201,5 sn, saniyede 2 kare.
- **Belge ve ölçüm:** `qa_donem.json`, `qa_flow_v2.txt`, `notlar_donem.md`, `teyit_P1.md`, `KURUL.md`, PK1 tur 2 (Y6).
- **Kod:**
  - `donem.py`;
  - `cilt_anim.draw_fig/blit`, `cilt_oda._blit_cf`;
  - `cilt_sehir._draw_main/loggia`, `cilt_city` (çan kulesi ve kule çizimi);
  - `kapak_medici.palle_erken`.
- **Kapaklar:** `yayin/studio_paketi_P1/kapak_P1_K1.jpg`, `_K2.jpg`.

## 2. Tur 1 maddelerinin durumu
Zaman damgaları v2'ye göredir. Koordinatlar 1920×1080 çerçevededir, ±25 px.

| Madde | Durum | Kanıt (v2) |
|---|---|---|
| **B1** Kubbe ve tam boy çan kulesi 1338/1348/1378'de | **KAPANDI** | **1338:** 138,0 ve 141,1 sn'de meydanda kubbe yok. qa_donem değerleri: nef 0,50, kubbe 0, çan kulesi 0,166.<br>**1348:** 184,5 sn'deki siluette kubbe yok.<br>**1378:** 237,6 ve 239,6 sn'de nef kubbesiz, çan kulesi tam boy; 1359 sonrası için bu doğru. Kızıl yıkamalı 1378 silueti tümden kaldırıldı. |
| **B2** 1378 alay ve kalabalıkta Medici sancağı | **KAPANDI** | **215,0 / 217,5 (alay):** Komün zambağı, Popolo haçı, düz yeşil ve sarı sancak; atlı yok.<br>**237,6 (22 Temmuz):** yalnız Popolo haçları.<br>**269,7 (milis):** zambak ve düz sancak.<br>qa_donem kaydı: istenen "medici" → çizilen "plain".<br>Salvestro çekimi iç mekâna alındı (224,0) ve kura torbasıyla (*borsa*) kuruldu; isabetli bir dönem ayrıntısı. |
| **B3** 1465 öncesi zambaklı arma | **KAPANDI** | **155,2 (1338):** çarpı işaretli, 8 toplu arma.<br>**281,8 (1378 kademe):** aynı biçim.<br>**341,4 (bölüm kartı II):** altın alanda kenar boyunca 8 kırmızı top, mavi top yok. qa_donem: `red8`.<br>Kapakla tutarsızlık için §5'e bakın. |
| **B4** 1429'da "PATER PATRIAE" | **KAPANDI** | **582,6 / 583,8:** "COSMVS · MEDICES ·" yazıyor; TEMSİLÎ damgası otomatik basılıyor. |
| **Ö1** Yıl rozeti içerikle çelişiyor | **KAPANDI** (c2) | **437,5 → 439,8:** HUD 1402'den 1410'a geçiyor; levha "COSSA = XXIII. JOHANNES · PİSA PAPASI · BUGÜN KARŞI PAPA SAYILIR".<br>**442,8:** HUD 1415, Konstanz.<br>**456,9–474,0:** HUD 1419 (mezar, Martinus).<br>**481,3:** HUD 1422.<br>**420,3:** zaman çizelgesinde HUD gizli.<br>Aynı sınıfın c0 ve c1'deki yeni örnekleri için Y3'e bakın. |
| **Ö2** 1378 isyanı "Gozzoli Magi alayı" kadrosuyla | **KISMEN** (küçüğe indirdim) | **215,0 / 217,5:** Atlılar ve Medici sancakları gitti.<br>Kadroda hâlâ brokar ve baklava desenli zengin giysiler var:<ul><li>x≈410–540: turuncu baklava cüppe;</li><li>x≈900–1080: yeşil brokar ve altın pelerin;</li><li>x≈1260–1460: siyah elbiseli, başörtülü kadın.</li></ul>Atsız ve halk ağırlıklı kadro "saray alayı" okumasını büyük ölçüde kırdı. |
| **Ö3** Boncuklu abaküs ve yeşil kara tahta | **KAPANDI** | **150,5:** Kâğıt levhada Hint-Arap rakamları var ("1 2 3 4 5 6 7 8 9 0 · 347 + 125 = 472"); çizgili sayma bezinde jetonlar duruyor.<br>Not (düzeltme istemez): rakam biçimleri bugünkü yazı tipine ait. |
| **Ö4** 1252'de 15. yy ortası kıyafet | **AÇIK** (önemli) | **109,0 / 112,5 (1252 panoraması):** kısa tunik, renkli çorap, kep ya da mazzocchio (ör. x≈540–660, y≈720–1000).<br>**128,5–137,3 (darphane):** zambak desenli kısa tunik ve tüylü kep (x≈440–700, y≈290–820).<br>Mimari ve arma yıla bağlandı, kıyafet bağlanmadı. |
| **Ö5** Büyük Dukalık sınırı etiketsiz | **KAPANDI** | **69,5:** "SINIR YAKLAŞIKTIR" levhası (x≈95–590, y≈930–995) ve "3. MADDE · ÖZET" kartı. |
| **Ö6** Cosimo'nun yaşı | **KAPANDI** | **583,8:** "39 YAŞINDAYDI" · "1389 DOĞUMLU". |
| **Ö7** Peruzzi'nin uydurma kalkanı | **KAPANDI** | **158,0 / 161,0 / 175,0:** Kalkan kaldırıldı.<br>**163,5:** ağ şemasında "ŞUBE SAYILARI TEMSİLÎ" etiketi. |
| **Ö8** 1429 kubbesi | **KAPANDI** | **585,2:** Yarım kabuk, açık tepe, korkuluk ve vinç var; fener ve top yok (kubbe değeri 0,562). |
| **K1** Uffizi revakı | **KAPANDI** | **80,0 / 85,5:** Sütunlar düz arşitrav taşıyor. |
| **K2** Modern hediye kutusu | **KAPANDI** | **390,4:** Kutu yerine kese. |
| **K3** Orsanmichele "Yunan tapınağı" simgesi | **AÇIK** (küçük) | **320,5:** Hâlâ alınlıklı, dört sütunlu simge (x≈980–1330, y≈130–460). |
| **K4** Anahtar yönü ve tiara | **KAPANDI** | **478,3:** Anahtar halkaları altta, dişleri üstte.<br>**462,0:** Martinus'un tiarası beyaz gövdeli ve altın taçlı.<br>Yeni bir mikro tutarsızlık için Y7'ye bakın. |
| **K5** Kitapların sırtı dışarı dönük | **KISMEN** | Banka odalarında (323–351) kitaplar yatık istiflenmiş.<br>Machiavelli'nin kütüphanesinde (253,2–267,3 ve 575,5–580,0) hâlâ dik duruyor, sırtı dışarıda. 1520'ler için sınırda; küçük. |
| **K6** Baklava kafesli cam | **AÇIK, stil olarak kabul** | 202,6; 224,0; 5,0. P2–P7 için oda ön ayarına alınmalı. |
| **K7** 17. yy şapkalı siluetler | **AÇIK** (küçük) | **231,6:** Yün tarayıcısının silueti tüylü şapka ve uzun ceketli (x≈750–930, y≈575–970).<br>**262,0:** İsyancının silueti geniş kenarlı şapka ve redingotlu (x≈1220–1460, y≈470–940).<br>**189,7–193,7:** Veba odasında geniş kenarlı şapkalı, yürüyen bir siluet.<br>Trecento için kapüşon ya da *cappuccio* olmalı. |
| **K8** 21 lonca arması | **KAPANDI** (etiketle) | **231,6 / 274,9:** "ARMALAR TEMSİLÎ". |
| **K9** Mor süsen | **KAPANDI** | **125,8:** Kırmızı, etamenli Floransa zambağı.<br>**138,0:** Sancaklardaki *giglio* da doğru. |
| **K10** 1438 öncesi portre madalyaları | **KAPANDI** | **530,7 / 582,6:** TEMSİLÎ damgası var.<br>Giovanni artık madalya değil, figür olarak çiziliyor (288,8). |
| **K11** 1737–43 iç mekânları Quattrocento kitiyle | **AÇIK, kimlik kararı olarak kabul** | 5,0 / 23,0. |
| **K12** Cossa'nın mezarı | **KAPANDI** | **456,9 / 464,1:** Kemer, perde, yatan figür (*gisant*); HUD 1419. |
| **K13** Kaynaksız mavi-sarı Ciompi şeritleri | **KAPANDI** | **237,6:** Popolo haçları. qa_donem: stripes → lily. |
| **K14** Kesik harita etiketleri | **AÇIK** (küçük) | **365,4:** "BRUGGE" üst kenarda kesik (x≈990–1140, y≈0–15).<br>**364,0:** "BARSELONA"nın B harfi poliçe simgesinin altında kalıyor; "ARSELONA" okunuyor (x≈880–1150, y≈850–870). |
| **K15** Başlıklar kuleyle çakışıyor | **KAPANDI** | **138,0:** "1338" levhası sola alındı.<br>**237,6:** "22 TEMMUZ 1378" levhası da solda. |

**Özet:**
- **Engelleyici (B):** 4'ün 4'ü kapandı.
- **Önemli (Ö):** 6 kapandı, 1 kısmen, 1 açık.
- **Küçük (K, toplam 15):**
  - kapandı: 9;
  - kısmen: 1;
  - açık: 3;
  - açık ama stil ya da kimlik kararı olarak kabul: 2.

## 3. Yeni sorunlar
Bu bulguların bir kısmı tur 1'de de vardı ama gözümden kaçmıştı. Y4 ise düzeltmelerin getirdiği bir gerilemedir.

**Y1 · ÖNEMLİ (katman) · Figür soldurularak belirirken baş ve ayakkabılar gövdeden önce, tam opak geliyor; havada asılı kafa görüntüsü.**
- **131,3–131,8 sn (c1_darphane, Villani'nin girişi):** Kırmızı kepli, sakallı baş gövdesiz duruyor (x≈1600–1720, y≈380–500). Gövde 0,6 sn içinde saydamdan belirirken baş baştan opak.
- **143,8–144,6 sn (c1_okul'un girişi):** Öğretmenin yeşil sarıklı başı boş duvarda tek başına duruyor (x≈985–1070, y≈400–525; tam çözünürlüklü kare 143,9).
- **Neden:**
  - `cilt_anim.draw_fig`, başı ve ayakkabıları `blit` ile alfa uygulamadan çiziyor.
  - `cilt_oda._blit_cf` yaması bu iki parçaya yalnız siluet renk süzgecini taşıyor, alfayı taşımıyor.
- **Düzeltme:**
  - `blit`'e alfa boyası eklenir, ya da her figür `saveLayerAlpha` ile tek katmanda soldurulur.
  - P2–P7'de alfa ile soldurulan her figürde aynı hata çıkar.
  - Yeniden render: 2 çekim.

**Y2 · ÖNEMLİ (dönem) · Loggia dei Lanzi 1338'de.**
- **137,3–144,2 (1338 · ≈90.000 kişi):** Sağ kenarda yonca frizli teras, korkuluk ve büyük yuvarlak kemer görünüyor (x≈1650–1920, y≈440–930; en belirgin 141,1–142,6 arası).
- **Neden:** `cilt_sehir._draw_main`, `loggia()` işlevini yıla bakmadan çağırıyor; işlevin açıklaması "Loggia dei Lanzi".
- **Tarih:** Loggia 1376'da başladı, 1382 dolayında bitti [güven: yüksek]. 1338'de henüz yoktu. 22 Temmuz 1378 çekiminde (234,8–239,8, sağ kenar x≈1830–1920) de bitmiş gibi duruyor; o tarihte inşaattaydı.
- **Düzeltme:**
  - `donem.loggia_stage(y)` eklenir: 1376'dan önce sıradan ev cepheleri; 1376–1382 arası ayaklar ve iskele; 1382'den sonra tam yapı.
  - Kural `qa_donem`'e de girer.
  - Yeniden render: 2 çekim.

**Y3 · ÖNEMLİ (HUD ve olgu) · HUD 1252'de kalırken 14. yüzyıl kişileri sahnede.**
- **119,4–127,1 (c1_cicek):** Ekranda "DANTE" levhası (x≈90–600, y≈105–215) ve HUD 1252 birlikte. "Lanetli çiçek" dizesi Paradiso IX'tan, ≈1316–21 [güven: orta-yüksek].
- **130,4–137,3 (c1_darphane):** Levha "GIOVANNI VILLANI · KRONİKÇİ · ESKİ DARPHANE YÖNETİCİSİ" (x≈740–1500, y≈170–320), HUD 1252.
  - DBI'ye göre Villani 1317'de darphane görevlisiydi (`teyit_P1.md`, c1s5).
  - Ekran "1252'de darphanede Villani" der gibi okunuyor; 1252'de Villani henüz doğmamıştı.
- **Düzeltme:** `YIL_AT`'a iki adım eklenir:
  - c1s3 "Dante" → "≈1320" (ya da yıl alanı gizlenir);
  - c1s5 "Villani" → 1317.
- **Aynı sınıftan küçük bir örnek:** 78,0–86,6'da Uffizi kuyruğunda "BUGÜN" levhası (x≈800–1120, y≈145–220) ile HUD 1737 yan yana duruyor. HUD "BUGÜN" yazmalı ya da gizlenmeli.

**Y4 · ÖNEMLİ (dönem katmanının getirdiği gerileme) · 1520 tarihli Medici mührü 1429 armasıyla çizildi.**
- **575,5–580,0 ("O KALEM · MEDİCİ SİPARİŞİ"):** Balmumu mühürde kenar boyunca 8 nokta var (`red8`; x≈1250–1470, y≈335–550).
- **Olgu:** Sipariş 1520'de, kardinal Giulio de' Medici'nin başında olduğu Studio Fiorentino'dan geldi [güven: yüksek]. O tarihte Medici arması 6 topluydu: 5 kırmızı ve zambaklı bir mavi.
- **Gerileme:** v1'deki standart biçim (`std`) doğruydu. Katman, nesnenin yılına değil HUD yılına (1429) baktığı için onu yanlışa çevirdi.
- **Düzeltme:**
  - Çekim ya da nesne düzeyinde yıl alanı eklenir (`year=`, ör. `donem.use_year(1520)`).
  - `qa_donem`'e kural: ileriye sıçrayan nesneler kendi yılını bildirmeli.
  - P2–P7'de olayı sonradan yazan her kalemde (Machiavelli, Guicciardini, Vasari) aynı durum yaşanır.
  - Yeniden render: 1 çekim.

**Y5 · KÜÇÜK (metin belirsizliği; KA üyelerine havale) · 172,0–181,2 Villani levhası.**
- Levha: "1300'DE PERUZZİ ORTAĞI · ŞİRKETİ 1341'DE BATTI".
- **Sorun:** "Şirketi" sözcüğü Peruzzi diye okunuyor. Peruzzi 1343'te battı (de Roover); 1341'de batan, Villani'nin Buonaccorsi şirketiydi (DBI; `teyit_P1.md` c1s10).
- **Öneri:** "… · SONRA BUONACCORSİ: 1341'DE BATTI" ya da ikinci yarı kaldırılır.

**Y6 · KÜÇÜK (katman ve yöntem) · 486,4–493,6 catasto sokağı.**
- **Katman:** Gün ışığında renkli figürlerin arasında simsiyah siluet yayalar yürüyor (487,0: x≈40–180 ve x≈910–1010, y≈730–940); "gölge insan" gibi okunuyorlar.
  - Ya hepsi renkli çizilmeli, ya da siluetler uzak plan sis tonuna alınmalı.
- **Yöntem:** Catasto kapı kapı dolaşılarak değil, hane reislerinin yazılı beyannamesiyle (*portata*) toplandı [güven: yüksek].
  - Sahne "masaya beyanname getiren hane reisleri" diye kurulursa hem doğru olur hem daha az şablon görünür.

**Y7 · KÜÇÜK · Tiaralar tutarsız.**
- **439,8:** Cossa'nın başında altın, arı kovanı biçimli bir tiara (x≈1020–1090, y≈390–510).
- **462,0:** Martinus'ta beyaz gövdeli, altın taçlı tiara.
- Dönem biçimi ikincisi; Cossa'nınki de öyle çizilmeli.

**Y8 · KÜÇÜK (isteğe bağlı) · 464,1 mezar yazıtı.**
- Lahdin ön yüzünde Türkçe "ESKİ PAPA" yazıyor (x≈660–1260, y≈715–800).
- Mezarın gerçek yazıtında "quondam papa" ifadesi geçer [güven: yüksek].
- Taşa Latince "IOANNES QVONDAM PAPA" yazılıp Türkçesi alttaki levhaya alınırsa fresk ve defter diline daha sadık olur.

**Y9 · KÜÇÜK (okunurluk) · 552,5–559,7 Cavalcanti.**
- **Mekân:** Levha "HAPİSTE" diyor, ama oda 1348 kronikçisinin (201,4–203,5) "hücre" kitiyle aynı: yatak ve camlı, büyük kafes pencere.
- **Kişi:** Cavalcanti, Machiavelli ile neredeyse aynı kostümde: sarı cüppe ve mavi kep (556,4 ile 578,0'ı karşılaştırın). "İki kalem, iki biçim" karşıtlığı görselde siliniyor.
- **Öneri:** Pencereye parmaklık eklenir, Cavalcanti'ye ayrı bir renk verilir.

## 4. Kullanıcının sorusu: "Bu çizim tarzı çok mu basit, ucuz görünüyor; yapay zekâ ile üretilmiş gibi mi duruyor?"
**Kısa cevap:** Yapay zekâ üretimi gibi durmuyor, ucuz da durmuyor; ama yer yer şablon gibi duruyor.

**YZ izleri neden yok:** Dönem konulu YZ görsellerini ele veren üç şey vardır: bozuk yazı, uydurma arma ve birbirine karışmış yüzyıllar. Bu videoda üçünün de tersi var:
- **Yazılar doğru Latince ve İtalyanca:**
  - florinde "S·IOHANNES·B" ve "FLORENTIA" (125,8; 305,4);
  - madalyada "COSMVS · MEDICES" (582,6);
  - defterde "DEBITORI / CREDITORI" (414,5).
- **Arma ve simgeler yıla bağlı bir kurala göre değişiyor:**
  - 1465 öncesinde zambaksız, 8 toplu arma;
  - etamenli Floransa zambağı;
  - doğru yöne bakan papalık anahtarları.
- **Bazı ayrıntılar ancak araştırmadan çıkabilir:**
  - kura torbası (224,0);
  - 25 Mart yılbaşı kartı (522,6);
  - iskeleli, vinçli yarım kubbe (585,2).

**"Basit" algısı:** Bu algı bilinçli bir üslup seçiminden geliyor. Düz renkli, konturlu kesme-bebek figürler ve Gozzoli/Lorenzetti friz dili, fresk geleneğine sadık bir sadelik; tek başına ucuz okunmuyor.

**Ucuz ya da şablon okunan üç şey:**
1. **Aynı oda kiti her yerde:** Ağaçlı duvar halısı, kafes cam ve uzun masadan oluşan oda 1390'ların Roma'sında (298,6), 1415 Konstanz'da (442,8), 1419'da papanın salonunda (462,0) ve 1743 Pitti'sinde (23,0) aynı.
2. **Aynı kostüm kiti beş yüzyıl boyunca:** 1252'den 1743'e aynı giysiler; üstüne 17. yüzyıl şapkalı siluetler.
3. **Gözü yakan teknik izler:** başı gövdesinden önce beliren figürler (131,3; 143,9) ve kesik etiketler (365,4).

**Çare:** Şablon hissini en çok iki iş azaltır:
- çağa bağlı kostüm ve oda ön ayarı (`donem.py`'ye iki tablo);
- Y1'in alfa düzeltmesi.

## 5. PK1-Y6 kararı: kapaktaki arma 6 top, bölüm kartındaki 8 top
**Karar: kapak videoya uysun.** 1397–1429 için `donem.py`'nin ürettiği arma kullanılmalı: altın alan, kenar boyunca 8 kırmızı top, mavi top yok.

**Gerekçe:**
- **K2'deki kalkanın kaynağı yok:** Kalkanda 1-2-2-1 dizilimli 6 kırmızı top var (1280×720 karede x≈837–897, y≈358–426). Bu, 1465 sonrasındaki 5+1 düzeninin mavi topunun kırmızıya boyanmış hâli. Belgelenmiş bir varyant olduğunu gösteren bir kaynak bizim setimizde yok: `notlar_donem.md` Cosimo için 8, Giovanni di Bicci için 11 top veriyor (Ceramelli Papiani).
- **"Tek doğru" sayı yok:** 15. yüzyılda top sayısı 5 ile 11 arasında oynadığı için 8 tek doğru sayı değil.
- **Tutarlılık:** Video, kapak ve sonraki parçalar tek kuralda (`donem.py`) birleşmeli. Böylece 1465'te mavi topun gelişi P3'te görünür bir dönüm noktası olur.

**Maliyet ve önem:**
- 168 px'te iki biçim arasındaki fark görünmüyor (PK1 haklı); tanınırlık değişmez.
- İş: `kapak_medici.palle_erken(n_balls=6)` yerine `CP.arms_image(variant="red8")` ve kapağın yeniden üretimi; birkaç dakika.
- Önem küçük, ama yayından önce yapılmalı.

**K1:** 1743 belgesindeki mühür standart biçimde ve doğru.

## 6. Dönem katmanı (`donem.py`) üzerine kısa değerlendirme
**İyi kurulmuş yanları:**
- Tek doğruluk kaynağı var; kuralların kaynak tablosu (`notlar_donem.md`) yanında duruyor.
- Denetim, kuralların bağımsız bir kopyasıyla yapılıyor; doğru yöntem.
- "Çekim yılı = HUD'da en uzun kalan yıl" kuralı yapıların çekim ortasında birden değişmesini önlüyor.
- Marka türleri ve yılsız modlar kapsam dışında tutulmuş; P2–P7 için duman testi yapılmış.
- Tur 1'de önerdiğim iyileştirme 1 ve 2 beklediğimden iyi uygulanmış.

**P2–P7 için eksikler (öncelik sırasıyla):**
1. **Nesne ve çekim düzeyinde yıl alanı (Y4).**
2. **Bina listesi:**
   - Loggia dei Lanzi 1376–82 (Y2);
   - Palazzo Medici 1444'ten itibaren; Uffizi 1560'tan itibaren;
   - Pitti 1458'den itibaren, büyük genişleme 1560'larda;
   - kodda "Santa Croce çan kulesi" diye etiketli sivri kule: bugünkü kule 1842 yapımı; ekranda etiketlenecekse TEYİT edilmeli.
3. **Kişi yaşam aralığı tablosu:** HUD yılında hayatta olmayan bir kişiyi niteleyicisiz gösteren levha için kapı (Y3'ü otomatik yakalardı).
4. **Kostüm ve oda ön ayarları:** Ö4, K6, K7 ve K11'i birlikte çözer.
5. **1438 sonrası madalyalar (KA2'nin alanı, not düşüyorum):** TEMSİLÎ damgası şu an yalnız tarihe bağlı. 1438 sonrası madalyalar damgasız çıkacak ama yüzler yine uydurma; "benzerlik iddiası yok" işareti tarihten bağımsız olmalı.

## 7. En emin olmadığım nokta
1. **Palle sayısı:** 15. yüzyılda 5 ile 11 arasında oynuyor. 8'i "tek doğru" diye değil, tutarlılık için öneriyorum. Giovanni di Bicci'nin kendi armasının arşiv varyantı 11 top olabilir; doğrulayamadım.
2. **Tarihler:** Dante dizesinin tarihi (≈1316–21) kendi bilgimden geliyor. Villani'nin 1317'si `teyit_P1.md` (DBI) kaynaklı. Loggia (1376–82), Machiavelli siparişi (1520) ve catasto beyannamesi bilgileri yine kendi bilgimden; güvenim yüksek, ama bu turda web doğrulaması yapmadım.
3. **Y1'in süresi:** Saniyede 8 karelik şeritlerle ölçtüm, tam kare sayısını ölçmedim. Kodda başka soldurulan figür aradım: darphane ve okul çekimleri var; `fade_out_at` ve kapı soldurması P1'de kullanılmıyor. Ama her çekimi tek tek karelemedim.
4. **Y6'daki siluetler:** Siyah siluetlerin bilinçli bir "anonim yaya" seçimi olup olmadığını bilmiyorum. Bilinçliyse bile gün ışığında ton sorunu sürüyor.
