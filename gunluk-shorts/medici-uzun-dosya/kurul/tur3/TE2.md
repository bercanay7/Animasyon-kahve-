# TE2 — Teknik kalite · Erişilebilirlik / Okunurluk — Medici Parça 1 · TUR 3 (v3)

Üye: TE2. Mercek: telefon, TV, aydınlık ve karanlık ortam. Önceki raporlarım: `kurul/tur1/TE2.md`, `kurul/tur2/TE2.md`.

**Sınırlarım:** videoyu oynatamadım, sesi dinleyemedim. Hareket ve süre yargılarım kare dizilerine ve ölçüme dayanıyor. Altyazının ekranda nereye düştüğünü YouTube oynatıcısında görmedim; stil rehberindeki bandı (y 938–1042) varsaydım.

---
## 1. Karar

**ONAY: 9,0 / 10** (eşikte). Tur 2'de 8,6 RED vermiştim; tur 1'de 7,0.

| Alan | Tur 2 | Tur 3 |
|---|---|---|
| Fotosensitivite | 10 | 10 |
| SRT | 9,0 | 9,5 |
| Yerleşim, kenar payı, HUD | 8,0 | 8,5 |
| Kontrast ve punto | 8,5 | 9,0 |
| Karanlık ve aydınlık ortam | 9,0 | 9,0 |
| Kapak | 9,5 | 9,5 |

**Gerekçe:**
- Tur 2'de ONAY için koyduğum koşulların hepsi yerine geldi: Y1–Y4, KUR FARKI ve SRT'deki iki bölünme. Tek istisna Y5: bir damga, iki saniyelik bir anda hâlâ fişsiz.
- Kontrast medyanı 8,9:1'e çıktı. Anahtar yazıların hepsi 4,5:1'in üstünde. Flaş temiz.

**Puanı eşiğe çeken yeni sorunlar** (§4): hepsi yerel ve tek satırla düzelir.
- Defter sayfası çekimlerinde kamera sayfadan ayrılırken yarım kalan sözcükler ve sayılar kadrajda kalıyor; örneğin "80 HANE" ve "7 HANE" (G1).
- "ETMEDİLER" damgası iki satırlık altyazının altında kalıyor (G2).
- Uygulanan yeni kamera "FRANSIZCA" damgasını sağ kenara itiyor (G4).

**v3.1 için:** başkanın düzeltme listesine şu üç madde eklensin:
- `stamp_hold` → `anim.paper_stamp`;
- ETMEDİLER damgasının konumu;
- defter sayfası çekimlerinde sol sayfa etiketlerinin söndürülmesi.

Bunlarla puanım 9,4 olur. Gerileme kontrolünü tek üye olarak yapabilirim.

---
## 2. Ne yaptım

Tur 1–2 betiklerimi v3'e karşı yeniden koştum. Aynı anda tek ağır işlem çalıştırdım, render yapmadım. Betikler ve kanıtlar `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/te2_t3/` altında. Raporda adı geçen PNG'ler (`out_p1/kurul/` önekli olanlar hariç) bu klasördedir.

- **Flaş ve karanlık:** v3'ün 14.437 karesinin tamamı (WCAG göreli parlaklık, 4×4 bölge ızgarası, doygun kırmızı payı).
- **Yazı kutuları:** motorun yalıtılmış kopyasında 102 çekim × 3 kare çizdirdim ve 5.546 yazı/damga kaydı topladım (`audit_v3.py`, `layout_v3.py`). Bu tur denetime yazı × yazı çakışmasını ve kadraj dışına taşmayı da ekledim.
- **Gerçek piksel kontrastı:** videodan 237 zaman noktasında 1.453 yazı örneği ve 26 damga/yaldız sprite'ı ölçtüm (`contrast_v3.py`, `stamps_v3.py`).
- **Hedefli tam çözünürlüklü kareler:** yaklaşık 90 kare.
- **Diğer:** 150.000+ sayacının oturuşu kare kare ölçüldü. SRT (05.11 02:22, md5 `336461a5…`) ayrıştırıldı. Kapaklar 168 px'te yeniden test edildi.
- **Okuduklarım:** `KURUL_BRIFI_P1_TUR3.md`, `KURUL.md` (tur 2 sonucu ve v3 planı), `tur3_duzeltme_listesi.md`, düzeltme raporları ENG-C, ENG-D, SCN-1 ve SCN-2, `qa_flow_v3.txt`.

