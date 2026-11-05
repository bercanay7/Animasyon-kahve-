# SCN-1 · Kurul tur 2 düzeltmeleri: c0 (0–101 sn) ve c1 (105,7–339,8 sn)

**Durum:** A–D maddelerinin hepsi uygulandı. Başkanın sonradan verdiği ek işler (B8 kule şeridi, Villani yazımı) ve SCN-2'nin `donem.py` API isteği de kapandı.
- Render, miks ve git kullanılmadı.
- Anlatım zaman çizelgesi ve bölüm sınırları değişmedi. Yeni ya da kayan bütün çekim sınırları cümle/sözcük çapalarına bağlı.

**Kanıt klasörü:** `out_p1/duzeltme/tur2/SCN-1/` (16 JPG).
- **ÖNCE:** v2 videosundan alınan kare (`out_p1/medici_P1.mp4`).
- **SONRA:** güncel kodla, tam motorla üretilmiş tek kare (`compose.Program(part=1).frame`).
- SONRA karelerinde ENG-C ve ENG-D'nin paralel değişiklikleri de görünür (ör. figür başlıkları, damga zeminleri, ışınsız ışık geçişi). Benim yaptığım fark, her satırın etiketinde yazan şeydir.

Çekim numaraları güncel `qa_flow` tablosundaki indislerdir; kurulun v2 numarası farklıysa parantez içinde verdim.

---

## 1. Özet tablo

