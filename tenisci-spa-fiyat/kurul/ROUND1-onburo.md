# ROUND 1: Ön büro ve terapist ekibi (uygulayanlar) (onburo)

**Dossier:** DOSSIER-01-tenisci-spa-fiyat.md. **Addenda read:** yok (klasörde `ADDENDUM-01*` dosyası yok; `ls` ile 2026-11-04'te kontrol edildi).
**Round 1, independent:** no other member's report was read before this one was written.

**Position:** Olduğu gibi gönderilmesin. %20 / %30 yapısı ekip için sorun değil; sorun masada uygulanacak kuralın olmaması. İşletme kısa bir yazılı kural kartını doldurduktan sonra, PDF'e iki koşul satırı eklenip "Ön ödeme yok" yalnızca tek seanslara bağlanınca gönderilsin (b). Paket kuralları (ödeme, kullanım süresi, paylaşım kaydı) gelmezse paketler PDF'ten çıkarılsın, yalnızca tek seans %20 ile gönderilsin (daraltılmış c). Son tarih ve uygunluk kuralı da gelmezse ertelensin (d).
**Confidence:** high

## 1. Position and why

1. **PDF'teki bir ifade ön büroyu ilk paket satışında yalancı durumuna düşürür.** Alt kutudaki "Ön ödeme yok, randevuyla" satırı (olgu: `index.html` satır 207), hemen üstte 17.500–28.000 TL'lik paketler listelenirken yazılmış. Sitede "ön ödeme yok" ifadesi her yerde randevu bağlamında geçiyor (olgu: `page-kit.tsx` satır 68 ve 74, `masaj.tsx` satır 86, `booking-dialog.tsx`, `vip.tsx` satır 35). Paket ödemesine dair hiçbir kural yok: repoda "peşin|taksit|ödeme|nakit|kredi kart|son kullan|geçerli|kontenjan" araması paket ödemesiyle ilgili bir şey döndürmedi (olgu: aramayı ben yaptım; bulunamaması, böyle bir kural olmadığı anlamına gelmez). Paketler fiilen peşin satılıyorsa (dosyadaki E4 varsayımı), PDF'teki satır bu koltuğun açık kırmızı çizgisidir: listede yazıp işletmede uygulanmayan bir ifade.
2. **"Tenisçilere özel" fiyatı kimin alacağını masada kimse belirleyemez.** PDF'te uygunluk kuralı, son tarih ve kontenjan yok (olgu: dosya F23, `index.html`'i ben de okudum). Resepsiyonun tenisçiyi tanıyacak bir aracı yok (varsayım: kulüplerin bu iş için kullanılabilecek bir üye kartı olduğuna dair dosyada bilgi yok). Kural yazılmazsa kapıda "ben de tenisçiyim" diyen herkesle pazarlık yapılır. Tartışmadan kaçmak için indirim verilir. İndirim de kayda "tenis" olarak girmez. Bu koltuk kimliği doğrulamak istemiyor, çünkü bunu yapamaz. İstediği, masada tek cümleyle uygulanabilecek bir kural: "Bu listedeki WhatsApp mesajıyla ya da TENİS yazarak randevu alan kişiye, [tarih]'e kadar uygulanır."
3. **Ekibin işini en çok artıracak kalem 20'li paylaşılabilir paket.** Tenisçi 20'li İsveç paketinde seans 1.225 TL. Bu, liste tek seansın (3.000 TL) %59,2, tenisçi tek seansın (2.400 TL) %49 altında. 20'li Mix'te seans 1.400 TL, liste Derin Doku'nun (3.500 TL) %60 altında (tahmin: aritmetik, F1/F19). Paket paylaşılabildiği için (olgu: F3) bir WhatsApp grubunda 4 arkadaş 24.500 TL'lik paketi bölüşüp kişi başı 6.125 TL'ye 5 seans alabilir (tahmin: aritmetik). Bu bir kural ihlali değil, sitenin kendi kuralı. Ama sonuç değişmiyor: ön büro tek bir paketten 4 kişinin kullandığı 20 seansı, kalan hakkı ve geçerlilik süresini takip etmek zorunda kalır. Kayıt kuralı (paketi kim aldı, kimler kullanacak, kaç seans kaldı) yazılmadan bu paket satılırsa masada "3 hakkım kalmıştı" tartışması kaçınılmaz.
4. **Terapist geliri sessizce düşebilir.** Terapist primi seans fiyatına bağlıysa (varsayım: persona kartından, dosyada veri yok), 20'li tenisçi paketinde aynı 50 dakikalık iş için prim tabanı liste fiyatının %59 altına iner. Ekip bu farkı şikâyetle değil, indirimli paket sahibine daha az uygun saat vererek ya da daha az özen göstererek yansıtabilir. Bu da en zor fark edilen hatadır (§4). İşletmenin bu konuda tek cümlelik bir karar vermesi gerekiyor: indirimli seansta prim hangi fiyattan hesaplanır?
5. **Fiyat yapısına bu koltuğun itirazı yok.** "Tek seans %20, paket %30" iki oranlı ama masada uygulaması kolay, çünkü PDF'in kendisi ikinci fiyat listesi olarak resepsiyonda durabilir. Bu koltuğun önceliği "açık kural > yüksek indirim". Oranın %20 mi %25 mi olduğu ekibin sorunu değil. Kimin, ne zamana kadar, hangi kalemde, nasıl ödeyerek indirim alacağı ekibin sorunu.
6. **Kazanç ve kayıp, dürüstçe:** Ekip boş saatlerin dolmasından ve prim tabanı korunursa ek seanstan kazanır (varsayım: doluluk verisi yok). Kaybı, kural yazılmazsa artan tartışma, iade talebi ve takip yükü olur. Bu koltuk "gönderme" demiyor. "Kural kartı gelmeden gönderme" diyor. Bu da kullanıcının "hemen gönderelim" umuduyla çelişiyor; çatışmayı saklamıyorum.

