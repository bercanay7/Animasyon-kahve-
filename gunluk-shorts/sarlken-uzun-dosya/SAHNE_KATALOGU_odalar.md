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

---
## `reichstag` — Worms Reichstag'ı (1521)
`p`: `monk=True` (koridorda tek başına keşiş), `books=True` (keşişin önünde masada kitap yığını), `emperor=True` (uzak kürsüde tahtta küçük Karl + 4 yan seçmen), `crowd=True` (iki yanda ~60 kişilik sıralar), `monk_z=1000` (keşişin koridordaki derinliği: 700 yakın … 1500 uzak), `sun=1.0` (pencere ışığı çarpanı).
Uzun yüksek gotik salon: SOL duvarda sivri pencereler (çapraz huzmeler zemine/halıya düşer), sağ duvarda sancaklar, tavanda kirişler + 3 avize (24 alev), uçta 3 basamaklı kürsü + kırmızı baldaken + kartal sancağı + taht, ortada kırmızı halı.
Kamera: genel `(960,540,1.0)`; keşişe yaklaşma `(960,540,1.0)`→`(960,700,1.9)`; kürsü/Karl `(960,420,2.0)`; solda pencere huzmeleri `(700,520,1.5)`; yavaş geri çekilme `(960,640,2.0)`→`(960,540,1.0)`.
Anlatı ipucu: "tek başına keşiş" = `monk=True,books=False`; "kitaplar masada" = `books=True`; imparatorun bildirisi = kamera kürsüye.
Ort. kare ≈ 90–130 ms. Kusur: kalabalık siluetleri benzer (7 başlık varyantı); keşiş figürü `stage.figure("monk")` olduğundan figür-lab sürümüyle otomatik güncellenir.

## `road_night` — gece yolu (Worms→Wartburg · Innsbruck sedye kaçışı)
`p`: `litter=False` (True: kapalı sedye + 2 taşıyıcı), `riders=3` (0..6 atlı), `torches=3` (0..6 meşaleci), `rain=0.0` (0..1; yağmur+kalın bulut; >0.5 ay kaybolur), `mountains=True` (alp zirveleri; False: yumuşak ormanlı tepeler → Thüringen/Wartburg yolu), `moon=True`, `walk=14` (px/sn; kafile sahnede sağa ilerler, 0=durağan), `x0=None` (kafile başı x; None=ekranda ortalı), `dir=1` (1 sağa, −1 sola), `fog=0.5`.
Kafile yandan siluet (sırtta yol, ıslak yol/su birikintileri, ön planda kara yamaç+çam+ot), meşale alevleri titrer + kıvılcım, at+binici, sedye direkli taşıyıcılarla.
Önerilen: **Worms→Wartburg**: `litter=False, riders=4, torches=2, mountains=False, rain=0.3`, kamera `(960,760,1.1)`; **Innsbruck**: `litter=True, riders=2, torches=3, rain=0.8, mountains=True`, kamera `(960,760,1.2)`→ yavaş sağa `(1200,780,1.6)`.
Kamera: genel `(960,720,1.0)`; sedye yakın `(960,780,1.8)`; meşale `(1150,700,2.0)`.
Ort. kare ≈ 110–165 ms (yağmurlu ≈ 150–200). Kusur: at proporsiyonları basit (siluet için yeterli), alt 1/4 geniş siyah (başlık/altyazı alanı).

