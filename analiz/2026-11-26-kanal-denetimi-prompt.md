# YouTube Studio veri çekme promptu (kanal düzeyi denetimi, 26 Kasım 2026)

Kullanıcının tarayıcısında YouTube Studio'ya giriş yapmış bir ajana verilir. Yalnız okur, hiçbir ayarı değiştirmez.
Sonuç `analiz/2026-11-26-narkissos-48saat.md` dosyasındaki "Kanal düzeyi denetimi" listesini karşılar.

```
Görev: YouTube Studio'da "Zaman Kuryesi" kanalının verilerini YALNIZ OKU ve bana Türkçe bir rapor olarak ver.

KESİN KURALLAR
- Hiçbir şeyi değiştirme: ayar, başlık, kapak, açıklama, kitle ayarı, A/B testi, oynatma listesi. "Kaydet", "Yayınla", "Testi bitir", "Uygula" düğmelerine basma.
- Sayıları ekranda gördüğün gibi yaz; tahmin etme, yuvarlama. Bir veri yoksa "görünmüyor" yaz.
- Gelişmiş mod (Analytics → sağ üst "Gelişmiş mod") okumak için serbest. Dışa aktarma (CSV) serbest; dosyayı yalnız bana ver.
- Her bölümün sonunda ekran görüntüsü al.

1) KANAL ERİŞİMİ, SON 90 GÜN
   Analytics → Erişim → tarih: Son 90 gün.
   - Gösterim, gösterim TO, görüntüleme toplamları.
   - Gelişmiş modda "Tarih" boyutuyla HAFTALIK tablo: her hafta için gösterim, TO, görüntüleme.
   - Trafik kaynağı türleri (son 90 gün ve son 28 gün ayrı): her kaynağın görüntüleme ve yüzdesi.

2) KANAL DURUMU
   - Ayarlar → Kanal → Özellik uygunluğu: üç basamağın durumu ve "Kanal durumu" bölümündeki her yazı (Topluluk Kuralları ihtarı, telif ihtarı var mı).
   - Kontrol paneli ve bildirimlerde kısıtlama, politika ya da "kanal ihlali" uyarısı var mı? Varsa metnini aynen yaz.
   - Para kazanma sayfasında "özgün olmayan / tekrarlayan içerik" ile ilgili uyarı var mı?

3) KİTLE VE İÇERİK AYARLARI
   - Ayarlar → Varsayılan yükleme ayarları → Gelişmiş ayarlar: Kitle seçeneği ne? ("çocuklara özel" mi, değil mi?)
   - İçerikler → Videolar listesi: son 15 video (Shorts dahil) için tablo: başlık · tarih · süre · Kısıtlamalar sütunu · Görüntüleme.
   - Son 6 uzun video (Narkissos, Mary Stuart, Ran, Kafka, İkaros, Milton) için Ayrıntılar → "Daha fazla göster": Kitle ayarı, "Değiştirilmiş içerik" (Evet/Hayır), yaş kısıtlaması. Yalnız oku, kaydetme.

4) NARKISSOS ("Kendini Sevmek Ne Zaman Narsisizme Döner? | Narkissos…"), yayından bu yana
   Video Analytics → Gelişmiş mod.
   - Trafik kaynağı: Önerilen videolar → ilk 15 kaynak video: video adı · kanal adı · görüntüleme. (Bizim videolarımız mı, başka kanallar mı?)
   - Trafik kaynağı: YouTube araması → arama terimlerinin tamamı ve görüntülemeleri.
   - Trafik kaynağı: Göz atma özellikleri alt kırılımı (Ana sayfa, Abonelikler, İzleme listesi…).
   - "Diğer" ve "Harici" kaynaklarının alt kırılımı.
   - Gösterimler ve TO: saatlik ya da günlük tablo (yayından bu yana).
   - Kitleyi elde tutma (hazırsa): eğrinin şu noktalardaki yüzdesi: 0:05, 0:10, 0:20, 0:30, 0:45, 1:00, sonra 8:52'ye kadar her 30 sn; ayrıca 6:23, 7:19, 7:40, 7:50. "Önemli an", "Artış", "Düşüş" işaretlerinin başlangıç ve bitiş zamanları. Hazır değilse "hazır değil" yaz.
   - A/B testi durumu: iki kapağın yüzdeleri ve test bitti mi?
   - Kitle: ülkeler (ilk 10, yüzdeleriyle), altyazı dilleri, abone / abone olmayan izlenme süresi payı, cihaz türü.

5) SHORTS
   Son 5 Shorts için: başlık · tarih · görüntüleme · "İzlemeye devam eden" / "Kaydırarak geçen" yüzdesi · ortalama izleme süresi.

RAPOR BİÇİMİ
- Her bölüm başlıkla, sayılar tabloyla.
- En sonda "Dikkat çeken" başlığı altında en fazla 5 madde: yalnız ekranda gördüğün olgular, yorum yok.
```
