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
| `flag` | `"#8E1F26"` | bayrak/tente rengi (yelken haçı da bu renk). **Yeşil ağırlıklı renk (ör. `#2F6B4A`) otomatik yarım ay + yıldız**, diğerleri haç/çapraz damga |
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
