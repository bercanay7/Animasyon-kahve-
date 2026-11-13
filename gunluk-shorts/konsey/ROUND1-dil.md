# ROUND 1: Türkçe dil editörü (dil)

**Dossier:** DOSSIER-01-kanal-yonu.md. **Addenda read:** yok (ADDENDUM-01*.md aranıp bulunamadı; klasörde yoktu, bu "arandı, bulunamadı"dır).
**Round 1, independent:** no other member's report was read before this one was written.

**Position:** Stil ve ses kimliği ne olursa olsun, yayından önce zorunlu bir "Türkçe kapı" kurulsun (okunuş metni, telaffuz sözlüğü, yıl/sayı kuralı, Türkçe-duyarlı büyük harf); ses ve stil tartışması bu kapı çalışana kadar yorumlanamaz. Tercihim C (hibrit) + sabit tek ses; D (deney) ancak kapıdan sonra.
**Confidence:** medium

## 1. Position and why

1. **Dilin payı en ucuz düzeltilebilen kalem.** Kullanıcı sesi "çok kötü" bulduğunda neyin kötü olduğu bilinmiyor: tını mı, prozodi mi, yoksa yanlış okunan ad ve yıllar mı? Ölçülen tek dil verisi, Whisper kelime hata oranı ~%20 (çoğu yabancı ad, F4). Bu, yankı veya kadın/erkek tartışmasından önce giderilebilecek bir kusur. Kazancım: hata yakalama. Kaybım: yok; yaratıcı özgürlüğü kısıtladığım için "kaba" sayılabilirim.
2. **Metin iki sürüm olmalı: ekran metni ve okunuş metni.** Ekranda "1896", seslendirmede "bin sekiz yüz doksan altı"; "Strasbourg" ekranda Strazburg (Türkçede yerleşik yazım), seslendirmede fonetik yazım. Tek metni hem altyazıya hem TTS'e vermek hatanın kaynağı.
3. **Anlaşılırlık > çarpıcılık.** 40 sn'de kaçan tek yanlış telaffuz ("Zanzibar", "Morgan Robertson", "Futility") güveni götürür; izleyici "robotik" demeden önce "yanlış söylüyor" der.
4. **Sabit ses kimliği şart.** Her videoda farklı ses, telaffuz sözlüğünü her ses için ayrı ayarlamak demek. Tek ses, tek sözlük.
5. **Çarpıcı kanca dilde de hesap verir.** Kanca ("20 bin kuşa savaş açtı") iyi Türkçe, ama olgu ile uyumu olgu denetçisinde. Ben yalnız söyleyişi, ek uyumunu ve noktalamayı denetlerim.

## 2. Where the dossier is wrong, incomplete or mis-posed

- **Videoların metni dosyada yok.** Senaryo/altyazı metinleri verilmedi; dil editörü kendi işini (yazım, ek, okunuş) denetleyemiyor. "Aradım, bulamadım" değil "dosyada verilmemiş"; asıl kaynakta olabilir ama bu klasörde yok.
- **F4'ün %20 WER'i kötü kurulmuş bir ölçüm.** (a) Whisper'ın kendi hatasını TTS hatasından ayırmıyor; (b) hangi video, kaç kelime, "çoğu" kaç tane belli değil; (c) Whisper sayıyı rakamla yazar, referans harfle ise normalizasyonsuz WER şişer; (d) Python'da `str.lower()` Türkçe `İ`'yi `i̇` (iki kod noktası) yapar, `I`'yi `i` yapar: ölçüm betiği Türkçe-duyarlı normalize etmiyorsa hata yapay artar. Bunu yerelde denedim (aşağıda).
- **"Kuru oran ~%8,5" belirsiz.** Yankı (ıslak) oranı mı, kuru ses payı mı? Kullanıcı "yankılı" derken bu sayı yorumlanamıyor.
- **Eksik seçenek: "sesli anlatımsız" (F).** Zanzibar'ın seslendirmesiz kinetik yazı biçimi bir seçenek olarak masada yok; TTS/telaffuz riskini sıfırlıyor ama yazı yükünü artırıyor. Zanzibar'ın izlenmesi bilinmiyor, o yüzden değerlendirilemiyor.
- **Kötü kurulmuş soru:** "Kadın mı erkek mi?" Telaffuz ve anlaşılırlık ölçülmeden verilen bir tercih kararı. WORLD f0×1,55 / formant×1,14 dönüşümü ünsüz netliğini bozabilir; kulakla dinlenmediği için kanıt yok (F4).
- **E1/E2 karışıyor:** Emu (1700) vs Dans (100) farkı konu, kanca, ses sürümü ve yayın zamanı birlikte değişmiş (F3); n=2, ses etkisi ayrılamaz.

## 3. Evidence

