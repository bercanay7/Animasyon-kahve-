# manken-cizim: geriye bakış (26 Kasım 2026)

## Başvurular
- Yön metnindeki r8 ve r1 görselleri bu oturuma eklenmedi. Kullanıcı vekil seçimini başkana bıraktı (kullanıcının yeni gönderdiği Pinterest örneklerinden):
  - r8 vekili: satranç taşları ve kırmızı koltuk (karanlık kütleler, gren, arkadan sert ışık);
  - r1 vekili: merdiven ve çerçeveler (çapraz sert ışık kaması, düz dolgu);
  - yardımcı başvuru: gri storyboard (yalnız yakın plan yüz düzlemleri için).
- Çözümleme metinleri depoda: `kanal/motorlar/r8-gri-kuru-firca-storyboard.md`, `r1-hardal-noir-cizgi-roman.md`. Ölçüler (ton oranı, üç ton, beyaz yalnız 3–4 noktada) oradan alındı.
- Görseller depoya ve videoya girmedi; yan yana karşılaştırma yalnız geçici klasörde yapıldı.

## Lisans kapısı
- Quaternius (insan paketleri CC0) ve MakeHuman (çıktı ve paket varlıkları CC0) ham metinden doğrulandı (`araclar/ASSETS.md`).
- **Yine de manken kodla kuruldu.** Gerekçeler:
  - Hazır bir model iskelet giydirme ve dışa aktarım hattı ister (glTF okuyucu, ağırlıklı deri, yeniden hedefleme).
  - Pürüzsüz model yüzü "vitrin mankeni" okumasına daha yakın.
  - Kodla kurulan baş, düzlemi biz seçtiğimiz için üsluba daha uygun.
- three.js de alınmadı: üç geçişlik zincir düz WebGL2'de 500 satır. SwiftShader maliyetini de satır satır görüyoruz.

## Üslup kapısı: koşullu geçti
Kareler `deneme.html` (25 sn): manzara, orta plan ve 15 sn hareket, yakın plan. Her biri vekil başvurularla yan yana tam boy bakıldı.

**Geçen**
- **Manzara:**
  - kara bina kütleleri, koyu gri gök, düz direkli lambanın sert ışık havuzu ve içinden geçen tek siluet;
  - lambanın cepheye düşen "çan" biçimli orta tonu;
  - r8'in ton oranı tuttu (karenin onda yedisi koyu, beyaz yalnız ışık lekesi).
- **Orta plan ve hareket:**
  - pencereden giren ışık kamaları yerde sert dikdörtgenler;
  - figür karanlıktan ışığa yürür, durur, masaya döner (ayaklar sırayla kalkar), hazırlıkla eğilir (önce hafif doğrulma, sonra yayla aşıp oturma), okur, başını kaldırıp pencereye bakar;
  - figür koyu siluet olarak okunuyor.
- **Doku yüzmüyor:**
  - fırça nesne uzayında; kamera ya da figür kayınca yüzeye yapışık gidiyor;
  - tohum iki karede bir değişiyor ve yalnız eşik kenarında görünüyor.
- **Hareket ağırlıklı:** figür ikişer çiziliyor (15 çizim/sn), eğilme ve baş kaldırma yayla (aşma ve oturma), kalça basışta iniyor.
- **Ayak kaymıyor:** `test.js`, kararlı yürüyüşte basan ayak 3B'de de sabit (2B ölçütüyle aynı; 6 yön ve tip).

**Sınırlı (kural olarak yazıldı)**
- **Yüz:**
  - Önden tam ışıkta figür ressam mankeni gibi duruyor (`?poz=dur`).
  - ¾ gölgede (ışık yanı düzlemli, gölge yanı karanlığa karışan) ve profil siluetinde okunuyor.
  - r8'in elle çizilmiş yüzlerinin ifadesine yaklaşmıyor; kodun sınırı bu. Kural: yüz önden tam ışıkta gösterilmez.
