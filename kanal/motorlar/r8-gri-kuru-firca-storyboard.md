# gri-kuru-firca-storyboard (r8)

Kullanıcının 25 Kasım 2026'da gönderdiği üslup örneği: gri tonlu kaba kuru fırça storyboard: masa başında tepeden ışık, gözlükleri parlayan figürler.
- Örneğin kendisi depoda yok (telif; yalnız başvuru).
- Çözümleme ve yön metni Fable'ın; yön metni ayrı bir ajanla sınandı (telif, kanal kuralları, mevcut motorlarla çakışma).

## Karar: mevcut bir motora ek
Ayrı motor gerekmiyor. Örneği taşıyan dört şeyin (ton oranı, siluet, tek biçimli ışık, kuru fırça kenarı) üçü mevcut motorlarda var; eksik olan yalnız fırça izi.

**Çakışma**
- `stanford/lib/ekran.js`: üç plakalı yapı zaten ton kütlesi (B.k), sert siluet (B.l) ve renk/ışık (B.c) ayrımını veriyor. Kâğıt modunda B.k "yumuşak mürekkep yıkaması" olarak basılıyor; kuru fırça bunun kenar davranışı olarak eklenir.
- `ran` (mürekkep): fırça ve yıkama orada da var; ayrı bir "kuru fırça motoru" onunla aynı işi ikinci kez yazar.
- `mary-stuart` (sessiz film): gri tonlu gren ve tepeden ışık orada da var.
- cinecode `ink-wash.md` ve `line-boil.md` tarifleri aynı alanı kapsıyor.

**Ek olarak yazılacak şey:** küçük bir fırça yardımcı dosyası (örneğin `lib/firca.js`, plakaya çizen üç dört işlev) ve kâğıt gölgelendiricisine bir "kuruluk" terimi. Başka videoya `ekran.js` ya da `ran` üzerinden taşınır.

