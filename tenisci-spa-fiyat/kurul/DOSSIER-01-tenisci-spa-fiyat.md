# DOSSIER 01: Tenisçilere özel spa fiyat listesi PDF'i

**Convened:** 2026-11-04. **Question:** Tenis WhatsApp gruplarına gönderilmek üzere hazırlanan spa fiyat listesi PDF'i gönderilsin mi; gönderilecekse hangi fiyat yapısı ve hangi düzeltmelerle?

This is the identical factual record every member works from. **Check it and report where it is
wrong, incomplete or mis-posed.** Later numbered addenda (ADDENDUM-01A, 01B, ...) win where
they conflict with this file.

## 0. The question in one line

Navitas Spa & Sports Topkapı'nın tenisçilere özel spa fiyat listesi PDF'i (a) olduğu gibi, (b) metin/tasarım düzeltmeleriyle, (c) fiyat yapısı değiştirilerek gönderilsin mi, yoksa (d) gönderilmesin / ertelensin mi?

## 1. Options on the table

| Option | What it means | Reversible? | Rough cost / time |
|---|---|---|---|
| Do nothing | PDF gönderilmez ya da ertelenir; tenisçilere özel teklif yapılmaz | Evet | Sıfır; olası satış kaybı |
| Olduğu gibi gönder | Bugünkü PDF (bkz. §4 F20) gruplara gönderilir | Kısmen: gönderilen fiyat gruplarda kalır | Hemen |
| Düzeltmelerle gönder | Fiyat yapısı aynı, metin ve tasarım düzeltilir | Kısmen | PDF yeniden üretimi birkaç dakika |
| Fiyat yapısını değiştir | İndirim oranları, kapsam (VIP, paketler), süre/kontenjan/doğrulama değiştirilir | Kısmen | Kullanıcı ve işletme onayı gerekir |

## 2. Market or domain

- İşletme: Navitas Spa & Sports, DoubleTree by Hilton Topkapı içinde, Bayrampaşa / İstanbul (F15).
- Hedef: tenis oynayan kişiler; kanal: tenis WhatsApp grupları. Hangi kulüp(ler), kaç grup, kaç üye olduğu bu dosyada bilinmiyor (§6).
- Benzer önceki çalışma: Kanal 7 çalışanlarına kurumsal teklif (F12, F13). Polis memurlarına özel üyelik görseli (F16).
- Rakip fiyatlar: bu dosyada veri yok.

## 3. Goal, constraints and success measures

- **Goal:** Tenisçilerden masaj randevusu ve paket satışı.
- **Measure of success:** Listeden gelen WhatsApp yazışması, randevu ve paket satışı sayısı; işletme marjının korunması. Hedef sayı belirlenmemiş.
- **Constraints:** Fiyat ve hizmet bilgileri yalnızca işletmeden gelir; uydurma fiyat, süre, yorum ya da sağlık iddiası yok (F18). PDF tek sayfa, telefona göre.
- **Who decides, and by when:** Kullanıcı (işletme adına). Tarih belirtilmedi.

## 4. Facts

Kaynak yolları `bercanay7/navitas-topkapi` reposunun yerel kopyasına göredir: `/home/user/navitas-topkapi/`. PDF klasörü: `/home/user/Animasyon-kahve-/tenisci-spa-fiyat/`.

