# ŞARLKEN — Yönetmen Notları (bölüm bölüm çekim önerileri)

Bunlar **öneridir**: daha iyi bir görsel fikrin varsa uygula; ama (1) anlatının söylediğinin ötesine geçen olgu koyma, (2) sayı/ad söylendiği anda gelsin, (3) rivayet/belirsiz yerlerde damga olsun, (4) her cümlede görsel olay olsun, (5) çekim türlerini harmanla. Teknik sözleşme: `STIL_REHBERI.md`. Cümleleri/çapaları `python3 preview_chapter.py cK --script` ile gör.
`[YENİ]` = senin (ya da lab'ın) yazması gereken yeni varlık. Ekrana koyacağın sayı/olgu için önce `arastirma/*.md` ve `kaynaklar.md` (varsa) içine bak.

Genel tasarım ilkeleri: her bölüm **tek bir dominant renk/ışık** taşısın (aşağıda "ton"), bölüm başı güçlü açılış, bölüm sonu vurgu çekimi. Kişi ilk kez anılınca madalya + levha. Aynı bilgi iki kez gösterilmez. Her bölümde en az 1 diorama, 1 harita, 1 belge/alıntı, 1 sayı/grafik, 1 madalya çekimi (kısa bölümlerde mümkün olduğunca).

---
## c0 — Soğuk açılış (46 sn) · ton: sıcak altın/kara, merak
Mevcut (`scenes_c0.py`) çalışıyor; **parlatma** gereği: 12 sn'lik tek salon çekimi bölünmeli (s2 geniş itme → s3 ortada yürüyen yaşlı figür, kamera onu izler → s4 baston + genç prensin omzu yakın plan). Kimlik gizli kalır (isim levhası s8'den önce yok). **s4'te baston YOK (kaynaksız): 'Kolunu genç bir prensin omzuna dayamış'.** Haritadaki "İSPANYA" etiketi sol alt tarih levhasıyla çakışıyor (levhayı yukarı al ya da etiketi kaydır). "Yakın" salon çekiminde figürler kaba görünüyor → kamerayı figürlerden çok tahta/pencereye ve mimariye kaydır ya da figür-lab'ın yeni figürlerini kullan.

