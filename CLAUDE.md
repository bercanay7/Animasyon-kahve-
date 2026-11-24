# Zaman Kuryesi: animasyonlu video üretim rehberi

Bu dosya her oturuma kendiliğinden yüklenir. Bu yüzden içinde yalnız **bugün geçerli kurallar** ve **neyin nerede durduğu** var.
- Geçmiş ölçümler, video video dersler ve eski yöntemler `kanal/` altında; gerektiğinde açılır.
- **Bu dosyayı kısa tut:**
  - Yeni bir ders önce o projenin `geriye_bakis.md` dosyasına yazılır.
  - Buraya yalnız birden çok videoda doğrulanmış ya da kullanıcının koyduğu kural girer.
  - Ölçüm kayıtları `analiz/` altına gider.
- Bir motoru ya da aracı yeniden kullanırken o projenin `geriye_bakis.md`'si ve `kanal/DERSLER.md`'deki bölümü okunur.
- Sadeleştirme: 23 Kasım 2026, eski metin satırı satırına `kanal/` içinde.

## Kanal ve kullanıcı
- **Kanal:** YouTube'da "Zaman Kuryesi" (@ZamanKuryesi). Türkçe animasyonlu anlatım: mit, tarih, felsefe, psikoloji, kitap, film.
  - Örnek aldığı kanal TED-Ed.
  - Kanalı bir arada tutan konu değil biçim: animasyonlu anlatım, tek büyük soru, Emrullah sesi, "geçmişten bugüne soru taşıyan kurye" fikri.
  - Kanal kullanıcının hobi alanı: amaç yalnız izlenme değil, ilgisini çeken fikirleri paylaşmak. Büyüme için konu ve kaliteden ödün verilmez; kaldıraç paketleme, düzenli yayın ve tek soru biçimi.
- **Oynatma listeleri:** Mitler ve Felsefe · Tarihin Dönüm Noktaları · Kitapların Sorduğu Sorular · Ekrandaki Felsefe.
- **Kullanıcı:**
  - Türkçe yazar, kararlarını kısa verir ("Üret", "Devam edelim"). İşin baştan sona yapılmasını ister.
  - Önerilerini öneri olarak verir; uzman gözüyle tartılmalarını bekler ("karar sana ait", "sen patronsun").
  - Uymayan öneri gerekçesiyle geri çevrilir, uygunsa sonraki işe not edilir. Onu memnun etmek için öneri kabul edilmez.
- **Yayın:** YouTube Studio'da kullanıcı elle yapar.
  - Dosyalar `SendUserFile` ile gönderilir; her video için adım adım bir `yayin.md` yazılır.
  - **Takvim (23 Kasım):** dört günde bir uzun video, 18:00. Narkissos 24 Kasım, Dorian Gray 28 Kasım, Gılgamış 2 Aralık, Lale Çılgınlığı 6 Aralık.
  - Önceki videonun 48. saat ölçümü yeni video yayına girmeden alınır.
- **Anlatıcı:** ElevenLabs'te **"Emrullah"**. Kanalın sesidir, değiştirilmez. `voice_id` her seferinde `creative_list_voices` ile bulunur, ezberden yazılmaz.
- **Kredi harcayan üretim** (ElevenLabs, Abracadabrax): yalnız kullanıcı açıkça istediğinde.
  - Önce karakter × çekim hesabı ve kalan kredi kullanıcıya bildirilir; onay çağrıdan hemen önce açık cümleyle alınır.
  - Aynı çağrı "yeniden dene" diye tekrarlanmaz; her tekrar yeniden ücretlendirilir.
  - Scribe'ın `estimate_only` tahmini ~16 kat düşük (gerçek ≈ 5,5 kredi/sn).
- **Süre:** sabit sınır yok; hikâye ne kadar gerektiriyorsa o kadar. Tutmayı sağlayan süre değil tempo.
- **Kitle (Sisifos verisi):** telefon %48, TV %22. İzleyicilerin %38'i Türkçe altyazıyla izliyor: her videoya doğru SRT şart. İngilizce dublaj düşük öncelik.

