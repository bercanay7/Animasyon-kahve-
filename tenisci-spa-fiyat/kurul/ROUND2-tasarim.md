# ROUND 2: Mobil okunabilirlik ve marka tasarımcısı (tasarim)

**Read:** ROUND1-TALLY.md, every ADDENDUM-01*, and all Round 1 reports.

**Vote:** A
**Changed from round 1:** no
**Confidence:** high (ölçüler prototipten). WhatsApp'ın önizleme kırpması ve iki bağlantının cihazlarda çalışması hâlâ test edilmedi; bu kısım medium.

## 1. Vote and reason

1. **Round 1'deki (b) oyum A'ya karşılık geliyor; oy değişmedi, ayrıntılar 01C'ye göre güncellendi.** A, karar sahibinin istediği fiyat kapsamıdır ve K1-K10 ile birlikte gelir. Fiyat kapsamı bu koltuğun alanı değil (kartımdaki kör nokta). B, C ve D'nin gerekçeleri marj, fiyat merdiveni ve ölçümle ilgili. Hiçbiri okunabilirlikle ilgili değil. Bu koltuğun Round 1'deki koşulu, koşul satırlarının sayfayı uzatmadan ve okunur boyda yazılabilmesiydi. 01C (madde 17-21, 23) bu satırların içeriğini verdi. Prototipte hepsi sığdı ve sayfa uzamadı, kısaldı. Ayrıntılar yanıtın devamında.
   - Round 1'den değişen üç ayrıntı:
     - Üst satırdaki "KASIM 2026" yerine geçerlilik tarihi yazılıyor (01C-17).
     - İki kişilik bölümünün etiketi "%20 İNDİRİM" değil, yalnız "İKİ KİŞİ TOPLAM" oluyor, çünkü Çift Masajı indirimsiz (01C-23).
     - Uygunluk kuralı giriş metnine giriyor (01C-20).
2. **Ölçüm: koşul satırları sığıyor ve sayfa kısalıyor.** `index.html`'in bir kopyasını (proto2) bütün düzeltmelerle Playwright'ta işledim. Asıl dosyalara dokunmadım. Yeni sayfaya şunlar eklendi:
   - geçerlilik tarihi (üstte ve altta);
   - uygunluk kuralı;
   - paketlerin peşin ödendiği ve bir yıl içinde kullanıldığı;
   - Mix paketin kapsamı;
   - Çift Masajı'nın kendi dahil satırı.

   Bu eklere rağmen sayfa 3.639'dan 3.540 CSS px'e iniyor (−99 px). PDF 810 × 2.730 pt'den 810 × 2.656 pt'ye iniyor; boyutu 261 KB ve içinde iki wa.me bağlantısı var. Genişliğe sığdırılmış 390 pt'lik bir telefonda bu 1.278 pt eder. Bugünkü sayfa 1.314 pt. 660 pt görünür alanla bu, 1,99 yerine 1,94 ekran boyu demek. Yer, şu çıkarmalardan geldi:
   - rozet;
   - paket kartlarındaki "10 SEANS" etiketleri;
   - alt bölümdeki "RANDEVU" üst etiketi;
   - "Kortun yorgunluğunu..." cümlesi;
   - fotoğrafın 480'den 340 px'e inmesi.
