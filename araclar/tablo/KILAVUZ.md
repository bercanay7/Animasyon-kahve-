# tablo: canlanan yağlıboya motoru (`araclar/tablo/`)

Düz, değer planlı bir resmi (Canvas 2D) fırça ve spatula darbelerine çevirir. Darbeleri boya kalınlığı, sıyıran ışık ve tuval dokusuyla basar. Üstüne her iki karede bir yeniden boyanan canlı katmanlar koyar: figür, rüzgârdaki başak, ışık, uçan kâğıt.
- İlk film: `kurye/tablo.html` ("Mektuplar").
- Figür için `araclar/manken` ile birlikte çalışır.

## Kaynak ve lisans
- `impasto.js`, `plate.js`: Lemo-Opuscar `styles/impasto/demo/engine` (MIT, LemoLab 2026; `LICENSE-MIT.txt`).
- Bizim değişikliklerimiz dosyada "ZK:" notuyla. Kayıt: `araclar/ASSETS.md`.
- Dorian Gray'in kopyası (`dorian-gray/kapi/vendor/`) değiştirilmedi.

## Nasıl çalışır
1. **Referans resim:** `new Ref(W, H, ölçek)`. Her şekil `fill(yol, renk, özellikler)` ile çizilir. Özellikler darbeyi yönetir:
   - `dir`: açı (derece), `'edge'` (biçimi izler), `{radial: [x, y]}` ya da `{fn: (x, y) => radyan}`;
   - `type`: 0 spatula, 1 fırça, 2 leke;
   - `maxR`: en büyük darbe yarıçapı; `len`, `wid`: darbe oranı;
   - `group`: darbe bu kümenin dışına taşmaz, siluet keskin kalır;
   - `hgt`: kabartma; `jit`: renk oynaması; `aj`: açı oynaması; `follow`: kenarda biçime dön; `alpha`.
2. **`paintRef`:** Hertzmann yöntemi. Kaba darbeler önce, ince darbe yalnız resmin hâlâ farklı olduğu yerde (kenar, ayrıntı).
3. **Önbellek (ZK):** `E.onbellek(() => { E.under(...); E.draw(...) })` durağan katmanı bir kez kendi dokusuna boyar. Karede `E.bas(k, {cam})` ile kamerayla basılır.
   - Doku öncül çarpılmıştır: renk RGBA8, yükseklik RG16F.
   - Kenarda %5 pay bırakılır; kamera bu payın dışına kaymamalı.
   - Etkisi: kare 7,2 sn'den 0,94 sn'ye indi (SwiftShader, tek işçi); görüntü farkı ortalama 1,4/255.
4. **Canlı katmanlar:** `new Strokes()` → `push({x, y, ang, len, wid, c, c2, type, alpha, hgt, bend, taper})` → `E.drawNow(data, {cam, t: 10, run})`. `run: 0` kâğıt gibi kırıksız düz darbe verir (spatula boyası bitmez).
5. **Bitiş:** `E.finish({...})`: kabartma ışığı (`light`, `norm`), tuval dokusu (`weave`), renk ayarı (`expo`, `sat`, `contrast`, `gain`, `vig`).
   - **Grisaille (ZK):** `mono: 1, monoK, monoA` değeri korur, rengi iki uçlu tona indirir. Kurye sahnesinde `?mono=1`.

## Kurallar (Mektuplar'ın bağımsız eleştirisinden)
- **Filtre görünümü:** her yerde aynı boy, aynı yön, aynı kabartmalı dörtgen darbe "Photoshop yağlıboya filtresi" okunur. Bunu önlemek için:
  - gökte uzun yatay sürütme (`type: 1, len ≈ 2.5, wid ≈ .6, hgt ≈ .35`);
  - tarlada yakında dik, uzakta küçük ve yatay darbe (aynı `group` içinde bant bant `maxR` ve `dir`);
  - `finish` `norm` ≈ 1.7 (varsayılan 3,2 kabartmayı fayans gibi gösteriyor).
