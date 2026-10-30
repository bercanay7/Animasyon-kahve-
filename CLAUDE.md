# Zaman Kuryesi: animasyonlu video üretim rehberi (yeni oturumlar için)

Bu dosya, yeni bir Claude Code oturumunun önceki işleri baştan anlatılmadan devralması içindir.
Önce bunu, ardından `sisifos/README.md` (komutlar) ve `sisifos/yayin.md` (yayın adımları) dosyalarını oku.

## Kanal ve kullanıcı
- **Kanal:** YouTube'da "Zaman Kuryesi" (@ZamanKuryesi). Türkçe mitoloji, tarih ve felsefe animasyonları.
- **Önceki videolar:**
  - "Orfeus ve Evridiki: Ölüleri İkna Etti, Kendini Durduramadı". Üslubu kâğıt kesme, düz vektör.
  - "Sisifos'u Neden Mutlu Hayal Etmeliyiz? | Camus ve Absürt". Bu depoda; üslubu Yunan siyah/kırmızı figürlü vazo.
- **Kullanıcının çalışma biçimi:**
  - Türkçe yazar, kararlarını kısa verir ("Üret", "Devam edelim").
  - İşin baştan sona yapılmasını ister.
  - Her aşamayı bağımsız bir kurula onaylatır ve 10/10'a doğru tekrar tekrar iyileştirir.
- **Yayın:** kullanıcı YouTube Studio'da elle yapar. Bu oturumda tarayıcı eklentisi yok, Metricool'da YouTube yok. Dosyalar `SendUserFile` ile gönderilir. Adım adım bir `yayin.md` yazılır.
- **Anlatıcı:** ElevenLabs'te **"Emrullah"** sesi. Kanalın sesidir, değiştirilmez. `voice_id` her seferinde `creative_list_voices` ile bulunur, ezberden yazılmaz.
- **Kredi harcayan üretim** (ElevenLabs, Abracadabrax görsel/video): yalnız kullanıcı açıkça istediğinde yapılır. Aynı çağrıyı "yeniden dene" diye tekrarlama; her tekrar yeniden ücretlendirilir.

## Uçtan uca iş akışı
1. **Senaryo** (`senaryo.json`): cümle cümle yazılır. `tts` alanı seslendirme metnidir (ses etiketleriyle), `alt` alanı altyazı metnidir. Senaryo/yönetmenlik kurulu ≥9 verene kadar düzeltilir.
2. **Seslendirme:** her bölüm iki çekim alınır.
   - `tools/transcribe.py` çekimleri Whisper'dan geçirir. Metne karşı doğrulayıp iyi olanı seçer (`vo/secim.json`).
   - `tools/build_vo.py` seçilen çekimleri birleştirir. Çıktılar `vo/vo.wav` ve kelime zamanlı `timeline.js` olur.
3. **Animasyon:** Canvas 2D, `film.html` + `lib/*.js`. Her çekim bir cümleye (`S('B04')`) ya da kelimeye (`Wd('B04','kelime')`) bağlanır; ses değişince görüntü kendiliğinden kayar.
   Yeniden kullanılabilir modüller:
   - `lib/core.js`: zaman ve yumuşatma (`ramp`, `kf`, `E.*`), gürültü, spline.
   - `lib/anim.js`: oturma, ön hazırlık hareketi, göz kırpma, boşta salınım.
   - `lib/figure.js`: ileri/ters kinematikli profil figür.
   - `lib/style.js`: dokular, kumlanma, vinyet.
   - `lib/i18n.js`: ekran yazılarının İngilizcesi; `?lang=en` ile açılır.
4. **Ses:**
   - Müzik `audio/score.py` ile numpy/scipy'de sentezlenir (özgün).
   - Efektler `lib/sfx.js` → `tools/export_sfx.js` hattından geçer. Doğal efektler ElevenLabs'ten, vuruş ve çan gibileri `tools/mix.py` içinde sentezlenir.
   - `tools/mix.py` müziği konuşmanın altında kısar ve sesi -14 LUFS / -1 dBTP'ye getirir. İngilizce sürümde tepe -2 dBTP olur.
