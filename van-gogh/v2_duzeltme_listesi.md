# Van Gogh'a Kim İnandı? v2 düzeltme listesi

Sıralama izleyicinin göreceği farka göre yapıldı. Hassasiyet ve yanlış bilgi maddeleri (5, 6, 7) önem sırasından bağımsız olarak yayından önce şarttır, ama ucuz oldukları için ilk iş gününde biter. Çakışan bulgular birleştirildi. Eleştirmenle şüphecinin önerileri ayrıştığında şüphecinin daha ucuz ya da daha güvenli yolu seçildi; ayrıştığı yerde gerekçesi yazıldı.

## A. Cevap ve doruk planları

1. **I02, "Sonra Jo: … kurye" (561,2–568,6): Jo duvara doğru yükselip kayboluyor, hayalet gibi okunuyor**
   - **Sorun:** `jo_yuru` klibi kendi Blender kamerasında zaten ~8 m uzaklaşıyor. `figurBas` bunun üstüne kendi kaymasını ekliyor (planlar2.js:291, `[760-40t, 1080-30t]`, boy `560-40t`, t saniye). Jo sonunda y≈600'de, ~50 px boyunda ve havada kalıyor. Figür açık gri ve iç çizgisiz. Senaryodaki eylem karede yok: defter kapanmıyor, çekmeceden zarf alınmıyor, kapıdan çıkılmıyor. Kanalın "kurye" imzası olan sarı zarf da yok. Filmin cevabı ölüm sahnelerinin hemen ardından "yükselen ruh" olarak okunuyor.
   - **Düzeltme:**
     - Kod kaymasını kaldır: çapa [700,1000], boy ≈620 sabit.
     - Set kamerasında yeni bir Blender klibi çek: `jo_oda`, `theo_louvre` deseniyle, konum [0,1.6,0], fov 40. Eylem sırası: 0–1,5 sn masada defteri kapatır; 1,5–3 sn çekmeceye eğilir; 3–7 sn sol duvardaki kapıya 3–4 adım yürür (`araclar/hareket`).
     - ODA setine (oda_ciz.js `esya`) sol duvarda uzun bir kapı ve yerde sıcak bir ışık şeridi ekle. Kapının yalnız dikey kasası olsun, yatay çıta olmasın (haç tuzağı).
     - t≈3'ten itibaren ele bağlı bir `{tur:'zarf', renk:'sari'}` nesnesi, nesneMaske ile. Karenin en parlak noktası bu zarf olur.
     - Jo'nun giysi değeri ≈.25–.3, kapı ışığına karşı kontra ışıkla koyu siluet, ayakta temas gölgesi.
     - 'kurye' sözcüğünde eşikte; 'bize'de kapı ışığı kadrajı açar ve I03'e eşleme kesmesi.
   - **Önem:** yüksek. **Emek:** büyük (Blender klibi ve set kapısı). Kayma düzeltmesi tek başına küçüktür ve hemen yapılmalı.

