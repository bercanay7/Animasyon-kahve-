# ROUND 1: Renk ve tipografi uzmanı (renktipo)

**Dossier:** DOSSIER-01-kanal-yonu.md. **Addenda read:** ADDENDUM-01*.md için klasörde arama yaptım, dosya bulunamadı (okunacak ek yok; "yok" demiyorum, yalnızca bu klasörde glob ile bulunamadı).
**Round 1, independent:** no other member's report was read before this one was written.

**Position:** Hibrit (C), ama sabit kısmın çekirdeği tipografi: tek yazı tipi ailesi, tek altyazı stili, tek güvenli alan ve ≥ 56 px altyazı. Cilt (illüstrasyon stili) değişebilir; okunabilirlik kuralları değişemez.
**Confidence:** medium

## 1. Position and why

1. **Tipografi ve renk, stil çeşitliliği tartışmasının üstündeki ortak zemindir.** Her videoda farklı çizim tarzı (kara kalem, kâğıt kesme, blueprint) tehlikeli değil; her videoda farklı altyazı rengi, kalınlığı, konumu tehlikeli. İzleyici çizimi değil yazıyı okur. Sabit: yazı ailesi, altyazı kutusu/konturu, vurgu rengi mantığı, HUD konumu. Değişken: arka plan paleti ve illüstrasyon.
2. **Okunabilirlik stilden önce gelir.** Dosya "≥ 40 px" diyor; bunu yetersiz buluyorum (bkz. bölüm 2). Altyazı için öneri: 1080 genişlikte ≥ 56 px, tercihen 64 px; HUD/etiket yazıları ≥ 44 px.
3. **Kontrast, her cilt için ölçülmeli.** Kara kalem (açık zemin) ile blueprint (koyu zemin) aynı beyaz altyazıyla çalışmaz. Çözüm: altyazıya cilde bağlı olmayan sabit koyu kontur + yarı saydam zemin (veya kalın dış çizgi). Ölçüt: metin/zemin kontrastı ≥ 4.5:1 (WCAG AA, normal metin), büyük metin için ≥ 3:1.
4. **Kayıp/kazanç:** Sabit tipografi benim koltuğumu kazandırır (okunabilirlik testleri geçer), ama sanatçı özgürlüğünü kısar. Bunu bilerek savunuyorum; kullanıcının "her video farklı" isteğiyle kısmen çatışır, çünkü yazı katmanını ortak tutuyorum.
5. **Kör noktam:** Estetik tutarlılığa fazla önem verip tutma verisini ikinci plana atabilirim; bu yüzden aşağıdaki öneriler ölçülebilir eşiklerle sınırlı.

## 2. Where the dossier is wrong, incomplete or mis-posed

- **"Alt %25 güvenli alan" (F6, Format) büyük olasılıkla eksik.** Aradım: organik Shorts için resmî piksel şartnamesi bulamadım (bu "yok" demek değil; yalnızca web aramasında resmî bir sayfa çıkmadı). Üçüncü taraf araçlar çelişiyor: bir kaynak (reklam şartnamesine dayandığını söylüyor) üst 288 px, alt 672 px (≈ %35), sağ 192 px; ölçüm tabanlı bir diğeri üst 241, alt 381, sağ 201, sol 60 px diyor. Alt %25 = 480 px; bu iki kaynağın arasında kalıyor ve üstü/sağı hiç kapsamıyor. Etiket: **tahmin** (kaynaklar tutarsız, organik Shorts için doğrulanmadı).
- **HUD y≈260 üst kenar bölgesine düşüyor olabilir.** Üst kenar için 241–288 px öneren kaynaklara göre sayaç, arayüz katmanıyla (arama/kamera/ses simgeleri, başlık) çakışabilir. Dosya yalnızca "alt %25" kuralını sınıyor; üst ve sağ kenar QA'da yok. Bu **kötü kurulmuş** bir kontrol.
- **"≥ 40 px" ölçütü tek başına anlamsız.** 1080 px genişlik ~390 pt'lik telefona sığınca ölçek ≈ 0,36: 40 px ≈ 14 pt, parlak ışıkta ve kaydırma hızında zor. **Tahmin** (hesap: 390/1080 × 40).
- **Eksik:** Dossier'de yazı tipi adı, altyazı rengi, kontrast oranları, Türkçe karakter (İ, ı, Ş, Ğ, Ü, Ö, Ç) glif testi yok. Dosya F6'da "yazı ≥ 40 px"ı QA'da saymıyor; kontrast ölçümü de listede değil.
- **Kötü kurulmuş soru:** "Sabit mi, farklı mı?" ikili değil; yazı katmanı ve görsel katmanı ayrı kararlardır.
- **E3 (stil farkı tanımayı zorlaştırır)**: kanıtsız; Emu (kara kalem) 1700 ile Dans (kâğıt kesme) 100 arasındaki farkı stile bağlamak da kanıtsız (n=2, konu karışık).

