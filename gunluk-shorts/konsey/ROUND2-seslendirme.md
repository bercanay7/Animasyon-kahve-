# ROUND 2: Seslendirme yönetmeni (seslendirme)

**Read:** ROUND1-TALLY.md, every ADDENDUM-01*, and all Round 1 reports.

**Vote:** C
**Changed from round 1:** no (Tur 1'de harf yoktu; tutumum "tek, kuru, sabit ses" aynı kaldı. Aşağıda yalnız sayısal eşiklerimi düzelttim.)
**Confidence:** medium

## 1. Vote and reason

C, çünkü ses kimliği ancak zaman bırakan bir tempoda kurulabilir. Ses işi video başına ucuz ama atlanması en kolay iş: telaffuz sözlüğü, telefonda baştan sona dinleme, yabancı ad kontrolü. Günlük yayında bu adımlar ilk aşınan kapıdır (pipeline ve qc'nin tamponu aynı yerden görüyorum). Haftada 5 video ve 3 günlük tampon bu kapıya zaman tanır. Ses tarafında A, B ve C aynıdır: tek erkek ses, kuru, sabit. Aralarındaki fark, bu kuralların gerçekten uygulanıp uygulanmayacağıdır.

**Tur 2 sorularına cevaplarım (Anayasa taslağı):**
- **Cilt tavanı (G1):** Ses için fark etmez. Ciltten ses sızmasın diye ses ve müzik paleti iskeletin parçasıdır. Tavan 3, ilk 14 günde 2.
- **Sıklık ve süre (G2):** Haftada 5. Süre 28–35 sn. Tempo tavanı 3,0 kelime/sn: video kısalırsa metin kısalır, ses hızlanmaz (40 sn ≈ 100–120 kelime, 30 sn ≈ 75–90 kelime; aritmetik, ölçülmedi).
- **Ses ve test (G3):** Erkek, kuru, `reverb_wet=0`. Ses seçimi ilk yayından önce, çevrimdışı ve 14 günlük pencerenin dışında yapılır. Aşama 1: dfki, fahrettin, fettah ve kadın dönüşümü, 7 kör dinleyici. Aşama 2: kadın sesi ile en iyi erkek sesi çift olarak dinletilir. Kadın sesi ancak **≥6/7 tercih ve ≤1/7 "robot"** alırsa ve ad hatası erkek sesten en fazla 5 puan fazlaysa geçer. Test yapılmamışsa gün 1'de erkek sesle başlanır.
- **Kapılar (G4):** Ses payı zorunludur ve **≤4 dk**: (a) telaffuz sözlüğü kaydı olmayan ad/yıl/sayı yoksa render yok; (b) telefon hoparlöründe baştan sona tek dinleme, anlaşılmayan kelime 0.
- **Ölçüt (G5):** Sesle ilgili tetik: yorumların ≥%30'u sesten şikâyet ediyorsa ses önceliği öne çekilir (topluluk'un eşiğini kabul ediyorum).
- **Kanca (G6):** İlk söz ≤0,4 sn'de başlar. Kanca cümlesinde tek vurgu vardır, soru tonu yoktur, reklam sesi yoktur.

## 2. Response to other members

| Member | Point | Agree / disagree | Why |
|---|---|---|---|
| sesmuh | Anlatıcıda yankı 0 | Agree, kendi eşiğimi geri çekiyorum | Tur 1'de "≤%10 ıslak" demiştim. Ek 01A m.4'e göre nominal 0,085 etkin %13,6 ıslak kazanç verdi ve kullanıcı bunu "yankılı" duydu. Aynı çarpanla %10 nominal ≈ %16 olur. Yani benim eşiğim kullanıcının şikâyet ettiği ayardan daha yankılı. Sıfır doğru. |
| izleyici | "Ses testinde ≥4/5 robot derse kadın elenir" | Disagree (eşik) | Varsayılan zaten erkek ses. Eleme eşiği gereksiz ve çok gevşek. Geçiş eşiği önemli. Ayrıca 5 kişide "≥4/5" şansla %19 çıkar (çift seçimde 6/32). 7 kişi ve ≥6/7 ile bu %6'ya iner (8/128). |
| izleyici | Seslendirmesiz video yayınlanmaz | Agree | sesmuh'un "kimliği bozuyorsa" şartı fazla yumuşak. Zanzibar'ın Studio verisi yeni sessiz video üretmeden okunabilir (seytan'ın doğal deney önerisi). |
| izleyici, dil | WER hedefi (≤%5, ≤%8) | Disagree | Ek 01A m.5: Whisper hatası TTS hatasından ayrılmıyor ve rakam/ad normalize edilmemiş. WER kapı eşiği olamaz. Kapı: sözlükteki adlar için insan kulağıyla 0 hata. WER yalnız eğilim göstergesi. |
| seytan | Bu pencerede kadın sesi yok | Partly agree | Yayında kadın sesi yok. Doğru. Ama çevrimdışı kör test (1–2 saat) pencereyi kirletmez ve kullanıcının açık önerisini kanıtla kapatır. Test yapılmadan yok demek, "kullanıcı yanlış" demektir ama elimizde kanıt yok. |
| dil | 40 öğelik telaffuz sınavı sözlükten önce gelir | Agree | Ses kararının ön adımıdır. Aynı oturumda yapılır; ad hata oranı ≥%15 ve ağırlıkla ad/sayıysa ses seçimi sözlükten sonraya kalır. |
| muzik | Konuşmanın 18–20 dB altında yatak; kanca anında yatak yok | Agree | sesmuh 14 dB diyor. Anlaşılırlık önceliğim olduğu için 18 dB başlangıcını destekliyorum. Telefon testinde 0 anlaşılmayan kelime çıkarsa 14 dB'e inilebilir. |
| retention | 25–32 sn | Partly agree | Dinleyici yorgunluğunu azaltır. Ama süreyi sesi hızlandırarak değil metni keserek tutturun. |
| analitik | Tek eksen, yayın günlüğü | Agree | Ses sürümü (anlatıcı adı, `reverb_wet`, sözlük sürümü) günlüğe yazılır. Ses değişimi ayrı bir değişkendir. |

## 3. Corrections accepted or disputed

- **Ek 01A m.4 (yankı):** Kabul. Eşiğimi bu yüzden %0'a çektim.
- **m.5 (Whisper %20):** Kabul. Sayı "TTS %20 hatalı" demek değildir. Tur 1'de zaten "kötü ölçüt" demiştim; şimdi eşik olarak kullanmayı da bırakıyorum.
- **m.10 (Piper "erkek" etiketi):** Kabul. Etiket yalnız üçüncü taraf sitesinden doğrulandı. Kör testte dinleyicilere cinsiyet sorusu da sorulur.
- **Doğrulanamayan:** Kadın dönüşümünün gerçek tınısı. Dosya "kulakla dinlenmedi" diyor, ben de dinlemedim. Vokoder artefakt riski varsayım olarak kalır.

## 4. What would reverse this vote

- Titanik'i motora taşıma ölçümü (pipeline) etkin video süresini ≤90 dk gösterir ve 3 günlük tampon korunabilirse **B** (günlük) kabul ederim.
- Ses kapısı ilk 10 videonun ikisinden fazlasında atlanırsa haftada 3–4'e (E) inmeyi önerim.
- Kör testte 3/5 veya daha fazla dinleyici yankılı sürümü tercih ederse yankı kararını yeniden açarım.
- Kadın sesi ≥6/7 ve ≤1/7 robot eşiğini geçerse erkek kilidini kaldırırım. Bu kimlik değişimidir; yazılı olarak ve tek seferde yapılır.

## 5. Dissent to record

Çoğunluk B'ye yakın. Karşı çıkışım B'nin aleyhine değil, uygulanabilirliği içindir: günlük tempoda ses kapıları sessizce aşınır. Telefon dinlemesi ve sözlük kaydı yapılmayan her video, LUFS ve kare sayısı yeşilken bile "yabancı adı yanlış okunmuş, kimsenin yorum yazmadığı" bir videodur (qa.py bunu ölçmez, Ek 01A m.9). Anayasa ya (a) kapıyı otomatik bloke eden bir kayıt dosyası ister (kayıt yoksa render yok) ya da sıklığı haftada 5'e indirir. Ben ikincisini oyluyorum. Ayrıca "14 gün her şey donuk" ifadesi ses testini pencerenin içine alıyormuş gibi okunmamalı: test pencere öncesidir. Aksi halde kullanıcının kadın sesi önerisi en erken 15. günde kanıtla karşılaşır.
