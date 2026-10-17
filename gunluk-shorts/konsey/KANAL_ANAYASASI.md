# ZAMAN KURYESİ: KANAL ANAYASASI (v1, 2026-10-14)

Kaynak: 21 koltuklu danışma kurulu, 2 tur, 1 doğrulama. 16/21 oyla **Seçenek C**. Gerekçeler ve muhalefet: `RECOMMENDATION.md`. Ham tartışma: `ROUND1-*.md`, `ROUND2-*.md`.
**Bu belge şunu söyler: bundan sonraki her video bu kurallara göre yapılır.** Kullanıcı değiştirmediği sürece geçerlidir. Sayısal eşiklerin çoğu **varsayımdır**; ilk 14 videonun verisiyle yeniden yazılır (bölüm 9).

## 0. Üç kullanıcı kararı (konseyin önerisi; karar sizin)

1. **Sıklık:** Konsey **haftada 5 video + 3 günlük tampon** öneriyor; "her gün" değil. Gerekçe: günlük baskıda telaffuz, kaynak ve telefon dinlemesi ilk atlanan adımlar. (Muhalif: buyume günlük + tampon istiyor; seytan haftada 4–5.)
2. **Cilt:** Konsey ilk 14 videoda **2 cilt, yazı-tura ile atanmış** öneriyor. (Muhalif: 4 koltuk 1 cilt dondurmak istiyor.)
3. **Kadın sesi:** Konsey **erkek ses, kuru** ile başlamayı; kadın dönüşümünü yalnız kör testi geçerse kullanmayı öneriyor.

## 1. Kimlik: sabit iskelet + değişen cilt

**Sabit (her videoda aynı):**
- Kare 0'da kanca kartı (bölüm 3), kart = son kare, açık döngü, son 0,1 sn sessiz.
- Tek yazı ailesi, tek altyazı biçimi ve yerleşimi, tek vurgu rengi; altyazı ≥56 px, tüm yazı ≥44 px (HUD dahil); kontrast ≥4,5:1; Türkçe karakter satırı (İ ı Ş Ğ Ç Ö Ü) kontrol edilir.
- HUD sayacı (y≈260; telefon denemesine kadar kart içeriği y 290–1250 bandında).
- Ortak motion kiti: 3 easing eğrisi, video başına ≤2 sarsıntı ve ≤1 flaş, hiçbir kare 3 sn'den uzun durağan değil, her 2–3 sn'de görsel değişim, son 0,5 sn ilk kareye easing ile kapanır.
- Tek anlatıcı ses (bölüm 4) ve tek ses/müzik paleti (96 BPM; 1 ölçü = 2,5 sn = 60 kare; ≤8 sabit efekt).
- Üç yayın kapısı (bölüm 5) ve yayın günlüğü.
- Süre: ilk 14 videoda **40 sn ±3**, metin ≤90 sözcük (≈2,6 sözcük/sn; ekran sözcüğü ölçümü: Emu 92, Dans 78, Titanik 77).

**Değişen:** yalnızca illüstrasyon "cildi" (palet + `art.py`; ortak motoru değiştirmez).

## 2. Cilt kuralları

