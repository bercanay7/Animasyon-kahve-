# Zaman Kuryesi: animasyonlu video üretim rehberi (yeni oturumlar için)

Bu dosya, yeni bir Claude Code oturumunun önceki işleri baştan anlatılmadan devralması içindir.
Önce bunu, ardından `sisifos/README.md` (komutlar) ve `sisifos/yayin.md` (yayın adımları) dosyalarını oku.

## Depo düzeni (13 Kasım 2026'dan beri her şey `main`'de)
Yeni oturum `main`'den başlar; eskiden her video kendi dalında kaldığı için yeni oturumlar önceki işi göremiyordu. Bütün kanal dalları `main`'de birleştirildi. **Her video bitince kendi dalı `main`'e birleştirilir** (kullanıcının kararı).

| Klasör | Ne |
|---|---|
| `ran/` | **Kurosawa, Ran** (16 Kasım 2026; kanalın ilk film videosu, mürekkep resmi üslubu, 8:02). Hazır motor: LemoLab ink-wash (MIT) → `lib/ink.bundle.js` (`tools/bundle_ink.py`) + **hızlı birleştirici** `lib/comp_hizli.js` + çizim ilkelleri `lib/ran_cizim.js` (kale, ateş, xieyi figür, flüt) + plan sistemi `lib/film.js`/`lib/sahneler.js`. Gerçek görsel araları (Met CC0, Commons PD) `kaynak/GORSELLER.md`. Kurgu özeti `tools/ozet.js`, kare `tools/kare_cek.js` (yerel http). `uretim_plani.md`, `geriye_bakis.md`, `KURUL.md` (kurulsuz) |
| `kafka/` | **Kafka, Dönüşüm** (15 Kasım 2026; ağaç baskı üslubu, 6:39). Hazır motor: LemoLab woodcut (MIT) → `lib/woodcut.bundle.js` (`tools/bundle_woodcut.py`) + baskı çekim sistemi `lib/kes.js` + 1910'lar figürleri `lib/insan.js`. Talep kontrolü ve iskelet `uretim_plani.md`; `geriye_bakis.md`, `KURUL.md` (kurulsuz) |
| `ikaros/` | **İkaros** (14 Kasım 2026; serigrafi seyahat afişi üslubu, 5:55). Hazır motor: LemoLab `silk.js` (MIT) + bizim çekim sistemimiz. Whisper/scipy yokken çalışan araçlar: `tools/hizala.py` (sessizliğe dayalı hizalama), `audio/dsp_shim.py` (numpy scipy yerine), `tools/mix_ffmpeg.py`; Shorts `shorts/build.py` (çok kesitli, gerçek duraklamadan keser). `geriye_bakis.md`, `KURUL.md` |
| `milton/` | Kayıp Cennet (Doré gravürü; en olgun motor ve araçlar). Yeni videoda buradan başla: `lib/` (gravür motoru, çekim sistemi `film.js`), `lib/acts/KILAVUZ.md` (sahne üretim kılavuzu), `tools/` (`kurgu_ozet.py` bütün filmi tek bakışta; `plan_zaman.py`; `srt.py`; `bolum_damga.py`; `build_vo.py`; `mix.py`), `render.js`, `kapak/` (kapak ve test seti), `KURUL.md`, `geriye_bakis.md` |
| `prometheus/` | Prometheus (vazo üslubu); `geriye_bakis.md`, `kurul/kararlar.md` |
| `sisifos/` | Sisifos (vazo üslubu); `README.md` komutlar, `yayin.md`, Shorts hattı (`shorts/`) |
| `orfeus/` | Orfeus (kâğıt kesme); `kapak.js` |
| `cumhuriyet/`, `29-ekim/`, `cumhuriyet_kapak/` | 29 Ekim videosu ve yeni kapakları |
| `gunluk-shorts/` | Şarlken uzun video ve günlük Shorts (Python motoru); `sarlken_kapak/` yeni paket. **Medici serisi** ("Medici Ailesi (1/7): Faiz Yasakken Nasıl Zengin Oldular?", 10:02, 5 Kasım): `gunluk-shorts/medici-uzun-dosya/` (kapak `kapak_medici.py`, `yayin/`); dersleri `gunluk-shorts/DERSLER.md`, yayın kaydı `gunluk-shorts/yayin_gunlugu.jsonl` |
| `analiz/` | Studio analizleri. **`2026-11-17-kanal-ortalamasi.md`: 9 uzun videonun ömür boyu ve ilk 7 gün verisi, kanal medyanları ve yeni videonun ölçüt çizgisi; yeni video bununla karşılaştırılır** (ham veri `2026-11-17-studio-verileri.md`). Eski: `2026-11-11-studio-analizi.md` (dışa aktarım) |
| `zaman-kuryesi-zanzibar/` | Zanzibar savaşı Shorts |
| `.claude/skills/` | `yonetmenlik` (hikâye iskeletleri, YouTube kuralları, taslak kontrol listesi), `cizim`, `karakter`, `ses`, `render`, `lisans-kontrol`; oturum başında otomatik yüklenir |
| `araclar/` | ortak araç kutusu, `ASSETS.md` (lisans kaydı). **`araclar/hareket/`** (14 Kasım): yürüyüş/koşu çözücüsü (ayak kaymaz), deterministik yay ve sarkaç, figürü izleyen kare şeridi `serit.js` (her filmde çalışır); kılavuz `hareket/KILAVUZ.md`. **`araclar/lemo/`**: Lemo-Opuscar'ın 99 üslubundan kanala uyanların kataloğu ve sabit commit'ten indirme betiği. **`araclar/ADAYLAR.md`**: incelenen açık kaynak depolar (alınan, alınmayan, sıradaki) |
| `.claude/skills/cinecode/` | **cinecode** (MIT, Sarp Yıldız): kodla film yapma becerisi. Yalnız kullanıcı `/cinecode` yazınca çalışır (kanal dışı işler için). Kanal videolarında başvuru kütüphanesidir: 61 üslup tarifi (`styles/`), uzun belgesel yazımı, jüri, ses, tipografi, kamera, denetim ve **arşiv malzemesi lisans kuralları**. Yeni videoda üslup seçerken, kurul brifi yazarken ve arşiv malzemesi kullanırken önce `.claude/skills/cinecode/BIZIM_NOT.md`'yi oku. Kanalın kuralları (Emrullah, kurul, kredi) önce gelir |
| kök dizin (`animation.html`, `render.js`, `poster.js`…) | eski Navitas kahve Story'si; kanalla ilgisiz |


## Kanal ve kullanıcı
- **Kanal:** YouTube'da "Zaman Kuryesi" (@ZamanKuryesi). Türkçe mitoloji, tarih ve felsefe animasyonları.
- **Önceki videolar:**
  - "Orfeus ve Evridiki: Ölüleri İkna Etti, Kendini Durduramadı". Üslubu kâğıt kesme, düz vektör.
  - "Sisifos'u Neden Mutlu Hayal Etmeliyiz? | Camus ve Absürt". Bu depoda; üslubu Yunan siyah/kırmızı figürlü vazo.
- **Kullanıcının çalışma biçimi:**
  - Türkçe yazar, kararlarını kısa verir ("Üret", "Devam edelim").
  - İşin baştan sona yapılmasını ister.
  - Her aşamayı bağımsız bir kurula onaylatır ve 10/10'a doğru tekrar tekrar iyileştirir.
  - Önerilerini öneri olarak verir. Onaylanmayı değil, uzman gözüyle tartılmayı bekler: "Karar tamamen sana ait", "sen patronsun".
    - Uymayan öneri gerekçesiyle geri çevrilir ve uygunsa sonraki işe not edilir.
    - Onu memnun etmek için öneriyi kabul etme.
- **Yayın:** kullanıcı YouTube Studio'da elle yapar. Bu oturumda tarayıcı eklentisi yok, Metricool'da YouTube yok. Dosyalar `SendUserFile` ile gönderilir. Adım adım bir `yayin.md` yazılır.
- **Anlatıcı:** ElevenLabs'te **"Emrullah"** sesi. Kanalın sesidir, değiştirilmez. `voice_id` her seferinde `creative_list_voices` ile bulunur, ezberden yazılmaz.
- **Kredi harcayan üretim** (ElevenLabs, Abracadabrax görsel/video): yalnız kullanıcı açıkça istediğinde yapılır. Aynı çağrıyı "yeniden dene" diye tekrarlama; her tekrar yeniden ücretlendirilir.

