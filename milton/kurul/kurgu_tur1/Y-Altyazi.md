# Y-Altyazı (altyazı editörü, Türkçe altyazı merceği): kurgu tur 1

Bakılan dosyalar: `milton.tr.srt` (379 altyazı, son çıkış 1538,14 sn), `senaryo.json` (`alt`), `timeline.js` (kelime zamanları), `tools/srt.py`, `animatik/planlar.json`.
Ölçümler Python betikleriyle bütün dosya üzerinde yapıldı (betikler ve ham çıktılar: `.../scratchpad/kurul_altyazi/`). Görüntü tarafı için 142 planın her birinden 3 kare (%30, %60, %90; toplam 426 kare) `fillText` kancasıyla taranıp her ekran yazısının gerçek y koordinatı ölçüldü; ayrıca 6 karenin üstüne YouTube tarzı altyazı bindirilerek bakıldı (`m1.png`).

## 1. Puan ve karar

| Ölçüt | Ağırlık | Puan | Not |
|---|---|---|---|
| Metin doğruluğu ve yazım | %25 | 9,0 | SRT `alt` ile birebir aynı; tek gerçek yazım hatası "Milton'ın" |
| Okuma hızı ve süre | %20 | 9,3 | ort. 13,7 kr/sn; yalnız 3 altyazı 17'nin üstünde |
| Anlam öbeğine göre bölme (satır ve altyazı) | %25 | 7,0 | asıl zayıf halka; araç dengeli uzunluğa göre bölüyor, dile bakmıyor |
| Senkron ve aralar | %15 | 9,0 | başlangıçlar kelimeye tam oturuyor; 80 ms'lik boşluklar titreme riski |
| Görüntüyle ilişki (alt bant, çift okuma, son 30 sn) | %15 | 8,3 | 3 etiket altyazı bandına çok yakın; çift okuma kabul edilebilir |

**Ağırlıklı puan: 8,5 / 10. Karar: RED** (eşik 9,0; hiçbir ölçüt 7'nin altında değil, bölme ölçütü tam 7,0'da). Neredeyse bütün düzeltmeler `srt.py` kuralıyla ya da tek bir yazım değişikliğiyle yapılabilir; yapılırsa 9,2 civarı bekliyorum.

