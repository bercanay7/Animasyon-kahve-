# Kapak kurulu, tur 1: P-TO (tıklama oranı ve paketleme stratejisti)

Bağımsız ilk bakış. Öteki üyenin raporunu görmedim. Koordinatlar 1280×720 kapak düzlemindedir.

## Neye baktım
- `milton/kapak/kapak_a.jpg`, `kapak_b.jpg` ve yedekler (karşılaştırma sayfasından).
- Test seti `kapak_is/tur5/test/`: `karsilastirma.jpg`, `akis_koyu.jpg`, `akis_acik.jpg`.
- Kendi küçültmelerim: 246×138, 168×94, 120×68 ve 168×94'ün 4 kat büyütmesi (`scratchpad/pto/`).
- Filmin açılış karesi `nif_is/kanca5/t0004.60.png`.
- `milton/youtube.md` (başlık adayları ve açıklama).

## Ölçümler (PIL ile)
| | A | B |
|---|---|---|
| Büyük harf yüksekliği | "BEN" y 225–353 = 129 px (%17,9); "CEHENNEMİM" y 392–523, İ noktası dahil 132 px (harf gövdesi ≈ %17,8) | "ŞEYTAN" E harfi y 72–204 = 133 px (%18,5); "AĞLADI" L harfi y 262–394 = 133 px (%18,5) |
| Yazının x aralığı | 47–771; figürün kanadına ≈ 60 px boşluk | 816–1236; göz levhasına ≈ 80 px, sağ kenara 44 px |
| Odak parlaklığı (0–255) | Alev ortalama 101; zemin 207, güneş halesi 179. **Karenin en parlak yeri zemin, alev değil.** | Gözyaşı 173, hemen çevresi 158 (fark 15). **En parlak yer yazı (253) ve göz akı; gözyaşı değil.** |
| Süre rozeti bölgesi (≈ x 960–1250, y 553–689) | Yazı yok; figürün etek ucu ve sağ kanat ucu var (sorun değil) | Boş |

