# TE1 — Tur 3: Medici P1 v3 · Render ve kodlama denetçisi

Mercek aynı: renk matrisi ve etiketler, kare hızı ve ritmi, segment birleşimleri, bandlaşma/blok/gren, bit hızı ve yükleme uygunluğu, ses ölçümü, faststart ve konteyner, kare kusurları.
Bu turun işi: tur 2 koşullarımı ve 6. bölümdeki gerileme listemi v3'te tek tek sınamak.

**Sınırım:** Videoyu oynatamadım, sesi dinleyemedim. Her şey ölçüme dayanıyor:
- ffprobe/ffmpeg, MP4 kutuları, x264 SEI;
- 14.437 karenin ve 13 segmentin tamamının kare MD5'i;
- motorla tek tek çizdiğim kaynak kareler;
- çözülmüş karelerin sayısal ve görsel incelemesi.

Değerlendirilen dosya `out_p1/medici_P1.mp4` (v3, 851.012.599 bayt, 5 Kas 08:48).

## 1. Karar

**ONAY — 9,1 / 10** (tur 1: 8,0 · tur 2: 8,7).

Tur 2'de ONAY için koyduğum koşulların hepsi kapandı; v3'te kendim ölçtüm:
- sikke dikişi ve yarım sikke yok;
- friz/plaka kenarı kapalı;
- yazı çakışması yok;
- segment başında deklanşör kararı 12 birleşimin hepsinde sıralı çizimle bit-birebir aynı;
- 13 segment tek zaman çizelgesinden üretilmiş;
- birleşim kayıpsız.

Renk, kodlayıcı, süre ve ses de yerinde.

Puanı 9,4 yerine 9,1 tutan şey yeni bir gerileme (**Y9**): dünyaya kilitlenen kâğıt dokusu, kaynak dokunun sınırını aşınca `BORDER_REFLECT` ile aynalanıyor.
- Örneklediğim karelerin %44'ünde ekranda bir ayna dikişi var.
- Düz alanlarda (gökyüzü, harita denizi, duvar) büyütmede görünür bir "fermuar/katlanma" çizgisi bırakıyor.
- Önemli, ama engelleyici değil: 1× izlemede ince, telefonda görünmez.
- Düzeltilirse P1'in **tamamı** yeniden üretilmeli (gerekçe Y9'da).

## 2. Tur 2 maddelerimin durumu

### 2a. Tur 2'deki ONAY koşulları ve yeni sorunlar (Y1–Y8)

