# Narkissos üslup kapısı: bağımsız denetim (Fable 5.2)

Karar ana oturumun. Benim önerim: **vazo**, ama kıl payı ve şartlı. Risograf dört ölçütün dördünü açık farkla kazanmıyor; kapının en iyi tek karesi ise risografın yakın planı.

## Kendi baktıklarım
- İki adayın 9 anahtar karesi, iki kapak, ölçüm ajanının 360p kırpım sayfası.
- Kendi ürettiklerim (`/tmp/claude-0/-home-user/d2cf6cd4-4d63-590c-86cd-58e0a7f88ab8/scratchpad/kapi/fable/`):
  - `kucuk_koyu.png`, `kucuk_acik.png`: kapak ve D_benim, 246/168/120 px, koyu ve açık zemin.
  - `seq_vazo.jpg`, `seq_riso.jpg`: mp4'ten 12 kare (0,3–4,0; 14,3–15,2; 17,2; 19,0).
  - `y360.png`, `y1080.png`: YouTube benzeri bit hızıyla kendi kodlamam (360p 450 kbit/sn, 1080p 2,5 Mbit/sn).

## Ölçüt 1: yakın plan baş "genç bir insan" mı
- Risograf: **geçiyor, net.** Kör okur altı karenin altısında "erkek, 18–25" dedi. Ben de öyle okuyorum: alın, burun, dudak, çene, kulak yerinde.
- Vazo: "genç, 16–25" okunuyor ama cinsiyeti belirsiz. Uzun saç + bant + sakalsız yüz + göğüs kavisi birlikte "üstü çıplak kadın" okumasına gidiyor.
- Bu ölçütte risograf açık farkla önde.

## Ölçüt 2: 246/168/120 px
- Kendi küçültmem: 120 px'te D_benim karesinde risografta yüz ve yansıma daha rahat seçiliyor; açık ten koyu saç ve orta ton zemin üç değer veriyor. Vazoda iki baş seçiliyor, ama soldaki gövde kütlesi belirsiz bir leke.
- Kapakta vazo önde: tek parlak nokta (yansıyan göz), yazı karşıtlığı yüksek. Risografta sarı yazı teal zeminde orta karşıtlıkta, odak gerçek yüz ile yansıma arasında bölünüyor.
- Koyu akışta vazonun kenarı kayboluyor (kendi ölçümüm: 168 px kenar bandı ort. 21, akış zemini 15). Risografın kenarı iki akışta da duruyor (96).
- Sonuç: **karışık, risograf hafif önde, açık fark yok.**

## Ölçüt 3: 480p/360p
- Hare görmedim. Kendi 360p/450 kbit kodlamamda durağan bölgede ardışık kare farkı risografta 0,017, vazoda 0,22: kodlayıcı greni donduruyor, titreme yok. **Geçiyor.**
- Ama ölçüm ajanının testi CRF'liydi: risograf 360p'de 408 kbit, 480p'de 1.117 kbit harcamış (vazonun 4–6 katı). YouTube bit hızını sınırlar.
- Kendi 1080p/2,5 Mbit kodlamam: PSNR vazo 49,2 dB, risograf **26,8 dB**. Durağan karede kabul edilebilir görünüyor; harekette yarım tonun bulanması beklenir. Bu, ölçütün sormadığı ama izleyicinin göreceği şey.

## Ölçüt 4: süre
- Risograf eşiği geçiyor (ort. 0,82; en kötü 1,38 sn). Tek işçide vazodan hızlı (1,00; p90 1,82).
- 4 işçide tersine dönüyor: 9 dk vazo ≈ 1,26 sa, risograf ≈ 2,02 sa. "Açık farkla kazanma" değil.
- Not: vazonun kendisi bu sahnede 1,5 sn eşiğini p90'da aşıyor. §5'teki 0,35–0,50 sn artık geçerli değil.

## Kural sonucu
- Risograf: 1 net, 3 ve 4 eşiği geçiyor, 2 karışık. Dördü birden açık fark değil → kural gereği vazo.
- Önyargı sınaması: risograf beklediğimden çok daha iyi çıktı. "Kuş gibi baş" itirazım düştü. Yine de kazanamıyor, çünkü açılış planı ve teknik bedel zayıf.

## Genel kalite
**Vazo**
- Güçlü: açılış. Dikey telefon, çentik, camda yüz: 0,3. saniyede "telefonuna bakan biri" okunuyor. Cam → havuz 2,6–3,2'de temiz.
- Zayıf: D planı. Gövde lekesi, göğüs kavisi, yumruk, burundan inen noktalı çizgi. Karanlık (kapak ort. Y 35).
- Zayıf: C. Kör okur "secde ya da yakarış, güçlü okuma" dedi (avuçlar yukarı).
- Açılışta 0,3–2,0 arası üç kare neredeyse aynı: donuk.

