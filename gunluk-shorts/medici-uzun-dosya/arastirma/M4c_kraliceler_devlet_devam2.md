# M4c — Ek doğrulama turu: c10 "Rahip ve Kral" (1492–1498) ve c13 "İki Kraliçe" (1519–1642)

**Bölümler:** c10, c13 (köprü: c11 başı, c14 kapısı) · **Hazırlayan:** brif ajanı (M4/M4b/M5 boşluk turu) · **Tarih:** 18 Ekim 2026 · **Durum:** 45 WebSearch sorgusu; **hiçbir satıra ● verilmedi** (WebFetch DNS hatası; sayfa açılamadı). Dosya adındaki "devlet" (c12 devlet mekanizması) boşluğuna **girilmedi**; sorgu bütçesi c10 ve c13'e harcandı.

> Bu dosya senaryo değildir; M2/M4/M4b/M5 ile birlikte okunur. Biçim M4'ün biçimidir: kimlik, olgu, sınıf, kaynak (S-kodu), düzeltme/nüans, "eksik" listesi. **Kimlik şeması:** `A##` = c10 kronoloji satırı · `B##` = c13 kronoloji satırı · `C##` = canlı ayrıntı/anekdot · `§5.n` = mit/tartışma · `N##` = sayı · `D47…` = düzeltme (M5 `D46`'nın devamı) · `S##` = kaynak anahtarı (§9). Tırnak içindeki her İngilizce/İtalyanca/Fransızca parça **arama özetinin tırnak içinde verdiği biçimdir**; sayfa açılıp doğrulanmadı; **Türkçe çeviriler bize aittir.**

---

## 1. Başlık notu

### 1.1 Araçlar ne yaptı?

