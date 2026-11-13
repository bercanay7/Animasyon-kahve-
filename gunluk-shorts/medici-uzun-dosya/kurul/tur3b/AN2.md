# AN2: Animasyon ve kurgu (kurgu ritmi, mizansen, yönetmenlik) · Medici Parça 1 · TUR 3b (v3.1 gerileme kontrolü)

Üye: AN2. Tarih: 5 Kasım 2026. Değerlendirilen: `out_p1/medici_P1.mp4` v3.1 (601,54 sn, 14.437 kare).

**Sınır:** Videoyu oynatamadım, sesi dinleyemedim. Değerlendirmem şunlara dayanıyor:
- kare dizileri (videodan kendim çıkardım);
- tam çözünürlük kesitler;
- 38 sert kesmede ORB + RANSAC ölçümü ve kare kare fark ölçümü;
- bütün videoda kopya kare taraması;
- `qa_flow_v31.txt`, `hareket.json` (v3.1);
- `kurul/duzeltme_tur3/SCN-3.md` ve `ENG-E.md`, `tur3_duzeltme_listesi.md`.

## 1. Karar

**ONAY: 9,5 / 10** (tur 1: 7,0 → tur 2: 8,4 → tur 3: 9,2 → tur 3b: 9,5).

Tur 3'teki ana maddem Ö1 (üstten açık defter kalıbı 102 sn'de 4 kez) koyduğum ölçütlerin hepsiyle kapandı. Küçük maddelerden üçü kapandı, biri kısmen kapandı. Benim alanımda v3.1'in getirdiği bir gerileme bulmadım. Yalnız önceden gözümden kaçmış küçük bir levha çakışması yazdım (§3).

## 2. Tur 3 maddelerimin durumu

