# İç mekân dünyası — Lab-D notları (`cilt_oda.py`, `preview_oda.py`)

Sözleşme: `YONETMENLIK_REHBERI.md` §1, §2, §5, §8 · `STIL_REHBERI.md` §7. Mimari `cilt_pano` ile aynıdır (katmanlı uzun plan + kareaş önbelleği), ama kamera bir ODA içinde dolaşır; ağır statik katmanlar
tembel pişer (`out/_cache/world/oda_*.png`, sürüm eki `o3`), alev/ışık/toz/perde/kapı/figür kare başına vektör çizilir (zumda keskin kalır).
Bu iş yalnız `cilt_oda.py`, `preview_oda.py`, `notlar_oda.md`, `out/frames/oda_*`, `out/clips/oda_*` dosyalarına dokunur; `cilt_kinds4.py` sonundaki korumalı `import cilt_oda` yeterlidir.

| # | ön ayar | durum |
|---|---|---|
| 1 | `room="oda1743"` | HAZIR — gece/gün, `path="in"`/`"out"` (ters yol), oturan/yatan kadın SİLÜETİ, belgeye zum (doc kâğıdıyla aynı doku), mum/güve/toz/perde |
| 2 | `room="salon"` `variant="medici"\|"napoli"\|"signoria"\|"pitti"\|"taht"` | HAZIR — masa başı iki oturan figür (konuşan/dinleyen sırayla), avize, harita masada; `taht` = boş taht odası |
| 3 | `room="banka"` | HAZIR — dört masa istasyonu (yazan/sayan bankacı + müşteri), florin ışıltısı, terazi; ŞUBE KAPANIŞI `close_at` |
| 4 | `room="calisma"` `variant="hucre"\|"kutuphane"\|"studiolo"` | HAZIR — San Marco hücresi (yağ kandili, kukuletalı siluet), kütüphane (boş raf yuvası `empty_frac`), studiolo (dört bölge + `zone_at` turu) |
| 5 | `room="sakristi"` | HAZIR — tunç kapı (iki kanat, kabartma), KAPANMA animasyonu + kamera sarsıntısı + ışık sızıntısı, içeride siluetler, uzun gölge |
| 6 | `room="bos"` `variant="blois"\|"koln"` | HAZIR — Blois gece odası (siluet kapıdan/pencereden çıkar), Köln soğuk boş oda (ışık solar), `thread_at` iplik kopar |
| 7 | `room="perde"` | HAZIR — Pitti sahnesi, perde açılır, Orfeo/Euridice siluetleri, ayak ışığı, loca/izleyici siluetleri |
| 8 | yeniden kullanılabilir işlevler | HAZIR — aşağıda §3 |

## 0. Komutlar (proje dizininden; `python3`, `-I` yok)

```
python3 preview_oda.py --list                      # girdi adları
python3 preview_oda.py oda1743_gece_in salon_napoli # kontak sayfası out/frames/oda_<ad>.png + klip out/clips/oda_<ad>.mp4 (ölçek 0,5; işçi 1)
python3 preview_oda.py --no-clip | --no-sheet      # yalnız sayfa / yalnız klip
python3 preview_oda.py --frame sakristi_gun 7.5 [--full]   # tek kare out/frames/oda_<ad>_t<sn>.png
python3 preview_oda.py --ms [ad…]                  # ms/kare (çekim + RGB + CM.post), çekirdek süresi
python3 preview_oda.py --bake                      # kareaş pişirme süreleri (oda önbelleğini siler!)
```
Önbelleği elle sıfırlamak: `rm out/_cache/world/oda_*` (çizim kodu değişince `OVER` sürümünü de artır). Önizleme çekimi `SH.shot("oda", 0.0, **params)`; çalıştırma tek işçi, kare kare ffmpeg'e yazar (bellek küçük).

## 1. API

