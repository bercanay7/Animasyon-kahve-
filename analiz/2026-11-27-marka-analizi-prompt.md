# Kanal marka ve altyapı analizi: veri çekme promptu (27 Kasım 2026)

Kullanıcının tarayıcısında YouTube'a ve Studio'ya giriş yapmış bir ajana verilir. Yalnız okur ve ekran görüntüsü alır; yorum ve öneri başkanındır.

```
Görev: "Zaman Kuryesi" (@ZamanKuryesi) YouTube kanalının marka kimliğini ve kanal altyapısını YALNIZ OKU, bana Türkçe bir rapor ver. Yorum ve öneri yazma; ne gördüğünü yaz.

KESİN KURALLAR
- Hiçbir şeyi değiştirme: Studio'da "Özelleştirme", video ayrıntıları, oynatma listeleri, topluluk sekmesi dahil. "Kaydet", "Yayınla", "Uygula", "Geri al" düğmelerine basma. Bir sayfa açılınca "Kaydet" etkinleşirse dokunma, sayfadan çık ve bunu rapora yaz.
- Yorum yazma, beğenme, abone olma, kimseye mesaj gönderme.
- Metinleri aynen kopyala; sayıları ekranda gördüğün gibi yaz. Yoksa "görünmüyor".
- Her bölümde ekran görüntüsü al (telefon görünümü varsa onu da).

A) KANAL SAYFASI (izleyici gözüyle; çıkış yapmış gibi görmek için gizli pencere kullan)
   1. Kanal adı, @kullanıcı adı, abone sayısı, video sayısı, profil resmi ve banner (ekran görüntüsü; banner'daki yazı aynen).
   2. Kanal açıklaması (aynen), bağlantılar, katılma tarihi, ülke, toplam görüntüleme.
   3. Ana sayfa düzeni: abone olmayana gösterilen öne çıkan video (kanal fragmanı) var mı, hangisi? Bölümler sırasıyla (ad ve içindeki ilk 3 video).
   4. Oynatma listeleri: ad, video sayısı, açıklama, kapak.
   5. "Videolar" sekmesinin ilk 24 küçük resmi tek ekran görüntüsünde (ızgara görünümü): bir yabancı gözüyle aynı kanal gibi duruyorlar mı? Sadece gördüğünü yaz: renkler, yazı tipi, figür, yazı miktarı.
   6. Shorts sekmesi: ilk 12 küçük resim.
   7. Topluluk sekmesi: son 5 gönderi (tarih, tür, metin).

B) STUDIO ALTYAPISI (Özelleştirme ve Ayarlar; yalnız okuma)
   1. Özelleştirme → Düzen: kanal fragmanı, öne çıkan video, öne çıkan bölümler.
   2. Özelleştirme → Marka: profil resmi, banner, video filigranı (var mı, ne zaman görünüyor).
   3. Özelleştirme → Temel bilgiler: ad, kullanıcı adı, açıklama, bağlantılar, iletişim bilgisi (e-posta varsa yalnız "var" yaz, adresi yazma).
   4. Ayarlar → Varsayılan yükleme ayarları: başlık/açıklama şablonu, etiketler, kategori, dil, altyazı dili, lisans, yorum ayarı.
   5. Ayarlar → Kanal → Temel bilgiler: ülke, anahtar kelimeler (aynen).
   6. Son 8 uzun videonun her biri için (yalnız oku): başlık · açıklamanın ilk 3 satırı · bölüm damgası var mı · etiket sayısı · kategori · bitiş ekranı öğeleri (sayı ve tür) · bilgi kartı sayısı · sabit yorum (metni) · oynatma listesi · altyazı dilleri · kapak (ekran görüntüsü).

C) KARŞILAŞTIRMA (herkese açık sayfalar)
   1. TED-Ed (@TEDEd): A1–A5 ile aynı bilgiler (fragman, bölümler, ilk 24 küçük resim, son 10 videonun başlığı, süresi, görüntülemesi, yayın aralığı).
   2. YouTube'da "animasyonlu mitoloji", "felsefe animasyon", "tarih animasyon belgesel", "kitap özeti animasyon" aramalarıyla, Türkçe anlatımlı, animasyon ya da çizimle hikâye anlatan, 10 bin – 1 milyon aboneli 4 kanal seç. Her biri için: ad, abone, son 10 videonun başlığı · süre · görüntüleme · yayın tarihi, kanal açıklaması, ilk 12 küçük resim (ekran görüntüsü), kanal fragmanı var mı.
   3. Seçtiğin 4 kanalı neden seçtiğini tek satırla yaz.

RAPOR BİÇİMİ
- A, B, C başlıklarıyla; sayılar tabloyla; metinler aynen alıntı.
- En sonda "Dikkat çeken" başlığı altında en fazla 8 madde: yalnız ekranda gördüğün olgular, yorum yok.
- Raporu bir Claude Docs belgesi olarak ver; ekran görüntülerini belgeye ekle.
```