**Ne zaman ayrı motora döner:** kullanıcı bütün bir videoyu bu görünümle isterse (bekleyen öneri: Zweig / Dostoyevski'de tek karar anı; *Oppenheimer*). O zaman da yeni motor değil, `ekran.js` kâğıt modunun nötr gri bir çeşidi yeter.

## Çözümleme
## r8: gri tonlu kuru fırça storyboard (3 panel, durağan görsel)

Örnek tek bir durağan görsel; kare farkı ölçümü yok. Hareketle ilgili her şey gözlem değil, öneridir. `stanford/lib/ekran.js` okundu, çalıştırılmadı.

**Palet (olcum.json, k-means, 1000×1306)**

| Küme | Hex | Pay |
|---|---|---|
| Siyah kütle | `#000000` + `#0C0C0C` + `#1B1B1B` | %44,2 |
| Koyu gri | `#2D2D2D` + `#454545` | %26,0 |
| Orta gri | `#616161` + `#9A9A9A` | %21,1 |
| Beyaz | `#F3F3F3` | %8,7 |

- Renk yok; bütün kümeler nötr gri (R=G=B).
- Beyazın %8,7'si yanıltıcı: sayfanın beyaz kenarı ve panel araları bu kümede. Panellerin içindeki gerçek beyaz gözle yaklaşık %1–2: tavan lambası, masa kenarındaki yatay çizgi, gözlük camları, ışık konisinin çekirdeği.
- Güzelliğin ilk kaynağı bu oran: karenin onda yedisi koyu, beyaz yalnız üç dört noktada ve hep bir "bakış" ya da "ışık kaynağı" olarak.

**Çizgi**
- Kontur yok denecek kadar az. Biçimi çizgi değil, koyu kütlenin kenarı kuruyor.
- Çizgi olan yerde (orta paneldeki ceket kıvrımları, sandalye) 1–3 px, siyah, hızlı, ucu sivrilen, üst üste binen eskiz çizgisi; kapalı kontur değil.
- Kütle kenarları iki türlü: ışığa bakan kenar sert ve düz, ışıktan kaçan kenar kuru fırça gibi saçaklı.

**Dolgu ve gölge**
- Figürde 3 ton: siyah gölge kütlesi, koyu gri orta ton, açık gri ışık alan yüzey. Ara geçiş yok, tonlar düz lekeler.
- Mekânda yumuşak geçiş yalnız duvarda ve zeminde, geniş bir gri yıkama olarak.

**Işık biçimi**
- Panel 1: arkadan ışık. Zemin ve tavan lambası parlak, figürler önünde tam siluet; siluetin içindeki tek ayrıntı gözlük parıltısı.
- Panel 2: tepeden gelen çapraz ışık konisi. Koninin bir kenarı cetvelle çekilmiş gibi sert, öteki kenarı griye eriyor. Koni masadaki beyaz çizgide bitiyor.
- Panel 3: masanın üstünde yatay, sert, saf beyaz bant; yüzler alttan ve yandan aydınlanıyor, göz çukurları siyah.

**Doku ve gren**
- Orta tonlarda ince, eş dağılımlı gren.
- Düşey sürtme izleri: koyu kütlelerin alt kenarından aşağı sarkan, 1–4 px genişlikte, 40–300 px boyunda, aralıklı düşey çizgiler (panel 1'de zemin yansıması ve kapı pervazları, panel 2'de sağdaki palto).
- Yatay sürtme: masa üstünde ve panel kenarlarında, kıl izleri görünen uzun yatay darbeler.
- Kütlelerin içinde fırçanın kuruduğu yerde alttaki gri görünüyor.

**Figür kuruluşu**
- Gerçekçi oran, yaklaşık 7–7,5 baş.
- Panel 1'de yüz yok: siluet ve gözlük.
- Panel 2 ve 3'te yüz çizilmiş (kaş kemeri, burun gölgesi, ağız çizgisi), ama gözler ya siyah çukur ya beyaz cam. Bakış hiç görünmüyor.
- Eller kaba leke; parmak ayrımı yok.

**Kompozisyon**
- Geniş, sinemaskop oranlı paneller (yaklaşık 2,35:1).
- Panel 1 simetrik tek kaçış noktası; figür grubu merkezde, iki yanda siyah kapı kütleleri çerçeve.
- Panel 2 ve 3'te masa ön planda yatay bir bariyer; arkası dönük koyu figür kadrajın sağını kapatıyor (omuz üstü).
- Odak her panelde en parlak nokta ile aynı yerde.

**Hareket (öneri)**
- Mekân ve kütle sabit tutulur; yalnız kütle kenarındaki saçak ve sürtme izleri 4 karede bir tohum değiştirir (30 fps'te ~7,5 çizim/sn "kaynama").
- Ara kare ve smear gerekmez; hareketi figür değil ışık taşır: koninin açılması, lambanın titremesi, parıltının yanması.
- Kamera: yavaş yaklaşma ve masa boyunca yatay kayma.
- Bütün karede gren kaynatmak dosyayı şişirir (Kafka dersi); kaynama yalnız kenar bandında kalmalı.

**Kodla yapılabilirlik**

| Parça | Zorluk | Neden |
|---|---|---|
| Ton dağılımı, siluet, arkadan ışık | Kolay | Kanalın güçlü yanı; düz yol dolgusu |
| Işık konisi | Kolay | Bir yamuk + tek yönlü gradyan; bir kenar sert kırpma |
| Sert beyaz masa çizgisi, gözlük parıltısı | Kolay | Düz dikdörtgen ve elips |
| Kuru fırça saçağı, düşey sürtme | Orta | Tohumlu, yöne bağlı gürültü: gölgelendiricide iki `vn` çağrısı ya da tuvalde tohumlu ince dikdörtgen demeti; SwiftShader'da ucuz |
| Eskiz çizgisi | Orta | Tohumlu titrek çoklu çizgi; `cizim` becerisindeki Rough.js yaklaşımı yeter |
| Panel 2–3'teki yüzler, kumaş kıvrımı, eller | Zor / yapılmamalı | Örneğin çekiciliğinin yarısı çizerin el anatomisi; kodla taklidi karikatüre düşer. Stanford'da zaten yüz yok |

**Kısaca neyi güzel yapıyor:** az beyaz, çok siyah; kenarın bir yanı sert bir yanı saçaklı; ışık hep tek biçim (koni, bant, nokta); bakış yerine parıltı.

## Hukuk
**Risk düşük, şu koşullarla:**

- **Kaynak belirsiz.** Görsel profesyonel bir storyboard çizerinin işine benziyor; bir filmin yapım malzemesi olabilir. Kimin olduğu bilinmiyor. Videoya, kapağa ve depoya girmez; yalnız başvuru olarak kalır.
- **Üslup korunmaz, kompozisyon korunur.** Gri ton, kuru fırça, tepeden ışık, gözlük parıltısı ortak sinema dili (kara film, storyboard geleneği); alınabilir. Üç panelin belirli kadrajı (dört figürün koridordan simetrik gelişi, masa + ayaktaki adam + omuz üstü palto dizilişi) birebir kurulmaz.
- **Çizer imzası.** Fırça darbelerinin kendine özgü ritmi elle taklit edilmez; bizdeki iz tohumlu gürültüden çıkar ve zaten farklı görünür. "Şu çizerin tarzında" diye künye ya da açıklama yazılmaz.
- **Karakter ve eser.** Örnekteki üniformalı figürler bir filmin karakterleri olabilir; hiçbiri alınmıyor.
- **Stanford'un kendi hukuku ayrı ve değişmiyor.** Yaşayan kişiler (Eshelman, Mark, Jaffe, Maslach, Ramsay) yüzsüz siluet ve numarayla kalır. Örnekteki gibi çizilmiş yüz, kişiye benzetme riskini geri getirir; alınmaz. Zimbardo arşivi telifli, depoya kopyalanmaz.
- **Hassasiyet (hukuk değil ama engelleyici).** Kask ve kol arması Alman askeri okuması; sorgu mizanseni yaşayan bir kişi hakkında görüntüyle hüküm (kişilik hakkı ve yönün "hüküm verme" yasağı). İkisi de alınmıyor.
- **5816 ve bayrak:** ilgisiz.

## Stanford için notu (kismen)
Kısmen uygun: ışık, ton oranı ve fırça kenarı alınır; figürlerin kimliği, yüzler ve sorgu mizanseni alınmaz. Film kuralları (§4) değişmez. Aşağıdaki değerler başlangıç önerisidir; karede denenmedi.

## Plan plan

| Plan | Alınır | Alınmaz |
|---|---|---|
| Koridor monitörü (video modu) | Panel 1'in arkadan ışığı: floresan ve zemin parlak, gardiyanlar önünde tam siluet, tek ayrıntı gözlük parıltısı. Mevcut P02 / P10 ile aynı fikir; pekiştirir | Kuru fırça. Monitörün dokusu tarama çizgisi ve gren; fırça izi "bu bir kayıt" kuralını bozar |
| Gözlem odası, bant sahnesi (kâğıt modu) | Işık konisi, masa kenarındaki sert açık çizgi, koyu oda, kuru fırça kenarı, düşey sürtme | Ayakta, elleri arkada duran adam ve başında bekleyenler |
| Belge planları | Hiçbir şey; belge okunaklı ve açık kalmalı | Koyu ton oranı |

## Gözlük kuralıyla karşılaştırma
- Örnekte parlayan gözlük masadaki otoritede. Stanford'da parıltı yalnız gardiyanın aynalı gözlüğünde ve "tek yüz öğesi".
- Müdüre ya da Mark'a parlayan cam verilirse kural sulanır ve izleyici müdürü gardiyanla karıştırır. Gözlem odasında parıltı insanda değil nesnede olmalı: teyp makarasının kenarı, VU göstergesi, masa kenarı.
- Örnekteki iki yuvarlak beyaz göz, koyu silüette "bembeyaz göz" karikatür okumasına ve iblis okumasına yakın (CLAUDE.md karikatür kuralı). `figur.js`'teki tek parça cam + küçük elips parıltı doğru; iki yuvarlak nokta yapılmaz.

## Mizansen uyarısı (hüküm vermeme yönü)
- Orta panel bir sorgu: tepeden ışık ayaktaki adamın üstünde, oturan otorite karanlıkta. Bant sahnesi böyle kurulursa görüntü, senaryonun vermediği hükmü verir ("müdür sorgucudur").
- Öneri: koni adamın değil teybin üstüne düşer; iki siluet koninin iki kenarında, eşit yükseklikte oturur.

## ekran.js kâğıt modunda kuruluş (ortak dosya; başkan değiştirir)
1. **Ton oranı.** Sahne başında B.k plakası bütünüyle `B.ton(.72)` ile doldurulur; kâğıt yalnız ışığın düştüğü yerde açılır. Hedef: koyu ≥ %60, kâğıt açıklığı ≤ %5. Kâğıdın sıcaklığı ışığın rengi olur; "gözlem odası sıcak kâğıtta" kuralı korunur.
2. **Işık konisi.** B.k'ya beyaz boyayla yamuk: tepe lambada (dar), taban masa üstünde. Dolgu tek yönlü doğrusal gradyan (bir kenarda `#fff`, öteki kenarda `B.ton(.55)`). Sert kenar düz yol; yumuşak kenar boyunca 20–30 kuru fırça darbesi. `destination-out` yok; silme beyaz boyayla (dosyanın kendi uyarısı).
3. **Masa çizgisi.** B.l'ye beyaz boyayla 6–10 px yüksekliğinde tek yatay dikdörtgen; ucu 3–4 parçaya kırılır. Karenin en açık yeri burası ve teyp olur.
4. **Kuru fırça, gölgelendirici.** Kâğıt dalında `dK` hesabından sonra yöne bağlı bir terim:
   - `float kil = vn(vec2(fc.x / (1.8*rs), fc.y / (260.*rs)) + 11.);` (düşey kıl)
   - `dK *= smoothstep(.0, .35, dK - (1. - kuru) * 0. + (kil - .5) * kuru * (1. - dK) * 2.);` biçiminde bir eşik: tam koyu yerde etkisiz, orta yoğunlukta kütleyi düşey şeritlere böler.
   - Yeni uniform `kuru` (0..1); `o.kuru` ile sahneden verilir, varsayılan 0. Böylece mevcut kâğıt planları değişmez.
   - Kütle kenarını saçaklamak için siluet B.k'ya çizilmeden önce düşük çözünürlüklü tuvalde 6–8 px yumuşatılır (Canvas `filter: blur` pahalı; küçük tuval + büyütme). Eşik yumuşak kenarı kıl kıl keser.
5. **Düşey sürtme, tuval.** `firca.surtme(g, x0, x1, y, tohum)`: koyu kütlenin alt kenarından aşağı tohumlu 30–60 ince dikdörtgen (genişlik 1–4 px, boy 40–300 px, alfa .4–.9). Açık olanlar aynı işlevin beyaz boyayla çağrılmasıdır. `Math.random` yok, tohumlu gürültü.
6. **Figür.** B.l'de siyah siluet (mevcut `FIG.kisi`). Işığa bakan yana B.k'da tek orta ton leke (`B.ton(.45)`), sert kenarlı. Yüz yok, kapalı kontur yok.
7. **Gren ve kaynama.** Kâğıt modunda `dK` greni .05; orta tonda .08'e çıkarılabilir. Tohum yalnız kenar bandında 4 karede bir değişir; bütün karede kaynatılmaz (dosya boyu).

## Alınmayacaklar ve hassasiyet
- Kask, tüfek, askı kayışı, apolet, kol arması, uzun palto: hiçbiri. Gardiyan haki gömlek, cop, aynalı gözlük; şapka ve rütbe yok (§3'teki Türk polisi / askeri yasağı).
- Örnekteki kask biçimi ve koldaki T / haç benzeri arma İkinci Dünya Savaşı Alman askeri okuması verir; bu çağrışım Stanford'a taşınırsa film "gardiyan = Nazi" hükmünü verir.
- Koyu, tepeden ışıklı odada ayakta eli arkada figür işkence / sorgu okunur. Mark'ın görüşmesi öyle çizilmez.
- Koyu oda ve fırça eklenen her plan tam boy karede yeniden taranır (düzeltme yeni simge üretebilir: koni + masa "sunak", düşey sürtmeler "parmaklık" okunabilir. Parmaklık okuması burada işe de yarayabilir; karar başkanın).

## Kapsam önerisi
Filmin tamamına değil, III. bölümdeki ters açıya (bant çalarken ilk kez görünen masa) ve en fazla 2–3 plana. Görüntünün ilk kez "döndüğü" an koyu oda + koniyle ayrışırsa kural güçlenir. Her kâğıt planına yayılırsa belge planlarıyla ayrım kaybolur.
