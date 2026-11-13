# SA1 · TUR 3 — Medici Parça 1, v3 (`out_p1/medici_P1.mp4`, 601,54 sn)
Mercek: sanat yönetmeni (kompozisyon, renk, ışık, çizim kalitesi, "fresk ve defter" cildinin tutarlılığı, kapak).

## 1. Karar

**ONAY — 9,1 / 10 (koşullu).**

| Bölüm | Tur 2 | Tur 3 |
|---|---:|---:|
| Son render (sanat yönetimi) | 8,6 | **9,1** |
| Kapak K1/K2 | 9,0 | **9,5** |
| Madalya v3 (P1'deki kullanımı) | 8,5 | **8,5** (Lorenzo düzeltmesi P3'e ertelendi) |

**Tur 2 koşullarım:** Y1 yarım sikke, Y2 yazı üstüne yazı, E4 madalya gölgesi, Y3 levha üstüne levha. Dördü de v3'te kapandı. Tur 2'deki öteki maddelerimden de yalnız Y6 kısmen açık kaldı.

**Bu turun koşulu: v3'te iki yeni görüntü hatası var (N1, N2).**
- İkisi de tur 2'de engelleyici saydığım yarım sikkeyle (Y1) aynı sınıfta: hikâyenin nesnesinde ya da yakın planın öznesinde görünür bir çizim hatası.
- İkisi de kısa (1,5 ve 1,7 sn), yerel ve ucuz: birer çekim yeniden render.
- Düzelirse ONAY 9,1 geçerli. Tek üyeli kare kontrolü yeter; ben bakarım.
- Düzelmeden yayınlanırsa puanım **8,7 (RED)** sayılsın.

**Bunlar puanı yükseltir ama ONAY koşulu değil:**
- N3: 1737 belgesindeki zikzak "yazı";
- Y6: defter sayfalarındaki arayüz görünümlü grafikler;
- yakın plan eller.

## 2. Neye dayandım

**Sınır:** videoyu oynatamadım, sesi dinleyemedim. Hareket yargıları kare dizilerine ve `hareket.json` ölçümüne dayanıyor.

**v3'ten kendim çıkardığım ≈450 kare:**
- Üç sikke çekiminin 12 fps dökümü (179 kare): 105,6–108,2 · 113,0–119,4 · 302,2–308,0 sn.
- Kapak yankısı 0–3,4 sn, 12 fps.
- c0_sikke 95,2–96,7 sn.
- Papa sahnesi 466,9–475,5 sn ve eğilme anı 473,5–475,7 sn (6 fps).
- Mitra ve kese ara planları; Brugge kesesi 355,9–361,1 sn (2 fps).
- 534,2–536,6 sn (8 fps).
- Madalyalar 528,5 / 532,5 / 581,5 / 583,5 sn (ham + yüksek geçiren süzgeç).
- Bitiş ekranı 592,0–601,4 sn; 1743 odası 6,0 sn; kule 586,0 / 588,5 sn.
- Setler, damgalar, set kenarı (545,3–546,5 sn) ve friz (215 / 218,5 / 270 sn).

**Kurul paketi:** `out_p1/kurul/` (genel_01–04, tam_*, gecis_light, hareket.json, teknik.json, qa_flow_ozet.txt). Ayrıca `out_p1/qa_flow_v3.txt`:
- 19 GEÇTİ · 0 KALDI · 2 UYARI · 1 PAS;
- yerleşim İHLAL 0 (303 kare, 80 levha);
- dönem İHLAL 0.

`out_p1/uretim_v3.log`: 601,54 sn, 14.437 kare, kare hatası 0.

**Kapak:** `out_p1/kapak/kapak_qa_P1.png` (07:07), `yayin/studio_paketi_P1/kapak_P1_K1.jpg`, `_K2.jpg`.

**Belgeler:** `kurul/KURUL.md` (tur 2 sonucu ve v3 planı), `kurul/duzeltme_tur2/ENG-C.md`, `ENG-D.md`, `SCN-1.md`, `SCN-2.md`.

**Kod:**
- `scenes_c0.py:28` (yankıda `isinlar=False`);
- `kapak_medici.py:133–134` (kapak zemin tonu, ışın yok).

**Saklanan kanıtlar** (`/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/t4/`):