## 2. Where the dossier is wrong, incomplete or mis-posed

1. **F2 eksik ve kaynak aralığı yanlış.** Dosya paket listesini "`masaj.tsx` satır 14-19" diye veriyor. Dizi aslında 14-21. satırlarda ve 20. satırda bir paket daha var: **"10 masaj + 10 kese köpük 38.000 TL"** (olgu: dosyayı okudum). Bu paket ne dosyada ne PDF'te var. Masada ilk sorulacak sorulardan biri "kombine paket ve 30'lu da indirimli mi?" olur. Kural kartında cevabı olmalı.
2. **Seçenek tablosu (b)'nin maliyetini olduğundan düşük gösteriyor.** "Düzeltmelerle gönder: PDF yeniden üretimi birkaç dakika" yazıyor. Oysa gerçek darboğaz PDF değil, işletmenin vermesi gereken kararlar: son tarih, uygunluk, paket ödemesi ve kullanım süresi, hafta sonu geçerliliği. Bunlar (c) gibi işletme onayı ister. (b) ile (c) arasındaki çizgi dosyada yanlış yerden çekilmiş.
3. **Seçeneklerin hiçbirinde uygulayan ekip yok.** Dört seçenek de yalnızca PDF'in içeriğini soruyor. Hangisi seçilirse seçilsin, ilk mesaj gelmeden resepsiyonun elinde bir sayfalık iç kural kartı olmalı. Dosyada böyle bir eylem kalemi yok. Eksik seçenek şu: "(b) + ön büro brifingi + önce tek grupta pilot."
4. **"Kanal 7 ile aynı oran" benzetmesi yanlış kurulmuş.** Kanal 7 teklifi İK üzerinden, çalışanlığı doğrulanabilen kapalı bir gruba yapılan kurumsal bir üyelik planı (olgu: F12; dokümanda masaj fiyatı yok). Tenis WhatsApp grubu ise açık ve kişiden kişiye iletilebilen bir kanal (olgu: COUNCIL §1). Aynı indirim oranı, aynı doğrulanabilirlik anlamına gelmiyor. Polis üyeliği görselinde de doğrulama yöntemi yazmıyor (olgu: `Main.dc.html` metnini çıkardım; "kimlik", "belge" vb. ifade yok). Yani dosyalarda örnek alınabilecek yazılı bir doğrulama kuralı bulamadım.
5. **Hafta sonu saati sorusu dosyadakinden daha ağır.** Sitede "Her gün 07.00–22.00" en az 10 yerde geçiyor: `site-footer.tsx` 18 ve 30, `page-kit.tsx` 67 ve 110, `home.tsx` 19 ve 47, `havuz.tsx` 9, `fitness.tsx` 18, `app/layout.tsx` 9, `lib/seo.ts` 6 (olgu: grep). Sitenin randevu penceresi her gün için 07:00'den başlayan saatler sunuyor (olgu: `booking-dialog.tsx` satır 25, 420. dakika = 07:00). "Hafta sonu 08:00" ifadesi yalnızca bir üyelik görselinde var ve orada **"Tesis saatleri"** başlığıyla yazılmış (olgu: F16, metni çıkardım). PDF tek aykırı kaynağı seçmiş ve bu saati "RANDEVU" başlığının altına koymuş. Tesis saati ile masaj (terapist) saatinin aynı olup olmadığı dosyada hiç sorulmamış (bilinmiyor). Hangisi doğruysa diğer taraf düzeltilmeli. Cumartesi 07:30'da kapıya gelen misafiri ön büro karşılar.
6. **PDF, kaynaktaki Derin Doku tanımını sertleştirmiş; dosya bunu işaretlememiş.** Site: "Daha belirgin baskıyı tercih edenler için ... Baskı, tercihinize göre ayarlanır" (olgu: F11). PDF: "Boyun, omuz ve sırta odaklanan **güçlü** baskı" ve "KORTTAN SONRA" etiketi (olgu: `index.html` satır 144-145). Etiket işletme kaynağında yok (F18 kuralı). Etiket, masaj öncesi baskı tercihini konuşacak terapiste "maçtan hemen sonra güçlü baskı" beklentisiyle gelen bir misafir bırakıyor.
7. **"Masajlara hamam, sauna ve buhar odası dahil" satırının kapsamı belirsiz.** Satır "İki kişilik" bölümünün altında duruyor. Oysa site, Çift Masajı için "sauna, hamam ve **havuz**" diyor (olgu: `rituals.ts` satır 8). VIP için de süitin kendi sauna ve hamamı var, ortak alan kullanılmıyor (olgu: `page-kit.tsx` satır 81, vip SSS). Paket seanslarına hamam ve saunanın dahil olup olmadığı sitede yazmıyor (olgu: aradım, bulamadım). Kese Köpük için site yalnızca "Mermer hamamda, 30 dakika" diyor. Masada "paket seansımda sauna var mı?" sorusunun cevabı yazılı değil.
8. **Sitenin kendi içinde VIP kapsamı tutarsız.** `lib/seo.ts` satır 9 VIP'e "kese köpük" dahil diyor. `rituals.ts` satır 3 ve PDF demiyor (olgu). PDF doğru kaynağı izlemiş. Ama misafir Google'da gördüğü açıklamayla gelirse masada tartışma çıkar. Bu dosyanın kapsamı dışında, ama işletmeye bildirilmeli.
9. **Doğru bulduklarım:** F19'daki tüm indirimli fiyatlar aritmetik olarak doğru (her birini yeniden hesapladım). PDF metni `index.html` ile aynı (olgu: `pdftotext -layout`). Hazır mesaj bağlantısı PDF'e gömülü (olgu: `strings` ile `wa.me/905330713373?text=...` görüldü). F3, F6, F7, F8 satır numaraları doğru.

