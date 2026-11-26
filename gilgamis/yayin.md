# Yayın talimatı: Gılgamış (uzun video)

Yükleme YouTube Studio'da bilgisayardan yapılır. YouTube'un kendi zamanlaması kullanıldığı için yükleme bittikten sonra bilgisayarın açık kalması gerekmez.

## Zamanlama (Europe/Istanbul)
- **Uzun video:** 2 Aralık 2026 Çarşamba, 18:00 (kullanıcının kararı, 23 Kasım: Gılgamış Lale Çılgınlığı'ndan önce çıkar; dört günde bir: Narkissos 24 Kasım, Dorian Gray 28 Kasım, Gılgamış 2 Aralık, Lale Çılgınlığı 6 Aralık).
- **Ölçüm:** 48. saat 4 Aralık 18:00; 7. gün 9 Aralık (6 Aralık'ta çıkan Frankenstein'la üst üste biner; 27 Kasım'da Lale'yle yer değiştirdi; bilerek okunur). Dorian Gray'in 48. saat ölçümü (30 Kasım) bu video yayına girmeden alınır.

## Dosyalar
| Dosya | Ne için |
|---|---|
| `teslim/gilgamis_youtube.mp4` | **YouTube'a yüklenecek dosya** (255 MB, 11:17): 1920×1080, 30 fps, H.264 CRF 21 + AAC, Türkçe ses (−14 LUFS), BT.709 |
| `teslim/gilgamis_telefon.mp4` | Telefonda izlemek için küçük kopya (97 MB, H.265 iki geçiş 1000k; ses aynı) |
| `kapak/A.jpg` | Kapak A: "BİR AN / **ELİNDEYDİ**" (vurgu altın #E2B04F). Ortadan başlamak: bitki elde, yılan kapıyor; filmin ilk karesiyle (A01) aynı kompozisyon. Vaat 0:05'te karşılanıyor: "ölüme karşı aradığını buldu, **eline aldı**… ve bir yılana kaptırdı" (A01, 0:00,6–0:08,2). Yazı cevabı (yılanı) söylemez |
| `kapak/B.jpg` | Kapak B: "7 GECE / **GÖMMEDİ**" (vurgu meşale alevinin turuncusu #F2A04A). Karşıtlık: örtülü dost, başını ellerine almış adam, duvarda yedi çentik. Vaat A02'de: sahne 0:09,5'te açılır, "yedi gece" 0:14,6, "gömdürmemişti" 0:17 (ilk 5 sn'nin dışında; bkz. aşağıdaki not) |

**Kapak sistemine uyarlama (27 Kasım, `kanal/KAPAK_SISTEMI.md`):** kompozisyon iki kapakta da aynı kaldı.
- A: tek kelime ("ELİNDEYDİ") 2–4 kelime kuralının altındaydı ve vurgu yoktu. "BİR AN" eklendi: çelişkiyi (elindeydi, artık yok) söylüyor, kimin aldığını saklıyor. İki satır yazıya yer açmak için figür, bitki ve yılan 260 px sağa kaydı (bitki yazıdan ~70 px uzakta). Vurgu altın: bitki boyalı değil, yalnız mavi ışık halesi var ve su da mavi; görüntüde tek renkli nesne yok. Yazı hariç en parlak yer bitki.
- B: vurgu yoktu ve yazı hariç en parlak yer sağdaki meşaleydi (odak yas sahnesinden kayıyordu). Meşale kısıldı, ışık yatağın başına ve oturan adama taşındı; şimdi en parlak yer ikisinin arası. "GÖMMEDİ" alevin rengiyle vurgulandı; yazı 280 px'ten 300 px'e çıktı (kural ≥ 290).
- Test sayfaları: `kapak/test/A_test.jpg`, `kapak/test/B_test.jpg` (ölçümler `.txt`). B'nin vaadi ilk 5 sn'de değil (film değişmeden düzeltilemez); "Test ve karşılaştır" sonucu okunurken bu fark hesaba katılır.
| `gilgamis.tr.srt` | Türkçe altyazı (182 satır) |
| `youtube.md` | Başlık, açıklama (bölümler, kaynaklar), etiketler, sabit yorum |

## 1. Yükleme
1. Dosya adını `gilgamis-destani-olum.mp4` yap, **Oluştur → Video yükle**.
2. **Ayrıntılar:**
   - Başlık: `Gılgamış: Öleceğini Bile Bile Nasıl Yaşanır?`
   - Açıklama: `youtube.md` → "Açıklama" bölümünün tamamı (bölüm zaman damgaları dahil; ilk satır 0:00).
   - Küçük resim: `kapak/A.jpg`. **Test ve karşılaştır** açıksa ikinci olarak `kapak/B.jpg`. Test sürerken başlık değiştirilmez.
   - Oynatma listesi: "Mitler ve Felsefe".
   - Kitle: "Hayır, çocuklara özel değil".
   - Daha fazla göster: etiketler (`youtube.md`), video dili Türkçe, kategori Eğitim.
   - "Değiştirilmiş veya yapay içerik" sorusu: **Hayır**. Video gerçekçi görüntü içermez; stilize kabartma animasyondur. Anlatımın yapay zekâ sesi olduğu açıklamanın "Yapım" kısmında yazılı.
3. **Video öğeleri:**
   - Altyazı ekle → Dosya yükle → "Zamanlamalı" → `gilgamis.tr.srt`.
   - **Bitiş ekranı:** 10:57'den sona (20 sn). Anlatımdaki "ekranda" sözcüğü 11:00'de, yani bitiş ekranının içinde. Son karede (render'dan bakıldı) **sol yarı boş** kil zemin (x < 1080); **sağ yarıda** pişmiş tuğla sur ve burçların üstünde küçük Gılgamış figürü var. Öğeler sol yarıya: video öğesi üstte, "Abone ol" altında
   - **Video öğesi:** "Belirli video: Sisifos'u Neden Mutlu Hayal Etmeliyiz?" (anlatım "Sisifos, ekranda" diyor).
   - **"Kanalda ayrıca" satırı:** açıklamadaki Sisifos satırının sonuna videonun adresini yapıştır.
4. **Görünürlük:** Planla → 02.12.2026, 18:00 (GMT+3) → **Planla**.

## 2. Yayından sonra
- **Sabit yorum:** `youtube.md` → "Sabit yorum" (tufanla ilgili dinî karşılaştırma tartışmasını önceden çerçeveler).
- **Ölçüm:** 48. saatte (4 Aralık) `analiz/tahminler.md` → "Gılgamış" (G1–G3) ve `analiz/2026-11-23-deney-yon-promptu.md` deney tablosu doldurulur.

## Kulakla bakılacaklar (kullanıcı)
Sessizliğe dayalı hizalama kullanıldı; seslendirme kelime kelime dinlenmedi.
- Okunuşlar: "Şamhat", "Utnapiştim" (11 kez), "Urşanabi", "Humbaba", "Hattuşa", "Boğazkale", "ağustosböcekleri", "kâtipten kâtibe".
- D13 "Ta ki burnundan bir kurt düşene kadar" fısıltıyla okundu (4:48 civarı); müziğin altında kalmıyor mu? Ardından ~2 sn sessizlik bilerek.
- C03 "İnsanın günleri sayılıdır; ne yapsa yeldir" (2:20 civarı) ve H10 son soru tonu.
- Müzik: lir, dron ve davul (Re Frig); yatağın başında neredeyse sessiz; sur bölümünde sur motifi ilk kez tam. Müzik özgün sentez; duyulup duyulmadığı saniye saniye ölçüldü (678 saniyenin 663'ünde -60 dB üstü).
- Seçilen çekimler: s00 a, s01 a, s02 a, s03 a, s04 a, s05 a, s06 b, s07 a (`vo/secim.json`). Beğenmediğin bölüm olursa öbür çekim zaman çizelgesini birkaç saniye kaydırır; görüntü sözcüğe bağlı olduğu için kendiliğinden kayar, yeniden render gerekir.
