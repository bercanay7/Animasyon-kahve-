# Çekim listesi (storyboard)

Her cümle bir ya da birkaç çekimdir. Zamanlar `timeline.js`'ten gelir (`S('B03')`, `Wd('B03','idadi')`).

- **Bölüm başında:** `press` geçişi ve `chapterCard`.
- **İlk görünüş:** kişinin ilk görünüşünde `nameTag` (ad + yaş).
- **Dönem:** her çekimin üst yorumu bölümün dönemini söyler. Yaş, başlık ve kıyafet o döneme göre seçilir (USLUP.md).
- **Kalıplar:** kâğıt, is ve en çok 3 renk kalıbı. Kırmızı finale saklanır.

## 0 · Açılış (A01–A05) · act0.js
- **A01 · Çankaya, gece, dış.**
  - Köşk silueti; lacivert gece, kâğıt yıldızlar, pencerelerden altın ışık.
  - Yavaş yakınlaşma.
  - Damga: `ANKARA · 28 EKİM 1923 · GECE`.
  - Geçiş: pencereden içeri baskı geçişi.
- **A02 · Sofra.**
  - Beyaz örtü (kâğıt), lamba halesi, çay bardakları. **Kadeh yok.**
  - MK (42, sivil koyu ceket, başı açık, bıyıksız) masanın başında ayakta; ¾ yakın.
  - Konuklar anonim siluetler.
  - "Yarın Cumhuriyet ilan edeceğiz!" sözü `quote` ile; künye: `— Nutuk, 1927`.
- **A04 · Kuşak şeridi.**
  - Sofradakilerin yüzleri yan yana bir şerit olur. Yaş levhaları basılır: 42, 39, 39, 43, 40.
  - "Otuz yıl önce": şerit aynı sırayla 1890'ların okul sırasına eşleşir (fesli çocuklar, kara tahta). Bu, sınıf fotoğrafı eşleşmesidir.
  - "İkinci Abdülhamid'in" sözünde duvarda Abdülhamid portresi (nötr ışık), levha `II. ABDÜLHAMİD · 1876–1909`.
- **A05 · Başlık kartı.**
  - `BİR KUŞAĞIN HİKÂYESİ` (Abril). Altında küçük: `Cumhuriyet'i kuranlar nasıl yetişti?`
  - Arkada kuşak şeridi: 7 büst siluet.

## I · Sultanın okulları (B01–B06) · act1.js
- **B01.**
  - İmparatorluk haritası 1876: kalıp dolgusu Balkanlar'da `clip` ile silinerek küçülür (toprak kaybı); borç senetleri damgalanır.
  - "Meclis'i süresiz tatil etti": Meclis kapısına kilit ve mühür.
  - Yıldız Sarayı silueti, gece; tek pencere ışığı.
- **B02.** Abdülhamid masada (fes, kırçıl kısa sakal, setre/İstanbulin), nötr ışık. Önünde okul planı, yanında jurnal kâğıtları. Kuşak olmadan, yalnız o.
- **B03.**
  - Harita: rüşdiye noktaları (600+) ve idadi kareleri (100+) lastik damgayla basılarak çoğalır.
  - `bigStamp('600+')` ve `bigStamp('100+')`.
- **B04.** Askerî idadi yatakhanesi: perspektifte sıra sıra demir karyola, fesli çocuklar. Üç simge: ekmek, setre, kitap.
- **B05 (yorum).**
  - Taşradan gelen bir baba-oğul okul kapısında.
  - "karnesiyle": karne yakın plan, not damgası (Osmanlıca soyut yazı; `PEK İYİ` izleyici katmanında).
- **B06.**
  - Selanik sokağı. Küçük Mustafa (12, fes) askerî rüşdiyeye girer.
  - Sınıf: kara tahtada geometri çizimi (yazı değil); öğretmen.
  - "Kemal": `nameTag` `MUSTAFA → MUSTAFA KEMAL` dönüşümü.

## II · Selanik ve yasak kitaplar (C01–C06) · act2.js
- **C01.**
  - Selanik rıhtımı panoraması: turkuaz deniz, Beyaz Kule, vapurlar, kalabalık damgaları (fes, şapka, başörtü).
  - Fransızca ve Rumca tabelalar serbest.
- **C02 (yorum).** Rıhtımda denize bakan çocuk; gazeteler farklı alfabelerle uçuşur.
- **C03.**
  - "sorgulamayı": soru işaretine dönüşen bir pergel ya da kalem.
  - Manastır ve Harbiye yatakhanesi, gece (lacivert). Yorgan altında mum ışığı; kitap elden ele geçer.
  - "Namık Kemal… vatan… hürriyet…": kelimeler Cormorant italik ile tek tek belirir.