## 3. Evidence

| Claim | Type | Source or method |
|---|---|---|
| Sitede ayrıca "10 masaj + 10 kese köpük 38.000 TL" paketi var; dosyada ve PDF'te yok | fact | `/home/user/navitas-topkapi/components/pages/masaj.tsx` satır 20 (repo HEAD 0a72fbc, 2026-10-31) |
| Sitede "Ön ödeme yok" yalnızca randevu bağlamında geçiyor; paket ödemesine dair kural bulunamadı | fact (arama sonucu; yokluğun kanıtı değil) | `grep -rn -E "peşin\|taksit\|ödeme\|nakit\|kredi kart\|son kullan\|geçerli\|kontenjan\|kimlik"` (`*.ts`, `*.tsx`, `*.md`) |
| PDF'te "Ön ödeme yok, randevuyla" satırı paketlerin hemen altındaki kutuda | fact | `index.html` satır 207; `pdftotext` çıktısı |
| 20'li İsveç tenisçi seansı 1.225 TL: liste tekin %59,2, tenisçi tekin %49, liste 30'lunun (1.666,67) %26,5 altında | estimate | Aritmetik, F1/F2/F19 |
| 20'li Mix tenisçi seansı 1.400 TL, liste Derin Doku'nun %60 altında | estimate | Aritmetik |
| Tenisçi tek İsveç (2.400 TL), mevcut liste 10'lu paket seansından (2.500 TL) %4 ucuz | estimate | Aritmetik; mevcut 10'lu sahiplerinin fark talebi riskini gösterir |
| 4 kişi bir 20'li paketi bölüşürse kişi başı 6.125 TL'ye 5 seans | estimate | 24.500 / 4; paylaşım kuralı F3 |
| Site saatleri en az 10 yerde "Her gün 07.00–22.00"; randevu penceresi her gün 07:00'den başlıyor | fact | grep; `booking-dialog.tsx` satır 25 |
| "Hafta sonu 08:00-22:00" yalnızca polis üyelik görselinde, "Tesis saatleri" başlığıyla geçiyor | fact | `Main.dc.html` metni (F16 yolu) |
| Polis görselinde doğrulama yöntemi yazmıyor | fact | Aynı dosya, HTML etiketleri temizlenerek okundu |
| PDF'te Derin Doku "güçlü baskı" ve "KORTTAN SONRA"; sitede "daha belirgin baskı, tercihinize göre ayarlanır" | fact | `index.html` 144-145; `rituals.ts` 7 |
| VIP kapsamı `seo.ts` (kese köpük dahil) ile `rituals.ts` (yok) arasında tutarsız | fact | `lib/seo.ts` satır 9; `lib/rituals.ts` satır 3 |
| Resepsiyonun tenisçiliği doğrulayacak bir aracı yok | assumption | Dosyada kulüp kartı ya da üye listesi bilgisi yok |
| Terapist primi seans fiyatına bağlı | assumption | Persona kartı; dosyada bordro verisi yok |
| Paketler peşin satılıyor | assumption | Dosya E4; kaynak yok |
| Kadın ve erkek hamamı ayrı olduğu için kese köpük uygunluğu cinsiyete göre personel planına bağlı olabilir | assumption | F7'den çıkarım; personel verisi yok |
| PDF metni `index.html` ile aynı; WhatsApp bağlantısı ve hazır mesaj gömülü | fact | `pdftotext -layout`, `strings` |

