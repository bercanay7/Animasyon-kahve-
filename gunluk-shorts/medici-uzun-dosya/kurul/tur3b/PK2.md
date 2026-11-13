# PK2 — TUR 3b · v3.1 gerileme kontrolü · Mercek: "İLK KEZ GÖREN İZLEYİCİ" · Medici Parça 1

Önceki rapor: `kurul/tur3/PK2.md` (ONAY 9,1). Bu tur, tur 3'te açık, kısmen ya da yeni bıraktığım maddelerin v3.1'deki durumunu ve v3.1'in kendi alanımda getirdiği gerilemeleri sınıyor; genel inceleme değil.

**Sınır:** videoyu OYNATAMADIM, sesi DUYAMADIM. Dayandıklarım:
- **v3.1 videosundan kendi çıkardığım kareler** (`out_p1/medici_P1.mp4`, 601,54 sn, 14.437 kare; `uretim_v31.log`: kare hatası 0, seviye 4.1):
  - açılış 0–3,3 sn;
  - 0:20–5:47 ve 5:57–9:38 arasında 42 tarama karesi;
  - defter ve yakın plan çekimleri 6:56–8:38;
  - 6:53–6:56 çifte kayıt paneli;
  - 4:31 geçişi;
  - 8:54,5–8:56,4;
  - bitiş 9:52,0–10:01,3.
- **Belgeler:** `qa_flow_v31.txt` (102 çekim; 20 GEÇTİ / 1 UYARI), `out_p1/kurul/hareket.json` (v3.1), `kapak_qa_P1.json`, `yayin/studio_paketi_P1/00 ve 03` (18:16), `kurul/tur3_duzeltme_listesi.md`, `KURUL.md` (Tur 3 bölümü).
- **Kanıt kareleri** (JPEG, her biri ≤ 290 KB): `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/pk2v31/`.

## 1. Karar

**ONAY — 9,5 / 10** (tur 1: 6,0 → tur 2: 8,5 → tur 3: 9,1 → tur 3b: 9,5; eşik ≥ 9).

Tur 3'te 9,5 için tek ana madde olarak N1'i saymıştım; kapandı. Ayrıca açık ya da kısmen kalan beş maddem kapandı: N2, Y3, Y7, Y8, Y9. v3.1'in getirdiği iki gerileme küçük (§3); ikisi de puanı düşürmüyor.

## 2. Tur 3 maddelerimin durumu

| # | Madde | Durum | Kanıt (v3.1) |
|---|---|---|---|
| **N1** | Kart payı; üstten açık defter 102 sn'de dört kez | **KAPANDI** | Ayrıntı aşağıda |
| **N2** | Bitiş ekranı 9:53; P2 günü satırları | **KAPANDI** | Ayrıntı aşağıda |
| **Y3** | 8:54,5 sayfaları boş açılıyor | **KAPANDI** | Ayrıntı aşağıda |
| **Y7** | İtalyanca başlıklar; MİT damgası CREDITORI'yi örtüyor | **KAPANDI** | Ayrıntı aşağıda |
| **Y8** | Yankı eski K1 zemininde; kilitte beyaz parıltı | **KAPANDI** | Ayrıntı aşağıda |
| **Y9** | 4:31'deki kırmızı geçiş | **KAPANDI** | Ayrıntı aşağıda |
| Y5 | "FAİZ" bölüm etiketi | **Değişiklik yok** (başkan kararı, tur 3; kabul) | 5:41'deki kart hâlâ "DEFTERİN SİHRİ"; c2'nin görsel omurgasıyla uyumlu |
| Y4 | K2'ye tıklayan açılışta K1'i görüyor | **REDDEDİLDİ** (başkan, tur 2; kabul) | Değişmedi. Test ve Karşılaştır ölçecek |
| K4 | Yatak odası silueti | **Kısmen; kabul** | Değişmedi; kanca yankıda |
| K11 | Şablon hissi | **KAPANDI** | Mekân setleri tur 3'te ayrışmıştı; defter tekrarı da kırıldı (N1). Kart payı süre olarak %43–46'da kalıyor, ama artık tek bir kalıbın tekrarı değil |

