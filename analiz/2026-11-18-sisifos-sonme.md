# Sisifos'un gösterim eğrisi ve kanalın "kapısı" (18 Kasım 2026)

**Soru (kullanıcı):** Kafka kanalın en iyi tutmasını aldı, TO da medyanın üstünde; buna rağmen geniş kitle testi gelmedi. YouTube yapay zekâ videolarını geri plana mı atıyor?
**Veri:** Studio → Sisifos → Küçük resim gösterimleri, 28 gün (21 Ekim – 17 Kasım), kullanıcının ekran görüntüsü. Toplam 230.594 (Önerilen 128,5 B, Göz atma 98,1 B, oynatma listeleri 1,7 B, kanal sayfaları 1,5 B, arama 588). Günlük değerler grafikten piksel ölçümüyle okundu; toplamları Studio'nun toplamıyla ±%5 tutuyor.

## Günlük gösterim (B = bin)
| Tarih | 24 Eki | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 1 Kas | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B | 1,8 | 11,8 | 7,0 | 5,9 | 8,3 | 18,3 | 22,2 | 21,6 | 7,9 | 6,1 | 9,8 | 26,9 | 19,1 | 10,6 | 13,3 | 13,7 | 5,9 | 9,0 | 6,5 | 5,7 | 3,5 | 3,6 | 2,4 | 1,3 |
(17 Kasım ≈0,5 B, muhtemelen yarım gün.)

## Okuma
- **Yapay zekâ cezası yok:**
  - Politika ya da ceza belli bir günde uçurum gibi görünür. Burada 8 Kasım'dan beri ~3 günde bir yarılanan düzgün bir sönme var: dört dalgadan sonra kitlesini tüketen videonun tipik eğrisi.
  - Düşüş, yayınların sıklaştığı 12 Kasım'dan önce başladı.
  - YouTube'un yazılı politikası da yapay zekâ etiketinin erişimi etkilemediğini söylüyor; "özgün olmayan içerik" kuralı şablon seri üretimle ve para kazanmayla ilgili.
- **Kanalın motoru Sisifos'tu.** Yeni videonun yayın günü Sisifos'un günlük gösterimi ile o videonun ertesi günkü göz atma testi:

| Yeni video | Yayın | O gün Sisifos | Sonuç |
|---|---|---|---|
| Abdülhamid | 29 Ekim | ~18 B | 2. gün 7,0 B test |
| Prometheus | 31 Ekim | ~22 B | 2. gün 17,6 B test |
| Medici | 5 Kasım | ~19 B | test yok (tutma %31, zayıf) |
| Milton | 12 Kasım | 5,7 B | büyük test yok |
| İkaros | 14 Kasım | 3,6 B | büyük test yok |
| Kafka | 16 Kasım | 1,3 B | büyük test yok (tutma kanalın en iyisi) |

- Dalga alanlar Sisifos tepedeyken yayımlananlar; Sisifos söndükçe yeni videoların testi küçüldü.
- İlişki, kanıt değil (n küçük). Mantığı: YouTube yeni videoyu önce kanalı izlemiş kişilere gösterir; o kişilerin çoğu Sisifos'tan geldi.

## Sonuç ve öneriler
1. **Yeni kapı gerekli.** Sonraki videoda talep kontrolünün iki şartı Sisifos kadar güçlü olmalı: (a) Türk izleyicinin bildiği ve aradığı ad, (b) izleyicinin kendi hayatına soru. Yeni izleyici getiren bir video sonrakileri de besler.
2. **Yayın aralığı en az 5–7 gün** (deneme). Zayıf akış dört videoya bölünmez. Shorts uzun videodan birkaç gün sonra.
3. Sisifos → Kafka bağlantısı yapılır, ama etkisi sınırlı (Sisifos günde ~1–2 B gösterimde).
4. Sınama: bir sonraki geniş kapılı video 2. gün göz atma testi alırsa ve ardından gelen video (≥5 gün sonra) da test alırsa açıklama güçlenir.