## 4. Risks from this seat

**(a) Olduğu gibi gönderilirse:**
- Paket satan resepsiyon "Ön ödeme yok yazıyordu" itirazıyla karşılaşır. Ya kural esnetilir ya da misafir kaybedilir.
- Son tarih olmadığı için Aralık'ta, Ocak'ta "Kasım 2026" yazan PDF'le gelen misafirle tartışma çıkar. Alt bilgideki "Kasım 2026" ifadesini kimi geçerlilik tarihi, kimi baskı tarihi olarak okur.
- Kapıda "tenisçiyim" diyene ne yapılacağı belli değil. Her personel farklı karar verir ve aynı gün iki misafir aynı hizmete iki farklı fiyat öder.
- Mevcut 10'lu ve 30'lu paket sahipleri aynı tenis grubundaysa fark ya da iade ister. Cevap yazılı değil.

**(b) Düzeltmelerle ama kural kartı olmadan gönderilirse:** PDF düzelir, masa yine kuralsız kalır. Riskler (a) ile aynı, yalnızca "ön ödeme" sorunu kalkar.

**(c) Fiyat yapısı değiştirilirse:** VIP'i ya da bazı kalemleri çıkarmak ekip için sorun değil; PDF'te olmayan kalem indirimsizdir. Ama kalem bazında istisna eklemek ("VIP'te %10", "hafta sonu hariç ama yalnız paketlerde") masada hata üretir. Her yeni istisna bir yanlış fiyat kaynağıdır.

**(d) Gönderilmezse:** Ekibe ek yük yok. Boş saat varsa (bilinmiyor) gelir fırsatı kaçar.

