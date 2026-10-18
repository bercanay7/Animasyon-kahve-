# SAHNE KATALOĞU — deniz / savaş alanı / kuşatma (sahne-lab)

Dosyalar: `scenes_sea.py` (sea) · `scenes_field.py` (field) · `scenes_siege.py` (siege) · yardımcılar `props_war.py`, `stage_war.py`, `figs_war.py`.
Hepsi `theatre` çekim şablonuyla kullanılır (STIL_REHBERI §6):

```python
import scenes_lib, scenes_sea as SS          # sahne modülünü import etmek şart değil (scenes_lib otomatik yükler) ama kamera yardımcıları için import et
shot("theatre", a=("c1s14", -0.2), scene="sea", cams=[(0.0, (960, 540, 1.0)), (("c1s14", 4.0), SS.cam_on(0, 0.5, 1.5))], p=dict(mood="storm", ...), label="tazones")
```
Ortak kurallar (üç aile için de geçerli):
- **Kamera**: `cams=[(çapa,(x,y,zoom)),…]`, zoom 1.0–2.2. Pişirilen katmanlarda 220 px pay var; sınırı aşan kamera kayması kenarda boşluk gösterir. **Güvenli aralık**: zoom 1.0'da |x−960| ≤ 190 ve |y−540| ≤ 190; zoom 1.5'te ≈ ±480 / ±360; zoom 2.0'da ≈ ±620 / ±440. Emin değilsen `SS.safe_cam(x, y, z)` (sıkıştırır) kullan. Paralaks: yakın katman daha çok kayar (derinlik 0.08 → 1.14).
- Yerel zaman `cx.t` (sn): dalga, bayrak, alev, duman, kürek hep yerel zamana bağlı sürekli animasyon; çekim başında "donmuş" kare yok.
- Her aile `dyn()` içinde bulanıklık/degrade/ışık huzmesi çizmez (hepsi pişirmede). Ağır işler `lru_cache`'li sprite'tır; ilk karede ~1–2 sn pişirme gecikmesi olur (sonraki çekimler aynı `p` ile anında).
- **İlk kare gecikmesi**: yeni bir `p` (gök/zemin/şehir) kombinasyonunun ilk karesi 1–2 sn'lik pişirme içerir (sonraki çekimler aynı `p` ile anında). Görüntü önbellekleri sınırlıdır (tepe bellek ≈ 1.2 GB, 98 farklı yapılandırmada) — ayrı `tag=` ile gereksiz farklı yapılandırma üretme.
- **Önbellek notu**: pişirme anahtarı `p`'nin yalnız *skaler* (str/sayı/bool/tuple) alanlarından çıkar; listeler (`ships`, `armies`) pişirmeyi etkilemez → aynı sahnede gemi/ordu listesini çekimler arasında serbestçe değiştir.
- Renk: bölüm kodları — Habsburg/İspanya kırmızı `#8E1F26`, Fransa mavi `#27427A`, Osmanlı yeşil `#2F6B4A`, Portekiz `#2D5A8E`, Venedik turkuaz `#2F7A8A`, Papalık altın `#D4B64E`, Protestan petrol `#1E5560`.
- Ölçülen süreler **post dahil** (sk.post ≈ 30–60 ms), 4 çekirdekli paylaşımlı makinede; boş makinede ≈ %25 daha hızlı.

---
## 1) `sea` — deniz  (scenes_sea.py)  ✅ hazır

Gök + ufuk + 5 derinlikli dalga bandı (kayan dikişsiz dalga şeritleri) + gemiler + isteğe bağlı kıyı. Kıyı/şehir/köy, güneş/ay yolu (ekran uzayında sabit), bulutlar kayar, şimşek, yağmur, top dumanı, yanma, batma.

