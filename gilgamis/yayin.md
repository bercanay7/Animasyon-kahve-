# Yayın talimatı: Gılgamış (uzun video)

Yükleme YouTube Studio'da bilgisayardan yapılır. YouTube'un kendi zamanlaması kullanıldığı için yükleme bittikten sonra bilgisayarın açık kalması gerekmez.

## Zamanlama (Europe/Istanbul)
- **Uzun video:** 6 Aralık 2026 Cumartesi, 18:00 (kullanıcının kararı, 23 Kasım; Lale Çılgınlığı 2 Aralık'tan dört gün sonra).
- **Ölçüm:** 48. saat 8 Aralık 18:00; 7. gün 13 Aralık. Lale'nin 48. saat ölçümü (4 Aralık) bu video yayına girmeden alınır.

## Dosyalar
| Dosya | Ne için |
|---|---|
| `teslim/gilgamis_youtube.mp4` | **YouTube'a yüklenecek dosya** (255 MB, 11:17): 1920×1080, 30 fps, H.264 CRF 21 + AAC, Türkçe ses (−14 LUFS), BT.709 |
| `teslim/gilgamis_telefon.mp4` | Telefonda izlemek için küçük kopya (97 MB, H.265 iki geçiş 1000k; ses aynı) |
| `kapak/A.jpg` | Kapak A: "ELİNDEYDİ" (ortadan başlamak: bitki elde, yılan kapıyor). Filmin ilk karesiyle aynı kompozisyon |
| `kapak/B.jpg` | Kapak B: "7 GECE GÖMMEDİ" (karşıtlık: örtülü dost, başını ellerine almış adam, duvarda yedi çentik). İlk 10 saniyede karşılanıyor (A02) |
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
4. **Görünürlük:** Planla → 06.12.2026, 18:00 (GMT+3) → **Planla**.

## 2. Yayından sonra
- **Sabit yorum:** `youtube.md` → "Sabit yorum" (tufanla ilgili dinî karşılaştırma tartışmasını önceden çerçeveler).
- **Ölçüm:** 48. saatte (8 Aralık) `analiz/tahminler.md` → "Gılgamış" (G1–G3) ve `analiz/2026-11-23-deney-yon-promptu.md` deney tablosu doldurulur.

## Kulakla bakılacaklar (kullanıcı)
Sessizliğe dayalı hizalama kullanıldı; seslendirme kelime kelime dinlenmedi.
- Okunuşlar: "Şamhat", "Utnapiştim" (11 kez), "Urşanabi", "Humbaba", "Hattuşa", "Boğazkale", "ağustosböcekleri", "kâtipten kâtibe".
- D13 "Ta ki burnundan bir kurt düşene kadar" fısıltıyla okundu (4:48 civarı); müziğin altında kalmıyor mu? Ardından ~2 sn sessizlik bilerek.
- C03 "İnsanın günleri sayılıdır; ne yapsa yeldir" (2:20 civarı) ve H10 son soru tonu.
- Müzik: lir, dron ve davul (Re Frig); yatağın başında neredeyse sessiz; sur bölümünde sur motifi ilk kez tam. Müzik özgün sentez; duyulup duyulmadığı saniye saniye ölçüldü (678 saniyenin 663'ünde -60 dB üstü).
- Seçilen çekimler: s00 a, s01 a, s02 a, s03 a, s04 a, s05 a, s06 b, s07 a (`vo/secim.json`). Beğenmediğin bölüm olursa öbür çekim zaman çizelgesini birkaç saniye kaydırır; görüntü sözcüğe bağlı olduğu için kendiliğinden kayar, yeniden render gerekir.
