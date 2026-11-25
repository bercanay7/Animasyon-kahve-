# Yayın talimatı: Stanford Hapishane Deneyi (uzun video)

Yükleme YouTube Studio'da bilgisayardan yapılır. Zamanlamayı YouTube yaptığı için yükleme bitince bilgisayarın açık kalması gerekmez.

## Zamanlama (Europe/Istanbul)
- **Uzun video (öneri):** 18 Aralık 2026 Cuma, 18:00. Dört günde bir düzeninin sıradaki yuvası (Çernobil'in Çayı 14 Aralık). Takvim kullanıcının; video başka güne alınırsa yalnız bu satırla ölçüm günleri değişir.
- **Ölçüm:** 48. saat 20 Aralık 18:00, 7. gün 25 Aralık. Çernobil'in 48. saat ölçümü (16 Aralık) bu video yayına girmeden alınır.

## Dosyalar
| Dosya | Ne için |
|---|---|
| `teslim/stanford_youtube.mp4` | **YouTube'a yüklenecek dosya** (11:11). 1920×1080, 30 fps, H.264 + AAC, Türkçe ses (−14,2 LUFS, tepe −1,5 dBFS), BT.709 |
| `teslim/stanford_telefon.mp4` | Telefonda izlemek için küçük kopya (H.265 iki geçiş 900k, AAC 128k) |
| `kapak/A.jpg` | Kapak A, "RASTGELE SEÇİLDİ": koridorda aynalı gözlüklü gardiyan, ¾ baş, camda tek parıltı. Filmin ilk planıyla aynı figür; vaadi A01'de, ilk 5 sn'de karşılanıyor |
| `kapak/B.jpg` | Kapak B, "BANTTA NE İSTENDİ?": karanlık masada teyp, kırmızı kayıt lambası. Teyp ilk 5 sn'de (P01T) görünüyor, vaadi III. bölümde (4:21) karşılanıyor |
| `stanford.tr.srt` | Türkçe altyazı (168 satır) |
| `kapak/test/` | Kapak odak ölçümü (`araclar/kapak/odak.py`); aşağıdaki nota bakın |
| `youtube.md` | Başlık, açıklama (bölümler, kaynaklar, yapım notu, gün çelişkisi), etiketler, sabit yorum |
| `fable_son_okuma/` | Fable'ın bağımsız son denetimi ve başkanın doğrulaması (ne neden değişti) |

**Kapak odak notu:** İki kapakta da ısı haritasının ilk tepesi yazı (A'da oran .78, B'de .71); figür ve teyp ikinci tepede. Bebas Neue büyük harflerinin kenarları bu ölçümde hep öne çıkıyor. Yazı figürle çakışmıyor, renkler kâğıt tonunda tutuldu; kapak bu hâliyle bırakıldı. Kararı "Test ve karşılaştır" verir.

## 1. Yükleme
1. Dosya adını `stanford-gardiyan-olsan-zalim-olur-muydun.mp4` yap, **Oluştur → Video yükle**.
2. **Ayrıntılar:**
   - Başlık: `Stanford: Gardiyan Olsan Zalim Olur muydun?`
   - Açıklama: `youtube.md` → "Açıklama" bölümünün tamamı (bölüm zaman damgaları dahil; ilk satır 0:00).
   - Küçük resim: `kapak/A.jpg`. **Test ve karşılaştır** açıksa ikinci olarak `kapak/B.jpg`. Test sürerken başlık değiştirilmez.
   - Oynatma listesi: "Tarihin Dönüm Noktaları".
   - Kitle: "Hayır, çocuklara özel değil".
   - Daha fazla göster: etiketler (`youtube.md`), video dili Türkçe, kategori Eğitim.
   - "Değiştirilmiş veya yapay içerik" sorusu: **Hayır**. Video gerçekçi görüntü içermiyor; yüzsüz, stilize bir animasyon. Kimsenin sesi taklit edilmedi: sözler anlatıcının sesinden ve "Müdür:", "Mark'ın cevabı:" diye anılarak aktarılıyor. Anlatımın yapay zekâ sesi olduğu açıklamanın "Yapım" kısmında yazılı.
3. **Video öğeleri:**
   - Altyazı ekle → Dosya yükle → "Zamanlamalı" → `stanford.tr.srt`.
   - **Bitiş ekranı:** son 20 saniye (10:51'den sona). BITIS_EKRANI
   - **Video öğesi:** "Belirli video: Çernobil'in Çayı". Bir önceki video; biri iyi bir gerekçeyle "korkma" diyor, burada biri iyi bir gerekçeyle sertlik istiyor.
   - **"Kanalda ayrıca" satırı:** açıklamadaki Çernobil satırının sonuna videonun adresini yapıştır.
4. **Görünürlük:** Planla → 18.12.2026, 18:00 (GMT+3) → **Planla**.

## 2. Yayından sonra
- **Sabit yorum:** `youtube.md` → "Sabit yorum".
- **Yorumlarda beklenenler:**
  - "Deney sahteydi" ve "insan doğası budur" diye iki kamp çıkacak. Video ikisine de hüküm vermiyor; cevap verilecekse aynı çizgide kalınır: iki taraf da kendi belgesini gösteriyor, belge isteyene künye verilir.
  - Kişiler hakkında (Eshelman, Mark, Jaffe) söz eklenmez; yalnız yayımlanmış sözleri aktarılır.
- **Ölçüm:** 48. saatte (20 Aralık) `analiz/tahminler.md` → "Stanford Hapishane Deneyi" (ST1–ST3) ve `analiz/2026-11-23-deney-yon-promptu.md` deney tablosu doldurulur. ST1'in çıtaları 18 Aralık'tan önce Studio verisiyle kilitlenir (tahminler dosyasındaki not).

## Kulakla bakılacaklar (kullanıcı)
Cümle hizalaması sessizlikten yapıldı; seslendirme kelime kelime dinlenmedi.
- **Okunuşlar:** "Ceffi" (Jaffe), "Eşelmın" (Eshelman), "Lö Teksiye" (Le Texier), "Tibo", "Deyvid", "Deyv", "Filip", "Con Ueyn" (John Wayne), "Con Mark", "Erih Fromm", "dört yüz on altı".
- **Konuşan etiketleri:** III. bölümde "Mark'ın cevabı:" ve "Müdür:" sözlerin önünde duyuluyor mu; iki ses tek anlatıcıdan çıktığı için bu etiketler şart.
- **C10 (≈3:36) "Buna bakamıyorum":** müzik bu cümlede bilerek çekiliyor.
- **F03 (≈10:18) "Peki.":** bandın son kelimesi. Önünde ve arkasında müzik susuyor; ardından çözülmeyen bir akor. Kelimenin tek başına, nefesle duyulması gerek.
- **Müzik:** baştan sona bant cızırtısı ve floresan uğultusu (120 Hz); sayım motifi (Re–Fa–La–Sol); bant bölümünün altında teyp motoru. Özgün sentez; 672 saniyenin 661'inde −60 dB üstü (sessiz saniyeler bilerek: C10 ve F03 çevresi).
- **Seçilen çekimler:** s00 a, s01 b, s02 b, s03 b, s04 b, s05 b, s06 a, s07 b (`vo/secim.json`). İki çekim arasında ölçülebilir kusur farkı yoktu; tempo için kısa olanlar seçildi.
