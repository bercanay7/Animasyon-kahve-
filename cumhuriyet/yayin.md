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
| `cumhuriyet_master.mp4` | Uzun video: 1920×1080, 6:19, Türkçe ses |
| `kapak.jpg` | Uzun videonun kapağı (1280×720) |
| `kapak_b.jpg` | İkinci kapak; YouTube'un "Test ve Karşılaştır" özelliği için |
| `cumhuriyet.tr.srt` | Türkçe altyazı |
| `cumhuriyet_shorts.mp4` | Shorts: 1080×1920, 43 sn; sonu başına dikişsiz bağlanır (döngü). Mobil uygulamada Shorts kapağı olarak 0:00 karesi seçilebilir (Mustafa Kemal ve "YARIN CUMHURİYET İLAN EDECEĞİZ!") |
| `youtube.md` | Başlık, açıklama (bölümler ve kaynaklar), etiketler |

## Zamanlama (Europe/Istanbul)
- **Uzun video:** 29 Ekim 2026 Perşembe, 10:00. Bayram sabahı, törenlerle aynı saatlerde.
- **Shorts:** 29 Ekim 2026 Perşembe, 19:23. Saat "1923"e göz kırpar. Uzun video o saatte yayında olacağı için Shorts ona bağlanabilir.

## 1. Uzun video
1. YouTube Studio'da **Oluştur → Video yükle** deyin ve `cumhuriyet_master.mp4` dosyasını seçin.
2. **Ayrıntılar** sekmesi:
   - **Başlık:** `Cumhuriyet'i Kuran Kuşak Nasıl Yetişti? | 29 Ekim`
   - **Açıklama:** `youtube.md` içindeki "Açıklama" bölümünün tamamı, bölüm zaman damgalarıyla birlikte. Damgalar YouTube'da bölüm çizgisi olarak görünür; ilk damganın 0:00 olması gerekir, öyle.
   - **Küçük resim, "Test ve karşılaştır":**
     1. Küçük resim bölümünde **Test ve karşılaştır** seçilir.
     2. Önce `kapak.jpg`, sonra `kapak_b.jpg` yüklenir.
     3. **Bitti** denir.
     - Test, video yayına girince başlar ve birkaç gün (en çok iki hafta) sürer. YouTube kazananı izlenme süresi payına göre seçer; sonuç belirsizse ilk yüklenen kapak (`kapak.jpg`) kalır.
     - Test sürerken başlığı ve kapağı elle değiştirmeyin.
     - Seçenek görünmüyorsa: YouTube Studio → Ayarlar → Kanal → Özelliklere uygunluk bölümünden gelişmiş özellikler açılır (telefon doğrulaması). Açılamazsa yalnız `kapak.jpg` yüklenir.
   - **Kitle:** "Hayır, çocuklara özel değil".
   - **Daha fazla göster:**
     - Etiketler: `youtube.md` → Etiketler.
     - Video dili: Türkçe. Kategori: Eğitim.
     - "Değiştirilmiş veya yapay içerik" sorusu: **Hayır**. Video gerçekçi görüntü içermez; stilize, taş baskı üslubunda bir animasyondur. Anlatımın yapay zekâ sesi olduğu açıklamada zaten yazıyor.
3. **Video öğeleri:**
   - **Altyazı:** Altyazı ekle → Dosya yükle → "Zamanlamalı" → `cumhuriyet.tr.srt`.
   - **Bitiş ekranı:** başlangıç **6:07**, bitiş 6:19 (12 saniye). Daha erken başlarsa öğeler son kartın ("103. YIL KUTLU OLSUN") üstüne biner. Videoda sağ yarıda "SIRADAKİ HİKÂYE" etiketi ve aşağı ok, en altta "ZAMAN KURYESİ'NE ABONE OL" yazısı var. Öğeler bunlara değmeyecek biçimde yerleştirilir:
     - **Video öğesi:** "İzleyiciye en uygun video" seçilir; kanaldaki iki video konu olarak uzak olduğu için bu seçenek daha iyidir. Okun altına konur:
       - üst kenarı ekran yüksekliğinin en az **%28**'i (ok %20–26 arasında);
       - yatay ortası ekran genişliğinin **%74**'ü.
     - **Abone ol öğesi:** ortası yatayda %74, dikeyde yaklaşık **%77**. Alt kenarı ekran yüksekliğinin **%87**'sini geçmesin; "ABONE OL" yazısı %90–92'dedir.
     - Önizlemede öğeler sol yarıdaki afişe (ekranın sol %46'sı) binmemeli.
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
3. **İlgili video (zorunlu):** uzun video ("Cumhuriyet'i Kuran Kuşak Nasıl Yetişti?").
   - Shorts'un sonunda ekranda "TAM HİKÂYE · 6 DAKİKALIK VİDEO · AŞAĞIDA" yazıyor. Bu bağlantı yoksa çağrı boşa düşer.
   - Planlanmış videolar listede görünürse yüklerken bağlanır.
   - Görünmezse uzun video 10:00'da yayına girdikten sonra, **19:00'dan önce** Shorts'un ayrıntılarından bağlanır.
   - 19:00'a kadar bağlanamazsa Shorts'un yayın saati, bağlanana dek ertelenir.
4. **Görünürlük:** Planla → 29.10.2026, 19:23 (GMT+3).

## 3. Yayından sonra: saatli kontrol listesi
**29 Ekim, 10:00'dan sonra**
- [ ] Video herkese açık.
- [ ] Oynatıcıda bölüm çizgileri görünüyor (0:33, 1:34, 2:43, 3:19, 4:22, 5:11).
- [ ] Bitiş ekranı 6:07'de açılıyor; öğeler oka, "ABONE OL" yazısına ve afişe binmiyor.
- [ ] Altyazı (Türkçe) seçilebiliyor.
- [ ] "Test ve karşılaştır" başlamış görünüyor (Analytics → küçük resim testi).
- [ ] Uzun videonun altına sabit yorum yazıldı ve sabitlendi:
  `Sizin hayatınızda iz bırakan öğretmen kimdi? Adını ve size ne kattığını yazın 👇 Cumhuriyetimizin 103. yılı kutlu olsun.`

**19:00'dan önce**
- [ ] Shorts'un "İlgili video" alanı uzun videoya bağlı (2. bölüm, 3. adım).

**19:23'ten sonra (Shorts yayına girince)**
- [ ] Shorts'un altına sabit yorum yazıldı ve sabitlendi:
  `Tam hikâye 6 dakikalık videoda: ekrandaki ▶ bağlantıya dokunun.`
  Shorts yorumlarındaki ve açıklamasındaki bağlantılar tıklanmaz (YouTube 2023'te kapattı); izleyiciyi uzun videoya "İlgili video" bağlantısı götürür.

**Yorum denetimi (ilk 72 saat)**
- YouTube Studio → Ayarlar → Topluluk → Varsayılanlar → Kanalınızdaki yorumlar: uygunsuz olabilecek yorumları incelemeye alma seçeneği açılır ve **daha katı** ayar seçilir. İngilizce arayüzde: "Hold potentially inappropriate comments for review" → "Increase strictness".
- Bekleyen yorumlar günde birkaç kez gözden geçirilir. Bayram günü ve B kapağındaki "Sultan" vurgusu tartışma çekebilir.
- Atatürk'e hakaret içeren yorumlar (5816 sayılı Kanun) yayımlanmaz, kanalda bırakılmaz.
- İlk 24 saatte yorumlara yanıt vermek videonun önerilere girmesine yardım eder. Öğretmen hikâyelerine kısa bir teşekkür yeterli.
