# KA1 · TUR 3 — Medici Parça 1, v3 (`out_p1/medici_P1.mp4`, 601,54 sn)
Mercek: konu uzmanı, olgu ve sayı denetimi (veto).

## 1. Karar
**ONAY — 9,3/10. Vetom kalktı.**
- Tur 2'de ONAY koşulum olarak saydığım beş madde v3'te kapandı: E1 (hançer), Ö1 (Loggia), Ö2 (Villani levhası), Ö3 (1520 mührü), Ö4 (HUD yılları). Küçük maddelerim K1–K4 de kapandı.
- 9,5 yerine 9,3 vermemin nedeni iki önemli madde. İkisi de KA2'nin bulgusu, ben de doğruladım:
  - **N1:** Konstanz çekiminde kardinalin eli öndeki figürün ensesinde.
  - **N2:** Machiavelli ve Cavalcanti sayfalarında, İtalyanca özgün satırın altındaki Türkçe özet çeviri gibi duruyor.
- İkisi de ücretsiz; düzelirse puanım 9,5 olur. Veto gerektirmiyorlar.

**Sınırlarım:** Videoyu oynatamadım, sesi dinleyemedim.
- **Kareler:** v3'ten ffmpeg ile ≈45 tam çözünürlüklü kare çıkardım. Zamanları `timeline.json` sözcük çapalarından seçtim; ses ve çizelge v2 ile aynı (toplam 590,23 sn).
- **Belgeler:** `KURUL_BRIFI_P1_TUR3.md`, `KURUL.md` (tur 2 sonucu, v3 planı), `duzeltme_tur2/SCN-1.md` ve `SCN-2.md`, `out_p1/qa_flow_v3.txt` (yerleşim ve dönem İHLAL 0), `kurul/tur3/KA2.md`, `yayin/studio_paketi_P1/00–05` ve SRT.
- **Kaynaklar** (curl, hepsi HTTP 200):
  - it.wikipedia "Loggia della Signoria", en.wikipedia "Loggia dei Lanzi", it.wikipedia "Luca Pacioli";
  - de Roover 1963 tam metin;
  - Machiavelli IV (it.wikisource);
  - Cavalcanti, *Istorie fiorentine* (Polidori 1838).
- **Güven etiketleri:** ● = metin okundu ve iddiayı taşıyor; ◐ = nitelikli; "bilgim" = kendi bilgim, bu turda açılmadı.
- **Saklanan kanıtlar** (`/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/ka1v3/`): `kanit_E1_472.7_crop.png`, `kanit_O1_1338_vs_1378.png`, `kanit_O3_muhur_577.5.png`, `kanit_N1_konstanz_444.3.png`, `kanit_N2_sayfalar_567.5.png`. Diğer kare dökümlerini (tur 1–3) sildim.

## 2. Tur 2 maddelerimin durumu