## c1 — Dört Tahtın Çocuğu (117 sn) · ton: süslü hanedan altını → hüzünlü (Juana) → fırtına mavisi
- s1 (24 Şubat 1500, Gent): Avrupa → Flandre zoom-in; GENT şehir işareti; tarih damgası "24 ŞUBAT 1500".
- s2 Juana & Filip: `medals` (juana, filip) + aralarında yüzük simgesi; plaka "JUANA · Kastilya Kraliçesi", "FİLİP · 'Yakışıklı' · Burgonya Dükü".
- s3 Dört büyükanne-büyükbaba: **soy ağacı** (`tree`): üstte maksimilyan, maria_burgonya, fernando, isabel_kastilya → ortada filip, juana → altta karl_genc. "BURGONYA, AVUSTURYA, ARAGON, KASTİLYA" etiketleri sözcükler söylenince (bölge renkleri) belirsin; ardından haritada 4 bölge sırayla yansın (`karl_kendi` parçaları).
- s4 "Beş ay sonra küçük bir bebek öldü ve yol açıldı": [YENİ] "miras yolu" çekimi: uzakta taç → Karl'a giden kesikli yol; "5 AY" sayacı; kuzen bebek (soluk gri düğüm) sönünce yol sürekli çizgiye döner. (Bebeğin adını söyleme; anlatı söylemiyor.)
- s5 "evlilikle ve ölümle": `iconrow` iki simge (ring "EVLİLİK", skull "ÖLÜM"); sözcüklerle belirsin.
- s6 Burgos 1506: harita zoom BURGOS + `dip` geçiş; filip madalyası onyx; "6 YAŞINDA".
- s7–s9 Juana/Tordesillas: [YENİ] **"kule" diorama**: küçük parmaklıklı pencere, içeride tek başına siluet (peçeli kadın, mum ışığı, soğuk ay ışığı dışarıda); kamera pencereye çok yavaş yaklaşır. s8 `counter` "46 YIL" (alt yazı "1509 – 1555"); `timeline` ile 1509→1555 vurgulu aralık. s9 soru işareti simgesi + `TARTIŞMALI` damgası; iki simge: "DELİLİK?" / "SİYASET?" (question ↔ crown).
- s10 Mechelen: harita MECHELEN + margareta madalyası (plaka "MARGARETA · Hala"); altyazı yok ama "ANA DİLİ: FRANSIZCA" etiketi (sözcük "Fransızcaydı" anında).
- s11–s12 Dört dil sözü: `quote` kartı 4 satır (Tanrı / kadınlar / erkekler / at) her satırda küçük simge (cross, ring, sword, [YENİ] horse); `RİVAYET` damgası "Rivayete" sözcüğünde. s12: `timeline` 1558 → 1601 aralığı "43 YIL" vurgusu + `BELGE YOK` damgası (önce arastirma/A1 ile doğrula: ölümünden 43 yıl sonra = 1601).
- s13 1516 Fernando'nun ölümü: fernando madalyası (onyx), `dip`; sonra iki taç ("KASTİLYA", "ARAGON") — `emblem` + harita `ispanya`; "tutsak annesiyle birlikte" → juana küçük madalya yanında.
- s14 **Tazones fırtınası** [sahne-lab: `sea`, mood="storm"]: gemiler savruluyor, yağmur, şimşek parlamaları; harita rotası Zeeland → İspanya, hedef SANTANDER (kesikli, soluk) vs gerçek TAZONES (parlak) — iki nokta ve sapma oku.
- s15 17 yaşında kral: karl_genc madalyası "17 YAŞINDA · KRAL"; küçük limanda köylüler (kalabalık siluet) — başı hafifçe öne eğik; üzerlerinde soru işaretleri.
- s16 Valladolid Kortesi 1518: `doc` (başlık "VALLADOLID KORTESİ · 1518", satırlar "Kastilyacayı öğren." / "Yabancı danışmanlarını gönder.", mühür). Bölüm sonu vurgusu.