## Çalışma düzeni (kullanıcının kararları)
- **Başkan:** ana oturum yönetmendir. Kararları kendisi verir, kullanıcıya her adımda sormaz. Reddettiği öneriyi gerekçesiyle yazar.
- **Kurul ve puanlama yok (19 Kasım).**
- **Alt ajanlar başkanın takdirinde (23 Kasım):** işi hızlandırmak ya da derinleştirmek için gerektiğinde açılır. "Var" ya da "yok" diye bir kural yok; ihtiyaç ölçüdür.
  - Açılırsa:
    - her işin tek sahibi olur ve aynı ajan `SendMessage` ile sürdürülür;
    - ortak dosyaları (motor, `film.js`, plan listesi) yalnız ana oturum değiştirir;
    - ajanın bulgusu iddiadır, başkan doğrular.
  - Eski kurul düzeni: `kanal/KURUL_YONTEMI.md` (arşiv).
- **Fable:** isteğe bağlı danışman. Dorian, Mary Stuart ve Lale'de engelleyici bulgu yakaladı. Her bulgu iddiadır, karede ve kaynakta doğrulanır.
  - Lale'den gelen öneri (karar değil): iki kapı.
    - Seslendirmeden önce senaryo okuması (puansız bulgu listesi).
    - Render'dan sonra izleyici gözüyle okuma: üç izleyici kişiliği zamanlı izleme günlüğü yazar. Tek kişinin düşüşü zevktir, üçünün ortak düşüşü bulgudur.
    - Düzen: `lale-cilginligi/fable_son_okuma/`.
- **Deney (23 Kasım):** Lale Çılgınlığı ayrıntılı promptla, Gılgamış yalnız yönle üretiliyor (`analiz/2026-11-23-deney-yon-promptu.md`).
- **Git:**
  - Her video kendi dalında üretilir; video bitince dal `main`'e birleştirilir.
  - Her iş parçasından sonra commit ve push. Commit mesajı Türkçe, sonunda oturumun atıf satırları.
  - PR yalnız kullanıcı isterse açılır.
  - `navitas-topkapi` deposuna ve kökteki eski Navitas dosyalarına dokunulmaz.

## İş akışı
1. **Konu ve talep kontrolü** (`uretim_plani.md`, senaryodan önce):
   - (a) Türk izleyici bu adı tanıyor mu? `python3 araclar/talep/talep.py "sorgu" …` (otomatik tamamlama + ilk 10 izlenme). Kontrol satırı olarak kanalın eski konuları da aranır.
   - Türkçede boşluk, dünyada yankı: `araclar/talep/iki_dil.py "tr|en"`.
   - (b) Başlık ve kapak izleyiciye kendi hayatından bir soru soruyor mu?
   - Kontrol zayıfsa açı kullanıcıya önerilir; konuyu değiştirmek kullanıcının kararıdır.
   - Konu taramaları: `analiz/2026-11-1*-konu-adaylari*.md`, `2026-11-2*-turkce-*.md`, `2026-11-23-bosluk-2-ve-gilgamis.md`.
2. **Kullanıcının fikri sorulur (kullanıcının kararı, 22 Kasım):** konu seçildikten sonra, iskeletten önce kısa ve seçenekli sorular sorulur.
   - Amaç herkesin yaptığı anlatım değil, farklı bir bakış; ama sıkıcı olmamalı.
   - Öne alınacak üç bakış: kaybedenin ya da sıradan birinin gözünden; bir nesnenin yolculuğu; bildiğimiz hikâyeyi arşivle bozmak.
   - Konu taramasında adaylar bu üç bakışla da tartılır.
