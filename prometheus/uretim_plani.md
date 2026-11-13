# Prometheus: üretim planı ve kurul düzeni

Organizatör ve son karar: ana oturum (Claude). Kurullar öneri verir; öneriler tek tek tartılır, yalnız işi iyileştirenler uygulanır. Reddedilenler gerekçesiyle kayda geçer (`kurul/kararlar.md`).

## İlke: kurul büyüklüğü kararın geri dönüş maliyetine göre
- **Büyük kurul** (çok üyeli, iki turlu: bağımsız değerlendirme → çapraz tartışma): geri dönmesi pahalı kararlarda kullanılır. Bunlar senaryo, görsel dil, animatik ve kapaktır.
- **Hızlı ikili inceleme** (aynı ölçütle iki bağımsız gözden geçirici): sahne sahne ilerleyen yinelemeli işlerde kullanılır. Bunlar bölüm animasyonları, ses miksi ve Shorts'tur.
- Her uzmanlıkta en az iki üye bulunur ve birbirinden bağımsız çalışır. İkinci turda bütün raporları okur, birbirini eleştirir.
- Sonraki turlarda aynı ölçütler korunur. Önceki turun dosyalarının üzerine yazılmaz, her tur yeni adla kaydedilir.

## Puanlama
- Her aşamanın 1–10 arası ölçütleri ve ağırlıkları vardır. Ağırlıklı ortalama **≥ 9,0 = ONAY**.
- Bir ölçüt 7'nin altındaysa ortalama ne olursa olsun RED.
- Puan tablosu her turda `kurul/` altında saklanır ve kullanıcıya özetlenir.

## Aşamalar
| # | Aşama | İnceleme | Ölçütler (ağırlık) |
|---|---|---|---|
| 1 | **Senaryo** | Büyük kurul: 6 uzmanlık × 2 üye, 2 tur. Bunlar dramaturgi, anlatım üslubu (Zweig / Dostoyevski), kaynak sadakati (Erhat / klasik metin), izleyici stratejisi (tutma / paketleme), dil (metin / ses) ve görsel yönetmenlik. Ardından değişiklikleri doğrulayan kısa bir tur yapılır (kaynak + dramaturgi). | K1 kaynak sadakati %20 · K2 açılış %15 · K3 yapı %15 · K4 tempo %15 · K5 psikolojik derinlik ve üslup %15 · K6 dil ve seslendirilebilirlik %10 · K7 görselleştirilebilirlik %10 |
| 2 | **Seslendirme** | Okunuş denemesi → bölüm başına 2 çekim → Whisper ile metne karşı doğrulama → en iyi çekim seçilir. Şüpheli yerleri ikili ses incelemesi dinler. | doğruluk, okunuş, duygu, tempo |
| 3 | **Görsel dil (üslup karesi)** | Büyük kurul: 4 uzmanlık × 2 üye, 2 tur. Bunlar vazo resmi ve ikonografi, karakter ve illüstrasyon, kompozisyon/ışık/renk ve animasyon/hareket. | üsluba sadakat · okunurluk (siluet, küçük ekran) · kompozisyon ve odak · karakter tasarımı · hareket potansiyeli ("hiç durmayan" plan) · küçük resme taşınabilirlik |
| 4 | **Animatik** (yeni) | Gerçek ses zamanlamasıyla her plan için tek kare ve kamera notu; filmin kaba kurgusu. Büyük kurul: yönetmen × 2, izleyici/tutma × 2, görsel kurgu × 2. Pahalı animasyondan önce tempo ve plan listesi burada onaylanır. | tempo · söz-görüntü eşleşmesi · hareket planı · bölüm açılışları · doruk |
| 5 | **Sahne üretimi** | Bölüm bölüm. Her bölüm ikili incelemeden geçer (sanat + animasyon), hedef ≥ 9. Üç katmanın ilk sahneleri ayrıca katman kontrolünden geçer: siyah figür (Hesiodos), kırmızı figür (Aiskhylos), beyaz zemin (Erhat). | üslup tutarlılığı · hareket · okunurluk · anlatıma hizmet |
| 6 | **Müzik, efekt, miks** | `score.py`, `sfx.js`, `mix.py`. İkili ses incelemesi: ses seviyeleri, konuşmanın anlaşılırlığı, -14 LUFS ve -1 dBTP hedefi. | anlaşılırlık · duygu · teknik hedefler |
| 7 | **Render ve film incelemesi** | Tam render. Kurula tarihli kare dizileri ve zaman çizelgesi verilir. Son kurul: yönetmen, izleyici, sanat, kaynak (her biri × 2). | bütünlük · tempo · hata avı |
| 8 | **Kapak A/B** | Büyük kurul: TO/paketleme × 2, illüstrasyon × 2. Test seti: tam boy; 246×138 ve 168×94 küçültmeler; gri değer; mobil akış taklidi; süre rozeti bölgesi. | ilk bakışta okunma · tek odak · merak · videoya sadakat |
| 9 | **Shorts** | 40–55 sn'lik aday bölümler, ikili inceleme | kanca · bağımsız anlaşılırlık · uzun videoya köprü |
| 10 | **Teslim** | `youtube.md` (başlık, bölüm zaman damgaları, künye), `prometheus.tr.srt`, `yayin.md` | — |
| 11 | **Geriye dönüp bakış** (kullanıcının isteği) | Teslimden sonra bütün iş baştan sona yeniden gözden geçirilir ve tek soru sorulur: **"Yapabileceğim en iyi işi mi yaptım?"** Cevap dürüst verilir: ilk istekten neyin tam karşılandığı, nerede ödün verildiği ve nedeni (bütçe, süre, aracın sınırı), hâlâ düzeltilebilecek olanlar. Düzeltilebilecek olan düzeltilir, kalanlar kullanıcıya açıkça söylenir. | ilk isteğe sadakat · ödünlerin dürüstçe sayılması · düzeltilebilenin yapılması |

## Sabit kurallar
- Erhat'a mal edilen her görüş yalnız önsöz sayfalarından gelir (`kaynak/onsoz_notlar.md`). Fikirler kendi cümlelerimizle anlatılır; yalnız kısa alıntılar sayfa numarasıyla verilir. Aiskhylos ve Hesiodos alıntıları kendi çevirimizdir.
- Animasyon hiç durmaz (`sanat.md`, "Yönetmenlik ilkesi").
- Süre: hikâye kırpılmaz, tekrar ve dolgu kırpılır.
- Kredi harcayan üretim (ElevenLabs) planlıdır. Aynı çağrı "yeniden dene" diye tekrarlanmaz.
