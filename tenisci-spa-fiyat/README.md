# Kurumlara ve gruplara özel spa fiyat listeleri (WhatsApp için)

Aynı fiyatlarla iki sürüm, tek şablondan üretilir:

- `navitas-tenisci-spa-fiyat-listesi.pdf`: tenis WhatsApp grupları için. Uygunluk satırı: "Tenisçi fiyatı için WhatsApp'tan yazmanız ya da söylemeniz yeterli." Hazır mesajda `(Ref: TENIS-PDF)`. Alt bölümde tenis kortu motifi.
- `navitas-karaca-spa-fiyat-listesi.pdf`: Karaca çalışanları için. İşletmenin kararıyla uygunluk kuralı yazılmadı; giriş satırında yalnız "Randevu için WhatsApp'tan yazın." var. Hazır mesajda `(Ref: KARACA-PDF)`. Başlıkta "Navitas × Karaca" düzeninde Karaca'nın kendi logosu var: `logo/karaca.svg`, karaca.com'un site başlığındaki yatay logo, hiç değiştirilmeden (renk ve oran aynı). Logonun bu listede kullanılmasına işletme 2026-11-04'te Karaca adına onay olduğunu bildirdi.

Her iki PDF de tek sayfa, telefona göre (1080 px genişlik), yaklaşık 690 KB; iki tıklanabilir WhatsApp bağlantısı var (giriş satırında ve alttaki düğmede).

- `sablon.html`: ortak sayfa. Sürüme göre değişen yerler `{{BASLIK}}`, `{{KURAL}}`, `{{IKON}}`, `{{MOTIF}}`, `{{ORTAK}}` (ortak kurum logosu), `{{WA}}`; değerleri `render.js` içindeki `VARIANTS` tablosunda. Yeni bir kurum için oraya bir satır eklemek yeter.
- `render.js`: `NODE_PATH=$(npm root -g) node tenisci-spa-fiyat/render.js` ikisini birden, `... render.js karaca` yalnız birini üretir.
- `logo/karaca.svg`: Karaca'nın resmi yatay logosu (kaynak: https://www.karaca.com/homepage/_next/static/media/karaca.18zadd84dr4do.svg, 2026-11-04). Yalnız Karaca sürümünde kullanılır.
- `foto/`: tesis fotoğrafları (havlu, masaj odası, Fin saunası, VIP Süit, havuz). Kullanıcının paylaştığı orijinallerden kırpıldı ve sitenin "edited" renk ayarıyla (site reposu `scripts/add-photos.py`) hafifçe ısıtıldı. Havuz fotoğrafının etiketi "Havuz · Çift Masajı'na dahil": kaynakta havuz yalnız Çift Masajı'na dahil.
- `onizleme-tenisci.jpg`, `onizleme-karaca.jpg`: yalnız kontrol için sayfa görüntüleri; gruba gönderilecek biçim değil.
- `kurul/`: tenisçi listesinin bağımsız danışma kurulu değerlendirmesi (`kurul/RECOMMENDATION.md`'den başlayın). Kurul tenisçi sürümünü değerlendirdi; Karaca sürümü aynı fiyat ve düzeltmeleri kullanıyor, ayrıca kurula sunulmadı.

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
| 30 seans İsveç paketi | 50.000 TL | 35.000 TL (seansı yaklaşık 1.167) |
| 30 seans Mix paket | listede yok | 35.970 TL (seansı 1.199, işletmenin belirlediği özel fiyat) |

30'lu paketler işletmenin talimatıyla eklendi: 30'lu İsveç sitedeki liste fiyatından (50.000 TL) %30 indirimli; 30'lu Mix'in sitede liste fiyatı olmadığı için seansı 1.199 TL'ye gelecek şekilde 35.970 TL olarak belirlendi ve PDF'te üstü çizili fiyat yerine "özel fiyat" yazıyor. "10 masaj + 10 kese köpük" paketi için özel fiyat tanımlanmadı.

## Kurallar (işletmenin verdiği)

- Geçerlilik: 31 Aralık 2026 (iki sürümde de).
- Tenisçi: kanıt istenmiyor, WhatsApp'tan bu listeden yazmak ya da söylemek yeterli. Karaca: PDF'te kural yok, resepsiyon uygular.
- VIP 12.000 TL'ye iki terapistle kişi başı 60 dk masaj dahil (işletme teyidi).
- Paketler peşin ödenir, satın alındıktan sonra bir yıl içinde kullanılır, arkadaşla paylaşılabilir. Mix'te her seansta İsveç, aromaterapi ya da derin doku seçilir.
- Randevu için ön ödeme yok. Hafta içi 07.00–22.00, hafta sonu 08.00–22.00.

## Takip

Tenisçi PDF'indeki bağlantılar "Merhaba, tenisçilere özel spa fiyat listesinden yazıyorum. Randevu almak istiyorum. (Ref: TENIS-PDF)", Karaca PDF'indekiler aynı metni Karaca için ve `(Ref: KARACA-PDF)` ile açar. Ref kodu yalnız ölçüm içindir, fiyat şartı değildir. Grup mesajındaki bağlantılarda her gruba ayrı kod kullanın (TENIS-1, TENIS-2 ...). Lead tablosunda: DATA KAYNAĞI listesine "Tenisçi grubu" eklenir, KAMPANYA "Tenisçi listesi 2026", REF KODU mesajdaki kod (hazır mesajsız "tenis listesi" diyenler için TENIS-SOZLU).

## Tasarım

Sitenin dili: Marcellus başlıklar, Hanken Grotesk metin, krem zemin, kahve ve amber tonları. Sıra: logo, geçerlilik tarihi, başlık, indirim satırı, kemer kesimli kapak fotoğrafı (Navitas spa işlemeli havlu), tek seanslar, masaj odası ve sauna fotoğrafları, paketler, VIP Süit ve havuz fotoğraflarıyla iki kişilik bölüm, koşul kutusu, koyu alt bölümde WhatsApp düğmesi (tenisçi sürümünde ince çizgili tenis kortu motifi). Önemli metin telefonda en az 10 pt (≥ 28 CSS px).
