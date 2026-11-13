# ROUND 2: Besteci ve ses tasarımcısı (muzik)

**Read:** ROUND1-TALLY.md, every ADDENDUM-01*, and all Round 1 reports.

**Vote:** C
**Changed from round 1:** no (Tur 1 pozisyonum zaten "C'nin ses karşılığı"ydı; aşağıdaki iki sıkılaştırma oy değişikliği değil, ayrıntı düzeltmesidir: analitik raporu ve qc/kanca raporları adlandırıldı)
**Confidence:** medium

## 1. Vote and reason

C, çünkü müzik bu kanalda en küçük kaldıraç ve C onu en az maliyetle disipline eder. Üç neden:

1. **Ritim ızgarası günlük emeği düşürür.** 96 BPM, 24 fps: vuruş = 15 kare, ölçü = 60 kare = 2,5 sn. Sahne kesimi ve efektler bu ızgaraya oturursa `cues.py` senkronu otomatik üretir. (Aritmetik: 60/96 = 0,625 sn; ×24 = 15.) Süre 8/12/16 ölçü = 20/30/40 sn olabilir; yani süre kararı hangi yöne çıkarsa çıksın ızgara bozulmaz.
2. **Haftada 5 + 3 günlük tampon (C) ses katmanı için yeterli.** Müzik üreteci (`bed.py`) bir kez yazılır; video başı iş tohum ve cilt satırından ibarettir. Günlük zorunluluk (B) kapıları aşındırırsa ilk feda edilen şey telefon hoparlörü dinlemesidir, bu benim ve sesmuh'un en çok korktuğumuz sessiz hata.
3. **Tek eksen kuralı müziğe de uygulanır (analitik'e uydum).** İlk 14 günde yatağın tonu ve motifi sabit kalır, cilt rotasyonu (en çok 2 cilt) müziği oynatmaz. Tur 1'de "temaya göre ton değişsin" demiştim; bunu 14. güne erteliyorum, çünkü müzik zaten ilk 14 günün değişkeni olmamalı demiştim ve kendi sözümle tutarsızdım.

Koşul: müzik dosyada ölçüsüz kalır. Mevcut videolarda müzik düzeyi/kaynağı kayıtlı değil (aradım, bulamadım); "var/yok" iddiam yok.

**Tur 2 sorularına (G) koltuğumdan cevap**

| Soru | Kural önerim |
|---|---|
| 1. Cilt tavanı | Tavan 3. İlk 14 günde 2 cilt, yatak ise tek ortak ton seti. Gün 14'ten sonra "müzik sütunu" cilt veri dosyasına eklenir (cilt başına en çok 1 enstrüman çifti); cilt eklemek müzik kodu gerektirmez. |
| 2. Sıklık/süre | Haftada 5. Süre ilk 14 gün 40,0 sn (960 kare); 30,0 sn (12 ölçü) ancak 14. gün tutma verisi çıkarsa. Süre ölçü katı olmalı (60 kare). Aynı pencerede süre ve kanca birlikte oynamaz. |
| 3. Ses testi | Önce anlatıcı, sonra çentik. Eşik: 5 kişide ≥4/5 hâlâ %18,75 şans eşleşmesidir (P(X≥4)=6/32). Değişim kararı için 7 dinleyici, ≥6/7 tercih (P=8/128≈%6,25) ve ≤1/7 "robot". |
| 4. Kapılar | Müziğin payı en çok 2 dk: otomatik ölçüm (aşağıdaki sayılar) + hoparlörde tek 30 sn dinleme (kanca + ilk sayı). Elle yapılan kısım 2 dk'yı aşarsa madde öneri düzeyine iner. |
| 5. Ölçüt | Müzik kararı yayın metriğinden çıkarılmaz (ayırt edecek n yok). Karar kaynağı çevrimdışı eşleştirilmiş test (Bölüm 4). |
| 6. Kanca kuralı | Müzik kancanın önüne geçmez: aşağıda qc/kanca'ya yaptığım taviz. |

Otomatik müzik kapısı: konuşma varken yatak-konuşma kısa süreli LUFS farkı ≥14 dB (QA tabanı, varsayım; hedef 18), toplam −14 LUFS, true peak ≤ −1 dBTP AAC sonrası, dikişte tık yok, ≤8 sabit efekt.

## 2. Response to other members

| Member | Point | Agree / disagree | Why |
|---|---|---|---|
| sesmuh | Ducking ≥14 dB; WER ≤%10 QA eşiği | Kısmen: 14 dB evet, WER eşiği hayır | 14 dB'yi sert taban kabul ederim (hedefim 18–20). Ama mutlak "WER ≤%10" QA eşiği Ek madde 5 ile çöküyor: Whisper hatası TTS hatasından ayrılmıyor, normalizasyon yok. Benim testim yalnız aynı sesin (a) kuru (b) yataklı iki miksini karşılaştırır; Whisper'ın sabit hatası farkta sıfırlanır. Mutlak eşik değil fark eşiği: ≥3 puan. |
| qc / kanca | Kare 0'da okunur kanca, ilk söz ≤0,4–0,5 sn | Agree, kendi kuralımı geri çekiyorum | Tur 1'de "imza vuruşu ≤1,2 sn" demiştim. Bu ilk kelimeyle çakışır. Yeni kural: vuruş ≤0,35 sn, 0,4 sn'de −20 dB altında; yatak 3. sn'de girer. Kanca konuşma+yazı işidir, müzik değil. |
| izleyici | Seslendirmesiz video yayınlanmaz | Kısmen disagree | Zanzibar kanalın tek "yalnız müzik+yazı" örneği; izlenme verisi (Studio) henüz çekilmedi. Veriye bakmadan kural yazmak izleyici kartının kendi "5 kişilik test" ilkesine aykırı. Önerim: varsayılan seslendirmeli; sessiz video yalnız etiketli ve gün 14 sonrası bir kez. |
| analitik | Hücre başına ≥7 video olmadan "kazanan" yok | Agree, ama bunu müziğe çevirmem | C'de 14 günde ~10 video / 2 cilt = hücre başına ~5; müzik için yayın içi test zaten imkânsız. Bu yüzden müziği yayın içi değil, çevrimdışı eşleştirilmiş testle çözüyorum; güç sorunu yok. |
| seslendirme | ≥4/5 kör tercih eşiği | Disagree (sayı) | 5 kişide ≥4 şansla %18,75 çıkar; ses kimliği 30 video kilitleniyorsa bu zayıf. 7 kişi, ≥6 daha iyi. |
| pipeline | Ortak motor + veri dosyası cilt, ≤4 cilt | Agree | Müzik sütunu veri dosyasında; yeni kod yok. Titanik'i motora taşıma ölçümüne `bed.py` süresini de ekleyin. |

## 3. Corrections accepted or disputed

- **Ek 4 (yankı ıslak pay ≈%13,6): kabul.** Konuşmadaki yankı müzik kuyruğuyla birleşince yatağın maskeleme maliyeti artar; kuru anlatıcı (yankı 0) benim çentik hesabımın ön koşulu. Atmosfer gerekirse müzik bus'ında olur, konuşmada değil.
- **Ek 5 (Whisper %20 ölçüm sınırı): kabul ve test tasarımıma uygulandı.** Karar ölçütü mutlak WER değil, aynı ses/aynı metin üzerinde miksler arası fark; Türkçe normalizasyon (sayı→harf, İ/ı) ve ad hataları ayrı raporlanır.
- **Ek 2 (40 sn tercih): kabul.** Izgara 60 kare katı; süre değişimi müziği bozmaz.
- **Ek 10 (güvenli alan açık): müzik açısından yük yok**, ancak QA'ya eklenen "HUD üst arayüze girer mi" denemesi, kare 0'daki imza vuruşunun görsel eşleşmesini (HUD belirmesi) etkilemez.
- **Ek 9 (LUFS `audio.py`'de):** müzik kapısı bu dosyaya eklenmeli; `qa.py`'ye değil.

## 4. What would reverse this vote

- **Sesten bağımsız:** Studio'dan çekilen veride gün 14 sonrası haftada 5 yerine günlük yayının dağıtımda açık üstünlüğü (B'ye geçerdim).
- **Müzik tutumum için:** 7 dinleyiciden ≥4'ü müziksiz sürümü açıkça tercih ederse sürekli yatağı bırakır, yalnız imza vuruşu + efekt paleti (8 ses) tutarım. Yataklı sürümde paired WER farkı >3 puan çıkarsa yatağı −4 dB indiririm, yine bozuksa yalnız boşluklarda çalarım.
- Zanzibar'ın (seslendirmesiz) kaydıran oranı seslendirmelilerden açıkça iyiyse müziğin rolünü yükseltirim; tek video olduğu için yalnız ipucu.

## 5. Dissent to record

Oy azınlıkta değil; yazılı çekincem şu: kanal anayasası, ölçülmemiş "müzik/ses tutmayı artırır" varsayımına dayanan hiçbir madde içermemeli. Bu raporun 14 dB, 18–20 dB, 3. sn girişi ve 8 efekt sayıları varsayımdır, kanal verisiyle test edilmemiştir. Asıl ses riski müzik değil anlatıcı ve telaffuzdur; müzik bahane edilerek anlatıcı kararı ertelenmemelidir.
