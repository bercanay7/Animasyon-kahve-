---
name: yonetmenlik
description: YouTube animasyon yönetmenliği — hook, senaryo, storyboard, shot list, kamera/kompozisyon, tempo ve retention, thumbnail ve başlık kontrol listesi. Yeni video planlanırken veya taslak gözden geçirilirken kullan.
---
# Yönetmenlik

(Kendi yazımız; dış repodan kopya yok.)

## 1. Kısa brief (yazmadan başlama)
Kim izliyor · tek cümlelik vaat · süre · format (16:9 / Shorts 9:16) · bitişte izleyici ne yapsın (abone/ziyaret/rezervasyon) · ton.

## 2. Hook (ilk 5 sn)
İlk karede boş ekran yok. Üç hook tipi: **merak** (cevapsız soru), **sonuç önden** (finali göster), **çatışma** (sorun/abartılı durum). Giriş logosu/uzun selam yok. İlk 30 sn'de ilk "ödül" (şaşırtma/gülme).

## 3. Yapı
Hook → vaat → 3-5 beat (her beat: kurulum, gerilim, ödül) → kapanış + CTA. Her 8-15 sn'de görsel/ritim değişimi (retention çukurlarını önler). Her beat tek fikir.

## 4. Storyboard & shot list (tablo)
| # | Süre | Plan (geniş/orta/yakın) | Ekranda ne oluyor | Ses/müzik | Yazı |
Önce animatik: statik kareler + ses; ritim sorunları burada çözülür, render'da değil.

## 5. Kamera & kompozisyon (2D)
Üçler kuralı, güvenli alan %5; yakın plan = duygu, geniş plan = bağlam; kamera "dalışı" = vurgu; sarsıntı yalnız darbede (6-8 kare söner). Hareket yönü tutarlı (soldan sağa = ilerleme). Kontrast: odak en parlak/doymuş.

## 6. Tempo
Cümle başına en az 1 görsel değişim; sessizlik de bir araç ama <1.5 sn. Müzik konuşmanın altında (-18 dB civarı), efektler vuruşta.

## 7. Thumbnail ve başlık
Tek odak + ≤4 kelime, yüksek kontrast, yüz/ifade veya net nesne, 1280x720, küçük boyutta (168 px) okunur mu test et. Başlık <60 karakter, vaat + merak; thumbnail başlığı tekrar etmesin, tamamlasın.

## 8. Teslim öncesi liste
Hook ilk karede · her beat değişiyor · Türkçe karakterler doğru · ses -14 LUFS · altyazı · lisanslar ASSETS.md'de · 3 kare (başı/ortası/sonu) gözle kontrol.

## Ritim ve kurgu kuralları
- Beat süresi (kare) = `fps×60/BPM`. Yuvarlamayı **indeksten** yap (`round(i*beat)`), birikimli toplayıp yuvarlama → 10 dk'da kayma olmaz. Kesmeyi beat'e, layout değişimini ölçüye (bar) bağla.
- Plan süreleri: hızlı montaj 0.13–0.8 sn; ortalama plan 1.8–3 sn; demo/anlatım 7–10 sn. Payoff'tan önce 0.3–0.75 sn bekle.
- Geçişler: film başına 3–5 tür, her biri ekrandaki bir şeyle motive. Sert kesme geçişlerin en fazla üçte biri. Farklı "dünyalar" arası crossfade yok. Dip-cut: çıkan kare ~3 karede %40 kararır.
- Başlık: indikten sonra sabit kalır; yükseklik kare yüksekliğinin %4–9'u; tek vurgu renkli kelime. Okuma süresi: satır başına ~0.5 sn + kelime başına 0.3 sn; son satır ≥ 2 sn. Safe-area: action %90, altyazı %80.
Kaynak: HyperFrames motion.md (Apache-2.0) — özetlenmiştir.

## Bu kanalın hattı (Zaman Kuryesi) — önce kökteki `CLAUDE.md`'yi oku
Üretim kuralları orada: senaryo (`tts`/`alt`), kurul yöntemi (≥9/10, alan başına iki farklı mercek, veto: doğruluk + hassasiyet), kapak dersleri, ölçüt verileri. `sisifos/README.md` komutlar, `sisifos/yayin.md` yayın adımları. Bu skill onları **tamamlar**, yerine geçmez; çelişirse CLAUDE.md ve kullanıcının kararı geçerli.

