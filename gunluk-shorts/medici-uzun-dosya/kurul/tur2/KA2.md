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

---

## 2. aşama (ekran ve görsel olgular, hassasiyet) — v2 render (`out_p1/medici_P1.mp4`, 598,5 sn)

### 2.1 Karar ve SON puan

**SON: RED, 8,0/10 — VETO (tek madde: D1).**

v2'de 471,7–475,8 sn arasında papa V. Martinus Giovanni'ye **hançer** çekiyor. Kaynakta olmayan bir şiddet uydurulmuş, ve bu bir din adamı figürü üzerinden yapılmış. Bu düzeltilmeden yayına çıkılmaz.

Geri kalan her şey eşiğin üstünde:
- 1. aşama maddelerimin hepsi kapandı. İki istisna var: Y8 (kulak kontrolü kullanıcıda) ve Y9 (küçük bir kayıt temizliği).
- Ekrandaki kaynak damgaları ve nitelemeler, anlatımla ve kaynaklarla tutarlı (aşağıda tek tek).

D1 düzeltilir, ücretsiz ekran düzeltmeleri D2 ve D3 de uygulanırsa v3'te **ONAY 9,2** veririm. Bunu v3'te yalnız 465–476 sn ve düzeltilen levhalar üzerinde kısa bir gerileme kontrolüyle teyit ederim.

### 2.2 Neye dayandım

- **Videoyu oynatamadım, sesi dinleyemedim.**
- **v2'den kendi çıkardığım kareler:** sözcük çapalarına göre ≈100 kare. Hepsi `timeline.json`'daki sözcük zamanlarından seçildi; scratch: `…/scratchpad/ka2t2_v2/`. Bunlara şunlar dahil:
  - 471,4–475,6 sn arası 8 kare;
  - 465,4–467,6 sn arası 6 kare;
  - 355,6–360,3 sn arası 4 kare;
  - tam çözünürlüklü kırpımlar (402,5 sn Roma kartı; 499,6 ve 500,4 sn çubuk grafik).
- **Kod:** `scenes_c2.py:186` (`kind="papa", action="threat"`) ve `cilt_anim.py:1556` (`act_threat`: "ŞİDDET İŞARETİ … kolu **hançerle** yukarı kalkar", `props.append(_prop_fn("dagger", …))`).
- **Bağımsız ASR, yayınlanacak v2 mp4'ün kendi sesinden** (yerel Whisper medium; kesitler `timeline.json` zamanlarıyla):

  | Cümle | ASR'nin duyduğu | Sonuç |
  |---|---|---|
  | c2s10 | "De Rovar'a göre Roma şubesi zamanla sermayesiz çalışır hale geldi. Kasayı kilisenin yatırdığı para dolduruyordu." | ✓ |
  | c2s30 | "…ise 1430'larda hapisteyken olaya daha yakın bir kalemle…" | ✓; ad "Kavay Kant" duyuldu |
  | c2s7 | "Tim Parks'ın aktardığına göre…" | ✓ |
  | c1s16 | "O yılın mayısında…" | ✓ |
  | c2s20 | "…Kovanni'yi **Aforoz'da** tehdit etmek…" | bu üçüncü bağımsız işaret |
  | c2s1 | "Çözüm, kan bir odaydı." | işaretli |

- **curl ile okunanlar:**
  - DBI "Giovanni XXIII, antipapa": "una tomba che fu posta, **dopo lunghe discussioni**, nel battistero"; fidye için "35.000 gulden renani … un agente di Giovanni di Bicci".
  - de Roover n. 826: "Joannes quodam papa XXIII (John XXIII, once pope)".
  - Online Catasto (Brown) notu: "**the original declarations of wealth made in 1427 (9,780 households in Florence)**"; "Filippo di Tommaso Alberti **submitted his tax declaration** three times".
- `SURUM_KUNYESI_P1.md` (Y7) ve `yayin/studio_paketi_P1/01–05` (Y3, Y5) yeniden okundu.

### 2.3 1. aşama maddelerinin son durumu

