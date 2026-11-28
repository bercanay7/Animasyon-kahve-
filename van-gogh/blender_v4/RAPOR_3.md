# RAPOR 3: Kapı görevi (Y4: Blender yalnız figür üretir)

Görev: `GOREV_3_kapi.md`. Üç kapı klibi çizildi: `theo_oda` (A01), `theo_dur` (G02, B01 …), `vincent_goster` (G02). Sonraki adım başkanda: klipleri motora takıp v3, Y4 ve oda_karma'yı yan yana kıyaslamak.

## Hat
- **Betik:** `van-gogh/blender_v4/figur_v4.py`.
  - `blender -b -P van-gogh/blender_v4/figur_v4.py -- --klip <ad>`
  - ardından `python van-gogh/blender_v4/kirp_klip.py <ad>` ve `python van-gogh/blender_v4/onizle_klip.py <ad>`.
- **v3 sözleşmesi korunur:**
  - aynı `eklem.json`: 121 kare, 15 fps (`klip_*` olanları `node van-gogh/blender/klip.js theo_dur,vincent_goster` üretti);
  - aynı `kamera.json` (konum, hedef, dikey fov, ışık);
  - aynı eksen, `B(p) = (x, −z, y)`;
  - 960×540, saydam zemin, Standard renk dönüşümü;
  - `figur_bpy.py` ile aynı kamera ve ışık kurulumu: güneş, gök ortamı, görünmez sıcak yer sekmesi; A01'de nokta lamba.
- **Figürü eklemlere oturtma:**
  - **Kök:** iskelet, pelvis çerçevesiyle döndürülür; iki uyluk başının ortası eklem kalçalarının ortasına konur.
  - **Gövde:** omurga pelvisten göğüs çerçevesine kademeli döner; boyun ve baş kendi çerçevelerine hizalanır.
  - **Kol ve bacak:** iki kemik IK. Uzuvlar her karede eklem uzaklıklarına esnetilir (çocuk kemik ölçeği devralmaz), böylece diz, dirsek, el bileği ve ayak bileği tam hedefte. Ayak eklemin ayak çerçevesine, el önkolun devamına hizalanır.
  - **Köprücük:** omuz noktası eklem omzuna %66 oranında çevrilir. Tam çevirmede omuzlar kalkık ve kambur duruyordu; bu oranda sapma 3 cm'nin altında.
- **Geçişler** (her kare üç kez render edilir):
  - `kare/k_*.png`: RGBA, Cycles 32 örnek + OptiX gürültü giderme.
  - `normal/n_*.png`: kamera uzayında normal (x sağ, y yukarı, z kameraya doğru), RGB = n·0.5+0.5, Raw (doğrusal) yazım.
  - `kimlik/i_*.png`: düz renk, 1 örnek, süzgeç 0,01 piksel (karışık kenar yok), alfa 0,5'te eşiklenir.
    - ten 255,0,0;
    - saç, sakal, kaş 0,255,0;
    - giysi 0,0,255;
    - yaka/gömlek 255,255,0;
    - şapka 255,0,255;
    - eldeki zarf 0,255,255.
- **Kırpma:** bütün karelerin alfa birleşimi + 6 px pay. Kutu `bilgi.json` → `kirpma {x, y, w, h, tam}` alanında. Motor kareyi (x, y) ofsetiyle tam kareye basar; kırpılmamış kareyle piksel piksel aynıdır. Kırpılmadan her klip ~60 MB'tı (sınır 20 MB).

## Ölçümler
| Klip | Kare | RGBA sn/kare | Normal | Kimlik | Kalça sapması | Omuz sapması | Bilek yükseltme | Kırpma (x,y,w,h) | Boyut |
|---|---|---|---|---|---|---|---|---|---|
| theo_oda | 121 | 0.98 | 1.04 | 1.06 | 1.4 cm | 3.0 cm | 3.4 cm | 228, 225, 143, 315 | 9.8 MB |
| theo_dur | 121 | 0.97 | 1.03 | 1.06 | 1.4 cm | 3.0 cm | 3.4 cm | 420, 95, 129, 413 | 11.7 MB |
| vincent_goster | 121 | 1.00 | 1.02 | 1.05 | 1.5 cm | 2.7 cm | 3.4 cm | 384, 96, 168, 410 | 13.4 MB |

- **Eklem sapması:**
  - Diz, dirsek, el bileği, ayak bileği: 0 mm. Uzuvlar eklem boyuna esnetildi; esneme birkaç yüzde.
  - Kalça kökü ≤ 1,5 cm; omuz ≤ 3 cm.
- **Ayak bileği yüksekliği:** eklem verisinde "bilek" yerde (y = 0,03 m), MPFB'nin ayak bileği tabanın 6–7 cm üstünde. Ayağın yere basması için bilek hedefi ≈ 3,4 cm yukarı alındı (`ayak_bilegi_yukseltme_m`); ayak tabanı yerde, ayak havada değil.

## Karakterler (GOREV_2'nin figür maddelerinden uygulananlar)
- **Theo:**
  - `male_elegantsuit01` düz renklere çevrildi: koyu ceket ve pantolon, yakadaki V'de beyaz yaka, koyu kravat.
  - Gömleğin yakadan aşağısı koyu yelek rengine boyandı; yelek ayrı bir giysi değil, gömlek bölgesinin rengi.
  - Arkadan ceket yakasının üstünde 1–2 cm beyaz yaka şeridi görünüyor.
  - `short01`: yandan ayrık, taranmış kısa saç, açık kumral.
  - Sakal: Viking sakalı çene altında kesildi; kısa, dolgun, çeneyi ve dudak altını örten sakal + bıyık.
  - A01'de sağ elinde sarı zarf (`#DBA84C` civarı), parmaklar kavrıyor.
