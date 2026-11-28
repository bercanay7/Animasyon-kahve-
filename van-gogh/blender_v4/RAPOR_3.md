# RAPOR 3: Kapı görevi (Y4: Blender yalnız figür üretir)

Görev: `GOREV_3_kapi.md`, 28 Kasım'daki "hazır şablon değil, kendin modelle" ekiyle birlikte. Üç kapı klibi çizildi:
- `theo_oda` (A01);
- `theo_dur` (G02, B01 …);
- `vincent_goster` (G02).

Sonraki adım başkanda: klipleri motora takıp v3, Y4 ve oda_karma'yı yan yana kıyaslamak.

Not: ilk teslimde giysiler MakeHuman takım şablonlarının boyanmış hâliydi. Görevdeki ek kararı (şablon giysi yok) iş sürerken gördüm; giysiler `giysi.py` ile yeniden modellendi ve klipler yeniden çizildi. Bu rapor yeni hâli anlatır.

## Hat
- **Betikler:**
  - `figur_v4.py`: figür, oturtma, geçişler.
  - `giysi.py`: giysi modelleme.
  - `kirp_klip.py`: kırpma.
  - `onizle_klip.py`: önizleme.
- **Komutlar:**
  - `blender -b -P van-gogh/blender_v4/figur_v4.py -- --klip <ad>`
  - `python van-gogh/blender_v4/kirp_klip.py <ad>`
  - `python van-gogh/blender_v4/onizle_klip.py <ad>`
- **v3 sözleşmesi korunur:**
  - aynı `eklem.json`: 121 kare, 15 fps. `klip_*` olanları `node van-gogh/blender/klip.js theo_dur,vincent_goster` üretti.
  - aynı `kamera.json` (konum, hedef, dikey fov, ışık);
  - aynı eksen, `B(p) = (x, −z, y)`;
  - 960×540, saydam zemin, Standard renk dönüşümü;
  - `figur_bpy.py` ile aynı kamera ve ışık kurulumu: güneş, gök ortamı, görünmez sıcak yer sekmesi; A01'de nokta lamba.
- **Figürü eklemlere oturtma:**
  - **Kök:** iskelet pelvis çerçevesiyle döner; iki uyluk başının ortası eklem kalçalarının ortasına konur.
  - **Gövde:** omurga pelvisten göğüs çerçevesine kademeli döner; boyun ve baş kendi çerçevelerine hizalanır.
  - **Kol ve bacak:** iki kemik IK. Uzuvlar her karede eklem uzaklıklarına esnetilir (çocuk kemik ölçeği devralmaz). Böylece diz, dirsek, el bileği ve ayak bileği tam hedefte.
  - **Köprücük:** omuz noktası eklem omzuna %66 oranında çevrilir. Tam çevirmede omuzlar kalkık ve kambur duruyordu; bu oranda sapma ≤ 3 cm.
- **Geçişler** (her kare üç kez render edilir):
  - `kare/k_*.png`: RGBA, Cycles 32 örnek + OptiX gürültü giderme.
  - `normal/n_*.png`: kamera uzayında normal (x sağ, y yukarı, z kameraya doğru), RGB = n·0.5+0.5, Raw (doğrusal) yazım.
  - `kimlik/i_*.png`: düz renk, 1 örnek, süzgeç 0,01 px (karışık kenar yok), alfa 0,5'te eşikli.
    - ten 255,0,0;
    - saç, sakal, kaş 0,255,0;
    - giysi 0,0,255;
    - yaka, gömlek, manşet 255,255,0;
    - şapka 255,0,255;
    - eldeki zarf 0,255,255.
- **Kırpma:** bütün karelerin alfa birleşimi + 6 px pay. Kutu `bilgi.json` → `kirpma {x, y, w, h, tam}` alanında. Motor kareyi (x, y) ofsetiyle tam kareye basar; kırpılmamış kareyle piksel piksel aynıdır. Kırpılmadan her klip ~60 MB'tı (sınır 20 MB).