**N1 — kart payı ve defter tekrarı.**
- **Kadrajlar (`defter31.jpg`):** üstten açık defter iki çekime indi: #72 (6:56,0–7:11,6) ve #85 (8:13,6–8:22,8).
  - **#83** (7:55,8–8:06,4): kızıl kadife papalık kasası yakın planı. El anahtarları bırakıyor; kapağa iğneli kâğıt şeritte "1422 · 22 YIL KESİNTİSİZ + 18 YIL ARALIKLI · MEDİCİ'DE KALDI" çetele çizgileriyle yazılıyor (`kasa485.jpg`).
  - **#88** (8:31,7–8:38,3): eğik açıdan sırtları "1397 / 1397–1420 / 1420" etiketli ciltler ve sandık. "150.000+ FLORİN KÂR" sayacı "yüz elli bini" sözüyle (515,4–516,0) eşleşiyor, 8:36,2–8:37,4 arasında tam okunuyor (`kar31.jpg`).
- **Dizinin ritmi:** "defter – kasa yakın planı – defter – ciltler/sandık". Üçüncü defterde "yine defter" demem artık mümkün değil.
- **Başlıklı açılış:** #72 "ÇİFTE KAYDIN İZİ | MEDİCİ'NİN FARKI" başlıkları ve eksen hazır açılıyor; #85 "CATASTO · 1427" ve sayaçla açılıyor.
- **Kart payı, tur 3'teki yöntemle** (kart + kart* + üstten defter; `qa_flow_v31`):

  | Pencere | v3 | v3.1 |
  |---|---:|---:|
  | Bütün video | %46,2 | **%43,3** |
  | 7:00–8:00 | %58 | **%51** |
  | 8:00–9:00 | %59 | **%37** |
  | 403,6–589,5 sn | %53 | **%43** |

- **Dürüstlük notu:** çekimler ve süreleri aynı; değişen kadraj. #83'ün kâğıt şeridini ve #88'i de kart sayarsam toplam %46,2'de kalıyor. İlk kez izleyen biri için önemli olan oran değil tekrar duygusu; o kırıldı.

**N2 — paket metni.** `00_yayin_adimlari.txt`:
- 35. satır: "9:53'ten videonun sonuna kadar".
- 46–47. satır: P2 tarihi sabit yoruma yazılacak; ilk hafta çerçevede başka video görüneceği açıklanıyor.
- 48. satır: "P2 YAYINLANDIĞI GÜN" sol öğe değişecek.
- Kareyle sınadım (`son31.jpg`): çerçeveler 9:52,3'te soluk, 9:52,9'da tam. 9:53 doğru. "2/7 · COSİMO: SÜRGÜN VE DÖNÜŞ" büyümüş ve İ'si noktalı (`outro31.jpg`).

