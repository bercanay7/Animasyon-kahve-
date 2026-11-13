# TE2 — Teknik kalite · Erişilebilirlik / Okunurluk — Medici Parça 1 · TUR 2 (v2)

Üye: TE2. Mercek: telefon, TV, aydınlık ve karanlık ortam. Tur 1 raporum: `kurul/tur1/TE2.md`.

**Sınırlarım:** videoyu oynatamadım, sesi dinleyemedim. Hareket ve süre yargılarım kare dizilerine ve ölçüme dayanıyor. Ekranda kalma süresi ile okuma süresini yalnız örnek karelerle karşılaştırdım.

---
## 1. Karar

**RED: 8,6 / 10.** Eşik ≥9; tur 1 puanım 7,0'dı.

Alt puanlar (tur 1 → tur 2):

| Alan | Tur 1 | Tur 2 |
|---|---|---|
| Fotosensitivite | 10 | 10 |
| SRT | 8,5 | 9,0 |
| Yerleşim, kenar payı, HUD | 5,5 | 8,0 |
| Kontrast ve punto | 6 | 8,5 |
| Karanlık ve aydınlık ortam | 6,5 | 9,0 |
| Kapak | 7 | 9,5 |

**Ne iyileşti:**
- Tur 1'in üç engelleyicisi (E1–E3: kesilen ve HUD altında kalan adlar) kapandı.
- Anahtar yazıların hepsi okunuyor: 31 EKİM 1737, nakarat, FLORANSA, bitiş ekranı.
- Kontrast medyanı 6,9:1'den 8,8:1'e çıktı. Okuma hızı 17 kar/sn'nin üstüne çıkan altyazı repliği kalmadı.
- Çukur çekimi aydınlandı. Kapaklar kanal çıtasında.

**Neden eşiğin altında:** beş yerel "önemli" hata var (Y1–Y5). Üçü düzeltmelerin getirdiği yeni hata:
- levha üstüne levha;
- altyazı bandında yeni bir etiket;
- yazı üstüne yazı.

İkisi kalan hata:
- 22 px'lik ve üstünden çarpı geçen "1426'DA ÇEKİLDİ";
- otomatik zeminin dışında kalan kaynak sınıfı damgaları.

**ONAY'a yol:** Y1–Y5, Ö5'in kalan kısmı (KUR FARKI) ve SRT'deki iki bölünme düzelsin, yaklaşık 7 çekim yeniden render edilsin. O zaman **9,3 ONAY** veririm. Gerileme kontrolünü tek üye olarak yapabilirim.

---
## 2. Ne yaptım ve neye dayandım

Tur 1 betiklerimi v2'ye karşı yeniden koştum. Aynı anda tek ağır işlem çalıştırdım, render yapmadım. Betikler: `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/te2_t2/` (`lumseries.py`, `flash.py`, `audit_v2.py`, `layout_v2.py`, `contrast_v2.py`, `srt_an.py`).

- **Flaş ve karanlık:** v2'nin 14.365 karesinin tamamı 192×108'e indirildi. Her kare için WCAG göreli parlaklığı ve 4×4 bölge ızgarası çıkarıldı; doygun kırmızı alan payı da ölçüldü.
- **Yazı kutuları:**
  - Motorun yalıtılmış bir kopyasını scratch'e aldım; proje dosyalarına yazmadım.
  - 106 çekimden her birinde 3 kare, toplam 318 kare çizdirdim.
  - `drawTextBlob` ve `draw_spr` sarmalayıcılarıyla 3.553 yazı kaydının ekran kutusunu, puntosunu ve rengini topladım.
- **Gerçek piksel kontrastı:**
  - 252 zaman noktasında videodan kare çıkardım.
  - 608 yazı örneğinde yazı ile arkasındaki pikseller arasındaki WCAG oranını ölçtüm (yüzdelik yöntemi).
  - 24 damga ve yaldız sprite'ını ayrıca ölçtüm.