| Madde | Ne yapıldı | Kanıt | Kapanan kurul maddesi |
|---|---|---|---|
| A1 "BUGÜN" kuyruğu HUD | gizli | `A1-A5_HUD.jpg` | AN2-K5, SA2-Y3 ("BUGÜN" kolu) |
| A2 Dante HUD | gizli (+ levha kenar payı) | `A1-A5_HUD.jpg`, `A8b_lorraine_dante.jpg` | SA2-Y3, KA1-Ö4b, KA2-D2 |
| A3 Villani HUD 1338 | c1s5 başında 1338; c1s6 adımı birleşti | `A1-A5_HUD.jpg` | SA2-Y3, KA1-Ö4b |
| A4 Machiavelli HUD | iki çekimde gizli | `A1-A5_HUD.jpg` | KA2-D2 |
| A5 evlilik sözleşmesi HUD 1385 | 27b'de 1385, c1s28'de 1397 | `A1-A5_HUD.jpg` | KA1-Ö4a (başkan kararı kadarı; kalıntı §5) |
| A6 "MEDİCİ HANEDANININ SON ÜYESİ" | iki satır | `A6-A8_metin.jpg` | KA2-D3 |
| A7 Villani levhası (Buonaccorsi) | yeni rol metni | `A6-A8_metin.jpg` | SA2-Y5, KA1-Ö2, KA2-D4 |
| A8 tr_upper tutarlılığı | c0–c1 tek biçim | `A6-A8_metin.jpg`, `A8b_lorraine_dante.jpg` | TE2-Ö12 (c0–c1) |
| B Loggia dei Lanzi kuralı | donem + qa_donem + cilt_sehir | `B_loggia.jpg` | SA2-Y2, KA1-Ö1 |
| C1 "13 MADDE" kutusu | kâğıdın dışında, belgeye bağlı | `C1_13madde.jpg` | qa_yerlesim çakışması |
| C2 CİOMPİ LONCASI etiketi | altyazı bandının dışında | `C2_C3_etiket_damga.jpg` | TE2-Y3 |
| C3 VİLLANİ'YE GÖRE damgası | kartın üstünde, çakışmasız | `C2_C3_etiket_damga.jpg` | KA1-K4, TE2-Y5 (çakışma kolu) |
| C4 kesik/çakışan harita etiketleri | 2 yer | `C4_harita_etiket.jpg` | SA2-K14 sınıfı (c1 payı) |
| C5 Orsanmichele | kübik Gotik simge | `C5_orsanmichele.jpg` | SA2-K3 |
| C6 1743 odası perde + uyuyan | kenar yumuşatma + örtülü beden | `C6_oda1743.jpg` | SA1-Ö4 (a)+(b) |
| D1 sıçrayan kesmeler (4) | ×1,55–1,64 ya da tek çekim | `D1_sicrayan_kesmeler.jpg` | AN2-Ö1 (c0–c1 kesmeleri) |
| D2 sikke ölü açılışı | sikke kesmede tam | `D2_sikke_kesme.jpg` | AN1-Y5 |
| D3 sessiz cepler | kese yürüyüşü + kamera | `D3_D4_talepler_kose.jpg` | AN1-Y4 (c1_kose, talepler) |
| D4 talepler kartı | 8,3 → 4,2 sn; Signoria çekimi; gerçek harf | `D3_D4_talepler_kose.jpg` | AN2-K3 (+AN2-K2 bu kart için) |
| D5 ışık patlaması | c0+c1'de 5 → 2 | `D5_isik_gecisleri.jpg` | AN1-Y8, SA1-Y7 (c0–c1 payı) |
| D6 17. yy şapkaları | sahne tarafında dönem başlıkları | `D6_baslik.jpg` | SA2-K7 (sahne kolu) |
| Ek: B8 kule şeridi | `XD` 700 → 730 | `B8_kule_serit.jpg`, `B8b_kule_serit_c1.jpg` | SA1-K3 / B8 |
| Ek: Villani literali | `c1_kinds` + LORRAİNE | `A8b_lorraine_dante.jpg` | TE2-Ö12 |
| Ek: `donem.nesne_yili` | resmî API | (birim sınaması, §2-Ek) | SCN-2 isteği 2 |
| ENG-D kamera kapısı (#12/#37/#55) | beyanlar düzeltildi | `qa_flow` | AN1-Y2 (c0–c1 payı) |

---

## 2. Ayrıntı

### A. Yıl göstergesi (HUD) ve metin

**A1 · `scenes_c0.py` #14 `c0_kuyruk` (78,0–86,6 sn):** `hud=False`.
- Kanıt: `A1-A5_HUD.jpg`, 82,0 sn. Önce HUD 1737, sonra HUD yok.

**A2 · `scenes_c1.py` #21 `c1_cicek` Dante (119,4–127,1 sn):** `hud=False`.
- DANTE levhası x 381 → 430. Levha kamera itmesiyle dışa kayıyordu; motor kutuyu sağa itiyordu (qa_yerlesim "düzeltildi" 2). İtme sonunda (z≈1,13) sol kenar ≥90 px, "lanetli çiçek" levhasıyla arası ≈70 px.
- Kanıt: `A1-A5_HUD.jpg` 124,0 sn; `A8b_lorraine_dante.jpg` 127,0 sn.

**A3 · `scenes_c1.py` `YIL_AT`:** `(("c1s5", -0.2), 1338)`. c1s6'daki ayrı 1338 adımı gereksizdi, kaldırıldı.
- Darphane artık tek çekim (D1). HUD, Villani cümlesinin başında (130,4 sn) 1338'e geçer.
- Kanıt: `A1-A5_HUD.jpg`, 133,2 sn. Önce 1252, sonra 1338.

**A4 · `scenes_c1.py` #45–#46 (Machiavelli, 252,5–267,3 sn):** iki çekimde de `hud=False`.
- Kanıt: `A1-A5_HUD.jpg`, 256,0 sn.

**A5 · `YIL_AT`:** `(("c1s27", "hanedanın", -0.3), 1385)`, ardından mevcut `(("c1s28", "1397'de", -0.1), 1397)`.
- Aynı çekimde (#54 `p1_doc`, 27b) "İLK SERMAYE" damgası başlığın üstünden alındı: (1250, 545); halka (880, 655).
- Kanıt: `A1-A5_HUD.jpg`, 309,5 sn. Önce HUD 1390 ve başlığı örten damga; sonra HUD 1385 ve damga başlığın altında.

**A6 · `scenes_c0.py` #2 `p1_palle` (9,1–13,3 sn):** "MEDİCİ HANEDANININ / SON ÜYESİ", iki satır.
- Yeni yardımcı `c0_kinds.tag_lines`: `P.tag` görünümü, çok satırlı, `x_min=990` ile armadan uzak.
- Kanıt: `A6-A8_metin.jpg`, 12,0 sn.

**A7 · `scenes_c1.py` Peruzzi sayım odası (c1s10, 172–181 sn):** rol satırı "1300'DE PERUZZİ ORTAĞI · YÖNETTİĞİ BUONACCORSİ 1341'DE BATTI". Tek satıra sığdı (`w=1030`), güvenli alanın içinde.
- Kanıt: `A6-A8_metin.jpg`, 176,0 sn.
- Not: rol satırındaki rakamlar eski stil ("13oo") çıkıyor. Bu, motordaki `name_plate` rol yazı tipinden geliyor (TE2-Y11) → ENG-C/ENG-D isteği.

**A8 · tr_upper (TE2-Ö12, c0–c1):** bütün ekran yazıları tarandı. Son durum:
- **c0:** ANNA MARİA LUİSA · LORRAİNE TARAFI (bu turda eklendi) · UFFİZİ · MEDİCİ HANEDANININ SON ÜYESİ.
- **c1:** GİOVANNİ VİLLANİ · VİLLANİ'YE GÖRE · BOCCACCİO · MARCHİONNE Dİ COPPO STEFANİ · SALVESTRO DE' MEDİCİ · GONFALONİERE · CİOMPİ / CİOMPİ LONCASI / CİOMPİ'NİN TALEPLERİ · MİCHELE Dİ LANDO · MACHİAVELLİ · GİOVANNİ Dİ BİCCİ · VİERİ Dİ CAMBİO · PİCCARDA BUERİ'NİN ÇEYİZİ · ORSANMİCHELE · VİA PORTA ROSSA · BUONACCORSİ · PERUZZİ.
- **Kullanılmayan tür:** `c1_kinds.c1_kardes` içindeki "GIOVANNI VILLANI" ve "VILLANI'NİN KARDEŞİ" de düzeltildi (başkanın ek işi).
- **CATASTO:** c0–c1'de bu sözcük hiç geçmiyor.
- **Bilerek dokunulmadı:** 1737 belgesindeki el yazısı "ITALIANO". Diegetik bir İtalyanca sözcük; noktalı İ belgeye yabancı düşer. Romen rakamları (I–XIII) da olduğu gibi kaldı.
- Kanıt: `A6-A8_metin.jpg` (224,9 sn SALVESTRO DE' MEDİCİ; 242,0 sn MİCHELE Dİ LANDO), `A8b_lorraine_dante.jpg` (38,85 sn LORRAİNE TARAFI).

### B. Loggia dei Lanzi (SA2-Y2 / KA1-Ö1)

**`donem.py`:** `loggia_stage(y)` eklendi.
- y yok → eski çizim;
- <1376 → 0,0: yapı yok, yerinde sıradan ev cepheleri;
- 1376–1381 → 0,5: ayaklar ve iskele;
- ≥1382 → 1,0: tam yapı.
- Sabitler: `LOGGIA_START=1376`, `LOGGIA_DONE=1382`.

**`qa_donem.py`:** aynı kuralın bağımsız kopyası.
- İhlaller: `loggia_erken`, `loggia_tam_erken`, `loggia_yok_gec`. Uyarı: `loggia_eksik`.
- Dönem katmanı kapalıyken (`disable_period`) Loggia 1,0 sayılır, yani "önce" ölçümü yapılabilir.

**`cilt_city.py`:**
- `era_key` 5'li oldu (Loggia aşaması eklendi).
- `era_tag`/`note_era` ilk dördünü kullanır; eski önbellek adları ve kayıtlar bozulmaz.
- Yeni: `loggia_of(era)`, `loggia_tag(era)`.

**`cilt_sehir.py`:**
- Yeni çizimler: `ev_cepheleri` ve `loggia_insaat`.
- Meydan ana katmanının önbellek etiketi Loggia aşamasını içerir.
- `_draw_main` aşamaya göre dallanır. Loggia yokken ya da inşaattayken bayraklar asılmaz.

Kanıt (`B_loggia.jpg`):
- 141,8 sn (1338): Loggia yerine ev cepheleri.
- 238,6 sn (22 Temmuz 1378): ayaklar ve iskele.

### C. Yerleşim ve okunurluk

**C1 · `scenes_c0.py` #7 `c0_belge` (7a):** "13 MADDE" artık kâğıdın dışında, masada duruyor.
- Belge düzlemine bağlı: doc (−760, −25), yeni yardımcı `c0_kinds.belge_sayac`.
- Kamera sağa kayınca kâğıtla birlikte kadrajdan çıkar, "Fransızca"da söner. Romen rakamlarının üstüne hiç binmez.
- Kanıt: `C1_13madde.jpg`, 41,5 ve 43,1 sn.

**C2 · `c1_kinds.k_lonca`:** "CİOMPİ LONCASI" etiketi kalkanın sağına alındı (y≈880). Altyazı bandının (938–1042) dışında, "ARMALAR TEMSİLÎ" hizasına yakın.
- Kanıt: `C2_C3_etiket_damga.jpg`, 274,0 sn.

**C3 · `scenes_c1.py` #23 `p1_sehir` 1338:** "VİLLANİ'YE GÖRE · TAHMİN" damgası (1030, 196) konumuna, rot −0,04 ile alındı. ≈90.000 kartının üstünde, ona değmiyor.
- Damga zemini ve kontrastı ENG-C'nin işi.
- Kanıt: `C2_C3_etiket_damga.jpg`, 143,0 sn.

**C4 · Harita etiketleri:**
- **c0 #12 `c0_harita`:** "SINIR YAKLAŞIKTIR" etiketi "3. MADDE · ÖZET" kartının üstüne biniyordu (qa_yerlesim çakışma kuralı). (330, 300) konumuna, haritanın sol üstüne alındı. Kanıt: 68,8 sn.
- **c1 #51 `p1_map` Roma:** v2'de kesik değildi. Güncel kamera motoruyla eski son anahtar (12.3, 42.2, 5.0) "FLORANSA"yı üst çerçeveye itiyordu. Son anahtar (12.15, 42.55, 4.3) yapıldı.
  - Kanıt satırı: "eski anahtar + güncel motor" ile "yeni anahtar" karşılaştırması, 294,0 sn.
- c2'deki BRUGGE ve BARSELONA etiketleri SCN-2'nin.
- Kanıt dosyası: `C4_harita_etiket.jpg`.

**C5 · Orsanmichele (`c1_kinds._orsanmichele`, `k_kose`):** alınlıklı "Yunan tapınağı" yerine kübik Gotik blok çizildi.
- Zemin katta üç sivri kemerli açıklık (ajurlu), üst katlarda ikiz pencereler, düz saçak.
- "ORSANMİCHELE" levhası yanda.
- `icons*.py`'ye dokunulmadı; simge yalnız bu türde kullanılıyor.
- Kanıt: `C5_orsanmichele.jpg`, 320,5 sn.

**C6 · `cilt_oda.py` (yalnız oda1743):**
- **(a) Perde:** basamakların nedeni, kırpma yolunun şerit kutularından (8 px saydam pay dahil) geçmesiydi. `_drape_aa_1743` perdenin gerçek kenarından kenar yumuşatmalı kırpar; yalnız oda1743 kullanır.
- **(b) Uyuyan figür:** `lying_sil(cover=…)` ile yorgan bedenin biçimini alıyor. Baş yastıkta, temas gölgesi var. `SLEEP_COVER` yalnız oda1743'te açık.
- Kanıt: `C6_oda1743.jpg`, 6,0 sn.

### D. Kurgu ve hareket

**D1 · Sıçrayan kesmeler (AN2-Ö1).** `qa_flow` "Aynı görüntü kesmesi": 37 sert kesme; kesin sıçrama 0, sınırda 0; `jump=True` hiç kullanılmadı.

| Kesme | Ne yapıldı |
|---|---|
| **#8, 43,86 sn (×1,21)** | 7b kesmede ×2,1'de açılıyor; 7a sonu ×1,28 olduğu için ×1,64. Konu ITALIANO satırı. Yakında yavaş itme, çizgide geri çekiliş. |
| **#23, 130,44 sn (×0,99, +80 px)** | 5a ve 5b tek çekim oldu (#22 `c1_darphane`, anahtar kareli kamera). "Villani"de uçan sikkeleri izleyerek sağa kayar; kesme yok. |
| **#46, 258,36 sn (×1,15)** | 21b isyancıya yakın planla açılıyor: ×2,0 / ×1,22 = ×1,64, konu değişiyor. "koydu"da geri çekilip yazan tarihçiyi açar. Soru işareti ve tomar oda kamerasına bağlı (`c1_kinds.oda_bagli`). |
| **#58, 333,30 sn (×1,01, −156 px)** | 32 defter ve florin yakın planıyla açılıyor: ×2,45 / ×1,58 = ×1,55, konu nesne. Sonra salonu, "FAİZ GÜNAHTIR" tabletini ve haçı açar. |

Kanıt: `D1_sicrayan_kesmeler.jpg` (her kesmenin önceki/sonraki karesi).

**D2 · #53 `p1_coin` (302,3 sn):** sikke `at=-1.0`. Kesme anında tam ve keskin; boş parşömende soluma ve yarım sikke dikişi yok.
- Kanıt: `D2_sikke_kesme.jpg`, 302,3 ve 302,5 sn.

**D3 · Sessiz cepler (AN1-Y4):**
- **#56 `c1_kose` (316,9–323,4 sn):** anlatıya bağlı ikinci sürekli hareket eklendi ("işi … köşeye taşıdı"). Florin kesesi "Via"da Via Porta Rossa boyunca yürür, ardında mürekkep izi bırakır, "köşeye"de iğne düşer. Yayalar ve ışık süpürmesi var. Kamera `("push", 0.10)`, ≈%1,5/sn.
  - Kanıt: `D3_D4_talepler_kose.jpg`, 319,6, 321,0 ve 322,6 sn.
- **Talepler:** D4'e bakın.
- `qa_flow` "Ölçülen hareket": GEÇTİ (0 çekim >6 sn ve hareketsiz).

**D4 · Ciompi'nin talepleri (AN2-K3), 244,9–252,5 sn:**
- **Yeni #43 `p1_oda` salon/signoria (244,9–248,3 sn):** Mayıs'taki kura sahnesinin salonu, yani aynı saray.
  - Ciompi temsilcisi dilekçeyi okur; tomarda gerçek harflerle "Vergide adalet" yazılı (`c1_kinds.dilekce_tomar`).
  - Priorlar arkada oturur. Kamera 1,16 → 1,36 itiyor. Tomar ve "YAZILDIĞINA GÖRE" oda kamerasına bağlı.
- **#44 `p1_doc` kart, 4,2 sn (248,3–252,5 sn):** kâğıt kesmede hazır.
  - Üç satır kendi sözcüğünde gerçek harflerle yazılıyor: "Vergide adalet / İşçilere lonca hakkı / Kamu borcunun azaltılması".
  - Boş alan küçüldü (`w=1040, h=500`).
- **Ekrana yeni olgu girmedi:** üç satır anlatımın sözcükleri; v2 kartında da vardı.
- Kanıt: `D3_D4_talepler_kose.jpg`, 247,6, 249,0 ve 251,9 sn.

**D5 · Işık patlaması (AN1-Y8):** c0+c1'de v2'de 5 vardı, şimdi 2.
- **Kalanlar:** #1, 1743 odası (açılış ifşası); #50, "GİOVANNİ Dİ BİCCİ" (asıl hikâyenin ifşası).
- **Değişenler:**
  - #13 `c0_gerekce`: sayfa geçişi (`lead=True`, başlık ve halkalar çizilerek açılıyor; ölü açılış yok).
  - #22 darphane: sert kesme.
  - #45 Machiavelli: sayfa geçişi (`place="after"`, cümleler arası nefeste).
- `qa_flow` "Işık geçişi bütçesi": c0 1 · c1 1 · c2 2.
- Kanıt: `D5_isik_gecisleri.jpg`.

**D6 · 17. yy şapkaları (SA2-K7, sahne kolu):** figür kitinin `hat=` geçersiz kılmasıyla dönem başlıkları verildi.
- Veba odası figürü (#32): `coif`.
- Yün tarayıcısı (`c1_kinds.k_lonca`): `coif`.
- İsyancı (#45, #46): `coif`.
- Signoria salonu (#43): prior `mazzocchio`, temsilciler `coif` ve `woolcap`.
- Kanıt: `D6_baslik.jpg`, 191,0, 231,6 ve 262,0 sn. Geniş kenarlı şapka yok.

### Ek işler (başkanın 2. mesajı ve SCN-2 istekleri)

**B8 / SA1-K3 · kuledeki beyaz şerit (`cilt_sehir.py` `SkylineDikey._draw_city_v`):** `XD` 700 → 730.
- **Neden:** çan kulesinin merkezi XD+1,5·205; gövdesi ±40,5 px, saçağı ±48 px. Palazzo Vecchio gövdesi 975–1265. XD=700'de saçak 959,5'ten başlıyordu, yani ≈15 px taşıyordu.
- **XD=730'da:** saçak 989,5'ten başlıyor; çan kulesi tamamen gövdenin arkasında. Kubbe (XD±160 → 570–890) solda görünür kalıyor.
- **Önbellek:** sürümü dosya içeriğinin özeti (`VER = crc32(cilt_sehir.py)`), yani eski kareaşlar kendiliğinden geçersiz. Eski `sehir_dikey_*` dosyalarını silmek gerekmedi: baktığımda diskte yalnız yeni sürüm vardı.
- **c2 doğrulaması:** 585,07, 586,0 ve 588,0 sn'de şerit yok (`B8_kule_serit.jpg`).
- **c1'de de etkili:** aynı dünya c1'deki #42 Michele di Lando kule çekiminde (239,8–244,9 sn) de kullanılıyor. v2'de 240,7 ve 242,4 sn'de aynı şerit vardı, şimdi yok (`B8b_kule_serit_c1.jpg`). `qa_donem` ve `qa_yerlesim` bu değişiklikten sonra koşuldu: 0 / 0.

**Villani literali:** `c1_kinds.py` `c1_kardes` → "GİOVANNİ VİLLANİ", "VİLLANİ'NİN KARDEŞİ".
- Tarama sırasında `scenes_c0.py` 7a/7b'de kalan "LORRAINE TARAFI" bulundu, "LORRAİNE TARAFI" yapıldı (`A8b_lorraine_dante.jpg`).

**SCN-2 isteği 2 · `donem.nesne_yili` (resmî API, yalnız ekleme):**
- `with donem.nesne_yili(1520): …` çekimin cx'ini korur. İç içe ckind'ler yılı devralır; `qa_donem` kaydı aynı çekim indisine düşer.
- **Fark:** çıkışta yığın derinliğini ve "son bağlamı" (`_LAST`) girişteki hâline geri yükler.
- **Birim sınaması geçti:** çekim içi, ekran uzayı kaplaması (yığın boş), istisna, `y=None`.
- **Bulgu:** p1_ortak'taki yerel `nesne_yili`, `seal_drop` gibi ekran uzayı kaplamasında kullanıldığında çıkışta `donem.pop()` çağırıyor. Bu `_LAST`'ı 1520 çerçevesine çeviriyor; aynı karede sonradan çizilen katmanlar 1520'yi görüyor. Sınadım: yerel çözüm sonrası yıl 1520, resmî API sonrası 1429.
- P1'de görünür bir etkisini bulmadım, ama P2–P7 için risk. → SCN-2/başkan isteği 1.

**ENG-D "Beyan ↔ gerçekleşen kamera" kapısı (c0–c1 KALDI'ları):**
- **#12 `c0_harita`:** `("truck","r", ease="in")`; kayma kilit anına doğru hızlanıyor.
- **#37 `c1_yazi`:** `push` → `pull`. Çekim gerçekte çekiyor.
- **#55 `p1_map` 1397:** `pull` → `push`. Harita anahtar karelerinde Floransa'ya yaklaşıyor; eski beyan TERS'ti.
- **Tek tek yoklama** (ENG-D'nin `_probe_cam`'ı): üçü de A testinde oran 1,0; #55 B testinde gerçekleşen/beyan 7,8. Tam koşuda c0–c1'de bulgu 0.
- Yönetmen kartları (`yonetmen_c0.md`, `yonetmen_c1.md`) yeni çekim listesine ve beyanlara göre güncellendi.

---

## 3. QA sonuçları (son koşular; çıktılar `…/scratchpad/fix_scn1/qa/`)

**`qa_yerlesim.py --part 1`**
- 303 kare, 80 levha kaydı.
- **İHLAL 0** · düzeltilen 0 · altyazı şeridi 0 · uyarı 0. P1'in tamamı.
- Dante düzeltmesinden önce "düzeltilen 2" vardı.

**`qa_donem.py --part 1`**
- 306 kare, 323 dönem kaydı · **İHLAL 0** · uyarı 0.
- Bağımsız Loggia kuralının çalıştığının kanıtı: `--eski` (dönem katmanı kapalı) koşusu 1338 karesini yakalıyor (139,3 sn: `loggia_erken` 1, `loggia_tam_erken` 2).

**`qa_flow.py --part 1 --no-eng-a`**
- **17 GEÇTİ · 0 KALDI · 2 UYARI · 1 PAS.**
- Bu görevin ilk koşusu: 16 GEÇTİ · 1 KALDI · 2 UYARI. KALDI 1 → 0.

| Kapı | Sonuç |
|---|---|
| Beyan ↔ gerçekleşen kamera | UYARI. Tek madde c2'de: #63 `p1_map`, kadraj koruması. c0–c1'de 0. |
| Aynı görüntü kesmesi | 0 |
| Işık geçişi bütçesi | 4 (c0 1 · c1 1 · c2 2) |
| Yönetmen kartı | GEÇTİ |
| Yön denetimi | UYARI: #15 `p1_skyline` "nasıl geldi?" bilinçli ters yönü. v2'den kalma; AN1-Y12 "kabul edilebilir" dedi; gerekçesi `yonetmen_c0.md`'de yazılı. Dokunmadım. |

---

## 4. İstekler

**SCN-2'ye (SCN-2 bitirdiği için başkana):**
1. **`p1_ortak.nesne_yili` → `donem.nesne_yili`.** Tek satır: sınıfı `DN.nesne_yili`ye devret ya da `nesne_yili = DN.nesne_yili`. Ekran uzayı kaplamasındaki `_LAST` sızıntısını kapatır (§2-Ek).
2. **`cilt_oda.draw_drape`:** basamaklı perde kenarının nedeni bütün odalarda aynı: kırpma yolu, 8 px saydam pay dahil şerit kutularından geçiyor. Ben yalnız oda1743'ü düzelttim (`_drape_aa_1743`). Çapraz bağlı perdeli öteki odalar da aynı yöntemi alabilir.
3. **Yatak odaları (ör. P1Yatak):** `lying_sil(cover=…)` ve `SLEEP_COVER` hazır; isteyen oda açabilir.
4. **Bilgi:** SCN-2'nin `scenes_c1.py` 26b'deki `variant="roma"` değişikliği korundu.

**P2 sahibine (`c3_kinds.py` `DikeyP2`):** aynı `_draw_city_v`'nin kopyasında `XD = 700` duruyor. Aynı çan kulesi dilimi orada da çıkar; 730 önerilir.

**ENG-C'ye:**
1. **Dönem başlıkları:** kit yıla göre varsayılan başlık (cappuccio/coif/mazzocchio) verdiğinde benim sahne geçersiz kılmalarım kaldırılabilir. Zararsızlar, kalabilirler de. Yerleri: `scenes_c1.py` #32, #43, #45, #46 ve `c1_kinds.k_lonca`.
2. **TE2-Y11:** `name_plate` rol satırında hizalı rakam (`lnum` ya da Cinzel). Villani levhasında "1300" hâlâ "13oo" gibi okunuyor.

**ENG-D'ye:** bu turda açık isteğim yok. Önceki yoklamada `qa_flow.py` 783. satırdaki çökme düzelmiş; son koşu temiz.

**Başkana (karar):** A5'in kalıntısı için §5'e bakın (KA1-Ö4a).

---

## 5. Açık kalanlar

**KA1-Ö4a kalıntısı (başkan kararı gereği bırakıldı).** 27a (302,4–307,9 sn: sikke ve "PİCCARDA BUERİ'NİN ÇEYİZİ") hâlâ HUD 1390 altında. HUD sırası: 1378 → 1390 (297,7) → 1385 (307,9) → 1397. Karar 27b ile sınırlıydı; ben de öyle uyguladım. Tek satırlık iki seçenek:
- **(a)** `(("c1s27", -0.1), 1385)` ekle. Çeyiz de 1385 olur; geri adım c1s27'nin sert kesmesine, anlatımdaki geri dönüşe denk gelir.
- **(b)** KA1'in tam önerisi: `(("c1s26", "Roma'da", -0.1), 1385)` ekle, 1390 adımını kaldır. HUD hiç geri gitmez; 1390 bilgisini "1390'LARIN BAŞI" levhası taşır.

**Diğer açıklar:**
- **TE2-Y11** (eski stil rakamlar): motor tarafında (§4 ENG-C 2).
- **Loggia 1376–1381:** tek bir "inşaat" görünümü (ayaklar + iskele). Yıla göre kademeli yükselme yok.
- **Yönetmen kartları:** `yonetmen_c0.md` ve `yonetmen_c1.md` sahiplik listemde değildi. `qa_flow` "Yönetmen kartı" kapısı shots ile birebir uyum istediği için güncelledim (c0 17, c1 41 satır).
- **Tam hızda görülmedi.** Yalnız tek tek karelerle denetlendi:
  - sayfa geçişleri (#13 `lead`, #45 `place="after"`);
  - kese yürüyüşü;
  - 21b geri çekilişi;
  - yeni #43 salon çekiminin ritmi (3,4 sn).
  - Bunlar için kısa bir kare dizisi kontrolü önerilir.

---

## 6. En emin olmadığım nokta

**Asıl:** 22 Temmuz 1378 meydanındaki Loggia'nın inşaat görünümü.
- Kural (1376–1381 = ayaklar + iskele) başkanın kararı. Ama Temmuz 1378'de yapının ne kadar yükseldiğini bilmiyorum; KA1 de aynı belirsizliği yazmış ("genel bir öneri").
- Ekrandaki "ayaklar ve iskele" bir tahmin. Sağ kenarda küçük ve geri planda olduğu için yanlış okunma riski düşük.

**İkincil:** yeni Signoria okuma çekimi (#43).
- Sahne bir canlandırma: talepleri bir temsilci priorlara okuyor.
- Ekrana yeni yazılı olgu girmedi: tomarda anlatımın "Vergide adalet"i, etikette "YAZILDIĞINA GÖRE".
- Ama sahneleme, taleplerin salonda resmen okunduğunu ima ediyor. Kurul bunu fazla somut bulabilir. O durumda çekim kesilir; kart 4,2 sn hâliyle tek başına durur.
