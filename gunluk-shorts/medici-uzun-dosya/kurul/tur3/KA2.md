# KA2 · TUR 3 — Medici Parça 1, v3 (`out_p1/medici_P1.mp4`, 601,54 sn)
Mercek: kaynak denetçisi, yöntem dürüstlüğü, hassasiyet ve hukuk (veto).

## 1. Karar

**ONAY — 9,0/10. Vetom kalktı.**

Tur 2'de ONAY koşulu olarak üç madde koymuştum: D1 hançer, D2 HUD yılları, D3 "son üye" levhası. Üçü de v3'te kapandı. 465–476 sn arasında gerileme yok. D4–D14 maddelerimin hepsi de kapandı.

Puanı 9,2 değil 9,0 vermemin nedeni, düzeltmelerle gelen iki yeni ÖNEMLİ sorun (N1 ve N2). İkisi de engelleyici değil ve ücretsiz düzeltilebiliyor. İkisi düzelirse puanım 9,4 olur.

## 2. Neye dayandım (sınırlarım)

- **Videoyu oynatamadım, sesi dinleyemedim.**
- **v3'ten kendim çıkardığım ≈80 kare.** Zamanlar `timeline.json` sözcük çapalarından seçildi. Ses ve zaman çizelgesi v2 ile aynı (dosya tarihi 4 Kasım 22:13; toplam 590,23 sn).
  - Papa dizisi: 465,0–475,2 sn arası 12 kare.
  - Konstanz: 440,6–445,0 sn arası 6 kare + tam çözünürlüklü kırpım (444,3 / 444,8 sn).
  - Diğer bütün tur 2 maddeleri.
- **Kod:**
  - `scenes_c2.py:217`: `kind="papa", action="admonish"`.
  - P1 sahnelerinde `threat` ve `dagger` aramam boş döndü.
  - `scenes_c2.py:170–177`: Konstanz çekimi.
- **Belgeler:** `KURUL.md` (tur 2 sonucu, v3 planı), `duzeltme_tur2/SCN-1.md` ve `SCN-2.md`, `out_p1/qa_flow_v3.txt` (19 GEÇTİ, 0 KALDI; yerleşim ve dönem İHLAL 0), `yayin/studio_paketi_P1/00–05`, `SURUM_KUNYESI_P1.md`.
- **Birincil metin karşılaştırması:** ekrandaki yeni İtalyanca satırları `kurul/teyit_P1.md`'deki KAY alıntılarıyla karşılaştırdım:
  - Machiavelli IV (it.wikisource);
  - Cavalcanti IV.3 (Polidori 1838).
- **Saklanan kanıtlar** (`/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/ka2t3/`): `g02_papa.png`, `g03_papa.png`, `g19_konstanz_crop.png`, `g16_mach.png`, `g13_defter.png`. Diğer kare dökümlerini sildim.

## 3. Tur 2 maddelerimin durumu