### Koşullar (tur 2'deki ONAY yolu)
| Madde | Durum | v3 kanıtı |
|---|---|---|
| **E1** Papanın hançeri (VETO) | **KAPANDI** | Hançer yok. 465,5 sn'de "DE ROOVER · ANDIĞI ARŞİV BELGELERİ" ve "BELGE · DE ROOVER" var. 470,2–471,2 sn ara planı: mitrayı tutan eller ve işaret eden papalık eli. 471,9–475,5 sn: papa kurşun mühürlü belgeyi (bulla) omuz hizasında uzatıyor (x≈1150–1260, y≈150–430); Giovanni mitrayla eğiliyor; "AFOROZ TEHDİDİ" kolun üstünde. de Roover n. 45 ("Pope Martin V had to threaten Giovanni di Bicci with excommunication") ile uyumlu ●. Kanıt: `kanit_E1_472.7_crop.png`. |
| **Ö1** Loggia dei Lanzi | **KAPANDI** | **1338** (139,3–143,5 sn): sağ kenarda (x≈1500–1920, y≈300–940) sıradan ev cepheleri ve sokak kemeri var; friz, teras ve korkuluk yok. **22 Temmuz 1378** (236,0–238,6 sn): sağ kenarda (x≈1700–1920, y≈620–940) taş ayak kütükleri ve ahşap iskele. Kanıt: `kanit_O1_1338_vs_1378.png`. Dayanak: it.wikipedia "L'edificazione risale al periodo tra il 1376 e il 1382" ●; en.wikipedia "built between 1376 and 1382" ●. Temmuz 1378'deki yüksekliği hiçbir kaynakta bulamadım (bkz. §5). |
| **Ö2** Villani levhası | **KAPANDI** | 176,4 sn: "GİOVANNİ VİLLANİ · 1300'DE PERUZZİ ORTAĞI · YÖNETTİĞİ BUONACCORSİ 1341'DE BATTI" (x≈750–1775, y≈185–325); önerdiğim metinle birebir. DBI "socio dal maggio 1300"; "precipitò nel 1341 quando la compagnia fallì" ●. |
| **Ö3** 1520 mührü | **KAPANDI** | 577,5 sn: "O KALEM · Istorie fiorentine" ve balmumu mühür (x≈1030–1370, y≈435–780). Mühürde 6 top var; en üstteki daha iri ve üç zambak kabartmalı. 1465 sonrası biçim, it.wikipedia "Stemma dei Medici" blazonuyla birebir ●. Kanıt: `kanit_O3_muhur_577.5.png`. |
| **Ö4a** Çeyiz ve evlilik sözleşmesi | **KAPANDI** (başkanın varyantıyla; küçük bir artık var, bkz. §3 Y1) | HUD 307,0 sn'de ("PİCCARDA BUERİ'NİN ÇEYİZİ · 1.500 FLORİN") ve 311,0 sn'de ("EVLİLİK SÖZLEŞMESİ · Piccarda Bueri · çeyiz · 1.500 florin · İLK SERMAYE") **1385**. 300,5 sn'de "1390'LARIN BAŞI" ile HUD 1390. Ardından 1385'e geri dönüş, olgu açısından doğru: devralma 1393, çeyiz Ekim 1385 (de Roover ●; DBI ●). |
| **Ö4b** Dante ve Villani HUD | **KAPANDI** | Dante "lanetli çiçek" (124,4 sn): HUD gizli. Villani darphanesi (133,5 sn): HUD **1338**; levha "KRONİKÇİ · ESKİ DARPHANE YÖNETİCİSİ". |

### Küçük maddeler
| Madde | Durum | v3 kanıtı |
|---|---|---|
| "BUGÜN" + HUD 1737 | **KAPANDI** | 82,5 sn: HUD gizli; "BUGÜN" ve "UFFİZİ" levhaları var. |
| **K1** Catasto (portata) | **KAPANDI** | 489,0–491,5 sn: "CATASTO · 1427" ve "HANE REİSLERİNİN BEYANNAMESİ · PORTATA". Hane reisleri beyannameyle masaya geliyor; duvarda Komün kalkanı (beyaz zeminde kırmızı zambak). it.wikipedia "Catasto fiorentino" ("ogni cittadino dovesse dichiarare sotto il suo Gonfalone…") ile uyumlu ●. |
| **K2** Latince mezar yazıtı | **KAPANDI** | 459,0–463,5 sn: taşa harf harf "IOANNES QVONDAM PAPA" yazılıyor; levha "ESKİ PAPA · ÇEVİRİ BİZE AİT". en.wikipedia "Tomb of Antipope John XXIII" ile uyumlu ●. Taştaki "XXIII" yok; anlatım "eski papa" dediği için kabul. |
| **K3** Kefalet/fidye HUD | **KAPANDI** | 447,5 ve 450,0 sn: HUD **1418** (DBI: kurtuluş 1418, fidye 1419 ●). |
| **K4** "VİLLANİ'YE GÖRE · TAHMİN" damgası | **KAPANDI** | 141,8–143,5 sn: damga sayaç kartının üstünde, tam okunuyor. |
| **K5** Darphane örsü (isteğe bağlı) | **AÇIK, kabul** | 133,5 sn: boynuzlu örs duruyor. Üslup sadeleştirmesi; olgu iddiası taşımıyor. |