**Sessiz hatalar (en tehlikelileri, çünkü şikâyet olarak görünmezler):**
1. **İndirim sızıntısı:** Tartışmadan kaçmak için kapıda indirim verilir ve kaynak "tenis" olarak kaydedilmez. Hem liste fiyatı fiilen aşınır, hem pazarlamanın ölçtüğü dönüşüm bozulur.
2. **Paket hakkı kaybı:** Paylaşılan pakette kimin kaç seans kullandığı kâğıtta ya da hafızada tutulur. Hatalar aylar sonra, paket bitince ortaya çıkar.
3. **Terapist motivasyonu:** Prim fiyata bağlıysa indirimli paket sahibine en kötü saatler verilir ya da özen azalır. Bu, şikâyetten önce Google yorumunda görünür.
4. **Kapasite çakışması:** Çift masajı ve VIP aynı anda iki terapist gerektiriyor (olgu: `rituals.ts` 3 ve 8). İndirimli talep hafta sonu ve akşama yığılırsa tam fiyatlı misafir yer bulamaz (varsayım: doluluk verisi yok).

## 5. The cheapest decisive step

**Adım:** İşletme müdürü ile resepsiyon sorumlusunun aşağıdaki **ön büro kural kartını** yazılı olarak (bir WhatsApp mesajı yeterli) doldurması. Tahmini süre 15–20 dakikalık tek görüşme. Boşluklar işletmenin kararıdır; köşeli parantezdeki hiçbir değeri ben önermiyorum.

