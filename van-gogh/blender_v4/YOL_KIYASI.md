# Yol kıyası: kod mu, Blender mı, ikisi birden mi? (28 Kasım 2026)

Kullanıcının sorusu: "Blender işi çok oyun gibi gözüktü; bizimki daha sanatsal ve orijinal bir işti. Kod ile Blender'ı kıyaslayın, kod + Blender sistemini de değerlendirin."

Girdi: dört mercekten görüş (sanat yönetimi, paketleme/izleyici, üretim/hassasiyet, kare eleştirisi). Başkanın kendi bakışı: v3 G02_yakin, v3 A01, v3 C05, v4 G02_75, oda_karma, hibrit g02_gri tam boyda açıldı. Mercek iddiaları bu karelerde doğrulandı.

## Karar
**Y4: dünya kodla kalır, figürler Blender'dan gelir, motor ikisini de darbeye çevirir.** Dört mercek de birinci sıraya bunu koydu.

- Blender sahnede değil, kulisin arkasında çalışır. Figürün biçimini, elini, giysi kıvrımını, hareketini ve ışık bilgisini verir. Rengi ve fırçayı motor koyar.
- Y1 ayrı bir yol değil, Y4'ün geri dönüş yoludur. Kapı geçmezse Y1'e dönülür ve figür yakın plandan çıkarılır.
- Bu filmde yayına girmeyenler:
  - Y2 saf Blender;
  - Y3 tam hat (Blender karesi üstüne filtre);
  - Y5 NPR/toon.
- Y5 bir sonraki videonun üslup kapısında, takvim baskısı yokken ayrı deney olarak sınanabilir.

## Neden (karelerde görülen)
- **Kavram yalnız aynı malzemede çalışıyor.** "Dünya gri, yalnız Vincent'in tabloları renkli" fikri, dünya ile tablo aynı boyadan yapılınca bir uyanış gibi okunuyor (v3 A01, F04). Gerçekçi odada ise tablo duvara yapıştırılmış poster gibi duruyor.
- **Gri kural Blender'ın asıl üstünlüğünü zaten siliyor.** Ahşap damarı, giysi rengi ve sıcak lamba griye inince geriye ışığın hacmi ve figürün oranı kalıyor (oda_karma). Bu yüzden Blender'dan yalnız bunlar alınır.
- **"Oyun gibi" algısının nedenleri G02_75'te görülüyor:**
  - Vincent'in "mavi iş giysisi" kot pantolon ve denim gömleğe dönmüş;
  - şapka kovboy şapkası gibi;
  - eller kasık hizasında pençe gibi;
  - bebek plastik oyuncak;
  - kamera tepeden, Sims bakışı.
- **Y3 bu sorunları düzeltmiyor, taşıyor.** g02_gri'de:
  - Vincent'in yüzü şapka altında boş bir maskeye dönmüş, elleri beyaz eldiven gibi;
  - Theo'nun saç ve sakalı griden kaçmış, kahverengi kalmış;
  - kundak kefen gibi okunuyor;
  - genel görünüm uygulama filtresi.
- **Y1'in tek gerçek zaafı figür.** G02_yakin'de kil bebek gövde, sucuk kol ve boncuk dizisi gibi tırtıklı kenar var. Bu, `araclar/tablo/KILAVUZ.md`'nin kendi kuralını ("kenar darbesi spatula olur; yuvarlak uçlu kısa fırça kenarı boncuk dizisi gösterir") çiğniyor. Sorunun yarısı model, yarısı motorun kenar işçiliği.

## Görüşlerin birleştiği yerler
- Sıralamanın başı her mercekte aynı: 1. Y4, 2. Y1.
- Blender'dan **dokusuz gri kil** figür alınır, ayrı geçişlerle (normal, derinlik, nesne kimliği). Dokulu güzel render (beauty) alınmaz. Y3'ün hatası dokulu kareyi filtrelemekti.
- Giysi 1880'lerden olmalı:
  - Theo: koyu takım ya da redingot, yelek;
  - Vincent: bol kesim mavi iş ceketi (bleu de travail), alçak tepeli geniş kenarlı hasır şapka.
  - Kot, denim ve modern kesim olmaz.
- Renk örtüsü renk tonuna göre değil, **nesne kimliğine göre** seçilir. g02_gri'deki saç kaçağı buradan çıktı.
- Duvar fırçası değişmeli. Bugün her yerde aynı boyda dikey bir "yağmur" taraması; yüzeyi ve ışık havuzunu izlemiyor.
- H05 koridoru boş bir 3B kutu gibi; o da biraz oyun koridoru.
- Blender oturumuna plan plan tur değil, **tek toplu görev** gider.
- İlk sınav G02 olur: Y1'in en çok kaybettiği kare o.

