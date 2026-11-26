# Kanal marka, kitle ve altyapı: veri çekme promptu (27 Kasım 2026, tek parça)

Kullanıcının tarayıcısında YouTube'a ve Studio'ya giriş yapmış bir ajana verilir (Sonnet yeterli). Yalnız okur; yorum ve öneri başkanındır.

```
Görev: "Zaman Kuryesi" (@ZamanKuryesi) YouTube kanalı için aşağıdaki verileri YALNIZ OKU ve tek bir Claude Docs belgesinde Türkçe rapor ver. Yorum ve öneri yazma; yalnız gördüğünü yaz.

KURALLAR
- Hiçbir şeyi değiştirme. "Kaydet", "Yayınla", "Uygula", "Geri al", "Testi bitir" düğmelerine basma. Bir sayfada "Kaydet" kendiliğinden etkinleşirse hiçbir şeye dokunmadan sayfadan çık ve rapora yaz.
- Yorum yazma, beğenme, abone olma, mesaj gönderme.
- Sayıları ve metinleri ekranda gördüğün gibi yaz. Yoksa "görünmüyor". E-posta adresi görürsen yalnız "var" yaz.
- Her bölümde ekran görüntüsü al ve belgeye ekle.

1) KİTLE (Studio → Analytics → Kitle; önce son 28 gün, sonra son 90 gün)
   - Abone kazandıran içerikler: ilk 15 içerik ve kazandırdığı abone sayısı; Shorts toplamı ve uzun video toplamı ayrı.
   - "Kitlenizin izlediği kanallar" ve "Kitlenizin izlediği içerikler": listelerin tamamı.
   - Yeni / geri gelen / düzenli izleyici sayıları.
   - Son 5 uzun videonun her birinde: abone izlenmesi ve abone olmayan izlenmesi.

2) KANAL SAYFASI (gizli pencerede, izleyici gözüyle)
   - Ad, @kullanıcı adı, abone ve video sayısı, açıklama (aynen), bağlantılar.
   - Profil resmi ve banner (ekran görüntüsü, banner yazısı aynen).
   - Ana sayfada abone olmayana gösterilen öne çıkan video var mı, hangisi? Bölümler sırasıyla.
   - Oynatma listeleri: ad, video sayısı, sıra.
   - "Videolar" sekmesinin ilk 24 küçük resmi tek ekran görüntüsünde; Shorts sekmesinin ilk 12'si.

3) STUDIO ALTYAPISI (yalnız okuma)
   - Özelleştirme → Düzen ve Marka: kanal fragmanı, öne çıkan video, video filigranı.
   - Varsayılan yükleme ayarları: açıklama şablonu, etiketler, kategori, dil.
   - Son 8 uzun video için tablo: başlık · bitiş ekranında kaç öğe ve hangileri (hangi videoya gidiyor) · bilgi kartı sayısı · sabit yorum var mı (metni) · hangi oynatma listesinde · bölüm damgası var mı.

4) KARŞILAŞTIRMA (herkese açık sayfalar)
   - TED-Ed (@TEDEd) ve YouTube'da "animasyonlu mitoloji", "felsefe animasyon", "tarih animasyon" aramalarıyla bulduğun, Türkçe anlatımlı, çizim ya da animasyonla anlatan, 10 bin – 1 milyon aboneli 3 kanal.
   - Her biri için: ad, abone sayısı, son 10 videonun başlığı · süresi · görüntülemesi · tarihi, ilk 12 küçük resim (ekran görüntüsü), kanal fragmanı var mı, oynatma listeleri seri gibi mi duruyor.

SON
- "Dikkat çeken" başlığı altında en fazla 8 madde: yalnız gördüğün olgular.
- Belgenin bağlantısını ver.
```
