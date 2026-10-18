# MEDICI — Yönetmenlik Rehberi (v1.0, 18 Ekim 2026)

> **Kullanıcı isteği (18 Ekim 2026):** "Görsel dilde senden ricam: olabildiğince akan ve çok animasyon. Sadece görsel çizim olarak değil **yönetmenlik** olarak da usta ol; çok uzun olacaksa part part yayınlayabiliriz."
> Bu belge `USLUP_REHBERI.md` (nasıl anlatılır) ve `STIL_REHBERI.md` (motor sözleşmesi) ile birlikte **sahne yazan herkesin** (ana ajan ve alt ajanlar) üçüncü sözleşmesidir: **nasıl çekilir, nasıl kesilir, nasıl akar.** Ölçülebilir maddeler `qa_flow.py` ile denetlenir (§10); denetimi geçmeyen bölüm teslim edilmez.

## 0. Tek cümle

**Ekran hiçbir zaman "gösterilmez"; yürür, akar, açılır.** Bir çekim bir sonrakinin içinden doğar; bilgi kartı bile yaşayan bir dünyanın içinde belirir. İzleyici "slayt değiştirdi" değil, "kamera ilerledi" hissetmeli.

## 1. On emir (hepsi ölçülebilir ya da gözle denetlenebilir)

1. **Sıfır durağan kare.** Her çekimde üç katman birden bulunur: **(a) kamera** (itme/çekme/kayma/hafif dönme: ≥%6 ölçek ya da ≥120 px kayma), **(b) ana eylem** (anlatıya çapalı bir şey belirir, dolar, yürür, yazılır, sayar), **(c) ortam hayatı** (toz, mum titremesi, dalga, kuş, bayrak, pigment ışıltısı). Hiçbir pencerede 1,5 sn'den uzun "durgun koşu" olamaz.
2. **Eylem sözcükte gelir.** Anlatıda söylenen ad/sayı/olay ekranda o sözcüğün 0,1 sn önünde başlar (çapa = `("c7s5", "bıçak", -0.1)`). Hareketin hızı cümlenin hızını izler: yavaş cümle → yavaş itme; kısa vuruş cümleleri → sert kesme, iri jest.
3. **Her kesmenin bir gerekçesi vardır.** Geçiş çıplak `fade` değildir: **(i)** hareket yönü eşleşir, **(ii)** biçim/renk eşleşir (para → güneş → kubbe gözü → palle), **(iii)** kamera devam eder (kayma bir sonraki çekimde sürer), **(iv)** bir nesne ekranı doldurur ve yeni sahne ondan açılır (iris/zum-geçiş), **(v)** malzeme geçişi (defter sayfası, pigment yıkama, fresk günlüğü), **(vi)** ses köprüsü (cümle/nota/çan bir önceki çekimde başlar). Çekimin `link=` etiketi gerekçeyi adlandırır. **Hedef: geçişlerin ≥%70'i gerekçeli; çıplak `fade` ≤%10.**
4. **Çekim uzunluğu anlatının nabzıdır.** Hikâye vuruşu 4–7 sn · açıklama/sayı 3–5 sn · yıldız an 8–14 sn (tek sürekli kamera) · ağır sahne uzun, yavaş, sessizliğe yakın (6–12 sn) · mizah kısa ve kesin (2–3,5 sn). 16 sn üstü yalnız `longtake=True` işaretli, kamerası kesintisiz çekimler için (≤28 sn). 1,2 sn'den kısa çekim yok.
5. **Ölçek oyunu.** Her bölümde ≥2 **ölçek geçişi** (harita → şehir → oda → tek bir nesne; ya da tersi). Makro ↔ mikro, bu videonun "yönetmen imzası"dır.
6. **Ekran yönü sözleşmesi.** Yükseliş/para/ilerleme/Medici: **soldan sağa ve yukarı.** Düşüş/sürgün/tehdit/saldırgan: **sağdan sola ve aşağı.** Zaman çizgisi hep soldan sağa. Yönü bozmak yalnız bilinçli dramatik olayda (Pazzi, 9 Kasım 1494, Roma 1527) ve her bölümde ≤1 kez.
7. **Işık bilgi taşır.** Altın/sıcak = güven, para, ev; lacivert/soğuk = gece, tehdit, yalnızlık; kızıl = şiddet, kan, öfke; kireç beyazı = gündüz, ilan, kamusal alan. Kesme anında ışık sıcaklığı değişiyorsa bu bir **hikâye bilgisidir** (rastgele değil).
8. **İnsan hareket eder.** Figürler dikilmez: yürür, eğilir, yazar, işaret eder, atlar dörtnala/yürüyüş yapar; kalabalık dalga gibi kıpırdar; yakın planda yüz için **madalya portresi**, geniş planda hareketli figür kullanılır (kaba yakın figür yok).
9. **Metin de animasyondur.** Yazılar belirmez, **yazılır/oyulur/damgalanır**: mürekkep akışı, yaldız parıltısı, damga "çarpması" (0,3 sn); sayılar sayılır; harita etiketleri iğneyle dikilir; hiçbir şey ani belirmez, hiçbir yazı yerinde "ölü" durmaz (hafif nefes: ±%0,8 ölçek).
10. **Ses–görüntü kilidi.** Kesme noktası ses vuruşuna ya da cümle nefesine denk gelir; efektler görsel vuruşla aynı karede (±1 kare); oda tonu çekimler arasında kesilmez (J/L kesme); müzik vurgu anında yükselir (yıldız anlar) ve ağır sahnede çekilir.