2. **H10, son hikâye anı (531,85–550,41; 18,6 sn): vitrin figürü örtüyor, zarflar ikaz bandı gibi, tablo küçük, müzede Theo duruyor** (üç bulgu birleşti)
   - **Sorun:**
     - Katman hatası: figür SE(.3,0,-7.2)'de vitrinin önünde duruyor, ama vitrin `ust` katmanında çizildiği için figürün üstüne basılıyor. Gövde kayboluyor, bacaklar kutunun altından çıkıyor.
     - Beş sarı KNIFE darbesi gri kenarda şerit gibi duruyor. "Düzeltildi" denen bariyer okuması sürüyor, uzun kutu tabut okumasına da açık.
     - Badem Çiçeği koridor dibinde, zoom 1,9'da bile ~197×185 px. Karenin en parlak noktası kapı (#c4beb0).
     - Figür `theo_dur`: 1890'ların Theo'su 1973 sonrası müzede.
     - Kaynak (DOGRULAMA §6) mektupların saklandığını ve nadiren sergilendiğini söylüyor.
   - **Düzeltme:** vitrin yerine arşiv çekmecesi kullan. Bu kaynakla örtüşür ve A03/D07/H04/G10 çekmecesiyle kafiye kurar. Planı ikiye böl. Komşu planlar H09 ayrıntı ve I01 yakın olduğu için sıra şöyle olmalı:
     - **H10a geniş (~531,9–540):** salon figürsüz. Badem Çiçeği sol yan duvarda büyük: x=−GX, z −10…−14, y 1,2–3,4, kadraj yüksekliğinin ≥ %35'i. Kapı ışığı koyulaşır; tek renkli ve en parlak bölge tablo olur.
     - **H10b ayrıntı (~540–550,4):** tablonun hemen altındaki duvar dolabının arşiv çekmecesi. Çekmecenin içinde 5–7 adet `{tur:'zarf', renk:'sari'}` nesnesi, kapaklı, dağınık açılarla, her biri nesneMaske ile. Tablonun alt kenarı kadrajın üstünde kalır, böylece iki motif aynı karede buluşur. 'badem' sözcüğünde (545,7) tablo örtüsü ile zarf örtüsü birlikte açılır; 'duruyor'da çekmece yavaşça kapanır (`cekmeceAc`, madde 4).
     - Seslendirme değişmez.
   - **Yedek yol (vitrin korunursa):** ince dört ayaklı, eğik cam kapaklı masa vitrini. Gövde yok. Vitrin kameraya yaklaşır (z ≈ −4,5…−5). Cam altında zarf nesneleri. Figür yoksa daha iyi; konacaksa çağdaş, şapkasız ayrı bir klip, x ≥ 1,4.
   - **Son adım:** tam boy karede tabut, bariyer ve mezar taraması.
   - **Önem:** yüksek. **Emek:** orta.

3. **Kanca (0–30 sn): A01b, A02 ve A03 aynı kare; dal geç ve kısa görünüyor; '651 / 39' yok; Jo ekilmiyor; A02'de 5,4 sn boşluk** (üç bulgu birleşti)
   - **Sorun:**
     - 5,5–30 sn arasında üç plan aynı tepe çekmece kompozisyonunda (kamera z 1,35/1,02/1,6). Ölçek kuralı etikette tutuyor, karede tutmuyor.
     - Kapak B'nin vaadi (gri yığından çıkan dal) 11,4. saniyede başlıyor ve tam dal yalnız ~0,2 sn kalıyor. Dal sarı zeminde sönük.
     - Senaryonun istediği '651 / 39' yazısı yok. 39'luk deste tek bir gri zarf gibi okunuyor.
     - A02'de zarflar 17,26'da bitiyor, gri yaprak kalkışı 22,62'de başlıyor: 5,4 sn eylemsiz.
     - A03'te Jo yok. Kod yorumu "kadın gölgesi" diyor, ama durumda figür de gölge de yok. Doruğu taşıyan kişi kancada ekilmemiş (Ran ve Medici dersi), Jo'nun ilk görüntüsü 88,9. saniyede.
   - **Düzeltme:**
     - **A01b:** dal tetiği 'zarflarla'ya (8,52) çekilir, büyüme 1,2 sn olur. Yığın gri başlar; 'sarı' (8,16) sözcüğünde mDaire örtüsü yığına yayılır. Dal ~9,7–13,3 arasında tam görünür. Daha güçlüsü: dal A01'in son saniyesinde masadaki zarflardan uzanmaya başlar.
     - **A02, gerçek orta plan:** kamYol z ~.8, y ~560; masa üstü, lamba ve çekmece birlikte görünür. Gri deste `yigin(39,{renk:'gri', w:200, h:120, dx:20, dy:12, kat:1.5})` ile kalın bir blok olur. 'altı'da (15,50) `yazi('651')`, 'otuz'da (20,02) `yazi('39')`; her biri ≤ 4 sn ve y < 880. Zarf düşüşü i*.09 ile 'mektup'a (16,8) kadar yayılır; gri kalkış 'kaldı'da (20,6) başlar.
     - **A03, gerçek ayrıntı:** alçak yan kamera, ör. [1250,700,1.9]→[1150,720,2.0]. `FIG.jo_dur` ~1400 px, sağ kenardan kırpılmış omuz ve kol. Koyu siluet, toplu saç, omzun altında koyu ciltli bir defter nesnesi. 'iki'de bir sarı zarf yukarı kalkıp kadrajdan çıkar (maskeye eklenir). 'ikincisi'nde çekmece kapanır (`cekmeceAc` 1→0, ince ışık yarığı kalır). 'sonda'da figür sağa çıkar, sonra mevcut expo kararması gelir.
     - Kapağın vaadi ve senaryo yeniden karşılaştırılır.
   - **Önem:** yüksek. **Emek:** orta.