3. **Paketleme taslağı ve iskelet** (senaryodan önce, `uretim_plani.md`):
   - **En az 10 başlık adayı.** Her biri şu sorularla elenir:
     - izleyiciye kendi hayatından soru soruyor mu?
     - tek nefeste okunuyor mu?
     - cevabı yarı tahmin ettiriyor ama ele vermiyor mu?
     - tanıdık kapı (izleyicinin aradığı kelime) içinde ve önde mi?
     - bağlamsız anlaşılıyor mu?
     - ≤ 45 karakter mi? Mobil 45–50 karakterde keser.
   - Art arda iki videoda aynı kalıp kullanılmaz.
   - **İki kapak taslağı:** aynı fikrin iki yazılışı değil, iki ayrı vaat.
     - Öneri: kapak merak açar, başlık tamamlar. Kapak yazısı başlığın sözcüklerini tekrar etmez.
     - Kapağın vaadi senaryoda en az bir cümleyle karşılanır; senaryo bitince kapakla yeniden karşılaştırılır.
   - **İskelet:** `yonetmenlik` becerisindeki tablodan seçilir (Kahramanın Yolculuğu, Harmon, Kişōtenketsu…). Yazılacaklar:
     - kahraman (her zaman başlıktaki karakter değildir) ve her adımın cümle numarası;
     - merak döngüleri (soru → cevap cümlesi);
     - bir önceki videonun iskeleti.
   - Kanalın imzası: "yolculuk nerede kırıldı?"
4. **Senaryo** (`senaryo.json`; `tts` seslendirme metni, `alt` altyazı):
   - Aşağıdaki "Senaryo ve kurgu kuralları"na uyar.
   - **Tempo kontrolü:** `python3 araclar/analiz/tempo_kontrol.py PROJE/senaryo.json --yazar "…"`. Seslendirmeden sonra `timeline.js` ile tekrarlanır.
     - Araç işaret koyar, karar vermez; her işaretli cümleye başkan "olay" ya da "soyut" der.
     - İşaretler: K köprü, M soyut, E erken soyut, T merak, A yeni ad, Y yazar.
   - **Tempo tahminleri:** 3 sınanabilir tahmin **yayından önce** `analiz/tahminler.md`'ye yazılır, 48. saatte doldurulur.
5. **Kaynak denetimi seslendirmeden önce** (`kaynak/DOGRULAMA.md`): her tarih, sayı ve alıntı kaynağıyla.
   - Kamu malı özgün metin satır numarasıyla depoya alınır.
   - İç dünya uydurulmaz: kişinin kendi mektup, hatırat ve sözlerine dayanır.
   - Telifli kaynaktan yalnız fikir alınır; kısa alıntı künyeyle verilir. Künye açıklamaya yazılır.
   - Kullanıcının hatırladığı sahne de kaynakla sınanır.
6. **Seslendirme:** her bölüm iki çekim; iyi olan seçilir.
   - Whisper varsa `tools/transcribe.py` + `tools/build_vo.py` (`milton/tools`).
   - Whisper yoksa cümle düzeyinde hizalama: `narkissos/tools/hizala_cumle.py`.
   - Tek cümle düzeltmesi tüm seslendirmeyi yenilemeden: `mary-stuart/tools/yama_vo.py`.
   - Kesim gerçek duraklamada yapılır.
7. **Üslup ve motor:** önce kendi motorlarımız (gravür `milton/lib`, vazo `sisifos/lib`/`prometheus`, kâğıt kesme `orfeus`, ağaç baskı `kafka`, mürekkep `ran`, sessiz film `mary-stuart`, karma üslup `dorian-gray`). Uymazsa cinecode tarifleri (`.claude/skills/cinecode/styles/`, önce `BIZIM_NOT.md`), sonra `araclar/lemo/KATALOG.md`.
   - Lemo belgeleri CC BY-NC: okunur, depoya kopyalanmaz. Kodu MIT.
   - Motor yazmak en pahalı aşama; hazır motor işe yarıyorsa yenisi yazılmaz.
   - **Üslup kapısı** tek kare değil: manzara + orta plan figür + yakın plan + 15 sn hareket.
   - Kodla çizimin zayıf yanı yüz, el ve karmaşık beden hareketi. Güçlü yanı siluet, profil, ışık, dönüşüm. Fikir görüntünün kuralı olabilir: Dorian'da yalnız tablo renkliydi, Kafka'da böcek hiç görünmedi.
