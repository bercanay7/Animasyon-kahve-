# ADDENDUM 01D: corrections to DOSSIER 01

**Wins over DOSSIER-01-tenisci-spa-fiyat.md and earlier addenda where they conflict.** Corrections and
measurements only. No member's position, vote or reasoning appears here.

Items are numbered on from the previous addendum so every correction has one stable number.
Kaynak: VERIFICATION.md üçüncü geçiş (V84-V101), Round 2 raporlarındaki yeni iddiaların doğrulaması. Round 2 oylaması bu ekten önce tamamlandı; bu ek tavsiyeden önce yayımlanır (rounds.md §6).

## 25. Ekim VIP satış tutarları aynı ürünü göstermiyor olabilir

- **The dossier said:** (Round 2, pazarlama) Ekim'deki 6 "Meta Ads - VIP" satışı 15.000, 15.000, 15.000, 12.000, 12.000 ve 7.500 TL; dolayısıyla 12.000 TL işletmenin VIP için zaten uyguladığı bir fiyat, yeni bir dip fiyat değil.
- **Correct:** Tutarlar doğru (V84). Ürün sütununda altısında da "VIP Oda" yazıyor, ama not sütununda kapsam farklı: 15.000 TL'lik üç satırın ikisi "VIP (hamam + masaj)", üçüncüsü "(hamam, VIP)"; 12.000 TL'lik satırlardan biri "VIP (hamam)" (masajdan söz edilmiyor), öteki yalnız "VIP oda satışı"; 7.500 TL'lik satırda kapsam yok. Altı satırın üçünde kampanya ataması varsayıma dayanıyor. PDF'teki 12.000 TL'lik VIP ise "jakuzi, sauna, hamam ve kişi başı 60 dk masaj" içeriyor. Kayıtlar, 12.000 TL'nin masaj dahil VIP için uygulanmış bir fiyat olduğunu göstermiyor.
- **Source:** "Navitas Lead & Satış Takip", "Spa Lead Takip" K16:N45 (2026-11-04).
- **Found by:** verifier (V85).
- **Matters because:** pazarlama'nın Round 2'de B'den A'ya geçişinin dayanağı; VIP tartışması (tally D2).

## 26. Ekim ve Kasım VIP satışlarının kampanya ataması

- **The dossier said:** (Round 2, pazarlama) Ekim'de VIP adlı 8 satış; biri "Meta Ads - Masaj" altında "VIP + hamam" 10.000 TL.
- **Correct:** Sayı ve tutarlar doğru (8 satış, ortalama 12.062,5 TL). "VIP + hamam" 10.000 TL'lik satış (30.10) "Google Ads - Masaj" altında; notunda "defterde 15.000 TL yazıyordu, gerçek tutar 10.000 TL olarak düzeltildi" yazıyor. Kasım'ın ilk üç günü: 15.000, 11.000, 12.000 TL (Google Ads kampanyaları altında).
- **Source:** aynı sekme.
- **Found by:** verifier (V86).
- **Matters because:** VIP'in fiilen hangi fiyatlardan satıldığı (tally D2).

## 27. "VIP bugün liste fiyatından satılıyor" kayıtlarla uyuşmuyor

- **The dossier said:** (Round 2, isletme) VIP bugün liste fiyatından ve ücretli reklamla satılıyor.
- **Correct:** Ekim'deki 6 Meta VIP satışının yalnız 3'ü 15.000 TL; öteki üçü 12.000, 12.000 ve 7.500 TL. VIP adlı 8 Ekim satışının da yalnız 3'ü 15.000 TL. Düşük tutarların bir kısmı daha dar bir kapsamı gösteriyor olabilir (madde 25); bunu kayıtlar söylemiyor, işletme söyleyebilir.
- **Source:** aynı sekme.
- **Found by:** verifier (V88).
- **Matters because:** isletme'nin VIP muhalefetinin bir dayanağı (ROUND2-isletme §5).

## 28. VIP satış başı edinme maliyeti "üst sınır" değil

