# SCN-2: kurul tur 2 düzeltmeleri · c2 (Defterin Sihri, 342,8–591,5 sn) ve set çeşitlemesi

Tarih: 5 Kasım 2026 · Ajan: SCN-2 (c2 sahne düzelticisi). Render, miks ve git kullanılmadı.

**Kanıt kareleri:** `out_p1/duzeltme/tur2/SCN-2/*.jpg` (30 sayfa).
- Her sayfanın üst sırası **ÖNCE**: v2 videosundan (`out_p1/medici_P1.mp4`) ffmpeg ile alınan kare.
- Alt sırası **SONRA**: güncel motorla çizilen kare (`compose.Program(part=1).frame`).
- Üretici betik: `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/fix_scn2/kanit.py`.

**Değişmeyenler:**
- Anlatım zaman çizelgesi aynı. Bütün çekim sınırları cümle ya da sözcük çapasına bağlı.
- c2 bölüm sınırları aynı: 342,80 → 590,23, ardından motorun bekleme süresi.
- Başkanın 18b/18c değişikliği (papa: `admonish` + bulla, ≥1,45× kadraj) ve sikke düzeltmesi korundu. 18b ile 18c arasına yalnız bir ara plan eklendi (D).

## Özet
- **c2 çekim listesi 45 → 41 çekim.**
  - Üç "defter" çekimi, sekiz kartın yerini aldı. Kartlar: eski #71–73 ağ/zaman çizgisi, #83–85 anahtar üçlüsü, #87–89 catasto montajı.
  - Üç nesne/el ara planı eklendi: kese, mitra, kalem.
  - Brugge çekimi ikiye bölündü.
- **Aynı kartta sıçrayan kesme:** 0. **Işık patlaması:** c2'de 2 (bölüm açılışı ve kapı).
- **Yer başına ayrı set:** Brugge, Roma bankası (c1), kâtip odası, papalık salonu, Konstanz, Catasto dairesi, Stinche hücresi.
- **QA:**
  - `qa_yerlesim`: İHLAL 0.
  - `qa_donem`: İHLAL 0.
  - `qa_flow`: c2'de KALDI yok. Tek KALDI, ENG-D'nin yeni "Beyan ↔ gerçekleşen kamera" kapısından geliyor ve c0/c1 çekimlerinde (ayrıntı QA bölümünde).

## A. Veto ve koşul maddeleri