| # | Tur 2 maddesi (önem) | Durum | Kanıt (v3) |
|---|---|---|---|
| Y3 | Sikke dikişi / yarım sikke (engelleyici) | **KAPANDI** | 302,29 · 302,42 · 302,58 sn (n=7255/7258/7262) ve 118,0 sn (n=2832): sikke tek parça, sert dikey sınır yok. 113,21 sn'de yalnız zoomthru geçişinin bulanık bindirmesi var. Kanıt: `v3_coin.png`. |
| Y5 | Fresk plakasının sağ kenarı açılıyor, 216,8–219,5 sn (önemli) | **KAPANDI** | 214,6–219,4 sn arası 6 karede sağ kenar dolu (x 1440–1920 şeridi). Kanıt: `v3_edge.png`. |
| Y4 | "EVLİLİK ÇEYİZİ" × "1.500", 306,8–307,2 sn (önemli) | **KAPANDI** | 306,4 · 306,8 · 307,2 · 307,6 sn: etiket kalkmış, çakışma yok. Kanıt: `v3_overlap.png`. |
| Y1 | Segment başında deklanşör (200,0 sn tek keskin kare) | **KAPANDI** | 12 birleşimin hepsinde (1200 … 14400) kare iki yoldan çizildi: soğuk (yeni `_sprev`) ve sıralı (n−2, n−1, n). **12/12'de MD5 aynı.** Bu çizimlerin 10'unda deklanşör çalıştı (N=3/5/7).<br>Videodaki birleşim kareleri bu çizimlerle 37,0–41,0 dB örtüşüyor.<br>Çizimden bağımsız sağlama: 199,83 · 200,00 · 200,17 sn karelerinde yön bağımlı bulanıklık oranı 0,70 / 0,69 / 0,70 (durgun karelerde 0,93). Birleşim karesi komşularıyla aynı bulanıklıkta.<br>Not: hem `render.py` n0−1'i çizip atıyor, hem `compose._shutter` önceki an eksikse onu kendisi çiziyor. |
| Y2 | 0–6. segmentler eski çizelgeyle | **KAPANDI** | 13 `.done` dosyasının hepsinde özet `887ba3df1637` = `sha1(out_p1/timeline.json)[:12]`. `cmd_concat` özet farkında duruyor (kodu okudum).<br>İlerleme çubuğu birleşimlerde sürekli: çizimde beklentiden sapma ±0,15 px, videoda ±1,5 px (kodek gürültüsü). v2'deki 350 sn'deki 3,6 px'lik geri sıçrama yok. |
| Y7 | Madalya gölgesinin kesik kenarı (küçük) | **KAPANDI** | 529,0 sn madalya çevresinde yüksek geçiren filtrede düz dikey kesik çizgi yok. En güçlü dikey kolon, sağdaki levhanın kendi çerçevesi (x≈1009). |
| Y8 | Ekran uzayında sabit doku + 6 karelik gren döngüsü (küçük/üslup) | **KAPANDI** (ama yeni gerileme: Y9) | **Doku içerikle birlikte gidiyor.** Ölçüm: ince doku korelasyonu, sıfır kaymada / içerikle birlikte kaydırıldığında.<br>187,5 sn: 0,046 / 0,205 (v2: 0,339 / 0,066). 324,2 sn: −0,012 / 0,268 (v2: 0,148 / 0,180).<br>Paralakslı panoramalarda (59,2 ve 110,0 sn) sonuç belirsiz: doku ana düzleme bağlı, benim ölçtüğüm katman başka.<br>**HUD ve levhalar:** HUD'da doku kaymıyor (sıfır kaymada korelasyon 0,995–0,999). 188 sn'deki BOCCACCIO levhasının dokusu levhanın kendi 2 px'lik salınımıyla birlikte gidiyor (0,93–0,98). ENG-D'nin "doku sabit kaplamaların üstünde kayar" kaygısı ölçümde görünmedi.<br>**Gren döngüsü yok:** durgun çekimlerde ince ayrıntı korelasyonu gecikmeyle düzgün azalıyor, 6. ve 12. karede tepe yok. |
| Y6 | H.264 seviyesi 5.0 (`ref=5`) (küçük) | **AÇIK** (kararda yok) | Seviye hâlâ 5.0. YouTube için önemsiz; ana dosya doğrudan oynatılacaksa `ref=4 -level 4.1`. |

### 2b. Tur 1'den taşınan maddeler