## 3. Evidence

| Claim | Type | Source or method |
|---|---|---|
| Organik Shorts için resmî piksel güvenli alanı bulunamadı; üçüncü taraf rakamlar çelişiyor (üst 241–288, alt 381–672, sağ ~192–201) | fact (kaynakların içeriği) / estimate (organik için geçerlilik) | Web araması 2026-10-14; ör. socialync.io, adkit.so, poster.ly Shorts safe zone sayfaları. Resmî sayfa doğrulanmadı. |
| 40 px yazı ≈ 14 pt telefonda | estimate | 390 pt / 1080 px ölçeği; cihaz genişliği varsayımı |
| WCAG AA: normal metin 4.5:1, büyük metin 3:1 | fact | WCAG 2.x başarı ölçütü 1.4.3 (bilgi, doğrulayıcı teyit etsin) |
| Altyazılı videoların okunabilirliği gerçekte sorun mu | assumption | Veri yok; kimse telefonda test etmedi (dossier bölüm 6) |
| Dans'ta ilk karede kanca kartı yoktu | assumption | F7: üretici ajan hatırlaması, görselle doğrulanmadı |

## 4. Risks from this seat

- **A (hiçbir şeyi değiştirme):** Her cildin kendi yazı stili çıkar; bir videoda okunabilir, ötekinde değil. Sessiz hata: kontrast ya da güvenli alan ihlali QA'dan geçer, çünkü QA bunu ölçmüyor.
- **B (tam sabit kimlik):** Güvenli, ama blueprint koyu / kara kalem açık zemin gibi cilt ihtiyaçlarını ezer; yazı görsele yapışık durur.
- **C (hibrit):** Risk, "iskelet" tanımının pratikte sızması: ressam yazıyı cilde uydurur. Sessiz hata: ayrıntılı kâğıt kolajda altyazı dokuda kaybolur.
- **Quiet failure (sessiz):** Altyazı kelime kelime belirdiği için (F2/Format) geç beliren kelime hızlı okuyan izleyiciyi geride bırakır; bu ölçülmüyor.

## 5. The cheapest decisive step

Mevcut 4 videodan her birinin (ilk kare, ortada altyazılı kare, HUD karesi) üç karesini al; telefonda gerçek boyut ve parlaklık max ile açıp 5 kişiye 2 sn gösterip "yazıyı oku" testi yap. Aynı kareler üzerinde Shorts arayüzünü gösteren bir üst katman şablonuyla (üst 290, alt 672, sağ 200 px şeritleri) çakışmayı ölçen 10 satırlık Python/Pillow betiği yaz. Maliyet: ~1 saat. **Önceden karar:** 12 karenin ≥ 11'i hem şablonla çakışmıyor hem 2 sn'de ≥ %90 doğru okunuyorsa mevcut 40 px ve alt %25 kuralı yeterli kabul edilir ve tutumum "altyazı 56 px şartı" yerine "40 px yeter" yönünde gevşer. Aksi halde bölüm 6'daki maddeleri anayasaya yazdırırım.

## 6. Conditions and red lines

Hibriti şu koşullarla desteklerim:
- Güvenli alan: üst ≥ 290 px, alt ≥ 672 px, sağ ≥ 200 px, sol ≥ 60 px içinde yalnız dekor; tüm önemli yazı 840×960 merkezinde (HUD'u bu alana al ya da şablonla kanıtla).
- Altyazı ≥ 56 px (hedef 64), HUD/etiket ≥ 44 px; tek yazı tipi ailesi, tam Türkçe glif kapsamı; "İSTANBUL ışığı ığ ş ç ö ü" test dizesi her sürümde render edilip QA'ya girer.
- Metin/zemin kontrastı ≥ 4.5:1, her ciltte sabit koyu kontur + zemin; ölçüm QA'da otomatik.
- Tüm renkler ≤ 5 tanımlı palet jetonu (metin, vurgu, uyarı, zemin-açık, zemin-koyu); vurgu rengi anlamı sabit (ör. sarı = sayı/rakam).
- **Kabul etmem:** güvenli alan dışında önemli metin; kontrast < 3:1; eksik/yanlış Türkçe karakter; videoya göre değişen altyazı konumu.

## 7. One line

Çizim cildi değişebilir, ama yazı, kontrast ve güvenli alan tek kural olmalı: altyazı ≥ 56 px, kontrast ≥ 4.5:1, önemli metin yalnız arayüzden temiz merkez alanda (alt 672, üst 290 px dışında).
