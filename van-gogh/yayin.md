# Yayın talimatı: Van Gogh'a Kim İnandı? (uzun video)

Yükleme YouTube Studio'da bilgisayardan yapılır. Zamanlamayı YouTube yaptığı için yükleme bitince bilgisayarın açık kalması gerekmez.

## Zamanlama (Europe/Istanbul)
- **Uzun video (öneri):** 22 Aralık 2026 Salı, 18:00. Dört günde bir düzeninin sıradaki yuvası (Stanford 18 Aralık). Takvim kullanıcının; video başka güne alınırsa yalnız bu satırla ölçüm günleri değişir.
- **Ölçüm:** 48. saat 24 Aralık 18:00, 7. gün 29 Aralık. Stanford'un 48. saat ölçümü (20 Aralık) bu video yayına girmeden alınır.

## Dosyalar
| Dosya | Ne için |
|---|---|
| `teslim/vangogh_youtube.mp4` | **YouTube'a yüklenecek dosya** (9:59). 1920×1080, 30 fps, H.264 + AAC, Türkçe ses (−14 LUFS, tepe −1 dBTP), BT.709 [boyut render sonunda yazılır] |
| `teslim/vangogh_telefon.mp4` | Telefonda izlemek için küçük kopya (H.265). **Müziği telefon hoparlöründe bir kez dinle.** |
| `kapak/A.jpg` | Kapak A, "SEKİZ YIL HER AY": karanlık Paris odası, şövalede Vincent'in Hasır Şapkalı Otoportresi (tek renkli ve en parlak yer). Film bu odayla açılır (0:00); vaadi ilk dakikada (B04, her ay bir zarf) ve sonda (I01) karşılanır. İlk taslaktaki "TEK KİŞİ İNANDI" filmin iki cevabıyla çeliştiği için değişti |
| `kapak/B.jpg` | Kapak B, "651 MEKTUP": gri zarf yığınından çıkan renkli badem dalı. Vaadi 0:11'de (yığından dal uzanır) ve 4:58'de (Badem Çiçeği bütün kareyi doldurur) karşılanıyor |
| `van-gogh.tr.srt` | Türkçe altyazı (137 satır) |
| `youtube.md` | Başlık, açıklama (bölümler, kaynaklar, görsel künyesi, yapım notu), etiketler, sabit yorum |

## 1. Yükleme
1. Dosya adını `van-gogh-a-kim-inandi.mp4` yap, **Oluştur → Video yükle**.
2. **Ayrıntılar:**
   - Başlık: `Van Gogh'a Kim İnandı?`
   - Açıklama: `youtube.md` → "Açıklama" bölümünün tamamı (bölüm zaman damgaları dahil; ilk satır 0:00).
   - Küçük resim: `kapak/A.jpg`. **Test ve karşılaştır** açıksa ikinci olarak `kapak/B.jpg`. Test sürerken başlık değiştirilmez.
   - Oynatma listesi: "Kitapların Sorduğu Sorular" (mektuplar bir kitap olarak yayımlandı, 1914). İkinci seçenek "Tarihin Dönüm Noktaları".
   - Kitle: "Hayır, çocuklara özel değil".
   - Daha fazla göster: etiketler (`youtube.md`), video dili Türkçe, kategori Eğitim.
   - "Değiştirilmiş veya yapay içerik" sorusu: **Hayır**. Video gerçekçi görüntü içermiyor: yağlıboya üslubunda, yüzsüz siluetler; tablolar müzelerin kamu malı fotoğrafları. Gerçek bir kişinin sesi taklit edilmedi; mektup cümleleri anlatıcının sesinden "şunu yazar:" diye aktarılıyor. Anlatımın yapay zekâ sesi olduğu açıklamanın "Yapım" kısmında yazılı.
3. **Video öğeleri:**
   - Altyazı ekle → Dosya yükle → "Zamanlamalı" → `van-gogh.tr.srt`.
   - **Bitiş ekranı:** son 20 saniye (9:39'dan sona). Son kare tepeden bir yazı masası; üst yarıda yan yana iki sarı zarf (solda ve sağda). **Video öğesini soldaki zarfın, "Abone ol"u sağdaki zarfın üstüne koy.** Alt bant (altyazının yeri) boş. Anlatım "o zarf şimdi ekranda" diye biter.
   - **Video öğesi:** "Belirli video: Stanford: Gardiyan Olsan Zalim Olur muydun?".
   - **"Kanalda ayrıca" satırı:** açıklamadaki Stanford satırının sonuna videonun adresini yapıştır.
4. **Görünürlük:** Planla → 22.12.2026, 18:00 (GMT+3) → **Planla**.

## 2. Yayından sonra
- **Sabit yorum:** `youtube.md` → "Sabit yorum".
- **Yorumlarda beklenenler:**
  - Kulak olayı ve ölümün nedeni sorulacak. Video bilerek ayrıntı vermiyor; cevap verilecekse tek cümle ve kaynak: olaylar Van Gogh Museum'un mektup sitesinde belgeli.
  - "Hiç tablo satmadı" efsanesi: video bunu söylemiyor; 1890 Brüksel satışını "elimizdeki en kesin satış belgesi" diye veriyor.
- **Ölçüm:** 48. saatte (24 Aralık) `analiz/tahminler.md` → "Van Gogh'a Kim İnandı?" (VG1–VG3) doldurulur.

## Kulakla bakılacaklar (kullanıcı)
Seslendirme Whisper ile senaryoya karşı denetlendi; kuşkulu yerler `vo/kulak.md`'de:
- **B06 (≈1:20):** "Haziranda **üçüncü** kattaki". Whisper iki çekimde de "üç kattaki" yazdı; ses eğrisi "üçüncü" uzunluğunda.
- **G05 (≈6:16):** "**zam** ister". Whisper "zan" yazdı.
- **Okunuşlar:** Arles, Auvers, Saint-Rémy, Gauguin, Utrecht, Louvre.
- **Sessizlikler bilerek:** G09 "Vincent öldü" sonrası (≈7:06–7:10) yalnız rüzgâr; G11 lamba söndükten sonra (≈7:20–7:28).
- **Müzik:** özgün sentez, "zarf" motifi (la-do-fa-mi-do). Telefon bandında saniyelerin %87'sinde duyuluyor; kalan iki boşluk yukarıdaki sessizlikler.