## 2. Kamera sözlüğü (`cam=` ön ayarları)

Her `shot(...)` çağrısı `cam=` alır (yoksa varsayılan `"push"`). Hepsi tüm çekim türlerinde çalışır (motor: `cilt_cam.py`, `CM.Cam` üzerinden).

| `cam=` | Ne | Ne zaman |
|---|---|---|
| `"push"` / `("push", 0.08)` | yavaş itme (varsayılan %6–8) | gerilim, nesne vurgusu, hikâye vuruşu |
| `"pull"` | yavaş çekme | bağlam açma, ifşa ("meğer…"), bölüm sonu |
| `("pan", "r"\|"l", px)` | yatay kayma + paralaks | geçit, alay, yolculuk; yükseliş = `r`, düşüş = `l` |
| `("crane", "up"\|"down", px)` | dikey kayma | kule, kubbe, merdiven; `up` = yükseliş/umut, `down` = düşüş |
| `("orbit", derece)` | dioramada hafif yörünge (≤12°) | yıldız an, maket/mimari |
| `"hand"` / `"hand2"` | elde kamera mikro titremesi (genlik 1,5 / 4 px) | `hand` canlı sokak; `hand2` yalnız Pazzi/Roma 1527 şiddet anları |
| `("rack", odak_a, odak_b)` | odak kaydırma (katman bulanıklığı önceden pişirilir) | iki nesne arasında dikkat taşıma |
| `("track", yol_id)` | panoramada **uzun plan**: anahtar kareli yol (`pano`) | imza sekanslar, "akan" bölümler |
| `[(çapa,(x,y,zoom,rot)),…]` | anahtar kareli serbest kamera | theatre/map/pano; çapalar sözcüğe bağlanır |

Kurallar: kamera **ease_io** ile başlar/biter (doğrusal yok); aynı çekimde iki ters hareket yok; `push` ile `pull` art arda gelirse (nefes) arada gerekçe vardır; yazı taşıyan nesne kamera kaymasıyla altyazı bölgesine (y≈1250–1390) girmez (Anayasa §12-7); HUD alanı (sağ üst 420×110, sol üst bölüm etiketi) boş kalır.

## 3. Geçiş sözlüğü (`tr=(ad, süre)` + `link=`)

**Mevcut (motorda):** `yikama` (pigment yıkama: ıslak boya yayılır) · `sayfa` (defter sayfası çevrilir) · `giornata` (fresk günlüğü: sıva parçaları sırayla) · `fade` · `dip` · `zoom` · `whip` · `wipe`.
**Eklenecek (cilt-lab, `cilt_fx.py`; hepsi sözcük çapalı):**

