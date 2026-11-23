# Video video süreç dersleri (Prometheus → Dorian Gray), teknik notlar, 29 Ekim, öneriler

> CLAUDE.md'den taşındı (23 Kasım 2026 sadeleştirmesi); metin değiştirilmeden. Geçerli kurallar CLAUDE.md'de; bu dosya ayrıntı ve geçmiş kayıttır.

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
- **Talep kontrolü ikinci kez:** "ran" araması konuya ulaşmıyor (Milton düzeyi), "kurosawa" orta (*Düşler*), "kral lear" güçlü. Tanıdık kapı başlıkta öne alındı: "Yaptıkların Sana Döner mi? | Kurosawa'nın Kral Lear'ı". Sonucu 48. saat ve 7. gün verisiyle buraya yaz. **Yayın: 17 Kasım 2026, 18:00 (zamanlanmış); 48. saat = 19 Kasım 18:00, 7. gün = 24 Kasım.** Kapak testi A2 ve C. **44. saat sonucu:** TO %3,0 (kanalın aynı yaştaki en yükseği), dalga yok; bkz. Ölçütler → Ran.
- **Film videosunda telife üslupla cevap:** tek renk mürekkep + tek kırmızı, filmin renk kodlarını, kostümlerini, makyajını kendiliğinden dışarıda bırakır; yüzsüz xieyi figür oyuncu benzerliğini engeller. Yönetmenin telifli resimleri gösterilmez ve bu anlatıda söylenir. Filmden diyalog yok; alıntılar kamu malı kaynaktan (Shakespeare).
- **Gerçek görseller "yer yer":** yalnız CC0 / kamu malı. Met Open Access API (`collectionapi.metmuseum.org/public/collection/v1/objects/<id>`, `isPublicDomain`) lisansı tek çağrıda verir; eski `search` uç noktası kapandı (v1.1). Commons'ta oran sınırı var: `Special:FilePath/<ad>` + birkaç saniye bekleme. Japon fotoğrafı 1956 öncesiyse PD-Japan-oldphoto (ABD'de de kamu malı). Kayıt: `kaynak/GORSELLER.md` + `araclar/ASSETS.md` + açıklamadaki künye.
- **file:// görselleri WebGL tuvalini kirletir** (`Tainted canvases`): render ve kare araçları küçük yerel http sunucusuyla çalışır.
- **Önce ölç, sonra hızlandır:** yazılımsal WebGL'de (SwiftShader) birleştirici kare başına 4–8 sn tutuyordu, çizim ~10 ms. Yalnız konuma bağlı gürültü (kâğıt, fbm) ön geçişte dokuya yazılınca görünüm aynı kaldı (ortalama fark 4/255), süre ~10 kat kısaldı. Uzun render'dan önce tek karede çizim/birleştirme/JPEG sürelerini ayrı ölç.
- **Kullanıcının hatırladığı sahne kaynakla sınanır:** "sondaki flüt sahnesi"nde flüt kaybolmuştu; eksiklik kapanışın sessizliği oldu. "Körken çizdi" → "gözleri iyice zayıflamışken" (kaynak "neredeyse kör").
- **ElevenLabs:** kota yarıda bitebilir (reddedilen çağrı ücretlendirilmez); büyük üretimden önce kalan krediyi kullanıcıya sor. **Scribe'ın `estimate_only` tahmini ~16 kat düşük** (gerçek ≈ 5,5 kredi/sn): döküm yalnız en riskli bölüme.
- **Düzenleme sonrası sözdizimi denetimi:** `node -e "new Function(require('fs').readFileSync('dosya.js','utf8'))"`; render işçileri sayfayı başta yüklediği için ortadaki kod değişikliği yalnız sonraki render'a geçer (gerekirse `ONLY=` ile parça yeniden).
- **Kurulsuz üretim kullanıcının kararıydı** (kullanım %90). Kullanım açılırsa ilk tur: hassasiyet (Amida resmi, Kaede, Japon kültürü) + kapak.
- **Yayın sonrası dersler (44. saat eğrisi):**
  - **Kural: kancadan hikâyeye köprü sıfır cümle.** İkaros, Kafka ve Ran'da aynı yerde sızıntı: kanca sorusundan sonraki ilk cümle hikâyenin ilk cümlesidir. Kimlik bilgisi (ad, yıl) kancanın içinde tek cümle olabilir; kaynak karşılaştırması ve "şunu ekledi" türü merak sözleri hikâyenin içine dağıtılır. Merak sorusu kalacaksa izleyicinin göreceği somut bir şeyi vaat eder (Kafka'nın "böceği hiç görmeyeceksiniz" sözü eğriyi yükseltti, Ran'ın soyut "Shakespeare'in vermediği şey"i yükseltmedi).
  - **Kural (67. saat; Ran'da üç nokta, İkaros'ta iki): somut olay tutar, soyut çözümleme düşürür.** Ran'ın üç kaybı (0:31 köprü, 1:44 "üç kız / üç oğul", 2:20 "eklediği şey: geçmiş") Kurosawa–Shakespeare karşılaştırması ve kavramı; en iyi tutan yer ("Önemli an" 3:25–4:54) somut yapım anekdotu. Ayrım "hikâye mi bilgi mi" değil, somut mu soyut mu. Bilgi bir olay, nesne ya da sahne olarak verilir; karşılaştırma ve çıkarım olaydan sonra tek cümle olur, paragraf olmaz.
  - **Kural: merak döngüsünün cevabı bir olaydır, kavram değil.** Ran'da "Shakespeare'in vermediği şey" sorusunun cevabı "geçmiş" kavramı oldu ve Studio'nun işaretlediği düşüş tam orada (2:20–2:32). Cevap olayla verilir ("Hidetora yıllar önce Kaede'nin ailesini kılıçtan geçirmişti"), kavram ardından tek cümle.
  - **Doğrulandı: yapım/bağlam bilgisi ilgili sahnenin yanına konur** (bu bölümün ilk maddesi). Kancanın arkasında kaybettiren bilgi türü, yanan kale sahnesinin hemen ardında "Önemli an" oldu.
  - **İpucu (Medici dersiyle aynı yönde; güçlendi): doruğu taşıyacak kişiler ilk perdede adı ve görüntüsüyle ekilir.** Gövdenin büyük düşüşü Tsurumaru ve Sue'nun 5. dakikada adları ve geçmişleriyle girdiği yerde (4:54 %39 → 5:33 %28); hemen önceki Nō yorumu düşürmedi.