| Konu | Dosyalar |
|---|---|
| Y1 | `coin_tiles_v3.png`, `coin_seam_v3.png`, `coin113_v3.png`, `sikke_v3.png` |
| Y2, Y3 | `y2y3_sheet.png` |
| E4 | `medal_hp_v3.png`, `medal_edge_check.png` |
| Y4 | `y4_v3.png`, `kalemler_v3.png` |
| Y5 | `figures_v3.png` |
| Y6 | `masa_v3.png`, `ledger_graphics.png` |
| Y7 | `echo_lock2.png` |
| Y8 | `outro_v3.png` |
| Ö4 | `room1743_v3.png` |
| K3 | `tower_v3.png`, `tower_base_v3.png` |
| N1 | `papa_seq.png`, `bow_mitre.png`, `papa_admonish.png` |
| N2 ve eller | `cuffs470.png`, `hands_full.png`, `hands_v3.png` |
| N4 | `ghost_arm.png` |
| Damga fişi | `stamps_v3.png`, `slips_zoom.png` |
| Setler | `sets_v3.png` |
| Set kenarı ve friz | `edges_v3.png` |

Kare dökümlerini sildim. Disk sınırlı olduğu için tur 2 kanıt klasörlerimi (`…/scratchpad/t2`, `…/t3`) de sildim; tur 2 raporundaki o yollar artık yok. Tur 2 bulgularını başkan v2 karelerinden doğrulamıştı (KURUL.md).

## 3. Tur 2 maddelerimin durumu

### Tur 2 koşulları

| # | Madde | Durum | Kanıt (v3) |
|---|---|---|---|
| **Y1** | Yarım sikke ve dikey dikiş | **KAPANDI** | 179 karede yarım sikke ya da sert dikiş yok. Örnekler: 302,28–302,53 sn (sert kesme sonrası tam sikke); 113,17 sn (geçişte sikke tam); 117,5–118,0 sn (parıltı yumuşak, çapraz bir bant). c0_sikke 95,2–96,7 sn de temiz |
| **Y2** | "EVLİLİK ÇEYİZİ" × "1.500" | **KAPANDI** | 304,5–307,6 sn: etiket kalktı. "1.478 → 1.500 FLORİN" ve halkalar çakışmasız; başlık "PİCCARDA BUERİ'NİN ÇEYİZİ" üstte |
| **E4** | Madalya gölgesinin dikey kesiği | **KAPANDI** | 528,5 / 532,5 / 581,5 / 583,5 sn: yüksek geçiren süzgeçte madalya ile levhalar arasında düz kenar yok. Ölçümün bulduğu tek tutarlı basamaklar (x 986 ve 1031) levhaların sol kenarı (`medal_edge_check.png`) |
| **Y3** | GİOVANNİ × BALDASSARRE COSSA | **KAPANDI** | 431,8–436,5 sn: GİOVANNİ levhası sol altta, COSSA sağ üstte; aralarında ≈45 px boşluk. `qa_yerlesim` artık levha×levha ve yazı×yazı çakışmasını İHLAL sayıyor; sonuç 0 |

### Tur 2'nin öteki maddeleri

| # | Madde | Durum | Kanıt / not |
|---|---|---|---|
| **Y4** | Boş, kıpırtısız parşömen (534,45–536,2 sn) | **KAPANDI** | Sayfalar ve iki levha ilk karede hazır. Kamera kayıyor: kare farkı 1/8 sn'de 2,4–2,7 (v2'de 0). Yazı 536,4 sn'de tüy kalemle akmaya başlıyor. İsteğe bağlı: kalemler ilk karede sayfanın kenarında dursun |
| **Y5** | Üç özdeş figür (571 sn) | **KAPANDI** | 569–575,5 sn: ön planda büyük, sağ kenarla kesik, cappuccio'lu figür. Arkada keçe kepli ve sakallı / coif'li ve sakalsız iki figür, farklı ton ve boyda. Kalan küçük not: üçünün de duruşu aynı. P2'de poz evresi ya da bir çömelen figür |
| **Y6** | İnfografik kümeleri | **KISMEN** | Kartlar masadaki defterlere taşındı: ön planda mum, sandık ve sikke yığınları; anahtarı bırakan el; yazan tüy kalem (416–431,6 · 475,8–486,4 · 493,6–502,8 sn). Bu doğru karar. Ama defterin içindeki grafik dili hâlâ modern arayüz (aşağıda Y6-k) |
| **Y7** | Işık geçişinde yıldız ışınları | **KAPANDI** | Işık geçişi 13 → 4 (qa: c0 1, c1 1, c2 2). Görünüm yumuşak yaldız parlaması + punzonato halkası (`gecis_light.png`, 3,3–3,6 sn). Kapak yankısında kilit "tık"ı ışınsız (`scenes_c0.py:28` `isinlar=False`; 0–3,4 sn). Kapaklarda da yok |
| **Y8** | Bitiş başlığı kontrastı ≈3,0:1 | **KAPANDI** | 592,9–600,5 sn: başlığın arkasında koyu hale var. Kaba ölçümümle (yüzdelik tabanlı) ≈8,6–9,6:1; ENG-D'nin ölçümü 4,75/4,91:1. Yöntem farklı, ikisi de ≥4,5. Bitiş ekranı artık 10 sn; "2/7 · COSIMO: SÜRGÜN VE DÖNÜŞ" satırı okunuyor |
| **Ö4** | 1743 perdesi ve uyuyan siluet | **KAPANDI** | 6,0 sn: perde kenarı yumuşak eğri, basamak yok. Yorgan bedenin biçimini alıyor, baş yastıkta, temas gölgesi var |
| **K3** | Kuledeki beyaz şerit | **KAPANDI** | 586,0 sn x≈790–809: şerit yok. Kubbe 1429 için yarım |

