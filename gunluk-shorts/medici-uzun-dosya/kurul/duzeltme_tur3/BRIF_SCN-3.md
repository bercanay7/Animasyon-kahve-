# BRİF — SCN-3 · v3.1 "defter ve c2" paketi (kurul tur 3 bulguları)

Sen Medici Parça 1'in v3.1 düzeltme ajanısın. P = `/home/user/Animasyon-kahve-/gunluk-shorts/medici-uzun-dosya`.

Kurul tur 3'te 10 üyeden 8'i ONAY verdi (≥9). Kalan bulgular engelleyici değil, ama puanları 9,0–9,2'den 9,5'e taşıyacak olanlar bunlar. Video v3: `P/out_p1/medici_P1.mp4`. Tur 3 raporları: `P/kurul/tur3/<KOD>.md`. Tur 2'de bu çekimleri kuran ajanın raporu: `P/kurul/duzeltme_tur2/SCN-2.md` ("DEFTER DÜNYADIR" kararı). Önce bunları oku: AN2.md (Ö1, K1), PK2.md (§3 N1), SA1.md (§4 Y6-k, N4), AN1.md (Y-N1, Y-N2, Y-N3, Y7), sonra SCN-2.md.

## Dosya sahipliği
- **Senin:** `c2_kinds.py`, `scenes_c2.py`.
- **Paralel çalışan ENG-E'nin:** `anim.py`, `cilt_cam.py`, `compose.py`, `c0_kinds.py`, `scenes_c0.py`, `scenes_c1.py`, `cilt_oda.py`, `kapak_medici.py`. Bunlara dokunma.
- `p1_ortak.py` ortak dosya; mecbur kalırsan yalnız yeni bir yardımcı ekle, var olanı değiştirme. Raporda belirt.
- Anlatım, ses, `timeline.json` ve altyazı DEĞİŞMEZ. Çapalar yalnız zaman çizelgesindeki sözcüklerden.

## İşler (öncelik sırasıyla)

### 1. Defter tekrarı — ANA MADDE (AN2 Ö1 + PK2 N1, iki üye ayrı ölçümle buldu)
Üstten açık defter kadrajı 102 saniyede dört kez dönüyor:
- #72 `c2_masa v="iz"` · 416,1–431,6
- #83 `c2_masa v="kasa"` · 475,8–486,4
- #85 `c2_masa v="catasto"` · 493,6–502,8
- #88 `p1_ledger` · 511,7–518,3

Hedef: üstten tam açılım **en çok iki** kalır: #72 ("Defterin Sihri"nin kendisi) ve #85 (catasto sayımı). Ritim "defter – yakın plan – defter – eğik/başka" olsun.

- **#83 → ≥2× yakın plan (ara plan).** Anlatım (c2s21, 476,0–485,8): "Papalığın resmî kasa memurluğu da 1422'den sonra yirmi iki yıl kesintisiz, ardından on sekiz yıl aralıklarla Medici'de kaldı."
  - Çekimin baş öğesi el ve anahtarlar olsun (papalık kasası, kızıl kadife).
  - "1422 · 22 YIL KESİNTİSİZ + 18 YIL ARALIKLI · MEDİCİ'DE KALDI" bilgisi defter sayfasında olmasın. Sandığın üstündeki ya da anahtar halkasına bağlı bir kâğıt şeritte (cartellino) dursun, ya da masaya serili dar bir şeritte. Mürekkep ve tüy kalem diliyle.
  - Mevcut sözcükler ve sayılar aynen kalır: "PAPALIĞIN RESMÎ KASA MEMURLUĞU", "1422", "22 YIL", "KESİNTİSİZ", "+ 18 YIL", "ARALIKLI", "MEDİCİ'DE KALDI".
  - Altın kapsül dolum çubuğu (SA1 Y6-k) kalkar. Yerine kalemle çekilmiş düz mürekkep çizgisi ya da 22 çentik, ardından 18 kesikli çentik.
