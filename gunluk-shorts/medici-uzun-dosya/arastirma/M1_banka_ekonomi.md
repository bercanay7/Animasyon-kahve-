# M1 — BANKA VE EKONOMİ · Kaynaklı Olgu Dosyası

**Kapsam:** c1 *Florin Şehri* · c2 *Defterin Sihri* · c9 *Defter Kapanıyor* · c3/c4'ün para yönü · c16'nın miras tartışması.
**Hazırlayan:** M1 araştırma ajanı · 18 Ekim 2026 · Bu bir **senaryo değil**, senaryoyu yazacak kişi için olgu dosyasıdır · git işlemi yapılmadı.

---

## 0. Başlık notu: araçlar, sınırlar, sınıf politikası

| Araç | Ne oldu |
|---|---|
| **WebSearch** | Çalıştı: yaklaşık **73 başarılı çağrı** (7'si `extended`, kalanı `standard`). Tur başına 200 çağrılık **ortak kota** (tüm ajanlarla paylaşılan) doldu; son iki sorgu **hiç çalıştırılmadı** (hata: "web search budget is used up"). Kotayı aşmak için başka yol denenmedi. |
| **WebFetch** | **Hiç çalışmadı.** 10 deneme (en.wikipedia.org, archive.org ×2, www.gutenberg.org, www.britannica.com, www.british-history.ac.uk, r.jina.ai, www.gwern.net, www.economics.utoronto.ca, arxiv.org, ehs.org.uk) hepsi `getaddrinfo ENOTFOUND`. **Hiçbir sayfa açılıp okunamadı.** |
| **Bash** | Proxy durum/README okuma denemesi izin sistemi tarafından reddedildi; **dolaşılmadı**. Bash yalnız klasör oluşturmak, dosya birleştirmek ve tablo/sayı denetimi (yerel betikler) için kullanıldı; internete erişmedi. |
| **Sonuç** | **● (birincil metin gerçekten okundu) sınıfı bu dosyada YOK.** Birincil metinlere (Machiavelli, Villani, Boccaccio, Stefani, Cavalcanti) ait olan parçalar yalnız **arama özetinin aktardığı kadarıyla** görüldü; sayfaları açılmadı. |

**Yararlı bir hile (diğer ajanlar için):** `WebSearch`'e `allowed_domains: ["dokumen.pub"]` verince özet, de Roover (1963), Parks, "Comparative History of Bank Failures" vb. **kitap kopyalarının metninden** cümleler getirdi (aşağıda K58–K63 olarak işaretli). `gutenberg.org` ile de Machiavelli/Ross metinlerinden kısa parçalar geldi. Bunlar **ikincil/aracılı aktarımdır**; sayfa numarası yok.

**Sınıf ölçeği (bu dosyada):**
- **●** birincil metin gerçekten okundu → *kullanılmadı (0)*.
- **◐** ≥2 *bağımsız* ikincil kaynakta uyumlu (arama özeti dahil). Wikipedia ve onun kopyaları (RallyPoint, Wikiwand, nooknet vb.) **tek kaynak** sayıldı. İçerik çiftlikleri ("net worth" siteleri) hiç sayılmadı.
- **○** tek ya da doğrulanamayan kaynak.
- Etiketler: **ANEKDOT** (sonradan yazılmış/anlatılan), **HAFIZA** (araçla doğrulanamadı, kendi bilgim; **senaryoya girmeden önce doğrulanmalı**).
- **Birebir alıntı kuralı:** Sütunlarda tırnak içinde verilen metin, arama özetinde *tırnaklı olarak göründüğü* kadarıyla verilmiştir (çoğu İngilizce çeviri/ikincil metin). Orijinal İtalyanca/Latince sayfadan **kontrol edilmedi**. Kendi hafızamdan yazdığım birkaç İtalyanca satır açıkça **HAFIZA** diye işaretli. Türkçe çeviriler **bize aittir**.

**Çalışırken sapan tuzaklar (not):** Arama özetleri kimi zaman yanlış atıf yapıyor (ör. Piero'nun "babasının son sözlerini alması" Lorenzo'nun 1492 ölümüne ait, Giovanni'nin 1429 ölümüne değil). Bu tür yerlerde özet çelişkileri açıkça notlandı.

### Hızlı özet

- **Sayılar:** Kronoloji **86 satır** (2A: 70, 2B: 16): **◐ 39**, **○ 44**, **HAFIZA/eksik 3**, **● 0** (ana sınıfa göre; 4 satırda ayrıntı/rakam ayrıca ○). **Canlı ayrıntı 54 satır** (c1: 10, c2: 10, c3: 10, c4: 8, c9: 9, c16: 7). Mit/tartışma **17 madde**, sahne adayı **4 (+1 zayıf yedek)**, DÜZELTME/NÜANS **10**.
- **En sağlam üç malzeme:** (1) Cossa'nın Vaftizhane mezarında **"eski papa"** yazıtı (3 bağımsız kaynak; D15–D16, S3). (2) Giovanni'nin **karısının 1.500 florinlik çeyiziyle** Roma'da ortak olması, 1397'de **Orsanmichele köşesine** taşınması ve 20 Şubat 1429 ölümü — DBI + 3 kaynak (D09–D11, S2). (3) **Ciompi 22 Temmuz 1378** ve Machiavelli'nin **uydurduğu** konuşma (D06–D07, S1).
- **En riskli üç iddia:** (1) **"Cosimo sanata 600.000 (663.755) florin harcadı"** — kapsam/ölçü belirsiz, kaynaklar tek kök (DÜZELTME #4). (2) **Medici'nin papalık *depositario*'luğunun tarihleri** (1410 mu, 1420'ler mi; 1455 görevden alınma) — kaynaklar çelişiyor (#7). (3) **Lorenzo'nun çeyiz fonu/banka zaafı** ve **"Londra şubesi 1478'de kapandı"** gibi tarihli cümleler — tek zayıf kaynak ya da desteksiz (D46, #65).
- **Eksik kalan:** ücret tabloları, Palazzo Medici maliyeti, Giovanni'nin 1427 beyanı, Tolfa/Foça/Volterra şap hikâyesi, şube kapanış yılları, 1494 el koyma, Padgett–Ansell, Fugger/Rothschild iddiası (§10).

---

## 1. DÜZELTME / NÜANS listesi (KAPSAM_VE_YAPI.md için)

> Kural gereği hafızadan kurulan iskelet doğrulandı; yanlış ya da kayan yerler **DÜZELTME**, küçük kaymalar **NÜANS** olarak yazıldı.

1. **DÜZELTME (c1/c2, "1397 kuruluşu" ve "Giovanni'nin tezgâhı").** Giovanni sıfırdan banka açmadı. ≈1385'te Vieri di Cambio'nun **Roma şubesinde** çalışıyor, karısı Piccarda Bueri'nin **1.500 florinlik çeyiziyle ortak oluyor**; Vieri çekilince (1393) Roma bankasının alacak-borçlarını devralıp firmayı *"Giovanni de' Medici e compagni in Roma"* yapıyor; **1397'de merkezi Roma'dan Floransa'ya (Orsanmichele yakını, Via Porta Rossa–Via Calimala kavşağı) taşıyor**. "1397 kuruluş" = *taşıma + yeni ortaklık*. (K50, K58, K49, K51; ◐). Bazı kaynaklar 1385 ya da 1393'ü "kuruluş" sayar; Wikipedia'da "1397'de yeğeni Averardo'nun bankasından ayrıldı" biçiminde başka bir anlatım da var (K01). **Güvenli cümle:** *"1397'de Roma'daki işini Floransa'ya taşıyan ortaklık."*
2. **NÜANS (c1).** "Çok şubeli banka" Medici'nin icadı değil: **Peruzzi** 1330'larda **15 şube, >100.000 florin sermaye, ≈100 faktör** (K12; ○). Medici'nin farkı, şubeleri **ayrı ortaklıklar** olarak kurması (§5C). Wikipedia'daki "Bardi/Peruzzi 1347'de Kara Veba'dan sonra çöktü" ifadesi başka kaynaklarla çelişir: çöküş **1342–46**, Veba **1348** (K11–K14) → Veba "neden" olarak yazılmamalı.
3. **DOĞRULANDI (§4/§7 "çifte kayıt").** "Medici çifte kaydı icat etti" = **mit** (◐). En eski tam örnek: Cenova **Massari hesapları 1340** (erken biçim ≈1327); Venedik defterleri **1407**; Datini defterleri ≈1380'de "ilkel" biçim; Cotrugli el yazması **1458**; Pacioli *Summa* **1494** (bazı kaynaklarda 1493). Medici için "Giovanni getirdi" diyen tek yer atıfsız, "[hangisi?]" etiketli bir forum/grup metni (K118); K75–K78 bunu desteklemiyor.
4. **DÜZELTME riski (c4/c16, "Cosimo sanata 600 bin florin harcadı").** Wikipedia: *"over 600,000 gold florins … on art and culture"* ve *≈500 milyon dolar* (K89; ○, tek kök). Benim hafızamdaki kayıt (**HAFIZA, doğrulanamadı**): Lorenzo'nun *Ricordi*'sinde 1434–1471 arası **663.755 florin**, kalemler **bina, sadaka ve vergi** — yani "sanat" değil. İki sayı aynı şeyi ölçmüyor olabilir. **Doğrulanana kadar senaryoda rakam yok.**
5. **NÜANS (c3, "serbest kalışı, Venedik sürgünü").** Hüküm **Padova'ya 10 yıl sürgün**; fiilen **Venedik**'te kaldı (Michelozzo'nun San Giorgio kütüphanesi anekdotu buraya bağlanıyor) (K103, K104, K105; ◐).
6. **NÜANS (§8 alum zinciri).** Zaman çizelgesi: 1453 Fetih → **1455 Foça'nın Osmanlı eline geçişi (HAFIZA)** → **1461 Tolfa keşfi (HAFIZA)** → **1466 Medici'nin papalık şap şirketine ortak olması (◐)** → 1470 Ischia anlaşması (○). "Fetih sonrası pazar" ile Medici'nin payı arasında **13 yıl** var; 1466 sözleşmesi **II. Paulus** dönemine ait (bir özet yanlışlıkla II. Pius'a bağlamıştı; Pius 1464'te öldü) (K110, K111).
7. **NÜANS (c2, "Papa'nın bankacısı").** Medici'nin papalık *depositario generale*'liğinin başlangıcı kaynaklarda uyuşmuyor: **XXIII. Johannes** (1410–15) vs **V. Martinus sonrası 1420'ler** (DBI: 1422'de Bartolomeo Bardi'nin atanması + "22 yıl kesintisiz"); **1455'te III. Callistus Roma müdürü Roberto Martelli'yi görevden aldı** (○). "Medici 1410'dan beri papalık bankacısı" gibi kesin cümle kurma (K48, K50, K115).
8. **NÜANS (c2, başlangıç ölçeği).** Kuruluş sermayesi **10.000 florin**, Roma şubesine **ayrı sermaye verilmedi** (Kilise mevduatla besliyor), **1402'de toplam ≈17 çalışan, Floransa merkezinde 5**. Banka *küçük* başladı (K01, K53, K58).
9. **NÜANS (c1, Ciompi'deki Medici).** 1378'de gonfaloniere olan **Salvestro de' Medici** ile Giovanni'nin atası aynı hat mı, kaynaklar bağlamıyor (arama özeti "doğrulanamadı" dedi). Hafızam: Salvestro di Alamanno, ayrı kol (**HAFIZA**). "Ailenin başka bir koluydu" demek yeter.
10. **NÜANS (tez cümlesi, "banka öldü").** Resmî son **1494** (Piero'nun sürgünü), ama fiilî çözülme **1470'lerden** itibaren şube şube; ve "Lorenzo'nun suçu" tek nedenli anlatılırsa kaynaklarla uyuşmaz: Machiavelli (1520'ler) ajanların "prens gibi" davranışını suçlar; de Roover ekolü yönetim zaafı der (HAFIZA); Brugge/Londra'da **Sassetti'nin 1471 kararı** ve **Portinari'nin** rolü ayrı (K93, K95). Tek kişiye bağlama.

---

## 2. Kronoloji tablosu

> Sütunlar: `# | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not`. Sıra **kabaca olay tarihine** göredir (ilk tablo; dönem-kârı satırları dönemin bittiği yere yakın konmuştur); tarihyazımı/kaynak olayları ayrı tablodadır (2B). "Hesap" satırları bana aittir ve **türetilmiş** diye işaretlidir. Sınıf hücresinde iki sınıf varsa (ör. "◐ / ○") ilki ana olguya, ikincisi ayrıntı/rakama aittir.

### 2A. Olay kronolojisi

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---:|---|---|---|---|---|---|
| 1 | c1 | ≈1150 | Calimala loncasına ait en eski belge ≈1150'ye atılır; Calimala çoğu anlatımda "en eski lonca" | ○ | K07, K10 | Tek kaynak yıl veriyor. |
| 2 | c1 | 1197 | Yün (Lana) loncası Calimala'dan ayrı bir büyük lonca olarak ayrılır | ○ | K07, K10 | Tek kaynak. |
| 3 | c1/c2 | 1230 | Medici adı ilk kez bir belgede anılır; Wikipedia kurucu olarak Giambuono'yu gösterir; köken Mugello | ○ | K114 | "Medico" (doktor) kökeni *efsane*, "palle" için bezant (Bizans ağırlığı) açıklaması birkaç açıklamadan biri. |
| 4 | c1 | 1252 | **Altın florin Floransa'da ilk kez basılır** | ◐ | K04, K05, K06 | Cenova'nın altın *genovino*'su aynı yıl (**HAFIZA**) → "Avrupa'nın ilk altın parası" denmez. Wikipedia: "uluslararası para statüsü kazanan ilk Avrupa altın sikkesi" (nitelikli). |
| 5 | c1 | 1252 | Florin'in ağırlığı o günün muhasebe birimi **1 lira (=20 soldi=240 denari)** değerine denk seçildi; 1252 Pisa kaydında florin 20 soldi | ◐ | K101, K100 | İki ayrı kaynak; ama "1 altın florin=20 gümüş florin" diyen forum yazısı güvenilmez sayıldı. |
| 6 | c1 | 1252–1533 | Floransa sikkesinin tasarımı ve metal standardı ≈280 yıl **değişmedi** | ◐ | K04, K05 | "1533" bitiş yılı tek özetten; ağırlık: 3,53 g (.986) / 3,49 g, çap 19,9 mm. |
| 7 | c1 | 1266 | 21 loncanın ikinci listesi: **7 büyük (Arti Maggiori) + 14 küçük** | ◐ | K07, K08, K09 | "7 büyük"ün üyeliği kaynaklar arasında tutarsız (Seta ↔ Por Santa Maria). Kesin olanlar: **Calimala, Lana, Cambio**. |
| 8 | c1 | 1293 | **Ordinamenti di Giustizia** (Giano della Bella): magnatlar siyasetten dışlanır, loncalar siyasi gücü sağlamlaştırır | ◐ | K07, K08 | Priörlerin sayısı kaynaklarda "12" diye geçiyor ve 7 büyük lonca sayısıyla çelişiyor → özetin hatası olabilir. |
| 9 | c1/c2 | 13. yy sonu | Medici'ler Mugello'dan şehre taşınır, tarımdan ticarete geçer | ○ | K114 | Tek kaynak. |
| 10 | c1 | 1324–25 | 1 florin ≈ **66–67 soldi** (≈3,3 lira) | ○ | K100 | Spufford'a dayalı kayıt. |
| 11 | c1 | 1330'lar | **Peruzzi:** 15 şube (Orta Doğu'dan Londra'ya), >100.000 florin sermaye, ≈100 faktör | ○ | K12 | Wikipedia; Medici ile kıyas için ölçü. |
| 12 | c1 | 1338 | **Villani'nin Floransa sayımı:** nüfus **≈90.000**; okuma öğrenen çocuk **8–10 bin**, abaküs/algoritma **1.000–1.200**, gramer-mantık **550–600** (4 büyük okulda) | ◐ | K33, K34, K35, K36 | Rakamlar sorgulanıyor ama 1427 catasto okuryazarlık resmiyle uyumlu bulunuyor (bir kaynak); "açık soru" diyen de var. Villani darphane yöneticisiydi (1310'lar). |
| 13 | c1 | 1342–1346 | **Bardi ve Peruzzi çöker.** Peruzzi 1343 (iflas 1345); Bardi 1344 (Wikipedia) ya da 1346 (Cambridge). Britannica: iki şirketin üyeleri 1342–45 arasında iflastan tutuklandı | ◐ | K11, K12, K13, K14 | Tarihler çelişkili, aralık verildi. |
| 14 | c1 | 1340'lar | **Villani'ye göre** Edward III'ün borcu: Bardi'ye **900.000**, Peruzzi'ye **600.000** altın florin (£135.000 / £90.000) | ◐ | K11, K12, K13 | Bu rakam Villani'nindir, defter bakiyesi değil; Peruzzi kayıtları o kadar sermayeleri olmadığını gösteriyor; "Edward'ın borcu yüzünden battılar" görüşü **basit** sayılıyor; Villani'nin kardeşi Peruzzi'deydi (taraflı). |
| 15 | c1 | Mart–Temmuz 1348 | **Kara Veba Floransa'da.** Boccaccio: surların içinde **100.000'den fazla** kişi öldü | ◐ (iddia Boccaccio'nun) | K21, K22, K23 | Modern tahminler: "yarıdan fazlası" (K17), "dörtte üçü" (başka kaynak), "üçte ikisi" (Hektoen'in andığı eski görüş) → tutarsız. Boccaccio'nun anlatımının öncül veba anlatılarından beslendiği de söyleniyor (K23). |
| 16 | c1 | 1348 | Floransa kararnamesi "birçok yurttaşın birden yoksullaştığını, yoksulların zenginleştiğini" kabul eder; **kentte ücret artışına izin, kırda ücret bastırılır** | ○ | K18, K20 | İkincil özet. |
| 17 | c1 | 1348–1350 | Kuzey İtalya'da tüketici fiyatları **%19** arttı | ○ | K18 | Tek kaynak. |
| 18 | c1 | 18 Haz 1378 | **Salvestro de' Medici** halk alkışıyla gonfaloniere seçilir (anti-magnat Ordinamenti'yi yenileme girişimi) | ○ | K27, K28 | Tarih tek kaynaktan. |
| 19 | c1 | 22 Tem 1378 | **Ciompi Palazzo Vecchio'yu ele geçirir** (Santa Croce Fransiskenlerinin yardımıyla, The Florentine); yün tarayıcısı **Michele di Lando** gonfaloniere; Salvestro istifa etmek zorunda | ◐ | K27, K28, K30 | Taleplere dair: vergi adaleti, loncasız işçilere lonca hakkı, kamu borcunun azaltılması (K29). |
| 20 | c1 | 30 Tem 1378 | Mevcut 21 loncaya **üç yeni lonca** eklendi | ○ | K30 | Tek kaynak. |
| 21 | c1 | Ağustos sonu 1378 | Büyük ve küçük lonca milisleri Ciompi'yi ezer ("Floransa tarihinin en kanlı günlerinden"); yeni lonca kaldırılır; di Lando dışındaki Ciompi hükümetten dışlanır | ◐ | K28, K30 | Bir kaynak "3,5 yıl (1382'ye kadar)" diyor → muhtemelen halk hükümetinin süresi; ayaklanma ≈3 ay. |
| 22 | c1 | 1370'ler sonu–1380'ler | **Marchionne di Coppo Stefani** (d. 1336) *Cronaca fiorentina*'yı yazar; veba bölümü İngilizce çevirilerde "Rubrik 643" | ◐ | K24, K25 | Kullanıcı sorgusundaki "634" muhtemelen yazım hatası ya da farklı numaralama (Rodolico, *RIS* 30, 1903–13). |
| 23 | c1 | ≈1385 (1386) | Giovanni (≈25) Roma'da Vieri di Cambio'nun şubesinde **faktör**; Piccarda Bueri çeyizi **1.500 florin** ile ortak olur; **1386'da Arte del Cambio'ya** girer | ◐ | K50, K49, K48, K52 | 1385/1386 ayrımı: Wikipedia "Vieri e Giovanni de' Medici in Roma 1386". |
| 24 | c1 | 1391–1393 | Vieri'nin bankası üçe bölünür (1391–92, Wikipedia) / Vieri çekilir (1393, DBI); Giovanni **Roma bankasının alacak-borçlarını devralır** → *"Giovanni de' Medici e compagni in Roma"* | ◐ | K01, K50, K52 | İki kronoloji çelişkili; ikisi de yazıldı. |
| 25 | c1/c2 | **1397** | **Giovanni merkezi Roma'dan Floransa'ya taşır** → bankanın kuruluş yılı. Merkez **Orsanmichele yakını, Via Porta Rossa–Via Calimala kavşağı**; Roma finans merkezi olarak kalır | ◐ | K58, K49, K51 | de Roover'dan aktarım: "1397 may be regarded as the founding date…". |
| 26 | c2 | 1397 | **Kuruluş sermayesi 10.000 florin**; yarısı Giovanni'den (**5.000**; Türkçe *Medici Ailesi* kitabı: **5.500**), kalanı Benedetto de' Bardi + ikinci ortak ("Gentile Boni"; HAFIZA'mda "Buondelmonti" var, **doğrulanamadı**) | ◐ (toplam) / ○ (paylar) | K01, K53, K60 | Bir Portekizce kaynak (Ferguson'un *Ascent of Money*'sinin Portekizce baskısı olabilir) 1402'de ≈20.000 florin diyor (○, K116). |
| 27 | c2 | 1397 | Roma şubesi faaliyete başlar; küçük ortak **Benedetto di Lippaccio de' Bardi** (1373–1420). **Roma şubesine ayrı sermaye verilmedi** | ○ | K58, K52 | Kilise mevduatla beslediği için. |
| 28 | c2 | 1398 → 25 Mart 1402 | Venedik ofisi kararı (1398); **25 Mart 1402'de şube:** **5.000 Venedik dukası = 5.225 Floransa florini** sermaye | ◐ | K58, K01 | 25 Mart = Floransa takviminde yılbaşı (K120; Giovanni'nin ölüm yılındaki 1428/1429 farkı da bunu gösteriyor, K55 çevresi) → tesadüf mü, muhasebe yılı başı mı, **yorum**. |
| 29 | c2 | 1402 | Bankada toplam ≈**17 çalışan**, Floransa merkezinde **5** | ○ | K01 | Wikipedia infobox'ında ≈40 yazıyor (dönem/kaynak belirsiz). |
| 30 | c2 | 1403 | Papalık *depositario* görevi esas olarak Spini, Alberti, Ricci'ye verilir (Curia'nın büyük alacaklıları) | ○ | K50 | |
| 31 | c2 | 1410–1415 | XXIII. Johannes (Baldassarre Cossa) döneminde Medici Roma müdürü "depositario generale" | ○ | K115, K48, K50 | **Çelişki:** Wikipedia "V. Martinus Giovanni'nin müdürünü Camera'nın başına getirdi (ödül)" der; DBI görevi 1422'den sayar. |
| 32 | c2 | 1414–1418 | Konstanz Konsili; Cossa 1415'te tahttan indirilir | HAFIZA | — | KAPSAM'da var; bu dosyada araçla doğrulanmadı. |
| 33 | c2 | 22 Ara 1419 | Cossa Floransa'da ölür | ○ | K79 | Mezar yazıtındaki "XI Kal. Ian." (HAFIZA) ile uyumlu. |
| 34 | c2 | 1420 | Giovanni bankanın yönetim çoğunluğunu **Cosimo ve Lorenzo**'ya bırakır ("1420'de çekildi"); Benedetto de' Bardi (1373–1420) aynı yıl ölür | ○ | K48, K52 | Bardi'nin ölümünün yeniden yapılanmayla ilişkisi **benim çıkarımım**. |
| 35 | c2/c3 | **1397–1420 kâr** | Dönem toplam kârı **152.820 florin** (≈**6.644/yıl**, 23 yıl); Giovanni'nin payı **%75** | ◐ (toplam) / ○ (%75) | K66, K60, K58, K116 | Portekizce kaynak "151.820" yazıyor (yazım farkı olabilir); 152.820/23=6.644 ve yıllık "6.644" diyen bir kaynakla tutarlı → 152.820 tercih. Hesap bana ait. |
| 36 | c2 | 1422–1428 | **Cossa'nın mezarı** (Donatello + Michelozzo), Floransa Vaftizhanesi; yazıt **"eski papa"** (*quondam papa*); V. Martinus itiraz eder | ◐ | K79, K80, K81 | Yorum: V. Martinus'a çelme ya da "Medici'nin kendini tanıtması" (Wikipedia). |
| 37 | c2 | 1425 | **Monte delle doti** (kamu çeyiz fonu) kurulur | ○ | K97 | c9'daki iddia için zemin. |
| 38 | c2 | 1426–1427 | Giovanni, **catasto** (mülk vergisi) için Signoria'da nüfuz kullanır (1426); catasto 1427'de yürürlükte | ◐ (yıl çelişkili) | K48, K102 | Giovanni'nin 1421 gonfaloniereliği doğrulanamadı. |
| 39 | c2 | 1427 | **Catasto:** Floransa ≈**38.000** kişi, **9.780** hane; en zengini **Palla Strozzi** (brüt **162.925 florin**); >10.000 florin değerinde **137 hane (%1,4)** toplam **3.000.672 florin = tüm kayıtlı servetin %29,8'i** | ◐ (nüfus, Strozzi) / ○ (%29,8) | K39, K40, K43, K44, K41 | **Giovanni'nin 1427 beyanı bulunamadı** (HAFIZA: "ikinci en zengin, net ≈79 bin"; **kullanma**) → bkz. §4B, §4E. |
| 40 | c2 | **20 Şub 1429** (Floransa takvimiyle 1428) | **Giovanni ölür** (≈69). Servet ≈**180.000 florin** ("Lorenzo'ya göre"); başka anlatımda **179.221** | ◐ (tarih) / ○ (servet) | K48, K49, K55, K102 | İki servet rakamı büyük olasılıkla aynı kökten; "Lorenzo'ya göre" ifadesindeki Lorenzo'nun kim olduğu (kardeş mi, torun mu) özetten anlaşılmıyor. |
| 41 | c3 | 1433 | **Cosimo tutuklanır, 10 yıl Padova'ya sürgün;** fiilen Venedik'te kalır (Michelozzo'nun kütüphane tasarımı Venedik sürgününe bağlanıyor) | ◐ | K103, K89, K85 | Zehirlenme korkusu rivayeti → ANEKDOT, bu dosyada doğrulanmadı. |
| 42 | c3 | 1434 | Cosimo alkışlarla döner ("rakip hizbin lideri sürülünce"); "tahtsız" iktidar başlar | ◐ | K103, K104 | |
| 43 | c3 | 1436 | **IV. Eugenius San Marco'yu** gevşek Silvestrinlerden alıp **Observant Dominiklere** verir; Cosimo yeniden inşayı üstlenir; "günahlarının kefareti ilan edildi" | ◐ | K83, K86, K105 | "Kefaret" vurgusu modern yorumcuya ait; Eugenius'un usuli üzerine açık bir öğüdü kayıtlı değil (özet). |
| 44 | c3/c4 | 1437 | Cosimo San Marco'yu yeniden inşa etmek için **10.000 florin** taahhüt eder | ○ | K105 | Tek kaynak. |
| 45 | c3 | 24 Mart 1439 | **Brugge şubesi resmen kurulur** (Flandre'de 1416'dan beri muhabir/ajan) | ○ | K01 | Wikipedia kökenli. |
| 46 | c3/c4 | 6 Oca 1443 | IV. Eugenius yeni San Marco kilisesini kutsamaya gelir; **Cosimo'nun hücresinde geceler** (Epifani) | ○ | K83 | |
| 47 | c3/c4 | 1445 başı | **Palazzo Medici** inşaat kampanyası başlar (komisyon ≈1444, Michelozzo); bitiş: 1460 (turizm sitesi) / 1484 (başka kaynak); tavan kerestesi 1449–51'de alınır | ◐ | K106, K117, K107 | **Maliyet bulunamadı.** |
| 48 | c3 | 1446 | **Gherardo (Gerard) Canigiani** Londra şubesinde işe girer; 1465'te müdür | ○ | K72 | |
| 49 | c3 | 1448–1459 | **Francesco Sassetti** Cenevre şubesi yöneticisi (HLS); Wikipedia: 1458'de Floransa'ya dönüş | ○ | K54, K71 | Çelişkili. |
| 50 | c3 | 1455 | III. Callistus Roma müdürü **Roberto Martelli**'yi *depositario*'luktan alır; aynı yıl papalık kayıtlarında **Piero ve Giovanni de' Medici** ve ortaklarından Camera'ya **6.000 florin** kredi | ○ | K115, K82 | İki ayrı kayıt; bağlantısı yok. |
| 51 | c3 | 1457–58 | Vergi beyanları: Cosimo **Venedik, Brugge, Londra, Milano, Avignon, Cenevre** şubelerinde ortak; bir Floransalı ortak 1457 beyanında Floransa bankasının sermayesinde **400 florinlik pay** gösterir | ○ | K90, K58 | Lyon bu listede yok (1466'dan). |
| 52 | c3 | **1435–1450 kâr** | Zirve dönem: toplam **290.791 florin**, **ortalama 19.386 florin/yıl** | ◐ | K91, K66 | 19.386×15=290.790 → iki kaynak tutarlı (hesap bana ait). |
| 53 | c3 | **1420–1435 kâr** | Dönem toplamı **186.382 florin** (≈**12.425/yıl**) | ○ | K66 | Hesap bana ait. **Okuma notu:** arXiv tablosu 152.820 / 186.382 / 290.791 değerlerini "1420 / 1435 / 1450" satırlarında veriyor; ben bunları **dönem toplamı** okudum, çünkü 290.791 = 15×19.386 (Spectator'ın yıllık ortalaması) ve 152.820 = 23×6.644 (başka bir kaynağın yıllık ortalaması) ile tutuyor. *Kümülatif* okuma (1420–35 için yalnız 33.562) bu iki bağımsız ortalamayla çelişir. |
| 54 | c3 | 1435–1441 | Kâr dağılımı (**imalat hariç**): **Roma %36,9, Venedik %28,9** | ○ | K115, K58, K01, K66 | Dönemler arası pay dalgalı → Roma payı: 1397–1420 **%52** (Floransa %17, Venedik %15; ○); 1420–1435 **%63** ya da 1420–1450 için **%62–63** (◐: dokumen.pub özetleri + Wikipedia'daki "%62 Roma, %13 Venedik" cümlesi; **dönem kaynaklarda net değil**). |
| 55 | c3 | 1461 | Tolfa'da şap keşfi (Giovanni da Castro) | HAFIZA | — | Bu dosyada araçla doğrulanamadı. |
| 56 | c3 | **1 Ağu 1464** | **Cosimo ölür** (74) | ◐ | K108, K109 | |
| 57 | c3/c9 | 1464'ten sonra (≈1465–68) | **Tommaso Portinari** Brugge'de genel müdür ve ortak olur ("40 yaşında"); Cosimo ona güvenmezmiş | ◐ | K93, K121 | Doğum 1428 (Met kaydı) ile "40 yaşında" birlikte okunursa ≈1468; kesin yıl **belirsiz**. |
| 58 | c3/c4 | **1466** | **Papalık şap şirketi:** Medici Tolfa madenlerinin işletmesi ve satışına ortak; Civitavecchia depolarından çıkan kantar başına Camera'ya **2 dukat**, ek kârın **2/3'ü Camera'ya** (başka anlatım: 1/3 Medici, 2/3 "Camera ve haçlı fonu") | ◐ | K110, K111, K59, K63 | **II. Paulus** dönemi (bir özet II. Pius dedi; Pius 1464'te öldü). Medici "bankanın zirve gücünü şap kontrolüne" bağlayan kaynak var (○). |
| 59 | c3/c9 | 1466 | **Cenevre şubesi Lyon'a taşınır** (Cenevre panayırlarının gerilemesi) | ○ | K54 | HLS: *"A la suite du déclin des foires de Genève, la filiale fut transférée à Lyon en 1466."* |
| 60 | c9 | 1466–1471 | Londra şubesinden **Edward IV**'e **£26.000'den fazla** kredi (bir kısmı geri ödendi); popüler anlatım: kralın borcu **£10.500** | ○ | K72, K59 | Rakamlar farklı ölçüler olabilir. |
| 61 | c9 | 1462–1472 | **Sassetti'nin "libro segreto"su** (gizli defter) | ○ | K71 | En bilinen gizli defter. |
| 62 | c9 | Haz 1470 | **Ischia** şap madenleri: Roma Medici bankası ile işletmeci arasında **25 yıllık anlaşma;** II. Paulus, Napoli Kralı Ferrante ve Medici onaylar | ○ | K110, K111 | "Kartel" yorumu. |
| 63 | c9 | 1471 | **Sassetti'nin etkisiyle** seküler yöneticilere kredi yasağı kalkar; **Portinari, Cesur Charles**'a büyük, **teminatsız** krediler verir; borç geri ödenmez, şube iflasa gider | ○ | K93, K94 | Portinari "iki efendiye hizmet" (Medici + dük danışmanı); kredilerin kapsamı tartışmalı (Cambridge). |
| 64 | c9 | 1469–1492 | **Lorenzo dönemi, Machiavelli'ye göre:** ticarette talihsiz, ajanları işleri "prens gibi" yönetir, özel servet büyük ölçüde erir; Lorenzo ticareti bırakıp **toprağa** (Prato, Pisa, Val di Pesa) yatırır | ○ (birincil çeviri, özetle) | K95 | Machiavelli'nin eserini Giulio de' Medici (VII. Clemens) ısmarladı (K32). Mugello alımı doğrulanamadı. |
| 65 | c9 | 1478 | Bruges'te Charles'a kredi "9.500 groat" (birim belirsiz) | ○ | K93 | **"Londra şubesi 1478'de kapandı" iddiası doğrulanamadı.** |
| 66 | c9 | 9 Mart 1490 | Sassetti ölür (Wikipedia; başka kaynak 1491) | ○ | K71 | |
| 67 | c9 | 9 Nis 1492–9 Kas 1494 | **Piero'nun yönetimi;** Charles VIII'e kaleleri teslim; Savonarola'nın etkisiyle Medici sürülür | ◐ | K98 | Tarih aralığı bir kaynakta açıkça var. |
| 68 | c9 | **Kasım 1494** | **Medici sarayı halk tarafından yağmalanır;** Piero Venedik'e kaçar (Philippe de Commynes'in yardımıyla) | ◐ | K98 | |
| 69 | c9 | **1494** | **Bankanın resmî sonu** (1397–1494) | ◐ | K01, K03, K58 | Kitap başlıkları ve Wikipedia aynı aralığı kullanıyor. |
| 70 | c9 | 1494–95 | Medici varlıklarına el konması, alacaklılar, defterlerin akıbeti | HAFIZA/eksik | — | **Arama sonuç vermedi.** |

### 2B. Tarihyazımı / kaynak kronolojisi

| # | Bölüm | Tarih | Olgu | Sınıf | Kaynak | Not |
|---:|---|---|---|---|---|---|
| 71 | c16 | 1327 / 1340 | Cenova komün hesapları "banka usulü": erken çifte kayıt biçimi ≈1327; **Massari hesapları 1340** en eski tam örnek | ◐ | K75, K76, K77 | |
| 72 | c16 | ≈1380 | Datini defterleri: "ilkel" dikey çifte kayıt | ○ | K76 | |
| 73 | c16 | 1407 | Venedik: Padova'dan alınan mülklerin defterleri | ○ | K76 | Venedik yönteminin Pacioli'den önce kullanıldığı tezi var. |
| 74 | c16 | 1429 / 1435 | Floransa'da **cambio secco (kuru kambiyo)** yasağı / kaldırılışı | ○ | K66 ya da K112 (özet hangisi olduğunu belirtmedi) | Tek özet. |
| 75 | c16 | 1458 | Benedetto Cotrugli'nin el kitabı (Pacioli'den önce) | ○ | K76, K77 | |
| 76 | c16 | 1494 (bazı kaynaklarda 1493) | **Pacioli, *Summa*** — ilk basılı muhasebe incelemesi | ◐ | K75, K78 | Pacioli *icat etmedi*, derledi. |
| 77 | c16 | 1499 | Kardinal **Cajetan**, *De Cambiis*: kambiyoda gizli faize eleştiri | ○ | K66, K112 | |
| 78 | c16 | 1938 / 1950 | de Roover Medici belgelerini fotoğraflar (1938) / "libri segreti 1950'de bulundu" (yayıncı metinleri) | ○ | K03 | İki yayıncı metni çelişkili. |
| 79 | c16 | 1944 | de Roover, *"What Is Dry Exchange?"* (JPE) | ○ | K66, K112 | |
| 80 | c16 | 1948; 1963 | de Roover, *The Medici Bank* (1948); *The Rise and Decline of the Medici Bank, 1397–1494* (Harvard UP, 1963) | ◐ | K03, K58, K02 | Bir listeleme 1966 baskısını gösteriyor. |
| 81 | c16 | 1957 | George Brucker, *The Medici in the Fourteenth Century* (14. yy Medici için standart) | ○ | K114 | |
| 82 | c16 | 1985 (Fr. 1978) | Herlihy–Klapisch-Zuber, *Tuscans and Their Families* (Yale) | ◐ | K39, K40 | |
| 83 | c16 | 2005 | Tim Parks, *Medici Money: Banking, Metaphysics, and Art in Fifteenth-Century Florence* | ◐ | K92 | Ayrıca dokumen.pub'da Türkçe bir *Medici Ailesi – Rönesans Çağı'nda Bankacılık, Siyaset ve Sanat* kitabı var (K60); Parks'ın Türkçesi mi, başka kitap mı **doğrulanamadı** — Türk izleyiciye okunacak kaynak olarak kontrol edilmeli. |
| 84 | c16 | 2006 | Eckstein, "Addressing Wealth in Renaissance Florence" (catasto) | ○ | K41 | |
| 85 | c16 | yıl doğrulanamadı | Barone & Mocetti: 1427'nin en zengin Floransa aileleri ≈600 yıl sonra yine en zengin | ◐ | K45, K46 | Yıl: "Florence 1427–2011". |
| 86 | c16 | 2025 (Temmuz) | Ridolfi–Vasta, Siena WP 928: Duomo işçilerinin reel ücretleri 1326–1861 (>20.000 gözlem) | ○ | K99 | **Ücret verisi için en iyi kapı.** |


---

## 3. Canlı ayrıntılar

> Sütunlar: `# | Bölüm | Ayrıntı | Kim yazdı / ne zaman (olaydan sonra mı?) | Güvenilirlik | Birebir alıntı (orijinal dil + Türkçe çeviri; çeviri bize aittir)`.
> **Uyarı:** Tırnak içindeki metinler arama özetinde *tırnaklı* göründüğü kadarıyla verildi (çoğu İngilizce çeviri/ikincil aktarım); orijinal İtalyanca/Latince sayfa açılıp **kontrol edilemedi**. Satırın "Birebir alıntı" hücresinde "—" varsa, doğrulanmış birebir cümle yok demektir. Her bölümde ≥5 satır var; kaynak kalitesi satır satır işaretli.

### 3.1 c1 — Florin Şehri (1252–1397)

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| D01 | c1 | **Dante florine lanet okur.** Cennet IX'da Marsilyalı Folco, florini "lanetli çiçek" diye anar: çobanı kurda çevirip koyunları ve kuzuları yoldan çıkaran şey. Florin burada hem zenginliğin hem ahlaki çürümenin simgesi. | Dante, *Paradiso* IX (sürgün yıllarında, ≈1310'ların sonu–1321; yıl HAFIZA). Florin'den ≈60–70 yıl sonra; yorum, belge değil | Edebi/ahlaki yorum; ifade ve imge ◐ (3 ayrı özet: K113) | "maladetto fiore" (It.; ifade arama özetinde doğrulandı) → "lanetli çiçek". Tam terzina **HAFIZA, kontrol et:** "…produce e spande il maladetto fiore / c'ha disviate le pecore e li agni, / però che fatto ha lupo del pastore." → "…lanetli çiçeği üretir ve yayar; çobanı kurda çevirdiği için koyunları ve kuzuları yoldan çıkarmış olan çiçeği." |
| D02 | c1 | **Villani kenti sayar (1338).** Okuma öğrenen 8–10 bin çocuk, abaküs/algoritma öğrenen 1.000–1.200 (6 okul), gramer-mantık öğrenen 550–600 (4 büyük okul); nüfus ≈90.000. Villani eskiden darphane yöneticisiydi ve geçmiş sikke kayıtlarını topladı. | Giovanni Villani, *Nuova Cronica* (1338 tablosu; çağdaş betimleme, ama rakamlar kendi tahmini) | ◐; rakamlar sorgulanıyor ama 1427 catasto okuryazarlık tablosuyla uyumlu bulunuyor (bir kaynak), "açık soru" diyen de var | — (rakamlar; birebir cümle doğrulanmadı) |
| D03 | c1 | **Boccaccio'nun veba girişi.** Salgın "İtalya'nın en güzel şehri" Floransa'ya gelir; sağlıklılar hastadan kaçar, hasta yalnız ölür; cesetler evlerde ve sokaklarda yığılır; hasta bakıcıları abartılı ücret ister, kendileri de ölür; Mart–Temmuz arası surlar içinde **100.000'den fazla** ölü iddiası. | Boccaccio, *Decameron*, 1. Gün girişi (≈1349–53; olaydan 1–5 yıl sonra; öncül veba anlatılarından yararlanmış olabilir: K23) | Olay ◐; 100.000 rakamı abartılı/retorik olabilir → ○ | EN (K21): "In the year then of our Lord 1348, there happened at Florence, the finest city in all Italy, a most terrible plague…" → "Rabbimizin 1348. yılında, İtalya'nın en güzel şehri Floransa'da çok korkunç bir veba baş gösterdi…". İtalyanca açılış **HAFIZA (kontrol et):** "…quando nella egregia città di Fiorenza, oltre a ogn'altra italica bellissima, pervenne la mortifera pestilenza." |
| D04 | c1 | **Stefani'nin veba çukurları.** Ölüler toplu çukurlara konur, katman katman toprakla örtülür. Stefani 1336 doğumlu → 1348'de 12 yaşında; kroniği 1370'ler sonu–1380'lerde yazdı. | Marchionne di Coppo Stefani, *Cronaca fiorentina* (olaydan ≈30 yıl sonra; çocukluk anısı + derleme) | ◐ (K24, K25, K26) | — (History Today özetinden "katman katman toprak"; birebir cümle yok) |
| D05 | c1 | **1348 kararnamesi:** birçok yurttaşın birden yoksullaştığı, yoksulların zenginleştiği kabul edilir; kentte ücretler yükselir, kırda bastırılır → reel ücretler kırda düşer. Bir tarihçi, İtalya'da işçi kazançlarının "iki üç kuşak sonra" geldiğini savunur. | Kararname (devlet belgesi) → modern ekonomi tarihi özetleri (K18, K20); belge görülmedi | ○ | — |
| D06 | c1 | **22 Temmuz 1378:** Palazzo Vecchio'yu işçiler alır; bir **yün tarayıcısı** (Michele di Lando) gonfaloniere olur; gonfaloniere **Salvestro de' Medici** (Medici soyundan) istifaya zorlanır. | Wikipedia, The Florentine (2025), Hanover tezi (modern) | ◐ | — |
| D07 | c1 | **Machiavelli, Ciompi'ye uydurma bir konuşma yazdırır** (Istorie fiorentine III.13): isimsiz bir ayaklanma önderi konuşur. Olaydan ≈145 yıl sonra, Medici'nin (Giulio, sonra VII. Clemens) ısmarladığı bir tarihte. **Belgesel değil, kurgu.** | Machiavelli, ≈1520–25; Yves Winter vb. akademik okuma (K31, K32) | ◐ (uydurma oluşu) | — (konuşma metni doğrulanmadı) |
| D08 | c1 | **Kronikçinin çıkarı:** Villani'nin kardeşi Peruzzi şirketindeydi ve şirket battı → Edward III borcu rakamları taraflı olabilir. | Modern tarih yazımı (K11–K13) | ◐ | — |
| D09 | c1 | **Giovanni'nin çıplak başlangıcı.** Medici hatları 14. yy'da seçkinlerin altındaydı, kır gelirleriyle yaşardı; Giovanni babasının mütevazı mirasının **beşte birini** aldı; ortaklığa karısının çeyiziyle (1.500 florin) girdi. | Treccani DBI, P. Terenzi (K50) + K49/K51 | ◐ | Firma adı (It., DBI özetinden): "Giovanni de' Medici e compagni in Roma" → "Giovanni de' Medici ve ortakları, Roma". |
| D10 | c1/c2 | **1397 köşesi.** Roma'dan taşınan küçük işletme; merkez Orsanmichele semtinde, Via Porta Rossa–Via Calimala kavşağı. | Palazzo Medici Riccardi mediateca + Italy On This Day | ◐ | EN (K49): "…establishing a headquarters at the crossroads between Via Porta Rossa and Via Calimala in an area of the city called Orsanmichele." → "…Via Porta Rossa ile Via Calimala'nın kesiştiği, Orsanmichele denen semtte bir merkez kurarak…" |

### 3.2 c2 — Defterin Sihri (1397–1429)

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| D11 | c2 | **Giovanni'nin ölüm yatağı (Machiavelli sürümü).** Hastalanır, sonunu görünce Cosimo ve Lorenzo'yu çağırır; onları zengin, sağlıklı ve itibarlı bıraktığı için huzurla gittiğini; onun yolundan giderlerse Floransa'da saygın yaşayacaklarını; devlet işlerinde **yasaların ve yurttaşların uygun gördüğü kadar pay** almalarını; kıskançlığın kişinin kendisine *verilenden* değil, *istediğinden* doğduğunu söyler. | Machiavelli, *Istorie fiorentine* IV (≈1520–25; olaydan ≈95 yıl sonra; Medici siparişi) | **ANEKDOT**; ◐ (K55, K57, K32 özetleri uyumlu) ama kelime kelime kontrol edilmedi | EN (Thomson çevirisi, K55): "About this time Giovanni de' Medici was taken ill, and finding his end approach, called his sons Cosmo and Lorenzo to him, to give them his last advice." → "Bu sıralarda Giovanni de' Medici hastalandı ve sonunun yaklaştığını görünce, son öğütlerini vermek için oğulları Cosmo ile Lorenzo'yu yanına çağırdı." (Konuşmanın devamı **doğrulanmadı**.) |
| D12 | c2 | **Cavalcanti sürümü:** ölüm yatağı konuşması aile önünde ve daha dindar bir tonda — "dünyevi tasaları sonsuz huzurla değiş tokuş etmek"te yas yok. (Özet, konuşmanın tam olarak Giovanni'ye ait olup olmadığını açıkça vermiyor → **doğrulanamadı**.) | Giovanni Cavalcanti, *Istorie fiorentine* (1440'lar; Machiavelli'den eski; **HAFIZA:** Medici karşıtı bir yazar olarak bilinir). İngilizcesi: Janet Ross, *Lives of the Early Medici* (1910; HAFIZA: yazar) | **ANEKDOT**; ○ | EN (K56): "Beloved sons, neither I nor any man born into this world should feel grief at exchanging worldly cares for perpetual repose." → "Sevgili oğullarım, ne ben ne de bu dünyaya doğmuş herhangi bir insan, dünyevi tasaları sonsuz huzurla değiş tokuş ettiği için kederlenmemeli." (It. orijinal kontrol edilmedi) |
| D13 | c2 | **"Dikkat çekme" öğüdü modern bir özet.** Modern kitaplar Giovanni'nin öğüdünü "gösterişli olma, başkalarının üstüne çıkmaya çalışma" diye özetler; Parks incelemesi "kamu gözünden uzak dur" der. Bu, Machiavelli'nin metni *değil*; **parafraz**. | *A Short History of Renaissance Italy* (K61); Parks incelemesi (Literary Review, K125) | **ANEKDOT / modern gloss**; ○ | EN (K61, kaynağın kendi tırnağı): "Be careful not to draw attention to yourself" → "Dikkat çekmemeye bak." (Aslı belirtilmemiş.) |
| D14 | c2 | **Machiavelli'nin Giovanni portresi:** yoksulların ihtiyacını *istenmeden* gideren; ölünce herkesçe yası tutulan adam. | Machiavelli IV (aynı) | ◐ (özetler uyumlu); sevgi dolu dil, Medici siparişli tarihin tonu | EN (K55): "…not only bestowing alms on those who asked them, but very frequently relieving the necessities of the poor, without having been solicited so to do." → "…isteyenlere sadaka vermekle kalmaz, yoksulların ihtiyaçlarını, kendisinden istenmeden de sık sık giderirdi." |
| D15 | c2 | **Cossa'nın mezarında "eski papa".** Vaftizhane'deki mezar (Donatello + Michelozzo, 1422–28) Cossa'yı *"eski papa"* diye anar; V. Martinus itiraz etse de yazıt kalır. Yorum: V. Martinus'a çelme ya da "Medici'nin kendini tanıtması". | Opera di S. Maria del Fiore sitesi (K80); Wikipedia (K79) | ◐ | EN (K79): "John the former pope" → "Eski papa Johannes". Latince **HAFIZA, kontrol et:** "IOANNES QUONDAM PAPA XXIII". |
| D16 | c2 | **Kefalet/fidye:** Duomo müzesi sitesi, Cossa'nın Giovanni "Bicci" tarafından **kefaletle** çıkarıldığını ve oğlu Cosimo'nun onu Floransa'ya davet ettiğini yazar; başka bir kaynak "Medici'nin ödediği büyük fidye" der. **Tutar bulunamadı** (HAFIZA'mda 38.000 florin; doğrulanamadı). | Opera del Duomo sitesi (K80); Wikipedia | ◐ (olay) / ○ (tutar yok) | EN (K80): "released on bail by Giovanni 'Bicci' of the Medici, he was then invited by his son, Cosimo, to move to Florence" → "Giovanni 'Bicci' de' Medici'nin kefaletiyle serbest bırakılan Cossa'yı, oğlu Cosimo Floransa'ya yerleşmeye davet etti." |
| D17 | c2 | **Giovanni ile Cossa Roma'da 1390'lardan tanışır.** DBI, Cossa'nın Curia'nın alacaklıları arasında Medici'ye Camera'dan yüksek faiz verdirdiğini **düşmanların iddiası** olarak aktarır. | DBI (Terenzi, K50) | ○ (DBI "iddia" diyor) | — |
| D18 | c2 | **Venedik şubesi Floransa yılbaşında doğar:** 25 Mart 1402; sermaye 5.000 Venedik dukası = 5.225 florin. (25 Mart'ın Floransa takvimindeki yılbaşı olması: bir ders notu özetinden [K120] ve Giovanni'nin ölüm yılındaki 1428/1429 farkını açıklayan özetten [K55 çevresi] çıkıyor; şubenin bu güne denk getirilmesi **yorum**, kasıtlı olup olmadığı bilinmiyor.) | de Roover'dan aktarım (K58, Wikipedia K01) | ◐ | EN (K58): "On March 25, 1402, a real branch was created and a capital of 5,000 ducats, Venetian currency, or 5,225 florins, Florentine currency, was assigned to it." → "25 Mart 1402'de gerçek bir şube kuruldu; ona 5.000 Venedik dukası, yani 5.225 Floransa florini sermaye ayrıldı." |
| D19 | c2 | **Başlangıçta banka ufacık:** 1402'de toplam ≈17 çalışan, Floransa merkezinde 5; Roma şubesi sermayesiz çalışıyor, çünkü Kilise para yatırıyor, borç almıyor. | Wikipedia (K01); de Roover aktarımı (K58) | ○ | EN (K58): "…no corpo (capital) was assigned to the Rome branch" → "Roma şubesine hiç sermaye (corpo) ayrılmadı." |
| D20 | c2 | **"Bankanın sahibi Giovanni'ydi":** 1397–1420 kârı 152.820 florin (≈6.644/yıl); kârın %75'i Giovanni'ye (tek kaynak). | de Roover'dan türetilmiş tablolar (K66, K60, K58) | ◐ (toplam) / ○ (%75) | — |

### 3.3 c3 — Kule ve Sürgün (1433–1464) · para yönü

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| D21 | c3 | **Cosimo müdürleri mülakatla seçer** ve kâra ortak eder; ortaklık sözleşmesi şube müdürünün çıkarını bankanın çıkarına bağlar. | BYU lisans tezi (K90) | ○ | — |
| D22 | c3 | **Kâr payı sermaye payından büyük:** müdürler çoğunlukla eş-sahip; yönetim sözleşmeleri **beş yıla kadar**; ana ortaklar istediğinde bitirebilir. | K59 (de Roover'a dayanır) | ◐ (K59 + K01/K02 yapı anlatımı) | EN (K59): "It was quite common that the branch managers had a share in profits (and losses) that was substantially larger than their ownership share." → "Şube müdürlerinin kâr (ve zarar) payının, sermaye payından hayli büyük olması oldukça yaygındı." |
| D23 | c3 | **"Holding" mi, "doğrudan ortaklıklar" mı?** Bir kitap, ana şirket katmanının *ortadan kalktığını* söyler; başka makale "holding"in şubelerin %50'sinden fazlasına sahip olduğunu. İki anlatım yan yana. | K59 vs K53 | Çelişki; ◐ | EN (K59): "The Medici family went directly into partnership with each of the branch managers; thus the intermediate layer of a parent company was eliminated." → "Medici ailesi her şube müdürüyle doğrudan ortaklığa girdi; böylece ara katman olan ana şirket ortadan kalktı." |
| D24 | c3 | **Sözleşmelerin dili:** Medici ile şube müdürleri arasındaki sözleşmeler işi "dürüst ve meşru" kambiyo olarak adlandırır. | Hidden Florence / Brewminate özeti (K85, K86; Parks'a dayanıyor olabilir) | ○ | EN (özet): "honest and licit" → "dürüst ve meşru". **Orijinal sözleşme metni görülmedi.** |
| D25 | c3 | **Cosimo'nun "defter" şakası:** Tanrı'ya ne verirse versin Tanrı'yı "defterlerine borçlu yazamadığını" söylemiş. | Kaynak belirsiz (Vespasiano geleneği olabilir — HAFIZA) | **ANEKDOT**; ○ | — ("…diye aktarılır"; birebir cümle doğrulanamadı) |
| D26 | c3 | **Vespasiano'nun gözlemi:** Cosimo'nun vicdanında "epey şey birikmişti". | Vespasiano da Bisticci, *Vite* (Cosimo'nun kitapçısı; olaydan sonra) — erişim K84/K85/K86 çevresindeki modern aktarımlar | **ANEKDOT/yorum**; ◐ (birden fazla özet aynı modern çeviriyi aktarıyor) | EN: "accumulated quite a bit on his conscience, as most men do who govern states and want to be ahead of the rest" → "vicdanında hayli şey biriktirmişti; devlet yönetip başkalarının önüne geçmek isteyen çoğu adamın başına geldiği gibi." (İtalyanca aslı **kontrol edilmedi**.) |
| D27 | c3 | **Modern yorumcunun retoriği:** Cosimo "tefeciliğe boğazına kadar batmış, vergisini kıvırmış (yine de şehrin en büyük vergi ödeyicisi), muhaliflerini işkence ve sürgüne göndermekten çekinmemiş" biri. Kaynaklı bilgi değil, **inceleme dili**. | NYRB "The Cosimos" (K84) ya da Brewminate (K86) — özet ayrımı yapmadı | ○ | EN: "…fiddled his taxes (though he was still the city's biggest taxpayer)…" → "…vergisini kıvırdı (yine de şehrin en büyük vergi ödeyicisiydi)…" |
| D28 | c3 | **Spectator'ın okuması:** Medici zenginliği ticaretten çok, bugün "kur arbitrajı" denen işten gelir. Aynı yazı Sforza'nın "55.000 florin"le sıkıştırılmasından söz eder (yönü ve bağlamı belirsiz). | Spectator (Mark Archer; yıl doğrulanamadı) | ○ | — |
| D29 | c3 | **1455:** III. Callistus Roma müdürü Roberto Martelli'yi *depositario*'luktan alır; aynı yıl Camera'ya Medici'ler ve ortaklarından 6.000 florin kredi kaydı. | Vatican Regesta 438 (BHO, K82); dokumen kopyası (K115) | ○ | — |
| D30 | c3 | **Cenevre panayırları söner, şube Lyon'a gider (1466).** | HLS | ○ | FR (K54): "A la suite du déclin des foires de Genève, la filiale fut transférée à Lyon en 1466." → "Cenevre panayırlarının gerilemesi üzerine şube 1466'da Lyon'a taşındı." |

### 3.4 c4 — Kubbe ve Kefaret (1418–1460'lar) · para yönü

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| D31 | c4 | **1436 San Marco takası:** IV. Eugenius gevşek Silvestrinleri çıkarır, Observant Dominikleri yerleştirir; Cosimo yeniden inşayı üstlenir; modern yazara göre papa "günahlarının kefaretini ilan etti". | Wikipedia (K83) + Brewminate (K86), modern | ◐ | EN (K86): "Cosimo agreed to rebuild San Marco as part of the transfer deal, and Eugenius proclaimed the expiation of his sins." → "Cosimo, devir anlaşmasının parçası olarak San Marco'yu yeniden inşa etmeyi kabul etti; Eugenius da günahlarının kefaretini ilan etti." (Modern yazar; papanın sözü değil.) |
| D32 | c4 | **Papa Cosimo'nun hücresinde:** Epifani 1443 gecesi (6 Ocak) kiliseyi kutsamaya gelen papa, Cosimo'nun hücresinde uyur. | Wikipedia "Cosimo de' Medici's cell" (K83) | ○ | EN (K83): "Pope Eugenius IV slept in the cell the night of Epiphany 1443 when he came to consecrate the new church." → "Papa IV. Eugenius, yeni kiliseyi kutsamaya geldiği 1443 Epifani gecesi bu hücrede uyudu." |
| D33 | c4 | **10.000 florin taahhüdü (1437).** | Tek müze/turizm sitesi (K105) | ○ | — |
| D34 | c4 | **Harvard öğrenci sergisi:** bankerler tefecilik için "iade/telafi" olarak dini sanat ısmarlamış olabilir mi — ve olduysa neden *sanat*? Kanıt değil, **tez**. | Harvard Omeka sergisi (K88) | ○ | — |
| D35 | c4 | **Parks'ın çerçevesi:** Kilise her türlü faizi yasaklıyor; ayrıca küçük bir cumhuriyette bankerin servetinin vergilendirilmemesi nasıl sağlanır? | Parks'ın tanıtım/inceleme metinleri (K92) | ◐ (birden fazla tanıtım metni) | EN: "Charging interest of any kind ran afoul of the Catholic Church's ban on usury, even at the height of the Renaissance." → "Her türlü faiz almak, Rönesans'ın zirvesinde bile Katolik Kilisesi'nin tefecilik yasağına aykırıydı." |
| D36 | c4 | **"600 bin florin" iddiası:** Wikipedia, Cosimo'nun sanat ve kültüre 600.000'den fazla altın florin harcadığını (≈500 milyon dolar) yazar; rakamın ne ölçtüğü belirsiz. (**DÜZELTME #4**: hafızamdaki 663.755 rakamı "bina, sadaka, vergi" kalemleri içerir; doğrulanamadı.) | Wikipedia (K89) + kopyası (Online Books Page) | ○ (tek kök) | EN (K89): "He spent over 600,000 gold florins (approx. $500 million inflation adjusted) on art and culture…" → "Sanat ve kültüre 600.000'den fazla altın florin (enflasyona göre ≈500 milyon dolar) harcadı…" |
| D37 | c4 | **Palazzo Medici şantiyesi:** inşaat 1445 başında başlar; bir Mart 1445 mektubu arsanın boşaltılmasını anlatır; tavanlar için kereste 1449–51'de alınır; bitiş yılı 1460 ya da 1484 (kaynaklar farklı). **Maliyet bulunamadı.** | UniFi (Ferretti) ve fupress makaleleri (K106, K117), turizm sitesi (K107) | ◐ | — |
| D38 | c4 | **Kubbe parası (HAFIZA):** Brunelleschi'nin kubbesi Opera del Duomo/Lana loncası hesabından ödendi, Medici'nin değil; "Medici kubbeyi finanse etti" demek yanlış olur. Opera'nın işçi ve usta ücret kayıtları (ör. 26 Mart 1425 girişi) MPIWG'nin "Duomo" belge veritabanında arama sonuçlarında göründü. | HAFIZA; MPIWG "Duomo" veritabanı sonuç sayfaları (K122) | HAFIZA/○ | — |

### 3.5 c9 — Defter Kapanıyor (1470–1494)

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| D39 | c9 | **Machiavelli'nin hükmü:** Lorenzo ticarette talihsizdi; ajanları işleri "prens gibi" yürüttü; servetin büyük kısmı eridi; Lorenzo ticareti bırakıp **toprağa** (Prato, Pisa, Val di Pesa) yöneldi. | Machiavelli, *Istorie fiorentine* VIII (≈1520–25; Medici siparişli) — Fordham çevirisi (K95) | ○ (birincil çeviri, özetle; açılıp okunmadı) | — (özet kendisi parafraz yaptı; "Mugello" alımı doğrulanamadı) |
| D40 | c9 | **Portinari'nin yükselişi:** yıllarca yardımcı/faktör; Cosimo ona güvenmezmiş; Cosimo ölünce Brugge'de genel müdür ve ortak (≈40 yaşında). | Wikipedia (K93) + Cambridge bölümü (K94) | ◐ | — |
| D41 | c9 | **1471 kararı:** Sassetti'nin etkisiyle seküler yöneticilere kredi yasağı kalkar; Portinari Cesur Charles'a büyük, teminatsız krediler verir; geri ödenmez, Brugge şubesi çöker. | Wikipedia (K93) | ○ | — |
| D42 | c9 | **İki efendi:** Portinari hem Medici'nin Brugge müdürü hem dükün danışmanı; kredi ilişkisinin kapsamı tartışmalı. | Cambridge, *Charles the Bold in Italy* bölümü (K94) | ○ | — |
| D43 | c9 | **Portinari'nin yüzü:** Hans Memling'in Tommaso (d. 1428) ve eşi Maria Baroncelli (d. 1456) portreleri (Metropolitan Museum) — Brugge'deki Floransalı bankerin görsel kaydı. (Hugo van der Goes'in Portinari Sunağı için **HAFIZA**: Brugge'den Floransa'ya gönderildi; doğrulanmadı.) | Met Müzesi kaydı, Smarthistory ve sanat siteleri (K121) | ◐ | — |
| D44 | c9 | **Londra:** Canigiani'nin Edward IV'e kredileri (1466–71, >£26.000; bir kısmı geri ödendi); Medici ile bağı kopunca İngiliz bir kadınla evlenir ve "denization" (yabancıdan yurttaşa yakın statü) mektubu alır. | Cambridge, "Lorenzo de' Medici's London branch" (K72) | ○ | — |
| D45 | c9 | **Sassetti:** Avignon ve Cenevre'de yükselen, ailenin dışından en üst mevkie ulaşan yönetici; 1462–72 gizli defteri; Lyon'da Lorenzo'nun ajanı olarak anılır; 1490 ya da 1491'de ölür. | Wikipedia (K71); HLS (K54) | ◐ | — |
| D46 | c9 | **Çeyiz fonu iddiası:** Lorenzo'nun kamu çeyiz fonundan "kişisel harcamalar için çektiği" ve bunun yıllarca gizli kaldığı söylenir. Tek ve popüler kaynak; **kullanma**. | Market Histories (K96) | ○ (zayıf) | — |
| D47 | c9 | **1494'ün sonu:** Piero kaleleri Charles VIII'e teslim eder; halk Medici sarayını yağmalar; Piero Venedik'e Philippe de Commynes'in yardımıyla kaçar. | Wikipedia (K98), Britannica, encyclopedia.com | ◐ | — |

### 3.6 c16 — Hesap (1737–bugün) · miras tartışması

| # | Bölüm | Ayrıntı | Kim yazdı / ne zaman | Güvenilirlik | Birebir alıntı |
|---|---|---|---|---|---|
| D48 | c16 | **Aynı aileler, 600 yıl sonra:** Floransa'nın 1427'deki en zengin aileleri günümüzde de en zengin dilimde (Barone–Mocetti). "Miras" kapanışı için ironik malzeme. | EUI çalışma kâğıdı, Tribune haberi | ◐ | — |
| D49 | c16 | **"Holding"in atası mı?** Wikipedia: Bardi ve Peruzzi tüm şubeleri tek ortaklık altında toplarken Medici ayrı ortaklıklar kurdu. Bir İtalyan yazar bunu "daha gevşek" diye niteler. | Wikipedia (K01), Linkiesta (K02) | ◐ | — |
| D50 | c16 | **Arşivde duran defterler:** *Mediceo avanti il Principato* (Floransa Devlet Arşivi) Londra şubesine dair çok belge içerir ve de Roover bunların hepsini kullanmadı; Medici–Tornaquinci fonu Harvard Baker Library'dedir. | Cambridge bölümü (K72), Linkiesta (K02) | ◐ | — |
| D51 | c16 | **Banka başarısızlıkları vakası:** *A Comparative History of Bank Failures: From Medici to Barings* (Routledge, 2019) Medici'yi bu tarihin başına koyar. | Kitap listesi (K59) | ○ | — |
| D52 | c16 | **Spectator'ın özeti:** zenginlik kur arbitrajından. | Spectator (K91) | ○ | — |
| D53 | c16 | **Parks'a eleştiri notu:** *The Economist*, Parks'ın bankacılara şüpheyle baktığını ve hızlı, esprili, biraz tutkulu yazdığını söyler. | Yayıncı/inceleme derlemesi (K92) | ○ | — |
| D54 | c16 | **Rönesans'ın "faturası":** "Cosimo sanata 600 bin florin harcadı" cümlesinin rakamı ve kapsamı sorunlu (D36, DÜZELTME #4). | Wikipedia (K89) | ○ | — |

---

## 4. Sayılar ve ölçüler

> Çelişki olan yerde **her değer** yazıldı. "Hesap" = bana ait türetme. "Günümüz parasıyla" iddiaları **○** sayıldı.

### 4A. Para birimi ve muhasebe

| Ölçü | Değer(ler) | Sınıf | Kaynak | Not |
|---|---|---|---|---|
| Florin ağırlığı | **3,53 g** (.986 saf) · **3,49 g**, çap **19,9 mm** (Wikipedia) · "24 ayar" nominal | ◐ | K04, K05, K06 | Ağırlık farkı ölçüm/dönem kaynaklı olabilir. |
| Standart süresi | **1252–1533** (≈280 yıl) değişmez tasarım ve metal standardı | ◐ | K04, K05 | 1533 tek özette. |
| Başlangıç paritesi | 1 florin = **1 lira = 20 soldi = 240 denari** (1252); 1252 Pisa kaydında 20 soldi | ◐ | K101, K100 | Başka bir forum: "1 altın florin=20 gümüş florin" (güvenilmez). |
| 1324–25 | **66–67 soldi** (≈3,3 lira) | ○ | K100 | |
| "Lira a fiorino" | 20/29 florin; yani **1 florin = 29 soldi = 348 denari** (muhasebe birimi) | ○ | K100 | Sabit ücret/borç hesaplarında kullanılan kur. |
| 1500 | **1 florin = 7 Floransa lirası** | ○ | K101 | |
| Fiorino largo | 1430'lar–1470'ler, ≈3,4–3,5 g | ○ | K100 (Numista) | |
| Villani'nin ima ettiği kur (hesap) | 900.000 fl = £135.000 → £1 = **6⅔ florin** (1 florin = 36 peni = 3 şilin) | hesap | K11, K12 | İki çift de aynı oranı veriyor (600.000/£90.000). |
| Venedik/Floransa (1402, hesap) | 5.000 dukat = 5.225 fl → **1 dukat ≈ 1,045 florin** | hesap | K58 | |
| "Günümüz parası" | florin ≈ **€800–1.500** (Wikipedia'nın bir sürümü); 600.000 florin ≈ **$500 milyon** (≈$833/florin) | ○ | K04, K89 | Kullanılacaksa "bir tahmine göre" denmeli. |

### 4B. Nüfus ve servet

| Ölçü | Değer(ler) | Sınıf | Kaynak | Not |
|---|---|---|---|---|
| Floransa nüfusu | **1338: ≈90.000** (Villani) · "1300 dolayında ≈120.000" (muhtemelen) · **1427: ≈38.000** (9.780 hane) · 15. yy boyunca **≈40.000** | ◐ (1338, 1427) / ○ (120.000) | K33, K34, K39, K40, K19 | 1338→1427: yaklaşık **−%58** (hesap). |
| Toskana | veba sıralarında ≈1 milyon; ≈1440'ta ≈400.000 | ○ | K19 | |
| Veba ölüm oranı (Floransa) | Boccaccio: **>100.000** · "yarıdan fazla" · "üçte iki" (eski görüş) · "dörtte üç" | çelişkili | K17, K21, K22 | Tek sayı verme; aralık ve kaynak kimliği ver. |
| 1427 dağılım | **137 hane (%1,4)** >10.000 fl; toplam **3.000.672 fl = kayıtlı servetin %29,8'i** | ○ | K41 | Ortalama ≈**21.900 fl/hane**, kayıtlı toplam ≈**10,07 milyon fl** (hesap). |
| Palla Strozzi | brüt **162.925 fl** (Wikipedia, "1427'de en zengin") | ◐ ("en zengin") / ○ (rakam) | K43, K44 | **HAFIZA:** net ≈101 bin; aynı listede Giovanni di Bicci ikinci, net ≈79 bin — **araçla doğrulanamadı, kullanma.** |
| Giovanni'nin ölümdeki serveti | **≈180.000 fl** ("Lorenzo'ya göre") · **179.221 fl** (başka anlatım) | ○ | K48, K102 | Büyük olasılıkla aynı kök. |
| Medici "varlık zirvesi" | 123.000 fl (bir forum yanıtında) | ○ (güvenilmez) | — | Kullanma. |

### 4C. Banka büyüklüğü ve kâr

| Ölçü | Değer(ler) | Sınıf | Kaynak | Not |
|---|---|---|---|---|
| Kuruluş sermayesi (1397) | **10.000 fl**; Giovanni **5.000** (Wikipedia/makale) ya da **5.500** (Türkçe kitap); öteki ortaklar Benedetto de' Bardi + bir ortak | ◐ (toplam) / ○ (paylar) | K01, K53, K60 | Portekizce kaynak: 1402'de ≈20.000 fl (○, K116). |
| Venedik şubesi (1402) | **5.000 dukat = 5.225 fl** | ◐ | K58, K01 | |
| Personel | **1402: ≈17** (Floransa 5) · infobox'ta ≈40 (dönem belirsiz) | ○ | K01 | |
| Kıyas: Peruzzi | **15 şube, >100.000 fl, ≈100 faktör** (1330'lar) | ○ | K12 | |
| Dönem kârı | **1397–1420: 152.820** (≈6.644/yıl) · **1420–1435: 186.382** (≈12.425/yıl) · **1435–1450: 290.791** (≈19.386/yıl) · toplam **1397–1450 ≈ 629.993** (hesap) | ◐ (ilk ve son) / ○ (orta) | K66, K91, K60, K58 | Yıllık ortalamalar hesap; "151.820" yazımı bir Portekizce kaynaktan (K116). **Dönem toplamı mı, kümülatif mi?** — okuma gerekçesi kronoloji #53 notunda. |
| Roma payı | **1397–1420: %52** · **1420–1435 (ya da 1420–50): %62–63** · 1435–41 (imalat hariç): **%36,9** | ◐/○ | K115, K58, K01, K66 | Venedik: %15 (1397–1420); %13 (Wikipedia'daki cümle); %28,9 (1435–41). **Kalem ve dönem karışıklığı var**, senaryoda "yarıdan fazlası Roma'dan" demek yeter. |
| Giovanni'nin payı | 1397–1420 kârın **%75'i** | ○ | K58/K115 | |
| Ortak sermaye payı örneği | 1457 beyanında bir ortak: Floransa bankasında **400 fl** | ○ | K58 | |
| Medici'nin şube sermayesindeki payı | **≥%50** (popüler site) / "çoğunlukla %50'den fazla" (akademik makale) | ○ | K53, K119 | Şubeye göre değişir. |
| Zirvede şube sayısı | Roma, Venedik, Milano, Pisa, Avignon, Brugge, Londra, Cenevre (+ Lyon 1466'dan) | ◐ | K65, K90, K54 | Yıllar: §5D. |

### 4D. Şap (alum) ve krediler

| Ölçü | Değer(ler) | Sınıf | Kaynak | Not |
|---|---|---|---|---|
| 1466 papalık şap şirketi | Camera'ya **2 dukat/kantar** (Civitavecchia depolarından çıkan) · ek kârın **2/3'ü Camera'ya** · başka anlatım: Tolfa gelirinin **1/3'ü Medici, 2/3'ü "Camera ve haçlı fonu"** | ◐ | K110, K111, K59, K63 | Hangi kantarın ağırlığı? (**doğrulanamadı**) |
| 1470 Ischia | **25 yıllık** anlaşma (Haz 1470) | ○ | K110, K111 | |
| Edward III borcu (Villani) | Bardi **900.000 fl** (£135.000) · Peruzzi **600.000 fl** (£90.000) | ◐ | K11, K12, K13 | Peruzzi sermayesinden büyük → rakam şüpheli. |
| Edward IV (Londra) | **>£26.000** (1466–71, kısmen ödendi) · kralın borcu **£10.500** (popüler) | ○ | K72, K59 | |
| Camera'ya kredi (1455) | **6.000 fl** | ○ | K82 | |
| Charles the Bold (Brugge) | 1478'de **"9.500 groat"** (birim belirsiz) | ○ | K93 | |
| "Sforza 55.000 florin" | yönü belirsiz | ○ | K91 | Kullanma. |

### 4E. Bulunamayan sayılar (kota bitti)

| Ölçü | Durum | Nereye bakılmalı |
|---|---|---|
| Usta/işçi **günlük ücretleri** | **Bulunamadı** | Ridolfi–Vasta, Siena WP 928 (>20.000 gözlem, Opera del Duomo/Badia Fiesolana) ve Opera'nın *Libro ordinario dei maestri e manovali* kayıtları (ör. 26 Mart 1425) arama sonuçlarında **göründü, açılmadı**. Goldthwaite (*The Building of Renaissance Florence*) ve Cohn (*The Laboring Classes in Renaissance Florence*, 1980) **benim HAFIZA önerim**; sonuçlarda bulunamadı. |
| **Palazzo Medici maliyeti** | **Bulunamadı** | Ferretti (UniFi; sonuçlarda göründü, açılmadı); Kent ve Goldthwaite (HAFIZA önerisi). |
| **Giovanni'nin 1427 beyanı** ve Cosimo'nun 1457 beyanı | **Bulunamadı** | Brown Üniv. Catasto veritabanı; Herlihy–Klapisch-Zuber; Georgia Southern tezi (catasto plutokratları; K123; arama sonuçlarında göründü). |
| Cosimo'nun toplam serveti, bankanın **zirve sermayesi** | **Bulunamadı** (içerik çiftliklerinin "net worth" rakamları kullanılmadı) | de Roover (1963) tabloları. |
| **Kubbe maliyeti** | **Bulunamadı** | Opera del Duomo belgeleri (MPIWG veritabanı). |

---

## 5. Bankanın işleyişi (c2/c3 için çalışma notları)

### 5A. Kambiyo senedi (bill of exchange), adım adım

**Önce dürüstlük notu:** Arama sonuçlarında *Medici'ye ait belgelenmiş* tek bir poliçe örneği çıkmadı. Aşağıda (1) **belgeli klasik model** (de Roover'ın 1399–1400 Brugge→Barselona poliçesi; John Munro metni yeniden yayımlıyor; ◐: K67, K68, K69, K70) ve (2) bunun **Medici ağına uyarlanmış açıklayıcı şeması** (belge değil, model; **sayı yok**) var.

**(1) Belgeli model: Brugge → Barselona (1399–1400)**

| Adım | Ne olur | Not |
|---:|---|---|
| 1 | Brugge'de bir Floransalı tüccar (**çeken/drawer**, kimi yazarda *taker*) Flandre mallarını Barselona'ya ihraç edecek; parası ihracattan önce lazım. | Para, alıcının ödemesinden **önce** gerekiyor. |
| 2 | Tüccar poliçeyi Brugge'deki **bankere** (*remitter/giver*) satar; banker parayı **peşin** verir. | Fiilen **kredi** bu; poliçe teminat. |
| 3 | Poliçe, Barselona'daki Floransalı ithalatçıya (**ödeyici/drawee**) çekilmiştir: "vadede şu parayı, bankerin Barselona'daki muhabirine (**alacaklı/payee**) öde." | Dört taraf: çeken, banker, ödeyici, muhabir. |
| 4 | **Vade (usance):** şehir çiftleri arasında gelenekle belirli süre; poliçe bu sürede yolculuk eder. | Munro: usance çoğu zaman sabit gelenek. |
| 5 | Muhabir poliçeyi vadede sunar, tahsil eder, bankerin hesabına geçirir. | |
| 6 | **Dönüş poliçesi (recambio/rechange):** muhabir aynı parayla Brugge'ye çekilmiş ikinci bir poliçe alır; sermaye geri döner. | Kâr **kur farkından**; iki poliçe de darphane paritesinin bankerin lehine üstünde fiyatlanır → "faiz" yazılmaz. |
| 7 | **Sınır:** ortaçağ poliçeleri çoğunlukla **devredilemez**; banker vade boyunca kendi sermayesiyle finanse eder. Devredilebilirlik sonra gelişti: **1436 Londra Belediye Mahkemesi** kararı (taşıyan, adı yazılı alıcıyla aynı haklara sahip); Anvers ve Brugge'de 1500'lerin başında benzerleri. | K67, K68. |
| 8 | Sınama verisi: Borromei bankasının Brugge ve Londra defterlerinden 1436–39 arası **≈2.000 poliçe** incelenmiş (Bolton & Guidi-Bruscoli). | K69. |

**(2) Medici uyarlaması (şema; belge değil):** Roller aynıdır; fark, **banker ile muhabirin aynı ağın iki şubesi** olması ve her şubenin **ayrı ortaklık, ayrı defter** tutmasıdır (şubeler birbirleriyle "dışarıdakilerle olduğu gibi" hesaplaşır: K59 ve K01'in yapı anlatımı). Örnek akış (açıklayıcı): Londra şubesi, yün ihracatçısı bir tüccara sterlin ödeyip onun için Brugge'ye çekilmiş poliçeyi satın alır → poliçe Brugge şubesince vadede tahsil edilir → Brugge'de sterlin karşılığı Flaman kumaşı ya da şap alımı yapılır, bedel Floransa'ya/Roma'ya çekilmiş poliçelerle kapatılır. Kâr, **şehirler arası kur farkı ve vade**dedir. **Bu zincirin Medici'ye özgü bir örneği doğrulanamadı** (HAFIZA/model); senaryoda "Londra–Brugge–Floransa üçgeni, her şubenin kendi defteri" diye anlatılabilir, **tutar uydurulmamalı**.

### 5B. Faiz yasağı ve çözümleri

- **Kilise:** doğrudan borçta fazlalık = tefecilik. Bankerlerin savunması: **kambiyo kredi değildir**; "borç yoksa tefecilik de yok" (K66 + dokumen.pub özetleri K58/K59/K111; ◐ — Floransa'nın bankerler loncasının adı da *Arte del Cambio*'dur).
- **Cambio secco (kuru kambiyo):** gerçek para/mal hareketi olmayan, **kurgusal kambiyo**; sonuç faiz gibidir; dönüş kuru baştan sabitlenirse düpedüz faizli borçtan farksızdır (K66). Medici muhasebesinde kârların bir kısmının kuru kambiyodan geldiği, **Milano şubesinin** bu yola ara sıra başvurduğu belirtiliyor (dokumen.pub kitap özetlerinden biri — K58/K111; **○**, tek özet). Floransa'da kuru kambiyo **1429'da tefecilik diye yasaklanmış, 1435'te yasak kalkmış** (○, tek kaynak: K66).
- **Ahlakçılar:** Floransa başpiskoposu **Sant'Antonino** (1445'ten) ve **San Bernardino** bu uygulamayı hile diye mahkûm etti (bir Hollandaca/İngilizce sanat tarihi kitabı özeti; de Roover'a atıf yapıyor — K111). Kardinal **Cajetan**, *De Cambiis* (1499): faiz, ikinci poliçenin kurunda saklanabilir (K66, K112). Standart modern kaynak: **de Roover, "What Is Dry Exchange?" (JPE, 1944)**.
- **Discrezione (isteğe bağlı faiz):** mevduatta faiz sözleşmeye yazılmaz; banker "lütuf" olarak, **kendi takdiriyle** öder → "faiz değil hediye". Parks'ın bir özetinden: (1) gizli/ketum, (2) faiz bankerin takdirinde, (3) sözleşmesel değil (K92/NovelInvestor; ○ — özet düzeyi; **primer kaynak görülmedi**).
- **Sözleşme dili:** Medici–şube müdürü sözleşmeleri işi "dürüst ve meşru" kambiyo diye adlandırır (○; D24).
- **Floransa tutumu:** Tefecilik yurttaş eleştirisinin hedefiydi, ama sermayedar bankerlerin kredisini yasaklamayı savunan çıkmadı (*Civic World of Early Renaissance Florence* özeti, K115; ○).
- **Vicdan boyutu → sanat/hayır:** bkz. D26, D31–D36 (kefaret tezi = *yorum*).

### 5C. Ortaklık / "holding" yapısı

| Konu | Bulgu | Sınıf | Kaynak |
|---|---|---|---|
| Bardi/Peruzzi | **Tek ortaklık**, tüm şubelerin sahibi | ◐ | K01, K12 |
| Medici | Şubeler **ayrı ortaklıklar**: her birinin kendi unvanı, sermayesi, defteri; şubeler birbirleriyle dışarıdaki gibi işlem yapar | ◐ | K01, K59 |
| "Holding" etiketi | Bir makale "holding çoğu zaman şubelerin sermayesinin %50'sinden fazlasına sahipti" der; bir kitap "ana şirket katmanı **ortadan kalktı**, aile her müdürle doğrudan ortak oldu" der | çelişkili (◐) | K53, K59 |
| Medici payı | **≥%50** (popüler bir tarih sitesi; Bank Frogs olabilir, özet belirtmedi) / **>%50** (akademik makale) | ○ | K119?, K53 |
| Müdürler | Eş-sahip; **maaş değil kâr payı**; sözleşme ≤5 yıl; ana ortaklar her zaman feshedebilir; kâr payı çoğu kez sermaye payından **büyük** | ◐ | K59, K01, K90 |
| Roma | Bu kuralın **istisnası**: sermayesiz; Kilise mevduatıyla çalışır | ○ | K58 |
| Temsilcilik | Şube olmayan yerlerde temsilci/sessiz ortak | ○ | K59 |
| Sassetti | Cenevre'de (sonra Lyon) ortak olarak kâr payı almaya devam etti | ○ | K59 |
| 1457 örneği | Bir Floransalı ortak: Floransa bankasını yönetiyor, sermayede **400 fl** payı var | ○ | K58 |

**Senaryo için çıkarım:** "Holding" kelimesi **sonradan** (de Roover'ın) etiketi; çağdaşların ağzında "ortaklık (compagnia)". Güvenli anlatım: *"Aile, her şubede en büyük ortak; müdür ise küçük ortak ama büyük kâr paylı."*

### 5D. Şube listesi (açılış/kapanış)

| Şube | Açılış | Kapanış | Sınıf | Kaynak | Not |
|---|---|---|---|---|---|
| Floransa (merkez/tavola) | **1397** (Roma'dan taşınma; Orsanmichele) | **1494** | ◐ | K58, K49, K01 | |
| Roma | ≈1385/86 (*Vieri e Giovanni de' Medici in Roma*); 1393 *Giovanni de' Medici e compagni*; 1397 yeni ortaklıkla faaliyet | 1494 (HAFIZA, **doğrulanamadı**) | ◐ (açılış) | K50, K52, K58 | Sermayesiz; papalık hesabı |
| Venedik | karar 1398; **resmî şube 25 Mart 1402** | doğrulanamadı (HAFIZA: 1470'ler sonu–80'ler) | ◐ | K58, K01 | Daha önce Vieri döneminde "yabancı poliçe" ofisi (bir özet; Vieri sayfası K52 olabilir) |
| Napoli, Gaeta | Giovanni dönemi (tarih yok) | doğrulanamadı | ○ | K64 | |
| Pisa | 15. yy ortasında listede | doğrulanamadı | ○ | K65 | |
| Cenevre | doğrulanamadı (HAFIZA: 1420'ler); Sassetti müdür 1448–59 (HLS) | **1466: Lyon'a taşındı** | ○ | K54, K71 | de Roover'ın, bir Cenevre alt şubesinin Konsil sona erince kapandığı yönünde **varsayımı** var (tarih yok; K01 özeti) |
| Brugge | **24 Mart 1439** resmî (ajan/muhabir 1416'dan) | doğrulanamadı (Portinari dönemi; HAFIZA ≈1480) | ○ | K01, K93 | |
| Londra | Canigiani 1446'dan çalışıyor; şube "15. yy'ın ilk yarısında"; müdür 1465 | doğrulanamadı; "1478" iddiası **desteklenmedi** | ○ | K72 | |
| Avignon | doğrulanamadı (HAFIZA: 1446); 1458 beyanında var | doğrulanamadı | ○ | K90 | |
| Milano | doğrulanamadı (HAFIZA: 1452); 1458 beyanında var | doğrulanamadı | ○ | K90 | |
| Lyon | **1466** (Cenevre'den) | 1494 (HAFIZA) | ○ | K54 | |
| Basel, Ancona, Lübeck vb. | HAFIZA | — | HAFIZA | — | Doğrulanmadı; listeye girmesin |

### 5E. Defterler ve çifte kayıt

- **Mit:** bkz. düzeltme #3, kronoloji 71–76, §6/M1. Medici defterlerinin *çifte kayıtlı* olması (HAFIZA: evet, ama ilk değil, ve **konsolide bilançosu yoktu** — doğrulanmadı) başka, "icat etti" başka.
- **Kalan defterler / dosyalar:** (i) **Sassetti'nin gizli defteri 1462–1472** (K71; ○). (ii) de Roover'ın kullandığı **libri segreti** — bir yayıncı metni "1950'de bulundu", bir başkası "de Roover ve eşi 1938 yazında fotoğrafladı" diyor (K03; çelişkili). (iii) Floransa Devlet Arşivi **Mediceo avanti il Principato** — Londra şubesine dair çok belge içerir, de Roover tamamını kullanmadı (K72). (iv) Harvard **Baker Library**, Medici–Tornaquinci fonu (K02). (v) **catasto beyanları** (1427, 1457/58).
- **Defterlerden çıkan serinin değeri:** 6.644 → 12.425 → 19.386 florin/yıl (§4C).
- **Atmosfer:** Datini'nin "Tanrı'nın ve kârın adıyla" başlığı gibi tüccar duası (HAFIZA) — **bu dosyada doğrulanmadı**, Medici'ye bağlanmamalı.

---

## 6. Mit/efsane ve tarihçi tartışmaları

> Biçim: iddia → kim ne diyor → kaynaklı değerlendirme (sınıf).

| # | İddia | Kim ne diyor | Değerlendirme | Sınıf |
|---|---|---|---|---|
| M1 | **"Medici çifte kayıt muhasebeyi icat etti."** | Atıfsız forum metni: Giovanni di Bicci'nin getirdiği ("[hangisi?]" etiketli). Karşı: Cenova Massari 1340 (erken biçim ≈1327), Datini ≈1380, Venedik 1407, Cotrugli 1458, Pacioli 1494. | **MİT.** Pacioli bile icat etmedi, derledi. Medici'nin kullanması ayrı soru. Videoda "çifte kayıt Medici'den önce de vardı" denmeli. | ◐ |
| M2 | **"Medici modern bankacılığın atası / ilk çok şubeli banka."** | Popüler: "modern finansı icat etti" (K96). Akademik: şubeleri **ayrı ortaklık** yapması farklı (K01); bir İtalyan yazar "daha gevşek" der (K02); Peruzzi'nin 15 şubesi var (K12). | Nitelikli: Medici **bir halka**, "ilk" ya da "icat" değil. Özgün olan: ortaklıklar ağı + Kilise hesabı + kambiyo/şap ağı. | ◐ |
| M3 | **"Avrupa'nın en büyük bankası."** | BYU tezi: "Quattrocento'nun en büyük Avrupa finans kuruluşu" (K90). Veri: 1402'de ≈17 çalışan; Peruzzi 1330'larda ≈100 faktör (K01, K12). | 15. yy için savunulabilir; **ölçüt belirtilmeli**. Mutlak "en büyük" denmez. | ○ |
| M4 | **"Bardi ve Peruzzi yalnız Edward III yüzünden battı."** | Villani: 900.000/600.000 fl (kardeşi Peruzzi'de); Britannica: kral borçları iptal etti; bir Cambridge kitabı ve makaleler: Peruzzi'nin o kadar sermayesi yoktu, "basit" görüş. | Villani'nin rakamı **retorik/tahmin**; tek nedenli anlatım yanlış. Veba **neden değil** (çöküş 1342–46, veba 1348). | ◐ |
| M5 | **"Florin neden güvenilir para oldu?"** | Bizans altınının 4. Haçlı Seferi sonrası aksaması; ≈280 yıl sabit standart; taklit edilen ilk uluslararası Avrupa altını (Wikipedia, nitelikli). | Gerçek ve sağlam; "ilk altın" diyemezsin (Cenova aynı yıl — HAFIZA). Dante'nin lanetini ekle (D01). | ◐ |
| M6 | **"Cosimo sanata 600 bin florin harcadı."** | Wikipedia: ">600.000 florin, ≈500 milyon dolar, sanat ve kültüre" (K89). Hafızam: Lorenzo'nun *Ricordi*'si 1434–71 için 663.755 florin, "bina, sadaka, vergi" (**doğrulanamadı**). | Rakamın kapsamı belirsiz; "sanat" yerine "bina, sadaka ve vergi" daha güvenli. **Doğrulanana kadar rakam yok.** | ○ |
| M7 | **"Medici sanatı = tefecilik kefareti."** | Vespasiano (vicdan cümlesi); Parks; Harvard sergisi ("iade/telafi" tezi); popüler anlatımlar (Papa'nın günahları bağışlaması). Karşı: Cossa mezarı gibi örnekler "Medici'nin kendini tanıtması" diye de okunuyor (Wikipedia). Floransa'da bankerlik toplumsal olarak normaldi. | Kefaret bir **yorum**; belgeli çıpalar: Vespasiano'nun cümlesi + San Marco devri (1436). **Hem kefaret hem itibar** — c4'ün "yatırım mı kefaret mi" sorusu doğru çerçeve. | ○ |
| M8 | **"Giovanni'nin son öğüdü: gösterişli olma."** | Machiavelli: yasaların verdiği payı al, kıskançlık istenenden doğar; Cavalcanti: dindar vedalaşma; modern kitaplar: "dikkat çekme". | **ANEKDOT**; üç sürüm yan yana verilebilir. Hiçbirinin kelimesi bu dosyada doğrulanmadı. | ○ |
| M9 | **"Cossa'nın mezarı Martinus'a meydan okumadır."** | Wikipedia: "V. Martinus'a çelme" ya da "Medici'nin kendini tanıtması". | Belgeli olan: yazıt "eski papa" ve itiraz; niyet **yorum**. Yürütücüler ve ödeyen belirsiz. | ◐ |
| M10 | **"Lorenzo kötü bankacıydı; kamu parasına el attı."** | Machiavelli: ajanlar prens gibi, servet eridi, toprağa yöneldi. Market Histories: çeyiz fonuna elini daldırdı. Hafızam: de Roover ekolü ve Guicciardini/Molho tartışması. | Ajan sorunu Machiavelli'den (Medici siparişli!) geliyor ○; **çeyiz fonu iddiası tek ve zayıf — kullanma**. Brugge/Londra'da karar Sassetti'ye ve Portinari'ye de bağlı. | ○ |
| M11 | **"Ciompi önderi şu konuşmayı yaptı."** | Machiavelli III.13 isimsiz önderin konuşmasını **uydurur**. | Bu bir **edebi kurgu**; "Machiavelli, 145 yıl sonra, ağzına şunu koyar" çerçevesiyle kullan. | ◐ |
| M12 | **"Medici adı doktor kökenli; toplar hap/kupa."** | Efsane; "palle" için bezant (Bizans ağırlığı) açıklaması birkaçından biri. | "Derler ki" düzeyi; kanıt yok. | ○ |
| M13 | **"Giovanni bugün X milyar dolar değerinde."** | İçerik çiftlikleri (kaynaksız). | **Kullanma.** Rakamsal çıpa: ≈180.000 florin (○). | ○ |
| M14 | **"Medici → Fugger → Rothschild zinciri."** (HAFIZA) | Popüler tarihler (ör. Ferguson, *The Ascent of Money*; Portekizce baskısı arama sonuçlarında göründü). | HAFIZA: anlatısal süreklilik; **kurumsal süreklilik yok** (farklı şehir, kuşak, ortaklık biçimi). Ortak payda: papalık/kraliyet kredisi + poliçe ağı. **Doğrulama gerekir.** | HAFIZA |
| M15 | **Padgett & Ansell, "Robust Action and the Rise of the Medici, 1400–1434"** (AJS, 1993) (HAFIZA) | Ağ analizi: evlilik, ortaklık, dostluk bağları; Medici örgütlü bir "parti" değil, birbirine bağlı olmayan gruplar arasında **tek köprü** (yıldız biçimli ağ); Cosimo'nun eylemi "çok-sesli" (multivocal), kasıtlı belirsizlik. | HAFIZA: ayrıntı (kaç aile, hangi veri) **doğrulanamadı**; bu dosyada yalnız atıf var. Eleştiri: Kent ve başkaları (HAFIZA). | HAFIZA |
| M16 | **"Floransa'nın zenginleri değişmez."** | Barone–Mocetti: 1427'nin en zengin aileleri ≈600 yıl sonra yine en zengin (K45, K46). | Çarpıcı ve kaynaklı; yıl/yöntem kontrol edilmeli. | ◐ |
| M17 | **"Banka 1494'te battı."** | Resmî son 1494; çözülme 1470'lerde şube şube; 1494'te el koyma (ayrıntı **bulunamadı**). | "1494'te kapandı" demek yeter; neden çok etkenli (Brugge/Londra kredileri, yönetim, siyasi risk). | ◐ |

---

## 7. TR-BAĞ (Osmanlı / Türkiye)

> **Not:** Bu paketteki arama sonuçları Osmanlı yönünü neredeyse hiç döndürmedi. Aşağıda yalnızca **T1 ◐**; **T2, T6, T7 ○**; geri kalanı (T3, T4, T5, T8) **HAFIZA** ve senaryoya girmeden önce doğrulanmalıdır.

| # | Konu | İçerik | Sınıf | Kaynak / Not |
|---|---|---|---|---|
| T1 | **1466 papalık şap sözleşmesi** (Medici–Camera) | Medici Tolfa madenlerinin işletmesi ve satışına ortak; kantar başına 2 dukat; ek kârın 2/3'ü Camera'ya (diğer anlatım: 1/3 Medici, 2/3 "Camera ve haçlı fonu") | ◐ | K110, K111, K59, K63 (dokumen özetleri) |
| T2 | **Şap = haçlı fonu** | "Haçlı fonu" ifadesi (Tolfa gelirinin Türk karşıtı kullanımı) özetlerde geçti; Pius II/Giovanni da Castro hikâyesi arama sonucunda **çıkmadı** | ○ | K111; ayrıntı HAFIZA |
| T3 | **Foça (Phocaea) şapı** | Ege kıyısında (bugünkü Eski Foça/İzmir) Cenevizlilerin elindeki şap madeni; Osmanlı'ya geçişi **1455 (HAFIZA)**; Fetih (1453) → Foça (1455) → Tolfa (1461) → Medici (1466) kronolojisi | HAFIZA | Doğrulanmadı |
| T4 | **Osmanlı şapı** | Şebinkarahisar ve Kütahya şap işletmeleri; "Şebin" adının şapla ilişkisi (Şebinkarahisar'ın adı "şap kara kalesi" diye açıklanır) | HAFIZA | Etimoloji doğrulanamadı; Türk izleyici için sevimli çıpa olabilir |
| T5 | **Volterra 1472** | Volterra'da şap bulundu (1470); Floransalı sendikanın (Lorenzo dahil) imtiyazı → ayaklanma → Montefeltro ordusunun yağması (Haz 1472) | HAFIZA | Pazzi/Lorenzo bağı (c7–c8) nedeniyle başka araştırma paketleriyle çakışabilir; çakışırsa orada doğrulananı esas al |
| T6 | **Okunacak** | Setton, *The Papacy and the Levant (1204–1571)*, cilt 2 (arama sonucunda listelendi); *Capital at Work in Antwerp's Golden Age* (şap ticareti); *Soil to Foil* (alüminyum tarihi, şap bölümü) | ○ | K63, K110, dokumen.pub |
| T7 | **Türkçe kaynak** | dokumen.pub'da Türkçe *Medici Ailesi – Rönesans Çağı'nda Bankacılık, Siyaset ve Sanat* (ISBN 9786257631396). Yazar/çeviri **doğrulanamadı**; Parks'ın kitabı olabilir. Türkçe terimler (compagnia, tavola vb.) için işe yarar. | ○ | K60 |
| T8 | **Para** | Floransa florini / Venedik dukası / Osmanlı akçesi ve altını ilişkisi; Mehmed II'nin altın sikkesi (1477?) — **hiç aranmadı** | HAFIZA | Devam sorgusu |

---

## 8. Sahne adayları ("yıldız an")

> Her aday: yer · kişiler · gün/saat akışı · belgelenmiş sözler · belirsiz noktalar · kaynak sağlamlığı.

### S1 · 22 Temmuz 1378 — Palazzo Vecchio'da bir yün tarayıcısı (c1)
- **Yer:** Piazza della Signoria / Palazzo Vecchio (Santa Croce çevresi: Fransiskenler yardım etti — The Florentine).
- **Kişiler:** Michele di Lando (yün tarayıcısı), **Salvestro de' Medici** (gonfaloniere), Ciompi kalabalığı, Santa Croce Fransiskenleri.
- **Akış (belgeli çizgi, ◐):** 18 Haz 1378 Salvestro seçilir → 22 Temmuz işçiler sarayı alır; di Lando gonfaloniere, Salvestro istifa → 30 Temmuz üç yeni lonca → Ağustos sonu lonca milisleri Ciompi'yi ezer. **Saat akışı yok (HAFIZA: 20–22 Temmuz'da evler yakıldı; doğrulanmadı).**
- **Sözler:** Belgeli söz **yok**. Machiavelli'nin **uydurduğu** isimsiz konuşma (III.13) var — "tarihçinin ağzına koyduğu söz" olarak kullanılabilir.
- **Belirsiz:** Fransiskenlerin rolü (tek kaynak), Salvestro'nun tutumu (karşı-devrimde öne çıktığı söyleniyor), saatler, konuşmanın kaynağı.
- **Sağlamlık:** Olay ◐; ayrıntılar zayıf. **Medici bağı:** bir Medici'nin ilk "halkçı" maskesi (ironi — yalnız Giovanni hattıyla aynı olup olmadığı belirsiz).

### S2 · 20 Şubat 1429 (Floransa takvimiyle 1428) — Giovanni'nin son öğüdü (c2)
- **Yer:** Medici evi, Floransa (adres doğrulanamadı; Palazzo Medici 1445'ten sonra).
- **Kişiler:** Giovanni (≈69), Cosimo (≈39), Lorenzo (kardeş), aile.
- **Akış:** hastalık → oğulların çağrılması → öğüt → ölüm → "herkesin yası" (Machiavelli). **Saat/gün ayrıntısı yok.**
- **Sözler (üç sürüm):** Machiavelli (parafraz: huzurla gidiyor, yasaların verdiği payı al); Cavalcanti (EN: *"Beloved sons, neither I nor any man born into this world should feel grief at exchanging worldly cares for perpetual repose."*); modern gloss (*"Be careful not to draw attention to yourself"*).
- **Belirsiz:** konuşma gerçekten yapıldı mı; hangisi eskiye daha yakın (Cavalcanti 1440'lar, Machiavelli ≈1520–25); gloss'un asıl kaynağı.
- **Sağlamlık:** Üç sürümün **farkı** zaten sahne: Zweig/Plutarkhos çerçevesinde "kaynaklar bile uzlaşmıyor" dürüstlüğü.

### S3 · 1420'ler — Vaftizhane'de "eski papa" (c2)
- **Yer:** Floransa Vaftizhanesi (Battistero di San Giovanni), Cossa'nın mezarı (Donatello + Michelozzo, 1422–28).
- **Kişiler:** Cossa'nın vasiyet yürütücüleri, Donatello, Michelozzo, V. Martinus (itiraz), Giovanni ve Cosimo (kefalet/davet).
- **Akış:** 22 Ara 1419 ölüm → 1422–28 mezar → yazıt "eski papa" → itiraz.
- **Sözler:** Yazıt (EN: *"John the former pope"*; Latince **HAFIZA**: *IOANNES QUONDAM PAPA XXIII*).
- **Belirsiz:** yürütücüler kimdi (Cosimo'nun yürütücü olduğu **doğrulanamadı**), fidye tutarı (HAFIZA 38.000 fl), mezarı kimin ödediği.
- **Sağlamlık:** Olay ◐; **mizah potansiyeli yüksek, kurban yok** (papalık kurumuna ve "eski"liğe yönelen ironi).

### S4 · 6 Ocak 1443 — Papa Cosimo'nun hücresinde (c3/c4 geçişi)
- **Yer:** San Marco, Floransa; yeni kilisenin kutsanması; Cosimo'nun kendi hücresi.
- **Kişiler:** IV. Eugenius, Cosimo, Observant Dominikler.
- **Akış:** 1436 devir → 1437'de yeniden inşa (+10.000 fl, tek kaynak) → 6 Ocak 1443 kutsama; papa geceyi Cosimo'nun hücresinde geçirir.
- **Sözler:** Vespasiano (modern çeviri): *"accumulated quite a bit on his conscience…"*; papadan **kayıtlı söz yok**.
- **Belirsiz:** kefaretin "ilanı" (modern yorum), 10.000 fl rakamı, hücre ayrıntısı.
- **Sağlamlık:** ○–◐. "Banker ve vicdan" sahnesi için en iyi görsel yer (hücre bugün müzede, HAFIZA).

**Yedek (zayıf):** Kasım 1494'te saray yağması ve defterlerin akıbeti — **kaynak çıkmadı**.

---

## 9. Okunacak kaynaklar (gerçekten bulunanlar — arama sonuçlarında göründü, **açılıp okunmadı**)

**Bankacılık ve ekonomi**
- **Raymond de Roover**, *The Rise and Decline of the Medici Bank, 1397–1494* (Harvard UP, 1963; Norton yeniden baskı) — K58, K03. Tablolar: dönem kârları, şube payları. *(Metin parçaları yalnız dokumen.pub özetinde görüldü.)*
- **Raymond de Roover**, *The Medici Bank: Its Organization, Management, Operations, and Decline* (1948) — K03.
- **de Roover**, "What Is Dry Exchange?" (*Journal of Political Economy*, 1944) — K66, K112.
- *Journal of Economic History*: "The Medici Bank: Financial and Commercial Operations" ve "Decline of the Medici Bank" başlıklı yazılar (yazar/yıl **doğrulanamadı**) — K73, K74.
- **John Munro**'nun poliçe sayfaları (Toronto) — 1399 Brugge→Barselona poliçesinin özgün metnini içerir — K68.
- **Bolton & Guidi-Bruscoli**, Borromei bankası poliçeleri (EHS blog "Your flexible friend") — K69.
- **Edwin S. Hunt**, *The Medieval Super-Companies* (Cambridge UP, 1994; yazar adı **HAFIZA**, sayfa Cambridge Core'da göründü) — K13.
- **Richard Goldthwaite**, *The Economy of Renaissance Florence* (Johns Hopkins UP, 2009) — yalnız dokumen.pub listelemesi görüldü — K124.
- *A Comparative History of Bank Failures: From Medici to Barings* (Routledge, 2019) — K59.
- *Florentine Banks in Germany* (Alberti, Medici, Spinelli, 1400–1475) — K62.
- **Ridolfi & Vasta**, "Reffici debet! The real wages of the workers of the Dome of Florence (1326–1861)", Siena WP 928 (2025) — K99.

**Floransa'nın toplumu**
- **Herlihy & Klapisch-Zuber**, *Tuscans and Their Families* (Yale, 1985; Fr. 1978) — K39, K40.
- **Nicholas Eckstein**, "Addressing Wealth in Renaissance Florence: Some New Soundings from the Catasto of 1427" (2006) — K41.
- **Barone & Mocetti**, Florence 1427–2011 hareketlilik çalışması — K46.
- **Paolo Malanima**, "Plague and Renaissance in Tuscany" — K19.
- **George Brucker**, *The Medici in the Fourteenth Century* (1957) — K114.

**Medici portreleri**
- **Tim Parks**, *Medici Money* (2005) — K92.
- **P. Terenzi**, "Medici, Giovanni di Bicci de'", *Dizionario Biografico degli Italiani* — K50 (PDF: UniFi).
- Historisches Lexikon der Schweiz, "Medici" girişi — K54.
- Cambridge: "Lorenzo de' Medici's London Branch" (*Progress and Problems in Medieval England*) — K72; *Charles the Bold in Italy 1467–1477*, Portinari bölümü — K94.

**Birincil metinler (özetle görüldü; açılmadı)**
- **Machiavelli**, *History of Florence* (Gutenberg #2464; kitap IV, VII, VIII) — K55; Fordham ayıklaması — K95.
- **Giovanni Villani**, *Nuova Cronica* (Gutenberg #33022: Selfe çevirisi) — K38.
- **Marchionne di Coppo Stefani**, *Cronaca fiorentina* (Rodolico, *RIS* 30) — K24, K25.
- **Boccaccio**, *Decameron*, 1. Gün girişi — K21.
- **Janet Ross**, *Lives of the Early Medici as Told in Their Letters* (Gutenberg #74973) — K56 (Cavalcanti çevirisi içerir).
- **Alfred von Reumont**, *Lorenzo de' Medici* (Gutenberg #50624, #50625) — listelendi, açılmadı.
- **Dante**, *Paradiso* IX; **Stocchi-Perucchio**, "Il maladetto fiore: Dante e il denaro alle origini del capitalismo" — K113.
- **Yves Winter**, Machiavelli'nin Ciompi konuşması üzerine makale — K31.

---

## 10. Eksikler ve devam sorguları (WebSearch kotası doldu)

| # | Eksik | Önerilen sorgu |
|---|---|---|
| E1 | **Usta/işçi ücretleri**, florin satın alma gücü | "Goldthwaite Building of Renaissance Florence wages master mason soldi per day 1420s"; "Ridolfi Vasta real wages Dome of Florence table"; `allowed_domains: dokumen.pub` |
| E2 | **Palazzo Medici maliyeti** | "Palazzo Medici Via Larga cost florins Michelozzo Kent Ferretti" |
| E3 | **Giovanni'nin 1427 beyanı**, Cosimo'nun 1457/58 beyanları | "catasto 1427 top taxpayers Palla Strozzi Giovanni di Bicci net worth Herlihy"; Brown Üniv. catasto veritabanı |
| E4 | **Tolfa 1461, Foça 1455, Volterra 1472, Pazzi şap/depositary 1473** | "Tolfa alum 1461 Giovanni da Castro Pius II Commentaries"; "Phocaea alum Genoese Ottoman 1455"; "sack of Volterra 1472 alum Lorenzo syndicate"; "Sixtus IV Pazzi papal depositary 1473 alum Medici" |
| E5 | **Şube tarihleri** (Cenevre, Avignon, Milano, Pisa, Londra, Brugge, Venedik kapanışları) | "de Roover Medici bank branches Geneva 1424 Avignon 1446 Milan 1452 closed 1478 1480 1481"; `allowed_domains: dokumen.pub` |
| E6 | **Lorenzo ve banka:** de Roover'ın tezinin kendi sözleriyle formülü; Portinari'nin 1480 tasfiyesi; Lionetto de' Rossi (Lyon); **Monte delle doti** için bilimsel kaynak; Lorenzo'nun amcaoğulları (Pierfrancesco) velayeti/1485 davası | "Lorenzo de' Medici bank neglect de Roover Portinari 1480 liquidation Lionetto de' Rossi Lyon"; "Molho Marriage alliance Monte delle doti Lorenzo Guicciardini" |
| E7 | **1494 el koyma**, defterlerin ve alacaklıların akıbeti; Medici kütüphanesinin San Marco'ya satışı | "1494 Medici confiscation inventory Signoria Piero creditors Medici bank liquidation Lyon" |
| E8 | **Padgett & Ansell** bulguları (aile sayısı, ağ türleri) ve eleştirisi | "Padgett Ansell Robust Action Rise of the Medici 1993 marriage network findings critique Kent" |
| E9 | **Fugger/Rothschild süreklilik** iddiası ve Medici sonrası papalık bankacıları | "Ferguson Ascent of Money Medici Fugger Rothschild critique"; "Fugger papal banker Medici successor" |
| E10 | **Cosimo'nun kayıtlı sözleri** (Vespasiano İtalyanca aslı; Machiavelli VII.6 "paternostri"; "meglio città guasta che perduta") | "Vespasiano da Bisticci Vita di Cosimo de' Medici coscienza testo"; "Machiavelli Istorie fiorentine VII 6 Cosimo paternostri" |
| E11 | **Giovanni'nin konuşmasının İtalyanca metni** (Machiavelli IV; Cavalcanti) | "Machiavelli Istorie fiorentine IV Giovanni de' Medici morendo chiamò Cosimo e Lorenzo"; "Cavalcanti Istorie fiorentine Giovanni de' Medici morte" |
| E12 | **Datini ve tüccar kültürü; "pietra dello scandalo"** (Mercato Nuovo) | "Datini 'Nel nome di Dio e del guadagno'"; "pietra dello scandalo Mercato Nuovo bankrupt debtors" |
| E13 | **Cossa:** fidye tutarı, vasiyet yürütücüleri | "Baldassarre Cossa ransom Medici 38,000 florins executors will Cosimo" |
| E14 | **Kara Veba sonrası ücretler (Floransa)**, 1300 nüfusu | "Florence wages after Black Death 1349 Cohn"; "Florence population 1300 estimate" |
| E15 | **TR-BAĞ:** Floransa–Osmanlı ticareti, florin/duka/akçe | "Florence Ottoman trade Mehmed II 1450s privileges Cosimo Pera"; "Ottoman gold sultani 1477 Venetian ducat" |

---

## 11. Kaynak anahtarı

> Hepsi **ikincil/aracılı** erişimdir (arama özeti). URL'ler arama sonuçlarında göründüğü gibi. Wikipedia ve kopyaları tek kaynak sayıldı.
> K15, K16, K37, K42, K47, K87 satırları arama sonuçlarında göründü ama olgu satırlarında doğrudan atıf yapılmadı (ek okuma/yan kaynak).

| Kod | Kaynak | URL |
|---|---|---|
| K01 | Wikipedia — Medici Bank | https://en.wikipedia.org/wiki/Medici_Bank |
| K02 | Linkiesta (2012) — "Banche al collasso, quando Wall Street era Firenze" | https://www.linkiesta.it/2012/02/banche-al-collasso-quando-wall-street-era-firenze/ |
| K03 | Bookshare katalog kayıtları (de Roover 1948/1963) | https://www.bookshare.org/browse/book/1986150 · https://www.bookshare.org/browse/book/1985769 |
| K04 | Wikipedia — Florin | https://en.wikipedia.org/wiki/Florin |
| K05 | Deutsche Bundesbank — Gold florin of Florence | https://www.bundesbank.de/en/bundesbank/numismatics/selected-objects/sign-of-the-lily-616530 |
| K06 | Moruzzi Numismatica — The Florin | https://www.moruzzi.it/lang2/the_florin.html |
| K07 | Wikipedia — Guilds of Florence | https://en.wikipedia.org/wiki/Guilds_of_Florence |
| K08 | Wikipedia — Ordinances of Justice | https://en.wikipedia.org/wiki/Ordinances_of_Justice |
| K09 | Brewminate — Corporate guild order… | https://brewminate.com/corporate-guild-order-control-of-the-florentine-republic-in-the-13th-and-14th-century/ |
| K10 | HistoryRise — Florence before the Renaissance | https://historyrise.com/florence-before-the-renaissance-guilds-wealth-and-rivalries/ |
| K11 | Wikipedia — Compagnia dei Bardi | https://en.wikipedia.org/wiki/Compagnia_dei_Bardi |
| K12 | Wikipedia — Peruzzi | https://en.wikipedia.org/wiki/Peruzzi |
| K13 | Cambridge Core — *Medieval Supercompanies*, Introduction | https://www.cambridge.org/core/books/medieval-supercompanies/introduction/ED84CB6808B41CFE1D63A8C924F4A0D5 |
| K14 | Britannica — Peruzzi family | https://www.britannica.com/print/article/453334 |
| K15 | IDEAS/RePEc — J. Econ. Hist. 50(1), 1990, 149–162 | https://ideas.repec.org/a/cup/jechis/v50y1990i01p149-162_03.html |
| K16 | British History Online — Russell, Bardi/Peruzzi ve Edward III | https://www.british-history.ac.uk/manchester-uni/london-lay-subsidy/1332/pp93-135 |
| K17 | Oregon State Open Textbook — The Black Death | https://open.oregonstate.education/middleearlymodernages/chapter/black-death/ |
| K18 | Conversable Economist — Some economics of the Black Death | https://conversableeconomist.com/2022/04/14/some-economics-of-the-black-death/ |
| K19 | EHS — Malanima, Plague and Renaissance in Tuscany | https://ehs.org.uk/plague-and-renaissance-in-tuscany/ |
| K20 | Berkeley Economics Review — Upheaval: plague, peasants and the proletariat | https://econreview.studentorg.berkeley.edu/upheaval-plague-peasants-and-the-proletariat-in-14th-century-europe/ |
| K21 | The Conversation — Boccaccio's Decameron | https://theconversation.com/guide-to-the-classics-boccaccios-decameron-a-masterpiece-of-plague-and-resilience-143437 |
| K22 | Hektoen International — Boccaccio on pandemics | https://hekint.org/2020/11/04/giovanni-boccaccio-on-pandemics-past-and-present/ |
| K23 | LitCharts — Decameron, Day 1 Introduction | https://litcharts.com/lit/the-decameron/day-1-introduction |
| K24 | Wikipedia — Cronaca fiorentina di Marchionne di Coppo Stefani | https://en.wikipedia.org/wiki/Cronaca_fiorentina_di_Marchionne_di_Coppo_Stefani |
| K25 | Fordham Medieval Sourcebook — Marchione di Coppo Stefani | https://sourcebooks.web.fordham.edu/med/marchione.asp |
| K26 | History Today — Debating Death and Disease | https://www.historytoday.com/node/52766 |
| K27 | Wikipedia — Michele di Lando | https://en.wikipedia.org/wiki/Michele_di_Lando |
| K28 | The Florentine — The Ciompi Uprising (2025) | https://www.theflorentine.net/2025/07/31/the-ciompi-uprising/ |
| K29 | Hanover Historical Review 2018 — Kitchel, The Ciompi Revolt of 1378 | https://history.hanover.edu/hhr/18/HHR2018-kitchel.pdf |
| K30 | Wikipedia — Ciompi Revolt | https://en.wikipedia.org/wiki/Ciompi_Revolt |
| K31 | DOAJ — Astérion (Kas 2016), Machiavelli'nin Ciompi konuşması | https://doaj.org/article/f640387ae9874f14b56e10f54eb5c75e |
| K32 | Wikipedia — Florentine Histories | https://en.wikipedia.org/wiki/Florentine_Histories |
| K33 | Wikipedia — Giovanni Villani | https://en.wikipedia.org/wiki/Giovanni_Villani |
| K34 | EBSCO Research Starters — Giovanni Villani | https://www.ebsco.com/research-starters/biography/giovanni-villani |
| K35 | Cambridge — *Dante in Context*, "Education" | https://resolve.cambridge.org/core/books/dante-in-context/education/9B7A91C40466293B462F36DA51BC91FF |
| K36 | UPenn HIST 230 — The City Takes Shape: Schools | https://web.sas.upenn.edu/hist-230/?p=22 |
| K37 | Menant, *Prelude to the Renaissance* (2009) PDF | https://www.histoire.ens.psl.eu/IMG/file/Menant/Menant,%20Prelude%20to%20the%20Renaissance%20(2009).pdf |
| K38 | Project Gutenberg #33022 — Villani's Chronicle | https://www.gutenberg.org/ebooks/33022 |
| K39 | Brown Üniv. Catasto projesi — Herlihy dosyaları notu | https://cds.library.brown.edu/projects/catasto/newsearch/note_on_herlihy_files.html |
| K40 | NYRB (1986) — "The Other Florence" | https://www.nybooks.com/articles/1986/10/09/the-other-florence/ |
| K41 | Eckstein (2006), Journal of Urban History | https://journals.sagepub.com/doi/10.1177/0096144206287095 |
| K42 | World History Commons — Florence Catasto of 1427 | https://worldhistorycommons.org/florence-catasto-1427 |
| K43 | Wikipedia — Palla Strozzi | https://en.wikipedia.org/wiki/Palla_Strozzi |
| K44 | Archivio Storico Fiorentino — Palla Strozzi finansı makalesi | https://oajournals.fupress.net/index.php/asf/article/download/7993/7991/7870 |
| K45 | Tribune.com.pk — richest families of Florence in 1427 remain the richest | https://tribune.com.pk/story/1165161/richest-families-florence-1427-remain-richest |
| K46 | EUI — Mocetti, Intergenerational mobility Florence 1427–2011 | https://www.eui.eu/Documents/DepartmentsCentres/Economics/Seminarsevents/Mocetti.pdf |
| K47 | CLARIAH dataLegend — The Florentine Catasto of 1427 | https://stories.datalegend.net/catasto |
| K48 | Wikipedia — Giovanni di Bicci de' Medici | https://en.wikipedia.org/wiki/Giovanni_di_Bicci_de%27_Medici |
| K49 | Italy On This Day — Giovanni di Bicci de' Medici, banker | https://www.italyonthisday.com/2026/02/giovanni-di-bicci-de-medici-banker.html |
| K50 | Treccani DBI — Medici, Giovanni di Bicci de' (P. Terenzi) | https://www.treccani.it/enciclopedia/giovanni-di-bicci-de-medici_res-0d7a7119-9b6c-11e6-9e53-00271042e8d9_(Dizionario-Biografico)/ · PDF: https://flore.unifi.it/bitstream/2158/1180965/1/Terenzi_DBI-Medici-Giovanni.pdf |
| K51 | Palazzo Medici Riccardi mediateca — Giovanni di Averardo detto Bicci | https://mediateca.palazzomediciriccardi.it/Personaggi/bicci-detto-giovanni-di-averardo-de-medici/ |
| K52 | Wikipedia — Vieri de' Medici | https://en.wikipedia.org/wiki/Vieri_de%27_Medici |
| K53 | ResearchGate — A Modern Look at the Banco de' Medici: Governance and Accountability Systems | https://www.researchgate.net/publication/309692478_A_Modern_Look_At_The_Banco_De'_Medici_Governance_And_Accountability_Systems |
| K54 | Historisches Lexikon der Schweiz — Medici | https://hls-dhs-dss.ch/it/articles/025536/ |
| K55 | Project Gutenberg #2464 — Machiavelli, History of Florence | https://www.gutenberg.org/files/2464/2464-h/2464-h.htm |
| K56 | Project Gutenberg #74973 — Lives of the Early Medici | https://www.gutenberg.org/files/74973/74973-h/74973-h.htm |
| K57 | IntraText — Machiavelli, Florentine Histories (IV) | https://www.intratext.com/IXT/ENG1267/4T.HTM |
| K58 | dokumen.pub — de Roover, *Rise and Decline of the Medici Bank* | https://dokumen.pub/the-rise-and-decline-of-the-medici-bank-1397-1494-9780674771451.html |
| K59 | dokumen.pub — *A Comparative History of Bank Failures: From Medici to Barings* | https://dokumen.pub/a-comparative-history-of-bank-failures-from-medici-to-barings-2019001662-9780367191092-9780429200489.html |
| K60 | dokumen.pub — *Medici Ailesi – Rönesans Çağı'nda Bankacılık, Siyaset ve Sanat* (Türkçe; yazar belirsiz) | https://dokumen.pub/medici-ailesi-rnesans-anda-bankaclk-siyaset-ve-sanat-9786257631396.html |
| K61 | dokumen.pub — *A Short History of Renaissance Italy* | https://dokumen.pub/a-short-history-of-renaissance-italy-2nbsped-103221869x-9781032218694.html |
| K62 | dokumen.pub — *Florentine Banks in Germany* | https://dokumen.pub/florentine-banks-in-germany-the-market-strategies-of-the-alberti-medici-and-spinelli-1400-1475-3968222474-9783968222479.html |
| K63 | dokumen.pub — Setton, *The Papacy and the Levant, 1204–1571*, vol. 2 | https://dokumen.pub/the-papacy-and-the-levant-1204-1571-vol-2-9780871691279.html |
| K64 | Clute Institute IBER (Medici şubeleri) | https://clutejournals.com/index.php/IBER/article/download/9827/9921/36514 |
| K65 | Saylor Academy — The Origins and Evolution of Global Banking | https://learn.saylor.org/mod/book/view.php?id=72553 |
| K66 | arXiv 2010.10703 — Cancellation of principal in banking… | https://arxiv.org/pdf/2010.10703 |
| K67 | arXiv 2009.08668 — International Trade Finance from the Origins to the Present | https://arxiv.org/pdf/2009.08668 |
| K68 | John Munro (Toronto) — The Bill of Exchange | https://www.economics.utoronto.ca/munro5/BILLEXCH.htm |
| K69 | EHS — "Your flexible friend": the bill of exchange… | https://ehs.org.uk/your-flexible-friend-the-bill-of-exchange-in-theory-and-practice-in-the-fifteenth-century/ |
| K70 | historylab.es — The functioning of a bill of exchange | https://historylab.es/the-functioning-of-a-bill-of-exchange-in-the-late-middle-ages/ |
| K71 | Wikipedia — Francesco Sassetti | https://en.wikipedia.org/wiki/Francesco_Sassetti |
| K72 | Cambridge — "Lorenzo de' Medici's London Branch" | https://www.cambridge.org/core/books/progress-and-problems-in-medieval-england/lorenzo-de-medicis-london-branch/2E4EDA1AB98762E9165D05A4175181D9 |
| K73 | Cambridge JEH — "The Medici Bank: Financial and Commercial Operations" | https://www.cambridge.org/core/journals/journal-of-economic-history/article/medici-bank-financial-and-commercial-operations/E8865702110452B1C5B0341407C0DBAC |
| K74 | Cambridge JEH — "Decline of the Medici Bank" | https://resolve.cambridge.org/core/journals/journal-of-economic-history/article/decline-of-the-medici-bank/62FE8FE5810E09274AE0FBDD66E0F867 |
| K75 | ICAEW — Earliest books on bookkeeping | https://icaew.com/library/library-collection/historical-accounting-literature/earliest-books-on-bookkeeping |
| K76 | Clute Institute IBER (muhasebe tarihi) | https://clutejournals.com/index.php/IBER/article/download/4003/4056/15999 |
| K77 | York Üniv. "Your Review" (muhasebe tarihi) | https://yourreview.journals.yorku.ca/index.php/yourreview/article/download/40678/36935/50926 |
| K78 | EXP Group — Who invented double-entry bookkeeping? | https://theexpgroup.com/blog/the-birth-of-double-entry-bookkeeping |
| K79 | Wikipedia — Tomb of Antipope John XXIII | https://en.wikipedia.org/wiki/Tomb_of_Antipope_John_XXIII |
| K80 | Opera di S. Maria del Fiore — Funeral monument of the Antipope John XXIII | https://duomo.firenze.it/en/discover/baptistry/9144/ |
| K81 | WDTPRS — Day 7, Florence: pici, paintings, and anti-popes | https://wdtprs.com/?p=56378 |
| K82 | British History Online — Vatican Regesta 438: 1455 · Wikipedia — Apostolic Camera | https://prod.british-history.ac.uk/node/89154 · https://en.wikipedia.org/wiki/Apostolic_Camera |
| K83 | Wikipedia — Cosimo de' Medici's cell | https://en.wikipedia.org/wiki/Cosimo_de%27_Medici%27s_cell |
| K84 | NYRB (2002) — "The Cosimos" | https://www.nybooks.com/articles/2002/12/19/the-cosimos/ |
| K85 | Hidden Florence — Cosimo: Patrons & penitence · Balancing the books | https://hiddenflorence.org/stories/cosimo/6-patrons-penitence/ · https://hiddenflorence.org/stories/cosimo/introduction-balancing-the-books/ |
| K86 | Brewminate — God, power and money: did Cosimo de' Medici deceive Renaissance Florence? | https://brewminate.com/god-power-and-money-did-cosimo-demedici-deceive-renaissance-florence/ |
| K87 | Brewminate — Arts endowment: banking, metaphysics and art | https://brewminate.com/arts-endowment-banking-metaphysics-and-art-in-fifteenth-century-florence/ |
| K88 | Harvard Omeka — Art for the Soul (sergi) | https://hist1993-16.omeka.fas.harvard.edu/exhibits/show/art-for-the-soul/introduction/the-patron |
| K89 | Wikipedia — Cosimo de' Medici | https://en.wikipedia.org/wiki/Cosimo_de%27_Medici |
| K90 | BYU lisans tezi — Cosimo de Medici, his Rise to Fortune… | https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1155&context=thetean |
| K91 | The Spectator — Mark Archer | https://spectator.co.uk/?p=212994 |
| K92 | Parks *Medici Money* incelemeleri/tanıtımlar (NovelInvestor, Three Monkeys, Profile, getAbstract) | https://novelinvestor.com/notes/medici-money-by-tim-parks/ · https://threemonkeysonline.com/?p=3757 · https://profilebooks.com/work/medici-money/ · https://www.getabstract.com/pt/resumo/medici-money/5556 |
| K93 | Wikipedia — Tommaso Portinari | https://en.wikipedia.org/wiki/Tommaso_Portinari |
| K94 | Cambridge — *Charles the Bold in Italy 1467–1477*, Portinari bölümü | https://www.cambridge.org/core/books/charles-the-bold-in-italy-14671477/relations-with-florence-and-the-activities-of-tommaso-portinari/685D243A2003787B474C9173CFE01B28 |
| K95 | Fordham Medieval Sourcebook — Machiavelli on Lorenzo | https://sourcebooks.web.fordham.edu/Halsall/source/machiavelli-histflo-lorenzo.asp |
| K96 | Market Histories — Rise and Fall of the Medici Bank | https://www.markethistories.com/en/the-rise-and-fall-of-the-medici-bank-how-renaissance-florence-invented-modern-finance-1397-1494 |
| K97 | Wikipedia — Monte delle doti | https://en.wikipedia.org/wiki/Monte_delle_doti |
| K98 | Wikipedia — Piero the Unfortunate · Britannica · Encyclopedia.com | https://en.wikipedia.org/wiki/Piero_the_Unfortunate · https://www.britannica.com/print/article/372362 · https://www.encyclopedia.com/people/history/italian-history-biographies/piero-de-medici |
| K99 | Siena WP 928 — Ridolfi & Vasta (RePEc/DEPS) | https://econpapers.repec.org/paper/usiwpaper/928.htm · https://www.deps.unisi.it/it/node/1953 |
| K100 | Rutgers MemDB (Spufford, *Handbook of Medieval Exchange*) · Numista/koleksiyon sayfaları | https://memdb.libraries.rutgers.edu/spufford-currency?page=49 |
| K101 | Wikipedia — Italian lira | https://en.wikipedia.org/wiki/Italian_lira |
| K102 | uamr.de — Cosimo: Vermögen und Biographie | https://www.uamr.de/?p=14147 |
| K103 | Chalmers Biographical Dictionary — Medici, Cosmo de | https://words.fromoldbooks.org/Chalmers-Biography/m/medici-cosmo-de.html |
| K104 | Florence As It Was (W&L) — Cosimo the Elder | https://florenceasitwas.wlu.edu/people/cosimo-medici.html |
| K105 | WonderfulMuseums — Museum of San Marco | https://www.wonderfulmuseums.com/museum/museum-of-san-marco-florence/ |
| K106 | UniFi — Ferretti, Palazzo Medici (PDF) | https://flore.unifi.it/retrieve/handle/2158/1039731/131850/Ferretti%20palazzo%20medici.pdf |
| K107 | VisitTuscany — Palazzo Medici Riccardi | https://www.visittuscany.com/it/attrazioni/palazzo-medici-riccardi/ |
| K108 | History Today — The Death of Cosimo de' Medici | https://www.historytoday.com/archive/months-past/death-cosimo-de-medici |
| K109 | RallyPoint (Wikipedia kopyası) — Cosimo, 1 Ağu 1464 | https://www.rallypoint.com/shared-links/bad-title-wikipedia--9 |
| K110 | dokumen.pub — *Capital at Work in Antwerp's Golden Age* (şap) | https://dokumen.pub/capital-at-work-in-antwerps-golden-age-studies-in-european-urban-history-1100-1800-55-9782503595634-2503595634.html |
| K111 | dokumen.pub — *Cultural Exchange Between the Low Countries and Italy* | https://dokumen.pub/cultural-exchange-between-the-low-countries-and-italy-1400-1600-museums-at-the-crossroads-9782503518381-2503518389.html |
| K112 | Markets & Morality (cambio secco) | https://marketsandmorality.com/index.php/mandm/article/download/278/269 |
| K113 | Dante/florin: First Online (TR) · Linkiesta (2024) · Dialnet (Stocchi-Perucchio) | https://firstonline.info/tr/dante-di-alighieri-ve-floransa%27dan-komediye-ekonomi/ · https://www.linkiesta.it/2024/09/letteratura-denaro-economia-classici-dante/ · https://dialnet.unirioja.es/descarga/articulo/7988925.pdf |
| K114 | Wikipedia — House of Medici · Averardo de' Medici · The Florentine (2005) | https://en.wikipedia.org/wiki/House_of_Medici · https://en.wikipedia.org/wiki/Averardo_de%27_Medici · https://www.theflorentine.net/2005/04/21/the-medici-story-of-a-european-dynasty/ |
| K115 | dokumen.pub kitap kopyaları (Roma kâr payı/depositary sorgusu; özet hangisinden aldığını belirtmedi): *Florentine Banks in Germany*; *The Civic World of Early Renaissance Florence*; *The Speculator of Financial Markets*; *The Making of the Modern Corporation*; *Jewish Bankers and the Holy See* | https://dokumen.pub/ (başlıkla arayın) |
| K116 | dokumen.pub — *A ascensão do dinheiro* (Ferguson, *The Ascent of Money*, Portekizce; yazar çıkarımı HAFIZA) | https://dokumen.pub/a-ascensao-do-dinheiro-a-historia-financeira-do-mundo-3-ediao-3nbsped-6555352175-9786555352177.html |
| K117 | Palazzo Medici tavanları makalesi (fupress/OI) | https://oajournals.fupress.net/index.php/oi/article/download/7919/7917/7796 |
| K118 | Forum/grup metni — "Luca Pacioli and double-entry bookkeeping" · a2asimulations forumu | https://groups.google.com/g/insurance-mortgage/c/Ovivv91vqic · https://a2asimulations.com/forum/viewtopic.php?p=401748 |
| K119 | Bank Frogs — Medici Bank: International Bankers to the Pope | https://bankfrogs.com/medici-bank-international-bankers-to-the-pope/ |
| K120 | skuola.net — Lorenzo'nun *Ricordi* tarihlemesi (Floransa yılbaşı 25 Mart) | https://www.skuola.net/documenti/appunti-appunti-letteratura-italiana-i-prima-parte-207900 |
| K121 | Met Müzesi · Smarthistory · GetDailyArt — Memling'in Portinari portreleri | https://metmuseum.org/art/collection/search/437056 · https://smarthistory.org/?p=57442 · https://www.getdailyart.com/en/20330/hans-memling/maria-portinari |
| K122 | MPIWG — "Duomo" belge veritabanı (Opera del Duomo ücret kayıtları) | https://duomo.mpiwg-berlin.mpg.de/ENG/RE/RElist31002S0.HTM |
| K123 | Georgia Southern tezi — 1427 catasto ve Floransa plütokratları | https://digitalcommons.georgiasouthern.edu/etd/2101 |
| K124 | dokumen.pub — Goldthwaite, *The Economy of Renaissance Florence* | https://dokumen.pub/the-economy-of-renaissance-florence-9780801896880-9780801889820-9781421400594.html |
| K125 | Literary Review — Parks, *Medici Money* incelemesi (Giovanni'nin "kamu gözünden uzak dur" öğüdü) | https://literaryreview.co.uk/?p=2053 |

**Güvenilmez bulunan ve KULLANILMAYAN sayfalar:** "net worth" içerik çiftlikleri (ör. wiki.rastrosystem.com.br, archive.jimboystacos.com, mc.nooknet.net, dev2.wearedeeperblue.co.uk, briston.voipcom.network, lsfellowship.missouri.edu makalesi), "HistoryCollection" (yapay zekâ destekli popüler makale: kendi uyarısı), Reddit yanıtları.