| # | Fact | Source | Date of source |
|---|---|---|---|
| F1 | Liste fiyatları (tek seans): İsveç Masajı 50 dk 3.000 TL; Derin Doku 50 dk 3.500 TL; Aromaterapi 50 dk 3.500 TL; Navitas Spesiyal (Masaj + Kese Köpük) 55 dk 4.500 TL; Kese Köpük 30 dk 2.250 TL; Çift Masajı 50 dk iki kişi 4.000 TL; VIP Özel Spa Süiti 180 dk iki kişi 15.000 TL | `lib/rituals.ts` satır 3-9 | repo main, 2026-10-31 |
| F2 | Liste paket fiyatları: 10'lu İsveç 25.000 TL (seans 2.500); 20'li İsveç 35.000 TL (seans 1.750); 30'lu İsveç 50.000 TL (seans ~1.670); 10'lu Mix 30.000 TL; 20'li Mix 40.000 TL | `components/pages/masaj.tsx` satır 14-19 | aynı |
| F3 | "Paketler başkasıyla paylaşılabilir. Mix pakette her seansta istediğiniz masaj türünü seçersiniz." | `components/pages/page-kit.tsx` satır 75; `masaj.tsx` satır 71 | aynı |
| F4 | Tek seans masajlar için: "Hamam, sauna ve buhar odası kullanımı dahil." Çift masajı için: "Sauna, hamam ve havuz kullanımı dahil." Kese köpük: "Mermer hamamda, 30 dakika." | `lib/rituals.ts` | aynı |
| F5 | VIP Süit: "İki kişilik özel süitte jakuzi, sauna ve hamam. Üç saatlik deneyime iki terapist eşliğinde kişi başı 60 dakika eşzamanlı masaj dahildir." | `lib/rituals.ts` satır 3 | aynı |
| F6 | SSS fiyat cevabı "... Ön ödeme yok. Paket fiyatları masaj sayfasında." | `page-kit.tsx` satır 68 | aynı |
| F7 | "Hamam ise kadın ve erkek için ayrı." | `page-kit.tsx` satır 76 | aynı |
| F8 | "Otel otoparkını kullanabilirsiniz; ilk 3 saat ücretsiz." | `page-kit.tsx` satır 73 | aynı |
| F9 | Sitedeki açılış saati: "Her gün 07.00–22.00 arası açığız." / venue: "Her gün · 07.00–22.00" | `page-kit.tsx` satır 67; `lib/venue.ts` satır 2 | aynı |
| F10 | Telefon/WhatsApp: 0533 071 33 73; adres: Orta Mahallesi, Anıt Sokağı No: 1, Bayrampaşa / İstanbul; otel: DoubleTree by Hilton Topkapı | `lib/venue.ts` satır 2 | aynı |
| F11 | Derin doku açıklaması (site): "Daha belirgin baskıyı tercih edenler için boyun, omuz ve sırta odaklanan derin doku masajı. Baskı, tercihinize göre ayarlanır." | `lib/rituals.ts` satır 7 | aynı |
| F12 | Kanal 7 Kurumsal Üyelik Planı dokümanı yalnızca yıllık **üyelik** fiyatları içerir: liste 45.000 (erkek) / 35.000 (kadın); kurumsal bireysel 30.000 / 25.000; 20+ kişi toplu 27.500 / 22.500. Dokümanda masaj fiyatı yok; "İK bütçe ayırmak isterse ... 10'lu masaj paketi önerin" cümlesi var, fiyatsız. | Claude Docs dokümanı "Kanal 7 Kurumsal Üyelik Planı", https://claude.ai/artifact/BLozArc1rrKQKPVvqFzGCc | 2026-10-20 |
| F13 | Kullanıcı bu oturumda: "Seninle geçmiş sohbetlerimizde ... yapmıştın ... Masaj paketleri mesela 10'lu 25'den 17.5'e aynı oranda tam sayı karşılığı olacak şekilde 20'li paketi de yazarsın." 25.000 → 17.500 = %30 indirim. Bu önceki sohbetin kaydı Drive, Gmail, repolar ve artifact listesinde bulunamadı. | Kullanıcı mesajı, 2026-11-04 | 2026-11-04 |
| F14 | Kullanıcı tek seanslar için %20 indirimi seçti (seçenekler %15/%20/%25/%30 idi). | Bu oturumdaki soru-cevap | 2026-11-04 |
| F15 | Otel adı ve konumu: DoubleTree by Hilton Topkapı, Bayrampaşa | `lib/venue.ts` | 2026-10-31 |
| F16 | 24 Ekim tarihli "Navitas Polis Özel Üyelik Görseli": "Tesis saatleri 07:00 – 22:00 / Hafta sonu 08:00-22:00", "3 Saat Ücretsiz Otopark", WhatsApp +90 533 071 33 73 | Artifact dosyası, yerel kopya: `/tmp/claude-0/-home-user/d6383d34-f4c3-53e1-9fb3-44f29c9d2c31/scratchpad/artifact-files/d7bfb5df-eccf-4601-bf3e-c3f5e82f0dec/project/Main.dc.html` | 2026-10-24 |
| F17 | Lead takip tablosunda "DATA KAYNAĞI", "KAMPANYA / REKLAM", "REF KODU (WhatsApp) / TIKLAMA ID" sütunları var. | Google Sheets "Navitas Lead & Satış Takip" başlık satırı | 2026-11-03 |
| F18 | Site içerik kuralı: "Prices and service details come only from the business. Do not invent prices, durations, reviews, or other claims." | `/home/user/navitas-topkapi/AGENTS.md` | 2026-10-31 |
| F19 | PDF'teki tenisçi fiyatları (hesap): tek seanslar liste × 0,80: 2.400 / 2.800 / 2.800 / 3.600 / 1.800 / 3.200 (çift, iki kişi) / 12.000 (VIP, iki kişi). Paketler liste × 0,70: 10'lu İsveç 17.500 (seans 1.750); 20'li İsveç 24.500 (seans 1.225); 10'lu Mix 21.000 (seans 2.100); 20'li Mix 28.000 (seans 1.400). 30'lu İsveç PDF'te yok (50.000 × 0,70 = 35.000; seans 1.166,67, tam sayı değil). | `index.html` | 2026-11-04 |
| F20 | PDF'in tam metni ve sırası: Logo "NAVITAS / SPA & SPORTS · TOPKAPI" → kemerli kapak fotoğrafı (Navitas işlemeli havlu) üzerinde rozet "%30 'A VARAN İNDİRİM" → "TENİSÇİLERE ÖZEL" / "Spa fiyat listesi" / "Kortun yorgunluğunu hamamda, saunada ve masajda bırakın. Tek seanslarda %20, paketlerde %30 tenisçi indirimi." → "Masaj ve hamam · KİŞİ BAŞI" 5 satır (eski fiyat üstü çizili, yeni fiyat büyük; Derin Doku'da "KORTTAN SONRA" etiketi) → "Masaj paketleri · %30 İNDİRİMLİ" 2×2 kart ("Seansı ... TL") + "Paketler arkadaşınızla paylaşılabilir. Mix pakette her seansta masaj türünü siz seçersiniz." → "İki kişilik · İKİ KİŞİ TOPLAM" (Çift, VIP) → kutu: "Masajlara hamam, sauna ve buhar odası kullanımı dahil" / "Hamam kadın ve erkek için ayrı" / "Ön ödeme yok, randevuyla" → koyu alt bölüm: "RANDEVU", WhatsApp düğmesi "WhatsApp'tan yazın 0533 071 33 73", "DoubleTree by Hilton Topkapı · Bayrampaşa / İstanbul", "Hafta içi 07.00–22.00 · Hafta sonu 08.00–22.00", "Otel otoparkında ilk 3 saat ücretsiz", "navitastopkapi.com", "Kasım 2026"; arka planda soluk tenis kortu çizimi. | `index.html`, `onizleme.jpg`, `navitas-tenisci-spa-fiyat-listesi.pdf` | 2026-11-04 |
| F21 | WhatsApp düğmesinin bağlantısı: `https://wa.me/905330713373?text=` + "Merhaba, tenisçilere özel spa fiyat listesinden ulaşıyorum. Randevu almak istiyorum." PDF'te tıklanabilir bağlantı olarak gömülü. | `index.html`; `strings` ile PDF'te doğrulandı | 2026-11-04 |
| F22 | PDF: 1 sayfa, 810 × 2730 pt (1080 × 3640 CSS px), 264 KB, fontlar gömülü (Marcellus, Hanken Grotesk). Önizleme JPG: 2160 × 7278 px, 1,2 MB. | `pdfinfo`, `pdffonts`, `ls` | 2026-11-04 |
| F23 | PDF'te geçerlilik süresi, kontenjan, tenisçi olduğunu doğrulama yöntemi, paketlerin son kullanma tarihi ve ödeme şekli yazmıyor. | `index.html` | 2026-11-04 |