8. **Animasyon:** Canvas 2D / WebGL2. Her çekim bir cümleye (`S('B04')`) ya da kelimeye (`Wd('B04','kelime')`) bağlanır; ses değişince görüntü kendiliğinden kayar (çekim sistemi `film.js`; en yenisi `lale-cilginligi/lib/film.js`). Görüntü kuralları aşağıda.
9. **Ses:** müzik her videonun tonuna göre o video için yazılır; seri ya da kategori kuralı yok (20 Kasım). Efektler ayrıca üretilir.
   - Miks: konuşmanın altında kısma; -14 LUFS, -1 dBTP.
   - **Her müzik üretiminden sonra saniye saniye düzey eğrisi basılır** (medyan, "−60 dB üstü saniye"). Miks LUFS'u müziğin yokluğunu göstermez: Mary Stuart neredeyse müziksiz teslim edilmişti.
   - Duyulması gerekenler kulakla dinlenecekler listesine yazılır.
   - Zaman çizelgesini kaydıran ses kararları render'dan önce biter.
10. **Render:** 1920×1080, 30 fps, H.264 CRF 18 + AAC, BT.709 renk etiketi ve ses dili etiketi.
   - `render.js` mutlak yolla başlatılır; depo kökünde ilgisiz eski bir `render.js` var.
   - Uzun render'dan önce tek karede çizim, birleştirme ve kodlama süreleri ayrı ölçülür.