| Claim | Type | Source or method |
|---|---|---|
| Python `'İ'.lower()` 2 kod noktası (`i`+U+0307) verir; `'titanik'.upper()` = "TITANIK" (noktalı İ kaybolur); `'ışık'.upper()` doğru, `'İSTANBUL'.lower()=='istanbul'` False | fact | Bu oturumda `python3 -I` ile çalıştırıldı |
| Altyazı/HUD büyük harf yazımında aynı hata olursa "TİTANİK'TEN" görünümü "TITANIK'TEN" olur | estimate | Yukarıdaki test + kodun `upper()` kullanıp kullanmadığı bilinmiyor; F7'deki doğru yazım elle yazılmış olabilir |
| Whisper WER ~%20, "çoğu yabancı ad" | fact (raporlanan), geçerliliği doğrulanmadı | F4; yöntemi belirsiz |
| Yıl ekleri okunuşa göre seçilir: 1896'da, 1518'de, 1932'de, 1898'de, 1912'de | fact (Türkçe ek uyumu kuralı) | Dil bilgisi; son sayı sözcüğüne bakılır (altı→"da", sekiz/iki→"de"). Piper'ın bunu nasıl okuduğunu bilmiyorum |
| Piper'ın rakamları ve ekleri doğru okuduğu | assumption | Denemedim; ortamda piper/espeak-ng yok ("arandı, bulunamadı" PATH'te) |
| Yabancı adlarda hata baskın | assumption | F4 "çoğu" diyor, sayısı yok |

## 4. Risks from this seat

- **A (hiçbir şey değişmesin):** Yanlış okunan ad ve yıl her videoda tekrar eder; sessiz hata: izleyici yorum yazmaz, kaydırır. QA (F6) yalnız teknik ölçüyor, telaffuzu hiç ölçmüyor.
- **B/C (sabit kimlik):** Sözlük bir kez kurulur, maliyet düşer; risk, sözlüğün bakımsız kalması.
- **D (deney):** Telaffuz kusuru varken "iki ses karşılaştırması" kusuru ölçer, sesi değil; yanlış ders çıkar (analitik'in de itirazı olur).
- **E (sıklık düşür):** Dil kalitesi için süre kazandırır ama dil kapısı olmadan yalnız süre kazanmak yetmez.
- **Sessiz başarısızlık:** Altyazı ile ses arasında 1-2 kelime kayması ve kelime ortasından bölünen ek ("Titanik" | "'ten") izleyicide "özensiz" izlenimi bırakır, kimse söylemez.

## 5. The cheapest decisive step

**~90 dakikalık "telaffuz sınavı":** 40 öğelik liste (15 yabancı ad, 10 yıl, 8 sayı/ölçü birimi "244 m", "50 km/s", "%", 7 ek+kesme örneği). Aynı listeyi dfki, fahrettin, fettah ve kadın dönüşümüyle sentezle; her öğeyi kullanıcı (anadil) "doğru / yanlış" işaretlesin; paralel olarak Türkçe-duyarlı normalizasyonlu Whisper WER çıkarılsın. Çıktı: ses başına hata sayısı ve hata türü (ad / sayı / prozodi).

**Önceden karar:** (a) Sözlüksüz ad hatası ≤%5 ve yıl/sayı okunuşu %100 ise zorunlu sözlük "tavsiye"ye iner; sorun dil değil, ses tınısıdır. (b) Kadın dönüşümünde hata oranı erkek sese göre ≥5 puan kötüyse kadın sese karşı çıkarım. (c) Hata ≥%15 ve ağırlıkla ad/sayı ise, kanal anayasasına sözlük kapısı zorunlu madde girer ve ses kararını bu kapı sonrasına ertelerim.

## 6. Conditions and red lines

Destekleme koşulları:
- Her video için **okunuş metni** ayrı dosya; yıl/sayı harfle, ek okunuşa göre.
- **Telaffuz sözlüğü** (`pron.tsv`): ad → Türkçe fonetik yazım; yeni ad eklenmeden video yayına çıkmaz; her sentezde sözlükteki adlar otomatik dinleme listesine girer.
- **Türkçe-duyarlı büyük/küçük harf** fonksiyonu (`i→İ`, `ı→I`); ekranda `.upper()` yasak.
- Kesme işareti: özel ad + ek tek bir ekran birimi ("Titanik'ten" bölünmez); altyazı-ses kayması ≤150 ms.
- Cümle başına ≤14 kelime, video başına en fazla 3 sayı; kısaltma yok ("m", "km/s" sesli "metre", "kilometre").
- Whisper WER ölçümü yalnız Türkçe normalizasyonla (sayı→harf, İ/ı) ve ad hatası ayrı raporlanır; hedef: sözlükteki adlarda 0 hata, genel ≤%8.

Kırmızı çizgiler: yanlış okunan ad/yıl/sayıyla yayın; ekranda `TITANIK` gibi Türkçe karakter kaybı; kanca için "Bu gerçek." tipi kalıbı olguyu aşarsa dil adına itiraz.

**Kanal anayasasına önerilen maddeler:** (1) Okunuş metni ≠ ekran metni. (2) Sözlük kapısı. (3) Türkçe-duyarlı harf. (4) Tek sabit ses, tek sözlük. (5) Her yayın öncesi sözlükteki adların 10 sn'lik dinleme kontrolü.

## 7. One line

Ses mi, stil mi diye kavga etmeden önce, 40 öğelik bir telaffuz sınavı ve zorunlu sözlük kapısıyla "Türkçe doğru okunuyor mu?" sorusunu 90 dakikada kapatın; sonra hibrit ve tek ses.