## 5. Estimates and assumptions

| # | Estimate or assumption | Basis or method | What would falsify it |
|---|---|---|---|
| E1 | Telefonda PDF genişliğe sığdırıldığında (≈390 pt ekran) ölçek ≈ 0,48 (390/810). CSS boyutu × 0,75 × 0,48: 37 px ad ≈ 13,3 pt; 29 px açıklama ≈ 10,4 pt; 27 px eski fiyat/paket notu ≈ 9,7 pt; 24 px grup etiketi ≈ 8,6 pt; 22 px (logo alt satırı, "10 SEANS", alt bilgi) ≈ 7,9 pt; 21 px rozet etiketi ≈ 7,6 pt; 19 px "KORTTAN SONRA" ≈ 6,8 pt. | `index.html` CSS ölçüleri, hesap | Gerçek cihazda farklı görüntüleme ölçeği |
| E2 | Sayfa telefonda ≈ 1.310 pt yüksekliğinde; görünen alan ≈ 650-750 pt ise yaklaşık 1,8-2 ekran kaydırma. | 2730 × 0,48 | WhatsApp'ın PDF görüntüleyicisinin farklı davranması |
| E3 | WhatsApp sohbetinde PDF ilk sayfanın küçük bir önizlemesiyle görünür; çoğu kişi önce önizlemeye bakar. | Varsayım | Kullanıcı testi |
| E4 | Paketler peşin ödenir. | Varsayım; dosyada kaynak yok | İşletmenin paket satış kuralı |
| E5 | Seans başı maliyet (terapist ücreti + sarf): bilinmiyor. | — | Kasa / bordro verisi |