| Madde | Durum | Kanıt (v2) |
|---|---|---|
| **Y1** c2s10 | **KAPANDI** | Ses yaması v2 mp4'te (ASR ✓). Ekranda "ROMA ŞUBESİ · SERMAYE · 1426'DA ÇEKİLDİ" + "DE ROOVER'A GÖRE" (397–405 sn). Küçük bir yerleşim notu var (D7) |
| **Y2** c2s30 | **KAPANDI** | Ses ✓. Levhalar "CAVALCANTI · HAPİSTE · 1430'LAR · OLAYA DAHA YAKIN" (555,8 sn) ve "1430'LAR · HAPİSTE" + "CAVALCANTI'YE GÖRE" + "ANEKDOT" (564,4 sn) |
| **Y3** paket satırları | **KAPANDI** | Tim Parks "Anlatımda anılan … kitabın kendisi okunmadı" ayrı başlıkta; çelişki cümlesi daraltıldı; sabit yorum dayanağı Online Catasto. 137/%29,8 KA1'in Online Catasto teyidine dayanıyor; kendim sorgulamadım, ama 9.780 hane ve "declarations" bilgisini aynı kaynakta okudum |
| **Y4** c0 kayıt yükseltmesi | **KAPANDI** | Casciu 2006 kaynak listesinde; ekranda "13 MADDE" + I–XIII + "FRANSIZCA" (42,8 sn) Casciu ile uyumlu |
| **Y5** "5:39'da" | **KAPANDI** | — |
| **Y6** YAYIN_TASLAK | **KAPANDI** | Satır 38 (yalnız okunanlar) ve satır 148 (Studio "Hayır" + şerh) |
| **Y7** ses lisansı kaydı | **KAPANDI** | `SURUM_KUNYESI_P1.md` §"Anlatım ve ses lisansı": voice_id, professional kategori, tarihler, 14 yama, U3 uzlaşması, Studio kararı ve şerhim. Kütüphane koşullarının ekran görüntüsü kanal sahibinde (kullanıcı eylemi) |
| **Y8** kulak kontrolü | **AÇIK** (kullanıcıda) | Yayınlanacak sesin ASR'si "aforozla"yı üçüncü kez "Aforoz'da" duydu; "kambiyodaydı" ve "Cavalcanti" de işaretli. "Aforozda" duyuluyorsa c2s20 yeniden üretilmeli: belgeli olgu cümlesi, ve SRT "aforozla" diyor |
| **Y9** `notlar_c2.md` eski tablo | AÇIK, küçük | Kayıt temizliği |
| **Ö6** Studio | Şerhim aynen kayıtlı, engellemiyorum | `SURUM_KUNYESI_P1.md` |

### 2.4 Ekran bulguları

#### ENGELLEYİCİ (VETO)

**D1. 471,7–475,8 sn: papa V. Martinus hançer çekiyor.**

