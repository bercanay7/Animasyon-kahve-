# KA2 · TUR 2 (1. aşama: anlatım, kaynak, paket metni) — Medici Parça 1
Mercek: kaynak denetçisi, yöntem dürüstlüğü, hassasiyet ve hukuk (veto). Ekran damgaları ve metinleri v2 render çıkınca ayrıca bakılacak (2. aşama).

## 1. Karar ve puan

**Şimdilik RED, 8,0/10** (eşik ≥9; ekran kısmı henüz puanlanmadı).
Tur 1'deki anlatım bulgularımın hepsi (E1, Ö1, Ö2, Ö7, K1) doğru yamalanmış. Kendi Whisper dökümüm de bunu doğruluyor. Teyit kapısı gerçekten kurulmuş: Gutenberg, Wikisource, Treccani ve archive.org açılmış, ve bu turda ben de açtım. Paket büyük ölçüde dürüstleşmiş.

Eşiğin altında kalmamın iki nedeni var:
- **(Y1) Yeni ve engelleyici bir olgu hatası:** c2s10'da "De Roover'a göre Roma şubesine ayrı sermaye verilmedi". De Roover'ın tam metni bunun tersini söylüyor: Roma şubesinin 1402'de 4.000, 1420'de 6.000 florin sermayesi vardı. Hatanın kaynağı da belli: araştırma notu de Roover'ın **Averardo de' Medici'nin ayrı Roma bankası** için yazdığı cümleyi Giovanni'nin bankasına bağlamış.
- **Paket metninde ücretsiz düzeltilecek üç satır:** E2'nin kalanı.

Y1 en azından ekranda, kalan paket satırları ve ses lisansı kaydı (Y7) düzelirse alan puanım 9,0 olur. Y1 ve Y2 aynı partide sesle yamalanırsa 9,5 olur.

## 2. Neye dayandım (sınırlarım)