## Ölçümler
| Klip | Kare | RGBA sn/kare | Normal | Kimlik | Kalça sapması | Omuz sapması | Bilek yükseltme | Kırpma (x, y, w, h) | Boyut |
|---|---|---|---|---|---|---|---|---|---|
| theo_oda | 121 | 1.13 | 1.20 | 1.24 | 1.4 cm | 3.0 cm | 3.4 cm | 231, 225, 140, 315 | 9.9 MB |
| theo_dur | 121 | 1.12 | 1.20 | 1.23 | 1.4 cm | 3.0 cm | 3.4 cm | 421, 95, 129, 411 | 11.9 MB |
| vincent_goster | 121 | 1.08 | 1.12 | 1.16 | 1.5 cm | 2.7 cm | 3.4 cm | 384, 96, 170, 409 | 14.0 MB |

- **Eklem sapması:**
  - Diz, dirsek, el bileği, ayak bileği: 0 mm (uzuvlar eklem boyuna birkaç yüzde esnetildi).
  - Kalça kökü ≤ 1,5 cm; omuz ≤ 3 cm.
- **Ayak bileği yüksekliği:** eklem verisinde "bilek" yerde (y = 0,03 m); MPFB'nin ayak bileği tabanın 6–7 cm üstünde. Ayağın yere basması için bilek hedefi ≈ 3,4 cm yukarı alındı. Bu bir anatomi farkı; ayak tabanı yerde.

## Giysiler: Blender'da modellendi (`giysi.py`)
- **Yöntem:**
  - Kalıp parçaları figürün kendi MPFB gövde yüzeyinden kesilir: kemik ağırlığı ve dinlenme yüksekliğiyle seçilen bölgeler, ayrıca MakeHuman'ın yardımcı kabukları (`helper-tights` pantolon, `helper-skirt` ceket eteği).
  - Parçalar bol pay verilerek dışa şişirilir; kalınlık, düşük frekanslı kumaş kırışığı ve yumuşatma eklenir.
  - Parçalar gövdenin kemik ağırlıklarını taşır, pozla birlikte hareket eder.
  - Hazır giysi şablonu kullanılmadı.
- **Theo:**
  - Göğüste yüksek kapanan koyu yün ceket: V açıklık göğüs hizasında, kalça boyu etek, önü aşağıda hafif açılır.
  - Koyu yelek V'de görünür.
  - Kolalı beyaz dik yaka; arkada ceket yakasının üstünde ≈ 1–2 cm şerit.
  - Ince düz koyu kravat, beyaz manşetler.
  - Düz bol pantolon, paçaya doğru genişler; yan şerit yok. Koyu deri ayakkabı.
- **Vincent:**
  - Bourgeron: mat mavi pamuk, bol, kalçayı örten, önü kapalı; boyunda küçük V, koyu mavi devrik yaka, kalçada iki yama cep.
  - Açık keten gömlek yakası, ince koyu boyun bağı.
  - Bol koyu kadife pantolon; kot, kemer ve toka yok.
- **Hasır şapka:**
  - Betikte modellendi: alçak, hafif çökük tepe; düz geniş kenar (kıvrık değil, kovboy değil).
  - Hasır örgü kabartısı: eş merkezli bantlar × ışınsal ilmekler.
  - `mixamorig:Head`'e bağlı. Altında saç bastırılır, ensede kızıl saç görünür.