| ad | Tarif | `link=` |
|---|---|---|
| `iris` | ekrandaki yuvarlak nesne (florin, palle, güneş/ay, kubbe gözü, mercek, mühür) büyüyüp ekranı doldurur ya da daralır; yeni sahne ondan açılır (kenarında nesnenin halka/kabartması) | `shape` |
| `slide` | iki çekim aynı yönde birlikte kayar (eşit hız + paralaks): "tek kamera, iki yer" hissi | `dir` |
| `zoomthru` | A'nın bir ayrıntısına zum sürer, içinden B yerleşik pozdan geri çekilerek açılır (harita → şehir, defter satırı → oda, göz → manzara) | `scale` |
| `carry` | ön plandan bir öğe (bayrak, kurdele, mürekkep çizgisi, figür siluet, kâğıt şerit) ekranı süpürür, perdesinin arkasında B belirir | `carry` |
| `light` | sıcak ışık patlaması/ışık huzmesi yükselir, B ondan doğar (ifşa, ilham, yıldız an) | `light` |
| `candle` | mum sönmesi (A kararır) ve yeni mum yanışı (B yanar); ölüm/gece/zaman atlaması | `light` |
| `yikama`/`sayfa`/`giornata` | malzeme geçişi (bölüm geçişleri ve zaman sıçramaları) | `material` |

Her geçişte önceki çekimin son 0,4 sn'sinde hareket **devam eder** (durup beklemez); sonraki çekim girişinde aynı hareket yönünde başlar. `whip` yalnız savaş/aksiyon; `dip` yalnız ölüm/zaman uçurumu; çıplak `fade` yalnız sayfa/pigment dışında nefes gereken tek yerde (bölüm başına ≤1).

## 4. Ritim ve kurgu eğrisi

- **Bölüm açılışı (ilk 5 sn):** kanca. Bölüm kartı **canlıdır**: arkasında önceki sahnenin devam eden hareketi ya da akan pigment/sıva; kart ≤2,5 sn görünür; oda tonu ve müzik köprüsü kesilmez (kart 3 sn'lik sessizlik boşluğunu hareketle doldurur).
- **Bölüm içinde üçlü ritim:** *akış* (sürekli kamera/uzun plan, 8–14 sn) → *vuruş* (kısa çekimler, 3–5 sn, kesmeli) → *nefes* (ağır/yavaş, 5–8 sn). Üst üste ≥3 aynı türde çekim yok (Şarlken kuralı korunur; `montage=True` ile bilinçli seri istisnadır).
- **Kapı cümlesi görseli:** bölüm sonu çekimi bir sonrakinin **ilk görüntüsünü ima eder** (kapı: ekranın sağından giren yeni renk/nesne; sonraki bölümün ilk çekimi aynı nesneden açılır).
- **Yoğunluk:** her cümlede ≥1 "olay" (yeni öğe, kamera hareketi başlangıcı, sayı, damga); dakikada ≈10–14 çekim (ağır bölümlerde 6–8, mizahta 14–18).
- **Mizah ritmi:** mizah cümlesi **kısa çekimlerle** sıkıştırılır ve bir "vuruş" (damga çarpması, madalya sıçraması, bir nesnenin tuhaf yürümesi) ile işaretlenir; mizahta kamera titremez, **zamanlama** oynar (bir an erken/geç kesme).
- **Ağır sahne ritmi (Pazzi, Roma 1527, ölümler):** çekimler uzar, hareket küçülür (yavaş itme), müzik çekilir, geçişler `dip`/`candle`; kan göstermeyiz — **pigment yıkama ile kızıl leke, gölge, nesne** (taşıyıcı mecaz). Mizah kapalı.

## 5. Işık ve renk dramaturjisi (Perde başına)

| Perde | Parça | Işık/renk | Hareket dili |
|---|---|---|---|
| **I — ALTIN** (c0–c6) | Parça 1 | sıcak altın + sıva beyazı + lapis detay; gündüz ağırlıklı; mum iç mekân | cömert, yatay, akıcı (soldan sağa kayma); uzun planlar |
| **II — BEDEL** (c7–c11) | Parça 2 | gece/şafak, lacivert gölge, kızıl vurgular; sıcaklık azalır, kontrast artar | keskin, dikey düşüş, sağdan sola; kısa vuruşlar + ağır nefesler |
| **III — MİRAS** (c12–c16) | Parça 3 | gün batımı, umber, soluk altın; c16'da 1743 odasına dönüş (c0'ın ışığı) | geniş, aydınlık planlar → sakin kapanış; dairesel dönüş |