```python
shot("oda", a, room="oda1743", variant=None, tod=None, path=None, cams=None, actors=None, props=None, kick=None, caption=None, at=0.0, frame="auto", seed=1, **oda_parametreleri,
     mode="day|night", cam=None, link=…, tr=…, longtake=…, montage=…)
```
* `room`: `oda1743 | salon | banka | calisma | sakristi | bos | perde` (takma ad `oda`=oda1743). `variant`: oda içi ayrıntı (aşağıdaki tablo).
* `tod`: `day | dusk | night`; verilmezse `mode`'a göre (night→night). Gece: karanlığı `CM.relight` mum havuzu getirir (havuz mumu izler; mum ekran dışındaysa havuz genişler ve ortaya kayar); gündüz: pencere huzmeleri + gün ışığı örtüsü. `dusk` = sıcak renk uyarlaması.
* **Kamera**: `path="…"` odanın adlı yolu (`"default"`, `"in"`, `"out"` = `in`'in TERS sırası — c16!, ayrıca odaya özgü yollar) ya da `cams=[(çapa,(x,y,zoom)),…]` (x = ekran merkezinin ODA x'i ≈ 960..PW−960, y = dikey kayma px, zoom ≥ 1; çapa: sn | `("c0s5","belge",−0.1)`; PCHIP + uçlarda ease). `cam=` (Lab-A): `("rack", (xa,ya), (xb,yb), dict(at=…, dur=…, r=…))` aynen çalışır (son-kare odak bulanıklığı, ≈+50–90 ms); `path/cams` verilmemişse `cam=("push"|"pull"|"pan"|"crane"|"orbit"|"hand"…)` odanın `default` yoluna EKRAN UZAYI ofseti olarak biner. Kamera ucu çekim sınırında durur (cam_in/cam_out devri yok; geçişte hareket yeniden başlar).
* **Çerçeve bandı** (`frame="auto"`, varsayılan): zum 1,55'i geçince asma bantlı fresk bandı tam ekrana açılır (belgeye/kapıya girerken); `frame=True` sabit bant, `False` bantsız (y 140–940).
* `actors=[dict(kind, x, y, h, action, at, dir, seed, sil, seated, walk, prop, layer, …)]`: x,y = ANA düzlem ayağı (oda koordinatı). `kind` = FA tipleri (`tuccar banker rahip kardinal papa kesis soylu soylu_f asker halk cocuk denizci`); `action` = FA eylemleri (`idle talk bow kneel point cheer pray write count handshake threat work`) ya da `seated=True` ile oturan eylemler (`talk listen read write count`; masa/sandalye odanın kendi çizimidir); `at` = tek seferlik eylemin çapası (`t0`); `sil=True|"#renk"` → SİLUET (düz koyu + ışığa dönük sıcak kenar ışığı, YÜZ YOK); `walk=(x_son, hız)` + `walk_at=çapa` yürür; `fade_x=(x_a,x_b)` yürürken kapıdan geçerken solar, `fade_out_at/_dur` yerinde solar; `layer`: `"behind"` (masa tablasının arkası) | `"back"` (varsayılan; masa tablası ile ön panel arası) | `"front"` (masa/tezgâh önü). **`actors` verilmezse odanın varsayılan figürleri çizilir; liste (boş `[]` dâhil) verilirse yalnız o.** `props=[dict(kind="candle|oil|inkwell|quill|doc|coins|book|scroll|goblet|flask", x, y, …)]` eklemelidir.
* `kick`, `caption`: `pano` ile aynı yerleşim (bant dışına/tam ekranda solar). Altyazı bölgesine yazı koymaz.