**Risograf**
- Güçlü: D yakın planı, palet, yansımanın halkayla dağılması (120 px'te bile görünüyor).
- Zayıf: telefon planları. Yatay ızgaralı dikdörtgen telefon okunmuyor (kör okur: akvaryum, lavabo, pencere); camdaki yüz seçilmiyor. Açılış sinyali yok.
- Zayıf: C'de çubuk figür, örtü altında çıplak okunan beden, ayak ucunda "telefon" gibi nesne.
- Dudak teması "öpüşme" okunuyor; kapakta "O BENİM" ile birlikte başka bir vaat.
- Dosya 9,6 kat büyük; son dört videodan sonra beşinci baskı dili.
- mp4 eski: 17,2. saniyede koyu benekler duruyor (kendi karemde gördüm).

## Tanıma hamlesi ('benim', 14,6) yazısız okunuyor mu
- İkisinde de **zayıf.**
- Vazo: 14,3 → 15,2 arasında yansıma biraz aydınlanıyor ve noktalı çizgi beliriyor. Çizgi burundan indiği için damla/salya okunuyor. Gecikmenin kilitlenmesi küçük baş hareketinde görünmüyor.
- Risograf: yeşilimsi yansıma sıcak tona dönüyor, gözde parıltı. 640 px'te ton değişimi olarak fark ediliyor, "anladı" diye değil.
- Öneri: Ovidius'un deneyi büyük bir hareketle yapılsın (el uzanır, yansımanın eli geç gelir; 'benim'de aynı karede buluşur, genç irkilir).

## Açılış: ilk 3 saniye
- Vazo: sinyal var. Eksikler: telefonu tutan el yok, 0–2,4 sn donuk, bugünün genci 25–35 yaş okunuyor.
- Risograf: sinyal yok.

## Kapak (kanal dersleri)
- İkisi de profil; ¾ kuralı karşılanmıyor (bilinen, kabul edilmiş açık).
- Harf yüksekliği ikisinde ≥ %19, rozet bölgesi boş, üslup filmle aynı.
- Vazo: tek odak ve en parlak nokta doğru yerde. Sorunlar: sol üstteki gövde ve 'c' halkası, yumruk, karanlık, koyu akışta kenar yok.
- Risograf: odak bölünmüş, yazı karşıtlığı orta, dudak teması.

## Vazo için düzeltmeler (1920×1080, sırayla)
1. D ve kapak: khiton görünür olsun. Göğüs kavisi (345–540, 230–330), ucundaki işaret (535, 330) ve 'c' halkası (488, 105) silinsin; boyun ve omuzda koyu sır kumaş kenarı çizilsin.
2. D: noktalı çizgi (900, 445–690) kaldırılsın ya da gerçek gözden (905, 350) yansıyan göze (900, 700) çekilsin.
3. Baş: enseye inen dalgalı uzun saç (620–850, 60–250) kısaltılsın; kulak açık, kısa bukle, bant kalsın.
4. Tanıma: el hareketiyle yeniden kurulsun (yukarıdaki öneri); yansımanın renk dönüşü korunur.
5. C: avuçlar yukarı eller (1100–1200, 500–545) kıyıyı kavrasın ya da tek el suya uzansın; omuzdaki noktalar (975–1040, 395–440) silinsin.
6. E ve A: yansıyan başın üstündeki elips (1185, 768) dalgalarla aynı parlaklıkta ve merkezde olsun.
7. A: telefonu tutan el; 0–2,4 sn'ye hareket (başparmak, ekran ışığı kıpırtısı); ceketli gövde (0–640, 180–1080) küçülsün, yüz büyüsün.
8. D: yumruk (750–1180, 880–1220 kapakta; D'de 370–590, 470–620) açık ele dönsün ya da kadraj dışına alınsın; koldaki kırmızı bant (205, 150) silinsin.
9. Kapak: ince kil kenar çizgisi ya da meander; ortalama parlaklık ~50'ye.
10. Düzeltmeden sonra D_benim ve C yeniden kör okura: "kim, kadın mı erkek mi, giyinik mi, ne yapıyor?"

## Risograftan vazoya taşınacaklar
- Kısa saçlı, kulağı açık, köşeli çeneli efeb başı.
- Halkada yansımanın kırık lekeye dağılması (vazoda 120 px'te kayboluyor).
- Kıyı çizgisi ve su ufku (yan görünüşte suyu okutuyor).
- Kıyıdaki beyaz çiçekler: nergis için hazır yer.
- "Yabancı yansıma" fikri: 'benim'e kadar kayık/soluk, sonra kayıtlı.

## Şüpheli sayılar
- Otsu eta risografta düşük çıkıyor, ama bu yarım ton dokusundan; okunurluğu ölçmüyor. Gözüm eta ile uyuşmuyor.
- odak.py vazoyu yapay parıltı yüzünden ödüllendiriyor; tıklamayı tahmin etmez.
- Ölçüt 3 testi bit hızı sınırsız yapıldı (bkz. yukarı).
- Hassasiyet raporu C'yi "secde değil" dedi, kör okur "güçlü secde/yakarış" dedi: çelişki, kör okur ağır basar.
- İki kurucunun "figürler giyinik" bildirimi karelerle uyuşmuyor.
- Rozet bölgesinde risografta tek piksel en çok 255 okudum (kâğıt noktaları); ortalama düz, sorun değil.

## En emin olmadığım
- Vazonun D planı düzeltmelerden sonra risografın yakın planı kadar çekici olur mu. Olmazsa kural vazoyu seçmiş, göz risografı seçmiş olur.
- Koyu, kil rengi kare geniş kitlede risografın açık paletinden iyi mi tıklanır: elimde veri yok.
