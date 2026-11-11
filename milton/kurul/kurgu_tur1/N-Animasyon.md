# N-Animasyon: animasyon yönetmeni (hareket merceği), ilk tam kurgu kurulu, tur 1

**Puan: 7,8 / 10 · RED**

Kareler `shot.js` ile bugünkü (son) kodla alındı. Makine boşken kare başına 0,2–0,9 sn sürdü. `.parts` ve `milton_v1.mp4` yalnız durağanlık taramasında kullanıldı (2 fps, 240 px). Hareket eğrileri ardışık kare farkından çıkarıldı: ortalama fark, değişen piksel yüzdesi (eşik 40), farkın ağırlık merkezi ve kaydırma için satır/sütun kayması.

Kare klasörü: `/tmp/claude-0/-home-user/11d2c568-95b3-5772-9108-19223f852e25/scratchpad/kurul_N-Animasyon/`
- `f/`: tek kareler (dosya adı film zamanı).
- `sheet/`: kare dizileri (`P0xx.jpg` planın tamamı, `f0xx.jpg` kritik anlar 0,1–0,2 sn aralıkla, `dif_*.jpg` fark görüntüsü kırmızıyla).
- `fd/`: her `fade` geçişinin ortası ile öncesi ve sonrası.

## 1. Ölçütler

| Ölçüt | Ağırlık | Puan | Gerekçe |
|---|---|---|---|
| Zamanlama ve kelimeye bağlama | %25 | 9,0 | Olaylar kelimeye 0–0,3 sn içinde oturuyor (ölçümler aşağıda). |
| Figür hareketi: ağırlık, ön hazırlık, takip, okunurluk | %25 | 7,4 | Çok sayıda iyi hareket var. Ama filmin kırılma anı (J07 düşüşü) ve yılana giriş (I05) ucuz okunuyor. Kalkışlarda ön hazırlık yok. |
| Kamera dili (kılavuz kuralı) | %15 | 7,6 | Bir plan %10 sınırını aşıyor. İki hızlı kaydırma tarama çizgisinde kırpışma üretiyor. 11 planda kaydırma ve yakınlaşma birlikte, 8 planda yumuşatma doğrusal. |
| Geçişler | %20 | 6,5 | 90 `fade` geçişinin 80'i ara karede gri üretiyor; en kötüsünde karenin %75'i gri. Üç değer kuralını en çok bozan şey bu. |
| Durağanlık dengesi | %15 | 7,8 | Bilinçli donmalar yerinde. Ama birkaç uzun plan "bitmemiş" duruyor (P097–P098, P107, L09 sonu, P021 başı). Gereksiz kıpırdama yok. |

Ağırlıklı toplam 7,79, yani 7,8. "Geçişler" 7'nin altında kaldığı için puan ne olursa olsun karar RED.

## 2. Engelleyici bulgular

