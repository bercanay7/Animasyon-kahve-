# AN1 — Animasyon ve kurgu / ANİMASYON YÖNETMENİ (hareket kalitesi) — TUR 1, Medici Parça 1

## 1. Karar
**RED — 6,5 / 10** (eşik ≥9). Alt puanlar:

| Başlık | Puan |
|---|---:|
| Geçiş dili (iris/zoomthru/slide/candle/sayfa/light) | 9,0 |
| Kamera çeşitliliği ve gerçek (ölçülen) kamera hareketi | 5,5 |
| Figür ve nesne animasyonu (rig kalitesi 8,5; oyunculuk ilkeleri ve ekrandaki ağırlık 5,5) | 6,5 |
| "Akan ve çok animasyon" talebi: c0 açılış 9 · c1 7 · c2 4,5 | 6,5 |
| Ölü/donuk kare (gerçek donma yok; ama "canlı" değil, bkz. §3-E1) | 7,0 |
| 24 fps + hareket bulanıklığı yalnız geçişte | 6,5 |

Özet: Açılış (0–35 s) kanal çıtasının üstünde, sinematik ve gerekçeli. Parça ilerledikçe hareket enerjisi çöküyor: kare-farkı medyanı c0'da 2,48 → c1'de 0,81 → c2'de 0,31. Son ≈4 dakika büyük ölçüde "parşömen üzerinde yavaş itmeli bilgi kartı" zinciri. Kullanıcının pazarlıksız talebi ("olabildiğince akan ve çok animasyon; yönetmenlik olarak da usta ol") bu hâliyle karşılanmıyor. Düzeltme motor değişimi gerektirmiyor, mizansen ve animasyon ilkeleri gerektiriyor.

## 2. Ne gördüm / neye dayandım
**Sınır:** Videoyu OYNATAMADIM, sesi duyamadım. Kare dizileri, kare başına ölçümler ve kod/belge okumasıyla değerlendirdim. Başka üyenin raporunu/dosyasını görmedim.

