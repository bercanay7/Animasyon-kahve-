# ENG-C — Figür ve hareket motoru düzeltmeleri · Medici P1 · kurul tur 2

**Ajan:** ENG-C (figür ve hareket motoru). **Tarih:** 5 Kasım 2026.
**Proje:** `gunluk-shorts/medici-uzun-dosya` (aşağıda P).
**Kanıt klasörü:** `P/out_p1/duzeltme/tur2/ENG-C/` (git'e girmez).
**Sınırlar:**
- Render yapmadım, git kullanmadım; kareleri `kare.py` ile ürettim (tam motor, deklanşör açık).
- Videoyu oynatamadım, sesi dinleyemedim.

**Dokunduğum dosyalar:**
- `cilt_anim.py`, `anim.py`, `cilt_medal.py`;
- `cilt_oda.py`: yalnız `sil_actor`, `seated`, `draw_actor` ve `draw_actor`'ın kullandığı iki yeni yardımcı (`_room_peers`, `_auto_look`, aynı bölümde). `_blit_cf` değişmedi.

Sahne dosyalarına dokunmadım.

## 0. Özet

| # | Kurul maddesi | Durum | Değişen yer (dosya:işlev) | Kanıt |
|---|---|---|---|---|
| 1 | **SA2-Y1:** baş ve ayakkabı gövdeden önce, opak geliyor | **KAPANDI** | `cilt_anim`: `blit`, `fade_begin`/`fade_end`/`fig_rect`, `draw_fig`, `_draw_pose`, `actor`, `handshake`, `threat`, `draw_rider`, `_flag_fn`, `_rider_banner`<br>`cilt_oda`: `sil_actor`, `seated` | `g1_villani_once_sonra.jpg`, `g1_okul_once_sonra.jpg`, `g1_siluet_suzgec_once_sonra.jpg` |
| 2 | **AN1:** "kukla" oyunculuk (hazırlık, oturma, göz kırpma, takip, baş çevirme) | **KAPANDI** (kit düzeyinde) | `cilt_anim`: `gesture_env`, `gesture_on`, `blink_eye`, `_ft_arm`, `apply_look`, `act_point/bow/kneel/handshake/admonish/threat/talk`, `gait`, `actor(look=)`<br>`cilt_oda`: `draw_actor` (otomatik bakış), `seated(look=)` | `g2_*.jpg` |
| 3 | **SA1-Y5 + SA2-K7:** kopya figürler, 17. yy şapkaları | **KAPANDI** | `cilt_anim`: `_add_hat3` (cappuccio, feltcap), `period_hat`, `_period_spec`, `kit_for`, `inst_jitter`, `clone_vary`, `costume`<br>`cilt_oda.seated` | `g3_*.jpg` |
| 4 | **TE2-Y5:** damga kontrastı 1,9–2,7:1 | **KAPANDI** (`anim.stamp` damgaları; doğrudan `CM.stamp` çağıranlar için SCN'e istek) | `anim`: `stamp`, `stamp_back`, `stamp_back_colors`, yeni `paper_stamp` | `g4_damga_kontrast_once_sonra.jpg`, `g4_damga_kontrast_olcum.txt` |
| 5 | **SA1-E4 kalıntısı:** madalya gölgesi dikey kesik | **KAPANDI** | `cilt_medal`: `medal_shadow(pad=)`, `draw_medal_b`, `SHADOW_PAD` | `g5_madalya_golgesi_once_sonra.jpg` |
| 6 | **SA1 §4:** Cossa madalyasında ermin | **ATLANDI** | `m_cossa` P1'de kullanılmıyor; `scenes_c2`'de yalnız `m_lorenzo` ve `m_cosimo` var | — |
| 7 | **SA2-Ö4:** 1252'de 15. yy kıyafeti | **KISMEN** | Görev 3'ün dönem katmanı: başlık, brokar desen, iki renk çorap, etek boyu. Giysi kesimi çağa bağlı değil | `g3_1252_kostum_once_sonra.jpg` |
| + | **SCN-2 isteği:** c2_sadaka ve catasto'da örnek başına çeşitleme | **YAPILDI** | `inst_jitter` + gevşetilmiş `clone_vary` | `g3_cesitleme_P1_sadaka_catasto_once_sonra.jpg` |
| + | **SCN-2 isteği:** yakın plan el çizimi | **YAPILDI** (üslup içinde) | `cilt_anim`: `_hand_spr`, `_hand_detail`, `HAND_DETAIL_MIN` | `g8_yakin_el_ayrinti_once_sonra.jpg` |

**Kapatma anahtarları:** her yenilik modül düzeyinde kapatılabilir; `False` eski davranışı birebir verir. Tek istisna: renk süzgecinin baş, ayakkabı ve aksesuara taşınması kalıcı bir hata düzeltmesidir, anahtarı yok.

| Anahtar | Ne kapatır |
|---|---|
| `FA.FADE_LAYER` | tek katmanda soldurma |
| `FA.ACT_V2` | hazırlık ve oturma |
| `FA.BLINK` | göz kırpma |
| `FA.FOLLOW` | gecikmeli takip |
| `OD.LOOK_AUTO` | otomatik bakış |
| `FA.PERIOD_COSTUME` | dönem kostümü |
| `FA.CLONE_VARY`, `FA.INST_JITTER` | çeşitleme |
| `FA.HAND_DETAIL_MIN` (çok büyük değer) | el ayrıntısı |
| `anim.STAMP_BACK` | damga fişi |

`cilt_medal.medal_shadow`'un `pad=0` varsayılanı eski sözleşmedir.

---

## 1. Görev 1 · SA2-Y1 — soldurmada baş ve ayakkabı gövdeden önce, opak geliyordu

**Neden (kodda doğrulandı):**
- `draw_fig` başı, ayakkabıları ve kimi durumda gövde parçasını `blit` ile çiziyordu; `blit`'te alfa yoktu.
- Kollar, eller ve etek alfayı ayrı ayrı alıyordu. Yarı saydamken binişen parçalar çift koyulaşıyordu: gövde kolun içinden görünüyordu.
- El aksesuarı (`_prop_fn` → `blit`) ve sancak (`_flag_fn`) da alfasızdı.
- **Ek bulgu:** renk süzgeci (`cf`) de yalnız `cilt_oda` siluet bağlamında başa taşınıyordu. `cilt_sehir.draw_actor` gibi `cf=` veren yollarda siluet gövdenin üstünde renkli baş, ayakkabı ve kese çiziliyordu (`g1_siluet_suzgec_once_sonra.jpg`).

**Düzeltme: tek katmanda soldurma.**
- `alpha < 1` iken figürün bütün parçaları opak olarak bir katmana çizilir, katman tek alfa ile birleştirilir (`saveLayer`, figür sınırlı dikdörtgen: `FIG_BOUNDS`).
- Figürün süzgeci `_CF_CTX` ile `blit`'e taşınır; baş, ayakkabı, aksesuar ve sancak süzülür.
- Uygulandığı yerler:
  - `_draw_pose`: yürüyen, kalabalık, alay;
  - `actor`: masa ve `extra` dahil;
  - `handshake`, `threat`: iki figür aynı katmanda;
  - `draw_rider`: at + binici + sancak;
  - `sil_actor`, `seated`: kenar ışığı ve siluet geçişleri aynı katmanda; yarı saydamken kenar ışığı kopyası siluetin içinden görünmez.
- Alfa 1 iken yol eskisiyle aynı (katman açılmaz).

**P1'de alfa ile soldurulan figürler (tarandı):**
- `c1_kinds`: `FA.actor(alpha=)` (darphane, okul, köşe) ve `OD.sil_actor(alpha=)` (lonca);
- `c2_kinds`: `OD.sil_actor(alpha=)` (rivayet);
- `cilt_oda.draw_actor`: `fade_x`, `fade_out_at`;
- `cilt_sehir.draw_actor`: androne `gate` alfası;
- alay ve kalabalık girişleri (`cx.amt`).

Hepsi düzeltilmiş yollardan geçiyor.

**Kanıt:**

| Dosya | Önce | Sonra |
|---|---|---|
| `g1_villani_once_sonra.jpg` (131,35–131,8 sn) | 131,35'te gövdesiz kırmızı kepli baş; 131,65'te gövde kolun içinden görünüyor | Bütün figür birlikte, düzgün solar |
| `g1_okul_once_sonra.jpg` (144,0–144,6 sn) | Boş duvarda yeşil başlık; yerde ayakkabı | Yok; figürler birlikte belirir |

**Maliyet:** yalnız alfa < 1 karelerinde ≈+%15 (ölçüm: 101 → 116 ms/kare).

## 2. Görev 2 · AN1 — "kukla" oyunculuk (kitin geneli, üslup korunarak)

**Hazırlık (anticipation):** büyük jestten 0,14–0,18 sn önce ters yönde −%5…−%14 karşı hareket. El geri çekilir, gövde dikleşir, belge hafif iner.
- İşlevler: `gesture_env` (gidip dönen jest) ve `gesture_on` (kalıcı jest).
- Kullanan eylemler: `act_point`, `act_bow`, `act_handshake`, `act_admonish`, `act_threat`, `act_kneel`.

**Sönümlü oturma (settle):** aynı zarflar.
- Varışta %3–10 aşma ve sönüm (`anim.settle` yayı).
- Dönüşte dinlenme konumunu %5–7 aşıp oturma.
- El sıkışmada aşma yalnız %3: eller buluşma noktasından geçmesin.
- Diz çökme ve hançer adımında aşma yalnız gövde, baş ve kolda. Kalça ve ayak sınırlı: diz yere girmez, ayak kaymaz.

**Göz kırpma:**
- Figür başına tohumlu evre; 3–6 sn'de bir; 0,21 sn kapak eğrisi, yani 2–3 kare kapalı. Kapalı göz ince kapak çizgisiyle çizilir.
- Yalnız gözü çizilen figürlerde (pişirilmiş baş >11 px), siluette yok.
- İşlevler: `blink_eye`, `Pose.eye`, `_paint_head(eye="closed")`, `draw_fig`.
- Bağlı olduğu yerler: `walker`, `actor`, `crowd`, `handshake`, `seated`.

**Dirsekten gecikmeli takip (follow-through):**
- Konuşmada ön kol bükümü 0,09 sn geriden gelir (`_ft_arm` → `act_talk`).
- Yürüyüşte ön kol üst kolu 0,06 döngü geriden izler (`gait`). Kol artık tek eklemden sallanmıyor.
- Boştaki (idle) figürde gövde neredeyse kıpırdamadığı için takip görünmez; eklemedim.

**Konuşanın başı karşısındakine:**
- `actor(look=(x, y), look_w=)` ve `seated(look=)`.
- Oda sahnelerinde varsayılan (`LOOK_AUTO`): `talk`, `listen`, `point` ve `admonish` eyleminde baş, önündeki en yakın duran figürün başına döner. Eğilme −17…+21°; ağırlık uzaklık sınırında yumuşakça söner. Dict'te `look=False` kapatır.
- İşlevler: `apply_look`; `cilt_oda.draw_actor` (`_room_peers`, `_auto_look`).

**Süreklilik ve sıçrama:**
- `gesture_env` 1/240 sn adımla tarandı: değer −0,14 … 1,11, adım başına en büyük değişim 0,012, hızda sıçrama yok, sonunda 0'a oturuyor.
- Video karelerinde ardışık 24 fps şeritler (§8) sıçrama göstermedi.

**Kanıt:**
- `g2_isaret_seridi_k_degeri.jpg`: T=0,92–1,00'de el geri; 1,75'te %8 aşma; 2,10'da oturma.
- `g2_jest_hazirlik_oturma_video_once_sonra.jpg`: V. Martinus 461,55–462,75 sn; Giovanni 509,6–510,6 sn.
- `g2_goz_kirpma.jpg`: ardışık kareler açık · kapalı · kapalı · açık.
- `g2_bakis_look.jpg`: konuşan oturana eğilir; oturan dinleyen başını kaldırır.

## 3. Görev 3 · SA1-Y5 + SA2-K7 (+ SA2-Ö4 kısmen) — kopya figürler, dönem başlıkları

### 3a. Dönem kostümü (`PERIOD_COSTUME`)

Yıl `donem.year()`'dan okunur: çekim yılı, yani HUD'da en uzun kalan yıl. Yıl yoksa eski çizim. Seçim (tür, seed) ile deterministik: aynı kişi aynı dönemde hep aynı başlıkla çıkar. `costume`'un RNG dizisi değişmedi; sakal, saç, ten ve çorap kimlikleri korunur.

| Yıl sınırı | Eski | Yeni |
|---|---|---|
| <1500 | Geniş kenarlı `straw`, `slouch`, `plume` (siluette 17. yy) | cappuccio, keçe kep, coif; zenginde ≥1380 mazzocchio |
| <1500 | Halkın Frig külahı (231,6 sn'de "tüylü şapka" okunuyordu) | cappuccio ya da keçe kep |
| <1500 | Fransız başlığı | veil ya da coif |
| <1500 | morion | sallet |
| <1480 | tüylü Rönesans bereti | mazzocchio, cappuccio ya da keçe kep |
| <1400 | yüksek brokar şapka | cappuccio ya da veil |
| <1380 | mazzocchio | cappuccio |
| <1340 | flatcap, scholar | cappuccio ya da coif |
| <1340 | brokar desen, iki renk çorap (mi-parti) | yok |
| <1340 | tunik ve orta boy cüppe | tunik dize, cüppe baldıra iner |

**Yeni başlık çizimleri (`_add_hat3`):**
- `cappuccio`: yüzü açık kukuleta + omuz yakası + becchetto. Becchetto tepedeki sivri uçtan dışa kıvrılıp boyundan ayrık sarkar; siluette kukuleta okunur, "uzun saç" değil.
- `feltcap`: yuvarlak keçe kep + dar bant.

### 3b. Örnek başına çeşitleme

İki katman var.

**1. `inst_jitter`:**
- Anonim türlerde tür+seed'e bağlı boy ve giysi tonu: halk, çocuk, denizci ve askerde boy ±%5–6, ton ±%8–11; kadında yalnız ton.
- Kareden ve komşudan bağımsız. Yürüyen, kalabalık ve alay figürlerinde de sıçrama yok; aynı kişi her çekimde aynı.
- Oturan ve kalabalık figürde yalnız ton değişir: masa hizası ve kalabalığın kendi boy dağılımı korunur.

**2. `clone_vary`:**
- **Kapsam:** aynı karede, yakında (Δx ≤ min(2,6·h, 640 px), |Δy| < 0,45·h, boy oranı 0,4–2,5: ön plan/arka plan da sayılır) DURAN aynı türden figürler.
- **Anonim türler:** görünümden bağımsız sıraya göre çeşitlenir.
- **Diğer türler** (banker, soylu, papa…): yalnız gerçek kopyada çeşitlenir: aynı tür+seed ya da aynı başlık+sakal+giysi tonu ailesi. Adı olan kişiler korunur (Giovanni, Cosimo ve Lorenzo'nun hepsi `banker`).
- **Sıra ≥1 olana:**
  - boy ×0,935 / 1,065 / 0,955 …; masa başında boy değişmez;
  - başlık: gruptakiyle aynıysa dönemin başka seçeneği;
  - sakal: aynıysa şablonun başka seçeneği;
  - giysi tonu ±%15–17;
  - poz evresi +0,37.
- **Pop güvenliği:** yalnız `actor` ve `seated`, h ≥ 240. Yürüyen, kalabalık ve alay figürlerinde komşuya bağlı çeşitleme yok, çünkü konumları kayar ve kırpılırlar.
- **Siluet:** iki geçişi aynı örnek sayılır.

**P1'de (SCN-2 düzeninde) sonuç** (`g3_cesitleme_P1_sadaka_catasto_once_sonra.jpg`):

| Sahne | Önce | Sonra |
|---|---|---|
| c2_sadaka, 572,5 sn | İki hasır şapka, üçü de sakallı ve kahverengi | Arka-sol: keçe kep, sakallı, açık ton. Arka-sağ: coif, sakalsız, koyu ton, biraz kısa. Ön: cappuccio, açık ton, biraz uzun |
| catasto, 493 sn | Hane reisinde 1427'de tüylü bere | Keçe kep + örnek başına ton |

Sınama sayfası: `g3_kopya_cesitleme_sinama.jpg`. Tur 2'deki 31/32/33 düzeni ve aynı tür+seed üçlüsü.

### 3c. Kanıt
- `g3_siluet_baslik_once_sonra.jpg`:
  - 231,6 sn: Frig külahı → cappuccio;
  - 262,0 sn: geniş kenarlı şapka → coif;
  - 190,5 sn: geniş kenarlı şapka → cappuccio.
- `g3_1252_kostum_once_sonra.jpg` (110,5 ve 128,6 sn). Darphane işçisi:
  - tüylü kep → cappuccio;
  - zambak desenli kısa tunik → düz, dize inen tunik;
  - iki renk çorap → tek renk.
- `g3_yeni_basliklar_renkli_siluet.jpg`.

## 4. Görev 4 · TE2-Y5 — kaynak damgalarının kontrastı

**Düzeltme (`anim.stamp`, `anim.stamp_ovl` üzerinden bütün P1 damgaları):**
- Damganın altına kâğıt fişi konur: koyu mürekkep → açık kâğıt, gece açık mürekkep → koyu kâğıt.
- Fiş %95 örtücü; çerçeveden ≈0,17·boy büyük; ±0,5–1° farklı açıyla oturur; yumuşak gölgeli ve ince kenarlıdır.
- Fiş damganın OTURDUĞU yerde sabittir: damga ona vurur; yaklaşımda yumuşakça belirir, sıçrama yok.
- **Mürekkep tonu:** nominal ≥7:1 olacak kadar koyulaşır (#A8321E → #8C2919; perde 3 sinabarına yakın). Gece ≥6:1 için açılır (#E56A52 → #E87A64).
- **Korunanlar:** kırmızı mürekkep, eğiklik, çift çerçeve, profil vuruşları. Mürekkep yayılması fiş üstünde %16'dan %7'ye iner.
- **`anim.paper_stamp(f, text, x, y, rot, size, color, alpha, t)`:** `CM.stamp` ile aynı imza. Sahnelerdeki doğrudan çağrılar için, tek satırlık değişim (§9).

**Ölçüm:**
- **Yöntem:** son kare (renk derecelendirme ve deklanşör dahil). Yazı maskesi `CM.stamp`'in kendi `draw_spr` matrisiyle ayrı yüzeye çizildi. Yazı çekirdeği medyanı ile yazının 0,2·boy çevresindeki zemin medyanı karşılaştırıldı.
- **Sonuç:** ÖNCE (`STAMP_BACK=False`) **1,1–4,1:1** → SONRA **5,3–5,8:1**; 15 damga, 17 ölçüm. Örnekler:

| Damga | Önce | Sonra |
|---|---|---|
| BİR KAYNAĞA GÖRE | 1,1 | 5,3 |
| ANEKDOT | 1,3 | 5,6 |
| İTİRAZ | 1,3 | 5,6 |
| DESTEKLEDİ | 2,0 | 5,6 |
| VILLANI'YE GÖRE | 2,6 | 5,6 |
| ÇEVİRİ | 2,4 | 5,5 |

- **Neden nominal hedef 7:1:** renk derecelendirme kontrastı ≈%30 düşürüyor.
- **Ayrıntı:** `g4_damga_kontrast_olcum.txt`.

**Kanıt:** `g4_damga_kontrast_once_sonra.jpg`.

## 5. Görev 5 · SA1-E4 kalıntısı — madalya gölgesinin dikey kesiği

**Neden:**
- `medal_shadow` 720×720 alfa tuvalini σ=16 ile bulanıklaştırıyordu.
- Disk kenarı tuval kenarından 11 px içerideydi; gölge tuval sınırında 118–125 alfa ile kesiliyordu.

**Düzeltme:**
- `medal_shadow(..., pad)`: tuval her yandan `SHADOW_PAD`=64 px (≥4σ) büyütülür.
- `draw_medal_b` gölgeyi −360−pad ofsetiyle çizer.
- `pad=0` varsayılanı eski sözleşmedir; c7_kinds ve c8_kinds çağrıları aynen çalışır.

**Ölçüm:**
- **Lorenzo, 531,0 sn:** x≈886 boyunca tutarlı dikey basamak 9,7 → 1,4 gri düzey.
- **Cosimo, 580,5 sn:** x≈998'deki 28,4 düzeylik kenar → yok. 582,0 sn: 24,9 → yok.

**Kanıt:** `g5_madalya_golgesi_once_sonra.jpg` (ham + yüksek geçiren).

## 6–7. İsteğe bağlılar
- **Görev 6 (Cossa ermini):** `m_cossa` P1'de yok; atlandı. Lorenzo'nun saç ve burnu P3'e kaldı; yapılmadı.
- **Görev 7 (SA2-Ö4):** 1340 öncesi kural başlık, desen, çorap ve etek boyunu çağa bağlıyor (§3a).
  - Giysi KESİMİ (`_robe_params`/robe_path biçimleri) için çağa bağlı ayrı ön ayar kurmadım; yeni kesim ailesi yeni boyama demek.
  - Önerim: P2'den önce 'gonnella' (13–14. yy uzun, düz, kemerli) ve 'giornea' (15. yy yarık üstlük) kesimlerinin eklenmesi.

## 8. SCN-2 isteği · yakın plan el (`c2_yakin`, `c2_masa`)

**Yapılan (`_hand_spr` + `_hand_detail`):** el boyu ≥26 px olunca fresk çizgi diliyle ayrıntı eklenir.
- parmak ayrımları;
- boğum ve bilek kıvrımları;
- yumruk katları;
- açık tırnaklar (işaret, başparmak, uç).

**Kapsam:** küçük figürlerin eli değişmez. El sprite'ı önbellekte; yeni maliyet yok.

**Sınır:** dış çizgi aynı kaldı. Kalın kontürlü "eldiven" biçimi üslubun parçası; parmak uçlarını kontürde ayırmak bütün figürlerin elini değiştirirdi.

**Kanıt:** `g8_yakin_el_ayrinti_once_sonra.jpg`: kese 358,5 sn, mitra 470,9 sn, kalem 577,0 sn.

## 9. Gerileme kontrolü

**qa_flow --part 1:**

| Koşu | Sonuç |
|---|---|
| 1. Görev 1–5 sonrası | **20 GEÇTİ · 0 KALDI · 1 UYARI · 1 PAS** |
| 2. Çeşitleme + el eklemeleri sonrası | 19 GEÇTİ · **1 KALDI** · 1 UYARI · 1 PAS |
| 3. Güncel kodla yeniden | (aşağıda güncellenir) |

**2. koşudaki KALDI benim değişikliğimden gelmiyor:**
- Kapı: "Beyan ↔ gerçekleşen kamera", #63 `p1_map` 361,1 sn; gerekçe "harita KADRAJ KORUMASI durduruyor".
- O çekimde figür ve damga yok; figür taraması 0 figür, damga taraması 0 damga buldu.
- Kapı ve harita kadraj koruması koşum sırasında başka ajanca değiştirildi (ENG-D alanı): `cilt_cam.py` 07:13, `p1_ortak.py` 07:12, `qa_flow.py` 07:14.

- v2'de: 17 GEÇTİ · 0 KALDI. Yeni kapılar ENG-D'nin.
- Yerleşim (ENG-A): 303 kare, İHLAL 0. Dönem (ENG-A): 306 kare, İHLAL 0.
- Tek uyarı eski yön uyarısı (#15 p1_skyline).
- KALDI artmadı.

**P1'in bütün figürlü çekimleri:** 47 çekimin her birinden çekim ortasında birer son kare. Bozulma, kırpık katman ya da renk sızması yok. Sayfalar: `g9_gerileme_figurlu_cekimler_1.jpg`, `g9_gerileme_figurlu_cekimler_2.jpg`.

**Eylem başlangıçlarında ardışık kareler (24 fps):** yerel kare farkında sıçrama aranan pencereler:

| Olay | Pencere (sn) |
|---|---|
| işaret (Salvestro) | 223,5–224,9 |
| selam | 387,4–388,8 |
| selam | 394,9–396,3 |
| kardinal işaret | 443,3–444,6 |
| Martinus işaret | 461,5–462,9 |
| aforoz belgesi + selam | 471,8–473,9 |
| selam (catasto) | 489,2–490,6 |
| Giovanni işaret | 509,5–510,9 |
| üç yoksul selam | 570,9–572,6 |
| soldurma | 130,9–132,0 |
| soldurma | 144,3–145,4 |
| ink damgası | 156,1–157,2 |
| squash damgası | 505,0–506,0 |

- Figürde sıçrama yok.
- Aday çıkan yerler damga vuruşu (İTİRAZ spin, DESTEKLEDİ squash) ve soldurmanın kendisi; şeritlerde gözle doğrulandı. Tasarlı hareket, pop değil.

**P2–P7 duman testi:** her parçanın her çekiminin ortası çizildi; son değişikliklerden (çeşitleme, el) sonra yeniden koşuldu, sonuç aynı.

| Parça | Çekim | Figürlü | Hata |
|---|---|---|---|
| P2 | 116 | 54 | 0 |
| P3 | 99 | 33 | 0 |
| P4 | 76 | 21 | 0 |
| P5 | 47 | 23 | 0 |
| P6 | 86 | 24 | 0 |
| P7 | 84 | 17 | 0 |

Görsel bakış normal. 1433/1449/1478 alay ve odalarında dönem başlıkları devrede.

## 10. SCN'e istekler

**SCN-1 (c0–c1):**
1. **VİLLANİ'YE GÖRE · TAHMİN damgası** (`scenes_c1.py` ≈65. satır: x=1420, y=290): 142,8 sn'den sonra "90.000" sayaç kartının üst kenarına biniyor. Kâğıt fişi rakamın üstünü artık örtüyor. Damgayı y≈225'e çek ya da sayaçtan önce söndür (`out=`). Bu, TE2-Y5'in ikinci maddesi.
2. **Doğrudan `CM.stamp` → `anim.paper_stamp`** (aynı imza; fiş + ≥4,5:1):
   - `c0_kinds.py`: "FRANSIZCA" ≈272, "ÇEVİRİ" (c0_gerekce) ≈866;
   - `c1_kinds.py`: "ÖDENMEDİ" ≈490, `stamp_text` ≈726, "KAYBEDENLERİN AİLESİNDEN" ≈1072.
3. **262 sn isyancı silueti** (`c1_kinds.py` ≈679): 17. yy şapkası, çekim yılı 1378 olduğu için gitti. Çekim yılı 1520'ye (Machiavelli) çevrilirse kural devreden çıkar; o durumda çağrıya `hat="cappuccio"` yazın.
4. **(İsteğe bağlı) `cilt_sehir.ring_members`:** seed aralığı 0–40; halkada aynı tür+seed kopyaları var. Kopya çeşitlemesi pop güvenliği için halkalara uygulanmıyor. `rs.randint(0, 9999)` önerilir.

**SCN-2 (c2, p1_ortak):**
1. **Doğrudan `CM.stamp` → `anim.paper_stamp`:**
   - `c2_kinds.py`: "KAYNAKLAR AYRIŞIYOR" ≈304, "İTİRAZ" ≈378, "AFOROZ TEHDİDİ" ≈449, `src_stamp` ≈456, "ANEKDOT" ≈624 ve ≈667;
   - `p1_ortak.stamp` (≈114).
2. **Oda sahnelerinde bakış:** belirli birine bakılacaksa actor dict'ine `look=(x, y_baş)` yazın; istenmeyen yerde `look=False`.

**ENG-A / ENG-D:**
- `qa_donem` için isteğe bağlı kostüm kuralı. `DN.note` yazmadım: çekim dışı çizimde "yil_yok" ihlali üretmesin diye. Bağımsız ayna olarak `cilt_anim.period_hat(kind, hat, yıl)` kullanılabilir.
- `qa_yerlesim`: damga fişi kutusu levha–damga çakışma denetimine alınabilir.
- P2/P3 madalyaları (`c7_kinds.py:1139`, `c8_kinds.py:1277,1379`) eski `medal_shadow` (pad=0) ile kesik gölge çizer. `CMD.medal_shadow(..., pad=CMD.SHADOW_PAD)` + ofset −360−pad'e geçilmeli.

## 11. Açık kalanlar
- **Oturan konuşma (`cilt_oda.act_sit_talk`):** gecikmeli takip uygulanmadı; işlev sahiplik listemde değil.
- **Kopya çeşitlemesi kapsam dışında kalanlar:** yürüyen, kalabalık, alay ve halka figürleri. Bunlarda yalnız kareden bağımsız tür+seed çeşitlemesi (`inst_jitter`) var.
- **Bakış:** baş yalnız eğilir; karşıdaki arkadaysa baş çevrilmez. Ayna baş "pop" üretirdi.
- **SA2-Ö4:** giysi kesimi çağa bağlı değil (§6–7).
- **Damga fişi:** yalnız `anim.stamp`/`stamp_ovl` damgalarında. Doğrudan `CM.stamp` çağıranlar SCN değişikliğine bağlı. P1'de şimdilik iki damga dili yan yana: fişli ve fişsiz.
- **Alanım dışı okunurluk maddeleri:** TE2'nin KUR FARKI yaldız rakamı ve zaman ekseni yılları.

## 12. En emin olmadığım nokta

**1. Varsayılanları değiştirdim.**
- Hazırlık ve oturma, göz kırpma, takip, otomatik bakış, dönem kostümü ve anonim türlerde tür+seed çeşitlemesi varsayılan olarak AÇIK. P2–P7'deki figürleri de değiştiriyor.
- Gerekçe: AN1 ve SA1 "kitin geneline" dedi.
- Yaptığım denetimler: duman testi hatasız; kurul henüz görmedi.
- Başkan P2–P7'yi eski görünümde tutmak isterse modül anahtarlarıyla kapatabilir (§0).
- En tartışmalı olan, anonim türlerde ±%5–6 boy farkı. P2–P7'de figürü sabit bir nesneye (kapı, masa) göre hizalayan sahne varsa birkaç piksel kayabilir.

**2. Damga fişi bir üslup kararı.**
- Kontrast hedefini sağlıyor. Ama "mürekkep doğrudan freske basılmış" dilinden "kâğıt fişe basılmış" dile geçiş.
- Sanat yönetmeni (SA1) sevmeyebilir.
- Alternatif: yalnız arka plan karmaşıksa fiş çizmek. Bunu kare kare değişen kararla yapmak titreme riski taşıdığı için seçmedim.