### Tur 1'den taşınanlar

| # | Madde | Durum | Kanıt / not |
|---|---|---|---|
| **Ö6** | Madalya portreleri | **ERTELENDİ** (başkan kararı) | Lorenzo'nun saç ve burnu P3'e ertelendi; P1'de 6 sn'lik kişi kartı. Gerekçeyi kabul ediyorum, P3 kapısında yeniden bakarım. Diğer madalya notlarım P1'i etkilemiyor: Giovanni ve Cossa madalyası P1'de kullanılmıyor; Cosimo'nun yaş farkı P2–P3'ün işi |

### Kapak (§5) — kapak puanı **9,5**

- **KAPANDI:**
  - PK1 Y4: zemin açıldı. 168 px'te kenar ortalaması gri 38; <25 payı %8 (K1) ve %11 (K2).
  - PK1 Y5: parıltı kolları yok.
  - K2'nin kesesindeki arma red8; videodaki 1397–1429 armasıyla tutarlı.
- **AÇIK (isteğe bağlı, puana etkisi yok):** kilide döküm pirinç malzemesi önerim uygulanmadı. Kilit hâlâ kalın konturlu, düz gradyanlı bir simge.

### Tur 2'nin "ucuz/şablon" önerileri (§6)

| Öneri | Durum |
|---|---|
| Figür çeşitlemesi | **Yapıldı** |
| Yer başına set | **Yapıldı** (`sets_v3.png`). Brugge: Flaman pencereleri, dama zemin, dışbükey ayna. Roma bankası: terrakota sıva. Kâtip odası: göz pencereler. Konstanz: kartallı altın perdeler. Catasto: kireç sıva + Komün kalkanı. Stinche: parmaklık + zincir halkası |
| Kartları dünyaya taşıma | **Kısmen** (Y6) |
| Işın yıldızı | **Kaldırıldı** |

**Hareket:** `hareket.json` v2 → v3:
- <2,0 kare farkı payı %11,3 → **%4,2**;
- medyan 5,75 → 7,16;
- en uzun düşük hareket 5 sn → 2 sn (ölüm döşeği 549,5 sn; bitiş ekranı 594,5 sn).

## 4. Gerilemeler ve yeni sorunlar

### ONAY koşulu (önem: önemli; kendi Y1 ölçütümle tutarlı)

**N1 — Eğilen Giovanni'nin elindeki mitra havada kalıyor (gerileme; ENG-C'nin yeni eğilme ve oturma hareketinden).**
- **Nerede:** #82 `p1_oda`, "aforoz tehdidi" (471,7–475,8 sn). Giovanni 473,7–475,2 sn arasında papaya eğiliyor.
- **Ne görünüyor:**
  - Elleri öne ve aşağı gidiyor: ≈x 793–853, y 807–840 (474,5 sn).
  - Rehin mitra omuz yüksekliğinde, sırtının üstünde asılı kalıyor: ≈x 593–687, y 633–767.
  - Ayakta dururken mitra göğsünün önünde (472,6 ve 475,5 sn).
  - Kanıt: `bow_mitre.png`, `papa_admonish.png`.
