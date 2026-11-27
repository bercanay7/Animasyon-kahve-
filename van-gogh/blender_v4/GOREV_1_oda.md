# GÖREV v4-1: Van Gogh filminin oda planları, Blender + GPU

Bu görev, kullanıcının bilgisayarındaki (RTX 4070) Claude Code oturumu içindir. Üslup testi (`araclar/gpu_test/`) başarılı oldu. Kullanıcı ve başkan kararı: "Van Gogh'a Kim İnandı?" filminin oda planları Blender'la yeniden çizilecek (v4).

Ses, zaman çizelgesi ve plan listesi değişmez. Yalnız görüntü değişir. Bulut oturumu (başkan) çıktıları filme yerleştirir; gri dünya + renkli tablo kuralını ve yazıları o uygular.

Önce şunları oku:
- `CLAUDE.md`: özellikle "Hassasiyet ve hukuk" ve "Dış varlıklar".
- `van-gogh/geriye_bakis.md`: v2 ve v3 bölümlerindeki hassasiyet dersleri.
- `araclar/gpu_test/oda_testi.py` ve `SONUC.md`: kendi testin.

## 1. Kalıcı oda sahnesi (bir kez kurulur, 12 plan kullanır)
Sahne betikle üretilir: `van-gogh/blender_v4/oda_kur.py` → `van-gogh/blender_v4/oda.blend`. Varlıklar `varlik/` altında; `.blend` ve varlıklar `.gitignore`'da.

**Mekân:** Theo'nun Paris dairesi, 1886–1890. Bir oda, iki dekor durumu:
- **Bekâr (A01–D01):** tek kişilik; masa, şövale, raflar, kitaplar, duvara dayalı birkaç tuval.
- **Evli (D06–H01):** aynı oda; masada Jo'nun dikiş sepeti, pencerede perde. G planlarında bir beşik, H01'de taşınma sandıkları.

**Testten gelen üç düzeltme (zorunlu):**
1. **Şövaledeki tablo ışıktan bağımsız gerçek renginde.**
   - Tablo malzemesi emisyon + diffuse karışımı ya da ayrı render katmanı olur; lamba onu turuncuya boyamaz.
   - Karma sürümde karenin en parlak ve en doğru renkli yeri tablo olmalı.
2. **Pencerede dikey koyu şerit dizisi yok** (parmaklık ya da hücre okunuyor).
   - Dönem penceresi: iki kanatlı, küçük camlı, yatay ve dikey kayıtlar ince.
   - İnce perde; dışarıda gece çatıları ve ay.
3. **Figürler dönem kıyafetiyle.** Rocketbox'ın modern takımı yerine aşağıdaki karakterler.

## 2. Karakterler
Yüz serbest, ama yaşayan birine ya da bir oyuncuya benzemesin. Kaynak olarak kamu malı fotoğraf ve otoportreler kullanılır.
- **Theo** (1857 doğumlu; 1886'da 29, 1890'da 33): ince, orta boy.
  - Kısa açık kumral saç, bıyık ve kısa sakal.
  - Koyu redingot ya da uzun ceket, yelek, beyaz dik yaka, ince kravat.
  - Referans: Van Gogh Museum'daki Theo fotoğrafları (Woodbury & Page 1887–1889, kamu malı).
- **Vincent:**
  - Kızıl saç ve sakal, sert yüz hatları.
  - 1887 Paris'inde hasır şapka ve koyu mavi iş ceketi (Met'teki otoportre: `van-gogh/gorsel/otoportre_hasir_sapka_1887_met436532.jpg`).
  - 1890'da (G01, G02, G05) mavi iş ceketi ve hasır şapka.
- **Jo** (1862 doğumlu): koyu saç, ensede topuz.
  - Dik yakalı koyu gri ya da lacivert elbise, bel oturtulmuş, etek bileğe kadar.
  - Baştan ayağa siyah olmasın: örtü ya da çarşaf okunur.
