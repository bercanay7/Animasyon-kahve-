# AN1 — TUR 2 · Animasyon ve kurgu / ANİMASYON YÖNETMENİ (hareket fiziği, kamera, geçiş zanaati) — Medici Parça 1 v2

## 1. Karar
**RED — 7,5 / 10.** Tur 1'de 6,5 vermiştim; eşik ≥9.

| Başlık | Tur 1 | Tur 2 | Gerekçe |
|---|---:|---:|---|
| Geçiş dili | 9,0 | 8,5 | Tempo artık çeşitli (σ 0,38 sn) ve 39 sert kesme var. Buna karşılık aynı kartta 3 atlamalı kesme çıktı, ışık patlaması 13 kez kullanılmış. |
| Kamera (beyan edilen değil, ölçülen) | 5,5 | 7,5 | Pan, truck ve tilt gerçekten hareket ediyor; itme payı %82'den %35'e indi. Ama 5 çekimde beyan edilen kamera hiç uygulanmıyor (açılış + 4 harita, 24 sn). |
| Figür ve nesne animasyonu | 6,5 | 6,0 | Figür ölçeği ve iki kişilik etkileşim büyük kazanç. Ama yeni bir engelleyici var (papa hançer çekiyor). Figür kitinde hâlâ hazırlık, oturma ve göz kırpma yok. Ayrıca yarım sikke hatası var. |
| "Akan ve çok animasyon" talebi | 6,5 | 8,0 | Sessiz süre %26,4'ten %9,6'ya indi; ≥3 sn'lik sessiz koşu 16'dan 1'e düştü. Yine de 5 sessiz cep kalıyor. |
| Ölü/donuk kare | 7,0 | 7,5 | Donma ve "pop" yok, geçişlerdeki çift kare giderilmiş. Ama 2 boş açılış var ve ilk 3,7 sn durağan. |
| 24 fps + deklanşör | 6,5 | 7,5 | Kamera savrulmasında 180° bulanıklık gerçekten çalışıyor (39,9–40,2 sn). Küçük hızlı nesnelerde hiç devreye girmiyor. |

**Özet.** v2 benim alanımda gerçek bir sıçrama. Bunu aynı motorla başardı, yani tur 1'deki "motoru baştan yazma, iyileştir" kararı ölçümle doğrulandı. Ancak c2'yi dünya sahnelerine çevirirken bir **engelleyici** girdi: Papa V. Martinus, "aforoz tehdidi" çekiminde hançer çekiyor (471,7–475,8 sn). Bunun yanında birkaç önemli hata kaldı: beyan edilen ama uygulanmayan kamera, aynı kartta atlamalı kesme, yarım sikke hatası ve figür oyunculuğundaki eksik ilkeler. Bunlar ucuz düzeltmeler (≈2 gün); düzelirse ≥9 mümkün.

## 2. Ne gördüm / neye dayandım
**Sınır:** videoyu OYNATAMADIM, sesi DUYAMADIM. Kare dizileri, kare başına ölçümler ve kod/belge okumasıyla değerlendirdim.

- **Okuduğum belgeler:**
  - `kurul/KURUL_BRIFI_P1_TUR2.md`, `kurul/KURUL.md` (tur 1 kararları + tur 2 KA1/KA2);
  - `notlar_hareket.md`;
  - `out_p1/kurul/qa_flow_ozet.txt` (son program: 17 GEÇTİ / 0 KALDI / 1 UYARI), `teknik.json`, `out_p1/uretim_v2.log`;
  - `out_p1/duzeltme/ENG-B/` (deklanşör önce/sonra, geçiş k testi);
  - kod: `scenes_c2.py:184-192`, `p1_ortak.py:21-50`, `cilt_anim.py` (`grep`), `anim.py`, `compose.py:559`;
  - çapraz eleştiri için tur 1 `AN2.md` (ilk bölüm) ve tur 2 `PK1.md` (§4).