| Madde | Ne yapıldı (dosya: çekim) | Kanıt | Kapanan |
|---|---|---|---|
| **A1 · 1520 mührü** | `p1_ortak.seal_drop(variant=, year=)`: armayı **nesne yılına** göre çizer. Yerel bağlam `p1_ortak.nesne_yili(1520)` çekimin cx'ini koruyarak donem yığınına 1520 yılını iter; dönem kaydı çekim indeksiyle ve 1520 yılıyla yazılır (qa_donem: `arms variant=std nesne_yili=1520`). Açıkça `variant="std"` verilir. `palle_relief` 6 topu tek renk kabartma olarak çizer; üst top büyük ve üç zambak kabartmalıdır (balmumu tek renk olduğundan zambak mavi değil, kabartmayla seçilir). Sahne: `scenes_c2` #98 `c2_yakin scene="kalem"` (575,5–580,0), `seal_year=1520, seal_variant="std"`. Mühür ekranda r=170 ile büyük çizilir ve zambaklar okunur. Mühür, sonraki iris geçişinin dairesi olur (eşleşen nesne → Cosimo madalyası). | `A1_muhur_1520.jpg` (önce 8 top; sonra 6 top + zambak) | SA2-Y4, KA1-Ö3, KA2-D12 |
| **A2 · HUD 1418** | `scenes_c2.YIL_AT`: `(("c2s17", -0.1), 1418)` eklendi. c2s18 "öldü" 1419'da kaldı. | `A2_hud_1418.jpg` | KA1-K3 |
| **A3 · Cossa'nın mezarı** | `c2_kinds.k_mezar`: taşta `MEZAR_YAZIT = "IOANNES QVONDAM PAPA"`. Harfler `mezarına`→`papa` arasında tek tek oyulur. Koyu harf + açık dudak, `fit_size` ile tek satır. Türkçesi levhada: `P.tag("ESKİ PAPA · ÇEVİRİ BİZE AİT")`, "eski" sözcüğünde gelir. Levha VAFTİZHANE plakasıyla çakışmasın diye y=372'de. Çekimler: #76 (17a) ve #78 (17c). | `A3_mezar_latince.jpg` | SA2-Y8, KA1-K2, KA2-D5 |
| **A4 · BELGE · DE ROOVER ≥2 sn** | #79 `c2_rivayet`: damga "De" sözcüğü +0,35'te basılır (465,25 sn; önceden 465,94). Konumu (600, 400): plakanın rol satırını örtmez. #80 (18b) `stamp_hold` aynı ekran yerinde durur, "Cossa'nın" +0,3'te (468,45 sn) söner. Görünme süresi 465,25–468,45 ≈ 3,2 sn. | `A4_belge_de_roover_2sn.jpg` | KA2-D8 |
| **A4 · 1426'DA ÇEKİLDİ** | `c2_kinds.k_kasa`: çarpı YALNIZ kese simgesinin üstünde. "SERMAYE" 40 px; "1426'DA ÇEKİLDİ" **38 px**, koyu kızıl, çarpının dışında, alt satırda. Ölçülen kontrast ≈5,3:1. | `A4_1426_cekildi.jpg` | TE2-Y4, KA2-D7 |
| **A4 · sayaç "143.194+"** | `P.count_up(step=, suffix_final=)`: ara değerler 5.000'lik adımla sayılır. "+" yalnız son değerde görünür. Sayaç 0,15 sn erken başlar ve 0,9 sn sürer; mum geçişi 1,8 → 1,2 sn. Son değer ≥1,2 sn okunur (TE2-Y10). Lorenzo'nun 180.000'i de 5.000'lik adımla sayılır. | `A4_sayac_150000.jpg` | KA2-D10, TE2-Y10 |
| **A4 · KLASİK BİR ÖRNEK** | Brugge ikiye bölündü. "BRUGGE · KLASİK BİR ÖRNEK" levhası #61'de, "Klasik" sözcüğünden çekim sonuna dek görünür (≈4 sn). "BARSELONA'YA ÇEKİLMİŞ POLİÇE" artık #62 ara planında; ikisi aynı karede yok. `qa_yerlesim` çakışması kalktı. | `A4_brugge_klasik_ornek.jpg` | KA2-D9, qa_yerlesim #61 |
| **A4 · catasto** | Yeni olgu eklenmedi. Sahne B5'te "masaya beyanname getiren hane reisleri" olarak kuruldu. Ekrandaki "PORTATA" başkan kararından. | `B5_catasto_dairesi.jpg` | KA2-D6 |
| **A5 · CATASTO / büyük harf** | c2'de her yerde "CATASTO · 1427" kullanılıyor (sahne + `k_katasto` + defter). Yabancı adlar `sk.tr_upper` kuralına göre yazıldı: GİOVANNİ, CAVALCANTİ, MACHİAVELLİ, MACHİAVELLİ'YE/'NİN, COSİMO, GİOVANNİ'NİN, PALLA STROZZİ, PACİOLİ, V. MARTİNUS. Latince ve İtalyanca dünya içi yazılar (DEBITORI/CREDITORI, IOANNES QVONDAM PAPA, COSMVS · MEDICES, *Istorie fiorentine*) özgün kaldı. | `A5_catasto_buyuk_harf.jpg` | TE2-Y7, TE2-Ö12 (c2) |

## B. Yerleşim, okunurluk, dönem

