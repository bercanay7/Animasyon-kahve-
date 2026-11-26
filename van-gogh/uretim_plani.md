# Van Gogh'un mektupları (Theo'nun gözünden): üretim planı

Durum: 27 Kasım 2026, taslak.
- Motor: `araclar/tablo` (canlanan yağlıboya) + Blender figür yolu. Üslup kapısından geçti: `kurye/kurgu.sh`.
- Dal notu: oturum yalnız `claude/3d-puppet-drawing-shader-4ca4y8` dalına yazabiliyor. Video bu dalda `van-gogh/` altında üretilir; motorla birlikte `main`'e birleşir.

## 1. Talep kontrolü (27 Kasım; `araclar/talep/iki_dil.py`)
| Sorgu | TR öneri | TR medyan | TR en çok | EN medyan | Okuma |
|---|---|---|---|---|---|
| van gogh \| van gogh | 14 | 250 B | 23,5 M | 1,6 M | çok büyük kapı |
| van gogh mektupları \| letters to theo | 2 | 377 | 1,38 M (tek video) | 7 B | **mektup açısı Türkçede boş** |
| van gogh buğday tarlası \| wheatfield with crows | 3 | 1 B | — | 344 | küçük |

Motora uygun öteki adaylar (aynı gün): Walden (TR medyan ~184 B, çoğu sesli kitap), Piri Reis haritası (~154 B, hep "gizem"), Küçük Prens (~64 B, telif ve karakter tasarımı riski), Tolstoy'un son yolculuğu (~8 B), Yaşlı Adam ve Deniz (~6 B, telifli metin). **Kullanıcının seçimi: Van Gogh'un mektupları.**

## 2. Kullanıcının kararları (27 Kasım, seçenekli sorular)
- **Bakış:** Theo'nun gözünden.
  - Mektupların öbür ucu: her ay para gönderen, tabloları satamayan kardeş.
  - Sıradan birinin gözünden büyük hikâye; Vincent'in sesi mektuplardan gelir.
- **Ölüm:** kısa ve ayrıntısız. Olay gösterilmez; tek cümle ve sessizlik.
- **Üslup:** karma. Dünya siyah-beyaz yağlıboya (grisaille); yalnız Vincent'in gördüğü ve boyadığı renkli.
  - Tabloları kamu malı fotoğraflarıyla, gerçek rengiyle girer.
  - Filmdeki tek yüzler Vincent'in kendi otoportreleri olur (kodla yüz çizilmez).

## 3. Hikâyenin omurgası (başkan)
- **Kahraman Theo** (başlıktaki ad değil, CLAUDE.md iş akışı 3).
- **Asıl kurye Johanna van Gogh-Bonger.** İki kardeş öldükten sonra mektupları ve tabloları geleceğe taşıyan, sergiyi kuran, mektupları yayımlayan o. Kanalın "geçmişten bugüne soru taşıyan kurye" fikri bu videonun dönüşü olur.
- **Motorun motifi tarihte:** *Badem Çiçekleri* (Şubat 1890), Theo'nun yeni doğan oğlu Vincent Willem için yapıldı (doğrulanacak, `kaynak/`). Mektuplar filmindeki "mektup ağaca ulaşır, ağaç çiçek açar" anının tarihteki karşılığı.

## 4. Başlık adayları (en az 10; beş soru)
**K**işisel soru · **N**efes · **Y**arı tahmin ettirir, ele vermez · **Ka**pı ("Van Gogh") önde · **B**ağlamsız anlaşılır. ≤ 45 karakter.
- Önceki videonun kalıbı "… Olur muydun?" (Stanford); "-ır mıydın" kalıbı art arda kullanılmaz.

