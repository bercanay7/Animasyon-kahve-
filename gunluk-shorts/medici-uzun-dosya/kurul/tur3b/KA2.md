# KA2 · TUR 3b — Medici Parça 1, v3.1 gerileme kontrolü (`out_p1/medici_P1.mp4`, 601,54 sn)
Mercek: kaynak denetçisi, yöntem dürüstlüğü, hassasiyet ve hukuk (veto).

## 1. Karar

**ONAY — 9,4/10. Veto yok.**

Tur 3'teki dört maddemin dördü de (N1–N4) v3.1'de kapandı. Y9 kayıt temizliği de kapandı. Alanımda gerileme bulmadım. Tur 3'te verdiğim sözü tutuyorum: N1 ve N2 kapandığı için puan 9,4.

Kalan 0,6 puanın iki nedeni var:
- **Y8:** kulak kontrolü hâlâ kullanıcıda. Belgeye dayanan c2s20'de "aforozla" sözcüğünü üç bağımsız ASR "Aforoz'da" diye duydu.
- **Ö6:** Studio'daki "yapay içerik" sorusunda muhalefet şerhim kayıtlı duruyor.

## 2. Neye dayandım (sınırlarım)

- **Videoyu oynatamadım, sesi dinleyemedim.**
- **v3.1'den kendim çıkardığım ≈50 kare.** Zamanlar `timeline.json`'dan seçildi (dosya değişmemiş).
- **Kod:** `scenes_c0–c2.py`'de `threat` ve `dagger` sayısı 0.
- **Belgeler:** `KURUL.md` (tur 3 ve v3.1 planı), `tur3_duzeltme_listesi.md`, `duzeltme_tur3/SCN-3.md` ve `ENG-E.md`, `qa_flow_v31.txt` (20 GEÇTİ, 0 KALDI; yerleşim ve dönem İHLAL 0), `uretim_v31.log` (601,54 sn, seviye 4.1), `yayin/studio_paketi_P1/00–05`, `notlar_c2.md`.
- **Tutulan kanıtlar** (JPEG, her biri ≤1 MB), `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/ka2t3b/`:
  - `s01_konstanz.jpg`, `c04_konstanz_444_4.jpg`;
  - `s02_cavalcanti.jpg`, `c01_machiavelli_it.jpg`;
  - `s03_defter.jpg`, `s04_kalem_kasa.jpg`;
  - `s07_belge.jpg`, `c03_asemik_46.jpg`;
  - `s08_misc.jpg`.

## 3. Tur 3 maddelerimin durumu

| Madde | Durum | Kanıt (v3.1) |
|---|---|---|
| **N1** Konstanz'da kol ensede | **KAPANDI** | 443,4–444,8 sn: kardinal sağda ve ayrık duruyor, kolu tahta ve tiaraya doğru boşlukta. 444,4 sn tam çözünürlükte el ≈(1525, 530), öndeki siyah cüppeli din adamının başı ≈(1360, 570): ≈160 px boşluk, temas yok (`c04_konstanz_444_4.jpg`) |
| **N2** Özetin çeviri gibi görünmesi | **KAPANDI** (ekran + açıklama) | Bkz. aşağıdaki not |
| **N3** "DEFTERLER GÖSTERİR" | **KAPANDI** | ≈514,5 sn'de ("defterler" 514,45) beliriyor, 517,0 sn'de hâlâ okunur: ≈3 sn. Mum örtmüyor (`s03_defter.jpg`) |
| **N4** "O KALEM" HUD | **KAPANDI** | 577,5 sn: HUD gizli; 1520 mührü nesne yılıyla çizilmiş (`s04_kalem_kasa.jpg`) |
| **N5** Bitiş ekranı vaadi | Kabul (değişmedi) | Paket artık P2 tarihini sabit yoruma yazmayı ve P2 günü sol öğeyi değiştirmeyi söylüyor (`00_yayin_adimlari.txt` 46–48) |
| **Y9** `notlar_c2.md` eski tablo | **KAPANDI** | Satır 34, 40 ve 52 güncel: TİM PARKS; 1407 yok; "150.000+" ● de Roover |
| **Y8** Kulak kontrolü | **AÇIK**, kullanıcıda | Ses değişmedi; `00_yayin_adimlari.txt` adım 0'da yazılı |
| **Ö6** Studio | Şerhim kayıtlı, engellemiyorum | `00_yayin_adimlari.txt` 29 |

**N2 notu:**
- **Cavalcanti sayfası (561,5–565,3 sn):** sayfanın altında "TÜRKÇESİ ÖZET · ÇEVİRİ BİZE AİT" ve "CAVALCANTİ'YE GÖRE" levhaları var (y≈850). Sayfa metniyle çakışmıyor.
- **İki sayfa yan yana (567,5 sn):** altta "TÜRKÇE SATIRLAR ÖZET · ÇEVİRİ BİZE AİT".
- **Açıklama** (`02_aciklama.txt` 8): "…Machiavelli ile Cavalcanti'den aktarılan sözlerin Türkçeleri bize aittir; … özetle aktarılmıştır, ekrandaki İtalyanca satırlar özgün metinlerden kısa alıntılardır". Önerdiğim cümle birebir girmiş.
- **Machiavelli İtalyancası** tam çözünürlükte (`c01_machiavelli_it.jpg`): "…Muoio contento…" / "…non vi recherà mai né invidia né pericolo," / "perché quello che l'uomo si toglie," / "non quello che all'uomo è dato…". Teyit metniyle (MAC IV, `teyit_P1.md:92`) sözcük ve noktalama olarak birebir. "invidia" artık özgünde de görünüyor, bu yüzden Türkçe özetteki "kıskançlık" kaynakta karşılık buluyor. Kalan "si toglie ≠ istediği" nüansını "ÖZET" etiketi dürüstçe karşılıyor.

