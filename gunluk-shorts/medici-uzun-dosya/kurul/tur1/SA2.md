# SA2 — Sanat ve üslup · Mercek: DÖNEM / GELENEK UZMANI (Trecento–Quattrocento Floransa görsel kültürü)
Kurul Turu 1 · Medici Parça 1/7 · son render + kapak + yayın paketi kapısı · Bağımsız ilk bakış

## 1. Karar
**RED — 5/10** (eşik ≥9). Alan puanıdır; "iyi niyetli" şişirme yok.

Gerekçe: üslup dili (fresk/defter/punzonato altın/giornata sıva, Gozzoli alay friz dili, yeşil çuhalı banka tezgâhı, gerçek kıyılı harita) **dönem duyusu olarak güçlü ve tutarlı**. Ama "dönem doğruluğu" kapısı hiç kurulmamış: aynı varlıklar 1252'den 1743'e hangi yıl olursa olsun aynı biçimde çiziliyor. Sonuç: **4 engelleyici** (hepsinin düzeltmesi ucuz), 8 önemli, 15 küçük bulgu. Engelleyiciler kapanırsa ve önemlilerin çoğu çözülürse alan 8,5–9'a çıkar; Medici serisinin kalan 6 parçası için asıl çözüm motorda bir "çağ (era) katmanı" kurmaktır (bkz. §5).

En ağır tek bulgu: **Brunelleschi kubbesi 1338, 1348 ve 1378 görsellerinde var** (6 çekim, ≈35 sn). Kubbe 1420–36'da yapıldı; kullanıcının "tek hata kabul etmem" çizgisinde yayın bu haliyle çıkmaz.

## 2. Ne gördüm / neye dayandım
**Sınır (açık söylüyorum):** videoyu oynatamadım, sesi dinleyemedim. Hareket/akış değerlendirmesi yapmadım (SA1/animasyon alanının işi). Yalnız duran kareler, kod ve belgelerle baktım. Ayrıca web'e erişemedim (`en.wikipedia.org` oturumun izinli alan adlarında değil, WebFetch `ENOTFOUND`); bu yüzden tarih/arma iddialarını kendi bilgimden veriyorum ve güven düzeyini yanında yazdım. Doğrulanamayanları "TEYİT" etiketledim.