- **Kendi ölçümlerim** (v2: 14.365 kare). Scratch dizini: `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/an1v2/`. Tur 1 verisi de aynı yöntemle `../an1/pf.json` içinde.
  1. **Kare farkı:** her kare için ardışık kare farkı (MAD, 320×180 gri) → `pf_v2.json`; v1 ile karşılaştırma `stats.py`.
  2. **Gerçek kamera hareketi:** OpenCV LK + RANSAC afin, 0,5 sn adımla (`cam.py`, `cam2.py`). Tüm çekimlerde "beyan edilen ↔ gerçekleşen" taraması (`camscan.txt`); şüpheli çekimleri kenar faz korelasyonuyla ve gözle ikinci kez doğruladım (`staticcheck.png`).
  3. **Kare kenarı:** iki yan kenar 2 kare/sn tarandı (`edges_v2.json`).
  4. **Küçük nesne hızı:** Farneback optik akışı (`flow.py`).
  5. **Kare şeritleri:** 4 kare/sn ve tam kare hızında (`dagger.png`, `popearm.png`, `cuts_same_card.png`, `coin302.png`, `blank424.png`, `blank534.png`, `coinzoom.png`, `konst.png`, `martinus.png`, `start05/125.png` = 106 çekimin açılış mozaiği).
- **Metrik uyarısı:** v2'de kodlama değişti (CRF 19, slow, aq-mode 3, 10,3 Mb/sn). Gren daha iyi korunduğu için gürültü tabanı biraz yükseldi: p1 0,069 → 0,087, p5 0,109 → 0,162. Bu, sessiz oranını v2 lehine birkaç puan iyileştirir. Ama %26 → %10'luk düşüşü açıklayamaz; ayrıca aynı sahneleri gözle de karşılaştırdım.

**Ana ölçümler (v1 → v2):**

| Ölçü | v1 | v2 |
|---|---:|---:|
| Kare farkı medyanı (bütün) / çekim içi | 0,68 / 0,61 | 0,83 / 0,80 |
| Bölüm medyanı c0 / c1 / c2 | 2,48 / 0,81 / 0,35 | 1,69 / 0,98 / 0,67 |
| Eski "kart vadisi" aralığı (v1 421–557 ↔ v2 416–552) | 0,22 | 0,60 |
| Sessiz süre (0,5 sn medyanı <0,25) | 158,7 sn (%26,4) | 57,3 sn (%9,6) |
| ≥1,5 sn sessiz koşu | 34 (114 sn) | 11 (24 sn) |
| ≥3 sn sessiz koşu | 16 (77 sn) | **1** (3,9 sn, 318,9 sn) |
| 10 sn'lik pencere medyanı <0,6 / <0,4 | 29/60 / 23 | 17/59 / 5 |
| Geçiş pencerelerinin süre / enerji payı | %14 / %31 | %10 / %24 |
| İtme payı / en uzun itme dizisi | %82 / 26 | %35 / 4 |
| Sert kesme / geçiş süresi σ | 4 / ≈0,02 sn | 39 / 0,38 sn |
| Figür boyu (kare yüksekliğine oranla, ana sahneler) | %22–45 | %45–60 (Konstanz ≈%52, Giovanni–Cossa ≈%45, Martinus yakın ≈%60) |

## 3. Tur 1 maddelerinin durumu