| Madde | Durum | Kanıt (v3) |
|---|---|---|
| **D1** Papanın hançeri (VETO) | **KAPANDI** | Bkz. aşağıdaki not |
| **D2** HUD yılları | **KAPANDI** | Dante "lanetli çiçek" (124,4 sn) HUD gizli. Villani darphanesi (133,5 sn) 1338. Machiavelli c1s20–21 (258, 261, 264,5 sn) gizli. Uffizi "BUGÜN" (82,5 / 84,5 sn) gizli, "BUGÜN" + "UFFİZİ" levhaları var. Çeyiz (307,0 sn) ve "EVLİLİK SÖZLEŞMESİ · Piccarda Bueri · çeyiz · 1.500 florin" (311,0 sn) 1385. Kefalet/fidye (447,5 / 450,0 sn) 1418. Küçük bir artık var: N4 |
| **D3** "Son üye" levhası | **KAPANDI** | 12,2 sn: "ANNA MARIA LUISA · MEDİCİ HANEDANININ SON ÜYESİ" (iki satır) |
| **D4** Villani levhası | **KAPANDI** | 176,4 sn: "1300'DE PERUZZİ ORTAĞI · YÖNETTİĞİ BUONACCORSİ 1341'DE BATTI" (DBI ile uyumlu) |
| **D5** Mezar yazıtı | **KAPANDI** | 458,5–463,5 sn: taşta harf harf "IOANNES QVONDAM PAPA"; levha "ESKİ PAPA · ÇEVİRİ BİZE AİT". de Roover n. 826'daki "XXIII" taşta yok; anlatım "eski papa" dediği için kabul |
| **D6** Catasto | **KAPANDI** | 487,5–491,8 sn: "Catasto dairesi"; hane reisleri masaya beyanname getiriyor; "HANE REİSLERİNİN BEYANNAMESİ · PORTATA"; Komün kalkanı. Online Catasto'nun "declarations" bilgisiyle uyumlu |
| **D7** "1426'DA ÇEKİLDİ" | **KAPANDI** | 401,0 sn: çarpı yalnız kese simgesinde; "SERMAYE / 1426'DA ÇEKİLDİ" çarpının dışında |
| **D8** "BELGE · DE ROOVER" süresi | **KAPANDI** | 465,6 sn'de basılıyor, papalık salonu çekiminde de duruyor (467,2 / 468,5 sn): ≥2,9 sn |
| **D9** "KLASİK BİR ÖRNEK" | **KAPANDI** | 354,5 sn: "BRUGGE · KLASİK BİR ÖRNEK" kendi çekiminde. "BARSELONA'YA ÇEKİLMİŞ POLİÇE" el ara planına taşındı (359,0 sn) |
| **D10** Sayaç | **KAPANDI** | 515,2–516,6 sn: 5.000'lik adımlarla sayıyor, "+" yalnız son değerde ("150.000+") |
| **D11** Loggia | **KAPANDI** | 141,4 sn (1338): sağ kenarda loggia yok. 1378 çekimlerinde (216,5, 219,5, 224,9, 241,5 sn) bitmiş loggia görmedim |
| **D12** 1520 mührü | **KAPANDI** | 577,5 sn: 6 toplu, üst topu zambaklı mühür (1465 sonrası biçim) |
| **D13** Yoksullar | **KAPANDI** | 571,0 / 573,5 sn: biri ön planda büyük ve kadrajla kesik, ikisi arkada farklı boyda. Saygın duruş, hassasiyet sorunu yok |
| **D14** "Temsilî" cümlesi | **KAPANDI** | `02_aciklama.txt` ve `03_sabit_yorum.txt`: "madalya portreleri TEMSİLÎ damgasıyla …; bütün figürler temsilîdir". Lorenzo (533,8 sn) ve Cosimo (582,0 sn) madalyalarında "TEMSİLÎ" var |
| **465–476 sn gerileme kontrolü** | **TEMİZ** | Hançer yok. Damga ve levha çakışması yok. "AFOROZ TEHDİDİ" (473,4 sn) papanın kolunun üstünde, figürle çakışmıyor |
| Y8 kulak kontrolü (tur 2) | **AÇIK, kullanıcıda** | Ses değişmedi. `00_yayin_adimlari.txt` adım 0'da yazılı |
| Y9 `notlar_c2.md` eski tablo | **AÇIK** (küçük kayıt temizliği) | Hâlâ "TRACY PARKS", "VENEDİK 1407", "152.820" satırları var (34, 40, 52). Video ve paketle ilgisi yok |
| Ö6 Studio "Yapay içerik" | **Şerhim kayıtlı**, engellemiyorum | `SURUM_KUNYESI_P1.md` §YouTube Studio; `00_yayin_adimlari.txt` 1.2 |

**D1 notu (kareler 465,0–475,2 sn; kanıt `g02_papa.png`, `g03_papa.png`):**
- Papa şiddetsiz `admonish` jestinde, kurşun mühürlü belgeyi (bulla) omuz hizasında uzatıyor (472,0–475,2 sn); Giovanni mitrayla eğiliyor.
- Araya mitra ara planı girmiş (470,2 / 471,2 sn): Giovanni'nin elleri mitrayı tutuyor, beyaz yenli papalık eli işaret ediyor.
- Papalık salonu yeni: anahtar ve tiara dokuması, taht.
- Görüntü de Roover n. 45'le ("threaten … with excommunication … restore the pledge") uyumlu.
- P1'de `threat` ve `dagger` kalmadı.

## 4. Gerilemeler ve yeni sorunlar

### ÖNEMLİ (engelleyici değil; ücretsiz düzeltme önerilir)

**N1. Konstanz çekimi (≈443,6–444,9 sn): kardinalin eli öndeki figürün ensesine değiyor.**
- **Ne görünüyor:** "indirdi" sözcüğünde kızıl cüppeli kardinal (`kind="kardinal", action="point", dir=-1`, `scenes_c2.py:174`) sola doğru işaret ediyor. Ama hemen solundaki siyah cüppeli figürün arkasında duruyor. Bu yüzden kolu o figürün başının hizasından geçiyor, eli ensesinde/başının arkasında bitiyor.
  - Tam çözünürlükte el ≈(1555, 550); kardinal x≈1540–1820, siyah figür x≈1460–1630.
  - Kanıt: `g19_konstanz_crop.png`.
