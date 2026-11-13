# SCN-3 · v3.1 "defter ve c2" paketi — kurul tur 3 düzeltmeleri

Tarih: 5 Kasım 2026 · Ajan: SCN-3 · Brif: `BRIF_SCN-3.md` + koordinatörün iki eki (KA1-N2 Machiavelli; TE2 tur 3 G1/G2/G7/Y5/G8).
render.py, git commit/push, `pkill -f` kullanılmadı. Anlatım, ses, `timeline.json` ve altyazı değişmedi. Sayılar ve etiket metinleri aynı; yeni olgu iddiası yok.

## Özet

- **Defter tekrarı (ana madde):** üstten tam açılım defter 102 sn'de **4 → 2**. #72 (İZ) ve #85 (CATASTO) kaldı; ikisi de başlıkları yazılı açılıyor.
  - **#83:** ≥2× yakın plan oldu: kızıl kadife kaplı papalık kasası, el ve anahtarlar, kapağa iğneli kâğıt şeritte 22 düz + 18 kesikli çentik.
  - **#88:** üç çeyrek eğik açıdan kapalı, ciltli defterler ve sandık.
  - Ritim: defter – yakın plan – defter – eğik.
- **Defter içi grafik:** arayüz öğeleri kalktı; yerlerine elle çekilmiş eksen, el yazısıyla yıllar, beşli çetele (ilk 137 yaldızlı), elle cetvellenmiş bantta mürekkep taraması ve çentikler geldi.
- **Hareket ve bağlantı:**
  - #63→#64 ölü bağlantısı giderildi.
  - Kese ve mitra elleri çan eğrisiyle gidip %8 aşmayla oturuyor; tüccarın kolu solmuyor, kadrajdan çekiliyor.
  - `c2_yakin` ve `c2_masa` kendi kameralarında sert kesme uçlarına CUT_SLOPE uygulandı.
  - c2'deki hızlı küçük nesneler `anim.hint_speed` ile deklanşöre bildiriliyor.
- **Küçükler ve TE2 maddeleri:** hepsi yapıldı (ayrıntı aşağıda).
- **qa_flow (2. koşu):** **20 GEÇTİ · 0 KALDI · 1 UYARI · 1 PAS**. v3'te 19 GEÇTİ · 2 UYARI idi; "Beyan ↔ gerçekleşen kamera" UYARI'dan GEÇTİ'ye döndü.
  - 2. koşudan sonra iki küçük değişiklik yaptım (§7). İkisini hedefli denetimle doğruladım; qa_flow'u üçüncü kez koşmadım (brif: en çok iki).

## Değişen dosyalar

