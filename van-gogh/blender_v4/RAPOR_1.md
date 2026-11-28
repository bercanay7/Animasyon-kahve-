# RAPOR 1: Van Gogh v4 oda planları (Blender + GPU), ilk iki plan

Görev: `GOREV_1_oda.md`. Bu rapor §5 sıra 4'ün teslimi: **A01 ve G02** çizildi, başkanın eleştirisini bekliyor. Kalan on plan eleştiriden sonra.

## Hat
- **Bilgisayar:** RTX 4070 (12 GB), Blender 5.3.0, Cycles OptiX, OptiX gürültü giderme, 1920×1080, 160 örnek, sabit tohum.
- **Betikler** (depo kökünden):
  - `oda_kur.py`: kalıcı oda. Dekor `bekar`/`evli` (+ beşik, sandıklar); ışık `gece_lamba`, `ogle`, `sabah`, `kis_gun`, `kis_gece`. Tek başına çalışırsa `oda.blend` yazar (depoda değil).
  - `karakter.py`: Theo, Vincent, Jo ve bebek (MPFB2 + MakeHuman paketleri; Mixamo iskeleti).
  - `poz.py`: dünya yönleriyle pozlama, bakış, nefes, iki kemik IK.
  - `planlar.py`: plan başına sahne, sözcüğe bağlı eylemler, kamera, RGB ve maske plakası.
  - `onizle.py`: depoya giren önizlemeler. `varlik_indir.py`: varlıklar.
- **Komut:** `blender -b -P van-gogh/blender_v4/planlar.py -- --plan A01 --fps 30`, ardından `python van-gogh/blender_v4/onizle.py A01`.
- **Plaka** (`plaka/<PLAN>/`, depoda değil): `rgb/0000.png …`, `maske/0000.png …`, `bilgi.json` (fps, kare sayısı, pay, kamera, kare süreleri). Kareler −0,5 sn'den `sure_sn + 0,5`'e.
- **Maske:** nesne indeksi 1, compositor ID Mask, kenar yumuşatmalı. Beyaz: şövaledeki tablo, duvara dayalı Vincent tuvallerinin yüzü, sarı zarflar.

## Testten gelen üç düzeltme
1. **Tablo ışıktan bağımsız gerçek renginde:** yağlıboya yüzeyi (kabartı, ince vernik) + tablonun kendi dokusundan yayım (gece 0,9; gündüz 1,4–1,6). Lamba turuncuya boyamıyor; A01'de karenin en parlak ve en doğru renkli yeri tablo.
2. **Pencere:** iki kanatlı, kanat başına 3 × 2 küçük cam; kayıtlar ince ve açık boyalı. Koyu dikey şerit dizisi yok. Evli dekorda ince tül perde. Dışarıda gece çatıları, bacalar ve ay ya da gündüz cepheleri.
3. **Dönem giysisi:** Rocketbox yerine MPFB2 (MakeHuman) insanları:
   - **Theo:** ince, açık kumral; bıyık ve kısa sakal; koyu takım, beyaz yaka, ince kravat.
   - **Vincent:** kızıl saç ve sakal; mavi iş giysisi; betikle modellenmiş hasır şapka.
   - **Jo:** ensede topuz; dik yakalı, bileğe kadar koyu lacivert elbise. Bu iki planda yok.
   - **Bebek:** MakeHuman'ın en küçük yaşı (1), 0,55 ölçekte. Krem kundakta (beyaz değil), yüzü görünür.

## Planlar
| Plan | Süre | Kare | fps | Kare süresi (ort.) | Ne var |
|---|---|---|---|---|---|
| A01 | 5,48 sn + 2×0,5 | 195 | 30 | 8,5 sn | bekâr, gece lamba; Theo sırttan ¾ şövaleye bakar, "inandı"da başını kaldırır, "yazı masası"nda lambaya döner; kamera tuvale ve lambaya %45 yaklaşır |
| G02 | 11,77 sn + 2×0,5 | 384 | 30 | 10,7 sn | evli, sabah; Güller şövalede; iki kardeş beşiğin başında ayakta, beşik ön planda. "tığ"da (8,64) Vincent örtüyü bir köşesinden kaldırıp gösterir, "şaka"da Theo başını kaldırıp kardeşine döner. Kamera hafif yaklaşır |

