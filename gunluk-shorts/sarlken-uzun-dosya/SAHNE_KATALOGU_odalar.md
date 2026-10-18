# SAHNE KATALOĞU — oda-lab (iç mekân / gece yolu / tören salonu)

Dosyalar: `scenes_rooms.py` (sahneler) · `stage_rooms.py` (perspektif "kutu oda" + numpy ışıklandırma + figürler) · `props_rooms.py` (eşyalar).
Kullanım (hepsi aynı): `shot("theatre", a=…, scene="ad", cams=[(çapa,(x,y,zoom)),…], p=dict(...))`. Kamera koordinatı sahne tuvali (1920×1080, merkez 960,540), zoom 1.0–2.2 güvenli.
**İlk kare 3–6 sn "pişirme" yer** (bir kez; aynı `p` ile tekrar eden çekimler önbellekten gelir). Sonraki kareler 75–150 ms (önizleme + post dahil).
Işık dili: tek sıcak kaynak (mum/avize) + soğuk ay/gün ışığı gobo'su; sahneler zaten vinyetli; `theatre` şablonunun `vig=`, `dust_n=` parametreleri yine geçerli (toz için `dust_n=0` verip sahnenin kendi tozunu kullanabilirsin).
Kamera ipuçları genel: pencere/mum/figür gibi odak noktasına `(x,y)` ver; zoom ≥1.6'da kenarlara kaymamak için |x−960| ≤ 350, |y−540| ≤ 250 tut.

---
## `tower` — dar taş kule odası (Juana / Madrid hapsi / Wartburg)
`p`: `variant="tordesillas"|"cell"|"wartburg"` (tordesillas), `night=True`, `figure="woman"|"man"|"writer"|"none"` (varyanta göre: woman/man/writer), `candle=0..1.4` (1.0; alev boyutu, 0=mum yok), `moon=1.0` (ay ışığı/huzme çarpanı, 0=kapat).
- **tordesillas**: taş oda, alçak yatak, haç, masada mum+testi+kitap; parmaklıklı küçük pencere (ay görünür) ve zemine süzülen ay huzmesi; peçeli kadın tabureye oturmuş, başı pencereye kalkık.
  Kamera: `(0,(960,540,1.0))` → `(8,(990,330,1.9))` pencereye yavaş yaklaşma; kadın yakın plan `(850,780,1.7)`; mum yakın plan `(1290,740,2.0)`.
- **cell** (Madrid): daha kaba/karanlık taş, küçük yüksek pencere (3 dikey+2 yatay demir), sakallı erkek profilde pencereye uzanmış; sıra+masa+mum. Kamera: `(960,560,1.0)`→`(1010,330,1.8)`.
- **wartburg**: tahta lambri, kurşun çıtalı baklava pencere (ay+orman), yazı masası: yazan figür (tüy kalem), mum, kitaplar, yeşil çini soba, duvarda kılıç. Kamera: `(960,540,1.0)`→`(1010,600,1.5)` (yazan eli+mum), pencere `(1100,330,1.8)`.
Animasyon: mum titremesi (flame), alev ışığı, toz (ay huzmesinde mavi, mum çevresinde sıcak), figür nefesi. 
Kusur: cell'de figür çok koyu/ayrıntısız; wartburg'da yazar sakalsız (profil kaba).

## `counting_house` — bankacı sayım odası (Augsburg/Anvers)
`p`: `coins=0.55` (0..1; masadaki sikke sütunu/yığın miktarı), `coins_t=None|(t0,t1)` (yerel sn; 0→coins'e DOLAR, dyn'de çizilir — "850.000 florin" için), `clerks=2` (0..4 katip, iki yan + iki arka), `chandelier=True`, `balance_tilt=None` (rad; None=terazi hafif salınır).
Yeşil sıva+lambri, kirişli tavan, dama zemin, iki vitray pencere (gün batımı turuncusu, içeri turuncu huzmeler), altın avize (8 alev), 2 şamdan (3'er alev), açık defter, mühürlü mektup, divit, terazi, açık kasa (altın parıltılı), raf+defterler, sancak.
Kamera: genel `(960,560,1.0)`; masa/para `(960,820,1.7)`; terazi `(1010,800,2.0)`; avize `(960,300,1.5)`; katip `(250,760,1.7)`.
Ort. kare ≈ 110–135 ms. Kusur: katipler iri/ayrıntısız siluet; coins_t kullanılırsa sikkeler dyn'de çizilir (+8 ms).

## `electors_hall` — Frankfurt, yedi seçmen
`p`: `seats=7` (1..7; azalınca ortadan dışarı eksilir), `occupied=True` (koltuklarda adsız seçmen siluetleri: 3 mitre/piskopos, 3 kurhut, 1 taç), `light_t=None|(t0,t1)` (yerel sn; koltuklar SOLDAN SAĞA sırayla altın parlar — "yedi seçmen/yedi oy"), `daylight=1.0` (vitray ışığı çarpanı).
Taş salon, 3 sivri vitray pencere (arkadan parlak), zemine süzülen altın huzmeler, dama zemin üstünde altın halka+yıldız, yüksek arkalıklı oyma koltuklar yarım daire, iki yanda ayaktan şamdan.
Kamera: genel `(960,540,1.0)`; koltuk sırası `(960,640,1.6)`; orta koltuk `(960,560,2.1)`; sol uç `(560,640,1.9)`.
Ort. kare ≈ 90–135 ms.

## `aachen` — Palatin Şapeli, taç giyme
`p`: `crown_t=(1.5,5.5)` (yerel sn: taç huzme içinde başın üstüne iner, oturunca parlama), `crown_show=True` (inmeden önce yukarıda soluk görünür), `figure=True` (diz çökmüş genç Karl), `bishops=True` (iki piskopos+asa), `attend=True` (arka planda nedimler), `flash=1.0`.
İki katlı kırmızı/beyaz kemerli galeri (perspektif-doğru yan duvarlar), altın mozaik tavan, çark avize (16 alev), mermer dama zemin + altın madalyon, tavandan inen ışık huzmeleri.
Kamera: genel `(960,560,1.0)`; taç inişi `(980,720,1.8)`; taç+baş `(990,760,2.1)`; avize `(960,330,1.6)`.
Ort. kare ≈ 95–150 ms (parlama anında en yüksek).

(Sonraki sahneler aşağıya eklenecek: reichstag, road_night, cloister, bedroom, chapel, ransom_room, debate_hall.)
