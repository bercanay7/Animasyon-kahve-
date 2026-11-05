# TE2 — Teknik kalite · Erişilebilirlik / Okunurluk — Medici Parça 1 · TUR 3b (v3.1 gerileme kontrolü)

Üye: TE2. Mercek: telefon, TV, aydınlık ve karanlık ortam. Önceki raporum: `kurul/tur3/TE2.md`.

**Sınırlarım:** videoyu oynatamadım, sesi dinleyemedim. Altyazının oynatıcıda nereye düştüğünü görmedim; stil rehberindeki bandı (y 938–1042) varsaydım.

---
## 1. Karar

**ONAY: 9,4 / 10.** Tur 3'te 9,0 vermiştim.

| Alan | Tur 3 | Tur 3b |
|---|---|---|
| Fotosensitivite | 10 | 10 |
| SRT | 9,5 | 9,5 (altyazı değişmedi) |
| Yerleşim, kenar payı, HUD | 8,5 | **9,0** |
| Kontrast ve punto | 9,0 | **9,5** |
| Karanlık ve aydınlık ortam | 9,0 | 9,0 |
| Kapak | 9,5 | 9,5 |

**Gerekçe:**
- Tur 3'te "bunlarla 9,4" dediğim üç maddenin üçü de kapandı: DE ROOVER damgası fişli, ETMEDİLER bandın dışında, defter sayfalarından ayrılan kameranın arkasında kalan etiketler sönüyor.
- G4–G8 de kapandı.
- Yeni bulduklarım dört küçük madde (§4). Hiçbiri önemli ya da engelleyici değil.

---
## 2. Ne yaptım

Tur 3 betiklerimi v3.1'e karşı yeniden koştum. Aynı anda tek ağır işlem çalıştırdım, render yapmadım. Betikler ve kanıtlar `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/te2_t3b/` altında (JPEG, her biri ≤0,3 MB).