- **C04.** Hafiye silueti pencerede. Jurnal kâğıtları Yıldız'daki masaya yığılır; karanlık.
- **C05.** 1889, Askerî Tıbbiye: dört öğrenci silueti, loş oda, el ele yemin. `İTTİHAT VE TERAKKİ'NİN ÇEKİRDEĞİ`.
- **C06.**
  - Kurmay yüzbaşı mezuniyeti: MK (24) ve Ali Fuat (23), setre, fes; ikisine de `nameTag`.
  - İhbar: omuza bir el. Harita: İstanbul → Şam rotası.
  - Şam'da gizli toplantı; `VATAN VE HÜRRİYET` damgası.

## III · 1908 (D01–D04) · act3.js
- **D01.** İmparatorluk haritasında garnizon noktaları birer birer yanar; kuşak şeridi: subay yüzleri.
- **D02.**
  - Makedonya dağları; subaylar dağa çıkar (siluet kolonu).
  - 1908 "Hürriyet" kartpostalı belge olarak gösterilir (kırmızı, turkuaz ve altın bolluğu); kalabalık sevinir.
- **D03.**
  - Hareket Ordusu treni İstanbul'a girer.
  - Yıldız'da boş bir koltuk.
  - Kurmaylar: MK (28) ve Karabekir (27), `nameTag`.
- **D04.** Bölünmüş kare: solda okul ve haritalar, sağda jurnal yığını. Abdülhamid ortada, nötr. Ardından boş sıralar.

## IV · Ateşte dövülen kuşak (E01–E06) · act4.js
- **E01.** Renk çöker: haki, okra, is. Büyük `SAVAŞ` damgası, is patlama yıldızı.
- **E02.**
  - Harita: İstanbul → Mısır → Trablusgarp rotası.
  - Çöl dioraması: Derne, hurmalar; kefiyeli genç binbaşı MK (30) ve yerel gönüllüler.
- **E03.**
  - Balkan haritası: Rumeli dolgusu silinir; Selanik noktası söner.
  - Muhacir kafilesi (kağnılar).
  - Zübeyde Hanım ve Makbule (çarşaflı) bohçalarla.
- **E04 (yorum).** Kuşak şeridi kaybolan Rumeli haritasının önünde.
- **E05.**
  - Çanakkale: turkuaz deniz, sırtlar, siperler.
  - Yarbay MK (34, kabalak) bir sırtta, cep saati.
  - `nameTag` `MUSTAFA KEMAL · 34 yaşında`.
- **E06.**
  - Üç pano: Kafkasya'da kar, Irak'ta nehir, Filistin'de çöl.
  - "İmparatorluk yenildiğinde": panolar kararır.
  - "ve birbirleri": siperde omuz omuza kuşak şeridi.

## V · Anadolu (F01–F06) · act5.js
- **F01.** Samsun, şafak (altın): Bandırma vapuru silueti, iskele. MK (38) sivil kaput, kalpak.
- **F02.**
  - Amasya: masa başında MK, Rauf, Ali Fuat ve Refet; isim levhaları. Rauf'a `nameTag` şart.
  - Telgraf teli doğuya uzanır: Karabekir telgrafla (`tickerTape`).
- **F03.** Gece, İstanbul'dan Anadolu'ya gizli geçiş: İsmet ve Fevzi, `nameTag`.
- **F04.** Sultanahmet mitingi: Halide Edib siyah çarşafla kürsüde, kalabalık damgaları. Sonra haki ceketle çavuş; `nameTag` `HALİDE EDİB · Amerikan Kız Koleji`.
- **F05.**
  - Hızlı montaj: kongre, TBMM binası (1920), Sakarya (Alagöz karesi), Büyük Taarruz şafağı.
  - Kadınlar ve kağnılar.
- **F06.** Alagöz karesi; kuşak şeridi aynı ölçekte MK'nin etrafında birleşir.

## VI · Kapanış (G01–G06) · act6.js
- **G01.**
  - TBMM, 29 Ekim akşamı, 20.30. Mebuslar ayakta.
  - `YAŞASIN CUMHURİYET!`: **ilk kez tam kırmızı bayrak** (alanın en çok %25'i).
- **G02.** Üç büst: MK (Cumhurbaşkanı), İsmet (Başvekil), Fevzi (Erkân-ı Harbiye Reisi). Diploma damgaları `ERKÂN-I HARBİYE · 1898 / 1905 / 1906`.
- **G03.** Kuşak şeridi çatlar (1924), sonra geriye: okul sırası ve siper.
- **G04 (yorum).** Bugünün sınıfı (Latin harfler artık serbest): sıralarda çocuklar, kara tahta.
- **G05.** Soru kartı: `SİZİN HAYATINIZDA İZ BIRAKAN ÖĞRETMEN?` Bir öğretmen silueti.
- **G06.**
  - Son afiş: kuşak şeridi (7 büst) ve bayrak. `CUMHURİYETİMİZİN 103. YILI KUTLU OLSUN`.
  - Bitiş ekranı: ~13 sn, sağ yarı boş (abone ve video öğeleri için).
