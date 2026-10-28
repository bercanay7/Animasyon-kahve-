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

## Ölçütler (YouTube Analytics)
- **Gösterim tıklama oranı (TO):** kanalların yarısı %2–10 arasında.
  - Göz at trafiğinde %3–5 iyi, Önerilen'de %4–8 normal.
  - Geniş kitleye açılırken TO'nun düşmesi normaldir.
- **İzleme süresi:** 5–10 dakikalık videoda ortalama izlenme %40 iyi, %50+ çok iyi. 0:30'da kalan izleyici %65–70 iyi.
- **Sisifos, ilk 18 saat:** 4,7 B gösterim, TO %1,6, izlenmelerin %84,5'i Göz at trafiğinden. Ortalama izleme 2:55 (%41) olduğu için YouTube gösterimi hızla artırdı.
- "Test ve karşılaştır" kazananı TO'ya göre değil izlenme süresi payına göre seçer. Test sürerken başlık değiştirilmez.

## Teknik notlar ve tuzaklar
- **Playwright:** `require('playwright')` her yerden çalışır, `NODE_PATH` ayarlama (bozuyor). `playwright install` çalıştırma.
- **Süreçler:** `pkill -f` kullanma; işlemleri PID ile durdur. Uzun render ve miks işlerini arka planda uzun `timeout` ile çalıştır.
- **Render önbelleği:** `render.js` parçaları `.parts*/` içinde tutar. Artık kod, zaman çizelgesi ve ayarların özetini (`KEY`) saklıyor ve değişince eski parçaları siliyor. Öncesinde kod değişse bile eski kareleri sessizce yeniden kullanıyordu (29 Ekim önizleme v2'de yaşandı). Şüphede klasörü elle sil.
- **Disk:** disk payı sınırlı. Ara parçaları (`.parts*/`) iş bitince sil. Büyük mp4'ler depoya girmez (`.gitignore`); kullanıcıya `SendUserFile` ile gönderilir.
- **Fontlar:** `sisifos/fonts.css` ve `orfeus/fonts.css` (Anton, Alfa Slab One, Lilita One, Bebas Neue, Cinzel …). Türkçe karakterli (latin-ext) woff2 dosyaları depoda.
- **Git:**
  - Oturumun kendi dalında çalış; kullanıcı istemedikçe PR açma.
  - Commit mesajı Türkçe ve açıklayıcı olsun, sonunda oturumun verdiği atıf satırları bulunsun.
  - Her iş parçasından sonra commit + push yap (durdurma kancası commit edilmemiş değişikliğe izin vermiyor).
- **`navitas-topkapi` deposu:** bu işle ilgisizdir, dokunma.

## Sonraki videolar için kullanıcının önerileri
- **Psikolojik anlatım:** Stefan Zweig (*Yıldızın Parladığı Anlar*) ve Dostoyevski gibi karakterin iç dünyasına inen bir anlatım.
  - 29 Ekim videosunda kayıt ve kurgu bittikten sonra önerildiği için uygulanmadı.
  - Senaryo en baştan bu üslupla kurulmalı: tek bir "karar anı" ve onu yaşayan kişinin iç dünyası.
  - İç dünya uydurulmaz. Kişinin kendi hatırat, mektup ve sözlerine dayanır; kaynak açıklamada verilir.
  - Atatürk için 5816 sayılı Kanun ve saygı kuralları gereği ona söz ya da düşünce uydurulmaz.
- **Hareket:** Animasyon hiç durmasın, sürekli aksın. Durağan kare kalmaz. Kontrol aracı `cumhuriyet/tools/donma.py`.

## Sıkışık takvimde öncelik (ör. 2 günlük teslim)
1. Senaryo (4–6 dk, 35–50 cümle) → kurul tek tur.
2. Seslendirme + zaman çizelgesi.
3. Yeni üslubun çizim ilkellerini (karakter, arka plan, doku) önce tek bir "üslup karesi" olarak kurula onaylat, sonra sahnelere yay.
4. Animasyon, müzik ve miks → render.
5. Kapak (A/B) + kurul.
6. Shorts.
7. `yayin.md`.
8. İngilizce dublaj: zaman kalırsa.