- **Neden önemli:** "Konstanz Konsili onu papalıktan indirdi" anlatımıyla birlikte, bir din adamının birini ensesinden tutması, yaka paça götürmesi gibi okunabiliyor. Kaynakta böyle bir şey yok. Bu, D1 türünden (din adamı figürüne belgesiz zor kullandırma) bir okumaya kapı aralıyor.
- **Neden veto değil:**
  - silah ve yaralanma yok;
  - temas belirsiz ve ≈1,3 sn sürüyor;
  - anlatımda Cossa'nın kendisi gösterilmiyor (düşen tiara simgesi var);
  - Cossa'nın 1415'te gözaltında tutulduğu da tarihî olgu (DBI, Martino V bölümü).
- **Yapılacak (tek çekim):**
  - işaret eden kardinal öne ya da sola alınsın, kolu kimseyi kesmeden tahta ve tiaraya uzansın; ya da
  - jest `talk` olsun ve işaret işini düşen tiara görsün.

**N2. Machiavelli ve Cavalcanti sayfalarında İtalyanca özgün satırların altında Türkçe özet var; ekran bunu çeviri gibi sunuyor (≈560,0–568,4 sn).**
- **Ne görünüyor:** v3'te "gerçek harfli sayfalar" geldi (kanıt `g16_mach.png`).
  - Cavalcanti sayfası (560–568,4 sn): "…non debbe aver dolore del partimento dalle mondane sollecitudini, per passare ai perpetuali riposi…" ve altında "kimse dünyevi tasaları sonsuz huzurla değiş tokuş ettiği için kederlenmemeli".
  - c2s31'de (566,3–568,4 sn) iki sayfa yan yana. Machiavelli sayfası: "…Muoio contento… …quello che l'uomo si toglie, non quello che all'uomo è dato…" ve altında "huzurla gidiyordur ve kıskançlık, insana verilenden değil, istediğinden doğar."
  - Konum (tam çözünürlük, yaklaşık): Machiavelli sayfası x≈180–820, y≈290–870; Cavalcanti sayfası x≈1090–1730. İtalyanca satırlar y≈340–440.
- **Sorun:**
  - İtalyanca alıntılar doğru; KAY'ın okuduğu metinlerle birebir.
  - Ama Türkçe satırlar çeviri değil, özet. Machiavelli'de "si toglie" "kendi aldığı" demek, Türkçede "istediği". "ci fa odiare" "nefret ettirir" demek, Türkçede "kıskançlık doğar". Bu kaymayı KAY ◐ "zorunlu yama değil" diye işaretlemişti.
  - İki metin üst üste konunca kayma görünür hâle geliyor ve özet, özgün metnin çevirisi gibi okunuyor.
  - Açıklamadaki çeviri notu ("Sözleşmenin 3. maddesi ve Dante dizesindeki Türkçe karşılıklar bize aittir") bu iki yazarı kapsamıyor.
- **Yapılacak (ücretsiz; ses yaması gerekmez):**
  1. **En az şu (render yok):** `02_aciklama.txt`'deki çeviri cümlesi şöyle olsun:
     > "Sözleşmenin 3. maddesi, Dante dizesi ve Machiavelli ile Cavalcanti'den aktarılan sözlerin Türkçeleri bize aittir; Machiavelli ve Cavalcanti'nin sözleri özetle aktarılmıştır, ekrandaki İtalyanca satırlar özgün metinlerden kısa alıntılardır."
  2. **Önerilen (iki çekim):** iki sayfada Türkçe bloğun altına "ÖZET · ÇEVİRİ BİZE AİT" etiketi; biçim mezar levhasındakiyle aynı.

  Anlatım zaten dolaylı ("…onun ağzından … bir konuşma yazar: …") ve ekranda "MACHIAVELLİ'YE GÖRE · ANEKDOT" var. Bu yüzden ses yamasına gerek yok.

### KÜÇÜK

