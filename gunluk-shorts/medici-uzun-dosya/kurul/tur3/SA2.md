# SA2 · Tur 3 · Sanat ve üslup · Mercek: DÖNEM / GELENEK UZMANI (dönem doğruluğu, katman ve okunurluk)
Medici Parça 1 v3 (`out_p1/medici_P1.mp4`, 601,54 sn, 14.437 kare) · 5 Kasım 2026 · tek üyeli gerileme kontrolü

## 1. Karar
**RED, 8,8/10** (tur 1: 5,0 · tur 2: 8,5; eşik ≥9).

- **Tur 2 koşullarımın hepsi kapandı:** Y1 figür alfası, Y2 Loggia, Y3 HUD yılları, Y4 1520 mührü ve kapak arması. Ö4 (1252 kıyafeti) kısmen kapandı, ama kalan fark küçük. Tur 2 hesabıma göre bu durum 9,5'e denk düşerdi.
- **Puanı eşiğin altında tutan tek şey yeni bir ÖNEMLİ bulgu (Y10):** Rehin mitranın üstündeki işaret bir Hristiyan motifi değil, rün benzeri uydurma bir simge. Ortasından dikey bir çizgi geçen eşkenar dörtgen ve iki bacaktan oluşuyor; görünüşü Othala/odal rününe (ᛟ) çok yakın. Rehin mitra 464,7–475,8 sn arasında dört çekimde görünüyor. 470,0–471,7 sn arasındaki yakın planda ekranın ortasında, yaklaşık 380 px yüksekliğinde duruyor.
  - Benim alanımda bu bir simge doğruluğu hatası.
  - Bu rünün aşırı sağ kullanımı nedeniyle hassasiyet tarafını KA2'ye havale ediyorum.
- **Düzeltmenin maliyeti:** tek bir ikon (`c2_kinds._i_mitra`) ve yaklaşık 11 sn'lik dört çekimin yeniden render'ı.
- **Yol:** Y10 düzelirse **ONAY 9,4**. Üç küçük madde de (Y11 papa sakalı, Y12 zaman çizelgesindeki HUD, Y13 levhanın kalkanı örtmesi) düzelirse 9,6.

**Sınır:** Videoyu oynatamadım, sesi dinleyemedim.

**Dayanaklar:**
- **Kareler:** v3'ün 102 çekiminin her birinin ortasından birer kare ve yaklaşık 30 tam çözünürlüklü kare.
- **Saniyede 8 karelik şeritler:** 130,9–132,4, 143,6–145,1 ve 229,9–231,4.
- **Belgeler:** `qa_flow_v3.txt` ("Dönem (ENG-A) GEÇTİ · 306 kare · İHLAL 0"), `KURUL.md` (tur 2 kararları), `duzeltme_tur2/ENG-C.md`, `SCN-1.md`, `SCN-2.md`.
- **Kod:** `donem.py` (`loggia_stage`), `p1_ortak.nesne_yili`/`seal_drop`, `c2_kinds._i_mitra`, `cilt_anim` (papa kiti).
- **Kapak:** `yayin/studio_paketi_P1/kapak_P1_K2.jpg`.

## 2. Tur 2 maddelerimin durumu
Zaman damgaları v3'e göredir. Koordinatlar 1920×1080 çerçevededir, ±25 px.

**Tur 2 ONAY koşulları**

