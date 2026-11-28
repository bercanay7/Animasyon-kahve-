# GÖREV v4-3: Kapı görevi, Blender yalnız figür üretir (Y4)

Bu görev bilgisayardaki (RTX 4070) Claude Code oturumu içindir. Önce iki belgeyi oku:
- `van-gogh/blender_v4/YOL_KIYASI.md`: karar ve gerekçe.
- `van-gogh/blender_v4/GOREV_2_duzeltme.md`: ilk partinin eleştirisi. Varsa figürle ilgili maddeleri uygula; oda, ışık ve renk maddeleri artık geçersiz.

## Karar (kullanıcı ve başkan, 28 Kasım)
Saf Blender görüntüsü "oyun gibi" okundu. Kanalın imzası bizim yağlıboya motoru: `araclar/tablo`, bulutta.
- **Dünya ve tablolar kodla kalır:** oda, masa, salon, tablo dünyaları.
- **Blender yalnız figür üretir:** dönem giysili, düzgün elli insanlar, saydam arka planlı klip kareleri.
- Bu kareleri bulutta motor fırça darbesine çevirir (`araclar/tablo/figur.js` `figurDarbe`), v3'teki Blender kliplerinin yerine geçerler.
- Oda, eşya, ışık havuzu, renk ve şövaledeki tablo Blender'dan **gelmez**.

## Mevcut hatla birebir uyum (zorunlu)
v3'teki klipler `van-gogh/blender/klip.js` + `figur_bpy.py` ile çizildi. Yeni klipler aynı sözleşmeye uyar; motor değişmeden yerine takılır.
- **Poz ve hareket:**
  - Her klibin iskelet verisi depoda: `van-gogh/blender/klip_<ad>/eklem.json`. A01 için `van-gogh/blender/eklem_oda.json`.
  - Yapı: 121 kare, 15 fps; her karede pelvis, göğüs, boyun ve baş çerçeveleri; bacak ve kol eklem konumları.
  - Eksen: bizim dünya (x sağ, y yukarı, z kameraya doğru) → Blender (x, −z, y). `figur_bpy.py`'deki `B()`.
  - MPFB2 karakterini bu eklemlere oturt: kök ve gövde yönü çerçevelerden; el ve ayak için IK hedefleri eklem konumları. `poz.py` buna hazır.
  - Hareket aynı kalmalı. Daha doğal yapmak istersen (parmak, omuz) eklem konumlarından sapma 3 cm'yi geçmesin.
- **Kamera:**
  - Klipler için `van-gogh/blender/klip_<ad>/kamera.json` (konum, hedef, dikey fov).
  - A01 için `van-gogh/blender/kamera_oda.json`.
  - Çözünürlük **960×540**, saydam arka plan; `figur_bpy.py` ile aynı kamera kurulumu.
- **Çıktı, eski klasörün yanına:**
  - Klasör `van-gogh/blender/v4_klip_<ad>/`:
    - `kare/k_0000.png … k_0120.png`: RGBA, 8 bit.
    - `normal/n_0000.png …`: kamera uzayında normal; RGB = (n·0.5 + 0.5).
    - `kimlik/i_0000.png …`: düz renkli nesne kimliği. Ten (255,0,0), saç ve sakal (0,255,0), giysi (0,0,255), beyaz yaka ve gömlek (255,255,0), şapka (255,0,255), elde tutulan nesne (0,255,255).
    - `bilgi.json`.
  - Depoya girer: 960×540 ve çoğu saydam olduğu için küçük. Klip başına 20 MB'ı geçerse kare dosyalarını `pngquant`'la ya da yalnız figürün kutusuna kırparak küçült; kırpılan kutuyu `bilgi.json`'a yaz.

## Görüntü
- **Render:** Cycles 32 örnek + OptiX gürültü giderme. Motor zaten darbeye çevirdiği için yüksek örnek boşa gider.
- **Malzeme:** gerçek değerler, doku yok ya da çok hafif.
  - Koyu takım koyu, yaka beyaz, ten orta, saç koyu (Vincent kızıl).
  - Motor bunları griye çevirip değer farkından boyar. Değer farkı önemli, desen önemli değil.
- **Işık:** klibin `kamera.json`'undaki ışık.
  - Dış klipler: `dis.gunes` yönü ve gücü, `ortam`.
  - A01: `isik` (lamba konumu, renk, güç).
- **Saç, sakal, kumaş:** sade. Her tel değil, kütle. Darbeye çevrilince kütle okunur.

