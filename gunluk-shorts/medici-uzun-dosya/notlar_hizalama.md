# Kredisiz sözcük hizalama — `ses_hizala_asr.py` (notlar + doğrulama raporu)

Amaç: ElevenLabs Scribe olmadan, `out_pN/voice.wav` anlatımı ile `script.py` metni arasında **güvenilir cümle/sözcük zamanları** üretmek.
Çıktı biçimi `ses_hizala_yerel.py` ile birebir aynı (`out_pN/scribe_words.json` = `[{text,start,end,type:"word"}]`, bölümler art arda, mutlak sn);
`ses_hizala.py` **değiştirilmeden** `out_pN/timeline.json`'u üretir.

Eski yöntemin (`ses_hizala_yerel.py`: duraklar + hece ağırlığıyla DP) sorunu: yanlış eşleşen bir durak sonraki bütün sınırları kaydırıyor
(c2 360–400 sn: 2–3 sn; c5'te 8–12 sn'ye kadar; hece-ağırlıklı sözcük dağıtımı duraklara uymadığı için komşu cümleler çakışıyor: gap<0).

## 1. Yöntem (ve önerilenden farkları)

| adım | ne yapılıyor | neden / öneriden fark |
|---|---|---|
| 1 Koşular | Bölüm sesi 250 Hz üstü süzülür, 10 ms RMS, eşik = %95 düzeyi − 34 dB (taban gürültüsü yüksekse tabana +10 dB). Sessizlik ≥ 0,12 sn → koşu sınırı. Gürültü kırıntıları (tepe < %95−22 dB: 44 adet) atılır; < 0,30 sn'lik parça + komşu durak < 0,16 sn ise komşuya katılır (8 adet; sözcük içi kapanma/patlama); > 14 sn koşu en düşük enerjiden bölünür (gerekmedi); kenarlar 10 ms dışarı alınır. | **Fark:** süzme. c2 ve c5'in son 20–26 sn'sinde 60–300 Hz'de −47 dB'lik bir uğultu tabanı var; ham RMS ile hiç durak bulunamıyor (19,8 ve 25,8 sn'lik "koşu"). Süzülmüş sinyalle durak dağılımı iki kümeli (≤0,10 sn kapanmalar | ≥0,20 sn gerçek duraklar; 0,12–0,20 arası yalnız 26) → 0,12 sn eşiği uygun. Toplam **629 koşu** (c0 51 · c1 126 · c2 127 · c3 111 · c4 128 · c5 86), medyan 1,3 sn. |
| 2 ASR | Her koşu ±0,12 sn paylı Whisper medium (sherpa-onnx int8) ile yazıya dökülür. `asr.py`'deki tanıyıcı 4 iş parçacıklı olduğundan işçi başına kendi tanıyıcı (1 iş parçacığı) × **2 işçi süreci** = toplam 2 iş parçacığı. Önbellek `out_pN/asr_cache.json`: anahtar `bölüm|başlangıç|bitiş`, ses CRC32 ile doğrulanır (ses yamalanırsa eski kayıt otomatik geçersiz). | Whisper her çağrıda ~0,3–0,5 sn/jeton harcıyor, iş parçacığı sayısı hızı neredeyse hiç artırmıyor (1 iş parçacığı ≈ 2 iş parçacığı); bu yüzden 2×1 daha hızlı. 629 iş = 1971 sn duvar saati (makine başka ajanlarca da yüklüyken). |
| 3 Eşleme | Bölümün bütün ASR sözcükleri ↔ `S._speech_of` jetonları: monoton Needleman–Wunsch. Katlama: küçük harf (İ/I Türkçe), ç→c ş→s ğ→g ı→i ö→o ü→u, noktalama/kesme işareti atılır; benzerlik = difflib oranı (tam eşit +3; ≥0,85 +2,2; ≥0,70 +1,2; ≥0,55 +0,2; değilse −1,3 "yerine koyma"; boşluk −1); 2↔1 ve 1↔2 birleştirme hamleleri (ASR "iki ye" ↔ "ikiye"; tek parçası zaten eşleşiyorsa birleştirme yasak). ASR'deki rakamlar senaryodaki gibi sözcüğe çevrilir (`1737'de` → "bin yedi yüz otuz yedide"). | Önerilen yöntem. Okunuş yazımı ("Mediçi" ↔ "Medici") katlama + oranla tolere ediliyor. |
| 4 Koşu → jeton aralığı | Eşleşen jetonlar koşunun aralığını **sert kısıt** yapar. Kanıtsız/kopuk jetonlar (ASR'nin duymadığı sözcükler, ASR'siz kalan koşular) küçük bir DP ile komşu koşulara dağıtılır: maliyet = koşu süresi ↔ hece/sözcük modeli (a·hece+b·sözcük+c, koşu verisinden en küçük kareler; ≈0,13 sn/hece) + sınırdaki noktalama ↔ durak süresi (. ? ! paragraf uzun, virgül serbest, noktalamasız uzun durak şüpheli) + yerine-koyma kanıtı. | Önerilen yöntem (sınırlar yalnız durak/noktalama ipucuyla değil, ASR kanıtı + süre modeliyle belirleniyor). |
| 5 Koşu içi zamanlar | **Kendi verisinden eğitilen monofon GMM-HMM zorlamalı hizalama** (Türkçe yazım ≈ sesbilgisi: her harf bir birim, 3 durum, tek Gauss, 39 boyutlu MFCC+Δ+ΔΔ, 10 ms; sil/sp isteğe bağlı). 626 güvenilir koşu (≈15 dk) ile sabit başlangıçtan Viterbi (sert EM) 8 yineleme; sonra her koşu kendi metniyle hizalanır. İlk sözcük koşu başına, son sözcük koşu sonuna (VAD) yaslanır; HMM ilk/son fonu >100 ms geç/erken buluyorsa (nefes, yumuşak başlangıç/sönüm: 47 kenar) HMM'e uyulur; sözcükler arası <50 ms boşluk ortadan bölünür, ≥50 ms gerçek durak kalır. HMM güvenilmeyen koşuda (log-olasılık aykırı / sözcük <30 ms) hece ağırlığına geri düşülür (bu veride 0 koşu). | **Fark (daha iyi doğruluk):** hece ağırlığı koşu içinde medyan 0,07 sn, %95 0,20 sn hata veriyor (aşağıda "duraktan bir bırak"); `shots.py` sözcük başlangıçlarına çıpa atıyor, bu yüzden akustik hizalama yapıldı (medyan 0,008 sn, %95 0,06 sn). Ses zarfı tepeleri denendi: akıcı sesli/sonorant dizilerde (l m n r) çukur oluşmadığından kararsız; HMM bu bilgiyi spektrumdan alıyor. |
| 5b Akustik düzeltmeler | (i) ASR kanıtının belirlemediği sınır jetonları (komşu koşulardan birinin ASR'sinin kaçırdığı sözcük), iki koşunun toplam HMM olabilirliğine göre seçilir (≥20 nat farkla DP kararı değişir): **4 düzeltme** (c1 «ona göre» 139,8 sn; c3 «Makyavelli'ye göre» 629,8 sn; c4 929,7 sn; c5 1095,7 sn; kazanç 322–696 nat). (ii) Tüm sınırlar için ±1 jeton kaydırma taraması (kanıtlı sınırlar değiştirilmez, yalnız raporlanır): şüpheli sınır 0. (iii) Sözcük atlama yayı (150 nat ceza): TTS'in **söylemediği sözcükler** saptanır — 3 sözcük (bkz. §4). | Önerilmeyen ama gerekli çıktı: DP'nin süre modeli "göre" gibi kısa sözcükleri yanlış koşuya verebiliyordu (ASR'nin düşürdüğü sözcük); akustik olabilirlik bunu 300–700 nat farkla düzeltiyor. Ceza 100–400 nat arasında sonuç değişmiyor (60 nat ve altında "bir" gibi kısa bir sözcük de atlanıyor → 150 seçildi). |
| 6 Çıktı | `scribe_words.json`: **her GÖSTERİM jetonu bir sözcük** (rakamlı jetonlar — "1737'de", "25" — tek sözcük; metin = gösterim jetonu). Gösterim↔söylenen jeton gruplaması DP ile (rakam → `tr_num` sözcük sayısı) doğrulanır; tutarsız cümlede saf söylenen sözcüklere düşülür (bu veride 0). Seste olmayan sözcük, AYNI cümlenin sonraki söylenen sözcüğünün başına 1 ms'lik yer tutucu olur (cümle başı yalnız söylenen sözcükle belirlenir). `--ham-konusma` ile eski biçim (saf söylenen sözcükler). | **Fark:** `ses_hizala.py` gösterim jetonlarını (rakam, okunuş yazımı) ASR/söylenen sözcüklerle bulanık eşliyor; eşleşmeyenleri komşu eşleşmeler arasında doğrusal ara değerliyor. Cümle **başındaki/sonundaki** rakamlı jeton ("1338'de kenti de saydı…": bu veride 18 cümle rakamla başlıyor, 2'si rakamla bitiyor) komşu durağı da yutuyor (t0 önceki cümlenin sonuna iniyor, gap=0). Gösterim jetonunu `text` yapınca eşleşme %100 oluyor ve ara değerleme hiç devreye girmiyor. |

Parça uyumu: `parca.py` (`MEDICI_PART`) kullanılır; `out_pN/voice_chapters.json`'daki bölümler gezilir, senaryodan bölüm yoksa/boşsa uyarıyla atlanır.
Başka ajanların yarım bıraktığı `scr_cN.py` sözdizimi hataları `import script`'i bozmasın diye bozuk bölüm modülü boş bölümle değiştirilir (uyarı verir).

## 2. Ölçümler

(Doldurulacak: a–e, aşağıda.)

## 3. Kullanım

```
# tam akış (uzun iş: ASR ≈ 30–40 dk; arka planda çalıştırın). Önbellek doluysa saniyeler–birkaç dk.
MEDICI_PART=1 nohup python3 ses_hizala_asr.py --timeline > /tmp/hizala.log 2>&1 &
MEDICI_PART=1 python3 ses_hizala_asr.py --asr-yok --timeline    # yalnız önbellekten (ASR çalıştırmaz)
MEDICI_PART=1 python3 ses_hizala.py                              # (--timeline yerine elle)
MEDICI_PART=1 python3 ses_hizala_asr.py --dogrula --n 40 [--tum] # bağımsız doğrulama (ASR ile yeniden yazdırma)
MEDICI_PART=1 python3 ses_hizala_asr.py --karsilastir            # eski ↔ yeni timeline farkları
MEDICI_PART=1 python3 ses_hizala_asr.py --loo                    # koşu içi zamanlama doğruluğu (duraktan bir bırak)
MEDICI_PART=1 python3 ses_hizala_asr.py --sondaj --n 60          # koşu içi sözcük sınırı için bağımsız ASR sondajı
# seçenekler: --bolum c2 (ya da c0,c1; ana dosyalara dokunmaz → *_c2.* yazar) · --agirlik (HMM kapalı) · --isci N · --ham-konusma
# Parça 2/3: MEDICI_PART=2 (out_p2/voice.wav + voice_chapters.json gerekir) — aynı komutlar.
```
Üretilen dosyalar (`out_pN/`): `asr_cache.json` · `scribe_words.json` (+ `scribe_words_yerel_eski.json` yedeği, yalnız ilk çalıştırmada alınır) ·
`hizala_asr_rapor.json` (bölüm bazında eşleşme, eşleşmeyen bölgeler, aykırı hız/akustik şüphe, seste olmayan sözcükler, cümle sınırı türü) ·
`hizala_asr_kosular.txt` (koşu koşu: zaman · süre · ASR metni · atanan senaryo jetonları — gözle denetim için) · `hizala_asr_karsilastirma.txt` ·
`hizala_asr_dogrulama.json/.txt` + `asr_dogrulama.json` · `hizala_asr_loo.txt` · `timeline_yerel_eski.json` (karşılaştırma için eski timeline).
