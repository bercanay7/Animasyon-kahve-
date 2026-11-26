# firca-noir (r5)

Kullanıcının 25 Kasım 2026'da gönderdiği üslup örneği: siyah-beyaz fırça mürekkebi noir; yağmur, şapkalı adamlar, eski araba.
- Örneğin kendisi depoda yok (telif; yalnız başvuru).
- Çözümleme ve yön metni Fable'ın; yön metni ayrı bir ajanla sınandı (telif, kanal kuralları, mevcut motorlarla çakışma).

## Karar: mevcut bir motora ek
Ayrı motor yazmaya değmez; Kafka'nın ağaç baskı hattına bir "fırça noir" modu olarak eklenir.

- **Çakışma büyük.** Kafka motoru zaten her kareyi "siyah blok + ak oyuk" maskesinden basıyor; bu örneğin iki tonlu, sert kenarlı, kontursuz yapısı aynı mimari. Ran'ın mürekkebi (ıslak, yumuşak, yüzsüz figür) ve İkaros'un serigrafisi de aynı aileden.
- **Gerçekten yeni olan üç parça**, üçü de fırça ve katman düzeyinde:
  - tüylenen gölge kenarı (oyma izinin yerine sivrilen fırça darbesi),
  - iki renkli yatık yağmur katmanı,
  - ıslak zemin yansıması ve biçim olarak çizilen ışık (far, lamba konisi).
- **Örneği güzel yapan şeyin yarısı motor değil, kompozisyon kararı:** siyah kütlelerin birbirine bağlanması ve yüzün şapka gölgesine gömülmesi. Bunlar plan listesinde verilir.
- **Kalan yarısı kodla alınamıyor:** yüz, el ve kıvrım çizimi. Yeni motor bunu çözmez.
- **Risk:** Kafka'nın `woodcut` paketine eklenirse oyma dokusu noir görünümü bozabilir; mod, baskı gürültüsünü ve oyuk izini kapatabilmeli. Kodu açıp doğrulamadım, bu bir iddia; başkan `kafka/lib` içinde bakmalı.

