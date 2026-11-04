# Tenisçilere Özel Spa Fiyat Listesi (WhatsApp grupları için)

- `navitas-tenisci-spa-fiyat-listesi.pdf`: gruplara gönderilecek PDF. Tek sayfa, telefona göre (1080 px genişlik), 260 KB civarı. İki tıklanabilir WhatsApp bağlantısı var (giriş satırında ve alttaki düğmede), ikisi de aynı hazır mesajı açar.
- `index.html`: kaynak. Fiyatı ya da metni burada değiştirip `NODE_PATH=$(npm root -g) node tenisci-spa-fiyat/render.js` ile PDF'i ve önizlemeyi yeniden üretin.
- `onizleme.jpg`: yalnız kontrol için sayfanın görüntüsü (2160 px genişlik). Gruba gönderilecek bir biçim değil; görsel isteyen bir yönetici olursa PDF'in yerine ayrı bir 4:5 kart hazırlanmalı.
- `kurul/`: listenin bağımsız danışma kurulu değerlendirmesi. `kurul/RECOMMENDATION.md`'den başlayın.

## Fiyatlar (31 Aralık 2026'ya kadar geçerli)

Liste fiyatları işletmenin fiyat listesinden (site reposu `lib/rituals.ts`, `components/pages/masaj.tsx`; yayındaki site fiyat göstermiyor). Tek seanslarda %20, paketlerde %30 tenisçi indirimi. Çift Masajı zaten kampanyalı fiyat olduğu için ek indirim yok. Fiyatlar yuvarlak; x99 önerisi kurulda değerlendirildi ve benimsenmedi.

| Hizmet | Liste | Tenisçi |
|---|---|---|
| İsveç Masajı, 50 dk | 3.000 TL | 2.400 TL |
| Derin Doku Masajı, 50 dk | 3.500 TL | 2.800 TL |
| Aromaterapi Masajı, 50 dk | 3.500 TL | 2.800 TL |
| Navitas Spesiyal, 55 dk | 4.500 TL | 3.600 TL |
| Kese Köpük, 30 dk | 2.250 TL | 1.800 TL |
| Çift Masajı, 50 dk (iki kişi) | 4.000 TL (kampanya) | 4.000 TL |
| VIP Özel Spa Süiti, 3 saat (iki kişi) | 15.000 TL | 12.000 TL |
| 10 seans İsveç paketi | 25.000 TL | 17.500 TL (seansı 1.750) |
| 20 seans İsveç paketi | 35.000 TL | 24.500 TL (seansı 1.225) |
| 10 seans Mix paket | 30.000 TL | 21.000 TL (seansı 2.100) |
| 20 seans Mix paket | 40.000 TL | 28.000 TL (seansı 1.400) |

Listede olmayan 30'lu İsveç paketi ve "10 masaj + 10 kese köpük" paketi için tenisçi fiyatı tanımlanmadı.

## Kurallar (işletmenin verdiği)

- Geçerlilik: 31 Aralık 2026.
- Kanıt istenmiyor: WhatsApp'tan bu listeden yazmak ya da söylemek yeterli.
- Paketler peşin ödenir, satın alındıktan sonra bir yıl içinde kullanılır, arkadaşla paylaşılabilir. Mix'te her seansta İsveç, aromaterapi ya da derin doku seçilir.
- Randevu için ön ödeme yok. Hafta içi 07.00–22.00, hafta sonu 08.00–22.00.

## Takip

PDF'teki bağlantılar şu hazır mesajı açar: "Merhaba, tenisçilere özel spa fiyat listesinden yazıyorum. Randevu almak istiyorum. (Ref: TENIS-PDF)". Ref kodu yalnız ölçüm içindir, fiyat şartı değildir. Grup mesajındaki bağlantılarda her gruba ayrı kod kullanın (TENIS-1, TENIS-2 ...). Lead tablosunda: DATA KAYNAĞI listesine "Tenisçi grubu" eklenir, KAMPANYA "Tenisçi listesi 2026", REF KODU mesajdaki kod (hazır mesajsız "tenis listesi" diyenler için TENIS-SOZLU).

## Tasarım

Sitenin dili: Marcellus başlıklar, Hanken Grotesk metin, krem zemin, kahve ve amber tonları. Sıra: logo, geçerlilik tarihi, başlık, indirim ve uygunluk satırı, kemer kesimli kapak fotoğrafı (Navitas işlemeli havlu), fiyat listeleri, koşul kutusu, koyu alt bölümde WhatsApp düğmesi ve ince çizgili tenis kortu motifi. Önemli metin telefonda en az 10 pt (≥ 28 CSS px).