1. **Fade geçişleri gri üretiyor (filmin geneli, 90 geçişin 80'i).** İki levha yarı saydam üst üste biniyor. Ölçüm, 80–160 arası gri piksel oranıdır. Normal levhalarda bu oran %0–3; fade ortasında:
   - P140→P141 (1503,17): %75,9
   - P135→P136 (1412,23): %75,7
   - P072→P073 (737,14): %73,7
   - P005→P006 (36,15): %73,7
   - P131→P132 (1367,38): %70,6
   - P042→P043 (425,77): %71,9
   - P043→P044 (436,87): %65,1
   - P132→P133 (1375,68): %62,7
   - P115→P116 (1192,19): %55,2. Bu, briefteki örnek.

   Toplam yaklaşık 70 sn'lik film bu hâlde. İzleyici kâğıt baskı yerine "yıkanmış fotoğraf" görüyor; özellikle açık ve koyu levha arasında. KILAVUZ "Gri, yarı saydam çizgi yok" diyor ve siyahtan açılışta saydamlığı zaten yasaklamış; plan arası geçiş aynı kurala tabi olmalı. Kareler: `fd/t1503.17.png`, `fd/t1412.23.png`, `g/t1192.00.png`, `g/t1375.70.png`, `g/t0442.50.png`.

2. **P109 (J07, filmin kırılma anı), 1109,3–1110,4.** Yer: x 520–1100, y 320–1000.
   - **Sorun 1 (biçim):** kolları gövdeye yapışmış, çizgili ve sivrilen gövde "havuç" ya da "mumya" gibi okunuyor (`sheet/f109a.jpg`).
   - **Sorun 2 (fizik):** bedenin ayakları yerde kalmıyor. Gövde ortasından dönüyor ve havada sağa kayıyor: alt uç 1109,8'de yerden kalkar, 1110,1–1110,3'te havada asılı kalır. 1110,3→1110,4 arasında tek karede yere "yapışıyor"; o karede fark 5,1, öncesinde 2,8–4,4. Çarpma, sekme ve toz yok.
   - **Sonuç:** "yüzüstü yere yığılır" anı, havada süzülüp tek karede düzleşen bir kütüğe dönüşüyor. Filmin dönüm noktasında bu kabul edilemez.

## 3. Sıralı düzeltme listesi

**1. Tüm `fade` geçişleri, ~70 sn (motordan istek, `lib/film.js` `drawFilm`).**
- **Düzeltme:** `fade` yerine gri üretmeyen bir "eşik" geçişi yazılmalı. Yeni levha önce kendi koyu kütleleriyle "basılır", sonra açıkları gelir; her piksel ya eski levhadan ya yeni levhadan gelir, hiçbir zaman ikisinin karışımı olmaz:
  - Sabit bir gürültü dokusu kullanılır: `N(x,y)`, `hash` ile 6–8 px tane, bir kez üretilir.
  - Yeni levhanın tonu L ile, kare başına şu ölçü hesaplanır: `m = 0,6·N + 0,4·L`.
  - Piksel, `m < E.sine(p)` olduğunda yeni levhadan alınır.
  - Süre 0,8–1,0 sn kalır.
- **Kısa yol:** koyuluk oranı farkı %25'i aşan çiftlerde `fade` yerine `cut` kullanılır.
- **Kazanç:** +0,8.

**2. P109 (J07) düşüş, 1109,3–1110,4; x 520–1100, y 320–1000.**
- **Düzeltme:**
  - Dönme noktası ayaklar olsun (alt uç zemin çizgisinde y ≈ 1000'de sabit).
  - Açı `E.in2` ile ivmelensin (yerçekimi); süre 0,7 sn: 1109,35 → 1110,05, yani "yığılır" 1110,10'da yerde.
  - Çarpma anında 2 kare ezilme olsun (boy %4 kısalır, en %4 genişler), ardından gövde ön ucu 6–8 px sekip `E.out2` ile 0,25 sn'de otursun. Zemine 3–4 beyaz toz vuruşu eklensin.
  - "Havuç" okumasını kırmak için:
    - Gövdedeki eğik beyaz şeritler kaldırılsın. Kolların gövdeye yapıştığını iki uzun kenar ışığı anlatsın.
    - Uç sivri koni yerine küt ve dalgalı olsun.
    - Baş, gövdeden ayrı yuvarlak top olarak değil, boyunla akan bir yılan başı olarak çizilsin.
- **Kazanç:** +0,5.

**3. P098 (I05) yılana giriş, 999,6–1002,4; tüp x 700–1100, y 330–1000.**
- **Sorun:** "duman" uçları küt, düz siyah bir hortum ya da çorap gibi; ilk kez gören izleyici "siyah bir boru yılanın ağzına emiliyor" sanıyor. Figür yukarıdan düz yatay bir kesme çizgisiyle siliniyor; 1000,6–1000,8'de kanatlar cetvelle kesilmiş gibi (`sheet/f098.jpg`).
- **Düzeltme:**
  - Tek tüp yerine 3–5 ince, sivrilen, kıvrımlı duman kolu kullanılsın. İçlerinde KILAVUZ'daki düzensiz beyaz vuruşlar olsun, uçları yırtık.
  - Figür uçlardan (kanat uçları, ayaklar) çözülsün: `erode` ile ve `noise` eşiğiyle, yatay kesme olmadan.
  - Akış `E.in2` olsun: yavaş başlasın, ağza yaklaştıkça hızlansın. Son 0,3 sn'de ağız kapanırken yılan gövdesi 1 kez kısa bir titreme (±4 px, 3 kare) yapsın; içine bir şey girdiği orada okunur.
- **Kazanç:** +0,35.

**4. P049 (E09) dikey kaydırma, 484,05–487,47; bütün kare.**
- **Ölçüm:** `camLerp` cy 830 → 1190 (360 px), 3,4 sn içinde. Tepe hızda kare başına 8 px dikey kayma var; yatay tarama aralığı 9–12 px. Ardışık karelerde pikselin %34–42'si değişiyor (`sheet/dif_p049.jpg`).
- **Sorun:** çizgiler yer yer ters yöne kayıyormuş gibi görünür ("vagon tekerleği"), ayrıca bit hızı fırlar.
- **Düzeltme:** kaydırma kaldırılsın, iki kadraj arasında "mızrağı" kelimesinde `cut` yapılsın. Ya da hız ≤ 3 px/kare olsun: aynı yol en az 8 sn ister, bu plana sığmaz.
- **Kazanç:** +0,25.

**5. P036 (D07) yatay kaydırma, 357,57–360,31.**
- **Ölçüm:** 1240 px'lik yol 2,74 sn'de, `mb: 1`. Tepe hızda kare başına 26 px (`f/t0358.87–90`); dik kenarlarda (toplar, dağlar) atlama ve takılma olur.
- **Düzeltme:** `mb: 3` verilsin ve süre 4 sn'ye çıksın: `Wd('D07','icat') - .5` → `Wd('D07','dağları') + 1.0`; tepe hız yaklaşık 15 px/kare olur.
- **Kazanç:** +0,15.

**6. P055 (E15) selam, 561,9–567; kalabalık y 620–880.**
- **Sorun:** kalabalık 5 sn boyunca tek parça hâlinde yavaşça "çöküyor" (fark 9–12/sn, düzgün). Selam değil, "batan ya da eriyen bir kütle" gibi okunuyor; dalga yönü seçilemiyor (`sheet/p055crop.jpg`).
- **Düzeltme:**
  - Sıra sıra kademelensin: tahta en yakın sıra "eğilir" 561,95'te başlasın, her sıra 0,25 sn gecikmeyle.
  - Her sıranın eğilişi 0,7 sn sürsün, `E.io2` ile; sonunda %3'lük taşma ve geri dönüş (`E.back` benzeri) olsun.
  - Mızraklar aynı anda 15–20° öne yatsın.
- **Kazanç:** +0,2.

**7. P021 (C04).**
- **Sorun 1, 198,6–206,6:** 8 sn neredeyse tam durağan (değişen piksel %0,3). "Oğulu" 202,46'da ikinci ışık için bir olay yok (201,8–203,6 farkı 0,16).
- **Düzeltme 1:** "oğulu" kelimesinde ikinci ışığın 0,8 sn'de `E.out2` ile doğması; saflarda başların 2–3 px yükselmesi (dikkat) ya da 6 sn'lik yatay kaydırma (40 px).
- **Sorun 2, 206,75–208,25:** diz çökme dalgası iyi. Ama her figür ara pozda uzun bir hamle adımı atıyor ve mızrak yatay olarak komşusuna doğrultuluyor. 207,2'de bu "saldırı" gibi okunuyor (`sheet/f021crop.jpg`, sol x 80–600, y 700–1000).
- **Düzeltme 2:** mızrak dik kalsın (çöken dizin yanında yere dayansın); ara pozda adım yarıya insin.
- **Kazanç:** +0,15.

**8. P097–P098 (I04–I05) havada duran figür, 976–999,5; x 820–1340, y 250–720.**
- **Sorun:** yaklaşık 23 sn aynı kompozisyon. Figür havada sabit, bacak kıvrık; yalnız alıntılar değişiyor. "Bitmemiş" duruyor.
- **Düzeltme:**
  - "Alçalış"ı sözle değil hareketle verin: 23 sn boyunca figür `E.io2` ile 180 px alçalsın ve kanatlar %20 kapansın.
  - "kendinden iğrenir" (978,73) kelimesinde baş 0,5 sn'de yılandan yana 15° dönsün.
  - "Yükseldiği kadar" alıntısında kısa bir yükselme olsun (40 px, 1 sn), sonra daha derine insin.
- **Kazanç:** +0,15.

**9. P033 → P034 kesmesi, 338,82; Şeytan x ≈ 560–700.**
- **Sorun:** P033 Şeytan diz çökmüşken bitiyor; P034 aynı set ve aynı ölçekte onu yeniden ayakta ve farklı yerde açıyor. İzleyici bunu "atlama, montaj hatası" diye okur.
- **Düzeltme:** iki yoldan biri: P034'ün ilk 1,5 sn'sinde Şeytan dizinden kalksın (0,8 sn, `E.io2`, kanat açılarak); ya da kesme `fade` yerine siyaha kısa bir "dip" ile verilsin (bu bölümde savaşın yeni anı olduğunu söyler).
- **Kazanç:** +0,1.

**10. Kamera kuralı ihlalleri (kod satırları).**
- %10 sınırını aşan tek plan **P073** (`kit.js:341`): z 1 → 1,16 ve cy +80, 738,0–745,2. Düzeltme: z en çok 1,10, kaydırma yok; daha yakın kadraj gerekiyorsa sahneyi o ölçekte çizip kesin.
- **P007** (`oda.js:534`): z 1,08 + kaydırma 20 px, `E.lin`, 4,68 sn; 6 sn kuralının altında. Düzeltme: yakınlaşma 1,05, kaydırma yok, `E.io2`.
- **Kaydırma ve yakınlaşma birlikte (kaydırma silinsin, yalnız z kalsın):**
  - P020 (`cen.js:87`)
  - P023 (`cen.js:173`): 7,3 sn'de 60 px + 1,08
  - P062 (`sav.js:502`)
  - P133 (`oku.js:144`)
  - P011 (`oda.js:613`)
  - P014 (`oda.js:738`)
  - P043 (`kit.js:314`)
  - P004 (`gol.js:48`): z 1,1 → 1 + 60 px. Küçük; düzeltilmesi iyi olur.
- **Doğrusal (`E.lin`) kamera, `E.sine` ya da `E.io2` olsun:**
  - P006 ve P071 (`kit.js:87`, `kit.js:325`)
  - P007, P010, P011, P014 (`oda.js`)
  - P043 (`kit.js:314`)
  - P084 (`adn.js:587`): 7,4 sn'de 260 px. Bu planlar `fade` ile girip çıktığı için ani başlama ve durma geçişte saklanıyor; ama P011 `cut` ile P012'ye geçiyor ve hareket ortasında kesiliyor.
- **Kazanç:** +0,15.

**11. P045 (E05) gölden kalkış, 443,0–445,3; figür x 700–1300, y 350–1000.**
- **Sorun:** hareket düzgün ve yumuşak (fark 2,5 → 7,6 → 6,9), ama ön hazırlık yok. Dev figür ağırlıksız bir asansör gibi yükseliyor (`sheet/f045.jpg`).
- **Düzeltme:**
  - "Kalkar" (443,01) kelimesinden önce 0,3 sn'lik çöküş: gövde 20 px aşağı, kanatlar suya bastırır.
  - Kalkış `E.io2` ile 1,6 sn sürsün.
  - Kanatlar gövdeden 0,15 sn geç açılsın (takip hareketi).
  - Suya 2–3 alev ya da damla sıçraması eklensin.
- **Kazanç:** +0,1.

**12. P140 (L09) ışığın doğuşu.**
- **Sorun:** ışığın doğuşu iyi (1489 "parla" kelimesinde nokta, 1492,3–1495,3'te 3 sn'lik yayılma). Ama 1495,3–1502,8 arasında 7,5 sn tam donuk (fark 0,00); 1481,9–1488 arası da 6 sn donuk. Doruk anı bir fotoğrafa dönüyor.
- **Düzeltme:**
  - Işınlarda yavaş "nefes" olsun: boy ±%4, 4 sn periyot, `Math.sin`. Tarama sabit kalır, yalnız ışın uçları oynar.
  - 22 sn boyunca 30 px yatay kaydırma (kurala uygun).
  - "Cehennem taşıyabileceğini" (1498,23) kelimesinde göğüste kısa bir alev titremesi; L07 ile ayna.
- **Kazanç:** +0,1.

**13. P107 (J04) bekleyiş, 1084,7–1089,7.**
- **Sorun:** 5 sn mutlak donuk (fark 0,00). İzleyici bunu "video takıldı" diye okuyabilir.
- **Düzeltme:** bekleyiş hareketle verilsin. Elmayı tutan kol 2 px titresin (6 Hz değil, 0,8 Hz yavaş salınım) ve ışık hâlesi %3 nefes alsın; "bekler" 1087,02'de baş 5° öne eğilsin.
- **Kazanç:** +0,05.

**14. P113 (J10) ağaç.**
- **Sorun:** ağaç 1150,6–1151,0 arasında büyürken tacın altı cetvel gibi düz ve köşeleri dik bir levha. 1150,6–1150,8'de "masa" ya da "mantar" gibi okunuyor (`sheet/f113a.jpg`, x 330–1450, y 380–560).
- **Düzeltme:** tacın alt kenarı ilk karesinden itibaren yumru ve sarkık olsun; taç yukarı doğru 3 bulut kümesi olarak sırayla doğsun (0,15 sn arayla, `E.out2`, %8 taşma). Plan "ağaçlar" diyor: arka planda 2 küçük ağaç daha.
- **Kazanç:** +0,05.

**15. P137 (L07).**
- **Sorun:** zincirin halka halka çizilmesi çok iyi (1444,9–1448,3, "kendi eliyle vurdu" ile örtüşüyor). Ama figür kendi zincirine hiç tepki vermiyor; ondan önceki 17 sn de (1427,8–1444,7) pratikte durağan (yalnız 25 sn'de 30 px kaydırma, saniyede 1,2 px).
- **Düzeltme:** "vurdu" (1448,19) kelimesinde son halka kapanırken baş 0,6 sn'de 8° öne düşsün, kanatlar 3–4 px içe çekilsin. "Gururu" (1449,03) kelimesinde baş yeniden kalksın: filmin son jesti olur.
- **Kazanç:** +0,05.

**Küçük not.** P002'nin ışınları `Se('A02') + .4`'e kadar sönüyor, ama plan 10,03'te P002g'ye kesiliyor. Işınlar yarıda kesiliyor: 9,90 karesinde ışınlar hâlâ var. Sönme `s1 - .9 → s1 - .05` aralığına çekilmeli.

## 4. Ölçülen ve doğru olanlar

- **Kelimeye bağlama** çok iyi; olaylar kelimeye 0–0,3 sn içinde oturuyor:
  - P047 mızrak yere 468,15'te saplanıyor ("söyler" 468,19). Kol 1,1 sn önceden kalkıyor, darbe tek karede ve kıvılcımla.
  - P034 kılıç 343,0–343,3'te iniyor ("yarar" 343,26). Darbeden sonra Şeytan büzülüyor, takip hareketi var.
  - P105 "birden belirir" 1068,6–1068,7 arasında tek karelik patlama (kelime 1068,66).
  - P021 diz dalgası "diz" kelimesinden 0,1 sn sonra soldan sağa 1,5 sn'de yayılıyor.
  - P133 damla "gözleri" kelimesiyle doğup 1385,4'te süzülüyor.
  - P001 alev "cehennemim" kelimesinden 0,2 sn önce büyümeye başlıyor.
- **Yumuşatma eğrileri temiz:**
  - P058 Günah'ın süzülüşü 590,4–592,3 arasında simetrik çan eğrisi çiziyor (tepe fark 7, iki uçta 0,3–0,5); "kadın" kelimesinden 0,2 sn önce başlıyor.
  - P075 doğrulma 757,9–759,4 arasında (fark 1,3 → 3,9 → 1,2).
  - P003 yükselişi ease-out.
- **Karanlıktan açılış:** P004'te önce gözler açılıyor ("gözlerini" 21,22), sonra 24,0–24,8'de ışıkla açılış geliyor ("yanan" 23,70). Kural birebir uygulanmış.
- **Titreme yok:** durağan bölgelerde ardışık kare farkı %0,00–0,2 (P004, P133, P137). Çizgiler kıpırdamıyor.
- **Anlatım olarak hareket:**
  - P137 zincirinin halka halka sarılması.
  - P124 merdiveninde her basamağın kendi kelimesinde belirmesi.
  - P109'da elmanın kollar yapışırken elden düşüp yerde kalması (iyi bir ayrıntı; korunmalı).

## 5. Durağanlık taraması

Kaynak `milton_v1.mp4`, 2 fps; değişen piksel %0,08'in altında kalan stretch'ler:
- 28,5 sn P142: bitiş ekranı, bilinçli.
- 11,5 sn P016 (144,5–156): sayfa levhası. Bilinçli ama uzun; 30 px kaydırma eklenebilir.
- 11 sn P137 (1427–1438): yukarıda 15. madde.
- 8,5 sn P130 (1345,5–1354).
- 8 sn P140→P141 (1495–1503).
- 7 sn P026.
- 6'şar sn: P114, P079, P141.

Shot.js ile ayrıca bulunanlar: P107 5 sn, P054 3,3 sn (553,4–556,8; kalkıştan önce, kabul edilebilir), P021 8 sn.

Gereksiz kıpırdayan, dikkat dağıtan alev, duman ya da çizgi bulmadım.

## 6. Kare çizim süresi

Makine boşken tek kare 0,2–0,9 sn sürüyor. En ağırları:
- P137 fade karesi: 0,89 sn
- K02 fade: 0,71 sn
- P021: 0,72 sn

`MB=3` ile:
- P047: 1,16 sn
- P034: 0,89 sn
- P038: 0,82 sn

1,2 sn'yi aşan plan bulmadım. (Arka planda render sürerken 1,2–1,7 sn ölçümler vardı; onlar yükten kaynaklanıyor.)

## 7. En emin olmadığım nokta

Fade grisinin hareket hâlinde ne kadar rahatsız edeceğinden emin değilim: 0,8 sn'lik bir çapraz geçiş izleyiciye "normal sinema geçişi" gibi de gelebilir. Kesin olan şu: ara karede gri oranı %55–76'ya çıkıyor ve bu, kurulun onayladığı üç değer kuralıyla çelişiyor. "Engelleyici" kararı bu kurala dayanıyor; kulakla ya da gözle son söz kullanıcının. İkinci emin olmadığım nokta J07'deki "havuç" okuması: 480 px küçültmede çok belirgin, tam boyda daha az. Düşüşün havada süzülüp tek karede yere yapışması ise boyuttan bağımsız bir kusur.
