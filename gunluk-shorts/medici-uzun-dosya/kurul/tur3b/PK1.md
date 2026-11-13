# PK1 — TUR 3b · v3.1 gerileme kontrolü · Paket: kapak/başlık, tıklama vaadi

**Sınır:** videoyu oynatamadım, sesi dinleyemedim.

**Neye baktım:**
- v3.1 `out_p1/medici_P1.mp4`: 601,54 sn, 14.437 kare, v3 ile aynı süre. Kareleri ffmpeg ile çıkardım:
  - 0–3,9 sn, 0,25 sn adımla (yankı);
  - 591–594 sn, 1/12 sn adımla, ve 597 sn tam kare (bitiş ekranı);
  - 36,5 · 40,6 · 46,0 · 55,8 sn (1737 belgesi);
  - 68,3 · 339,5 · 346 · 389,5 · 390,5 · 394,5 · 413,2 · 432,0 · 487,0 sn (vaat ödemeleri ve bölüm çapaları).
- Yeni K1 (`kapak_P1_K1.jpg`, 16:47): kendi ölçümüm + `kapak_qa_P1.png/.json` (16:48).
- `studio_paketi_P1/00–05`, `YAYIN_TASLAK.md` §6, `tur3_duzeltme_listesi.md`, `duzeltme_tur3/ENG-E.md` §3, §5, §9.

Kanıtlar `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/pk1t3b/` içinde (JPEG, her biri ≤ 0,5 MB):
- `k1_v31_yakin.jpg`, `qa_feed_v31.jpg`;
- `yanki_v31.jpg`, `bitis_597_v31.jpg`;
- `belge_v31.jpg`, `belge_v31_kirpinti.jpg`, `vaat_bolum_v31.jpg`.

Disk için önceki turların kanıtlarını aynı adlarla JPEG'e çevirdim (`pk1/`, `pk1t2/`, `pk1t3/`; `.png` → `.jpg`). Bu turda proje dosyalarına dokunmadım.

## 1. Karar

**ONAY — 9,5 / 10 (değişmedi).** Tur 3'teki açık ve yeni maddelerimin hepsi kapandı. v3.1 benim alanımda gerileme getirmedi; iki yerde iyileştirdi:
- 1737 belgesi artık asemik el yazısıyla;
- kesedeki şaka "HEDİYE" başlığıyla daha açık okunuyor.

## 2. Tur 3 maddelerimin durumu

| Madde | Durum | Kanıt |
|---|---|---|
| **G1** QA görseli eski (9:58) | **KAPANDI** | QA 16:48'de yeniden üretilmiş. Akış maketinde iki Medici kapağı da **10:01** (`qa_feed_v31.jpg`). v3.1 süresi v3 ile aynı (601,54 sn), etiket doğru |
| **G2** YAYIN_TASLAK §6 m. 8 | **KAPANDI** | Şimdiki metin: "çıkış çekimi 10 sn; yuvalar 1,4. sn'de tam … sol yuva sonraki parça yayınlanana dek **'İzleyiciye en uygun video'** (… kurul PK2-Y2), yayınlanınca o parçanın videosu". Eski "son 7 sn / oynatma listesi" kalktı |
| **G3** ilk hafta bitiş ekranı vaadi (bilgi) | **KAPANDI, beklediğimden iyi** | `00_yayin_adimlari.txt` §2'ye iki satır eklendi: "P2'nin yayın tarihi kesinleşince sabit yorumun son satırına yaz" ve "P2 YAYINLANDIĞI GÜN: sol öğeyi P2 videosuyla değiştir" (PK2-N2) |
| Tur 3, en emin olmadığım #3: T3 onayı | **KAPANDI** | `00_yayin_adimlari.txt` §5: "kaynak üyeleri KA1 ve KA2 kurul tur 3'te onayladı (de Roover, papalık mevduatı ve Camera Apostolica…)" |
| Tur 3 §4 kalanı: 0:33–0:58 sözleşmede zikzak "sahte yazı" | **KAPANDI** | 36,5 / 40,6 / 46,0 / 55,8 sn: satırlar sağa eğik, kalın-ince vuruşlu asemik el yazısı (`belge_v31.jpg`). 2× kırpıntıda bile kalem izi gibi okunuyor (`belge_v31_kirpinti.jpg`). İlk dakikadaki "yer tutucu" izlenimi gitti |
| Tur 3, en emin olmadığım #1: Studio öğesi çerçeveye oturur mu | **AÇIK (buradan sınanamaz)** | Yuvalar aynı boyda (≈ 520×292 px), yalnız 54 px yukarı alındı. `00_yayin_adimlari.txt` "çerçevelerin üstüne yerleştir, dışına taşırma" diyor; yayın günü bir bakış yeter |
| İsteğe bağlı K3 (silüetli kapak) | **AÇIK (puanlanmadı)** | 48. saat verisine bağlı |