## Ayrıştıkları yerler ve başkanın hükmü
| Konu | Görüşler | Hüküm |
|---|---|---|
| Y2, Y3, Y5'in sırası | İki mercek Y3'ü üçüncü, Y2'yi sonuncu koydu. Biri oda_karma yüzünden Y2'yi üçüncü yaptı, Y3'ü sona attı. Biri Y5'i sonuncu yaptı. | Pratikte fark etmiyor; üçü de bu filmde yayına girmiyor. Y2'den alınacak ders oda_karma'nın ışık hacmi ve sandalye gölgesi. |
| Blender'dan durağan oda levhası | Sanat yönetimi: 2–3 anahtar oda Blender'da gri ışık levhası olarak çizilsin, motor boyasın. Paketleme: isteğe bağlı. Üretim ve kare eleştirisi: gerek yok, kodla ışık konisi yeter. | Önce **kodla**: A01'e lamba ışık havuzu ve şövalenin duvara düşen gölgesi eklenir, GPU'suz. A01 kapıda yine düz kalırsa tek karelik gri kil levha denenir. Blender oturumunun yükü küçük tutulur. |
| Bebek (G02) | İki mercek: bebek yüzü görünmesin, kundak yandan ve göz hizasından görülsün. Kare eleştirisi: yüz ve kol görünsün, battaniye renkli ya da desenli olsun. | Renkli battaniye kurala aykırı (yalnız tablo ve zarf renkli). Kamera göz hizasında ve yandan; tepeden bakış olmaz. Desenli, kabarık kundak. Canlılık hareketle verilir: bebeğin kolu kıpırdar, Theo'nun eli kundağa değer. Yüz küçük kalır ve darbe ölçeğinde çözülür. İki figür aynı anda öne eğilmez. |
| Yakın planda yüz | Paketleme: yakın plan yüze değil ele, zarfa, tabloya gitsin. Sanat yönetimi ve kare eleştirisi: yüz yakında iri darbeyle, izlenimci. | Yakın yüz yalnız Theo'nun birkaç anahtar anında, iri darbeyle. Öteki yakın planlar el ve nesne. Vincent'in yüzü otoportrelerinden; yaşayan birine ya da *Loving Vincent* oyuncularına benzemez. |
| Tabloların fırçası | Sanat yönetimi: dünya ve tablo aynı malzeme olsun. Paketleme: tablo özgün kamu malı görselden basılsın. Kare eleştirisi: C05 ve F04'te bile Van Gogh'un kendi darbesi genel bir kıvrıma dönmüş. | Kare eleştirisi kısmen haklı. C05'te özgün darbe yönü yumuşamış ve filtreye yaklaşıyor; alt ortada anlamsız açık bir leke var. **Odadaki tablolar** özgün görselden basılır, motor yalnız kenarı yumuşatır. **Tablo dünyalarında** (C05, F04) darbe yönü kaynak tablonun akışından alınır; motorda `dir: {fn}` zaten var. C05'teki leke giderilir. |
| B03'teki boş tuvaller | Paketleme: "kimse görmedi" fikri güçlü. Öteki üçü: yer tutucu gibi. | Fikir kalır, biçim değişir: tuvaller yüzü duvara dönük üst üste yığılır, yalnız biri gri yüzüyle görünür. |
| Klip sayısı | Paketleme: 8–12. Üretim: yaklaşık 20–25 (kodda 22 klip, ~37 yerleştirme, 76 plan). | Sayı plan listesinden çıkarılır. Orta ve yakın planlar Y4'e geçer. Uzak geniş planlar kapıda ölçüsü tutarsa v3'teki gibi kalır. |
| Y4'ün darboğazı | Çoğunluk: figürün kalitesi. Kare eleştirisi: motorun kenar işçiliği. Düzelmezse iyi model de kil bebek görünür. | İkisi de doğru. Kenar düzeltmesi kapının **önkoşulu**; bulut oturumunun ilk işi. |
| İkişerli boyama | Sanat yönetimi: figür 12 kare/sn boyansın. | Motor canlı katmanı zaten iki karede bir boyuyor (15 çizim/sn). Ek iş yok. Kaynamaya karşı darbe tohumu plan başına sabitlenir. |

## Hangi plan hangi yolla
| Plan türü | Örnek | Yol |
|---|---|---|
| Tablo dünyaları | C05, F04 | Kod. Blender yok. Darbe yönü tablonun akışından. |
| Figürsüz iç ve dış setler | şehir, masa, zarf ayrıntıları | Kod. Yeni duvar ve zemin fırçası. |
| Orta ve yakın planda figür | A01, G02, B03, Jo'lu planlar | **Y4**: Blender kil figür + v3 seti. |
| Yürüyen figür | theo_louvre, H05 | Y4 + set kamerası. H05'in seti kodla yeniden kurulur: alçak yan açı, değişen çerçeve boyları, birkaç ziyaretçi silueti. |
| Uzak geniş planda figür | — | v3 klibi kalır; kapıda ölçüsü tutmazsa Y4. |

