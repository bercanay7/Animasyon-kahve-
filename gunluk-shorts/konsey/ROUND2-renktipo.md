# ROUND 2: Renk ve tipografi uzmanı (renktipo)

**Read:** ROUND1-TALLY.md, every ADDENDUM-01*, and all Round 1 reports.

**Vote:** C
**Changed from round 1:** no (Tur 1'de "hibrit, çekirdek tipografi" demiştim; tally B ile C'yi ayırdı, ben C'yi seçiyorum)
**Confidence:** medium

## 1. Vote and reason

C, çünkü kapı ancak zaman tamponu varsa işler. B'de "bugün yaz, bugün yayınla" baskısı ilk atılan kontrolü okunabilirlik bakışı yapar; pipeline ve qc'nin uyarısı bu. C'nin 3 günlük tamponu ve ilk 14 günde en çok 2 cilt kuralı, yeni palet başına doğrulamam gereken zemin sayısını sınırlar.

Yeni kanıt (ilk_kareler_kanit.png üzerinde bu oturumda ölçtüm; kare 270×480 yani 1/4 ölçek, boyutlar gözle ve Pillow ile kabaca, Titanik karesi levhada yok):
- Üç videoda üç ayrı altyazı biçimi var. Dans: koyu yazı, krem etiket, ~64 px. Emu: koyu yazı, açık zemin, ortalı. Zanzibar: beyaz yazı, ince koyu kontur, sola yaslı ve daha küçük (~40–48 px). Bu, "cilt başına altyazı" modelinin bugün zaten işlediğinin kanıtı.
- HUD yazıları (DANSÇI 1, MERMİ 9.860, 00:00) en küçük metin; gözle ~32–40 px, yani 44 px hedefimin altında olabilir (tahmin).
- Zanzibar'da beyaz yazı alt gradyan zemine karşı kontursuz ~2,9:1, sarı vurgu ("38") ~2,0:1 ölçtüm (tek nokta örnek). Konturla okunuyor, ama kontrast kontura bağımlı, ölçüm de bunu saymıyor.
- Dans ve Emu altyazısı y≈1270–1400; "alt %25" (y≥1440) kuralından geçer, benim R1'deki 672 px alt şeridine (y≥1248) girer. Hangisinin doğru olduğu bilinmiyor.

## 2. Response to other members

| Member | Point | Agree / disagree | Why |
|---|---|---|---|
| analitik | 14 gün her şey donsun, cilt de | Kısmen hayır | Yazı katmanını bugün dondurmak benim talebim; ama 2 ciltli, kayda geçen rotasyon ölçümü bozmaz diyorum. Haklı olduğu yer: cilt ile kanca tipi aynı hafta değişirse karışır. Kabul: cilt günlüğe yazılır, kanca testi sırasında rotasyon konu eşlemesine bağlı sabit. |
| kanca | Kanca ≤9 kelime, ≥64 px | Evet, sayı ayarıyla | 960 px kullanılabilir genişlikte 64 px kalın yazı ≈ 27 karakter/satır (glif genişliği varsayımı), yani 9 kelime = 3 satır. Bu sınırda. ≤8 kelime ve ≤3 satır öneriyorum. |
| retention | İlk karede ≤4 kelime | Evet (yönde), hayır (sayıda) | Titanik'in 8 kelimelik kartı 1 sn'de okunmaz, haklı. Ama 4 kelime hem sesle hem yazıyla aynı vaadi taşımaya yetmeyebilir; 6 kelime + 2 satır tavanı. |
| qc | Kanca ≥48 px | Hayır | 48 px 1/4 ölçekte ~12 px; telefonda hızlı kaydırmada zayıf. Kanca ≥64, altyazı ≥56. Kontrast ve güvenli alanı insan kapısına bırakma, otomatik yaz: 0 dk. |
| artdir | "≥40 px" ve tek imza vurgu rengi | Kısmen | 40 px dosyanın sayısıydı; benim önerim 56. İmza vurgu rengi fikri doğru, ama Zanzibar'ın sarısı açık/orta zeminde ~2:1; vurgu rengi her cilt zemininde ≥3:1 geçmeli ya da koyu plaka şart. |
| pipeline | Tavan 4 cilt | Hayır | Her cilt = ayrı kontrast ve glif doğrulaması. Tavan 3, ilk 14 gün 2. |
| dil | `.upper()` yasak | Evet | Aynı hata ekranda "TITANIK" üretir; benim kırmızı çizgim. Glif test dizesi QA'ya girer. |

## 3. Corrections accepted or disputed

- **Ek madde 10 (HUD y≈260, üst/sağ güvenli alan açık):** kabul. Kaynaklar çelişiyor; yeni olgu iddiası getirmiyorum, ama yukarıdaki levhada HUD kutusu y≈220–300 aralığında: üst arayüz bölgesine girme olasılığı gerçek.
- **Ek madde 3:** kabul; levha bunu doğruluyor (Dans ilk karede kanca yok, Emu skor tabelası, Zanzibar saat). Levhada Titanik yok; onun için sonucu iddia etmiyorum.
- **Ek madde 5:** etkilenmem yok; ölçüm kısıtı sesle ilgili.

## 4. What would reverse this vote

- Bir Shorts (listelenmemiş test videosu) üzerinde telefon arayüzü ızgarasıyla ölçülür ve mevcut yerleşim (HUD y≈260, altyazı y≈1270–1400) çakışmazsa: 672/290 px şartım düşer; yine C.
- Kullanıcı 14 gün 2 ciltten fazlasını veya kapı atlamayı istiyorsa ve okunabilirlik kuralları "öneri"ye inerse A'ya (dondur ve ölç) oy veririm: tek cilt, tek tipografi en azından doğrulanması en ucuz olandır.
- 12 kareden ≥11'i şablon çakışması ve 2 sn okuma testini geçerse altyazı şartımı 56'dan 48 px'e gevşetirim.

## 5. Dissent to record

Oy azınlıkta değil. Kayıt altına alınacak koşullu itiraz: kanal anayasası okunabilirlik ve güvenli alan kurallarını "öneri" yapar veya ölçümsüz bırakırsa karşıyım. Anayasaya girecek sayılar (Bölüm 1 soruları):

- **Cilt tavanı:** 3; ilk 14 gün 2.
- **Sıklık ve süre:** C'nin haftada 5; metin boyutu süre için küçülmez, kelime sayısı azalır. Her ekran yazısı ≥ karakter sayısı/14 sn + 0,3 sn kalır (motion'ın 12–14 karakter/sn varsayımına dayanır, ölçülmedi).
- **Kapı (otomatik, 0 dk):** altyazı ≥56 px, HUD ≥44 px; kontrast ≥4,5:1 (yazı kutusu arkası pikselde ölçülür; kontur sayılmaz); "İSTANBUL ışığı ığ ş ç ö ü" glif testi; önemli yazı arayüzden temiz bölgede. Elle 1 dk: telefonda tam parlaklık bakışı.
- **Kanca kuralı:** kare 0'da, ≥64 px, ≤8 kelime, ≤3 satır, kontrast ≥4,5:1, güvenli bölgede.
- **Ölçüt:** 12 karenin ≥11'i çakışmasız ve 2 sn'de ≥%90 okunur.
- **Ucuz adım:** listelenmemiş 1 test Shorts + telefon ekran görüntüsü, ~1 saat.