## 3. v3.1 gerilemeleri (alanımda)

**Bulmadım.** Sınadıklarım:

**K1 yeniden çizimi (`k1_v31_yakin.jpg`).**
- Belgede asemik yazı var; yankıyla aynı.
- Kilitteki beyaz parıltı ışınsız, yumuşak bir leke: Y5 kararıma uygun, kapağın en parlak noktası kilit (QA: parlak leke 1, odak payı 1,0).
- Ölçüler korunmuş:

| Ölçü | Değer |
|---|---|
| "MEDİCİ" büyük harfi | 132 px (%18,3); kendi eşik ölçümüm y 55–191 |
| Kontrast (hero / ikincil) | 10,1:1 / 14,0:1 |
| Kenar grisi (QA / kendi ölçümüm) | 38,4 / 38,0 |
| Gri < 25 payı | %8,3 |
| Bölge ihlali | 0 |
| Dosya boyutu | 0,26 MB |

- Yankıdaki parıltı sıcak yansımaya çevrilmiş, kapaktaki ise beyaz. Bu küçük fark tanınırlığı etkilemiyor: yazı, kilit, zincir ve belge birebir aynı.

**Yankı, 0–3,25 sn (`yanki_v31.jpg`).**
- Yeni K1 zemininde. 168 px'te kenar grisi 37,6–42,0 (ENG-E 37,8–44,5 ölçmüş).
- Işın yok. 3,25 sn'deki ışık geçişi yıldızsız.

**Bitiş ekranı (`bitis_597_v31.jpg`).**
- Çıkış 592,0 sn'de başlıyor, çerçeveler ≈ 592,8'de tam görünüyor. "9:53'ten" talimatı doğru: YouTube öğeleri çerçeveler belirdikten sonra geliyor.
- Yeni yerleşim: yuvalar y 556–848; "2/7 · COSİMO: SÜRGÜN VE DÖNÜŞ" satırı y 916–952, büyük ve okunur.
- Arma iki yuvanın arasında; her yanda ≈ 30 px pay var, çakışma yok.

**Vaat ödemeleri ve bölüm çapaları (`vaat_bolum_v31.jpg`).**
- 1:08: haritada aynı kilit.
- 5:39: "FAİZ GÜNAHTIR". 5:46: "KİLİSE: FAİZ = TEFECİLİK".
- 6:29,5–6:30,5: kese ve "FAİZ" yazısı; yazı üstü çizilince **"HEDİYE"** başlığı geliyor. K2'nin vaadi şimdi daha açık ödeniyor.
- 6:34,5: "MÜŞTERİ: KİLİSE".
- 6:53: DEBITORI/BORÇLULAR – CREDITORI/ALACAKLILAR. 7:12: GİOVANNİ. 8:07: CATASTO · 1427.
- Anlatım zaman çizelgesi değişmediği için 9 bölüm damgası geçerli.

**Paket metinleri.**
- 01–05 tur 3 ile aynı. SHA-256 ilk 16 hane: 02 `cc3c7b46…`, 03 `2b54f4c3…`, 05 ve `bolumler_P1.txt` `142585e6…`.
- Yalnız `00_yayin_adimlari.txt` değişti (`42464a86…`). Değişen kısımları satır satır okudum: bitiş ekranı 9:53'ten, P2 günü adımları, T3 onayı. Hepsi doğru.

## 4. En emin olmadığım nokta

1. **Bitiş ekranı öğelerinin çizili yuvalara oturması.** Studio'nun öğe boyutlarını buradan göremiyorum; yayın günü bir bakış gerekir.
2. **Asemik yazıda okunur harf parçaları.** Kapak 1280 px'te ve videoda 2× yakın planda okunur bir sözcük görmedim. ENG-E yer yer "la", "n" gibi parçalar olabileceğini yazıyor. 168 px kapakta görünmez; videoda tam boy belgede seyirci fark etmez diye düşünüyorum.
3. **Kapak testinin sonucu ve açılan zeminin TO'ya etkisi.** Ancak yayından sonra görülür.