| Madde | Ne yapıldı | Kanıt | Kapanan |
|---|---|---|---|
| **B1 · GİOVANNİ × COSSA** | #73: GİOVANNİ levhası (420, 410) konumunda, solda-aşağıda. BALDASSARRE COSSA levhası (900, 190), w=740. Çakışma yok. XXIII. JOHANNES levhası w=870 (motorun genişlettiği değere eşitlendi). | `B1_giovanni_cossa_levha.jpg` | SA1-Y3, AN2-Ö2, TE2-Y1, qa_yerlesim #74 |
| **B2 · KUR FARKI** | `c2_kinds.k_nolist`: yazı oyma yaldız değil, düz koyu mürekkep `#2E1C06`. Parıltı levhanın arkasına alındı. Ölçülen kontrast **3,2:1 → 7,5:1**. BORÇ/FAİZ çarpıları yarı saydam ve inceltildi (TE2-K6). Çekim: #64 (368,8–373,4). | `B2_kur_farki_kontrast.jpg` | TE2-Y5 (Ö5 kalanı) |
| **B3 · harita etiketleri** | #63 `cams` daha geniş açıyla ve kuzeyde kuruldu: (2,7–2,8; 46,2–46,4; 1,68–1,80). BARSELONA `side="l"`. Poliçe rotası kentin biraz kuzeyinde biter, sikke ve kese simgeleri etiketlerden uzakta. BRUGGE kadraj içinde ve tam okunur. Not: ENG-D'nin harita takip kamerası da bu çekimde çalışıyor. | `B3_harita_etiketleri.jpg` | SA2-K14 |
| **B4 · Cossa'nın tiarası** | `p1_ortak.tiara_draw`: beyaz kovan gövde, üç altın taç halkası ve küre-haç (Martinus'un kit tiarasıyla aynı dil). `prop_arc` artık çizim işlevi de kabul ediyor. #73 (papalık) ve #74 (Konstanz'da düşen taç). | `B4_tiara.jpg` | SA2-Y7 |
| **B5 · catasto sahnesi** | #84 yeni set `salon/catasto`. Kireç sıva, Floransa kırmızısı lambri, ikiz kemerli pencereler, Komün kalkanı (beyaz zeminde kırmızı zambak), iple bağlı beyanname rafları var. İki görevli masada yazıyor. Hane reisleri beyannameyle (`prop="book"`) sırayla yürüyerek masaya gelir, biri eğilip teslim eder. Levhalar: "CATASTO · 1427" ve "HANE REİSLERİNİN BEYANNAMESİ · PORTATA". Sokak/kapı kapı sahnesi ve simsiyah siluet yayalar kalktı; bütün figürler renkli. | `B5_catasto_dairesi.jpg` | SA2-Y6, KA1-K1, KA2-D6 |
| **B6 · Cavalcanti** | #94 yeni oda `p1zindan` (`p1_ortak.P1Zindan`). Kaba taş duvar, yüksek pencerede demir **parmaklık**, duvarda zincir halkası, saman şilte var; haç, yatak ve kitaplık yok. Kostüm `CAVALCANTI`: solgun gri-yeşil cüppe, koyu kahve başlık. Machiavelli'nin sarı-mavisinden ayrışıyor. | `B6_cavalcanti_hucre_kostum.jpg` (556,4 ↔ 541,2 Machiavelli) | SA2-Y9 |
| **B7 · İTİRAZ damgası** | #77: damga (520, 440) konumunda, papa figürünün dışında. "V. MARTİNUS" (520, 220). | `B7_itiraz_damgasi.jpg` | AN1-Y9 |
| **B8 · kuledeki beyaz şerit** | **Teşhis:** şerit, Palazzo Vecchio kulesinin arkasındaki Giotto **çan kulesinin** kule kenarından taşan 12 px'lik dilimi. Denetimde kule geçici olarak kaldırılınca çan kulesi tümüyle görünüyor. `SkylineDikey` katmanlarında yatay paralaks yok (`VLayer fx=0`), bu yüzden kamera x'i bunu çözmüyor (denendi, geri alındı). Düzeltme `cilt_sehir.py`'de, yani SCN-1'in dosyasında yapılmalı. → **SCN-1 isteği 1.** | `B8_kule_serit.jpg` | SA1-K3 (açık, istek) |

## C. Kurgu ve hareket

