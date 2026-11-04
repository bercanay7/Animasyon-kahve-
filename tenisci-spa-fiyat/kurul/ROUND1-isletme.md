# ROUND 1: Spa işletme müdürü (gelir, marj, kapasite) (isletme)

**Dossier:** DOSSIER-01-tenisci-spa-fiyat.md. **Addenda read:** yok (kurul klasörüne `ls` ile baktım, ADDENDUM-01* dosyası bulunmadı).
**Round 1, independent:** no other member's report was read before this one was written.

**Position:** (c) Fiyat yapısı değiştirilerek gönderilsin. Tek seanslarda %20 ve 10'lu paketlerde %30 kalsın. 20'li paketler (seans 1.225 ve 1.400 TL) ve VIP indirimi çıkarılsın, Çift Masajı liste fiyatında kalsın. Son geçerlilik tarihi, paket kullanım süresi ve düzeltilmiş "ön ödeme" satırı yazılmadan PDF gönderilmesin.
**Confidence:** orta (maliyet ve doluluk verisi yok; §5'teki adımla yükselir ya da pozisyon değişir)

## 1. Position and why

1. **Bugünkü PDF bu koltuğun bir kırmızı çizgisini kesin olarak, diğerini muhtemelen aşıyor.** Kesin aşılan çizgi şu: indirimin süresi, kontenjanı, doğrulaması ve paketlerin son kullanma tarihi yok (F23), PDF de WhatsApp'ta serbestçe iletilebiliyor. Altbilgideki "Kasım 2026" bir geçerlilik tarihi değil. Muhtemel aşılan çizgi 20'li İsveç paketinde seansın 1.225 TL olması: seans maliyeti bilinmiyor (E5), bu fiyatın terapist ve sarf maliyetini karşılayıp karşılamadığı bilinmeden basılamaz. Bu yüzden (a) "olduğu gibi gönder" seçeneğine hayır diyorum.

2. **Asıl sorun indirim oranı değil, evde yeni bir taban fiyat oluşması.** Tenisçiye 10'lu İsveç 17.500 TL (seansı 1.750). Bu, bugün herkesin alabildiği liste 20'li paketin seans fiyatına eşit. Tenisçiye 10'lu Mix ise seansı 2.100 TL; bu da liste 20'li Mix'in (2.000) üstünde kalıyor. Yani 10'lu paketlerde işletme yeni bir dip fiyat yaratmıyor, yalnızca taahhüt eşiğini 35.000 TL'den 17.500 TL'ye indiriyor. İki tane 10'lu tenisçi paketi 35.000 TL ediyor, yani tam liste 20'li fiyatı. 20'li tenisçi paketleri ise yeni dip fiyat yaratıyor. İsveç'te seans 1.225 TL; evin bugünkü en düşük fiyatı olan liste 30'lu paketin (seans 1.666,67) %26,5 altında. 20'li Mix'te seans 1.400 TL; liste 20'li İsveç'in (1.750) bile altında. Gruplara düşen dip fiyat geri alınamaz.

3. **Paylaşım kuralıyla (F3) birleşince 20'li tenisçi paketi bir "grup alımı" aracına dönüşür.** Bir kişi paketi 24.500 TL'ye alır, gruptan 20 kişi seansı 1.225 TL'den kullanır. Bu, tek seans liste fiyatının %59 altı ve kimse ayrıca paket taahhüdü vermiyor (senaryo; F3 bunu engellemiyor). Böylece paketlerde "tenisçiye özel" doğrulaması da anlamsızlaşır. Son kullanma tarihi olmadığı için, liste fiyatları ileride güncellendiğinde (varsayım) bu seanslar bugünkü fiyattan uzun süre kapasite bağlar.

4. **Peşin paket nakdi bu koltuk için tek seanstan daha değerli.** Tek seansta %20, pakette %30 farkı doğru yönde, çünkü tenisçiyi pakete itiyor; 10'lu paketleri bu yüzden tutuyorum. Tek seanstaki %20'nin bir bedeli var ve bunu açıkça söylüyorum. Tenisçi tek İsveç 2.400 TL, liste 10'lu paketin seans fiyatından (2.500) ucuz. Tenisçi Derin Doku ve Aromaterapi 2.800 TL, liste 10'lu Mix seansından (3.000) ucuz. PDF gruptan dışarı sızarsa liste paketi alacak olan müşteri tenisçi tek seans fiyatını ister. Bu bedeli yalnızca süreli bir teklifte (bkz. §6) kabul ederim, süresiz bir teklifte kabul etmem.

5. **VIP ve Çift Masajı indirimine karşıyım.** VIP'te indirim 3.000 TL. Bu ürün üç saat boyunca tek süiti ve iki terapisti bağlıyor, tenis sonrası toparlanmayla bağı zayıf ve bir prestij ürünü. Süitin boş kaldığını gösteren veri yok; boş kalıyorsa bu ayrı ve dar bir teklifin konusu, tenis listesinin değil. Çift Masajı ise liste fiyatıyla zaten kişi başı 2.000 TL, yani menünün kişi başı en ucuz masajı. %20 indirimle terapist başına 1.600 TL'ye iner ve karşılığında hiçbir taahhüt alınmaz. İki tenis arkadaşı için liste fiyatı zaten cazip olduğundan indirime gerek yok.

6. **Göndermemek (d) bu koltuğun tercihi değil.** Boş kalan saatin geliri geri gelmez ve tenisçiler mantıklı bir segment. Ancak son tarih ve paket kullanım süresi bugün kararlaştırılamıyorsa, PDF'i bu haliyle göndermektense ertelemek daha az zararlıdır. Kullanıcının isteğiyle açık bir çatışma var: kullanıcı 20'li paketin de %30 indirimle yazılmasını istedi (F13). Maliyet bilinene kadar bu koltuk buna karşı.

## 2. Where the dossier is wrong, incomplete or mis-posed

- **F2 eksik.** `components/pages/masaj.tsx` dosyasındaki paket dizisi 15-20. satırlarda. Dosya 14-19. satırları kaynak göstermiş ve altıncı paketi atlamış: "10 masaj + 10 kese köpük 38.000 TL" (satır 20). `git log -L` ile baktım, bu paket 2026-10-03'ten beri sitede. PDF'te yok, ama masada "bu da %30 indirimli mi?" sorusu gelecek. Yazılı bir kural gerekiyor: indirim yalnızca listedeki paketlerde geçerli.
- **§8 soru 2 iki farklı tabanı karıştırıyor.** "%20 ile %30 arasındaki fark" iki ayrı tabana göre hesaplanıyor: %30, zaten hacim indirimi içeren liste paket fiyatına uygulanıyor. Tek seans liste fiyatına göre gerçek indirimler şöyle: 10'lu İsveç %41,7; 20'li İsveç %59,2; 20'li Mix Aromaterapi veya Derin Doku için kullanılabiliyorsa %60. Tenisçi tek İsveç (2.400) ile tenisçi 20'li seans (1.225) arasındaki fark %49; "10 puanlık fark" değil.
- **Fiyat basamağındaki terslikler dosyada yok.** 2.400 < 2.500 (liste 10'lu seans); 2.800 < 3.000 (liste 10'lu Mix seans); 1.225 < 1.666,67 (liste 30'lu seans).
- **"Reversible? Kısmen" sütunu eksik kurulmuş.** Satılan her paket bir seans borcudur ve son kullanma tarihi yoksa açık uçludur. Geri alınamayan şey yalnızca "gruplarda kalan fiyat" değil, satılmış seanslardır.
- **Eksik seçenekler:** (i) "paket öncelikli" yapı: yalnızca 10'lu paketler indirimli; (ii) önce 1-2 grupta süreli pilot, sonra yaygınlaştırma; (iii) tek seans indirimini yalnızca boş saatlerle sınırlamak (saatleri işletme kendi randevu defterine göre belirler); (iv) VIP ve Çift Masajı'nı indirim dışında tutmak.
- **§6'da olmayan bilinmeyenler:** (1) Mix paketin hangi hizmetleri kapsadığı (Navitas Spesiyal dahil mi?). Sitede tanımlı değil; `grep` ile aradım, yalnızca "istediğiniz masaj türünü seçersiniz" cümlesi var. Kapsam gerçek indirimi değiştirir. (2) Fiyatların KDV dahil olup olmadığı ve oranı; net geliri değiştirir. (3) Kart ya da taksitle ödemede komisyon. (4) Terapistlere nasıl ödendiği (sabit maaş mı, seans primi mi). Seans başı ek maliyet buna bağlı: maaşlı ve boş bekleyen bir terapistin ek maliyeti sarf malzemesine yakındır.
- **F13 emsali dar.** Kullanıcının hatırladığı 25.000 → 17.500 indirimi kapalı ve işveren üzerinden tanımlanabilen bir kurumsal gruba (Kanal 7) verilmişti ve yalnızca 10'lu paket içindi. 20'li pakete %30 bu oturumda verilen yeni bir karar ("20'li paketi de yazarsın"); bir emsali yok. Dosyanın F12 özetine göre Kanal 7 üyelik indirimi de hacme bağlı ve kademeliydi (20+ kişi toplu). Açık WhatsApp kanalının riski kapalı bir kurumsal grubun riskiyle aynı değil.
- **PDF'te dosyanın çelişki olarak işaretlemediği bir ifade var.** "Ön ödeme yok, randevuyla" kutusu paketlerin hemen altında duruyor ve paketleri de kapsıyor gibi okunuyor. Paket satışı doğası gereği peşin olur (E4, varsayım). Kaynakta (F6; `page-kit.tsx` satır 68 ve 74, `masaj.tsx` satır 86) bu cümle tek seans fiyatı ve randevu bağlamında geçiyor.
- **"Kasım 2026" altbilgisi belirsiz.** Geçerlilik tarihi mi, baskı tarihi mi olduğu anlaşılmıyor. F23'teki tespit doğru, ama bu satır okuyana örtük bir süre gibi gelebilir.
- **Kontrol ettiğim ve doğru bulduğum maddeler:** F1; F2'deki beş fiyat; F3; F6; F9; F16 (24 Ekim görselinde "Hafta sonu 08:00-22:00" yazıyor); F19 hesapları; F20 metni (`pdftotext` ve önizleme); F21 bağlantısı (`strings`); F22 sayfa boyutu (`pdfinfo`).

## 3. Evidence

| Claim | Type | Source or method |
|---|---|---|
| Tek seans liste fiyatları: 3.000 / 3.500 / 3.500 / 4.500 / 2.250 / Çift 4.000 (iki kişi, iki terapist) / VIP 15.000 | fact | `/home/user/navitas-topkapi/lib/rituals.ts` satır 3-9 |
| Sitede 6 paket var; altıncısı "10 masaj + 10 kese köpük 38.000 TL" | fact | `masaj.tsx` satır 15-20; `git log -L14,21` (2026-10-03'ten beri) |
| Paketler başkasıyla paylaşılabilir | fact | `page-kit.tsx` satır 75; `masaj.tsx` satır 71 |
| "Ön ödeme yok" kaynakta tek seans fiyatı ve randevu bağlamında geçiyor | fact | `page-kit.tsx` satır 68 ve 74; `masaj.tsx` satır 86 |
| PDF fiyatları: tek seans 2.400 / 2.800 / 2.800 / 3.600 / 1.800 / 3.200 / 12.000; paket 17.500 / 24.500 / 21.000 / 28.000 | fact | `pdftotext -layout` ile PDF; `onizleme.jpg` |
| Tek seans İsveç liste fiyatına göre gerçek indirim: 10'lu %41,7; 20'li %59,2; 20'li Mix (Aromaterapi veya Derin Doku 3.500'e göre) %60 | estimate (aritmetik) | `/tmp/claude-0/-home-user/d6383d34-f4c3-53e1-9fb3-44f29c9d2c31/scratchpad/isletme/fiyat.py` |
| Basamak terslikleri: 2.400 < 2.500; 2.800 < 3.000; 1.225, liste 30'lu seansın %26,5 altında | estimate (aritmetik) | aynı betik |
| İki tane 10'lu tenisçi paketi 35.000 TL, yani liste 20'li fiyatı; 10'lu paketler yeni dip fiyat yaratmıyor | estimate (aritmetik) | F2, F19 |
| Çift Masajı terapist başına liste 2.000 TL, tenisçi fiyatıyla 1.600 TL | estimate (aritmetik) | `rituals.ts` ("iki terapistle eşzamanlı") |
| 20'li tenisçi paketinin grup alımıyla 20 kişiye seansı 1.225 TL'den dağılabilmesi | estimate (senaryo) | F3 paylaşımı engellemiyor; gerçekleşme sıklığı bilinmiyor |
| Tenisçiler çoğunlukla akşam ve hafta sonu, maçtan sonra gelir; yani indirim yoğun saatlere düşer | assumption | Veri yok; randevu defteriyle sınanmalı |
| Liste fiyatları ileride güncellenir; süresiz paket bugünkü fiyattan kapasite bağlar | assumption | `masaj.tsx` satır 7: "Prices from the Navitas price list (October 2026)", fiyat listesi tarihli tutuluyor |
| Seans maliyeti, doluluk, KDV, paket son kullanma ve Mix kapsamı sitede yok | fact (arama) | Site reposunda (node_modules, build ve vendor hariç) maliyet, prim, doluluk, geçerlilik ve KDV için `grep` yaptım, ilgili bir şey çıkmadı. Bu, verinin olmadığı anlamına gelmez; kasa ve bordroda olur |
| Kanal 7 teklifi kapalı bir kurumsal gruba yönelikti; üyelik indirimi hacimle kademeliydi | fact (dosyaya göre) | F12; dokümanı kendim açmadım |
| PDF'te geçerlilik, kontenjan, doğrulama, son kullanma ve ödeme şekli yok | fact | `index.html`; F23 |

**Başabaş analizi (estimate, yöntem):** İndirim yalnızca gerçekten yeni gelen müşteri getiriyorsa kâr ettirir. Zaten indirimsiz alacak olan bir müşteri indirimli alırsa, işletme indirim tutarı (D) kadar kaybeder. Yeni gelen bir müşteri ise P − v katkı getirir (P: indirimli fiyat, v: seans başı ek maliyet). Kâra geçmek için gereken yeni müşteri payı i* = D / (P − v + D). **v değerleri işletmenin maliyeti değil, yalnızca senaryodur.** KDV oranı da varsayımdır ve muhasebeyle doğrulanmalıdır.

| Ürün (P, D) | KDV yok: v=600 / 900 / 1.200 | Fiyat %20 KDV dahilse: v=600 / 900 / 1.200 |
|---|---|---|
| Tek İsveç (2.400; 600) | %25 / %29 / %33 | %26 / %31 / %38 |
| 10'lu İsveç seansı (1.750; 750) | %39 / %47 / %58 | %42 / %53 / %71 |
| 20'li İsveç seansı (1.225; 525) | %46 / %62 / %95 | %51 / %78 / zarar (KDV hariç net 1.020,8 < v) |

Okuması şöyle: tek seans indirimi maliyete karşı dayanıklı. 20'li tenisçi paketi ise maliyete çok duyarlı. Seans maliyeti 1.000 TL civarındaysa paket ya zarar eder ya da neredeyse her alıcının gerçekten yeni müşteri olmasını gerektirir.

## 4. Risks from this seat

- **(a) Olduğu gibi gönderilirse fark edilmesi zor bir başarısızlık olur.** 20'li tenisçi paketi iyi satar, ilk ay kasaya nakit girer, ciro iyi görünür. Ama seanslar sonraki aylarda 1.225 TL'den kullanılır. Varsayımım doğruysa bu seanslar akşam ve hafta sonu yoğun saatlerde tam fiyatlı randevuların yerini alır. Kayıp, nakit girişinden aylar sonra "doluluk yüksek ama seans başı gelir düşük" olarak ortaya çıkar ve nedeni kolayca görülmez.
- **Grup alımı:** tek paketi 20 kişi kullanır. Yeni müşteri sayısı artmış görünür ama seans başı gelir 1.225 TL'de kalır.
- **Liste fiyatı aşınır:** PDF gruptan dışarı iletilir ve 25.000 TL'lik paket alan müşteri 2.400 TL'lik tek seans fiyatını görür.
- **Terapist primi:** prim seans fiyatına bağlıysa (varsayım) indirim terapistin gelirini düşürür. Ekip düşük fiyatlı paket seanslarını isteksiz alır ve hizmet kalitesi düşer. Bu hiçbir raporda görünmez.
- **(b) Yalnızca metin ve tasarım düzeltilirse:** fiyat riskleri olduğu gibi kalır.
- **(c) Benim önerim uygulanırsa:** rozet daha az etkileyici olur ve bazı paket satışları kaçar. 20'li paket isteyen tenisçi liste 20'li pakete (35.000) ya da iki tane 10'lu pakete yönlendirilir. Bu bedeli kabul ediyorum.
- **(d) Hiç gönderilmezse:** boş saatler boş kalır; kaybın büyüklüğünü ölçemiyoruz. Erteleme uzarsa teklif başka bir kanaldan, daha gevşek koşullarla yapılabilir.

## 5. The cheapest decisive step

İşletme sahibi ve muhasebe yaklaşık bir saatlik masa başı çalışmayla üç şeyi çıkarmalı:
1. 50 dakikalık bir masajda seans başı ek maliyet (v): terapistin seans primi ya da ücreti, yağ ve havlu yıkama, KDV hariç. Terapist maaşlıysa ve o saatte boş bekliyorsa ek maliyet sarf malzemesine yakındır; bunun ayrıca belirtilmesi gerekir.
2. Fiyatların KDV dahil olup olmadığı ve oranı.
3. Son 4 haftanın randevu defterinden gün ve saat bazında doluluk, özellikle hafta içi akşamlar ve hafta sonu.

**Pozisyonumu değiştirecek sonuçlar (şimdiden belirliyorum; eşikler bu koltuğun önerisidir):**
- **v ≥ 1.225 TL'nin KDV hariç neti** (fiyat %20 KDV dahilse 1.020,8 TL): 20'li tenisçi paketine kalıcı olarak hayır derim. Bu kırmızı çizgim.
- **v ≤ 600 TL ve tenisçilerin geleceği saatlerde boş kapasite var:** 20'li İsveç paketini 24.500 TL'den listeye geri alırım, ama yalnızca paket kullanım süresi yazılırsa (öneri: 12 ay). Bu durumda başabaş için alıcıların yaklaşık yarısının gerçekten yeni müşteri olması yeter (i* ≈ %51).
- **v 600 ile 1.020 TL arasında:** 20'li paket listeye girmez; pilottan yeni müşteri payı verisi gelene kadar bekler.
- **Akşam ve hafta sonu saatleri zaten neredeyse doluysa:** tek seans indiriminin de yalnızca boş saatlerde geçerli olmasını isterim (saatleri işletme belirler).

**Pilot ölçütü:** ilk iki haftada tenisçi fiyatıyla alanların kaçının daha önce kayıtlı müşteri olduğu, lead tablosundaki "DATA KAYNAĞI" sütunuyla (F17) ölçülür. Yeni müşteri payı §3'teki tabloda o ürünün eşiğinin altında kalırsa indirim gereğinden derin demektir.

## 6. Conditions and red lines

**Desteklemem için koşullar.** Aşağıdaki yeni sayıların ve kuralların hepsi işletmenin karar vereceği önerilerdir; işletme onaylamadan PDF'e girmez:
1. VIP satırı çıkarılsın. Çift Masajı ya çıkarılsın ya da "4.000 TL · iki kişi toplam" olarak, üstü çizili eski fiyat olmadan liste fiyatıyla kalsın.
2. Paket kartları yalnızca şunlar olsun: "10 SEANS İsveç paketi 17.500 TL · Seansı 1.750 TL" ve "10 SEANS Mix paket 21.000 TL · Seansı 2.100 TL". 20'li kartlar §5'in sonucu gelene kadar yer almasın.
3. "Kasım 2026" altbilgisinin yerine şu yazılsın: "Teklif 31 Aralık 2026'ya kadar alınan randevu ve paketlerde geçerlidir." (Tarih öneridir.)
4. Paket notuna şu eklensin: "Paketler satın alındıktan sonra 6 ay içinde kullanılır." (Süre öneridir; işletmenin mevcut bir kuralı varsa o yazılır.)
5. "Ön ödeme yok, randevuyla" satırı şöyle değişsin: "Tek seanslarda ön ödeme yok; randevu WhatsApp'tan." İşletme paketlerin peşin ödendiğini teyit ederse şu da eklensin: "Paket ücreti satın alırken ödenir."
6. Şu kural eklensin: "İndirim yalnızca bu listedeki hizmet ve paketlerde geçerlidir." Böylece 10+10 paketi ve 30'lu paket dışarıda kalır.
7. Mix paketin hangi masajları kapsadığını işletme yazılı olarak belirlesin. PDF'e ancak işletme teyit ederse yazılsın.
8. Ön büro kuralı: tenisçi fiyatı, hazır mesajla gelen ya da gruptan geldiğini söyleyen randevulara uygulanır. Kaynak lead tablosuna "Tenis PDF" olarak yazılır (F17).
9. PDF önce 1-2 gruba gitsin, iki hafta sonra genişletilsin.

**Kırmızı çizgiler:**
- Seans başı ek maliyetin altında kalan herhangi bir fiyat.
- Son geçerlilik tarihi ve paket kullanım süresi olmadan WhatsApp'a gönderim, yani süresiz ve herkese yayılan bir indirim.

Maliyet kontrolü yapılmadan liste 30'lu paketin altında bir tenisçi seans fiyatı basılmasını ve VIP'te indirimi kırmızı çizgi saymıyorum, ama ikisine de güçlü biçimde karşıyım.

## 7. One line

Tenisçi listesi gönderilsin ama 10'lu paketlerle sınırlı kalsın, son tarih ve paket kullanım süresi yazılsın; 1.225 TL'lik 20'li paket ve VIP indirimi, maliyet ve doluluk verisi bu fiyatların kâr bıraktığını gösterene kadar basılmasın.
