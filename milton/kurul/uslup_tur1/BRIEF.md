# Üslup karesi kurulu, tur 1: ortak brif

Sen "Zaman Kuryesi" YouTube kanalının üslup kurulunda bağımsız bir üyesin. Değerlendirilen şey, yeni videonun (Milton, *Kayıp Cennet* ve Şeytan'ın iç yolculuğu) görsel dilini belirleyecek **tek üslup karesi**. Kare onaylanırsa aynı dil yaklaşık 23 dakikalık filmin bütün sahnelerine yayılacak.

## Bağlam
- **Üslup hedefi:** Gustave Doré'nin 1866 tarihli *Kayıp Cennet* gravürleri: siyah-beyaz, ton çizgi kalınlığıyla verilir, ışık huzmeleri, karanlık kütleler, düşmüş melek.
- **Üretim:** görüntü baştan sona kodla çiziliyor (Canvas 2D, `milton/lib/gravur.js`, `prim.js`, `kanat.js`, `figur.js`, sahne `lib/sahne/gol.js`). Hazır görsel, fotoğraf ya da Doré levhası kullanılmıyor; Doré kopyalanmıyor, dili örnek alınıyor.
- **Kodla çizimin sınırı:** siluet, kompozisyon, ışık ve dönüşüm güçlü; yüz yakın planı, el ve karmaşık anatomi zayıf. Bu yüzden karede yüz gölgede bırakıldı, yalnız iki göz ışığı var.
- **Kullanıcının üç bağlayıcı isteği:**
  1. Çizim gözü yormasın.
  2. Ucuz ve kalitesiz durmasın.
  3. Olabildiğince profesyonel olsun.
- **Bu isteklerden çıkan karar:** tarama bilerek Doré'den daha seyrek ve kalın tutuldu, benekli gürültü azaltıldı, geniş düz siyah ve temiz kâğıt alanları bırakıldı. Sebep: izleyicinin %48'i telefonda izliyor ve ince çizgiler video sıkıştırmasında titreşiyor.
- **Sahne:** destanın açılışı (I. kitap). Şeytan yanan gölde gözlerini açıyor, kırılmaz zincirlerle göle bağlı, dokuz gün düşmüş. "Alev var ama ışık yok; yalnızca görünür bir karanlık." Sağ üstteki ışık, yitirdiği cennetten kalan uzak yarık.
- **Görsel kırmızı çizgiler (hassasiyet kurulu):**
  - Tanrı ve Oğul yalnız ışık olarak gösterilir.
  - Âdem ile Havva yalnız uzak, örtülü siluet olur.
  - Çıplaklık ve cinsel çağrışım olmaz.
  - Kubbe, minare, hilal gibi İslam mimarisi çağrışımı olmaz.

## Dosyalar (hepsi `/home/user/Animasyon-kahve-/milton/kurul/uslup_tur1/` altında)
| Dosya | Ne |
|---|---|
| `kare_t1.jpg` | Üslup karesi, 1920×1080, t = 1,0 sn |
| `kare_t1_sonraki.jpg` | Bir sonraki film karesi (t = 1,033 sn); titreşim kontrolü için |
| `kare_t3.jpg` | Aynı sahne, t = 3,0 sn; alev ve duman hareketi |
| `kirpma_figur_1e1.png`, `kirpma_gok_1e1.png`, `kirpma_alev_1e1.png` | Bire bir kırpmalar |
| `telefon_640.png`, `kucuk_246.png`, `kucuk_168.png` | Telefon ve küçük resim boyları |
| `gri.png` | Gri değer |
| `ref/dore_satan.jpg`, `ref/dore_abdiel.jpg`, `ref/dore_abdiel_kirpma_1e1.png` | Doré'nin iki özgün levhası (kamu malı); yalnız karşılaştırma için |

Kodu da okuyabilirsin (`/home/user/Animasyon-kahve-/milton/lib/`); özellikle somut parametre önerisi vereceksen.

## Puanlama
| Ölçüt | Ağırlık |
|---|---|
| U1 gravür diline sadakat (Doré'yi çağrıştırıyor mu, ucuz filtre gibi mi duruyor?) | %20 |
| U2 göz konforu ve okunurluk (telefon, küçük boy, titreşim, kalabalık) | %20 |
| U3 kompozisyon, değer planı ve odak | %20 |
| U4 karakter (Şeytan figürü, kanatlar; siluet, oran, anlatım) | %20 |
| U5 profesyonellik ve bitmişlik (kusur, yapaylık, tutarsızlık) | %10 |
| U6 hareket potansiyeli ve sahnelere taşınabilirlik | %10 |

- Ağırlıklı ortalama ≥ 9,0 ise **ONAY**; herhangi bir ölçüt 7'nin altındaysa **RED**.
- Sert ol. Bu kare onaylanırsa bütün film bu düzeyde olacak; gerçek bir Doré levhasının yanına koyunca nerede ucuz durduğunu söyle.

## Çıktı
Raporunu yalnız şu dosyaya JSON olarak yaz: `/home/user/Animasyon-kahve-/milton/kurul/uslup_tur1/<kodun>.json`

```json
{
  "uye": "<kod>",
  "karar": "ONAY|RED",
  "puanlar": {"U1":0,"U2":0,"U3":0,"U4":0,"U5":0,"U6":0},
  "agirlikli": 0.0,
  "duzeltmeler": [
    {"sira":1, "bolge":"x0–x1, y0–y1 (1920×1080)", "sorun":"…", "oneri":"… (mümkünse dosya ve parametre adıyla)", "onem":"kritik|yüksek|orta|düşük"}
  ],
  "korunmali": ["…"],
  "en_emin_olmadigim_nokta": "…"
}
```

## Kurallar
- Hiçbir dosyayı değiştirme; yalnız kendi rapor dosyanı yaz.
- Başka üyelerin raporlarını okuma.
- Düzeltmeleri önem sırasına koy; her birinde kare üzerindeki bölgeyi koordinatla ver.
- Son mesajında kararı, puanı ve en önemli 3 düzeltmeyi kısaca yaz.
