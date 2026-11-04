# ADDENDUM 01B: corrections to DOSSIER 01

**Wins over DOSSIER-01-tenisci-spa-fiyat.md and earlier addenda where they conflict.** Corrections and
measurements only. No member's position, vote or reasoning appears here.

Items are numbered on from the previous addendum so every correction has one stable number.
Kaynak: VERIFICATION.md ikinci geçiş (V49-V83), Round 1 raporlarındaki yeni iddiaların doğrulaması. Bu ekte yalnız düzeltilmesi gereken iddialar var; geri kalan yeni iddialar doğrulandı (VERIFICATION.md).

## 12. Meta satış başı maliyetleri dönem uyuşmazlığı içeriyor

- **The dossier said:** (Dossier'de yoktu; pazarlama koltuğu Round 1'de ekledi.) "Meta Ads - Masaj satış başına 234 TL (gerçek harcamayla 269 TL), Meta Ads - VIP 667 TL (767 TL)."
- **Correct:** Rakamlar "Kampanya Performansı" sekmesinde yazdığı gibi, ama harcama 28.09-22.10 dönemine ait; lead ve satış sayıları ise Ekim'in tamamına (Meta Masaj 163 lead / 24 satış, VIP 43 / 6). Panelde 23-31 Ekim tarihli 15 Meta Masaj ve 5 Meta VIP lead'i bu sayılara dahil. 22.10'da açılan ayrı bir Meta kampanyası ("MT_SPA_WA_2210 · VIP · Cift · Masaj · Hamam") ₺8.743,20 harcamış ve bu satırlara eklenmemiş. Gerçek satış başı maliyet bu yüzden 234 ve 667 TL'den yüksek olabilir. 23-31 Ekim satışları ayrıca sayılmadı.
- **Source:** Google Sheets "Navitas Lead & Satış Takip", "Kampanya Performansı" ve "Spa Aylık Panel" (2026-11-04).
- **Found by:** verifier (V54).
- **Matters because:** Tek seans ve VIP indiriminin ücretli reklam maliyetiyle karşılaştırması (Soru 2; pazarlama §1.3).

## 13. Ekim lead kaynak farkının nedeni

- **The dossier said:** (Round 1, pazarlama) "Ekim'de listede olmayan kaynak değerleriyle girilmiş 10 lead var (309'a karşı 299)."
- **Correct:** Fark 10 doğru; 10 kaydın 4'ü listede olmayan bir değerle girilmiş ("Belirsiz", "Belirsiz (site mesajı değil)" iki kez, "Web Sitesi (Google/Meta belirsiz)"), 6'sında DATA KAYNAĞI boş. Diğer ölçüm bulguları doğrulandı: "Spa Lead Takip"te REF KODU (AE) ve UTM (AA-AD) sütunları 2-735. satırlarda boş; DATA KAYNAĞI listesinde tenis grubu için bir değer yok.
- **Source:** "Spa Aylık Panel" D24:E340; "Spa Lead Takip"; "Listeler".
- **Found by:** verifier (V52).
- **Matters because:** Ölçüm kurulumu (K9).

## 14. Campus Challenge emsalinin kapsamı

- **The dossier said:** (Round 1, tam-fiyat) Campus Challenge, daha dar, süreli ve sakin görsel dilli bir emsal (liste 18.500, özel 14.900 TL, %19,5; Semester 15.500, %16,2; 72 saat; Campus Pass ve ref takibi).
- **Correct:** Rakamlar doğru (`CampusChallengeClient.tsx` 9-12, 110-112, 241). Eksik çekinceler: ürün spa hizmeti değil, **3 aylık üyelik** ("3 Ay · 14.900", satır 579-584); sayfa liste fiyatını **üstü çizili** gösteriyor ("Normal 3 ay: <s>18.500</s>", satır 584; "18.500 TL Değerinde", satır 307); canlı `navitastopkapi.com/campus-challenge` 2026-11-04'te 404 döndü.
- **Source:** `/home/user/navitas-topkapi/app/campus-challenge/CampusChallengeClient.tsx`; canlı site.
- **Found by:** verifier (V58).
- **Matters because:** Emsal karşılaştırması ve üstü çizili fiyat gösterimi (Soru 4).

## 15. Mix paketin kapsamı: canlı site belirliyor

- **The dossier said:** (Round 1, isletme, onburo, tam-fiyat, grup-yoneticisi) Mix paketin kapsamı kaynaklarda yazmıyor; Spesiyal girerse 20'li Mix seansı liste Spesiyal fiyatının %69 altında.
- **Correct:** Yalnız repo için doğru. Canlı `/spa`: "Her seansta istediğiniz masaj türünü seçersiniz: İsveç, aromaterapi ya da derin doku." (bkz. 01A madde 3). Buna göre Spesiyal Mix'e girmiyor; %69 senaryosu geçersiz, en yüksek indirim %60 (3.500 TL'ye göre).
- **Source:** canlı `/spa` (2026-11-04).
- **Found by:** verifier (V67).
- **Matters because:** 20'li Mix'in derinliği (Soru 1).

## 16. Sitede hafta sonu saati var

- **The dossier said:** (Round 1, grup-yoneticisi) Site reposunda hafta sonu saati bulunamadı.
- **Correct:** "hafta sonu / cumartesi / pazar" kelimeleri repoda geçmiyor, ama site hafta sonunu kapsayan saati açıkça veriyor: en az 14 yerde "Her gün 07.00–22.00"; JSON-LD'de Cumartesi ve Pazar dahil 07:00-22:00 (`seo.ts` 25); randevu formunda her gün 07:00'den başlayan saatler. Karar sahibinin bildirdiği gerçek hafta sonu açılış saati için bkz. ADDENDUM-01C madde 21.
- **Source:** repo grep; `seo.ts` 25; `booking-dialog.tsx` 25.
- **Found by:** verifier (V83).
- **Matters because:** Saat satırı (K6).

## Disagreements recorded, not adjudicated

Yok.

## Standing instruction

Check this record too. Report anything further, and prefer checking a source or running the
analysis over arguing about it.