- **#88 → üstten açık defter olmayan bir kadraj.** Anlatım (c2s25 ikinci yarı, 512,0–517,8): "1397'den o yıla kadar defterler yüz elli bini aşkın florin kâr gösterir."
  - Seçenekler:
    - (a) yandan ya da üç çeyrek eğik açıdan kapalı, ciltli defterler: sırtlarında yıllar 1397…1420, yanında sandık;
    - (b) PK2'nin önerisi, sandık ya da masada Giovanni.
  - #87 (1420: yönetim oğullarına, p1ofis) ile aynı oda olabilir, ama kadraj ondan belirgin farklı olmalı.
  - Korunacaklar:
    - sayaç `count_up` 150.000, `suffix="+"` yalnız son değerde (KA2-D10), "FLORİN KÂR";
    - "1397 – 1420";
    - "DEFTERLER GÖSTERİR" etiketi "defterler" sözcüğünde basar (KA2 tur 3 N3).
  - Yeni bir olgu iddiası ekleme: defter adı ("libro segreto" vb.), kişi adı ya da tutar yazma.
- **#72 ve #85:** sayfalar başlığı yazılı açılsın; kalem yalnız yeni veriyi yazsın (PK2 N1.4). Boş açılış olmasın.

### 2. Defter içi grafik dili: arayüz değil mürekkep (SA1 Y6-k; AN2 de "9.780 hane düz kahverengi blok" diyor)
- #85 "9.780 hane", 495,5 sn (≈x 630–1290, y 165–705). İnce yatay çizgilerden gri bir blok; barkod gibi okunuyor.
  - → Satır satır küçük el yazısı ya da beşli çetele.
  - İlk 137'si yaldızlı.
  - Doku elle yazılmış görünsün: satır sonları düzensiz, mürekkep yoğunluğu değişken.
- #85 "KAYITLI SERVET", ≈498 sn (x 540–1250, y 750–835). Dikdörtgen ilerleme çubuğu.
  - → Elle cetvellenmiş bir bantta %29,8'lik mürekkep taraması ya da çapraz tarama, kenarı hafif titrek.
  - "%29,8 · BİR HESABA GÖRE" ve "PALLA STROZZİ · 163.000" aynen kalır.
- #72 Cenova–Pacioli ekseni (416–424). Tik etiketli arayüz ekseni.
  - → Elle çekilmiş çizgi, yıllar el yazısıyla.
  - "CENOVA 1340 · PACİOLİ 1494 · ETMEDİLER" ve "MEDİCİ'NİN FARKI…" metinleri aynen kalır.

### 3. Hareket ve bağlantı (AN1 Y-N1, Y-N2, Y-N3, Y7; SA1 N4)
- **Y-N1:** #63 `p1_map` → #64 `c2_nolist`, 367,9–369,3. ≈1,4 sn ölü bağlantı:
  - harita, kadraj korumasına takılan "pull" yüzünden donuyor;
  - 368,88'de boş parşömen;
  - "BORÇ" ancak ≈369,3'te geliyor.
  - Ne yapılacak:
    - #63'te `cam=("pull",)` beyanı kalksın; rota merkezine yavaş itme (≥%1/sn) son kareye dek sürsün;
    - kazanç sikkelerinin salınımı kesmeye dek sürsün;
    - #64'te ilk kart (BORÇ) ilk karede hazır olsun ya da `lead` ile doğsun.
- **Y-N2 ve SA1 N4:** yakın plan eller.
  - #62 kese (355,8–361,1, `c2_yakin scene="kese"`):
    - el 61 px/kare tepeden sonra sabit 27 px/kare gidiyor ve ≈357,7'de iki karede duruyor; oturma yok. → Çan eğrisi + `anim.settle` (%6–10 aşma); yolda 5–10° bilek dönüşü.
    - SA1 N4: tüccarın kolu 358,4–358,7'de yerinde soluklaşıyor (yarı saydam "hayalet" kol, ≈x 1000–1920, y 450–700). → Soldurma yerine geri çekilip kadrajdan çıksın.
  - #81 mitra (469,95–471,67):
    - işaret eden el oturmadan duruyor;
    - mitrayı tutan eller 1,7 sn hareketsiz (parçanın en düşük kare farkı).
    - → Oturma + hafif itme ya da odak kayması.
