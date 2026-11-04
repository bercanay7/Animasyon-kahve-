# ADDENDUM 01A: corrections to DOSSIER 01

**Wins over DOSSIER-01-tenisci-spa-fiyat.md and earlier addenda where they conflict.** Corrections and
measurements only. No member's position, vote or reasoning appears here.

Items are numbered on from the previous addendum so every correction has one stable number.
Kaynak: VERIFICATION.md birinci geçiş (V1-V48). İkinci geçişin düzeltmeleri ADDENDUM-01B'de.

## 1. Sitedeki paket listesi eksik verilmiş (F2)

- **The dossier said:** Beş liste paketi, `masaj.tsx` satır 14-19.
- **Correct:** Paket dizisi 14-21. satırlarda, paket kayıtları 15-20. satırlarda ve **altı** paket var. Altıncısı: "10 masaj + 10 kese köpük" **38.000 TL** (satır 20). Bu paket PDF'te yok. Canlı sitede de "Masaj + kese köpük paketi" olarak, fiyatsız listeleniyor.
- **Source:** `/home/user/navitas-topkapi/components/pages/masaj.tsx` 14-21; canlı `/spa` (2026-11-04).
- **Found by:** verifier (V2); ayrıca isletme, tenisci, grup-yoneticisi, onburo, pazarlama ve tam-fiyat koltukları.
- **Matters because:** Soru 2 (fiyat yapısı) ve 6 (hangi kalemler kampanyada).

## 2. Liste fiyatları yayındaki sitede görünmüyor (F1, F2, F6 ve "sitedeki fiyat" çerçevesi)

- **The dossier said:** Liste fiyatları "site" kaynaklı; kaynak yolları yerel repo kopyası.
- **Correct:** 2026-11-04 10:15 UTC'de canlı `navitastopkapi.com/masaj` adresi `/spa`'ya yönleniyor. `/spa`, `/vip`, `/hamam` ve ana sayfada **hiçbir TL tutarı yok**. Canlı SSS: "Fiyatlar seansa, pakete ve üyelik türüne göre değişiyor. Numaranızı bırakın; ekibimiz sizi arayıp size uygun seçenekleri, güncel fiyat ve kampanyaları paylaşsın." Bu metin repo `main`'de ve uzaktaki 11 dal başının hiçbirinde yok; yayındaki sitenin kaynağı bu repoda bulunamadı. F1/F2'deki fiyatlar yalnız repoda (`main`, son fiyat değişikliği 2026-10-22). Bu fiyatların işletmede hâlâ geçerli olup olmadığı bu kaynaklardan çıkmıyor. Not (olgu): Kullanıcının kendi örneği (F13) 10'lu paketin liste fiyatını 25.000 TL olarak kullanıyor; bu değer repodakiyle aynı. Kullanıcı ayrıca yedi tek seans liste fiyatının listelendiği soruda "Liste fiyatı + indirim oranı" seçeneğini seçti (V16).
- **Source:** canlı site (curl), `git ls-remote`, `git grep`; oturum dökümü.
- **Found by:** verifier (V3).
- **Matters because:** PDF'teki üstü çizili "eski fiyat" gösterimi ve liste fiyatı karşılaştırmaları; Soru 3. Alıcı bu liste fiyatlarını sitede göremez.

## 3. Canlı site Mix paketi üç masajla sınırlıyor (F3)

- **The dossier said:** "Mix pakette her seansta istediğiniz masaj türünü seçersiniz." (repo)
- **Correct:** Canlı `/spa` Mix paketi "İsveç, aromaterapi ya da derin doku" ile sınırlıyor. Repoda bu sınır yok. Navitas Spesiyal, Mix kapsamında görünmüyor (canlı siteye göre).
- **Source:** canlı `/spa` (2026-11-04); `page-kit.tsx` 75; `masaj.tsx` 71.
- **Found by:** verifier (V4).
- **Matters because:** 20'li Mix seansının (1.400 TL) liste fiyatıyla karşılaştırması: en yüksek liste fiyatlı seçenek Derin Doku / Aromaterapi 3.500 TL'dir (Spesiyal 4.500 değil).

## 4. VIP kapsamı kaynaklar arasında farklı (F5)

- **The dossier said:** VIP: jakuzi, sauna, hamam; iki terapistle kişi başı 60 dk masaj (`rituals.ts` 3).
- **Correct:** `rituals.ts` 3 böyle diyor (ayrıca "Meyve ve bitkisel ikramlar eşliğinde"). Canlı `/vip` ise "kese köpük ve ikramlar dahil" diyor; `lib/seo.ts` 9 da VIP'e kese köpüğü dahil sayıyor. VIP süitin kendi saunası ve hamamı var, ortak alan kullanılmıyor (`page-kit.tsx` 81).
- **Source:** `lib/rituals.ts` 3; `lib/seo.ts` 9; `page-kit.tsx` 81; canlı `/vip`.
- **Found by:** verifier (V6); onburo koltuğu (`seo.ts`).
- **Matters because:** PDF'teki VIP açıklaması ve dahil kutusu; Soru 3.

