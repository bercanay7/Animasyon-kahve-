# Çernobil'in çayı, 1986: üretim planı

Başlangıç: 24 Kasım 2026. Yön usulüyle (`analiz/2026-11-23-deney-yon-promptu.md`); yön kullanıcının (bu oturumun ilk mesajı). Malzeme dosyaları (`analiz/2026-11-24-cernobil-yon-notlari.md`, `2026-11-23-sonraki-video.md`, `2026-11-24-arastirma-sekmesi.md`) bağlayıcı değil.

**Yön (kullanıcının, özet):** reaktörün ya da bir bakanın hikâyesi değil; kötü adam yok. Mayıs yağmuruyla Karadeniz'de bir çay yaprağına konan, görünmeyen, kokmayan bir şeyin hikâyesi. Soru izleyicinin: göremediğin bir tehlikede "korkacak bir şey yok" diyene neye bakarak inanırsın? Cevap kavramla değil, yaprağın yoluyla: toplanıyor, ölçülüyor, kamera önünde bir bardak içiliyor; sonra o yılın çayına ne oluyor? Peşinden gidilecek şey bardakla son arasındaki mesafe. Söz kimden gelirse gelsin dönemin gazetesinden. Hastalıkta bilimin bildiğinden fazlası söylenmez; ölçülmemiş olmak da hikâyenin parçası. İzleyici kendi bardağına bakarak çıkar.