5. **Render:** `render.js`.
   - 4 paralel Chromium işçisi çalışır. 4 alt örnekli hareket bulanıklığı uygulanır. 1920×1080, 30 fps, H.264 CRF 18 + AAC.
   - Dosyaya BT.709 renk etiketleri ve ses dili etiketi eklenir.
6. **Shorts:** `shorts/` (EDL + `shorts.html`). 1080×1920, 40–55 sn, kelime vurgulu altyazı. Shorts'ta "İlgili video" alanı uzun videoya bağlanır.
7. **İngilizce dublaj (isteğe bağlı):**
   - `en/` klasörü, `senaryo_en.json` ve ayrı ses.
   - YouTube'da aynı videoya ikinci ses kanalı olarak yüklenir (`sisifos_en.m4a`).
8. **Kapak:** 1280×720 JPG (<2 MB). A/B için iki seçenek yapılır ve "Test ve karşılaştır" ile denenir.
   - Örnek kod `orfeus/kapak.js`: kâğıt kesme ilkelleri `paperCloud`, `cloudBank`, `lowPoly`, `head3q` (¾ baş), `hand`, `grip`, `rim`, `paperShadow`.
   - Kare çekmek için: `node orfeus/shot.js out.png "v=a"`.
9. **Yayın rehberi:** `yayin.md`. Başlık, açıklama (bölüm zaman damgalı), etiketler, altyazı, bitiş ekranı, zamanlama, ikinci ses kanalı.

## Kurul (bağımsız değerlendirme) yöntemi
- Her kurul, `Agent` ile açılan ayrı bir alt ajandır. Türleri:
  - senaryo/yönetmenlik;
  - sanat/üslup;
  - ses/miks;
  - kapak için ayrıca CTR/paketleme.
- **Kurula verilecekler:** amaç, dosya yolları, önceki turun eleştirileri (kontrol listesi olarak), ölçüt (≥9/10 = ONAY).
- **Kuruldan istenecekler:** puan, ONAY/RED, 1920×1080 koordinatlı ve sıralı düzeltme listesi.
- Sonraki turlarda **aynı ajana `SendMessage` ile devam et**, ölçütler tutarlı kalsın. "Yaptığım değişiklikler" listesini iddia olarak ver; kurul kendisi doğrulasın.
- Önceki turun dosyalarının **üzerine yazma**: yeni tur yeni isimle (`a5.png`, `board/tur4/…`). Kurullar karşılaştırma için eskisine bakıyor.
- **Kapak kurulunun test seti:** tam boy, 246×138 ve 168×94 küçültmeler; bulanıklık/belirginlik (odak noktası); gri değer; mobil akış taklidi (`mkfeed.py` mantığı); sağ alttaki süre rozeti bölgesi.