Her bölümün kendi **renk anahtarı** vardır (yönetmen kartında yazılır): örn. c3 kule taşı gri + sürgün lacivert + dönüş altın; c7 sabah kireç beyazı → kızıl.

## 6. Animasyon envanteri (neyin hareket ettiği)

- **Dünya:** kamera (yukarıdaki sözlük) + paralaks katmanları (≥3 derinlik) + atmosfer (toz, ışık huzmesi, kuş, duman, dalga).
- **Figürler:** yürüme döngüsü, jestler (yazmak, saymak, işaret etmek, eğilmek, el sıkışmak, kılıç/hançer *işareti* — kan yok), at yürüyüşü/dörtnalı, kalabalık dalgası, bayrak/sancak dalgalanması.
- **Nesneler:** florin dönüşü (3B hissi), defter satırı yazılışı/silinişi, mühür basılışı, mektup açılışı, çan sallanışı, saat/zaman çarkı, terazi sallanışı, tartı.
- **Grafik:** harita kamerası + rota çizimi, sayaç, çubuk/yığın dolumu, soy ağacı büyümesi/solması, ağ (düğüm-bağ) kurulumu, yıl rulosu (HUD).
- **Yazı:** oyma/yaldız/mürekkep yazımı, damga, iğneli harita etiketi.
- **Işık:** mum alevi, gün→gece döngüsü, güneş yönü ile gölge kayması, meşale, şimşek yok (tarih sahnesinde dramatik değil).

## 7. Ses–görüntü kilidi (miks ve efekt)

- `sfx.py` kuyruk dosyası (`sfx_cues.json`) **görsel olay listesiyle birlikte üretilir**: her damga, sayaç bitişi, sayfa çevirme, mühür, çan, florin cıngırtısı, adım, kapı çarpması için kare düzeyinde kuyruk.
- Oda tonu (mum çıtırtısı, sokak uğultusu, katedral yankısı) **çekimler arasında süreklidir**; yeni mekâna geçişte önce ses (L/J kesmesi) 0,3–0,6 sn önce girer.
- Müzik motifleri: Perde I **florin motifi** (parlak, pizzicato); II **bedel motifi** (alçak, tek çekilen yay); III **miras motifi** (sakin, tekrar eden üç nota). Yıldız anlarda müzik yarım ses yükselir, sessizliğe giriş **0,6 sn** önceden başlar.
- Mizah cümlelerinde müzik kuru bir "tıkırtı" ile durur (komik duraklama) — yalnız ölçülü.

## 8. Bölüm imza sekansları (set piece önerileri; sahne yazarı geliştirir, daha iyisini bulursa uygular)