**Y3 — 8:54,5 sayfaları.** Levhalar ve sayfalar ilk karede var. Kalem 8:54,6'da Machiavelli sayfasında; 8:55,0'da "…Muoio c…" yazılıyor; 8:56,4'te sol sayfada üç satır var, sağ sayfa başlıyor (`kalem31.jpg`). Kare farkı 534,5–539,0 arasında 2,6–3,0: hâlâ sakin, ama artık "yükleniyor" ekranı değil, yazılan bir sayfa. ≥ 4 sn süren durgun koşu (kare farkı < 3) v3.1'de yalnız iki tane: 548,0–552,0 (#93) ve bitiş ekranı (593–601).

**Y7 — çifte kayıt paneli.** "DEBITORI / BORÇLULAR" ve "CREDITORI / ALACAKLILAR" var. Kalem aynı kaydı iki sayfaya yazıyor, her sayfaya bir sikke. MİT damgası "derler" sözcüğünde sağ sayfanın alt köşesine iniyor (≈ x 1440–1760, y 490–670); başlıklara değmiyor (`mit31.jpg`, 6:53,0–6:55,9).

**Y8 — yankı.**
- Zemin yeni K1 ile eşleşiyor. 168 px kenar grisi: yankıda 39–43, kapakta 38. Koyu (< 25) pay: yankıda %12, kapakta %10.
- Belgede asemik el yazısı; kapakta da aynısı var (`yanki31.jpg`).
- Kilitteki beyaz parıltı 0,3–3,0 sn boyunca hiçbir karede yok; yalnız yumuşak, sıcak yansıma kalmış (`kilit31.jpg`).
- Kapak QA: K1 tek odak, kahraman kontrastı 10,1:1, koyu tema kenarı 38,4; geçti.

**Y9 — 4:31 geçişi.** 4:31,1–4:31,4 arasındaki taşıma geçişi artık koyu kahverengi bir mürekkep şeridi; kırmızı yok (`gecis31.jpg`). "Ezdi" sözcüğünden sonra kan çağrışımı kalmadı.

## 3. v3.1 gerilemeleri (kendi alanımda)

**G1 — [KÜÇÜK; algı] 7:56,3–7:58,3: büyüyen yakın planda kaba el.**
- N1 düzeltmesinin yan etkisi. #83'te anahtarları bırakan el ≥2× yakın planda, kalın konturlu, parmaksız bir yumru gibi duruyor (≈ x 800–1160, y 600–840; `kasa477.jpg`, `eller31.jpg`).
- İlk kez izleyen biri için videonun "ucuz" okunabilecek tek karesi bu; ≈2 sn sürüyor. Diğer yakın plan eller daha az sorunlu: 5:56,5'te açık el, 7:50,3'te mitrayı tutan iki el.
- SA1-E-1 ("eldiven eller") P2 öncesi motor işine yazılmış.
- P1 için ucuz çözüm (yalnız #83 segmenti):
  - eli kadraj dışında bırak, anahtarlar üstten kısa bir gölgeyle düşsün;
  - ya da yalnız kol yeni ve parmak uçları görünsün.
- Engelleyici değil.

**G2 — [KÜÇÜK] 7:56,8–7:57,5: şerit başlığı HUD'a değiyor.**
- "PAPALIĞIN RESMÎ KASA MEMURLUĞU" başlığının son "U" harfi (≈ x 1325–1558, y 85–165) HUD kutusunun (≈ x 1548–1846, y 73–137) altına ≈10 px giriyor (`hud31.jpg`).
- Kamera hareket ederken ≈0,7 sn; izleyici büyük olasılıkla fark etmez.
- Düzeltme: başlığı ≈60 px sola al ya da kamera yolunu başlık HUD'dan ayrık kalacak biçimde ayarla.
- `qa_yerlesim`'in OWN_CAMERA yazılarını görmediği biliniyor (düzeltme listesi #41, P2 öncesi motor işi).

**Gerileme bulmadığım yerler** (`tara31a.jpg`, `tara31b.jpg`):
- kapak yankısı ve künye;
- 1737 belgesindeki asemik yazı: okunmuyor ama yazı gibi duruyor, kanca bozulmuyor;
- FRANSIZCA damgası kadraj içinde;
- 1:07,8'de kilit;
- yol haritası çipleri;
- c1 sahneleri;
- c2'deki papa, Konstanz, catasto ve Cavalcanti sahneleri;
- Cosimo kartı;
- bitiş ekranı.

Ses, SRT ve bölüm damgaları değişmedi (`timeline.json` aynı); 9 bölüm geçerli.

## 4. En emin olmadığım nokta

- **G1'in ağırlığı.** Elin kabalığını tek karelerde görüyorum. Hareket hâlinde ve ≈2 sn içinde bir izleyicinin bunu fark edip etmediğini bilemiyorum; bu yüzden puana yansıtmadım.
- **Kart payının artık sorun olmadığı yargısı.** Oran süre olarak %43–46'da duruyor. Tekrar duygusunun kırıldığını kare dizilerinden çıkarıyorum; tam hızda oynatıp göremedim. YouTube tutma eğrisinde 6:52–8:54 aralığı yayın sonrası analizde özellikle izlenmeli.