Bir noir konusu (dedektif, casusluk, 1940'lar) takvime girerse o zaman ayrı motor kararı yeniden tartılır; şimdilik böyle bir video yok.

## Çözümleme
**Not:** r5 tek bir durağan görsel (753×1198, dikey). Hareket ölçümü yok; hareket satırı örnekten ölçülmedi, bu üslubun kodda nasıl hareket ettirileceğine dair önerimdir.

**Palet (olcum.json)**
- Görüntü aslında iki değerli. Ara tonlar çizimde yok, taramanın ve ince taramaların ortalaması.
- Koyu küme: `#2E2B32` %29,9 + `#38363C` %9,9 + `#504E52` %6,7 = **yaklaşık %46,5**.
- Açık küme: `#E0DCDD` %20,5 + `#C1BEBF` %10,3 = **yaklaşık %30,8**.
- Ara küme: `#A5A3A4` %9,2 + `#878688` %7,3 + `#6B696C` %6,2 = **yaklaşık %22,7**. Bunlar yağmur ve fırça taramasının olduğu bölgeler; yakından bakınca siyah ve beyaz çizgidir.
- Siyah saf değil, hafif mor-gri (`#2E2B32`); kâğıt saf beyaz değil (`#E0DCDD`). Renk yok.

**Çizgi**
- Dış çizgi (kontur) neredeyse yok. Biçimi çizgi değil, siyah lekenin kenarı kuruyor.
- Fırça çizgisi kalın başlar, ince biter; uçlar sivri. Kalınlık kabaca 1–12 px arasında değişiyor (753 px genişlikte).
- Gölgenin kenarı düz kesilmiyor: aynı yöne yatık, sivrilen kısa fırça darbeleriyle "tüyleniyor" (gökyüzü, tente altı, evlerin çatısı).
- Yağmur iki renkli: açık zeminde siyah kısa çizgi, siyah zeminde beyaz çizgi ve beyaz nokta. Hepsi tek açıda, dikeyden yaklaşık 20–25 derece yatık.

**Dolgu ve gölge**
- İki ton, kenar sert. Geçiş tonu yok; yarı ton yalnız tarama sıklığıyla veriliyor.
- Siyah lekeler birbirine bağlanıyor: soldaki direk, tente, soldaki adamın sırtı ve arabanın gövdesi tek bir siyah kütle. Görüntüyü güçlü yapan asıl karar bu.
- Siyah kütlenin içinde biçim ince beyaz çizgiyle ayrılıyor (araba ızgarası, tampon, palto kıvrımı).

**Işık**
- Tek kaynak, yukarıdan ve arkadan; figürler yarı siluet. Işık bir biçim olarak çiziliyor: farın ovali, şapka siperinin altındaki bant, ıslak kaputtaki parlak şerit.
- Yerde yansıma dalgalı yatay beyaz çizgilerle verilmiş.

**Doku ve gren**
- Gren yok. Doku fırçanın kuru ucundan ve taramadan geliyor. Kâğıtta hafif tarama lekesi var.

**Figür kuruluşu**
- Yaklaşık 7 baş boyunda, gerçekçi oran. Fötr şapka ve uzun palto silueti tanımlıyor.
- Yüzler çok az çizilmiş: şapka gölgesi yüzün üst yarısını siyaha gömüyor, geriye burun, çene ve bir iki çizgi kalıyor. Bir figür tamamen arkadan.
- Eller küçük ama ayrıntılı (silah, sigara). Palto kıvrımları anatomik.

**Kompozisyon**
- Üç derinlik katmanı: önde kadrajı alttan dolduran araba (karenin alt %45'i), ortada üç figür, arkada evler ve elektrik direği.
- Sol kenarda dikey siyah direk ve ok levhası kadrajı kapatıyor; yağmurun çaprazı bütün kareyi tek yöne bağlıyor.
- En parlak yer figürlerin arkasındaki gökyüzü boşluğu; göz oraya, yani üç şapkaya gidiyor.

**Hareket (öneri, ölçüm değil)**
- Bu üslup "ikişerli" çizime uyar: çizim 2 karede bir değişir (30 kare/sn çıktıda saniyede 15 çizim), ara kare ve sürtünme kullanılmaz.
- Hareketi figür değil ortam taşır: yağmur katmanı, yansımanın titremesi, sigara dumanı, far ışığının süpürmesi, yavaş kamera yaklaşması.
- Tüylenen gölge kenarı 2–3 karede bir tohumlu olarak yeniden çizilirse el çizimi titremesi verir; her karede değişirse dosya şişer (Kafka dersi).

**Kodla yapılabilirlik**
- **Kolay:** iki tonlu eşikleme, bağlanan siyah kütleler, yatık yağmur çizgileri (siyah üstünde beyaz, beyaz üstünde siyah), far ve lamba biçimleri, yansıma çizgileri, siluet figür, şapka ve palto profili.
- **Orta:** tüylenen gölge kenarı (kenar boyunca tohumlu, sivrilen darbeler), kalından inceye fırça çizgisi, siyah kütle içinde beyaz ayırma çizgisi.
- **Zor:** palto kıvrımlarının inandırıcı çizimi, eski araba gibi eğri yüzeyli nesnede parlama şeritleri (elle Path yazmak gerekir).
- **Yapılamaz sayılır:** bu ayrıntıda yüz ve el. Örnekteki çözüm zaten yol gösteriyor: şapka gölgesi yüzü siyaha gömer, figür arkadan ya da profilden verilir.

## Hukuk
**Risk orta: üslup serbest, bu görselin kendisi değil.**

- **Kaynak belirsiz.** Çizeri ve yayını tanımlayamadım; görsel 20. yüzyıl ortası çizgi roman ya da dergi illüstrasyonuna benziyor ve büyük olasılıkla telifli. Videoya girmez, depoya kopyalanmaz, kapakta kullanılmaz.
- **Alınabilecek olan:** iki tonlu fırça mürekkebi, bağlanan siyah kütle, yatık yağmur, şapka gölgesiyle gizlenen yüz. Bunlar noir türünün ortak dili, kimsenin malı değil.
- **Alınamayacak olan:** bu kompozisyonun kendisi (soldaki ok levhası ve tente, üç adamın dizilişi, öndeki araba, arkadaki direk bir arada) ve çizerin tanınır el yazısı. Aynı sahneyi yeniden çizmek kopyadır.
- **Araba:** gerçek bir modelin ızgarasını birebir çizmek marka tasarımı riski taşır; genel bir 1940'lar silueti kullanılır.
- **İçerik:** görselde iki tabanca var. Kapakta ya da ilk karede doğrultulmuş silah YouTube'da yaş kısıtı ve reklam sınırlaması riski getirir.
- **Hassasiyet listesi:** dikey direk + yatay ok levhası birleşimi tam boy karede haç gibi okunabilir; benzer bir levha çizilirse kollar asimetrik tutulur.

## Stanford için notu (kismen)
Çizgi dokusu alınmaz, ışık ve leke düzeni alınır. Stanford'un üslup kuralları (bodrum yalnız monitörde, renk yalnız kayıtta) değişmez.

**Alınacaklar**
- **Gözlem odası (III. bölüm ters açısı):** siyah kütleleri bağla. Masa, sandalyeler ve iki araştırmacı tek bir koyu siluet olsun; biçimi yalnız monitörün ışığından gelen ince açık kenar ayırsın. Örnekteki araba–figür–direk birleşmesinin karşılığı bu.
- **Bant sahnesi:** ışığı biçim olarak çiz. Teybin kehribar lambası ve kırmızı kayıt ışığı, örnekteki far ovali gibi karenin tek parlak lekesi olsun; geri kalan siyaha gömülsün.
- **Koridor monitörü:** gardiyanlarda yüz yerine tek parlak öğe kuralı zaten var (aynalı gözlük). Örnekteki şapka gölgesi aynı işi yapıyor; gözlüğün üstünü siyaha gömüp yalnız parıltıyı bırakmak bu kuralı güçlendirir.
- **Üç katmanlı derinlik:** önde kadrajı kesen koyu bir nesne (parmaklık, kapı kasası, monitörün kenarı), ortada figür, arkada açık boşluk. Koridor planlarında denenebilir.

**Alınmayacaklar**
- **Fırça taraması ve yağmur:** monitör modunun tarama çizgisi ve yatay bulanıklığı ince taramayı ya yutar ya da hareli desen üretir.
- **Belge planları:** sıcak kâğıt ve daktilo harfi kalır; fırça mürekkebi belgeyi "çizim" gibi okutur ve "bu gerçek bir kayıt" hissini zayıflatır.
- **İçerik:** fötr, palto, silah. 1971 Kaliforniya'sına ve yaşayan kişilere uymaz; gardiyanlara gangster okuması yükler, bu da videonun hüküm vermeme yönüne aykırı.

Stanford'un motoru yazılmış durumda; bu öneriler yeni kod değil, plan düzeyinde ışık kararları.
