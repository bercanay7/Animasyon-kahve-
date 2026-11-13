# AN2 — Animasyon ve kurgu · KURGU / RİTİM UZMANI · Medici Parça 1 (TUR 1)

Üye: AN2 (kurgu/ritim mercek). Tarih: 4 Kasım 2026. Kapsam: `out_p1/medici_P1.mp4` (601,9 sn, 24 fps) + kanıt paketi + motor dosyaları. Başka üyenin raporunu görmedim.

## 1. Karar

**RED — 7,0 / 10** (eşik ≥9). Alan puanıdır, iyi niyet payı yok.

Tek cümle: **yerel kurgu zanaati (geçiş eşleşmeleri, anlatıyla senkron, bölüm kapıları) yüksek; ama 10 dakikalık eğri bozuk: ilk 7 dakika çeşitli, 404–590 s arası (parçanın son %31'i) "parşömen üstüne kart" modunda donuyor, kamera 182 sn boyunca hep aynı itme, geçişlerin hepsi aynı 0,9 sn'lik darbe, kesme yok.** Kapıların 11/11 GEÇTİ olması bu vadiyi yakalamıyor, çünkü kapılar eşik denetliyor, çeşitlilik denetlemiyor.

Engelleyici: 1 madde (E1). Önemli: 5. Küçük: 4.

## 2. Ne gördüm / neye dayandım

**Sınır (açık):** Videoyu oynatamadım, sesi duyamadım. Hareket ölçümü 0,5 sn aralıklı iki kare farkıdır (240×135 gri): kamera kayması, küçük "pop-in" ve geçişi ayıramaz; sık kesen bir pasajı "az hareket" gösterebilir, ince animasyonu göstermez. "Dünya / kart" sınıfını 95 çekimin orta karesine bakarak elle verdim (480 px küçük resimlerden; `story_1…4` benzeri kendi scratch'imde). "Kapsama" göstergesi (arka plandan farklı piksel oranı) kaba bir vekildir, mutlak değil göreli okunmalı. Sisifos'u yalnız koddan saydım (`sisifos/lib/act*.js`), videosunu izlemedim.

**Kaynaklar:** `qa_flow_ozet.txt` çekim tablosu (95 satır = 92 gerçek çekim + 3 kart: `fresco_title`, `chapter_card`, `outro`), `hareket.json` (1203 örnek), `out_p1/timeline.json` (85 cümle, 959 sözcük, sözcük zamanları), `medici_P1_tr.srt`, `sfx_gecis.json` (86 geçiş efekti), `genel_01…04.png`, `gecis_*.png`, `tam_*.png`; ayrıca videodan kendi çıkardığım: 95 çekim ortası kare, 7 zaman şeridi (448 s tam çözünürlük dahil: 437–449, 458–469, 470–482, 345–353, 96–109, 588–601, 0–21 s). Motor: `YONETMENLIK_REHBERI.md`, `notlar_yonetmen_motoru.md`, `qa_flow.py` (static_analysis), `cilt_fx.norm_tr`, `yonetmen_c2.md`.

### 2.1 Çekim süresi dağılımı (n=95)

| ölçü | değer |
|---|---|
| ortalama / medyan | 6,34 / 5,80 sn |
| p10 / p25 / p75 / p90 / p95 | 3,0 / 4,3 / 7,7 / 9,3 / 13,3 sn |
| min / maks | 2,2 (#34) / 16,3 (#55) sn |
| değişim katsayısı | 0,47 |
| bölüm ortalamaları | c0 6,3 · c1 6,2 · c2 6,5 (düz) |
| 1. gecikmeli özilinti | **0,06** (ardışık çekim uzunlukları birbirinden bağımsız: "tümcelenmiş" ritim yok) |
| 4–8 sn bandında kalan | 56/95 (%59) |

Histogram (sn: adet): 2–3: 9 · 3–4: 11 · 4–5: 12 · 5–6: 18 · 6–8: 26 · 8–10: 10 · 10–12: 0 · 12–14: 6 · 14–17: 3. Yani 10–12 sn boşluğu var; çekimler ya "cümle boyu" (4–9 sn) ya "uzun alıntı" (12–16 sn). 2 sn altı çekim hiç yok; `montage=True` P1'de **0 kez** kullanıldı. Rehberin kendi hedefi "dakikada 10–14 çekim"; gerçek **9,5/dk** (dakika dakika: 11, 9, 9, 12, 9, 10, 10, **6**, 11, 8).

### 2.2 Anlatıyla ilişki

- Anlatı duvar duvara: 520,8 sn konuşma / 594,9 sn (%87,5); konuşma içi hız **1,84 sözcük/sn**, 30 sn pencerelerde 1,30–1,77 (düz). Cümle arası boşluk medyan 0,81 sn (bölüm içi en uzun 1,36 sn). Görüntünün tek başına konuştuğu an yok (başlık kartları hariç).
- **1 çekim ≈ 1 cümle:** 79 çekim tam 1 cümleye değiyor, 11 çekim 2, 1 çekim 3, 1 çekim 4 cümleye; 3 kart cümlesiz. Tek cümleli çekimlerde çekim/cümle süre oranı medyan 1,06 (korelasyon 0,33: uzun cümleler 2 çekime bölünüyor).
- **Kesme anı = cümle nefesi:** 94 kesmeden 69'u cümle başlangıcının −0,22…+0,03 sn'si içinde (ortalama −0,11 sn: görüntü sesten ≈0,1 sn önce yerleşiyor); yalnız 6'sı konuşulan bir sözcüğün içine düşüyor. 25 kesme cümle ortasında ve hepsi 8–12 sn'lik uzun cümlelerin içinde. Geçiş (0,9 sn) bu 0,88 sn'lik ortalama boşluğa oturtulmuş. Bu, senkron için mükemmel; ritim için tek biçimli (hiçbir yerde görüntü cümleyi 0,6–1 sn önceden kesmiyor, hiçbir yerde cümle bitince 1+ sn görüntüde kalmıyor).

### 2.3 Geçişler (94 geçiş)

| tür | adet | link |
|---|---|---|
| zoomthru 20 · slide 20 · sayfa 11 · carry 10 · yikama 10 · iris 7 · light 7 · candle 4 · dip 1 | 90 | scale 21, dir 19, material 17, light 11, carry 10, shape 7, color 5, cam 3, audio 1 |
| **sert kesme** | **4** (#13, #22, #28, #57) | cam/audio/ölçek |

- **Süre: 86 geçiş 0,9 sn, 4 geçiş 1,0 sn.** Yani tek tempo. (`norm_tr` yeni geçişlerde ≤1,0 sn'ye kırpıyor.)
- Geçişler toplam **81 sn = ekran süresinin %13,5'i**; <3,5 sn'lik 15 çekimde süresinin **%33'ü** geçişte. Temiz görünüm süresi (çekim − 0,9) medyan 4,9 sn ama 8 çekimde <2,0 sn (#5, #6, #9, #17, #30, #34, #58, #89), en kötüsü #34: 1,3 sn.
- 10 sn'lik pencerelerin en yoğunu: **25–35 s %36 geçiş** (sayfa → zoomthru → zoomthru: 28,6–34,6 s'de üç geçiş); 183–193, 196–206, 106–116, 48–58, 503–513 s %27–28.
- Geçiş tepe enerjisi (0,5 sn kare farkı): medyan 38, çekim içi medyan 3,25: **12 kat**. Tür başına tepe hemen aynı (zoomthru 36, slide 42, sayfa 38, carry 38, yikama 33, iris 39, light 33; yalnız candle 84, dip 123 kararıyor). Yani 9 farklı görünüm, tek enerji.
- Her geçişin kendi SFX'i var (`sfx_gecis.json`: 86 cue, −21…−24 dB): ses de ≈7 sn periyotla atıyor (ses üyesi için not).
- 7 geçiş aynı mekân/aynı tür çekimler arasında (#2, #3, #4, #33, #42, #58, #89). Orada sert kesme doğal olurdu.

### 2.4 Kamera

78 itme (%6–8) + 4 geri çekme + 3 pan + 2 crane + 5 anahtar kareli + 3 kamerasız kart = 95. İtme oranı çekim süresine bakmadan %6/7/8 (41 çekim %7); sonuç hız farkı **9,9 kat**: 2,2–2,6 sn'lik çekimde %2,3–3,6/sn, 12,2–16,3 sn'lik çekimde **%0,37–0,57/sn** (kenarda ≈4–5 px/sn kayma: algılanmaz). En uzun itme dizisi **26 çekim: #62–#87 (375,8–557,5 s = 181,7 sn)**; bu aralıkta pan/crane/pull/rack yok. "Kamera hareket yeterliliği" kapısı toplam %6'ya bakıyor, hıza bakmıyor: 16 sn'de %6 ve 2 sn'de %6 aynı sayılıyor.

### 2.5 Görsel sınıf akışı (elle, orta kare)

Dünya (W: tam sahne; oda/şehir/pano/skyline/alay) 31 çekim = 175,7 sn (%29); kart/harita/belge/figür-parşömen (K+M+D+F) 56 çekim; başlık/koyu kart (T) 8.

| dakika | çekim | ASL sn | W süre% | çekim içi hareket medyanı | kapsama | itme dizisi |
|---|---|---|---|---|---|---|
| 0 | 11 | 5,9 | 67 | 11,8 | 0,75 | |
| 1 | 9 | 6,3 | 41 | 6,7 | 0,55 | |
| 2 | 9 | 7,0 | 12 | 2,4 | 0,63 | |
| 3 | 12 | 4,7 | 54 | 6,5 | 0,50 | veba/Ciompi |
| 4 | 9 | 6,9 | 50 | 2,3 | 0,54 | |
| 5 | 10 | 6,2 | 41 | 4,1 | 0,58 | |
| 6 | 10 | 5,6 | 19 | 2,3 | 0,51 | |
| **7** | **6** | **10,2** | **0** | **1,1** | **0,36** | 6/6 itme |
| **8** | 11 | 5,7 | **0** | **1,8** | **0,36** | 11/11 itme |
| 9 | 8 | 7,2 | 9 | 2,7 | 0,52 | |

- **403,6–589,5 s = 185,9 sn arasında tek "dünya" çekimi yok.** 403,6–523,2 s'de (#67–#83) **17 ardışık kart/harita/defter/infografik çekimi (119,6 sn)**.
- Kapsama (kareyi dolduran öğe oranı) c0 0,70 → c1 0,53 → c2 0,47: parça ilerledikçe kare boşalıyor. 7.–8. dakika 0,36.
- Hareket eğrisi: durgunluk kapısı geçti (en düşük örnek 0,41), ama örneklerin **%42'si ≤3, %32'si ≤2**. 7. dakikada %83'ü ≤3 (ilk dakikada %4). En uzun ≤2 koşusu 458–469 s (11 sn), ≤3 koşuları: 154,5–167 s (12,5 sn), 437,5–449 s (11,5 sn), 458–469 s (11 sn), 547–556,5 s (9,5 sn). 404–590 s aralığında örneklerin %67'si ≤3 (parçanın geri kalanında %30).
- Önemli not: bu çekimler "ölü" değil. #72, #74, #75 şeritlerinde (437–449, 458–469, 470–482 s) her 1,5–2 sn'de yeni öğe beliriyor (çip, sikke yağmuru, damga, taç, mum). Sorun olay sıklığı değil, **olayın hep aynı biçimde olması**: boş parşömen üstünde çip → damga → siluet.

### 2.6 Açılışın ilk 90 sn'si (c0)

16 çekim / 101 sn: 3,8 · 9,6 · 6,7 · 6,1 · 3,4 · 2,6 · 2,4 · 14,8 · 4,9 · 2,4 · 8,2 · 4,4 · 8,7 · 8,6 · 5,8 · 8,8. 30 sn'lik pencerelerde çekim sayısı 6, 5, 4 (60–90 s'de yavaşlıyor: #12 gerekçe kartı 8,7 sn, çekim içi hareket medyanı 1,3; ardından #13 Uffizi kuyruğu 8,6 sn).
- Güçlü: **26–55 s** (3,4 / 2,6 / 2,4 / 14,8 / 4,9 / 2,4: takvim "97 gün" → imza → belgeye iniş → 14,8 sn'lik belge çekimi → carry ile belge masaya dönüyor). Parçanın en iyi kurgu pasajı; kalıp bu.
- Zayıf: 0–34 s'nin 6 çekiminden 5'i **aynı 1743 odası** (#1–#4 ardışık; #6) ve ilk 13 sn = 3,8 sn skyline + 9,6 sn yatak odası (çekim içi tek yeni öğe ≈7 sn'de "ANNA MARIA LUISA" çipi; sonrası arma/belge kamerayla giriyor). Kanal verisi: kayıp ilk 10–15 sn'de. Kapıların "Tür tekrarı" kontrolü `oda` ile `p1_oda`'yı farklı `kind` sayıp geçiriyor.
- Bölüm kapısı c0→c1 (92–108 s): sikkenin yıl yıl dönmesi (1396 → 1252), fresk, MEDİCİ, sikke yeni sahnede dönerek açılıyor: iyi.

## 3. Sıralı düzeltme listesi

**E1 — ENGELLEYİCİ · 403,6–589,5 s (#67–#91) "kart vadisi".** Kullanıcının pazarlıksız talebi ("olabildiğince akan ve çok animasyon") parçanın son üçte birinde, üstelik içeriğin en yüklü yerinde (Cossa borcu, çifte kayıt tezi, kadastro, Machiavelli/Cavalcanti) karşılanmıyor. Yapılacak, ölçülebilir hedef: **her 60 sn pencerede ≥1 "dünya" çekimi; üst üste ≤4 kart; 403–590 s içinde ≥4 dünya/figür çekimi; 7.–8. dakika kapsaması ≥0,50.** Somut öneri (mevcut motor türleriyle, yeni tür gerekmez):
  - **#72 (436,6, 13,3 sn):** ikiye böl. 436,7 "Giovanni … borç verdi" madalya+siluet kartı 7–8 sn; **445,3 "1415'te Konstanz Konsili onu indirdi"** → `oda` (#63 vicdan komitesi masa/sandalye setinin soğuk tonlusu) 5 sn, pan ya da pull (itme değil).
  - **#75 (469,8, 12,6 sn, tek cümle 11,4 sn):** 475,4 "Martinus … mitrayı … aforozla tehdit" noktasında kes; ikinci yarı taht odası (#2'nin boş tahtı seti) + papa silueti.
  - **#78–#79 (491,3–504,7):** iki kart (2.077 hane ızgarası, %29,8 çubuğu) arasına 4–5 sn'lik `sehir` çekimi (hane hane kapı/memur siluetleri; #30–#33 sokak setinin sıcak tonlusu) ya da iki kartı tek çekimde kamera hareketiyle birleştir.
  - **#86, #88, #89 (539,5–544,4 ve 557,5–573,7):** toplam 21 sn okunacak şey olmayan sayfa (boş kart; dalgalı çizgili iki sayfa); #87 ve #91 de #44'ün aynı masa seti. #88–#89'u bir `oda` çekimine (yazan figür, #55'in raf/masa seti ya da yazıcı odası) çevir; sayfa kartları yalnız damga/vuruş anında kalsın.
  - 403–523 s arasında en az 2 sert kesme ve 1 "iki cümlelik tutma" (bkz. Ö2, Ö3) ile eğri nefes alsın. Harita üçlüsü (#59, #61, #68; 358–417 s) için K3'e bak.
  - Gerekçe: aralık parçanın %67–%98'ine denk geliyor ve parçanın ana olay örgüsünü (Cossa, çifte kayıt, kadastro, 1429, Cosimo kapısı) taşıyor; görüntü en az bilgiyi en önemli yerde veriyor. Bunu kapatmadan "akan" talebi karşılanmış sayılmaz.

**Ö1 — ÖNEMLİ · Kamera: 375,8–557,5 s 26 ardışık itme + hız normalizasyonu.** ≥12 sn'lik itmeli 8 çekimde (#7, #25, #44, #55, #72, #74, #75, #87) hız %0,37–0,57/sn. Yap: (a) ≥8 sn'lik çekimlerde hız bazlı kamera (≥%1,0/sn: 13 sn'de %13 itme) ya da kamera türü değiştir (`pan r 120–200`, `pull 0.10`, `rack` sikke → siluet #72'de "Cossa adlı bir kilise adamı" sözcüğünde, anahtar kareli kamera çapaları #22/#88 gibi); (b) c2'de her 4 çekimde ≥1 itme-dışı hareket; hiçbir yerde ≤5 ardışık itme. Yön sözleşmesine (§1-6) uy: Giovanni/yükseliş sağa, Cossa'nın düşüşü (445 s sonrası) sola.

**Ö2 — ÖNEMLİ · Geçiş tek tempo, sert kesme yok (4/94).** Yap: tasarlı geçişi yalnız mekân/zaman/ölçek/bölüm değişiminde tut (hedef ≈%30–40, şimdi %96); gerisini söz/vuruş üstünde sert kesme (`tr=None`, `link="audio"` ya da `"cam"`). Kesmeye çevrilecek *giriş geçişleri* (aynı mekân/aynı set devamı): #3, #33, #42, #58, #89 kesin; #2 ve #4 isteğe bağlı (#4'te 1743 → 1737 zaman atlaması `candle`'a gerekçe verir, #2'de iris palle→taht); ayrıca c2'nin kart koşusundaki (#69–#83) geçişlerin yarısı (ör. #71, #77, #80, #82'ye girenler) ve #5→#6→#7 üçlüsünden #6'ya giren zoomthru (32,1 s). Süre çeşidi ekle: 0,25–0,4 sn "vuruş" (sayı/liste: kadastro, Strozzi), standart 0,9, 1,6–2,4 sn "uzun" (veba 184,6 s `yikama`, 1429 ölümü #84 `candle`, #92). 25–35 s pencere (sayfa → zoomthru → zoomthru, %36 geçişte) bu yüzden gevşetilir. Not: kesmeye dönen çekimlerde `lead` kalkar (yerel saat erken doğmaz); mutlak `at=` kullanan ovl'ler gözden geçirilmeli (notlar_yonetmen_motoru §3).

**Ö3 — ÖNEMLİ · 1 çekim = 1 cümle kilidi; hızlanma/yavaşlama yok.** (a) 2–3 yerde bilinçli **hızlı seri** (`montage=True`, sert kesmeli, 3–5 çekim, 1,2–2,0 sn): Peruzzi/Bardi çöküşü ("Peruzzi de Bardi de 1340'larda battı; … III. Edward'ın ödemediği borçlar", 164–173 s: #25'in ikinci yarısı + #26), kadastro sayı vuruşları (482–512 s: 22 yıl, 2.077 hane, %29,8, Strozzi 162.925); sonrasında 8–12 sn'lik nefes. (b) 2–3 yerde görüntü cümleyi **0,6–1,0 sn önceden** kessin (ifşa: "Fransızca" 41 s, "eski papa" 464 s, "hücreye" 589,5 s) ve 2–3 yerde cümle bitince **1+ sn** görüntüde kalsın. (c) Dakika başına çekim hedefi 9–13, tam bir dakika ≥14 (3. dakika 12 var; 4., 6., 7. dakikalar 9–10, 6). (d) 2 cümleyi tek çekimde tutmak yalnız duygusal vuruşta olsun; #55'te (331,2–347,6, 16,3 sn, 4 cümle) "bir masa ve bir defter" (333,8) sözcüğünde defter/masa yakın planına kes (maks. çekim ≤12 sn).

**Ö4 — ÖNEMLİ · Parça kapısı: son görüntüde bekleme yok.** Son cümle 594,88 sn'de bitiyor, `voice_chapters.json` c2 `gap_after` = 0,0; `outro` t0 = 594,9 ve yıkama hemen başlıyor (595,5 s karesinde yıkama sürüyor). "…bir hücreye kapatılacaktı" cümlesinin ardından kulenin hücre ışığıyla (594,3 s karesinde pencerede parıltı) **1,2–1,5 sn** sessiz/müzik-yalnız kalış ver, sonra outro. Maliyet düşük (yalnız #93 kuyruğu ve outro kayar). Kapı fikri (crane up kule → P2'nin ilk çekimi `skyline_dikey_p2` "kule") iyi.

**Ö5 — ÖNEMLİ · Kamera itmesi kenardaki yazıyı kırpıyor (kare içi).** 445–449 s (#72): "XXIII. JOHANNES" çipi (≈x 1435–1916, y 430–584 @1920×1080, 448 s karesi) sağ kenarda "XXIII. JOHANNE" olarak kesiliyor; "BALDASSARRE COSSA" çipinin sağ üst köşesi (≈x 1500–1670, y 70–100) HUD yıl kutusuyla temas ediyor. Çipi ≥80 px içeri al ya da bu çekimde itmeyi ≤%4 yap. Genel: kamera hareketinin SON pozunda çip kenar payı ≥48 px olsun (qa_flow'a kapı, §5'e bak). Tipografi üyesiyle çapraz bakılmalı; ben yalnız kameradan kaynaklanan kısmı yazıyorum.

**K1 — KÜÇÜK · 3,8–13,3 s açılış yatak odası 9,6 sn.** 9,2 sn'de ("Toskana'yı yönetmiş …son üyesi o") arma/soy ağacı goblenine kes ya da çekimi 6–7 sn'e indir; ilk 13 sn'de 2 yerine 3 görsel olay olsun (kanca üyesiyle çapraz bakılmalı).

**K2 — KÜÇÜK · `qa_flow` "Tür tekrarı" adlandırmayla atlatılıyor.** `oda` / `p1_oda`, `map` / `p1_map` / `c0_harita` farklı `kind` sayılıyor: #1–#4 aynı oda 4 ardışık çekim, 6 çekimden 5'i aynı oda. Taban tür (`p1_` önekini sıyır) ve görsel aile haritası kullan (§5).

**K3 — KÜÇÜK · 358–417 s üç harita.** #59 (Brugge → Barselona, 5,9 sn), #61 (7,7 sn, aynı rota, ikinci poliçe), #68 (411 s, Venedik): #59–#61'i anahtar kareli tek harita çekimine birleştir (kamera çapaları "Brugge", "Barselona", "tahsil") ve #61'in yerine bir mektup/poliçe ya da figür (bankacı el sıkışması) çekimi koy. Haritalar rota anlatımında meşru; sorun üçünün 60 sn'ye sıkışması.

**K4 — KÜÇÜK · c1→c2 bölüm kartı.** #55 kütüphane → 3 sn kart → #57 aynı kütüphane (KAMBİYO): kart bir mekân değişimi olmadan süreklilik kesiyor ve 3,1 sn müzik-yalnız boşlukla bitiyor. Bırakılabilir (Rehber §9 "3 sn sessizlik"), ama kart ≤2,2 sn ya da kartı çekimin üstüne bindirmek akışı güçlendirir. Değiştirmeden bırakmak da kabul.

**Korunacaklar (dokunma):** c0→c1 sikke-yıl dönüşü ve fresk başlığı; 26–55 s ivmeli pasaj ve 49 s `carry` belge→masa eşleşmesi (gecis_carry); 31→1737 `zoomthru` (gecis_zoomthru); veba pasajı 184–217 s (8 çekim/32 s, renk solması); #44/#87/#91 Machiavelli masa motifi; madalya = kişi motifi; defter üç kez (303, 418, 517 s) giderek dolarak dönüyor; sözcük çapaları (239) ve kesme noktasının cümle nefesine kilidi.

### Doğrulama için hedef değerler (Başkan yeniden ölçsün)
- sert kesme payı ≥%30; geçiş süresi standart sapması ≥0,3 sn; en uzun itme dizisi ≤5.
- her 60 sn pencerede ≥1 dünya çekimi; üst üste kart ≤4; 7.–8. dk kapsama ≥0,50, çekim içi hareket ≤3 payı ≤%50.
- dakika çekim sayısı 9–13, en az bir dakika ≥14, ≥2 montaj dizisi; 12 sn üstü çekim ≤5.
- 593,9 sn sonrası ≥1,2 sn kalış.

## 4. En emin olmadığım nokta

Kart vadisinin "monoton" mu yoksa "bilinçli sakin/ağır" mı hissettireceği. Veri (kapsama 0,36, %83 düşük hareket, 26 ardışık itme, 186 sn dünyasız) nesnel ama algı değil: çekim içi pop-in animasyonu (1,5–2 sn'de bir öğe) izleyiciyi tutuyor olabilir; defter/fresk cildinin kendisi markanın imzası olabilir ve kullanıcı bunu seviyor olabilir. Ayrıca "dünya/kart" sınıflaması benim gözümle 480 px küçük resimden; sınır vakalar (#17/#19 sikke, #20 çiçek, #21–#22 darphane figürleri) tartışılabilir. Karar açısından en emin olduğum kısım kamera (26 itme), geçiş tempo tekdüzeliği ve 0 dünya çekimi; en az emin olduğum, bunun izleme süresine ne kadar yansıyacağı.

## 5. Motor sorusu (kurgu açısından)

**Kurgu araçları yeterli mi?** Evet; aletler yeterli, politika ve ölçütler yetersiz. Çapalar (239 sözcük, 107 cümle, mutlak yalnız 9) ses değişince görüntüyü kaydırıyor; `link=`'li geçişler gerçekten eşleşme kesmesi üretiyor (31 → 1737 odası, belge → masa, sikke → bölüm); `lead/birth` gelen çekimi "doğmuş" getiriyor; geçiş görsel kalitesi Sisifos'un 5 türünün (cut/fade/clay/black/white; 75 çekim, 43 sert kesme) belirgin üstünde. Kurgu zanaati açısından yeniden yazmaya ya da başka motora (Chromium/Canvas) geçmeye **değmez**: ritim sorunları motorda değil çekim listesinde ve kapılarda.

**Eksik:** (1) Kapılar eşik denetliyor, **çeşitlilik ve dağılım denetlemiyor**: 11/11 GEÇTİ iken 26 ardışık itme, 17 ardışık kart, 186 sn dünyasız çekim var; "Tür tekrarı" `kind` adına bakıyor (`oda` ≠ `p1_oda`); "Çekim uzunluğu" medyanı 4–6'ya çiviliyor, dağılımı ve fazlama yapısını ölçmüyor (özilinti 0,06). (2) "Gerekçeli geçiş ≥%70 / çıplak kesme" dili sert kesmeyi cezalandırıyor: 94'te 4 sert kesme (Sisifos 75'te 43, geçiş süreleri 0,35–1,2 sn; Medici 0,9 sn tek tempo, `norm_tr` ≤1,0'a kırpıyor). (3) Kamera oran bazlı (%6–8), hız bazlı değil: aynı "push" 0,37 ile 3,64 %/sn arası (9,9 kat). (4) `montage` hiç kullanılmadı; 2,2 sn altı çekim, J/L ayarı, sessizlik payı için araç/kapı yok. **Fazla:** 12 geçiş türü görsel çeşit veriyor ama hepsi aynı 0,9 sn'lik darbeyi (enerji 33–42) ve her biri kendi SFX'ini taşıyor: çeşit görsel, ritim tek.

**En yüksek getirili 3 iyileştirme (maliyet tahmini):**
1. **qa_flow çeşitlilik kapıları + aile haritası** (≈0,5–1 gün, render yok): ardışık aynı kamera ≤5; ≥8 sn çekimde hız ≥%0,8/sn ya da itme-dışı hareket; ardışık kart ≤4 ve her 75 sn'de ≥1 dünya çekimi (tür → aile haritası, `p1_` önekini sıyır; isteğe bağlı kapsama vekili); sert kesme ≥%30, geçiş süresi σ ≥0,25; dakika başı çekim 9–13 ve ≥1 dakika ≥14; kamera son pozunda yazı kenar payı ≥48 px. Bu kapılar bugünkü parçayı KALDI yapardı; amaç tam bu.
2. **Geçiş politikası + süre aralığı** (≈0,5 gün motor: `norm_tr` kırpmasını kaldır/uzun varyant, 0,25–0,4 sn "vuruş" ekle, `tr=None` birinci sınıf; ≈1 gün yazım: c1–c2'de ≈35 geçişi kesmeye ve süre çeşidine çevir; render ≈17 dk (4 işçi) + `sfx_gecis` yeniden üretimi otomatik; yerel saat/lead kayması ve mutlak `at=` taraması dahil). Montaj dizileri ve 1,2–1,5 sn parça sonu kalışı (Ö4) bu iş paketine girer.
3. **E1: c2 kart vadisini kırma + hız bazlı kamera** (≈1,5–2 gün yazım: 4–6 çekim mevcut `oda`/`sehir` setlerinin yeniden ışıklandırılmasıyla; ≈0,5 gün `cilt_cam` hız bazlı itme `("push", rate=…)`; yalnız c2 yeniden render ≈7 dk, çekimlerin süresi değişirse tüm parça ≈17 dk). Getiri: 7.–8. dakika kapsama 0,36 → ≥0,5, 26 ardışık itmenin kırılması.

Dürüst bilanço: Medici, kurgu araçları açısından Sisifos hattından daha yetenekli; ama bu parçada o yetenek 0–420 s arasında kullanılmış, 420–590 s arasında bırakılmış. Geçiş/kamera/kesme politikasını gevşetmeden bu zaafı tekrar üretir: P2–P7 de aynı kapılardan geçecek ve aynı vadiyi aynı yerde (parçaların son üçte biri, bilgi yüklü bölümler) yaşama riski taşıyor. Önce kapılar (1), sonra P1'i onlara göre düzelt (2–3).
