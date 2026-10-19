# Deniz, liman ve gemi dünyası — Lab-C notları (19 Ekim 2026)

Sözleşme: `STIL_REHBERI.md` §2 (sahiplik), §7; `YONETMENLIK_REHBERI.md` §1 on emir, §2 kamera, §3 geçişler. Bu iş yalnız `cilt_deniz.py`, `preview_deniz.py`, `notlar_deniz.md`, `out/frames/deniz_*`, `out/clips/deniz_*` ve `out/_cache/world/deniz_*` dosyalarını oluşturur/düzenler; Lab-A/B/D/E dosyalarına **dokunmaz**, yalnız okur.
`cilt_kinds4.py` sonundaki korumalı import (`for _m in ("cilt_deniz", "cilt_oda", "cilt_sehir")`) `cilt_deniz`'i yükler (dokunulmadı). `python3 -c "import shots, compose"` hatasız.
Kayıtlı çekim türleri: **`deniz`** (scene="acik"|"rota"|"filo"|"kiyi"), **`deniz_rota`**, **`deniz_filo`**, **`deniz_kiyi`** (aynı işin ayrı adları: "aynı tür üst üste ≤2" kuralı için), **`liman`**. Beşi de `cilt_cam.OWN_CAMERA`'ya modül yüklenirken çalışma anında eklenir (pano/sehir gibi: kendi kamera yolu `cams=` ile; `cams` yoksa `cam=` ön ayarı `cilt_cam.state` ile çözülür, o da yoksa türün varsayılan sinematik yolu).

| dosya | ne |
|---|---|
| `cilt_deniz.py` | türler + dalga/gök/gemi/liman motoru + bağımsız işlevler |
| `preview_deniz.py` | kontak sayfaları `out/frames/deniz_<ad>.png`, klipler `out/clips/deniz_<ad>.mp4`, `--ms`, `--energy`, `--at`, `--bake` |
| `out/_cache/world/deniz_*_<sürüm>.png` | gökyüzü ve liman katmanı önbelleği; sürüm = `cilt_deniz.py` içerik özeti (kod değişince eski dosyalar otomatik silinir) |

## Komutlar (proje dizininden; `python3 -I` YOK; TEK işçi, ölçek 0,5, kare kare yazım)
```
python3 preview_deniz.py                           # tüm girdiler: sayfa + klip (sıralı, tek işlem)  [arka planda çalıştır]
python3 preview_deniz.py acik_kadirga --no-clip    # yalnız kontak sayfası (6 kare, CM.post dâhil)
python3 preview_deniz.py liman_marsilya_1533       # sayfa + klip
python3 preview_deniz.py --at liman_pera 9.0       # tam çözünürlüklü tek kare → out/frames/deniz_liman_pera_t9.png
python3 preview_deniz.py --ms [ad…]                # ms/kare (CM.post dâhil)
python3 preview_deniz.py --energy [ad…]            # klip hareket enerjisi + ölü (kopya) pencere sayısı
python3 preview_deniz.py --bake                    # soğuk önbellek pişirme süreleri
```
Girdiler: `acik_kadirga, acik_nao_gece, acik_nao_alacakaranlik, acik_ufuk_yaklasan, rota_pisa_napoli, filo_inebahti, filo_yogun, kiyi_otranto, liman_marsilya_1533, liman_marsilya_1600, liman_napoli_yedi, liman_pera, liman_napoli, liman_livorno_elci, liman_generic`.

## 1. API — `shot(…)` satırları

Ortak parametreler (tüm deniz türleri): `tod` (`day|dusk|night|fire`; yoksa moda göre day/night), `cams=[(çapa,(x,y,zoom)),…]` (pano ile aynı: x ≈ 960 nötr, y + aşağı, zoom ≥ 1), ya da `cam=` ön ayarı, `wind` (şiddet), `wind_dir` (−1 sola | +1 sağa: bayrak/yelken/bulut/dalga yönü; öntanım −1: soldan sağa giden gemide flamalar KIÇA doğru uçar), `swell`, `foam`, `horizon` (ufuk y, bant yerel), `sun=(x,y,r)|False`, `glitter`, `birds`, `clouds`, `coast=[dict(x, kind, w, h, f, y, seed)]` (uzak kara), `kick`, `caption`, `labels=[dict(name, at_xy, f, dx, dy, t)]` (yalnız parametreyle gelen ad levhaları), `at`, `frame`, `seed`, `ships=[…]`.

