# ROUND 1: Besteci ve ses tasarımcısı (muzik)

**Dossier:** DOSSIER-01-kanal-yonu.md. **Addenda read:** yok. ADDENDUM-01*.md için klasörde glob araması yaptım, eşleşen dosya bulunamadı. Bu "o an klasörde yoktu" demektir; sonradan eklenip eklenmeyeceği hakkında bir şey söylemez.
**Round 1, independent:** no other member's report was read before this one was written.

**Position:** Seçenek C'nin ses karşılığı: tek sabit "ses kimliği" (96 BPM'lik ortak palet, 1 sn'lik imza vuruşu, 6–8 sabit efekt) ve konuşmanın altında kalan, temaya göre yalnız tonu/motifi değişen müzik yatağı. Videoya özel besteleme yapılmayacak. Müzik ilk 14 günün ana değişkeni değil; önce ses (anlatıcı) ve kanca çözülmeli.
**Confidence:** medium (orta). Yapı kararlarında yüksek, "müzik tutmayı ne kadar artırır" konusunda düşük.

## 1. Position and why

1. **Müzik bu kanalın en küçük kaldıracıdır; bunu açıkça söylüyorum.** Emu (1700) ile Dans (100) arasındaki fark, dosyanın kendi tahminine göre (E1) konu ve kancadan gelir. İkisinde de ses/müzik farkı belirleyici görünmüyor ve bunu ayırt edecek veri yok. Koltuğumun çıkarı "daha çok müzik" olurdu. Bence doğru olan "daha az ama daha disiplinli müzik".
2. **Günlük üretimde videoya özel beste sürdürülemez** (cevap: ortak palet). F5'e göre her video zaten yeni sahne kodu istiyor. Müziği de her gün sıfırdan yazarsak mikste tutarsızlık ve bakım yükü doğar. Çözüm: tek bir `bed.py` üreteci; girdisi tema (tonalite, 2 enstrüman, motif tohumu), çıktısı tam 40,0 sn'lik, döngüye uygun yatak. "Ses kimliği" sabit, "renk" değişken. Bu, görsel tarafta hibritin (C) aynısıdır.
3. **Tempo kare ızgarasına oturmalı.** 24 fps'te 96 BPM = vuruş başına tam 15 kare; 64 vuruş = 16 ölçü = 40,000 sn = 960 kare. Sahne geçişleri, kelime belirmeleri ve vurgu efektleri bu ızgaraya (15 karelik adım) bağlanırsa senkron elle ayarlanmaz, `cues.py` sahne olaylarından otomatik üretir. (Hesap aritmetiktir; "izleyici bunu hisseder" ise varsayım.)
4. **Konuşma kutsaldır.** Kanalın zaten ~%20 kelime hatası var (F4, çoğu yabancı ad). Müzik yatağı bu hatayı büyütebilir. Bu yüzden müzik, konuşmanın 1–4 kHz bandından ve seviyesinden geri durur (bkz. Bölüm 6).
5. **Sessizlik bir araçtır.** Kanca cümlesinde (0–3 sn) yatak yok ya da çok düşük olsun; yalnız kare 0'da tek vuruş ve kanca metnine bağlı tek efekt. Yatak 3. saniyede açılsın. (Varsayım: ilk saniyede müzik değil net vaat tutar. Retention ve kanca koltuğu itiraz edebilir.)
6. **Döngü sesle de kapanmalı.** Görüntüde son kare = ilk kare. Müziğin son ölçüsü çözülmemiş bir akorla (dominant) bitip ilk ölçüye bağlanırsa "tekrar izle" hissi doğar. Son örnek ile ilk örnek aynı genlikte (sıfır geçişi) olmalı, tık sesi olmamalı.

## 2. Where the dossier is wrong, incomplete or mis-posed