- **Vincent:**
  - `toigo_male_suit_3`: ceket mat orta-koyu mavi, gömlek açık keten rengi.
  - Kırmızı kravat koyu ince bağa çevrildi; cep mendili ceket rengine çekildi (beyaz dikdörtgen kalmadı).
  - Pantolon koyu, kemer ve toka yok. Kot dokusu ve kot dikişi yok (giysi değişti).
  - Kızıl kısa sakal + bıyık.
  - Hasır şapka: alçak tepe, düz geniş kenar (kıvrık değil: kovboy değil), açık saman rengi, başa oturur (`mixamorig:Head`'e bağlı). Altındaki saç bastırıldı, ensede kızıl saç görünür.
  - 2–3,2 sn arası sol eliyle aşağıyı gösterir: işaret parmağı düz, diğerleri kıvrık.
- **Eller:** dinlenme pozu kademeli 20–40° bükük, başparmak içe.
  - Avuç yönü artık elin kendi geometrisinden sabitleniyor.
  - Önceki partideki pençe pozunun kökü buydu: avuç yönü bedene göre seçiliyordu ve kol dışa açılınca ters dönüyordu.
- **Malzeme:** gerçek değerler, doku yok ya da çok hafif. Kıvrım gölgesi okunsun diye doku parlaklığı ±%10 bırakıldı. Ten MPFB derisi, yüzey altı saçılımı 0,15.

## Varlıklar ve lisanslar (`araclar/ASSETS.md`'de)
- **MPFB2:** GPL-3 araç, yerelde çalışır; ürettiği gövdeler CC0.
- **MakeHuman paketleri:**
  - system assets (CC0): `male_elegantsuit01`, `short01`, `short02`, kaşlar, kirpik, gözler, dişler, ayakkabı `shoes02`, deriler.
  - `toigo_male_suit_3` ve `toigo_light_skin_male_ginger` (MargaretToigo, CC0).
  - `rehmanpolanski_beard_viking` (kesilerek) ve `rehmanpolanski_moustache_viking` (RehmanPolanski, CC0; dosya başlığı da CC0).
- **Kullanımdan çıkarılanlar:** `wdg_scruffy_beard`, `rehmanpolanski_hair_bun_brown`, `grinsegold_beard_sigmund_wip`.
  - Paket sayfası CC0 diyor ama `.mhclo` dosya başlığı AGPL3.
  - Çelişkili lisans kullanılmaz. v4-1 önizlemelerindeki sakal ve Jo'nun topuzu bunlardı.
  - Jo için topuz toplu görevde yeniden seçilecek.
- **Hasır şapka ve zarf:** betikte üretildi.

## Sorunlar ve dürüst değerlendirme
- **Yelek:** ayrı bir giysi değil, gömlek bölgesinin koyu boyanması. Önden yakın bakışta yelek düğmesi ya da yaka katı yok. Bu kliplerde figür sırttan ¾ olduğu için görünmüyor.
- **Vincent'in ceketi:** takım ceketi kesimi. GOREV_2 E1'deki bol bourgeron değil, yama cepler yok. Mavi, mat ve kalçayı örtüyor; kemer hattı görünmüyor. Bol kesim için ayrı modelleme gerekir.
- **Omuz:** köprücük oranı bir uzlaşma. Eklem omuzları MPFB'ninkinden ~6 cm yüksek; tam oturtunca omuz kalkıyordu. Bu oranda omuzda hafif dolgunluk kalıyor.
- **Ayak bileği:** eklem verisinin "bilek"i yerde; MPFB'nin ayak bileği tabanın üstünde. Bu fark sözleşmenin sınırı değil, anatomi farkı (≈ 3,4 cm).
- **Gülme, göz silme gibi yüz eylemleri:** bu kapıdaki üç klipte yok; GOREV_2 Y1 için yüz şekil anahtarları toplu görevde gerekecek.
- **v4-1 oda planlarının kalan G02 yeniden render'ı** (şapka düzeltmesi) yön değiştiği için durduruldu. Şapka düzeltmesi `planlar.py`'de kayıtlı.

## Hassasiyet (tam boy karede, gri zeminde)
- **Papaz yakası:** Theo'nun yakası kravatlı V ve arkada ince şerit; siyah giyside tek beyaz dikdörtgen yok. Vincent'in cep mendili kaldırıldı.
- **Pençe el:** dinlenme eli kademeli bükük; işaret eli tek parmak düz.
- **Şapka:** başın üstünde, düz kenar, tepesi alçak; hale ya da kovboy şapkası okunmuyor.
- **Baş gövdeden kopuk değil:** boyun ve yaka sürekli.
- **Ayaklar yerde:** bilek hedefi tabanı yere koyacak yükseklikte; havada asılı ayak yok.
- Kırmızı leke yok; Vincent'in kızıl saç ve sakalı dışında kırmızı yüzey yok.

## Önizlemeler
`onizleme/klip_<ad>_{000,040,080}.jpg`: gri zemin üstünde RGBA kare; altta normal ve kimlik şeridi.
