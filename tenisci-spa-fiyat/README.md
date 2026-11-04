# Tenisçilere Özel Spa Fiyat Listesi (WhatsApp grupları için)

- `navitas-tenisci-spa-fiyat-listesi.pdf`: gruplara gönderilecek PDF. Tek sayfa, telefon ekranına göre (1080 px genişlik), 260 KB civarı. WhatsApp düğmesi tıklanabilir.
- `onizleme.jpg`: aynı sayfanın görsel hali (PDF açmak istemeyenler için).
- `index.html`: kaynak. Fiyatı ya da metni burada değiştirip `NODE_PATH=$(npm root -g) node tenisci-spa-fiyat/render.js` ile PDF'i ve önizlemeyi yeniden üretin.

## Fiyatlar
Sitedeki liste fiyatlarına (navitastopkapi.com/masaj, Kasım 2026) %20 tenisçi indirimi uygulandı. Paketler bilerek eklenmedi: tenisçi tek seans İsveç fiyatı (2.400 TL), 10'lu İsveç paketinin seans başı fiyatından (2.500 TL) düşük kalıyor.

| Hizmet | Liste | Tenisçi |
|---|---|---|
| İsveç Masajı, 50 dk | 3.000 TL | 2.400 TL |
| Derin Doku Masajı, 50 dk | 3.500 TL | 2.800 TL |
| Aromaterapi Masajı, 50 dk | 3.500 TL | 2.800 TL |
| Navitas Spesiyal, 55 dk | 4.500 TL | 3.600 TL |
| Kese Köpük, 30 dk | 2.250 TL | 1.800 TL |
| Çift Masajı, 50 dk (iki kişi) | 4.000 TL | 3.200 TL |
| VIP Özel Spa Süiti, 3 saat (iki kişi) | 15.000 TL | 12.000 TL |

## Takip
WhatsApp düğmesi şu hazır mesajı açar: "Merhaba, tenisçilere özel spa fiyat listesinden ulaşıyorum. Randevu almak istiyorum." Bu mesajla gelenler lead takibine kaynak olarak "Tenisçi grubu" diye girilebilir.

## Tasarım
Sitenin dili: Marcellus başlıklar, Hanken Grotesk metin, krem zemin, kahve ve amber tonları. Kemer kesimli kapak fotoğrafı (Navitas işlemeli havlu), %20 rozeti, küçük tenis topu simgesi ve alt bölümde ince çizgili bir tenis kortu motifi.
