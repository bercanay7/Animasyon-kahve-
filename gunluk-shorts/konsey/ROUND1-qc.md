# ROUND 1: Kalite kontrol uzmanı (qc)

**Dossier:** DOSSIER-01-kanal-yonu.md. **Addenda read:** ADDENDUM-01* aradım, klasörde bulunamadı (yok olduğunu değil, bu oturumda glob ile görünmediğini söylüyorum); okunacak ek yoktu.
**Round 1, independent:** no other member's report was read before this one was written.

**Position:** C (hibrit) ama koşullu: sabit iskelet + değişen cilt ancak "sabit iskelet = kontrol edilebilir yüzey" ilkesiyle; her yayın, otomatik QA'nın yanında 10 dakikalık insan/içerik kapısından geçmeden çıkmaz. Seçenek A (hiçbir şeyi değiştirme) QC açısından kabul edilemez.
**Confidence:** medium

## 1. Position and why

1. **Mevcut QA bir "teknik QA"; içerik QA'sı yok.** F6'daki kontroller (kare sayısı, boş kare, HUD, ≤0,3 sn yazısız süre, ilk/son kare eşitliği, alt %25, LUFS/true peak) videonun *düzgün üretildiğini* ölçer, *işe yarayıp yaramadığını* değil. Hiçbiri şunları yakalamaz: ilk karede kanca olup olmadığı (F7: Dans'ta yoktu), yanlış telaffuz edilen ad/yıl (F4: Whisper KHO ~%20), kaynaksız iddia (C2 "kehanet"), telefonda okunurluk. Bunların hepsi "sessiz hata": qa.py yeşil yanar, izleyici kaydırır. Bu, kartımdaki "sessiz hata" kırmızı çizgisinin tam kendisi.
2. **Her videoda yeni stil = her videoda yeni, denetlenmemiş kod yolu (F5).** Her `scenes.py/ui.py/art.py/cues.py` yeni hata yüzeyi. qa.py ortak kısımları yakalar ama stile özgü hatayı (örn. kâğıt-kesme 12 fps'te yazı okunurluğu) yakalayamaz. Sabit iskelet (kanca kartı, HUD, tipografi, ses zinciri) bu yüzeyi küçültür; QC maliyeti şablonla düşer. Bu yüzden B/C'ye yatkınım; cildin değişmesine ancak iskelet kapıdan geçiyorsa razıyım.
3. **Ölçüm olmadan sesi/stili "düzeltmek" test edilmemiş değişiklik yayınlamaktır.** Kadın WORLD sesi "kulakla dinlenmedi" (F4); dinlenmemiş sesi yayınlamak kontrolsüz yayındır. D (kontrollü deney) QC'yi de kurtarır: neyin hataya neyin tercihe dönüştüğünü ayırır.
4. **E (sıklığı düşür) bir kalite aracı değil, son çare.** Önce 14 gün kapı + denetim; kapı yüzünden süre 90 dakikayı aşıyorsa o zaman haftada 4-5'e düşmeyi savunurum.
5. Koltuğumun kaybı: kapı yayını yavaşlatır, "hız baskısı" ile çatışır. Bunu dürüstçe kabul ediyorum; ama 4 videoda 3 farklı ses/stil ve en az 1 kanca eksikliği, kapının zaten geç kaldığını gösteriyor.

## 2. Where the dossier is wrong, incomplete or mis-posed

- **F7 doğrulanmamış:** "Dans'ta ilk karede kanca kartı yoktu" üretici ajanın hafızasından; dosyada 4 videonun `out` klasörü zaten var, kare çıkarmak 1 komut. Bunu hafızaya bırakmak QC'ye aykırı. Bu, E1'in ("fark konudan/kancadan") ilk testi olabilir ama bugün kanıt değil.
- **F2/E1 metrik karışıklığı (doğruladım):** YouTube, 31 Mart 2025'ten itibaren Shorts görüntülenmesini "oynatma başladı/yeniden başladı" diye sayıyor (asgari izlenme süresi yok); eski ölçüt "engaged views" adıyla Analytics'te kaldı; sonraki bir yardım sayfası 24 Ağustos 2026'dan itibaren tüm biçimlerde "oynatma başlayınca sayılır" diyor (sonuçlarda gördüm, tam metni doğrulamadım). Kullanıcının "1700" ve "100"ü hangi metrik, hangi tarih? Belirtilmemiş. İki sayıyı kıyaslamak bile temkinli yapılmalı.
- **E7 yanlış/eksik kurulmuş:** "Shorts maks. süre değişti" doğrulandı: kare/dikey videolar 3 dakikaya kadar Short sayılıyor (15 Ekim 2024; yardım sayfaları 8 Aralık 2025 tarihli bir eşik de anıyor, çelişkiyi çözemedim). 40 sn bir platform sınırı değil, bizim seçimimiz; dosya bunu kısıt gibi sunuyor.
- **F4 ölçüm kötü kurulmuş:** Whisper KHO'su, TTS hatası ile Whisper'ın yabancı ad hatasını karıştırır; %20'den "ses iyi/kötü" sonucu çıkmaz. Doğrusu: telaffuz sözlüğü + her yeni özel ad için bir dinleme kontrolü.
- **F3 belirsizliği:** Emu hangi ses sürümüyle yayınlandı bilinmiyor; bu yüzden ses ile izlenme ilişkisi (E2) şu an test edilemez.
- **Eksik:** qa.py'nin bugüne kadar *gerçekte ne yakaladığı* dosyada yok (kartımdaki sorum). Dosyada aradım, bulamadım; bu "hiç yakalamadı" demek değil, "kayıt tutulmuyor" demek. Kontrol listesi kanıtsız büyüyor.
- **-14 LUFS:** dosya bunu şart gibi yazıyor; YouTube normalizasyonu yalnız yüksek sesi aşağı çeker, bu bir yayın şartı değil. Varsayım olarak etiketliyorum; tutarlılık hedefi olarak makul, zorunluluk olarak değil.

## 3. Evidence

| Claim | Type | Source or method |
|---|---|---|
| qa.py kontrolleri teknik, kanca/telaffuz/kaynak içermiyor | fact | DOSSIER F6 listesi (dosyada aranarak) |
| Dans'ta ilk karede kanca kartı yoktu | assumption (doğrulanmadı) | DOSSIER F7: "yeniden doğrulanmadı" |
| Views 31 Mart 2025'te yeniden tanımlandı; eski ölçüt "engaged views" | fact | support.google.com/youtube/answer/15424877 ve ilgili Help sonuçları (WebSearch, bugün) |
| 24 Ağustos 2026'dan itibaren tüm biçimlerde oynatma başlayınca sayım | fact, tam doğrulanmadı | arama özeti; sayfanın kendisini okumadım |
| Shorts 3 dk'ya kadar | fact | YouTube Help "Understand three-minute YouTube Shorts" |
| Her yeni stil, denetlenmemiş kod yolu getirir | estimate | F5: her video yeni sahne kodu; yöntem: yapısal akıl yürütme, ölçülmedi |
| Kapı video başına ~10 dk ekler | estimate | 12 maddelik liste x ~50 sn; pilotla ölçülecek |
| Sessiz hataların izlenmeyi düşürdüğü | assumption | kanıt yok; denetimle ölçülecek |

## 4. Risks from this seat

- **A (değiştirme):** her yeni stil yeni hata; telaffuz/kanca/kaynak hatası kanalda kalır, kimse fark etmez. En sinsi hata: yanlış tarih iddiası (Titanik "kehanet" vs romanın gerçek bağlamı) düzeltilmeden yorumlarda büyür.
- **B/C:** iskelet bir kez bozuksa her videoya kopyalanır (tek hata, çoğalan etki). Bu yüzden iskelet sürümlenmeli ve değişince 4 eski videoya karşı regresyon koşulmalı.
- **D:** deney sırasında değişkenleri bulandırmamak için QC "sürüm kilidi" şart; yoksa sonuçlar (analitik koltuğunun korkusu) anlamsızlaşır.
- **E:** daha az video = daha az kontrol yükü ama kanıt toplama hızı düşer.
- **Quiet failure:** ilk kare ≠ son kare kontrolü geçsin diye ikisi de boş/zayıf olabilir; qa.py "eşit" der, kanca yoktur.

## 5. The cheapest decisive step

**Geriye dönük 4 videolık denetim (~2 saat, ek yayın yok):** (a) her videodan 0 / 0,5 / 1 / 3 sn kareleri çıkar, kanca okunuyor mu; (b) ilk sözün başlama zamanı; (c) tüm özel ad/yıl okunuşu için dinleme listesi; (d) her iddiaya (C1-C4) tek satır kaynak; (e) telefon hoparlöründe %50 sesle bir dinleme; (f) Studio'dan Emu ve Dans için "izlenenlere karşı kaydıran" oranı ve ilk 3 sn eğrisi (metrik adı ve tarihle).
**Pozisyonu değiştirecek sonuçlar (şimdiden):** (1) 4 videonun ≥2'sinde qa.py yeşilken ≥1 kanca/telaffuz/kaynak kusuru çıkarsa kapıyı zorunlu ve haftalık denetimi kalıcı yaparım. (2) Hiç kusur çıkmaz ve Emu/Dans'ın ilk 3 sn eğrileri farklıysa, sorun QC değil konu/kancadır; kapıyı hafifletir (≤5 dk) ve D'yi konu/kanca deneyine çeviririm. (3) Kapı süresi pilotta 20 dk'yı aşarsa E'ye (haftada 4-5) geçmeyi önerim.

## 6. Conditions and red lines

Destek şartları: sürümlenmiş iskelet, yazılı kapı, qa.py yakalama kaydı. Kabul etmem: kontrolsüz yayın; dinlenmemiş ses; kaynaksız çarpıcı iddia; ilk karede kanca olmayan video; aynı gün hem ses hem stil hem kanca değiştirilmesi.

**Anayasaya önerdiğim maddeler (QC kapısı):**
1. Yayın = qa.py yeşil + insan kapısı imzası (12 madde, ≤10 dk). Kırmızıda yayın yok.
2. Kare 0'da okunur kanca metni (≥48 px, alt %25 dışında) ve ilk söz ≤0,4 sn'de başlar.
3. Her iddia için `sources.md` satırı: 1 birincil ya da 2 bağımsız kaynak; kaynaksızsa kesin dille söylenmez ("anlatılır", "iddia edilir").
4. Yabancı ad/yıl/sayı için ortak telaffuz sözlüğü; yeni ad eklenince bir dinleme kontrolü.
5. Her yayın öncesi telefon hoparlöründe %50 sesle tek dinleme; konuşma anlaşılır, müzik bastırmıyor.
6. Ses hedefi −14 LUFS ±1, true peak ≤ −1 dBTP, döngü dikişinde tık yok (varsayım: platform şartı değil, tutarlılık hedefi).
7. İskelet sürümü (v1, v2...) yayın kaydına yazılır; iskelet değişirse 4 eski videoya regresyon.
8. Tek seferde tek değişken: ses, stil ya da kanca; aynı hafta ikisi değişmez.
9. Her kontrol bir gerçek hatayla ilişkilendirilir; 14 günde hiç tetiklenmeyen kontrol gözden geçirilir ya da kaldırılır.
10. Yayın sonrası 24 saat içinde Studio metrikleri (metrik adı ve tarih ile) kayda geçer; "1700/100" gibi sayılar etiketsiz kullanılmaz.

## 7. One line

Kapıyı önce kurun, sonra stili/sesi tartışın: sabit bir iskelet ve 10 dakikalık içerik kapısı olmadan "hiçbir şeyi değiştirmeme" kalitesiz bir gelenek, "her şeyi değiştirme" ise ölçülemeyen kaostur.

Sources: [Understand three-minute YouTube Shorts](https://support.google.com/youtube/answer/15424877?hl=en), [Understand your YouTube content performance](https://support.google.com/youtube/answer/12220281)