## Uçtan uca iş akışı
1. **Senaryo** (`senaryo.json`): cümle cümle yazılır. `tts` alanı seslendirme metnidir (ses etiketleriyle), `alt` alanı altyazı metnidir. Senaryo/yönetmenlik kurulu ≥9 verene kadar düzeltilir.
   - **Önce talep kontrolü (Kafka'dan itibaren kural):** senaryodan önce `uretim_plani.md`'ye yazılır.
     - (a) Türk izleyici bu adı ya da konuyu tanıyor mu? YouTube otomatik tamamlaması (`suggestqueries-clients6.youtube.com`, `hl=tr&gl=tr`) ve konudaki Türkçe videoların izlenme sayıları ile ölçülür. Kontrol satırı olarak kanalın eski konuları da aranır.
     - (b) Başlık ve kapak izleyiciye kendi hayatından bir soru soruyor mu?
     - Başlık ve kapağın ilk taslağı senaryodan **önce** yazılır; paketleme kurulu onu senaryo kuruluyla birlikte görür.
     - **On başlık adayı (17 Kasım 2026'dan beri kural):** başlık tek aday yazılıp düzeltilmez; `uretim_plani.md`'ye en az 10 aday yazılır, paketleme kurulu (kurulsuz üretimde başkan) aralarından seçer ve gerekçeyi yazar. Her aday şu sorularla elenir:
       - izleyiciye kendi hayatından soru soruyor mu, yoksa yalnız konuyu mu anlatıyor?
       - tek nefeste okunuyor mu?
       - cevabı yarı tahmin ettiriyor ama ele vermiyor mu?
       - talep kontrolündeki tanıdık kapı (izleyicinin aradığı kelime) içinde mi?
       - bağlam istemeden anlaşılıyor mu?
       Soru biçimi tek başına ölçüt değildir: genel soru zayıf, izleyicinin hayatına sorulan soru güçlüdür. Kaynak: bir "Viral Hook Tier List" ile kanal verisinin (Sisifos, Milton, İkaros, Cumhuriyet) karşılaştırması.
     - Kontrol zayıfsa açı kullanıcıya önerilir; konuyu değiştirmek ya da korumak kullanıcının kararıdır.
   - **Önce iskelet (İkaros'tan sonra kural):** senaryo yazılmadan önce `yonetmenlik` becerisindeki "Hikâye yapısı seç" tablosundan bir iskelet seçilir (Harmon çemberi, Kahramanın Yolculuğu, Kişōtenketsu, Shorts için Pixar omurgası). Projenin `uretim_plani.md`'sine yazılır: hangi iskelet, neden, kahraman kim, her adımın cümle numarası. Ayrıca açık merak döngüleri (soru → cevap cümlesi) ve bir önceki videonun iskeleti yazılır. Senaryo kurulunun ilk sorusu "senaryo bu iskeletle mi kuruldu?" olur.
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

## Senaryo yapısı: Kahramanın Yolculuğu + kanalda işe yarayanlar
Campbell'ın (Vogler uyarlamasıyla) Kahramanın Yolculuğu bir kalıp değil, kontrol listesi olarak kullanılır. Her videonun konusu bu kalıba uymaz (tarih videoları, kolektif hikâyeler). Kalıba uymayan aşama zorlanmaz. Senaryo kurulu bu listeyle bakar.

| Aşama | Videoda karşılığı | Sisifos verisinden ders |
|---|---|---|
| 0. Kanca | 0–5 sn: kapağın sorusu, büyük sınavdan bir kare (olayın ortasından başla) | Kayıp ilk 10–15 sn'de; kapak ile açılış aynı vaadi vermeli |
| 1. Sıradan dünya | Kısa: kim, hangi dünya, kurallar ne | Uzatma |
| 2. Çağrı ve eşik | Belayı başlatan seçim | Bölüm başlığı + küçük merak sorusu |
| 3. Sınavlar, dostlar, düşmanlar | Bölüm bölüm ilerleyen hikâye | Gövde "Önemli an" oldu; bölümlü yapı tutuyor |
| 4. Büyük sınav | İkonik an (Orfeus'un dönüp bakışı, Prometheus'un zincire vurulması) | Kapak bu andan seçilir |
| 5. Bedel ya da ödül | Kazanılan ve kaybedilen | |
| 6. Dönüş ya da kırılma | Mitin kalıbı nerede kırdığı: Orfeus dönüş yolunda, Sisifos sonsuz sınavda kırılır | Kanalın imzası: "yolculuk nerede kırıldı?" |
| 7. İksir | Bugüne taşınan fikir (Camus, Erhat …); "Zaman Kuryesi"nin getirdiği soru | Doruk ~son dakika; abone çağrısı burada |
| 8. Bitiş | Bitiş ekranı: seriden bir sonraki video | |

- **Kanalın kendisi bir yolculuk:** izleyici geçmişe gider ve bir soruyla (iksirle) döner. Anlatıcı bu yolculuğun kuryesidir.
- **Kahraman her zaman başlıktaki karakter değildir.** Örneğin Prometheus'ta kahraman insanlıktır: Prometheus ona ateşi (iksiri) veren ve bedelini ödeyen yol göstericidir. Kurul bu bakışın konuya uyup uymadığını değerlendirir.

## Kurul (bağımsız değerlendirme) yöntemi
**Yapı (kullanıcının kararı, 1 Kasım 2026):**
- **Başkan:** ana oturumdur (yapımcı).
  - Bulguları kendisi doğrular (ölçer, bakar, dinler).
  - Çatışmaları çözer ve son kararı verir.
  - Reddettiği bulguyu gerekçesiyle yazar.
- **Kullanıcının kararları** her şeyin üstündedir.
- **Üyeler:** her alanda **en az iki üye** bulunur. Her üye ayrı bir `Agent` alt ajanıdır ve farklı bir mercekle bakar; aynı bakışın iki kopyası olmaz.
- **Eşik:** ≥9/10 ONAY.

**Alanlar ve üyeler** (29 Ekim projesinin `cumhuriyet/KURUL.md` düzeninden):

| Alan | Üyeler (iki farklı mercek) |
|---|---|
| Senaryo ve dramaturji | senaryo/yönetmenlik + dramaturg (Kahramanın Yolculuğu listesi) |
| Kaynak ve doğruluk | konu uzmanı (tarih/edebiyat/felsefe) + kaynak denetçisi (tarih, alıntı, dize numarası, atıf; uydurma avı) |
| Anlatım (seslendirme) | seslendirme yönetmeni + Türkçe diksiyon uzmanı |
| Kanca ve tutma | YouTube tutma stratejisti + "ilk kez gören izleyici" (akışta kaydıran, şüpheci; şeytanın avukatı) |
| Sanat ve üslup | sanat yönetmeni + üslubun dönem/gelenek uzmanı |
| Animasyon ve kurgu | animasyon yönetmeni + kurgu/ritim uzmanı |
| Ekran yazıları ve altyazı | tipografi tasarımcısı + altyazı editörü (okuma hızı, satır bölme) |
| Müzik, ses ve miks | müzik direktörü + ses tasarımcısı/miks mühendisi |
| Teknik kalite | render ve kodlama denetçisi (renk etiketleri, kare kusurları, ses ölçümleri) + erişilebilirlik (telefon ve TV okunurluğu) |
| Hassasiyet ve hukuk | telif ve YouTube politikaları uzmanı + toplumsal ve dini hassasiyet okuru |
| Kapak, başlık, yayın paketi | TO/paketleme stratejisti + sanat yönetmeni |
| Yayın sonrası analiz (48. saat ve 7. gün) | kanal analisti + paketleme stratejisti; dersleri bu dosyaya yazar |

**Akış (her alan için):**
1. **Bağımsız ilk bakış:** üyeler birbirinin raporunu görmeden puan verir. Her rapor şunları içerir:
   - ONAY ya da RED;
   - 1920×1080 koordinatlı, sıralı düzeltme listesi;
   - "en emin olmadığım nokta".
2. **Çapraz eleştiri:** başkan iki raporu çapraz verir (`SendMessage`). Her üye ötekinin raporunda katıldığını, katılmadığını (gerekçeyle) ve gözden kaçanı yazar. Uzlaşma zorunlu değildir.
3. **Başkan kararı:**
   - Başkan iddiaları kendisi doğrular, düzeltmeleri sıralar ve uygular.
   - Projenin `KURUL.md` dosyasına alan, üyeler, puan, durum, reddedilen bulgular ve gerekçeleri işlenir.
4. **Sonraki tur:** aynı üyelerle devam edilir (`SendMessage`), ölçütler tutarlı kalır. "Yaptığım değişiklikler" listesi iddia olarak verilir; üyeler kendileri doğrular. Önceki turun dosyalarının **üzerine yazılmaz** (yeni tur yeni adla, ör. `board/tur4/…`).

**Kurallar:**
- **Veto:** kaynak/doğruluk ve hassasiyet/hukuk alanlarının engelleyici bulguları estetik oyla geçersiz kılınamaz. Yanlış bilgi, telif ve 5816 bulguları düzeltilmeden iş bitmez.
- **Maliyet:** iki üyeli tam tur yalnız şu kapılarda yapılır:
  - senaryo onayı;
  - üslup karesi;
  - ilk tam kurgu;
  - son render;
  - kapak;
  - yayın paketi.

  Küçük düzeltme turlarında tek üyeyle gerileme kontrolü yeterlidir.
- **Kurulun sınırı:** kurullar sesi dinleyemez. Whisper sözcük güveni, konuşma hızı, duraklar, perde ve enerji eğrileriyle ölçerler; kulakla son onay kullanıcınındır.
- **Kapak test seti:**
  - tam boy;
  - 246×138, 168×94 ve 120×68 küçültmeler;
  - bulanıklık/belirginlik (odak noktası);
  - gri değer;
  - koyu ve açık mobil akış taklidi (`mkfeed.py` mantığı);
  - TV boyunda bakış;
  - sağ alttaki süre rozeti bölgesi.

## Kapak dersleri (Orfeus turlarından)
- **Yüzler:** küçük boyda profil okunmaz, ¾ yüz kullan. Duygu (gözyaşı, kaş iç uçları yukarıda, açık ağız) 168 px'te okunmalı.
- **Odak:** tek odak olsun ve karenin en parlak noktası orası olsun (Orfeus'ta parmak uçları arasındaki kıvılcım). İkinci bir beyaz leke odağı böler.
- **Yazı:** büyük harfin yüksekliği karenin yüksekliğinin %18'inden fazla olsun. Figürlere en az 30 px boşluk bırak. Sağ alt köşe (süre rozeti) boş kalsın.
- **Üslup:** videonun üslubundan sapma; kapak izleyiciyi yanıltmamalı.
- **Türkçe kelime seçimi:** "SAKIN DÖNME!" yerine "ARKANA BAKMA!" kullanıldı, çünkü "dönme" argo bir hakaret olarak da okunur. "TEK BAKIŞ YETTİ" önce "ilk görüşte aşk" gibi okunuyor.
- Art arda iki videoda aynı kalıbı ("NEDEN …?") kullanma.
- Duruşta T pozundan kaçın. "Geri dönme" gibi bir anı gövde ile başın yön zıtlığıyla göster.
- **Cumhuriyet kapağı (5 tur):**
  - Gerçek kişinin silueti (kalpaklı Atatürk profili) 168 px'te ancak doğru biçimle tanınıyor:
    - kalpak kafatasından geniş, alında ve ensede kısa eğimle taşar;
    - yumuşak köşeli, hafif genişleyen silindir;
    - düzgün aralıklı yumru taç ya da kale gibi okunur, dik basamak silindir şapka gibi okunur.
  - Kalıp kayması yüzde ince kâğıt boşluğu bırakıp gözyaşı gibi okunabilir; yakın plan yüzler kaymasız basılır.
  - Ağız çizgisi yüz konturunu aşarsa "sigara" gibi okunur.
  - Eller iki yanda ayna gibi olmalı; tek el sarkarsa "hata" gibi görünür.

### Kapak kompozisyonu seçenekleri (öneri, kural değil; 17 Kasım 2026)
Kaynak: Mario Joos'un 1 milyonu geçen videolardaki 15 kapak kompozisyonu listesi (X paylaşımı, kullanıcı getirdi). Liste kazananlardan çıkarıldığı için "bu tıklatır" diye değil, fikre göre seçilecek bir menü olarak okunur. Kapak kurulu taslak çıkarırken buna bakabilir.
- **Kanala uyanlar:**
  - **Çatışma:** iki güç birbirine yaklaşıyor, sonuç belli değil (Prometheus ve kartal, Lear ve kızları). İki siluet ve aradaki boşlukla kurulur.
  - **A, B'yi etkiliyor:** biri ötekini hedef alıyor.
  - **Ortadan başlamak:** hikâye çoktan başlamış; "olayın ortasından başla" kuralının kapaktaki hâli.
  - **Üç aşamalı dönüşüm:** soldan sağa değişim (Lewis'in başmelek → karabatak → kurbağa → yılan okuması; Medici'nin yükselişi).
  - **Hareket oku:** sonuç gizli (İkaros'un güneşe giden yolu; Ran kapak B'deki üç ok).
  - **Karşıtlık:** boyut ya da değer farkı (Şarlken: imparatorluk ve yere bırakılmış taç).
  - **"Bunu yapma" uyarısı:** Orfeus'un "ARKANA BAKMA!" kapağı; art arda kullanılmaz.
  - **Suçlama:** izleyiciyi hedef alır. Talep kontrolünün (b) maddesine en yakın kalıp, ama riskli: video duygu açısından vaadi karşılamazsa izleyici hayal kırıklığına uğrar. Hassasiyet kurulundan geçer.
- **Uymayanlar:**
  - **Başlık + yüz ve dramatik yüz:** tanınan bir yüz ister. Milton'ın "BEN CEHENNEMİM" kapağı bu kalıba yakındı ama yüz tanınmıyordu; talep kontrolünün (a) maddesiyle aynı ders.
  - **Sohbet sorusu, alıntı ya da tepki, puanlama:** kanalın tonuna ve hâline uymuyor.
  - **Kısıtlama kuralı:** meydan okuma videoları için; bizde nadiren.
- **Öneri:** iki kapak iki farklı kompozisyondan seçilirse "Test ve karşılaştır" iki kalıbı karşılaştırır. Kapak kaydına kullanılan kompozisyon yazılırsa birkaç video sonra kanalın kendi verisiyle hangi kalıbın tuttuğu görülür.
- **Araştırma bulguları (17 Kasım 2026, öneri):**
  - **Formüller kanalın kurallarıyla uyuşuyor.** MrBeast'in sızan yapım kılavuzu (gerçekliği doğrulanmadı): kapak videonun en heyecanlı anını gösterir, ilk dakika vaadi karşılar. Paddy Galloway: kapağın %80–90'ı tıklama psikolojisi, tasarım küçük pay.
  - **Eden'in çalışması** (8.691 kanal, 507 bin video; kanal ortalamasının 2 katını aşanlar ile altında kalanlar karşılaştırılmış; gözlemsel, satıcı yayını, konu ayrımı yok):
    - yüz neredeyse fark etmiyor (%84,2'ye %82,2);
    - renk ve parlaklıkta fark yok;
    - en büyük fark **4–6 kelimelik kapak yazısı** (%30,6'ya %26,5);
    - çizilmiş ok ve halka biraz daha sık (%41,8'e %38,1).
  - **1of10 raporu** (Search Engine Journal aktarımı): yüz yalnız büyük kanallarda ve az işe yarıyor; belirleyici olan kapağın konuya uyması.
  - **Deneme önerisi:** bizim kapak yazılarımız 2–3 kelime ("BEN CEHENNEMİM", "İKİ UYARI VARDI"). Bir videoda iki kapaktan biri 4–6 kelimelik iki satırla denenebilir; %18 harf yüksekliği kuralıyla çatışması test setinde ölçülür.
  - **Odak ölçümü:** `araclar/kapak/odak.py` göz ilk nereye gider sorusunu ısı haritasıyla gösterir. Kapak test setindeki "belirginlik (odak noktası)" maddesine sayı verir. Tıklanmayı tahmin etmez: en kalabalık kapak Sisifos'unki ve en iyi tıklanan o; en temiz tek odak Milton'da ve TO düşük.
  - Kaynak ve araç kararları: `araclar/ADAYLAR.md`.

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
- **Sisifos, 8. gün:**
  - Erişim: toplam ~9.500 görüntüleme (5. günde 3.452'ydi), 99,7 B gösterim, TO %2,4 (hâlâ yükseliyor).
  - İzleme: tutma %41 (2:54), 0:30'da kalan %61.
  - Trafik: Göz at %78,4. Beğenme oranı %98,7.
  - Gösterim eğrisi 100 B civarında yavaşlıyor.
  - Bu video artık kanalın kapısı: Prometheus ve diğer videolar bitiş ekranı, sabit yorum ve oynatma listesiyle buraya bağlanır.
- **Kanaldaki diğer videolar:**
  - "Cumhuriyet'i Kuran Kuşak Nasıl Yetişti?" (29 Ekim; 6:20; kapak "KURUCU KADRO / AYNI SIRADA"): 15 saatte 61 görüntüleme.
  - "Şarlken: Dünyayı Teslim Eden İmparator" (21:27): 11 günde 147 görüntüleme.
    - 14. gün: toplam 1,0 B gösterim, TO %9,9.
    - Trafik: önerilen %44,7, kanal sayfası %29,5, göz at yalnız %13,2.
    - Yorum: YouTube videoyu hiç geniş bir göz atma testine sokmadı. Yayın sırasında kanalın kitlesi yoktu; şimdiki kitle (Sisifos) mit ve felsefe izleyicisi.
    - Paketleme fırsatı: videoda Kanuni ve 1529 Viyana bölümü var. Türk izleyici "Şarlken"i tanımıyor ama Kanuni'yi tanıyor. "Kanuni'nin rakibi tahtı neden bıraktı?" açısı doğru ve geniş kitleye açılır.
    - Doğruluk notu: 1529'da Viyana'yı savunan Şarlken değil, kardeşi Ferdinand'dı. Başlıkta "Kanuni'yi durduran" gibi bir iddia kullanılmaz.
    - Proje: `gunluk-shorts/sarlken-uzun-dosya/` klasöründe (Python motoru).
    - **Yeni paket (2 Kasım):** `sarlken_kapak/`.
      - Kapaklar: "KANUNİ'NİN RAKİBİ / TAHTI BIRAKTI" (madalyalar + bırakılmış taç), salon versiyonu ve mevcut kapak (kontrol).
      - Başlık: "Osmanlı'nın 'İspanya Kralı' Dediği İmparator: Şarlken Neden Vazgeçti?"
      - 11:03 bölümü "Kanuni" adını taşıyacak şekilde yeniden adlandırıldı.
      - Kurul dersleri: YouTube'un gerçek süre rozeti "önerilen" listesinde x 1440–1874, y 829–1034 alanını kaplar, bu bölgeye yazı konmaz. Çatlak taç "tahttan indirildi" anlamı verir; gönüllü bırakma için bütün, yere bırakılmış taç kullanılır. Şimdiye kadar en iyi sonucu mit ve felsefe videoları verdi. Bu bir süre kuralı değil; aşağıdaki "Süre" maddesine bak.
- **Prometheus ("Prometheus: Asıl Tutsak Ki…", kapak "BİLE BİLE ÇALDI"), yayından 5 saat sonra:**
  - Erişim: 484 gösterim, TO %5,8, 73 görüntüleme, 7,0 saat izlenme.
  - İzleme: ortalama 9:02. Kanalın en güçlü başlangıcı.
  - Trafik: Göz at %58,9, kanal sayfası %17,8, Önerilen %13,7. Kanal sayfası payı yüksek, yani Sisifos'la gelen izleyici geri dönüyor.
  - İlk saatlerin TO'su ve izleme süresi sadık kitleden geldiği için şişkin. Geniş kitleye açıldıkça ikisi de düşer; asıl karşılaştırma 3. ve 5. günde yapılır.
- **Prometheus, 45. saat:**
  - Erişim: yaklaşık 20. saatte büyük bir göz atma testi geldi; gösterim birkaç saatte ~1 B'den 18 B'ye çıktı, sonra düz kaldı.
  - TO %1,6 (ilk saatlerdeki %5,8 sadık kitledendi); Sisifos'un aynı aşamadaki oranıyla aynı.
  - Gösterim başına izlenme süresi (TO × ortalama izleme) 1,6 % × 6,7 dk ≈ 0,11 dk. Sisifos'ta 1,6 % × 2,9 dk ≈ 0,05 dk. Prometheus gösterim başına iki kattan fazla izlenme süresi getiriyor. Uzun videolarda bu ölçüt TO'dan daha anlamlı.
  - İzleme: 23:55'lik videoda ortalama 6:43 (%28,1). 0:30'da izleyicilerin %70'i kalıyor ("standart"), ama ilk dakikada ~%55'e iniyor.
  - Yorum: yükseliş durdu, çünkü geniş kitle testinde tıklama düşük kaldı. Sisifos'ta da dalgalar arasında ~1 günlük duraklama olmuştu.
  - Kural: 2–3 gün yeni dalga gelmezse paketleme (kapak ve başlık) kurulla yenilenir. Cumhuriyet'te bu yöntem işe yaradı.
- **Dört video yan yana (1 Kasım 2026):**

  | Video | Süre | 0:30'da kalan | Ort. izleme | TO | Gösterim |
  |---|---|---|---|---|---|
  | Sisifos (7. gün) | 7:05 | %63 | 3:10 (%44,8) | %2,2 | 85 B, hâlâ hızlanıyor |
  | Şarlken (13. gün) | 21:27 | **%79** | 8:58 (%41,8) | %10 (az gösterimde) | ~0,8 B; önerilen %38,6, kanal sayfası %35,1 |
  | Cumhuriyet (2. gün) | 6:20 | %65 | 2:45 (%43,5) | **%1,1** | 14,2 B'de durdu |
  | Prometheus (5. saat) | 24:00 | – | 9:02 (%37,6) | %5,8 | 484 (erken) |

  - **Tutma her uzunlukta %42–45:** anlatım ve görsel kalite darboğaz değil. Uzun video aynı oranı tutuyor, izlenme başına ~3 kat izlenme süresi getiriyor.
  - **Paketleme değişikliğinin sonucu (Cumhuriyet):**
    - Değişiklik: kapak "SULTANIN ÖĞRENCİSİ", başlık "Abdülhamid, Kendi Sonunu Getiren Kuşağı Nasıl Yetiştirdi?".
    - Sonuç: duran video yeniden açıldı. Görüntüleme 372'den 1.101'e, gösterim 14,2 B'den 18,5 B'ye çıktı.
    - Ömür boyu TO %1,1'den %1,5'e çıktı. Değişiklikten sonraki gösterimlerde TO kabaca %2,5–3 (tahmin).
    - Tutma %42,2'de korundu, yani yeni kapak yanıltmıyor.
    - Ders: yayından sonra kapak ve başlık düzeltmek ölü bir videoyu diriltebilir.
  - **Darboğaz paketleme (kapak ve başlık):** Sisifos'un gösterimi büyüdü, Cumhuriyet'inki %1,1 TO ile 14 B'de durdu (konusu da güne bağlıydı). Her videoda en az iki kapak hazırlanır ve "Test ve karşılaştır" ile denenir. Kapak kurulu "ilk bakışta anlaşılıyor mu?" sorusuna öncelik verir.
  - **En iyi açılış Şarlken'de (%79):** yeni videoların açılışı onunla karşılaştırılır.
  - **Kanal vitrin gibi çalışıyor:** diğer videolarda trafiğin %17–35'i kanal sayfasından geliyor. Sisifos kapı açıyor, izleyici kanala dağılıyor.
- **Milton ("Kayıp Cennet: Şeytan Cehennemden Neden Kaçamadı? | Milton"; 25:46; kapak "BEN CEHENNEMİM"), yayından ~15–18 saat sonra (12 Kasım 21:00'de yayımlandı):**
  - Erişim: 1,2 B gösterim, TO %1,7, 95 görüntüleme, ~15 saat izlenme.
  - İzleme: ortalama 9:30 (%37). Kanalın en yüksek ortalama izlemesi (Prometheus 5. saatte 9:02).
  - Gösterim başına izlenme süresi ≈ %1,7 × 9,5 dk ≈ 0,16 dk (Prometheus 0,11, Sisifos 0,05): kanalın en iyisi.
  - Yorum: ilk saatlerde bile TO düşük (Prometheus'un ilk saatlerinde %5,8'di); sadık kitle tıklamakta isteksiz ya da gösterim erkenden geniş kitleye gitti. Büyük göz atma testi henüz gelmedi (Prometheus'ta ~20. saatte geldi). Bakılacak: 48. saatte trafik kaynakları, 0:30'da kalan, ilk 3 sn (açılıştaki sessiz göz planı), "Test ve karşılaştır" sonucu.
- **Milton, ~1. gün sonu (13 Kasım akşamı):** 4,5 B gösterim, 171 görüntüleme (görüntüleme/gösterim ≈ %3,8; Studio'daki TO ayrıca bakılacak), ortalama 6:33 (%25). İzlenmenin %60'ı abonelerden: büyük göz atma testi henüz gelmedi (Prometheus'ta ~20. saatte gelmişti). Gösterim başına izlenme ≈ 0,25 dk (Prometheus 45. saatte 0,11). Ortalamanın 9:30'dan düşmesi kitle genişledikçe beklenen düşüş. Karar noktası 3. gün: yeni dalga yoksa paketleme kurulla yenilenir.
- **Milton Shorts** (37 sn; açılış: durağan büst + "O hâlde kimi suçlayacaksın?", en güçlü cümle "Ben cehennemim" 10. sn'de): 20. dakikada izlemeye devam eden %32; ~1.000 izlenmede %38, ortalama izleme 16 sn (%43). Ders: Shorts'ta en güçlü cümle ve en güçlü kare ilk saniyede olur; bağlam isteyen soru kanca değildir; 25–30 sn'lik sıkı kesit tercih edilir.
- **Kanal, 14 Kasım 2026:** ~500 abone. **Abone getiren videolar (kullanıcının Studio verisi):** Sisifos ~450, Prometheus ~90 küsur. `analiz/2026-11-11-studio-analizi.md`'deki "1000 görüntülemede abone" tablosu (Sisifos 9,1, Orfeus 24,7) dışa aktarım dönemine (13 Ekim–10 Kasım) bağlıdır ve Orfeus'unki küçük örnektir (689 görüntüleme); mutlak sayıda açık ara birinci Sisifos'tur. Abone sayısını Studio'nun video bazındaki "Kazanılan aboneler" kartından al. Sisifos 200 B gösterimi geçti, ~25 B görüntüleme. Medici (1/7) 8. günde ~300 görüntüleme, ~5 B gösterim, TO ~%1,5, ortalama 3:05 / 10:02 (~%30). Düşük tutmanın nedeni kanal cezası değil videonun kendisi: kullanıcı da "ne başı var ne sonu, isimlerden beynim allak bullak" dedi (`gunluk-shorts/DERSLER.md`). YouTube kanala değil videoya puan verir; Sisifos aynı kanalda 200 B gösterim aldı.
- **Milton, ~40. saat (14 Kasım 13:20; Studio'daki başlık artık "Milton'ın Şeytanı: "Ben Ceh…"; kullanıcı kapak testi sürerken yanlışlıkla değiştirmiş, 40. saat verisi iki başlığı karıştırır):**
  - Erişim: 4,5 B gösterim (1. gün sonuyla aynı), ömür boyu TO %1,4; günlük TO ~%1,5'ten ~%0,9–1,0'a indi. 189 görüntüleme (gerçek zamanlı; izlenme saati kartı ~10 saat gösteriyor, yani Analytics verisi gerçek zamanlıdan geride).
  - **Büyük göz atma testi gelmedi.** ~22.–26. saatte küçük bir test geldi (~2 B → 4,4 B), TO düşük kaldı, ~27. saatten beri gösterim düz. Karşılaştırma: Prometheus ~20. saatte 1 B → 18 B; Sisifos 18. saatte 4,7 B, 3. günde 22,2 B.
  - İzleme: ortalama 6:43 (%26,1); Prometheus'un 45. saatiyle dakikası dakikasına aynı (6:43, %28,1). 0:30'da kalan %68 (Prometheus %70, Sisifos %63, Şarlken %79). 1:00'da ~%58 (Prometheus ~%55). Eğri 5. dakikadan sonra yavaş iniyor: ~%40 (9–12 dk), Nifates (10:56–14:09) %39 → %37 düz, 18–25 dk ~%28–30, bitiş ekranında düşüş. Küçük artışlar ~3:25, ~6:15, ~8:25, ~22:00. **İçerik tutuyor; darboğaz ilk 10 saniye ve paketleme.**
  - Trafik: Göz atma %64 (abonelik akışı dahil; abonelik akışı tek başına 33 görüntüleme, %17), Önerilen %14,8, kanal sayfası %9, arama %4,8. İzlenme süresinin %54,7'si abonelerden (1. gün %60; Sisifos'ta %1,2). Türkiye payı %48,1 (Sisifos %73,6); altyazısız %33,5, Türkçe altyazı %20. Örnek küçük, diğer ülkelere ve altyazı dillerine ayrıca bakılacak.
  - Gösterim başına izlenme süresi = TO × ort. izleme = %1,4 × 6,7 dk ≈ **0,09 dk** (Prometheus 0,11). 1. gün sonundaki "0,25 dk" hesabı yanlıştı: TO yerine görüntüleme/gösterim kullanılmıştı; görüntüleme/gösterim TO değildir (abonelik bildirimi, kanal sayfası, dış kaynak gösterimsiz görüntüleme getirir).
  - Shorts A'nın (~1.000 izlenme) uzun videoya katkısı görünmüyor: trafik kaynaklarında "Shorts" satırı yok, en çok "Diğer" (15) içinde. Ders: Shorts kendi başına izlenme getirir ama 25 dk'lık videoya izleyici taşımıyor; Shorts uzun videonun tanıtımı sayılmaz, ayrı içerik sayılır.
  - **Karar (yayın sonrası analiz, 40. saat):** paketleme şimdi değiştirilmez. Kapak testi sürüyor ve 3. gün (15 Kasım akşamı, ~72. saat) kuralı geçerli. 72. saatte gösterim hâlâ ~4,5 B'deyse paketleme kurulu açılır. Kurulun başlangıç noktası: TO kapağın vaadinde değil ilk bakışta anlaşılmasında; "Milton" adı Türk izleyiciye Şarlken gibi yabancı. Konunun tanıdık kapısı Milton değil Şeytan'dır. Bu arada maliyetsiz kaldıraç: Sisifos'un (kanalın kapısı, ~100 B gösterim) bitiş ekranı, açıklaması ve sabit yorumu Milton'a bağlanır.
- **Milton, ~4. gün (17 Kasım, kullanıcının ekran görüntüleri):** 5,8 B gösterim (40. saatte 4,5 B; büyük göz atma testi yine gelmedi), TO %1,6. Ortalama 6:57 (%27,0). **0:30'da kalan %56** (40. saatte %68; Studio "standart değerin altında" diyor): kitle abonelerden yabancılara genişledikçe giriş kaybı büyüdü. Trafik: Göz atma %63, Önerilen %13,9, kanal sayfası %10,6, arama %5,3, diğer %7,3. Ders: ilk 48 saatin 0:30 değeri sadık kitleden şişer; videolar arası karşılaştırma aynı yaştaki (≥4. gün) veriyle yapılır.
- **İkaros ("İkaros: "Güneşe Yaklaşma." Peki Öteki Uyarı Neydi?"; 5:55; kapak "İKİ UYARI VARDI"), 47. saat:**
  - Erişim: 9,5 B gösterim (~10.–20. saatte küçük test, sonra düz), TO **%0,8** (kanalın en düşüğü), ~150 görüntüleme.
  - Trafik: Önerilen %39,1 (çoğu alakasız dizi/eğlence videoları), Göz at %38,5, arama %8,3, kanal sayfası %7.
  - İzleme: ortalama 2:12 (%37,3); **0:30'da kalan ~%40** (kanalda %63–79). Düşüş ilk 20 sn'de (A03 kancasından B02 "Romalı şair Ovidius'a göre…" serimine geçiş). 0:40–4:00 arası ~%33'te dümdüz: kalan izleyici F08'deki ifşaya kadar kalıyor. İki düşüş: ~4:06 (G01 "Bu hikâyede üç uçuş var": hikâye bitip yorum başlıyor) ve ~4:45 (G05–G06, soyut yorum).
  - **Düzeltilmiş okuma (17 Kasım, Studio "Kitleyi elde tutma" grafiği, ömür boyu ortalama yine 2:12, %37,3):** 47. saatteki eğri okuması fazla kötümserdi; ortalama %37,3 ile %33'lük bir düzlük birbirini tutmaz. Eğri: 0:20'de ~%53 (düşüş B02 Ovidius serimine geçişte), **0:30'da ~%48–50**, 1:00'da ~%41, **1:00–4:00 arası ~%40–42 düz**, G01–G05 yorumunda yalnız ~%42 → ~%35 (~5–7 puan), 5:15'ten sonra bitiş ekranı düşüşü. YouTube'un **"Önemli an" bölgesi ~1:07–2:31** (C04–E02): kanatların denenmesi, **kancanın cevabı (C06 "İşte unutulan uyarı", 1:23)**, babanın gözyaşı, uçuş ve düşüş. Yani: kancanın vaadi karşılandığı an izleyiciyi normalden uzun tutuyor; kayıp kancadan sonraki bağlam anlatısında; ifşadan sonraki yorumun bedeli küçük. Ortalama değişmediği için bu bir iyileşme değil, daha doğru okuma.
  - Ders: (1) İlk kez açılışta kayıp var; kanca sorusu cevaplanmadan bağlam anlatısına (kim, nerede) geçmek izleyiciyi düşürüyor. (2) İfşadan sonra yorum bölümü kısa tutulur ya da hikâyenin içine dağıtılır. (3) Önerilen trafiği alakasız videolardan gelince giriş düşüşü şişer; YouTube kitleyi bulamamış, bu da paketlemenin belirsizliğine işaret. (4) Kişisel soru başlıkta yoktu (talep kontrolü, bkz. son konuşmanın analizi).
- "Test ve karşılaştır" kazananı TO'ya göre değil izlenme süresi payına göre seçer. Test sürerken başlık değiştirilmez.
- **Kanal ortalaması (17 Kasım 2026, 9 uzun video; ayrıntı `analiz/2026-11-17-kanal-ortalamasi.md`).** Yeni video tek bir videoyla değil bu medyanlarla, aynı yaştaki veriyle karşılaştırılır:
  - Medyanlar: TO %1,8 (ilk 7 gün %1,7), ortalama izlenme %39,8, 0:10'da ≈%77, 0:30'da %61, ilk 7 gün gösterim ~25 B.
  - Göz atma testi yayından sonraki gün gelir (Sisifos 11,7 B, Prometheus 17,6 B, Abdülhamid 7,0 B); gelmezse video düz kalır. 48. saat ölçümü karar noktasıdır.
  - Son dört videoda (Medici, Milton, İkaros, Kafka) izlenme süresinin %36–56'sı abonelerden: YouTube bunları yeni izleyiciye götürmedi. Tutma bandı aynı kaldığı için sorun içerik değil, paketleme ve ilk 10 saniye (İkaros 0:10'da ≈%66).
  - Kapak testlerinin çoğu berabere bitti (Prometheus, Abdülhamid, Medici ~%50/%50); tek net kazanan Sisifos (%62,5), ardından ikinci dalga geldi. Test edilen kapaklar aynı fikrin iki yazılışı değil, iki ayrı vaat olur.
  - Abone sayısı Studio gelişmiş moddan alınır: Sisifos +240, Prometheus +44, Orfeus +17 (1000 görüntülemede 19,6), Milton +5 (16,6). Önceki "Sisifos ~450, Prometheus ~90" ekran okumasıydı.
- **Geniş kitle dersi (kullanıcının çıkarımı, 15 Kasım 2026):** kanalda geniş kitleye açılan tek video Sisifos oldu. Prometheus, Milton, Cumhuriyet ve Medici'de tutma iyiydi (0:30'da %63–70), ama geniş gösterim testinde TO %1–1,6'da kaldı ve dalga gelmedi; Cumhuriyet ancak kapak ve başlık değişince yeniden açıldı. Sisifos'ta iki şey birlikteydi: (a) Türk izleyicinin zaten tanıdığı popüler bir ad (Camus'nün Sisifos Söyleni), (b) izleyicinin kendi hayatına sorulan bir soru ("Neden mutlu hayal etmeliyiz?"). Milton'da (a) eksikti (ad yabancı; "milton" araması kasırgaya ve futbolcuya gidiyor), İkaros'ta (b) zayıftı ("ikaros" araması işaret fişeğine gidiyor; bilgi merakı vardı, kişisel soru yoktu). Bu yüzden her videoda senaryodan önce talep kontrolü yapılır ("Uçtan uca iş akışı", 1. adım). İlk sınama: Kafka, *Dönüşüm* (a güçlü, b güçlü); ikinci: Ran (a: tanıdık kapı "Kral Lear" başlıkta, b güçlü); sonuçları 48. saat ve 7. gün verisiyle buraya yazılacak.

## Kitle (Sisifos, 5. gün) ve kanal yönü
- **Kitle verileri:**
  - Ülke: Türkiye %73,6.
  - Altyazı: izleyicilerin %38,4'ü Türkçe altyazıyla izliyor. Her videoya doğru SRT şart. İngilizce altyazı %1,2, bu yüzden İngilizce dublaj düşük öncelikli.
  - Bağlılık: izlenme süresinin %98,8'i abone olmayanlardan, izleyicilerin %95,5'i yeni. Abone çağrısı doruk anına (~son dakika) ve bitiş ekranına konmalı.
  - Cihaz: telefon %48, bilgisayar %23, TV %22, tablet %6.
  - Cinsiyet: kadın %22,5.
- **Kanal yönü (kullanıcının kararı):** yalnız mitoloji değil, geniş bir alan: tarih, felsefe, psikoloji ve kitap, film ve dizi. Örnek aldığı kanal TED-Ed. Kanal kullanıcının arka bahçesi: amaç yalnız izlenme değil, ilgisini çeken fikirleri ve bakış açısını paylaşıp etkileşim almak. Hızlı büyüme için konu ve kaliteden ödün verilmez; büyüme kaldıracı paketleme, düzenli yayın ve her videoda tek soru biçimidir. Kanalı bir arada tutan konu değil biçim olacak:
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
- **Prometheus** (kullanıcının kararı). Durum: üretildi ve yayımlandı (`prometheus/yayin.md`, karar kaydı `prometheus/kurul/kararlar.md`, geriye bakış `prometheus/geriye_bakis.md`).
  - **Çıkış noktası:** Aiskhylos'un *Zincire Vurulmuş Prometheus*'u (İş Bankası Kültür Yayınları, Hasan Âli Yücel Klasikler). Kullanıcıyı asıl etkileyen, kitabın kendisinden çok Azra Erhat'ın önsözü; onun Prometheus'a bakışı videonun omurgası olacak.
  - **Önsözden yorum uydurma:** Erhat'a ait her görüş ve alıntı yalnız kullanıcının verdiği önsöz sayfalarından (fotoğraf ya da metin) alınır. Kaynak yoksa sorulur.
  - **Telif:** önsöz ve çeviri telif kapsamında (Erhat 1982'de öldü). Fikirler kendi cümlelerimizle anlatılır; kısa alıntılar kaynak gösterilerek yapılır. Açıklamaya künye yazılır.
  - **Konu yapısı:** Hesiodos'taki düzenbaz Prometheus, Aiskhylos'taki insanlığın velinimeti ve Zeus'un zorbalığına direnen Prometheus, ve Erhat'ın okuması.
  - **Üslup (kullanıcının kararı):** Sisifos'taki Yunan vazo resmi üslubu. Motor `sisifos/lib` yeniden kullanılır: `figure.js`, `style.js`, `core.js`, `anim.js`, `render.js` ve ses hattı. Proje `prometheus/` klasöründe kurulur, Sisifos dosyalarına dokunulmaz. Bu üslup "Mitler ve Felsefe" serisinin görsel kimliğidir. Prometheus ve kartal antik vazolarda gerçekten tasvir edilmiştir.
  - **Üslubun sınırı:** kodla çizimin güçlü olduğu alan siluet, profil figür, sahne kurgusu, ışık ve dönüşüm efektleridir; yüz, el ve karmaşık beden hareketleri zayıf yandır. Sahneleri buna göre kur: güçlü kompozisyon, az ama anlamlı hareket.
  - **Köprü:** Prometheus yeni alanlara köprü olarak kullanılabilir:
    - Mary Shelley'nin *Frankenstein*'ının alt başlığı "Modern Prometheus"tur (kitap bölümü).
    - Nolan'ın *Oppenheimer* filmi, *American Prometheus* biyografisine dayanır (film bölümü).
- **Milton, *Kayıp Cennet* ve Şeytan** (kullanıcıyla konuşularak netleşti, 1 Kasım 2026). **Durum (12 Kasım 2026):** film, iki kapak ve yayın paketi hazır (`milton/`, `milton/yayin.md`); kurgu kurulunun gerileme turu, Shorts ve yayın yapılmadı.
  - **Amaç:** "Şeytan haklı mıydı?" diye sormak değil. İzleyiciyi Şeytan'la empati kurduran bir **iç yolculuk** anlatmak.
  - **Ağırlık:** ağırlık Şeytan'da. Milton'ın hayatı kısa tutulur; yalnız eseri kör olduktan sonra kızlarına ve yardımcılarına yazdırması öne çıkar (kullanıcıyı en çok etkileyen ayrıntı).
    - Çerçeve fikri: kör bir şair, göremediği ışığı ve cehennemi anlatıyor. III. kitabın açılışındaki ışığa yakarış bunun için kullanılabilir.
  - **İki okuma çarpışır, karar izleyiciye kalır:**
    - Blake ve Romantikler: "Milton farkında olmadan Şeytan'ın tarafındaydı" (kullanıcı da buna yakın).
    - C. S. Lewis: Şeytan gururuyla küçülür; başmelekten karabataka, kurbağaya, en sonunda yılana döner.
  - **Başkaldırı teması:** kanalın ortak damarı (Sisifos, Prometheus, Şeytan).
    - Kullanıcının görüşü: tarihteki başkaldırıların çoğu kısıtlanan hak ve özgürlüklere karşıdır, ama istisnalar var (ör. Mussolini, İran 1979). "Başkaldırı her zaman özgürlük müdür?" sorusu bu inceliği taşır.
  - **Yalnız edebi okuma (kullanıcının kararı):** dinî karşılaştırma, ör. İblis, yapılmaz; video başta bunun Milton'ın destanının okuması olduğunu söyler.
    - Tanrı ve Oğul figürle çizilmez, ışık olarak gösterilir (Doré de böyle yapar).
  - **İç yolculuk planı (öneri; Kahramanın Yolculuğu kontrol listesiyle):**
    - **0. Kanca:** destan da olayın ortasında başlar. İlk 5 saniye yanan gölde açılan gözler ve bir merak sorusu.
    - **1. Sıradan dünya:** Cennet, Lucifer ("ışık taşıyan").
    - **2. Çağrı:** Oğul'un yüceltilmesi; kıskançlık ve gurur; isyan.
    - **3. Sınavlar:** cennetteki savaş, dokuz gün süren düşüş, Pandemonium ve şeytanlar meclisi.
      - **"Cennette köle olacağıma cehennemde kral olurum"** (I. kitap, 263) 1. perdenin sonunda menteşe olur.
    - **4. Büyük sınav ve duygusal doruk:** IV. kitaptaki Nifates Dağı iç konuşması, "Hangi yöne kaçsam cehennem; cehennem benim". Pişmanlık var ama gururdan eğilemiyor. Empatinin kurulduğu an burası.
    - **5. Bedel ve ödül:** Aden'e sızma, Havva; kazanırken kaybetmek.
    - **6. Kırılma:** X. kitapta şeytanlar yılana dönüşür (Lewis'in okuması).
    - **7. İksir:** Milton'dan sonra Şeytan "insanlaştı": Romantikler ve Cabanel'in *Düşmüş Melek*'i (1847, gözünde bir damla yaş). Son soru izleyiciye: o gözyaşı pişmanlık mı, gurur mu? Başkaldırı ne zaman özgürlük, ne zaman insanın kendi cehennemi?
  - **Üslup (kullanıcı bana bıraktı):** Gustave Doré'nin *Kayıp Cennet* gravürleri (1866).
    - Siyah-beyaz çelik/ağaç baskı, yoğun tarama ve çapraz tarama, ışık huzmeleri, düşen melek siluetleri.
    - Kodla çizime uygun: çizgi alanları, kontrast, siluet.
    - Yeni ilkeller kurulacak: tarama motoru, kanat, alev ve bulut gravürü. Önce tek üslup karesi kurula onaylatılır.
    - Cabanel tablosu kapanış sahnesi ve kapak adayıdır; telifli bir eser değil (1847).
    - Yüz yakın planları azdır ve gravür diliyle stilize edilir.
  - **Kaynak:**
    - Kullanıcı eseri Türkçe çeviriden okudu, çevirmeni hatırlamıyor.
    - Türkçe çeviriler telifli olabilir. Dizeler İngilizce özgün metinden (1674, kamu malı) kendi çevirimizle verilir; açıklamada kaynak yazılır.
    - Tarihler, kitap ve dize numaraları ve Milton'ın hayatına dair ayrıntılar senaryo kurulunda kaynaktan doğrulanır.
  - **Süre:** hikâye ne kadar gerektiriyorsa o kadar.
- **Film ve dizi videolarında:** film görüntüsü kullanma; oyuncuya benzeyen gerçekçi çizimden ve telifli karakter tasarımlarını kopyalamaktan kaçın. Kendi animasyonunla fikri anlat.

## Süreç dersleri (Prometheus'tan)
- **Kurul kapıları:** senaryo → seslendirme → üslup karesi → animatik → sahneler → ses/miks → kapak → Shorts.
  - Render ancak ses/miks ONAY'ından sonra başlar. Prometheus'ta ses kurulu geç açıldı; kesik kelimeler ("güvenmez" → "güvenme") ve kelimenin üstündeki motifler neredeyse yayına gidiyordu.
  - Shorts render'dan önce kurula gider. Prometheus'ta Shorts ilk turda 6,3 aldı.
  - ONAY'sız geçilen kapı kayda açıkça yazılır.
- **Kurula verilen "yaptım" iddiası** kare, ölçüm ya da diff ile verilir. Kurulun kendi önerisi de iddiadır: yan etkisi ölçülmeden uygulanmaz. Örnek: sabit müzik sınırlayıcısı dorukları 5–7 dB söndürdü.
- **Seslendirme kesimi:** Whisper kelime zamanları cümle sınırında üst üste binebilir. `build_vo.py` kesimdeki RMS'i denetleyip ilk gerçek duraklamaya keser; zaman çizelgesi değişmez.
- **Shorts'ta `notext`** filmin ekran yazılarını siler. Damga, künye ve kanca katmanı Shorts için ayrıca kurulur. Kadraj ve zemin geçişleri filmin kesmelerine kare kare eşlenir.
- **Teslim (Milton'da güncellendi):**
  - `SendUserFile` sınırı 400 MiB; Drive'a buradan yükleme sınırı 10 MB (büyük dosya Drive'a gönderilemez).
  - Kullanıcı telefondan büyük dosyayı indiremedi. Üç kopya hazırlanır: YouTube'a yüklemek için yüksek kalite (≤ 400 MiB), telefonda izlemek için H.265 küçük kopya (Milton: CRF 33, 25:46'da 143 MiB, SSIM 0,986) ve gerekirse ≤ 50 MB'lık parçalar (`ffmpeg -c copy -f segment`).
  - YouTube'a yüklemeyi kullanıcı bilgisayardan yapar; bu oturumda YouTube'a yükleme aracı yok.
- **Render'ı mutlak yolla başlat:** depo kökünde ilgisiz, eski bir `render.js` var.

## Üslup ve çizim motoru seçimi (kullanıcının kararı, 13 Kasım 2026)
Yeni videoda üslup seçilirken sıra şudur:
1. **Kendi motorlarımız:** gravür (`milton/lib`; en olgunu), vazo resmi (`sisifos/lib`, `prometheus/`), kâğıt kesme (`orfeus/`), Python motoru (`gunluk-shorts/`). Konuya uyuyorsa bunlardan biri yeniden kullanılır.
2. **Uymuyorsa cinecode, sonra Lemo:** cinecode tarifine bakılmadan önce de sonra da `araclar/lemo/KATALOG.md` açılır; Lemo'da 38 yeni üslup ve güncel motorlar var. Lemo 2.0'dan beri belgeleri (STYLE.md) CC BY-NC 4.0 lisanslı: okunur ve uygulanır, ama herkese açık bu depoya kopyalanmaz. Kodu MIT.
   **cinecode:** `.claude/skills/cinecode/styles/` içindeki 61 üslup tarifine bakılır. Her tarif hazır bir tasarım belgesidir: malzeme ve çizgi yasası, renk mantığı, yazı, hareket kalitesi, kamera dili, ses paleti, ortamın tuzakları ve motor notu. Motorun çerçevesi `references/engine.md` ve `starter/` (three.js ya da tek gölgelendirici).
3. **Yeni motor:** seçilen tarif yeni bir motora çevrilir. Motor **bizim hattımıza** takılır: anlatıma kelime kelime bağlı çekim sistemi (`milton/lib/film.js`: `S()`, `Wd()`, `plan()`), `render.js`, `tools/` ve kurul düzeni. cinecode'un kendi akışı (kendi soru turu, dış sesi, jürisi) kullanılmaz.
- cinecode tarifleri kod değil, tasarım belgesidir. Kodla çizimin zayıf yanı (yüz, el, karmaşık beden hareketi) orada da geçerli; tarif seçilirken Milton'daki üslup kapısı dersi uygulanır: manzara + orta plan figür + yakın plan + 15 sn hareket.
- **Figür yürüyor, koşuyor ya da bir şey taşıyorsa** `araclar/hareket/` kullanılır: `yuruyusYolu` (konum ve faz aynı integralden, ayak kaymaz), kol ve pelerin için `yayIzi`, asılı şeyler için `sarkacIzi`. Kurgu kuruluna `serit.js` şeridi kanıt olarak verilir. Mevcut motorlara dokunmaz; `film.html`'e tek `<script>` satırı eklenir.
- Motor yazmak videonun en pahalı aşamasıdır (Milton'da üslup kapısı altı tur sürdü). Hazır motor işe yarıyorsa yenisi yazılmaz.

## Orkestra düzeni ve Milton dersleri (kullanıcının kararı; 12 Kasım 2026)
Milton videosunda denendi, sonuç iyi; bundan sonra hep böyle çalışılır. Ayrıntı: `milton/geriye_bakis.md`, `milton/KURUL.md`.
- **Roller:** ana oturum yönetmen ve kurul başkanıdır; kararları kendisi verir, kullanıcıya her adımda sormaz. Çizim işleri alt ajanlara dağıtılır: her sahne setinin **tek sahibi** vardır ve aynı ajan düzeltme turlarında `SendMessage` ile sürdürülür. Zor çizim ve hassas kurul işleri büyük modele, ölçüm ve metin işleri küçük modele verilir.
- **Kullanım sınırı:** aynı anda en çok iki ağır ajan. Sınır dolunca ajanlar yarım kalır; sıfırlanınca `SendMessage` ile kaldıkları yerden sürdürülür, yeni ajan açılmaz.
- **Ortak dosyalar** (motor, `film.js`, `KILAVUZ.md`, plan listesi) yalnız ana oturumca değiştirilir; ajanlar kendi set dosyasına yazar. Durdurma kancası için ara durum sık sık commit edilir.
- **Kurula gitmeden önce** başkan bütün filmi `tools/kurgu_ozet.py` ile (her plandan bir kare) yan yana görür ve zayıf bölgeleri sahiplerine yeniden çizdirir.
- **Üslup kapısı** tek kare değil: bir manzara karesi + bir orta plan figür + bir yakın plan + 15 sn'lik hareketli sahne. Kodla çizimde iç çizgisiz açık figür "kâğıt kesme" okunur; ana figür koyu siluettir.
- **Plan listesinde her plana ölçek yazılır** (geniş / orta / yakın / ayrıntı / ters açı); ardışık iki plan aynı ölçekte olmaz. Yazı levhası plan başına en çok 8 sn ve filmin beşte birini geçmez; boş kâğıt 2 sn'den uzun kalmaz.
- **Geçiş:** aynı mekânda kesme; yumuşak geçiş yalnız mekân/zaman sıçramasında, kısa ve sessizlikte. İki levha saydamlıkla karıştırılmaz (gri üretir).
- **Hassasiyet kurulu görüntüye de bakar** (yalnız senaryoya değil): Milton'da yakaladıkları: sıra hâlinde eğilen figürler (namaz safı), baştan ayağa siyah örtülü kadın figürü, dört kollu yıldız (haç), göğsünde alev tutan önden simetrik figür (Kutsal Kalp), "ŞEYTAN AĞLADI" kapak yazısı (vaaz motifi), siluetin karnındaki küçük figür (hamilelik). Kapak yazısı da bu kuruldan geçer.
- **Kapak:** en iyi sonuç filmin ilk karesiyle aynı figür + tek vurgu rengi + Bebas Neue yazı (%18 harf yüksekliği). İkinci kapağın vaadi de ilk saniyede karşılanır (Milton'da film 0,9 sn'lik göz planıyla açılır).
- **Kredi:** seslendirmeden önce karakter sayısı × çekim sayısı hesaplanıp kullanıcıya bildirilir.

## İkaros dersleri (14 Kasım 2026)
Ayrıntı: `ikaros/geriye_bakis.md`, `ikaros/KURUL.md`.
- **İskelet baştan seçilmedi:** senaryo bölüm bölüm yazıldı; iskelet sonradan kurulda belirdi (Harmon çemberi, kahraman Daidalos; keklik Kişōtenketsu'nun "dönüş"ü; iki merak döngüsü). İşe yaradı ama tesadüfe bağlıydı; artık iskelet senaryodan önce seçilip kayda yazılır ("Uçtan uca iş akışı", 1. adım). Kayıt: `ikaros/uretim_plani.md`.
- **Yorum kullanıcıyla birlikte kurulur:** önce birkaç soru sorulur ("suçlu mu, kurban mı?", "hangi okuma seni etkiledi?"). Kullanıcının görüşleri kaynakla sınanarak omurgaya girer.
- **Bilinen hikâyede sürpriz kaynağın kendisindedir:** özgün metni (burada Ovidius'un Latincesi) satır numarasıyla depoya al ve kurula ver. Kaynak üyesi kendisi doğrular.
- **Üslup için önce hazır motor:** cinecode tarifi ve kaynağındaki MIT motor (`silk.js`) yeni motor yazmanın yerini tuttu; üslup kapısı 3 turda geçti.
- **Donuk plan yok:**
  - Sabit kadrajlı afiş planları donuk kalıyor; ilk kurguda filmin %25,7'si donuktu.
  - Her planın ilk saniyeden hareketi olmalı (varsayılan yavaş yaklaşma + sözcüğe bağlı eylem).
  - Kurgu kurulu kare farkıyla ölçer.
- **Palet ya da geçiş değişimi sözcüğe bağlanır ve plan içinde olur;** plan başındaki değişim kesmeye dönüşür, görünmez.
- **Karikatür okuması:** koyu siluet + bembeyaz göz + kıvırcık yuvarlak baş + çıkık ağız birleşimi kullanılmaz. Göz küçük ve sıcak tonda olur.
- **Kapak yazısı:** Bebas'ta büyük harf ≈ 0,70 em; %18 için 1080 ölçeğinde font ≥ 290 px.
- **Ekran yazısı ve künye alt banda (y > 880) konmaz;** orası altyazının yeri.
- **Kapta paket eksikse:**
  - Bu oturumda Whisper, scipy, soundfile ve pyloudnorm yoktu; `pip install` izin sisteminde reddedildi.
  - Kurulumsuz yollar `ikaros/` altında: `tools/hizala.py`, `audio/dsp_shim.py`, `tools/mix_ffmpeg.py`.
  - Kalıcı çözüm kullanıcıda: ortamın kurulum betiğine ya da izinlere `pip install openai-whisper scipy soundfile pyloudnorm` eklemek.
- **Kurul kısaltması (kullanım sınırı):** kapı başına iki birleşik mercekli üye işe yaradı. Ses/miks ve Shorts kurulsuz kalırsa bu kayda açıkça yazılır.

## Kafka dersleri (15 Kasım 2026)
Ayrıntı: `kafka/geriye_bakis.md`, `kafka/KURUL.md`, `kafka/uretim_plani.md`.
- **Talep kontrolü işe yaradı:** on dakikalık, bedava bir ölçüm. "dönüşüm kafka" otomatik tamamlamada özet, analiz, felsefe ve "animasyon" çıkarken "milton" ve "ikaros" konuya hiç ulaşmıyordu.
- **Kaynağın kendi kuralı üslubu çözebilir:** Kafka'nın "böcek çizilmesin" mektubu (25 Ekim 1915) hem merak döngüsü hem kodla çizimin zayıf yanının (beden) çözümü oldu; kamera yerden, izleyici Gregor'un yerinde.
- **Derinlik kaynaktaki az bilinen ayrıntıdan gelir:** kullanıcı "bu eser beni derin düşüncelere atmadı" dedi; omurga özetten değil satır numaralı ayrıntılardan kuruldu (gizli birikime sevinen Gregor, kardeşinin adını ağzına almayan Grete, tramvayda gerinen Grete). Yorumun omurgasını ("koşullu sevgi") kullanıcı seçti.
- **Ağaç baskı motoru:** cinecode `woodcut` demo motoru ES modülü; `tools/bundle_woodcut.py` ile tek klasik betiğe paketlenir. `mkStroke` tohumsuz çağrıda `Math.random` kullanıyordu; işçiler arası belirlenimcilik için nokta özetine çevrildi. Başsız Chromium'da WebGL2 çalışıyor (kare başına ~0,5 sn). Her kare: maske (siyah blok, ak oyuk) + kırmızı levha → baskı. Kenar boşluğu kâğıt ve sabit; alt boşluk (y > 900) altyazının yeri.
- **Siluet figür kuralları:** gövde kutu olmasın (omuz eğimi, dar bel, açılan etek ya da palto); kollar ayrı yol ve ince ak konturla gövdeden ayrılır; yakın planda baş kadraj içinde kalır (boy ≤ 1300 px), yoksa geriye "borular" kalır.
- **Numara kayması:** senaryodan cümle çıkarınca kimlikler yeniden numaralandı, plan listesi bir cümle kaydı ve oyulmuş soru anlatımla uyuşmadı. Plan listesi senaryo kesinleşince yazılır ya da çıkarılan cümlenin numarası boş bırakılır.
- **Bitiş ekranı:** anlatım "… ekranda" diyorsa o kelime bitiş ekranının (son 20 sn) içinde olmalı; `vo/plan.json` "sonra" buna göre hesaplanır.
- **Kredi harcayan çağrılar ve izin:** otomatik izin denetleyicisi yedi seslendirme çağrısından üçünü durdurdu (ücretsiz). Kullanıcı açıkça izin verince gönderildi. Kredi onayı çağrıdan hemen önce açık cümleyle alınır.
- **Dosya boyu:** ağaç baskının karede değişen mürekkep gürültüsü dosyayı şişirir (6:39 → H.264 310 MB, H.265 CRF 26 259 MB; telefon H.265 CRF 32 98 MB). Baskı gürültüsünü iki karede bir değiştir ya da teslimde `-tune grain` + yüksek CRF dene.
- **Kurulsuz üretim kullanıcının kararıydı** (kullanım %89). Bütün kapılar başkan denetimiyle geçti; kayıt `kafka/KURUL.md`. Kullanım açılırsa ilk tur: hassasiyet + kaynak.

## Ran dersleri (16 Kasım 2026; kanalın ilk film videosu)
Ayrıntı: `ran/geriye_bakis.md`, `ran/KURUL.md`, `ran/uretim_plani.md`.
- **Kural (kullanıcının kararı, İkaros 47. saat verisinden): kancadan sonra hikâye en geç ~0:45'te başlar; yapım/bağlam bilgisi kancanın arkasına değil, ilgili sahnenin yanına konur.** Ran yayından önce buna göre yeniden kurgulandı: yapım hikâyesi 0:23–1:22'den yanan kale sahnesinin arkasına taşındı, hikâye 1:24 yerine 0:42'de başlıyor. Yeni seslendirme gerekmedi: `ran/tools/build_vo.py` iki geçişli (cümleler çekimden gerçek duraklamada kesilir, `vo/sira.json` sırasıyla dizilir); cümleye bağlı planlar ve altyazı kendiliğinden kayar, sıraya dayanan müzik blokları ve bölüm başlıkları elle düzeltilir. Taşınan cümledeki gösterme sözcükleri ("bu noktada", "bu sahne") yeni yerinde göndergesini korumalı; korumuyorsa görsel köprü kurulur (Ran B05 → E07).
- **Talep kontrolü ikinci kez:** "ran" araması konuya ulaşmıyor (Milton düzeyi), "kurosawa" orta (*Düşler*), "kral lear" güçlü. Tanıdık kapı başlıkta öne alındı: "Yaptıkların Sana Döner mi? | Kurosawa'nın Kral Lear'ı". Sonucu 48. saat ve 7. gün verisiyle buraya yaz. **Yayın: 17 Kasım 2026, 18:00 (zamanlanmış); 48. saat = 19 Kasım 18:00, 7. gün = 24 Kasım.** Kapak testi A2 ve C.
- **Film videosunda telife üslupla cevap:** tek renk mürekkep + tek kırmızı, filmin renk kodlarını, kostümlerini, makyajını kendiliğinden dışarıda bırakır; yüzsüz xieyi figür oyuncu benzerliğini engeller. Yönetmenin telifli resimleri gösterilmez ve bu anlatıda söylenir. Filmden diyalog yok; alıntılar kamu malı kaynaktan (Shakespeare).
- **Gerçek görseller "yer yer":** yalnız CC0 / kamu malı. Met Open Access API (`collectionapi.metmuseum.org/public/collection/v1/objects/<id>`, `isPublicDomain`) lisansı tek çağrıda verir; eski `search` uç noktası kapandı (v1.1). Commons'ta oran sınırı var: `Special:FilePath/<ad>` + birkaç saniye bekleme. Japon fotoğrafı 1956 öncesiyse PD-Japan-oldphoto (ABD'de de kamu malı). Kayıt: `kaynak/GORSELLER.md` + `araclar/ASSETS.md` + açıklamadaki künye.
- **file:// görselleri WebGL tuvalini kirletir** (`Tainted canvases`): render ve kare araçları küçük yerel http sunucusuyla çalışır.
- **Önce ölç, sonra hızlandır:** yazılımsal WebGL'de (SwiftShader) birleştirici kare başına 4–8 sn tutuyordu, çizim ~10 ms. Yalnız konuma bağlı gürültü (kâğıt, fbm) ön geçişte dokuya yazılınca görünüm aynı kaldı (ortalama fark 4/255), süre ~10 kat kısaldı. Uzun render'dan önce tek karede çizim/birleştirme/JPEG sürelerini ayrı ölç.
- **Kullanıcının hatırladığı sahne kaynakla sınanır:** "sondaki flüt sahnesi"nde flüt kaybolmuştu; eksiklik kapanışın sessizliği oldu. "Körken çizdi" → "gözleri iyice zayıflamışken" (kaynak "neredeyse kör").
- **ElevenLabs:** kota yarıda bitebilir (reddedilen çağrı ücretlendirilmez); büyük üretimden önce kalan krediyi kullanıcıya sor. **Scribe'ın `estimate_only` tahmini ~16 kat düşük** (gerçek ≈ 5,5 kredi/sn): döküm yalnız en riskli bölüme.
- **Düzenleme sonrası sözdizimi denetimi:** `node -e "new Function(require('fs').readFileSync('dosya.js','utf8'))"`; render işçileri sayfayı başta yüklediği için ortadaki kod değişikliği yalnız sonraki render'a geçer (gerekirse `ONLY=` ile parça yeniden).
- **Kurulsuz üretim kullanıcının kararıydı** (kullanım %90). Kullanım açılırsa ilk tur: hassasiyet (Amida resmi, Kaede, Japon kültürü) + kapak.

## Kurgu önerileri (öneri, kural değil; 17 Kasım 2026)
Kaynak: Linus (@linus5x), filmlerini Claude'a çizdiren biri; X'te 5 maddelik liste, kullanıcı getirdi (1. madde ekran görüntüsünde yoktu). Kendi videolarının verisinden; örnek küçük, ama dördü kanalın kendi verisiyle örtüşüyor.
- **Her 3–5 saniyede ekranda bir yenilik; 30 sn duran kare izleyiciyi kaybeder.** Bizdeki karşılığı "donuk plan yok" (İkaros'ta ilk kurguda film %25,7 donuktu) ve "yazı levhası en çok 8 sn". Öneri: kurgu kurulu donukluğun yanında "kesme ya da sözcüğe bağlı eylem olmadan geçen en uzun süre"yi de ölçer; 5 sn'yi aşan aralıklar listelenir.
- **Sade tut: bir kahraman, bir karşıt güç, bir mekân, ekranda hep hareket eden tek bir şey.** Medici dersiyle aynı ("isimlerden beynim allak bullak"). Uzun videoda bölüm başına uygulanır: her bölümün tek kahramanı, tek karşıtı, tek mekânı.
- **Sesi kapat, yazıları ört: plan böyle anlaşılmıyorsa çalışmıyor.** Linus her planı yazısız ve sessiz olarak yeni bir yapay zekâya izletip "ne oluyor?" diye soruyor. Öneri, "sessiz okuma testi": kurgu özetinin kareleri (`kurgu_ozet.py`, `ozet.js`; ekran yazısız sürüm `notext` ile) plan listesini görmemiş yeni bir alt ajana verilir, her kare için ne olduğunu yazar; anlatılmak istenenle uyuşmayan planlar sahibine döner. Bu, kurulun "ilk kez gören izleyici" merceğinin ucuz bir hâlidir. İzleyicilerin %38'i altyazıyla izlese de görüntü tek başına anlaşılmalı.
- **Her şeyi hikâyenin içine koy: hikâye bitince izleyici gider.** Linus'un filmlerinde bitiş levhası çıkınca ~20 puan kayıp var. Bizde de aynısı ölçüldü: İkaros'ta "Bu hikâyede üç uçuş var" (G01) ile yorum başlayınca düşüş. Abone çağrısı, iksir ve bitiş ekranına yönlendirme hikâyenin son anının içinde verilir, ardından yorum uzatılmaz (İkaros dersi: ifşadan sonra yorum kısa ya da hikâyeye dağıtılır).

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

## 29 Ekim dersleri
- **Türk bayrağı (2893 sayılı Kanun ve cetveli):** Doğru çizim `cumhuriyet/lib/act6.js` içindeki `a6_flagImg`.
  - Yıldız merkezi = iç çemberin uçkurluk yanındaki kesişimi + G/3 + G/8. G = 60000'de 49250 olur.
  - Uçkurluk beyazdır. Hilalin dış konturu uçların arasında kapanmaz.
  - Kıvrım gölgesi is ile basılır, kırmızıyla değil; yoksa ay ve yıldız pembeleşir.
  - Dalgalı bayrak 1 px'lik şeritlerle çizilir; daha geniş şerit kenarda basamak bırakır.
  - Osmanlı bayrağında 1844'ten sonra beş köşeli yıldız vardır.
  - Bu hata üç kurul turunda gözden kaçtı. **Hassasiyet ve hukuk kurulunu sona bırakma, üslup karesi aşamasında çalıştır.**
- **Zaman çizelgesini kaydıran ses kararları** (cümle arası boşluk gibi):
  - Etkiledikleri yerler: tam render, bitiş ekranı saati (`yayin.md`, `youtube.md`), SRT ve Shorts EDL.
  - Bu yüzden ses kurulunu son render'dan önce bitir.
  - Yalnız miks değişirse render gerekmez; sesi yeniden bağlamak yeter.
- **ElevenLabs ses efekti:** `creative_generate_in_flow` süre parametresi almıyor. Kalabalık sesi 1 sn'lik dört çekim olarak geldi.
  - Belli bir süre gerekiyorsa node'u ekle, `duration_seconds` ver, sonra çalıştır.
  - Kısa çekimler 0,25–0,4 sn geçişle birleştirilebilir.
  - Sol ve sağ için iki ayrı sıra kullanılırsa stereo genişlik doğar.
- **Teslim boyutu:** Uygulamada 100 MB'ı aşan dosyada indirme düğmesi çıkmıyor (413 ve 153 MB'lık dosyalar inmedi, 83 MB'lık indi).
  - Uzun videonun ana kopyasından ayrıca 100 MB'ın altında bir yükleme kopyası üret.
  - Kullanılan ayar: `libx265 -preset medium -crf 26 -tag:v hvc1`, BT.709 etiketleri ve ses `-c:a copy`. Sonuç 83 MB, SSIM 0,980; YouTube kabul etti.
  - Yedek olarak H.264 iki geçiş, 1750k (~96 MB).
- **Shorts kırpması:** Üst künye kutusu ile bayrak ya da yüz arasında ≥ 30 px boşluk bırak.
  - Bunun için klipte `z0` ve `cy0` kullan; kırpmayı üste hizala (y0 = 0).

## Sonraki videolar için kullanıcının önerileri
- **Psikolojik anlatım:** Stefan Zweig (*Yıldızın Parladığı Anlar*) ve Dostoyevski gibi karakterin iç dünyasına inen bir anlatım.
  - 29 Ekim videosunda kayıt ve kurgu bittikten sonra önerildiği için uygulanmadı.
  - Senaryo en baştan bu üslupla kurulmalı: tek bir "karar anı" ve onu yaşayan kişinin iç dünyası.
  - İç dünya uydurulmaz. Kişinin kendi hatırat, mektup ve sözlerine dayanır; kaynak açıklamada verilir.
  - Atatürk için 5816 sayılı Kanun ve saygı kuralları gereği ona söz ya da düşünce uydurulmaz.
- **Kendi sesini klonlamak (14 Kasım 2026, ertelendi):** kullanıcı ekipmanı olmadığı için şimdilik istemedi; anlatıcı Emrullah kalıyor. İleride açılırsa sıra: önce hızlı klon (1–2 dk temiz kayıt, kanalın senaryolarından bir metin), Emrullah'la kör karşılaştırma, beğenilirse profesyonel klon (Creator planı, 30 dk–3 sa kayıt, canlı doğrulama, 3–24 sa eğitim). Ses değişimi seri ortasında değil yeni bir videoyla yapılır.
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
