# duz-vektor-yuruyus (v2)

Kullanıcının 25 Kasım 2026'da gönderdiği üslup örneği: düz vektör deve ve binici, yürüyüş döngüsü, yansıma (video 1,4 sn).
- Örneğin kendisi depoda yok (telif; yalnız başvuru).
- Çözümleme ve yön metni Fable'ın; yön metni ayrı bir ajanla sınandı (telif, kanal kuralları, mevcut motorlarla çakışma).

## Karar: mevcut bir motora ek
Bu örneği güzel yapan bir çizim tekniği değil, üç ayrı küçük şey: (1) eğriyle hızlanan, ayağı kaymayan dört ayaklı yürüyüş, (2) kontursuz, iki tonlu köşeli figür kuruluşu, (3) tek tonlu zemin yansıması. Hiçbiri yeni bir gölgelendirici, doku ya da plaka mimarisi istemiyor; motor yazmak en pahalı aşama ve burada yazılacak "motor" boş kalır.

Doğru yer:
- **Yürüyüş:** `araclar/hareket/hareket.js`'e dört ayaklı çözücü (deve, at, öküz) eklenir; `serit.js` ve `test.js` ayak kayması denetimi aynen kullanılır. Bu, kanalın her üslubuna yarar (gravürde kervan, vazoda at, mürekkepte süvari).
- **Yansıma:** figürü çevirip tek renge boyayan küçük bir yardımcı; hangi motorda olursa olsun çalışır.
- **Düz renk figür:** en yakın mevcut motor `ikaros` (serigrafi afiş: düz renk alanları) ve `orfeus` (kâğıt kesme). İkisinin de üstünde doku var; dokuyu kapatınca bu görünüm zaten çıkıyor. cinecode'da `pictogram-motion`, `swiss-motion`, `vox-explainer` tarifleri aynı aileden.

Çakışma: ikaros ile yüksek (düz dolgu, sınırlı palet), orfeus ile orta (parçalı figür). Uyarı: kontursuz açık renkli figür kanal kuralına göre "kâğıt kesme" okunur; bu örnek bunu iki tonlu yüzey ve koyu uzak bacaklarla aşıyor, ek yazılırken o kural korunmalı.

Kullanıcı bu görünümü yine de ayrı bir film üslubu olarak isterse (örneğin bir İpek Yolu ya da kervan videosu), o zaman karar üslup kapısında verilir: ikaros'un dokusuz kipi + hareket eki ile dört kare ve 15 sn çıkarılır; yetmezse motor o zaman yazılır.

## Çözümleme
## v2: düz vektör deve ve binici (1,4 sn döngü)

Kaynak dosya 800×600, 100/7 ≈ 14,3 kare/sn, 20 kare. Kareleri kendi ölçümümle de karşılaştırdım (eşik 40/255, kare çiftleri).