4. **D07, H04 ve defter: Jo'nun eylemleri hiçbir karede olay değil** (A03 ve I02 dışında kalan kısım)
   - **Sorun:** D07'de "Jo ilk kez o çekmeceyi açar" (açar@227,5) ve H04'te "mektupları saklar" (saklar@480,9) cümlelerinde el, gölge ya da hareket yok. set_masa.js'te çekmece ikili (açık/kapalı), kayan kapak yok. A03→D07 "aynı kare şimdiki zamanda" eşlemesi bu yüzden çalışmıyor.
   - **Düzeltme:**
     - set_masa.js'e `cekmeceAc: 0..1` ekle: CEKMECE üstünde kayan, KNIFE darbeli koyu ahşap ön panel. nesneMaske aynı oranla daralır, sarı yalnız aralıkta görünür.
     - **D07:** A03'ün kamerası, aynı Jo omzu ya da lamba yönünde masaya izdüşen koyu gölgesi (figurDarbe, düşük alfa; daha ucuz ve daha temiz) ve aynı defter. 'açar'da `cekmeceAc` 0→1, gri yığın görünür.
     - **H04:** 'saklar'da aynı gölge çekmeceyi iter (1→.08), sarı yarık daralır.
     - Defter Blender kliplerine eklenmez. A03, D07 ve I02'de nesne olarak tekrarlanır; H03'teki açık defterin yanına aynı koyu cilt konur.
   - **Önem:** yüksek. **Emek:** orta. `cekmeceAc` madde 2 ve 3'te de kullanılır, önce bu yapılır.

## B. Hassasiyet ve yanlış bilgi (yayından önce şart)

5. **G09, H07 ve H08: görünmeyen ağacın gölgesi tarlada mezar tümseği gibi duruyor**
   - **Sorun:** ağaç gölgesi kurye/lib/tablo_ciz.js `tarla()` içinde (`tgolge`, A=[1318,748], B=[1780,1230]). `agac:false` yalnız ağaç katmanını gizliyor. H07 ve H08'de "küçük mezarlıkta birlikte yatıyorlar" cümlesinde, Jo'nun yanında tek bir koyu tümsek görünüyor: taze mezar tuzağı.
   - **Düzeltme (ortak dosya, ana oturum yapar):**
     - `tarla(R, patika, o={})` içinde gölge yalnız `o.golge !== false` olduğunda çizilir. Böylece kurye filmi etkilenmez.
     - Gölge `TB.tarlaGolge(R)` olarak ayrı dışa aktarılır.
     - set_disari.js: tarla katmanı `TB.tarla(R,[],{golge:false})` olur. Ağaçtan önce yeni katman: `{ad:'tgolge', d:.45, ciz:TB.tarlaGolge, alfa:(t,du)=>du&&du.agac===false?0:1}`.
     - `.parts*/` önbelleği silinir. Üç plan tam boy karede yeniden taranır; boş kalan sağ önde yeni leke ya da sıralı yuvarlak leke oluşmamalı.
   - **Önem:** yüksek. **Emek:** küçük.

6. **Şövalenin varsayılanı otoportre: Vincent yaşarken G02 ve G05 anma köşesi gibi okunuyor**
   - **Sorun:** set_oda.js:35'te varsayılan `'oda_otoportre'`. Tablo belirtmeyen dokuz oda planında (C06, D01, D06, G01, G02, G05, G10, G11, I02) şövalede gri, çerçeveli bir erkek portresi duruyor: siyah-beyaz anma fotoğrafı gibi. Figürler ona bakıyor, ölüm G09'dan önce ele veriliyor. Dokuz tekrar da yüzü sıradanlaştırıyor.
   - **Düzeltme:** tek satır, varsayılan `'oda_aycicek'` olur (yüklü). Portre yalnız A01 ve B06'da açıkça kalır. On iki oda planı `PLAN=1 SADECE=... node van-gogh/tools/kare.js` ile yeniden çizilir. Gri Ayçiçekleri'nde halka tarama ya da hedef tahtası okuması olmadığına bakılır.
   - **Önem:** yüksek. **Emek:** küçük.

