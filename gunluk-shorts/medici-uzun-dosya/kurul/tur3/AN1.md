# AN1 — TUR 3 · Animasyon ve kurgu / ANİMASYON YÖNETMENİ (hareket fiziği, kamera, geçiş zanaati) — Medici Parça 1 v3

## 1. Karar
**ONAY — 9,0 / 10.** Tur 1'de 6,5, tur 2'de 7,5 vermiştim; eşik ≥9.

| Başlık | Tur 2 | Tur 3 | Gerekçe |
|---|---:|---:|---|
| Geçiş dili | 8,5 | 9,0 | Aynı kartta kesme kalmadı. Işık geçişi 13'ten 4'e indi ve yıldız parlaması kalktı. 368,8 sn'de tek bir ölü bağlantı var (Y-N1). |
| Kamera (ölçülen) | 7,5 | 9,0 | Açılışta ve 3 haritada beyan edilen kamera artık uygulanıyor. Hızlı panlarda yön bulanıklığı ölçülüyor. #63 haritası yarı durağan. |
| Figür ve nesne animasyonu | 6,0 | 8,5 | Hançer kalktı. Hazırlık, oturma ve göz kırpmayı videoda gördüm. Yakın plan eller katı kayıyor; florin yağmurunda bulanıklık yok. |
| "Akan ve çok animasyon" talebi | 8,0 | 9,5 | Sessiz süre %9,6'dan %2,1'e indi; ≥3 sn'lik sessiz koşu kalmadı. Bölüm medyanları dengeli: c0 1,94, c1 1,40, c2 1,30. |
| Ölü/donuk kare | 7,5 | 9,0 | Açılış artık hareketli. 367,9–369,3 sn'de ≈1,4 sn ölü bağlantı ve iki kesme girişinde 1'er karelik duruş kaldı. |
| 24 fps + deklanşör | 7,5 | 8,5 | Kamerada ve büyük alanda 180° bulanıklık çalışıyor. Küçük hızlı nesnelerde (Y7) çalışmıyor. |

**Özet.** Tur 2'de ONAY için koyduğum dört koşulun dördü de karşılandı: hançer, beyan edilen kamera, aynı kartta kesme, figür oyunculuğu. Kalan dört iş engelleyici değil: Y7, #63 sonu ve #64 başı, yakın plan ellere oturma, iki kesme girişi. Bunlar bir sonraki render'a ya da P2'nin motor varsayılanlarına girebilir.

**Bir ölçüm hatamı kabul ediyorum (ayrıntı §2.1).** Tur 2'deki "4 harita hareketsiz" bulgum #69 ve büyük olasılıkla #51 için ölçüm artefaktıydı; ENG-D bu noktada haklıydı.

## 2. Ne gördüm / neye dayandım
**Sınır:** videoyu OYNATAMADIM, sesi DUYAMADIM. Kare dizileri, kare başına ölçümler ve kod okumasıyla değerlendirdim.

- **Okuduklarım:**
  - `kurul/KURUL_BRIFI_P1_TUR3.md`; `kurul/KURUL.md` ("Tur 2 — tam kurul sonucu", "v3 düzeltme planı");
  - `kurul/duzeltme_tur2/ENG-C.md` (§0, §2, §12) ve `ENG-D.md` (§0–1.8, §7);
  - `SCN-1.md` ve `SCN-2.md` (AN1 satırları);
  - `out_p1/qa_flow_v3.txt` (19 GEÇTİ, 2 UYARI);
  - `out_p1/uretim_v3.log` (14.437 kare, 601,54 sn, kare hatası 0);
  - `out_p1/kurul/gecis_light.png`, `gecis_kesme_10.png`;
  - `out_p1/duzeltme/tur2/ENG-D/01c`, `01d`, `08`; `ENG-C/g2_*`;
  - kod: `cilt_anim.py` (`blink_eye`, `BLINK`/`ACT_V2`/`FOLLOW`, `actor`), `cilt_oda.py:1150–1200`, `anim.py` (`blink`, `_blink_times`), `c2_kinds.py:1278`, `scenes_c2.py:184–192`.