## Mary Stuart dersleri (18 Kasım 2026)
Ayrıntı: `mary-stuart/geriye_bakis.md`, `mary-stuart/KURUL.md`, `mary-stuart/uretim_plani.md`.
- **Gerçek görseli tam boyutta, her köşesine bakarak incele.** Finden gravürünün köşesindeki küçük ek resim idam anını (balta, kütük) gösteriyordu ve dört plana taşınmıştı; render başladıktan sonra fark edildi, örtüldü (`fotoP` → `ort`). Kurgu özeti 480 px'te bunu gizler; hassasiyet taraması tam boy karede yapılır.
- **Tek rengi gravüre boyarken:** koyuluk maskesi (yalnız koyu kumaş) + yumuşak kenar + el ve nesneleri çıkarma. Düz çokgen "yapıştırılmış kâğıt", çizgiyle çarpılan koyu kıvrım ya da nesnedeki leke "kan" okunur (Fable kapakta yakaladı).
- **Görüntüde hassasiyet:** havaya kalkmış düz kollar (dans) selam gibi, simetrik açık kanatlı kuş amblem kartalı gibi okunur. Figür pozları ve amblemler render'dan önce bu gözle taranır.
- **Sessizliğe dayalı hizalama** (Whisper yok): iki cümleli satırlar alt cümlelere bölünerek hizalanır; iki nokta ve tırnak öncesi duraklamalar satır sınırı sanılabilir, cümle başına harf/sn aykırılığıyla bulunur ve `vo/sinir.json` ile elle zorlanır. Rakamlı cümlelerde altyazı eşlemesi `tools/merge.json` rakamdan otomatik üretilir.
- **Yazılımsal WebGL'de önce ölç:** Redraw'ın dört bulanıklık geçişi tek iki kanallı geçişe, ağırlıklar JS'e, tarama dallanmayla yalnız karanlığa: 0,95 → 0,55 sn/kare. Canvas `filter: blur` her çizimde pahalı (bulut 22 sn/kare): düşük çözünürlüklü tuvale çiz, büyüt. Gri/kontrast süzgeci görüntü başına bir kez (`griOn`).
- **Sessiz film 15 kare/sn:** bütün görüntü saniyede 15 kez güncellenir; 30 kare/sn çıktıda kareler ikişer aynı, render yarı süre ve kodlayıcı tekrar kareyi bedava saklar. Aynı tarayıcıdaki sayfalar tek GPU sürecini paylaşır; paralel render ayrı tarayıcılarla (`render.js` işçileri).
- **Kart dili:** sessiz film ara yazıları kişilerin kendi sözlerini taşır (iç dünya uydurulmaz kuralıyla aynı yöne çalışır); bölüm kartı bölüm sorusunu taşır. Kartlar sürenin %17'si, her biri ≤ 8 sn (`tools/kontrol.js`).
- **Paketleme:** talep kontrolünde en güçlü kapı başlıkta öne alınır (akış ~45–50 karakterde keser). Kapak A'da çizilmiş dev siluet "satranç taşı" okundu; gerçek madalya profili (Elizabeth) çözdü: tanınan bir yüz yoksa tanınan bir dönem nesnesi.
- **Yayın (kullanıcı kesinleştirdi, 18 Kasım):** 20 Kasım 2026 Cuma 18:00. **48. saat = 22 Kasım 18:00, 7. gün = 27 Kasım.** Ran'ın 48. saat ölçümüyle (19 Kasım) çakışmasın diye bir gün sonrası. Kapak testi A ("RAKİBİNE SIĞINDI") ve B ("İDAMINA KIRMIZI GİYDİ"). Sonuçlar buraya yazılır; talep kontrolünün üçüncü sınaması (a: "I. Elizabeth" güçlü, b: güçlü).
- **Seslendirme yaması (kullanıcı onayıyla, 1.330 kredi):** kaynak denetiminde kalan beş anlatım sapması (tarih, fiil, zaman, "daha") tüm seslendirme yenilenmeden düzeltildi: cümle önünde bir bağlam cümlesiyle okutulur, bağlam kesilir, yeni cümle eski klibin yerine konuşma başı aynı ana gelecek biçimde oturtulur (`mary-stuart/tools/yama_vo.py`). Zaman çizelgesi kaymaz; müzik ve efekt yeniden üretilir, yalnız ilgili parçalar yeniden render edilir. Sığmazsa hız değil iç duraklama kısaltılır. Düzey eski cümleye, eski okuma bilerek farklıysa (haykırış) komşulara eşitlenir. Ders: kaynak denetimi seslendirmeden önce yapılır.
- **Shorts (23 Kasım ölçümü):** Elizabeth Shorts'unda izlemeye devam eden %27 (Milton Shorts %32–38): kanalın Shorts'ları akışta kaydırılıyor; düşük izlenme algoritma cezası değil, ilk saniye sorunu. Yatay filmden kırpılan Shorts dikey akışta küçük ve durgun kalıyor; ilk karede hareket ve büyük tek görüntü yoksa YouTube birkaç yüz kişiden sonra göstermeyi bırakır. Sonraki Shorts ya dikey için kurulur ya da hiç yapılmaz (ölçüt: izlemeye devam eden ≥ %60).
- **Kurulsuz üretim kullanıcının kararıydı;** Fable iki kez (senaryo, paketleme). İki rapor da engelleyici bulgu getirdi (ters aktarılmış Zweig hükmü; kan gibi okunan kırmızı): senaryo ve paketleme kapılarında danışman pahasına değer.

