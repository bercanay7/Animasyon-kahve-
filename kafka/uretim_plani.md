# Kafka, *Dönüşüm*: üretim planı (rev0, 15 Kasım 2026)

Durum: konu ve üslup kullanıcıyla kararlaştırıldı; senaryo yazılmadı. Kullanıcının haftalık kullanımı %89: bu hafta yalnız plan, kaynak ve senaryo taslağı; kurul ve sahneler sıfırlamadan sonra.

## Talep kontrolü (senaryodan önce; yeni kural)
YouTube otomatik tamamlama (hl=tr, gl=tr) ve Türkçe arama sonuçları, 15 Kasım 2026:

| Arama | Otomatik tamamlama | Var olan Türkçe videolar |
|---|---|---|
| "dönüşüm kafka" | özet, sesli kitap, analiz, **animasyon**, film, felsefesi, 5 dakika | Portal "HEPİMİZ BİRER BÖCEĞİZ" 1,0 M; sesli kitaplar ~100 B; "Yararlı Olmayı Bıraktığında Sevilmezsin" 8,5 B; Türkçe animasyon yalnız 1 (6:24, 1,6 B) |
| "gregor samsa" | dönüşüm, böcek, edit, animation | |
| Kontrol: "milton" | Milton Delgado, kasırga, Friedman: **konu hiç çıkmıyor** | |
| Kontrol: "ikaros" | işaret fişeği, Brawl Stars: **konu hiç çıkmıyor** | |
| Kontrol: "sisifos" | söyleni, felsefesi, hikayesi | |

- (a) **Tanınırlık: güçlü.** İsim Sisifos düzeyinde tanınıyor; Milton ve İkaros'ta arama konuya ulaşmıyordu.
- (b) **Kişisel soru: güçlü,** ama açı seçilmeli. Rakip açılar: "hepimiz böceğiz" (yabancılaşma, Portal), "yararlı olmayınca sevilmezsin". Bizim farkımız aşağıdaki iki kaynak sürprizi ve "o / bu" zamiri.
- Elenen adaylar: Suç ve Ceza (tanınır, kalabalık, kişisel soru orta), Nietzsche/Torino atı (kişisel soru zayıf), Diyojen (arama bir podcast markasına kayıyor).

## Yorum (kullanıcıyla birlikte)
- **Kullanıcıyı etkileyen:** bir sabah böcek olarak uyanmak; dış görünüş değişince herkesin onu hor görmesi.
- **Kullanıcının dürüst notu:** eser popüler ama onu *Kayıp Cennet* gibi derin düşüncelere atmadı. Bu yüzden derinlik özetten değil, metnin içindeki az bilinen ayrıntılardan kurulur (İkaros dersi: sürpriz kaynağın kendisinde).
- **Aile:** ne kötü ne masum; ikisinin ortası (kullanıcı ve başkan aynı yerde). Yorgun, korkmuş, sonunda rahatlamış.
- **Kafka'nın babası:** tek kısa geri dönüş (kullanıcının kararı).
- **Omurga: koşullu sevgi (kullanıcının seçimi, 15 Kasım; başkanın ilk önerisiydi).** Dış görünüşün değişmesi tetikleyicidir, anlamı koşullu sevgidir: aile Gregor'u para getirdiği ve tanıdık göründüğü sürece "o" diye sever; ikisi de bitince "bu" der (K4, K7). Kaynakla uyumlu: Gregor'un ailedeki yeri baştan beri parayla kurulmuş (borç, satış seyahatleri), dönüşümden sonra ilk düşündüğü de iş ve para.
  - İncelik (kurul tartacak): Grete'nin ilk günlerdeki bakımı gerçek sevgidir; sevgi bir anda değil, yorgunlukla aşınır. "Aile kötü" değil, "sevginin koşulları yavaş yavaş görünür olur".
  - Derinlik: koşulu yalnız aile koymaz; Gregor da kendi değerini kazancıyla ölçer ve gizli birikimi öğrenince sevinir (K4). Koşullu sevgiyi önce kendine uygulamıştır.
  - Rakipten ayrım: "Yararlı olmayınca sevilmezsin" (8,5 B) aynı damarda; bizim farkımız zamir (o → bu), Gregor'un kendi koşulu ve ailenin dönüşümü.
  - Bugünkü karşılık: hastalık ya da engellilik **değil** (insanı böcekle eşleştirir; hassasiyet riski), bakım veren aile **değil** (aileleri suçlar). Karşılık: eskisi gibi kazanamayan, eskisi gibi görünmeyen, eskisi gibi "işe yaramayan" herkes. Son soru: *seni sevenler seni mi seviyordu, yoksa senin işe yarayan hâlini mi? Ve sen kendini hangi koşulla seviyorsun?*