- **Müzik hakkında neredeyse hiç olgu yok.** F1 yalnız Zanzibar için "müzik/efekt" diyor. Diğer üçünde müzik var mıydı, hangi seviyede, hangi kaynakla (sentez/numpy)? Dosyada bunu aradım ve bulamadım; "yok" demiyorum, dosyada kayıtlı değil. Soru 3 "müzik düzeyi"ni sorarken mevcut düzeyi vermiyor.
- **Zanzibar seslendirmesiz** (F1), yani kanalın elindeki tek "yalnız müzik + kinetik yazı" örneği. Ama izlenmesi bilinmiyor (F2/bölüm 6). Bu, müziği seslendirmeye karşı ölçecek tek doğal örnek olabilir; yine de n=1 ve konu farklı.
- **Seçenek A'daki "kuru/yankılı ayarı videoya göre" ifadesi**, ses kimliği fikriyle çelişir. Videodan videoya değişen yankı, müzik karışımını da her seferinde yeniden ayarlamak demektir. Bu "A"nın gizli maliyetidir (cevap 8).
- **Kadın dönüşüm sesi dinlenmedi** (F4). WORLD ile f0×1,55 yapılan ses, erkek sese göre daha yüksek aralıkta duracak; müzik yatağının boşaltılacak bandı (notch) buna göre kayar. Ses seçilmeden müzik karışımı kesinleşmez. Sıralama: önce anlatıcı, sonra yatak.
- **İzlenme sayıları karışık tabanlıdır** (F2): ölçüm tarihi yok, Emu iki farklı ses sürümüyle yeniden seslendirildi (F3), videoların yaşı farklı. Hiçbir ses/müzik sonucu bu sayılardan çıkarılamaz.
- **Süre**: videolar 40–43 sn (F1). Müzik döngü/ritim ızgarası için sabit uzunluk gerekir. Anayasaya "40,0 sn ± 0,5" maddesi şart.
- "Şablon yazımı ~1–2 gün" (seçenek B) kaynaksız bir tahmindir; ses tarafı için ben kendi tahminimi aşağıda veriyorum.

## 3. Evidence

| Claim | Type | Source or method |
|---|---|---|
| 24 fps'te 96 BPM = 15 kare/vuruş; 64 vuruş = 40,0 sn = 960 kare | fact (aritmetik) | 60/96 = 0,625 sn; 0,625×24 = 15; 64×0,625 = 40 |
| Zanzibar seslendirmesiz, müzik/efektli; diğer üçü seslendirmeli | fact | DOSSIER F1 |
| Dosyada müzik seviyesi/kaynağı kayıtlı değil | fact (aranıp bulunamadı) | DOSSIER F1–F8 tarandı |
| Müzik yatağı konuşma anlaşılırlığını düşürebilir | estimate | Maskeleme genel ilkesi; kanalın verisiyle ölçülmedi. Ölçüm önerisi Bölüm 5'te |
| Kadın dönüşüm sesinde yatak boşluk bandı yukarı kayar | estimate | f0×1,55 (F4); kulakla doğrulanmadı |
| Müzik/efekt tutmayı belirgin artırır | assumption | Kanıt yok; web'de doğrulamadım, bu oturumda ölçüm de yok |
| Kendi sentezlediğimiz müzik telif/Content ID riski taşımaz | assumption | Doğrulanmadı; "sıfır risk" iddia etmiyorum |
| Sabit palet ile günlük müzik üretimi ~yarım gün ilk kurulum, sonra video başı dakikalar | estimate | Tek üreteç + tohum varsayımı; pipeline koltuğu doğrulamalı |

## 4. Risks from this seat

- **A (hiçbir şeyi değiştirme):** Müzik her videoda farklı tonda ve seviyede kalır. Sessiz hata: izleyici "bu kanalın sesi" diye bir şey öğrenemez; ayrıca yatak yüzünden anlaşılırlık sessizce düşer, çünkü kimse ölçmüyor.
- **B/C (sabit kimlik):** Aynı yatak 10–15 videodan sonra "stok" hissi verebilir. Hafifletme: motif tohumu temaya göre değişir, ana palet sabit kalır.
- **D (deney):** Müzik deneyi yapacak örneklem yok. Konuya bağlı sapma (analitik haklı) yüzünden "müzikli/müziksiz" karşılaştırması bu hacimde kanıt üretmez.
- **E (sıklığı düşür):** Müziğe daha çok emek ayrılır ama bu emeğin getirisi bilinmiyor; benim koltuğumun cazibesi tam burada, bu yüzden en çok burada kendimi sorguluyorum.
- **Sessiz başarısızlık:** −14 LUFS hedefi, yatak yüksekse konuşmayı toplamdan daha düşük tutar; sayı doğru görünür, konuşma kısık kalır.

