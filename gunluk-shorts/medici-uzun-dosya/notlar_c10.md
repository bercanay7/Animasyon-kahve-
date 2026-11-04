# notlar_c10 — Rahip ve Kral (Parça 5 / c10) · sahne yazarı notları

Dosyalar: `scenes_c10.py` (36 çekim, `YIL_AT`), `c10_kinds.py` (özel tür/oda/istasyonlar), `p5_lib.py` (Parça-5 ortak kitaplığı: sarmalayıcılar, bindirme kurucuları, siluet madalya, haritaya bağlı parçalar), `yonetmen_c10.md` (yönetmen kartı).
Önizleme: `python3 preview_chapter.py c10 --shots N -k K --cols C` · kapılar: `python3 preview_chapter.py c10 --check|--flow` · örneklemeli: `python3 qa_flow.py --part 5 --chapters c10 --workers 1`.

## Kapı sonuçları (örneklemeli qa_flow, 1 işçi)
8 GEÇTİ · 0 KALDI · 3 UYARI · 1 PAS. Durgunluk 0,0 sn (≤1,5) · kamera %100 (36/36) · hareket yeterliliği 0 zayıf · gerekçeli geçiş %100 (çıplak fade %0, çıplak kesme 0) · tür tekrarı 0 ihlal · çapa: sözcük 116 / cümle 68 / mutlak 2 (%1) · olay yoğunluğu %97 · altyazı bölgesi 0 ihlal.
UYARI'lar: (1) çekim uzunluğu medyan 6,3 sn (ağır bölüm bandı kayar); (2) yön: #22 aynada ters alay (bilinçli yön bozma, yönetmen kartında gerekçeli); (3) yönetmen kartı (`yonetmen_c10.md` yazıldıktan sonra kapanır).
ms/kare: çekim ortalaması ≈150 ms (hedef ≤250); en ağır: `c10_plan` ≈360 ms (parşömen + gölge), `p5_oda careggi` ilk kare ≈370 ms (kareaş ısınması).

## Kısıtlar (nasıl uygulandı)
* **Ekrana yalnız seslendirilen sözcükler** (ad/tarih/sayı): Piero, Capponi, Corsini, Bernardo del Nero, 9 Kasım 1494, 17 Kasım, 7 Şubat 1497, 7 Nisan 1498, 23 Mayıs 1498, 3.000+, 60 YIL ÖNCE, 1434/1494… Eski brif'in "Ferrara", "24 NİSAN", "San Marco" (s8) etiketleri **gösterilmedi** (söylenmiyor). "SAN MARCO" yalnız s33'te.
* **Kaynak damgaları:** ANEKDOT (s5, s9, s21, s22, s27) gravürde/mono; ○ TEK KAYNAK (s15 Corsini, s17 Bologna); YORUM (s30). KANIT YOK yalnız s27 şakasında (boş yaldızlı çerçeve: Botticelli resmi **çizilmedi**).
* **Şiddet/yüz:** kral, kardinal, papa, Savonarola, Piero = siluet madalya ya da kâğıt-kukla profil; idam gösterilmedi: s31 mumlar söner, s34 `meydan odun` darağacı siluet + ip çizgisi (beden yok); Piero'nun kaçışı yaya koşu (at yok: "atına atlayıp" ANEKDOT söylenmez).
* **Çan/saat/şafak/koku iddiası:** yalnız kaynakta olan: "şafağında" (s34, pencere ışığı) ve "çanlarla" (s22, görsel halka); `pano nave` kürsü çekimlerinde `st_bell` YOK (özel `stations`).
* **Mizah:** yalnız s27 (Botticelli yaktı → boş çerçeveler → KANIT YOK); s28 kaynaklar "geç ve zayıf" aynı şakanın ikinci vuruşu (kesikli, kopuk iplik).
* `sfx_cues_p5.json`'a dokunulmadı; özel ses istekleri `yonetmen_c10.md` içinde.
* Ses geçici (Piper): tüm zamanlar cümle/sözcük çapalı; 2 mutlak saniye (açılış 0 ve bir geçiş).

## Bilinen kusurlar
1. Kâğıt-kukla figürlerin yüzü (FA kiti) soyut profil; adlı kişiler levha ile ayrılır, portre iddiası yok. Kral/Piero için siluet yerine renkli kukla kullanıldı (s14–s17, s21): "yüz yok" kuralı madalya/siluet çekimlerinde tam, kukla çekimlerde soyut.
2. s9 galero ve s13 kale simgesi sayısı: kaynaklar 4–5 arası çelişir, script söylemez → 4 simge çizildi, sayı yazılmadı.
3. `oda careggi` gece tam ay diski (pencere) ↔ dış çekimde hilal: iç/dış ayrı çizim, ayrı kareaş.
4. Madalya siluetlerinde tiara kutu gibi, sakal zor seçilir (`sil_medal`); c11'de tiara/camauro yalnız madalya içinde, küçük.
5. s26 Kibirler: eşyalar stok `ates` taşıyıcılarıyla uçar (küçük); listedeki "kozmetik" ve "resim/heykel" yalnız levha (görsel eşya yok).
6. `c10_kilik` kardinal→rahip geçişi sövenin ardında kısa solma; fark çok küçük kamerada belirgin değil.
7. İlk çekimin orta bandı (1,2–4,8 sn) başlık bindirmesi için boş bırakıldı: `c10_tepe` yalnız tarih plakası ve ad levhası kenarlara yakın.

## Motor istekleri
* Stok `oda`, `pano`, `sehir` kinds'ına `after=` bindirme kancası (şu an `p5_lib.WOv/PanoProbe` ile dünya-uzaylı bindirme yeniden kuruluyor; cams açıkça verilmek zorunda).
* `cilt_cam.OWN_CAMERA` içine `map` ve `procession`'ın kendi kamerası olarak eklenmesi (qa_flow "cam= yok" uyarısını `cam=("push",…)` ile susturuyoruz; çift hareket riski).
* `FA.rider` için taç/miğfer başlığı ve zambak (`lily`) desen sözlüğü (şu an `fleur`, `beret`).
* Madalya siluet (`sil_medal`) çekirdeğe taşınsın (Parça 6–7 de kullanabilir).
