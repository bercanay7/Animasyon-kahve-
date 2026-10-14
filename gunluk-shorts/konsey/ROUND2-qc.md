# ROUND 2: Kalite kontrol uzmanı (qc)

**Read:** ROUND1-TALLY.md, ADDENDUM-01A.md, VERIFICATION.md ve 21 Tur 1 raporunun tamamı (ROUND2-* dosyaları açılmadı).

**Vote:** C
**Changed from round 1:** no
**Confidence:** medium

## 1. Vote and reason

Tur 1'deki "hibrit, ama kapı ve sürüm kilidi şartıyla" tutumum aynı; tally'deki C bu şartların yazılı hâli. A ile C arasındaki fark yalnız cilt sayısı ve sıklık güvencesi. QC için birincil mesele cilt sayısı değil kapı bütçesi. "Her gün" kapıyı aşındıran ilk şeydir ve kontrolsüz yayın benim kırmızı çizgimdir. Haftada 5 ve 3 günlük tampon kapıya zaman satın alır.

Ek 9, qa.py'nin kanca, telaffuz, kaynak ve okunurluğa bakmadığını söylüyor. Ek 3'e göre Dans ve Zanzibar'ın kare 0'ında kanca metni yok. Yani "≥2/4 videoda teknik QA geçerken içerik kusuru çıkarsa kapı zorunlu" eşiğim Tur 1'de yazdığım hâliyle karşılandı. Bu yeni bir argüman değil, eşiğin sınanması.

**Tur 2 sorularına (anayasa maddesi olarak):**
- **Cilt (G1):** tavan 3. İlk 14 günde fiilen 1 cilt. İkinci cilt ancak Titanik ortak motora taşınıp 4 eski videoya regresyon QA'sı geçerse, 8. günden sonra girer. Her videoda sürüm künyesi (motor, cilt, ses) yazılır.
- **Sıklık ve süre (G2):** haftada 5, tampon 3 gün. Tampon 1 günün altına inerse ya da kapı üst üste 3 gün 20 dk'yı aşarsa otomatik 3–4/hafta. 40 sn korunur. 25–32 sn denemesi 14. günden sonra ayrı pencerede yapılır (bkz. retention satırı).
- **Ses (G3):** erkek, yankısız (Ek 4: etkin ıslak pay ≈ %13,6). Kadın sesi yalnız kör testle girer: ≥4/5 tercih, ≤1/5 "robot", adları doğru yazma ≥%60. Dinlenmemiş ses yayınlanmaz.
- **Kapılar (G4):** kırmızıda yayın yok. Zorunlu beşi: (1) qa.py çıkış kodu 0 ve raporun kare sayısı ile dosya özeti teslim edilen videoyla eşleşiyor (Emu'da 960'a karşı 1032 vardı); (2) kare 0'da kanca; (3) `sources.md`; (4) `pron.tsv` adlarının dinlenmesi; (5) telefon hoparlöründe tek dinleme. 5 kişilik izleyici testi öneri. Bütçe: hedef 10 dk, tavan 20 dk. Bu bir tahmin (12 madde × ~50 sn); ilk 5 yayında süre loglanıp ölçülür.
- **Ölçüt (G5):** QC ölçütü, yayın sonrası hata raporu = 0 ve kapıda yakalanan kusur/video. Büyüme için kaydıran oranı ve ort. izlenme %, 48 sa ve 7 gün penceresi. Kusur sayımı düşük varyanslı olduğundan 14 videoda değerlendirilir; büyüme için kol başına ≥7 video.
- **Kanca (G6):** kare 0'da ≤9 kelime, ≥64 px, güvenli alanda; kelime ve px otomatik ölçülür. "Vaat ödenmeli" insan kapısındadır: kanca cümlesi bir `sources.md` satırına ve videodaki "ödeme anı" zaman damgasına (≤40 sn) bağlanır, yoksa kırmızı.
- **Titanik (G8):** ilk kart mutlak "kehanet" demesin ("…YAZILDI: KEHANET Mİ?"). "6 benzerlik" videoda 6 gösterilip ≥1 farkla dengelenir. Yeniden yükleme yeni video sayılır.

## 2. Response to other members

