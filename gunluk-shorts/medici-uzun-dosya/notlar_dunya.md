# Dünya ve figür animasyonu — Görev B notları (18 Ekim 2026)

Sözleşme: `YONETMENLIK_REHBERI.md` §1, §2, §6, §8. Bu iş Lab-A dosyalarına (`compose.py, cilt_fx.py, cilt_medici.py, cilt_cam.py, qa_flow.py, preview_reel.py, cilt_hero.py,
preview_cilt.py, shots.py, cilt_kinds.py`) **dokunmaz**; yalnız okur. Yüklenme: `cilt_kinds4.py` SONUNDA `import cilt_anim, cilt_pano, cilt_build  # noqa`.
`python3 -c "import shots, compose"` hatasız (yalnız ortamın skia/fontconfig uyarısı çıkar; bizden değil).

| dosya | satır | ne |
|---|---|---|
| `cilt_anim.py` | 2615 | eklemli (iskelet interpolasyonlu) figür kiti + at + kalabalık + alay + `procession` çekim türü |
| `cilt_pano.py` | 2126 | `pano` çekim türü: katmanlı uzun plan motoru + 3 hazır dünya (florence / nave / corridor) |
| `cilt_build.py` | 1570 | `build` çekim türü: `dome` (Brunelleschi kubbesi) ve `uffizi` (iki kanatlı avlu) zaman atlamalı yapım |
| `preview_world.py` | 324 | kontak sayfaları `out/frames/world_<ad>.png` + klipler `out/clips/world_<ad>.mp4` + ölçüm |

## 1. API

### 1.1 Figür kiti (`import cilt_anim as FA`)
Hepsi `f = cx.f` üzerine çizer; `x, y` = AYAK noktası (ekran), `h` = nominal boy (px), `t` = çekim saniyesi. Tüm figürler `cilt_figs` ile aynı çizgi/pigment dilinde
(mürekkep dış hat `#2A1A0C`, ışık sol-üstten) kemik iskeletiyle (2 kemikli IK, ayak kaymaz) hareket eder; kare çevirme (flipbook) yoktur.

```python
FA.walker(f, kind, x, y, h, t, speed=90.0, dir=1, phase=0.0, seed=0, alpha=1.0, run=False, prop=None, flag=None, **stil)
FA.actor(f, kind, x, y, h, t, action="idle", dir=1, seed=0, phase=0.0, alpha=1.0, prop=None, **eylem_parametreleri)
FA.rider(f, x, y, h, t, speed=120.0, gait="walk"|"trot"|"gallop", dir=1, seed=0, prop=None, **stil)          # at + binici; toynak kaymaz
FA.crowd(f, t, rect, n, seed=1, wave=0.0, mode="mill", dir=1, h=(130,240), speed=70.0, mix=None, scroll=0.0, rise_at=None, wave_speed=1.0, view=None)
FA.procession_cast(seed, dirn, density=1.0, mix=None, rows=None, span=None, margin=520);  FA.procession(f, t, cast, dirn=1, speed=120.0, ...)
FA.handshake(f, kindA, kindB, x, y, h, t, gap=0.6, t0=0.5, seedA=0, seedB=1);  FA.threat(f, t, x, y, h, dir=1, t0=0.4, dur=1.2, victim="kardinal", attacker="asker")
FA.atmo_birds(c, t, n, a, x0, x1, y0, y1, speed, night, seed, size);  FA.vine_band(f, y, alpha)                # atmosfer / asma bandı (önbellekli)
```
* **kind**: `tuccar, banker, rahip, kardinal, papa, kesis, soylu, soylu_f, asker, halk, cocuk, denizci`. Takma adlar: `katip→banker, muhafiz→asker, kadin→soylu_f, savonarola/monk→kesis, page→cocuk, noble→soylu,
  merchant→tuccar, priest→rahip, sailor→denizci …` (`FA.ALIAS`). Kostüm `crc32(kind, seed)` ile belirlenir (süreçler arası tekrarlanabilir); `**stil` ile ezilir:
  `robe, robe2, hat, hat_col, hair, skin, hose_l, hose_r, pat, beard, cloak, build, sleeves, nose, body, hem, head, barefoot`.
* **action**: `idle talk bow kneel point cheer pray write count handshake threat work` — `bow(t0,dur,depth)`, `kneel(t0,rise_at,pray)`, `point(t0,dur,target=(dx,dy))`, `cheer(amount,hop)`,
  `talk(energy)`, `write`/`count` (masa + defter/florin yığını), **`work(mode="lay"|"strike"|"haul", period, high)`** (yeni: mala ile duvara tuğla/harç, çekiçle keski vuruşu, halat çekme + geriye yaslanma).
  Tek seferlik eylemler için çağırırken `t % periyot` verin (döngü).