## İş bölümü
**Bilgisayardaki Blender oturumu.** Kullanım hakkı harcar, bu yüzden iki toplu görev alır.
1. **Kapı görevi:** yalnız G02 ve A01 figür klipleri (ayarlar aşağıda) ve tek rapor.
2. **Kapı geçerse, toplu klip görevi:** bir JSON klip listesi. Her klip için:
   - ad, hareket, kamera, ışık yönü, kare sayısı;
   - sözcüğe bağlı eylem zamanları (`bilgi.json`).

   Bir betik listenin hepsini gece boyunca çizer; sonunda tek rapor gelir.
- Set, eşya, oda ve renk Blender'dan gelmez.
- Yeni giysi varlıkları `lisans-kontrol` becerisinden geçer ve `araclar/ASSETS.md`'ye yazılır. MPFB/MakeHuman gövdeleri CC0.

**Bulut oturumu.** Motor, dünya ve kurgu burada.
1. **Figür katmanı:**
   - Kenar: alfa sınırında konturun teğetine uzun spatula darbesi, alfa 2 px yumuşatma. Boncuk dizisi biter.
   - Darbe yönü normal geçişinden; değer kil gölgelemesinden.
   - Ton grisaille; nesne kimliğine göre maske.
   - Darbe tohumu plan başına sabit.
2. **Dünya:**
   - Duvar, ışık havuzuna göre boyu ve yönü değişen iki üç ölçekli fırça; zemin tahtası yatay.
   - Masaya üst yüz ışığı ve kenar; düz siyah blok olmaz.
   - A01'e lamba havuzu ve şövale gölgesi.
3. **Tablolar:**
   - Odadakiler özgün kamu malı görselden.
   - C05 ve F04'te akış yönlü darbe; C05'teki leke giderilir.
4. B03 yığını, H05'in yeni seti.
5. Kurgu özeti, tam boy hassasiyet taraması, müzik, render, kapak, `yayin.md`.

## İlk deneme: kararı kesinleştirecek kareler
CLAUDE.md'deki dört parçalı üslup kapısı uygulanır:
- **manzara:** C05, akış yönlü darbeyle yeniden boyanır, Blender gerekmez;
- **orta plan figür:** A01;
- **yakın plan:** G02;
- **15 sn hareket:** G02 klibi.

**Blender ayarları (G02 ve A01):**
- **Görüntü:**
  - Cycles 32 örnek + OptiX gürültü giderme; motor darbeye çevirdiği için 160 örnek boşa gider.
  - 1920×1080, RGBA, saydam arka plan.
  - 15 çizim/sn: G02'de 15 sn ≈ 225 kare, A01'de ≈ 100 kare.
- **Malzeme:** figürün tamamında tek gri kil (taban ~0,5, pürüzlülük ~0,9, doku yok).
- **Geçişler:**
  - kil gölgeleme ve AO;
  - kamera uzayında normal;
  - derinlik;
  - nesne kimliği: Theo, Vincent, saç ve sakal, kundak, beşik ayrı;
  - zemin teması için gölge yakalayıcı.
- **Kamera:** v3 kadrajıyla eşlenir, göz hizasında. Tepeden bakış yok.
  - G02: iki kardeş ¾ arkadan; beşik yandan ve ön planda.
  - A01: Theo sırttan ¾, şövaleye bakar.
- **Işık:** set başına tek yön, klip JSON'una yazılır.
  - G02: sabah, pencere solda, duvardan yumuşak dolgu.
  - A01: sağda masadaki lamba ya da mum; solda ay ters ışığı, omuzda kontur.
- **Giysi:**
  - Vincent: bol kesim iş ceketi ve bol koyu pantolon, kot dokusu ve dar kesim yok; alçak tepeli geniş kenarlı açık hasır şapka.
  - Theo: koyu takım ve yelek. Beyaz yaka V biçiminde açık olur, kravat görünür. Siyah giyside küçük beyaz dikdörtgen papaz yakası okunur (tarama listesi).
- **Eller:** nesne tutar ya da gevşek durur; pençe pozu yok.
  - A01: Theo'nun elinde zarf.
  - G02: Vincent örtünün köşesini kaldırır; Theo'nun eli kundağa değer.

**Motor ayarları (bulutta):**
- Figür içi `maxR` setin yaklaşık %60'ı ve %100'ü, iki sürüm yan yana.
- `finish` `norm` ≈ 1.7 (KILAVUZ).

