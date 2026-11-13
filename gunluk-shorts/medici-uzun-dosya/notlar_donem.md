# Dönem katmanı (`donem.py`) — kurallar, kaynaklar, uygulama yerleri (ENG-A, 4 Kasım 2026)

Kurul tur 1 kararı (KURUL.md B-2; SA2 B1–B4, KA1 G1/G2/S4): motor yıla bakmadan "son hâl" çiziyordu (1338'de kubbe, 1378'de Medici sancağı, 1429'da
PATER PATRIAE, 1465 öncesinde mavi zambaklı top). Artık tek doğruluk kaynağı `donem.py`; çizim kodu yılı oradan alır.

## 1. Yıl nereden gelir
* `compose` her karede `cx.year` (HUD yılı) yazar → `cilt_medici.ckind` sarmalayıcısı çekim çizilirken `donem.push(cx, tür)`, bitince `pop()`.
* **Çekim yılı** = çekim süresince HUD'da en uzun kalan yıl (`donem.shot_year`): HUD yılı çekimin ortasında dönse bile (YIL_AT sözcük çapası)
  yapı/arma çekim ortasında "pop" etmez. Bölüm kartı: kendi `years` metninin ilk yılı (II → 1397).
* **Yıl yoksa eski çizim:** `cx.year` yok/None, `Program(shots=…)` modu (reel, kapak `engine_frame`, qa çekim listesi — YearState boş, compose
  1397 varsayılanı verir; donem bunu çağrı yığınından tanır), marka türleri (`fresco_title`, `outro`). P2–P7 `Program(part=N)` ile yıl alır →
  aynı kurallar orada da işler (c4 kubbe inşası, c3 1433–64 arması vb.).