- **Bebek (Vincent Willem, 1890):** kundak açık renk ama beyaz değil (krem ya da açık gri; beyaz kundak kefen okunur). Yüzü görünür.

**Kaynak sırası:**
1. MPFB2 (MakeHuman, CC0) beden + dönem giysisi.
2. Fab, Sketchfab ya da CGTrader'da "Victorian / 19th century" karakter ve giysi (CC BY ya da Standard lisans; satın alma gerekirse kullanıcıya fiyatıyla sor).
3. Gerekirse Blender'da giysi modelleme (cloth sim).

Hareketler için Mixamo kullanılır: kullanıcının Adobe hesabıyla indirilir, ticari kullanıma serbest. Retarget için "Rokoko Retargeting" ya da "Auto-Rig Pro" (ücretliyse sor) gibi araçlar kullanılabilir.

## 3. Planlar
Zaman bilgisi `van-gogh/blender_v4/oda_planlari.json` dosyasında:
- `sure_sn`: planın süresi;
- `sozcukler`: seslendirmedeki her sözcüğün plan içindeki saniyesi (`t`).

Eylemler sözcüğe bağlanır, yani belirtilen sözcüğün `t` anında başlar. Her plan ilk saniyeden hareket eder; donuk plan yok, 5 saniyeyi aşan eylemsiz aralık olmaz.

