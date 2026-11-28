# Van Gogh'a Kim İnandı?: geriye bakış (üretim sırasında yazılır)

## Hat
- **Motor:** `araclar/tablo` (canlanan yağlıboya) ilk kez tam filmde. Setler `lib/set_*.js`, planlar `lib/planlar.js` (A–B) ve `lib/planlar2.js` (C–I), çekim sistemi `lib/film_t.js` (cümleye ve kelimeye bağlı plan: `A('C04@sarı')`).
- **Karma üslup tek kuralla:** finish geçişinde grisaille (`mono: 1`) + ekran uzayında **renk örtüsü** (`finish({maske})`, 480×270 tuval; beyaz = renkli kalır). Tablonun gri dünyadan renge açılması, zarfların renkli kalması, badem dalı: hepsi örtü çizimi. Ayrı renk katmanı gerekmedi.
- **Gerçek tablo = darbe katmanı:** `tabloCiz` resmi Ref tuvaline basar, `paintRef` darbe yönünü resmin değer kenarlarından alır. Fotoğraf yapıştırılmış gibi durmuyor; dünyayla aynı kabartma.
- **Tablo dünyası:** Vincent'in tablosu gri olarak sahnenin kendisi (C04 Sarı Ev, E01 Selvili tarla, G06 Fırtınalı gök); "sarı"/"tarlaları" sözcüğünde renk örtüyle yayılır. Fikir görüntünün kuralı: dünya ancak Vincent'in resminde renklenir.
- **Figürler Blender'da, sahneden bağımsız klip:** `blender/klip.js` (iskelet + hareket) → `figur_bpy.py` → saydam kareler; sahneye `figurBas(ayak, boy)` ile 2B yerleştirilir. Yürüyüş gibi perspektif isteyen planlarda set kamerasıyla ayrı klip (`theo_louvre`).
- **Seslendirme:** 9 bölüm × 2 çekim (15.784 kredi). Kelime zamanları **faster-whisper** ile kredisiz (`tools/transcribe_fw.py`; openai-whisper kapta yok, model HuggingFace'ten). Rakamlar Türkçe okunuşa açılır, karşılaştırma senaryoyla.

## Kurgu özetinde yakalananlar (hassasiyet)
- Tığ işi örtü: yatay ve dikey kısa darbeler dönüşümlü → **küçük artılar (haç)**. Örtü yumuşak tümsek darbesine döndü.
- Koyu dikdörtgen beşik → **tabut** okunabilir. Açık ahşap, kavisli sallanma ayağı, baş ucu kubbesi.
- Şövalenin tuval rafı ayağı kesiyordu → **haç**. Ayaklar tepede birleşir, raf yalnız aralarında.
- H07 taş duvarın üstünde sıra hâlinde koyu sarmaşık lekeleri → **mezar taşı sırası**. Kaldırıldı.
- Müze vitrini koyu gövde + sarı-siyah dizi → **ikaz bandı**. Açık ahşap, cam, aralıklı zarflar.
- Erkek figürde başın arkasına eklenen saç parçaları büyük planda **topuz** (kadın) okunuyordu. Baş tek parça saç renginde.
- Ders (Stanford'la aynı): bu tuzakları plan yazarken biliyordum, yine de karede gördüm. Tarama tam boy karede yapılır.

## v2: çok ajanlı eleştiri (dört mercek + çürütme; 30 bulgu, 24'ü geçti; `v2_duzeltme_listesi.md`)
- En değerli bulgular hassasiyetteydi:
  - görünmeyen ağacın tarlada kalan gölgesi, mezar cümlesinin yanında tek koyu tümsek oluyordu;
  - şövaledeki otoportre her odada tekrarlanınca anma köşesine dönüyordu;
  - "TEK KİŞİ İNANDI" kapağı filmin kendi "iki cevap" teziyle çelişiyordu.
- Düzeltme yeni simge üretti (Lale dersi bir kez daha): beşiğe eğilen iki kardeş, yan yana iki eğik siluet olarak **namaz safı** okundu. Ayakta duruşa dönüldü. Kural: iki ya da daha çok figür aynı anda öne eğilmez.
- Jo'nun gölgesi ilk denemede masada dikilen iri bir hayalet oldu; düşük alfa, sık darbe ve kenardan girişle "gölge" okunuyor.
- Masa filmin %37'siydi: ışık mekâna ve zamana göre ayrıldı (gece lamba, gün pencere, bugün müze).

## v3: render edilmiş filmin eleştirisi (üç izleyici kişiliği + tam boy tarama + teknik; `scratchpad/v3_sentez.md`)
- Üç izleyicinin ortak düşüşleri hep aynı türdendi: **eylemsiz bilgi planı.** Boş masa (B05, D02), boş koridor (F06–F08), boş defter (H03), kara tahta gibi okunan cilt (H06). Düzeltme her seferinde sözcüğe bağlı bir olay oldu: tablo duvardan iner, satırlar dolar, sayaç akar, zarfların yarısı solar.
- Kanal kuralı ("somut olay tutar") plan yazarken uygulanmış gibiydi; plan notu "satış etiketi asılır" diyordu ama etiket 46 piksellikti. Ders: not karede ölçülür, notta değil.
- Hassasiyette yeni tuzaklar:
  - kırmızı yorgan yağlıboya süzgecinde dokusuz düz bir lekeye döndü (kan okuması);
  - bileğe inen koyu palto + düz geniş şapka papaz okundu (Gauguin);
  - açık renk eller şişe ya da kutu okundu;
  - gri, çerçeveli portre siyah-beyaz anma fotoğrafı okundu.
- Renk kuralı netleşti: renklenen tablo griye dönmez (`uretim_plani.md` §7).
- Badem dalı çizim yerine tablonun kendisinden kesildi (turkuaz gök anahtarlandı); kanca ile doruk aynı dalı paylaşır.

## v4 denemesi: Blender (28 Kasım), kullanıcının kararıyla bu videoda kapandı
- Önce saf Blender denendi (kullanıcının RTX 4070'i, Cycles, MakeHuman, Poly Haven). Işık ve malzeme iyiydi; ama görüntü "oyun gibi" okundu.
  - Kot pantolon, kovboy şapkası, pençe eller, plastik bebek.
  - Gerçekçi odada Vincent'in tablosu poster gibi duruyordu; kavram (gri dünya, renkli tablo) aynı boyayı gerektiriyor.
- Kıyas (dört mercek) hibriti seçti: dünya bizim motorla, figür Blender'dan, motor darbeye çevirir.
  - Kapı klipleri geldi. Yüz, şapka ve oranlar daha iyiydi; ama giysi beden yüzeyi şişirilerek üretildiği için omuzlar apolet gibi kabardı.
  - Kullanıcı yan yana bakınca v3'ü daha çok beğendi ("bizimki daha sanatsal ve orijinal").
- Ders:
  - Kanalın imzası yağlıboya motoru.
  - Gerçekçilik kaliteyle aynı şey değil.
  - Yeni bir hat ancak kör kıyasta kullanıcının gözünü geçerse filme girer.
- Figür kenarı denemesi: pürüzsüz normal + kenara paralel iç darbe boncuk dizisini kaldırdı. Ama iç kenarlarda kesik koyu-açık çizgiler doğurdu; ense yüz gibi okundu. Geri alındı.
- Aynı turda kaynak düzeltmesi geldi: Met otoportresi ve Güller Theo'nun dairesinde değildi. Şövaleler tarih tarih belgeli tablolarla değişti (DOGRULAMA §8).

## Ses
- Müzik özgün sentez (`audio/score.py`, zarf motifi). Düzey eğrisi: medyan −33 dBFS; telefon bandında saniyelerin %87'sinde duyuluyor. İlk ölçümde tren ostinatosu (re2) ve telgraf tremolosu telefon bandının altındaydı; üst oktav eklendi. Bilerek sessiz: G09 "öldü" ve G11 lamba söner.
- Efektler ElevenLabs (8 × 4 çeşitleme, 544 kredi).

## Açık işler
- VGM kaynaklı tablolar (Badem Çiçeği, Sarı Ev, Fırtınalı gök, 1888 Yatak Odası, Yıldızlı Gece) Commons PD-Art'tan bekleniyor; gelmezse yer tutucu planlar yeniden düşünülür.
- Render süresi: tek işçide ~2,5–4 sn/çizim (ss 1,5), 15 çizim/sn × 599 sn ≈ 9.000 çizim.