## c2 — Taç Satılık (87 sn) · ton: para altını, entrika (koyu yeşil-altın), parıltılı
- s1 Maksimilian ölümü: maksimilyan madalyası (1459–1519), onyx kenar, `dip`.
- s2 Yedi seçmen: [YENİ] "7 koltuk" çekimi (yedi taç/şapka halka içinde sırayla yanar; "YEDİ SEÇMEN"). Seçmenlerin adları anlatıda yok → adsız.
- s3–s4 Rakipler: `medals` karl_genc vs fransuva (+ `vs`), ardından henri8 küçük üçüncü (royal/crimson) ve "GÖSTERİ" etiketi.
- s5 Pazarlık: terazi simgesi + paralar yığılır.
- s6 **850.000 florin**: [YENİ] **"sayım odası" diorama** (masa, defter, mum, para yığınları, katipler siluet) + `counter` 850.000 FLORİN (alt: "yaklaşık").
- s7 543.000 Fugger: `stacked` (543.000 Fugger + kalan 307.000 "DİĞERLERİ", toplam 850.000) + fugger madalyası + harita AUGSBURG.
- s8 Frankfurt 28 Haziran 1519: harita zoom FRANKFURT + tarih; yedi oy simgesi tek tek altına döner → "7 / 7".
- s9 (yeni metin: "seçmenler parayı aldı, ama kararı yine de Almanya için en iyi saydıkları yönde verdi"): paralar seçmen keselerine akar, sonra seçmenler 'ALMANYA İÇİN EN İYİSİ' etiketli bir terazi/oy simgesine döner; `BAZI TARİHÇİLERE GÖRE` damgası. ('İki taraftan da' fikri kaynaksız → YOK.)
- s10 Terazi: "RÜŞVET: TARTIŞMALI" ↔ "BORÇ: GERÇEK"; sonunda imperial_crown + zincirler.
- s11 Yazılı söz: `doc` ("YAZILI SÖZ · 1519"; "Prenslerin ayrıcalıklarına saygı", "Birlikte yönetecek bir konsey"; mühür).
- s12 Aachen taç giyme: harita AACHEN + diorama (sekizgen şapel kemerleri, avize, ışık huzmesi; genç Karl'a taç iner). `sarlman` madalyası (Şarlman) küçük yanda "ŞARLMAN'IN ŞEHRİ".
- s13 Plus ultra: [YENİ] Herkül Sütunları simgesi + bant "PLUS ULTRA · DAHA ÖTEYE".
- s14 Silinen sözcük: bant "NON PLUS ULTRA" → "NON" sözcüğü çizilip silinir; `RİVAYET` damgası.

## c3 — Şehirlerin İsyanı (49 sn) · ton: kan kırmızısı, gri yağmur
- s1 Rota İspanya → Aachen (harita). s2 Kastilya şehirleri kızarır (TOLEDO, SEGOVIA, SALAMANCA, VALLADOLID…); "VERGİ" (coins) ve "YABANCI DANIŞMAN" etiketleri.
- s3 "KOMÜNERO İSYANI 1520": meşaleli sokak/sancaklı kalabalık diorama ya da `title`.
- s4 **Villalar** [sahne-lab `field`, weather="rain"]: ovada süvari hücumu, yağmur; `whip` geçiş; "23 NİSAN 1521".
- s5 `medals` üçlü: padilla, bravo, maldonado (onyx kenar), "24 NİSAN 1521 · İDAM", `dip`.
- s6 Toledo: maria_pacheco madalyası + Toledo siluet (Alcázar) / kuşatma duman; "AYLARCA DİRENDİ".
- s7 Valensiya: harita VALENCIA + "GERMANÍA · LONCALAR" etiketi (kısa). s8 harita Kastilya-León vurgusu + "23 NİSAN · BAYRAM" (sancak simgesi).
- s9 "Aynı anda bütün tahtlar": 4 taç haritada dört yerde; Karl yalnız birinde → "İLK DERS" damgası.

## c4 — Worms'ta Bir Keşiş (114 sn) · ton: yargı salonu — petrol (protestan) ↔ kırmızı (Habsburg); gerilim
- s1 Harita WORMS + "NİSAN 1521". s2 **Reichstag salonu** (`hall` varyantı: kalabalık, tahtta Karl [seated figür], ortada küçük keşiş [monk]); ardından `medals` karl_genc vs luther.
- s3 "95 MADDE · 1517": `doc` + [YENİ] matbaa simgesi; harita WITTENBERG'den Almanya şehirlerine yayılan çizgiler.
- s4 `doc` "GÜVENLİ GEÇİŞ" + `counter` "21 GÜN".
- s5–s6 Kitaplar masada (diorama/prop), "SENİN Mİ?"; `counter` "1 GÜN"; iki rulo "ALMANCA" → "LATİNCE"; "VAZGEÇMİYORUM" vurgusu.
- s7 `quote` + `TUTANAKTA YOK` / `SONRADAN EKLENMİŞ` damgaları.
- s8–s11 İmparatorun bildirisi: `doc` — atalar (Alman imparatorları / İspanya kralları / Burgonya dükleri) sözcüklerle; "bin yıllık Hıristiyanlık"; s11'de altı şey tek tek (krallıklar, dostlar, beden, kan, can, ruh) simgelerle.
- s12 `doc` WORMS FERMANI + `GERİYE DÖNÜK TARİHLİ` damgası. s13 üç simge (book, [YENİ] press, coin) üstü çizilir + `KANUN DIŞI`.
- s14 Gece yolu [sahne-lab/siz: `road_night`]: atlılar, mum/meşale; harita Worms → Wartburg; "KAÇIRILDI" tırnaklı; sonra frederik_bilge madalyası "Saksonya Seçmeni'nin adamları".
- s15 Wartburg kulesi: pencerede mum, yazan figür (quill); "ŞÖVALYE JÖRG"; açık kitap "YENİ AHİT · ALMANCA".
- s16 Rulo (ferman) solarken meşale parlar → "FİKRİ DURDURAMADI"; bölüm sonu vurgusu.

## c5 — İmparator Hep Başka Yerde (104 sn) · ton: yol/kervan — toprak, duman; sonunda salon (c0'a dönüş)
- s1 Rota Almanya → İspanya + `counter` "9 YIL". s2 Haritada üç ok: İspanya (huzursuzluk), Fransa (mavi ok), Osmanlı (yeşil ok) Karl'a kapanır.
- s3 Köylü Savaşı: duman + siluet köylüler (meşale/tırpan) + `counter` "70.000 – 100.000" (aralık; `TAHMİN`).
- s4–s5 Speyer 1529: `doc` + `counter` "14 ŞEHİR"; büyük sözcük "PROTESTAN" (itiraz etmek) — kök anlamı anlatıyla uyumlu.
- s6 Augsburg itirafı: melanchthon madalyası + `doc` "AUGSBURG İTİRAFI · 1530" ("ana yazar" plakası).
- s7 Şmalkalden Birliği: zincirli kalkan simgeleri + harita. s8 `timeline` 1521 → 1546.
- s9 **Mühlberg** [`field`, sis + nehir]: şafak, Elbe'yi geçen süvari, sis; "24 NİSAN 1547"; ardından johann_friedrich madalyası "ESİR".
- s10 Tiziano: **altın çerçeve içinde** tek başına zırhlı atlı siluet (resmi birebir kopyalama; stilize) + tiziano madalyası.
- s11 moritz madalyası "ESKİ MÜTTEFİK · 1552", `dip`.
- s12 **Innsbruck gece** [`road_night`]: meşaleli atlı kafile, dağ siluetleri, yağmur (**sedye/litter YOK — kaynaksız**; hasta imparator belirsiz kalsın). 
- s13 `doc` AUGSBURG BARIŞI · EYLÜL 1555 (mühür). s14 ferdinand madalyası "YÜRÜTEN: KARDEŞİ".
- s15 Salon (c0 ile aynı sahne), sabit uzak çekim, yaşlı figür — "Tam bir ay sonra" → bölüm kartı c6'ya geçiş `dip`.

## c6 — Kral, Esir, Düello (115 sn) · ton: kraliyet mavisi ↔ kırmızı, düello gerilimi
- s1 `medals` karl_olgun vs fransuva (`vs` kılıç). s2 Harita: Fransa (mavi) etrafında Habsburg bölgeleri sırayla yanar (ispanya, hollanda+franche_comte, napoli) + kuşatma okları.
- s3 **Pavia** [`field`, sis, 24 ŞUBAT 1525]. s4 `doc` mektup ("bana şeref ve canım kaldı") + ünlü cümle için `SONRADAN YAYGINLAŞTI` damgası.
- s5 Madrid hapsi: kule/hücre penceresi diorama + `doc` antlaşma; iki çocuk siluet "REHİN". s6 antlaşmaya büyük `GEÇERSİZ` damgası, belge yırtılır.
- s7 **Roma 1527** [`siege`]: surlar, merdiven, duman; "6 MAYIS 1527"; "MAAŞ ALINAMADI" (coin üstü çizili).
- s8 Castel Sant'Angelo siluet + klemens madalyası; `bars`/`counter` "147 / 189 İSVİÇRELİ MUHAFIZ ÖLDÜ". s9 "EMİR YOK" vurgusu + takvim "AYLARCA".
- s10 Neden-sonuç zinciri (`tree`/özel): Roma 1527 → papa tutsak → catherine_aragon (boşanma onaylanamadı) → henri8 (Roma'dan kopuş; kırık anahtar simgesi); `SIKÇA ANLATILIR` damgası; Catherine imparatorun **TEYZESİ** (etikette 'TEYZE').
- s11 İki madalya yüz yüze + "YALANCI!" söz balonları; `DÜELLO YAPILMADI`. s12 louise_savoy + margareta, başlık "HANIMLAR BARIŞI · CAMBRAI 1529".
- s13 `counter` "2.000.000 ECÜ". s14 `timeline` 1521–1558 savaş dilimleri (kesintili çubuk).

## c7 — Sultan: Hiç Karşılaşmadılar (105 sn) · ton: Osmanlı yeşili ↔ kırmızı; uzaklık
- s1–s2 `medals` suleyman | karl; aralarında uzun boşluk, "HİÇ KARŞILAŞMADILAR"; harita İstanbul–Brüksel doğrusu.
- s3 **Mohaç** [`field`, bataklık/nehir]; lajos2 madalyası (onyx) "DERE'DE BOĞULDU". s4–s5 Harita: Macaristan bölünür (macar_habsburg ↔ macar_osmanli ↔ erdel); ferdinand + zapolya madalyaları.
- s6–s8 **Viyana 1529** [`siege`]: surlar, çadır, top, yağmur/çamur/kar; "27 EYLÜL"; `counter` "75.000 – 100.000" (`MODERN TAHMİN`); "EKİM ORTASI · GERİ ÇEKİLME".
- s9 Harita İtalya rotası (Karl, papadan taç için). s10 `doc` sefer günlüğü → "İSPANYA KRALI" vurgulu. s11 Güns küçük kale [`siege`]: `counter` "700–800 KİŞİ" × "25 GÜN". s12 harita: iki ordu yaklaşır, karşılaşmaz.
- s13 Levha: karl madalyası altında "İMPARATOR" üstü çizilir → "İSPANYA KRALI". s14 `doc` ATEŞKES 1547 + `counter` "30.000 ALTIN / YIL". s15 harita: Macaristan rengi (kayıp) + ferdinand madalyası.

## c8 — Akdeniz'de Barbaros (71 sn) · ton: derin deniz mavisi/turkuaz, fırtına
- s1 `sea` diorama (kadırgalar) + barbaros madalyası. s2 Harita İstanbul → Tunus (yeşil) "1534".
- s3–s4 doria madalyası; Halkulvadi kuşatması [`siege`]; `counter` "≈ 20.000 ESİR SERBEST". s5 kutlama: defne/çan/sancak (kısa). s6 gece denizi, ufukta filo.
- s7 **Preveze** deniz savaşı [`sea`, kadırga çatışması] + harita; "28 EYLÜL 1538". s8 harita yeşil dalga (yeni metin: "sonraki yıllarda" — **'30 YIL' sayacı YOK**).
- s9 `counter`'lar "≈500 YELKENLİ", "≈24.000 ASKER". s10 **fırtına** [`sea` storm]: gemiler batar ("≈150"). s11 kortes madalyası + boş sandalyeli konsey masası, `ANLATILIR` damgası ("çağrılmadığı anlatılır").

## c9 — Yeni Dünya: Altın, Gümüş ve Vicdan (108 sn) · ton: tropik yeşil + altın + kan; son kısım vicdan (sade)
- s1 Atlantik haritası, "HİÇ GÖRMEDİ". s2 Küba → Veracruz → Tenochtitlan rotası + kortes madalyası + [YENİ] Tenochtitlan (göl kenti: setyol, piramit, duman) + "13 AĞUSTOS 1521".
- s3 `doc` "CORTÉS'İN MEKTUPLARI" ("KENDİNİ SAVUNAN" vurgulu). s4 durer madalyası + altın eşya simgeleri + `counter` "≈100.000 FLORİN" (`TAHMİN`).
- s5–s8 **Cajamarca** [YENİ `ransom_room`]: duvarda kırmızı çizgiye dek yığılan altın, tutsak Atahualpa (tüylü başlık siluet); `counter` "1.326.539 PESO"; `dip` (idam); `stacked` 1/5 kraliyet payı.
- s9 `doc` YENİ YASALAR 1542 + harita Peru. s10–s11 sepulveda vs lascasas madalyaları + tartışma salonu (hall varyantı, iki kürsü); `RESMÎ KAZANAN YOK` damgası.
- s12–s14 Dünya turu haritası (rota animasyonu); elkano madalyası; arma: küre simgesi + bant "PRIMUS CIRCUMDEDISTI ME".

## c10 — Faturayı Kim Ödedi? (64 sn) · ton: soğuk gümüş-yeşil, defter
- s1–s2 Soru: gümüş sandık simgesi (üstü çizili) + `quote`. s3 `bars` (Alçak Ülkeler > 10M, Kastilya > 9M, Napoli > 5M — birimi `arastirma/A4` ile doğrula; birim yoksa "milyon" yaz). s4 `timeline` Potosí 1545.
- s5–s6 sayım odası + fugger madalyası + `doc` "FUGGER'İN MEKTUBU · 1523" (özet; uydurma tırnak yok). s7 harita VENEZUELA + welser.
- s8 felipe2 madalyası + "NİSAN 1557 · ÖDEMELER DURDU" damgası + uçurum/borç grafiği. s9 kapanış: para yığınları üstünde taç, altında uçurum — "BORÇ".

## c11 — Adamın Kendisi (63 sn) · ton: yakın, sıcak, melankolik; mum ışığı
- s1 karl_olgun madalyası yavaş yakın plan. s2–s3 Çene: madalyada çeneye yaklaş (saygılı); `doc` "2019 ÇALIŞMASI"; `ÇALIŞMA KÜÇÜK · KESİN DEĞİL` damgası.
- s4–s6 isabel madalyası + yüzük; "1526 – 1539"; `dip`; manastır avlusu diorama; "ANLATILIR" damgası (siyah giyim).
- s7 Yatak odası diorama (mum, gut, yemek masası) `ANLATILIR`. s8–s9 Karl'ın gezi ağı: tüm rotaları haritada altın çizgilerle çiz (Almanya, İtalya, İspanya, Hollanda, Fransa, Tunus, Cezayir) → "YOLLARDA TAŞIDI".

## c12 — Bırakmak (95 sn) · ton: c0'ın aynası: aynı salon, ağır altın ışık, vedaya dönük
- s1 `title` "25 EKİM 1555 · 15.00" + hourglass; salon geniş. s2 juana madalyası (onyx), "ALTI AY ÖNCE"; kule penceresi.
- s3 Salon: yürüyen çift figür (imparator + Orange'ın omzu), arkada felipe2 ve mary_macar madalyaları sırayla. s4 `timeline` 1515 → 1555 "40 YIL" + genç/yaşlı madalya yan yana.
- s5 Devir şeması (`tree`/özel ağaç): HOLLANDA → Felipe (şimdi), İSPANYA → Felipe (Ocak 1556), İMPARATORLUK UNVANI → Ferdinand (1556–1558). s6 iki neden simgesi (gut/yorgunluk; evrensel imparatorluk) + `YORUM` damgası.
- s7 felipe2 + çatlayan sikke ("SAVAŞTA VE İFLASA YAKIN"). s8 Harita Flandre → İspanya (Eylül 1556) → YUSTE (Şubat 1557) + manastır diorama.
- s9 Şapel/mumlar + tabut siluet: "AYİN: ÇALIŞMAYA GÖRE" ↔ "PROVA: RİVAYET" damgası. s10 Yatak odası; mum söner; "31 AĞUSTOS → 21 EYLÜL 1558 · 58 YAŞINDA"; `dip` siyaha.

## c13 — Hesap (80 sn) · ton: son — açılan altın ışık, sonra sade soru
- s1 `emblem` family (5. cephe yanar). s2 dört tahtı Karl'a bağlayan **akrabalık ağı** (düğüm-çizgi). s3 ağaç: Karl → Felipe (İSPANYA KOLU) / Ferdinand (AVUSTURYA KOLU); harita rengi ikiye ayrılır.
- s4 Taç çatlar; protestan petrol bölge yayılır. s5 Terazi: birbirini dengeleyen çok sayıda küçük devlet kalkanı; `BİRÇOK TARİHÇİ` damgası.
- s6 Dünya haritası: üç vurgu sırayla (dünya turu rotası, Atlantik ticaret çizgileri, tartışma/terazi simgesi).
- s7 **Strateji oyunu paneli** [YENİ özel çekim]: jenerik oyun arayüzü ("KİŞİSEL BİRLİK · 1 HÜKÜMDAR — ÇOK DEVLET"); sonra "OYUN DEĞİL, ÖMÜR". (Gerçek bir oyunun arayüzünü/markasını kopyalama.)
- s8 karl_yasli madalyası ↔ "FİKİR" simgesi (taç + küre) — soru. s9 beş cephe simgesi (1–5 numaralı) + "HANGİSİNİ BIRAKIRDIN?" + yorum balonu. (s10 sonrası kapanışı compose.py ekler.)