| # | Madde | Durum | Kanıt (v3) |
|---|---|---|---|
| 1 | Renk matrisi | **KAPANDI** | 12 birleşim karesinin hepsinde PSNR(709 çözümü) > PSNR(601 çözümü): +0,35 … +2,88 dB. Etiketler: VUI ve `colr nclx` 1/1/1, `tv`; `pasp` 1:1. |
| 2 | x264 ve VBV | **KAPANDI** | 13 segmentin SEI'si aynı (slow, `aq=3`, `psy_rd=1.00:0.15`, CRF 19, VBV 24M/48M). SPS/PPS tek.<br>En yüksek bit hızlı saniyelerin en büyük 8 karesi, sürekli çizimle karşılaştırıldı: PSNR 36,2–40,0 dB, SSIM 0,940–0,978.<br>VBV benzetimi: tampon en az 17,8/48 Mb, hiç kıstırmıyor. |
| 3 | Koyu degradelerde bandlaşma | **KAPANDI** (hafif gerileme, Y10) | 1204 kare tarandı. Düz-degrade payı p90 %0,66 (v2 %0,29, v1 %2,95), p99 %2,86 (v2 %1,7), en kötü %5,57.<br>En kötüler 0,0 sn ve 600,0 sn karanlıkları. Payı >%5 olan 2 kare var.<br>Blok oranı medyan 0,958, p99 1,11. Yüksek değerler içerikten geliyor: 497,5 sn'de 16 px ızgaraya denk gelen çizgiler, 25,5 sn'de neredeyse siyah kare. |
| 4 | Çekim içi hareket bulanıklığı | **KAPANDI** | Çekim içi hız arttı: >8 px/kare 43,5 sn (v2 33,8), >30 px/kare 3,6 sn.<br>Kenar enerjisi hızla düşüyor: 8–16 px/kare 0,79 · 16–30: 0,63 · ≥30: 0,55.<br>Ölçütün "keskin" dediği 63 hızlı karenin bir kısmına baktım: içeri giren nesneler (476,9–477,3 sn anahtarlı kol bulanık) ya da açılan tomar (260,7 sn). Kaçan kamera hareketi bulmadım. |
| 5 | Kuyruk / süre | **KAPANDI** | 14.437 kare = ⌈601,53 × 24⌉; segmentlerin kare MD5 dizisi finalinkiyle birebir aynı.<br>Ses 601,530 sn (edit list), video 601,542 sn: fark 11,7 ms.<br>Ses akışı `mix_audio.m4a` ile paket düzeyinde birebir aynı (MD5 091cd58e…). |
| 6 | Dil / SAR | **KAPANDI** | `tur` / `tur`, SAR 1:1, DAR 16:9. |
| 7 | Anahtar-kare tazeleme nabzı | **KISMEN** (değişmedi) | Durgun çekimlerde oran medyan 2,68 (v2 2,89; hedefim ≤2,5). Görünür değil. |
| 8 | Birleştirme sonrası otomatik doğrulama | **KISMEN** | `cmd_concat` artık çizelge özetini denetliyor. Kare sayısı, SPS tekliği ve renk matrisi öz sınaması hâlâ yok. Özet yalnız `timeline.json`'u kapsıyor, kodu kapsamıyor (Y11). |

### 2c. Benim yeniden ölçtüklerim (v3)

- **Kayıpsız birleşim:**
  - 13 segmentin kare MD5 dizisi = finalin 14.437 karesi;
  - özdeş ardışık kare yok;
  - tek SPS/PPS;
  - 12 birleşimin hepsi IDR;
  - PTS adımı sabit 512/12288, boşluk yok;
  - 347 anahtar kare.