Ölçüt: kare ≤ 12 sn → 30 fps. İkisi de altında kaldı.

## Varlıklar ve lisanslar (hepsi `araclar/ASSETS.md`'de)
- **MPFB 2.0.18:** GPL-3 araç; yerelde çalışır, ürettiği gövdeler CC0. Kullanıcının onayıyla kuruldu.
- **MakeHuman paketleri:**
  - system assets (CC0): gözler, kaşlar, kirpik, saçlar, deriler, `male_casualsuit01`, ayakkabılar.
  - `toigo_male_suit_tie_and_jacket` ve `toigo_light_skin_male_ginger` (MargaretToigo, CC0).
  - `wdg_scruffy_beard` (WDG, CC0).
  - `rehmanpolanski_moustache_viking` ve `rehmanpolanski_hair_bun_brown` (RehmanPolanski, CC0).
  - `punkduck_medieval_dress` (punkduck, **CC BY**: Jo'nun elbisesi; Jo'lu planlarda açıklamaya atıf gerekir).
- **Poly Haven (CC0):** masa, sandalye, yağ lambası, kitaplar, gözlük, dikiş sepeti, sandıklar; döşeme, sıva ve ahşap dokuları.
- **Tablolar:** Met Open Access CC0 (otoportre 436532, Güller 436534, İrisler, Zeytinlik, Ayçiçekleri, Selviler), depodaki `van-gogh/gorsel/`.

## Sorunlar ve dürüst değerlendirme
- **Yüzler:** MakeHuman yüzleri genel ve oyuncuya ya da yaşayan birine benzemiyor; ama gerçek fotoğraf kalitesinde değil. Theo "hafif güler" yüz ifadesiyle yapılamadı: Mixamo iskeletinde yüz kemiği yok. Baş kaldırma ve kardeşe dönme olarak çizildi.
- **Giysi:** Theo'nun takımı modern kesim ama koyu, yaka beyaz ve kravat ince; 1880'ler gibi okunuyor. Vincent'in iş giysisi gömlek + kot pantolon dokusu; mavi iş takımı gibi okunuyor, yakın planda kot dikişi görülebilir.
- **Örtü:** kumaş simülasyonu yok. "Tığ"da örtü düz hâlden elden sarkan biçime şekil anahtarıyla geçiyor; yakında sert bir mendil gibi duruyor. Deseni yuvarlak ilmek tümseği, haç deseni yok.
- **Eller:** parmak bükümü betikle; bazı karelerde parmaklar açık ve gergin.
- **Vincent'in yüzü:** G02'de yukarıdan bakan kamerada hasır şapkanın gölgesinde kalıyor; sakal ve ağız görünüyor.
- **Mixamo:** onaylandı; yürüyüş isteyen G01 ve G05 için gerekecek. Oturumu kullanıcı açacak.

## Hassasiyet taraması (tam boy karede)
- İki figür aynı anda öne eğilmiyor: G02'de yalnız Vincent örtüye uzanırken eğiliyor; Theo dik duruyor, yalnız başı hafif eğik.
- Beşik: açık ahşap, kavisli sallanma kızakları, parmaklıklı yanlar (yalnız dikey çubuk), baş ucunda kumaş gölgelik. Kapalı kutu yok, koyu renk yok.
- Kundak, yatak ve örtü krem-bej, beyaz değil.
- Şövale: iki bacak tepede birleşiyor, raf yalnız aralarında, kesişen çubuk yok.
- Arkadan görünen tuval: yalnız çevre çıtası, orta ya da çapraz çıta yok.
- Pencere: küçük camlı ızgara, ince ve açık boyalı kayıtlar; tek bir koyu haç biçimi okunmuyor.
- Kırmızı leke yok (Vincent'in sakalı ve tablolar dışında).
- Theo'nun beyaz yakası kravatlı, gömlek yakası; papaz yakası dikdörtgeni yok.
- Hasır şapka başın üstünde, başın arkasında daire (hale) okunmuyor. İlk denemede baş ters eğildiği için hale gibi duruyordu; düzeltildi.
- Ayaklar yerde; asılı ya da havada beden yok.

## Önizlemeler
`onizleme/A01_{25,50,75}.jpg`, `onizleme/A01.mp4`, `onizleme/G02_{25,50,75}.jpg`, `onizleme/G02.mp4`.