## 4. v3.1 gerilemeleri ve yeni öğeler (hassasiyet gözüyle)

**Gerileme bulmadım.** Yeni ve değişen öğelerin hepsi temiz:

- **#83 papalık kasası yakın planı** (476,5–485,9 sn; `s04_kalem_kasa.jpg`):
  - Kızıl kadife kasa, iki anahtar, kapağa iğneli kâğıt şerit.
  - Şeritte "PAPALIĞIN RESMÎ KASA MEMURLUĞU · 1422 · 22 YIL KESİNTİSİZ (22 çentik) · + 18 YIL ARALIKLI (18 kesik çentik) · MEDİCİ'DE KALDI". DBI ile birebir ("22 anni consecutivi e per altri 18 a intermittenza").
  - Çapraz anahtarlar papalığın ve papalık maliyesinin (Camera Apostolica) yaygın simgesi. Örneğin taht boşken basılan sikkelerde ve Camerlengo armasında yer alır (genel bilgi, güven orta-yüksek). Saygılı kullanılmış, alay yok.
  - Anahtarları bırakan elin yeni koyu kızıl; yüz ve ad yok. Görevin 1422'de Medici'nin Roma müdürü Bartolomeo Bardi'ye verildiğini (DBI) çiğneyen bir iddia taşımıyor. Kabul.
- **#88 kapalı defterler ve sandık** (512,5–517,0 sn): "1397", "1397 – 1420", "1420" sırt etiketleri; "150.000+ FLORİN KÂR" ve "DEFTERLER GÖSTERİR" nitelemesi korunmuş.
- **#85 catasto defteri** (494–502 sn):
  - "BİR HESABA GÖRE · 9.780 HANE · KAYITLI SERVET · %29,8 · 137 HANE";
  - "PALLA STROZZİ · 1427'NİN EN ZENGİNİ · 163.000 FLORİN · YAKLAŞIK".
  - Nitelemeler yeni mürekkep diline taşınırken kaybolmamış.
- **Çifte kayıt** (414,0 sn): "DEBITORI / BORÇLULAR · CREDITORI / ALACAKLILAR". Çeviri doğru. Satırlar okunmaz el yazısı izi; tutar ya da ad uydurulmamış.
- **1737 belgesi** (36,5–55,8 sn; `s07_belge.jpg`, `c03_asemik_46.jpg`):
  - Asemik el yazısı. Tam çözünürlükte okunabilen bir sözcük yok (Fransızca, İtalyanca ya da Türkçe); yalnız "on" ya da "an" gibi iki harflik parçalar var. Uygunsuz bir parça görmedim.
  - Yöntem açısından doğru karar: Fransızca özgünü görmediğimiz için metin uydurulmuyor, belge "var ama okunmuyor" diye çiziliyor.
  - "13 MADDE" ve "FRANSIZCA" Casciu 2006'ya (●) dayanıyor.
- **Kırmızı taşıma geçişi** (271,0–271,2 sn; `s08_misc.jpg`): "isyanı ezdi"nin ardından gelen kızıl şerit koyu mürekkep fırçasına çevrilmiş. Kan çağrışımı kalkmış.
- **Mitra simgesi** (466,4–473,4 sn): rüne benzeyen işaret gitmiş, yerine Latin haçı ve inci dizisi gelmiş; dinî simge doğru ve saygılı. Papa sakalsız. Hançer yok. "AFOROZ TEHDİDİ"nde papalık belgesi (bulla) var.
- **Yankı kapağı** (1,6 sn): "SON MEDİCİ / MİRASI KİLİTLEDİ"; asemik belge, beyaz parıltı yok.
- **Bitiş ekranı** (597,0 sn): "2/7 · COSİMO: SÜRGÜN VE DÖNÜŞ".

**Küçük (isteğe bağlı, paket metni):** `00_yayin_adimlari.txt` 62'de başlık testi T3 hâlâ "(yalnız kaynak üyesi onayıyla)" diyor. KA1 ve KA2 tur 3'te onayladı (`KURUL.md` tur 3 tablosu). Satır "(kaynak üyeleri KA1 ve KA2 onayladı, tur 3)" diye güncellenebilir.

## 5. En emin olmadığım nokta

1. **Asemik yazının bütün karelerde temiz kalması.** Yazı yordamsal üretiliyor ve kamera belgede hareket ediyor. Ben 46,0 sn'yi tam çözünürlükte, 36,5, 40,6 ve 55,8 sn'yi ölçekli kontrol ettim. Başka bir karede rastlantısal bir Türkçe sözcük belirmesi olasılığını sıfırlayamam, ama düşük görüyorum.
2. **Y8.** Ses değişmedi. Sorun gerçekse kurulun göremeyeceği bir yerde. Kullanıcının kulak kontrolü yayın öncesi son koşul olarak kalmalı.