- **Birleşim istatistikleri:**
  - birleşim karesinin kare farkı oranı 1,0–2,3; sıradan durgun anahtar karelerde medyan 2,68;
  - parlaklık sıçraması ≤0,48 düzey (yalnız 500 sn'de, 14,7 px/kare hareket varken; diğerleri ≤0,21);
  - bant geçiren enerji oranı 0,994–1,033.
- **Bit hızı:** video ortalaması 11,11 Mb/sn (v2 10,32). Saniye bazında p10 6,24 · medyan 10,51 · p90 16,65 · p99 27,47 · en yüksek 41,25 Mb/sn (66. sn). Faststart tamam; YouTube yüklemesine uygun.
- **Ses** (ffmpeg ebur128, çözülmüş AAC):
  - −14,1 LUFS (raporda −14,00/−14,04), LRA 3,5 LU;
  - gerçek tepe −1,5 dBTP (raporda AAC çözülmüş −1,48); örnek tepe −1,49/−1,49 dBFS; kırpılan örnek 0; DC −3,7e-4;
  - L/R korelasyonu 0,991, S/M −23,3 dB;
  - ilk örnek 4,3e-4; son örnek 1,3e-6; son 250 ms −82 dBFS'e iniyor;
  - sessizlik 590,3–591,8 sn ve son 0,5 sn.
- **Ses-görüntü:** render ve miks aynı çizelgeden çıkıyor (özet `887ba3df1637`). Geçiş sesleri (08:10) ile render (08:14) aynı kod durumundan; arada değişen motor dosyası yok.

## 3. Gerilemeler ve yeni sorunlar

**Y9 — Dünyaya kilitli kâğıt dokusunda ayna dikişleri (`BORDER_REFLECT`). ÖNEMLİ (yeni gerileme).**

*Neden:* `compose._tooth_warp` 1920×1080'lik tek bir doku görüntüsünü `cv2.warpAffine(..., borderMode=BORDER_REFLECT)` ile çarpıtıyor. Kamera ya da oda/pano/harita dünyası kaydıkça doku koordinatı [0, 1920) × [0, 1080) dışına taşıyor. Taşan yer aynalanıyor, ve doku kabartması yönlü ışıkla (sol-üst) gölgelendiği için ayna çizgisinin iki yanında ışık yönü de dönüyor.

*Ölçüm:*
- **Analitik:** `paper_matrix`'i çizim sırasında yakaladım. Her 2 sn'de bir örneklediğim 301 karenin 132'sinde (%44) ekranın iç bölgesinde dikey (x 90–1830) ya da yatay (y 180–900) dikiş var.
  - Örnekler: 20,0 sn x≈318 · 59,2 sn x≈1761 · 110,0 sn x≈1537 · 187,5 sn x≈1604 · 324,2 sn x≈975 ve y≈836 · 374,2 sn x≈1111 · 378,75 sn x≈1579 · 292,5 sn x≈1492.
  - Yoğunluk: oda çekimleri 84/100, harita 10/11, şehir 8/8, sokak 5/5, panorama 5/7.
- **Videoda doğrulama:** öngörülen sütunda ince dokunun ayna simetrisi ölçülebiliyor.
  - 110,0 sn gökyüzünde (y 360–460) x=1537'de korelasyon 0,508; aynı banttaki medyan −0,003, p99 0,30.
  - 292,5 sn harita denizinde x=1491'de 0,257 (medyan −0,004).
  - 3× büyütmede gökyüzünde ve denizde dikey bir "fermuar/şerit simetrisi" açıkça görünüyor (`seam_sky.png`, `seam_map.png`). 1×'te ince bir katlanma çizgisi; dünyayla birlikte kayıyor.

*Ne yapılmalı:* dokuyu döşenebilir (periyodik) üret ve `BORDER_WRAP` kullan.
- Gaussian bulanıklığı ve Sobel gölgelemesi periyodik sınırla (ör. FFT ya da `np.pad(mode="wrap")` ile) yapılmalı ki döşeme dikişi de olmasın.
- Alternatifler: kamera yolunun azami kaymasını kapsayan büyük bir doku, ya da dokuyu dünya koordinatında doğrudan üreten prosedürel gürültü.
- Maliyet: ≈1–2 saat kod.
- **Tam yeniden render (≈34 dk) şart.** Doku her segmentte. Kısmî render'da bir çekimi ortasından kesen birleşimde (ör. 50, 350 ve 500 sn'de süren çekimler) doku deseni o karede aniden değişir. Bunu yapmayacaksanız, P1'de olduğu gibi kabul edip P2'den önce düzeltin.

**Y10 — Uzayan karanlık bitiş ekranında hafif bandlaşma artışı. KÜÇÜK.**
- Bitiş ekranı 10 sn oldu, karanlık kare payı %1,3'ten %3,2'ye çıktı (593–601 sn).
- Düz-degrade payı 600,0 sn'de %5,06, açılış karesinde (0,0 sn) %5,57.
- 4× kazançla açılış karesinin koyu köşelerinde zayıf eşmerkezli halkalar var; bitiş ekranının lacivert vinyeti temiz görünüyor.
- İş gerekmez. İstenirse bitiş ekranı vinyetine ±0,5 düzey dither.

**Y11 — Çizelge özeti kodu kapsamıyor; v3.1'in kısmî render'ı için risk. KÜÇÜK (süreç), v3.1 için önemli.**
- v3'ten sonra `c2_kinds.py` (11:49), `cilt_anim.py` ve `scenes_c2.py` (11:53) değişti.
- `cilt_anim.py` ortak figür modülü. Değişiklik yalnız papa kitinde kalmıyorsa, yeniden üretilmeyen segmentlerdeki figürlerle yeniden üretilenler farklı koddan çıkar. Bir çekimi ortasından kesen sınırda bu fark görünür.
- **Ne yapılmalı:**
  - `.done` özetine `timeline.json`'un yanında ortak motor modüllerinin özetini de ekle (`compose`, `cilt_*`, `anim`, `sk`, `shots`), ya da kısmî render'da hangi sınırların hangi kodla çizildiğini kaydet.
  - Ben v3.1'de her eski/yeni segment sınırında süren çekimi ve kare sürekliliğini ayrıca denetleyeceğim (bölüm 6).