## Ağırlıklar
| # | Ölçüt | Ağırlık |
|---|---|---|
| 1 | İlk bakışta anlaşılırlık (168×94'te yazı ve görsel) | %25 |
| 2 | Merak boşluğu (kapak + başlık birlikte) | %20 |
| 3 | Vaat ve tutma (ilk 5 saniyede karşılanıyor mu, yanıltıcılık) | %20 |
| 4 | Akışta ayrışma (koyu ve açık tema, A ile B'nin farkı) | %15 |
| 5 | Türk izleyici için kelime ve çağrışım | %10 |
| 6 | Rozet bölgesi, yazı boyu, odak tekliği | %10 |

Eşik 9,0. Hiçbir ölçüt 7'nin altında olamaz.

---

## Kapak A: "BEN CEHENNEMİM" → **8,3 / 10: RED** (düzeltilebilir; en yakın aday)

| Ölçüt | Puan | Gerekçe |
|---|---|---|
| 1 Anlaşılırlık | 8,5 | Yazı 120×68'de bile okunuyor. Kanatlı kara figür ve göğüsteki alev 168'de "karanlık melek" olarak okunuyor. Kim olduğunu ve neden tıklanacağını başlık tamamlıyor. Baş yüzsüz ve küçük bir topuz, gövde dimdik ve simetrik; heykel ya da manken gibi duruyor, acı okunmuyor. |
| 2 Merak | 8,0 | Birinci tekil bir itiraf: "kim, neden?" sorusunu doğuruyor ama bir iddia cümlesi; soru kendiliğinden çıkmıyor. 1 numaralı başlıkla ("…Neden Kaçamadı?") birleşince güçlü: başlık soruyor, kapak cevabın ipucunu veriyor. |
| 3 Vaat ve tutma | 9,5 | Açılış karesiyle neredeyse aynı (güneş, kanatlı figür, göğüste alev, "Ben cehennemim." cümlesi). Kanalın "kapak = ilk 5 saniye" kuralını tam karşılıyor. Yanıltma riski yok. Tek fark kapaktaki turuncu alev; filmde alev beyaz. Kabul edilebilir. |
| 4 Ayrışma | 7,5 | Koyu temada parlak parşömen kutusu çok iyi ayrışıyor (`akis_koyu.jpg`). Açık temada kâğıt rengi beyaz zeminle birleşiyor, kapağın kenarı kayboluyor (`akis_acik.jpg`). Renkli rakiplerin arasında tek renkli olması bir ayrım ama "soluk" da okunabilir. B'den yeterince farklı (açık/koyu, tam figür/yakın plan, alıntı/olay). |
| 5 Kelime | 8,0 | Yanlış okuma yok. Dinî bir iddia taşımıyor, bir karakterin sözü olarak okunuyor. Hafif "emo, metal grubu, dizi repliği" havası var; başlıktaki "Milton / Kayıp Cennet" bunu dengeliyor. |
| 6 Rozet, yazı, odak | 7,5 | Yazı %18 sınırında (17,8–18,3). Rozet bölgesinde yazı yok. **Odak bölünüyor:** alev rengiyle tek odak ama koyu (101). Karenin en parlak alanı hale ve sol zemin. Sol ve sağ üst köşedeki kara bulut parçaları (x 0–230 ve 1010–1280, y 0–66) 168'de kir ya da kesik leke gibi duruyor. |

Ağırlıklı toplam: 2,13 + 1,60 + 1,90 + 1,13 + 0,80 + 0,75 = **8,3**

## Kapak B: "ŞEYTAN AĞLADI" → **7,3 / 10: RED** (iki ölçüt 7'nin altında)

| Ölçüt | Puan | Gerekçe |
|---|---|---|
| 1 Anlaşılırlık | 7,5 | Yazı okunuyor. Görsel 168'de "ağlayan bir göz" olarak okunuyor, ama:<br>• Göz levhasının tırtıklı üst kenarı (x 130–670, y 70–110) ve dört bir yandaki tırtıklar küçük boyda **posta pulu** gibi duruyor.<br>• Yatay tarama 168'de "tarama çizgili, bozuk ekran görüntüsü" gibi okunuyor.<br>• Kimin gözü olduğu görselden çıkmıyor (kanat, boynuz, saç yok); bütün yükü yazı taşıyor.<br>• Gözün altındaki çapraz bant (y 450–600) kol olduğu belli olmadığı için sargı ya da maske gibi duruyor. |
| 2 Merak | 8,5 | Çelişki güçlü: "Şeytan ağlar mı?" Tek başına en çok tıklatan fikir bu. 1 numaralı başlıkla "Şeytan" kelimesi iki kez geçiyor. 2 numaralı başlıkla ("Ben Cehennemim") iki ayrı vaat veriyor, dağınık. |
| 3 Vaat ve tutma | **6,0** | Vaat 22:44'te ("Bir damla yaş") karşılanıyor. İlk 5 saniyede ne göz ne gözyaşı var; açılış güneşin önündeki figürle başlıyor. Kanalın kendi dersi (Sisifos: "NEDEN GÜLÜYOR?" kapağı farklı bir sahneyle açılıyordu ve kayıp ilk 10–15 saniyedeydi) burada tekrar ediliyor. "Test ve karşılaştır" izlenme süresi payına baktığı için bu kapak tıklama kazansa bile testi kaybetme riski yüksek. |
| 4 Ayrışma | 8,0 | Tek renk vurgusu olarak mavi gözyaşı iyi. Açık temada koyu kutu ayrışıyor. Koyu temada kapak zeminle birleşiyor (`akis_koyu.jpg`, sağ sütunda 5. sıra). A'dan net biçimde farklı; iki ayrı fikri test ediyor. |
| 5 Kelime | **6,0** | **Dinî vaaz çağrışımıyla çakışma.** Türk YouTube'unda "şeytan ağlar / şeytanı ağlatan amel" yaygın bir vaaz kalıbı. Kaynağı, secde ayetinde secde edildiğinde şeytanın ağlayarak uzaklaştığını anlatan hadis (Müslim, İman). "ŞEYTAN AĞLADI" akışta bu türün kapağı gibi okunabilir. İki sonucu var:<br>(a) yanlış kitle tıklar, ilk saniyelerde gravür ve Milton'ı görünce çıkar (tutma düşer);<br>(b) videonun "dinî karşılaştırma yapmıyoruz, edebi okuma" çizgisine ters bir ilk izlenim verir.<br>Ayrıca "-DI" ile biten olay bildirimi magazin ya da "son dakika" tonunda. YouTube'un sınırlama riskini düşük görüyorum; kelimenin kendisi politika ihlali değil. |
| 6 Rozet, yazı, odak | 7,5 | Yazı %18,5, rozet bölgesi boş, kenar boşlukları iyi. **Odak bölünüyor:** en parlak yer yazı (253) ve göz akı. Gözyaşı çevresinden yalnız 15 birim parlak; gri testte neredeyse kayboluyor. Ölçü olarak gözyaşı küçük (≈ 50×165 px). |

Ağırlıklı toplam: 1,88 + 1,70 + 1,20 + 1,20 + 0,60 + 0,75 = **7,3**

---

## Sıralı düzeltme listesi

### A (önce bunlar; A yayına en yakın aday)
1. **Alevi tek ve en güçlü odak yap.** Alev şu an x ≈ 950–1070, y ≈ 270–410.
   - Boyutu ≈ %35 büyüt.
   - İçine sıcak bir çekirdek koy: sarı-beyaz, parlaklık 230 ve üstü.
   - Etrafına figürün karası üzerinde ince bir turuncu ışıma ver (yarıçap ≈ 40 px).

   Hedef: 168'de ilk bakışta göz alevden başlasın.
2. **Haleyi ve sol zemini ≈ %10 karart ya da hafifçe vinyetle**, alevin yanında en parlak alan kalmasın.
   - Hale: x 900–1280, y 80–620.
   - Sol zemin: x 0–800.
3. **Köşe bulut parçalarını kaldır** (x 0–230 ve 1010–1280, y 0–66). `cerceve_1_bulut_0` sürümü zaten bunu yapıyor; 168'de kesik leke gibi duruyorlar.
4. **Açık tema için ince koyu çerçeve kullan** (`kapak_a_cerceve.jpg` yönü): 1280 düzleminde 6–8 px, renk #1a1714 dolayı. Açık akışta kapağın kenarını geri getirir. Koyu temada zararı yok.
5. **Figüre duygu ver** (sanat yönetmenine öneri). Baş x ≈ 985–1025, y ≈ 185–240.
   - Başı 10–15° öne ve yana eğ.
   - Ellerin alevi "tutuyor" değil "göğsünü kavrıyor" gibi okunmasını sağla.

   "Ben cehennemim" bir acı cümlesi; şu anki dimdik, simetrik duruş heykel gibi. Kanal dersi: duygu 168 px'te okunmalı. Yüzsüzlük kabul edilebilir, ama duygu duruştan okunmalı.
6. **Yazının rengi siyah kalsın.** `yazirenk` (CEHENNEMİM turuncu) sürümünü teste sokmuyorum:
   - turuncu yazı ikinci bir renk odağı yaratıp alevle yarışıyor;
   - kâğıt zemin üzerinde parlaklık farkını düşürüyor (gri testte zayıflıyor).
7. Yazıyı ≈ %4 büyüt (harf yüksekliği ≈ 135 px, %18,8). Sol kenar x 47'de kalabilir. Sağda kanatla en az 30 px boşluk kalmalı; şu an ≈ 60 px var, buna yer var.

### B (aynı fikirle teste girecekse)
1. **Kelimeyi değiştir.** "ŞEYTAN AĞLADI" yerine öneriler:
   - **"PİŞMAN MIYDI?"**: ilk tercihim. Yazıda Şeytan geçmiyor, ama gözyaşı ve başlıktaki "Şeytan" kelimesi bunu taşıyor. Vaaz kalıbıyla çakışmıyor. Filmin son sorusuyla aynı.
   - **"ŞEYTAN PİŞMAN MI?"**: daha açık ama 3 kelime ve iki satırda daha küçük harf demek.
   - **"GURUR MU, PİŞMANLIK MI?"**: anlamca en doğrusu, ama küçük boy için uzun.

   Neden "pişman"? Açılıştaki Nifates iç konuşması ("Hangi yana kaçsam cehennem…") tam olarak pişmanlık ile gurur arasındaki çatışma. Bu yüzden "pişman mı?" vaadi ilk saniyelerde temada karşılanıyor; "ağladı" vaadi yalnız 22:44'te karşılanıyor. 3. ve 5. ölçütü aynı anda düzeltir.
2. **Pul görüntüsünü kır.** Göz levhasının tırtıklı üst ve yan kenarlarını (x 60–735, y 70–600) yumuşak, düzensiz bir karanlığa erit; kare çerçeve hissi kalmasın.
3. **Gözü büyüt ve kırp.** Göz şu an x ≈ 200–640, y ≈ 250–360. Göz ≈ 560 px genişliğe çıksın, kaş ve gözyaşı kadrajda kalsın. Altındaki belirsiz çapraz bandı (y 450–600) kaldır ya da açıkça kol/kanat yap.
4. **Gözyaşını en parlak nokta yap.** Gözyaşı şu an x 490–540, y 380–545.
   - Boyutu ≈ 1,5 kat büyüt.
   - İçine beyaz bir ışık ver; parlaklık ≥ 240, çevreyle en az 80 birim fark.
   - Yazıyı #EDE6D8'den ≈ #CFC7B8'e indir (≈ 205); gözyaşı yazıdan parlak kalsın.
5. **İlk 5 saniyede vaadi karşıla** (kurgu kararı, başkana). Bu kapak teste girecekse açılışa 1–1,5 sn'lik bir gözyaşı ara kesmesi ya da tek bir cümle eklensin. Örnek: "Ben cehennemim." cümlesinden hemen sonra gözyaşının ilk karesi. Bu yapılmazsa B izlenme süresi payında kaybeder ve kanala yanlış sinyal verir.

## Başlık eşleştirmesi
| Başlık | A ile | B ("ŞEYTAN AĞLADI") ile | B′ ("PİŞMAN MIYDI?") ile |
|---|---|---|---|
| 1. `Kayıp Cennet: Şeytan Cehennemden Neden Kaçamadı? \| John Milton` | **En iyi.** Başlık soruyor, kapak cevabın ipucunu veriyor ("çünkü kendisi cehennem"). | "Şeytan" iki kez geçiyor; iki ayrı soru. | İyi: iki soru aynı damarda (kaçamadı / pişman mı). |
| 2. `Milton'ın Şeytanı: "Ben Cehennemim" \| Kayıp Cennet` | Kapak yazısını tekrar ediyor; merak boşluğu kapanıyor. Kötü. | Tamamlıyor ama dağınık (biri alıntı, biri olay). | Orta. |
| 3. `Kör Bir Şairin Cehennemi: Kayıp Cennet'te Şeytan'ın Düşüşü` | Odağı ikiye bölüyor (şair mi, Şeytan mı); "düşüş" bilinen bir şey, soru doğurmuyor. | Zayıf. | Zayıf. |

- **Öneri:** başlık 1. Test sürerken başlık sabit kalacağı için bütün kapaklarla çalışan başlığı seçmek gerekiyor; o da 1.
- **Küçük iyileştirme:** "| John Milton" yerine "| Milton" yaz. Kısalır, mobilde kesilme noktası öne gelir. Kesilme noktası 1080 genişlikte ≈ 55–60 karakter, başlık 62 karakter. "Kayıp Cennet:" başta olduğu için kesilse de anahtar kelime görünür.
- **Alternatif başlık:** `Kayıp Cennet: Şeytan Neden Geri Dönemedi? | Milton`. "Dönemedi" pişmanlık temasına daha yakın; "kaçamadı" ise A'nın cevabıyla daha iyi eşleşiyor. Yine de 1'i öneriyorum.
- **Tutarsızlık:** test setindeki sahte akışta (`akis_*.jpg`) başlık "Şeytan'ın İç Yolculuğu: Milton'ın Kayıp Cennet'i". Bu başlık `youtube.md` adaylarında yok. Kurul hangi başlığa bakıyor, netleştirilmeli. Bu başlık soru doğurmuyor ve "iç yolculuk" kişisel gelişim videosu gibi okunuyor; önermiyorum.

## Test planı ("Test ve karşılaştır", 3 seçenek)
1. **A′:** A + yukarıdaki A düzeltmeleri 1–4 (5 varsa daha iyi). Kontrol ve ana aday.
2. **B′:** düzeltilmiş göz + "PİŞMAN MIYDI?". Yalnız açılışa gözyaşı ara kesmesi eklenirse girsin; eklenmezse B′ de 22:44'e kadar vaadini karşılamaz.
3. **Üçüncü seçenek (isteğe bağlı):** A′'nün koyu sürümü (`kapak_a_koyu` mantığı, alev düzeltmesiyle). Açık/koyu zemin değişkenini ayrı ölçer; koyu temalı telefonlarda A′'nün soluk okunma riskini sınar.

- Orijinal "ŞEYTAN AĞLADI"yı hassasiyet ve hukuk alanı onaylamadan teste sokmuyorum.
- Kazanan izlenme süresi payıyla seçilir. Başlık 1 sabit kalır.
- Teste B′ girmezse A′ tek başına yayınlanır. Paketleme kuralı (2–3 gün yeni dalga gelmezse yenileme) için B′ yedekte tutulur.

## Karar
- **A: 8,3, RED.** Düzeltme 1–4 ile 9,0+ beklerim; en çok getirecek olan alev odağı.
- **B: 7,3, RED.** 3. ve 5. ölçüt 7'nin altında. Kelime değişikliği ve açılış ara kesmesi olmadan yayına çıkmamalı.

## En emin olmadığım nokta
"ŞEYTAN AĞLADI"nın vaaz kalıbıyla çakışmasının gerçek büyüklüğünü bilmiyorum. Kalıbın var olduğundan eminim, ama akışta bu kapağın vaaz içeriği gibi okunup okunmayacağı gravür üslubu ve başlıktaki "Milton" ile büyük ölçüde dengelenebilir. Aynı çakışma, din tartışmasına girmek isteyenlerden ek tıklama da getirebilir. Saf TO açısından "ŞEYTAN AĞLADI" muhtemelen en çok tıklatan seçenek. Onu indirmemin gerekçesi TO değil; tutma ve yanlış kitle riski. Bu bulguyu hassasiyet okuyucusu ve başkan doğrulamalı.

İkinci belirsizlik: açık parşömen A'nın, kitlenin açık ya da koyu temada izleme oranını bilmeden, akışta ne kadar soluk kalacağı. Bunu ancak test ölçer; üçüncü seçeneği bu yüzden öneriyorum.
