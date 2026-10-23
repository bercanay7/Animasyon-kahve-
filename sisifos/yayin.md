# Yayın talimatı: Sisifos (uzun video + Shorts + İngilizce ses)

Bu dosya, yüklemeyi yapacak kişi ya da bilgisayarda Chrome eklentisiyle çalışan Claude oturumu içindir. Adımlar sırayla uygulanır. Bütün işlemler YouTube Studio'da (studio.youtube.com) yapılır.
YouTube'un kendi zamanlaması kullanıldığı için yükleme bittikten sonra bilgisayarın açık kalması gerekmez.

## Dosyalar
| Dosya | Ne için |
|---|---|
| `sisifos_master.mp4` (yoksa `sisifos.mp4`) | Uzun video, 1920×1080, Türkçe ses |
| `kapak.png` | Uzun videonun kapağı (1280×720) |
| `sisifos.tr.srt` | Türkçe altyazı |
| `audio/mix_en.wav` (ya da `sisifos_en.m4a`) | İngilizce dublaj ses kanalı (görüntüyle aynı süre) |
| `en/sisifos.en.srt` | İngilizce altyazı |
| `en/youtube_en.md` | İngilizce başlık / açıklama / etiketler |
| `sisifos_shorts.mp4` | Shorts, 1080×1920, 42,7 sn |
| `youtube.md` | Türkçe başlık, açıklama (bölümler + kaynaklar), etiketler |

## Zamanlama (Europe/Istanbul)
- **Uzun video:** 24 Ekim 2026 Cumartesi, 20:00
- **Shorts:** 25 Ekim 2026 Pazar, 18:00 (uzun video yayında olduktan sonra, ona bağlanabilsin diye)

## 1. Uzun video
1. YouTube Studio'da **Oluştur → Video yükle** ile `sisifos_master.mp4` dosyasını seçin.
2. **Ayrıntılar** sekmesi:
   - Başlık: `Sisifos: Ölümü Zincirleyen Adam Neden Mutlu? | Camus ve Absürt`
   - Açıklama: `youtube.md` içindeki "Açıklama" bölümünün tamamı (bölüm zaman damgaları dahil).
   - Küçük resim: `kapak.png`.
   - Kitle: "Hayır, çocuklara özel değil".
   - Daha fazla göster:
     - Etiketler: `youtube.md` → Etiketler.
     - Video dili: Türkçe. Kategori: Eğitim.
     - Altyazı sertifikası: gerekmez.
     - "Değiştirilmiş veya yapay içerik" sorusu: **Hayır**. Video gerçekçi görüntü içermez, stilize animasyondur. Anlatım yapay zekâ sesiyle yapıldıysa ve kanal bunu belirtmeyi tercih ediyorsa açıklamaya bir satır eklenebilir.
3. **Video öğeleri:**
   - Altyazı ekle → Dosya yükle → "Zamanlamalı" → `sisifos.tr.srt`.
   - Bitiş ekranı: son 14 saniye (6:51–7:05). Sağ yarı boş bırakıldı; "Abone ol" ve "En yeni video" öğeleri oraya konur.
4. **Görünürlük:** Planla → 24.10.2026, 20:00 (GMT+3) → **Planla**.

## 2. İngilizce dublaj (aynı videoya ikinci ses kanalı)
Yükleme işlendikten sonra videonun sayfasında: **Altyazılar** (Languages) → **Dil ekle** → İngilizce.
- **Ses** sütunu → Ekle → `audio/mix_en.wav` (ya da `sisifos_en.m4a`) → Yayınla.
  - Ses kanalının süresi videoyla aynıdır (424,9 sn); kaydırma gerekmez.
  - Çoklu ses kanalı özelliği kanalda açık değilse bu satır görünmez. Bu durumda `sisifos_en.mp4` ayrı bir İngilizce video olarak yüklenebilir (aynı adımlar, `en/youtube_en.md` metinleriyle).
- **Başlık ve açıklama** sütunu → Ekle → `en/youtube_en.md` içindeki başlık ve açıklama.
- **Altyazılar** sütunu → Ekle → `en/sisifos.en.srt`.

## 3. Shorts
1. **Oluştur → Video yükle** → `sisifos_shorts.mp4`. Dikey ve 60 saniyeden kısa olduğu için YouTube bunu otomatik olarak Shorts sayar.
2. Ayrıntılar:
   - Başlık: `Ölümü zincire vuran adam: Sisifos #shorts`
   - Açıklama:
     ```
     Tanrıları iki kez kandırdı, Ölümü zincire vurdu… ve cezası sonsuza dek bir kayayı itmek oldu.
     Camus neden "Sisifos'u mutlu hayal etmeliyiz" dedi? Tam hikâye kanalda.

     #Sisifos #Camus #YunanMitolojisi #mitoloji #shorts
     ```
   - Etiketler: Sisifos, Sisyphus, Camus, Yunan mitolojisi, mitoloji, absürt, felsefe, shorts
   - Kitle: çocuklara özel değil. Kategori: Eğitim.
3. **İlgili video:** uzun video (Sisifos: Ölümü Zincirleyen Adam…). Uzun video yayında değilse de planlanmış videolar listede görünür; görünmüyorsa uzun video yayınlandıktan sonra eklenir.
4. **Görünürlük:** Planla → 25.10.2026, 18:00 (GMT+3).

## 4. Yayından sonra
- Uzun videonun altına sabit yorum: `Senin kayan ne? Hepimizin her sabah ittiği bir kaya var. Seninkini yaz 👇`
- Shorts'un altına sabit yorum: `Tam hikâye (7 dk): <uzun videonun bağlantısı>`