| # | Aday | Kr. | K | N | Y | Ka | B | Not |
|---|---|---|---|---|---|---|---|---|
| 1 | Van Gogh'a Kim İnandı? | 22 | ~ | ✓✓ | ✓✓ | ✓ | ✓ | Cevabı yarı tahmin ettirir ("kardeşi"), dönüşü saklar (Jo); izleyiciye örtük soru: sana kim inanıyor? |
| 2 | Van Gogh'u Bize Kim Getirdi? | 28 | ✗ | ✓ | ✓✓ | ✓ | ~ | Kurye fikri; "bize" bağlamsız biraz belirsiz |
| 3 | Van Gogh'a Kimse İnanmasa Sen İnanır mıydın? | 44 | ✓✓ | ~ | ✓ | ✓ | ✓ | En kişisel; kalıp Stanford'a yakın (art arda) |
| 4 | Van Gogh'a On Yıl Para Gönderen Adam | 35 | ✗ | ✓ | ~ | ✓ | ✓ | Somut vaat, soru yok |
| 5 | Van Gogh'un Tek Hayranı Kimdi? | 30 | ✗ | ✓ | ✓ | ✓ | ✓ | "Tek" iddiası doğrulanmalı (Anna Boch, eleştirmen Aurier) |
| 6 | Van Gogh Satamadı, Peki Kim İnandı? | 35 | ~ | ~ | ✓ | ✓ | ✓ | 1'in uzunu; "satamadı" efsaneye yaslanır |
| 7 | Van Gogh'u Ünlü Yapan Kadın | 27 | ✗ | ✓ | ✗ | ✓ | ✓ | Dönüşü ele verir |
| 8 | Herkes Güldü, Biri İnandı: Van Gogh | 35 | ✗ | ✓ | ✓ | ✗ | ✓ | Kapı sonda |
| 9 | Van Gogh'un Mektupları Kime Yazıldı? | 36 | ✗ | ✓ | ✗ | ✓ | ✓ | Bilgi merakı, cevabı tek kelime |
| 10 | Van Gogh'a İnanmanın Bedeli Neydi? | 33 | ~ | ✓ | ✓ | ✓ | ✓ | Theo'nun hikâyesini doğru vaat eder; biraz ağır |
| 11 | Van Gogh'u Kim Yaşattı? | 23 | ✗ | ✓✓ | ✓ | ✓ | ~ | 1'e yakın; "yaşattı" iki anlamlı (para, ün) |

**Başkanın seçimi (öneri): 1, "Van Gogh'a Kim İnandı?"**
- Kapı en önde, tek nefes.
- Cevap ilk bakışta "kardeşi" gibi görünür (doğru ama eksik); video sonunda ikinci kişiyle (Jo) tamamlanır.
- Kişisel soru ilk ve son cümlede: "Sana kimse inanmazken kim inandı? Sen kime inandın?"
- **Yedek: 10.** Kapak B'nin vaadi olarak yaşar.

## 5. Kapak taslakları (iki ayrı vaat; kapakta da yalnız Vincent'in dünyası renkli)
- **A, "tek ışık": TEK KİŞİ İNANDI.**
  - Grisaille, karanlık bir Paris odası. Masada lamba ışığında bir zarf yığını; sırtı dönük bir adam (Theo) bir tuvali ışığa tutuyor.
  - Tuval karenin tek renkli ve en parlak yeri (Badem Çiçekleri ya da Ayçiçekleri; PD fotoğraf).
  - Yazı 3 kelime: "TEK KİŞİ İNANDI". Film ilk saniyede bu odayla açılır.
- **B, "nesne": 650 MEKTUP** (sayı doğrulanınca).
  - Gri bir mektup yığınının içinden renkli bir badem dalı çıkıyor, çiçekleri açık. Yazı: "650 MEKTUP".
  - Vaat: mektuplardan çıkan resim. Film kancanın sonunda (mektup açılır, renk dalı büyür) bunu karşılar.
- **Hassasiyet:**
  - Kulak olayı kapağa girmez (sansasyon, yara).
  - Kırmızı leke yok (kan okunur).
  - Dört yapraklı çiçek yok (haç); badem çiçeği beş yapraklıdır, doğru da budur.
  - "DELİ" sözcüğü hiçbir yazıda yok (ruh sağlığı damgası).

## 6. İskelet: Harmon çemberi, kahraman Theo
- Önceki iskeletler: Lale Kahramanın Yolculuğu, Dorian Harmon. Stanford'unki `stanford/`'dan teyit edilecek; aynıysa Kişōtenketsu'ya geçilir.
- **Ad yükü:** seste yalnız Vincent, Theo, Jo (ve Gauguin tek cümle).
  - Anna Boch, Aurier ve Dr. Gachet ekranda etiket ya da anılmaz.
  - Doruğu taşıyan Jo kancada ekilir (Ran dersi): görüntüsüyle (bir kadın sırtı ve elinde bir defter), adı söylenmeden "bu hikâyeyi bitiren üçüncü kişi".