### Tur 2'de kapanan maddelerde gerileme kontrolü: TEMİZ
- **G1:** 1348 panoramasında kubbe yok (183,5 sn); 1429 kulesinde kubbe yarım, fenersiz ve vinçli (588,5 sn).
- **G2:** 1743 bağlamında 1465 sonrası arma doğru (12,2 sn); bitiş kartında marka işareti olarak.
- **V9:** Lorenzo ve Cosimo madalyalarında "TEMSİLÎ"; Cosimo yazıtı "COSMVS · MEDICES" (583,0 sn).
- **Strozzi:** 501,5 sn "PALLA STROZZİ · 1427'NİN EN ZENGİNİ · 163.000 FLORİN · YAKLAŞIK"; "ikinci en zengin" ifadesi yok.
- **Diğerleri:**
  - 401,0 sn "SERMAYE · 1426'DA ÇEKİLDİ · DE ROOVER'A GÖRE";
  - 483,5 sn "22 YIL + 18 YIL · 1422 · KESİNTİSİZ · ARALIKLI";
  - 183,5 sn "MART 1348 · YAZ BOYUNCA";
  - 224,9 sn "KURAYLA".

## 3. Gerilemeler ve yeni sorunlar

### ÖNEMLİ (engelleyici değil; ücretsiz)
| # | Yer | Bulgu ve kaynak | Ne yapılmalı |
|---|---|---|---|
| **N1** (KA2; doğruladım) | 443,6–444,9 sn, Konstanz. El ≈(1540–1590, 540–590); kardinal x≈1540–1820. Kanıt: `kanit_N1_konstanz_444.3.png`. | Kırmızı cüppeli figürün eli, öndeki koyu cüppeli figürün başının arkasında, ensesinde bitiyor. "Konstanz Konsili onu papalıktan indirdi" cümlesiyle birlikte bir din adamının birini ensesinden tuttuğu biçiminde okunabiliyor. Cossa 1415'te gözaltına alındı, ama bunu dünyevi yetkililer yaptı (bilgim ◐). Bir kardinalin bedensel zor kullandığına dair kaynak yok. Silah ve şiddet yok, temas belirsiz ve ≈1,3 sn sürüyor; bu yüzden veto değil. | Kardinal öne ya da sola alınsın ve kolu yerdeki tiaraya ya da tahta uzansın; ya da eylem `talk` olsun. 1 çekim. |
| **N2** (KA2; kaynak gözüyle sınadım) | 560,0–568,4 sn: Machiavelli sayfası (x≈200–830, y≈300–865) ve Cavalcanti sayfası (x≈1090–1720). İtalyanca satırlar y≈340–455. Kanıt: `kanit_N2_sayfalar_567.5.png`. | **İtalyanca alıntılar birebir doğru.** Machiavelli IV (it.wikisource): "Muoio contento…" ve "…perché quello che l'uomo si toglie, non quello che all'uomo è dato, ci fa odiare" ●. Cavalcanti (Polidori 1838): "…non debbe aver dolore del partimento dalle mondane sollecitudini, per passare ai perpetuali riposi" ●. **Altlarındaki Türkçe metinler çeviri değil, özet:**<br>• Machiavelli'de "si toglie" "kendine aldığı" demektir; Türkçe metin "istediği" diyor. "ci fa odiare" "nefret ettirir" demektir; "invidia" (kıskançlık) bir önceki yan cümlede geçiyor ("né invidia né pericolo"). Türkçe özet bu ikisini birleştiriyor.<br>• Cavalcanti'deki "değiş tokuş" benzetmesi özgün metinde yok.<br>İki metin yan yana konunca özet, çevirisi gibi okunuyor. Paketteki asgari düzeltme yapılmış: `02_aciklama.txt` "…sözleri özetle aktarılmıştır, ekrandaki İtalyanca satırlar özgün metinlerden kısa alıntılardır" ✓. | İki sayfada Türkçe bloğun altına "ÖZET · ÇEVİRİ BİZE AİT" etiketi; mezar levhasıyla aynı biçimde. İsteğe bağlı: Machiavelli alıntısına "…né invidia né pericolo…" eklensin; böylece özgünde "kıskançlık" da görünür. 2 çekim. Anlatım değişmez; KAY bu kaymayı ◐ "zorunlu yama değil" diye işaretlemişti, ben de aynı görüşteyim. |