## 5. The cheapest decisive step

**Adım (yaklaşık 1–2 saat, yeni video gerekmez):** Mevcut bir videonun konuşma kanalını iki kez miksle: (a) kuru, (b) önerdiğim yatakla. `check_voice.py` (Whisper) kelime hata oranını iki sürümde ölç, sonra 5 kişiye telefon hoparlöründen aynı 15 sn'yi (a/b, kör sıra) dinlet ve "sayıları ve adları anladın mı, hangisini tercih edersin" sor.

**Önceden belirlenmiş karar kuralları:**
- (b) hata oranı (a)'dan mutlak 3 puandan fazla kötüyse: yatak −4 dB indirilir; yine bozuksa yatak yalnız boşluklarda çalar.
- 5 dinleyiciden en az 3'ü müziksiz sürümü açıkça tercih ederse: pozisyonum "yalnız imza vuruşu + efekt paleti, sürekli yatak yok"a döner.
- 5'ten en az 4'ü yataklı sürümü tercih eder ve anlaşılırlık sorunu çıkmazsa: sürekli yatak anayasaya girer.
- Ayrıca Studio'da Zanzibar'ın (seslendirmesiz) "kaydıranlar" oranı seslendirmeli videolardan açıkça iyiyse müziğin rolünü yükseltirim. Bu tek video olduğu için yalnız bir ipucu olarak sayarım, karar vermem.

## 6. Conditions and red lines

**Destek koşulları (anayasa maddesi önerileri):**
1. Müzik yatağı konuşma sırasında konuşmanın 18–20 dB altında; boşluklarda en fazla −10 dB'e çıkar. Konuşma başlayınca 12 dB ducking, attack ~20 ms, release ~300 ms. (Başlangıç değerleri varsayımdır; Bölüm 5 testiyle kalibre edilir.)
2. Yatakta 150 Hz altı süzülür; konuşma bandında (1–4 kHz) −4 dB çentik. Anlatıcı sesi seçilince çentik merkezi yeniden ayarlanır.
3. Toplam miks −14 LUFS integrated, true peak ≤ −1 dBTP. Seviye konuşma tek başınayken değil, tüm miksle ölçülür.
4. Tek tempo: 96 BPM, 16 ölçü, tam 40,0 sn (960 kare). Sahne kesimleri 15 karelik vuruş ızgarasında.
5. Kanca: kare 0'da tek imza vuruşu (≤1,2 sn), 0–3 sn arası yatak yok ya da çok düşük; yatak 3. sn'de girer. Kanca metni her belirdiğinde aynı tek efekt.
6. Sabit efekt paleti en fazla 8 ses (whoosh, vuruş, tink, tik, kesik, derin vuruş, zil, sessiz kesme); her biri sentezle üretilmiş, her videoda aynı. Bir video 3 saniyede 2'den fazla efekt almaz.
7. Müzik motifi video tohumundan türer, enstrüman çifti temaya göre iki seçenekten gelir; her videoda ayrı beste yok.
8. Son örnek ile ilk örnek aynı genlikte, tık sesi yok; kapanış çözülmemiş akor.

**Kabul etmeyeceğim:** konuşmayı bastıran yatak; her videoda farklı ses seviyesi/yankı; "stok" hissi veren hazır efektler; müziği bahane edip anlatıcı sesi (en büyük kırılgan nokta) ertelemek.

## 7. One line

Sürekli ve dikkat çekici müzik değil, 96 BPM'lik tek bir ortak ses paleti, konuşmanın 18–20 dB altında duran döngülü yatak ve 8 sabit efekt kuralı; bunun gerçek etkisini Bölüm 5'teki 2 saatlik kelime-hata ve 5 kişilik dinleme testi gösterecek.
