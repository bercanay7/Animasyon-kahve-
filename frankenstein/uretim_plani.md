# Frankenstein ve 1816, yazsız yıl: üretim planı

Başlangıç: 23 Kasım 2026. Yön usulüyle (`analiz/2026-11-23-deney-yon-promptu.md`); yön metni `analiz/2026-11-24-frankenstein-yon-prompt.md`. Başkan tek başına; alt ajan yalnız Fable'ın senaryo okuması (seslendirmeden önce).

**Yön (kullanıcının, özet):** canavar ya da haddini aşan bilim hikâyesi değil. Frankenstein'ın suçu yaratmak değil, kaçmak. Yaratığın adı yok; iki yüz yıldır ona kaçan adamın adını veriyoruz. Soru izleyicinin: canavar doğulur mu, terk edilince mi olunur? Cevap kavramla değil, yaratığın kendi ağzından anlattığı hikâyeyle. Peşinden gidilecek soru: bunu on sekiz yaşında, annesini hiç tanımamış, bir yıl önce bebeğini kaybetmiş bir genç kadın neden yazdı? Tambora, gelmeyen yaz, Byron ve yarış o odaya giden yol. İzleyici kendi yarım bıraktığına bakarak çıkar.

**Kullanıcının fikrini sorma adımı (CLAUDE.md iş akışı 2):** yön metni bu adımın yazılı hâli; kullanıcı "kararlar senin" dedi. Ayrıca sorulmadı (Gılgamış'taki gibi).

## 1. Talep kontrolü (23 Kasım; `araclar/talep/talep.py`, `iki_dil.py`)
| Sorgu | Öneri | İlk 10 medyan | En çok | Öne çıkan öneriler |
|---|---|---|---|---|
| **frankenstein** | 14 | **41 B** | 14,8 M | sesli kitap, fragman, **2025** (Del Toro), korku evi |
| frankenstein mary shelley | 14 | 244 B | 2,4 M | İngilizce özet ve analiz |
| frankenstein kitap | 5 | 4,7 B | 413 B | kitap yorumu, özeti, inceleme |
| frankenstein'ın canavarı | 3 | 1,2 B | | **frankenstein gerçek mi**, filmleri |
| frankenstein canavar değil | 2 | 22 B | 386 B | gerçek mi, gerçek hikâyesi |
| mary shelley | 14 | 65 B (TR başlıklı 76 B) | 1,5 M | film (2017) |
| yazsız yıl | 3 | 219 | 3 B | nedir, olayı |
| canavar doğulur mu | 3 | 53 B | | canavar insanlar |
| kötülük doğuştan mı | 1 | 5,4 B | | "kötülük doğuştan mı gelir" |
| terk edilmek | 14 | 73 B | | şarkı ve "nasıl unutulur" |
| *kontrol:* kafka dönüşüm | 14 | 34 B | 1 M | |

**Okuma:**
- (a) **Tanıdık kapı güçlü:** "frankenstein" Kafka'nın kontrol satırıyla aynı bantta (41 B / 34 B) ve Del Toro filmi (2025) aramayı canlı tutuyor. Kitabın kendisini anlatan Türkçe video az (4,7 B medyan); "frankenstein gerçek mi" önerisi izleyicinin "canavarın arkasında ne var?" merakını gösteriyor.
- (b) **Kişisel soru güçlü:** "canavar doğulur mu" ve "kötülük doğuştan mı gelir" izleyicinin kendi sorusu; "terk edilmek" geniş bir duygu kapısı (başlığa değil, anlatıma).
- "Yazsız yıl" Türkçede boş ama tek başına kapı değil (219 medyan): başlığa girmez; açıklamada ve bölüm adında.

## 2. Başlık adayları (en az 10; eleme soruları: **K**işisel soru · **N**efes · **Y**arı tahmin ettirir, ele vermez · **Ka**pı kelimesi önde · **B**ağlamsız)
| # | Aday | Kr. | K | N | Y | Ka | B | Not |
|---|---|---|---|---|---|---|---|---|
| 1 | **Frankenstein: Canavar Doğulur mu, Olunur mu?** | 44 | ✓ | ✓ | ✓ | ✓ | ✓ | Yönün sorusu; "olunur" cevabı sezdirir ama yaratığın cinayeti cevabı tek yöne bırakmaz |
| 2 | Frankenstein: Asıl Canavar Kim? | 31 | ~ | ✓ | ✗ | ✓ | ✓ | Klişe ("Victor'du" diye tahmin edilir); yön bu okumayı da istemiyor |
| 3 | Frankenstein: Canavarın Adı Neden Yok? | 38 | ✗ | ✓ | ✓ | ✓ | ✓ | Bilgi merakı; kapağa daha uygun |
| 4 | Frankenstein: Kötü Doğulur mu, Olunur mu? | 41 | ✓ | ✓ | ✓ | ✓ | ~ | "Kötü" geniş; "canavar" filmin ve aramanın sözcüğü |
| 5 | Frankenstein: 18 Yaşında Bir Kız Neden Yazdı? | 45 | ✗ | ✓ | ✓ | ✓ | ✓ | Yönün ikinci sorusu; konu sorusu, izleyicinin hayatına değil → kapak B'ye |
| 6 | Frankenstein: Yarattığından Kaçan Adam | 38 | ✗ | ✓ | ✓ | ✓ | ✓ | Soru değil |
| 7 | Frankenstein: Terk Edilen Canavar Olur mu? | 42 | ✓ | ✓ | ✗ | ✓ | ✓ | Cevabı ele veriyor ("evet") |
| 8 | Frankenstein Gerçekte Kimin Adı? | 32 | ✗ | ✓ | ✓ | ✓ | ✓ | Trivia |
| 9 | Frankenstein: Seni Yapan Kaçsaydı? | 34 | ✓ | ✓ | ✓ | ✓ | ~ | Güçlü ama bağlamsız biraz anlaşılmaz |
| 10 | Yazsız Yıl: Frankenstein Nasıl Doğdu? | 37 | ✗ | ✓ | ✓ | ~ | ✓ | Kapı ikinci sırada; köken anlatısı (İngilizcede çok, Türkçede yok) |
| 11 | Frankenstein: Terk Edilmek İnsanı Canavar Yapar mı? | 51 | ✓ | ~ | ✗ | ✓ | ✓ | Uzun, ele veriyor |
| 12 | Frankenstein: Canavar Doğulur mu, Yapılır mı? | 45 | ✓ | ✓ | ✓ | ✓ | ~ | "Yapılır" çift anlamlı (yaratık gerçekten yapıldı); zekice ama telefonda ikinci okumayı ister |

**Seçim: 1. aday (44 karakter).** Kalıp: Gılgamış "Ad: genel soru?", Lale "Ad: ikinci tekil soru?"; art arda aynı kalıp sayılmaz mı? Üç videodur "Ad: soru?" biçimi sürüyor; bu kez soru **ikili** (doğulur mu / olunur mu), Gılgamış'ın "nasıl"ından ve Lale'nin "alır mısın"ından ayrışıyor. Kanal kuralı kalıbı korur, süsünü değiştirir. **Yedek:** 9.

## 3. Kapaklar (iki ayrı vaat)
- **A "ELİNİ UZATTI":** fener ışığı dairesinde yatağın perdesini aralayan yaratığın uzanan eli (dirsek kırık, avuç yukarı: selam okunmaz) ve kapıdan kaçan adamın sırtı. Tek odak: elin önündeki ışık; vurgu rengi yaratığın sarı gözü. Vaat: "bir yaratığın ilk hareketi bir istekti". A01'de (ilk 5 sn) ve G02'de (halka) karşılanır.
- **B "18 YAŞINDA YAZDI":** mum ışığında masada yazan genç kadın (¾ yüz, Regency saç), arkasında yağmurlu karanlık pencere ve camda fener gölgesi gibi beliren uzun bir siluet. Vaat: "bunu bir genç kız yazdı, nasıl?". A01'de "on sekiz yaşında bir kızın yazdığı" sözüyle ilk saniyelerde, B03'te karşılanır. (Fable: "18 YAŞINDAYDI" üçüncü sayfa haberi gibi okunabilir → "YAZDI".)
- Kapak yazıları başlığın sözcüklerini tekrar etmez. Hassasiyet: tabutta haç yok, düz kalkık kol yok.

## 4. Üslup: sihirli fener (boyalı cam slayt) — başkanın seçimi
**Neden:** 1816'nın korku gösterisi fenerdi: fantazmagorya karanlık bir salonda perdeye hayalet düşürürdü, Diodati'deki yarışı başlatan kitabın adı da *Fantasmagoriana*. Güneşin gelmediği bir yazın tek ışığı mum ve lambaydı. Fener aynı zamanda filmin fikrini taşıyor: **ışık bakıştır.**
- **Işık kuralı:** fener dairesi kimin üstündeyse hikâye ona bakıyordur. Başkalarının anlattığı bölümlerde (B–C) yaratık ışığın kenarında ya da dışında kalır; kendi ağzından anlattığı bölümde (D–F) dairenin merkezi ondadır; kör ihtiyarla tek sıcak daireyi paylaşır, kapı açılınca ışık sertleşir. Son sahnede (G05) ışık iris gibi kapanır: "karanlıkta, uzakta kayboldu".
- **Malzeme:** koyu örtücü boya (siluet), saydam boya yıkamaları (fırça izli, çizgiden hafif kayan), saydam bırakılan yerler (ay, alev, pencere) en parlak; camda toz ve kıl; perdede bez dokusu (ekrana sabit; slayt kayınca ikisi ayrışır).
- **Renk:** 1816 çerçevesi (B, H) gece mavisi ve mum sarısı; yaratığın dünyası mevsimle renklenir: kış mavi-gri, odunluk ilkbaharı yeşil, kör adamın odası sıcak; reddedilişten sonra renk çekilir. Tek vurgu: yaratığın küçük sarı gözü.
- **Figür:** koyu siluet profil; yaratık roman tarifiyle (uzun, ince, uzun parlak siyah saç, yırtık pelerin, küçük sarı göz). Universal tasarımı yok.
- **Geçiş:** aynı mekânda kesme; mekân sıçramasında slayt değişimi (yeni cam sağdan itilir, arada çerçevenin koyu kenarı); zaman sıçramasında iris (fener kapanır ve açılır).
- **Motor:** yeni ve küçük (`lib/fener.js`): Canvas 2D slayt tuvali × ışık lekesi, kadraj maskesi, küçük tuvalde parıltı. Hazır motorlarımızın hiçbiri aktarılan ışığı (geçen ışıkla renk) yapmıyor; cinecode `shadow-puppet` tarifi en yakın akraba, kodu bizim.

## 5. İskelet: iç içe çerçeve (romanın kendi yapısı) + Kişōtenketsu
**Seçim gerekçesi:** roman iç içe anlatılardır (Walton → Victor → yaratık → aile). Yönün istediği "yaratığın kendi ağzından" bu yapının merkezidir. Film de içe doğru iner ve geri çıkar: kanca (sahne) → 1816 odası (Mary) → romanda Victor → yaratığın kendi anlatısı (merkez) → buzlar (çerçeve kapanır) → 1831 önsözü (Mary). Akış Kişōtenketsu: giriş (1816), gelişme (yaratığın öğrenmesi ve iyiliği), dönüş (kör adam; sonra arşivdeki ikinci dönüş: "mutlu günlerdi" ↔ 1815 günlüğü), birleşme (çirkin evladıma yolun açık olsun). Önceki iki video Harmon (Dorian, Gılgamış); Lale ayrı.

**Kahraman:** yaratık (D–G). **Çerçevenin kahramanı:** Mary (B, H). **Karşıt:** Victor (kaçan). Her bölümde tek kahraman, tek mekân.

| Adım | İçerik | Cümleler |
|---|---|---|
| Kanca | el uzatılır, adam kaçar; ad yok; "genç bir kız nasıl buldu?"; başlığın sorusu | A01–A05 |
| I. Yazsız yıl (giriş) | Cenevre, yağmur; Mary 18, annesiz, kaybettiği kız, beş aylık oğul; Byron, Tambora; yarış; uyanık düş | B01–B16 |
| II. Kasım gecesi | Victor'un kaçışı; ad yok; buzulda yaratığın iddiası ("iyiydim") ve "beni dinle" | C01–C09 |
| III. Duvardaki yarık (gelişme) | yaratık kendi ağzından: ay, ateş, köy, yarık, odun ve "iyi ruh", aile sözcükleri, su yansıması, Victor'un günlüğü | D01–D13 |
| IV. Kör adam (dönüş) | görmeyen kabul eder, görenler kovar; yangın; kurtardığı kızın karşılığı kurşun | E01–E10 |
| V. Ben de yaratabilirim | çocuk, "Frankenstein", ilk cinayet, madalyon; "kötüyüm çünkü mutsuzum"; yarım kalan eş; düğün gecesi | F01–F11 |
| VI. Buzların arasında | tabutun üstünde uzanan el (halka); "soğumuş"; karanlıkta kaybolur | G01–G05 |
| VII. Çirkin evladım (birleşme) | adsız kitap ve afiş; 1831 önsözü; "mutlu günlerdi" ↔ 1815 günlüğü; "ona karşı bir sevgim var"; izleyiciye soru | H01–H11 |

**Merak döngüleri (soru → cevap olay):**
1. **L1** "Genç bir kız bunu nereden buldu?" (A04) → B12–B16 (uyanık düş) → H03–H09 (1831 önsözü ve 1815 günlüğü yan yana; Mary kendi yarattığını yeniden gönderir).
2. **L2** başlığın sorusu (A05) → C07 (yaratığın iddiası) → D–E (olaylar) → F03–F04 (cinayet: kanıt tek yöne eğilmez) → F07 ("kötüyüm, çünkü mutsuzum") → H10 (izleyiciye geri verilir).
3. **L3** "Adam neden kaçtı?" (A02) → C03–C04.
4. **L4** "Adı yok" (A03) → C05 → H02 (adsız kitap, afişte çizgi).
5. **L5** kaybettiği kız (B05) → H05–H06.
6. **L6** "Birazdan yaratık konuşacak" (A05) → C08–C09.
7. **L7** "O evde beni göremeyecek biri vardı" (D13) → E02.
8. **L8** yarım kalan beden (F09) → H10 ("yarım bırakıp yüzüne bakamadığın").
- **Kapak A halkası:** A01 uzanan el ↔ G02 tabutun üstünde uzanan el.

**Bölüm kartları** (YouTube bölümleri; kancadan hemen sonra kart yok, Gılgamış dersi): II. Kasım gecesi · III. Duvardaki yarık · IV. Kör adam · V. Ben de yaratabilirim · VI. Buzların arasında · VII. Çirkin evladım. "I. Yazsız yıl" yalnız açıklamadaki bölüm damgası.

## 6. Tempo kontrolü (rev1; `araclar/analiz/tempo_kontrol.py senaryo.json --yazar "Mary,Shelley,Byron"`)
Art arda soyut dizi yok; ilk iki dakikada soyut aday yok; köprü adayı yok; ikinci yarıda yeni ad yok (yalnız kanal adı H11'de).
| id | bayrak | karar |
|---|---|---|
| A04, A05 | T, YT | olay: cevaplar B12–B16, D–F, H |
| B02, B06 | Y | olay (Mary'nin mektubu, Byron'ın dizesi) |
| B07 | T | olay (patlama) + tek yan cümle; odadakilere bilgi verilmiyor |
| B10, B11 | YT | olay (sabah soruları, gece konuşmaları); Mary'nin anlatımı diye çerçeveli |
| D02, D10 | T | olay (ay; aile sözcükleri → kendi sorusu, kendi sözü) |
| E02 | T | olay (ihtiyarın sözü) |
| F02, F05, F07 | T | olay (çocuğun sözü, madalyon, yaratığın sözü) |
| H01 | T | L1'in dönüşü; hemen olay (H02 kitap, afiş) |
| H07 | Y | tek yorum cümlesi, iki kayıttan sonra (olaydan sonra tek cümle kuralı) |
| H10 | MT | iksir sorusu, olaydan (H08–H09) sonra |

**Hikâye nerede bitiyor:** G05 (yaratık karanlıkta kaybolur). Ardından H (~75 sn): kapak B'nin ve L1'in cevabı; somut kayıtlar (kitap, afiş, önsöz, günlük). "Hikâye bitince izleyici gider" riski bilinçli kabul; tahmin olarak `analiz/tahminler.md`'ye yazılır.

## 7. Yönden kendi seçtiklerim (deney kaydı; `geriye_bakis.md`'ye taşınacak)
- **Üslup: sihirli fener**, gerekçesi dönemin hayalet gösterisi ve *Fantasmagoriana*; "ışık bakıştır" kuralı.
- **İskelet:** romanın iç içe çerçevesi; yaratığın anlatısı filmin ortasında ve birinci tekil.
- **El zinciri:** perdeyi aralayan el (A01) → közdeki el (D04) → görünmeyen el (D09) → ihtiyarın tutulan eli (E04) → kaldırılmayan el (E06) → çırpılan eller (F04) → tabutun üstünde uzanan el (G02) → Mary'nin ateşin önünde ovan elleri (H06, yalnız görüntüde).
- **Ad zinciri:** ad yok (A03) → sıfatlar (C05) → "iyi ruh" (D09) → çocuğun ağzından "Frankenstein" (F02) → adsız kitap ve afişteki çizgi (H02).
- **Arşivle bozmak:** Mary'nin 1831'deki "mutlu günlerdi, ölüm yalnızca sözcüktü" sözü ile 1815 günlüğünün yan yana konması; nedensellik kurulmadan.
- **Beş aylık oğul:** yönde yoktu (Fable'ın bulgusu); tabloyu seçici bırakmamak için B05'e girdi.
- **Bırakılanlar:** *Kayıp Cennet* ve epigraf (dinî karşılaştırma), Polidori'nin adı ve *Vampir*, Claire, Christabel gecesi, Justine'in idamı, Fanny ve Harriet'in ölümleri, kuzey kutbu yolculuğunun ayrıntısı.

## 8. Fable senaryo okuması ve rev1 (23 Kasım; seslendirmeden önce)
Fable puansız tek okuma yaptı: 6 engelleyici, ~25 düzeltme, ~10 öneri. Her birini kaynakta sınadım.
- **Engelleyici, uygulandı:** F03–F04 cinayet kaynağa aykırı yumuşatılmıştı ("susturmak istedim" kaza gibi okunuyordu; romanda "ilk kurbanım sen olacaksın", boğaz, el çırpma) → kaynaktaki sırayla; F11 edilgen ("öldü") → "elinden aldı". H03 ve H09'daki "on beş yıl sonra" 1818'den sayılınca yanlış → "1831'de", "yıllar sonra". H03'te uydurma tırnak ("bir düş gördüm, dedi"; Mary "uyumadım" diyor) → "gözlerim kapalı ama uyanıkken". E07 "birkaç gün sonra" → "ertesi gün". 1823 afiş mektubu depoda yoktu → Marshall 1889 indirildi, söz doğrulandı ("rather good": "çok beğendi" abartıydı), cümle H02'ye taşındı. Eksik künyeler (Darkness, Tambora, 1818'in adsızlığı) depoya ve DOGRULAMA'ya.
- **Düzeltmeler, uygulandı:** B16 "yazdığı ilk cümle"; C07 yaratığın iddiası hikâyeden önce (sırası doğru) ve F07'de hikâyeden sonraki sözü (4508) → geriye dönüş kalmadı; "iblis" (dinî ad gibi) → "canavar"; F10 "tek bir söz" → "giderken şunu söyledi"; F02 kaynakta olmayan alay kalıbı çıktı; C06 öznesi (yaratık bulur); C08 "terk et"; C01 "iki yıla yakın"; "sulu göz" → "ıslak"; B11 "Mary'nin anlattığına göre"; H07 "bildiğimiz hiçbir yazısında"; H08 Mary'nin kendi kipi; B05 "geçen kış" + beş aylık oğul; B04 iki Mary karışmasın (ad ekranda); B bölümü sırası (kahramanlı cümleler öne, Tambora sonra); C bölümündeki olay dışı cümleler azaldı (Mary'nin buzul yürüyüşü çıktı, açıklamada); H10 tek soru (yas içindeki izleyiciye "ad koymak" bebeği çağırırdı); D06 odunluk; G05 çeviri kokusu; F06 dönüş işareti; okunuşlar yalnız `tts`'te (Frankenştayn, Meri Şelli, Bayrın, Pörsi, Viktor, Mon Blan).
- **Öneriler, uygulandı:** *Kayıp Cennet* cümlesi çıktı (karşılığı dinî benzetme); G04 yaratığın kendi sözü ("bu da benim kurbanım"); H05 13 Mart satırı ("bir anneydim, artık değilim"); kapak B "18 YAŞINDA YAZDI".
- **Reddedilen:** G03'ün yerine yaratığın sözü: G03 kapak A'nın halkasını sesle de kapatıyor, G04'te yaratığın sözü zaten var.

## 9. Seslendirme
- Emrullah (`DpEiQMnL9WxMsymCsjPY`, `creative_list_voices` ile doğrulandı), `eleven_v4`, 9 çekim × 2.
- Tahmin: s00 için `estimate_only` 1.265,9 kredi (664 etiketli karakter, 2 çekim → 1,906 kredi/karakter). Toplam 8.899 etiketli karakter × 1,906 ≈ **16.960 kredi** (Gılgamış'ta gerçek tahminin %2 üstündeydi: ~17.300). Kalan kredi bu bağlantıdan okunamadı (izin hatası).