- **Kendi ölçümlerim (v3).** Scratch dizini: `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/an1v3/`.
  1. **Kare farkı:** her kare için (320×180 gri) → `pf_v3.json`. Tur 1/2 ile aynı yöntem.
  2. **Kamera:** 8 kare/sn zincirleme LK + RANSAC, iki maskeyle:
     - tam kare → `chain_v3.json`, `chainrep.txt`;
     - yalnız merkez %60×%65 → `chainC_v3.json`, `chainrepC2.txt`. Bu sürümde geçiş kareleri hariç tutuldu.
  3. **Hız ölçümleri:** Farneback optik akışı (florin yağmuru, yakın plan eller) ve yön keskinliği oranı Gx/Gy (bulanıklık testi).
  4. **Kenar taraması:** 2 kare/sn (`edges_v3.json`).
  5. **Göz kırpma takibi:** şablon izleme ile, kare kare (`cossa_blink_zoom.png`).
  6. **Kare şeritleri:** `pope_v3.png`, `pope_point_strip.png`, `coin302_v3.png`, `coins389_v3.png`, `lowcuts_v3.png`, `masa_v3.png`, `open534_v3.png`, `itiraz_v3.png`, `edge545_v3.png`, `yakin_v3.png`, `maps_grid.jpg`.
- **Metrik notu:** v3'te gren her karede yeniden tohumlanıyor ve kâğıt dokusu dünyaya kilitli. Ama tam durağan anlarda ölçülen taban yükselmedi: bitiş ekranında en düşük kare farkı v2'de 0,14, v3'te 0,10; #63'ün donuk sonunda 0,01. Bu yüzden v2 ile ham karşılaştırma adil.