| Madde | Ne yapıldı | Kanıt | Kapanan |
|---|---|---|---|
| **C1 + C5 · ağ kartları** | Eski #71–73 (zaman çizgisi, iki ağ kartı, 427,6 sıçraması) tek çekim oldu: **#72 `c2_masa v="iz"`** (416,0–431,6, 15,6 sn, longtake). Kâtibin defterinden `zoomthru` ile masadaki açık deftere geçilir. Sol sayfada mürekkep zaman çizgisi var: 1340 CENOVA, 1494 PACİOLİ (eski olgular, yeni olgu yok), MEDİCİ İCADI ✗, ETMEDİLER. Kamera tek sürekli hareketle sağ sayfaya kayar: MEDİCİ'NİN FARKI: YAPI, DEFTER DEĞİL ✗, FLORANSA → ROMA / VENEDİK, KENDİ ORTAKLIĞI / KENDİ DEFTERİ. Tüy kalem yazının ucunu izler; ön planda bulanık şamdan var. | `C1_C5_ag_tek_kamera.jpg` | AN1-Y3 (427,6), AN1-Y4 (ağ cebi), AN2-K2 (seyrek şema), SA1-Ö2 |
| **C1 + C4 · anahtar üçlüsü** | Eski #83–85 (480,2 ve 482,2 sıçramaları, sessiz cep, "22 YIL" slaytı) tek çekim oldu: **#83 `c2_masa v="kasa"`** (475,8–486,4). Papalık kasası, kızıl kadife masa. Bir **el** (Giovanni'nin koyu kızıl yeni) anahtarları "memurluğu" sözcüğünde deftere bırakır. Sağ sayfada 1422'den **22 YIL** düz mürekkep şerit dolar, **+ 18 YIL** kesikli; KESİNTİSİZ / ARALIKLI; MEDİCİ'DE KALDI. | `C1_C4_anahtar_tek_kamera.jpg` | AN1-Y3 (480,2 / 482,2), AN1-Y4, SA1-Y6 (1. küme), PK1 "slayt" |
| **C4 · catasto kümesi** | Eski #87–89 (ızgara, %29,8 çubuğu, sayaç + sandık) tek çekim oldu: **#85 `c2_masa v="catasto"`** (493,6–502,8). Görevlilerin kayıt defterinde 9.780 hane yazılır, ilk 137 hane altın renkte. **%29,8 defterin alt kenarına** mürekkeple işlenir ("%29,8 · 137 HANE", BİR HESABA GÖRE). Kamera sağ sayfaya geçer: PALLA STROZZİ · 1427'NİN EN ZENGİNİ · 163.000 FLORİN · YAKLAŞIK. Olgular eski ekran olgularıyla aynı. | `C4_catasto_defter.jpg` | SA1-Y6 (2. küme), AN2 (montaj kartları) |
| **C2 · ölü açılışlar** | 423,75: çekim birleştiği için ortadan kalktı, içerik süreklidir. 534,45 (#91): `c2_kalemler` sayfaları ve levhaları **ilk karede** hazır. Kaynakların kendi sözleri soluk el yazısıyla "kalemden" sözcüğünde akmaya başlar. | `C2_olu_acilis_534.jpg` | AN1-Y6, SA1-Y4, PK2-Y3 |
| **C3 · sessiz cepler** | Anahtar ve ağ cepleri tek çekim oldu (yukarıda). Harita #63: anlatıya bağlı ikinci hareket olarak "kazanç / kur" sözcüklerinde kesenin yanında sallanan kazanç sikkeleri belirir; kamerası ENG-D'de. `c1_machiavelli` #92: "bir asra yakın sonra" sözünde **pencere ışığı sahneyi süpürür** (zaman akar; `light_sweep`). ≥6 sn çekimlerde kamera var; qa "Ölçülen hareket" GEÇTİ. | `C3_machiavelli_isik.jpg` | AN1-Y4 |
| **C5 · dalgalı çizgili sayfalar** | Sayfalarda gerçek harfler var (`k_kalemler(lines_a/lines_b, full, orig)`, `tomar(words=)`). Anahtar söz **anlatımla birebir** yazılır: Machiavelli "huzurla gidiyordur / ve kıskançlık, / insana verilenden değil, / istediğinden doğar."; Cavalcanti "kimse dünyevi tasaları / **sonsuz huzurla** (kızıl alt çizgi) / değiş tokuş ettiği için / kederlenmemeli.". Her satır kendi sözcüğünde yazılır. Sayfa başında kaynağın kendi sözleri soluk el yazısı dokusu olarak durur; bunlar teyit_P1'deki birincil alıntılardır (MAC IV "Muoio contento…", CAV IV "…per passare ai perpetuali riposi"). #95/#96 iki sayfa yazılı hâlde ve "?" ile. | `C5_gercek_harfler.jpg` | AN2-K2, TE2 §5 |
| **C6 · Cosimo kartı** | #99: COSİMO levhası "öldüğünde" sözcüğünde gelir (580,57 ≈ 580,6). "39 YAŞINDAYDI" **sayılmadan** "oğlu" sözcüğünde gelir (`count=False`), "1389 DOĞUMLU" "Cosimo"da. Çıkış geçişi (kule) **1,6 → 1,0 sn**. Giriş iris'i 1520 mührünün dairesinden açılır (eşleşen nesne). | `C6_cosimo_karti.jpg` | AN2-K4 |
| **C7 · ışık patlaması** | c2'de **8 → 2**: #60 bölüm açılışı ("Çözüm" ifşası) ve #100 kapı (1,0 sn). Diğerleri: #72 zoomthru (ölçek), #73 zoomthru (eşleşen nesne: defterdeki kese → Giovanni'nin kesesi), #76 candle (Cossa'nın ölümü), #83 sert kesme, #90 dip (zaman uçurumu), #94 sayfa (iki kalem arası malzeme). qa "Işık geçişi bütçesi": c0 1, c1 1, c2 2 = 4 ≤ 4. | qa_flow | AN1-Y8, SA1-Y7 (c2) |
| **C8 · üç yoksul** | `c2_kinds.k_sadaka`: biri **ön planda**, büyük (h 760) ve sağ kadraj kenarıyla kesik. İkisi arkada, küçük ve üst üste (x 1268 / 1392). Aralıklar eşit değil; teşekkür jestleri ve sikke sırası farklı zamanlarda. Figür çeşitlemesi ENG-C'nin kitinde. | `C8_yoksullar_kompozisyon.jpg` | SA1-Y5, KA2-D13 (kompozisyon) |