7. **Kapak A "TEK KİŞİ İNANDI": filmin kendi tezine ve olguya ters, başlığın sözcüğünü tekrarlıyor**
   - **Sorun:** film 0:25'te "iki cevabı var" diyor, I01/I02'de iki kişi sayıyor, F02'de Aurier'yi, F06'da Anna Boch satışını gösteriyor. "Tek kişi" yanlış bilgi. "İNANDI" başlıktaki sözcüğü tekrar ediyor.
   - **Düzeltme:** görüntü aynı kalır, kapak.html'de A sürümünün `o.satir` değeri "SEKİZ YIL HER AY" olur. Bu I01'in cümlesi ("sekiz yıl boyunca her ay bir zarf"), B04'te ilk dakikada karşılanıyor. Seçenek: "KARDEŞİNİN MAAŞIYLA". yayin.md:14 güncellenir. Kapak test seti (246/168/120, odak.py, süre rozeti) yeniden çalıştırılır.
   - **Önem:** orta (yanlış bilgi). **Emek:** küçük.

8. **C08 (158,8–166,9): Yatak Odası, Ekim 1888'de Theo'nun Paris odasında ve kırpılmış**
   - **Sorun:** tablo Arles'daydı ve Paris'e 1889'da gitti. Pencerede Montmartre bacaları var. Senaryo "gri bir Arles odası" istiyor. Yatay eser dikey SOVALE'ye ortadan kırpılarak basılıyor (film_t.js:77).
   - **Düzeltme:** en ucuzu, C08 Paris'te kalır, planlar2.js:77 `tablo:'oda_otoportre'` olur (1887'den beri Paris'te, doğru). Masaya katlı bir `kagit` ve üstünde küçük gri bir yatak odası eskizi konur; çizimden önce VGM 705 kontrol edilir. Arles istenirse C08, C07'nin tb_yatak sahnesinden geri çekilme olarak kurulur (z 1,18→~.8, pay kenarı gri duvar). Genel önlem: tabloCiz'e `sigdir` (contain) dalı eklenir.
   - **Önem:** orta. **Emek:** küçük.

## C. Figür ve sahne okunurluğu

9. **Figürler zemine basmıyor, Jo açık gri, yakın planda kil manken** (G05, D01, G02, B03, E04, H08)
   - **Sorun:** figurBas temas gölgesi çizmiyor. G05'te ayaklar y≈990–1000'de, zemin y≈1040'ta başlıyor. Jo bütün planlarda iç çizgisiz açık gri bir koni; H08'de gökle aynı değerde. Bu, ana figür koyu siluettir kuralının ihlali. G02'de (900 px) eller kopuk silindir.
   - **Düzeltme:**
     - figurBas'ta figurDarbe'den önce ayak noktasına yatay DAB elips: genişlik ≈ .6×boy/4, alfa .4.
     - Ayakları zemin çizgisine indir (y≈1050) ya da ODA zeminini yukarı al.
     - `jo_dur` ve `jo_yuru` kliplerinde hava ≈ [.08,.07,.07]. Jo'yu biçim taşır (etek, topuz), açıklık yalnız kenarAlfa'da kalır.
     - G02 ve B03'te eller kadraj dışında: belden yukarı kırp ya da Blender'da eller arkada pozu. E04'te değişiklik az.
     - D01'e oturan klip gerekmez (not "yan yana" diyor, oturmayı istemiyor).
   - **Önem:** yüksek. **Emek:** orta.

