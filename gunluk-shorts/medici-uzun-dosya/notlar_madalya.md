# Madalya portre üreteci v3 (MDL, 4 Kasım 2026)

Kurul tur 1: SA1-Ö6 ("Lorenzo kadın başı gibi, Giovanni'nin kafası kutu"), SA1-E4 (dikdörtgen artefakt — ENG-A kapatmıştı, v3'te yok),
PK2 ("Lorenzo'nun saçı peruk/kask; Giovanni ve Cossa aynı kalıp"), AN2 (madalya MALZEMESİ korunacak), KA1-V9 (portre madalyası 1438'den önce yok).
Dosyalar: `cilt_medal.py` (üreteç + API), `donem.py` (`portrait_medal_is_anachronistic`), `c6_kinds.py` 116–118 (kalibrasyon). Kanıt: `out_p1/duzeltme/MDL/`.

## 1. Kök neden (neden "kutu kafa / kadın başı")
* v1/v2 kafatası kulağın arkasında ~130 px KISA: derinlik/yükseklik ≈ 0,56 (gerçek ≈ 0,86). Küçük kafatası + iri yüz = "kutu", saçla birleşince "kadın başı".
* Yüz modelajı yok; çizgi kazıma (göz, kaş, dudak) + düz yükseklik platosu → şematik çizgi çizimi.
* Saç tek kütle + paralel oluk → "kask/peruk"; saçın kesimi her yerde aynı → "küt bob".

## 2. v3 tekniği
* **Yükseklik alanı (px):** alan 0, kenar ≈30, baş ≈50–60, başlık ≈60–75. Katmanlar alttan üste: büst → boyun → baş → kulak → giysi → saç → sakal → başlık.
  Her katman `over()` ile alttakinin üstünden **yuvarlak duvarla** yükselir (kontur çizgisi değil, kabartma kenarı). Kalın örtüler (kukuleta, camauro,
  cuffia, berretta, sarık) alttaki biçimi yalnız yumuşatılmış izler (`smooth_under`: kulak kumaştan sızmaz).
* **Anatomi** (`head_geom`, `sculpt_face`): gerçek kafa oranı; profil hattı ~30 nirengi (alın, glabella, nasion, burun sırtı [kambur/basık], uç, kolumella,
  dudaklar, sulkus, çene); alın tümseği, kaş kemeri, şakak çukuru, göz çukuru + göz küresi + üst/alt kapak + kapak kıvrımı, elmacık, yanak çukuru/dolgunluğu,
  gıdı, burun kanadı + oluğu + delik, nazolabial oluk, dudak kütleleri + ağız köşesi, çene ucu, çene kemiği sırtı; çene ALT kenarı keskin, ramus/ense yumuşak;
  kulak (helix, scapha, Y antihelix, concha, tragus, lob); boyun (göğüs-köprücük-meme kası, gırtlak, yaşlı boyun); yaş: kırışık, göz altı, kaz ayağı.
* **Saç:** tepe girdabından yayılan tutam aileleri (iki kılavuz eğri arasında ara değerleme), S dalgası, **alttan oyulmuş örtüşen tutamlar**
  (arkadan öne çizilir; tutam sınırı kademe olarak okunur), içinde ince tel olukları. Kısa saç: girdaptan dışa/aşağı virgül tutamlar.
* **Kumaş:** yumuşak kütle (`pillow`) + geniş kıvrım sırtları + dar vadiler; mazzocchio = boru kesitli, yuvarlak uçlu dolgulu halka, burgulu dikiş + kabarık
  dilimler; foggia = rulodan kalkıp arkaya devrilen lob; becchetto = sarkan kalın şerit; ermin = kürk tutamlı şerit.
* **Malzeme** (`shade`): normal → üst-sol ışık (x −0,50, y −0,62, z 0,60) + zayıf dolgu + iki yansıma lobu; çok ölçekli ortam kapanması; yükseklik alanı
  gölgesi (kabartmanın alana düşen gölgesi); patina = genel koyu kahve + çukurda koyu/yeşilimsi, yüksek ve dışbükey yerde el değmiş parlak bronz, benekli;
  alan hafif içbükey, ince döküm tanesi + gözenek; kenar halkası (düz tepe, dış pah, hafif düzensiz), ince iç fileto, **kabartma harfli yazıt**
  (eski: boncuklu halka + plak çizgileri — "vinil plak" görünümü kaldırıldı).

## 3. Kişiler (benzerlik iddiası YOK: tarihsel portrelerin genel karakteri)
| anahtar | karakter | başlık / saç / giysi | dayanak (genel tip) |
|---|---|---|---|
| `m_giovanni` | yaşlı, ince uzun yüz, çökük yanak, sıkı ince dudak | uzun cappuccio: kalın mazzocchio (öne-arkaya taşar) + yüksek foggia + becchetto; rulonun altında kısa kır saç | Masaccio/Uccello freskolarındaki Floransa cappuccio'su; Bronzino'nun ölüm sonrası portresi |
| `m_cosimo` | kartal burun, ince dudak, belirgin elmacık; kanonik ≈75 yaş | alçak cappuccio: kulağı saran kumaş başlık (cuffia) + kısa halka + becchetto; kürk yaka | Pontormo'nun ölüm sonrası portresi; Niccolò Fiorentino çevresi madalyası |
| `m_cosimo_genc` / `age=40` | aynı yüz, 1429'da 40 yaş: düz cilt, dolgun yanak, kırışık yok | aynı | — |
| `m_lorenzo` | büyük ama basık (eyer sırtlı, geniş uçlu) burun, öne çıkık alt çene + alt dudak, ağır kaş, kalın güçlü boyun, gırtlak | omuza dökülen düz saç (zazzera) + kâkül; ön tutamlar çene köşesinin ARKASINDAN iner (çene/boyun görünür), eğik kesim | Verrocchio büstü, Ghirlandaio Sassetti freskosu |
| `m_cossa` / `m_cossa_tiara` | tıraşlı, dolgun yuvarlak yüz, gıdı, ağır göz kapağı | papalık camauro'su + kalın ermin kenar / üç taçlı tiara (+ infulae); cüppe (piviale) + işlemeli şerit + mors | Vaftizhane mezarı (Donatello–Michelozzo); yazıt oradan: "IOANNES QVONDAM PAPA XXIII" |
| `c6_piero` (= `m_piero`) | dolgun etli yüz, gıdı, kalın boyun | kısa kıvırcık saç; brokar (nar motifi) | Mino da Fiesole büstü |
| `m_savonarola` | iri çengel burun, dolgun dudak, çökük yanak, derin göz, ağır kaş | sivri tepeli Dominiken kukuletası (alnı kaşa dek örter) + pelerin | Fra Bartolomeo'nun profil portresi |

168 px ayırt edilebilirlik (siluet dahil): `out_p1/duzeltme/MDL/MDL_168_ayirt.png`.
Diğer ERKEK anahtarlar (c6_giuliano, c6_poliziano, c7_*, m_portinari, m_sarl, m_mehmed, m_cosimo1…) `medal.PEOPLE` parametrelerinden genel v3 yüze
çevrilir (`params_for`; saç/başlık/giysi eşlemeleri `HAIR_MAP`/`HAT_MAP`/`GARMENT_MAP`; tanınmayan başlık/sakal eski çizimden MASKE olarak alınır).
Kadın/örtülü profiller eski portre çizimiyle (medal_extra'nın `_x` hattı dahil) ama **v3 gövde + malzemeyle** çizilir — v2 yolu `_x` başlığını
çizemiyordu (ör. `c6_simonetta` kel erkek başı gibi çıkıyordu; düzeldi).

## 4. API (eski imzalar aynen)
* `medal_img(key, metal, inscription, flip, size, age=None)` · `medal_array_b(…, age=None)` · `medal_shadow(…, age=None)`
* `draw_medal_b(f, key, x, y, size, metal, flip, alpha, tilt, glint, inscription, shadow, age=None, stamp=None)`
  * `age`: yaş (yıl). None → `resolve_age`: sabit yaşlı anahtar (`m_cosimo_genc`=40) ya da **AUTO_AGE**: çekim yılı − doğum (ölümden sonra ölüm yaşı;
    5 yıla yuvarlı; yalnız PROFILES'ta `born`+`young` olan kişiler). Yıl yoksa kanonik yaş. P1 1429: Cosimo → 40 yaş otomatik.
    `cilt_kinds2.k_medal` `age=` geçiremiyor (`**_`) → sahnede genç Cosimo için `key="m_cosimo_genc"` ya da AUTO_AGE.
  * `stamp`: None → `donem.portrait_medal_is_anachronistic()` True ise (yıl < 1438) otomatik "TEMSİLÎ"; False → yok; True/metin → zorla.
* `feature_point(key, which, flip=False, age=None)` → yüz öğesinin madalya merkezine göre konumu (çap biriminde): nose | chin | eye | mouth | ear.
* Bayraklar: `V3` (False → eski v2/v1), `AUTO_AGE`, `STAMP_AUTO`, `STAMP_ANGLE` (58°), `MEDAL_VER = 3` (lru anahtarında; disk önbelleği yok).
* Yeni anahtarlar: `m_cossa`, `m_cossa_tiara`, `m_savonarola`, `m_piero`, `m_cosimo_genc` (v1 uyumlu PEOPLE kayıtlarıyla). Takma ad: `c7_pazzi_lor` → Lorenzo.
* Maliyet: madalya başına ≈1–2,5 sn (süreç başına bir kez; lru önbellek), 720² RGBA.

## 5. TEMSİLÎ kuralı (KA1-V9)
* `donem.portrait_medal_is_anachronistic(y)`: y < 1438 → True; ≥1438 → False; yıl yok → None (kapak/reel/önizleme: damga yok). `PORTRAIT_MEDAL_FIRST = 1438`
  (Pisanello, VIII. Ioannes Palaiologos madalyası).
* Çizim: madalyanın alt kenarında, diskin DIŞINDA (kenar yazıtıyla çakışmaz), ekran merkezine bakan yana 32° kaydırılmış küçük levha: koyu zemin, ince yaldız
  çerçeve, beyaz Cinzel, yazı = clamp(0,066 × çap, 30, 46) px. Ekran uzayında güvenli alana / altyazı bandının (930) üstüne / HUD dışına kıstırılır.
  Neden merkeze kayık: gece çekimlerinde `relight` mum havuzu ekran ortasında; tam alttaki damga 2,8–3,5:1'e düşüyordu → 58°'de ≈4,5:1 (gündüz ≈9:1).
* Denetim kaydı: `note("medal", …, stamp=True/False)` + `note("medal_stamp", key, text)`.
* P1: c2s27 Lorenzo (1429) ve c2s34 Cosimo (1429) → damga otomatik; c0 "gerekçe" madalyonları simge (taç/terazi), portre değil → etkilenmez.

## 6. c6 kalibrasyonu
`c6_tarif` ölçü işaretleri (`c6_kinds.py` 116–118) v3 yüzüne göre: burun (149, 1), çene (129, 96), göz (89, −62) × ms/640
(= `CMD.feature_point("m_lorenzo", …)` × 640). P3 karesiyle doğrulandı (kırmızı noktalar burun ucu ve çene önünde).

## 7. Doğrulama
* Kişi sayfaları (ÖNCE v2 / SONRA v3; 720 · 360 · 168): `out_p1/duzeltme/MDL/MDL_{giovanni,cosimo,lorenzo,cossa,piero,savonarola}.png`
* P1 önce/sonra kareleri: `P1_c2s27_lorenzo_529sn_once_sonra.png`, `P1_c2s34_cosimo_581sn_once_sonra.png`; `P1_c0_gerekce_75sn_sonra.png`
* `qa_flow.py --part 1 --fast`: 12 GEÇTİ · 0 KALDI · 1 UYARI (eski yön uyarısı). P3 duman testi: `Program(part=3)` kurulur; c6_valori, c6_tarif, c6_aile,
  c6_lucrezia, c6_madalyalar, c6_iki_madalya, c7_med kareleri çizildi.

## 8. Açık kalanlar
* Lorenzo'nun saç biçimi (zazzera) doğası gereği "sayfa oğlan" kesimidir; erkeklik yüz/çene/boyundan okunur — kurul tur 2'de yeniden bakılmalı.
* Cosimo genç/yaşlı farkı ince (yaşlı: kırışık, göz altı, sarkık boyun) — daha belirgin istenirse `PROFILES["m_cosimo"]["young"]`.
* Genel anahtarlarda berretta/sarık/miğfer orta kalite (P4–P7'de yakın plan gerekirse kişiye özgü profil eklenmeli: `PROFILES`).
* Kadın profilleri yalnız malzemede birleşti; çizimleri hâlâ v1 (çizgi kazıma).
* `qa_donem.py` bağımsız kural kopyası TEMSİLÎ damgasını henüz denetlemiyor (kayıt hazır: `medal` öğesinde `stamp`).
* Savonarola yazıtı (dönem madalyalarındaki kısaltmanın yaklaşığı) P7'de kullanılmadan önce KA teyidi.