## YouTube: kanıt düzeyine göre kurallar
Düzey **A** = YouTube resmi yardım sayfası · **B** = kanalın kendi verisi (CLAUDE.md) · **C** = blog/topluluk (hipotez; 3 videoda ölç).
- (A) Açılış, başlık+kapak vaadiyle uyuşmalı; ilk 30 sn "intro" metriği buna bakar. (B) Sisifos: kapak "NEDEN GÜLÜYOR?" derken açılış başka sahneydi, kayıp ilk 10–15 sn'de oldu → ilk 5 sn kapağın vaadini karşılasın, merak sorusu ilk cümlede, cevap sona.
- (A) Retention raporu: spike = tekrar izlenen/paylaşılan an **ya da anlaşılmayan yer**; otomatik "başarı" sayma. En iyi anlar geçse güçlü içeriği öne al.
- (A) Test ve Karşılaştır: en çok 3 başlık/kapak, optimize edilen ölçüt TO değil **izlenme süresi payı**; benzer varyantlar kazananı belirsizleştirir (belirgin farklı olsun); test sürerken değiştirme.
- (A) Aldatıcı başlık/kapak politikaya aykırı; ödül karşılığı beğeni/abone isteme yasak (beğen/abone ol demek serbest).
- (A) Shorts: azami 3 dk; Analytics'te "Engaged views" ve ort. izlenme yüzdesine bak, ham görüntülenmeye değil.
- (A, orta güven) **"Inauthentic content" riski:** aynı şablondan küçük farklı seri üretim monetizasyonu etkileyebilir. ElevenLabs + kodla çizim bir araçtır; her bölüm kendi hikâyesi, yorumu, üslup kararıyla farklı olmalı (CLAUDE.md'deki kurul bunu zaten besliyor). Gerçekçi sentetik içerik "açıklama" sorusu: YouTube'un güncel sayfasından kontrol edilmeli (doğrulanamadı).
- (B) Uzun videoda TO tek başına yetmez: **gösterim başına izlenme süresi ≈ TO × ort. izleme** (Prometheus 0,11 dk vs Sisifos 0,05 dk). İlk saatlerin TO'su sadık kitleden şişkindir; 3. ve 5. günde karşılaştır.
- (C) Open loop: bir soruyu aç, cevabı bir bölüm sonra ver; "tadımlık" serpiştir. Pattern interrupt aralığı (≈60–90 sn önerisi kaynaksız): kendi retention grafiğinle kalibre et.
- (C→ölç) Kanca kalıpları: önizleme/teaser, merak tırmandırma, problem büyütme, anında değer; anlatıda "olayın ortasından başla". İlk saniye görüntü hareketli ve anlaşılır; ses açılışı selam değil olay cümlesi.
- Mit say, kural yapma: "belirli saat/gün zorunlu", "etiketler sıralamayı belirler", "ilk X saatte Y izlenme şart" — resmi kaynakla doğrulanamadı. Sayısal oranlar (örn. "%70 ilk-30 sn → %50 genel") kaynaklar çelişiyor, kullanma.

## Yapma listesi
Vaat edilmeyen şeyi başlık/kapakta gösterme · selam/uzun intro ile açma · en iyi anı sona gömme · art arda iki videoda aynı başlık kalıbı (CLAUDE.md) · tek metriğe (yalnız TO ya da yalnız izlenme süresi) bakma · benzer kapak varyantı test etme · ücretli analiz/zamanlama servislerini (DataForSEO, Buffer vb.) ekleme.

## Yayın sonrası not şablonu (48. saat / 7. gün)
Gösterim · TO · ort. izleme (%) · 0:30'da kalan % · trafik payı (Göz at/Önerilen/Kanal) · tutma grafiğinde ilk düşüş saniyesi · spike'lar ("sevildi" / "anlaşılmadı" diye etiketle) · ders → CLAUDE.md "Ölçütler"e işle.

Kaynaklar (yardım sayfaları, erişim 2026-11-11, 3–6 ayda yenile): support.google.com/youtube/answer/9314415 (retention), /13861714 (Test ve Karşılaştır), /2801973 (spam/aldatıcı politikalar), /10059070 (Shorts). Repo fikirleri (claude-youtube MIT, claude-gtm-plugin MIT) yalnız paraphrase; kurulmadı; ücretli bağlantıları (DataForSEO/Gemini/Buffer) alınmadı.
