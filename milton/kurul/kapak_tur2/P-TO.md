# Kapak kurulu, tur 2: P-TO (tıklama oranı ve paketleme stratejisti)

Çapraz eleştiri ve yeniden değerlendirme. Ölçütler ve ağırlıklar tur 1 ile aynıdır:

| # | Ölçüt | Ağırlık |
|---|---|---|
| 1 | Anlaşılırlık | %25 |
| 2 | Merak | %20 |
| 3 | Vaat ve tutma | %20 |
| 4 | Ayrışma | %15 |
| 5 | Kelime | %10 |
| 6 | Rozet, yazı ve odak | %10 |

Eşik 9,0; hiçbir ölçüt 7'nin altında olamaz. Koordinatlar 1280×720 kapak düzlemindedir.

**Baktıklarım:**
- `kapak_a.jpg`, `kapak_a_sade.jpg`, `kapak_b.jpg`, `kapak_b_vektor.jpg`, `kapak_b_gurur.jpg`
- `tur7b/yanyana168.png`, `tur7b/test/akis_koyu.jpg`, `tur7b/test/akis_acik.jpg`
- `goz/ozet.jpg`
- `milton.tr.srt` (ilk 60 sn)
- P-Sanat tur 1 raporu

## 0. İddiaların doğrulanması (PIL ile kendi ölçümüm)