### Metinden doğrulanmış dayanaklar (Gutenberg satırı, `kaynak/die_verwandlung_numarali.txt`)
| # | Ne | Satır |
|---|---|---|
| K1 | "ungeheueres Ungeziefer": Kafka bir böcek türü adı vermez; "Ungeziefer" (haşere, yaratılmışların en değersizi) | 2 |
| K2 | İlk derdi korku değil iş: saat beşteki tren kaçtı, sonraki yedide | 64, 73 |
| K3 | Müdür yardımcısı: "Das war eine Tierstimme" (bu bir hayvan sesiydi). Gregor kendini anlaşılır sanıyor; sesi artık insan sesi değil | 365 |
| K4 | **Gizli birikim:** babanın eski işten kalan küçük bir serveti ve Gregor'un getirdiği paradan artırılmış bir sermaye varmış. Gregor yıllarca babanın borcunu ödemek için çalışmıştı. Kapının arkasında bunu duyunca **"hevesle başını sallar"**, bu tutumluluğa sevinir | 855–868 |
| K5 | Baba: aylardır koltukta oturan adam, altın düğmeli mavi üniformayla dimdik | 1197 |
| K6 | Kırmızı elmalar; biri sırtına saplanır ve orada çürür (filmin tek rengi) | 1233–1236; sırtta kalır 1258; çürümüş elma 1736 |
| K7 | **Zamir:** kız kardeş "Wir müssen es loszuwerden suchen" (ondan, "bundan" kurtulmalıyız) ve "bunun Gregor olduğu düşüncesinden kurtulmalısın". Almancada "er" (o, Gregor) → "es" (bu, şey) | 1651, 1676 |
| K8 | Son cümle: tramvayda kız "genç bedenini gerindi"; asıl dönüşen aile | 1892 |
| K9 | Kafka'nın yayıncıya mektubu: böcek çizilmesin, uzaktan bile gösterilmesin (Kurt Wolff Verlag, Ekim 1915) | **DOĞRULANACAK** (senaryo kurulunda kaynak üyesi; mektup metni bulunamazsa cümle çıkar) |
| K10 | *Babaya Mektup* (1919; kamu malı): tek geri dönüş için hangi cümle | **DOĞRULANACAK**; Almanca metin depoya alınacak |

Çeviriler kendi çevirimizdir (Türkçe çeviriler telifli olabilir); açıklamada kaynak yazılır.