- **Flaş ve karanlık:** v3.1'in 14.437 karesinin tamamı.
- **Yazı kutuları:** motorun yalıtılmış kopyasında 306 kare çizdirdim, 5.747 kayıt topladım. Denetim: kenar, HUD, altyazı bandı ve yazı × yazı çakışması.
- **Gerçek piksel kontrastı:** 1.538 yazı örneği ve 26 damga/yaldız sprite'ı.
- **Hedefli kareler:** yaklaşık 60 tam çözünürlüklü kare; #83 için ayrıca kare kare keskinlik ölçümü.
- **Okuduklarım:** `KURUL_BRIFI_P1_TUR3B.md`, `tur3_duzeltme_listesi.md` (#34–#41), `duzeltme_tur3/SCN-3.md` ve `ENG-E.md` (TE2 bölümleri), `qa_flow_v31.txt`, `uretim_v31.log`.
- **Altyazı:** md5 `336461a5…`; tur 3'teki dosyayla aynı.

| Ölçüt | v3 | v3.1 |
|---|---|---|
| Yazı örneklerinde kontrast medyanı | 8,9:1 | **8,9:1** |
| Benzersiz yazıların en iyi anında <4,5:1 | %8,1 | **%7,6** (kalanlar dekoratif belge numaraları ve geçiş anları) |
| Damgalar | 4,5–6,7:1; bir damga fişsiz (≈3,5:1) | **4,5–6,6:1, hepsi fişli** |
| Yazı × yazı çakışması | 0 | **0** (yalnız dekoratif madde numaraları, 54,8 sn) |
| Flaş: 1 sn içindeki dönüm noktası (WCAG eşiği 6) | genel 2, bölgesel 4 | **genel 2, bölgesel 4**; doygun kırmızı ≤%0,6 |
| Kare ortalaması <0,03 olan süre | 15,3 sn | 16,9 sn: koyu bitiş ekranından. Oradaki yazılar 8–17:1, sorun değil |
| 34 px'ten küçük gerçek yazı | 17 | 19 (iki yeni 30 px etiket: G12) |

---
## 3. Tur 3 maddelerimin durumu

| Madde | Durum | Kanıt (v3.1) |
|---|---|---|
| **G1** Defter sayfası çekimlerinde yarım sözcük ve sayı | **KAPANDI** | #72: 425–431,6 sn'de sol sayfa etiketleri ve damga sönüyor; "1400" kenarda alfa 0,36 ile kayboluyor; yarım sözcük yok. #85: 500,4–502,8 sn'de "80 HANE" / "7 HANE" artık yok, "137 HANE" sönerek gidiyor. #83 (yeniden kuruldu): kamera sağa kaydıkça "22 YIL / KESİNTİSİZ" sönüyor (484,6–484,9). 1737 belgesi: 37,6 sn'de mühür altındaki ad kenarda sönüyor. Grafikler (çetele, eksen) kenarda kesik kalabiliyor; yazı değil, kabul (`g1_72.jpg`, `g1_85.jpg`, `k83_end.jpg`). Yan etki için G11 |
| **G2** ETMEDİLER altyazı bandında | **KAPANDI** | 420,3 sn: harfler y 689–753 (v3'te 872–956), 4,7:1 |
| **G7** KENDİ DEFTERİ ve "%29,8 · 137 HANE" bantta | **KAPANDI** | KENDİ DEFTERİ y 803–831 (430,4 sn); "%29,8 · 137 HANE" y≈774 (498,6 sn) |
| **Y5** BELGE · DE ROOVER fişsiz | **KAPANDI** | #80, 467,2–468,4 sn: kâğıt fişi üstünde **6,6:1**; tiara artık harflerin üstünde değil (`deroover_hud_v31.jpg`) |
| **G4** FRANSIZCA sağ kenarda | **KAPANDI** | 48,2 sn: harfler x ≤1748, çerçeve ≈1830; harflerin altı y ≤885, bandın dışında (`edges_v31.jpg`) |
| **G5** CİOMPİ LONCASI sağ kenarda | **KAPANDI** | 273,1 sn: x≈1323–1827, y 879–909, **5,9:1** |
| **G6** Bitiş ekranı satırı | **KAPANDI** | "2/7 · COSİMO: SÜRGÜN VE DÖNÜŞ": 34 px, **17,4:1**, harfler y≈920–946. Denetim çubuğu bölgesinin üstünde; bitiş ekranında altyazı yok |
| **G8** DEFTERLER GÖSTERİR kısa | **KAPANDI** | ≈514,4 sn'den mum geçişine (≈517,3) dek ≈3 sn; 40 px, **16:1**, y 824–855 (`defterler_v31.jpg`) |
| **Ö7** Altyazı bandı | **KAPANDI** | Bantta yalnız dekoratif belge numaraları kaldı (XII/XIII, 54–56 sn) |
| **Ö12** Büyük harf tutarlılığı | **KAPANDI** | Bitiş satırı da "COSİMO" |
| **Y6** Kapak yankısının kenar payı | **KISMEN (değişmedi)** | Başlık bloğu x 60–1731, "İ" noktaları y 27. KÜÇÜK |
| **Y8** HUD perde rakamları | **AÇIK** | Hâlâ 21 px. KÜÇÜK |
| **Y9** SRT'deki diğer bölünmeler | **AÇIK** | Altyazı değişmedi: "öteki │ kıymetli", "kısa │ ömürlü", "en │ eski", "torununun │ oğlu", "kimse │ istemeden"; 45 ve 43 karakterlik satırlar. KÜÇÜK |
| **Ö8** Karanlık hasta odası | **KISMEN (değişmedi)** | 189,7–193,7 sn: kare ortalaması 0,043. Düşük öncelik |
| **Ö11** Punto tabanı | **KISMEN** | Galeri etiketleri 25–30 px (56,7–64,9 sn) değişmedi; iki yeni 30 px etiket: G12 |
| **K4** zoomthru sıklığı | **AÇIK** | 15 kullanım. KÜÇÜK |
| **Denetim notu** (`qa_yerlesim`) | **KISMEN** | "Yarım yazı" UYARI kuralı eklendi ve çalışıyor (55,8 sn uyarısı). Kendi kamerası olan türlerin yazısını ekran uzayında hâlâ görmüyor; G10'u bu yüzden kaçırdı. Başkanın notuna göre bu, P2 öncesi motor işi |

---
## 4. v3.1 gerilemeleri ve yeni bulgular

**G9 · KÜÇÜK · #83'te özetin son hali yalnız bulanık bir anda görünüyor (yeni kurulum).**
- Yer: ≈485,2–485,95 sn, yaklaşık 0,7 sn. Şeridin son hali şu: "1422 · 22 YIL + 18 YIL · KESİNTİSİZ / ARALIKLI · MEDİCİ'DE KALDI".
- Bu süre boyunca kamera geri çekiliyor ve hareket bulanıklığı var (keskinlik ≈1.500'den ≈450'ye düşüyor). Hemen ardından kayma geçişi geliyor.
- "MEDİCİ'DE KALDI" bu yüzden ancak yarım okunur. Anlatım ve altyazı aynı sözü taşıdığı için bilgi kaybı yok.
- Ara satırlar keskin anda okunuyor (484,6 sn: "+ 18 YIL" 9,4:1, "ARALIKLI" 8,6:1).
- Yapılacak: son durum en az 1,2 sn keskin kalsın. Geri çekilme daha erken başlasın ya da "MEDİCİ'DE KALDI" "aralıklarla" sözcüğünde yazılsın (`k83_end.jpg`, `k83_485_6.jpg`).

**G10 · KÜÇÜK · #83 başlığı HUD'un köşesine değiyor (yeni kurulum).**
- Yer: ≈476,0–477,5 sn. "…KASA MEMURLUĞU" başlığının son "U"su ve "Ğ"nin kırması HUD kutusunun sol alt köşesine değiyor (HUD x 1548, y 138; harf tepeleri y≈128–145, birkaç piksellik değme).
- Harfler okunur kalıyor. `qa_yerlesim` bunu görmüyor (denetim notu).
- Yapılacak: başlığın sağ ucu ≤1520 olsun ya da başlık y ≥150'ye insin (`k83_hud_edge.jpg`, `deroover_hud_v31.jpg` alt şerit).

**G11 · KÜÇÜK · 1737 belgesinde imza adlarının asimetrisi (G1 söndürmesinin yan etkisi).**
- 39,6 sn'deki genel planda mavi mührün altında "LORRAİNE TARAFI" (4,7:1) var, ama kırmızı mührün altı boş: "ANNA MARİA LUİSA" geri gelmiyor.
- Luisa etiketi yalnız 36,6–37,6 sn'de görünüyor; kamera hareketinden yumuşak ve soluk (≈2,2–3,5:1). v3'te de bu anda böyleydi.
- Yapılacak: genel planda iki ad birlikte görünsün; mühür altı mürekkebi ≥4,5:1'e koyulaştırılsın (`signatories_v31.jpg`, `c0_contract.jpg`).

**G12 · KÜÇÜK · #95 ve #96'nın yeni etiketleri 30 px.**
- "TÜRKÇESİ ÖZET · ÇEVİRİ BİZE AİT" (559,7–566,2 sn) ve "TÜRKÇE SATIRLAR ÖZET · ÇEVİRİ BİZE AİT" (566,2–569 sn): kontrast 10,7–11:1.
- İkisi de altyazı bandının üstünde (y ≤903). İki satırlık replik 151 (559,95–565,28) ile çakışmıyor; "CAVALCANTİ'YE GÖRE" de y 834–865'te.
- Tek sorun punto: 34 px tabanının altında, telefonda küçük. Yapılacak: 34 px (`p95_v31.jpg`).

**Gerileme olmayan yeni öğeler:**
- **#95 Türkçe satırlar:** 54–63 px, 8,9–10:1. Satır aralığı sıkılaştı ama ≈1,35 em; okunur.
- **#88 sırt etiketleri:** "1397", "1397 – 1420", "1420" 6,3–7,6:1. "1397" 517,2 sn'de sol kenara yakın (x≈70) ama tam.
- **1737 belgesinin asemik yazısı:** okunmak için değil. Tur 3'te "şablon" dediğim zikzak çizgilerin yerini aldı; iyileşme.
- **Flaş:** hâlâ temiz.

---
## 5. En emin olmadığım nokta

1. **G9:** hareket bulanıklığının oynatma hızında ne kadar rahatsız ettiğini kareden kestiriyorum. 24 fps'te göz bulanıklığı hareket olarak okur; sorun yazıyı okumaya kalan sürenin kısalığı.
2. **G10:** HUD ile değme birkaç piksel ve kısa süreli. Kare üstünde gözle ölçtüm; piksel maskesiyle doğrulamadım.
