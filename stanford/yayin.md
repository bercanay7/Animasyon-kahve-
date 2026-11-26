# Yayın talimatı: Stanford Hapishane Deneyi (uzun video)

Yükleme YouTube Studio'da bilgisayardan yapılır. Zamanlamayı YouTube yaptığı için yükleme bitince bilgisayarın açık kalması gerekmez.

## Zamanlama (Europe/Istanbul)
- **Uzun video (öneri):** 18 Aralık 2026 Cuma, 18:00. Dört günde bir düzeninin sıradaki yuvası (Çernobil'in Çayı 14 Aralık). Takvim kullanıcının; video başka güne alınırsa yalnız bu satırla ölçüm günleri değişir.
- **Ölçüm:** 48. saat 20 Aralık 18:00, 7. gün 25 Aralık. Çernobil'in 48. saat ölçümü (16 Aralık) bu video yayına girmeden alınır.

## Dosyalar
| Dosya | Ne için |
|---|---|
| `teslim/stanford_youtube.mp4` | **YouTube'a yüklenecek dosya** (11:53, 360 MB). 1920×1080, 30 fps, H.264 iki geçiş 3,8 Mbps + AAC 256k, Türkçe ses (−14,2 LUFS, tepe −1,3 dBFS), BT.709. CRF 18 render 1,05 GB'tı (monitör greni); teslim bit hızıyla küçültüldü |
| `teslim/stanford_telefon.mp4` | Telefonda izlemek için küçük kopya (93 MB; H.265 iki geçiş 900k, AAC 128k). **Müziği telefon hoparlöründe bir kez dinle.** |
| `kapak/A.jpg` | Kapak A, "RASTGELE SEÇİLDİ" (vurgu "RASTGELE", altın #E2B04F: görüntüde renkli nesne yok). Kapak sistemine uyduruldu (26 Kasım): yazı sol üstte, aynalı gözlüklü gardiyan sağda (eski kapağın aynası); koridor gölgede, tavan lambaları kısık; tek odak camdaki çapraz parıltı (oval beyaz değil). Vaat filmde: aynı figür P02'de 0:04'te, "rastgele gardiyan seçilmiş bir öğrenci" A01'de 0:07'de |
| `kapak/B.jpg` | Kapak B, "BANTTA NE İSTENDİ?" (vurgu "İSTENDİ?", kayıt lambasının kırmızısı #B92D22: görüntüdeki tek renkli nesne). Kapak sistemine uyduruldu (26 Kasım): yazı sol üstte, teyp sağda ve süre rozetinin üstünde; spotun kaynağı kadraj dışında, en parlak bölge teybin ışık alan yüzü. Yazının arkası soldan koyulaştırıldı (27 Kasım, Fable bulgusu): kırmızı satır gri değerde zeminden ayrılmıyordu (yerel fark +17); şimdi kırmızı L 85, arkası L 29 (+56), koni ve teyp aynı. Yedek başlık ("…Bantta Gardiyandan Ne İstendi?") seçilirse bu kapak başlığı tekrar eder: o durumda B kullanılmaz. Vaat filmde: teyp ve yanan lamba P01T'de 0:03'te; "bir ses bandı… ondan bir şey istiyor" A02'de 0:18–0:26; bantta istenen III. bölümde (4:21) |
| `stanford.tr.srt` | Türkçe altyazı (177 satır) |
| `kapak/test/` | Kapak test seti (`araclar/kapak/test_seti.py`): `A_test.jpg`/`B_test.jpg` sayfaları ve `.txt` ölçümleri; yazısız sürümler `kapak/A_yazisiz.jpg`, `kapak/B_yazisiz.jpg`; aşağıdaki nota bakın |
| `youtube.md` | Başlık, açıklama (bölümler, kaynaklar, yapım notu, gün çelişkisi), etiketler, sabit yorum |
| `fable_son_okuma/` | Fable'ın bağımsız son denetimi ve başkanın doğrulaması (ne neden değişti) |

**Kapak testi notu (26 Kasım, kapak sistemi):** İki kapakta yazı kutusu solda (A x%4–%51, B x%4–%55), üstte (y%7–%59 / %55), 2 satır, harf yüksekliği karenin %20,1'i (Bebas 300 px), rozete binen yazı pikseli 0. Yazı hariç en parlak bölge A'da gözlük camlarının arası (x%75 y%44: iki çapraz parıltı), B'de teybin yüzü (x%80 y%56). B'de yazı/zemin farkı +131 (27 Kasım, sol koyulaştırmadan sonra; önce +90), harf yüksekliği %19,6. Isı haritasının ilk tepesi iki kapakta da yazı (2./1. oran .81 ve .87); Bebas büyük harflerinin kenarları bu ölçümde hep öne çıkıyor, figür ve teyp ikinci tepede. A'da süre rozetinin altında yalnız gardiyanın koyu omzu ve yakası, B'de ışık konisinin zemine düşen kısmı var; önemli öğe yok. Kararı "Test ve karşılaştır" verir.

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
   - **Bitiş ekranı:** son 20 saniye (11:33'ten sona). Son kare karanlık gözlem odası: sol üstte küçük monitör (koridorda eşikte duran gardiyan), ortada ışık konisinin altında teyp, masada aynalı gözlük. **Sağ yarı ve alt üçte bir boş ve koyu.** Video öğesini sağ üste, "Abone ol"u sağ alta koy; sol üstteki monitörü kapatmasın. Anlatım 11:31'de biter; son 20 saniyede makaralar döner, kayıt lambası yanar, ekranda yazı yok.
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
- **F03 (≈10:42) "Peki.":** Mark'ın müdürün son isteğine cevabı. Önünde ve arkasında müzik susuyor; ardından çözülmeyen bir akor, sonra müdürün notu (F03b). Kelimenin tek başına, nefesle duyulması gerek.
- **Yama cümleleri (rev3, 25 Kasım):** D15 (≈6:37), E07–E08 (≈8:24–8:56), E12 (≈9:29), F02–F03b (≈10:20–11:09) ayrı çekimden; düzeyleri eski cümlelere eşitlendi. Geçişlerde ton ya da oda sesi farkı duyulursa söyle.
- **F04 (≈11:11):** "Gardiyan olsan…" eski çekimden; önündeki cümle kesildi. Başında nefes ya da kesik hece duyulursa söyle.
- **Müzik:** baştan sona bant cızırtısı ve floresan uğultusu (120 Hz); sayım motifi (Re–Fa–La–Sol); bant bölümünün altında teyp motoru. Özgün sentez; 672 saniyenin 661'inde −60 dB üstü (sessiz saniyeler bilerek: C10 ve F03 çevresi).
- **Seçilen çekimler:** s00 a, s01 b, s02 b, s03 b, s04 b, s05 b, s06 a, s07 b (`vo/secim.json`); yamalar r1 a, r2 a, r3 b, r4 a (`vo/yama/secim.json`). İki çekim arasında ölçülebilir kusur farkı yoktu; tempo için kısa olanlar seçildi.
- **Müzik telefonda (kullanıcının isteği, 25 Kasım):** ilk mikste tonlu müzik telefon hoparlöründe (300 Hz altı yok) saniyelerin yalnız %45'inde duyuluyordu; bant bölümü iki dakika yalnız cızırtıydı. Dronların notası oktavla telefon bandına taşındı, bant bölümüne ince bir zemin eklendi. Şimdi %82; 5 sn'yi aşan sessizlikler bilerek: "Buna bakamıyorum" ve "Peki." (`tools/muzik_denetim.py`). Telefonda bir kez dinlenmesi iyi olur.