| Adım | İçerik (taslak; kaynaklar `kaynak/arastirma_dosyasi.md` gelince) |
|---|---|
| **0. Kanca** (0–~30 sn) | Paris, bir oda; kapı altından bir zarf. Theo açar; içinden bir çizim ve bir istek: "Biraz daha boya…". İlk cümle başlığın sorusu: "Van Gogh'a kim inandı?" Sayı olay olarak: on yılda yüzlerce mektup, her biriyle bir parça para. Üçüncü kişi ekilir: yıllar sonra aynı mektupları sandıktan çıkaran bir kadın eli |
| **1. Sen (rahat yer)** | Theo, Paris'te bir sanat galerisinde çalışan düzenli, saygın bir genç. Ağabeyi başarısız işlerden sonra 27 yaşında "ressam olacağım" der. Theo cebinden para gönderir |
| **2. İhtiyaç** | Ağabeyinin resimleri satmaz; Theo'nun işi resim satmak, ama kendi kardeşininkini satamaz. Mektupların dili: Vincent Theo'ya resimlerin ortak yapımcısı der (alıntı, numaralı) |
| **3. Gitmek** | Arles (1888): sarı ev, güneş. Ekranda renk patlaması: tablolar renkli, dünya gri. Theo her ay gönderir |
| **4. Aramak** | Aralık 1888: kriz (yalnız tarih ve bir cümle; ayrıntı yok); Theo gece trenine biner. Ardından hastane, mektuplar sürer |
| **5. Bulmak** | Ocak 1890: Theo'nun oğlu doğar, adı Vincent. Ağabey ona bir badem dalı boyar: çiçek açan ağaç (filmin rengi en çok burada). Aynı yıl ilk satış ve ilk övgü yazısı |
| **6. Bedel** | Temmuz 1890: Vincent ölür (tek cümle, sessizlik; olay gösterilmez). Cebinden gönderilmemiş bir mektup çıkar (alıntı). Altı ay sonra Theo da ölür |
| **7. Dönüş (kurye)** | Jo, 28 yaşında, bir bebek, yüzlerce tablo ve bir sandık mektupla kalır. Herkes "satıp kurtul" der; o mektupları okur, defter tutar, sergi açar (1905), mektupları yayımlar (1914), Theo'yu Vincent'in yanına taşır (1914) |
| **8. Değişim (iksir)** | Bugün müzede iki kardeşin mektupları yan yana. Soru izleyiciye: sana kimse inanmazken kim inandı? Ve sen kime inanıyorsun? Abone çağrısı son anın içinde (mektup kapanır) |

**Merak döngüleri (soru → cevabı olan olay):**
1. Kanca: "Van Gogh'a kim inandı?" → 1–6 Theo, 7 Jo (ikinci cevap).
2. 2: "Theo resim satıyordu; neden kardeşininkini satamadı?" → 2–3: galerinin istediği resim, Vincent'in boyadığı resim (iki tablo yan yana).
3. 5: "Bu badem dalı kimin için?" → 5: bebeğin adı.
4. 6: "Mektuplar bize nasıl ulaştı?" → 7: Jo'nun sandığı ve 1914.

**Uygulanacak dersler:**
- Kancadan hikâyeye köprü sıfır cümle; hikâye ≤ 0:45'te başlar.
- "Melankoli", "deha" gibi kavram anlatımı yok; nesne ve olay (zarf, tuval, tren bileti, defter).
- Hikâye bitince yorum kısa tutulur.

## 7. Üslup (başkan; kapı `araclar/tablo/geriye_bakis.md`)
- **Dünya:** grisaille yağlıboya (`mono` kipi). Paris odası, galeri, tren, Arles ve Auvers tarlaları, Bussum'daki ev.
  - İç mekân motorda henüz denenmedi: ilk üslup karesi Theo'nun odası.
- **Renk:** yalnız Vincent'in tabloları (kamu malı fotoğraflar, `lisans-kontrol`) ve onun boyadığı şeyin dünyadaki karşılığı. Örnek: Arles'da gri tarla, Vincent'in baktığı yerden renklenir. Palet değişimi sözcüğe bağlı ve plan içinde olur.
- **Figür:** Theo, Vincent, Jo; Blender figür yolu, siluet, sırt, omuz üstü.
  - Yüz yok. Yüzler yalnız otoportrelerde, gerçek tablo olarak.
  - Vincent'in figürü kendi otoportrelerindeki giysiden: mavi iş gömleği, hasır şapka. Ama renksiz.
- **Hassasiyet** (CLAUDE.md taraması + bu video):
  - Kulak ve yara gösterilmez.
  - Ölüm gösterilmez; silah, tabanca, kan gösterilmez.
  - Hastane ve akıl hastanesi pencerelerinde parmaklık haç okunabilir: yalnız dikey çubuk.
  - Kilise ve haç kompozisyona girmez (Auvers kilisesi tablosu gerekirse gerçek tablo olarak, sanat eseri bağlamında).
  - "Deli" ve "çılgın" sözcükleri yok. İntihar sözcüğü YouTube kurallarına göre bilgilendirici ve kısa; anlatımın tonu Türkçe yardım hattı notunu gerektirirse açıklamaya konur.

## 8. Sıradaki adımlar
1. Kaynak dosyası (araştırma ajanı, sürüyor); başkan doğrular → `kaynak/DOGRULAMA.md`.
2. İskeletin teyidi (Stanford'un iskeleti) ve kapakların vaadinin senaryoda karşılanması.
3. Senaryo (`senaryo.json`); tempo kontrolü; 3 tahmin `analiz/tahminler.md`.
4. Üslup kapısı: Theo'nun odası (iç mekân, lamba, gri) + Arles tarlası (renklenme) + 15 sn hareket.
5. Seslendirme (Emrullah; kredi hesabı önce bildirilir).