| # | Ne | Nerede | Önerim |
|---|---|---|---|
| N3 | Kâr rakamının kaynak damgası "DEFTERLER GÖSTERİR" yalnız mum geçişinde, ≈0,5 sn görünüyor; mum "E" harfini örtüyor. Anlatım "defterler … gösterir" diyor ve rakam ● (de Roover Tablo 8), bu yüzden yöntem açısından zarar yok (kanıt `g13_defter.png`) | 517,3–517,8 sn, x≈1155–1755, y≈835–890 | "defterler" sözcüğünde (514,45 sn) bassın ya da kaldırılsın |
| N4 | D2 mantığının artığı: "O KALEM · Istorie fiorentine · MEDİCİ SİPARİŞİ" çekiminde HUD 1429, ama nesne 1520'ler. Mühür zaten "nesne yılı 1520" ile çizilmiş | 575,6–580,0 sn | HUD gizlensin ya da karta "≈1520" eklensin |
| N5 | Bitiş ekranında "SIRADAKİ PARÇA · 2/7 · COSIMO", ama P2 yayınlanana dek tıklanan öğe "İzleyiciye en uygun video" olacak; bir haftalık vaat farkı | 592–601,5 sn | Kabul (PK2-Y2 başkan kararı; `00_yayin_adimlari.txt` P2 çıkınca değiştirmeyi yazıyor). Eylem yok |

### Paket: başlık testi T3 için kaynak üyesi görüşü

`00_yayin_adimlari.txt` §5: "Medici Ailesi (1/7): Faiz Yasaktı, Kilise Müşteri Oldu" (yalnız kaynak üyesi onayıyla).

- **KA2 olarak onaylıyorum.** İddia c2s9'un karşılığı ("…müşterilerinden biri, faizi yasaklayan Kilise'nin ta kendisiydi"). Bu ● dayanaklı: de Roover, "depositi a discrezione made by high churchmen … the Pope himself"; Camera Apostolica mevduatı.
- İroni kurumun maliyesine yöneliyor, inanca değil; videodaki tonla aynı.
- Olgunun özü için KA1'in onayı da alınmalı.

### Hassasiyet merceğiyle yeni sahneler: temiz

- **Stinche hücresi** (553–556,4 sn): taş duvar, parmaklıklı pencere, duvarda zincir halkası; Cavalcanti masada yazıyor. İşkence ya da zor kullanma yok. DBI ile uyumlu: "imprigionato e trattenuto alle Stinche", borç yüzünden hapis.
- **Catasto dairesi** (487–492 sn): saygın memur ve hane reisleri.
- **Papalık salonu:** anahtar ve tiara simgeleri saygılı.
- **El yakın planları:**
  - kese ve poliçe (356,8–359,0 sn);
  - mitra ve işaret eden papalık eli (470,2–471,2 sn);
  - kalem (575–580 sn).

  Yüz yok, temas yok, şiddet yok.
- **Ciompi taleplerinin Signoria'da okunması** (246,5 sn, "YAZILDIĞINA GÖRE"): Machiavelli III'teki dilekçe sunumuyla uyumlu.
- **Ölüm odası** (4,5–7,5 sn): yatakta siluet, onurlu.

**Sonraki parçalar için not (P1 dışı):** `cilt_anim.act_threat` hâlâ her çağrıda hançer ekliyor. P3'teki Pazzi sahnelerinde (c7) din adamları `threat` ile çiziliyor. Saldırgan rahiplerin (Maffei, Bagnone) hançer kullanması belgeli (genel bilgi, güven yüksek), bu yüzden orada doğru olabilir. Yine de tur 2'deki önerim geçerli: hançer yalnız açık `prop="dagger"` ile eklensin; din adamı + `threat` birleşimi QA'da uyarı versin. P3 kurulunda bakacağım.

## 5. Kullanıcının sorusu: "Bu çizim tarzı ucuz mu, yapay zekâ gibi mi?"

Yanıtım küçük ölçüde değişti. Tur 2'de ucuz ya da şablon hissi veren üç şey saymıştım: hançer, üç özdeş yoksul ve üst üste binen etiketler. Üçü de v3'te düzeldi.

Yeni el ve nesne yakın planları basit, "eldiven" gibi eller, ama üslupla tutarlı. YZ izi yok: harfler gerçek ve doğru, mimari tutarlı. v3'te gördüğüm tek "hata gibi" an Konstanz'daki kol çakışması (N1).

## 6. En emin olmadığım nokta

1. **N1'in okunuşu.** Çoğu izleyici kolu tahta doğru "işaret" olarak görebilir; ensesine dokunma okuması kare kare bakınca belirgin. Ağırlığı tam bilemiyorum. Bu yüzden önemli dedim, veto demedim.
2. **N2.** Türkçe izleyicinin İtalyanca satırları Türkçeyle karşılaştırması olası değil. Asıl risk yöntem dürüstlüğü (özetin çeviri gibi görünmesi), bu yüzden açıklama notunu asgari koşul saydım.
3. **Y8.** v2 sesinde üç bağımsız ASR "aforozla"yı "Aforoz'da" duymuştu; ses değişmedi. Bu kulak kontrolüyle çözülecek; kurul sesi dinleyemez.