### KÜÇÜK
| # | Yer | Bulgu | Öneri |
|---|---|---|---|
| **Y1** | 291,9–296,8 sn (c1s26 "Roma'da…"); levha x≈960–1600, y≈170–315 | "VİERİ Dİ CAMBİO · GİOVANNİ'NİN PATRONU" levhası hâlâ HUD **1378** altında. de Roover: "From 1385, the manager of this establishment was Giovanni di Bicci"; 1386–93 arası ortaklık "Vieri e Giovanni de' Medici in Roma" ●. 1378'de Vieri yanında çalıştığına dair belge yok. | c1s26'daki "Roma'da" sözcüğünde HUD **1385**; ardından "1390'ların başı"nda 1390 ve c1s27'de 1385 olarak kalsın. Ya da 285–296,8 sn arasında HUD gizlensin. |
| **Y2** (KA2-N4'e katılıyorum) | 575,6–580,0 sn | "Istorie fiorentine · MEDİCİ SİPARİŞİ" çekiminde HUD 1429, ama nesne 1520'den (mühür doğru biçimde nesne yılıyla çizilmiş). Machiavelli'nin c1s20–21 çekimlerinde HUD gizli; burada da gizli olmalı. | HUD gizlensin ya da karta "1520" eklensin. |
| **Y3** (KA2-N3; zarar yok) | 517,3–517,8 sn | Mum "DEFTERLER GÖSTERİR" damgasının "E" harfini örtüyor; damga ≈0,5 sn görünüyor. Rakam doğru (de Roover Tablo 8 ●; ekranda "150.000+"). | İsteğe bağlı. |

### Doğru bulduğum yeni ekran olguları (v3'te eklenenler)
- **12,2 sn** "ANNA MARİA LUİSA · MEDİCİ HANEDANININ SON ÜYESİ": DBI ve it.wikipedia'daki "linea primogenita… si estinse" ile uyumlu ●. "Hanedan" sözcüğü yönetici kolu anlatıyor; anlatımdaki "Toskana'yı yönetmiş Medici hattı" ile tutarlı.
- **Çifte kayıt defteri (418,5–430 sn):** "CENOVA 1340 · PACİOLİ 1494 · MEDİCİ İCADI ✗ · ETMEDİLER", sağ sayfada "MEDİCİ'NİN FARKI: YAPI · DEFTER DEĞİL · FLORANSA → ROMA / VENEDİK · KENDİ ORTAKLIĞI". Kaynaklar: de Roover "first unquestionable examples in 1340" ●; it.wikipedia "Luca Pacioli": "Nel 1494 pubblicò a Venezia… Summa" ●.
- **Catasto defteri (496,5–501,5 sn):** "9.780 HANE", "137 HANE", "%29,8 · BİR HESABA GÖRE" (Online Catasto ●).
- **Kasa defteri (483,5 sn):** "22 + 18 YIL" (DBI ●).
- **Signoria'da Ciompi taleplerinin okunması (246,5 sn):** "YAZILDIĞINA GÖRE" damgasıyla; Machiavelli III'teki dilekçe sunumuyla uyumlu ●.
- **Orsanmichele (320,0 sn):** Gotik kübik yapı, "VİA PORTA ROSSA" ile birlikte. Yapı 14. yüzyıl ortasından kalma (bilgim ◐).
- **Konstanz salonu (444,3 sn):** altın zemin üzerinde tek başlı kara kartal sancakları. 1415'te Sigismund "Romalıların Kralı"ydı; çift başlı kartal 1433 imparatorluk taç giyiminden sonra geldi (bilgim ◐). Dönemine uygun bir ayrıntı.
- **Stinche hücresi (554,5 sn):** "HAPİSTE · 1430'LAR · OLAYA DAHA YAKIN"; DBI Cavalcanti ile uyumlu ●.
- **Bitiş ekranı (597,5 sn):** "SIRADAKİ PARÇA · 2/7 · COSİMO: SÜRGÜN VE DÖNÜŞ"; P2'nin konusuyla (1433 sürgünü, 1434 dönüşü) uyumlu.

### Sonraki parçalar için not (P1'i etkilemiyor)
`donem.loggia_stage` 1382'den sonrasını "tam yapı" sayıyor ve `cilt_sehir.loggia()` tam yapıyı teraslı ve korkuluklu çiziyor. Ama teras sonradan eklendi:
- it.wikipedia: "Nel 1583 … Bernardo Buontalenti creò sulla sommità della loggia una terrazza" ●;
- en.wikipedia: Uffizi'den sonra "the Loggia's roof was modified by Bernardo Buontalenti and became a terrace" ●.

Bu yüzden P2–P7'deki 1382–1582 meydan sahnelerinde (ör. Savonarola 1497–98) korkuluklu teras anakronik olur. Aynı şey heykeller için de geçerli: Perseus 1554, Sabin Kadınlarının Kaçırılışı 1583 (bilgim ◐). Öneri: dördüncü bir aşama eklensin: 1382–1582 arası çatı terassız ve korkuluksuz; 1583'ten sonra teras.

### Paket: yedek başlık T3 için kaynak üyesi onayı
**ONAYLIYORUM:** "Medici Ailesi (1/7): Faiz Yasaktı, Kilise Müşteri Oldu".
- **"Faiz yasaktı":** de Roover, "According to canon law, usury consisted in any increment…" ●.
- **"Kilise müşteri oldu":** de Roover, "time deposits (depositi a discrezione) made by high churchmen and prominent laymen, among them, the Pope himself"; 1427 bilançosunda Camera Apostolica'nın ≈25.000 florin mevduatı ●. Ayrıca 1422'den itibaren papalığın resmî kasa memurluğu (DBI ●).
- Başlık videonun c2s9'da söylediğinden fazlasını iddia etmiyor; Kilise'nin faiz ödediğini ya da aldığını söylemiyor.

## 4. Kullanıcının sorusu: "Bu çizim tarzı ucuz mu, yapay zekâ gibi mi?"
Yanıtım kısmen değişti. YZ izi yine yok. Gerçek harfli sayfalardaki İtalyanca alıntılar birincil metinle birebir; Latince mezar yazıtı da öyle. Bu, YZ'nin tam tersi bir titizlik olarak okunuyor.

Tur 2'de şablon hissini veren "dönemsiz oda kiti" büyük ölçüde gitti. Artık her yerin kendi seti var: kartal sancaklı Konstanz salonu, Komün kalkanlı Catasto dairesi, Stinche hücresi, anahtar ve tiaralı papalık salonu.

Kalan şablon izleri iki tane: aynı "üstten açık defter" kalıbı üç kez tekrarlanıyor, ve 1743 yatak odası Quattrocento kitiyle duruyor (stil kararı olarak kabul edildi).

## 5. En emin olmadığım nokta
1. **Temmuz 1378'de Loggia'nın ne kadar yükseldiği.** it.wikipedia ve en.wikipedia yalnız "1376–1382" diyor; aşama aşama bir inşaat takvimini web aramasında da bulamadım. Ekrandaki "ayaklar + iskele" makul ama doğrulanmamış bir temsil. Sağ kenarda, geri planda olduğu için yanlış okunma riski düşük; bu yüzden Ö1'i kapandı sayıyorum.
2. **N1 oynatma hızında nasıl okunur?** Kare kare bakınca ense teması belirgin; 1,3 sn içinde çoğu izleyici bunu "işaret" olarak görebilir. Bu yüzden önemli dedim, veto demedim.
3. **Konstanz'daki tek başlı kartal.** Doğru olduğunu düşünüyorum, ama bu yalnız benim bilgime dayanıyor (◐). Yanlış olsa bile ekranda adı ya da tarihi geçmiyor.