- **The dossier said:** (Round 2, isletme ve tam-fiyat) Meta VIP satış başı maliyetin en kötü durumu / aşırı üst sınırı ≈ 2.224-2.443 TL; 3.000 TL'lik indirimin altında.
- **Correct:** Aritmetik doğru (13.344,2 / 6 = 2.224,0; 14.655,7 / 6 = 2.442,6), ama bu bir üst sınır değil: Meta VIP kampanyasının 22.10'dan sonraki kendi harcaması sekmede yok. Pazarlama'nın ekstrapolasyonlu üst değeri 2.500 / 2.719 TL; o da 3.000 TL'nin altında.
- **Source:** "Kampanya Performansı"; hesap.
- **Found by:** verifier (V90).
- **Matters because:** VIP indiriminin ücretli kanal maliyetiyle karşılaştırması (isletme ve tam-fiyat muhalefeti).

## 29. Tasarım koltuğunun iki küçük ölçümü

- **The dossier said:** (Round 2, tasarim) "Yedi tek seans fiyatı 500 TL'nin katı"; Marcellus'ta 3, 5, 7 ve 9 rakamları satır çizgisinin altına sarkıyor.
- **Correct:** Kese Köpük 2.250 TL 500'ün katı değil (öteki altı tek seans 500'ün katı; altı paket 1.000'in katı). Marcellus'ta 3, 5 ve 9 satır çizgisinin altına iniyor; **7 inmiyor**. "2.399"da üç rakamın (3, 9, 9) sarktığı ve "2.400"de hiçbirinin sarkmadığı doğru; genişlikler 186,25 ve 155,9 px.
- **Source:** `rituals.ts`, `masaj.tsx`; proje font dosyası, Playwright `measureText`.
- **Found by:** verifier (V96, V97).
- **Matters because:** x99 değerlendirmesinin destekleyici gerekçeleri; sonuç değişmiyor.

## 30. Son PDF doğrulama geçişlerinden sonra değişti

- **The dossier said:** VERIFICATION birinci ve ikinci geçişteki PDF satırları (V21-V41) PDF'in 10:06 sürümünü anlatıyor.
- **Correct:** PDF, `index.html`, `onizleme.jpg` ve README 15:54'te kurulun düzeltmeleriyle güncellendi (commit 2bf52f9). Doğrulayıcı yeni sürümü satır satır yeniden doğrulamadı. Kolaylaştırıcı yeni PDF'i `pdftotext -layout`, `pdfinfo`, `pdffonts` ve `strings` ile kontrol etti: 1 sayfa, 810 × 2.703 pt, fontlar gömülü, iki wa.me bağlantısı (Ref: TENIS-PDF), 11 kalemin fiyatları 01C'ye göre (tek seanslar 2.400 / 2.800 / 2.800 / 3.600 / 1.800; Çift 4.000 üstü çizilisiz; VIP 15.000 → 12.000; paketler 17.500 / 24.500 / 21.000 / 28.000, seansları 1.750 / 1.225 / 2.100 / 1.400). Bu kontrol bağımsız değildir.
- **Source:** `navitas-tenisci-spa-fiyat-listesi.pdf` (15:54 sürümü).
- **Found by:** verifier (not), kolaylaştırıcı (kontrol).
- **Matters because:** Tavsiyenin sınırları.

## Disagreements recorded, not adjudicated

VIP'in fiilen hangi fiyattan satıldığı konusunda isletme ("liste fiyatından") ve pazarlama ("12.000 zaten uygulanan fiyat") karşıt okumalar yaptı. Kayıtlar ikisini de tam desteklemiyor (madde 25, 27): VIP satışlarının yarısı 15.000 TL'nin altında, ama düşük tutarlı satırların kapsamı (masaj dahil mi) belli değil. Bu, işletmeye sorulacak bir sorudur.

## Standing instruction

Check this record too. Report anything further, and prefer checking a source or running the
analysis over arguing about it.