| İddia | Ölçtüğüm | Sonuç |
|---|---|---|
| A: alev en parlak yer (%5'lik dilim 225) | Alev bölgesinde %95'lik dilim 229. Karede ≥230 olan 634 pikselin **hepsi** alevin çekirdeğinde (x 997–1036, y 369–400). Alev dışı %99,9'luk dilim 202. Sol zemin ortalaması 188. | Doğru |
| A: bulutlar kalktı, çerçeve var, yazı siyah | Görsel olarak doğru. Yazı x 0–819'a kadar ölçülüyor, çünkü çerçeve de dahil oluyor. | Doğru |
| A: yazı boyu | "B" harfi y 220–352 = 133 px (%18,5) | Eşik geçildi |
| A: künye | "MILTON · KAYIP CENNET", harf yüksekliği ≈ 27 px. 168 px'te ≈ 3,5 px: okunmuyor, gri bir leke. | Bilgi notu |
| B: yazı "PİŞMAN MIYDI?" | "P" harfi y 155–290 = 136 px (%18,9). Yazı x 802–1240 aralığında. | Doğru |
| B: damla en parlak (parlama 255, ortalama 223) | Damla bölgesinde %99'luk dilim 254, damla y 460–652. Ama karede ≥235 olan 1.187 pikselin **467'si damlanın dışında**: yüzün kâğıt beyazında, x 311–756 ve y 61–470 arasına yayılmış. Yüz beyazının %99'luk dilimi 227, yazınınki 212. | Kısmen doğru: damla en parlak nokta, ama tek parlak alan değil |
| B: pul kenarı ve sargı kalktı | Doğru. Ancak yüzün sağ kenarında yeni bir "tarak / bozuk ekran" kenarı var: x 600–760, y 60–470. Yatay çizgiler x 756'ya kadar uzanıyor, yazıya 46 px kalıyor. | Kısmen |
| B: rozet bölgesi | Ortalama 19,9, sapma 0,8: boş | Doğru |
| Film: 10. saniyede göz ve damla planı | `ozet.jpg`'de 9,9 ile 11,35 sn arasında Cabanel gözü var. Damla **beyaz ve küçük**; kadraj kapağınkinden geniş (kollar görünüyor). Altyazıya göre bu sırada "…cennetin en parlak meleğiydi" (6,2–10,3 sn) biterken "Birazdan cehennemden kaçacak" (11,3 sn) başlıyor. | Plan var, ama 0–5 sn kuralının dışında (aşağıya bak) |

**Yeni bulgu (doğrulanmalı):** elimdeki filmin açılış karesi (`nif_is/kanca5/t0004.60.png`, saat 17:28) eski figürü gösteriyor: kel, yumurta baş, dimdik duruş. Kapak A ise 18:11'de yeni figürle (kıvırcık saç, eğik baş, kambur) yeniden çizildi.
- Film güncellenmediyse kapak ile ilk 5 saniye artık aynı figürü göstermiyor.
- Sahne, ışık ve alev aynı olduğu için yanıltma değil, ama vaat eşleşmesi zayıflıyor.
- `lib/figur.js` içinde bir güncelleme olabilir. Son render'ı görmedim.

---

## 1. Çapraz eleştiri: P-Sanat tur 1 raporu

### Katıldıklarım
- **A, piktogram figür.** Tur 1'de "heykel ya da manken gibi, duygu yok" demiştim. Sanat yönetmeni bunu çizim düzeyinde (sabit kontur, kel yumurta baş, boyun dikdörtgeni) daha isabetli koydu. Yeni çizim bu sorunun çoğunu kapatıyor.
- **A, alevin alt bloğu "el, pençe, mangal" gibi okunuyor.** Bunu **gözden kaçırmıştım**. Ben alevi yalnız parlaklık ve boyut olarak ölçtüm, biçim okumasına bakmadım. Haklı bir bulgu ve düzeltildi. Yeni alev 168 px'te "göğüste yanan kor" gibi okunuyor.
- **A, "Kutsal Kalp" ikonografisine yakınlık.** Bunu da **gözden kaçırmıştım**. Haklı bir hassasiyet notu. Yeni çizimde eller görünmüyor ve "sunma" jesti yok. Önden duruş, göğüste ışık ve arkada ışınlar düzeni kalıyor, ama kara kanat ve kambur siluetle risk bence düşük.
- **B, iris jant kapağı gibi ve yüz kenarı tarak gibi.** Katılıyorum.
  - İris düzeltilmiş: ışınsal vuruşlar ve kare bir pencere yansıması var.
  - Tarak kenar yeni sürümde de duruyor (x 600–760, y 60–470). 168 px'lik akışta "bozuk görüntü" gibi okunuyor. Tur 1'deki "bozuk ekran" bulgumla aynı yerde birleşiyoruz.
- **B, damlanın vektör dili gravürle çatışıyor.** Tam boyda katılıyorum.

### Katılmadıklarım
- **Damlayı %35 küçültmek** (P-Sanat B-1: yükseklik 300'den 195 px'e). Katılmıyorum.
  - Gerekçe: 168×94'te damla, kapağın tek renkli ve tek "olay" öğesi. 195 px, 168'de ≈ 25 px yükseklik demek; 120×68'de ≈ 18 px'e iner ve kanca zayıflar.
  - Mevcut sürümde damla y 460–652 (≈ 190 px), ayrıca ince bir iz var. Bence doğru boyda; daha fazla küçültülmemeli.
- **B'ye kimlik için "Cabanel bukleleri" eklemek** (P-Sanat B-5). Amaca katılıyorum, uygulamaya katılmıyorum.
  - Mevcut sol üst bukleler (x 0–240, y 0–120) 168'de "siyah top dizisi" gibi okunuyor. Kimlik kurmuyor, dikkat dağıtıyor.
  - "Kimin gözü?" sorusunu kapakta çizimle çözmeye gerek yok: başlık 1'deki "Şeytan" kelimesi bunu taşıyor. Ya buklelerin saç olduğu okunsun (tutam halinde, kenar ışıklı), ya kaldırılsın.
- **"Emoji damlanın tıklama getirebileceği konusunda stratejistin görüşü ağır basabilir."** Görüşüm: **burada bir takas yok.**
  - `yanyana168.png`'de gravür damla ile vektör damla 168 px'te ayırt edilemiyor.
  - Akış boyunda tıklamayı getiren şey damlanın **rengi, boyutu, konumu ve parlaklık farkı**; işlenişi (gradyan, oval parlama) değil.
  - İşleniş yalnız tam boyda, yani TV, masaüstü ve video sayfası gibi büyük görünümlerde fark ediliyor. Orada gravür dili, filmle tutarlılık ve "ucuz değil" algısı kazandırıyor. İzleyicinin %22'si TV'den izliyor.
  - Bu yüzden **gravür damla** seçilmeli. Vektör sürümün TO avantajı olduğuna dair bir işaret görmüyorum.
  - Tek koşul: gravürleştirme damlanın rengini ve parlaklık farkını azaltmasın. Ölçüm: damla %99'luk dilim 254, iyi.

### P-Sanat raporunda eksik bulduklarım
- **Akış bağlamı yok.** Koyu temada B'nin siyah zemini akışın zeminiyle birleşiyor; açık temada A'nın sepyası beyaz zeminle. A'nın çerçevesi ikincisini çözdü. Rapor yalnız "küçük boy okunurluk" ölçtü, rakip kapaklar arasındaki ayrışmayı ölçmedi.
- **Vaat ve açılış eşleşmesi.** B'nin vaadinin finalde karşılandığı sorunu ele alınmadı. A'nın figürü yeniden çizildiğinde filmin açılış figürünün de güncellenmesi gerektiği yazılmadı. Bu, yeni çizimin doğurduğu bir risk.
- **Yazı ile başlığın ilişkisi.** Kapak yazısının başlığı tekrar edip etmediği ele alınmadı.
- **B'de yüz beyazı ile damlanın yarışı.** Raporda var (yüz beyazı ≥245). Bu turda yazı 212'ye inmiş, ama yüz beyazı hâlâ 227 ve ≥235 piksellerin %39'u damla dışında.

---

## 2. Puanlar (tur 1 ile yan yana)

### Kapak A: "“BEN CEHENNEMİM” / MILTON · KAYIP CENNET"

| Ölçüt | Tur 1 | Tur 2 | Gerekçe |
|---|---|---|---|
| 1 Anlaşılırlık | 8,5 | **9,0** | 168'de yazı ve "kara kanatlı figür, göğsünde kor" ilk bakışta okunuyor. Tırnak işareti bunun "bir karakterin sözü" olduğunu gösteriyor. Künye 168'de okunmuyor, ama zarar da vermiyor. |
| 2 Merak | 8,0 | **8,5** | Başlık 1 ("…Neden Kaçamadı?") soruyor, kapak cevabın ipucunu veriyor. Açılıştaki 17. saniye sorusu "Onu orada tutan ne?" bu soru-cevabı birebir taşıyor. İddia cümlesi olduğu için tavan 8,5–9. |
| 3 Vaat ve tutma | 9,5 | **9,0** | Sahne, ışık ve alev açılışla aynı. Ama yeni figür filmin açılışındaki (elimdeki) figürden farklı (0. bölüme bak). |
| 4 Ayrışma | 7,5 | **8,5** | 7 px çerçeve açık temada kenarı geri getirdi (`tur7b/akis_acik.jpg`). Zemin karartılınca kapak renkli rakiplerin arasında biraz "çamurlu bej" kaldı. |
| 5 Kelime | 8,0 | **8,5** | Tırnak işareti ve künye "kanal Şeytan adına konuşuyor" okumasını kaldırıyor. Yanlış okuma yok. |
| 6 Rozet, yazı, odak | 7,5 | **9,0** | Yazı %18,5. Alev tek ve en parlak odak (≥230 piksellerin tamamı alevde). Rozet bölgesinde yazı yok. |
| **Ağırlıklı** | 8,3 | **8,8** | 2,25 + 1,70 + 1,80 + 1,28 + 0,85 + 0,90 |

**Karar: A 8,8, RED, ama eşiğe çok yakın.** Hiçbir ölçüt 7'nin altında değil. Aşağıdaki A-1 ve A-2 düzeltmeleriyle 9,0+ olur.

### Kapak B: "PİŞMAN MIYDI?" (gravür damla)

| Ölçüt | Tur 1 | Tur 2 | Gerekçe |
|---|---|---|---|
| 1 Anlaşılırlık | 7,5 | **8,5** | Büyük göz, damla ve soru 120 px'te bile okunuyor. Kalan kusurlar: sağ kenardaki tarak/bozuk görüntü etkisi ve sol üstteki siyah toplar. "Kimin gözü?" sorusunu başlık çözüyor. |
| 2 Merak | 8,5 | **8,5** | Gözyaşı ile "pişman mıydı?" uyumlu ve kendi içinde bir hikâye kuruyor; geçmiş zaman da bir anlatı vaat ediyor. Başlık 1 ile iki soru yan yana ama aynı damarda (kaçamadı / pişman mı). |
| 3 Vaat ve tutma | **6,0** | **7,5** | Göz ve damla planı artık 9,9–11,35 sn'de. Ama kanal kuralı 0–5 sn. Filmdeki damla beyaz ve küçük, kapaktaki mavi ve büyük. "Pişmanlık" teması sözle ancak Nifates'te (≈ 10:56) açılıyor. Büyük ölçüde düzeldi, tam değil. |
| 4 Ayrışma | 8,0 | **8,5** | Açık temada güçlü. Koyu temada zemin akışla birleşiyor, ama büyük açık yüz ve mavi damla bunu kurtarıyor. A'dan net biçimde farklı. |
| 5 Kelime | **6,0** | **9,0** | Vaaz kalıbıyla çakışma kalktı. "Pişman mıydı?" nötr ve edebi; finaldeki soruyla aynı. |
| 6 Rozet, yazı, odak | 7,5 | **8,0** | Yazı %18,9, rozet bölgesi boş. Damla en parlak nokta, ama yüz beyazı (227; ≥235 piksellerin %39'u) onunla yarışıyor. |
| **Ağırlıklı** | 7,3 | **8,3** | 2,13 + 1,70 + 1,50 + 1,28 + 0,90 + 0,80 |

**Karar: B 8,3, RED.** Hiçbir ölçüt 7'nin altında değil. Darboğaz vaat (7,5).

---

## 3. Tur 1 bulgularının durumu

| # | Tur 1 bulgusu | Durum |
|---|---|---|
| A-1 | Alev tek ve en parlak odak olsun | **Kapandı.** ≥230 pikseller yalnız alevde. |
| A-2 | Hale ve zemin ≈ %10 koyu | **Kapandı.** Biraz fazla bile: zemin "çamurlu" duruyor (A-2 düzeltmesine bak). |
| A-3 | Köşe bulutları kaldırılsın | **Kapandı.** |
| A-4 | Açık tema için çerçeve | **Kapandı** (7 px). |
| A-5 | Figüre duygu (eğik baş, göğsü kavrama) | **Kısmen.** Baş eğik, omuz kambur; tam boyda iyi. 168'de baş "topuz saçlı" bir siluet gibi okunuyor, eğim zor seçiliyor. Eşik için zorunlu değil. |
| A-6 | Yazı siyah kalsın | **Kapandı.** |
| A-7 | Yazı ≈ %4 büyüsün | **Kapandı** (133 px, %18,5). |
| B-1 | "ŞEYTAN AĞLADI" değişsin ("PİŞMAN MIYDI?") | **Kapandı.** |
| B-2 | Pul kenarı kırılsın | **Kapandı**, ama yerine **tarak/bozuk ekran kenarı** geldi (x 600–760, y 60–470). Yeni bulgu olarak açık. |
| B-3 | Göz büyüsün, sargı bandı kalksın | **Kapandı.** |
| B-4 | Gözyaşı en parlak, yazı ≈ #CFC7B8 | **Kısmen.** Yazı 212, damla tepe 254. Yüz beyazı 227, ≥235 piksellerin %39'u damla dışında. |
| B-5 | İlk 5 sn'de vaat (ara kesme) | **Kısmen.** Plan 9,9 sn'de, 0–5 sn'de değil; damla beyaz ve küçük. |
| — | Başlık tutarsızlığı (akışta "İç Yolculuğu") | **Kapandı.** Akışta başlık 1 kullanılıyor. |

---

## 4. Kalan sıralı düzeltmeler (yalnız 9'a taşıyacak olanlar)

### A (8,8 → 9,0+)
1. **Filmin açılış figürünü kapakla eşleştir** (ya da eşleştiğini kanıtla). A01 açılış planındaki figür yeni kapak figürüyle aynı olsun: kıvırcık baş, eğik boyun, kambur omuz, üç dilli alev.
   - Film güncellenmişse t = 4,6 sn karesini kurula göster; bulgu kapanır.
   - Kazanç: vaat 9,0'dan 9,5'e.
   - Önerim filmi güncellemek; P-Sanat'ın figür eleştirisi filmdeki aynı figür için de geçerli.
2. **Zemini biraz aç.** Sol zemin ortalaması 188'den ≈ 198'e ve ışın alanına çıksın:
   - Bölge: x 0–820, y 0–720 ve hale çevresi x 820–1280.
   - Alev dışı tepe parlaklık ≤ 210 kalsın, böylece alev (229+) yine tek en parlak yer olur.

   Kazanç: renkli akışta "çamurlu bej" görüntüsü gider, ayrışma 8,5'ten 9,0'a çıkar.
3. **(İsteğe bağlı)** Künyeyi ≈ 34 px harf yüksekliğine çıkar, x 50–680 ve y 560–600 aralığında kalsın. Böylece 246 px'lik ana sayfa boyunda okunur. Puanı etkilemiyor; künyeyi kaldırmayın, hassasiyet üyesinin isteği.

### B (8,3 → 9,0)
1. **Göz ve damla planını ilk 5–7 saniyeye çek.** Planı 9,9 sn'den, "Bunu söyleyen, bir zamanlar cennetin en parlak meleğiydi" cümlesinin başına (≈ 6,3 sn) taşı. Bu kurgu kararı başkanın.
   - Cümle bu planla anlam olarak da örtüşüyor: "söyleyen" = bu göz.
   - Filmdeki damla planda bir kare için kapaktaki gibi açık maviye dönsün, ya da kapaktaki damla beyaza çekilsin. Kapak ile film aynı damlayı göstermeli.
   - Kazanç: vaat 7,5'ten ≈ 8,5'e.
2. **Yüzün sağ kenarını sakinleştir** (x 600–760, y 60–470).
   - Yatay çizgiler en fazla x 680'de, düzensiz boylarda sivrilerek karanlığa erisin.
   - Tarak gibi düz bir dikey sınır kalmasın.
   - Yazıya en az 100 px boşluk kalsın.

   Kazanç: 168'deki "bozuk görüntü" okuması gider, anlaşılırlık 8,5'ten 9,0'a çıkar.
3. **Yüz beyazını ≈ 215 tepeye indir** (x 0–660, y 0–520). ≥235 piksellerin ≥ %90'ı damlada kalsın. Yazı 212 kalabilir.
   - Kazanç: odak 8,0'dan 9,0'a.
4. **Sol üstteki siyah topları ya saç tutamı olarak okunur yap ya da kaldır** (x 0–240, y 0–120). 168'de "boncuk dizisi" gibi duruyorlar; bir "tespih" okuması da tamamen dışlanamaz.

Tahminim: B'nin 1–3 numaralı düzeltmeleriyle B ≈ 9,0 olur. Düzeltme 1 yapılmazsa B en fazla ≈ 8,6'ya çıkar.

---

## 5. Ana sürüm seçimleri

- **A tırnaklı mı, sade mi:** **tırnaklı.**
  - 168'de iki sürüm neredeyse aynı okunuyor (`yanyana168.png`). TO farkı ihmal edilebilir.
  - Tırnak ve künye, bunun bir karakterin sözü olduğunu ve edebi bir okuma olduğunu söylüyor. Hassasiyet alanının isteği estetik ya da TO tercihiyle geçersiz kılınmaz.
- **B gravür damla mı, vektör mü:** **gravür.** 168'de fark yok. Tam boyda ve TV'de gravür daha tutarlı ve daha "kaliteli" okunuyor (gerekçesi 1. bölümde).
- **"PİŞMAN MIYDI?" mı, "GURUR MU?" mu:** **"PİŞMAN MIYDI?"**
  - "GURUR MU?" tek başına belirsiz.
  - Türkçede gözyaşı ile "gurur" birleşince ilk çağrışım **"gurur gözyaşları"**: mezuniyet, milli maç, gururlanan anne baba. Yani tam ters bir duygu.
  - "Gurur" sorusunun anlamı ancak "pişmanlık mı?" ile birlikte kuruluyor ("GURUR MU, PİŞMANLIK MI?"), bu da küçük boy için uzun.
  - "PİŞMAN MIYDI?" gözyaşıyla uyumlu ve geçmiş zamanıyla bir hikâye vaat ediyor.
- **Başlık:** **1. aday, `Kayıp Cennet: Şeytan Cehennemden Neden Kaçamadı? | Milton`**
  - Açılışın 17. saniyesindeki soru "Onu orada tutan ne?". Başlık, video ve kanca aynı soruyu soruyor. Kanalın "merak sorusunu ilk cümlede sor, cevabı sona sakla" dersine birebir uyuyor.
  - **Hassasiyet üyesinin 2. aday tercihini tarttım.** 2. aday ("Milton'ın Şeytanı: "Ben Cehennemim" | Kayıp Cennet") A'nın kapak yazısını kelimesi kelimesine tekrar ediyor. A ile eşleşince merak boşluğu kapanıyor; akışta aynı cümleyi iki kez görmek tıklama için boşa harcanmış bir yer. Hassasiyet üyesi üç adayı da uygun buldu; 2. adayı yalnız "en güvenli" saydı, veto etmedi.
  - 1. adayın güvenlik açısı: "Kayıp Cennet:" ile başlıyor, yani bir kitap çerçevesi kuruyor. Kapak A'da tırnak ve künye var. Açıklama ve sabit yorum "edebi okuma" diyor.
  - Bu yüzden 1. adayı öneriyorum. Başkan 2. adayı seçerse test sırası değişmeli: o durumda B ana kapak, A ikinci seçenek olmalı. Çünkü 2. başlık B ile tekrar etmiyor, tamamlıyor.
- **Test planı ("Test ve karşılaştır", başlık sabit):**
  1. **A (tırnaklı)**: ana kapak, yükleme anında bu konur.
  2. **B (gravür, "PİŞMAN MIYDI?")**: yalnız B'nin 1. düzeltmesi (açılışta göz planı) yapılırsa. Yapılmazsa B testten çıkar ve 2–3 gün sonra paketleme yenilemesi için yedekte kalır.

  İki seçenek yeterli. Vektör damla, "GURUR MU?" ve sade A teste girmesin: bunlar ayrı fikir değil, aynı fikrin varyantı. Örneklemi bölüp sonucu geciktirirler.

---

## 6. En emin olmadığım nokta
1. **Filmin açılış figürü güncellendi mi?** Elimdeki tek kare (17:28) kapaktan (18:11) eski. `lib/figur.js` güncellenmiş olabilir; doğrulamadım. A'nın 9,0'a çıkması büyük ölçüde buna bağlı.
2. **B'nin vaadi 10. saniyede karşılanınca tutma ne kadar zarar görür?** Kanalın verisi kaybın 10–15. saniyede olduğunu söylüyor. 9,9 sn bu pencerenin hemen başında; 6,3 sn'ye çekmek bence anlamlı bir fark. Ama bunu yalnız test ölçer.
3. **Başlık.** Başlık 1 ile 2 arasındaki tercihte hassasiyet alanının görüşü "en güvenli", ama bir veto değil. Başkan bunu veto olarak okursa test sırasını yukarıdaki gibi çevirmek gerekir.