Ne görünüyor (1920×1080'e göre):
- Papa figürü x≈1060–1400, y≈140–800.
- 471,9 sn: hançer elinde, bel hizasında.
- 472,4 sn: hançer elinde.
- 472,7 sn: hançer başının üstünde, saplama pozunda (≈(1250, 220)).
- 473,3 ve 474,8 sn: "AFOROZ TEHDİDİ" levhası çıkıyor; Giovanni mitrayı tutarak eğilip geri çekiliyor.

Bu sahne üç şeyi birden yapıyor:
1. **Kaynakta olmayan bir şiddet uyduruyor.** De Roover n. 45: "Pope Martin V had to threaten Giovanni di Bicci with **excommunication** if he failed to obey and restore the pledge" (Camerani Marri 1951, belge 48–49). Ortada yazılı, dinî-hukuki bir yaptırım tehdidi var; silah yok.
2. **Hassasiyet sorunu yaratıyor:** gerçek ve tarihî bir papayı silahlı saldırgan gibi çiziyor. Bu, Katolik izleyici için doğrudan, genel izleyici için de "Kilise = şiddet" diye okunabilecek bir karikatür. Kanalın Kilise'ye yaklaşımı videonun başka yerlerinde kurum ve kibir üzerine nazik bir mizah; bu kare o çizgiyi bozuyor.
3. **Belgeye dayanan bir olguyu sansasyonla gölgeliyor.** Video bu cümle için "BELGE · DE ROOVER" damgası koymuşken, belgede olmayan bir hançer ekliyor.

**Neden oldu (kod):**
- `scenes_c2.py:186` `action="threat"` kullanıyor. `cilt_anim.act_threat` her çağrıda hançer ekliyor ("ŞİDDET İŞARETİ"); P7'deki Pazzi suikastı (`scenes_c7.py:136, 150–151, 177`) için yazılmış bir jest.

**Yapılacak** (ücretsiz, yalnız bu segment yeniden render):
- `action="point"` kullanılsın (`act_point` mevcut; 471,4 sn'de papa zaten işaret ediyor, o jest yeterli).
- Bir **papalık mektubu (bulla)** gösterilsin. Projede `c2_bulla` simgesi var: kurşun mühürlü, ipe bağlı belge papanın elinde ya da papayla Giovanni arasında açılsın.
- İsteğe bağlı küçük etiket: "AFOROZ TEHDİDİ · MEKTUPLA".
- Giovanni'nin eğilmesi (saygı ya da itaat) hançer kalkınca sorun değil; kalabilir.

**Motor önerisi (yeniden kullanıma karşı, ~15 dk):**
- `threat` jesti ancak açık bir `prop="dagger"` parametresiyle hançer taşısın.
- `qa_donem` ya da `qa_flow`'a basit bir kural: `kind in {papa, kardinal, rahip}` ve `action="threat"` ise uyarı.

#### ÖNEMLİ (ücretsiz ekran düzeltmesi; veto değil)

**D2. HUD yılı, kaynak yazarlarının sahnelerinde olayı yanlış tarihliyor** (SA2-Y3'ü doğruladım).
- **119,4–127,1 sn:** "DANTE" ve "“lanetli çiçek”" sahnesinde HUD **1252**. Dante 1265'te doğdu; *Cennet* ≈1316–21'de yazıldı (genel bilgi, güven: yüksek).
- **130,6–136,6 sn:** "GIOVANNI VILLANI · KRONİKÇİ · ESKİ DARPHANE YÖNETİCİSİ" sahnesinde HUD **1252**. DBI: Villani "ufficiale della Moneta nel **1317**", "sovrintendente alla moneta … nel **1327-28**".
- **≈80–86 sn:** "Bugün Uffizi'nin kapısında…" kuyruğunda HUD **1737**.

HUD kanalın "anlam taşıyan sayacı" (Anayasa §1). Bu karelerde ekran, olaya yanlış bir tarih yazıyor.

Yapılacak, ikisinden biri:
- bu çekimlerde HUD gizlensin (`hud=False`); ya da
- levhalara tarih eklensin: "DANTE · CENNET, ≈1320"; "VILLANI · 1317'DE DARPHANE GÖREVLİSİ".

Kuyrukta HUD gizlensin ya da "BUGÜN" yazsın.

c2'deki Machiavelli (HUD 1429; levha "BİR ASRA YAKIN SONRA") ve Cavalcanti ("1430'LAR") levhaları zamanı kendisi söylüyor, sorun yok. Ama c1s20'deki Machiavelli levhası "MEDİCİ SİPARİŞİYLE TARİH YAZAR" (HUD 1378) zaman işareti taşımıyor; "≈1520" eklensin.

**D3. 11,6–12,6 sn: "ANNA MARIA LUISA · MEDİCİ'NİN SON ÜYESİ" levhası** (x≈950–1730, y≈480–560).

Anlatım aynı anda "Toskana'yı yönetmiş Medici hattının son üyesi" diyor; levha bu nitelemeyi düşürüyor. it.wiki: "Con la sua morte si estinse **il ramo granducale** della famiglia Medici". Yan kollar sürdü (güven: orta-yüksek). Kapaktaki "SON MEDİCİ" yaygın bir sıfat olarak kabul edilebilir; ama kimlik levhası bir olgu cümlesi gibi okunuyor.

Yapılacak: "MEDİCİ HANEDANININ SON ÜYESİ" ya da "BÜYÜK DÜKAL KOLUN SON ÜYESİ".

#### KÜÇÜK

| # | Ne | Nerede | Önerim |
|---|---|---|---|
| D4 | Villani levhası "1300'DE PERUZZİ ORTAĞI · **ŞİRKETİ 1341'DE BATTI**" muğlak (SA2-Y5'i doğruladım). DBI'ye göre 1341'de batan, Villani'nin yönettiği **Buonaccorsi**; Peruzzi 1343'te battı. İzleyici "şirketi"ni Peruzzi sanabilir. Anlatım (c1s10) doğru | 172–180 sn; levha x≈880–1640, y≈180–320 | "1300'DE PERUZZİ ORTAĞI · YÖNETTİĞİ BUONACCORSI 1341'DE BATTI" |
| D5 | Mezar yazıtı ekranda Türkçe oyulmuş "ESKİ PAPA" (SA2-Y8). Özgün yazıt Latince: de Roover n. 826 "Joannes quodam papa XXIII". c0'da çeviriye "ÇEVİRİ" damgası koyan video, burada çeviriyi taşa oyuyor (yöntem tutarlılığı). "Quondam" hem "eski" hem "merhum" demek; Martinus'un itirazı da bundan | 452,7–464,1 sn; yazıt x≈660–1260, y≈660–770 | Taşta "IOANNES QVONDAM PAPA XXIII", altında levha "ESKİ PAPA · ÇEVİRİ" |
| D6 | Catasto "HANE HANE" ve kapı kapı memur ziyareti gibi sahnelenmiş (SA2-Y6). Online Catasto: veriler hane reislerinin **yazılı beyannameleri** ("declarations"). Anlatım "yazdırdı" diyor, uyumlu | 486,6–493,1 sn | Hane reisleri masaya beyanname (portata) getiriyor; etiket "BEYANNAME" |
| D7 | "SERMAYE · 1426'DA ÇEKİLDİ" yazısı kırmızı X'in altında; "1426'da çekildi" cümlesinin üstü çizilmiş gibi okunuyor, tersine anlam riski | 397–405 sn; kart x≈180–640, y≈395–640 | X yalnız kese simgesinin üstüne; yazı X'in dışında |
| D8 | "BELGE · DE ROOVER" damgası ≈0,8 sn, "DE ROOVER · ANDIĞI ARŞİV BELGELERİ" levhası ≈1,3 sn görünüyor. Bu bölümün yöntem damgası, okunmaya zaman kalmıyor | 465,4–466,7 sn | ≥2 sn tut, ya da damgayı oda çekiminde de göster |
| D9 | "BRUGGE · KLASİK BİR ÖRNEK" nitelemesi 358,4 sn'den sonra "BARSELONA'YA ÇEKİLMİŞ POLİÇE" etiketinin altında kalıyor. Önceki ~3 sn okunur | 358,4–360,5 sn; x≈520–1400, y≈270–330 | Etiketi aşağı al |
| D10 | Sayaç "150.000+"a doğru sayarken ara değerler artıyla yazılıyor ("143.194+"); kesin bir ara rakam gibi okunuyor | ≈515,4–516,4 sn | "+" yalnız son değerde, ya da yuvarlak adımlarla sayım |
| D11 | Loggia dei Lanzi 1338 sahnesinde bitmiş görünüyor (SA2-Y2) | 141,4 sn, sağ kenar | Yapımı 1376–82 (güven: yüksek). Yalnız görsel anakronizm, anlatıda karşılığı yok; SA alanı |
| D12 | 1520 tarihli "MEDİCİ SİPARİŞİ" mührü 1465 öncesi armayla (zambaksız palle) çizilmiş (SA2-Y4) | 575,5–580 sn | 1465'te XI. Louis'nin verdiği zambaklı mavi top sonrası arma (güven: yüksek). Görsel; SA alanı |
| D13 | "Machiavelli'nin çizdiği" sahnesinde üç özdeş yoksul figür, 17. yüzyıl görünümlü şapkalar (SA1-Y5, SA2-K7). Hassasiyet açısından sorun yok: saygın duruş, sadaka veriliyor | 569,1–575,0 sn | Klon izlenimi "yoksul" kalıbını güçlendiriyor; yaş, cinsiyet ve duruş çeşitlensin |
| D14 | Paket: "temsilî portreler TEMSİLÎ damgasıyla işaretlidir" yalnız madalyalar için doğru (Lorenzo 533,8 sn, Cosimo 583,7 sn ✓). Sahne figürleri de temsilî ama damgasız | `02_aciklama.txt` | "Madalya portreleri TEMSİLÎ damgasıyla işaretlidir; tüm figürler temsilîdir, gerçek benzerlik iddiası yoktur." |

#### Doğruladığım ve doğru bulduğum ekran olguları ve damgaları

- **c0:**
  - kapak yankısı (1,6 sn) ve "18 ŞUBAT 1743";
  - "31 EKİM 1737" + takvim "TEMMUZ 9 1737" (27,8 sn) ve 114 güne sayaç;
  - "ANNA MARIA LUISA" / "LORRAINE TARAFI" mühürleri (38,9 sn);
  - "13 MADDE", I–XIII, "FRANSIZCA" (42,8 sn);
  - "ITALIANO" çizilmesi (48,4 sn): Casciu'nun "özgün Fransızca, İtalyancaya çevrilip onaylandı" bilgisiyle uyumlu, kabul;
  - galeri "ÇEVİRİ" (61,1 sn);
  - harita "3. MADDE · ÖZET / Koleksiyonlar Floransa'dan ve Büyük Dukalık'tan çıkarılamaz." tırnaksız + "SINIR YAKLAŞIKTIR" (68,5 sn);
  - "GEREKÇE … ÇEVİRİ" (76,3 sn).
- **c1:**
  - "3,5 GRAM · 2 CM" (117 sn);
  - "DANTE · “lanetli çiçek”" (çevirimiz, tırnaklı);
  - "VILLANI'YE GÖRE · TAHMİN" (141,4 sn);
  - "PERUZZİ … 15 ŞUBE · BİR KAYNAĞA GÖRE" (160,9 sn); "1340'LAR … ŞUBE SAYILARI TEMSİLÎ" (165,6 sn);
  - "III. EDWARD · ÖDENMEDİ";
  - "MART 1348 · YAZ BOYUNCA" (185,3 sn); veba ve toplu mezarda beden yok ("KATMAN KATMAN" yalnız toprak, 207,5 sn);
  - "MARCHIONNE … 12 YAŞINDA";
  - "SALVESTRO DE' MEDICI · MEDİCİ AİLESİNİN BAŞKA BİR KOLU · KURAYLA" (224,9 sn);
  - "ARMALAR TEMSİLÎ";
  - "MICHELE DI LANDO · YÜN TARAYICISI → GONFALONIERE", "ÇEKİLDİ" yok (243,4 sn);
  - "CIOMPI'NİN TALEPLERİ … YAZILDIĞINA GÖRE": üç kalem anlatımla aynı (252 sn);
  - "KURGU · KONUŞMA TARİHÇİNİN" (265,9 sn);
  - "AĞUSTOS SONU" milis alayı, şiddet yok (271 sn); "YÖNETİMDEN DE DIŞLANDILAR" (276,5 sn);
  - "MEDİCİ'NİN BU KOLUNDAN"; "1390'LARIN BAŞI · DEVRALDI · ALACAK + BORÇ"; "1.500 FLORİN";
  - Orsanmichele yalnız "VIA PORTA ROSSA" (322,3 sn); "10.000 FLORİN".
- **c2:**
  - "BRUGGE · KLASİK BİR ÖRNEK" (355,6–358 sn);
  - "VİCDAN KOMİTESİ · EN YARATICI DEPARTMAN";
  - "TİM PARKS · AKTARDIĞINA GÖRE" (383,5 sn);
  - "MİT" (415,7 sn); zaman çizgisi yalnız "1340 CENOVA · 1494 PACIOLI", "MEDİCİ İCADI ✗", 1407 yok (423,4 sn);
  - "COSSA = XXIII. JOHANNES · PİSA PAPASI · BUGÜN KARŞI PAPA SAYILIR" (439,8 sn);
  - "KAYNAKLAR AYRIŞIYOR · KEFALET/FİDYE": DBI'de fidye "35.000 gulden" ✓;
  - "V. MARTINUS · İTİRAZ": DBI "dopo lunghe discussioni" ile uyumlu;
  - "22 YIL KESİNTİSİZ + 18 YIL ARALIKLI · 1422" (484,4 sn);
  - "KAYITLI SERVET %29,8 · 137 HANE · BİR HESABA GÖRE", son değerler 30/70 ✓;
  - "PALLA STROZZI · 1427'NİN EN ZENGİNİ · 163.000 FLORİN · YAKLAŞIK" (502,1 sn);
  - "GIOVANNI · CATASTO'YU DESTEKLEDİ";
  - "150.000+ FLORİN KÂR" (516,8 sn);
  - "20 ŞUBAT 1429 → 1428 · FLORANSA TAKVİMİ · YILBAŞI 25 MART";
  - "LORENZO · TORUNUNUN OĞLU · İLERİDE MUHTEŞEM · 180.000 · LORENZO'NUN KAYDINA GÖRE" + "TEMSİLÎ";
  - "MACHIAVELLİ'YE GÖRE · ANEKDOT";
  - "MACHIAVELLİ'NİN ÇİZDİĞİ · KİMSE İSTEMEDEN DE";
  - "O KALEM · MEDİCİ SİPARİŞİ";
  - "COSIMO · 39 YAŞINDAYDI · 1389 DOĞUMLU" + "TEMSİLÎ";
  - kule (hücre gösterilmiyor); bitiş ekranı.
- **1737 imza sahnesi (32,0–34,5 sn; başkanın sorusu):** Odada, Medici arması altında bir siluet belgeyi mühürlüyor; yer ya da kimlik yazısı yok, anlatım yalnız "imzalandı" diyor. Sözleşme Viyana'da elçilerce imzalandı (Verga; Casciu: "Alla corte di Vienna agiva … il marchese Ferdinando Bartolommei"). Casciu'ya göre İtalyanca metin ayrıca "ratificati" (onaylandı); XIII. madde bir ay içinde onay öngörüyor. Bu yüzden sahne Floransa'daki **onay** olarak okunabilir. **Kabul ediyorum**, düzeltme gerekmiyor. İleride c0 yeniden render edilirse "VİYANA'DA İMZALANDI · FLORANSA'DA ONAY" küçük etiketi daha da kesin olur.

### 2.5 Başkanın ilettiği bulgular (benim hükmüm)

| | Bulgu | Hükmüm | Gerekçe / güven |
|---|---|---|---|
| a | Papanın hançeri (AN1/AN2) | **Doğrulandı, ENGELLEYİCİ (veto) = D1** | Kareler ve kod. Önerilen jest: işaret eden el + bulla, silah yok. Güven: yüksek |
| b | HUD 1252 (Dante, Villani), HUD 1737 + bugün (SA2-Y3) | **Doğrulandı, ÖNEMLİ = D2** | Kareler 124,4, 133,5 ve 80,5 sn. Güven: yüksek |
| c | Loggia dei Lanzi (SA2-Y2) | **Doğrulandı, küçük = D11** | 1376–82 (genel bilgi, güven: yüksek). 1378 Temmuz'da yapımı sürüyordu; 1338'de yoktu |
| d | 1520 mührü, 1429 arması (SA2-Y4) | **Doğrulandı, küçük = D12** | 1465 öncesi arma; görsel, anlatıda iddia yok |
| e | Villani levhası (SA2-Y5) | **Doğrulandı, küçük = D4** | Tur 2 1. aşamadaki c1s10 kararımla tutarlı: anlatım doğru, levha muğlak. DBI okundu |
| f | "ESKİ PAPA" Türkçe yazıt (SA2-Y8) | **Doğrulandı, küçük = D5** | de Roover n. 826 okundu |
| g | Catasto kapı kapı (SA2-Y6) | **Doğrulandı, küçük = D6** | Online Catasto notu "declarations" diyor, okundu |
| h | Özdeş yoksullar, 17. yy şapkaları (SA1-Y5, SA2-K7) | **Kısmen.** Hassasiyet sorunu yok; sanat ve dönem sorunu = D13 | — |

### 2.6 Kullanıcının sorusu (v2 karelerine göre, alanımdan)

v2'de figürlü oda ve sokak sahneleri, halılar, ışık ve tutarlı karakter tasarımları "kodla, elle yönetilmiş" duruyor. Tipik YZ izleri yok: bozuk el, bozuk yazı, tutarsız mimari görmedim. Kaynak damgaları (BELGE, ANEKDOT, MİT, TEMSİLÎ, "…GÖRE") bilgi taşıyor ve güven veriyor.

Ucuz ya da şablon hissini tek tek kareler veriyor:
- belgeye dayanan bir anı sansasyona çeviren hançer (D1);
- üç özdeş yoksul (D13);
- birbirinin üstüne binen etiketler (D7, D9).

Bunlar düzelirse, kaynak ve hukuk merceğinden çizim dili güven veren bir artıya dönüşüyor.

### 2.7 En emin olmadığım nokta (2. aşama)

1. **D3'ün ağırlığı.** "Son Medici" yaygın bir sıfat; ben levhayı olgu cümlesi saydığım için önemli dedim. Başkan "kapakla tutarlı sıfat" diye kabul ederse vetoya konu etmem.
2. **Y8.** Üç bağımsız ASR da "aforozla"yı "Aforoz'da" duydu. Yine de Whisper'ın Türkçe dil modeli "-la"yı "-da"ya çevirebilir. Son söz kulağın.
3. **Loggia'nın 1378 görünümü.** Yapımın Temmuz 1378'de ne kadar ilerlediğini kaynaktan okumadım; 1338 için anakronizm kesin.