10. **Ölüm anı: G10'da Theo seçilmiyor ve renk yok; G11 G10'un aynısı; G11'de lamba sesi son sözcüğü örtüyor** (görüntü ve ses bulgusu birleşti)
    - **Sorun:**
      - G10'da `theo_oku` [1260,1160]'ta, kadrajın dibinde bir tümsek.
      - Senaryonun "en güçlü Theo karesi"ndeki sarı zarflar yok, plan tamamen gri.
      - G11 aynı boş oda; Theo zaten görünmediği için yokluk okunmuyor.
      - mix.py:55'te lamba −18 dB ile en yüksek efekt. Düz hışırtı, 444,3–447,3 arası. "yaşındaydı"da sesten ~3,5 dB yüksek, 1–4 kHz bandında sinyal-gürültü ≈0 dB. Alev 446,1'de sönüyor, ses 1,2 sn daha sürüyor ve bilinçli sessizliği dolduruyor.
    - **Düzeltme:**
      - **G10:** kamYol([1150,700,1.2],[1170,720,1.3]); baş ve omuz alt üçte birde, sırttan. Dirseğin yanında, lamba ışığında sarı zarf yığını (yigin + nesneMaske). Kamera omuz üstünden yığına kayar; Theo'nun yazdığı zarf gri kalır.
      - **G11:** G10'un ilk kamera noktası birebir. Theo yok, yığın yok, ışık 'kis'. Ayrıntıya kayış plan içinde olur.
      - Alev cümleden sonra söner: planlar2.js'te `ts = CUES G11 sonu + .3` (≈445,8–447,4).
      - Ses: mix.py:55 `koy('lamba', CUES['G11']['e']+.3, -27, fi=.15, fo=1.2)`. Efekt `EF['lamba'][:int(1.6*SR)]` ile kesilir ve doğrusal söner.
      - score.py:196'da SUS başlangıcı `CUES['G11']['e']+.2` olur.
      - Ölçüm: 444,4–445,5 arasında 1–4 kHz bandında ses efektten ≥ 12 dB yüksek olmalı.
      - G09 ile H07 kafiyesi bilerek kurulmuş, dokunulmaz.
    - **Önem:** yüksek. **Emek:** orta.

