# Kapak, tur 1: H (sanat yönetmeni + görsel hassasiyet/okunurluk)

**A: 7,5/10 RED. B: 6,0/10 RED. Veto: yok.** Engelleyici olmayan bir hassasiyet uyarısı var (madde 4).

Ölçümler 1280×720'de yapıldı. Kod parametreleri `kapak.js`'deki 1920 uzayındadır.
- **Büyük harf yüksekliği:** A ve B'de 118 px, yani %16,4. Kural %18 (130 px). Koddaki "harf ≥ %18" yorumu doğru değil: Bebas'ta büyük harf ≈ 0,70 em, 250 px font %16,4 verir.
- **Parlaklık:** A'da en parlak nokta göz (L 243). Güneş L 225.
- **Güneş-zemin karşıtlığı:** 1,19:1; gri testinde güneş neredeyse kayboluyor.
- **Diğer karşıtlıklar:** yazı-zemin 8:1, göz-baş 9,9:1.

## Ne çalışıyor
- Üslup filmle tutarlı: düz opak mürekkep, şerit gökyüzü, kayık baskı.
- A'daki bakış çizgisi (göz → güneş) 168 px'te okunuyor: "güneşe bakan kanatlı genç".
- A'da yazı ile figür arasında 271 px boşluk var.
- B'nin yazısı filmdeki P47 geri çağrısıyla ("Unutulan uyarı buydu") birebir aynı.
- **Hassasiyet:** hale yok (baş güneşten ~620 px uzakta), haç pozu yok. Siluet ayrıntısız, çıplaklık okunmuyor. Uçurumda aşağı bakan figür yok. Mutlak iddia yok; iki uyarı Ovidius VIII 203–206'ya uyuyor. Melek okuması düşük, çünkü açık renkli çapraz kayış kanadın takma olduğunu söylüyor. Kayış korunmalı.

## Düzeltmeler (önem sırasıyla)
1. **Harf yüksekliği (A, B):** `kapakYazi` px 250 → 290. Böylece büyük harf ~135 px (%18,8) olur.
   - A: taban çizgileri 720 ve 981. Yazı 1280'de x 60–596, y ~345–654 arasına düşer; figürle arada ~200 px kalır.
   - B: aşağıdaki 6. maddeye bak.
2. **A'da kanat blok ya da pelerin gibi okunuyor.**
   - Neden: kanadın ucu kare dışında kalıyor (`span 1000, ang -.6`). Üst kenar düz bir tahta gibi, birincil tüylerin arası görünmüyor.
   - Tek "tüy" işareti alt saçak (x 1000–1180, y 560–660). O da rozet bölgesinde (x 960–1250, y 553–690); akış taklidinde rozetin altında kalıyor.
   - Çözüm: `span ≈ 620`, `ang ≈ -0,95`. Kanat yukarı ve sağa kalkar, uç (1160–1220, 150–220) kare içinde kalır.
   - En az 3 ayrık birincil tüy görünsün; araları zemin renginde ve ≥ 8 px olsun (üslup kapısındaki yakın plandaki gibi). Saçak y ≤ 520'de kalsın.
   - Gerekirse figür `x 1330 → 1250`.
3. **A'da değer sıralaması.** Güneş tek ve en parlak odak olmalı.
   - Güneşi somon şerit bandına taşı: `gunes(pr, 400, 150, 120, 2)`. 1280'de merkez (267,100) olur. Somon üstünde karşıtlık 1,8:1'e çıkar.
   - Dış halka y ≤ ~300'de kalır; bugün y ~375'te "İ" noktalarına neredeyse değiyor (x 130–260). Bu teğet de böylece kalkar.
   - Diski bir ton aç (~#FAF0CF).
   - Gözü kâğıt beyazı yerine `sky1` bejine (241,201,149) çevir. Göz-baş karşıtlığı 8:1 kalır, bakış yine okunur.
4. **A, hassasiyet (engelleyici değil).** Siyah siluet + bembeyaz badem göz + yuvarlak kıvırcık baş + öne çıkık açık ağız, kapak boyutunda ırkçı karikatür (minstrel) okumasına kapı aralıyor. İzleyicinin yaklaşık yarısı yurt dışından.
   - Çözüm: 3. maddedeki bej göz ve ağız çentiğini küçültmek ya da kapatmak. Ağız 168 px'te zaten okunmuyor, kayıp olmaz.
5. **B'de kanat yaprak, yüzgeç ya da balina kuyruğu gibi okunuyor** (168 px ve bulanıklık testi). İki açık yarık muz yaprağına benziyor. İnsan ve yüz yok; görselin vaadi yalnız "denizle ilgili unutulmuş bir şey", kimin olduğunu başlık söylüyor.
   - Çözüm: arka kenara A'daki pul sıraları ve 4–5 ayrık birincil tüy "parmağı" ekle.
   - Suyun üstüne 2–3 serbest tüy koy (x 600–900, y 560–600). Tüy İkaros'un en evrensel işaretidir.
   - Kanat kökünde kısa bir kayış parçası görünsün.
6. **B'de güneş yazıyla çakışıyor.** Diskin alt kenarı y ≈ 210'da; "UNUTULAN"ın harf üstü y 197'de, "UL" harflerine (x 1000–1080) değiyor. Odak yazıyla çakışık.
   - Çözüm: `gunes(pr, 1600, 140, 80, 2)`, yazı taban çizgileri 520 ve 781 (px 290).
   - 1280'de disk alt kenarı ~147, harf üstü ~211 olur. Yazının altı ile deniz arasında ≥ 30 px kalır. Halkalar harfleri kesmesin.
7. **Paketlemeye not (alanım dışı):**
   - A'nın yazısı başlığı tekrar ediyor ("İkaros'a İki Uyarı Yapıldı").
   - Başlıktaki "Herkes Birini Unuttu" mutlak iddiaya yakın; kırmızı çizgi 7 kapak için yazılmış, başlığa da bakılsın.

## En emin olmadığım nokta
4. madde: karikatür riski gerçek mi, aşırı okuma mı? Üslup kapısında aynı baş onaylandı ve 168 px'te bu ayrıntı görünmüyor. Yine de kapakta baş 1920'de ~225 px; önerilen düzeltme bedava ve 3. maddeyle aynı. İkinci belirsizlik: soluk güneş bilinçli bir afiş yumuşaklığı olarak savunulabilir. Ama gri testinde kaybolan bir odak kapakta taşıyıcı olamaz.
