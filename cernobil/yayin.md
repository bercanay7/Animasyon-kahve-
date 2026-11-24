# Yayın talimatı: Çernobil'in çayı (uzun video)

Yükleme YouTube Studio'da bilgisayardan yapılır. YouTube'un kendi zamanlaması kullanıldığı için yükleme bittikten sonra bilgisayarın açık kalması gerekmez.

## Zamanlama (Europe/Istanbul)
- **Uzun video (öneri):** 14 Aralık 2026 Pazartesi, 18:00. Dört günde bir düzeninin sıradaki yuvası (Lale Çılgınlığı 6 Aralık, Frankenstein 10 Aralık). Takvim kullanıcının; başka güne alınırsa yalnız bu satır ve ölçüm günleri değişir.
- **Ölçüm:** 48. saat 16 Aralık 18:00; 7. gün 21 Aralık. Frankenstein'ın 48. saat ölçümü (12 Aralık) bu video yayına girmeden alınır.

## Yayından önce: dört sayfaya bakılacak (kullanıcı)
Videodaki bütün sözler Milliyet arşivinin **OCR metninden** alındı (`kaynak/ARSIV.md`). Sayfa görüntüsü arşivde oturum açınca görülüyor; bu oturumdan açılamadı. Şu dört sayfaya bir kez bakılması yeterli:
1. **9 Aralık 1986, s. 7** ("Radyasyona inat, bardak bardak içti"). Aynı haber arşivde **9 Ocak 1987, s. 7** olarak da duruyor. Hangisinin doğru tarih olduğu görüntüden anlaşılır (sayfanın üstündeki tarih). **9 Ocak çıkarsa** iki cümle değişir: C05 "Aralık'ta" → "Ocak'ta", D01 "Aynı ay" → "Bir ay önce"; ikisi tek cümle yamasıyla düzeltilir (`mary-stuart/tools/yama_vo.py`, kredi gerekir).
2. **6 Ocak 1987, s. 11** (Çaykur: 56 bin ton; genel müdürün "göstermelik" sözü).
3. **25 Aralık 1989, s. 3 ve 12** (fabrika bahçelerine gömme; "Killi toprağa gömülen çaylar…").
4. **31 Mart 1990, s. 12** (köylülerin "TAEK'in raporuna mı, yoksa kendi gözlerimize mi inanalım?" sözü).

## Dosyalar
| Dosya | Ne için |
|---|---|
| `teslim/cernobil_youtube.mp4` | **YouTube'a yüklenecek dosya** (351 MB, 11:43; Fable'ın son okumasından sonraki sürüm): 1920×1080, 30 fps, H.264 iki geçiş 3,7 Mbps + AAC 256k, Türkçe ses (−14,2 LUFS, tepe −1,0 dBFS), BT.709. Tram dokusu yüzünden CRF 18 ara render 900 MB'ı aşıyordu; teslim bit hızıyla küçültüldü |
| `teslim/cernobil_telefon.mp4` | Telefonda izlemek için küçük kopya (~93 MB; H.265 iki geçiş 920k, AAC 128k) |
| `kapak/A.jpg` | Kapak A: "BAKAN İÇTİ" (kaldırılan bardak, mikrofonlar; yüz yok). İlk 5 sn'de karşılanıyor |
| `kapak/B.jpg` | Kapak B: "58 BİN TON NEREYE?" (naylonla örtülü çuvallar, dökülen çay). 0:09'da açılıyor, 7:04-9:42'de karşılanıyor, sayı 9:11'de duyuluyor |
| `cernobil.tr.srt` | Türkçe altyazı (177 satır) |
| `kapak/test/` | Kapak odak ölçümü (`araclar/kapak/odak.py`): A tek odak (yazının "İÇTİ" satırı); B dört tepe (yazı ve dökülen çay), test ve karşılaştır kararı verir |
| `youtube.md` | Başlık, açıklama (bölümler, kaynaklar, yapım notu; 56/58 bin ton ve canlandırma notu), etiketler, sabit yorum |
| `fable_son_okuma/` | Üç izleyicili son okuma ve başkanın doğrulaması: neyin neden değiştiği |