## Hazır şablon değil, kendin modelle (kullanıcının kararı, 28 Kasım)
Hazır giysi ve aksesuar şablonları "oyun gibi" ve dönem dışı çıktı: kot pantolon, ofis blazeri, kovboy şapkası, karton örtü. Bundan sonra:
- **Beden (anatomi, rig):** MPFB2 ya da MakeHuman tabanı yalnız başlangıç noktası olarak kullanılabilir. Yüz ve oran kaynağa göre elle düzeltilir:
  - Vincent: otoportreleri (sert elmacık, çökük yanak, kızıl sakal);
  - Theo: 1887–1889 fotoğrafları;
  - Jo: 1889 fotoğrafı.

  Yüzler yaşayan birine benzememeli.
- **Giysi, şapka, aksesuar:** Blender'da sen modellersin. Hazır şablon kullanılmaz; kullanılırsa tanınmayacak kadar değiştirilir.
  - Dönem kalıbından yola çık: redingot ya da 1880'ler ceketi, yelek, dik yaka, işçi önlüğü ya da iş ceketi (*bourgeron*), bol pantolon.
  - Yöntem: kalıp parçalarından dikiş (Blender *Cloth* + *Sewing*) ya da elle modelleme + *Solidify* + *Subdivision*, sonra kumaş simülasyonuyla doğal kıvrım.
  - Hasır şapkayı örgü dokusu ve alçak tepesiyle modelle.
  - Toplu görevde Jo'nun elbisesi ve bebeğin örgü battaniyesi de böyle.
- Referans görseller (kamu malı otoportre ve fotoğraflar) `varlik/referans/` altında durur; depoya yalnız künyeleri girer.
- Kullanıcı kararıyla bu iş daha uzun sürebilir; kalite önce gelir. Ama kapı yalnız üç klip: önce bunlar.

## Karakterler (dönem doğru, CLAUDE.md "Figür" kuralı)
- **Theo:**
  - Koyu takım, yelek, beyaz dik yaka ve kravat. Yaka V biçiminde açık, kravat görünür.
  - Siyah giyside küçük beyaz dikdörtgen olmasın (papaz yakası okunur).
  - Kısa açık kumral saç, bıyık ve kısa sakal.
- **Vincent:**
  - Bol kesim mavi iş ceketi ve bol koyu pantolon; kot dokusu yok, dar kesim yok.
  - Alçak tepeli, geniş kenarlı, açık renk hasır şapka, başa oturur (kovboy şapkası değil).
  - Kızıl saç ve sakal.
- **Jo** (bu kapıda yok, toplu görevde): dik yakalı koyu lacivert elbise, ensede topuz; baştan ayağa siyah değil.
- **Eller:** nesne tutar ya da gevşek durur; pençe pozu, gergin açık parmak yok.

## Kapı klipleri (yalnız bu üçü; sonra dur, rapor ver)
| Klip | Plan | Eklem | Kamera | Not |
|---|---|---|---|---|
| `theo_oda` | A01 | `blender/eklem_oda.json` | `blender/kamera_oda.json` | Theo sırttan ¾ şövaleye bakar; sağ elinde bir zarf. |
| `theo_dur` | G02 (B01 ve başka planlarda da kullanılır) | `blender/klip_theo_dur/eklem.json` | `…/kamera.json` | Ayakta, sırttan ¾. |
| `vincent_goster` | G02 | `blender/klip_vincent_goster/eklem.json` | `…/kamera.json` | 2–3,2 sn arası sol eliyle aşağıyı gösterir; parmaklar doğal. |

## Rapor ve sonra
- `van-gogh/blender_v4/RAPOR_3.md`: kare süreleri, varlıklar ve lisanslar (`araclar/ASSETS.md`'ye de), sorunlar.
- Üç klibin 0., 40. ve 80. karelerinden `onizleme/` altına 960 px JPG (gri zemin üstünde).
- Commit ve push; Türkçe mesaj, CLAUDE.md biçiminde.
- Başkan klipleri bulutta motora takıp eski v3, yeni Y4 ve oda_karma'yı yan yana kıyaslar. Kapı geçerse toplu klip görevi (`GOREV_4`) bir JSON listesiyle gelir.

## Hassasiyet
`CLAUDE.md` listesinin tamamı ve `GOREV_1_oda.md` §6 geçerli. Bu kapı için özellikle şunlar:
- papaz yakası;
- pençe el;
- şapkanın hale ya da kovboy şapkası gibi okunması;
- baş gövdeden kopuk;
- havada asılı ayak.