## Dorian Gray dersleri (19 Kasım 2026)
Ayrıntı: `dorian-gray/geriye_bakis.md`, `dorian-gray/uretim_plani.md`.
- **Piyano sentezinde alçak nota hatası (Mary Stuart'tan devralındı):** MIDI < ~37'de sönüm katsayısı negatife düşüp notayı patlatıyor, normalleştirme bütün müziği kısıyordu. **Mary Stuart müziksiz teslim edilmişti** (1.249 sn'nin ~14'ünde müzik); yayından bir gün önce düzeltilip film, YouTube kopyası ve Shorts yeniden üretildi (`mary-stuart/KURUL.md`). Düzeltme `dec = max(.3, …)`. **Kural: her müzik üretiminden sonra saniye saniye düzey eğrisi basılır** (medyan, "−60 dB üstü saniye"); miks LUFS'u bunu göstermez (ebur128 sessizliği kapıdan atar, anlatım ölçümü taşır).
- **Müzik seçimi (kullanıcının kararı, 20 Kasım 2026):** seriye ya da kategoriye bağlı ortak bir müzik yok, kural da öneri de konmaz. Her videonun müziği o videonun tonuna, hikâyesine ve anlatımına göre o an düşünülerek yazılır (Mary Stuart'ta ve Dorian'da yapıldığı gibi): aynı seride farklı, farklı serilerde benzer müzik olabilir. Kullanıcı Mary Stuart'ın düzeltilmiş müziğini çok beğendi ("müziksiz atsaydım video etkisini yitirirdi"); bundan sonra müziğin gerçekten duyulduğu teslimden önce ölçülür (yukarıdaki düzey eğrisi) ve kulakla dinlenecekler listesine yazılır.
- **Karma üslup:** fikir görüntünün kuralı olunca (yalnız tablo renkli, yüz yalnız tabloda) kodla çizimin zayıf yanı (yüz) tek yerde, ressamın elinde toplanır.
- **Kıyafet ayrıntısı da hassasiyettir:** siyah giysinin ortasındaki küçük beyaz dikdörtgen papaz yakası okundu (Fable). Dönem kıyafeti tanınır öğelerle çizilir (gömlek önü, yaka uçları, fular).
- **İç içe `GR.frame` göreli değil:** milton motorunda çerçeve içinde çerçeve açmak mutlak koordinata döner; parmak gibi alt parçalar elle döndürülür. Belirti: parça hiç görünmez, kalan şekil anlamsızlaşır.
- **Bitiş ekranı tarifi son karenin kendisinden yazılır** (plan listesinden yazılan tarif boş yarıyı ters gösterdi).
- **Başlık uzunluğu karakterle sayılır:** 54 karakterlik başlık mobilde sorunun ortasında kesiliyordu; tanıdık kapı + soru 42 karaktere sığdı.
- **Fable'ın tek son yorumu (kullanıcının düzeni):** iki engelleyici bulgu (yaka, bitiş ekranı) ve dört görüntü düzeltmesi getirdi; bir saatlik bedeli yayın öncesi yeniden üretimle karşılaştırıldığında ucuz. Bulgu "iddia" olarak alındı, her biri karede doğrulandı; bir düzeltme denemesi (cinayette öne uzanan kol) yeni bir kusur doğurduğu için tekrar çizildi.
- **Paralel render yerine öncelik:** iki film aynı 4 çekirdeği paylaşırken, yarın yayımlanacak olanın kodlaması için öteki render'ın süreçleri `kill -STOP` ile durdurulup sonra `-CONT` ile sürdürüldü; Playwright işçileri sorunsuz devam etti.

## Lale Çılgınlığı dersleri (22 Kasım 2026)
Ayrıntı: `lale-cilginligi/geriye_bakis.md`, `lale-cilginligi/uretim_plani.md`, `lale-cilginligi/kaynak/DOGRULAMA.md`.
- **Türkçe boşluk ölçütü (kullanıcının ölçütü) talep kontrolüyle çelişmez:** konu ("lale çılgınlığı") Türkçede aranmıyor (2 öneri), ama tanıdık kapı "lale" ve okuldan bilinen "Lale Devri". Kapı başlıkta konu adının ilk sözcüğü olarak öne alındı; "Lale Devri" araması diziye ve şarkıya gittiği için başlığa değil açıklamaya, bölüm adına ve etikete girdi. Sonuç 48. saatte `analiz/2026-11-22-turkce-bosluk.md`'ye yazılır.
- **Kaynak taraması senaryodan önce bir efsaneyi ikiye böldü:** TDV'deki "Ekim 1722 narh fermanı" sicilde bulunamadı; Aktepe'nin (1953–54) yayımladığı belgeler 28 Haziran 1726 (239 lale, en pahalısı 50 kuruş) ve Ağustos 1727 (aynı lale 200 kuruş). Ahmed Refik'in "500–1000 altın" rivayetine Aktepe "belge yok" diyor: ikinci efsanenin somut kanıtı, Mackay'in denizcisinin ikizi. **Ders:** ansiklopedi maddesindeki tarih, maddenin kaynağına kadar izlenir; arşiv belgesini yayımlayan makale bulunursa (dergipark) o esas alınır.
- **Fable senaryo kapısında yine engelleyici bulgu getirdi** (Mary Stuart ve Dorian gibi): Ahmed Refik'e yanlış rol biçilmişti (dönemi kınamadı, övdü); "Lale Devri hiç yaşanmamıştır" alıntısı bağlamsız kalıyordu; Goldgar yarım aktarılmıştı (kriz paranın değil tutulmayan sözlerin krizi); kapak A'nın "ev" vaadi senaryoda hiç karşılanmıyordu. Okunuş hataları da yakalandı ("Anne Goldgar" Türkçe "anne" okunur → "En"; "bir Ekim gecesi" → "Ekim'in ilk gecesi"). **Kural önerisi:** seslendirmeden önce Fable'ın tek okuması (puansız bulgu listesi) kanal düzeni olsun.
- **Kapağın vaadi senaryoda bir cümleyle karşılanır:** "BİR EV FİYATINA" kapağı için A05'e "Haarlem'de beş küçük ev parası" eklendi (1.000 gulden = küçük ev, Ocak 1637 fiyatı). Kapak taslağı senaryodan önce yazılsa da senaryo kapakla yeniden karşılaştırılır.
- **Hassasiyet taraması görüntüde yeni üç şey yakaladı (kod çizimi kendiliğinden üretiyor):** (1) siyah kaftanın önündeki açık dikey şerit + yatay kuşak = **haç**; (2) koyu kalabalıkta beyaz sivri börk = kukuleta (KKK) okuması; (3) kemerin ortasında asılı kandil = mihrap. Kaftan önü şeritsiz, kuşak geniş ve koyu; börk kullanılmaz; kapılar düz, fener yanda. Gerçek görselde (Mallewagen 1637) alegorik figürlerin açık göğsü ve sol üstteki kilise kulesi kırpmanın dışında bırakıldı; yalnız iki güvenli ayrıntı kullanıldı.
- **Scribe çağrısını otomatik izin denetleyicisi durdurdu** (tahmin 0 kredi olsa da). Kurulumsuz cümle hizalaması (`hizala_cumle.py`, sessizlik + harf uzunluğu) yeterli oldu; tek aykırılık (hızlı okunan cümle) hız bandıyla bulundu ve öbür çekim seçildi. Kulak denetimi kullanıcıda.
- **Ekran yazısı alt bandı:** künyeler ilk taslakta y ≈ 980'e kondu; kural (y > 880 altyazının yeri) render'dan önce bütün plan dosyasında tarandı. Kural aracı: `over` içindeki y değerleri > 880 olan çağrılar.
- **Renk = değer kuralı kodda tek parametre:** `LALE.boya(ctx, cam, renk)`. Çöküşte ve 1730'da `renk` 1 → 0; sonda kitap sayfalarında 0 → 1. Görsel kural fikir taşıdığı sürece karma üslup (Dorian'dan sonra ikinci kez) tekrar gibi okunmaz; kapakta da renk yalnız lalede.
- **Fable'ın izleyici gözüyle son okuması (kullanıcının isteği, 22 Kasım; ayrıntı `lale-cilginligi/uretim_plani.md` → Fable danışmaları 2, raporlar `lale-cilginligi/fable_son_okuma/`):** render'dan sonra üç izleyici kişiliği (telefonda sabırsız öğrenci, TV'de abone, konuya başka kapıdan gelen yetişkin) zamanlı izleme günlüğü yazdı; malzeme 2 sn'de bir kare + altyazı, tam boy plan kareleri, zamanlı metin, saniye saniye hareket ve ses düzeyi. **Tek kişinin düşüşü zevk, üçünün ortak düşüşü bulgudur;** ortak düşüşler kanalın kendi derslerinin yerleriydi (kancadan sonra ön hikâye, hikâye bitince "video bitti" hissi, art arda belge, tek planda soyut tez). Mercek bulguları (hassasiyet, kaynak, paketleme) ayrı doğrulayıcılarla karede ve kaynakta sınandı; birkaçı çürüdü. **Öneri: her videoda yayından önce bu okuma** (seslendirmeden önceki senaryo okumasıyla birlikte iki Fable kapısı). Seslendirme sabitken düşüş yerleri görüntüyle (yeni plan, sözcüğe bağlı olay) karşılanır.
- **Çarpma boyası katman sırası bilmez:** el boyaması lale, önünden geçen figürün elini ve yüzünü de boyuyordu ("kanlı el" okuması). `lib/lale.js` artık lale kuyruğa girdikten sonra çizilen her opak şekli kaydedip boyayı orada siliyor (örtü maskesi). Karma üslupta renk katmanı her zaman örtüyle basılır.
- **Künye paneli hatası (Milton ve Dorian'ın `film.js`'inden devralındı):** `txt()` koyu paneli hizadan bağımsız çapaya ortalıyordu; sola hizalı künyenin sağ yarısı açık zeminde okunmuyordu. Lale'de `softBand` ile düzeldi (Narkissos'ta ayrıca düzeltilmişti). Dorian'ın kodu da 23 Kasım'da düzeltildi, ama yayına giden dosya eski: üç künye kısmen okunmuyor (0:12 yıl, 0:44 "LORD HENRY", 6:51 yıl); **kullanıcının kararı: Dorian yeniden yüklenmez** (YouTube dosya değiştirmeye izin vermiyor; kusur küçük, anlatım aynı bilgiyi veriyor). Yeni videoda `film.js` Lale'den alınır.
- **Alt bant ölçümle denetlenir:** `lale-cilginligi/tools/alt_bant.js` her planın üç karesinde çizilen bütün yazıların (`fillText`) cihaz y'sini ölçer; kod taraması çizim katmanındaki yazıları (`YAZI.ekle`) kaçırmıştı.
- **Her düzeltme yeni bir simge üretebilir:** bu turda düzeltme sırasında başın yanında açık bohça (hale), belde çizgili oval (kalkan), alna giden el (selam), halka taramalı kabuk ve yastık (hedef tahtası) çıktı. Düzeltilen her plan tam boy karede yeniden bakılır; halka tarama ("rad") yuvarlak nesnede hedef okunur. Gerileme okuması (23 Kasım) aynı deseni sarık, kese, para, halat, mühür ve sandıktaki soğanlarda da buldu; kök nedeninden kaldırıldı (soğanda boyuna kabuk çizgisi). **Yeni sette yuvarlak nesneye halka tarama verilmez.**
- **Gravür videosunda teslim kopyası:** ince tarama kodlayıcıyı şişirir; x265 CRF 26 10 dakikada 266 MB verdi. 100 MB altı kopya iki geçişli sabit bit hızıyla üretilir (`-b:v 1150k`, 2 pass); YouTube kopyası H.264 CRF 22 (~345 MB).
- **Kullanıcının renk önerisi ("daha renkli olsa?") kapakta uygulandı, filmde değil:** izleyicilerin üçü de filmdeki renk kuralını övdü, kapak A'yı soluk buldu. Kapakta lale büyük, alevler kalın, iki kat boya.

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
- **Fikir sorma ve bakış açısı (kullanıcının kararı, 22 Kasım 2026):** yeni videonun açısı kurulurken kullanıcının kendi fikirleri sorulur (konu seçiminden sonra, iskeletten önce; kısa sorular, seçenekli). Amaç herkesin yaptığı anlatım değil, farklı bir bakış; ama **sıkıcı olmamalı** (somut olay kuralı geçerli). Öne alınacak üç bakış:
  - **Kaybedenin gözünden:** kazananı değil kaybedeni ya da sıradan bir insanı (yetim çocuk, eskici, kâtip) merkeze almak;
  - **Bir nesnenin yolculuğu:** lale gibi bir nesneyi kurye yapmak (kahve, kâğıt para, saat, bir kitap…);
  - **Bildiğimiz hikâyeyi bozmak:** okulda öğrenilen bir anlatının arşivde başka çıkması (Lale Devri adı, Mackay'in denizcisi).
  Lale Çılgınlığı ikinci ve üçüncüyü birlikte kullandı; sonraki konu taramasında adaylar bu üç bakışla da puanlanır.
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
