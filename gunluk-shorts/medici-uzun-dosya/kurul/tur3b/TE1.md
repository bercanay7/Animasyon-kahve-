# TE1 — Tur 3b: Medici P1 v3.1 gerileme kontrolü · Render ve kodlama denetçisi

**Sınırım:** Videoyu oynatamadım, sesi dinleyemedim. Her şey ölçüme dayanıyor:
- ffprobe/ffmpeg, x264 SEI, MP4 kutuları;
- 14.437 karenin ve 13 segmentin tamamının kare MD5'i;
- motorla çizdiğim kaynak kareler (render sonrası kod değişmemiş: 17:20'den sonra değişen `.py` yok);
- çözülmüş karelerin sayısal ve görsel incelemesi.

Dosya: `out_p1/medici_P1.mp4` (v3.1, 862.197.959 bayt, 5 Kas 17:54).

## 1. Karar

**ONAY — 9,4 / 10** (tur 3: 9,1).
- Tur 3'teki yeni maddem Y9 (doku ayna dikişi) kapandı. Süreç maddeleri Y11 ve §8 ile seviye maddesi Y6 kapandı.
- v3.1'in benim alanımda bir gerilemesi yok: birleşim, determinizm, renk, ses, bantlaşma ve bit hızı v3 düzeyinde ya da daha iyi.
- Puanı tavana çıkarmayan küçük şeyler:
  - birleştirme öz sınaması renk matrisini piksel düzeyinde değil yalnız etiketten denetliyor;
  - anahtar-kare nabzı (görünmez) aynı.

## 2. Tur 3 maddelerimin durumu

| # | Madde (tur 3 önemi) | Durum | Kanıt (v3.1) |
|---|---|---|---|
| Y9 | Kâğıt dokusunda ayna dikişleri (önemli) | **KAPANDI** | **Videoda, eski dikiş sütunlarında ayna korelasyonu:**<br>110,0 sn gökyüzü bandı (y 360–460) x=1537: **−0,015** (v3: 0,508; bant medyanı −0,005).<br>292,5 sn harita denizi x=1491: **0,071** (v3: 0,257; bant p99 0,084, yani gürültü içinde).<br>**Karo gerçekten periyodik:** `compose.tooth_periodic()` 3840×2160; sarma sınırında komşu farkı x 6,00 / y 6,60, içeride 5,84 / 6,31. Bitişik sütun korelasyonu sarmada 0,585, içeride medyan 0,598. Yani sarma dikişi de yok.<br>Aynı bantta kalan yüksek değerler (110,0 sn x≈1425 / 1753 / 1777) içerikten geliyor: simetrik kuş çizgisi ve direk. ENG-E'nin "x≈1754 içerik aynası" notu da direk; set kenarı aynalaması değil (`f110_crop.jpg`). |
| Y11 + §8 | Kod özeti ve birleştirme öz sınaması (süreç) | **KAPANDI** (küçük kalıntı) | 13 `.done` dosyasının hepsinde `887ba3df1637` (çizelge = `sha1(timeline.json)`) ve **`ae58fa355abb` (kod)**.<br>`cmd_concat` şunları birleştirmeden önce/sonra denetliyor (kodu okudum; uyuşmazlıkta duruyor):<br>• çizelge özeti;<br>• tek kod özeti;<br>• segment akış imzası (profil, seviye, boyut, piksel biçimi, renk etiketleri, fps);<br>• birleşik dosyada kare sayısı = plan;<br>• BT.709/tv etiketi.<br>**Kalıntı (küçük):** renk denetimi yalnız etiket. v1'deki hata etiket doğruyken matrisin yanlış olmasıydı; 8 yamalı sentetik piksel testi hâlâ yok. Günlükteki "ref 1" ffprobe'un akış alanı, SPS'teki başvuru sayısı değil (SEI'de `ref=4`); yanıltıcı ama zararsız. |
| Y6 | H.264 seviye 5.0 (küçük) | **KAPANDI** | ffprobe `level=41`, avcC seviye baytı 41, SEI `ref=4`. Diğer ayarlar aynı: CRF 19, `aq=3:1.00`, `psy_rd 1.00:0.15`, VBV 24M/48M. |
| Y10 | Karanlık bitiş ekranında hafif bantlaşma (küçük) | **KAPANDI** (iş yapılmadı; ölçüm iyileşti) | 1204 kare tarandı. Düz-degrade payı:<br>• p90 %0,63 (v3 %0,66);<br>• p99 %2,75 (v3 %2,86);<br>• en kötü %4,91, 600,0 sn (v3 %5,57);<br>• >%5 olan kare **0** (v3: 2).<br>Blok oranı medyan 0,956, p99 1,13 (v3: 0,958 / 1,11). |
| Y12 | Karmaşık karelerde SSIM / bit hızı (küçük) | **KAPANDI** (bedel kabul) | Video 11,26 Mb/sn (v3: 11,11). Saniye bazında p99 27,6, en yüksek 44,2 Mb/sn (66. sn).<br>VBV tamponu en az 17,4/48 Mb, alt-akış yok. |
| 7 | Anahtar-kare nabzı (küçük) | **KISMEN** (değişmedi) | İş istemedim; görünür değil. |

