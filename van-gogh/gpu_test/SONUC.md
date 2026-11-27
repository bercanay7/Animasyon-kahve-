# GPU'lu Blender üslup testi: Theo'nun odası (sonuç)

Görev: `araclar/gpu_test/GOREV.md`. Betik: `araclar/gpu_test/oda_testi.py` (varlıklar: `araclar/gpu_test/varlik_indir.py`).
Tarih: 27 Kasım 2026, kullanıcının bilgisayarı.

## Donanım ve yazılım
- **Ekran kartı:** NVIDIA GeForce RTX 4070 (12 GB), sürücü 610.88. Cycles cihazı: **OptiX**.
- **Blender:** 5.3.0 (winget ile kuruldu; görevdeki "4.2 ya da üstü" koşulunu karşılıyor).
- **ffmpeg:** 9.1 (winget, Gyan.FFmpeg).
- Blender 5.x ve ffmpeg 9 farkları (betikte çözüldü): ffmpeg 9 PNG'nin sRGB etiketini MP4'e taşıyor (`color_trc=iec61966-2-1`), `setparams` ile BT.709'a çevrildi; compositor `scene.compositing_node_group` ile kurulur; File Output düğümünde önce `format.media_type = 'IMAGE'` seçilmezse yalnız çok katmanlı EXR yazar.

## Render süreleri (1920×1080, Cycles GPU, OptiX gürültü giderme, sabit tohum 1888)
- **Tek kare** (`oda_renkli.png`, 256 örnek): 11,9 sn.
- **Hareketli kare ortalaması** (180 kare, 256 örnek): 12,5 sn/kare (çoğu 12–13 sn; en kısa 11,7, en uzun 17,9; yavaş karelerin nedeni ölçülmedi, büyük olasılıkla ekran kartını aynı anda kullanan masaüstü uygulamaları); toplam ≈ 37 dk.
- Karma (grisaille) birleştirmesi kare başına ~1 sn (Blender içi numpy).
- Ölçümlerin ham hâli: `olcum.json`.

## Çıktılar
| Dosya | Ne |
|---|---|
| `oda_renkli.png` | tam renkli tek kare |
| `oda_karma.png` | filmin kuralı: dünya gri (siyah `#0b0a0a` → beyaz `#f7f0e1`), yalnız tuvaldeki tablo ve sarı zarflar renkli |
| `oda_hareket.mp4` | 6 sn, 30 fps, H.264 CRF 18, BT.709, 2,1 MB, karma; kamera lambaya ve tuvale yaklaşır, Theo nefes alır, başını lambaya çevirir, mektuplu elini hafifçe kaldırır |
| `oda_hareket_renkli.mp4` | aynı hareket, tam renkli (2,5 MB) (karşılaştırma için) |
| `karsilastirma_A01.jpg` | bulut hattının A01 karesi ile bu hattın karma ve renkli kareleri yan yana |

## Yöntem
- **Sahne:** 4,8 × 6 m oda, 3,05 m tavan. Arka duvarda uzun pencere (yalnız dikey kayıtlar), iki perde, korniz. Dışarıda prosedürel Paris çatıları (mansard, bacalar ve çömlekler, birkaç sıcak pencere), ay ve koyu lacivert gece göğü. Sağ duvara dik yazı masası; üstünde yağ lambası, el yazılı kâğıtlar, sarı zarflar, kitaplar, gözlük. Masanın önünde sandalye. Odanın ortasında şövale ve tuval.
- **Tuval:** *Hasır Şapkalı Otoportre* (1887, Met 436532, CC0) renk dokusu; parlaklığından hafif kabartı (impasto) ve ince vernik.
- **Figür:** Rocketbox Business_Male_03 (MIT). A-pozdan betikle doğal duruşa çevrildi (kollar, dirsekler, parmaklar), sağ ele katlı bir mektup bağlandı. Kravat dokuda koyu boyunbağına çevrildi. Boy 1,76 m. Gövdeye bir kat alt bölümleme.
- **Işık:** lamba = küçük yarıçaplı (1,2 cm) nokta ışık, 2700 K + damla biçimli yayım alevi + camın yumuşak ışıması; ay = 0,8° açılı zayıf soğuk güneş ışığı, pencereden. Dünya ışığı yalnız gökyüzü dolgusu. AgX, hafif sis parlaması (compositor Glare).
- **Karma:** compositor'da nesne indeksiyle iki maske (tablo = 1, zarflar = 2; ID Mask, kenar yumuşatmalı) PNG olarak yazılır. Maske dışı, görüntü uzayında parlaklıktan sıcak grisaille'e eşlenir. Tablodaki lamba dökümü kısmen nötrlenir (gri dünya kazancı, 0,75–1,7 ile sınırlı) ki tablo kendi renkleriyle okunsun; zarflar ham renkleriyle kalır.