## 5. Hafta sonu saati: PDF sitenin bütün kaynaklarıyla çelişiyor (F9, F16, §6)

- **The dossier said:** Site (F9) ile 24 Ekim görseli (F16) çelişiyor; hangisinin güncel olduğu bilinmiyor.
- **Correct:** "Her gün 07.00–22.00": `page-kit.tsx` 67, `venue.ts` 2, `seo.ts` 25 (JSON-LD, yedi gün), `booking-dialog.tsx` 25 (her gün 07:00'den randevu saatleri), canlı sitenin bütün sayfaları (2026-11-04) ve Kanal 7 dokümanı ("tesis 07:00-22:00 açık", 2026-10-20). "Hafta sonu 08:00-22:00" yalnız 24 Ekim polis görselinde, "Tesis saatleri" başlığıyla geçiyor. PDF bu tek kaynağı izliyor. Hangisinin işletmede geçerli olduğu bu kaynaklardan çıkmıyor; ama PDF, yetkili kaynak sayılan siteyle (F18) kesin olarak çelişiyor.
- **Source:** yukarıdaki dosyalar; canlı site; Claude Docs Kanal 7 dokümanı; `Main.dc.html` 86.
- **Found by:** verifier (V39); onburo, tenisci, grup-yoneticisi ve pazarlama koltukları.
- **Matters because:** PDF'in alt bölümündeki saat satırı; Soru 3.

## 6. "Ön ödeme yok" kaynakta yalnız randevu bağlamında geçiyor (F6, E4)

- **The dossier said:** F6 SSS cevabını aktarıyor; E4 paketlerin peşin ödendiğini varsayıyor; ikisi arasındaki gerilim belirtilmemiş.
- **Correct:** "Ön ödeme yok" kaynakta randevu için söyleniyor (`page-kit.tsx` 68 ve 74, `masaj.tsx` 86, canlı site). Paketlerin ödeme şekli, peşin/taksit durumu ve geçerlilik süresi hiçbir kaynakta yok (repo ve canlı sitede arandı; bulunamaması kuralın olmadığı anlamına gelmez). PDF'te "Ön ödeme yok, randevuyla" maddesi paket kartlarından sonra, genel bir madde olarak duruyor ve paketleri de kapsıyor gibi okunabiliyor.
- **Source:** `page-kit.tsx` 68, 74; `masaj.tsx` 86; `index.html` 207; canlı site.
- **Found by:** verifier (V37, V45); isletme, tenisci, grup-yoneticisi, onburo, pazarlama ve tam-fiyat koltukları.
- **Matters because:** Soru 3 ve 6.

## 7. Dahil kutusu kaynağından geniş (F4, F20)

- **The dossier said:** F4 kaynak cümlelerini veriyor; F20 PDF'teki "Masajlara hamam, sauna ve buhar odası kullanımı dahil" maddesini aktarıyor.
- **Correct:** Bu ifade kaynakta tek seans masajlar ve Spesiyal için var. Kutu bütün listenin altında duruyor: Çift Masajı için kaynak "sauna, hamam ve **havuz**" diyor ve havuz PDF'te yok (SSS: "çift masajında havuz da dahil", `page-kit.tsx` 71); VIP süit kendi alanını kullanıyor; aynı "Masaj ve hamam" grubundaki Kese Köpük için sauna veya buhar odasının dahil olduğunu söyleyen bir kaynak yok. Paket seanslarında hamam ve saunanın dahil olup olmadığı da kaynaklarda yazmıyor.
- **Source:** `lib/rituals.ts` 3-9; `page-kit.tsx` 71, 81.
- **Found by:** verifier (V35); tenisci ve onburo koltukları.
- **Matters because:** Soru 3.

## 8. Derin Doku açıklaması ve "KORTTAN SONRA" etiketinin işletme kaynağında karşılığı yok (F11, F20)

- **The dossier said:** F11 sitedeki açıklamayı veriyor; §7 etiketi kolaylaştırıcının seçimi olarak anıyor.
- **Correct:** PDF "Boyun, omuz ve sırta odaklanan güçlü baskı" diyor. Kaynak "Daha belirgin baskıyı tercih edenler için ... Baskı, tercihinize göre ayarlanır" diyor (`rituals.ts` 7); canlı `/spa`: "Boyun, omuz ve sırta odaklanan, daha belirgin baskı." "Güçlü" kaynaktan ileri gidiyor; baskının ayarlanabildiği bilgisi düşmüş. Sitenin bu masaj için kullandığı etiket "GEVŞEME". "KORTTAN SONRA" için işletme kaynaklarında (repo, canlı site, Kanal 7 dokümanı, polis görseli) dayanak bulunamadı; bu yokluk yalnız aranan kaynaklar için geçerli.
- **Source:** `lib/rituals.ts` 7; canlı `/spa`; F18.
- **Found by:** verifier (V32, V33); tasarim, tenisci, grup-yoneticisi, onburo, pazarlama ve tam-fiyat koltukları.
- **Matters because:** Soru 3 (F18 kuralı).

## 9. PDF klasöründeki README eski sürümü anlatıyor

- **The dossier said:** (README dossier'de kaynak olarak geçmiyordu.)
- **Correct:** `tenisci-spa-fiyat/README.md` hâlâ "%20 tenisçi indirimi uygulandı", "Paketler bilerek eklenmedi" ve "%20 rozeti" diyor ve fiyatların kaynağı olarak canlı `/masaj`'ı gösteriyor. Bugünkü PDF'te paketler (%30) ve "%30" rozeti var; canlı `/masaj` fiyat göstermiyor (madde 2). README, önceki sürümde paketlerin dışarıda bırakılma gerekçesini de yazıyor: tek İsveç 2.400 TL, liste 10'lu paketin seans fiyatından (2.500 TL) düşük. `render.js` yorumu "PNG preview" diyor, çıktı JPG.
- **Source:** `README.md`; `index.html`; `render.js`.
- **Found by:** verifier (V48); tasarim, tenisci ve grup-yoneticisi koltukları.
- **Matters because:** Ekibin hangi teklifi aktaracağı; Soru 3.

## 10. Telefon ölçeği ve kaydırma hesabı (E1, E2)

- **The dossier said:** E1: ölçek ≈ 0,48 (PDF pt başına); E2: "yaklaşık 1,8-2 ekran kaydırma".
- **Correct:** E1'in aritmetiği doğru (CSS px × 0,361 ≈ telefonda pt, 390 pt genişlikte). Listede olmayan ölçüler: süre metni 30 px ≈ 10,8 pt; alt bilgi 28 px ≈ 10,1 pt; dahil kutusu 29 px ≈ 10,5 pt; "TENİSÇİLERE ÖZEL" 27 px ≈ 9,7 pt; "Seansı X TL" 27 px ≈ 9,7 pt; "WhatsApp'tan yazın" 24 px ≈ 8,7 pt. 360-430 pt ekran genişliğinde ölçek 0,333-0,398 (CSS px başına) olur. E2: sayfa telefonda ≈ 1.314 pt, yani 650-750 pt görünür alanla 1,75-2,02 **ekran boyu**; ilk ekrandan sonra kaydırılacak mesafe 0,75-1,02 ekran.
- **Source:** `index.html` CSS; `pdfinfo`; hesap.
- **Found by:** verifier (V42, V43); tasarim koltuğu (ek ölçüler).
- **Matters because:** Soru 4.

## 11. Kanal 7 emsali (F12, F13)

- **The dossier said:** F12 Kanal 7 dokümanını özetliyor; F13 kullanıcının 25.000 → 17.500 örneğini aktarıyor.
- **Correct:** F12 ve F13'ün aktardıkları doğrulandı. Kanal 7 dokümanında ayrıca şunlar var: "20+ kişiye hediye masaj seansı" (fiyatsız, açık soru olarak), "lead takip sistemine kaynak olarak 'Kanal 7' yazın". Kanal 7'ye daha önce masaj paketi fiyatı verildiğini gösteren kayıt bulunamadı (bakılan yerler: Claude Docs, artifact listesi, Drive, Gmail, lead tablosu, oturum dökümü); kullanıcının andığı önceki sohbete erişim yok. Yokluğu kanıtlanmadı.
- **Source:** Claude Docs "Kanal 7 Kurumsal Üyelik Planı"; oturum dökümü.
- **Found by:** verifier (V13, V14, V15).
- **Matters because:** %30 paket oranının dayanağı; Soru 2.

## Disagreements recorded, not adjudicated

Bu birinci geçişte iki koltuğun aynı olguya farklı sayılarla ulaştığı bir durum yok. Hafta sonu saatinde (madde 5) kaynaklar birbiriyle çelişiyor; hangisinin işletmede geçerli olduğu karar sahibine sorulmuştur.

## Standing instruction

Check this record too. Report anything further, and prefer checking a source or running the
analysis over arguing about it.