- **Tavan 3:** kara kalem, blueprint, kâğıt kesme. Düz vektör (Zanzibar) bir cilt sayılmaz; ortak tabandır.
- **İlk 14 video: 2 cilt (kara kalem + blueprint).** Hangi videonun hangi cildi aldığına **yazı-tura** karar verir; konu türleriyle çaprazlanır (her cilt her konu türünde görünür). Cilt-konu eşlemesi (ör. blueprint = teknik) en erken 15. videoda başlar.
- **Kâğıt kesme** yalnız tek kahraman/nesne sahnesinde (kalabalık açılış yasak; Dans'ın kanca sorunu).
- **Yeni cilt:** mevcut cilt ≥5 videoda kullanılmış, ortak motor sürümü kilitli, ek maliyet ≤90 dk ve ilk karesi 270×480'de 5 kişiden ≥4'ü tarafından doğru adlandırılmış olmalı. Her seferinde tek cilt eklenir.
- **Çizim:** ana nesne yüksekliğin ≥%35'i veya genişliğin ≥%60'ı; çizgi ≥9 px; 4 renk + 1 vurgu; karakter başına ≤3 poz.
- **Geri alma:** cilt tavanı 30. günde ızgara testiyle sınanır: telefonda son 9 video, 5 kişi, 2 sn; 4/5 "aynı kanal" demezse tavan 2'ye iner.

## 3. Kanca kuralları (ilk 3 saniye)

- **Kare 0'da kart (= kapak = son kare):** ≤6 kelime (≤40 karakter), ≥64 px, ≤3 kısa satır (Türkçe sözcükler eş aralıklı yazıda ≥64 px'te iki satıra sığmıyor; v1'de ≤2 yazılmıştı, Titanik'te ölçüldü), giriş animasyonu yok (kare 0'da tam kurulmuş), güvenli alanda; en çok 5 öğe. Kart özne+olay söyler ("ORDU 0 – EMU 1" tipi).
- **Ses:** ilk sesli söz ≤0,5 sn; ilk cümle ≤9 kelime ve ≤3,5 sn; kare 0'da tek imza vuruşu ≤0,25 sn.
- **Vaat ödenir:** kanca cümlesindeki her sayı/iddia videoda gösterilir; vaadin ödendiği saniye ≤30 (en çok 35) ve kaynak dosyasına yazılır.
- **Kanca üretimi:** her video için 3 aday yazılır (~15 dk), biri seçilir. Kanca türleri iki: **R** (rakam/çelişki), **S** (soru/merak). İlk 14 videoda tür yazı-tura ile atanır.
- **Kanca kapısı (3 dk, evet/hayır):** ≤6 kelime · 270×480'de okunuyor · yazı ile ses aynı vaadi veriyor · her sayı/iddia videoda ödeniyor ve olgu onaylı · HUD/güvenli alan çakışması yok.
- **Titanik "kehanet" tuzağı:** kanca videonun söylemediğini vaat etmez; soru biçimi serbest, mutlak ifade yasak.

## 4. Ses kuralları

- **Anlatıcı:** tek erkek ses (Piper dfki), **kuru: yankı (ıslak pay) = 0** (kullanıcı yankıdan şikâyet etti; eski sürümde etkin ıslak pay ≈%13,6 ölçüldü). Videoya göre ses ayarı yok; tüm parametreler sürümlü tek ses dosyasında.
- **Kadın sesi (WORLD dönüşümü):** yayına yalnız şu kör testi geçerse girer: aynı metin, telefon hoparlörü (%50) ve kulaklık, 7 dinleyici, ≥6/7 tercih ve ≤1/7 "robot", yabancı adlarda erkekten en çok 5 puan kötü, s/ş/ç netliği bozuk değil. Test yapılmadıysa erkek ses. Ses kimliği değişirse 30 gün sabit kalır.
- **Yankı geri açma:** kör testte 3/5 yankılı sürümü seçerse en çok %5 ıslak pay.
- **Miks:** kodlanmış mp4 üzerinde −14 LUFS ±1; true peak ≤ −1 dBTP; ilk/son örnekte tık ve DC yok; müzik+efekt konuşma sırasında konuşmadan ≥16 dB aşağıda (≤14 dB QA hatası; ducking çarpanı ≈0,85); konuşma yokken müzik −10 dB'e çıkabilir.
- **Müzik:** tek ortak palet; videoya özel beste yok; ilk 14 videoda yatağın tonu ve motifi sabit. Kare 0–3 sn arası yatak yok ya da çok düşük, yatak 3. sn'de girer.
- **Telaffuz:** sözlükte olmayan özel ad/yıl/sayı varsa render yapılmaz (aşağıda kapı 2).
- **Sessiz video yok:** her video seslendirmelidir.

## 5. Yayın kapıları (kırmızıda yayın yok)

**Toplam hedef ≤20 dk/video (otomatik kısım 0 dk insan; insan kısmı tek oturum ≤15 dk).** Aşan günde **sıklık düşer, kapı gevşemez** (aşağıda 5.5).

1. **Kaynak kapısı (olgu).** `sources.md` olmadan `qa.py` çıkış kodu ≠ 0. Her sayı/yıl/ad için 1 birincil veya 2 bağımsız kaynak. Tek tarafın öz-bildirimi ("komutanın raporuna göre") nitelenir ve **sesle söylenir**. Kaynaksız mutlak sözcük yasak: "tek", "ilk", "en kısa", "kehanet", "batmaz". Kancadaki iddia kaynak tablosunun 1. satırıdır. Kaynak doğrulaması render gününde değil konu seçiminde yapılır; havuzda ≥5 doğrulanmış konu bulunur.
2. **Türkçe/telaffuz kapısı (dil; ≤8 dk).** Ekran metni ile okunuş metni ayrı (`göster=söylenen`); sayı/yıl harfle yazılır; sözlükte olmayan her özel ad ve her sert/ğ'li sözcük için **10 sn kulak kontrolü** (sözlük girdisini Whisper değil insan kulağı onaylar); video başına ≤3 sayı; cümle ≤14 kelime; Türkçe-duyarlı küçük/büyük harf (`.lower()` ve `.upper()` doğrudan yasak; `İ/I` testi).
3. **Kalite kapısı (qc; otomatik + ≤10 dk).** `qa.py` çıkış kodu 0 ve raporun kare sayısı/dosya özeti teslim edilen videoyla eşleşir; kare 0'da kanca; ilk ses ≤0,5 sn; telefon hoparlöründe baştan sona tek dinleme (anlaşılmayan kelime 0); kodlanmış mp4'te LUFS/peak; `freezedetect`; güvenli alan/HUD; her video için sürüm künyesi (motor, cilt, ses, `pyworld` sürümü).
4. **Metin kapısı (seo; ≤3 dk).** Başlık ≤60 karakter, ilk ~40 karakterde vaat; **başlık anahtar sözcükleri arama niyeti açısından kontrol edilir** (Dans'ın "kadın dansa başladı" başlığı "dans eden kadın", "sırf kadın" gibi yanlış niyetli aramaları getirdi; YouTube arama önerilerinde başlığın ana sözcüklerini yazıp çıkan önerilere bakın); başlık ve kart videonun söylediğinden fazlasını vaat etmez; açıklama: 1. satır vaat + seri etiketi ("TESLİMAT #N"), 2. satır tek kaynak, sonra 3 hashtag; sabit yorum = kaynak + tek açık soru. Yayın saati ilk 14 videoda sabit.
5. **Otomatik düşüş kuralı:** kapı bütçesi üst üste 3 gün 20 dk'yı aşarsa veya tampon 1 günün altına inerse yayın otomatik **haftada 3–4**'e düşer.
6. **Doğrulama sonrası:** yayınlanmış videoda hata bulunursa video silinmez (analitiği sıfırlar); sabit yorumda düzeltme yapılır. Yeniden yüklenen video yeni video sayılır.

## 6. Üretim hattı

- **Ortak motor** (`engine.py`, `compose.py`, `contact.py`, `render.py` zaten aynı) tek sürüme kilitlenir; cilt = `art.py` + palet; `ui.py`, `cues.py`, `audio.py` ortak şablona çekilir. Yeni cilt ancak motor kilitliyken eklenir.
- **Tek `voice.json`** (model, `reverb_wet=0.0`, sürüm). Kadın WORLD adımı video başına ≤+5 dk ve `pyworld` sürümü kilitli.
- **Hedef:** video başına ≤90 dk (TTS beklemesi hariç). **Yayın günlüğü** (motor hash, cilt, ses, kanca türü, metrik, tarih) `jsonl` olarak otomatik yazılır.
- **Tampon:** ≥3 videoluk tampon kurulunca haftada 5; kurulana kadar haftada 3–4.
- **Süre/kelime:** 40 sn şablonu ≤90 sözcük; 30 sn (12 ölçü = 720 kare) şablonu sonra tek değişken olarak sınanır (≤65 sözcük).

## 7. Başlık, açıklama, kapak, topluluk

- **Seri adı:** "TESLİMAT #N" (yalnız açıklamanın 1. satırı; ekranda/HUD'da sabit yazı olarak yer almaz, bkz. §12-8). Başlık Shorts'ta "vaat sözleşmesidir"; arama ağırlığı Studio trafik kaynağı verisine göre belirlenir (Shorts akışı ≥%90 ise anahtar kelime çalışması kapanır; arama+önerilen ≥%20 ise açılır).
- **Kapak = tasarlanmış ilk kare** (ayrı kapak emeği yok). Kapak/ızgara trafik payı <%10 ise bu konu kapanır.
- **Sabit yorum her videoda:** kaynak + tek açık soru; **24 saatte cevap** ve düzeltme kuralı (%100); ses/stil deneyleri izleyiciye açıkça söylenir; ses sorunu yorumların ≥%30'unu oluşturursa ses önceliği öne çekilir.

## 8. Ölçüt ve karar kuralları (ön-kayıtlı)

- **Birincil ölçüt:** "izlenenlere karşı kaydıranlar" (viewed / stayed to watch) %; **ikincil:** ortalama izlenme %. Ham görüntülenme yardımcıdır. Pencere: **48. saat (işaret) ve 7. gün (karar)**. Her ekran görüntüsü metrik adı ve tarihiyle saklanır. Video akışta ≥300 kez gösterilmeden analize girmez (varsayım).
- **Tek eksen:** aynı pencerede yalnız tanımlı eksenler (cilt ve kanca türü, ikisi de yazı-tura ile) oynar; süre, ses, iskelet ve müzik sabit.
- **Kazanan ilanı:** hücre başına ≥7 video. **≥10 puan fark ve 5/5 çiftte aynı yön = "etki var"**; 4/5 çift veya 5–10 puan = "ipucu"; <5 puan = "ayırt edilemedi" ("etkisiz" denmez). 14. videoda yalnız yön okunur; **hüküm 28. videoda/gününde** (≥10 çift).
- **Baz çizgi:** ilk 14 videonun medyan viewed %'i; 30. gün hedefi bu baz çizginin üzerinde (varsayım: +%30 medyan).
- **Baz çizgi (2026-10-14):** Emu: Stayed to watch %43,0 / Swiped away %57,0 (1.625 görüntülenme, %97 Shorts akışı); Dans: Shorts akışı %0 (28 görüntülenme; `veri/`). 14 videonun ilk baz çizgisi bu iki veriyle başlar.
- **Retro ilk adım (kullanıcı) — YAPILDI (kısmen):** 4 videonun Studio dökümü (gösterilme, viewed %, ort. izlenme %, ilk 3 sn düşüşü, trafik kaynağı, yorum sayısı).

## 9. Gözden geçirme tetikleyicileri (hangi sonuç neyi değiştirir)

| Sonuç | Değişiklik |
|---|---|
| Titanik'in ortak motora taşınması >3 gün | A'ya dön: ilk 14 videoda 1 cilt |
| Kapı bütçesi pilotta >20 dk | Haftada 4'e düş; kapı korunur |
| Emu ve Dans viewed % farkı ≤5–10 puan | "Konu/kanca açıklıyor" tezi düşer; ilk eksen konu türü olur |
| Emu–Dans fark ≥25 puan | Kanca-önce kuralı kalıcı zorunlu madde |
| 14. videoda iki kanca türü ≥15 puan ayrışıyor, 5 çiftin ≥4'ü aynı yön | Kanca türü zorunlu kural olur |
| 14. videoda son 7 videonun medyanı ilk 7'den ≥10 puan düşük | Tekdüzelik sinyali: cilt rotasyonu hemen açılır |
| Aynı iskelette cilt farkı ≥10 puan (≥8 kişilik test veya Studio) | Cilt ayrı eksen olarak sınanır; tavan 3 |
| Kör testte kadın ≥6/7, ≤1/7 robot | Erkek kilidi kalkar, kimlik değişimi yazılı ve tek seferde |
| 60. günde ≥30 video ve medyan engaged views baz çizginin 2 katına çıkmadı | "Daha çok iş" yerine yön değişikliği (seytan'ın hükmü) |

## 10. Mevcut videolar için eylemler

- **Titanik'in Kehaneti** (yayınlanmadan önce): kartta "6 BENZERLİK" kalkar veya videoda birebir 6 madde gösterilir (yalnız doğrulananlar sayılır); "KEHANET" mutlak değil soru: örn. **"14 YIL ÖNCE YAZILDI: KEHANET Mİ?"**; "İkisi de batmaz diye tanıtıldı" → "basında 'pratikte batmaz' denmişti"; "sancak tarafı" doğrulanana kadar çıkar; boy (244/269 m) ve bot sayısı (24/20) "yaklaşık" ve kaynaklı (hangi baskı: UNVERIFIED); kadın sürümde true peak ≤ −1 dBTP'ye düşürülür; cevap ("denizcilik bilgisi") ≤35. sn'de verilir.
- **Emu Savaşı** (yayınlandı): "1.000 emu / tam 10 mermi" sabit yorumda nitelenir ("komutanın kendi raporuna göre 986 emu, 9.860 mermi; sayım tartışmalı"); görev gücü üç kişiydi ("ordu" mecazı) notu; "zikzak" doğrulanamadı.
- **Dans Salgını** (yayınlandı): ~400 kişi üst sınırdır (50–400), ölüm iddiaları sonraki kroniklerden; sabit yorumda not. Video silinmez.
- **Zanzibar:** seslendirmesiz; sürekli sesli standardına uyum için yeniden değerlendirilir (yeniden yükleme yeni video).

## 11. Sınırlar

Bu belge simüle edilmiş bir kurulun tavsiyesidir; gerçek izleyici/Studio verisi yerine geçmez. Sayısal eşikler varsayımdır ve ilk 14 videoda yeniden yazılacaktır. Resmî YouTube sayfaları okunamadı; platform kuralları ikincil kaynaklara dayanır.

## 12. Kullanıcı düzeltmeleri (2026-10-15, 2026-10-17) — bu bölüm diğerlerinden önceliklidir

Kullanıcı Sıtma videosunu (TESLİMAT #5) izledikten sonra üç şey söyledi: **anlatım çok hızlı**, **bağlam zayıf**, **çizimler Titanik'le aynı** ("her konu için farklı çizimler yapacaktık"). Kurallar buna göre değişti:

1. **Her konu kendi çizim dilini taşır.** Bölüm 2'deki "tavan 3 cilt + yazı-tura" kaldırıldı. Önceki videonun cildi/sahne şablonu aynen tekrar edilmez; ortak olan yalnızca motor (çizim ilkelleri, render, ses, QA). Yeni konu için önce görsel dil seçilir (örnekler: düz renkli → Zanzibar; kara kalem → Emu, Dans; mavi baskı → Titanik, Sıtma; **kâğıt kesme diyorama → Dune × Star Wars**), HUD ve altyazı biçemi de konuya göre değişir (Dune videosunda serif altyazı + kâğıt "KANIT" etiketi).
2. **Tempo ve bağlam.** Anlatıcı hızı ≤ 1,0 (Piper `speed`; Dune videosunda 0,90), cümle arası ≥ 0,4 s, virgül/iki nokta arası ≥ 0,2/0,3 s. Her yeni olgudan önce kısa bağlam (kim/ne/ne zaman); cümle başına en çok **bir** yeni olgu; sayı/tarih yoğunluğu düşük. Toplam hız (duraklar dahil) ≈ 1,8 sözcük/sn (Dune: 276 sözcük / 156 sn); 2,3 sözcük/sn üstü "çok hızlı" sayılır.
3. **"Özel video" biçimi** (kullanıcı isterse): dikey 9:16, ≤ 3 dk (Shorts sınırı). Süre ve kanca kuralları gevşer: kanca bir **soru** olabilir ve vaat tek seferde değil **üç aşamada** ödenir (ara kanıt → "geri sayım" açık döngüsü → hüküm); kare 0 = son kare döngüsü, kaynak/telaffuz/QC kapıları aynen geçerlidir. Sıradan günlük Shorts 40 sn ±3 kalır.
4. **Aşırı yoğun bilgi yasak:** sayı sınırı (≤3) 40 sn'lik videolar içindir; özel videoda her sayı ekranda büyük kartla gösterilir ve söylenen sayı ≤ 6'dır.
5. **Doğrulanamayan hiçbir alıntı birebir söylenmez;** "anlatıldığına/bildirildiğine göre" ile niteliklenir ve kaynak dosyasında ikincil olduğu belirtilir.
6. **Hareket (özel video).** Sarsıntı/flaş sınırı (40 sn başına ≤2 / ≤1) süreyle ölçeklenir. Kâğıt/diyorama gibi durağan çizim dillerinde "2 sn'lik durağan pencere" ve `freezedetect` (−55 dB, 1 sn) kapıları, dünya katmanına yavaş kamera sürüklenmesi (zoom ≈ %2,6–5, HUD/altyazı sabit) ve vurgu anlarında kısa zoom itişleriyle geçilir. Tane (grain) ≤ 0,01 tutulur: hareketli sahnede 0,05 tane bit hızını 2,4× yaptı (134 MB).
7. **Yerleşim.** Altyazı bölgesine (y ≈ 1250–1390) metin taşıyan nesne (kart, etiket, damga) konmaz; kamera sürüklenmesi içeriği ±45 px kaydırdığı için nesneler bölgeden ≥ 60 px uzak tutulur. `capzone` taraması: altyazı sayfalarının orta anında dünya karesinde kenar yoğunluğu ölçülür; yalnız kum tepesi/zemin gibi arka plan dokusu kalmalıdır.
8. **HUD yalnız anlam taşıyan sayaçtır (2026-10-17).** Kullanıcı Pellagra videosunda (TESLİMAT #7) ekrandaki sabit "TESLİMAT #7" yazısına itiraz etti; bölüm 7'deki "HUD'da seri adı" ifadesi harfiyen uygulanınca Sıtma (YIL sayacı) ve Dune (KANIT n/5) ile tutarsızlık doğmuştu. HUD'da seri adı gibi değişmeyen yazı bulunmaz; HUD videonun ilerleyişini gösteren sayaçtır (Sıtma: YIL; Dune: KANIT n/5; Pellagra: KANIT + 4 kapsül). Seri adı yalnız açıklamanın 1. satırındadır.