## 2. Kurallar ve kaynaklar
| öğe | kural (`donem.py`) | kaynak (erişim 4 Kas 2026, curl) |
|---|---|---|
| Duomo nefi | 1296 temel → 1378 orta nef örtüsü, 1380 yan nefler (`nave` 0→1; 1296 öncesi alçak eski Santa Reparata) | it.wikipedia *Cattedrale di Santa Maria del Fiore*: "Le navate furono completate con la copertura nel 1378 di quella centrale nel 1380 di quelle laterali" |
| tribünler + tambur | tribün 1380→1410 (iskeleli şantiye), tambur 1410→1415 | aynı madde: "Entro il 1421 vennero eseguite le tribune e il tamburo"; en.wikipedia *Florence Cathedral* (tambur 1410–13) |
| kubbe | 7 Ağu 1420 → 30 Ağu 1436; oran ≈ (y−1420)/16; yarımken açık sekizgen ağız + iskele + vinç | it.wikipedia *Cupola del Brunelleschi*: "Il 7 agosto 1420 ebbe inizio la costruzione… completata fino al cosiddetto serraglio… il 30 agosto 1436" |
| fener | 1446 başlar → 23 Nis 1461 (Antonio Manetti) biter; 1446–61 iskeleli yarım gövde; 1436–46 yalnız serraglio halkası | aynı madde: "I lavori iniziarono però solo nel 1446… terminati da Antonio Manetti il 23 aprile 1461"; en.wikipedia: "completed by… Michelozzo in 1461" |
| top + haç | ≥1471 (Verrocchio'nun yaldızlı bakır topu) | it.wikipedia kubbe maddesi "Completamento 1436 (1471 inclusa la lanterna)"; en.wikipedia "ball and cross… by Verrocchio in 1469" (sipariş; yerleştirme 1471) |
| çan kulesi | 19 Tem 1334 temel → 1337 Giotto ölürken yalnız ilk kat (≈0,15) → 1348 A. Pisano kabartma + niş katları (≈0,33; veba durdurur) → 1350–1359 Talenti üç pencereli kat → tam | it.wikipedia *Campanile di Giotto* ("Alla morte di Giotto nel 1337 solo il primo dado era compiuto"; "Andrea Pisano diresse il cantiere dal 1337 al 1348"); en.wikipedia *Giotto's Campanile* ("first stone 19 July 1334… Talenti… completing the bell tower in 1359") — ara oranlar görsel kestirim |
| Palazzo Vecchio (uzak siluet) | <1299 yok, 1299→1314 yükselir | genel bilgi (1299 başlangıç, 1314 tamam); yalnız skyline/pano uzak katmanında uygulanır, meydan sahnesinin ana cephesi değişmez |
| San Lorenzo büyük kubbesi | ≥1604 (Cappella dei Principi; Nigetti tasarımı) | it.wikipedia *Cappella dei Principi* ("progettato da Matteo Nigetti nel 1604"). Not: kubbenin bitişi 17. yy'ın içine uzanır; ≥1604 basitleştirme |
| Medici arması | ≤1464: mavi (Fransa zambaklı) top YOK — 8 kırmızı palle kenar boyunca (in orlo); ≥1465: üstte mavi top + 3 altın zambak, 5 kırmızı | it.wikipedia *Stemma dei Medici*: "Re Luigi XI di Francia, con un decreto emanato a Montluçon nel maggio del 1465, concesse a Piero il Gottoso…"; "fino a tutto il XV secolo… varianti… fino a undici palle". Commons: Cosimo il Vecchio "Campo d'oro a 8 bisanti rossi"; Giovanni di Bicci "a undici palle… 3,2,3,2,1" (Ceramelli Papiani) |
| sancak | Medici (palle) sancağı kamusal alay/kalabalıkta yalnız ≥1434 ve isyan/halk/lonca bağlamı dışında; izinsiz Medici → düz altın (SA2), kaynaksız mavi-sarı şerit → Komün zambağı; nötr: Popolo (beyaz zemin kırmızı haç), Komün (beyaz zemin kırmızı zambak), düz renk | kurul kararı (KURUL.md B-2, SA2 B2/K13, KA1 S4); 1434 = Cosimo'nun dönüşü (Medici yönetiminin başı) |
| madalya yazıtı | "PATER · PATRIAE" yalnız ≥1464; öncesi "COSMVS · MEDICES ·" | kurul kararı (SA2 B4); Signoria kararı 20 Mart 1465 = Floransa takviminde (yılbaşı 25 Mart) 1464 |

**Emin olunamayan (yazılı tutum):** palle sayısı 15. yy boyunca değişken (5–11); başkanın "6–8" bandında **8** seçildi (Cosimo dönemi kaydı) ve
bütün 1465 öncesi yıllara uygulandı (Giovanni di Bicci'nin 11'li varyantı çizilmez). 1465–69 arası Piero varyantları (3-2-1 diploma düzeni; 6+1 top)
çizilmez; ≥1465 Lorenzo dönemi 6'lı biçim kullanılır. Kaynak sayfaları: `/tmp/…/scratchpad/web/` (yalnız veri olarak okundu).

## 3. Uygulama yerleri (kim neyi okuyor)
| dosya | ne değişti |
|---|---|
| `cilt_city.py` | `draw_dome(stage=)` (tribün/tambur/yarım kubbe + açık ağız + iskele + vinç/fener yükselişi/top-haç), `draw_campanile(stage=)`, `draw_pv(stage=)`, `draw_duomo_group`, `city_layers(era=)` (önbellek anahtarı = dönem), `anchors()` (etiket çapası o yılın en üst noktası), `era_key/era_tag/note_era` |
| `cilt_pano.py` | `World(tod, era)`, `ERA_LAYERS` (yalnız Duomo'lu katman önbellek adı dönem eki alır), `get_world(…, era)`; Florence şehir katmanı |
| `cilt_sehir.py` | Meydan/Sokak/KaleSur/SkylineDikey Duomo grubu; Medici kalkanı (`medici_shield` varyantı); kalabalık sancakları (`flag_sub`) |
| `cilt_build.py` | kubbe yapım çekimi: ilerleme (p) çekimin kendi zaman atlaması, ama FENER ve TOP+HAÇ yılın kuralına uyar |
| `cilt_props.py` | `arms_array/arms_image/draw_arms(variant=)` — `red8` (≤1464) / `std` (≥1465) |
| `cilt_medici.py` | `ckind` → `donem.push/pop`; `mini_palle` varyantı (mühür izi) |
| `cilt_anim.py` | `flag_sprite` yeni cihazlar `medici_old` (8 palle) / `medici_new` (mavi top); alay sancakları `flag_sub` (bağlam `flag_ctx`) |
| `cilt_medal.py` | kenar yazısı `donem.medal_inscription` |
| `cilt_oda.py` | 1743 odasındaki arma yalnız o odada (1737–43: mavi top doğru) — kayda yazılır |
Değişmeyenler (gerekmedi): `cilt_scene.py` (Duomo çizmiyor), `kit_a.py`, `icons_extra.py` (cihazsız bayrak simgesi), `cilt_hero.py` (önizleme; yıl yok → eski).

## 4. Denetim
* `python3 qa_donem.py` — P1 her çekimden 3 kare **gerçekten çizilir**; çizim kodu `donem.note()` ile NE ÇİZDİĞİNİ yazar (kubbe/fener/top, çan kulesi,
  arma varyantı, sancak cihazı + istenen cihaz, madalya yazıtı); `qa_donem.check` kuralların donem.py'den BAĞIMSIZ kopyasıyla denetler.
  `--eski`: dönem katmanı kapalı (önce ölçümü). Çıktı `out_p1/duzeltme/ENG-A/qa_donem.json` (+ `qa_donem_eski.json`), çekim başına çizilen öğeler tablosu.
* Önbellek: dönem eki önbellek dosya adına girer (`cilt_city.ERA_VER`); aşamalı çizim kodu değişince `ERA_VER` artırılır.

## 5. Sonuç (4 Kasım 16:40; P1 güncel sahneler, c1s10'daki 2 eksik sözcük çapası cümle başına düşürülerek)
* `qa_donem.py`: dönem katmanı açık **0 ihlal** (303 kare, 336 kayıt) · `--eski` (katman kapalı) **95 ihlal / 17 çekim** (kubbe-fener-top 1338/1348/1378/1429,
  çan kulesi, San Lorenzo kubbesi, 3 mavi toplu arma, 2 Medici sancağı + 2 tarihsel olmayan cihaz, 1 PATER PATRIAE).
* P2–P7 duman testi: `Program(part=2..7)` kurulur, kareler çizilir (c3 1433 yarım kubbe, c4 1418 açık tambur, c4 yapım 1420 fenersiz, c7 1478 tam; 1537 alayında
  `medici_new` sancak). Kapak/reel (`Program(shots=…)`) yılsız → eski çizim (doğrulandı).