## D. Set tekrarı ve ara planlar
**Mekanizma (`cilt_oda.py`, yalnız Salon):**
- `SALON_HOOKS` sözlüğü: (varyant, "wall"|"main") → çizim kancası. Varsa Salon o katmanı kancayla çizer.
- `window_light` rengi paletten (`light`) alınır.
- Eski varyantlar (napoli/medici/signoria/pitti/taht) **değişmedi**.
- Kancalar ve paletler `p1_ortak.py`'de; önbellek anahtarı varyant adı olduğu için yeni setler kendi önbelleğinde.

| Yer | Set | Kanıt |
|---|---|---|
| **Brugge** (#61) | `salon/brugge`: soğuk badana, koyu meşe kirişli tavan, **Flaman haç kasalı pencereler**. Pencereden kanal, basamaklı çatılı tuğla evler ve su görünür; üst camlar göz camlı, alt kanatlar açık. Ayrıca dışbükey ayna, küçük pano resimleri, **siyah-beyaz dama taş**, arduvaz masa örtüsü ve **soğuk kuzey ışığı** (`light #DCE8F4`). | `D_set_brugge.jpg` |
| **Roma bankası** (c1 #52, 294,1) | `salon/roma` (scenes_c1.py'de yalnız `variant=` satırı): sıcak toprak sıva, Roma meander frizi, **dikdörtgen taş haç kasalı pencereler**, kemerli raf nişlerinde yatık defterler, **yeşil çuha banco**, para sandığı, küçük terrakota tuğla döşeme. | `D_set_roma_bankasi_c1.jpg` |
| **Kâtip odası** (#71) | `salon/katip`: yeşilimsi gri badana, koyu yeşil lambri, **yuvarlak göz pencereler**, uzun defter rafları, asılı terazi, tahta döşeme. | `D_set_katip.jpg` |
| **Papalık salonu** (#77, #80, #82) | `P1Salon papa` (yeni önbellek anahtarı `p1salonpapat2`): Medici ağaç goblen **yok**. Yerine koyu kızıl damasko üstünde **çapraz anahtarlar + tiara** dokuması, **beyaz-altın perde**, koyu ceviz lambri. | `D_set_papalik.jpg` |
| **Konstanz** (#74) | `P1Salon konstanz`: kesme taş duvar. **Altın zeminde siyah tek başlı imparatorluk kartalı** kumaşları var; 1415'te Sigismund "Romalıların kralı" idi, çift başlı kartal yok. Lacivert perde, **açık meşe** lambri, açık taş zemin. | `D_set_konstanz.jpg` |
| **Catasto dairesi** (#84) | B5. | `B5_catasto_dairesi.jpg` |
| **Stinche hücresi** (#94) | B6. | `B6_cavalcanti_hucre_kostum.jpg` |

**Ara planlar (≥2×, nesne + el; yüz yok):** `c2_kinds.k_yakin` + `arm_hand` (kit el sprite'ı, yen ve kol ağzı).
- **#62 kese** (355,8–361,1): banker keseyi peşin sürer, tüccar karşılığında poliçeyi verir.
- **#81 mitra** (469,9–471,7, 18b ile 18c arasında): rehin mitra Giovanni'nin ellerinde; beyaz yenli papalık eli uzanır.
- **#98 kalem** (575,5–580,0): tüy kalem *Istorie fiorentine* yazar, el çekilir, 1520 mührü düşer.
- Ayrıca **#83'te anahtarları bırakan el**, **#72/#83/#85'te tüy kalem** var.

Böylece papalık, Brugge, Machiavelli ve Catasto sahnelerinin her biri birer ara plan kazandı. Kanıt: `D_ara_plan_el_nesne.jpg`. Kapananlar: AN2-Ö3, SA1 §6, SA2 §4, KA1/KA2 "hazır set".

## QA sonuçları
- **`qa_yerlesim.py --part 1`:** 303 kare, 80 levha · **İHLAL 0** (önce 8; c2'deki 2'si #61 BRUGGE × poliçe ve #74 GİOVANNİ × COSSA). Düzeltilen: 2 uyarı, c0/c1.
- **`qa_donem.py --part 1`:** 306 kare, 323 kayıt · **İHLAL 0**, uyarı 0. 1520 mührü `arms std nesne_yili=1520` olarak kaydedildi.
- **`qa_flow.py --part 1`:** 19 GEÇTİ · 1 KALDI · 1 UYARI · 1 PAS (dosya: `…/scratchpad/fix_scn2/qf_1.json`).
  - **KALDI**, ENG-D'nin yeni "Beyan ↔ gerçekleşen kamera" kapısından. Kalan çekimler: #12 c0_harita, #37 c1_yazi, #55 p1_map 313 sn (TERS yön). **c2'de 0.** Bu kapı v2 qa'sında yoktu; v2 özeti 17 GEÇTİ / 0 KALDI idi. c2 kendi payına KALDI eklemiyor.
  - **c2 için geçen kapılar:**
    - Aynı görüntü kesmesi: kesin 0, sınırda 0.
    - Işık bütçesi: c2'de 2.
    - Yönetmen kartı: `yonetmen_c2.md` 41 satır = 41 çekim, tür sırası aynı; yeniden üretildi.
    - Kart dizisi: dünya/figür %61.
    - Sert kesme: %39.
    - Durgunluk: en uzun 0,0 sn.
    - Ölçülen hareket: 0 zayıf.
    - Çapa denetimi: mutlak %2.
    - Olay yoğunluğu: %98.
  - **UYARI** yön denetiminden; c2 kısmı Konstanz `pan l` (bilinçli, kartta yazılı).
- **Ölçülen kontrast:** KUR FARKI 3,2 → 7,5:1 · 1426'DA ÇEKİLDİ 5,3:1 · mezar yazıtı koyu mürekkep + açık dudak.

## Değişen dosyalar
- **`scenes_c2.py`** (yeniden yazıldı):
  - 41 çekim; YIL_AT +1418.
  - `light_sweep` ve `stamp_hold` ovl'ları.
  - Cavalcanti kostümü.
- **`c2_kinds.py`:**
  - Değişen türler: `k_nolist`, `k_kasa`, `k_mezar` (Latince), `k_kalemler` (gerçek harfler, ölü açılış yok), `k_sadaka` (derinlik), `tomar(words=)`.
  - Yeni türler: **`c2_masa`** (iz / kasa / catasto) ve **`c2_yakin`** (kese / mitra / kalem); yardımcılar `arm_hand`, `_letter`.
  - Ad düzeltmeleri: V. MARTİNUS, GİOVANNİ.
  - `OWN_CAMERA` += c2_masa, c2_yakin.
- **`p1_ortak.py`** (`_wrap` ve harita sarmalayıcısına dokunulmadı):
  - `count_up(step, suffix_final, count)`, `prop_arc` çizim işlevi kabul ediyor.
  - Yeni işlevler: `tiara_draw`, `lily_path`, `palle_relief`, `nesne_yili`, `seal_drop(variant, year)`.
  - Set kancaları: brugge, roma, katip, catasto.
  - `P1Salon` papa/konstanz dekoru: `_papal_hanging`, `_imperial_hanging`, `eagle_single`, perde rengi, yeni önbellek anahtarı.
  - `P1Zindan`.
- **`cilt_oda.py`:** yalnız Salon'a `SALON_HOOKS` + pencere ışığı rengi (10 satır). Oda1743, `_blit_cf`, `sil_actor`, `seated` ve `draw_actor`'a dokunulmadı.
- **`scenes_c1.py`:** yalnız Vieri çekiminde `variant="napoli"` → `variant="roma"` (tek satır).
- **`yonetmen_c2.md`:** kurul tur 2 kartı, shots'tan üretildi. Eski hâli: `…/scratchpad/fix_scn2/yonetmen_c2_once.md`.

## İstekler
**SCN-1:**
1. **`cilt_sehir.py` `SkylineDikey._draw_city_v`** (B8, SA1-K3):
   - Sorun: `XD = 700` iken Duomo grubundaki çan kulesinin ≈12 px'lik sol dilimi Palazzo Vecchio kulesinin sol kenarından taşıyor. 586 sn'de x≈797–809, y≈740–950.
   - Öneri: `XD ≈ 730`. Çan kulesi tümüyle kulenin arkasında kalır, kubbe solda görünür kalır ve "şehrin en yüksek kulesi" anlatısıyla çelişen ikinci kule görünmez.
   - Alternatif: `XD ≈ 600`; çan kulesi tam görünür.
   - Değişiklikten sonra `out/_cache/world/sehir_dikey_*_city_*` dosyaları silinmeli. Katmanın yatay paralaksı olmadığı için (`VLayer fx=0`) bu sahneden kamera x'iyle çözülemiyor.
2. **`donem.py`'ye resmî "nesne yılı" API'si** (ör. `donem.nesne_yili(y)` ya da `use_year(y, cx=…)`: çekimin cx'ini koruyan bağlam):
   - Şimdi `p1_ortak.nesne_yili` yerel çözüm; `donem._STACK/_Frame` iç yapısını kullanıyor, yoksa `use_year`'a düşüyor.
   - Machiavelli, Guicciardini ve Vasari gibi sonradan yazan kalemler P2–P7'de de bunu kullanacak (SA2 §6-1).
3. **Tutarlılık için:**
   - c2'deki yabancı adlar `tr_upper` ile yazıldı.
   - c1'de `c1_kinds.py` içinde hâlâ "GIOVANNI VILLANI" literali var (scenes_c1'deki levha "GİOVANNİ VİLLANİ").
   - Kâtip/Brugge/papalık setlerinde masa üstündeki `doc_sheet` mühürü dönem kuralıyla `red8` palle çiziyor. Medici dışı mekânlarda bu küçük mühür tarafsız olabilir; motor tarafında isteğe bağlı.

**ENG-C:**
1. `c2_sadaka` yoksulları (seed 32/33/34) ve catasto hane reisleri (halk 3, soylu_f 6, soylu 14) için örnek başına çeşitleme (boy, başlık, giysi tonu) kitte bekleniyor. Kompozisyon sahnede kuruldu.
2. `c2_yakin` ara planları kitin `hand_sprite` elini büyük ölçekte kullanıyor (yen ve kol ağzı `arm_hand`'de). Kit büyük el için daha ayrıntılı bir çizim (parmak boğumları, tırnak) sunarsa ara planlar güçlenir.

**ENG-D:**
1. Yeni "Beyan ↔ gerçekleşen kamera" KALDI'sı c0/c1 çekimlerinden: #12 c0_harita, #37 c1_yazi, #55 p1_map 313 sn TERS. c2'de ihlal yok.
2. `c2_masa` ve `c2_yakin` `cilt_cam.OWN_CAMERA`'ya eklendi (c2_kinds). Kamera `cams=[(çapa,(x,y,zum))]` ile dünya koordinatında; qa "own:pan/yol" sayıyor.
3. #63 kambiyo haritasında `cams` daha geniş açıya alındı (BRUGGE etiketi için). Takip kamerası açılınca etiketin üst kenara yaklaşmadığı doğrulanmalı. Bu karelerde 365,4 sn'de BRUGGE y≈108, içeride.

## Açık kalanlar
- **B8:** kuledeki dilim SCN-1'in dosyasında (istek 1).
- **Ara planların el çizimi:** kitin düz "eldiven" eli; üslupla tutarlı ama yüz yakın planı gibi zayıf yan. Ara planlar kısa tutuldu (1,7–5,4 sn), odakta nesne var.
- **İsteğe bağlı fırsat:** ölüm döşeğinde mum ara planı (#89) yapılmadı. Ölüm sahnesi iki çekimden oluşuyor; mumun sönüşü yakın planla güçlenebilir.
- **`notlar_c2.md`:** eski tablo duruyor (KA2-Y9 kayıt temizliği). Bu dosya görev sahipliğimde değildi; güncel tablo ve gerekçeler `yonetmen_c2.md`'de.
- **c1'deki Roma HUD yılı (1390 / 1385, KA1-Ö4a):** SCN-1'in alanında.

## En emin olmadığım nokta
- **Masa defteri dili:** bölümün imza sekansı ("Defter dünyadır") için üç masa defteri çekimi kullandım (İZ, KASA, CATASTO).
  - Masa, kapak rengi, nesneler, ışık ve kamera her birinde farklı.
  - Yine de aynı "üstten açık defter" kalıbı üç kez tekrar ediyor. Kurul bunu "yeni bir şablon" diye okuyabilir.
  - Kâğıtta boş alan çok. Okunurluk için içeriği seyrek tuttum; bu da "boş sayfa" izlenimi verebilir.
- **Bu çekimler hiç oynatılmadı.** Ritmi ve kamera kaymalarını yalnız tek tek karelerden değerlendirdim. Özellikle 15,6 sn'lik İZ çekiminde sol sayfadan sağ sayfaya geçiş (423,3–424,6) için tam hızda kısa bir kare dizisi kontrolü önerilir.
- **Mühürde zambak:** 1520 mührünü tek renk balmumunda zambak kabartmasıyla çizdim. Başkanın kararındaki "zambaklı **mavi** top" ifadesini balmumu gerçekliğine göre yorumladım: SA2/KA1 de "balmumu tek renk, zambak kabartmayla seçilir" diyor. Renkli bir arma isteniyorsa mühür yerine kâğıdın başına boyalı küçük bir arma eklenebilir.