11. **Kapak:** 1280×720 JPG (< 2 MB). İki kapak "Test ve karşılaştır" ile denenir. Kurallar aşağıda.
12. **Shorts:** dikey için kurulur (`narkissos/shorts_dikey.html` hattı: filmin planlarını 1080×1920'ye yeniden çizer, her filme taşınabilir) ya da hiç yapılmaz.
    - Kırpılmış yatay film akışta kaydırılıyor (Elizabeth Shorts'unda izlemeye devam eden %27).
    - Ölçüt: izlemeye devam eden ≥ %60.
    - En güçlü cümle ve kare ilk saniyede olur; 25–40 sn.
    - Yayın uzun videodan birkaç gün sonra; Shorts uzun videoya izleyici taşımaz, ayrı içerik sayılır.
13. **Yayın paketi ve teslim:**
    - `yayin.md`: başlık, bölüm zaman damgalı açıklama, künye ve kaynaklar, etiketler, SRT, bitiş ekranı, kapak testi.
    - Bitiş ekranı tarifi son karenin kendisinden yazılır.
    - Üç kopya:
      - YouTube için yüksek kalite (≤ 400 MiB, `SendUserFile` sınırı);
      - telefon için H.265 küçük kopya (`libx265 -crf 26–33 -tag:v hvc1`, BT.709, `-c:a copy`);
      - gerekirse ≤ 50 MB'lık parçalar.
    - Uygulamada 100 MB'ı aşan dosyada indirme düğmesi çıkmayabilir.
    - İnce taramalı gravürde CRF kopyası şişer; 100 MB altı kopya iki geçişli sabit bit hızıyla üretilir (Lale: `-b:v 1150k`, 2 pass).

## Senaryo ve kurgu kuralları (yayın verisiyle doğrulanmış)
Kanıt sayıları `analiz/2026-11-22-genel-karsilastirma.md` dosyasında. Yeni video planlanırken önce o okunur.
- **Açılış:** ilk 5 saniye kapağın vaadini karşılar (ikinci kapağınki de). Merak sorusu ilk cümlede sorulur, cevabı sona saklanır. Kayıp ilk 10–15 saniyede.
- **Kancadan hikâyeye köprü sıfır cümle** (4 video). Kimlik bilgisi (ad, yıl) kancanın içinde tek cümle olabilir.
  - Hikâye en geç ~0:45'te başlar.
  - Yapım ve bağlam bilgisi kancanın arkasına değil, ilgili sahnenin yanına konur (Ran'ın yapım bölümü orada "Önemli an" oldu).
- **Somut olay tutar, soyut açıklama düşürür** (3 video, 8 nokta).
  - Bilgi bir olay, nesne ya da sahne olarak verilir. Karşılaştırma ya da çıkarım olaydan sonra tek cümle olur; art arda iki soyut cümle olmaz.
  - En pahalı kayıp ilk iki dakikadaki soyutluk (Mary Stuart 1:12–1:36).
  - Yazarın somut bir olay hakkındaki yargısı tutar; olaydan kopuk açıklama kaybettirir.
- **Merak sorusunun cevabı bir olaydır, kavram değil** (Ran, Mary Stuart). Merak sorusu izleyicinin göreceği somut bir şeyi vaat eder.
- **Doruğu taşıyacak kişiler ilk perdede** adıyla ve görüntüsüyle ekilir; ikinci yarıda yeni ad ve geçmiş kaybettirir (Ran, Medici).
- **Hikâye bitince izleyici gider** (3 video).
  - İksir, abone çağrısı ve bitiş ekranına yönlendirme hikâyenin son anının içinde verilir.
  - İfşadan sonra yorum kısa tutulur.
  - Anlatım "… ekranda" diyorsa o kelime bitiş ekranının (son 20 sn) içinde olur.
- **Uzunluk tutmayı bozmaz** (10 video). Her bölüm kendi küçük merak sorusuyla açılır; YouTube bölüm damgaları konur.
- **Sadelik:** her bölümün tek kahramanı, tek karşıtı, tek mekânı olur ("isimlerden beynim allak bullak", Medici).
- **Kahramanın Yolculuğu** kalıp değil, kontrol listesidir; uymayan aşama zorlanmaz (tablo: `kanal/arsiv/depo_akis_2026-11-23.md`).

## Görüntü ve kurgu kuralları
- **Donuk plan yok:** her plan ilk saniyeden hareket eder (varsayılan yavaş yaklaşma + sözcüğe bağlı eylem). Kesmesiz ya da eylemsiz geçen en uzun süre ölçülür; 5 sn'yi aşan aralıklar listelenir.
- **Plan listesinde her plana ölçek yazılır** (geniş / orta / yakın / ayrıntı / ters açı); ardışık iki plan aynı ölçekte olmaz.
- **Yazı levhası:** plan başına ≤ 8 sn ve toplamda filmin beşte birini geçmez. Boş kâğıt ≤ 2 sn.
- **Geçiş:** aynı mekânda kesme. Yumuşak geçiş yalnız mekân ya da zaman sıçramasında, kısa ve sessizlikte. İki levha saydamlıkla karıştırılmaz (gri üretir).
- **Palet ya da geçiş değişimi** sözcüğe bağlanır ve plan içinde olur.
- **Ana figür koyu siluettir;** iç çizgisiz açık figür "kâğıt kesme" okunur.
  - Gövde kutu olmaz.
  - Kollar ayrı yolla çizilir.
  - Yakın planda baş kadrajın içinde kalır.
- **Karikatür okuması:** koyu siluet + bembeyaz göz + kıvırcık yuvarlak baş + çıkık ağız birleşimi kullanılmaz. Göz küçük ve sıcak tonda olur.
- **Yürüyen, koşan ya da bir şey taşıyan figür** `araclar/hareket/` ile çizilir (ayak kaymaz; `serit.js` kanıt şeridi).
- **Ekran yazısı ve künye alt banda (y > 880) konmaz;** orası altyazının yeri.
  - Kod taramasıyla değil ölçümle denetlenir: `lale-cilginligi/tools/alt_bant.js` her planda çizilen bütün yazıların y'sini ölçer.
- **Kurguya bakış:** render'dan önce bütün film her plandan bir kareyle yan yana görülür (`milton/tools/kurgu_ozet.py`, `ran/tools/ozet.js`).
  - Öneri: yazısız karelerle "sessiz okuma testi". Plan listesini görmemiş biri her karede ne olduğunu yazar.

## Hassasiyet ve hukuk (estetik oyla geçilmez)
- **Yanlış bilgi, telif ve 5816 bulguları düzeltilmeden iş bitmez.** Hassasiyet taraması sona bırakılmaz; üslup karesinde başlar ve görüntüye de bakar.
- **Görüntüde yakalananlar** (Milton → Dorian). Taramada bunlara bakılır, tam boy karede:
  - sıra hâlinde eğilen figürler (namaz safı); baştan ayağa siyah örtülü kadın;
  - dört kollu yıldız (haç); göğsünde alev tutan önden simetrik figür (Kutsal Kalp);
  - siluetin karnındaki küçük figür (hamilelik);
  - havaya kalkmış düz kol (selam); simetrik açık kanatlı kuş (amblem kartalı);
  - siyah giysideki küçük beyaz dikdörtgen (papaz yakası); kan gibi okunan kırmızı leke;
  - gerçek görselin köşesindeki küçük ek resim (Mary Stuart'ta idam sahnesi);
  - koyu kaftan önünde açık dikey şerit + yatay kuşak (haç);
  - koyu kalabalıkta beyaz sivri börk (kukuleta); kemer ortasında asılı kandil (mihrap);
  - başın yanında açık bohça (hale); belde çizgili oval (kalkan); alna giden el (selam);
  - yuvarlak nesnede halka tarama (hedef tahtası). Yeni sette yuvarlak nesneye halka tarama verilmez.
  - (Çernobil) sıra hâlinde dik, yuvarlak tepeli nesneler (çuval, güğüm: mezar taşı); dikenli tel + baraka + çantalı figür (toplama kampı); ters L direk ve sarkan ince çizgi (vinç: darağacı); kırmızı dolu dairede eş merkezli halka (hedef, bayrak).
- **Düzeltme yeni simge üretebilir:** düzeltilen her plan tam boy karede yeniden bakılır (Lale).
- **Dinî karşılaştırma yapılmaz;** eser kendi edebî bağlamında okunur (Milton kararı). Tanrı figürle çizilmez, ışıkla gösterilir.
- **Kapak yazısı da taranır.** Türkçe kelime tuzaklarına dikkat: "dönme" argo okunur, "ŞEYTAN AĞLADI" vaaz gibi okunur.
- **Atatürk:** 5816 ve saygı kuralları; ona söz ya da düşünce uydurulmaz. **Türk bayrağı** 2893'e göre çizilir: `cumhuriyet/lib/act6.js` → `a6_flagImg`.
- **Film videoları:** film görüntüsü yok, oyuncuya benzeyen gerçekçi çizim yok, telifli karakter tasarımı kopyası yok, filmden diyalog yok. Fikir kendi animasyonumuzla anlatılır.
- **Gerçek görseller** yalnız CC0 ya da kamu malı.
  - Kayıt yerleri: `araclar/ASSETS.md`, proje kaynak kaydı ve açıklamadaki künye.
  - Dışarıdan eklenen her varlıkta `lisans-kontrol` becerisi kullanılır.
  - Kaynaklar: Met Open Access API (`isPublicDomain`). Commons'ta oran sınırı var.
- **Türkçe çeviriler çoğunlukla telifli:** dizeler kamu malı özgün metinden ya da kamu malı çeviriden kendi Türkçemizle verilir.

## Kapak kuralları
Ayrıntı ve kompozisyon menüsü: `kanal/KAPAK_DERSLERI.md`.
- **Odak:** tek odak, karenin en parlak noktası orası. İkinci bir beyaz leke odağı böler.
- **Figür:** en iyi sonuç filmin ilk karesiyle aynı figür + tek vurgu rengi.
  - Küçük boyda profil okunmaz, ¾ yüz kullanılır. Tanınan bir yüz yoksa tanınan bir dönem nesnesi kullanılır (Mary Stuart'ta madalya).
- **Yazı:**
  - Bebas Neue; büyük harf yüksekliği karenin ≥ %18'i (1080 ölçeğinde font ≥ 290 px). Figürlere ≥ 30 px boşluk.
  - Sağ alt köşe süre rozetine ayrılır (önerilen listesinde x 1440–1874, y 829–1034).
  - Deneme önerisi: 4–6 kelimelik iki satırlık yazı.
- **Test seti:**
  - tam boy; 246×138, 168×94, 120×68 küçültmeler;
  - odak ısı haritası (`araclar/kapak/odak.py`); gri değer;
  - koyu ve açık mobil akış taklidi; TV boyu; süre rozeti bölgesi.
- **"Test ve karşılaştır":** kazananı izlenme süresi payına göre seçer. Test sürerken başlık değiştirilmez.

## Ölçüt çizgisi
- **Karşılaştırma:** yeni video tek bir videoyla değil, kanal medyanlarıyla ve aynı yaştaki veriyle karşılaştırılır (`analiz/2026-11-17-kanal-ortalamasi.md`).
  - Medyanlar: TO %1,8, ortalama izlenme %39,8, 0:10'da ≈ %77, 0:30'da %61.
  - İlk 48 saatin 0:30 değeri sadık kitleden şişer.
- **Göz atma testi** 2. gün gelir ya da hiç gelmez; 48. saat karar noktasıdır.
  - Düşük TO'da 2–3 gün yeni dalga gelmezse paketleme yenilenir; yayından sonra kapak ve başlık düzeltmek ölü videoyu diriltebilir (Cumhuriyet).
  - TO iyi ama gösterim yoksa sorun paketleme değil gösterim havuzudur.
- **Hesaplar:** gösterim başına izlenme süresi = TO × ortalama izleme. Görüntüleme/gösterim TO değildir. Abone sayısı Studio gelişmiş moddan alınır.
- **Okuma araçları:** elde tutma eğrisi Studio ekran görüntüsünden `araclar/analiz/elde_tutma.py` ile okunur. Eğri ~100–400 izleyicilik; ±3 puanın altındaki fark yok sayılır.
- **Durum (22 Kasım):** kanalda geniş kitleye açılan tek video Sisifos oldu ve havuzu sönüyor.
  - Talep kontrolü TO'yu medyanın üstüne taşıyor (Kafka, Ran, Mary Stuart), ama dalga için yetmiyor; büyüme yeni bir kapıya bağlı.
  - Video video kayıt: `kanal/OLCUTLER_GECMIS.md` ve `analiz/`.

## Teknik notlar ve tuzaklar
- **Playwright:** `require('playwright')` her yerden çalışır. `NODE_PATH` ayarlanmaz (bozuyor), `playwright install` çalıştırılmaz.
- **Süreçler:** PID ile durdurulur, `pkill -f` kullanılmaz. Uzun render ve miks arka planda, uzun `timeout` ile.
  - İki iş aynı çekirdekleri paylaşırken öncelikli olan için ötekine `kill -STOP` / `-CONT`.
- **Render önbelleği:** `.parts*/` kod ve ayar özetini (`KEY`) saklar; şüphede klasör elle silinir.
  - Ara parçalar iş bitince silinir; disk payı sınırlı.
  - Büyük mp4'ler depoya girmez.
- **file:// görselleri WebGL tuvalini kirletir:** render ve kare araçları yerel http sunucusuyla çalışır (`dorian-gray/tools/sunucu.js`).
- **Yazılımsal WebGL (SwiftShader):** önce ölç, sonra hızlandır.
  - Konuma bağlı gürültü dokuya önceden yazılır.
  - Canvas `filter: blur` pahalıdır; düşük çözünürlüklü tuvale çizilip büyütülür.
  - Sessiz film 15 kare/sn.
- **Belirlenimcilik:** `Math.random` yerine tohumlu gürültü; işçiler arası aynı kare.
- **Sözdizimi denetimi:** `node -e "new Function(require('fs').readFileSync('dosya.js','utf8'))"`. Render işçileri sayfayı başta yükler; ortadaki değişiklik yalnız sonraki render'a geçer (gerekirse `ONLY=` ile parça).
- **Piyano sentezi:** MIDI < ~37'de sönüm katsayısı negatife düşüyordu; düzeltme `dec = max(.3, …)` (`dorian-gray/audio/score.py`).
- **milton motoru:** iç içe `GR.frame` göreli değil, mutlak koordinata döner.
- **Yeni videoda `film.js` Lale'den alınır.** Milton ve Dorian'ın `txt()`'si sola hizalı künyenin panelini kaydırıyordu; düzeltme `softBand`.
- **Karma üslupta renk katmanı örtüyle basılır.** Çarpma boyası katman sırası bilmez; önünden geçen figürü de boyar (`lale-cilginligi/lib/lale.js` örtü maskesi).
- **Kapta paket eksikse:** Whisper ve scipy olmadan çalışan yollar `ikaros/tools/hizala.py`, `ikaros/audio/dsp_shim.py`, `ikaros/tools/mix_ffmpeg.py`.
- **Fontlar:** `sisifos/fonts.css`, `orfeus/fonts.css` (Türkçe karakterli woff2 depoda).
- **Dosya boyu:** ağaç baskı gibi karede değişen gürültü dosyayı şişirir; gürültü iki karede bir değiştirilir.

## Depo dizini
| Yer | Ne |
|---|---|
| `lale-cilginligi/` | Lale Çılgınlığı (gravür + yalnız laleler el boyaması; Türkçe boşluk ölçütüyle seçilen ilk video; Fable'ın izleyici okuması; en yeni `film.js`) |
| `dorian-gray/` | *Dorian Gray'in Portresi* (karma üslup: gravür + yalnız portre yağlıboya; en yeni tam hat: film, müzik, kapak, render) |
| `narkissos/` | Narkissos → narsisizm (vazo; cümle düzeyinde hizalama; **ilk dikey Shorts hattı**) |
| `mary-stuart/` | Mary Stuart ve I. Elizabeth (sessiz film; seslendirme yaması `tools/yama_vo.py`) |
| `ran/` | Kurosawa, *Ran* (mürekkep; ilk film videosu; gerçek görsel araları) |
| `kafka/` | *Dönüşüm* (ağaç baskı) |
| `ikaros/` | İkaros (serigrafi afiş; kurulumsuz ses ve hizalama araçları) |
| `milton/` | *Kayıp Cennet* (gravür motoru, `lib/film.js` çekim sistemi, `tools/`, `lib/acts/KILAVUZ.md`) |
| `prometheus/`, `sisifos/`, `orfeus/` | vazo ve kâğıt kesme motorları; `sisifos/README.md` komutlar, `sisifos/yayin.md` |
| `cumhuriyet/`, `29-ekim/`, `cumhuriyet_kapak/` | 29 Ekim videosu (bayrak çizimi, donma denetimi `tools/donma.py`) |
| `gunluk-shorts/` | Şarlken, Medici (Python motoru); dersler `DERSLER.md` |
| `analiz/` | Studio analizleri, konu taramaları, `tahminler.md`, **`2026-11-22-genel-karsilastirma.md`**, `2026-11-17-kanal-ortalamasi.md` |
| `araclar/` | `talep/` (talep ve iki dil), `analiz/` (tempo, elde tutma), `hareket/`, `kapak/odak.py`, `lemo/KATALOG.md`, `ASSETS.md`, `ADAYLAR.md` |
| `kanal/` | bu dosyadan taşınan ayrıntı: `DERSLER.md` (video video dersler), `OLCUTLER_GECMIS.md`, `KANAL_YONU.md`, `KAPAK_DERSLERI.md`, `KURUL_YONTEMI.md` (arşiv), `arsiv/` (ayrıntılı eski depo tablosu ve iş akışı) |
| `.claude/skills/` | `yonetmenlik`, `cizim`, `karakter`, `ses`, `render`, `lisans-kontrol`; `cinecode` (yalnız `/cinecode` ile çalışır; kanal videolarında başvuru kütüphanesi) |
| kök dizin | eski Navitas kahve Story'si; kanalla ilgisiz |

## Bekleyen öneriler (kullanıcıdan)
- Psikolojik anlatım (Zweig, Dostoyevski): tek bir karar anı ve onu yaşayanın iç dünyası, kendi sözlerinden.
- Kendi sesini klonlamak (ertelendi): önce hızlı klon ve Emrullah'la kör karşılaştırma; ses değişimi yeni bir videoyla yapılır.
- Animasyon hiç durmasın.
- Prometheus'tan köprüler: *Frankenstein* ("Modern Prometheus"), *Oppenheimer* (*American Prometheus*).