## 3. v3.1 gerilemeleri: yok

**Birleşim ve determinizm:**
- 13 segmentin kare MD5 dizisi finalin 14.437 karesiyle birebir aynı; özdeş ardışık kare yok.
- Tek SPS/PPS, tek x264 ayar dizisi; 12 birleşimin hepsi IDR; PTS adımı sabit.
- 12 birleşimde soğuk çizim ile sıralı çizim yeni deklanşör ipuçlarıyla da **bit-birebir aynı** (12/12; çizimlerin 10'unda bulanıklık açık, N=3/5/7).
- Videodaki birleşim kareleri çizimle 37,0–41,0 dB örtüşüyor.

**Renk:** 12 birleşim karesinin hepsinde PSNR(709 çözümü) > PSNR(601 çözümü): +0,4 … +2,9 dB. Etiketler 709/709/709/tv; `pasp` 1:1; dil `tur`; faststart (`moov` 32).

**Süre ve ses:**
- Video 14.437 kare / 601,542 sn; ses 601,530 sn: fark 11,7 ms.
- Ses akışı `mix_audio.m4a` ile paket düzeyinde birebir aynı (MD5 e4b376d6…). v3'ten farklı, çünkü geçiş sesleri yeniden üretildi (59 cue); anlatım ve çizelge aynı.
- −14,1 LUFS, LRA 3,5 LU, gerçek tepe −1,5 dBTP; örnek tepe −1,56/−1,52 dBFS; kırpma 0; DC −3,7e-4; L/R korelasyonu 0,991.
- Başı ve sonu temiz: ilk örnek 3,7e-4; son 250 ms −82 dBFS.

**Deklanşör ipuçları (AN1-Y7), maliyet ve yan etki:**
- **Maliyet:** segment sürelerinin toplamı 3.815,6 işçi-sn (v3: 3.915,9), yani −%2,6. Ek alt örnekleri dokunun hızlanan çarpıtması dengeliyor. En çok ipucu alan segment 0 (c0): 528,7 → 514,2 sn. c2'nin 9. segmenti +%5,9 (SCN-3 sahne değişiklikleriyle birlikte).
- **Görsel sınama:** 30,42 / 30,79 · 41,92 / 42,00 · 95,29 / 95,42 · 236,25 / 236,42 · 290,71 · 300,92 · 309,13 · 331,58 sn (`shutter_events.jpg`). Ayrıca 290,6–290,8 sn sikke yayı ve 300,8–301,0 sn uçan kitap 1:1 (`small_objects.jpg`).
  - Bulanıklık sürekli; ayrık kopya, hale ya da boşluk doldurma dikişi görmedim.
  - "N GÜN" sayacında hayalet rakam yok (30,79 sn "84" keskin).
- **Bantlaşma** gerilemedi (yukarıda). Doku dikişi yok (Y9).

## 4. En emin olmadığım nokta

1. **Y9'u yalnız iki sütunda, tam görüntüyle ölçtüm.** Gerisi analitik: karo periyodik ve sarma sınırı ölçülebilir bir iz bırakmıyor. Kâğıt dokusunun başka bir karede başka bir nedenle (ör. çok büyük ölçek, k > 1,6'daki yavaş yol) iz bırakmadığını her karede görmedim.
2. **Deklanşör ipuçlarının bütün olay karelerine bakmadım.** 12 karede ve 1:1 iki dizide baktım; ENG-E'nin ≈400 karesinin hepsine bakmadım.

Kanıtlar (JPEG, her biri ≤1 MB):
- `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/te1v31/shutter_events.jpg`
- `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/te1v31/small_objects.jpg`
- `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/te1v31/f110_crop.jpg`