| Ölçü | v2 | v3 |
|---|---:|---:|
| Kare farkı medyanı: bütün / çekim içi | 0,83 / 0,80 | **1,36 / 1,32** |
| Bölüm medyanı c0 / c1 / c2 | 1,69 / 0,98 / 0,67 | **1,94 / 1,40 / 1,30** |
| Sessiz süre (0,5 sn medyanı <0,25) | 57,3 sn (%9,6) | **12,6 sn (%2,1)** |
| ≥1,5 sn / ≥3 sn sessiz koşu | 11 / 1 | **2 / 0** |
| 10 sn'lik pencere medyanı <0,6 | 17/59 | **2/60** |
| Kayan 10 sn pencere <0,5 (başlangıç sn'si) | 10 aralık | 3 aralık: 359, 541–546, 588–591 (sonuncusu bitiş ekranı) |
| Geçişlerin enerji payı | %24 | %22 |
| Sert kesme / ışık geçişi / geçiş süresi σ | 39 / 13 / 0,38 sn | 37 / **4** / 0,33 sn |

### 2.1 ENG-D ile harita ölçümü ayrışması (ENG-D §7): sonuç
- **Tam kare LK, v3:** doku artık dünyaya kilitli olmasına rağmen #70 haritası (406,0 sn) hâlâ hareketsiz ölçülüyor: ölçek −%0,6, kayma −19 px.
- **Merkez maskeli LK, aynı çekim:** ölçek **+%11,5**, kayma **−271 / +93 px**.
- **Gözle (`maps_grid.jpg`):** 406,6 → 412,4 sn arasında FLORANSA etiketi ≈(−246, +93) px kayıyor. Bu, merkez ölçümüyle örtüşüyor.
- **Sonuç:**
  - Tur 2 ölçümümü çarpıtan asıl şey ekrana sabit **harita çerçeve frizi** (kenardaki baklavalı şerit) ve HUD'du; kâğıt dokusu tek başına değil. En güçlü köşeler bu sabit öğelerde toplanıyor, RANSAC da onları "kamera" sanıyor.
  - Bu yüzden tur 2'deki "#69 hareketsiz" bulgum yanlıştı; ENG-D'nin v2 karesi (01c: FLORANSA 139 px kayıyor) bunu gösteriyor. #51 için v2 dosyası artık olmadığından yeniden ölçemedim; ENG-D'nin fark testine güveniyorum.
  - Tur 2 bulgusu şu çekimlerde doğruydu:
    - #0 kapak yankısı: tür kamerayı okumuyordu;
    - #55: beyan ters yöndeydi (ENG-D);
    - #62, şimdi #63: "yarı durağan" (ENG-D de böyle tanımladı).
  - Çerçeveli görüntülerde (harita, belge kartı) kapının fark testi benim tam kare LK'mden daha güvenilir. Ölçümümü bundan sonra merkez maskesiyle yapıyorum.

## 3. Tur 2 maddelerimin durumu

| Madde | Durum | Kanıt (v3) |
|---|---|---|
| **Y1** Papanın hançeri (engelleyiciydi) | **KAPANDI** | 471,8–475,4 sn (`pope_v3.png`). Hiçbir karede bıçak yok. Papa kurşun mühürlü bullayı kalçadan (471,8) omuz hizasına (472,6) kaldırıp Giovanni'ye uzatıyor (≈x 1150–1230, y 230–380), Giovanni eğiliyor. Yüz ve taç açık. "AFOROZ TEHDİDİ" etiketi (x≈644–1274, y≈96–184) kolun üstünde. |
| **Y2** Beyan edilen kamera (açılış + 4 harita) | **KAPANDI** (#63 kısmen; #69 benim ölçüm hatamdı, §2.1) | Ölçümler aşağıda. "Beyan ↔ gerçekleşen kamera" kapısı var: 43 çekim, 0 ihlal; #63 UYARI. |
| **Y3** Aynı kartta kesme (427,6 / 480,2 / 482,2) | **KAPANDI** | Ağ ve anahtar çekimleri iki sürekli "masa" çekimi oldu: #72 (416,0–431,6) ve #83 (475,8–486,4). `masa_v3.png`: tüy kalem yazıyor, el anahtarı bırakıyor, çubuk büyüyor; medyanlar 1,87 ve 3,05 (v2'de 0,17–0,23). "Aynı görüntü kesmesi" kapısı: 37 kesmede 0. Benim en düşük kesme farkım 18,1 (165,9 sn: farklı kartlar). |
| **Y4** Sessiz cepler | **BÜYÜK ÖLÇÜDE KAPANDI** | Sayılar aşağıda. Kalan: #63 harita (0,47; donuk biten son, Y-N1) ve ölüm döşeği konuşması #93 (545,2–552,4; 0,40; itme +%2,5 / 6,4 sn). #93 ağır sahne olduğu için kabul edilebilir. |
| **Y5** Yarım sikke (302,29–302,62) | **KAPANDI** | `coin302_v3.png`: sikke ilk kareden tam, yarım kenar ve dikiş yok. |
| **Y6** Ölü açılışlar (423,9 / 534,5) | **KAPANDI** (adı geçen iki yerde) | 423,9: çekimler birleşti. 534,5: Machiavelli ve Cavalcanti sayfaları ile levhaları ilk karede hazır (`open534_v3.png`); yazı "kalemden" sözcüğünde akıyor. Benzer bir yer 368,8'de kaldı (Y-N1). |
| **Y7** Küçük hızlı nesnelerde deklanşör | **AÇIK** (v3 planında yoktu) | 389,5–391,5 sn florin yağmuru: hız p99 16–18 px/kare (en çok ≈21), sikkeler keskin (`coins389_v3.png`). `anim.hint_speed` yalnız `c2_kinds.py:1278`'de, 4 px/kare ile çağrılıyor; tetik eşiği 8. |
| **Y8** Işık patlaması (13×) | **KAPANDI** | 4 kullanım: #1 (3,7), #50 (285,2), #60 (342,8), #100 (584,8). Yıldız ışınları yok; yumuşak yaldız parlaması + zımba halkaları (`gecis_light.png`). |
| **Y9** İTİRAZ damgası papanın yüzünde | **KAPANDI** | 462,4 sn: damga ≈x 330–705, y 360–510; papa ≈x 810–1380 (`itiraz_v3.png`). |
| **Y10** Set kenarı (545,5) | **KAPANDI** | Sol kenarda artık oda dekoru var (`edge545_v3.png`). Bütün videoda kenar taramasında 1 işaret çıktı (33,0 sn); kareye baktım, bu lacivert duvar halısı, gerçek kenar değil. |
| **Y11** Kesmede 1 karelik duruş | **KISMEN** | v2'deki 416,0 / 480,2 / 482,25 / 502,8 duruşları gitti. Kalanlar: 43,9 (#8, kesme sonrası ilk adım 0,07), 575,5 (#98 `c2_yakin`, 0,11), 355,8 (#62, yavaş kalkış 0,21). Yeni bir kesme öncesi donukluk da var: 368,8 (Y-N1). |
| **Y12** Yön uyarısı #15 | **KABUL** | Gerekçesi `yonetmen_c0.md`'de yazılı (SCN-1). |
| **E3 / kontrol 12** Figür oyunculuğu: hazırlık, oturma, göz kırpma | **KAPANDI** (kit düzeyinde, videoda doğrulandı) | Ayrıntı aşağıda. Kitte `ACT_V2`, `BLINK` ve `FOLLOW` açık, `LOOK_AUTO` açık. Baş çevirmeyi videoda ayrıca ölçmedim (ENG-C `g2_bakis_look.jpg`). |
| E1 (c2 kart vadisi) | **KAPANDI** | c2 medyanı 0,35 (v1) → 0,67 (v2) → 1,30 (v3). |
| E2 (kamera tekdüzeliği) | **KAPANDI** | Gerçekleşen hareketler çeşitli: pan, truck, tilt, crane, itme, çekme; masa çekimlerinde uzun kayma (#72: −444 px / 14,5 sn). |
| E4 (24 fps, deklanşör) | **KISMEN** | Kamera/alan bulanıklığı var; küçük nesnede yok (Y7). |
| E6 (Machiavelli mizanseni) | **KISMEN, kabul** | #92 tek kullanım, pencere ışığı eklenmiş (0,70). Yerleşim aynı ama artık sessiz cep değil. |
| E7 (geçişte çift kare) | **KAPANDI** | Neredeyse özdeş ardışık kareler yalnız iki yerde: 25,42–25,46 (mum geçişinin kasıtlı karanlık anı) ve #63 haritası (361,17 / 364,0 / 368,46–368,83 → Y-N1). |
| E8, E9 | **KAPANDI** | — |
| Motor önerisi 1 (ölçülü hareket kapısı) | **KAPANDI** | "Beyan ↔ gerçekleşen kamera" ve "Aynı görüntü kesmesi" kapıları var. |
| Motor önerisi 2 (`anim.py`) | **KAPANDI** | Figür kitine bağlandı. |
| Motor önerisi 3 (seçici deklanşör) | **KISMEN** | Y7. |

**Y2 ölçümleri** (merkez maskeli LK, geçişler hariç):

| Çekim | Gerçekleşen hareket | Değerlendirme |
|---|---|---|
| #0 kapak yankısı | Kilit ve belge bölgesinde 0,3→2,9 sn +%5,9 itme; yazı ekrana sabit, bu doğal. Medyan 0,14 → 0,45. Işık süpürmesi ve kilit sarsıntısı var. | Uygulanıyor |
| #51 (291,8) | +%34, ≈95 px/sn | Uygulanıyor |
| #55 (313,0) | +%41 | Uygulanıyor |
| #70 (406,0) | +%11,5, −271 / +93 px | Uygulanıyor |
| #63 (361,1) | −%2,8 ve 16 px / 7,3 sn | Kısmen (kadraj koruması, kapı UYARI'sıyla aynı) |

**Y4 cepleri (v2 → v3 çekim içi medyan):**

| Çekim | v2 | v3 | Not |
|---|---:|---:|---|
| #56 `c1_kose` | 0,24 | 0,56 | itme +%5,9 |
| #44 `p1_doc` | 0,26 | 0,54 | itme +%5,9; Signoria'da okuma eklendi |
| #92 Machiavelli | 0,26 | 0,70 | — |
| Anahtar üçlüsü | 0,17 | 3,05 | tek masa çekimi oldu |
| Ağ çifti | 0,23 | 1,87 | tek masa çekimi oldu |

**Figür oyunculuğu, videodaki kanıt:**
- **Papanın işareti (`pope_point_strip.png`):** el önce geri/aşağı çekiliyor (461,55–461,97, hazırlık). Sonra 462,05–462,38'de 0,33 sn'de uzanıyor. 462,47–462,72'de hafif aşıp oturuyor.
- **Göz kırpma (`cossa_blink_zoom.png`):** Cossa'nın gözü 433,50–433,54'te iki kare kapalı (ince kapak çizgisi), 433,58'de açık. İkinci kırpma 437,96'da başlıyor.

## 4. Gerilemeler ve yeni sorunlar
Engelleyici yok.

**Y-N1 — KÜÇÜK-ÖNEMLİ: 367,9–369,3 sn ölü bağlantı (#63 harita → #64 `c2_nolist`).**
- #63'te beyan edilen çekme kadraj korumasına takılıyor ve son ≈1 sn hareket söndükçe kare donuyor: kare farkı 0,12 → 0,01. 368,46–368,83 arasındaki 10 kare neredeyse özdeş.
- Kesmeden sonra 368,88'de boş parşömen var; "BORÇ" ancak ≈369,3'te beliriyor (`lowcuts_v3.png`, 3. satır).
- Sonuç: ≈1,4 sn hareketsiz ve içeriksiz an, üstelik "hareket üstünde kesme" kuralı bu kesmede bozuluyor.
- **Ne yapılmalı:** ENG-D'nin önerisi gibi `cam=("pull",)` beyanını kaldır. Yerine rota merkezine doğru yavaş bir itme ver (≥%1/sn) ve son ana kadar sür; kazanç sikkelerinin salınımı da kesmeye kadar sürsün. #64'te ilk kart (BORÇ) ilk karede hazır olsun ya da `lead` ile doğsun.

**Y-N2 — KÜÇÜK: Yakın plan ellerde katı kayma.** Ölçüm Farneback ile, `yakin_v3.png`.
- **#62 kese (355,8–361,1):** el 61 px/kare tepe hızından sonra sabit 27 px/kare gidiyor ve ≈357,7'de iki karede duruyor (27 → 4 px/kare); oturma yok. İkinci el düzgün bir çan eğrisiyle (ease) hareket ediyor.
- **#81 mitra (469,9–471,6):** işaret eden el çan eğrisiyle giriyor, oturmadan duruyor. Mitrayı tutan eller 1,7 sn hareketsiz (kare farkı 0,20, parçanın en düşüğü).
- Bilekte ve parmakta dönüş yok; açıklayıcı video (explainer) "kesik el" hissi veriyor.
- **Ne yapılmalı:** el varışlarına `anim.settle` (%6–10 aşma), yolda 5–10° bilek dönüşü; #81'e hafif itme ya da odak kaydırma (rack).

**Y-N3 — KÜÇÜK: Kesme girişinde 1 karelik duruş (Y11'in kalanı).** 43,9 (`c0_belge`, "hand" kamerası) ve 575,5 (`c2_yakin` kendi kamerası; ENG-D de yazdı). `c2_yakin` ve `c0_belge` kameralarına da `CUT_SLOPE` uygulanmalı.

**Y7 (devam) — KÜÇÜK-ÖNEMLİ:** florin yağmuru ve damga düşüşü gibi küçük hızlı nesneler çizen türler `anim.hint_speed(cx, v)` çağırmalı; ≈2 saatlik iş.

**ENG-D'nin ikinci şüphesi (CUT_SLOPE = 1, iki ucu kesme olan hızlı pan) — ölçüm olarak sorun yok.**
- #65 (373,4–379,2) baştan sona ≈13 px/kare (≈320 px/sn) sabit hızla gidiyor; kesmeye tam hızda girip tam hızda çıkıyor.
- Yön bulanıklığı var: Gx/Gy 0,49 (376,0 sn) ve 0,73 (377,5 sn). Durağan ya da yavaş karelerde bu oran 0,85–1,02 (351,6 sonrası, 382,0, 23,0 sn). Yani deklanşör bu panda devrede.
- "Ani kalkış" algısını oynatmadan yargılayamam. Gerekirse yalnız ≥250 px/sn panlarda `CUT_SLOPE` 0,8.

**Not, sorun değil:** haritalarda kamera artık ekrana sabit çerçeve frizinin içinde geziyor ("pencere" etkisi). Üslup olarak kabul edilebilir. Tam kare ölçümleri de bu yüzden yanılıyor (§2.1).

## 5. Kullanıcının sorusu: "Bu çizim tarzı ucuz mu, yapay zekâ gibi mi?"
**Değişti, olumlu yönde.**
- Tur 2'de "ucuz" okumasının hareket kaynaklı nedenleri kalktı: durağan kapak yankısı, hareketsiz kart ve haritalar, aynı kartta kesmeler, boş açılışlar, kukla oyunculuk. c2'deki kartların yerini tüy kalemin yazdığı, elin anahtar bıraktığı masa ve defter dünyası aldı. Figürler artık hazırlanıp, oturup, göz kırpıyor.
- YZ izlenimi hâlâ yok.
- Bu mercekten en "şablon" okunan iki şey kaldı: yakın plan ara planlarda katı kayan düz eller (355,8; 469,9) ve kalan birkaç parşömen kartı (165,9 kese ve sikke; 368,8 BORÇ/FAİZ; 444,9 yol ayrımı silueti).

## 6. En emin olmadığım nokta
1. **#51'in v2'deki durumu:** v2 dosyası silindiği için yeniden ölçemedim. "v2'de de hareket ediyordu" sonucu ENG-D'nin fark testine ve 01c karesine dayanıyor; #69 için bunu kendi v3 ölçümümle ve görsel kanıtla doğruladım.
2. **Göz kırpmanın yaygınlığı:** iki kırpmayı (Cossa) videoda gördüm. Papanın 6,8 sn'lik ekran süresinde ise kırpma görmedim (460,45–463,24 ve 471,75–475,79, kare kare).
   - Zamanlayıcı her çekimde 3–6 sn'lik tohumlu aralıkla başladığı için kısa çekimlerde bu olası.
   - Ama "her figür kırpıyor" diyemem: kod yalnız `cf=None` olan ve başı ≥12 px figürlerde kırptırıyor; siluetler kırpmıyor.
3. **Algı:** hızlı panların kesmede tam hızla girişini ve Y-N1'deki ≈1,4 sn'lik ölü anın izleyicide ne kadar fark edildiğini oynatmadan bilemem. Sayılar küçük, ama ikisi de kesme anında.
