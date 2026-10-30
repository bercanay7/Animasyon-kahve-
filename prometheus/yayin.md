# Yayın talimatı: Prometheus (uzun video + Shorts)

Adımlar sırayla uygulanır ve hepsi YouTube Studio'da (studio.youtube.com) yapılır. Zamanlamayı YouTube yaptığı için yükleme bittikten sonra bilgisayarın açık kalması gerekmez.

## 0. Hazırlık: dosyaları bilgisayara al
- **Depo:** `https://github.com/bercanay7/Animasyon-kahve-`
- **Dal:** `claude/prometheus-story-video-uvblhl` (main değil)

Depo bilgisayarda yoksa:
```bash
git clone -b claude/prometheus-story-video-uvblhl https://github.com/bercanay7/Animasyon-kahve-.git
```

Depo varsa:
```bash
git fetch origin claude/prometheus-story-video-uvblhl
git checkout claude/prometheus-story-video-uvblhl
git pull
```

**Depoda olmayan dosyalar:**
- Uzun film ve Shorts büyük olduğu için depoya girmez; ikisi sohbette dosya olarak gönderilir. İndirip `Animasyon-kahve-/prometheus/` klasörüne koy.
- Uzun filmin yüklenecek dosyası `prometheus_youtube.mp4`.
  - Neden: ana kayıt (`prometheus_master.mp4`, H.264, 1,03 GB) sohbetin 500 MB dosya sınırını aşıyor.
  - Yüklenecek dosya aynı filmin H.265 (HEVC) kodlaması, yaklaşık 400 MB.
  - Görüntü ana kayda neredeyse birebir eşit (SSIM 0,991); ses aynı, yeniden kodlanmadı.
  - YouTube HEVC kabul eder.

## Dosyalar
| Dosya | Ne için |
|---|---|
| `prometheus_youtube.mp4` | Uzun video, 1920×1080, 30 fps, 23:55, Türkçe ses (HEVC, ≈ 400 MB) |
| `kapak.jpg` | Kapak A (1280×720) |
| `kapak_b.jpg` | Kapak B: "Test ve karşılaştır" için ikinci kapak |
| `prometheus.tr.srt` | Türkçe altyazı (izleyicilerin %38'i Türkçe altyazıyla izliyor) |
| `prometheus_shorts.mp4` | Shorts, 1080×1920, 54 sn: "Asıl tutsak kim?" (doruk kesiti) |
| `youtube.md` | Başlık, açıklama (bölüm zaman damgaları ve kaynaklarla), etiketler |

## Zamanlama (Europe/Istanbul)
| Ne | Zaman | Neden |
|---|---|---|
| Uzun video | Cumartesi 20:00 | Sisifos'un açıldığı gün ve saat |
| Shorts | Ertesi gün (pazar) 18:00 | Uzun video yayında olur, Shorts ona bağlanabilir |

## 1. Uzun video
1. **Oluştur → Video yükle** → `prometheus_youtube.mp4`.
2. **Ayrıntılar:**
   - **Başlık:** `Prometheus: Asıl Tutsak Kimdi? | Aiskhylos ve Azra Erhat` (iki kapak için ortak). "Test ve karşılaştır" sürerken başlık değiştirilmez.
   - **Açıklama:** `youtube.md` → "Açıklama" bölümünün tamamı. Bölüm zaman damgaları ve kaynak künyesi dahil.
   - **Küçük resim:** `kapak.jpg`. "Test ve karşılaştır" açıksa `kapak_b.jpg` ikinci seçenek olarak eklenir. YouTube kazananı izlenme süresi payına göre seçer.
   - **Kitle:** "Hayır, çocuklara özel değil".
   - **Daha fazla göster:**
     - Etiketler: `youtube.md` → Etiketler.
     - Video dili: Türkçe. Kategori: Eğitim.
     - "Değiştirilmiş veya yapay içerik" sorusu: **Hayır**. Video gerçekçi görüntü içermez; stilize, kodla çizilmiş vazo resmi animasyonudur. Açıklamada anlatımın ElevenLabs sesiyle yapıldığı zaten yazıyor.
3. **Video öğeleri:**
   - Altyazı ekle → Dosya yükle → "Zamanlamalı" → `prometheus.tr.srt`.
   - Bitiş ekranı: son 20 saniye (23:35–23:55). Filmde iki çerçeve çizildi:
     - solda video öğesi için: x 150–870, y 180–585. "Belirli video" olarak Sisifos seçilir; kanalın en güçlü videosu, kitlesi aynı.
     - sağda abone öğesi için: x 1250–1650, y 230–630.
4. **Görünürlük:** Planla → cumartesi 20:00 (GMT+3) → **Planla**.

## 2. Shorts
1. **Oluştur → Video yükle** → `prometheus_shorts.mp4`. Dikey ve 60 saniyeden kısa olduğu için YouTube bunu Shorts sayar.
2. **Ayrıntılar:**
   - **Başlık:** `Asıl tutsak Zeus muydu? Prometheus #shorts`
   - **Açıklama:**
     ```
     Zincirdeki Prometheus mu tutsak, yoksa onu zincire vuran Zeus mu?
     Azra Erhat'ın 1967'de yazdığı önsözdeki şaşırtıcı cevap. Tam hikâye kanalda.

     #Prometheus #AzraErhat #Aiskhylos #YunanMitolojisi #shorts
     ```
   - **Etiketler:** Prometheus, Zeus, Azra Erhat, Aiskhylos, Zincire Vurulmuş Prometheus, Yunan mitolojisi, mitoloji, felsefe, özgürlük, shorts
   - **Kitle:** çocuklara özel değil. **Kategori:** Eğitim.
3. **İlgili video:** uzun video (Prometheus). Planlanmış videolar listede görünür; görünmüyorsa uzun video yayınlandıktan sonra eklenir.
4. **Görünürlük:** Planla → pazar 18:00 (GMT+3).

## 3. Yayından sonra
- **Uzun videonun altına sabit yorum:** `Bedelini bile bile, o ateşi yine de verir miydin? Yorumlarda yaz 👇`
- **Shorts'un altına sabit yorum:** `Tam hikâye (24 dk, 13 bölüm): <uzun videonun bağlantısı>`
- **Oynatma listesi:** uzun video "Mitler ve Felsefe" listesine eklenir. Liste yoksa oluşturulur; Orfeus ve Sisifos da aynı listeye girer.
- **İlk 48 saatte bakılacaklar:**
  - Gösterim tıklama oranı.
  - 0:30'da kalan izleyici oranı; hedef ≥ %63, Sisifos'un oranı.
  - Ortalama izlenme süresi.
  - "Test ve karşılaştır" sonucu.