`ships=[dict(kind, x0, x1 | dir+speed, y, scale, flag, t0, t1, ease, sails, oars, crew, highlight, arms, route, hz, seed)]`
* `kind`: `kadirga` (galera) · `nao` / `karrak` (üç direkli) · `tekne` · `kayik`. `y` = su hattı (bant yerel; perspektif: boy ve paralaks `persp(y)` ile ölçeklenir; `scale=1` @ y=640 → kadırga gövdesi ≈600 px). `x0/x1/dir+speed`: ekran pikseli (kamera nötr). `t0/t1` çapa olabilir. `ease`: `lin|io|out|in`. `flag`: `hristiyan | osmanli | toskana | papalik | fransa | venedik | genel` ya da sözlük (`LIVERY`). `highlight=True`: altın flama + parıltı (Toskana vurgusu). `oars`: `True` (çeker) | `False` (çizilmez) | 0..1 (kısmen/tam kaldırılmış) | `callable(t)`. `sails`: `True|False|"reduced"`. `sail_set`: `callable(t)` (kare yelken toplanma 0..1). `route=[(x,y),…]`: Catmull-Rom yol (gemi yola göre döner, kuyruk köpüğü). `arms="medici|cross|lily|crescent"`: nao kalkanı.
* Tasarım: kadırgada **senkron kürek çekişi** (24 kürek; çekiş–çıkış–geri–giriş evresi, su girişinde ripple halkaları), tente, kıç feneri, 2 flama + kıç sancağı, mürettebat (`FA.actor`: komutan işaret eder, denizciler `work haul`, askerler mızraklı), kaldırılabilir antena yelkeni (şişen latin mesh). Naoda 3 direk, kare yelkenler (şişme + kıvrım dalgası, `set_` ile toplanma), latin mizana, 4 bayrak/sancak, kofalar, babalar. Gemi **dalgayı sürer** (sallanma + eğim), su eteği/köpük çizgisi, kıç izi, baş dalgası, yansıma.

