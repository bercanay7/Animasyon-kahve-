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