**Kapı ölçütleri (başkan bakar):**
- **Karşılaştırma düzeni:** eski v3 G02, yeni Y4 G02 ve oda_karma yan yana; tam boy, 246×138 ve 168×94.
- **Okunurluk:**
  1. El, oran ve giysi okunuyor mu? 168×94'te hâlâ insan mı?
  2. Yüz boş maskeye dönüyor mu?
- **Yerleşim:** figür sete yapıştırılmış gibi mi? Işık yönü ve ayak teması tutuyor mu?
- **Hareket:** 15 sn klipte darbe kaynıyor mu?
- **Hassasiyet taraması:** kefen, papaz yakası, pençe el, şapka okuması.
- **Seçenek:** üç kare kullanıcıya kör sıralama için gösterilebilir ("hangisi oyun gibi?"). Estetik son söz onun.

Kapı geçmezse (en geç 4. gün) Y1'e dönülür:
- motor ve dünya düzeltmeleri yine yapılır;
- figür orta ve geniş planda, ters ışıklı siluet olarak kalır (A01 bunu kanıtlıyor);
- yakın planlar el ve nesneye kayar.

## Takvim (24 gün)
- **1–3. gün:** iki iş paralel yürür.
  - Bulutta kenar, duvar ve C05 düzeltmeleri.
  - Bilgisayarda kapı görevi (iki klip).
- **4. gün:** kapı ve karar.
- **5–8. gün:** toplu klip gecesi, yerleştirme, B03 ve H05.
- **9–13. gün:** plan düzeltmeleri, kurgu özeti, tam boy tarama.
- **14–17. gün:** müzik, render (kod hattında ~9.000 çizim, 6–15 saat), kapak.
- **18–24. gün:** yayın paketi ve pay.

## Riskler
- **Yapıştırma:** 3B figür ile 2.5B setin ışık yönü ve ayak teması uyuşmazsa figür kesilip konmuş görünür. Önlem: set başına tek ışık yönü ve gölge yakalayıcı.
- **Kaynama:**
  - Durağan kare göstermez; yalnız 15 sn klipte görülür.
  - Y3'ün tam hattını eleyen neden de bu.
- **Kenar:** motor kenarı düzelmezse iyi model de kil bebek görünür. Bu yüzden kenar önkoşul.
- **Aktarım:** plakalar depoya girmiyor (RAPOR_1). Tam boy, çok geçişli PNG dizileri yüzlerce MB tutabilir. Önlem:
  - figür kutusuna kırpılmış 8 bit PNG;
  - plan başına tek arşiv;
  - geçici bir aktarım yolu. Bunu başkan kapı görevinden önce belirler.
- **Bilgisayara bağlılık:** kapı ve toplu görev için bilgisayarın açık olması ve kullanım hakkı gerekir; tek toplu görev bu yükü küçültür.
- **Hassasiyet:**
  - Theo'nun beyaz yakası;
  - bebek ve kundak (kefen);
  - pençe el;
  - şapka biçimi;
  - düzeltilen her planın yeni simge üretmesi. Düzeltilen her plan tam boy karede yeniden taranır.
- **Yeni kod:** tablonun akışından darbe yönü bir yenilik. Tutmazsa C05 ve F04 bugünkü hâliyle kalır; bu iki kare zaten filmin en iyileri arasında.
- **YouTube'un "değiştirilmiş veya yapay içerik" sorusu:** kullanıcının kararı. Figürün boyalı ve izlenimci olması gerçekçi insan sorusunu hafifletir; `yayin.md`'ye öneri olarak yazılır.

## Geri çevrilen öneriler
- **Y5 NPR/toon, bu filmde:** cel gölgeleme kullanıcının itiraz ettiği oyun dilinin kendisi. Denenmedi. Yeni bir araç zincirini 24 günde başka bir makinede oturtmak çok riskli.
- **Y3 tam hat:**
  - Her plan için Blender'da tam render gerekiyor.
  - Harekette kaynıyor.
  - Vincent'in fırçasını dünyanın fırçasıyla eşitleyip siliyor.
  - Yalnız dar biçimde, tek karelik ışık levhası olarak yedekte kalır.
- **Renkli bebek battaniyesi:** filmin renk kuralını bozar.
- **Theo'nun dünyasındaki darbelerin sonda kıvrılması (sanat yönetimi):** iyi fikir ama kapıdan sonraya, sözcüğe bağlanırsa. Bu karara girmiyor.

## Kullanıcıya iletilecek
"Haklıydın: Blender'ın ışığı iyi ama görüntü oyun gibi; kanalın imzası bizim motor. Dünyayı ve tabloları kodla tutuyorum. Blender'ı yalnız figür için kullanacağım: dönem giysili, düzgün elli insanları gri kil olarak çizip motordan geçireceğim. Dört günde G02 ve A01 ile bir sınav yapıyorum. Tutmazsa figürü siluette bırakıp v3'ü düzeltilmiş fırçayla bitiriyorum."