```python
# 1) acik — açık deniz (c3 "Venedik'e gemi", c12 Santo Stefano kadırgaları, c14 Fahreddin'in üç gemisi)
shot("deniz", ("c3s14", 0), scene="acik", tod="day", cam=("pan", "r", 180), link="dir", label="Venedik'e gemi",
     ships=[dict(kind="kadirga", flag="toskana", x0=300, x1=1500, y=650, scale=1.0, t0=0.0, t1=("c3s15", 0), highlight=True),
            dict(kind="nao", flag="venedik", x0=1750, x1=1250, y=500, scale=0.8, t0=0.0, t1=("c3s15", 0))])
shot("deniz", a, scene="acik", tod="night", wind_dir=1, ships=[dict(kind="nao", x0=1650, x1=380, y=600, flag="venedik", arms="cross")])   # gece
# 2) rota — A → B (c5 Lascaris, c8 Pisa→Napoli, c13 V7 Livorno→Marsilya); kamera gemiyi izler; thread=True: kat edilen yol boyunca yaldız kesik "iplik" (c13 iplik)
shot("deniz_rota", ("c8s11", 0), ship_kind="kadirga", flag="toskana", scale=0.9, thread=True,
     route=[(240, 664), (900, 620), (1700, 590), (2500, 560), (3200, 600)],
     labels=[dict(name="PİSA", at_xy=(300, 300), f=0.40, t=("c8s11", 0), dy=-90), dict(name="NAPOLİ", at_xy=(3500, 300), f=0.40, t=("c8s12", 0), dy=-90)])
# 3) filo — iki filo karşılıklı yaklaşır (c12 Lepanto: "12 / ≈200"); n = cephe başına kadırga; highlight = soldaki filoda altın flamalı Toskana gemisi
shot("deniz_filo", ("c12s32", -0.2), n=24, highlight=12, gap=(1700, 420), horizon=292, smoke_at=("c12s33", 0), smoke_dur=3.5, dim=0.5, link="dir")
shot("deniz_filo", a, n=90, highlight=12, gap=(1700, 520), horizon=292)             # yoğun hat (≈180 kadırga; küçük gemiler sprite sayfasından)
# 4) kiyi — Otranto: tepede kale-kent, stilize alev + duman, turuncu→altın ışık (insan/kan/ceset yok); donanma silüet olarak yaklaşır
shot("deniz_kiyi", ("c8s27", 0), n=16, fire_at=("c8s27", 0.5), link="light", cams=[(0, (1050, 20, 1.0)), (1, (940, -8, 1.2))])
# 5) liman — variant = marsilya | pera | napoli | livorno | generic; year → damga/kıyafet/ışık
shot("liman", ("c13s1", 0), variant="marsilya", year=1533, thread=True, t_dock=("c13s3", 0), link="scale", label="Marsilya 1533")
shot("liman", ("c13s40", 0), variant="marsilya", year=1600, t_dock=("c13s41", 0), link="shape", label="Marsilya 1600 (AYNI kadraj)")
shot("liman", ("c8s17", 0), variant="pera", year=1479, link="dir", label="Pera: Antonio'nun gemisi sağdan sola")          # öntanım mode="depart", dir=-1
shot("liman", ("c12s14", 0), variant="napoli", year=1539, ship=dict(mode="depart", dir=-1, flag="toskana"), followers=6, t_dock=("c12s14", 1.0))   # yedi kadırga
shot("liman", ("c15s9", 0), variant="livorno", year=1598, delegation=dict(side="osmanli", n=5, t0=("c15s9", 0.5)), label="Mustafa Ağa'nın gelişi")
shot("liman", a, variant="generic", name="LİMAN ADI", year=None)                                                          # ad levhası yalnız parametreyle
```
**Liman** parametreleri: `variant`, `year` (köşede Cinzel yıl damgası; `stamp=False` kapatır; sayı ya da metin olabilir: `1533`, `"1533"`, `"3 KASIM 1600"` → plakada parametre OLDUĞU GİBİ basılır, kıyafet/ışık mantığı metindeki son 4 haneli sayıyı kullanır), `tod` (marsilya ≥1590 → `dusk`, diğerleri `day`; gece modunda `night`), `ship=dict(kind, flag, scale, x0, mode="arrive"|"depart", dir, highlight, t_leave)`, `followers=n` (arkadan gelen/giden ek kadırgalar; küçük LOD), `x_dock`/`t_dock` (yanaşma konumu/anı; çapa olabilir), `wave_at` (kalabalığın el sallama başlangıcı), `crowd=n` (rıhtım kalabalığı), `delegation=dict(side, n, t0, x_stop, x_from)` (sarıklı, uzun kaftanlı heyet + mektup rulosu), `extra_ships`, `ambient=False` (bayrak/duman/vinç/yeldeğirmeni kapalı), `name=` (levha).
Yanaşma sırası (arrive): gemi soldan gelir → kürekler kaldırılır → baş halatı atılır (~td−1,7) → kıç halatı (~td−1,1) → iniş tahtası iner (td−0,3…+1) → kalabalık el sallar (td−2,6'dan) → iskele işçileri `work haul` ile çeker. depart: tersi (halat çözülür, tahta kalkar, yelken açılır, gemi ayrılır).
**Marsilya 1533/1600 eşleşmesi:** kadraj (katmanlar, kamera `LIMAN_CAMS`, yanaşma yeri/zamanı kesirleri) AYNI; yıla göre yalnız yıl damgası, rıhtım bayrağı (1533 lacivert zemin altın zambak · 1600 beyaz zemin altın zambak), gemi (1533 papalık livresi · 1600 Toskana livresi + altın flama), kıyafet (1533 bereli parlak Rönesans · 1600 koyu, uzun şapkalı) ve ışık (day → dusk) değişir.

## 2. Bağımsız işlevler (haritaya / başka çekime serpiştirme)
```python
import cilt_deniz as DN
DN.ship(f, "kadirga", x, y, h, t, dir=1, flag="toskana", sails=True, oars=True, crew=True, water=True, tod="day")   # h = gövde BOYU (px); su eteği/iz/ripple kendi küçük dalga satırıyla
DN.wave_layers(f, t, tod="day", yh=330.0, band=(150, 800), camx=960, camy=0, z=1.0, swell=1.0, sun_sx=None, glitter=0.0)   # gök + paralaks dalga sıraları → (Sea, Ctx)
DN.flag(c, x, y, w, h, t, shape="swallow|pennant|rect", dev="cross|crescent|lily|medici|bands|stripes|plain", c1, c2, c3, wind=1.0)   # mesh bayrak/flama
DN.gulls(ctx, n, …)  DN.draw_sun(ctx, sx, sy, r)  DN.draw_clouds(ctx, n)  DN.sky_image(tod, yh)  DN.draw_smoke_column(c, x, y_base, h, t, seed, tod)  DN.flame_cluster(c, x, y, s, t, seed)
```

## 3. Mimari ve performans
* **Dalga:** 24 satır, analitik (y = A·(0,62 sin θ + 0,26 sin θ′ + 0,12 sin θ″)); tepe konumları kapalı formda → köpük başlıkları, güneş/ay parıltısı, gemi sallanması aynı dalgayı sürer. Paralaks: satır çarpanı `f = persp(y)`; gemi, önündeki satırdan ÖNCE çizilir (kıyıya ait su eteği + 2 satır sonra kürek/ripple/yansıma/baş dalgası ön dalgaların ÜSTÜNE) → suya oturur.
* **Katmanlar:** gök (önbellek PNG), uzak siluet f=0,30, yapı f=0,82, rıhtım f=1,0 (önbellek PNG, rıhtım 1,2× çözünürlük); gemi gövdeleri/direkler ölçek kovalarında sprite (renk filtresi/kPlus yok); yelken/bayrak = `drawVertices` mesh (köşe rengi = kıvrım gölgesi).
* **LOD:** uzak filo gemileri (≤330 px) `galley_sheet` (14 kürek evreli sprite sayfası) + ucuz flama; yakın gemiler tam dinamik.
* **Bellek / önbellek:** gemi sprite'ları (`_SPR`, 150 MB) ve kadırga sayfaları (`_SHEETS`, 220 MB) **bayt bütçeli LRU**; bütçe aşılınca en az kullanılan atılır (eskiden "hepsini sil" idi → yaklaşan filoda her karede sayfa yeniden pişiyordu: 324 → 119 ms/kare). Güneş huzmeleri 24 önceden döndürülmüş evre (14 kollu simetri) + iki komşu evre çapraz geçişi (döndürerek örnekleme yok; ≈9 → ≈3 ms).
* Deterministik (seed); Program/geçiş/`qa_flow` entegrasyonu sınandı (`Program(shots=[deniz, liman, deniz_filo, deniz_kiyi])` karesi + yikama/slide/light geçişleri; `qa_flow --fast` kapıları geçti).

## 4. c0–c16 uyum tablosu (brif §7 "Ekran önerileri / AKIŞ NOTU" + YONETMENLIK_REHBERI §8 imza sekansları taraması)

| bölüm | bu dünyadan beklenen | karşılayan | not / eksik |
|---|---|---|---|
| c0, c4, c6, c7, c10, c11, c16 | deniz/liman/gemi yok | — | c11 (Roma 1527/Passetto) ve c16 (1743 odası) iç/dış mekân dünyaları (Lab-D/E) |
| c1 | florin yolculuğu (ticaret rotası); V8 şap | `deniz_rota` (tek gemi + `thread`) isteğe bağlı; `ship()` ile harita üstü gemi | rota harita çekimi (`map`) ana ajanda; deniz çekimi yalnız dekor |
| c2 | "senetler kâğıt tekne olup Floransa→Brugge→Londra rotasında yüzer" (rehber §8) | `DN.ship(f, "tekne", …)` + `DN.wave_layers` defter sayfasına serpiştirilebilir | kâğıt-tekne stili (katlanmış kâğıt) bu işte yok: `tekne` ahşap; ana ajan `ship(... flag=dict(...))` ile renk verir |
| c3 | Venedik'e gemi (`pan r`) | `deniz` scene="acik" (kadırga + nao; `cam=("pan","r",180)`) | Venedik silueti (liman) yok: `liman variant="generic", name="VENEDİK"` yedek |
| c5 | Lascaris rotası (harita + gemi) | `deniz_rota` (kadırga/nao, `thread=True`, iki etiket) | Ege/Athos kıyı siluetleri jenerik ada/burun; ad levhası parametreyle |
| c8 V3 | Pisa→Napoli deniz rotası + gemi diorama | `deniz_rota` (`rota_pisa_napoli`) → `liman variant="napoli"` (varış, Castel Nuovo + Vezüv) | rota çizgisi `thread` (soldan sağa); "dalgaya dönüşen çizgi" `wipe` Lab-A'da |
| c8 V4 | Pera/İstanbul limanı; Antonio'nun gemisi **sağdan sola** | `liman variant="pera", year=1479` (mode="depart", dir=−1; Galata kulesi + yarımada silueti; Ayasofya tek minare) | Floransalı temsilcinin mektubu ekranı arka planı olarak da kullanılır (`ambient`, `crowd=6`) |
| c8 V6 | Adriyatik/Otranto alevleri (insan/kan yok) | `deniz_kiyi` (`kiyi_otranto`; kale-kent, alev, duman, silüet donanma) | Osmanlı donanması saygılı/nötr (livre `osmanli`, kadırgalarla aynı özen); ölü sayısı/yazı yok |
| c9 | şap yolu, şube kapanışları (harita) | `deniz_rota` isteğe bağlı (Foça→Brugge); liman yok | |
| c12 | Eleonora'nın yedi kadırgası (Napoli→Livorno), Santo Stefano kadırgaları (`pan r`), Lepanto "12/≈200" | `liman variant="napoli" ship=dict(mode="depart", dir=-1) followers=6` (`liman_napoli_yedi`); `deniz` acik + `highlight=True` kadırgalar; `deniz_filo n=24 highlight=12` (+ `n=90` yoğun) | "Toskana gönderdi ↔ papalık kiralamış" belirsizliği: altın flama yalnız görsel vurgu; rakam/etiket ekrana basılmaz (kadırga çubuğu `bars` ana ajanda) |
| c13 V1 | Marsilya 1533 limanı: kadırgalar, sancaklar, mendireğe yaklaşan alay; kamera deniz seviyesinden ağır itiş; Floransa→Marsilya iplik | `liman variant="marsilya" year=1533 thread=True` (`LIMAN_CAMS`: alçak başlangıç + itiş) | alay = rıhtım kalabalığı + bayraklar; yürüyen "gelin alayı" `frieze/procession` (Lab-B) |
| c13 V7 | Livorno→Marsilya rotası; **V1'in aynı kadrajı**, 3 KASIM 1600 | `deniz_rota` → `liman variant="marsilya" year=1600` (AYNI kadraj/kamera; dusk ışığı, Toskana livresi, koyu kıyafet) | etiket "3 KASIM 1600" yazısı ana ajanda (`kick=`/`caption=`) |
| c14 V3 | Livorno limanı kuşbakışı (ağırlıkla yan görünüm), Fahreddin'in üç gemisi | `liman variant="livorno"` + `followers=2` (kıyıya yaklaşan üç gemi); `deniz` acik + 3 nao | kuşbakışı (üstten) görünüm yok: yan panorama |
| c15 | Livorno, Mustafa Ağa'nın gelişi (rıhtımda heyet + mektup rulosu); Fahreddin'in gemileri | `liman variant="livorno" year=1598 delegation=dict(side="osmanli", n=5)` (`liman_livorno_elci`) | heyet saygılı, sarık + uzun kaftan; "siluet" yerine renkli figür (isteğe bağlı koyu ton ana ajanda) |
| rehber §8 imza | c3 gemi `pan r`, c5 Lascaris, c8 deniz rotası + İstanbul limanı, c12 Lepanto, c14 Livorno | yukarıdakiler | |

## 5. Olgu ve kısıt notları
* Ekrana yalnız parametreyle gelen metin basılır: yıl damgası (`year`), liman adı (`name`), rota etiketleri (`labels`), `kick/caption`. Hiçbir ad/sayı/tarih uydurulmadı.
* Şiddet yok: filo çekimlerinde çarpışma/ateş/ölü yok (yaklaşma + sancak + isteğe bağlı duman perdesi); Otranto'da alev+duman stilize, insan/ceset/kan yok; hançer/çatışma jesti yok.
* Osmanlı unsurları: kadırgalar aynı özenle çizilir (yeşil kuşak, yaldız, kızıl tente, hilâl armalı flama); heyet/kayıkçı figürleri sarıklı ve uzun kaftanlı (karikatür yok). Pera siluetinde Ayasofya'nın minare sayısı yıla göre (<1500: 1; <1574: 2; sonra 4).
* Marsilya yeldeğirmenleri, Livorno bastionu, Napoli Castel Nuovo kuleleri, Galata kulesi vb. **stilize** siluetlerdir (mimari kesinlik iddiası yok; "mekân siluetleri kodla; mimari doğrulama gerekir").
* Venedik livresi: kızıl zemin + altın bant (yıldız/aslan armasız; ekrana devlet bayrağı iddiası konmaz). Toskana vurgusu: altın flama + altı top (palle) devresi.

## 6. Ölçümler (tek işlem, tek çekirdek, paylaşımlı makine: yük ort ≈3; tam çözünürlük çizim 1920×1080 + `CM.post`)
`python3 preview_deniz.py --ms` = klipteki gibi **ardışık** 24 kare (çekimin %45'inden; kare sprite/evre pişirmeleri bir ısınma geçişinde yapılır, klipte süreye yayılır). "ilk kare" = soğuk bellek (gökyüzü/liman/sprite pişirme) süresi.

| girdi | ort ms/kare | maks | ilk (soğuk) kare |
|---|---|---|---|
| acik_kadirga | 130 | 160 | 1408 |
| acik_nao_gece | 126 | 153 | 412 |
| acik_nao_alacakaranlik | 128 | 160 | 272 |
| acik_ufuk_yaklasan | 113 | 138 | 203 |
| rota_pisa_napoli | 106 | 146 | 144 |
| filo_inebahti (24+24, `highlight=12`) | 119 | 157 | 452 |
| filo_yogun (90+90) | 124 | 158 | 102 |
| kiyi_otranto | 146 | 188 | 452 |
| liman_marsilya_1533 | 173 | 224 | 615 |
| liman_marsilya_1600 | 177 | 216 | 895 |
| liman_napoli_yedi | 176 | 204 | 669 |
| liman_pera | 166 | 229 | 713 |
| liman_napoli | 170 | 229 | 402 |
| liman_livorno_elci | 181 | 245 | 631 |
| liman_generic | 148 | 203 | 879 |

Hepsi **≤250 ms/kare (en kötü kare 245 ms)**. Klip duvar süreleri (0,5 ölçek, ffmpeg dâhil, 288–336 kare): 38–46 s (açık/filo/kıyı), 57–69 s (liman). Kontak sayfası 1–2 s. Soğuk önbellek pişirme (`--bake`, disk önbelleği silinmiş): Marsilya 1,2 s, Pera 1,1 s, Otranto 0,2 s. Önbellek dosyaları `out/_cache/world/deniz_*_<sürüm>.png`.

**Hareket enerjisi** (klip, 240×135 gri; ardışık-kare ort. fark / 0,5 sn'lik fark; ölü kare = fark<0,02):
açık kadırga 1,40 / 5,04; nao alacakaranlık 0,95 / 3,92; nao gece 0,62 / 2,96; ufuktan yaklaşan 0,76 / 3,89; rota 1,53 / 3,90; filo 0,68 / 4,12; filo yoğun 0,54 / 3,13; kıyı (Otranto) 0,79 / 5,25; limanlar 1,13–1,68 / 5,96–7,83. **Hiçbir klipte ölü kare yok (0).** Karşılaştırma: `sehir_meydan_ates` 1,80 / 9,61; `sehir_kale_castel` 1,23 / 7,64; `oda_salon_medici` 3,98 / 19,5; `world_build_uffizi` 2,25 / 13,0. Deniz çekimleri büyük sakin gök/su alanı taşıdığı için piksel farkı doğal olarak düşüktür; hareket kaynakları: dalga sıraları (paralaks), köpük/parıltı, gemi yalpası, kürek/yelken/flama mesh'i, martılar, bulut kayması, kamera yolu (her varsayılan kamerada itiş/kayma var).

**Doğrulamalar:** (1) Determinizm: Marsilya 1533 / filo_inebahti / acik_kadirga t=5 sn tam çözünürlük karesi iki ayrı işlemde (biri soğuk, biri disk önbelleği sıcak) **bayt bayt aynı** (md5). (2) Marsilya 1533 ↔ 1600 aynı kadraj/kamera: t=1/5/9/13 sn karelerinin yapısal kenar haritaları arasında sıfır kaymada korelasyon 0,90–0,91 ve en iyi hizalama her seferinde (dx=0, dy=0). (3) `import shots, compose` ve `Program` (deniz+liman+deniz_filo+deniz_kiyi) kare/geçiş/`qa_flow --fast` denemesi hatasız.

## 7. Bilinen kusurlar
* **Hareket enerjisi** pano/şehir/oda çekimlerinden düşük (bkz. §6): açık deniz klipleri sakin ritimli; "daha da canlı" isteniyorsa `swell=` (dalga genliği) ve `cams=` ile daha hızlı itiş/kayma verilebilir, `acik_nao_gece` en durgun çekimdir (gece ışığı).
* Kâğıt tekne (c2 "senetler kâğıt tekne olup yüzer") **yok**: `tekne` ahşap.
* Livorno limanı kuşbakışı (c14) **yok**: yan panorama (bastion + rıhtım + açık deniz).
* Mimari siluetler (Marsilya yeldeğirmenleri/kule, Livorno bastionu, Napoli Castel Nuovo/Vezüv, Pera/Galata/Ayasofya) **stilize**; mimari doğrulama ana ajanda/metin denetiminde.
* Yanaşmış kadırgada kürekler dikey "selam" dizisi gibi ince çubuklar (stilize; tam çözünürlükte çok ince hatlar 0,5 ölçekte kaybolabilir).
* Heyet/kalabalık figürleri küçük (86–100 px); yakın plan insan/yüz çekimi bu işin kapsamında değil (Lab-B figürleri).
* Gece gemi fenerleri ve ay parıltısı yalnız önceden renklendirilmiş parıltı sprite'ı (kPlus/renk filtresi yok: bu CPU'da 6× yavaş) → cam/yelken üzerinde gerçek ışık sıçraması yok.
* Soğuk ilk kare 0,1–1,4 s: kod değişince sürüm özeti değiştiği için gökyüzü/liman katmanı ilk çalıştırmada yeniden pişer (sonra önbellekten).
* Bayrak/armalar stilize hane/devlet renkleri: Venedik kızıl-altın bant (aslan/yıldız yok), Toskana altın palle, Marsilya'da Fransa kraliyet renkleri (mavi/altın zambak, beyaz sancak; kale + rıhtım sancakları), Napoli/Pera/Livorno'da jenerik şerit/bant. Birebir resmî bayrak/arma iddiası yok; ekrana yazı olarak yalnız parametre gelir.

## 8. Ana ajandan istek (paylaşılan API; bu iş dokunmadı)
1. **`cilt_cam.OWN_CAMERA` kalıcı kayıt:** şu an `cilt_deniz` modül yüklenirken `OWN_CAMERA.update(("deniz","deniz_rota","deniz_filo","deniz_kiyi","liman"))` çağırıyor (sehir de aynı yolu izliyor). İstenirse `cilt_cam.py`'de `OWN_CAMERA = {"pano","build","sehir","deniz","deniz_rota","deniz_filo","deniz_kiyi","liman"}` yapılırsa `qa_flow` ve sahne yazıcıları modülü import etmeden aynı bilgiyi görür (davranış değişmez).
2. **`qa_flow` yerleşim denetimi:** `liman` çekimlerinde yıl plakası (`year=`) sol-altta, liman adı levhası (`name=`) üst-ortada, rota etiketleri (`labels=`) kıyı üstünde; `kick/caption` bandı bunlarla çakışmasın diye alt şeritte `kick`/`caption` yalnız yıl plakası YOKKEN kullanılmalı (ya da `caption` sağa kaydırılmalı).
3. **Sahne yazarı notu:** `deniz_rota`, `deniz_filo`, `deniz_kiyi` aynı işin ayrı adlarıdır ("aynı tür üst üste ≤2" kuralını aşmadan arka arkaya kullanım için); olay zamanları parametreyle belirlenir (`t_dock`, `smoke_at`, `fire_at`, `delegation.t0`) — SFX/ses tasarımı bu zamanlara bağlanabilir (dalga/halat/kürek/martı/çan).
4. **Ses (müzik/SFX):** yanaşma (`t_dock`), ip atma, alev başlangıcı (`fire_at`) ve duman perdesi (`smoke_at`) saniyeleri çekim satırından okunabilir.

## 9. Komut özeti
```
cd gunluk-shorts/medici-uzun-dosya
python3 preview_deniz.py                         # 15 girdi: sayfa + klip (≈12 dk, arka planda)
python3 preview_deniz.py --ms                    # ms/kare (ardışık, ısınmış)
python3 preview_deniz.py --energy acik_kadirga   # hareket enerjisi + ölü pencere
python3 preview_deniz.py --bake                  # soğuk pişirme süreleri (önbelleği siler)
python3 preview_deniz.py --at liman_pera 9.0     # tam çözünürlüklü tek kare
```
Kullanım (örnek satırlar §1): `shot("deniz", t, scene="acik", ...)`, `shot("liman", t, variant="marsilya", year=1533, thread=True)`.