* **prop**: `staff crosier spear halberd pole(+flag=(cihaz,w,h,c1,c2)) book cross torch sack basket dagger quill hammer trowel coin` (eller aksesuarı taşır; sancak rüzgârda dalgalanır).
* **crowd mode**: `mill` (dolaşan/konuşan) · `stand` · `kneel` (`rise_at` ile dalga halinde kalkar) · `cheer` (kollar havada, `wave` dalgası) · `march` · `run` (kaçış). Üyeler faz kaydırmalı, `crowd_members` bellekli.
* **şiddet SİNYALİ** yalnız siluet/jest: `FA.threat(...)` (hançer kalkışı silueti, pigment yıkama rengi `rim`); kan/yara yok.

### 1.2 `pano` — uzun plan panoraması
```python
shot("pano", "c1s9", pano="florence", tod="day")                                    # tod: day | dusk | night; yol çekim süresine yayılır (ease_io)
shot("pano", "c1s9", pano="florence", tod="dusk", kick="FLORANSA, 1420", caption="Arno kıyısı",
     cams=[(("c1s2","şafak",0.0),(960,0,1.0)), (("c1s5","boyahane",0.0),(4450,0,1.0)), (("c1s8","banka",0.0),(5620,60,1.38)), (("c1s11","Duomo",0.0),(9300,-10,1.0))], longtake=True)
shot("pano", "c7s3", pano="nave", tod="night",
     stations=[dict(x=2300, at_frac=0.0, fn=cilt_pano.st_celebrant), dict(x=4700, at=("c7s4","çan",0.0), fn=cilt_pano.st_bell), dict(x=8100, at=("c7s6","kaç",0.0), fn=cilt_pano.st_flee)])
shot("pano", "c12s4", pano="corridor", cam=("push", 0.05))                            # Vasari Koridoru: pencerelerden akan nehir/şehir
```
Parametreler: `pano, tod, cams, stations, kick, caption, at, frame, seed, band`; `cam/link/longtake/montage` kabul edilir (cam'i Lab-A sarmalayıcısı uygular).
* `cams=[(çapa,(x,y,zoom)),…]`: x = ekran merkezinin ana düzlem x'i (başlangıç ≈ 960), y = dikey kayma (px, + aşağı), zoom ≥ 1; çapa = saniye | `("c7s5","sözcük",−0.1)`; PCHIP + uçlarda ease_io.
* `stations=[dict(x=…, at=çapa | at_frac=0..1, fn=callable(ctx, st))]`: o x'te canlanan sahne (`ctx.f, ctx.c, ctx.t, ctx.night`; `st["x"], st["_at"]`). `stations=[]` → yok. Varsayılanlar:
  florence: `st_dyers`(x1500) `st_market`(2950) `st_banker`(5600, gece masada mum) `st_duomo_walk`(8100) · nave: `st_celebrant`(2300) `st_bell`(4700) `st_flee`(8100) · corridor: —.
* Katmanlar: gök → uzak tepe → uzak şehir → orta bina/revak → nehir → ana düzlem → ön plan; ≥3 paralaks derinliği; ağır katmanlar 1024 px kareaş olarak tembel pişirilir ve `out/_cache/world/*.png`
  (sürüm eki `p1`) altında önbelleklenir; kamera zumunda sprite'lar `FA.set_scale_hint` ile keskin kalır.
* Dünyalar: **florence** (13400 px ≈ 7 ekran: Arno kıyısı, Ponte Vecchio, kıyıya asılı rüzgârlı boya bezleri, tezgâhlar, revak altında yazan bankacı, Duomo'ya yürüyüş; gün/alacakaranlık/gece),
  **nave** (11200 px: sütun sırası, tonoz, pencere ışık huzmesi, diz çöken/ayakta kalabalık, çan sarkacı, kaçan figürler), **corridor** (11600 px: Arno üstünde Vasari Koridoru, pencerelerden akan nehir/şehir, portreler).

### 1.3 `build` — zaman atlamalı yapım
```python
shot("build", "c4s7", build="dome", p=(("c4s2","kubbe",0.0), ("c4s7","tamam",0.0)), orbit=10, kick="KUBBE KENDİNİ KURAR", caption="1420–1436")
shot("build", "c12s2", build="uffizi", p=(0.0, 11.0), tod="day")      # p tek sayı → sabit ilerleme (kamera yine zamanla ilerler)
```
Parametreler: `build ("dome"|"uffizi"), p=(çapa_a, çapa_b) | sayı | None (tüm çekim), orbit (°, ≤12), tod, kick, caption, at, seed, frame`. İlerleme p∈[0,1] = `ease_io` (çapa saniye ya da `("c4s2","sözcük",0.0)`).
* **dome**: katedral gövdesi (çok renkli mermer) + kiremit çatı halkası + tambur (yeşil bantlar, gözler) → sivri sekizgen kabuk **sıra sıra** (44 sıra; her sırada tuğlalar rastgele sırayla yerleşir; balık kılçığı zikzak,
  tek-çift sıra tonu), beyaz mermer nervürler, asma platform halkaları + dikmeler + korkuluk halatı, **çarklı vinç** (çarkın içinde yürüyen adam yük çıkarken ileri/inerken geri, halatta sallanan yük), platformda mala/çekiç/halat
  çeken/işaret eden işçiler, tuğla taşıyıcılar (mekik yürüyüş), tuğla yığınları; p>0.78 fener yükselir (kemerli pencereler, konik çatı, küre+haç), p>0.86 iskele söker, p>0.88 kamera geri çekilir (zum-out + alçalma).
  Kamera üst kenarı izler (`crane up`) + yavaş yörünge (`orbit`). Güneş yayı + gökyüzü (şafak→öğle→gün batımı) + yüz parlaklığı + sıcak örtü ilerler; kireç ocağı + bacalardan duman, kuşlar, bulutlar (hızlı akar). `tod="night"`: yıldız/ay, meşaleler.
* **uffizi**: tek noktalı perspektifte (f 560→640, ufuk, kamera Z −13→+7.5 ve yükseklik 1,9→8,6 m) iki kanat; temel hendeği → portico (kemerler) → ara kat → piano nobile (çerçeve, alınlık, denizlik, kayıt çıtası) → çatı katı; ham taş
  duvar (sıra çizgileri) → sıva + pietra serena (sıva 3,6 m geriden izler), silme gölgeleri; iskele (dikmeler, 4 m tablalar, yükselen üst tabla) ve kat kat işçiler (mala/çekiç/konuşma/işaret; alfa ile belirir), avluyu enine geçen taşıyıcılar
  (çuval/sepet), taş yığınları, kireç çukuru, kereste, araba izleri, **çarklı vinç** (direk duvarla birlikte uzar), toz, yan sokak evleri (iki sıra, pencere/kapı/bacalardan duman), Arno revağı + karşı kıyı.

### 1.4 `procession` — Gozzoli "Magi" frizi (mevcut `frieze` dokunulmadı)
```python
shot("procession", "c5s3", dir="r", density=1.2, mix=dict(rider=0.35, noble=0.2, page=0.15, banner=0.12, guard=0.08, elder=0.05, cleric=0.03, common=0.02), pan=("r", 900), speed=125.0, seed=2)
shot("procession", "c1s14", dir="l", density=1.6, seed=4, kick="CIOMPI")                       # sağdan sola kabaran alay
```
Parametreler: `seed, dir ("r"|"l"), density, mix, speed (px/sn), pan (None | px/sn | "r"/"l" | ("r", toplam_px)), x0, ease=(giriş,çıkış), tod, rows, birds, dust, kick, caption, at`.
Üç sıra (arka→ön, kendi zemin hızıyla paralaks), her sıra kendi karışımı: sancak taşıyıcılar (dalgalanan sancak), atlılar (yürüyüş/tırıs, brokar kapariş), sayfalar (çocuk), ağır cüppeli yaşlılar/ruhban, muhafızlar; çiçekli çayır,
selvi/portakal/şato/tepe paralaksı, toz, kuşlar. Yürüyüş hızı zemine göre senkron (ayak kaymaz).

### 1.5 `preview_world.py`
`python3 preview_world.py [ad…] [--no-clip] [--no-sheet] [--ms] [--bake] [--workers 2] [--scale 0.5]` · girdiler: `kit_walk kit_acts kit_riders kit_crowd procession procession_l pano_florence pano_florence_night
pano_nave pano_corridor build_dome build_uffizi build_dome_night`. Sayfa = 6 kare (zamana yayılmış, `CM.post` dâhil, etiketli); klip = 24 fps, 8–12 sn, 960×540, ffmpeg (yoksa cv2). İşçi ≤2.

## 2. Ölçümler (bu makine, 4 çekirdek Lab-A ile paylaşımlı; yük ortalaması 2–4)
| ölçüt | değer |
|---|---|
| pano bake (soğuk önbellek, tüm kareaşlar) | florence gün 1,2 s (45 kareaş) · gece 1,3 s · nave 1,4 s (32) · corridor 1,7 s (43) — yüklüyken ≤3 s; hepsi ≪15 s. Disk önbelleği `out/_cache/world` ≈ 7 MB (165 dosya); ikinci çalıştırmada yalnız okuma |
| ilk kare (soğuk: kit pişirme + kareaş okuma) | 0,3–0,7 s (procession 2,7 s: 3 sıra × kostüm kitleri) |
| sıralı render, çekim yalnız (ort) | pano florence 75 ms · gece 83 · nave 92 · corridor 64 · dome 53 · uffizi 76 · procession 91 (yoğun 1,5×: 122) · kit_crowd (58 kişi) 133 · kit_acts 95 · kit_walk 72 · kit_riders 75 |
| + RGB okuma + `CM.post` | ≈ +42–47 ms (florence gündüz ≈ +33) → **toplam 100–175 ms/kare**, hepsi ≤250 ms hedefinin altında (nave ≈ 137, kit_crowd ≈ 175 en ağır) |
| figür maliyeti (h≈280) | walker ≈ 1,8–2,8 ms · atlı ≈ 4,4 ms · kit pişirme 7–14 ms/kostüm (ısınma toplam ≈ 7–10 s, süreç başına bir kez) |
| klipler | 13 klip, 8–12 sn, 0,3–2,4 MB, hareket enerjisi (ort. ardışık kare farkı) 0,5–13; ölü (kopya) kare yalnız build çekimlerinin son ≈1 sn tutuşunda (p tamamlanınca) — orada duman/kuş/bulut/taşıyıcı akar |
Teknik not: bu CPU'da `kPlus` karışımı + renk filtresi ≈6× yavaş (sunum parıltısı 28–31 ms), önceden renklendirilmiş sprite + srcover ≈ 2,6–5 ms → `cilt_pano.glow` bunu kullanır; çarpma örtüsü (`kMultiply`) yerine düşük alfalı örtü kullanıldı.

## 3. İyi olanlar
* Figürler kare çevirmeyle değil iskeletle akar: IK ayaklar (adım evresi sabit zemin hızıyla), kalça yüksekliği, kol-bacak ters salınımı, gövde eğimi, nefes, kumaş şeritleri; atın bacakları IK (toynak kaymaz); kalabalık faz kaydırmalı dalga.
* Dünya kamerası gerçek paralaks (≥3 derinlik) + kareaş önbelleği; aynı kod gündüz/akşam/gece; istasyonlar (bankacı masası, boyahane, çan, kaçış) çekim süresine çapayla oturur.
* Zaman atlamalı yapımlar gerçekten "kendini kurar": kubbe sıra sıra, avlu kat kat; ışık/gökyüzü/gölge akar; vinç/çark/işçi/duman hep hareket halinde; kamera olayı izler (crane-up/yörünge/dolly) ve sonda geri çekilir.
* Tüm şiddet gösterimi siluet/jest; renk dili Lab-A'nın fresk bandı ile uyumlu (asma bandı, altın şerit, `TH` renkleri, `CM.bgfill/finish`).

## 4. Çirkin / eksik kalanlar, bilinen kusurlar
1. Figürler yandan kesme-bebek: dönüş yalnız yatay çevirme; yüz ayrıntısı asgari; eller basit; diz çökmede arka ayakkabı biraz yassı; `haul` halatı süs (uçta makara yok).
2. Kalabalıkta tipler jenerik; `crowd` içinde "kaçış" ve "diz çökme" geçişleri mod değiştirirken zıplar (mod başına ayrı çağrı; yumuşak geçiş yok).
3. `pano`: istasyon `fn`'leri Python çağrılabilir (JSON olamaz); nave/corridor yalnız tanımlı varsayılan yollarla test edildi; corridor'da Pitti ucu (yol sonu) kaba; gündüz/gece dışı "veba solması" (renk→gri) parametresi yok.
4. `build=dome`: yüzler düz gölgeli (kendi gölgesi yok); iskele şematik (asma halkalar); balık kılçığı yalnız yakında seçilir; işçiler 58 px (geniş planda küçük); `orbit` ≤12° (görsel ≈±6°). Gece: meşaleli ama pencereli ev ışıkları sabit.
5. `build=uffizi`: iskele tablaları alttan bakınca ağır kahverengi şeritler; yakın bay pencereleri büyük koyu kutular (çerçeve + kayıt çıtası var, kanat/panjur yok); heykel nişleri yok; iskeledeki işçiler kat yüksekliğine ulaşınca alfa ile belirir; p tutuşunda (son sn) hareket yalnız küçük ayrıntılar.
6. `procession`: gece yalnız ton (özel meşale alayı yok); `pan` uçlarda yumuşak durma yok (isteğe bağlı `ease`). `frieze` ile aynı sahnede iki farklı peyzaj dili.
7. İlk karede kit/kareaş pişirme 0,3–0,7 s (kabul: çekim başına bir kez); farklı `seed` ve boyda her yeni kostüm 7–14 ms.
8. Ortam: skia `Fontconfig warning … reset-dirs` satırları (sistem), bizden değil.

## 5. Yönetmen sekanslarına (§8 c0–c16) uyum
| # | bu kitin karşıladığı | eksik |
|---|---|---|
| c0 / c16 | `actor(write)` yazan bankacı, mum ışığı (`st_banker` gece), kalabalık tipleri | oda + belge zoomthru + gün-geri-yön kamera yolu: sahne yazarı/Lab-A (`pano` kullanılırsa `cams` ters sırayla verilir) |
| c1 | şafakta Floransa panoraması soldan sağa (`pano florence`), Arno'da asılı boya bezleri rüzgârda, `procession dir="l"` (Ciompi alayı sağdan sola kabarır), çan (nave'de) | veba: renk/gün→gri solması (parametre yok), florin→`iris` geçişi (Lab-A) |
| c2 / c9 / c14 / c15 | — (defter/harita/grafik sekansları; kit yalnız `count`/`write` figürleri sağlar) | tamamı bu işin dışında |
| c3 | 1434 dönüş alayı (`procession`), `crane up` yerine `build dome` kamerası | Palazzo Vecchio kulesine tek dikey plan (dikey pano yok); boş koltuk/gölge; ağ (`network`) |
| c4 | **tam**: `build dome` — kubbe sıra sıra (balık kılçığı), `crane up` + `orbit`, vinç/işçi/duman | "kefaret/yatırım terazisi" (Lab-A nesnesi) |
| c5 | **tam**: `procession` (Gozzoli friz, kesintisiz `pan r`, sancak/atlı/sayfa karışımı) | elyazması yığını, Ficino mum ışığı, harita+gemi |
| c6 | atlı/sancak/kalabalık dalgası parçaları (`rider gallop`, `crowd cheer`, sancaklı `procession`) | **giostra çekimi** (mızrak koşusu iki atlı + bariyer + seyirci) hazır değil (~100 satır: iki `rider` + `prop="spear"` + `crowd`) |
| c7 | **büyük kısım**: nave tek uzun plan (sütun sırası, ışık huzmesi, diz çöken/ayakta kalabalık, çan sarkacı, kaçan figürler `st_flee`), `FA.threat` hançer siluet jesti, "Palle! Palle!" için `crowd(mode="cheer", wave)` + hareketli sancak (`procession`/`prop pole`), gece skyline (`pano florence tod=night`) | tunç kapıların kapanışı (`whip`, Lab-A), pigment yıkama kızıllaşması (Lab-A fx) |
| c8 | masa başı iki figür (`actor talk/handshake`), saray figürleri | rota haritası + gemi diorama; Otranto alevleri |
| c10 | San Marco kürsüsü için `kesis` + `crowd(stand/kneel)`, Charles ordusu `procession dir="l"` (asker ağırlıklı `mix`), eşya taşıyan figürler (`prop sack/basket`) | çan titreşim dalgası, saray yağması sahnesi, ateş ışığında yavaş pull |
| c11 | Roma alayı sol→sağ (`procession dir="r"`), dar koridor kayan plan için `pano corridor` yeniden kullanılabilir (dış katmanlar değişmeli) | 1527 duman `dip`, kuşatma surları/istihkâm maketi |
| c12 | **büyük kısım**: `build uffizi` (kubbe gibi kendini kurar) + **Vasari Koridoru'nda kesintisiz kayma** (`pano corridor`, Arno üstünde, pencerelerden nehir/şehir) | Santo Stefano kadırgaları / Lepanto (gemi kiti yok) |
| c13 | Marsilya düğün alayı (`procession`) | MİT/GERÇEK damgaları, Rubens panoları (Lab-A) |