| Member | Point | Agree / disagree | Why |
|---|---|---|---|
| pipeline | Kapı = qa.py yeşil + "elle 10 sn" bakış | Kısmen karşı | 10 sn, Ek 9'un saydığı dört boşluğu (kanca, telaffuz, kaynak, okunurluk) kapatamaz. Taşıma ölçümüne (≤1 gün, ≤90 dk/video) ve qa.py çıkış kodunun bloklamasına katılıyorum. |
| sesmuh | QA eşiği: WER ≤%10 (adlar hariç) | Karşı | Ek 5: ölçüm Whisper hatasını TTS hatasından ayırmıyor. Gate'e bozuk ölçüt konmaz; yerine `pron.tsv` dinleme kontrolü konur. Ducking ≥14 dB ve kodlama sonrası ölçüm kuralına katılıyorum. |
| retention | 40 sn → 25–32 sn ve ilk 14 günde kanca testi | Karşı (zamanlama) | İki değişken aynı pencerede, kendi tek-değişken ilkesine aykırı. Süre 14. günden sonra. Ayrıca onun ≤4 kelime ile kanca'nın ≤9 kelimesi arasında tek sayı gerek: ≤9 sert sınır. |
| olgu | Her iddia için 2 bağımsız kaynak | Kısmen | Kapıyı destekliyorum. Ama VERIFICATION §0'a göre hiçbir sayfa okunamadı, yalnız arama özeti görüldü. `sources.md`'de "sayfa okundu" ile "arama özeti" ayrı işaretlenmeli. Maddi sayı, yıl ve nedensellik için 1 birincil ya da 2 ikincil. Gerisi niteleyerek söylenir. Aksi hâlde 10 dk bütçesi tutmaz. |
| analitik | Yayın günlüğü, sabit pencere, yeniden yükleme = yeni video | Katılıyorum, ekliyorum | Günlüğe QC alanları da girsin: kapıda yakalanan kusur, kapı süresi, sürüm künyesi. Böylece "hangi kontrol gerçekten bir şey yakaladı" sorusu (kartımdaki soru) ilk kez cevaplanır. |
| seytan | Tek cilt, haftada 4–5, atlanan gün başarısızlık değil | Çoğunda katılıyorum | Frekansa ve "kapı kırmızıysa gün atlanır"a evet. Cilt sınırına evet, 14 gün tek cilt (sınırlı) olarak. "Hiçbir şey 14 gün yok" tarafına hayır: kapı ve kanca zorunluluğu bekleyemez, çünkü maliyeti ölçülmüş kusurlar. |

## 3. Corrections accepted or disputed

- **Ek 9:** kabul. Anayasaya "qa raporu teslim dosyasına bağlı" maddesi girer. LUFS ölçümü `audio.py`'de olduğundan kapı listesinde ayrıca işaretlenir.
- **Ek 3:** kabul. Kare 0 kontrolü otomatik (OCR/kutu ölçümü) yapılabilir ve ilk uygulaması Dans ve Zanzibar'ı kırmızıya alırdı.
- **Ek 10:** kabul, açık kalıyor. HUD (y≈260) üst arayüz bandına girebilir. renktipo'nun 290/672/200 px şeritleri üçüncü taraf kaynaklı ve doğrulanmamış: **varsayım**. Gizli (unlisted) bir test yüklemesinin telefon ekran görüntüsüyle doğrulanana dek kural "geçici" etiketlenir.
- **Ek 5:** kabul. WER yalnız bir ipucu; sertleştirilmiş eşik olarak kullanılamaz.

## 4. What would reverse this vote

- **→ A (tek cilt, 14 gün):** Titanik'in motora taşınması 3 günü aşarsa ya da regresyon QA'sı geçmezse. İkinci cilt güvenle eklenemez.
- **→ daha seyrek yayın (3–4/hafta):** kapı ilk 5 yayında ortalama 20 dk'yı aşarsa.
- **→ kapıyı hafifletirim (≤5 dk):** 14 günde hiçbir kapı maddesi gerçek bir kusur yakalamazsa (kartımdaki değişim koşulu). Bu, Ek 3 ve 9'un bugünkü bulgularıyla çelişir; bu yüzden olası görmüyorum.

## 5. Dissent to record

none. Not: kapı bütçesi aşılırsa feda edilen şey kalite değil sıklık olmalı. Bu madde anayasada "otomatik düşüş kuralı" olarak yazılmazsa kapı baskı altında sessizce gevşer.