| Madde | Durum | Kanıt |
|---|---|---|
| **E1** c1 sonu + c2 kart zinciri (engelleyiciydi) | **KISMEN.** Engelleyiciden "önemli"ye indi. | c2 dünya/figür sahnelerine çevrilmiş: Konstanz salonu 440–445, Martinus taht odası 460–476, ölüm döşeği 518 ve 545, catasto sokağı 486, Brugge 351. Sessiz koşu ≥3 sn 16 → 1, c2 medyanı 0,35 → 0,67. Tur 1 kabul ölçütümden yalnız biri tuttu: "≥3 sn koşu ≤4" ✓. "Her 10 sn penceresinde ≥0,6" ✗ (17 pencere altında) ve "c2 ≥0,9" ✗ (0,67) tutmadı. Kalan cepler Y4'te. |
| **E2** tek tip ve zayıf kamera | **KISMEN.** | Gerçekleşen hareketler artık ölçülebilir: c2_ayrim pan −153 px/7 sn, c2_kasa −192 px/7,5 sn, c2_sadaka truck −154 px/5,5 sn, c2_mezar tilt +84 px/6,5 sn, p1_timeline −84 px, p1_medal −119 px, c1_kose itme +%4,7/5 sn, p1_ledger çekme −%5,7. Bunlar ölçek ya da yatay/dikey kaymadır. `ease`, `whip`, `shake` ve süreye bağlı itme eklenmiş. Açık kalan: 5 çekimde kamera hiç oynamıyor (Y2). "Ölçülen hareket" kapısı eklenmiş ama eşiği gevşek (Y4b). `rack`/`orbit` hâlâ hiç kullanılmamış; bu bir hata sayılmaz. |
| **E3** figür oyunculuğu ve ekrandaki ağırlık | **KISMEN.** | Kazanılanlar: figür boyu %45–60; temas gölgesi (`cilt_anim.py:1036` `CONTACT_SHADOW`); iki kişilik eylemler. 431,6–440 sn'de Giovanni Cossa'ya belge uzatıyor, 439,25 sn'de tiara beliriyor, 440–445 sn'de Konstanz'da taç düşüyor, 467–471 sn'de Martinus mitrayı geri istiyor. Açık kalan: `anim.anticip/settle/blink` figür kitine bağlanmamış (`cilt_anim.py`, `cilt_oda.py` ve `cilt_sehir.py` içinde `grep` sonucu 0); jestler hâlâ tek eklemli sinüs ya da kolay-geçiş (ease) salınımı. Ayrıca bkz. Y1 ve Y9. |
| **E4** 24 fps, yalnız geçişte deklanşör | **KISMEN.** | Kamera ve büyük alan hareketinde 180° deklanşör çalışıyor: 39,9–40,2 sn belge savrulmasında satırlar yön bulanıklığıyla akıyor (`ENG-B/deklansor_1e1_40.2s.jpg` ile videodaki kare aynı). Küçük hızlı nesnelerde çalışmıyor: 389,5–391,5 sn florin yağmuru 16–21 px/kare hızla düşüyor ama sikkeler jilet gibi keskin (`coinzoom.png`). `anim.hint_speed` hiçbir sahne ya da tür tarafından çağrılmıyor (`grep`: yalnız `compose.py`/`shots.py` tanımları). Bkz. Y7; Y5 de büyük olasılıkla bununla ilgili. |
| **E5** parşömenden parşömene ayırt edilemeyen geçişler | **BÜYÜK ÖLÇÜDE KAPANDI.** | Kart → kart sınırlarının çoğu artık kesme ya da 0,3–0,4 sn'lik "vuruş" kaydırması. Kalan: 423,9 (timeline → network, ışık) ve 452,6 (ayrım → mezar, ışık). Bunlar Y8 ile birlikte çözülür. |
| **E6** Machiavelli mizanseni 3 kez | **KISMEN.** | `c1_machiavelli` artık bir kez kullanılıyor (539,4 sn, 5,8 sn). Ama tur 1'deki düzen aynı kalmış: solda sarı cüppeli yazıcı, sağda siyah siluet. Medyan 0,26, karelerin %46'sı sessiz. Kütüphane odası 253,2 / 258,4 / 575,5 sn'de farklı kameralarla dönüyor; bu kabul edilebilir. |
| **E7** geçiş başında tekrar eden kare | **KAPANDI** (geçişlerde). | Geçişlerde özdeş kare yok. Kalan, kesmede 1 karelik duruş: 43,92 sn (ortalama fark 0,031) ve 482,25 sn (0,015; en büyük fark 7 düzey; pratikte özdeş). Bkz. Y11. |
| **E8** tek damga jesti | **KAPANDI.** | Profiller `squash/bounce/drop/spin/ink`, bölüm başına en fazla 2 (scenes_c1/c2). Darbe sarsıntısı `impact_ovl` 2 yerde (c2s16, c2s20). |
| **E9** ana başlık kamerasız | **KAPANDI.** | Fresk başlığı 4,5 sn. Kamerasız ama medyan 0,66 ve donuk kare yok; kurulum hızlı. |
| Motor önerisi 1: ölçülü hareket kapısı | **KISMEN.** | Kapı var (`qa_flow` "Ölçülen hareket"). Ama eşik gevşek ve beyan ↔ gerçekleşen denetimi yok (Y2, Y4b). |
| Motor önerisi 2: `anim.py` | **KISMEN.** | Kütüphane iyi yazılmış ve damga, mühür, takvim ve madalyonda kullanılıyor. Figür kitine bağlanmamış. |
| Motor önerisi 3: seçici deklanşör | **KISMEN.** | Kamera ve büyük alan hareketinde var; küçük nesnede yok. |
| Korunacaklar: c0 açılışı | **KISMEN GERİLEDİ.** | 0–3,7 sn "kapak yankısı" kamerası 0 px (Y2). 3,7–35 sn medyanı 2,62 → 1,92. Mum, taht, takvim ve belge savrulması hâlâ güçlü. |
| Korunacaklar: 0 pop, 0 donma, veba soluşu, banka salonu | **KORUNDU.** | `uretim_v2.log`: siyah/donuk bölge 0, kare hatası 0. 181,2 sn yikama 2,0 sn renk soluşu var, medyan 1,81. |