**Palet (olcum.json + kare sayımı)**
- Zemin tek renk: `#F1B070` çevresi. k-means'in ilk altı kümesi (`#F1B070`, `#F2B173`, `#F2B171`, `#EEAE6F`, `#F0B173`, `#F0AF72`) aynı rengin sıkıştırma titremesi; toplam pay ≈ %89.
- Yansıma: `#C38C5D` (≈ %7). Zeminin aynı tonunun koyusu, başka renk yok.
- Figür koyusu: `#753F22` (≈ %4) ve en koyu `#381008` civarı (eyer örtüsü, arka bacaklar).
- Küçük vurgular (her biri %1'in altında): gri-mavi giysi, pembe eyer bezi, kiremit başlık, beyaz yular ayrıntısı.
- Sonuç: tek sıcak ton ailesi + iki soğuk/pembe vurgu. Karenin %89'u boş zemin; güzelliğin yarısı bu boşluk.

**Çizgi:** kontur yok. Biçimler yalnız dolguyla ayrılıyor. Tek çizgi öğeleri dizgin (1–2 px, koyu kahve) ve eyer saçağı.

**Dolgu ve gölge:** her biçimde 2, en çok 3 ton; kenarlar sert, geçiş (gradyan) yok. Gölge yumuşatılmıyor, köşeli bir "yüzey" olarak kesiliyor (deve gövdesinde açık kahve + koyu kahve üçgenler). Uzak taraftaki bacaklar tek adım koyu: derinlik yalnız bununla veriliyor.

**Işık biçimi:** yönlü ışık yok. Işık duygusunu zemin yansıması veriyor: figürün düşey çevrilmiş, tek tonlu, ayrıntısız silueti; alta doğru hafif açılıyor. Zemin çizgisi çizilmemiş, yansıma zemini kuruyor.

**Doku ve gren:** yok. Görülen bantlanma dosya sıkıştırması.

**Figür kuruluşu:** tam profil. Deve köşeli çokgenlerden: boyun, gövde, dört bacak ayrı parçalar, eklemde kırılan düz kenarlar. Binicinin yüzü çizilmemiş: ten lekesi + sakal lekesi + başlık; göz, ağız, burun yok. El tek küçük leke. Figür karenin eninin ≈ %39'u, boyunun ≈ %54'ü (yansıma hariç).

**Kompozisyon:** tek figür ortada, kamera sabit, ufuk yok, arka plan nesnesi yok. Yansıma figürün altına ikinci bir kütle koyup kareyi dengeliyor.

**Hareket (20 kare tek tek)**
- 19 kare çiftinin 19'unda çizim değişiyor: bekletilen kare yok, "ikişerli" çizim değil. Parçalı iskeletin (rig) aradoldurmayla döndürülmesi; her kare ara karedir.
- olcum.json "13 kare" diyor; o daha yüksek eşiğin sonucu. Kendi sayımımda fark şöyle dalgalanıyor: 5., 9–10., 13. ve 17. karelerde düşük (≈ 3.000 piksel), aralarında yüksek (≈ 6.000–7.500). Yani yaklaşık 4 karede bir yavaşlama: ayak basışında ivme düşüyor, salınımda artıyor. Hız sabit değil, eğriyle.
- Döngü kusursuz kapanıyor: son kare ile ilk kare arasındaki fark ardışık kare farkı kadar. 1,4 sn = tam bir adım çevrimi.
- Sürtünme (smear) ve hareket bulanıklığı yok. Ezilme-uzama yok.
- İkincil hareket üç yerde: ayak basışında yerden kalkan toz öbeği (2–3 kare yaşayan küçük köşeli lekeler), kuyruk, dizgin. Binicinin başı yalnız ≈ 7 px (boyun %1,2'si) inip kalkıyor: gövde sakin, bacaklar çalışıyor.
- Kamera hareketsiz; figür yerinde yürüyor (koşu bandı), zemin kaymıyor.

**Kodla yapılabilirlik**
- Kolay: düz dolgu, köşeli iki tonlu yüzeyler, tek renk zemin, yansıma (aynı çizimi `scale(1,-1)` ile tek renge boyayıp basmak), toz öbekleri (tohumlu). Canvas 2D'de gölgelendirici bile gerekmez; SwiftShader yükü sıfıra yakın.
- Orta: dört ayaklı yürüyüş. `araclar/hareket/hareket.js` iki ayaklı çözüyor; dört ayak için faz kaydırmalı iki çift bacak + ayak kilidi yazılmalı. Deve "rahvan" yürür (aynı yandaki iki bacak birlikte); bu, at yürüyüşünden kolaydır.
- Zor: bu sadelikte hata saklanacak yer yok. Gravürde tarama, monitörde gren kusuru örter; burada eklem açısı bir derece yanlışsa görünür. Yüz zaten çizilmediği için yüz sorunu yok; el tek leke.
- Yapılamaz olan bir şey yok.

## Hukuk
- **Örneğin kendisi:** kaynağı ve çizeri belli olmayan bir döngü (büyük olasılıkla bir portfolyo sitesinden). Telifli sayılır: videoya girmez, depoya kopyalanmaz, kare olarak kapakta ya da Shorts'ta kullanılmaz.
- **Üslup serbest:** kontursuz düz vektör, köşeli iki tonlu gölge ve zemin yansıması yaygın, kimseye ait olmayan tekniklerdir. Risk birebir kopyada: aynı deve silueti, aynı binici (gri-mavi giysi, pembe eyer bezi, kiremit başlık), aynı turuncu zemin ve aynı kadraj birlikte kullanılmaz. Kendi figürümüz, kendi paletimiz çizilir.
- **Kod:** dört ayaklı yürüyüş kendi yazımımız olur; dışarıdan hazır rig ya da kütüphane alınırsa `lisans-kontrol` becerisi ve `araclar/ASSETS.md` kaydı gerekir.
- **Hassasiyet (hukuk değil ama aynı kapı):** kefiyeli, sakallı, yüzsüz binici tek başına sorun değil; ama İslam tarihiyle ilgili bir videoda yüzsüz figür "peygamber tasviri" diye okunabilir. Böyle bir konuda figür adıyla ve bağlamıyla açıkça sıradan bir kervancı olarak kurulur. Karikatür kuralı da geçerli: abartılı burun, sakal ya da başlıkla "Arap tipi" çizilmez.

## Stanford için notu (kismen)
Görünüm alınmaz: sıcak turuncu düz vektör, Stanford'un §4 kurallarıyla çelişir (bodrum yalnız siyah-beyaz monitörde, renk yalnız kayıtta ve belgede). Çöl sıcaklığı o filmin soğuk gözetim duygusunu bozar.

Teknik olarak üç şey alınır:
- **Koridor monitörü, zemin yansıması:** bodrum koridoru cilalı zemin. Gardiyan siluetinin altına çevrilmiş, tek tonlu, ayrıntısız yansıması basılır (örnekteki gibi zeminin bir ton koyusu; monitörde bir ton açığı). Zemin çizgisi çizmeden zemini kurar, sabit kameralı geniş planı doldurur ve tarama çizgileriyle iyi karışır. Sayım ve koridor yürüyüşü planlarında.
- **Yürüyüş eğrisi:** örnekte hız sabit değil, yaklaşık dört karede bir ayak basışında yavaşlıyor; üst gövde yalnız boyun %1'i kadar oynuyor. `stanford/lib/hareket.js` ile yürüyen gardiyanlarda aynı oran denetlenir: bacak çalışır, omuz ve cop sakin kalır. Sakin üst gövde gardiyanı daha tehditkâr gösterir.
- **Yüz yerine leke:** örnek yüzü üç lekeyle (ten, sakal, başlık) çözüyor ve eksik durmuyor. Stanford'da zaten "yüz yok, tek öğe aynalı gözlük parıltısı" kuralı var; bu örnek o kararın doğru olduğunu gösteriyor, eklenecek bir şey yok.

Gözlem odası, bant sahnesi ve belge planlarına bir şey alınmaz; oralar oturan figür ve nesne planı, yürüyüş ve yansıma yok.