11. **Jo'nun bölümü (H) görüntüde yok: H01 15,5 sn boş tren, H05 1905 sergisi yine gri koridor**
    - **Sorun:**
      - H01 merak sorusu bir kadını soruyor ("kalan bir kadın ne yapar?"), ekranda üçüncü kez aynı tren var.
      - H05'te maske ve figür yok, kare B02'nin aynısı.
      - Filmin renk kuralının en büyük ödemesi (G09'dan beri ilk geniş renk dönüşü) kayıp.
    - **Düzeltme:**
      - **H01:** set_disari ev ya da kapı, `agac:true`, gündüz. `sandik()` ile 2–3 sandık. Duvara sırtı dönük 3–4 çerçeve: KNIFE dikdörtgen, içinde çapraz çıta yok. Eşikte `FIG.jo_dur`, sırttan, koyu değerli (madde 9).
      - Bebek için bohça konmaz: sırttan bakışta kucak görünmez, karın ya da baş yanındaki leke hamilelik veya hale okunur. Bebeği ses taşır.
      - 'tablolarla'da sandık aralığındaki küçük mRect renklenir. Tren istenirse 'Hollanda'ya'da ≤ 3 sn'lik bir ara olur.
      - **H05:** cerceveListesi('dolu')'dan ilk 8–10 çerçeve için mRect. A('H05@büyük')'ten (≈490,6) başlayarak yakından uzağa 0,2–0,25 sn arayla açılır. Çerçevelere tabloCiz ile CC0/PD-Art Van Gogh'lar basılır; tablolar adlandırılmaz ve "1905 listesinde vardı" iddiası kurulmaz. Arka kapı aydınlığına küçük bir `jo_dur`.
      - B02'den ayırmak için kamera yan duvar boyunca kayar. `donem` parametresi ancak zaman kalırsa eklenir.
    - **Önem:** yüksek. **Emek:** orta.

12. **Bebek hiç görünmüyor: G02'de "beşiğin başında" cümlesinde iki adam tuvale bakıyor; G04'te üç kişi var** (iki bulgu birleşti)
    - **Sorun:** bebek altı yerde seste var, görüntüde yok. G02 sessiz okumada "tabloya bakan iki adam", madde 6 ile birlikte "portre önünde ağlayan iki adam". G04'te "Theo, Jo ve bebek" cümlesinde üç yetişkin var. H10'daki "bebek büyür" ödemesi görüntüde kurulmamış bir şeye dayanıyor.
    - **Düzeltme:** önce nesne yolu, çünkü daha ucuz ve kefen, hale ve hamilelik riski taşımıyor.
      - **G02:** şövale çıkar. İki erkeğin arasına, alt üçte bire açık ahşap alçak bir kenar ve üstünde tığ işi örtü (DAB ağ dokusu, halka tarama yok, sıcak gri). Kapalı koyu kutu olmaz.
      - G02'de 'şaka'da (364,0) örtünün ucu kıpırdar, kapı eşiğindeki `jo_dur`'un omzu 2–3 kare sarsılır (ayak y ±6 px).
      - **G04:** Jo'nun göğsüne açık gri tek bir yatay DAB (~18×10 px), figurBas'tan sonra. Bu boyda hale ya da hamilelik okunmaz.
      - **F03:** son 1,5 sn'de kâğıdın yanında aynı örtünün katlı köşesi. Örtü F03, G02 ve H10b'yi (çekmecenin köşesi) bağlar.
      - **G05:** ses "hastalanır" derken bebek gösterilmez.
      - `jo_bebek_dur` (bebek omuzda dik, küçük koyu baş; yatay beyaz sargı yok) ancak bu yol yetmezse açılır.
      - Her kare tam boy taranır: kefen, hale, hamilelik, namaz safı.
    - **Önem:** orta. **Emek:** küçük (nesne yolu) ya da büyük (klip).

## D. Tempo ve eşleme

13. **5 sn'yi aşan eylemsiz aralıklar** (G07 12,2 sn; H09 11,6; E01 11,7; G02 11,8; F02 ~8,5; H06 ~9,7; F07 ~7,2; D01; G05 ve D07'de yalnız kamera)
    - **Sorun:** donuk plan kuralı ihlal ediliyor, planların çoğu duygusal doruğun yanında. Telefonda yavaş zoom hareket sayılmıyor.
    - **Düzeltme:** var olan parametreleri sözcüğe bağla.
      - **G07:** kâğıdın `yazi` değeri 0'dan büyür, 'bitirmez'de yarıda kalır. Kalem kalkıp masaya bırakılır (`duser` yayı). 'konuşturabiliriz'de expo t'ye bağlanır, ışık kayar.
      - **H09:** yığın sayısı t'ye bağlanır, sayfalar tek tek konur. 'öldüğünde' kalem durur, expo düşer. 'İngilizce'de sarı deste belirir.
      - **F07:** `satirR` 'deftere'de 2→3 olur. '400 fr.' 'satış' sözcüğüne kayar.
      - **H06:** 'girişini'de üstteki cilt `acikdefter`e döner. Zarf 'Theo'ya' sözcüğünde çıkar.
      - **F02:** 'övgü'de sayfa çevrilir.
      - **E01:** `vincent_yuru` (dongu:false) ile bahçe yolunda uzak bir siluet; şövale gerekiyorsa `araclar/hareket` taşıma pozu.
      - **G02:** madde 12'deki sarsılma.
      - **G05:** 'zam'da Theo'nun yanına zarf nesnesi girer.
      - **D01:** 'nişanlanır'da Jo bir adım yaklaşır.
      - **D07:** madde 4'teki çekmece açılışı.
      - Render'dan önce plan kodu ve timeline.js'ten "son olay → plan sonu" aralığını çıkaran betik (`cumhuriyet/tools/donma.py` uyarlanır); > 5 sn olanlar listelenir.
    - **Önem:** yüksek. **Emek:** orta.

14. **Para → tuval → zarf eşlemesi kopuk: G08 G06'nın tablo hareketini tekrarlıyor, I01 durağan**
    - **Sorun:** senaryo G08 için "EŞLEME KESMESİ" istiyor: B04'ün eli ve açısı, para yerine rulo bir tuval. Kod ise tam kare `tb_selvili_tarla` ve 12 sn önce G06'da yapılan gri→renk hareketinin aynısı. I01'de (filmin ilk cevabı) zarf baştan kapalı. 'her ay bir zarf' ve 'sergilere giden tablolar' sözcüklerinde ekranda bir şey olmuyor, eylemsiz aralık ~8 sn.
    - **Düzeltme:**
      - **G08:** sahne 'masa', B04 kamerası kamYol([960,400,1.3],[960,400,1.36]). Gri zarf (980,420), solda sarı yığın (`yigin(8,{x:560,y:420})`). B04 yörüngesiyle (lerp 620→980) banknot değil rulodan açılan bir `kagit` tuval girer. 'tuvallerin'de bu tuvale Selvili Buğday Tarlası basılır ve nesneMaske ile renklenir (Auvers değil, senaryonun tablosu). 'payın'da sarı yığının maskesi açılır, kısa bir lamba parlaması (expo/lightCol).
      - **I01:** B04 nesne fonksiyonu tek döngü olarak çalışır. 'her ay bir zarf'ta banknot girer ve zarf kapanır (yuz 'arka'→'on'). 'sergilere giden tablolar'da sırtı dönük bir çerçeve kayarak çıkar. 'gece treni'nde mevcut iki bilet düşer.
    - **Önem:** orta. **Emek:** küçük ya da orta.

