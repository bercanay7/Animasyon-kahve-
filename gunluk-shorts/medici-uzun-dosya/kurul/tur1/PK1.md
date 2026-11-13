# PK1 — Kapak, başlık, yayın paketi · Mercek: TO / paketleme stratejisti · TUR 1

Kapsam: `yayin/kapak_P1_A|B|C.jpg`, `kapak_P1_kontrol.png`, `yayin/studio_paketi_P1/*`, `yayin/YAYIN_TASLAK.md`. Başka üyenin raporunu görmedim, başka üyenin dosyasını okumadım. Scratch (maketler, test sayfaları): `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/pk1/`.

---

## 1. Karar

**RED — 6/10** (eşik ≥9).

| Parça | Puan | Tek cümle gerekçe |
|---|---:|---|
| Kapak A (MEDİCİ freski) | 5 | Başlık kartı, vaat yok; büyük harf %14,2; ikincil yazılar 246 px'te bile okunmaz; çerçeve boşluğu + altın benekler gürültü |
| Kapak B (BİR SÖZLEŞME…) | 6 | Açılışla uyumlu tek kapak ve merak var; ama büyük harf %9,7, ikinci satır %7,3, metin "şehri bağladı" ile tam doğru değil, dokümanın kendisi duygusuz |
| Kapak C (FLORİN…) | 6,5 | En okunaklısı (%13) ama "Florin ve çifte defter" ders kitabı başlığı; "çifte defter" videonun çürüttüğü Medici-icadı mitini çağrıştırıyor |
| Başlık | 5,5 | "Nasıl Doğdu? Florin ve Defter": jargon + belirsiz; aranan "Medici Ailesi" ifadesinin "Ailesi" kısmı yok |
| Açıklama (ilk 2 satır) | 6,5 | Tarihle başlıyor; kanca ve anahtar sözcük 100. karakterden sonra |
| Sabit yorum | 7,5 | Soru iyi (faiz/kambiyo, bölümün en tartışmaya açık yeri) ama uyarı paragrafı sorunun önünde |
| Bölüm damgaları | 6 | 3 bölüm / 10 dk; arama "önemli anlar"ına ve ilerleme çubuğuna merak taşımıyor |
| Etiketler | 6,5 | "Lorenzo de Medici" yanlış niyet (P3'ün konusu); aranan sözcüklerin bir kısmı eksik |

Kapak test seti (aşağıda ölçümler) kanalın kendi eşiklerini üç kapakta da geçmiyor. Kapaklar "videonun bir karesi + yazı"; kanalın çalışan kapakları (Sisifos, Orfeus, Şarlken madalyalar, Sultanın Öğrencisi) "tasarlanmış bileşim + iki kelimelik iddia". Engelleyici bulgular kapakta; başlık/açıklama ise kısa sürede düzelir.

---

## 2. Ne gördüm / neye dayandım

**Sınır (açık):** videoyu oynatamadım, sesi dinleyemedim. Kare çıkardım (ffmpeg: 0,5–30 sn arası 7 kare, 42/61/82/96/104/112/378/394/400/407/462/480/590 sn, 65–84 sn harita/Uffizi, 393–395 sn "faiz hediye" karesi), `out_p1/kurul/qa_flow_ozet.txt` çekim tablosundan zaman damgalarını aldım, anlatı metnini `script.py c0/c2` ile okudum, `kaynaklar_P1.md` sınıflarına (◐/○/ANEKDOT/MİT) baktım. Gerçek TO verisi yok; "TO tahmini" yerine kanalın kendi verisiyle (Cumhuriyet yeniden paketleme, Şarlken %79 açılış, Sisifos "kapak–açılış uyumu" dersi) akıl yürüttüm. YouTube arama önerilerini/hacmini göremedim (WebSearch yalnız genel Türkçe sayfalar döndürdü; Türkçe yazımda "Medici ailesi", "Mediciler", "Medici bankası", "Floransalı Medici ailesi" görüldü, hacim bilinmiyor).

**Bakılan dosyalar:** `kapak_P1_A/B/C.jpg` (1280×720), `kapak_P1_kontrol.png`, `kapak_medici.py` (yazı boyutları, rozet), `studio_paketi_P1/01–05`, `YAYIN_TASLAK.md`, `KULAK_KONTROL_P1.md`, `bolumler_P1.txt`; kanal referansları `sisifos/kapak.png`, `kapak_b.png`, `orfeus/kapak_final_A…`, `sarlken_kapak/*` + README, `cumhuriyet_kapak/*`; Anayasa §7/§13/§15 başlık ve kapak maddeleri; CLAUDE.md "Kapak dersleri / Ölçütler / Kapak test seti".

**Yaptığım testler** (scratch: `test_orig.png`, `feed_orig.png`):
tam boy; 246×138, 168×94, 120×68 (INTER_AREA, ayrıca 2× en-yakın-komşu büyütme); gri değer; bulanıklık (odak vekili); koyu ve açık mobil akışta kanalın diğer kapaklarıyla yan yana (360 px); sağ alt rozet bölgesi (1280×720'de x 960–1250, y 553–689); büyük harf yüksekliği ölçümü (piksel eşiği + Cinzel metriği: kap yüksekliği = 0,70 × punto).

**Ölçümler (1280×720):**

| | Hero yazı | Hero yazı % | İkincil yazı | İkincil % | 168×94'te hero | Rozet bölgesi | Sorun |
|---|---|---:|---|---:|---|---|---|
| A | MEDİCİ cap ≈ 102 px (y 333–435) | **14,2** | "PARÇA 1/7 · ALTIN FLORİN" ≈ 28 px; "ZAMAN KURYESİ" ≈ 14 px | 3,9 / 1,9 | okunur | temiz | İkincil yazılar 246×138'de bile okunmaz. Bez bandı x 0–110 ve 1190–1280, y 0–50 ve 615–720 boş/karanlık (alanın ≈%22'si). Altın benekler harfle aynı renk, figür-zemin gürültüsü; gri dönüşümde orta-ton çamuru |
| B | satır 1 cap ≈ 70 px (y 60–133) | **9,7** | satır 2 ≈ 52 px (y 190–245) | **7,3** | satır 1 ≈ 9 px, satır 2 ≈ 7 px | belge makarası (x 930–1200, y 530–570) kısmen içinde (önemsiz) | 120×68'de satır 2 okunmaz. Soldaki kesik siluet okunmuyor ("kim?"); belge çizgileri kıvrım dolgu, bilgi taşımıyor |
| C | FLORİN cap ≈ 93 px (y 167–260) | **13,0** | "VE ÇİFTE DEFTER" ≈ 36 px (y 335–372) | 5,1 | okunur | temiz | İkinci satır 168 px'te okunmaz. Tek belirgin en parlak nokta yok: sol sikke ile yazı yarışıyor; kapak en karanlık |
| Rozet "1/7" kutusu (üçü) | 220×100 px (x 24–244, y 594–694) | | "PARÇA" etiketi ≈ 19 px | | 168 px'te kutu 29 px, "PARÇA" okunmaz | | Yer harcıyor ama bilgi taşımıyor |

Kanal kuralı: büyük harf ≥ %18 (130 px @720p). Üçü de altında. `kapak_medici.py` docstring'inde "≥72 px" yazıyor: bu kural kanalınkinden zayıf; QA'yı yanıltıyor.

**Mobil akış karşılaştırması** (`feed_orig.png`, koyu + açık): Sisifos/Orfeus/Şarlken/Sultanın Öğrencisi kapakları iki kelimelik kalın yazı + doygun renk + net özne; Medici üçlüsü ise ince hatlı Cinzel, düşük doygunluk, koyu zemin: koyu modda ana sayfanın zemini #0f0f0f'e karışıyor, B en soluk, C en koyu, yalnız A mavisi sayesinde çıkıyor (ama hiçbir şey söylemiyor).

**Beş saniye testi ("ilk bakışta anlaşılıyor mu?"):**
A: "Medici belgeseli, 1. parça": anlaşılıyor, tıklama nedeni yok.
B: "bir belge/sözleşme bir şeyi bağlamış": merak var, hangi sözleşme/kim belirsiz, "Medici" kelimesi kapakta yok.
C: "Florin = para tarihi / muhasebe": anlaşılıyor, merak yok, "çifte defter" kuru.

**Kapak–açılış uyumu** (Sisifos "NEDEN GÜLÜYOR?" dersi): video 0:00–1:41 arası 1743 odası, belge, mühür, III. madde, Uffizi kuyruğu; sonra 1:41'de ana başlık freski (A kapağı bu kare); florin 1:48'de; **faiz yasağı / kambiyo / "vicdan komitesi" / "faiz değil hediye" 5:48–6:40'ta**; Cossa–Papa 7:17–8:10. Yani:
- B kapağı açılışla uyumlu (vaat ≤1:41'de ödeniyor).
- C kapağı 1:48'deki sikke bölümüyle uyumlu ama "çifte defter" 6:58'de ve orada "Medici icat etmedi" deniyor.
- Videonun en yoğun merak noktası (faiz yasağını aşmak; faizi yasaklayan Kilise'nin müşteri olması; "faiz değil hediye") hiçbir kapakta ve başlıkta yok.

---

## 3. Sıralı düzeltme listesi

Koordinatlar 1280×720 (1920×1080 için ×1,5).

### 3a. Kapak (hepsi için)

1. **[ENGELLEYİCİ] A, B, C'nin hepsi "başlık kartı" düzeyinde; kanalın "ilk bakışta tıklama nedeni" ölçütünü geçmiyor.** A'yı teste sokma (aşağıda gerekçe). B ve C'yi 3b'deki K1/K2 ile değiştir ya da bu iki kapağı o yönde yeniden kur.
2. **[ENGELLEYİCİ] Hero yazı < %18.** A: 102 → ≥130 px; B: 70 → ≥130 px; C: 93 → ≥130 px. K1/K2 maketinde "FAİZ" cap 160 px (%22), "MEDİCİ/SON MEDİCİ" cap 120–130 px. İkincil satır ≥ 70 px (%10), daha küçüğü 168×94'te zaten okunmaz: yazma.
3. **[ENGELLEYİCİ] İkincil yazılar silinmeli veya büyütülmeli:** A: "ZAMAN KURYESİ" (x 490–810, y 108–128) ve "PARÇA 1/7 · ALTIN FLORİN" (x 440–865, y 495–528) kaldır (kanal adı akışta zaten yazılı; "1/7" rozette var). C: "VE ÇİFTE DEFTER" (x 720–1215, y 335–372): kaldır ya da ≥ 70 px.
4. **[ENGELLEYİCİ — vaat doğruluğu]** B: "BİR ŞEHRİ BAĞLADI": sözleşmenin 3. maddesi sanat hazinesini ve kütüphaneleri Floransa'dan çıkarılamaz kıldı (c0s11–12); şehri değil, mirası bağladı. "Hiçbir şey buradan çıkmayacak" cümlesi kapakta kullanılmamış: doğru (YAYIN_TASLAK notuna uygun, Anna Maria Luisa'ya atfedilmiyor). Yeni metin "MİRASI KİLİTLEDİ" (K1), kaynak üyesi "kilitledi" fiilini "çıkarılamayacaktı" düzeyinde mi kabul ediyor, teyit etsin.
5. **[ÖNEMLİ]** C: "FLORİN VE ÇİFTE DEFTER": videonun 6:58–7:16 bölümü çifte kaydın Medici icadı olmadığını söylüyor (c2s12–13). Kapakta ve başlıkta "defter" Medici'nin yeniliği gibi okunur. "Çifte defter/defter" kapaktan ve başlıktan çıksın; videonun kendi çürütmesi bölüm adında ("Çifte kayıt: Medici icadı mı?") bir "önemli an" olarak kalsın.
6. **[ÖNEMLİ] Doygunluk/kontrast:** üç kapak da koyu ve düşük doygun. Hedef: hero yazı ile zemin parlaklık farkı ≥ 7:1, yazı rengi altın (≈ #F0CD73) / krem (#FAEEC8), zemin yakın-siyah sıcak gradyan (maketteki #140C08 → #0A0818) + tek ışık kaynağı. Gri testte hero yazı zeminden ≥ 70 gri seviyesi ayrılsın. Orfeus/Sisifos'tan fark: onlarda en az bir doygun renk alanı var (turuncu/mavi); Medici'de kırmızı (hediye kutusu, mühür) bu rolü oynasın.
7. **[ÖNEMLİ] Tipografi:** kapakta Cinzel Bold (700) yerine **Cinzel Black (900)** kullan. `/home/user/sisifos-wt/sisifos/fonts/Cinzel-normal-900-latin(.woff2, -latin-ext)` mevcut; değişken yazı tipi (400–900), PIL'de `font.set_variation_by_axes([900])` ile 900'a çekiliyor; latin-ext İ, Ş, Ğ, Ç, Ö, Ü karakterlerini taşıyor (125 glif, doğruladım). Sonuç maketlerde 120×68'de "FAİZ" ve "SON MEDİCİ" okunuyor. Medici `fonts/` dizininde 900 yok: kopyala. Not: Şarlken kurulunda sanat üyesinin tercihi video yazı kimliği (Cinzel); 900 ağırlığı kimliği bozmadan okunurluğu getiriyor. Anton/Alfa Slab yedek.
8. **[ÖNEMLİ] Rozet "1/7":** "PARÇA" etiketini kaldır, kutuyu 220×100 → 150×74 px yap (maket: x 26–176, y 620–694), yazı "1/7" (≈46 px). Sol alt köşede kalsın (aile tutarlılığı, rozet bölgesi dışı). 168 px'te zaten ancak "1" okunur; amaç yer açmak.
9. **[ÖNEMLİ] Süre rozeti ve fare üstü simgeler:** x 960–1250 × y 553–689 boş (benim K2 maketimde kutunun sağ alt köşesi bu bölgeye giriyor; gerçek sahnede düzeltilmeli: kutu y ≤ 545 ya da x < 960). Ek olarak masaüstü fare üstü simgeler (Sonra izle / kuyruğa ekle) sağ üst köşede: x ≥ 1170, y ≤ 110 hero yazı içermesin.
10. **[KÜÇÜK] A kapağı çerçeve:** x 0–110, 1190–1280, y 0–50, 615–720 boş; sahneyi ≈ %18 yakınlaştırıp bez bandı kadraj dolduracak şekilde kırp (merkez 640,330). Altın benekleri (harf rengiyle aynı) hero yazı arkasında %60 bastır. Bu iş yalnız A kapağı herhangi bir yerde kullanılacaksa gerekli (3b: seri kapağı/Tam Film).
11. **[KÜÇÜK] `kapak_medici.py` kuralını ve QA'sını düzelt** (bkz. Motor sorusu #1): docstring "≥72 px" → "hero cap ≥ %18 (130 px @720p)"; `kontrol()` 320×180 şeridinden 246/168/120 + gri + rozet bölgesi + besleme taklidi çıktısına çıksın.

### 3b. Kazanan A/B çifti ve test düzeni

**Öneri: K1 ile K2, 14 günlük "Test ve Karşılaştır", başlık sabit (T1).** Mevcut A, B, C'den yalnız B ve C'nin fikri (açılış belgesi / para) taşınıyor; ikisi de yeniden çizilecek. A elenir (gerekçe: tıklama nedeni yok, kanalın kapı kapaklarıyla yan yana akışta en az bilgi taşıyan kapak); yalnız seri aile kapağı ve Tam Film için saklanır.

**K1 — "SON MEDİCİ / MİRASI KİLİTLEDİ"** (açılışla uyumlu; B'nin gelişmişi). Hızlı yol, ≈2–3 saat: B'nin `oda1743` karesini kullan.
- Zemin: B'nin belge karesi 40 px aşağı kaydırılır (belge x 360–945, y 276–660); üst bant sıcak koyu gradyan (y 0–250 tam, 250–320 geçiş).
- Hero: "SON MEDİCİ", Cinzel Black, **cap 120 px** (%16,7; genişlik ≈ 1160 px, x 60–1220, taban çizgisi y 160) altın #F0CD73. Kural sapması −%1,3: tek satırda genişliğin %90'ı kaplıyor. Tam %18 istenirse alternatif: sol sütun, "SON" cap 62 (y 215) + "MEDİCİ" cap 130 (taban y 330; ≈ 760 px) + "MİRASINI/KİLİTLEDİ" iki satır cap 70 (ilk maketim, `mock_K1.png`).
- İkincil: "MİRASI KİLİTLEDİ", cap 72 px, krem #FAEEC8, merkezde, taban çizgisi y 262.
- Odak: belgenin üzerine **zincir + pirinç asma kilit** (merkez x 655, y 545; gövde 152×130; kulp yayı yarıçap 48; zincir y ≈ 545, x 380–860). Motorda hazır ilkeller: `c0_kinds.py` `c0_harita` zincir/kilit, `icons_extra.py` `chains`, `c4_kinds.py` `draw_key`. Kilidin çevresinde mum sıcaklığında yumuşak parlama (merkez 655,545; yarıçap ≈ 130): kare en parlak noktası orası olsun (belge ikinci).
- Kırmızı mühür (x 800–860, y 535–595) görünür; **makara/tomar (x 930–1200, y 530–570) kaldırılır** (rozet bölgesi).
- Silüet (sol kenar kesik gövde): kaldır ya da tam göster; kesik hâli "kim?" sorusu doğuruyor, ½ siluet 168 px'te bir leke.
- Rozet: 3a-8. Kanıt: maket `mock_K1b.png`; test sayfası `test_new2.png`: 120×68'de "SON MEDİCİ" okunuyor, kilit net odak, gri testte kilit ve hero ayrışıyor.

**K2 — "FAİZ YASAKTI"** (gövdenin en güçlü merakı; C'nin gelişmişi). İki yol:
- *Güçlü yol, ≈yarım gün (yeni kapak sahnesi):* motorda hazır `c2_hediye` sahnesini (hediye kutusu, açılan kapak, dökülen florinler, "FAİZ" etiketi; 391.8–397.9 sn) kapak ölçeğinde yeniden çiz: video karesinde kutu ekranın ≈%22'si, bej parşömen zemin üzerinde. Kapak için kutu ≈ %30 genişlik, koyu sıcak zemin, parlama merkezi (900, 300), kutu gövdesi x 760–1060 × y 330–545, kapak 24° eğik, florin yağmuru y 40–330. Kutu kurdelesine Medici palle arması (5 kırmızı küre; kutu üstünde ≈ 60 px) koy: "Medici" adı kapakta bu simgeyle (marka tanıma) gelsin; etiket yazısı ("FAİZ") kaldırılsın (başlıkta zaten var, tekrar).
- *Hızlı yol, ≈1 saat:* C'nin sikke karesine yeni metin: "FAİZ" cap 150 (x 718–1240, taban y 270, sağa yaslı), "YASAKTI" cap 95 (x 598–1240, taban y 390). Daha zayıf (sikke ile "faiz yasağı" bağı soyut), ama C'nin okunurluk avantajını korur.
- Yazı (iki yol için): hero **"FAİZ" cap 160 px (%22), x 48–604, taban y 235**, altın; **"YASAKTI" cap 100 px (%14), x 48–723, taban y 370**, krem. Üçüncü satır **yok** (maketteki "MEDİCİ NE YAPTI?" cap 56 px, 168 px'te okunmadı: çıkar). Kanıt: maket `mock_K2.png`, `test_new2.png`.
- Risk 1: "faiz yasağı" Türk izleyicide dinî çağrışım taşır; video Kilise'nin yasağını anlatıyor. Kutu kurdelesindeki palle arması, başlıktaki "Medici Ailesi" ve açıklamanın ilk cümlesi ("Kilise faizi yasaklamıştı…") bu belirsizliği çözer. Gerekirse hero "KİLİSE FAİZİ YASAKLADI" (daha az dramatik, 3 sözcük) alternatif, ama kapakta cap küçülür.
- Risk 2: ödeme 5:48'de (vaat videonun %58'inden sonra). 0:30 ve 3:00 tutma düşebilir. Bu yüzden K2 **tek başına yayınlanmaz**, K1 ile testte yarışır: Test ve Karşılaştır kazananı tıklamaya göre değil izlenme süresi payına göre seçer (Anayasa §13-16; CLAUDE.md), yani "tıklanan ama bırakılan kapak" kendiliğinden elenir.

**Test düzeni:** 14 gün; test sürerken başlık değişmez (CLAUDE.md). Kazanan K2 çıkarsa: bölüm damgası 5:48'i sabit yoruma ve açıklamanın 2. satırına koy; P2–P7 kapaklarında "para/yasak/ironi" kalıbını dene. Kazanan K1 çıkarsa: "açılış–kapak uyumu" dersi pekişir (Şarlken %79). Şarlken'in günde ~70 gösterimlik hızında 14 gün yetmeyebilir; Prometheus ~20. saatte 18 B gösterimlik göz atma testi aldı, o ölçekte test günler içinde biter. Sonuç "fark yok" çıkarsa K1 kalsın (kural: doğru vaat).

Not (aile): K1 kanalın "nesne + geçmiş zaman" kalıbını sürdürüyor (ÖLÜMÜ ZİNCİRLEDİ / TAHTI BIRAKTI / BİLE BİLE ÇALDI / MİRASI KİLİTLEDİ). Bu kanalın imzası olarak güçlü, ama dördüncü art arda aynı kalıp "NEDEN …?" yorgunluğunun benzerini doğurabilir; bu yüzden K2'yi (isim + yüklem: "FAİZ YASAKTI") dilbilgisi olarak ayrı tuttum.

### 3c. Başlık (≤60 karakter; ilk ~40 karakterde anahtar sözcük + vaat — Anayasa kapı 4)

Mevcut: `Medici (1/7): Bankacı Aile Nasıl Doğdu? Florin ve Defter` (56; YAYIN_TASLAK'ta 55 yazıyor, doğrusu 56). Sorunlar: "Ailesi" yok (Türkçe aramada "Medici ailesi" baskın), "Nasıl Doğdu?" belirsiz, "Florin ve Defter" jargon ve yukarıdaki 3a-5 nedeniyle "defter" yanıltıcı.

**Öneri T1 (testte sabit başlık):** `Medici Ailesi (1/7): Faiz Yasakken Nasıl Zengin Oldular?` (56). Aranan ad başta; vaat videonun gerçek gövdesi (c2s2–c2s11: Kilise faizi yasakladı, bankacılar yol buldu, Giovanni'nin 180 bin florinlik servet).
K1 ile birlikte okununca iki yarı birleşir: "Son Medici mirasını kilitledi" + "faiz yasakken nasıl zengin oldular?" = videonun kendi sorusu (c0s16). K2 ile pekiştirir.
İki satırlı mobil akışta ilk ~45 karakter "Medici Ailesi (1/7): Faiz Yasakken Nasıl…" görünür.

**T2 (K1'e dönük, ifade + açık uç):** `Medici (1/7): Son Medici Mirasını Kilitledi. Peki Nasıl?` (56).
**T3 (ironi, soru kalıbı yok):** `Medici Ailesi (1/7): Faiz Yasaktı, Kilise Müşteri Oldu` (54). Not: "Kilise'nin müşteri olması" c2s9–10 tek kaynak (de Roover, ○): kaynak üyesi onaylamadan kullanma.

**Uyarılar:**
- **"NEDEN" yok.** Son kanal paketlerinde: Sisifos (kapak "NEDEN GÜLÜYOR?" + başlık "Neden Mutlu"), Şarlken yeni başlık ("…Neden Vazgeçti?"). Cumhuriyet başlığı "Nasıl Yetiştirdi?". Dördüncü art arda soru kalıbı yorgunluk riski: T1 "Nasıl" kullanıyor; bu yüzden T2/T3 ifade biçiminde. P1'in başlığında **bir** soru kökü (Nasıl) yeter; kapakta soru işareti yok.
- Seri düzeyi: `YAYIN_TASLAK` P4 alternatifi "Defter Neden Kapandı?", P7 alternatifi "Rönesans'ı Gerçekten Onlar mı Yarattı?" art arda soru yükü getirir. Öneri ritim: P1 soru (Nasıl), P2 ifade, P3 ifade, P4 soru (Ne/Kim), P5 ifade, P6 soru ("…mi?"), P7 ifade.
- "(1/7)" önde: seri bilgisini veriyor ama 6 karaktere ve hook'u sağa itiyor. Alternatif sonda: `Medici Ailesi: Faiz Yasakken Nasıl Zengin Oldular? (1/7)` (56), P2–P7 de aynı ek biçimle. Önem küçük; oynatma listesi seri sırasını zaten taşıyor.
- Aşırı iddia: "satın aldı/ele geçirdi" yok, doğru. "Zengin oldular" yalnız P1 (1429'a kadar; 180 bin florin, 152.820 florin kâr) düzeyinde; "Avrupa'nın en güçlü bankası" gibi video söylemediği ifadeler kullanma.

### 3d. Açıklamanın ilk 2 satırı

Mobilde ilk ≈100 karakter, masaüstünde ≈2 satır görünür; mevcut metin "18 Şubat 1743, Floransa. Yetmiş beş yaşında bir kadın ölüyor…" ile başlıyor, soru 270. karakterde.

```
Medici Ailesi (1/7): Kilise faizi yasaklamıştı; bir bankacı ailesi yine de para kazanmanın yolunu buldu.
1743'te son Medici'nin imzaladığı sözleşmeden 1252'de basılan ilk florine geri sarıyoruz. 5:48'de faiz yasağı ve "vicdan komitesi".
```
Karakter: 104 / 131. 1. satır anahtar sözcük ("Medici Ailesi") + vaat; 2. satır açılışı ve bölüm bağlantısını verir. Mevcut açıklamanın kalanı (1743 anlatısı, kaynak ayrımı, kaynaklar, ses notu) aşağıda kalsın. Sorunun kendisi ("Peki bir bankacı ailesi, mirasını bir şehre bağlayacak noktaya nasıl geldi?") 3. paragrafa düşsün.

İsteğe bağlı (yalnız açıklamada; başlıkta yok): "Netflix/Rai dizisi Medici 1429'da başlar; bu parça o yıla kadarki hikâye." — **benim bilgim, teyit edilmedi** (dizinin başlangıç yılı); doğrulanmadan yazma. Etiket olarak "Medici dizisi" kullanma: yanıltıcı metaveri riski.

### 3e. Bölüm damgaları (qa_flow çekim tablosundan; her biri ≥ 10 sn)

```
0:00 Son Medici ve 1743 sözleşmesi
1:41 Florin: Floransa kendi altınını basıyor (1252)
3:05 Kara veba (1348)
3:37 Ciompi isyanı (1378)
4:53 Giovanni di Bicci ve ilk sermaye (1397)
5:48 Faiz yasağı, kambiyo ve "vicdan komitesi"
7:17 Cossa, Papa ve Medici'nin kasası
8:11 Catasto: Floransa servet sayıyor (1427)
```
İsteğe bağlı 6:58 "Çifte kayıt: Medici icadı mı?" (mit çürütme; arama niyetiyle uyumlu). Kaynak zamanları (sn): 101.2, 184.6, 217.2, 293.0, 347.6, 436.6, 491.3. Videonun ekrandaki bölüm kartı hâlâ "Defterin Sihri": açıklamada "Defterin Sihri" ismi kullanma (3a-5); Şarlken'in 11:03 yeniden adlandırması emsal. Bölümler yayından sonra düzenlenebilir.

### 3f. Sabit yorum

Mevcut: kaynak uyarısı ilk, soru son. Sırayı çevir:
```
Soru: Kilise faizi yasaklamıştı; bankacılar kambiyo ve "faiz değil, hediye" gibi yollar buldu (5:48). Sizce bu zekâ mıydı, dolambaçlı yol mu?
Rakamlar ve tarihler araştırma özetlerine dayanır; rivayetler videoda "rivayet" diye işaretlendi. Tam kaynak/teyit tablosu isteyen yazsın, paylaşalım.
Sıradaki: 2/7, Cosimo'nun kulesi, sürgün ve dönüş.
```
Not: "Birincil metinlere doğrudan erişemediğimiz yerlerde…" cümlesi (mevcut) kamuya açık yorumda kanal otoritesini zayıflatıyor; ◐/○ nitelemesi videoda zaten yapılıyor. Bu kararı kaynak üyesi/başkan versin; ben yalnız TO açısından uyarıyorum. "faiz" tartışması dinî yorum savaşına dönüşebilir: ilk saat yorum cevabı (Anayasa §7) bu yüzden kritik; hassasiyet üyesi bu konuyu ayrıca görsün.

### 3g. Etiketler

Mevcut listeden çıkar: `Lorenzo de Medici` (P1'de yalnız büyük torun olarak bir cümle; aranınca yanlış niyet, P3'ün konusu), `Cosimo de Medici` (P2'de güçlü; P1'de yalnız son cümle), `Uffizi` (≈20 sn; zayıf).
Ekle (≈ aranan ifadeler, Türkçe yazım çeşitleri): `Medici Ailesi Tarihi, Medici bankası, Mediciler, faiz yasağı, kambiyo, Orta Çağ bankacılığı, Floransa tarihi, Medici ailesi nasıl zengin oldu, Giovanni di Bicci`. Kalsın: `Medici, Medici Ailesi, Floransa, Rönesans, Florin, Ciompi İsyanı, Kara Veba, çifte kayıt, bankacılık tarihi, Anna Maria Luisa de Medici, İtalya tarihi, tarih belgeseli, Zaman Kuryesi`.
Hashtag (açıklama sonu): ilk üçü başlığın üstünde görünür: `#Medici #Floransa #Rönesans` (mevcut sıra doğru); dördüncü `#TarihBelgeseli` kalabilir.

### 3h. Aile (7 kapak) için ilke

Parça başına bir nesne, bir hero sözcük: P1 kilit/hediye; sabit unsurlar: koyu-sıcak zemin, Cinzel Black altın hero ≥ %18 (cap), krem ikincil, sol alt "n/7" (150×74), nesne sağda, palle arması kutu/kurdele üzerinde (marka). Yüz gerektiren parçalar (P3 Pazzi/Lorenzo, P6 iki kraliçe) için motorun yüz zayıflığını nesne/madalya ile çöz: Şarlken'in madalyalı kapağı (profil madalya) motorun zaten yaptığı biçim.

---

## 4. En emin olmadığım nokta

1. **K2'nin tutma maliyeti.** Vaadin ödemesi 5:48'de; izleyicinin 0:30'da kalma oranı (Şarlken %79'a karşı Sisifos %63) K2 tıklayanlarında düşük çıkabilir. Bunu yalnız deneyle öğrenebiliriz; çifti bu yüzden K1 ile K2 olarak kurdum.
2. **"Son Medici" soğuk izleyiciye bir şey söyler mi?** Medici adı Türkiye'de (dizi, Rönesans) tanınıyor ama "son Medici" vaadi bilinmiyor; K1 mühür/kilit simgeleriyle okunacak, ama TO'su K2'den düşük çıkabilir. Bilmiyorum.
3. **Cinzel Black'in dijital besleme gücü.** Ağır ağırlık maketlerde iyi okunuyor ama Anton/Alfa Slab kadar "çarpıcı" değil; Şarlken kurulundaki Cinzel–Anton tartışması burada da geçerli.
4. **"Faiz" sözcüğünün Türkiye'deki dinî yüklü okuması.** Hem tıklama artırabilir hem yanlış niyet (İslami finans) çekebilir; ölçemedim.
5. YouTube arama önerileri/hacimleri (arama niyeti kapısı) görülmedi: başkan ya da kullanıcı arama kutusuna `medici`, `medici ailesi`, `medici ailesi nasıl`, `mediciler`, `medici bankası` yazıp önerileri bakmalı.

---

## 5. Motor sorusu (kapak üretimi)

**Yeterli mi?** Nesne odaklı kapaklar için evet, yüz/duygu odaklı kapaklar için hayır; ve mevcut kapak hattı kanal çıtasının altında.

1. **Fark (Sisifos/Orfeus ile):** Sisifos ve Orfeus'ta kapak, videodan ayrı bir bileşim (`orfeus/kapak.js`: `head3q`, `hand`, `grip`, `rim`, `paperShadow`; Sisifos'ta özne + ışık + kalın başlık). Medici'de `kapak_medici.py` motorun bir karesini (`compose.Program(shots=[shot]).frame`) alıp üstüne Cinzel yazı koyuyor. Sonuç: video içi ölçek ve ışık (kamera, vinyet, düşük doygunluk) kapağa taşınıyor; kapakta ne tek odak ne tek hero yazı ölçeği var.
2. **Güçlü yan:** fresk/defter cildi ayırt edici ve pahalı görünüyor; sikke, belge+mühür, hediye kutusu, zincir/kilit, palle arması, harita gibi nesne ilkelleri hazır; Şarlken'in 9/10 alan madalyalı kapağı gibi nesne odaklı kapaklar motorun özüne uygun.
3. **Zayıf yan:** profil "kesme-bebek" figürü ve yüz/el (CLAUDE.md "üslubun sınırı"): Orfeus'un gözyaşı/uzanan eller gibi duygu kapakları bu motorla üretilemez; P3 (Lorenzo/Pazzi), P6 (Catherine/Marie) gibi parçalarda sorun çıkar → nesne/madalya/mekan ile çözülmeli.
4. **Karar:** yeniden yazma ya da başka motora geçme gerekmez; kapak hattını **iyileştir**. Bu iş motorun kendisine değil, kapak katmanına (`kapak_medici.py` + birkaç yeni sahne) ait.
5. **En yüksek getirili 3 iyileştirme:**
   - **(a) Kapak QA otomasyonu, ≈2–3 saat:** `kapak_qa.py`: hero cap % (eşik %18), ikincil ≥%10, rozet bölgesi (x 960–1250, y 553–689) ve fare simgesi köşesi (x ≥ 1170, y ≤ 110) içinde yazı/odak kontrolü, 246/168/120 + gri + koyu/açık besleme taklidi (kanal kapaklarıyla yan yana). Bu oturumdaki scratch betikleri (`mk_tests.py`, `mk_feed.py`) başlangıç noktası. Docstring "≥72 px" kuralını düzelt. Getiri: bu raporun 3a-1…11 maddelerinin çoğu otomatik yakalanır.
   - **(b) Kapak tipografisi + "kapak modu", ≈2–3 saat:** Cinzel Black 900 (değişken yazı tipi, yukarıda doğrulandı), iki seviyeli hiyerarşi (hero ≥%18 / ikincil ≥%10), gölge/dış hat, +%15–20 doygunluk ve kontrast eğrisi, tek ışık kaynağı + kenar parlaması, vinyetsiz. Getiri: hem 120×68 okunurluğu hem koyu modda ayrışma.
   - **(c) İki kapak sahnesi (hediye+florin yağmuru, kilitli/zincirli belge), ≈½–1 gün:** mevcut `c2_hediye` ve `c0_harita` zincir/kilit ilkellerini kapak ölçeğinde (kutu ≈%30 genişlik) kapak-özel kamera/ışıkla çiz; Orfeus'taki kapak bileşiminin Medici karşılığı. Getiri: K1 ve K2'nin gerçek sürümleri; sonraki parçalar için şablon.
6. **Sınır:** yukarıdaki maketler (`mock_K1b.png`, `mock_K2.png`) PIL ile kaba çizildi; amaç tipografi ölçeği, kompozisyon bölgeleri ve 120×68 okunurluğunu denemek; nesne çizimi motorun gerçek çıktısı olmayacak ve nihai kalite kurula yeniden sunulmalı.

---

## 6. Kabul ölçütü (2. tur için)

K1/K2 teslim edildiğinde şunlar tutmalı:
- hero cap ≥ %18 (K1 için en az %16,7 ve genişliğin ≥ %90'ı), ikincil ≥ %10 ya da yok;
- 120×68'de hero okunuyor, 168×94 gri testte hero–zemin ayrışıyor;
- süre rozeti bölgesi ve sağ üst fare köşesi temiz; ≤ 5 öğe; tek parlak odak;
- kapakta "Hiçbir şey buradan çıkmayacak" ya da "çifte defter" yok; "kilitledi" fiili kaynak üyesinden geçti;
- başlık T1, açıklamanın ilk 2 satırı 3d, 8 bölüm damgası 3e, sabit yorum 3f, etiket 3g uygulandı.
