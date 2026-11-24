# Dil denemesi: İngilizce ve İspanyolca paket (17 Kasım 2026)

**Soru:** Türkçe anlatımlı videolara çevrilmiş başlık, açıklama ve altyazı eklemek yabancı izleyici getiriyor mu?
**Neden şimdi:** İngilizce altyazı payı her videoda %1'in altında. Ama videoların yabancı dilde başlığı yok; YouTube onları yabancı izleyiciye hiç göstermiyor. Düşük pay ilgisizlik değil, görünmezlik de olabilir. YouTube Yardım: çevrilmiş başlık ve açıklama o dili konuşan izleyiciye kendi dilinde gösterilir ve o dildeki aramada çıkar.

## Ne eklendi
| Video | Dil | Dosyalar |
|---|---|---|
| Sisifos | İngilizce (Ekim'den beri hazır; yüklü olup olmadığı Studio'dan teyit edilecek) | `sisifos/en/youtube_en.md`, `sisifos/en/sisifos.en.srt` (zamanları İngilizce dublaja göre; Türkçe sesle ~0,5 sn kayabilir) |
| Sisifos | İspanyolca | `sisifos/es/youtube_es.md`, `sisifos/es/sisifos.es.srt` |
| Ran | İngilizce | `ran/dil/youtube_en.md`, `ran/dil/ran.en.srt` |
| Ran | İspanyolca | `ran/dil/youtube_es.md`, `ran/dil/ran.es.srt` |

Altyazılar Türkçe altyazının zamanlarıyla birebir aynı ve `araclar/altyazi/denetle.py` ile denetlendi (zaman, satır uzunluğu ≤ 42, okuma hızı ≤ 17 kr/sn hedefi). Her açıklamanın ilk satırı anlatımın Türkçe olduğunu söyler; izleyici yanıltılmaz.

## Studio'da adımlar (bilgisayardan)
1. **İçerik** → videoyu seç → sol menüde **Altyazılar**.
2. **Dil ekle** → İngilizce (sonra İspanyolca).
3. Dilin satırında **Başlık ve açıklama** → Ekle → `youtube_xx.md` dosyasından başlığı ve açıklamayı yapıştır → Yayınla.
4. Aynı satırda **Altyazılar** → Ekle → **Dosya yükle** → "Zamanlamayla" → `.srt` dosyasını seç → Yayınla.
5. **Otomatik dublaj denetimi:** YouTube Türkçe videoları kendiliğinden İngilizce seslendirebiliyor (yalnız Türkçe → İngilizce; ses Emrullah olmaz). Videonun **Diller** sayfasında İngilizce "Ses" sütununda otomatik dublaj görünüyorsa dinlemeden yayımda bırakma. Yeni videolar için: Studio uygulamasında Ayarlar → İçerik → Otomatik dublaj → **Elle yayımla**.

## Ölçüm planı
- **Taban (17 Kasım, `2026-11-17-studio-verileri.md`):**
  - Sisifos: Türkiye %86,7, Azerbaycan %4,3, Almanya %1,7. Altyazı: Türkçe %31,4, İngilizce %0,8.
  - Ran: yayın 17 Kasım 18:00. 7. gün (24 Kasım): Türkiye %77,0; altyazı yok %54,8, Türkçe %44,1, İngilizce %0,4 (paketin yüklenip yüklenmediği henüz bilinmiyor).
  - Kafka (kontrol, 48. saat): Türkiye %75,4; altyazı yok %59,9, Türkçe %22,5, İngilizce görünmüyor.
- **Kontrol videoları:**
  - Ran'ı aynı yaştaki **Kafka** ile karşılaştır; Kafka'ya çeviri eklenmez.
  - Sisifos'u kendi önceki 14 günüyle karşılaştır.
- **Durum (24 Kasım):** paket yüklenmedi (kullanıcı). Deneme askıda; dosyalar hazır. Yüklenirse tarih buraya yazılır ve 14. güne hatırlatıcı kurulur. Ran'ın 7. gün kitlesi (yüklemesiz) taban olarak duruyor.
- **Bakış günü:** yüklemeden 14 gün sonra (yükleme tarihi: ____).
  - Studio → Analytics → Kitle: coğrafya ve altyazı dili.
  - Analytics → Erişim: arama terimleri; İngilizce ya da İspanyolca aramalar var mı?
- **Başarı ölçütü (önceden yazıldı):**
  - Türkiye dışı izlenme payı en az 5 puan artar, **ya da** İngilizce + İspanyolca altyazı payı izlenmelerin %3'ünü geçer;
  - **ve** bu izleyicilerin ortalama izleme süresi kanal medyanının (%39,8) yarısından düşük değildir.
  - Sağlanırsa paket her videonun yayın hazırlığına eklenir; sağlanmazsa bırakılır ve sonuç buraya yazılır.

## Sonuç
(14 gün sonra doldurulacak.)
