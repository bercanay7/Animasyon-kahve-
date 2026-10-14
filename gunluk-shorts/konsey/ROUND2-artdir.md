# ROUND 2: Art director (artdir)

**Read:** ROUND1-TALLY.md, ADDENDUM-01A.md, VERIFICATION.md ve 21 Tur 1 raporunun tamamı (ROUND2-* açılmadı).

**Vote:** C
**Changed from round 1:** yes: pipeline raporu (3 günlük tampon, "ortak motor yokken üçüncü cilt yok") ve analitik raporu (tek eksen, hücre başına en az 7 video). Tur 1'de tally beni B'ye yakın saydı. Kendi şartım ("ui.py ve cues.py ortak motora çekilmeden üçüncü cilt yok") günlük tempoyla çakışıyor; C bu şartı kuruyor.
**Confidence:** medium

## 1. Vote and reason

Tanınabilir imza koltuğumun önceliği. Ek 01A madde 3 şunu gösterdi: Dans'ta kanca metni yok, Emu'da büyük skor tabelası var. Dans'ın 100 izlenmesini ciltten çok kancaya bağlamak daha makul, ama bu tek çift, kanıt değil. Cilt etkisi 14 günde okunamaz (analitik: ~45 video/hücre gerekir). Bu yüzden "tek cilt mi, iki cilt mi" bir veri sorusu değil, kimlik ve üretim sorusudur. İki cilt kullanıcının isteğini taşır, A'nın "varsayılan cilt" seçme riskini almaz.

**G sorularına yanıtım (anayasa maddesi):**
- **Cilt tavanı: 3.** İlk 14 gün: 2 cilt, **kara kalem + blueprint**, ikisi de 24 fps. Kâğıt kesme (12 fps hilesi) sonra gelir. Bu bir üretim sıralamasıdır, Dans'a verilmiş hüküm değildir.
- **Yeni cilt:** mevcut cilt ≥5 videoda kullanılmış VE ortak motor sürümü kilitlenmiş olacak. Cilt = yalnız `art.py` + palet; ≤90 dk.
- **Sıklık:** haftada 5, 3 günlük tampon (pipeline). Tampon 1 güne inerse otomatik 3–4/hafta.
- **Cilt kararı eşiği:** hücre başına ≥7 video, konu türü aynı, medyan "viewed" oranı farkı ≥10 puan. Tur 1'deki "≥4 video" şartımı geri çekiyorum (analitik haklı).
- **Kanca kartı (soru 6):** ≤6 kelime, ≥64 px, en çok 2 satır, kare 0'dan itibaren, güvenli alanda. Gerekçe: 64 px'te 9 kelime 3 satıra çıkar ve ana nesneyi sıkıştırır (tahmin; Pillow ölçümüyle doğrulanacak). Vaat 10 sn içinde ödenir, kontrolü olgu/kanca koltuklarında.
- **Görsel kapı (soru 4, toplam 10–15 dk bütçenin ~3 dk'sı):** 270×480'de silüet testi, güvenli alan şablonu çakışması, Türkçe glif satırı (İ ı Ş Ğ).
- **Titanik kartı (soru 8):** kartta "kehanet" sözcüğü yok, ≤6 kelime. Metni olgu ve kanca koltukları yazar.

## 2. Response to other members

| Member | Point | Agree / disagree | Why |
|---|---|---|---|
| buyume | 14 gün tek imza, blueprint öneriyor ("Titanik'te zaten var") | Kısmen | Tanınırlık ve "Dosya #N" seri adı: katılıyorum. Seçim gerekçesi kolaylık; Emu'yu blueprint ile anlatmak zor. Ayrıca ">%30 geri kalma" eşiği n=14'te gürültüdür. |
| analitik | Tek eksen, hücre başına ≥7, ham izlenme yok | Katılıyorum, bir yerde karşı | Cilt-konu eşlememin cilt ile konuyu birbirine bağladığı doğru; bu yüzden 14 günde cilt etkisi iddia etmiyorum. Ama cildi dondurmak da veri almaz: tek hücre, karşılaştırma yok. |
| pipeline | Tavan 4, belki 6; motor + veri dosyası | Motor: evet. Tavan: hayır | 6 cilt, kanal sayfasında A'nın yeniden etiketlenmiş halidir. Tavan 3. "14 günde bir yeni cilt" ile benim "≥5 video" şartımdan hangisi yavaşsa o geçerli. |
| renktipo | Üst ≥290, alt ≥672, sağ ≥200; içerik 840×960 merkezde | Kısmen | Üst ve sağ: iki kaynak da 241–288 / 192–201 diyor, benimsiyorum, HUD y≈260 yukarı alınacak. Alt 672 yalnız bir reklam şartnamesine dayanıyor (organik doğrulanmadı); uygulanırsa tuval 960 px yüksekliğe iner ve kanca kartı, ana nesne, HUD, altyazı sığmaz. Alt sınırı sizin Pillow şablon testiniz belirlesin. |
| illustrator | Silüet testi, ≥9 px çizgi, ana nesne ≥%35, köşede küçük Kurye | Çoğuna evet | Silüet testi ve 3 poz kuralı anayasaya girsin. Köşe Kurye'ye hayır: 270×480'de okunmaz, sağ/alt arayüz bölgesine düşer. Kurye HUD sayacının parçası olsun. |
| kanca | ≤9 kelime kanca | Hayır | Bkz. ≤6 kelime gerekçesi. |

## 3. Corrections accepted or disputed

- **Ek 01A madde 3 (ilk kareler): kabul.** Tur 1'deki "Dans'ta kanca yoktu" tahminim doğrulandı. Ama E1 tek çifttir.
- **Madde 10 (güvenli alan açığı): kabul.** V1'deki "HUD y geçici" notumu şuna çeviriyorum: HUD yukarıdaki bölgeden çıkarılana ve şablonla doğrulanana kadar yayın şartı.
- **Madde 1 (metrik): kabul.** Cilt kararında yalnız "viewed" oranı ve ortalama izlenme % kullanılır.

## 4. What would reverse this vote

- Studio'da kancalı videolar (Emu, Titanik) ile kancasız (Dans) arasında kaydıran farkı yoksa, kanca önceliği düşer ve cilt tartışması geri açılır.
- Ortak motora taşıma (Titanik, pipeline'ın ölçümü) >3 gün sürerse B'ye değil A'ya (tek cilt) dönerim: cilt maliyeti çeşitliliği satın alamaz.
- 5 kişilik 270×480 testinde iki cilt de <3/5 çıkarsa tek okunur cilde kilitlerim.
- 14. günde iki cildin "viewed" medyanı arasında ≥10 puan fark ve her hücrede ≥7 video varsa, kazanan cilde (B-tek cilt) yaklaşırım. Fark görünmezse 2→3 cilt, iskelet kalıcı.

## 5. Dissent to record

Oyum çoğunluk çizgisinde (iskelet sabit, cilt kısıtlı); azınlık itirazım yok. Kayda geçsin diye bir çekince: A kazanırsa 14 günlük tek cilt, blueprint'e "Titanik'te hazır" diye değil, 270×480 silüet testinin sonucuna göre seçilmelidir. Kolaylık nedeniyle seçilen cilt, kanalın görsel kimliğini veri olmadan belirler. Cilt-konu eşlemesi yazılı kalmalı; yoksa çeşitlilik rastgeleliğe döner (benim kırmızı çizgim).