- **Y-N3:** 575,5 sn #98 `c2_yakin` (kendi kamerası), kesme girişinde 1 karelik duruş (0,11). → `c2_yakin`'in kendi kamerasında da sert kesmeyle birleşen uca `cilt_cam.CUT_SLOPE` uygulanmalı (motordaki `cilt_cam` mantığını oku; değiştirme, kendi kamera kodunda uygula). 355,8 (#62 yavaş kalkış, 0,21) de aynı işin parçası.
- **Y7:** #67 `c2_hediye` florin yağmuru (389,15–391,38). Hız p99 16–18 px/kare, en çok ≈21; sikkeler keskin. Bu türde hızı `anim.hint_speed(cx, v)` ile bildir (`anim.speed_of` yardımcı; eşik `compose.SHUTTER_V_HINT` = 8). c2'de hızlı küçük nesne çizen başka tür varsa onlara da ekle.

### 4. Küçükler
- **PK2 Y7:** çifte kayıt vuruşu, 412,9–415,1 (`scenes_c2.py` ≈138–144):
  - "DEBITORI / CREDITORI" altına küçük Türkçe karşılık: "BORÇLULAR / ALACAKLILAR";
  - "MİT" damgası "CREDITORI" başlığını (≈x 1460–1760, y 265–305) ≈0,8 sn örtmesin.
- **AN2:** 559,7'deki kesmede CAVALCANTİ levhası ≈340 px sıçrıyor (#94 → #95 `c2_kalemler`). Levha konumu kesmenin iki yanında tutarlı olsun, ya da değişim bilinçli bir hareketle olsun.
- **AN2:** 471,7'de mitra ≈0,3 sn kayboluyordu (#81 → #82). v3.1'de mitra artık Giovanni'nin elinde bir nesne (`prop="mitra"`, `cilt_anim.attach_prop`). Kesmenin iki yanını kare kare doğrula; boşluk kaldıysa gider.

## Kurallar ve kapılar
- **Yerleşim ve dönem:**
  - `qa_yerlesim` levha, zemin ve yazı çakışmasını İHLAL sayar.
  - HUD kuralları: nesne yılı ≠ olay yılıysa HUD gizlenir ya da `donem.nesne_yili`.
  - 1500 öncesinde geniş kenarlı şapka yok; 1511 öncesinde papa sakalsız.
- **Damgalar:** `_paper_stamp` / `anim.stamp_ovl` kâğıt fişli, tek dilde.
- **Görsel dil:** guaj kâğıt-kukla cildi; mevcut yardımcıları kullan (`_write`, `_hand` (fell_i), `CM.ink`, `OD.quill`, `P.tag`, `P.count_up`, `_paper_stamp`).
- **Kare kontrolü:** `python3 /tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/v3/kare.py <ad> t1 t2 … --w 640 --cols 4`
  - Program karesi üretir, kontak sayfasını `…/scratchpad/v3/<ad>.png` olarak yazar.
  - 6 kare ≈5 sn, ≈0,6 GB RAM.
  - Hareket için 1/24 sn aralıklı ardışık kareler al.
- **Son kapı:** `cd P && python3 qa_flow.py --part 1 > /tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/scn3_qa.txt 2>&1`
  - 19 kapının hepsi GEÇTİ olmalı.
  - ≈6 dk, 2 süreç; en çok iki kez koş.
  - Kendi ağır işinle aynı anda koşma.
- **Yasaklar:** render.py yok, git commit/push yok (başkan yapar), `pkill -f` yok (PID ile dur).
- **Disk sınırlı (≈2,9 GB boş):** kare dökümlerini sil; kanıt olarak JPEG kontak sayfaları (her biri ≤1 MB) `P/out_p1/duzeltme/tur3/SCN-3/` altına.

## Teslim
- Rapor `P/kurul/duzeltme_tur3/SCN-3.md` olacak. Her madde için:
  - ne yaptığın;
  - dosya:satır;
  - önce ve sonra kanıtı (kare ya da ölçüm);
  - açık kalan ne varsa.
- Son mesajında kısa özet ve qa_flow sonucunun son satırları olsun.