## 4. Yeni sorunlar (öneme göre sıralı)

**Y1 — ENGELLEYİCİ: Papa V. Martinus hançer çekiyor (471,7–475,8 sn, "aforoz tehdidi").**
- **Kanıt (`dagger.png`, `popearm.png`):**
  - 471,9 sn: sağ elinde kalça hizasında hançer (x≈1280–1330, y≈350–530).
  - 472,7 sn: hançer başının üstünde (x≈1220–1270, y≈150–300).
  - 473,0–475,5 sn: kalkık kol yüzü ve tiarayı kapatıyor; elin ucu "AFOROZ TEHDİDİ" etiketinin (x≈645–1275, y≈158–243) altında kalıyor.
- **Kod:** `scenes_c2.py:186` `dict(kind="papa", …, action="threat")`. `cilt_anim.act_threat` kitte "şiddet işareti: hançer yükselir" diye tanımlı.
- **Neden engelleyici:** aforoz manevi/hukuki bir tehdittir. Ekranda papa Giovanni'ye bıçak kaldırıyor; bu belgesiz bir şiddet olgusu üretir (de Roover n. 45 yalnız aforoz tehdidini anlatır). Ayrıca dinî figürü silahla gösterir. Kaynak ve hassasiyet alanlarının veto kapsamına girer; onlara da iletilmeli.
- **Ne yapılmalı:**
  - `action="point"`: işaret parmağı Giovanni'ye uzanır, ≈0,15 sn hazırlıkla. Ya da `talk` + kaldırılmış avuç, ya da elinde mühürlü papalık belgesi/bulla (`prop="book"`).
  - Bıçak hiçbir karede görünmesin.
  - Jestte uzak kolu kullan ya da kolu öne 45° aç; yüz ve tiara kapanmasın.
  - Etiketi y≈200'den y≈130'a al, ya da kolun üst sınırını y≥300'de tut.
- **Maliyet:** 1 satır + 4 sn'lik bölümün yeniden render'ı.

**Y2 — ÖNEMLİ: Beyan edilen kamera 5 çekimde hiç uygulanmıyor (toplam ≈24 sn). `qa_flow` bunları "kamera var" diye geçiriyor.**
- **#0 `kapak_kilit` (0,0–3,7 sn), `cam=("push",)`:** 0,6 ile 2,9 sn arasında ölçek 1,0000 ve kayma 0,0 px. LK afin (435/798 iç nokta) ve kenar faz korelasyonu aynı sonucu veriyor. Kare başına fark medyanı 0,14, yani gren tabanı. **Videonun ilk 3,7 saniyesi bütün parçanın en hareketsiz yeri.**
- **`p1_map` ×4:** #51 291,8 (push 0,07), #55 313,0 (pull), #62 361,1–368,8 (pull; 7,7 sn), #69 406,0–412,7 (pan r; 6,7 sn). Hepsinde ölçek ±%0,3 ve kayma ≤2 px; #62 ve #69'da faz korelasyonu da 0,0. Yalnız rota çizgisi hareket ediyor (`map361.png`).
- **Olası neden:** `p1_ortak._wrap` "map" içteki türü çağırıyor, ama kamera ön ayarı (`mapsk.Cam` yaması) içteki çağrıya ulaşmıyor gibi. `kapak_kilit` de `cam=`'yi yok sayıyor.
- **Ne yapılmalı:**
  1. Bu türlerde kamerayı uygula. Kapakta ≥%4 itme, kilit kapanınca `impact_ovl` sarsıntısı, zincirde `settle`, altında ışık süpürmesi. Haritada pan/itme ve rota ucunu izleyen kamera.
  2. `qa_flow`'a **"beyan ↔ gerçekleşen" kapısı** ekle: `cam=` verilen her çekimde, çekim içinde video karelerinden ölçülen ölçek/kayma, beyan edilenin en az %50'si olmalı. Bu kapı bu 5 çekimi otomatik yakalardı.