1. Son tarih: Tek seans **[tarih]'e kadar yapılan** seanslarda mı, yoksa **[tarih]'e kadar alınan** randevularda mı geçerli? Paket **[tarih]'e kadar satın alınan** paketlerde mi?
2. Kim hak kazanır: Bu listedeki hazır mesajla ya da "TENİS" yazarak WhatsApp'tan randevu alan herkes mi, yoksa grup bazlı kod listesi mi?
3. Kapıda "tenisçiyim" diyene ne yapılır? (Önerim: "Hemen listedeki WhatsApp mesajını gönderin, uygulayalım." Böylece hem kural tek kalır hem kaynak kaydı oluşur.)
4. Paket ödemesi: Peşin mi? Nakit mi, kart mı, taksit mi?
5. Paket kullanım süresi: [ay]. Paylaşımda kimler kullanacak, satın alırken adları kayda geçer mi?
6. Mix pakette hangi masajlar seçilebilir? Navitas Spesiyal dahil mi?
7. 30'lu İsveç ve 10+10 kombine paket kampanyada mı? (Değilse "listede olmayan kalemlerde indirim yok".)
8. Hafta sonu ve akşam saatlerinde geçerli mi? (Kısıt varsa PDF'e yazılmalı; gizli koşul olmaz.)
9. Başka indirimle (polis, Kanal 7 kurumsal, üyelik) birleşir mi?
10. Mevcut paket sahibi fark isterse ne söylenir?
11. Hafta sonu açılış saati 07.00 mı, 08.00 mı? Terapist randevu saatleri tesis saatleriyle aynı mı?
12. İndirimli seansta terapist primi hangi fiyattan hesaplanır?
13. Paket seanslarına hamam ve saunanın dahil olup olmadığı.

**Sonuçlara göre konumum (önceden ilan ediyorum):**
- **1, 2, 4, 5 ve 11 cevaplanırsa** (b)'yi desteklerim: kural kartı resepsiyona asılır, PDF §6'daki satırlarla güncellenir, önce tek gruba gönderilir.
- **4 veya 5 cevaplanmazsa** (paket ödemesi ya da kullanım süresi belirsizse) paketler PDF'ten çıkarılsın, yalnızca tek seans %20 ile gönderilsin; paketler için "WhatsApp'tan yazın" yazılsın.
- **1 veya 2 cevaplanmazsa** (son tarih ya da uygunluk kuralı yoksa) ertelenmesini (d) savunurum.
- **12'nin cevabı "prim indirimli fiyattan hesaplanır" olursa** ekip adına 20'li paketlerin tenisçi teklifinden çıkarılmasını ya da primin ayrı belirlenmesini isterim. Karar işletmenindir; bu koltuğun itirazı kayda geçsin.

## 6. Conditions and red lines

**Destek için olması gerekenler:**
- Resepsiyonda, ilk mesaj gelmeden önce, bir sayfalık iç kural kartı (§5) ve PDF'in basılı bir kopyası.
- PDF'te son tarih ve "nasıl hak kazanılır" satırı.
- "Ön ödeme yok" yalnızca tek seanslara bağlanmış olmalı.
- Kaynak kaydı: lead takip tablosundaki "DATA KAYNAĞI" sütununa tek bir sabit değer girilmeli, örneğin "Tenis PDF – Kasım 2026" (olgu: F17 sütunu var). Kod hazır mesajın içinde gelmeli; resepsiyon müşteriye "hangi gruptan geldiniz?" diye sormak zorunda kalmamalı. Grup başına kod istenirse en fazla birkaç kod olmalı ve hepsi karta yazılmalı.
- Önce tek grupta pilot. Resepsiyon ilk iki haftada gelen her soruyu not eder; diğer gruplara bu notlarla düzeltilmiş sürüm gider.

**PDF için önerilen tam metin değişiklikleri** (köşeli parantezler işletmenin dolduracağı yerlerdir; yeni fiyat ya da süre önermiyorum):
1. Kutu satırı "Ön ödeme yok, randevuyla" → **"Tek seanslarda ön ödeme yok; saatinizi WhatsApp'tan onaylıyoruz."**
2. Paket notu → **"Paketler arkadaşınızla paylaşılabilir. Mix pakette her seansta masaj türünü siz seçersiniz. Paket ödemesi: [işletme]. Kullanım süresi: [işletme]."** İşletme bu iki bilgiyi vermezse paketler çıkarılır (§5). "Koşulları WhatsApp'tan paylaşıyoruz" yazmak ön büro için yeterli olurdu, ama müşteri bunu gizli koşul olarak okur; bu yüzden önermiyorum.
3. Kutuya yeni satır → **"Tenisçi fiyatları [tarih]'e kadar geçerlidir. WhatsApp'ta bu listedeki mesajla ya da "TENİS" yazarak randevu alın. Başka indirimle birleşmez."** "Birleşmez" ifadesi ancak işletme 9. maddeye öyle cevap verirse yazılmalı.
4. Alt bilgideki "Kasım 2026" → **"Son geçerlilik: [tarih]"**. Belirsiz tarih damgası kaldırılmalı.
5. Derin Doku açıklaması → **"Boyun, omuz ve sırta odaklanan, daha belirgin baskı"**. "KORTTAN SONRA" etiketi kaldırılmalı, çünkü işletme kaynağında yok (F18).
6. Saat satırı: İşletmenin onayladığı tek bir saat yazılmalı ve site ile PDF aynı olmalı. Onay gelene kadar sitedeki "Her gün 07.00–22.00" kullanılabilir ya da satır şöyle değiştirilebilir: **"Saat ve uygunluğu WhatsApp'tan onaylıyoruz."**
7. 8. maddede kısıt varsa (ör. hafta sonu geçersiz) PDF'e açıkça yazılmalı.

**Kabul etmeyeceklerim (kırmızı çizgiler):**
- PDF'te yazıp işletmede uygulanmayan bir ifade. Bugün bunun örneği "Ön ödeme yok" satırı ile peşin paketin yan yana durması.
- Resepsiyonun uygulayamayacağı bir uygunluk koşulu, örneğin kulüp kartı ya da üyelik kanıtı. Böyle bir kart yoksa (varsayım) bu koşul kâğıt üzerinde kalır ve masada tartışmaya dönüşür.
- Son tarihi olmayan indirim.
- Kalan seans ve kullanıcı kaydı tanımlanmadan satılan paylaşılabilir paket.
- Kalem kalem istisna yağmuru. İndirimsiz olacak bir kalem varsa PDF'ten çıkarılsın; PDF'te dursun ama "bunda geçmez" denmesin.

## 7. One line

Ön büro %20 ve %30'u masada uygulayabilir ama kuralsız uygulayamaz. Önce işletme son tarihi, kimin hak kazandığını, paket ödemesini ve kullanım süresini yazsın; sonra "Ön ödeme yok" tek seanslara bağlanmış ve koşul satırı eklenmiş PDF'i tek bir gruba göndersin. Paket kuralları gelmezse yalnızca tek seans indirimi gitsin, son tarih ve uygunluk kuralı da gelmezse ertelensin.