### Ölçüm özeti (v2 → v3)

| Ölçüt | v2 | v3 |
|---|---|---|
| Yazı örneklerinde kontrast medyanı | 8,8:1 | **8,9:1** |
| Örneklerin <4,5:1 payı | %17 | **%12** |
| Benzersiz yazıların en iyi anında <4,5:1 | %14 | **%8** (kalanlar dekoratif belge numaraları ve geçiş anları) |
| Damgalar (sprite, fişli) | 1,9–2,7:1 | **4,5–6,7:1** (bir istisna: Y5) |
| 34 px'ten küçük gerçek yazı | %13 | **%5** (17 yazı; 7'si galeri etiketi) |
| Flaş: 1 sn içindeki dönüm noktası (WCAG eşiği 6) | genel 2, bölgesel 4 | **genel 2, bölgesel 4** |
| Doygun kırmızı alan | azami %0,8 | **azami %0,6** |
| Kare ortalaması <0,03 olan süre | 6,8 sn | 15,3 sn: artış 10 sn'lik koyu lacivert bitiş ekranından. Oradaki yazılar 7–18:1, sorun değil |
| SRT: replik / ort. kar/sn / azami / yetim | 158 / 14,0 / 17,0 / 0 | **158 / 14,0 / 17,0 / 0** |

---
## 3. Tur 2 maddelerimin durumu

Koordinatlar 1920×1080'dir.
- HUD: x 1548–1848, y 72–138.
- Altyazı bandı: y 938–1042.
- Güvenli alan: x 90–1830, y 60–1020.