- **Hedefli kareler:** tur 1 maddelerinin zamanlarında yaklaşık 100 tam çözünürlüklü kare.
- **SRT:** `yayin/medici_P1_tr.srt` ayrıştırıldı. 05.11 01:47 tarihli dosya, analiz ettiğim içerikle aynı (md5 eşit).
- **Kapaklar:** 05.11 01:56'da yeniden üretilen K1/K2. Testler: 246/168/120 px, gri, koyu ve açık zemin, kenar griliği, süre rozeti bölgesi.
- **Okuduklarım:**
  - Kurul: `KURUL.md` (tur 2), SA1/SA2 tur 2 raporları (çapraz bakış için).
  - Notlar: `notlar_hareket.md`, `notlar_c0–c2.md`.
  - Denetim çıktıları: `qa_yerlesim.json`, `out/qa_flow.json`.
  - Kod: `cilt_medici.py` (`contrast_scrim`, `ink`, `kick`, `name_plate`).

### Ölçüm özeti (v1 → v2)

| Ölçüt | v1 | v2 |
|---|---|---|
| Yazı örneklerinde kontrast medyanı | 6,9:1 | **8,8:1** |
| Örneklerin <4,5:1 payı | %30 | **%17** |
| Benzersiz yazıların en iyi anında <4,5:1 | %25 | **%14** (çoğu dekoratif belge numarası, zaman ekseni ya da geçiş anı) |
| Punto boyuna göre WCAG'de kalan benzersiz yazı | — | 32/278. Gerçek okuma sorunu: zaman ekseni (K5) ve takvim yaprağı. Damgalar ve KUR FARKI bu ölçümün dışında; ayrı ölçtüm (Y5, Ö5) |
| En küçük yazı | 25,2 px | **22,3 px** (yeni: "1426'DA ÇEKİLDİ") |
| 34 px'ten küçük benzersiz yazı | Örneklerin %37'sinde en küçük yazı <33 px | %13 (46/343). Örneklerin %17'sinde en küçük yazı <34 px |
| Flaş: 1 sn içindeki dönüm noktası (WCAG eşiği 6) | genel 2, bölgesel 5 | **genel 2, bölgesel 4** (506,2 sn) |
| Doygun kırmızı alan | <%2 | azami %0,8 |
| Kare ortalaması <0,03 olan süre | ≈11,4 sn | **6,8 sn** |
| SRT: replik / ort. kar/sn / azami | 166 / 13,8 / 18,7 | **158 / 14,0 / 17,0** |
| 17 kar/sn'yi aşan replik | 15 | **0** (7 replik tam 17,0) |
| Yetim replik (≈1,07–1,16 sn) | 11 | **0** (en kısa 1,21 sn) |

---
## 3. Tur 1 maddelerinin durumu

Koordinatlar 1920×1080 ekran uzayındadır.
- HUD: x 1548–1848, y 72–138.
- Altyazı bandı: y 938–1042.
- Güvenli alan: x 90–1830, y 60–1020.