## Kullanılan varlıklar ve lisansları
Hepsi `araclar/ASSETS.md`'de kayıtlı. Ham dosyalar depoda değil (`araclar/gpu_test/varlik/`, `.gitignore`).
| Varlık | Kaynak | Lisans |
|---|---|---|
| WoodenTable_01, gallinera_chair, vintage_oil_lamp, book_encyclopedia_set_01, round_spectacles | Poly Haven | CC0 |
| old_wooden_floor_01, plastered_wall_04, dark_wooden_planks (2k dokular) | Poly Haven | CC0 |
| Business_Male_03 (riglenmiş insan) | Microsoft Rocketbox (GitHub) | MIT, lisans metni `varlik/rocketbox/LICENSE.md` |
| *Hasır Şapkalı Otoportre* (1887) | The Met Open Access 436532 (depoda zaten var) | CC0 |
Gökyüzü, çatılar, şövale, tuval şasisi, perdeler, kâğıt ve zarflar betikte üretildi. HDRI kullanılmadı.

## Değerlendirme (dürüst)
**İyi olan**
- **Malzemeler gerçek okunuyor:** döşemede ahşap damarı ve aşınma, sıvada leke ve tabana doğru kir, masada cilalı ahşap, kâğıtta el yazısı satırları, tuvalde boya kabartısı ve kenarda keten.
- **Lamba ışığı fiziksel:** küçük kaynak; şövalenin duvara düşen gölgesi yumuşak kenarlı, ışık lambadan uzaklaştıkça sıcak ve yumuşak düşüyor; köşede duvar parlıyor, odanın solu karanlığa gömülüyor.
- **Figür manken gibi değil insan gibi okunuyor:** kulak, saç çizgisi, ense, ceket kırışıkları, el ve tutulan mektup. Bulut hattının "örülmüş manken"iyle aradaki fark tek bakışta görülüyor (`karsilastirma_A01.jpg`).
- **Karma kural tutuyor:** gri oda içinde tablo ve sarı zarflar gözü hemen çekiyor.
- **Hız:** RTX 4070'te 1080p 256 örnek kare ~12 sn. 6 saniyelik plan ~40 dakikada çıkıyor; bir videonun figürlü planları gece boyunca render edilebilir.

**Hâlâ zayıf olan**
- **Yüz:** kadrajda yalnız ense, kulak ve çene hattı görünüyor. Rocketbox yüzü oyun kalitesinde (~4 bin köşe); yakın planda zayıf kalır. Yakın plan gerekirse daha yoğun bir insan modeli (MPFB2 ya da satın alınmış bir model) ve yüz rig'i denenmeli. Yaşayan birine benzerlik yakın planda ayrıca denetlenmeli.
- **El:** parmak bükümü betikle yapıldı. Geniş planda mektubu tutuyor gibi okunuyor, ama yakın planda parmakların kâğıda temas etmediği görülebilir.
- **Giysi:** modern takım elbise. Geniş planda ve lamba ışığında koyu ceket, beyaz yaka olarak 1880'lere geçiyor; ama ceket kısa ve dar, yüksek kolalı yaka ve redingot yok. Orta ve yakın planda modern okunur; dönem giysisi (ör. Marvelous Designer ile dikilmiş redingot) gerekir.
- **Işık:** Theo neredeyse siluet. Ay ışığı figürün kameranın görmediği önüne düşüyor, sırtına kenar ışığı vermiyor. Lamba camı ince ve alev küçük; parıltı compositor'dan geliyor. Lamba çevresinde hacimsel toz denenmedi (gürültü ve süre).
- **Tablo rengi:** 2700 K lamba altında tablo sıcak ve sarıya kayıyor; karmada kısmi beyaz dengesi bunu yarıya indiriyor, ama özgün mavi-yeşil tonlar biraz soluk.
- **Hareket:** nefes, baş çevirme ve el kaldırma betikle (prosedürel); hareket yakalama (mocap) yok. Sayfa çevirme yapılmadı, onun yerine baş çevirme seçildi. Kamera yaklaşırken Theo kadrajdan soldan çıkıyor (bilinçli: son karede lamba ve tuval).
- **Pencere dışı:** çatılar basit kutu ve kesik piramit; uzaklıkta ve karanlıkta geçiyor, yaklaşırsa zayıf kalır.

## Hassasiyet taraması (tam boy karede, `CLAUDE.md` "Görüntüde yakalananlar")
- **Haç gibi çerçeve ya da çıta:** pencerede yatay kayıt yok, yalnız dikey bölmeler. Şövale A biçiminde: iki bacak tepede birleşiyor, raf yalnız iki bacak arasında; arka bacak tuvalin arkasında. Kesişen dik iki çubuk yok.
- **Kan gibi kırmızı leke:** yok. Tek kırmızı, tablodaki sakal (eserin kendisi). Lamba gövdesindeki pembe çiçek deseni küçük ve gri dünyada griye dönüyor.
- **Asılı ya da havada duran beden:** yok; Theo ayakları yerde duruyor.
- **Yaşayan birine benzeyen yüz:** yüz görünmüyor (sırttan ¾).
- Diğer maddeler (papaz yakası, hale, kalkan, hedef tahtası, mihrap kandili vb.) için de bakıldı; benzer bir şekil yok. Ay tek parlak daire, halka taraması yok.

## Sonraki adım için öneri (başkana)
- Geniş ve orta planlar bu hatla hemen çizilebilir; figürlü yakın planlar için önce yüz, el ve dönem giysisi çözülmeli.
- Theo'ya sırttan kenar ışığı için ay yönü ya da ikinci bir soğuk dolgu, film diline göre ayarlanmalı.
- Plan başına süre: 1080p, 256 örnek, ~12 sn/kare. 30 fps'de dakikalık figürlü sahne ≈ 6 saat.