| Madde | Durum | Kanıt (v3) |
|---|---|---|
| **Y1** GİOVANNİ × COSSA levhaları | **KAPANDI** | 432,4–436 sn: GİOVANNİ levhası x≈216–630, y≈414–504; BALDASSARRE COSSA x≈540–1268, y≈186–330. Çakışma yok (`check_a.png`) |
| **Y2** "EVLİLİK ÇEYİZİ" × "1.500" | **KAPANDI** | 306,6–307,4 sn: yalnız "PİCCARDA BUERİ'NİN ÇEYİZİ" levhası ile "1.500 FLORİN" var |
| **Y3** "CİOMPİ LONCASI" altyazı bandında | **KAPANDI (bant)** | 271,6–277,7 sn: y≈862–922, bandın üstünde. Etiket sağ kenara kaydı: **G5** |
| **Y4** "1426'DA ÇEKİLDİ" | **KAPANDI** | 397–406 sn: 39 px, **5,5:1**. Çarpı yalnız kese simgesinde (`check_a.png`) |
| **Y5** damga kontrastı | **KISMEN** | Fişli damgalar: BİR KAYNAĞA GÖRE **5,8**, VİLLANİ'YE GÖRE **6,0** (artık 90.000 kartının üstünde, çakışma yok), DESTEKLEDİ **6,3**, ANEKDOT **6,6**, İTİRAZ **6,7** (462,6 sn; figürün dışında), CİOMPİ 6,2, İLK SERMAYE 6,1, YILBAŞI 5,2 (`stamps_crops_v3.png`). **Kalan:** "BELGE · DE ROOVER" kesmeden sonra 466,9–≈469,0 sn'de (#80, taht odası) fişsiz, x 288–914, y 374–419. Kırmızı mürekkep kırmızı duvar halısının üstünde, ≈3,5:1. Tiara simgesi "R"nin üstünde (`deroover_itiraz_fr.png`). Neden: `scenes_c2.py` 47–53. satırdaki `stamp_hold` doğrudan `CM.stamp` çağırıyor. **Yapılacak:** aynı imzalı `anim.paper_stamp`'e çevir. ÖNEMLİ, tek satır |
| **Ö5 kalan** KUR FARKI | **KAPANDI** | 368,8–373,4 sn: **6,4:1** (benim yöntemim; ENG 7,5:1) |
| **SRT** "III. Edward" ve "Michele di Lando" | **KAPANDI** | Replik 47 (2:48,8): "III. Edward'ın ödemediği / borçlar gösterilir." Replik 65 (3:59,98): "bir yün tarayıcısı, / Michele di Lando, gonfaloniere oldu." |
| **Y6** Kapak yankısının kenar payı | **KISMEN** | Başlık bloğu x 60–1730 (v2'de 53–1731); "İ" noktaları y 27'de. 90 px kuralının dışında. Güncel TV uygulamalarında aşırı tarama (overscan) olmadığı için KÜÇÜK (`cover_echo_safe.png`) |
| **Y7** CATASTO / KATASTO | **KAPANDI** | Her yerde "CATASTO · 1427" |
| **Y8** HUD perde rakamları 21 px | **AÇIK** | Değişmedi. KÜÇÜK, planda yoktu |
| **Y9** SRT'deki diğer bölünmeler | **KISMEN** | Kalanlar: "öteki │ kıymetli" (19), "kısa │ ömürlü" (72), "en │ eski" (113/114), "torununun │ oğlu" (141), "kimse │ istemeden" (153/154). Satır uzunluğu: replik 63'te 45, replik 85'te 43 karakter. KÜÇÜK |
| **Y10** Sayının son değeri kısa kalıyor | **KAPANDI** | "150.000+" 516,00 sn'de oturuyor. Mum geçişinin kararması 517,17 sn'de başlıyor: **1,2 sn** tam, ≈0,3 sn de sönerek okunuyor (`ledger150_v3.png`) |
| **Y11** Eski stil rakamlar | **KAPANDI** | "1300'DE … 1341'DE" (Villani levhası) ve "1430'LAR · HAPİSTE" hizalı rakamla (`villani_plate_v3.png`) |
| **Ö4** ESKİ PAPA | **KAPANDI (iyileşti)** | Latince yazıt "IOANNES QVONDAM PAPA" **10–11:1**; "ESKİ PAPA · ÇEVİRİ BİZE AİT" **15,8:1** (`mezar_v3.png`) |
| **Ö6** Bitiş ekranı | **KAPANDI** | SIRADAKİ PARÇA ve ABONE OL **13,5:1**, TESLİMAT TAMAM **7,2:1**, büyük "ZAMAN KURYESİ" **8,3–8,7:1** (v2'de ≈3:1). Yeni satır için **G6** |
| **Ö7** Altyazı bandı | **KISMEN** | Eskiler kapandı; sözleşme madde numaraları dekoratif. Yeni bant ihlalleri: **G2**, **G7** |
| **Ö8** Karanlık çekimler | **KISMEN** | c1_toprak 0,154 (kapandı). Hasta odası (189,7–193,7 sn) hâlâ 0,043. Düşük öncelik |
| **Ö11** Punto tabanı | **KISMEN** | Galeri etiketleri değişmedi: "KIYMETLİ ŞEYLER" 25 px, "KÜTÜPHANELER" 27 px, diğerleri 30 px (56,7–64,9 sn). Gerçek <34 px yazı 17 tane (%5) |
| **Ö12** Büyük harf tutarlılığı | **KAPANDI (bir istisna)** | `tr_upper` her yerde: GİOVANNİ, CAVALCANTİ, MACHİAVELLİ, SALVESTRO DE' MEDİCİ… İstisna: bitiş ekranındaki "2/7 · COSIMO" (**G6**). "ITALIANO" belgedeki yabancı sözcük olarak kabul edilebilir |
| **K4** zoomthru sıklığı | **AÇIK** | 13'ten 15'e çıktı; 8'i 0,6 sn ya da daha kısa. Vestibüler konfor; KÜÇÜK |
| **K5** Zaman ekseni yılları | **KAPANDI** | Yıllar artık defterde: 33–34 px, **4,7–6,6:1** (416–431 sn) |
| **K6** Çarpının harfleri örtmesi | **KAPANDI** | BORÇ ve FAİZ çarpıları ince ve yarı saydam (`check_b.png`) |
| **Denetim notu** (`qa_yerlesim` kör noktaları) | **KISMEN** | Levha × levha ve yazı × yazı çakışması artık yakalanıyor; GİOVANNİ×COSSA, poliçe×BRUGGE ve 13 MADDE düzeltildi. Hâlâ görmediği üç şey: sprite damgalar, `c2_masa` yazıları ve kısmen kadraj dışında kalan yazı. Bu yüzden "İHLAL 0 · altyazı şeridi 0" derken G1, G2, G4, G5, G7 ve DE ROOVER'ı kaçırdı |
| E1–E3, Ö1–Ö3, Ö10, K1, K2 (tur 2'de kapanmıştı) | **KAPALI KALDI** | 31 EKİM 1737 **17,4:1**; 18 ŞUBAT 1743 **19,9:1**; nakarat **10,5 / 17,2:1**; levhalarda kenar ve HUD ihlali yok. Kapaklar: kahraman yazı kontrastı **12,0 / 12,7:1**; 168 px'te kenar grisi 38, gri<25 payı %10,6 (`k168_dark_v3.png`) |

---
## 4. Gerilemeler ve yeni sorunlar

**G1 · ÖNEMLİ · Defter sayfası çekimlerinde yarım sözcükler ve yarım sayılar kadrajda kalıyor (yeni masa defteri çekimleri).**

Kamera sağ sayfaya geçince sol sayfanın yazıları kenarda kesik kalıyor ve orada 2,4–6 sn duruyor:
- **Catasto (#85), ≈500,4–502,8 sn, x 0–270:** "ASTO · 1427", "80 HANE" → "0 HANE" (aslı 9.780), "R HESABA GÖRE" (damga), "LI SERVET", "7 HANE" (aslı 137; y≈1000–1030, altyazı bandında). Yarım sayılar yanlış okunabilir (`catasto_left_edge.png`).
- **Çifte kayıt (#72), ≈424–431,6 sn, x 0–450:** "TE KAYDIN İZİ", "EDİCİ İCADI", "1360" ve "1400" yılları, "MEDİLER" damgası (`iz_seq.png`).
- **Kasa (#83), ≈480,0–484,6 sn:** "APALIĞIN RESMÎ / ASA MEMURLUĞU" (x 0–340, y≈40–160). Bu, o anda anlatılan başlık (replik 129); `out_p1/kurul/tam_10_483s.png` ve `kasa_seq.png`.

**Yapılacak:**
- Kamera bir sayfadan ayrılırken o sayfanın etiketleri sönsün. Ya da kamera durduğunda sol sayfa ya tümüyle kadraj dışında ya da ≥90 px payla içeride olsun.
- `qa_yerlesim`'e kural: kutusunun %5–95'i ekranda olan bir yazı ≥0,5 sn kalırsa İHLAL.

**G2 · ÖNEMLİ · "ETMEDİLER" damgası iki satırlık altyazının altında (gerileme).**
- Yer: #72, 416,5–421,4 sn. Harfler y≈872–956, kâğıt fişi y≈995'e iniyor (x≈735–1280).
- Aynı anda replik 113 iki satır (416,08–421,43): YouTube'un altyazı kutusu harflerin alt ≈%20–50'sini örter. Damga bölümün vurucu sözcüğü (`band_edge_v3.png`).
- Yapılacak: damgayı en az 80 px yukarı al (harflerin altı ≤870 olsun) ya da kameranın aşağı kayışını geciktir.

**G4 · KÜÇÜK · "FRANSIZCA" damgası sağ kenara dayanıyor (gerileme).**
- Yer: #8, ≈45–48,8 sn. Son "A"nın sağ ucu 46,6 sn'de x≈1905, 48,2 sn'de x≈1915 (v2'de ≤1661).
- Neden: ENG-D ile artık gerçekten uygulanan crane/hand kamerası damgayı sağa itiyor. Sözcük okunuyor ama kenara 5–15 px kalıyor (`fransizca_seq.png`, `deroover_itiraz_fr.png`).
- Yapılacak: damganın sağ ucu ≤1830 olsun (yaklaşık 100 px sola ya da %8 küçült).

**G5 · KÜÇÜK · "CİOMPİ LONCASI" etiketi sağ kenarda.**
- Yer: #48, 271,6–277,7 sn. Y3 düzeltmesiyle bant dışına çıktı ama x≈1420–1887 oldu: güvenli çizginin 57 px dışında, kenara 33 px (`band_edge_v3.png`).
- Yapılacak: en az 60 px sola al.

**G6 · KÜÇÜK · Bitiş ekranındaki "2/7 · COSIMO: SÜRGÜN VE DÖNÜŞ" satırı.**
Kontrastı iyi (17,7:1) ama üç sorunu var (`outro_next_line.png`):
- **Punto:** 28 px; kurulun 34 px tabanının altında.
- **Yazım:** "COSIMO" noktasız; 10 sn önceki levha "COSİMO" diyor. `compose.NEXT_PART_LINE` `tr_upper`'dan geçmiyor.
- **Konum:** y≈973–994. İzleyici bitiş ekranı öğesine tıklamak için fareyi gezdirdiğinde ya da ekrana dokunduğunda oynatıcı denetim çubuğu tam bu bölgeyi örter.

Yapılacak: ≥34 px, `tr_upper`, en az 40 px yukarı.

Alan dışı not (PK karar versin): ekrandaki "SIRADAKİ PARÇA · 2/7" yazısı, P2 yayınlanana dek sol yuvaya konacak "İzleyiciye en uygun video" öğesiyle çelişebilir.

**G7 · KÜÇÜK · Diğer bant ihlalleri.**
- "KENDİ DEFTERİ": #72, 429,8–431,6 sn, y≈939–970. Tek satırlık replik 117 aynı sözcükleri söylüyor; risk düşük. G2 düzeltmesiyle birlikte yukarı alınabilir.
- "%29,8 · 137 HANE" parçası: ≈500,4–502,8 sn (G1'in parçası).

**G8 · KÜÇÜK · "DEFTERLER GÖSTERİR" okunamayacak kadar kısa.**
- Yer: ≈517,2–517,7 sn, yaklaşık 0,5 sn; mum alevinin üstünde.
- İki sözcük için en az 1,2 sn gerekir. KA2-N3'e katılıyorum (başkanın listesinde #4).

**Bilgi (sorun değil):**
- Işık geçişlerindeki yıldızın kalkması ve 39 sert kesme flaş ölçümünü değiştirmedi. En büyük tek kare adımı −0,35 (545,2 sn, kesme); tekrarlanan bir parlaklık değişimi yok.
- Bitiş ekranı 10 sn boyunca koyu (ortalama parlaklık ≈0,03), ama üstündeki yazılar 7–18:1.

---
## 5. Kullanıcının sorusu: "Bu çizim tarzı ucuz mu, yapay zekâ gibi mi?"

**Yanıtım değişti, olumlu yönde.** Gerçek harfli sayfalar (Machiavelli ve Cavalcanti, Ciompi talepleri, evlilik sözleşmesi, masa defterleri) ve kâğıt fişli damgalar tur 2'de "yer tutucu" dediğim hissi büyük ölçüde kaldırdı. Yapay zekâ izi hâlâ yok.

Kalan şablon izleri:
- açılıştaki 1737 sözleşmesi hâlâ zikzak çizgili (34–56 sn);
- koyu yuvarlak etiket kalıbı hâlâ sık;
- 534,5–536 sn'de iki sayfa neredeyse boş (`out_p1/kurul/tam_11_536s.png`; gerçek harfli sayfalar için `pages_seq.png`).

---
## 6. En emin olmadığım nokta

1. **G2'nin büyüklüğü:** altyazı kutusunun gerçek yüksekliği oynatıcıya, altyazı boyutuna ve denetim çubuğunun görünüp görünmediğine bağlı. Örtülen kısım harflerin %20'si de olabilir %50'si de.
2. **G1'in algısı:** belge üzerinde gezinen kamerada kenarda kesilen yazı bir anlatım alışkanlığı da sayılabilir. Ben ÖNEMLİ dedim, çünkü kamera durduktan sonra yarım sayılar ("80 HANE", "7 HANE") 2,4 sn kadrajda kalıyor.
3. **Kontrast yöntemi:** yüzdelik yöntemi ±%20 sapabilir; döndürülmüş yazıda (VİA PORTA ROSSA) düşük çıkıyor. Kritik maddeleri kareden gözle doğruladım.