## Kapak dersleri (Orfeus turlarından)
- **Yüzler:** küçük boyda profil okunmaz, ¾ yüz kullan. Duygu (gözyaşı, kaş iç uçları yukarıda, açık ağız) 168 px'te okunmalı.
- **Odak:** tek odak olsun ve karenin en parlak noktası orası olsun (Orfeus'ta parmak uçları arasındaki kıvılcım). İkinci bir beyaz leke odağı böler.
- **Yazı:** büyük harfin yüksekliği karenin yüksekliğinin %18'inden fazla olsun. Figürlere en az 30 px boşluk bırak. Sağ alt köşe (süre rozeti) boş kalsın.
- **Üslup:** videonun üslubundan sapma; kapak izleyiciyi yanıltmamalı.
- **Türkçe kelime seçimi:** "SAKIN DÖNME!" yerine "ARKANA BAKMA!" kullanıldı, çünkü "dönme" argo bir hakaret olarak da okunur. "TEK BAKIŞ YETTİ" önce "ilk görüşte aşk" gibi okunuyor.
- Art arda iki videoda aynı kalıbı ("NEDEN …?") kullanma.
- Duruşta T pozundan kaçın. "Geri dönme" gibi bir anı gövde ile başın yön zıtlığıyla göster.

## Süreç dersleri (Prometheus'tan)
- **Kurul kapıları:** senaryo → seslendirme → üslup karesi → animatik → sahneler → ses/miks → kapak → Shorts.
  - Render ancak ses/miks ONAY'ından sonra başlar. Prometheus'ta ses kurulu geç açıldı; kesik kelimeler ("güvenmez" → "güvenme") ve kelimenin üstündeki motifler neredeyse yayına gidiyordu.
  - Shorts render'dan önce kurula gider. Prometheus'ta Shorts ilk turda 6,3 aldı.
  - ONAY'sız geçilen kapı kayda açıkça yazılır.
- **Kurula verilen "yaptım" iddiası** kare, ölçüm ya da diff ile verilir. Kurulun kendi önerisi de iddiadır: yan etkisi ölçülmeden uygulanmaz. Örnek: sabit müzik sınırlayıcısı dorukları 5–7 dB söndürdü.
- **Seslendirme kesimi:** Whisper kelime zamanları cümle sınırında üst üste binebilir. `build_vo.py` kesimdeki RMS'i denetleyip ilk gerçek duraklamaya keser; zaman çizelgesi değişmez.
- **Shorts'ta `notext`** filmin ekran yazılarını siler. Damga, künye ve kanca katmanı Shorts için ayrıca kurulur. Kadraj ve zemin geçişleri filmin kesmelerine kare kare eşlenir.
- **Teslim:**
  - Sohbetin dosya sınırı 500 MB; kullanıcının YouTube yükleme sınırı 400 MB (MB, MiB değil).
  - Uzun video için ≤ 400 MB H.265 yükleme kopyası hazırlanır (CRF ≈ 21, ses kopyalanır).
  - Dosyalar iş bitince tek seferde, ayrı ayrı gönderilir.
- **Render'ı mutlak yolla başlat:** depo kökünde ilgisiz, eski bir `render.js` var.

## Ölçütler (YouTube Analytics)
- **Gösterim tıklama oranı (TO):** kanalların yarısı %2–10 arasında.
  - Göz at trafiğinde %3–5 iyi, Önerilen'de %4–8 normal.
  - Geniş kitleye açılırken TO'nun düşmesi normaldir.
- **İzleme süresi:** 5–10 dakikalık videoda ortalama izlenme %40 iyi, %50+ çok iyi. 0:30'da kalan izleyici %65–70 iyi.
- **Sisifos, ilk 18 saat:** 4,7 B gösterim, TO %1,6, izlenmelerin %84,5'i Göz at trafiğinden. Ortalama izleme 2:55 (%41) olduğu için YouTube gösterimi hızla artırdı.
- **Sisifos, 3. gün:**
  - Erişim: 22,2 B gösterim, 1.554 görüntüleme, 27,7 saat izlenme.
  - İzleme: ortalama 3:07, izleyici tutma %44,3.
  - Trafik: Göz at %75, Önerilen %20,6.
  - Gösterim basamak basamak arttı (ikinci dalga); Orfeus'un ~92 görüntülemesine göre yaklaşık 17 kat.
  - Zayıf halka TO (%1 küsur). Güçlü yanı tutma: açılış kancası ve bölüm yapısı korunmalı.
- **Sisifos, 5. gün:** kanalın en çok izlenen ve en çok etkileşim alan videosu oldu.
  - Erişim: 43,7 B gösterim, TO %2,2 (yükseliyor), 3.452 görüntüleme, 75,7 saat izlenme.
  - İzleme: tutma %44,8 (3:10).
  - Büyüme 5. günde hızlandı (üçüncü dalga).
  - **Giriş dersi:** 0:30'da izleyicilerin %63'ü kalıyor ("standart"), ama kayıp ilk 10–15 saniyede.
    - Yeni videolarda ilk 5 saniye kapağın vaadini hemen karşılamalı. Kapak "NEDEN GÜLÜYOR?" diye sorarken açılış başka bir sahneyle başlıyordu.
    - Merak sorusunu ilk cümlede sor, cevabı sona sakla.
  - **Son:** sondaki düşüş bitiş ekranından (6:51), normal. Sona doğru (~6:10) küçük bir artış var: doruk anı. Shorts için en iyi aday bu an.
  - **Gövde:** YouTube'un "Önemli an" işareti yaklaşık 1:00–6:15 aralığını kapsıyor: izleyiciyi normalden uzun tutuyor. Bölümlü hikâye yapısı çalışıyor, korunmalı.
  - **Kanala etkisi:** Orfeus, "ARKANA BAKMA!" kapağıyla ve Sisifos'tan gelen önerilerle 7. günde ~92'den 244 görüntülemeye çıktı.
- **Kanaldaki diğer videolar:**
  - "Cumhuriyet'i Kuran Kuşak Nasıl Yetişti?" (29 Ekim; 6:20; kapak "KURUCU KADRO / AYNI SIRADA"): 15 saatte 61 görüntüleme.
  - "Şarlken: Dünyayı Teslim Eden İmparator" (21:27): 11 günde 147 görüntüleme. Şimdiye kadar en iyi sonucu mit ve felsefe videoları verdi. Bu bir süre kuralı değil; aşağıdaki "Süre" maddesine bak.
- "Test ve karşılaştır" kazananı TO'ya göre değil izlenme süresi payına göre seçer. Test sürerken başlık değiştirilmez.

## Kitle (Sisifos, 5. gün) ve kanal yönü
- **Kitle verileri:**
  - Ülke: Türkiye %73,6.
  - Altyazı: izleyicilerin %38,4'ü Türkçe altyazıyla izliyor. Her videoya doğru SRT şart. İngilizce altyazı %1,2, bu yüzden İngilizce dublaj düşük öncelikli.
  - Bağlılık: izlenme süresinin %98,8'i abone olmayanlardan, izleyicilerin %95,5'i yeni. Abone çağrısı doruk anına (~son dakika) ve bitiş ekranına konmalı.
  - Cihaz: telefon %48, bilgisayar %23, TV %22, tablet %6.
  - Cinsiyet: kadın %22,5.
- **Kanal yönü (kullanıcının kararı):** yalnız mitoloji değil, geniş bir alan: tarih, felsefe ve kitap, film ve dizi. Kanalı bir arada tutan konu değil biçim olacak:
  - animasyonlu anlatım;
  - tek bir büyük soru;
  - Emrullah sesi;
  - "geçmişten bugüne soru taşıyan kurye" fikri.
- **Bölümler** (her biri ayrı oynatma listesi):
  - Mitler ve Felsefe;
  - Tarihin Dönüm Noktaları;
  - Kitapların Sorduğu Sorular;
  - Ekrandaki Felsefe.
- **Süre (kullanıcının kararı):** sabit bir süre sınırı yok. Hikâye ne kadar gerektiriyorsa o kadar anlatılır; izlenme için içerik kırpılmaz. Kanal kullanıcının hobi alanıdır. Uzun videoda tutmayı sağlayan süre değil temposudur:
  - her bölüm kendi küçük merak sorusuyla açılır;
  - YouTube bölüm zaman damgaları konur;
  - açılış kuralı (ilk 5 saniyede kapağın vaadi) değişmez;
  - kurul "bu sahne hikâyeye bir şey katıyor mu?" diye sorar, "kısa mı?" diye değil.
- **Sıradaki video:** Prometheus (kullanıcının kararı). Durum: üretildi, yayına hazır (`prometheus/yayin.md`, karar kaydı `prometheus/kurul/kararlar.md`, geriye bakış `prometheus/geriye_bakis.md`).
  - **Çıkış noktası:** Aiskhylos'un *Zincire Vurulmuş Prometheus*'u (İş Bankası Kültür Yayınları, Hasan Âli Yücel Klasikler). Kullanıcıyı asıl etkileyen, kitabın kendisinden çok Azra Erhat'ın önsözü; onun Prometheus'a bakışı videonun omurgası olacak.
  - **Önsözden yorum uydurma:** Erhat'a ait her görüş ve alıntı yalnız kullanıcının verdiği önsöz sayfalarından (fotoğraf ya da metin) alınır. Kaynak yoksa sorulur.
  - **Telif:** önsöz ve çeviri telif kapsamında (Erhat 1982'de öldü). Fikirler kendi cümlelerimizle anlatılır; kısa alıntılar kaynak gösterilerek yapılır. Açıklamaya künye yazılır.
  - **Konu yapısı:** Hesiodos'taki düzenbaz Prometheus, Aiskhylos'taki insanlığın velinimeti ve Zeus'un zorbalığına direnen Prometheus, ve Erhat'ın okuması.
  - **Üslup (kullanıcının kararı):** Sisifos'taki Yunan vazo resmi üslubu. Motor `sisifos/lib` yeniden kullanılır: `figure.js`, `style.js`, `core.js`, `anim.js`, `render.js` ve ses hattı. Proje `prometheus/` klasöründe kurulur, Sisifos dosyalarına dokunulmaz. Bu üslup "Mitler ve Felsefe" serisinin görsel kimliğidir. Prometheus ve kartal antik vazolarda gerçekten tasvir edilmiştir.
  - **Üslubun sınırı:** kodla çizimin güçlü olduğu alan siluet, profil figür, sahne kurgusu, ışık ve dönüşüm efektleridir; yüz, el ve karmaşık beden hareketleri zayıf yandır. Sahneleri buna göre kur: güçlü kompozisyon, az ama anlamlı hareket.
  - **Köprü:** Prometheus yeni alanlara köprü olarak kullanılabilir:
    - Mary Shelley'nin *Frankenstein*'ının alt başlığı "Modern Prometheus"tur (kitap bölümü).
    - Nolan'ın *Oppenheimer* filmi, *American Prometheus* biyografisine dayanır (film bölümü).
- **Film ve dizi videolarında:** film görüntüsü kullanma; oyuncuya benzeyen gerçekçi çizimden ve telifli karakter tasarımlarını kopyalamaktan kaçın. Kendi animasyonunla fikri anlat.

## Teknik notlar ve tuzaklar
- **Playwright:** `require('playwright')` her yerden çalışır, `NODE_PATH` ayarlama (bozuyor). `playwright install` çalıştırma.
- **Süreçler:** `pkill -f` kullanma; işlemleri PID ile durdur. Uzun render ve miks işlerini arka planda uzun `timeout` ile çalıştır.
- **Disk:** disk payı sınırlı. Ara parçaları (`.parts*/`) iş bitince sil. Büyük mp4'ler depoya girmez (`.gitignore`); kullanıcıya `SendUserFile` ile gönderilir.
- **Fontlar:** `sisifos/fonts.css` ve `orfeus/fonts.css` (Anton, Alfa Slab One, Lilita One, Bebas Neue, Cinzel …). Türkçe karakterli (latin-ext) woff2 dosyaları depoda.
- **Git:**
  - Oturumun kendi dalında çalış; kullanıcı istemedikçe PR açma.
  - Commit mesajı Türkçe ve açıklayıcı olsun, sonunda oturumun verdiği atıf satırları bulunsun.
  - Her iş parçasından sonra commit + push yap (durdurma kancası commit edilmemiş değişikliğe izin vermiyor).
- **`navitas-topkapi` deposu:** bu işle ilgisizdir, dokunma.

## Sıkışık takvimde öncelik (ör. 2 günlük teslim)
1. Senaryo (4–6 dk, 35–50 cümle) → kurul tek tur.
2. Seslendirme + zaman çizelgesi.
3. Yeni üslubun çizim ilkellerini (karakter, arka plan, doku) önce tek bir "üslup karesi" olarak kurula onaylat, sonra sahnelere yay.
4. Animasyon, müzik ve miks → render.
5. Kapak (A/B) + kurul.
6. Shorts.
7. `yayin.md`.
8. İngilizce dublaj: zaman kalırsa.