## 6. What is not known

- Seans başı terapist ve sarf maliyeti, doluluk oranı, boş saatler (aranmadı; dosyada veri yok).
- Kanal 7 için daha önce verildiği söylenen masaj fiyatlarının tam listesi ve koşulları (Drive, Gmail, iki repo, artifact listesi ve Kanal 7 dokümanında arandı; bulunamadı — bu, var olmadığı anlamına gelmez; kullanıcı önceki bir sohbette yapıldığını söylüyor).
- Hafta sonu saati: site (F9) ile 24 Ekim görseli (F16) çelişiyor; hangisinin güncel olduğu bilinmiyor.
- Paketlerin geçerlilik süresi ve ödeme şekli (aranmadı; sitede yazmıyor).
- Hedef gruplar: hangi kulüpler, kaç grup, kaç kişi; grup yöneticilerinin paylaşım izni.
- Tenisçi olduğunun nasıl doğrulanacağı ve indirimin süresi.

## 7. Positions already held

Bunlar test edilecek pozisyonlardır, öncül değildir:

- Kullanıcı: tek seanslarda %20, paketlerde %30 (Kanal 7 örneğiyle aynı oran: 10'lu 25.000 → 17.500), seans başı fiyat yazılsın.
- Tasarımı hazırlayan (kolaylaştırıcı) şu seçimleri yaptı: %20'yi kese köpük ve VIP dahil tüm tek seanslara uyguladı; 30'lu paketi seans fiyatı tam sayı çıkmadığı için koymadı; hafta sonu saatini 24 Ekim görselinden aldı; Derin Doku'ya "KORTTAN SONRA" etiketi koydu; rozete "%30'a varan indirim" yazdı.

## 8. What the council is asked

1. PDF gönderilmeli mi; hangi seçenek (olduğu gibi / düzeltmeli / fiyat yapısı değişmiş / gönderme)?
2. Fiyat yapısı tutarlı ve işletme için güvenli mi (tek seans %20 ile paket %30 arasındaki fark; 1.225 TL seans; VIP'te 3.000 TL indirim; 30'lu paketin yokluğu)?
3. PDF'te yanlış, çelişkili ya da işletmenin kaynaklarında dayanağı olmayan bir ifade var mı?
4. Telefonda okunabilir ve yorucu değil mi; neyi kısaltmak, büyütmek, çıkarmak ya da yeniden sıralamak gerekir?
5. Dönüşüm ve ölçüm: CTA, hazır mesaj, kaynak takibi ve gruba paylaşım biçimi yeterli mi?
6. Hangi koşullar (süre, kontenjan, doğrulama, paket kuralları) PDF'e yazılmalı ya da gönderim mesajında söylenmeli?
7. En büyük açık soruyu çözecek en ucuz adım nedir ve hangi sonuç kararı değiştirir?