- **Zarf** (A01, Theo'nun sağ elinde): betikte modellendi, `#DBA84C` civarı mat kâğıt.
- **Eller:**
  - Dinlenme pozu kademeli 20–40° bükük, başparmak içe.
  - Gösteren elde işaret parmağı düz.
  - Avuç yönü elin kendi geometrisinden sabitlendi; önceki partideki pençe pozunun kökü bu yöndü.

## Beden ve yüz
- **Beden:** MPFB2 tabanı, başlangıç noktası olarak.
- **Yüz oranları:** MakeHuman hedefleriyle kaynağa göre düzeltildi, yaşayan birine benzetilmedi.
  - **Vincent:** belirgin elmacık, çökük yanak, öne çıkık çene, burun kemeri (otoportreler).
  - **Theo:** daha ince yanak ve oval baş (1887–1889 fotoğrafları).
  - Kliplerde figürler sırttan ¾ olduğu için yüz az görünür.
  - Referans görselleri `varlik/referans/` altına henüz konmadı; ayar elle, kamu malı otoportre ve fotoğraflara bakılarak yapıldı.
- **Saç ve sakal** (gövde parçası; giysi şablonu değil):
  - Theo: `short01` (taranmış, yandan ayrık).
  - Vincent: `short02`.
  - İkisinde de Viking sakalı çene altında kesilerek kısa dolgun sakala çevrildi, bıyık eklendi. İkisi de CC0.

## Varlıklar ve lisanslar (`araclar/ASSETS.md`'de)
- **MPFB2:** GPL-3 araç; yerelde çalışır, ürettiği gövdeler CC0.
- **MakeHuman paketleri:**
  - system assets (CC0): beden, deriler, gözler, kaşlar, kirpik, dişler, `short01` ve `short02` saçları;
  - `toigo_light_skin_male_ginger` (MargaretToigo, CC0);
  - `rehmanpolanski_beard_viking` (kesilerek) ve `rehmanpolanski_moustache_viking` (RehmanPolanski, CC0; dosya başlığı da CC0).
- **Kullanımdan çıkarılanlar:**
  - Lisans çelişkisi: `wdg_scruffy_beard`, `rehmanpolanski_hair_bun_brown` ve `grinsegold_beard_sigmund_wip` paket sayfasında CC0, `.mhclo` başlığında AGPL3. Kullanılmaz.
  - Kullanıcı kararı: MakeHuman giysi şablonları (`male_elegantsuit01`, `toigo_male_suit_3`, `toigo_male_suit_tie_and_jacket`, `male_casualsuit01`, `punkduck_medieval_dress`, ayakkabılar). Yerlerine `giysi.py`.
- **Betikte üretilenler:** giysiler, hasır şapka, zarf.

## Sorunlar ve dürüst değerlendirme
- **Kumaş simülasyonu yok:**
  - Kıvrım düşük frekanslı yer değiştirmeyle veriliyor; dökümlü kat ve dikiş çizgisi yok.
  - Görevin önerdiği Cloth + Sewing yoluna geçilmedi. Klipler sırttan ve 960×540'ta küçük olduğu için kapıda yeterli olur mu, başkanın kıyası söyleyecek.
  - Toplu görevde Jo'nun eteği ve bebek battaniyesi için kumaş simülasyonu gerekecek.
- **Ceket kesimi:**
  - Yaka katı (devrik ceket yakası) ayrı parça değil; V açıklığın kenarı kalınlıkla okunuyor.
  - Ceket üstüyle etek arasında belde ince, koyu gri bir dikiş izi var (iki parça bindiriliyor); parlak değil.
- **Omuz:** köprücük oranı bir uzlaşma. Eklem omuzları MPFB'ninkinden ~6 cm yüksek; bu oranda omuzda hafif dolgunluk kalıyor.
- **Ayak bileği:** eklem verisinin "bilek"i yerde, MPFB'ninki tabanın üstünde (≈ 3,4 cm).
- **Yüz eylemleri** (gülme, göz silme; GOREV_2 Y1) bu üç klipte yok; toplu görevde yüz şekil anahtarları gerekecek.
- **v4-1 oda planlarının G02 yeniden render'ı** yön değiştiği için durduruldu; şapka düzeltmesi `planlar.py`'de kayıtlı.

## Hassasiyet (tam boy karede, gri zeminde)
- **Papaz yakası:** Theo'nun yakası kravatlı ve V açıklıkta; arkada ince şerit. Siyah giyside tek başına beyaz dikdörtgen yok. Cep mendili yok.
- **Pençe el:** dinlenme eli kademeli bükük, gösteren elde tek parmak düz.
- **Şapka:** başın üstünde, düz kenarlı, alçak tepeli; hale ya da kovboy şapkası okunmuyor.
- **Baş:** gövdeden kopuk değil; boyun, yaka ve ceket sürekli.
- **Ayaklar yerde.**
- **Kırmızı leke yok:** kızıl saç ve sakal dışında kırmızı yüzey yok.

## Önizlemeler
`onizleme/klip_<ad>_{000,040,080}.jpg`: gri zemin üstünde RGBA kare; altta normal ve kimlik şeridi.