### `p` anahtarları (varsayılan)
| anahtar | değer | açıklama |
|---|---|---|
| `mood` | `"calm"`(varsayılan) `"dawn"` `"dusk"` `"night"` `"storm"` | calm: sıcak sisli öğleden sonra; dawn: pembe-altın şafak (güneş solda, ufuk üstünde); dusk: kızıl gün batımı (güneş sağda), fener/lomboz ışıkları yanar; night: ay + yıldız, soğuk mavi; storm: koyu gri-yeşil, büyük dalga, köpük |
| `ships` | `[dict(...)]` (varsayılan: tek karaka x=.5,row=0) | gemi listesi, aşağıda |
| `coast` | `None` `"tazones"` `"africa"` `"harbor"` | tazones: Asturias burnu + taş evli balıkçı köyü + kilise + mendirek feneri + demirli balıkçı tekneleri + kıyı köpüğü · africa: teraslı beyaz şehir, minareler, kubbeler, sur-kule, fener, palmiye (Tunus/Cezayir) · harbor: rıhtım, çan kuleleri, fener, bağlı gemi direkleri (kutlama/liman) |
| `coast_side` | `"l"` `"r"` | kıyının tarafı (tazones→"r", africa→"l", harbor→"r") |
| `lightning` | 0..1 (storm: 0.7, diğer: 0) | şimşek sıklığı/şiddeti. Çatal + bulut/deniz aydınlanması. Parlama zamanları sahte-rastgele ama deterministik (lightning=.7'de yerel ≈0.4, 4.2, 7.4, 10.3 sn) |
| `flashes` | `[t1, t2, …]` yerel sn | verilirse şimşekler tam bu anlarda çakar (anlatıdaki sözcüğe bağlamak için `cx.at(...)` kullanamazsın—çekim yaratılırken saniyeyi elle yaz: `flashes=[1.2, 3.9]`) |
| `rain` | 0..1 (storm: 0.85, diğer: 0) | yağmur (3 katman çizgi, ekran uzayı) |
| `moon` | bool (night: True) | herhangi bir ruh hâlinde ay + ay yolu |
| `smoke` | 0..1 | top dumanı bulutları (`gun>0` gemilerin çevresinde; yoksa rastgele yerlerde) |
| `mist` | 0..1 | deniz sisi (bantlar arası derinlik buğusu artar; c9 açık okyanus/Preveze sabahı için) |
| `wind` | -1 (varsayılan) `1` | dalga/bulut kayma yönü: −1 = sola, +1 = sağa |

### Gemi sözlüğü `ships=[dict(...)]`
| anahtar | varsayılan | açıklama |
|---|---|---|
| `kind` | `"carrack"` | `"carrack"` (3–4 direkli karaka/nau: haçlı yelken, çarmıh, gözetleme sepeti, kıç kasara, fener) · `"galley"` (kadırga: mahmuz, iki latin yelken, 22 hareketli kürek, kıç tente + 3 fener, pruva topu) · `"fishing"` (balıkçı: tek latin yelken, 2 balıkçı) |
| `x` | 0.5 | yatay konum 0..1 (1920 px'e oranlı; −0.2..1.2 ekran dışından giriş için geçerli) |
| `row` | 0 | **0 = en yakın/en büyük**, 1 orta, 2 uzak, 3 ufuk (gövdesi ufukta batık "hull-down", çok küçük). Ölçek çarpanı: 1.0 / 0.68 / 0.42 / 0.22 |
| `s` | 1.0 | sıra ölçeğine ek çarpan |
| `flag` | `"#8E1F26"` | bayrak/tente rengi (yelken haçı da bu renk). **Belirgin yeşil (ör. `#2F6B4A`) otomatik yarım ay + yıldız**; zeytin/haki (`#5A6A3A`), turkuaz (`#2F7A8A`), altın, mavi, kırmızı → haç. Zorlamak için `emblem` |
| `emblem` | `"auto"` | `"cross"` `"crescent"` ile zorla (haç bayrağı vs yarım ay bayrağı: Preveze) |
| `heading` | 1 | +1 pruva sağa, −1 pruva sola |
| `rock` | storm 1.0, diğer 0.28 | sallanma (yalpa ≤ ±5.5°, dikey çırpınma) |
| `sink` | 0 | 0..1 batma: yan yatar + suya gömülür (su hattında kırpılır) + köpük halkası/kabarcık/enkaz. **Çekim içinde animasyon**: `sink=0, sink_to=0.9, sink_t=(1.0, 7.0)` (yerel sn; yumuşak geçiş). 0.55 gibi sabit yarı-batmış poz da iyi görünür |
| `burn` | 0 | 0..1 yanma: güvertede 3–6 alev, yanık yelken, duman sütunu, su üstünde turuncu yansıma. Animasyon: `burn=0, burn_to=1, burn_t=(0.5, 4.0)` (yelken kararması 0.25'lik adımlarla) |
| `gun` | 0 | 0..1 top atışı sıklığı: namlu alevi + büyüyen/dağılan duman |
| `sails` | carrack&storm: `"reef"`, diğer `"full"` | `"full"` `"reef"` (alt yelkenler) `"torn"` (yırtık) `"bare"` (çıplak direk; kıyıda bağlı gemi) |
| `lamp` | dusk/night: True | gövde lombozları + kıç fener ışığı |
| `drift` | 7 px/sn × sıra ölçeği | pruva yönünde yavaş ilerleme (0 = olduğu yerde) |

### Kamera
`SS.cam_on(row, x, zoom, rise=0, s=1)` → geminin ekran ortasına geleceği güvenli `(x, y, zoom)`; `rise` 0 = gövde, 1 = direk ucu. Örnekler:
- Geniş (yavaş itme): `cams=[(0,(960,540,1.0)), (8,(1010,556,1.18))]`
- Kahraman gemi: `cams=[(0, SS.cam_on(0, .46, 1.35)), (6, SS.cam_on(0, .46, 1.9, rise=.35))]`
- Tazones köy: `cams=[(0,(1000,560,1.0)), (6,(1180,600,1.45))]`
- Ufuktaki filo: `cams=[(0,(960,520,1.0)), (7,(960,505,1.5))]` (ufuk ≈ y 500; zoom'da ufuk yukarı kayar)

### Bölüm tarifleri
- **c1 Tazones fırtınası**: `dict(mood="storm", coast="tazones", lightning=0.8, rain=0.9, ships=[dict(kind="carrack",x=.3,row=0,rock=1,flag="#8E1F26"), dict(kind="carrack",x=.62,row=1,heading=-1,rock=1), dict(kind="carrack",x=.5,row=2,rock=1,sails="torn"), dict(kind="carrack",x=.12,row=2,rock=1), dict(kind="carrack",x=.84,row=0,s=.85,heading=-1,sails="torn")])` — köyü göstermek için kamerayı sağa (x≈1150–1300) kaydır. Köy ışıkları fırtınada yanık.
- **c8 Tunus / Halkulvadi çıkışı**: `mood="dawn"` veya `"calm"`, `coast="africa"`, 6–10 kadırga (`row` 0/1/2 dağıt, yeşil bayraklı Osmanlı). `drift` ile yavaş ilerlet.
- **c8 Preveze (iki taraf)**: `mood="calm"` veya `"dusk"`, `smoke=0.8`, yeşil `#2F6B4A` (yarım ay) galeri vs kırmızı/haç `#8E1F26`/`#2D5A8E` karaka+kadırgalar, hepsinde `gun=0.6–1.0`; bir-iki gemide `burn` / `sink=.55`.
- **c8 Cezayir fırtınası (batan gemiler)**: `mood="storm", coast="africa", rain=.9`, gemilerde `sink=.35/.6/.9` (yarım batmış, yan yatmış) ve `sails="torn"`.
- **c8 gece denizi / ufukta filo**: `mood="night"`, `row=3` + `row=2` küçük kadırgalar; `lamp` ışıkları.
- **c9 Magellan/Elcano (açık okyanus)**: `mood="dawn"` veya `"dusk"`, tek karaka `row=0`, `mist=0.3`, `rock=.2` (başka gemi yok); çok yavaş itme.
- **c8 kutlama (defne/çan/sancak)**: `mood="dusk"`, `coast="harbor"`, bağlı gemiler kıyıda otomatik (sails="bare").

### Performans (ms/kare, post dahil)
calm 1 karaka ≈ 110–135 · dawn ≈ 110–140 · storm 5 karaka + tazones ≈ 120–180 · night+harbor ≈ 130–185 · dusk 8 kadırga (tümü top atıyor) + africa + smoke ≈ 190–270 (aşırı durum). Zoom 1.7'de +10–40 ms.

### Bilinen kusurlar
- Gemiler yandan görünüştür (perspektif yok); haç/yelken kabarması stilizedir. Gövde su altında dalga bandıyla kesilir (gemi "oturur"): yüksek dalgada alt gövde dalga arkasında kaybolur — bilinçli.
- `sink` yarım-batmış duruş içindir; tam batış animasyonu için çekim başına farklı `sink` verip kesme/geçiş kullan.
- Kıyı burnu (tazones) arkasındaki sıra-1/2 gemileri örter; gemileri kıyıdan uzak (x<.6) tut ya da `coast_side` çevir.
- `coast="africa"` şehri gündüzleri biraz açık/krem; dusk/dawn/night'ta daha iyi görünür.
- Dalga şeritlerinin tekrar periyodu 900–1540 px: çok yavaş ve çok uzun çekimde desen tekrarı fark edilebilir (15 sn'ye kadar sorun yok).

---
## 2) `field` — savaş alanı  (scenes_field.py)  ✅ hazır

Gök + ufuk + uzak sırtlar (+ isteğe bağlı uzak kale/şehir) + 4 derinlikli zemin bandı (+ isteğe bağlı nehir bandı) + ordular (figür-lab siluetleri) + ön plan çimen/kamış çerçevesi + hava (yağmur/sis/kar/şafak/alacakaranlık).
Ordular `ST.figure` sprite'larıyla çizilir: pikeman, landsknecht, arquebusier, halberdier, peasant, crowd_a/c, janissary, cavalry_charge(+_b), sipahi(+_b) (figür-lab türleri yoksa otomatik `pikeman`'a düşer).

### `p` anahtarları (varsayılan)
| anahtar | değer | açıklama |
|---|---|---|
| `ground` | `"plain"`(varsayılan) `"marsh"` `"river"` `"hills"` | plain: Kastilya ovası, hafif dalgalı, kavaklar; marsh: düz, su birikintileri, ölü ağaçlar (Mohaç); river: `river=True` varsayılır, nehir bandı + kıyı kamışları; hills: belirgin tepeler, çam kümeleri |
| `weather` | `"clear"`(varsayılan) `"fog"` `"rain"` `"dawn"` `"dusk"` `"snow"` | clear: sıcak öğleden sonra; fog: kalın sis (kayan sis katmanı, soluk güneş); rain: koyu bulut + 3 katman yağmur + ıslak zemin/su birikintisi; dawn: pembe-altın şafak (güneş solda), sis; dusk: kızıl alacakaranlık (güneş sağda), kor/meşale daha çok parlar; snow: kar yağışı (3 katman) + beyazımsı zemin |
| `armies` | `[dict(...)]` | ordu listesi, aşağıda (varsayılan: tek 30 kişilik pike bloğu) |
| `banners` | bool (True) | her ordudan bir sancak (piyadede; atlıda yok). Renk = `side`; arma: kırmızı Habsburg tonları → Burgonya çaprazı, yeşil → yarım ay, diğer → haç |
| `smoke` | 0..1 veya bool | barut dumanı bulutları (uzak/orta bantlarda). Arquebus atışları ayrıca kendi dumanını üretir |
| `fire` | 0..1 | ufukta yanan köy/kale (1–3 yangın: alev + duman sütunu + parıltı) — Köylü Savaşı, kuşatma sonrası |
| `river` | bool | nehir bandı (ground="river"da otomatik). Nehir b0–b1 arası; `ford=True` ordular nehrin içinde yürür |
| `castle_far` | `None` `"pavia"` `"toledo"` | ufukta (x≈.70) sisli siluet: pavia = Visconti kalesi + park surları + kavaklar; toledo = tepe şehri + Alcázar + katedral kulesi |
| `wind` | −1 / 1 | bulut/sis/nehir/sancak yönü (varsayılan −1: sancaklar sola dalgalanır → ordu `dir=+1` ilerlerken doğal) |
| `rain` / `snow` | 0..1 | hava dışında yağmur/kar ekle ya da kıs |

### Ordu sözlüğü `armies=[dict(...)]`
| anahtar | varsayılan | açıklama |
|---|---|---|
| `side` | `"#8E1F26"` | taraf rengi (sancak, hafif siluet tonu). **Belirgin yeşil** (`#2F6B4A` gibi; zeytin/haki `#5A6A3A`/`#6A7A38` sayılmaz) ise: atlı → sipahi, piyade → janissary, sancak → yarım ay. Zorlamak/kapatmak için `ottoman=True/False`, sancak arması için `emblem="cross|crescent|saltire|none"` |
| `kind` | `"pike"` | `"pike"` (pike/landsknecht/halberd karışık blok) · `"arquebus"` (arkebüzcü + halberd; periyodik namlu alevi + duman) · `"cavalry"` (dörtnala; iki pozlu yürüyüş) · `"peasants"` (yabalı köylüler + kalabalık; `torch` ile meşale) · `"mixed"` (pike+arkebüz karışık) |
| `x` | 0.5 | grubun merkezi (0..1 × 1920). Birlikler `dir*hız*t` ile ilerler (x'i ekran dışına taşırma) |
| `row` | 1 | **0 = en yakın/en büyük** (boy ≈ 250 px piyade / 262 atlı), 1 orta (×0.66), 2 uzak (×0.43). Yakın sıra alttaki bandda durur (ground eğimini izler) |
| `n` | 24 | kişi/atlı sayısı (piyade: 3–6 saflı blok; atlı: ≤9 tek saf, fazlası 2 saf) |
| `dir` | 1 | +1 sağa, −1 sola bakar/ilerler |
| `charge` | 0 | 0..1 ilerleme/atılış: atlıda 0→170 px/sn (×sıra ölçeği), piyadede 0→34 px/sn, köylüde 48 px/sn; aynı zamanda yürüyüş/dörtnala salınımı ve dörtnala yürüyüş hızı. 0 = yerinde bekler (hafif nefes) |
| `unit` | otomatik | belirli figür türü: `"janissary"`, `"landsknecht"`, `"halberdier"`, `"knight"`, `"horse_rider"` ya da tür listesi `("pikeman","landsknecht")` |
| `s` | 1.0 | ölçek çarpanı |
| `spread` | 1.0 | yatay aralık çarpanı (gevşek/sıkı dizi) |
| `fire` | arquebus: 1.0 | atış sıklığı (0..1). Namlu alevi + büyüyen duman |
| `torch` | 0 | 0..1 meşale taşıyan oranı (dusk/dawn/rain/fog'da çok iyi) |
| `banner` | True | bu ordunun sancağı |
| `ford` | False | `river=True` iken ordu nehrin içinde (bel hizası su, çevresinde sıçrama): **Mühlberg** süvarisi |

### Kamera
`SF.cam_on(row, x, zoom, rise=.4)` → verilen sıradaki birliğin ekran ortasına geldiği güvenli kamera. Örnekler:
- Geniş: `cams=[(0,(960,560,1.0)), (8,(1010,576,1.2))]`
- Hücum takibi (süvari row 0): `cams=[(0, SF.cam_on(0,.30,1.25)), (6, SF.cam_on(0,.62,1.6))]` — süvari `dir=+1` ilerlerken kamera da sağa kayar.
- Piyade bloğu yakın: `cams=[(0,(900,600,1.4)), (6,(1000,620,1.9))]`
- Güvenli kayma: zoom 1.0'da |Δx|,|Δy| ≤ 190; zoom 1.6'da ≈ ±530 / ±400; `SF.safe_cam(x,y,z)` sıkıştırır. Ön plan çimeni (en yakın katman) hızlı paralaks verir.

### Bölüm tarifleri
- **c3 Villalar**: `ground="plain", weather="rain"`, `armies=[dict(side="#8E1F26",kind="cavalry",x=.28,row=0,n=10,dir=1,charge=.9), dict(side="#5A6A3A",kind="peasants",x=.74,row=1,n=34,dir=-1)]`; kamera süvariyi izler.
- **c5 Mühlberg**: `ground="river", weather="fog"` (veya `"dawn"`), `armies=[dict(side="#8E1F26",kind="cavalry",x=.30,row=1,n=9,dir=1,charge=.5,ford=True), dict(side="#1E5560",kind="pike",x=.78,row=2,n=34,dir=-1)]` (Protestan petrol `#1E5560`).
- **c5 Köylü Savaşı**: `ground="plain", weather="dusk", smoke=.8, fire=.9`, `peasants` (`torch=.3`) + karşıda `mixed`/`pike`.
- **c6 Pavia**: `weather="fog", castle_far="pavia", smoke=.6`, `arquebus` (fire=1) + `cavalry` + `pike`; Fransız mavi `#27427A` vs İspanyol kırmızı.
- **c7 Mohaç**: `ground="marsh", weather="rain"` (veya dusk), Macar (kırmızı/haç) vs Osmanlı yeşil: yeşil `cavalry` otomatik sipahi, yeşil `pike/mixed` otomatik janissary.

### Performans (ms/kare, post dahil)
villalar (3 ordu, 54 kişi) ≈ 150–170 · muhlberg nehir ≈ 115–170 · pavia sis+kale+duman ≈ 140–210 · köylü (60 köylü + yangın + meşale) ≈ 160–220 · 190 figür kar tepeleri ≈ 120–185. Zoom 1.7'de +30–60 ms. Ordu başına ~60 figürden sonra maliyet artar (figür başına ≈ 0.15 ms + yalnız ekranda görünenler çizilir).

### Bilinen kusurlar
- Piyade yalnız dikey salınımla yürür (sprite sabit poz); dörtnala iki poz (_a/_b) arasında geçişle. Formasyon sahte-rastgele (aynı n → aynı düzen).
- Zemin eğimi yalnız 4 sabit bant: figürler bantlar arasında kayarak "sıra değiştirmez" (row sabit).
- Kar ve sis sahnelerinde kontrast düşük tutuldu; "snow" yine de en açık sahnedir (kasıtlı).
- Ön plan çimen/kamış çerçevesi kamera yakındayken alt kenarı kaplar; gerekirse kamerayı yukarı al.

---
## 3) `siege` — kuşatma  (scenes_siege.py)  ✅ hazır

Gök + uzak tepe/dağ (+ aya/güneşe göre ışık) + **şehir/kale katmanı** (sur, kule, bastiyon, ev dizisi, yapılar; derinlik .42) + orta zemin (hendek, palisad, gabion, çadırlar, top mevzileri; .64) + yakın zemin (büyük çadırlar, gabion, topçu, askerler; .92) + ön plan (kamış/kazık; 1.22) + dyn: yangın/alev/duman, top ateşi + sur isabetleri, merdiven + tırmanan askerler, savunucular, sancaklar, kamp ateşleri, yağmur/kar. Su kentleri (Halkulvadi, Tenochtitlan, Toledo nehri) gerçek dalga şeritleriyle kayan su.

### `p` anahtarları (varsayılan)
| anahtar | değer | açıklama |
|---|---|---|
| `city` | `"roma"`(varsayılan) `"viyana"` `"guns"` `"halkulvadi"` `"tenochtitlan"` `"toledo"` | aşağıda şehir şehir |
| `time` | `"day"`(varsayılan) `"dusk"` `"night"` | day: güneşli, gök mavi; dusk: kızıl-turuncu, çadır/pencere/ateş ışığı yanar (en sinematik); night: ay + yıldız, soğuk mavi, ateş/meşale ışığı baskın |
| `weather` | `"clear"`(varsayılan) `"rain"` `"snow"` | rain: koyu bulut, 3 katman yağmur, çamur birikintisi, ıslak zemin; snow: kar yağışı, çatılar/zemin beyaz, gökyüzü soluk |
| `fire` | 0..1 (0) | şehirde yangın: pencere/çatı alevleri (en fazla ~9 alev, boyu `fire` ile büyür), duman sütunları, gökyüzü/su turuncu parıltı; su kentlerinde suya yansır. Bool da kabul (True=1) |
| `cannon_fire` | 0..1 veya bool (0) | top ateşi: yakın+orta mevzilerdeki toplar periyodik ateşler (namlu alevi, geri tepme, büyüyen duman) + **surda isabet** (parlama, toz, moloz) + savunucuların küçük ateşleri. 0 = toplar sessiz. Kuşatma gemileri (Halkulvadi/Tenochtitlan) de `gun` ile ateşler |
| `ladders` | bool (False) | surlara dayalı merdivenler + tırmanan askerler (roma 5, viyana 3, halkulvadi 3, guns/toledo uygun değil → yok sayılır) |
| `smoke` | 0..1 veya bool | ek barut duman bulutları (yakın plan). `cannon_fire>0.3` zaten biraz üretir |
| `soldiers` | 0..1 (1) | yakın/orta zemindeki asker yoğunluğu |
| `wind` | −1/1 | bulut/duman/su yönü (varsayılan −1) |
| `tag` | str | yok sayılır (yalnız önbellek ayırmak için kullanabilirsin) |

### Şehirler
| `city` | içerik | saldıran | kamera notu |
|---|---|---|---|
| `roma` | Aurelius surları (tuğla, kareli kuleler, kapı + kafes), arkada yanan evler, Eski Aziz Petrus (nef + çan kulesi), **Castel Sant'Angelo** (kare kaide + silindir + melek heykeli) sağda x≈1480; savunucular; papalık sancakları | İmparatorluk (landsknecht/arkebüz/halberd/pike; kırmızı çadır) | c6: `time="dusk"`, `fire=.6–1`, `ladders=True`, `cannon_fire=.8`; sur tepesine yakın plan: `SS.cam_on_city(.30, 1.8)` |
| `viyana` | taş sur + 2 açılı bastiyon + kapı, **Stephansdom** (sivri kule + mozaik çatı), kırmızı çatılı evler, kule sancakları | Osmanlı (yeniçeri; yeşil/kırmızı/altın çadırlar, yarım ay alemli) | c7: day/dusk/rain/snow; yağmur+çamur: `weather="rain"`; geri çekilme: `time="dusk", weather="snow"` |
| `guns` | tepe üstünde küçük kale (iki yuvarlak kule + donjon + şapel), yamaçta köy, çam | Osmanlı | küçük, uzak görünür → kamera `SS.cam_on_city(.62, 1.5)` ile kaleye yaklaş |
| `halkulvadi` | denize uzanan kare kale (bastiyonlar, talus, kapı), Tunus minareleri (sisli), kum bankı; **önde deniz + kuşatma kadırgaları/karaka (top atar)**, kumsalda topçu | İmparatorluk filosu (kırmızı haç) + Osmanlı yeşil kadırga | c8: `time="day"`, `cannon_fire=.8`, `fire=.4` |
| `tenochtitlan` | göl üstü ada kenti: **Templo Mayor** (5 kademe, çift merdiven, mavi-kırmızı iki tapınak; tepelerinde haçsız tüy/geometrik bantlı renkli sancaklar), iki yan piramit, düz çatılı beyaz evler, setyolları, ağaç kümeleri, Popocatépetl/Iztaccíhuatl; **önde göl: kanolar (tüylü savaşçılar) + İspanyol brigantinleri**; yangın göle yansır | İspanyol (brigantin) | c9: `time="dusk", fire=.6–.9` — saygılı, ihtişamlı tasvir (kan/ceset yok) |
| `toledo` | tepe üstü şehir: Alcázar (dört köşe kuleli kare blok), katedral kulesi, yığılı evler (yanan pencereler), yamaç boyunca basamaklı sur; önde nehir + kuşatma hattı | İmparatorluk/kraliyet | c3: `time="dusk"` veya `"day"`, `fire=.3`, kamera Alcázar'a: `SS.cam_on_city(.58, 1.6, y=380)` |

### Kamera
`SS.cam_on_city(x, zoom, y=0)` → şehir/sur katmanında (x: 0..1) bir noktaya güvenli kamera (y verilmezse sur tepesi). `SS.cam_on_gun(near, idx, zoom)` topçu mevzisine. Güvenli kayma: zoom 1.0'da |Δx|,|Δy| ≤ 190; zoom 1.7'de ≈ ±500 / ±380; `SS.safe_cam(x,y,z)` sıkıştırır. Öneriler: açılış geniş (960,540,1.0) → yavaş itme (1000,580,1.3); vurgu: sur/merdiven yakın plan.

### Performans (ms/kare, post dahil)
roma (yangın+merdiven+top) ≈ 170–195 · viyana day+top ≈ 140–170 (yağmurlu ≈ 100–130) · guns ≈ 125–150 · halkulvadi (5 gemi) ≈ 140–170 · tenochtitlan ≈ 140–170 · toledo ≈ 140–185. 810 kombinasyon (6 şehir × 3 zaman × 3 hava × 3 efekt × 5 kamera) hatasız.

### Bilinen kusurlar
- Toplar yandan çizilir (namlu sağa/sola); ateş yönü sur değil yan — stilize. Sur isabetleri rastgele noktalarda.
- Askerler sabit konumlarda "nöbet" tutar (hafif bob), saldıran hücum yürüyüşü yok; hücum hissi için merdiven tırmanışı + top ateşi + duman kullan.
- `ladders=True` yalnız roma/viyana/halkulvadi'de; tırmanan figürler eğik duran küçük siluet (döndürülmüş sprite).
- Tenochtitlan'da kara askeri yok (göl savaşı): kanolar/brigantinler ve piramit basamaklarındaki savunucular; piramit gece/ateş ışığında çok parlak görünebilir.
- Şehir katmanı zoom ≥ 1.9'da biraz yumuşaklaşır (katmanlar 1× piksel yoğunluğunda pişer).