| # | İmza | Kamera/kurgu fikri |
|---|---|---|
| c0 | **Aile Antlaşması, tek plan** | Mum ışıklı oda → kâğıt üzerinde tüy kalem → kamera belgenin içinden geçer → galerinin içine açılır (zoomthru) → bugünün kuyruğu (siluet) → "Bir masa ve bir defter" ile defter sayfası çevrilir (`sayfa`) |
| c1 | **Florin yolculuğu** | Dönen florin → `iris` → şafakta Floransa panoraması (soldan sağa kayma) → Arno'da boyahane renkleri akar → veba: renk solar (gün → gri), çanlar → Ciompi: alay sağdan sola kabarır |
| c2 | **Defter dünyadır** | Defter sayfası sahnedir: kalemler satırı yazar, senetler kâğıt tekne olup Floransa → Brugge → Londra rotasında yüzer; "vicdan komitesi" damgası çarpar; Cossa mezarı: altın yaprak parıltısı |
| c3 | **Kule, tek dikey plan** | `crane up` Palazzo Vecchio'nun kulesi; Venedik'e gemi (`pan r`); 1434 dönüş: kalabalık alayı (friz); tahtsız iktidar = boş koltuk + gölge; "dostlar ağı" (`network`) canlanır |
| c4 | **Kubbe kendini kurar** | Zaman atlamalı: kubbe sıra sıra (balık kılçığı tuğla) yükselir; kamera `crane up` + `orbit`; "kefaret/yatırım" terazisi sallanır |
| c5 | **Konsil alayı** | Doğu heyetinin süslü alayı (Gozzoli stili friz, kesintisiz `pan r`), elyazması yığını yükselir, mum ışığında Ficino; Lascaris'in rotası (harita + gemi) |
| c6 | **Giostra** | Santa Croce meydanı: sancaklar, mızrak koşusu (yatay hızlı kayma), Lorenzo madalyası + şiir mısralarının satır satır açılışı; sonda Giuliano'ya gölge (ışık soğur) |
| c7 | **26 Nisan 1478: saat saat** | Gece skyline → şafak → katedral içi *tek uzun plan* (nef boyunca kayma, ışık huzmesi, kalabalık) → çan → iki an: **hançer işareti** (pigment yıkamayla kızıl) → tunç kapılar kapanır (`whip`) → sokak/Palazzo Vecchio: *"Palle! Palle!"* alayı (kalabalık dalgası, hareketli sancak) → gece skyline'a dönüş |
| c8 | **Aslanın ini** | Pisa'dan Napoli'ye rota (harita → gemi diorama), saray salonu masa başı iki figür; Doğu: harita `whip` İstanbul'a, Bandini'nin iadesi (iki şehir arasında `slide`), Otranto alevleri |
| c9 | **Defter kapanıyor** | Şubelerin sayfaları tek tek kapanır (`sayfa` serisi), haritada mumlar tek tek söner (`candle` mantığı) |
| c10 | **Rahip ve kral** | San Marco kürsüsü + kalabalık nefesi; Charles'ın ordusu sağdan sola yürür (friz); 9 Kasım: çan titreşimi (görsel ses dalgası) ve saray yağması (nesneler kapıdan taşınır, `carry`); Savonarola'nın sonu: ateş ışığında yavaş pull |
| c11 | **Papa oğulları** | Roma alayı (sol→sağ) → 1527 duman (`dip`) → Castel Sant'Angelo koridoru (Passetto: dar koridorda kayan tek plan) → Floransa kuşatması: surlar, Michelangelo'nun istihkâmı (harita→maket `zoomthru`) → Alessandro/Cosimo kapısı |
| c12 | **Dük makinesi** | Uffizi inşası kubbe gibi kendini kurar; **Vasari Koridoru'nda kesintisiz kayma** (Palazzo Vecchio → Ponte Vecchio → Pitti, Arno üstünde); Santo Stefano kadırgaları (`pan r`), Lepanto |
| c13 | **İki kraliçe** | Catherine: Marsilya düğünü (alay), mitler hızlı seri (**MİT/GERÇEK** damgaları çarpar: çatal, dondurma, parfüm, zehir) — mizah açık; Marie: Rubens panoları canlanır (çerçeve içinde parıldayan gerçek boya, kamera çerçeveden çerçeveye `slide`) |
| c14 | **Mercek** | Galileo'nun merceği: `iris` (mercek halkası) → Jüpiter'in uyduları dans eder; Euridice perdesi açılır; piyano mekanizmasının çekici; Livorno limanı; Arapça matbaa harf dizimi |
| c15 | **Soy ağacı solar** | Düğümler tek tek söner (mum mantığı), Gian Gastone odası: kamera çok yavaş `pull`; Patto belgesi ışıkla belirir |
| c16 | **Hesap: aynı oda, ters yön** | c0'ın odası, kamera yolu **ters sırada**; "Ne SAĞLAM ne MİT" levhaları (altın/lacivert/kızıl) çarpar; Uffizi kuyruğu; son: florin dönüşü → `iris` → "ZAMAN KURYESİ" |

## 9. Parça planı ("part part") ve kanca/kapı