- **Ufuk cetvel çizgisi olmaz:** uzak çit, ağaç öbeği ve pus ufku kırar. Tepeler pusla erir.
- **Bulut mercek biçiminde olmaz:** düzensiz kalınlık, yırtık uç, alt kenar ışıkta.
- **Yuvarlak parlak nesneye halka ya da ışınsal darbe verilmez** (güneş diski hedef tahtası, hipnoz sarmalı okunur). Disk yatay sürütülür, ışıma çevresinde.
- **Koyu taçta doygun turuncu leke köz okunur** (yanan ağaç). Taçtaki ışık kül pembesidir, gök boşlukları gökün rengindedir.
- **Kafa kadar bir çiçek ya da yıldız** dört yapraklıysa küçükte haç okunur. Beş yaprak ya da düzensiz öbek kullanılır.
- **Gölge:**
  - Düz kenarlı simetrik kama gölge "rampa, ışık konisi" okunur; taç gölgesi yumuşak, loblu bir göldür.
  - Figürün gölgesi koyu, ince ve incelerek gider; açık saydam dikdörtgen gölge "cam direk, mezar taşı" okunur.
- **Figür:**
  - Pikselden darbeye çevrilen figürde iç darbeler iri ve diktir; kenar darbeleri biçimi sarar ve iç darbelerden sonra basılır.
  - Kenar darbesi spatula olur (yuvarlak uçlu kısa fırça kenarı boncuk dizisi, şapkayı kıvırcık saç gibi gösterir).
  - Karşı ışıkta güneş yanındaki kenar altın olur (`kenarIsik`). Figür saf siyah olmaz; havanın rengine çekilir (uzaklık).
- **Uzaktaki başak tek tek çizilmez** (eşit aralıklı iğne okunur); doku durağan katmanda kalır, başak yakına doğru sıklaşır.
- **Kâğıt ve mektup:** kapak çizgisi (`type: 3`) ve iki yüz (ışıkta krem, gölgede mor). Düz beyaz dörtgen konfeti ya da kar okunur.

## Ölçümler (SwiftShader, 26 Kasım 2026)
- Yükleme: beş katmanın darbeleri ve önbellekleri ~20–30 sn (işçi başına bir kez). İlk kare ~5 sn (gölgelendirici derleme).
- Kare: tek işçide 0,95–1,1 sn (canlı katmanlar: ~2 bin başak, figür, mektup, çiçek).
- `ss` (süper örnekleme) varsayılan 1,5. `?ss=1` hızlı önizleme.

## Figür kaynağı: Blender (`kurye/blender/`, 26 Kasım)
Bağımsız eleştirinin iki turunda da en zayıf öğe figürdü: kutu gövde, tek sütun bacak, sert palto. Çözüm karma yol:
1. **Eklemler:** hareket yine bizim çözücümüzden gelir. `eklem_disa.js` sahnedeki `kuryePoz`'un kemiklerini 15 çizim/sn dışa yazar.
2. **Gövde (`kurye_bpy.py`):** Blender'da (bpy 5.x Python modülü, Cycles, işlemci) örülür:
   - beden eklemlerden deri (skin) değiştiricisiyle;
   - palto halkalardan (A-kesim, etek açık);
   - fötr, çanta ve kayış ayrı parça.
   - Model indirilmez, lisans sorunu yoktur.
3. **Görüntü:** kamera sahneyle birebir (dikey 40°; ufuk ortanın altında olduğu için kamera 6,15° yukarı bakar).
   - Kare saydam RGBA (960×540); yalnız figürün kutusu çizilir.
   - 376 kare 84 sn sürer.
4. **Boyama:** `tablo.html?blender=1` kareleri okur ve aynı fırça çevirisinden geçirir; görüntü boyalı kalır.

Dersler:
- **Düz tepe + geniş kenarlı koyu şapka ve uzun koyu palto** din adamı (papaz, haham) giysisi okunur. Fötr kullanılır (tepesi daralan, kenarı kısa) ve palto kahverengi yolcu paltosu olur.
- **Kol deri zinciri omuzdan başlarsa** paltonun üstünde apolet gibi çıkıntı yapar (askerî okunur). Kol paltonun içinden başlar.
- **Karşı ışıkta dünya ışığı fazlaysa** figür soluk ve hayalet gibi olur. Gök ışığı .22, yer sekmesi koyu turuncu; sıcak kenarı fırça çevirisi ekler.
- **Kurulum:** EEVEE ekran kartsız açılmaz; Cycles işlemciyle yeter. Kurulum: `python3 -m venv bpyenv && bpyenv/bin/pip install bpy==5.2.5` (≈1 GB, depoya girmez).