- **El:** eldiven gibi kaba leke (r8'de de "parmak ayrımı yok"); yakın planda el kadrajın dışında tutulur.

**Açık kalan (başkanın notu, engelleyici değil)**
- **Başlama ve durma rampası:** çözücünün `go < 1` karışımı basan ayağı kare başına en çok 1 cm kaydırıyor (2B'de de var; `test.js` bilgi satırı). Şeritte göze batmadı. Yakın planda yürüyüş başlatılacaksa ayrıca bakılmalı.
- **Kontur** neredeyse görünmüyor (yalnız ışıklı yanda iki basamak atlayan sınırda). r8'e uygun, ama r1 gibi çizgili bir üslup istenirse güçlendirilmeli.
- **Kuru fırça izi duvarda "ahşap damarı / yağmur" gibi okunabilir;** `kuru` ile azaltılır.

**Başarısızlık ölçütleri tek tek**

| Ölçüt | Sonuç |
|---|---|
| 3B oyun ya da ön izleme render'ı gibi | İlk sürümde düz duvarlar yüzünden evet. Orta tonda nesne uzayında kıl izi ve saçak eklenince belirgin biçimde azaldı. Manzarada hayır |
| Yüz vitrin mankeni | Önden ışıkta evet → kural: yalnız ¾ gölge ya da profil |
| Hareket fazla pürüzsüz, ağırlıksız | İkişer çizim + yay ile hayır; kol sallanması hâlâ az |
| Doku figürün üstünde yüzüyor | Hayır (nesne uzayı) |
| Figür koyu siluet okunmuyor | Okunuyor |

## Hassasiyet taraması (ilk karede başladı, her düzeltmeden sonra tam boy yeniden)
- **Sorgu masası:** masanın tepesinde lamba yok, karşısında kimse yok. Işık pencereden gelir; masa çalışma masasıdır.
- **Sıra hâlinde üniformalı siluet yok** (tek figür, deneme sahnesinin kuralı).
- **L kollu, sarkan lambalı sokak direği** darağacı okunur; düz direk kullanıldı.
- **Pencere kayıtları (bir dikey + bir yatay)** yerde haç biçiminde koyu gölge bırakıyordu. Yalnız iki dikey kayda indirildi; yeniden bakıldı, kamalar şerit.
- **Gözlük:**
  - opak koyu cam güneş ya da aynalı gözlük okunuyordu → ince çerçeve, cam yalnız parıltı;
  - ayna simetrik parıltılar "/ \" biçiminde öfkeli kaş gibiydi → iki camda aynı yönde, kısa, sıcak.
- **Kuru fırça saçağı** ilk sürümde uzun ve düzenliydi: damlayan boya, kan okunabilirdi. Kısaltıldı ve seyreltildi.
- **İlk düzlemli baş** önden siyah göz delikli bembeyaz maske gibiydi ("bembeyaz yüz + siyah göz" okuması). Ten tonu orta griye çekildi, baş yeniden kuruldu.
- **Poz kütüphanesi** (`dur`, `egil`, `oku`): havaya kalkmış düz kol yok, alna giden el yok (`test.js` bileğin omuzun altında olduğunu ölçer), sıra hâlinde eğilen figür yok.
- **Alt bant:** `alt_bant.js` sahne boyunca bütün yazı çağrılarını ölçtü; deneme sahnesinde yazı yok (sonuç aşağıda).

## Ölçümler
- **Tek işçide kare:** 0,17–0,35 sn (ilk kare derlemeyle 0,3–0,47). Bütçe 1 sn; Çernobil 0,5 sn.
- **Dört işçi (4 çekirdek paylaşımlı):** 0,9 sn/kare, 2,9 kare/sn duvar saati.
- 15 kare/sn'ye gerek kalmadı; gerekirse `olcek: .75` ve `smN: 512`.

## Dersler
- **Eşik ve ışıksız yüzey:** ışıksız yüzeyin değeri (ton × ortam) bir basamak eşiğinin dibine düşerse fırça gürültüsü yüzeyi karlandırır (TV karı, kamuflaj). Fırça eşik bozmayı yalnız ışık alan bölgede yapar. Işıksız kütleye doku, eşiği değiştirmeyen ayrı bir koyulaştırma (B kanalı) olarak verilir.
- **Yön ışığında gölge sapması** derinlik birimindedir: 0,004 × 40 m = 16 cm. Burun ve kaş gölgesini yok ediyordu. Sapma dünya biriminde verilir.
- **Işık noktası bir kutunun içinde kalırsa** gölge haritası her şeyi karartır. Lamba başı ve direk `golgeYok`; bina kütlesi ışığın arkasında kalmalı.
- **Yön ışığında gölge haritasının dışı** aydınlık sayılırsa sahnenin kenarında sahte ışık lekesi çıkar. Dışarısı gölgedir (duvarlar ışığı zaten keser).
- **Az dilimli düz gölgeli baş** gölge sınırında basamak basamak "oyun" kırığı yapar. Yeterli çözünürlük (36×28) + yumuşak normal + sert basamak + fırça kenarı düzlemi daha iyi verir.
- **Okuyan figürün yüzü 60°'den fazla aşağı bakar.** Yakın planda kamera başın tepesini görür; yakın plan baş kalkınca kurulur.