Süre ≈68 dk (tahmin) → **3 parça** (her biri tek başına izlenebilir, Şarlken'e yakın uzunlukta, bölüm kapıları kanca olarak seçilir):

| Parça | Perde | Bölümler | ≈dk | Kapanış kapısı |
|---|---|---|---:|---|
| **1 — Altın** | I ALTIN | c0 + c1–c6 | ≈26 | Giuliano'ya gölge; "26 Nisan 1478" kapısı |
| **2 — Bedel** | II BEDEL | c7–c11 | ≈23,5 | Alessandro'nun sonu; "17 yaşında bir çocuk" kapısı |
| **3 — Miras** | III MİRAS | c12–c16 | ≈19,5 | 1743 kapanışı; "hiçbir şey buradan çıkmayacak" |

- Parça 2 **c7 ile açılır** (soğuk açılış = videonun en güçlü sahnesi); önceki parçanın özeti anlatının ilk cümlelerine gömülür ("Floransa'nın en zengin ailesi…"), ayrı "önceki bölümde" bandı **yok** (izleyiciyi kaybettirir). Parça 3 **c12 ile açılır**; Parça 3'ün ilk 30 sn'sinde 1743 odasına iki çekimlik gönderme (c16'daki dönüşü hazırlar).
- Her parçanın **bitiş ekranı:** sol "SIRADAKİ PARÇA" (bir sonraki parça kapağı/fragmanı), sağ "ABONE OL"; Parça 3'te sol "TÜM FİLM / ÖNCEKİ PARÇALAR". Parça sonu 20 sn: ağırlık merkezi bir vuruş + sessiz kapanış + bitiş ekranı.
- Yayın: Parça 1 → +7 gün Parça 2 → +7 gün Parça 3 (kadans kararı sonuç verisiyle ayarlanır); Parçalar tek **oynatma listesi**; her parçanın başlığı ve kapağı kendi içinde bağımsız; sonda isteğe bağlı **Tam Film** (≈68 dk, parçalar peş peşe) ayrı yüklenir.
- Perde etiketi her parçanın ilk bölüm kartında: "PERDE I — ALTIN" (c1), "PERDE II — BEDEL" (c7), "PERDE III — MİRAS" (c12).

## 10. Ölçülebilir kapılar (`qa_flow.py`; her bölümde ve parçada çalışır)

| Kapı | Ölçüt | Eşik |
|---|---|---|
| **Durgunluk** | 0,5 sn adımlı kare farkı (240×135 gri) < τ olan ardışık süre | ≤1,5 sn (kalibrasyon: iyi çekimler τ'yu belirler) |
| **Kamera varlığı** | her çekimde `cam=` ≥ ön ayar ya da anahtar kareli hareket | %100 |
| **Gerekçeli geçiş** | `link≠none` oranı | ≥%70; çıplak `fade` ≤%10 |
| **Çekim uzunluğu** | bölüm medyanı 4–6 sn; p90 ≤ 12 sn; max ≤ 16 sn (`longtake` ≤ 28) | ağır/mizah bölümlerde bant kayar (§4) |
| **Tür tekrarı** | aynı `kind` üst üste | ≤2 (`montage=True` hariç) |
| **Çapa denetimi** | sahne zamanlarının cümle/sözcük çapalı olanı | ≥%90 (mutlak saniye ≤%10) |
| **Olay yoğunluğu** | cümle başına ≥1 olay (yeni öğe/kamera başlangıcı/sayı/damga) | ≥%95 cümle |
| **Yön denetimi** | `pan`/`slide` yönleri §1-6 ile çelişmiyor | uyarı listesi, yönetmen onayı |
| **Altyazı bölgesi** | y≈1250–1390'de metin taşıyan nesne | 0 (Anayasa §12-7) |
| **Donma (ffmpeg)** | `freezedetect` n=−55 dB d=1 s | 0 olay (kapı sıkılaştırıldı) |

## 11. Yönetmen kartı (her bölümün sahne yazarı `yonetmen_cK.md` yazar)

```
# cK — Yönetmen kartı
Renk anahtarı: …  · Işık: …  · Ana hareket yönü: … · İmza sekans: … (çekim aralığı s#–s#)
| çekim | çapa | tür | cam | giriş geçişi (tr, link) | neden böyle (bir cümle) |
Ölçek geçişleri: … (≥2) · Uzun plan(lar): … · Mizah vuruşları: … · Ses köprüleri: …
Bilinen kusur / ana ajandan ortak-kit isteği: …
```
Kart, çekim listesinin **gerekçeli** hâlidir; `qa_flow.py` bu kartı `shots` ile çapraz denetler.

## 12. Yasaklar

Slayt hissi (yerinde duran kart, yalnız `fade`); donmuş yakın figür; kaynaksız detay için "sinema" bahanesi (görsel, anlatının söylediğinin ötesine olgu taşımaz); kan/şiddet gösterimi (taşıyıcı mecaz kullanılır); rastgele renk/ışık değişimi; sert yön değişimi (§1-6) gerekçesiz; ekranı dolduran paragraf; altyazı bölgesi çakışması; aynı geçişin üst üste ≥3 kullanımı.