- **Maliyet:** ≈0,5 gün.

**Y3 — ÖNEMLİ: Aynı kart üzerinde atlamalı kesme (jump cut) ×3. "Sert kesme payı ≥%15" kapısının yan etkisi (`cuts_same_card.png`).**
- **427,6 sn (#72 → #73 network):** aynı "FLORANSA" ikonu ve başlık, ≈%1 ölçek değişimi, kamera yönü itmeden çekmeye dönüyor. Kesme anındaki kare farkı 1,3; tipik kesmede bu 30–60. Kesme gibi değil, takılma gibi okunur.
- **480,2 sn (#83 → #84):** ortadaki anahtarlar (x≈820–1100, y≈300–560) kayboluyor, iki kare yalnız boş koyu levha kalıyor, ardından anahtarlar solda küçük olarak (x≈270–460) beliriyor.
- **482,2 sn (#84 → #85):** soldaki anahtarlar kesmede yok oluyor, levha yerinde kalıyor.
- **Ne yapılmalı:** aynı kompozisyonun devamında kesme yapma. Öğeyi çekim içinde hareket ettir: anahtar sola süzülüp küçülür (`settle`), çubuk kayarak gelir. Ya da üç çekimi tek uzun çekimde birleştir. Kesme kapısı yalnız mekân, ölçek ya da konu değişen sınırları saymalı.

**Y4 — ÖNEMLİ: Kalan sessiz cepler (kare farkı medyanı ve 0,25'in altındaki karelerin oranı).**
- **(a) Cepler:**

  | Çekim | Aralık (sn) | Medyan | <0,25 olan kareler |
  |---|---|---:|---:|
  | Anahtar üçlüsü (#83–85) | 475,8–486,4 | 0,17 | %65 |
  | Network çifti | 423,9–431,6 | 0,23 | %58 |
  | `c1_kose` | 316,9–323,4 | 0,24 | %58 |
  | Kambiyo haritası (Y2 ile aynı) | 361,1–368,8 | 0,22 | %54 |
  | `p1_doc` "Ciompi'nin talepleri" | 244,9–253,2 | 0,26 | %44 |
  | `c1_machiavelli` | 539,4–545,2 | 0,26 | %46 |

  Her birine anlatıya bağlı ikinci bir sürekli hareket ekle: el, figür, ışık süpürmesi, kayan nesne. ≥6 sn'lik olanlarda ≥%1/sn kamera gerekir.
- **(b) "Ölçülen hareket" kapısının eşiği:** 0,5 sn adımda medyan ≥1,25, kabaca kare başına ≈0,1'e denk geliyor. Bu benim ölçeğimdeki gren tabanına (0,07–0,09) çok yakın; kapı "canlı mı" değil "donmamış mı" sorusunu ölçüyor. Önerim: ya ≥%1/sn ölçek ya da ≥20 px/sn gerçekleşen kamera, ya da kameradan bağımsız hareket eden alan ≥%3.

**Y5 — ÖNEMLİ: Yarım sikke hatası (302,29–302,62 sn; sikke x≈310–730, y≈350–770; `coin302.png`, `coin302b.png`).** Kesmeden hemen sonra sikkenin yalnız sol yarısı keskin dikey bir kenarla görünüyor. Sağ yarı yarı saydam ve ortasında sert bir dikiş var; ≈8 kare sonra bütünleşiyor. Aynı türün diğer çekimleri temiz (105,6 ve 113,5 sn). Muhtemel neden: kesmede `lead` olmadan başlayan dönme girişi ile deklanşör alt örneklemesinin ya da açılma maskesinin etkileşimi. Nedenini değil belirtiyi görüyorum. **Ne yapılmalı:** bu çekimde sikke çerçevenin içinde, kenardan (yan profilden) başlasın (#18 ve #20'deki gibi). Ya da `shutter=False` ile dene; ardından iki karede yeniden denetle.

**Y6 — ÖNEMLİ/KÜÇÜK: Boş parşömenle açılan çekimler ("ölü açılış").**
- **423,75–425,2 sn (#72):** ışık geçişinden sonra ≈1,4 sn boyunca yalnız soluk başlık var; ilk ikon 425,25 sn'de geliyor (`blank424.png`).
- **534,5–536,1 sn (#95):** sert kesme doğrudan boş parşömene iniyor, ilk kart 536,2 sn'de geliyor; truck kamera ölçümde yalnız −6 px (`blank534.png`).
- **Ne yapılmalı:** ilk öğeyi geçişten/kesmeden 0,3 sn önce doğur (`lead`/`birth`), ya da kesmeyi öğenin girişine kaydır.

**Y7 — KÜÇÜK-ÖNEMLİ: Küçük hızlı nesnelerde deklanşör yok.** Florin yağmurunda (389,5–391,5 sn) hız 16–21 px/kare ve bulanıklık sıfır (E4). **Ne yapılmalı:** sikke, damga ve tüy kalem çizen türlerde `anim.hint_speed(cx, v)` çağır. Maliyet ≈2 saat; render süresine etkisi yalnız bu karelerde.

**Y8 — KÜÇÜK: Işık patlaması 13 kez (qa dağılımı 12), bunun 8'i c2'de.** Çekimler: #60, #72, #74, #77, #83, #94, #98, #104. Aynı ışınlı parlama her ≈31 sn'de bir geliyor ve hazır efekt (preset) gibi okunuyor. Rehber §3 bu geçişi "ifşa, yıldız an" için ayırır. Parça başına ≤4'e indir; gerisi kesme, malzeme geçişi ya da eşleşen nesne olsun.

**Y9 — KÜÇÜK: Figür jest okunurluğu.** 462,0 sn'de "İTİRAZ" damgası papanın yüzünün üstüne basılıyor (x≈1000–1350, y≈130–420; `pope2.png`). Damgayı figürün dışına al.

**Y10 — KÜÇÜK: Set kenarı görünüyor (545,5–546,0 sn).** Sol kenarda x≈0–10, y≈150–950 boyunca lacivert bir şerit var; oda dekoru bitiyor (`crop545_left.png`). Kamerada ≥%2 örtme zumu ya da dekoru genişletmek yeter.

**Y11 — KÜÇÜK: Kesmede 1 karelik duruş.** Kesmeden hemen sonra kamera durgun: 43,92 ve 482,25 sn. Kesmeden hemen önce kamera durgun: 416,0, 480,2 ve 502,8 sn. Kalan 34/39 kesmede "hareket üstünde kesme" kuralı tutuyor.

**Y12 — KÜÇÜK (kabul edilebilir):** `qa` yön uyarısı #15 (86,5 sn) "nasıl geldi?" sorusunda geçmişe dönüş, yani sağdan sola. Yönetmen kartına gerekçesi yazılırsa kabul.

## 5. Kullanıcının sorusu: "Bu çizim tarzı çok mu basit, ucuz görünüyor; yapay zekâ ile üretilmiş gibi mi duruyor?"

- **YZ gibi durmuyor.** YZ videosunun hareket izleri hiçbir karede yok: kareden kareye eriyen eller, kimliği kayan yüzler, titreşen dokular, fizik dışı akış. Her hareket deterministik ve anahtar karelidir, aynı çizim kareden kareye korunuyor (ör. 431,6–440 sn Giovanni–Cossa, 214 ve 267 sn alaylar). Buradaki risk tersidir: "mekanik kâğıt kukla" hissi.
- **Düz biçim dili tek başına ucuz değil, bir üsluptur.** Basitlik yalnız hareketin olmadığı yerde ucuz okunuyor: ilk 3,7 sn kamerası 0 px oynayan kapak karesi; kamerası hiç oynamayan dört harita (361–369 sn); aynı kartta atlamalı kesmeler (427,6 / 480,2 / 482,2) ve boş parşömenle açılan çekimler (423,9 / 534,5). Bunlar "slayt değişti" gibi okunuyor.
- **En "Flash animasyonu" okunan yer figür oyunculuğu.** Kollar tek eklemden sallanıyor; hazırlık, oturma, göz kırpma ve diyalogda baş çevirme yok. 13 kez tekrarlanan aynı ışık patlaması da hazır efekt gibi duruyor.
- **Pahalı ve "elden çıkma" okunan yerler:**
  - 3,7–35 sn oda, taht ve takvim; 39,9–40,2 sn belge savrulmasında gerçek hareket bulanıklığı;
  - 214 ve 267 sn yürüyen alaylar;
  - 440–445 sn Konstanz'da düşen taç;
  - yikama, sayfa ve giornata malzeme geçişleri: bunlar şablon değil, imza.
- **En yüksek getirili düzeltme:** figür kitine hazırlık, oturma ve göz kırpma bağlamak, kapak yankısını canlandırmak, Y2 ve Y3'ü kapatmak. Toplam ≈1,5 gün.

## 6. Çapraz eleştiri (kısa)
- **AN2 (tur 1):** "tek tempo geçiş + 26'lık itme dizisi" tanısına katılıyorum; v2 bunu çözdü (σ 0,38, en uzun itme dizisi 4). Ama düzeltmenin aracı olan "kesme payı ≥%15" kapısı, aynı kartta 3 atlamalı kesme üretti (Y3). AN2'nin ritim merceğinden bakması gereken yer: 427,6, 480,2, 482,2 sn.
- **PK1 (tur 2 §4):** "7:56'da yalnız anahtarlar … slayt şablonu" gözlemi benim ölçümümle örtüşüyor: anahtar üçlüsü parçanın en sessiz cebi (medyan 0,17). "Açılış ne ucuz ne YZ" yargısına kısmen katılmıyorum. Kompozisyon güçlü, ama hareket merceğinden ilk 3,7 sn videonun en durağan anı (kamera 0 px). Kapak yankısı korunarak canlandırılmalı.
- **KA1/KA2 (veto) için:** Y1'deki hançer belgesiz bir şiddet olgusu ve dinî hassasiyet konusu. Bunu sizin alanınızda da engelleyici saymanızı öneririm.

## 7. En emin olmadığım nokta
1. **Y5 (yarım sikke):** belirti 7 karede net, nedeni (deklanşör mü, açılma maskesi mi) koddan doğrulamadım.
2. **Y2 (`p1_map`):** "hareketsiz" bulgusu iki yöntemle ve gözle tutarlı. Ama sahne yazarı rotanın okunurluğu için kamerayı bilerek kapatmış olabilir. O durumda `cam=` beyan edilmemeli ve `qa` bu çekimleri "kamera var" saymamalı. Bulgunun özü, beyan ile gerçekleşenin uyuşmaması.
3. **Eşiklerim:** MAD eşiklerimi (0,25 / 0,6) kendim kalibre ettim. v2'de gren tabanı biraz yükseldi; sessiz oranındaki iyileşmenin birkaç puanı bundan gelebilir. Başkan 6 cebin 2–3'ünü gözle teyit etmeli; öneri: 475,8, 423,9, 316,9 sn.
4. **Hareket halinde algı:** Y1'de hançerin 4 sn'lik hareket içinde ne kadar fark edildiğini oynatarak göremedim. Ama bıçak iki ayrı karede açıkça çizili ve sahne kodu bunu doğruluyor.

## 8. ≥9 için yol (maliyet tahminiyle)
1. **Y1:** `threat` → `point`/`talk`/bulla; bıçak yok, yüz açık. 1 satır, kısa render.
2. **Y2:** `kapak_kilit` ve `p1_map` kamera uygulaması + `qa` "beyan ↔ gerçekleşen" kapısı. ≈0,5 gün.
3. **Y3 + Y6:** aynı kartta kesme yerine çekim içi hareket; ilk öğeyi önceden doğur. ≈3 saat.
4. **Y5 + Y7:** yarım sikke; `hint_speed` çağrıları. ≈3–4 saat.
5. **E3:** `act_point/talk/bow/handshake/write`'a `anticip` (≈0,15 sn) + `settle` (≈0,4 sn, %10 aşma), bütün figürlere `blink`/`breathe`, iki kişilik sahnelerde konuşana baş çevirme. ≈0,5–1 gün.
6. **Y4a + Y8:** 6 sessiz cebe ikinci hareket; ışık patlamasını ≤4'e indir. ≈0,5 gün.

Toplam ≈2–2,5 gün + kısmi yeniden render (c0 başı, c1 ≈290–325 sn, c2 ≈360–545 sn). Sonra aynı ölçümlerle gerileme turu yapılmalı. Hedef: Y1–Y3 ve Y5 kapalı; her 10 sn penceresinde medyan ≥0,5; beyan ↔ gerçekleşen kapısı 0 ihlal.