| madde | durum | kanıt |
|---|---|---|
| **Ö1** üstten açık defter 4 kez | **KAPANDI** | Ayrıntı aşağıda |
| **K1** #91 iki boş sayfa (534,5–539,4) | **KISMEN** (kabul) | Boş açılış giderildi: tüy kalem ilk karede yazıyor (534,55); Machiavelli satırı 535,2'de, Cavalcanti satırı 536,6'da başlıyor. Ama sayfalar sonuna dek ≈%75 boş kalıyor: üstte 3–4 küçük İtalyanca satır var. Ölçülen hareket 2,6–3,0 (v3: 2,5–2,9), boş kâğıt payı %42 (v3: %43). 4,9 sn'lik bir hazırlık kartı olarak kabul ediyorum; koşul değil. |
| **K2** 471,7 sn'de mitra kayboluyor | **KAPANDI** | #82'nin ilk karesinde (471,67) mitra Giovanni'nin elinde; 471,71 / 471,75 / 471,85'te de. Ara plandan (#81, 469,95–471,62) eylem eşleşmeli kesme temiz. |
| **K3** CAVALCANTİ levhası 559,7 sn'de ≈340 px sıçrıyor | **KAPANDI** | 559,55 / 559,65 (#94) ve 559,75 / 559,95 (#95) karelerinde levha aynı yerde (≈x 240–1000, y 170–310). ≈560,3–561,0 arasında sönüyor. ORB'da bu kesme 672 inlier ve ×1,00 veriyor; eşleşmenin kaynağı sabit kalan levha, görüntüler farklı (hücre → sayfa). |
| Motor önerim: qa'da "sayfa" ailesi, 100 sn'de ≤2 kuralı | **AÇIK** (isteğe bağlı) | Uygulanmadı. Türler artık ayrı (`c2_masa` yalnız #72 ve #85; #83 `c2_yakin`, #88 `c2_defterler`). P2–P7 için hâlâ önerilir; P1 için koşul değil. |
| Önceki turlardan: cümle kilidi, c1→c2 bölüm kartı, #15 yön uyarısı | **değişmedi**, kabul | Çizelge ve çekim sınırları aynı. |

### Ö1 ayrıntısı (koyduğum ölçütlere göre)

| ölçüt (tur 3 raporumdan) | v3.1 |
|---|---|
| en çok iki üstten tam açılım | **#72** (416,0–431,6) ve **#85** (493,6–502,8). 416–518 sn arasında üstten defter süresi 42,0 sn'den (4 çekim) 24,8 sn'ye (2 çekim) indi; ikisi arasında 62 sn var. |
| biri tek öğeye ≥2× yakın plan | **#83** (475,8–486,4): kızıl kadife kasa kapağı, el ve anahtarlar, iğneli kâğıt şerit. Boş kâğıt payı %49 → **%15**. Şeritte "1422" → 22 düz çentik → 18 kesikli çentik → "MEDİCİ'DE KALDI" kendi sözcüklerinde yazılıyor; çekim içi hareket 3,1–34,6. |
| biri eğik açı / 150.000+ vuruşu defter dışına | **#88** (511,7–518,3): üç çeyrek eğik açıdan kapalı ciltli defterler, sandık ve florin istifleri. Boş kâğıt payı %18 → **%4**. Sayaç ve "DEFTERLER GÖSTERİR" aynı. #87'den sert kesmeyle (geniş oda → nesne ayrıntısı) giriliyor. |
| boş sayfa açılışları kalksın | #72 "ÇİFTE KAYDIN İZİ", "MEDİCİ'NİN FARKI" ve elle çekilmiş eksenle açılıyor (416,1). #85 "CATASTO · 1427" ile açılıyor (493,7). #83 şerit başlığıyla, #88 defterlerle açılıyor. |
| 9.780 hane seçilebilir hücrelerle | Tam çözünürlükte (497,2 sn; ≈x 580–1350, y 20–480) beşli çetele grupları tek tek seçiliyor. İlk satır yaldızlı, altında kızıl çizgi var. Telefon boyunda doku gibi okunur; bu kabul. |

**Genel tablo:**
- Kalan iki üstten defterin boş kâğıt payı (#72 %45, #85 %38) haritalar ve kartlarla aynı düzeyde (%37–46). Bu bölüm adının ("Defterin Sihri") bilinçli motifi olarak kabul.
- Sıkı sayımla (üstten defterler kart sayılınca) dünya+figür payı tüm videoda %57, eski vadi aralığında (403,6–589,5) %57 (v3: %54 / %47). qa aile etiketleriyle süre üzerinden %61 / %70; qa kapısının kendi satırı %63.
- Ritim artık "defter → oda zinciri → yakın plan → oda → defter → oda → eğik ayrıntı". Aynı kalıp art arda gelmiyor.

## 3. v3.1 gerilemeleri ve yeni gözlem

**Ölçtüklerim (gerileme yok):**

- **Sert kesmeler (38).** ORB + RANSAC ile kesmenin iki yanını karşılaştırdım; maske uyguladım. Aynı görüntü adayı:
  - #8 ×1,64 ve #46 ×1,63: bilinçli yakınlaşma.
  - #44, #80, #95 ×1,00: kesme boyunca ekranda kalan levha/fişten geliyor ("YAZILDIĞINA GÖRE", fişli "BELGE · DE ROOVER", CAVALCANTİ); görüntüler farklı.
  - Sıçrayan kesme: 0. `qa_flow` ile aynı sonuç.
- **Kesme girişi ve çıkışında duruş.** 38 kesmenin hiçbirinde yok. Kesmeden sonraki ilk kare farkı en az 0,35. Sorulan kesmelerde: 43,9 (#8) 0,36 ve 575,5 (#98) 1,82.
- **Kopya kare.** Bütün videoyu 320×180'de taradım. Yalnız 25,42–25,46 sn'de iki kare var: mum geçişinin tasarlanmış ≈0,2 sn'lik karanlığı. Takılma yok.
- **#63 → #64 bağlantısı (367,9–369,3).** Harita kesmeye dek itiyor (son örnekler 3,8–5,2; v3'te harita donuyordu). #64'ün ilk karesinde (368,85) BORÇ var. FAİZ 370,4'te, KUR FARKI ✓ 372,0'da geliyor. SCN-3'ün kendi düzelttiği "FAİZ/KUR FARKI görünmüyor" gerilemesi tam renderda yok.
- **Yakın plan ellerde eylem zinciri okunuyor.**
  - #62: kese sürülür (355,85–357,5), poliçe gelir (358,5), kese alınıp kadrajdan çıkar (359,5–360,3).
  - #81: papalık eli girer ve işaret eder (470,6–471,3).
  - #98: el yazar ve çekilir (576,2–577,0), mühür düşer (577,8), iris ile Cosimo madalyasına geçer.
- **#95 levhaları.** "CAVALCANTİ'YE GÖRE" ve "TÜRKÇESİ ÖZET · ÇEVİRİ BİZE AİT" y≈850'de; sayfanın son satırının ("kederlenmemeli.", y≈740) altında ve altyazı bandının (938–1042) üstünde. Çakışma yok (563,5 / 565,4).
- **Hareket eğrisi.** ≤3 örnek payı %11 (v3: %12). Bitiş ekranı dışında en uzun ≤3 koşusu 4,0 sn (548–552, ölüm döşeği konuşması; v3'te de vardı). #72'nin sonunda (428–430,5) ağ çizilirken 2,5 sn sakin bir kuyruk oluşuyor. Önemsiz.

**K-yeni: KÜÇÜK · önceden kaçırdığım levha çakışması (v3.1 gerilemesi değil).**
- **Ne:** #48 `c1_lonca`'da "KISA ÖMÜRLÜ LONCA KALDIRILDI" (≈275,0) ve "YÖNETİMDEN DE DIŞLANDILAR" (≈275,3–277,6) levhaları (≈x 475–1445, y 160–240) ilk sıradaki lonca kalkanlarının üst ≈45 px'ini örtüyor (kalkan tepeleri y≈195).
- **Neden gerileme değil:** ENG-E bu çekimde yalnız içeriği 100 px sola kaydırdı, zum aynı. Dikey düzen v3'te de böyleydi.
- **Neden önemli sayılabilir:** tur 2'de "özensiz otomatik yerleşim gibi okunur" dediğim sınıftan. Kalkanlar zemin öğesi olarak kayıtlı olmadığı için `qa_yerlesim` görmüyor.
- **Yapılacak:** levhaları ≥60 px yukarı al, alt kenar ≤180 olsun. Levha x 1445'e dek uzandığı için HUD'la (x≥1548) çakışmaz. Ya da kalkan ızgarasını ≥60 px aşağı indir. Sahibi `c1_kinds.k_lonca`; TE2 ile çapraz bakılmalı.

## 4. En emin olmadığım nokta

**Yakın planlar bir zayıflığı daha görünür kılıyor.** Tur 2'de istediğim ≥2× el/nesne ara planları, motorun en zayıf çizim öğesini, yani "eldiven" eli (SA1 E-1, P2'ye ertelendi), ekranda daha uzun tutuyor:
- #62 boyunca;
- #83 başı (≈476,4–478);
- #98 başı.

Toplam ≈9–10 sn. Kurgu açısından bu ara planlar işini görüyor: eylem okunuyor ve kesmeler hareket üstünde. Ama oynatmada bu ellerin "ucuz" okunup okunmayacağını göremiyorum. P2'de el yenilenmezse ara planları nesneye (kese, anahtar, mühür) daha sıkı kadrajlamak gerekir.

**#88'in perspektifi.** Kapalı defterlerin iğne deliği perspektifi videonun öteki düz/cephe dilinden ayrışıyor. Kurgu açısından çeşitlilik olarak iyi; üslup uyumu SA1'in kararı.

**Kanıtlar** (`/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/an2v31/`, JPEG, her biri ≤300 KB):

| dosya | içerik |
|---|---|
| `defter72.jpg`, `kasa83.jpg`, `catasto85.jpg`, `defterler88.jpg` | Ö1: dört çekimin zaman şeritleri |
| `cetele_4972.jpg` | çetele, tam çözünürlük kesit |
| `kalemler91.jpg` | K1 |
| `mitra81_82.jpg` | K2 |
| `cav95.jpg` | K3 ve #95 levhaları |
| `bag63_64.jpg`, `nolist64.jpg` | #63 → #64 bağlantısı |
| `kesmeler31.jpg` | #80, #83 ve #88 kesmeleri, #83 çıkışı |
| `kese62.jpg`, `kalem98.jpg` | yakın plan eller |
| `lonca48.jpg`, `lonca_ust.jpg` | K-yeni |
