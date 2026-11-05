# P2–P7 için kurul tur 2'den kalan notlar (5 Kasım 2026)

Parça 1 düzeltmeleri sırasında ajanların ve kurulun, sonraki parçalara taşınması gereken bulguları. Her parçanın sahne turu başlamadan önce okunur.

## Motor / ortak
- `c3_kinds.DikeyP2` Duomo grubu konumu `XD=700` kopyasını taşıyor; P1'de 730'a alındı (çan kulesi kule kenarından taşıyordu; SCN-1/SCN-2, SA1-K3). P2'de de 730 yapılmalı ve önbellek silinmeli.
- c7/c8 madalya gölgeleri `pad=SHADOW_PAD` ile çizilmeli (ENG-C: gölge tuvali payı; SA1-E4).
- `act_sit_talk` (oturarak konuşma) gecikmeli ön kol takibini almadı (ENG-C açık kalan).
- Komşuya bağlı kopya çeşitlemesi yürüyen/kalabalık/alay/halka figürlerinde kapalı (sıçrama riski); yalnız tür+seed farkı var (ENG-C).
- Baş yalnız eğiliyor; karşıdaki figür arkadaysa dönmüyor (ENG-C).
- Giysi kesimi çağa bağlı değil; yalnız başlık, desen, çorap ve etek boyu (SA2-Ö4, ENG-C kısmen).
- Öteki odaların perdelerinde 1743 odasındaki basamaklı kenar hatası olabilir (SCN-1 yalnız oda1743'ü düzeltti).
- Yakın plan el: el boyu 26 px'i geçince parmak/boğum çiziliyor (ENG-C); yüz yakın planından kaçınma kuralı sürüyor.
- Damgalar: sahnelerde doğrudan `CM.stamp` yerine `anim.paper_stamp` (P1'de 14 çağrı çevrildi). P2–P7 kinds dosyalarında da aynısı yapılmalı.
- Bütün figürler temsilîdir; TEMSİLÎ damgası yalnız madalyalarda (KA2-D14 paket cümlesi).

## Kurul önerileri (P1'de kapsam dışı bırakılanlar)
- **Lorenzo madalyası (P3'ten önce, SA1 §4):** saçı 6–9 incelen, uçları düzensiz tutama böl, tepeye hacim; burnu uzat/bas, ucu aşağı; alt çene öne. Cossa ermin kenarı: camauronun alt çizgisinde düz bant, kulakta bitsin.
- **Cosimo genç/yaşlı ayrımı (P2–P3):** yaşlıda sarkık çene ve ince boyun, gençte dolgun yanak (SA1 §4).
- **Kişi yaşam aralığı kapısı (SA2 §6.3):** HUD yılında hayatta olmayan kişiyi niteleyicisiz gösteren levha için qa kapısı.
- **Bina listesi (SA2 §6.2):** Palazzo Medici ≥1444; Uffizi ≥1560; Pitti ≥1458 (büyük genişleme 1560'lar); "Santa Croce çan kulesi" etiketi (bugünkü 1842) ekranda kullanılacaksa teyit.
- **1438 sonrası madalyalar (SA2 §6.5, KA2):** TEMSİLÎ/"benzerlik iddiası yok" işareti tarihten bağımsız olmalı.
- **Seri başlık öneki (PK1-Y8):** P2–P7 `Medici Ailesi (n/7):` öneğine çekilecek; P5 62 karaktere çıkıyor → kısalt; P4 "Defter Neden Kapandı?" art arda NEDEN kuralına takılır.

## ENG-D'den (kamera, geçiş, bitiş ekranı)
- `compose.OUTRO` = 10 sn bütün parçalarda geçerli (yuvalar `OUTRO_SLOT_FULL` = 1,4 sn'de tam görünür; `TAIL` 11,3 sn); her parçanın miksi bu kuyrukla üretilir.
- Bitiş ekranındaki "sıradaki parça" satırı yalnız Parça 1 için tanımlı; P2–P6 için metin eklenmeli, P7 "TÜM FİLM".
- Skyline'da sahne hem `pan=` hem kamera pan'ı yazmışsa kaydırma miktarı artık kameranınki: bu çekimlere ilk render'da bakılmalı.
- `qa_flow` P2 duman testi: 13 GEÇTİ · 7 KALDI (5'i önceden vardı; yeniler: ışık geçişi 16 > 4 bütçe, #114 kamera "kısmen").
- Kesme ucundaki kamera eğimi (`CUT_SLOPE` 1,0) büyük kaydırmalı oda çekimlerinde ani kalkış gibi okunabilir; gerekirse 0,6–0,8.

## Kurul tur 3'ten (5 Kasım 2026)
- **Loggia terası (KA1, ●):** teras ve korkuluk 1583'te Buontalenti'nin eklemesi (it.wikipedia: "Nel 1583 … Bernardo Buontalenti creò sulla sommità della loggia una terrazza"; en.wikipedia: Uffizi'den sonra "the Loggia's roof was modified … and became a terrace"). `donem.loggia_stage` 1382 sonrasını "tam" sayıyor ve `cilt_sehir.loggia()` tam yapıyı teraslı çiziyor → 1382–1582 meydan sahnelerinde (ör. Savonarola 1497–98) anakronik. **Yapılacak:** dördüncü aşama: 1382–1582 çatı terassız ve korkuluksuz; 1583'ten sonra teras. Heykeller de çağa bağlansın: Perseus 1554, Sabin Kadınlarının Kaçırılışı 1583 (KA1 ◐) — qa_donem kuralı olarak.
- **Yakın plan el silueti (SA1 E-1, AN1):** ≥2× ara planda el öznenin kendisi; tek parça "kürek" siluet (kalın kontur, ayrık başparmak lobu, düz dolgu) ekrandaki en zayıf çizim. P2'den önce iki seçenek: (a) ara plan eli için ayrı siluet: parmak arası boşluklar, parmak uçları, bilek kirişi; (b) kadrajı nesneye daraltıp yalnız parmak uçlarını göstermek. Hareket: varışta `anim.settle` (%6–10 aşma), yolda 5–10° bilek dönüşü (AN1 Y-N2; P1'de c2 yakın planlarına uygulandı).
- **Deklanşör ipucu (AN1 Y7):** küçük hızlı nesne çizen her tür `anim.hint_speed(cx, anim.speed_of(...))` çağırmalı (eşik `compose.SHUTTER_V_HINT` 8 px/kare). P1'de c2 florin yağmuru ve damga düşüşleri bağlandı (SCN-3, ENG-E); P2–P7 türlerinde de taranmalı.
- **Kendi kamerasını kuran türler (AN1 Y-N3):** `OWN_CAMERA` türleri (`c2_masa`, `c2_yakin`, `c0_belge` …) sert kesmeyle birleşen uçta `cilt_cam.CUT_SLOPE` uygulamalı; yoksa kesme girişinde 1 karelik duruş olur.
- **Kart benzeri süre (PK2 N1, AN2 Ö1):** v3'te %46. Aynı kadraj (üstten açık defter, ekranı dolduran krem sayfa) bir parçada en çok iki kez; sayı yoğun bölgelerde "defter – yakın plan – defter – eğik/sandık" ritmi. qa_flow'a "aynı kadraj ailesi ≤2 / 120 sn" kapısı düşünülmeli.
- **Test kapağının vaadi (PK2 Y4 notu):** yankı yalnız varsayılan kapağa göre tasarlanır; test kapağının vaadi ilk 15 sn'de bir kez görsel olarak anılsın.
- **Bitiş ekranı başlangıcı (PK2 N2):** `paket_P*.bitis_zamanlari` öğeleri yuvalar TAM göründükten sonraki ilk tam saniyede başlatır (P1: 9:53). P2–P7 paket betikleri aynı işlevi kullanmalı.