**Y12 — En karmaşık karelerde SSIM hafif düştü (en kötü 0,963 → 0,940; 242,46 sn), bit hızı +%8. KÜÇÜK.**
- Doku artık hareket ettiği için sıkıştırması zorlaştı; beklenen bir bedel.
- VBV kıstırmıyor (en az 17,8/48 Mb). Gözle bakılacak bir bozulma bulmadım.

## 4. Kullanıcının sorusu: "Bu çizim tarzı ucuz mu, yapay zekâ gibi mi?"

**Değişti.** Tur 2'de saydığım iki teknik "şablon" izi giderildi: ekrana çakılı kâğıt dokusu artık sahneyle birlikte gidiyor, 6 karelik gren döngüsü kalktı. v2'deki üç görünür hata da (yarım/dikişli sikke, plaka kenarı, üst üste yazı) kapandı. Yapay zekâ izi yine yok.

Doku kilidinin getirdiği yeni bir iz var: düz gökyüzü, deniz ve duvarlarda büyütünce görülen ayna "katlanma" çizgileri (Y9). Döşenebilir doku ile kapanır.

## 5. En emin olmadığım nokta

1. **Y9'un 1× izlemede görünürlüğü.** Simetriyi ölçtüm ve 3×'te açıkça gördüm. 1×'te TV'de düz bir gökyüzünde fark edilir mi, emin değilim. Ayrıca dünyayla birlikte kaydığı için "kâğıttaki doğal bir kat" gibi de okunabilir. Önemini bu yüzden "engelleyici" değil "önemli" verdim.
2. **Hareket bulanıklığı ölçütümün yanlış alarmları.** "Keskin" çıkan 63 hızlı karenin tamamına bakmadım. Baktıklarımın hepsi içeri giren nesneydi; kaçan bir kamera hareketi olabilir.
3. **Karanlık bitiş ekranının OLED'de bantlaşıp bantlaşmadığı.** Yalnız 4× kazançla ve sayısal ölçtüm.

## 6. v3.1 için gerileme listesi (yalnız etkilenen segmentler yeniden üretilecekse)

1. **Yeniden üretilmeyen segmentler:** kare MD5'leri v3 ile birebir aynı mı? v3 listem duruyor.
2. **Tüm segmentler:**
   - SEI ve SPS/PPS tek mi?
   - `.done` özeti tek mi?
   - kare sayısı ⌈toplam × 24⌉ mi; ses ile video farkı < 1 kare mi?
3. **Her eski/yeni sınırda:**
   - sınırı geçen çekim değişen koddan (`cilt_anim`, `c2_kinds`, `scenes_c2`) etkileniyor mu?
   - sınır karesinde içerik, doku ve ilerleme çubuğu sürekli mi?
   - kare farkı oranı sıradan anahtar kare aralığında mı?
4. **Renk ve ses:**
   - renk matrisi: gerçek karelerde PSNR709 > PSNR601;
   - etiketler: `colr`, `pasp`, dil;
   - ses değişmediyse paket MD5'i aynı mı?
5. **Y9 düzeltilirse** (tam render): bu turdaki dikiş sütunlarında ayna korelasyonu medyana inmeli (110,0 sn x≈1537; 292,5 sn x≈1491).

Kanıt dosyaları:
- `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/te1v3/v3_coin.png`
- `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/te1v3/v3_edge.png`
- `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/te1v3/v3_overlap.png`
- `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/te1v3/seam_sky.png`
- `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/te1v3/seam_map.png`
- kare MD5 listeleri: `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/te1v3/md5_*.txt`