### 1.1 Odaya özgü parametreler ve yollar
| oda | parametreler | `path` |
|---|---|---|
| `oda1743` | `figure="seated"` (masada oturan KADIN SİLÜETİ belge yazar: 31 Ekim 1737 imza masası; varsayılan) \| `"lying"` (yatakta yatan siluet, nefes: 18 Şubat 1743) \| `"both"` \| `None`; `doc_lines` (13), `doc_shown`, `doc_seed`, `seal_at` (mühür basılışı), `candle_lit`, `snuff_at` (mum söner), `candle_day` | `default in out sweep_r sweep_l bed table doc` |
| `salon` | `variant`: `medici` (palle frizi, goblen) · `napoli` (serin; Lorenzo–Ferrante: iki SİLUET masa başı) · `signoria` (kızıl-beyaz sancaklar) · `pitti` (aynalar) · `taht` (boş taht + baldaken + toz); `sil`, `speaker="alt"\|"a"\|"b"` (kim konuşuyor), `map_route` (0..1) ya da `map_at` (masadaki haritada rota çizilir), `chandelier_day`, `candle_day` | `default in sweep_r sweep_l table heads pull taht taht_in` |
| `banka` | `close_at`, `close_dur` (7 sn): kandiller tek tek söner (duman), defterler kapanır (sayfa çevrilir), ışık havuzu son kandile çekilir, sonunda karanlık; `customers` (True) | `default sweep_r sweep_l corner count close in` |
| `calisma` `hucre` | `figure="desk"` (kukuletalı siluet yazar) \| `"kneel"` (diz çökmüş siluet) \| `None`; `lamp_lit`, `snuff_at`, `lamp_day`; yağ kandili alevi büyük ve kararlı (c10 alev→alev) | `default in lamp sweep_r pull` |
| `calisma` `kutuphane` | `figure="desk"\|None`, `sil`, `empty_frac` (0..1: BOŞ RAF YUVALARI, c10 V1) | `default sweep_r sweep_l scribe in` |
| `calisma` `studiolo` | `zone_at=[a,b,c,d]` (dört bölgeye kamera + ışık turu; `zone_zoom`), `secret_at` (saklanma yeri kapısı açılır), `figure="desk"`; **bölgeler**: `Calisma.ZONES["studiolo"]` = `[(x0,y0,x1,y1)]` (oda koordinatı; ofis · laboratuvar · saklanma yeri · merak kabini); `zone_centers()` | `default tour sweep_r wide` |
| `sakristi` | `open0` (0,9), `open`, `close_at` + `close_dur` (1,7 sn): kanatlar kapanır, nef ışığı daralıp söner, sonunda kamera sarsılır; `shadow_at` (kapıdan uzun gölge); `door="bronze"\|"wood"` | `default close push sweep_r pull` (`close`: kamera kapıya girer; z≈7,4'te kanat ekranı doldurur) |
| `bos` `blois` | `exit="door"\|"window"`, `exit_at` (kapıdan geçiş/pencerede solma anı çapası), `exit_dur`, `figure=False` (figürsüz), `candle_lit`, `snuff_at` | `default window exit sweep_r pull` |
| `bos` `koln` | `fade_at`, `fade_dur` (9 sn): pencere ışığı SOLAR, oda kararır (gri-lapis) | `default in pull sweep_r` |
| `bos` (ikisi) | **`thread_at`** (çapa): odanın ortasından geçen ince iplik/çizgi o anda KOPAR, iki yarı çapalarından serbest kalır ve uçları aşağı süzülür/salınır; `thread=True` (yalnız gergin çizgi), `thread_from=(x,y)`, `thread_to=(x,y)` | — |
| `perde` | `open_at`, `open_dur` (3,2 sn): perde açılır; `open` (sabit 0..1), `stage=False` (boş sahne) | `default in stage sweep_r pull` |

### 1.2 Örnek `shot(...)` satırları
```python
# c0 açılışı: gece, mumlu oda → masaya yaklaş → belgenin içine (Lab-A zoomthru belge çekimine bağlar; belge ekran ortasında ≈ (960,520))
shot("oda", ("c0s1", -0.2), room="oda1743", path="in", figure="seated", mode="night", perde=1, link="scale", longtake=True, label="1743 odası")
shot("doc", ("c0s8", 0), tr=("zoomthru", 1.0, dict(at=(960, 520))), link="scale", title="", lines=[…], seal=True, mode="night", perde=1, cam=("push", 0.05), label="belge")
# c16: AYNI oda, kamera yolu TERS (belgeden odaya çıkar); yatan siluet
shot("oda", ("c16s2", 0), room="oda1743", path="out", figure="lying", mode="night", perde=3, link="scale", longtake=True, label="aynı oda, ters yön")
# c8: Napoli sarayı, masa başı iki siluet; "Konuk muydu, rehine mi?" cümlesinde odak kayması
shot("oda", ("c8s9", -0.3), room="salon", variant="napoli", path="table", mode="night", perde=2, cam=("rack", (330, 560), (1560, 560), dict(at=("c8s9", "rehine", -0.1), dur=1.6, r=420)), link="light", label="Napoli salonu")
# c9: şube kapanışı (kandiller tek tek söner)
shot("oda", ("c9s7", 0), room="banka", path="close", close_at=("c9s7", "kapandı", 0.0), close_dur=8.0, mode="night", perde=2, link="light", label="kapanan banka")
# c7: sakristi, tunç kapı kapanır (Lab-A whip/zoomthru ile kes)
shot("oda", ("c7s16", 0), room="sakristi", path="close", close_at=("c7s16", "kapı", 0.0), close_dur=1.8, shadow_at=("c7s16", 0.4), mode="day", perde=2, cam=None, link="carry", tr=("light", 0.9))
# c10: San Marco hücresi: yağ kandili alevi ekranda büyük (alev → alev eşleşmeli kesme)
shot("oda", ("c10s6", 0), room="calisma", variant="hucre", path="lamp", figure="desk", mode="night", perde=2, link="light", label="hücre")
# c15: studiolo'nun dört bölgesi (kamera + ışık turu); etiketler ZONES'a göre yerleştirilir
shot("oda", ("c15s4", 0), room="calisma", variant="studiolo", path="tour", zone_at=[("c15s4", "ofis", 0), ("c15s4", "laboratuvar", 0), ("c15s4", "saklanma", 0), ("c15s4", "merak", 0)], secret_at=("c15s4", "saklanma", 0), mode="night", perde=3)
# c13: Blois (iplik ucu serbest) ve Köln (ışık solar, iplik kopar)
shot("oda", a, room="bos", variant="blois", path="default", exit="window", exit_at=("c13s20", 0), thread_at=("c13s22", "iplik", 0), mode="night", perde=3)
shot("oda", a, room="bos", variant="koln", path="in", fade_at=("c13s30", 0), fade_dur=8.0, thread_at=("c13s31", 0), mode="day", perde=3, link="light")
# c15: 1737 boş taht odası (siluet)
shot("oda", a, room="salon", variant="taht", path="taht", mode="night", perde=3)
# c14: Pitti sahnesi
shot("oda", a, room="perde", path="in", open_at=("c14s9", 0), open_dur=3.2, mode="night", perde=3)
```

## 2. Yeniden kullanılabilir küçük işlevler (§8; ekran/tuval koordinatında; `f` = `sk.Frame`, `c` = tuval)
```python
candle(f, x, y, h, t, seed, lit=1.0, holder=True, …) -> (alev_x, alev_y, parlaklık)   # mum: taban (x,y), boy h; alev titrer/eğilir/esintiyle söner, ışıma, ince duman
oil_lamp(f, x, y, s, t, seed, lit, hang)             # yağ kandili (San Marco); hang>0 zincirle sarkar
window_light(f, x, y, w, h, t, dx=260, y_floor, col, a, seed, cross=True, patch=True, dust=18, drift=24, night=False, part="all|shaft|patch")  # pencere (x,y,w,h) → eğik huzme + toz + zemin lekesi (çıta gölgeli), yavaş kayar
table(f, x, y, w, depth=130, y_floor, cloth=(ana,şerit), T, front=True, top=True) -> TGeom   # ters perspektifli masa; g.pt(u,v) tabla üstü nokta
door_bronze(f, x, y, h, open_amount, w=None, seed, light=True) -> (sol_serbest_x, sağ_serbest_x, kapalılık)   # tunç kapı (iki kanat, kabartma; zumda keskin)
quill(c, x, y, ang, s), inkwell(c, x, y, s, t), doc_sheet(f, x, y, scale, t, n=13, shown, seed, seal=True)   # doc kâğıdı (paper_image 1100×760, aynı ton/kenar) + okunmaz satırlar + palle mührü
sil_actor(f, kind, x, y, h, t, action, dir, seed, color, rim, rim_dir, walker=None)        # siluet figür (baş/ayakkabı dâhil düz koyu; FA.blit yamasıyla)
seated(f, kind, x, y, h, t, action="write|count|talk|listen|read", sil=None, desk_top=False) -> ek bilgi   # oturan figür (masa/sandalye çağıranın)
chandelier, candelabra_table, candelabra_floor, balance_scale, map_sheet, sparkle, moth, draw_throne, draw_bed, draw_chest, draw_chair, draw_window, draw_tapestry, draw_alcove, draw_bookcase, door_leaf, fireplace, thread_line, draw_drape …
```
Not: `cilt_oda` `FA.blit`'i YAMAR (`_blit_cf`): `FA.draw_fig` baş ve ayakkabı sprite'larına renk filtresi uygulamadığı için siluetlerde yüz/ayakkabı görünüyordu; yama yalnız `_SILCF` doluyken (siluet çizerken) etkindir, diğer çağrıları değiştirmez.

## 3. Ölçümler (bu makine, paylaşımlı; çekim + RGB + `CM.post`, ms/kare ort / maks, 1 çekirdek; son ölçüm)
| girdi | ort | maks | | girdi | ort | maks |
|---|---:|---:|---|---|---:|---:|
| oda1743 gece `in` (belgeye zum) | 145 | 207 | | kütüphane gün / boş raf | 113 / 116 | 194 / 195 |
| oda1743 gece `out` / gün / yatak | 117 / 117 / 97 | 190 / 200 / 135 | | studiolo turu (ateş+alembik+armiller) | 162 | 249 |
| salon napoli (gece, 2 siluet, 2 avize) | 166 | 236 | | sakristi gün (kapı kapanışı) / gece | 158 / 112 | 195 / 120 |
| salon medici / signoria / pitti / taht | 141 / 124 / 138 / 110 | 165 / 159 / 219 / 155 | | blois kapı / pencere | 83 / 100 | 92 / 111 |
| banka gün / gece / kapanış | 125 / 124 / 121 | 238 / 149 / 195 | | köln (ışık solar + iplik) | 84 | 90 |
| hücre gece / diz çöken | 110 / 94 | 142 / 114 | | perde (Euridice) | 104 | 128 |
| salon napoli + `cam=rack` | 185 | 250 | | (rack bulanıklığı ≈ +45–90 ms) | | |
Hedef ≤250 ms/kare (çekim + post, 1 çekirdek): tüm girdilerde ortalama ≤185 ms; en yavaş tek kare 250 ms (rack'li napoli, studiolo turu). Kareaş pişirme (soğuk önbellek, oda başına): 1,0–2,3 sn (10–18 kareaş, ≈4 MB/oda); ilk kare (kit/sprite ısınması) 0,1–2,1 sn (süreç başına bir kez).
Klipler (`out/clips/oda_*.mp4`, 960×540, 24 fps, 6–14 sn, 0,2–1,2 MB): kare-farkı (240×135 gri, ardışık kare ort. mutlak fark) ortalaması 0,3–4,4 (gündüz salonlar/kütüphane/banka 2–4,4; gece odaları 1–2,5; Blois/Köln/Perde 0,3–0,7 = yavaş sahneler; sakristi kapı kapanışı maks 12 = sarsıntı). Özdeş (ölü) kare: yalnız tam karanlığa solan uçlarda birkaç kare; `qa_flow` için sahne yazarı `cam=`/`path` hareketini güçlendirmelidir (varsayılan yollar yumuşaktır).

## 4. İyi olanlar
* Her çekimde üç katman: kamera + ana eylem + ortam hayatı (mum/yağ alevi esintiyle titrer ve eğilir; güve alevin çevresinde döner; toz zerreleri huzmede süzülür; pencere huzmesi yavaş kayar; avize sarkaç gibi sallanır; perde/sancak rüzgârla dalgalanır; ocak ateşi/alembik/armiller; florin sayarken ışıltı).
* Belgeye zum: doc kâğıdı (`paper_image`) vektör olarak çizilir → z≈6'ya kadar keskin; çerçeve bandı otomatik açılır; mühür, satır satır "yazılan" okunmaz satırlar (13 madde). Tunç kapıya zum: kanat sprite'ı zum kademesine göre 1×/2×/4× pişer.
* Gece ışığı bilgi taşır: havuz mumu/kandili izler, mum ekran dışındayken genişler; banka kapanışında havuz son kandile çekilip söner.
* Siluet figürler (yüz çizilmez) kenar ışığıyla; şiddet/kan yok (sakristi: yalnız kapı + uzun gölge siluet).

## 5. Bilinen kusurlar
1. Figürler yandan kesme-bebek (Lab-B kiti); oturan figürün eli masa tablasına yaklaşık oturur (tablanın "ters perspektifi" nedeniyle kalem ucu belge satırına tam izlemez; yazılma ilerlemesi ayrı hesaplanır).
2. Statik mobilya/duvar kareaşları 1,0–1,4× pişer: zum ≥3'te yumuşar; zumda keskin olanlar yalnız dinamik nesneler (belge, masa tablası, mum, kapı, figür, kandil). Studiolo/hücre duvarı yakın planda yumuşaktır.
3. Tek ışık havuzu (`CM.relight`): çok kaynaklı sahnelerde (banka) ek kandil ışıması `after_finish` ile üstüne eklenir; havuz rengi her zaman sıcak-kahve merkezli (Köln'de bu yüzden özel bitiş: soğuk lapis örtü).
4. `studiolo` penceresizdir: mod gündüz olsa bile geçici gece havuzu kullanır (`always_lit`); renk derecelendirme çekim moduna göre kalır (`mode="night"` önerilir).
5. `cam_in/cam_out` devri yok: oda kamerası uçlarda durur (geçişte "hareket sürer" etkisi için `path` ucu hareketli seçilmeli ya da `cams` ucu uzatılmalı).
6. `sakristi`: nef/ışık arkası düzdür (derinlik yok); uzun gölge basit siluet; kapı kanadı dönüşü yatay daralma + serbest kenar kısalması (gerçek perspektif yok).
7. `perde`: hall duvarı/localar çok koyu (yalnız ayak ışığı aydınlatır); sahne figürleri 2 siluet, lir yok.
8. Seyirci/müşteri kalabalığı yalnız Banka'da (4 müşteri) ve Perde'de (siluet sıralar); kalabalık için `FA.crowd` `actors` dışında kullanılmadı.
9. Ortam: skia `Fontconfig warning` satırları sistemden.

## 6. c0–c16 uyum tablosu (brif §7 "Ekran önerileri / AKIŞ NOTU")
| # | bölümün odadan beklediği | karşılayan | eksik / not |
|---|---|---|---|
| c0 | mumlu oda, belgeye giriş (zoomthru), tüy kalem, mühür; geri dönüş c16 | **tam**: `oda1743 path="in"` (gece), `figure="seated"` (imza), belge ekran ortasında z≈5,9; `tr=("zoomthru",…,at=(960,520))` | "bugünün kuyruğu" Lab-E; `sayfa` Lab-A |
| c1 | banka köşesi (Giovanni), florin | **tam**: `banka path="corner"` (gün), yazan/sayan bankacı, florin ışıltısı | Orsanmichele köşesi/sokak Lab-E |
| c2 | defter dünyadır; çifte kayıt | `banka path="count"\|"corner"` (yazan bankacı, defter satırı yazılır) | defter sayfası animasyonu `ledger` türü; Cossa mezarı yok |
| c3 | San Marco hücresi; Palazzo Medici içi; Careggi mektubu | `calisma hucre` (masa, kitap, yağ kandili), `salon medici` | Palazzo Vecchio kulesi/Albergettino Lab-E |
| c5 | elyazması kopyalama, Ficino mum ışığı, San Marco rafı 800→200 | `calisma kutuphane` (yazan rahip, mum, `empty_frac` ile raf boşalır) | raf boşalmasını zamanla animasyonlayan parametre yok (`empty_frac` sabit) |
| c7 | sakristi, tunç kapı kapanışı (`whip`), Lorenzo siluet, Nori gölgesi, Palazzo Vecchio içi (V9 kapı kilitlenir) | **tam**: `sakristi path="close"` (kapı kanadı ekranı doldurur, sarsıntı), siluet `walk`, `shadow_at`; V9: `salon signoria` + `sakristi door="wood"` | nef = `pano nave` (Lab-B); kapı kilit sesi miks |
| c8 | Napoli salonu masa başı iki figür siluet + `rack` | **tam**: `salon napoli` (iki oturan siluet, konuşan/dinleyen sırayla, harita + rota `map_route`), `cam=("rack",…)` | Signoria salonu V5 iskemleleri: `salon signoria` (sandalye sırtları; sayaç Lab-A) |
| c9 | defter kapanıyor; ışıklar tek tek söner | **tam**: `banka close_at` (kandiller söner + duman, defterler kapanır, havuz daralır) | harita ışıkları Lab-A `map` |
| c10 | San Marco hücresi (alev→alev), boş kitap rafı yuvası, Büyük Konsey salonu | **tam**: `hucre path="lamp"` (kandil alevi ekran ortasında büyük), `kutuphane empty_frac`, `salon signoria` | Careggi tek pencere ışığı: `bos blois` pencere ışığıyla yaklaşık |
| c11 | V8 "yalnız oda silueti/gölge, şiddet gösterilmez" | `bos blois` + `actors` (siluet) ya da `sakristi shadow_at`; Passetto: `pano corridor` | — |
| c13 | Blois (iplik ucu serbest), Köln (boş oda, solan ışık, kopan iplik), oda dioraması (V2) | **tam**: `bos blois` (tek pencere, siluet çıkar, `thread_at`), `bos koln` (soğuk ocak, ışık solar, iplik kopar); V2: `bos blois` + `actors` (Henri–Diane siluet, pencerede küçük siluet `h≈120`) | 24 çerçeve (Lab-A/frieze); Marsilya limanı Lab-C |
| c14 | Euridice perdesi açılır | **tam**: `perde` (perde açılır, Orfeo/Euridice siluet, ayak ışığı) | Galileo/piyano/Livorno yok |
| c15 | studiolo (dört etiket: ofis · laboratuvar · saklanma yeri · merak kabini), "boş taht odası" siluet | **tam**: `calisma studiolo` (`ZONES`, `zone_at` turu, gizli dolap kapısı açılır), `salon taht` | Gian Gastone yatağı/hastalığı GÖSTERİLMEZ (hiç çizilmedi) |
| c16 | c0'ın odası, kamera yolu TERS; 1737 imza masası ↔ 1743 oda | **tam**: `oda1743 path="out"`, `figure="seated"` (imza) / `"lying"` (1743) | 2013 mezar açımı, Uffizi kapısı Lab-E |
| c4, c6, c12 | — | (iç mekân beklenmiyor) | |

## 7. Ana ajandan istekler
1. `STIL_REHBERI.md` §5/§7 tür kataloğuna `oda` satırı (API için bu dosya §1).
2. (İsteğe bağlı) `cilt_anim.draw_fig` baş/ayakkabı `blit`'ine `cf` desteği eklenirse `cilt_oda._blit_cf` yaması gereksiz olur.
3. (İsteğe bağlı) `cilt_cam.OWN_CAMERA`'ya `"oda"` eklenmesi: şu an `cam=` yalnız ekran-uzayı ofseti ve `rack` için kullanılır; `path/cams` ile çakışmaz (path/cams varken `cam` geometrisi yok sayılır).
4. `cilt_kinds4.py` sonunda `cilt_oda` zaten yüklü; ek değişiklik gerekmiyor.