| Madde | Durum | Kanıt (v2) |
|---|---|---|
| **E1** XXIII. JOHANNES taşıyor; Konstanz plakası taşıyor; Cossa plakası HUD'da | **KAPANDI** | 437 sn: "COSSA = XXIII. JOHANNES" levhası x≈465–1335, y≈190–338; yazı levhanın içinde. 442,5 sn: "KONSTANZ KONSİLİ · 1415" koyu etiket x≈254–1024, y≈154–230. Cossa levhası y≥190, HUD'dan uzak. Aynı çekimde yeni bir levha çakışması var: **Y1** |
| **E2** VILLANI'NİN KARDEŞİ HUD altında ve kenarda | **KAPANDI** | 176–179 sn: "GIOVANNI VILLANI / 1300'DE PERUZZİ ORTAĞI · ŞİRKETİ 1341'DE BATTI" levhası x≈880–1640, y≈176–320; HUD'un altında boşluk var. Rakam biçimi için Y11 |
| **E3** İki kalem çekiminde adlar kesik, HUD altında; ANEKDOT altyazı bandında | **KAPANDI** | 538 sn: MACHIAVELLİ x≈260–860, CAVALCANTI x≈1000–1600, y≈150–304. 565 sn: ANEKDOT x 1331–1670, y 812–858; "CAVALCANTI'YE GÖRE" y≈844–916. Bant ve HUD boş |
| **Ö1** "31 EKİM 1737" okunmuyor (≈1,6:1) | **KAPANDI** | 26,2–32,1 sn: koyu levha x≈1054–1524, y≈204–296, 58 px; **17,5:1** |
| **Ö2** İlk yazı üst kenara yapışık, ≈1,9:1 | **KAPANDI** | Açılış artık kapak yankısı. "18 ŞUBAT 1743" ve "FLORANSA" levhaları x≈1374–1806, y≈770–924; **20:1**. Yankının kenar payı için Y6 |
| **Ö3** Nakarat okunmuyor; ekran metni anlatımdan farklı | **KAPANDI** | 210,8 sn: "NE DÜŞÜNDÜĞÜNÜ BİLMİYORUZ" **10,6:1**. 213,3 sn: "NE GÖRDÜĞÜNÜ YAZDIĞINI BİLİYORUZ" **17,4:1**. Metin anlatımla birebir |
| **Ö4** "ESKİ PAPA" ≈2,4:1 | **KAPANDI (sınırda)** | 463,5–464,7 sn: oyma yazıt ≈60 px, **≈3,2:1**. Büyük yazı eşiği 3:1 aşılıyor |
| **Ö5** FLORANSA / GÜN / slogan / YAZILDIĞINA GÖRE / KUR FARKI | **KISMEN** | Kapananlar: FLORANSA (109,4 sn) **11,6:1**; GÜN (31 sn, 65 px) **3,65:1**; slogan "BANKA ÖLDÜ, GÜZELLİK KALDI" 102,5–104,6 sn arası **3,9–4,3:1** (yalnız belirdiği 101,8 sn'de 1,6); YAZILDIĞINA GÖRE (247 sn) koyu etiket **12,3:1**. **Açık:** "KUR FARKI" (368,8–373,4 sn) 1,8'den başlayıp en çok **2,8:1**'e çıkıyor; kambiyo açıklamasının vurgu sözcüğü ve büyük yazı eşiğinin (3:1) altında. Yapılacak: yaldızı koyulaştır ya da levha içinde koyu mürekkep kullan (≥4,5:1) |
| **Ö6** Bitiş ekranı etiketleri 1,3–1,9:1 | **KAPANDI** | 595–597,5 sn: SIRADAKİ PARÇA **12–14:1**, ABONE OL · ZAMAN KURYESİ **12–14:1**, TESLİMAT TAMAM **6,8–7,7:1**. Büyük "ZAMAN KURYESİ" ≈3,0–3,3:1; büyük yazı eşiğinde, isteğe bağlı (SA1-Y8) |
| **Ö7** Altyazı bandında öğeler | **KISMEN** | Kapananlar: BARSELONA (artık y≈850), ANEKDOT (bkz. E3), "… HANE" (alt kenar ≤920), OĞULLARI. Kalan: c0_belge madde numaraları XI–XIII 45–56 sn arasında banda giriyor; dekoratif, düşük öncelik. **Yeni bant ihlali: Y3** |
| **Ö8** Aşırı karanlık çekimler | **KISMEN** | c1_toprak (203,5–209,7 sn) ortalaması 0,008'den **0,154**'e çıktı; çukur ve toprak katmanları seçiliyor, kapandı. Hasta odası (189,7–193,7 sn) ortalaması hâlâ 0,043; 192,0–193,7 sn arası <0,03. Ruh hali çekimi; düşük öncelik |
| **Ö9** SRT | **BÜYÜK ÖLÇÜDE KAPANDI** | 11 yetim replik birleşti. 17 kar/sn üstü replik kalmadı. "doksan bin", "okuma yazma", "yüz elli bin", "yüz seksen bin", "üç buçuk", "yazıldığına göre", "bu altına", "eski bir" artık bölünmüyor. **Açık:** "İngiltere Kralı III. │ Edward'ın" hâlâ iki ayrı replikte (46/47, 2:46–2:52). Muhtemel neden: `make_srt` "III."teki noktayı cümle sonu sayıyor. Yeni bölünmeler: Y9 |
| **Ö10** Kapak okunurluğu | **KAPANDI** | K1/K2 (05.11 01:56): kahraman yüksekliği %18,3 / %22,2 (kapak QA). Benim ölçümüm: kahraman kontrastı **12,0:1 / 12,7:1**. 168 px'te kenar gri ortalaması 38 (koyu temada ayrışıyor), <25 gri payı ≈%10,5. 168 ve 120 px'te iki satır da okunuyor; gri testte yazı ve odak ayrışıyor; süre rozeti bölgesi boş (ortalama gri 26) |
| **Ö11** Punto tabanı (telefon) | **KISMEN** | Rol satırları 32'den **34 px**'e çıktı; <34 px yazı %13'e indi. Kalan küçükler: "1426'DA ÇEKİLDİ" 22 px (Y4); galeri etiketleri "KIYMETLİ ŞEYLER" 25 px, "KÜTÜPHANELER" 27 px, "MÜCEVHERLER" 30 px (56,7–64,9 sn; "KIYMETLİ ŞEYLER"in sağ ucu x≈1885, güvenli alanın dışında; "KÜTÜPHANELER" ile "MÜCEVHERLER" arası ≈15 px); zaman ekseni yılları 28 px (K5); bölüm etiketi 30 px; ağ şehirleri 30,6 px; "137 HANE" 30,4 px. 34/46 tabanı levha ve kick'te uygulanıyor, `fit_size` ile küçülen ve özel türlerdeki etiketlerde uygulanmıyor |
| **Ö12** Yabancı özel adlarda büyük harf tutarlılığı | **AÇIK** | "MEDİCİ" (her yerde) ile "SALVESTRO DE' MEDICI" (219,5–227,8 sn) aynı levhada, rol satırı "MEDİCİ AİLESİNİN BAŞKA BİR KOLU". "MACHIAVELLİ" noktalı; "CAVALCANTI", "GIOVANNI", "VILLANI", "PACIOLI", "CIOMPI", "UFFIZI" noktasız; "PERUZZİ", "BARDİ" noktalı. Yeni: KATASTO / CATASTO (Y7) |
| **K1** HUD kenara çok yakın | **KAPANDI** | HUD x 1548–1848, y 72–138: kenarlardan 72 px, eylem güvenli alanının içinde |
| **K2** Bölüm etiketi kenarda | **KAPANDI** | (96, 60), mavi levha üstünde 30 px, **11:1** |
| **K3** SRT 20 ms boşluklar | — | Sorun değildi; aynı |
| **K4** zoomthru sıklığı (vestibüler) | **KISMEN** | 20 kullanım 13'e indi; ama 6'sı 0,9 sn'den 0,5–0,6 sn'ye hızlandı (derinlik hâlâ 5,0: beş kat zum yaklaşık 0,3 sn'de) |
| **K5** Zaman ekseni yılları | **AÇIK** | 416–424 sn: 28 px, **2,9–3,5:1**; "1320" x≈21'de, "1520" sağ ucu x≈1884'te, ekran kenarında |
| **K6** Çarpı harfleri örtüyor | **AÇIK** | 370–373 sn: BORÇ ve FAİZ harflerinin üstünden kırmızı çarpı geçiyor. Aynı kalıp "MEDİCİ İCADI" (≈418 sn) ve "FAİZ" çipinde (385 sn) var; en ağır örnek Y4 |
| **K7** Pan titremesi (TE1 alanı) | — | Değerlendirmedim. Deklanşör eklendi; yazı bulanıklığını yalnız geçişlerde gördüm (ör. 307,4 sn) |

---
## 4. Yeni sorunlar (gerilemeler dahil)

**Y1 · ÖNEMLİ · Levha üstüne levha (SA1-Y3 ile aynı).**
- Yer: 432,8–434,6 sn (≈1,8 sn). "BALDASSARRE COSSA" levhası (x≈530–1270, y≈190–340), "GIOVANNI" levhasının (x≈310–730, y≈298–403) sağ üst köşesine biniyor. GIOVANNI yazısının üst kısmı ("…VANNI") Cossa levhasının alt kenarında kalıyor.
- Neden: yeni kıskaç levhayı kenarlardan ve HUD'dan kaçırıyor ama başka bir levhayla çakışmasını denetlemiyor.
- Yapılacak: Cossa levhası GIOVANNI tamamen söndükten sonra girsin. Ya da GIOVANNI levhası y≥360'a insin. Kıskaca levha–levha çakışma denetimi eklensin.

**Y2 · ÖNEMLİ · Yazı üstüne yazı, güvenli alan dışı (SA1-Y2 ile aynı).**
- Yer: 306,4–307,9 sn. "EVLİLİK ÇEYİZİ" etiketi (40 px, x≈1403–1904, y≈429–465) "1.500" rakamlarının sağ ucunun altından başlıyor ve x≈1904'e, güvenli alanın 74 px dışına taşıyor.
- Etiket tam opaklığa hiç ulaşmıyor: 306,7 sn'de alfa 0,48; 307,4 sn'de sağa kayma geçişiyle bulanıklaşıp kayboluyor.
- Neden: serbest `ink` etiketleri kıskaçtan geçmiyor; kıskaç yalnız levha ve kick için.
- Yapılacak: etiketi kaldır (levha "PICCARDA BUERI'NİN ÇEYİZİ" aynı bilgiyi veriyor) ya da "FLORİN"in altına, güvenli alan içine al.

**Y3 · ÖNEMLİ · Yeni etiket altyazı bandında.**
- Yer: ≈271,6–277,7 sn. "CIOMPI LONCASI" koyu etiketi x≈1075–1570, y≈960–996, bandın tam ortasında.
- Aynı anda 72–74 numaralı replikler ekranda ("Yün işçilerinin kısa / ömürlü loncası kaldırıldı;" …). Altyazı açıkken (kitlenin %38'i) etiket örtülür.
- Gözden kaçma nedeni: `qa_flow`'daki "Altyazı bölgesi: 0" ve `qa_yerlesim`'deki "altyazı şeridi 0" yalnız levhalara bakıyor.
- Yapılacak: etiketi y≤900'e, "ARMALAR TEMSİLÎ" hizasına al.

**Y4 · ÖNEMLİ · Kaynak düzeltmesinin taşıdığı olgu okunmuyor.**
- Yer: 397–406 sn, c2_kasa. Kart "SERMAYE / 1426'DA ÇEKİLDİ" (KA2-Y1 düzeltmesi), x≈200–660, y≈400–640.
- "1426'DA ÇEKİLDİ" 22,3 px; videonun en küçük yazısı.
- Kırmızı çarpının uçları "SERMAYE"nin S'sini, "1426"nın 1'ini ve "ÇEKİLDİ"nin son İ'sini örtüyor. Okunan: "…ERMAY…", "426'DA ÇEKİLD…".
- 1426 yılı anlatımda geçmiyor; altyazı okuyan izleyici için tek taşıyıcı bu kart.
- Yapılacak: yazıyı ≥34 px yap ve kartın altına, ayrı satıra al. Çarpıyı yazının arkasına çiz ya da inceltip %50 opaklığa indir.

**Y5 · ÖNEMLİ · Kaynak sınıfı damgaları otomatik zeminin dışında.**
Damgalar sprite olarak çiziliyor ve `contrast_scrim` yalnız `ink`/`kick` için çalışıyor. Kanalın dürüstlük işaretleri olan damgalar desenli ya da koyu zeminde zayıf:
- "BİR KAYNAĞA GÖRE" (157–162 sn; x 1178–1703, y 270–303; 40 px): **≈2,7:1**. Sol yarısı koyu mavi duvar halısının üstünde.
- "ANEKDOT" (549–552 sn; x 1291–1630, y 272–318): **≈1,9:1**. Pencere kafesi ve koyu ahşap üstünde; "A" kafese karışıyor.
- "DESTEKLEDİ" (505 sn; x 1134–1587, y 389–439): **≈2,6:1**. "D" kırmızı bayrağın üstünde kayboluyor.
- "VILLANI'YE GÖRE · TAHMİN" (141,5–144 sn; x 1027–1814, y 268–304): ≈2,7:1. 142,8 sn'den sonra "90.000" sayaç kartının üst kenarıyla çakışıyor; "VILLANI'YE" kartın üstüne biniyor.
- Ayrıca sınırda (2,9–3,1:1): "ÇEVİRİ", "BİR HESABA GÖRE", "İLK SERMAYE", "YILBAŞI".

Yapılacak:
- Damga sprite'larına da aynı ölçüm uygulansın. Kontrast düşükse damganın arkasına açık kâğıt yaması konsun (gerçek bir mürekkep damgası gibi).
- Damgalar sayaç ve levhalarla çakışma denetiminden geçsin.

**Y6 · KÜÇÜK · Kapak yankısının kenar payı.**
- Yer: 0–3,7 sn. Altın başlık bloğu x 53–1731; İ noktaları y 27'de, büyük harflerin üstü y 83'te.
- Sol pay 53 px: eylem güvenli alanının (67 px) dışında. Çağdaş TV ve YouTube uygulamalarında sorun çıkmaz. Aşırı tarama (overscan) açık eski TV'lerde "S" ve "M" kırpılabilir.
- Yapılacak: yankıyı merkezden 0,94 ölçekle ya da 40 px sağa al.

**Y7 · KÜÇÜK · KATASTO / CATASTO tutarsızlığı.**
- 486,4–493,6 sn'de "KATASTO · 1427", 502,8–506,7 sn'de "GIOVANNI · CATASTO'YU DESTEKLEDİ" yazıyor.
- Anlatım ve SRT "catasto" diyor. Tek yazım seçilsin: "CATASTO".

**Y8 · KÜÇÜK · HUD perde rakamları küçük.**
- HUD küçülünce "I II III" 21 px'e indi; stil kuralının ikincil yazı tabanı 22 px. Pasif rakamlar soluk.
- Yapılacak: ≥24 px yap ya da pasif rakamları kaldır; yalnız etkin perdeyi göster.

**Y9 · KÜÇÜK · SRT'de yeni bölünmeler ve uzun satırlar.**
- Ad satır sonunda bölünüyor: "bir yün tarayıcısı, Michele │ di Lando, gonfaloniere oldu." (replik 65, 3:59,98).
- Diğer bölünmeler:
  - replik sınırında: "en │ eski" (113/114, 6:56–7:03), "kimse │ istemeden" (153/154);
  - satır sonunda: "kısa │ ömürlü" (72), "torununun │ oğlu" (141), "öteki │ kıymetli şeyler" (19).
- 42 karakteri aşan satırlar: replik 63'te 45, replik 85'te 43 karakter. Telefonun dikey küçük oynatıcısında üç satıra kırılabilir.
- Yapılacak: `make_srt` kurallarına ekle:
  - Roma rakamı + nokta + ad bölünmesin.
  - Ad öbekleri bölünmesin ("… di …", "de' …").
  - Sıfat + ad, iyelik öbeği ve "en + sıfat" bölünmesin.
  - Satır en çok 42 karakter olsun.

**Y10 · KÜÇÜK · Sayının son değeri kısa kalıyor.**
- "150.000+ FLORİN KÂR" son değerine ≈516,1 sn'de oturuyor. 516,5 sn'de mum geçişi başlıyor; 517,6 sn'de ekran kararmış. Tam okunur kalma süresi ≈0,8 sn.
- Yapılacak: sayılarda son değer en az 1,2 sn kalsın ya da geçiş cümle sonundan (517,96 sn) sonra başlasın.

**Y11 · KÜÇÜK · Eski stil rakamlar.**
- Cormorant italik rol satırlarında rakamlar eski stil: "1300'DE … 1341'DE", "1430'LAR · HAPİSTE" (34 px; büyük harf yüksekliği ≈21 px).
- Telefonda "13oo" gibi okunuyor.
- Yapılacak: rol satırlarında hizalı rakam kullan (`lnum`) ya da rakamları Cinzel ile yaz.

### Denetim notu (motor)
`qa_yerlesim` "İHLAL 0" diyor. Ama Y1–Y3'ü göremiyor, çünkü yalnız levha–kenar, levha–HUD ve levha–altyazı ilişkisine bakıyor. Göremediği dört durum:
- levha–levha çakışması;
- yazı–yazı çakışması;
- serbest `ink` etiketi;
- sprite (damga, yaldız).

`contrast_scrim` da yalnız düz renkli `ink` için çalışıyor; damgalar ve yaldız rakamlar (KUR FARKI) kapsam dışı. Benim `audit_v2.py` + `layout_v2.py` yaklaşımım (çizilen her yazının gerçek ekran kutusu) bu dört durumu da kapsıyor. Yarım günde kapıya çevrilebilir.

---
## 5. Kullanıcının sorusu: "Bu çizim tarzı çok mu basit, ucuz görünüyor; yapay zekâ ile üretilmiş gibi mi duruyor?"

**Yapay zekâ ile üretilmiş gibi durmuyor.** Üretken görsellerin en kolay yakalanan izi bozuk harf ve tutarsız geometridir. Burada 340'ı aşkın ekran yazısı vektör olarak çiziliyor, Türkçe karakterlerde hiç eksik glif yok, perspektif ve çizgi dili tutarlı. Videoyu "elle kurulmuş" gösteren en güçlü işaret tipografi.

**Ucuz ya da şablon okunan üç yer var:**
1. Belgelerdeki yazı dalgalı zikzak çizgilerle temsil ediliyor ve yer tutucu gibi duruyor. Örnekler: Machiavelli/Cavalcanti sayfaları (538–568 sn), evlilik sözleşmesi (309 sn), talepler kâğıdı (252 sn).
2. Kontrast için eklenen koyu yuvarlak etiketler her yerde aynı. Kontak sayfalarındaki 64 karenin ≈29'unda en az bir tane var. Okunurluğu çözdüler ama freskin içinde değil, üstüne yapıştırılmış bir arayüz katmanı gibi duruyorlar.
3. Boş parşömen anları (534,5–536,3 sn; SA1-Y4) ve ışık geçişlerindeki yıldız parlaması (SA1-Y7).

**Ucuz okunmayanlar:**
- krem levhalar (176 sn, Villani);
- oyma "ESKİ PAPA" (464 sn);
- kapak yankısı (0–3,7 sn);
- sayaçlar ve madalyalar.

**Öneri:**
- Zikzak çizgileri düşük kontrastlı gerçek el yazısıyla değiştir (IM Fell italik, kısa İtalyanca/Latince sözcükler). Göz "yazı" olarak tanır, okunması da gerekmez.
- Koyu etiketleri yalnız gerçekten kalabalık zeminde kullan. Sakin zeminde aynı okunurluğu krem levha ya da mürekkep şerit (banderol) diliyle ver.

---
## 6. En emin olmadığım nokta

1. **Kontrast yönteminin kör noktası:** yüzdelik yöntemi döndürülmüş yazıda kutuya fazla zemin aldığı için yanılabiliyor. "VIA PORTA ROSSA" ölçümde 1,6:1 çıktı, gözle ≈4:1. Bu yüzden damgaları (Y5) ve KUR FARKI'nı kareden gözle de doğruladım. Sayılar ±%20 sapabilir; sıralama güvenilir.
2. **Örnekleme:** çekim başına 3 kare aldım. 0,5 sn'den kısa yaşayan bir yazı kaçabilir. Nitekim Y2'yi (alfa 0,48'de kalan etiket) ilk taramada alfa süzgecim yüzünden kaçırdım; SA1'in raporuyla yakalayıp doğruladım.
3. **Telefon izleme biçimi:** satır içi dikey mi, tam ekran yatay mı izlendiği hâlâ bilinmiyor. 34 px tabanı tam ekranda yeterli, satır içi dikeyde sınırda. Gerçek cihazda bir bakış bu yargıyı kesinleştirir.

---
## 7. Çapraz not (SA1, SA2 tur 2)

- **SA1:** Y2, Y3, Y4 ve Y8'i kendi ölçümümle doğruladım (benim Y2, Y1, kullanıcı sorusu ve Ö6 satırlarım).
- **SA1-Y7 (yıldız ışınlı parlama):** fotosensitivite açısından güvenli. Flaş ölçümünde 1 sn'de en çok 2 dönüm noktası çıktı, yani tek flaş. Stok/YZ çağrışımı yargısına katılıyorum.
- **SA2-Y1 (figürün başı gövdeden önce beliriyor):** benim merceğim dışında.