| Madde | Durum | Kanıt (v3) |
|---|---|---|
| **Y1** Figürün başı gövdesinden önce, opak beliriyordu | **KAPANDI** | **Okul (143,6–145,1):** öğretmen ve üç çocuk tek katmanda, aynı saydamlıkla birlikte beliriyor (yaklaşık 144,4–144,6); gövdesiz baş yok.<br>**Lonca (229,9–231,4):** yün tarayıcısının silueti (başı ve tarağıyla) tek parça olarak soluyor.<br>**Darphane:** Villani artık çekimin başından tam görünür (130,9); soldurma yok. |
| **Y2** 1338'de Loggia dei Lanzi | **KAPANDI** | **141,1 / 142,6 (1338):** Sağ kenarda (x≈1600–1920) Loggia değil, panjurlu ev cepheleri var; frizli teras yok.<br>**237,6 (22 Temmuz 1378):** Sağ kenarda iskele ve kademeli yükselen taş ayaklar (x≈1755–1920, y≈615–915).<br>Kural `donem.loggia_stage`: 1376'dan önce yok, 1376–81 inşaat, 1382'den sonra tam. Bağımsız kopyası `qa_donem`'de var. Sınır için §5'e bakın. |
| **Y3** HUD yılı içerikle çelişiyordu | **KAPANDI** (başkanın 1338 kararıyla) | **Dante (119,4–127,1):** HUD gizli (120,0 ve 126,8).<br>**Villani:** HUD 130,9'da 1252'den 1338'e dönüyor; levha "ESKİ DARPHANE YÖNETİCİSİ" diyor. Benim önerim 1317'ydi; başkan KA1'in gerekçesini seçti, itirazım yok.<br>**Uffizi "BUGÜN" (82,7):** HUD gizli.<br>**c1'deki Machiavelli çekimleri (255,7 ve 263,3):** HUD gizli.<br>Aynı sınıftan bir gerileme için Y12'ye bakın. |
| **Y4** 1520 mührü 1429 armasıyla (8 top) çiziliyordu | **KAPANDI** | **578,0:** Mühürde 1-2-2-1 düzeninde 6 top var; üstteki büyük topta zambak kabartması (x≈1020–1380, y≈450–790).<br>Nesne yılı `p1_ortak.nesne_yili(1520)` ile veriliyor; HUD 1429'da kalıyor. Doğru: nesne kendi yılına göre çiziliyor. |
| **Kapak arması** (PK1-Y6: K2'de 6, bölüm kartında 8 top) | **KAPANDI** | **K2 (07:07):** Kesenin bağındaki kalkanda kenar boyunca 8 kırmızı top var, mavi top yok (1280×720 karede x≈835–897, y≈358–427).<br>**341,4:** Bölüm kartı II ile birebir aynı. |

**Tur 2'deki diğer maddeler (Y5–Y9)**

| Madde | Durum | Kanıt (v3) |
|---|---|---|
| **Y5** Villani levhası ("şirketi 1341'de battı") | **KAPANDI** | **177,1:** "1300'DE PERUZZİ ORTAĞI · YÖNETTİĞİ BUONACCORSİ 1341'DE BATTI". |
| **Y6** Catasto: kapı kapı dolaşma, simsiyah yayalar | **KAPANDI** | **486,4–493,6:** Catasto dairesi. Kireç sıva, Komün kalkanı (beyaz zeminde kırmızı zambak), beyanname rafları; hane reisleri masaya *portata* getiriyor; bütün figürler renkli.<br>Küçük bir yerleşim kalıntısı için Y13'e bakın. |
| **Y7** Tutarsız tiaralar | **KAPANDI** | **439,8:** Cossa'nın tiarası beyaz kovan gövdeli, altın taçlı.<br>**462,0:** Martinus'unki aynı dilde. |
| **Y8** Mezarda Türkçe yazıt | **KAPANDI** | **464,1:** Lahitte "IOANNES QVONDAM PAPA"; levhada "ESKİ PAPA · ÇEVİRİ BİZE AİT". |
| **Y9** Cavalcanti'nin "hapis" odası | **KAPANDI** | **556,4:** Stinche hücresi: parmaklıklı yüksek pencere, zincir halkası, kaba taş.<br>Cüppe gri-yeşil, başlık koyu kahve; 542,6'daki Machiavelli'nin sarı-mavisinden ayrışıyor. |

**Tur 1'den kalan açık ve kısmi maddeler**

| Madde | Durum | Kanıt (v3) |
|---|---|---|
| **Ö4** 1252'de 15. yüzyıl kıyafeti | **KISMEN — kabul edilebilir** | **110,0 / 112,5 (1252 pazarı):** mazzocchio, mi-parti çorap ve brokar yok; kukuleta ve başörtüsü var, tunikler dize iniyor.<br>**127,6:** Darphane ustasında cappuccio ve sade tunik.<br>**Kalan:** giysi kesimi çağa bağlı değil. Örneğin 110,0'da kürk yakalı siyah uzun cüppe (x≈1520–1630, y≈720–940) 14. yüzyıl sonu–15. yüzyıl görünümü taşıyor. Küçük; P1'de düzeltme istemiyorum. |
| **Ö2** 1378 isyan kadrosunda brokar | **KISMEN** (küçük, değişmedi) | **217,2:** Baklava ve benek desenli zengin cüppeler hâlâ var:<ul><li>x≈300–430, y≈455–735;</li><li>x≈790–980, y≈540–840.</li></ul>1378 için desen kuralı izin veriyor; ama halk alayında fazla zengin. Kabul. |
| **K3** Orsanmichele'nin "Yunan tapınağı" simgesi | **KAPANDI** | **320,5:** Kübik Gotik blok; zemin katta sivri kemerli üç açıklık, üstte ikiz pencereler. |
| **K5** Kitapların sırtı dışarı dönük | **KISMEN, kabul** | Banka ve kâtip odalarında kitaplar yatık istiflenmiş (328,8; 414,5).<br>Machiavelli'nin kütüphanesinde (252,5–267,3) dik duruyor; 1520'ler için sınırda. |
| **K6** Kafes cam / **K11** 1737–43 iç mekânları | **Stil kararı olarak kabul** (başkan kaydı) | Değişiklik yok, değişiklik de istemiyorum. |
| **K7** 17. yüzyıl şapkalı siluetler | **KAPANDI** | Geniş kenarlı şapka kalmadı:<ul><li>191,9 (veba odası): yuvarlak başlık;</li><li>195,7 (sokak): düz tepeli kep;</li><li>231,6 (yün tarayıcısı): coif;</li><li>263,3 (isyancı): kukuleta;</li><li>542,6: rulo başlık.</li></ul> |
| **K14** Kesik harita etiketleri | **KAPANDI** | **365,4:** BRUGGE ve BARSELONA tam okunuyor.<br>**294,0:** Roma haritasında FLORANSA çerçevenin içinde.<br>**68,8:** "SINIR YAKLAŞIKTIR" sol üstte, kartla çakışmıyor. |
| **Yer başına setler** (tur 2 §4: "aynı oda kiti her yerde") | **KAPANDI** | Her yer ayrı ve dönemine uygun:<ul><li>**Brugge (353,9):** basamaklı tuğla alınlıklar, yuvarlak cam göbekli pencereler, dışbükey ayna, damalı zemin.</li><li>**Konstanz (442,8):** altın zeminde tek başlı siyah kartal. 1415'te Sigismund Roma Kralı'ydı; çift başlı kartal 1433 imparatorluğundan sonra gelir, yani doğru seçim.</li><li>**Papalık salonu:** dişleri yukarı bakan anahtarlar.</li><li>**Catasto dairesi**, **Stinche** ve **kâtip odası** (DEBITORI / CREDITORI).</li></ul> |
| **Tur 2 §6: P2–P7 motor notları** | **Kısmen** | **Var:**<ul><li>nesne yılı (`p1_ortak.nesne_yili`, `seal_drop(year=)`);</li><li>Loggia kuralı;</li><li>çağa bağlı başlıklar;</li><li>paket metninde "bütün figürler temsilîdir".</li></ul>**Yok (P2 için not):**<ul><li>`nesne_yili` P1 kütüphanesinde; P2–P7 için `donem.py`'ye taşınmalı;</li><li>Palazzo Medici (1444/45'ten itibaren; P2'nin merkezi), Uffizi (1560'tan itibaren) ve Pitti için bina kuralları;</li><li>kişi yaşam aralığı kapısı.</li></ul> |

