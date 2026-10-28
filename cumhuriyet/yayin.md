# Yayın talimatı: 29 Ekim (uzun video + Shorts)

Bu dosya, yüklemeyi yapacak kişi içindir. Adımlar sırayla uygulanır ve bütün işlemler YouTube Studio'da (studio.youtube.com) yapılır.
YouTube'un kendi zamanlaması kullanıldığı için, yükleme bittikten sonra bilgisayarın açık kalması gerekmez.

## 0. Hazırlık: dosyaları bilgisayara al
Depo: `https://github.com/bercanay7/Animasyon-kahve-`. Dal: `claude/29-ekim-animation-video-hzh7dw` (main değil).

- **Depo bilgisayarda yoksa:**
  ```bash
  git clone -b claude/29-ekim-animation-video-hzh7dw https://github.com/bercanay7/Animasyon-kahve-.git
  ```
- **Depo zaten varsa:**
  ```bash
  git fetch origin claude/29-ekim-animation-video-hzh7dw
  git checkout claude/29-ekim-animation-video-hzh7dw
  git reset --hard origin/claude/29-ekim-animation-video-hzh7dw
  ```
- **Büyük dosyalar:** iki video depoda yoktur, sohbette dosya olarak gönderildi: `cumhuriyet_master.mp4` ve `cumhuriyet_shorts.mp4`. İkisini de `Animasyon-kahve-/cumhuriyet/` klasörüne koyun.
- **Kontrol:** `cumhuriyet/` klasöründe şunlar bulunmalı:
  - `cumhuriyet_master.mp4`
  - `cumhuriyet_shorts.mp4`
  - `kapak.jpg`
  - `kapak_b.jpg`
  - `cumhuriyet.tr.srt`
  - `youtube.md`

## Dosyalar
| Dosya | Ne için |
|---|---|
| `cumhuriyet_master.mp4` | Uzun video: 1920×1080, 6:18, Türkçe ses |
| `kapak.jpg` | Uzun videonun kapağı (1280×720) |
| `kapak_b.jpg` | İkinci kapak; YouTube'un "Test ve Karşılaştır" özelliği için |
| `cumhuriyet.tr.srt` | Türkçe altyazı |
| `cumhuriyet_shorts.mp4` | Shorts: 1080×1920, 43 sn; sonu başına dikişsiz bağlanır (döngü) |
| `youtube.md` | Başlık, açıklama (bölümler ve kaynaklar), etiketler |

## Zamanlama (Europe/Istanbul)
- **Uzun video:** 29 Ekim 2026 Perşembe, 10:00. Bayram sabahı, törenlerle aynı saatlerde.
- **Shorts:** 29 Ekim 2026 Perşembe, 19:23. Saat "1923"e göz kırpar. Uzun video o saatte yayında olacağı için Shorts ona bağlanabilir.

## 1. Uzun video
1. YouTube Studio'da **Oluştur → Video yükle** deyin ve `cumhuriyet_master.mp4` dosyasını seçin.
2. **Ayrıntılar** sekmesi:
   - **Başlık:** `Cumhuriyet'i Kuran Kuşak Nasıl Yetişti? | 29 Ekim`
   - **Açıklama:** `youtube.md` içindeki "Açıklama" bölümünün tamamı, bölüm zaman damgalarıyla birlikte. Damgalar YouTube'da bölüm çizgisi olarak görünür; ilk damganın 0:00 olması gerekir, öyle.
   - **Küçük resim:** `kapak.jpg`. Kanalda "Test ve Karşılaştır" açıksa ikinci kapak olarak `kapak_b.jpg` eklenir. YouTube kazananı izlenme süresi payına göre seçer; test sürerken başlığı değiştirmeyin.
   - **Kitle:** "Hayır, çocuklara özel değil".
   - **Daha fazla göster:**
     - Etiketler: `youtube.md` → Etiketler.
     - Video dili: Türkçe. Kategori: Eğitim.
     - "Değiştirilmiş veya yapay içerik" sorusu: **Hayır**. Video gerçekçi görüntü içermez; stilize, taş baskı üslubunda bir animasyondur. Anlatımın yapay zekâ sesi olduğu açıklamada zaten yazıyor.
3. **Video öğeleri:**
   - **Altyazı:** Altyazı ekle → Dosya yükle → "Zamanlamalı" → `cumhuriyet.tr.srt`.
   - **Bitiş ekranı:** son 13 saniye (6:05–6:18). Videoda sağ yarıda "SIRADAKİ HİKÂYE" etiketi ve aşağı ok, en altta "ZAMAN KURYESİ'NE ABONE OL" yazısı var. Öğeler bunlara göre yerleştirilir:
     - **Video öğesi** ("İzleyiciye en uygun video"; kanaldaki iki video konu olarak uzak olduğu için bu seçenek daha iyi): okun hemen altına, ekranın sağ yarısının ortasına (üst kenarı ekran yüksekliğinin yaklaşık %24'ü, yatayda sağ yarının ortası).
     - **Abone ol öğesi:** video öğesinin altına, "ABONE OL" yazısının hemen üstüne (yatayda aynı hizada, dikeyde ekranın yaklaşık %80'i).
     - Önizlemede öğeler sol yarıdaki afişin ve bayrağın üstüne binmemeli.
4. **Görünürlük:** Planla → 29.10.2026, 10:00 (GMT+3) → **Planla**.

## 2. Shorts
1. **Oluştur → Video yükle** deyin ve `cumhuriyet_shorts.mp4` dosyasını seçin. Dikey ve 60 saniyeden kısa olduğu için YouTube bunu otomatik olarak Shorts sayar.
2. **Ayrıntılar:**
   - **Başlık:** `“Yarın Cumhuriyet ilan edeceğiz!” O sofradakiler nerede yetişti? #shorts`
   - **Açıklama:**
     ```
     Cumhuriyet'i kuran kadro, bir gün karşısına dikilecekleri sultanın okullarında yetişti. Tam hikâye: 6 dakikalık video.

     #29Ekim #CumhuriyetBayramı #Atatürk #tarih #shorts
     ```
   - **Etiketler:** 29 Ekim, Cumhuriyet Bayramı, Atatürk, Mustafa Kemal, İsmet İnönü, Cumhuriyet'in ilanı, Türk tarihi, shorts
   - **Kitle:** çocuklara özel değil. **Kategori:** Eğitim.
3. **İlgili video:** uzun video ("Cumhuriyet'i Kuran Kuşak Nasıl Yetişti?"). Planlanmış videolar da listede görünür. Görünmüyorsa, uzun video 10:00'da yayına girdikten sonra eklenir.
4. **Görünürlük:** Planla → 29.10.2026, 19:23 (GMT+3).

## 3. Yayından sonra
- **Uzun videonun altına sabit yorum:** `Sizin hayatınızda iz bırakan öğretmen kimdi? Adını ve size ne kattığını yazın 👇 Cumhuriyetimizin 103. yılı kutlu olsun.`
- **Shorts'un altına sabit yorum:** `Tam hikâye (6 dk): <uzun videonun bağlantısı>`. Bağlantı, uzun video 10:00'da yayına girince kopyalanır.
- İlk 24 saatte yorumlara yanıt vermek, videonun önerilere girmesine yardım eder. Öğretmen hikâyelerine kısa bir teşekkür yeterli.