Bakılanlar:
- `out_p1/medici_P1.mp4` üzerinden **qa_flow tablosundaki 95 çekimin tamamından ortası** (ffmpeg, 960 px) + **19 tam çözünürlüklü kare** (139.3, 143.2, 161.7, 187.6, 220.1, 231.2, 243.7, 277.9, 282.6, 289.3, 349.2, 468.5, 588.6, 589.2, 592.5 sn vb.). Zaman damgaları `qa_flow_ozet.txt` çekim tablosuyla birebir (program süresi 594,88 sn + 7 sn bitiş ekranı = 601,88 sn video).
- Hazır paket: `genel_01…04.png`, `qa_flow_ozet.txt`.
- Kod/belge: `cilt_city.py` (Duomo/çan kulesi), `cilt_props.py` (`BALLS`, `arms_array`), `cilt_anim.py` (`FLAGS`, `flag_sprite`, `procession_cast`), `cilt_medal.py` (`INSCR`), `cilt_kinds3.py` + `c0_kinds.py` (harita poligonları), `cilt_build.py` (kubbe yapım), `cilt_deniz.py` (yıl-farkındalıklı tek örnek), `heraldry.py`, `scenes_c1.py`, `scenes_c2.py` (`YIL_AT`), `scr_c2.py`, `notlar_c1.md`, `yonetmen_c1.md`, `arastirma/M2…` (1465 notu), `brif/c1_brif.md`.
- Kapak ve yayın paketi dosyalarına bu raporda bakmadım (SA2'nin mercekle ilgili kısmı: kapaktaki arma/kubbe kontrolü ayrıca yapılmalı; bkz. §6).

## 3. Sıralı düzeltme listesi
Koordinatlar 1920×1080, ±25 px. Zaman damgaları çekim başlangıcı–bitişi (sn). **Düzeltmelerin hepsi küçük kod değişikliğidir; "engelleyici" ağır yeniden iş demek değil, "bu düzelmeden yayına çıkılmaz" demektir.**

### ENGELLEYİCİ

**B1 · Tamamlanmış Duomo kubbesi (fener, haç) ve tam boy Giotto çan kulesi, kubbenin yapılmadığı yıllarda.**
Kubbe 1420–36 (kabuk), fener 1446–61, top-haç ≈1471; çan kulesi 1359 dolayında tamamlandı, 1338'de yalnız alt katları, 1348'de yarım (veba yapıyı durdurdu) [güven: yüksek]. 1378'de kubbe yok (kubbe formu 1367 civarı maketle kararlaştırılmış, inşa edilmemiş). Yani aşağıdaki 6 çekimde **görüntü yanlış olgu söylüyor**; üstüne serinin c4 bölümü ("Kubbe ve Kefaret") kubbeyi ayrı bir olay olarak anlatacak, P1 onu baştan "spoiler" ediyor.

| # | Çekim (süre) | Yıl rozeti | Kubbe/kule konumu | Yapılacak |
|---|---|---|---|---|
| 23 | `p1_sehir` 139,3–146,3 | 1338 | kubbe+fener x≈300–590, y≈150–470; çan kulesi x≈700–790, y≈250–510 | Kubbeyi kaldır; çan kulesini alt 1/3 + iskele |
| 29 | `p1_skyline` 184,6–190,0 | 1348 (gri-mavi) | kubbe x≈1000–1215, y≈315–585; çan kulesi x≈1285–1345, y≈420–620 | Kubbesiz Duomo; çan kulesi yarım |
| 39 | `p1_sehir` 228,2–233,6 | 1378 | kubbe x≈305–630, y≈370–590 (başlık levhası altında) | Kubbeyi kaldır (çan kulesi tam kalabilir) |
| 41 | `p1_sehir` 240,6–246,3 | 1378 | kubbe+fener x≈345–630, y≈150–470; çan kulesi x≈735–830 | Kubbeyi kaldır |
| 42 | `p1_sehir` 246,4–253,2 | 1378 | sol alt: küçük kırmızı-beyaz kubbe+fener, başlangıçta x≈450–610, y≈600–740 (crane up ile çıkar) | Kubbeyi kaldır |
| 46 | `p1_skyline` 279,9–284,9 | 1378 (kızıl yıkama) | kubbe x≈1045–1260, y≈325–535; çan kulesi x≈1327–1386 | Kubbesiz |

Düzeltme önerisi (en ucuzdan): (a) `cilt_city.draw_dome` çağrısını yıl<1420 iken atla, yerine alçak çatılı katedral gövdesi (`draw_nave` zaten var) + Vaftizhane sekizgeni çiz; çan kulesi yüksekliği `h`'yi yıla göre ölçekle; (b) ya da motorda zaten bulunan `build="dome"` ilerleme durumunu (`cilt_build.py`, p=0→1) skyline'a yeniden kullan. Tanınırlık için Palazzo Vecchio kulesi + Vaftizhane + (yarım) çan kulesi üçlüsü yeter. Yeniden render: yalnız bu 6 çekim.

**B2 · Alayda ve kalabalıkta "Medici sancağı": yanlış arma biçimi + yanlış atıf (1378).**
`FLAGS` listesinden **rastgele** seçilen sarı-kırmızı "medici" sancakları (altı daire 2×3 sekizgen/rozet düzeninde; mavi top yok; gerçek arma düzeni değil) 1378 sahnelerinde taşınıyor:
- 217,2–222,4 (`p1_procession`): x≈100–270,y≈230–360 · x≈600–750,y≈255–365 · x≈1005–1130,y≈295–390 · x≈1370–1490,y≈215–300.
- 228,2–233,6 (`p1_sehir flags="medici"`, Salvestro): x≈40–1050, y≈590–780 (6–7 sancak).
- 275,6–279,8 (`p1_procession` "loncaların milisleri"): x≈130–375, y≈225–395 (+ ekran dışı).
Sorun iki katlı: (i) cihaz Medici armasının hiçbir tarihsel biçimine benzemiyor (toplar kenar boyunca, `in orlo`; rozet değil) [güven: yüksek, kesin sayı değil]; (ii) 275,6–279,8'de anlatı "loncaların milisleri isyanı ezdi" derken Medici sancağının milisin başında görünmesi atıf hatası (Medici o yıllarda dışlanan taraftı; kendi `brif/c1_brif.md` §5.5 bunu "ironi" diye anıyor).
Düzeltme: `FLAGS` rastgelesini sahne bazında **izin listesine** çevir: 1378 alayı = `lily` (kırmızı zambak/beyaz: komün), `cross` (kırmızı haç/beyaz: popolo), `plain`; "medici" cihazını 1378 alaylarından çıkar. Salvestro çekiminde (228,2) sarı sancağı **düz altın** yap (225,6'daki `p1_tree` zaten düz altın kalkan kullanıyor: aynı özen).

**B3 · Mavi toptaki Fransız zambağı (1465 sonrası biçim) 1465 öncesi yıllarda.**
Proje kendi araştırmasında bunu biliyor (`M2:K29`: "Louis XI, Medici armasına Fransız zambağı hakkı verir 1465", HAFIZA-O) ama arma sabit 1000×1000 görüntü (`cilt_props.BALLS`, mavi top + 3 zambak) ve yıl parametresi yok. Dönem içi kimlik gösteren üç yerde:
- 154,2–167,9 (`c1_agi`, **1338**): "Medici ✗" çarpılı arma, x≈85–370, y≈150–435.
- 284,8–293,0 (`c1_kademe`, **1378**): "MEDİCİ" basamağında arma, x≈835–990, y≈535–705.
- 347,6–350,6 (`chapter_card`, bölüm II, **1397–1429**): arma x≈345–630, y≈365–680.
(Geçişte iris nesnesi olarak 293 sn civarı 1378 rozetinde tekrar görünür; geçiş bağlayıcısı olduğu için kabul edilebilir.)
Meşru kullanımlar (dokunma): 1737 duvar armaları (≈9–13 sn; 26,2–29,5 sn; 49,4–54,3 sn), Machiavelli mührü (1520'ler), ana başlık 104,8, bitiş 598,8 (marka işareti).
Not: sayı ve dizilim de değişir; **8 civarı top 14. yy sonu–15. yy ortası kayıtlarında sık görülür, 6'lı düzen sonraya oturur** [güven: orta; TEYİT: Palazzo Vecchio/Bargello stemma'ları, Pastoureau]. Bu yüzden kesin sayı iddia etmeden en güvenli çözüm: 1465 öncesi için **mavi topsuz/zambaksız şematik arma** ya da (s38/s69'daki gibi) **düz altın kalkan**; şematik ise `kaynak: temsilî` dipnotuyla.
Gerekirse hakem notu: başkan bu üç kullanımı "ikon/marka" sayıp **önemli**'ye indirebilir; ama kural brif'te açık ("1465 sonrası") ve düzeltme bir saatlik iş.

**B4 · Kosimo madalyasında "PATER PATRIAE" yazısı 1429 çekiminde.**
584,7–589,5 (`p1_medal`, rozet 1429, "37 yaşındaydı" kartı): madalya kenar yazısı `COSMVS · MEDICES · PATER · PATRIAE ·` (`cilt_medal.py:29`). "Pater Patriae" unvanı Cosimo'ya **ölümünden sonra, 1464'te** verildi [güven: yüksek]. Yazı madalyanın üçte ikisini kaplayan kenarda okunabilir: coin x≈320–950, y≈170–820.
Düzeltme: P1 için `INSCR["m_cosimo"] = "COSMVS · DE · MEDICIS ·"` (ya da `COSMVS · MEDICES ·`); "PATER PATRIAE" yalnız ≥1464 bölümlerinde.
(Ayrıca bkz. Ö6: "37 yaşındaydı" sayacı son değeri; mid-frame'de 37 görünüyor, final değeri 39/40 olmalı; SA1/kaynak alanı teyit etsin. Cosimo 27 Eylül 1389'da doğdu: Şubat 1429'da 39.)

### ÖNEMLİ

**Ö1 · Yıl rozeti "anlatı saati" gibi davranıp olgularla çelişiyor.** Rozet yalnız konuşulan yıllarla ilerliyor (`scenes_c2.py:230 YIL_AT`: 1402→1415→1427→1429), içerikle sınanmıyor:
- 436,6–449,9 (`c2_borc`): rozet **1402**, kartta "XXIII. JOHANNES, PAPA" (Cossa 1410'da papa seçildi, 1415'te indirildi). → `c2s15 "papa"` için 1410 adımı ekle.
- 457,6–491,3 (≈34 sn, 5 çekim): rozet **1415**; oysa mezar (Cossa 29 Mayıs 1415'te indirildi, 22 Aralık 1419'da öldü; anıt 1420'lerde), **V. Martinus (1417'den itibaren; kartta 469,8–482,4)** ve "1420'lerin başından" (482,4–487,1). → `c2s18 "öldü"` için 1419, `c2s21 "1420'lerin"` için 1420 adımı ekle. Aynı mantıkla Cenova 1340 / Pacioli 1494 zaman çizelgesi çekimlerinde (421,0–428,9) rozeti kıs ya da gizle.
Öneri: `qa_donem` lint'inde kart adı + rozet yılı sınaması (§5, İyileştirme 2).

**Ö2 · 1378 isyanı "Gozzoli Magi alayı" kadrosuyla çiziliyor.** 217,2–222,4: kumaşlı (brokar) örtülü atlar, soylu atlılar, mazzocchio/sarıklı şapkalar; "öfke sokakta" ile yün işçilerinin (Ciompi) **kaba giysili, topraktan** gelen kalabalığı yerine 1459–61 saray alayı okunuyor. `procession` docstring'i bunu bilerek "Gozzoli Magi alayı üslubunda" kuruyor; 241 sn'deki `riders=0` doğru yön. 217 sn çekimine `riders=0`, `mix=dict(common=.5, guard=.3, banner=.2)` ver; mazzocchio (15. yy modası) 1378 kadrosundan çıkar.

**Ö3 · "Hesap okulları" çekiminde boncuklu abaküs ve yeşil kara tahta.** 146,2–154,2: tel üzerinde boncuk dizisi (Rus/Çin tipi) yeşil tebeşir tahtası x≈565–845,y≈225–320. 14. yy Floransa "abbaco" okulu Hint-Arap rakamlarıyla yazılı hesap öğretir (Fibonacci mirası); Avrupa'da sayma tahtası çizgili zemin + jeton idi, boncuklu çerçeve ve yeşil kara tahta yok [güven: yüksek]. Üstelik anlatılan nokta "defterlerin şehri". → Çizgili sayma bezi + jeton + kâğıtta "1 2 3 4" rakamları; tahtayı ahşap/balmumu tablete çevir.

**Ö4 · 1252 (ve 1338/1348) 15. yy ortası kıyafetle giydirilmiş.** 110,1–115,6 (pano): çorap/ters renkli (mi-parti) pantolon, kısa üstlük, çok desenli brokar elbiseler, tenteli/yeşil-beyaz çizgili pazar tentesi; 129,2–139,3 (darphane): zambak desenli üstlük, sivri tüylü şapka. 1252 için uzun cotta/surcot, cappuccio ve sade başlık beklenir; mazzocchio ve parti-colored hose 1400'lerden sonra. Kitte hazır bir örnek var: `cilt_deniz.person_style(variant, year, …)` (1533 bereli, 1600 yüksek şapka). Aynı mantık Floransa çağları için yazılabilir (bkz. §5 İyileştirme 1). Dönem estetiği "stil" kararı olarak kabul edilebilir; ama **1252'yi** 1450'ye çevirmek en uç nokta, burada düzelt, öbürlerini küçük say.

**Ö5 · "Büyük Dukalık" haritası: temsilî çokgen etiketsiz.** 64,9–69,3 (rozet 1737; kare 67,3): çokgen `c0_kinds.TOSKANA` (≈1570 yaklaşık, kıyıya kırpılmış). Dışarıda bırakılması gerekenler içeride/eksik: Lucca Cumhuriyeti ve Massa-Carrara (bağımsız), Stato dei Presidi (Orbetello vb., İspanya/Napoli), Piombino; köşe (12.30, 43.30) Umbria/Papalık topraklarında; Elba'nın Portoferraio'su dışarıda (kadrajda ada boş kalıyor) [güven: orta-yüksek]. Notlarda "temsilî" yazıyor (`notlar_c0.md`) ama ekranda `approx=False` ile uyarı kapalı. Düzeltme: `approx=True` ya da küçük "TEMSİLÎ SINIR" etiketi; çokgenden Presidi'yi ve Lucca/Massa'yı çıkar. (Kıyı çizgileri Natural Earth gerçek veri; harita tabanı güvenilir.)

**Ö6 · Cosimo "37 yaşındaydı" kartı (587,3 kare; sayaç yükselirken).** Cosimo Şubat 1429'da 39'du; anlatı "kırk yaşına yaklaşıyordu" diyor. Final değerin 39 olduğunu `scenes_c2` sayaç hedefinden doğrula; 37 ise düzelt. (Küçük: "1389 DOĞUMLU · HESAPLA" altyazısı iyi.)

**Ö7 · Peruzzi'ye atfedilen mavi-beyaz şeritli kalkan.** 176,6–184,6 (`c1_kardes`): "Villani'nin kardeşi: Peruzzi'de çalışıyordu" kartında kalkan x≈1415–1560, y≈240–420 (`_shield(... "bars")`). Peruzzi'nin gerçek armasının bu olduğuna dair `kaynaklar_P1.md` ya da `arastirma/` içinde kayıt yok. **TEYİT**: kayıt çıkmazsa kalkanı şematik (tek renk, işaretsiz) yap ya da kaldır; uydurma arma "gerçek aile armasıymış gibi" okunur.

**Ö8 · 1429 kapı çekimi: kubbe yarım, fener/haç yok olmalı.** 589,5–594,9 (kare 589,2): kubbe+fener+haç x≈345–670, y≈500–930. 1429'da kabuk hâlâ inşa halinde (kapanış 1436), fener 1446'da başlar, top-haç 1471. Çözüm: `build="dome"` p≈0.55 durumu ya da kubbeyi kadrajdan çıkar (çan kulesi/Palazzo Vecchio hikâyenin kendisi, kubbe zaten c4'ün konusu).

### KÜÇÜK

| # | Zaman / konum | Bulgu | Öneri |
|---|---|---|---|
| K1 | 78,0–86,6 ("BUGÜN · UFFIZI", kare 82,7) | Uffizi avlusu yuvarlak kemerli revak; gerçek revak düz arşitravlı sütun/payandalı (kemer yalnız Arno ucundaki serliana'da) | `cilt_build` `uffizi` revakını kullan ya da kemerleri düz lento yap |
| K2 | 391,8–397,9 ("faiz değil hediye") | Kurdeleli modern hediye kutusu (kırmızı kutu + altın şerit) | Çuval/kese/mühürlü kutucuk |
| K3 | 324,6–331,2 (`c1_kose`) | Orsanmichele plan simgesi dört sütunlu Yunan tapınağı (x≈1490–1620,y≈70–170 sağ üst); bina dikdörtgen bloktur, ışıklı niş cephe | Kare blok + niş sıraları simgesi |
| K4 | 457,6–469,8 (mezar çekimi, Martinus mührü x≈1460–1620, y≈240–400) ve 482,4–487,1 (`p1_emblem`): çapraz anahtarlar; 436,6–449,9 Cossa'nın üstünde yüzen beş uçlu **taç** | Papalık anahtarlarında halka (bow) altta, diş (ward) yukarıda olur; burada tersine. Papa için taç değil üç katlı **tiara** (469,8'deki Martinus silueti konik: doğru) | Anahtarları çevir; Cossa'ya tiara |
| K5 | 205,3 (`p1_oda` 1348 kütüphane), 340,2–357,5 (banka salonu 1397–1402), 353,7, 401,0 | Renkli ciltler **sırt dışarı** dizili; 14. yy sonu/15. yy başında kitaplar yatık, enine kenar ön yüzde ya da sandıkta durur (sırt dışarı dizme 16. yy) | Yatay istif + sandık/defter rafı |
| K6 | Pencereler: 192,5 (1348), 253–260 (1378), 383,5 (1397) | Baklava kafesli kurşun camlı pencere; 1348 evlerinde yağlı bez/ahşap kepenk daha doğru | `draw_window` desen seçeneği; ya da kabul |
| K7 | Siluet kiti: 192,5–196,5, 200,1–204,1 (adam), 261,5–275,6, 544,5–557,5 | Siluetlerin çoğu geniş kenarlı yassı şapka/uzun frak: 17. yy görünümü; 14.–15. yy için kapüşon/cappuccio, berretta (Machiavelli için) | Siluet kiti `hat` parametresini çağa göre seç |
| K8 | 233,6–240,6 (21 lonca) | Zırh-kalkan ızgarası **uydurma** işaretlerle (haç, yıldız, halka); gerçek loncaların (Calimala: balyayı tutan kartal; Lana: kuzu; Cambio: kırmızı zeminde florin) tanınır simgeleri var. brif "yalnız Calimala, Lana, Cambio vurgulu" diyor ama ekranda vurgu yok | Üçü için gerçek simge (TEYİT), kalanı soluk/şematik; ya da "şematik" notu |
| K9 | 121,3–129,2 (lanetli çiçek) | Mor **süsen**: Floransa zambağı kırmızı (komün armasında) ya da beyaz süsen; ekran mor; ayrıca 139,3'teki sancaklardaki Floransa zambağı Fransız fleur-de-lis'e çok benziyor (Floransa giglio'su taç yapraklar arasında etamin taşır) | Rengi kırmızı/beyaz; etamin ekle |
| K10 | Madalya portreleri 296,6; 439–443; 509,8; 535,7; 587,3 | Portre madalyası sanat biçimi 1438 (Pisanello) sonrası; 1378–1429 çekimlerinde "nesne" olarak yanlış (görsel gösterge olarak kabul) | Köşeye "temsilî portre" notu ya da siluet |
| K11 | 3,8–32,1 (1743–1737 odaları) | Salon/taht gotik-erken Rönesans (sivri kemerli taht x≈430–560,y≈630–880; goblen; baklava kafesli pencere) 1737–43 Pitti'nin geç barok iç mekânı yerine | Kimlik kararı olarak kabul; taht için `variant="taht"` baldaken seçeneğini dene |
| K12 | 457,6–469,8 (Cossa mezarı) | Düz lahit; gerçeği Donatello-Michelozzo duvar anıtı (yatan tunç figür, kemer, perde). Rozet 1415 (anıt 1420'ler) | Hafif dekor: gisant + perde |
| K13 | 240,6–246,3 (Ciompi, `flags="stripes"`) | Mavi-sarı çizgili Ciompi sancakları (`yonetmen_c1.md` L25 "mavi-sarı sancaklar") için kaynak notu yok | Kaynak koy ya da "stilize" damgası; Adalet Sancağı için TEYİT |
| K14 | 358,5–364,4 ve 368,1–375,8 (kambiyo haritası) | "BRUGGE" etiketi kadrajın üst kenarında yarım ve "2. POLİÇE" yazısıyla üst üste (x≈1360–1450,y≈40–60) | Kamerayı 40–60 px aşağı al (SA1/tipografi ile de paylaş) |
| K15 | 139,3 ve 240,6 | "1338"/"22 TEMMUZ 1378" başlıkları Palazzo Vecchio çan odasının üstüne biniyor (x≈850–1070,y≈150–215) | Tipografi alanına not (dönem değil) |

**Doğru bulduklarım (korunmalı; "ne yapmamalı" yönergesi olarak):** 1737 armaları 6 top + zambaklı mavi top (1737'de doğru); 1252 florin arka yüzü (S. IOHANNES B + haçlı asa); 1397–1402 banka/kambiyo masasında **yeşil çuha** (Floransa banka tezgâhı için doğru); Palazzo Vecchio Arnolfo kulesi (1310'dan beri; kule/mazgal/çan odası doğru); Floransa komün sancağı (beyaz üstüne kırmızı zambak) ve popolo haçı doğru; DEBITORI/CREDITORI başlıkları ve f./s./d. sütunları gerçek Floransa defteri düzeni; "Cenova 1340" çifte kayıt; Floransa yılbaşı 25 Mart ("20 Şubat 1429; takvimde hâlâ 1428") **doğru ve ustaca**; haritalarda gerçek kıyı verisi; Medici ailesi başka kol için **düz altın kalkan** (225,6) ve defter bağında düz kalkan: arma konusundaki en doğru karar; siluetlerde 1737 peruk; ana başlık/bitişte marka arması olarak 6 top.

## 4. En emin olmadığım nokta
1. **Medici armasının dönem içi sayı/dizilimi** (hangi on yılda kaç top, hangi düzen). Brif'in 1465 zambak kuralını ve genel bilgimi kullandım; web doğrulaması yapamadım. Bu yüzden B3 düzeltmesini "sayı iddia etmeyen şematik/düz kalkan" olarak önerdim, "doğru 8'li arma çiz" demedim.
2. **Peruzzi kalkanı** (Ö7) ve **21 lonca simgeleri** (K8): kaynakta arma tarifi yok; doğrulayamadım.
3. B3'ün ve Ö1'in şiddeti: başkan "ikon/anlatı saati" gerekçesiyle önemliye çekebilir; ben kuralı katı okudum.
4. Ö3 (abaküs) ve K1 (Uffizi revakı) kendi bilgime dayanıyor; kaynak taraması yapmadım.

## 5. Motor sorusu — "Bu motor dönem doğruluğu ve temsil gücü açısından yeterli mi?"
**Yetersiz değil ama kontrolsüz.** Motorun *dili* (punzonato altın zemin, giornata sıva, Gozzoli alayı, yaldızlı yazı, balmumu mühür, gerçek kıyılı harita, `build="dome"` yapım animasyonu, banka tezgâhı) dönem temsili açısından kanalın Sisifos hattından belgesel bakımdan zengin; Sisifos'un kapalı bir motif repertuvarı vardır (vazo resmi: zamansız mit, birkaç nitelik), Medici ise 1252–1743 arasında 5 asır değişen maddi kültür ister; Sisifos hattında hiç gerekmemiş olan **"yıl → varlık" kapısı burada hayati** ve yok. Somut bulgular: (1) Duomo, çan kulesi, Palazzo Vecchio **sabit son hâl** (`cilt_city.draw_dome/draw_campanile` → `skyline`, `pano florence`, `sehir meydan/skyline_dikey/kale` hep koşulsuz çağırıyor; yalnız `liman(year=…)` ve `person_style(variant, year,…)` yıl alıyor); (2) Medici arması sabit sabitler (`cilt_props.BALLS`, `arms_array(size, field, flat)` yalnız alan ve düzlük parametreli) ve **aynı arma üç ayrı çizimde** (arma görüntüsü, `flag_sprite("medici")` 2×3 daire, `PALLE_POS` mühür) birbirine bağlı değil; (3) `heraldry.py` başka projeden (Habsburg/Kastilya/Aragon/Burgonya/Fransa/Osmanlı/Papalık/Luther-Tudor) ve Floransa'ya özgü hiçbir arma/lonca simgesi yok; Peruzzi/lonca kalkanları `c1_kinds._shield(c1,c2,charge)` ile anlık uydurulmuş; (4) rozet yılı yalnız söylenen yıl sözcüklerinden ilerliyor; `qa_flow`'un 11 kapısı **tamamı akış/ritim**; dönem/içerik kapısı sıfır; (5) madalya yazıları (`INSCR`) yıla bağlı değil; (6) harita çokgenleri yalnız ~1450 ve ~1570 için (1252/1338/1378/1737 yok), poligon `approx=False` ile uyarısız. Yeniden yazma ya da başka motora geçme **gerekmez**: parametrik kod bu bulguların hepsini düşük maliyetle düzeltebilir (yalnız etkilenen çekimler yeniden render; bu rapordaki B1–B4+Ö1–Ö8 ≈ 25–30 çekim (rozet adımları dahil) ≈ 3–4 dk görüntü ≈ 5000–6000 kare; kare başına ≈0,2 sn ve 4 işçiyle ≈ 5–8 dk + kodlama/miks; toplamda <30 dk).

**En yüksek getirili 3 iyileştirme**
1. **Çağ (era) katmanı:** `era.py` ya da `ERA(year)` tablosu + çekim parametresi `year=` (HUD yılından otomatik). Kapılar: Duomo durumu (<1420 kubbesiz alçak çatı; 1420–36 kabuk ilerlemesi `cilt_build` kubbe durumunu paylaşır; ≥1446 fener; ≥1471 top-haç), çan kulesi yüksekliği (1338/1348/≥1359), Medici arması varyantı (≤1464 şematik/düz, ≥1465 zambaklı), sancak izin listesi, kıyafet ön ayarı (1250'ler / 1340'lar / 1380–1430 / 1430+; `person_style` örneğiyle), pencere camı, kitap istifi. **Maliyet: 1,5–2 gün geliştirme** (4–5 çağrı yeri: `cilt_city`, `cilt_props`, `cilt_anim.FLAGS`, `cilt_medal`, `c1_kinds`) + bu raporun düzeltmeleri için yeniden render <30 dk. En büyük getiri: P2–P7 (1434→1743: kubbe inşası c4, 1478, 1494, Büyük Dukalık) aynı hataları tekrarlamasın.
2. **`qa_donem` lint'i** (qa_flow'a 12. kapı): çekim tablosundaki rozet yılı × kullanılan varlıklar (arma varyantı, kubbe durumu, madalya yazısı, "V. Martinus" gibi kişi+unvan tarih aralıkları: Cossa/Johannes XXIII 1410–15, Martinus V 1417–31, Pater Patriae ≥1464) sınaması; rozet yılı olay yılı ile ≥5 yıl sapıyorsa FAIL. **Maliyet: 0,5–1 gün** (≈40 satırlık geçerlilik tablosu + 80 satır kod); yayın öncesi ücretsiz sigorta.
3. **`heraldry_flo.py` (Floransa arma/simge kütüphanesi):** komün zambağı (kırmızı/beyaz, etaminli), popolo haçı, Medici varyantları (yıl aralığı + `kaynak` + `teyit` bayrağı), 7 büyük lonca simgesi, Albizzi/Strozzi/Pazzi/Peruzzi/Bardi kalkanları; **teyit edilmemiş arma ekrana yalnız "şematik" modunda çıkar**. **Maliyet: 1–2 gün + kaynak araştırması süresi** (dış doğrulama olmadan kalkanlar uydurma kalır; bu araştırma web/kütüphane erişimi ister).

Dürüst zayıf yerler: "stilize" gerekçesi şu an tek bir sihirli kelime; hangi hatanın bilinçli stil, hangisinin yanlış olgu olduğunu ayıran bir listeye bağlı değil. `notlar_c1.md` L48 ("palle sayısı/biçimi ... stilize") bunu sorunu fark edip dipnota gömme örneği. Çözüm: stil kararı **belgelenmiş çağ tablosu** olsun, "stilize" özgürlüğü kapı sayılmasın.

## 6. Kapak / yayın paketi için dönem notları (bu turda dosyalara bakmadım)
Kapak A/B/C (`kapak_P1_A/B/C.jpg`) ve `YAYIN_TASLAK.md` ayrı üyelerde; dönem merceği olarak yalnız şu kontrolü öneririm: kapaklarda (i) Duomo kubbesi/skyline kullanılmışsa yıl ile çelişmesin (kapak yıl iddiası taşımaz, kubbe orada serbest ama 1252/1348 yazısıyla birlikte olmasın); (ii) 1465 öncesi iddiası taşıyan "arma" yerine marka arması (6 top) yalnız logo olarak; (iii) florin yığını kapağında florin yüzü/yazısı doğru (S. IOHANNES B / FLORENTIA).

## 7. Tur 2 için doğrulama listesi (başkana)
B1 (6 çekimde kubbe yok + çan kulesi yüksekliği), B2 (1378 alay/kalabalıkta Medici cihazı yok), B3 (1338/1378/1397 armaları şematik/düz), B4 (`INSCR["m_cosimo"]`), Ö1 (YIL_AT adımları 1410/1419/1420), Ö2 (217 sn kadro), Ö3 (abaküs), Ö4 (1252 kıyafet), Ö5 (`approx=True` + çokgen), Ö6 (sayaç son değeri), Ö7 (Peruzzi kalkanı teyit ya da kaldırma), Ö8 (1429 kubbesi). Düzelmeler yeniden render edildikten sonra aynı 95 ortası-kare tarama + 6 B1 çekimi tam çözünürlükte aynı üyeyle geri kontrol.

Telif/temsil sınırı notu: Gozzoli/Pisanello/punzonato altın dili 15. yy kamu malı dil, kodla yeniden çizim; gerçek eser kopyası yok. Portreler jenerik stilize (benzerlik iddiası yok; `cilt_medal.py` açıkça yazıyor); Anna Maria Luisa ve diğer kişiler siluet. Natural Earth (kamu malı, lisans dosyası var). Telif/hukuk açısından bulgu yok; sorun tamamen dönem doğruluğu.
