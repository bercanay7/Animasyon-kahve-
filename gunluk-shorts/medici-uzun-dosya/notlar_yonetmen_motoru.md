# Yönetmenlik motoru — notlar (Lab-A, 18 Ekim 2026)

Kapsam: `YONETMENLIK_REHBERI.md` (SPEC) §2 kamera sözlüğü, §3 geçiş sözlüğü, §9 parça planı, §10 kapılar için motor tarafı.
Dosyalar: `cilt_cam.py` (yeni), `cilt_fx.py`, `cilt_medici.py` (ckind + Cam), `compose.py`, `cilt_kinds.py` (yalnız `chapter_card`), `cilt_hero.py`, `shots.py` (yalnız `Shot/shot/Ctx` alanları), `qa_flow.py` (yeni), `preview_reel.py` (yeni).
Kanıt: `out/reel_yonetmen.mp4` (59 sn, 1920×1080, 24 fps), `out/frames/reel_sheet.png` (+ `reel_sheet_tr.png`, `reel_sheet_cam.png`), `out/qa_flow.json`.

## 0. SPEC düzeltmeleri (yalnız §2 ve §3 değişti; API adları gerçek koda uyduruldu)

1. §2: `cam=` verilmezse türün **eski varsayılanı** (yavaş push + drift) çalışır (eski sahneler bozulmaz); yeni kamera yalnız `cam=` verilince devreye girer. `qa_flow` `cam=`'siz çekimi "örtük" sayıp Kamera kapısını KALDI yapar ("her çekimde açıkça yaz").
2. §2: `pan r` = **kamera sağa gider, içerik ekranda sola akar** (zaman çizgisi soldan sağa okunur); `crane up` = kamera yükselir, içerik aşağı akar. Tüm geçişlerde `dir` de KAMERA yönüdür.
3. §2: `rack` imzası `("rack", (xa,ya), (xb,yb)[, dict(at=çapa, dur=sn, r=px, sigma=px)])`: odak NOKTALARI (px; 0–2 aralığı ekran oranı); "katman bulanıklığı pişirme" yerine son-kare çevre bulanıklığı (odak dairesi keskin).
4. §2: anahtar kareli biçim `(x, y, zoom, rot)` anlamı yazıldı (x,y kamera konumu px; +x kamera sağa; rot derece, + = içerik saat yönünde); sonuna isteğe bağlı `dict` (pivot/push/hand/drift) eklenebilir; `("track", id)` kayıt defteri `cilt_cam.register_track`.
5. §2: kamera uçları geçişte durmaz (CARRY = ortalama hızın %65'i); şerit türlerinde (`skyline/frieze/procession`) `pan` türün kendi kaydırmasına çevrilir, kendi kamerası olan türlerde (`pano`, `build`) `cam=` uygulanmaz; `map` için `view=(lon,lat,zoom)`.
6. §3: `tr=(ad, süre[, opts])` + opts sözlüğü (iris: `at/r/obj/inv`; slide: `dir/seam/punch`; zoomthru: `at/at_b/depth`; carry: `strip/dir`; light: `at/col/rays/dim/tint`; candle: `at/at_b`); ortak `place/lead/birth`; `link` sözlüğü. "Eklenecek" → "Eklendi".

## Komutlar (proje dizininden; `python3`, `-I` yok)

```
python3 preview_reel.py --workers 2 --qa     # reel mp4 + 3 kontak sayfası + qa_flow (≈3 dk, 2 işçi)
python3 preview_reel.py --sheet              # yalnız kontak sayfaları      · --range 30 40 → out/reel_part.mp4 (hızlı deneme)
python3 qa_flow.py --reel [--video out/reel_yonetmen.mp4] [--fast]    # --fast = yalnız statik analiz
python3 qa_flow.py --part 2 [--fast]         # gerçek film, parça zaman çizelgesiyle (out_pN/timeline.json)  · --chapters c3,c4
python3 qa_flow.py --calibrate               # τ kalibrasyon ölçümü
python3 cilt_cam.py                          # kamera öz sınaması
python3 preview_cilt.py --only trans2        # yeni geçişlerin k=0,5 karesi (tek sayfa)
```

## 1. API özeti

### `shots.shot(...)` ve `Shot`
```python
shot(kind, a, tr=None, label="", cam=None, link=None, longtake=False, montage=False, **tür_parametreleri)
```
`Shot` alanları: `cam, link, longtake, montage` (qa_flow okur) · Program doldurur: `cam_in, cam_out` (geçişte kamera devri), `lead` (gelen çekim saati önden başlar), `tr_eff=(ad, süre, opts)` · `Shot.origin = t0 − lead` (yerel saat 0'ın küresel karşılığı; **sfx kuyruğu üretirken `cx.g = origin + t` kullan**).
`Ctx`: `cx.cam_spec, cx.cam_in/out, cx.lead, cx.link` + `cx.at()` lead'e duyarlı (anlatı çapaları her zaman doğru). `map` türünde `cam=(lon,lat,zoom)` (üç sayı) eski tür parametresi olarak kalır; kamera ön ayarıyla birlikte `view=` kullan.

Örnek satırlar:
```python
shot("skyline", ("c1s9", -0.2), tr=("iris", 0.9, dict(at=(960,508), obj="florin", r=252)), link="shape",
     cam=("crane", "up", 130), seed=1, pan=170, kick="FLORANSA, 1434", label="Floransa şafakta")
shot("map", ("c8s2", 0), view=(11.25, 43.77, 2.3), link="scale", tr=("zoomthru", 1.0, dict(at=(890, 510))),
     cam=[(0, (0,0,1,0)), (("c8s2","Floransa",-0.1), (40,18,1.25,0)), (("c8s4",0), (70,30,1.5,0))], label="harita")
shot("medal", ("c7s12", 0), cam=("rack", (960,470), (960,925), dict(at=("c7s12","levha",0), dur=1.4, r=340)), key="m_cosimo", name="COSIMO DE' MEDICI")
shot("quote", a, cam=("pan", "r", 160, dict(hand=1.5)), tr=("carry", 0.95, dict(dir="r", strip="banner")), link="carry", text="…")
shot("palle", a, cam=("orbit", 10), tr=("light", 0.9, dict(at=(960, 650))), link="light", kick="ALTI TOP")
shot("tree", a, mode="night", cam=("track", "sweep_r"), tr=("candle", 1.0, dict(at=(1730, 600))), link="light", …)
```
Çapa biçimleri (cam anahtar karelerinde de): `saniye | "sid" | ("sid", ofset) | ("sid","sözcük",ofset) | ("sid","sözcük",nth,ofset)`.

### Kamera (`cilt_cam.py`)
`parse(spec)`, `state(cx, spec)` → `CamState(x, y, zoom, rot, dx, dy, s, pivot, blur, focus, ws, wdx, wdy)`; `register_track(ad, [(u,(x,y,zoom,rot)),…] | callable)`; `describe(spec)` (qa); `motion_ok(spec)` (≥%6 / ≥120 px); `BAND_KINDS`, `OWN_CAMERA`; `python3 cilt_cam.py` öz sınama (t<0 / t>dur hız sürekliliği, hand determinizmi).
Zaman profili: Hermite (smoothstep ≡ ease_io); `cam_in/cam_out` açıkken uç eğimi `CARRY=0,65`; t<0 ve t>dur doğrusal uzatılır (eğim sürekli) → gelen çekim hareket halinde başlar, giden durmadan sürer. `hand` seed = `cx.seed` (çekim sırası); beş sinüs toplamı, deterministik.
Duvar: içeriğin %40'ı kadar paralaks (orbit'te ters yön), `ws` ekranı örtecek şekilde otomatik büyür (`wall_cover`). `rot` yalnız içeriğe uygulanır (tam-kare döndürme ~90 ms).
Yeni türler için: `@ckind` kullan → `cam/link/longtake/montage` otomatik ayıklanır; `CM.Cam(cx, …)` spec varsa onu uygular; kamerayı kendin çiziyorsan `cx.cam_state` (None = spec yok) ham değerleri (`x, y, zoom, rot`) verir. Türün kendi `cam` parametresi tanımlanamaz (map hariç). `pano/build` kendi yolunu kullanır (spec uygulanmaz); `("track", id)` kaydını pano kendi dünya koordinatında yorumlamak isterse `cilt_cam.TRACKS[id]`'i okuyabilir.
`map` türü: `mapsk.Cam` çağrı süresince yamalanır (ekran-uzayı kayma/zoom → dünya merkezi/zoom); kendi `drift` itmesi sıfırlanır (çift itme olmasın). `orbit` map'te dönüş uygulamaz.

### Geçişler (`cilt_fx.py`)
`TR` kaydı: `yikama, sayfa, giornata` (eski) + `iris, slide, zoomthru, carry, light, candle` (yeni). `blend(kind, a, b, k, g=0.0, d=0.8, **opts)`; `norm_tr(tr)`; `lead_for(ad, d, opts)`; `NEW_TR`, `NO_CARRY=("dip","candle")`, `BIRTH`.
Süre ≤1,0 sn (norm_tr kırpar). Ortak opts: `place="before"|"after"`, `lead=True|False`, `birth=sn`. `link` sözlüğü: `shape color dir cam scale carry light material audio`.

| geçiş | opts (varsayılan) | not |
|---|---|---|
| `iris` | `at=(960,508)`, `r` (obj'ye göre 95–270), `obj="florin\|palle\|sun\|moon\|dome\|lens\|seal"`, `inv=False` | A, nesneyle birlikte büyür; B halkanın içinde; `r` ekrandaki nesneye elle eşlenir |
| `slide` | `dir="r"`, `seam=True`, `punch=0.03` | iki çekim birlikte kayar; hareket bulanıklığı (σ≈hız·0,15) |
| `zoomthru` | `at`, `at_b`, `depth=5.0` | A zum + B geri çekilme; zum bulanıklığı, çözülmede ince oker sır |
| `carry` | `strip="ribbon\|ink\|banner\|paper"`, `dir="r"` | eğik şerit (%10 eğim), değişim şeridin arkasında |
| `light` | `at=(960,864)`, `col`, `rays=True`, `dim=0.46`, `tint=0.55` | çevre kararır + sıcak boya + huzme; beyaza boğulmaz |
| `candle` | `at=(960,670)`, `at_b` | mum + ışık havuzu (alan ~doğrusal daralır/genişler), duman, ~0,2 sn karanlık |

**Lead / birth:** yeni geçişlerde gelen çekimin yerel saati `lead = süre + birth` kadar ÖNCE başlar (varsayılan `birth`: iris 0,9 · slide 0,9 · carry 0,9 · zoomthru 0,5 · light 0,6 · candle 0,5; eski geçişlerde 0,6–0,7, `whip` 0). Böylece B, geçişte boş duvar değil doğmuş bir çekim olarak görünür. Anlatı çapaları (`cx.at`) etkilenmez; **mutlak yerel saniyeler (`at=0.4`) lead kadar erken gelir** (kesmeden 0,4 sn sonra için `at = lead + 0.4`; `FX.lead_for(*FX.norm_tr(tr))`). Eski geçişlerde varsayılan kapalı (`lead=True` açar); `place="after"` ve `whip` lead almaz.

### Program, parçalar, bölüm kartı (`compose.py`)
```python
Program()                      # tam film (eski davranış)
Program(part=2)                # Parça 2: c7 t=0'da (kart yok), 1,2→4,8 sn başlık bindirmesi, bitiş ekranı "SIRADAKİ PARÇA"
Program(chapters=["c3","c4"])  # alt küme (eski davranış)
Program(shots=[...], end=T)    # çekim listesi: reel / qa_flow (HUD/bölüm mantığı yok)
```
`part=None` → `MEDICI_PART` ortam değişkeni ya da `out`→`out_pN` bağlantısı (parca.py düzeni); `part=0` → tam film. `part=N` verilince `out_pN/timeline.json` varsa o yüklenir (`SH.TL` değiştirilir; parçanın ilk bölümü t=0), yoksa genel çizelge `t_off` ile kaydırılır. `prog.total` parça uzunluğu, `prog.frame(n)` n=0 parçanın ilk karesi, HUD/progress_line parça içi.
`PERDE_OF`: c0–c6→1, c7–c11→2, c12–c16→3 · `PERDE_FIRST={"c1":1,"c7":2,"c12":3}` · `FX.PERDE_NAMES={1:"ALTIN",2:"BEDEL",3:"MİRAS"}` · P1: c0 sonrası `fresco_title`; P2/P3: ayrı başlık kartı yok, ilk çekimin üzerinde `FX.part_title` ("MEDİCİ" yaldız + "PARÇA II — BEDEL"). `outro(part=…)`: P1/P2 sol "SIRADAKİ PARÇA", P3 "TÜM FİLM", sağ "ABONE OL · ZAMAN KURYESİ"; part=None → "SIRADAKİ TESLİMAT". Sahne modülü `OUTRO_TR = ("iris", 1.0, dict(obj="florin"))` ile kapanış geçişini seçebilir (varsayılan: `yikama`, `place="after"`).
Bölüm kartı ve ana başlık girişi: `tr=("yikama", 0.9, dict(place="after"))`, `link="material"` (anlatının son sözcükleri örtülmez; önceki çekim kamerasıyla sürer). **Canlı kart:** kayan pigment bulutları + eğik tarama ışığı + kamera sürüklenmesi, yazı 0,28–2,55 sn; kart 3 sn kalır.
Renk derecelendirme geçişte gün↔gece değişiyorsa iki LUT yumuşakça karıştırılır (sıçrama yok). Bilinmeyen geçiş adı / geçersiz `cam=` / çözülemeyen cam çapası Program kurulurken hata verir.

### qa_flow
`python3 qa_flow.py --reel [--fast] [--video out/reel_yonetmen.mp4]` · `--part N` · `--chapters c3,c4` · `--calibrate` · `qa_flow.run_shots(liste, end=T)`. Statik kapılar: kamera varlığı + hareket yeterliliği, gerekçeli geçiş (+ çıplak fade, ≥3 üst üste, sözlük dışı link), çekim uzunluğu, tür tekrarı, çapa tipi, yön, altyazı bölgesi, yönetmen kartı (`yonetmen_cK.md` ↔ shots). Örnekleme: her 0,5 sn'de bir kare (240×135 gri) → MAD; parlaklık normalizasyonlu (MAD/clamp(ort/150, 0,3, 1)); durgunluk koşusu ≤1,5 sn; olay yoğunluğu (cümle penceresi, yoksa 3 sn). Video: ffmpeg `freezedetect=n=-55dB:d=1`. Çıktı: tablo + `out/qa_flow.json`; ölçülemeyen kapı PAS + neden.
**τ kalibrasyonu (TAU=0,40):** sabit çekim MAD 0,03–0,04 (quote/timeline/title), 0,2 (medal: eğilme+parıltı), 0,8 (palle: yaldız parıltısı); push %4/6 sn → 0,6–1,5; push %6 → 0,85–1,9; eski varsayılan kamera 0,8–2,9; reel kararlı aralıklar p5=0,67, p10=1,17, medyan 4,2 → τ sabit çekimin 10× üstünde, yavaş kameranın altında.

## 2. Ölçümler (1920×1080, tek iş parçacığı cv2, paylaşımlı CPU)

Geçiş işlevi tek başına (ms, 6 k değeri): iris florin ort 58 / maks 107 · slide 34/41 · zoomthru 34/63 · carry ribbon 85/99, banner 68/82, ink 46/49, paper 41/46 · light 38/41 · candle 26/30 · eski: yikama **363 → ~65** (numpy/cv2'ye taşındı, aynı görünüm: ort. fark ≤0,2, maks 4 düzey; referans `blend_wash_skia` korundu) · sayfa 23 · giornata 22.
Tam kare (`Program.frame`: iki çekim + geçiş + post + rgb), reel geçiş pencereleri maks: iris 254 · slide 302 · giornata 238 · zoomthru 334 · sayfa 406 (defter+mektup çekimleri ağır) · light 381 · carry banner 234 · candle 202/391 · yikama 212 · whip 392 · carry ink 302 · slide 232. `CM.post` ≈35 ms, `Frame.rgb` ≈6–9 ms.
Reel: 1416 kare (59,0 sn, 24 fps), 2 işçi, 131–185 sn (aynı anda çalışan başka işlere göre değişir; son koşu 131 sn ≈ 93 ms/kare/işçi-ortalama 120–250 ms/kare); MP4 ≈76 MB (crf 18). qa_flow örnekleme: 118 kare / 25 sn (2 işçi, 309 ms/kare).
Reel sonucu (`qa_flow --reel --video`): durgunluk **GEÇTİ** (en uzun durgun koşu 0,0 sn; eşik ≤1,5), kamera varlığı %100, link≠none %100, çıplak fade %0, medyan çekim 4,0 sn, tür tekrarı 0, olay yoğunluğu %100, donma 0 olay; UYARI: altyazı bölgesi (network, medal levhası: tür düzeni); PAS: çapa (reel çapasız), yönetmen kartı (reel). Ek video analizi (mp4, 240×135 gri, kare kare): en büyük ortalama-parlaklık adımı +25 (yikama gece→gündüz süpürmesi; yaklaşık 14 karede 45→187, S eğrisi) ve −24 (mum sönmesi; ilk sürümde kenardaki alevde −33'tü → `cilt_fx.CANDLE_P`=0,62 ile ≈−23'e indirildi, ortada alevde de ≈23); kare-farkı (MAD) sıçraması yalnız yikama süpürmesinde (27; geçişin kendi hareketi), başka yerde komşu medyanın 3,5×'ini aşan ve MAD>2 olan adım yok; özdeş ardışık kare çifti 2 = iki mum geçişinin tam karanlık anı (kasıtlı, ≈0,08 sn). Geçiş pencerelerinde kare başına en büyük |Δluma|: yikama 25 · mum 24 · carry2 16 · whip 14 · diğerleri ≤7.

## 3. Bilinen kusurlar

- `slide`: gerçek paralaks yok (düz görüntü kayması + hareket bulanıklığı + zum vuruşu + dikiş çizgisi).
- `rack`: katman bulanıklığı değil, son-kare çevre bulanıklığı (σ=5 px, odak yer değiştirirken ×1,55'e kadar; 1/4 çözünürlükte); odak dışı metin yumuşar. `orbit`: perspektif yok (paralaks + ≤1° yuvarlanma); `rot` yalnız içeriğe (duvar/korniş dönmez); `map` türünde dönüş uygulanmaz.
- Şerit türleri: `frieze` sola `pan` yerleşik kaydırmaya çevrilemez (genel öteleme + örtme zumu: 240 px'te ≈%12 zum); skyline'da `pan>500 px` aynı şekilde.
- `iris` halkası A'daki nesneye `r=` ile elle eşlenir (dönen sikke yandan görünürken halka daha büyük kalır). `candle` mumu geçişin kendi nesnesidir (sahnedeki içerikle çakışmaması `at` seçimine bağlı).
- `lead`: mutlak yerel `at` değerleri lead kadar erken gelir (çapalılar etkilenmez); eski geçişlerde lead kapalı → gelen çekim t<0'da boş duvar (kamera yine hareket halinde). `cx.seed = çekim sırası×7+3` Program yapısına bağlı: aynı çekim parçada ve tam filmde farklı `hand`/mum tohumu alır (görünüm aynı, titreşim deseni farklı).
- Kontak sayfası/gözle denetimde medal türünde yaldız parıltısı yüzün sağ yarısını silik gösteriyor (kind sahibine not). Tree (gece) düğümleri düşük kontrastlı. `whip` hâlâ ~100–200 ms (skia bulanıklığı; "aynen kalsın").
- Altyazı bölgesi: SPEC'teki y≈1250–1390 Shorts (1080×1920) koordinatıdır; 1080p'de alt şerit y≈938–1042 varsayıldı, kapı yalnız tür düzen tablosundan (coin, palle, emblem, medal, counter, quote, timeline, tree, network, title) denetler; ledger/letter/map/frieze/skyline ölçülemedi (PAS notu). Medal levhası ve network düğüm etiketleri tür düzeni gereği bölgeye giriyor.
- Örnekleme 2 kare/sn: 0,5 sn'den kısa olay/hareket sıçramaları kaçabilir; `--video` donma denetimi bunu kısmen tamamlar.

## 4. SPEC'ten sapmalar (bilinçli)

`cam=` varsayılanı (bkz. 0.1) · `rack` noktalar/son-kare bulanıklığı · `iris` "daralır" = `inv=True` · `slide` paralaks yerine zum vuruşu · başlık: Türkçe büyük harf **"MEDİCİ"** (SPEC'te "MEDICI") · başlık bindirmesi 1,2. sn'de girer (0,9 sn açılım), 4,8. sn'de çıkar (0,8 sn solma) · bölüm kartı yazısı 0,28–2,55 sn arasında görünür (2,27 sn; kart 3 sn kalır, kalanı canlı arka plan) · olay yoğunluğu 0,5 sn örnek farkından (cümle çapası yoksa 3 sn pencere) · altyazı bölgesi varsayımı · durgunluk metriği parlaklık-normalizasyonlu · `lead/birth` ve `place` kavramları SPEC'te yoktu (motor gereği) · `fade`'ler `link` ile gerekçelendirilir (çıplak fade = link'siz fade).