| Araç | Sonuç |
|---|---|
| **WebSearch** | **45 sorgu** (tamamı `standard`; `extended` kullanılmadı). 41'i `allowed_domains` ile (treccani.it, britannica.com, gutenberg.org, dokumen.pub, cambridge.org, academia.edu, archive.org, louvre.fr, chateauversailles.fr vb.), **4'ü filtresiz** (çatal, topuklu ayakkabı, parfüm, Catherine'in kuşatma anekdotu). Bütçe (≤45) tam kullanıldı; ret/hata yok. |
| **WebFetch** | **Kullanılmadı** (görev talimatı: DNS çalışmıyor; M2/M4/M4b/M5 hepsi `getaddrinfo ENOTFOUND` aldı). **● imkânsız.** |
| **Bash/Read** | Yalnız yerel dosya okuma ve hesap. Web'e Bash'ten çıkılmadı. |

**Sınıf politikası:** ● yok. **◐** = ≥2 bağımsız ikincil kaynakta (arama özeti dahil) uyumlu; aynı yayıncının farklı eserleri (Treccani DBI / Enciclopedia machiavelliana / EI) ayrı kaynak sayıldı ama not edildi; Wikipedia ve aynaları tek. **○** = tek ya da çelişkili. **ANEKDOT** = sonradan yazılmış/anlatılan, kim yazdı yazıldı. **HAFIZA** = araçla doğrulanmadı, metne girmez. Aynı kurumun (Louvre) birkaç sayfası bağımsız ikinci kaynak sayılmadı; kurumun **kendi beyanı** olarak ◐ zayıf.

**`allowed_domains` karnesi:** `britannica.com` çok verimli (Lorenzo, Savonarola, Catherine, Marie, Blois, Day of the Dupes). `treccani.it` verimli (Enc. machiavelliana Piero/Capponi/Firenze; DBI Lorenzo/Leoni/Del Nero/Leone X; EI Caterina). `gutenberg.org` verimli (Symonds, Reumont, Johnson, Gardner, Pardoe, Guizot, Thompson, Mariéjol, *Lives of the Early Medici*). `dokumen.pub` verimli (Weinstein *Savonarola*, Polizzotto *Elect Nation*, Piero monografisi, McIlvenna). `louvre.fr` / `collections.louvre.fr` **çok verimli** (Rubens döngüsü başlıkları, galeri düzeni, 2026 restorasyonu). `chateauversailles.fr` tek ama resmî (Aldatılanlar Günü). `cambridge.org` yalnız özet/bölüm başlığı. `ezrapoundcantos.org` ve `wikisource.org` bu konuda bir şey vermedi (wikisource: EB 1911 ve Catholic Encyclopedia sayfaları göründü). Filtresiz 4 sorgudan çatal ve topuklu için "kanıt yok" yönünde malzeme geldi; parfüm için yalnız turizm siteleri.

**Okuma uyarısı:** Arama özeti bir modelin birden çok sayfadan yaptığı derlemedir; **iç çelişkiler** var (örn. aynı özet Marie'nin Köln'e gelişini hem Ekim 1641 hem 12 Ekim 1642 verdi; Britannica'nın aynı konudaki ifadesi iki özette farklı geldi). Çelişkili günler olduğu gibi bırakıldı. Kritik her tarih/sayı için sayfa açılarak teyit gerekir.

### 1.2 Sınıf dağılımı (satırın ilk sınıfına göre)
c10 kronoloji (A) **35 satır**: ◐ 26 · ○ 8 · ANEKDOT/HAFIZA 1. c13 kronoloji (B) **30 satır**: ◐ 30 (B05 ANEKDOT; B15, B16, B30 kısmen ○/çelişkili/zayıf). Canlı ayrıntı (C) **25**. Mit/tartışma **19 girdi** (§5). Düzeltme/nüans **D47–D83** (37 madde).

### 1.3 En önemli bulgular (hızlı kullanım)
- **M2'nin "Poliziano'nun mektubu Savonarola'yı anmaz" notu büyük olasılıkla YANLIŞ (D48):** üç ayrı özet mektupta Savonarola'nın **bulunduğunu** söyler (günah çıkarma; kutsama konusunda üç ayrı aktarım); mektupta **olmayan** şey, Savonarolacı anlatılardaki **"üç şart / yüzünü duvara çevirdi"** sahnesidir. (Mektubun kendisi görülmedi.)
- **Lorenzo'nun son sözü Pico'ya (D49):** "kütüphanem bitene dek ölüm beni bağışlasaydı" — iki özette; 1494'te el konan kütüphaneyle Zweig'ci bağ.
- **9 Kasım 1494'te "çan" doğrulanamadı (D56):** özetteki çan sesi 1478 Pazzi bağlamındaki bir pasajdan olabilir; **kullanma.**
- **Kibirlerin Yakılması:** Britannica "sanat ve kitap yıkımı önemsizdi" der; Botticelli yakma hikâyesinin çağdaş kanıtı yok (D61).
- **Rubens'in "doğduğu ev" MİT (D69):** Rubens **Siegen**'de doğdu (28 Haziran 1577); Köln'deki Sternengasse evi çocukluk evidir; "doğduğu oda" efsanesi Wallraf'ın 1822 anma levhalarından çıkar.
- **Rubens döngüsü 24 = 21 sahne + 3 portre (D70)**, Louvre'un galeri düzenine göre (10+10 yan duvar, 3 portre giriş duvarı, 1 büyük uç duvar tablosu).
- **Marie'nin doğum yılı:** Louvre'un kendi tablo başlığı ve Britannica **1573** der (M4b: çoğu kaynak 1575) → yıl söylenmez (D68).
- **Louvre 24 Mart 2026'da döngünün 4 yıllık, yerinde restorasyonunu duyurdu; galeri halka kapalı (D71).**
- **Çatal, topuklu, parfüm** için Catherine bağı **kanıtsız**; dondurma/zehir ◐ mit; **Balet comique** gerçek (§5).

### 1.4 Düzeltme / nüans kutusu (M5 `D46`'nın devamı; numaralar D47'den)

**— c10 —**

- **D47 — Lorenzo'nun ölüm günü.** DBI (c. 73, 2009): *"La morte lo colse l'8 apr. 1492 nella villa di Careggi dove si era fatto portare nella speranza di trovarvi sollievo."* → "Ölüm onu 8 Nisan 1492'de, rahatlama umuduyla taşıttığı Careggi villasında yakaladı." Britannica **9 Nisan** der; üç özet "8 ya da 9". **8 Nisan (DBI) tercih; "Nisan 1492" yeter; gün söylenirse teyit.** DBI aynı yerde Pico ve Poliziano'nun orada olduğunu söyler. (A02) ◐
- **D48 — Poliziano mektubu ve Savonarola (M2 §4.8/K84 notunu DÜZELTİR).** Mektup **Iacopo Antiquari**'ye; tarih **18 Mayıs 1492** (bir akademik atıf, Poliziano *Letters* I, s. 230–248; ○ tek özet). Üç özet (Symonds, Gardner, bir üçüncü Gutenberg/dokumen özeti; Britannica da ziyareti anar) mektupta Savonarola'nın **bulunduğunu** söyler: Lorenzo günah çıkarmak için onu çağırır; **kutsama konusunda üç ayrı aktarım** (Symonds: günah çıkarmayı dinleyip kutsama vermeden ayrılır; Gardner: Lorenzo ayrılırken kutsama ister, birlikte ölüm duasını okurlar; bir başka özet: rahip günah çıkarmayı dinler ve kutsar) → **kutsama ayrıntısı söylenmez.** **"Üç şart" ve "duvara dönüş" mektupta yok**; yalnız Savonarolacı kaynaklarda (Burlamacchi, G. F. Pico, Razzi, Barsanti; ≈40 yıl sonra, olayı Savonarola'dan duyduklarını söylerler). Britannica ve Catholic Encyclopedia hikâyeyi şüpheli/geniş ölçüde reddedilmiş sayar. İngilizce çeviri: Janet Ross, *Lives of the Early Medici* (Gutenberg 74973, s. 336) — **metin bu turda görülmedi.** (C01–C03) ◐
- **D49 — Pico'ya söz.** Poliziano'nun mektubunda Lorenzo, Pico'ya, **kütüphanesi tamamlanana dek ölümün onu bağışlamasını dilediğini** söyler (iki özet; mektup metni görülmedi). Kütüphane 1494'te Signoria'ca alınıp San Marco'ya katılacaktır (M3:#35; c5). (C04) ◐
- **D50 — Hekim Pier Leoni.** DBI Leoni (F. Bacchelli, c. 64, 2005): 8 Nisan'da Lorenzo'nun başucunda; **ertesi gün San Gervasio'daki Malcantone villasının kuyusunda ölü bulundu**; kaynakçada L. Frati, *La morte di Lorenzo de' Medici e il suicidio di Pier L.* (intihar okuması). DBI Lorenzo (M5 K22): zehir söylentisi temelsiz. M2'nin "HAFIZA-D" satırı ○'ya yükseldi; **intihar/cinayet kesin kipte söylenmez.** (C05) ○
- **D51 — Duomo fenerine yıldırım (5 Nisan 1492).** İki ayrı aramada **bulunamadı** ("lightning/lantern kaynağı yok"). M2 K83 ANEKDOT/HAFIZA olarak kalır: **kullanma.**
- **D52 — Savonarola'nın 1482/1490/1491'i.** 1482'de San Marco'ya lector (ders veren) olarak gönderildi, "vaizlikte başta başarısızdı" (Britannica ◐; DBI özeti: Ferrara şivesi ve skolastik üslup, M5 K28 ○). 1490 dönüşü: bir sürüm "Pico'nun önerisiyle Lorenzo izin verdi", başka sürüm "Lorenzo'nun açık isteğiyle" (○ iki sürüm; M2 K80 ANEKDOT niteliği sürer). 1491'de prior (Britannica + Symonds ◐). (A05–A08)
- **D53 — Vaazların konusu.** "Kılıç, kırbaç, tufan" kehaneti (Symonds ◐), Nuh'un gemisi vaazları 1493–94 (Symonds ○), Genesis dizileri Büyük Perhiz 1492 ve 1494 (*Selected Writings* girişi ○ tek; "Floransa'ya özel rol" henüz yok), Vahiy vaazları (Cambridge). Charles'a **"yeni Cyrus"** denmesi bir kaynakta **1495** vaazı → 1494'e koyma. (C06) ◐/○
- **D54 — Piero'nun siyaseti.** Treccani Enc. machiavelliana: *"Educato dal Poliziano alle lettere, non ebbe invece attitudini politiche."* → "Poliziano'dan edebiyat eğitimi aldı, siyasi yeteneği olmadı." (**tek ansiklopedi yargısı: YORUM/○**). Aynı madde: Lorenzo ölünce şehir konseyleri varisliği *"senza proteste, ma anche senza dimostrazioni di sostegno da parte degli ottimati"* onayladı. Cambridge monografisi (2020): eleştirmenler Piero'yu babasının "İtalya'nın denge noktası" rolünü bırakmakla suçladı, oysa **sürdürmeye çalıştı**. DBI Orsini d'Aragona (Virginio): 1493'te kurulan Aziz Marko Ligi **Floransa ve Napoli'yi dışarıda bıraktı**, Piero'yu yalnızlaştırdı (◐ iki kaynak); 28 Mart 1494 Roma antlaşması (○ tek özet). **Ludovico Sforza'nın Charles'ı çağırması bu turda doğrulanamadı (HAFIZA).** "beceriksiz" kesin kipte söylenmez. (A09–A12) ◐/○
- **D55 — Sarzana.** Treccani: Piero Sarzana'da (26 Ekim) Sarzana, Sarzanello, Pietrasanta, Pisa ve Livorno'yu devretti; başka bir özet **30 Ekim** ve **dört** yer (Sarzana, Pietrasanta, Pisa, Livorno); süre "Napoli seferi boyunca" (Charles söz verdi: geri verilecek). Signoria'ya danışılmadı (Savonarola elçiliği özeti: "yetkisiz anlaşma"). Johnson: bu tavizler Floransalıları daha da öfkelendirdi; Pisa ayaklandı, kaleler geri verilmedi. Gün söylenmez; "ekim sonu". (A13) ◐
- **D56 — 9 Kasım 1494 (Pazar).** Landucci'nin 9 Kasım Pazar girdisi (ikinci el; Del Badia 1883 / Jervis çevirisi görülmedi); Cambi: *vespro* (akşam duası saati) ○; Johnson: Piero 8 Kasım'da döndü. "Signoria'dan **Luca Corsini** kapıyı Piero'nun yüzüne kapattı" (tek özet ○; M2'deki ad HAFIZA-D'ydi, şimdi bir özette daha). Cambridge monografisi: Piero silahlı adamlarıyla kamu sarayına girmeye çalıştı; Signoria **bir saat içinde huzura çıkmasını** emretti (kayıt 86v–87r, 9 Kasım); **20 Kasım'da isyancı ilan edildi** ◐. **"Popolo e libertà"** çağrısı Landucci'ye atfen (ikincil ◐). Piero **Bologna yoluna** çıktı (tek Gutenberg anlatısı ○), sonra **Venedik** (Johnson; M1/Commynes ◐). **San Gallo Kapısı** (Cambridge monografisi; Savonarola biyografisi ○). **Çan:** bir Savonarola biyografisindeki "saray çanı çalarken kalabalık içinden geçti" pasajı 1478 Pazzi bağlamında; **1494 için doğrulanamadı** → **kullanma** (M2 "Vacca çanı" HAFIZA'dır). (A14–A17) ◐/○
- **D57 — Kardinal Giovanni'nin kaçışı.** DBI Leone X: Piero'nun kovulmasından **birkaç gün sonra** *"travestito da frate francescano"* (Fransisken rahibi kılığında). Cambridge monografisi: Piero gibi San Gallo Kapısı'ndan; Giuliano kapıyı Paolo Orsini'nin atlılarıyla açık tuttu. Bir Savonarola biyografisi: Giovanni "sade bir rahip kılığında" Piero'yla çıktı. **Kılık ◐; zaman çelişir.** Britannica: Kasım 1494'te Medici ailesiyle "cumhuriyete ihanetle" sürgün; sonraki altı yıl kuzey Avrupa'yı dolaştı. (A18) ◐
- **D58 — Charles'ın girişi.** 17 Kasım ◐; "mızrak yatay, fatih gibi" ○ (tek özet; M2 HAFIZA-O); anlaşma **25 Kasım**, ayrılış **28 Kasım** (iki ayrı olgu, kaynaklar tek tek); **120.000 florin / altı ay / iki kraliyet temsilcisi ağırlama** ○ (tek özet; M2 HAFIZA-D). **Capponi:** Treccani Enc. machiavelliana ve ikinci kaynak: dört müzakereciden biri, şart taslağını kralın önünde yırttı ◐; "trompetlerinizi çalın, biz de çanlarımızı çalarız" **birçok kaynakta farklı lafızlarla** (ANEKDOT ◐ varlık, ○ lafız; M2 K94/§4.13). Nisan 1494'te Capponi ve Guidantonio Vespucci Fransa'ya gönderilip soğuk karşılandı (○). (A19–A22)
- **D59 — Savonarola'nın elçiliği.** Kasım 1494'te Charles'a giden Floransa heyetinin başındaydı/içindeydi; heyet **Pisa**'da kralı buldu; beş elçiden biri (bir kaynak); "5 Kasım gecesi yola çıktı" (bir kaynak — Piero'nun 9 Kasım'daki kovulmasından önce olduğu için **şüpheli**). Guicciardini derlemesi: Savonarola "görünüşe göre" kralı şehri yağmalamamaya ikna etti — **gelenek/○**. 19. yy anlatısı: Pisa'da krala "Rab'bin seçilmiş kabı" diye seslendi (○). (A23) ◐/○
- **D60 — Büyük Konsey.** Treccani Enc. machiavelliana ("Firenze"): **22–23 Aralık 1494** eski komünal konseylerin onayladığı yasa; Venedik modeli; Signoria'ya ya da kolleje bir kez adı çıkmış herkes üye olabilir (geniş uygunluk); Treccani (*Firenze alla fine del Quattrocento*): **üç binden fazla yurttaş**; Treccani Savonarola maddesi: yeni biçimin seçiminde **belirleyici pay** (◐ üç Treccani eseri + Oxford). "Üç bin" = **uygunluk**, fiilî üye sayısı değil. Parlamento (2 Aralık) ve balìa: yalnız parça (○). (A24–A25) ◐
- **D61 — Kibirlerin Yakılması (7 Şubat 1497).** Tarih 7 Şubat ◐ (bir kaynak 8 Şubat). İçerik: Nardi'nin listesi (bir bilimsel ciltte alıntılı): peruk, kadın saç süsü, ipek, kozmetik, parfüm, iskambil, zar, oyun masası, satranç tahtası, müzik aleti; **resim ve heykel de**. *Selected Writings* (Yale): "müstehcen resimler, aynalar, kozmetik, bebekler, parfümler, panolar, heykeller, aşk tanrıları". **Britannica:** kişisel süs eşyası, müstehcen resimler, kart ve oyun masaları; *"destruction of books and works of art was negligible"* (kitap ve sanat yıkımı **önemsizdi**). Botticelli: çağdaş kanıt yok ◐ (M3:#46–47 + Britannica: Vasari Botticelli'nin Savonarola yanlısı olduğunu yazar, yakma yazmaz; 1490'larda komisyon aldı; 1505'te lonca aidatını ödüyordu). **M3'ün "1498 sonrası tarihli eserleri var" ifadesi Britannica'yla örtüşmüyor** (Britannica: sonraki komisyon yok, son Dante çizimleri tereddütlü; sağlık sorunu olası) → "1498'den sonra da resim yaptı" **kesin söylenmez.** Fra Bartolomeo/Lorenzo di Credi'nin yakması **doğrulanamadı**; "Venedikli tüccar 20.000 scudo" **bulunamadı** (M2 ANEKDOT). 'Fanciulli' gezileri ◐ (bir kaynak: 1497'den itibaren evleri dolaşan gençler). (A26–A28) ◐
- **D62 — Aforoz.** Boğa **13 Mayıs 1497**; Floransa'da resmen ilan **18 Haziran** (bir kaynak: kurye gecikti); Britannica "Haziran 1497"; Treccani 12 Mayıs ↔ EdP 13 Mayıs (M5 D40). **"1497'de aforoz edildi" yeter.** (A29) ○
- **D63 — Medici komplosu 1497.** Bernardo del Nero Mart 1497'de Adalet Gonfalonieri seçilince Piero'nun en ciddi dönüş girişimi tetiklendi; **Lamberto dell'Antella 5 Ağustos'ta tutuklandı**, itirafı **beş** Medici yanlısının idamına yol açtı (Del Nero, Giovanni Cambi, Giannozzo Pucci, Niccolò Ridolfi, Lorenzo Tornabuoni) ◐. Gün: **21 Ağustos** (Enc. machiavelliana) ↔ **23 Ağustos gecesi** (DBI Del Nero). Johnson: mahkûmlara **Büyük Konsey'e başvuru hakkı verilmedi** (yeni anayasaya aykırı); bir Savonarola çalışması: Francesco Valori idamları isteyip müdahale etmedi; Treccani: Savonarola savunduğu yasanın çiğnenmesini **önlemedi**, Medici yanlılarının kalan desteğini yitirdi ◐. **İki ayrı Giovanni Cambi** (idam edilen ↔ 9 Kasım 1494 girdisini yazan günlükçü): karıştırma. (A30–A31)
- **D64 — Ateş sınavı ve son.** **7 Nisan 1498** için ateş sınavı kuruldu (Fransisken Francesco da Puglia ↔ Savonarola'nın yerine Domenico da Pescia); sınav **hiç yapılmadı**; Savonarola "kararname gereği galip" ama mucize göstermemekle suçlandı (Britannica ◐). **Ertesi gün** Arrabbiati'nin kışkırttığı kalabalık San Marco'yu bastı; Savonarola, Domenico ve bir arkadaşı tutuklandı (Britannica ◐; **Palm Pazarı = 8 Nisan 1498** bizim hesap, M2). 20–22 Mayıs sorgu ve işkence ◐ (M5 K30). **23 Mayıs 1498** Signoria Meydanı'nda asıldılar, yakıldılar; külleri Arno'ya atıldı, "yadigâr olmasın diye" (Britannica ◐; M5 K29 üç DBI); bir özet, Landucci'nin girdisi dahil, **22 Mayıs** tarihini kullanır → teyit. (A32–A34)
- **D65 — Savonarola'nın 1475'i ve kırmızı şapka.** Britannica: **24 Nisan 1475**'te babasının evini ve tıp öğrenimini bırakıp Bologna'da Dominiken tarikatına girdi ◐; yürüyerek (M5/DBI özeti; bir kitap özeti "yirmi beş mil" der — dokumen.pub'daki *Inventing the Renaissance* olabilir, özetten kesin değil). **Baba mektubu / *De ruina mundi* bu turda bulunamadı** (kullanma). **Kırmızı şapka:** Britannica, Papa'nın kardinal şapkası önerdiğini ve cevabını kaydeder; ikinci kaynak sözü **vaazda** söylenmiş gösterir ve teklifin "yalnız ima edildiğini, doğrulanmadığını" der → **ANEKDOT ○**, tırnaksız, "aktarılır". (C07–C08)
- **D66 — Michelangelo 1492–95.** Kar heykeli: Vasari (tarihsiz) ve Symonds (20 Ocak 1494 yoğun kar) ◐ ANEKDOT; Condivi bu turda görülmedi. Floransa'dan ayrılış: Vasari "Medici sürülmeden birkaç hafta önce"; Rolland kronolojisi "Ekim"; Strutt "1494 başı" → "1494 sonbaharı" ○; 1495'te döndü (Symonds). Santo Spirito'ya tahta haç (1492–): Britannica 1960'larda bulunan haçı **bazı** uzmanların ona atfettiğini söyler → atıf tartışmalı. (C09)
- **D67 — Charles'ın İtalya'ya girişi.** Britannica: 1494'te **borçla toplanmış** büyük orduyla karşı konulmadan geçti; bir diplomat hesabına göre 9 Eylül (akademik atıf); bir JSTOR kitap tanıtımı: Rapallo, Mordano, Fivizzano otuz bin kişilik Fransız süvari ve İsviçreli ordusunca yağmalandı (○). **Andreas Palaiologos devri ve haçlı hedefi bu turda doğrulanamadı (HAFIZA).** (A10) ◐

**— c13 —**

- **D68 — Marie'nin doğum yılı.** **Louvre'un kendi tablo başlığı** *"La Naissance de la reine, à Florence le 26 avril 1573"* ve portre başlığı *"Portrait de Marie de Médicis (1573-1642)"* + Britannica **1573**; Wikipedia ve çoğu biyografi **1575** (M4b D20). **Yıl söylenmez**; 26 Nisan günü Louvre başlığında da geçer. (B16) ◐ çelişkili
- **D69 — "Rubens'in doğduğu evde ölüm" MİT.** Britannica: Rubens **28 Haziran 1577, Siegen** (Vestfalya). Marie 3 Temmuz 1642'de Köln'de öldü (Britannica, Osborne ◐); ev **Sternengasse 10** (dokumen.pub Köln kaynağı; M4b b48: Wikipedia/EBSCO); bu "Rubenshaus" Rubens ailesinin yıllarca oturduğu evdir (Rubens gençliğini orada geçirdi; M4b D13 doğru). *"Marie Rubens'in doğduğu odada öldü"* efsanesi **Wallraf'ın 1822'de tasarladığı iki anma levhasından** gelir ("Köln için gurur verici bir yanlış"); **1987 levhası** Siegen'i düzeltir ama Marie'nin ölüm yılını **1643** yazar; ev **1942'de yıkıldı**; son özel sahibi Gustav von Mevissen 1890'da şehre bağışladı (**tek makale ○**; hangi dokumen.pub cildi olduğu özetten kesin değil: *Köln in unheiligen Zeiten* ya da *Lexikon der Kölner Architekten*). Marie'nin Köln'e gelişi: **Ekim 1641** ↔ "12 Ekim 1642" (aynı kaynakta iç çelişki; ikincisi ölümden sonra olduğu için dizgi hatası olasılığı) ○. (B28) ◐/○
- **D70 — Rubens döngüsü: 24 = 21 + 3.** Louvre (*To the glory of a queen of France* sayfası): galeri **girişten okunur; her uzun duvarda on tablo, giriş duvarında üç portre, uç duvarda bir büyük tablo** → 10+10+1 = **21 anlatı tablosu + 3 portre = 24**. Kullanıcı notundaki "21 tablo" bir yanlış okuma. **Sipariş 1622** (Louvre); üretim **1622–25**; Rubens'in aldığı **en büyük sipariş**; sipariş sahibi Marie, eser mirasla Gaston d'Orléans'a geçti (Louvre koleksiyon kaydı); Louvre'a 1816, "Galerie Médicis" 1993 (M4b b44 ◐). 26 Şubat 1622 sözleşme (M4b b43 ◐). (B25) ◐
- **D71 — Louvre restorasyonu (2026).** Louvre, **24 Mart 2026**'da 24 tablonun restorasyonunu duyurdu: **in situ**, Galerie Médicis'te, galeri **halka kapalı**, **dört yıl**, yaklaşık **293 m²** boyalı yüzey, Société des Amis du Louvre **4 milyon €**; ihale haziran 2026'da iki restoratör grubuna; işlemlerin **Ekim 2026'da** başlaması bekleniyor; ziyaret sayfası başlığı *"Temporarily closed"*. Kurumun kendi beyanı (üç Louvre sayfası): ◐ zayıf. **Yayın tarihinde durum değişmiş olabilir → yayın öncesi teyit.** (B30)
- **D72 — Marie 1599–1600.** Gutenberg (*Marie de Medicis*): sözleşme **Mayıs 1599**, Palazzo Pitti, çeyiz **600.000 taç**; Britannica: Henri IV, **borçlarını ödemeye yarayacak büyük çeyiz** için evlendi (Margaret'ten boşandıktan sonra); M4b b41: çeyiz Fransa'nın Ferdinando I'e olan borcundan **düşülür** (herodote.net, sept.info, Britannica ◐). Guizot: elçi Brulart de Sillery Floransa'da evliliği yürütme yetkisi aldı. **"Henri IV 'şişman bankacı kızı' dedi" aranmadı** (kullanma). (B17–B18) ◐
- **D73 — Catherine'in "naipliği".** Guizot: Francis II 5 Aralık 1560'ta ölünce Catherine **IX. Charles'ın vasiliğini ve işlerin idaresini** elde etti, Genel Meclis ona "naip" unvanını vermedi; Antoine de Bourbon "tümgeneral" (lieutenant general) oldu (Guizot + Thompson ◐). M4 #75 ("1560–1563 naip") → "fiilen yönetti". (B09)
- **D74 — Hoşgörü politikası.** Britannica: Catherine Francis I/Henri II'nin baskı siyasetini bıraktı, uzlaşma aradı; Şansölye Michel de L'Hôpital destekledi; **Poissy görüşmesi (1561) başarısız**; **Ocak 1562 fermanı**: Hugenotlara surların dışında, silahsız, ilk kez açık ibadet; Britannica "belki Catherine'in en somut başarısı"; başka görüş: ferman iç savaşı **olasılaştırdı** (◐ iki yorum). Bir kaynak Ocak 1561 fermanı (tutukluları serbest bırakma) ayrıca anar → erken ölçüler tarih farkı gösterir. (B10) ◐
- **D75 — 1572 sorumluluk ve sayı.** Britannica: Catherine Coligny'nin ve başlıca yandaşlarının öldürülmesini **onayladı**, ardından gelen katliamı **büyük olasılıkla onaylamadı**; "kötü İtalyan kraliçe" efsanesi 1572'den biçimlendi; **yalnız Paris'te tahminen ≈3.000 ölü**. Mariéjol: "kendi tuzağına düştü" tezi; Janine Garrisson: önce Catherine'i sorumlu görüp sonra yorumunu değiştirdi (bir özet). **M4'ün HAFIZA ülke geneli (10.000–30.000) aralığı hâlâ HAFIZA.** (B11) ◐
- **D76 — "Siyah efsane" kökeni (M4 §5.14'ü düzeltir/doğrular).** *Discours merveilleux de la vie, actions & deportemens de Catherine de Medicis, royne mere…* — Internet Archive kaydı yazarı **Henri Estienne (1531–1598)** gösterir, eser ayrıca **Théodore de Bèze** ya da **Jean de Serre**'e atfedilmiştir; **Paris, 1575, anonim**; bir kitap "1574" der; EB 1911: Estienne "kuşkusuz iş birliği yaptı"; **1576 İngilizce çeviri**; ◐. McIlvenna (Routledge 2016): saldırıların kökü **parlamenter/hukukçu erkek elit**; en eski saldırılardan biri **1573 Huguenot polemik broşürü içindeki şiir**; zehir ve ensest suçlamaları "kadın karalamasının edebî kalıpları"; efsane 19. yy'da **Michelet**'de zirve yapar. **Gentillet *Anti-Machiavel* (1576) bu turda doğrulanmadı (HAFIZA).** (B12) ◐
- **D77 — Mitler (M4b bM9'a ek).** **Çatal:** M. F. K. Fisher *The Art of Eating* (1954) 1533'ü "dönüm noktası" yapar; bir özet, Bizanslı prenses Theodora Anna Doukaina'nın 1071'de Venedik'e çatalla geldiğini söyler (anekdot, tek özet ○); İtalya'da çatal 16. yy'da yaygınlaştı, Fransa'da yavaş (satirik yazarlar direnç gösterir); Henri III'ün çatalı alay konusu (blog ○); Coryat'ın *Crudities*'i 1611'de basıldı (gezi 1608) → **Catherine'in getirdiğine kaynaklı bağ yok** (◐ National Geographic + California Academy of Sciences + The Florentine; sayfa metni görülmedi). **Topuk:** "1533 evliliği ilk topuklu örneği" popüler iddia; Bata Shoe Museum küratörü Elizabeth Semmelhack aktarımı: topuk yüzyıllarca Yakın Doğu'da **binicilik ayakkabısı** (üzengide ayakta durmak); Catherine = "moda taşıyıcı" iddiası kaynaksız (○; üç ikinci el site, Bata sayfası görülmedi). **Parfüm:** Grasse'ın kokulu eldiven hikâyesi (Jean de Galimard, Catherine'e hediye) turizm anlatısı, Wikipedia'da "citation needed"; "kişisel parfümcüsünü getirdi" efsane; René Bianchi gerçek saray parfümcüsü (M4b b37 ○) ama "Fransa parfümcülüğünü başlattı" kanıtsız. **Dondurma/zehir:** M4b ◐ mit (yeniden aranmadı). (§5.8–5.12) ◐/○
- **D78 — Catherine'in ölümü.** Britannica: 5 Ocak 1589, Blois ◐. Britannica *Blois*: Henri III **Guise'i 23 Aralık 1588'de şatonun ikinci katında** öldürttü, kardinal ertesi gün; bir kaynak: kraliçe anne "birkaç gün sonra tam altındaki odada" öldü. Bir Fransızca biyografi: 4–5 Ocak gecesi ani yüksek ateş; **Venedik elçisi raporu plörezi** der; Henri II ve Charles IX'un aksine **yazılı bir tıbbi rapor yok**; saat kaynaklarda çelişir. (B14–B15) ◐
- **D79 — Çocuksuz on yıl.** Britannica: Henri'nin Diane de Poitiers'ye bağlılığı sürerken Catherine "10 endişeli yıl"dan sonra on çocuk doğurdu ◐. Fernel'in müdahalesi, Henri'nin hipospadyası = modern/erken 20. yy yorumları ○ (cinsel/tıbbi ayrıntı; **videoya girmez**). Bir tıp-tarihi sitesinin "gebe hayvan idrarı, yaban domuzu organı tozu" kayıtları ○ **kullanma**. İlk çocuğun doğum günü (19 Ocak 1544) bu turda görülmedi (HAFIZA). (B07) ◐
- **D80 — 1559 kazası ve siyah yas.** Britannica: Henri II **10 Temmuz 1559**'da öldü, turnuvada Montgomery'nin mızrağı başına isabet etmişti (10 gün önce); turnuva tarihi **29 Haziran** (Guizot) ↔ **30 Haziran** (Thompson) → "Haziran sonu". Guizot: Montgomery kırık mızrak parçasını bırakmadı; kıymık gözüne girdi. "Catherine 1559'dan beri hep siyah" bir çalışmada (○). **Kırık mızrak amblemi bulunamadı** (M4 3.D #7 HAFIZA). (B08)
- **D81 — Aldatılanlar Günü.** Versailles resmî sayfası: kriz **10 Kasım'da Luxembourg Sarayı'nda başladı, 11 Kasım'da Louis XIII'ün küçük Versailles sarayında bitti**; Britannica 10 Kasım; başka sayfa 10–12 ◐. Ad: Guillaume Bautru (Serrant Kontu) arabayı görünce söylemiş (tek, ANEKDOT ○). Şansölye Michel de Marillac'ın idamı ayrı olay (○). Marie **Şubat 1631'de Compiègne'e**, **Temmuz 1631'de Brüksel'e** kaçtı ve bir daha dönmedi (Versailles + Osborne ◐). (B26–B27)
- **D82 — Richelieu ve Louis XIII'ün ölümü.** "Marie'den beş ay sonra Richelieu öldü" (4 Aralık 1642) bu turda **doğrulanamadı** (bir kaynak yalnız "Louis XIII'ten kısa süre önce" der) → HAFIZA; kullanılacaksa teyit.
- **D83 — Clemens VII ve Catherine'in akrabalığı.** Britannica Catherine'in evliliğini "amcası Papa VII. Clemens" kıydı diye verir. Giulio (Clemens), Giuliano'nun doğal oğlu (M5 P12); Catherine'in babası Lorenzo di Piero, Piero II'nin oğlu (Treccani EI: babaanne Alfonsina Orsini). Giulio ile Piero II ilk kuzen → Clemens Catherine'e **uzak akraba**dır; "amca" gevşek bir kullanım. Video: "Medici papası VII. Clemens". (B06) ◐

---

## 2. Kronoloji tablosu

> Okuma: **Kaynak** sütunu §9'daki S-kodlarıdır; içerikleri **açılıp okunmadı**, yalnız arama özeti. Gün–hafta hesapları bizim hesabımızdır. "—" = bu turda bulunamadı.

### 2.A c10 — Rahip ve Kral (1475–1503)

| # | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|
| A01 | 5 Nisan 1492 | Duomo fenerine yıldırım (kötü alâmet) | ANEKDOT/HAFIZA | — | İki aramada bulunamadı (D51) |
| A02 | **8 Nisan 1492** | **Lorenzo Careggi villasında ölür** (43 yaş 3 ay, M5); rahatlama umuduyla taşınmıştı; Pico ve Poliziano orada | ◐ | S13, S01 | Britannica 9 Nisan (D47) |
| A03 | 8–9 Nisan 1492 | Hekim Pier Leoni ertesi gün kuyuda ölü bulunur | ○ | S14 | D50 |
| A04 | 18 Mayıs 1492 | Poliziano'nun Iacopo Antiquari'ye ölüm mektubu (Savonarola burada anılır; "üç şart" yok) | ○ (tarih) / ◐ (içerik özeti) | S02, S04, S28 | D48 |
| A05 | 24 Nisan 1475 | Savonarola Bologna'da Dominiken tarikatına girer | ◐ | S05, M5 | D65 |
| A06 | 1482 | Savonarola San Marco'ya lector olarak gelir; vaizlikte başta başarısız | ◐ | S05 | D52 |
| A07 | 1490 | Floransa'ya dönüş (Pico önerisi / Lorenzo isteği) | ○ | S05, S08 | D52 |
| A08 | 1491 | San Marco prioru | ◐ | S05, S04 | |
| A09 | 1492 | Piero babasının yerine geçer; konseyler "itirazsız ama destek gösterisi olmadan" onaylar | ◐ | S09 | D54 |
| A10 | Eylül 1494 | Charles VIII borçla toplanmış orduyla İtalya'ya girer (diplomat hesabı: 9 Eylül) | ◐ | S24 | D67 |
| A11 | 1493 | Aziz Marko Ligi: Floransa ve Napoli dışarıda | ◐ | S30, S17 | D54 |
| A12 | 28 Mart 1494 | Papa–Napoli antlaşması Roma'da (denge değişir) | ○ | S30 | |
| A13 | 26 ↔ 30 Ekim 1494 | Piero Sarzana'da kaleleri devreder (Sarzana, Pietrasanta, Pisa, Livorno…) | ◐ | S09, S18 | D55 |
| A14 | 8 ↔ 9 Kasım 1494 | Piero Floransa'ya döner | ◐ | S18, S09 | D56 |
| A15 | **9 Kasım 1494 (Pazar)** | Piero kamu sarayına silahlı adamlarla girmek ister; Corsini kapıyı kapatır; "bir saat içinde huzura çık" emri; "Popolo e libertà"; Piero Bologna yoluna çıkar | ◐ / ○ (Corsini) | S17, S19, S09, S29 | D56 |
| A16 | 9 Kasım 1494 | Cambi günlüğü: Piero "vespro"da halk tarafından kovuldu | ○ | S19 | |
| A17 | 20 Kasım 1494 | Piero emre uymadığı için isyancı ilan edilir | ◐ | S17 | |
| A18 | Kasım 1494 | Kardinal Giovanni Fransisken kılığında kaçar | ◐ | S16, S17 | D57 |
| A19 | 17 Kasım 1494 | Charles Floransa'ya girer ("mızrak yatay" ○) | ◐ / ○ | S10, S04 | D58 |
| A20 | Kasım 1494 | Capponi şart taslağını yırtar; "trompet/çan" sözü ANEKDOT | ◐ / ANEKDOT | S10 | D58 |
| A21 | 25 ↔ 28 Kasım 1494 | Anlaşma ≈120.000 florin / Charles Floransa'dan ayrılır | ○ | S10, S31 | D58 |
| A22 | Nisan 1494 | Capponi ve Vespucci Fransa'ya gönderilir, soğuk karşılanır | ○ | S10 | |
| A23 | Kasım 1494 | Savonarola heyetiyle Pisa'da Charles'tadır | ◐ | S04, S31, S22 | D59 |
| A24 | 22–23 Aralık 1494 | Büyük Konsey yasası (Venedik modeli, geniş uygunluk) | ◐ | S11 | D60 |
| A25 | Aralık 1494 | Savonarola'nın yeni biçimin seçiminde belirleyici payı | ◐ | S11, S12 | |
| A26 | **7 Şubat 1497** | Kibirlerin Yakılması (Karnaval) | ◐ | S05, S26 | D61 (8 Şubat bir kaynak) |
| A27 | 1497 | Gençler evleri dolaşıp eşya toplar ("fanciulli") | ◐ | S26 | |
| A28 | 1497→ | Botticelli yakma iddiası: çağdaş kanıt yok | ◐ | S25, M3 | D61 |
| A29 | 13 Mayıs 1497 | Aforoz boğası (Floransa'da ilanı 18 Haziran: ○) | ○ | S05, M5 D40 | D62 |
| A30 | Mart–5 Ağustos 1497 | Del Nero seçilir; dell'Antella tutuklanır | ◐ | S15 | D63 |
| A31 | 21 ↔ 23 Ağustos 1497 | Beş Medici yanlısı idam edilir; temyiz hakkı tanınmaz | ◐ | S15, S09, S18 | D63 |
| A32 | 7 Nisan 1498 | Ateş sınavı planlanır, yapılmaz | ◐ | S05 | D64 |
| A33 | 8 Nisan 1498 | San Marco baskını, Savonarola tutuklanır | ◐ | S05 | Palm Pazarı: hesap |
| A34 | 20–22 / **23 Mayıs 1498** | Sorgu–işkence; asılıp yakılma; küller Ponte Vecchio'dan Arno'ya | ◐ | S05, M5 | 22 Mayıs bir özette |
| A35 | 28 Aralık 1503 | Piero Garigliano'da boğulur (M5 teyit) | ◐ | M5 | |

### 2.B c13 — İki Kraliçe (1519–1642)

| # | Tarih | Olgu | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|
| B01 | 13 Nisan 1519 | Caterina Floransa'da doğar | ◐ | S33, S35, S34 | |
| B02 | 28 Nisan 1519 | Annesi Madeleine de La Tour d'Auvergne ölür (on beş gün; ateş: bir akademik PDF) | ◐ | S35, S34 | |
| B03 | 4 Mayıs 1519 | Babası Lorenzo di Piero (Urbino Dükü) ölür | ◐ | S34, S33 | |
| B04 | 1519 → | Babaanne Alfonsina Orsini vasi (EI) | ◐ | S34 | M5: Alfonsina 7 Şub 1520'de ölür |
| B05 | 24 Eki 1529–10 Ağu 1530 | Floransa kuşatması; Catherine Murate'de; "surlara çıkarılsın" sesleri | ◐ ANEKDOT | S46 | İlk kaynak yok (C16) |
| B06 | 28 Ekim 1533 (27 Ekim: başka) | Marsilya'da Henri ile evlilik, VII. Clemens kıydı; çeyiz ≈100.000 duka/écu + mücevher | ◐ | S33, S35, M4 | 14 yaş: hesap |
| B07 | 1533→ | On çocuksuz yıl; Henri Diane'a bağlı; sonra on çocuk | ◐ | S33, S37 | D79 |
| B08 | 29/30 Haziran → **10 Temmuz 1559** | Henri II turnuvada yaralanır, ölür | ◐ | S36 | D80 |
| B09 | 5 Aralık 1560 → | Francis II ölür; Catherine IX. Charles'ın vasisi (naip unvanı verilmedi) | ◐ | S36 | D73 |
| B10 | 1561–Ocak 1562 | Poissy; hoşgörü fermanı | ◐ | S44 | D74 |
| B11 | 22–24 Ağustos 1572 | Coligny suikast girişimi; konsey; katliam; Paris'te ≈3.000 (tahmin) | ◐ | S33, S40, M4b | D75 |
| B12 | 1573 / 1575 / 1576 | Huguenot şiiri; anonim *Discours merveilleux*; İngilizce çeviri | ◐ | S38, S39 | D76 |
| B13 | 15 Ekim 1581 | *Balet comique de la reine* | ◐ | M4b b38 | |
| B14 | 23–24 Aralık 1588 | Guise ve kardinal Blois'da öldürülür | ◐ | S41 | |
| B15 | 4–5 Ocak 1589 | Ateş; Catherine ölür (plörezi: Venedik elçisi) | ◐ / ○ | S33, S41 | D78 |
| B16 | 26 Nisan 1573 ↔ 1575 | Marie doğar | ◐ çelişkili | S50, S47 | D68 |
| B17 | Mayıs 1599 | Evlilik sözleşmesi Pitti'de; çeyiz 600.000 taç | ◐ | S47 | D72 |
| B18 | 5 Ekim 1600 / 3 Kasım 1600 | Floransa'da vekâlet / Marsilya'ya iniş (Louvre başlığı) | ◐ | M4b b40, S50 | |
| B19 | 13 Mayıs 1610 | Saint-Denis'de taç (Louvre başlığı + Pardoe) | ◐ | S50, S47 | |
| B20 | 14 Mayıs 1610 | Henri IV öldürülür; Parlement Marie'yi naip ilan eder | ◐ | S47, S50 | |
| B21 | 1617 | Concini öldürülür (gün 24 Nisan HAFIZA) | ◐ yıl | S47 | |
| B22 | 1617–19 | Marie Blois'da gözetim altında | ◐ | S47 | |
| B23 | 21–22 Şubat 1619 | Blois'dan gece kaçış (Louvre başlığı; başka kaynak 23 Şubat) | ◐ | S50, S47 | |
| B24 | 1621 | Anne–oğul barışı | ◐ | S51 | |
| B25 | 1622–1625 | Rubens döngüsü: sipariş 1622, 24 tablo (21+3), 1625'te Luxembourg | ◐ | S51, S50, M4b | D70 |
| B26 | 10–11 Kasım 1630 | Aldatılanlar Günü | ◐ | S49 | D81 |
| B27 | Şubat–Temmuz 1631 | Compiègne; Brüksel'e kaçış; 1638–41 İngiltere | ◐ | S49, S48 | |
| B28 | 3 Temmuz 1642 | Marie Köln'de, Sternengasse 10'da yoksul ölür | ◐ | S47, S48, S53 | D69 |
| B29 | 1816 / 1993 | Louvre'a taşınma / Galerie Médicis | ◐ | M4b b44 | |
| B30 | 24 Mart 2026 → Ekim 2026 | Louvre restorasyon duyurusu; çalışma başlangıcı; galeri kapalı | ◐ zayıf | S51 | D71 |

---

## 3. Canlı ayrıntılar (C) — kim yazdı, güvenilirlik

| # | Ayrıntı | Kim yazdı / ne zaman | Sınıf | Birebir parça (arama özeti; çeviri bize ait) |
|---|---|---|---|---|
| C01 | **Poliziano'nun mektubu:** Lorenzo ölüm ayında Careggi'de sakramentleri alır; gece yarısına doğru kutsal ekmeği getiren rahibi sıcak karşılar; Pico oradadır | Poliziano → Antiquari, 1492; aktaran Reumont, Symonds, Gardner (19. yy), *Lives of the Early Medici* (1910) | ◐ özet | — (çevirisi Gutenberg 74973'te; metin görülmedi) |
| C02 | **Savonarola, Poliziano'nun sürümünde:** Lorenzo sakramentten sonra rahibi çağırır; rahip öğütler, günah çıkarmayı dinler; **kutsama ayrıntısı üç ayrı aktarımda üç ayrı** | Poliziano'nun mektubu; Symonds, Gardner ve bir üçüncü özet | ◐ | EN (Symonds özeti): *"Savonarola confessed Lorenzo and retired without volunteering the blessing"* ↔ Gardner: Lorenzo ayrılırken kutsama ister, birlikte dua okurlar ↔ üçüncü özet: günah çıkarmayı dinleyip kutsadı |
| C03 | **Savonarolacı sürüm:** üç şart (canlı iman; haksız kazancı iade; Floransa'ya özgürlük); Lorenzo ilk ikisini kabul eder, üçüncüde yüzünü duvara çevirir | Burlamacchi, G. F. Pico, Razzi, Barsanti (hepsi Savonarola partisi; ≈1530; Razzi: görüşme tanıksız; Pico ve Burlamacchi olayı **Savonarola'dan duyduklarını** söyler); bir uzman: hikâye Silvestro Maruffi'nin hayal gücünden doğmuş görünür; bir başkası: Burlamacchi/Pico metinleri San Marco'da uydurulmuş olabilir (şüphe kitapların özgünlüğüne dair) | ANEKDOT ◐ | EN (Symonds özeti): *"Three things are required of you: to have a full and lively faith in God's mercy; to restore what you have unjustly gained; to give back liberty to Florence."* → TR: "Senden üç şey isteniyor: Tanrı'nın merhametine canlı bir iman; haksız kazandığını iade etmek; Floransa'ya özgürlüğünü geri vermek." (**birebir söylenmez**) |
| C04 | **Lorenzo'nun Pico'ya sözü:** kütüphanesi tamamlanana dek ölümün onu esirgemesini dilemiş | Poliziano mektubundan, iki modern özet | ◐ | — (özet; mektup metni görülmedi) |
| C05 | **Pier Leoni'nin kuyusu** | DBI Leoni (Bacchelli 2005) | ○ | IT (özet): *"Il giorno dopo fu trovato morto in un pozzo della villa di Malcantone a San Gervasio presso Careggi."* |
| C06 | **Vaazlar:** "bir kılıç, bir kırbaç, bir tufan" | Symonds (19. yy); Cambridge (*Apocalypse without God*) | ◐ | — |
| C07 | **1475'te yürüyerek Bologna'ya** | DBI (M5); 2025 tarihli bir kitap ("yirmi beş mil") | ◐ | EN (özet): *"twenty-two-year-old Savonarola walked twenty-five miles to Bologna"* |
| C08 | **Kardinal şapkası:** *"A red hat? I want a hat of blood."* | Britannica (kaydeder); başka kaynak: vaazda söylenmiş, teklif doğrulanmamış | ANEKDOT ○ | EN (Britannica özeti): "Kırmızı şapka mı? Ben kandan bir şapka isterim." → **tırnaksız aktarılır** |
| C09 | **Kar heykeli:** Piero Michelangelo'ya avluda kardan heykel yaptırır | Vasari (tarihsiz), Symonds (20 Ocak 1494) | ANEKDOT ◐ | — |
| C10 | **Piero hakkında Treccani** | Enc. machiavelliana | ○ yargı | IT: *"non ebbe invece attitudini politiche."* |
| C11 | **9 Kasım'ın tanıkları:** Landucci (Pazar 9 Kasım; "halk ve özgürlük"), Cambi (*vespro*) | Luca Landucci (günlük, çağdaş); Giovanni di Neri Cambi (günlükçü) — **metinleri görülmedi, ikincil aktarım** | ◐ | — |
| C12 | **Kibirler listesi** | Jacopo Nardi *Istorie* (16. yy, cumhuriyetçi, Medici'ye hasım) → bilimsel cilt; Savonarola yazıları (Yale) | ◐ | — |
| C13 | **Britannica: Botticelli** — Vasari'ye göre Savonarola'ya 1498'den sonra bile bağlı | Vasari (≈1550) → Britannica | ◐ | — |
| C14 | **İdam sabahı:** üç Dominiken şafakta ayine katılır, komünyon alır; rütbeleri sökülür; sapkınlık, bölücülük ve yenilik vaazıyla suçlanırlar (M5 K29) | DBI Savonarola, Buonvicini, Maruffi | ◐ | (M5 K29'a bak) |
| C15 | **Del Nero:** Mart 1497'de Gonfalonier; "gece başı kesildi" (DBI) | DBI Del Nero | ◐ | — |
| C16 | **Catherine ve surlar:** kuşatma uzayınca "çıplak surlara zincirlensin/askerlere teslim edilsin" önerileri | EN Wikipedia, palazzo-pitti.net, careexperienceandculture.com (hepsi modern özet) — **kim önerdi/ilk yazan: bulunamadı** (Varchi/Busini/Altoviti/Cavalcanti adları aramada çıkmadı) | ANEKDOT ◐ | — (ayrıntı cinsel şiddet içerir: videoda söylenmez) |
| C17 | **Murate'de üç yıl; "hayatının en mutlu yılları"** | Mark Strage'a atfen (modern) | ○ | EN: *"the happiest of her entire life"* |
| C18 | **Çeyiz ve düğün:** *"une dot conséquente de 100 000 ducats et de somptueux bijoux"*; evlilik "promptement consommé" | Fransızca özetler | ◐ | FR (özet) → "Hatırı sayılır bir çeyiz: 100.000 duka ve gösterişli mücevherler" (**evlilik gecesi ayrıntıları: söylenmez**) |
| C19 | **Henri II'nin kazası:** Montgomery kırık mızrak parçasını bırakmadı; kıymık gözüne girdi | Guizot (19. yy) | ◐ | EN (Guizot özeti): *"a splinter of wood entered Henry's eye"* |
| C20 | **Catherine'in dul giysisi:** "1559'dan beri hep siyah" | Bir tarih çalışması | ○ | EN: *"dressed always in black widow's weeds"* |
| C21 | **Çifte nitelik:** *"…the familiar myth of the wicked Italian queen."* | Britannica (Catherine) | ◐ | → "tanıdık 'kötü İtalyan kraliçe' efsanesi" |
| C22 | **Louvre başlıkları (Rubens döngüsü, görülenler):** *Les Parques filant le destin de la reine Marie de Médicis sous la protection de Jupiter et de Junon* · *La Naissance de la reine, à Florence le 26 avril 1573* · *L'Instruction de la reine* · *Henri IV reçoit le portrait de Marie de Médicis et se laisse désarmer par l'Amour* · *Les Épousailles de la reine* · *Le Débarquement de la reine à Marseille, le 3 novembre 1600* · *L'Arrivée de la reine à Lyon* · *La Naissance du Dauphin… à Fontainebleau, le 27 septembre 1601* · *Le Couronnement de la reine à l'abbaye de Saint-Denis, le 13 mai 1610* · *L'Apothéose de Henri IV et la proclamation de la régence de la reine, le 14 mai 1610* · *La Majorité de Louis XIII. La reine remet les affaires au roi, le 20 octobre 1614* · *L'Échange des deux princesses de France et d'Espagne sur la Bidassoa à Hendaye, le 9 novembre 1615* · *La Reine s'enfuit du château de Blois dans la nuit du 21 au 22 février 1619* | Louvre koleksiyon sitesi (başlıklar sayfa başlığı olarak görüldü; içerik açılmadı) | ◐ zayıf | (başlıklar kurum başlığıdır; 21 anlatı tablosunun **tamamı görülmedi** → Concini'nin yokluğu doğrulanamaz) |
| C23 | **Louvre'un yorumu:** sipariş Marie'ye **kendi anlatısını sunma** olanağı verdi; ressam kralı gücendirmemeye dikkat etmeliydi; anne–oğul ancak **1621**'de barıştı; tablolar "kahramanca" bir kipte (*"heroic mode"*) | Louvre (*To the glory of a queen of France* ve koleksiyon sayfası) | ◐ zayıf | EN (özet) |
| C24 | **Dissimulation tezi:** seri, farklı seyirciye farklı katmanlar sunan, bilgiye erişimi kraliçe ve çevresinin denetlediği bir dil | *Renaissance Quarterly* 67/3 (2014), s. 878–916 (yazar özetten çıkmadı) | ◐ | — |
| C25 | **Köln levhaları:** Wallraf 1822; 1987 levhası; ev 1942'de yıkıldı | dokumen.pub Köln makalesi (tek) | ○ | — |

---

## 4. Sayılar ve ölçüler

| Konu | Değer(ler) | Kaynak / çelişki | Sınıf |
|---|---|---|---|
| Lorenzo'nun yaşı | 43 yıl 3 ay (1 Oca 1449 → 8 Nis 1492; M5) | DBI + EI | ◐ |
| Piero'nun yaşı | Nisan 1492'de 20; 9 Kasım 1494'te 22 (doğum 15 Şub 1472: yıl ◐, gün ○; hesap bize ait) | M5 | ◐ |
| Savonarola'nın yaşı | 24 Nisan 1475'te 22 yıl 7 ay (21 Eyl 1452 doğum); ölürken 45 yıl 8 ay (M5) | Britannica + M5 | ◐ |
| Charles: Piero'nun kovulmasından girişe | 8 gün (9 → 17 Kasım; hesap) | — | ◐ |
| Anlaşma bedeli | 120.000 florin, altı ay, iki temsilci | tek özet; M2 HAFIZA-D | ○ |
| Büyük Konsey | "üç binden fazla" yurttaş (uygunluk) | Treccani | ◐ |
| 1497 idam | 5 kişi | Enc. machiavelliana; DBI Del Nero | ◐ |
| 1434 → 1494 | 60 yıl (Cosimo'nun dönüşü → Piero'nun gidişi; hesap bize ait; 1434 M2/c3) | — | ◐ + hesap |
| 7 Şubat 1497 → 23 Mayıs 1498 | ≈ 15,5 ay ("bir buçuk yıl"; hesap) | — | ◐ |
| Ateş: Charles'ın ordusu | 30.000 (yağma bağlamı) | JSTOR kitap tanıtımı | ○ |
| Piero/Giovanni başına ödül | 4.000 / 2.000 florin (Beck) ↔ 5.000 dukat | M1b b68 | ○ çelişir |
| Catherine: anne/baba ölümü | 15 gün / 21 gün (doğumdan; hesap bize ait) | Treccani EI + PUF | ◐ |
| Catherine: evlilik yaşı | 14 yıl 6 ay (13 Nis 1519 → 28 Eki 1533; hesap) | — | ◐ |
| Catherine: çocuk | 10 (Britannica); yaşayan sayısı HAFIZA | Britannica | ◐ / HAFIZA |
| Çeyiz (1533) | 100.000 duka/écu + mücevher (28.000 écu: tek Fr. özet ○) | S35, M4 | ◐ / ○ |
| Henri II kaza → ölüm | ≈10 gün | Britannica | ◐ |
| Francis II ölümü → Henri II ölümü | 17 ay (hesap) | — | ◐ |
| Paris 1572 | ≈ 3.000 (Britannica tahmini); ülke geneli 10.000–30.000 **HAFIZA** | Britannica | ◐ / HAFIZA |
| Guise → Catherine'in ölümü | 13 gün (23 Aralık 1588 → 5 Ocak 1589; hesap) | Britannica | ◐ |
| Çeyiz (1600) | 600.000 taç/écu; Fransa'nın borcu "bir milyona yakın écu" (tek Fr. özet ○) | S47; M4b b41 | ◐ / ○ |
| 1589 → 1600 | 11 yıl (hesap) | — | ◐ |
| Rubens döngüsü | 24 tablo = 21 anlatı + 3 portre (10+10+1 + 3); sipariş 1622, üretim 1622–25 | Louvre | ◐ |
| Rubens'in doğumu | 28 Haziran 1577, Siegen | Britannica | ◐ |
| Louvre restorasyonu | 4 yıl; ≈293 m²; 4 milyon € | Louvre | ◐ zayıf |
| Marie'nin sürgünü | Temmuz 1631 → Temmuz 1642 ≈ 11 yıl (hesap) | Versailles + Britannica | ◐ |
| **Kullanma** | Marie'nin doğum yılı (1573/1575); 1.174.000 écu (görülmedi); ek yıllık 20.000 (tek); 28.000 écu mücevher (tek); Rubens ücreti (bilinmiyor); Piero/Giovanni ödülleri (çelişir) | | |

---

## 5. Mit/efsane ve tarihçi tartışmaları

### 5.1 Savonarola Lorenzo'nun ölüm yatağında  **[ANEKDOT ◐ / mit]**
- **İddia:** Üç şart; Lorenzo üçüncüde yüzünü duvara çevirir; rahip günah çıkarma/kutsama vermeden ayrılır.
- **Kim ne diyor:** Burlamacchi, G. F. Pico, Razzi, Barsanti (Savonarola partisi, ≈40 yıl sonra). **Poliziano (görgü tanığı mektubu)** rahibi anar ama şartlar ve duvar yok; kutsama konusunda üç ayrı aktarım (Symonds ↔ Gardner ↔ üçüncü özet) → ayrıntı söylenmez. Britannica "şüpheli"; Catholic Encyclopedia "genellikle reddedilir". Villari "Burlamacchi'ye inanabiliriz" (Symonds aktarır); Gino Capponi inanmıyor; Reumont "tartışma hiç kesin çözülmedi".
- **Davranış:** "Yandaşları şöyle anlattı…" + "Poliziano'nun mektubunda ise…" (D48). **Uydurma iç ses yok.**

### 5.2 Botticelli kendi resimlerini yaktı mı?  **[MİT ◐]**
- Çağdaş kanıt yok; Vasari yazmaz; Nardi'nin listesinde (özetlere göre) Botticelli adı geçmez; "Botticelli'lerin Ateşi" türü başlıklar geç ve kaynaksız; Britannica: sanat yıkımı **önemsiz**. Düşük kaliteli sayfalar (Academia/dokumen özetleri) iddiayı tekrarlar ama birincil pasaj göstermez. **Davranış:** "Sık anlatılır; kanıt yok." Botticelli'nin sonraki işleri konusunda M3 ↔ Britannica nüansı (D61).

### 5.3 Kibirlerin Yakılması "sanat katliamı" mıydı?  **[NİTELİKLİ ◐]**
- Esas eşya: süs, ayna, kozmetik, kart, zar, oyun masası, müzik aleti; resim ve heykel de listede (Nardi); Britannica "sanat ve kitap yıkımı önemsizdi". Taraflı kaynaklar (Piagnoni/Arrabbiati). **Davranış:** "Çoğu eşya süs ve oyundu; resimler de vardı ama toplu bir sanat yıkımı kanıtlı değil."

### 5.4 Lorenzo'nun ölümünde Duomo yıldırımı ve zehir  **[HAFIZA / ○]**
- Yıldırım: bulunamadı. Zehir: DBI "temelsiz"; Leoni'nin kuyudaki ölümü ○ (D50).

### 5.5 Capponi'nin "trompet–çan" sözü  **[ANEKDOT]**
- Varlığı ◐ (birçok kaynak, farklı lafız); lafız ○; ilk anlatıcı (Guicciardini/Landucci/Cambi) belirsiz. **Birebir söylenmez.**

### 5.6 Savonarola'nın "kandan şapka" sözü  **[ANEKDOT ○]**
- D65. Britannica "kaydeder"; teklif doğrulanmamış; vaazda söylenmiş olabilir. **Tırnaksız.**

### 5.7 Piero "tembel/beceriksiz" mi?  **[YORUM]**
- Tek ansiklopedi yargısı (Treccani) ↔ Cambridge monografisi (D54). **"Çözülen düzen" çerçevesi**; kişiye alay yok. "lo Sfortunato" lakabı bu turda da görülmedi (M5).

### 5.8 Catherine çatalı getirdi  **[MİT ◐; "kanıt yok"]**
- D77. Fisher 1954 → popüler; çatalın Catherine'den önce de bilindiği (Bizanslı prenses 1071 anekdotu tek özet ○), İtalya'da 16. yy'da yaygınlaştığı, Fransa'da yavaş girdiği ◐; **"getirdi" iddiasına kaynaklı bağ yok.**

### 5.9 Catherine dondurmayı getirdi  **[MİT ◐]**
- M4b bM9: Liddell–Weir, Colonial Williamsburg, Cooks Info; 19. yy dondurmacı hikâyesi; Procope 1686 (M4 HAFIZA). Bu turda yeniden aranmadı.

### 5.10 Catherine topuklu ayakkabıyı getirdi  **[MİT ○]**
- D77. Popüler iddia; Semmelhack aktarımı: Yakın Doğu binicilik ayakkabısı; 1533 evliliği ile bağ kaynaksız.

### 5.11 Catherine parfümü getirdi / kokulu eldiven  **[ANEKDOT ○]**
- D77. Grasse'ın Galimard hikâyesi; "citation needed"; Bianchi gerçek, "başlattı" kanıtsız; "zehirci" etiketi ○ (M4b b37).

### 5.12 Catherine'in zehirleri  **[MİT ◐]**
- Jeanne d'Albret (Haziran 1572) akciğer hastalığı; zehir suçlamaları McIlvenna'ya göre kadın karalamasının **edebî kalıbı**; bir akademik derleme: Catherine'in zehirle ilişkisi "sorgulanabilir, kanıtlı vaka az"; Dumas gibi sonraki kurgu pekiştirdi.

### 5.13 *Balet comique de la reine* (1581)  **[GERÇEK ◐]**
- M4b b38: Joyeuse Dükü düğün şenlikleri, Catherine himayesi, Beaujoyeulx, Circe, 5 saati aşkın, 1582 basılı metin. **"İlk balet de cour" sıfatı nitelikli.**

### 5.14 1572'de Catherine'in sorumluluğu  **[◐ kısmen]**
- D75. "Coligny'nin öldürülmesini onayladı, katliamı büyük olasılıkla değil" kalıbı; Mariéjol "tuzak"; Jouanna konsey; Knecht daha az aklayıcı. **Tek tarihçi adı kesin tutum olarak verilmez.** Charles IX'un "hepsini öldürün" sözü ANEKDOT (M4b bM8): **söylenmez.** Coligny girişiminin azmettiricisi ○ (Guise/Alba/Catherine).

### 5.15 "Kötü İtalyan kraliçe": siyah efsane  **[◐]**
- D76. Britannica + McIlvenna + IA kaydı. **Davranış:** "Efsane 1572'den hemen sonra, broşür ve şiirle başladı; kimi düşmanları 'İtalyan'lığını suçlamaya çevirdi."

### 5.16 Rubens'in doğduğu evde Marie  **[MİT ◐/○]**
- D69.

### 5.17 Rubens döngüsü propaganda mı, aklama mı?  **[YORUM ◐]**
- Louvre dili: "kendi anlatısını sunma"; dissimulation tezi: katmanlı alegori; M4b bM10: "aklama" (özet yorumu). **"Propaganda" kesin kipte değil; "imge siyaseti" YORUM.** Concini'nin gösterilmeyişi ve suikastın sahnelenmeyişi: **Louvre başlıklarında Henri IV'ün ölümü yerine "Apotheosis" (14 Mayıs 1610) var** (C22); 21 başlığın tamamı görülmedi.

### 5.18 "Kızı çırılçıplak aldım" (I. François)  **[ANEKDOT ○]**
- M4 §5.16 (Orieux'ye atfen, herodote.net). **Kaba; videoya girmez.**

### 5.19 Düğün gecesinde kralın yatak odasında kalışı  **[ANEKDOT ◐]**
- M4 3.D #5. **Cinsel gönderme: videoya girmez** (USLUP §2-7).

---

## 6. Sahne adayları ("yıldız an")

| # | Aday | Belgelenmiş / aktarılan | Belirsiz / yasak |
|---|---|---|---|
| S-c10-1 | **9 Kasım 1494** (Pazar) | Landucci tarihi; Corsini ○; "bir saat" emri ◐; "halk ve özgürlük" ◐; Bologna yolu; Giovanni'nin kılığı | **Saat, ışık, çan yok** (Cambi: *vespro* ○); kapıdaki kişinin adı ○ |
| S-c10-2 | **Nisan 1492 Careggi** | DBI: Pico ve Poliziano orada; Poliziano mektubu; Pico'ya söz | Mektup metni görülmedi; yıldırım yok; Savonarola sahnesi iki sürüm |
| S-c10-3 | **7 Şubat 1497 → 23 Mayıs 1498** | İki ateş, aynı meydan; liste; ateş sınavı; şafak ayini | Botticelli ANEKDOT/mit; Venedikli teklif yok; ateş sınavının ayrıntıları (yağmur, şartlar) bulunamadı |
| S-c13-1 | **3 Temmuz 1642 Köln** | Yoksulluk; Sternengasse; tablolar Paris'te | Odanın betimi, son sözler, tanıklar yok; Richelieu H |
| S-c13-2 | **22–24 Ağustos 1572** | Britannica kalıbı; tarihler | Çan, şafak, sayılar (ülke), Charles'ın sözü yok |
| S-c13-3 | **28 Ekim 1533 Marsilya / 3 Kasım 1600 Marsilya** | İki iniş aynı limanda (kurgusal eşleme) | Törenin saat akışı, hediyeler yok |
| S-c13-4 | **Galerie Médicis (1625'te Luxembourg / bugün Louvre)** | 10+10+3+1 düzeni; başlıklar | Tabloların kopyası çizilmez (özgün temsil) |

---

## 7. Hâlâ eksik kalanlar (metne GİRMEZ)

**c10**
1. Poliziano'nun mektubunun metni (özgünü ve Ross çevirisi, Gutenberg 74973) — Pico'ya söz, Savonarola'nın rolü, tarih.
2. Landucci, Cambi, Parenti, Guicciardini (*Storie fiorentine*) **9 Kasım** ve **17 Kasım** anlatıları; kapının adı; çan; saat; Piero'nun sözleri; Medici evinin o gün ve sonrası (envanter: M1b X6).
3. Capponi sözünün kaynağı; müzakerenin tam şartları; 120.000 florin; Savonarola–Charles görüşmesinin anlatısı (Pisa mı Floransa mı).
4. Savonarola'nın vaaz metinleri (1493–94) ve 1494 Aralık vaazları; "yeni Cyrus" vaazı (1495).
5. Kibirlerin Yakılması tanık metni (Landucci, Nardi, Burlamacchi); yığının biçimi ve yüksekliği; Venedikli teklif; Fra Bartolomeo/Credi.
6. Ateş sınavı günü (sahne, yağmur, pazarlık); tutuklama; son sözler; Landucci'nin idam girdisi (22/23 Mayıs).
7. Piero'nun karakteri için Guicciardini/Nardi/Poliziano mektupları; Ludovico Sforza'nın daveti; Andreas Palaiologos; Fivizzano günü.
8. Michelangelo: Condivi'nin kar heykeli ve ayrılış anlatısı.
9. **HAFIZA (önerilmez):** Pico (17 Kasım 1494) ve Poliziano'nun (24 Eylül 1494) ölümleri; "Vacca" çanının 9 Kasım 1494'te çaldığı; Savonarola'nın boyu/yüzü; "kadınlar mücevher attı" türü sahneler.

**c13**
1. Catherine'in **mektupları** (iç dünya için); 1572 sonrası yazışmaları; çocukluk (Murate) kaynağı; kuşatma anekdotunun ilk yazanı.
2. Marsilya 1533'ün tanık anlatısı (yer, saat, hediyeler); çeyiz belgesi; ilk çocuğun doğum günü (19 Ocak 1544 H).
3. Estienne/Bèze/de Serre atfının çözümü; Gentillet; "tuez-les tous" zinciri (Tavannes, Bourgeon 1996); Holt/Crouzet/Sutherland/Diefendorf'un tutumları.
4. Çatal (Fisher'in kaynağı), dondurma (Procope), topuk (Bata Museum sayfası), parfüm (Galimard hikâyesinin ilk geçtiği yer) için doğrudan kaynak sayfaları.
5. Marie: doğum yılı/günü; çeyiz–borç mahsubunun birincil belgesi (Medici Archive Project); vekilin kimliği; Concini'nin öldürülme günü (24 Nisan 1617 H); Blois kaçışı ayrıntıları (ip/merdiven ANEKDOT); Marie'nin Köln'e geliş tarihi; son günleri; cenaze/kalbin yeri; Richelieu ve XIII. Louis'in ölüm tarihleri.
6. Rubens döngüsü: sözleşme metni, ücret, teslim takvimi, Peiresc'in rolü; **21 anlatı tablosunun başlıklarının tamamı** (Concini/Henri IV suikastı); Marie'nin ve Richelieu'nun tepkisi; "Sternengasse 10" levhalarının asıl kaynağı.
7. Louvre restorasyonunun güncel durumu (Ekim 2026): çalışmaların başlayıp başlamadığı; galerinin açık kalan bölümü.

**Sonraki tur için yapıştırılabilir sorgular**
- `Poliziano lettera ad Jacopo Antiquario morte di Lorenzo testo Careggi Pico biblioteca confessore Savonarola`
- `Landucci Diario fiorentino 9 novembre 1494 Piero de' Medici palazzo porta Corsini "popolo e libertà" campana`
- `Savonarola Carlo VIII Pisa novembre 1494 ambasceria Cambi Landucci Guicciardini Storie fiorentine`
- `Rubens Medici cycle Concini omitted Thuillier Foucart Rubens Peiresc letters Marie de Medicis Galerie 1625 Henrietta Maria`
- `Marie de Médicis Cologne 1642 mort Sternengasse dernière demeure testament cœur La Flèche Saint-Denis`
- `Catherine de Médicis Marseille 1533 entrée Clément VII noces témoin ambassadeur récit dot`

---

## 8. Okunacak kaynaklar (HAFIZA künyeleri — araçla doğrulanmadı)

Poliziano, *Letters* (ed. S. Butler, Harvard 2006) · Luca Landucci, *Diario fiorentino* (Del Badia 1883; Jervis çevirisi 1927: archive.org'da kaydı görüldü, S29) · Giovanni Cambi, *Istorie* · F. Guicciardini, *Storie fiorentine* · J. Nardi, *Istorie della città di Firenze* · D. Weinstein, *Savonarola: The Rise and Fall of a Renaissance Prophet* (Yale 2011) · L. Polizzotto, *The Elect Nation* (Oxford 1994) · Piero monografisi (Cambridge UP 2020; yazar özetten çıkmadı) · J. Knecht, *Catherine de' Medici* (1998) · A. Jouanna, *La Saint-Barthélemy* · U. McIlvenna, *Scandal and Reputation at the Court of Catherine de Medici* (Routledge 2016) · T. Osborne, "A Queen Mother in Exile…" · Corpus Rubenianum XIV (Büttner; Merle du Bourg) · Thuillier–Foucart, *Rubens' Life of Marie de' Medici* (1967) · *Renaissance Quarterly* 67/3 (2014) makalesi.

---

## 9. Kaynak anahtarı (arama sonuçlarında **görülen** adresler; içerikleri **açılmadı**)

**c10**
- **S01** Britannica, Lorenzo de' Medici: https://www.britannica.com/biography/Lorenzo-de-Medici
- **S02** *Lives of the Early Medici* (Gutenberg 74973): https://www.gutenberg.org/files/74973/74973-h/74973-h.htm
- **S03** Reumont, *Lorenzo de' Medici* c. 1 ve 2: https://www.gutenberg.org/files/50624/50624-h/50624-h.htm · https://www.gutenberg.org/files/50625/50625-h/50625-h.htm
- **S04** Symonds, *Renaissance in Italy* c. 1: https://www.gutenberg.org/files/15400/15400-h/15400-h.htm
- **S05** Britannica, Savonarola: https://www.britannica.com/biography/Girolamo-Savonarola · https://www.britannica.com/biography/Girolamo-Savonarola/Trial-and-execution · https://www.britannica.com/place/Italy/Savonarola · https://www.britannica.com/summary/Girolamo-Savonarola
- **S06** dokumen.pub, *Savonarola* (Yale; ISBN 9780300178487): https://dokumen.pub/savonarola-9780300178487.html
- **S07** dokumen.pub, *The Elect Nation* (Oxford-Warburg): https://dokumen.pub/the-elect-nation-the-savonarolan-movement-in-florence-1494-1545-oxford-warburg-studies-1nbsped-0199206007-9780199206001.html
- **S08** dokumen.pub, *Selected Writings of Girolamo Savonarola* (Yale): https://dokumen.pub/selected-writings-of-girolamo-savonarola-religion-and-politics-1490-1498-9780300129045.html
- **S09** Treccani Enc. machiavelliana, Piero de' Medici: https://www.treccani.it/enciclopedia/piero-de-medici_(Enciclopedia-machiavelliana)/ · https://www.treccani.it/enciclopedia/piero-de-medici/ · EI Piero di Lorenzo: https://www.treccani.it/enciclopedia/piero-di-lorenzo-de-medici_(Enciclopedia-Italiana)/
- **S10** Treccani, Capponi, Piero: https://www.treccani.it/enciclopedia/piero-capponi_(Enciclopedia-machiavelliana)/ · https://www.treccani.it/enciclopedia/piero-capponi/
- **S11** Treccani, Firenze (Enc. machiavelliana): https://www.treccani.it/enciclopedia/firenze_(Enciclopedia-machiavelliana)/ · *Firenze alla fine del Quattrocento*: https://www.treccani.it/enciclopedia/firenze-alla-fine-del-quattrocento_(Storia-della-civilt%C3%A0-europea-a-cura-di-Umberto-Eco)/
- **S12** Treccani, Savonarola (Enc. machiavelliana): https://www.treccani.it/enciclopedia/girolamo-savonarola_(Enciclopedia-machiavelliana)/
- **S13** DBI Lorenzo (c. 73, 2009): https://www.treccani.it/enciclopedia/lorenzo-de-medici_(Dizionario-Biografico)/ · EI: https://www.treccani.it/enciclopedia/medici-lorenzo-de-detto-il-magnifico_(Enciclopedia-Italiana)/
- **S14** DBI Leoni, Piero (c. 64, 2005): https://www.treccani.it/enciclopedia/piero-leoni_(Dizionario-Biografico)/
- **S15** DBI Del Nero, Bernardo: https://www.treccani.it/enciclopedia/bernardo-del-nero_(Dizionario-Biografico)/
- **S16** DBI Leone X: https://www.treccani.it/enciclopedia/papa-leone-x_(Dizionario-Biografico)/
- **S17** Piero di Lorenzo monografisi (Cambridge UP): https://www.cambridge.org/core/books/piero-di-lorenzo-de-medici-and-the-crisis-of-renaissance-italy/FA69B4422BF159C072451FC26640DC76 · bölüm 16: https://www.cambridge.org/core/books/abs/piero-di-lorenzo-de-medici-and-the-crisis-of-renaissance-italy/perambulating-italy-14941497/DBAF1409B95B0F7F03A972CABF6BA0D1 · dokumen.pub: https://dokumen.pub/piero-di-lorenzo-de-medici-and-the-crisis-of-renaissance-italy.html
- **S18** Johnson, *Europe in the Sixteenth Century 1494–1598*: https://www.gutenberg.org/files/42025/42025-h/42025-h.htm
- **S19** *Florentine Palaces and Their Stories*: https://www.gutenberg.org/files/71464/71464-h/71464-h.htm
- **S20** Gardner, *The Story of Florence*: https://www.gutenberg.org/files/37793/37793-h/37793-h.htm
- **S21** Academia, "Hosting the Enemy… Florence, 1494": https://www.academia.edu/79999531/Hosting_the_Enemy_Accommodating_the_French_King_and_his_Troops_in_Florence_1494
- **S22** Cambridge, *Apocalypse without God*: https://www.cambridge.org/core/books/apocalypse-without-god/historical-case-studies/82EB1580C2809AC968A9F6D840CCD06D · *Church History* makalesi: https://www.cambridge.org/core/journals/church-history/article/abs/savonarola-florence-and-the-millenarian-tradition/446A1B40E8BD6C88F210AAD5CED20FE0
- **S23** Academia, "King Charles VIII, Savonarola, and Florence in Botticelli's Final Adoration": https://www.academia.edu/13176766/King_Charles_VIII_Savonarola_and_Florence_in_Botticellis_Final_Adoration_improved_version
- **S24** Britannica, Charles VIII: https://www.britannica.com/biography/Charles-VIII · Italian Wars: https://www.britannica.com/event/Italian-Wars
- **S25** Britannica, Botticelli (Late works): https://www.britannica.com/biography/Sandro-Botticelli/Late-works
- **S26** Academia, "Botticelli and the Bonfire of the Vanities": https://www.academia.edu/21479916/Botticelli_and_the_Bonfire_of_the_Vanities · JSTOR Daily: https://daily.jstor.org/the-renaissance-lets-its-hair-down/
- **S27** Symonds, *Life of Michelangelo*: https://www.gutenberg.org/cache/epub/11242/pg11242-images.html · Vasari *Lives*: https://www.gutenberg.org/files/32362/32362-h/32362-h.htm · Britannica, Michelangelo: https://www.britannica.com/biography/Michelangelo
- **S28** Wikisource, EB 1911 "Savonarola": https://en.wikisource.org/wiki/1911_Encyclop%C3%A6dia_Britannica/Savonarola,_Girolamo · Catholic Encyclopedia "House of Medici": https://en.wikisource.org/wiki/Catholic_Encyclopedia_(1913)/House_of_Medici
- **S29** Landucci, *A Florentine diary from 1450 to 1516* (archive.org kaydı): https://archive.org/details/ldpd_10273453_000
- **S30** DBI Orsini d'Aragona, Gentil Virginio: https://www.treccani.it/enciclopedia/orsini-d-aragona-gentil-virginio_(Dizionario-Biografico)/
- **S31** dokumen.pub, *The Italian Wars 1494–1559*: https://dokumen.pub/the-italian-wars-1494-1559-war-state-and-society-in-early-modern-europe-2nd-edition-1138739049-9781138739048.html · Guicciardini seçkisi: https://dokumen.pub/the-defeat-of-a-renaissance-intellectual-selected-writings-of-francesco-guicciardini-9780271084336.html
- **S32** dokumen.pub, *Inventing the Renaissance* (U. Chicago Press; Savonarola 1475): https://dokumen.pub/inventing-the-renaissance-the-myth-of-a-golden-age-1nbsped-0226837971-9780226837970-g-2263223.html

**c13**
- **S33** Britannica, Catherine de' Medici: https://www.britannica.com/biography/Catherine-de-Medici · https://www.britannica.com/biography/Catherine-de-Medici/The-Massacre-of-St-Bartholomews-Day · https://www.britannica.com/summary/Catherine-de-Medici
- **S34** Treccani EI, Caterina: https://www.treccani.it/enciclopedia/caterina-de-medici-regina-di-francia_(Enciclopedia-Italiana)/ · Treccani Atlante: https://www.treccani.it/magazine/atlante/cultura/Caterina_de_Medici_la_Regina_Nera.html
- **S35** *Catherine de Médicis* (PUF; kronoloji; dokumen.pub): https://dokumen.pub/catherine-de-medicis-9782130818908-2130818900.html
- **S36** Britannica, Henry II: https://www.britannica.com/biography/Henry-II-king-of-France · Guizot, *History of France*: https://www.gutenberg.org/files/11954/11954-h/11954-h.htm · Thompson, *Wars of Religion in France*: https://www.gutenberg.org/files/49266/49266-h/49266-h.htm
- **S37** Academia, "The 'infertility' of Catherine de Medici…": https://www.academia.edu/81994577/The_infertility_of_Catherine_de_Medici_and_its_influence_on_16th_century_France
- **S38** Internet Archive, Estienne *Discours merveilleux…*: https://archive.org/details/discoursmerveill00esti · Wikisource EB 1911 "Catherine de' Medici": https://en.wikisource.org/wiki/1911_Encyclop%C3%A6dia_Britannica/Catherine_de'_Medici · Academia "Has-been Queens": https://www.academia.edu/3793505/Has-been_Queens_Reception_and_Re_figuration_of_Catherine_de_Medici_and_Mary_Stuart_in_Translation
- **S39** McIlvenna, *Scandal and Reputation…* (dokumen.pub): https://dokumen.pub/scandal-and-reputation-at-the-court-of-catherine-de-medici-9781317059318-9781472428219-9781315607672.html · "A Stable of Whores?": https://www.academia.edu/5065751/A_Stable_of_Whores_The_Flying_Squadron_of_Catherine_de_Medici
- **S40** Britannica, Massacre of St Bartholomew: https://www.britannica.com/event/Massacre-of-Saint-Bartholomews-Day · Jouanna (dokumen.pub): https://dokumen.pub/the-saint-bartholomews-day-massacre-the-mysteries-of-a-crime-of-state-0719088313-9780719088315.html
- **S41** Britannica, Blois: https://www.britannica.com/place/Blois-France · Mariéjol (Gutenberg): https://www.gutenberg.org/files/36315/36315-h/36315-h.htm
- **S42** National Geographic: https://www.nationalgeographic.com/history/world-history-magazine/article/table-manners-renaissance-catherine-de-medici · California Academy of Sciences: https://research.calacademy.org/research/anthropology/utensil/forks.htm · The Florentine: https://www.theflorentine.net/?p=5463 · Wikipedia Coryat's Crudities: https://en.wikipedia.org/wiki/Coryat%27s_Crudities
- **S43** Topuk (ikinci el; Bata Shoe Museum/Semmelhack aktarımı): https://truefashionistas.com/blogs/fashion-files/history-of-high-heels · https://www.fibre2fashion.com/industry-article/4819/history-of-high-heel-shoes
- **S44** Britannica, France – The age of the Reformation: https://www.britannica.com/place/France/The-age-of-the-Reformation · Michel de L'Hospital: https://www.britannica.com/biography/Michel-de-LHospital · dokumen.pub *The French Wars of Religion, 1562–1629*: https://dokumen.pub/the-french-wars-of-religion-1562-1629-9780521358736-9780521353595-9780511131844.html
- **S45** Grasse (turizm/Wikipedia): https://www.hellomonaco.com/the-riviera/in-the-neighborhood/grasse-perfumery-rare-jasmine-and-catherine-medici-s-fragrant-gloves-1/ · https://www.connexionfrance.com/magazine/visit-grasse-the-picturesque-fragrance-capital-of-france/720886
- **S46** Catherine ve kuşatma: https://en.wikipedia.org/wiki/Catherine_de%27_Medici · https://www.palazzo-pitti.net/the-siege-of-floreence-1529-1530.html · https://www.careexperienceandculture.com/master/women-of-power%3A-the-life-and-times-of-catherine-de'-medici
- **S47** Britannica, Marie de Médicis: https://www.britannica.com/biography/Marie-de-Medicis · Gutenberg *Marie de Medicis*: https://www.gutenberg.org/files/11531/11531-h/11531-h.htm · Pardoe c. 2 ve 3: https://www.gutenberg.org/cache/epub/11600/pg11600-images.html · https://www.gutenberg.org/files/11601/11601-h/11601-h.htm · Guizot c. 2: https://www.gutenberg.org/files/11955/11955-h/11955-h.htm
- **S48** Osborne, "A Queen Mother in Exile…": https://www.academia.edu/48394484/A_Queen_Mother_in_Exile_Marie_De_M%C3%A9dicis_in_the_Spanish_Netherlands_and_England_1631_41
- **S49** Château de Versailles, Day of the Dupes: https://en.chateauversailles.fr/discover/history/key-dates/day-dupes-1630 · Britannica: https://www.britannica.com/event/Day-of-the-Dupes
- **S50** Louvre koleksiyon sayfaları (Rubens döngüsü): https://collections.louvre.fr/en/ark:/53355/cl010060825 (Parklar) · …/cl010060824 (Doğum, 26 avril 1573) · …/cl010060820 (Marsilya, 3 novembre 1600) · …/cl010060841 (Dauphin, 1601) · …/cl010066009 (Taç, 13 mai 1610) · …/cl010060839 (Apothéose, 14 mai 1610) · …/cl010060834 (Majorité, 1614) · …/cl010060836 (Hendaye, 1615) · …/cl010060833 (Blois, 21–22 fév. 1619) · …/cl010060900 (Portre 1573–1642) · …/cl010060822, …/cl010060823, …/cl010060821, …/cl010060819
- **S51** Louvre, *To the glory of a queen of France – The Galerie Médicis (Temporarily closed)*: https://www.louvre.fr/en/explore/the-palace/to-the-glory-of-a-queen-of-france · Basın: https://presse.louvre.fr/annonce-de-la-restauration-du-cycle-de-marie-de-medicis-de-pierre-paul-rubens/ · PDF: https://presse.louvre.fr/wp-content/uploads/2026/03/d936895176d342b63bd1c1f2c7aed694.pdf · Louvre+: https://louvre.fr/louvreplus/video-une-restauration-hors-norme-le-cycle-de-marie-de-medicis-de-pierre-paul-rubens
- **S52** *Renaissance Quarterly*, dissimulation: https://www.cambridge.org/core/journals/renaissance-quarterly/article/abs/rubenss-life-of-maria-de-medici-dissimulation-and-the-politics-of-art-in-early-seventeenthcentury-france/7330379A5889F6D8EE0D8E142B038FC7 · Academia: https://www.academia.edu/10543855/_Rubens_s_Life_of_Maria_de_Medici_Dissimulation_and_the_Politics_of_Art_in_Early_Seventeenth_Century_France_Renaissance_Quarterly_67_n_3_2014_878_916 · "Pictures fit for a queen": https://www.academia.edu/628091/Pictures_fit_for_a_queen_Peter_Paul_Rubens_and_the_Marie_de_Medici_cycle · "L'iconologie du pouvoir": https://www.academia.edu/6771238/L_iconologie_du_pouvoir_Le_cycle_de_Marie_de_M%C3%A9dicis_par_P_P_Rubens · IA *La Galerie Médicis de Rubens au Louvre*: https://archive.org/details/lagaleriemedicis00rube
- **S53** Köln/Rubenshaus (dokumen.pub; hangi cilt olduğu özetten kesin değil): https://dokumen.pub/kln-in-unheiligen-zeiten-die-stadt-im-dreiigjhrigen-krieg-9783412217938-9783412224110.html · https://dokumen.pub/lexikon-der-klner-architekten-vom-mittelalter-bis-zum-20-jahrhundert-1nbsped-9783412524487-9783412524463.html · Britannica, Rubens özeti: https://www.britannica.com/summary/Peter-Paul-Rubens