## Hikâye iskeleti: Kişōtenketsu (seçildi)
- **Neden:** Dönüşüm'ün gücü bir çatışmanın çözümünde değil, okurun beklentisinin ters dönmesinde: herkes "Gregor dönüştü" diye okur, metin "asıl dönüşen aile" der. Kişōtenketsu'nun üçüncü adımı (ten, dönüş) tam olarak bu. Kahramanın Yolculuğu'nun "dönüş" ve "iksir" adımları Gregor'a uymaz (geri dönmez, ölür).
- **Önceki videolar:** İkaros = Harmon çemberi; Milton = Kahramanın Yolculuğu. Art arda tekrar yok.
- **Kahraman:** Gregor değil, **izleyici**. Gregor bir ayna; soru izleyicinin kendisine döner. Ailenin (özellikle Grete'nin) dönüşümü hikâyenin ikinci ekseni.

| Adım | İçerik | Cümleler (taslak) |
|---|---|---|
| **Ki (giriş)** | Kanca: uyanış ve ilk dert: tren (K1, K2). Merak sorusu ilk cümlede. Böceği görmeyeceğiz (L2 açılır) | A01–A06 |
| **Shō (gelişme)** | Kapı açılır, müdür yardımcısı kaçar, "hayvan sesi" (K3); baba sopa ve gazeteyle geri iter; Grete süt getirir, oda boşaltılır; elma (K6) | B01–B14 |
| **Ten (dönüş)** | İki sürpriz: (1) gizli birikim ve Gregor'un buna sevinmesi (K4): "böcek olmadan önce de bir şeydi"; (2) "o" "bu" olur (K7); baba dikleşir (K5); asıl dönüşen aile, Grete gerinir (K8) | C01–C12 |
| **Ketsu (birleştirme)** | Kafka neden böceği göstermedi (K9, L2 kapanır); tek geri dönüş: Kafka ve babası (K10); bugüne soru; abone çağrısı doruk anında | D01–D10 |

Toplam ~42–48 cümle; hedef 6–7 dk (kullanıcı 5–10 dk önerdi; başkan kararı).

### Merak döngüleri
- **L1 (A01 → A03):** "Böcek olarak uyandığında Gregor'u en çok ne korkutur?" → böcek olmak değil, işe geç kalmak. Hızlı ödül, ilk 20 sn.
- **L2 (A05 → D02):** "Bu videoda böceği hiç görmeyeceksiniz. Nedenini sona saklıyorum." → Kafka'nın mektubu (K9 doğrulanamazsa döngü "Kafka ona bir tür adı bile vermez" (K1) ile kapanır).
- **L3 (A06 → C10):** "Bu hikâyede biri daha dönüşüyor." → aile, Grete'nin gerinmesi.
- **ABT:** her bölümde bir AMA: "ama sesi artık insan sesi değildi", "ama Gregor sevindi", "ama artık 'o' demiyorlardı".

## Paketleme taslağı (senaryodan önce; paketleme kurulu senaryo kuruluyla birlikte görecek)
**Başlık adayları** (<60 karakter; "NEDEN …?" kalıbından kaçınılır, Sisifos ve Milton'da kullanıldı):
1. Kafka'nın Dönüşüm'ü: İşe Yaramasan da Seni Severler miydi?
2. Sevgi Koşullu mudur? | Kafka'nın Dönüşüm'ü
3. Bir Sabah Böcek Olarak Uyansan Seni Kim Severdi? | Kafka

**Kapak adayları** (ağaç baskı, tek renk kırmızı elma; tek odak; Bebas ≥ 290 px; sağ alt boş):
- **A:** aralık kapı, karanlık odaya düşen ışık şeridi, eşikte kırmızı elma. Yazı: **"ARTIK O DEĞİL"** (zamir sürprizi; ilk saniyede karşılanır: film aralık kapıyla açılır).
- **B:** aile sofrada, kapıya sırtı dönük; kapının altından uzanan gölge. Yazı: **"ONDAN KURTULALIM"**.
- Hassasiyet notu: "böcek" kelimesi kapakta insana hakaret gibi okunabilir; kapak kurulunda sorulacak.

## Üslup
- **cinecode `woodcut` (ağaç baskı)**, LemoLab'ın MIT lisanslı demo motoru (`styles/woodcut/demo/engine/index.js` + `core/lib.js`), bizim çekim sistemimize (`film.js`: `S()`, `Wd()`, `plan()`) ve `render.js`'e takılır. Yeni motor yazılmaz.
- Neden: karanlık oda siyah blok, ışık yalnız oyulan yerde (kapı aralığı, pencere); figürler küçük oyulmuş silüet (yüz yakın planı yok); tarifin "en çok bir renk, yalnız yanan şey için" kuralı = kırmızı elma.
- `silent-film` elendi: demo karesindeki figür bebek yüzlü, oyuncak gibi; ailenin yakın planlarında aynı sorun çıkar.
- Risk: Milton'a benzerlik (ikisi de siyah-beyaz). Ayrım: Milton beyaz kâğıtta ince gravür, bu siyah blokta kaba bıçak izi + kırmızı.
- **Kırmızı çizgiler (taslak; hassasiyet üslup kapısında bakar):** böcek hiç gösterilmez (yalnız gölge, kapı, mobilya, ailenin bakışı); Gregor'un bedeni ve ölümü görsel olarak işlenmez; gerçek kişiler (Kafka, babası) gerçekçi portre değil dönem silueti; hastalık ya da engellilik böcekle eşleştirilmez; Yahudi kimliği ya da 1940'lar (Kafka'nın kız kardeşlerinin ölümü) bu videoya girmez: ayrı ve ağır bir konu, bağlamsız ima hassasiyet riski.

## Kurul ve kullanım planı
- Kapılar: senaryo + paketleme taslağı → üslup kapısı (manzara + orta plan + yakın plan + 15 sn; hassasiyet burada) → ilk tam kurgu → son render ve yayın paketi (tek tur; birleştirme kullanım sınırı yüzünden, kayda yazılır) → kapak.
- Kapı başına 2 birleşik mercekli üye (İkaros düzeni): A = senaryo/dramaturji/kanca/paketleme, B = kaynak/doğruluk/hassasiyet. Çizim ajanı yok. Ölçüm küçük modelle ya da araçla.
- Bu hafta (kullanım %89): plan, kaynak, senaryo taslağı. Kurul toplanmaz.
- Ortam: Whisper, scipy, soundfile, pyloudnorm yine yok → `ikaros/tools/hizala.py`, `ikaros/audio/dsp_shim.py`, `ikaros/tools/mix_ffmpeg.py`.

## Kredi (tahmin; kesin sayı kurul sonrası metinle)
~45 cümle × ~95 karakter ≈ 4.300 karakter × 2 çekim ≈ **8.600 karakter** (İkaros 9.206). Üretimden önce kesin sayı kullanıcıya bildirilir, onay beklenir.
