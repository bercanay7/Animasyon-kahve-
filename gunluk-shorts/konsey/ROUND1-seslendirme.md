# ROUND 1: Seslendirme yönetmeni (seslendirme)

**Dossier:** DOSSIER-01-kanal-yonu.md. **Addenda read:** ADDENDUM-01*.md aradım, klasörde eşleşen dosya bulunamadı (Glob sonucu boş); yani "ek yok" diyebilirim, "ek asla olmayacak" demem.
**Round 1, independent:** no other member's report was read before this one was written.

**Position:** Tek, sabit, kuru-yakın mikrofonlu bir anlatıcı kimliği kilitlensin (şimdilik erkek Piper sesi, yankı kapalı); kadın dönüşüm sesi yalnızca kör dinleme testini kazanırsa geçer; "videoya göre değişen ses/yankı ayarı" (Seçenek A'nın ses kısmı) reddedilir.
**Confidence:** medium

## 1. Position and why

1. **Ses kimliği bir marka varlığıdır ve şu an yok.** Dossier'e göre 4 videoda üç ayrı ses rejimi var: Zanzibar seslendirmesiz, Emu önce eski sonra yeni anlatıcıyla (F1, F3), Dans ve Titanik yeni anlatıcıyla. Kanal 4 videolukken ses kimliğini kilitlemenin maliyeti sıfıra yakın; 60 videodan sonra değiştirmek, tanıdık geleni seven izleyiciyi (izleyici koltuğunun kör noktası ama gerçek bir davranış) kaybettirir. Tahmin (yöntem: ses markası mantığı, kanıt yok).
2. **Yankı varsayılan olarak kapalı.** Kullanıcı sesi iki kez eleştirdi: "çok kötü", sonra "yankılı geliyor" (F3). Piper çıktısına oda yankısı eklemek, zaten sentetik bir sesin anlaşılırlığını düşürür; 40 sn'lik telefon hoparlörü dinlemesinde "sinematik" bir şey kazandırmaz. Benim ölçütüm "güvenilir ve sıcak"; yankı sıcaklık değil uzaklık verir. Sesmuh ile bu konuda hemfikir olmam beklenir; "heyecan" katmanını ben de istemem.
3. **Kadın dönüşüm sesine isteksiz ama kapalı değilim.** WORLD ile f0×1,55 ve formant×1,14 (F4) teorik olarak kadın perde aralığına düşer ama dossier'in kendisi "kulakla dinlenmedi" diyor. WORLD vokoder çıktıları tipik olarak vızıltı/metalik tını artefaktı taşır (tahmin; yöntem: bu tür dönüşümlerin bilinen davranışı, burada kulakla doğrulanmadı). Dönüştürülmüş bir ses, benim kırmızı çizgim olan "robotik" ihtimaline erkek sesten daha yakın. Ama bu bir hipotez; test edilir, tartışılmaz.
4. **Bir kullanıcının zevki karar değil, bir veri noktasıdır.** Kullanıcının "kadın sesi" önerisi test edilecek tutum (dossier bölüm 7). Gerçek izleyici testi gelene kadar hiçbir cinsiyet "kazanmış" sayılmaz.
5. **Ses kalitesinin izlenmeye etkisini bilmiyoruz.** Emu 1700 vs. Dans 100 farkının sebebi ses olabilir ama dossier E1'de haklı olarak konu ve kanca diyor. Ben ses lehine abartılı iddia kurmayacağım: koltuğumun çıkarı sesi önemli göstermek, tam bu yüzden kanıtsız önem iddia etmem.

## 2. Where the dossier is wrong, incomplete or mis-posed

- **Seçenek A'nın ses tarifi kendi içinde bir sorun:** "mevcut anlatıcı ses (erkek, kuru/yankılı ayarı videoya göre)". Videoya göre değişen yankı ayarı ses kimliğini bozar ve tam benim kırmızı çizgim (her videoda farklı ses). Dossier bunu "değiştirme" diye maliyetsiz sunuyor; maliyeti gizli ve kimlik kaybı.
- **Seçenek B "tek sabit ses" diyor ama hangisi olduğunu sormuyor.** Dört aday var: dfki, fahrettin, fettah (erkek) ve kadın dönüşümü (F4 yalnız dfki'yi anıyor). Fahrettin ve fettah'ın dfki ile yan yana kıyaslandığına dair dossier'de hiçbir kayıt yok. Aradım, bulamadım; "denenmedi" demiyorum, "kayıt yok" diyorum.
- **Eksik seçenek 1: seslendirmesiz / yalnız metin + müzik formatı.** Zanzibar (F1) zaten böyle üretildi. Bu, Piper sınırlarından tamamen kaçan, ses yorgunluğunu sıfırlayan bir format. Ama izleyici, "anlatıyı dinlemek" ile "okumak" arasında Shorts'ta büyük olasılıkla anlatıyı tercih eder (varsayım, kanıt yok); yine de seçenek olarak masada olmalı ve Zanzibar'ın izlenmesi (bilinmiyor, F2'de verilmedi) sorulmalı.
- **Eksik seçenek 2: kullanıcının kendi sesi veya tanıdığı birinin kaydı.** Kısıt "ücretsiz ve çevrimdışı" ve bu seçenek ücretsiz ama günlük üretimde sürdürülebilir olmayabilir; yine de 40 sn'lik metin için 10 dk'lık kayıt ve gürültü giderme makul bir üst sınır. Dossier'in kısıtları bunu açıkça dışlamıyor, ama hiç anmıyor. Doğrulama: kısıt bölümü (§3) ile TTS kısıtı yalnızca "TTS yalnızca Piper..." diyor; yani kullanıcı kaydı kısıt çiğnemez, sadece düşünülmemiş.
- **F4'teki "kuru oran ~%8,5" belirsiz:** Bu, ıslak (yankılı) karışımın %8,5 mi olduğu, yoksa kuru ses payının %8,5 mi olduğu belli değil. İkincisiyse ses %91,5 yankılı demektir ve kullanıcının "yankılı geliyor" şikayetini tam açıklar. Hangisi olduğunu `ses-lab/narrator.py` bilir; ben dosyayı açmadım (kuralım yalnız üç dosya). **Bunu pipeline koltuğunun doğrulaması gerekir.**
- **WER ~%20 (F4) kötü kurulmuş bir ölçüt:** Whisper kendi başına yabancı adlarda (Zanzibar, Strasbourg, Futility, Morgan Robertson) yanlışlar yapar; hata Whisper'dan mı TTS telaffuzundan mı geldiği ayrılmıyor. Ayrıca insan izleyicinin anlaması ile Whisper'ın transkripsiyonu aynı şey değil. %20 "ses kötü" kanıtı değil; yalnızca "telaffuz sözlüğü yok" işareti.
- **F3 kronolojisi ses deneyini bozuyor:** Emu'nun hangi sesle yayınlandığı bilinmiyor; bu yüzden Emu(1700) ile Dans(100) karşılaştırması, ses hipotezi için de, ses-dışı hipotez için de kullanılamaz (analitik koltuğunun n=2 uyarısına katılıyorum). Dossier E2'yi "Ses kalitesi izlenmeyi etkiler" diye yazıyor ama F3 yüzünden hiçbir veri bunu test edemez.
- **"Heyecanlı ama klas" talebi (bölüm 7) çelişkili bir brif:** Hem "klas" (düşük enerji, kontrollü) hem "heyecanlı" (yüksek enerji, vurgu) istiyor. TTS ile bu ikisini aynı anda vermek zor; vurgu katmanı yapay duyulur (kırmızı çizgim). Brifin netleşmesi lazım: ben "güvenilir, sıcak, orta tempo" seçerim.

## 3. Evidence

| Claim | Type | Source or method |
|---|---|---|
| 4 videoda en az üç farklı ses rejimi var (seslendirmesiz, eski anlatıcı, yeni anlatıcı) | fact | Dossier F1, F3 |
| Emu'nun hangi sesle yayınlandığı bilinmiyor, bu yüzden ses-izlenme ilişkisi test edilemez | fact | Dossier F3 ve §6 |
| Kullanıcı sesi "çok kötü", sonra "yankılı" bulmuş | fact | Dossier F3, §7 (kullanıcı sözü, özet) |
| Whisper WER ~%20, çoğu yabancı ad | fact | Dossier F4 (ham çıktı görmedim) |
| %20 WER büyük ölçüde telaffuz sözlüğü eksikliğinden gelir | estimate | Hata yabancı adlarda toplanıyor (F4'ün kendi tarifi); yöntem: varsayım, adların listesi ve düzeltilmiş sürümle yeniden ölçüm yapılmadı |
| WORLD kadın dönüşümü artefakt (vızıltı) riski taşır | estimate | Genel vokoder davranışı bilgisi; bu kanalın dosyasıyla dinlenip doğrulanmadı |
| Kadın dönüşümü ortalama perdesi kadın aralığında | fact (dossier iddiası) | F4; "kulakla dinlenmedi" notu ile; iç tutarlılık kontrolü: erkek ~110–120 Hz × 1,55 ≈ 170–185 Hz kadın aralığı. Bu aritmetik yaklaşık bir tahmindir, dfki'nin gerçek F0'ı ölçülmedi |
| Yankı, sentetik sesin anlaşılırlığını düşürür; kuru ses kısa biçimde tercih edilir | assumption | Genel ses mühendisliği bilgisi; bu kanal için ölçülmedi |
| Ses kimliği sabitliği tekrar izleyici/abone dönüşümünü artırır | assumption | Marka mantığı; kanıt yok (E3 ile aynı zayıflık) |
| 40 sn için yaklaşık 100–120 kelime gerekir | estimate | Türkçe TTS ~2,5–3 kelime/sn varsayımı; ölçülmedi |
| Platform kuralları (E7) ile ilgili | not checked | Bu rapor için web araması yapmadım; ses koltuğu için yük taşımıyor |

## 4. Risks from this seat

- **A (hiçbir şeyi değiştirme):** Sessiz hata: ses her videoda hafifçe farklı çıkar, kullanıcı ve izleyici bunu "tutarsız/amatör" diye hisseder, ama hiçbir metrik buna isim vermez. Telaffuz sözlüğü yoksa her video yeni bir yabancı ad hatası riski taşır; olgu ve dil koltuklarının da bundan zarar göreceğini tahmin ediyorum.
- **B (sabit kimlik):** Yanlış sesi kilitlersek 30–60 video sonra geri dönüş pahalı. Bu yüzden önce kör test, sonra kilit. Sessiz risk: "sabit" kelimesi bahane olur ve ses hiç iyileştirilmez; sürüm numarası ve yılda bir gözden geçirme kuralı lazım.
- **C (hibrit):** Ses iskeletin parçası olmalı, "cilt" parçası değil. Her stile ses efekt paleti uydurma eğilimi (müzik koltuğu) ses kimliğini sızdırabilir.
- **Kadın dönüşümü seçilirse:** Her videoda WORLD adımı, sentez süresini artırır (F5: ses zaten dakikalar) ve artefakt riski tüm kanalın imzası olur. Erkek sese göre daha kırılgan bir boru hattı (pipeline koltuğunun işi).
- **Seslendirmesiz formata geçilirse:** Okuma yükü izleyiciye biner, altyazı ≥40 px kuralı (renktipo) ağırlaşır; Shorts'ta sessiz izleme oranı yüksek ama anlatı bağlılığı düşer (varsayım).
- **Sessiz başarısızlık (hepsinde):** Kimse telefon hoparlöründe gerçekten dinlemezse hiçbir kontrol (qa.py LUFS/peak, F6) "ses insana yapay geliyor" diyemez. qc koltuğunun kör noktası olarak anılan "his" kalitesi tam burada.

## 5. The cheapest decisive step

**Kör ses testi, ~1–2 saat, maliyet sıfır.**

1. Tek bir ~15 sn'lik paragrafı (yabancı ad ve yıl içeren; örn. Zanzibar'dan) 4 sesle üret: dfki, fahrettin, fettah, kadın dönüşümü. Hepsi yankısız, aynı LUFS (−14).
2. Hangi sesin hangisi olduğunu bilmeyen en az 5 kişiye (Türk, 18–34, Shorts kullanıcısı) telefon hoparlöründen sırasız dinlet. Soru: "Hangisini 40 sn dinlersin?", "Hangisi robot gibi?", ve metindeki yabancı adı yazdır (anlama testi).
3. Aynı metnin yankılı/yankısız iki sürümünü dfki ile ekle.

**Kararlaştırdığım eşik (önceden):**
- Kadın dönüşümü, 5 kişiden en az 4'ünün en çok tercih ettiği ve en çok 1'inin "robot" dediği ses olursa → kadın sese geçilsin.
- Aksi halde en çok tercih edilen erkek ses kilitlensin.
- 5 kişinin ≥3'ü yankılı sürümü tercih ederse → yankı oranımı yeniden gözden geçiririm (tutumumu değiştiren sonuç).
- Anlama testinde (adı doğru yazma) en iyi sesin bile yabancı adları ≥%40 yanlış yazdırması → sorun ses değil telaffuz sözlüğüdür; o zaman sözlük işi ses seçiminden önce gelir.

Not: 5 kişi istatistiksel kanıt değildir; yön göstergesidir (analitik koltuğuna katılıyorum). Ama şu an elimizde sıfır gerçek izleyici dinlemesi var.

## 6. Conditions and red lines

Destek koşulları:
- Ses kimliği 30 video veya 90 gün (hangisi önceyse) boyunca değişmez; değişiklik yalnız yukarıdaki kör testle.
- Yankı varsayılan kapalı; kullanılacaksa en fazla çok hafif ıslak karışım (öneri: ≤%10 ıslak; kuru ses baskın) ve tüm videolarda aynı.
- Telaffuz sözlüğü zorunlu: her videoda geçen yabancı ad, yıl ve sayı için yazıya dökülmüş okunuş (dil koltuğu sahibi) ve render öncesi sese ayrı bir kulak kontrolü.
- Her videoda ilk 3 sn içinde ses başlamalı (ölü hava yok), tempo ~2,5–3 kelime/sn, cümle sonlarında kısa nefes boşluğu.

Kabul etmeyeceklerim:
- Her videoda farklı ses veya farklı yankı ayarı.
- Yapay "heyecan" vurgusu veya reklam sesi.
- Telefon hoparlöründe hiç dinlenmeden yayın.
- Kadın dönüşümünü kulakla dinlemeden ve kör testsiz kanalın kalıcı sesi yapmak.

**Kanal anayasasına önerdiğim maddeler:**
1. Kanalın tek bir anlatıcı sesi vardır; adı ve sürümü anayasada yazılıdır; en az 30 video veya 90 gün değişmez.
2. Yankı varsayılan kapalıdır; ıslak karışım ≤%10; tüm videolarda aynı değer.
3. Her yabancı ad, yıl ve sayı için telaffuz sözlüğü kaydı olmadan video render edilmez.
4. Ses, yayın öncesi telefon hoparlöründe bir kez baştan sona dinlenir; dinleyen kişi "anlaşılmayan kelime" sayısını not eder (hedef 0).
5. Anlatıcı sesi değişikliği yalnızca en az 5 kişilik kör testle ve yazılı eşikle yapılır.
6. Müzik anlatıyı bastırmaz (düzey tespiti sesmuh/muzik koltuklarının işi; benim şartım: konuşma anlaşılırlığı öncelikli).

## 7. One line

Önce kör testle sesi seç, sonra tek bir kuru ve sabit anlatıcıyı en az 30 videoya kilitle; videoya göre değişen ses/yankı ayarı ise kanalın görünmeyen ama gerçek maliyetidir.