3. **İlk ekran ve sohbet önizlemesi artık ana mesajı taşıyor.** Ölçümler prototipten, CSS px olarak:
   - Yatay önizleme şeridi (1,91:1, sayfanın ilk 565 px'i) şunları gösteriyor: logo, "31 ARALIK 2026'YA KADAR GEÇERLİ" (170-209), "Tenisçilere özel spa fiyatları" (223-386), "Tek seanslarda %20, paketlerde %30 indirim." ve "Tenisçi fiyatı için WhatsApp'tan yazmanız yeterli." (404-495). Görüntü: `/tmp/claude-0/-home-user/d6383d34-f4c3-53e1-9fb3-44f29c9d2c31/scratchpad/tasarim/r2/thumb191.png`. Bugünkü PDF'te bu şeritte yalnız logo, havlu ve rozetin yarısı görünüyordu.
   - Açılan ilk ekranda (0-1.830 px) bunlara ek olarak fotoğraf, beş tek seans fiyatı ve "Masaj paketleri · %30 İNDİRİM" başlığı görünüyor.
4. **Telefondaki yazı boyları (390 pt / 360 dp):**
   - Koşul satırları, bölüm etiketleri, tarih ve "Seansı X TL" 30 px'te: 10,8 / 10,0 pt.
   - Giriş metni 32 px'te: 11,6 / 10,7 pt.
   - Önemli metnin en küçüğü 28 px'te kalıyor (üstü çizili liste fiyatları, alt bilgi): 10,1 / 9,3 pt.
   - 26 px'te yalnız iki öğe kaldı: marka alt satırı "SPA & SPORTS · TOPKAPI" ve büyük rakamın yanındaki "TL" birimi (9,4 / 8,7 pt). İkisi de tek başına bilgi taşımıyor.

   Kartımdaki onay ölçütü (390 pt'de en küçük önemli metin 10 pt'nin üstünde, ana mesaj ilk ekranda) karşılanıyor. 9 pt kırmızı çizgimin altında önemli bilgi kalmıyor.
5. **B ya da C sayfayı daha da kısaltır, ama bu benim için bir gerekçe değil.** VIP satırı yaklaşık 133 px tutuyor. C'de 20'li kartlar da çıkarsa yaklaşık 248 px daha gider (kart satırı yüksekliği, prototipten ölçüldü). Uzunluk artık sorun değil: sayfa iki ekranın altında ve bugünkünden kısa. Karar sahibinin tuttuğu kalemleri tasarım gerekçesiyle kesmem.

**x99 önerisi: benimsemiyorum, hiçbir kalemde.** Gerekçeler:
- **Marka.** İşletmenin bütün fiyatları yuvarlak:
  - Yedi tek seans fiyatı 500 TL'nin katı, altı paket 1.000 TL'nin katı (`lib/rituals.ts` 3-9, `masaj.tsx` 15-20).
  - Polis görseli "35.000 TL" diyor (V59).
  - Repoda 9 ile biten tek fiyat Campus Challenge'ın 14.900'ü. Bu, yüzler basamağında bir indirim ve bir üyelik ürünü; sayfası da canlıda 404 dönüyor (01B-14; `CampusChallengeClient.tsx` satır 10'u kendim okudum).
  - Repoda x99 biçiminde hiçbir fiyat bulamadım (grep).

  x99, mağaza ve indirim zinciri dilidir. Kartımdaki teşvik, listenin "ucuz kampanya" gibi değil spa kalitesinde görünmesi.
- **Tipografi (ölçtüm).** Fiyatlar Marcellus ile yazılıyor ve bu yazı tipinde 3, 5, 7 ve 9 rakamları satır çizgisinin altına sarkıyor. "2.399"da üç rakam sarkar, "2.400"de hiçbiri sarkmaz. Sayfanın en büyük öğesi olan fiyat sütunu bu yüzden düzensiz bir siluete dönüşüyor. Karşılaştırma görüntüsü: `/tmp/claude-0/-home-user/d6383d34-f4c3-53e1-9fb3-44f29c9d2c31/scratchpad/tasarim/r2/x99_compare.png`. Genişlik açısından x99 bir sorun çıkarmıyor (2.400 TL 186 px, 2.399 TL 156 px). Ama bir yer kazancı da getirmiyor, çünkü sayfada yer sıkıntısı yok.
- **Tek fiyat sistemi.** Paketlerde x99 yapılamaz, çünkü karar sahibinin kendi kuralı "seans başı tam sayı" (17.499 / 10 = 1.749,90; tally not 2). Çift Masajı da indirimsiz 4.000 TL. x99 uygulanırsa aynı sayfada üç ayrı fiyat sistemi olur: x99'lu tek seanslar, yuvarlak paketler ve yuvarlak Çift. Okuyan bunu "neden bazıları 99" diye fark eder. Tek sistem, ilk bakışta taranmayı kolaylaştırır.
- **Kanal tonu.** grup-yoneticisi "%30'a varan" kalıbını broşür dili olarak reddetti. x99 da aynı dildendir ve onun "grup reklamdan rahatsız olur" uyarısına doğrudan dokunur.
- **Literatür (dürüst not).** Kanıt karışık, bu yüzden kararımı buna dayandırmıyorum.
  - Stiving (2000, *Management Science* 46(12)) yüksek kaliteli ürünlerde yuvarlak fiyatın daha sık kullanıldığını buldu. 2003'te yayımlanan bir yorum bu modele itiraz etti. Kaynaklar: https://ideas.repec.org/a/inm/ormnsc/v46y2000i12p1617-1629.html ve https://pubsonline.informs.org/doi/10.1287/mnsc.49.12.1753.25118
  - Wadhwa ve Zhang (2015, *JCR* 41(5)) duyguyla verilen satın alma kararlarında yuvarlak fiyatın daha iyi sonuç verdiğini buldu. Spa da duyguyla alınan bir hizmettir. Ancak 2018'deki bir tekrar çalışması bu sonucu doğrulayamadı. Kaynak: https://forrt.org/flora-replication-atlas/doi/10.1086/678484/
- **x99'un lehine en güçlü argüman.** "2.399" diyen birinin bu listeden geldiği anlaşılır, yani fiyatın kendisi kaynak izi olur. Ama K9'daki hazır mesaj ve kod bu işi marka bedeli ödemeden yapıyor.
- **Karar sahibi yine de isterse:** x99 yalnız tek seanslar grubunun beş satırına uygulansın ve beşine birden uygulansın. VIP (11.999 bir prestij ürününe elektronik mağazası görünümü verir), Çift ve paketler yuvarlak kalsın. "%20 İNDİRİM" etiketi yine doğru kalır (2.399 / 3.000 = %20,03 indirim).

**Rozet ve ilk ekran: rozet olmasın.**
- Kapakta büyütülmüş bir yüzde sayısı olmayacak. Rakamlar giriş cümlesinde aynı boyda yan yana duracak: "Tek seanslarda %20, paketlerde %30 indirim." Rozetin yerine tarih geliyor. Bu, dikkat çeken ve aynı zamanda dürüst olan tek "aciliyet" işareti.
- **"Tenisçilere özel" başlığı kalsın (Soru 9).** Grup üyesinin listenin kendisine yönelik olduğunu sohbet önizlemesinde anlaması bu kelimeye bağlı. 01C-20'den sonra "özel" kelimesini dürüst yapan şey kod değil, kuralın ilk ekranda yazılmasıdır.
- Kuralı olumlu ve tek satır olarak yazıyorum: "Tenisçi fiyatı için WhatsApp'tan yazmanız yeterli." Bu cümle "nasıl kanıtlarım" sorusunu cevaplıyor ve başka bir şart olmadığını söylüyor. "Belge istemiyoruz" demek de doğru olurdu. Ama "özel" başlığının hemen altında, kanalın açıklığını reklam eder gibi durur. Bu açıklama sohbette sorulursa söylenir.

**Koşul satırları: nereye, hangi boyda.** Sayfa uzamıyor, her satır 30-32 px'te (390 pt'de 10,8-11,6 pt):

| Koşul | Yer | Boy |
|---|---|---|
| Geçerlilik 31 Aralık 2026 | Başlığın üstündeki satır: tenis topu simgesi + "31 ARALIK 2026'YA KADAR GEÇERLİ"; altbilgide "Kasım 2026" yerine "Fiyatlar 31 Aralık 2026'ya kadar" | 30 px büyük harf, amber; altbilgi 28 px |
| Kanıt yok | Giriş metninin ikinci satırı: "Tenisçi fiyatı için WhatsApp'tan yazmanız yeterli." Altı çizili kısım wa.me bağlantısıdır, yani ilk ekranda ikinci bir CTA olur ve sayfayı uzatmaz | 32 px |
| Paket peşin, 1 yıl | Paket kartlarının hemen altındaki notun ilk cümlesi, koyu ve kalın: "Paketler peşin ödenir, 1 yıl içinde kullanılır." | 30 px |

**Son PDF için şart koştuğum düzeltmeler** (`index.html` üzerinden; sayfa genişliği 1.080 CSS px; hepsi `/tmp/claude-0/-home-user/d6383d34-f4c3-53e1-9fb3-44f29c9d2c31/scratchpad/tasarim/r2/proto2.html` içinde denendi):

1. **Rozet silinsin.** Satır 117-120'deki `.badge` bloğu kaldırılır, yerine bir şey konmaz. Kapakta hiçbir yüzde sayısı büyütülmez.
2. **Sıra şöyle olsun:** logo → tarih satırı → H1 → giriş metni → fotoğraf → listeler. `.hero` bloğu `.lead`'in altına taşınır. CSS: `.title{margin-top:34px;padding-right:0}`, `.hero{margin-top:36px}`, `.hero .photo{height:340px;border-radius:476px 476px 28px 28px / 220px 220px 28px 28px}`.
3. **Tarih satırı.** Tenis topu simgesi + "31 ARALIK 2026’YA KADAR GEÇERLİ". CSS: `.eyebrow{font-size:30px;letter-spacing:.14em}`. Karar sahibi 30 Aralık derse yalnız bu satır ve altbilgi değişir.
4. **Başlık.** H1 metni `Tenisçilere özel<br>spa fiyatları`. CSS: `h1{font-size:80px}`.
5. **Giriş metni (32 px, iki satır).** Birinci satır: "**Tek seanslarda %20, paketlerde %30 indirim.**" Satırın sonuna `<br>` konur. İkinci satır: "Tenisçi fiyatı için" ve ardından bağlantılı "WhatsApp’tan yazmanız yeterli." Bağlantı alt bölümdeki düğmeyle aynı wa.me adresine gider. CSS: `.lead{margin-top:18px}`, `.lead a{color:var(--amber);font-weight:600;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:6px}`. "Kortun yorgunluğunu hamamda, saunada ve masajda bırakın." cümlesi çıkarılır.
6. **Bölüm başlıkları.** "Masaj ve hamam / KİŞİ BAŞI" → "Tek seanslar / %20 İNDİRİM · KİŞİ BAŞI". "%30 İNDİRİMLİ" → "%30 İNDİRİM". "İKİ KİŞİ TOPLAM" aynen kalır. CSS: `.ghead span{font-size:30px;letter-spacing:.12em}`. Ölçtüm: üçü de tek satıra sığıyor.
7. **Derin Doku.** "KORTTAN SONRA" etiketi silinir. Açıklama "Boyun, omuz ve sırt; baskı tercihinize göre ayarlanır" olur (kaynak: `rituals.ts` 7). Tek satıra sığıyor.
8. **Paket kartları.** `.cnt` etiketleri silinir. Kart adları "10 seans İsveç", "20 seans İsveç", "10 seans Mix" ve "20 seans Mix" olur. CSS: `.pack .pname{margin-top:0}`, `.pack .unit{font-size:30px}`, `.old{font-size:28px}`. Paket fiyatları ve seans başı fiyatlar tam sayı kalır, x99 uygulanmaz.
9. **Paket notu (30 px).** Metin: "**Paketler peşin ödenir, 1 yıl içinde kullanılır.** Arkadaşınızla paylaşabilirsiniz. Mix’te her seansta İsveç, aromaterapi ya da derin doku seçersiniz." Kaynaklar: 01C-18, 01C-19; F3; 01A-3 (canlı `/spa`). CSS: `.pnote{font-size:30px}`, `.pnote b{color:var(--ink);font-weight:600}`.
10. **İki kişilik bölümü.** Çift Masajı satırında `.old` olmaz ve fiyat yalnız "4.000 TL" yazılır (01C-23). Açıklama "İki kişi birlikte; sauna, hamam ve havuz dahil" olur (kaynak: `rituals.ts` 8; böylece "çift odası" ifadesi de düşer). VIP satırı aynen kalır: üstü çizili 15.000, yeni fiyat 12.000 (01C-24).
11. **Dahil kutusu.** Üç satır şöyle olur: "Tek seans masajlarda hamam, sauna ve buhar odası dahil" / "Hamam kadın ve erkek için ayrı" / "Randevu için ön ödeme yok" (K3, K4; 01A-6, 01A-7).
12. **Alt bölüm.**
    - `.k` "RANDEVU" etiketi silinir.
    - CSS: `.cta{margin-top:0}`, `.cta .t1{font-size:30px}`, `.court{top:40px}`. Kort çizimi adres satırının altına taşmasın diye yukarı alınıyor.
    - CSS: `.brand .sub{font-size:26px}`, `.legal{font-size:28px}`.
    - Altbilgideki "Kasım 2026" → "Fiyatlar 31 Aralık 2026’ya kadar".
    - "Hafta içi 07.00–22.00 · Hafta sonu 08.00–22.00" satırı aynen kalır (01C-21).
13. **Kod.** Ölçüm kodu (K9) yalnız hazır mesajın içinde olur. PDF'te "kodu söyleyin" gibi bir satır basılmaz. 01C-20'ye göre bu cümle, işletmenin uygulamadığı bir şart gibi okunur.
14. **Göndermeden önce kontrol.**
    - Sayfa yüksekliği 3.540 CSS px'i geçmemeli.
    - 28 px'in altında önemli metin olmamalı.
    - 11 fiyat kalemi tek tek 01C'ye göre kontrol edilmeli: Çift 4.000 TL; diğer 10 kalem bugünkü PDF'teki gibi.
    - PDF'te iki wa.me bağlantısı olmalı (`strings` ile bakılır).
15. **Cihaz testi (yaklaşık 15 dakika).** Son PDF, PDF'in altındaki açıklama metniyle birlikte bir iPhone'a ve bir Android'e test sohbetinde gönderilir. Her telefonda üç ekran görüntüsü alınır:
    - sohbet balonundaki küçük resim;
    - dosya açılınca görünen ilk ekran;
    - üç bağlantıya dokunulunca ne olduğu (giriş metnindeki, düğmedeki ve açıklama metnindeki); hazır mesajın açılıp açılmadığına bakılır.
16. **README ve biçim.**
    - `README.md` güncel PDF'e göre yeniden yazılır: 11 kalem, koşullar, "%30 rozeti" ve "paketler eklenmedi" ifadelerinin kaldırılması.
    - `onizleme.jpg`'nin gruba gönderilecek bir biçim olmadığı yazılır.
    - Görsel isteyen bir yönetici olursa PDF'in **yerine** tek bir 4:5 kart gönderilir, yanına değil. Kart: 1.080 × 1.350 px; H1 en az 80 px; tarih ve oran satırları en az 44 px.

**Önerdiğim açıklama metni** (K8; köşeli parantezi pazarlama ve yönetici doldurur; fiyatlar PDF'teki fiyatlar):
> Navitas Spa & Sports Topkapı (DoubleTree by Hilton Topkapı, Bayrampaşa) tenisçilere özel fiyat listesi, 31 Aralık 2026'ya kadar:
> • Tek seans masajlarda %20 (İsveç masajı 50 dk 2.400 TL)
> • Masaj paketlerinde %30 (20'li İsveç 24.500 TL, seansı 1.225 TL)
> Tenisçi fiyatı için WhatsApp'tan yazmanız yeterli: [grup kodlu wa.me bağlantısı]. Ayrıntılı liste ekte.

## 2. Response to other members

| Member | Point | Agree / disagree | Why |
|---|---|---|---|
| tenisci | Tarih, kural ve bir fiyat, sohbet balonunda görünen üst alana girsin; rozetteki "varan" kalksın. | Agree | Prototipte ilk 565 px'te tarih, başlık, iki oran ve kural görünüyor (§1.3). Rozet tamamen kalkıyor. Bu, kartındaki 10 saniye testinin "nasıl kanıtlarım" ve "ne zamana kadar" kısımlarını ilk ekranda cevaplıyor. |
| tenisci | "Kanıt istemiyoruz" diye açık bir cümle yazılsın. | Kısmen disagree | "Tenisçi fiyatı için WhatsApp'tan yazmanız yeterli" aynı soruyu tek satırda cevaplıyor. "Yeterli" kelimesi başka bir şart olmadığını söylüyor, yani gizli koşul yok. Ama bu cümle "belge yok"u "özel" başlığının altında reklam etmiyor. Okur bunu sohbette sorarsa açıkça söylenir. |
| tenisci | "Çift odası" ifadesi iki arkadaşı caydırıyor; havuz bilgisi düşmüş. | Agree | Açıklama, kaynağın ifadesine döndü: "İki kişi birlikte; sauna, hamam ve havuz dahil" (`rituals.ts` 8). Tek satıra sığıyor. |
| grup-yoneticisi | "%30'a varan" broşür dilidir; ayrıca JPG atılmasın, tek mesaj olsun. | Agree, genişleterek | Aynı gerekçe x99 için de geçerli; 2.399 da broşür dilidir. Görsel kart yalnız PDF'in yerine gönderilir, yanına asla. |
| grup-yoneticisi | "Özel" sözünü dürüst kılmak için grup kodu ve doğrulama şart olsun. | Disagree (01C-20'den sonra) | İşletme fiyat için kod ya da kanıt istemiyor. Kodu PDF'te şart gibi basmak, masada uygulanmayan bir koşul yazmak olur. Bu, onburo'nun kırmızı çizgisi. "Özel"i dürüst kılan şey, kuralın ilk ekranda açıkça yazılması. Kod yalnız ölçüm için hazır mesajda durur. |
| pazarlama | Rozet "PAKETTE %30" olsun. | Disagree | Kapağın en büyük sayısı yine %30 olur. Altındaki ilk liste ise %20. 11 kalemin 6'sı %20, 4'ü %30, 1'i indirimsiz. Bu, kartımdaki "çelişkili vurgu" kırmızı çizgisi. Paket stratejikse dürüst kaldıraçlar şunlar: paket bölümünün kendi "%30 İNDİRİM" başlığı (30 px) ve açıklama metninde paket fiyatı. |
| pazarlama | İlk ekranda ikinci bir CTA olsun. | Agree, sıfır uzunlukla | Ayrı bir düğme yaklaşık 100 px ekler. Onun yerine giriş metnindeki "WhatsApp’tan yazmanız yeterli." ifadesi bağlantı yapıldı. Prototip PDF'te 2 wa.me annotation var. Bağlantıların çalışıp çalışmadığı cihaz testinde görülecek (madde 15). |
| pazarlama | PDF'te "Kendiniz yazar ya da ararsanız kodu söyleyin: TENIS" yazsın. | Disagree | 01C-20'den sonra bu cümle bir şart gibi okunur ve bir satır daha ekler. "Tenisçi fiyatı" ifadesi zaten ön büro için anahtar kelime görevi görüyor. Kod hazır mesajda kalsın. |
| tam-fiyat | Üstü çizili fiyat yerine "Liste fiyatı 3.000 TL" yazılsın. | Disagree (ölçtüm) | Bütün eski fiyatlar "Liste X TL" yapılınca sayfa +72 px uzuyor. Paket kartlarında eski fiyatın sağ kenarı 495-501 px'e, kartın iç sınırına (502 px) dayanıyor ve kartlar 228'den 264 px'e çıkıyor (`proto2_liste.html`). Üstelik işletme kendi Campus sayfasında da üstü çizili fiyat kullanmış (01B-14). Bu gösterimin yasal tarafı ayrıca profesyonele sorulmalı. |
| tam-fiyat | Bitiş tarihi üstte ve rozette olsun; rozet "Tenis grubu kodu ile" desin. | Kısmen agree | Tarih üstte: evet, sayfanın en üstündeki bilgi satırı o. Rozet ve "kodu ile" ifadesi: hayır. Kod fiyat için şart değil (01C-20) ve bu ifade sahte bir koşul olur. 20'li paket ve VIP itirazı tasarımla çözülecek bir şey değil. Bu koltuk o konuda ağırlık koymuyor. |
| onburo | İndirimsiz kalem varsa PDF'ten çıksın; kalem kalem istisna olmasın. | Kısmen disagree | Çift Masajı'nın 4.000 TL'si masada bir istisna yaratmıyor, çünkü herkese aynı fiyat. Üstü çizili fiyat olmadan yazıldığı için kimse 3.200 TL beklemez. "Bunda geçmez" gibi bir dipnot eklenmiyor; bu noktada onburo ile aynı yerdeyim. |
| onburo | "Ön ödeme yok" yalnız randevuya bağlansın; paket ödemesi yazılsın. | Agree | "Randevu için ön ödeme yok" dahil kutusunda duruyor. "Paketler peşin ödenir, 1 yıl içinde kullanılır" ise paket kartlarının hemen altında, kalın yazıyla. İki bilgi görsel olarak ayrı bloklarda. |
| isletme | Kırmızı çizgi: süresi ve sınırı belirsiz, herkese yayılan indirim. | Agree (tasarım payı) | Tarih iki yerde (30 ve 28 px), paket kullanım süresi paket fiyatlarının hemen altında yazılı. 20'li paketin maliyet itirazı ise bir tasarım sorusu değil. |

## 3. Corrections accepted or disputed

- **01A-2 (yayındaki sitede fiyat yok): kabul.** Sonucu: okur üstü çizili fiyatı sitede doğrulayamaz. Ben yine de üstü çizili gösterimi koruyorum. Gerekçeler: işletme liste fiyatı + oran gösterimini seçti (V16); "Liste X TL" etiketi ölçüldü ve sığmıyor (§2); Campus sayfası emsal (01B-14). Yasal gösterim şartı kurulun cevaplayacağı bir soru değil.
- **01A-3 ve 01B-15 (Mix üç masajla sınırlı): kabul.** Paket notuna canlı sitedeki ifade girdi. Repodaki "masaj türünü siz seçersiniz" cümlesi Spesiyal'i de kapsıyor gibi okunuyordu.
- **01A-4 (VIP kapsamı): kabul.** VIP açıklamasına kese köpük eklenmedi; `rituals.ts` 3'teki metin kaldı.
- **01A-5, 01B-16 ve 01C-21 (hafta sonu): kabul.** PDF'teki saat satırı doğru ve aynen kalıyor. Sitenin düzeltilmesi bu kurulun konusu değil.
- **01A-6 ve 01C-18, 01A-7, 01A-8: kabul.** Düzeltmeler 9-11 ve 7 bunlara dayanıyor.
- **01A-9 (README): kabul;** düzeltme 16.
- **01A-10 ve V74, V77 (ölçüler): kabul.** V77, Round 1 prototipindeki 26 px'lik "TL" birimlerini saymadığımı not etmişti. Doğru. Bu turda onları açıkça sayıyorum (§1.4). V75'in eklediği ikinci en düşük kontrast (5,09:1, koyu zeminde "WhatsApp'tan yazın") 30 px'e büyütmeyle daha da okunur oluyor. Bunu kabul ediyorum.
- **01B-14 (Campus): kabul.** Bu madde iki yönde kullanılıyor ve ikisini de açıkça yazıyorum: (a) işletme üstü çizili fiyat kullanmış; (b) işletme bir kez 9 ile biten bir fiyat (14.900) kullanmış. (b) x99'u desteklemiyor: o bir yüzler basamağı indirimiydi, bir üyelik ürünüydü ve sayfa bugün yayında değil.
- **01C-17, 19, 20, 23, 24: kabul;** ilk ekran, paket notu ve İki kişilik bölümü bunlara göre kuruldu. **01C-22:** bu koltuğun alanı dışında.
- İtiraz ettiğim bir düzeltme yok.

## 4. What would reverse this vote

- **Son PDF'te kapakta yine büyük bir yüzde rozeti olursa** ("%30'a varan", "PAKETTE %30" ya da niteleyici ekin sayının yarısından küçük yazıldığı herhangi bir biçim): bu koltuk o PDF'in gönderilmesini desteklemez. Rozet kalkana kadar bu sürüm için D. Hiçbir cihaz testi bu oranı kabul edilebilir yapamaz.
- **Geçerlilik tarihi ya da paket kuralı 28 px'in altına, örneğin alt bilgiye inerse,** ya da işletme sonradan bir saat veya gün kısıtı koyar ve bu kısıt aynı boyda ilk ekrana yazılmazsa: yazılana kadar D.
- **Cihaz testinde Android görüntüleyicisi sayfayı genişliğe değil bütün sayfaya sığdırırsa** (fiyatlar 9 pt'nin altına iner): oyum A'da kalır, ama birincil biçim değişir. Gruba 4:5 kart + açıklama metni gider, PDF istek üzerine gönderilir.
- **x99 benimsenirse** oy değişmez. Ama §5'teki karşı görüş kayda geçer.
- **Maliyet verisi 20'li paketin maliyetin altında kaldığını gösterirse:** bu koltuk tasarım açısından C'ye de, B'ye de itiraz etmez. Hangi kapsamda olursa olsun aynı düzeltme listesi uygulanır.

## 5. Dissent to record

**Oyda:** none.

**Karar x99'u ya da kapakta bir yüzde rozetini benimserse, bu koltuğun karşı görüşü şudur, zayıflatılmadan:**
- **x99.** Liste, gruba bir arkadaş tavsiyesi gibi girmeli ve spa kalitesinde görünmeli. x99 bu iki hedefin de karşısında duruyor:
  - Mağaza dilidir; grup yöneticisinin "broşür dili" itirazına doğrudan dokunur.
  - İşletmenin bütün fiyat geçmişi yuvarlaktır.
  - Marka yazı tipinde (Marcellus) 9 ve 3 rakamları satır çizgisinin altına sarkar. "2.399"da üç rakam sarkar, sayfanın en büyük öğesi olan fiyat sütunu düzensizleşir (ölçülü görüntü: `/tmp/claude-0/-home-user/d6383d34-f4c3-53e1-9fb3-44f29c9d2c31/scratchpad/tasarim/r2/x99_compare.png`).
  - Paketlerde uygulanamadığı için aynı sayfada üç fiyat sistemi oluşur.
  - Getirdiği tek şey, fiyatın kaynak izi olmasıdır. Hazır mesajdaki kod bunu marka bedeli ödemeden zaten yapıyor.
  - Psikolojik fiyatlama literatürü x99'u bu tür, duyguyla alınan bir hizmet için desteklemiyor; en fazla karışık.
- **Yüzde rozeti.** Kapaktaki en büyük sayı, altındaki ilk listede bulunmayan bir oran olursa, okur "%30" görür ve %20 bulur. Bu "yem" hissi şikâyet olarak değil, yazmamak olarak ortaya çıkar. Ölçümde de "tenisçiler ilgilenmedi" diye okunur; tasarımdan kaynaklandığı kimsenin aklına gelmez. Oranlar giriş cümlesinde ve bölüm başlıklarında aynı boyda durduğu sürece hiçbir şey kaybedilmez. Rozetin dikkat çekme işini, ilk ekrandaki tarih satırı dürüst olarak yapar.