- Okunan: `kurul/KURUL_BRIFI_P1.md`, `/home/user/sisifos-wt/CLAUDE.md` (kurul yöntemi), `YONETMENLIK_REHBERI.md`, `notlar_yonetmen_motoru.md`, `out_p1/kurul/{qa_flow_ozet.txt, hareket.json, teknik.json}`, `genel_01…04.png`, `gecis_{zoomthru,slide,iris,carry,yikama,sayfa,light,candle,ana_baslik_c1}.png`, `tam_01/02/04/10`. Kod: `cilt_anim.py` (figür kiti, ACTIONS), `cilt_cam.py` notları, `render.py` (FPS=24, tek zaman örneği), `cilt_fx.py:564` (deklanşör ≈0,3 kare). Karşılaştırma: `/home/user/sisifos-wt/sisifos/lib/{anim,core,film,figure}.js`, `sisifos_shorts.mp4` (30 fps, 1080×1920).
- **Kendi ölçümlerim** (scratch: `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/an1/`):
  - **Her kare** (14.442 kare, 320×180 gri) ardışık kare farkı (MAD): `pf.py` → `pf.json`. 0,5 sn adımlı eski eğriden 12× daha ince. Gürültü tabanı (grenli/tozlu boş parşömen) ≈0,07–0,11.
  - **Çekim bazında** medyan MAD / sessiz oran (qa_flow çekim tablosu t0'larıyla; ilk 1,0 sn geçiş payı atıldı).
  - **Gerçek kamera hareketi:** `zoom.py`/`smooth.py`: OpenCV LK + RANSAC ile saniye başına ölçek/kayma, tek tek çekimlerde.
  - Kontak sayfaları: 1,0–1,3 sn adımlı 4×N (çekimler s25, s44, s55, s70, s72, s74, s78), ardışık kare şeritleri (damga, bozuk para, yazıcı).
  - Sisifos Shorts'u için aynı MAD ölçümü (yalnız kabaca referans; dikey kadraj, 30 fps, daha kontrastlı).
- **Metrik uyarısı:** MAD kontrasta duyarlı; düz parşömende %1/sn'lik itme ≈0,2 MAD verir, küçük bir figürün jesti ≈0,1'den azdır. Bu yüzden "sessiz (MAD<0,25)" = "tam donuk" değil; "≤%1/sn kamera sürüklenmesi + küçük birikme animasyonu" demektir. Yine de gözle de doğruladım: s72, s74, s70, s78 kontak sayfaları aynı resmi veriyor.

**Ölçüm sonuçları:**
- Donma: gerçek özdeş kare 3 tane (428,92 / 482,42 / 539,54 s; hepsi geçiş başlangıcında, bkz. E7). Kare içi ani sıçrama ("pop") 0. Parlaklık sıçramaları yalnız geçişlerde (mum/ışık). Bu açıdan temiz.
- Hareket enerjisi (kare başına MAD medyanı): c0 (0–101 s) **2,48** · c1 (101–348 s) **0,81** · c2 (348–595 s) **0,31**. Dakika bazında 7. dakika (420–480 s): medyan **0,19**, süre %64 "sessiz". Sisifos Shorts referansı: medyan 1,48, sessiz oran %8; Medici P1 tamamı: medyan 0,68, sessiz oran %26 (c2'de %38).
- 0,5 sn medyanıyla MAD<0,25 olan **≥3 sn'lik 16 sessiz koşu, toplam 77 sn** (≥5 sn: 5 koşu). En uzunlar: 261,6 s (7,9 sn), 428,9 s (6,8), 421,5 s (6,5), 544,8 s (6,2), 161,4 s (5,7). qa_flow'un "Durgunluk" kapısı bunları yakalamıyor ("en uzun durgun koşu 0,5 sn"), çünkü τ=0,4 eşiği (0,5 sn adım) gerçekten donmuş kareyi ayırıyor, "canlı mı" sorusunu ölçmüyor.
- Geçişler 89 adet, toplam 84,5 sn = süre payı %14; toplam kare-farkı enerjisinin %31'i geçiş pencerelerinde. Yani "akış hissi" büyük ölçüde geçişlerden geliyor, çekim içinden değil (çekim içi medyan 0,61, geçiş içi 2,43).
- Kamera: 95 çekim, **78 push** (hepsi %6–8), 4 pull, 3 pan, 2 crane, 5 anahtar kareli, 3 kamerasız (başlık/kart/bitiş). `rack`, `orbit`, `hand`, `track` P1 sahnelerinde (`scenes_c0/c1/c2.py`, `p1_ortak.py`) **hiç kullanılmamış** (grep: 0). Nominal %6–8'lik itme gerçekte çok daha az: `c1_agi` (154–168 s) 11 sn'de ölçülen toplam ≈%2,2; 403,6 s çekiminde 405,2–407,2 s arası ölçek değişimi %0,004 (kamera fiilen durmuş). Kapı "nominal ≥%6" diye geçiyor.
- Kamera akıcılığı: 24 fps'te kademeleşme/titreme ölçülmedi (yavaş hareketler 0,5 px/kare altında, kare başı ölçek artışı düzgün). Kamera kaynaklı judder kusuru yok.
- Figür kiti: `cilt_anim.py` iskelet (IK, ayak kilitli yürüyüş, kumaş mesh'i, `Skin`) teknik olarak güçlü. 12 eylem var (idle/talk/bow/kneel/point/cheer/pray/write/count/handshake/threat/work). Ama: beklenti/öne hazırlık (anticipation), söner salınım (settle), çarpma sarsıntısı (shake), göz kırpma kodda **yok** (grep: 0). Sisifos `anim.js` bunların hepsini içeriyor.
- Figür ölçeği (kareden ölçtüm): yürüyenler kare yüksekliğinin ≈%22–25'i (58–62 s galeri, y≈690–950), masa başındakiler ≈%30–45'i (266 s yazıcı y≈460–950; ama kare genişliğinin yalnız ≈%15'i, sol kenarda), siluetler ≈%35 (436 s Cossa). Hepsi yan profil; galeri yürüyüşçüleri uzun cübbede, bacak okunmuyor. Figür türü çekimler ≈284 sn (üst sınır; çoğunda figür küçük/idle). Sisifos Shorts'ta kahraman dikey kareyi %60–90 dolduruyor.

## 3. Sıralı düzeltme listesi

**E1 — ENGELLEYİCİ: c1 sonu + c2 "kart-slayt" zinciri hareket yoğunluğu hedefini tutturmuyor (kullanıcının pazarlıksız talebi).**
- Pencere **421,0–557,5 s**: medyan MAD 0,22, %54 sessiz. Çekimler: timeline 421,0–428,9 (7,9 sn) · network 428,9–436,6 · c2_borc 436,6–449,9 (13,3 sn) · c2_ayrim 449,9–457,6 · c2_mezar 457,6–469,8 (12,2 sn; tek hareket mum/damga/harf oyma) · c2_rivayet 469,8–482,4 (12,6 sn) · emblem 482,4–487,1 · counter 487,1–491,3 · katasto 491,3–498,5 · stacked 498,5–504,7 · tree 511,6–516,5 · yil 523,2–531,0 · medal 531,0–539,5.
- Aynı desen c1'de: **154,2–167,9** (c1_agi 13,7 sn), **206,4–217,2**, **222,4–228,2** (tek düğümlü tree, %79 sessiz), **261,5–275,6** (Machiavelli 14,1 sn; yazıcı sol kenarda (kare genişliğinin ≈%15'i), karşıdaki siluet 14 sn kıpırdamıyor), **284,8–330** (kademe/medal/map/ledger/doc/kose: medyan 0,26, %47 sessiz) ve c0'da **69,3–78,0** (üç madalyon "gerekçe", %84 sessiz).
- Neden: kare alanının ≈%10–25'ini kaplayan bir nesne/etiket + geri kalanı boş parşömen; hareket = sıralı belirme (reveal) + ≤%1/sn itme. Yapı animasyonları (katasto 8.282 hane dolumu, para yağmuru, ağ kurulumu) iyi fikir, ama "hareket" değil "birikme"; birikme bitince kare duruyor.
- NE YAPILMALI (her çekim için, ≥25 çekim): (a) kartı bir **mekâna** bağla: masa üstü/defter/sokak maketi, nesneler fiziksel kayıp/düşüp/çevrilsin; (b) her çekimde birikme dışında **≥2 sürekli hareket eden öğe** (kayan sikke sütunu, çevrilen sayfa, yürüyen/jest yapan figür, ışık süpürmesi, paralaks katman); (c) ≥8 sn'lik çekimlerde **≥%12 ölçek ya da ≥200 px kamera yolu** (`track`/`rack`/`orbit`, bkz. E3); (d) 12–14 sn'lik çekimleri 2–3 çekime böl, aralarına **ölçek geçişi** (rehber §1-5) koy; (e) boş parşömen alanlarına yaşayan ortam (toz, mürekkep damlası, mum ışığı kayması) değil, **anlatıya çapalı** ikinci bir eylem koy.
- KABUL ÖLÇÜTÜ (benim metrikle, yeniden ölçülebilir): her 10 sn'lik pencerede kare farkı medyanı ≥0,6; ≥3 sn'lik sessiz koşu ≤4 adet (şimdi 16); c2 medyanı ≥0,9 (şimdi 0,31).

**E2 — ÖNEMLİ: Kamera dili tek tip ve gerçekte zayıf.**
- 95 çekimin 78'i %6–8 push; ölçülen gerçek itme 0,1–1 %/sn. Rehberdeki `rack/orbit/hand/track` P1'de 0 kez kullanıldı. `qa_flow` "Kamera hareket yeterliliği" nominal parametreyi denetliyor, gerçekleşen hareketi değil.
- NE YAPILMALI: (a) çekimlerin en az %30'unu farklı hareketle yeniden kamerala (pan r/l, crane, rack iki nesne arası, orbit yalnız maket/mimari, hand yalnız sokak); (b) ≥8 sn çekimlerde simetrik smoothstep yerine asimetrik eğri (hızlı giriş, uzun yumuşak çıkış) ya da geçişten devralınan hız; (c) kapıyı **ölçülü hareket** kapısına çevir: `zoom.py` mantığıyla (LK, 2 kare/sn) çekim başına gerçekleşen ölçek+kayma ≥%1,2/sn ya da ≥25 px/sn sürekli, yoksa "başka hareket kaynağı ≥2" şartı.
- Örnekler: 154,2 s (c1_agi), 403,6 s (c2_kasa; ilk 2,5 sn kamera durağan), 457,6 s (mezar), 544,5 s (Machiavelli yeniden).

**E3 — ÖNEMLİ: Figür oyunculuğu: ilkeler yok, ekrandaki ağırlık az.**
- `cilt_anim.py`'de anticipation, settle, shake, göz kırpma yok. Sonuç: eylemler sinüs/ease döngüsü; başlangıç/bitiş "mekanik". Figürler kare yüksekliğinin ≈%22–45'i, yatayda dar, yalnız idle/yazma döngüsü. Cossa (436–450 s) ve papa (469,8–482 s) siluetleri 12+ sn **hiç jest yapmıyor**, oysa `ACTIONS` içinde `point/bow/talk/handshake` hazır.
- NE YAPILMALI: Sisifos `anim.js` mantığını (`keyed`, `anticip`, `settle`, `idleOffsets`, `shake`) ~100 satırlık `anim.py` olarak taşı; şuraya uygula: eylem başlangıcında 3–5 karelik ters yönlü hazırlık, bitişte söner salınım (el/tüy kalem/baş), mühür/damga/para çarpmasında 2–4 px 6 karelik kamera/nesne sarsıntısı. Her bölüm için ≥2 "figür anı" (1,3–1,6× ölçek, 6–9 sn): örnek 261,5 s (Machiavelli ↔ siluet: talk/point + rack), 436,6 s (Giovanni ↔ Cossa: el uzatma/borç jesti), 331,2 s banka salonu (zaten iyi; kapanışta yakın plan).

**E4 — ÖNEMLİ: 24 fps + yalnız geçişte, üstelik kısa (0,3 kare) deklanşör.**
- Çekim içinde tek zaman örneği ⇒ hızlı küçük nesnelerde stroboskop: bozuk para yağmuru (394,0–395,5 s, ≈26 px/kare), damga inişi (470,2 s, 4 kareden ibaret), uçan tüy-kalem şeridi (≈267–273 s), demirci çekici, `rack` odak geçişleri. Geçişlerde bile deklanşör ≈1/80 sn (24p sinema normu 180° ≈ 1/48 sn).
- NE YAPILMALI: hız tabanlı seçmeli bulanıklık: sprite/öğe hızı >8 px/kare ise 3 alt örnek (yalnız o öğe, tam kare değil); pan ≥3 px/kare ise kamera alt örneklemesi; geçiş deklanşörü 0,5 kare. Yavaş kamera hareketlerine dokunma (zaten sub-piksel, temiz).

**E5 — KÜÇÜK-ÖNEMLİ: Geçişler parşömen→parşömen olduğunda ayırt edilemiyor.** c2'de A ve B aynı kâğıt zemin: zoomthru/slide/yikama "slayt kaydı" gibi okunuyor, `link=` nominal (örn. 380,3 → 386,1 → 391,8 s). NE YAPILMALI: kart→kart geçişlerde efekt yerine **eşleşen nesnenin devamı** (sikke yerinde kalır, etiket dönüşür, kamera sürer) ve geçiş sayısını bölümde azalt; efekti yalnız ölçek/mekân değişiminde kullan.

**E6 — KÜÇÜK: Aynı mizansen 3 kez.** `c1_machiavelli`: 261,5 s, 544,5 s, 580,2 s (yazıcı + soru işaretli siluet + şerit). 2. ve 3. kullanımda farklı açı/yön/poz/kamera ya da farklı jest.

**E7 — KÜÇÜK: 3 geçişte 1 karelik tekrar** (özdeş ardışık kare): 428,92 · 482,42 · 539,54 s (geçiş k=0 karesi önceki karenin aynısı). Geçiş ilerlemesini k=(n+1)/N yap ya da ilk kareyi atla.

**E8 — KÜÇÜK: Tek damga jesti.** ÇEVİRİ/FRANSIZCA/ANEKDOT×3/BİR HESABA GÖRE/ETMEDİLER/KURGU/İTİRAZ aynı "büyükten küçüğe, 4 karede" inişi (470,2 s). Çeşitlendir: mürekkep yayılması, kâğıt çökmesi, gölge sıçraması, kısa sarsıntı (E3 ile birlikte).

**E9 — KÜÇÜK: Ana başlık 101,2–107,7 s kamerasız** (qa tablosu "—"; MAD 0,76): harfler açılıyor ama kare duruyor. Yavaş itme + yıldız parıltısı/altın süpürme ekle.

**Korunacaklar (dokunma):** c0 açılış 0–35 s (skyline pan → push → iris → slide → mum → zoomthru; çekim içi medyan MAD 2,6; her geçişin gerekçesi görünüyor); 331,2 s banka salonu uzun planı; 184–206 s veba renk soluşu; geçiş katalogu ve `lead/birth` mantığı; 0 pop, 0 donma.

## 4. En emin olmadığım nokta
1. **Algı payı:** c2 yoğun, sayısal, sözcüğe çapalı bir anlatı (kambiyo, faiz, catasto). Kart-yapı animasyonu bu içerikte pedagojik olarak doğru bir tercih olabilir; kurgu/ritim üyesi ve başkan, "slayt hissi" ile "açıklama netliği" dengesini benden farklı tartabilir. Benim itirazım: hareketin **süre boyunca** (≥6 sn) birikmeden ibaret kalması ve kameranın fiilen durması; kartların kendisi değil.
2. **MAD metriği** düz parşömende hareketi olduğundan az, kontrastlı sahnede olduğundan çok gösterebilir; 0,6/0,25 eşikleri benim kalibrasyonum (yalnız P1 ve bir Sisifos Shorts'u). Eşikleri nihai yapmadan başkan 3–4 çekimde gözle teyit etmeli (öneri: 421, 457,6, 544,5, 154,2 s).
3. E4'teki stroboskop şiddeti: 24 fps'te gerçek oynatmada ne kadar rahatsız ettiğini göremedim; ölçülen hız (≈26 px/kare) ve kare şeritlerine dayanıyorum.

## 5. Motor sorusu (animasyon açısından)
Mevcut motor animasyon için **yeterli bir iskelet, ama "animasyon yönetmenliği" katmanı eksik**; yeniden yazmaya ya da başka motora (Canvas2D/Chromium) geçmeye değmez, mevcut motoru iyileştirmek doğru. Sisifos hattıyla kıyas: **figür rigi** teknik olarak Medici'de ileri (kâğıt-kukla skinning, kumaş mesh'i, ayak kilitli IK, rim ışığı; Sisifos çubuk-IK + kazıma çizgisi), fakat **oyunculuk ilkeleri ve ekrandaki ağırlık** geride: Sisifos'ta kahraman kareyi dolduruyor (kayayı iten adam, düşen asker) ve `anim.js` ile hazırlık/söner salınım/çarpma sarsıntısı/göz kırpma var; Medici'de bunların hiçbiri kodda yok, figürler yatayda dar ve idle/yazma döngüsünde. **Kamera/geçiş dili** söz dağarcığı ve gerekçe disiplini bakımından Sisifos'un (translate/rotate/scale + paralaks, fade/wipe/cut) çok önünde (12 geçiş, `link`, `lead/birth`, `qa_flow`), ama P1'de kullanımı geride: çekimlerin %82'si aynı %6–8 push, `rack/orbit/hand/track` 0 kez, ölçülen gerçek hareket düşük. **24 fps tek başına kusur değil** (sinema normu, YouTube 1080p24 ≈8 Mb/sn doğru ayar, yavaş kamera hareketi sub-piksel ve temiz); kusur olan, **24 fps'in deklanşörsüz hızlı hareketle birleşmesi**: Sisifos her karede 4 alt örnekli 180° bulanıklık uyguluyor (30 fps), Medici çekim içinde sıfır, geçişte yalnız 0,3 kare uyguluyor; bozuk para/damga/tüy kalem gibi hızlı küçük öğelerde stroboskop var, bunu seçmeli (hız tabanlı) bulanıklıkla çözmek yeter, tüm kareleri alt örneklemek gerekmez. Yeniden yazma (≈35 çekim türü, 12 geçiş, skinning figür kiti, qa_flow) haftalar sürer ve eksik olan şeyi (mizansen + animasyon ilkeleri + hareket yoğunluğu kapısı) vermez; Chromium'da da 4 alt örnek render maliyeti ≈4× olur.

**En yüksek getirili 3 iyileştirme:**
1. **Ölçülü hareket kapısı + c1 sonu/c2 yeniden mizansen (E1, E2c):** `qa_flow`'a LK tabanlı gerçekleşen-hareket ölçümü (0,5 gün; `smooth.py/zoom.py` hazır mantık) ve ≈25 çekimin yeniden sahnelenmesi (mekân + ≥2 sürekli hareket + uzun çekimleri bölme). Maliyet ≈2–2,5 gün sahne yazımı + kısmi yeniden render ≈8–10 dk (c1 sonu + c2 ≈%45 süre, 4 işçi). En büyük kazanç: kullanıcının "akan ve çok animasyon" talebi.
2. **`anim.py` animasyon ilkeleri + figür ölçeği/oyunculuğu + kamera çeşitlendirme (E2, E3, E8):** Sisifos `anim.js`'in ≈100 satırlık portu; damga/mühür/para çarpmasına sarsıntı, eylem başı/sonuna hazırlık/söner salınım; bölüm başına 2 yakın "figür anı"; çekimlerin ≥%30'unda `pan/crane/rack/track`. Maliyet ≈1,5 gün; render maliyeti ≈0.
3. **Seçmeli deklanşör (E4):** hız >8 px/kare olan öğeler için 3 alt örnek, pan ≥3 px/kare için kamera alt örneklemesi, geçiş deklanşörü 0,3→0,5 kare. Maliyet ≈1–1,5 gün; render süresi yalnız etkilenen karelerde +%30–60 (≈+4–8 dk/10 dk'lık parça).

Toplam ≈5 gün iş + tam yeniden render ≈17–25 dk; ardından aynı üyeyle regresyon turu önerilir (hedef ≥9: E1 kabul ölçütü + E2/E3 teyidi).