| Dosya | Ne | Not |
|---|---|---|
| `c2_kinds.py` | yeni yardımcılar ve türler, #72/#85 yeniden yazımı, `c2_yakin` kamera + kese/mitra/kasa, yeni `c2_defterler`, küçük türler | sahiplik: SCN-3 |
| `scenes_c2.py` | çekim parametreleri (#62, #63, #64, #71, #72, #81, #83, #85, #88, #94/#95, #98), `stamp_hold` | sahiplik: SCN-3 |
| `yonetmen_c2.md` | 24. ve 29. satırın tür sütunu (`c2_masa`→`c2_yakin`, `p1_ledger`→`c2_defterler`) ve değişen çekimlerin açıklamaları | **İki dosya kuralının dışında.** "Yönetmen kartı" kapısı tür sırasını denetliyor; güncellenmeseydi kapı UYARI verirdi. Bu dosyaya ENG-E dokunmuyor. Yalnız c2 kartı, 41 satır korunuyor |

- `p1_ortak.py` ve motor dosyaları (`anim.py`, `cilt_cam.py`, `compose.py`, …) **değişmedi**.
- Motordan yalnız okunanlar:
  - sabitler: `cilt_cam.CUT_SLOPE`, `cilt_cam.CARRY`;
  - yardımcılar: `anim.settle`, `anim.wobble`, `anim.hint_speed`, `anim.speed_of`, `anim.paper_stamp`.
- Ara kayıtlar: başkan değişikliklerimi `f4354b2` ve `10f86ee` ile kaydetti. Yalnız #64 düzeltmesi (§7-2) henüz commit edilmemiş durumda.

**Kanıtlar:** `out_p1/duzeltme/tur3/SCN-3/`, 18 JPEG, her biri ≤1 MB, toplam 5 MB.
- `_ONCE` dosyaları programın çalışmaya başladığım andaki hâlinden (v3 + başkanın bf1645b/e7d6e73 düzeltmeleri).
- `_SONRA` dosyaları son durumdan, aynı zaman damgalarıyla.
- Kare dökümlerini sildim.

---

## 1. Defter tekrarı — ANA MADDE (AN2-Ö1, PK2-N1)

| Çekim | Zaman | Önce | Sonra |
|---|---|---|---|
| #72 İZ | 416,0–431,6 | Üstten açık defter. 416,3'te yalnız "ÇİFTE" yazılıyor (boş açılış); tik etiketli eksen | **Kalır.** "ÇİFTE KAYDIN İZİ" ve "MEDİCİ'NİN FARKI" ilk karede yazılı; eksen ilk karede elle çekilmiş. Kalem yalnız yeni veriyi yazar: CENOVA 1340, PACİOLİ 1494, MEDİCİ İCADI ✗, düğümler. ": YAPI" "yapıdaydı"da eklenir, son metin aynı: "MEDİCİ'NİN FARKI: YAPI" |
| #83 KASA | 475,8–486,4 | Üstten açık defter, iki boş sayfa ("PA…"); altın kapsül dolum çubuğu | **≥2× yakın plan** (`c2_yakin scene="kasa"`), aşağıda |
| #85 CATASTO | 493,6–502,8 | Üstten açık defter, "CA…" açılışı; gri blok; ilerleme çubuğu | **Kalır.** "CATASTO · 1427" ilk karede yazılı; kalem haneleri, bandı ve Strozzi'yi yazar |
| #88 | 511,7–518,3 | `p1_ledger`: üstten açık defter, silik açılış | **Kapalı, ciltli defterler, üç çeyrek eğik açı** (`c2_defterler`), aşağıda |

### #83 → ≥2× yakın plan

Yer: `c2_kinds.py:1511–1714` (`_kasa_base`, `_kasa_strip`, `_notch`, `_yakin_kasa`, `_kasa_keys`), `k_yakin` 1809; `scenes_c2.py:234–245`.

- **Sahne:** kızıl kadife kaplı sandık kapağı; yaldızlı demir kuşaklar, çiviler, ön kenarda kilit aynası; arkada bulanık ceviz masa ve mum.
- **Baş öğe el ve anahtarlar:**
  - El (Giovanni'nin koyu kızıl yeni, yaldız ağız) anahtarları kesmenin içinde taşımaya başlar (hareket üstünde kesme).
  - Hareket `anim.settle` ile çan eğrisi, %8 aşma ve ≈10° bilek dönüşü içerir.
  - "Memurluğu"nda anahtarları kapağa bırakır, açılır ve kadrajdan çekilir; soldurma yok.
  - Taşınırken anahtarlar biraz büyük, gölgeleri uzak (kameraya yakın).
- **Bilgi kâğıt şeritte (cartellino), tüy kalemle:**
  - Başlık ilk karede yazılı: "PAPALIĞIN RESMÎ KASA MEMURLUĞU".
  - "1422" "1422'den"de; **22 düz çentik** ve sürekli cetvel çizgisi "yirmi iki yıl"da; "22 YIL" ve "KESİNTİSİZ".
  - **18 kesikli çentik** (ortası boş iki parça) ve kesik kesik cetvel "on sekiz yıl"da; "+ 18 YIL" ve "ARALIKLI".
  - "MEDİCİ'DE KALDI" kızıl mürekkeple, altı çizili. Sözcükler ve sayılar eskisiyle birebir; dolum çubuğu yok.
- **Kamera:** anahtarlardan şeride iner ve kalemi izler. Sonda (485,73) şeridin tamamı ve anahtarlar birlikte görünür, ≈0,7 sn.
- **Kanıt:** `03_kasa_yakin_plan_83_SONRA.jpg`, `03b_kasa_sonu_83_SONRA.jpg`, `10_defter_grafik_kesitleri.jpg` (çentikler).
- **Çapa notu:** "on" sözcüğü çözümleyicide "sonra" ile eşleşiyordu (alt dize). 18 çentik bu yüzden 480,6'da erken başlıyordu; çapayı "sekiz"e bağladım.

### #88 → kapalı defterler (üç çeyrek eğik açı)

Yer: `c2_kinds.py:1877–2144` (`_Proj`, `_face`, `_def_bg`, `_spine`, `_book_top`, `_book_cover`, sandık yüzleri, `k_defterler`); `scenes_c2.py:287–295`.

- **Çizim:** basit iğne deliği perspektifi, 15° aşağı bakış. Yüzler yerel dikdörtgende çizilip ekran dörtgenine eşlenir (`skia setPolyToPoly`). Yedi deri ciltli defter masada sırt sırta durur; sıra sağa doğru uzaklaşır; ilk defterin ön kapağı görünür.
- **Olgu disiplini:**
  - Sırtlarda yalnız **1397** (ilk) ve **1420** (son); aradaki sırtlar yazısız.
  - **"1397 – 1420"** ortadaki deftere iple asılı kâğıt etikette; kamera kayarken çekim boyunca kadrajda kalır.
  - Defter adı, kişi adı ya da tutar yok.
- **Yanındakiler:** demir kuşaklı sandık, kapağında florin istifleri; arka planda bulanık ofis duvarı, pencere ve raf. #87 ile aynı oda dili, ama kadraj belirgin farklı: geniş yan çekim yerine eğik nesne ayrıntısı.
- **Korunanlar:**
  - `count_up` 150.000, "+" yalnız son değerde, "FLORİN KÂR";
  - "DEFTERLER GÖSTERİR" "defterler" sözcüğünde basar (514,35; KA2 N3).
- **Geçiş:** #87→#88 "sayfa" yerine sert kesme (`link="cam"`), ofisten ayrıntıya. Kamera sağa kayar (bölümün yön sözleşmesi).
- **Kanıt:** `01_defter_tekrari_SONRA.jpg` (alt satır), `04_kapali_defterler_88_SONRA.jpg`.

### Önce / sonra

`01_defter_tekrari_ONCE.jpg` ↔ `01_defter_tekrari_SONRA.jpg`: aynı 16 zaman damgası; satırlar sırasıyla #72, #83, #85, #88.

---

## 2. Defter içi grafik dili: arayüz değil mürekkep (SA1-Y6-k, AN2)

| Öğe | Önce | Sonra | Yer |
|---|---|---|---|
| #85 "9.780 hane" (495,5) | İnce yatay çizgilerden gri blok (barkod gibi) | **Elle beşli çetele** (dört dik + bir çapraz), 9.780 çentik / 1.956 grup. Satır sonları ve girintiler düzensiz, mürekkep yoğunluğu satıra ve gruba göre değişken. İlk 137 çentik "yüz otuz yedi"de **yaldızlanır**; kızıl kalem çizgisi ve "137 HANE". Tam çözünürlükte gruplar seçiliyor | `c2_kinds.py:1257–1312`, 1342 |
| #85 "KAYITLI SERVET" (≈498) | Dikdörtgen ilerleme çubuğu | **Elle cetvellenmiş bant** (titrek kalem çizgisi), içinde %29,8'lik **mürekkep taraması** (çapraz, seyrek karşı tarama), sağ kenarı titrek. "%29,8 · 137 HANE" ve "BİR HESABA GÖRE" aynen | `c2_kinds.py:1315`, 1390–1412 |
| #72 Cenova–Pacioli ekseni (416–424) | Düz çizgi + tik + düzgün yazılı yıllar | **Tüy kalemle çekilmiş çizgi** (titrek, değişken basınç), elle atılmış çentikler, **yıllar el yazısıyla** (`fell_i`, 36 px). "CENOVA 1340 · PACİOLİ 1494 · ETMEDİLER" ve "MEDİCİ'NİN FARKI…" aynen | `c2_kinds.py:1130` (`_hand_line`), 1172–1215 |
| #83 "22 YIL" | Altın kapsül dolum çubuğu | 22 düz + 18 kesikli çentik (§1) | `c2_kinds.py:1599`, 1614 |
| Ek: #71 çifte kayıt paneli | Satır kaydı düzgün sinüs çizgisi (yer tutucu; AN2 not etmişti) | **Okunmaz el yazısı izi** (halkalar, sözcük araları, sağa eğim; sözcük oluşturmaz, tutar/ad yok). İki sütunda aynı iz: aynı kayıt | `c2_kinds.py:706–736`, 774 |

- Masa çizgileri (çarpılar, düğüm bağları, alt çizgiler) da aynı `_hand_line` diliyle çizildi.
- **Kanıt:** `10_defter_grafik_kesitleri.jpg` (beş tam çözünürlük kesit: eksen, taramalı bant, çentikler, çetele, florin), `05_iz_72_SONRA.jpg`, `06_catasto_85_SONRA.jpg`.

---

## 3. Hareket ve bağlantı (AN1 Y-N1, Y-N2, Y-N3, Y7; SA1-N4)

### Ölçüm: kesme noktalarında ardışık kare farkı

Yöntem: 320×180 gri, ortalama mutlak fark. "Önce" v3 videosundan (ffmpeg), "sonra" programdan (deklanşörlü). Video kodlaması küçük farkları biraz yumuşatır; yine de büyüklük farkı açık.

| Yer | Önce | Sonra |
|---|---|---|
| #62 kese, kesme sonrası (355,8–356,1) | 0,21–0,26 | **1,53–1,57** |
| #63 harita, son ≈1 sn (367,9–368,84) | 0,01–0,09 (donuk) | **0,66–0,94** (kesmeye dek) |
| #64 ilk kareler (368,9–369,4) | 0,60–0,67 (boş parşömen) | **1,06–1,09** (BORÇ hazır, pan) |
| #81 mitra başı (469,95–470,3) / sonu (471,4–471,67) | 0,13–0,20 / 0,15–0,21 | **0,65–0,68 / 0,89–0,94** |
| #98 kalem, kesme sonrası ilk adım (575,50) | 0,10 | **2,06** |

### Y-N1 — #63 → #64 ölü bağlantı (367,9–369,3)

`scenes_c2.py:92`, 104, 106–107; `c2_kinds.py:60–76`.

- **#63:** `cam=("pull",)` beyanı kalktı, yerine `("push", rate=0.012)`: %1,2/sn itme, son kareye dek.
  - Sahnenin anahtar kareleri geniş çerçeveden hafif itme ve sağa kayma yapıyor. Son anahtar kesmeden 2,6 sn sonra, yani kamera kesmede hareketli.
  - BRUGGE y ≥ 187 ve BARSELONA y ≤ 870 kalıyor. Bu yüzden kadraj koruması itmeyi durdurmuyor.
  - Kazanç sikkelerinin salınımı 6–7 → 10–11 px, kesmeye dek sürüyor.
- **Ara deneme:** yalnız sabit çerçeve + itme ilk qa_flow'da "Ölçülen hareket" kapısından KALDI aldı (medyan 0,90). Yalnız anahtar karede zum ise son 0,6 sn'de korumaya takılıp donuyordu. Kapının ölçüsünü birebir kopyalayan bir araçla seçenekleri karşılaştırdım; son hâlin medyanı **3,41**.
- **#64:** BORÇ levhası **ilk karede hazır**; "borç" sözcüğünde hafif vurgu (`borc_hit`, sönümlü salınım). FAİZ ve KUR FARKI eskisi gibi kendi sözcüklerinde gelir.
- **Kanıt:** `09_harita_63_SONRA.jpg`, `09b_borc_faiz_kur_64_SONRA.jpg`, `02_…_SONRA.jpg` (2. satır).
- **qa_flow:** "Beyan ↔ gerçekleşen kamera" kapısında "kadraj koruması 1 → 0"; kapı UYARI'dan **GEÇTİ**'ye döndü.

### Y-N2 + SA1-N4 — yakın plan eller

`c2_kinds.py:1716` (`_kese`), 1780 (`_mitra`); `scenes_c2.py:86–88`, 224.

**#62 kese:**
- Kese kesmeden 0,25 sn önce yola çıkar. `anim.settle` ile hareket eder: kesmede 34,6 px/kare, tepe 38,0 px/kare. Sonra pürüzsüz yavaşlar, 52 px (%8) aşar ve −3 px/kare ile geri oturur. Eski sabit hız / iki karede durma deseni yok.
- Yolda bilek −16° → −6° döner.
- Tüccar poliçeyi sürüp oturtur. Ardından açık eli keseye uzanır, keseyi kavrar ve **keseyle birlikte kadrajdan çıkar** (hızlanarak). Hayalet kol yok; kol solmuyor.
- Banker poliçeyi kendine çeker.
- **Kanıt:** `07_kese_62_SONRA.jpg`; `02_…_ONCE/SONRA.jpg` (1. satır).

**#81 mitra:**
- Papalık eli 0,7 sn'de çan eğrisiyle gelir ve %8 aşmayla çekim içinde oturur. Hız profili: 0 → 60 px/kare → 0. Yolda bilek 194° → 186° döner.
- Giovanni'nin elleri nefes alır; el yaklaşınca mitrayı oturmalı biçimde hafifçe kendine çeker.
- Kamera iter (`push` 0,05 → 0,08) ve papalık eline kayar (`drift`).
- **Kanıt:** `08_mitra_81_82_SONRA.jpg`.

**AN2 · 471,7 mitra sürekliliği:** kesmenin iki yanını kare kare inceledim (471,62 / 471,667 / 471,708 / 471,75 / 471,79 / 472,0). #82'nin ilk karesinde mitra Giovanni'nin elinde görünüyor; boşluk yok (`08_…`).

### Y-N3 — kesme girişinde 1 karelik duruş

`c2_kinds.py:1057–1089` (`_ends`, `_herm`, `_wcam`), 1809–1834 (`k_yakin` kamerası), 1433 (`k_masa`).

- Motordaki `cilt_cam` mantığını okudum ve kendi kamera kodumda uyguladım; motor değişmedi.
  - Sert kesmeyle birleşen uçta eğim en az `cilt_cam.CUT_SLOPE`.
  - Geçişle birleşen uçta `cilt_cam.CARRY`.
  - Serbest uçta 0.
- `c2_yakin` itmesi artık bu uç eğimli Hermite eğrisiyle çiziliyor; dünya kamerası (`cams`) `cilt_pano.pchip`'e e0/e1 ile veriliyor.
- `c2_masa`'da yalnız sert kesme uçları değişti (`cut_only`); #72'nin zoomthru uçları eskisi gibi.
- **#98:** `push` 0,0 → 0,05 ve yazı kesmenin 0,15 sn öncesinden başlıyor; kesmede kamera ve kalem hareketli (0,10 → 2,06).
- **#62:** 0,21 → 1,53.
- `c0_belge` (43,9) ENG-E'nin işi.

### Y7 — küçük hızlı nesnelerde deklanşör

`c2_kinds.py:134–136` (`c2_hediye`), 690 (`c2_sadaka`), 789 (`cifte_panel`), 1870 (`c2_yakin`: el, kese, poliçe, anahtar).

- Hız `anim.speed_of` ile hesaplanıp kamera ölçeğiyle çarpılıyor ve `anim.hint_speed(cx, v)` ile bildiriliyor (eşik `compose.SHUTTER_V_HINT` = 8).
- Ölçüm aynı programda yapıldı, ipucu kapalı ve açık; değer: alt-kare bulanık kare / örneklenen kare.

| Yer | İpucu kapalı | İpucu açık |
|---|---|---|
| #67 florin yağmuru (389,4–391,3) | **0** / 23 | **23** / 23 |
| #71 çifte kayıt florini | 0 / 20 | 8 / 20 (yalnız uçarken) |
| #97 sadaka florini | 0 / 32 | 18 / 32 |
| #62 kese elleri | 28 / 56 | 47 / 56 |

- **Kanıt:** `10_defter_grafik_kesitleri.jpg`, son kesit (389,9 sn): sikkelerde dikey hareket bulanıklığı görünüyor.
- **Bedel:** bu karelerde 3 alt örnek çiziliyor, dolayısıyla render süresi o karelerde artar.

---

## 4. Küçükler

- **PK2-Y7 · çifte kayıt (412,9–415,1):**
  - DEBITORI ve CREDITORI altına küçük Türkçe karşılık: "BORÇLULAR", "ALACAKLILAR" (32 px; `c2_kinds.py:758–762`).
  - MİT damgası (1640, 300) → (1600, 590), 104 → 96 px: sağ sütunun boş satırlarına basıyor, CREDITORI başlığını örtmüyor (`scenes_c2.py:155`).
  - **Kanıt:** `02_…_SONRA.jpg`, 4. satır.
- **AN2 · CAVALCANTİ levhası (559,7):**
  - #94 ve #95 aynı `P.plate` tanımını kullanıyor (`scenes_c2.py:60–62`): kesmenin iki yanında aynı yerde ve aynı rol satırıyla. 340 px sıçrama yok.
  - #95'te kamera ittikçe levha sayfanın İtalyanca satırlarını örtmeye başlıyordu. Bu yüzden levha kesmeden ≈0,5 sn sonra sönüyor (`out=("c2s30","kimse",0.15)`); `c2_kalemler` iç levhası `plate=False` (`c2_kinds.py:573`, `scenes_c2.py:337`, 341).
  - **Ek:** tek sayfa çekiminde ANEKDOT damgası "TÜRKÇESİ ÖZET" etiketinin altında kalıyordu (çakışma). Damgayı sağ üste aldım (`c2_kinds.py:653`).
  - **Kanıt:** `11_cavalcanti_94_95_SONRA.jpg`.
- **AN2 · mitra kaybolması:** kapalı (§3).

---

## 5. TE2 tur 3 ek maddeleri (koordinatör)

| Madde | Ne yapıldı | Yer | Önce → sonra |
|---|---|---|---|
| **G1** kadraj kenarında yarım sözcük/sayı (#72, #85, #83) | Kenar söndürmesi: yazının yalnız görünen kısmının ekran kutusu yatayda kenara 90 px'ten yakınsa söner, kenarda 0; dikeyde 30 px payla söner. Bütün defter yazıları (`_write`, `_ink_e`), damgalar (`_stamp_e`), #83 şeridi, #88 sırt etiketleri ve askı etiketi bundan geçiyor. Kamera bir sayfadan ayrılınca o sayfanın kenarda kalan yazıları söner; tam içeridekiler kalır | `c2_kinds.py:1092–1101`, 1104, 1121, 1162 | qa_yerlesim'e yeni eklenen "yarım yazı" kuralıyla (TE2-G1, kutunun %5–95'i ekranda): **c2'de 0 uyarı.** 15 uyarının hepsi #7 ve #10'da (c0). Kareler: `05_iz_72`, `06_catasto_85`, `03_kasa_83` |
| **G2** ETMEDİLER altyazı bandında (#72) | Damga sayfada 170 px yukarı (y0+820 → y0+650), 70 → 68 px; eksen ve "MEDİCİ İCADI" da yukarı alındı | `c2_kinds.py:1213`, 1181–1212 | Harflerin altı y≈872–956, fiş y≈995 → harflerin altı **en çok 769**, fişin altı en çok 810 (416,2–421,4 boyunca, kamera dönüşümünden kare kare) |
| **G7** KENDİ DEFTERİ bantta (#72) | Sağ sayfa sıkıştırıldı (düğümler ve etiketler yukarı), etiketler 870/935 → 735/795; son kamera anahtarları buna göre | `c2_kinds.py:1216–1255`; `scenes_c2.py:165`, 166–168 | y≈939–970 → yazının altı **en çok 838** (429,8–431,6). Ayrıca #85 "%29,8 · 137 HANE": ≈1000–1030 → görünür olduğu sürece en çok **846** |
| **Y5** BELGE · DE ROOVER fişsiz (466,9–469) | `stamp_hold` `CM.stamp` yerine `anim.paper_stamp`; önceki çekimdeki `stamp_ovl` ile aynı kâğıt fişli görünüm | `scenes_c2.py:50–57` | `12_kucukler_SONRA.jpg` (467,2 / 468,2) |
| **G8** DEFTERLER GÖSTERİR ≥1,2 sn | "defterler"de (514,35) basar; mum geçişi başlayana dek (≈517,3) ≈3 sn ekranda. Konum (1460, 860) → (700, 840): kutu y 803–877 (bant dışı), mum geçişinin alevinden (x≈1229) uzak | `scenes_c2.py:294` | `04_kapali_defterler_88_SONRA.jpg` |

---

## 6. KA1-N2 eki: Machiavelli İtalyancası

`c2_kinds.py:585–587` ve `k_kalemler` içindeki satır döngüsü.

- Machiavelli sayfasının özgün satırları teyit metniyle (`kurul/teyit_P1.md:92`, MAC IV) sözcük ve noktalama olarak birebir:
  - "…Muoio contento…"
  - "…non vi recherà mai né invidia né pericolo,"
  - "perché quello che l'uomo si toglie,"
  - "non quello che all'uomo è dato…"
- Dört satır sığsın diye İtalyanca punto 30 → 27 px, satır aralığı 40 → 34 px; aynı değerler Cavalcanti sayfasına da uygulandı (tutarlılık).
  - En uzun satır 430 px (sayfa 620 px).
  - Satırlar 66/100/134/168'de; 4. satırın altı ≈175, Türkçe bloğun tepesi ≈195: çakışma yok.
- Türkçe blok ve "TÜRKÇE SATIRLAR ÖZET · ÇEVİRİ BİZE AİT" etiketi değişmedi.
- **Kanıt:** `12_kucukler_SONRA.jpg` (536,6), `13_c2_genel_SONRA.jpg` (537 / 567,5).

---

## 7. QA

### qa_flow (iki koşu)

- **1. koşu:** 1 KALDI ("Ölçülen hareket": #63 harita 7,7 sn, medyan 0,901 < 1,25). Nedeni ve düzeltmesi §3 Y-N1'de.
- **2. koşu** (`…/scratchpad/scn3_qa.txt`, 13:19). ENG-E aynı anda kendi koşusunu yapıyordu; bellek yetti. Son satırlar:

```
✓ Ölçülen hareket             GEÇTİ    0 çekim >6 sn ve hareketsiz (medyan MAD<1.25)
✓ Beyan ↔ gerçekleşen kamera  GEÇTİ    42 çekim ölçüldü: ulaşmıyor 0, kısmen 0, gerçekleşen <%50/ters 0; kadraj koruması 0; ...
✓ Aynı görüntü kesmesi        GEÇTİ    38 sert kesme: kesin sıçrama 0, sınırda 0, muaf 0
· Donma (ffmpeg)              PAS      video verilmedi (--video yol.mp4)
✓ Yerleşim (ENG-A)            GEÇTİ    qa_yerlesim P1: 303 kare, 77 levha kaydı · İHLAL 0  · düzeltilen 3 · altyazı şeridi 0
✓ Dönem (ENG-A)               GEÇTİ    qa_donem P1 [dönem katmanı açık]: 306 kare, 323 dönem kaydı · İHLAL 0  · uyarı 0
ÖZET: 20 GEÇTİ · 0 KALDI · 1 UYARI · 1 PAS
```

- Tek UYARI "Yön denetimi". v3'teki ile aynı ve önceden vardı: c0 #15 ve c2'nin bilinçli Konstanz `pan l`'si, gerekçesi kartta yazılı.
- c2 için öteki ölçümler: dünya/figür payı %61 → %63; sert kesme %39 → %40; işik geçişi c2'de 2; yönetmen kartı uyumlu.

### 2. koşudan sonra yapılan iki değişiklik ve hedefli doğrulama

1. **#83 son kamera anahtarı** 486,30 → 485,73 (`scenes_c2.py:244`). Şeridin tamamı (1422 dahil) ve anahtarlar sonda birlikte görünsün diye. Başkanın `10f86ee` kaydında var.
2. **#64'te kendi açtığım gerilemeyi düzelttim** (`scenes_c2.py:106–107`).
   - Ne oldu: `borc_at` düzenlemesinde eklediğim yorum satırın ortasına düşmüş ve `faiz_at`, `faiz_x`, `kur_at` parametrelerini yoruma çevirmişti. FAİZ ve KUR FARKI levhaları **hiç görünmüyordu**. qa kapıları içerik eksikliğini yakalamadığı için 2. koşu bu hâliyle GEÇTİ verdi.
   - Rapor hazırlarken satır numaralarını toplarken fark edip düzelttim.
   - Ardından orijinal ve güncel `scenes_c2.py`'deki 41 `shot(...)` çağrısının parametre adlarını AST ile karşılaştırdım. Kalan bütün farklar kasıtlı; başka kayıp parametre yok.
   - **Bu düzeltme henüz commit edilmedi.**

**Hedefli doğrulama:**
- `qa_yerlesim --part 1`: İHLAL 0, c2'de yarım yazı 0.
- Hareket ölçüsü (qa_flow'un birebir kopyası): #83 medyan 12,5 · #88 11,2 · #72 6,5 · #85 6,8 (eşik 1,25).
- #64 kareleri: BORÇ ilk karede, FAİZ "faiz"de, KUR FARKI ✓ "yalnızca"da (`09b_…jpg`).
- **Öneri:** başkanın tam zincirindeki qa_flow bu son hâli bir kez daha sınamalı. ENG-E'nin commit mesajındaki "20 GEÇTİ" koşusu da muhtemelen #64 gerilemesini içeren ara hâlle yapıldı.

---

## 8. Açık kalanlar / emin olmadığım noktalar

1. **#83 yakın plan 10,6 sn.**
   - Bir ara plan için uzun; tek çekim olarak tuttum: el ve anahtarlar açılışta (476–478) ve kapanışta baş öğe.
   - Yazım sırasında (478–485) kadrajı şerit dolduruyor, anahtarlar alt kenarda kısmen görünüyor.
   - "Baş öğe el ve anahtarlar" isteğini bu ara bölümde tam karşılayıp karşılamadığı kurulun gözüne kalıyor.
   - Ölçekte de ihtiyatlıyım: anahtarlar eskisinin ≈1,6 katı. "≥2×", nesnenin önceki geniş plandaki ölçeğine göre sağlanıyor; sayfa yazısı ölçeğine göre değil.
2. **#88 perspektifi.**
   - Basit iğne deliği izdüşümü; yakın defterler perspektif yüzünden hafif "eğik duruyor" gibi okunabilir. Üslupla (guaj kâğıt-kukla) uyumunu oynatarak göremedim.
   - Çekimin sonunda mum geçişi kendi mumunu (1229, 680) defterlerin üstüne çiziyor (motor davranışı, değiştirmedim).
3. **Kenar söndürmesi.**
   - Kamera kayarken kenardaki mürekkep yumuşakça siliniyor; dikkatli izleyici bunu kenar karartması gibi görebilir. TE2'nin önerdiği çözüm bu.
   - Sayfa grafikleri (çetele bloğu, taramalı bant, eksen çizgisi) kenarda kesik kalabiliyor; bunlar yazı değil.
4. **Başkanın #95/#96 etiketleri** ("CAVALCANTİ'YE GÖRE", "TÜRKÇESİ ÖZET · ÇEVİRİ BİZE AİT" y≈880; "TÜRKÇE SATIRLAR ÖZET…" y≈905) koordinatörün "y ≥ 880'e önemli yazı koyma" kuralının sınırında ya da içinde.
   - Yukarı almak #95'te sayfa yazısıyla çakışıyor, bu yüzden dokunmadım.
   - Başkanın kararına bırakıyorum.
5. **#95 sayfası** kesmede (559,7) hâlâ yazısız açılıyor; İtalyanca yazım kesmeyle başlıyor. Önceden vardı, brif listemde yoktu.
6. **#71'de uçan florin** 413,4–413,6'da ≈0,2 sn "ALACAKLILAR"ın üstünden geçiyor (geçici, hareketli nesne).
7. **#85 sağ sayfa** açılışta cetvelli ama boş; kadrajın sağ ≈%30'unda görünüyor. Sol sayfa başlıkla ve yazılan çeteleyle dolu. Sağ sayfaya yeni olgu eklemeden konacak başlık bulamadım.
8. **Yönetmen kartı** (`yonetmen_c2.md`) iki dosya kuralının dışında değişti. Gerekçe: kapı tür sırasını denetliyor.
9. **AN2'nin motor önerisi** (qa_flow'da `c2_masa`/`p1_ledger` için "sayfa" ailesi ve aynı kalıp 100 sn'de ≤2 kuralı) benim alanım değil.
   - Not: c2'de `c2_masa` artık yalnız #72 ve #85'te; `p1_ledger` c2'de yok.
   - #83 (`c2_yakin`) ve #88 (`c2_defterler`) ayrı türler. Böylece ileride eklenecek tür adı temelli bir kural yanlış sayım yapmaz.
10. **Ölçüm koşulları:** "önce" kare farkları v3 videosundan (H.264), "sonra" programdan. Kodlama farkı nedeniyle mutlak değerler birebir karşılaştırılamaz; fark büyüklükleri yine açık.