## `cloister` — Yuste manastır avlusu
`p`: `time="dusk"|"day"|"night"` (dusk), `monks=1` (0..3 gezen keşiş), `lamps=True` (galeri kemerlerinde lamba ışığı; day'de yok), `walk=1.0` (keşiş hızı çarpanı).
İki katlı kemerli galeri (arka+iki yan kanat perspektif-doğru), kiremit çatı, çan kulesi, ortada çim parter+kutu çiti, çeşme, 4 selvi, 2 turunç ağacı; dusk: turuncu-mor gökyüzü + lambalı kemerler; night: ay ışığı, tek meşaleli keşiş.
Kamera: genel `(960,600,1.0)`; çeşme/avlu `(960,820,1.5)`; galeri lambaları `(1100,560,1.8)`; selvi `(500,620,1.7)`.
Ort. kare ≈ 95–110 ms.

## `bedroom` — Yuste yatak odası
`p`: `candle=1.0` (0..1.4 alev boyutu/ışık; 0=mumsuz karanlık oda), `fade_candle_t=None|(t0,t1)` (yerel sn: mum küçülüp titreyerek söner → oda soğuk aya geçer, duman kıvrılır; **ilk pişirme ≈ 6–8 sn** çünkü iki ışık sürümü pişer), `patient=True` (yastığa yaslanmış yaşlı adam), `food=True` (komodinde yemek), `moon=1.0`.
Baldakenli yatak (kırmızı perdeler), pencere (ay), duvarda haç, komodin: mum+ekmek+kapaklı kap+testi.
Kamera: genel `(960,540,1.0)`; hasta+yastık `(560,720,1.8)`; mum+yemek `(1260,700,2.0)`; pencere `(1370,330,1.7)`.
Ort. kare ≈ 100–135 ms. Not: sönme sırasında ek tam-ekran koyu örtü (ucuz).

## `chapel` — mum ışıklı şapel
`p`: `coffin=True` (nefin ortasında siyah örtülü tabut + altın haç + 6 yüksek mum), `candles=1.0` (alev/ışık çarpanı), `mourners=3` (0..4 diz çökmüş keşiş), `incense=True` (tütsü).
Uzun yüksek nef, yan kemerler (üstte ay ışıklı pencereler), kirişli tonoz, yaldızlı retabl + haç + 6 sunak şamdanı, kırmızı kutsal lamba.
Kamera: genel `(960,560,1.0)`; tabut `(960,760,1.8)`; sunak `(960,420,1.7)`; itme `(960,600,1.0)`→`(960,780,1.9)`.
Ort. kare ≈ 110–150 ms.

## `ransom_room` — Cajamarca fidye odası
`p`: `fill_t=None|(t0,t1)` (yerel sn: altın yığını `fill0`→`fill` oranına DOLAR), `fill=1.0` (son seviye; `fill_t` yoksa sabit), `fill0=0.0`, `prisoner=True` (Atahualpa: tüylü başlık, kolu kırmızı çizgiyi gösterir), `soldiers=2` (0..3 İspanyol, sağ kapıda ışığa karşı siluet), `door=True`.
İnka taş işçiliği + trapez nişler, tüm duvarlarda yüksekte KIRMIZI çizgi, yüksek delikten giren ışık huzmesi (+ parlayan kapı huzmesi), altın eşyalar (vazo/aryballos, levha, kadeh, heykelcik, güneş diski, külçe) yığılır, parıltılar.
Kamera: genel `(960,540,1.0)`; yığına yaklaşma `(900,640,1.0)`→`(880,640,1.8)`; Atahualpa `(650,760,1.8)`; kapı/askerler `(1330,700,1.8)`; kırmızı çizgi `(960,420,1.5)`.
Ort. kare ≈ 90–150 ms (fill sırasında ≈ +10 ms).

## `debate_hall` — Valladolid 1550
`p`: `lecterns=2` (0..2: kaç kürsüde konuşmacı), `jury=7` (0..9 jüri üyesi), `crowd=True` (yan sıralar), `left="friar"`, `right="scholar"` (konuşmacı tipi: friar=keşiş/cüppe, scholar=birretli âlim), `sun=1.0`.
İki yandan çapraz huzmeli yüksek salon, arkada yüksek kürsüde yüksek arkalıklı koltuklar + yeşil örtülü masa + defter/mum, duvarda haç ve iki sancak (taç ↔ kitap), iki kürsü, kâtipler, yan sıralarda dinleyiciler.
Kamera: genel `(960,540,1.0)`; jüri `(960,620,1.8)`; sol konuşmacı `(580,800,1.7)`; sağ konuşmacı `(1340,800,1.7)`.
Ort. kare ≈ 90–130 ms.

---
### Genel notlar (tüm sahneler)
- **Perf**: ölçümler `preview.render_shot` (post dahil) ile; CPU paylaşımlı olduğundan ±40 ms oynama olur. En ağır: `road_night` yağmurlu (~200 ms), `electors_hall` ışık dizisinde (~140 ms).
- **Önbellek**: `theatre` yalnız son 5 sahne anahtarını tutar; aynı sahneyi farklı `p` ile üst üste çekimde değiştirirsen her biri yeniden pişer (3–8 sn).
- **Figürler**: `stage_rooms.ROOM_FIG` içinde `woman_seated, man_window, writer_seated, clerk_seated, elector_{mitre,kurhut,crown,galero,cap}, bishop_standing, king_kneel, monk_kneel, old_man_bed, atahualpa, horse_rider, torchbearer, bearer, litter, orator_{friar,scholar}, sit_{beret,cap,galero,mitre,hood}` — `stage_rooms.rfigure(f, kind, x, y_ayak, h, rim=…, rimd=…, face=±1)` ile başka sahnede de kullanılabilir (overlay=fn ile).
- **Işık dili**: sıcak mum (≈ #FF9C40) + soğuk ay/gün (≈ #7FA0E8) kenar ışığı; her sahne bir kez numpy ile gerçek ışıklandırılır (nokta ışık, ay gobo'su, kabartma/bump, köşe kararması).