- **Neden önemli:** sahnenin konusu bu mitra.
- **Ne yapılmalı:**
  - Kit düzeyinde: `act_bow`/`gesture_env` elde tutulan nesneyi el (bilek) dönüşümüne bağlasın.
  - Hızlı yol: bu çekimde Giovanni'yi eğdirme (`listen`/`hold`) ya da mitrayı eğilmeden önce masaya bıraktır.
  - Aynı eylem+nesne birleşimi başka çekimlerde de taranmalı. Ben yalnız #82'de gördüm; catasto'da teslim eden figüre ayrıntılı bakamadım.

**N2 — Mitra ara planında kol ağızlarının deseni dışarı taşıyor.**
- **Nerede:** #81 `c2_yakin` (469,9–471,7 sn). Sol kol ağzı ≈x 555–760, y 685–915; sağ ≈x 1030–1250, y 685–915.
- **Ne görünüyor:**
  - Kürk ya da işleme deseni yarı saydam, üst üste binen dairelerden oluşuyor.
  - Daireler kol ağzının dikdörtgen çizgisinin dışına taşıyor; çizgi desenin üstünden geçiyor.
  - Yakın planda yarım kalmış ya da bozuk bir çizim gibi okunuyor (`cuffs470.png`).
  - Aynı ara plan türünün kese çekiminde (#62) kol ağzı düz bant ve temiz.
- **Ne yapılmalı:** desen kol ağzı yoluna kırpılsın (`clipPath`) ve opak çizilsin, ya da #62'deki düz bant kullanılsın (`c2_kinds.arm_hand`).

### ÖNEMLİ (ONAY koşulu değil, puanı yükseltir)

**N3 — 1737 belgesinde gövde metni zikzak "yer tutucu" çizgilerden oluşuyor.**
- **Nerede:**
  - Videoda: #7–#8 `c0_belge` 34,6–49,4 sn ve #10 54,3–56,7 sn. Toplam ≈17 sn tam ekran, ilk dakikada.
  - K1 kapağının belgesinde de var, ama 168 px'te görünmez.
- **Neden şimdi önemli:**
  - v3'te c2'nin sayfaları gerçek harflerle yazılıyor (536–566 sn).
  - Böylece aynı videoda iki yazı dili oluştu; c0'daki zikzak artık "çizilmemiş" gibi okunuyor.
  - PK1 tur 2'de bunu "yer tutucu" diye anmıştı; ben önceki turlarda yazmamıştım, eksiğim.
- **Ne yapılmalı:** düşük kontrastlı, gerçek harfli Fransızca el yazısı. Metin ya kaynak üyesinin onayladığı III. madde metninden alınır, ya da açıkça temsilî bir dua ve tarih kalıbı olur. ITALIANO/FRANSIZCA vuruşu aynen kalır.
- **Maliyet:** sahne değişikliği + ≈17 sn render.

**Y6-k — Defter sayfalarındaki grafikler arayüz gibi görünüyor** (`ledger_graphics.png`).

| Öğe | Nerede | Sorun |
|---|---|---|
| "22 YIL" | 475,8–486,4 sn | yuvarlak uçlu altın kapsül dolum çubuğu |
| "KAYITLI SERVET" | ≈498 sn, x 540–1250, y 750–835 | dikdörtgen ilerleme çubuğu |
| "9.780 hane" | 495,5 sn, ≈x 630–1290, y 165–705 | ince yatay çizgilerden gri blok; barkod ya da yer tutucu gibi |
| Cenova–Pacioli | 416–424 sn | tik etiketli eksen |

Ne yapılmalı:
- Çubukları tüy kalemle çizilmiş mürekkep taramasına (tarama/çapraz tarama) çevir; kenarı hafif titrek olsun.
- Haneleri satır satır küçük el yazısına ya da çeteleye çevir; ilk 137'si yaldızlı olsun.
- Eksen yıllarını el yazısıyla yaz.
- Ön plan nesneleri ve ışık zaten iyi; sorun yalnız sayfanın içindeki grafik dili.

**E-1 — Yakın plan eller hâlâ "eldiven" gibi.**
- **Nerede:** #62 kese 355,8–361,1 sn; #81 mitra 469,9–471,7 sn; #83'te anahtarı bırakan el ≈477 sn; #98 kalem 575,5–580,0 sn.
- **Ne var, ne eksik:**
  - ENG-C parmak ayrımı ve boğum çizgileri ekledi; çizgiler görünüyor.
  - Ama siluet tek parça kürek gibi: kalın kontur, ayrık başparmak lobu, düz dolgu (`hands_full.png`).
  - ≥2× ara planda el öznenin kendisi olduğu için ekrandaki en zayıf çizim bu.
  - Üslupla tutarlı, bu yüzden P1'de koşul yapmıyorum.
- **P2'den önce iki seçenek:**
  - (a) ara plan eli için ayrı siluet: parmak arası boşluklar, parmak uçları, bilek kirişi;
  - (b) kadrajı nesneye daraltıp yalnız parmak uçlarını göstermek; klasik ara plan hilesi, en ucuzu.

### KÜÇÜK

**N4 — Kese ara planında tüccarın kolu yerinde soluklaşıyor** (358,4–358,7 sn, ≈x 1000–1920, y 450–700; `ghost_arm.png`).
- Kol bir an yarı saydam bir "hayalet" gibi görünüyor.
- Kol geri çekilerek kadrajdan çıksın; soldurma yerine kayma.

**D-1 — Damga fişi.** ENG-C'nin üslup kararı. Görüşüm: **kabul**.
- Fiş, cildin "defter" yarısının diline (arşiv fişi) uyuyor.
- P1'in bütün damgaları artık tek dilde (`stamps_v3.png`).
- Kontrast kazancı (1,1–4,1 → 5,3–5,8:1) tartışmasız.

İki küçük not:
- (a) Defter sayfasının üstünde fiş gereksiz; kâğıt üstüne kâğıt oluyor. Burada mürekkep doğrudan sayfaya basılsın. Örnekler: ETMEDİLER 416–431 sn, BİR HESABA GÖRE 498–502 sn.
- (b) Fişin kenarları kusursuz düz, köşeleri yuvarlak, gölgesi belirgin; yer yer "etiket/çıkartma" gibi okunuyor (`slips_zoom.png`). `cilt_paper`'ın tırtıklı kenar ve lifli dokusu ile daha küçük bir gölge, fişi fresk üstüne iğnelenmiş arşiv kâğıdına çevirir.

**Kontrol ettim, gerileme görmedim:**
- Set kenarı 545,3–546,5 sn dolu.
- Friz uçları 215–218,5 ve 270 sn dolu.
- Uzun defter çekimi #72'de metin kırpılması yalnız kamera kadrajından; dünya içi yazı, kusur değil.
- Kâğıt dokusunun dünyaya kilitlenmesi yakın zumda (113 sn) dikiş ya da aynalama izi bırakmıyor.

## 5. Kullanıcının sorusu: "Bu çizim tarzı ucuz mu, yapay zekâ gibi mi?"

**Değişti, iyi yönde.**
- Yapay zekâ gibi durmuyor. YZ ya da stok çağrışımı yapan tek öğe olan ışın yıldızları gitti.
- Tur 2'deki "yer yer şablon" hissi de belirgin biçimde azaldı:
  - her mekânın kendi seti var (Brugge, Konstanz, Stinche…);
  - figürler örnek başına çeşitleniyor;
  - kartların çoğu masadaki defterlere taşındı.

Kalan "ucuz" işaretleri dar ve somut:
- 0:34–0:58'deki belgede zikzak "yer tutucu" yazı (N3);
- defter sayfalarındaki arayüz gibi dolum çubukları ve gri satır bloğu (Y6-k);
- ≥2× ara planlardaki eldiven eller ve 469,9–471,7 sn'de taşan kol ağzı deseni (E-1, N2).

## 6. En emin olmadığım nokta

1. **N1 ve N2'nin oynatma hızında fark edilirliği.**
   - Kareden kesin görülüyorlar, ama süreleri kısa (≈1,5 ve 1,7 sn).
   - Onları koşul yapmam, tur 2'de yarım sikkeyi (Y1) engelleyici saymamla tutarlılık içindir.
   - Başkan bunları "önemli, koşulsuz" sayarsa puanım 9,0'a iner, yine ONAY olur.
2. **Damga fişi.** İzleyicinin bunu "arşiv fişi" mi yoksa "etiket/çıkartma" mı okuyacağını kareden bilemem. Kabul ediyorum, ama P2'de tırtıklı kenarlı sürüm daha güvenli.
3. **N1'in kapsamı.** Eğilme + elde nesne birleşimini yalnız #82'de doğruladım. Aynı hata başka sahnelerde de olabilir (ör. catasto'da beyanname teslimi, 489 sn); oraya kare kare bakmadım.
4. **Y8 ölçümü.** Kontrastı ENG-D'den farklı bir yöntemle ölçtüm. Sayılarımız farklı, ama ikisi de eşiğin üstünde.