**Kullanıcının fikrini sorma adımı (iş akışı 2):** yön metni bu adımın yazılı hâli; kullanıcı "kararlar senin" dedi (Gılgamış ve Frankenstein'daki gibi). Ayrıca sorulmadı.

**Takvim:** Frankenstein 10 Aralık; bu video dört günlük düzende **14 Aralık 2026, 18:00** (öneri; takvim kullanıcının). Tarihin Dönüm Noktaları listesi.

## 1. Talep kontrolü (24 Kasım; `araclar/talep/talep.py`)
| Sorgu | Öneri | İlk 10 medyan | En çok | Öne çıkan öneriler |
|---|---|---|---|---|
| **çernobil** | 14 | **857 B** | 43,2 M | patlaması anı, belgeseli, faciası |
| çernobil çay | 5 | 251 | 722 B | **çernobil çay içen bakan** |
| radyasyonlu çay | 3 | 234 | 3,6 B | **radyasyonlu çay içen bakan** |
| çernobil türkiye | 6 | 722 B | 16,3 M | türkiye etkisi, "türkiyenin çernobil" |
| cahit aral çay | 2 | 251 | 56 B | |
| çernobil karadeniz | 3 | 417 | 2,1 M | karadeniz etkisi |
| çay radyasyon | 4 | 1,2 B | 703 B | radyasyonlu çay içen bakan |
| *kontrol:* sisifos | 14 | 106 B | 9 M | |

**Okuma:**
- (a) **Kapı kanalın ölçtüğü en büyüğü:** "çernobil" medyanı Sisifos'un sekiz katı. Çay açısı Türkçede boş (medyan 250 civarı), ama otomatik tamamlama "çay içen bakan" sahnesini kendiliğinden öneriyor: izleyici sahneyi biliyor, hikâyeyi bilmiyor.
- (b) **Kişisel soru:** bardak izleyicinin elindeki nesne; "kime inanırsın" sorusu gündem izleyen kitlenin (Araştırma sekmesi) her gün yaşadığı soru.

## 2. Başlık adayları (eleme: **K**işisel soru · **N**efes · **Y**arı tahmin ettirir, ele vermez · **Ka**pı kelimesi önde · **B**ağlamsız)
| # | Aday | Kr. | K | N | Y | Ka | B | Not |
|---|---|---|---|---|---|---|---|---|
| 1 | **Çernobil'in Çayını Sen İçer miydin?** | 35 | ✓ | ✓ | ✓ | ✓ | ✓ | Bardak izleyicinin eline veriliyor; "bakan içti" sahnesini bilen tamamlar, bilmeyen merak eder |
| 2 | Radyasyonlu Çayı Sen İçer miydin? | 33 | ✓ | ✓ | ✓ | ✓ | ~ | "Radyasyonlu çay" arama kalıbı; ama "çernobil" kapısı daha büyük |
| 3 | Çernobil Çayı: "Korkma" Diyene İnanır mısın? | 42 | ✓ | ✓ | ✓ | ✓ | ✓ | Yönün sorusu birebir; ama son dört video "Ad: soru?" kalıbında |
| 4 | Bakan İçti, Sen İçer miydin? | 28 | ✓ | ✓ | ✓ | ✗ | ✗ | Kapı kelimesi yok; kapağın sözü |
| 5 | Çernobil'den Sonra Türkiye Neden Çay İçti? | 42 | ✗ | ✓ | ✓ | ✓ | ✓ | "Neden" kalıbı; kişisel değil |
| 6 | 58 Bin Ton Radyasyonlu Çay Nereye Gitti? | 40 | ✗ | ✓ | ✓ | ~ | ✓ | Kapak B'nin vaadi |
| 7 | Çernobil Türkiye'ye Geldiğinde Ne Dediler? | 42 | ✗ | ✓ | ✓ | ✓ | ✓ | Belgesel başlığı |
| 8 | Korkacak Bir Şey Yok Dediler: Çernobil Çayı | 43 | ~ | ✓ | ✗ | ✗ | ✓ | Cevabı ele veriyor; kapı sonda |
| 9 | Çernobil'in Türkiye'deki Yüzü: 1986 Çayı | 40 | ✗ | ✓ | ✗ | ✓ | ✓ | Konu adı, soru değil |
| 10 | Çernobil Çayı Gerçekten Zararsız mıydı? | 39 | ✗ | ✓ | ✗ | ✓ | ✓ | Sağlık sorusunu vaat eder; video bunu cevaplamıyor (bilinmiyor) → yanlış vaat |
| 11 | Görmediğin Tehlikeye Kim Söylerse İnanırsın? | 44 | ✓ | ~ | ✓ | ✗ | ✗ | Kapı yok |
| 12 | Çernobil Çayı: Bardağa Mı, Depoya Mı Bakmalı? | 45 | ✓ | ✗ | ✗ | ✓ | ✗ | Cevabı veriyor, bağlamsız anlaşılmaz |

**Seçim: 1 (35 karakter).** Kalıp değişiyor: son dört video "Ad: soru?" idi (Gılgamış, Lale, Frankenstein, Narkissos); bu kez iki noktasız, ikinci tekil, "sen" vurgulu tek soru. Kapı kelimesi ilk sözcük. Video sağlık sorusunu cevaplamadığı için "zararsız mıydı?" (10) bilerek alınmadı: başlık izleyiciye cevabını vermeyeceğimiz bir şey vaat etmemeli. **Yedek:** 3.

## 3. Kapaklar (iki ayrı vaat)
- **A "BAKAN İÇTİ":** gazete baskısı üslubunda flaş patlamış bir basın masası; önde mikrofonlar, ortada yakın planda bir el ve tek renkli (amber) bir bardak çay. Yüz yok: bakan kadrajın dışında, yalnız eli ve kravatının ucu. Tek odak: bardağın parıltısı. Vaat: "bunu biliyorsun; arkası?" A01'de (ilk 5 sn) karşılanır.
- **B "58 BİN TON NEREYE?":** bir fabrika bahçesinde naylonla örtülü çuval yığını, alacakaranlık; tek renk yığının arasından görünen bir avuç bakır rengi çay. Vaat: "çaya ne oldu?" A02'de (0:10) açılır, IV. bölümde karşılanır.
- Kapak yazıları başlığın sözcüklerini (çernobil, çay, içer) tekrar etmez; A'daki "İÇTİ" başlığın "içer miydin"iyle bilerek kafiyeli (soru ↔ olgu). Hassasiyet: kravat ve el tek başına simge üretmesin (tam boy karede bakılır); radyasyon simgesi (yonca) kullanılmaz.

## 4. Üslup: 1986 gazete baskısı (başkanın seçimi)
**Neden:** yön "söz dönemin gazetesinden gelsin" diyor ve bu filmin bütün sözleri Milliyet'in 1986-1993 sayfalarından. Gazete yalnız kaynak değil, filmin malzemesi olsun: her kare 1986 gazete kâğıdına, kaba tram noktalarıyla, tek siyah mürekkeple basılmış gibi.
- **Görüntünün kuralı 1: radyasyon hiç çizilmez.** Parıltı yok, parçacık yok, yeşil ışık yok, uyarı simgesi yok. Görünmeyen görünmez kalır; ekrana yalnız **bir sayı** olarak gelir: dizgi harfleriyle basılmış "15.000 Bq/kg". Bulut yalnız haritada bir gölge, yağmur yalnız yağmur.
- **Görüntünün kuralı 2: renk yalnız çayda.** Bütün film siyah tram; tek ikinci baskı mürekkebi çayın kendisi. Yaprakta yeşil, fabrikada bakıra döner (oksitlenme: siyah çayın gerçek renk değişimi), bardakta kehribar dem. Gömülen çuvallarda renk toprağın altında söner. Sonda laboratuvar şişesinde ve izleyicinin bardağında yeniden yanar. Renk plakası 1980'lerin gazete renkli baskısı gibi siyahın üstüne 2-4 px kayık basılır.
- **Görüntünün kuralı 3: her söz bir kupürdür.** Biri konuştuğunda yüzü değil, sözünün basıldığı gazete sütunu görünür: başlık, tarih ve sayfa. Kişiler siluet, sırt, el; yaşamış siyasetçilerin yüzü çizilmez (karikatür yok, taraf yok).
- **Malzeme:** sararmış gazete kâğıdı (lif, hafif mürekkep yayılması), kaba tram (gazetenin 65 satır/inç ızgarası; 1080p'de ~7 px), sütun çizgileri, dizgi harfleri, ofset kaydırması; geçişlerde sayfa çevirme ve matbaa merdanesi (plaka kadrajı süpürerek basar).
- **Motor:** yeni ve küçük (`lib/baski.js`): Canvas 2D'de iki plaka (R = siyah yoğunluk, G = çay yoğunluğu, B = çayın tonu: 0 yeşil → 1 kehribar) → WebGL2 gölgelendirici "basar" (ekrana sabit tram ızgarası, plaka kaydırması, kâğıt dokusu). Tarifin akrabası cinecode `risograph` ve `halftone-dossier`; kod bizim. Hazır motorlarımızın hiçbiri tram baskı ya da plaka ayrımı yapmıyor.
- **Figür:** koyu siluet (kanal kuralı), 1986 Karadeniz'i: sırtında çay sepeti taşıyan toplayıcılar (yürüyüş `araclar/hareket/`), takım elbiseli siluetler yalnız sırttan ya da elden, işçiler, muhabirler.

## 5. İskelet: Harmon çemberi, kahraman bir çay yaprağı
**Seçim gerekçesi:** yön bir nesnenin yolculuğunu istiyor; Harmon'un sekiz adımı yaprağın yolunu kendiliğinden sıralıyor. Frankenstein iç içe çerçeve + Kishōtenketsu idi; Gılgamış ve Dorian Harmon'du, arada iki video var.
**Kahraman:** yaprak (B-G boyunca görüntüde izlenen tek renkli nesne). **Karşıt:** kişi değil, bardağın kendisi: "inanmak için bakılan şey". **Sıradan insanın gözü:** toplayıcılar (B10) ve sonda aynı yamacın köylüleri (E11-E13): sorunun kendisini onlar soruyor.

| Harmon | İçerik | Cümleler |
|---|---|---|
| Kanca | bardak (Aralık 1986) ↔ 56 bin ton (dört hafta sonra); soru | A01-A03 |
| 1 Rahat (sen) | Mayıs 1986, ilk sürgün, yaprak | B01-B02 |
| 2 İhtiyaç | Çernobil, bulut, Trakya'da önlem, 7 Mayıs yağmuru | B03-B07 |
| 3 Gidiş | ölçüm yapılıyor ama önlem yok; toplanıyor, fabrika, beş kiloya bir kilo | B08-B13 |
| 4 Arayış | Almanya'da ölçülüyor; sayı (bekerel, 600, 15.000) | C01-C04 |
| 5 Buluş | bardak: basın toplantısı, "zararsızdır", "on kişinin öleceğine inansaydık" | C05-C12 |
| 6 Bedel | bir hafta sonra yazı, dört hafta sonra depo; yirmi saatlik yüzleşme; yüzde 1,5 ↔ 65; ODTÜ'nün öğüdü; ölçülmeden satılan çay | D01-D13 |
| 7 Dönüş | depo: vadi, valiler, fırın, kırık seralar, çürüme, naylon, fabrika bahçeleri; "TAEK'in raporuna mı, kendi gözlerimize mi?"; 1993'te hâlâ yer yok | E01-E16 |
| (ara) | ölçülmeyen: iki kişinin ölçümü; bilimin cevabı yok | F01-F06 |
| 8 Değişim | zincir (kurum → bakan → cumhurbaşkanı → halk); 2007 oteli; çay laboratuvarda ölçenleri ölçüyor; bugünün çayında 39 Bq; izleyicinin bardağı | G01-G10 |

**Merak döngüleri (soru → cevap olay):**
1. **L1** "neye bakarak inanırsın?" (A03) → E13 (köylüler aynı soruyu soruyor) → G01-G02 (herkes bir öncekinin bardağına baktı) → G09 (üç soru, olaylardan) → G10 (izleyicinin bardağı).
2. **L2** "56 bin ton depoda" (A02, kapak B) → D02 → E01-E15 → E16 (son çuval bilinmiyor) → G03, G05.
3. **L3** "on kişinin öleceğine inansaydık tüm çayı imha ederdik" (C11-C12) → E08-E10 ("çay hâlâ zararsızdı ve toprağın altındaydı").
4. **L4** "paketin içinde ne olduğunu kim söyleyecek?" (C01) → C04 → D07 (iki sayı) → G05-G06 (laboratuvarlar ölçüyor).
5. **L5** bölüm başları: "Peki depodaki çay?" (E01), "Peki bardaklara giden çay?" (F01), "Herkes kime bakmıştı?" (G01).
- **Kapak A halkası:** A01 bardak ↔ G10 izleyicinin bardağı (aynı kompozisyon, el değişir).

**Bölüm kartları** (YouTube bölümleri; kancadan hemen sonra kart yok): kart yerine gazete künyesi gibi bir tarih bandı ("7 AY ÖNCE · MAYIS 1986"): bardaktan uzaklık sayılıyor. II. Bardak · III. Yirmi saat · IV. Depo · V. Ölçülmeyen · VI. Bugün.

## 6. Tempo kontrolü (rev0; `araclar/analiz/tempo_kontrol.py senaryo.json --yazar "Aral,Milliyet"`)
Art arda soyut dizi yok; ilk iki dakikada soyut aday yok; köprü adayı yok (A04 çıkarıldı, vaadi A03'ün kuyruğuna ve A02'ye girdi).
| id | bayrak | karar |
|---|---|---|
| A01, C05, C07, D01, E08 | Y | olay (gazetenin yazdığı, tarihli) |
| A03, C01, D06, E01, F01, G01 | T | olay vaadi; cevaplar aynı bölümde |
| C02 | M | soyut ama tek cümle; görüntüde sayaç (olay) ve C01-C04 arasında |
| C10, D03, D07, E09, F03 | M | olay (birinin sözü ya da ölçümü) |
| D08, D11, E10, G02, G07 | (yorum) | olaydan sonra tek yorum cümlesi |
| F05 | M | soyut; bilimin cevabı. F04-F06 bölümü kısa tutuldu (~40 sn) |
| D13, E03, E15 | A | ikinci yarıda yer adları azaltıldı (Hopa, Of, Ardeşen, Işıklı, Kırıkkale çıktı) |
| G09, G10 | T | iksir: olaylardan çıkan üç soru ve izleyicinin bardağı |

**Hikâye nerede bitiyor:** E16 ("son çuval"). F (ölçülmeyen, ~40 sn) ve G (~90 sn) yorum değil olay taşıyor (milletvekilinin ölçümü, 2007 oteli, laboratuvar testi); "hikâye bitince izleyici gider" riski G'nin olaylarıyla karşılanıyor.

## 7. Yönden kendi seçtiklerim (deney kaydı; `geriye_bakis.md`'ye taşınacak)
- **Üslup: 1986 gazete baskısı**, üç kural: radyasyon çizilmez yalnız sayı olarak görünür; renk yalnız çayda (yeşil → bakır → kehribar); her söz bir kupür.
- **Bardak zinciri:** bakan (A01, C07) → Çaykur genel müdürü (D02) → yüzleşmede "bol bol çay içildi" (D05) → eski cumhurbaşkanı (G01) → izleyici (G10).
- **"Mesafe" bir takvim:** bardaktan bir hafta (yazı), dört hafta (depo), iki yıl (fırın, kırık seralar), tam üç yıl (fabrika bahçeleri), yirmi bir yıl (otel), otuz yıl (laboratuvar).
- **Son: çay ölçenleri ölçüyor** (TAEK'in yeterlilik testi): yönde yoktu; arşiv dışından, TAEK yayınından.
- **Sorunun olayın içinde tekrar sorulması:** Of'taki köylülerin "TAEK'in raporuna mı, yoksa kendi gözlerimize mi inanalım?" sözü (M 31.3.1990).
- **Bırakılanlar:** Edirne'deki çamurun Çekmece'ye taşınması, Lipton depoları, çalıntı çay ve İstanbul'daki 181 ton (M 8.4.1988), radyasyonlu et ithalatı, Sovyet profesörün "Türkler hiç korkmadan çay içebilir" demeci (M 17.4.1987; dışarıdan bir bardak daha, ama yeni ad), ODTÜ raporundaki "ölü ve sakat doğum" iddiası ve TAEK'in cevabı (sağlık iddiası; bilimin bildiğinden fazlası), yakma sırasında işçilerin şikâyetleri (nedensellik kurulamaz), kişisel hastalık hikâyeleri (Can Dündar 2005 röportajı dahil), 1992-1993 Milliyet kampanyası ve sorumluların yargılanması tartışması (siyasi taraf).
