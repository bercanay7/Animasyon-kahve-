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