## 2. Engelleyici bulgular
Yayını durduracak bir şey yok. Ama iki bulgu yayından önce düzeltilmeli, çünkü izleyicinin gözüne ilk çarpacak hatalar bunlar:
1. **Özel ad ikiye bölünmüş: "C." ile "S. Lewis" ayrı altyazılarda** (#311 ve #312). Araç tek harflik "C." kısaltmasını cümle sonu sanıyor. Altyazı #311 yalnız "Yirminci yüzyılda ise Narnia'nın yazarı C." diye kalıp 1 sn ekranda duruyor, sonra "S. Lewis" geliyor.
2. **"Milton'ın" yazımı 12 yerde ünlü uyumuna aykırı.** Türkçede yabancı özel adlara gelen ekler okunuşa göre yazılır; "Milton" son ünlüsü "o" olduğu için doğrusu "Milton'un" (Newton'un gibi). Seslendirme metni (`tts`) "Milton'un" yazıyor, altyazı "Milton'ın". `KURUL.md` 180. satır bunu bilerek bırakılmış gibi kaydetmiş. Doğru ifade bence "Milton'un" olmalı; emin olmadığım tek nokta bu kararın kayda geçmiş bir gerekçesi olup olmadığı (bkz. madde 5).

## 3. Ölçümler

### Okuma hızı ve süre
- Karakter/saniye (boşluklar dahil): ortalama 13,7, ortanca 13,7, en yüksek 18,3; %90'lık dilim 16,0.
- **17 kr/sn üstü: 3 altyazı**, **20 kr/sn üstü: yok.**
  - #39 (142,67 sn): 17,4 kr/sn, 71 kr / 4,08 sn. "gözleri henüz görürken, bir tiyatro / oyununun açılışı olarak yazılmıştı."
  - #167: 17,7 kr/sn, 26 kr / 1,47 sn. "Sana dostça seslenmiyorum."
  - #244: 18,3 kr/sn, 42 kr / 2,29 sn. "Bir zamanlar en yüce yer için yarışan ben,"
  - 16 üstü 33 altyazı, 15 üstü 95 altyazı. Yani çoğu rahat; tavan 17 olarak belirlenmiş, 3 altyazıda aşılıyor çünkü sonraki cümle çok yakın başlıyor. Kabul edilebilir, düzeltme listesinde en altta.
- Süre: **1 sn'den kısa yok** (en kısa 1,00 sn; ≤1,3 sn olanlar 8: #41, #152, #185, #195, #261, #317, #322, #374; hepsi tam cümle, sorun yok). **7 sn'den uzun: 1** (#203, 7,01 sn, 78 kr). 5,5 sn üstü 28 altyazı.
- Satır: **42'yi aşan 1 satır** (#82, 43 kr: "kendinden üstüne başkaldırana hizmet etmek;"). En uzun satır 43. 40 ve üstü 43 satır, 38 ve üstü 77 satır (632 satırın %12'si). **Üç satırlı altyazı yok.** 126 tek satırlı, 253 iki satırlı altyazı. Altyazı başına en çok 80 kr, 75 kr üstü 26 altyazı.
- #203 yedi saniye boyunca "öfkeyle, kıskançlıkla, umutsuzlukla." sayımını baştan ekranda tutuyor; yüzün üç kez değişmesiyle eşleşen bir sayım, ama altyazı hepsini birden önceden veriyor. İkiye bölünmesi hem 7 sn sınırını düzeltir hem sayımı sesle eşler (":" sonrası ikinci altyazı).

### Aralar
- Çakışma ya da negatif boşluk yok.
- **Aralar: 80 ms'lik 80 boşluk** (srt.py `nxt - .08`). 100 ms ve altı toplam 91; bunların 54'ü cümle ortasında (önceki altyazı noktalamayla bitmiyor). 30 fps'te 2,4 kare: ekranda bir göz kırpması gibi kısa bir boş kare olarak görülüyor. Konuşma sürerken (aynı cümlenin ikinci yarısı) boşluk sıfır olmalı; yalnız cümle sonlarında kalmalı (düzeltme #9).
- Cümle ortasında gereksiz uzun boşluk yok: cümle ortası boşlukların en büyüğü 600 ms (#341→#342, "şöyle resmetti:" sonrası, alıntı öncesi); 2 sn üstü 14 boşluğun hepsi segment sınırında.

### Metin doğruluğu
- SRT kelimeleri (2605) `senaryo.json` `alt` metniyle **birebir aynı** (eksik, fazla, değişmiş kelime yok); noktalama dahil karşılaştırıldı.
- Dosya UTF-8, CRLF yok, çift boşluk yok, üç nokta yerine tek `…` karakteri (1 yerde, #166), düz tırnak (`"`) yok, kıvrık tırnak “ ” tutarlı.
- Özel adlar tutarlı: Milton, Beelzebub, Abdiel, Uriel, Nifates, Pandemonium, Cabanel, Blake, Lewis, Shelley, Cromwell, Prometheus, Âdem, Havva, Aden, Hürmüz hep aynı yazılıyor; ek tekrarları tutarlı ("Nifates'in/Dağı'nda", "Uriel'e/'in", "Abdiel'in"). Büyük harf: Cehennem/cennet yalnız cümle başında ve "Cennet'ten" (kitap adı) büyük; "Ölüm", "Günah", "Kaos" kişileştirme olarak tutarlı büyük. Bir tutarsızlık yok.
- Yazım sorunları (hepsi küçük):
  1. "Milton'ın" ×12 → "Milton'un" (yukarıda). Ek: ses de aynı biçimde okuyor.
  2. G10 (#188): "Gururu, ve cehennemde bıraktığı ordunun önünde rezil olma korkusu." "ve" öncesi virgül Türkçede olağan değil (vurgu için kasıtlı olabilir; kabul edilebilir).
  3. Apostrof düz (`'`), tırnak kıvrık (“ ”): tipografik tutarsızlık; YouTube yazı tipinde fark edilmez. Düzeltme gerekmez; ister ’ kullanılır.
  4. H01 / #208 "Yok etmeye geldiğin bir şeyi, sevebilir misin?": nesne ile fiil arasındaki virgül dilbilgisi açısından gereksiz; duraklama için seçilmiş (ses de duruyor). Dokunma.
  5. De/da, ki, mi yazımı hatasız (taranan "ki" örnekleri: "Diyelim ki", "aç ki", "büyüktür ki" doğru ayrı; "Belki/Peki/Doğudaki…" birleşik doğru).
- Kitap adı "Kayıp Cennet'e Önsöz" altyazıda biçimsiz (italik/tırnak yok). SRT bunu italik ifade edemez (YouTube `<i>` etiketini destekler ama güvenilmez); alıntı olmadığı için sorun değil.

### Bölme ve tırnak taşıması
- **73 altyazı cümlenin ortasında bitiyor** (cümle noktalaması yok). Çoğu virgül/noktalı virgülden sonra olduğundan iyi; asıl sorun öbeğin ortasından kesilenler. Dil kuralıyla taradığım adaylar (satır sonu ya da altyazı sonu: "bir, bu, en, çok, bütün, tek, ve, ama, ki, de, için, gibi, kadar, ancak", tamlayan eki "…'ın/'in", açık tırnak): 24 satır sonu, 25 altyazı sonu, hepsi araçtaki `wrap()` ve bölme maliyetinin dile bakmamasından.
- **Tırnak taşıması:** 40 alıntı var; 63 altyazı açık bir tırnağın içinde başlıyor; **21 alıntı 3 altyazıya yayılıyor, en uzunu 5** (#314–#318, Lewis). Açılış tırnağı yalnız ilk altyazıda, kapanış yalnız sonuncuda. Standart uygulama bu; ortadaki altyazılarda "bunu kim söylüyor?" sorusu kalıyor. Asıl sorunlu olanlar, alıntının açılışı bir altyazının son 2–4 kelimesine sıkıştığında: #81 ("…şunu söyler: “Asıl kölelik budur: akılsıza ya da" / ardından devam), #176 ("“Sadık kalanlar gibi" tek başına altyazı sonunda), #246 ("“Kim yükselmeye"), #170/#171 ("…hem de Tanrı / için: “Benden böyle bir"), #198/#362 ("…o ne kadar" altyazı sonu). Alıntı açılışının altyazı sonuna sıkışması, izleyicinin ilk bakışta ne okuduğunu anlamasını zorlaştırıyor.
- #202: "Elveda pişmanlık.” “Kötülük: sen benim iyiliğim ol.”" aynı altyazıda iki ayrı alıntı; doğru, ama tek tırnak çifti gibi okunabilir. Kabul.

### En kötü 15 bölme (numara, mevcut durum, önerilen bölme)
`|` satır sonu, `||` altyazı sınırı. Önerilen satırlar ≤42 kr, işaretlenenler 43 kr (aşağıdaki 3 numaralı kural önerisiyle 44'e kadar yumuşak sınır gerektirir).

1. **#311/#312 (1260,40 sn):** "…Narnia'nın yazarı C." || "S. Lewis, Kayıp Cennet'e Önsöz|adlı kitabında…". **Öneri:** "Yirminci yüzyılda ise Narnia'nın|yazarı C. S. Lewis," || "Kayıp Cennet'e Önsöz adlı kitabında|tam tersini savundu." (Kural hatası, `srt.py` 42. satır.)
2. **#38/#39 (142,67 sn):** "…çok daha önce, Milton'ın" || "gözleri henüz görürken, bir tiyatro|oyununun…". Tamlayan ile tamlanan ayrılmış. **Öneri:** #38 "Yeğeninin anlattığına göre, bu hikâyenin|ilk dizeleri çok daha önce," || "Milton'ın gözleri henüz görürken, bir|tiyatro oyununun açılışı olarak yazılmıştı." (satır 2 = 43; bu altyazı zaten 17,4 kr/sn ile hızlı, süre ayarı kendiliğinden düzelir).
3. **#50–#53 (196,95 sn):** "Bir gün, Milton'ın|anlattığına göre, Tanrı bütün" || "melekleri…"; ayrıca "…sayılacak ve|dönüşü olmayan…" (satır sonunda "ve"). **Öneri:** "Bir gün, Milton'ın anlattığına göre," || "Tanrı bütün melekleri toplar ve|Oğul'u onların başına geçirir."; #53: "Tanrı'ya karşı gelmiş sayılacak|ve dönüşü olmayan bir karanlığa düşecektir." (43).
4. **#176/#177 (712,40 sn):** "Sonra kendine bir soru sorar:|“Sadık kalanlar gibi" || "senin de özgür iraden,|…". Açık tırnak üç kelimeyle altyazı sonunda. **Öneri:** #176 "Sonra kendine bir soru sorar:" || "“Sadık kalanlar gibi senin de özgür iraden,|ayakta kalma gücün yok muydu?" (43/29).
5. **#198/#199 ve #362/#363 (797,29 ve 1458,73 sn):** "…barışı bağışlamaktan o ne kadar" || "uzaksa, dilemekten ben o kadar uzağım.”" (aynı cümle iki kez geçiyor, ikisinde de "o ne kadar" altyazı sonu). **Öneri:** #198 "“Beni cezalandıran da bunu biliyor.|Bu yüzden," || "barışı bağışlamaktan o ne kadar uzaksa,|dilemekten ben o kadar uzağım.”" ve #362 "Şeytan bunu da biliyordu:" || "“Barışı bağışlamaktan o ne kadar uzaksa,|dilemekten ben o kadar uzağım.”" (40/36).
6. **#246/#247 (987,14 sn):** "Ve kendi geleceğini söyler:|“Kim yükselmeye" || "kalkarsa, yükseldiği|kadar…". **Öneri:** "Ve kendi geleceğini söyler:" || "“Kim yükselmeye kalkarsa, yükseldiği|kadar alçalmak zorundadır." (36/26).
7. **#251/#252 (1007,98 sn):** "Sonra destanın belki de en|şaşırtıcı anı gelir: Havva'nın" || "masumiyeti…". Hem satır sonunda "en" hem sıfat+ad hem tamlayan ayrı. **Öneri:** "Sonra destanın belki de en şaşırtıcı|anı gelir:" || "Havva'nın masumiyeti karşısında Şeytan,|kendi kötülüğünden kopup dalgın durur." (36/10 ve 39/38)
8. **#170/#171 (693,65 sn):** "…bir şey söyler, hem de Tanrı" || "için: “Benden böyle bir|karşılığı hak etmemişti." **Öneri:** #170 "Sonra hiç beklemediğimiz|bir şey söyler, hem de Tanrı için:" || "“Benden böyle bir karşılığı|hak etmemişti. Beni yaratmıştı;…" (alıntı artık altyazının başında).
9. **#157/#158 (632,62 sn):** "…cennete altın bir zincirle" || "asılı, ayın yanındaki en|küçük yıldız kadar bir dünya." Satır sonunda "en". **Öneri:** "Sonunda uzakta bir şey görür:|cennete altın bir zincirle asılı," || "ayın yanındaki en küçük yıldız|kadar bir dünya."
10. **#349/#350 (1404,39 sn):** "Şeytan destanın bir|yerinde ağlıyor; başka bir" || "yerinde, “boyun eğmek”|…". Üç satır sonu "bir". **Öneri:** "Şeytan destanın bir yerinde ağlıyor;" || "başka bir yerinde, “boyun eğmek”|sözünü kendine yasaklıyor."
11. **#308/#309 (1246,11 sn):** "Blake'in gerekçesi şuydu:|Milton gerçek bir" || "şairdi ve…". **Öneri:** "Blake'in gerekçesi şuydu:" || "Milton gerçek bir şairdi ve|farkında olmadan Şeytan'ın tarafındaydı."
12. **#12/#13 (41,11 sn):** "…çıkmış bir karakter; biz de bu" || "hikâyeyi bir din anlatısı olarak değil,…" (altyazı sonu ve satır sonu "bu"). **Öneri:** üç altyazı: "Buradaki Şeytan, bir şairin kaleminden|çıkmış bir karakter;" || "biz de bu hikâyeyi bir din anlatısı|olarak değil," || "bir edebiyat eseri olarak okuyacağız."
13. **#27 (99,02 sn):** "Bu adam yalnızca bir şair değil, bir|devrimciydi: …". **Öneri:** "Bu adam yalnızca bir şair değil,|bir devrimciydi: Kralın idamını savunmuştu." (32/43). Aynı örüntü: #124 "…yıkılmış bir|başmelek" → "ama hâlâ yıkılmış|bir başmelek kadar görkemli."; #139 "…edemediği bu|yolculuğa" → "…edemediği|bu yolculuğa…" ; #143 "…onu çok|iyi tanıyan" → "Cehennemin kapısında,|onu çok iyi tanıyan biri bekliyordu."
14. **#375/#376 (1515,43 ve 1520,83 sn, bitiş ekranı):** "Ateşi insanlar için çalan bir başka|asinin, Prometheus'un hikâyesi ekranda." (satır sonunda "bir başka"); #376 "Romantik şair Shelley'ye göre|Prometheus'a benzeyen tek hayalî" || "karakter, …" (sıfat ile ad iki altyazıya bölünmüş). **Öneri:** #375 "Ateşi insanlar için çalan|bir başka asinin, Prometheus'un hikâyesi ekranda." (26/48 → 44 üstü; o zaman "Ateşi insanlar için çalan bir başka asinin,|Prometheus'un hikâyesi ekranda." 44/31); #376 "Romantik şair Shelley'ye göre|Prometheus'a benzeyen tek hayalî karakter," (29/42) || "Milton'ın Şeytan'ıydı; ama Prometheus hırstan,".
15. **#11 (35,75 sn):** "Bu hikâye bir şiirden: John Milton'ın|destanından, Kayıp Cennet'ten." (tamlayan satır sonunda). **Öneri:** "Bu hikâye bir şiirden: John|Milton'ın destanından, Kayıp Cennet'ten." kötü görünüyor; daha iyisi "Bu hikâye bir şiirden:|John Milton'ın destanından," || "Kayıp Cennet'ten. Buradaki Şeytan," (üç altyazı; aynı zamanda #12'nin düzeltmesiyle birlikte yapılmalı).

### Senkron
- Altyazı başlangıçları kelime zamanıyla karşılaştırıldı (tüm 379 altyazı, ayrıca rastgele 20 örnek):
  - Başlangıç sapması: ortalama −2 ms, ortanca 0 ms; **376 altyazı tam 0 ms**, 3 altyazı 221 ms'ye kadar erken (araç süreyi okuma hızı için başı öne alıyor): #275 −221 ms, iki tane daha −100 ms üstü. Geç başlayan yok.
  - Bitişler: kelime bitişinden ortanca +350 ms sonra; en çok +468 ms; 57 altyazı kelime bitişinden 0–120 ms önce kapanıyor (sonraki altyazıya 80 ms boşluk bırakmak için). Konuşma sürerken en fazla 120 ms erken kesilme; fark edilmez.
- Örnek 20'li liste (altyazı, başlangıç sapması ms): #20 0, #25 0, #30 0, #36 0, #38 0, #45 0, #47 0, #49 0, #78 0, #110 0, #124 0, #166 0, #188 0, #203 0, #215 0, #223 0, #260 0, #275 −221, #299 0, #334 0. Bitiş: +349/+350 (çoğu), −79/−80 (#47, #78, #275).
- **Altyazı kelime başlangıcında tam açılıyor; 100–150 ms öncesinden açılsa göz hazırlanırdı.** Sorun değil, tercih. (Bu zamanlar sesin kendisine göre; `timeline.js` zamanının film sesiyle hizalı olduğunu miksi dinleyerek doğrulamadım, ses sıfır kayma varsayıldı.)

### Görüntüyle çakışma
- **Alt bant (y > 880):** 426 kare tarandı; bantla kesişen ekran yazısı 3 plan:
  - **P129, "Cromwell, 1657": y=878, 68 px**; metnin alt kenarı ≈ 912. Altyazıyla (2 satır) bitişik; sağdan soldan değil ortada. Karede (`m1.png`, alt sol) altyazı kutusuyla yan yana çıkıyor.
  - **P132, "Alexandre Cabanel · Düşmüş Melek, 1847": y=868, 58 px**; alt kenar ≈ 897. Aynı anda altyazı #341 ("Alexandre Cabanel, düşmüş bir meleği şöyle resmetti:") aynı adı veriyor, yani çift okuma + bantta yazı. Karede altyazı kutusu etiketin altına yapışıyor.
  - **P142, "ZAMAN KURYESİ": y=853, 64 px**; alt kenar ≈ 880. Bitiş ekranında altyazı #376–#379 sürerken etiketin hemen altında.
  - Kılavuz "y 90–880" diyor; bu üç yazı sınırda ya da taşıyor. YouTube altyazı kutusu kullanıcı ayarına (büyük yazı) ve TV'de çok büyür; yakın bile olsa iki metin üst üste yığılır. **Öneri: P129 etiketi y≤820, P132 künyesi y≤830 (iki satıra bölünerek), P142 "ZAMAN KURYESİ" y≤820.**
  - Bantta olmayan ama sınıra yakın: P029 "Asıl başkaldıran kim?" y=823/84 px, P130 "Başkaldırı her zaman özgürlük müdür?" y=822/80 px (alt ≈ 862), P124 "kurbağa" y=798/50, P006 "bir destanın okuması" y=798/74. Kabul edilebilir.
- **Çift okuma (ekran yazısı ile altyazı aynı anda aynı cümle):** 142 planın 31'inde ekran yazısı sözcüklerinin ≥%70'i o anki altyazıda geçiyor. Bunların çoğu kasıtlı vurgu (üç-dört kelimelik alıntı: P031, P041, P093, P106, P115); okuma yükü düşük çünkü kısa, tek bakışta eşleşiyor. **Tam cümle çift olanlar (ekranda cümlenin tamamı, altında aynısı):** P139 (iki satırlık "Belki herkesin…" kartı + aynı altyazı), P141 (iki soru kartı), P109, P055, P016, P029, P114, P136, P008. Bu planlarda CC açık izleyici (%38) aynı cümleyi iki kez okuyor; CC kapalı izleyici bir kez. Çözüm olarak altyazı kapatılamaz; bunun yerine bu 9 planda ekran yazısı cümleyi tekrar etmek yerine yalnız **vurgulu tek kelime** ya da başlık olabilir (bu kurgu kurulunun alanı; altyazı tarafı bunu "kabul edilebilir, tekrar nadir" diye değerlendiriyor).
  - P122 (Blake/Lewis öncesi toplu alıntılar): ekranda 6 ayrı alıntı yan yana (“Cehennemde hükümdar olmak…”, “Zihin kendi dünyasıdır.” …) ve altyazı aynı sırada "Şurası doğru: bu destandan akılda kalan sözlerin çoğu, Şeytan'ın sözleri." diyor; burada iki metin farklı, ama göz altyazı ile 6 alıntı arasında bölünüyor. Karedeki yerleşim (üst yarıda, altyazı altta) çakışmıyor; okuma yükü yüksek ama süre yeterli (K08 ~5 sn).
  - **Alıntı tırnağı tutarsızlığı:** P028 ekranda “binlerce hainin arasında sadık kalan tek kişi” tırnaklı, ama altyazı (#74) aynı sözü tırnaksız anlatım olarak veriyor ("Milton onu şöyle anlatır: binlerce hainin arasında sadık kalan tek kişi."). P089 ekranda “zorbaların bahanesi: zorunluluk”, altyazı #219/#220 "zorbaların hep sığındığı bahaneyle, zorunlulukla" (sözler farklı). P125 ekranda “yükseldiği kadar alçalır” tırnaklı, altyazı #320 tırnaksız ("söylemişti: yükselmeye kalkan, yükseldiği kadar alçalır."). İzleyici tırnaklı metni altyazıdaki cümleyle eşler; ikisinin aynı olması ya da ekranda tırnak kullanılmaması gerekir.
- **İlk 10 sn:** #1 (0,90–2,99; “Hangi yana kaçsam cehennem.) / #2 (3,78–5,29; Ben cehennemim.”) / #3 (6,24–10,33, iki satır, 14,4 kr/sn). Açılış iyi: ilk altyazı sesle birlikte açılıyor; tırnak #1'de açılıp #2'de kapanıyor (iki altyazıda, 0,8 sn boşlukla), okunabilir. Ekranda “Ben cehennemim.” yazısı yaklaşık 4,2. sn'de beliriyor (P001, y=150) ve #2 ile çift okuma oluyor; kısa ve kapakla aynı söz olduğu için olumlu.
- **Son 30 sn (1515,43–1545,98, bitiş ekranı P142):** altyazılar #375–#379 ile 1538,14'te bitiyor; son 7,8 sn boş (bitiş müziği, süre). Son altyazı (#379 "Bu hikâyeler hoşuna gidiyorsa, Zaman Kuryesi'ne abone olmayı unutma.", 15,7 kr/sn, 4,33 sn) iyi bölünmüş (iki satır, 31/37 yok; "Bu hikâyeler hoşuna gidiyorsa,|Zaman Kuryesi'ne abone olmayı unutma."). Sorun yalnız yukarıdaki "bir başka|asinin" ve "tek hayalî|karakter" bölmeleri (madde 14) ve "ZAMAN KURYESİ" etiketinin bantta olması. YouTube'un gerçek bitiş ekranı öğeleri (video + abone) sol/sağ üstte çerçeveler üzerine biniyor; altyazı bandı bunlara çakışmıyor (çerçeveler karede yaklaşık y 220–680 aralığında, altyazı bandının üstünde).

## 4. `tools/srt.py` için kural önerileri (dosyayı değiştirmedim)

| # | Yer | Sorun | Öneri |
|---|---|---|---|
| 1 | Satır 42 (`toks[i][-1] in '.?!…'`) | "C." gibi tek harfli kısaltma cümle sonu sayılıyor (#311) | Cümle sonu koşuluna `and not re.fullmatch(r'[A-ZÇĞİÖŞÜ]\.', toks[i])` ekle (ayrıca "Dr.", "St." için küçük bir istisna listesi). |
| 2 | Satır 14–23 `wrap()` maliyeti | Yalnız uzunluk dengesi ve noktalama bonusu var; dile bakmıyor | Maliyete ekle: satır 1 sonunda DANGLE kümesi (`bir, bu, şu, o, en, çok, her, bütün, tek, ve, ama, ki, de, da, ile, için, gibi, kadar, ancak, daha, ne, hem, ya`) +60; satır 1 sonunda `'(ın|in|un|ün|nın…)` tamlayan eki +60; satır 1 sonunda açık tırnak “ ile biten sözcük (ya da “ ile başlayan 2 sözcükten kısa son parça) +80; satır 2'nin başında "ve/ama/ki/çünkü" için −15 bonus (bağlaç ikinci satırı açsın). Noktalama bonusunu 12'den 25'e çıkar. |
| 3 | Satır 4, satır 21 ve 60 `100 * max(0, len - MAXL)` | 43 kr'lık bir satır tüm iyi bölmeleri eliyor | Yumuşak sınır: MAXL 42, 44'e kadar tek karakter başına +15, sonrası +100. |
| 4 | Satır 51–60 (altyazıları parçalara bölme) | Aynı DANGLE ve tamlayan cezası burada da yok; yalnız ",;:" −10 bonusu | Parça sonu DANGLE/tamlayan/açık tırnak ise +80; ",;:" bonusu −10'dan −30'a; parçanın son 4 sözcüğü içinde açık tırnak başlıyorsa ve kapanmamışsa +100 (alıntı açılışı altyazı sonuna sıkışmasın). |
| 5 | Satır 51 (`k = max(1, -(-L // MAXC))`) | Yalnız karakter sayısına göre bölme; 7 sn'lik #203 gibi uzun, yavaş okunan altyazılar tek parça | `k` hesabına süre kriteri ekle: `k = max(k, ceil(süre / 5.5))` ve ":" ya da ";" sonrası bölmeyi tercih et (yalnız süre 6 sn'yi aşıyorsa). |
| 6 | Satır 72 (`nxt - .08`) | Cümle ortasındaki altyazılar arasında 80 ms boşluk titreme yapıyor (54 yer) | Önceki altyazı `[.?!…]”?` ile bitmiyorsa ve sonraki başlangıç aradaki konuşma boşluğu ≤300 ms ise bitişi `nxt`'e (boşluk 0) eşitle; cümle sonlarında 80 ms boşluğu koru. |
| 7 | Satır 67 `CPS = 17` | 3 altyazı 17'yi aşıyor çünkü uzatma payı yok | Sorun değil; #244 ve #167 için başlangıcı 250 ms yerine 350 ms'ye kadar öne alma izni ya da kısa cümlede 18 kr/sn tavanı. En düşük öncelik. |
| 8 | `senaryo.json` `alt` (12 yer) | "Milton'ın" | "Milton'un" yap (`tts` ile aynı). `srt.py` `alt`'ı okuyor; yeniden üretince düzelir. |

Uygularken iki kural çakışırsa (ör. satır uzunluğu ve bağlaç), bağlacın satır başına gitmesi uzunluğa tercih edilir. Her değişiklikten sonra `python3 tools/srt.py` çıktısındaki "UYARI" satırlarına ve 17 kr/sn üstü sayısına bakılmalı.

## 5. Sıralı düzeltme listesi (en çok kazandıran en üstte)

1. **#311/#312 (1260,40 sn) "C." ile "S. Lewis" ayrı altyazılarda.** İzleyici "C." tek başına bir cümle sonu sanıyor. Düzeltme: `srt.py` 42. satır kısaltma istisnası (kural #1); sonuç "Yirminci yüzyılda ise Narnia'nın|yazarı C. S. Lewis," || "Kayıp Cennet'e Önsöz adlı kitabında…". Kazanç: +0,3.
2. **"Milton'ın" ×12 (A05, B09, C02, C04, G02b, I06, J02, K03, K15b, L04, L08, L11)** `alt`'ta "Milton'un" olsun. Seslendirme zaten böyle; Türkçe okuyucu yazım hatası olarak görür (en sık tekrar eden isim). Kazanç: +0,3.
3. **Dile duyarlı bölme (kurallar #2, #3, #4):** 24 satır sonu + 25 altyazı sonu, yukarıdaki 15 örneğin hepsi. Beklenen sonuç: yetim "bir/en/bu/ve" satır sonu ve "Milton'ın|gözleri" ayrılması kalmaz. Kazanç: +0,6 (bölme ölçütü 7,0 → 8,8).
4. **Alıntı açılışı altyazı sonuna sıkışan 6 yer (#81, #170/171, #176, #198, #246, #362)** kural #4'ün açık tırnak cezasıyla; "“Sadık kalanlar gibi|" gibi parçalar kalmaz. Kazanç: +0,2.
5. **P132 künyesi y=868 → ≤830 ve P129 "Cromwell, 1657" y=878 → ≤820, P142 "ZAMAN KURYESİ" y=853 → ≤820** (kare yolları: `.../kurgu2/kare/t1371.13.png`, `t1338.72.png`, `t1530.71.png`; üst üste bindirilmiş: `.../kurul_altyazi/m1.png`). Altyazı bandı (y>880) ile ekran yazısı karışmasın. Kazanç: +0,2.
6. **Tırnak tutarsızlığı: P028, P089, P125'te ekran yazısı tırnaklı ama altyazı tırnaksız ya da kelimeler farklı** (#74, #219–#220, #320). Ekrandaki alıntı işaretlerini kaldır ya da altyazı cümlesiyle aynı yap. Kazanç: +0,15.
7. **#203 (820,91 sn) 7,01 sn:** ":" sonrasında ikiye böl (kural #5) → "Bu sözleri söylerken yüzü üç kez değişir:" || "öfkeyle, kıskançlıkla, umutsuzlukla." Sayım sesle eşleşir. Kazanç: +0,1.
8. **Bitiş ekranı #375/#376 (1515–1525 sn) ve #12/#13 (41 sn)** için yukarıdaki üç altyazılı bölme (kural #2/#4 ile kendiliğinden gelir). Kazanç: +0,1.
9. **80 ms'lik 54 cümle içi boşluk** → 0 ms (kural #6). Titreme kalkar. Kazanç: +0,1.
10. **9 planda ekranda tam cümle çift okuma** (P139, P141, P109, P055, P016, P029, P114, P136, P008): vurgulu tek kelimeye indirmek kurgu kurulunun kararı; altyazı açısından kabul edilebilir. Kazanç: +0,1.
11. **#82'de 43 kr'lık satır:** kural #3 ile ("kendinden üstüne başkaldırana hizmet|etmek; seninkilerin şimdi sana ettiği gibi." / alt satır 42'yi geçmez). Kazanç: +0,05.
12. **#39, #167, #244 (17 kr/sn üstü):** kural #7 ya da ses hızına dokunmadan kabul. Kazanç: +0,05.
13. **Alıntıda ortadaki altyazılar (63 altyazı):** isteğe bağlı: 3 ve daha çok altyazıya yayılan 21 alıntıda devam eden altyazıların başına açılış tırnağı tekrarı ya da araya `…`. Türkçe uygulamada yaygın değil; yalnız Lewis alıntısı (#314–#318, 5 altyazı) için düşünülebilir. Kazanç: +0,05.
14. **G10 (#188) "Gururu, ve cehennemde…":** virgül kaldırılırsa hem altyazı hem tts etkilenir; ses duraklıyorsa bırak. Kazanç: ihmal edilebilir.
15. **Apostrof ve tırnak karakter tutarlılığı (’ ve “ ”):** isteğe bağlı. Kazanç: ihmal edilebilir.

## 6. İyi olan ve korunması gereken
1. **SRT metni `senaryo.json` `alt` ile birebir; hiçbir kelime kaybolmamış.** Tek kaynak, tek doğruluk.
2. **Başlangıç senkronu kelime zamanına tam oturuyor** (376/379 altyazıda 0 ms sapma; konuşmayla altyazı birlikte açılıyor).
3. **Okuma hızı kontrollü:** ortalama 13,7 kr/sn, 17 üstü yalnız 3 altyazı, 20 üstü yok, 1 sn altı yok, üç satırlı altyazı yok.
4. **Kısa sorular tek başına altyazı:** "Onu orada tutan ne?", "Peki ya o gözyaşları?", "Kazanmıştır." tek altyazıda; videonun merak soruları altyazıda da ayrı duruyor (`MERGE` ve "tek kelimelik yetim kalmasın" kuralı işe yarıyor).
5. **Alıntı tırnakları temiz:** her alıntı açılıp kapanıyor, 40 alıntıda sızıntı yok; cümle sonu kapanış tırnağı `.”` biçiminde tutarlı.

## 7. En emin olmadığım nokta
**"Milton'ın" ile "Milton'un" kararı.** `KURUL.md` 180. satır `tts`te "Milton'un", altyazıda "Milton'ın" yazıldığını kayda geçirmiş; bunun bilinçli (örn. "Milton" için "Milton'ın" yazımının okunuşa değil yazıya uydurulması) olup olmadığını bilmiyorum. Türkçe Yazım Kılavuzu'na göre yabancı özel adlara gelen ek okunuşa göre uyum sağlar ve "Milton" Türkçede "milton" okunur; bu yüzden "-un" doğru. Yüzde 85 eminim; başkan Türkçe konusunda başka bir kaynağa sormak isterse bunu yaparsa daha iyi.

İkinci belirsizlik: YouTube altyazı kutusunun gerçek konumu (alt kenardan yaklaşık %5–10 boşluk ve kullanıcı yazı boyutu ayarı) ölçülmedi; "y>880 bandı" yorumunu kılavuz kuralına göre yaptım, kutu simülasyonu (`m1.png`) yaklaşıktır.