## 1. Yükleme
1. Dosya adını `cernobil-cayini-icer-miydin.mp4` yap, **Oluştur → Video yükle**.
2. **Ayrıntılar:**
   - Başlık: `Çernobil'in Çayını Sen İçer miydin?`
   - Açıklama: `youtube.md` → "Açıklama" bölümünün tamamı (bölüm zaman damgaları dahil; ilk satır 0:00).
   - Küçük resim: `kapak/A.jpg`. **Test ve karşılaştır** açıksa ikinci olarak `kapak/B.jpg`. Test sürerken başlık değiştirilmez.
   - Oynatma listesi: "Tarihin Dönüm Noktaları".
   - Kitle: "Hayır, çocuklara özel değil".
   - Daha fazla göster: etiketler (`youtube.md`), video dili Türkçe, kategori Eğitim.
   - "Değiştirilmiş veya yapay içerik" sorusu: **Hayır**. Video gerçekçi görüntü içermez; stilize gazete baskısı animasyonudur. Anlatımın yapay zekâ sesi olduğu açıklamanın "Yapım" kısmında yazılı.
3. **Video öğeleri:**
   - Altyazı ekle → Dosya yükle → "Zamanlamalı" → `cernobil.tr.srt`.
   - **Bitiş ekranı:** son 20 saniye (11:22'ten sona). Son karede ortada yukarıdan görülen bir bardak dem (kehribar daire) ve altında "ZAMAN KURYESİ" yazısı; **sol ve sağ kenarlar boş**. Video öğesi sola, "Abone ol" sağa.
   - **Video öğesi:** "Belirli video: Lale Çılgınlığı" (aynı oynatma listesi; "herkes yapıyorsa" sorusu bu videonun "herkes içiyorsa" sorusuyla akraba).
   - **"Kanalda ayrıca" satırı:** açıklamadaki Lale Çılgınlığı satırının sonuna videonun adresini yapıştır.
4. **Görünürlük:** Planla → 14.12.2026, 18:00 (GMT+3) → **Planla**.

## 2. Yayından sonra
- **Sabit yorum:** `youtube.md` → "Sabit yorum". Yorumlarda kanser hikâyeleri gelecektir: video "bilinmiyor" diyor; yorumlara cevap verilecekse aynı çizgide kalınır (kişisel hikâyeye saygı, nedensellik iddiasına kaynak).
- **Ölçüm:** 48. saatte (16 Aralık) `analiz/tahminler.md` → "Çernobil'in çayı" (Ç1-Ç3) ve `analiz/2026-11-23-deney-yon-promptu.md` deney tablosu (üçüncü yön videosu) doldurulur.

## Kulakla bakılacaklar (kullanıcı)
Sessizliğe dayalı cümle hizalaması kullanıldı; seslendirme kelime kelime dinlenmedi.
- **Okunuşlar:** "Taek" (TAEK), "Odtü" (ODTÜ), "Güneysu", "Çaykur", "bekerel". Sayılar seslendirme metninde yazıyla ("bin dokuz yüz seksen altı").
- **C10 (3:27)** "Eğer biz on kişinin bile öleceğine inansaydık…": müzik bu cümlede bilerek tamamen çekiliyor; ardından "Bu cümleyi aklında tut."
- **E13 (9:03)** köylülerin sorusu: müzik yine çekiliyor.
- **Müzik:** kemençe benzeri yaylı ezgi (yaprak), piyano ve kaşığın bardağa değmesi (bardak motifi), depo bölümünün altında matbaa nabzı. Özgün sentez; 703 saniyenin ~690'ında −60 dB üstü (sessiz saniyeler bilerek: C10 ve açılış).
- **Seçilen çekimler:** s00 a, s01 a, s02 b, s03 a, s04 b, s05 b, s06 a (`vo/secim.json`).