## E. Mekân ayrımı ve ölçek

15. **Filmin %37'si (26 plan, 223,8 sn) aynı tepe açısından aynı masa; ölçek ve mekân karede ayrılmıyor**
    - **Sorun:** set_masa.js'te tek kamera ve tek ışık var. Plan yorumlarındaki sabah, gece, gün ışığı farkları kareye yansımıyor. Senaryodaki Arles kapı eşiği (C02) ve kapı altından giren telgraf (D02) masaya çizilmiş.
    - **Düzeltme:**
      - `bitir`'e `du.isik` ekle: gece lightCol [1,.8,.55] ve expo .9; gün [.95,.97,1] ve ışık sağ üstten; bugün soğuk mavi-gri ve düşük vinyet. Işık merkezi `du` ile kayar.
      - Her plana kendi `kamYol`u (F03'teki `kamera:F3k` örneği).
      - C02 ve D02 ODA setinin döşemesine taşınır: alçak açı, kapı altından ışık şeridi, kâğıt tahta üstünde kayar.
      - Mekân başına tek ayırıcı nesne: Paris'te hokka; Auvers'te (G07) pencere gölgesi ızgarası; Hollanda'da (H03, H09) açık ahşap `du.ton`; bugün (I01, I03, I04) damarsız soğuk yüzey.
      - C07b (2,6 sn) kaldırılır. Ardışık masa çiftlerinde en az biri farklı ışık ya da ölçek alır.
      - Kurgu özeti yeniden basılıp gözle denetlenir.
    - **Önem:** orta. **Emek:** orta.

16. **Arles odasında Paris bacaları (C08); B06→B07 aynı ölçek**
    - **Sorun:** C08'de Arles'tan yazan Vincent var, ekranda Theo'nun Paris odası. Kardeşlerin ayrı şehirlerde olması görüntüde kayboluyor. B06 orta → B07 orta; senaryo B07'yi geniş istiyor.
    - **Düzeltme:**
      - **B07:** olcek 'genis', kamera [960,560,1.0]→[960,570,1.06], figür boyları aynı kalır.
      - **B08** aynı anda 'orta'ya alınır (senaryo da öyle istiyor: kompartıman içi). Yoksa B07–B08 iki geniş olur.
      - Arles odası istenirse ODA setine `durum.pencere='arles'`: alçak kiremit çatı ve tek selvi, 'ogle' ışığında keskin sıcak güneş lekesi, lamba ve masa yok, sandalyede katlı mektup. Madde 8'de ucuz yol seçilirse bu ikincil kalır.
      - D01 ve D06'ya dokunulmaz (Paris, tutarlı).
      - Plan listesinde ardışık aynı ölçek otomatik denetlenir.
    - **Önem:** orta. **Emek:** küçük (ölçek), orta (Arles varyantı).

17. **E04 (267,2–274,1): Theo İrisler'in içinde duruyor, Saint-Rémy bahçesi okunuyor**
    - **Sorun:** sahne çerçevesiz `tb_irisler` ve mTam(1). Ses Paris'teki bir sergiden söz ediyor, Theo ise Saint-Rémy'ye hiç gitmedi.
    - **Düzeltme:** sahne 'salon', `duvar:'seyrek'` (C03 ve F08'in salonu). İrisler tabloCiz ile duvarda çerçeveli, ikinci tuval sırtı dönük ve renksiz. Maske yalnız tuval dikdörtgeni (mRect). `theo_dur` sağda, omuz üstü, koyu. Kamera tuvalden salona geri çekilir, ör. kamYol([tuval merkezi,1.35],[960,540,1.1]). Ölçek 'yakin' kalır (E03d geniş).
    - **Önem:** düşük. **Emek:** küçük.

## F. Ses

18. **Zarf sesleri görüntünün 1,35 sn gerisinde; A01'deki "bir zarf daha" yanlış sözcüğe bağlı; D07b'nin son vuruşu E01'e taşıyor**
    - **Sorun:** zarf.mp3'ün vuruşu dosyanın 1,35. saniyesinde. `W('A01','bir')` ilk 'bir'i (3,82, "bir yazı masası") alıyor. "her hafta bir zarf daha ekleniyor" (10,7–11,4) ne duyuluyor ne görülüyor; A01b açıldığında zarf çoktan düşmüş (te = −1,66). A02'de ses aralığı .45, görüntü aralığı .12. D07b'nin son vuruşu 242,17'de hastane bahçesine düşüyor.
    - **Düzeltme:**
      - `EF['zarf'] = EF['zarf'][int(1.25*SR):]` (fi=.02).
      - A01: planlar.js:110'da `te = A('A01@bir#1') + .25`; mix.py:50'de `koy('zarf', W('A01','bir',1)+.25+.6-.05, -20)`. Ses iniş anına bağlanır.
      - A02: her üçüncü Y2 zarfı `S('A02')+i*.12-1.2+.5`, −28…−34 dB arasında değişen kazançla; 13,28'den önce inenler atılır.
      - D07b: her ikinci zarf `ts+i*.28+.45`, yalnız `S('E01')-.3`'ten öncekiler.
    - **Önem:** orta. **Emek:** küçük.

19. **Nesne olaylarının sesi yok; ayrıca kaldırılan beşiğin sesi hâlâ çalıyor**
    - **Sorun:** mix.py:54'te besik.mp3 F03'te (doğum mektubu) ve G01'de −26 dB çalıyor, oysa beşik koddan kaldırıldı. Seyirci mektubun üstünde beşik sesi duyuyor. B01b pusula, D02 telgraf, D04 biletler ve H06 ciltler, nesnenin tek hareketli şey olduğu yakın planlarda sessiz.
    - **Düzeltme:** kredisiz, yalnız mix.py.
      - Satır 54 `koy('kalem', W('F03','Vincent')-.1, -26)` olur; G01 çağrısı silinir; 'besik' EF listesinden çıkar.
      - zarf.mp3'ün ilk ~.35 sn'si np.interp ile ×.85 (cilt için ×.7), 8 ms fade-in:
        - B01b `W('B01','pusula')+.1, -26`;
        - D02 `W('D02','ertesi')`, d=1.2, fi .1, fo .4, −26 (kapı vuruşu yok);
        - D04 `CUES['D04'].s + .8 / 1.2`, −28;
        - H06 `+.7/1.2/1.7`, ×.7, −24;
        - I03 `S('I03')+.5`, −28.
      - D07'de çekmece için en çok tek bir .4 sn tahta kayması (numpy bant geçiren gürültü 300–900 Hz, −30).
      - Tren düdüğü sentezlenmez; D03–I01 bağı istenirse mevcut tren.mp3 `W('I01','gece')`'de −34 dB.
      - Her yeni vuruş telefon bandında sesten ≥ 12 dB aşağıda kalmalı.
    - **Önem:** orta (beşik sesi kalıntısı yüksek sayılmalı). **Emek:** küçük.

## Uygulama sırası ve kapanış denetimi

- **1. gün (küçük, engelleyici):** 5, 6, 7, 8, 19'daki beşik sesi, 1'deki kayma düzeltmesi, 16'daki B07/B08 ölçeği, 17, 18.
- **2. gün:** set_masa.js'e `cekmeceAc` (4), ardından 3, 2, 10, 14.
- **3. gün:** Blender `jo_oda` klibi ve oda kapısı (1), 9, 11, 12, 13, 15.
- **Ortak dosyalar** (kurye/lib/tablo_ciz.js, set_*.js, planlar*.js, mix.py, score.py) yalnız ana oturumda değişir. Ses kararları (10, 18, 19) render'dan önce biter.
- **Kapanışta:**
  - kurgu özeti yeniden basılır ve sessiz okuma testi yapılır;
  - değişen her plan tam boy karede hassasiyet listesine göre taranır;
  - `alt_bant.js` ile y > 880 ölçülür;
  - ardışık ölçek denetimi ve donma betiği çalıştırılır;
  - kapak A ve B'nin vaadi senaryo ile yeniden karşılaştırılır.