## 3. Gerilemeler ve yeni sorunlar

**Y10 · ÖNEMLİ (simge doğruluğu; hassasiyet tarafı KA2'ye) · Rehin mitrada rün benzeri uydurma işaret.**
- **Nerede:**
  - **470,0–471,7 (yakın plan, ≥2× ara plan):** Altın mitra ekranın ortasında (x≈765–1030, y≈310–700). İşaret x≈815–990, y≈360–655 aralığında.
  - Ayrıca 464,7–466,9 (rivayet, x≈870–1040, y≈440–680), 466,9–470,0 (Giovanni elinde) ve 471,7–475,8 (diz çöken Giovanni'nin elinde).
- **Ne görünüyor:** Mitranın ortasından dikey bir çizgi geçiyor; üstünde bir eşkenar dörtgen var, dörtgenin alt köşesinden iki bacak açılıyor. Biçim Othala/odal rünü ᛟ ile ortadan geçen bir çubuğa çok benziyor.
- **Kaynağı:** `c2_kinds._i_mitra` üç çizgi oyuyor:
  - dikey orfre: (256,112)→(256,410);
  - eşkenar dörtgen: tepe noktası (256,130), alt köşesi (256,250);
  - alt köşeden açılan ters V: (168,330)→(256,250)→(344,330).
  Niyet büyük olasılıkla "orfre ve süs"tü; sonuç ise bir rün.
- **Neden önemli:**
  1. **Dönem:** 15. yüzyılın değerli papalık mitrası (*mitra pretiosa*) orfre şeritleri (*titulus* ve *circulus*), inci ve taşlarla süslenir. Rün, pagan ve İskandinav çağrışımlı, döneme yabancı bir işaret.
  2. **Konum:** Rehin mitra P1'in belgeli anekdotunun nesnesi ve ekranın ortasında, büyük duruyor.
  3. **Risk:** Othala rünü bazı bağlamlarda aşırı sağ simgesi olarak kullanılır. Katolik bir nesnenin üstünde yorum çekebilir.
- **Düzeltme:**
  - İkon şu motiflerle yeniden çizilir:
    - orfre: dikey şerit ve taban şeridi;
    - şeritlerde 5–7 inci ya da taş noktası;
    - isteğe bağlı küçük haç.
  - Dörtgen ve ters V kaldırılır.
  - 4 çekim yeniden render edilir (≈11 sn).
- **Not:** Tur 2'de bu ikon rivayet çekiminde küçük boyda vardı; gözümden kaçmıştı. v3'ün yakın planı onu büyüttü.

**Y11 · KÜÇÜK (dönem) · V. Martinus sakallı.**
- **Nerede:** 460,4–463,3 ve 471,7–475,8. Koyu, kısa sakal ve bıyık (462,0'da x≈1260–1370, y≈190–300; 474,0'da yaklaşık x≈1285–1325, y≈320–365).
- **Olgu:** 13. yüzyıldan II. Julius'a (1511) kadar papalar sakal bırakmadı [güven: yüksek]. Martinus'un Lateran'daki tunç mezar figürü sakalsızdır. Cossa doğru biçimde sakalsız çiziliyor (439,8).
- **Neden:** Papa kitinde `beard=[None, "short"]` var; Martinus'un tohumu sakallı çıkıyor.
- **Düzeltme:** 1511'den önce papa için `beard=None`. Kural `PERIOD_COSTUME`'a eklenmeli; P3 (IV. Sixtus) ve P4 (X. Leo) için de geçerli.

**Y12 · KÜÇÜK (gerileme, HUD) · Çifte kayıt zaman çizelgesinde HUD yeniden göründü.**
- **Nerede:** 416,0–431,6 (`c2_masa v="iz"`). HUD 1402'yi gösterirken defter sayfasında "CENOVA 1340 … PACİOLİ 1494" ve 1320–1520 çentikli cetvel var (418,0; 424,6).
- **Gerileme:** v2'de bu çizelgede HUD gizliydi (tur 2: 420,3). SCN-2 çekimleri birleştirirken `hud=False` düşmüş.
- **Düzeltme:** Çekime `hud=False` eklenir. İstenirse yalnız `zoomthru`'dan sonra gizlenir; kâtip odasında 1402 kalır.

**Y13 · KÜÇÜK (katman) · 486,4–493,6 Catasto dairesi.**
- "HANE REİSLERİNİN BEYANNAMESİ · PORTATA" levhası (x≈510–1610, y≈270–334) Komün kalkanının üst üçte birini örtüyor (kalkan x≈1130–1300, y≈225–430). Dairenin kimliğini taşıyan zambağın tepesi görünmüyor.
- **Düzeltme:** Levha y≈470'e ya da kalkanın soluna alınır.

**Bakıp temiz bulduğum, gerileme olmayan noktalar:**
- **Kubbe ve çan kulesi:**
  - 1338 ve 1348'de kubbe yok;
  - 1378'de çan kulesi tam boy;
  - 1429'da yarım kubbe ve iskele (588,5).
- **Sancaklar:**
  - 1378'de Popolo haçı, Komün zambağı ve düz sancaklar (217,2; 237,6; 269,7);
  - Medici sancağı yok.
- **Madalyalar:** Lorenzo ve Cosimo'da TEMSİLÎ damgası var (530,7; 582,6); "COSMVS · MEDICES" doğru.
- **Bölüm kartı II:** `red8` (341,4).
- **Marka armaları:** ana başlık (103,7) ve bitiş ekranı (597,0) `std`; marka işareti olarak doğru.
- **Damgasız dönem metinleri:** Sayfalarda gerçek İtalyanca ve Latince metin var: Machiavelli'nin "Muoio contento…", Cavalcanti'nin "…dalle mondane sollecitudini…" satırları ve *Istorie fiorentine* (567,7; 578,0).
- **Salvestro'nun kura torbası (*borsa*):** 224,1.

## 4. Kullanıcının sorusu ("ucuz mu, YZ gibi mi?")
**Değişti, iyi yönde.** Tur 2'de "ucuz değil ama yer yer şablon" demiştim. Şablon hissinin iki kaynağı büyük ölçüde gitti:
- **Her yerin kendi seti var:** Brugge'nin basamaklı alınlıkları ve dışbükey aynası, Konstanz'ın Roma Kralı kartalı, catasto dairesi, Stinche hücresi.
- **Figürler doğal davranıyor:** başları gövdeleriyle birlikte, tek parça beliriyor; başlıklar çağa uyuyor.

YZ izlenimi yok. Tersine, sayfalarda okunabilen gerçek İtalyanca ve Latince metinler el emeğini gösteriyor.

**Tek istisna:** mitradaki rün benzeri işaret (Y10). Böyle "uydurma sembol", YZ görsellerinin bilinen izlerinden biri. Düzeltilince bu açık da kapanır.

## 5. En emin olmadığım nokta
1. **Y10'un okunuşu:** Mitradaki işaretin izleyiciye "rün" ya da Othala gibi görüneceği benim yorumum. Biçim (ortası çubuklu, bacaklı eşkenar dörtgen) bence nesnel olarak ᛟ'ye çok yakın. Ama Türk izleyicinin çoğu bu çağrışımı kurmayabilir. Bu yüzden önemi alanım açısından (yanlış dönem simgesi) veriyorum. Nefret simgesi boyutunun ağırlığına KA2 karar versin.
2. **Loggia'nın Temmuz 1378'deki yüksekliği:** Kaynakta yok. Ekrandaki "ayaklar ve iskele" makul bir genel temsil: küçük, kenarda, iddia taşımıyor. SCN-1 ile aynı belirsizliği taşıyorum, itirazım yok.
3. **Y11 (papa sakalı):** Genel kural ve Martinus'un mezar figürü kendi bilgimden geliyor [güven: yüksek]; bu turda web doğrulaması yapmadım.
4. **Y1'in kapandığı:** Üç soldurma noktasında saniyede 8 karelik şeritlerle doğruladım, her kareyi tek tek değil. Kodda başka soldurulan figür kalmadığını ENG-C'nin taramasına dayanarak varsayıyorum.