- **Videoyu oynatamadım, sesi dinleyemedim.** `out_p1/medici_P1.mp4` hâlâ v1 (09:54 tarihli); v2 render yok. Ekran yargısı 2. aşamaya kaldı. Ekran metinleri için şimdilik yalnız sahne kodunu okudum (`scenes_c0–c2.py`).
- **Okunan proje dosyaları:** `KURUL_BRIFI_P1_TUR2.md`, `KURUL.md`, `teyit_P1.md` (başkan notu dahil), `kaynaklar_P1.md`, `python3 script.py c0/c1/c2` (söylenen metin), `timeline.json` (yeni), `yayin/studio_paketi_P1/01–05`, `medici_P1_tr.srt` (paketteki kopyayla birebir aynı), `KULAK_KONTROL_P1.md`, `ses_ham/yama_p1/rapor.json`, `notlar_c2.md`, `YAYIN_TASLAK.md`, kapaklar K1/K2, KA1 tur 1 raporu (çapraz bakış).
- **Bu turda curl ile kendim okuduğum birincil ve otoriter metinler** (scratch: `…/scratchpad/ka2t2_dl/`):
  - de Roover 1963, archive.org tam metin (`_djvu.txt`);
  - Treccani DBI maddeleri: Giovanni di Bicci (Terenzi 2016), Villani (Zabbia), Cavalcanti;
  - Machiavelli, *History of Florence*, Gutenberg #2464 (III ve IV. kitap);
  - **S. Casciu 2006** (*La Principessa saggia* katalog denemesi, storiadifirenze.org PDF); **M. Verga 2006** (aynı katalog); **R. Menicucci** (storiadifirenze.org);
  - Italia Nostra 2017 bildirisi; Museo de' Medici "Patto di Famiglia" sayfası;
  - it.wikipedia "Anna Maria Luisa de' Medici", en.wikipedia "Palla Strozzi";
  - S. Tognetti, "Gli affari di messer Palla Strozzi" (Firenze University Press, özet); Eckstein 2006 Crossref özeti; NovelInvestor'un *Medici Money* notları;
  - **YouTube Yardım "Disclosing use of GenAI content"** (support.google.com/youtube/answer/14328491, 4 Kasım 2026'da okundu).
- **Sesle ilgili tek kanıtım bağımsız ASR:** yerel Whisper medium (sherpa-onnx) ile 12 yamalı klibin hepsini döktüm.

## 3. Tur 1 maddelerimin durumu

| Madde | Durum | Kanıt |
|---|---|---|
| **E1** "Tracy Parks" → Tim Parks | **KAPANDI** (anlatım, SRT, paket, belgeler); ekran v2'de doğrulanacak | Senaryo c2s7 "Tim Parks'ın aktardığına göre…"; ASR (yama klibi): "Tim Parks'ın aktardığına göre, mevduata gelince…"; SRT 6:19; sahne kodu `P.plate("TİM PARKS")`. Artıklar: `notlar_c2.md` eski ekran tablosu ve `YAYIN_TASLAK.md` ortak blokta hâlâ "Tracy" (bkz. Y6, Y9) |
| **E2** Paket videodan fazlasını iddia ediyor | **KISMEN** | Etiket vaadi, ilk paragraf ("Toskana'yı yönetmiş Medici hattının son üyesi", "31 Ekim 1737'de imzalanan … 3. maddesine göre"), yapay ses satırı ve okunan birincil kaynaklar düzeldi. Kalan üç satır engelleyici ama ücretsiz (bkz. Y3) |
| **E3** Teyit kapısı kaydı | **KAPANDI** | `teyit_P1.md` (71 satır, özgün dilde alıntı, karar), başkan notu, `kaynaklar_P1.md` özeti (46 ● · 18 ◐ · 5 ○ · 2 ANEKDOT). Bu turda açık kalan c0s4, c0s8, c0s11 ve c0s12–13 için otoriter kaynak buldum (Y4); c2s10 kaydı ise yanlış (Y1) |
| **Ö1** "Salvestro çekildi" | **KAPANDI** | ASR c1s18: "…Michele Di Lando gonfaloniere oldu." ("çekildi" yok). Machiavelli III (Gutenberg #2464): "Salvestro Alammano de' Medici was therefore drawn Gonfalonier"; Temmuz'da "Luigi Guicciardini, Gonfalonier of Justice". c1s16 "kurayla" ✓; "Mayıs" iki aylık Signoria'dan türetme ("in the next Signory", Nisan bağlamı), kabul |
| **Ö2** Veba "Temmuz'a kadar" | **KAPANDI** | ASR c1s11: "Veba 1348 Mart'ında geldi ve yaz boyunca şehri bırakmadı." Stefani "finì di Settembre", Boccaccio "marzo … luglio": ikisiyle de uyumlu |
| **Ö3** Ekranda 152.820 | **KAPANDI** (kodda); v2'de bakılacak | `amt=("150.000+ fl.",)`; de Roover Tablo 8 toplamı **151.820** (KAY). Anlatım "yüz elli bini aşkın" ✓ |
| **Ö4** "1407 VENEDİK" | **KAPANDI** (kodda); v2'de bakılacak | `events=[(1340,"CENOVA"…),(1494,"PACIOLI"…)]`. Pacioli 1494 genel bilgi, ◐ kabul |
| **Ö5** 3. madde kartı alıntı gibi | **KAPANDI** (kodda); v2'de bakılacak | "3. MADDE · ÖZET", "SINIR YAKLAŞIKTIR" (`scenes_c0.py:104–111`) |
| **Ö6** Studio "Yapay içerik" = Evet | **DEĞİŞTİRİLDİ** (başkan: "Hayır" + açıklamada YZ sesi satırı). **Muhalefet şerhim sürüyor**, engellemiyorum | Resmî metin (YouTube Yardım, 4 Kasım 2026):<br>• "Realistic AI content and meaningful changes require disclosure"<br>• Bildirim gerekmeyenler listesinde yalnız "**Cloning one's own voice** to create voice overs or dubs" var; "Emrullah" ise başka bir gerçek kişinin (Emrullah Uzun) kütüphane klonu<br>• "Labels may appear **in the expanded description** for non-music AI-generated audio or AI content that is non-photorealistic or animated"<br>• "**Disclosing AI content alone won't limit a video's audience or impact its eligibility to earn money**"<br>• "Creators who consistently choose not to disclose … may be subject to … penalties"<br>Sonuç: "Evet" kanala neredeyse hiçbir şeye mal olmuyor (etiket yalnız açılan açıklamada), "Hayır" ise yoruma dayalı bir risk taşıyor. Karar kullanıcının; ben "Evet" öneriyorum. |
| **Ö6b** Ses lisansı kaydı | **AÇIK** | `SURUM_KUNYESI_P1.md` ve `yayin_gunlugu.jsonl` yok (KURUL E'de planlı). Bkz. Y7 |
| **Ö7** "büyük torunu" | **KAPANDI** | ASR c2s27: "…torununun oğlu Lorenzo'nun kaydına göre…"; DBI "secondo il bisnipote Lorenzo il Magnifico … circa 180.000 fiorini" |
| **Ö8** Machiavelli parafrazı | **KAPANDI** | Gutenberg #2464, IV. kitap: "…thus you will escape both danger and envy; for it is not what is given to any individual, but **what he has determined to possess**, that occasions odium." "İstediğinden" İngilizce çeviriye sadık. İtalyancadaki "si toglie" (kendi aldığı) nüansı ◐ düzeyinde kabul; ekranda "MACHIAVELLİ'YE GÖRE" ve "ANEKDOT" var |
| **K1** c1s24 "Medici adı…" | **KAPANDI** (yamalı). Düzeltme notu: tur 1 gerekçem kısmen yanlıştı | DBI Terenzi: "**Anche i nuclei più importanti** della casata Medici si collocavano, nel Trecento, al di sotto dell'élite cittadina". Eski cümle de savunulabilirdi; yeni ve daraltılmış "Medici'nin bu kolu" daha güvenli ve doğru |
| **K2** c1s6 "kenti de saydı" | **KABUL** | Anlatım aynı kaldı; ekranda "VILLANI'YE GÖRE · TAHMİN" (kodda) yeterli. Villani: "Istimavasi … per l'aviso del pane" |
| **K3** Karşı-papa nüansı | **KAPANDI** (kodda) | "COSSA = XXIII. JOHANNES · PİSA PAPASI · BUGÜN KARŞI PAPA SAYILIR" |
| **K4** Etiketler | **KAPANDI** | Lorenzo, Cosimo ve Uffizi çıktı; eklenenlerin hepsi videoda geçiyor |
| **K5** Kapak C "ÇİFTE DEFTER" | **KAPANDI** | Yeni kapaklar K1 "SON MEDİCİ / MİRASI KİLİTLEDİ", K2 "FAİZ YASAKTI". K2'deki kesede zambaksız palle var, dönemle uyumlu |
| **K6** 1465 sonrası arma | **KAPANDI** (motor dönem katmanı); v2'de bakılacak | `donem.py`, `qa_donem` |
| **K7** Ölüm sahnesinde alacakaranlık | **KABUL** (dokunulmadı, önerim de buydu) | it.wiki (H. Mann): ölüm "durante un breve fortunale … poi … sole splendente". Saat yine yok, görsel saat iddiası taşımıyor |
| **K8** "Vicdan komitesi" | **KABUL** | Açıkça YORUM ve mizah |
| **K9** Ekran olguları kaynak kapısına | **KISMEN** | `notlar_c2.md` "güncel durum" bölümü ekran-yalnız olguları sayıyor (9.780, %29,8, 162.925) ama `kaynaklar_P1.md`'de "ekran olguları" bölümü yok. `notlar_c2.md`'nin eski tablosu bayat: TRACY, 1407, 152.820, TRECCANI-ANEKDOT. Bkz. Y9 |

## 4. Yeni sorunlar (şimdiki aşama)

### ENGELLEYİCİ

**Y1. c2s10, 6:37,2–6:43,8: "De Roover'a göre Roma şubesine ayrı sermaye verilmedi; kasayı Kilise'nin yatırdığı para doldurdu." Bu, anlatıldığı dönem için yanlış ve de Roover'a yanlış atfedilmiş.**

Bağlam: cümle 1397–1402 dizisinin içinde (c2s11 "25 Mart 1402"). c2'nin `YIL_AT`'ı c2s11'de başladığı için bu cümle boyunca HUD **1397** gösteriyor (`scenes_c2.py:324`).

De Roover'ın tam metni (archive.org):
- 1402: "aggregate capital invested in banking … probably amounted to 20,000 florins: 8,000 florins in Florence and also in Venice and **only 4,000 florins in Rome**."
- 1420: "This capital was then allocated … **6,000 florins to the branch at the Roman Curia**."
- Sonrası: "In the new contract with Salutati, dated March 10, **1429, no corpo** was assigned to the Roman branch … the capital had already been **withdrawn in 1426**."

Yani "sermayesiz Roma" Giovanni'nin son üç yılının (1426–29) gerçeği; kuruluşun değil.

**Hatanın izi:** `arastirma/M1` D19'daki tırnak "…no corpo (capital) was assigned to the Rome branch" ve gerekçe "Kilise para yatırıyor, borç almıyor" de Roover'ın şu cümlesinden geliyor: "Strange as it may be, no corpo (capital) was assigned to the Rome branch; perhaps this was deemed unnecessary, since the papal court was seeking to invest rather than to borrow". Bu cümle **Averardo de' Medici'nin** ayrı Roma şubesi ("Andrea de' Bardi & Co.", 1422'den "Boscoli & Company") için yazılmış. KAY dönem sorununu fark etmiş ama "opsiyonel" saymış; 1402 ve 1420 rakamları ◐ "nitelikli kalsın" kararına girmemiş.

**Yapılmalı (tercih edilen: ses yaması). Tam yedek cümle:**
> "De Roover'a göre Roma şubesi zamanla sermayesiz çalışır hale geldi; kasayı Kilise'nin yatırdığı para dolduruyordu."

Neden yamaya değer: tek cümle (~95 karakter) ve v2 render henüz çıkmadı, şimdi yamalamak render sonrasından ucuz. Yayının ana kaynağı olarak tanıtılan bir akademisyene, onun yazdığının tersini atfetmek, sabit yorumdaki "tam kaynak ve teyit tablosu" davetiyle birlikte en kolay yakalanacak hata.

**Asgari ücretsiz yol** (yama yapılmazsa veto ancak böyle kalkar): "AYRI SERMAYE ✗" kartının yanına "1426'DAN SONRA" etiketi; `teyit_P1.md` ve `kaynaklar_P1.md`'de c2s10 dayanağı "dR: 1426'da çekildi, 1429'dan itibaren yok; 1402'de 4.000, 1420'de 6.000 fl" diye düzeltilsin ve M1:D19 hatası not edilsin.

**Y3. Paket metninde kalan üç satır (E2'nin kalanı; ücretsiz, ~5 dakika).**

(a) `02_aciklama.txt` "KAYNAKLAR (bu parçada **gerçekten okunanlar**)" altında "Tim Parks, Medici Money (2005): anlatımda anılan aktarım" duruyor. Kitap okunmadı; `teyit_P1.md` §5 "Açıklamaya yazılmaması gerekenler: Tim Parks (okunmadı)" diyor. Atfın tek dayanağı kitabın okur notları (NovelInvestor: "The deposit is discretionary … interest (gift) is at the discretion of the banker … not contractual"); içerik de Roover'da ●. Önerilen satır, başlığın dışına:
> "Anlatımda anılan ama okunmayan: Tim Parks, Medici Money (2005) — aktarım kitabın özet notlarına dayanır; aynı bilgi de Roover'da doğrulandı."

Aynı listede dayanılan ama yazılmayan Wikipedia sayfaları da var: it.wikipedia "Anna Maria Luisa de' Medici" (3. maddenin İtalyanca alıntısı) ve en.wikipedia "Tomb of Antipope John XXIII" (Martinus'un itirazı). Ya eklensin ya da Y4'teki Casciu/Verga kaynaklarıyla değiştirilsin.

(b) `03_sabit_yorum.txt`: "Rakamlar ve tarihler açıklamadaki kaynaklara dayanır" fazla geniş. "137 hane / %30" (c2s23) Eckstein 2006'dan özetle alındı ve okunmadı; ekrandaki 162.925 en.wikipedia → Baldwin 2007'den, 9.780 hane araştırma özetinden. Önerilen yeni metin:
> "Rakam ve tarihlerin çoğu açıklamadaki kaynaklara dayanır; '137 hane / yüzde 30' hesabını kaynağından okuyamadık, videoda 'bir hesaba göre' diye nitelendi."

(c) `02_aciklama.txt`: "Kaynaklar çeliştiğinde videoda bunu açıkça söylüyoruz." mutlak bir iddia. Video bazı çelişkileri sessizce seçiyor: 21/22 Temmuz (Machiavelli/DBI), Via Calimala / via dell'Arte della Lana (it.wiki/de Roover). Önerilen yeni metin:
> "Önemli çelişkilerde (Cossa'nın kurtarılması, Giovanni'nin son sözleri) bunu videoda açıkça söylüyoruz."

### ÖNEMLİ

**Y2. c2s30, 9:11,1: "Cavalcanti ise 1440'larda, olaya daha yakın bir kalemle…" (ekranda "CAVALCANTI · 1440'LARDA").**

DBI "Cavalcanti, Giovanni": Stinche'de yaklaşık on yıl, '30'ların sonuna kadar hapis kaldı. "In prigione egli attese alla stesura delle Istorie fiorentine, narrando avvenimenti compresi tra il 1420 e il 1440; l'interruzione delle Istorie corrisponde grosso modo all'uscita dal carcere". 1441–47'yi anlatan *Seconde istorie* ise Giovanni'nin ölümünü içermiyor. "Olaya daha yakın" vurgusu doğru, on yıl ise yanlış.

**Tam yedek cümle (Y1 ile aynı partide):**
> "Cavalcanti ise 1430'larda, hapisteyken, olaya daha yakın bir kalemle başka bir şey yazar: kimse dünyevi tasaları sonsuz huzurla değiş tokuş ettiği için kederlenmemeli."

Neden değer: c2 yaması zaten yapılacaksa marjinal maliyet tek cümle. "Hapisteyken" ayrıntısı Cavalcanti'nin bakışını da açıklıyor. Yama yapılmazsa ekran levhasından on yıl çıkarılsın ("CAVALCANTI · ÇAĞDAŞI · OLAYA DAHA YAKIN"), sabit yoruma bir düzeltme satırı eklensin.

**Y4. Açık kalan c0 "erişilemedi" maddeleri artık otoriter kaynakla kapanabilir. Bu bir düzeltme değil, kayıt yükseltmesi; c0 anlatımı doğru.**
- **c0s8 "on üç madde, Fransızca" ve c0s11 "üçüncü madde":** Casciu 2006, s. 48–49: "Nei suoi **tredici articoli redatti nell'originale in francese e quindi tradotti in italiano e ratificati**…", "(il celebre articolo iii)". Menicucci de "articolo 3" diyor.
- **c0s12–13 (3. madde lafzı ve gerekçesi):** Casciu, maddenin İtalyanca tam metnini veriyor: "…per ornamento dello Stato, e per utilità del Pubblico, e per attirare la curiosità dei Forestieri, non ne sarà nulla trasportato, o levato fuori della Capitale, e dello Stato del Gran Ducato". Anlatımın "İtalyanca çevirisine göre" kipi Casciu ile tam uyumlu.
- **c0s4 "devleti yabancı birliklerin elindeyken":** it.wiki: "nel gennaio del 1737 le truppe spagnole … furono sostituite da 6.000 soldati austriaci". Casciu de Temmuz 1737'de "generale Wachtendonk, comandante delle truppe austriache in Toscana" diyor.
- **Not:** Verga ("Convenzione di Famiglia sottoscritta **a Vienna** il 31 ottobre 1737") ve Casciu ("Alla corte di Vienna agiva con pienezza di poteri, in nome dell'Elettrice, il marchese Ferdinando Bartolommei") sözleşmenin Viyana'da elçilerce imzalandığını söylüyor. Museo de' Medici, Elettrice'nin nüshasının İtalyanca olduğunu yazıyor ("in doppia copia, una in italiano per la Medici e l'altra in francese per il Lorena").
- **Anlatım doğru:** özgünü Fransızca, İtalyancası çeviri. Ama ekranda "ITALIANO" sözcüğünün çizilmesi ve imza masası sahnesi 2. aşamada bu ışıkta bakılacak.
- **Açıklama notu önerisi:** "Aile Sözleşmesi'nin Fransızca özgününü görmedik; 13 madde, Fransızca özgün ve İtalyanca onaylı çeviri bilgisi S. Casciu'ya (2006) dayanır." Kaynak listesine Casciu 2006 ve Verga 2006 eklensin.

**Y6. `YAYIN_TASLAK.md` (P2–P7 şablonu) P1 paketinin gerisinde kalmış.** Ortak "BAŞLICA KAYNAKLAR" bloğunda hâlâ "Tracy Parks, Goldthwaite, Padgett–Ansell, Uffizi/V&A/Met" var. §6 madde 5 "Değiştirilmiş veya sentetik içerik: **Evet**" diyor, başkan kararı ise "Hayır". P2 paketi bu şablondan üretilirse tur 1 E2 hatası geri gelir. Şablon P1 paketine göre güncellensin.

**Y7. Ses lisansı ve Studio kararının kaydı yok** (`SURUM_KUNYESI_P1.md` yok). Kayda girmesi gerekenler:
- ElevenLabs kütüphane sesi "Emrullah" (voice_id `DpEiQMnL9WxMsymCsjPY`, category professional; tanımına göre Emrullah Uzun'un sesi);
- üretim tarihleri ve abonelik planı (ticari kullanım), sesin kütüphane kullanım koşullarının ekran görüntüsü;
- Studio cevabı ve gerekçesi.

Ayrıca Anayasa U3 ("gerçek bir kişinin sesi klonlanmaz") ile §12-17 ("Emrullah Uzun") arasındaki gerilim yazılı olarak çözülsün: istisna "sahibinin ticari lisansla paylaştığı kütüphane sesi; taklit değil, rızalı lisans".

**Y8. Bağımsız ASR iki yama sözcüğünü bayrakladı; kulak kontrolü şart.**
- c2s20: "Covanni'yi **Aforoz'da** tehdit etmek" (metin: "aforozla"). Başkanın ASR'si de aynı yeri işaretlemiş.
- c2s1: "Çözüm, **kan bir odaydı**" (metin: "kambiyodaydı").

Diğer 10 yamada döküm metinle anlamca birebir (yalnız ASR yazım farkları var: "Derover", "Kosa"). "Mayıs'ında" bu kez doğru çıktı ("O yılın mayısında"). Sesi duyamıyorum. "Aforozla" gerçekten "aforozda" diye okunuyorsa c2s20'nin belgeli olgusu bozulur ve yeniden üretim gerekir. Kullanıcı `KULAK_KONTROL_P1.md`'deki `yama_c2s20.mp3` ve `yama_c2s1.mp3` kliplerine özellikle bakmalı.

### KÜÇÜK

- **Y5.** `02_aciklama.txt` 2. satır: "**5:39'de**" yanlış ek, doğrusu "5:39'da" (beş otuz dokuz → -da). Aynı satırdaki "son Medici'nin ölümünden" kısaltması arama önizlemesinde görünüyor. Gövde nitelediği için kabul edilebilir; istenirse "Toskana'nın son Medici'sinin ölümünden" yazılabilir.
- **Y9.** `notlar_c2.md` "Ekrandaki olgular" tablosu bayat (TRACY PARKS, VENEDİK 1407, 152.820, TRECCANI-ANEKDOT). Kaynak kaydı ekranla çelişmesin: tablo yeniden üretilsin ya da üstü çizilsin. `kaynaklar_P1.md`'ye "ekran olguları" bölümü (tur 1 K9) hâlâ önerim.
- **Y10.** c1s28 anlatımı "Via Porta Rossa ile Via Calimala'nın kesiştiği köşe" (it.wiki) diyor; ekran levhası teyit gereği yalnız "VIA PORTA ROSSA". De Roover Tavola'yı 1427 ve sonrası için "via di Porta Rossa × via dell'Arte della Lana"ya koyuyor. Anlatım ◐ olarak kabul; tutarsızlık küçük.
- **Hassasiyet:** başlık, kapak K2 ve sabit yorum sorusu "faiz yasağı"nı yalnız Orta Çağ kanon hukuku üzerinden işliyor; videoda bugünün faizsiz bankacılığıyla karşılaştırma yok. Böyle kalsın; yorumlar o tartışmaya kayarsa ılımlı moderasyon yeter. Ciompi'nin ezilmesinde kızıl yıkama kalktı ("loncanın kaldırılması ve dışlanma"), şiddet yok. Telif temiz: yazı tipleri OFL, müzik ve SFX sentez, görüntü kodla çizim, alıntılar kamu malı metinlerden ve çevirileri bize ait.
- **Kapak K1 "SON MEDİCİ":** yaygın bir sıfat (it.wiki'nin bölüm başlığı "Ultima dei Medici"; Museo de' Medici "the last survivor of the grand ducal branch"). Anlatım 0:09'da niteliyor. Kapak için kabul.

### 2. aşama (v2 render) için ön notlar — ekranda bakacaklarım

1. c0s3 levhası "**MEDİCİ'NİN SON ÜYESİ**" (`scenes_c0.py:43`) anlatımın nitelemesini düşürüyor. it.wiki: "Con la sua morte si estinse **il ramo granducale**". Önerim: "MEDİCİ HANEDANININ SON ÜYESİ" ya da "TOSKANA HATTININ SON ÜYESİ".
2. "ITALIANO" sözcüğünün çizilmesi: Casciu'ya göre İtalyanca onaylı bir çeviri var. Önerim "ÖZGÜN: FRANSIZCA · İTALYANCA ÇEVİRİ".
3. İmza ve mühür sahnesi: sözleşme Viyana'da elçilerce imzalandı. Floransa'daki odada imza olarak değil "onay" olarak okunmalı, ya da "VİYANA" künyesi eklenmeli.
4. "162.925 FLORİN · BRÜT" (`scenes_c2.py:228`): tek dayanağı en.wiki → Baldwin 2007 (üçüncül). "BİR HESABA GÖRE" ile nitelensin ya da kaldırılsın. "1427'NİN EN ZENGİNİ" ✓ (Tognetti: "risultava essere il cittadino più ricco").
5. Y1 ve Y2 ekran karşılıkları.
6. Ayrıca doğrulanacaklar: "TİM PARKS", "150.000+", "BELGE · DE ROOVER", "PİSA PAPASI", "3. MADDE · ÖZET", "SINIR YAKLAŞIKTIR", "MART 1348 · YAZ BOYUNCA", "VILLANI'YE GÖRE · TAHMİN", 1438 öncesi madalyalarda "TEMSİLÎ".

## 5. Kullanıcının sorusu (alanım açısından): "Bu çizim tarzı basit, ucuz, yapay zekâ ile üretilmiş gibi mi duruyor?"

Kaynak ve politika merceğinden: görüntü üretken yapay zekâ değil, kod. v1 karelerinde YZ'nin tipik izleri yok (eriyen el ya da yazı, tutarsız mimari, anlamsız harfler); Türkçe metinler kusursuz. Bu, YouTube'un "özgün olmayan / şablondan üretilmiş içerik" politikasına karşı bir güç. "YZ gibi" algısını en çok tetikleyebilecek şey çizim değil: biri gerçekçi sentetik anlatıcı sesi (açıklamada dürüstçe beyan edilmiş), öteki her çekimde tekrar eden "levha + ikon + damga" dili. Damgalar (ANEKDOT, MİT, BELGE, "…GÖRE") kanalın dürüstlük imzası ve değerli; ama süs amaçlı, bilgi taşımayan damgalar azaltılırsa şablon hissi düşer. v2 karelerinde bunu ölçüp somut kare ve zamanla yazacağım.

## 6. En emin olmadığım nokta

1. **Y1'in ağırlığı:** c2s10 tek başına zaman belirtmiyor. De Roover'ın 1426 sonrası için söylediğiyle "genel" olarak doğru okunabilir. Engelleyici dememin gerekçesi HUD'ın 1397 göstermesi, cümlenin 1402'den önce gelmesi ve atfın kaynağının başka bir bankaya ait olması. Başkan HUD'ı ve etiketi düzeltirse ses yaması olmadan da vetoyu kaldırırım.
2. **Ö6 (Studio beyanı):** YouTube metni YZ anlatıcı sesini açıkça "bildirilmeli" listesinde saymıyor. "Hayır" savunulabilir; benim "Evet" önerim maliyetsizliğe ve "yalnız kendi sesini klonlamak muaf" ifadesine dayanıyor.
3. **Y8:** "aforozla" ve "kambiyodaydı" ASR'nin hatası da olabilir. Son söz kulağın.
4. **Sözleşmenin dili:** Casciu "Fransızca özgün, İtalyanca onaylı çeviri", Museo de' Medici "İtalyanca ve Fransızca iki nüsha" diyor. Anlatım ikisiyle de bağdaşıyor; ekrandaki "ITALIANO"nun çizilmesi tartışmalı.
