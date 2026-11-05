# ENG-D · Kurul tur 2 düzeltmeleri: kamera, geçişler, QA kapıları (Medici P1)

- **Tarih:** 05.11.2026
- **Alan:** motor dosyaları. `compose.py`, `shots.py`, `cilt_cam.py`, `cilt_pano.py`, `cilt_fx.py`, `qa_flow.py`. `p1_ortak.py`'de yalnız `_wrap` ve harita sarmalayıcısı, `kapak_medici.py`'de yalnız `k_kapak_kilit` hareketi.
- **Dokunmadıklarım:** `mapsk.py`, `fx.py`, sahne dosyaları.
- **Yapmadıklarım:** render, miks, git.
- **Kanıtlar:** `out_p1/duzeltme/tur2/ENG-D/` (01–13). Ölçüm betikleri ENG-D çalışma alanında.

## 0. Kısa sonuç

| # | Görev | Durum | Kapanan kurul maddeleri |
|---|---|---|---|
| 1 | Beyan edilen kamera (kapak yankısı + haritalar) + "Beyan ↔ gerçekleşen kamera" kapısı | **Kapandı.** Tek UYARI: #63 harita, kadraj koruması (SCN-2 isteği). | AN1-Y2; PK2-Y8'in durağanlık kısmı |
| 2 | "Aynı görüntü kesmesi" kapısı + sert kesme payının yeni sayımı | **Kapandı** | AN1-Y3, AN2-Ö1 |
| 3 | Işık geçişi: yıldız ışınları kalktı + parça başına ≤4 kapısı | **Kapandı** (P1'de 4) | AN1-Y8, SA1-Y7 |
| 4 | Şerit ucunun açılması (alay frizi) | **Kapandı** | AN2-K1, TE1-Y5 |
| 5 | Set kenarı (545,5 sn) | **Kapandı** | AN1-Y10 |
| 6 | Kesmede 1 karelik kamera duruşu | **Kısmen.** Duruş 6 → 2. Kalan ikisi `c2_yakin`'in kendi kamerasında (SCN-2 isteği). | AN1-Y11 |
| 7 | Bitiş ekranı | **Kapandı.** Miks kuyruğu yeniden üretilmeli. | PK2-Y6, SA1-Y8 |
| 8 | Kâğıt dokusu dünyaya kilitli + döngüsüz gren | **Kapandı.** Kare süresi +%3,4. | TE1-Y8 (§7 önerisi) |
| + | Segment başında deklanşör | **Kapandı** | TE1-Y1 |

**Son ölçüm (güncel ağaç, 05.11 08:00; 07:37 koşusuyla birebir aynı):**
- `qa_flow.py --part 1`: **19 GEÇTİ · 0 KALDI · 2 UYARI · 1 PAS** (kanıt: `09_qa_flow_P1_son.txt`).
  - UYARI 1: eski yön uyarısı, #15 `p1_skyline`. AN1-Y12 bunu "kabul edilebilir" sayıyor.
  - UYARI 2: #63 kadraj koruması.
- `kapak_qa.py --part 1`: K1 ve K2'de 0 hata, 0 uyarı.
- `qa_flow.py --part 2` duman testi hatasız bitti (kanıt: `10_qa_flow_P2_duman.txt`). Sonuç ve P2 notları §3'te.

---

## 1. Görevler

### 1.1 Beyan edilen kamera uygulanmıyor (AN1-Y2)

**Kapak yankısı #0 `kapak_kilit` (0–3,7 sn, `cam=("push",)`)**

- **Neden:** beyan edilen kamera türe ulaşmıyordu. Tür cilt_cam'in hesapladığı `cx.cam_state`'i okumuyor, yalnız kendi `kamera=("itme", 0.025)` itmesini çiziyordu (çekim boyunca en çok %2,5).
  - AN1 videoda ölçeği 1,0000 ölçmüş. Bunun bir payı, videodaki yankının eski K1 render'ı olmasından gelebilir (PK2-Y8, TE1-Y2).
- **Değişiklik** (`kapak_medici.py: k_kapak_kilit`, yalnız hareket):
  - Çekime `cam=` açıkça verilmişse (`not cx.sh.cam_auto`), cilt_cam durumu (pivot + dx/dy + ölçek) dünyaya uygulanır. Türün kendi itmesi o zaman devre dışı kalır.
  - 1,0–2,5 sn: belgenin üstünden ışık süpürmesi geçer (döndürülmüş kırpma, toplamsal degrade).
  - Kilit kapanınca (`kapan_at + 0,14`): `anim.jolt(*anim.shake(t, t_hit, 0.25, 3.5))` sarsıntısı (impact_ovl mantığı).
  - Zincir sarkması `1 + 0,16·anim.wobble(…)` ile oturur (settle).
  - Işık havuzu ve parıltı kameranın içinde.
- **Ölçüm:** yankıda ölçek 1,0000 → 1,0786: çekim boyunca +%7,86, AN1'in ölçtüğü 0,6–2,9 sn aralığında +%4,9 (hedef ≥%4). v2 kodunun kendi itmesi en çok +%2,5'ti.
- **Kapak karesi (JPG, zaman=1,6) bozulmadı.** JPG kamera beyanı olmayan yoldan çizilir.
  - `kapak_medici.py --part 1` yeniden üretildi.
  - Önce/sonra bulanık fark ortalaması: K1 0,26, K2 0,30 gri düzey.
  - `kapak_qa`: 0 hata, 0 uyarı.
- **Kanıt:** `01_kapak_yankisi_once_sonra.jpg`, `01b_kapak_K1_once_sonra.jpg`.

**Haritalar (`p1_map`; AN1: #51, #55, #62, #69)**

- **Bulgu:** v2'de harita kamerası çizime ulaşıyordu (`cilt_cam.map_patch`, mapsk.Cam yaması).
  - Fark testi (§2.1) #51, #62 ve #69'da kamerayı çizimde gördü.
  - v2 videosundan alınan karelerde kıyı ve rota çizgisi kayıyor, ölçekleniyor (`01c_v2_harita69_videoda_hareket.jpg`, `01d_v2_harita62_videoda_hareket.jpg`).
  - Açıklamam: AN1'in LK ölçümü ekrana çakılı kâğıt dokusuna ve sabit kaplamalara kilitlendi. TE1-Y8 dokunun ekranda sabit olduğunu ayrıca ölçmüştü (§7).
- **Gerçek sorunlar:**
  - #55 (313 sn): beyan TERS. Beyan pull, anahtar kareler ise yaklaşıyor. SCN-1 beyanı `("push",)` yaptı.
  - #62 (şimdi #63, "kur farkı"): pull beyanı sahnenin anahtar kare zumunu kısmen götürüyordu; çekim yarı durağan kalıyordu.
- **Değişiklik (rota ucunu izleyen kamera)** — `p1_ortak.py: map_follow, _follow_patch, _route_world, _wrap`:
  - Kamera, çizilmekte olan rotaların ucu ilerledikçe kayar: uç yolunun %34'ü kadar (`MAP_FOLLOW`).
  - Kayma tanh yumuşak sınırla en çok genişliğin %14'ü (`MAP_FOLLOW_MAX`).
  - Beyan (push/pull/pan) ve `cams=` anahtar kareleri aynen üstüne biner.
- **Kadraj koruması (iki kat):**
  - Kenar payları sol 170, üst 160, sağ 330, alt 190 px. Sağ pay büyük, çünkü kent adı noktanın sağına yazılır.
  - (1) İzleme, rota ve kent noktalarını güvenli alanın dışına itmez (`_follow_patch`).
  - (2) Ön ayar da itemez (`cilt_cam._map_guard`, `map_patch` içinde).
  - Korunan noktalar `cx._map_keep`'te: rota noktaları ve kentler (`_wrap` doldurur).
- **#63 doğrulaması (başkanın ek kontrolü):**
  - BRUGGE noktası çekim boyunca y ≥ 111. İzleme açıkken ve kapalıyken aynı.
  - Etiket noktanın sağında yazılıyor; üst frize değmiyor, kamera hareketiyle kesilmiyor.
  - Korumasız ilk izleme sürümünde BRUGGE y = −127'ye itiliyordu.
  - Kanıt: `02_harita63_brugge_kadraj_korumasi_sonra.jpg`, `12_harita63_brugge_konum.txt`.
- **Kalan:** #63'te ön ayar pull korumaya takılıyor. Gerçekleşen hareket anahtar karelerden geliyor ve beyanla aynı yönde (izdüşüm 1,11). Kapı bunu UYARI olarak yazıyor. Çözüm sahnede (§4, SCN-2/1).

### 1.2 Aynı görüntü kesmesi (AN1-Y3, AN2-Ö1)

Kapı §2.2'de. Sahnelerde bu turda bu tür kesme kalmadı: güncel P1'de 37 sert kesmenin hiçbiri aynı görüntü kesmesi değil.

### 1.3 Işık geçişi (AN1-Y8, SA1-Y7)

- **Değişiklik** (`cilt_fx.py: blend_light`):
  - Yıldız ışınları kaldırıldı (`LIGHT_RAYS = False`). `rays=True` ya da `LIGHT_RAYS = True` eski görünümü geri getirir.
  - Yerine üç öğe:
    - yumuşak yaldız parlaması (`_glow_small`: iki katman, #F2C35E / #FFDC98);
    - Floransa altın zemin resimlerinin zımba (punzonato) halkaları (`_punzonato_dots`, `_punzonato`: 4 halka, noktaların ≈%14'ü eksik, 3. halkada rozetler);
    - sıcak bir çekirdek.
  - Parlamanın merkezi geçiş boyunca hafifçe kayar.
  - İlk sürüm fazla beyazdı; renk altına çekildi, alfa düşürüldü.
- **Bütçe kapısı:** §2.4. P1'de light geçişi 13 → 4: #1, #50, #60, #100. Azaltmayı sahne yazarları yaptı; kapı izliyor.
- **Kanıt:** `03_isik_gecisi_once_sonra.jpg`.

### 1.4 Şerit ucunun açılması (AN2-K1, TE1-Y5; 214,4–219,5 sn ve 267–271 sn alayları)

- **Nedenler:**
  - (a) `BAND_KINDS` tür adını birebir arıyordu; `p1_procession` sarmalayıcısı kümede yoktu.
  - (b) truck beyanı türün kendi kaydırmasına çevrilmiyordu.
  - (c) Örtme zumu sabit bir tahmindi.
- **Değişiklik** (`cilt_cam.py`):
  - `base_kind()` pN_ önekini soyar. `attach` ve `state` şerit türlerini taban adla tanır.
  - `attach` pan ile birlikte truck'ı da türün kendi kaydırmasına çevirir. Kullanılan işlevler:
    - `_native_skyline`, `_native_procession`, `_native_frieze`;
    - `_inner_raw`: sarmalanan türün imzasını okur;
    - `_dir_sign`: türün `dir=` yönüyle çelişen beyanı çevirmez.
  - Çevrilemeyen durumda `_band_cover` devreye girer:
    - Kaymanın gerçek kapsamı t ∈ [−0,1 ; süre + 0,7] aralığında sayısal örneklenir (geçiş taşmaları dahil, 49 örnek, el titremesi payıyla).
    - Örtme zumu z = 1 + (kapsam + 2)/(W/2).
  - Skyline'da sahne `pan=` de yazmışsa artık kameranın miktarı geçerli. Eskiden genel öteleme ile tür kaydırması üst üste biniyordu.
- **Kanıt:** `04_serit_ucu_once_sonra.jpg`. Baş, orta ve son karelerde sağ kenar dolu.

### 1.5 Set kenarı 545,5–546,0 sn (AN1-Y10)

- **Değişiklik** (`cilt_pano.py: Layer._tiles`, `Layer.draw_view`):
  - Görünür aralık dünyanın [0, genişlik] sınırını aşınca taşan şerit aynalanmış dekorla dolar. Sınır en çok `EDGE_FILL` = 320 katman px.
  - Kırpmalı çizilir: solda `scale(−1, 1)`, sağda 2 × genişlikte aynalama.
  - Daha uzak aşımlar `_oob_note` ile kaydedilir (`OOB`).
- **Ölçüm:** 545,5 sn'de sol kenar şeridi BGR 22/1/1 (lacivert boşluk) → 37/23/28 (dekor).
- **Kanıt:** `05_set_kenari_545s_once_sonra.jpg`.

### 1.6 Kesmede 1 karelik kamera duruşu (AN1-Y11)

- **Neden:** kesmeyle birleşen uçta hermite/pchip uç eğimi 0'dı. Kamera kesme anında duruyordu.
- **Değişiklik:**
  - `shots.py`:
    - `Shot.cut_in` / `cut_out` ve `Ctx.cut_in` / `cut_out` eklendi.
    - `shot(..., jump=False)` parametresi eklendi.
  - `compose.py: Program._link_flags`: sert kesmede `cut_in`/`cut_out` ve `cam_in`/`cam_out` birlikte işaretlenir; geçişte yalnız `cam_in`/`cam_out`.
  - `cilt_cam.py: CUT_SLOPE = 1.0`, `_prof_slopes`, `_end_factor`, `state()`. Uç eğimleri:
    - kesme ucu: ≥1,0, yani ortalama hız ("hareket üstünde kesme");
    - geçiş ucu: CARRY 0,65;
    - serbest uç: 0.
  - `cilt_pano.py`: `pchip(ts, vs, e0, e1)` ve `PanoCam`. Oda ve pano kameralarında aynı kural.
- **Ölçüm** (`06_kesmede_durus_olcum.txt`):
  - 37 sert kesme, 74 uç incelendi. Kare farkı 0,06 gri düzeyin altındaysa duruş sayıldı.
  - Duruş 6 → 2.
  - Kalan ikisi (355,76 ve 575,50 sn) `c2_yakin`'in kendi kamerasında (OWN_CAMERA, `ease_io`). SCN-2 isteği: §4.
- **Not:** AN1'in v2 saatleri (43,92; 416,0; 480,2; 482,25; 502,8) güncel listede ya kesme değil ya da yapı değişti. Örneğin 480/482'deki anahtar üçlüsü SCN-2'de değişti. Ölçümü güncel 37 kesmenin hepsinde yaptım.

### 1.7 Bitiş ekranı (PK2-Y6, SA1-Y8)

**`compose.py` sabitleri**

| Sabit | Değer | Not |
|---|---|---|
| `OUTRO` | 10.0 | önce 7 sn |
| `OUTRO_SLOT_IN` / `OUTRO_SLOT_FADE` | 0,55 / 0,85 sn | |
| `OUTRO_SLOT_FULL` | 1,4 sn | yuvaların tam göründüğü an, çıkış başından; ≤1,5; son kareye dek kalır |
| `NEXT_PART_LINE` | `{1: "2/7 · COSIMO: SÜRGÜN VE DÖNÜŞ"}` | |
| `OUTRO_TITLE_LIFT` | 1.25 | |
| `TAIL` | `END_HOLD + OUTRO` = 11,3 sn | |

**`k_outro` değişiklikleri**
- Kamera itmesi 0,025, kayma yarıya indi.
- Başlık ve arma yalnız son 0,6 sn'de söner.
- "ZAMAN KURYESİ" için iki önlem: arkasına koyu eliptik hale ve kabartmanın ışık yüzüne toplamsal ikinci geçiş. Kontrast 3,07–4,34 → **4,75 / 4,91:1** (hedef ≥4,5).
- Yuvalar ekrana sabit.
- Sol yuvanın altındaki levhada iki satır: "SIRADAKİ PARÇA" ve "2/7 · COSIMO: SÜRGÜN VE DÖNÜŞ" (title_m 28 px, #F2E4B8). Levhanın alt kenarı ≤ 1020.

**Yan bulgu:** 593,0 sn'de 1 px'lik dikey bir çizgi vardı. Kaynağı arma parıltısı: `cilt_medici.soft_glint` α ≈ 0,01'de bu çizgiyi bırakıyor. Parıltı artık yalnız arma tam görünürken (a > 0,98) çiziliyor. Kök neden cilt_medici'de (§4).

**Paket ve miks**
- `paket_P1.py` `compose.OUTRO` ve `compose.OUTRO_SLOT_FULL`'u okuyor; bitiş ekranı saatleri kendiliğinden güncellenir.
- `miks.py`, `--tail` verilmezse `compose.TAIL`'i okur (≈683. satır).
- **Miks kuyruğu yeniden üretilmeli** (8,3 → 11,3 sn). Miksi çalıştırmadım.

**Kanıt:** `07_bitis_ekrani_once_sonra.jpg`, `07b_baslik_kontrast_once_sonra.jpg`.

### 1.8 Kâğıt dokusu ve gren (TE1-Y8, TE1 §7 önerisi)

- **Eski:** CM.post sıva tanesini (tooth) ekrana çakılı çarpıyordu. Gren 6 karelik döngüydü (`n % 6`).
- **Değişiklik** (`compose.py`):
  - **`PAPER_WORLD = True`**.
  - **`paper_matrix(cx)`**: dokuyu üç kaynaktan birine göre kilitler.
    - cilt_cam durumu: k = 1/s, pivot + dx/dy.
    - Oda/pano dünyası: `cx.world_xf = ("pano", …)`, ana düzlem f = 1, başvuru zumu çekimin orta anından.
    - Harita kamerası: `("map", …)` ve `cx._map_zref`.
  - **`_tooth_warp`**: warpAffine, WARP_INVERSE_MAP, BORDER_REFLECT.
  - **`paper(img, n, samples)`**:
    - Deklanşörlü karede alt örneklerin ilk, orta ve son dönüşümleri ortalanır; doku da hareket bulanıklığı alır.
    - Geçişte iki çekimin dokusu ağırlıkla karışır.
  - **`grain_at(n)`**: 4 geniş gren alanı, her kareye tohumlu 96 px kaydırma. Döngü yok.
  - **`frame()`**: `CM.post`'u `tooth=0, grain=0` ile çağırır; doku ve gren `paper()`'da eklenir.
  - **Kaynak kancaları:** `cilt_pano.Ctx` ve `cilt_cam.map_patch` `world_xf` yazar.
- **Ölçüm** (`08_doku_kilidi_ve_kare_suresi.txt`). Üç çekim: #40, #69, #90.

  | Korelasyon (eski → yeni) | #40 | #69 | #90 |
  |---|---|---|---|
  | içerikle kaydırılmış | 0,18 → 0,37 | 0,43 → 0,69 | 0,40 → 0,62 |
  | sıfır kaymada | 0,41 → 0,15 | 0,65 → 0,36 | 0,69 → 0,45 |

  Doku artık içerikle birlikte gidiyor.
- **Kare süresi** (100 kare, 5 çekim, A/B dönüşümlü):
  - Ortalama +%3,4; kare başına oranın medyanı +%4,0. Sınır ≤%15'in içinde.
  - p90 +%39: ucuz kart karelerinde dokunun payı büyük.

### 1.9 Segment başında deklanşör (TE1-Y1)

- **Değişiklik** (`compose.py: Program._shutter`): önceki kare yoksa aynı çekimin bir önceki anı çizilir ve akış ondan ölçülür. Önceki kare şu durumlarda yoktur: segment başı, geçişten sonraki ilk kare, tek kare çizimi.
- **Ölçüm:** 200,000 sn (kare 4800) iki yoldan çizildi: sıralı (n−2, n−1, n) ve soğuk (yeni Program, yalnız n). İki kare bit-birebir aynı (fark 0).
- **Kanıt:** `11_deklansor_segment_basi.txt`.

---

## 2. Yeni ve değişen QA kapıları (`qa_flow.py`)

- `--fast`'ta bu kapılar PAS olur.
- Tam koşuda kareler 2 işçide çizilir. P1'de 84 iş, 70–100 sn sürüyor; bütün qa 5 dk 41 sn.
- Başlık belgesine (e) maddesi olarak eklendi.

### 2.1 Beyan ↔ gerçekleşen kamera (AN1-Y2) — `_probe_cam`, `camreal_gate`

**(A) Fark testi**
- Beyanın en büyük olduğu an %15, %50 ve %85'ten seçilir.
- O an iki kez çizilir: nötr kamerayla ve beyan edilen kamerayla. Ekran-uzayı kaplamalar çıkarılır. Nesne animasyonu iki karede özdeş olduğu için fark yalnız kameradan gelir.
- Değişen piksel < %0,5 → **ULAŞMIYOR** (KALDI).
- En çok 3 RANSAC benzerlik katmanı çıkarılır. En iyisinin beyana izdüşüm oranı < 0,5 → **KISMEN** (KALDI).
- Ölçülebilir katman yoksa oran yazılmaz ve karar (B)'ye kalır. Bu, beyan kadraj boyunu aştığında olur (P2'de #5 ve #63: beyan 900–9600 px).

**(B) Zaman testi**
- %20 → %50 → %80 karelerinde dünya katmanının benzerlik hareketi iki adımda zincirlenir ve aynı aralıktaki beyanla karşılaştırılır.
- Odalarda duvar paralaksı ayrı katman sayılır; haritada duvar yok.
- İzdüşüm < 0,5 ya da ters yön → KALDI.
- İçerik değişiyor ya da eşleşme zayıfsa "ölçülemedi" yazılır. Listelenir ama kapıyı kaldırmaz.

**Harita kadraj koruması tanısı**
- (A) "ulaşmıyor" derse koruma kapatılıp kare yeniden çizilir.
- Kamerayı koruma durduruyorsa ve (B) beyanla uyumluysa sonuç UYARI olur, gerekçesi yazılır.

**Ölçülmeyenler (sayıları yazılır)**
- Kendi kameralı türler (OWN_CAMERA): oda, pano, şehir, belge, `c2_masa`, `c2_yakin`, ….
- Kartlar.
- Şerit türlerinde yatay beyan. Beyan türün kendi kaydırmasına çevrildiği için nötr ↔ beyan farkı anlamsız.

**Sonuçlar**
- **v2'de yakaladığı:**
  - (A): #0.
  - (B): #0, #55 (−5,49, TERS) ve #12 (0,47).
  - AN1'in öteki üç haritası v2'de de çizime ulaşıyordu (§1.1, §7).
- **Güncel P1:** 43 çekim ölçüldü.
  - Ulaşmıyor 0, kısmen 0, <%50/ters 0.
  - Kadraj koruması 1 (#63) → UYARI.
  - Ölçülemedi 10; şerit 4; kendi kameralı 52.

### 2.2 Aynı görüntü kesmesi (AN1-Y3, AN2-Ö1) — `_probe_cut`, `jump_gate`

- **Yöntem:** her sert kesmede A'nın son karesi ile B'nin ilk karesi (kaplamasız) karşılaştırılır. ORB + RANSAC benzerlik kullanılır; asma bant şeritleri (y 95–170 ve 930–1005) maskelenir.
- **Karar:**
  - inlier ≥ 100 ve ölçek 0,80–1,35 → aday.
  - Ölçek 1/1,12–1,12 ve hizalı farkta değişen pay ≤ %35 → **KALDI** (kesin sıçrama).
  - Diğer adaylar → **UYARI** (sınırda).
- **Muafiyet:** `shot(..., jump=True)` bilinçli sıçramayı muaf tutar.
- **v2'de yakaladığı** (kanıt: `13_v2_yakalamalar.txt`):
  - KALDI: #23 ×0,98; #58 ×1,01; #73 (427,58) ×0,99; #84 (480,23) ×0,97; #85 (482,18) ×1,02; #89 (499,92) ×0,99.
  - UYARI: #8 ×1,21; #46 ×1,15.
  - #82 ×1,45 aralık dışında kaldı; gerçek bir ölçek değişimi.
  - AN1-Y3'ün üç kesmesi ve AN2-Ö1 tablosunun ikisi yakalanıyor.
- **Güncel P1:** 37 sert kesme, 0 sıçrama.

### 2.3 Sert kesme payı (değişti) — `cut_share_gate`

- Artık yalnız mekân, ölçek ya da konu değişen kesmeler sayılıyor; aynı görüntü kesmeleri payı şişirmiyor. AN1-Y3 bunu kapının yan etkisi olarak işaret etmişti.
- v2: %39 → %33.
- Güncel: %39 (37/96).

### 2.4 Işık geçişi bütçesi (AN1-Y8) — `light_budget_gate`

- Statik kapı, kare çizmez.
- Kural: parça başına en çok 4 `tr="light"`. Fazlası KALDI ve çekimler listelenir.
- v2'de 13 (c0 2, c1 3, c2 8; AN1-Y8'in c2 listesiyle birebir). Kanıt: `13_v2_yakalamalar.txt`.
- Güncel P1'de 4: #1 (3,7 sn), #50 (285,2), #60 (342,8), #100 (584,8).

---

## 3. Son durum

| Denetim | Sonuç |
|---|---|
| `qa_flow.py --part 1` (tam) | **19 GEÇTİ · 0 KALDI · 2 UYARI · 1 PAS.** UYARI'lar: #15 yön (eski) ve #63 kadraj koruması. PAS: donma, video verilmedi. |
| `kapak_qa.py --part 1` | K1 0 hata · 0 uyarı; K2 0 hata · 0 uyarı |
| `qa_flow.py --part 2` (duman) | **Hatasız bitti** (5 dk 24 sn). 13 GEÇTİ · 7 KALDI · 0 UYARI · 2 PAS. |

**P2 KALDI'ları.** Beşi bu turdan önce de vardı:
- kart dizisi;
- sert kesme payı %0;
- geçiş süresi σ 0,05;
- ölçülen hareket 4;
- yerleşim 23.

İkisi yeni kapılardan geliyor:
- Işık bütçesi: 16 (c3 5, c4 6, c5 5).
- Kamera "kısmen": 1 (#114 `c5_liste_lorenzo`, izdüşüm 0,44).

İkisi de P2 sahne bulgusu; P2 işlenirken ele alınmalı. P2'de ayrıca:
- #38 `p2_skyline` şerit kuralıyla ölçülmüyor.
- #5, #63 ve #82'de fark testinin oranı yok. Üçünde de (B) beyanla uyumlu: izdüşüm 1,0 / 1,0 / 0,99.

---

## 4. İstekler

**SCN-1 (c0–c1)**
1. `scenes_c0.py:28`: `KP.kapak_sahne_shot("K1", …)` çağrısına `isinlar=False` ekleyin.
   - Videodaki yankıda kilidin "tık"ında hâlâ dört kollu parıltı yıldızı çıkıyor. `k_kapak_kilit`'in varsayılanı `isinlar=True`; kapak JPG'sinde zaten False.
   - SA1-Y7 ve PK2-Y8'in yankı kısmı. Tek satırlık iş, ama sahne dosyasında olduğu için benim alanım değil.
2. Bilgi: #12, #37 ve #55 beyanları sizde düzeltildi. Güncel koşuda c0–c1'de kamera bulgusu 0.

**SCN-2 (c2)**
1. **#63 `p1_map` "kur farkı" (361,1 sn).** `('pull',)` ön ayarı kadraj korumasına takılıyor; BRUGGE ve BARSELONA zaten kenar payında. Sonuç UYARI. Seçenekler:
   - (a) daha küçük bir beyan, ör. `cam=("pull", 0.02)`;
   - (b) `cams`'teki zum aralığını ≈%8 genişletmek, böylece korumaya pay kalır;
   - (c) beyanı anahtar karelere uydurmak.

   Gerçekleşen hareket zaten beyanla aynı yönde (izdüşüm 1,11).
2. **`c2_yakin` kesmede duruyor:** 355,76 ve 575,50 sn, ikisi de çekim girişi. Kamera `ease_io(clamp(t/dur), 1.4)` kullanıyor; uçta hız 0. `cx.cut_in` / `cx.cut_out` (shots.Ctx; sert kesmede True) ile uç eğimi verilebilir:
   - h(u) = (u³ − 2u² + u)·m0 + (3u² − 2u³) + (u³ − u²)·m1
   - m0 = 1 if `cx.cut_in` else 0; m1 = 1 if `cx.cut_out` else 0.

**ENG-C / başkan**
1. **`cilt_medici.soft_glint`:** düşük alfada katman kenarında 1 px opak sütun bırakıyor (593,0 sn, arma parıltısı). `k_outro`'da parıltıyı kısıtladım; kök düzeltme cilt_medici'de yapılmalı.
2. **TE2-Y11 (`cilt_medici.name_plate`):** rol satırında eski stil rakam ("13oo"). SCN-1 bu isteği ENG-C/ENG-D'ye yazmış. İşlev benim dosyalarımda değil → ENG-C.

**Başkan**
1. **Miks kuyruğu yeniden üretilmeli:** `compose.TAIL` 8,3 → 11,3 sn. miks.py yardım metnindeki "8,3" eskidi; kod değeri compose'tan okuyor.
2. **P1'in tamamı yeniden render edilmeli.** Değişenler:
   - doku ve gren: her kare;
   - kesme uç eğimleri, şerit zumu, harita izleme/koruma, oda kenarı: birçok çekim;
   - ışık geçişleri;
   - kapak yankısı;
   - bitiş ekranı.
3. **Bitiş ekranı saatleri:** paket_P1, `OUTRO_SLOT_FULL = 1,4`'ü okuyor. `00_yayin_adimlari`'ndaki ve Studio'daki saatler paket çıktısıyla güncellenmeli.
4. **P2–P7 için:**
   - `OUTRO` 10 sn ve `TAIL` 11,3 sn bütün parçalarda geçerli.
   - `NEXT_PART_LINE` yalnız parça 1 için tanımlı. Parça 2–6'ya satır eklenmeli; parça 7'de yok.
   - Skyline'da `pan=` ile `cam=("pan", …)` birlikteyse kaydırma artık kameranın miktarı (eski çift hareket kalktı). P2–P7 skyline çekimlerine ilk render'da gözle bakılmalı.
   - P2'nin ışık bütçesi (16) ve #114 bulgusu P2 sahne sahiplerine gitmeli.

---

## 5. Geçiş çizen motor dosyaları

| Dosya | İçerik |
|---|---|
| `cilt_fx.py` | `blend_giornata`, `blend_wash_skia`, `blend_wash`, `blend_page`, `blend_iris`, `blend_slide`, `blend_zoomthru`, `blend_carry`, `blend_light` (bu turda değişti; `_punzonato*`, `LIGHT_RAYS`), `blend_candle`; `TR` sözlüğü ve `blend()` dağıtıcısı |
| `compose.py` | `Program._blend` (tür ve seçenek), `Program.frame` (geçiş karesinde iki çekimin doku örnekleri), `Program._link_flags` (kesme/geçiş uç bayrakları) |
| `cilt_hero.py` | önizleme `FX.blend` çağırıyor (124. ve 145. satırlar) |
| `fx.py` | eski PIL `whip` / `zoom_cut`. Hiçbir modül içe aktarmıyor (ölü kod). |

---

## 6. Açık kalanlar

1. **#63 UYARI** (SCN-2 isteği 1).
2. **`c2_yakin` kesme duruşu ×2** (SCN-2 isteği 2).
3. **Kamera kapısının (B) testi P1'de 10 çekimde ölçemiyor:** #5, #12, #14, #16, #20, #37, #53, #67, #75, #79. İçerik belirirken ya da zumlarken dünya katmanı ayrışmıyor. Bu çekimlerde karar yalnız (A)'ya dayanıyor.
4. **Şerit türlerinde yatay beyan ölçülmüyor** (P1'de 4 çekim).
   - v2'de (A) oranları 0,94 / 0,55 / 0,99 / 1,00 idi.
   - 0,55'lik #30 artefaktın sınırındaydı: türün `pan=`'ı nötr çizimde de var, fark küçülüyor.
   - Şerit uçlarını §1.4 güvenceye alıyor. Kaydırma miktarını ölçen kapı yok.
5. **AN1-Y4(b):** "Ölçülen hareket" eşiği gren tabanına yakın. Görev listemde yoktu, dokunmadım.
6. **Ekran-uzayı kaplamalar:** HUD ve ovl levhaları doku katmanının altında kalıyor, doku hepsinin üstünden geçiyor. Kamera kayınca doku sabit kaplamanın üstünde kayar; eski durumun tersi. Küçük bir etki; gözle bakılmalı.
7. **TE1-Y6 (H.264 seviyesi) ve TE1-Y2 (segment süreci):** render/kodlama hattında, benim dosyalarımda değil.

---

## 7. En emin olmadığım nokta

**AN1-Y2 harita ölçümüyle ayrışmam.**
- Ben #51, #62 ve #69'da kameranın v2'de çizime ulaştığını ölçtüm: fark testi ve v2 videosundan kareler (01c/01d).
- AN1 aynı videoda LK ile "ölçek ±%0,3, kayma ≤2 px" ölçmüş.
- Açıklamam: LK ekrana çakılı kâğıt dokusuna ve sabit kaplamalara kilitlendi. TE1-Y8'in doku ölçümü bunu destekliyor.
- Yanılıyorsam kapım bu üç çekimi v2'de kaçırıyordu.
- Yeni render'da doku dünyaya kilitli olacak; bu yüzden aynı LK ölçümü bu ayrışmayı kendiliğinden sınar. Doğru ölçüyorsam haritalarda hareket görmeli.

**İkinci şüphe: kesme ucunda eğim 1,0.**
- Örnek #65 (373,38 sn, oda, `('pan','r')`, iki ucu da kesme). Kamera ilk karede 9,3 dünya px/kare ile giriyor. Eskiden ilk karede 0,3 px/kare duruyor, sonra hızlanıyordu.
- Ortalama hız aynı. Tepe hız %33 düştü, çünkü hareket artık doğrusal.
- "Hareket üstünde kesme" bunu istiyor. Ama büyük kaydırmalı oda çekimlerinde giriş ani bir kalkış gibi okunabilir. Gözle bakılmalı; gerekirse `CUT_SLOPE` 0,6–0,8'e indirilebilir.

---

## 8. Değişen dosyalar

| Dosya | İşlevler |
|---|---|
| `compose.py` | `OUTRO`, `OUTRO_SLOT_IN/FADE/FULL`, `NEXT_PART_LINE`, `OUTRO_TITLE_LIFT`, `TAIL`; `PAPER_WORLD`, `_tooth1`, `_grain_fields`, `_h32`, `grain_at`, `paper_matrix`, `_tooth_warp`, `paper`; `Program._link_flags`, `Program.frame`, `Program._shutter`; `k_outro` |
| `shots.py` | `Shot` (`jump`, `cut_in`, `cut_out`), `shot(..., jump=False)`, `Ctx` (`cut_in`, `cut_out`) |
| `cilt_cam.py` | `CUT_SLOPE`, `base_kind`, `_prof_slopes`, `_end_factor`, `state`, `_At`, `_band_cover`, `SKYLINE_MAX_PX`, `_dir_sign`, `_native_skyline`, `_native_procession`, `_native_frieze`, `_inner_raw`, `attach`, `MAP_GUARD`, `MAP_GUARD_ON`, `_map_guard`, `map_patch` |
| `cilt_pano.py` | `EDGE_FILL`, `OOB`, `_oob_note`, `Layer._tiles`, `Layer.draw_view`, `pchip(e0, e1)`, `PanoCam`, `Ctx` (`world_xf`) |
| `cilt_fx.py` | `LIGHT_RAYS`, `_punzonato_dots`, `_punzonato`, `blend_light` |
| `qa_flow.py` | sabitler (`CAMREAL_*`, `JUMP_*`, `LIGHT_MAX`, `NEUTRAL_CAM`); `light_budget_gate`; ölçüm altyapısı: `_probe_grid`, `_render_gray`, `_orb_pairs`, `_ransac`, `_spread`, `_disp`, `_layers`, `_proj`, `_state_xf`, `_wall_xf`, `_xf_apply`, `_xf_inv`; ölçüm: `_probe_cam`, `_probe_cut`, `probe_tasks`, `_probe_worker`, `probe_series`; kapılar: `camreal_gate`, `jump_gate`, `cut_share_gate`; `run` (bağlantı, `--fast` PAS, JSON `probe`) |
| `p1_ortak.py` | yalnız harita sarmalayıcısı: `MAP_FOLLOW`, `MAP_FOLLOW_MAX`, `MAP_KEEP`, `_route_world`, `map_follow`, `_follow_patch`, `_wrap` |
| `kapak_medici.py` | yalnız `k_kapak_kilit`: canlı kamera yolu, ışık süpürmesi, zincir oturması, kilit sarsıntısı |

**Doğrulama komutları:**
- `python3 qa_flow.py --part 1`
- `python3 qa_flow.py --part 2`
- `python3 kapak_medici.py --part 1`
- `python3 kapak_qa.py --part 1`

Ölçüm betikleri (`t_cutstall.py`, `t_texture.py`, `t_perf.py`, `t_brugge.py`, `t_shutter_det.py`, `t_kalkis.py`) çalışma alanında.