| Plan | Ölçek | Dekor, ışık | Şövale | Ne olur |
|---|---|---|---|---|
| A01 | geniş | bekâr, gece, lamba | otoportre | Kapak A'nın odası (filmin ilk karesi). Theo şövaleye bakar, sırttan ¾. Kamera tuvale ve lambaya doğru yavaş yaklaşır (%45 yol). |
| B06 | orta | bekâr, öğle güneşi | otoportre | Vincent şövalenin başında boyar; fırçalı kolu hareket eder. Renk kuralı başkanda: tablo "atölye"de (8,8 sn) renklenecek. Kamera hafif kayar. |
| C06 | orta | bekâr, gece | otoportre | Theo masaya eğilmiş mektup okur; "sanatçılara"da (2,96) sayfayı çevirir. |
| D01 | orta | bekâr, kış ışığı | otoportre | Theo ve Jo yan yana pencere önünde. "nişanlanır"da (9,72) Jo bir adım yaklaşır, el ele tutuşurlar. Kamera hafif geri çekilir. |
| D06 | geniş | evli, sabah | otoportre | Taşınma: sandıklar. Jo solda; Theo sağda, "taşınırlar"da (6,18) eliyle yazı masasını gösterir. Kol Jo'ya değil masaya uzanır; kol hiçbir an yatay ve düz olmaz (selam okunur). |
| F03 | yakın | evli, kış, gün | otoportre | Jo kucağında bebekle (bebek ve yüzü görünür). "oğlu"nda (3,40) Theo eğilip bebeğe bakar. Yalnız Theo eğilir. |
| G01 | orta | evli, sabah | Güller (`van-gogh/gorsel/aday/guller_1890_saintremy_met436534.jpg`) | Vincent (hasır şapka) kapıdan odaya girer, yürür, durur. Beşik kadrajda; açık ahşap, sallanma ayaklı, içinde kundak ve bebek. |
| G02 | yakın | evli, sabah | Güller | İki kardeş beşiğin başında ayakta, beşik ön planda. "tığ"da (8,64) Vincent tığ işi örtünün ucunu kaldırıp gösterir, Theo hafif güler. İki adam aynı anda öne eğilmez (namaz safı okunur). |
| G05 | orta | evli, öğle | Güller | "hastalanır"da (2,06) Jo beşiğe eğilir. "ayrılmayı"da (6,56) Theo pencereye döner. "gergin"de (10,58) Vincent kapıya yürür. |
| G10 | orta | evli, gece, lamba | Güller | Theo masada sırttan ¾ oturur. Dirseğinin yanında sarı zarf yığını (Vincent'in mektupları). Kamera omuz üstünden zarflara kayar. |
| G11 | ayrıntı | evli, kış gecesi | Güller | Boş masa, lamba yakın plan. "öldü"de (5,48) +0,6 sn alev kısılıp söner; ardından bacadan ince duman yükselir (sessizlikte tek hareket). Figür yok. |
| H01 | yakın | taşınma sandıkları, kış gün ışığı | Güller | Jo ¾, kucağında bebek. Sandığın üstünde sarı zarf destesi. Duvara dayalı tuvaller arkadan (yalnız çevre çıtası; çapraz çıta haç okunur). Jo bebeği hafifçe sallar. |

**Renk ve maske:** "Vincent'in tabloları ve onun sarı zarfları renkli" kuralını başkan uygular. Senden iki çıktı beklenir:
- **RGB:** tam renkli, fiziksel ışıklı kare.
- **Maske:** siyah zemin üstünde beyaz. Beyaz olanlar: şövaledeki tablo, varsa duvara dayalı Vincent tuvallerinin yüzü, sarı zarflar. Yöntem Object Index ya da Cryptomatte ile tam kenar.
  - Sarı zarf rengi: `#DBA84C` civarı, mat kâğıt.

## 4. Render ve çıktı
- **Ayarlar:** Cycles GPU (OptiX), 1920×1080, denoise.
  - Önce tek karede süreyi ölç.
  - Kare başına ≤ 12 sn tutuyorsa 30 fps, tutmuyorsa 15 fps render et (film 15 çizim/sn'yi 30'a çoğaltıyor; ikisi de olur).
- **Her plan için** baştan ve sondan 0,5 sn pay: `-0,5 sn`'den `sure_sn + 0,5`'e kadar.
- **Klasör yapısı** (`van-gogh/blender_v4/plaka/<PLAN>/`, `.gitignore`'da, depoya girmez):
  - `rgb/0000.png …`;
  - `maske/0000.png …`;
  - `bilgi.json`: fps, kare sayısı, pay, kamera.
- **Depoya girenler** (küçük; başkan bunlarla değerlendirir):
  - `van-gogh/blender_v4/onizleme/<PLAN>_{25,50,75}.jpg`: 960 px, JPEG kalite 85;
  - `van-gogh/blender_v4/onizleme/<PLAN>.mp4`: 640 px, ≤ 3 MB;
  - `van-gogh/blender_v4/RAPOR_1.md`: plan başına süre, kare süresi, kullanılan varlıklar ve lisanslar (ASSETS.md'ye de), sorunlar.

## 5. Sıra
1. Oda sahnesini kur.
2. Karakterleri hazırla.
3. Önce A01 ve G02'yi çiz.
4. Bu ikisinin önizlemesini push et ve kullanıcıya göster. Başkan eleştirir, gerekirse düzeltilir.
5. Kalan on planı çiz.

## 6. Hassasiyet (v2 ve v3'te yakalananlar; tam boy karede bak)
- İki ya da daha çok figür aynı anda öne eğilmez (namaz safı).
- Beşik tabut ya da sedye gibi okunmaz: kapalı kutu yok, koyu renk yok, yastıklı uzun düz yatak yok.
- Ayaklar yere basar; havada ya da asılı beden okunmaz.
- Baş gövdeden kopuk görünmez.
- Kundak beyaz değil.
- Şövale ve tuval çıtasında kesişen iki çubuk (haç) yok.
- Kan gibi okunan kırmızı leke yok.
- Erkeğin kolu kadının beline ya da kalçasına uzanmaz.
- Siyah giysiye beyaz dikdörtgen yaka konmaz (papaz yakası okunur). Beyaz dik yaka ince ve kravatlı olur.
- CLAUDE.md'deki "Görüntüde yakalananlar" listesinin tamamı geçerli.
